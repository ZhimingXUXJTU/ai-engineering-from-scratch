# 潜在扩散与 Stable Diffusion

> 在 512x512 像素空间做扩散是计算犯罪。Rombach et al.（2022）注意到你不需要全部 78.6 万维度来生成图像——你只需要足够捕获语义结构的维度，其余用单独的解码器补充。在 VAE 的潜在空间中运行扩散。这一个想法就是 Stable Diffusion。

> **【中文解读】** 在 512x512 像素空间做扩散是计算灾难。Rombach 等人发现不需要全部 78.6 万维度——只需捕获语义结构，其余用解码器补充。在 VAE 的潜在空间中运行扩散，这一个想法就是 Stable Diffusion。

> **【拓展：Stable Diffusion 的革命】** Stable Diffusion 将扩散过程从像素空间移到潜在空间，计算量降低数十倍，使消费级 GPU 可以运行。开源发布后催生了 LoRA、ControlNet 等丰富生态，推动了 AIGC 的普及化。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 02（VAE）、阶段 8 · 06（DDPM）、阶段 7 · 09（ViT）
**预计时间：** ~75 分钟

## 问题引入

512² 分辨率的像素空间扩散意味着 U-Net 在形状 `[B, 3, 512, 512]` 的张量上运行。对于 500M 参数的 U-Net，每个采样步约 100 GFLOPS。50 步是每张图像 5 TFLOPS。在十亿张图像上训练，计算成本荒谬。

这些 FLOP 中的大部分用于将感知上不重要的细节推过网络——有损 VAE 可以压缩掉的高频纹理。Rombach 的想法：训练一次 VAE（*第一阶段*），冻结它，完全在 4 通道 64×64 的潜在空间（*第二阶段*）中运行扩散。同一个 U-Net。像素数降为 1/16。FLOP 约减少 64 倍，质量相当。

这就是 Stable Diffusion 的配方。SD 1.x / 2.x 使用 860M 的 U-Net 在 `64×64×4` 潜在表示上，SDXL 使用 2.6B 的 U-Net 在 `128×128×4` 上，SD3 将 U-Net 换成了带流匹配的扩散 Transformer (DiT)。Flux.1-dev（Black Forest Labs，2024）部署了一个 12B 参数的 DiT-MMDiT。所有都运行在相同的两阶段基础设施上。

> **【中文解读】** Stable Diffusion 的核心架构是两阶段设计：(1) 第一阶段——VAE 编码器将 512x512 图像压缩到 64x64x4 潜在空间（16 倍压缩）；(2) 第二阶段——在潜在空间中运行扩散过程。U-Net 在 64x64 张量上运行，计算量降低约 64 倍。从 SD 1.x 到 SD3 的演进：U-Net → DiT（Diffusion Transformer），DDPM → Flow Matching。

> **【拓展：从 U-Net 到 DiT 的架构变迁】** SD 1.x/2.x 使用 U-Net 作为去噪网络。SD3（2024）和 FLUX 转向 DiT（Diffusion Transformer）——用 Transformer 替代 U-Net。DiT 的优势在于扩展性更好（Transformer 的缩放定律适用）、支持更高分辨率、可以更好地融合文本条件。这一架构变迁与 NLP 领域的 Transformer 统一趋势一致。

## 核心概念

![潜在扩散：VAE 压缩 + 潜在空间中的扩散](../assets/latent-diffusion.svg)

**两个阶段，分别训练。**

1. **阶段 1 — VAE。** 编码器 `E(x) → z`，解码器 `D(z) → x`。目标压缩：每个空间轴 8 倍下采样 + 调整通道使总潜在大小约为像素数的 1/16。损失 = 重建（L1 + LPIPS 感知）+ KL（小权重，这样 `z` 不会被强制太接近高斯，因为我们不需要从 `z` 精确采样）。通常还会加上对抗损失使解码图像更清晰。

2. **阶段 2 — 在 `z` 上做扩散。** 将 `z = E(x_real)` 视为数据。训练 U-Net（或 DiT）对 `z_t` 去噪。推理时：通过扩散采样 `z_0`，然后 `x = D(z_0)`。

