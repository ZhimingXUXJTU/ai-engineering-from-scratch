# Build Your Own Mini Framework | 构建你自己的迷你框架

> You have built neurons, layers, networks, backprop, activations, loss functions, optimizers, regularization, initialization, and LR schedules. All as separate pieces. Now wire them together into a framework. Not PyTorch. Not TensorFlow. Yours.

> **【中文解读】** 把前面所有课程的概念整合成完整框架：自动微分引擎、多种层类型、优化器、正则化、训练循环。这就是 PyTorch 的核心设计——理解这个框架，就理解了 torch.nn 和 torch.autograd 的底层原理。

**Type:** Build
**Languages:** Python
**Prerequisites:** All of Phase 03 (Lessons 01-09)
**Time:** ~120 minutes

## Learning Objectives | 学习目标

- Build a complete deep learning framework (~500 lines) with Module, Linear, ReLU, Sigmoid, Dropout, BatchNorm, Sequential, loss functions, optimizers, and DataLoader
- Explain the Module abstraction (forward, backward, parameters) and why train/eval mode toggling is necessary
- Wire all components into a working training loop that trains a 4-layer network on circle classification
- Map each component of your framework to its PyTorch equivalent (nn.Module, nn.Sequential, optim.Adam, DataLoader)

> **【中文解读】** 本章是 Phase 03 的集成章节——把前面 9 课的所有概念串成一个完整的 ~500 行框架。核心抽象是 Module（forward/backward/parameters），对应 PyTorch 的 nn.Module。完成后你会真正理解 PyTorch 每一行代码背后发生的事情。

## The Problem | 问题引入

You have ten lessons of building blocks scattered across separate files. A `Value` class here, a training loop there, weight initialization in another file, learning rate schedules in yet another. To train a network, you copy-paste from five different lessons and wire them together by hand.

> 你有十课的构建模块散落在不同文件中。这里一个 `Value` 类，那里一个训练循环，另一个文件中是权重初始化，还有另一个是学习率调度。要训练一个网络，你需要从五六个不同的课程中复制粘贴并手动组装。

That is what frameworks solve. PyTorch gives you `nn.Module`, `nn.Sequential`, `optim.Adam`, `DataLoader`, and a training loop pattern that ties them together. TensorFlow gives you `keras.Layer`, `keras.Sequential`, `keras.optimizers.Adam`. These are not magic. They are organizational patterns that make it possible to define, train, and evaluate networks without reinventing the plumbing every time.

> 这就是框架解决的问题。PyTorch 给你 `nn.Module`、`nn.Sequential`、`optim.Adam`、`DataLoader` 和将它们绑在一起的训练循环模式。TensorFlow 给你 `keras.Layer`、`keras.Sequential`、`keras.optimizers.Adam`。这些不是魔法。它们是组织模式，让你可以定义、训练和评估网络，而不必每次都重新发明管道。

You are going to build the same thing in ~500 lines of Python. No numpy. No external dependencies. A framework that can define any feedforward network, train it with SGD or Adam, batch the data, apply dropout and batch normalization, use any activation, and schedule the learning rate.

> 你将用大约 500 行 Python 构建同样的东西。不用 numpy。没有外部依赖。一个可以定义任何前馈网络、用 SGD 或 Adam 训练、批量处理数据、应用 dropout 和批归一化、使用任何激活函数并调度学习率的框架。

When you finish, you will understand exactly what happens when you write `model = nn.Sequential(...)` in PyTorch. You will understand why `model.train()` and `model.eval()` exist. You will understand why `optimizer.zero_grad()` is a separate call. You will understand all of it, because you built all of it.

> 完成后，你会完全理解在 PyTorch 中写 `model = nn.Sequential(...)` 时到底发生了什么。你会理解为什么 `model.train()` 和 `model.eval()` 存在。你会理解为什么 `optimizer.zero_grad()` 是一个单独的调用。你会理解这一切，因为你自己构建了这一切。

> **【中文解读】** 框架的核心价值：把散落的组件统一到一个接口下。Module 是一切的基础——Linear、ReLU、Dropout、BatchNorm 都是 Module。Sequential 是组合模式——一堆 Module 串起来还是一个 Module。这和 PyTorch 的设计完全一致。

