# Multi-Layer Networks and Forward Pass | 多层网络与前向传播

> One neuron draws a line. Stack them, and you can draw anything.

> 一个神经元画一条直线。把它们叠起来，你就能画出任何形状。

> **【中文解读】** 一个神经元只能画一条直线，但把多个神经元叠成多层，就能拟合任意形状的曲线。这就是多层网络的核心价值——用层的堆叠突破单层感知机的线性限制。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 01 (Math Foundations), Lesson 03.01 (The Perceptron)
**Time:** ~90 minutes

## Learning Objectives | 学习目标

- Build a multi-layer network from scratch with Layer and Network classes that perform a complete forward pass
  从零构建带有 Layer 和 Network 类的多层网络，执行完整的前向传播
- Trace matrix dimensions through each layer of a network and identify shape mismatches
  追踪网络每层的矩阵维度，识别形状不匹配问题
- Explain how stacking nonlinear activations enables a network to learn curved decision boundaries
  解释堆叠非线性激活如何使网络能够学习弯曲的决策边界
- Solve the XOR problem using a 2-2-1 architecture with hand-tuned sigmoid weights
  使用手动调整的 sigmoid 权重，用 2-2-1 架构解决 XOR 问题

> **【中文解读】** 本章目标：从零构建 Layer 和 Network 类，理解前向传播中矩阵维度的变化，搞清楚为什么非线性激活函数让网络能学习弯曲的决策边界。

## The Problem | 问题引入

A single neuron is a line drawer. That's it. One straight line through your data. Every real problem in AI -- image recognition, language understanding, playing Go -- requires curves. Stacking neurons into layers is how you get curves.

> 单个神经元只是一个画线的工具。仅此而已。在你的数据中画一条直线。AI 中的每个真实问题——图像识别、语言理解、下围棋——都需要曲线。将神经元堆叠成层就是获得曲线的方法。

In 1969, Minsky and Papert proved this limitation was fatal: a single-layer network cannot learn XOR. Not "struggles to learn" -- mathematically cannot. The XOR truth table places [0,1] and [1,0] on one side, [0,0] and [1,1] on the other. No single line separates them.

> 1969 年，Minsky 和 Papert 证明了这个限制是致命的：单层网络无法学习 XOR。不是"很难学"——是数学上不可能。XOR 真值表将 [0,1] 和 [1,0] 放在一边，[0,0] 和 [1,1] 放在另一边。没有一条直线能把它们分开。

This killed neural network funding for over a decade. The fix was obvious in hindsight: stop using one layer. Stack neurons into layers. Let the first layer carve the input space into new features, and let the second layer combine those features into decisions no single line could make.

> 这让神经网络的资金中断了十多年。事后看来，解决方案很明显：不再只用一层。将神经元堆叠成层。让第一层将输入空间切割成新特征，让第二层将这些特征组合成任何单条直线都无法实现的决策。

That stack is the multi-layer network. It is the foundation of every deep learning model in production today. The forward pass -- data flowing from input through hidden layers to output -- is the first thing you need to build before anything else works.

> 那个堆叠就是多层网络。它是当今生产环境中每个深度学习模型的基础。前向传播——数据从输入流经隐藏层到输出——是你在其他一切工作之前需要构建的第一件事。

> **【中文解读】** 单个神经元只能画直线，但图像识别、语言理解、围棋这些真实 AI 任务都需要曲线。1969 年 Minsky 和 Papert 证明了单层网络无法学习 XOR（数学上不可能，不是"学不好"）。解法就是叠层：第一层把输入空间切成新特征，第二层把这些特征组合成更复杂的决策。这就是所有深度学习模型的基础。

## The Concept | 核心概念

### Layers: Input, Hidden, Output | 层：输入层、隐藏层、输出层

A multi-layer network has three types of layers:

> 多层网络有三种类型的层：

**Input layer** -- not really a layer. It holds your raw data. Two features means two input nodes. No computation happens here.

