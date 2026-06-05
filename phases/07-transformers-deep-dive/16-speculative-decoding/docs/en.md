# Speculative Decoding — Draft, Verify, Repeat | 推测解码 — 草案、验证、重复

> Autoregressive decoding is serial. Each token waits for the previous one. Speculative decoding breaks the chain: a cheap model drafts N tokens, the expensive model verifies all N in one forward pass. When the draft is right you paid one big forward for N generations.

> **【中文解读】** 用小模型快速生成候选 token，大模型批量验证。可以加速推理 2-3 倍而不降低质量。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

A 70B LLM sampling one token takes ~30 ms on an H100. A 3B draft model takes ~3 ms. If we let the 3B draft 5 tokens ahead, then run the 70B *once* to verify all 5, the total is `5×3 + 30 = 45 ms` for up to 5 accepted tokens — versus `5×30 = 150 ms` for straight-line generation. That is the full speculative-decoding pitch: trade a small amount of extra GPU memory (draft model) for 2–4× lower decode latency.

> 一个 70B LLM 采样一个 token 在 H100 上需要约 30 ms。一个 3B 草案模型需要约 3 ms。如果我们让 3B 提前生成 5 个 token，然后运行 70B *一次*验证所有 5 个，总时间为 `5×3 + 30 = 45 ms` 最多获得 5 个接受的 token——而直行生成需要 `5×30 = 150 ms`。这就是推测解码的全部卖点：用少量额外 GPU 内存（草案模型）换取 2-4 倍更低的解码延迟。

The trick has to preserve the distribution. Speculative sampling, introduced by Leviathan et al. (2023) and by Chen et al. concurrently, guarantees that the output sequence is **identically distributed** to what the big model would have produced on its own. No quality tradeoff. Just faster.

> 这个技巧必须保持分布不变。推测采样由 Leviathan 等人（2023）和 Chen 等人同时引入，保证输出序列与大模型自行生成的分布**完全相同**。没有质量损失。只是更快。

Four families of draft-verifier pairs dominate 2026 inference:

> 四类草案-验证器对在 2026 年推理中占主导地位：

1. **Vanilla speculative (Leviathan 2023).** Separate draft model (e.g., Llama 3 1B) + verifier (e.g., Llama 3 70B).
   中文翻译：**朴素推测（Leviathan 2023）。** 独立的草案模型（如 Llama 3 1B）+ 验证器（如 Llama 3 70B）。
2. **Medusa (Cai 2024).** Multiple decoding heads on the verifier predict positions `t+1..t+k` in parallel. No separate draft model.
   中文翻译：**Medusa（Cai 2024）。** 验证器上的多个解码头并行预测位置 `t+1..t+k`。无需独立草案模型。
3. **EAGLE family (Li 2024, 2025).** Lightweight draft that reuses the verifier's hidden states; closer acceptance rate than vanilla; 3–4× typical.
   中文翻译：**EAGLE 系列（Li 2024, 2025）。** 复用验证器隐藏状态的轻量草案；接受率比朴素方案更高；典型加速 3-4 倍。
4. **Lookahead decoding (Fu 2024).** Jacobi iteration; no draft model required at all. Self-speculation. Niche but dependency-free.
   中文翻译：**前瞻解码（Fu 2024）。** Jacobi 迭代；完全不需要草案模型。自推测。小众但无依赖。

Every production inference stack in 2026 ships speculative decoding by default. vLLM, TensorRT-LLM, SGLang, and llama.cpp all support at least vanilla + EAGLE-2.

> 2026 年的每个生产推理栈都默认搭载推测解码。vLLM、TensorRT-LLM、SGLang 和 llama.cpp 都至少支持朴素 + EAGLE-2。

> **【中文解读】** 推测解码的核心洞察：自回归生成是串行的瓶颈。用小模型（3B）快速生成 N 个候选 token，大模型（70B）一次前向传播验证所有 N 个。总时间从 N×30ms 降到 5×3+30=45ms，加速 2-4 倍。关键：推测采样保证输出分布与大模型完全一致，无质量损失。

> **【拓展：EAGLE 与 Medusa 的自推测策略】** EAGLE（2024）复用大模型的隐藏状态来生成草案，接受率比独立小模型更高，典型加速 3-4 倍。Medusa 在大模型上添加多个解码头，并行预测多个未来位置，无需额外模型。这两种"自推测"策略避免了维护独立草案模型的开销，成为 2026 年的主流选择。

## The Concept | 核心概念

### The core algorithm

Given a verifier `M_q` and a cheaper draft `M_p`:

> 给定验证器 `M_q` 和更便宜的草案模型 `M_p`：

