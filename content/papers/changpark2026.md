---
id: "changpark2026"
title: "Factors affecting changes in the customer journey with generative AI shopping agents: aspects of purchase decision-making."
zhTitle: "生成式 AI 購物代理人對顧客旅程與購買決策之影響"
citation: "Chang & Park (2026)"
authors: ["Chang", "Park"]
year: 2026
venue: "Journal of Marketing Management"
doi: "10.1080/0267257x.2026.2715539"
theme: "consumer"
status: "已精讀"
tags: ["GAISA", "CustomerJourney", "BehaviouralReasoningTheory", "TrustTransfer", "ContextualRelevance", "AlgorithmAversion", "消費者研究"]
related: ["aggarwal2024", "chen2025", "kumarpalkhouski2025", "arshad2026", "zhuhussain2026", "hu2026"]
summary: "這篇**直接測量消費者的心理反應**。用「行為推理理論」和「信任轉移理論」證明：消費者對生成式 AI 購物代理人（GAISA）的採行，走的是理性推理路徑而非直覺捷徑；「情境適切性」是最強的採行動機，「感知複雜性」是最大阻力；信任會沿著 **GAISA → 推薦商品 → 購買意願** 這條鏈一路傳遞下去。"
---

## 研究問題

> [!success] 重點
> 用「行為推理理論（BRT）」與「信任轉移理論（Trust Transfer Theory）」，探討 GAISA 如何改變消費者的採行意願、對推薦商品的購買意願以及顧客旅程，並檢驗「演算法反感（Algorithm Aversion）」與「產品類型（搜尋型 vs. 體驗型）」的邊界條件。

### 核心研究問題（Introduction, p. 3）

- **RQ1**：當 GAISA 即時理解消費者的消費情境並提供行銷提案時，如何影響採行意願（Adoption Intention）與購買意願（Purchase Intention）？背後的心理推理因子是什麼？顧客旅程如何改變？
- **RQ2**：GAISA 行銷提案的影響，是否取決於「演算法使用傾向（反感 vs. 非反感）」與「推薦目標產品類型（搜尋型 vs. 體驗型產品）」的交互作用？

## 研究方法

### 研究設計
**線上情境實驗法**（Online Scenario-based Experiment），用具備即時聯網搜尋能力的 **Microsoft Co-pilot** 作為 GAISA 的實驗代理工具（Proxy）。（Methodology, p. 14）

### 樣本
- **美國 18–64 歲居民**，透過 Amazon MTurk 招募，施測時間 **2024 年 9 月 13–15 日**
- 刪除不認真與未通過操弄檢定的問卷後，獲得 **457 份有效樣本**：
  - **Algorithm Non-aversion 組**：$n=230$（NS 組 230、NE 組 230）
  - **Algorithm Aversion 組**：$n=227$（AS 組 227、AE 組 227）
- 兩組在年齡、性別、職業分佈均勻（大專／大學以上學歷占 69%–74%）

（出處：p. 16；Table 2, p. 17）

### 實驗任務刺激物（Stimuli）

| 任務 | 情境 | 內容 |
| :--- | :--- | :--- |
| **Mission 1**（搜尋型產品） | 參加朋友 Potluck 派對 | 輸入 4 個 Prompt，要求 Co-pilot 推薦熱門菜餚、食譜、影片、評價，並生成 Instacart 購物清單 |
| **Mission 2**（體驗型產品） | 規劃 2 週度假 | 輸入 4 個 Prompt，要求 Co-pilot 推薦地點、機酒預訂、評價，並連結到 Kayak |

（出處：Table 1, p. 15）

### 分析方法
- 用 **AMOS 29.0** 進行**基於共變異數的結構方程模型（CB-SEM）**
- **多組比較分析（Multigroup SEM）**驗證邊界條件（檢驗跨組 Critical Ratio > 1.96）
- 用 **Phantom Variable** 與 **Bias-corrected Bootstrapping**（5,000 次抽樣，95% CI）做多重中介分析

（出處：p. 17、21、25）

## 主要發現

