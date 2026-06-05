# StyleGAN | StyleGAN — 风格生成对抗网络

> Most generators stir `z` into every layer at the same time. StyleGAN split it apart: first map `z` to an intermediate `w`, then *inject* `w` at every resolution level through AdaIN. That single change untangled the latent space and made photorealistic faces a solved problem for seven years running.

> **【中文解读】** StyleGAN 将隐变量 z 先映射到中间空间 w，再通过 AdaIN 在每个分辨率层级注入 w，实现了对生成图像不同层面（粗粒度/细粒度特征）的独立控制。这一改变解开了隐空间，使逼真人脸生成成为已解决的问题长达七年。

> **【拓展：StyleGAN 的应用】** StyleGAN 广泛用于人脸生成（thispersondoesnotexist.com）、虚拟人物创建、艺术创作。其 Style Mixing 技术可以混合不同人脸的粗细特征。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## The Problem | 问题引入

A DCGAN maps `z` to an image through a stack of transposed convolutions. The problem: `z` controls everything — pose, lighting, identity, background — entangled together. Move along one axis of `z`, all four change. You cannot ask the model "same person, different pose" because the representation does not factor that way.

> DCGAN 通过转置卷积堆栈将 `z` 映射为图像。问题是：`z` 控制一切——姿态、光照、身份、背景——纠缠在一起。沿 `z` 的一个轴移动，四个都变。你无法要求模型"同一个人，不同姿态"，因为表示没有这样分解。

Karras et al. (2019, NVIDIA) proposed: stop feeding `z` directly into conv layers. Feed a constant `4×4×512` tensor as the network input. Learn an 8-layer MLP that maps `z ∈ Z → w ∈ W`. Inject `w` at every resolution via *adaptive instance normalization* (AdaIN): normalize each conv feature map, then scale and shift by affine projections of `w`. Add per-layer noise for stochastic detail (skin pores, hair strands).

> Karras 等人（2019，NVIDIA）提出：停止将 `z` 直接送入卷积层。用一个常数 `4×4×512` 张量作为网络输入。学习一个 8 层 MLP 将 `z ∈ Z → w ∈ W`。通过*自适应实例归一化*（AdaIN）在每个分辨率注入 `w`。添加每层随机噪声用于随机细节（毛孔、发丝）。

The result: `W` has roughly orthogonal axes for "high-level style" (pose, identity) vs "fine style" (lighting, color). You can swap styles between two images by using image A's `w` for the low-resolution levels and image B's `w` for the high. This unlocked editing, cross-domain stylization, and the entire "StyleGAN-inversion" line of research.

> 结果：`W` 空间对"高级风格"（姿态、身份）和"精细风格"（光照、颜色）有大致正交的轴。你可以通过用图像 A 的 `w` 用于低分辨率层、图像 B 的 `w` 用于高分辨率层来交换风格。这解锁了编辑、跨域风格化和整个"StyleGAN 反演"研究方向。

> **【中文解读】** StyleGAN 的关键创新：(1) 映射网络 z→w 解开纠缠的隐空间；(2) AdaIN 在每个分辨率层级注入风格——低分辨率层控制粗粒度（姿势、身份），高分辨率层控制细粒度（颜色、纹理）；(3) 每层随机噪声添加细节（毛孔、发丝）。Style Mixing 技术可以混合不同图像的粗细特征。

> **【拓展：StyleGAN 3 的平移等变性】** StyleGAN 2 生成的图像有"纹理粘附"问题——特征（如头发）会"粘"在特定像素位置而非物体表面。StyleGAN 3（2021）通过连续的信号处理解决了这个问题，使生成结果对平移和旋转具有等变性。这对视频生成和 3D 应用尤为重要。

## The Concept | 核心概念

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, an 8-layer MLP. `Z = N(0, I)^512`. `W` is not forced to be Gaussian — it learns a data-adapted shape.

> **映射网络。** `f: Z → W`，8 层 MLP。`W` 不被强制为高斯——它学习数据适应的形状。

