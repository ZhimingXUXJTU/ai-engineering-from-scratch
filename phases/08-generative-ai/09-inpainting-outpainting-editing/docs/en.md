# Inpainting, Outpainting & Image Editing | 图像修复、扩展与编辑

> Text-to-image makes new things. Inpainting fixes old ones. In production, 70% of billable image work is editing — swap a background, remove a logo, extend the canvas, regenerate a hand. Inpainting is where diffusion earns its keep.

> **【中文解读】** 文本生成图像创造新东西，图像修复（inpainting）修改已有的。生产中 70% 的付费图像工作是编辑——换背景、去 logo、扩展画布、重画手。Inpainting 是扩散模型真正赚钱的地方。

> **【拓展：Photoshop 生成式填充】** Adobe Photoshop 的生成式填充（Generative Fill）就是基于 inpainting 技术。它让非专业用户也能一键移除/替换图像中的任何内容。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 8 · 08 (ControlNet & LoRA)
**Time:** ~75 minutes

## The Problem | 问题引入

A client sends a perfect product photo with a distracting sign in the background. You want to erase the sign and leave everything else pixel-identical. You cannot run text-to-image from scratch — the result will have a different color, different lighting, different product angle. You want to regenerate *only* the masked region, and you want the regeneration to respect the surrounding context.

> 客户发来一张完美的产品照片，背景有分散注意力的标志。你想擦除标志并保持其他像素完全一致。你不能从头运行文生图——结果会有不同的颜色、光照和产品角度。你想只重新生成*被遮蔽的区域*，并让重新生成的内容尊重周围上下文。

That is inpainting. Variants:

> 这就是 inpainting（图像修复）。变体：

- **Inpainting.** Regenerate inside a mask, keep outside pixels.
  **图像修复。** 在遮蔽内重新生成，保持外部像素。
- **Outpainting.** Regenerate outside a mask (or beyond the canvas), keep inside.
  **图像扩展。** 在遮蔽外重新生成，保持内部。
- **Image editing.** Regenerate the whole image but keep semantic or structural fidelity to the original (SDEdit, InstructPix2Pix).
  **图像编辑。** 重新生成整个图像但保持语义或结构一致性。

Every diffusion pipeline in 2026 ships an inpainting mode. Flux.1-Fill, Stable Diffusion Inpaint, SDXL-Inpaint, DALL-E 3 Edit. They work on the same principle.

> 2026 年每个扩散流水线都有 inpainting 模式。Flux.1-Fill、SD-Inpaint、SDXL-Inpaint、DALL-E 3 Edit。原理相同。

> **【中文解读】** Inpainting（图像修复）是生产环境中最常见的图像编辑需求。核心挑战：只重新生成被遮蔽的区域，同时保持与周围上下文的一致性。正确的做法是训练修改过的 U-Net，接受 9 通道输入（4 通道噪声潜在 + 4 通道编码图像 + 1 通道遮罩），让模型"看到"遮蔽区域周围的上下文。

> **【拓展：Photoshop 生成式填充与商业 Inpainting】** Adobe Photoshop 的生成式填充是 inpainting 技术的里程碑式应用。它结合了扩散模型和边缘融合技术，让用户可以通过自然语言指令移除/替换图像中的任何内容。类似的商业应用还包括 Canva 的 Magic Edit、Figma 的 AI 图像编辑等。

## The Concept | 核心概念

![Inpainting: mask-aware denoising with context-preserving reinjection](../assets/inpainting.svg)

### The naive approach (and why it's wrong)

> ### 朴素方法（以及为什么它不对）

Run standard text-to-image with a mask. At each sampling step, replace the unmasked region of the noisy latent with the forward-diffused clean image. It works... badly. Boundary artifacts bleed through because the model has no information about what is in the masked region.

> 用遮蔽运行标准文生图。在每个采样步替换未遮蔽区域。效果很差——边界伪影渗透，因为模型不知道遮蔽区域里有什么。

### The proper inpainting model

> ### 正确的 Inpainting 模型

Train a modified U-Net that takes 9 input channels instead of 4:

```
input = concat([ noisy_latent (4ch), encoded_image (4ch), mask (1ch) ], dim=channel)
```

The extra channels are a copy of the VAE-encoded source image plus a single-channel mask. At training time, you randomly mask regions of the image and train the model to denoise only the masked region while the unmasked region is given as a clean conditioning signal. At inference, the model can "see" what surrounds the masked region and produces coherent completions.

SD-Inpaint, SDXL-Inpaint, Flux-Fill all use this 9-channel (or analog) input. Diffusers `StableDiffusionInpaintPipeline`, `FluxFillPipeline`.

