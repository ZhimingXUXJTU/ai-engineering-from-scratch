# 处理不平衡的数据
# 处理不平衡数据


> 当99%的数据是"正常的",准确性是谎言.

> 当99%的数据是"正常"时,准确率就是一个谎言.

**Type:** Build | **类型：** 构建
**Language:**子**语言：**字符串
**Prerequisites:** Phase 2, Lessons 01-09 (especially evaluation metrics) | **前置知识：** Phase 2 第 1-9 课（尤其是评估指标）
**Time:** ~90 minutes | **时间：** 约 90 分钟

## 学习目标

- 从零开始实施SMOTE,并解释合成过量样本采集与随机复制如何不同
  从零实现SMOTE,解释合成采样与随机复制的区别
- 评估不平衡分类器使用F1,AUPRC和马修斯相关系数而不是准确性
  使用F1、AUPRC 和马修斯相关系数 (MCC) 评估不平衡分类器,而非准确率
- 进行类权重,门调整和重新样本策略的比较,并选择对给定的失衡比率的正确方法
  值调整和重采采集策略,为给定不平衡比例选择正确的方法
- 构建一个完整的不平衡数据管道,结合SMOTE,类重量和门优化
  构建结合 SMOTE 类权重和值优化完整不平衡数据管线


> **【中文解读】**
> 金融欺诈检查和医疗诊断中不平衡数据是常见的.

> **【拓展：不平衡数据在真实系统中的挑战】**
> 通过F1、AUPRC等指标进行处理,但通过少数类型的样本中插值产生新样本,但在高层空间中可能产生噪音样本.

## 问题 问题引入

你建立一个欺诈检测模型,它得到99.9%的准确性,你庆祝,然后你意识到它预测"不欺诈"每一个交易.

> 你建立了一个欺诈检测模型. 它获得了99.9%的准确率.

只有0.1%的交易是欺诈性的.模型学会了总是猜测多数类最小化总体错误.这技术上是正确的,完全无用的.

> 这不是错误. 当只有0.1%的交易是欺诈时,这是合理的行为.

网络入侵率:0.01%攻击.制造业缺陷:0.5%缺陷.垃圾邮件过率:20%垃圾邮件. 缩预测:5%缩.少数群体的影响力越高,它往往越少.

> 这在真正需要分类的地方都会发生. 疾病诊断:1% 阳性率. 网络入侵:0.01% 攻击.

准确性失败,因为它对待所有正确的预测均等.正确标记合法的交易和正确捕获欺诈都是一个准确性点.但捕获欺诈是模型存在的全部原因.我们需要指标,技术和培训策略,迫使模型注意罕见但重要的类别.

> 准确率失败因为它同样对待所有正确预测――正确标记合法交易和正确捕获欺诈都算准确率的一分之一――但捕获欺诈是模型存在的全部原因――我们需要迫使模型关注稀有但重要类别的指标,技术和训练策略――

> **【中文解读】**
> 不平衡数据的核心问题:准确率是"谎言"――99.9% 准确率可能只是全猜多数类――正确做法:(1) 换指标用F1、AUPRC、MCC 替代准确率;(2) 重采样SMOTE 过采样少数类或缺采样多数类;(3) 代价敏感学习给少数类更大的损失权重;(4) 调整值降分类通常提高召回率――组合使用多种策略效果最好.

## 概念的核心概念

### 为什么准确性失败

考虑一个数据集,有1000个样本:990个负,10个正.一个模型总是预测负:

> 考虑一个1000个样本的数据集:990个负样本,10个正样本――一个始终预测负类型的模型:

|  | Predicted Positive | Predicted Negative |
|--|---|---|
| Actually Positive | 0 (TP) | 10 (FN) |
| Actually Negative | 0 (FP) | 990 (TN) |

精度 = (0 + 990) / 1000 = 99.0%

模型没有欺诈,没有疾病,没有缺陷,但精确度是99%.

> 模型捕获了零欺诈――零疾病――零缺陷――但准确率显示了99%.

### 更好的指标

