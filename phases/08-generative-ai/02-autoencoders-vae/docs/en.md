# Autoencoders & Variational Autoencoders (VAE) | 自编码器与变分自编码器

> A plain autoencoder compresses then reconstructs. It memorizes. It does not generate. Add one trick — force the code to look Gaussian — and you get a sampler. That single trick, the reparameterization of `z = mu + sigma * epsilon`, is why every latent-diffusion and flow-matching image model you use in 2026 has a VAE at the input.

> **【中文解读】** 普通自编码器压缩再重建，只是记忆，不能生成。加一个技巧——强制隐编码服从高斯分布——就得到了采样器。重参数化技巧 `z = mu + sigma * epsilon` 让梯度可以穿过采样操作，是 VAE 训练的关键。

> **【拓展：VAE 是 Stable Diffusion 的基石】** 2026 年所有潜在扩散模型（Stable Diffusion、FLUX）都在 VAE 的潜在空间中运行。VAE 编码器将图像压缩为低维表示，VAE 解码器将生成结果还原为图像。没有 VAE 就没有高效的图像生成。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## The Problem | 问题引入

Compress a 784-pixel MNIST digit to a 16-number code, then reconstruct. A plain autoencoder will ace reconstruction MSE but the code space is a lumpy mess. Pick a random point in the code space, decode it, and you get noise. It has no sampler. It is a compression model dressed up.

> 将 784 像素的 MNIST 数字压缩为 16 个数字的编码再重建。普通自编码器能获得很好的重建 MSE，但编码空间一团糟。在编码空间中随机取点解码得到的是噪声。它没有采样器，只是伪装的压缩模型。

What you actually want is: (a) the code space is a clean, smooth distribution you can sample from — say an isotropic Gaussian `N(0, I)`, (b) decoding any sample produces a plausible digit, and (c) the encoder and decoder still compress well. Three goals, one architecture, one loss.

> 你真正想要的是：(a) 编码空间是干净、平滑、可采样的分布——比如各向同性高斯 `N(0, I)`；(b) 解码任何样本都产生合理的数字；(c) 编码器和解码器仍然压缩良好。三个目标，一个架构，一个损失。

Kingma's 2013 VAE solves this by training the encoder to output a *distribution* `q(z|x) = N(μ(x), σ(x)²)`, pulling that distribution toward the prior `N(0, I)` via a KL penalty, and then sampling `z` from `q(z|x)` before decoding. At inference time, drop the encoder, sample `z ~ N(0, I)`, decode. The KL penalty is what forces the code space to be structured.

> Kingma 2013 年的 VAE 通过训练编码器输出*分布* `q(z|x) = N(μ(x), σ(x)²)` 来解决这个问题，通过 KL 惩罚将该分布拉向先验 `N(0, I)`，然后从 `q(z|x)` 中采样 `z` 再解码。推理时，丢弃编码器，从 `N(0, I)` 采样 `z`，解码。KL 惩罚正是使编码空间结构化的关键。

In 2026 VAEs rarely ship standalone — they have been outclassed by diffusion for raw image quality — but they are the encoder of choice for every latent-diffusion model (SD 1/2/XL/3, Flux, AudioCraft). Learn the VAE and you learn the invisible first layer of every image pipeline you use.

> 2026 年 VAE 很少独立部署——在原始图像质量上已被扩散模型超越——但它是所有潜在扩散模型（SD 1/2/XL/3、Flux、AudioCraft）的首选编码器。学会 VAE 就学会了你使用的每个图像流水线中隐形的第一层。

> **【中文解读】** VAE 的核心洞察：让编码器输出分布而非点估计。通过重参数化技巧 `z = mu + sigma * epsilon` 使采样可微，用 KL 散度约束编码空间接近标准正态分布。ELBO 损失 = 重建损失 + beta * KL 散度，两者相互权衡。推理时只需从标准正态采样并解码，一次前向传播即可生成。

> **【拓展：beta-VAE 与解耦表示学习】** beta-VAE（2017）通过调节 beta 参数控制重建与 KL 的权衡。beta<1 时重建更清晰但潜在空间不规整；beta>1 时潜在空间更规整但图像更模糊。当 beta 足够大时，VAE 可以学到"解耦"的表示——每个维度编码独立的语义因子（如颜色、形状、大小）。这启发了后续的扩散模型在潜在空间中做可控生成。

