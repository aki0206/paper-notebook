---
id: "zhang2027"
title: "How digital mediation shapes patronage of hidden consumption spaces"
zhTitle: "數位中介如何塑造實體隱蔽消費空間的光顧行為"
citation: "Zhang et al. (2027)"
authors: ["Zhang", "Hou", "Wang", "Liu"]
year: 2027
venue: "Journal of Retailing and Consumer Services"
doi: "10.1016/j.jretconser.2026.105069"
theme: "consumer"
status: "已精讀"
tags: ["HiddenConsumptionSpaces", "DigitalMediation", "ConsumerPatronage", "SpatialFriction", "MachineLearning"]
related: ["aggarwal2024", "chen2025", "kumarpalkhouski2025", "arshad2026", "zhuhussain2026", "hu2026", "changpark2026", "martinez2026"]
summary: "傳統零售理論假設消費者偏好臨街可見、易達的店面，但本研究發現：隨著大眾點評、社交媒體、地圖導航等**數位中介**普及，越來越多位於非臨街、高樓層或地下室的「**隱蔽消費空間（Hidden Consumption Spaces, HCS）**」靠數位平台的事前篩選與驗證打破了地點劣勢，吸引穩定客流——但實體隱蔽度仍形成一條清晰的「**隱蔽度梯度**」，數位中介只是局部補償，而不是徹底抹平空間距離。"
---

## 研究問題

> [!success] 重點
> 本研究旨在探討數位中介（Digital Mediation）與空間隱蔽度（Spatial Concealment）如何交織影響消費者對實體隱蔽消費空間（HCS）的光顧與選擇行為。

### 核心研究預期（Analytical Expectations）

1. **Expectation 1（隱蔽度梯度）**：HCS 光顧遵循「隱蔽度梯度（Hiddenness gradient）」，可達性較高的 HCS 類型造訪率較廣，而隱蔽度較高的類型則呈現更具選擇性的參與。
2. **Expectation 2（數位中介依賴）**：隨著 HCS 隱蔽度增加，消費者對第三方評價平台、社交媒體、預約行為及寫評分等數位中介實踐的依賴程度顯著提升。
3. **Expectation 3（空間限制的殘餘）**：數位中介並未消除隱蔽地點的劣勢；造訪高度隱蔽的 HCS 仍取決於價值-風險的權衡（包含環境品質、導航可達性、服務可靠性及對可達性降低的容忍度）。

## 研究方法

### 研究設計
探索性混合研究設計（Exploratory Mixed-methods Design），結合描述性統計、隱蔽度分組卡方/非母數檢定、類型特定隨機森林（Random Forest）預測模型與 SHAP 值分析，以及開放式文本的 AI 輔助混合質性分析。

### 樣本來源與樣本數
- 透過騰訊問卷（Tencent Questionnaire）於 2025 年 3 月進行線上發放，回收 532 份有效問卷，其中 495 人（93.0%）曾造訪過至少一種 HCS [20, 23, Table 2]。
- 受試者特徵：男女比例均衡（男 46.2%、女 52.4%），高度集中於青年族群（26–30 歲佔 42.3%，18–25 歲佔 20.9%），且普遍具備大專/專科以上學歷（76.7%）[23, Table 2]。

### 測量工具
17 個主問題構造之問卷，包含單選、複選、排序與情境問答（包含門市重置移至臨街一樓時可接受的價格增幅 M15）。

### 機器學習模型與訓練細節
- **模型演算法**：`scikit-learn` 之 Random Forest（`n_estimators = 300`, `max_depth = 12`, `random_state = 42`）。
- **驗證機制**：分層 5 折交叉驗證（Stratified 5-fold Cross-validation）。
- **可解釋性分析**：採用 SHAP（Shapley Additive Explanations）計算特徵重要度（Mean absolute SHAP value）與摘要圖（Summary plots）。
- **比較基準模型**：Logistic Regression 與 XGBoost（相關結果收錄於 SM）。

### 質性分析細節
收集 144 份有效開放式文本，利用 DeepSeek-V3 進行初階段語意編碼，再經人工校驗歸納為 6 大主題類別 [30, 48, Table 8]。

## 主要發現

> [!success] 重點
> HCS 參與已深植於日常都市消費（93.0% 曾造訪），但呈現明確的隱蔽度梯度；隨隱蔽度提升，消費者對評價平台（64.5%）、社交媒體（55.3%）與事前預約（56.9%）的依賴劇增；隨機森林模型證實，最高隱蔽度（Type C）的光顧行為具備最強的特徵預測力（ROC-AUC = 0.772）[23, 31, 35, 36, Table 4, Table 7]。

