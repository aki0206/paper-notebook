---
id: "arshad2026"
title: "Cited or Invisible? A Multilingual, Multi-Platform Audit of Brand Citation in Generative Search"
zhTitle: "被引用還是隱形？生成式搜尋中品牌引用的跨語言、跨平台審計"
citation: "Arshad (2026)"
authors: ["Arshad"]
year: 2026
venue: "Zenodo 預印本"
doi: "10.5281/zenodo.22491737"
theme: "engine"
status: "已精讀"
tags: ["GenerativeSearch", "BrandCitation", "MultiPlatformAudit", "MultilingualAudit", "GEO"]
related: ["aggarwal2024", "chen2025", "zhuhussain2026", "hu2026"]
summary: "這是一篇**跨平台、跨語言的外部審計**研究，測試品牌在四大 AI 搜尋平台（Perplexity、Gemini、ChatGPT、Google AI Overviews）中的引用率。結論很直接：**決定品牌能不能被引用的是「平台」，不是「語言」**——平台間差距最高達 10 倍，語言間差距幾乎不顯著。而且就算消費者明確搜尋「正品」，AI 搜尋還是常常推薦二手平台或複刻商家，原廠反而被「隱形」。"
---

## 研究問題

> [!success] 重點
> 透過跨平台、跨語言的雙重審計實驗，量化四大生成式搜尋平台在六種歐語市場中的品牌引用分布，驗證「平台差異」與「語言差異」哪個才是主導因素，並檢驗真品檢索需求在 AI 搜尋中的真實流向。

### 核心研究問題

1. 品牌的引用率（Brand Citation Rate），主要是被「平台類型」驅動，還是被「語言」驅動？
2. 小樣本的 Prompt 採樣，會在多大程度上人為製造出虛假的語言差距？
3. 同一個 Prompt 重複執行時，不同平台的回答不穩定性（Instability）表現如何？
4. 當消費者明確搜尋「正品／授權經銷」時，生成式搜尋引擎能不能把需求正確導向原廠版權持有者？

## 研究方法

### 研究設計
**雙研究外部審計實驗**（External Audit with Two Disjoint Studies & Replicates）。（Section 3.1，p. 3）

### 樣本與資料

**Study 1**
- 6 個市場 × 5 個商業垂直領域 × 12 個原生 Prompt = **360 個 Prompt**
- 每個在 4 個平台重複執行 3 次 → 共 **4,320 個觀察值**
- 焦點品牌：4 家複刻家具零售商（R1–R4，其中 **R1 由作者本人營運**）

**Study 2**
- 6 個市場 × 15 個真品尋求 Prompt = **90 個 Prompt**
- 每個在 4 個平台重複執行 3 次 → 共 **1,080 個觀察值**
- 焦點品牌：8 家正版家具設計版權持有者（Vitra、Herman Miller 等）

**Prompt 撰寫原則**：由各語言母語者**原生撰寫**（Native Authoring），絕不使用機器翻譯（例如德語搜尋複刻用 *Nachbau*、荷語用 *namaak*——翻譯無法反映真實購物搜尋行為）。

（出處：Abstract、Section 3.1、3.2、3.6，p. 1、3–4）

### 測量工具與數據處理
- **API 呼叫**：Google AI Overviews（透過 SERP API，設定地理與語言定位）、Gemini（with search grounding）、Perplexity Sonar、ChatGPT Responses API（with web search）
- **引用提取與技術陷阱修正**：只採計結構化引用列表中的網域；修正了 Gemini 把 `uri` 指向 Google 重導向主機、導致引用率歸零的技術陷阱（需改從 `chunk title` 讀取網域）
- 出處：Section 3.3、3.4，p. 3

### 分析方法
- **Cluster Bootstrap**：以 Prompt 為群集重抽樣，建立 95% 信賴區間（CI）
- **重抽樣實驗（Resampling Experiment）**：進行 5,000 次單次抽樣重抽樣，量化 Prompt 選擇偏差
- **總 API 數據收集成本**：**$57.65 美元**（Study 1：$46.14；Study 2：$11.50）
- 出處：Abstract、Section 3.5、3.7，p. 1、4

## 主要發現

> [!success] 重點
> **平台差異決定 AI 能見度**（引用率跨平台相差最高 10 倍），**語言之間的差異極小且不顯著**。當消費者明確搜尋正品時，AI 搜尋優先推薦二手平台與複刻商家，原廠版權商普遍被「隱形」。

### 平台效應主導語言效應（Platform Dominates Language）

**引用率排序（兩個獨立研究完全複製）**

