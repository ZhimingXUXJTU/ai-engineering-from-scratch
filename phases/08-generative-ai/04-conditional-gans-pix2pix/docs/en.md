# Conditional GANs & Pix2Pix | 条件 GAN 与 Pix2Pix

> The first big unlock of 2014-2017 was controlling what a GAN makes. Attach a label, or an image, or a sentence. Pix2Pix did the image version and it still beats every generic text-to-image model on narrow image-to-image tasks.

> **【中文解读】** 2014-2017 年的第一个重大突破是控制 GAN 生成什么：附加标签、图像或文本。Pix2Pix 做了图像版本，至今在窄域图像翻译任务上仍胜过通用文本生成图像模型。

> **【拓展：Pix2Pix 的应用】** Pix2Pix 开创了"图像到图像翻译"的范式：素描→照片、白天→夜晚、线稿→彩色图。这个范式后来被 ControlNet 继承和发展。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## The Problem | 问题引入

An unconditional GAN samples arbitrary faces. Useful for a demo, useless in production. You want: *map a sketch to a photo*, *map a map to an aerial photo*, *map a daytime scene to nighttime*, *colorize a grayscale image*. In all of these, you are given an input image `x` and must output `y` with some semantic correspondence. There are many plausible `y`s per `x`. Mean-squared error flattens them into mush. An adversarial loss doesn't, because "looks real" is sharp.

> 无条件 GAN 采样任意人脸。适合演示，不适合生产。你想要的是：*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜晚*、*给灰度图上色*。在所有这些场景中，给定输入图像 `x`，必须输出具有语义对应关系的 `y`。每个 `x` 有多种合理的 `y`。均方误差将它们压成一团糊，而对抗损失不会，因为"看起来真实"是锐利的。

Conditional GAN (Mirza & Osindero, 2014) adds a condition `c` as an input to both `G` and `D`. Pix2Pix (Isola et al., 2017) specialized this: condition is a full input image, generator is a U-Net, discriminator is a *patch-based* classifier (PatchGAN), and loss is adversarial + L1. That recipe outperforms from-scratch text-to-image models on narrow image-to-image domains even in 2026 because it is trained on *paired data* — you have exactly the signal you need.

> 条件 GAN（2014）在 `G` 和 `D` 的输入中添加条件 `c`。Pix2Pix（2017）专门化了这个：条件是完整输入图像，生成器是 U-Net，判别器是 PatchGAN，损失 = 对抗 + L1。这个方案在窄域图像翻译任务上甚至 2026 年仍优于从头训练的文生图模型，因为它在*配对数据*上训练——你恰好有所需的信号。

> **【中文解读】** 条件 GAN 的核心改进：给生成器和判别器都添加条件输入 c。Pix2Pix 的条件是完整输入图像，生成器用 U-Net（保留空间细节），判别器用 PatchGAN（对局部图像块分类）。损失 = 对抗损失 + L1 损失。这种配对数据训练方式在窄域图像翻译任务上至今仍优于通用文本生成图像模型。

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】** Pix2Pix 的"图像条件生成"思想被 ControlNet（2023）继承和发展。ControlNet 将条件控制（边缘、深度图、姿态等）注入预训练的 Stable Diffusion 模型，实现了更通用的可控生成。从 Pix2Pix 到 CycleGAN 再到 ControlNet，这是一条清晰的"可控生成"技术演进路径。

