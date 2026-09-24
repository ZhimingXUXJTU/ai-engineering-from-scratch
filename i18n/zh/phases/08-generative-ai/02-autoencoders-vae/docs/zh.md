# 变量自动编码器和变分自动编码器

> 简单的自动编码器压缩,然后重建.它记住.它不会生成. 添加一个技巧强加代码看起来高斯式,你得到一个样本器.`z = mu + sigma * epsilon`于是,每一个2026年使用的隐形传播和流量相匹配图像模型都会在输入时有VAE.

> **【中文解读】**简单的自编码器压缩重建,只是记忆,不能产生.`z = mu + sigma * epsilon`让梯度可以通过采样操作,这是AE训练的关键.

> **【拓展：VAE 是 Stable Diffusion 的基石】**2026年所有潜在扩散模型都在VAE的潜在空间中运行.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## 问题 问题引入

压缩一个784像素的MNIST数字到16个数字代码,然后重建.一个简单的自动编码器将重建MSE,但代码空间是一个乱的混乱.在代码空间中选择一个随机点,解码它,你会得到噪音.它没有样本器.它是一个装饰的压缩模型.

> 编码空间一团糟. 在编码空间中随时取点解码得到的噪音. 它没有采样机,只是伪装的压缩模型.

实际上你想要的是: (a) 代码空间是一个清洁的,平稳的分布,你可以从一个同位性高斯人样本`N(0, I)`编码器和解码器仍然压缩得很好. 三个目标,一个架构,一个损失.

> 你真正想要的是: (a) 编码空间是干净,平滑,可采用的分布`N(0, I)`编码器和编码器仍然压缩良好.

通过训练编码器输出 * 分布 *`q(z|x) = N(μ(x), σ(x)²)`拉出了分布到前方`N(0, I)`通过 KL 罚款,然后采样`z`其他`q(z|x)`在解码之前.在推断时,放下编码器,样本`z ~ N(0, I)`卡洛特的惩罚是迫使代码空间结构化.

> 通过训练编码器输出*分布*`q(z|x) = N(μ(x), σ(x)²)`为了解决这个问题,通过 KL 惩罚将被分配到前者.`N(0, I)`然后从`q(z|x)`中采样 `z`解码. 推理时,丢弃编码器,从`N(0, I)`采样`z`解码――KL 惩罚正是使编码空间结构化的关键.

2026年,VAE很少独立运输,它们因质量而被排名出了,但它们是每个隐藏式扩散模型 (SD 1/2/XL/3,Flux,AudioCraft) 的最佳编码器.学习VAE,你将学习你使用的每个图像管道的无形第一层.

> 2026年,VAE 很少独立部署已在原始图像质量上扩散模型超越,但它是所有潜在扩散模型的首选编码器 (SD 1/2/XL/3、Flux、AudioCraft).

> **【中文解读】**通过重参数化技巧,让编码器输出分布而不是点估计.`z = mu + sigma * epsilon`采样可微,使用KL 散度约束编码空间接近标准正态分布──ELBO 损失 = 重建损失 + beta *KL 散度,两者相互权衡──推理时只需从标准正态采样并解码,一次前向传播即可产生──

