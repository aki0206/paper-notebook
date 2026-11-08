"""把 content/ 建置成 docs/ 靜態網站，並執行隱私與連結檢查。

用法：
    python scripts/build.py

任何檢查失敗都會以非零狀態結束，網站不算完成。
"""
import hashlib
import html
import math
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

import markdown

from common import ROOT, load_catalog, split_frontmatter

DOCS = ROOT / "docs"
CONTENT = ROOT / "content"
TEMPLATE = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
KATEX = (
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>'
)
NAV = [("index.html", "文獻"), ("compare.html", "對照表"),
       ("concepts/index.html", "概念"), ("about.html", "關於")]
ARROW = ('<span class="arrow" aria-hidden="true"><svg viewBox="0 0 16 16" width="14" height="14">'
         '<path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

esc = html.escape


# ---------- 角色 ----------

def blob_svg(seed: str, color: str, *, cls: str = "blob", eyes: bool = True, label: str = "") -> str:
    """依 seed 產生固定形狀的圓滾滾角色：不規則圓形 + 兩顆小眼睛。"""
    h = hashlib.md5(seed.encode("utf-8")).digest()
    n = 7
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + (h[0] / 255) * 0.8
        r = 30 + (h[i + 1] / 255) * 15
        pts.append((50 + r * math.cos(a), 52 + r * math.sin(a) * 0.92))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):  # Catmull-Rom 轉三次貝茲，讓輪廓平滑
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    face = ""
    if eyes:
        ex = 44 + (h[9] / 255) * 12
        ey = 44 + (h[10] / 255) * 12
        gap = 7 + (h[11] / 255) * 3
        face = (f'<ellipse cx="{ex - gap:.1f}" cy="{ey:.1f}" rx="2.6" ry="3.6" fill="#111111"/>'
                f'<ellipse cx="{ex + gap:.1f}" cy="{ey:.1f}" rx="2.6" ry="3.6" fill="#111111"/>')
    aria = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 100 100" {aria}>'
            f'<path d="{d} Z" fill="{color}"/>{face}</svg>')


LOGO = blob_svg("文獻手帳-logo", "#111111", cls="logo", eyes=False).replace(
    "</svg>", '<ellipse cx="42" cy="47" rx="4" ry="5.5" fill="#F7F3EF"/>'
              '<ellipse cx="58" cy="47" rx="4" ry="5.5" fill="#F7F3EF"/></svg>')


# ---------- Markdown ----------

