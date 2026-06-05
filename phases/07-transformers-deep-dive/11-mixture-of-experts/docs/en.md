# Mixture of Experts (MoE) | 混合专家模型 (MoE)

> A dense 70B transformer activates every parameter for every token. A 671B MoE activates only 37B per token and beats it on every benchmark. Sparsity is the most important scaling idea of the decade.

> **【中文解读】** MoE 只激活部分专家网络处理每个 token，大幅增加参数量而不增加计算量。DeepSeek、Mixtral 都用 MoE 架构。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

A dense transformer's FLOPs at inference equal its parameter count (times 2 for forward pass). Scale up a dense model and every token pays the full bill. By 2024 the frontier was hitting a compute wall: to be meaningfully smarter, you needed exponentially more FLOPs per token.

> 稠密 Transformer 推理时的 FLOPs 等于其参数量（前向传播乘以 2）。扩大稠密模型意味着每个 token 都要支付全部代价。到 2024 年，前沿模型遇到了计算墙：要变得更聪明，需要指数级增长的每 token FLOPs。

Mixture of Experts breaks this link. Replace each FFN with `E` independent experts + a router that picks `k` experts per token. Total parameters = `E × FFN_size`. Active parameters per token = `k × FFN_size`. Typical 2026 configuration: `E=256`, `k=8`. Storage scales with `E`, compute scales with `k`.

> 混合专家模型打破了这个联系。将每个 FFN 替换为 `E` 个独立专家 + 一个路由器，每个 token 选择 `k` 个专家。总参数量 = `E × FFN_size`。每个 token 的活跃参数量 = `k × FFN_size`。典型的 2026 年配置：`E=256`、`k=8`。存储随 `E` 扩展，计算随 `k` 扩展。

The 2026 frontier is almost entirely MoE: DeepSeek-V3 (671B total / 37B active), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss. On Artificial Analysis's independent leaderboard, the top 10 open-source models are all MoE.

> 2026 年的前沿几乎完全是 MoE：DeepSeek-V3（671B 总参数 / 37B 活跃）、Mixtral 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss。在 Artificial Analysis 的独立排行榜上，排名前 10 的开源模型都是 MoE。

> **【中文解读】** MoE 打破了"参数量 = 计算量"的等式。每个 FFN 层替换为 E 个独立专家 + 路由器，每 token 只激活 k 个专家。总参数量随 E 增长，但每个 token 的计算量只随 k 增长。典型配置 E=256, k=8，存储随 E 缩放，计算随 k 缩放。这是 2020 年代最重要的扩展思路。

> **【拓展：DeepSeek-V3 的 MoE 创新】** DeepSeek-V3 拥有 671B 总参数但每 token 只激活 37B——通过 256 个路由专家 + 1 个共享专家实现。它还引入了辅助损失无关的负载均衡策略，避免了传统 MoE 的路由崩塌问题。在 Artificial Analysis 排行榜上，DeepSeek-V3 以不到 GPT-4 十分之一的推理成本达到了可比的性能。

## The Concept | 核心概念

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### The FFN swap

Dense transformer block:

> 稠密 Transformer 块：

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

> 每个专家是一个独立的 FFN（通常是 SwiGLU）。路由器是一个单线性层。每个 token 选择自己的 `k` 个专家，获得它们输出的门控混合。

### The load-balancing problem

If the router puts 90% of tokens through expert 3, the other experts starve. Three fixes have been tried:

> 如果路由器将 90% 的 token 分配给专家 3，其他专家就会"挨饿"。已尝试三种修复方案：

1. **Auxiliary load-balancing loss** (Switch Transformer, Mixtral). Add a penalty proportional to the variance in expert usage. Works, but adds a hyperparameter and a second gradient signal.
   中文翻译：**辅助负载均衡损失**（Switch Transformer、Mixtral）。添加与专家使用方差成比例的惩罚。有效，但增加了超参数和第二个梯度信号。
2. **Expert capacity + token dropping** (early Switch). Each expert processes at most `C × N/E` tokens; overflow tokens skip the layer. Hurts quality.
   中文翻译：**专家容量 + token 丢弃**（早期 Switch）。每个专家最多处理 `C × N/E` 个 token；溢出的 token 跳过该层。损害质量。
3. **Auxiliary-loss-free balancing** (DeepSeek-V3). Add a learned per-expert bias that shifts the router's top-k selection. Bias is updated outside the training loss. No penalty on the main objective. 2024's big unlock.
   中文翻译：**辅助损失无关均衡**（DeepSeek-V3）。添加一个学习到的逐专家偏置，调整路由器的 top-k 选择。偏置在训练损失之外更新。不对主目标施加惩罚。2024 年的重大突破。