> **【拓展：PyTorch 框架的设计哲学】** PyTorch 的核心设计只有 5 个概念：Tensor（数据）、nn.Module（模型）、autograd（自动微分）、Optimizer（优化器）、DataLoader（数据加载）。但就是这 5 个概念支撑了 GPT-4、Stable Diffusion、AlphaFold 等所有前沿模型的训练。简洁是最大的力量。

## The Concept | 核心概念

### The Module Abstraction | Module 抽象

Every layer in PyTorch inherits from `nn.Module`. A Module has three responsibilities:

> PyTorch 中每一层都继承自 `nn.Module`。一个 Module 有三个职责：

1. **forward()** -- compute the output given inputs
   **forward()** -- 给定输入计算输出
2. **parameters()** -- return all trainable weights
   **parameters()** -- 返回所有可训练权重
3. **backward()** -- compute gradients (handled by autograd in PyTorch, explicit in ours)
   **backward()** -- 计算梯度（PyTorch 中由 autograd 处理，我们的框架中需要显式实现）

A Linear layer is a Module. A ReLU activation is a Module. A dropout layer is a Module. A batch normalization layer is a Module. They all have the same interface.

> Linear 层是一个 Module。ReLU 激活是一个 Module。Dropout 层是一个 Module。BatchNorm 层是一个 Module。它们都有相同的接口。

### Sequential Container | Sequential 容器

`nn.Sequential` chains Modules. Forward pass: feed data through Module 1, then Module 2, then Module 3. Backward pass: reverse the chain. The container itself is a Module -- it has forward(), parameters(), and backward(). This is the composite pattern: a sequence of Modules is itself a Module.

> `nn.Sequential` 将 Module 串联起来。前向传播：数据流过 Module 1、然后 Module 2、然后 Module 3。反向传播：反向遍历链。容器本身也是一个 Module——它有 forward()、parameters() 和 backward()。这就是组合模式：Module 序列本身也是一个 Module。

> **【拓展：真实框架的额外功能】** 你的迷你框架覆盖了 PyTorch 的核心概念，但真实框架还有：(1) autograd 自动微分（不需要手写 backward）；(2) GPU 支持（CUDA 内存管理和 kernel 调度）；(3) 分布式训练（DDP、FSDP、DeepSpeed）；(4) 混合精度训练（AMP）；(5) 模型序列化（state_dict + save/load）。PyTorch 的代码库超过 100 万行，但核心抽象还是你实现的这 5 个。

### Training vs Evaluation Mode | 训练与评估模式

Dropout randomly zeroes neurons during training but passes everything through during evaluation. Batch normalization uses batch statistics during training but running averages during evaluation. The `train()` and `eval()` methods toggle this behavior. Every Module has a `training` flag.

### Optimizer | 优化器

The optimizer updates parameters using their gradients. SGD: `param -= lr * grad`. Adam: maintains momentum and variance estimates, then updates. The optimizer does not know about the network architecture -- it only sees a flat list of parameters and their gradients.

### DataLoader | 数据加载器

Batching matters for two reasons. First, you cannot fit the entire dataset in memory for large problems. Second, mini-batch gradient descent provides noise that helps escape local minima. The DataLoader splits data into batches and optionally shuffles between epochs.

> **【拓展：DataLoader 在大模型训练中的演进】** PyTorch 的 DataLoader 是单机的。大模型训练需要分布式 DataLoader：(1) WebDataset 用于流式加载 TB 级数据；(2) Meta 的 SPDL (Streaming Parallel Data Loader) 支持从 S3/GCS 直接流式加载；(3) HuggingFace datasets 库使用 memory-mapped 文件处理超大数据集。Llama 3 的训练数据约 15T token，不可能全部加载到内存。

### Framework Architecture | 框架架构

