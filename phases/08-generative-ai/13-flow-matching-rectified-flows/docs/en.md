# Flow Matching & Rectified Flows | 流匹配与整流流

> Diffusion models take 20-50 sampling steps because they walk a curved path from noise to data. Flow matching (Lipman et al., 2023) and rectified flow (Liu et al., 2022) trained straight paths. Straighter paths mean fewer steps mean faster inference. Stable Diffusion 3, Flux.1, and AudioCraft 2 all switched to flow matching in 2024.

> **【中文解读】** 扩散模型需要 20-50 步采样因为走的是弯曲路径。Flow Matching 和 Rectified Flow 训练直线路径——更直的路径意味着更少的步数和更快的推理。SD3、FLUX.1、AudioCraft 2 都在 2024 年切换到了 Flow Matching。

> **【拓展：Flow Matching 是 2024-2026 的趋势】** Flow Matching 正在取代传统扩散调度成为新一代生成模型的标准。它数学上更优雅，实验上更高效。SD3 和 FLUX 的质量提升很大程度上归功于这个改进。

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

DDPM's reverse process is a 1000-step stochastic walk from `N(0, I)` back to the data distribution. DDIM collapsed it to 20-50 deterministic steps. You want fewer steps — ideally one. The blocker is that the ODE solving the reverse process is stiff; the path is curved.

> DDPM 的反向过程是从 `N(0, I)` 回到数据分布的 1000 步随机游走。DDIM 将其压缩到 20-50 步。你想要更少步数——理想情况下一步。障碍是反向过程的 ODE 是刚性的；路径是弯曲的。

If you could train the model such that the path from noise to data was a *straight line*, a single Euler step from `t=1` to `t=0` would work. Flow matching builds this directly: define a straight-line interpolation from `x_1 ∼ N(0, I)` to `x_0 ∼ data`, train a vector field `v_θ(x, t)` to match its time derivative, integrate at inference.

> 如果能训练模型使噪声到数据的路径是*直线*，一步 Euler 从 `t=1` 到 `t=0` 就够了。Flow Matching 直接构建这个：定义 `x_1 ∼ N(0, I)` 到 `x_0 ∼ data` 的直线插值，训练向量场 `v_θ(x, t)` 匹配时间导数。

Rectified flow (Liu 2022) goes further: iteratively straighten the paths with a reflow procedure that produces a progressively closer-to-linear ODE. After two reflow iterations, a 2-step sampler matches 50-step DDPM quality.

> Rectified Flow（2022）更进一步：通过 reflow 过程迭代拉直路径。两次 reflow 迭代后，2 步采样器匹配 50 步 DDPM 质量。

> **【中文解读】** Flow Matching 的核心思想：DDPM 的噪声到数据路径是弯曲的，需要 20-50 步采样。如果能训练直线路径，一步就能从噪声到数据。Flow Matching 定义 x_1（噪声）到 x_0（数据）的直线插值，训练向量场 v_theta(x,t) 匹配时间导数。Rectified Flow 进一步通过 reflow 迭代拉直路径，2 步采样即可匹配 50 步 DDPM 的质量。

> **【拓展：FLUX.1 的 Flow Matching 实现】** Black Forest Labs 的 FLUX.1（由 Stable Diffusion 原作者创建）使用 Flow Matching 替代传统扩散调度，配合 MMDiT（多模态 DiT）架构，在图像质量和生成速度上都显著优于 SDXL。FLUX.1-schnell 版本仅需 4 步采样即可生成高质量图像，验证了 Flow Matching 的实际优势。

## The Concept | 核心概念

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Straight-line flow | 直线流

Define:

> 定义：

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

where `x_0 ~ data` and `x_1 ~ N(0, I)`. The time derivative along this straight line is constant:

> 其中 `x_0 ~ data`，`x_1 ~ N(0, I)`。沿这条直线的时间导数是常数：

```
dx_t / dt = x_1 - x_0
```

Define a neural vector field `v_θ(x_t, t)` and train it to match this derivative:

> 定义神经向量场 `v_θ(x_t, t)`，训练它匹配这个导数：

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

This is the **conditional flow matching** loss (Lipman 2023). Training is simulation-free: you never unroll the ODE. Just sample `(x_0, x_1, t)` and regress.

> 这就是**条件 Flow Matching** 损失（Lipman 2023）。训练是 simulation-free 的：你永远不需要展开 ODE。只需采样 `(x_0, x_1, t)` 并做回归即可。

### Sampling | 采样

At inference, integrate the learned vector field *backwards* in time:

> 推理时，将学到的向量场沿时间*反向*积分：

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Start at `x_1 ~ N(0, I)`, Euler-step down to `t=0`.

