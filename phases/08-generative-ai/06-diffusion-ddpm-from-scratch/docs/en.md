# Diffusion Models — DDPM from Scratch | 扩散模型 — 从零实现 DDPM

> Ho, Jain, Abbeel (2020) gave the field a recipe it could not quit. Destroy the data with noise over a thousand small steps. Train one neural net to predict the noise. Reverse the process at inference. Today every mainstream image, video, 3D, and music model runs on this loop, possibly with flow matching or consistency tricks on top.

> **【中文解读】** DDPM 的核心流程：用一千步逐步给数据加噪声破坏数据，训练一个神经网络预测噪声，推理时反向去除噪声。2026 年所有主流图像/视频/3D/音乐模型都基于这个循环（可能加上 Flow Matching 或一致性技巧）。

> **【拓展：扩散模型是当前 AI 生成的核心】** Stable Diffusion、DALL-E 3、Midjourney、Sora 都基于扩散模型。DDPM 证明了一个简单的去噪目标可以产生惊人的生成能力。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## The Problem | 问题引入

You want a sampler for `p_data(x)`. GANs play a minimax game that often diverges. VAEs produce blurry samples from a Gaussian decoder. What you really want is a training objective that is (a) a single stable loss (no saddle point, no minimax), (b) a lower bound on `log p(x)` (so you have likelihoods), and (c) samples that match SOTA quality.

> 你想要 `p_data(x)` 的采样器。GAN 的 minimax 博弈经常发散。VAE 的高斯解码器产生模糊样本。你真正想要的是：(a) 单一稳定的损失，(b) `log p(x)` 的下界，(c) 样本质量匹配 SOTA。

Sohl-Dickstein et al. (2015) had a theoretical answer: define a Markov chain `q(x_t | x_{t-1})` that gradually adds Gaussian noise, and train a reverse chain `p_θ(x_{t-1} | x_t)` to denoise. Ho, Jain, Abbeel (2020) showed the loss could be simplified to one line — predict the noise — and cleaned up the math. In 2020 this was a curiosity. In 2021 it produced state-of-the-art samples. In 2022 it became Stable Diffusion. In 2026 it is the substrate.

> Sohl-Dickstein (2015) 给出了理论答案：定义逐步加高斯噪声的马尔可夫链，训练反向链去噪。Ho 等人 (2020) 将损失简化为一行——预测噪声。2020 年是个新奇事物，2021 年产出 SOTA 样本，2022 年成为 Stable Diffusion，2026 年它就是基础设施。

> **【中文解读】** DDPM 的三步流程：(1) 前向过程——逐步加高斯噪声直到数据变为纯噪声；(2) 训练——学习一个网络预测每一步添加的噪声；(3) 反向过程——从纯噪声开始逐步去噪，恢复出逼真数据。损失函数简化为"预测噪声"这一个目标——训练稳定，无需对抗博弈。

> **【拓展：从 DDPM 到实用扩散模型】** DDPM 原始论文在像素空间操作，速度慢（需要 1000 步去噪）。三个关键改进使其成为实用工具：(1) DDIM（2020）将采样步数从 1000 降到 20-50；(2) 潜在扩散（2021，Rombach）在 VAE 潜在空间中操作，大幅降低计算量；(3) CFG（Classifier-Free Guidance，2022）通过条件/无条件预测的差值提升生成质量。

## The Concept | 核心概念

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.** Add Gaussian noise in `T` small steps. The closed form — the reason the math is tractable — is that the cumulative step is also Gaussian:

> **前向过程 `q`。** 在 `T` 小步中逐步添加高斯噪声。闭式解——数学可处理的原因——是累积步骤也是高斯的：

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

where `α̅_t = ∏_{s=1..t} (1 - β_s)` for a schedule of `β_t`. Pick `β_t` from 1e-4 to 0.02 linearly over T=1000 steps and `x_T` is approximately `N(0, I)`.

> 其中 `α̅_t = ∏_{s=1..t} (1 - β_s)`。将 `β_t` 从 1e-4 到 0.02 线性排列 T=1000 步，`x_T` 近似 `N(0, I)`。

**Reverse process `p_θ`.** Learn a neural net `ε_θ(x_t, t)` that predicts the noise that was added. Given `x_t`, denoise by:

> **反向过程 `p_θ`。** 学习一个神经网络 `ε_θ(x_t, t)` 预测添加的噪声。给定 `x_t`，去噪方式为：

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

where `σ_t` is either `sqrt(β_t)` or a learned variance. The expression is ugly but it is just algebra — solving for `x_{t-1}` given the posterior `q(x_{t-1} | x_t, x_0)` and substituting `x_0` with its noise-predicted estimate.

