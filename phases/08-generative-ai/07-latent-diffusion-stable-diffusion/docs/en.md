# Latent Diffusion & Stable Diffusion | 潜在扩散与 Stable Diffusion

> Pixel-space diffusion on 512x512 images is a computational war crime. Rombach et al. (2022) noticed that you do not need all 786k dimensions to generate an image — you need enough to capture semantic structure, and a separate decoder for the rest. Run diffusion inside a VAE's latent space. That one idea is Stable Diffusion.

> **【中文解读】** 在 512x512 像素空间做扩散是计算灾难。Rombach 等人发现不需要全部 78.6 万维度——只需捕获语义结构，其余用解码器补充。在 VAE 的潜在空间中运行扩散，这一个想法就是 Stable Diffusion。

> **【拓展：Stable Diffusion 的革命】** Stable Diffusion 将扩散过程从像素空间移到潜在空间，计算量降低数十倍，使消费级 GPU 可以运行。开源发布后催生了 LoRA、ControlNet 等丰富生态，推动了 AIGC 的普及化。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## The Problem | 问题引入

Pixel-space diffusion at 512² means the U-Net runs on tensors of shape `[B, 3, 512, 512]`. Each sampling step is ~100 GFLOPS for a 500M-param U-Net. Fifty steps is 5 TFLOPS per image. Train on a billion images and the compute bill is absurd.

> 512² 像素空间扩散意味着 U-Net 在 `[B, 3, 512, 512]` 张量上运行。每个采样步约 100 GFLOPS。50 步就是 5 TFLOPS。在十亿图像上训练计算成本荒谬。

Most of those FLOPs go to pushing perceptually unimportant details through the net — the high-frequency texture that a lossy VAE could compress away. Rombach's idea: train a VAE once (the *first stage*), freeze it, and run diffusion entirely in the 4-channel 64×64 latent space (the *second stage*). Same U-Net. 1/16th the pixels. ~64x fewer FLOPs for comparable quality.

> 大部分 FLOPs 用于推过感知上不重要的细节。Rombach 的想法：训练一次 VAE（第一阶段），冻结它，完全在 4 通道 64×64 潜在空间运行扩散（第二阶段）。相同 U-Net。1/16 像素。约 64 倍更少 FLOPs。

This is the Stable Diffusion recipe. SD 1.x / 2.x used an 860M U-Net over `64×64×4` latents, SDXL used a 2.6B U-Net over `128×128×4`, SD3 swapped the U-Net for a Diffusion Transformer (DiT) with flow matching. Flux.1-dev (Black Forest Labs, 2024) ships a 12B-param DiT-MMDiT. All run on the same two-stage substrate.

> 这就是 Stable Diffusion 的配方。SD 1.x/2.x 用 860M U-Net 在 64×64×4 上，SDXL 用 2.6B U-Net 在 128×128×4 上，SD3 用 DiT + Flow Matching 替换 U-Net。Flux.1-dev 用 12B MMDiT。都运行在相同的两阶段基础上。

> **【中文解读】** Stable Diffusion 的核心架构是两阶段设计：(1) 第一阶段——VAE 编码器将 512x512 图像压缩到 64x64x4 潜在空间（16 倍压缩）；(2) 第二阶段——在潜在空间中运行扩散过程。U-Net 在 64x64 张量上运行，计算量降低约 64 倍。从 SD 1.x 到 SD3 的演进：U-Net → DiT（Diffusion Transformer），DDPM → Flow Matching。

> **【拓展：从 U-Net 到 DiT 的架构变迁】** SD 1.x/2.x 使用 U-Net 作为去噪网络。SD3（2024）和 FLUX 转向 DiT（Diffusion Transformer）——用 Transformer 替代 U-Net。DiT 的优势在于扩展性更好（Transformer 的缩放定律适用）、支持更高分辨率、可以更好地融合文本条件。这一架构变迁与 NLP 领域的 Transformer 统一趋势一致。