> [!success] 重點
> **理性的深層資訊處理路徑在所有組別中完全成立**；「情境適切性」是驅動採行的最核心優勢，「感知複雜性」是最大阻力；**信任轉移機制（TG → TR → PI）顯著成立**。

### 深層資訊處理路徑完全成立，啟發式路徑被拒絕

| 路徑 | 係數 $\beta$ | 顯著性 |
| :--- | :--- | :--- |
| H1a：CC → RA | −.35 ～ −.48 | $p < .001$（顯著負向） |
| H1b：CC → RF | .55 ～ .58 | $p < .001$（顯著正向） |
| H3a：RA → AT | −.18 ～ −.41 | $p < .05$（顯著負向） |
| H3b：RF → AT | .26 ～ .59 | $p < .01$（顯著正向） |
| H5：AT → AI | .23 ～ .55 | $p < .01$（顯著正向） |
| H2：CC → AT（啟發式路徑） | — | **所有組別均不顯著（被拒絕）** |

- ⇒ 證實消費者採行 GAISA，必須經過「理由推理」的過程，不是靠直覺捷徑。
- 出處：Table 7, p. 24

### 核心驅動與阻力因子
- **採行理由中**：**Contextual Relevance（情境適切性）** 因子載荷最高（$\lambda = .76$ ～ $.84$），超越傳統的省時省力。
- **反對理由中**：**Perceived Complexity（感知複雜性）** 因子載荷最高（$\lambda = .68$ ～ $.78$），其次是傳統障礙、感知干擾；**Privacy Concerns（隱私疑慮）** 的權重反而相對最低（$\lambda = .53$ ～ $.65$）。
- 出處：Table 7, p. 24；Discussion, p. 26

### 信任轉移鏈（Trust Transfer）完全驗證

| 路徑 | 係數／效果量 | 顯著性 |
| :--- | :--- | :--- |
| H6：RF → TG | $\beta = .49$ ～ $.55$ | $p < .001$ |
| H9：TG → TR | $\beta = .36$ ～ $.54$（NS 組 $f^2=.23$，AE 組 $f^2=.27$，中等效果量） | $p < .001$ |
| H10：TR → PI | $\beta = .27$ ～ $.56$ | $p < .001$ |
| H7：RF → TR（直接路徑） | — | **不顯著** |

- ⇒ H7 不顯著證實：採行理由必須**透過對 GAISA 的信任（TG）**，才能間接轉移到對商品的信任，不能跳過這一步。
- 出處：Table 7, p. 24；Mediation Analysis, p. 25、27

### 演算法反感者的逆轉發現（邊界條件）
- 對演算法反感者（Algorithm Aversion）而言，在評估**體驗型產品**（AE 組）時，**Usefulness of Advice（建議實用性）** 的權重顯著高於非反感者（Critical Ratio = 2.18 > 1.96）。
- 在 H10（TR → PI）路徑中，演算法反感者對**體驗型產品**的購買意願（$\beta = .49$）顯著**高於**搜尋型產品（$\beta = .27$，CR = 2.52 > 1.96）。
- ⇒ 情境對話獲得的實用建議，能克服演算法反感，讓反感者在資訊不足的體驗型產品上，反而更願意依賴 GAISA。
- 出處：Table 7, p. 24；Discussion, p. 28

## 限制與未來方向

### 作者承認的限制
1. **用 Co-pilot 當 Proxy**：由於商業化 GAISA 當時尚未完全普及，研究用 Microsoft Co-pilot 做情境模擬，跟真實嵌入電商 App 的動態體驗仍有微小落差。
2. **新奇效應（Novelty Effect）干擾**：生成式 AI 早期帶來的高期待，可能膨脹受試者的採行意願。
3. **樣本集中於美國與高教育群體**：MTurk 樣本 69%–74% 具學士學位以上，數位素養較高，可能低估一般大眾對複雜性的感受。

（出處：Limitations, p. 32–33）

### 未來研究方向
1. 等原生 GAISA（如 Amazon Rufus、品牌自主 Agent）全面上市後，做縱向追蹤研究，追蹤真實購物車轉換。
2. 擴展到非英語國家與低教育程度／低數位素養群體，檢驗跨文化與跨階層的通用性。

（出處：p. 32–33）
