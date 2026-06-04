# Any-Resolution Vision: Patch-n'-Pack and NaFlex | 任意分辨率视觉：Patch-n'-Pack 与 NaFlex

> Real images are not 224x224 squares. A receipt is 9:16, a chart is 16:9, a medical scan might be 4096x4096, a mobile screenshot is 9:19.5. The pre-2024 VLM answer — resize everything to a fixed square — threw away the signal that makes OCR, document understanding, and high-resolution scene parsing work. NaViT (Google, 2023) showed you could pack variable-resolution patches into a single transformer batch with block-diagonal masking. Qwen2-VL's M-RoPE (2024) dropped absolute positional tables entirely. LLaVA-NeXT's AnyRes tiled high-resolution images into a base + sub-images. SigLIP 2's NaFlex variant (2025) is now the default encoder for open VLMs that want a single checkpoint to serve every aspect ratio. This lesson implements patch-n'-pack end to end.

> **【中文解读】** 真实世界的图像不是 224x224 的正方形——收据是 9:16，图表是 16:9，医疗影像可能 4096x4096。2024 年前 VLM 统一将图像缩放为固定正方形，这会丢失 OCR、文档理解和高分辨率场景解析的关键信息。本课讲解如何让 Transformer 以原始分辨率处理任意宽高比的图像。

> **【拓展：金融文档场景的分辨率挑战】** 在金融场景中，报表、发票、合同等文档的宽高比千差万别。固定正方形缩放会导致文字变形、OCR 精度下降。AnyRes 和 Patch-n'-Pack 技术让 VLM 能以原始比例理解这些文档，是构建金融文档理解系统的关键技术基础。

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言：Python（标准库，补丁打包器 + 块对角掩码）**
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置：阶段12第01课（ViT补丁）、阶段12第05课（LLaVA）**
**Time:** ~120 minutes  | **时长：约120分钟**

## Learning Objectives  | 学习目标

- Pack patches from a batch of variable-resolution images into one sequence and build the block-diagonal attention mask.  | 将不同分辨率图像的补丁打包到一个序列中，构建块对角注意力掩码。
- Pick between AnyRes tiling (LLaVA-NeXT), NaFlex (SigLIP 2), and M-RoPE (Qwen2-VL) for a given task.  | 根据任务选择 AnyRes 切片（LLaVA-NeXT）、NaFlex（SigLIP 2）或 M-RoPE（Qwen2-VL）。
- Compute token budgets for OCR, charts, and photography without resizing.  | 计算无缩放情况下 OCR、图表和摄影的 token 预算。
- Name the three failure modes of square-resize: squished text, cropped content, wasted tokens on padding.  | 列举正方形缩放的三种失败模式：文字压缩、内容裁剪、padding 浪费。

## The Problem  | 问题背景

Transformers expect a sequence. A batch is a stack of sequences the same length. If your images are 224x224, you get 196 patch tokens every time, padding not required, job done. Train on 224, infer on 224, never think about resolution again.

The world does not cooperate. Documents are portrait (8.5x11 inches, 2:3-ish). Chart screenshots are landscape (16:9). Receipts are tall and thin (1:3). Medical imaging ships at 2048x2048 or larger. Mobile device screenshots are 1170x2532 (0.46:1).

Three pre-2024 options and why each fails:

1. Resize to a fixed square (224x224 or 336x336). The squish distorts text and faces. The downscale destroys chart labels and OCR content. Standard practice until LLaVA-1.5.
2. Crop to a fixed aspect ratio. You throw away most of the image, and picking the crop location is its own vision problem.
3. Pad to the longest side. Fixes distortion but wastes 50%+ of tokens on padding for portrait images. Quadratic attention cost on all those pad tokens.

> **【中文解读】** Transformer 期望固定长度的序列。真实世界的图像宽高比各异，2024 年前有三种做法：(1) 缩放为正方形——文字变形、OCR 内容丢失；(2) 裁剪——丢弃大量内容；(3) 填充——竖屏图像浪费 50%+ 的 token 在 padding 上，注意力计算成本二次增长。

The 2024-2025 answer: let the transformer eat patches at the image's native resolution, and figure out how to pack a heterogeneous batch into one sequence without wasted compute.

> **【中文解读】** 2024-2025 年的答案：让 Transformer 直接以原始分辨率"吃"补丁，然后把不同分辨率的批次打包成一个序列，不浪费任何计算。

## The Concept  | 核心概念

### NaViT and patch-n'-pack  | NaViT 与补丁打包

NaViT (Dehghani et al., 2023) was the paper that showed this works at scale. The idea is mechanical:

1. For each image in the batch, compute its native patch grid at a chosen patch size (say 14).  | 对批次中每张图像，以指定补丁大小（如14）计算原始补丁网格。
2. Flatten each image's patches into its own variable-length sequence.  | 将每张图像的补丁展平为各自的可变长度序列。
3. Concatenate all images' patches into one long sequence for the batch.  | 将所有图像的补丁拼接成一个长序列。
4. Build a block-diagonal attention mask so image A's patches only attend within image A.  | 构建块对角注意力掩码，使图像A的补丁只在自身内部做注意力计算。
5. Carry per-patch position information (2D RoPE or fractional position embeddings).  | 为每个补丁携带位置信息（2D RoPE 或分数位置嵌入）。

A batch of three images at 336x336 (576 tokens), 224x224 (256 tokens), and 448x336 (768 tokens) becomes one 1600-token sequence with a 1600x1600 block-diagonal mask. No padding. No wasted compute. The transformer handles arbitrary aspect ratios.

NaViT also introduced fractional patch dropping during training — drop 50% of patches at random across the batch — which both regularizes and speeds training. SigLIP 2 inherited this.

> **【中文解读】** NaViT 的核心：三张不同分辨率的图像（576 + 256 + 768 = 1600 个 token）被打包成一个序列，用块对角掩码防止跨图像注意力。零 padding，零浪费。NaViT 还引入了训练时随机丢弃 50% 补丁的技术，既正则化又加速训练。

### AnyRes (LLaVA-NeXT)  | AnyRes 切片策略

LLaVA-NeXT's AnyRes is the pragmatic alternative. Given a high-resolution image and a fixed encoder (CLIP or SigLIP at 336), tile the image:

1. Pick a grid layout from a predefined set — (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), etc. — that best fits the image's aspect ratio.  | 从预定义集合中选择最匹配图像宽高比的网格布局。
2. Tile the full image into the grid; each tile becomes a 336x336 crop.  | 将图像按网格切片，每片裁剪为 336x336。
3. Also produce a thumbnail: the whole image resized to 336x336 as a global-context token.  | 同时生成缩略图：整张图缩放到 336x336 作为全局上下文 token。
4. Encode every tile through the frozen 336-encoder. Concatenate the tile tokens + thumbnail tokens.  | 每个切片通过冻结的 336 编码器，拼接切片 token + 缩略图 token。

For a 672x672 image at 2x2 grid plus thumbnail: 4 * 576 + 576 = 2880 visual tokens. Expensive but effective — the LLM sees both local detail and global context.

AnyRes is the route of choice when your encoder is frozen and only supports one resolution. It explodes token count for large images (a 1344x1344 image at 4x4 grid is 9216 + 576 ≈ 9800 tokens, which fills most of a 8k LLM context).

> **【中文解读】** AnyRes 适用于编码器被冻结且只支持单一分辨率的情况。代价是大图像的 token 数激增（1344x1344 在 4x4 网格下约 9800 个 token，几乎填满 8k LLM 上下文）。它的优势是 LLM 同时看到局部细节和全局上下文。

### M-RoPE (Qwen2-VL)  | M-RoPE 多模态旋转位置编码

Qwen2-VL introduced Multimodal Rotary Position Embedding. Instead of NaViT's fractional positions or AnyRes's tile-and-thumbnail, each patch carries a 3D position (temporal, height, width). The query/key rotations handle arbitrary H, W, and temporal length.

M-RoPE ships native dynamic resolution without retraining. At inference you feed any HxW image, the patch embedder produces H/14 x W/14 tokens, each token gets its (t=0, r=row, c=col) position, RoPE rotates attention with the right frequencies, done. Qwen2.5-VL and Qwen3-VL continue this. InternVL3's V2PE is the same idea with variable encoding per modality.

Unlike AnyRes, M-RoPE is O(H x W / P^2) tokens at native resolution — no multiplicative tile overhead. Unlike NaViT, it still expects a single image per forward. Batching across resolutions still needs patch-n'-pack on top.

> **【中文解读】** M-RoPE 为每个补丁赋予三维位置（时间、高度、宽度），用旋转位置编码处理任意 H、W 和时间长度。推理时直接输入任意 HxW 图像，产生 H/14 x W/14 个 token，无需重训练。与 AnyRes 不同，M-RoPE 的 token 数是 O(HxW/P^2)，没有切片的乘法开销。

### NaFlex (SigLIP 2)  | NaFlex 灵活分辨率

NaFlex is the SigLIP 2 checkpoint's native-flex mode. A single model serves multiple sequence lengths (256, 729, 1024 tokens) at inference. Internally it uses NaViT-style patch-n'-pack during training and absolute fractional positions per patch. The selling point: one checkpoint, pick your token budget at inference based on the task.

For a semantic task (classification, retrieval), 256 tokens. For OCR or chart understanding, 1024 tokens. No retraining.

> **【中文解读】** NaFlex 的核心卖点：一个 checkpoint，推理时按任务选择 token 预算。语义任务用 256 token，OCR 或图表理解用 1024 token，无需重训练。这非常适合构建成本敏感的多模态服务——按需分配 token 预算。

### The packing mask  | 打包掩码