> **输入层**——其实不算真正的层。它存放原始数据。两个特征意味着两个输入节点。这里不进行任何计算。

**Hidden layers** -- where the work happens. Each neuron takes every output from the previous layer, applies weights and a bias, then passes the result through an activation function. "Hidden" because you never see these values directly in the training data.

> **隐藏层**——真正干活的地方。每个神经元接收前一层的所有输出，应用权重和偏置，然后将结果通过激活函数。"隐藏"是因为你在训练数据中永远看不到这些值。

**Output layer** -- the final answer. For binary classification, one neuron with sigmoid. For multi-class, one neuron per class.

> **输出层**——最终答案。二分类用一个 sigmoid 神经元，多分类用每类一个神经元。

```mermaid
graph LR
    subgraph Input["Input Layer"]
        x1["x1"]
        x2["x2"]
    end
    subgraph Hidden["Hidden Layer (3 neurons)"]
        h1["h1"]
        h2["h2"]
        h3["h3"]
    end
    subgraph Output["Output Layer"]
        y["y"]
    end
    x1 --> h1
    x1 --> h2
    x1 --> h3
    x2 --> h1
    x2 --> h2
    x2 --> h3
    h1 --> y
    h2 --> y
    h3 --> y
```

This is a 2-3-1 network. Two inputs, three hidden neurons, one output. Every connection carries a weight. Every neuron (except input) carries a bias.

> 这是一个 2-3-1 网络。两个输入，三个隐藏神经元，一个输出。每个连接都有一个权重。每个神经元（除了输入层）都有一个偏置。

Each layer produces a vector of numbers called a hidden state. For text, hidden states increase dimensionality -- encoding a word as 768 numbers to capture semantic meaning. For images, they reduce dimensionality -- compressing millions of pixels into a manageable representation. The hidden state is where the learning lives.

> 每一层产生一个数字向量，称为隐藏状态。对于文本，隐藏状态增加维度——将一个词编码为 768 个数字来捕捉语义。对于图像，它们降低维度——将数百万像素压缩为可管理的表示。学习就发生在这些隐藏状态中。

> **【中文解读】** 三种层：输入层（只是数据入口，不计算）、隐藏层（做特征变换，"隐藏"是因为训练数据里看不到这些值）、输出层（最终答案）。每一层产出一个向量叫"隐藏状态"——文本任务中它增加维度（把词变成 768 维向量来捕捉语义），图像任务中它降低维度（压缩百万像素为紧凑表示）。学习就发生在这些隐藏状态中。

> **【拓展：Transformer 中的隐藏状态】** 在 GPT/BERT 中，每一层 Transformer 的输出也是一个隐藏状态（shape: [batch, seq_len, d_model]）。这些隐藏状态逐层"理解"输入的语义——低层捕捉语法，高层捕捉语义。这也是为什么可以通过 `model(x).hidden_states[-1]` 提取特征用于下游任务。

### Neurons and Activations | 神经元与激活函数

Each neuron does three things:

> 每个神经元做三件事：

1. Multiply every input by its corresponding weight
   将每个输入乘以对应的权重
2. Sum all the products and add a bias
   将所有乘积求和并加上偏置
3. Pass the sum through an activation function
   将和通过激活函数

For now, the activation is sigmoid:

> 目前使用的激活函数是 sigmoid：

```
sigmoid(z) = 1 / (1 + e^(-z))
```

Sigmoid squashes any number into the range (0, 1). Large positive inputs push toward 1. Large negative inputs push toward 0. Zero maps to 0.5. This smooth curve is what makes learning possible -- unlike the perceptron's hard step, sigmoid has a gradient everywhere.

> Sigmoid 将任何数字压缩到 (0, 1) 范围内。大的正输入趋向 1，大的负输入趋向 0，0 映射到 0.5。这条平滑曲线使学习成为可能——与感知机的硬阶跃不同，sigmoid 处处都有梯度。

