# 自编码器与变分自编码器 (VAE)

> 普通自编码器先压缩再重建——它只是在记忆，不能生成。加一个技巧——强制编码服从高斯分布——你就得到了一个采样器。这个技巧就是重参数化 `z = mu + sigma * epsilon`，正是 2026 年你使用的每一个潜在扩散和流匹配图像模型在输入端都有一个 VAE 的原因。

> **【中文解读】** 普通自编码器压缩再重建，只是记忆，不能生成。加一个技巧——强制隐编码服从高斯分布——就得到了采样器。重参数化技巧 `z = mu + sigma * epsilon` 让梯度可以穿过采样操作，是 VAE 训练的关键。

> **【拓展：VAE 是 Stable Diffusion 的基石】** 2026 年所有潜在扩散模型（Stable Diffusion、FLUX）都在 VAE 的潜在空间中运行。VAE 编码器将图像压缩为低维表示，VAE 解码器将生成结果还原为图像。没有 VAE 就没有高效的图像生成。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 3 · 02（反向传播）、阶段 3 · 07（CNN）、阶段 8 · 01（分类）
**预计时间：** ~75 分钟

## 问题引入

将 784 像素的 MNIST 数字压缩到 16 维编码，然后重建。普通自编码器在重建 MSE 上表现出色，但编码空间是一团糟。在编码空间中随机取一个点，解码出来，得到的只是噪声。它没有采样器。它只是一个穿了马甲的压缩模型。

你真正想要的是：(a) 编码空间是一个干净、平滑、可以从中采样的分布——比如各向同性高斯 `N(0, I)`；(b) 解码任意样本都能产生合理的数字；(c) 编码器和解码器仍然能有效压缩。三个目标，一个架构，一个损失。

Kingma 2013 年的 VAE 通过训练编码器输出一个*分布* `q(z|x) = N(μ(x), σ(x)²)` 来解决这个问题，通过 KL 惩罚将该分布拉向先验 `N(0, I)`，然后从 `q(z|x)` 中采样 `z` 再解码。推理时，丢掉编码器，从 `N(0, I)` 采样 `z`，解码即可。KL 惩罚就是强制编码空间具有结构的原因。

2026 年，VAE 很少单独部署——在原始图像质量上已被扩散模型超越——但它们是每个潜在扩散模型（SD 1/2/XL/3、Flux、AudioCraft）的首选编码器。学会了 VAE，你就学会了你使用的每个图像流水线中看不见的第一层。

> **【中文解读】** VAE 的核心洞察：让编码器输出分布而非点估计。通过重参数化技巧 `z = mu + sigma * epsilon` 使采样可微，用 KL 散度约束编码空间接近标准正态分布。ELBO 损失 = 重建损失 + beta * KL 散度，两者相互权衡。推理时只需从标准正态采样并解码，一次前向传播即可生成。

> **【拓展：beta-VAE 与解耦表示学习】** beta-VAE（2017）通过调节 beta 参数控制重建与 KL 的权衡。beta<1 时重建更清晰但潜在空间不规整；beta>1 时潜在空间更规整但图像更模糊。当 beta 足够大时，VAE 可以学到"解耦"的表示——每个维度编码独立的语义因子（如颜色、形状、大小）。这启发了后续的扩散模型在潜在空间中做可控生成。

## 核心概念

![自编码器 vs VAE：重参数化技巧](../assets/vae.svg)

**自编码器。** `z = encoder(x)`，`x̂ = decoder(z)`，损失 = `||x - x̂||²`。编码空间无结构。

**VAE 编码器。** 输出两个向量：`μ(x)` 和 `log σ²(x)`。它们定义了 `q(z|x) = N(μ, diag(σ²))`。

**重参数化技巧。** 从 `q(z|x)` 采样不可微分。将样本重写为 `z = μ + σ·ε`，其中 `ε ~ N(0, I)`。现在 `z` 是 `(μ, σ)` 的确定性函数加上一个非参数噪声——梯度可以流过 `μ` 和 `σ`。

**损失。** 证据下界 (ELBO, Evidence Lower BOund)，两项：

