# Differential Attention (V2) | 差分注意力 (V2)

> Softmax attention spreads a small amount of probability over every non-matching token. Over 100k tokens that noise adds up and drowns the signal. Differential Transformer (Ye et al., ICLR 2025) fixes it by computing attention as the difference of two softmaxes, subtracting the shared noise floor. DIFF V2 (Microsoft, January 2026) is the production-stack rewrite: matching decode latency to baseline Transformer, no custom kernels, FlashAttention-compatible. This lesson is V1 to V2 end-to-end, with a working toy implementation of the difference operation you can run in stdlib Python.

> **【中文解读】** Softmax 注意力给每个不匹配的 token 分配微小概率，在 100K token 的上下文中噪声累积淹没信号。差分 Transformer 用两个 softmax 的差值减去共享噪声基底。DIFF V2 是微软 2026 年的生产级重写，兼容 FlashAttention。

> **【拓展：长上下文优化】** 差分注意力是长上下文 LLM 优化的重要方向之一。100K+ token 的上下文窗口中，标准注意力的"注意力稀释"问题日益严重，差分注意力提供了一种不牺牲推理速度的解决方案。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 02 (self-attention), Phase 7 · 15 (attention variants), Phase 10 · 14 (architecture walkthrough)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- State precisely why softmax attention has a noise floor and why it grows with context length.
  精确说明 softmax 注意力为什么存在噪声基底，以及为什么它随上下文长度增长
- Derive the differential attention formula and explain why the subtraction cancels the shared noise component while preserving signal.
  推导差分注意力公式，解释为什么减法能消除共享噪声分量同时保留信号
- Walk the V1-to-V2 diff: what got faster, what got simpler, what got more stable, and why each change was necessary for production pre-training.
  梳理 V1 到 V2 的差异：什么变快了、简化了、稳定了，以及为什么每项修改对生产预训练必要
- Implement differential attention from scratch in pure Python and empirically verify the noise-cancellation property on a synthetic signal-plus-noise query.
  用纯 Python 从零实现差分注意力，在合成信号加噪声查询上实验验证噪声消除特性

## The Problem | 问题引入

Standard softmax attention has a mathematical property that turns into an operational headache at scale. For a query `q`, the attention weights are `softmax(qK^T / sqrt(d))`. Softmax can never produce exact zeros — every non-matching token gets some positive mass. That residual mass is noise, and it scales with context length. At 128k tokens, even if each non-matching token gets only 0.001% of the probability, 127,999 of them combined contribute about 12% of the total. The model has to learn to route around a noise floor that grows with context.

> 标准 softmax 注意力有一个数学特性，在规模上变成操作上的头痛。对于查询 `q`，注意力权重是 `softmax(qK^T / sqrt(d))`。Softmax 永远不能产生精确零——每个不匹配的 token 都获得一些正质量。那个残余质量是噪声，且随上下文长度增长。在 128k token 时，即使每个不匹配 token 只获得 0.001% 的概率，127,999 个加起来贡献了约 12%。模型必须学会绕过一个随上下文增长的噪声底。

Empirically this shows up as attention-head interference: hallucinated citations in long-context RAG, lost-in-the-middle failures on 100k-token retrieval tasks, and subtle accuracy degradation on needle-in-haystack benchmarks past 32k. The Differential Transformer paper (arXiv:2410.05258, ICLR 2025) measured the gap: DIFF Transformers hit lower perplexity, higher long-context accuracy, and fewer hallucinations than same-size baselines.

> 经验上这表现为注意力头干扰：长上下文 RAG 中的幻觉引用、100k token 检索任务的中间丢失失败，以及 32k 以上草堆找针基准测试中的微妙精度下降。Differential Transformer 论文（arXiv:2410.05258，ICLR 2025）测量了差距：DIFF Transformer 达到了更低的困惑度、更高的长上下文精度和更少的幻觉。

DIFF V1 had three problems that kept it out of frontier pre-training pipelines. Its value cache had to be loaded twice per decode step, it required custom CUDA kernels that broke FlashAttention compatibility, and its per-head RMSNorm destabilized long-run training at 70B-plus scale. DIFF V2 (Microsoft unilm blog, January 20, 2026) fixed all three. This lesson walks both versions, builds the difference operator, and benchmarks noise cancellation on a toy query.

## The Concept | 核心概念

> **【中文解读】** 差分注意力（Differential Attention）通过计算两个独立 softmax 的差值来消除注意力噪声，让模型更专注于真正相关的信息。这种方法减少了注意力机制中的注意力分散问题。

