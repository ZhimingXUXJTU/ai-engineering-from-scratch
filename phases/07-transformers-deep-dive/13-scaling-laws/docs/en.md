# Scaling Laws | 缩放定律

> The 2020 Kaplan paper said: bigger model, lower loss. The 2022 Hoffmann paper said: you were under-training. Compute goes into two buckets — parameters and tokens — and the split is not obvious.

> **【中文解读】** Chinchilla 定律揭示了模型大小、数据量、计算量的最优关系。理解缩放定律 = 理解为什么 LLM 需要那么多数据。

**Type:** Study | **类型:** 学习
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

When you have C FLOPs of training compute and want the best model, you face two knobs:

> 当你有 C FLOPs 的训练计算量并想要最好的模型时，你面对两个旋钮：

1. **How many parameters (N)?** Bigger model, higher capacity.
   中文翻译：**多少参数（N）？** 模型越大，容量越高。
2. **How many training tokens (D)?** More data, better use of capacity.
   中文翻译：**多少训练 token（D）？** 数据越多，容量利用越好。

FLOPs scale approximately as `6 × N × D`. You can push N up and D down, or D up and N down. Which is better?

> FLOPs 大约按 `6 × N × D` 扩展。你可以增大 N 减小 D，或增大 D 减小 N。哪个更好？

Before 2022, the answer was "push N hard." GPT-3 (2020) was 175B parameters trained on ~300B tokens. A ratio of about 1.7 tokens per parameter. The Kaplan scaling laws backed this up.

> 2022 年之前，答案是"推大 N"。GPT-3（2020）有 175B 参数，在约 300B token 上训练。比例约为每个参数 1.7 个 token。Kaplan 缩放定律支持这一观点。

Hoffmann et al. (2022), training a small family of models called Chinchilla, found something different: optimal ratio is closer to **20 tokens per parameter**. GPT-3 was 10× undertrained. Chinchilla (70B params, 1.4T tokens) beat GPT-3 (175B, 300B tokens) on every benchmark at 2.5× less inference cost.

> Hoffmann 等人（2022）训练了一小组名为 Chinchilla 的模型，发现了不同的结果：最优比例接近**每个参数 20 个 token**。GPT-3 低估训练了 10 倍。Chinchilla（70B 参数，1.4T token）在每个基准测试上都击败了 GPT-3（175B，300B token），推理成本仅为后者的 2.5 分之一。

2026 is Chinchilla's world — with one important twist. Llama 3 8B was trained on 15 trillion tokens, a ratio of 1,875 tokens per parameter. Ninety-four times past Chinchilla-optimal. Inference cost matters more than training cost for models that will be used at scale, so over-training (past Chinchilla) for a smaller deployable footprint is the 2026 default.

> 2026 年是 Chinchilla 的世界——但有一个重要的转折。Llama 3 8B 用了 15 万亿 token 训练，比例为每个参数 1,875 个 token。是 Chinchilla 最优的 94 倍。对于将被大规模使用的模型，推理成本比训练成本更重要，因此为了更小的部署足迹而过度训练（超过 Chinchilla）是 2026 年的默认策略。

> **【中文解读】** 缩放定律的核心洞察：FLOPs ≈ 6 × N × D（参数量 × token 数）。Kaplan（2020）倾向于增大 N，但 Chinchilla（2022）证明最优比例约为 20 token/参数。2026 年的实践更进一步：Llama 3 8B 用了 1,875 token/参数训练——远超 Chinchilla 最优，因为推理成本比训练成本更重要，过度训练小模型以降低部署成本已成为行业标准。

> **【拓展：过度训练策略的经济逻辑】** Llama 3 8B 用 15T token 训练（远超 Chinchilla 最优的 160B token），推理成本却大幅降低。这是因为推理时每个 token 的计算量与参数量成正比，8B 参数的推理成本仅为 70B 模型的约 1/9。对于部署量大的模型（如 API 服务），推理成本的节约远超额外训练成本。这解释了为什么 Phi-3-mini（3.8B）和 Qwen2-1.5B 等小模型都被过度训练。

## The Concept | 核心概念

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### The Hoffmann law

From the Chinchilla paper, loss follows:

> 来自 Chinchilla 论文，损失遵循：

```
L(N, D) = A / N^α + B / D^β + E
```

- `N` = parameters (non-embedding).
  中文翻译：`N` = 参数量（非嵌入）。
- `D` = training tokens.
  中文翻译：`D` = 训练 token 数。
- `α ≈ 0.34`, `β ≈ 0.28` (roughly symmetric).
  中文翻译：`α ≈ 0.34`、`β ≈ 0.28`（大致对称）。
- `E ≈ 1.69`, the irreducible loss ceiling.
  中文翻译：`E ≈ 1.69`，不可约损失上限。
- `A ≈ 406`, `B ≈ 411`.
  中文翻译：`A ≈ 406`、`B ≈ 411`。

Two terms trade against each other as you scale. Take the derivative w.r.t. `N` at fixed compute (C = 6ND) and solve:

