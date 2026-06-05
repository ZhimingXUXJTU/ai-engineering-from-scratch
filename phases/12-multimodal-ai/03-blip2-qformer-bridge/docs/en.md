# From CLIP to BLIP-2 — Q-Former as Modality Bridge | 从 CLIP 到 BLIP-2：Q-Former 模态桥接

> CLIP aligns image and text but cannot generate captions, answer questions, or hold a conversation. BLIP-2 (Salesforce, 2023) solved that with a small trainable bridge: 32 learnable query vectors attend over a frozen ViT's features via cross-attention, then slot directly into a frozen LLM's input stream. 188M parameters of bridge connected an 11B LLM to a ViT-g/14. Every adapter-based VLM through 2026 — MiniGPT-4, InstructBLIP, LLaVA's cousins — is a descendant. This lesson reads the Q-Former's architecture, explains its two-stage training, and builds a toy version that feeds visual tokens into a frozen text decoder.

> **【中文解读】** CLIP 只能对齐图文但无法生成。BLIP-2 用32个可学习查询向量通过交叉注意力桥接冻结的 ViT 和 LLM，仅188M参数就能将视觉特征注入11B的语言模型。

> **【拓展：Q-Former→多模态架构演进】** Q-Former 是"冻结视觉编码器+冻结LLM+轻量桥接"范式的开创者，MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

## Learning Objectives | 学习目标

- Explain why a trainable bottleneck between a frozen vision encoder and frozen LLM beats end-to-end finetuning in cost and stability.
  中文翻译：解释为什么在冻结视觉编码器和冻结 LLM 之间的可训练瓶颈在成本和稳定性上优于端到端微调。
- Implement a cross-attention block where a fixed set of learnable queries attend to external image features.
  中文翻译：实现一个交叉注意力块，其中一组固定的可学习查询关注外部图像特征。
- Walk through BLIP-2's two-stage pretraining: representation (ITC + ITM + ITG) then generative (LM loss with frozen decoder).
  中文翻译：梳理 BLIP-2 的两阶段预训练：表示学习（ITC + ITM + ITG）然后生成学习（冻结解码器的 LM 损失）。
- Compare Q-Former to the simpler MLP projector used in LLaVA and argue when each choice wins.
  中文翻译：比较 Q-Former 和 LLaVA 使用的更简单的 MLP 投影器，论证各自的优势场景。

## The Problem | 问题引入

You have a frozen ViT that produces 256 patch tokens of dim 1408 per image. You have a frozen 7B LLM that expects token embeddings of dim 4096. The obvious bridge — a linear layer from 1408 to 4096 — works, but feeding all 256 patch tokens into the LLM's context costs 256 extra tokens per image. Over a batch of 32 images that is 8192 tokens consumed by the visual modality alone.

> 你有一个冻结的 ViT，每张图像产生 256 个维度为 1408 的 patch token。你有一个冻结的 7B LLM，期望维度为 4096 的 token 嵌入。显而易见的桥接——从 1408 到 4096 的线性层——可行，但将所有 256 个 patch token 喂入 LLM 的上下文需要每张图像额外消耗 256 个 token。32 张图像的批次仅视觉模态就消耗了 8192 个 token。

The BLIP-2 question: can you compress the 256-token image representation into far fewer tokens (say 32) while preserving enough information for the LLM to caption, answer questions, and reason about the image? And can you train this bridge without touching the frozen backbones, keeping the training cost at just the bridge's parameters?

> BLIP-2 的问题：你能否将 256 token 的图像表示压缩到远少于 32 个 token，同时保留足够的信息让 LLM 进行图像描述、回答问题和推理？并且能否在不触及冻结主干网络的情况下训练这个桥接层，将训练成本仅限于桥接层的参数？

The answer: a Q-Former. 32 learnable "query" vectors that cross-attend to the ViT's patch tokens, producing a 32-token visual summary that the LLM consumes. 188M parameters total. Trained with contrastive, matching, and generative objectives before ever touching the LLM.

> 答案是：Q-Former。32 个可学习的"查询"向量通过交叉注意力关注 ViT 的 patch token，产生 LLM 消费的 32 token 视觉摘要。总共 188M 参数。在接触 LLM 之前用对比、匹配和生成目标进行训练。

## The Concept | 核心概念

> **【中文解读】** BLIP-2 引入 Q-Former 作为冻结视觉编码器和冻结 LLM 之间的轻量桥接层。Q-Former 使用一组可学习的 query token 从视觉编码器提取与文本最相关的视觉特征，大幅减少了训练参数量（仅训练 Q-Former），实现了高效的视觉-语言对齐。