> **【拓展：注意力机制的演进】** 从标准 Multi-Head Attention → GQA（分组查询注意力，Llama 2/3 使用）→ MLA（多头潜在注意力，DeepSeek-V2/V3 使用，将 KV-cache 压缩到低维潜在空间）→ 差分注意力。MLA 将 DeepSeek-V3 的 KV-cache 压缩了约 10 倍，是推理效率的关键创新。


### The noise floor of softmax

For a query `q` and keys `K = [k_1, ..., k_N]`, attention weights are:

```
w_i = exp(q . k_i / sqrt(d)) / sum_j exp(q . k_j / sqrt(d))
```

No `w_i` is ever zero. If `k_i` is completely unrelated to `q`, the score `q . k_i` is not 0 — it fluctuates around zero with variance `||q||^2 / d`. After softmax normalization, each unrelated token still contributes `O(1/N)` to the weighted sum. The total contribution of unrelated tokens is `O((N-1)/N) = O(1)` — not a small quantity.

What the model wants is something like a hard top-k: high weight on matching tokens, near-zero weight everywhere else. Softmax is too smooth to do that directly.

### The differential idea

Split each head's Q and K projections into two: Q = (Q_1, Q_2) and K = (K_1, K_2). Compute two attention maps:

```
A_1 = softmax(Q_1 K_1^T / sqrt(d))
A_2 = softmax(Q_2 K_2^T / sqrt(d))
```

Output:

```
DiffAttn = (A_1 - lambda * A_2) V
```

The subtraction cancels whatever noise distribution the two maps share. If both maps have roughly uniform weight on the 127k unrelated tokens (which they will, at random initialization), those cancel. The signal — peaked weight on the few actually relevant tokens — only cancels if it appears in both maps at the same magnitude, which it will not once the model trains.

`lambda` is a learnable scalar per head, parameterized as `lambda = exp(lambda_q1 dot lambda_k1) - exp(lambda_q2 dot lambda_k2) + lambda_init`. It can be negative. `lambda_init` defaults to a small positive number like 0.8.

### Why this matches headed noise-canceling

Think of two noisy microphones recording the same voice. Both pick up the speaker plus correlated background noise. Subtract one from the other and the shared noise drops out. The voice survives because the two signals differ in phase or amplitude by enough to prevent full cancellation. The per-head `lambda` learns exactly this balance.

### V1 vs V2: the diff

V1 kept the parameter count equal to the baseline Transformer. To get two queries per head it halved the head dimension. That cost head expressiveness and — more painfully — halved the value cache per head. Decode had to load the value cache twice per step (once per softmax branch). Result: decode slower than baseline despite matching parameter count.

V2 doubles the number of query heads and keeps the KV heads the same (borrowing parameters from the up-projection). The head dimension stays the same as baseline. After the subtraction, the extra dimension is projected back down to match baseline Transformer's O_W projection. Three things happen at once:

1. Decode speed matches baseline (KV cache is loaded once).
2. FlashAttention runs unchanged (no custom kernel).
3. Arithmetic intensity at decode goes up (more compute per byte loaded from HBM).

V2 also removes the per-head RMSNorm that V1 used to stabilize the subtraction. At 70B-class pre-training scales, that RMSNorm destabilized late training. V2 replaces it with a simpler initialization scheme that keeps training stable without the extra module.

### When to reach for it

| Workload | Benefit |
|----------|---------|
| Long-context RAG (64k+) | Cleaner attention maps, fewer hallucinated citations |
| Needle-in-haystack benchmarks | Substantial accuracy lift past 32k |
| Multi-document QA | Less cross-document interference |
| Code completion at 8k | Marginal, not worth the architecture change |
| Short chat (< 4k) | Essentially indistinguishable from baseline |

The value grows with context length. At 4k tokens the noise floor is small enough that standard attention is fine. At 128k it is hurting you.

### How it stacks with other 2026 knobs

| Feature | Compatible with DIFF V2? |
|---------|------------------------|
| GQA | Yes (V2 increases Q heads, not KV heads) |
| MLA (DeepSeek) | Yes in principle, no published paper combining them |
| MoE | Yes (attention is independent of MLP block) |
| RoPE | Yes (unchanged) |
| YaRN / long-context scaling | Yes (exactly where DIFF helps most) |
| FlashAttention | Yes in V2 (was no in V1) |
| Speculative decoding | Yes (attention change is invisible to the spec-decode loop) |


