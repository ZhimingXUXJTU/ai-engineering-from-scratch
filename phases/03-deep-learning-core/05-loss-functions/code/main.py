"""
损失函数大全 (Loss Functions)

核心概念：
  - 损失函数是模型唯一优化的目标——选错损失函数，模型优化错的方向
  - MSE（均方误差）：回归任务标配，对异常值敏感
  - 交叉熵（Cross-Entropy）：分类任务标配，用 -log(p) 惩罚不自信的预测
  - 标签平滑：防止过度自信，把硬标签变成软标签
  - 对比损失（Contrastive Loss）：自监督学习/RAG嵌入模型的核心
  - Focal Loss：处理类别不平衡

在 AI 中的位置：
  - GPT 训练：交叉熵损失（预测下一个 token）
  - RAG 嵌入模型（BGE/E5）：对比学习损失
  - 目标检测（RetinaNet）：Focal Loss
  - 图像生成（Stable Diffusion）：MSE + 感知损失
  - PyTorch: F.mse_loss, F.cross_entropy, F.binary_cross_entropy 等
"""

import math
import random


# ========== 损失函数及其梯度 ==========

def mse(predictions, targets):
    """均方误差 (MSE)：回归任务的默认损失

    L = (1/n) * Σ(pred_i - true_i)²
    特点：对大误差二次惩罚，对异常值敏感
    对应 PyTorch: F.mse_loss(predictions, targets)
    """
    assert len(predictions) == len(targets), "predictions and targets must have the same length"
    n = len(predictions)
    total = 0.0
    for p, t in zip(predictions, targets):
        total += (p - t) ** 2
    return total / n


def mse_gradient(predictions, targets):
    """MSE 梯度：dL/dpred = 2*(pred - true) / n

    梯度与误差成线性关系——对回归是好事，对分类是坏事
    """
    assert len(predictions) == len(targets), "predictions and targets must have the same length"
    n = len(predictions)
    grads = []
    for p, t in zip(predictions, targets):
        grads.append(2.0 * (p - t) / n)
    return grads


def binary_cross_entropy(predictions, targets, eps=1e-15):
    """二元交叉熵 (BCE)：二分类任务的标配损失

    L = -(y*log(p) + (1-y)*log(1-p))
    核心机制：-log(p) 让自信的错误预测付出巨大代价
    对应 PyTorch: F.binary_cross_entropy(predictions, targets)
    """
    assert len(predictions) == len(targets), "predictions and targets must have the same length"
    n = len(predictions)
    total = 0.0
    for p, t in zip(predictions, targets):
        p_clipped = max(eps, min(1 - eps, p))  # 裁剪防止 log(0) = -inf
        total += -(t * math.log(p_clipped) + (1 - t) * math.log(1 - p_clipped))
    return total / n


def bce_gradient(predictions, targets, eps=1e-15):
    """BCE 梯度：dL/dp = -y/p + (1-y)/(1-p)

    当 y=1 且 p 接近 0 时，梯度趋近 -inf（强烈修正信号）
    """
    assert len(predictions) == len(targets), "predictions and targets must have the same length"
    n = len(predictions)
    grads = []
    for p, t in zip(predictions, targets):
        p_clipped = max(eps, min(1 - eps, p))
        grads.append((-(t / p_clipped) + (1 - t) / (1 - p_clipped)) / n)
    return grads


def softmax(logits):
    """Softmax：把 logits 变成概率分布

    所有输出在 (0,1) 之间且和为 1
    减去最大值保证数值稳定性
    对应 PyTorch: F.softmax(logits, dim)
    """
    max_val = max(logits)  # 数值稳定性技巧
    exps = [math.exp(x - max_val) for x in logits]
    total = sum(exps)
    return [e / total for e in exps]


def categorical_cross_entropy(logits, target_index, eps=1e-15):
    """多类交叉熵 (CCE)：多分类任务的标配损失

    L = -log(p_target)
    只有真实类别贡献损失
    对应 PyTorch: F.cross_entropy(logits, target_index)
    """
    probs = softmax(logits)
    p = max(eps, probs[target_index])
    return -math.log(p)


def cce_gradient(logits, target_index):
    """CCE + Softmax 的联合梯度：softmax 输出 - one-hot 目标

    优雅的简化：真实类别是 p-1，其他类别是 p
    这就是为什么 softmax 和交叉熵总是配对使用
    """
    probs = softmax(logits)
    grads = list(probs)
    grads[target_index] -= 1.0  # 真实类别的梯度减 1
    return grads


