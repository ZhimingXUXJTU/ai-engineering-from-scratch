# Why Transformers — The Problems with RNNs
# 为什么是 Transformer — RNN 的问题

> RNNs process tokens one at a time. Transformers process all tokens at once. That single architectural bet changed every scaling curve in deep learning after 2017.

> RNN 逐个处理 token。Transformer 一次性处理所有 token。这一个架构赌注改变了 2017 年之后深度学习中的每一条扩展曲线。

> **【中文解读】** RNN 有三个致命问题：无法并行、长程梯度消失、固定长度瓶颈。Transformer 用自注意力解决了这三个问题，开启了深度学习的新时代。

**Type:** Learn | **类型:** 学习
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Understand the three fatal weaknesses of recurrent neural networks (RNNs)
  理解循环神经网络（RNN）的三个致命弱点
- Explain why serial depth, not operation count, determines GPU training time
  解释为什么串行深度（而非操作数）决定了 GPU 训练时间
- Compare RNN vs Transformer complexity on sequence modeling tasks
  比较 RNN 与 Transformer 在序列建模任务上的复杂度
- Identify scenarios where RNNs or state-space models may still be preferred
  识别 RNN 或状态空间模型仍然更优的场景
- Recognize the inductive bias shift from locality to global attention
  认识从局部性到全局注意力的归纳偏好转移

## The Problem | 问题引入

Before 2017, every state-of-the-art sequence model on the planet — language, translation, speech — was a recurrent neural network. LSTMs and GRUs won ImageNet-equivalent translation benchmarks for half a decade. They were the only tool anyone had.

> 2017 年之前，全球每一个最先进的序列模型——语言、翻译、语音——都是循环神经网络。LSTM 和 GRU 在相当于 ImageNet 级别的翻译基准测试上称霸了五年。它们是所有人手中唯一的工具。

They had three fatal weaknesses. Sequential computation meant you could not parallelize along the time axis: token `t+1` needs the hidden state from token `t`. A 1,024-token sequence meant 1,024 serial steps on a GPU that can do 1,000,000 floating-point ops per cycle. Training wall-clock time scaled linearly with sequence length on hardware designed for parallelism.

> 它们有三个致命弱点。串行计算意味着你无法沿时间轴并行化：token `t+1` 需要来自 token `t` 的隐藏状态。一个 1,024 个 token 的序列意味着在每周期可执行 1,000,000 次浮点运算的 GPU 上要跑 1,024 个串行步骤。在为并行性而设计的硬件上，训练时间随序列长度线性增长。

> **【中文解读】** 第一个致命弱点：串行计算。RNN 必须按顺序处理每个 token，完全无法利用 GPU 的并行计算能力。训练时间与序列长度线性增长，这在 GPU 时代是巨大的浪费。

Vanishing gradients meant information 50 tokens back was already compressed through 50 non-linearities. Gated recurrent units (LSTM, GRU) softened the crush but never eliminated it. Long-range dependencies — "the book I read last summer on a plane to Kyoto was…" — routinely failed.

> 梯度消失意味着 50 个 token 之前的信息已经被 50 个非线性变换压缩殆尽。门控循环单元（LSTM、GRU）缓解了这种压榨但从未消除它。长程依赖——"我去年夏天在飞往京都的飞机上读的那本书是……"——经常失败。

> **【中文解读】** 第二个致命弱点：梯度消失。经过 50 层非线性变换后，远处的信息几乎完全丢失。LSTM 和 GRU 的门控机制只是缓解而非根治这个问题。

Fixed-width hidden states meant the encoder squeezed the entire source sequence into a single vector before the decoder saw anything. Doesn't matter if the source is 5 tokens or 500; the bottleneck is the same shape.

> 固定宽度的隐藏状态意味着编码器在解码器看到任何内容之前，将整个源序列压缩为一个向量。无论源序列是 5 个 token 还是 500 个；瓶颈的形状都一样。

> **【中文解读】** 第三个致命弱点：固定宽度瓶颈。编码器必须把整个源序列压缩到一个固定长度的向量中——信息瓶颈是结构性的。Transformer 的自注意力让每个位置都能直接访问所有其他位置，彻底消除了这个瓶颈。

