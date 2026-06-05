# ControlNet, LoRA & Conditioning | ControlNet、LoRA 与条件控制

> Text alone is a clumsy control signal. ControlNet lets you clone a pretrained diffusion model and steer it with a depth map, pose skeleton, scribble, or edge image. LoRA lets you fine-tune a 2B-parameter model by training 10 million parameters. Together they turned Stable Diffusion from a toy into the 2026 image pipeline that ships at every agency.

> **【中文解读】** 纯文本控制太粗糙。ControlNet 用深度图、姿态骨架、涂鸦或边缘图精确控制生成；LoRA 只训练 1000 万参数就能微调 20 亿参数的模型。两者结合让 Stable Diffusion 从玩具变成了 2026 年每个设计公司都在用的图像流水线。

> **【拓展：LoRA 是大模型时代的微调标准】** LoRA（低秩适配）不仅在图像生成中使用，也被广泛用于 LLM 微调（如 LLaMA-LoRA）。只需训练 0.1% 的参数就能适配新任务/新风格，使 AI 定制化成本大幅降低。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## The Problem | 问题引入

A prompt like "a woman in a red dress walking a dog on a busy street" gives the model no information about *where* the dog is, *what pose* the woman is in, or *the perspective* of the street. Text pins down about 10% of what you need to specify an image. The rest is visual and cannot be described efficiently in words.

> 像"一个穿红裙的女人在繁忙的街道上遛狗"这样的提示没有告诉模型狗在*哪里*、女人是*什么姿态*、街道的*视角*如何。文本只能确定约 10% 的图像信息。其余是视觉的，无法用文字高效描述。

Training a new conditional model from scratch for every signal (pose, depth, canny, segmentation) is prohibitive. You want to keep the 2.6B-param SDXL backbone frozen, attach a small side-network that reads the conditioning, and have it nudge the backbone's intermediate features. That is ControlNet.

> 为每个信号（姿态、深度、边缘、分割）从头训练新的条件模型代价太高。你想要保持 2.6B 参数的 SDXL 骨干冻结，附加一个读取条件的小型侧网络。这就是 ControlNet。

You also want to teach the model new concepts (your face, your product, your style) without retraining the full model. You want a 100x smaller delta. That is LoRA — low-rank adapters that plug into existing attention weights.

> 你还想教模型新概念（你的脸、你的产品、你的风格）而不重训整个模型。你需要小 100 倍的增量。这就是 LoRA——插入现有注意力权重的低秩适配器。

ControlNet + LoRA + text = the 2026 practitioner's toolkit. Most production image pipelines layer 2-5 LoRAs, 1-3 ControlNets, and an IP-Adapter on top of an SDXL / SD3 / Flux base.

> ControlNet + LoRA + text = 2026 年实践者的工具箱。大多数生产图像流水线在 SDXL/SD3/Flux 基础上叠加 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter。

## The Concept | 核心概念

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

Take a pretrained SD. *Clone* the encoder half of the U-Net. Freeze the original. Train the clone to accept an extra conditioning input (edges, depth, pose). Connect the clone back to the decoder half of the original with *zero-convolution* skip connections (1×1 convs initialized to zero — start as a no-op, learn a delta).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

Zero-conv init means ControlNet starts as identity — no harm even before training. Train on 1M (prompt, condition, image) triples with the standard diffusion loss.

Per-modality ControlNets ship as small side models (~360M for SDXL, ~70M for SD 1.5). You can compose them at inference:

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### LoRA (Hu et al., 2021)

For any linear layer `W ∈ R^{d×d}` in the model, freeze `W` and add a low-rank delta:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

with `r << d`. Rank 4-16 is standard for attention, rank 64-128 for heavy fine-tunes. Number of new parameters: `2 · d · r` instead of `d²`. For SDXL attention with `d=640`, `r=16`: 20k params per adapter instead of 410k — a 20x reduction. Across the whole model: a LoRA is usually 20-200MB vs the base 5GB.

At inference you can scale the LoRA: `W' = W + α · B @ A`. `α = 0.5-1.5` is normal. Multiple LoRAs stack additively (with the usual caveat that they interact in non-linear ways).

### IP-Adapter (Ye et al., 2023)

A tiny adapter that accepts an *image* as conditioning (alongside text). Uses the CLIP image encoder to produce image tokens, injects them into cross-attention alongside text tokens. ~20MB per base model. Lets you do "generate an image in the style of this reference" without a LoRA.

## Composability matrix | 可组合性矩阵

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

ControlNet ≈ spatial. LoRA ≈ semantic. Use both.

> ControlNet ≈ 空间控制。LoRA ≈ 语义控制。两者配合使用。

> **【中文解读】** ControlNet 的核心机制：克隆 SD U-Net 编码器，冻结原始部分，训练克隆部分接受额外条件输入（边缘、深度、姿态）。零卷积（zero-convolution）初始化确保训练开始时 ControlNet 不影响原始模型。LoRA 在线性层上添加低秩矩阵 B@A，只训练极少量参数（20-200MB vs 基础模型 5GB）。

> **【拓展：ControlNet + LoRA 的组合控制】** 实际生产中，ControlNet（空间控制）和 LoRA（风格/主题控制）通常组合使用。例如：ControlNet 控制人物姿态，LoRA 注入特定艺术风格，文本 prompt 描述场景内容。这种三层控制机制是 2026 年商业 AI 图像服务的标准配置。IP-Adapter 则提供了"用图片控制图片"的第四维度。