## The Concept | 核心概念

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`, `x̂ = decoder(z)`, loss = `||x - x̂||²`. Code space unstructured.

> **自编码器。** `z = encoder(x)`，`x̂ = decoder(z)`，损失 = `||x - x̂||²`。编码空间无结构。

**VAE encoder.** Outputs two vectors: `μ(x)` and `log σ²(x)`. These define `q(z|x) = N(μ, diag(σ²))`.

> **VAE 编码器。** 输出两个向量：`μ(x)` 和 `log σ²(x)`。它们定义了 `q(z|x) = N(μ, diag(σ²))`。

**Reparameterization trick.** Sampling from `q(z|x)` is not differentiable. Rewrite the sample as `z = μ + σ·ε` where `ε ~ N(0, I)`. Now `z` is a deterministic function of `(μ, σ)` plus a non-parameter noise — gradients flow through `μ` and `σ`.

> **重参数化技巧。** 从 `q(z|x)` 采样不可微。将采样重写为 `z = μ + σ·ε`，其中 `ε ~ N(0, I)`。现在 `z` 是 `(μ, σ)` 的确定性函数加上非参数噪声——梯度可以通过 `μ` 和 `σ` 反向传播。

**Loss.** Evidence Lower BOund (ELBO), two terms:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

Reconstruction pushes `x̂` toward `x`. KL pushes `q(z|x)` toward the prior. They trade off. Small β (<1) = sharper samples, code space less Gaussian. Large β (>1) = cleaner code space, blurrier samples. β-VAE (Higgins 2017) made this knob famous and kicked off disentanglement research.

> 重建损失推动 `x̂` 趋近 `x`。KL 推动 `q(z|x)` 趋近先验。两者相互权衡。β 小（<1）= 更锐利的样本，编码空间不太高斯。β 大（>1）= 更干净的编码空间，更模糊的样本。β-VAE（2017）使这个旋钮闻名，并开启了解耦表示学习研究。

**Sampling.** At inference: draw `z ~ N(0, I)`, forward through decoder. One forward pass — no iterative sampling like diffusion.

> **采样。** 推理时：从 `N(0, I)` 抽取 `z`，送入解码器前向传播。单次前向传播——无需像扩散模型那样迭代采样。

> **【中文解读】** ELBO 损失的两个组成部分各有分工：重建损失确保解码质量，KL 散度确保潜在空间的规整性。推理时完全不需要编码器——直接从 N(0,I) 采样 z 送入解码器。VAE 生成速度快（单次前向传播），但图像质量通常比扩散模型模糊，因为它优化的是 ELBO 下界而非精确似然。

> **【拓展：Stable Diffusion 中的 VAE】** Stable Diffusion 使用预训练的 VAE 将 512x512 图像压缩到 64x64 的潜在空间（8 倍下采样）。扩散过程在潜在空间中进行，大幅降低了计算量。SD 3 使用的 VAE 更先进——支持 16 通道潜在空间，图像质量更高。VAE 的压缩质量直接影响最终生成图像的细节保真度。

## Build It | 动手实现

`code/main.py` implements a tiny VAE without numpy or torch. Input is 8-dimensional synthetic data drawn from a 2-component Gaussian mixture in 8-D. Encoder and decoder are single hidden-layer MLPs. We implement tanh activation, forward pass, loss, and a hand-written backward pass. Not production — pedagogy.

> `code/main.py` 实现了一个不依赖 numpy 或 torch 的微型 VAE。输入是从 8 维 2 分量高斯混合中抽取的 8 维合成数据。编码器和解码器是单隐层 MLP。我们实现了 tanh 激活、前向传播、损失和手写反向传播。不是生产代码——纯粹教学。

### Step 1: encoder forward

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²` instead of `σ` so the network output is unconstrained (softplus of σ is a trap — gradients die at σ ≈ 0).

> 使用 `log σ²` 而非 `σ` 使得网络输出不受约束（σ 的 softplus 是个陷阱——在 σ ≈ 0 时梯度会消失）。

### Step 2: reparameterize and decode

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Step 3: the ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

Exact closed-form KL because both distributions are Gaussian. Do not integrate numerically. People still ship code with monte-carlo KL estimates in 2026 — it is 3x slower for no reason.

> 精确的闭式 KL，因为两个分布都是高斯的。不要数值积分。2026 年还有人发布蒙特卡洛 KL 估计的代码——无端慢了 3 倍。

### Step 4: generate

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

That is the generative model. Five lines.

> 这就是生成模型。五行代码。

## Pitfalls | 常见陷阱

- **Posterior collapse.** KL term drives `q(z|x) → N(0, I)` so aggressively that `z` carries no info about `x`. Fix: β-annealing (start β=0, ramp to 1), free bits, or skip the KL on inactive dimensions.
  **后验坍塌。** KL 项如此强势地将 `q(z|x)` 拉向 `N(0, I)`，导致 `z` 不携带关于 `x` 的信息。修复：β 退火（从 β=0 开始，逐渐增至 1）、free bits 或跳过不活跃维度的 KL。
- **Blurry samples.** The Gaussian decoder likelihood implies MSE reconstruction, which is Bayes-optimal for L2 (the mean) — the mean of a set of plausible digits is a fuzzy digit. Fix: discrete decoder (VQ-VAE, NVAE), or use the VAE only as an encoder and stack diffusion on the latents (this is what Stable Diffusion does).
  **模糊样本。** 高斯解码器似然意味着 MSE 重建——一组合理数字的均值是一个模糊的数字。修复：离散解码器（VQ-VAE、NVAE），或仅将 VAE 用作编码器，在潜在空间上叠加扩散模型。
