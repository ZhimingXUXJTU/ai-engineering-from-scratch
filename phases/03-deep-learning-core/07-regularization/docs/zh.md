# 正则化

> 训练集 99% 但测试集只有 60%——它是在"背诵"而不是"学习"。正则化是对复杂度征收的税，强迫模型泛化。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.06 课（优化器）
**预计时间：** ~75 分钟

## 学习目标

- 从零实现带 inverted scaling 的 dropout、L2 权重衰减、批归一化、层归一化和 RMSNorm
- 测量训练-测试准确率差距，使用正则化实验诊断过拟合
- 解释为什么 Transformer 用 LayerNorm 而不是 BatchNorm，为什么现代 LLM 更偏好 RMSNorm
- 根据过拟合严重程度应用正确的正则化技术组合

## 问题引入

参数足够的神经网络可以记住任何数据集。Zhang 等人（2017）在完全随机标签的 ImageNet 上训练标准网络，达到了接近零的训练损失。训练损失完美，测试准确率为零。

GPT-3 有 1750 亿参数、5000 亿 token——没有正则化，它只会背诵训练数据。每个正则化手段从不同角度攻击过拟合：Dropout 强制冗余表示、权重衰减限制参数幅度、归一化平滑损失曲面。

## 核心概念

### 随机丢弃（Dropout）

训练时以概率 p 随机将每个神经元的输出设为零。网络必须学习冗余表示，因为它无法预测哪些神经元可用。集成解释：N 个神经元的 dropout 网络创建了 2^N 个可能的子网络，训练近似等于同时训练所有这些子网络。

默认比率：Transformer p=0.1，MLP p=0.5，CNN p=0.2-0.3。

### 权重衰减（L2 正则化）

将所有权重的平方幅度加到损失中。梯度为 lambda * w，每步将权重向零缩小。大权重被惩罚更多。

### 批归一化（BatchNorm）

在传递给下一层之前，对小批量数据归一化每层的输出。训练时用批量统计量，推理时用运行平均。根本局限：依赖批量统计量。batch_size=1 时均值方差无意义。

### 层归一化（LayerNorm）

按特征归一化而非按批量。每个样本独立归一化——不依赖批量大小。这就是 Transformer 用 LayerNorm 的原因。

### RMSNorm

LayerNorm 不减均值。省略均值计算节省约 10%。LLaMA、LLaMA 2、LLaMA 3、Mistral 和大多数现代 LLM 使用 RMSNorm。

## 动手实现

### Dropout（训练/评估模式）

```python
class Dropout:
    def __init__(self, p=0.5):
        self.p = p
        self.training = True
        self.mask = None

    def forward(self, x):
        if not self.training:
            return list(x)
        self.mask = []
        output = []
        for val in x:
            if random.random() < self.p:
                self.mask.append(0)
                output.append(0.0)
            else:
                self.mask.append(1)
                output.append(val / (1 - self.p))  # inverted scaling
        return output
```

### 层归一化

```python
class LayerNorm:
    def __init__(self, num_features, eps=1e-5):
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.eps = eps

    def forward(self, x):
        mean = sum(x) / len(x)
        var = sum((xi - mean) ** 2 for xi in x) / len(x)
        return [self.gamma[j] * (x[j] - mean) / math.sqrt(var + self.eps) + self.beta[j]
                for j in range(len(x))]
```

### RMSNorm

```python
class RMSNorm:
    def __init__(self, num_features, eps=1e-6):
        self.gamma = [1.0] * num_features
        self.eps = eps

    def forward(self, x):
        rms = math.sqrt(sum(xi * xi for xi in x) / len(x) + self.eps)
        return [self.gamma[j] * x[j] / rms for j in range(len(x))]
```

## 用框架实现

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 10),
)

model.train()
out_train = model(torch.randn(32, 784))

model.eval()
out_test = model(torch.randn(1, 784))
```

`model.train()` / `model.eval()` 切换是关键。忘记 `model.eval()` 是最常见的深度学习 bug 之一。

## 练习题

1. 实现空间 dropout：丢弃整个特征通道而非单个神经元。对比标准 dropout 的训练-测试差距。
2. 组合标签平滑和 dropout，对比四种配置（两者都不用、只用 dropout、只用标签平滑、两者都用）。
3. 在隐藏层和激活之间添加 BatchNorm，分别用学习率 0.01、0.05、0.1 训练。BatchNorm 应该允许更高学习率。
4. 实现早停法：追踪测试损失，保存最佳权重，20 轮无改善则停止。
5. 对比 LayerNorm vs RMSNorm 在 4 层网络上的表现。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 过拟合 (Overfitting) | "模型背诵了数据" | 训练性能远超测试性能，说明学了噪声而非信号 |
| 正则化 (Regularization) | "防止过拟合" | 约束模型复杂度以改善泛化的技术：dropout、权重衰减、归一化 |
| Dropout | "随机删神经元" | 训练时以概率 p 将随机神经元置零，等价于训练集成 |
| 权重衰减 (Weight decay) | "L2 惩罚" | 每步将权重向零缩小，惩罚大权重 |
| 批归一化 (Batch normalization) | "按批归一化" | 用批量统计量在批量维度上归一化 |
| 层归一化 (Layer normalization) | "按样本归一化" | 在特征维度上归一化每个样本；不依赖批量大小 |
| RMSNorm | "LayerNorm 不减均值" | 省略均值计算，快 10%，精度相同 |
| 早停法 (Early stopping) | "过拟合前停止" | 验证损失不再改善时停止训练 |

## 延伸阅读

- Srivastava et al., "Dropout" (2014) —— Dropout 原始论文
- Ioffe & Szegedy, "Batch Normalization" (2015) —— 引入 BatchNorm
- Zhang & Sennrich, "Root Mean Square Layer Normalization" (2019) —— 提出 RMSNorm
