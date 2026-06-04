# 逻辑回归

> 逻辑回归将直线弯成 S 形曲线，用概率回答是非问题。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 1-2 课（什么是机器学习、线性回归）
**时长：** 约 90 分钟

## 学习目标

- 从零实现逻辑回归，掌握 Sigmoid 函数和二元交叉熵损失
- 计算并解释精确率 (Precision)、召回率 (Recall)、F1 分数和混淆矩阵
- 解释为什么均方误差 (MSE) 不适用于分类任务，以及为什么二元交叉熵能产生凸的代价曲面
- 构建 Softmax 回归模型进行多分类，并评估阈值调优的权衡

## 问题引入

你想根据肿瘤大小预测它是恶性还是良性。你尝试用线性回归。它输出的数字如 0.3、1.7 或 -0.5。这些数字意味着什么？1.7 是"非常恶性"？-0.5 是"非常良性"？线性回归输出的是无界数值。而分类需要 0 到 1 之间的有界概率，以及一个明确的决策：是或否。

逻辑回归解决了这个问题。它取相同的线性组合 (wx + b)，通过 Sigmoid 函数传递，将任何数值压缩到 (0, 1) 范围内。输出就是概率。你设定一个阈值（通常为 0.5），然后做出决策。

这是实践中最广泛使用的算法之一。尽管名字中有"回归"，逻辑回归是一种分类算法，而不是回归算法。名字来源于它使用的逻辑（Sigmoid）函数。

## 核心概念

### 为什么线性回归不适用于分类

假设根据学习时间预测通过/不通过（1/0）。线性回归拟合一条直线：

```
学习时间:  1   2   3   4   5   6   7   8   9   10
实际结果:  0   0   0   0   1   1   1   1   1   1
```

线性拟合可能在学习 1 小时时产生 -0.2 的预测，在 10 小时时产生 1.3 的预测。这些值不是概率——它们低于 0 且高于 1。更糟糕的是，一个离群值（学习了 50 小时的人）会拖动整条线，改变所有人的预测。

分类需要一个满足以下条件的函数：
- 输出 0 到 1 之间的值（概率）
- 产生急剧的过渡（决策边界）
- 不被远离边界的离群值扭曲

### Sigmoid 函数

Sigmoid 函数恰好满足这些需求：

```
sigmoid(z) = 1 / (1 + e^(-z))
```

性质：
- 当 z 很大且为正时，sigmoid(z) 趋近于 1
- 当 z 很大且为负时，sigmoid(z) 趋近于 0
- 当 z = 0 时，sigmoid(z) = 0.5
- 输出始终在 0 和 1 之间
- 函数处处光滑可微

导数有一个便捷的形式：sigmoid'(z) = sigmoid(z) * (1 - sigmoid(z))。这使得梯度计算非常高效。

### 逻辑回归 = 线性模型 + Sigmoid

模型先计算 z = wx + b（与线性回归相同），然后应用 Sigmoid：

```mermaid
flowchart LR
    X[输入特征 x] --> L["线性变换: z = wx + b"]
    L --> S["Sigmoid: p = 1/(1+e^-z)"]
    S --> D{"p >= 0.5?"}
    D -->|是| P[预测为 1]
    D -->|否| N[预测为 0]
```

输出 p 被解释为 P(y=1 | x)，即输入属于类别 1 的概率。决策边界是 wx + b = 0 的位置，此时 Sigmoid 输出恰好为 0.5。

### 二元交叉熵损失

你不能在逻辑回归中使用均方误差 (MSE)。MSE 与 Sigmoid 组合会产生非凸的代价曲面，存在许多局部最小值。应使用二元交叉熵（对数损失）：

```
Loss = -(1/n) * sum(y * log(p) + (1-y) * log(1-p))
```

为什么有效：
- 当 y=1 且 p 接近 1 时：log(1) = 0，损失接近 0（正确，低代价）
- 当 y=1 且 p 接近 0 时：log(0) 趋近负无穷，损失巨大（错误，高代价）
- 当 y=0 且 p 接近 0 时：log(1) = 0，损失接近 0（正确，低代价）
- 当 y=0 且 p 接近 1 时：log(0) 趋近负无穷，损失巨大（错误，高代价）

这个损失函数对逻辑回归是凸函数，保证找到唯一的全局最小值。

### 逻辑回归的梯度下降