> **【拓展：BLIP-2 的高效训练】** BLIP-2 可在单张 A100 上 12 小时内完成训练（仅 Q-Former 参数），比之前的方法快 10-100 倍。Q-Former 的设计影响了后续的 LLaVA、InternVL 等模型。Salesforce 的 BLIP-2 在 VQAv2 上达到 82.2% 准确率，接近当时的最优水平。


> **【拓展：Q-Former 的影响】** Q-Former 的设计思想（用可学习 query 从冻结编码器提取任务相关特征）被广泛借鉴。InstructBLIP 用类似方法做指令感知的视觉特征提取。Q-Former 的轻量性（仅约 188M 参数）使得在消费级 GPU 上训练多模态模型成为可能。


### Learnable queries

The Q-Former's core trick: instead of letting the LLM's text tokens attend to image patches, introduce a new set of 32 learnable query vectors `Q` and let *them* attend to image patches. The queries are parameters of the model — they are learned during training and the same 32 queries are used for every image.

> Q-Former 的核心技巧：不让 LLM 的文本 token 关注图像 patch，而是引入一组新的 32 个可学习查询向量 `Q`，让*它们*关注图像 patch。查询是模型的参数——在训练中学习，且每张图像都使用相同的 32 个查询。

After cross-attention, each query holds a compressed summary of the image — "describe the main object", "describe the background", "count the objects", etc. The queries do not literally specialize on semantic labels; they learn whatever encoding makes downstream losses drop.

> 交叉注意力后，每个查询持有图像的压缩摘要——"描述主要对象"、"描述背景"、"计算对象数量"等。查询并非字面上专精于语义标签；它们学习使下游损失下降的任何编码。

### Architecture

The Q-Former is a small transformer (12 layers, ~100M params) with two paths:

> Q-Former 是一个小型 Transformer（12 层，约 100M 参数），有两条路径：

1. Query path: 32 query vectors flow through self-attention (among themselves), then cross-attention over the frozen ViT's patch tokens, then FFN.
   中文翻译：查询路径：32 个查询向量流过自注意力（彼此之间），然后对冻结 ViT 的 patch token 做交叉注意力，最后是 FFN。
2. Text path: a BERT-like text encoder shares the self-attention and FFN weights with the query path. Cross-attention is disabled for the text path.
   中文翻译：文本路径：类 BERT 的文本编码器与查询路径共享自注意力和 FFN 权重。文本路径禁用交叉注意力。

At training time both paths run. The queries and text interact through shared self-attention, which means the queries can condition on text for tasks that need it (ITM, ITG). At inference time for VLM handoff, only the queries flow through, yielding 32 visual tokens.

> 训练时两条路径同时运行。查询和文本通过共享的自注意力交互，这意味着查询可以在需要文本的任务（ITM、ITG）上以文本为条件。推理时 VLM 交接仅查询流过，产生 32 个视觉 token。

### Two-stage training

BLIP-2 pretrains in two stages:

> BLIP-2 分两阶段预训练：

Stage 1: representation learning (no LLM). Three losses:
- ITC (image-text contrastive): CLIP-style contrastive between pooled query tokens and text CLS token.
  中文翻译：ITC（图文对比）：池化查询 token 与文本 CLS token 之间的类 CLIP 对比损失。
- ITM (image-text matching): binary classifier — is this image-text pair a match? Hard-negative-mined.
  中文翻译：ITM（图文匹配）：二分类器——这个图文对是否匹配？使用难负例挖掘。
- ITG (image-grounded text generation): causal LM head on text, conditioned on the queries. Forces queries to encode text-generatable content.
  中文翻译：ITG（图像条件文本生成）：文本上的因果 LM 头，以查询为条件。强制查询编码可生成文本的内容。

Only the Q-Former trains. The ViT is frozen. No LLM involved.

> 仅训练 Q-Former。ViT 冻结。不涉及 LLM。

Stage 2: generative learning. Attach a frozen LLM (OPT-2.7B or Flan-T5-XL, etc.). Project the 32 query outputs to the LLM's embedding dim via a small linear layer. Prepend them to the text prompt. Train only the linear projection and the Q-Former on LM loss over the concatenated prompt + image + caption sequence.

> 第二阶段：生成学习。连接一个冻结的 LLM（OPT-2.7B 或 Flan-T5-XL 等）。通过一个小的线性层将 32 个查询输出投影到 LLM 的嵌入维度。将它们前置到文本提示。仅在线性投影和 Q-Former 上训练拼接的提示 + 图像 + 描述序列的 LM 损失。

After stage 2, the Q-Former + projection is the full visual adapter. At inference: image → ViT → Q-Former → linear proj → prepended to text → frozen LLM emits output.

> 第二阶段后，Q-Former + 投影就是完整的视觉适配器。推理时：图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 冻结 LLM 生成输出。

### Parameter economics