## The Concept | 核心概念

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.** Encoder `E(x) → z`, decoder `D(z) → x`. Target compression: 8× downsample in each spatial axis + adjust channels so total latent size is ~1/16th of pixel count. Loss = reconstruction (L1 + LPIPS perceptual) + KL (small weight so `z` isn't forced too Gaussian, because we do not need exact sampling from `z`). Often trained with an adversarial loss so decoded images are sharp.

   **阶段 1 — VAE。** 编码器 `E(x) → z`，解码器 `D(z) → x`。目标压缩：每空间轴 8 倍下采样。损失 = 重建（L1 + LPIPS）+ KL（小权重）。

2. **Stage 2 — diffusion on `z`.** Treat `z = E(x_real)` as the data. Train a U-Net (or DiT) to denoise `z_t`. At inference: sample `z_0` via diffusion, then `x = D(z_0)`.

   **阶段 2 — 在 `z` 上扩散。** 将 `z = E(x_real)` 视为数据。训练 U-Net（或 DiT）去噪。推理时：采样 `z_0`，然后 `x = D(z_0)`。

**Text conditioning.** Two additional components. A frozen text encoder (CLIP-L for SD 1.x, CLIP-L+OpenCLIP-G for SD 2/XL, T5-XXL for SD3 and Flux). A cross-attention injection: every U-Net block takes `[Q = image features, K = V = text tokens]` and mixes them in. The tokens are the only way text influences the image.

> **文本条件化。** 两个额外组件：冻结的文本编码器和交叉注意力注入。每个 U-Net 块用 `[Q = 图像特征, K = V = 文本 token]` 做交叉注意力。token 是文本影响图像的唯一方式。

**The loss function is identical to Lesson 06.** Same DDPM / flow matching MSE on noise. You just swap the data domain.

> **损失函数与第 06 课完全相同。** 只是交换了数据域。

## Architecture variants | 架构变体

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

The trend: replace U-Net with DiT (transformer over latent patches), scale the text encoder (T5 beats CLIP for prompt adherence), increase latent channels (4 → 16 gives more detail headroom).

> 趋势：用 DiT 替代 U-Net，扩展文本编码器（T5 在 prompt 遵循上优于 CLIP），增加潜在通道（4→16 给更多细节余量）。

## Build It | 动手实现

`code/main.py` stacks a toy 1-D "VAE" (identity encoder + decoder, for demonstration; a real VAE would be a conv net) on top of the DDPM from Lesson 06 and adds class conditioning with classifier-free guidance. It shows that the same diffusion loss works whether you run on raw 1-D values or on encoded values — the key insight.

> `code/main.py` 在第 06 课的 DDPM 之上叠加了一个玩具 1D"VAE"并添加了类别条件化的无分类器引导。它展示了扩散损失无论在原始值还是编码值上都有效——关键洞察。

### Step 1: encoder/decoder

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

A real VAE has trained weights. For pedagogy, this linear map is enough to show that diffusion operates on `z` without caring about the original data space.

> 真正的 VAE 有训练好的权重。教学上，这个线性映射足以展示扩散在 `z` 上操作而不关心原始数据空间。

### Step 2: diffusion in `z`-space

Same DDPM as Lesson 06. The data the net sees is `z = E(x)`. After sampling `z_0`, decode with `D(z_0)`.

> 与第 06 课相同的 DDPM。网络看到的数据是 `z = E(x)`。采样 `z_0` 后用 `D(z_0)` 解码。

### Step 3: classifier-free guidance

During training, drop the class label 10% of the time (replace with a null token). At inference, compute both `ε_cond` and `ε_uncond`, then:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0` = no guidance (full diversity), `w = 3` = default, `w = 7+` = saturated / over-sharp.

> `w = 0` = 无引导（完全多样性），`w = 3` = 默认，`w = 7+` = 饱和/过度锐利。

### Step 4: text conditioning (concept, not code)

Replace the class label with a frozen text encoder output. Feed the text embedding to the U-Net via cross-attention:

> 用冻结文本编码器输出替换类别标签。通过交叉注意力将文本嵌入送入 U-Net：

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

This is the only substantive difference between a class-conditional diffusion model and Stable Diffusion.

> 这是类别条件扩散模型和 Stable Diffusion 之间唯一实质性的区别。

## Pitfalls | 常见陷阱

- **VAE-scale mismatch.** SD 1.x VAEs have a scaling constant (`scaling_factor ≈ 0.18215`) applied after encoding. Forgetting this makes the U-Net train on latents with wildly wrong variance. Every checkpoint ships one.
  **VAE 尺度不匹配。** SD 1.x VAE 编码后有缩放常数。忘记它会让 U-Net 在错误方差的潜在空间上训练。
- **Text encoder silently wrong.** SD3 needs T5-XXL with >=128 tokens, and the fallback to CLIP-only is lossy. Always check `use_t5=True` or prompt fidelity craters.
  **文本编码器静默错误。** SD3 需要 T5-XXL 且 >=128 token。
- **Mixing latent spaces.** SDXL, SD3, Flux all use different VAEs. A LoRA trained on SDXL latents will not work on SD3. Hugging Face diffusers 0.30+ refuses to load mismatched checkpoints.
  **混合潜在空间。** SDXL、SD3、Flux 用不同的 VAE。SDXL 的 LoRA 不能用在 SD3 上。
- **CFG too high.** `w > 10` produces saturated, oily images and over-fits the prompt at the cost of diversity. The sweet spot is `w = 3-7`.
  **CFG 太高。** `w > 10` 产生饱和、油腻的图像。
- **Negative prompts leaking.** Empty negative prompt becomes the null token; a filled negative prompt becomes the `ε_uncond`. These are not the same; some pipelines silently default to the null.
  **负向 prompt 泄漏。** 空负向 prompt 变为 null token；填充的变为 `ε_uncond`。两者不同。

## Use It | 用框架实现

Production stacks in 2026:

> 2026 年生产技术栈：

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## Ship It | 产出物

Save `outputs/skill-sd-prompter.md`. Skill takes a text prompt + target style and outputs: model + checkpoint, CFG scale, sampler, negative prompt, resolution, optional ControlNet/IP-Adapter combo, and a per-step QA checklist.

> 保存 `outputs/skill-sd-prompter.md`。Skill 接收文本提示+目标风格，输出模型+检查点、CFG、采样器、负向 prompt 等。

## Exercises | 练习题

1. **Easy / 简单.** Run `code/main.py` with guidance `w ∈ {0, 1, 3, 7, 15}`. Record mean sample by class. At what `w` do the class means diverge past the real data means?
   用 `w ∈ {0, 1, 3, 7, 15}` 运行。在哪个 `w` 值类别均值偏离真实数据均值？
2. **Medium / 中等.** Swap the toy linear encoder for a tanh-MLP encoder/decoder pair with a reconstruction loss. Retrain diffusion on the new latents. Does sample quality change?
   将玩具线性编码器替换为 tanh-MLP 编码/解码器。在新潜在空间上重训扩散。质量变化了吗？
3. **Hard / 困难.** Set up a real Stable Diffusion inference with diffusers: load `sdxl-base`, run 30 Euler steps with CFG=7, time it. Now switch to `sdxl-turbo` with 4 steps and CFG=0. Same subject, different quality — describe what changed and why.
   用 diffusers 搭建真实 SD 推理，比较 SDXL-base 和 SDXL-Turbo。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| First stage | "The VAE" | Trained encoder/decoder pair; compresses 512² to 64². / 训练好的编码/解码器对；将 512² 压缩到 64²。 |
| Second stage | "The U-Net" | Diffusion model over the latent space. / 潜在空间上的扩散模型。 |
| CFG | "Guidance scale" / "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`; tunes conditioning strength. / 调节条件化强度。 |
| Null token | "Empty prompt embed" / "空 prompt 嵌入" | Unconditional embed used for `ε_uncond`. / 用于无条件预测的嵌入。 |
| Cross-attention | "How text gets in" / "文本如何进入" | Each U-Net block attends to text tokens as K and V. / 每个 U-Net 块对文本 token 做注意力。 |
| DiT | "Diffusion Transformer" | Replace U-Net with a transformer over latent patches; scales better. / 用 Transformer 替代 U-Net。 |
| MMDiT | "Multi-modal DiT" / "多模态 DiT" | SD3's architecture: text and image streams with joint attention. / SD3 架构：文本和图像流的联合注意力。 |
| VAE scaling factor | "Magic number" / "魔数" | Divides latents by ~5.4 so diffusion operates in unit-variance space. / 除以约 5.4 使扩散在单位方差空间操作。 |

## Production note: running Flux-12B on an 8GB consumer GPU | 生产笔记：在 8GB 消费级 GPU 上运行 Flux-12B

the reference Flux integration is the canonical "I have a consumer GPU, can I ship this?" recipe. The trick is the same three-knob recipe production inference literature lists applied to a diffusion DiT:

> 参考 Flux 集成是经典的"我只有消费级 GPU，能部署吗？"方案。三旋钮方案：

1. **Staggered loading.** Flux has three networks that never need to coexist in VRAM: T5-XXL text encoder (~10 GB in fp32), CLIP-L (small), the 12B MMDiT, and the VAE. Encode the prompt first, *delete* the encoders, load the DiT, denoise, *delete* the DiT, load the VAE, decode. Consumer 8GB GPUs only fit one stage at a time.
   **交错加载。** Flux 有三个不需要同时驻留 VRAM 的网络。编码 prompt 后删除编码器，加载 DiT，去噪后删除，加载 VAE 解码。
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)` on both the T5 encoder and the DiT. Cuts memory 8×, quality drop is imperceptible for text-to-image per Aritra's benchmarks (linked in the notebook).
   **4 位量化。** 将 T5 和 DiT 量化到 4 位，内存降 8 倍，质量损失微乎其微。
3. **CPU offload.** `pipe.enable_model_cpu_offload()` auto-swaps modules between CPU and GPU as each forward pass advances. Adds 10-20% latency but makes the pipeline run at all.
   **CPU 卸载。** 自动在 CPU 和 GPU 之间交换模块。增加 10-20% 延迟但使流水线能运行。

The memory accounting is: `10 GB T5 / 8 = 1.25 GB` quantized, `12 B params × 0.5 bytes = ~6 GB` quantized DiT, plus activations. In stas00's terms this is the extreme-end of TP=1 inference — no model parallelism, maximum quantization. For production you'd run TP=2 or TP=4 on H100s; for a single dev laptop, this is the recipe.

## Further Reading | 延伸阅读

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — Stable Diffusion.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) — SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748) — DiT.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) — SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) — CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) — Flux.1 family.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) — reference implementation for every checkpoint above.
