# Generative Models — Taxonomy & History | 生成模型 — 分类与历史

> Every image model, text model, video model, and 3D model fits in one of five buckets. Pick the wrong bucket and you will fight the math for weeks. Pick the right one and the field's last twelve years of progress stacks cleanly in your head.

> **【中文解读】** 所有图像、文本、视频和 3D 生成模型都可以归入五个类别：VAE、GAN、扩散模型、流模型和自回归模型。选错类别会让你和数学搏斗数周；选对了，过去十二年的进展就会在你脑中清晰堆叠。

> **【拓展：生成式 AI 的五大路线】** (1) VAE——变分自编码器，Stable Diffusion 的编码器；(2) GAN——生成对抗网络，StyleGAN 的核心；(3) 扩散模型——DDPM/DDIM，当前图像生成主流；(4) 流模型——Flow Matching，SD3/FLUX 的新方向；(5) 自回归——GPT 模式，VAR 应用于图像。

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## The Problem | 问题引入

A generative model does one job: given training samples drawn from some unknown distribution `p_data(x)`, output new samples that look like they came from the same distribution. Faces, sentences, MIDI files, protein structures — all the same problem if you squint.

> 生成模型只做一件事：给定从某个未知分布 `p_data(x)` 中抽取的训练样本，输出看起来来自同一分布的新样本。人脸、句子、MIDI 文件、蛋白质结构——仔细看都是同一个问题。

The rub is that `p_data` lives in a space with millions of dimensions (a 512x512 RGB image is ~786k dimensions), the samples sit on a thin manifold inside that space, and you only have maybe 10M examples. Brute-forcing the density is hopeless. Every generative model is a compromise that trades one hard problem for a slightly less hard one.

> 问题在于 `p_data` 存在于一个数百万维的空间中（一张 512x512 RGB 图像约 78.6 万维），样本只占据该空间中一个薄薄的流形，而你可能只有 1000 万个样本。暴力计算密度是 hopeless 的。每个生成模型都是一种妥协——用一个稍简单的问题替换一个难题。

Five families have survived the last twelve years. Knowing which compromise each family makes tells you why it wins on some tasks and collapses on others.

> 在过去十二年中有五个模型家族存活下来。了解每个家族做了什么妥协，就能知道它为什么在某些任务上胜出而在其他任务上崩溃。

> **【中文解读】** 生成模型的核心任务：从训练样本中学习未知分布 p_data(x)，然后生成看起来来自同一分布的新样本。挑战在于高维空间（512x512 图像约 786K 维）中的稀疏数据。五大模型家族各有不同的妥协方式：自回归/流模型直接建模密度但受限于架构；VAE/扩散模型优化密度下界；GAN 跳过密度直接生成样本。

> **【拓展：从扩散模型到 Flow Matching 的范式转移】** 2024-2026 年最重要的趋势是从扩散模型（DDPM）向 Flow Matching（流匹配）的转移。Flow Matching 训练更简单（不需要噪声调度）、采样路径更直（更少步数）、速度提升 4-10 倍。Stable Diffusion 3、FLUX、AudioCraft 2 都已采用 Flow Matching。这是生成式 AI 领域正在发生的范式变革。

## The Concept | 核心概念

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.** Write `log p(x)` as a sum you can actually evaluate. Autoregressive models (PixelCNN, WaveNet, GPT) factorize `p(x) = ∏ p(x_i | x_<i)`. Normalizing flows (RealNVP, Glow) build `p(x)` as an invertible transform of a simple base. Pro: exact likelihood, clean training loss. Con: autoregressive inference is sequential (slow for long sequences), flows need invertible architectures (architecturally restrictive).

> **1. 显式密度，可处理。** 将 `log p(x)` 写成可以实际求值的求和。自回归模型（PixelCNN、WaveNet、GPT）将联合分布分解为条件分布的乘积。标准化流（RealNVP、Glow）通过简单分布的可逆变换构建 `p(x)`。优点：精确似然，训练损失清晰。缺点：自回归推理是顺序的（长序列慢），流需要可逆架构（架构受限）。

**2. Explicit density, approximate.** Bound `log p(x)` from below (ELBO) and optimize the bound. VAEs (Kingma 2013) use an encoder-decoder with a variational posterior. Diffusion models (DDPM, Ho 2020) train a denoiser that implicitly optimizes a weighted ELBO. Diffusion is the dominant image, video, and 3D backbone in 2026.