| 研究 | 排序（高到低） | 最大差距 |
| :--- | :--- | :--- |
| **Study 1**（複刻零售商） | Perplexity 91.2% [84.3–97.2] > Gemini 63.9% [55.1–72.7] > ChatGPT 36.1% [25.5–46.8] > Google AI Overviews 16.2% [9.3–24.1] | **5.6 倍** |
| **Study 2**（正版版權商） | Perplexity 63.3% [53.3–73.0] ≈ Gemini 54.4% [45.6–63.3] > ChatGPT 30.4% [21.9–38.9] > Google AI Overviews 6.3% [3.0–10.0] | **10.0 倍** |

**相較之下，語言間差距極小、信賴區間幾乎完全重疊**
- Study 1 跨語言引用率：41.0%（法語）～ 61.1%（西班牙語）
- Study 2 跨語言引用率：31.1%（義大利語）～ 46.1%（英語）
- 沒有任何語言對在統計上能明確分離。

（出處：Abstract、Section 4.1、Table 1、Table 2，p. 1、4）

### Prompt 選擇偏差會製造「虛假的語言差距」
- 重抽樣實驗顯示：在**單次、小樣本（8 個 Prompt）**的測試條件下，即使整體資料庫中 ChatGPT 的英德語言差距是 0.0，仍有 **12.5%** 的機率測出 ≥ 20 個百分點的虛假語言差距。
- 在 Google AI Overviews 下（$k=8$），有 **16.4%** 的機率出現 ≥ 20 個百分點的虛假差距（實測最大差距達 **50 個百分點**）。
- 作者在前導實驗中，曾因 Prompt 數目過少而測出 **38 個百分點**的虛假英德差距。
- 出處：Abstract、Section 4.3、Table 3，p. 1、4

### 重複查詢有顯著不穩定性，但平台排序一致

| 平台 | Study 1 不穩定率 | Study 2 不穩定率 |
| :--- | :--- | :--- |
| **Gemini**（最不穩定） | 40.3% | 32.2% |
| Google AI Overviews | 15.3% | 13.3% |
| ChatGPT | 5.6% | 18.9% |
| **Perplexity**（最穩定） | 1.4% | 2.2% |

（出處：Abstract、Section 4.4，p. 1、4–5）

### 真品需求沒有被引導至原廠版權持有者
- Study 2（明確尋求正品的 1,080 個回答）中，前三大被引用網域：
  1. `vitra.com`（13.6%，**原廠**）
  2. `1stdibs.com`（12.5%，二手平台）
  3. `whoppah.com`（11.3%，二手平台）
- **複刻零售商 R1 排名第 4（9.7%）**，引用率超越了 8 家原廠中的 4 家（如 Cassina 4.8%、Herman Miller 4.4%、Flos 4.4%、Louis Poulsen 4.4%）。
- 在 Google AI Overviews 中，原廠版權持有者整體引用率只有 **6.3%**，德語市場的原廠引用率甚至是 **0%**。
- 出處：Abstract、Section 4.5、Table 4，p. 1、5

### AI 搜尋回答率不是 100%，引用網域也高度分散
- Google AI Overviews 在 Study 1 只有 **38%** 的查詢生成了 AI 摘要，Study 2 只有 **30%**。
- 引用網域極度分散：Study 1 的 28,371 次引用涉及 **5,755 個獨立網域**，前 10 大網域只佔總引用的 **7.7%**。
- 引用頻率最高的單一網域：`reddit.com`（10.7%）與 `youtube.com`（7.7%）。
- 出處：Section 4.2、4.6，p. 4–5

## 限制與未來方向

### 作者承認的限制
1. **API vs. 消費者介面差異**：用 API 做審計，API 管道跟真實消費者介面（含個人化、介面重排名等）會不一樣。
2. **語言涵蓋範圍有限**：只研究了 6 種資源豐富的西歐語言，無法推論到低資源語言（如烏爾都語、斯瓦希里語、越南語）。
3. **時間有效性**：資料是 2026 年 9 月的時間點快照，系統隨時在更新。
4. **作者利益衝突**：作者本身營運複刻零售商（R1）。作者透過獨立設計 Study 2（對照 8 家第三方正版商）並公開原始 Log，確保結果可被獨立驗證。

（出處：Section 3.3、3.6、5，p. 3–6）

### 未來研究方向
1. 擴展到低資源語言（Low-resource languages），檢驗訓練資料不對稱下的真實語言差距。
2. 深入解析造成平台間引用率巨大差異的內部檢索與重排名機制（Retrieval & Ranking Mechanisms）。

（出處：Section 6，p. 6）