BLIP-2 with ViT-g/14 (1.1B, frozen) + OPT-6.7B (6.7B, frozen) + Q-Former (188M, trained) = 8B total, 188M trained. The Q-Former alone is ~2.4% of the full stack's parameters. Training cost reflects this: days on a handful of A100s vs weeks for end-to-end.

> BLIP-2 使用 ViT-g/14（11 亿，冻结）+ OPT-6.7B（67 亿，冻结）+ Q-Former（1.88 亿，训练）= 共 80 亿，训练 1.88 亿。Q-Former 仅占全栈参数的约 2.4%。训练成本反映了这一点：少量 A100 上数天 vs 端到端数周。

Quality: BLIP-2 matches or beats Flamingo-80B on zero-shot VQA while being 50x smaller. The bridge works.

> 质量：BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B，同时小了 50 倍。桥接方案有效。

### InstructBLIP and the instruction-aware Q-Former

InstructBLIP (2023) extends the Q-Former with an extra input: the instruction text itself. At cross-attention time, the queries now have access to both the image patches and the instruction. The queries can specialize per-instruction ("count the cars", "describe the mood") rather than learning a single fixed summary. Benchmark gains on held-out tasks.

> InstructBLIP（2023）通过额外输入扩展了 Q-Former：指令文本本身。在交叉注意力时，查询可以同时访问图像 patch 和指令。查询可以按指令专精化（"计算汽车数量"、"描述情绪"），而不是学习单一的固定摘要。在保留任务上有基准测试提升。

### MiniGPT-4 and the projector-only approach

MiniGPT-4 kept the Q-Former but trained only the output linear projection while freezing everything else. Cheap, but cost is quality — the queries were BLIP-2's, not yours. Good for rapid iteration, not the best architecture.

> MiniGPT-4 保留了 Q-Former，但仅训练输出线性投影，冻结其他一切。便宜，但代价是质量——查询是 BLIP-2 的，不是你的。适合快速迭代，不是最佳架构。

### Why LLaVA went simpler

LLaVA (2023, Lesson 12.05) replaced the Q-Former with a plain 2-layer MLP that projects every ViT patch token into LLM space — 576 tokens per image for a 24x24 grid, all fed to the LLM. Worse compression but lets the LLM attend over raw patches. At the time this was controversial; by late 2023 it was dominant because visual instruction data (LLaVA-Instruct-150k) proved that the MLP could be trained to preserve enough signal. The tradeoff: LLaVA's context fills faster, but it scales naturally to multi-image and video.

> LLaVA（2023，第 12.05 课）用简单的 2 层 MLP 替换了 Q-Former，将每个 ViT patch token 投影到 LLM 空间——24x24 网格下每张图像 576 个 token，全部喂给 LLM。压缩更差但让 LLM 可以关注原始 patch。当时这有争议；到 2023 年底它已成为主流，因为视觉指令数据（LLaVA-Instruct-150k）证明 MLP 可以被训练以保留足够的信号。权衡是：LLaVA 的上下文填充更快，但它自然扩展到多图像和视频。

By 2026 the field split: Q-Former survives where token budget matters (long video, many images); MLP projector dominates where raw quality per token is the priority.

> 到 2026 年，领域分化：Q-Former 在 token 预算重要时（长视频、多图像）存活；MLP 投影器在每个 token 的原始质量优先时占主导。

### Gated cross-attention: Flamingo, the ancestor

Flamingo (Lesson 12.04) predated BLIP-2 and used the same cross-attention idea but at every frozen LLM layer, not as a single bridge. BLIP-2 showed you can compress to the input layer only and still work. Gemini and Idefics combine both: interleaved input tokens plus optional gated cross-attention for in-context few-shot.

> Flamingo（第 12.04 课）早于 BLIP-2，使用相同的交叉注意力思想但在每个冻结的 LLM 层，而非单一桥接。BLIP-2 证明可以仅压缩到输入层仍然有效。Gemini 和 Idefics 结合两者：交错输入 token 加上可选的门控交叉注意力用于上下文少样本。

### The 2026 descendants

- Q-Former: BLIP-2, InstructBLIP, MiniGPT-4, and most video-language models for token budget reasons.
  中文翻译：Q-Former：BLIP-2、InstructBLIP、MiniGPT-4，以及大多数视频语言模型（因为 token 预算原因）。
- Perceiver resampler: Flamingo's variant (Lesson 12.04); Idefics family, Eagle, OmniMAE.
  中文翻译：Perceiver resampler：Flamingo 的变体（第 12.04 课）；Idefics 系列、Eagle、OmniMAE。
- MLP projector: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  中文翻译：MLP 投影器：LLaVA、LLaVA-NeXT、LLaVA-OneVision、Cambrian-1。
- Attention pool: VILA, PaliGemma.
  中文翻译：注意力池化：VILA、PaliGemma。

