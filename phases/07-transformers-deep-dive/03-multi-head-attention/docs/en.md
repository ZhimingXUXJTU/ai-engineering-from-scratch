# Multi-Head Attention
# 多头注意力

> One attention head learns one relation at a time. Eight heads learn eight. Heads are free. Take more of them.

> 一个注意力头一次学习一种关系。八个头学习八种。头是免费的。多用一些。

> **【中文解读】** 多头注意力让模型同时关注不同类型的关系：语法、语义、位置等。GPT-3 有 96 个注意力头。理解多头 = 理解 Transformer 的表达能力。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A single self-attention head computes one attention matrix. That matrix captures one kind of relationship — usually the one that minimizes loss on whatever the training signal is. If your data has subject-verb agreement, co-reference, long-range discourse, and syntactic chunking all tangled together, a single head smears them into a single soft-max distribution and loses half the signal.

> 单个自注意力头计算一个注意力矩阵。该矩阵捕获一种关系——通常是最小化训练信号上损失的那一种。如果你的数据中主谓一致、共指消解、长程语篇和句法分块纠缠在一起，单个头会将它们模糊成单个 softmax 分布，丢失一半信号。

The fix from the 2017 Vaswani paper: run several attention functions in parallel, each with its own Q, K, V projections, and concatenate the outputs. Each head operates in a smaller subspace of dimension `d_model / n_heads`. Total parameters stay the same. Expressive power goes up.

> 2017 年 Vaswani 论文的修复方案：并行运行多个注意力函数，每个都有自己的 Q、K、V 投影，然后拼接输出。每个头在维度为 `d_model / n_heads` 的较小子空间中操作。总参数量不变。表达能力上升。

Multi-head attention is the default every transformer in 2026 ships with. The only argument is about *how many* heads and whether keys and values share projections (Grouped-Query Attention, Multi-Query Attention, Multi-head Latent Attention).

> 多头注意力是 2026 年每个 Transformer 的默认配置。唯一的争论是关于*多少*个头以及键和值是否共享投影（分组查询注意力、多查询注意力、多头潜在注意力）。

> **【中文解读】** 单个注意力头只能学习一种关系模式，但自然语言中存在多种关系（主谓一致、指代消解、句法结构等）。多头注意力的核心思想：用多个独立的注意力头并行工作，每个头在不同子空间中学习不同的关系，最后拼接混合。参数量不变，表达能力大幅提升。

## The Concept | 核心概念

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.** Take `X` of shape `(N, d_model)`. Project to Q, K, V each of shape `(N, d_model)`. Reshape to `(N, n_heads, d_head)` where `d_head = d_model / n_heads`. Transpose to `(n_heads, N, d_head)`.

> **拆分。** 取形状为 `(N, d_model)` 的 `X`。投影到形状各为 `(N, d_model)` 的 Q、K、V。重塑为 `(N, n_heads, d_head)`，其中 `d_head = d_model / n_heads`。转置为 `(n_heads, N, d_head)`。

**Attend in parallel.** Run scaled dot-product attention inside each head. Each head produces `(N, d_head)`. The heads operate on different subspaces of the embedding and never talk during the attention computation itself.

> **并行计算注意力。** 在每个头内运行缩放点积注意力。每个头产生 `(N, d_head)`。头在嵌入的不同子空间上操作，在注意力计算本身期间互不通信。

**Concatenate and project.** Stack heads back to `(N, d_model)` and multiply by a learned output matrix `W_o` of shape `(d_model, d_model)`. `W_o` is where heads get to mix.

> **拼接并投影。** 将头重新堆叠为 `(N, d_model)` 并乘以学习的输出矩阵 `W_o`，形状为 `(d_model, d_model)`。`W_o` 是头得以混合的地方。

**Why it works.** Each head can specialize without competing with the others for representational budget. Probing studies from 2019–2024 show distinct head roles: positional heads, head that attends to the previous token, copy heads, named-entity heads, induction heads (which underlie in-context learning).