> **2. 显式密度，近似。** 从下方约束 `log p(x)`（ELBO）并优化该下界。VAE 使用编码器-解码器和变分后验。扩散模型训练去噪器，隐式优化加权 ELBO。扩散模型是 2026 年图像、视频和 3D 的主导骨干。

**3. Implicit density.** Skip density entirely; learn a generator `G(z)` that produces samples and a discriminator `D(x)` that tells real from fake. GANs (Goodfellow 2014). Fast at inference (one forward pass) but notoriously unstable during training. StyleGAN 1/2/3 remain state of the art for fixed-domain photorealism (faces, bedrooms) even in 2026.

> **3. 隐式密度。** 完全跳过密度估计；学习一个生成器 `G(z)` 产生样本，一个判别器 `D(x)` 区分真假。GAN 推理快（单次前向传播），但训练极不稳定。StyleGAN 1/2/3 即使在 2026 年仍是固定域照片级真实感的最先进模型。

**4. Score-based / continuous-time.** Learn the gradient of the log-density `∇_x log p(x)` (the score) directly. Song & Ermon (2019) showed score matching generalizes diffusion to an SDE. Flow matching (Lipman 2023) is the 2024-2026 hotness: simulate-free training, straighter paths, 4-10x faster sampling than DDPM. Stable Diffusion 3, Flux, AudioCraft 2 all use flow matching.

> **4. 基于分数/连续时间。** 直接学习对数密度的梯度（分数函数）。Song & Ermon (2019) 证明分数匹配将扩散推广到 SDE。Flow Matching（2023）是 2024-2026 的热门：免模拟训练，更直的路径，比 DDPM 快 4-10 倍。Stable Diffusion 3、Flux、AudioCraft 2 都使用 Flow Matching。

> **【中文解读】** 分数匹配和 Flow Matching 是扩散模型的泛化和改进。分数匹配直接学习 log 密度的梯度（分数函数），Flow Matching 进一步简化了训练过程——不需要模拟 SDE，直接学习从噪声到数据的直线路径。采样速度比 DDPM 快 4-10 倍，这是 2026 年图像/视频/3D 生成的主流方向。

**5. Token-based autoregressive over discrete codes.** Compress high-dim data with a VQ-VAE or residual quantizer into a short sequence of discrete tokens, then use a Transformer to model the token sequence. Parti, MuseNet, AudioLM, VALL-E, Sora's patch tokenizer all use this. This is bucket 1 plus a learned tokenizer.

> **5. 基于离散 token 的自回归。** 用 VQ-VAE 或残差量化器将高维数据压缩为离散 token 的短序列，然后用 Transformer 建模 token 序列。Parti、MuseNet、AudioLM、VALL-E、Sora 的 patch tokenizer 都使用这种方式。这本质上是第一类加上一个学习到的 tokenizer。

## A brief history | 简要历史

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## The five-question triage | 五问分类法

When a new generative model paper drops, answer these five questions before reading the method section.

> 当一篇新的生成模型论文发布时，在读方法部分之前先回答这五个问题。

1. **What is being modeled?** Pixels, latents, discrete tokens, 3D Gaussians, meshes, waveforms?
   **正在建模什么？** 像素、潜在表示、离散 token、3D 高斯、网格、波形？
2. **Is the density explicit or implicit?** Do they write down `log p(x)`?
   **密度是显式还是隐式的？** 他们是否写出了 `log p(x)`？
3. **Sampling: one-shot or iterative?** Iterative means slower inference; one-shot usually means adversarial or distilled.
   **采样：单次还是迭代？** 迭代意味着推理更慢；单次通常意味着对抗或蒸馏。
