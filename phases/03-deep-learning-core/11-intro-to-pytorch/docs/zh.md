# PyTorch 入门

> 你从零构建了引擎的所有部件。现在学真正在用的框架。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.10 课（构建迷你框架）
**预计时间：** ~75 分钟

## 学习目标

- 使用 PyTorch 的 nn.Module、nn.Sequential 和 autograd 构建和训练神经网络
- 使用 PyTorch 张量、GPU 加速和标准训练循环
- 将迷你框架组件转换为 PyTorch 对应物
- 对比纯 Python 框架和 PyTorch 在相同任务上的训练速度

## 问题引入

你有一个可工作的迷你框架。它能在圆形分类问题上训练 4 层网络。但它比 PyTorch 慢约 500 倍。你的框架用嵌套 Python 循环逐个处理样本。PyTorch 将相同操作分发到优化的 C++/CUDA 内核在 GPU 上运行。

PyTorch 填补了每一个差距：GPU 支持、自动微分、序列化、分布式训练、混合精度。而且它保持了你已经构建的完全相同的心智模型：Module、forward()、parameters()、backward()、optimizer.step()。概念一一对应。

## 核心概念

### PyTorch 为什么赢了

2017 年 PyTorch 发布时，TensorFlow 占据 80% 市场份额。PyTorch 的 eager execution（立即执行）让调试和原型开发远比 TF 1.x 的静态图简单。到 2022 年，PyTorch 在 ML 研究论文中的份额超过 75%。教训：开发者体验比绝对性能更重要。

### 张量

张量是多维数组，有三个关键属性：shape、dtype 和 device。

| dtype | 位数 | 用途 |
|-------|------|------|
| float32 | 32 | 默认训练 |
| float16 | 16 | 混合精度 |
| bfloat16 | 16 | LLM 训练 |
| int8 | 8 | 量化推理 |

### Autograd

PyTorch 在前向传播时将操作记录到有向无环图中，然后反向遍历该图自动计算梯度。三条规则：
1. 只有 `requires_grad=True` 的叶张量累积梯度
2. 梯度默认累积——每次 backward 前调用 `optimizer.zero_grad()`
3. `torch.no_grad()` 禁用梯度追踪（评估时使用）

### nn.Module

PyTorch 中每个神经网络组件的基类。当你在 `__init__` 中将 nn.Module 或 nn.Parameter 赋值为属性时，PyTorch 自动注册它。

### 训练循环

每个 PyTorch 训练循环遵循相同的 5 步模式：

```python
for epoch in range(num_epochs):
    model.train()
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
```

五行代码。训练了 GPT-4、Stable Diffusion 和 LLaMA 的五行代码。

## 动手实现

用纯 PyTorch 训练 3 层 MLP 做 MNIST 手写数字分类（784→256→128→10）。10 个 epoch 约 97.8% 测试准确率。

### 模型定义

```python
class MNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.net(x)
```

参数量：235,146。现代标准下很小。训练只需几秒。

## 用框架实现

保存和加载模型：

```python
torch.save(model.state_dict(), "model.pt")
model = MNISTModel()
model.load_state_dict(torch.load("model.pt", weights_only=True))
model.eval()
```

始终保存 `state_dict()`（参数字典），不要直接保存模型对象。

## 练习题

1. 添加批归一化，对比测试准确率和训练速度。
2. 实现学习率搜索器，找到最佳学习率。
3. 添加混合精度训练，测量吞吐量提升。
4. 构建 Fashion-MNIST 自定义 Dataset 并训练。
5. 用 SGD+momentum 替代 Adam，对比收敛曲线。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 张量 (Tensor) | "多维数组" | 类型化、设备感知、带自动微分的数组 |
| Autograd | "自动反向传播" | 前向传播记录操作，反向回放计算精确梯度的系统 |
| nn.Module | "一个层" | 任何可微分计算块的基类 |
| state_dict | "模型权重" | 参数名到张量的有序字典 |
| .backward() | "计算梯度" | 反向遍历计算图 |
| .to(device) | "移到 GPU" | 递归转移所有参数和缓冲区 |
| 混合精度 (Mixed precision) | "用 float16" | float16 前向/反向 + float32 主权重 |
| Eager execution | "立即执行" | 调用时立即执行操作 |

## 延伸阅读

- PyTorch Tutorials (https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)
- PyTorch Performance Tuning Guide (https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
