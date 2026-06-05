# GANs — Generator vs Discriminator | GAN — 生成器与判别器

> Goodfellow's trick in 2014 was to skip density entirely. Two networks. One makes fakes. One catches them. They fight until the fakes are indistinguishable from real. It shouldn't work. It often doesn't. When it does, the samples are still the sharpest in the literature for narrow domains.

> **【中文解读】** Goodfellow 2014 年的技巧是完全跳过密度估计。两个网络：一个造假，一个抓假，互相博弈直到假样本与真样本不可区分。理论上不该work，实践中常常不work，但一旦成功，在窄域生成上仍是文献中最锐利的结果。

> **【拓展：GAN 的遗产】** StyleGAN（人脸生成）、CycleGAN（风格迁移）、Pix2Pix（图像翻译）是 GAN 的经典应用。虽然扩散模型在 2022 年后成为主流，GAN 的对抗训练思想仍被用于提升其他模型质量。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## The Problem | 问题引入

VAEs produce blurry samples because their MSE decoder loss is Bayes-optimal for the *mean* image — and the mean of many plausible digits is a fuzzy digit. You want a loss that rewards *plausibility*, not pixel-wise proximity to any one target. There is no closed-form for plausibility. You have to learn it.

> VAE 产生模糊样本，因为 MSE 解码器损失对*均值*图像是贝叶斯最优的——而许多合理数字的均值是一个模糊的数字。你需要一个奖励*逼真度*的损失，而不是与任何目标的像素级接近度。逼真度没有闭式解，你必须学习它。

Goodfellow's idea: train a classifier `D(x)` to distinguish real images from fakes. Train a generator `G(z)` to fool `D`. The loss signal for `G` is whatever `D` currently thinks makes something look real. This signal updates as `G` improves, chasing a moving target. If both networks converge, `G` has learned the data distribution without ever writing down `log p(x)`.

> Goodfellow 的想法：训练一个分类器 `D(x)` 区分真假图像，训练一个生成器 `G(z)` 来欺骗 `D`。`G` 的损失信号是 `D` 当前认为"看起来真实"的东西。这个信号随着 `G` 的改进而更新——追逐一个移动目标。如果两个网络都收敛，`G` 就学会了数据分布，而不需要写出 `log p(x)`。

This is adversarial training. The math is a minimax game:

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

In 2026 GANs are no longer the SOTA generator (diffusion and flow matching ate that crown). But StyleGAN 2/3 remain the sharpest face models ever shipped, GAN discriminators are used as *perceptual losses* in diffusion training, and adversarial training powers the fast 1-step distillations (SDXL-Turbo, SD3-Turbo, LCM) that let you ship real-time diffusion.

> 2026 年 GAN 不再是最先进的生成器（扩散模型和 Flow Matching 夺走了桂冠）。但 StyleGAN 2/3 仍然是有史以来最锐利的人脸模型，GAN 判别器被用作扩散训练中的*感知损失*，对抗训练驱动着快速的 1 步蒸馏（SDXL-Turbo、SD3-Turbo、LCM）。

> **【中文解读】** GAN 的核心思想：不建模密度，通过对抗训练学习生成。生成器 G(z) 尝试生成逼真图像，判别器 D(x) 尝试区分真假。两者在 minimax 博弈中共同进化。VAE 的 MSE 损失导致模糊（因为它最优化的是均值图像），而 GAN 的对抗损失奖励"逼真度"。GAN 生成速度快（单次前向传播），但训练不稳定。

> **【拓展：GAN 在扩散模型蒸馏中的新角色】** 虽然 GAN 不再是主流生成方法，但对抗训练思想在扩散模型蒸馏中焕发新生。SDXL-Turbo、SD3-Turbo、LCM 等快速模型使用对抗损失将多步扩散蒸馏为 1-4 步，实现实时生成。GAN 的判别器作为可学习的"质量评估器"，比固定的感知损失更有效。

## The Concept | 核心概念

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.** Maps a noise vector `z ~ N(0, I)` to a sample `x̂`. A decoder-shaped network (dense or transposed conv).

> **生成器 `G(z)`。** 将噪声向量 `z ~ N(0, I)` 映射为样本 `x̂`。一个解码器形状的网络（全连接或转置卷积）。

**Discriminator `D(x)`.** Maps a sample to a scalar probability (or score). Real → 1, fake → 0.

