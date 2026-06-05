# Self-Attention from Scratch
# 自注意力从零实现

> Attention is a lookup table where every word asks "who matters to me?" — and learns the answer.

> 注意力是一张查找表，其中每个词都在问"谁对我重要？"——然后学会了答案。

> **【中文解读】** Self-Attention 是 Transformer 的核心：Q*K^T 计算每个 token 对其他 token 的关注度。理解 Q/K/V 的直觉是理解 GPT/BERT 的基础。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 Lesson 10 (Sequence-to-Sequence) | **前置知识:** 阶段 3（深度学习基础），阶段 5 第 10 课（序列到序列）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Learning Objectives | 学习目标

- Implement scaled dot-product self-attention from scratch using only NumPy, including query/key/value projections and the softmax-weighted sum
  仅使用 NumPy 从零实现缩放点积自注意力，包括查询/键/值投影和 softmax 加权求和
- Build a multi-head attention layer that splits heads, computes parallel attention, and concatenates results
  构建多头注意力层，实现头拆分、并行注意力计算和结果拼接
- Trace how the attention matrix captures token relationships and explain why scaling by sqrt(d_k) prevents softmax saturation
  追踪注意力矩阵如何捕获 token 关系，并解释为什么除以 sqrt(d_k) 能防止 softmax 饱和
- Apply causal masking to convert bidirectional attention into autoregressive (decoder-style) attention
  应用因果掩码将双向注意力转换为自回归（解码器风格）注意力

## The Problem | 问题引入

RNNs process sequences one token at a time. By the time you reach token 50, the information from token 1 has been squeezed through 50 compression steps. Long-range dependencies get crushed into a fixed-size hidden state — a bottleneck that no amount of LSTM gating fully solves.

> RNN 逐个 token 处理序列。当你到达第 50 个 token 时，来自第 1 个 token 的信息已经被压缩了 50 次。长程依赖被压碎成固定大小的隐藏状态——这是 LSTM 门控无法完全解决的瓶颈。

The 2014 Bahdanau attention paper showed the fix: let the decoder look back at every encoder position and decide which ones matter for the current step. But it was still bolted onto an RNN. The 2017 "Attention Is All You Need" paper asked a sharper question: what if attention is the *only* mechanism? No recurrence. No convolution. Just attention.

> 2014 年 Bahdanau 注意力论文展示了修复方法：让解码器回顾编码器的每个位置，并决定哪些对当前步骤重要。但它仍然附加在 RNN 上。2017 年的 "Attention Is All You Need" 论文提出了一个更尖锐的问题：如果注意力是*唯一*的机制呢？没有循环。没有卷积。只有注意力。

Self-attention lets every position in a sequence attend to every other position in a single parallel step. That is what makes transformers fast, scalable, and dominant.

> 自注意力让序列中的每个位置在单个并行步骤中关注所有其他位置。这就是使 Transformer 快速、可扩展且占主导地位的原因。

> **【中文解读】** RNN 的信息传递像传话游戏——经过多步后信息严重失真。Bahdanau 注意力让解码器"回头看"编码器的每个位置，但仍依赖 RNN。Transformer 的革命性在于：完全抛弃循环，只用注意力一个机制。自注意力让序列中每个位置都能直接关注所有其他位置，一步到位。

## The Concept | 核心概念

### The Database Lookup Analogy | 数据库查找类比

Think of attention as a soft database lookup:

> 将注意力想象成软数据库查找：

```
Traditional database:
  Query: "capital of France"  -->  exact match  -->  "Paris"

Attention:
  Query: "capital of France"  -->  similarity to ALL keys  -->  weighted blend of ALL values
```

Every token generates three vectors:
- **Query (Q)**: "What am I looking for?"
  **查询 (Query, Q)**："我在找什么？"
- **Key (K)**: "What do I contain?"
  **键 (Key, K)**："我包含什么？"
- **Value (V)**: "What information do I provide if selected?"
  **值 (Value, V)**："如果被选中，我提供什么信息？"

The dot product between a query and all keys produces attention scores. High score means "this key matches my query." Those scores weight the values. The output is a weighted sum of values.

> 查询与所有键的点积产生注意力分数。高分意味着"这个键匹配我的查询"。这些分数对值进行加权。输出是值的加权求和。

> **【中文解读】** 注意力的数据库类比是理解 Q/K/V 的最佳方式。Q 是"我在找什么"，K 是"我有什么"，V 是"我的实际内容"。Q 和 K 的点积衡量匹配程度，softmax 归一化后作为权重，对 V 做加权求和。整个过程就是一个可微的"软查找"操作。

> **【拓展：注意力机制在真实系统中的应用】** GPT 系列使用因果自注意力（每个 token 只能看到之前的 token）；BERT 使用双向自注意力（每个 token 能看到所有 token）；交叉注意力（Cross-Attention）则在 T5、Stable Diffusion 等模型中连接编码器和解码器。理解 Q/K/V 是理解所有这些变体的基础。

