"""
反向传播从零实现 (Backpropagation from Scratch)

核心概念：
  - Value 类：类似 PyTorch 的 Tensor，每个值节点存储数据、梯度和反向传播函数
  - 计算图：前向传播时构建有向无环图，反向传播时沿图逆序传播梯度
  - 链式法则：每个操作的梯度 = 上游梯度 × 局部导数
  - 拓扑排序：保证节点梯度完全累加后再传播给子节点
  - 梯度消失：sigmoid 的导数最大 0.25，多层堆叠后梯度指数级缩小

在 AI 中的位置：
  - 这就是 PyTorch autograd 的简化实现
  - loss.backward() = 这里的 backward() 方法
  - optimizer.step() = 这里的 p.data -= lr * p.grad
  - 理解本课 = 理解深度学习训练的核心机制
"""

import math
import random


class Value:
    """自动微分的基本节点——类似 PyTorch 的标量 Tensor

    每个 Value 存储：
      - data: 数值
      - grad: 损失对这个值的梯度
      - _backward: 反向传播函数（定义梯度如何传给子节点）
      - _children: 产生这个值的输入节点（用于拓扑排序）
      - _op: 产生这个值的操作名称（用于调试）

    对应 PyTorch: torch.tensor(x, requires_grad=True)
    """

    def __init__(self, data, children=(), op=''):
        self.data = data
        self.grad = 0.0                        # 梯度初始为 0
        self._backward = lambda: None          # 反向传播函数初始为空
        self._children = set(children)         # 子节点（用于拓扑排序）
        self._op = op                          # 操作名（如 '+', '*', 'sigmoid'）

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other):
        """加法操作：a + b

        反向传播：梯度直接传递（d(a+b)/da = 1, d(a+b)/db = 1）
        对应 PyTorch: torch.add(a, b)
        """
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad    # d(a+b)/da = 1，直接传递上游梯度
            other.grad += out.grad   # d(a+b)/db = 1

        out._backward = _backward
        return out

    def __radd__(self, other):
        """支持 0 + Value 的情况（sum() 函数需要）"""
        return self.__add__(other)

    def __mul__(self, other):
        """乘法操作：a * b

        反向传播：d(a*b)/da = b, d(a*b)/db = a
        对应 PyTorch: torch.mul(a, b)
        """
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad    # d(a*b)/da = b * 上游梯度
            other.grad += self.data * out.grad    # d(a*b)/db = a * 上游梯度

        out._backward = _backward
        return out

    def __rmul__(self, other):
        """支持 2 * Value 的情况"""
        return self.__mul__(other)

    def __neg__(self):
        """取负操作：-a = a * (-1)"""
        return self * -1

    def __sub__(self, other):
        """减法操作：a - b = a + (-b)"""
        return self + (-other)

    def sigmoid(self):
        """Sigmoid 激活函数：σ(x) = 1 / (1 + e^(-x))

        反向传播：sigmoid'(x) = σ(x) * (1 - σ(x))，最大值 0.25
        这个最大值 0.25 是梯度消失问题的根源。

        对应 PyTorch: torch.sigmoid(x)
        """
        x = max(-500, min(500, self.data))  # 裁剪防止溢出
        s = 1.0 / (1.0 + math.exp(-x))      # 前向：计算 sigmoid
        out = Value(s, (self,), 'sigmoid')

        def _backward():
            # 反向：σ'(x) = σ(x) * (1 - σ(x))
            # 注意：s 在前向时已计算，这里直接复用
            self.grad += (s * (1 - s)) * out.grad

        out._backward = _backward
        return out

    def backward(self):
        """反向传播：沿计算图逆序传播梯度

        1. 拓扑排序：保证每个节点的梯度完全累加后再传播
        2. 从损失节点开始（梯度 = 1，即 dL/dL = 1）
        3. 逆序遍历，每个节点执行自己的 _backward 函数

        对应 PyTorch: loss.backward()
        """
        topo = []      # 拓扑排序结果
        visited = set()

        def build_topo(v):
            """递归构建拓扑排序：子节点先入队，父节点后入队"""
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1.0     # 损失对自己的梯度 = dL/dL = 1
        for v in reversed(topo):  # 逆序：从输出到输入
            v._backward()         # 每个节点传播梯度给子节点


def mse_loss(predicted, target):
    """均方误差损失：L = (predicted - target)^2

    对应 PyTorch: nn.MSELoss()(predicted, target)
    """
    diff = predicted + Value(-target)  # predicted - target
    return diff * diff                  # (predicted - target)^2


class Neuron:
    """单个神经元：加权求和 + sigmoid 激活

    对应 PyTorch: nn.Linear(n_inputs, 1) + nn.Sigmoid()
    """

    def __init__(self, n_inputs):
        scale = (2.0 / n_inputs) ** 0.5  # He 初始化：防止 sigmoid 饱和
        self.weights = [Value(random.uniform(-scale, scale)) for _ in range(n_inputs)]
        self.bias = Value(0.0)

    def __call__(self, x):
        """前向传播：z = w·x + b, a = sigmoid(z)"""
        act = sum((wi * xi for wi, xi in zip(self.weights, x)), self.bias)
        return act.sigmoid()

    def parameters(self):
        """返回所有可训练参数（权重 + 偏置）"""
        return self.weights + [self.bias]


