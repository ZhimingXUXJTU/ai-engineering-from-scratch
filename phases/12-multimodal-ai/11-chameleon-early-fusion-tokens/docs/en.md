# Chameleon and Early-Fusion Token-Only Multimodal Models | Chameleon 早期融合纯 Token 多模态模型

> Every VLM we have seen so far keeps images and text separate. Visual tokens come from a vision encoder, flow into a projector, then meet text inside the LLM. The vision and text vocabularies never overlap. Chameleon (Meta, May 2024) asked: what if they did? Train a VQ-VAE that turns an image into a sequence of discrete tokens from a shared vocabulary. Every multimodal document is now one sequence — text tokens and image tokens interleaved, a single autoregressive loss. Side effect: the model can generate mixed-modality outputs — alternating text and image tokens in a single inference call. This lesson reads the early-fusion thesis and builds a toy version end to end.

> **【中文解读】** Chameleon（Meta，2024年5月）提出了一种激进的多模态方法：用 VQ-VAE 将图像转换为离散 token，与文本 token 共享同一个词汇表，用单一的自回归损失训练。这样模型既能理解又能生成混合模态内容。

> **【拓展：早期融合 vs 后期融合】** 之前所有 VLM（LLaVA、BLIP-2、Qwen-VL）都保持图像和文本分离。Chameleon 的"早期融合"意味着图像和文本从一开始就在同一个空间中处理，模型可以自然地交替输出文本和图像。这是统一生成模型家族（Emu3、Show-o、Janus-Pro）的起点。

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·05（LLaVA 后期融合方案）、Phase 8（VQ-VAE 离散表示）、Phase 7（Transformer next-token 训练）。Chameleon 是"反 LLaVA"的另一个极端：所有模态都用 next-token loss。
> 💡 **【类比】** Chameleon = "世界语"。LLaVA = 翻译机（视觉编码器把图片翻成 LLM 能懂的语言）；Chameleon = 世界语（图片和文本都用同一种人造语言，模型不用翻译）。世界语的好处是模型可以无缝交替生成文本和图片；坏处是每种模态都要离散化（VQ-VAE 给图片"造词"），信息损失大。

## Learning Objectives  | 学习目标

- Explain why a shared vocabulary + single loss changes what the model can do.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力。
- Describe how a VQ-VAE tokenizes an image into a discrete sequence compatible with a transformer's next-token objective.
  > 描述 VQ-VAE 如何将图像分词为与 Transformer 下一 token 目标兼容的离散序列。
- Name Chameleon's training-stability tricks: QK-Norm, dropout placement, LayerNorm ordering.
  > 列举 Chameleon 的训练稳定性技巧：QK-Norm、Dropout 位置、LayerNorm 顺序。
- Compare Chameleon vs BLIP-2's Q-Former approach and describe when each is the right choice.
  > 比较 Chameleon 与 BLIP-2 的 Q-Former 方案，描述各自适合的场景。

## The Problem  | 问题背景

Adapter-based VLMs (LLaVA, BLIP-2, Qwen-VL) treat text and image as two different things. A text token goes through `embed(text_token)`; an image goes through `visual_encoder(image) → projector → ... pseudo_tokens`. The model has two input paths that merge partway in.

> 适配器式 VLM（LLaVA、BLIP-2、Qwen-VL）将文本和图像视为两种不同的东西。文本 token 通过 `embed(text_token)`；图像通过 `visual_encoder(image) → projector → ... pseudo_tokens`。模型有两条在中间合并的输入路径。

Three consequences:

> 三个后果：

1. The LLM can only consume images, not emit them. Output is text only.
   中文翻译：LLM 只能消费图像，不能生成图像。输出只能是文本。
2. Mixed-modality documents (alternating paragraphs and images, as in an article) are awkward — you either parse the multimodal input outside the model or chain generations.
   中文翻译：混合模态文档（段落和图像交替，如文章）很别扭——你要么在模型外解析多模态输入，要么链式生成。
3. Distributional mismatch. Visual tokens and text tokens live in different regions of the hidden space, creating subtle alignment issues.
   中文翻译：分布不匹配。视觉 token 和文本 token 位于隐藏空间的不同区域，造成微妙的对齐问题。

Chameleon rejects the premise: images are just sequences of discrete tokens from a shared vocabulary. Train the model on interleaved documents, one loss, one autoregressive decoder, and you unlock mixed-modality generation for free.