### Q, K, V Computation | Q、K、V 计算

Each token embedding gets projected through three learned weight matrices:

> 每个 token 嵌入通过三个学习的权重矩阵进行投影：

```
Input embeddings (sequence of n tokens, each d-dimensional):

  X = [x1, x2, x3, ..., xn]       shape: (n, d)

Three weight matrices:

  Wq  shape: (d, dk)
  Wk  shape: (d, dk)
  Wv  shape: (d, dv)

Projections:

  Q = X @ Wq    shape: (n, dk)      each token's query
  K = X @ Wk    shape: (n, dk)      each token's key
  V = X @ Wv    shape: (n, dv)      each token's value
```

Visually, for one token:

> 直观地看，对于一个 token：

```
             Wq
  x_i ------[*]------> q_i    "What am I looking for?"
       |
       |     Wk
       +----[*]------> k_i    "What do I contain?"
       |
       |     Wv
       +----[*]------> v_i    "What do I offer?"
```

### The Attention Matrix | 注意力矩阵

Once you have Q, K, V for all tokens, attention scores form a matrix:

> 一旦你有了所有 token 的 Q、K、V，注意力分数形成一个矩阵：

```
Scores = Q @ K^T    shape: (n, n)

              k1    k2    k3    k4    k5
        +-----+-----+-----+-----+-----+
   q1   | 2.1 | 0.3 | 0.1 | 0.8 | 0.2 |   <- how much q1 attends to each key
        +-----+-----+-----+-----+-----+
   q2   | 0.4 | 1.9 | 0.7 | 0.1 | 0.3 |
        +-----+-----+-----+-----+-----+
   q3   | 0.2 | 0.6 | 2.3 | 0.5 | 0.1 |
        +-----+-----+-----+-----+-----+
   q4   | 0.9 | 0.1 | 0.4 | 1.7 | 0.6 |
        +-----+-----+-----+-----+-----+
   q5   | 0.1 | 0.3 | 0.2 | 0.5 | 2.0 |
        +-----+-----+-----+-----+-----+

Each row: one token's attention over the entire sequence
```

### Why Scale? | 为什么要缩放？

The dot products grow with dimension dk. If dk = 64, dot products can be in the range of tens, pushing softmax into regions where gradients vanish. The fix: divide by sqrt(dk).

> 点积随维度 dk 增长。如果 dk = 64，点积可能在几十的范围内，将 softmax 推入梯度消失的区域。修复方法：除以 sqrt(dk)。

```
Scaled scores = (Q @ K^T) / sqrt(dk)
```

This keeps values in a range where softmax produces useful gradients.

> 这使值保持在 softmax 能产生有用梯度的范围内。

> **【中文解读】** 缩放因子 1/sqrt(dk) 是一个关键但容易被忽视的细节。当维度 dk 较大时，点积的值会变得很大，导致 softmax 进入饱和区（输出接近 one-hot），梯度几乎为零。除以 sqrt(dk) 将值拉回有效范围，保证训练稳定。

### Softmax Turns Scores into Weights | Softmax 将分数转换为权重

Softmax converts raw scores into a probability distribution across each row:

> Softmax 将原始分数转换为每行的概率分布：

```
Raw scores for q1:   [2.1, 0.3, 0.1, 0.8, 0.2]
                            |
                         softmax
                            |
Attention weights:   [0.52, 0.09, 0.07, 0.14, 0.08]   (sums to ~1.0)
```

Now each token has a set of weights saying how much to attend to every other token.

> 现在每个 token 都有一组权重，表示对其他每个 token 的关注程度。

> **【拓展：注意力矩阵的可解释性】** 注意力矩阵（N×N）是 Transformer 可解释性研究的重要工具。通过可视化注意力权重，可以发现模型学到的语言模式：哪些 token 之间有强关联。例如，代词 "it" 通常会高度关注其指代的名词。BERT 的注意力可视化（如 bertviz 工具）已成为 NLP 可解释性研究的标准方法。

### Weighted Sum of Values | 值的加权求和

The final output for each token is a weighted sum of all value vectors:

> 每个 token 的最终输出是所有值向量的加权求和：

```
output_i = sum( attention_weight[i][j] * v_j  for all j )

For token 1:
  output_1 = 0.52 * v1 + 0.09 * v2 + 0.07 * v3 + 0.14 * v4 + 0.08 * v5
```

### Full Pipeline | 完整流水线