> SD-Inpaint、SDXL-Inpaint、Flux-Fill 都使用这种 9 通道（或类似）输入。

### SDEdit (Meng et al., 2022) — free editing

> ### SDEdit — 免费编辑

Add noise to the source image up to some intermediate `t`, then run the reverse chain from `t` down to 0 with a new prompt. No retraining. The choice of starting `t` trades fidelity for creative freedom:

> 给源图像加噪声到某个中间 `t`，然后用新 prompt 反向去噪。无需重训。起始 `t` 的选择权衡保真度与创作自由：

- `t/T = 0.3` → nearly identical to source, small stylistic changes / 几乎与源相同，小风格变化
- `t/T = 0.6` → moderate edits, preserves coarse structure / 中等编辑，保留粗结构
- `t/T = 0.9` → generated from near-noise, minimal source preservation / 从近噪声生成，最小源保留

### InstructPix2Pix (Brooks et al., 2023)

> ### InstructPix2Pix

Fine-tune a diffusion model on `(input_image, instruction, output_image)` triples. At inference, condition on both the input image and a text instruction ("make it sunset", "add a dragon"). Two CFG scales: image scale and text scale.

> 在 `(输入图像, 指令, 输出图像)` 三元组上微调扩散模型。推理时同时以输入图像和文本指令为条件。

### RePaint (Lugmayr et al., 2022)

> ### RePaint

Keep a standard unconditional diffusion model. At each reverse step, resample — jump back to a noisier state occasionally and regenerate. Avoids boundary artifacts. Used when you don't have a trained inpainting model.

> 保持标准无条件扩散模型。在每个反向步偶尔重采样——跳回更噪的状态重新生成。避免边界伪影。

## Build It | 动手实现

`code/main.py` implements a toy 1-D inpainting scheme on 5-dimensional data. We train a DDPM on 5-D mixture data where each sample is 5 floats from one of two clusters. At inference, we "mask" 2 of the 5 dimensions, inject the noisy-forward version of the unmasked three at each step, and regenerate only the masked dimensions.

### Step 1: 5-D DDPM data

```python
def sample_data(rng):
    cluster = rng.choice([0, 1])
    center = [-1.0] * 5 if cluster == 0 else [1.0] * 5
    return [c + rng.gauss(0, 0.2) for c in center], cluster
```

### Step 2: train denoiser over all 5 dims

Standard DDPM. Net outputs 5-D noise prediction for 5-D noisy input.

### Step 3: at inference, mask-aware reverse

```python
def inpaint_step(x_t, mask, clean_image, alpha_bars, t, rng):
    # replace unmasked dims with a freshly noised version of the clean source
    a_bar = alpha_bars[t]
    for i in range(len(x_t)):
        if not mask[i]:
            x_t[i] = math.sqrt(a_bar) * clean_image[i] + math.sqrt(1 - a_bar) * rng.gauss(0, 1)
    # ...then run the normal reverse step on x_t
```

This is the naive approach and it works on toy 1-D data. Real image inpainting uses the 9-channel input because texture coherence matters more.

### Step 4: outpainting

Outpainting is inpainting with the mask inverted: mask the new (previously non-existent) canvas, fill the rest with the original. Identical training objective.

## Pitfalls | 常见陷阱

- **Seams.** The naive approach leaves visible boundaries because gradient info doesn't flow across the mask. Fix: dilate the mask by 8-16 pixels, or use a proper inpainting model.
- **Mask leakage.** If the conditioning image's unmasked region is low-quality or noisy, it pollutes the generation inside the mask. Denoise or blur slightly.
- **CFG interacts with mask size.** High CFG on a small mask = saturated patch. Reduce CFG for small edits.
- **SDEdit fidelity cliff.** Going from `t/T = 0.5` to `t/T = 0.6` can lose the subject's identity. Sweep and checkpoint.
- **Prompt mismatch.** The prompt should describe the *whole* image, not just the new content. "A cat sitting on a chair" not "a cat".

## Use It | 用框架实现

| Task / 任务 | Pipeline / 方案 |
|------|----------|
| Remove object, small mask / 移除物体 | SD-Inpaint or Flux-Fill, standard prompt |
| Replace sky / 替换天空 | SD-Inpaint + "blue sky at sunset" |
| Extend canvas / 扩展画布 | SDXL outpaint mode (8px feather) or Flux-Fill with outpaint mask |
| Regenerate hand / face / 重画手/脸 | SD-Inpaint with prompt re-describing the subject + ControlNet-Openpose |
| Change style of one region / 改变区域风格 | SDEdit at `t/T=0.5` on masked region |
| "Make it sunset" / "变成日落" | InstructPix2Pix or Flux-Kontext |
| Background replacement / 背景替换 | SAM mask → SD-Inpaint |
| Ultra-high-fidelity / 超高保真 | Flux-Fill or GPT-Image (hosted) for hardest cases |

