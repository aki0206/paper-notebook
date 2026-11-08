---
id: "shanqiu2026"
title: "Examining the Impact of Generative AI on Users' Voluntary Knowledge Contribution: Evidence from a Natural Experiment on Stack Overflow."
zhTitle: "生成式 AI 對用戶自願知識貢獻的影響：Stack Overflow 自然實驗證據"
citation: "Shan & Qiu (2026)"
authors: ["Shan", "Qiu"]
year: 2026
venue: "Information Systems Research (INFORMS)"
doi: "10.1287/isre.2023.0332"
theme: "platform"
status: "已精讀"
tags: ["GenerativeAI", "ChatGPT", "VoluntaryKnowledgeContribution", "StackOverflow", "SocialLearningTheory", "CognitiveLoadTheory", "DifferenceInDifferences"]
related: ["aggarwal2024", "chen2025", "kumarpalkhouski2025", "arshad2026", "zhuhussain2026", "hu2026", "changpark2026", "martinez2026", "zhang2027", "jmis2025", "sikhondze2025"]
summary: "採用生成式 AI（ChatGPT）能顯著提升問答平台上用戶自願知識貢獻的「數量」與「品質」：使用 ChatGPT 使用戶每日回答數量顯著增加 **16.77%**，回答長度平均減少 **22.64 個字**，可讀性提升（理解所需教育年數減少 **2.165 年**）。「累積使用量」會透過「學習機制」強化此正向影響，但「短時間使用強度」會因「認知負擔」而減弱對回答數量的提升效果。"
---

## 研究問題

> [!success] 重點
> 使用生成式 AI 是否會影響用戶自願知識貢獻的數量、長度與可讀性？「累積使用量」與「使用強度」如何調節此影響？

### 研究問題
1. **RQ1**：在問答平台上，使用生成式 AI（GenAI）是否會影響用戶自願知識貢獻的回答數量、回答長度與可讀性？
2. **RQ2**：ChatGPT 的「累積使用量（Cumulative Usage）」與「使用強度（Usage Intensity）」如何調節生成式 AI 對用戶知識貢獻（數量、長度、可讀性）的影響？

### 研究目的
- 結合社會學習理論與認知負擔理論，檢驗生成式 AI 影響用戶知識貢獻的雙重機制（學習機制 vs. 認知負擔機制）。
- 為問答平台管理者（如 Stack Overflow）評估是否限制或如何規範生成式 AI 提供實證依據。

## 研究方法

### 研究設計
- **雙重差分法（Difference-in-Differences, DID）**：利用 ChatGPT 發布（2022/11/30）至 Stack Overflow 宣布禁用（2022/12/05）之間的自然實驗。
- 採用雙向固定效應模型（Two-Way Fixed Effects Model：包含 User Fixed Effects 與 Day Fixed Effects）。

### 樣本來源與樣本數
- 資料抓取自 Stack Overflow 平台（2022 年 9 月 1 日至 2022 年 12 月 4 日）。
- 原始資料涵蓋 223,696 位用戶、3,238,381 個問題與 1,254,841 個回答。
- 基準模型面板資料（User-Day level）包含 **578,480 個觀察值**；經動態傾向分數配對後樣本為 **58,512 個觀察值**。

### 處理組辨識（Treatment Identification）
1. 主要使用 OpenAI **GPT-2 Output Detector** 辨識回答是否來自 ChatGPT（正確率最高達 99.3%）。
2. 輔助使用 **ChatGPT API** 對相同問題生成答案，計算文本重疊度 Jaccard Overlap Index（閾值設為 > 0.9，允許用戶進行微幅改寫）。
3. 對真實 Stack Overflow 用戶發放問卷，證實此辨識演算法的分類準確度達 **83.02%**。

