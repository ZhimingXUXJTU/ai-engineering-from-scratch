# 处理不平衡数据

> 当 99% 的数据是"正常"时，准确率就是一个谎言。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 1-9 课（尤其是评估指标）
**时长：** 约 90 分钟

## 学习目标

- 从零实现 SMOTE，解释合成过采样与随机复制的区别
- 使用 F1、AUPRC 和马修斯相关系数 (MCC) 评估不平衡分类器，而非准确率
- 比较类权重、阈值调优和重采样策略，为给定不平衡比例选择正确方法
- 构建结合 SMOTE、类权重和阈值优化的完整不平衡数据管线

## 问题引入

你构建了一个欺诈检测模型。它有 99.9% 的准确率。你庆祝。然后你意识到它对每笔交易都预测"非欺诈"。

这不是 bug。当只有 0.1% 的交易是欺诈时，这是理性选择。模型学到始终猜多数类最小化总误差。它在技术上正确，但完全无用。

这种情况在所有真正重要的分类场景中都会发生。疾病诊断：1% 阳性率。网络入侵：0.01% 攻击。制造缺陷：0.5% 不良品。垃圾邮件过滤：20% 垃圾。流失预测：5% 流失者。少数类越重要，它往往越稀少。

准确率失败因为它平等对待所有正确预测。正确标记合法交易和正确抓住欺诈都算准确率的一点。但抓住欺诈是模型存在的全部理由。我们需要指标、技术和训练策略来强制模型关注稀少但重要的类别。

## 核心概念

### 为什么准确率失败

考虑 1000 个样本的数据集：990 个负例，10 个正例。始终预测负例的模型：

|  | 预测为正 | 预测为负 |
|--|---|---|
| 实际为正 | 0 (TP) | 10 (FN) |
| 实际为负 | 0 (FP) | 990 (TN) |

准确率 = (0 + 990) / 1000 = 99.0%

模型抓住了零欺诈、零疾病、零缺陷。但准确率说 99%。

### 正确的指标

- **F1 分数：** 精确率和召回率的调和平均。不平衡数据的默认选择。
- **AUPRC（精确率-召回率曲线下面积）：** 比 AUC-ROC 对不平衡数据更有信息量。
- **MCC（马修斯相关系数）：** 考虑混淆矩阵全部四个值，不受类别不平衡影响。
- **精确率@k：** 在 top-k 预测中真正正例的比例。实用且直观。

### 重采样策略

**过采样 (Oversampling)：** 增加少数类样本。
- 随机过采样：复制少数类样本。简单但可能导致过拟合。
- SMOTE：在少数类样本之间插值生成合成样本。

**欠采样 (Undersampling)：** 减少多数类样本。
- 随机欠采样：随机删除多数类样本。简单但可能丢失有用信息。
- Tomek Links：移除与少数类样本最近的多数类样本。

**SMOTE（合成少数类过采样技术）：**

```
对每个少数类样本 x_i:
  1. 找到 k 个最近邻（通常 k=5）
  2. 随机选一个邻居 x_z
  3. 生成新样本: x_new = x_i + lambda * (x_z - x_i)
     其中 lambda 是 [0,1] 的随机数
```

SMOTE 在特征空间的少数类区域中创建新样本，而非简单复制。这给模型更多少数类的视角，减轻过拟合。

### 代价敏感学习

不是重采样，而是让模型更关注少数类：

```python
from sklearn.linear_model import LogisticRegression

# class_weight='balanced' 自动按类别频率的倒数加权
model = LogisticRegression(class_weight='balanced')
```

或者手动设置权重：

```python
# 欺诈类权重是非欺诈的 100 倍
weights = {0: 1, 1: 100}
model = LogisticRegression(class_weight=weights)
```

### 阈值调优

默认阈值 0.5 对不平衡数据不是最优的。降低阈值可以捕获更多正例（高召回率）但增加假正例（低精确率）。最佳阈值取决于业务成本。

```
from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)
f1_scores = 2 * precisions * recalls / (precisions + recalls)
best_threshold = thresholds[np.argmax(f1_scores)]
```

### 组合策略

实践中，组合多种策略效果最好：

1. 先用 SMOTE 过采样
2. 用 class_weight 微调
3. 最后优化阈值

## 动手实现

### 步骤 1：从零实现 SMOTE

```python
import random
import math

def smote(minority_samples, k=5, n_synthetic=100, seed=42):
    random.seed(seed)
    n = len(minority_samples)
    d = len(minority_samples[0])

    synthetic = []
    for _ in range(n_synthetic):
        idx = random.randint(0, n - 1)
        sample = minority_samples[idx]

        # 找 k 个最近邻
        distances = []
        for j in range(n):
            if j == idx:
                continue
            dist = math.sqrt(sum((sample[f] - minority_samples[j][f]) ** 2 for f in range(d)))
            distances.append((dist, j))
        distances.sort()
        neighbors = [j for _, j in distances[:k]]

        # 随机选一个邻居并插值
        neighbor_idx = random.choice(neighbors)
        neighbor = minority_samples[neighbor_idx]
        lambda_val = random.random()

        new_sample = [sample[f] + lambda_val * (neighbor[f] - sample[f]) for f in range(d)]
        synthetic.append(new_sample)

    return synthetic
```

### 步骤 2：评估函数

```python
def matthews_correlation_coefficient(tp, tn, fp, fn):
    numerator = (tp * tn) - (fp * fn)
    denominator = math.sqrt(
        (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    )
    return numerator / denominator if denominator > 0 else 0.0
```

### 步骤 3：完整管线

详见 `code/imbalanced.py` 获取完整实现，包含 SMOTE、类权重和阈值优化的组合。

## 用框架实现

```python
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

model = LogisticRegression(class_weight='balanced')
model.fit(X_resampled, y_resampled)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

## 产出物

本课产出 `code/imbalanced.py`。

## 练习题

1. 生成不平衡数据集（1% 正例）。比较始终预测多数类、随机森林（默认）、随机森林（class_weight='balanced'）和 SMOTE+随机森林的 F1 和 MCC。

2. 在同一数据集上比较随机过采样和 SMOTE。展示 SMOTE 产生更好的决策边界。

3. 实现阈值调优：对逻辑回归输出的概率，扫描 0.01 到 0.99 的阈值，找到 F1 最高的阈值。展示它比默认阈值 0.5 好多少。

4. 构建完整管线：SMOTE -> 标准化 -> 逻辑回归（class_weight='balanced'）-> 阈值优化。比较管线中移除任一步骤的性能下降。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 不平衡数据 (Imbalanced Data) | 类别分布严重不均的数据集 |
| SMOTE | 合成少数类过采样技术，通过插值生成新的少数类样本 |
| 过采样 (Oversampling) | 增加少数类样本数量 |
| 欠采样 (Undersampling) | 减少多数类样本数量 |
| 代价敏感学习 | 给不同类别不同的损失权重 |
| AUPRC | 精确率-召回率曲线下面积，不平衡数据的标准指标 |
| MCC | 马修斯相关系数，不受类别不平衡影响的综合指标 |
| 阈值调优 | 调整分类阈值以优化精确率-召回率权衡 |

## 延伸阅读

- [Chawla et al.: SMOTE (2002)](https://arxiv.org/abs/1106.1813) - SMOTE 原始论文
- [He & Garcia: Learning from Imbalanced Data (2009)](https://link.springer.com/article/10.1007/s10115-008-0164-4) - 不平衡学习综述
- [imbalanced-learn 文档](https://imbalanced-learn.org/) - Python 不平衡学习库
