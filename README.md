# 文獻手帳

研究所讀過的論文精讀筆記網站，一篇一頁。目前以 GEO（生成式引擎最佳化）與 AI 消費者行為為主。

**網站：** https://aki0206.github.io/paper-notebook/

## 這個專案在做什麼

讀論文原本要經過 Zotero → NotebookLM → Claude → Obsidian 四段手動搬運。這個專案把規則寫進 [`CLAUDE.md`](CLAUDE.md)，讓 AI 直接讀 Zotero 裡的 PDF，寫出固定格式的筆記，再自動產生網站。

```
Zotero（私人） → Obsidian 精讀筆記（私人） → content/（公開版） → docs/（網站）
```

## 新增一篇論文

在 Claude Code 輸入：

```
/add-paper 論文關鍵字
```

AI 會依照 `CLAUDE.md` 第 4 節完成找論文、寫筆記、更新清單、建置與檢查。

一次整理整個 Zotero 收藏夾：

```
/add-collection GEO consumer
```

AI 會先列出收藏夾裡還沒整理的論文讓你確認，再一篇一篇完成。

## 手動執行

需要 Python 3.10 以上：

```bash
pip install -r requirements.txt
cp local.config.example.json local.config.json   # 填入 Vault 與 Zotero 路徑
python scripts/find_paper.py "關鍵字"               # 查 Zotero
python scripts/find_paper.py --collection "名稱" --missing   # 收藏夾裡還沒整理的論文
python scripts/sync_notes.py                        # Vault → content/papers/
python scripts/build.py                             # content/ → docs/，含隱私與連結檢查
python -m http.server 8765 --directory docs         # 本機預覽
```

## 目錄

| 路徑 | 用途 |
|---|---|
| `CLAUDE.md` | 給 AI 的專案規則 |
| `data/catalog.json` | 論文清單、主題、公開段落白名單、隱私字詞 |
| `content/` | 公開版筆記、概念頁、說明頁 |
| `templates/` | 筆記範本與網頁版型 |
| `assets/` | 樣式與 JavaScript |
| `scripts/` | 查詢、同步、建置工具 |
| `docs/` | GitHub Pages 發布的網站 |

## 授權與聲明

筆記是個人閱讀整理，只公開部分段落；論文版權屬原作者，引用前請閱讀原文。
