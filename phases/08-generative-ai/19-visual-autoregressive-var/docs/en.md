# Visual Autoregressive Modeling (VAR): Next-Scale Prediction | 视觉自回归建模 (VAR)：下一尺度预测

> Diffusion models sample iteratively in time (denoising steps). VAR samples iteratively in scale — it predicts a 1x1 token, then 2x2, then 4x4, up to the final resolution, each scale conditioning on the previous. The 2024 paper showed VAR matches GPT-style scaling laws for image generation and beats DiT at the same compute budget. This lesson builds the core mechanism.

> **【中文解读】** 扩散模型在时间维度上迭代采样（去噪步骤），VAR 在尺度维度上迭代——先预测 1x1 token，再 2x2，再 4x4，直到目标分辨率。2024 年论文证明 VAR 展现了 GPT 风格的 Scaling Law，在相同计算预算下超越 DiT。

> **【拓展：VAR 是生成模型的新范式】** VAR 将自回归思想从"下一个 token"扩展到"下一个尺度"，为图像生成开辟了新方向。它可能成为继扩散模型之后的下一代生成范式。

**Type:** Build / 构建型
**Languages:** Python (with PyTorch)
**Prerequisites:** Phase 7 Lesson 03 (Multi-Head Attention / 多头注意力), Phase 8 Lesson 06 (DDPM)
**Time:** ~90 minutes

## The Problem | 问题引入

Autoregressive generation dominated language modeling because it scales predictably: more compute, more parameters, lower perplexity, better outputs. Image generation had two main AR attempts before 2024: PixelRNN/PixelCNN (pixel-by-pixel) and DALL-E 1 / Parti / MuseGAN (token-by-token on VQ-VAE codes).

> 自回归生成在语言建模中占主导地位因为它可预测地扩展：更多计算、更多参数、更低困惑度、更好输出。2024 年前图像生成有两种主要 AR 尝试：PixelRNN/PixelCNN（逐像素）和 DALL-E 1 / Parti / MuseGAN（逐 token）。

Both suffered from a generation-order problem. Pixels and tokens are arranged in a 2D grid, but the AR model has to visit them in a 1D raster order. An early corner pixel has no idea what the image eventually becomes. Generation quality scaled worse than GPT-on-text and never reached diffusion-model quality at matched compute.

> 两者都受困于生成顺序问题。像素和 token 排列在 2D 网格中，但 AR 模型必须以 1D 光栅顺序访问。早期角落像素不知道图像最终会变成什么。生成质量的扩展不如 GPT，在相同计算量下从未达到扩散模型的质量。

VAR fixes the generation-order problem by changing what is being generated. Instead of predicting image tokens one by one in space, VAR predicts a whole image at increasing resolutions. Step 1: predict a 1x1 token (the overall image "summary"). Step 2: predict a 2x2 grid of tokens (coarser features). Step 3: predict a 4x4 grid. Step K: predict the final (H/8)x(W/8) grid.

> VAR 通过改变生成对象来修复生成顺序问题。不再逐空间预测图像 token，VAR 以递增分辨率预测整个图像。步骤 1：预测 1x1 token（全局摘要）。步骤 2：预测 2x2 token 网格。步骤 K：预测最终网格。

Each scale attends to all previous scales (causally in "scale order") and parallel within its own scale. The order problem disappears: the whole image at scale k is produced in one transformer pass.

> 每个尺度注意所有先前尺度（在"尺度顺序"上因果），在其自身尺度内并行。顺序问题消失了：尺度 k 的整个图像在一次 transformer 前向传播中产生。

> **【中文解读】** VAR（Visual Autoregressive）的核心创新：将图像生成的自回归顺序从"逐像素/逐 token"改为"逐尺度"。先预测 1x1 的全局摘要，再 2x2 的粗特征，再 4x4 的细节，直到目标分辨率。每个尺度内并行生成，消除了传统图像 AR 的"生成顺序问题"。2024 年论文证明 VAR 展现了类似 GPT 的 Scaling Law。

> **【拓展：VAR 与扩散模型的对比】** VAR 是继扩散模型之后最有潜力的图像生成新范式。优势：(1) 清晰的 Scaling Law——像 GPT 一样可预测扩展；(2) 生成过程结构化——先全局后局部，更符合人类感知；(3) 在相同计算预算下超越 DiT。挑战：需要多尺度 VQ-VAE tokenizer，训练更复杂。如果 Scaling Law 验证成功，VAR 可能成为下一代图像生成的基础架构。

