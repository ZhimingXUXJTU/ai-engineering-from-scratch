# Multimodal RAG and Cross-Modal Retrieval | 多模态 RAG 与跨模态检索

> Vision-native document RAG is one slice. Production multimodal RAG goes wider — retrieving across text, images, audio, and video for workflows like trip planning ("find me a quiet vegan brunch with natural light"), medical triage ("what injury matches this photo + these notes"), e-commerce ("outfits similar to this selfie, in my size"), and field service ("diagnose this engine sound plus photo of the part"). Three 2025 surveys — Abootorabi et al., Mei et al., Zhao et al. — codified the sub-problems: cross-modal retrieval, retrieval fusion, generation grounding, multimodal evaluation. This lesson reads the surveys and designs a production pipeline.

> **【中文解读】** 生产级多模态 RAG 超越了单一文档检索——需要跨文本、图像、音频、视频检索，用于旅行规划、医疗分诊、电商推荐、现场服务等场景。2025 年三篇综述文章定义了四个子问题：跨模态检索、检索融合、生成接地、多模态评估。核心挑战是多个检索器结果的融合策略。

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·23（ColPali 视觉文档 RAG）、Phase 11·14-17（RAG 检索/融合/reranking）、Phase 12·02（CLIP 跨模态对齐）。本节是 ColPali 的扩展——多种模态一起检索+融合。
> 💡 **【类比】** 多模态 RAG = "全科医生诊断"。病人说"我胸口疼"（文本）+ 给你看心电图（图像）+ 让你听心跳录音（音频）。医生要同时检索医学文献（文本）、心电图案例库（图像）、心跳声纹库（音频），融合多源信息后给出诊断。融合策略：分数融合 = 各源给分加权平均；注意力融合 = 让 LLM 自己决定哪源重要；MoE 融合 = 不同专家处理不同模态。

## Learning Objectives

- Design cross-modal retrieval: text → image, image → text, audio → video, etc.
  中文翻译：设计跨模态检索：文本→图像、图像→文本、音频→视频等。
- Compare three fusion strategies: score fusion, attention-based fusion, MoE fusion.
  中文翻译：比较三种融合策略：分数融合、注意力融合、MoE 融合。
- Explain generation grounding: what "cite your sources" looks like when sources are a mix of modalities.
  中文翻译：解释生成接地：当来源是多种模态混合时，"引用来源"是什么样子。
- Name the three canonical multimodal RAG surveys of 2025 and their sub-problem taxonomy.
  中文翻译：列举 2025 年三篇经典多模态 RAG 综述及其子问题分类。

## The Problem | 问题引入

Single-modality RAG is a solved pattern: embed query, embed chunks, retrieve, stuff into LLM. Multimodal RAG requires:

> 单模态 RAG 是已解决的模式：嵌入查询、嵌入块、检索、塞入 LLM。多模态 RAG 需要：

1. Multiple retrieval heads (each modality needs embeddings in a compatible space).
   中文翻译：多个检索头（每种模态需要兼容空间的嵌入）。
2. Fusion of retrieval results across modalities.
   中文翻译：跨模态检索结果的融合。
3. Generation grounding that cites sources across modalities.
   中文翻译：跨模态引用来源的生成接地。
4. Evaluation metrics that cover cross-modal signal.
   中文翻译：覆盖跨模态信号的评估指标。

The 2025 surveys all arrive at the same taxonomy.

> 2025 年的综述都得出相同的分类法。

## The Concept | 核心概念

> **【中文解读】** 跨模态 RAG 扩展了传统文本 RAG，支持多模态检索和生成：可以用文本检索图像，用图像检索文本，或混合检索多模态文档。关键技术：统一多模态嵌入空间、跨模态重排序、多模态上下文融合。

> **【拓展：多模态 RAG 的应用** 多模态 RAG 在医疗（检索影像+病历）、电商（以图搜商品+商品描述）、法律（检索合同条款+附件图表）等领域有巨大价值。主要挑战是评估——如何衡量多模态检索的质量，目前缺乏标准化基准。


### Cross-modal retrieval

Retrieve documents of modality B given a query of modality A. Three patterns:

> 给定模态 A 的查询，检索模态 B 的文档。三种模式：

1. Shared embedding space. CLIP and CLAP produce text + image / text + audio embeddings in a shared space. Cosine similarity across modalities works directly. Limited to CLIP-trained pairs.
   中文翻译：共享嵌入空间。CLIP 和 CLAP 在共享空间中产生文本+图像/文本+音频嵌入。跨模态余弦相似度直接有效。限于 CLIP 训练过的配对。

2. Per-modality encoder + translation. Text encoder + image encoder + a small translator module mapping between spaces. Sen2Sen by Gupta et al. and other 2024 designs. Flexible but adds complexity.
   中文翻译：每模态独立编码器 + 翻译。文本编码器 + 图像编码器 + 在空间间映射的小翻译模块。Sen2Sen 等 2024 年设计。灵活但增加复杂度。

