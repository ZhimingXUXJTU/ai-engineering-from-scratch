# 创建模型 类别与历史

> 每个图像模型,文本模型,视频模型和3D模型都适合五个桶之一. 选择错误的桶,你会数周战斗. 选择正确的模型,

> **【中文解读】**所有图像,文本,视频和3D生成模型都可以归类为五类:VAE、GAN、扩散模型、流模型和自归模型──选错类别让你和数学斗数周;选对,过去12年的进展就会在你的脑海中清晰堆积──

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,稳定传播的编码器;(2) GAN生成对抗网络,StyleGAN的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow匹配,SD3/FLUX的新方向;(5) 自归GPT模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## 问题 问题引入

产生型号只能做一个工作:从某种未知的分布中获取的训练样本`p_data(x)`面孔,句子,MIDI文件,蛋白质结构,如果你眼,所有这些都是相同的问题.

> 模型只能做一个事:从某个未知的分布中得到定位.`p_data(x)`抽取的训练样本,输出看起来来自相同分布的新样本――人脸,句子,MIDI文件,蛋白质结构仔细看都是同一个问题――

问题是,`p_data`它们在一个空间里存在数百万个维度 (一个512x512 RGB图像是786k维度),样本坐落在一个薄型的多元体内,你只能得到10M的例子.

> 问题在于`p_data`样本只占据了空间中的薄薄的流形,而你可能只有1000万样本. 暴力计算密度是绝望的. 每个生成模型都是一个妥协的,用一个简单的问题取代一个难题.

知道每个家庭都会做出什么妥协,就能告诉你,为什么它在某些任务上胜利,而在其他任务上崩.

> 在过去的12年中,有五个模型家庭生存下来.

> **【中文解读】**生成模型的核心任务:从训练样本中学习未知分布 p_data(x),然后生成看起来来自相同分布的新样本――挑战在高维空间中,512x512 图像约786K维) 稀疏数据――五大模型家族各有不同的妥协方式:自归/流模型直接建模密度但局限于架构;VAE/扩散模型优化密度下界;GAN 跳过密度直接生成样本――

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**2024-2026年最重要的趋势是从扩散模型 (DDPM) 转向流量匹配 (流量匹配) 的转移――流量匹配 (流量匹配) 训练更简单 (不需要调节噪音) 采样路径更直 (更少步数) 速度提升4-10倍――稳定扩散3、FLUX、AudioCraft 2 都采用了流量匹配――这是人工智能领域正在发生的范式变化――

## 概念的核心概念

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**写下`log p(x)`它们是可以实际评估的.`p(x) = ∏ p(x_i | x_<i)`正常化流量 (RealNVP,Glow) 构建`p(x)`优点:精确的可能性,清洁的训练损失. 缺点:自行降低推理是序列 (长序列的缓慢),流需要可逆的架构 (建筑限制).