二元交叉熵与 Sigmoid 组合的梯度形式非常简洁：

```
dL/dw = (1/n) * sum((p - y) * x)
dL/db = (1/n) * sum(p - y)
```

这与线性回归的梯度看起来完全相同。区别在于 p = sigmoid(wx + b) 而非 p = wx + b。Sigmoid 引入了非线性，但梯度更新规则保持不变。

```mermaid
flowchart TD
    A[初始化 w=0, b=0] --> B[前向传播: z = wx+b, p = sigmoid(z)]
    B --> C[计算损失: 二元交叉熵]
    C --> D["计算梯度: dw = (1/n) * sum((p-y)*x)"]
    D --> E[更新: w = w - lr*dw, b = b - lr*db]
    E --> F{收敛?}
    F -->|否| B
    F -->|是| G[模型训练完成]
```

### 决策边界

对于二维输入（两个特征），决策边界是满足以下等式的直线：

```
w1*x1 + w2*x2 + b = 0
```

一侧的点被分类为 1，另一侧为 0。逻辑回归总是产生线性决策边界。如果需要曲线边界，可以添加多项式特征或使用非线性模型。

### 多分类与 Softmax

二分类逻辑回归处理两个类别。对于 k 个类别，使用 Softmax 函数：

```
softmax(z_i) = e^(z_i) / sum(e^(z_j) for all j)
```

每个类别有自己的权重向量。模型为每个类别计算一个得分 z_i，然后 Softmax 将得分转换为总和为 1 的概率。预测类别是概率最高的那个。

损失函数变为分类交叉熵 (Categorical Cross-Entropy)：

```
Loss = -(1/n) * sum(sum(y_k * log(p_k)))
```

其中 y_k 对真实类别为 1，对其余类别为 0（独热编码）。

### 评估指标

仅看准确率 (Accuracy) 是不够的。对于 95% 负例和 5% 正例的数据集，一个始终预测为负的模型有 95% 的准确率，但毫无价值。

**混淆矩阵 (Confusion Matrix)**：

| | 预测为正 | 预测为负 |
|---|---|---|
| 实际为正 | 真正例 (TP) | 假负例 (FN) |
| 实际为负 | 假正例 (FP) | 真负例 (TN) |

**精确率 (Precision)**：在所有预测为正的样本中，有多少是真正的正例？
```
Precision = TP / (TP + FP)
```

**召回率 (Recall)**（灵敏度 Sensitivity）：在所有真正的正例中，我们找出了多少？
```
Recall = TP / (TP + FN)
```

**F1 分数**：精确率和召回率的调和平均。平衡两个指标。
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

何时优先使用哪个指标：
- **精确率**：当假正例代价高时（垃圾邮件过滤，你不想误拦正常邮件）
- **召回率**：当假负例代价高时（癌症筛查，你不想漏掉肿瘤）
- **F1**：当你需要一个平衡的综合指标时

### 步骤 1：Sigmoid 函数和数据生成

```python
import random
import math

def sigmoid(z):
    z = max(-500, min(500, z))  # 裁剪防止数值溢出
    return 1.0 / (1.0 + math.exp(-z))  # Sigmoid 函数：将任意实数映射到 (0,1)


random.seed(42)
N = 200
X = []
y = []

# 生成类别 0 的数据：中心在 (2,2)
for _ in range(N // 2):
    X.append([random.gauss(2, 1), random.gauss(2, 1)])
    y.append(0)

# 生成类别 1 的数据：中心在 (5,5)
for _ in range(N // 2):
    X.append([random.gauss(5, 1), random.gauss(5, 1)])
    y.append(1)

combined = list(zip(X, y))
random.shuffle(combined)
X, y = zip(*combined)
X = list(X)
y = list(y)

print(f"生成了 {N} 个样本（2 个类别，2 个特征）")
print(f"类别 0 中心: (2, 2), 类别 1 中心: (5, 5)")
print(f"前 5 个样本:")
for i in range(5):
    print(f"  特征: [{X[i][0]:.2f}, {X[i][1]:.2f}], 标签: {y[i]}")
```

### 步骤 2：从零实现逻辑回归

