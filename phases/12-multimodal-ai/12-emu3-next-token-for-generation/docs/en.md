# Emu3: Next-Token Prediction for Image and Video Generation | Emu3：用下一 Token 预测生成图像与视频

> BAAI's Emu3

> **【中文解读】** Emu3（BAAI，2024年9月）用单一的自回归下一 token 预测目标，在统一的文本+图像+视频词汇表上训练，在图像生成上击败了 SDXL，在视觉理解上击败了 LLaVA-1.6。没有 CLIP 损失，没有扩散调度，核心训练目标就是下一 token 预测。发表在 Nature 上。

> **【拓展：自回归 vs 扩散的争论】** Emu3 的核心贡献是概念性的：如果下一 token 预测能在图像生成上匹敌扩散模型，那么统一模型路径（一个损失、一个骨干、任何模态）就是可行的。后续的 Show-o、Janus-Pro、InternVL-U 都建立在这个论点之上。 (Wang et al., September 2024) is the 2024 result that should have ended the diffusion-versus-autoregressive debate. A single Llama-style decoder-only transformer, trained only on the next-token-prediction objective, across a unified vocabulary of text + VQ image tokens + 3D VQ video tokens, beats SDXL on image generation and LLaVA-1.6 on perception. No CLIP loss. No diffusion schedule. Classifier-free guidance is used at inference for quality, but the core training objective is next-token prediction with teacher forcing. Published in Nature. This lesson reads the Emu3 thesis — why a better tokenizer plus scale is all you need — and contrasts with diffusion approaches.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives  | 学习目标

- Explain why Emu3's single-loss next-token objective works despite the long-held assumption that diffusion is required for image quality.
- Describe the 3D video tokenizer: what a spatiotemporal VQ codebook looks like, why patches span time.
- Compare Emu3 vs Stable Diffusion XL on (training compute, inference cost, quality ceiling).
- Name the three roles the same Emu3 model plays: Emu3-Gen (image gen), Emu3-Chat (perception), Emu3-Stage2 (video gen).

## The Problem  | 问题背景

The conventional wisdom through 2024: image generation needs diffusion. The argument: discrete image tokens lose too much information to reconstruct detail, and autoregressive sampling accumulates error across thousands of tokens. Stable Diffusion, DALL-E 3, Imagen, Midjourney all use some form of diffusion. Chameleon (Lesson 12.11) partially disproved this at small scale but did not match SDXL on quality.

> 2024 年前的共识：图像生成需要扩散模型。论点是：离散图像 token 损失太多信息无法重建细节，自回归采样在数千个 token 上累积误差。Stable Diffusion、DALL-E 3、Imagen、Midjourney 都使用某种形式的扩散。Chameleon（第 12.11 课）在小规模上部分证伪了这一点，但质量上没有匹敌 SDXL。

Emu3 attacked the argument head-on. The claim: better visual tokenizer + enough scale + next-token loss = diffusion-beating image generation in the same model that also does perception.

> Emu3 正面攻击了这一论点。声称：更好的视觉分词器 + 足够的规模 + 下一 token 损失 = 在同一模型中超越扩散的图像生成，同时还能做感知。

The bet was controversial when it published. Two years on, the open-source unified-generation family (Emu3, Show-o, Janus-Pro, Transfusion) is the default path for research; production frontier models appear to use some variant.

> 这个赌注发表时有争议。两年后，开源统一生成家族（Emu3、Show-o、Janus-Pro、Transfusion）成为研究的默认路径；生产前沿模型似乎也使用某种变体。

## The Concept  | 核心概念

> **【中文解读】** EMU3 使用纯自回归下一个 token 预测统一了多模态理解和生成。图像被离散化为 token 序列后，模型像预测文本一样预测下一个视觉 token。无需扩散模型——一切多模态任务都是 next-token prediction。

> **【拓展：自回归图像生成的挑战】** EMU3 的纯自回归方法在图像生成上仍落后于扩散模型，因为视觉 token 的长程依赖比文本更难学习。但统一架构的优势在于同一个模型同时理解和生成图像/文本。