def label_smoothed_cce(logits, target_index, num_classes, alpha=0.1, eps=1e-15):
    """带标签平滑的多类交叉熵

    把硬标签 [0,0,1,0,...] 变成软标签 [0.01,0.01,0.91,0.01,...]
    防止模型过度自信（softmax 输出 1.0 需要 logit = infinity）
    用于 GPT 和大多数现代 Transformer
    对应 PyTorch: F.cross_entropy(logits, labels, label_smoothing=0.1)
    """
    probs = softmax(logits)
    loss = 0.0
    for i in range(num_classes):
        if i == target_index:
            smooth_target = 1.0 - alpha + alpha / num_classes  # 目标类别：约 0.9
        else:
            smooth_target = alpha / num_classes                 # 非目标类别：约 0.01
        p = max(eps, probs[i])
        loss += -smooth_target * math.log(p)
    return loss


def cosine_similarity(a, b):
    """余弦相似度：衡量两个向量的方向相似程度

    sim = (a · b) / (||a|| * ||||b||)
    范围 [-1, 1]，1 表示方向相同
    用于对比学习、RAG 检索、嵌入模型
    """
    assert len(a) == len(b), "vectors must have the same length"
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return dot / (norm_a * norm_b)


def contrastive_loss(anchor, positive, negatives, temperature=0.07):
    """InfoNCE 对比损失（SimCLR/CLIP 风格）

    L = -log(exp(sim(anchor, positive) / tau) / Σ exp(sim(anchor, k) / tau))
    让正对相似度最高，负对相似度最低
    temperature 越低，区分越严格（SimCLR 默认 0.07）

    在 RAG 中的位置：嵌入模型（BGE/E5/text-embedding-ada-002）都用对比学习训练
    """
    sim_pos = cosine_similarity(anchor, positive) / temperature
    sim_negs = [cosine_similarity(anchor, neg) / temperature for neg in negatives]

    # 数值稳定性：减去最大值防止 exp 溢出
    max_sim = max(sim_pos, max(sim_negs)) if sim_negs else sim_pos
    exp_pos = math.exp(sim_pos - max_sim)
    exp_negs = [math.exp(s - max_sim) for s in sim_negs]
    total_exp = exp_pos + sum(exp_negs)

    return -math.log(max(1e-15, exp_pos / total_exp))  # -log(正对在所有对中的概率)


def sigmoid(x):
    """Sigmoid 激活函数"""
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


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