```python
class LogisticRegression:
    def __init__(self, n_features, learning_rate=0.01):
        self.weights = [0.0] * n_features  # 权重初始化为 0
        self.bias = 0.0  # 偏置初始化为 0
        self.lr = learning_rate  # 学习率
        self.loss_history = []  # 记录训练损失

    def predict_proba(self, x):
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias  # 线性组合 z = wx + b
        return sigmoid(z)  # 通过 Sigmoid 得到概率

    def predict(self, x, threshold=0.5):
        return 1 if self.predict_proba(x) >= threshold else 0  # 概率 >= 阈值则预测为 1

    def compute_loss(self, X, y):
        n = len(y)
        total = 0.0
        for i in range(n):
            p = self.predict_proba(X[i])
            p = max(1e-15, min(1 - 1e-15, p))  # 裁剪防止 log(0)
            # 二元交叉熵损失
            total += y[i] * math.log(p) + (1 - y[i]) * math.log(1 - p)
        return -total / n  # 取负号得到正值损失

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            dw = [0.0] * n_features
            db = 0.0
            for i in range(n):
                p = self.predict_proba(X[i])
                error = p - y[i]  # 预测概率 - 真实标签
                for j in range(n_features):
                    dw[j] += error * X[i][j]  # 累积权重梯度
                db += error  # 累积偏置梯度
            # 梯度下降更新参数
            for j in range(n_features):
                self.weights[j] -= self.lr * (dw[j] / n)
            self.bias -= self.lr * (db / n)
            loss = self.compute_loss(X, y)
            self.loss_history.append(loss)
            if epoch % print_every == 0:
                print(f"  轮次 {epoch:4d} | 损失: {loss:.4f} | w: [{self.weights[0]:.3f}, {self.weights[1]:.3f}] | b: {self.bias:.3f}")
        return self

    def accuracy(self, X, y):
        correct = sum(1 for i in range(len(y)) if self.predict(X[i]) == y[i])
        return correct / len(y)


split = int(0.8 * N)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print("\n=== 训练逻辑回归 ===")
model = LogisticRegression(n_features=2, learning_rate=0.1)
model.fit(X_train, y_train, epochs=1000, print_every=200)

print(f"\n训练集准确率: {model.accuracy(X_train, y_train):.4f}")
print(f"测试集准确率:  {model.accuracy(X_test, y_test):.4f}")
print(f"权重: [{model.weights[0]:.4f}, {model.weights[1]:.4f}]")
print(f"偏置: {model.bias:.4f}")
```

### 步骤 3：从零实现混淆矩阵和评估指标

```python
class ClassificationMetrics:
    def __init__(self, y_true, y_pred):
        # 统计混淆矩阵四个值
        self.tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)  # 真正例
        self.tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)  # 真负例
        self.fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)  # 假正例
        self.fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)  # 假负例

    def accuracy(self):
        total = self.tp + self.tn + self.fp + self.fn
        return (self.tp + self.tn) / total if total > 0 else 0

    def precision(self):
        denom = self.tp + self.fp
        return self.tp / denom if denom > 0 else 0

    def recall(self):
        denom = self.tp + self.fn
        return self.tp / denom if denom > 0 else 0

    def f1(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r) if (p + r) > 0 else 0

    def print_confusion_matrix(self):
        print(f"\n  混淆矩阵:")
        print(f"                  预测")
        print(f"                  正   负")
        print(f"  实际 正     {self.tp:4d}  {self.fn:4d}")
        print(f"  实际 负     {self.fp:4d}  {self.tn:4d}")

    def print_report(self):
        self.print_confusion_matrix()
        print(f"\n  准确率:  {self.accuracy():.4f}")
        print(f"  精确率: {self.precision():.4f}")
        print(f"  召回率:    {self.recall():.4f}")
        print(f"  F1 分数:  {self.f1():.4f}")


y_pred_test = [model.predict(x) for x in X_test]
print("\n=== 分类报告（测试集）===")
metrics = ClassificationMetrics(y_test, y_pred_test)
metrics.print_report()
```

### 步骤 4：决策边界分析

```python
print("\n=== 决策边界 ===")
w1, w2 = model.weights
b = model.bias
print(f"决策边界: {w1:.4f}*x1 + {w2:.4f}*x2 + {b:.4f} = 0")
if abs(w2) > 1e-10:
    print(f"解出 x2:     x2 = {-w1/w2:.4f}*x1 + {-b/w2:.4f}")

print("\n边界附近的样本预测:")
test_points = [
    [3.0, 3.0],
    [3.5, 3.5],
    [4.0, 4.0],
    [2.5, 2.5],
    [5.0, 5.0],
]
for point in test_points:
    prob = model.predict_proba(point)
    pred = model.predict(point)
    print(f"  [{point[0]}, {point[1]}] -> 概率={prob:.4f}, 类别={pred}")
```