All four are valid. The deciding question is whether you are constrained on token budget or on quality-per-token.

> 四种方案都有效。决定性问题是你的约束是 token 预算还是每个 token 的质量。

## Use It | 用框架实现

`code/main.py` builds a stdlib Q-Former-style cross-attention:

> `code/main.py` 构建了一个标准库 Q-Former 风格的交叉注意力：

1. Simulate 256 image patch tokens (dim 128).
   中文翻译：模拟 256 个图像 patch token（维度 128）。
2. Instantiate 32 learnable queries (dim 128).
   中文翻译：实例化 32 个可学习查询（维度 128）。
3. Run scaled-dot-product cross-attention (Q from queries, K/V from patches).
   中文翻译：运行缩放点积交叉注意力（Q 来自查询，K/V 来自 patch）。
4. Project to LLM-dim (512) via a linear layer.
   中文翻译：通过线性层投影到 LLM 维度（512）。
5. Output the 32 LLM-ready visual tokens.
   中文翻译：输出 32 个 LLM 就绪的视觉 token。

All math in pure Python (nested loops over vectors). Toy but correct shape. The attention-weight matrix is printed so you can see which patches each query pulled from.

> 所有数学运算用纯 Python（向量的嵌套循环）。玩具级但形状正确。打印注意力权重矩阵，你可以看到每个查询从哪些 patch 提取信息。

## Ship It | 产出物

This lesson produces `outputs/skill-modality-bridge-picker.md`. Given a target VLM configuration (vision encoder token count, LLM context budget, deployment constraints, quality target), it recommends Q-Former vs MLP vs Perceiver resampler with a short justification and a parameter-count estimate for each bridge.

> 本课产出 `outputs/skill-modality-bridge-picker.md`。给定目标 VLM 配置（视觉编码器 token 数、LLM 上下文预算、部署约束、质量目标），它推荐 Q-Former vs MLP vs Perceiver resampler，附简短理由和每个桥接层的参数量估算。

## Exercises | 练习题

1. Implement the cross-attention block in PyTorch. Verify that with 32 queries and 256 keys/values, the attention-weight matrix is 32 x 256 and each row sums to 1 after softmax.
   中文翻译：用 PyTorch 实现交叉注意力块。验证 32 个查询和 256 个 key/value，注意力权重矩阵为 32 x 256，每行 softmax 后和为 1。

2. In BLIP-2 stage 1 the Q-Former runs three losses simultaneously: ITC, ITM, ITG. Write the forward signature for each in pseudo-code. Which one requires the text encoder path to be active?
   中文翻译：在 BLIP-2 第一阶段，Q-Former 同时运行三个损失：ITC、ITM、ITG。用伪代码写出每个的前向签名。哪个需要文本编码器路径激活？

3. Compare parameter counts: Q-Former (12 layers, 768 hidden) vs a 2-layer MLP projector (1408 → 4096, two layers). At what LLM scale does the 188M Q-Former cost pay back in training efficiency?
   中文翻译：比较参数量：Q-Former（12 层，768 隐藏维度）vs 2 层 MLP 投影器（1408 → 4096，两层）。在什么 LLM 规模下，188M 的 Q-Former 成本在训练效率上回本？

4. Read Section 3.2 of the BLIP-2 paper (arXiv:2301.12597) on how the Q-Former is initialized. Explain why initializing from BERT-base (not random) accelerates convergence.
   中文翻译：阅读 BLIP-2 论文（arXiv:2301.12597）第 3.2 节关于 Q-Former 初始化的部分。解释为什么从 BERT-base（非随机）初始化加速收敛。

5. For a 10-minute video at 1 FPS sampled to 60 frames, compute the per-frame token cost at (Q-Former → 32 tokens/frame) vs (MLP projector → 576 tokens/frame). Which fits into a 128k-token LLM context window?
   中文翻译：对于 10 分钟视频以 1 FPS 采样为 60 帧，计算每帧 token 成本：（Q-Former → 32 token/帧）vs（MLP 投影器 → 576 token/帧）。哪个能放进 128k token 的 LLM 上下文窗口？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Further Reading | 延伸阅读

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) — the core paper.
  中文翻译：BLIP-2 核心论文。
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) — the predecessor with the ITC/ITM/ITG trio.
  中文翻译：前作，包含 ITC/ITM/ITG 三联损失。
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) — "align before fuse" — the conceptual ancestor of stage 1 training.
  中文翻译："先对齐再融合"——第一阶段训练的概念先驱。
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500) — instruction-aware Q-Former.
  中文翻译：指令感知的 Q-Former。
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) — projector-only approach.
  中文翻译：仅投影器方案。
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) — general architecture for learnable-query cross-attention.
  中文翻译：可学习查询交叉注意力的一般架构。
