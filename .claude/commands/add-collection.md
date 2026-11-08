---
description: 把 Zotero 收藏夾裡還沒整理的論文，一批一批加進文獻手帳
argument-hint: 收藏夾名稱，例如 "GEO consumer"
---

把 Zotero 收藏夾「$ARGUMENTS」裡還沒整理的論文加進文獻手帳。

依照 `CLAUDE.md` 第 4 節「一次新增多篇」的規則：

1. 執行 `python scripts/find_paper.py --collection "$ARGUMENTS" --missing`。
2. 先把清單給使用者看：每篇的標題、年份、有沒有 PDF，以及你建議的主題。沒有 PDF 的論文列出來但跳過。
3. 等使用者確認要整理哪幾篇，再開始。
4. 一篇一篇照第 4 節的步驟 2–4 完成，每篇寫完再讀下一篇。
5. 全部寫完後只執行一次同步與建置。
6. 回報每篇的一句話總結、新增的網頁路徑，以及需要使用者確認的內容。

不要執行 `git push`。
