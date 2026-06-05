"""完整 Transformer：编码器 + 解码器块（纯标准库）
The Full Transformer: Encoder + Decoder blocks in pure stdlib.

本模块从零实现完整的 Transformer 架构，包括：
- LayerNorm vs RMSNorm（两种归一化方案对比）
- ReLU-FFN vs SwiGLU FFN（两种前馈网络对比）
- 编码器块（双向注意力）vs 解码器块（因果注意力 + 交叉注意力）
- 前归一化接线方式（2026 年默认）

AI 应用：这是所有 Transformer 模型的基础架构。
理解编码器/解码器块的结构是理解 BERT、GPT、T5 等模型的前提。
2026 年的现代块使用 RMSNorm + SwiGLU + Pre-norm + RoPE + GQA。
"""

import math
import random
from typing import List


class Matrix:
    """行优先二维浮点矩阵。仅实现注意力计算所需的最少操作。"""
    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows, cols, fill=0.0, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data if data is not None else [fill] * (rows * cols)

    def get(self, i, j):
        return self.data[i * self.cols + j]

    def set(self, i, j, v):
        self.data[i * self.cols + j] = v

    def row(self, i):
        return self.data[i * self.cols:(i + 1) * self.cols]

    def copy(self):
        """创建矩阵的深拷贝。"""
        return Matrix(self.rows, self.cols, data=list(self.data))


def randn(rows, cols, rng, scale=None):
    """生成 Xavier 初始化的随机矩阵。"""
    if scale is None:
        scale = math.sqrt(2.0 / (rows + cols))
    m = Matrix(rows, cols)
    for i in range(rows * cols):
        m.data[i] = rng.gauss(0.0, scale)
    return m


def matmul(A, B):
    """矩阵乘法 A @ B。"""
    out = Matrix(A.rows, B.cols)
    for i in range(A.rows):
        for k in range(A.cols):
            aik = A.get(i, k)
            if aik == 0.0:
                continue  # 跳过零值以加速
            base_i = i * B.cols
            base_k = k * B.cols
            for j in range(B.cols):
                out.data[base_i + j] += aik * B.data[base_k + j]
    return out


def transpose(A):
    """矩阵转置。"""
    out = Matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            out.set(j, i, A.get(i, j))
    return out


def add(A, B):
    """矩阵逐元素相加（残差连接的核心操作）。"""
    assert (A.rows, A.cols) == (B.rows, B.cols)
    return Matrix(A.rows, A.cols, data=[a + b for a, b in zip(A.data, B.data)])


def softmax_rows(A, mask=None):
    """逐行 softmax，支持因果掩码。
    Row-wise softmax with optional causal masking.
    """
    out = Matrix(A.rows, A.cols)
    for i in range(A.rows):
        row = A.row(i)
        if mask is not None:
            row = [row[j] if not mask[i][j] else float("-inf") for j in range(A.cols)]
        m = max(v for v in row if v != float("-inf"))
        exps = [math.exp(v - m) if v != float("-inf") else 0.0 for v in row]
        s = sum(exps)
        for j, e in enumerate(exps):
            out.set(i, j, e / s if s > 0 else 0.0)
    return out


def layer_norm(X, eps=1e-5):
    """LayerNorm：减去均值，除以标准差（2017 年原版 Transformer 使用）。
    Layer Normalization: subtract mean, divide by std.
    """
    out = Matrix(X.rows, X.cols)
    for i in range(X.rows):
        row = X.row(i)
        mean = sum(row) / len(row)  # 计算均值
        var = sum((v - mean) ** 2 for v in row) / len(row)  # 计算方差
        denom = math.sqrt(var + eps)
        for j in range(X.cols):
            out.set(i, j, (row[j] - mean) / denom)
    return out


def rms_norm(X, eps=1e-6):
    """RMSNorm：除以均方根，不减均值（2026 年现代 Transformer 使用）。
    Root Mean Square Layer Normalization: divide by RMS, no mean subtraction.
    比 LayerNorm 少一次减法操作，经验上至少同样稳定。
    """
    out = Matrix(X.rows, X.cols)
    for i in range(X.rows):
        row = X.row(i)
        rms = math.sqrt(sum(v * v for v in row) / len(row) + eps)
        for j in range(X.cols):
            out.set(i, j, row[j] / rms)
    return out


def silu(x):
    """SiLU (Swish) 激活函数：x * sigmoid(x)。
    SwiGLU FFN 的核心激活函数。
    """
    return x / (1.0 + math.exp(-x))