> **1. 显式密度，可处理。**将`log p(x)`写成可以实际求值的求和──自归模型 ((PixelCNN、WaveNet、GPT) 将联合分布分解为条件分布乘积──标准化流(RealNVP、Glow) 通过简单分布可逆变换构建`p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)。

**2. Explicit density, approximate.**绑定`log p(x)`通过在下面 (ELBO) 进行优化,并优化边界.VAE (Kingma 2013) 使用一个变化后背的编码解码器. 扩散模型 (DDPM, Ho 2020) 训练一个暗示器,隐含优化一个权重的ELBO. 扩散是2026年占主导地位的图像,视频和3D脊柱.

> **2. 显式密度，近似。**从下面约束`log p(x)`扩散模型训练去噪音器,隐式优化加权 ELBO──扩散模型是2026年图像、视频和3D 主导骨干──

**3. Implicit density.**完全跳过密度;学习一个发电机`G(z)`产品的样本和差异性`D(x)`简单的GAN (Goodfellow 2014). 快速推断 (一次前进通过),但在训练期间不稳定. 风格GAN 1/2/3即使在2026年仍然是固定域光现实主义的最先进状态.

> **3. 隐式密度。**完全跳过密度估计;学习一个生成器`G(z)`产生样本,一个判别器`D(x)`区分真假――GAN 推理快(单次前向传播),但训练极不稳定――StyleGAN 1/2/3 即使在2026年仍是固定域照片级真感的最先进模型――

**4. Score-based / continuous-time.**了解木材密度的梯度`∇_x log p(x)`和埃尔蒙 (2019) 显示,分数匹配将扩散扩散到SDE.流量匹配 (Lipman 2023) 是2024-2026年的热度:无模拟训练,更直线路,比DDPM快4-10倍的样本采集.稳定扩散3,流量,音频工艺2都使用流量匹配.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度(分数函数) ――Song & Ermon (2019) 证明分数匹配将扩散推广到SDE──流量匹配(2023) 是2024-2026的热门:免模拟训练,更直的路径,比DDPM 快 4-10倍──稳定分散3、流量、AudioCraft 2 都使用流量匹配──

> **【中文解读】**分数匹配和流量匹配是扩散模型的泛化和改进. 分数匹配直接学习日志密度的梯度. 分数函数.

**5. Token-based autoregressive over discrete codes.**通过VQ-VAE或残余量化器将高模数数据压缩到单独代币的短序列中,然后使用变压器来模拟代币序列.Parti,MuseNet,AudioLM,VALL-E,Sora的补丁代币器都使用此.这是桶1加上学习代币器.

> **5. 基于离散 token 的自回归。**使用VQ-VAE或残差量化器将高维数据压缩为离散代币的短序列,然后使用变压器 建模代币序列.

## 简短的历史

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## 五个问题分类法

在阅读方法部分之前,当新生成模型纸出现时,请回答这五个问题.

> 在新生成模型论文发布时,在阅读方法部分之前,先回答这五个问题.

1. **What is being modeled?**像素,隐藏,分离代币,3D高西安,网格,波形?
   **正在建模什么？**像素,潜在表示,离散标志,3D高斯,网格,波形?
2. **Is the density explicit or implicit?**他们写下了吗?`log p(x)`现在,我们要去.
   **密度是显式还是隐式的？**他们写了吗?`log p(x)`现在,我们要去.
3. **Sampling: one-shot or iterative?**反复式意味着推断速度较慢; 一次射击通常意味着反向性或蒸性.
   **采样：单次还是迭代？**代意味着推理更慢;单次通常意味着对抗或蒸.
4. **Conditioning: unconditional, class, text, image, pose?**这决定了损失和建筑架构.
   **条件：无条件、类别、文本、图像、姿态？**这决定了损失函数和架构框架.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**每个人都知道故障模式 (见14课).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**它们都具有已知的失效模式.

在这个阶段,你会对每一个课程都回复这些五个答案.

> 你将在这个阶段的每节课中重新回答这些五个问题.

> **【中文解读】**这五个问题 (建模对象,显式/隐式密度,采样方式,条件类型,评估标志) 是分析任何生成模型的通用框架.

## 建立它,实现它.
```figure
autoencoder-bottleneck
```

## 建立它

这一课的代码是轻量化可视化:通过使用三个玩具方法 (核密度,分离性 histogram 和最近的样本"GAN-ish"发电机) 来从样本中调整1D的Gaussians混合物,这样你就可以在一个屏幕上打印出的问题上看到明确与隐含密度之间的区别.

> 本课程的代码是一个轻量级可视化:使用三种简单方法 ((核密度估计,离散直方图,近邻"GAN风格"生成器) 从样本中适合一维高的混合分布,让你在一屏幕内清晰地看出显著密度与隐形密度之间的区别.

跑步`code/main.py`它从两种模式的高斯混合物中取出2000个样本,然后打印:

> 运行`code/main.py`,它从双峰高斯混合中抽取2000个样本,然后打印:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

首先,我们需要注意:第两个问题让你问"这个问题是多么可能的?"第三个问题是不能.这是*明确与隐含的*区别,这将在每一个未来的课程中都重要.

> 注意:前两种方法可以回答"这个点有多大概率?"第三种不能.

## 用它实现框架

2026年,哪个家庭,要做什么任务?

> 2026年,哪个家庭适合哪个任务?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## 运送它.

保存如`outputs/skill-model-chooser.md`现在,我们要去.

> 保存为`outputs/skill-model-chooser.md`,我知道.

技能需要一个任务描述和输出: (1) 使用哪个组件, (2) 排列三个开放和三个托管的选项, (3) 您应该关注的可能失败模式,以及 (4) 计算/时间预算.

> 应注意可能失效模式, (4) 计算/时间预算.

## 练习题

1. **Easy / 简单.**对于这五种产品,确定其家族和脊椎:ChatGPT图像,Midjourney v7,Sora,Runway Gen-3,ElevenLabs. 证据应来自公开技术报告.
   对于这五个产品,识别其家族和骨干:ChatGPT图片、Midjourney v7、Sora、Runway Gen-3、ElevenLabs──证据应来自公开技术报告──
2. **Medium / 中等.**报纸中,你即将读到的报纸称采样速度比扩散速度快100倍.
   你明天要读的论文声称比扩散快100倍采样――写下三个问题来检查是否在条件生成和高分辨率下仍然存在――
3. **Hard / 困难.**回答当前SOTA模型的五个问题分类,并绘制一个更好的模型将改变什么.
   选择一个你关心的领域 (如蛋白质结构,CAD,分子轨迹) 对于该领域当前的SOTA模型回答五个问题分类法,并勾勒出更好的模型会改变什么――

## 关键词 快速查找表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## 产品注释:五个家庭,五个推理形态

每个家庭都将推断服务器成本曲线进行不同的映射.

> 每个家庭应对不同的推理服务器成本曲线.

- **Autoregressive (bucket 1 and 5).**序列解码占据延迟;KV缓存,连续批量和推测解码都直接适用于.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**没有法学法学意义上的解码.`num_steps × step_cost`其他`step_cost`生产是步骤计数 (DDIM / DPM-Solver /蒸),批量大小和精度 (bf16 / fp8 / int4).
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**法律法学 意义上没有解码.`num_steps × step_cost`生产调节旋转是步数,批量大小和精度.
- **GAN (bucket 3).**没有时间表,没有KV缓存,TTFT ≈总延迟,这就是为什么StayGAN仍然在狭域UX中获胜的原因.
  **GAN（第 3 类）。**单次前向传播――没有调度,没有KV缓存――TTFT ≈ 总延迟――这就是StayGAN在狭域UX上仍然胜出的原因――

在论文摘要中,当你看到"快于传播"时,把它转化为"少步 × 同步成本"或"同步步 × 低成本".其他的都是营销.

> 当论文摘要中说"比扩散更快"时,翻译为"更少步数 × 相同步成本"或"同步数 × 更便宜的步数成本"──其余都是营销──

## 继续阅读 继续阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661)GAN文件.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)VAE论文.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) 关于DDPM的论文.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456)作为SDE的扩散.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) 流量相匹配的纸.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206)稳定扩散 3.