1. Let `x_1..x_k` be the prefix already decoded.
   中文翻译：设 `x_1..x_k` 为已解码的前缀。
2. **Draft**: use `M_p` to autoregressively propose `d_{k+1}, d_{k+2}, ..., d_{k+N}` with draft probabilities `p_1..p_N`.
   中文翻译：**草案**：用 `M_p` 自回归地提出 `d_{k+1}, d_{k+2}, ..., d_{k+N}`，附带草案概率 `p_1..p_N`。
3. **Verify in parallel**: run `M_q` once on `x_1..x_k, d_{k+1}, ..., d_{k+N}`, getting verifier probabilities `q_1..q_{N+1}` for positions `k+1..k+N+1`.
   中文翻译：**并行验证**：对 `x_1..x_k, d_{k+1}, ..., d_{k+N}` 运行一次 `M_q`，获得位置 `k+1..k+N+1` 的验证器概率 `q_1..q_{N+1}`。
4. **Accept/reject each draft token left to right**: for each `i`, accept with probability `min(1, q_i(d_i) / p_i(d_i))`.
   中文翻译：**从左到右接受/拒绝每个草案 token**：对每个 `i`，以概率 `min(1, q_i(d_i) / p_i(d_i))` 接受。
5. On first rejection at position `j`: sample `t_j` from the "residual" distribution `(q_j - p_j)_+` normalized. All drafts after `j` are discarded.
   中文翻译：在位置 `j` 首次被拒绝时：从"残差"分布 `(q_j - p_j)_+` 归一化后采样 `t_j`。`j` 之后的所有草案被丢弃。
6. On accepting all `N`: sample one extra token `t_{N+1}` from `q_{N+1}` (the free bonus token).
   中文翻译：当所有 `N` 个都被接受时：从 `q_{N+1}` 采样一个额外的 token `t_{N+1}`（免费奖励 token）。

The residual distribution trick is the mathematical insight that keeps the output distributed exactly as if `M_q` had sampled from scratch.

> 残差分布技巧是保持输出分布与 `M_q` 从头采样完全相同的数学洞见。

### What determines speedup

Let `α` = expected acceptance rate per draft token. Let `c` = draft-to-verifier cost ratio. Per step:

> 设 `α` = 每个草案 token 的预期接受率。设 `c` = 草案与验证器的成本比。每步：

- Naive generation makes 1 big-model call per token.
  中文翻译：朴素生成每个 token 调用一次大模型。
