# 优化器

> 梯度下降告诉你方向，但不说步幅和速度。SGD 像指南针——只知道方向。Adam 像带实时路况的 GPS——根据历史信息调整策略。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.05 课（损失函数）
**预计时间：** ~75 分钟

## 学习目标

- 从零用 Python 实现 SGD、带动量的 SGD、Adam 和 AdamW 优化器
- 解释 Adam 的偏差修正如何补偿初始训练步中零初始化的矩估计
- 演示为什么 AdamW 在相同任务上比 Adam + L2 正则化产生更好的泛化
- 为 Transformer、CNN、GAN 和微调选择合适的优化器和默认超参数

## 问题引入

原始 SGD 有三个问题：振荡（在窄谷中来回跳动）、单一学习率（不适合所有参数）、无法穿越平坦区域（梯度接近零就卡住）。Adam 同时解决这三个问题：动量抑制振荡、自适应学习率适合不同参数、偏差修正加速初期收敛。

## 核心概念

### 随机梯度下降（SGD）

最简单的优化器。在小批量数据上计算梯度，向相反方向走一步。

```
w = w - lr * gradient
```

"随机"意味着你用数据的随机子集（小批量）来估计梯度。学习率是唯一的旋钮。太高：损失发散。太低：训练极慢。

### 动量（Momentum）

球滚下山的类比。维护一个速度，累积过去的梯度：

```
m_t = beta * m_{t-1} + gradient    # 速度 = 衰减 × 历史速度 + 当前梯度
w = w - lr * m_t                    # 沿速度方向更新
```

Beta（通常 0.9）控制保留多少历史。为什么这能修复振荡：方向一致的梯度累积，方向翻转的梯度抵消。在窄谷中，"横向"分量每步翻转被抑制，"纵向"分量保持一致被放大。

### Adam：动量 + 自适应学习率

Adam 维护两个指数移动平均：

```
m_t = beta1 * m_{t-1} + (1 - beta1) * gradient        （一阶矩：均值）
v_t = beta2 * v_{t-1} + (1 - beta2) * gradient^2       （二阶矩：方差）
```

**偏差修正**是关键细节。第 1 步时 m_1 = (1 - beta1) * gradient。beta1 = 0.9 时，只有 0.1 * gradient——小了十倍。偏差修正确保初始步正确：

```
m_hat = m_t / (1 - beta1^t)
v_hat = v_t / (1 - beta2^t)
```

更新：`w = w - lr * m_hat / (sqrt(v_hat) + epsilon)`

Adam 默认值：lr = 0.001, beta1 = 0.9, beta2 = 0.999, epsilon = 1e-8。这些默认值在 80% 的问题上有效。

### AdamW：正确的权重衰减

L2 正则化在 SGD 中等价于权重衰减，但在 Adam 中不等价。AdamW 将权重衰减直接应用于参数，不经过 Adam 的自适应缩放。BERT、GPT、Llama、Stable Diffusion 都用 AdamW 训练。

## 动手实现

### 第一步：原始 SGD

```python
class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        for i in range(len(params)):
            params[i] -= self.lr * grads[i]
```

### 第二步：带动量的 SGD

```python
class SGDMomentum:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.velocities = None

    def step(self, params, grads):
        if self.velocities is None:
            self.velocities = [0.0] * len(params)
        for i in range(len(params)):
            self.velocities[i] = self.beta * self.velocities[i] + grads[i]
            params[i] -= self.lr * self.velocities[i]
```

### 第三步：Adam

```python
import math

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)
        self.t += 1
        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
```

### 第四步：AdamW

```python
class AdamW:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.weight_decay = weight_decay
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)
        self.t += 1
        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
            params[i] -= self.lr * self.weight_decay * params[i]  # 解耦权重衰减
```

## 用框架实现

```python
import torch
import torch.optim as optim

model = torch.nn.Sequential(
    torch.nn.Linear(784, 256),
    torch.nn.ReLU(),
    torch.nn.Linear(256, 10),
)

optimizer = optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

for epoch in range(100):
    optimizer.zero_grad()
    output = model(torch.randn(32, 784))
    loss = torch.nn.functional.cross_entropy(output, torch.randint(0, 10, (32,)))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    scheduler.step()
```

训练循环模式：zero_grad → forward → loss → backward → clip → step → schedule。CNN 用 SGD+Momentum（lr=0.1），Transformer 用 AdamW（lr=1e-4）。

## 练习题

1. 实现 Nesterov 动量（在"前瞻"位置计算梯度），对比标准动量的收敛速度。
2. 实现 warmup + cosine decay 调度，对比有/无 warmup 达到 90% 准确率的轮数。
3. 追踪 Adam 训练中各参数的有效学习率，观察不同参数的更新速度差异。
4. 实现梯度裁剪，统计有/无裁剪时高学习率下训练发散的比例。
5. 在大初始权重下对比 Adam 和 AdamW，观察权重衰减效果差异。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 学习率 (Learning rate) | "步长" | 梯度更新的标量乘数；训练中影响最大的超参数 |
| SGD | "基础梯度下降" | 随机梯度下降：用小批量梯度更新 |
| 动量 (Momentum) | "滚球的类比" | 历史梯度的指数移动平均；抑制振荡、加速一致方向 |
| Adam | "默认优化器" | 动量 + RMSProp + 偏差修正的统一优化器 |
| AdamW | "正确的 Adam" | Adam + 解耦权重衰减 |
| 偏差修正 (Bias correction) | "运行平均的热身" | 补偿 Adam 矩估计的零初始化偏差 |
| 权重衰减 (Weight decay) | "缩小权重" | 每步减去权重的一小部分；惩罚大权重 |
| 梯度裁剪 (Gradient clipping) | "限制梯度范数" | 梯度范数超限时缩小梯度；防止梯度爆炸 |

## 延伸阅读

- Kingma & Ba, "Adam: A Method for Stochastic Optimization" (2014) —— Adam 原始论文
- Loshchilov & Hutter, "Decoupled Weight Decay Regularization" (2017) —— 提出 AdamW