### The Emu3 tokenizer

The key ingredient is the visual tokenizer. Emu3 trains a custom IBQ-class tokenizer (Inverse Bottleneck Quantizer, SBER-MoVQGAN family) at 8x8 resolution-reduction per token. A 512x512 image becomes 64x64 = 4096 tokens at codebook size 32768.

> 关键成分是视觉分词器。Emu3 训练了自定义的 IBQ 类分词器（逆瓶颈量化器，SBER-MoVQGAN 家族），每个 token 8x8 分辨率缩减。一张 512x512 图像变成 64x64 = 4096 个 token，码本大小 32768。

This is larger than Chameleon's 1024 tokens per 512x512 at K=8192 but cheaper per token (smaller codebook lookups, simpler codec). The key metric: reconstruction PSNR at 30.5 dB, competitive with Stable Diffusion's continuous latent space at 32 dB.

> 这比 Chameleon 的每张 512x512 图像 1024 个 token（K=8192）更大，但每个 token 更便宜（更小的码本查找、更简单的编解码器）。关键指标：重建 PSNR 为 30.5 dB，与 Stable Diffusion 的连续潜空间 32 dB 竞争。

For video: a 3D VQ tokenizer encodes a spatiotemporal patch (4x4x4 pixels) to one integer. A 4s clip at 8 FPS has 32 frames; at 256x256 with 4x spatial and 4x temporal reduction, the token count is (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32,768 tokens.

> 对于视频：3D VQ 分词器将时空 patch（4x4x4 像素）编码为一个整数。4 秒片段在 8 FPS 下有 32 帧；256x256 分辨率下 4x 空间和 4x 时间缩减，token 数为 32768。

Tokenizer quality is the ceiling. Emu3's contribution is partly "we trained a very good tokenizer."

> 分词器质量是上限。Emu3 的贡献部分在于"我们训练了一个非常好的分词器"。

### Single-loss training

Emu3 uses one objective: next-token prediction on a shared vocabulary across text tokens, 2D image tokens, and 3D video tokens. Weights are multiplied by modality-specific factors during training to balance contribution, but the loss function is identical.

> Emu3 使用一个目标：在共享词汇表上的下一 token 预测，涵盖文本 token、2D 图像 token 和 3D 视频 token。训练时权重乘以模态特定因子以平衡贡献，但损失函数相同。

Train on a mix of:
- Image gen: `<text caption> <image> image_tokens </image>`
  中文翻译：图像生成
- Image perception: `<image> image_tokens </image> <question> text_tokens`
  中文翻译：图像感知
- Video gen: `<text caption> <video> video_tokens </video>`
  中文翻译：视频生成
- Video perception: analogous.
  中文翻译：视频感知：类似。
- Text only: standard NTP.
  中文翻译：纯文本：标准下一 token 预测。

The model learns when to emit image tokens vs text tokens from the data distribution. Generation emerges from the model predicting image tokens after the `<image>` tag.

> 模型从数据分布中学习何时输出图像 token 与文本 token。生成能力来自模型在 `<image>` 标签后预测图像 token。

### Classifier-free guidance and temperature

Autoregressive image generation gets much better with classifier-free guidance (CFG) at inference. Emu3 uses it: generate twice, once with the full caption, once with an empty caption, mix the logits with a guidance weight (typical 3.0-7.0). This is the same CFG trick diffusion uses, borrowed to the autoregressive setting.

> 自回归图像生成在推理时使用无分类器引导（CFG）效果更好。Emu3 使用它：生成两次，一次用完整描述，一次用空描述，用引导权重（典型值 3.0-7.0）混合 logits。这是扩散模型使用的相同 CFG 技巧，借用到自回归设置中。

Temperature matters: too high, artifacts; too low, mode collapse. Emu3's recommended temperature is 1.0 for perception, 0.8 for image generation.

> 温度很重要：太高会有伪影；太低会导致模式崩溃。Emu3 推荐的温度是感知用 1.0，图像生成用 0.8。

### Three roles, one model

Emu3 ships as three functionally distinct APIs but one underlying weight set:

> Emu3 以三个功能不同的 API 发货，但使用同一套权重：

- Emu3-Gen. Image generation. Input text, output image tokens.
  中文翻译：Emu3-Gen。图像生成。输入文本，输出图像 token。
- Emu3-Chat. VQA and captioning. Input image (tokens), output text.
  中文翻译：Emu3-Chat。视觉问答和描述。输入图像（token），输出文本。
- Emu3-Stage2. Video generation and video VQA. Input text or video, output text or video.
  中文翻译：Emu3-Stage2。视频生成和视频问答。输入文本或视频，输出文本或视频。

No task-specific heads. Just different prompt templates. Same checkpoint.

> 没有任务特定的头。只是不同的提示模板。同一个检查点。

### Benchmarks

From Emu3 paper (September 2024):

> 来自 Emu3 论文（2024 年 9 月）：

- Image generation: beats SDXL on MJHQ-30K FID (5.4 vs 5.6), GenEval overall (0.54 vs 0.55 — statistical tie), and Deep-Eval's composite on-par.
  中文翻译：图像生成：在 MJHQ-30K FID 上击败 SDXL（5.4 vs 5.6），GenEval 总体（0.54 vs 0.55——统计上打平）。
- Image perception: beats LLaVA-1.6 on VQAv2 (75.1 vs 72.4) and roughly matches on MMMU.
  中文翻译：图像感知：在 VQAv2 上击败 LLaVA-1.6（75.1 vs 72.4），在 MMMU 上大致持平。
- Video generation: 4-second-clip quality at competitive FVD with Sora-era publicly benchmarked models.
  中文翻译：视频生成：4 秒片段质量与 Sora 时代的公开基准模型竞争力相当。

The numbers are not always winning — Emu3 trades a point here for a point there — but the claim "next-token prediction is all you need" is defensible across modalities.

> 数字并不总是赢——Emu3 在一个点上换另一个点——但"下一 token 预测就是你需要的一切"这一声称在所有模态上都是站得住脚的。

### Compute cost

Emu3 was trained on ~300 billion multimodal tokens with a 7B-parameter model. GPU-hours roughly comparable to Llama-2-7B pretraining (2k-4k GPU-years on A100-class silicon). Diffusion models like Stable Diffusion 3 train in similar budgets but need separate text encoders and more complex pipelines.

> Emu3 在约 3000 亿多模态 token 上用 70 亿参数模型训练。GPU 小时数大致与 Llama-2-7B 预训练相当（A100 级硅片上 2k-4k GPU 年）。Stable Diffusion 3 等扩散模型在类似预算下训练，但需要独立的文本编码器和更复杂的管线。

At inference, Emu3 is slower than SDXL per image: 4096 image tokens at 30 tok/s is ~2 minutes per 512x512 image, vs 2-5 seconds for SDXL. Speculative decoding and KV-cache optimization narrow the gap but do not close it. Autoregressive image gen is compute-heavy; this is the standing trade-off.

> 推理时，Emu3 每张图像比 SDXL 慢：4096 个图像 token 以 30 tok/s 生成，每张 512x512 图像约 2 分钟，而 SDXL 只需 2-5 秒。投机解码和 KV 缓存优化缩小了差距但没有关闭它。自回归图像生成计算密集；这是持续存在的权衡。

### Why it matters

Emu3's deep contribution is conceptual. If next-token prediction scales to match diffusion on image generation, the unified-model path (one loss, one backbone, any modality) is viable. Future models do not need separate text encoders, separate diffusion schedulers, separate VAEs. One transformer, one tokenizer per modality, scale.

> Emu3 的深层贡献是概念性的。如果下一 token 预测能扩展到在图像生成上匹敌扩散，统一模型路径（一个损失、一个骨干、任何模态）就是可行的。未来的模型不需要独立的文本编码器、独立的扩散调度器、独立的 VAE。一个 Transformer，每种模态一个分词器，然后扩展规模。

Show-o, Janus-Pro, and InternVL-U all build on or challenge this thesis. Chinese labs (BAAI, DeepSeek) publish more aggressively in this direction than US labs through 2025.

> Show-o、Janus-Pro 和 InternVL-U 都建立在这个论点之上或挑战它。中国实验室（BAAI、DeepSeek）在 2025 年之前比美国实验室更积极地在这个方向发表。


> **【拓展：EMU3 的统一训练策略】** EMU3 的核心贡献是证明纯自回归方法可以同时做理解和生成。在视觉理解任务上接近 LLaVA，在文生图上接近 SDXL。训练使用多模态混合数据，不同模态的 loss 按比例加权。


## Use It  | 动手实践

`code/main.py` builds two toy pieces:

> `code/main.py` 构建了两个玩具组件：

- A 2D vs 3D VQ tokenizer count calculator: given (resolution, patch, clip_length, FPS), compute token counts for image vs video.
  中文翻译：2D vs 3D VQ 分词器计数计算器：给定（分辨率、patch、片段长度、FPS），计算图像与视频的 token 数。
- An autoregressive image-token sampler with classifier-free guidance at temperature.
  中文翻译：带温度和无分类器引导的自回归图像 token 采样器。

The CFG implementation matches Emu3's recipe — mix conditional and unconditional logits with a guidance weight.

> CFG 实现匹配 Emu3 的方案——用引导权重混合条件和无条件 logits。

## Ship It  | 部署上线

This lesson produces `outputs/skill-token-gen-cost-analyzer.md`. Given a generation product spec (image or video, target resolution, quality tier, latency budget), it computes token counts, inference cost, and picks Emu3-family vs diffusion.

> 本课产出 `outputs/skill-token-gen-cost-analyzer.md`。给定生成产品规格（图像或视频、目标分辨率、质量等级、延迟预算），它计算 token 数量、推理成本，并在 Emu3 系列与扩散模型之间选择。

## Exercises  | 练习题

1. Emu3 produces 4096 tokens per 512x512 image at 8x8 reduction. Compute the equivalent for 1024x1024 and 2048x2048. What happens to inference latency?
   中文翻译：Emu3 在 8x8 缩减下每张 512x512 图像产生 4096 个 token。计算 1024x1024 和 2048x2048 的等效值。推理延迟会怎样？

2. Read Emu3 Section 3.3 on the video tokenizer. Describe the 3D VQ patch shape and why it is 4x4x4 not 8x8x1.
   中文翻译：阅读 Emu3 第 3.3 节关于视频分词器。描述 3D VQ patch 形状以及为什么是 4x4x4 而非 8x8x1。

3. Classifier-free guidance weight 5.0 vs 3.0: what visual effect? Trace the math in `code/main.py`.
   中文翻译：无分类器引导权重 5.0 vs 3.0：视觉效果是什么？追踪 `code/main.py` 中的数学。

4. Compute training FLOPs for Emu3-7B at 300B tokens and compare to Stable Diffusion 3. Which was more expensive to train?
   中文翻译：计算 Emu3-7B 在 300B token 上的训练 FLOPs，并与 Stable Diffusion 3 比较。哪个训练更贵？

5. Emu3 beats SDXL on FID but not on VQAv2 vs specialized VLMs. Explain why the unified-loss approach shows different strengths vs specialists on different benchmarks.
   中文翻译：Emu3 在 FID 上击败 SDXL，但在 VQAv2 上不如专业 VLM。解释为什么统一损失方法在不同基准上表现出不同的优势。

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Further Reading  | 延伸阅读

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  中文翻译：Emu3 论文——下一 token 预测就是你需要的一切。
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  中文翻译：Emu 多模态生成预训练。
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  中文翻译：LWM 论文。
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  中文翻译：MAGVIT-v2 视频分词器。
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  中文翻译：VAR 视觉自回归模型。
