"""把 Obsidian 精讀筆記轉成公開版，寫入 content/papers/。

用法：
    python scripts/sync_notes.py

- 只保留 catalog.json 的 publicSections 列出的段落與一句話總結。
- 書目資料（作者、年份、出處、DOI）以 Zotero 為準，筆記 frontmatter 為備援。
- 不會修改 Vault 或 Zotero。
"""
import re
import sys
from pathlib import Path

import find_paper
from common import ROOT, dump_frontmatter, load_catalog, load_local_config, split_frontmatter

OUT = ROOT / "content" / "papers"
CALLOUT = re.compile(r"(?m)^> \[!(\w+)\][^\n]*\n(?:>[^\n]*\n?)*")
WIKILINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|([^\]]+))?\]\]")


def note_stem(name: str) -> str:
    return Path(name).stem


def concept_aliases() -> dict[str, str]:
    """[[GEO]] 這類連結對應到概念頁 id。"""
    aliases = {}
    for path in (ROOT / "content" / "concepts").glob("*.md"):
        meta, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        for alias in [meta.get("title"), meta.get("english"), *meta.get("aliases", [])]:
            if alias:
                aliases[str(alias).lower()] = path.stem
    return aliases


def rewrite_links(text: str, papers: dict[str, str], concepts: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        target, label = m.group(1).strip(), (m.group(2) or m.group(1)).strip()
        if target in papers:
            return f"[{label}](../papers/{papers[target]}.html)"
        if target.lower() in concepts:
            return f"[{label}](../concepts/{concepts[target.lower()]}.html)"
        return label  # 沒有對應頁面就只留文字
    return WIKILINK.sub(repl, text)


def citation(authors: list[str], year) -> str:
    if not authors:
        return f"（作者待補）({year})"
    if len(authors) == 1:
        name = authors[0]
    elif len(authors) == 2:
        name = f"{authors[0]} & {authors[1]}"
    else:
        name = f"{authors[0]} et al."
    return f"{name} ({year})"


def venue_label(venue: str | None, doi: str | None) -> str:
    if venue:
        return venue
    doi = (doi or "").lower()
    if "arxiv" in doi:
        return "arXiv 預印本"
    if "zenodo" in doi:
        return "Zenodo 預印本"
    return ""


def extract_sections(body: str, public: dict[str, str]) -> list[tuple[str, str]]:
    sections = []
    for part in re.split(r"(?m)^(?=## )", body):
        m = re.match(r"## (\d+)\.\s*[^\n]*\n", part)
        if not m or m.group(1) not in public:
            continue
        text = part[m.end():]
        text = CALLOUT.sub(lambda c: "" if c.group(1) == "question" else c.group(0), text)
        text = re.sub(r"(?m)^(#{3,6}) \d+(?:\.\d+)*\.?\s+", r"\1 ", text)  # 去掉 6.1 這類編號
        text = re.sub(r"(?m)^---\s*$", "", text).strip()
        sections.append((public[m.group(1)], text))
    return sections


def main() -> None:
    catalog = load_catalog()
    local = load_local_config()
    vault = Path(local["vault"])
    zotero_dir = Path(local["zotero"])
    zotero = {r["itemID"]: r for r in find_paper.search(find_paper.open_copy(zotero_dir), "", zotero_dir)}

    papers = {note_stem(p["note"]): p["id"] for p in catalog["papers"]}
    concepts = concept_aliases()
    theme_ids = {t["id"] for t in catalog["themes"]}
    OUT.mkdir(parents=True, exist_ok=True)
    warnings, written = [], set()

    for entry in catalog["papers"]:
        pid = entry["id"]
        src = vault / entry["note"]
        if not src.exists():
            warnings.append(f"{pid}：找不到筆記 {entry['note']}")
            continue
        if entry["theme"] not in theme_ids:
            warnings.append(f"{pid}：主題 {entry['theme']} 不在 themes 中")
        meta, body = split_frontmatter(src.read_text(encoding="utf-8"))
        zot = zotero.get(entry.get("zoteroId"), {})
        if entry.get("zoteroId") and not zot:
            warnings.append(f"{pid}：Zotero 找不到 itemID {entry['zoteroId']}")

        authors = zot.get("authors") or [a.strip() for a in re.split(r",|&", str(meta.get("authors", ""))) if a.strip()]
        year = zot.get("year") or meta.get("year")
        doi = zot.get("DOI") or meta.get("doi") or ""
        venue = venue_label(zot.get("venue") or meta.get("journal") or meta.get("venue"), doi)
        if str(meta.get("year")) != str(year):
            warnings.append(f"{pid}：筆記年份 {meta.get('year')} 與 Zotero {year} 不一致")

        h1 = re.search(r"(?m)^# (.+)$", body)
        zh = re.search(r"《(.+?)》", h1.group(1)) if h1 else None
        abstract = re.search(r"> \[!abstract\][^\n]*\n((?:>[^\n]*\n?)+)", body)
        summary = entry.get("summary") or (
            " ".join(l.lstrip("> ").strip() for l in abstract.group(1).splitlines()) if abstract else "")
        if not summary:
            warnings.append(f"{pid}：缺少一句話總結")

        links = re.search(r"(?ms)^## 相關連結\n(.*?)(?=^## |\Z)", body)
        related = []
        for m in WIKILINK.finditer(links.group(1) if links else ""):
            rid = papers.get(m.group(1).strip())
            if rid and rid != pid and rid not in related:
                related.append(rid)

        sections = extract_sections(body, catalog["publicSections"])
        if len(sections) != len(catalog["publicSections"]):
            warnings.append(f"{pid}：公開段落只找到 {len(sections)} 個，請檢查標題編號")

        out_meta = {
            "id": pid,
            "title": zot.get("title") or meta.get("title", ""),
            "zhTitle": zh.group(1) if zh else "",
            "citation": citation(authors, year),
            "authors": authors,
            "year": int(year) if str(year).isdigit() else year,
            "venue": venue,
            "doi": doi,
            "theme": entry["theme"],
            "status": meta.get("status", ""),
            "tags": [t for t in meta.get("tags", []) if t not in ("論文筆記", "碩論")],
            "related": related,
            "summary": rewrite_links(summary, papers, concepts),
        }
        md = "\n\n".join(f"## {name}\n\n{rewrite_links(text, papers, concepts)}" for name, text in sections)
        (OUT / f"{pid}.md").write_text(dump_frontmatter(out_meta) + "\n" + md + "\n", encoding="utf-8")
        written.add(f"{pid}.md")

    for stale in OUT.glob("*.md"):
        if stale.name not in written:
            stale.unlink()
            print(f"移除已不在清單中的 {stale.name}")

    print(f"已同步 {len(written)} 篇到 content/papers/")
    for w in warnings:
        print(f"  ⚠ {w}")
    if any("找不到筆記" in w for w in warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