> 两项在扩展时相互制衡。在固定计算量（C = 6ND）下对 `N` 求导并求解：

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Compute-optimal: 20 tokens per parameter.

> 计算最优：每个参数 20 个 token。

### Why over-training anyway

Chinchilla-optimal minimizes training loss per training FLOP. But you pay training cost once; inference cost forever.

> Chinchilla 最优最小化每个训练 FLOP 的训练损失。但训练成本只付一次；推理成本永远持续。

For a chatbot that serves a trillion tokens per month, inference dominates total cost. Llama's approach: train smaller, longer. 8B at 15T tokens is deeply inference-optimized:

> 对于每月服务万亿 token 的聊天机器人，推理主导总成本。Llama 的方法：训练更小、更长。8B 在 15T token 上训练是深度推理优化的：

- Fits on consumer GPUs.
  中文翻译：适配消费级 GPU。
- Latency is a fraction of 70B Chinchilla-optimal.
  中文翻译：延迟仅为 70B Chinchilla 最优的一小部分。
- Quality is close enough for most tasks.
  中文翻译：质量对大多数任务来说足够接近。

DeepMind's 2024 paper ("Over-training is the new optimal") formalized this. For inference-dominated workloads, the right ratio is closer to 100–500 tokens per parameter depending on serving volume.

> DeepMind 2024 年的论文（"过度训练是新的最优"）形式化了这一点。对于推理主导的工作负载，正确的比例接近每个参数 100-500 个 token，取决于服务量。

### Emergence vs smoothness

Claim: certain abilities (arithmetic, multi-step reasoning, chain-of-thought following) "emerge" suddenly at some scale.

> 声称：某些能力（算术、多步推理、思维链遵循）在某个规模"涌现"。

Schaeffer et al. (2023) argued this is a measurement artifact: emergent metrics use discontinuous scoring (exact match, accuracy at threshold) that hide smooth improvement in the underlying logits. Continuous metrics (cross-entropy) show smooth curves.

> Schaeffer 等人（2023）认为这是度量伪影：涌现指标使用不连续的评分（精确匹配、阈值准确率），隐藏了底层 logits 的平滑改善。连续指标（交叉熵）显示平滑曲线。

In 2026 the consensus is: predictions via continuous loss are reliable. Benchmark jumps are often scorer artifacts. Plan budgets against continuous metrics.

> 2026 年的共识是：通过连续损失进行预测是可靠的。基准测试的跳变往往是评分标准的问题。根据连续指标规划预算。

> **【中文解读】** "涌现能力"（emergence）在 2023 年引发了大量讨论——某些能力似乎在特定规模突然出现。但 Schaeffer 等人证明这可能是度量伪影：不连续的评分标准（如精确匹配）隐藏了底层 logits 的平滑改善。2026 年的共识是：用连续损失（如交叉熵）预测是可靠的，基准测试的跳变往往是评分标准的问题。

> **【拓展：数据质量比数据量更重要】** 2026 年缩放定律的新变量是数据质量。Microsoft 的 Phi 系列证明，精心筛选的"高质量" token 可以将有效计算量提升 2 倍以上。Llama 3 使用了数据配比优化和合成数据增强。MoE 架构则进一步解耦了总参数量和活跃计算量。这些因素使得传统的 Chinchilla 曲线需要重新校准。

### The 2026 picture

Scaling laws still work, but:

> 缩放定律仍然有效，但：

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】** 2026 年缩放定律面临数据墙问题——高质量人类文本数据可能在未来几年耗尽。合成数据（模型生成的训练数据）是潜在的解决方案。Microsoft 的 Phi 系列使用 GPT-4 生成的"教科书质量"合成数据进行训练，NVIDIA 的 Nemotron 使用合成数据增强。如果合成数据有效，缩放定律的"有效计算"可以持续增长。

The Muon optimizer (Kimi Moonlight, 2024) showed a ~2× effective-compute gain over AdamW at matched data. Some 2026 training runs use Muon by default. Changes the absolute constant in the scaling law, not its shape.

> Muon 优化器（Kimi Moonlight，2024）在相同数据上显示了比 AdamW 约 2 倍的有效计算增益。一些 2026 年的训练运行默认使用 Muon。它改变了缩放定律的绝对常数，而非其形状。

## Build It | 动手实现

See `code/main.py`. We implement the Chinchilla loss equation and solve for compute-optimal `(N, D)` at each of several compute budgets.

> 参见 `code/main.py`。我们实现 Chinchilla 损失方程，并在多个计算预算下求解计算最优的 `(N, D)`。

### Step 1: Chinchilla loss

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

Plot `L` as a contour over `(N, D)` at fixed `C = 6ND`. Find the minimum.

> 将 `L` 作为 `(N, D)` 的等高线图，固定 `C = 6ND`。找到最小值。

### Step 2: compute-optimal frontier

For compute budgets from `1e17` to `1e25` FLOPs, find `(N, D)` that minimize loss subject to `6ND = C`. Verify the ratio `D/N ≈ 20`.