> **【拓展：注意力机制的关键创新时间线】** 2017 年 Multi-Head Attention 到 2022 年 GQA（Llama 2，减少 KV-cache）到 2024 年 MLA（DeepSeek-V2，KV 压缩到潜在空间）到 2024 年 Differential Attention（消除注意力噪声）。MLA 将 KV-cache 缩小约 10 倍。


## Build It | 动手实现

`code/main.py` implements differential attention in pure Python. A toy query with known signal-plus-noise structure lets you measure the noise-cancellation ratio directly.

### Step 1: standard softmax attention

Stdlib matrix ops: lists of lists, manual matmul, softmax with numerical-stability subtraction of the max.

```python
def softmax(row):
    m = max(row)
    exps = [math.exp(x - m) for x in row]
    s = sum(exps)
    return [e / s for e in exps]
```

### Step 2: split Q, K into two halves

V1 style: halve the head dimension. V2 style: keep the head dimension and double the number of heads. The toy implementation uses V1 for pedagogical clarity — the math is identical, only the bookkeeping differs.

### Step 3: two softmax branches + subtraction

```python
A1 = [softmax([dot(q1, k) / scale for k in K1]) for q1 in Q1]
A2 = [softmax([dot(q2, k) / scale for k in K2]) for q2 in Q2]
diff_weights = [[a1 - lam * a2 for a1, a2 in zip(r1, r2)] for r1, r2 in zip(A1, A2)]
out = [[sum(w * v[j] for w, v in zip(row, V)) for j in range(d_v)] for row in diff_weights]
```

Note: the output weights can be negative. That is fine — the value cache still handles signed contributions. The subsequent V projection absorbs the sign.

### Step 4: noise cancellation measurement

Build a synthetic sequence of length 1024. Place the signal token at a known position, fill the rest with noise. Compute (a) standard softmax attention weight on the signal position and (b) differential attention weight. Measure the ratio of signal-to-noise in each. DIFF attention reliably produces a higher signal-to-noise ratio by a factor of 3x-10x depending on how much the two branches have been trained to differ.

### Step 5: V1 vs V2 parameter accounting

Given a config (hidden=4096, heads=32, d_head=128), print:

- Baseline Transformer: Q, K, V each size `hidden * hidden`, MLP at 4 * hidden.
- DIFF V1: Q, K each size `hidden * hidden`, V size `hidden * hidden` (unchanged), head dim halved internally. Adds per-head `lambda` parameters (O(heads * d_head)).
- DIFF V2: Q size `2 * hidden * hidden`, K size `hidden * hidden`, V size `hidden * hidden`. Extra dim projected back down before O_W. Adds same `lambda` parameters.

The toy measures the extra parameter cost for V2 (roughly `hidden * hidden` extra per attention block) and prints it.

## Use It | 用框架实现

DIFF V2 is not yet shipping in every production inference server as of April 2026, but integration is underway in vLLM and SGLang. Meanwhile the pattern shows up in:

- Microsoft internal long-context production models.
- Research replications in several open model training runs targeting 256k-plus context.
- Hybrid architectures that combine DIFF attention with sliding-window attention on alternate layers.

When you would reach for this in 2026:

- Training a new model from scratch targeting 64k-plus effective context. Add differential attention from the start; retraining later is expensive.
- Fine-tuning a long-context model where lost-in-the-middle failures dominate your eval. A LoRA on the Q projections can approximate the DIFF structure.

When you would not:

- You are serving a pre-trained dense model with stable long-context performance. The retraining cost rarely pays back on existing weights.
- Your context is always under 16k. Noise floor is negligible.

## Ship It | 产出物

This lesson produces `outputs/skill-diff-attention-integrator.md`. Given a model architecture, target context length, hallucination profile, and training budget, it produces an integration plan for adding differential attention to a new pre-training run or LoRA fine-tune.

> 本课产出 `outputs/skill-diff-attention-integrator.md`。给定模型架构、目标上下文长度、幻觉配置和训练预算，它产生将差分注意力集成到新预训练运行或 LoRA 微调的集成计划。

## Exercises | 练习题

1. Run `code/main.py`. Verify the signal-to-noise ratio reported for differential attention is higher than standard softmax attention on the synthetic query. Vary the noise amplitude and show the crossover point where standard attention becomes unusable.
   中文翻译：运行 `code/main.py`。验证差分注意力报告的信噪比在合成查询上高于标准 softmax 注意力。改变噪声幅度并展示标准注意力变得不可用的交叉点。

2. Compute the parameter-count delta from baseline to DIFF V1 and from baseline to DIFF V2 for a 7B-class model (hidden=4096, heads=32, d_head=128, 32 layers). Show which components gained parameters and which stayed the same.
   中文翻译：计算 7B 级模型（hidden=4096，heads=32，d_head=128，32 层）从基线到 DIFF V1 和从基线到 DIFF V2 的参数量差异。展示哪些组件增加了参数，哪些保持不变。

