# InternVL3: Native Multimodal Pretraining | InternVL3：原生多模态预训练

> Every open VLM before InternVL3 followed the same three-step recipe: take a text LLM trained on trillions of text tokens, bolt on a vision encoder, then fine-tune the seams. This works but has alignment debt — the text LLM has spent its full pretraining budget on pure text and does not natively understand visual tokens. When you add vision post-hoc, the LLM has to re-learn how to relate visual input to its text reasoning without forgetting the text. InternVL3 (Zhu et al., April 2025) rejects the post-hoc approach: one pretraining run, text and multimodal interleaved from step one. The result matches Gemini 2.5 Pro on MMMU-Pro at 78B params open. This lesson reads the case for native pretraining and what changes when you make it.

> **【中文解读】** InternVL3 的核心创新：拒绝"先训文本 LLM 再接视觉编码器"的后装方案，改为从第一步就将文本和多模态数据交织训练。这消除了"对齐债务"——后装 VLM 会遗忘文本技能、回答漂移、视觉-文本不一致等问题。InternVL3-78B 在 MMMU-Pro 上匹配了 Gemini 2.5 Pro。

> **【拓展：原生预训练 vs 后装的成本权衡】** 原生预训练消除了对齐债务，但成本远高于后装方案——需要数百万 GPU 小时从头训练，且放弃了随时替换基础 LLM 的灵活性。对于大多数项目，后装方案仍然更经济。只有当你的规模达到需要训练新基础模型时，原生预训练才值得考虑。

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

## Learning Objectives  | 学习目标

- Explain why post-hoc VLM training accumulates alignment debt, citing the three measurable symptoms (catastrophic forgetting, answer drift, visual-text inconsistency).  | 解释后装 VLM 训练为什么积累对齐债务，列举三个可测量症状（灾难性遗忘、回答漂移、视觉-文本不一致）。
- Describe InternVL3's native pretraining corpus mix and why the ratio of text : interleaved : caption matters.  | 描述 InternVL3 原生预训练的语料混合比例及其重要性。
- Compare V2PE (variable visual position encoding) to Qwen2-VL's M-RoPE.  | 对比 V2PE（可变视觉位置编码）与 Qwen2-VL 的 M-RoPE。
- Name the Visual Resolution Router (ViR) and Decoupled Vision-Language (DvD) deployment optimizations.  | 列举 ViR（视觉分辨率路由器）和 DvD（解耦视觉-语言部署）优化。

## The Problem  | 问题背景

Post-hoc VLM training is the default. LLaVA, BLIP-2, Qwen-VL, Idefics — all take an already-pretrained LLM (Llama, Vicuna, Qwen, Mistral) and add vision. The training stages typically look like:

1. Frozen LLM + frozen vision encoder + trainable projector, trained on caption pairs to align embeddings.  | 冻结 LLM + 冻结视觉编码器 + 可训练投影器，用描述对训练。
2. Unfreeze LLM, train on instruction data (LLaVA-Instruct, ShareGPT4V).  | 解冻 LLM，用指令数据训练。
3. Optional task-specific fine-tune.  | 可选的任务特定微调。

Three symptoms of alignment debt show up:  | 对齐债务的三种症状：

- Catastrophic forgetting / 灾难性遗忘. The post-hoc VLM forgets text-only skills. GSM8K scores drop 5-10 points. Hellaswag scores drop. Pure-text agents regress.
- Answer drift / 回答漂移. Small phrasings of the same visual question get different answers. The vision encoder connects to the LLM with weaker bindings than the LLM's own tokens.
- Visual-text inconsistency / 视觉-文本不一致. The VLM can describe an image correctly and then answer a question contradicting its own description. Visual tokens do not participate in the LLM's internal consistency checks the same way text does.

> **【中文解读】** 后装 VLM 的三种对齐债务：(1) 灾难性遗忘——GSM8K 掉 5-10 分；(2) 回答漂移——同一种视觉问题的不同表述得到不同答案；(3) 视觉-文本不一致——模型正确描述了图像，却给出矛盾的回答。这些症状是因为视觉 token 不像文本 token 那样深度参与了 LLM 的内部一致性检查。

## The Concept  | 核心概念

### Native multimodal pretraining  | 原生多模态预训练

InternVL3 trains from scratch on a corpus that is native multimodal from step one. The mix is:  | 语料混合比例：