> 对于从 `1e17` 到 `1e25` FLOPs 的计算预算，找到使损失最小化的 `(N, D)`，约束 `6ND = C`。验证比例 `D/N ≈ 20`。

### Step 3: over-training cost

Compute the extra loss you pay to train a 10× smaller model (1/10 of optimal N, 10× the optimal D). Reports the inference FLOP savings (proportional to N) in exchange.

> 计算训练一个 10 倍小模型（最优 N 的 1/10，最优 D 的 10 倍）所付出的额外损失。报告作为交换的推理 FLOP 节约（与 N 成正比）。

### Step 4: compare to real models

Drop in known `(N, D)` pairs for GPT-3, Chinchilla, Llama 3 8B, DeepSeek-V3 (active params), and compare predicted vs reported loss.

> 输入 GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3（活跃参数）的已知 `(N, D)` 对，比较预测损失与报告损失。

## Use It | 用框架实现

You're unlikely to train a frontier model yourself. But scaling laws tell you:

> 你不太可能自己训练前沿模型。但缩放定律告诉你：

1. **Whether your fine-tune has enough data.** If your task-specific data is below 20 tokens per param of the base model, expect saturation at some loss floor.
   中文翻译：**你的微调是否有足够数据。** 如果你的任务特定数据低于基础模型每参数 20 个 token，预期会在某个损失下限饱和。
2. **Whether to pick a bigger base model.** If you're spending all your budget on inference, prefer a smaller, longer-trained model.
   中文翻译：**是否选择更大的基础模型。** 如果你把所有预算花在推理上，优先选择更小的、训练更久的模型。
3. **Where the returns diminish.** Beyond 1000× Chinchilla-optimal, log-loss changes become noise.
   中文翻译：**收益递减在哪里。** 超过 Chinchilla 最优的 1000 倍后，对数损失的变化变成噪声。

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.** The web has a finite number of high-quality tokens (~5–10 trillion English after filtering). Frontier pretraining is approaching this ceiling. Synthetic data, multilingual, multimodal, and RLHF-scaled fine-tuning are the next levers.
  中文翻译：**数据受限时代。** 网络上的高质量 token 数量有限（过滤后约 5-10 万亿英文）。前沿预训练正在接近这个上限。合成数据、多语言、多模态和 RLHF 缩放的微调是下一个杠杆。
- **Compute-multiplier tricks.** Muon optimizer, MoE, better data curation — each shifts the absolute constants, not the asymptote.
  中文翻译：**计算倍增技巧。** Muon 优化器、MoE、更好的数据策展——各自改变绝对常数，而非渐近线。
- **Scaling laws for RL.** Open question. Early evidence suggests power-law in RL samples but with very different exponents than pretraining.
  中文翻译：**RL 的缩放定律。** 开放问题。早期证据表明 RL 样本有幂律关系，但指数与预训练大不相同。

## Ship It | 产出物

See `outputs/skill-training-budget-estimator.md`. The skill picks `(N, D, hours, GPU)` for a new training run given compute budget, deployment constraints, and target loss.

> 参见 `outputs/skill-training-budget-estimator.md`。该 skill 根据计算预算、部署约束和目标损失，为新训练运行选择 `(N, D, hours, GPU)`。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Print Chinchilla-optimal `(N, D)` for compute budgets `1e20`, `1e22`, `1e24`. Compare to the real model table.
   中文翻译：运行 `code/main.py`。打印计算预算为 `1e20`、`1e22`、`1e24` 时的 Chinchilla 最优 `(N, D)`。与真实模型表对比。
2. **Medium.** Implement the Hoffmann loss-as-function-of-compute curve. Plot loss vs `log10(C)` for the compute-optimal frontier. Identify when the law predicts we'd need `>10^28` FLOPs for the next 0.1 reduction in cross-entropy.
   中文翻译：实现 Hoffmann 损失-计算量曲线。绘制计算最优前沿的损失 vs `log10(C)`。确定定律预测何时需要 `>10^28` FLOPs 才能使交叉熵再降低 0.1。
3. **Hard.** Fit your own scaling law on 5 tiny models (100K to 10M params) trained on the same dataset. Estimate `α` and `E`. How well do your exponents match published ones?
   中文翻译：在相同数据集上训练 5 个小模型（100K 到 10M 参数）并拟合自己的缩放定律。估计 `α` 和 `E`。你的指数与发布值匹配度如何？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## Further Reading | 延伸阅读

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) — the first scaling law paper; undertrained.
  中文翻译：第一篇缩放定律论文；低估训练了。
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) — Chinchilla.
  中文翻译：Chinchilla 论文。
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) — emergence as measurement artifact.
  中文翻译：涌现能力是否是幻觉的论文。
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448) — why Llama's over-training is right for its workload.
  中文翻译：为什么 Llama 的过度训练对其工作负载是正确的。
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) — 2× compute multiplier.
  中文翻译：Muon 优化器，2 倍计算倍增器。