### HCS 造訪的普及性與隱蔽度梯度（Gradient）
- 63.2%（n = 336）曾造訪 Type A（一樓非臨街），55.8%（n = 297）曾造訪 Type B（非一樓臨街），37.0%（n = 197）曾造訪 Type C（非一樓非臨街），僅 7.0%（n = 37）從未造訪過 HCS [31, Fig 1a]。
- 單一類型造訪以 Type A（26.3%）與 Type B（20.4%）為主，獨自造訪 Type C 僅占 7.7%；22.0%（n = 109）受試者全數造訪過三種類型，顯示最隱蔽的空間具備更高門檻與選擇性 [32, Fig 1b]。

### 數位中介管道與實踐的階梯式遞增（Gradient in Digital Mediation）
- **第三方評價平台 (M9-C)** 依賴率：`None`（13.5%）→ `A-only`（41.5%）→ `Max = B`（60.1%）→ `Any C`（**64.5%**，$\chi^2 = 43.76, p < 0.001, q < 0.001$）[Table 4]。
- **社交媒體 (M9-E)** 依賴率：在 `Any C` 組急劇攀升至 **55.3%**（`Max = B` 僅 26.8%，$\chi^2 = 48.34, p < 0.001$）[Table 4]。
- **演算法/網紅推薦 (M10-F)**：`None`（2.7%）→ `A-only`（10.0%）→ `Max = B`（18.5%）→ `Any C`（**29.4%**，$p < 0.001$）[Table 4]。
- **事前預約行為 (M13-A)**：在 `Any C` 組顯著上升至 **56.9%**（其餘三組皆在 28.6%–35.1% 之間，$\chi^2 = 36.62, p < 0.001$）[36, Table 4]。
- **發表線上評價 (M13-C)**：`None`（21.6%）→ `A-only`（31.5%）→ `Max = B`（**49.4%**）→ `Any C`（**46.7%**，$p < 0.001$）[Table 4]。

### 消費金額與價格-可達性權衡（Expenditure & Relocation Trade-offs）
- 平均消費金額 (M14) 在 `Any C` 組最高（$p = 0.019$），顯示造訪極隱蔽空間者願意支付略高的單次消費 [37, Table 5]。
- 然而在遷至臨街一樓情境（M15-A, M15-B）中，`Any C` 組表現出**最低的可接受價格增幅**（$p < 0.001$），顯示熟客雖享受隱蔽空間，但拒絕為「移至臨街一樓」支付額外的位置溢價 [37, Table 5]。

### 預測模型與 SHAP 特徵解析
- 隨機森林模型預測能力：**Type C** 判別力最強（**Accuracy = 0.729, ROC-AUC = 0.772**），Type B 居次（Accuracy = 0.641, ROC-AUC = 0.691），Type A 最弱（ROC-AUC = 0.627，僅略高於基準）[41, Table 7]。
- **Type C 特徵結構**：SHAP 分析顯示，Top 特徵包含活動偏好（M6-A, M6-E）、社交媒體（M9-E）、預約（M13-A）以及多個「**屬性×數位中介**」交互作用項（如 M10-B×M9-E 性價比×社交媒體、M10-E×M9-C 線上評分×評價平台），證實極隱蔽空間的採行取決於數位管道與門市屬性的複合結合 [42, Fig 2c, 2f]。

### 質性核心障礙與建議分類
- 144 份開放式文本中，正面認可占 29 份（強調獨特體驗與探索感），負面疑慮占 18 份（難達性、詐欺疑慮、安全隱患）[49, Table 8]。
- 最大建議類別為**營運管理建議**（49 份，強調衛生、安全、服務品質與價格透明度）與**克服「隱蔽性」建議**（24 份，主張改善指標標誌、地圖導航整合與精準線上行銷）[50, Table 8]。

## 限制與未來方向

### 作者承認的研究限制
1. **自我報告數據的偏差**：依賴問卷自評，可能存在回憶偏差（Recall bias）；未來可結合 App 使用 Log、移動軌跡或交易次級資料。
2. **樣本偏向青年數位活躍族群**：受試者集中於青年與高學歷都市消費者（42.3% 為 26–30 歲），在推論至全體大眾時需謹慎。
3. **模型為橫斷面關聯而非因果關係**：隨機森林與統計檢定僅揭示結構化關聯，無法證明確切因果關係。

### 未來研究方向
1. 結合實驗法（Experimental designs）或縱向追蹤（Longitudinal designs），檢驗平台資訊調整、價格變化或環境改善對 HCS 造訪的因果影響。
2. 進行跨城市與跨平台生態系的比較研究，檢驗不同都市空間型態與平台生態中的通用性。
