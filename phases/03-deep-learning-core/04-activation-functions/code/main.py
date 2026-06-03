"""
激活函数大全 (Activation Functions)

核心概念：
  - 没有激活函数，多层线性网络等价于单层（线性变换的复合还是线性的）
  - 激活函数引入非线性，让网络能学习弯曲的决策边界
  - 不同激活函数的梯度特性决定了深度网络的可训练性：
    - Sigmoid/Tanh：导数 < 1，深层梯度消失
    - ReLU：正区间导数 = 1，但存在死亡神经元问题
    - GELU/Swish：处处平滑，兼顾梯度流和避免死亡神经元

在 AI 中的位置：
  - Transformer (GPT/BERT)：隐藏层用 GELU
  - CNN (ResNet/EfficientNet)：隐藏层用 ReLU 或 Swish
  - 多分类输出层：Softmax
  - 二分类输出层：Sigmoid
  - PyTorch 对应：torch.nn.GELU, torch.nn.ReLU, torch.nn.Softmax 等
"""

import math
import random


# ========== 激活函数及其导数 ==========

def sigmoid(x):
    """Sigmoid：σ(x) = 1/(1+e^(-x))，输出范围 (0, 1)

    缺点：导数最大 0.25，深层网络梯度消失；输出全正导致优化锯齿形
    对应 PyTorch: torch.sigmoid(x)
    """
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    """Sigmoid 导数：σ(x)(1-σ(x))，最大值 0.25（在 x=0 时）"""
    s = sigmoid(x)
    return s * (1 - s)


def tanh_act(x):
    """Tanh：双曲正切，输出范围 (-1, 1)

    比 sigmoid 好：零中心化，导数最大 1.0
    用于 LSTM 的隐藏状态和候选记忆
    对应 PyTorch: torch.tanh(x)
    """
    return math.tanh(x)


def tanh_derivative(x):
    """Tanh 导数：1 - tanh²(x)，最大值 1.0（在 x=0 时）"""
    t = math.tanh(x)
    return 1 - t * t


def relu(x):
    """ReLU：max(0, x)，正区间导数恒为 1

    让深度学习成为可能的激活函数：梯度不衰减
    缺点：负区间导数为 0，可能导致"死亡神经元"
    对应 PyTorch: torch.nn.functional.relu(x)
    """
    return max(0.0, x)


def relu_derivative(x):
    """ReLU 导数：x>0 时为 1，x<=0 时为 0"""
    return 1.0 if x > 0 else 0.0


def leaky_relu(x, alpha=0.01):
    """Leaky ReLU：负区间保留小斜率 alpha

    解决 ReLU 死亡神经元的最简单方案
    对应 PyTorch: torch.nn.LeakyReLU(alpha)
    """
    return x if x > 0 else alpha * x


def leaky_relu_derivative(x, alpha=0.01):
    """Leaky ReLU 导数：正区间为 1，负区间为 alpha"""
    return 1.0 if x > 0 else alpha


def gelu(x):
    """GELU：高斯误差线性单元，Transformer 的默认激活函数

    近似公式：0.5 * x * (1 + tanh(sqrt(2/π) * (x + 0.044715 * x³)))
    概率解释：按输入为正的概率加权
    优势：处处平滑、允许小负值、无死亡神经元问题
    用于：GPT、BERT、RoBERTa、GPT-4 等
    对应 PyTorch: torch.nn.functional.gelu(x)
    """
    return 0.5 * x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x ** 3)))


def gelu_derivative(x):
    """GELU 导数：Φ(x) + x * φ(x)，其中 Φ 是 CDF，φ 是 PDF"""
    phi = 0.5 * (1 + math.erf(x / math.sqrt(2)))  # 标准正态 CDF
    pdf = math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)  # 标准正态 PDF
    return phi + x * pdf


def swish(x):
    """Swish/SiLU：x * sigmoid(x)，通过自动搜索发现

    用于 EfficientNet 等视觉模型
    与 GELU 性能几乎相同，区别在于用 sigmoid 门控而非高斯 CDF
    对应 PyTorch: torch.nn.functional.silu(x)
    """
    return x * sigmoid(x)


def swish_derivative(x):
    """Swish 导数：σ(x) + x * σ(x)(1-σ(x))"""
    s = sigmoid(x)
    return s + x * s * (1 - s)


def softmax(xs):
    """Softmax：把 logits 变成概率分布

    所有输出在 (0, 1) 之间且和为 1
    减去最大值保证数值稳定性
    用于：多分类输出层、Transformer 注意力权重
    对应 PyTorch: torch.nn.functional.softmax(x, dim)
    """
    max_x = max(xs)  # 数值稳定性技巧：减去最大值防止 exp 溢出
    exps = [math.exp(x - max_x) for x in xs]
    total = sum(exps)
    return [e / total for e in exps]