The 2017 paper "Attention Is All You Need" proposed something radical: drop recurrence entirely. Let every position attend to every other position in parallel. Train in one big matrix multiplication instead of 1,024 sequential ones.

> 2017 年的论文 "Attention Is All You Need" 提出了一个激进的方案：完全抛弃循环。让每个位置同时关注所有其他位置。用一次大规模矩阵乘法代替 1,024 次串行计算。

The result dominates every modality by 2026. Language (GPT-5, Claude 4, Llama 4), vision (ViT, DINOv2, SAM 3), audio (Whisper), biology (AlphaFold 3), robotics (RT-2). Same block, different inputs.

> 到 2026 年，其成果主导了每一种模态。语言（GPT-5、Claude 4、Llama 4）、视觉（ViT、DINOv2、SAM 3）、音频（Whisper）、生物学（AlphaFold 3）、机器人（RT-2）。相同的模块，不同的输入。

## The Concept | 核心概念

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.** An RNN computes `h_t = f(h_{t-1}, x_t)`. Each step depends on the previous. You cannot compute `h_5` before `h_4`. On modern GPUs with 10,000+ parallel cores, this wastes 99% of the silicon on a long sequence.

> **循环即瓶颈。** RNN 计算 `h_t = f(h_{t-1}, x_t)`。每一步都依赖前一步。你无法在 `h_4` 之前计算 `h_5`。在拥有 10,000+ 并行核心的现代 GPU 上，这浪费了长序列中 99% 的芯片算力。

> **【中文解读】** 循环是瓶颈的本质：每个时间步的计算都依赖前一步的结果。GPU 擅长的是成千上万并行操作，而 RNN 的串行依赖让它只能用到 GPU 极小一部分算力。Transformer 通过自注意力将序列处理从 O(N) 串行深度降到 O(1)，彻底释放了 GPU 的并行能力。

**Attention as a broadcast.** Self-attention computes `output_i = sum_j(a_ij * v_j)` for every pair `(i, j)` simultaneously. The whole N×N attention matrix fills in one batched matmul. No step depends on another. GPUs love it.

> **注意力即广播。** 自注意力同时为每一对 `(i, j)` 计算 `output_i = sum_j(a_ij * v_j)`。整个 N×N 注意力矩阵在一次批量矩阵乘法中填满。没有步骤相互依赖。GPU 喜欢它。

**The speedup is not a constant.** It is the difference between `O(N)` serial depth and `O(1)` serial depth. In practice, transformers train 5–10× faster per epoch on matched hardware at N=512, and the gap widens with sequence length until you hit the `O(N²)` memory wall of attention (which Flash Attention later fixed — see Lesson 12).

> **加速不是常数。** 它是 `O(N)` 串行深度与 `O(1)` 串行深度之间的区别。在实践中，在匹配硬件上 N=512 时，Transformer 每个 epoch 的训练速度快 5-10 倍，而且差距随序列长度增加而扩大，直到你碰到注意力的 `O(N²)` 内存墙（Flash Attention 后来修复了它——见第 12 课）。

**What transformers cost.** Attention memory scales as `O(N²)`. For 2K context, fine. For 128K context, you need sliding windows, RoPE extrapolation, Flash Attention tiling, or linear attention variants. Recurrence was `O(N)` in both time and memory; transformers trade time for memory and then win the time back through parallelism.

> **Transformer 的代价。** 注意力内存按 `O(N²)` 增长。对于 2K 上下文，没问题。对于 128K 上下文，你需要滑动窗口、RoPE 外推、Flash Attention 分块计算或线性注意力变体。循环在时间和内存上都是 `O(N)`；Transformer 用内存换时间，然后通过并行性赢回时间。

**The inductive bias shift.** RNNs assume locality and recency. Transformers assume nothing — every pair is a candidate for attention. That is why transformers need more data to train well but scale further once they have it. Chinchilla (2022) formalized this: given enough tokens, a transformer always beats an RNN of equal parameter count.