## The Concept | 核心概念

### VQ-VAE Multi-Scale Tokenizer

> ### VQ-VAE 多尺度 Tokenizer

VAR needs a **multi-scale discrete tokenizer**. For an image x, it produces a sequence of progressively higher-resolution token grids:

> VAR 需要一个**多尺度离散 tokenizer**。对于图像 x，它产生一系列递增分辨率的 token 网格：

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

Each z_k uses the same codebook (typical size 4096-16384). The tokenization at each scale is not independent — it is trained so that summing the residuals at each scale reconstructs f:

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

This is a **residual VQ** variant. Scale k captures what scales 1..k-1 missed. Decoder takes the sum of all scale embeddings and produces the image.

> 这是一个**残差 VQ** 变体。尺度 k 捕获尺度 1..k-1 遗漏的内容。解码器将所有尺度嵌入求和并产生图像。

The multi-scale VQ tokenizer is trained once (like VQGAN) and then frozen. All the generative work is done by the autoregressive model on top.

> 多尺度 VQ tokenizer 训练一次（像 VQGAN）然后冻结。所有生成工作由上层的自回归模型完成。

### Next-Scale Prediction

> ### 下一尺度预测

The generative model is a transformer that sees tokens from all previous scales and predicts the tokens at the next scale.

> 生成模型是一个 transformer，看到所有先前尺度的 token 并预测下一尺度的 token。

Input sequence structure:
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

Position embeddings encode both scale index and spatial position within the scale. Attention is causal in scale order: token at scale k, position (i, j) can attend to all tokens at scales 1..k and to tokens at scale k itself that come earlier in whatever intra-scale order is used (VAR uses fixed positional attention with no intra-scale causality — all positions within a scale are predicted in parallel).

Training loss: at each scale k, predict the tokens z_k given all prior-scale tokens. Cross-entropy loss on the discrete VQ codes. Same structure as GPT except the "sequence" is now scale-structured.

### Generation

