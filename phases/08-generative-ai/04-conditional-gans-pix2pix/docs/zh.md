# 条件 GAN 与 Pix2Pix

> 2014-2017 年的第一个重大突破是控制 GAN 生成什么。附加一个标签、一张图像或一句话。Pix2Pix 做了图像版本，至今在窄域图像翻译任务上仍胜过通用文本生成图像模型。

> **【中文解读】** 2014-2017 年的第一个重大突破是控制 GAN 生成什么：附加标签、图像或文本。Pix2Pix 做了图像版本，至今在窄域图像翻译任务上仍胜过通用文本生成图像模型。

> **【拓展：Pix2Pix 的应用】** Pix2Pix 开创了"图像到图像翻译"的范式：素描→照片、白天→夜晚、线稿→彩色图。这个范式后来被 ControlNet 继承和发展。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 03（GAN）、阶段 4 · 06（U-Net）、阶段 3 · 07（CNN）
**预计时间：** ~75 分钟

## 问题引入

无条件 GAN 采样出随机人脸。适合做演示，生产中无用。你想要：*将素描映射为照片*、*将地图映射为航拍照片*、*将白天场景映射为夜晚*、*将灰度图着色*。在所有这些场景中，你给定一张输入图像 `x`，必须输出与 `x` 有某种语义对应的 `y`。每个 `x` 对应许多合理的 `y`。均方误差将它们压成一团糊。对抗损失不会，因为"看起来像真的"是锐利的。

条件 GAN（Mirza & Osindero，2014）将条件 `c` 作为 `G` 和 `D` 的输入。Pix2Pix（Isola et al.，2017）专门化了这一点：条件是完整的输入图像，生成器是 U-Net，判别器是*基于图像块*的分类器 (PatchGAN)，损失是对抗损失 + L1。这个配方即使在 2026 年，在窄域图像到图像任务上也优于从零训练的文本生成图像模型，因为它是用*配对数据*训练的——你恰好有你需要的信号。

> **【中文解读】** 条件 GAN 的核心改进：给生成器和判别器都添加条件输入 c。Pix2Pix 的条件是完整输入图像，生成器用 U-Net（保留空间细节），判别器用 PatchGAN（对局部图像块分类）。损失 = 对抗损失 + L1 损失。这种配对数据训练方式在窄域图像翻译任务上至今仍优于通用文本生成图像模型。

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】** Pix2Pix 的"图像条件生成"思想被 ControlNet（2023）继承和发展。ControlNet 将条件控制（边缘、深度图、姿态等）注入预训练的 Stable Diffusion 模型，实现了更通用的可控生成。从 Pix2Pix 到 CycleGAN 再到 ControlNet，这是一条清晰的"可控生成"技术演进路径。

## 核心概念

![Pix2Pix：U-Net 生成器，PatchGAN 判别器](../assets/pix2pix.svg)

**条件 G。** `G(x, z) → y`。在 Pix2Pix 中，`z` 是 G 内部的 dropout（没有输入噪声——Isola 发现显式噪声被忽略了）。

**条件 D。** `D(x, y) → [0, 1]`。输入是*配对*（条件，输出）。这是关键区别：D 必须判断 `y` 是否与 `x` 一致，而不仅仅是 `y` 看起来是否真实。

**U-Net 生成器。** 带有跨瓶颈跳跃连接的编码器-解码器。对于输入和输出共享低层结构（边缘、轮廓）的任务至关重要。没有跳跃连接，高频细节会消失。

**PatchGAN 判别器。** D 不输出单个真/假分数，而是输出一个 `N×N` 网格，其中每个单元判断约 70×70 像素的感受野。取平均。这是一个马尔可夫随机场假设：真实性是局部的。训练更快，参数更少，输出更清晰。

**损失。**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

L1 项稳定训练并将 G 推向已知目标。L1 比 L2 给出更锐利的边缘（中位数 vs 均值）。`λ = 100` 是 Pix2Pix 的默认值。

## CycleGAN — 当你没有配对数据时

Pix2Pix 需要配对的 `(x, y)` 数据。CycleGAN（Zhu et al.，2017）通过额外的损失去掉这个要求：*循环一致性*损失。两个生成器 `G: X → Y` 和 `F: Y → X`。训练它们使得 `F(G(x)) ≈ x` 和 `G(F(y)) ≈ y`。这让你可以在没有配对样本的情况下将马翻译为斑马、夏天翻译为冬天。

2026 年，无配对图像到图像翻译主要通过扩散模型（ControlNet、IP-Adapter）而非 CycleGAN 完成，但循环一致性思想在几乎所有无配对域适应论文中仍然存活。

## 动手实现

`code/main.py` 在 1 维数据上实现了一个微型条件 GAN。条件 `c` 是类别标签（0 或 1）。任务是：为给定类别生成条件分布的样本。

