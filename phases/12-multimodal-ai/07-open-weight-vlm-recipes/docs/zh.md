# Open-Weight VLM Recipes: What Actually Matters | 开源视觉语言模型配方：真正重要的因素

> The 2024-2026 open-weight VLM literature is a forest of ablation tables. Apple's MM1 tested 13 combinations of image encoder, connector, and data mix. Allen AI's Molmo proved detailed human captions beat GPT-4V distillation. Cambrian-1 ran 20+ encoder comparisons. Idefics2 formalized the five-axis design space. Prismatic VLMs compared 27 training recipes on a controlled benchmark. Out of all that noise, a small set of results holds across papers: image encoder matters more than connector architecture, data mixture matters more than either, and detailed human captions beat distilled synthetic data. This lesson reads those tables so you do not have to.

> **【中文解读】** 2024-2026 年开源 VLM 论文中充斥着大量消融实验。本课从 Apple MM1、Allen AI Molmo、Cambrian-1、Idefics2、Prismatic VLMs 等论文中提炼出核心结论：编码器比连接器架构更重要，数据混合比编码器更重要，详细的人工描述胜过蒸馏数据。

> **【拓展：VLM 工程的实践指南】** 本课的结论直接指导 VLM 工程实践。当你发现 VLM 性能不达标时，应按以下优先级排查：(1) 视觉 token 数量是否足够（60% 方差），(2) 编码器选择是否合适（20%），(3) 数据质量是否足够（10%），(4) 连接器架构（5%，几乎不影响）。这能避免在错误的维度上浪费 GPU 时间。

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

## 学习目标

- Name the five-axis VLM design space: image encoder, connector, LLM, data mix, resolution schedule.  | 列出 VLM 五轴设计空间：图像编码器、连接器、LLM、数据混合、分辨率调度。
- Read an MM1 / Idefics2 / Cambrian-1 ablation table and predict which knob moves a given benchmark.  | 阅读 MM1/Idefics2/Cambrian-1 消融表并预测哪个参数能提升给定基准。
- Pick a recipe (encoder, connector, data, resolution) for a new VLM given a compute budget and task mix.  | 给定计算预算和任务组合，为新 VLM 选择配方。
- Explain why detailed human captions beat GPT-4V distillation at the same token count.  | 解释为什么详细的人工描述在相同 token 数量下胜过 GPT-4V 蒸馏。

## 问题背景

Hundreds of open-weight VLMs exist. Most of the gap between "good" and "state-of-the-art" is not architecture. It is data, resolution schedule, and encoder choice. Knowing which knob to turn first when your model underperforms saves you a 5-million-GPU-hour mistake.

The 2023 wave (LLaVA-1.5, InstructBLIP, MiniGPT-4) ran on caption-pair pretraining + LLaVA-Instruct-150k. Good baseline. Topped out around MMMU 35%.

The 2024 wave (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) ran exhaustive ablations. Results were surprising and practical.

> **【中文解读】** 数百个开源 VLM 中，"好"与"最好"之间的差距主要不是架构，而是数据、分辨率调度和编码器选择。知道模型不达标时该先调哪个参数，能避免浪费 500 万 GPU 小时。2023 年的 LLaVA-1.5 等 VLM 在 MMMU 上停在 35% 左右；2024 年的 MM1、Molmo 等通过系统消融实验揭示了关键因素。

## 核心概念

### The five-axis design space  | 五轴设计空间

Idefics2 (Laurençon et al., 2024) named the axes:

1. Image encoder / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Encoders differ in patch size, resolution, and pretraining objective / 编码器在补丁大小、分辨率和预训练目标上各不相同.
2. Connector / 连接器. MLP (2-4 layers), Q-Former (32 queries + cross-attn), Perceiver Resampler (64 queries), C-Abstractor (convolutional + bilinear pooling) / MLP（2-4层）、Q-Former（32查询+交叉注意力）、Perceiver 重采样器（64查询）、C-Abstractor（卷积+双线性池化）.
3. Language model / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5. LLM size is the dominant param cost / LLM 大小是主要参数成本.
4. Training data / 训练数据. Caption pairs (CC3M, LAION), interleaved (OBELICS, MMC4), instruction (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Resolution schedule / 分辨率调度. Fixed 224/336/448, AnyRes, native dynamic. Ramped during training or constant / 固定分辨率、AnyRes、原生动态分辨率。训练中递增或恒定.

Every production VLM makes a choice on each axis. Most of the variance in MMMU scores is explained by axes 1, 4, and 5 — not by which connector you picked.

> **【中文解读】** 每个 VLM 都在五个轴上做出选择。MMMU 分数的大部分方差由轴1（编码器）、轴4（数据）和轴5（分辨率）解释——而不是你选了哪个连接器。这意味着：把钱花在更好的编码器和更好的数据上，比纠结连接器架构有价值得多。

### Axis 1: encoder > connector  | 编码器 > 连接器

MM1 Section 3.2 showed: swapping from CLIP ViT-L/14 to SigLIP SO400m/14 added 3+ points MMMU. Swapping the connector from MLP to Perceiver Resampler added less than 1 point. Idefics2 replicated: SigLIP > CLIP, Q-Former ≈ MLP ≈ Perceiver at the same token count.

Cambrian-1's "Cambrian Vision Encoders Match-Up" (Tong et al., 2024) ran 20+ encoders on a vision-centric benchmark (CV-Bench). The top of the leaderboard is a mix of DINOv2 and SigLIP; CLIP is middle of the pack; ImageBind and ViT-MAE are lower. The gap from CLIP ViT-L to DINOv2 ViT-g/14 is ~5-7 points on CV-Bench.

The 2026 default encoder for open VLMs is SigLIP 2 SO400m/14 for semantic + dense features, sometimes concatenated with DINOv2 ViT-g/14 features (Cambrian's "Spatial Vision Aggregator" does this).

> **【中文解读】** 换编码器（CLIP→SigLIP）加 3+ 分 MMMU，换连接器（MLP→Perceiver）加不到 1 分。2026 年开源 VLM 的默认编码器是 SigLIP 2 SO400m/14，有时与 DINOv2 ViT-g/14 拼接（Cambrian 的"空间视觉聚合器"就是这么做的）。

### Axis 2: connector design is a wash  | 连接器设计几乎无影响

MM1, Idefics2, Prismatic, and MM-Interleaved all reached the same conclusion: at a fixed visual-token count, connector architecture barely matters. A 2-layer MLP on mean-pooled patches performs within 1 point of a 32-query Q-Former at the same token budget.

What does matter is the token count. More visual tokens = more LLM compute = better performance up to a point, then diminishing returns. 64 tokens per image is too few for OCR. 576-1024 tokens is the sweet spot for most open VLMs. 2048+ helps only for documents and charts.

Q-Former vs MLP is a cost question, not a quality question: Q-Former caps tokens at 32-64 regardless of image resolution; MLP emits all patch tokens. For high-res inputs, Q-Former saves LLM context; for low-res, the difference is noise.

> **【中文解读】** 在固定视觉 token 数量下，连接器架构几乎不影响性能。2 层 MLP 和 32 查询 Q-Former 的差距在 1 分以内。真正重要的是 token 数量：64 个太少，576-1024 是最佳区间，2048+ 只对文档和图表有帮助。

### Axis 3: LLM size sets the ceiling  | LLM 大小决定天花板

Doubling the LLM from 7B to 13B reliably adds 2-4 points on MMMU across every VLM paper. At 70B you saturate most benchmarks. The VLM's multimodal reasoning ceiling is the LLM's text reasoning ceiling — the visual encoder can only feed it, not reason for it.

This is why Qwen2.5-VL-72B and Claude Opus 4.7 crush MMMU-Pro and ScreenSpot-Pro: the language brain is huge. A 7B VLM cannot substitute for a 70B VLM through clever connector design.

> **【中文解读】** LLM 翻倍（7B→13B）稳定增加 2-4 分 MMMU。70B 时大多数基准饱和。VLM 的多模态推理天花板就是 LLM 的文本推理天花板——视觉编码器只能"喂"数据，不能代替推理。这就是为什么 72B 参数的 VLM 能碾压 7B 的——语言大脑的规模不可替代。

### Axis 4: data — detailed human captions beat distillation  | 数据：人工描述胜过蒸馏

Molmo + PixMo (Deitke et al., 2024) is the 2024 result everyone should read. Allen AI had human annotators describe images in 1-3 minute dense speech-to-text passes, yielding 712K densely-captioned images. No GPT-4V distillation anywhere in the training data.

Molmo-72B beat Llama-3.2-90B-Vision on 11 of 11 benchmarks. The delta is not architecture — it is caption quality. Detailed human captions contain 5-10x more information per image than short web captions and stay factually grounded where GPT-4V distillation hallucinates.

ShareGPT4V (Chen et al., 2023) and Cauldron (Idefics2) followed the same playbook with mixed human + GPT-4V captions. The trend is clear: for the 2026 frontier, caption density > caption quantity > distillation convenience.

> **【中文解读】** Molmo 的核心发现：让人类标注者用 1-3 分钟的密集语音描述图像，得到 712K 张高质量标注图像，完全不使用 GPT-4V 蒸馏。Molmo-72B 在 11/11 基准上击败了 Llama-3.2-90B-Vision。差距不是架构——是描述质量。详细人工描述每张图的信息量是短网络描述的 5-10 倍，且事实准确，不像 GPT-4V 蒸馏数据会"继承"幻觉。

> **【拓展：数据质量的投资回报】** 这一发现对构建垂直领域 VLM 有重要启示：与其花大量算力调架构，不如投入资源获取高质量的领域数据。在金融场景中，用专业人员标注报表、发票、合同的图像描述，比用 GPT-4V 自动生成数据的效果会好得多。

### Axis 5: resolution and its schedule  | 分辨率及其调度

Idefics2's ablations: 384 -> 448 adds 1-2 points. 448 -> 980 with image splitting (AnyRes) adds another 3-5 on OCR benchmarks. Flat resolution training plateaus at medium accuracy; resolution ramping (start 224, finish 448 or native) trains faster and ends higher.

Cambrian-1 ran a resolution vs tokens trade-off: at fixed compute, you can have more tokens at lower resolution or fewer tokens at higher resolution. Higher resolution wins for OCR; lower-res-more-tokens wins for general scene understanding.

The 2026 production recipe: train Stage 1 at 384 fixed, Stage 2 with dynamic resolution up to 1280 for OCR-heavy tasks.

> **【中文解读】** 分辨率从 384 提升到 448 加 1-2 分，448 到 980（加 AnyRes）在 OCR 基准上再加 3-5 分。分辨率递增调度（从 224 开始，到 448 或原生分辨率结束）训练更快、结果更好。固定计算预算下：高分辨率利于 OCR，低分辨率+更多 token 利于通用场景理解。

### The Prismatic controlled comparison  | Prismatic 控制对比实验

Prismatic VLMs (Karamcheti et al., 2024) is the paper that controlled all the axes. Same 13B LLM, same instruction data, same evaluation — only one axis varies at a time. Results:

- Per-image visual-token count explains ~60% of variance.  | 每张图的视觉 token 数解释约 60% 方差。
- Encoder choice explains ~20%.  | 编码器选择解释约 20%。
- Connector architecture explains ~5%.  | 连接器架构解释约 5%。
- Everything else (data mix, scheduler, LR) the remaining ~15%.  | 其余因素（数据混合、调度器、学习率）解释剩余约 15%。

This is a rough decomposition, but it is the cleanest answer to "what should I ablate first" in the literature.

> **【中文解读】** Prismatic VLMs 是最干净的控制实验——同一 13B LLM、同一指令数据、同一评估，每次只变一个轴。结论：视觉 token 数（60%）> 编码器（20%）> 其余（15%）> 连接器（5%）。这是"应该先消融什么"的最佳答案。

### A picker for 2026  | 2026 年推荐配方

Given the evidence, the default open-VLM recipe for a new project in 2026:

- Encoder / 编码器: SigLIP 2 SO400m/14 at native resolution with NaFlex, concatenated with DINOv2 ViT-g/14 for dense features if you need segmentation/grounding / 如需分割/定位则拼接 DINOv2.
- Connector / 连接器: 2-layer MLP on patch tokens. Skip Q-Former unless you are token-constrained / 除非 token 受限否则跳过 Q-Former.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B for cost / 成本优先选7B, 70B for quality / 质量优先选70B, picked by target latency / 按延迟目标选择.
- Data / 数据: PixMo + ShareGPT4V + Cauldron, topped up with task-specific instruction data / 补充任务特定的指令数据.
- Resolution / 分辨率: dynamic (min 256, max 1280 pixels per long side) / 动态（最小256，最大1280像素每长边）.
- Schedule / 调度: Stage 1 alignment (projector-only / 仅投影器), Stage 2 full fine-tune / 全参数微调, Stage 3 task-specific fine-tune / 任务特定微调.

Every one of those defaults traces back to a measured ablation in the papers cited at the end of this lesson.

> **【中文解读】** 以上每一条默认选择都可追溯到本课引用的论文中的消融实验结果。这是 2026 年构建新 VLM 项目的最佳起点配方。

## 动手实践

`code/main.py` is an ablation table parser and recipe picker. It encodes the MM1 and Idefics2 ablation tables (condensed) and lets you query:

- "Given budget X and task Y, what recipe wins?"  | "给定预算 X 和任务 Y，哪种配方最优？"
- "If I swap SigLIP for CLIP on a 7B Llama, what is the expected MMMU delta?"  | "在 7B Llama 上把 CLIP 换成 SigLIP，预期 MMMU 变化多少？"
- "Which axis should I ablate first for an 80% confidence answer?"  | "要获得 80% 置信度的答案，应先消融哪个轴？"

The output is a ranked recipe list with expected benchmark deltas and an "ablate first" recommendation.

## 部署上线

This lesson produces `outputs/skill-vlm-recipe-picker.md`. Given a target task mix, a compute budget, and a latency target, it emits a full recipe (encoder, connector, LLM, data mix, resolution schedule) with citations to the ablation that justifies each choice. Stops engineers from reinventing the Idefics2 ablation table every time a new VLM project starts.

> **【中文解读】** 本课产出 VLM 配方选择工具。给定目标任务组合、计算预算和延迟目标，输出完整配方，每项选择都附带论文消融实验的引用。避免工程师每次新开 VLM 项目都要重新做 Idefics2 消融表。

## 练习题

1. Read MM1 Section 3.2. For a fixed 2B LLM at budget 50M images, which encoder wins? Would the answer flip at 13B LLM? Why?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1 finds that concatenating DINOv2 + SigLIP outperforms either alone on vision-centric benchmarks but adds no signal on MMMU. Predict which benchmarks gain and which stay flat.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. Your target is a mobile UI agent on a 2B LLM. Pick encoder, connector, resolution, and data mix. Justify each choice with a specific ablation table.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo ships 4B and 72B models. The 4B is competitive with closed 7B VLMs; the 72B beats Llama-3.2-90B-Vision on 11/11 benchmarks. What does that tell you about the LLM-size plateau hypothesis?
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. Design an ablation table to isolate data-mix quality from encoder quality on a 7B VLM. How many training runs minimum? Propose the four axis settings.
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## 延伸阅读

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611) | Apple MM1 多模态模型消融实验
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) | 构建 VLM 的关键因素
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146) | Molmo 与 PixMo 人工标注数据
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860) | Cambrian-1 编码器对比
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) | Prismatic VLMs 控制消融实验
