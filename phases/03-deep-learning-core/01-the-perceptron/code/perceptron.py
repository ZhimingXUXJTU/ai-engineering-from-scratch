"""
感知机 (Perceptron) —— 神经网络的最小学习单元

核心概念：
  - 感知机是最简单的线性分类器：输入加权求和 + 偏置 → 阶跃函数 → 0/1 输出
  - 学习规则：预测错误时，按误差方向调整权重和偏置
  - 局限性：单层感知机只能解决线性可分问题（无法解决 XOR）
  - 突破方案：多层感知机 + sigmoid 激活 + 反向传播 → 可以学习任意形状的决策边界

在 AI 中的位置：
  - 感知机是所有神经网络的基本组成单元
  - PyTorch 的 nn.Linear 就是一个感知机层（不含激活函数）
  - 从感知机到 GPT：多层感知机堆叠 → 多层神经网络 → Transformer → 大语言模型
"""


class Perceptron:
    """感知机分类器 —— 用阶跃函数做二分类

    对应 sklearn.linear_model.Perceptron，核心逻辑相同：
    前向传播（加权求和+阶跃函数）+ 反向更新（按误差调整权重）
    """

    def __init__(self, n_inputs, learning_rate=0.1):
        self.weights = [0.0] * n_inputs  # 权重初始化为 0（实际中常用随机初始化）
        self.bias = 0.0                   # 偏置初始化为 0
        self.lr = learning_rate           # 学习率：控制每次参数更新的步长

    def predict(self, inputs):
        """前向传播：计算加权和 + 阶跃函数

        数学公式：output = step(w · x + b)
        其中 step(z) = 1 if z >= 0 else 0
        """
        total = sum(w * x for w, x in zip(self.weights, inputs))  # 加权求和 w·x
        total += self.bias  # 加偏置 b
        return 1 if total >= 0 else 0  # 阶跃函数：>=0 输出 1，否则输出 0

    def train(self, training_data, epochs=100):
        """感知机学习规则：逐样本更新权重

        对每个样本：预测 → 计算误差 → 按误差调整权重和偏置
        当所有样本都预测正确时收敛（提前停止）
        """
        for epoch in range(epochs):
            errors = 0
            for inputs, target in training_data:
                prediction = self.predict(inputs)  # 前向预测
                error = target - prediction         # 误差 = 真实值 - 预测值
                if error != 0:
                    errors += 1
                    for i in range(len(self.weights)):
                        # 感知机学习规则：w_i += lr * error * x_i
                        # 这个规则是梯度下降的最简单形式
                        self.weights[i] += self.lr * error * inputs[i]
                    self.bias += self.lr * error  # 偏置也按误差更新
            if errors == 0:
                print(f"Converged at epoch {epoch + 1}")  # 全部正确，提前收敛
                return
        print(f"Did not converge after {epochs} epochs")  # 未收敛（如 XOR 问题）


def test_gate(name, n_inputs, data):
    """测试感知机在某个逻辑门上的表现，打印权重和预测结果"""
    print(f"=== {name} ===")
    p = Perceptron(n_inputs)
    p.train(data)
    print(f"  Weights: {p.weights}, Bias: {p.bias}")  # 打印学到的权重和偏置
    for inputs, expected in data:
        result = p.predict(inputs)
        status = "OK" if result == expected else "WRONG"
        print(f"  {inputs} -> {result} (expected {expected}) {status}")
    print()


# ========== 逻辑门训练数据 ==========

and_data = [       # AND 门：两个输入都为 1 时输出 1（线性可分）
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1),
]

or_data = [        # OR 门：任一输入为 1 时输出 1（线性可分）
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 1),
]

not_data = [       # NOT 门：取反（线性可分）
    ([0], 1),
    ([1], 0),
]

xor_data = [       # XOR 门：两个输入不同时输出 1（非线性可分！感知机无法学习）
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0),
]

# ========== 测试线性可分的逻辑门 ==========

test_gate("AND Gate", 2, and_data)   # 会收敛
test_gate("OR Gate", 2, or_data)     # 会收敛
test_gate("NOT Gate", 1, not_data)   # 会收敛

# ========== 测试 XOR（单层感知机会失败） ==========

print("=== XOR Gate (single perceptron - will fail) ===")
p_xor = Perceptron(2)
p_xor.train(xor_data, epochs=1000)  # 即使 1000 轮也无法收敛——这是数学上的硬限制
for inputs, expected in xor_data:
    result = p_xor.predict(inputs)
    status = "OK" if result == expected else "WRONG"
    print(f"  {inputs} -> {result} (expected {expected}) {status}")
print()


# ========== 多层网络解决 XOR ==========
# 核心思路：XOR = (x1 OR x2) AND NOT(x1 AND x2)
# 第一层（隐藏层）：OR 神经元 + NAND 神经元（两条线性决策边界）
# 第二层（输出层）：AND 神经元（组合两条线性的结果，形成非线性边界）

def xor_network(x1, x2):
    """手动构建两层网络解决 XOR：OR + NAND → AND

    展示了多层网络如何组合线性决策边界形成非线性边界。
    这就是深度学习"深"的意义：每多一层，表达能力指数级增长。
    """
    or_neuron = Perceptron(2)
    or_neuron.weights = [1.0, 1.0]    # OR 门权重：两个输入同等重要
    or_neuron.bias = -0.5             # 阈值 -0.5：任一输入为 1 即激活

    nand_neuron = Perceptron(2)
    nand_neuron.weights = [-1.0, -1.0]  # NAND 门权重：取反逻辑
    nand_neuron.bias = 1.5               # 偏置 1.5：只有两个输入都为 1 时不激活

    and_neuron = Perceptron(2)
    and_neuron.weights = [1.0, 1.0]    # AND 门权重
    and_neuron.bias = -1.5             # 偏置 -1.5：需要两个输入都为 1 才激活

    hidden1 = or_neuron.predict([x1, x2])    # 隐藏层神经元 1：检测"至少有一个为 1"
    hidden2 = nand_neuron.predict([x1, x2])  # 隐藏层神经元 2：检测"不全为 1"
    return and_neuron.predict([hidden1, hidden2])  # 输出层：组合两个隐藏特征