- 40% text-only data (FineWeb, Proof-Pile-2, etc.) / 40% 纯文本数据
- 35% interleaved image-text data (OBELICS, MMC4-style) / 35% 交织图文数据
- 20% paired image-caption data / 20% 图文配对数据
- 5% video-text data / 5% 视频文本数据

Vision tokens, text tokens, and cross-modal interactions all participate in the same loss from the first gradient step. No alignment pretraining, no projector freezing stage, no catastrophic forgetting to recover from.

Training is a single stage for the base model. Instruction tuning follows, but the base model already understands visual tokens as first-class citizens.

> **【中文解读】** InternVL3 从第一步就将视觉 token、文本 token 和跨模态交互纳入同一个损失函数。不需要对齐预训练，不需要投影器冻结阶段，不需要从灾难性遗忘中恢复。基础模型在预训练完成后就已经将视觉 token 视为一等公民。

### V2PE (variable visual position encoding)  | V2PE 可变视觉位置编码

Qwen2-VL uses M-RoPE with fixed axis allocation. InternVL3 introduces V2PE: the position encoding varies per modality type (text, image, video) with learnable scaling. In practice:

- Text tokens get 1D position (text index).  | 文本 token 用 1D 位置（文本索引）。
- Image patches get 2D position (row, col).  | 图像补丁用 2D 位置（行、列）。
- Video frames get 3D position (time, row, col).  | 视频帧用 3D 位置（时间、行、列）。

The three share the same RoPE frequency base, but the hidden-dim allocation per band is a learned parameter rather than a fixed split. Freedom to trade off temporal vs spatial frequency resolution during pretraining.

V2PE's ablation claim: 1-2 points on video benchmarks over M-RoPE at the same compute. Not a revolution, but cleaner.

> **【中文解读】** V2PE 与 M-RoPE 的区别：隐藏维度在各频段间的分配是可学习参数而非固定分割。模型可以在预训练过程中自动权衡时间与空间频率分辨率。在视频基准上比 M-RoPE 高 1-2 分。

### Visual Resolution Router (ViR)  | 视觉分辨率路由器

Deployment optimization. Not all images need full-resolution encoding. A photo with one object at low detail wastes tokens when encoded at 1280px native. ViR is a small classifier that predicts the minimum resolution needed to answer the question, before encoding.

The routing has three tiers: low-res (256 tokens), medium (576), high (2048+). For 60% of queries in production traffic, low or medium is sufficient. Net effect: 2-3x throughput at equal quality.

> **【中文解读】** ViR 是部署优化：一个小型分类器在编码前预测查询所需的最低分辨率。三级路由：低分辨率（256 token）、中（576）、高（2048+）。生产流量中 60% 的查询低或中分辨率就够了，吞吐量提升 2-3 倍。

> **【拓展：ViR 与金融场景】** 在金融文档处理中，大部分查询（如"这张发票的总金额是多少"）只需要低分辨率，但 OCR 密集任务（如"提取所有行项目"）需要高分辨率。ViR 可以根据查询自动选择合适的分辨率，大幅降低成本。

### Decoupled Vision-Language deployment (DvD)  | 解耦视觉-语言部署

When you serve a large VLM, the vision encoder runs once per image but the LLM runs autoregressively for every output token. The two components have different bottlenecks (vision = GPU memory bandwidth for conv + attention; LLM = KV cache). DvD splits them onto separate GPUs with streaming between.

For an 8B + 400M encoder model, DvD roughly doubles per-node throughput vs co-located.

> **【中文解读】** DvD 将视觉编码器和 LLM 部署在不同的 GPU 上，通过流式传输连接。编码器的瓶颈是 GPU 内存带宽，LLM 的瓶颈是 KV 缓存。分离部署后每节点吞吐量约翻倍。

### Single-stage vs multi-stage quality  | 单阶段 vs 多阶段质量

InternVL3's primary benchmark claim: at 78B params, match Gemini 2.5 Pro's MMMU-Pro. At 38B, match GPT-4o. At 8B, lead the open-8B leaderboard. All on a single-stage pretrain + instruction-tune recipe.

The alignment-debt hypothesis is measurable: InternVL3-8B loses fewer text-benchmark points (MMLU, GSM8K) than Qwen2.5-VL-7B per unit of vision-benchmark gain. The model is more of a generalist because training was one piece, not two.

