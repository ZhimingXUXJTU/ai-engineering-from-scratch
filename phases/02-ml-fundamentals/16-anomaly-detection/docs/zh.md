# 异常检测

> 正常容易定义。不正常的就是不拟合的。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 1-9 课
**时长：** 约 75 分钟

## 学习目标

- 从零实现 Z-score、IQR 和 Isolation Forest 异常检测方法
- 区分点异常、上下文异常和集合异常，为每种选择合适的检测方法
- 解释为什么异常检测被框架为建模正常数据而非分类异常
- 比较无监督异常检测与监督分类，评估新异常覆盖率和精确率之间的权衡

## 问题引入

一张信用卡下午 2 点在纽约使用，2:05 在东京使用。一个工厂传感器读数 150 度，正常范围是 80-120。一个服务器每秒发送 50,000 个请求，日均 200。

这些都是异常。找到它们很重要。欺诈造成数十亿损失。设备故障造成停机。网络入侵造成数据泄露。

挑战：你很少有异常的标注样本。欺诈占交易的 0.1%。设备故障每年发生几次。你不能训练标准分类器，因为"异常"类中几乎没有东西可学。即使有一些标签，你见过的异常也不是你将遇到的全部类型。明天的欺诈方案看起来和今天不同。

异常检测翻转了问题。不学什么是异常的，学什么是正常的。任何偏离正常的都是可疑的。这无需标签，适应新类型异常，可扩展到海量数据集。

## 核心概念

### 异常类型

- **点异常 (Point Anomalies)。** 无论上下文都不寻常的单个数据点。温度读数 500 度。
- **上下文异常 (Contextual Anomalies)。** 在给定上下文中不寻常的数据点。90 度在夏天正常，在冬天异常。
- **集合异常 (Collective Anomalies)。** 作为一组不寻常的数据序列，但每个单独点可能正常。50 次连续登录失败是暴力攻击。

大多数方法检测点异常。上下文异常需要时间或位置特征。集合异常需要序列感知方法。

### Z-score 方法

假设数据服从正态分布，标记偏离均值超过 k 个标准差的点：

```
z = (x - mean) / std
异常如果 |z| > threshold（通常 3）
```

快速、简单，但假设正态分布且对离群值敏感（离群值拉动均值和标准差）。

### IQR 方法

使用四分位距，对分布假设更鲁棒：

```
Q1 = 第 25 百分位
Q3 = 第 75 百分位
IQR = Q3 - Q1
异常如果 x < Q1 - 1.5*IQR 或 x > Q3 + 1.5*IQR
```

不假设正态分布，对离群值更鲁棒。

### Isolation Forest

随机森林的变体，专门为异常检测设计。核心思想：异常点更容易被隔离。

算法：
1. 随机选择一个特征
2. 随机选择该特征的最大值和最小值之间的一个分割值
3. 分割数据
4. 递归重复直到每个点被隔离

异常点（远离正常聚类的点）平均需要更少的分裂次数来隔离。正常点被其他正常点包围，需要更多分裂。

路径长度短的点 = 异常。

### 其他方法

| 方法 | 类型 | 适合 |
|------|------|------|
| One-Class SVM | 边界学习 | 高维数据、正常数据边界 |
| LOF (Local Outlier Factor) | 密度 | 局部密度变化大的数据 |
| DBSCAN | 聚类 | 任意形状的数据 |
| Autoencoder | 重构误差 | 复杂非线性模式 |

### 评估异常检测

没有标签时，评估困难。有标签时：

- **精确率 (Precision)：** 标记的异常中有多少是真正的异常
- **召回率 (Recall)：** 真正的异常中有多少被找到
- **F1 分数：** 平衡精确率和召回率
- **假正例率：** 正常点被错误标记为异常的比例（必须保持很低）

异常检测的精确率-召回率权衡：降低阈值找到更多异常（高召回率）但标记更多正常点为异常（低精确率）。

## 动手实现

### 步骤 1：Z-score 异常检测

```python
def zscore_detect(data, threshold=3.0):
    mean = sum(data) / len(data)
    var = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(var) if var > 0 else 1e-10
    anomalies = []
    for i, x in enumerate(data):
        z = abs(x - mean) / std
        if z > threshold:
            anomalies.append(i)
    return anomalies
```

### 步骤 2：IQR 异常检测

```python
def iqr_detect(data, factor=1.5):
    sorted_data = sorted(data)
    n = len(sorted_data)
    q1 = sorted_data[n // 4]
    q3 = sorted_data[3 * n // 4]
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return [i for i, x in enumerate(data) if x < lower or x > upper]
```

### 步骤 3：Isolation Forest（简化版）

```python
class IsolationTree:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth

    def fit(self, X):
        self.tree = self._build(X, depth=0)

    def _build(self, X, depth):
        if depth >= self.max_depth or len(X) <= 1:
            return {"type": "leaf", "size": len(X)}
        feature = random.randint(0, len(X[0]) - 1)
        values = [x[feature] for x in X]
        threshold = random.uniform(min(values), max(values))
        left = [x for x in X if x[feature] < threshold]
        right = [x for x in X if x[feature] >= threshold]
        return {
            "type": "split",
            "feature": feature,
            "threshold": threshold,
            "left": self._build(left, depth + 1),
            "right": self._build(right, depth + 1),
        }

    def path_length(self, x):
        return self._path(x, self.tree, 0)

    def _path(self, x, node, depth):
        if node["type"] == "leaf":
            return depth
        if x[node["feature"]] < node["threshold"]:
            return self._path(x, node["left"], depth + 1)
        else:
            return self._path(x, node["right"], depth + 1)
```

完整实现见 `code/anomaly_detection.py`。

## 用框架实现

```python
from sklearn.ensemble import IsolationForest

clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit(X_train)
predictions = clf.predict(X_test)  # -1 = 异常, 1 = 正常
```

## 产出物

本课产出 `code/anomaly_detection.py`。

## 练习题

1. 在正态数据中注入不同比例的异常（1%、5%、10%）。比较 Z-score、IQR 和 Isolation Forest 的精确率和召回率。

2. 生成一个上下文异常数据集（正常值在冬季和夏季不同）。展示简单的 Z-score 在冬天把夏天的正常值标为异常。添加上下文特征后重新检测。

3. 构建 Isolation Forest 的集成：训练 10 棵 Isolation Tree，取平均路径长度。比较单棵树与集成的稳定性。

4. 用 Autoencoder 思路实现异常检测：训练一个简单的重构模型，标记重构误差高的点为异常。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 异常 (Anomaly) | 偏离正常模式的数据点或模式 |
| Z-score | 数据点偏离均值多少个标准差 |
| IQR | 四分位距，Q3-Q1，衡量数据的中间 50% 展布 |
| Isolation Forest | 通过随机分裂隔离点来检测异常，异常点需要更少分裂 |
| 点异常 | 无论上下文都不正常的单个点 |
| 上下文异常 | 在特定上下文中不正常的点 |
| 集合异常 | 单独看正常但作为序列不正常的一组点 |
| 污染率 (Contamination) | 数据中预期的异常比例 |

## 延伸阅读

- [Liu et al.: Isolation Forest (2008)](https://ieeexplore.ieee.org/document/4781136) - Isolation Forest 原始论文
- [Chandola et al.: Anomaly Detection: A Survey (2009)](https://dl.acm.org/doi/10.1145/1541880.1541882) - 异常检测综述
- [scikit-learn 异常检测](https://scikit-learn.org/stable/modules/outlier_detection.html)