3. Read Section 3 of the DIFF V1 paper (arXiv:2410.05258) and Section 2 of the DIFF V2 Hugging Face blog. In two sentences, explain why the V1 per-head RMSNorm was necessary and why V2 could remove it without causing training divergence.
   中文翻译：阅读 DIFF V1 论文第 3 节和 DIFF V2 Hugging Face 博客第 2 节。用两句话解释为什么 V1 的逐头 RMSNorm 是必要的，以及为什么 V2 可以在不导致训练发散的情况下移除它。

4. Implement an ablation: compute differential attention with `lambda = 0` (pure first softmax) and `lambda = 1` (full subtraction). On the synthetic query, measure how signal-to-noise changes across the sweep. Identify the `lambda` that maximizes signal-to-noise.
   中文翻译：实现消融实验：用 `lambda = 0`（纯第一 softmax）和 `lambda = 1`（完全减法）计算差分注意力。在合成查询上测量信噪比在扫描中如何变化。找到最大化信噪比的 `lambda`。

5. Extend the toy to GQA + DIFF V2. Pick 8 KV heads and 32 Q heads. Show that the KV cache size matches a baseline GQA model with the same (8, 32) configuration.
   中文翻译：将玩具模型扩展到 GQA + DIFF V2。选择 8 个 KV 头和 32 个 Q 头。展示 KV 缓存大小与相同 (8, 32) 配置的基线 GQA 模型匹配。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Differential attention | "Two softmaxes minus each other" | Split Q, K into two halves, compute two softmax maps, subtract the second (scaled by lambda) from the first, then multiply by V | 差分注意力，两个 softmax 相减消除噪声 |
| Noise floor | "The non-zero tail of softmax" | The O(1/N) weight softmax puts on every unrelated token, which sums to O(1) across long contexts | 噪声基底，softmax 对不相关 token 的非零权重 |
| lambda | "The subtraction scale" | Per-head learnable scalar parameterized as `exp(lq1.lk1) - exp(lq2.lk2) + lambda_init`; can be negative | lambda 参数，可学习的减法缩放标量 |
| DIFF V1 | "The ICLR 2025 version" | Original Differential Transformer; halves head dim to preserve parameter count, needs custom kernel, slower decode | DIFF V1，原始差分 Transformer，需要自定义核 |
| DIFF V2 | "The January 2026 fix" | Doubles Q heads keeping KV heads; matches baseline decode speed and works with FlashAttention | DIFF V2，双倍 Q 头保持 KV 头，兼容 FlashAttention |
| Per-head RMSNorm | "The V1 stabilizer" | Extra norm V1 applied after the difference; V2 removed it to prevent late-training instability | 逐头 RMSNorm，V1 的稳定器，V2 移除 |
| Signal-to-noise ratio | "How much attention is wasted" | Ratio of weight on the true signal position to average weight on unrelated positions | 信噪比，信号位置权重与不相关位置平均权重之比 |
| Lost in the middle | "Long-context failure mode" | Empirical phenomenon where retrieval accuracy dips for documents in the middle of a long context — DIFF attention reduces this | 中间丢失现象，长上下文中间文档检索准确率下降 |
| Arithmetic intensity | "FLOPs per byte loaded" | Ratio V2 increased at decode by doubling queries per KV load; important for memory-bound decode | 算术强度，每次字节加载的 FLOPs 比 |

## Further Reading | 延伸阅读

- [Ye et al. — Differential Transformer (arXiv:2410.05258, ICLR 2025)](https://arxiv.org/abs/2410.05258) — the original paper with noise-cancellation theory and long-context ablations
- [Microsoft unilm — Differential Transformer V2 (Hugging Face blog, January 2026)](https://huggingface.co/blog/microsoft/diff-attn-v2) — the production-stack rewrite, matching baseline decode, FlashAttention-compatible
- [Understanding Differential Transformer Unchains Pretrained Self-Attentions (arXiv:2505.16333)](https://arxiv.org/abs/2505.16333) — theoretical analysis of why the subtraction recovers pretrained attention structure
- [Shared DIFF Transformer (arXiv:2501.17900)](https://arxiv.org/html/2501.17900) — parameter-sharing variant
- [Vaswani et al. — Attention Is All You Need (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762) — the baseline Transformer DIFF subtracts from
- [Liu et al. — Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) — the long-context benchmark DIFF attention targets
