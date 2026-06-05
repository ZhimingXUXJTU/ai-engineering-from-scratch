# Attention Variants — Sliding Window, Sparse, Differential | 注意力变体 — 滑动窗口、稀疏、差分注意力

> Full attention is a circle. Every token sees every token, and memory pays the price. Four variants bend the shape of the circle and recover half the cost.

> **【中文解读】** 标准注意力的 O(n^2) 复杂度太昂贵。滑动窗口注意力(Mistral)、稀疏注意力、差分注意力是降低复杂度的方法。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Full attention costs `O(N²)` memory and `O(N²)` compute in sequence length. For a 128K-context Llama 3 70B that is 16 billion attention entries per layer, times 80 layers. Flash Attention (Lesson 12) hides the `O(N²)` activation memory but does not change the arithmetic cost — every token still attends to every other token.

> 全注意力在序列长度上的内存和计算成本都是 `O(N²)`。对于 128K 上下文的 Llama 3 70B，那是每层 160 亿个注意力条目，乘以 80 层。Flash Attention（第 12 课）隐藏了 `O(N²)` 的激活内存，但不改变算术成本——每个 token 仍然关注每个其他 token。

Three classes of variants change the topology of the attention matrix itself:

> 三类变体改变了注意力矩阵本身的拓扑结构：

1. **Sliding window attention (SWA).** Each token attends to a fixed window of neighbors, not the full prefix. Memory and compute drop to `O(N · W)` where `W` is the window. Gemma 2/3, Mistral 7B's first layers, Phi-3-Long.
   中文翻译：**滑动窗口注意力 (SWA)。** 每个 token 只关注固定窗口的邻域，而非完整前缀。内存和计算降到 `O(N · W)`，其中 `W` 是窗口大小。Gemma 2/3、Mistral 7B 的前几层、Phi-3-Long。
2. **Sparse / block attention.** Only selected pairs `(i, j)` get scored; the rest are forced to zero weight. Longformer, BigBird, OpenAI sparse transformer.
   中文翻译：**稀疏/块注意力。** 只有选定的 `(i, j)` 对被评分；其余被迫为零权重。Longformer、BigBird、OpenAI 稀疏 Transformer。
3. **Differential attention.** Compute two attention maps with separate Q/K projections, subtract one from the other. Kills the "attention sink" that bleeds weight into the first few tokens. Microsoft's DIFF Transformer (2024).
   中文翻译：**差分注意力。** 用独立的 Q/K 投影计算两个注意力图，将一个从另一个中减去。消除将权重汇聚到前几个 token 的"注意力汇聚"现象。Microsoft 的 DIFF Transformer（2024）。

These coexist. A 2026 frontier model often mixes them: most layers are SWA-1024, every fifth is global full attention, and a handful are differential heads that clean up retrieval. Gemma 3's 5:1 SWA-to-global ratio is the current textbook default.

> 它们可以共存。一个 2026 年的前沿模型通常混合使用：大多数层是 SWA-1024，每第五层是全局全注意力，少数是清理检索的差分头。Gemma 3 的 5:1 SWA 与全局注意力比例是当前的教科书默认配置。

> **【中文解读】** 三种降低注意力复杂度的方法：(1) 滑动窗口（SWA）——只关注局部邻域，O(N*W) 复杂度；(2) 稀疏/块注意力——只计算选定的 token 对；(3) 差分注意力——两组 Q/K 注意力相减，消除"注意力汇聚"现象。2026 年的模型通常混合使用这些变体。

## The Concept | 核心概念

### Sliding Window Attention (SWA)

Each query at position `i` attends only to positions in `[i - W, i]` (causal SWA) or `[i - W/2, i + W/2]` (bidirectional). Tokens outside the window get `-inf` in the score matrix.

> 位置 `i` 的每个查询只关注 `[i - W, i]`（因果 SWA）或 `[i - W/2, i + W/2]`（双向）范围内的位置。窗口外的 token 在分数矩阵中获得 `-inf`。

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