**Precision**值得注意的是,在每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上,每一个电路上.

> **精确率**在所有标记为正确的样本中,有多少确实正确?高精确率意味着少假阳性.

**Recall**现在,我们已经发现了多少个正确的结果?

> **召回率**在所有实际为正确的样本中,我们捕获了多少?

**F1 Score**准度和回忆之间的极端不平衡比算术平均更严重.

> **F1 分数**调和平均值――比算术平均值更严厉地惩罚精确率和召回率之间的极端不平衡――

**F-beta Score**精度 (F2) 在欺诈检测中很常见 (错失欺诈比虚假报警更糟).

> **F-beta 分数**= (1 + beta^2) * 精确率 * 召回率 / (beta^2 * 精确率 + 召回率) ・・・当beta > 1 时,召回率更重要──当beta < 1 时,精确率更重要──F2 在欺诈检查中常用(漏检欺诈比误报更糟) ・・・

**AUPRC**(精度回忆曲线下的区域).类似于AUC-ROC,但对于不平衡数据来说更有信息性.随机分类器具有AUPRC等于正分类率 (而不是0.5像ROC).这使得改善更容易看到.

> **AUPRC**(精确率-召回率曲线下面积) .类似于AUC-ROC,但对不平衡数据有更多信息.随机分类器的AUPRC等于正类比例.

**Matthews Correlation Coefficient**= (TP * TN - FP * FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)).从 -1 到 +1. 只会给出高分,当模型在两个类中表现得很好时.即使类的尺寸非常不同时,也会平衡.

> **马修斯相关系数 (MCC)**只有在两个类别上表现良好才给高分――即使类别大差异也很大也保持平衡――

对于上述"总是预测负"模型:精度=0/0 (未定义,通常设置为0),回忆 =0/10 = 0,F1 = 0,MCC = 0. 这些指标正确地确定模型是无价值的.

> 对于上述"始终预测负类"模型:精确率 = 0/0(未定义,通常设为 0),召回率 = 0/10 = 0,F1 = 0,MCC = 0──这些指标正确地将模型识别为无用的──

### 失衡数据管道

```mermaid
flowchart TD
    A[Imbalanced Dataset] --> B{Imbalance Ratio?}
    B -->|Mild: 80/20| C[Class Weights]
    B -->|Moderate: 95/5| D[SMOTE + Threshold Tuning]
    B -->|Severe: 99/1| E[SMOTE + Class Weights + Threshold]
    C --> F[Train Model]
    D --> F
    E --> F
    F --> G[Evaluate with F1 / AUPRC / MCC]
    G --> H{Good Enough?}
    H -->|No| I[Try Different Strategy]
    H -->|Yes| J[Deploy with Monitoring]
    I --> B
```

### 综合少数民族过量样本技术

随机过量样本复制现有少数样本. 这有效,但风险过度匹配,因为模型会多次看到相同的点.

> 随时过采样复制现有少数类型的样本.

通过SMOTE创建新的合成少数样本,这些样本是可行的,但不是副本.

> 创建新的合成少数类样本,它们是合理的,但不是副本.

1. 对于每个少数群体样本x,在其他少数群体样本中,找到其最近邻居的 k
   对于每种少数类型的样本,在其他少数类型中找到其近邻
2. 随机选择一个邻居
   随时选择一个邻居
3. 在 x 与邻居之间的线段上创建一个新的样本
   在 x 和邻居之间的线段上创建一个新的样本

公式:`new_sample = x + random(0, 1) * (neighbor - x)`

> 公式:`new_sample = x + random(0, 1) * (neighbor - x)`

这种方法是对实际少数点进行间接的, 创造样本在同一区域的特征空间,而不仅仅是复制现有数据.

> 这是在真正的少数类点之间插入值,在特征空间的同一区域创建样本,而不仅仅是复制现有数据.

