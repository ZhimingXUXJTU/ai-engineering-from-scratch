# Self-Attention from Scratch | 自注意力从零实现

> Attention is a lookup table where every word asks "who matters to me?" - and learns the answer.

> **【中文解读】** Self-Attention 是 Transformer 的核心：Q*K^T 计算每个 token 对其他 token 的关注度。理解 Q/K/V 的直觉是理解 GPT/BERT 的基础。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 Lesson 10 (Sequence-to-Sequence)
**Time:** ~90 minutes

## Learning Objectives

- Implement scaled dot-product self-attention from scratch using only NumPy, including query/key/value projections and the softmax-weighted sum
- Build a multi-head attention layer that splits heads, computes parallel attention, and concatenates results
- Trace how the attention matrix captures token relationships and explain why scaling by sqrt(d_k) prevents softmax saturation
- Apply causal masking to convert bidirectional attention into autoregressive (decoder-style) attention

> **【中文解读】** 学习目标：1) 用纯 NumPy 实现缩放点积自注意力，包括 Q/K/V 投影和 softmax 加权求和；2) 构建多头注意力层；3) 追踪注意力矩阵如何捕获 token 关系，理解为什么除以 sqrt(d_k) 防止 softmax 饱和；4) 应用因果掩码实现自回归注意力。

## The Problem

RNNs process sequences one token at a time. By the time you reach token 50, the information from token 1 has been squeezed through 50 compression steps. Long-range dependencies get crushed into a fixed-size hidden state - a bottleneck that no amount of LSTM gating fully solves.

The 2014 Bahdanau attention paper showed the fix: let the decoder look back at every encoder position and decide which ones matter for the current step. But it was still bolted onto an RNN. The 2017 "Attention Is All You Need" paper asked a sharper question: what if attention is the *only* mechanism? No recurrence. No convolution. Just attention.

Self-attention lets every position in a sequence attend to every other position in a single parallel step. That is what makes transformers fast, scalable, and dominant.

> **【中文解读】** RNN 的根本瓶颈：信息必须经过逐步压缩，长距离依赖被"压碎"在固定大小的隐状态中。2014 年 Bahdanau 注意力证明了"回头看"的必要性，但仍然依附于 RNN。2017 年 "Attention Is All You Need" 提出更激进的问题——如果注意力是唯一机制会怎样？自注意力让序列中的每个位置在一步并行操作中就能关注所有其他位置，这就是 Transformer 快速、可扩展、统治一切的根源。

> **【拓展：从 Bahdanau 到 Transformer 的演进】** Bahdanau 注意力（2014）是 seq2seq 模型的附加组件，Luong 注意力（2015）简化了它的计算方式。Transformer（2017）的关键洞察是：与其在 RNN 上"外挂"注意力，不如把注意力作为核心计算单元，完全去掉循环结构。这一转变使训练可以高度并行化，直接催生了 GPT 和 BERT。

## The Concept

### The Database Lookup Analogy

Think of attention as a soft database lookup:

```
Traditional database:
  Query: "capital of France"  -->  exact match  -->  "Paris"

Attention:
  Query: "capital of France"  -->  similarity to ALL keys  -->  weighted blend of ALL values
```

Every token generates three vectors:
- **Query (Q)**: "What am I looking for?"
- **Key (K)**: "What do I contain?"
- **Value (V)**: "What information do I provide if selected?"

The dot product between a query and all keys produces attention scores. High score means "this key matches my query." Those scores weight the values. The output is a weighted sum of values.

> **【中文解读】** 注意力的数据库查找类比：传统数据库做精确匹配（"法国首都" → "巴黎"），注意力做模糊匹配——Query 与所有 Key 计算相似度，得到一个权重分布，最终输出所有 Value 的加权和。每个 token 生成三个向量：Q（我在找什么）、K（我包含什么）、V（如果被选中我提供什么信息）。

### Q, K, V Computation

Each token embedding gets projected through three learned weight matrices:

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

### The Attention Matrix

Once you have Q, K, V for all tokens, attention scores form a matrix:

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

> **【中文解读】** 注意力矩阵是 Self-Attention 的核心产物：一个 N×N 的矩阵，每一行代表一个 token 对所有 token 的关注度分布。对角线上通常分数较高（自己最关注自己），但非对角线的高分位置揭示了 token 之间的语义关系——比如句法依赖、指代消解等。

### Why Scale?

The dot products grow with dimension dk. If dk = 64, dot products can be in the range of tens, pushing softmax into regions where gradients vanish. The fix: divide by sqrt(dk).

```
Scaled scores = (Q @ K^T) / sqrt(dk)
```

This keeps values in a range where softmax produces useful gradients.

> **【中文解读】** 为什么要缩放？当维度 dk 较大时（如 64），Q 和 K 的点积数值可能达到数十甚至上百，这会将 softmax 推入饱和区（梯度接近零）。解决方案：除以 sqrt(dk)，将数值保持在 softmax 能产生有效梯度的范围内。这是 Transformer 论文中一个看似简单但至关重要的技巧。

### Softmax Turns Scores into Weights