> Chameleon 拒绝了这一前提：图像只是共享词汇表中离散 token 的序列。在交织文档上训练模型，一个损失函数，一个自回归解码器，即可免费解锁混合模态生成。

## The Concept  | 核心概念

> **【中文解读】** Chameleon（Meta）采用早期融合策略：图像和文本都离散化为统一 token 序列，用同一个 Transformer 处理。图像通过 VQGAN 编码为离散 token，与文本 token 在同一词表中。这是统一多模态理解的极致实现。

> **【拓展：早期融合 vs 晚期融合】** 早期融合（Chameleon）将多模态统一到同一 token 空间，理论上更优雅但训练成本高。晚期融合（LLaVA）保持视觉和语言模型独立性通过桥接层连接，训练更高效。


### VQ-VAE as image tokenizer

The tokenizer is a vector-quantized variational autoencoder. The architecture:

> 分词器是一个向量量化变分自编码器。架构如下：

- Encoder: CNN + ViT that maps image to a spatial feature map, say 32x32 features of dim 256.
  中文翻译：编码器：CNN + ViT 将图像映射为空间特征图，如 32x32 个维度为 256 的特征。
- Codebook: a learned vocabulary of K vectors (Chameleon uses 8192), also dim 256.
  中文翻译：码本：K 个学习向量的词汇表（Chameleon 使用 8192 个），也是 256 维。
- Quantization: for each spatial feature, look up the nearest codebook entry by L2 distance. Replace the continuous feature with the integer index.
  中文翻译：量化：对每个空间特征，用 L2 距离查找最近的码本条目。用整数索引替换连续特征。
- Decoder: CNN that takes quantized features back to pixels.
  中文翻译：解码器：CNN 将量化特征重建为像素。

Training: VAE reconstruction loss + commitment loss + codebook loss. The codebook indices form a discrete alphabet for images.

> 训练：VAE 重建损失 + 承诺损失 + 码本损失。码本索引构成图像的离散字母表。