The block-diagonal mask is where most implementations stumble. For a packed sequence of length `N_total` covering images `i=0..B-1` with lengths `n_i`, the mask `M` of shape `(N_total, N_total)` is 1 if both indices fall in the same image's block, else 0. You can build it from a cumulative length list:

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

This is one line in PyTorch with `torch.block_diag` or an explicit gather. FlashAttention's variable-length path (`cu_seqlens`) skips the mask entirely and attends within sequences using the cumulative-length tensor directly — ~10x faster than a dense mask for typical batches.

> **【中文解读】** 块对角掩码确保每张图像的补丁只关注自身，不会"看到"同批次中其他图像的补丁。FlashAttention 的可变长度路径（`cu_seqlens`）直接用累积长度张量做注意力，跳过了密集掩码，速度约快 10 倍。

### Token budgets  | Token 预算

Pick your strategy by task:

- OCR / documents: 1024-4096 tokens. SigLIP 2 NaFlex at 1024, or AnyRes 3x3 + thumbnail.  | OCR/文档：1024-4096 token。
- Charts and UI: 729-1024 tokens at 384-448 native. Qwen2.5-VL dynamic resolution with max pixels cap.  | 图表和UI：729-1024 token。
- Natural photos: 256-576 tokens is fine. The downstream LLM sees enough. Pay for tokens where content density is high.  | 自然照片：256-576 token 足够。
- Video: 64-128 tokens per frame after spatial pooling, 2-8 FPS. Lesson 12.17 covers this.  | 视频：每帧 64-128 token，2-8 FPS。

The 2026 production rule: pick a per-task max-pixels cap, encode at native aspect ratio up to that cap, pack the batch, and skip padding. Qwen2.5-VL exposes `min_pixels` and `max_pixels` for exactly this knob.

> **【拓展：Token 预算与成本优化】** 在生产环境中，token 预算直接影响 API 成本和延迟。为 OCR 任务分配 1024+ token 是必要的（文字密度高），但自然照片用 256 token 就够了。按任务动态调整分辨率是 2026 年 VLM 部署的最佳实践。

## Use It  | 动手实践

`code/main.py` implements patch-n'-pack for a heterogeneous batch of images with integer pixel coordinates. It:

- Takes a list of (H, W) image sizes.  | 接收 (H, W) 图像尺寸列表
- Computes each image's patch sequence length at patch size 14.  | 计算每张图像在补丁大小14下的序列长度
- Packs them into one sequence of total length `sum(n_i)`.  | 打包为总长度 `sum(n_i)` 的序列
- Builds the block-diagonal attention mask (dense, for clarity).  | 构建块对角注意力掩码（密集格式，便于理解）
- Compares the packed cost vs square-resize and AnyRes tiling.  | 对比打包成本 vs 正方形缩放和 AnyRes 切片
- Prints a token budget table for a mixed batch (receipt, chart, screenshot, photo).  | 打印混合批次的 token 预算表

Run it. The numbers that drop out are the reason every 2026 open VLM uses patch-n'-pack.

## Ship It  | 部署上线

This lesson produces `outputs/skill-resolution-budget-planner.md`. Given a mixed-aspect-ratio workload (OCR, charts, photos, video frames) and a total-token budget, it picks the right strategy (NaFlex, AnyRes, M-RoPE, or fixed-square) and emits a per-request configuration. Use this skill when you are sizing a VLM for a product — it prevents the silent 10x token blowup that kills latency budgets.

> **【中文解读】** 本课产出分辨率预算规划工具。给定混合宽高比工作负载和总 token 预算，自动选择最优策略（NaFlex/AnyRes/M-RoPE/固定正方形），防止因分辨率不当导致的 10 倍 token 爆炸。

## Exercises  | 练习题

1. A receipt is 600x1500 (1:2.5). At patch size 14, how many native-resolution tokens? How many after square-resize to 336? Which loses more OCR accuracy in practice?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. Build the block-diagonal mask for a batch of four images with lengths 256, 576, 729, 1024. Verify the attention matrix is 2585x2585 and has exactly `256^2 + 576^2 + 729^2 + 1024^2` non-zero entries.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. For a 1792x896 image at patch 14, compare: (a) square-resize to 336 then encode, (b) AnyRes 2x1 + thumbnail, (c) M-RoPE at native. Which uses fewest tokens? Which preserves most detail?
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Implement fractional patch dropping: given a packed sequence, drop 50% of tokens uniformly at random, and update the block-diagonal mask accordingly. Measure the mask's sparsity change.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Read Section 3.2 of the Qwen2-VL paper (arXiv:2409.12191). Describe in two sentences what `min_pixels` and `max_pixels` control and why both bounds matter.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Further Reading  | 延伸阅读

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304) | NaViT 任意分辨率训练
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) | Qwen2-VL 多模态旋转位置编码
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) | 构建 VLM 的关键因素
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) | SigLIP 2 NaFlex
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) | Qwen2.5-VL 技术报告