Softmax converts raw scores into a probability distribution across each row:

```
Raw scores for q1:   [2.1, 0.3, 0.1, 0.8, 0.2]
                            |
                         softmax
                            |
Attention weights:   [0.52, 0.09, 0.07, 0.14, 0.08]   (sums to ~1.0)
```

Now each token has a set of weights saying how much to attend to every other token.

> **【中文解读】** Softmax 将原始注意力分数转换为概率分布：每行总和为 1.0，每个值代表"我有多关注这个位置"。以示例来看，q1 对 k1 的权重为 0.52（最高），说明 token 1 最关注自身，但也分配了少量注意力给 k4（0.14）。这种"软"注意力机制允许模型同时考虑多个信息源。

### Weighted Sum of Values

The final output for each token is a weighted sum of all value vectors:

```
output_i = sum( attention_weight[i][j] * v_j  for all j )

For token 1:
  output_1 = 0.52 * v1 + 0.09 * v2 + 0.07 * v3 + 0.14 * v4 + 0.08 * v5
```

### Full Pipeline

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

```
Attention(Q, K, V) = softmax( Q @ K^T / sqrt(dk) ) @ V
```

> **【中文解读】** 完整的缩放点积注意力公式，一行搞定：先计算 Q 和 K 的点积（相似度），除以 sqrt(dk)（缩放），过 softmax（归一化为概率分布），最后与 V 做矩阵乘法（加权求和）。这个公式是 GPT、BERT、T5、Llama 等所有 Transformer 模型的共同基础。

> **【拓展：从自注意力到 Flash Attention】** 上述公式的朴素实现在长序列上内存消耗为 O(N²)——一个 8K 序列需要 64M 个浮点数的注意力矩阵。Flash Attention（2022）通过分块计算（tiling）和在线 softmax，将内存从 O(N²) 降到 O(N)，同时计算速度反而更快（减少了 HBM 读写次数）。2026 年所有主流推理框架都默认启用 Flash Attention。

## Build It

### Step 1: Softmax from scratch

Softmax converts raw logits into probabilities. Subtract the max for numerical stability.

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

### Step 2: Scaled dot-product attention

The core function. Takes Q, K, V matrices and returns the attention output plus the weight matrix.

```python
def scaled_dot_product_attention(Q, K, V):
    dk = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(dk)
    weights = softmax(scores)
    output = weights @ V
    return output, weights
```

### Step 3: Self-attention class with learned projections

A full self-attention module with Wq, Wk, Wv weight matrices initialized with Xavier-like scaling.

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

### Step 4: Run it on a sentence

Create fake embeddings for a sentence and watch the attention weights.

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

### Step 5: Visualize attention with ASCII heatmap

Map attention weights to characters for a quick visual.

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

## Use It

PyTorch's `nn.MultiheadAttention` does exactly what we built, plus multi-head splitting and output projection:

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

> **【中文解读】** PyTorch 的 `nn.MultiheadAttention` 封装了我们手写的全部逻辑：Q/K/V 投影、多头分割、并行注意力计算、结果拼接。关键区别在于多头注意力——多组独立的 Q/K/V 投影并行运行，每组关注不同类型的关系（如语法、语义、位置），最后拼接并线性投影输出。

## Ship It

This lesson produces:
- `outputs/prompt-attention-explainer.md` - a prompt for explaining attention through the database lookup analogy

## Exercises

1. Modify `scaled_dot_product_attention` to accept an optional mask matrix that sets certain positions to negative infinity before softmax (this is how causal/decoder masking works)
2. Implement multi-head attention from scratch: split Q, K, V into `n_heads` chunks, run attention on each, concatenate, and project through a final weight matrix Wo
3. Take two different sentences of the same length, feed them through the same SelfAttention instance, and compare their attention patterns. What changes? What stays the same?

## Key Terms

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Query (Q) | "The question vector" | A learned projection of the input that represents what information this token is looking for | 查询向量——"我在找什么信息" |
| Key (K) | "The label vector" | A learned projection that represents what information this token contains, matched against queries | 键向量——"我包含什么信息" |
| Value (V) | "The content vector" | A learned projection carrying the actual information that gets aggregated based on attention scores | 值向量——"我提供的实际内容" |
| Scaled dot-product attention | "The attention formula" | softmax(QK^T / sqrt(dk)) @ V - scaling prevents softmax saturation in high dimensions | 缩放点积注意力——Transformer 的核心公式 |
| Self-attention | "The token looks at itself and others" | Attention where Q, K, V all come from the same sequence, letting every position attend to every other position | 自注意力——Q/K/V 来自同一序列 |
| Attention weights | "How much focus" | A probability distribution over positions, produced by softmax over scaled dot products | 注意力权重——每个位置的关注度分布 |
| Multi-head attention | "Parallel attention" | Running multiple attention functions with different projections, then concatenating results for richer representations | 多头注意力——多组并行注意力捕获不同关系 |

## Further Reading

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) - the original transformer paper
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) - best visual walkthrough of the full architecture
- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) - line-by-line PyTorch implementation with explanations