> **为什么有效。** 每个头可以专门化而不与其他头争夺表示预算。2019-2024 年的探测研究显示了不同的头角色：位置头、关注前一个 token 的头、复制头、命名实体头、归纳头（它是上下文学习的基础）。

> **【中文解读】** 三步走：Split（拆分到多个子空间）→ Attend（每个头独立做注意力）→ Concat+Project（拼接并通过 W_o 混合）。关键洞察：每个头在不同子空间中独立工作，不争夺表示资源。实验表明不同头确实学会了不同的"职责"。

> **【拓展：GQA 在 Llama 3 中的实际应用】** Llama 3 70B 使用 64 个查询头但只有 8 个 KV 头，将 KV 缓存压缩了 8 倍。这在推理时节省大量显存，同时几乎不损失模型质量。GQA 已成为 2024-2026 年开源大模型的标配。DeepSeek-V2 的 MLA 则更进一步，将 KV 压缩到低秩隐空间。

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA is the modern default because it cuts KV-cache memory by a factor of `N/G` while keeping nearly full quality. MLA goes further by compressing K/V into a latent space, then projecting back at compute time — costs FLOPs, saves a lot more memory.

> GQA 是现代默认选择，因为它将 KV 缓存内存减少了 `N/G` 倍，同时几乎保持完整质量。MLA 通过将 K/V 压缩到隐空间更进一步，然后在计算时投影回来——花费 FLOP，节省更多内存。

## Build It | 动手实现

### Step 1: Split heads from the single-head attention we already have | 步骤 1：从已有的单头注意力拆分头

Take the `SelfAttention` from Lesson 02 and wrap it with a split/concat pair. See `code/main.py` for a numpy implementation; the logic is:

> 取第 02 课的 `SelfAttention`，用拆分/拼接对包装它。参见 `code/main.py` 中的 numpy 实现；逻辑如下：

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

One reshape and one transpose. No loop. This is exactly what PyTorch does under `nn.MultiheadAttention`.

> 一次 reshape 和一次 transpose。没有循环。这正是 PyTorch 在 `nn.MultiheadAttention` 底层所做的。

> **【中文解读】** `split_heads` 和 `combine_heads` 只是 reshape + transpose 操作，无需循环。这就是多头注意力在 GPU 上高效的原因——它本质上就是批量矩阵乘法。

### Step 2: Run scaled-dot-product attention per head | 步骤 2：每个头运行缩放点积注意力

Each head gets its own slice of Q, K, V. Attention becomes a batched matmul:

> 每个头获得自己的 Q、K、V 切片。注意力变成批量矩阵乘法：

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

On real hardware `Qh @ Kh.transpose(...)` is one `bmm`. The GPU sees a single batched matmul of shape `(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`. Adding heads is free.

> 在真实硬件上，`Qh @ Kh.transpose(...)` 是一次 `bmm`。GPU 看到的是形状为 `(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)` 的单次批量矩阵乘法。增加头是免费的。

### Step 3: Grouped-Query Attention variant | 步骤 3：分组查询注意力变体

Only the key and value projections change. Q gets `n_heads` groups; K and V get `n_kv_heads < n_heads` groups and are repeated to match:

> 只有键和值的投影发生变化。Q 有 `n_heads` 个组；K 和 V 有 `n_kv_heads < n_heads` 个组，并被重复以匹配：

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

At inference this saves memory because only `n_kv_heads` copies live in the KV cache, not `n_heads`. Llama 3 70B uses 64 query heads with 8 KV heads — an 8× cache shrink.

> 在推理时，这节省了内存，因为只有 `n_kv_heads` 份副本存在于 KV 缓存中，而不是 `n_heads` 份。Llama 3 70B 使用 64 个查询头和 8 个 KV 头——8 倍的缓存缩减。

> **【拓展：MQA/GQA 在推理中的内存节约】** KV 缓存的大小与 KV 头数成正比。Llama 3 70B 使用 64 个查询头但仅 8 个 KV 头，将 KV 缓存压缩了 8 倍。对于 128K 上下文，这意味着节省数 GB 显存。这是大模型长上下文推理的关键优化——GQA 几乎不损失质量，但显著降低推理成本。