```mermaid
graph TD
    subgraph "Modules"
        Linear["Linear<br/>W*x + b"]
        ReLU["ReLU<br/>max(0, x)"]
        Sigmoid["Sigmoid<br/>1/(1+e^-x)"]
        Dropout["Dropout<br/>random zero mask"]
        BatchNorm["BatchNorm<br/>normalize activations"]
    end

    subgraph "Containers"
        Sequential["Sequential<br/>chains modules"]
    end

    subgraph "Loss Functions"
        MSE["MSELoss<br/>(pred - target)^2"]
        BCE["BCELoss<br/>binary cross-entropy"]
    end

    subgraph "Optimizers"
        SGD["SGD<br/>param -= lr * grad"]
        Adam["Adam<br/>adaptive moments"]
    end

    subgraph "Data"
        DataLoader["DataLoader<br/>batching + shuffle"]
    end

    Sequential --> |"contains"| Linear
    Sequential --> |"contains"| ReLU
    Sequential --> |"forward/backward"| MSE
    SGD --> |"updates"| Sequential
    DataLoader --> |"feeds"| Sequential
```

### Training Loop | 训练循环

```mermaid
sequenceDiagram
    participant DL as DataLoader
    participant M as Model
    participant L as Loss
    participant O as Optimizer

    loop Each Epoch
        DL->>M: batch of inputs
        M->>M: forward pass (layer by layer)
        M->>L: predictions
        L->>L: compute loss
        L->>M: backward pass (gradients)
        M->>O: parameters + gradients
        O->>M: updated parameters
        O->>O: zero gradients
    end
```

### Module Hierarchy | Module 层级

```mermaid
classDiagram
    class Module {
        +forward(x)
        +backward(grad)
        +parameters()
        +train()
        +eval()
    }

    class Linear {
        -weights
        -biases
        +forward(x)
        +backward(grad)
    }

    class ReLU {
        +forward(x)
        +backward(grad)
    }

    class Sequential {
        -modules[]
        +forward(x)
        +backward(grad)
        +parameters()
    }

    Module <|-- Linear
    Module <|-- ReLU
    Module <|-- Sequential
    Sequential *-- Module
```

## Build It | 动手实现

> **【中文解读】** 下面按顺序构建框架的每个组件：Module 基类 → Linear 层 → 激活函数 → Dropout → BatchNorm → Sequential 容器 → 损失函数 → 优化器 → DataLoader → 完整训练循环。每一步对应 PyTorch 的一个核心类。

### Step 1: Module Base Class | 第一步：Module 基类

The abstract interface that every layer implements.

> 每一层实现的抽象接口。

```python
class Module:
    def __init__(self):
        self.training = True

    def forward(self, x):
        raise NotImplementedError

    def backward(self, grad):
        raise NotImplementedError

    def parameters(self):
        return []

    def train(self):
        self.training = True

    def eval(self):
        self.training = False
```

### Step 2: Linear Layer | 第二步：Linear 层

The fundamental building block. Stores weights and biases, computes Wx + b forward, and weight/input gradients backward.

> 基本构建块。存储权重和偏置，前向计算 Wx + b，反向计算权重/输入梯度。

```python
import math
import random


class Linear(Module):
    def __init__(self, fan_in, fan_out):
        super().__init__()
        std = math.sqrt(2.0 / fan_in)
        self.weights = [[random.gauss(0, std) for _ in range(fan_in)] for _ in range(fan_out)]
        self.biases = [0.0] * fan_out
        self.weight_grads = [[0.0] * fan_in for _ in range(fan_out)]
        self.bias_grads = [0.0] * fan_out
        self.fan_in = fan_in
        self.fan_out = fan_out
        self.input = None

    def forward(self, x):
        self.input = x
        output = []
        for i in range(self.fan_out):
            val = self.biases[i]
            for j in range(self.fan_in):
                val += self.weights[i][j] * x[j]
            output.append(val)
        return output

    def backward(self, grad):
        input_grad = [0.0] * self.fan_in
        for i in range(self.fan_out):
            self.bias_grads[i] += grad[i]
            for j in range(self.fan_in):
                self.weight_grads[i][j] += grad[i] * self.input[j]
                input_grad[j] += grad[i] * self.weights[i][j]
        return input_grad

    def parameters(self):
        params = []
        for i in range(self.fan_out):
            for j in range(self.fan_in):
                params.append((self.weights, i, j, self.weight_grads))
            params.append((self.biases, i, None, self.bias_grads))
        return params
```