### 步骤 5：多分类与 Softmax

```python
class SoftmaxRegression:
    def __init__(self, n_features, n_classes, learning_rate=0.01):
        self.n_features = n_features
        self.n_classes = n_classes
        self.lr = learning_rate
        self.weights = [[0.0] * n_features for _ in range(n_classes)]
        self.biases = [0.0] * n_classes

    def softmax(self, scores):
        max_score = max(scores)
        exp_scores = [math.exp(s - max_score) for s in scores]
        total = sum(exp_scores)
        return [e / total for e in exp_scores]

    def predict_proba(self, x):
        scores = [
            sum(self.weights[k][j] * x[j] for j in range(self.n_features)) + self.biases[k]
            for k in range(self.n_classes)
        ]
        return self.softmax(scores)

    def predict(self, x):
        probs = self.predict_proba(x)
        return probs.index(max(probs))

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        for epoch in range(epochs):
            grad_w = [[0.0] * self.n_features for _ in range(self.n_classes)]
            grad_b = [0.0] * self.n_classes
            total_loss = 0.0
            for i in range(n):
                probs = self.predict_proba(X[i])
                for k in range(self.n_classes):
                    target = 1.0 if y[i] == k else 0.0
                    error = probs[k] - target
                    for j in range(self.n_features):
                        grad_w[k][j] += error * X[i][j]
                    grad_b[k] += error
                true_prob = max(probs[y[i]], 1e-15)
                total_loss -= math.log(true_prob)
            for k in range(self.n_classes):
                for j in range(self.n_features):
                    self.weights[k][j] -= self.lr * (grad_w[k][j] / n)
                self.biases[k] -= self.lr * (grad_b[k] / n)
            if epoch % print_every == 0:
                print(f"  轮次 {epoch:4d} | 损失: {total_loss / n:.4f}")
        return self

    def accuracy(self, X, y):
        correct = sum(1 for i in range(len(y)) if self.predict(X[i]) == y[i])
        return correct / len(y)


random.seed(42)
X_3class = []
y_3class = []

centers = [(1, 1), (5, 1), (3, 5)]
for label, (cx, cy) in enumerate(centers):
    for _ in range(50):
        X_3class.append([random.gauss(cx, 0.8), random.gauss(cy, 0.8)])
        y_3class.append(label)

combined = list(zip(X_3class, y_3class))
random.shuffle(combined)
X_3class, y_3class = zip(*combined)
X_3class = list(X_3class)
y_3class = list(y_3class)

split_3 = int(0.8 * len(X_3class))
X_train_3 = X_3class[:split_3]
y_train_3 = y_3class[:split_3]
X_test_3 = X_3class[split_3:]
y_test_3 = y_3class[split_3:]

print("\n=== 多分类 Softmax 回归（3 个类别）===")
softmax_model = SoftmaxRegression(n_features=2, n_classes=3, learning_rate=0.1)
softmax_model.fit(X_train_3, y_train_3, epochs=1000, print_every=200)
print(f"\n训练集准确率: {softmax_model.accuracy(X_train_3, y_train_3):.4f}")
print(f"测试集准确率:  {softmax_model.accuracy(X_test_3, y_test_3):.4f}")

print("\n样本预测:")
for i in range(5):
    probs = softmax_model.predict_proba(X_test_3[i])
    pred = softmax_model.predict(X_test_3[i])
    print(f"  真实: {y_test_3[i]}, 预测: {pred}, 概率: [{', '.join(f'{p:.3f}' for p in probs)}]")
```

### 步骤 6：阈值调优

```python
print("\n=== 阈值调优 ===")
print("默认阈值: 0.5。调整阈值会在精确率和召回率之间做权衡。\n")

thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
print(f"{'阈值':>10} {'准确率':>10} {'精确率':>10} {'召回率':>10} {'F1':>10}")
print("-" * 52)

for t in thresholds:
    y_pred_t = [1 if model.predict_proba(x) >= t else 0 for x in X_test]
    m = ClassificationMetrics(y_test, y_pred_t)
    print(f"{t:>10.1f} {m.accuracy():>10.4f} {m.precision():>10.4f} {m.recall():>10.4f} {m.f1():>10.4f}")
```