For `N = 8192` and `W = 1024`, the score matrix has 1024 × 8192 non-zero rows in expectation — an 8× reduction.

> 对于 `N = 8192` 和 `W = 1024`，分数矩阵预期有 1024 × 8192 个非零行——减少了 8 倍。

**KV cache shrinks with SWA.** Only the last `W` tokens of K and V need to be kept per layer. For a Gemma-3-ish config (1024 window, 128K context), KV cache drops 128×.

> **KV 缓存随 SWA 缩小。** 每层只需保留 K 和 V 的最后 `W` 个 token。对于类 Gemma-3 的配置（1024 窗口，128K 上下文），KV 缓存减少 128 倍。

**Quality cost.** SWA-only transformers struggle with long-range retrieval. The fix: interleave SWA layers with full-attention layers. Gemma 3 uses 5:1 SWA:global. Mistral 7B used a causal-SWA stack where information "flows forward" through overlapping windows — each layer extends effective receptive field by `W`, and after `L` layers the model can attend `L × W` tokens back.

> **质量代价。** 纯 SWA Transformer 在长距离检索上表现不佳。修复方案：将 SWA 层与全注意力层交替使用。Gemma 3 使用 5:1 的 SWA:全局比例。Mistral 7B 使用因果 SWA 堆栈，信息通过重叠窗口"向前流动"——每层将有效感受野扩展 `W`，`L` 层后模型可以回溯 `L × W` 个 token。

### Sparse / Block Attention

Pick an `N × N` sparsity pattern ahead of time. Three canonical shapes:

> 预先选择 `N × N` 的稀疏模式。三种经典形状：

- **Local + strided (OpenAI sparse transformer).** Attend to the last `W` tokens plus every `stride`-th token before that. Captures both local and long-range at `O(N · sqrt(N))` compute.
  中文翻译：**局部 + 步进（OpenAI 稀疏 Transformer）。** 关注最后 `W` 个 token 加上之前每隔 `stride` 个 token。以 `O(N · sqrt(N))` 的计算量同时捕获局部和长距离信息。
- **Longformer / BigBird.** Local window + a small set of global tokens (e.g. `[CLS]`) that attend to everyone and are attended by everyone + random-sparse links. Empirical 2× context at matched quality.
  中文翻译：**Longformer / BigBird。** 局部窗口 + 少量全局 token（如 `[CLS]`）与所有 token 双向关注 + 随机稀疏连接。实验表明在相同质量下上下文扩展 2 倍。
- **Native Sparse Attention (DeepSeek, 2025).** Learn which blocks of `(Q, K)` matter; skip the zero blocks at kernel level. FlashAttention-compatible.
  中文翻译：**原生稀疏注意力（DeepSeek，2025）。** 学习哪些 `(Q, K)` 块重要；在内核级别跳过零块。与 FlashAttention 兼容。

Sparse attention is a kernel-engineering story. The math is simple (mask the score matrix); the win comes from never loading the zero entries into SRAM. FlashAttention-3 and the 2026 FlexAttention API make custom sparse patterns first-class in PyTorch.

> 稀疏注意力是一个内核工程的故事。数学很简单（掩码分数矩阵）；优势来自从不将零条目加载到 SRAM。FlashAttention-3 和 2026 年的 FlexAttention API 使自定义稀疏模式在 PyTorch 中成为一等公民。

> **【拓展：滑动窗口的信息传递机制】** 滑动窗口注意力看似只能捕获局部信息，但通过多层堆叠，信息可以"渗透"到更远的位置。W 窗口的 L 层注意力，有效感受野为 L×W。例如 W=1024、L=32 的模型有效感受野为 32K token。Mistral 7B 正是利用了这个特性在保持 O(N*W) 计算复杂度的同时实现长上下文建模。

### Differential Attention (DIFF Transformer, 2024)

Regular attention has an "attention sink" problem: softmax forces every row to sum to 1, so tokens that don't want to attend to anything in particular dump weight on the first token (or the first few). This steals capacity that should have gone to real content.