### Step 4: Probe what each head learned | 步骤 4：探测每个头学到了什么

Run MHA on a short sentence with 4 heads. For each head, print the `(N, N)` attention matrix. You'll see different heads pick out different structure even with random initialization — that's partly signal, partly rotational symmetry in the subspaces.

> 在短句子上用 4 个头运行 MHA。对每个头，打印 `(N, N)` 注意力矩阵。你会看到即使使用随机初始化，不同的头也会挑选出不同的结构——这部分是信号，部分是子空间中的旋转对称性。

## Use It | 用框架实现

In PyTorch, the one-line version:

> PyTorch 中，一行版本：

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

GQA as of PyTorch 2.5+:

> GQA（PyTorch 2.5+）：

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?** Rules of thumb from production models in 2026:

> **多少个头？** 2026 年生产模型的经验法则：

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head` almost always lands at 64 or 128. It is the unit of how much one head can "see." Drop below 32 and heads start fighting the scaling factor `sqrt(d_head)`; go above 256 and you lose the "many small specialists" benefit.

> `d_head` 几乎总是 64 或 128。它是一个头能"看到"多少的度量单位。低于 32 时，头开始与缩放因子 `sqrt(d_head)` 冲突；超过 256 时，你失去了"许多小专家"的好处。

## Ship It | 产出物

See `outputs/skill-mha-configurator.md`. The skill recommends head count, kv-head count, and projection strategy for a new transformer given parameter budget, sequence length, and deployment target.

> 参见 `outputs/skill-mha-configurator.md`。该技能为新 Transformer 推荐头数、KV 头数和投影策略，给定参数预算、序列长度和部署目标。

## Exercises | 练习题

1. **Easy / 简单。** Take the MHA from `code/main.py` and change `n_heads` from 1 to 16 with `d_model=64` fixed. Plot the loss of a tiny one-layer model on a synthetic copy task. Do more heads help, plateau, or hurt?
   取 `code/main.py` 中的 MHA，在 `d_model=64` 固定的情况下将 `n_heads` 从 1 改为 16。在一个合成复制任务上绘制微型单层模型的损失。更多头有帮助、达到平台期还是有害？

2. **Medium / 中等。** Implement MQA (one KV head shared across all query heads). Measure how much parameter count drops vs full MHA. Compute how much the KV-cache size shrinks at inference for N=2048.
   实现 MQA（一个 KV 头在所有查询头间共享）。测量与完整 MHA 相比参数量下降多少。计算在 N=2048 的推理时 KV 缓存大小缩减多少。

3. **Hard / 困难。** Implement a tiny version of Multi-head Latent Attention: compress K,V to a rank-`r` latent, store the latent in the KV cache, decompress at attention time. At what `r` does cache memory cross below 1/8 of full MHA while quality stays within 1 bit of validation ppl?
   实现迷你版的 Multi-head Latent Attention：将 K,V 压缩为秩 `r` 的隐向量，在 KV 缓存中存储隐向量，在注意力计算时解压。在什么 `r` 值下缓存内存降到完整 MHA 的 1/8 以下，同时质量保持在验证困惑度的 1 bit 以内？

## Key Terms | 术语速查表

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Further Reading | 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) — the original multi-head spec.
  Vaswani 等人（2017）— 原始多头规范。

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) — the MQA paper.
  Shazeer（2019）— MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) — how to convert MHA to GQA after training.
  Ainslie 等人（2023）— 训练后如何将 MHA 转换为 GQA。

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) — MLA and why it beats MHA/GQA on cache memory.
  DeepSeek-AI（2024）— MLA 及为何在缓存内存上击败 MHA/GQA。

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) — mechanistic look at what heads actually do.
  Olsson 等人（2022）— 对头实际功能的机制分析。

> **【拓展：Induction Heads 与上下文学习】** Anthropic 的研究发现，Transformer 的上下文学习能力（in-context learning）主要由一种称为"induction head"的注意力头实现。它们检测序列中之前出现的模式并复制后续内容。这解释了为什么大模型能"从示例中学习"而无需更新权重——这是 prompt engineering 有效性的底层机制。