> **【拓展：beta-VAE 与解耦表示学习】**通过调节beta 参数控制重建与KL的权衡――beta<1 时重建更清晰但潜在空间不规整;beta>1 时潜在空间更规整但图像更模糊――当beta 足够大时,VAE可以学到"解"的表示每个维度编码独立的语义因子 ((如颜色,形状,大小) ⋅这启发了后续的扩散模型在潜在空间中进行可控生成――

## 概念的核心概念

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`现在`x̂ = decoder(z)`损失 = `||x - x̂||²`代码空间是不结构化的.

> **自编码器。** `z = encoder(x)`没有任何`x̂ = decoder(z)`损失 = `||x - x̂||²`编码空间无结构.

**VAE encoder.**输出两个向量:`μ(x)`其他`log σ²(x)`这些定义了`q(z|x) = N(μ, diag(σ²))`现在,我们要去.

> **VAE 编码器。**输出两个向量:`μ(x)`和 `log σ²(x)`它们定义了`q(z|x) = N(μ, diag(σ²))`,我知道.

**Reparameterization trick.**采样`q(z|x)`检测量: 检测量:`z = μ + σ·ε`在哪里`ε ~ N(0, I)`现在`z`是一个定性函数`(μ, σ)`梯度流通通过 `μ`其他`σ`现在,我们要去.

> **重参数化技巧。**从`q(z|x)`采样不可微.将采样重写为`z = μ + σ·ε`在其中`ε ~ N(0, I)`现在`z`是 `(μ, σ)`确定性函数加上非参数噪音 梯度可通过`μ`和 `σ`转向传播.

**Loss.**证据下层结合 (ELBO),两个术语:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

重建推动了`x̂`走向`x`克莱拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉`q(z|x)`它们交换. 小 β (<1) = 较敏的样本,代码空间少于高斯. 大 β (>1) = 更清洁的代码空间,模糊的样本. β-VAE (Higgins 2017) 使这个按成为著名的,并启动了解脱研究.

> 重建损失推动`x̂`趋近`x`│ 推动`q(z|x)`趋近先验──两者相互权衡──β 小(<1)= 更利的样本,编码空间不太高斯──β 大(>1)= 更干净的编码空间,更模糊的样本──β-VAE(2017) 使这个旋闻名,并开启了解表示学习研究──

**Sampling.**在推断时:抽出`z ~ N(0, I)`通过解码器进行前进. 一个前进传输,没有反复采样,比如扩散.

> **采样。**推理时:从`N(0, I)`抽取`z`单次前向传播无需像扩散模型那样代采样

> **【中文解读】**解码质量,KL 散度确保潜在空间的规整性.推理时完全不需要编码器直接从N(0,I) 采样 z 送入解码器.VAE 生成速度快(单次前向传播),但图像质量通常比扩散模型模糊,因为它优化是ELBO 下界而不是精确的模样.

> **【拓展：Stable Diffusion 中的 VAE】**稳定扩散使用预训练的VAE将512x512 图像压缩到64x64的潜在空间(8倍下采样) ⋅扩散过程在潜在空间中进行,大幅降低计算量──SD 3 使用的VAE 更进步支持16通道潜在空间,图像质量更高──VAE的压缩质量直接影响最终生成图像的细节保真性──

## 建立它,实现它.
```figure
vae-latent-grid
```

## 建立它

`code/main.py`输入是从8维的2组件高斯混合物中获取的8维合成数据.编码器和解码器是单个隐藏层MLP.我们实现了tanh激活,前传,损失和手写后传.不是生产教学.

> `code/main.py`实现一个不依赖于或火的微型VAE──输入是从8维2 分量高斯混合中抽取的8维合成数据──编码器和编码器是单隐层MLP──我们实现了 tanh 激活、前向传播、损失和手写反向传播──不是生产代码纯粹的教学──

### 步骤1:向前编码器

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`没有`σ`因此网络输出不受限制 (s 的软加值是陷  梯度在 σ ≈ 0 时死亡).

> 使用 `log σ²`而不是`σ`为了使网络输出不受限制,

### 步骤2:重组和解码

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### 步骤3:ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

由于两个分布都是高斯式的,所以它不能数字化整合.人们仍然在2026年运输代码,蒙特卡洛估计KL速度将会慢得3倍.

> 精确的关闭式KL,因为两个分布都是高的.

### 步骤4:生成

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

这就是生成模型,五行.

> 这就是生成模型.

## 陷常见的陷

- **Posterior collapse.**卡通通通用驱动器`q(z|x) → N(0, I)`如此积极的`z`没有关于`x`修复: β-取消 (开始 β=0, 向 1), 释放位,或在不活跃的尺寸上跳过 KL.
  **后验坍塌。**如此强大的地将`q(z|x)`拉向`N(0, I)`导致`z`没有关于`x`信息──修复:β 退火(从β=0开始,逐渐增长到1) 、自由位或跳过不活跃维度的 KL──
- **Blurry samples.**盖斯解码器概率意味着MSE重建,这是Bays最佳的L2 (平均值) 一个可信数字的平均值是模糊的数字. 修正:分离解码器 (VQ-VAE,NVAE),或仅用VAE作为编码器和堆扩散在隐藏 (这是稳定扩散所做的).
  **模糊样本。**高斯解码器似然意味着MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE),或仅将VAE用作编码器,在潜在空间上叠加扩散模型──
- **β too large, too early.**看到后部崩. 开始在 β≈0.01 和道.
  **β 太大太早。**见后验塌──从 β≈0.01 开始并逐渐增加──