> 其中 `σ_t` 是 `sqrt(β_t)` 或学习到的方差。表达式看起来复杂但只是代数——给定后验 `q(x_{t-1} | x_t, x_0)` 求解 `x_{t-1}`。

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Sample `x_0` from data, pick a random `t`, sample `ε ~ N(0, I)`, compute the noisy `x_t` in one shot via the closed form, and regress on the noise. One loss, no minimax, no KL, no reparameterization tricks.

> 从数据采样 `x_0`，随机选 `t`，采样 `ε ~ N(0, I)`，通过闭式一次计算含噪 `x_t`，对噪声做回归。一个损失，无 minimax，无 KL，无重参数化技巧。

**Sampling.** Start `x_T ~ N(0, I)`. Iterate the reverse step from `t = T` to `1`. Done.

> **采样。** 从 `x_T ~ N(0, I)` 开始，从 `t = T` 到 `1` 迭代反向步骤。完成。

## Why it works | 为什么有效

Three intuitions:

> 三个直觉：

1. **Denoising is easy; generating is hard.** At `t=T`, the data is pure noise — the net has to solve a trivial problem. At `t=0`, the net only has to clean up a few pixels. At intermediate `t`, the problem is hard but the net has many gradients flowing through the same weights from every noise level.
   **去噪容易，生成难。** 在 `t=T` 时，数据是纯噪声——网络只需解决简单问题。在 `t=0` 时，网络只需清理少量像素。

2. **Score matching in disguise.** Vincent (2011) proved that predicting the noise is equivalent to estimating `∇_x log q(x_t | x_0)`, the *score*. The reverse SDE uses this score to walk up the density gradient — a guided random walk toward high-probability regions.
   **伪装的分数匹配。** 预测噪声等价于估计分数函数 `∇_x log q(x_t | x_0)`。反向 SDE 利用这个分数沿密度梯度上升。

3. **The ELBO reduces to simple MSE.** The full variational lower bound has a KL term per timestep. With DDPM's parameterization those KL terms simplify to MSE on noise prediction with specific coefficients; Ho dropped the coefficients (calling it "simple" loss) and quality *improved*.
   **ELBO 简化为简单 MSE。** 完整的变分下界每个时间步都有 KL 项。Ho 丢弃了系数后质量反而*提升*了。

## Build It | 动手实现

`code/main.py` implements a 1-D DDPM. Data is a two-mode mixture. The "net" is a tiny MLP that takes `(x_t, t)` and outputs predicted noise. Training is the one-line loss. Sampling iterates the reverse chain.

> `code/main.py` 实现了一维 DDPM。数据是双峰混合。"网络"是一个微型 MLP，接收 `(x_t, t)` 输出预测噪声。训练就是那一行损失。采样迭代反向链。

### Step 1: the forward schedule (closed form)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### Step 2: sample `x_t` in one shot

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Step 3: one training step

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### Step 4: reverse sampling

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

For a 1-D problem with 40 timesteps and a 24-unit MLP, this learns the two-mode mixture in ~200 epochs.

> 对于 40 个时间步和 24 单元 MLP 的一维问题，约 200 轮即可学会双峰混合。

## Time conditioning | 时间条件化

The net needs to know which timestep it is denoising. Two standard options:

> 网络需要知道它在去噪哪个时间步。两种标准选择：

- **Sinusoidal embedding.** Like Transformer positional encoding. `embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`. Pass through an MLP, broadcast into the net.
  **正弦嵌入。** 类似 Transformer 位置编码。
- **Film / group-norm conditioning.** Project embedding to per-channel scale/bias (FiLM) at each block.
  **FiLM / 组归一化条件化。** 将嵌入投影为每通道缩放/偏置。

Our toy code uses sinusoidal → concat. Production U-Nets use FiLM.

> 我们的玩具代码用正弦→拼接。生产 U-Net 用 FiLM。

## Pitfalls | 常见陷阱

- **Schedule matters a lot.** Linear `β` is the DDPM default but cosine schedule (Nichol & Dhariwal, 2021) gives better FID for the same compute. Switch schedules if quality plateaus.
  **调度很重要。** 线性 `β` 是 DDPM 默认但余弦调度在相同计算量下 FID 更好。
- **Timestep embedding is fragile.** Passing raw `t` as a float works for toy 1-D but fails for images; always use a proper embedding.
  **时间步嵌入脆弱。** 原始 `t` 浮点数在玩具 1D 可用但图像不行。
- **V-prediction vs ε-prediction.** For narrow regimes (very small or very large t), `ε` has poor signal-to-noise. V-prediction (`v = α·ε - σ·x`) is more stable; SDXL, SD3, and Flux use it.
  **V 预测 vs ε 预测。** 在极端时间步，V 预测更稳定；SDXL、SD3、Flux 使用它。