> **判别器 `D(x)`。** 将样本映射为标量概率（或分数）。真实 → 1，伪造 → 0。

**Loss.** Two alternating updates:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`. Binary cross-entropy on real=1, fake=0.
- **Train `G`:** `loss_G = -log D(G(z))`. This is the *non-saturating* form Goodfellow used (original `log(1 - D(G(z)))` saturates and kills gradients when `D` is confident).

> **损失。** 两个交替更新：训练 D 用二元交叉熵（真实=1，伪造=0）；训练 G 用非饱和形式 `-log D(G(z))`（原始形式在 D 自信时梯度消失）。

**Training loop.** One step of `D`, one step of `G`. Repeat.

> **训练循环。** 一步 D，一步 G，交替进行。

**Why it works.** If `G` perfectly matches `p_data`, then `D` cannot do better than chance and outputs 0.5 everywhere; `G` gets no more gradient. Equilibrium.

> **为什么有效。** 如果 `G` 完美匹配 `p_data`，则 `D` 无法比随机猜测更好，处处输出 0.5；`G` 不再获得梯度。这就是均衡。

**Why it breaks.** Mode collapse (`G` finds one mode `D` can't classify and mints it forever), vanishing gradient (`D` learns too fast and `log D` saturates), training instability (learning rates, batch sizes, anything).

> **为什么会失败。** 模式坍塌（`G` 找到 `D` 无法分类的一种模式并永远生成它）、梯度消失（`D` 学得太快导致 `log D` 饱和）、训练不稳定（学习率、批大小等）。

## Variants that made GANs work | 使 GAN 成功的变体

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Build It | 动手实现

`code/main.py` trains a tiny GAN on 1-D data: a mixture of two Gaussians. Generator and discriminator are single-hidden-layer MLPs. We implement forward, backward, and the minimax loop by hand. The goal is to see the two key failure modes (mode collapse + vanishing gradient) as they happen.

> `code/main.py` 在一维数据上训练一个微型 GAN：双峰高斯混合。生成器和判别器是单隐层 MLP。我们手动实现前向、反向和 minimax 循环。目标是看到两种关键失败模式（模式坍塌 + 梯度消失）的发生过程。

### Step 1: non-saturating loss

The vanilla Goodfellow loss `log(1 - D(G(z)))` goes to 0 when D classifies G's fake as fake with high confidence. At that point the gradient for G is basically zero — G cannot improve. The non-saturating form `-log D(G(z))` has the opposite asymptote: it blows up when D is confident, giving G a strong signal.

> 原始 Goodfellow 损失 `log(1 - D(G(z)))` 在 D 高置信度地将 G 的伪造分类为假时趋近 0，此时 G 的梯度基本为零。非饱和形式 `-log D(G(z))` 有相反的渐近行为：在 D 自信时爆发，给 G 强信号。

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Step 2: one discriminator step per generator step

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

Fresh fakes for G, otherwise gradients are stale.

> 为 G 生成新的假样本，否则梯度过时。

### Step 3: watch for mode collapse

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

The canonical symptom: one of the two real modes stops being generated. The discriminator stops correcting it because it's never seen as a fake.

> 典型症状：两个真实模式之一不再被生成。判别器停止纠正它，因为它从未被看到作为伪造样本。

## Pitfalls | 常见陷阱

- **Discriminator too strong.** Cut D's learning rate by 2-5x, or add instance/layer noise. If D reaches >95% accuracy, G is dead.
  **判别器太强。** 将 D 的学习率降低 2-5 倍，或添加实例/层噪声。如果 D 准确率超过 95%，G 就死了。
- **Generator memorizes a mode.** Add noise to D inputs, use a minibatch-discriminator layer, or switch to WGAN-GP.
  **生成器记住了一种模式。** 给 D 输入添加噪声，使用小批量判别器层，或切换到 WGAN-GP。
- **Batch norm leaking statistics.** Real batch + fake batch flowing through the same BN layer mixes their statistics. Use instance norm or spectral norm instead.
  **批归一化泄漏统计量。** 真实批次和伪造批次通过同一 BN 层混合了统计量。改用实例归一化或谱归一化。
- **Inception-score gaming.** FID and IS are noisy at low sample counts. Use ≥10k samples at eval.
  **Inception Score 作弊。** FID 和 IS 在低样本量时噪声大。评估时使用 ≥10k 样本。
- **One-shot sampling is a lie for conditional tasks.** You still need CFG scales, truncation tricks, and re-sampling to get usable outputs.
  **条件任务中"单次采样"是个谎言。** 你仍然需要 CFG 缩放、截断技巧和重采样才能获得可用输出。

## Use It | 用框架实现

The 2026 GAN stack:

> 2026 年 GAN 技术栈：

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

GANs are sharp but narrow. Once your domain opens up — photos, arbitrary text prompts, video — switch to diffusion. The adversarial trick lives on as a component (perceptual losses, distillation), not a standalone generator.

> GAN 锐利但窄域。一旦领域开放——照片、任意文本提示、视频——就切换到扩散模型。对抗技巧作为组件存活（感知损失、蒸馏），而非独立生成器。

## Ship It | 产出物

Save `outputs/skill-gan-debugger.md`. Skill takes a failing GAN run (loss curves, sample grid, dataset size) and outputs a ranked list of likely causes, one-line fixes, and a rerun protocol.

> 保存 `outputs/skill-gan-debugger.md`。Skill 接收一个失败的 GAN 运行（损失曲线、样本网格、数据集大小），输出可能原因排序列表、一行修复和重跑方案。

## Exercises | 练习题

1. **Easy / 简单.** Run `code/main.py` with the stock settings. Then set `D_LR = 5 * G_LR` and rerun. How fast does G's loss collapse to a constant?
   用默认设置运行 `code/main.py`。然后设置 `D_LR = 5 * G_LR` 重跑。G 的损失多快坍塌为常数？
2. **Medium / 中等.** Replace the Goodfellow BCE loss with the WGAN loss: `loss_D = E[D(fake)] - E[D(real)]`, `loss_G = -E[D(fake)]`, and clip D's weights to `[-0.01, 0.01]`. Is training more stable? Compare wall-clock convergence.
   将 Goodfellow BCE 损失替换为 WGAN 损失，裁剪 D 的权重到 `[-0.01, 0.01]`。训练更稳定吗？比较墙钟收敛。
3. **Hard / 困难.** Extend the 1-D example to 2-D data (mixture of 8 Gaussians on a ring). Track how many of the 8 modes the generator captures at steps 1k, 5k, 10k. Implement minibatch discrimination and re-measure.
   将 1D 示例扩展到 2D 数据（环上 8 个高斯混合）。追踪生成器在 1k、5k、10k 步捕获了多少模式。实现小批量判别并重新测量。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Production note: one-shot inference is GAN's lasting advantage | 生产笔记：单次推理是 GAN 的持久优势

GANs no longer win on sample quality for open-domain generation, but they still win on inference cost. In production-inference literature vocabulary a GAN has:

> GAN 不再在开放域生成的样本质量上胜出，但在推理成本上仍然胜出。用生产推理术语来说：

- **No prefill, no decode stages.** A single `G(z)` forward pass. TTFT ≈ total latency.
  **无 prefill，无 decode 阶段。** 单次 `G(z)` 前向传播。TTFT ≈ 总延迟。
- **No KV-cache pressure.** The only state is the weights. Batch size is bounded by activation memory, not cache.
  **无 KV 缓存压力。** 唯一的状态是权重。批大小受限于激活内存而非缓存。
- **Trivial continuous batching.** Since every request takes the same fixed FLOPs, a static batch at the server's target occupancy is usually optimal. No in-flight scheduler needed.
  **简单的连续批处理。** 每个请求消耗相同 FLOPs，静态批量通常最优。

This is why GAN distillation (SDXL-Turbo, SD3-Turbo, ADD, LCM) is the dominant technique for fast text-to-image in 2026: it collapses a 20-50-step diffusion pipeline into 1-4 GAN-style forward passes while keeping the distribution of a diffusion base. The adversarial loss survives as a training-time knob for turning slow generators into fast ones.

> 这就是为什么 GAN 蒸馏（SDXL-Turbo、SD3-Turbo、LCM）是 2026 年快速文生图的主导技术：它将 20-50 步扩散流水线压缩为 1-4 次 GAN 风格的前向传播，同时保持扩散模型的分布。

## Further Reading | 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) — the original GAN paper.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434) — the first stable architecture.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) — WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) — SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) — StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) — StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042) — SDXL-Turbo.
