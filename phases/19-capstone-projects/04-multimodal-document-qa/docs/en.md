# Capstone 04 — Multimodal Document QA (Vision-First PDF, Tables, Charts) | 文档问答 多模态 结业

> The 2026 document-QA frontier moved away from OCR-then-text and toward vision-first late interaction. ColPali, ColQwen2.5, and ColQwen3-omni treat each PDF page as an image, embed it with multi-vector late interaction, and let the query attend to patches directly. On financial 10-Ks, scientific papers, and handwritten notes this pattern beats OCR-first by a large margin. Build the pipeline end to end on 10k pages and publish the side-by-side against OCR-then-text.

> **【中文解读】** 本节是综合项目——构建多模态文档问答系统，处理文本、图像和表格。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (pipeline), TypeScript (viewer UI) | **语言:** Python（管道）, TypeScript（查看器 UI）
**Prerequisites:** Phase 4 (computer vision), Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 17 (infrastructure)

> 🔗 **【前置】** 顶点项目 04 = 综合 Phase 4/5/7/11/12/17。文档 QA 走视觉优先（ColPali 风格，参考 Phase 12·23）。
> 💡 **【类比】** 文档 QA = "PDF 直接看"。2026 前沿：从"OCR→文本"转向"视觉优先 + 延迟交互"（ColPali/ColQwen2.5/ColQwen3-omni）。把 PDF 页面当图像，多向量嵌入，query 直接关注 patch。在金融 10-K、科学论文、手写笔记上大幅胜 OCR 方案。| **前置知识:** Phase 4（计算机视觉）, Phase 5（NLP）, Phase 7（Transformer）, Phase 11（LLM 工程）, Phase 12（多模态）, Phase 17（基础设施）
**Phases exercised:** P4 · P5 · P7 · P11 · P12 · P17 | **涉及阶段:** P4 · P5 · P7 · P11 · P12 · P17
**Time:** 30 hours | **时间:** 30 小时

## Problem | 问题引入

> **【中文解读】** 本节阐述文档问答从"先 OCR 再文本"到"视觉优先"的范式转变。企业 PDF 中的旋转表格、公式、图表、手写批注是 OCR 管道的噩梦。2026 年的答案是 ColPali/ColQwen 系列的晚期交互多向量检索——将每页 PDF 当作图像，让查询直接关注到图像块（patch）。在图表、表格和手写内容上，视觉优先方案显著优于 OCR 文本方案。

> **【拓展：视觉文档检索前沿】** ColPali 由 Illuin Tech 在 2024 年提出（arXiv:2407.01449），将文档检索从文本匹配推向视觉匹配。ColQwen2.5 和 ColQwen3-omni 进一步提升精度。在 ViDoRe v3 基准上，视觉优先检索 nDCG@5 比 OCR-then-text 高出显著幅度。代价是存储膨胀——每页约 2048 个 patch 向量，DocPruner 通过 50% 剪枝将存储减半，精度损失 < 0.5%。Vespa 和 Qdrant 都支持多向量字段和 MaxSim 检索。

Enterprises sit on PDFs that OCR pipelines mangle: scanned 10-Ks with rotated tables, scientific papers dense with equations, charts that only make sense as images, handwritten annotations. Treating these as text-first means losing half the signal. The 2026 answer is late-interaction multi-vector retrieval on raw page images. ColPali (Illuin Tech) introduced it; ColQwen2.5-v0.2 and ColQwen3-omni pushed accuracy. On ViDoRe v3, vision-first retrieval scores above OCR-then-text by meaningful margins — and the gap widens on charts, tables, and handwriting.

> 企业拥有大量 OCR 管道无法正确处理的 PDF：带旋转表格的扫描 10-K 报告、充满公式的科学论文、只有作为图像才有意义的图表、手写批注。将这些视为文本优先意味着丢失一半信号。2026 年的答案是在原始页面图像上进行晚期交互多向量检索。ColPali（Illuin Tech）引入了它；ColQwen2.5-v0.2 和 ColQwen3-omni 推动了精度。在 ViDoRe v3 上，视觉优先检索以显著优势超过 OCR-then-text——差距在图表、表格和手写内容上更大。