### 步骤 1：将条件附加到 G 和 D 的输入

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

独热编码是最简单的方式。更大的模型使用学习到的嵌入、FiLM 调制或交叉注意力。

### 步骤 2：条件训练

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

生成器必须匹配*给定条件下*的真实分布，而非边缘分布。

### 步骤 3：验证逐类输出

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## 常见陷阱

- **条件被忽略。** G 学会了边缘化，D 从不惩罚因为条件信号太弱。修复：更激进地条件化 D（早期层，不仅仅是后期层），使用投影判别器 (Miyato & Koyama 2018)。
- **L1 权重太低。** G 漂移到任意的看起来真实的输出，而非忠实的输出。Pix2Pix 风格任务从 λ≈100 开始。
- **L1 权重太高。** G 产生模糊输出，因为 L1 仍然是 L_p 范数。训练稳定后逐渐降低。
- **D 中的真值泄漏。** 将 `(x, y)` 拼接为 D 的输入，而非仅仅是 `y`。没有这个 D 无法检查一致性。
- **每个类别的模式坍塌。** 每个类别可能独立坍塌。运行类别条件多样性检查。

## 用框架实现

2026 年图像到图像任务的最佳实践：

| 任务 | 最佳方案 |
|------|---------------|
| 素描 → 照片，同域，配对数据 | Pix2Pix / Pix2PixHD（仍然快速、仍然清晰） |
| 素描 → 照片，无配对 | ControlNet + 涂鸦条件模型 |
| 语义分割 → 照片 | SPADE / GauGAN2 或 SD + ControlNet-Seg |
| 风格迁移 | 使用 IP-Adapter 或 LoRA 的扩散模型；GAN 方法已是遗留 |
| 深度图 → 照片 | Stable Diffusion 上的 ControlNet-Depth |
| 超分辨率 | Real-ESRGAN (GAN)、ESRGAN-Plus 或 SD-Upscale（扩散） |
| 着色 | ColTran、基于扩散的着色器或 Pix2Pix-color |
| 白天 → 夜晚、季节、天气 | CycleGAN 或基于 ControlNet |

当你 (a) 有数千个配对样本、(b) 任务窄且可重复、(c) 需要快速推理时，Pix2Pix 仍然是正确的工具。在通用开放式任务上，扩散模型胜出。

## 产出物

保存 `outputs/skill-img2img-chooser.md`。技能接收任务描述、数据可用性（配对 vs 非配对、样本数 N）、延迟/质量预算，输出：方案（Pix2Pix、CycleGAN、ControlNet 变体、SDXL + IP-Adapter）、训练数据需求、推理成本和评估协议（LPIPS、FID、任务特定指标）。

## 练习题

1. **简单。** 修改 `code/main.py` 添加第三个类别。确认 G 仍然将每个类别的噪声映射到正确的模式。
2. **中等。** 在 1 维设置中用感知风格损失替换 L1（例如一个冻结的小型 D 作为特征提取器）。是否改变了条件分布的清晰度？
3. **困难。** 在 1 维设置中草拟一个 CycleGAN：两个分布、两个生成器、循环损失。证明它可以在无配对数据的情况下学会在两个分布之间映射。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 条件 GAN | "带标签的 GAN" | G(z, c), D(x, c)。两个网络都看到条件。 |
| Pix2Pix | "图像到图像 GAN" | 配对 cGAN，U-Net G 和 PatchGAN D + L1 损失。 |
| U-Net | "带跳跃连接的编码-解码器" | 对称卷积网络；跳跃连接保留高频信息。 |
| PatchGAN | "局部真实性分类器" | D 输出逐块分数而非全局分数。 |
| CycleGAN | "无配对图像翻译" | 两个 G + 循环一致性损失；无需配对数据。 |
| SPADE | "GauGAN" | 用语义图归一化中间激活；分割到图像。 |
| FiLM | "特征级线性调制" | 来自条件的逐特征仿射变换；低成本条件化。 |

## 生产笔记：Pix2Pix 作为延迟下限的基线

当你有配对数据和一个窄任务（素描 → 渲染、语义图 → 照片、白天 → 夜晚）时，Pix2Pix 的一步推理在延迟上比扩散快一个数量级。生产对比通常是：

| 路径 | 步数 | 单张 L4 上 512² 的典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix（U-Net 前向） | 1 | ~30 ms |
| SD-Inpaint 或 SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix 在静态批次中赢得吞吐量（每个请求消耗相同 FLOPs）。扩散模型在质量和泛化上获胜。现代策略通常是为窄任务部署 Pix2Pix 风格的蒸馏模型，为尾部输入使用扩散回退。

## 延伸阅读

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) — cGAN 论文。
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004) — Pix2Pix。
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) — CycleGAN。
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) — Pix2PixHD。
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291) — SPADE / GauGAN。
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) — 投影 D。
