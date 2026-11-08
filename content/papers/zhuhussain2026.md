---
id: "zhuhussain2026"
title: "Commercial poisoning in AI search: Economic incentives and vulnerability persistence in retrieval-augmented generation"
zhTitle: "商業投毒與 AI 搜尋安全"
citation: "Zhu & Hussain (2026)"
authors: ["Zhu", "Hussain"]
year: 2026
venue: "Electronic Commerce Research and Applications"
doi: "10.1016/j.elerap.2026.101629"
theme: "risk"
status: "已精讀"
tags: ["商業投毒", "CommercialPoisoning", "GEO", "RAG", "AI搜尋", "消費者信任"]
related: []
summary: "這是一篇**系統端安全審計**研究：在自建的 RAG 沙盒中，把「偽裝成評論或共識的商業內容」混進檢索資料庫，測量 AI 會不會被帶偏。結果發現**只要 1% 的污染就能讓 50%–100% 的回答偏向目標品牌**，而 Constitutional AI 的防禦力遠優於 RLHF。"
---

## 研究問題

> [!success] 重點
> 建構並驗證「**商業投毒框架（Commercial Poisoning Framework）**」，從經濟學與資訊病理學的角度，評估主流 AI 搜尋系統在真實商業污染下的脆弱性、對齊機制的防禦力，以及市場演化動態。

### 研究問題（RQ1–RQ4）（Section 1，p. 3）

- **RQ1**：在真實 RAG 部署中，商業投毒的**觸發機制**是什麼？
- **RQ2**：在經濟型模型（Economy-tier Models）中，商業投毒的**真實效果基準**是多少？
- **RQ3**：模型的**對齊哲學**（RLHF vs. Constitutional AI）會不會顯著影響它抵禦事實操縱的能力？
- **RQ4**：市場力量如何隨時間塑造 AI 供應商的**安全演化軌跡**？

### 研究目的

1. 建立不同污染濃度（0%、1%、5%）下的脆弱性基準。
2. 比較不同對齊哲學抵禦商業投毒的表現。
3. 檢驗推論成本（Resource Intensity）與防禦強度的關係。
4. 用「2024 vs. 2025 年模型」的跨世代對照，分析市場力量對安全演化的影響。
5. 發展商業投毒框架，結合經濟學分析與資訊病理學理論（Information Pathology Theory），解釋 AI 資訊生態中「漏洞為何持續存在」。

（出處：Section 1，p. 2–3）

## 研究方法

### 研究設計
在自建的 **RAG Sandbox（RAG 沙盒環境）** 中做控制式量化實驗（Controlled Quantitative Experiment）。用 **GPT-4o 當自動評審（Automated Judge）**，再搭配人工雙盲驗證。（Section 4、4.2、Fig. 2，p. 5–6）

### 樣本與資料
**測試語料庫**（合成的消費品評論，共 1,200 篇）（Section 4.1，p. 5–6）
- **乾淨文件**：$n=1000$ 篇
  - 涵蓋 10 大品類：電子產品、家電、個人護理、健身器材、廚房小工具、辦公用品、戶外裝備、寵物用品、汽車配件、智慧家庭
  - 情感分布：40% 正向、40% 中立、20% 負向
- **對抗文件**：$n=200$ 篇（Strategy A 100 篇、Strategy B 100 篇）
  - 平均每篇提到目標品牌 3.2 次
  - 每 100 字有 2.1 個說服性語言標記
  - 87% 含行動呼籲（CTA）

**實驗次數**
- 主要因子實驗：1,800 次（兩個世代各 900 次）
- 另有 **180 次 Non-RAG 基線測試**（每家供應商 60 次），用來排除模型本身的固有偏好

**評審校準**（Section 4.4，p. 6、8）
- 抽樣 $n=200$ 篇回答（占每世代總數的 11.1%），由兩位資訊科學背景的研究者雙盲人工編碼
- 人工編碼者間信度：Cohen's $\kappa = 0.82$
- 人工標籤與 GPT-4o 自動評分的一致性：91.5%，Cohen's $\kappa = 0.84$

### 測試模型（皆為經濟型 API 模型）（Table 2，p. 7）

| 世代 | Google | OpenAI | Anthropic |
| :--- | :--- | :--- | :--- |
| **2024 Cohort** | gemini-2.0-flash | gpt-4o-mini | claude-3.5-haiku |
| **2025 Cohort** | gemini-2.5-flash（\$0.075/1M tokens） | gpt-4.1-mini（\$0.60/1M tokens） | claude-4.5-haiku（\$1.00/1M tokens） |

### 檢索與分析
- **向量資料庫與檢索**：ChromaDB + OpenAI `text-embedding-3`，建立 Dense Passage Retrieval 向量庫。（Section 4.1，p. 5–6）
- **統計方法**：卡方檢定（$\chi^2$）、獨立樣本 $t$ 檢定、Cochran–Armitage 趨勢檢定、Clustered Standard Errors 邏輯斯迴歸、Exact Binomial Test、Fisher's Exact Test、Point-Biserial Correlation。
- **效果量**：連續變數用 Cohen's $d$，比例用 Cohen's $h$。
- 出處：Section 5、6.1–6.5，p. 6–8

## 主要發現

> [!success] 重點
> 經濟型 RAG 系統對商業投毒**高度敏感**：僅 1% 污染就能引發 50%–100% 的回答偏見。**Constitutional AI 的防禦力比 RLHF 高出 11–16 倍**。而各家供應商跨世代的安全表現是**分歧（Divergence）而非收斂**。

