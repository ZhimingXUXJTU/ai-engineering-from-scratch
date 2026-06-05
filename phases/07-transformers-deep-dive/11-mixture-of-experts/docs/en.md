# Mixture of Experts (MoE) | 混合专家模型 (MoE)

> A dense 70B transformer activates every parameter for every token. A 671B MoE activates only 37B per token and beats it on every benchmark. Sparsity is the most important scaling idea of the decade.

> **【中文解读】** MoE 只激活部分专家网络处理每个 token，大幅增加参数量而不增加计算量。DeepSeek、Mixtral 都用 MoE 架构。

**Type:**  | **类型:** 动手
**Language:** Python | **语言:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

A dense transformer's FLOPs at inference equal its parameter count (times 2 for forward pass). Scale up a dense model and every token pays the full bill. By 2024 the frontier was hitting a compute wall: to be meaningfully smarter, you needed exponentially more FLOPs per token.

Mixture of Experts breaks this link. Replace each FFN with `E` independent experts + a router that picks `k` experts per token. Total parameters = `E × FFN_size`. Active parameters per token = `k × FFN_size`. Typical 2026 configuration: `E=256`, `k=8`. Storage scales with `E`, compute scales with `k`.

The 2026 frontier is almost entirely MoE: DeepSeek-V3 (671B total / 37B active), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss. On Artificial Analysis's independent leaderboard, the top 10 open-source models are all MoE.

> **【中文解读】** MoE 打破了"参数量 = 计算量"的等式。每个 FFN 层替换为 E 个独立专家 + 路由器，每 token 只激活 k 个专家。总参数量随 E 增长，但每个 token 的计算量只随 k 增长。典型配置 E=256, k=8，存储随 E 缩放，计算随 k 缩放。这是 2020 年代最重要的扩展思路。

> **【拓展：DeepSeek-V3 的 MoE 创新】** DeepSeek-V3 拥有 671B 总参数但每 token 只激活 37B——通过 256 个路由专家 + 1 个共享专家实现。它还引入了辅助损失无关的负载均衡策略，避免了传统 MoE 的路由崩塌问题。在 Artificial Analysis 排行榜上，DeepSeek-V3 以不到 GPT-4 十分之一的推理成本达到了可比的性能。

## The Concept | 核心概念

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### The FFN swap

Dense transformer block:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

MoE block:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Every expert is an independent FFN (typically SwiGLU). The router is a single linear layer. Each token picks its own `k` experts and gets a gated mixture of their outputs.

### The load-balancing problem

If the router puts 90% of tokens through expert 3, the other experts starve. Three fixes have been tried:

1. **Auxiliary load-balancing loss** (Switch Transformer, Mixtral). Add a penalty proportional to the variance in expert usage. Works, but adds a hyperparameter and a second gradient signal.
2. **Expert capacity + token dropping** (early Switch). Each expert processes at most `C × N/E` tokens; overflow tokens skip the layer. Hurts quality.
3. **Auxiliary-loss-free balancing** (DeepSeek-V3). Add a learned per-expert bias that shifts the router's top-k selection. Bias is updated outside the training loss. No penalty on the main objective. 2024's big unlock.

DeepSeek-V3's approach: after each training step, for every expert, check if its usage is above or below the target. Nudge the bias by `±γ`. Selection uses `scores + bias`. Expert probabilities used for gating are the raw `scores` unchanged. Decouples routing from expression.

### Shared experts

DeepSeek-V2/V3 also split experts into *shared* and *routed*. Every token passes through all shared experts. Routed experts are picked via top-k. Shared experts capture common knowledge; routed experts specialize. V3 runs 1 shared expert plus top-8 of 256 routed.

### Fine-grained experts

Classic MoE (GShard, Switch): each expert is as wide as a full FFN. `E` is small (8–64), `k` is small (1–2).

Modern fine-grained MoE (DeepSeek-V3, Qwen-MoE): each expert is narrower (1/8 FFN size). `E` is large (256+), `k` is larger (8+). Same total parameters, but combinations scale much faster. `C(256, 8) = 400 trillion` possible "experts" per token. Quality goes up, latency stays flat.