- Speculative makes 1 big-model call per `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)` tokens when `α` is high.
  中文翻译：推测解码在 `α` 较高时，每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)` 个 token 调用一次大模型。

Typical rule of thumb at `α = 0.75` and `N = 5`: 3× fewer big-model calls. Draft cost is 5× cheap. Total wall-clock drops ~2.5×.

> `α = 0.75` 和 `N = 5` 时的典型经验法则：大模型调用减少 3 倍。草案成本是 5 倍便宜。实际总时间下降约 2.5 倍。

> **【中文解读】** 加速效果取决于接受率 alpha。当 alpha=0.75、草案长度 N=5 时，大约 3 倍减少大模型调用。残差分布（residual distribution）是保持分布一致性的数学关键——拒绝时从 (q-p)+ 归一化分布中采样，确保最终输出与大模型直接采样的分布完全一致。

**α depends on:**

> **α 取决于：**

- How well the draft approximates the verifier. Same family / same training data boosts α significantly.
  中文翻译：草案对验证器的近似程度。同系列/同训练数据显著提升 α。
- Decoding strategy. Greedy draft against greedy verifier: high α. Temperature sampling: harder to match; acceptance drops.
  中文翻译：解码策略。贪心草案对贪心验证器：高 α。温度采样：更难匹配；接受率下降。
- Task type. Code and structured output accept more (predictable); free-form creative writing accepts less.
  中文翻译：任务类型。代码和结构化输出接受更多（可预测）；自由形式创意写作接受更少。

### Medusa — drafts without a draft model

Medusa replaces the draft model with extra output heads on the verifier. At position `t`:

> Medusa 用验证器上的额外输出头替换草案模型。在位置 `t`：

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Each head outputs its own logits. At inference you sample from each head to get a candidate sequence, then verify with one forward pass using a tree-attention scheme that considers all candidate continuations at once.

> 每个头输出自己的 logits。推理时从每个头采样得到候选序列，然后用树注意力方案一次前向传播验证，同时考虑所有候选续写。

Pros: no second model. Cons: adds trainable parameters; needs a supervised fine-tuning stage (~1B tokens); acceptance rate is a bit lower than vanilla speculative with a good draft.

> 优点：无需第二个模型。缺点：增加可训练参数；需要监督微调阶段（约 1B token）；接受率比好的草案模型的朴素推测略低。

> **【拓展：推测解码在 vLLM 中的实现】** vLLM 是 2026 年最流行的 LLM 推理框架，原生支持推测解码。它使用 continuous批处理（continuous batching）+ PagedAttention + 推测解码的组合优化。在生产部署中，推测解码通常带来 2-3 倍的延迟降低，对于聊天场景（用户感知延迟敏感）尤为关键。结合量化（AWQ/GPTQ），可以在单张 GPU 上实现高性能推理。

### EAGLE — better draft by reusing hidden states

EAGLE-1/2/3 (Li et al., 2024–2025) makes the draft model a tiny transformer (typically 1 layer) that ingests the verifier's last-layer hidden states. Because the draft sees the verifier's feature representation, its predictions correlate strongly with the verifier's output distribution. Acceptance rates climb from ~0.6 (vanilla) to 0.85+.

> EAGLE-1/2/3（Li 等人，2024-2025）将草案模型做成一个微型 Transformer（通常 1 层），吸收验证器最后一层的隐藏状态。因为草案看到了验证器的特征表示，其预测与验证器的输出分布高度相关。接受率从约 0.6（朴素）提升到 0.85+。

EAGLE-3 (2025) added tree search over candidate continuations. vLLM and SGLang ship EAGLE-2/3 as the default spec pathway for Llama 3/4 and Qwen 3.

> EAGLE-3（2025）添加了对候选续写的树搜索。vLLM 和 SGLang 将 EAGLE-2/3 作为 Llama 3/4 和 Qwen 3 的默认推测路径。

### The KV cache dance

Verification feeds `N` draft tokens into the verifier in one forward pass. This extends the verifier's KV cache by `N` entries. If some drafts are rejected, you must roll the cache back to the accepted prefix length.

> 验证在一次前向传播中将 `N` 个草案 token 输入验证器。这会将验证器的 KV 缓存扩展 `N` 个条目。如果一些草案被拒绝，你必须将缓存回滚到已接受的前缀长度。

Production implementations (vLLM's `--speculative-model`, TensorRT-LLM's LookaheadDecoder) handle this with scratch KV buffers. Write first, commit on acceptance. It's not conceptually hard, but it is fiddly.

> 生产实现（vLLM 的 `--speculative-model`、TensorRT-LLM 的 LookaheadDecoder）使用临时 KV 缓冲区处理这个问题。先写入，接受时提交。概念上不难，但实现上比较繁琐。

## Build It | 动手实现

See `code/main.py`. We implement the core speculative-sampling algorithm (rejection step + residual distribution) with:

> 参见 `code/main.py`。我们用以下组件实现核心推测采样算法（拒绝步骤 + 残差分布）：

- A "big model" that is a deterministic-softmax over a hand-coded distribution (so we can verify acceptance math analytically).
  中文翻译：一个"大模型"，是手动编码分布上的确定性 softmax（以便分析性验证接受数学）。
- A "draft model" that is a perturbation of the big model.
  中文翻译：一个"草案模型"，是大模型的扰动版本。
- An acceptance / rejection loop that produces the same marginal distribution as direct sampling.
  中文翻译：一个接受/拒绝循环，产生与直接采样相同的边际分布。

### Step 1: the rejection step

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u` is a uniform random number. `q_prob` is the verifier's probability for the drafted token. `p_prob` is the draft model's probability. The Leviathan theorem is that this Bernoulli decision, followed by sampling from the residual on rejection, preserves the verifier's distribution exactly.

> `u` 是均匀随机数。`q_prob` 是验证器对草案 token 的概率。`p_prob` 是草案模型的概率。Leviathan 定理表明，这个伯努利决策加上拒绝时从残差采样，可以精确保持验证器的分布。

### Step 2: residual distribution

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Subtract `p` from `q` element-wise, clamp negative values to zero, renormalize. Sample from this on any rejection.

> 逐元素从 `q` 减去 `p`，将负值截断为零，重新归一化。在任何拒绝时从中采样。

### Step 3: one speculative step

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Five accepted → one bonus → six tokens produced in one verifier pass.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个 token。

### Step 4: measure acceptance rate

Run 10,000 speculative steps at varying draft-quality levels. Plot acceptance rate vs. KL divergence between draft and verifier distributions. You should see a clean monotone relationship.

> 在不同草案质量水平上运行 10,000 次推测步骤。绘制接受率 vs 草案与验证器分布之间的 KL 散度。你应该看到一个清晰的单调关系。

