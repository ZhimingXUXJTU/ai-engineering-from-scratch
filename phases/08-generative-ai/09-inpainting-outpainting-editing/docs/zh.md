# 图像修复、扩展与编辑

> 文本生成图像创造新东西，图像修复（inpainting）修改已有的。生产中 70% 的付费图像工作是编辑——换背景、去 logo、扩展画布、重画手。Inpainting 是扩散模型真正赚钱的地方。

> **【中文解读】** 文本生成图像创造新东西，图像修复（inpainting）修改已有的。生产中 70% 的付费图像工作是编辑——换背景、去 logo、扩展画布、重画手。Inpainting 是扩散模型真正赚钱的地方。

> **【拓展：Photoshop 生成式填充】** Adobe Photoshop 的生成式填充（Generative Fill）就是基于 inpainting 技术。它让非专业用户也能一键移除/替换图像中的任何内容。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 07（潜在扩散）、阶段 8 · 08（ControlNet 与 LoRA）
**预计时间：** ~75 分钟

## 问题引入

客户发来一张完美的产品照片，背景中有一个分散注意力的招牌。你想要擦除招牌，其他一切保持像素级一致。你不能从零运行文本生成图像——结果会有不同的颜色、不同的光照、不同的产品角度。你想只重新生成*被遮蔽的区域*，并且重新生成要尊重周围上下文。

这就是 inpainting。变体包括：

- **Inpainting（图像修复）。** 在遮罩内重新生成，保持外部像素不变。
- **Outpainting（图像扩展）。** 在遮罩外（或画布外）重新生成，保持内部不变。
- **图像编辑。** 重新生成整个图像但保持与原始图像的语义或结构一致性（SDEdit、InstructPix2Pix）。

2026 年每个扩散流水线都提供 inpainting 模式。Flux.1-Fill、Stable Diffusion Inpaint、SDXL-Inpaint、DALL-E 3 Edit。它们都基于相同原理工作。

> **【中文解读】** Inpainting（图像修复）是生产环境中最常见的图像编辑需求。核心挑战：只重新生成被遮蔽的区域，同时保持与周围上下文的一致性。正确的做法是训练修改过的 U-Net，接受 9 通道输入（4 通道噪声潜在 + 4 通道编码图像 + 1 通道遮罩），让模型"看到"遮蔽区域周围的上下文。

> **【拓展：Photoshop 生成式填充与商业 Inpainting】** Adobe Photoshop 的生成式填充是 inpainting 技术的里程碑式应用。它结合了扩散模型和边缘融合技术，让用户可以通过自然语言指令移除/替换图像中的任何内容。类似的商业应用还包括 Canva 的 Magic Edit、Figma 的 AI 图像编辑等。

## 核心概念

![Inpainting：遮罩感知去噪与上下文保持重注入](../assets/inpainting.svg)

### 朴素方法（以及为什么它是错的）

用遮罩运行标准文本生成图像。在每个采样步，用前向扩散后的干净图像替换含噪潜在表示中未遮蔽的区域。它...效果很差。边界伪影渗透出来，因为模型没有关于遮蔽区域内容的信息。

### 正确的 Inpainting 模型

训练一个修改过的 U-Net，接受 9 个输入通道而非 4 个：

```
input = concat([ noisy_latent (4ch), encoded_image (4ch), mask (1ch) ], dim=channel)
```

额外通道是 VAE 编码的源图像副本加上一个单通道遮罩。训练时，随机遮蔽图像区域，训练模型只对遮蔽区域去噪，而未遮蔽区域作为干净的条件信号。推理时，模型可以"看到"遮蔽区域周围的内容，产生连贯的补全。

SD-Inpaint、SDXL-Inpaint、Flux-Fill 都使用这种 9 通道（或类似）输入。Diffusers 的 `StableDiffusionInpaintPipeline`、`FluxFillPipeline`。

### SDEdit (Meng et al., 2022) — 免费编辑

对源图像加噪声到某个中间时间步 `t`，然后用新提示从 `t` 反向运行到 0。无需重新训练。起始 `t` 的选择权衡保真度与创作自由度：

