# Multimodal RAG and Cross-Modal Retrieval | 多模态 RAG 与跨模态检索

> Vision-native document RAG is one slice. Production multimodal RAG goes wider — retrieving across text, images, audio, and video for workflows like trip planning ("find me a quiet vegan brunch with natural light"), medical triage ("what injury matches this photo + these notes"), e-commerce ("outfits similar to this selfie, in my size"), and field service ("diagnose this engine sound plus photo of the part"). Three 2025 surveys — Abootorabi et al., Mei et al., Zhao et al. — codified the sub-problems: cross-modal retrieval, retrieval fusion, generation grounding, multimodal evaluation. This lesson reads the surveys and designs a production pipeline.

> **【中文解读】** 生产级多模态 RAG 超越了单一文档检索——需要跨文本、图像、音频、视频检索，用于旅行规划、医疗分诊、电商推荐、现场服务等场景。2025 年三篇综述文章定义了四个子问题：跨模态检索、检索融合、生成接地、多模态评估。核心挑战是多个检索器结果的融合策略。

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

## 学习目标

- Design cross-modal retrieval: text → image, image → text, audio → video, etc.
- Compare three fusion strategies: score fusion, attention-based fusion, MoE fusion.
- Explain generation grounding: what "cite your sources" looks like when sources are a mix of modalities.
- Name the three canonical multimodal RAG surveys of 2025 and their sub-problem taxonomy.

## 问题引入

Single-modality RAG is a solved pattern: embed query, embed chunks, retrieve, stuff into LLM. Multimodal RAG requires:

1. Multiple retrieval heads (each modality needs embeddings in a compatible space).
2. Fusion of retrieval results across modalities.
3. Generation grounding that cites sources across modalities.
4. Evaluation metrics that cover cross-modal signal.

The 2025 surveys all arrive at the same taxonomy.

## 核心概念

> **【中文解读】** 跨模态 RAG 扩展了传统文本 RAG，支持多模态检索和生成：可以用文本检索图像，用图像检索文本，或混合检索多模态文档。关键技术：统一多模态嵌入空间、跨模态重排序、多模态上下文融合。

> **【拓展：多模态 RAG 的应用** 多模态 RAG 在医疗（检索影像+病历）、电商（以图搜商品+商品描述）、法律（检索合同条款+附件图表）等领域有巨大价值。主要挑战是评估——如何衡量多模态检索的质量，目前缺乏标准化基准。


### Cross-modal retrieval

Retrieve documents of modality B given a query of modality A. Three patterns:

1. Shared embedding space. CLIP and CLAP produce text + image / text + audio embeddings in a shared space. Cosine similarity across modalities works directly. Limited to CLIP-trained pairs.

2. Per-modality encoder + translation. Text encoder + image encoder + a small translator module mapping between spaces. Sen2Sen by Gupta et al. and other 2024 designs. Flexible but adds complexity.

3. VLM as encoder. Use a VLM's hidden states as the retrieval representation. Any modality the VLM supports works. Higher quality, more expensive.

Choice: CLIP / SigLIP 2 for text+image; CLAP for text+audio; VLM-hidden-states for cross-modal at frontier quality.

### Fusion strategies

You retrieved 10 results: 5 images, 3 text passages, 2 audio clips. How do you merge?

Score fusion (cheapest). Each modality has its own retriever, each returns scores. Normalize scores within-modality then sum. Simple, often works.

Attention-based fusion. Concatenate all retrieved items, let a small attention network weight them. Needs training.

MoE fusion. Gating network routes to modality-specific experts. Different query types route differently — a visual question weights images higher.

Production default: score fusion with a slight bias toward the query's dominant modality. Upgrade to MoE if A/B shows clear wins on your domain.

> **【中文解读】** 三种融合策略：(1) 分数融合——各模态检索器分别归一化分数后加权求和，最简单；(2) 注意力融合——小网络学习权重，需训练；(3) MoE 融合——门控网络按查询类型路由到不同专家。生产默认是分数融合 + 对查询主导模态的轻微偏置。

> **【拓展：多模态 RAG 的跨模态检索基础】** 跨模态检索有三种模式：(1) 共享嵌入空间（CLIP/SigLIP 2 用于图文，CLAP 用于文本-音频）；(2) 每模态独立编码器 + 翻译模块；(3) 用 VLM 隐藏状态作为检索表示。选择建议：文本+图像用 CLIP/SigLIP 2，文本+音频用 CLAP，跨模态前沿质量用 VLM 隐藏状态。