class Layer:
    """全连接层：一组神经元

    对应 PyTorch: nn.Linear(n_inputs, n_outputs) + nn.Sigmoid()
    """

    def __init__(self, n_inputs, n_outputs):
        self.neurons = [Neuron(n_inputs) for _ in range(n_outputs)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out  # 单神经元直接返回 Value

    def parameters(self):
        """收集所有神经元的参数"""
        params = []
        for n in self.neurons:
            params.extend(n.parameters())
        return params


class Network:
    """多层神经网络：按尺寸列表构建

    对应 PyTorch: nn.Sequential(...)
    用法：Network([2, 4, 1]) 构建 2→4→1 的网络
    """

    def __init__(self, sizes):
        self.layers = []
        for i in range(len(sizes) - 1):
            self.layers.append(Layer(sizes[i], sizes[i + 1]))

    def __call__(self, x):
        """前向传播：逐层计算"""
        for layer in self.layers:
            x = layer(x)
            if not isinstance(x, list):
                x = [x]
        return x[0] if len(x) == 1 else x

    def parameters(self):
        """收集所有层的所有参数"""
        params = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params

    def zero_grad(self):
        """清零所有参数的梯度

        对应 PyTorch: optimizer.zero_grad()
        每次反向传播前必须调用，否则梯度会累加
        """
        for p in self.parameters():
            p.grad = 0.0


def train_xor():
    """训练 XOR：验证反向传播能学习非线性决策边界"""
    print("=" * 50)
    print("Training on XOR")  # 用反向传播训练 XOR
    print("=" * 50)

    random.seed(42)
    net = Network([2, 4, 1])  # 2 输入 → 4 隐藏 → 1 输出

    xor_data = [
        ([0.0, 0.0], 0.0),  # 0 XOR 0 = 0
        ([0.0, 1.0], 1.0),  # 0 XOR 1 = 1
        ([1.0, 0.0], 1.0),  # 1 XOR 0 = 1
        ([1.0, 1.0], 0.0),  # 1 XOR 1 = 0
    ]

    learning_rate = 1.0

    for epoch in range(1000):
        total_loss = Value(0.0)
        for inputs, target in xor_data:
            x = [Value(i) for i in inputs]
            pred = net(x)                       # 前向传播
            loss = mse_loss(pred, target)       # 计算损失
            total_loss = total_loss + loss      # 累积批损失

        net.zero_grad()           # 清零梯度
        total_loss.backward()     # 反向传播：计算所有参数梯度

        for p in net.parameters():
            p.data -= learning_rate * p.grad    # 梯度下降更新权重

        if epoch % 100 == 0:
            print(f"Epoch {epoch:4d} | Loss: {total_loss.data:.6f}")  # 每 100 轮打印损失

    print("\nXOR Results:")  # 打印最终预测结果
    for inputs, target in xor_data:
        x = [Value(i) for i in inputs]
        pred = net(x)
        predicted_class = 1 if pred.data > 0.5 else 0
        print(f"  {inputs} -> {pred.data:.4f} (rounded: {predicted_class}, expected {int(target)})")


def generate_circle_data(n=100):
    """生成圆形分类数据：距原点 < 1 的点标记为"内部""""
    data = []
    for _ in range(n):
        x1 = random.uniform(-1.5, 1.5)
        x2 = random.uniform(-1.5, 1.5)
        label = 1.0 if x1 * x1 + x2 * x2 < 1.0 else 0.0
        data.append(([x1, x2], label))
    return data


def train_circle():
    """训练圆形分类：用在线 SGD 学习曲线决策边界"""
    print("\n" + "=" * 50)
    print("Training on Circle Classification")  # 训练圆形分类
    print("=" * 50)

    random.seed(7)
    circle_data = generate_circle_data(80)

    net = Network([2, 8, 1])  # 2 输入 → 8 隐藏 → 1 输出
    learning_rate = 0.5

    for epoch in range(2000):
        random.shuffle(circle_data)   # 打乱数据防止记住顺序
        total_loss_val = 0.0
        for inputs, target in circle_data:
            x = [Value(i) for i in inputs]
            pred = net(x)
            loss = mse_loss(pred, target)
            net.zero_grad()           # 清零梯度
            loss.backward()           # 反向传播
            for p in net.parameters():
                p.data -= learning_rate * p.grad  # 在线 SGD：逐样本更新
            total_loss_val += loss.data

        if epoch % 200 == 0:
            correct = 0
            for inputs, target in circle_data:
                x = [Value(i) for i in inputs]
                pred = net(x)
                predicted_class = 1.0 if pred.data > 0.5 else 0.0
                if predicted_class == target:
                    correct += 1
            accuracy = correct / len(circle_data) * 100
            print(f"Epoch {epoch:4d} | Loss: {total_loss_val:.4f} | Accuracy: {accuracy:.1f}%")  # 每 200 轮打印准确率

    print("\nSample Circle Results:")  # 测试几个典型点
    test_points = [
        ([0.0, 0.0], "inside"),    # 原点：一定在内部
        ([0.5, 0.5], "inside"),    # 靠近原点：应该在内部
        ([1.2, 1.2], "outside"),   # 远离原点：应该在外部
        ([0.0, 1.2], "outside"),   # 边界附近
        ([-0.3, 0.3], "inside"),   # 内部
    ]
    for point, expected_region in test_points:
        x = [Value(i) for i in point]
        pred = net(x)
        predicted_class = "inside" if pred.data > 0.5 else "outside"
        status = "OK" if predicted_class == expected_region else "WRONG"
        print(f"  {point} -> {pred.data:.4f} ({predicted_class}, expected {expected_region}) {status}")


if __name__ == "__main__":
    train_xor()      # 演示 1：XOR 训练
    train_circle()   # 演示 2：圆形分类训练