DeepSeek-V3's approach: after each training step, for every expert, check if its usage is above or below the target. Nudge the bias by `±γ`. Selection uses `scores + bias`. Expert probabilities used for gating are the raw `scores` unchanged. Decouples routing from expression.

> DeepSeek-V3 的方法：每个训练步骤后，对每个专家检查其使用量是否高于或低于目标。将偏置调整 `±γ`。选择使用 `scores + bias`。用于门控的专家概率是未更改的原始 `scores`。将路由与表达解耦。

### Shared experts

DeepSeek-V2/V3 also split experts into *shared* and *routed*. Every token passes through all shared experts. Routed experts are picked via top-k. Shared experts capture common knowledge; routed experts specialize. V3 runs 1 shared expert plus top-8 of 256 routed.

> DeepSeek-V2/V3 还将专家分为*共享*和*路由*两类。每个 token 都通过所有共享专家。路由专家通过 top-k 选择。共享专家捕获通用知识；路由专家负责专业化。V3 运行 1 个共享专家加上从 256 个路由专家中选择 top-8。

### Fine-grained experts

Classic MoE (GShard, Switch): each expert is as wide as a full FFN. `E` is small (8–64), `k` is small (1–2).

> 经典 MoE（GShard、Switch）：每个专家与完整 FFN 一样宽。`E` 较小（8-64），`k` 较小（1-2）。

Modern fine-grained MoE (DeepSeek-V3, Qwen-MoE): each expert is narrower (1/8 FFN size). `E` is large (256+), `k` is larger (8+). Same total parameters, but combinations scale much faster. `C(256, 8) = 400 trillion` possible "experts" per token. Quality goes up, latency stays flat.

> 现代细粒度 MoE（DeepSeek-V3、Qwen-MoE）：每个专家更窄（1/8 FFN 大小）。`E` 较大（256+），`k` 也更大（8+）。总参数量相同，但组合增长更快。`C(256, 8) = 400 万亿`种可能的"专家"组合。质量提升，延迟不变。

> **【拓展：MoE 的路由崩塌问题】** MoE 训练中的核心挑战是路由崩塌（router collapse）——路由器可能将大部分 token 分配给少数几个专家，导致其他专家得不到训练。解决方案包括：辅助损失（auxiliary loss）鼓励均匀分配、噪声注入（在路由决策前加随机扰动）、DeepSeek-V3 的辅助损失无关负载均衡策略。

### The cost profile

Per token, per layer:

> 每个 token，每层：

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 beats Llama 3 70B (dense) on almost every benchmark while doing **fewer active FLOPs per token**. More parameters = more knowledge. More active FLOPs = more compute per token. MoE decouples them.

> DeepSeek-V3 在几乎所有基准测试上击败了 Llama 3 70B（稠密），同时**每个 token 的活跃 FLOPs 更少**。更多参数 = 更多知识。更多活跃 FLOPs = 每个 token 更多计算。MoE 将两者解耦。

### The catch: memory

All experts live on GPU regardless of which ones fire. A 671B model needs ~1.3 TB of VRAM for fp16 weights. Frontier MoE deployment requires expert parallelism — shard experts across GPUs, route tokens across the network. Latency is dominated by the all-to-all communication, not the matmul.

> 所有专家无论是否激活都驻留在 GPU 上。一个 671B 模型需要约 1.3TB 的 fp16 权重显存。前沿 MoE 部署需要专家并行——将专家分片到多个 GPU 上，通过网络路由 token。延迟主要取决于全互联通信，而非矩阵乘法。

> **【中文解读】** MoE 的核心权衡：用内存换计算。DeepSeek-V3 以 37B 活跃参数达到超越 70B 稠密模型的性能，但需要 1.3TB 显存存储所有专家。这推动了专家并行（expert parallelism）技术的发展——将专家分散到多个 GPU 上，通过网络路由 token。

> **【拓展：细粒度专家 vs 粗粒度专家】** 传统 MoE（Switch Transformer）使用少量大型专家（E=8-64）。现代细粒度 MoE（DeepSeek-V3）使用大量小型专家（E=256+），每个专家只有 1/8 的 FFN 宽度。组合数 C(256,8) 约为 400 万亿种，远超粗粒度的组合空间。质量提升显著，延迟基本不变。

## Build It | 动手实现

See `code/main.py`. A compact MoE layer in pure stdlib with:

> 参见 `code/main.py`。一个用纯标准库实现的紧凑 MoE 层，包含：

- `n_experts=8` SwiGLU-ish experts (one linear each, for illustration)
  中文翻译：`n_experts=8` 个类 SwiGLU 专家（每个一条线性层，用于演示）
- top-k=2 routing
  中文翻译：top-k=2 路由
- softmax-normalized gating weights
  中文翻译：softmax 归一化门控权重