**Synthesis network.** Starts from a learned constant `4×4×512`. Each resolution block: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`. Resolutions double: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。** 从学习到的常数 `4×4×512` 开始。每个分辨率块：上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声。分辨率翻倍：4 到 1024。

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

where `y_scale` and `y_bias` come from affine projections of `w`. Normalize per feature map, then restyle. "Style" here is the first- and second-order statistics of the feature map.

> 其中 `y_scale` 和 `y_bias` 来自 `w` 的仿射投影。逐特征图归一化，然后重新施加风格。"风格"即特征图的一阶和二阶统计量。

**Per-layer noise.** Single-channel Gaussian noise added to each feature map, scaled by a learned per-channel factor. Controls stochastic detail without affecting global structure.

> **每层噪声。** 单通道高斯噪声添加到每个特征图，由可学习的逐通道因子缩放。控制随机细节而不影响全局结构。

**Truncation trick.** At inference, sample `z`, compute `w = mapping(z)`, then `w' = ŵ + ψ·(w - ŵ)` where `ŵ` is the mean `w` over many samples. `ψ < 1` trades diversity for quality. Almost every StyleGAN demo uses `ψ ≈ 0.7`.

> **截断技巧。** 推理时，`w' = ŵ + ψ·(w - ŵ)`，其中 `ŵ` 是 `w` 在多个样本上的均值。`ψ < 1` 以多样性换质量。几乎所有 StyleGAN 演示都用 `ψ ≈ 0.7`。

## StyleGAN 1 → 2 → 3 | StyleGAN 版本演进

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

In 2026 StyleGAN3 remains the default for (a) narrow-domain photorealism at high FPS, (b) few-shot domain adaptation (train on a new dataset with 100 images, freeze mapping), (c) inversion-based editing (find the `w` that reconstructs a real photo, then edit that `w`). For open-domain text-to-image, it is not the tool — diffusion is.

> 2026 年 StyleGAN3 仍是以下场景的默认选择：(a) 高 FPS 窄域照片级真实感，(b) 少样本域适应，(c) 基于反演的编辑。开放域文生图则不是它的工具——扩散模型才是。

## Build It | 动手实现

`code/main.py` implements a toy "style-GAN lite" in 1-D: a mapping MLP, a synthesis function that takes a learned constant vector and modulates it with `w`-derived scale/bias, and per-layer noise. It shows that injecting `w` via affine-modulation matches or beats concatenating `z` into the generator's input.

> `code/main.py` 在 1D 中实现了一个"StyleGAN lite"：映射 MLP、合成函数和每层噪声。它展示了通过仿射调制注入 `w` 与将 `z` 拼接到输入相比效果相当或更好。

### Step 1: mapping network

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Step 2: adaptive instance normalization

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

Per-feature-map scale and bias come from `w` via linear projection.

> 逐特征图的缩放和偏置来自 `w` 的线性投影。

### Step 3: per-layer noise

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma per-channel is learnable.

> 每通道的 sigma 是可学习的。

## Pitfalls | 常见陷阱

- **Droplet artifacts.** StyleGAN 1 produced a blobby droplet in the feature maps because AdaIN zeroed out mean. StyleGAN 2's weight demodulation fixes it by scaling the convolution weights instead.
  **液滴伪影。** StyleGAN 1 因 AdaIN 归零均值产生液滴。StyleGAN 2 的权重解调通过缩放卷积权重修复。
- **Texture sticking.** StyleGAN 1 and 2 textures followed pixel coordinates, not object coordinates (visible when interpolating). StyleGAN 3's alias-free convolutions fix this with windowed sinc filters.
  **纹理粘附。** StyleGAN 1/2 的纹理跟随像素坐标而非物体坐标。StyleGAN 3 的无混叠卷积用窗口 sinc 滤波器修复。
