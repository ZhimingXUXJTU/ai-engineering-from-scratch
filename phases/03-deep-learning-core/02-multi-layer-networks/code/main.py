"""
多层网络与前向传播 (Multi-Layer Networks and Forward Pass)

核心概念：
  - Layer 类：封装一层神经元的计算（线性变换 Wx+b + 激活函数）
  - Network 类：按顺序堆叠多个 Layer，实现前向传播
  - 前向传播：数据从输入层 → 隐藏层 → 输出层的计算过程（不含学习）
  - 矩阵维度追踪：W 形状为 (当前层神经元数, 上一层神经元数)

在 AI 中的位置：
  - PyTorch nn.Linear = 这里的 Layer 类
  - PyTorch nn.Sequential = 这里的 Network 类
  - 理解前向传播是理解反向传播、训练、推理的基础
  - 所有深度学习模型（CNN、RNN、Transformer）的核心计算都是矩阵乘法 + 激活
"""

import math
import random


def sigmoid(x):
    """Sigmoid 激活函数：σ(x) = 1 / (1 + e^(-x))

    把任意实数压缩到 (0, 1) 区间，处处可导（可计算梯度）。
    在现代深度学习中，ReLU 更常用，但 sigmoid 更容易理解反向传播原理。

    对应 PyTorch: torch.nn.Sigmoid()
    """
    x = max(-500.0, min(500.0, x))  # 裁剪防止 math.exp 溢出
    return 1.0 / (1.0 + math.exp(-x))


class Layer:
    """全连接层（Fully Connected Layer / Dense Layer）

    对应 PyTorch 的 nn.Linear + 激活函数的组合。
    每个 Layer 内部维护：
      - weights: 形状 (n_neurons, n_inputs) 的权重矩阵
      - biases: 形状 (n_neurons,) 的偏置向量

    前向传播：output = sigmoid(W @ input + b)
    """

    def __init__(self, n_inputs, n_neurons, weights=None, biases=None):
        if weights is not None:
            self.weights = weights    # 手动指定权重（如 XOR 的预设权重）
        else:
            self.weights = [
                [random.uniform(-1, 1) for _ in range(n_inputs)]  # 随机初始化
                for _ in range(n_neurons)
            ]  # 形状：(n_neurons, n_inputs) —— 每行是一个神经元的权重
        if biases is not None:
            self.biases = biases      # 手动指定偏置
        else:
            self.biases = [0.0] * n_neurons  # 偏置初始化为 0

    def forward(self, inputs):
        """前向传播：对每个神经元计算 w·x + b，然后过 sigmoid

        数学：z_i = Σ(w_ij * x_j) + b_i,  a_i = sigmoid(z_i)
        保存 last_input 和 last_output 供后续反向传播使用。
        """
        self.last_input = inputs    # 保存输入（反向传播时需要）
        self.last_output = []
        for neuron_idx in range(len(self.weights)):
            z = sum(
                w * x for w, x in zip(self.weights[neuron_idx], inputs)
            )  # 加权求和：w·x
            z += self.biases[neuron_idx]  # 加偏置：w·x + b
            self.last_output.append(sigmoid(z))  # sigmoid 激活
        return self.last_output