- auxiliary-loss-free balancing via per-expert bias
  中文翻译：通过逐专家偏置实现辅助损失无关均衡

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

> 偏置影响选择，不影响门控权重。这就是 DeepSeek-V3 的技巧——偏置纠正负载不平衡，但不干预模型的预测。

### Step 2: run 100 tokens through the router

Track which experts fire how often. Without the bias, usage is skewed. With a bias update loop (`-γ` for over-used experts, `+γ` for under-used), usage converges to a uniform distribution over a few iterations.

> 跟踪哪些专家被激活了多少次。没有偏置时，使用量不均匀。通过偏置更新循环（过度使用的专家 `-γ`，使用不足的专家 `+γ`），使用量在几次迭代后收敛到均匀分布。

### Step 3: param count comparison

Print the "dense equivalent" of an MoE config. DeepSeek-V3-shaped: 256 routed + 1 shared, 8 active, d_model=7168. The total parameter count is eye-watering. The active count is a seventh of a dense Llama 3 70B.

> 打印 MoE 配置的"稠密等价"。DeepSeek-V3 形状：256 个路由 + 1 个共享，8 个活跃，d_model=7168。总参数量令人惊叹。活跃参数量只有稠密 Llama 3 70B 的七分之一。

## Use It | 用框架实现

HuggingFace loading:

> HuggingFace 加载：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 production inference: vLLM supports MoE routing natively. SGLang has the fastest expert-parallel path. Both automatically handle top-k selection and expert parallelism.

> 2026 年生产推理：vLLM 原生支持 MoE 路由。SGLang 拥有最快的专家并行路径。两者都自动处理 top-k 选择和专家并行。

**When to pick MoE:**
- You want frontier quality at lower inference cost per token.
  中文翻译：你想以更低的每 token 推理成本获得前沿质量。
- You have the VRAM / expert-parallel infrastructure.
  中文翻译：你有足够的显存/专家并行基础设施。
- Your workload is token-heavy (chat, code) not context-heavy (long docs).
  中文翻译：你的工作负载是 token 密集型（聊天、代码）而非上下文密集型（长文档）。

**When NOT to pick MoE:**
- Edge deployment — you pay full storage for any active FLOP.
  中文翻译：边缘部署——你要为任何活跃 FLOP 支付全部存储。
- Latency-critical single-user serving — expert routing adds overhead.
  中文翻译：延迟敏感的单用户服务——专家路由增加开销。
- Small models (<7B) — MoE's quality advantage only appears above a compute threshold (~6B active params).
  中文翻译：小模型（<7B）——MoE 的质量优势只在计算阈值以上（约 6B 活跃参数）才会出现。

## Ship It | 产出物

See `outputs/skill-moe-configurator.md`. The skill picks E, k, and shared-expert layout for a new MoE given parameter budget, training tokens, and deployment target.

> 参见 `outputs/skill-moe-configurator.md`。该 skill 根据参数预算、训练 token 数和部署目标，为新 MoE 选择 E、k 和共享专家布局。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Watch how the auxiliary-loss-free bias update evens out expert usage over 50 iterations.
   中文翻译：运行 `code/main.py`。观察辅助损失无关偏置更新如何在 50 次迭代中均衡专家使用。
2. **Medium.** Replace the learned router with a hash-based router (deterministic, no learning). Compare quality and balance. Why is the learned router better?
   中文翻译：用基于哈希的路由器替换学习式路由器（确定性的，无需学习）。比较质量和均衡性。为什么学习式路由器更好？
3. **Hard.** Implement GRPO-style "rollout-matched routing" (DeepSeek-V3.2 trick): log which experts fire during inference, force the same routing during gradient computation. Measure the effect on a toy policy-gradient setup.
   中文翻译：实现 GRPO 风格的"推演匹配路由"（DeepSeek-V3.2 技巧）：记录推理时哪些专家被激活，在梯度计算时强制相同路由。在玩具策略梯度设置上测量效果。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## Further Reading | 延伸阅读

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) — the idea.
  中文翻译：MoE 的原始论文。
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) — Switch, the classic MoE.
  中文翻译：Switch Transformer，经典的 MoE 论文。
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) — Mixtral 8×7B.
  中文翻译：Mixtral 8×7B 论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) — MLA + auxiliary-loss-free MoE + MTP.
  中文翻译：DeepSeek-V3 技术报告，MLA + 辅助损失无关 MoE + MTP。
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) — the bias-based balancing paper.
  中文翻译：基于偏置的均衡策略论文。
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) — the fine-grained + shared-expert split this lesson's router uses.
  中文翻译：DeepSeekMoE 论文，细粒度 + 共享专家拆分。
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) — original shared-expert paper.
  中文翻译：DeepSpeed-MoE 原始共享专家论文。
