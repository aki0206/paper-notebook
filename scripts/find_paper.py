"""在 Zotero 書庫中找論文，印出書目資料與 PDF 路徑。

用法：
    python scripts/find_paper.py "algorithm discount"
    python scripts/find_paper.py "algorithm discount" --json

只讀取 zotero.sqlite 的暫存副本，不會修改 Zotero。
"""
import argparse
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

from common import load_local_config

FIELDS = ("title", "date", "publicationTitle", "proceedingsTitle",
          "volume", "pages", "DOI", "url")


def open_copy(zotero_dir: Path) -> sqlite3.Connection:
    src = zotero_dir / "zotero.sqlite"
    if not src.exists():
        sys.exit(f"找不到 Zotero 資料庫：{src}")
    tmp = Path(tempfile.gettempdir()) / "geo-notebook-zotero.sqlite"
    shutil.copyfile(src, tmp)  # Zotero 開著時原檔會被鎖住，所以讀副本
    return sqlite3.connect(tmp)


def search(con: sqlite3.Connection, keyword: str, zotero_dir: Path) -> list[dict]:
    like = f"%{keyword}%"
    item_ids = [r[0] for r in con.execute(
        """
        SELECT DISTINCT i.itemID FROM items i
        JOIN itemTypes t ON t.itemTypeID = i.itemTypeID
        LEFT JOIN itemData d ON d.itemID = i.itemID
        LEFT JOIN itemDataValues v ON v.valueID = d.valueID
        LEFT JOIN itemCreators ic ON ic.itemID = i.itemID
        LEFT JOIN creators c ON c.creatorID = ic.creatorID
        WHERE t.typeName NOT IN ('attachment', 'note', 'annotation')
          AND i.itemID NOT IN (SELECT itemID FROM deletedItems)
          AND (v.value LIKE ? OR c.lastName LIKE ?)
        """, (like, like))]

    results = []
    for item_id in item_ids:
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
        results.append(rec)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keyword", help="標題、期刊、DOI 或作者姓氏的關鍵字")
    parser.add_argument("--json", action="store_true", help="以 JSON 輸出")
    args = parser.parse_args()

    zotero_dir = Path(load_local_config()["zotero"])
    con = open_copy(zotero_dir)
    results = search(con, args.keyword, zotero_dir)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
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
            print("    PDF：（沒有附件）")


if __name__ == "__main__":
    main()