```
                    +-------+
  X (input)  ----->|  @ Wq  |-----> Q
                    +-------+
                    +-------+
  X (input)  ----->|  @ Wk  |-----> K
                    +-------+                     +----------+
                    +-------+                     |          |
  X (input)  ----->|  @ Wv  |-----> V ---------->| weighted |----> output
                    +-------+          ^          |   sum    |
                                       |          +----------+
                              +--------+--------+
                              |    softmax      |
                              +---------+-------+
                                        ^
                              +---------+-------+
                              | Q @ K^T / sqrt  |
                              +-----------------+
```

Formula in one line:

> 一行公式：

```
Attention(Q, K, V) = softmax( Q @ K^T / sqrt(dk) ) @ V
```

## Build It | 动手实现

### Step 1: Softmax from scratch | 步骤 1：从零实现 Softmax

Softmax converts raw logits into probabilities. Subtract the max for numerical stability.

> Softmax 将原始 logits 转换为概率。减去最大值以确保数值稳定性。

```python
import numpy as np

def softmax(x):
    shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

logits = np.array([2.0, 1.0, 0.1])
print(f"logits:  {logits}")
print(f"softmax: {softmax(logits)}")
print(f"sum:     {softmax(logits).sum():.4f}")
```

### Step 2: Scaled dot-product attention | 步骤 2：缩放点积注意力

The core function. Takes Q, K, V matrices and returns the attention output plus the weight matrix.

> 核心函数。接收 Q、K、V 矩阵，返回注意力输出和权重矩阵。

```python
def scaled_dot_product_attention(Q, K, V):
    dk = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(dk)
    weights = softmax(scores)
    output = weights @ V
    return output, weights
```

### Step 3: Self-attention class with learned projections | 步骤 3：带学习投影的自注意力类

A full self-attention module with Wq, Wk, Wv weight matrices initialized with Xavier-like scaling.

> 一个完整的自注意力模块，包含 Wq、Wk、Wv 权重矩阵，使用 Xavier 式缩放初始化。

```python
class SelfAttention:
    def __init__(self, d_model, dk, dv, seed=42):
        rng = np.random.default_rng(seed)
        scale = np.sqrt(2.0 / (d_model + dk))
        self.Wq = rng.normal(0, scale, (d_model, dk))
        self.Wk = rng.normal(0, scale, (d_model, dk))
        scale_v = np.sqrt(2.0 / (d_model + dv))
        self.Wv = rng.normal(0, scale_v, (d_model, dv))
        self.dk = dk

    def forward(self, X):
        Q = X @ self.Wq
        K = X @ self.Wk
        V = X @ self.Wv
        output, weights = scaled_dot_product_attention(Q, K, V)
        return output, weights
```

### Step 4: Run it on a sentence | 步骤 4：在句子上运行

Create fake embeddings for a sentence and watch the attention weights.

> 为一个句子创建伪嵌入，观察注意力权重。

```python
sentence = ["The", "cat", "sat", "on", "the", "mat"]
n_tokens = len(sentence)
d_model = 8
dk = 4
dv = 4

rng = np.random.default_rng(42)
X = rng.normal(0, 1, (n_tokens, d_model))

attn = SelfAttention(d_model, dk, dv, seed=42)
output, weights = attn.forward(X)

print("Attention weights (each row: where that token looks):\n")
print(f"{'':>6}", end="")
for token in sentence:
    print(f"{token:>6}", end="")
print()

for i, token in enumerate(sentence):
    print(f"{token:>6}", end="")
    for j in range(n_tokens):
        w = weights[i][j]
        print(f"{w:6.3f}", end="")
    print()
```

### Step 5: Visualize attention with ASCII heatmap | 步骤 5：用 ASCII 热力图可视化注意力

Map attention weights to characters for a quick visual.

> 将注意力权重映射到字符以快速可视化。

```python
def ascii_heatmap(weights, tokens, chars=" ░▒▓█"):
    n = len(tokens)
    print(f"\n{'':>6}", end="")
    for t in tokens:
        print(f"{t:>6}", end="")
    print()

    for i in range(n):
        print(f"{tokens[i]:>6}", end="")
        for j in range(n):
            level = int(weights[i][j] * (len(chars) - 1) / weights.max())
            level = min(level, len(chars) - 1)
            print(f"{'  ' + chars[level] + '   '}", end="")
        print()

ascii_heatmap(weights, sentence)
```

## Use It | 用框架实现

PyTorch's `nn.MultiheadAttention` does exactly what we built, plus multi-head splitting and output projection:

> PyTorch 的 `nn.MultiheadAttention` 完全实现了我们构建的内容，加上多头拆分和输出投影：

```python
import torch
import torch.nn as nn

d_model = 8
n_heads = 2
seq_len = 6

mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads, batch_first=True)

X_torch = torch.randn(1, seq_len, d_model)

output, attn_weights = mha(X_torch, X_torch, X_torch)

print(f"Input shape:            {X_torch.shape}")
print(f"Output shape:           {output.shape}")
print(f"Attention weight shape: {attn_weights.shape}")
print(f"\nAttn weights (averaged over heads):")
print(attn_weights[0].detach().numpy().round(3))
```