SAM (Meta's Segment Anything, 2023) + diffusion inpaint is the 2026 background-removal pipeline. SAM 2 (2024) works on video.

> SAM（Meta 的 Segment Anything）+ 扩散 inpaint 是 2026 年的背景移除流水线。SAM 2（2024）支持视频。

## Ship It | 产出物

Save `outputs/skill-editing-pipeline.md`. Skill takes an original image + edit description + optional mask (or SAM prompt) and outputs: mask-generation approach, base model, CFG scales (image + text), SDEdit-t or inpainting mode, and QA checklist.

## Exercises | 练习题

1. **Easy.** In `code/main.py`, vary the fraction of dimensions masked from 0.2 to 0.8. At what fraction does the inpaint quality (residual in masked dims) equal unconditional generation?
2. **Medium.** Implement RePaint: at every 10th reverse step, jump back 5 steps (add noise) and re-denoise. Measure whether it reduces boundary residual at the mask edge.
3. **Hard.** Use Hugging Face diffusers to compare: SD 1.5 Inpaint + ControlNet-Openpose vs Flux.1-Fill on 20 face-regeneration tasks. Score pose adherence and identity preservation separately.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Inpainting | "Fill the hole" | Regenerate inside a mask; keep outside pixels. |
| Outpainting | "Extend the canvas" | Regenerate outside the canvas; keep inside. |
| 9-channel U-Net | "Proper inpainting model" | U-Net with `noisy \| encoded-source \| mask` as input. |
| SDEdit | "Img2img with noise level" | Noise to time `t`, denoise with new prompt. |
| InstructPix2Pix | "Text-only edits" | Fine-tuned diffusion on (image, instruction, output) triples. |
| RePaint | "No retraining" | Re-noise periodically during reverse to reduce seams. |
| SAM | "Segment Anything" | Mask generator by clicks or boxes; pairs with inpaint. |
| Flux-Kontext | "Edit with context" | Flux variant that accepts a reference image + instruction for edits. |

## Production note: edit pipelines are latency-sensitive | 生产笔记：编辑流水线对延迟敏感

Users editing an image expect sub-5-second round trips. A 30-step SDXL-Inpaint at 1024² is 3-4 s on an L4, plus SAM mask generation (~200 ms) and VAE encode/decode (~500 ms combined). In production framing, this is TTFT-bound rather than throughput-bound — batch 1, low concurrency, minimize every stage:

- **SAM-H is the slow one.** SAM-H at 1024² is ~200 ms; SAM-ViT-B is ~40 ms with minor quality loss. SAM 2 (video) adds temporal overhead; do not use it for single-image edits.
- **Skip the encode when possible.** `pipe.image_processor.preprocess(img)` encodes to latents. If you have the latents from the previous generation (typical in iterative-edit UIs), pass them directly via `latents=...` to skip one VAE encode.
- **Mask dilation matters for throughput too.** A small mask means most of the U-Net forward pass is wasted (the unmasked pixels are clamped anyway). `diffusers`' `StableDiffusionInpaintPipeline` runs the full U-Net regardless; only the 9-channel proper-inpaint variants exploit masked compute.
- **Flux-Kontext is the 2025 answer.** Single forward pass over `(source_image, instruction)` — no separate mask, no SDEdit noise sweep. On an H100 it ships an edit in ~1.5 s. The architectural lesson: collapse the stages.

## Further Reading | 延伸阅读

- [Lugmayr et al. (2022). RePaint: Inpainting using Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2201.09865) — training-free inpainting.
- [Meng et al. (2022). SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073) — SDEdit.
- [Brooks, Holynski, Efros (2023). InstructPix2Pix](https://arxiv.org/abs/2211.09800) — text-instruction editing.
- [Kirillov et al. (2023). Segment Anything](https://arxiv.org/abs/2304.02643) — SAM, the mask source.
- [Ravi et al. (2024). SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) — video SAM.
- [Hertz et al. (2022). Prompt-to-Prompt Image Editing with Cross-Attention Control](https://arxiv.org/abs/2208.01626) — attention-level editing.
- [Black Forest Labs (2024). Flux.1-Fill and Flux.1-Kontext](https://blackforestlabs.ai/flux-1-tools/) — 2024 tooling.