The trade-off is storage and latency. A ColQwen embedding is ~2048 patch vectors per page, not a single 1024-dim vector. Raw storage balloons. DocPruner (2026) brings 50% pruning without measurable accuracy loss. You will index 10k pages, measure ViDoRe v3 nDCG@5, serve answers under 2s, and compare directly against an OCR-then-text baseline.

> 代价是存储和延迟。ColQwen 嵌入是每页约 2048 个 patch 向量，而不是单个 1024 维向量。原始存储膨胀。DocPruner（2026）在不损失可测量精度的情况下实现 50% 剪枝。你将索引 1 万页，测量 ViDoRe v3 nDCG@5，在 2 秒内提供答案，并直接与 OCR-then-text 基线比较。

## Concept | 核心概念

> **【中文解读】** 晚期交互（Late Interaction）是指每个查询 token 与每个页面 patch token 独立计算相似度，取每个查询 token 的最大得分后求和。这比单池化向量匹配更精细。多向量索引（Vespa/Qdrant/AstraDB）存储每个页面的 patch 嵌入并在检索时执行 MaxSim。答案生成使用视觉语言模型（Qwen3-VL-30B/Gemini 2.5 Pro），带证据区域定位和页码引用。

> **【拓展：多模态 VLM 选型】** 2026 年文档问答的主流 VLM 包括：Qwen3-VL-30B（自托管最优）、Gemini 2.5 Pro（API 调用最优）、InternVL3（开源备选）。对于公式密集页面，Nougat OCR 作为补充文本通道。评估采用二维矩阵：横轴内容类型（文本段落/密集表格/图表/手写/公式），纵轴检索方法（视觉优先/OCR-then-text/混合），每个单元格计算 nDCG@5 和答案准确率。

Late interaction means every query token scores against every patch token, and the maximum score per query token is summed. You get fine-grained matching without needing a single pooled vector. A multi-vector index (Vespa, Qdrant multi-vector, or AstraDB) stores the per-patch embeddings and runs MaxSim at retrieval time.

> 晚期交互意味着每个查询 token 与每个 patch token 计算分数，每个查询 token 的最大分数被求和。你获得精细匹配而不需要单个池化向量。多向量索引（Vespa、Qdrant multi-vector 或 AstraDB）存储每个 patch 的嵌入并在检索时运行 MaxSim。

The answerer is a vision-language model that takes the query plus the top-k retrieved pages as images and writes an answer with evidence regions (bounding boxes or page references). Qwen3-VL-30B, Gemini 2.5 Pro, and InternVL3 are the 2026 frontier choices. For equations and scientific notation, an OCR fallback (Nougat, dots.ocr) is spliced in as an optional text channel.

> 回答器是一个视觉语言模型，接收查询加 top-k 检索页面作为图像，并写出带证据区域（边界框或页码引用）的答案。Qwen3-VL-30B、Gemini 2.5 Pro 和 InternVL3 是 2026 年前沿选择。对于公式和科学记号，OCR 回退（Nougat、dots.ocr）作为可选文本通道拼入。

Evaluation is a two-dimensional matrix. One axis: content type (plain text paragraphs, dense tables, bar/line charts, handwritten notes, equations). Other axis: retrieval approach (vision-first late interaction vs OCR-then-text vs hybrid). Each cell gets nDCG@5 and answer accuracy. The report is the deliverable.

> 评估是一个二维矩阵。一个轴：内容类型（纯文本段落、密集表格、条形/折线图、手写笔记、公式）。另一个轴：检索方法（视觉优先晚期交互 vs OCR-then-text vs 混合）。每个单元格获得 nDCG@5 和答案准确率。报告是交付物。

## Architecture | 架构

```
PDFs -> page renderer (PyMuPDF, 180 DPI)
           |
           v
  ColQwen2.5-v0.2 embed (multi-vector per page, ~2048 patches)
           |
           +------> DocPruner 50% compression
           |
           v
   multi-vector index (Vespa or Qdrant multi-vector)
           |
query ----+----> retrieve top-k pages (MaxSim)
           |
           v
  VLM answerer: Qwen3-VL-30B | Gemini 2.5 Pro | InternVL3
    inputs: query + top-k page images + optional OCR text
           |
           v
  answer with cited page numbers + evidence regions
           |
           v
  Streamlit / Next.js viewer: highlighted boxes on source page
```