class LossComparisonNetwork:
    """用不同损失函数训练的网络，对比 MSE 和 BCE 的收敛速度

    结构：输入(2) → 隐藏层(8, ReLU) → 输出(1, Sigmoid)
    对比 MSE 和 BCE 在分类任务上的表现差异
    """

    def __init__(self, loss_type="bce", hidden_size=8, lr=0.1):
        random.seed(0)
        self.loss_type = loss_type  # "mse" 或 "bce"
        self.lr = lr
        self.hidden_size = hidden_size

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def forward(self, x):
        """前向传播"""
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))  # ReLU 激活

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def backward(self, target):
        """反向传播：根据损失类型计算不同的梯度"""
        if self.loss_type == "mse":
            d_loss = 2.0 * (self.out - target)  # MSE 梯度：线性的
        else:
            eps = 1e-15
            p = max(eps, min(1 - eps, self.out))
            d_loss = -(target / p) + (1 - target) / (1 - p)  # BCE 梯度：错误时极大

        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            self.w2[i] -= self.lr * d_out * self.h[i]
            for j in range(2):
                self.w1[i][j] -= self.lr * d_h * self.x[j]
            self.b1[i] -= self.lr * d_h
        self.b2 -= self.lr * d_out

    def compute_loss(self, pred, target):
        """计算单个样本的损失"""
        if self.loss_type == "mse":
            return (pred - target) ** 2
        else:
            eps = 1e-15
            p = max(eps, min(1 - eps, pred))
            return -(target * math.log(p) + (1 - target) * math.log(1 - p))

    def train(self, data, epochs=200):
        """训练并记录每轮的损失和准确率"""
        losses = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in data:
                pred = self.forward(x)
                self.backward(y)
                total_loss += self.compute_loss(pred, y)
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            avg_loss = total_loss / len(data)
            accuracy = correct / len(data) * 100
            losses.append((avg_loss, accuracy))
            if epoch % 50 == 0 or epoch == epochs - 1:
                print(f"    Epoch {epoch:3d}: loss={avg_loss:.4f}, accuracy={accuracy:.1f}%")
        return losses


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: MSE Loss")  # 均方误差演示
    print("=" * 60)
    preds = [0.9, 0.1, 0.7, 0.4]
    targets = [1.0, 0.0, 1.0, 0.0]
    print(f"  Predictions: {preds}")
    print(f"  Targets:     {targets}")
    print(f"  MSE Loss:    {mse(preds, targets):.6f}")  # MSE 损失值
    print(f"  MSE Grads:   {[f'{g:.4f}' for g in mse_gradient(preds, targets)]}")  # MSE 梯度

    print("\n" + "=" * 60)
    print("STEP 2: Binary Cross-Entropy")  # 二元交叉熵演示
    print("=" * 60)
    print(f"  Predictions: {preds}")
    print(f"  Targets:     {targets}")
    print(f"  BCE Loss:    {binary_cross_entropy(preds, targets):.6f}")  # BCE 损失值
    print(f"  BCE Grads:   {[f'{g:.4f}' for g in bce_gradient(preds, targets)]}")  # BCE 梯度

    # 对比不同置信度下 CE 和 MSE 的惩罚力度
    print("\n  CE loss at different confidence levels (true label = 1):")
    for conf in [0.01, 0.1, 0.5, 0.9, 0.99]:
        ce = -(1.0 * math.log(max(1e-15, conf)))  # 交叉熵
        ms = (conf - 1.0) ** 2                       # MSE
        print(f"    p={conf:.2f}: CE={ce:.4f}, MSE={ms:.4f}, ratio={ce/max(0.0001, ms):.1f}x")
        # 观察：CE 在 p=0.01 时是 MSE 的 50+ 倍——对不自信的预测惩罚更重

    print("\n" + "=" * 60)
    print("STEP 3: Categorical Cross-Entropy + Softmax")  # 多类交叉熵演示
    print("=" * 60)
    logits = [2.0, 1.0, 0.1, -1.0, 3.0]
    target_idx = 4  # 真实类别是第 5 个（logit=3.0，最高）
    probs = softmax(logits)
    print(f"  Logits:  {logits}")
    print(f"  Softmax: {[f'{p:.4f}' for p in probs]}")  # 概率分布
    print(f"  Target class: {target_idx}")
    print(f"  CCE Loss: {categorical_cross_entropy(logits, target_idx):.6f}")  # 交叉熵损失
    print(f"  Gradient: {[f'{g:.4f}' for g in cce_gradient(logits, target_idx)]}")  # 梯度 = softmax - one_hot

    print("\n" + "=" * 60)
    print("STEP 4: Label Smoothing")  # 标签平滑演示
    print("=" * 60)
    num_classes = 5
    hard_loss = categorical_cross_entropy(logits, target_idx)  # 硬标签损失
    smooth_loss = label_smoothed_cce(logits, target_idx, num_classes, alpha=0.1)  # 软标签损失
    print(f"  Hard target loss:    {hard_loss:.6f}")  # 硬标签
    print(f"  Smooth target loss:  {smooth_loss:.6f}")  # 软标签
    print(f"  Smoothing increases loss by {smooth_loss - hard_loss:.6f}")
    print(f"  This prevents overconfidence by targeting 0.9 instead of 1.0")  # 目标上限 0.9 而非 1.0

    print("\n" + "=" * 60)
    print("STEP 5: Contrastive Loss")  # 对比损失演示
    print("=" * 60)
    random.seed(42)
    anchor = [random.gauss(0, 1) for _ in range(8)]       # 锚点向量
    positive = [a + random.gauss(0, 0.1) for a in anchor]  # 正对：锚点的微小扰动
    negatives = [[random.gauss(0, 1) for _ in range(8)] for _ in range(7)]  # 负对：随机向量

    loss_val = contrastive_loss(anchor, positive, negatives, temperature=0.07)
    sim_pos = cosine_similarity(anchor, positive)  # 正对相似度（应该很高）
    sim_negs = [cosine_similarity(anchor, neg) for neg in negatives]  # 负对相似度（应该很低）
    print(f"  Anchor-positive similarity: {sim_pos:.4f}")  # 正对相似度高
    print(f"  Anchor-negative similarities: {[f'{s:.4f}' for s in sim_negs]}")  # 负对相似度低
    print(f"  Contrastive loss (tau=0.07): {loss_val:.4f}")  # 低温：严格区分

    loss_easy = contrastive_loss(anchor, positive, negatives, temperature=0.5)
    print(f"  Contrastive loss (tau=0.5):  {loss_easy:.4f}")  # 高温：宽松区分
    print(f"  Lower temperature = sharper = higher loss for imperfect separation")  # 温度越低越严格

    print("\n" + "=" * 60)
    print("STEP 6: MSE vs Cross-Entropy on Classification")  # MSE vs 交叉熵分类对比
    print("=" * 60)
    data = make_circle_data()

    for loss_type in ["mse", "bce"]:
        print(f"\n--- Training with {loss_type.upper()} ---")
        net = LossComparisonNetwork(loss_type=loss_type, hidden_size=8, lr=0.1)
        results = net.train(data, epochs=200)
        final_loss, final_acc = results[-1]
        print(f"  Final: loss={final_loss:.4f}, accuracy={final_acc:.1f}%")
        # 预期：BCE 收敛更快且最终准确率更高

    print("\n=== Key Takeaway ===")  # 核心结论
    print("  Cross-entropy converges faster on classification because its")
    print("  gradient is strong when predictions are wrong and weak when correct.")
    print("  MSE gradient flattens near 0 and 1 due to sigmoid saturation.")
    # 交叉熵收敛更快：梯度在预测错误时强、正确时弱
    # MSE 在 sigmoid 饱和区梯度平坦
