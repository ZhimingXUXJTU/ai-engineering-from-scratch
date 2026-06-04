# 激活函数

> 没有非线性激活函数，100 层网络等价于一个矩阵乘法。激活函数是让神经网络能"弯曲思考"的门。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.03 课（反向传播）
**预计时间：** ~75 分钟

## 学习目标

- 从零实现 sigmoid、tanh、ReLU、Leaky ReLU、GELU、Swish 和 softmax 及其导数
- 通过测量 10+ 层不同激活函数的激活幅度，诊断梯度消失问题
- 检测 ReLU 网络中的死亡神经元，解释为什么 GELU 能避免这种失败
- 为给定架构（Transformer、CNN、RNN、输出层）选择正确的激活函数

## 问题引入

堆叠两个线性变换：y = W2(W1x + b1) + b2。展开：y = W2W1x + W2b1 + b2。这就是 y = Ax + c——一个单独的线性变换。不管你叠多少个线性层，结果都会坍缩为一个矩阵乘法。你的 100 层网络和单层网络有相同的表达能力。

这不是理论推想。它意味着深度线性网络完全无法学习 XOR、无法分类螺旋数据集、无法识别人脸。没有激活函数，深度就是一种错觉。

激活函数打破线性。它们通过非线性函数扭曲每层的输出，赋予网络弯曲决策边界、逼近任意函数和真正学习的能力。但选错激活函数，你的梯度会消失到零（深度网络中的 sigmoid）、爆炸到无穷（无界激活函数没有仔细初始化时），或者你的神经元会永久死亡（ReLU 配合大负偏置时）。激活函数的选择直接决定你的网络是否能学习。

## 核心概念

### 为什么必须要有非线性

矩阵乘法是可组合的。向量先乘矩阵 A 再乘矩阵 B，等价于乘以 AB。这意味着堆叠十个线性层在数学上等价于一个带大矩阵的线性层。所有那些参数，所有那些深度——都浪费了。你需要一些东西打破这条链。这就是激活函数的作用。

数学证明：线性层计算 f(x) = Wx + b。堆叠两层：

```
第 1 层: h = W1 * x + b1
第 2 层: y = W2 * h + b2
```

代入：

```
y = W2 * (W1 * x + b1) + b2
y = (W2 * W1) * x + (W2 * b1 + b2)
y = A * x + c                     # 合并为单一矩阵——深度消失了！
```

一层。在层间插入非线性激活 g()：

```
h = g(W1 * x + b1)               # 加入非线性激活
y = W2 * h + b2
```

现在代入不再成立。W2 * g(W1 * x + b1) + b2 无法简化为单一线性变换。网络可以表示非线性函数。每增加一个带激活的层，表达能力就真正增加。

### Sigmoid

神经网络最初的激活函数。

```
sigmoid(x) = 1 / (1 + e^(-x))
```

输出范围：(0, 1)。平滑、可导，将任何实数映射为类似概率的值。

导数：

```
sigmoid'(x) = sigmoid(x) * (1 - sigmoid(x))
```

这个导数的最大值是 0.25，在 x = 0 时达到。在反向传播中，梯度逐层相乘。十层 sigmoid 意味着梯度最多乘以 0.25 十次：

```
0.25^10 = 0.000000953674     # 不到原始信号的百万分之一
```

这就是梯度消失问题。前面几层的梯度变得极小，权重几乎不更新。网络看起来在学习——后面几层的损失在下降——但前面几层是冻住的。深度 sigmoid 网络根本无法训练。

额外问题：sigmoid 输出总是正数（0 到 1），意味着权重梯度总是同号。这导致梯度下降呈锯齿形路径。

### Tanh

Sigmoid 的零中心版本。

```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```

输出范围：(-1, 1)。零中心化，消除了锯齿形问题。

导数：

```
tanh'(x) = 1 - tanh(x)^2
```

最大导数为 1.0（在 x = 0 时）——比 sigmoid 好 4 倍。但梯度消失问题仍然存在。对于大正或大负输入，导数趋近于零。

### ReLU：深度学习的突破

修正线性单元（Rectified Linear Unit）。Nair 和 Hinton 在 2010 年推广用于深度学习，它改变了一切。

```
relu(x) = max(0, x)
```

输出范围：[0, infinity)。导数极其简单：