> **【中文解读】** 每个神经元做三件事：输入乘权重、求和加偏置、过激活函数。Sigmoid 把任意数字压缩到 (0, 1) 区间。关键是它处处可导——这让梯度下降成为可能。感知机的阶跃函数在 0 处不可导，所以无法用梯度下降训练。

### Forward Pass: How Data Flows | 前向传播：数据如何流动

The forward pass pushes input data through the network, layer by layer, until it reaches the output. No learning happens during the forward pass. It is pure computation: multiply, add, activate, repeat.

> 前向传播将输入数据逐层推过网络，直到到达输出。前向传播过程中不发生任何学习。它是纯粹的运算：乘、加、激活、重复。

```mermaid
graph TD
    X["Input: [x1, x2]"] --> WH["Multiply by Weight Matrix W1 (2x3)"]
    WH --> BH["Add Bias Vector b1 (3,)"]
    BH --> AH["Apply sigmoid to each element"]
    AH --> H["Hidden Output: [h1, h2, h3]"]
    H --> WO["Multiply by Weight Matrix W2 (3x1)"]
    WO --> BO["Add Bias Vector b2 (1,)"]
    BO --> AO["Apply sigmoid"]
    AO --> Y["Output: y"]
```

At each layer, three operations happen in sequence:

> 在每一层，按顺序执行三个操作：

```
z = W * input + b       (linear transformation)    # 线性变换
a = sigmoid(z)           (activation)                # 激活
```

The output of one layer becomes the input to the next. That is the entire forward pass.

> 一层的输出成为下一层的输入。这就是整个前向传播。

> **【中文解读】** 前向传播就是数据从输入流到输出的过程——没有任何学习，纯粹的计算。每一层做两件事：线性变换（Wx + b）+ 非线性激活（sigmoid）。上一层的输出就是下一层的输入。这就是 PyTorch 里 `model(x)` 在做的事情。

### Matrix Dimensions | 矩阵维度

Tracking dimensions is the single most important debugging skill in deep learning. Here is the 2-3-1 network:

> 追踪维度是深度学习中最重要的调试技能。以下是 2-3-1 网络：

| Step | Operation | Dimensions | Result Shape |
|------|-----------|------------|-------------|
| Input | x | -- | (2,) |
| Hidden linear | W1 * x + b1 | W1: (3, 2), b1: (3,) | (3,) |
| Hidden activation | sigmoid(z1) | -- | (3,) |
| Output linear | W2 * h + b2 | W2: (1, 3), b2: (1,) | (1,) |
| Output activation | sigmoid(z2) | -- | (1,) |

| 步骤 | 操作 | 维度 | 结果形状 |
|------|------|------|---------|
| 输入 | x | -- | (2,) |
| 隐藏层线性变换 | W1 * x + b1 | W1: (3, 2), b1: (3,) | (3,) |
| 隐藏层激活 | sigmoid(z1) | -- | (3,) |
| 输出层线性变换 | W2 * h + b2 | W2: (1, 3), b2: (1,) | (1,) |
| 输出层激活 | sigmoid(z2) | -- | (1,) |

The rule: weight matrix W at layer k has shape (neurons_in_layer_k, neurons_in_layer_k_minus_1). Rows match the current layer. Columns match the previous layer. If the shapes do not line up, you have a bug.

> 规则：第 k 层的权重矩阵 W 的形状为 (第k层神经元数, 第k-1层神经元数)。行对应当前层，列对应上一层。如果形状不匹配，那就是有 bug。

> **【中文解读】** 追踪矩阵维度是深度学习中最重要的调试技能。规则很简单：第 k 层的权重矩阵 W 形状是 (第 k 层神经元数, 第 k-1 层神经元数)。行对应当前层，列对应上一层。维度不匹配就是 bug。