```mermaid
flowchart LR
    subgraph Original["Original Minority Points"]
        P1["x1 (1.0, 2.0)"]
        P2["x2 (1.5, 2.5)"]
        P3["x3 (2.0, 1.5)"]
    end
    subgraph SMOTE["SMOTE Generation"]
        direction TB
        S1["Pick x1, neighbor x2"]
        S2["random t = 0.4"]
        S3["new = x1 + 0.4*(x2-x1)"]
        S4["new = (1.2, 2.2)"]
        S1 --> S2 --> S3 --> S4
    end
    Original --> SMOTE
    subgraph Result["Augmented Set"]
        R1["x1 (1.0, 2.0)"]
        R2["x2 (1.5, 2.5)"]
        R3["x3 (2.0, 1.5)"]
        R4["synthetic (1.2, 2.2)"]
    end
    SMOTE --> Result
```

### 采样策略的比较

**Random Oversampling**复制少数群体样本以匹配多数群体数量.
- 优点:简单,没有信息丢失
  优点:简单,无信息损失
- 缺点:精确复制导致过度适应,增加了训练时间
  缺点:完全相同的副本导致过适合,增加训练时间

**Random Undersampling**取消多数样本,以匹配少数人数.
- 优势:快速训练,简单
  优点:训练快,简单
- 缺点:丢弃潜在有用的多数数据,更高的差异性
  缺点:丢弃可能有用的大部分数据,方差更高

**SMOTE**通过插射,创造合成少数群体样本.
- 优点:生成新的数据点,减少随机过度采样相比过度匹配
  优点:生成新数据点,比随机采样减少过适应
- 缺点:可以在决策边界附近产生噪音样本,不考虑多数类分布
  缺点:可能在决策边界附近创建噪声样本,不考虑多数类分布

| Strategy | Data Changed | Risk | When to Use |
|----------|-------------|------|-------------|
| Oversample | Minority duplicated | Overfitting | Small datasets, moderate imbalance |
| Undersample | Majority removed | Information loss | Large datasets, want fast training |
| SMOTE | Synthetic minority added | Boundary noise | Moderate imbalance, enough minority samples for k-NN |

### 类型的重量

换取数据,更改模型处理错误的方式. 赋予更高的重量错误分类少数类.

> 不改变数据,而是改变模型对待错误的方式.

对于950负样本和50正样本的二进制问题:
- 负类的重量 = n_samples / (2 * n_negative) = 1000 / (2 * 950) = 0.526
  负类权重 = n_样本 / (2 * n_负) = 1000 / (2 * 950) = 0.526
- 积极类的重量 = n_样本 / (2 * n_积极) = 1000 / (2 * 50) = 10.0
  正类权重 = n_样本 / (2 * n_正) = 1000 / (2 * 50) = 10.0

正面类型的重量是19倍.错误分类一个正面样本的成本是错误分类19个负面样本.模型被迫注意少数类型.

> 正类获得19倍权重.正类的一个正品样本的价格等于正品类19个负品样本.

在物流回归中,这改变了损失函数:

```
weighted_loss = -sum(w_i * [y_i * log(p_i) + (1-y_i) * log(1-p_i)])
```

在哪里 w_i 取决于样本 i 的类型.

类重量在数学上相当于预期过度样本,但没有创造新的数据点. 这使它们更快,避免了重复样本过度合适的风险.

> 类权重在预期上与过采样数学等价,但没有创建新的数据点.

### 值调整