## Build It | 动手实现

`code/main.py` simulates the two mechanisms on 1-D:

1. **LoRA.** A pretrained linear layer `W`. Freeze it. Train a low-rank `B @ A` such that `W + BA` matches a target linear layer. Show that `r = 1` is enough to learn a rank-1 correction perfectly.

2. **ControlNet-lite.** A "frozen base" predictor and a "side network" that reads an extra signal. The side network's output is gated by a learnable scalar initialized to zero (our version of zero-conv). Train and watch the gate ramp up.

### Step 1: LoRA math

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Step 2: zero-init side network

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

At step 0 the output is identical to base. Early training updates `gate` slowly — no catastrophic drift.

> 在第 0 步输出与基础模型完全相同。训练初期 `gate` 更新缓慢——没有灾难性偏移。

## Pitfalls | 常见陷阱

- **Over-scaling LoRAs.** `α = 2` or `α = 3` is a common "make it stronger" hack that produces over-stylized / broken outputs. Keep `α ≤ 1.5`.
  **LoRA 过度缩放。** `α = 2` 或 `α = 3` 是常见的"加强"做法，会产生过度风格化/损坏的输出。保持 `α ≤ 1.5`。
- **ControlNet weight conflict.** Using a Pose ControlNet at weight 1.0 and a Depth ControlNet at weight 1.0 usually overshoots. Sum of weights ≈ 1.0 is a safe default.
  **ControlNet 权重冲突。** 权重之和 ≈ 1.0 是安全的默认值。
- **LoRA on the wrong base.** SDXL LoRAs silently no-op on SD 1.5 because the attention dimensions do not match. Diffusers will warn in 0.30+.
  **LoRA 用错基础模型。** SDXL LoRA 在 SD 1.5 上会静默无效。
- **Textual Inversion drift.** Tokens trained on one checkpoint drift badly on another. LoRA is more portable.
  **Textual Inversion 漂移。** 在一个检查点上训练的 token 在另一个上严重漂移。
- **LoRA weight-merging and storage.** You can bake a LoRA into the base model weights for faster inference (no runtime addition), but you lose the ability to scale `α` at runtime. Keep both versions.
  **LoRA 权重合并。** 可以烘焙到基础模型中加速推理，但失去运行时调节 `α` 的能力。

## Use It | 用框架实现

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## Ship It | 产出物

Save `outputs/skill-sd-toolkit-composer.md`. Skill takes a task (input assets: prompt, optional reference image, optional pose, optional depth, optional scribble) and outputs the tool stack, weights, and a reproducible seed protocol.

## Exercises | 练习题

1. **Easy / 简单.** In `code/main.py`, vary the LoRA rank `r` from 1 to 4. At what rank does the LoRA exactly match a rank-2 target delta?
   在 `code/main.py` 中将 LoRA 秩 `r` 从 1 变到 4。在哪个秩时 LoRA 恰好匹配秩 2 目标？
2. **Medium / 中等.** Train two separate LoRAs on two target transforms. Load them together and show their additive interaction. When does the interaction break linearity?
   在两个目标变换上分别训练 LoRA。一起加载并展示加性交互。交互何时打破线性？
3. **Hard / 困难.** Use diffusers to stack: SDXL-base + Canny-ControlNet (weight 0.8) + a style LoRA (α 0.8) + IP-Adapter (weight 0.6). Measure FID-vs-prompt-adherence trade-off as the stack weights vary.
   用 diffusers 堆叠组合，测量 FID 与 prompt 遵循的权衡。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## Production note: LoRA swaps, ControlNet lanes, multi-tenant serving | 生产笔记：LoRA 热插拔、ControlNet 通道、多租户服务

A real text-to-image SaaS serves hundreds of LoRAs and a dozen ControlNets over the same base checkpoint. The serving problem looks a lot like LLM multi-tenancy (the production literature covers the LLM case under continuous batching and LoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.** Merging `W' = W + α·B·A` into the base gives ~3-5% faster per-step inference but freezes `α` and the base. Keep LoRAs hot in VRAM as rank-r deltas; diffusers exposes `pipe.load_lora_weights()` + `pipe.set_adapters([...], adapter_weights=[...])` for per-request activation. Swap cost is the `2 · d · r · num_layers` weights — MB-scale, sub-second.
- **ControlNet as a second attention lane.** The cloned encoder runs in parallel with the base. Two ControlNets at weight 1.0 each = two extra forward passes per step, not one merged pass. Batch-size headroom drops quadratically. Budget for ~1.5× step cost per active ControlNet.
- **Quantized LoRAs too.** If you quantized the base (see Lesson 07, Flux on 8GB), the LoRA delta also quantizes cleanly to 8-bit or 4-bit. QLoRA-style loading lets you stack 5-10 LoRAs on top of a 4-bit Flux base without blowing memory.

Flux-specific: Niels' Flux-on-8GB notebook quantizes the base to 4-bit; stacking a style LoRA (`pipe.load_lora_weights("user/style-lora")`) on that quantized base at `weight_name="pytorch_lora_weights.safetensors"` still works. This is the recipe most SaaS agencies ship in 2026.

## Further Reading | 延伸阅读

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) — ControlNet.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) — LoRA (originally for LLMs; ports to diffusion).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) — IP-Adapter.
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) — lighter alternative to ControlNet.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) — DreamBooth.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) — reference pipelines.