class Network:
    """多层神经网络：按顺序堆叠多个 Layer

    对应 PyTorch 的 nn.Sequential。
    前向传播：把上一层的输出传给下一层。
    """

    def __init__(self, layers):
        self.layers = layers  # Layer 对象列表，按顺序连接

    def forward(self, inputs):
        """前向传播：输入 → 逐层计算 → 输出

        对应 PyTorch: output = model(x)
        """
        current = inputs
        for layer in self.layers:
            current = layer.forward(current)  # 上一层的输出是下一层的输入
        return current

    def count_parameters(self):
        """统计所有可训练参数的总数（权重 + 偏置）

        对于 Layer(n_inputs, n_neurons)，参数量 = n_inputs * n_neurons + n_neurons
        了解参数量有助于判断模型复杂度和过拟合风险。
        """
        total = 0
        for layer in self.layers:
            for neuron_weights in layer.weights:
                total += len(neuron_weights)  # 权重数量
            total += len(layer.biases)         # 偏置数量
        return total


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO 1: XOR with hand-tuned 2-2-1 network")  # 手动设定权重的 XOR 网络
    print("=" * 60)

    # 手动设定的权重：大权重(20)让 sigmoid 近似阶跃函数
    # 隐藏层第 1 个神经元 ≈ OR 门，第 2 个神经元 ≈ NAND 门
    hidden = Layer(
        n_inputs=2,
        n_neurons=2,
        weights=[[20.0, 20.0], [-20.0, -20.0]],  # 第 1 个神经元：w=[20,20], 第 2 个：w=[-20,-20]
        biases=[-10.0, 30.0],                      # OR 的偏置 -10, NAND 的偏置 30
    )

    # 输出层 ≈ AND 门：组合隐藏层的 OR 和 NAND 结果
    output = Layer(
        n_inputs=2,
        n_neurons=1,
        weights=[[20.0, 20.0]],
        biases=[-30.0],
    )

    xor_net = Network([hidden, output])

    xor_data = [
        ([0, 0], 0),  # 0 XOR 0 = 0
        ([0, 1], 1),  # 0 XOR 1 = 1
        ([1, 0], 1),  # 1 XOR 0 = 1
        ([1, 1], 0),  # 1 XOR 1 = 0
    ]

    all_correct = True
    for inputs, expected in xor_data:
        result = xor_net.forward(inputs)
        predicted = 1 if result[0] >= 0.5 else 0  # 以 0.5 为阈值做二分类
        status = "OK" if predicted == expected else "WRONG"
        if predicted != expected:
            all_correct = False
        print(f"  {inputs} -> {result[0]:.6f} (rounded: {predicted}, expected: {expected}) {status}")

    print(f"\nXOR solved: {all_correct}")  # 应该全部正确
    print(f"Parameters: {xor_net.count_parameters()}")  # 参数量：2*2+2 + 2*1+1 = 9

    print()
    print("=" * 60)
    print("DEMO 2: Circle classification with 2-8-1 network")  # 圆形分类：非线性决策边界
    print("=" * 60)

    random.seed(42)

    # 生成 200 个 2D 点，标记是否在半径 0.5 的圆内
    data = []
    for _ in range(200):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        label = 1 if (x * x + y * y) < 0.25 else 0  # 距原点 < 0.5 则标记为"内部"
        data.append(([x, y], label))

    inside_count = sum(1 for _, label in data if label == 1)
    outside_count = len(data) - inside_count
    print(f"  Dataset: {len(data)} points ({inside_count} inside, {outside_count} outside)")  # 圆内/圆外点数

    random.seed(7)
    # 2-8-1 网络：2 个输入 → 8 个隐藏神经元 → 1 个输出
    circle_net = Network([
        Layer(n_inputs=2, n_neurons=8),  # 隐藏层：8 个神经元足以学习圆形边界
        Layer(n_inputs=8, n_neurons=1),  # 输出层：1 个神经元做二分类
    ])

    correct = 0
    for inputs, expected in data:
        result = circle_net.forward(inputs)
        predicted = 1 if result[0] >= 0.5 else 0
        if predicted == expected:
            correct += 1

    print(f"  Accuracy with random weights: {correct}/{len(data)} ({100 * correct / len(data):.1f}%)")  # 随机权重准确率很低
    print(f"  Parameters: {circle_net.count_parameters()}")  # 参数量：2*8+8 + 8*1+1 = 33
    print(f"  (Random weights give poor accuracy -- training needed)")  # 需要训练才能提高准确率

    print()
    print("=" * 60)
    print("DEMO 3: Forward pass internals on XOR")  # 观察前向传播中间层输出
    print("=" * 60)

    for inputs, expected in xor_data:
        xor_net.forward(inputs)
        h = xor_net.layers[0].last_output  # 隐藏层输出
        o = xor_net.layers[1].last_output  # 输出层输出
        print(f"  Input: {inputs}")
        print(f"    Hidden: [{h[0]:.6f}, {h[1]:.6f}]")  # 隐藏层：OR 值和 NAND 值
        print(f"    Output: {o[0]:.6f} -> {'1' if o[0] >= 0.5 else '0'} (expected: {expected})")  # 最终输出

    print()
    print("=" * 60)
    print("DEMO 4: Parameter count for classic architectures")  # 经典网络的参数量
    print("=" * 60)

    architectures = [
        ("2-3-1 (this lesson)", [2, 3, 1]),                # 本课示例
        ("2-8-1 (circle)", [2, 8, 1]),                     # 圆形分类器
        ("784-256-128-10 (MNIST)", [784, 256, 128, 10]),   # 经典 MNIST 手写数字网络
        ("784-512-256-128-10 (deep MNIST)", [784, 512, 256, 128, 10]),  # 更深的 MNIST 网络
    ]

    for name, sizes in architectures:
        layers = []
        for i in range(1, len(sizes)):
            layers.append(Layer(n_inputs=sizes[i - 1], n_neurons=sizes[i]))
        net = Network(layers)
        print(f"  {name}: {net.count_parameters():,} parameters")  # 打印参数量
        # MNIST (784-256-128-10) 参数量 = 784*256+256 + 256*128+128 + 128*10+10 = 235,146
