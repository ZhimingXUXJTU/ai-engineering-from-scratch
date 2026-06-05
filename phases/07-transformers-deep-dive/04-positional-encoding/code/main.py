"""位置编码 — 正弦编码、RoPE、ALiBi
Positional Encoding — Sinusoidal, RoPE, ALiBi.

本模块用纯标准库实现三种主流位置编码方案：
1. 绝对正弦编码（Vaswani 2017）— 原始 Transformer 使用
2. RoPE 旋转位置嵌入（Su 2021）— Llama/GPT-NeoX 使用
3. ALiBi 线性偏置注意力（Press 2022）— 支持超长序列外推

AI 应用：位置编码是所有 Transformer 模型的必备组件。
选择合适的位置编码直接影响模型的上下文长度能力。
RoPE 是 2026 年的主流选择，支持通过 base 缩放扩展上下文。

Pure stdlib. Each encoding scheme shipped as a small reusable function.
Demos the relative-distance property of RoPE numerically.
"""

import math
import random


def sinusoidal_pe(n, d, base=10000.0):
    """绝对正弦位置编码（Vaswani 2017）。
    Absolute sinusoidal positional encoding.

    对每个位置 pos 和维度 i，计算 sin/cos 波形。
    不同维度使用不同的频率，形成唯一的位置"指纹"。

    AI 应用：原始 Transformer 和早期 BERT 使用此编码。
    缺点是无法外推到训练时未见过的位置。

    Args:
        n: 序列长度
        d: 嵌入维度
        base: 频率基数（默认 10000）
    Returns:
        位置编码矩阵，形状 (n, d)
    """
    pe = [[0.0] * d for _ in range(n)]
    for pos in range(n):
        for i in range(d // 2):
            theta = pos / (base ** (2 * i / d))  # 角度与位置和维度相关
            pe[pos][2 * i] = math.sin(theta)      # 偶数维度用 sin
            pe[pos][2 * i + 1] = math.cos(theta)  # 奇数维度用 cos
    return pe


def apply_rope(x, pos, base=10000.0):
    """旋转位置嵌入（RoPE）：按位置旋转 Q/K 向量的每一对维度。
    Rotary Position Embedding: rotate even/odd pairs of x by angle pos * theta_i.

    核心思想：对 Q 和 K 做位置相关的旋转，使得 Q_m · K_n 的点积
    自然编码相对距离 (m-n)，而非绝对位置。

    AI 应用：Llama 2/3/4、Qwen、Mistral、DeepSeek 等主流模型均使用 RoPE。
    通过调整 base 参数可实现长上下文外推（如 Llama 3 从 8K 到 128K）。

    Args:
        x: 输入向量（Q 或 K）
        pos: 位置索引
        base: 频率基数（默认 10000，增大可支持更长上下文）
    Returns:
        旋转后的向量
    """
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))  # 旋转角度与位置成正比
        c = math.cos(theta)  # cos 分量
        s = math.sin(theta)  # sin 分量
        a = x[2 * i]      # 偶数维度
        b = x[2 * i + 1]  # 奇数维度
        # 二维旋转矩阵 [cos, -sin; sin, cos] @ [a, b]^T
        out[2 * i] = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out


def dot(a, b):
    """向量点积。"""
    return sum(x * y for x, y in zip(a, b))


def alibi_slopes(n_heads):
    """计算 ALiBi 每个头的斜率。
    Compute per-head slopes for ALiBi.

    斜率按几何级数递减：slope_h = 2^(-8h/H)。
    头 0 的斜率最大（最强距离惩罚），头 H-1 最小。

    AI 应用：ALiBi 的斜率设计让不同头关注不同范围的依赖关系。
    """
    return [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]