- **Classifier-free guidance.** At inference, compute both conditional and unconditional `ε`, then `ε_cfg = (1 + w) · ε_cond - w · ε_uncond` with `w ≈ 3-7`. Covered in Lesson 08.
  **无分类器引导。** 推理时计算条件和无条件预测的差值。第 08 课详述。
- **1000 steps is a lot.** Production uses DDIM (20-50 steps), DPM-Solver (10-20 steps), or distillation (1-4 steps). See Lesson 12.
  **1000 步太多了。** 生产用 DDIM（20-50 步）、DPM-Solver（10-20 步）或蒸馏（1-4 步）。

## Use It | 用框架实现

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

Diffusion is the universal generative backbone. Flow matching (Lesson 13) is the 2024-2026 competitor that usually wins on inference speed for the same quality.

> 扩散是通用生成骨干。Flow Matching（第 13 课）是 2024-2026 的竞争者，通常在相同质量下推理速度更快。

## Ship It | 产出物

Save `outputs/skill-diffusion-trainer.md`. Skill takes a dataset + compute budget and outputs: schedule (linear/cosine/sigmoid), prediction target (ε/v/x), number of steps, guidance scale, sampler family, and an eval protocol.

> 保存 `outputs/skill-diffusion-trainer.md`。Skill 接收数据集+计算预算，输出调度、预测目标、步数、引导缩放、采样器族和评估协议。

## Exercises | 练习题

1. **Easy / 简单.** Change T from 40 to 10 in `code/main.py`. How does sample quality (visual histogram of outputs) degrade? At what T does the two-mode structure collapse?
   将 T 从 40 改为 10。样本质量如何退化？双峰结构在哪个 T 值坍塌？
2. **Medium / 中等.** Switch from ε-prediction to v-prediction. Re-derive the reverse step. Compare final sample quality.
   从 ε 预测切换到 v 预测。重新推导反向步骤。比较最终样本质量。
3. **Hard / 困难.** Add classifier-free guidance. Condition on a class label `c ∈ {0, 1}`, drop it 10% of the time during training, and at sampling time use `ε = (1+w)·ε_cond - w·ε_uncond`. Measure the conditional-mode-hit rate at `w = 0, 1, 3, 7`.
   添加无分类器引导。测量 `w = 0, 1, 3, 7` 时的条件模式命中率。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Production note: diffusion inference is a step-count problem | 生产笔记：扩散推理是步数问题

The DDPM paper runs T=1000 reverse steps. Nobody ships that in production. Every real inference stack picks one of three strategies — and each maps cleanly to production framing of "where is the latency coming from":

> DDPM 论文用 T=1000 反向步。生产中没人这么做。每种策略对应生产中"延迟来自哪里"：

1. **Faster sampler, same model.** DDIM (20-50 steps), DPM-Solver++ (10-20), UniPC (8-16). Drop-in replacement of the reverse loop; the trained `ε_θ` weights are untouched. Cuts latency 20-50×.
   **更快的采样器，相同模型。** DDIM、DPM-Solver++、UniPC。即插即用替换反向循环，降低延迟 20-50 倍。
2. **Distillation.** Train a student to match the teacher in fewer steps: Progressive Distillation (2 → 1), Consistency Models (arbitrary → 1-4), LCM, SDXL-Turbo, SD3-Turbo. Cuts latency another 5-10×, requires retraining.
   **蒸馏。** 训练学生模型在更少步数匹配教师。再降延迟 5-10 倍，需要重训。
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`, TensorRT-LLM's diffusion backends, `xformers`/SDPA attention, bf16 weights. Cuts per-step latency ~2×. Stacks with (1) and (2).
   **缓存和编译。** torch.compile、TensorRT、xformers、bf16。降低每步延迟约 2 倍。

For a production diffusion server the budget conversation is the same as production literature describes for LLMs: latency is `num_steps × step_cost + VAE_decode`, throughput is `batch_size × (num_steps × step_cost)^-1`. TTFT is small (one step); TPOT-equivalent is the full response time because image generation is "all-at-once" from the user's perspective.

> 生产扩散服务器的预算对话与 LLM 相同：延迟 = `num_steps × step_cost + VAE_decode`。TTFT 很小（一步）；TPOT 等价物是完整响应时间。

## Further Reading | 延伸阅读

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) — the diffusion paper, ahead of its time.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) — DDIM, fewer steps.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672) — cosine schedule, learned variance.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) — classifier guidance.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) — CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) — unified notation, cleanest recipe.
