# 权重初始化与训练稳定性

> 初始化错了，训练永远不会开始。初始化对了，50 层训练和 3 层一样平滑。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.04 课（激活函数）、第 03.07 课（正则化）
**预计时间：** ~90 分钟

## 学习目标

- 实现零初始化、随机初始化、Xavier/Glorot 和 Kaiming/He 初始化策略，测量它们在 50 层网络中对激活幅度的影响
- 推导为什么 Xavier 用 Var(w) = 2/(fan_in + fan_out) 而 Kaiming 用 Var(w) = 2/fan_in
- 演示零初始化的对称性问题，解释为什么仅靠随机缩放不够
- 将正确的初始化策略与激活函数匹配：sigmoid/tanh 用 Xavier，ReLU/GELU 用 Kaiming

## 问题引入

初始化是深度学习中最被低估的决策。架构写论文，优化器写博客，初始化只是脚注。但搞错了，其他都不重要——你的网络在训练开始前就已经死了。

零初始化导致所有神经元相同。随机初始化方差不对会导致 50 层网络信号消失或爆炸。Xavier 和 Kaiming 初始化通过数学推导解决了这个问题。

## 核心概念

### 对称性问题

同一层的每个神经元结构相同。如果所有权重从相同值开始（零是极端情况），每个神经元计算相同输出，接收相同梯度，做相同更新。你付了 512 个参数的钱，却只得到 1 个。

### 方差逐层传播

```
Var(z) = fan_in * Var(w) * Var(x)
```

如果 Var(w) = 1 且 fan_in = 512，输出方差是输入的 512 倍。10 层后：512^10 = 1.2e27，信号爆炸。

目标：选择 Var(w) 使 Var(z) = Var(x)。信号幅度在层间保持恒定。

### Xavier/Glorot 初始化

sigmoid 和 tanh 的解决方案：

```
Var(w) = 2 / (fan_in + fan_out)
```

### Kaiming/He 初始化

ReLU 将一半输出归零。有效 fan_in 减半。He 等人（2015）调整了公式：

```
Var(w) = 2 / fan_in
```

因子 2 补偿 ReLU 将一半激活归零。50 层后，Kaiming 保持信号稳定。

PyTorch 的 nn.Linear 默认使用 Kaiming Uniform 初始化——这就是为什么大多数网络"开箱即用"。

### Transformer 初始化

GPT-2 引入了残差缩放：将残差连接的权重乘以 1/sqrt(2N)，N 是层数。Llama 3（126 层）使用类似方案。

## 动手实现

### 初始化策略

```python
import math
import random

def zero_init(fan_in, fan_out):
    return [[0.0 for _ in range(fan_in)] for _ in range(fan_out)]

def random_init(fan_in, fan_out, scale=1.0):
    return [[random.gauss(0, scale) for _ in range(fan_in)] for _ in range(fan_out)]

def xavier_init(fan_in, fan_out):
    std = math.sqrt(2.0 / (fan_in + fan_out))
    return [[random.gauss(0, std) for _ in range(fan_in)] for _ in range(fan_out)]

def kaiming_init(fan_in, fan_out):
    std = math.sqrt(2.0 / fan_in)
    return [[random.gauss(0, std) for _ in range(fan_in)] for _ in range(fan_out)]
```

### 50 层实验

让信号通过 50 层网络，测量每层激活幅度：零初始化 → 所有神经元相同；随机 N(0,1) → 爆炸；随机 N(0,0.01) → 消失；Xavier+tanh / Kaiming+ReLU → 稳定。

## 用框架实现

```python
import torch.nn as nn

layer = nn.Linear(512, 256)
nn.init.xavier_uniform_(layer.weight)       # Xavier 均匀
nn.init.kaiming_normal_(layer.weight, nonlinearity='relu')  # Kaiming 正态
```

## 练习题

1. 添加 LeCun 初始化（Var = 1/fan_in），和 Xavier + tanh 对比。
2. 实现 GPT-2 残差缩放，对比有/无缩放时残差幅度增长速度。
3. 创建"初始化健康检查"函数，根据层维度和激活类型推荐正确的初始化。
4. 对比 fan_in=16 vs fan_in=1024 时各初始化的效果。
5. 实现正交初始化，和 Kaiming 在 50 层 ReLU 网络上对比。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 权重初始化 (Weight initialization) | "随机设初始权重" | 决定网络能否训练的初始权重选择策略 |
| 对称性打破 (Symmetry breaking) | "让神经元不同" | 随机初始化确保神经元学习不同特征 |
| Xavier/Glorot 初始化 | "sigmoid 初始化" | Var(w) = 2/(fan_in + fan_out)，为 sigmoid/tanh 设计 |
| Kaiming/He 初始化 | "ReLU 初始化" | Var(w) = 2/fan_in，补偿 ReLU 归零一半激活 |
| 残差缩放 (Residual scaling) | "GPT-2 初始化技巧" | 1/sqrt(2N) 缩放防止 N 层 Transformer 方差增长 |

## 延伸阅读

- Glorot & Bengio, "Understanding the difficulty of training deep feedforward neural networks" (2010) —— Xavier 初始化原始论文
- He et al., "Delving Deep into Rectifiers" (2015) —— Kaiming 初始化
- Radford et al., "Language Models are Unsupervised Multitask Learners" (2019) —— GPT-2 残差缩放