At inference:
```
generate z_1 = sample from p(z_1)                    # 1 token
generate z_2 = sample from p(z_2 | z_1)              # 4 tokens in parallel
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 tokens in parallel
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

For K = 10 scales, generation is 10 transformer forward passes. Each pass produces its entire scale in parallel — no per-token autoregression within a scale. For a 256x256 image this is roughly 10 passes vs DiT's 28-50.

> 对于 K = 10 个尺度，生成是 10 次 transformer 前向传播。每次产生整个尺度——尺度内无逐 token 自回归。256x256 图像约 10 次传播 vs DiT 的 28-50 次。

### Why Next-Scale Wins Over Next-Token

> ### 为什么下一尺度胜过下一 token

Three structural wins:

> 三个结构性优势：

1. **Coarse-to-fine aligns with natural image statistics.** Human visual perception and image datasets both exhibit scale-dependent regularities: low-frequency structure is stable and predictable; high-frequency detail is conditional on low-frequency content. Next-scale prediction exploits this.
   **从粗到细与自然图像统计一致。** 低频结构稳定可预测；高频细节依赖低频内容。
2. **Parallel generation within scale.** Unlike GPT-style token AR, VAR produces all tokens at a scale in one step. Effective generation length is log-scale instead of linear.
   **尺度内并行生成。** 不同于 GPT 风格的 token AR，VAR 一步产生整个尺度的所有 token。
3. **No generation order bias.** Tokens at scale k see all of scale k-1; there is no "left-of" or "above" bias that forces early tokens to commit before late context is available.
   **无生成顺序偏差。** 尺度 k 的 token 看到尺度 k-1 的全部。

### Scaling Law

> ### Scaling Law / 缩放定律

Tian et al. demonstrated that VAR follows a power-law scaling curve for FID on ImageNet — just like GPT does for perplexity. Doubling parameters or compute reliably halves error. This was the first image-generative model to exhibit this kind of scaling behavior as cleanly as language models. The result is that VAR-scale predictions become predictable from compute, not empirical guesses per architecture.

> Tian 等人证明 VAR 在 ImageNet 上的 FID 遵循幂律缩放曲线——就像 GPT 对困惑度一样。翻倍参数或计算量可靠地将误差减半。这是首个像语言模型一样清晰展现这种缩放行为的图像生成模型。

### Relationship to Diffusion

> ### 与扩散模型的关系

VAR and diffusion share the same data-compression story: both break the generation problem into a sequence of easier subproblems.

> VAR 和扩散共享相同的数据压缩故事：都将生成问题分解为更简单子问题的序列。

- Diffusion: gradually add noise, learn to undo one step.
  扩散：逐步加噪声，学习撤销一步。
- VAR: gradually add resolution, learn to predict the next scale.
  VAR：逐步加分辨率，学习预测下一尺度。

They are different axes through the problem. Both yield tractable conditional distributions. Empirically VAR is faster at inference (fewer passes, all parallel within a scale) and matches or beats DiT on class-conditional ImageNet. Text-conditional VAR (VARclip, HART) is an active research direction.

> 它们是穿过问题的不同轴。两者都产生可处理的条件分布。实验上 VAR 推理更快（更少传播，尺度内全并行），在类别条件 ImageNet 上匹配或超越 DiT。文本条件 VAR 是活跃研究方向。

## Build It | 动手实现

In `code/main.py` you will:
1. Build a tiny **multi-scale VQ tokenizer** on synthetic "image" data (2D Gaussian rings).
2. Train a **VAR-style transformer** to next-scale-predict the tokens.
3. Sample by calling the transformer 4 times (4 scales) and decoding.
4. Verify that scale-ordered training makes generation parallel within a scale.

This is a toy implementation. The point is to see the scale-structured attention mask and the parallel-within-scale generation actually working.

> 这是一个玩具实现。重点是看到尺度结构化的注意力掩码和尺度内并行生成真正工作。

## Ship It | 产出物

This lesson produces `outputs/skill-var-tokenizer-designer.md` — a skill for designing a multi-scale tokenizer: number of scales, scale ratios, codebook size, residual sharing, decoder architecture.

> 本课产生 `outputs/skill-var-tokenizer-designer.md`——设计多尺度 tokenizer 的 skill：尺度数、尺度比率、码本大小、残差共享、解码器架构。

## Exercises | 练习题

1. **Scale count ablation.** Train VAR with 4, 6, 8, 10 scales. Measure reconstruction quality vs number of autoregressive passes. More scales = finer residuals = better quality but more passes.

2. **Codebook size.** Train tokenizers with codebook sizes 512, 4096, 16384. Larger codebooks give better reconstruction but harder prediction. Find the knee.

3. **Parallel-within-scale check.** For a trained VAR, measure the attention pattern explicitly. Within scale k, does the model attend to cross-scale positions but not intra-scale? Verify the mask implementation.

4. **VAR vs DiT scaling.** For the same ImageNet class-conditional task, train VAR and DiT at matched param budgets (e.g., 33M, 130M, 458M). Plot FID vs compute. VAR should pull ahead of DiT at each size — reproduce the paper's result at small scale.

5. **Text conditioning.** Extend VAR to take a text embedding (CLIP pooled) as an extra conditioning input via adaLN. This is the HART recipe. How much does FID improve on text-aligned sampling?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| VAR | "Visual AutoRegressive" | Image generation by next-scale prediction over a pyramid of VQ token grids |
| Next-scale prediction | "Predict coarser, then finer" | The model predicts tokens at increasing resolution scales, conditioning on all previous scales |
| Multi-scale VQ tokenizer | "Residual VQ" | VQ-VAE that produces K token grids of increasing resolution, with decoder summing all scales |
| Scale k | "Pyramid level k" | One of K resolution levels, from 1x1 at k=1 up to (H/p)x(W/p) at k=K |
| Parallel-within-scale | "One forward per scale" | All tokens at scale k are predicted in one transformer pass, not autoregressively |
| Causal-across-scales | "Scale-ordered attention" | Token at scale k can attend to all of scales 1..k but not scales k+1..K |
| Residual VQ | "Additive tokenization" | Each scale's tokens encode the residual left by lower scales; decoder sums all scale embeddings |
| VAR scaling law | "Image GPT scaling" | FID follows a predictable power law in compute, like language models' perplexity |
| HART | "Hybrid VAR + text" | Text-conditional VAR variant combining MaskGIT-style iterative decoding with VAR's scale structure |
| Scale position embedding | "(scale, row, col) triple" | Positional encoding carries both the scale index and spatial coordinates within the scale |

## Further Reading | 延伸阅读

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) — the VAR paper, canonical reference
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) — DiT, the diffusion comparison baseline
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) — VQGAN, the tokenizer family VAR's multi-scale tokenizer extends
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) — VQ-VAE, the foundation of discrete image tokenization
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) — text-conditional VAR