**文本条件化。** 两个额外组件。一个冻结的文本编码器（SD 1.x 用 CLIP-L，SD 2/XL 用 CLIP-L+OpenCLIP-G，SD3 和 Flux 用 T5-XXL）。一个交叉注意力注入：每个 U-Net 块接收 `[Q = 图像特征, K = V = 文本 token]` 并将它们混合。文本 token 是文本影响图像的唯一途径。

**损失函数与第 06 课完全相同。** 同样的 DDPM / 流匹配噪声 MSE。你只是换了数据域。

## 架构变体

| 模型 | 年份 | 主干 | 潜在形状 | 文本编码器 | 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 token) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | 蒸馏版 | 128×128×4 | 同上 | 1-4 步采样 |
| SD3 | 2024 | MMDiT（多模态 DiT） | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT 蒸馏版 | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 步 |

趋势：用 DiT（潜在 patch 上的 Transformer）替代 U-Net，扩展文本编码器（T5 在提示遵循度上优于 CLIP），增加潜在通道（4 → 16 提供更多细节空间）。

## 动手实现

`code/main.py` 在第 06 课 DDPM 之上堆叠了一个玩具 1 维"VAE"（恒等编码器 + 解码器，用于演示；真实 VAE 应该是卷积网络），并添加了带无分类器引导的类别条件化。它展示了相同的扩散损失无论在原始 1 维值还是编码值上都能工作——这是关键洞察。

### 步骤 1：编码器/解码器

```python
def encode(x):    return x * 0.5          # 玩具"压缩"到更小尺度
def decode(z):    return z * 2.0
```

真实的 VAE 有训练好的权重。为了教学，这个线性映射足以展示扩散在 `z` 上操作而不关心原始数据空间。

### 步骤 2：在 `z` 空间中做扩散

与第 06 课相同的 DDPM。网络看到的数据是 `z = E(x)`。采样 `z_0` 后，用 `D(z_0)` 解码。

### 步骤 3：无分类器引导

