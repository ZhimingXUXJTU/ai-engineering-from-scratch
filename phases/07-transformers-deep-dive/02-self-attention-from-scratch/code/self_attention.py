"""自注意力从零实现
Self-Attention from Scratch

Self-Attention 是 Transformer 的核心机制：Q*K^T 计算每个 token 对其他 token 的关注度。
理解 Q/K/V 的直觉是理解 GPT/BERT 等现代大语言模型的基础。

AI 应用：自注意力是所有 Transformer 模型（GPT、BERT、T5、ViT 等）的核心组件。
理解其数学原理对于模型调试、注意力可视化和架构创新至关重要。
对应 PyTorch 的 nn.MultiheadAttention。
"""

import numpy as np


def softmax(x):
    """数值稳定的 softmax 实现。
    Numerically stable softmax: subtract max to prevent overflow.

    AI 应用：softmax 将原始分数转换为概率分布，是注意力机制的核心归一化步骤。
    减去最大值是为了防止指数溢出（数值稳定性技巧）。
    """
    shifted = x - np.max(x, axis=-1, keepdims=True)  # 减去最大值防止溢出
    exp_x = np.exp(shifted)  # 计算指数
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)  # 归一化为概率分布


def scaled_dot_product_attention(Q, K, V):
    """缩放点积注意力：Transformer 的核心计算。
    Scaled dot-product attention: the core computation of Transformer.

    公式：Attention(Q, K, V) = softmax(Q @ K^T / sqrt(dk)) @ V

    AI 应用：这是 GPT/BERT 中每个注意力层执行的核心操作。
    缩放因子 1/sqrt(dk) 防止高维时 softmax 饱和。

    参数：
        Q: 查询矩阵，形状 (n, dk)
        K: 键矩阵，形状 (n, dk)
        V: 值矩阵，形状 (n, dv)
    返回：
        output: 注意力输出，形状 (n, dv)
        weights: 注意力权重矩阵，形状 (n, n)
    """
    dk = Q.shape[-1]  # 键向量的维度
    scores = Q @ K.T / np.sqrt(dk)  # 计算缩放点积分数
    weights = softmax(scores)  # softmax 归一化为权重
    output = weights @ V  # 加权求和得到输出
    return output, weights


class SelfAttention:
    """单头自注意力模块。
    Single-head self-attention module with learned projections.

    将输入通过三个独立的线性投影（Wq, Wk, Wv）得到 Q、K、V，
    然后执行缩放点积注意力。

    AI 应用：这是 Transformer 编码器/解码器中注意力层的简化版本。
    实际模型使用多头版本（见 MultiHeadSelfAttention）。
    """

    def __init__(self, d_model, dk, dv, seed=42):
        """初始化自注意力模块。
        Args:
            d_model: 输入嵌入维度
            dk: 查询/键的投影维度
            dv: 值的投影维度
            seed: 随机种子
        """
        rng = np.random.default_rng(seed)
        # Xavier 初始化：防止梯度消失/爆炸
        scale_qk = np.sqrt(2.0 / (d_model + dk))
        self.Wq = rng.normal(0, scale_qk, (d_model, dk))  # 查询投影矩阵
        self.Wk = rng.normal(0, scale_qk, (d_model, dk))  # 键投影矩阵
        scale_v = np.sqrt(2.0 / (d_model + dv))
        self.Wv = rng.normal(0, scale_v, (d_model, dv))  # 值投影矩阵
        self.dk = dk

    def forward(self, X):
        """前向传播：计算自注意力。
        Args:
            X: 输入矩阵，形状 (n, d_model)
        Returns:
            output: 注意力输出
            weights: 注意力权重矩阵
        """
        Q = X @ self.Wq  # 投影到查询空间
        K = X @ self.Wk  # 投影到键空间
        V = X @ self.Wv  # 投影到值空间
        return scaled_dot_product_attention(Q, K, V)


