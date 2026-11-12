"""在 Zotero 書庫中找論文，印出書目資料與 PDF 路徑。

用法：
    python scripts/find_paper.py "algorithm discount"          # 用關鍵字找
    python scripts/find_paper.py --collections                  # 列出所有收藏夾
    python scripts/find_paper.py --collection "GEO consumer"    # 列出收藏夾裡的論文
    python scripts/find_paper.py --collection "GEO consumer" --missing
                                                                # 只列還沒寫進手帳的論文
    加上 --json 可輸出 JSON。

只讀取 zotero.sqlite 的暫存副本，不會修改 Zotero。
"""
import argparse
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

from common import load_catalog, load_local_config

FIELDS = ("title", "date", "publicationTitle", "proceedingsTitle",
          "volume", "pages", "DOI", "url")
PAPER_FILTER = """
    i.itemTypeID NOT IN (SELECT itemTypeID FROM itemTypes WHERE typeName IN ('attachment', 'note', 'annotation'))
    AND i.itemID NOT IN (SELECT itemID FROM deletedItems)
"""


def open_copy(zotero_dir: Path) -> sqlite3.Connection:
    src = zotero_dir / "zotero.sqlite"
    if not src.exists():
        sys.exit(f"找不到 Zotero 資料庫：{src}")
    tmp = Path(tempfile.gettempdir()) / "geo-notebook-zotero.sqlite"
    shutil.copyfile(src, tmp)  # Zotero 開著時原檔會被鎖住，所以讀副本
    # Zotero 開著時，最近的變更還在 -wal 檔裡，沒寫回主檔；要一起複製才讀得到最新資料
    wal = src.with_name(src.name + "-wal")
    tmp_wal = tmp.with_name(tmp.name + "-wal")
    tmp.with_name(tmp.name + "-shm").unlink(missing_ok=True)
    if wal.exists():
        shutil.copyfile(wal, tmp_wal)
    else:
        tmp_wal.unlink(missing_ok=True)
    return sqlite3.connect(tmp)


def describe(con: sqlite3.Connection, item_id: int, zotero_dir: Path) -> dict:
    rec = {"itemID": item_id}
    for name, value in con.execute(
        """SELECT f.fieldName, v.value FROM itemData d
           JOIN fields f ON f.fieldID = d.fieldID
           JOIN itemDataValues v ON v.valueID = d.valueID
           WHERE d.itemID = ?""", (item_id,)):
        if name in FIELDS:
            rec[name] = value
    rec["authors"] = [r[0] for r in con.execute(
        """SELECT c.lastName FROM itemCreators ic
           JOIN creators c ON c.creatorID = ic.creatorID
           WHERE ic.itemID = ? ORDER BY ic.orderIndex""", (item_id,))]
    rec["venue"] = rec.pop("publicationTitle", None) or rec.pop("proceedingsTitle", None)
    rec["year"] = (rec.get("date") or "")[:4]
    rec["pdf"] = [
        str(zotero_dir / "storage" / key / path.removeprefix("storage:"))
        for key, path in con.execute(
            """SELECT i.key, a.path FROM itemAttachments a
               JOIN items i ON i.itemID = a.itemID
               WHERE a.parentItemID = ? AND a.contentType = 'application/pdf'""",
            (item_id,))
        if path
    ]
    return rec


def search(con: sqlite3.Connection, keyword: str, zotero_dir: Path) -> list[dict]:
    like = f"%{keyword}%"
    ids = [r[0] for r in con.execute(
        f"""SELECT DISTINCT i.itemID FROM items i
            LEFT JOIN itemData d ON d.itemID = i.itemID
            LEFT JOIN itemDataValues v ON v.valueID = d.valueID
            LEFT JOIN itemCreators ic ON ic.itemID = i.itemID
            LEFT JOIN creators c ON c.creatorID = ic.creatorID
            WHERE {PAPER_FILTER} AND (v.value LIKE ? OR c.lastName LIKE ?)""", (like, like))]
    return [describe(con, i, zotero_dir) for i in ids]