> 从 `x_1 ~ N(0, I)` 开始，用 Euler 步进降到 `t=0`。

### Rectified flow (Liu 2022) | 整流流（Liu 2022）

Straight-line flow works but the learned paths are *not actually straight* — they curve because many `x_0`s can map to the same `x_1`. Rectified flow's reflow step:

> 直线流虽然有效，但学到的路径其实*并不真正是直的*——因为许多 `x_0` 可以映射到同一个 `x_1`，路径会弯曲。Rectified Flow 的 reflow 步骤：

1. Train flow model v_1 with random pairings.
   用随机配对训练 Flow 模型 v_1。
2. Sample N pairs `(x_1, x_0)` by integrating v_1 from `x_1` to its landing `x_0`.
   通过将 v_1 从 `x_1` 积分到落点 `x_0` 采样 N 对 `(x_1, x_0)`。
3. Train v_2 on those paired examples. Because the pairs are now "ODE-matched", the straight-line interpolant between them is genuinely flatter.
   在这些配对样本上训练 v_2。因为配对现在是 "ODE 匹配" 的，它们之间的直线插值确实更平坦。
4. Repeat.
   重复。

In practice 2 reflow iterations get you to near-linear, enabling 2-4 step inference. SDXL-Turbo, SD3-Turbo, LCM are all distilled-from-flow-matching models.

> 实践中 2 次 reflow 迭代就能使路径接近线性，从而支持 2-4 步推理。SDXL-Turbo、SD3-Turbo、LCM 都是基于 Flow Matching 蒸馏出来的模型。

### Why this won for images in 2024 | 为何 2024 年图像生成全面转向 Flow Matching

Three reasons:

> 三个原因：

1. **Simulation-free training** — no ODE unrolling during training, trivial to implement.
   **无需仿真的训练**——训练时无需展开 ODE，实现非常简单。
2. **Better loss geometry** — straight paths have consistent signal-to-noise, whereas DDPM ε-loss has bad SNR at edges of the schedule.
   **更优的损失几何**——直线路径信噪比一致，而 DDPM 的 ε-loss 在调度边缘 SNR 较差。
3. **Faster inference** — 4-8 steps at SDXL-Turbo quality; 1 step with consistency distillation.
   **更快的推理**——4-8 步即可达到 SDXL-Turbo 质量；配合一致性蒸馏可一步生成。

## Flow matching vs DDPM — the exact connection | Flow Matching vs DDPM — 精确联系

Flow matching with a Gaussian-conditional path is diffusion *with a specific noise schedule*. Pick the `x_t = α(t) x_0 + σ(t) x_1` schedule and flow matching recovers Stratonovich-reformulated diffusion with `v = α'·x_0 - σ'·x_1`. The two are algebraically equivalent for Gaussian paths.

> 使用高斯条件路径的 Flow Matching 实际上是*具有特定噪声调度*的扩散模型。选取 `x_t = α(t) x_0 + σ(t) x_1` 调度后，Flow Matching 还原为以 Stratonovich 形式重写的扩散，其中 `v = α'·x_0 - σ'·x_1`。对于高斯路径，两者在代数上等价。

What flow matching added: the *clarity* of the target (a plain velocity), a cleaner loss, and the license to experiment with non-Gaussian interpolants.

> Flow Matching 的真正贡献是：目标的*清晰度*（一个普通的速度向量）、更干净的损失，以及尝试非高斯插值的自由。

## Build It | 动手实现

`code/main.py` implements 1-D flow matching on a two-mode Gaussian mixture. The vector field `v_θ(x, t)` is a tiny MLP trained with the straight-line target. At inference, integrate 1, 2, 4, and 20 Euler steps and compare sample quality.

> `code/main.py` 在双峰高斯混合分布上实现 1-D Flow Matching。向量场 `v_θ(x, t)` 是一个微型 MLP，使用直线目标训练。推理时分别用 1、2、4、20 个 Euler 步数积分并比较样本质量。

### Step 1: training loss | 步骤 1：训练损失

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 训练损失：采样噪声 `x1` 和时间 `t`，构造插值 `x_t`，目标为 `x1 - x0`，做平方回归。

### Step 2: multi-step inference | 步骤 2：多步推理

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> 多步推理：从高斯噪声出发，按步长反向积分。步数越多结果越精确，但延迟越高。

### Step 3: compare step counts | 步骤 3：比较步数

Expect the 4-step sampler to already match the 20-step quality — a big deal for latency.

> 4 步采样器应已经匹配 20 步质量——这对延迟是重大改进。

## Pitfalls | 常见陷阱