### 內生性與穩健性檢定方法
- **插補估計量（Imputation Estimator）**：解決處理時機不一（Staggered Adoption）與處理反轉（Treatment Reversal）導致的係數偏誤，並檢驗平行趨勢假設（Parallel Trend Assumption）。
- **配對技術（Matching Techniques）**：結合動態傾向分數配對（PSM + DID，Caliper matching 1-to-1 鄰近選取）與粗化精確配對（CEM + DID），消除可觀察變數的自選擇偏誤。
- **兩階段 Heckman 選擇修正模型**：納入外生工具變數 `CNAGOC`（其他用戶累積使用 ChatGPT 生成回答數）計算 Inverse Mills Ratio (IMR)，排除未觀察到的參與意願偏誤。
- **虛假檢定（Falsification Tests）**：1,000 次 Placebo 偽處理隨機賦予實驗，並進行去除 AI 答案後僅分析原生答案的檢定。
- **置換檢定（Permutation Tests）**：模擬 10% 控制組標籤錯誤的最壞情境。

## 主要發現

> [!warning] 關鍵結論
> 使用生成式 AI 使回答數量增加 16.77%、長度減少 22.64 字、可讀性改善 2.165 年；累積使用量強化學習效果；短時間使用強度則因認知負擔抑制回答數量。即使禁令後，用戶寫作風格仍持續向 ChatGPT 靠攏，顯示內化學習已發生。

### 主效應：提升數量與品質（H1 & H2 支持）
- **回答數量（H1）**：使用生成式 AI 工具能使用戶每天產生的回答數量顯著增加 **16.77%**（$\exp(0.155) - 1, p < 0.001$）。
- **回答長度（H2）**：採用生成式 AI 使回答平均長度顯著減少 **22.64 個字**（$p < 0.001$）。
- **可讀性（H2）**：採用生成式 AI 使 Gunning Fog Index 顯著下降 **2.165 年**（$p < 0.001$），代表理解該回答所需的教育年數減少，內容變得更通俗易懂。

### 累積使用量之調節：驗證「學習機制」（H3a & H3b 支持）
- **累積使用強化數量（H3a）**：`Treatment × Cumu_usage` 交互作用項對 `Log(NumAnswer)` 為顯著正向（$\beta = 0.296, p < 0.001$）。
- **累積使用強化品質（H3b）**：對回答長度的縮短效果額外增強 **2.582 字**（$\beta = -2.582, p < 0.001$），對可讀性指數的改善額外增強 **0.490 年**（$\beta = -0.490, p < 0.001$）。說明用戶在重複互動中學到了 AI 的精簡表達與結構化呈現技巧。

### 使用強度之調節：驗證「認知負擔機制」（H4a 支持，H4b 不支持）
- **強度抑制數量（H4a）**：`Treatment × Intensity` 交互作用項對 `Log(NumAnswer)` 為顯著負向（$\beta = -0.021, p < 0.001$）。說明短時間內極高頻率地使用 ChatGPT 會引發認知疲勞，進而降低回答產出量。
- **對品質之調節不顯著（H4b）**：`Treatment × Intensity` 對長度與可讀性的交互作用項未達統計顯著水準。

### 風格轉移與持久學習（Style Alignment）
即使在 Stack Overflow 禁令生效後（Post-ban），用戶自己撰寫的原生回答（Organic answers）在長度、極性、主觀性與可讀性上，依然持續向 ChatGPT 的寫作風格靠攏（長度差異縮小 4.807 字、可讀性差異縮小 1.868）。證實用戶發生了內化的技巧學習（Internalized Learning）。

### 用戶問卷調查驗證
對 Stack Overflow 用戶發放的問卷顯示，超過 **75%** 的受訪者表示在使用 ChatGPT 答題時「總是」或「經常」體驗到學習效果與認知負擔。

## 限制與未來方向

### 研究限制
- **外部有效性局限**：研究情境僅限於 Stack Overflow 程式開發問答平台。
- **觀察窗口較短**：ChatGPT 在平台發布至禁令僅有 5 天（2022/11/30–2022/12/05），無法觀察極長期的動態演化。
- **處理組辨識演算法非 100% 精確**：準確度為 83.02%，且無法完全區分「直接複製貼上」與「深度人機改寫」的個案差異。
- **認知負擔未生理化測量**：僅透過使用強度間接測量，未採用眼動儀或皮膚電位等生理指標。

### 未來研究方向
1. 探討生成式 AI 對用戶「發問行為」的影響。
2. 運用隨機對照實驗（RCT）或生理實驗（Eye-tracking）精準捕捉認知負擔與學習歷程。
3. 深入檢驗「純複製貼上」與「人機共創改寫」兩類用戶在社群價值與內容品質上的長期差異。