> **【拓展：MoE 的路由崩塌问题】** MoE 训练中的核心挑战是路由崩塌（router collapse）——路由器可能将大部分 token 分配给少数几个专家，导致其他专家得不到训练。解决方案包括：辅助损失（auxiliary loss）鼓励均匀分配、噪声注入（在路由决策前加随机扰动）、DeepSeek-V3 的辅助损失无关负载均衡策略。

### The cost profile

Per token, per layer:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 beats Llama 3 70B (dense) on almost every benchmark while doing **fewer active FLOPs per token**. More parameters = more knowledge. More active FLOPs = more compute per token. MoE decouples them.

### The catch: memory

All experts live on GPU regardless of which ones fire. A 671B model needs ~1.3 TB of VRAM for fp16 weights. Frontier MoE deployment requires expert parallelism — shard experts across GPUs, route tokens across the network. Latency is dominated by the all-to-all communication, not the matmul.

> **【中文解读】** MoE 的核心权衡：用内存换计算。DeepSeek-V3 以 37B 活跃参数达到超越 70B 稠密模型的性能，但需要 1.3TB 显存存储所有专家。这推动了专家并行（expert parallelism）技术的发展——将专家分散到多个 GPU 上，通过网络路由 token。

> **【拓展：细粒度专家 vs 粗粒度专家】** 传统 MoE（Switch Transformer）使用少量大型专家（E=8-64）。现代细粒度 MoE（DeepSeek-V3）使用大量小型专家（E=256+），每个专家只有 1/8 的 FFN 宽度。组合数 C(256,8) 约为 400 万亿种，远超粗粒度的组合空间。质量提升显著，延迟基本不变。

## Build It | 动手实现

See `code/main.py`. A compact MoE layer in pure stdlib with:

- `n_experts=8` SwiGLU-ish experts (one linear each, for illustration)
- top-k=2 routing
- softmax-normalized gating weights
- auxiliary-loss-free balancing via per-expert bias

### Step 1: the router

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

Bias affects selection, not gate weight. That is the DeepSeek-V3 trick — bias corrects load imbalance without steering the model's predictions.

### Step 2: run 100 tokens through the router

Track which experts fire how often. Without the bias, usage is skewed. With a bias update loop (`-γ` for over-used experts, `+γ` for under-used), usage converges to a uniform distribution over a few iterations.

### Step 3: param count comparison

Print the "dense equivalent" of an MoE config. DeepSeek-V3-shaped: 256 routed + 1 shared, 8 active, d_model=7168. The total parameter count is eye-watering. The active count is a seventh of a dense Llama 3 70B.

## Use It | 用框架实现

HuggingFace loading:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 production inference: vLLM supports MoE routing natively. SGLang has the fastest expert-parallel path. Both automatically handle top-k selection and expert parallelism.

**When to pick MoE:**
- You want frontier quality at lower inference cost per token.
- You have the VRAM / expert-parallel infrastructure.
- Your workload is token-heavy (chat, code) not context-heavy (long docs).

**When NOT to pick MoE:**
- Edge deployment — you pay full storage for any active FLOP.
- Latency-critical single-user serving — expert routing adds overhead.
- Small models (<7B) — MoE's quality advantage only appears above a compute threshold (~6B active params).

## Ship It | 产出物

See `outputs/skill-moe-configurator.md`. The skill picks E, k, and shared-expert layout for a new MoE given parameter budget, training tokens, and deployment target.

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Watch how the auxiliary-loss-free bias update evens out expert usage over 50 iterations.
2. **Medium.** Replace the learned router with a hash-based router (deterministic, no learning). Compare quality and balance. Why is the learned router better?
3. **Hard.** Implement GRPO-style "rollout-matched routing" (DeepSeek-V3.2 trick): log which experts fire during inference, force the same routing during gradient computation. Measure the effect on a toy policy-gradient setup.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |

## Further Reading | 延伸阅读

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) — the idea.
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) — Switch, the classic MoE.
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) — Mixtral 8×7B.
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) — MLA + auxiliary-loss-free MoE + MTP.
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) — the bias-based balancing paper.
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) — the fine-grained + shared-expert split this lesson's router uses.
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) — original shared-expert paper.