For Chameleon: one image becomes 32*32 = 1024 tokens drawn from a vocabulary of 8192. Concatenate with text tokens (from the LLM's BPE vocabulary, say 32000). Final vocabulary: 40192. The transformer sees one sequence, one loss.

> 对于 Chameleon：一张图像变成 32*32 = 1024 个 token，来自 8192 的词汇表。与文本 token（来自 LLM 的 BPE 词汇表，如 32000）拼接。最终词汇表：40192。Transformer 看到一个序列，一个损失。

### The shared vocabulary

Chameleon's vocabulary combines text tokens, image tokens, and modality separators. Each token has a single ID. The input embedding layer maps every ID to a D-dim hidden vector. The output projection maps hidden back to vocab logits. Softmax picks the next token, whatever modality.

> Chameleon 的词汇表结合了文本 token、图像 token 和模态分隔符。每个 token 有一个唯一的 ID。输入嵌入层将每个 ID 映射到 D 维隐藏向量。输出投影将隐藏向量映射回词汇表 logits。Softmax 选择下一个 token，无论什么模态。

Separators matter: `<image>` and `</image>` tags bracket the image-token sequence. At generation time, if the model emits `<image>`, downstream software knows the next 1024 tokens are VQ indices to send to the decoder for pixel rendering.

> 分隔符很重要：`<image>` 和 `</image>` 标签包裹图像 token 序列。生成时，如果模型输出 `<image>`，下游软件就知道接下来的 1024 个 token 是 VQ 索引，需要发送给解码器进行像素渲染。

### Mixed-modality generation

Inference is next-token prediction in the shared vocabulary. Example prompt: "Draw a cat and describe it." Chameleon emits:

> 推理是共享词汇表中的下一 token 预测。示例提示："画一只猫并描述它。"Chameleon 输出：

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

The model picks the order autonomously — it may produce image then text, text then image, or interleave. Same decoder, same loss.

> 模型自主选择顺序——可以先图像后文本、先文本后图像，或交替输出。同一个解码器，同一个损失。

Compare to adapter VLMs where generation is text-only. Chameleon reopens the question of model output modalities.

> 与适配器 VLM（只能生成文本）对比。Chameleon 重新打开了模型输出模态的问题。

### Training stability — QK-Norm, dropout, LayerNorm ordering

Early-fusion training is unstable at scale. Chameleon's paper documents three tricks:

> 早期融合训练在大规模时不稳定。Chameleon 论文记录了三个技巧：

- QK-Norm. Apply LayerNorm to the query and key projections inside attention, before the dot product. Prevents logit magnitude explosion at depth. Used by multiple post-2024 large models.
  中文翻译：QK-Norm。在注意力内部的 query 和 key 投影上应用 LayerNorm，在点积之前。防止深度上的 logit 幅度爆炸。被多个 2024 年后的大模型使用。
- Dropout placement. Dropout after every residual-add, not just after attention and MLP. More regularization required when gradients from image tokens can dominate.
  中文翻译：Dropout 位置。在每次残差加法后放 Dropout，不仅是注意力和 MLP 后。当图像 token 的梯度可能主导时需要更多正则化。
- LayerNorm ordering. Pre-LN on the residual branch (standard), plus an extra LN on the skip connection of the last block. Stabilizes final-layer gradient flow.
  中文翻译：LayerNorm 顺序。残差分支上的 Pre-LN（标准做法），加上最后一个块跳跃连接上的额外 LN。稳定最后一层的梯度流。

Without these tricks, 34B-param Chameleon training diverged at multiple checkpoints. With them, it converges. The training recipe is as much of the contribution as the architecture.

> 没有这些技巧，340 亿参数的 Chameleon 训练在多个检查点发散。有了它们，训练收敛。训练配方与架构本身同等重要。

### The tokenizer's reconstruction ceiling

VQ-VAE is lossy. At 8192 codebook entries and 1024 tokens per 512x512 image, reconstruction PSNR caps around 26-28 dB. This is enough for recognizable image gen but visibly worse than continuous-space diffusion (Stable Diffusion 3 achieves 32+ dB).

> VQ-VAE 是有损的。8192 个码本条目和每张 512x512 图像 1024 个 token，重建 PSNR 上限约 26-28 dB。足以生成可识别的图像，但明显差于连续空间扩散（Stable Diffusion 3 达到 32+ dB）。

The tokenizer is the bottleneck. Better tokenizers (MAGVIT-v2, IBQ, SBER-MoVQGAN) lift the ceiling. Emu3 (Lesson 12.12) achieves SDXL-quality generation via a better tokenizer alone.

> 分词器是瓶颈。更好的分词器（MAGVIT-v2、IBQ、SBER-MoVQGAN）能提高上限。Emu3（第 12.12 课）仅通过更好的分词器就实现了 SDXL 质量的生成。

### Chameleon vs BLIP-2 / LLaVA

Chameleon (early fusion, shared vocab):
- One loss, one decoder.
  中文翻译：一个损失，一个解码器。
- Generates mixed-modality output.
  中文翻译：生成混合模态输出。
- Tokenizer is the quality ceiling.
  中文翻译：分词器是质量上限。
- Expensive: VQ-VAE decoder per generated image on inference path.
  中文翻译：昂贵：推理路径上每张生成图像都需要 VQ-VAE 解码器。

BLIP-2 / LLaVA (late fusion, separate towers):
- Vision in, text out only.
  中文翻译：视觉输入，仅文本输出。
- Reuses pretrained LLM.
  中文翻译：复用预训练 LLM。
- No tokenizer bottleneck for understanding.
  中文翻译：理解没有分词器瓶颈。
- Cheap: single forward pass.
  中文翻译：便宜：单次前向传播。

Pick by task. If you need image generation, Chameleon family. If you only need understanding, adapter-VLM is simpler and reuses more pretrained compute.

> 按任务选择。如果需要图像生成，选 Chameleon 系列。如果只需要理解，适配器 VLM 更简单且复用更多预训练计算。

### Fuyu and AnyGPT

Fuyu (Adept, 2023) is a related approach: skip the separate vision encoder entirely, feed raw image patches through the LLM's input projection as if they were tokens, no tokenizer. Simpler than Chameleon, loses the shared-vocab output generation.

> Fuyu（Adept，2023）是一种相关方法：完全跳过独立的视觉编码器，将原始图像 patch 通过 LLM 的输入投影，就像它们是 token 一样，没有分词器。比 Chameleon 更简单，但失去了共享词汇表的输出生成。

AnyGPT (Zhan et al., 2024) extends Chameleon to four modalities: text, image, speech, music. Same VQ-VAE trick for each, shared transformer. Any-to-any generation. Covered more in Lesson 12.16.

> AnyGPT（Zhan 等人，2024）将 Chameleon 扩展到四种模态：文本、图像、语音、音乐。每种模态使用相同的 VQ-VAE 技巧，共享 Transformer。任意到任意生成。第 12.16 课详细介绍。


> **【拓展：早期融合的训练挑战】** 早期融合需要将图像和文本统一离散化，对图像 tokenizer 的质量要求极高。Meta 的 Chameleon 使用 8192 码本的 VQGAN，在 ImageNet 重建质量（rFID 约 5.0）和文本兼容性之间做了精心权衡。


## Use It  | 动手实践

`code/main.py` builds a toy end-to-end early-fusion model:

> `code/main.py` 构建了一个端到端的玩具早期融合模型：

- A tiny VQ-VAE-style quantizer that maps 8x8 patches to codebook indices (K=16).
  中文翻译：一个微型 VQ-VAE 风格的量化器，将 8x8 patch 映射到码本索引（K=16）。
- A shared vocabulary of (text ids 0..31) + (image ids 32..47) + (separators 48, 49).
  中文翻译：共享词汇表（文本 id 0..31）+（图像 id 32..47）+（分隔符 48, 49）。
- A toy autoregressive decoder (bigram table) trained on synthetic captions + image-token sequences.
  中文翻译：一个玩具自回归解码器（二元组表），在合成描述 + 图像 token 序列上训练。
- Sampling loop that emits alternating text + image tokens given a prompt.
  中文翻译：采样循环，给定提示后输出交替的文本 + 图像 token。

The code intentionally keeps the transformer tiny (bigrams) so you can trace the signal flow end to end.

> 代码故意将 Transformer 保持得非常小（二元组），以便你可以端到端地追踪信号流。

## Ship It  | 部署上线

This lesson produces `outputs/skill-tokenizer-vs-adapter-picker.md`. Given a product spec (understand only vs understand + generate, required image quality, cost budget), it picks between Chameleon-family (early fusion) and LLaVA-family (late fusion) and justifies with quantitative rules of thumb.

> 本课产出 `outputs/skill-tokenizer-vs-adapter-picker.md`。给定产品规格（仅理解 vs 理解+生成、所需图像质量、成本预算），它在 Chameleon 系列（早期融合）和 LLaVA 系列（晚期融合）之间选择，并用定量经验法则进行论证。

## Exercises  | 练习题

1. Chameleon uses K=8192 codebook entries and 1024 tokens per 512x512 image. Estimate the compression ratio vs a 24-bit RGB image. Is it lossy? How lossy?
   中文翻译：Chameleon 使用 K=8192 个码本条目和每张 512x512 图像 1024 个 token。估算相对于 24 位 RGB 图像的压缩比。有损吗？损失多少？

2. A 4K image (3840x2160) at the same VQ-VAE density produces how many image tokens? Can a Chameleon-style model generate a 4K image in one inference call? What breaks first — context, tokenizer quality, or KV cache?
   中文翻译：4K 图像（3840x2160）在相同 VQ-VAE 密度下产生多少图像 token？Chameleon 风格的模型能一次推理调用生成 4K 图像吗？什么先崩溃——上下文、分词器质量还是 KV 缓存？

3. Implement QK-Norm in pure Python. Given a 64-dim query and key, show the dot product before and after LayerNorm. Why is magnitude control important at depth?
   中文翻译：用纯 Python 实现 QK-Norm。给定 64 维的 query 和 key，展示 LayerNorm 前后的点积。为什么在深度网络中幅度控制很重要？

4. Read Chameleon Section 2.3 on training stability. Describe the exact failure mode the paper observed at 34B without QK-Norm. What was the "norm explosion" signature?
   中文翻译：阅读 Chameleon 第 2.3 节关于训练稳定性。描述论文在 340 亿参数下不使用 QK-Norm 观察到的确切失败模式。"范数爆炸"的特征是什么？

5. Extend the toy decoder to emit a mixed-modality response given a text-only prompt. Measure how often the model picks image-first vs text-first given training-data distribution 60% text-first / 40% image-first.
   中文翻译：扩展玩具解码器，使其能在给定纯文本提示时发出混合模态响应。在训练数据分布为 60% 文本优先 / 40% 图像优先时，测量模型选择图像优先 vs 文本优先的频率。

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Further Reading  | 延伸阅读

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  中文翻译：Chameleon 混合模态早期融合基础模型。
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  中文翻译：CM3 论文，Chameleon 的前身。
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  中文翻译：CM3Leon，Chameleon 的近亲。
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  中文翻译：AnyGPT，扩展到四种模态。
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  中文翻译：Fuyu-8B 博客，跳过视觉编码器的方案。