## 用框架实现

现在用 scikit-learn 实现同样的功能。

```python
from sklearn.linear_model import LogisticRegression as SklearnLR
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X_0 = np.random.randn(100, 2) + [2, 2]
X_1 = np.random.randn(100, 2) + [5, 5]
X_sk = np.vstack([X_0, X_1])
y_sk = np.array([0] * 100 + [1] * 100)

X_tr, X_te, y_tr, y_te = train_test_split(X_sk, y_sk, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_tr)
X_te_sc = scaler.transform(X_te)

lr = SklearnLR()
lr.fit(X_tr_sc, y_tr)
y_pred = lr.predict(X_te_sc)

print("=== Scikit-learn 逻辑回归 ===")
print(f"准确率:  {accuracy_score(y_te, y_pred):.4f}")
print(f"精确率: {precision_score(y_te, y_pred):.4f}")
print(f"召回率:    {recall_score(y_te, y_pred):.4f}")
print(f"F1:        {f1_score(y_te, y_pred):.4f}")
print(f"\n混淆矩阵:\n{confusion_matrix(y_te, y_pred)}")
print(f"\n分类报告:\n{classification_report(y_te, y_pred)}")
```

你从零实现的版本产生了相同的决策边界和指标。scikit-learn 增加了求解器选项（liblinear、lbfgs、saga）、自动正则化、多分类策略（一对多、多项式）和数值稳定性优化。

## 产出物

本课产出：
- `code/logistic_regression.py` - 从零实现的逻辑回归及评估指标

## 练习题

1. 生成一个**非**线性可分的数据集（例如两个同心圆）。训练逻辑回归并观察其失败。然后添加多项式特征（x1^2, x2^2, x1*x2）重新训练。展示准确率的提升。
2. 为 3 类 Softmax 模型实现多分类混淆矩阵。计算每个类别的精确率和召回率。哪个类别最难分类？
3. 从零构建 ROC 曲线。对于 0 到 1 之间的 100 个阈值，计算真正例率和假正例率。用梯形法则计算 AUC（曲线下面积）。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 逻辑回归 (Logistic Regression) | "用于分类的回归" | 线性模型后接 Sigmoid 函数，输出类别概率 |
| Sigmoid 函数 | "S 形曲线" | 函数 1/(1+e^(-z))，将任意实数映射到 (0,1) 范围 |
| 二元交叉熵 (Binary Cross-Entropy) | "对数损失" | 损失函数 -[y*log(p) + (1-y)*log(1-p)]，严重惩罚高置信度的错误预测 |
| 决策边界 (Decision Boundary) | "分界线" | 模型输出概率等于 0.5 的曲面，分隔预测类别 |
| Softmax | "多分类 Sigmoid" | 将得分向量转换为总和为 1 的概率的函数 |
| 精确率 (Precision) | "选出的有多少相关" | TP / (TP + FP)，正预测中实际为正的比例 |
| 召回率 (Recall) | "相关的有多少被选出" | TP / (TP + FN)，模型正确识别的实际正例比例 |
| F1 分数 | "平衡准确率" | 精确率和召回率的调和平均：2*P*R / (P+R) |
| 混淆矩阵 (Confusion Matrix) | "错误分解表" | 显示每对类别的 TP、TN、FP、FN 计数的表格 |
| 阈值 (Threshold) | "截断值" | 模型预测类别 1 的概率上限（默认 0.5，可调） |
| 独热编码 (One-Hot Encoding) | "类别的二进制列" | 将类别 k 表示为在位置 k 处为 1、其余为 0 的向量 |
| 分类交叉熵 (Categorical Cross-Entropy) | "多分类对数损失" | 二元交叉熵在 k 个类别上的推广，使用独热编码标签 |

## 延伸阅读

- [Ng & Jordan: On Discriminative vs. Generative Classifiers (2002)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf) - 逻辑回归与朴素贝叶斯的比较
- [scikit-learn Logistic Regression 文档](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) - 实用指南及正则化选项
- [Hosmer & Lemeshow: Applied Logistic Regression](https://www.wiley.com/en-us/Applied+Logistic+Regression%2C+3rd+Edition-p-9780470582473) - 逻辑回归的经典教材
