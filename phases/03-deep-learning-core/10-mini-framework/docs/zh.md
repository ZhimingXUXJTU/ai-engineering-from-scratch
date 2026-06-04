# 构建你自己的迷你框架

> 你构建了神经元、层、网络、反向传播、激活函数、损失函数、优化器、正则化、初始化和学习率调度——都是独立的部件。现在把它们组装成一个框架。不是 PyTorch，不是 TensorFlow。是你自己的。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 03 全部课程（第 01-09 课）
**预计时间：** ~120 分钟

## 学习目标

- 构建完整的深度学习框架（~500 行），包含 Module、Linear、ReLU、Sigmoid、Dropout、BatchNorm、Sequential、损失函数、优化器和 DataLoader
- 解释 Module 抽象（forward、backward、parameters）以及为什么需要 train/eval 模式切换
- 将所有组件连接成可工作的训练循环，在圆形分类上训练 4 层网络
- 将框架的每个组件映射到 PyTorch 对应物

## 问题引入

十节课的构建模块散落在不同文件中。Value 类在这里，训练循环在那里，权重初始化在另一个文件，学习率调度在又一个文件。训练一个网络，你需要从五个不同课程复制粘贴并手动接线。

框架解决的就是这个问题。PyTorch 给你 `nn.Module`、`nn.Sequential`、`optim.Adam`、`DataLoader` 和串联它们的训练循环模式。

你将在约 500 行 Python 中构建同样的东西。不用 numpy，不用外部依赖。

## 核心概念

### Module 抽象

每个层继承自 Module。Module 有三个职责：
1. **forward()** —— 给定输入计算输出
2. **parameters()** —— 返回所有可训练权重
3. **backward()** —— 计算梯度

### Sequential 容器

串联 Module。前向传播：数据通过 Module 1、然后 Module 2、然后 Module 3。反向传播：逆序。容器本身是 Module——组合模式。

### 训练与评估模式

Dropout 在训练时随机归零神经元，在评估时全部通过。BatchNorm 在训练时用批量统计量，在评估时用运行平均。`train()` 和 `eval()` 方法切换这种行为。

### 框架架构

Module 基类 → Linear 层 → 激活函数 Module → Dropout Module → BatchNorm Module → Sequential 容器 → 损失函数 → 优化器 → DataLoader → 完整训练循环。每一步对应 PyTorch 的一个核心类。

## 动手实现

### Module 基类

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

### Linear 层

```python
class Linear(Module):
    def __init__(self, fan_in, fan_out):
        super().__init__()
        std = math.sqrt(2.0 / fan_in)
        self.weights = [[random.gauss(0, std) for _ in range(fan_in)] for _ in range(fan_out)]
        self.biases = [0.0] * fan_out
        self.weight_grads = [[0.0] * fan_in for _ in range(fan_out)]
        self.bias_grads = [0.0] * fan_out
```

### Sequential 容器

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
```

### 完整训练循环

```python
def train():
    model = Sequential(
        Linear(2, 16), ReLU(), Linear(16, 16), ReLU(),
        Linear(16, 8), ReLU(), Linear(8, 1), Sigmoid(),
    )
    criterion = BCELoss()
    optimizer = Adam(model.parameters(), lr=0.01)
    loader = DataLoader(train_data, batch_size=16, shuffle=True)

    model.train()
    for epoch in range(100):
        for batch_inputs, batch_targets in loader:
            for x, t in zip(batch_inputs, batch_targets):
                pred = model.forward(x)
                loss = criterion(pred, t)
                optimizer.zero_grad()
                grad = criterion.backward()
                model.backward(grad)
                optimizer.step()
```

## 用框架实现

PyTorch 等价代码结构完全一致：Sequential、Linear、ReLU、Sigmoid、BCELoss、Adam、zero_grad、backward、step、train、eval。唯一区别是 PyTorch 用 autograd 自动计算梯度。

```python
model = nn.Sequential(
    nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(),
    nn.Linear(16, 8), nn.ReLU(), nn.Linear(8, 1), nn.Sigmoid(),
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
```

## 练习题

1. 添加 SoftmaxCrossEntropyLoss 用于多分类。
2. 在优化器中实现学习率调度，对比 warmup+cosine 和恒定 lr。
3. 实现 save/load 序列化。
4. 在 Adam 中添加权重衰减。
5. 实现真正的批量梯度累积。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| Module | "一个层" | 框架中的基础抽象——有 forward()、backward()、parameters() 的任何东西 |
| Sequential | "按顺序叠层" | 串联 module 的容器，前向顺序，反向逆序 |
| DataLoader | "喂数据的" | 将数据集分成批量、可选打乱的迭代器 |

## 延伸阅读

- Paszke et al., "PyTorch" (2019) —— PyTorch 设计决策论文