> **【拓展：维度不匹配是深度学习最常见的 bug】** 在 PyTorch 中，你经常看到 `RuntimeError: mat1 and mat2 shapes cannot be multiplied`。这就是维度不匹配。学会手动追踪维度，就能快速定位这类错误。现代工具如 `torchsummary` 或 `torchinfo` 可以帮你自动检查。

### Universal Approximation Theorem | 万能逼近定理

In 1989, George Cybenko proved something remarkable: a neural network with a single hidden layer and enough neurons can approximate any continuous function to any desired accuracy.

> 1989 年，George Cybenko 证明了一件了不起的事：一个具有单个隐藏层和足够多神经元的神经网络可以以任意精度逼近任何连续函数。

This does not mean one hidden layer is always best. It means the architecture is theoretically capable. In practice, deeper networks (more layers, fewer neurons per layer) learn the same functions with far fewer total parameters than shallow-wide networks. That is why deep learning works.

> 这并不意味着一个隐藏层总是最好的。它意味着架构在理论上是可行的。在实践中，更深的网络（更多层，每层更少神经元）用远少于浅宽网络的总参数量来学习相同的函数。这就是深度学习有效的原因。

The intuition: each neuron in the hidden layer learns one "bump" or feature. Enough bumps placed in the right locations can approximate any smooth curve. More neurons, more bumps, better approximation.

> 直觉：隐藏层中的每个神经元学习一个"凸起"或特征。足够多放在正确位置的凸起可以逼近任何平滑曲线。更多神经元，更多凸起，更好的逼近。

```mermaid
graph LR
    subgraph FewNeurons["4 Hidden Neurons"]
        A["Rough approximation"]
    end
    subgraph MoreNeurons["16 Hidden Neurons"]
        B["Close approximation"]
    end
    subgraph ManyNeurons["64 Hidden Neurons"]
        C["Near-perfect fit"]
    end
    FewNeurons --> MoreNeurons --> ManyNeurons
```

> **【中文解读】** 万能逼近定理（1989）：一个隐藏层 + 足够多的神经元可以逼近任何连续函数。但这不代表一层就够了——实践中，"深而窄"的网络比"浅而宽"的更高效。直觉上，每个隐藏神经元学一个"凸起"或特征，足够多的凸起就能拼出任何曲线。

> **【拓展：为什么"深"比"宽"好】** 理论上一层 2^n 个神经元等价于 n 层每层 2 个神经元，但前者参数量是指数级的，后者是线性的。Transformer 的深度（GPT-3 有 96 层）就是利用了这一点——用层数换参数效率。

### Composability | 可组合性

Neural networks are composable. You can stack them, chain them, run them in parallel. A Whisper model uses an encoder network to process audio and a separate decoder network to generate text. Modern LLMs are decoder-only. BERT is encoder-only. T5 is encoder-decoder. The architecture choice defines what the model can do.

> 神经网络是可组合的。你可以堆叠、链接、并行运行它们。Whisper 模型使用编码器网络处理音频，使用单独的解码器网络生成文本。现代 LLM 是纯解码器的。BERT 是纯编码器的。T5 是编码器-解码器的。架构选择决定了模型能做什么。

> **【中文解读】** 神经网络是可组合的：Whisper 用编码器处理音频 + 解码器生成文本；GPT 是纯解码器；BERT 是纯编码器；T5 是编码器-解码器。架构选择决定了模型的能力。

## Build It | 动手构建

Pure Python. No numpy. Every matrix operation written from scratch.

> 纯 Python。不用 numpy。每个矩阵运算从头写起。

### Step 1: Sigmoid Activation

```python
import math

def sigmoid(x):
    x = max(-500.0, min(500.0, x))  # 裁剪到 [-500, 500] 防止指数溢出
    return 1.0 / (1.0 + math.exp(-x))  # σ(x) = 1/(1+e^(-x))
```

The clamp to [-500, 500] prevents overflow. `math.exp(500)` is large but finite. `math.exp(1000)` is infinity.

> 裁剪到 [-500, 500] 可防止溢出。`math.exp(500)` 很大但有限。`math.exp(1000)` 是无穷大。

