# Why Transformers — The Problems with RNNs | 为什么是 Transformer — RNN 的问题

> RNNs process tokens one at a time. Transformers process all tokens at once. That single architectural bet changed every scaling curve in deep learning after 2017.

> **【中文解读】** RNN 有三个致命问题：无法并行、长程梯度消失、固定长度瓶颈。Transformer 用自注意力解决了这三个问题，开启了深度学习的新时代。

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism)
**Time:** ~45 minutes

## The Problem | 问题引入

Before 2017, every state-of-the-art sequence model on the planet — language, translation, speech — was a recurrent neural network. LSTMs and GRUs won ImageNet-equivalent translation benchmarks for half a decade. They were the only tool anyone had.

They had three fatal weaknesses. Sequential computation meant you could not parallelize along the time axis: token `t+1` needs the hidden state from token `t`. A 1,024-token sequence meant 1,024 serial steps on a GPU that can do 1,000,000 floating-point ops per cycle. Training wall-clock time scaled linearly with sequence length on hardware designed for parallelism.

> **【中文解读】** 第一个致命弱点：串行计算。RNN 必须按顺序处理每个 token，完全无法利用 GPU 的并行计算能力。训练时间与序列长度线性增长，这在 GPU 时代是巨大的浪费。

Vanishing gradients meant information 50 tokens back was already compressed through 50 non-linearities.

> **【中文解读】** 第二个致命弱点：梯度消失。经过 50 层非线性变换后，远处的信息几乎完全丢失。LSTM 和 GRU 的门控机制只是缓解而非根治这个问题。 Gated recurrent units (LSTM, GRU) softened the crush but never eliminated it. Long-range dependencies — "the book I read last summer on a plane to Kyoto was…" — routinely failed.

Fixed-width hidden states meant the encoder squeezed the entire source sequence into a single vector before the decoder saw anything. Doesn't matter if the source is 5 tokens or 500; the bottleneck is the same shape.

> **【中文解读】** 第三个致命弱点：固定宽度瓶颈。编码器必须把整个源序列压缩到一个固定长度的向量中——信息瓶颈是结构性的。Transformer 的自注意力让每个位置都能直接访问所有其他位置，彻底消除了这个瓶颈。

The 2017 paper "Attention Is All You Need" proposed something radical: drop recurrence entirely. Let every position attend to every other position in parallel. Train in one big matrix multiplication instead of 1,024 sequential ones.

The result dominates every modality by 2026. Language (GPT-5, Claude 4, Llama 4), vision (ViT, DINOv2, SAM 3), audio (Whisper), biology (AlphaFold 3), robotics (RT-2). Same block, different inputs.

## The Concept | 核心概念

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.** An RNN computes `h_t = f(h_{t-1}, x_t)`. Each step depends on the previous. You cannot compute `h_5` before `h_4`. On modern GPUs with 10,000+ parallel cores, this wastes 99% of the silicon on a long sequence.

> **【中文解读】** 循环是瓶颈的本质：每个时间步的计算都依赖前一步的结果。GPU 擅长的是成千上万并行操作，而 RNN 的串行依赖让它只能用到 GPU 极小一部分算力。Transformer 通过自注意力将序列处理从 O(N) 串行深度降到 O(1)，彻底释放了 GPU 的并行能力。

**Attention as a broadcast.** Self-attention computes `output_i = sum_j(a_ij * v_j)` for every pair `(i, j)` simultaneously. The whole N×N attention matrix fills in one batched matmul. No step depends on another. GPUs love it.

**The speedup is not a constant.** It is the difference between `O(N)` serial depth and `O(1)` serial depth. In practice, transformers train 5–10× faster per epoch on matched hardware at N=512, and the gap widens with sequence length until you hit the `O(N²)` memory wall of attention (which Flash Attention later fixed — see Lesson 12).

**What transformers cost.** Attention memory scales as `O(N²)`. For 2K context, fine. For 128K context, you need sliding windows, RoPE extrapolation, Flash Attention tiling, or linear attention variants. Recurrence was `O(N)` in both time and memory; transformers trade time for memory and then win the time back through parallelism.

**The inductive bias shift.** RNNs assume locality and recency. Transformers assume nothing — every pair is a candidate for attention. That is why transformers need more data to train well but scale further once they have it. Chinchilla (2022) formalized this: given enough tokens, a transformer always beats an RNN of equal parameter count.

> **【中文解读】** 归纳偏好的转移是 Transformer 成功的关键洞察。RNN 隐式假设"近处的 token 更重要"，而 Transformer 不做任何假设——任何两个位置之间都可以建立直接联系。这种弱归纳偏好意味着需要更多数据训练，但一旦数据充足，扩展性远超 RNN。

> **【拓展：Chinchilla 缩放定律】** DeepMind 的 Chinchilla 论文（2022）证明，模型参数量和训练数据量应等比例增长。这解释了为什么 Llama、GPT-4 等模型需要万亿级 token 的训练数据——弱归纳偏好需要大量数据来"补偿"。

## Build It | 动手实现