> **【中文解读】** InternVL3-8B 每获得一个视觉基准分数的提升，损失的文本基准分数比 Qwen2.5-VL-7B 少。模型更"全科"，因为训练是一体的，不是两段拼接。

### InternVL3.5 and InternVL-U

InternVL3.5 (August 2025) scales the recipe. Same native-pretrain approach, more data, more params. MMMU improvements are incremental.

InternVL-U (2026) adds unified generation — image output via MMDiT heads on top of the same backbone. The "U" stands for "Understanding + generation," chasing Transfusion-style unified models (Lesson 12.13). The same native-pretrain backbone supports both understanding and generation heads.

> **【中文解读】** InternVL-U（2026）在同一个骨干上加入了图像生成能力（通过 MMDiT 头），追求 Transfusion 风格的理解+生成统一模型。同一预训练骨干同时支持理解和生成。

### Trade-offs of native pretraining  | 原生预训练的权衡

Native pretraining is not free:

- Compute / 计算. Training a new VLM from scratch costs the same as training a text LLM — millions of GPU-hours. Post-hoc adaptation reuses existing LLM weights, saves most of the cost.  | 从头训练的成本与训练文本 LLM 相同——数百万 GPU 小时。
- Data / 数据. Interleaved image-text corpora at scale are rare. OBELICS is 141M documents; MMC4 is 571M. Text alone ships at 15T tokens. Multimodal pretraining data scarcity is a hard constraint.  | 大规模交织图文语料稀缺，这是硬约束。
- Base-LLM reuse / 基础LLM复用. Native pretraining gives up the option to drop in a new LLM later. Post-hoc lets you swap Llama-3.1 for Llama-4 by retraining only the adapter.  | 原生预训练放弃了后续替换基础 LLM 的灵活性。

The bet InternVL3 makes: the alignment debt is worse than the reuse loss. The benchmarks back the claim. The cost-to-produce bars future labs from cheaply replicating. Post-hoc VLMs will keep existing because they remain cheaper for most projects.

> **【中文解读】** InternVL3 的赌注：对齐债务比失去复用灵活性更糟。基准测试支持这一判断。但原生预训练的高成本使得大多数项目仍然会选择后装方案。

## Use It  | 动手实践

`code/main.py` is a training-corpus mixer and ViR router simulator. It:

- Takes a target corpus mix (%text, %interleaved, %caption, %video) and computes expected steps per modality.  | 接收目标语料混合比例，计算每种模态的预期步数。
- Simulates ViR routing on a batch of queries (distribution: 50% low-detail, 30% medium, 20% high-detail) and reports average token count.  | 模拟 ViR 路由，报告平均 token 数。
- Reports DvD throughput estimates given encoder vs LLM FLOPs.  | 报告 DvD 吞吐量估计。
- Prints a side-by-side of post-hoc vs native pretraining in params, compute, data, and expected alignment-debt symptoms.  | 对比后装 vs 原生预训练。

## Ship It  | 部署上线

This lesson produces `outputs/skill-native-vs-posthoc-auditor.md`. Given a proposed VLM training plan, it audits whether to go native or post-hoc, flags alignment-debt risk, and recommends a corpus mix. Use it when you are sizing a new open-VLM project and need to pick the training strategy.

> **【中文解读】** 本课产出"原生 vs 后装审计工具"。给定 VLM 训练计划，评估应走原生还是后装路线，标记对齐债务风险，推荐语料混合比例。

## Exercises  | 练习题

1. Estimate the compute delta between InternVL3-8B (native pretrain) and LLaVA-OneVision-7B (post-hoc). Ratio of GPU-hours approximately? What explains the gap?
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 reports 40% text / 35% interleaved / 20% caption / 5% video. If your target task is video-heavy, propose a new ratio and argue why the base model still needs substantial text and caption data.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. Read MM1.5 Section 4 on forgetting. Name the exact benchmark where post-hoc training showed the largest regression. How much did the regression cost?
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. ViR routes 60% of traffic to low-resolution encoding. What kinds of queries does it misroute (sends to low-res when high-res was needed)? Propose three router-failure modes.
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. DvD splits vision and LLM onto separate GPUs. Under what traffic pattern does DvD hurt throughput instead of helping?
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Further Reading  | 延伸阅读

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238) | InternVL 第一代
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479) | InternVL3 原生预训练
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265) | InternVL3.5 规模扩展
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877) | InternVL-U 理解+生成统一
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566) | MM1.5 对齐债务量化