> 标准注意力有"注意力汇聚"问题：softmax 强制每行总和为 1，所以不想关注任何特定内容的 token 会将权重倾倒到第一个 token（或前几个）。这窃取了本应用于真实内容的容量。

Differential attention fixes this by computing **two** attention maps and subtracting:

> 差分注意力通过计算**两个**注意力图并相减来修复这个问题：

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

where `λ` is a learned scalar (typically 0.5–0.8). A1 captures real content weights; A2 captures the sink. Subtraction cancels the sink, reallocates weight to relevant tokens.

> 其中 `λ` 是一个学习到的标量（通常 0.5-0.8）。A1 捕获真实内容权重；A2 捕获汇聚。相减消除汇聚，将权重重新分配给相关 token。

Reported results (Microsoft 2024): 5–10% lower perplexity, 1.5–2× longer effective context at same trained length, sharper needle-in-haystack retrieval.

> 报告结果（Microsoft 2024）：困惑度降低 5-10%，相同训练长度下有效上下文长度增加 1.5-2 倍，needle-in-haystack 检索更精确。

> **【中文解读】** 差分注意力的创新之处：标准注意力因 softmax 归一化导致"注意力汇聚"（attention sink）——不相关的 token 把权重集中在序列开头的 token 上。差分注意力计算两组注意力并相减，A1 捕获真实内容权重，A2 捕获汇聚噪声，相减后消除汇聚现象。困惑度降低 5-10%。

> **【拓展：Gemma 3 的混合注意力策略】** Google 的 Gemma 3 使用 5:1 的滑动窗口与全局注意力比例——每 5 层局部注意力后接 1 层全局注意力。这既保持了长上下文的建模能力（全局层提供远程连接），又大幅降低了计算成本（局部层只有 O(N*W) 复杂度）。这种混合策略已成为 2026 年长上下文模型的标准范式。

### Variant Comparison

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Build It | 动手实现

See `code/main.py`. We implement a causal mask comparator that shows full, SWA, local+strided, and differential attention side by side on a toy sequence.

> 参见 `code/main.py`。我们实现一个因果掩码比较器，在玩具序列上并排展示全注意力、SWA、局部+步进和差分注意力。

### Step 1: full causal mask (baseline)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Baseline from Lesson 07. Lower triangular; zero weight above the diagonal.

> 第 07 课的基线。下三角；对角线上方权重为零。

### Step 2: sliding window causal mask

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

One parameter — `window`. For `window >= n`, you recover full causal attention. For `window = 1`, each token attends only to itself.

> 一个参数——`window`。当 `window >= n` 时，恢复为全因果注意力。当 `window = 1` 时，每个 token 只关注自身。

### Step 3: local + strided sparse mask

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

Dense local window plus every `stride`-th token back to the start of the sequence. Receptive field grows in log steps with additional layers.

> 密集局部窗口加上从序列开头每隔 `stride` 个 token。感受野随层数以对数步长增长。

### Step 4: differential attention

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

Two attention passes, subtract with a learned mixing coefficient. In the code we compare the attention-sink heatmap of single vs differential and watch the sink collapse.

> 两次注意力计算，用学习到的混合系数相减。在代码中我们比较单次注意力与差分注意力的汇聚热图，观察汇聚现象的消除。

### Step 5: KV cache sizes

Print the cache size per layer at `N = 131072` for each variant. SWA and sparse variants drop by 10–100×. Differential doubles. Pay your memory bill consciously.

> 打印 `N = 131072` 时每种变体每层的缓存大小。SWA 和稀疏变体减少 10-100 倍。差分变体翻倍。要有意识地管理你的内存开销。

## Use It | 用框架实现

2026 production patterns:

> 2026 年生产模式：

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

FlexAttention in PyTorch 2.5+ accepts a mask function:

> PyTorch 2.5+ 中的 FlexAttention 接受掩码函数：

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

This compiles to a custom Triton kernel. Within 10% of FlashAttention-3 speed for common patterns, and the mask function is a Python callable.

