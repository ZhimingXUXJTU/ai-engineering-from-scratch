"""
优化器从零实现 (Optimizers from Scratch)

核心概念：
  - SGD：最简单的优化器，w = w - lr * gradient
  - Momentum：累积历史梯度，抑制振荡、加速一致方向
  - Adam：Momentum + RMSProp 的结合，自适应学习率 + 偏差修正
  - AdamW：Adam + 解耦权重衰减，Transformer 训练的标配

在 AI 中的位置：
  - GPT/BERT/Llama 训练：AdamW（lr=1e-4~3e-4, weight_decay=0.01~0.1）
  - CNN（ResNet/EfficientNet）：SGD + Momentum（lr=0.1, momentum=0.9）
  - 微调预训练模型：AdamW（lr=2e-5）
  - PyTorch: torch.optim.AdamW, torch.optim.SGD 等
"""

import math
import random


class SGD:
    """随机梯度下降：最简单的优化器

    w = w - lr * gradient
    缺点：振荡、单一学习率、无法穿越平坦区域
    对应 PyTorch: torch.optim.SGD(lr=0.01)
    """

    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        """参数更新：沿梯度反方向移动"""
        for i in range(len(params)):
            params[i] -= self.lr * grads[i]


class SGDMomentum:
    """SGD + 动量：累积历史梯度方向

    v = beta * v + gradient（速度 = 衰减 × 历史速度 + 当前梯度）
    w = w - lr * v

    动量的直觉：球滚下山坡——一致方向加速，振荡方向抵消
    beta=0.9 意味着大约记住最近 10 步的梯度
    对应 PyTorch: torch.optim.SGD(lr=0.01, momentum=0.9)
    """

    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.velocities = None  # 速度（动量）向量

    def step(self, params, grads):
        if self.velocities is None:
            self.velocities = [0.0] * len(params)
        for i in range(len(params)):
            self.velocities[i] = self.beta * self.velocities[i] + grads[i]  # 累积动量
            params[i] -= self.lr * self.velocities[i]


class Adam:
    """Adam：自适应矩估计优化器

    结合 Momentum（一阶矩 = 梯度均值）和 RMSProp（二阶矩 = 梯度方差）
    每个参数有不同的有效学习率：
      - 经常大幅更新的参数 → 减慢
      - 更新少的参数 → 加速
    偏差修正：补偿初始几步 m 和 v 偏向 0 的问题

    默认参数：lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8
    对 80% 的问题有效
    对应 PyTorch: torch.optim.Adam(lr=0.001)
    """

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1    # 一阶矩衰减率（梯度均值的记忆长度）
        self.beta2 = beta2    # 二阶矩衰减率（梯度方差的记忆长度）
        self.epsilon = epsilon  # 防止除以零
        self.m = None         # 一阶矩（梯度均值）
        self.v = None         # 二阶矩（梯度方差）
        self.t = 0            # 时间步

    def step(self, params, grads):
        """Adam 参数更新：
        1. 更新一阶矩 m = beta1 * m + (1-beta1) * grad
        2. 更新二阶矩 v = beta2 * v + (1-beta2) * grad²
        3. 偏差修正 m_hat = m / (1 - beta1^t), v_hat = v / (1 - beta2^t)
        4. 更新参数 w -= lr * m_hat / (sqrt(v_hat) + eps)
        """
        if self.m is None:
            self.m = [0.0] * len(params)  # 初始化一阶矩
            self.v = [0.0] * len(params)  # 初始化二阶矩

        self.t += 1

        for i in range(len(params)):
            # 更新矩估计
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]   # 一阶矩（梯度均值）
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2  # 二阶矩（梯度方差）

            # 偏差修正：初始几步 m 和 v 偏向 0，除以 (1-beta^t) 修正
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # 参数更新：自适应学习率 = lr * m_hat / (sqrt(v_hat) + eps)
            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)