# ========== 实验工具函数 ==========

def gradient_scan(name, derivative_fn, start=-5, end=5, n=100):
    """扫描激活函数的梯度死亡区域

    在 [-5, 5] 均匀采样 100 个点，统计梯度接近零的比例
    梯度接近零的区域就是"死亡区域"，训练时无法有效更新权重
    """
    step = (end - start) / n
    near_zero = 0  # 梯度接近零的点数
    healthy = 0    # 梯度健康的点数
    for i in range(n):
        x = start + i * step
        g = derivative_fn(x)
        if abs(g) < 0.01:       # 梯度小于 0.01 视为"死亡"
            near_zero += 1
        else:
            healthy += 1
    pct_dead = near_zero / n * 100
    print(f"{name:15s}: {healthy:3d} healthy, {near_zero:3d} near-zero ({pct_dead:.0f}% dead zone)")


def vanishing_gradient_experiment(activation_fn, name, n_layers=10, n_inputs=5):
    """梯度消失实验：信号经过 N 层后的幅度变化

    观察不同激活函数下，信号幅度如何随层数变化：
    - Sigmoid：幅度快速缩小（梯度消失）
    - ReLU：幅度保持不变
    - GELU：幅度略有变化但基本保持
    """
    random.seed(42)
    values = [random.gauss(0, 1) for _ in range(n_inputs)]

    print(f"\n{name} through {n_layers} layers:")
    for layer in range(n_layers):
        weights = [random.gauss(0, 1) for _ in range(n_inputs)]
        z = sum(w * v for w, v in zip(weights, values))  # 加权求和
        activated = activation_fn(z)
        magnitude = abs(activated)
        bar = "#" * int(magnitude * 20)  # 可视化幅度
        print(f"  Layer {layer+1:2d}: magnitude = {magnitude:.6f} {bar}")
        values = [activated] * n_inputs