## The Concept | 核心概念

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`. In Pix2Pix, `z` is dropout inside G (no input noise — Isola found explicit noise got ignored).

> **条件生成器 G。** `G(x, z) → y`。在 Pix2Pix 中，`z` 是 G 内部的 dropout（无输入噪声——Isola 发现显式噪声会被忽略）。

**Conditional D.** `D(x, y) → [0, 1]`. Input is the *pair* (condition, output). This is the key difference: D must judge whether `y` is consistent with `x`, not just whether `y` looks real.

> **条件判别器 D。** `D(x, y) → [0, 1]`。输入是*配对*（条件，输出）。关键区别：D 必须判断 `y` 是否与 `x` 一致，而不仅仅是 `y` 是否看起来真实。

**U-Net generator.** Encoder-decoder with skip connections across the bottleneck. Critical for tasks where input and output share low-level structure (edges, silhouette). Without the skips, high-frequency detail vanishes.

> **U-Net 生成器。** 带有跳跃连接的编码器-解码器。对于输入输出共享低级结构（边缘、轮廓）的任务至关重要。没有跳跃连接，高频细节会消失。

**PatchGAN discriminator.** Instead of outputting a single real/fake score, D outputs an `N×N` grid where each cell judges a receptive field of ~70×70 pixels. Averaged. This is a Markov random field assumption: realism is local. Much faster to train, fewer parameters, sharper output.

> **PatchGAN 判别器。** D 输出 `N×N` 网格而非单一真/假分数，每个单元判断约 70×70 像素的感受野。这是马尔可夫随机场假设：真实感是局部的。训练更快，参数更少，输出更锐利。

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

The L1 term stabilizes training and pushes G toward the known target. L1 gives sharper edges than L2 (medians, not means). `λ = 100` was the Pix2Pix default.

> L1 项稳定训练并推动 G 趋向已知目标。L1 比 L2 产生更锐利的边缘（中位数 vs 均值）。`λ = 100` 是 Pix2Pix 的默认值。

## CycleGAN — when you don't have pairs | CycleGAN — 没有配对数据时

Pix2Pix needs paired `(x, y)` data. CycleGAN (Zhu et al., 2017) drops this requirement at the cost of an extra loss: the *cycle consistency* loss. Two generators `G: X → Y` and `F: Y → X`. Train them so `F(G(x)) ≈ x` and `G(F(y)) ≈ y`. This lets you translate horses to zebras, summer to winter, without paired examples.

> Pix2Pix 需要配对 `(x, y)` 数据。CycleGAN（2017）放弃了这个要求，代价是额外的循环一致性损失。两个生成器 `G: X → Y` 和 `F: Y → X`，训练使 `F(G(x)) ≈ x` 和 `G(F(y)) ≈ y`。这让你无需配对样本就能将马变成斑马、夏天变成冬天。

In 2026, unpaired image-to-image is mostly done via diffusion (ControlNet, IP-Adapter) rather than CycleGAN, but the cycle-consistency idea survives in almost every unpaired domain adaptation paper.

> 2026 年，非配对图像翻译主要通过扩散模型（ControlNet、IP-Adapter）而非 CycleGAN 完成，但循环一致性思想几乎存在于每篇非配对域适应论文中。

## Build It | 动手实现

`code/main.py` implements a tiny conditional GAN on 1-D data. The condition `c` is a class label (0 or 1). The task: produce a sample from the conditional distribution for the given class.

> `code/main.py` 在一维数据上实现一个微型条件 GAN。条件 `c` 是类别标签（0 或 1）。任务：为给定类别从条件分布中生成样本。

### Step 1: append condition to both G and D inputs

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

One-hot encoding is the simplest way. Larger models use learned embeddings, FiLM modulation, or cross-attention.

> One-hot 编码是最简单的方式。更大的模型使用学习嵌入、FiLM 调制或交叉注意力。

### Step 2: train conditional

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

The generator must match the real distribution *for the given condition*, not the marginal.

> 生成器必须匹配*给定条件*下的真实分布，而非边际分布。

### Step 3: verify per-class output

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## Pitfalls | 常见陷阱

- **Condition ignored.** G learns to marginalize, D never penalizes because condition signal is weak. Fix: condition D more aggressively (early layer, not just late), use projection discriminator (Miyato & Koyama 2018).
  **条件被忽略。** G 学会了边缘化，D 从不惩罚因为条件信号弱。修复：更积极地条件化 D，使用投影判别器。
- **L1 weight too low.** G drifts to arbitrary real-looking outputs, not faithful ones. Start λ≈100 for Pix2Pix-style tasks.
  **L1 权重太低。** G 偏移到任意看起来真实的输出。Pix2Pix 任务从 λ≈100 开始。
- **L1 weight too high.** G produces blurry outputs because L1 is still an L_p norm. Anneal down once training stabilizes.
  **L1 权重太高。** G 产生模糊输出。训练稳定后逐渐降低。
- **Ground-truth leakage in D.** Concatenate `(x, y)` as D input, not just `y`. Without this D cannot check consistency.
  **D 中的真值泄漏。** 将 `(x, y)` 拼接为 D 的输入，而非仅 `y`。
- **Mode collapse per class.** Each class can collapse independently. Run class-conditional diversity checks.
  **每类模式坍塌。** 每个类别可能独立坍塌。运行类别条件多样性检查。

## Use It | 用框架实现

2026 state of image-to-image tasks:

> 2026 年图像到图像任务的状态：

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix remains the right tool when (a) you have thousands of paired examples, (b) the task is narrow and repeatable, and (c) you need fast inference. On generic open-domain tasks, diffusion wins.

> Pix2Pix 在以下情况仍是正确工具：(a) 有数千配对样本，(b) 任务窄且可重复，(c) 需要快速推理。通用开放域任务，扩散模型胜出。

## Ship It | 产出物

Save `outputs/skill-img2img-chooser.md`. Skill takes a task description, data availability (paired vs unpaired, N samples), and latency/quality budget, then outputs: approach (Pix2Pix, CycleGAN, ControlNet variant, SDXL + IP-Adapter), training data requirements, inference cost, and eval protocol (LPIPS, FID, task-specific).

> 保存 `outputs/skill-img2img-chooser.md`。Skill 接收任务描述、数据可用性和延迟/质量预算，输出方案、训练数据需求、推理成本和评估协议。

## Exercises | 练习题

1. **Easy / 简单.** Modify `code/main.py` to add a third class. Confirm G still maps each class's noise to the correct mode.
   修改 `code/main.py` 添加第三个类别。确认 G 仍将每个类的噪声映射到正确的模式。
2. **Medium / 中等.** Replace L1 with a perceptual-style loss in the 1-D setting (e.g. a small frozen D acting as feature extractor). Does it change sharpness of the conditional distribution?
   在 1D 设置中用感知损失替换 L1。它改变了条件分布的锐度吗？
3. **Hard / 困难.** Sketch a CycleGAN in the 1-D setting: two distributions, two generators, cycle loss. Show that it learns to map between them with no paired data.
   在 1D 设置中勾画 CycleGAN：两个分布、两个生成器、循环损失。证明它无需配对数据就能学习映射。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Production note: Pix2Pix as a latency-bound baseline | 生产笔记：Pix2Pix 作为延迟基线

When you have paired data and a narrow task (sketch → render, semantic map → photo, day → night), Pix2Pix's one-shot inference beats diffusion by an order of magnitude on latency. The production comparison is usually:

> 当你有配对数据和窄域任务时，Pix2Pix 的单次推理在延迟上比扩散模型快一个数量级。生产对比通常是：

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix wins on throughput in static batches (every request is the same FLOPs). Diffusion wins on quality and generalization. The modern play is often to ship a Pix2Pix-style distilled model for the narrow task and a diffusion fallback for tail inputs.

> Pix2Pix 在静态批量吞吐量上胜出（每个请求 FLOPs 相同）。扩散模型在质量和泛化上胜出。现代做法通常是为窄域任务部署 Pix2Pix 风格蒸馏模型，为尾部输入提供扩散回退。

## Further Reading | 延伸阅读

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) — the cGAN paper.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004) — Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) — CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) — Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291) — SPADE / GauGAN.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) — the projection D.