> **归纳偏好的转变。** RNN 假设局部性和邻近性。Transformer 不做任何假设——每一对都是注意力的候选者。这就是为什么 Transformer 需要更多数据来训练好，但一旦拥有足够数据就能扩展得更远。Chinchilla（2022）形式化了这一点：给定足够的 token，Transformer 总是击败同等参数量的 RNN。

> **【中文解读】** 归纳偏好的转移是 Transformer 成功的关键洞察。RNN 隐式假设"近处的 token 更重要"，而 Transformer 不做任何假设——任何两个位置之间都可以建立直接联系。这种弱归纳偏好意味着需要更多数据训练，但一旦数据充足，扩展性远超 RNN。

> **【拓展：Chinchilla 缩放定律】** DeepMind 的 Chinchilla 论文（2022）证明，模型参数量和训练数据量应等比例增长。这解释了为什么 Llama、GPT-4 等模型需要万亿级 token 的训练数据——弱归纳偏好需要大量数据来"补偿"。

## Build It | 动手实现

No neural network here — we simulate the core bottleneck numerically so you feel the gap on your laptop.

> 这里没有神经网络——我们用数值模拟核心瓶颈，让你在笔记本电脑上感受差距。

> **【中文解读】** 这一节用纯数值模拟让你亲手感受串行 vs 并行的性能差距。关键在于"依赖深度"——串行链的深度为 N，而并行归约的深度仅为 O(1) 或 O(log N)。这就是 Transformer 比 RNN 快的根本原因。

### Step 1: Measure Serial Depth | 步骤 1：测量串行深度

See `code/main.py`. We build two functions. One encodes a sequence as a chain of additions (serial, like an RNN). One encodes it as a parallel reduction (broadcast, like attention). Same math, different dependency graph.

> 参见 `code/main.py`。我们构建两个函数。一个将序列编码为加法链（串行，类似 RNN）。一个将其编码为并行归约（广播，类似注意力）。相同的数学，不同的依赖图。

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

> 我们对长达 100,000 个元素的序列进行计时。RNN 版本是 O(N) 的单一 CPU 流水线。即使在纯 Python 中，attention-style 归约在长度 ≥ 1,000 时也能胜出，因为 Python 的 `sum()` 是用 C 实现的，迭代时没有解释器的逐步开销。

### Step 2: Count Theoretical Operations | 步骤 2：计算理论操作数

Both algorithms do N adds. The difference is *dependency depth*: how many operations must happen sequentially before the next can start. RNN depth = N. Attention depth = log(N) with a tree reduction, or 1 with a parallel scan. Depth, not op count, decides GPU time.

> 两种算法都做 N 次加法。区别在于*依赖深度*：在下一个操作开始之前，必须顺序执行多少操作。RNN 深度 = N。注意力深度 = 用树形归约时为 log(N)，用并行扫描时为 1。决定 GPU 时间的是深度，而非操作数。

### Step 3: Empirical Scaling on Long Sequences | 步骤 3：长序列上的实证扩展

We print a timing table that makes the O(N) gap visible. On a 2026 Mac laptop, sequences under 1,000 elements are too fast to measure. Sequences of 100,000 show a clean linear scan. Scale that to a 16,384-token transformer with a 12-layer LSTM equivalent and you see why training wall-clock was a blocker in 2016.

> 我们打印一张使 O(N) 差距可见的计时表。在 2026 年的 Mac 笔记本上，少于 1,000 个元素的序列太快而无法测量。100,000 个元素的序列显示出清晰的线性扫描。将其扩展到具有 12 层 LSTM 等效的 16,384-token Transformer，你就会明白为什么 2016 年训练时间是瓶颈。

## Use It | 用框架实现

When to still pick an RNN in 2026:

> 2026 年何时仍应选择 RNN：

> **【中文解读】** 虽然 Transformer 在大多数场景下胜出，但并非万能。流式推理（每次只处理一个 token）、超长序列（>1M token）和边缘设备场景下，RNN 或状态空间模型（如 Mamba）仍有优势。2026 年的趋势是混合架构（如 Jamba），结合两者的优点。