class AdamW:
    """AdamW：解耦权重衰减的 Adam

    与 Adam + L2 正则化的区别：
      - Adam + L2：正则化项被自适应学习率缩放，不同参数正则化强度不同
      - AdamW：权重衰减直接作用于参数，所有参数正则化强度一致

    这是 BERT、GPT、Llama、Stable Diffusion 等模型的默认优化器
    对应 PyTorch: torch.optim.AdamW(lr=3e-4, weight_decay=0.01)
    """

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.weight_decay = weight_decay  # 权重衰减系数
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        """AdamW 更新 = Adam 更新 + 解耦权重衰减"""
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)

        self.t += 1

        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2

            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # 解耦权重衰减：直接缩小权重，不受自适应学习率影响
            params[i] = params[i] * (1 - self.weight_decay * self.lr)
            # Adam 参数更新
            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)


def sigmoid(x):
    """Sigmoid 激活函数"""
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def make_circle_data(n=200, seed=42):
    """生成圆形分类数据"""
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class OptimizerTestNetwork:
    """用于对比不同优化器的两层网络

    结构：输入(2) → 隐藏层(8, ReLU) → 输出(1, Sigmoid)
    损失：二元交叉熵
    """

    def __init__(self, optimizer, hidden_size=8):
        random.seed(0)
        self.hidden_size = hidden_size
        self.optimizer = optimizer  # 可替换的优化器

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def get_params(self):
        """收集所有参数为一维列表（传给优化器）"""
        params = []
        for row in self.w1:
            params.extend(row)
        params.extend(self.b1)
        params.extend(self.w2)
        params.append(self.b2)
        return params

    def set_params(self, params):
        """从一维列表恢复参数"""
        idx = 0
        for i in range(self.hidden_size):
            for j in range(2):
                self.w1[i][j] = params[idx]
                idx += 1
        for i in range(self.hidden_size):
            self.b1[i] = params[idx]
            idx += 1
        for i in range(self.hidden_size):
            self.w2[i] = params[idx]
            idx += 1
        self.b2 = params[idx]

    def forward(self, x):
        """前向传播"""
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))  # ReLU

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def compute_grads(self, target):
        """计算所有参数的梯度（BCE + sigmoid + ReLU）"""
        eps = 1e-15
        p = max(eps, min(1 - eps, self.out))
        d_loss = -(target / p) + (1 - target) / (1 - p)  # BCE 梯度
        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        grads = [0.0] * (self.hidden_size * 2 + self.hidden_size + self.hidden_size + 1)
        idx = 0
        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            grads[idx] = d_h * self.x[0]
            grads[idx + 1] = d_h * self.x[1]
            idx += 2

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            grads[idx] = d_out * self.w2[i] * d_relu
            idx += 1

        for i in range(self.hidden_size):
            grads[idx] = d_out * self.h[i]
            idx += 1

        grads[idx] = d_out
        return grads

    def train(self, data, epochs=300):
        """训练：前向 → 计算梯度 → 优化器更新"""
        losses = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in data:
                pred = self.forward(x)
                grads = self.compute_grads(y)
                params = self.get_params()
                self.optimizer.step(params, grads)  # 优化器更新参数
                self.set_params(params)

                eps = 1e-15
                p = max(eps, min(1 - eps, pred))
                total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            avg_loss = total_loss / len(data)
            accuracy = correct / len(data) * 100
            losses.append((avg_loss, accuracy))
            if epoch % 75 == 0 or epoch == epochs - 1:
                print(f"    Epoch {epoch:3d}: loss={avg_loss:.4f}, accuracy={accuracy:.1f}%")
        return losses