def ffn_swiglu(X, W1, W2, W3):
    """SwiGLU 前馈网络：SiLU(X @ W1) ⊙ (X @ W3) → @ W2。
    SwiGLU FFN: gate mechanism with three weight matrices.

    AI 应用：Llama、PaLM、Qwen 等现代模型使用 SwiGLU 替代 ReLU/GELU，
    在困惑度上提升约 0.5 个点。扩展比从 4x 降到 2.6x 以补偿参数量。
    """
    h1 = matmul(X, W1)  # 第一个投影
    h3 = matmul(X, W3)  # 门控投影
    gated = Matrix(h1.rows, h1.cols)
    for i in range(len(h1.data)):
        gated.data[i] = silu(h1.data[i]) * h3.data[i]  # 门控：SiLU * 门
    return matmul(gated, W2)  # 输出投影


def ffn_relu(X, W1, W2):
    """ReLU 前馈网络：max(0, X @ W1) @ W2（2017 年原版 Transformer 使用）。"""
    h = matmul(X, W1)
    for i in range(len(h.data)):
        if h.data[i] < 0:
            h.data[i] = 0.0  # ReLU 激活
    return matmul(h, W2)


def scaled_dot_product_attention(Q, K, V, causal=False):
    """缩放点积注意力，支持因果掩码。
    Scaled dot-product attention with optional causal masking.
    """
    dk = Q.cols
    scores = matmul(Q, transpose(K))  # Q @ K^T
    inv = 1.0 / math.sqrt(dk)  # 缩放因子
    for i in range(len(scores.data)):
        scores.data[i] *= inv
    mask = None
    if causal:
        # 因果掩码：屏蔽未来位置（j > i 的位置设为 -inf）
        mask = [[j > i for j in range(scores.cols)] for i in range(scores.rows)]
    w = softmax_rows(scores, mask=mask)
    return matmul(w, V)


def multi_head_attention(X, Wq, Wk, Wv, Wo, n_heads, causal=False, kv_source=None):
    """多头注意力，支持因果掩码和交叉注意力。
    Multi-head attention with optional causal mask and cross-attention.

    当 kv_source 不为 None 时，实现交叉注意力（K/V 来自编码器输出）。
    """
    Q = matmul(X, Wq)
    kv_input = kv_source if kv_source is not None else X  # 交叉注意力时 K/V 来自编码器
    K = matmul(kv_input, Wk)
    V = matmul(kv_input, Wv)
    d_head = Q.cols // n_heads
    head_outs = []
    for h in range(n_heads):
        Qh = Matrix(Q.rows, d_head, data=[Q.get(i, h * d_head + j) for i in range(Q.rows) for j in range(d_head)])
        Kh = Matrix(K.rows, d_head, data=[K.get(i, h * d_head + j) for i in range(K.rows) for j in range(d_head)])
        Vh = Matrix(V.rows, d_head, data=[V.get(i, h * d_head + j) for i in range(V.rows) for j in range(d_head)])
        head_outs.append(scaled_dot_product_attention(Qh, Kh, Vh, causal=causal))
    concat = Matrix(X.rows, Q.cols)
    for h, H in enumerate(head_outs):
        for i in range(H.rows):
            for j in range(d_head):
                concat.set(i, h * d_head + j, H.get(i, j))
    return matmul(concat, Wo)


class BlockParams:
    """一个编码器或解码器块的所有权重参数。
    All weights for one encoder or decoder block.

    包含自注意力权重（Wq, Wk, Wv, Wo）、FFN 权重（W1, W2, W3）、
    以及交叉注意力权重（Wq_x, Wk_x, Wv_x, Wo_x，仅解码器使用）。
    """
    def __init__(self, d, n_heads, ffn_expansion, rng, use_swiglu=True):
        self.d = d
        self.n_heads = n_heads
        self.use_swiglu = use_swiglu
        # 自注意力权重
        self.Wq = randn(d, d, rng)
        self.Wk = randn(d, d, rng)
        self.Wv = randn(d, d, rng)
        self.Wo = randn(d, d, rng)
        # FFN 权重
        h = int(d * ffn_expansion)
        if use_swiglu:
            self.W1 = randn(d, h, rng)  # SwiGLU 需要三个权重矩阵
            self.W2 = randn(h, d, rng)
            self.W3 = randn(d, h, rng)
        else:
            self.W1 = randn(d, h, rng)  # ReLU FFN 只需两个权重矩阵
            self.W2 = randn(h, d, rng)
        # 交叉注意力权重（仅解码器使用）
        self.Wq_x = randn(d, d, rng)
        self.Wk_x = randn(d, d, rng)
        self.Wv_x = randn(d, d, rng)
        self.Wo_x = randn(d, d, rng)