3. VLM as encoder. Use a VLM's hidden states as the retrieval representation. Any modality the VLM supports works. Higher quality, more expensive.
   中文翻译：VLM 作为编码器。使用 VLM 隐藏状态作为检索表示。VLM 支持的任何模态都可用。质量更高，成本更高。

Choice: CLIP / SigLIP 2 for text+image; CLAP for text+audio; VLM-hidden-states for cross-modal at frontier quality.

> 选择建议：文本+图像用 CLIP/SigLIP 2；文本+音频用 CLAP；前沿质量跨模态用 VLM 隐藏状态。

### Fusion strategies

You retrieved 10 results: 5 images, 3 text passages, 2 audio clips. How do you merge?

> 你检索了 10 个结果：5 张图像、3 段文本、2 个音频片段。如何合并？

Score fusion (cheapest). Each modality has its own retriever, each returns scores. Normalize scores within-modality then sum. Simple, often works.

> 分数融合（最便宜）。每种模态有自己的检索器，各自返回分数。模态内归一化后求和。简单，通常有效。

Attention-based fusion. Concatenate all retrieved items, let a small attention network weight them. Needs training.

> 注意力融合。拼接所有检索项，让小型注意力网络加权。需要训练。

MoE fusion. Gating network routes to modality-specific experts. Different query types route differently — a visual question weights images higher.

> MoE 融合。门控网络路由到模态特定专家。不同查询类型路由不同——视觉问题给图像更高权重。

Production default: score fusion with a slight bias toward the query's dominant modality. Upgrade to MoE if A/B shows clear wins on your domain.

> 生产默认：分数融合 + 对查询主导模态的轻微偏置。如果 A/B 测试在你的领域显示明显优势，升级到 MoE。

> **【中文解读】** 三种融合策略：(1) 分数融合——各模态检索器分别归一化分数后加权求和，最简单；(2) 注意力融合——小网络学习权重，需训练；(3) MoE 融合——门控网络按查询类型路由到不同专家。生产默认是分数融合 + 对查询主导模态的轻微偏置。

> **【拓展：多模态 RAG 的跨模态检索基础】** 跨模态检索有三种模式：(1) 共享嵌入空间（CLIP/SigLIP 2 用于图文，CLAP 用于文本-音频）；(2) 每模态独立编码器 + 翻译模块；(3) 用 VLM 隐藏状态作为检索表示。选择建议：文本+图像用 CLIP/SigLIP 2，文本+音频用 CLAP，跨模态前沿质量用 VLM 隐藏状态。

### Generation grounding

The LLM should cite which retrieved item drove each claim. For multi-modal:

> LLM 应引用哪个检索项驱动了每个声明。对于多模态：

- Text source: standard citation `[1]`.
  中文翻译：文本来源：标准引用 `[1]`。
- Image source: `[img 3]` with a short caption.
  中文翻译：图像来源：`[img 3]` 附简短描述。
- Audio: `[audio 2 at 0:34]`.
  中文翻译：音频来源：`[audio 2 at 0:34]`。

Train the generator with grounding-aware data: each claim in the training target is tagged with the source index. At inference, the model naturally emits citations.

> 用接地感知数据训练生成器：训练目标中的每个声明都标注来源索引。推理时模型自然输出引用。

### The 2025 surveys

Abootorabi et al. (arXiv:2502.08826, "Ask in Any Modality"): taxonomy for multimodal RAG. Covers retrieval, fusion, generation. Broadest coverage.

> Abootorabi 等人：多模态 RAG 分类法。覆盖检索、融合、生成。覆盖最广。

Mei et al. (arXiv:2504.08748, "A Survey of Multimodal RAG"): focuses on sub-task benchmarks and failure modes. Useful for evaluation design.

> Mei 等人：聚焦子任务基准和失败模式。对评估设计有用。

Zhao et al. (arXiv:2503.18016): vision-focused survey. Strong on ColPali-family work.

> Zhao 等人：聚焦视觉的综述。对 ColPali 系列工作覆盖深入。

Reading all three gives you the state of the art as of spring 2025. Most of the sub-problems are still open.

> 阅读全部三篇可获得 2025 年春的最前沿状态。大多数子问题仍然开放。

### MuRAG — the foundational paper

MuRAG (Chen et al., 2022) was the first multimodal RAG. Retrieved image + text from a multimodal KB, generated answers. Showed feasibility before the VLM wave. Modern systems (REACT, VisRAG, M3DocRAG) build on it.

> MuRAG 是第一个多模态 RAG。从多模态知识库检索图像+文本，生成回答。在 VLM 浪潮之前证明了可行性。现代系统（REACT、VisRAG、M3DocRAG）建立在此基础上。

### A production trip-planner example

Query: "find me a quiet vegan brunch with natural light."

> 查询："给我找一个安静的纯素早午餐，有自然光。"

Pipeline:

> 管道：