## Stack | 技术栈

- Page rendering: PyMuPDF (fitz) at 180 DPI, portrait-normalized
  中文翻译：Page rendering: PyMuPDF (fitz) at 180 DPI, portrait-normalized
- Late-interaction model: ColQwen2.5-v0.2 or ColQwen3-omni (vidore team on Hugging Face)
  中文翻译：Late-interaction model: ColQwen2.5-v0.2 or ColQwen3-omni (vidore team on Hugging Face)

> 中文翻译：Late-interaction model: ColQwen2.5-v0.2 or ColQwen3-omni (vidore team on Hugging Face)（翻译）

- Index: Vespa with multi-vector field, or Qdrant multi-vector, or AstraDB with MaxSim
  中文翻译：Index: Vespa with multi-vector field, or Qdrant multi-vector, or AstraDB with MaxSim
- Pruning: DocPruner 2026 policy (keep high-variance patches, 50% compression at < 0.5% accuracy loss)
  中文翻译：Pruning: DocPruner 2026 policy (keep high-variance patches, 50% compression at < 0.5% accuracy loss)
- OCR fallback (equations / dense tables): dots.ocr or Nougat
  中文翻译：OCR fallback (equations / dense tables): dots.ocr or Nougat
- VLM answerer: Qwen3-VL-30B self-hosted or Gemini 2.5 Pro hosted; InternVL3 as fallback
  中文翻译：VLM answerer: Qwen3-VL-30B self-hosted or Gemini 2.5 Pro hosted; InternVL3 as fallback

> 中文翻译：VLM answerer: Qwen3-VL-30B self-hosted or Gemini 2.5 Pro hosted; InternVL3 as fallback（翻译）

- Evaluation: ViDoRe v3 benchmark, M3DocVQA for multi-page reasoning
  中文翻译：Evaluation: ViDoRe v3 benchmark, M3DocVQA for multi-page reasoning
- Viewer UI: Next.js 15 with canvas overlay for evidence regions
  中文翻译：Viewer UI: Next.js 15 with canvas overlay for evidence regions

## Build It | 动手构建

> **【中文解读】** 构建步骤分为 8 个阶段：摄取 10k 页 PDF 并渲染为 PNG、ColQwen2.5 嵌入（每页 ~2048 个 patch，dim 128）并应用 DocPruner 50% 压缩、MaxSim 检索 top-k 页面、VLM 答案合成带引用、证据区域提取与可视化、OCR 回退通道（公式密集页）、ViDoRe v3 + M3DocVQA 评估、Streamlit/Next.js 查看器。

1. **Ingest.** Walk a corpus of 10k PDF pages across 10-Ks, scientific papers, and scanned documents. Render each page to a 1536x2048 PNG. Persist `{doc_id, page_num, image_path}`.
   中文翻译：1. **Ingest.** Walk a corpus of 10k PDF pages across 10-Ks, scientific papers, and scanned documents. Render each page to a 1536x2048 PNG. Persist `{doc_id, page_num, image_path}`.

2. **Embed.** Run ColQwen2.5-v0.2 on each page image. Output shape ~2048 patch embeddings of dim 128. Apply DocPruner to keep the highest-signal half. Write to Vespa multi-vector field or Qdrant multi-vector.
   中文翻译：2. **Embed.** Run ColQwen2.5-v0.2 on each page image. Output shape ~2048 patch embeddings of dim 128. Apply DocPruner to keep the highest-signal half. Write to Vespa multi-vector field or Qdrant multi-vector.

3. **Query.** For each incoming query, embed with the query tower (token-level embeddings). Run MaxSim against the index: for every query token, take the max dot-product over page patch embeddings, sum. Return top-k pages.
   中文翻译：3. **Query.** For each incoming query, embed with the query tower (token-level embeddings). Run MaxSim against the index: for every query token, take the max dot-product over page patch embeddings, sum. Return top-k pages.

4. **Synthesize.** Call Qwen3-VL-30B with the query and the top-5 page images. Prompt: "Answer using only the supplied pages. Cite each claim by (doc_id, page) and name the region (figure, table, paragraph)."
   中文翻译：4. **Synthesize.** Call Qwen3-VL-30B with the query and the top-5 page images. Prompt: "Answer using only the supplied pages. Cite each claim by (doc_id, page) and name the region (figure, table, paragraph)."