### Step 3: Activation Modules | 第三步：激活函数 Module

ReLU, Sigmoid, and Tanh as Modules. Each caches what it needs for the backward pass.

> ReLU、Sigmoid 和 Tanh 作为 Module。每个缓存反向传播所需的信息。

```python
class ReLU(Module):
    def __init__(self):
        super().__init__()
        self.mask = None

    def forward(self, x):
        self.mask = [1.0 if v > 0 else 0.0 for v in x]
        return [max(0.0, v) for v in x]

    def backward(self, grad):
        return [g * m for g, m in zip(grad, self.mask)]


class Sigmoid(Module):
    def __init__(self):
        super().__init__()
        self.output = None

    def forward(self, x):
        self.output = []
        for v in x:
            v = max(-500, min(500, v))
            self.output.append(1.0 / (1.0 + math.exp(-v)))
        return self.output

    def backward(self, grad):
        return [g * o * (1 - o) for g, o in zip(grad, self.output)]


class Tanh(Module):
    def __init__(self):
        super().__init__()
        self.output = None

    def forward(self, x):
        self.output = [math.tanh(v) for v in x]
        return self.output

    def backward(self, grad):
        return [g * (1 - o * o) for g, o in zip(grad, self.output)]
```

### Step 4: Dropout Module | 第四步：Dropout Module

Randomly zeroes elements during training. Scales remaining elements by 1/(1-p) so expected values stay the same. Does nothing during eval.

> 训练时随机将元素置零。按 1/(1-p) 缩放剩余元素，使期望值不变。评估时不做任何操作。

```python
class Dropout(Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p
        self.mask = None

    def forward(self, x):
        if not self.training:
            return x
        self.mask = [0.0 if random.random() < self.p else 1.0 / (1 - self.p) for _ in x]
        return [v * m for v, m in zip(x, self.mask)]

    def backward(self, grad):
        if self.mask is None:
            return grad
        return [g * m for g, m in zip(grad, self.mask)]
```

### Step 5: BatchNorm Module | 第五步：BatchNorm Module

Normalizes activations to zero mean and unit variance per feature across the batch. Maintains running statistics for eval mode.

> 将激活值归一化为跨批量的零均值和单位方差。维护运行统计量用于评估模式。

```python
class BatchNorm(Module):
    def __init__(self, size, momentum=0.1, eps=1e-5):
        super().__init__()
        self.size = size
        self.gamma = [1.0] * size
        self.beta = [0.0] * size
        self.gamma_grads = [0.0] * size
        self.beta_grads = [0.0] * size
        self.running_mean = [0.0] * size
        self.running_var = [1.0] * size
        self.momentum = momentum
        self.eps = eps
        self.x_norm = None
        self.std_inv = None
        self.batch_input = None

    def forward_batch(self, batch):
        batch_size = len(batch)
        output_batch = []

        if self.training:
            mean = [0.0] * self.size
            for sample in batch:
                for j in range(self.size):
                    mean[j] += sample[j]
            mean = [m / batch_size for m in mean]

            var = [0.0] * self.size
            for sample in batch:
                for j in range(self.size):
                    var[j] += (sample[j] - mean[j]) ** 2
            var = [v / batch_size for v in var]

            self.std_inv = [1.0 / math.sqrt(v + self.eps) for v in var]

            self.x_norm = []
            self.batch_input = batch
            for sample in batch:
                normed = [(sample[j] - mean[j]) * self.std_inv[j] for j in range(self.size)]
                self.x_norm.append(normed)
                output = [self.gamma[j] * normed[j] + self.beta[j] for j in range(self.size)]
                output_batch.append(output)

            for j in range(self.size):
                self.running_mean[j] = (1 - self.momentum) * self.running_mean[j] + self.momentum * mean[j]
                self.running_var[j] = (1 - self.momentum) * self.running_var[j] + self.momentum * var[j]
        else:
            std_inv = [1.0 / math.sqrt(v + self.eps) for v in self.running_var]
            for sample in batch:
                normed = [(sample[j] - self.running_mean[j]) * std_inv[j] for j in range(self.size)]
                output = [self.gamma[j] * normed[j] + self.beta[j] for j in range(self.size)]
                output_batch.append(output)

        return output_batch

    def forward(self, x):
        result = self.forward_batch([x])
        return result[0]

    def backward(self, grad):
        if self.x_norm is None:
            return grad
        for j in range(self.size):
            self.gamma_grads[j] += self.x_norm[0][j] * grad[j]
            self.beta_grads[j] += grad[j]
        return [grad[j] * self.gamma[j] * self.std_inv[j] for j in range(self.size)]

    def parameters(self):
        params = []
        for j in range(self.size):
            params.append((self.gamma, j, None, self.gamma_grads))
            params.append((self.beta, j, None, self.beta_grads))
        return params
```