大多数分类器输出一个概率.默认门为0.5:如果P ((正) >=0.5,预测正.但0.5是任意的.当类是不平衡时,最佳门通常要低得多.

> 大多数分类器输出概率──默认值为0.5:如果P(正) >=0.5,预测为正确──但0.5是任意──当类别不平衡时,最优值通常低得多──

过程:
1. 训练一个模型
   训练一个模型
2. 在验证集中得到预测概率
   在验证集中获取预测概率
3. 扫描门从0到1.0
   从0.0到1.0扫描值
4. 在每一个门时计算F1 (或您选择的指标)
   在每个值下计算F1 ((或你选择的指标)
5. 选择最大化你的标准值
   选择最大化你的指标的值

```mermaid
flowchart LR
    A[Model] --> B[Predict Probabilities]
    B --> C[Sweep Thresholds 0.0 to 1.0]
    C --> D[Compute F1 at Each]
    D --> E[Pick Best Threshold]
    E --> F[Use in Production]
```

模型可能输出 P ((欺诈) = 0.15 对欺诈交易.在0.5的门上,这个值被归类为不是欺诈.在0.10的门上,它被正确捕获.概率校准比排名更不重要 - 只要欺诈比非欺诈更高的概率,就有一个分离它们的门.

> 模型可能对一个欺诈交易输出 P(欺诈) =0.15──在值0.5下,被分为非欺诈──在值0.10下,它被正确捕获──概率校准不如排名重要只要欺诈获得比非欺诈更高的概率,就存在一个能够分离它们的值──

### 低成本的学习

类重量概括. 代替统一成本,分配特定的错误分类成本:

> 类权重的推广――不使用统一代价,而是分配特定的误分类代价:

| | Predict Positive | Predict Negative |
|--|---|---|
| Actually Positive | 0 (correct) | C_FN = 100 |
| Actually Negative | C_FP = 1 | 0 (correct) |

错过欺诈交易 (FN) 的成本高于虚假报警 (FP) 的100倍. 该模型优化了总成本,而不是总错误数量.

> 漏检一笔欺诈交易的价格是FP的100倍.

没有发现癌症的确诊,与假报警,导致额外的生物检查,产生了非常不同的成本.

> 实际上,当你估计现实世界成本时,这是最有原则的方法.

### 决策流程图

```mermaid
flowchart TD
    A[Start: Imbalanced Dataset] --> B{How imbalanced?}
    B -->|"< 70/30"| C["Mild: try class weights first"]
    B -->|"70/30 to 95/5"| D["Moderate: SMOTE + class weights"]
    B -->|"> 95/5"| E["Severe: combine multiple strategies"]
    C --> F{Enough data?}
    D --> F
    E --> F
    F -->|"< 1000 samples"| G["Oversample or SMOTE, avoid undersampling"]
    F -->|"1000-10000"| H["SMOTE + threshold tuning"]
    F -->|"> 10000"| I["Undersampling OK, or class weights"]
    G --> J[Train + Evaluate with F1/AUPRC]
    H --> J
    I --> J
    J --> K{Recall high enough?}
    K -->|No| L[Lower threshold]
    K -->|Yes| M{Precision acceptable?}
    M -->|No| N[Raise threshold or add features]
    M -->|Yes| O[Ship it]
```

## 建立它,实现它.

> **【中文解读】**
> 从零实现SMOTE (SMOTE) 合成少数类过采样技术):对每个少数类样本,找到其近邻,在连线随时插值生成新的合成样本.

> **【拓展：工业级不平衡数据处理的高级技术】**
> 在实际金融风控中,处理不平衡数据的策略比SMOTE更复杂:使用焦点损失,让模型更关注难分类样本) 两阶段训练 (先使用采样训练,再使用原始数据微调) 代价敏感学习 (将欺诈的误分类代价设为正常交易的100倍) ⋅Square (前方方方方) 欺诈检测系统使用多个模型融合 + 动态来处理每天百万级交易中极少数欺诈案例).
```figure
class-imbalance
```

## 建立它

### 步骤1:生成一个不平衡的数据集

```python
import numpy as np


def make_imbalanced_data(n_majority=950, n_minority=50, seed=42):
    rng = np.random.RandomState(seed)

    X_maj = rng.randn(n_majority, 2) * 1.0 + np.array([0.0, 0.0])
    X_min = rng.randn(n_minority, 2) * 0.8 + np.array([2.5, 2.5])

    X = np.vstack([X_maj, X_min])
    y = np.concatenate([np.zeros(n_majority), np.ones(n_minority)])

    shuffle_idx = rng.permutation(len(y))
    return X[shuffle_idx], y[shuffle_idx]
```

### 步骤2:从零开始