5. **Evidence regions.** Post-process the answer to extract cited regions. If the VLM emits bounding boxes (Qwen3-VL does), render them as overlays in the viewer.
   中文翻译：5. **Evidence regions.** Post-process the answer to extract cited regions. If the VLM emits bounding boxes (Qwen3-VL does), render them as overlays in the viewer.

6. **OCR fallback.** For pages identified as equation-dense (heuristic on image variance), run Nougat or dots.ocr and pass the OCR text as an extra channel alongside the image.
   中文翻译：6. **OCR fallback.** For pages identified as equation-dense (heuristic on image variance), run Nougat or dots.ocr and pass the OCR text as an extra channel alongside the image.

7. **Eval.** Run ViDoRe v3 (retrieval nDCG@5) and M3DocVQA (multi-page QA accuracy). Also run OCR-then-text pipeline on the same corpus with the same synthesizer. Produce a content-type x approach matrix.
   中文翻译：7. **Eval.** Run ViDoRe v3 (retrieval nDCG@5) and M3DocVQA (multi-page QA accuracy). Also run OCR-then-text pipeline on the same corpus with the same synthesizer. Produce a content-type x approach matrix.

8. **UI.** Streamlit prototype first; Next.js 15 production viewer with page-by-page evidence-region overlay.
   中文翻译：8. **UI.** Streamlit prototype first; Next.js 15 production viewer with page-by-page evidence-region overlay.

## Use It | 使用方法

```
$ doc-qa ask "what was the 2024 operating margin change for segment EMEA?"
[retrieve]   top-5 pages in 320ms (ColQwen2.5, MaxSim, Vespa)
[synth]      qwen3-vl-30b, 1.4s, cited (form-10k-2024, p. 88) + (..., p. 92)
answer:
  EMEA operating margin moved from 18.2% to 16.8%, a 140bp decline.
  cited: 10-K-2024.pdf p.88 (Table 4, Segment Operating Margin)
         10-K-2024.pdf p.92 (MD&A, Operating Performance)
[viewer]     open with highlighted bounding boxes overlaid on p.88 Table 4
```

## Ship It | 部署上线

`outputs/skill-doc-qa.md` describes the deliverable: a vision-first multimodal document QA system tuned to a specific corpus and evaluated against an OCR-then-text baseline on ViDoRe v3.

> `outputs/skill-doc-qa.md` 描述了交付物：一个根据特定语料库调优的视觉优先多模态文档 QA 系统，在 ViDoRe v3 上与 OCR-then-text 基线对比评估。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | ViDoRe v3 / M3DocVQA accuracy | Benchmark numbers vs OCR-text baseline and published leaderboard |
| 25 | ViDoRe v3 / M3DocVQA 准确率 | 基准数字 vs OCR-text 基线和已发布排行榜 |
| 20 | Evidence-region grounding | Fraction of cited regions that actually contain the answer span |
| 20 | 证据区域定位 | 引用区域中实际包含答案跨度的比例 |
| 20 | Storage and latency engineering | DocPruner compression ratio, index p95, answer p95 |
| 20 | 存储与延迟工程 | DocPruner 压缩比、索引 p95、答案 p95 |
| 20 | Multi-page reasoning | Accuracy on a hand-labeled 100-question multi-page set |
| 20 | 多页推理 | 手工标注的 100 题多页集合上的准确率 |
| 15 | Source-inspection UX | Viewer clarity, overlay fidelity, side-by-side comparison tools |
| 15 | 源文档查看体验 | 查看器清晰度、覆盖层保真度、并排比较工具 |
| **100** | | |

## Exercises | 练习题

1. Measure ColQwen2.5-v0.2 vs ColQwen3-omni on the same corpus. Which pages does one get right and the other miss? Add a "content class" tag to the index to route by type.
   中文翻译：在同一语料库上测量 ColQwen2.5-v0.2 vs ColQwen3-omni。哪个在某些页面上正确而另一个遗漏？向索引添加"内容类别"标签以按类型路由。

> 中文翻译：在同一语料库上测量 ColQwen2.5-v0.2 vs ColQwen3-omni。哪个在某些页面上正确而另一个遗漏？向索引添加"内容类别"标签以按类型路由。（翻译）


