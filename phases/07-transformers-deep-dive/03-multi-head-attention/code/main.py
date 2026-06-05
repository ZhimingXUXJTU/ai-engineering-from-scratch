"""多头注意力从零实现（纯标准库）
Multi-head attention from scratch in pure stdlib.

本模块用纯 Python 标准库实现多头注意力（MHA）和分组查询注意力（GQA）。
不依赖 numpy 或 torch，使用自定义 Matrix 类实现所有矩阵操作。

AI 应用：多头注意力是所有 Transformer 模型的核心组件。
GPT-3 有 96 个注意力头，Llama 3 使用 GQA（64 个查询头，8 个 KV 头）。
理解多头机制的实现对于模型架构设计和推理优化至关重要。

Demonstrates: split heads, per-head scaled dot-product attention,
combine heads, output projection, and a Grouped-Query variant.
"""

import math
import random
from typing import List


class Matrix:
    """行优先二维浮点矩阵。仅实现注意力计算所需的最少操作。
    Row-major 2D matrix of floats. Just enough ops for attention.

    AI 应用：这是简化版的张量实现，帮助理解 GPU 上批量矩阵乘法的本质。
    """
    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows: int, cols: int, fill: float = 0.0, data=None):
        self.rows = rows
        self.cols = cols
        if data is not None:
            self.data = data
        else:
            self.data = [fill] * (rows * cols)

    def get(self, i: int, j: int) -> float:
        """获取第 i 行第 j 列的元素。"""
        return self.data[i * self.cols + j]

    def set(self, i: int, j: int, v: float) -> None:
        """设置第 i 行第 j 列的元素。"""
        self.data[i * self.cols + j] = v

    def row(self, i: int) -> List[float]:
        """获取第 i 行的所有元素。"""
        return self.data[i * self.cols:(i + 1) * self.cols]


def randn_matrix(rows, cols, rng, scale=None):
    """生成 Xavier 初始化的随机矩阵。
    Generate a random matrix with Xavier-like initialization.
    """
    if scale is None:
        scale = math.sqrt(2.0 / (rows + cols))  # Xavier 缩放因子
    m = Matrix(rows, cols)
    for i in range(rows * cols):
        m.data[i] = rng.gauss(0.0, scale)
    return m


def matmul(A: Matrix, B: Matrix) -> Matrix:
    """矩阵乘法 A @ B。
    Matrix multiplication A @ B.

    AI 应用：这是注意力计算的核心操作，GPU 上对应 cuBLAS 的 GEMM 操作。
    """
    assert A.cols == B.rows, f"{A.cols} vs {B.rows}"
    out = Matrix(A.rows, B.cols)
    for i in range(A.rows):
        for k in range(A.cols):
            aik = A.get(i, k)
            if aik == 0.0:
                continue  # 跳过零值以加速计算
            base_i = i * B.cols
            base_k = k * B.cols
            for j in range(B.cols):
                out.data[base_i + j] += aik * B.data[base_k + j]
    return out


def transpose(A: Matrix) -> Matrix:
    """矩阵转置。"""
    out = Matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            out.set(j, i, A.get(i, j))
    return out


def softmax_rows(A: Matrix) -> Matrix:
    """逐行 softmax，带数值稳定性（减去最大值）。
    Row-wise softmax with numerical stability.
    """
    out = Matrix(A.rows, A.cols)
    for i in range(A.rows):
        row = A.row(i)
        m = max(row)  # 减去最大值防止溢出
        exps = [math.exp(x - m) for x in row]
        s = sum(exps)
        for j, e in enumerate(exps):
            out.set(i, j, e / s)
    return out


def scaled_dot_product_attention(Q: Matrix, K: Matrix, V: Matrix):
    """缩放点积注意力：softmax(QK^T / sqrt(dk)) @ V。
    Scaled dot-product attention.

    AI 应用：这是每个注意力头内部执行的核心计算。
    缩放因子 1/sqrt(dk) 防止高维时 softmax 饱和。
    """
    dk = Q.cols
    scale = 1.0 / math.sqrt(dk)  # 缩放因子
    scores = matmul(Q, transpose(K))  # Q @ K^T
    for i in range(scores.rows * scores.cols):
        scores.data[i] *= scale  # 除以 sqrt(dk)
    weights = softmax_rows(scores)  # softmax 归一化
    out = matmul(weights, V)  # 加权求和
    return out, weights


def split_heads(X: Matrix, n_heads: int) -> List[Matrix]:
    """将输入矩阵按头数拆分为多个子矩阵。
    Split input into n_heads sub-matrices along the embedding dimension.

    等价于 numpy 的 X.reshape(n, n_heads, d_head).transpose(1, 0, 2)。
    """
    assert X.cols % n_heads == 0, "d_model not divisible by n_heads"
    d_head = X.cols // n_heads
    heads = []
    for h in range(n_heads):
        H = Matrix(X.rows, d_head)
        for i in range(X.rows):
            for j in range(d_head):
                H.set(i, j, X.get(i, h * d_head + j))
        heads.append(H)
    return heads


def combine_heads(heads: List[Matrix]) -> Matrix:
    """将多个头的输出拼接回一个大矩阵。
    Concatenate head outputs back into a single matrix.

    等价于 numpy 的 H.transpose(1, 0, 2).reshape(n, d_model)。
    """
    n = heads[0].rows
    d_head = heads[0].cols
    d_model = d_head * len(heads)
    out = Matrix(n, d_model)
    for h, H in enumerate(heads):
        for i in range(n):
            for j in range(d_head):
                out.set(i, h * d_head + j, H.get(i, j))
    return out