```python
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


def find_k_neighbors(X, idx, k):
    distances = []
    for i in range(len(X)):
        if i == idx:
            continue
        d = euclidean_distance(X[idx], X[i])
        distances.append((i, d))
    distances.sort(key=lambda x: x[1])
    return [d[0] for d in distances[:k]]


def smote(X_minority, k=5, n_synthetic=100, seed=42):
    rng = np.random.RandomState(seed)
    n_samples = len(X_minority)
    k = min(k, n_samples - 1)
    synthetic = []

    for _ in range(n_synthetic):
        idx = rng.randint(0, n_samples)
        neighbors = find_k_neighbors(X_minority, idx, k)
        neighbor_idx = neighbors[rng.randint(0, len(neighbors))]
        t = rng.random()
        new_point = X_minority[idx] + t * (X_minority[neighbor_idx] - X_minority[idx])
        synthetic.append(new_point)

    return np.array(synthetic)
```

### 步骤3:随机过量样本和下样本

```python
def random_oversample(X, y, seed=42):
    rng = np.random.RandomState(seed)
    classes, counts = np.unique(y, return_counts=True)
    max_count = counts.max()

    X_resampled = list(X)
    y_resampled = list(y)

    for cls, count in zip(classes, counts):
        if count < max_count:
            cls_indices = np.where(y == cls)[0]
            n_needed = max_count - count
            chosen = rng.choice(cls_indices, size=n_needed, replace=True)
            X_resampled.extend(X[chosen])
            y_resampled.extend(y[chosen])

    X_out = np.array(X_resampled)
    y_out = np.array(y_resampled)
    shuffle = rng.permutation(len(y_out))
    return X_out[shuffle], y_out[shuffle]


def random_undersample(X, y, seed=42):
    rng = np.random.RandomState(seed)
    classes, counts = np.unique(y, return_counts=True)
    min_count = counts.min()

    X_resampled = []
    y_resampled = []

    for cls in classes:
        cls_indices = np.where(y == cls)[0]
        chosen = rng.choice(cls_indices, size=min_count, replace=False)
        X_resampled.extend(X[chosen])
        y_resampled.extend(y[chosen])

    X_out = np.array(X_resampled)
    y_out = np.array(y_resampled)
    shuffle = rng.permutation(len(y_out))
    return X_out[shuffle], y_out[shuffle]
```

### 阶段4:与类权重的物流回归

```python
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def logistic_regression_weighted(X, y, weights, lr=0.01, epochs=200):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = sigmoid(z)
        error = pred - y
        weighted_error = error * weights

        gradient_w = (X.T @ weighted_error) / n_samples
        gradient_b = np.mean(weighted_error)

        w -= lr * gradient_w
        b -= lr * gradient_b

    return w, b


def compute_class_weights(y):
    classes, counts = np.unique(y, return_counts=True)
    n_samples = len(y)
    n_classes = len(classes)
    weight_map = {}
    for cls, count in zip(classes, counts):
        weight_map[cls] = n_samples / (n_classes * count)
    return np.array([weight_map[yi] for yi in y])
```

### 步骤5:调整门

```python
def find_optimal_threshold(y_true, y_probs, metric="f1"):
    best_threshold = 0.5
    best_score = -1.0

    for threshold in np.arange(0.05, 0.96, 0.01):
        y_pred = (y_probs >= threshold).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))

        if metric == "f1":
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        elif metric == "recall":
            score = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        elif metric == "precision":
            score = tp / (tp + fp) if (tp + fp) > 0 else 0.0

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold, best_score
```

### 步骤 6: 评估功能

```python
def confusion_matrix_values(y_true, y_pred):
    tp = np.sum((y_pred == 1) & (y_true == 1))
    tn = np.sum((y_pred == 0) & (y_true == 0))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    return tp, tn, fp, fn


def compute_metrics(y_true, y_pred):
    tp, tn, fp, fn = confusion_matrix_values(y_true, y_pred)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    denom = np.sqrt(float((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
    mcc = (tp * tn - fp * fn) / denom if denom > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "mcc": mcc,
    }
```

### 步骤7:将所有方法进行比较