训练时，10% 的时间丢弃类别标签（替换为空 token）。推理时，同时计算 `ε_cond` 和 `ε_uncond`，然后：

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0` = 无引导（完全多样性），`w = 3` = 默认值，`w = 7+` = 饱和/过度清晰。

### 步骤 4：文本条件化（概念，非代码）

将类别标签替换为冻结文本编码器的输出。通过交叉注意力将文本嵌入送入 U-Net：

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

这是类别条件扩散模型与 Stable Diffusion 之间唯一实质性的区别。

## 常见陷阱

- **VAE 尺度不匹配。** SD 1.x VAE 有一个缩放常数（`scaling_factor ≈ 0.18215`）在编码后应用。忘记这个会让 U-Net 在方差严重错误的潜在表示上训练。每个检查点都会附带这个值。
- **文本编码器静默出错。** SD3 需要带 >=128 token 的 T5-XXL，仅回退到 CLIP 会有信息损失。始终检查 `use_t5=True`，否则提示保真度会崩溃。
- **混合潜在空间。** SDXL、SD3、Flux 都使用不同的 VAE。在 SDXL 潜在空间上训练的 LoRA 在 SD3 上不起作用。Hugging Face diffusers 0.30+ 会拒绝加载不匹配的检查点。
- **CFG 过高。** `w > 10` 产生饱和、油腻的图像，并以多样性为代价过度拟合提示。最佳范围是 `w = 3-7`。
- **负面提示泄漏。** 空的负面提示变成空 token；填写的负面提示变成 `ε_uncond`。这两者不同；某些流水线静默默认为空 token。

## 用框架实现

2026 年生产技术栈：

| 目标 | 推荐主干 |
|--------|----------------------|
| 窄域，配对数据，从零训练模型 | SDXL 微调（LoRA / 全量）——最快上线 |
| 开放域文本生成图像，开源权重 | Flux.1-dev（12B，Apache / 非商业）或 SD3.5-Large |
| 最快推理，开源权重 | Flux.1-schnell（1-4 步，Apache）或 SDXL-Lightning |
| 最佳提示遵循度，托管服务 | GPT-Image / DALL-E 3（仍在更新）、Midjourney v7、Imagen 4 |
| 编辑工作流 | Flux.1-Kontext（2024 年 12 月）——原生接受图像 + 文本 |
| 研究，基线 | SD 1.5 — 古老但研究充分 |

## 产出物

保存 `outputs/skill-sd-prompter.md`。技能接收文本提示 + 目标风格，输出：模型 + 检查点、CFG 缩放、采样器、负面提示、分辨率、可选 ControlNet/IP-Adapter 组合，以及逐步 QA 检查清单。

## 练习题

1. **简单。** 在 `code/main.py` 中使用引导 `w ∈ {0, 1, 3, 7, 15}` 运行。记录每个类别的样本均值。在什么 `w` 下，类别均值偏离超过真实数据均值？
2. **中等。** 将玩具线性编码器替换为带重建损失的 tanh-MLP 编码器/解码器对。在新潜在空间上重新训练扩散。样本质量是否改变？
3. **困难。** 使用 diffusers 搭建真正的 Stable Diffusion 推理：加载 `sdxl-base`，运行 30 步 Euler 步，CFG=7，计时。然后切换到 `sdxl-turbo`，4 步，CFG=0。相同主题，不同质量——描述什么改变了以及为什么。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 第一阶段 | "那个 VAE" | 训练好的编码器/解码器对；将 512² 压缩到 64²。 |
| 第二阶段 | "那个 U-Net" | 潜在空间上的扩散模型。 |
| CFG | "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`；调节条件化强度。 |
| 空 token | "空提示嵌入" | 用于 `ε_uncond` 的无条件嵌入。 |
| 交叉注意力 | "文本如何进入" | 每个 U-Net 块以文本 token 为 K 和 V 进行注意力计算。 |
| DiT | "扩散 Transformer" | 用潜在 patch 上的 Transformer 替代 U-Net；扩展性更好。 |
| MMDiT | "多模态 DiT" | SD3 的架构：文本和图像流使用联合注意力。 |
| VAE 缩放因子 | "那个神奇数字" | 将潜在表示除以约 5.4，使扩散在单位方差空间中操作。 |

## 生产笔记：在 8GB 消费级 GPU 上运行 Flux-12B

Niels 的 Flux 集成笔记是经典的"我有一块消费级 GPU，能部署吗？"配方。诀窍是生产推理文献中列出的三旋钮配方应用于扩散 DiT：

1. **交错加载。** Flux 有三个从不需要同时存在于 VRAM 中的网络：T5-XXL 文本编码器（fp32 约 10 GB）、CLIP-L（小）、12B MMDiT 和 VAE。先编码提示，*删除*编码器，加载 DiT，去噪，*删除* DiT，加载 VAE，解码。消费级 8GB GPU 一次只能装一个阶段。
2. **通过 bitsandbytes 进行 4-bit 量化。** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)` 应用于 T5 编码器和 DiT。内存降低 8 倍，对文本生成图像的质量下降几乎不可感知。
3. **CPU 卸载。** `pipe.enable_model_cpu_offload()` 在每个前向传播推进时自动在 CPU 和 GPU 之间交换模块。增加 10-20% 延迟，但使流水线可以运行。

内存核算：`10 GB T5 / 8 = 1.25 GB` 量化后，`12 B 参数 × 0.5 字节 = ~6 GB` 量化后的 DiT，加上激活。用 stas00 的术语来说，这是 TP=1 推理的极端端——没有模型并行，最大化量化。生产环境中你会在 H100 上运行 TP=2 或 TP=4；对于单台开发者笔记本电脑，这就是配方。

## 延伸阅读

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — Stable Diffusion。
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) — SDXL。
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748) — DiT。
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) — SD3, MMDiT。
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) — CFG。
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) — Flux.1 系列。
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) — 上述每个检查点的参考实现。