### Step 6: Sequential Container | 第六步：Sequential 容器

Chains modules. Forward goes left-to-right, backward goes right-to-left.

> 串联模块。前向从左到右，反向从右到左。

```python
class Sequential(Module):
    def __init__(self, *modules):
        super().__init__()
        self.modules = list(modules)

    def forward(self, x):
        for module in self.modules:
            x = module.forward(x)
        return x

    def backward(self, grad):
        for module in reversed(self.modules):
            grad = module.backward(grad)
        return grad

    def parameters(self):
        params = []
        for module in self.modules:
            params.extend(module.parameters())
        return params

    def train(self):
        self.training = True
        for module in self.modules:
            module.train()

    def eval(self):
        self.training = False
        for module in self.modules:
            module.eval()
```

### Step 7: Loss Functions | 第七步：损失函数

MSE and Binary Cross-Entropy. Each returns the loss value and provides a backward() that returns the gradient.

> MSE 和二元交叉熵。每个返回损失值，并提供返回梯度的 backward() 方法。

```python
class MSELoss:
    def __call__(self, predicted, target):
        self.predicted = predicted
        self.target = target
        n = len(predicted)
        self.loss = sum((p - t) ** 2 for p, t in zip(predicted, target)) / n
        return self.loss

    def backward(self):
        n = len(self.predicted)
        return [2 * (p - t) / n for p, t in zip(self.predicted, self.target)]


class BCELoss:
    def __call__(self, predicted, target):
        self.predicted = predicted
        self.target = target
        eps = 1e-7
        n = len(predicted)
        self.loss = 0
        for p, t in zip(predicted, target):
            p = max(eps, min(1 - eps, p))
            self.loss += -(t * math.log(p) + (1 - t) * math.log(1 - p))
        self.loss /= n
        return self.loss

    def backward(self):
        eps = 1e-7
        n = len(self.predicted)
        grads = []
        for p, t in zip(self.predicted, self.target):
            p = max(eps, min(1 - eps, p))
            grads.append((-t / p + (1 - t) / (1 - p)) / n)
        return grads
```

### Step 8: SGD and Adam Optimizers | 第八步：SGD 和 Adam 优化器

Both take a parameter list and update weights using gradients.

> 两者都接收参数列表，使用梯度更新权重。

```python
class SGD:
    def __init__(self, parameters, lr=0.01):
        self.params = parameters
        self.lr = lr

    def step(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                container[i][j] -= self.lr * grad_container[i][j]
            else:
                container[i] -= self.lr * grad_container[i]

    def zero_grad(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                grad_container[i][j] = 0.0
            else:
                grad_container[i] = 0.0


class Adam:
    def __init__(self, parameters, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = parameters
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [0.0] * len(parameters)
        self.v = [0.0] * len(parameters)

    def step(self):
        self.t += 1
        for idx, (container, i, j, grad_container) in enumerate(self.params):
            if j is not None:
                g = grad_container[i][j]
            else:
                g = grad_container[i]

            self.m[idx] = self.beta1 * self.m[idx] + (1 - self.beta1) * g
            self.v[idx] = self.beta2 * self.v[idx] + (1 - self.beta2) * g * g

            m_hat = self.m[idx] / (1 - self.beta1 ** self.t)
            v_hat = self.v[idx] / (1 - self.beta2 ** self.t)

            update = self.lr * m_hat / (math.sqrt(v_hat) + self.eps)

            if j is not None:
                container[i][j] -= update
            else:
                container[i] -= update

    def zero_grad(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                grad_container[i][j] = 0.0
            else:
                grad_container[i] = 0.0
```