- **Latent dim too small.**16D为MNIST工作,256-D为ImageNet 2562,2048-D为ImageNet 10242.稳定扩散的VAE压缩为512×512×3 →64×64×4 (32x空间面积下样数,32x频道).
  **潜在维度太小。**磁力共振系统将512×512×3压缩为64×64×4

## 用它实现框架

2026 年的VAE堆:

> 2026 年 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

隐形传播模型是一个VAE,其中一个分布模型在编码器和解码器之间存在.VAE执行粗压,扩散模型执行重量起重.视频 (VAE +视频扩散diT) 和音频 (Encodec + MusicGen变压器) 的模式相同.

> 潜在扩散模型就是编码器和编码器之间加入扩散模型的VAE──VAE做粗压缩,扩散模型做重活──视频(VAE + 视频 DiT) 和音频(Encodec + MusicGen变压器) 同理──

## 运送它.

保存`outputs/skill-vae-trainer.md`现在,我们要去.

> 保存`outputs/skill-vae-trainer.md`,我知道.

技能:数据集的配置文件 + 隐形dim目标 + 下游使用 (重建,采样或隐形diffusion输入) 和输出:建筑选择 (平面/β/VQ/RVQ), β时间表,隐形dim,解码概率 (Gaussian vs 类型),评估计划 (Recon MSE, KL per dim, Fréchet 距离之间的距离`q(z|x)`其他`N(0, I)`)

> 接收技能:数据集概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(平/β/VQ/RVQ) 、β调度、潜在维度、解码器似然(高斯 vs 类别) 和评估计划──

## 练习题

1. **Easy / 简单.**改变`β`在`code/main.py`为了`0.01`现在`0.1`现在`1.0`现在`5.0`记录最后的重建MSE和KL. 哪个 β是最适合你的合成数据?
   在`code/main.py`中将 `β`改为`0.01`,我知道.`0.1`,我知道.`1.0`,我知道.`5.0`记录最终重建MSE和KL. 对于你的合成数据,哪个是最好的?
2. **Medium / 中等.**替换高斯解码器概率为伯诺利概率 (跨进力损失).对同样的合成数据的二进制版本进行样本质量比较.
   将高斯解码器似然替换为伯努利似然交叉损失
3. **Hard / 困难.**延长时间`code/main.py`换成小型VQ-VAE:将连续的`z`通过在 K=32 条目编程册中查找最近邻居. 进行重建MSE的比较,并报告使用的代码册条目数量 (代码册崩是真实的).
   将`code/main.py`扩展为迷你 VQ-VAE:用 K=32 的码本近邻查找替换连续 `z`△ 较重建MSE并报告使用了多少码本条款.

## 关键词 快速查找表

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

## 产品注释:VAE是扩散服务器中最热的路径

在稳定扩散/流动/SD3管道中,VAE 需要每次调用两次,一次编码 (如果做 img2img / inpainting) 和一次解码.在10242时,解码器传递通常是整个管道中最大的激活记忆峰值,因为它提升了`128×128×16`隐藏的回归`1024×1024×3`两种实际后果:

> 在稳定扩散/流动/SD3流水线中,VAE 每次请求被调用两次一次编码(img2img/inpainting) 一次解码. 在10242分辨率下,解码器通常是整个流水线中激活内存峰值最大的部分.

- **Slice or tile the decode.** `diffusers`暴露`pipe.vae.enable_slicing()`其他`pipe.vae.enable_tiling()`件交易小件`O(tile²)`记忆而不是`O(H·W)`对于10242+的消费者GPU.
  **切片或分块解码。** `diffusers`提供`enable_slicing()`和 `enable_tiling()`分块以轻微接伪影换取`O(tile²)`存储
- **bf16 decoder, fp32 numerics for the final resize.**在10242+SDXL船上,SD 1.x VAE在fp32中发布,在投到fp16时,它地产生了NaNs.`madebyollin/sdxl-vae-fp16-fix`总是偏爱fp16-fix变体或使用bf16.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在fp16 下 10242+ 会静默产生 NaN──始终使用fp16-fix 变体或bf16──

## 继续阅读 继续阅读

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)VAE论文.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl)分离 β-VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898)最新的图像.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752)稳定扩散;VAE作为编码器.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec,音频VAE标准.