1. Decompose query. "quiet" → audio/review keyword; "vegan brunch" → menu item; "natural light" → image feature.
   中文翻译：分解查询。"安静"→音频/评论关键词；"纯素早午餐"→菜单项；"自然光"→图像特征。
2. Retrieve per modality:
   中文翻译：按模态检索：
   - Text retrieval on reviews: "vegan brunch, quiet ambiance."
     中文翻译：评论文本检索："纯素早午餐，安静氛围"。
   - Image retrieval on restaurant photos: "natural light, airy."
     中文翻译：餐厅照片图像检索："自然光，通风"。
   - Audio retrieval on ambient-sound clips: "low decibel, no music."
     中文翻译：环境声音频检索："低分贝，无音乐"。
3. Fuse scores. Each restaurant has a composite score.
   中文翻译：融合分数。每个餐厅有综合分数。
4. Top-k restaurants → VLM generator with all evidence → answer with citations.
   中文翻译：Top-k 餐厅 → VLM 生成器（附所有证据）→ 带引用的回答。

This is well beyond text-RAG. Each modality adds signal that text alone misses.

> 这远超文本 RAG。每种模态添加了仅靠文本会遗漏的信号。

### Agentic multimodal RAG

Multi-hop: if the first retrieval does not return high-confidence answers, the LLM reformulates and retrieves again. Agentic RAG patterns from Phase 14 apply here. Examples:

> 多跳：如果首次检索未返回高置信度回答，LLM 重新表述并再次检索。Phase 14 的 Agent RAG 模式在此适用。示例：

- Retrieve initial top-10 → LLM asks "too noisy, filter for <40 dB" → re-retrieve.
  中文翻译：检索初始 top-10 → LLM 提问"太嘈杂，过滤 <40 分贝" → 重新检索。
- Retrieve images → LLM sees one has a menu → retrieve the menu text → answer.
  中文翻译：检索图像 → LLM 看到一张有菜单 → 检索菜单文本 → 回答。

Adds complexity but handles queries that single-shot retrieval cannot.

> 增加复杂度但能处理单次检索无法处理的查询。

### Evaluation

Cross-modal evaluation is still immature. Common proxies:

> 跨模态评估仍不成熟。常用代理指标：

- Recall@k per modality.
  中文翻译：每模态的 Recall@k。
- Fused top-k accuracy.
  中文翻译：融合后的 top-k 准确率。
- Human-judged end-to-end satisfaction.
  中文翻译：人工评判的端到端满意度。
- Task-specific (bookings completed, purchases made).
  中文翻译：任务特定指标（完成的预订、达成的购买）。

No standard benchmark spans all modalities. Most papers evaluate on domain-specific tasks.

> 没有标准基准覆盖所有模态。大多数论文在领域特定任务上评估。

## Use It | 用框架实现

`code/main.py`:

- Three mock retrievers (text, image, audio) operating on a shared corpus of restaurants.
  中文翻译：三个模拟检索器（文本、图像、音频）在共享餐厅语料上运行。
- Score fusion that combines modality scores with configurable weights.
  中文翻译：用可配置权重组合模态分数的分数融合。
- A generator stub that emits a final answer with citations.
  中文翻译：输出带引用最终回答的生成器桩。
- A simple agentic loop that reformulates the query if confidence is low.
  中文翻译：置信度低时重新表述查询的简单 Agent 循环。

## Ship It | 产出物

This lesson produces `outputs/skill-multimodal-rag-designer.md`. Given a product spec with a multimodal query flow, designs retrievers, fusion, generator, and evaluation.

> 本课产出 `outputs/skill-multimodal-rag-designer.md`。给定多模态查询流的产品规格，设计检索器、融合策略、生成器和评估方案。

## Exercises | 练习题

1. Propose a medical-triage multimodal RAG: query = photo of injury + text symptoms. What modalities retrieve from what KB? 设计医疗分诊多模态 RAG：查询 = 伤处照片 + 文字症状。哪些模态从哪些知识库检索？

2. Score fusion is a simple weighted sum. What failure mode does it have that MoE fusion avoids? 分数融合是简单的加权求和。它有什么 MoE 融合可以避免的失败模式？

3. Read Abootorabi et al.'s taxonomy (Section 3). What are the three canonical sub-problems and how do they map to your chosen product? 阅读 Abootorabi 等人的分类法（第 3 节）。三个标准子问题是什么？如何映射到你选择的产品？

4. Design an eval spec for a trip-planner multimodal RAG. What metrics cover image recall, audio recall, and composite correctness? 设计旅行规划多模态 RAG 的评估规格。哪些指标覆盖图像召回、音频召回和综合正确性？

5. Agentic multi-hop RAG has a latency tax per round-trip. At what query difficulty does the accuracy gain justify the latency? Agent 多跳 RAG 每轮有延迟开销。在什么查询复杂度下，准确率提升值得延迟代价？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Further Reading | 延伸阅读

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