```python
X, y = make_imbalanced_data(950, 50, seed=42)
split = int(0.8 * len(y))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Baseline: no treatment
w_base, b_base = logistic_regression_weighted(
    X_train, y_train, np.ones(len(y_train)), lr=0.1, epochs=300
)
probs_base = sigmoid(X_test @ w_base + b_base)
preds_base = (probs_base >= 0.5).astype(int)

# Oversampled
X_over, y_over = random_oversample(X_train, y_train)
w_over, b_over = logistic_regression_weighted(
    X_over, y_over, np.ones(len(y_over)), lr=0.1, epochs=300
)
preds_over = (sigmoid(X_test @ w_over + b_over) >= 0.5).astype(int)

# SMOTE
minority_mask = y_train == 1
X_minority = X_train[minority_mask]
synthetic = smote(X_minority, k=5, n_synthetic=len(y_train) - 2 * int(minority_mask.sum()))
X_smote = np.vstack([X_train, synthetic])
y_smote = np.concatenate([y_train, np.ones(len(synthetic))])
w_sm, b_sm = logistic_regression_weighted(
    X_smote, y_smote, np.ones(len(y_smote)), lr=0.1, epochs=300
)
preds_smote = (sigmoid(X_test @ w_sm + b_sm) >= 0.5).astype(int)

# Class weights
sample_weights = compute_class_weights(y_train)
w_cw, b_cw = logistic_regression_weighted(
    X_train, y_train, sample_weights, lr=0.1, epochs=300
)
probs_cw = sigmoid(X_test @ w_cw + b_cw)
preds_cw = (probs_cw >= 0.5).astype(int)

# Threshold tuning (tune on held-out validation set, not test set)
probs_val = sigmoid(X_val @ w_cw + b_cw)
best_thresh, best_f1 = find_optimal_threshold(y_val, probs_val, metric="f1")
preds_thresh = (probs_cw >= best_thresh).astype(int)
```

代码文件将所有这些运行在一个脚本中,

> 代码文件在单个脚本中运行所有这些并打印结果.

## 用它实现框架

通过学习和不平衡学习,这些技术是单行:

> 通过使用小学习和失衡学习,这些技术只需要一行代码:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)

model_weighted = LogisticRegression(class_weight="balanced")
model_weighted.fit(X_train, y_train)
print(classification_report(y_test, model_weighted.predict(X_test)))

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
model_smote = LogisticRegression()
model_smote.fit(X_resampled, y_resampled)
print(classification_report(y_test, model_smote.predict(X_test)))