```
loss = 重建损失 + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

重建损失将 `x̂` 推向 `x`。KL 将 `q(z|x)` 推向先验。两者相互权衡。小的 β（<1）= 更清晰的样本，编码空间不太高斯。大的 β（>1）= 更干净的编码空间，更模糊的样本。β-VAE（Higgins 2017）使这个旋钮出名，并开启了解耦表示学习的研究。

**采样。** 推理时：从 `N(0, I)` 抽取 `z`，送入解码器前向传播。一次前向传播——不像扩散模型那样需要迭代采样。

> **【中文解读】** ELBO 损失的两个组成部分各有分工：重建损失确保解码质量，KL 散度确保潜在空间的规整性。推理时完全不需要编码器——直接从 N(0,I) 采样 z 送入解码器。VAE 生成速度快（单次前向传播），但图像质量通常比扩散模型模糊，因为它优化的是 ELBO 下界而非精确似然。

> **【拓展：Stable Diffusion 中的 VAE】** Stable Diffusion 使用预训练的 VAE 将 512x512 图像压缩到 64x64 的潜在空间（8 倍下采样）。扩散过程在潜在空间中进行，大幅降低了计算量。SD 3 使用的 VAE 更先进——支持 16 通道潜在空间，图像质量更高。VAE 的压缩质量直接影响最终生成图像的细节保真度。

## 动手实现

`code/main.py` 实现了一个不依赖 numpy 或 torch 的微型 VAE。输入是从 8 维双分量高斯混合中抽取的合成数据。编码器和解码器都是单隐藏层的 MLP。我们实现了 tanh 激活、前向传播、损失函数和手写反向传播。不是生产代码——是为了教学。

### 步骤 1：编码器前向传播

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

使用 `log σ²` 而非 `σ`，这样网络输出不受约束（σ 的 softplus 是个陷阱——在 σ ≈ 0 时梯度会消失）。

### 步骤 2：重参数化与解码

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### 步骤 3：ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

因为两个分布都是高斯，KL 有精确的闭合形式解。不要数值积分。2026 年仍有人在代码中使用蒙特卡洛 KL 估计——慢了 3 倍且毫无意义。

### 步骤 4：生成

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

这就是生成模型。五行代码。

## 常见陷阱

- **后验坍塌 (Posterior collapse)。** KL 项将 `q(z|x) → N(0, I)` 推得过于激进，导致 `z` 不携带关于 `x` 的信息。修复：β 退火（从 β=0 开始，逐渐增加到 1）、free bits、或跳过不活跃维度的 KL。
- **样本模糊。** 高斯解码器似然意味着 MSE 重建，对 L2 来说贝叶斯最优的是均值——一组合理数字的均值是一个模糊的数字。修复：离散解码器（VQ-VAE、NVAE），或仅将 VAE 用作编码器，在潜在表示上叠加扩散模型（Stable Diffusion 就是这么做的）。
- **β 过大、过早。** 参见后验坍塌。从 β≈0.01 开始并逐渐增加。
- **潜在维度太小。** MNIST 用 16 维，ImageNet 256² 用 256 维，ImageNet 1024² 用 2048 维。Stable Diffusion 的 VAE 将 512×512×3 压缩为 64×64×4（空间面积压缩 32 倍，通道压缩 32 倍）。

## 用框架实现

2026 年的 VAE 技术栈：

| 场景 | 选择 |
|-----------|------|
| 扩散模型的图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) 或 Flux VAE |
| 音频潜在编码器 | Encodec (Meta)、SoundStream 或 DAC (Descript) |
| 视频潜在表示 | Sora 的时空 patch、Latte VAE、WAN VAE |
| 解耦表示学习 | β-VAE、FactorVAE、TCVAE |
| 离散潜在表示（用于 Transformer 建模） | VQ-VAE、RVQ (ResidualVQ) |
| 用于生成的连续潜在表示 | 普通 VAE，然后在潜在空间上搭建流/扩散模型 |

潜在扩散模型就是一个在编码器和解码器之间加入扩散模型的 VAE。VAE 做粗压缩，扩散模型做重活。同样的模式适用于视频（VAE + 视频扩散 DiT）和音频（Encodec + MusicGen Transformer）。

## 产出物

保存 `outputs/skill-vae-trainer.md`。

技能接收：数据集画像 + 目标潜在维度 + 下游用途（重建、采样或潜在扩散输入），输出：架构选择（普通/β/VQ/RVQ）、β 调度、潜在维度、解码器似然（高斯 vs 分类）、评估计划（重建 MSE、每维度 KL、`q(z|x)` 与 `N(0, I)` 之间的 Fréchet 距离）。

## 练习题

1. **简单。** 在 `code/main.py` 中将 `β` 改为 `0.01`、`0.1`、`1.0`、`5.0`。记录最终的重建 MSE 和 KL。哪个 β 对你的合成数据是帕累托最优的？
2. **中等。** 将高斯解码器似然替换为伯努利似然（交叉熵损失）。在二值化的相同合成数据上比较样本质量。
3. **困难。** 将 `code/main.py` 扩展为一个微型 VQ-VAE：用 K=32 个条目的码本中的最近邻查找替换连续的 `z`。比较重建 MSE，报告有多少码本条目被使用（码本坍塌是真实存在的）。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 自编码器 | 编码-解码网络 | `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | 带采样器的自编码器 | 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`；当 `q = p(z\|x)` 时取等。 |
| 重参数化 | `z = μ + σ·ε` | 将随机节点重写为确定性部分 + 纯噪声。使反向传播可以穿过采样操作。 |
| 先验 | `p(z)` | 潜在变量的目标分布，通常是 `N(0, I)`。 |
| 后验坍塌 | "KL 项赢了" | 编码器忽略 `x`，输出先验；解码器只能凭空想象。 |
| β-VAE | 可调 KL 权重 | `loss = recon + β·KL`。更高的 β = 更解耦但更模糊。 |
| VQ-VAE | 离散潜在表示 | 用最近码本向量替换连续 `z`；使 Transformer 建模成为可能。 |

## 生产笔记：VAE 是扩散服务器中最热的数据路径

在 Stable Diffusion / Flux / SD3 流水线中，VAE 每个请求被调用两次——一次用于编码（如果做 img2img / inpainting），一次用于解码。在 1024² 分辨率下，解码器的前向传播通常是整个流水线中最大的激活内存峰值，因为它需要将 `128×128×16` 的潜在表示上采样回 `1024×1024×3`。两个实际后果：

- **切片或分块解码。** `diffusers` 提供了 `pipe.vae.enable_slicing()` 和 `pipe.vae.enable_tiling()`。分块以微小的接缝瑕疵为代价，将内存从 `O(H·W)` 降至 `O(tile²)`。在 1024²+ 分辨率的消费级 GPU 上必不可少。
- **解码器用 bf16，最终调整用 fp32 精度。** SD 1.x VAE 以 fp32 发布，在 1024²+ 分辨率下转为 fp16 时*会静默产生 NaN*。SDXL 提供了 `madebyollin/sdxl-vae-fp16-fix`——始终优先使用 fp16 修复版本或使用 bf16。

## 延伸阅读

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) — VAE 论文。
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) — 解耦 β-VAE。
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) — VQ-VAE。
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) — 最先进的图像 VAE。
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — Stable Diffusion；VAE 作为编码器。
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) — Encodec，音频 VAE 标准。