def dead_neuron_detector(n_inputs=5, hidden_size=20, n_samples=1000):
    """死亡神经元检测器

    在 ReLU 网络中，统计有多少神经元从未被激活（输出始终为 0）
    这些"死亡"神经元无法学习，浪费模型容量
    """
    random.seed(0)
    weights = [[random.gauss(0, 1) for _ in range(n_inputs)] for _ in range(hidden_size)]
    biases = [random.gauss(0, 1) for _ in range(hidden_size)]

    fire_counts = [0] * hidden_size  # 记录每个神经元的激活次数

    for _ in range(n_samples):
        inputs = [random.gauss(0, 1) for _ in range(n_inputs)]
        for neuron_idx in range(hidden_size):
            z = sum(w * x for w, x in zip(weights[neuron_idx], inputs)) + biases[neuron_idx]
            if relu(z) > 0:
                fire_counts[neuron_idx] += 1  # ReLU 输出 > 0 算激活

    dead = sum(1 for c in fire_counts if c == 0)  # 从未激活 = 死亡
    rarely_fire = sum(1 for c in fire_counts if 0 < c < n_samples * 0.05)  # 极少激活
    healthy = hidden_size - dead - rarely_fire

    print(f"\nDead Neuron Report ({hidden_size} neurons, {n_samples} samples):")
    print(f"  Dead (never fired):     {dead}")          # 从未激活的神经元数
    print(f"  Barely alive (<5%):     {rarely_fire}")    # 极少激活的神经元数
    print(f"  Healthy:                {healthy}")        # 健康神经元数
    print(f"  Dead neuron rate:       {dead/hidden_size*100:.1f}%")  # 死亡率

    for i, c in enumerate(fire_counts):
        status = "DEAD" if c == 0 else "WEAK" if c < n_samples * 0.05 else "OK"
        bar = "#" * (c * 40 // n_samples)  # 可视化激活频率
        print(f"  Neuron {i:2d}: {c:4d}/{n_samples} fires [{status:4s}] {bar}")


def make_circle_data(n=200, seed=42):
    """生成圆形分类数据：距原点 < sqrt(1.5) 为"内部"（label=1）"""
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class ActivationNetwork:
    """使用指定激活函数的两层网络，用于对比不同激活函数的训练效果

    结构：输入(2) → 隐藏层(hidden_size, 指定激活) → 输出(1, sigmoid)
    对应 PyTorch: nn.Sequential(nn.Linear(2, hidden_size), act, nn.Linear(hidden_size, 1), nn.Sigmoid())
    """

    def __init__(self, activation_fn, activation_deriv, hidden_size=8, lr=0.1):
        random.seed(0)
        self.act = activation_fn       # 激活函数（可替换对比）
        self.act_d = activation_deriv  # 激活函数导数
        self.lr = lr
        self.hidden_size = hidden_size

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def forward(self, x):
        """前向传播：隐藏层用指定激活函数，输出层用 sigmoid"""
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(self.act(z))  # 使用指定的激活函数

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)  # 输出层始终用 sigmoid（二分类标准）
        return self.out

    def backward(self, target):
        """反向传播：用指定激活函数的导数计算隐藏层梯度"""
        error = self.out - target
        d_out = error * self.out * (1 - self.out)  # 输出层 sigmoid 梯度

        for i in range(self.hidden_size):
            d_h = d_out * self.w2[i] * self.act_d(self.z1[i])  # 隐藏层梯度（不同激活函数导数不同）
            self.w2[i] -= self.lr * d_out * self.h[i]
            for j in range(2):
                self.w1[i][j] -= self.lr * d_h * self.x[j]
            self.b1[i] -= self.lr * d_h
        self.b2 -= self.lr * d_out

    def train(self, data, epochs=200):
        """训练并记录每轮的损失和准确率"""
        losses = []
        for epoch in range(epochs):
            total_loss = 0
            correct = 0
            for x, y in data:
                pred = self.forward(x)
                self.backward(y)
                total_loss += (pred - y) ** 2
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            avg_loss = total_loss / len(data)
            accuracy = correct / len(data) * 100
            losses.append(avg_loss)
            if epoch % 50 == 0 or epoch == epochs - 1:
                print(f"    Epoch {epoch:3d}: loss={avg_loss:.4f}, accuracy={accuracy:.1f}%")
        return losses


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: Activation Function Values")  # 各种激活函数在典型输入点的值
    print("=" * 60)
    test_points = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
    for x in test_points:
        print(f"  x={x:5.1f}  sigmoid={sigmoid(x):.4f}  tanh={tanh_act(x):.4f}  "
              f"relu={relu(x):.4f}  gelu={gelu(x):.4f}  swish={swish(x):.4f}")
        # 观察：sigmoid 输出全正(0-1)，tanh 零中心(-1到1)，ReLU 负数变零，GELU/Swish 允许小负值

    print(f"\n  softmax([2.0, 1.0, 0.1]) = {softmax([2.0, 1.0, 0.1])}")  # 最大值得到最高概率
    print(f"  softmax([10, 10, 10])    = {softmax([10.0, 10.0, 10.0])}")  # 等值输入 → 均匀分布

    print("\n" + "=" * 60)
    print("STEP 2: Gradient Dead Zones")  # 梯度死亡区域扫描
    print("=" * 60)
    gradient_scan("Sigmoid", sigmoid_derivative)      # 预期：大量死亡区域（两端饱和）
    gradient_scan("Tanh", tanh_derivative)             # 预期：比 sigmoid 少但仍存在
    gradient_scan("ReLU", relu_derivative)              # 预期：负半轴全部死亡
    gradient_scan("Leaky ReLU", leaky_relu_derivative)  # 预期：负半轴仍有小梯度
    gradient_scan("GELU", gelu_derivative)              # 预期：几乎没有死亡区域
    gradient_scan("Swish", swish_derivative)            # 预期：几乎没有死亡区域

    print("\n" + "=" * 60)
    print("STEP 3: Vanishing Gradient Experiment")  # 梯度消失实验
    print("=" * 60)
    vanishing_gradient_experiment(sigmoid, "Sigmoid")  # 预期：magnitude 快速缩小
    vanishing_gradient_experiment(relu, "ReLU")        # 预期：magnitude 保持
    vanishing_gradient_experiment(gelu, "GELU")        # 预期：magnitude 基本保持

    print("\n" + "=" * 60)
    print("STEP 4: Dead Neuron Detection")  # ReLU 死亡神经元检测
    print("=" * 60)
    dead_neuron_detector()  # 统计 ReLU 网络中从未激活的神经元比例

    print("\n" + "=" * 60)
    print("STEP 5: Training Comparison (Circle Dataset)")  # 不同激活函数的训练对比
    print("=" * 60)
    data = make_circle_data()

    configs = [
        ("Sigmoid", sigmoid, sigmoid_derivative),    # 预期：收敛最慢（梯度消失）
        ("ReLU", relu, relu_derivative),              # 预期：收敛快（梯度不衰减）
        ("GELU", gelu, gelu_derivative),              # 预期：收敛快且平滑
    ]

    results = {}
    for name, act_fn, act_d_fn in configs:
        print(f"\n--- Training with {name} ---")
        net = ActivationNetwork(act_fn, act_d_fn, hidden_size=8, lr=0.1)
        losses = net.train(data, epochs=200)
        results[name] = losses

    print("\n=== Final Loss Comparison ===")  # 最终损失对比
    for name, losses in results.items():
        improvement = (1 - losses[-1] / losses[0]) * 100 if losses[0] > 0 else 0
        print(f"  {name:10s}: start={losses[0]:.4f} -> end={losses[-1]:.4f} (improvement: {improvement:.1f}%)")
        # GELU/ReLU 的 improvement 应明显高于 Sigmoid