### Step 9: DataLoader | 第九步：DataLoader

Splits data into batches, optionally shuffles each epoch.

> 将数据分成批次，可选地每个 epoch 打乱。

```python
class DataLoader:
    def __init__(self, data, batch_size=32, shuffle=True):
        self.data = data
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __iter__(self):
        indices = list(range(len(self.data)))
        if self.shuffle:
            random.shuffle(indices)
        for start in range(0, len(indices), self.batch_size):
            batch_indices = indices[start:start + self.batch_size]
            batch = [self.data[i] for i in batch_indices]
            inputs = [item[0] for item in batch]
            targets = [item[1] for item in batch]
            yield inputs, targets

    def __len__(self):
        return (len(self.data) + self.batch_size - 1) // self.batch_size
```

### Step 10: Train a 4-Layer Network on Circle Classification | 第十步：4 层网络分类训练

Wire everything together. Define a model, pick a loss, pick an optimizer, run the training loop.

> 将一切组装在一起。定义模型，选择损失函数，选择优化器，运行训练循环。

```python
def make_circle_data(n=500, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], [label]))
    return data


def train():
    random.seed(42)

    model = Sequential(
        Linear(2, 16),
        ReLU(),
        Linear(16, 16),
        ReLU(),
        Linear(16, 8),
        ReLU(),
        Linear(8, 1),
        Sigmoid(),
    )

    criterion = BCELoss()
    optimizer = Adam(model.parameters(), lr=0.01)

    data = make_circle_data(500)
    split = int(len(data) * 0.8)
    train_data = data[:split]
    test_data = data[split:]

    loader = DataLoader(train_data, batch_size=16, shuffle=True)

    model.train()

    for epoch in range(100):
        total_loss = 0
        total_correct = 0
        total_samples = 0

        for batch_inputs, batch_targets in loader:
            batch_loss = 0
            for x, t in zip(batch_inputs, batch_targets):
                pred = model.forward(x)
                loss = criterion(pred, t)
                batch_loss += loss

                optimizer.zero_grad()
                grad = criterion.backward()
                model.backward(grad)
                optimizer.step()

                predicted_class = 1.0 if pred[0] >= 0.5 else 0.0
                if predicted_class == t[0]:
                    total_correct += 1
                total_samples += 1

            total_loss += batch_loss

        avg_loss = total_loss / total_samples
        accuracy = total_correct / total_samples * 100

        if epoch % 10 == 0 or epoch == 99:
            print(f"Epoch {epoch:3d} | Loss: {avg_loss:.6f} | Train Accuracy: {accuracy:.1f}%")

    model.eval()
    correct = 0
    for x, t in test_data:
        pred = model.forward(x)
        predicted_class = 1.0 if pred[0] >= 0.5 else 0.0
        if predicted_class == t[0]:
            correct += 1
    test_accuracy = correct / len(test_data) * 100
    print(f"\nTest Accuracy: {test_accuracy:.1f}% ({correct}/{len(test_data)})")

    return model, test_accuracy
```

## Use It | 用框架实现

> **【中文解读】** 下面的 PyTorch 代码和你的迷你框架结构完全一致：Sequential、Linear、ReLU、Sigmoid、BCELoss、Adam、zero_grad、backward、step、train、eval。唯一的区别是 PyTorch 用 autograd 自动计算梯度，而你需要手写 backward()。训练循环的五步模式是不变的。

Here is the PyTorch equivalent of what you just built:

> 下面是你刚才构建的框架的 PyTorch 等价实现：

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid(),
)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    model.train()
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, targets)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        test_predictions = model(test_inputs)
```

The structure is identical. `Sequential`, `Linear`, `ReLU`, `Sigmoid`, `BCELoss`, `Adam`, `zero_grad`, `backward`, `step`, `train`, `eval`. Every concept maps one-to-one. The difference is that PyTorch handles autograd automatically (no need to implement backward() in each module), runs on GPU, and has been optimized for years. But the bones are the same.

> 结构完全相同。`Sequential`、`Linear`、`ReLU`、`Sigmoid`、`BCELoss`、`Adam`、`zero_grad`、`backward`、`step`、`train`、`eval`。每个概念一一对应。区别在于 PyTorch 自动处理 autograd（不需要在每个模块中实现 backward()），在 GPU 上运行，并经过多年优化。但骨架是一样的。

Now when you see PyTorch code, you know exactly what is happening at every line. That understanding is the whole point.

> 现在当你看到 PyTorch 代码时，你确切地知道每一行发生了什么。这种理解就是全部意义所在。

## Ship It | 产出物

This lesson produces:
- `outputs/prompt-framework-architect.md` -- a prompt for designing neural network architectures using framework abstractions

> 本课产出：`outputs/prompt-framework-architect.md` - 一个使用框架抽象设计神经网络架构的提示词

## Exercises | 练习题

1. Add a `SoftmaxCrossEntropyLoss` class for multi-class classification. Softmax the predictions, compute cross-entropy loss, and handle the combined backward pass. Test it on a 3-class spiral dataset.

2. Implement learning rate scheduling in the optimizer: add a `set_lr()` method and wire in the cosine schedule from Lesson 09. Train the circle classifier with warmup + cosine and compare to constant LR.

3. Add a `save()` and `load()` method to Sequential that serializes all weights to a JSON file and loads them back. Verify that a loaded model produces the same predictions as the original.

4. Implement weight decay (L2 regularization) in the Adam optimizer. Add a `weight_decay` parameter that shrinks weights toward zero each step. Compare training with decay=0 vs decay=0.01.

5. Replace the per-sample training loop with proper mini-batch gradient accumulation: accumulate gradients across all samples in a batch, then divide by batch size and take one optimizer step. Measure whether this changes convergence speed.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Module | "A layer" | The base abstraction in a framework -- anything with forward(), backward(), and parameters() |
| Sequential | "Stack layers in order" | A container that chains modules, applying them in sequence for forward and reverse for backward |
| Forward pass | "Run the network" | Computing the output by passing input through each module in order |
| Backward pass | "Compute gradients" | Propagating the loss gradient through each module in reverse to compute parameter gradients |
| Parameters | "The trainable weights" | All values in the network that the optimizer can update -- weights and biases |
| Optimizer | "The thing that updates weights" | An algorithm that uses gradients to update parameters, implementing SGD, Adam, or other rules |
| DataLoader | "The thing that feeds data" | An iterator that splits a dataset into batches, optionally shuffling between epochs |
| Training mode | "model.train()" | A flag that enables stochastic behavior like dropout and batch normalization with batch stats |
| Evaluation mode | "model.eval()" | A flag that disables dropout and uses running statistics for batch normalization |
| Zero grad | "Clear the gradients" | Resetting all parameter gradients to zero before computing the next batch's gradients |

## Further Reading | 延伸阅读

- Paszke et al., "PyTorch: An Imperative Style, High-Performance Deep Learning Library" (2019) -- the paper describing PyTorch's design decisions
  Paszke 等人，《PyTorch：一种命令式风格的高性能深度学习库》(2019)——描述 PyTorch 设计决策的论文
- Chollet, "Deep Learning with Python, Second Edition" (2021) -- Chapter 3 covers Keras internals with the same module/layer abstraction
  Chollet，《Python 深度学习》第二版 (2021)——第 3 章用相同的模块/层抽象讲解 Keras 内部机制
- Johnson, "Tiny-DNN" (https://github.com/tiny-dnn/tiny-dnn) -- a header-only C++ deep learning framework for understanding framework internals
  Johnson，《Tiny-DNN》——一个纯头文件 C++ 深度学习框架，用于理解框架内部机制