- **Mode coverage.** Truncation `ψ < 0.7` looks clean but samples from a narrow cone; use `ψ = 1.0` if you need diversity.
  **模式覆盖。** 截断 `ψ < 0.7` 看起来干净但从窄锥采样；需要多样性时用 `ψ = 1.0`。
- **Inversion is lossy.** Inverting a real photo into `W` is usually done through optimization or an encoder (e4e, ReStyle, HyperStyle). Results drift over many iterations.
  **反演有损。** 将真实照片反演到 `W` 通常通过优化或编码器完成，结果在多次迭代后会漂移。

## Use It | 用框架实现

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

For product-grade demos where the answer is "photo of a person's face", StyleGAN beats diffusion on inference cost (single forward pass, <10ms on a 4090) and sharpness for the same quality bar.

> 对于"人物面部照片"级别的产品演示，StyleGAN 在推理成本（单次前向传播，4090 上 <10ms）和同等质量下的锐度上胜过扩散模型。

## Ship It | 产出物

Save `outputs/skill-stylegan-inversion.md`. Skill takes a real photo and outputs: inversion method (e4e / ReStyle / HyperStyle), expected latent loss, editing budget (how far in `W` you can move before artifacts), and a list of known-good editing directions (age, expression, pose).

> 保存 `outputs/skill-stylegan-inversion.md`。Skill 接收真实照片，输出反演方法、预期潜在损失、编辑预算和已知编辑方向。

## Exercises | 练习题

1. **Easy / 简单.** Run `code/main.py` with `adain_on=True` and `adain_on=False`. Compare the spread of outputs for a fixed latent vs perturbed latent.
   分别用 `adain_on=True` 和 `adain_on=False` 运行。比较固定隐变量和扰动隐变量的输出分布。
2. **Medium / 中等.** Implement mixing regularization: for a training batch, compute `w_a`, `w_b`, and apply `w_a` for the first half of synthesis and `w_b` for the second half. Does the decoder learn disentangled styles?
   实现混合正则化。解码器是否学到了解耦的风格？
3. **Hard / 困难.** Take a pretrained StyleGAN3 FFHQ model (ffhq-1024.pkl). Find the `w` direction that controls "smile" by training an SVM on labelled samples; report how far you can push before identity drifts.
   使用预训练 StyleGAN3 FFHQ 模型，通过 SVM 找到控制"微笑"的 `w` 方向。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Production note: why StyleGAN still ships in 2026 | 生产笔记：为什么 StyleGAN 在 2026 年仍然出货

StyleGAN3 on a 4090 generates a 1024² FFHQ face in under 10 ms — `num_steps = 1`, no VAE decode, no cross-attention pass. In production terms this is the floor latency for any image generator. A 50-step SDXL + VAE-decode pipeline at the same resolution is ~3 seconds. That is a **300× gap**, and for narrow-domain products (avatar services, ID document pipelines, stock face generation) it wins on TCO.

> StyleGAN3 在 4090 上不到 10ms 生成 1024² 人脸——`num_steps = 1`，无 VAE 解码，无交叉注意力。50 步 SDXL 在同分辨率约 3 秒。这是 **300 倍差距**，在窄域产品上 TCO 获胜。

Two operational consequences:

> 两个运营后果：

- **No scheduler, no batcher.** Static batch at the target occupancy is optimal. Continuous batching (essential for LLMs and diffusion) provides zero benefit because every request takes the same FLOPs.
  **无需调度器或批处理器。** 静态批量最优。连续批处理（对 LLM 和扩散模型至关重要）零收益。
- **Truncation `ψ` is the safety knob.** `ψ < 0.7` samples from a narrow cone of the mapping network's range. This is the only lever the serving layer has over sample variance. Lower `ψ` at peak load, raise it for premium users.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7` 从映射网络范围的窄锥采样。这是服务层控制样本方差的唯一杠杆。高峰负载时降低 `ψ`，高级用户时提高。

## Further Reading | 延伸阅读

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) — StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) — StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) — StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) — e4e inversion.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273) — StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) — modern minimal GAN recipe.
