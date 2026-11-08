---
id: "aggarwal2024"
title: "GEO: Generative Engine Optimization"
zhTitle: "GEO：生成引擎最佳化"
citation: "Aggarwal et al. (2024)"
authors: ["Aggarwal", "Murahari", "Rajpurohit", "Kalyan", "Narasimhan", "Deshpande"]
year: 2024
venue: "Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining"
doi: "10.1145/3637528.3671900"
theme: "engine"
status: "已精讀"
tags: ["GEO", "GenerativeEngineOptimization", "GEObench", "InformationDiscovery"]
related: ["chen2025", "zhuhussain2026", "hu2026"]
summary: "這是 **GEO（生成引擎最佳化）這個研究領域的創始論文**。作者建立了黑箱優化框架與 **GEO-bench** 評測基準，發現「加統計數據、引述名言、引用來源」能讓網頁在 AI 生成回答中的曝光率提升最高 41%，而傳統 SEO 的關鍵字堆疊完全沒用；GEO 還能讓原本排名低的網站大幅翻身。"
---

## 研究問題

> [!success] 重點
> 提出全球首個「**生成引擎最佳化（Generative Engine Optimization, GEO）**」黑箱優化框架，以及「**GEO-bench**」評測基準，協助內容創作者在不了解 GE 內部演算法的前提下，提升內容在 GE 生成回答中的曝光率（Visibility / Impression）。

### 核心研究問題

1. 網頁內容創作者如何透過調整文本風格與內容展現方式，提升網頁在黑箱 Generative Engine 答覆中的曝光率？
2. 哪些 GEO 優化策略（如加入統計數據、引用來源、權威語氣、流暢度優化等）最能有效提升曝光率？這些策略在不同主題領域（Domains）間是否有差異？
3. 傳統 SEO 策略（如關鍵字堆疊 Keyword Stuffing）在 GE 情境下是否依然有效？

## 研究方法

### 研究設計
模擬 GE 系統的實驗室控制實驗（Lab Benchmark Experiment），加上真實上線系統（In-the-wild Perplexity.ai）驗證。

### 樣本與資料

**GEO-bench 基準測試**
- 共 **10,000 個查詢**（8,000 訓練集、1,000 驗證集、1,000 測試集）
- 採集自 **9 個開源資料集**：MS MARCO、ORCAS-1、Natural Questions、AllSouls、LIMA、Davinci-Debate、Perplexity.ai Discover、ELI5，以及 GPT-4 生成查詢
- 每個查詢搭配 **Google 搜尋前 5 名網頁**（Top 5 Search Results）的清洗文本內容

**真實系統測試**
- 在 Perplexity.ai 上抽樣 **200 個測試集範例**進行上傳與評測

（出處：Section 3.1、3.2）

### 測量工具
- **GE 模擬器**：檢索前 5 名網頁，用 `gpt-3.5-turbo`（temperature=0.7）生成回答，每組實驗採樣 5 次以降低統計偏差。
- **主觀指標測量**：G-Eval 評測法，用 GPT-3.5 搭配表單模板評分，並校準把均值與方差標準化到與 Position-Adjusted Word Count 相同的量尺。

（出處：Section 2.2.1）

### 分析方法
**相對改善率（Relative Improvement %）**：

$$Improvement_{s_i} = \frac{Imp_{s_i}(r') - Imp_{s_i}(r)}{Imp_{s_i}(r)} \times 100\%$$

搭配 **5 個隨機種子**（Random Seeds）重複實驗，取平均與標準差。（出處：Section 3.5, Eq. 4）

## 主要發現

> [!success] 重點
> 加入權威引文、統計數據與引用來源，能讓網頁在 AI 答覆中的曝光率**提升最高 41%**；傳統 SEO 的「關鍵字堆疊」**完全無效**；GEO 對傳統排名較低的網站有強烈的「民主化」翻轉效應。

### 內容增強策略顯著提升曝光率

| 策略 | Position-Adjusted Word Count | Subjective Impression |
| :--- | :--- | :--- |
| **Quotation Addition**（引述名言） | +41.4%（27.2 vs. 基準 19.3） | +28.0%（24.7 vs. 19.3） |
| **Statistics Addition**（統計數據） | +30.6%（25.2） | +22.8%（23.7） |
| **Cite Sources**（引用來源） | +27.5%（24.6） | +13.5%（21.9） |

（出處：Table 1）

### 傳統 SEO 的「關鍵字堆疊」完全失效
- **Keyword Stuffing** 在 Position-Adjusted Word Count 上表現**比未優化基準更差**：17.7 vs. 19.3，相對下降 **−8.3%**。
- ⇒ 傳統 SEO 技巧無法直接轉移到 GE。
（出處：Table 1）

### 文字風格優化也有顯著效益
- **Fluency Optimization**（流暢優化）：+28.0%（分數 24.7）
- **Easy-to-Understand**（白話易懂）：+14.0%（分數 22.0）
- ⇒ GE 也重視資訊的呈現風格，不只是內容本身。
（出處：Table 1）

### GEO 具備強烈的「民主化效應」，造福低排名網站
- 當所有網站同時應用 GEO 時，傳統排名**第五名（Rank-5）**的低排名網站獲益最大：
  - Cite Sources 策略讓曝光率爆發性成長 **+115.1%**
  - Quotation Addition：**+99.7%**
  - Statistics Addition：**+97.9%**
- 相反地，傳統排名**第一名（Rank-1）**的網站曝光率平均下降 **20.6%–30.3%**。
- ⇒ GE 削弱了大企業靠反向連結（Backlinks）累積的獨佔優勢，拉平了小創作者的起跑線。
（出處：Table 2）

### 策略組合有加乘效果
- **Fluency Optimization + Statistics Addition** 組合表現最佳，曝光率相對改善達 **35.8%**，超越任何單一策略。
- Cite Sources 與其他策略組合時，效益大增（平均改善 **31.4%**）。
（出處：Figure 4）

### 真實系統 Perplexity.ai 驗證泛化性
- Statistics Addition 在 Subjective Impression 提升 **37.2%**（33.9 vs. 24.7）
- Quotation Addition 在 Position-Adjusted Word Count 提升 **20.7%**（29.1 vs. 24.1）
- Keyword Stuffing 表現比基準差 **−9.1%**
（出處：Table 5、Table 7）

## 限制與未來方向

### 作者承認的限制
1. **系統演化動態性**：GE 演算法會隨時間更新，GEO 策略需要動態調整。
2. **黑箱 SERP 排名影響未知**：因搜尋引擎演算法是黑箱，論文沒有評測 GEO 文本修改是否會反過來影響傳統 Google SERP 排名。
3. **標籤與查詢時效性**：GEO-bench 的標籤由 GPT-4 自動標註，可能有主觀雜訊，查詢熱點也會隨時間變化。

### 未來研究方向
1. 當 LLM 上下文長度（Context Window）變長、成本降低時，GE 能採納更多來源，GEO 策略需要持續更新。
2. 探討多輪對話（Multi-turn Conversational GEs）情境下的 GEO 策略。

（出處：Section 6，Appendix A）