- `t/T = 0.3` → 与源图几乎相同，小的风格变化
- `t/T = 0.6` → 中等编辑，保留粗略结构
- `t/T = 0.9` → 从接近噪声开始生成，最小源图保留

### InstructPix2Pix (Brooks et al., 2023)

在 `(input_image, instruction, output_image)` 三元组上微调扩散模型。推理时，以输入图像和文本指令（"让它变成黄昏"、"加一条龙"）为条件。两个 CFG 缩放：图像缩放和文本缩放。

### RePaint (Lugmayr et al., 2022)

保持标准无条件扩散模型不变。在每个反向步，重采样——偶尔跳回到更嘈杂的状态并重新生成。避免边界伪影。当你没有训练好的 inpainting 模型时使用。

## 动手实现

`code/main.py` 在 5 维数据上实现了一个玩具 1 维 inpainting 方案。我们在 5 维混合数据上训练 DDPM，每个样本是来自两个聚类之一的 5 个浮点数。推理时，我们"遮蔽"5 个维度中的 2 个，在每步注入未遮蔽三个维度的含噪前向版本，只重新生成被遮蔽的维度。

### 步骤 1：5 维 DDPM 数据

```python
def sample_data(rng):
    cluster = rng.choice([0, 1])
    center = [-1.0] * 5 if cluster == 0 else [1.0] * 5
    return [c + rng.gauss(0, 0.2) for c in center], cluster
```

### 步骤 2：在所有 5 维上训练去噪器

标准 DDPM。网络对 5 维含噪输入输出 5 维噪声预测。

### 步骤 3：推理时，遮罩感知的反向过程

```python
def inpaint_step(x_t, mask, clean_image, alpha_bars, t, rng):
    # 用干净源图的新加噪版本替换未遮蔽维度
    a_bar = alpha_bars[t]
    for i in range(len(x_t)):
        if not mask[i]:
            x_t[i] = math.sqrt(a_bar) * clean_image[i] + math.sqrt(1 - a_bar) * rng.gauss(0, 1)
    # ...然后对 x_t 运行正常反向步骤
```

这是朴素方法，在玩具 1 维数据上有效。真实图像 inpainting 使用 9 通道输入，因为纹理一致性更重要。

### 步骤 4：Outpainting

Outpainting 就是反转遮罩的 inpainting：遮蔽新的（以前不存在的）画布，用原图填充其余部分。训练目标相同。

## 常见陷阱

- **接缝。** 朴素方法留下可见边界，因为梯度信息不流过遮罩。修复：将遮罩膨胀 8-16 像素，或使用正确的 inpainting 模型。
- **遮罩泄漏。** 如果条件图像的未遮蔽区域质量低或有噪声，它会污染遮罩内的生成。略微去噪或模糊。
- **CFG 与遮罩大小交互。** 小遮罩上的高 CFG = 饱和斑块。小型编辑降低 CFG。
- **SDEdit 保真度悬崖。** 从 `t/T = 0.5` 到 `t/T = 0.6` 可能失去主体身份。扫描并设置检查点。
- **提示不匹配。** 提示应该描述*整张*图像，而不仅是新内容。"一只猫坐在椅子上"而非"一只猫"。

## 用框架实现

| 任务 | 流水线 |
|------|----------|
| 移除物体，小遮罩 | SD-Inpaint 或 Flux-Fill，标准提示 |
| 替换天空 | SD-Inpaint + "日落时的蓝天" |
| 扩展画布 | SDXL outpaint 模式（8px 羽化）或带 outpaint 遮罩的 Flux-Fill |
| 重画手 / 脸 | SD-Inpaint + 重新描述主体的提示 + ControlNet-Openpose |
| 改变某区域风格 | SDEdit `t/T=0.5` 在遮蔽区域上 |
| "让它变成黄昏" | InstructPix2Pix 或 Flux-Kontext |
| 背景替换 | SAM 遮罩 → SD-Inpaint |
| 超高保真度 | Flux-Fill 或 GPT-Image（托管）用于最困难的情况 |

SAM（Meta 的 Segment Anything，2023）+ 扩散 inpaint 是 2026 年的背景移除流水线。SAM 2（2024）适用于视频。

## 产出物