4. **Conditioning: unconditional, class, text, image, pose?** This determines the loss and architecture scaffolding.
   **条件：无条件、类别、文本、图像、姿态？** 这决定了损失函数和架构框架。
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?** Each has known failure modes (see Lesson 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？** 每个都有已知的失效模式（见第 14 课）。

You will re-answer these five for every lesson in this phase. By the end, they will be reflex.

> 你将在本阶段的每节课中重新回答这五个问题。到最后，它们会变成你的直觉。

> **【中文解读】** 这五个问题（建模对象、显式/隐式密度、采样方式、条件类型、评估指标）是分析任何生成模型的通用框架。在后续每节课中反复回答这五个问题，可以帮助你快速理解新论文的核心贡献和技术选择。

## Build It | 动手实现

The code for this lesson is a lightweight visualization: fit a 1-D mixture-of-Gaussians from samples using three toy approaches (kernel density, discrete histogram, and a nearest-sample "GAN-ish" generator) so you can see the difference between explicit vs implicit density on a problem you can print on one screen.

> 本课的代码是一个轻量级可视化：使用三种简单方法（核密度估计、离散直方图、最近邻"GAN 风格"生成器）从样本中拟合一维高斯混合分布，让你在一屏之内看清显式密度与隐式密度的区别。

Run `code/main.py`. It draws 2000 samples from a two-mode Gaussian mixture, then prints:

> 运行 `code/main.py`。它从双峰高斯混合中抽取 2000 个样本，然后打印：

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Notice: the first two let you ask "how likely is this point?" The third cannot. This is the *explicit vs implicit* distinction that will matter for every future lesson.

> 注意：前两种方法可以回答"这个点有多大概率？"第三种不能。这就是*显式 vs 隐式*的区别，在后续每节课中都很重要。

## Use It | 用框架实现

Which family, for which task, in 2026?

> 2026 年，哪个家族适合哪个任务？

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## Ship It | 产出物

Save as `outputs/skill-model-chooser.md`.

> 保存为 `outputs/skill-model-chooser.md`。

The skill takes a task description and outputs: (1) which family to use, (2) a ranked list of three open and three hosted options, (3) the likely failure mode you should watch for, and (4) a compute/time budget.

> 该 skill 接收任务描述，输出：(1) 应使用哪个家族，(2) 三个开源和三个托管选项的排序列表，(3) 应注意的可能失效模式，(4) 计算/时间预算。

## Exercises | 练习题

1. **Easy / 简单.** For each of these five products, identify the family and backbone: ChatGPT image, Midjourney v7, Sora, Runway Gen-3, ElevenLabs. Evidence should be from public technical reports.
   对于这五个产品，识别其家族和骨干：ChatGPT image、Midjourney v7、Sora、Runway Gen-3、ElevenLabs。证据应来自公开技术报告。
2. **Medium / 中等.** The paper you are about to read tomorrow claims 100x faster sampling than diffusion. Write down three questions to check whether the speedup survives conditioning and high resolution.
   你明天要读的论文声称比扩散快 100 倍采样。写下三个问题来检查加速是否在条件生成和高分辨率下仍然成立。
3. **Hard / 困难.** Take one domain you care about (e.g. protein structure, CAD, molecules, trajectories). Answer the five-question triage for the current SOTA model in that domain and sketch what a better model would change.
   选一个你关心的领域（如蛋白质结构、CAD、分子、轨迹）。对该领域当前 SOTA 模型回答五问分类法，并勾画更好的模型会改变什么。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Production note: five families, five inference shapes | 生产笔记：五个家族，五种推理形态

Each family maps to a different inference-server cost curve. production-inference literature frames LLM inference as prefill + decode; the same decomposition applies here:

> 每个家族对应不同的推理服务器成本曲线。LLM 推理可分解为 prefill + decode；同样的分解适用于此：

- **Autoregressive (bucket 1 and 5).** Sequential decode dominates latency; KV-cache, continuous batching, and speculative decoding all apply directly.
  **自回归（第 1 和 5 类）。** 顺序解码主导延迟；KV 缓存、连续批处理和推测解码直接适用。
- **VAE / diffusion / flow-matching (buckets 2 and 4).** There is no decode in the LLM sense. Cost = `num_steps × step_cost`, and the `step_cost` is a transformer or U-Net forward at the full latent resolution. The production knobs are step count (DDIM / DPM-Solver / distillation), batch size, and precision (bf16 / fp8 / int4).
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。** LLM 意义上没有解码。成本 = `num_steps × step_cost`，生产调节旋钮是步数、批大小和精度。
- **GAN (bucket 3).** One forward pass. No schedule, no KV-cache. TTFT ≈ total latency. This is why StyleGAN still wins on narrow-domain UX.
  **GAN（第 3 类）。** 单次前向传播。没有调度，没有 KV 缓存。TTFT ≈ 总延迟。这就是 StyleGAN 在窄域 UX 上仍然胜出的原因。

When you see "faster than diffusion" in a paper abstract, translate it to "fewer steps × same step cost" or "same steps × cheaper step cost". Everything else is marketing.

> 当论文摘要中说"比扩散更快"时，翻译为"更少步数 × 相同步成本"或"相同步数 × 更便宜的步成本"。其余都是营销。

## Further Reading | 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) — the GAN paper.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) — the VAE paper.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — the DDPM paper.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) — diffusion as an SDE.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) — the flow matching paper.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) — Stable Diffusion 3.