- **β too large, too early.** See posterior collapse. Start at β≈0.01 and ramp.
  **β 太大太早。** 见后验坍塌。从 β≈0.01 开始并逐渐增加。
- **Latent dim too small.** 16-D works for MNIST, 256-D for ImageNet 256², 2048-D for ImageNet 1024². Stable Diffusion's VAE compresses 512×512×3 → 64×64×4 (32x downsample factor in spatial area, 32x in channels).
  **潜在维度太小。** MNIST 用 16 维，ImageNet 256² 用 256 维。Stable Diffusion 的 VAE 将 512×512×3 压缩为 64×64×4。

## Use It | 用框架实现

The 2026 VAE stack:

> 2026 年 VAE 技术栈：

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

A latent-diffusion model is a VAE with a diffusion model living between encoder and decoder. The VAE does coarse compression, the diffusion model does the heavy lifting. Same pattern for video (VAE + video-diffusion DiT) and audio (Encodec + MusicGen transformer).

> 潜在扩散模型就是编码器和解码器之间加入了扩散模型的 VAE。VAE 做粗压缩，扩散模型做重活。视频（VAE + 视频 DiT）和音频（Encodec + MusicGen transformer）同理。

## Ship It | 产出物

Save `outputs/skill-vae-trainer.md`.

> 保存 `outputs/skill-vae-trainer.md`。

Skill takes: dataset profile + latent-dim target + downstream use (reconstruction, sampling, or latent-diffusion input) and outputs: architecture choice (plain/β/VQ/RVQ), β schedule, latent dim, decoder likelihood (Gaussian vs categorical), and evaluation plan (recon MSE, KL per dim, Fréchet distance between `q(z|x)` and `N(0, I)`).

> Skill 接收：数据集概况 + 潜在维度目标 + 下游用途（重建、采样或潜在扩散输入），输出：架构选择（plain/β/VQ/RVQ）、β 调度、潜在维度、解码器似然（高斯 vs 类别）和评估计划。

## Exercises | 练习题

1. **Easy / 简单.** Change `β` in `code/main.py` to `0.01`, `0.1`, `1.0`, `5.0`. Record the final reconstruction MSE and KL. Which β is Pareto-best for your synthetic data?
   在 `code/main.py` 中将 `β` 改为 `0.01`、`0.1`、`1.0`、`5.0`。记录最终重建 MSE 和 KL。哪个 β 对你的合成数据是帕累托最优？
2. **Medium / 中等.** Replace the Gaussian decoder likelihood with a Bernoulli likelihood (cross-entropy loss). Compare sample quality on a binarized version of the same synthetic data.
   将高斯解码器似然替换为伯努利似然（交叉熵损失）。在二值化的合成数据上比较样本质量。
3. **Hard / 困难.** Extend `code/main.py` into a mini VQ-VAE: replace the continuous `z` with a nearest-neighbour lookup in a codebook of K=32 entries. Compare reconstruction MSE and report how many codebook entries get used (codebook collapse is real).
   将 `code/main.py` 扩展为迷你 VQ-VAE：用 K=32 的码本最近邻查找替换连续 `z`。比较重建 MSE 并报告使用了多少码本条目。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Production note: the VAE is the hottest path in a diffusion server | 生产笔记：VAE 是扩散服务器中最热的路径

In a Stable Diffusion / Flux / SD3 pipeline the VAE is called twice per request — once to encode (if doing img2img / inpainting) and once to decode. At 1024² the decoder pass is often the single largest activation-memory peak in the whole pipeline because it upsamples `128×128×16` latents back to `1024×1024×3`. Two practical consequences:

> 在 Stable Diffusion / Flux / SD3 流水线中，VAE 每次请求被调用两次——一次编码（img2img/inpainting）一次解码。在 1024² 分辨率下，解码器通常是整个流水线中激活内存峰值最大的部分。两个实际后果：

- **Slice or tile the decode.** `diffusers` exposes `pipe.vae.enable_slicing()` and `pipe.vae.enable_tiling()`. Tiling trades a small seam artifact for `O(tile²)` memory instead of `O(H·W)`. Essential for 1024²+ on consumer GPUs.
  **切片或分块解码。** `diffusers` 提供 `enable_slicing()` 和 `enable_tiling()`。分块以轻微接缝伪影换取 `O(tile²)` 内存。
- **bf16 decoder, fp32 numerics for the final resize.** The SD 1.x VAE was released in fp32 and *silently produces NaNs* when cast to fp16 at 1024²+. SDXL ships `madebyollin/sdxl-vae-fp16-fix` — always prefer the fp16-fix variant or use bf16.
  **bf16 解码器，fp32 用于最终 resize。** SD 1.x VAE 在 fp16 下 1024²+ 会静默产生 NaN。始终使用 fp16-fix 变体或 bf16。

## Further Reading | 延伸阅读

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) — the VAE paper.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) — disentangled β-VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) — VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) — state-of-the-art image VAE.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — Stable Diffusion; VAE as encoder.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) — Encodec, the audio VAE standard.