def multi_head_attention(X: Matrix, Wq, Wk, Wv, Wo, n_heads: int):
    """多头注意力（MHA）：并行运行多个注意力头，拼接并投影。
    Multi-head attention: split → attend → concat → project.

    AI 应用：这是 GPT-2、BERT 等模型中使用的标准多头注意力。
    每个头在不同子空间中学习不同的关系模式。
    """
    Q = matmul(X, Wq)  # 查询投影
    K = matmul(X, Wk)  # 键投影
    V = matmul(X, Wv)  # 值投影
    Qh = split_heads(Q, n_heads)  # 拆分查询
    Kh = split_heads(K, n_heads)  # 拆分键
    Vh = split_heads(V, n_heads)  # 拆分值
    head_outs = []
    per_head_weights = []
    for q, k, v in zip(Qh, Kh, Vh):
        o, w = scaled_dot_product_attention(q, k, v)  # 每个头独立计算注意力
        head_outs.append(o)
        per_head_weights.append(w)
    concat = combine_heads(head_outs)  # 拼接所有头的输出
    return matmul(concat, Wo), per_head_weights  # 输出投影


def grouped_query_attention(X: Matrix, Wq, Wk, Wv, Wo, n_heads: int, n_kv_heads: int):
    """分组查询注意力（GQA）：KV 头数少于查询头数，KV 被重复以匹配。
    Grouped-Query Attention: K and V have fewer heads, repeated to match Q.

    AI 应用：Llama 2/3、Mistral、Qwen 等模型使用 GQA 来减少 KV 缓存大小。
    例如 Llama 3 70B 使用 64 个查询头和 8 个 KV 头，缓存缩减 8 倍。
    """
    Q = matmul(X, Wq)
    K = matmul(X, Wk)
    V = matmul(X, Wv)
    Qh = split_heads(Q, n_heads)  # 查询头：n_heads 个
    Kh_small = split_heads(K, n_kv_heads)  # KV 头：n_kv_heads 个（更少）
    Vh_small = split_heads(V, n_kv_heads)
    repeat = n_heads // n_kv_heads  # 每个 KV 头需要被重复的次数
    Kh = [Kh_small[i // repeat] for i in range(n_heads)]  # 重复 KV 头以匹配查询头
    Vh = [Vh_small[i // repeat] for i in range(n_heads)]
    head_outs = []
    for q, k, v in zip(Qh, Kh, Vh):
        o, _ = scaled_dot_product_attention(q, k, v)
        head_outs.append(o)
    concat = combine_heads(head_outs)
    return matmul(concat, Wo)


def print_matrix(name, M: Matrix, width=6, prec=3):
    """打印矩阵内容。"""
    print(f"-- {name} ({M.rows}x{M.cols}) --")
    for i in range(M.rows):
        row = M.row(i)
        print("  " + "  ".join(f"{v:>{width}.{prec}f}" for v in row))


def main():
    """主函数：演示多头注意力和 GQA。"""
    rng = random.Random(42)
    tokens = ["the", "cat", "sat", "on", "the", "mat"]
    n = len(tokens)
    d_model = 8
    n_heads = 2

    # 生成随机输入和权重矩阵
    X = randn_matrix(n, d_model, rng, scale=1.0)
    Wq = randn_matrix(d_model, d_model, rng)
    Wk = randn_matrix(d_model, d_model, rng)
    Wv = randn_matrix(d_model, d_model, rng)
    Wo = randn_matrix(d_model, d_model, rng)

    # ===== 多头注意力演示 =====
    out, weights = multi_head_attention(X, Wq, Wk, Wv, Wo, n_heads=n_heads)

    print(f"=== multi-head attention: {n_heads} heads, d_model={d_model}, d_head={d_model // n_heads} ===")
    print(f"input  shape: ({X.rows}, {X.cols})")
    print(f"output shape: ({out.rows}, {out.cols})")
    print()
    for h, W in enumerate(weights):
        print(f"-- head {h} attention weights --")
        print(f"{'':>6}", end="")
        for t in tokens:
            print(f"{t:>7}", end="")
        print()
        for i in range(n):
            print(f"{tokens[i]:>6}", end="")
            for j in range(n):
                print(f"{W.get(i, j):>7.3f}", end="")
            print()
        print()

    # ===== GQA 演示：4 个查询头，2 个 KV 头 =====
    d_model = 8
    n_heads = 4
    n_kv = 2
    Wq = randn_matrix(d_model, d_model, rng)
    Wk = randn_matrix(d_model, (d_model // n_heads) * n_kv, rng)  # KV 维度更小
    Wv = randn_matrix(d_model, (d_model // n_heads) * n_kv, rng)
    Wo = randn_matrix(d_model, d_model, rng)
    out_gqa = grouped_query_attention(X, Wq, Wk, Wv, Wo, n_heads=n_heads, n_kv_heads=n_kv)
    print(f"=== GQA: {n_heads} Q heads, {n_kv} KV heads ===")
    print(f"output shape: ({out_gqa.rows}, {out_gqa.cols})")
    # 计算 KV 缓存大小对比
    kv_cache_full = n_heads * n * (d_model // n_heads) * 2  # MHA 的 KV 缓存大小
    kv_cache_gqa = n_kv * n * (d_model // n_heads) * 2  # GQA 的 KV 缓存大小
    print(f"KV cache elements (MHA):  {kv_cache_full}")
    print(f"KV cache elements (GQA):  {kv_cache_gqa}  ({kv_cache_full // kv_cache_gqa}x smaller)")


if __name__ == "__main__":
    main()