def normalise_lists(text: str) -> str:
    """Obsidian 允許清單緊貼段落、用兩格縮排；Python-Markdown 需要空行與四格縮排。"""
    out, prev = [], ""
    for line in text.splitlines():
        m = re.match(r"^( *)([-*+]|\d+\.) ", line)
        if m:
            indent = len(m.group(1))
            line = " " * (indent // 2 * 4) + line[indent:]
            if prev.strip() and not re.match(r"^\s*([-*+]|\d+\.) ", prev) and not prev.startswith((">", "|")) and indent == 0:
                out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def callouts(text: str) -> str:
    """> [!success] 標題 → 粉彩提示卡。"""
    def repl(m: re.Match) -> str:
        kind, title = m.group(1).lower(), m.group(2).strip()
        body = "\n".join(re.sub(r"^> ?", "", l) for l in m.group(3).splitlines())
        head = f'<p class="callout-title">{esc(title)}</p>\n' if title else ""
        return f'\n<div class="callout callout-{kind}" markdown="1">\n{head}\n{body}\n\n</div>\n'
    return re.sub(r"(?m)^> \[!(\w+)\]([^\n]*)\n((?:>[^\n]*(?:\n|$))*)", repl, text)


def render_md(text: str) -> tuple[str, bool]:
    stash: list[str] = []

    def keep(m: re.Match) -> str:
        stash.append(m.group(0))
        return f"\x00MATH{len(stash) - 1}\x00"

    text = text.replace("\\$", "&#36;")  # 跳脫的金額符號，不是數學式
    text = re.sub(r"\$\$.+?\$\$", keep, text, flags=re.S)
    text = re.sub(r"(?<![\\$\w])\$(?=\S)[^$\n]+?(?<=\S)\$(?!\w)", keep, text)
    text = re.sub(r"==(\S(?:[^=\n]*\S)?)==", r"<mark>\1</mark>", text)
    text = callouts(normalise_lists(text))
    out = markdown.markdown(text, extensions=["tables", "fenced_code", "md_in_html", "sane_lists"])
    out = re.sub(r"<table>", '<div class="table-scroll"><table>', out).replace("</table>", "</table></div>")
    out = re.sub(r"\x00MATH(\d+)\x00", lambda m: f'<span class="math">{esc(stash[int(m.group(1))])}</span>', out)
    return out, bool(stash)


def inline_md(text: str) -> str:
    out, _ = render_md(text)
    return re.sub(r"^<p>(.*)</p>$", r"\1", out.strip(), flags=re.S)


def plain(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*_`]", "", text)


# ---------- 資料 ----------

def load_dir(path: Path) -> list[dict]:
    items = []
    for f in sorted(path.glob("*.md")):
        meta, body = split_frontmatter(f.read_text(encoding="utf-8"))
        meta.setdefault("id", f.stem)
        meta["body"] = body
        items.append(meta)
    return items


# ---------- 版型 ----------

def page(catalog: dict, *, path: str, title: str, content: str, description: str = "",
         body_class: str = "", math_on: bool = False) -> None:
    root = "../" * path.count("/")
    current = ' aria-current="page"'
    nav = "\n    ".join(
        f'<a href="{root}{href}"{current if href == path else ""}>{label}</a>' for href, label in NAV)
    foot_nav = "".join(f'<a href="{root}{href}">{label}</a>' for href, label in NAV)
    theme_css = ":root{" + "".join(f"--theme-{t['id']}:{t['color']};" for t in catalog["themes"]) + "}"
    site = catalog["site"]
    out = TEMPLATE
    for key, value in {
        "title": esc(title if title == site["title"] else f"{title}｜{site['title']}"),
        "description": esc(description or site["subtitle"]),
        "root": root, "theme_css": theme_css, "head_extra": KATEX if math_on else "",
        "body_class": body_class, "site_title": esc(site["title"]), "nav": nav, "foot_nav": foot_nav,
        "repo": site["repo"], "logo": LOGO, "content": content,
        "foot_blob": blob_svg("footer", "#FFB5C1", cls="foot-blob"),
    }.items():
        out = out.replace("{{" + key + "}}", value)
    target = DOCS / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")


def chip(theme: dict, tag: str = "span", extra: str = "") -> str:
    return f'<{tag} class="chip" style="--chip:var(--theme-{theme["id"]})"{extra}>{esc(theme["name"])}</{tag}>'


def paper_card(p: dict, theme: dict, root: str = "") -> str:
    text = plain(p["summary"])
    short = text if len(text) <= 64 else text[:62] + "…"
    search = " ".join([p["citation"], p["title"], p.get("zhTitle", ""), text, *p.get("tags", [])]).lower()
    return f"""<a class="paper-card" href="{root}papers/{p['id']}.html" data-theme="{p['theme']}" data-year="{p['year']}" data-search="{esc(search)}" style="--theme:var(--theme-{p['theme']})">
  <span class="paper-art">{blob_svg(p['id'], theme['color'])}</span>
  <span class="paper-cite">{esc(p['citation'])}</span>
  <span class="paper-title">{esc(p.get('zhTitle') or p['title'])}</span>
  <span class="paper-summary">{esc(short)}</span>
  <span class="paper-foot">{chip(theme)}{ARROW}</span>
</a>"""


def build_index(catalog, papers, themes, concepts):
    site = catalog["site"]
    years = sorted({p["year"] for p in papers})
    counts = {t["id"]: sum(p["theme"] == t["id"] for p in papers) for t in catalog["themes"]}
    chips = "".join(
        chip(t, "button", f' type="button" data-filter-theme="{t["id"]}" aria-pressed="false"')
        for t in catalog["themes"])
    year_opts = "".join(f'<option value="{y}">{y}</option>' for y in years)
    cards = "\n".join(paper_card(p, themes[p["theme"]]) for p in papers)
    theme_cards = "".join(
        f'<a class="theme-card" href="compare.html#t-{t["id"]}" style="--theme:var(--theme-{t["id"]})">'
        f'<span class="theme-count">{counts[t["id"]]}<small>篇</small></span>'
        f'<span class="theme-name">{esc(t["name"])}</span><span class="theme-desc">{esc(t["description"])}</span>'
        f'{blob_svg("theme-" + t["id"], "#FFFFFF", cls="theme-blob")}</a>'
        for t in catalog["themes"])
    concept_cards = "".join(
        f'<a class="concept-mini" href="concepts/{c["id"]}.html"><span>{esc(c["title"])}</span><small lang="en">{esc(c.get("english", ""))}</small>{ARROW}</a>'
        for c in concepts)
    hero_art = "".join(
        blob_svg(f"hero-{i}", color, cls=f"hero-blob hb{i}")
        for i, color in enumerate(["#B7E1D1", "#FFB5C1", "#FFFFFF"]))
    content = f"""
<section class="bento hero-row">
  <div class="card hero">
    <p class="eyebrow">LITERATURE NOTEBOOK</p>
    <h1>{esc(site['title'])}</h1>
    <p class="hero-sub">{esc(site['subtitle'])}</p>
    <div class="hero-actions">
      <a class="btn" href="#papers">開始閱讀{ARROW}</a>
      <a class="btn btn-ghost" href="compare.html">看對照表{ARROW}</a>
    </div>
  </div>
  <div class="card hero-art" aria-hidden="true">
    {hero_art}
    <div class="bubble"><strong>{len(papers)}</strong> 篇精讀<br><span>{years[0]}–{years[-1]} 出版</span></div>
  </div>
</section>

<section class="bento theme-row" aria-label="研究主題">
  {theme_cards}
</section>

<section class="card block" id="papers" aria-labelledby="cards-h">
  <div class="block-head">
    <div><p class="eyebrow">PAPERS</p><h2 id="cards-h">文獻卡片</h2></div>
    <p class="count" aria-live="polite"><span id="shown">{len(papers)}</span> / {len(papers)} 篇</p>
  </div>
  <div class="filters">
    <div class="chips" role="group" aria-label="依主題篩選">
      <button type="button" class="chip chip-all" data-filter-theme="" aria-pressed="true">全部</button>{chips}
    </div>
    <div class="filter-row">
      <label class="field"><span class="sr-only">年份</span><select id="year"><option value="">全部年份</option>{year_opts}</select></label>
      <label class="field grow"><span class="sr-only">搜尋</span><input id="q" type="search" placeholder="搜尋作者、標題、關鍵字"></label>
    </div>
  </div>
  <div class="paper-grid" id="cards">
{cards}
  </div>
  <p class="empty" id="empty" hidden>這個條件下沒有論文，換個關鍵字試試。</p>
</section>

<section class="bento duo-row">
  <div class="card block" aria-labelledby="concept-h">
    <div class="block-head"><div><p class="eyebrow">CONCEPTS</p><h2 id="concept-h">概念</h2></div><a class="more" href="concepts/index.html">全部{ARROW}</a></div>
    <div class="concept-list">{concept_cards}</div>
  </div>
  <a class="card about-card" href="about.html">
    <p class="eyebrow">ABOUT</p>
    <h2>這本手帳<br>怎麼做的？</h2>
    <p>一句「整理這篇」，AI 就照同一套規則寫筆記、做網頁。</p>
    {blob_svg("about", "#FFFFFF", cls="about-blob")}
    <span class="about-arrow">{ARROW}</span>
  </a>
</section>
"""
    page(catalog, path="index.html", title=site["title"], content=content, body_class="home")


def build_paper(catalog, p, papers, themes, index):
    theme = themes[p["theme"]]
    body_html, has_math = render_md(p["body"])
    sections = re.findall(r"<h2>(.*?)</h2>", body_html)
    for i, name in enumerate(sections, 1):
        body_html = body_html.replace(f"<h2>{name}</h2>", f'<h2 id="s{i}">{name}</h2>', 1)
    toc = "".join(f'<a href="#s{i}">{n}</a>' for i, n in enumerate(sections, 1))

    by_id = {x["id"]: x for x in papers}
    related = [by_id[r] for r in p.get("related", []) if r in by_id]
    same = [x for x in papers if x["theme"] == p["theme"] and x["id"] != p["id"] and x not in related]
    related = (sorted(related, key=lambda x: x["theme"] != p["theme"]) + same)[:4]
    rel_cards = "\n".join(paper_card(r, themes[r["theme"]], "../") for r in related)

    prev_p = papers[index - 1] if index > 0 else None
    next_p = papers[index + 1] if index + 1 < len(papers) else None
    pager = '<nav class="pager" aria-label="上一篇與下一篇">'
    pager += f'<a class="btn btn-ghost" href="{prev_p["id"]}.html">← {esc(prev_p["citation"])}</a>' if prev_p else "<span></span>"
    pager += f'<a class="btn btn-ghost" href="{next_p["id"]}.html">{esc(next_p["citation"])}{ARROW}</a>' if next_p else "<span></span>"
    pager += "</nav>"

    doi = f'<a href="https://doi.org/{esc(p["doi"])}">{esc(p["doi"])}</a>' if p.get("doi") else "（待補）"
    tags = "".join(f"<li>#{esc(t)}</li>" for t in p.get("tags", []))
    content = f"""
<div class="bento paper-top" style="--theme:var(--theme-{p['theme']})">
  <header class="card paper-head">
    <a class="back" href="../index.html#papers">← 回到文獻卡片</a>
    <div class="head-chips">{chip(theme)}<span class="chip chip-plain">{p['year']}</span></div>
    <p class="paper-cite-lg">{esc(p['citation'])}</p>
    <h1>{esc(p.get('zhTitle') or p['title'])}</h1>
    <p class="orig-title" lang="en">{esc(p['title'])}</p>
    <dl class="biblio">
      <div><dt>作者</dt><dd>{esc(', '.join(p.get('authors', [])) or '（待補）')}</dd></div>
      <div><dt>出處</dt><dd>{esc(p.get('venue') or '（待補）')}</dd></div>
      <div><dt>DOI</dt><dd>{doi}</dd></div>
    </dl>
    <ul class="tags">{tags}</ul>
  </header>
  <div class="card paper-portrait">{blob_svg(p['id'], theme['color'], cls='portrait-blob', label=p['citation'] + ' 的角色')}</div>
</div>

<aside class="card summary-card" aria-label="一句話總結">
  <p class="eyebrow">ONE-LINE SUMMARY</p>
  <p class="summary-text">{inline_md(p['summary'])}</p>
</aside>

<article class="card block paper-body" style="--theme:var(--theme-{p['theme']})">
  <nav class="toc" aria-label="本頁目錄">{toc}</nav>
  <div class="prose">
{body_html}
  </div>
</article>

<section class="card block" aria-labelledby="rel-h">
  <div class="block-head"><div><p class="eyebrow">READ NEXT</p><h2 id="rel-h">接著讀</h2></div></div>
  <div class="paper-grid small">{rel_cards}</div>
  {pager}
</section>
"""
    page(catalog, path=f"papers/{p['id']}.html", title=p["citation"], content=content,
         description=plain(p["summary"])[:150], body_class="paper-page", math_on=has_math)


def build_compare(catalog, papers, themes):
    blocks = []
    for t in catalog["themes"]:
        rows = "".join(
            f"<tr><td><a href=\"papers/{p['id']}.html\">{esc(p['citation'])}</a></td>"
            f"<td>{esc(p.get('zhTitle') or p['title'])}</td><td>{esc(p.get('venue') or '')}</td>"
            f"<td>{inline_md(p['summary']).replace('../papers/', 'papers/').replace('../concepts/', 'concepts/')}</td></tr>"
            for p in papers if p["theme"] == t["id"])
        blocks.append(f"""
<section class="card block compare-block" id="t-{t['id']}" style="--theme:var(--theme-{t['id']})">
  <div class="block-head"><div>{chip(t)}<p class="theme-line">{esc(t['description'])}</p></div>
  {blob_svg("theme-" + t["id"], t["color"], cls="compare-blob")}</div>
  <div class="table-scroll"><table class="compare">
    <thead><tr><th scope="col">論文</th><th scope="col">主題</th><th scope="col">出處</th><th scope="col">一句話總結</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</section>""")
    content = f"""
<section class="card page-head">
  <p class="eyebrow">COMPARE</p>
  <h1>文獻對照表</h1>
  <p class="lead">依研究視角分成 {len(catalog['themes'])} 組，一眼看出每篇論文在研究脈絡裡的位置。</p>
</section>
{''.join(blocks)}"""
    page(catalog, path="compare.html", title="文獻對照表", content=content)


def build_concepts(catalog, concepts, papers, themes):
    by_id = {p["id"]: p for p in papers}
    colors = ["#FFE59A", "#FFB5C1", "#B7E1D1", "#A9D3FF"]
    cards = "".join(
        f'<a class="concept-card" href="{c["id"]}.html" style="--theme:{colors[i % 4]}">'
        f'{blob_svg("concept-" + c["id"], "#FFFFFF", cls="concept-blob")}'
        f'<span class="concept-name">{esc(c["title"])}</span>'
        f'<span class="concept-en" lang="en">{esc(c.get("english", ""))}</span>'
        f'<span class="concept-def">{esc(plain(c.get("short", "")))}</span>{ARROW}</a>'
        for i, c in enumerate(concepts))
    page(catalog, path="concepts/index.html", title="概念", content=f"""
<section class="card page-head">
  <p class="eyebrow">CONCEPTS</p>
  <h1>概念</h1>
  <p class="lead">讀這些文獻常遇到的名詞，每個都用白話解釋，並連回原本的論文。</p>
</section>
<section class="bento concept-grid">{cards}</section>""")
    for i, c in enumerate(concepts):
        body_html, has_math = render_md(c["body"])
        rel = "\n".join(paper_card(by_id[x], themes[by_id[x]["theme"]], "../") for x in c.get("papers", []) if x in by_id)
        color = colors[i % 4]
        page(catalog, path=f"concepts/{c['id']}.html", title=c["title"], math_on=has_math,
             description=plain(c.get("short", "")), content=f"""
<div class="bento paper-top" style="--theme:{color}">
  <header class="card paper-head">
    <a class="back" href="index.html">← 所有概念</a>
    <p class="eyebrow">CONCEPT</p>
    <h1>{esc(c['title'])}</h1>
    <p class="orig-title" lang="en">{esc(c.get('english', ''))}</p>
  </header>
  <div class="card paper-portrait">{blob_svg("concept-" + c["id"], "#FFFFFF", cls="portrait-blob")}</div>
</div>
<aside class="card summary-card"><p class="eyebrow">IN ONE LINE</p><p class="summary-text">{inline_md(c.get('short', ''))}</p></aside>
<article class="card block" style="--theme:{color}"><div class="prose">{body_html}</div></article>
<section class="card block"><div class="block-head"><div><p class="eyebrow">PAPERS</p><h2>出現在這些論文</h2></div></div><div class="paper-grid small">{rel}</div></section>""")


def build_about(catalog):
    meta, body = split_frontmatter((CONTENT / "about.md").read_text(encoding="utf-8"))
    body_html, _ = render_md(body)
    page(catalog, path="about.html", title=meta.get("title", "關於"), content=f"""
<div class="bento paper-top" style="--theme:var(--theme-consumer)">
  <section class="card page-head"><p class="eyebrow">ABOUT</p><h1>{esc(meta.get('title', '關於'))}</h1></section>
  <div class="card paper-portrait">{blob_svg("about", "#FFFFFF", cls="portrait-blob")}</div>
</div>
<article class="card block"><div class="prose">{body_html}</div></article>""")


# ---------- 檢查 ----------

def check(catalog, papers, concepts) -> list[str]:
    errors = []
    terms = catalog["privateTerms"]
    for f in [*CONTENT.rglob("*.md"), *DOCS.rglob("*.html")]:
        text = f.read_text(encoding="utf-8")
        for t in terms:
            if t in text:
                errors.append(f"隱私：{f.relative_to(ROOT)} 含有「{t}」")
    for f in DOCS.rglob("*.html"):
        for href in re.findall(r'href="([^"#]+)', f.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:)", href):
                continue
            if not (f.parent / unquote(href)).resolve().exists():
                errors.append(f"連結：{f.relative_to(ROOT)} → {href} 不存在")
    ids = {p["id"] for p in papers}
    for c in concepts:
        for pid in c.get("papers", []):
            if pid not in ids:
                errors.append(f"概念：{c['id']} 引用了不存在的論文 {pid}")
    return errors


def main() -> None:
    catalog = load_catalog()
    themes = {t["id"]: t for t in catalog["themes"]}
    order = [p["id"] for p in catalog["papers"]]
    papers = sorted(load_dir(CONTENT / "papers"), key=lambda p: order.index(p["id"]) if p["id"] in order else 999)
    concepts = load_dir(CONTENT / "concepts")

    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(ROOT / "assets", DOCS / "assets")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    build_index(catalog, papers, themes, concepts)
    for i, p in enumerate(papers):
        build_paper(catalog, p, papers, themes, i)
    build_compare(catalog, papers, themes)
    build_concepts(catalog, concepts, papers, themes)
    build_about(catalog)

    warnings = [f"{p['id']}：缺少 {k}" for p in papers for k in ("authors", "venue", "doi") if not p.get(k)]
    errors = check(catalog, papers, concepts)
    pages = len(list(DOCS.rglob("*.html")))
    print(f"已建置 {pages} 個頁面到 docs/（{len(papers)} 篇論文、{len(concepts)} 個概念）")
    for w in warnings:
        print(f"  ⚠ {w}")
    for e in errors:
        print(f"  ✗ {e}")
    if errors:
        sys.exit("建置檢查失敗，請修正上面的問題。")
    print("檢查通過：沒有隱私字詞，內部連結都正確。")


if __name__ == "__main__":
    main()