print("=== XOR Gate (multi-layer network - works) ===")
for inputs, expected in xor_data:
    result = xor_network(inputs[0], inputs[1])
    status = "OK" if result == expected else "WRONG"
    print(f"  {inputs} -> {result} (expected {expected}) {status}")
print()


# ========== 用反向传播自动训练两层网络 ==========
# 手动设权重不现实，真实问题中需要自动学习
# 方法：sigmoid 替代阶跃函数（可导）+ 反向传播（链式法则求梯度）

class TwoLayerNetwork:
    """两层神经网络，用 sigmoid 激活 + 反向传播训练

    结构：输入层(2) → 隐藏层(2, sigmoid) → 输出层(1, sigmoid)
    训练：前向传播 → 计算误差 → 反向传播梯度 → 更新权重

    这就是 PyTorch 中以下代码的底层原理：
        model = nn.Sequential(nn.Linear(2, 2), nn.Sigmoid(), nn.Linear(2, 1), nn.Sigmoid())
        loss.backward()   # 反向传播
        optimizer.step()  # 更新权重
    """

    def __init__(self, learning_rate=0.5):
        import random
        random.seed(0)
        # 隐藏层：2 个神经元，每个接收 2 个输入
        self.w_hidden = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(2)]
        self.b_hidden = [random.uniform(-1, 1), random.uniform(-1, 1)]
        # 输出层：1 个神经元，接收隐藏层的 2 个输出
        self.w_output = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.b_output = random.uniform(-1, 1)
        self.lr = learning_rate

    def sigmoid(self, x):
        """Sigmoid 激活函数：σ(x) = 1 / (1 + e^(-x))

        为什么用 sigmoid 而不是阶跃函数：sigmoid 处处可导，可以计算梯度
        在现代深度学习中，ReLU 更常用，但 sigmoid 更容易理解反向传播的原理
        """
        import math
        x = max(-500, min(500, x))  # 裁剪到 [-500, 500] 防止数值溢出
        return 1.0 / (1.0 + math.exp(-x))

    def forward(self, inputs):
        """前向传播：输入 → 隐藏层 → 输出

        对应 PyTorch 中的 model(x) 调用
        """
        self.inputs = inputs
        self.hidden_outputs = []
        for i in range(2):
            z = sum(w * x for w, x in zip(self.w_hidden[i], inputs)) + self.b_hidden[i]  # 线性变换
            self.hidden_outputs.append(self.sigmoid(z))  # sigmoid 激活
        z_out = sum(w * h for w, h in zip(self.w_output, self.hidden_outputs)) + self.b_output
        self.output = self.sigmoid(z_out)
        return self.output

    def train(self, training_data, epochs=10000):
        """反向传播训练：前向 → 算误差 → 反向算梯度 → 更新权重

        对应 PyTorch 中的：
            output = model(x)          # 前向传播
            loss = criterion(output, y)  # 计算损失
            loss.backward()             # 反向传播（自动计算梯度）
            optimizer.step()            # 更新权重

        这里手动实现了 backward() 和 step() 的逻辑
        """
        for epoch in range(epochs):
            total_error = 0
            for inputs, target in training_data:
                # ---- 前向传播 ----
                output = self.forward(inputs)
                error = target - output           # 误差
                total_error += error ** 2         # 平方误差（MSE 损失）

                # ---- 反向传播 ----
                # 输出层梯度：d(loss)/d(w_output) = error * sigmoid'(z_out)
                # 其中 sigmoid'(z) = sigmoid(z) * (1 - sigmoid(z))
                d_output = error * output * (1 - output)

                # 隐藏层梯度：链式法则 = 输出层梯度 × 输出层权重 × sigmoid'(z_hidden)
                saved_w_output = self.w_output[:]  # 保存旧权重（更新前要用）
                hidden_deltas = []
                for i in range(2):
                    h = self.hidden_outputs[i]
                    hd = d_output * saved_w_output[i] * h * (1 - h)
                    hidden_deltas.append(hd)

                # ---- 更新权重（梯度下降） ----
                # 更新输出层权重
                for i in range(2):
                    self.w_output[i] += self.lr * d_output * self.hidden_outputs[i]
                self.b_output += self.lr * d_output

                # 更新隐藏层权重
                for i in range(2):
                    for j in range(len(inputs)):
                        self.w_hidden[i][j] += self.lr * hidden_deltas[i] * inputs[j]
                    self.b_hidden[i] += self.lr * hidden_deltas[i]

            if epoch % 2000 == 0:
                print(f"  Epoch {epoch}, error: {total_error:.4f}")  # 每 2000 轮打印误差


print("=== XOR Gate (trained 2-layer network with backpropagation) ===")
net = TwoLayerNetwork(learning_rate=2.0)  # 学习率 2.0（较大，因为数据集很小）
net.train(xor_data, epochs=10000)         # 训练 10000 轮
print()
for inputs, expected in xor_data:
    result = net.forward(inputs)
    predicted = 1 if result >= 0.5 else 0  # 以 0.5 为阈值做二分类决策
    print(f"  {inputs} -> {result:.4f} (rounded: {predicted}, expected {expected})")
    # 输出：4 个样本全部正确，说明两层网络 + 反向传播成功学到了 XOR