```
relu'(x) = 1  if x > 0
           0  if x <= 0
```

正输入没有梯度消失。梯度恰好是 1，直接通过。这就是深度网络变得可训练的原因——ReLU 在层间保持梯度幅度。

但有一个失败模式：死亡神经元问题。如果一个神经元的加权输入始终为负（由于大负偏置或不幸运的权重初始化），它的输出始终为零，梯度始终为零，永远不会更新。它永久死亡。实践中，ReLU 网络中 10-40% 的神经元可能在训练中死亡。

### Leaky ReLU

修复死亡神经元的最简单方法。

```
leaky_relu(x) = x        if x > 0
                alpha * x if x <= 0
```

alpha 是一个小常数，通常 0.01。负区间有小的斜率而非零，所以死亡神经元仍能收到梯度信号并可能恢复。

### GELU：现代默认选择

高斯误差线性单元（Gaussian Error Linear Unit）。Hendrycks 和 Gimpel 在 2016 年引入。BERT、GPT 和大多数现代 Transformer 的默认激活函数。

```
gelu(x) = x * Phi(x)
```

其中 Phi(x) 是标准正态分布的累积分布函数。实际使用的近似公式：

```
gelu(x) ~= 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
```

GELU 处处平滑，允许小的负值（不像 ReLU 硬截断为零），具有概率解释：按输入为正的概率对每个输入加权。这种平滑门控在 Transformer 架构中优于 ReLU，因为它提供更好的梯度流且完全避免死亡神经元问题。

### Swish / SiLU

Ramachandran 等人 2017 年通过自动搜索发现的自门控激活函数。

```
swish(x) = x * sigmoid(x)
```

像 GELU 一样，它平滑、非单调，允许小的负值。细微区别：Swish 用 sigmoid 门控而 GELU 用高斯 CDF 门控。实践中性能几乎相同。Swish 用于 EfficientNet 和一些视觉模型。GELU 统治语言模型。

### Softmax：输出层激活函数

不用于隐藏层。Softmax 将原始分数向量（logits）转换为概率分布。

```
softmax(x_i) = e^(x_i) / sum(e^(x_j) for all j)
```

每个输出在 0 和 1 之间。所有输出之和为 1。这使它成为多分类分类的标准最终激活。最大 logit 获得最高概率，但与 argmax 不同，softmax 可导且保留了相对置信度信息。

### 什么时候用什么激活函数

经验法则：Transformer/NLP 用 GELU，CNN/视觉用 ReLU，RNN/LSTM 用 tanh。输出层：二分类用 sigmoid，多分类用 softmax，回归不用激活。

## 动手实现

### 第一步：实现所有激活函数及导数

```python
import math

def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)  # 最大值 0.25

def tanh_act(x):
    return math.tanh(x)

def tanh_derivative(x):
    t = math.tanh(x)
    return 1 - t * t  # 最大值 1.0

def relu(x):
    return max(0.0, x)

def relu_derivative(x):
    return 1.0 if x > 0 else 0.0

def leaky_relu(x, alpha=0.01):
    return x if x > 0 else alpha * x

def leaky_relu_derivative(x, alpha=0.01):
    return 1.0 if x > 0 else alpha

def gelu(x):
    return 0.5 * x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x ** 3)))

def gelu_derivative(x):
    phi = 0.5 * (1 + math.erf(x / math.sqrt(2)))
    pdf = math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    return phi + x * pdf

def swish(x):
    return x * sigmoid(x)

def swish_derivative(x):
    s = sigmoid(x)
    return s + x * s * (1 - s)

def softmax(xs):
    max_x = max(xs)
    exps = [math.exp(x - max_x) for x in xs]
    total = sum(exps)
    return [e / total for e in exps]
```

### 第二步：可视化梯度死亡区域

```python
def gradient_scan(name, derivative_fn, start=-5, end=5, n=100):
    step = (end - start) / n
    near_zero = 0
    healthy = 0
    for i in range(n):
        x = start + i * step
        g = derivative_fn(x)
        if abs(g) < 0.01:
            near_zero += 1
        else:
            healthy += 1
    pct_dead = near_zero / n * 100
    print(f"{name:15s}: {healthy:3d} 健康, {near_zero:3d} 接近零 ({pct_dead:.0f}% 死亡区域)")
```