> **【拓展：Mamba 与状态空间模型】** Mamba（2023）通过选择性扫描机制实现了 O(N) 复杂度的序列建模，同时支持并行训练。它本质上是一种参数化的 RNN，但在训练效率上接近 Transformer。在代码生成、长文档理解等任务中，混合 Mamba+Transformer 架构已成为前沿实验室的重要探索方向。

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

State-space models (SSMs) like Mamba are essentially RNNs with structured parameterization that gives them the best of both: `O(N)` scan memory, parallel training via selective scan. They recover 90% of transformer quality with better long-context scaling. In 2026 most frontier labs train hybrid SSM+transformer models (e.g. Jamba, Samba) — recurrence is not dead, it is a component.

> 状态空间模型（SSM）如 Mamba 本质上是具有结构化参数化的 RNN，兼具两者的优势：`O(N)` 扫描内存，通过选择性扫描实现并行训练。它们恢复了 Transformer 90% 的质量，同时具有更好的长上下文扩展性。2026 年大多数前沿实验室训练混合 SSM+Transformer 模型（如 Jamba、Samba）——循环没有消亡，它是一个组件。

## Ship It | 产出物

See `outputs/skill-architecture-picker.md`. The skill picks an architecture for a new sequence problem given length, throughput, and training-budget constraints. It should always refuse to recommend a pure RNN for training runs above 1B tokens without stating the trade-off.

> 参见 `outputs/skill-architecture-picker.md`。该技能为新的序列问题选择架构，给定长度、吞吐量和训练预算约束。它应始终拒绝为超过 1B token 的训练运行推荐纯 RNN，除非声明了权衡。

> **【拓展：架构选择决策树】** 在实际工程中，架构选择需要考虑多个维度：序列长度、延迟要求、内存预算、训练数据量、部署硬件。对于大多数 NLP 任务，Decoder-only Transformer 是默认选择；对于超长序列，考虑 Mamba 或混合架构；对于边缘部署，量化的 RNN/SSM 可能更合适。参考 Google 的 Pathways 和 Microsoft 的 Phi 系列的设计决策。

## Exercises | 练习题

1. **Easy / 简单。** Take `rnn_style` from `code/main.py` and replace the scalar hidden state with a length-64 vector of hidden states. Re-measure. How much does the serial overhead grow with hidden-state dimension?
   取 `code/main.py` 中的 `rnn_style`，将标量隐藏状态替换为长度 64 的隐藏状态向量。重新测量。串行开销随隐藏状态维度增长了多少？

2. **Medium / 中等。** Implement a parallel prefix-sum (Hillis-Steele scan) in pure Python. Verify it produces the same numerical output as a serial scan on length 1024. Count the depth.
   用纯 Python 实现并行前缀和（Hillis-Steele 扫描）。验证它在长度 1024 上产生与串行扫描相同的数值输出。计算深度。

3. **Hard / 困难。** Port the attention-style reduction to PyTorch on GPU. Time both as you sweep sequence length from 64 to 65,536. Plot and explain the curve shape.
   将 attention-style 归约移植到 GPU 上的 PyTorch。在序列长度从 64 扫到 65,536 时对两者计时。绘制并解释曲线形状。

## Key Terms | 术语速查表

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Further Reading | 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the paper that killed recurrence in mainstream NLP.
  Vaswani 等人（2017）— 终结了主流 NLP 中循环的论文。

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — where attention was born, bolted onto an RNN.
  Bahdanau, Cho, Bengio（2014）— 注意力诞生的地方，附加在 RNN 上。

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) — the original LSTM paper, for the record.
  Hochreiter, Schmidhuber（1997）— 原始 LSTM 论文，留作记录。

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) — modern recurrent answer to transformers.
  Gu, Dao（2023）— Transformer 的现代循环替代方案。

> **【拓展："Attention Is All You Need" 的历史影响】** Vaswani 等人 2017 年的论文不仅解决了 RNN 的并行化问题，更引发了一场范式革命。从 BERT（2018）到 GPT-4（2023），从 ViT（2020）到 AlphaFold 2（2021），Transformer 架构已成为现代 AI 的基础模块。它证明了"弱归纳偏好 + 大数据 + 大算力"可以超越精心设计的领域特定架构。