### Generation grounding

The LLM should cite which retrieved item drove each claim. For multi-modal:

- Text source: standard citation `[1]`.
- Image source: `[img 3]` with a short caption.
- Audio: `[audio 2 at 0:34]`.

Train the generator with grounding-aware data: each claim in the training target is tagged with the source index. At inference, the model naturally emits citations.

### The 2025 surveys

Abootorabi et al. (arXiv:2502.08826, "Ask in Any Modality"): taxonomy for multimodal RAG. Covers retrieval, fusion, generation. Broadest coverage.

Mei et al. (arXiv:2504.08748, "A Survey of Multimodal RAG"): focuses on sub-task benchmarks and failure modes. Useful for evaluation design.

Zhao et al. (arXiv:2503.18016): vision-focused survey. Strong on ColPali-family work.

Reading all three gives you the state of the art as of spring 2025. Most of the sub-problems are still open.

### MuRAG — the foundational paper

MuRAG (Chen et al., 2022) was the first multimodal RAG. Retrieved image + text from a multimodal KB, generated answers. Showed feasibility before the VLM wave. Modern systems (REACT, VisRAG, M3DocRAG) build on it.

### A production trip-planner example

Query: "find me a quiet vegan brunch with natural light."

Pipeline:

1. Decompose query. "quiet" → audio/review keyword; "vegan brunch" → menu item; "natural light" → image feature.
2. Retrieve per modality:
   - Text retrieval on reviews: "vegan brunch, quiet ambiance."
   - Image retrieval on restaurant photos: "natural light, airy."
   - Audio retrieval on ambient-sound clips: "low decibel, no music."
3. Fuse scores. Each restaurant has a composite score.
4. Top-k restaurants → VLM generator with all evidence → answer with citations.

This is well beyond text-RAG. Each modality adds signal that text alone misses.

### Agentic multimodal RAG

Multi-hop: if the first retrieval does not return high-confidence answers, the LLM reformulates and retrieves again. Agentic RAG patterns from Phase 14 apply here. Examples:

- Retrieve initial top-10 → LLM asks "too noisy, filter for <40 dB" → re-retrieve.
- Retrieve images → LLM sees one has a menu → retrieve the menu text → answer.

Adds complexity but handles queries that single-shot retrieval cannot.

### Evaluation

Cross-modal evaluation is still immature. Common proxies:

- Recall@k per modality.
- Fused top-k accuracy.
- Human-judged end-to-end satisfaction.
- Task-specific (bookings completed, purchases made).

No standard benchmark spans all modalities. Most papers evaluate on domain-specific tasks.

## 用框架实现

`code/main.py`:

- Three mock retrievers (text, image, audio) operating on a shared corpus of restaurants.
- Score fusion that combines modality scores with configurable weights.
- A generator stub that emits a final answer with citations.
- A simple agentic loop that reformulates the query if confidence is low.

## 产出物

This lesson produces `outputs/skill-multimodal-rag-designer.md`. Given a product spec with a multimodal query flow, designs retrievers, fusion, generator, and evaluation.

## 练习题

1. Propose a medical-triage multimodal RAG: query = photo of injury + text symptoms. What modalities retrieve from what KB? 设计医疗分诊多模态 RAG：查询 = 伤处照片 + 文字症状。哪些模态从哪些知识库检索？

2. Score fusion is a simple weighted sum. What failure mode does it have that MoE fusion avoids? 分数融合是简单的加权求和。它有什么 MoE 融合可以避免的失败模式？

3. Read Abootorabi et al.'s taxonomy (Section 3). What are the three canonical sub-problems and how do they map to your chosen product? 阅读 Abootorabi 等人的分类法（第 3 节）。三个标准子问题是什么？如何映射到你选择的产品？

4. Design an eval spec for a trip-planner multimodal RAG. What metrics cover image recall, audio recall, and composite correctness? 设计旅行规划多模态 RAG 的评估规格。哪些指标覆盖图像召回、音频召回和综合正确性？

5. Agentic multi-hop RAG has a latency tax per round-trip. At what query difficulty does the accuracy gain justify the latency? Agent 多跳 RAG 每轮有延迟开销。在什么查询复杂度下，准确率提升值得延迟代价？

## 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## 延伸阅读

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
