---
id: "martinez2026"
title: "Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023-2026)"
zhTitle: "生成引擎最佳化（GEO）關鍵文獻綜述"
citation: "Martinez (2026)"
authors: ["Martinez"]
year: 2026
venue: "arXiv 預印本"
doi: "10.48550/arXiv.2607.14035"
theme: "engine"
status: "已精讀"
tags: ["GEO", "CriticalSurvey", "MultistagePipeline", "VisibilityVector", "EvidenceHierarchy", "文獻綜述"]
related: ["aggarwal2024", "chen2025", "kumarpalkhouski2025", "arshad2026", "zhuhussain2026", "hu2026", "changpark2026"]
summary: "這是一篇**批判性文獻綜述**，系統性檢視了 45 篇 GEO／RAG 論文，提出「多階段因果管線」「可見度向量」「實證階層」三套框架。核心結論很犀利：**業界宣稱的「GEO 提升 40% 可見度」嚴重誇大**，目前學術界幾乎沒有任何強實證證明 GEO 能真正改善有機檢索或帶來長期商業轉換；最穩健的槓桿只有「主題相關性」與「上下文位置」。"
---

## 研究問題

> [!success] 重點
> 對 2023–2026 年間 45 篇 GEO 及相關 RAG／評測文獻做系統性批判審視，建立 GEO 的多階段因果管線模型、可見度向量與實證階層，釐清哪些 GEO 技術真的有可複現的效力。

### 四大核心論文主張（Propositions）（Section 1，p. 2）

1. **GEO 是多階段管線**：有機可檢索性、上下文排名、引用、顯著性、事實吸收、流量，是不同階段的獨立變數——優化某個階段可能反而損害另一個階段。
2. **可見度是動態分佈**：它會隨引擎、日期、地點、Prompt 換句話說、搜尋觸發狀態與生成隨機性變動，單點測量不代表穩定指標。
3. **現有實證高度受限於檢索後條件**：實驗只證實「已放入上下文的文件」可以被改寫操縱，但幾乎沒證實能提升「有機檢索」，更完全沒證實能帶來持久的商業轉換。
4. **優化與操縱共享同一管道**：有益的內容重寫、對抗性序列、間接 Prompt 注入，本質上都是在修改模型消耗的文本，規範邊界應該建立在真誠性與透明度上。

## 研究方法

### 研究設計
**批判性範疇綜述**（Critical Scoping Review）與**文獻計量審計**。（Section 2.1）

### 樣本來源與篩選
- 涵蓋 **2023 年 11 月 16 日至 2026 年 7 月 14 日**間發布或接受的 **45 篇核心研究**
- 檢索來源：arXiv、ACM Digital Library、ACL Anthology、NeurIPS、PMLR、OpenReview 等
- **篩選標準**：論文須符合以下至少一項——定義／評估 GEO 干擾技術、測量商業引擎可見度／穩定性／忠實度、研究攻擊／防禦機制、或建構 GEO 經濟與外在性模型

（出處：Abstract、Section 2.1、2.2）

### 分析與編碼方法
- 對 45 篇文獻做結構化編碼：出版狀態（Peer-reviewed / Forthcoming / Preprint）、管線階段、系統類型（Controlled vs. Commercial）、測量單位、核心發現、效度威脅
- 提出**可複現 GEO 測量協定（Minimum Protocol）**：強調以 Prompt 為群集的階層模型（Hierarchical Models with Clustering），要求多次重複（7–8 次）、換句話說（Paraphrases）、時間縱向監測

（出處：Section 2.2；Appendix B, Table 8；Section 6.2、11.2、11.3）

## 主要發現

> [!success] 重點
> **主題相關性與上下文位置**是最穩健的兩大槓桿；**通用啟發式策略泛化不良**，甚至可能損害檢索；商業引擎間來源重複率極低且高度不穩定；目前學術界**完全缺乏強實證**證明 GEO 能長期改善有機可檢索性或帶來真實商業轉換。

### 主題相關性與上下文位置是最穩健的兩大槓桿
- 提高網頁在上下文中的位置（Context Position）對引用的影響，超越絕大多數文本改寫技術。
- Vishwakarma et al. (2026) 在 **252,000 次試驗**中證實：相關性與位置是決定首次引用的主導因素。
- 出處：Section 7.1；Table 4、5

### 通用啟發式策略普遍泛化不良，甚至損害檢索

| 研究 | 發現 |
| :--- | :--- |
| **C-SEO Bench**（16,360 篇文件） | 54 種方法－領域組合中，只有 **3 種**呈顯著正向；QA 任務中**完全沒有**顯著正向 |
| **E-GEO**（電商） | 15 個初始啟發式中，**10 個**是中性或負向 |
| **SAGEO Arena**（完整管線測試） | 僅對內文（Body-only）做 GEO 重寫，會讓網頁 Top-20 出現率下降約 **9%**，重排序後 Top-10 下降 **16%**，最終引用下降 **6%** |

- ⇒ 在檢索後有效的改寫，可能在檢索上游產生負面干擾。
- 出處：Section 7.3、7.4；Table 1、5

### 商業引擎間來源重複度極低
- Grossman et al. (2026)：在 11,500 個查詢中，Google 有機 SERP、AI Overviews（AIO）與 Gemini 之間的 URL 層級 Jaccard 重複率只有 **0.11–0.18**。
- Kirsten et al. (2026)：**53%** 被 Google AIO 引用的網域根本不在 Google 有機 SERP 前 10 名，**27%** 不在前 100 名。
- 出處：Section 8.1；Table 5

### 生成結果具備高動態不穩定性
- Kirsten et al. (2026) 觀察跨 2 個月：AIO 頁面重複率只有 **18%**；即使控制 Temperature=0，重複運行仍有 **9%–28%** 的決策會改變。
- 出處：Section 6.2

### 認知（Recognition）與發現（Discovery）之間有巨大鴻溝
- Sharma (2026) 測試 112 家新創公司：ChatGPT 在**直接點名**時能識別 **99.4%** 的產品，但在**通用類別購物查詢**中只能推薦 **3.32%**（Perplexity 從 94.3% 驟降至 8.29%）。
- 出處：Section 8.4

### 流量與轉換的實證證據極度脆弱（整篇綜述實證最弱的一環）
> [!warning] 關鍵結論
> 目前文獻中**沒有任何一項 GEO 技術被證明能對有機可檢索性或下游流量與轉換，產生長期、跨平台的穩定因果效應**。商業宣稱嚴重超越了學術實證。

- 出處：Abstract、Section 8.5、10；Table 5

## 限制與未來方向

### 作者承認的限制
- 綜述涵蓋 45 篇論文，**部分未經 Peer-review**（Preprints）
- 任務異質性高，導致無法做定量 Meta-analysis
- 商業 AI 系統持續更新，資料只能是快照

（出處：Section 2.1、2.3、2.4）

### 未來研究方向（Section 13）
1. **連結爬取、索引與生成的全管線測試**：擴展到商業系統的真實爬取與檢索驗證。
2. **因果測量「事實吸收度」與真實人類注意力**：結合眼動儀、點擊與轉換數據，評估引用的真實心理與經濟價值。
3. **多角色競爭平衡模型**：研究當 100% 的市場參與者都做 GEO 時的博弈結果。
