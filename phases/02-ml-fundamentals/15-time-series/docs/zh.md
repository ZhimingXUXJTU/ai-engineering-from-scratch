# 时间序列基础

> 过去的表现确实能预测未来——前提是你先检查了平稳性。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 1-9 课
**时长：** 约 90 分钟

## 学习目标

- 将时间序列分解为趋势、季节性和残差分量，并检验平稳性
- 实现滞后特征和滚动统计将时间序列转换为监督学习问题
- 构建前向滚动验证框架，防止未来数据泄漏到训练中
- 解释为什么随机训练/测试分割对时间序列无效，并用正确的时间分割展示性能差距

## 问题引入

你有时序排列的数据。每日销售量、每小时温度、每分钟 CPU 使用率、每周股价。你想预测下一个值、下周、下季度。

你使用标准 ML 工具箱：随机训练/测试分割、交叉验证、特征矩阵输入、预测输出。每一步都是错的。

时间序列打破了标准 ML 依赖的假设。样本不独立——今天的温度依赖昨天的。随机分割将未来信息泄漏到过去。在回测中看起来很棒的特征在生产中失败，因为它们依赖随时间变化的模式。

用随机交叉验证得到 95% 准确率的模型，用正确的时间评估可能只有 55%。这不是技术细节，这是"纸面上好用"和"生产中好用"的区别。

## 核心概念

### 时间序列有什么不同

标准 ML 假设 i.i.d.——独立同分布。时间序列违反两者：

- **不独立。** 今天的股价依赖昨天的。
- **不同分布。** 分布随时间变化。12 月的销量与 3 月的不同。

### 时间序列分解

任何时间序列可以分解为：

- **趋势 (Trend)：** 长期方向（上升、下降、平坦）
- **季节性 (Seasonality)：** 周期性重复模式（每日、每周、每年）
- **残差 (Residual)：** 去除趋势和季节性后剩余的随机噪声

```
y(t) = Trend(t) + Seasonality(t) + Residual(t)    （加法分解）
y(t) = Trend(t) * Seasonality(t) * Residual(t)    （乘法分解）
```

### 平稳性

平稳序列的统计特性（均值、方差、自相关）不随时间变化。大多数时间序列模型要求数据是平稳的。

检验平稳性：
- **ADF 检验 (Augmented Dickey-Fuller)：** p 值 < 0.05 拒绝非平稳的原假设
- **KPSS 检验：** p 值 > 0.05 表示平稳

使序列平稳：
- 差分：y'(t) = y(t) - y(t-1)
- 对数变换（处理增长的方差）
- 去趋势（减去趋势分量）

### 将时间序列转为监督学习

标准 ML 模型不能直接处理序列。需要构造特征：

- **滞后特征 (Lag Features)：** 过去的值作为特征。y(t-1), y(t-2), ..., y(t-k)
- **滚动统计 (Rolling Statistics)：** 过去 k 个值的均值、标准差、最小值、最大值
- **时间特征：** 星期几、月份、是否假日、季度

### 前向滚动验证 (Walk-Forward Validation)

对于时间序列，标准交叉验证无效。你必须按时间顺序分割：

```
Fold 1: Train [1..100]     Test [101..150]
Fold 2: Train [1..150]     Test [151..200]
Fold 3: Train [1..200]     Test [201..250]
```

每次，训练集扩展到包含更多历史。测试集始终在训练集之后。这模拟了真实世界：你只有过去的数据来预测未来。

### 常见时间序列模型

| 方法 | 类型 | 适合 |
|------|------|------|
| 移动平均 (Moving Average) | 统计 | 短期预测、平滑 |
| 指数平滑 (Exponential Smoothing) | 统计 | 带趋势和季节性的数据 |
| ARIMA | 统计 | 平稳或差分后平稳的数据 |
| Prophet | 加法模型 | 带强季节性和假日效应的商业数据 |
| LSTM | 深度学习 | 长依赖的复杂序列 |
| Transformer | 深度学习 | 多变量长序列 |

## 动手实现

`code/time_series.py` 中的代码从零实现了时间序列分解、平稳性检验、滞后特征构建和前向滚动验证。

详见 `code/time_series.py`。

## 用框架实现

```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import GradientBoostingRegressor

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    model = GradientBoostingRegressor()
    model.fit(X[train_idx], y[train_idx])
    score = model.score(X[test_idx], y[test_idx])
```

对于经典统计方法：
```python
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(y_train, order=(1, 1, 1))
fitted = model.fit()
forecast = fitted.forecast(steps=10)
```

## 产出物

本课产出 `code/time_series.py` -- 完整的时间序列分析工具。

## 练习题

1. 生成一个带趋势和季节性的合成时间序列。用移动平均和差分去除趋势。ADF 检验确认平稳性。

2. 构建滞后特征（lag 1-7）和滚动统计（窗口 3、7、14）。用梯度提升树预测。比较不同特征组合的准确率。

3. 在同一数据集上比较随机交叉验证和前向滚动验证。展示随机分割导致过度乐观的估计。

4. 实现 ARIMA(p, d, q) 从零。网格搜索最优参数，用 AIC 选择最佳模型。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 平稳性 (Stationarity) | 统计特性（均值、方差）不随时间变化 |
| 趋势 (Trend) | 数据的长期上升或下降方向 |
| 季节性 (Seasonality) | 以固定间隔重复的周期性模式 |
| 滞后特征 (Lag Feature) | 将过去时间步的值作为当前预测的特征 |
| 滚动统计 (Rolling Statistics) | 过去 k 个值的统计量（均值、标准差等） |
| 前向滚动验证 (Walk-Forward) | 按时间顺序分割数据，训练集始终在测试集之前 |
| ADF 检验 | 检验时间序列是否平稳的统计检验 |
| 差分 (Differencing) | y(t) - y(t-1)，使非平稳序列变平稳的变换 |

## 延伸阅读

- [Hyndman & Athanasopoulos: Forecasting: Principles and Practice](https://otexts.com/fpp3/) - 免费在线教材
- [statsmodels 时间序列文档](https://www.statsmodels.org/stable/tsa.html) - Python 时间序列分析库
- [sklearn TimeSeriesSplit](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-cross-validation)