### 第三步：梯度消失实验

前向传播信号通过 N 层，使用 sigmoid vs ReLU。测量激活幅度如何变化。

### 第四步：死亡神经元检测器

创建一个 ReLU 网络，传入随机输入，统计有多少神经元从不激活。

### 第五步：训练对比——Sigmoid vs ReLU vs GELU

用三种不同激活函数在圆形数据集上训练相同的两层网络。对比收敛速度。

## 用框架实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

x = torch.randn(4, 10)  # 4 个样本，每个 10 维

relu_out = F.relu(x)           # ReLU
gelu_out = F.gelu(x)           # GELU
sigmoid_out = torch.sigmoid(x)  # Sigmoid
swish_out = F.silu(x)          # Swish/SiLU

logits = torch.randn(4, 5)     # 4 个样本，5 个类别
probs = F.softmax(logits, dim=1)  # Softmax

model = nn.Sequential(
    nn.Linear(10, 64),
    nn.GELU(),          # Transformer 标配：GELU
    nn.Linear(64, 32),
    nn.GELU(),
    nn.Linear(32, 5),   # 输出层：不加激活（logits）
)
```

隐藏层在 Transformer 中用 GELU。隐藏层在 CNN 中用 ReLU。输出层分类用 softmax。输出层回归不用激活。输出层概率用 sigmoid。如果 ReLU 神经元死亡，换 GELU。

## 产出物

本课产出：
- `outputs/prompt-activation-selector.md` -- 帮助你为任何架构选择正确激活函数的可复用提示词

## 练习题

1. 实现 PReLU（负斜率 alpha 可学习），在圆形数据上训练并与 Leaky ReLU 对比。

2. 把梯度消失实验扩展到 50 层。哪个激活函数的信号最先归零？

3. 实现 ELU，在相同网络上对比 ELU 和 ReLU 的死亡神经元率。

4. 构建"梯度健康监控器"——每轮计算各层平均梯度大小，低于 0.001 或超过 100 时报警。

5. 用 XOR 数据集替代圆形数据做对比。哪个激活函数收敛最快？为什么和圆形结果不同？

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 激活函数 (Activation function) | "非线性那部分" | 施加在每个神经元输出上的函数，打破线性，使网络能学习非线性映射 |
| 梯度消失 (Vanishing gradient) | "深层梯度消失" | 导数小于 1 的激活函数导致梯度逐层指数缩小，前面的层无法训练 |
| 梯度爆炸 (Exploding gradient) | "梯度爆炸" | 有效乘数超过 1 时梯度逐层指数增长，训练不稳定 |
| 死亡神经元 (Dead neuron) | "停止学习的神经元" | ReLU 神经元输入永远为负，输出和梯度永远为零 |
| Sigmoid | "压到 0-1" | 逻辑函数 1/(1+e^-x)，历史重要但深层网络中梯度消失 |
| ReLU | "负数变零" | max(0, x)——通过保持梯度幅度让深度学习变得可行的激活函数 |
| GELU | "Transformer 激活" | 高斯误差线性单元，按输入为正的概率加权的平滑激活 |
| Swish/SiLU | "自门控 ReLU" | x * sigmoid(x)，通过自动搜索发现，用于 EfficientNet |
| Softmax | "分数变概率" | 把 logits 归一化为概率分布，所有值在 (0,1) 且和为 1 |
| Leaky ReLU | "不会死的 ReLU" | max(alpha*x, x)，负区间保留小梯度防止神经元死亡 |
| 饱和 (Saturation) | "sigmoid 的平坦区" | 激活函数导数趋近于零的区域，阻断梯度流 |
| Logit | "softmax 前的原始分" | 最终层未归一化的输出 |

## 延伸阅读

- Nair & Hinton, "Rectified Linear Units Improve Restricted Boltzmann Machines" (2010) —— 引入 ReLU 并使深度网络训练成为可能的论文
- Hendrycks & Gimpel, "Gaussian Error Linear Units (GELUs)" (2016) —— 引入 Transformer 默认激活函数的论文
- Ramachandran et al., "Searching for Activation Functions" (2017) —— 通过自动搜索发现 Swish
- Glorot & Bengio, "Understanding the difficulty of training deep feedforward neural networks" (2010) —— 诊断梯度消失/爆炸并提出 Xavier 初始化的论文
