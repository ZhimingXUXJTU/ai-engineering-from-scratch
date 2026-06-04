# 损失函数

> 网络做出预测，真实标签说不是。到底错多少？那个数字就是损失。选错损失函数，模型优化的就是完全错误的东西。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.04 课（激活函数）
**预计时间：** ~75 分钟

## 学习目标

- 从零实现 MSE、二元交叉熵、多类交叉熵和对比损失（InfoNCE）及其梯度
- 通过演示"全部预测 0.5"的失败模式，解释为什么分类任务不能用 MSE
- 应用标签平滑到交叉熵，描述它如何防止过度自信的预测
- 为回归、二分类、多分类和嵌入学习任务选择正确的损失函数

## 问题引入

用 MSE 做分类的模型会自信地对所有输入预测 0.5。它在最小化损失。它也毫无用处。

损失函数是模型唯一优化的目标。不是准确率。不是 F1 分数。不是你报告给经理的任何指标。优化器取损失函数的梯度并调整权重来使那个数字更小。如果损失函数没有捕捉你在意的东西，模型会找到数学上最省事的方式来满足它，那个方式几乎从来不是你想要的。

MSE 做分类时，模型发现预测 0.5 是最安全的策略——损失最低但毫无区分能力。交叉熵则通过 -log(p) 惩罚不自信的预测：-log(0.5)=0.693（很差）vs -log(0.99)=0.01（很好），迫使模型做出明确判断。

在自监督学习中，对比损失定义了全部学习信号——搞错了会导致所有嵌入坍缩到同一点。

## 核心概念

### 均方误差（MSE）

回归任务的默认损失。计算预测和目标的平方差，取所有样本的平均。

```
MSE = (1/n) * sum((y_pred - y_true)^2)
```

为什么平方很重要：它对大误差施加二次惩罚。误差 2 的代价是误差 1 的 4 倍。误差 10 的代价是 100 倍。这让 MSE 对异常值敏感。

梯度与误差成线性关系——对回归是好事（大误差需要大修正），对分类是坏事（应该对"自信的错误"指数级惩罚）。

### 交叉熵损失

分类任务的损失函数。基于信息论——衡量预测概率分布和真实分布之间的差异。

**二元交叉熵（BCE）：**

```
BCE = -(y * log(p) + (1 - y) * log(1 - p))
```

核心是 -log(p)：预测正确且自信（p=0.99）时损失只有 0.01，预测错误且自信（p=0.01）时损失高达 4.6——460 倍的差距！梯度在预测错误时趋近无穷大，给模型强烈的修正信号。

GPT 的训练损失就是交叉熵——预测下一个 token 的交叉熵。

### 为什么 MSE 不适合分类

MSE 的梯度在预测接近 0 或 1 时变平（因为 sigmoid 饱和），导致修正缓慢。交叉熵的 -log 正好抵消 sigmoid 的平坦区域，在最需要修正的地方提供最强梯度。

### 标签平滑

把硬标签 [0, 0, 1, 0, ...] 变成软标签 [0.01, 0.01, 0.91, 0.01, ...]。因为要让 softmax 输出 1.0 需要 logit 趋近无穷大，这会导致过拟合和过度自信。GPT 和大多数现代模型都用标签平滑。

### 对比损失

不需要标签！取一张图片的两个增强版本作为"正对"，其他图片作为"负对"。损失 = -log(正对相似度 / 所有可能对的相似度之和)。温度 tau 越低，区分越严格。

### Focal Loss

为类别不平衡设计。简单样本权重只有 0.01，困难样本权重 0.81。这让模型专注于困难案例。

## 动手实现

### 第一步：MSE 及其梯度

```python
def mse(predictions, targets):
    n = len(predictions)
    total = 0.0
    for p, t in zip(predictions, targets):
        total += (p - t) ** 2
    return total / n

def mse_gradient(predictions, targets):
    n = len(predictions)
    return [2.0 * (p - t) / n for p, t in zip(predictions, targets)]
```

### 第二步：二元交叉熵

```python
import math

def binary_cross_entropy(predictions, targets, eps=1e-15):
    n = len(predictions)
    total = 0.0
    for p, t in zip(predictions, targets):
        p_clipped = max(eps, min(1 - eps, p))
        total += -(t * math.log(p_clipped) + (1 - t) * math.log(1 - p_clipped))
    return total / n
```

### 第三步：带 softmax 的多类交叉熵

```python
def softmax(logits):
    max_val = max(logits)
    exps = [math.exp(x - max_val) for x in logits]
    total = sum(exps)
    return [e / total for e in exps]

def categorical_cross_entropy(logits, target_index, eps=1e-15):
    probs = softmax(logits)
    p = max(eps, probs[target_index])
    return -math.log(p)
```

Softmax + 交叉熵的梯度简化为：预测概率减去 one-hot 目标。这个优雅的简化就是为什么 softmax 和交叉熵总是配对使用。

## 用框架实现

```python
import torch
import torch.nn.functional as F

predictions = torch.tensor([0.9, 0.1, 0.7], requires_grad=True)
targets = torch.tensor([1.0, 0.0, 1.0])

mse_loss = F.mse_loss(predictions, targets)              # MSE：回归
bce_loss = F.binary_cross_entropy(predictions, targets)   # BCE：二分类

logits = torch.randn(4, 10)                              # 4 个样本，10 类
labels = torch.tensor([3, 7, 1, 9])
ce_loss = F.cross_entropy(logits, labels)                # CCE：多分类
ce_smooth = F.cross_entropy(logits, labels, label_smoothing=0.1)  # 带标签平滑
```

直接用 `F.cross_entropy(logits, labels)`——它内部合并了 log-softmax 和 NLL，数值最稳定。

## 练习题

1. 实现 Huber 损失（小误差用 MSE，大误差用 MAE），在有异常值的数据上对比 MSE 和 Huber。

2. 在 90:10 的不平衡数据集上对比 BCE 和 Focal Loss（gamma=2）的少数类召回率。

3. 实现带半困难负样本挖掘的三元组损失，对比随机选择负样本的收敛速度。

4. 追踪 MSE 和交叉熵训练中各层梯度大小，验证交叉熵在早期产生更大梯度。

5. 实现 KL 散度损失，验证在 one-hot 真实分布时与交叉熵梯度相同，然后尝试知识蒸馏中的软目标。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 损失函数 (Loss function) | "模型错多少" | 把预测和目标映射为标量的可导函数，优化器最小化这个值 |
| MSE | "平方误差平均" | 预测与目标的平方差的均值；对大误差二次惩罚 |
| 交叉熵 (Cross-entropy) | "分类损失" | 用 -log(p) 衡量预测分布和真实分布的差异 |
| 标签平滑 (Label smoothing) | "软化目标" | 把硬标签换成软值，防止过度自信 |
| 对比损失 (Contrastive loss) | "拉近推远" | 让相似样本嵌入接近、不同样本嵌入远离 |
| InfoNCE | "CLIP/SimCLR 损失" | 温度缩放的相似度交叉熵 |
| Focal Loss | "不平衡数据修复" | 降低简单样本权重，聚焦困难样本 |
| 温度 (Temperature) | "尖锐度旋钮" | logits 的除数，控制分布尖锐程度 |

## 延伸阅读

- Lin et al., "Focal Loss for Dense Object Detection" (2017) —— 引入 Focal Loss
- Chen et al., "A Simple Framework for Contrastive Learning of Visual Representations" (SimCLR, 2020)
- Szegedy et al., "Rethinking the Inception Architecture" (2016) —— 引入标签平滑