### Step 5: verify distribution equivalence

Empirically: the histogram of tokens produced by the speculative loop should match the histogram produced by sampling directly from the verifier. This is the Leviathan theorem in practice. A chi-square test confirms within sampling error.

> 经验上：推测循环产生的 token 直方图应与直接从验证器采样的直方图匹配。这就是实践中的 Leviathan 定理。卡方检验在采样误差范围内确认。

## Use It | 用框架实现

Production:

> 生产部署：

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM has the fastest Medusa path as of mid-2026. `faster-whisper` wraps speculative decoding for Whisper-large with a small draft.

> TensorRT-LLM 在 2026 年中期拥有最快的 Medusa 路径。`faster-whisper` 为 Whisper-large 封装了推测解码，使用小草案模型。

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Single-sequence generation of 1–5 tokens. Overhead dominates.
  中文翻译：1-5 token 的单序列生成。开销占主导。
- Wildly creative / high-temperature sampling (α drops).
  中文翻译：高度创意/高温度采样（α 下降）。
- Memory-constrained deployments (draft model adds VRAM).
  中文翻译：内存受限的部署（草案模型增加显存）。

## Ship It | 产出物

See `outputs/skill-spec-decode-picker.md`. The skill picks a speculative decoding strategy (vanilla / Medusa / EAGLE / lookahead) and tuning parameters (N, draft temperature) for a new inference workload.

> 参见 `outputs/skill-spec-decode-picker.md`。该 skill 为新的推理工作负载选择推测解码策略（朴素/Medusa/EAGLE/前瞻）和调优参数（N、草案温度）。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Confirm the speculative token distribution matches the verifier's direct-sample distribution on 50,000 tokens within chi-square p > 0.05.
   中文翻译：运行 `code/main.py`。确认在 50,000 个 token 上，推测 token 分布与验证器的直接采样分布在卡方检验 p > 0.05 内匹配。
2. **Medium.** Plot speedup (tokens per big-model forward) as a function of `N` for `α = 0.5, 0.7, 0.85`. Identify the optimal `N` for each α. (Hint: expected tokens per verify call = `(1 - α^{N+1}) / (1 - α)`.)
   中文翻译：绘制 `α = 0.5, 0.7, 0.85` 时加速比（每次大模型前向的 token 数）与 `N` 的关系。确定每个 α 的最优 `N`。（提示：每次验证调用的预期 token 数 = `(1 - α^{N+1}) / (1 - α)`。）
3. **Hard.** Implement a tiny Medusa: take the capstone GPT from Lesson 14, add 3 extra LM heads that predict positions t+2, t+3, t+4. Train on tinyshakespeare with a joint multi-head loss. Compare acceptance rates vs a vanilla draft made by truncating the same model.
   中文翻译：实现一个小型 Medusa：取第 14 课的 GPT 毕业项目，添加 3 个额外的 LM 头预测位置 t+2、t+3、t+4。用联合多头损失在 tinyshakespeare 上训练。比较与截断同一模型得到的朴素草案的接受率。
4. **Hard.** Implement rollback: start with a 10-token prefix KV cache, feed 5 draft tokens, simulate a rejection at position 3. Verify your cache reads correctly match "prefix + first 2 accepted drafts" at the next iteration.
   中文翻译：实现回滚：从 10 token 的前缀 KV 缓存开始，输入 5 个草案 token，模拟位置 3 的拒绝。验证你的缓存读取在下次迭代时正确匹配"前缀 + 前 2 个已接受草案"。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Further Reading | 延伸阅读

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — the core algorithm and the equivalence theorem.
  中文翻译：推测解码的核心算法和等价定理论文。
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) — concurrent introduction; clean Bernoulli-rejection proof.
  中文翻译：同时期发表的推测采样论文；清晰的伯努利拒绝证明。
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) — Medusa paper; tree-attention verification.
  中文翻译：Medusa 论文；树注意力验证。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) — EAGLE-1; hidden-state-conditioned draft.
  中文翻译：EAGLE-1 论文；隐藏状态条件草案。
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) — EAGLE-2; dynamic tree depth.
  中文翻译：EAGLE-2 论文；动态树深度。
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840) — EAGLE-3.
  中文翻译：EAGLE-3 论文。
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057) — lookahead, no-draft approach.
  中文翻译：前瞻解码论文，无草案方案。
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) — canonical production reference with all four strategies wired up.
  中文翻译：vLLM 推测解码文档，四种策略的生产参考。
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) — the reference code for EAGLE-1/2/3.
  中文翻译：EAGLE-1/2/3 参考实现代码。