class MultiHeadSelfAttention:
    """多头自注意力模块。
    Multi-head self-attention: runs multiple attention heads in parallel,
    then concatenates and projects the results.

    AI 应用：多头注意力让模型同时关注不同类型的关系——
    一个头可能关注语法关系，另一个关注语义关系，还有一个关注位置关系。
    这是 GPT、BERT 等模型中实际使用的注意力形式。
    """

    def __init__(self, d_model, n_heads, seed=42):
        """初始化多头注意力。
        Args:
            d_model: 输入嵌入维度（必须能被 n_heads 整除）
            n_heads: 注意力头的数量
            seed: 随机种子
        """
        assert d_model % n_heads == 0  # d_model 必须能被头数整除
        self.n_heads = n_heads
        self.dk = d_model // n_heads  # 每个头的键维度
        self.dv = d_model // n_heads  # 每个头的值维度
        # 创建多个独立的注意力头
        self.heads = [
            SelfAttention(d_model, self.dk, self.dv, seed=seed + i)
            for i in range(n_heads)
        ]
        # 输出投影矩阵：将多头结果映射回 d_model 维度
        rng = np.random.default_rng(seed + n_heads)
        scale = np.sqrt(2.0 / (d_model + d_model))
        self.Wo = rng.normal(0, scale, (n_heads * self.dv, d_model))

    def forward(self, X):
        """前向传播：并行计算多头注意力。
        Args:
            X: 输入矩阵，形状 (n, d_model)
        Returns:
            output: 多头注意力输出，形状 (n, d_model)
            all_weights: 每个头的注意力权重列表
        """
        head_outputs = []
        all_weights = []
        for head in self.heads:
            out, w = head.forward(X)  # 每个头独立计算注意力
            head_outputs.append(out)
            all_weights.append(w)
        # 拼接所有头的输出
        concatenated = np.concatenate(head_outputs, axis=-1)
        # 通过输出投影矩阵映射回 d_model 维度
        output = concatenated @ self.Wo
        return output, all_weights


def print_attention_matrix(weights, tokens):
    """打印注意力权重矩阵。"""
    print(f"\n{'':>6}", end="")
    for token in tokens:
        print(f"{token:>6}", end="")
    print()
    for i, token in enumerate(tokens):
        print(f"{token:>6}", end="")
        for j in range(len(tokens)):
            print(f"{weights[i][j]:6.3f}", end="")
        print()


def ascii_heatmap(weights, tokens, chars=" ░▒▓█"):
    """用 ASCII 字符绘制注意力热力图。
    ASCII heatmap visualization of attention weights.
    越深的字符表示越高的注意力权重。
    """
    print(f"\n{'':>6}", end="")
    for t in tokens:
        print(f"{t:>6}", end="")
    print()
    w_max = weights.max()
    for i in range(len(tokens)):
        print(f"{tokens[i]:>6}", end="")
        for j in range(len(tokens)):
            level = int(weights[i][j] * (len(chars) - 1) / w_max)
            level = min(level, len(chars) - 1)
            print(f"{'  ' + chars[level] + '   '}", end="")
        print()


if __name__ == "__main__":
    # 演示：在简单句子上运行自注意力和多头自注意力
    sentence = ["The", "cat", "sat", "on", "the", "mat"]
    n_tokens = len(sentence)
    d_model = 16  # 嵌入维度
    dk = 8  # 查询/键维度
    dv = 8  # 值维度

    rng = np.random.default_rng(42)
    X = rng.normal(0, 1, (n_tokens, d_model))  # 随机生成伪嵌入

    # ===== 单头自注意力演示 =====
    print("=" * 60)
    print("SELF-ATTENTION FROM SCRATCH")
    print("=" * 60)

    print(f"\nSentence: {' '.join(sentence)}")
    print(f"Tokens: {n_tokens}, d_model: {d_model}, dk: {dk}, dv: {dv}")
    print(f"Input shape: {X.shape}")

    attn = SelfAttention(d_model, dk, dv, seed=42)
    output, weights = attn.forward(X)

    print(f"\nOutput shape: {output.shape}")
    print("\nAttention weights:")
    print_attention_matrix(weights, sentence)

    print("\nASCII heatmap (darker = higher attention):")
    ascii_heatmap(weights, sentence)

    # ===== 多头自注意力演示 =====
    print("\n" + "=" * 60)
    print("MULTI-HEAD SELF-ATTENTION")
    print("=" * 60)

    n_heads = 2
    mha = MultiHeadSelfAttention(d_model, n_heads, seed=42)
    mha_output, head_weights = mha.forward(X)

    print(f"\nHeads: {n_heads}")
    print(f"Output shape: {mha_output.shape}")

    for h, hw in enumerate(head_weights):
        print(f"\nHead {h + 1} attention weights:")
        print_attention_matrix(hw, sentence)

    # ===== Softmax 数值稳定性演示 =====
    print("\n" + "=" * 60)
    print("SOFTMAX DEMO")
    print("=" * 60)

    logits = np.array([2.0, 1.0, 0.1])
    probs = softmax(logits)
    print(f"\nLogits:  {logits}")
    print(f"Softmax: {probs.round(4)}")
    print(f"Sum:     {probs.sum():.4f}")

    # 演示大数值下的数值稳定性
    large_logits = np.array([100.0, 200.0, 300.0])
    probs_large = softmax(large_logits)
    print(f"\nLarge logits:  {large_logits}")
    print(f"Softmax:       {probs_large.round(4)}")
    print(f"Sum:           {probs_large.sum():.4f}")
    print("(Numerically stable - no overflow)")