def bias_correction_demo():
    """演示 Adam 的偏差修正：初始几步原始矩偏向 0，修正后接近真实值"""
    beta1 = 0.9
    beta2 = 0.999
    gradient = 1.0

    print("  Step | m_raw  | m_corrected | v_raw    | v_corrected")
    print("  " + "-" * 55)

    m = 0.0
    v = 0.0
    for t in range(1, 11):
        m = beta1 * m + (1 - beta1) * gradient  # 原始一阶矩
        v = beta2 * v + (1 - beta2) * gradient ** 2  # 原始二阶矩
        m_hat = m / (1 - beta1 ** t)  # 修正后一阶矩
        v_hat = v / (1 - beta2 ** t)  # 修正后二阶矩
        print(f"  {t:4d} | {m:.4f} | {m_hat:.4f}      | {v:.6f} | {v_hat:.6f}")
        # 观察：step 1 时 m_raw=0.1 但 m_corrected=1.0（修正后接近真实梯度）
        # step 10+ 时修正效果消失（1-beta^t ≈ 1）


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: SGD on a Simple Function")  # SGD 最小化简单二次函数
    print("=" * 60)
    print("  Minimizing f(x) = (x - 3)^2, starting at x = 10")
    x = [10.0]
    sgd = SGD(lr=0.1)
    for step in range(20):
        grad = [2.0 * (x[0] - 3.0)]  # f'(x) = 2(x-3)
        sgd.step(x, grad)
        loss = (x[0] - 3.0) ** 2
        if step % 5 == 0 or step == 19:
            print(f"    Step {step:2d}: x={x[0]:.6f}, loss={loss:.6f}")  # 逐步逼近 x=3

    print("\n" + "=" * 60)
    print("STEP 2: Bias Correction in Adam")  # Adam 偏差修正演示
    print("=" * 60)
    print("  Showing how raw moments are biased toward zero initially")
    bias_correction_demo()  # 展示修正前后差异

    print("\n" + "=" * 60)
    print("STEP 3: Optimizer Comparison on Circle Dataset")  # 四种优化器对比
    print("=" * 60)
    data = make_circle_data()

    configs = [
        ("SGD (lr=0.05)", SGD(lr=0.05)),                                       # 基础 SGD
        ("SGD+Momentum (lr=0.05, beta=0.9)", SGDMomentum(lr=0.05, beta=0.9)),  # SGD + 动量
        ("Adam (lr=0.001)", Adam(lr=0.001)),                                     # Adam
        ("AdamW (lr=0.001, wd=0.01)", AdamW(lr=0.001, weight_decay=0.01)),     # AdamW
    ]

    results = {}
    for name, opt in configs:
        print(f"\n--- {name} ---")
        net = OptimizerTestNetwork(opt, hidden_size=8)
        history = net.train(data, epochs=300)
        results[name] = history

    print("\n" + "=" * 60)
    print("FINAL COMPARISON")  # 最终对比
    print("=" * 60)
    for name, history in results.items():
        final_loss, final_acc = history[-1]
        first_90 = None
        for epoch, (loss, acc) in enumerate(history):
            if acc >= 85.0:
                first_90 = epoch
                break
        reached = f"epoch {first_90}" if first_90 is not None else "never"
        print(f"  {name:40s}: acc={final_acc:.1f}%, loss={final_loss:.4f}, reached 85%: {reached}")
        # 预期：Adam/AdamW 达到 85% 最快，SGD 最慢

    print("\n" + "=" * 60)
    print("STEP 4: Weight Decay Effect")  # 权重衰减效果对比
    print("=" * 60)
    random.seed(42)
    large_weights = [random.uniform(-5, 5) for _ in range(10)]
    weights_adam = list(large_weights)
    weights_adamw = list(large_weights)

    opt_adam = Adam(lr=0.001)
    opt_adamw = AdamW(lr=0.001, weight_decay=0.1)

    print(f"  Initial weight L2 norm: {math.sqrt(sum(w*w for w in large_weights)):.4f}")

    for step in range(100):
        grads = [random.gauss(0, 0.1) for _ in range(10)]
        opt_adam.step(weights_adam, list(grads))
        opt_adamw.step(weights_adamw, list(grads))

    norm_adam = math.sqrt(sum(w * w for w in weights_adam))
    norm_adamw = math.sqrt(sum(w * w for w in weights_adamw))
    print(f"  After 100 steps:")
    print(f"    Adam  weight L2 norm: {norm_adam:.4f}")  # Adam 权重几乎没缩小
    print(f"    AdamW weight L2 norm: {norm_adamw:.4f}")  # AdamW 权重明显缩小
    print(f"    AdamW shrinks weights {norm_adam/max(0.001, norm_adamw):.1f}x more")  # AdamW 缩小更多倍