def alibi_bias(n_heads, seq_len, causal=True):
    """生成 ALiBi 偏置矩阵。
    Generate ALiBi bias matrices for all heads.

    偏置为 -m_h * |i - j|，距离越远惩罚越大。
    可选因果掩码：将未来位置设为 -inf。

    AI 应用：ALiBi 不需要位置嵌入，直接修改注意力分数。
    支持训练短序列、推理长序列（长度外推）。

    Args:
        n_heads: 头数
        seq_len: 序列长度
        causal: 是否应用因果掩码
    Returns:
        偏置矩阵列表，每个头一个 (seq_len, seq_len) 矩阵
    """
    slopes = alibi_slopes(n_heads)
    out = []
    for m in slopes:
        head_bias = []
        for i in range(seq_len):
            row = []
            for j in range(seq_len):
                if causal and j > i:
                    row.append(float("-inf"))  # 因果掩码：屏蔽未来位置
                else:
                    row.append(-m * abs(i - j))  # 距离惩罚：越远越负
            head_bias.append(row)
        out.append(head_bias)
    return out


def demo_sinusoidal():
    """演示正弦位置编码。"""
    print("=== sinusoidal positional encoding ===")
    pe = sinusoidal_pe(n=8, d=8)
    print("first 4 positions, first 4 dims:")
    for pos in range(4):
        print(f"  pos={pos}: " + "  ".join(f"{v:+.3f}" for v in pe[pos][:4]))
    print()


def demo_rope_relative():
    """演示 RoPE 的相对距离属性：点积只取决于相对距离。"""
    print("=== RoPE: dot product depends only on relative distance ===")
    rng = random.Random(0)
    d = 16
    q = [rng.gauss(0, 1) for _ in range(d)]
    k = [rng.gauss(0, 1) for _ in range(d)]

    # 不同绝对位置但相同相对距离的点积应该相等
    pairs = [(3, 5), (7, 9), (100, 102), (1024, 1026)]
    print(f"{'pos_q':>6}  {'pos_k':>6}  {'gap':>4}  {'<q_rot, k_rot>':>18}")
    for pq, pk in pairs:
        q_rot = apply_rope(q, pq)  # 按位置 pq 旋转 Q
        k_rot = apply_rope(k, pk)  # 按位置 pk 旋转 K
        d_prod = dot(q_rot, k_rot)
        print(f"{pq:>6}  {pk:>6}  {pk - pq:>4}  {d_prod:>18.6f}")
    print("all rows with gap=2 should have matching dot products.")
    print()


def demo_rope_base_scaling():
    """演示 RoPE base 缩放（NTK-aware 长上下文扩展）。"""
    print("=== RoPE base scaling (NTK-aware for long context) ===")
    rng = random.Random(1)
    d = 8
    q = [rng.gauss(0, 1) for _ in range(d)]
    k = [rng.gauss(0, 1) for _ in range(d)]

    # 更大的 base = 更慢的旋转 = 更长的上下文不发生相位包裹
    for base in [10000, 100000, 1_000_000]:
        q_rot = apply_rope(q, pos=4096, base=base)
        k_rot = apply_rope(k, pos=4098, base=base)
        print(f"  base={base:>8d}  score={dot(q_rot, k_rot):+.6f}")
    print("larger base = slower rotation = longer context without phase wrap.")
    print()


def demo_alibi():
    """演示 ALiBi 偏置矩阵。"""
    print("=== ALiBi bias matrix ===")
    n_heads = 4
    slopes = alibi_slopes(n_heads)
    print(f"slopes for {n_heads} heads: " + ", ".join(f"{s:.4f}" for s in slopes))
    bias = alibi_bias(n_heads, seq_len=6, causal=False)
    print(f"head 0 bias (closer tokens get smaller penalty):")
    for row in bias[0]:
        print("  " + "  ".join(f"{v:+6.2f}" for v in row))
    print()


def main():
    """主函数：运行所有位置编码演示。"""
    demo_sinusoidal()     # 正弦编码演示
    demo_rope_relative()  # RoPE 相对距离属性
    demo_rope_base_scaling()  # RoPE base 缩放
    demo_alibi()          # ALiBi 偏置矩阵

    print("takeaway: RoPE encodes relative position in the dot product itself.")
    print("ALiBi skips embeddings entirely. sinusoidal is a footnote by 2026.")
    # 总结：RoPE 在点积中直接编码相对位置；ALiBi 完全跳过嵌入；
    # 正弦编码到 2026 年已成为历史注脚。


if __name__ == "__main__":
    main()