def collections(con: sqlite3.Connection) -> list[dict]:
    rows = con.execute(
        f"""SELECT c.collectionID, c.collectionName, c.parentCollectionID,
                   (SELECT COUNT(*) FROM collectionItems ci JOIN items i ON i.itemID = ci.itemID
                    WHERE ci.collectionID = c.collectionID AND {PAPER_FILTER})
            FROM collections c ORDER BY c.collectionName""").fetchall()
    return [{"id": r[0], "name": r[1], "parent": r[2], "count": r[3]} for r in rows]


def in_collection(con: sqlite3.Connection, name: str, zotero_dir: Path) -> list[dict]:
    all_cols = collections(con)
    match = [c for c in all_cols if c["name"] == name] or \
            [c for c in all_cols if name.lower() in c["name"].lower()]
    if not match:
        sys.exit(f"找不到收藏夾「{name}」。用 --collections 查看所有收藏夾。")
    if len(match) > 1:
        sys.exit("符合的收藏夾不只一個，請寫完整名稱：" + "、".join(c["name"] for c in match))
    # 包含子收藏夾
    wanted, frontier = {match[0]["id"]}, [match[0]["id"]]
    while frontier:
        parent = frontier.pop()
        for c in all_cols:
            if c["parent"] == parent and c["id"] not in wanted:
                wanted.add(c["id"])
                frontier.append(c["id"])
    marks = ",".join("?" * len(wanted))
    ids = [r[0] for r in con.execute(
        f"""SELECT DISTINCT i.itemID FROM collectionItems ci JOIN items i ON i.itemID = ci.itemID
            WHERE ci.collectionID IN ({marks}) AND {PAPER_FILTER}""", tuple(wanted))]
    return [describe(con, i, zotero_dir) for i in ids]


def print_papers(results: list[dict]) -> None:
    if not results:
        print("找不到符合的論文。")
        return
    for r in results:
        print(f"[{r['itemID']}] {r.get('title')}")
        print(f"    作者：{', '.join(r['authors']) or '（無）'}")
        print(f"    年份：{r['year'] or '（無）'}　出處：{r['venue'] or '（無）'}")
        print(f"    DOI：{r.get('DOI') or '（無）'}")
        for p in r["pdf"]:
            print(f"    PDF：{p}")
        if not r["pdf"]:
            print("    PDF：（沒有附件，無法整理）")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keyword", nargs="?", help="標題、期刊、DOI 或作者姓氏的關鍵字")
    parser.add_argument("--collections", action="store_true", help="列出所有收藏夾")
    parser.add_argument("--collection", metavar="名稱", help="列出這個收藏夾（含子收藏夾）的論文")
    parser.add_argument("--missing", action="store_true", help="只列出還沒加入 catalog.json 的論文")
    parser.add_argument("--json", action="store_true", help="以 JSON 輸出")
    args = parser.parse_args()

    zotero_dir = Path(load_local_config()["zotero"])
    con = open_copy(zotero_dir)

    if args.collections:
        cols = collections(con)
        if args.json:
            print(json.dumps(cols, ensure_ascii=False, indent=2))
        for c in cols:
            if not args.json:
                indent = "    " if c["parent"] else ""
                print(f"{indent}{c['name']}（{c['count']} 篇）")
        return

    if args.collection:
        results = in_collection(con, args.collection, zotero_dir)
    elif args.keyword:
        results = search(con, args.keyword, zotero_dir)
    else:
        parser.error("請提供關鍵字，或使用 --collections / --collection")

    total = len(results)
    if args.missing:
        done = {p.get("zoteroId") for p in load_catalog()["papers"]}
        results = [r for r in results if r["itemID"] not in done]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    print_papers(results)
    if args.missing:
        no_pdf = sum(not r["pdf"] for r in results)
        print(f"\n共 {total} 篇，其中 {total - len(results)} 篇已在手帳裡，"
              f"{len(results)} 篇還沒整理（{no_pdf} 篇沒有 PDF）。")


if __name__ == "__main__":
    main()