2. Prune embeddings aggressively (75%, 90%). Find the compression cliff: the point where ViDoRe nDCG@5 drops below the OCR baseline.
   中文翻译：激进剪枝嵌入（75%、90%）。找到压缩悬崖：ViDoRe nDCG@5 降到 OCR 基线以下的点。

3. Build a hybrid: run OCR-then-text and ColQwen in parallel, fuse with RRF, rerank with a cross-encoder. Does the hybrid beat either alone? Where does it help most?
   中文翻译：构建混合方案：并行运行 OCR-then-text 和 ColQwen，用 RRF 融合，用交叉编码器重排序。混合方案是否胜过单独使用？在哪里帮助最大？

> 中文翻译：构建混合方案：并行运行 OCR-then-text 和 ColQwen，用 RRF 融合，用交叉编码器重排序。混合方案是否胜过单独使用？在哪里帮助最大？（翻译）


4. Swap Qwen3-VL-30B for a smaller VLM (Qwen2.5-VL-7B). Measure the accuracy-per-dollar curve.
   中文翻译：将 Qwen3-VL-30B 换为更小的 VLM（Qwen2.5-VL-7B）。测量每美元准确率曲线。

5. Add handwritten-note support. Render the handwriting corpus, embed with ColQwen, measure retrieval. Compare against a handwriting OCR pipeline.
   中文翻译：添加手写笔记支持。渲染手写语料库，用 ColQwen 嵌入，测量检索。与手写 OCR 管道对比。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Late interaction | "ColPali-style retrieval" | Query tokens score against page patches independently; MaxSim aggregates |
| 晚期交互 | "ColPali 风格检索" | 查询 token 独立于页面 patch 计分；MaxSim 聚合 |
| Multi-vector | "Per-patch embedding" | Each document has many vectors, not one pooled vector |
| 多向量 | "每个 patch 的嵌入" | 每个文档有多个向量，而不是一个池化向量 |
| MaxSim | "Late-interaction scoring" | For every query token, take max similarity over document vectors; sum |
| MaxSim | "晚期交互评分" | 对每个查询 token，取文档向量上的最大相似度；求和 |
| DocPruner | "Patch compression" | 2026 pruning that keeps 50% of patches with negligible accuracy loss |
| DocPruner | "Patch 压缩" | 2026 年剪枝，保留 50% 的 patch，精度损失可忽略 |
| ViDoRe v3 | "Document-retrieval benchmark" | The 2026 standard for measuring visual-document retrieval |
| ViDoRe v3 | "文档检索基准" | 2026 年测量视觉文档检索的标准 |
| Evidence region | "Cited bounding box" | A bbox on the source page that localizes the answer span |
| 证据区域 | "引用边界框" | 源页面上定位答案跨度的边界框 |
| OCR fallback | "Equation channel" | Text pipeline used alongside vision for equation- or table-heavy pages |
| OCR 回退 | "公式通道" | 在公式或表格密集页面与视觉并用的文本管道 |

## Further Reading | 延伸阅读

- [ColPali (Illuin Tech) repository](https://github.com/illuin-tech/colpali) — reference late-interaction doc retrieval
  中文翻译：参考晚期交互文档检索
- [ColPali paper (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449) — the foundational method paper
  中文翻译：基础方法论文
- [ColQwen family on Hugging Face](https://huggingface.co/vidore) — production-ready checkpoints
  中文翻译：生产就绪的检查点
- [M3DocRAG (Adobe)](https://arxiv.org/abs/2411.04952) — multi-page multimodal RAG baseline
  中文翻译：多页多模态 RAG 基线
- [Vespa multi-vector tutorial](https://docs.vespa.ai/en/colpali.html) — reference serving stack
  中文翻译：参考服务栈
- [Qdrant multi-vector support](https://qdrant.tech/documentation/concepts/vectors/#multivectors) — alternate index
  中文翻译：备选索引
- [AstraDB multi-vector](https://docs.datastax.com/en/astra-db-serverless/databases/vector-search.html) — alternate managed index
  中文翻译：备选托管索引
- [Nougat OCR](https://github.com/facebookresearch/nougat) — equation-capable OCR fallback
  中文翻译：支持公式的 OCR 回退