### Step 2: Layer Class | Layer 类

The most important operation in all of deep learning is matrix multiplication. Every layer, every attention head, every forward pass -- it's matmuls all the way down. A linear layer takes an input vector, multiplies it by a weight matrix, and adds a bias vector: y = Wx + b. That single equation is 90% of the compute in a neural network.

> 深度学习中最重要的运算是矩阵乘法。每一层、每个注意力头、每次前向传播——都是矩阵乘法。线性层接收一个输入向量，乘以权重矩阵，加上偏置向量：y = Wx + b。这一个方程占了神经网络 90% 的计算量。

A layer holds a weight matrix and a bias vector. Its forward method takes an input vector and returns the activated output.

> 一个层包含一个权重矩阵和一个偏置向量。它的 forward 方法接收一个输入向量并返回激活后的输出。

```python
class Layer:
    def __init__(self, n_inputs, n_neurons, weights=None, biases=None):
        if weights is not None:
            self.weights = weights                       # 使用指定的权重（如手动设置 XOR 的权重）
        else:
            import random
            self.weights = [
                [random.uniform(-1, 1) for _ in range(n_inputs)]  # 随机初始化权重
                for _ in range(n_neurons)
            ]                                           # 形状：(n_neurons, n_inputs)
        if biases is not None:
            self.biases = biases                         # 使用指定的偏置
        else:
            self.biases = [0.0] * n_neurons              # 偏置初始化为 0

    def forward(self, inputs):
        self.last_input = inputs                         # 保存输入（反向传播时需要）
        self.last_output = []
        for neuron_idx in range(len(self.weights)):
            z = sum(
                w * x for w, x in zip(self.weights[neuron_idx], inputs)  # 加权求和
            )
            z += self.biases[neuron_idx]                 # 加偏置
            self.last_output.append(sigmoid(z))          # sigmoid 激活
        return self.last_output
```

The weight matrix has shape (n_neurons, n_inputs). Each row is one neuron's weights across all inputs. The forward method loops through neurons, computes the weighted sum plus bias, applies sigmoid, and collects the results.

> 权重矩阵的形状为 (n_neurons, n_inputs)。每一行是一个神经元对所有输入的权重。forward 方法遍历神经元，计算加权和加偏置，应用 sigmoid，并收集结果。

> **【拓展：PyTorch 的 nn.Linear】** 这里的 Layer 类就是 PyTorch `nn.Linear` 的简化版。`nn.Linear(in_features, out_features)` 内部也是维护一个 `(out_features, in_features)` 的权重矩阵和一个 `(out_features,)` 的偏置向量。理解了这个，就理解了深度学习 90% 的计算。

### Step 3: Network Class | Network 类

A network is a list of layers. The forward pass chains them: output of layer k feeds into layer k+1.

> 网络是一个层的列表。前向传播将它们串联：第 k 层的输出作为第 k+1 层的输入。

```python
class Network:
    def __init__(self, layers):
        self.layers = layers   # 按顺序存储所有层

    def forward(self, inputs):
        current = inputs               # 当前层的输入
        for layer in self.layers:
            current = layer.forward(current)  # 逐层前向传播
        return current
```

That is the entire forward pass. Four lines of logic. Data goes in, flows through every layer, comes out the other side.

> 这就是整个前向传播。四行逻辑。数据进入，流过每一层，从另一端出来。

> **【中文解读】** Network 类就是 PyTorch `nn.Sequential` 的简化版。四行代码：数据进去，逐层流过，出来。这就是所有深度学习模型前向传播的本质。

### Step 4: XOR with Hand-Tuned Weights | 用手动设定的权重解决 XOR

In Lesson 01, we solved XOR by combining OR, NAND, and AND perceptrons. Now do the same thing with our Layer and Network classes. The 2-2-1 architecture: two inputs, two hidden neurons, one output.