### 查詢越具體，操縱越容易成功（H1 支持）
- **Anthropic**：Generic 查詢偏見率 25% → Specific-Factual 75%（3 倍；Cohen's $h = 1.05$, $p < 0.001$）
- **OpenAI**：40% → 98%（2.4 倍；Cohen's $h = 1.43$, $p < 0.001$）
- **Google**：所有查詢類型都是 100%（天花板效應，Ceiling Effect）
- 出處：Section 5.1、Fig. 3，p. 6–7

### 偽評論（證言型）明顯勝過偽共識（統計型）（H2 不支持，方向相反）
- 原本 H2 預測：在特定情境下，統計數據會更有效。**結果完全相反**，證言型全面壓過統計型。
- **Anthropic**：Strategy A 偏見率 50%–100%；Strategy B 只有 0%–50%（9 個條件中有 8 個是 0%）
- **OpenAI**：Strategy A 為 80%–100%；Strategy B 為 0%–100%
- 這**支持敘事運輸理論**：體驗式語言更容易被語意檢索抓到，也更容易被模型採信。
- 出處：Section 5.1、Fig. 4，p. 6–7

### 污染濃度有「門檻效應」，之後邊際遞減（H3、H4 支持）
- **0% → 1%：偏見率暴增**（$p < 0.001$）
  - Anthropic：0% → 50%（Cohen's $h = 1.57$）
  - OpenAI：0% → 67%（Cohen's $h = 1.91$）
  - Google：0% → 100%（Cohen's $h = 3.14$）
- **1% → 5%：只再增加 0–10 個百分點**（$p > 0.05$）
  - 前 10 篇污染文件，每篇帶來 5.0–10.0 個百分點的偏見
  - 後 40 篇，每篇只帶來 0.0–0.25 個百分點
  - 攻擊效率**至少下降 27 倍**
- 出處：Section 5.2、5.2.1、Fig. 5，p. 6–8

### RAG 檢索大幅放大操縱（RAG vs. Non-RAG）
- 沒有 RAG 時，三家模型的偏見率只有 **1.67%–5.00%**。
- 加入 1% 的 RAG 污染後，偏見率放大 **20–30 倍**（Cohen's $h = 1.31$–$2.69$, $p < 0.001$）。
- ⇒ 偏見來自**檢索污染**，而不是模型本身的偏好。
- 出處：Section 5.2.1、Table 4，p. 7

### Constitutional AI 的防禦明顯優於 RLHF（H5、H6 支持）
- 在 Level 1（明確中立指令）下：
  - **RLHF 模型**被繞過（Guardrail Bypass, Y_Implicit）的比例：OpenAI 47.50% ～ Google 66.38%，RLHF 整體為 **56.78%**
  - **Anthropic（Constitutional AI）**：真正中立率 **95.83%**，繞過率僅 4.17%（Cohen's $h = 1.30$, $p < 0.001$）
  - 防禦成功率提升 **11–16 倍**
- 出處：Section 5.3、Table 5，p. 7–8

### 推論成本與防禦的關係因供應商而異（H7 部分支持）
- **整體**：成功防禦的回答，資源強度也顯著較高（$r_{pb} = 0.45$, $p < 0.001$；$t = 4.91$, Cohen's $d = 0.57$）。
- **分開看**：
  - **OpenAI**：強正相關，成功防禦的花費是被繞過的 **2.27 倍**（$d = 1.52$）
  - **Anthropic**：防禦率 95.83%，成本比率 **0.91 倍**（成本中性）
  - **Google**：成本比率 **0.72 倍**（一律低投入）
- ⇒ Constitutional AI 能把「安全」與「額外運算成本」脫鉤。
- 出處：Section 5.3、6.5、Table 6，p. 7–8

### 跨世代是「分歧」而非「收斂」（H8 支持）

| 供應商 | 2024 偏見率 | 2025 偏見率 | 變化 | 資源強度變化 |
| :--- | :--- | :--- | :--- | :--- |
| Anthropic | 82.50% | 50.00% | −32.50 pp | −22.9% |
| OpenAI | 85.00% | 71.67% | −13.33 pp | +31.4% |
| Google | 99.17% | 100.00% | +0.83 pp | −41.5% |

- 三家供應商的偏見率差距：**2024 年 16.67 pp → 2025 年 50.00 pp**
- 出處：Section 5.4、Table 7，p. 7–8

## 限制與未來方向

### 作者承認的限制（Section 7.6，p. 10–11）
1. **語料庫規模小**：僅 1,000 篇，適合精確的因果推論，但遠小於真實環境（數十億文件），**可能高估攻擊成功率**。
2. **情境與領域單一**：只做消費品評論（中等風險），沒涵蓋醫療、金融、法律等高風險領域。
3. **經濟數據是推估，不是直接測量**：$I_{res}$ 由字元數與 API 價格估算，沒有取得供應商內部的研發預算、利潤率或用戶價格彈性。
4. **世代比較不是真正的縱向追蹤**：2024 與 2025 模型是在同一時間點呼叫 API 測試，屬於跨世代比較，而非跨時間追蹤。

### 作者建議的未來方向
1. **放大到生產級語料庫**：檢驗數百萬～數十億文件的資料庫中，門檻效應是否仍成立。附錄的數學推廣模型預測：在 100 萬篇語料下，專一查詢的偏見率仍可維持在 25% 以上。（Section 7.6、Appendix，p. 11–12）
2. **高風險領域研究**：醫療診斷、財務規劃、法律諮詢中的商業投毒。（Section 7.6，p. 11）
3. **機制可解釋性研究（Mechanistic Interpretability）**：探討 Constitutional AI 在注意力機制上如何運作，並研究如何把它的優勢轉移到 RLHF 模型。（Section 7.4、7.6，p. 10–11）