pipeline = Pipeline([
    ("smote", SMOTE()),
    ("model", LogisticRegression(class_weight="balanced")),
])
pipeline.fit(X_train, y_train)
print(classification_report(y_test, pipeline.predict(X_test)))
```

首先,我们可以看到一个小组的数量,然后我们可以看到一个小组的数量.

> 从零实现准确显示了每种技术的作用.SMOTE就是少数类的 k-NN 插值.类权重乘以损失.

## 运送它.

这一课产生了:
- `outputs/skill-imbalanced-data.md`-- 处理不平衡分类问题的决策检查清单

## 练习题

1. **Borderline-SMOTE**通过修改SMOTE实现,只能生成接近决策边界的少数点的合成样本 (其中 k-近邻包括多数类样本).
   1. 生成不平衡数据集 ((1% 正例) 〔比较始终预测多数类、随机森林〕默认)、随机森林

2. **Cost matrix optimization**运用成本对比矩阵为参数的成本敏感学习.创建一个取成本矩阵的函数,返回最大的预测,以最大限度地降低预期成本.使用不同的成本比率 (1:10, 1:100, 1:1000) 测试,并绘制精度召回权衡如何变化.
   2. 在同一数据集中,与采样和SMOTE相比较.

3. **Threshold calibration**实现平板规模化 (将模型原始输出进行物流回归,以产生校准概率). 在校准之前和之后进行精度召回曲线的比较. 显示校准不会改变排名 (AUC保持不变),而是使概率变得更有意义.
   3. 实现值调整:对逻辑回归输出概率,扫描0.01到0.99的值,找到F1最高值――展示它比默认值0.5少很多――

4. **Ensemble with balanced bagging**训练多个模型,每个模型都基于均衡的启动样本 (所有少数+多数的随机子集).平均他们的预测.与单个模型进行比较.测量运行中的性能和差异.
   4. 构建完整管线:SMOTE -> 标准化 -> 逻辑归归(class_weight='balanced')-> 值优化――比较管线中移除任一步的性能下降――

5. **Imbalance ratio experiment**对于每一个比率,训练与与没有SMOTE. 剧情 F1对两个方法的不平衡比率. 在哪个比率上,SMOTE开始产生有意义的差异?

> **【中文解读】**
> 不平衡数据处理的完整策略组合:(1) 评估指标使用F1/AUPRC/MCC 替代准确率;(2) 重采样SMOTE 过采样少数类或随机欠采样多数类;(3) 代价敏感在损失函数中给少数类加权((明确中级_权重='平衡');(4) 值调整降分类值提高召回率――关键洞察:没有万能方法,不同策略组合通常最好.

> **【拓展：Focal Loss——深度学习中的不平衡数据解决方案】**
> 焦点损失 (Focal Loss) 简称是"重量损失"的核心思想:使模型集中于"难分类"的样本――公式:FLp) = -(1-p) ^gamma * log(p),gamma=2 时效果最好――RetinaNet使用焦点损失在COCO检测任务上超越了当时的SOTA方法――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Class imbalance | "One class has way more samples" | The distribution of classes in the dataset is significantly skewed, causing models to favor the majority class |
| SMOTE | "Synthetic oversampling" | Creates new minority samples by interpolating between existing minority samples and their k-nearest minority neighbors |
| Class weights | "Making errors on rare classes more expensive" | Multiplying the loss function by class-specific weights so the model penalizes minority misclassification more heavily |
| Threshold tuning | "Moving the decision boundary" | Changing the probability cutoff for classification from the default 0.5 to a value that optimizes the desired metric |
| Precision-recall tradeoff | "You cannot have both" | Lowering the threshold catches more positives (higher recall) but also flags more false positives (lower precision), and vice versa |
| AUPRC | "Area under the PR curve" | Summarizes the precision-recall curve into a single number; more informative than AUC-ROC when classes are heavily imbalanced |
| Matthews Correlation Coefficient | "The balanced metric" | A correlation between predicted and actual labels that produces a high score only when the model performs well on both classes |
| Cost-sensitive learning | "Different mistakes cost different amounts" | Incorporating real-world misclassification costs into the training objective so the model optimizes for total cost, not error count |
| Random oversampling | "Duplicate the minority" | Repeating minority class samples to balance class counts; simple but risks overfitting to duplicated points |

## 继续阅读 继续阅读

- [SMOTE: Synthetic Minority Over-sampling Technique (Chawla et al., 2002)](https://arxiv.org/abs/1106.1813)--原始的SMOTE论文,仍然是最受引用的不平衡学习论文
  [Chawla et al.: SMOTE (2002)](https://arxiv.org/abs/1106.1813)- 史莫特 原始论文
- [Learning from Imbalanced Data (He & Garcia, 2009)](https://ieeexplore.ieee.org/document/5128907)综合调查包括采样,成本敏感和算法方法
  [He & Garcia: Learning from Imbalanced Data (2009)](https://link.springer.com/article/10.1007/s10115-008-0164-4)- 不平衡学习综述
- [imbalanced-learn documentation](https://imbalanced-learn.org/stable/)-- 配备SMOTE变体,低样本策略和管道集成的Python库
  [imbalanced-learn 文档](https://imbalanced-learn.org/)- 字符号不平衡学习库
- [The Precision-Recall Plot Is More Informative than the ROC Plot (Saito & Rehmsmeier, 2015)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432)-- 什么时候和为什么要偏好 PR 曲线而不是 ROC 曲线,以解决不平衡问题