> 在第 01 课中，我们通过组合 OR、NAND 和 AND 感知机解决了 XOR。现在用我们的 Layer 和 Network 类做同样的事。2-2-1 架构：两个输入，两个隐藏神经元，一个输出。

```python
hidden = Layer(
    n_inputs=2,
    n_neurons=2,
    weights=[[20.0, 20.0], [-20.0, -20.0]],  # 大权重让 sigmoid 接近阶跃函数
    biases=[-10.0, 30.0],                      # 第一个神经元 ≈ OR，第二个 ≈ NAND
)

output = Layer(
    n_inputs=2,
    n_neurons=1,
    weights=[[20.0, 20.0]],                    # 输出层 ≈ AND
    biases=[-30.0],
)

xor_net = Network([hidden, output])

xor_data = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0),
]

for inputs, expected in xor_data:
    result = xor_net.forward(inputs)
    predicted = 1 if result[0] >= 0.5 else 0
    print(f"  {inputs} -> {result[0]:.6f} (rounded: {predicted}, expected: {expected})")
```

The large weights (20, -20) make sigmoid act like a step function. The first hidden neuron approximates OR. The second approximates NAND. The output neuron combines them into AND, which is XOR.

> 大权重 (20, -20) 使 sigmoid 表现得像阶跃函数。第一个隐藏神经元近似 OR，第二个近似 NAND。输出神经元将它们组合成 AND，即 XOR。

### Step 5: Circle Classification | 圆形分类

A harder problem: classify 2D points as inside or outside a circle of radius 0.5 centered at the origin. This requires a curved decision boundary -- impossible for a single perceptron.

> 一个更难的问题：将二维点分类为在原点为中心、半径 0.5 的圆内或圆外。这需要弯曲的决策边界——单个感知机不可能做到。

```python
import random
import math

random.seed(42)

data = []
for _ in range(200):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    label = 1 if (x * x + y * y) < 0.25 else 0   # 距原点距离 < 0.5 则为"内部"
    data.append(([x, y], label))

circle_net = Network([
    Layer(n_inputs=2, n_neurons=8),   # 隐藏层：8 个神经元
    Layer(n_inputs=8, n_neurons=1),   # 输出层：1 个神经元
])
```

With random weights, the network will not classify well. But the forward pass still runs. This is the point -- the forward pass is just computation. Learning the right weights is backpropagation, coming in Lesson 03.

> 使用随机权重，网络分类效果会很差。但前向传播仍然可以运行。这就是关键——前向传播只是计算。学习正确的权重是反向传播的内容，在第 03 课中。

```python
correct = 0
for inputs, expected in data:
    result = circle_net.forward(inputs)
    predicted = 1 if result[0] >= 0.5 else 0
    if predicted == expected:
        correct += 1

print(f"Accuracy with random weights: {correct}/{len(data)} ({100*correct/len(data):.1f}%)")
```

Random weights give poor accuracy -- often worse than guessing the majority class. After training (Lesson 03), this same architecture with 8 hidden neurons will draw a curved boundary that separates inside from outside.

> 随机权重给出很差的准确率——通常比猜测多数类还差。经过训练（第 03 课）后，同样拥有 8 个隐藏神经元的架构将画出弯曲的边界，将圆内和圆外分开。

> **【中文解读】** 随机权重的网络分类效果很差——这很正常，因为还没训练。前向传播只是计算，不涉及学习。训练（下一课的反向传播）才会调整权重。8 个隐藏神经元足以画出圆形的决策边界。

## Use It | 实际应用

PyTorch does everything above in four lines:

> PyTorch 用四行代码就能完成上面的所有功能：

```python
import torch
import torch.nn as nn

model = nn.Sequential(       # 对应我们的 Network 类
    nn.Linear(2, 8),         # 对应 Layer(2, 8)：权重形状 (8, 2)
    nn.Sigmoid(),             # 对应 sigmoid 激活
    nn.Linear(8, 1),         # 对应 Layer(8, 1)：权重形状 (1, 8)
    nn.Sigmoid(),             # 输出层 sigmoid
)

x = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])  # XOR 输入
output = model(x)             # 前向传播
print(output)
```