保存 `outputs/skill-editing-pipeline.md`。技能接收原始图像 + 编辑描述 + 可选遮罩（或 SAM 提示），输出：遮罩生成方法、基础模型、CFG 缩放（图像 + 文本）、SDEdit-t 或 inpainting 模式，以及 QA 检查清单。

## 练习题

1. **简单。** 在 `code/main.py` 中，将遮蔽维度的比例从 0.2 变到 0.8。在什么比例下，inpaint 质量（遮蔽维度的残差）等于无条件生成？
2. **中等。** 实现 RePaint：每 10 个反向步，跳回 5 步（加噪声）并重新去噪。测量是否减少了遮罩边缘的边界残差。
3. **困难。** 使用 Hugging Face diffusers 比较：SD 1.5 Inpaint + ControlNet-Openpose vs Flux.1-Fill 在 20 个人脸重新生成任务上。分别对姿态遵循度和身份保持度评分。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| Inpainting | "填补空洞" | 在遮罩内重新生成；保持外部像素不变。 |
| Outpainting | "扩展画布" | 在画布外重新生成；保持内部不变。 |
| 9 通道 U-Net | "正确的 inpainting 模型" | 以 `noisy \| encoded-source \| mask` 为输入的 U-Net。 |
| SDEdit | "带噪声级别的 img2img" | 加噪到时间步 `t`，用新提示去噪。 |
| InstructPix2Pix | "纯文本编辑" | 在（图像、指令、输出）三元组上微调的扩散模型。 |
| RePaint | "无需重新训练" | 反向过程中定期重新加噪以减少接缝。 |
| SAM | "分割一切" | 通过点击或框选生成遮罩；与 inpaint 配合。 |
| Flux-Kontext | "带上下文编辑" | 接受参考图像 + 指令进行编辑的 Flux 变体。 |

## 生产笔记：编辑流水线对延迟敏感

编辑图像的用户期望 5 秒内的往返。30 步 SDXL-Inpaint 在 1024² 分辨率下单张 L4 上需要 3-4 秒，加上 SAM 遮罩生成（~200 ms）和 VAE 编码/解码（共 ~500 ms）。用生产术语来说，这是 TTFT 限制而非吞吐量限制——批大小为 1，低并发，优化每个阶段：

- **SAM-H 是慢的那个。** SAM-H 在 1024² 约 200 ms；SAM-ViT-B 约 40 ms，质量损失很小。SAM 2（视频）增加时间开销；不要用于单图像编辑。
- **可能时跳过编码。** `pipe.image_processor.preprocess(img)` 编码为潜在表示。如果你有上一次生成的潜在表示（在迭代编辑 UI 中典型），通过 `latents=...` 直接传入以跳过一次 VAE 编码。
- **遮罩膨胀也影响吞吐量。** 小遮罩意味着 U-Net 前向传播的大部分是浪费的（未遮蔽像素被夹住了）。`diffusers` 的 `StableDiffusionInpaintPipeline` 不管怎样都运行完整 U-Net；只有 9 通道的正确 inpaint 变体才利用遮罩化计算。
- **Flux-Kontext 是 2025 年的答案。** 对 `(source_image, instruction)` 的单次前向传播——无需单独遮罩，无需 SDEdit 噪声扫描。在 H100 上约 1.5 秒完成编辑。架构教训：合并阶段。

## 延伸阅读

- [Lugmayr et al. (2022). RePaint: Inpainting using Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2201.09865) — 免训练 inpainting。
- [Meng et al. (2022). SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073) — SDEdit。
- [Brooks, Holynski, Efros (2023). InstructPix2Pix](https://arxiv.org/abs/2211.09800) — 文本指令编辑。
- [Kirillov et al. (2023). Segment Anything](https://arxiv.org/abs/2304.02643) — SAM，遮罩来源。
- [Ravi et al. (2024). SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) — 视频 SAM。
- [Hertz et al. (2022). Prompt-to-Prompt Image Editing with Cross-Attention Control](https://arxiv.org/abs/2208.01626) — 注意力级编辑。
- [Black Forest Labs (2024). Flux.1-Fill and Flux.1-Kontext](https://blackforestlabs.ai/flux-1-tools/) — 2024 工具。
