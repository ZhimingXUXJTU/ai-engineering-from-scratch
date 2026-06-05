"""为什么是 Transformer — RNN 的问题
Why Transformers — demonstrate the serial-depth gap between RNN-style
recurrence and attention-style parallel reduction.

本模块用数值模拟展示 RNN 串行计算与 Transformer 并行计算之间的核心性能差距。
AI 应用：理解 Transformer 为何取代 RNN 成为现代大语言模型的基础架构，
对于模型选型（何时用 Transformer、何时用 SSM）至关重要。

Runs in pure stdlib. No numpy, no torch.
"""

import math
import time


def rnn_style(xs, decay=0.9):
    """串行循环计算：h_t 依赖 h_{t-1}，无法并行化。
    Sequential recurrence: h_t depends on h_{t-1}. Cannot parallelize.

    模拟 RNN 的核心瓶颈——每个时间步必须等待前一步完成。
    AI 应用：这就是为什么 RNN 训练在 GPU 上效率低下的根本原因。
    """
    h = 0.0
    for x in xs:
        h = decay * h + x  # 串行依赖：h 依赖前一个 h
    return h


def attention_style(xs):
    """顺序无关的归约：每个元素相互独立。
    Order-independent reduction: every element is independent.

    模拟自注意力机制的核心优势——所有位置可以同时计算。
    AI 应用：Transformer 的并行性使得 GPU 的万级核心得以充分利用。
    """
    return sum(xs) / len(xs)


def serial_scan(xs):
    """串行前缀和。深度 O(N)。
    Prefix sum computed serially. Depth O(N).

    AI 应用：传统 RNN 的梯度传播就像串行扫描，深度与序列长度成正比。
    """
    out = []
    acc = 0.0
    for x in xs:
        acc += x  # 累加器逐步累加，无法跳步
        out.append(acc)
    return out


def parallel_scan(xs):
    """Hillis-Steele 并行前缀和。深度 O(log N)。
    Hillis-Steele parallel prefix sum. Depth O(log N).

    在纯 Python 中每步仍是串行的，但数据依赖图的深度仅为 log2(N)。
    在真正的 GPU 上，这带来对数深度的扫描。图的形状决定了 GPU 内核的性能。

    AI 应用：Transformer 的自注意力本质上类似于并行扫描——
    所有位置间的信息传递可以在对数步内完成，而非线性步。
    """
    out = list(xs)
    step = 1
    n = len(out)
    while step < n:
        new = list(out)
        for i in range(step, n):
            new[i] = out[i] + out[i - step]  # 并行步：每个位置与 step 前的位置相加
        out = new
        step *= 2  # 步长翻倍，总深度为 log2(N)
    return out


def benchmark(n, reps=3):
    """对长度为 n 的序列运行 RNN 风格和 Attention 风格的性能基准测试。
    Benchmark RNN-style vs Attention-style on sequence of length n.

    AI 应用：这种基准测试帮助工程师理解在实际部署中选择哪种架构。
    """
    xs = [0.001 * (i % 17) for i in range(n)]

    # 测试 RNN 风格（串行）的耗时
    best_rnn = math.inf
    for _ in range(reps):
        t0 = time.perf_counter()
        _ = rnn_style(xs)
        best_rnn = min(best_rnn, time.perf_counter() - t0)

    # 测试 Attention 风格（并行）的耗时
    best_attn = math.inf
    for _ in range(reps):
        t0 = time.perf_counter()
        _ = attention_style(xs)
        best_attn = min(best_attn, time.perf_counter() - t0)

    return best_rnn, best_attn


def depth(n):
    """计算 RNN 与 Attention 风格归约的串行深度。
    Serial-depth count for RNN vs attention-style reductions.

    AI 应用：串行深度是衡量模型能否在 GPU 上高效训练的关键指标。
    """
    rnn_depth = n  # RNN 深度 = 序列长度 N
    attn_depth = max(1, math.ceil(math.log2(n)))  # 注意力深度 = log2(N)
    return rnn_depth, attn_depth


def main():
    """主函数：运行串行深度对比、时间基准测试和前缀和等价性验证。"""
    # 第一部分：理论深度对比
    print("=== serial-depth comparison ===")
    print(f"{'N':>8}  {'rnn depth':>12}  {'attn depth':>12}  {'speedup (ops)':>16}")
    for n in [64, 512, 4096, 32768, 262144]:
        rd, ad = depth(n)
        print(f"{n:>8}  {rd:>12}  {ad:>12}  {rd / ad:>15.0f}x")

    # 第二部分：实际耗时对比（纯 Python）
    print()
    print("=== wall-clock on this machine (pure Python) ===")
    print(f"{'N':>8}  {'rnn (ms)':>10}  {'attn (ms)':>10}  {'ratio':>8}")
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        rnn_t, attn_t = benchmark(n)
        ratio = rnn_t / attn_t if attn_t > 0 else float("inf")
        print(f"{n:>8}  {rnn_t * 1000:>10.2f}  {attn_t * 1000:>10.2f}  {ratio:>7.1f}x")

    # 第三部分：验证串行前缀和与并行前缀和的结果一致性
    print()
    print("=== prefix-sum equivalence check ===")
    xs = [float(i) for i in range(16)]
    ser = serial_scan(xs)
    par = parallel_scan(xs)
    mismatches = sum(1 for a, b in zip(ser, par) if abs(a - b) > 1e-9)
    print(f"length: {len(xs)}, mismatches between serial and parallel scan: {mismatches}")
    print(f"last value (serial):   {ser[-1]}")
    print(f"last value (parallel): {par[-1]}")

    # 总结
    print()
    print("takeaway: attention wins on every dimension but memory.")
    print("memory cost is O(N^2) for full attention; Lesson 12 covers the fixes.")
    # 关键结论：注意力在所有维度上获胜，除了内存。全注意力的内存开销为 O(N²)，
    # 第 12 课将介绍 Flash Attention 等优化方案。


if __name__ == "__main__":
    main()