The key difference: multi-head attention runs multiple attention functions in parallel, each with its own Q, K, V projections of size dk = d_model / n_heads, then concatenates results. This lets the model attend to different relationship types simultaneously.

> 关键区别：多头注意力并行运行多个注意力函数，每个都有自己的 Q、K、V 投影，大小为 dk = d_model / n_heads，然后拼接结果。这让模型能同时关注不同类型的关系。

> **【中文解读】** PyTorch 的 `nn.MultiheadAttention` 封装了我们从零实现的所有逻辑，加上多头拆分和输出投影。多头注意力的优势在于让模型同时关注不同类型的关系——一个头可能关注语法关系，另一个关注语义关系，还有一个关注位置关系。

> **【拓展：多头注意力的生物学类比】** 多头注意力可以类比视觉皮层的多个特征检测器。就像 V1 区域的不同神经元分别检测边缘、方向、颜色一样，不同的注意力头学习捕捉不同类型的 token 间关系。研究表明，Transformer 的不同头确实学到了不同的语言模式：有的关注相邻词，有的关注句法依赖，有的关注指代关系。

## Ship It | 产出物

This lesson produces:
- `outputs/prompt-attention-explainer.md` — a prompt for explaining attention through the database lookup analogy

> 本课产生：
> - `outputs/prompt-attention-explainer.md` — 通过数据库查找类比解释注意力的提示词

## Exercises | 练习题

1. Modify `scaled_dot_product_attention` to accept an optional mask matrix that sets certain positions to negative infinity before softmax (this is how causal/decoder masking works)
   修改 `scaled_dot_product_attention` 以接受可选的掩码矩阵，在 softmax 前将某些位置设为负无穷（这就是因果/解码器掩码的工作方式）

2. Implement multi-head attention from scratch: split Q, K, V into `n_heads` chunks, run attention on each, concatenate, and project through a final weight matrix Wo
   从零实现多头注意力：将 Q、K、V 拆分为 `n_heads` 块，分别运行注意力，拼接，并通过最终权重矩阵 Wo 投影

3. Take two different sentences of the same length, feed them through the same SelfAttention instance, and compare their attention patterns. What changes? What stays the same?
   取两个相同长度的不同句子，通过同一个 SelfAttention 实例，比较它们的注意力模式。什么变了？什么保持不变？

## Key Terms | 术语速查表

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Query (Q) | "The question vector" / "问题向量" | A learned projection of the input that represents what information this token is looking for. 输入的学习投影，表示这个 token 在寻找什么信息。 |
| Key (K) | "The label vector" / "标签向量" | A learned projection that represents what information this token contains, matched against queries. 学习投影，表示这个 token 包含什么信息，与查询匹配。 |
| Value (V) | "The content vector" / "内容向量" | A learned projection carrying the actual information that gets aggregated based on attention scores. 学习投影，携带根据注意力分数聚合的实际信息。 |
| Scaled dot-product attention | "The attention formula" / "注意力公式" | softmax(QK^T / sqrt(dk)) @ V — scaling prevents softmax saturation in high dimensions. softmax(QK^T / sqrt(dk)) @ V — 缩放防止高维时 softmax 饱和。 |
| Self-attention | "The token looks at itself and others" / "token 看自己和其他 token" | Attention where Q, K, V all come from the same sequence, letting every position attend to every other position. Q、K、V 都来自同一序列的注意力，让每个位置关注所有其他位置。 |
| Attention weights | "How much focus" / "多少关注" | A probability distribution over positions, produced by softmax over scaled dot products. 位置上的概率分布，由缩放点积上的 softmax 产生。 |
| Multi-head attention | "Parallel attention" / "并行注意力" | Running multiple attention functions with different projections, then concatenating results for richer representations. 使用不同投影运行多个注意力函数，然后拼接结果以获得更丰富的表示。 |

## Further Reading | 延伸阅读

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — the original transformer paper
  Vaswani 等人（2017）— 原始 Transformer 论文

- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — best visual walkthrough of the full architecture
  Jay Alammar 的可视化 Transformer — 最佳完整架构可视化讲解

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) — line-by-line PyTorch implementation with explanations
  Harvard NLP 的注释版 Transformer — 逐行 PyTorch 实现与解释

> **【拓展：Flash Attention 与注意力优化】** 标准 self-attention 的 O(N^2) 内存开销是长序列处理的瓶颈。Flash Attention（2022）通过分块计算和重计算策略，在不改变数学结果的情况下将内存复杂度降至 O(N)。这在 GPT-4 的 128K 上下文窗口等实际应用中至关重要。