`nn.Linear(2, 8)` is your Layer class: weight matrix of shape (8, 2), bias vector of shape (8,). `nn.Sigmoid()` is your sigmoid function applied element-wise. `nn.Sequential` is your Network class: chain layers in order.

> `nn.Linear(2, 8)` 就是你的 Layer 类：形状为 (8, 2) 的权重矩阵，形状为 (8,) 的偏置向量。`nn.Sigmoid()` 是你的 sigmoid 函数的逐元素应用。`nn.Sequential` 就是你的 Network 类：按顺序链接层。

The difference is speed and scale. PyTorch runs on GPUs, handles batches of millions of samples, and automatically computes gradients for backpropagation. But the forward pass logic is identical to what you just built from scratch.

> 区别在于速度和规模。PyTorch 在 GPU 上运行，处理数百万样本的批量，并自动计算反向传播的梯度。但前向传播的逻辑与你从零构建的完全相同。

> **【中文解读】** PyTorch 四行代码就实现了我们手动构建的全部逻辑。`nn.Linear` = 我们的 Layer，`nn.Sequential` = 我们的 Network，`nn.Sigmoid()` = 我们的 sigmoid。区别在于 PyTorch 支持 GPU 加速、批量处理和自动求导，但前向传播的核心逻辑完全相同。

## Ship It | 输出物

This lesson produces a reusable prompt for designing network architectures:

> 本课产出一个可复用的网络架构设计提示词：

- `outputs/prompt-network-architect.md`

Use it when you need to decide how many layers, how many neurons per layer, and which activation functions to use for a given problem.

> 当你需要为给定问题决定多少层、每层多少神经元以及使用哪些激活函数时，可以使用它。

## Exercises | 练习题

1. Build a 2-4-2-1 network (two hidden layers) and run the forward pass on XOR data with random weights. Print the intermediate hidden layer outputs to see how the representation transforms at each layer.
   > **练习 1：** 构建 2-4-2-1 网络（两个隐藏层），用随机权重跑 XOR 数据的前向传播。打印中间隐藏层输出，观察每层如何变换数据的表示。

2. Change the hidden layer size in the circle classifier from 8 to 2, then to 32. Run the forward pass with random weights each time. Does the number of hidden neurons change the output range or distribution? Why?
   > **练习 2：** 把圆形分类器的隐藏层从 8 改成 2，再改成 32，分别用随机权重跑前向传播。隐藏神经元数量会改变输出的范围或分布吗？为什么？

3. Implement a `count_parameters` method on the Network class that returns the total number of trainable weights and biases. Test it on a 784-256-128-10 network (the classic MNIST architecture). How many parameters does it have?
   > **练习 3：** 在 Network 类中实现 `count_parameters` 方法，返回所有可训练的权重和偏置总数。用 784-256-128-10 网络（经典 MNIST 架构）测试，它有多少参数？

4. Build a forward pass for a 3-4-4-2 network. Feed it RGB color values (normalized to 0-1) and observe the two outputs. This is the architecture for a simple color classifier with two classes.
   > **练习 4：** 为 3-4-4-2 网络构建前向传播。输入 RGB 颜色值（归一化到 0-1），观察两个输出。这是一个简单的双色分类器的架构。