def encoder_block(x, p):
    """编码器块：Pre-norm + 双向自注意力 + Pre-norm + FFN。
    Encoder block: pre-norm self-attention + pre-norm FFN, both with residual.

    AI 应用：BERT、DeBERTa 等模型使用此结构。
    双向注意力让每个位置能看到所有其他位置。
    """
    # 子层 1：前归一化 + 自注意力 + 残差连接
    h = rms_norm(x)
    a = multi_head_attention(h, p.Wq, p.Wk, p.Wv, p.Wo, p.n_heads)
    x = add(x, a)  # 残差连接：x + MHA(x)
    # 子层 2：前归一化 + FFN + 残差连接
    h = rms_norm(x)
    f = ffn_swiglu(h, p.W1, p.W2, p.W3) if p.use_swiglu else ffn_relu(h, p.W1, p.W2)
    return add(x, f)  # 残差连接：x + FFN(x)


def decoder_block(x, enc_out, p):
    """解码器块：Pre-norm + 因果自注意力 + Pre-norm + 交叉注意力 + Pre-norm + FFN。
    Decoder block: masked self-attention + cross-attention + FFN, all with residual.

    AI 应用：GPT 省略交叉注意力，只有因果自注意力 + FFN。
    T5/BART/Whisper 使用完整的三子层结构。
    交叉注意力是信息从编码器流向解码器的唯一通道。
    """
    # 子层 1：前归一化 + 因果自注意力 + 残差连接
    h = rms_norm(x)
    a = multi_head_attention(h, p.Wq, p.Wk, p.Wv, p.Wo, p.n_heads, causal=True)
    x = add(x, a)
    # 子层 2：前归一化 + 交叉注意力 + 残差连接（Q 来自解码器，K/V 来自编码器）
    h = rms_norm(x)
    a = multi_head_attention(h, p.Wq_x, p.Wk_x, p.Wv_x, p.Wo_x, p.n_heads, kv_source=enc_out)
    x = add(x, a)
    # 子层 3：前归一化 + FFN + 残差连接
    h = rms_norm(x)
    f = ffn_swiglu(h, p.W1, p.W2, p.W3) if p.use_swiglu else ffn_relu(h, p.W1, p.W2)
    return add(x, f)


def main():
    """主函数：演示 2 层编码器 + 2 层解码器的 Transformer 前向传播。"""
    rng = random.Random(42)
    d = 8  # 嵌入维度
    n_heads = 2  # 注意力头数
    ffn_expansion = 2.0  # FFN 扩展比
    src_len = 6  # 源序列长度
    tgt_len = 5  # 目标序列长度

    # 生成随机输入
    src = randn(src_len, d, rng, scale=0.5)  # 源序列嵌入
    tgt = randn(tgt_len, d, rng, scale=0.5)  # 目标序列嵌入

    # 创建 2 层编码器和 2 层解码器
    enc_params = [BlockParams(d, n_heads, ffn_expansion, rng) for _ in range(2)]
    dec_params = [BlockParams(d, n_heads, ffn_expansion, rng) for _ in range(2)]

    # 编码器前向传播
    enc_out = src
    for p in enc_params:
        enc_out = encoder_block(enc_out, p)

    # 解码器前向传播
    dec_out = tgt
    for p in dec_params:
        dec_out = decoder_block(dec_out, enc_out, p)

    print("=== full transformer forward pass ===")
    print(f"source shape:           ({src.rows}, {src.cols})")
    print(f"encoder output shape:   ({enc_out.rows}, {enc_out.cols})")
    print(f"target shape:           ({tgt.rows}, {tgt.cols})")
    print(f"decoder output shape:   ({dec_out.rows}, {dec_out.cols})")
    print()
    print("first 3 cells of encoder output:")
    for i in range(3):
        print("  " + "  ".join(f"{v:+.3f}" for v in enc_out.row(i)[:4]))
    print()
    print("first 3 cells of decoder output:")
    for i in range(3):
        print("  " + "  ".join(f"{v:+.3f}" for v in dec_out.row(i)[:4]))
    print()
    print("stack: 2-layer encoder + 2-layer decoder, pre-norm, RMSNorm, SwiGLU.")
    print("this is the 2026 block skeleton (minus RoPE).")
    # 总结：2 层编码器 + 2 层解码器，前归一化，RMSNorm，SwiGLU。
    # 这是 2026 年的块骨架（除了 RoPE）。


if __name__ == "__main__":
    main()