- **Time parameterization.** Flow matching uses `t ∈ [0, 1]` with `t=0` at data, `t=1` at noise. DDPM uses `t ∈ [0, T]` with `t=0` at data, `t=T` at noise. Same direction, different scale. Papers get this wrong constantly.
  时间参数化：Flow Matching 用 `t ∈ [0, 1]`，`t=0` 在数据端，`t=1` 在噪声端；DDPM 用 `t ∈ [0, T]`，方向相同但尺度不同。论文经常搞错。
- **Schedule choice.** Rectified flow's straight line is "the" flow-matching schedule, but you can use cosine or logit-normal t-sampling (SD3 does this) for better scale coverage.
  调度选择：Rectified Flow 的直线是 "标准" 的 Flow Matching 调度，但可以用 cosine 或 logit-normal 的 t 采样（SD3 就是这样做的）来获得更好的尺度覆盖。
- **Reflow cost.** Generating the paired dataset for reflow is a full inference pass per sample. Only do reflow when you really need 1-2 step inference.
  Reflow 成本：生成 reflow 配对数据集需要每个样本一次完整推理。只有真正需要 1-2 步推理时才做 reflow。
- **Classifier-free guidance still applies.** Just swap ε for v in the linear combination: `v_cfg = (1+w) v_cond - w v_uncond`.
  Classifier-Free Guidance 仍然适用：只需把线性组合里的 ε 换成 v：`v_cfg = (1+w) v_cond - w v_uncond`。

## Use It | 用框架实现

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Whenever a paper says "faster than diffusion" in 2025-2026, it is almost always flow matching + distillation.

> 当论文说"比扩散更快"时，几乎总是 Flow Matching + 蒸馏。

## Ship It | 产出物

Save `outputs/skill-fm-tuner.md`. Skill takes a diffusion-style model spec and converts it to a flow-matching training config: schedule choice, time sampling distribution (uniform / logit-normal), optimizer, reflow plan, target step count, eval protocol.

> 保存为 `outputs/skill-fm-tuner.md`。该技能接收一个扩散式模型规格，将其转换为 Flow Matching 训练配置：调度选择、时间采样分布（uniform / logit-normal）、优化器、reflow 计划、目标步数、评估协议。

## Exercises | 练习题

1. **Easy.** Run `code/main.py` and compare 1-step vs 20-step MSE vs the true data distribution.
   **简单。** 运行 `code/main.py`，比较 1 步和 20 步相对真实数据分布的 MSE。
2. **Medium.** Switch from uniform `t` sampling to logit-normal (concentrates sampling at mid-t). Does the model quality improve?
   **中等。** 将均匀 `t` 采样切换为 logit-normal（集中在中间 t 附近采样）。模型质量是否提升？
3. **Hard.** Implement one reflow iteration: generate paired (x_0, x_1) by integrating the first model, train a second model on the pairs, and compare 1-step sample quality.
   **困难。** 实现一次 reflow 迭代：通过对第一个模型积分生成配对 (x_0, x_1)，在配对上训练第二个模型，并比较 1 步采样质量。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Production note: Flux.1-schnell is flow matching at its fastest | 生产笔记：Flux.1-schnell 是 Flow Matching 的最快形态

Flow matching's production win is Flux.1-schnell — a flow-matched DiT distilled to 1-4 inference steps while keeping Flux-dev-grade quality. Niels' "Run Flux on an 8GB machine" notebook is the reference deployment recipe: T5 + CLIP encode, quantized MMDiT denoise (in 4 steps for schnell vs 50 for dev), VAE decode. The cost accounting:

> Flow Matching 在生产中的胜利是 Flux.1-schnell——一个蒸馏到 1-4 步推理、保持 Flux-dev 级质量的 Flow-Matched DiT。Niels 的 "在 8GB 机器上运行 Flux" notebook 是参考部署方案：T5 + CLIP 编码、量化 MMDiT 去噪（schnell 4 步 vs dev 50 步）、VAE 解码。成本核算：

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

The production rule: **flow-matched base + distillation = the 2026 default for fast text-to-image.** Every major vendor ships this combo: SD3-Turbo (SD3 + flow + distillation), Flux-schnell (Flux-dev + rectified-flow straightening), CogView-4-Flash. Pure diffusion bases exist only for legacy checkpoints.

> 生产规则：**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。** 每个主要厂商都推出这种组合：SD3-Turbo（SD3 + flow + 蒸馏）、Flux-schnell（Flux-dev + Rectified Flow 拉直）、CogView-4-Flash。纯扩散基座只为遗留 checkpoint 保留。

## Further Reading | 延伸阅读

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) — rectified flow.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) — flow matching.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) — SD3, rectified flow at scale.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) — general framework that covers FM + diffusion.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) — 1-step distillation of diffusion / flow.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042) — turbo variant.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) — flow matching in production.