5. Replace sigmoid with a "leaky step" function: return 0.01 * z if z < 0, else 1.0. Run the forward pass on XOR with the same hand-tuned weights from Step 4. Does it still work? Why is the smooth sigmoid preferred over hard cutoffs?
   > **练习 5：** 用"漏斗阶跃"函数替代 sigmoid：z < 0 时返回 0.01\*z，否则返回 1.0。用 Step 4 的手动权重跑 XOR。还能正常工作吗？为什么平滑的 sigmoid 比硬截断更好？

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Forward pass | "Running the model" | Pushing input through every layer -- multiply by weights, add bias, activate -- to produce an output |
| Hidden layer | "The middle part" | Any layer between input and output whose values are not directly observed in the data |
| Multi-layer network | "A deep neural network" | Layers of neurons stacked sequentially, where each layer's output feeds the next layer's input |
| Activation function | "The nonlinearity" | A function applied after the linear transformation that introduces curves into the decision boundary |
| Sigmoid | "The S-curve" | sigma(z) = 1/(1+e^(-z)), squashes any real number to (0,1), smooth and differentiable everywhere |
| Weight matrix | "The parameters" | A matrix W of shape (current_layer_neurons, previous_layer_neurons) containing learnable connection strengths |
| Bias vector | "The offset" | A vector added after the matrix multiply that lets neurons activate even when all inputs are zero |
| Universal approximation | "Neural nets can learn anything" | A single hidden layer with enough neurons can approximate any continuous function -- but "enough" can mean billions |
| Linear transformation | "The matrix multiply step" | z = W * x + b, the computation before activation, which maps inputs to a new space |
| Decision boundary | "Where the classifier switches" | The surface in input space where the network output crosses the classification threshold |

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 前向传播 (Forward pass) | "跑模型" | 把输入推过每一层——乘权重、加偏置、激活——得到输出 |
| 隐藏层 (Hidden layer) | "中间那部分" | 输入层和输出层之间的层，其值在训练数据中不可直接观测 |
| 多层网络 (Multi-layer network) | "深度神经网络" | 神经元按层堆叠，每层的输出是下一层的输入 |
| 激活函数 (Activation function) | "非线性" | 线性变换后施加的函数，让决策边界变成曲线 |
| Sigmoid | "S 曲线" | σ(z) = 1/(1+e^(-z))，把任意实数压缩到 (0,1)，处处平滑可导 |
| 权重矩阵 (Weight matrix) | "参数" | 形状为 (当前层神经元, 上一层神经元) 的矩阵，包含可学习的连接强度 |
| 偏置向量 (Bias vector) | "偏移" | 矩阵乘法后加上的向量，让神经元在全零输入时也能激活 |
| 万能逼近 (Universal approximation) | "神经网络什么都能学" | 一个隐藏层 + 足够多神经元可逼近任何连续函数——但"足够"可能意味着数十亿 |
| 线性变换 (Linear transformation) | "矩阵乘法那步" | z = Wx + b，激活前的计算，把输入映射到新空间 |
| 决策边界 (Decision boundary) | "分类器切换的地方" | 输入空间中网络输出跨过分类阈值的曲面 |

## Further Reading | 延伸阅读

- Michael Nielsen, "Neural Networks and Deep Learning", Chapter 1-2 (http://neuralnetworksanddeeplearning.com/) -- the clearest free explanation of forward passes and network structure, with interactive visualizations
  Michael Nielsen，《神经网络与深度学习》第 1-2 章——关于前向传播和网络结构最清晰的免费解释，带有交互式可视化
- Cybenko, "Approximation by Superpositions of a Sigmoidal Function" (1989) -- the original universal approximation theorem paper, surprisingly readable
  Cybenko，《用 Sigmoid 函数叠加逼近》(1989)——原始的万能逼近定理论文，出人意料地易读
- 3Blue1Brown, "But what is a neural network?" (https://www.youtube.com/watch?v=aircAruvnKk) -- 20-minute visual walkthrough of layers, weights, and forward passes that builds the right mental model
  3Blue1Brown，《神经网络到底是什么？》——20 分钟的视频讲解，帮助你建立正确的直觉
- Goodfellow, Bengio, Courville, "Deep Learning", Chapter 6 (https://www.deeplearningbook.org/) -- the standard reference for multi-layer networks, free online
  Goodfellow、Bengio、Courville，《深度学习》第 6 章——多层网络的标准参考，免费在线