> 这会编译为自定义 Triton 内核。对于常见模式，速度在 FlashAttention-3 的 10% 以内，且掩码函数是一个 Python 可调用对象。

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** — every layer up to ~16K context, or when retrieval quality is paramount.
  中文翻译：**纯全注意力** — 每层都用到约 16K 上下文，或检索质量至关重要的场景。
- **SWA + global mix** — long context (>32K), training and inference memory-bound. The 2026 default above 32K.
  中文翻译：**SWA + 全局混合** — 长上下文（>32K），训练和推理受内存约束。32K 以上的 2026 年默认配置。
- **Sparse block attention** — custom kernel, custom pattern. Reserved for specialized workloads (retrieval, audio).
  中文翻译：**稀疏块注意力** — 自定义内核，自定义模式。专用于特殊工作负载（检索、音频）。
- **Differential attention** — any workload where attention-sink contamination hurts (long-context RAG, needle-in-haystack).
  中文翻译：**差分注意力** — 注意力汇聚污染有害的任何工作负载（长上下文 RAG、needle-in-haystack）。

## Ship It | 产出物

See `outputs/skill-attention-variant-picker.md`. The skill picks an attention topology for a new model given target context length, retrieval demands, and training/inference compute profile.

> 参见 `outputs/skill-attention-variant-picker.md`。该 skill 根据目标上下文长度、检索需求和训练/推理计算配置，为新模型选择注意力拓扑。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Verify SWA at `window=4` zeroes everything outside the last 4 tokens per row. Verify `window=n` reproduces full causal attention bit-identically.
   中文翻译：运行 `code/main.py`。验证 `window=4` 的 SWA 将每行最后 4 个 token 之外的所有内容置零。验证 `window=n` 能逐位复现全因果注意力。
2. **Medium.** Implement causal SWA with `window=1024` on top of the Lesson 07 capstone. Train for 1,000 steps on tinyshakespeare. How much does val loss regress vs full attention? How much does peak memory drop?
   中文翻译：在第 07 课毕业项目上实现 `window=1024` 的因果 SWA。在 tinyshakespeare 上训练 1,000 步。验证损失比全注意力回退多少？峰值内存降低多少？
3. **Hard.** Implement a Gemma-3-style 5:1 layer mix (5 SWA, 1 global) in the capstone model. Compare loss, memory, and generation quality against pure-SWA and pure-global baselines at matched parameters.
   中文翻译：在毕业项目模型中实现类 Gemma-3 的 5:1 层混合（5 层 SWA、1 层全局）。在匹配参数量下与纯 SWA 和纯全局基线比较损失、内存和生成质量。
4. **Hard.** Implement differential attention with a learned `λ` per head. Train on a synthetic retrieval task (one needle, 2,000 distractors). Measure retrieval accuracy vs a single-attention baseline at matched parameters.
   中文翻译：实现每个头有学习 `λ` 的差分注意力。在合成检索任务（一个针、2,000 个干扰项）上训练。在匹配参数量下与单注意力基线比较检索准确率。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Further Reading | 延伸阅读

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) — the canonical sliding-window + global-token paper.
  中文翻译：Longformer 论文，经典的滑动窗口 + 全局 token 方案。
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062) — local + global + random.
  中文翻译：BigBird 论文，局部 + 全局 + 随机模式。
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) — OpenAI's local+strided pattern.
  中文翻译：OpenAI 稀疏 Transformer 论文，局部+步进模式。
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) — the 1:1 SWA:global mix.
  中文翻译：Gemma 2 论文，1:1 SWA 与全局混合。
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) — the 5:1 mix with window=1024 that's now the textbook default.
  中文翻译：Gemma 3 技术报告，5:1 混合，窗口=1024，现已成为教科书默认。
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) — DIFF Transformer paper.
  中文翻译：DIFF Transformer 论文。
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089) — DeepSeek-V3.2's learned-sparsity attention.
  中文翻译：DeepSeek-V3.2 的原生稀疏注意力论文。
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) — API reference for the mask-as-callable pattern in Use It.
  中文翻译：PyTorch FlexAttention 文档，掩码即可调用模式的 API 参考。