No neural network here — we simulate the core bottleneck numerically so you feel the gap on your laptop.

> **【中文解读】** 这一节用纯数值模拟让你亲手感受串行 vs 并行的性能差距。关键在于"依赖深度"——串行链的深度为 N，而并行归约的深度仅为 O(1) 或 O(log N)。这就是 Transformer 比 RNN 快的根本原因。

### Step 1: measure serial depth

See `code/main.py`. We build two functions. One encodes a sequence as a chain of additions (serial, like an RNN). One encodes it as a parallel reduction (broadcast, like attention). Same math, different dependency graph.

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

We time both on sequences up to 100,000 elements. The RNN version is O(N) and a single CPU pipeline. Even in pure Python, the attention-style reduction beats it at length ≥ 1,000 because Python's `sum()` is implemented in C and iterates without interpreter overhead per step.

### Step 2: count theoretical operations

Both algorithms do N adds. The difference is *dependency depth*: how many operations must happen sequentially before the next can start. RNN depth = N. Attention depth = log(N) with a tree reduction, or 1 with a parallel scan. Depth, not op count, decides GPU time.

### Step 3: empirical scaling on long sequences

We print a timing table that makes the O(N) gap visible. On a 2026 Mac laptop, sequences under 1,000 elements are too fast to measure. Sequences of 100,000 show a clean linear scan. Scale that to a 16,384-token transformer with a 12-layer LSTM equivalent and you see why training wall-clock was a blocker in 2016.

## Use It | 用框架实现

When to still pick an RNN in 2026:

> **【中文解读】** 虽然 Transformer 在大多数场景下胜出，但并非万能。流式推理（每次只处理一个 token）、超长序列（>1M token）和边缘设备场景下，RNN 或状态空间模型（如 Mamba）仍有优势。2026 年的趋势是混合架构（如 Jamba），结合两者的优点。

> **【拓展：Mamba 与状态空间模型】** Mamba（2023）通过选择性扫描机制实现了 O(N) 复杂度的序列建模，同时支持并行训练。它本质上是一种参数化的 RNN，但在训练效率上接近 Transformer。在代码生成、长文档理解等任务中，混合 Mamba+Transformer 架构已成为前沿实验室的重要探索方向。

| Situation | Pick |
|-----------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

State-space models (SSMs) like Mamba are essentially RNNs with structured parameterization that gives them the best of both: `O(N)` scan memory, parallel training via selective scan. They recover 90% of transformer quality with better long-context scaling. In 2026 most frontier labs train hybrid SSM+transformer models (e.g. Jamba, Samba) — recurrence is not dead, it is a component.

## Ship It | 产出物

See `outputs/skill-architecture-picker.md`. The skill picks an architecture for a new sequence problem given length, throughput, and training-budget constraints. It should always refuse to recommend a pure RNN for training runs above 1B tokens without stating the trade-off.

> **【拓展：架构选择决策树】** 在实际工程中，架构选择需要考虑多个维度：序列长度、延迟要求、内存预算、训练数据量、部署硬件。对于大多数 NLP 任务，Decoder-only Transformer 是默认选择；对于超长序列，考虑 Mamba 或混合架构；对于边缘部署，量化的 RNN/SSM 可能更合适。参考 Google 的 Pathways 和 Microsoft 的 Phi 系列的设计决策。

## Exercises | 练习题

1. **Easy.** Take `rnn_style` from `code/main.py` and replace the scalar hidden state with a length-64 vector of hidden states. Re-measure. How much does the serial overhead grow with hidden-state dimension?
2. **Medium.** Implement a parallel prefix-sum (Hillis-Steele scan) in pure Python. Verify it produces the same numerical output as a serial scan on length 1024. Count the depth.
3. **Hard.** Port the attention-style reduction to PyTorch on GPU. Time both as you sweep sequence length from 64 to 65,536. Plot and explain the curve shape.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Recurrence | "RNNs are sequential" | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. |
| Serial depth | "How deep the graph is" | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. |
| Attention | "Let tokens look at each other" | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. |
| Context window | "How much the model sees" | Number of positions an attention layer can take as input; quadratic memory cost scales here. |
| Inductive bias | "Assumptions baked into the architecture" | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. |
| State-space model | "RNN with algebra behind it" | Recurrence parameterized for parallel training via structured state-space matrices. |
| Quadratic bottleneck | "Why context costs so much" | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. |

## Further Reading | 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the paper that killed recurrence in mainstream NLP.
- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — where attention was born, bolted onto an RNN.
- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) — the original LSTM paper, for the record.
- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) — modern recurrent answer to transformers.

> **【拓展："Attention Is All You Need" 的历史影响】** Vaswani 等人 2017 年的论文不仅解决了 RNN 的并行化问题，更引发了一场范式革命。从 BERT（2018）到 GPT-4（2023），从 ViT（2020）到 AlphaFold 2（2021），Transformer 架构已成为现代 AI 的基础模块。它证明了"弱归纳偏好 + 大数据 + 大算力"可以超越精心设计的领域特定架构。
