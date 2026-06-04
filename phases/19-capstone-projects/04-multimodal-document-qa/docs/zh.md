# Capstone 04 — Multimodal Document QA (Vision-First PDF, Tables, Charts) | 文档问答 多模态 结业

> The 2026 document-QA frontier moved away from OCR-then-text and toward vision-first late interaction. ColPali, ColQwen2.5, and ColQwen3-omni treat each PDF page as an image, embed it with multi-vector late interaction, and let the query attend to patches directly. On financial 10-Ks, scientific papers, and handwritten notes this pattern beats OCR-first by a large margin. Build the pipeline end to end on 10k pages and publish the side-by-side against OCR-then-text.

> **【中文解读】** 本节是综合项目——构建多模态文档问答系统，处理文本、图像和表格。


**类型：** 结业项目
**语言：** Python (pipeline), TypeScript (viewer UI)
**前置知识：** Phase 4 (computer vision), Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 17 (infrastructure)
**涉及的 Phase：** P4 · P5 · P7 · P11 · P12 · P17
**预计时间：** 30 hours

## Problem

> **【中文解读】** 本节阐述文档问答从"先 OCR 再文本"到"视觉优先"的范式转变。企业 PDF 中的旋转表格、公式、图表、手写批注是 OCR 管道的噩梦。2026 年的答案是 ColPali/ColQwen 系列的晚期交互多向量检索——将每页 PDF 当作图像，让查询直接关注到图像块（patch）。在图表、表格和手写内容上，视觉优先方案显著优于 OCR 文本方案。

> **【拓展：视觉文档检索前沿】** ColPali 由 Illuin Tech 在 2024 年提出（arXiv:2407.01449），将文档检索从文本匹配推向视觉匹配。ColQwen2.5 和 ColQwen3-omni 进一步提升精度。在 ViDoRe v3 基准上，视觉优先检索 nDCG@5 比 OCR-then-text 高出显著幅度。代价是存储膨胀——每页约 2048 个 patch 向量，DocPruner 通过 50% 剪枝将存储减半，精度损失 < 0.5%。Vespa 和 Qdrant 都支持多向量字段和 MaxSim 检索。

Enterprises sit on PDFs that OCR pipelines mangle: scanned 10-Ks with rotated tables, scientific papers dense with equations, charts that only make sense as images, handwritten annotations. Treating these as text-first means losing half the signal. The 2026 answer is late-interaction multi-vector retrieval on raw page images. ColPali (Illuin Tech) introduced it; ColQwen2.5-v0.2 and ColQwen3-omni pushed accuracy. On ViDoRe v3, vision-first retrieval scores above OCR-then-text by meaningful margins — and the gap widens on charts, tables, and handwriting.

The trade-off is storage and latency. A ColQwen embedding is ~2048 patch vectors per page, not a single 1024-dim vector. Raw storage balloons. DocPruner (2026) brings 50% pruning without measurable accuracy loss. You will index 10k pages, measure ViDoRe v3 nDCG@5, serve answers under 2s, and compare directly against an OCR-then-text baseline.

## Concept

> **【中文解读】** 晚期交互（Late Interaction）是指每个查询 token 与每个页面 patch token 独立计算相似度，取每个查询 token 的最大得分后求和。这比单池化向量匹配更精细。多向量索引（Vespa/Qdrant/AstraDB）存储每个页面的 patch 嵌入并在检索时执行 MaxSim。答案生成使用视觉语言模型（Qwen3-VL-30B/Gemini 2.5 Pro），带证据区域定位和页码引用。

> **【拓展：多模态 VLM 选型】** 2026 年文档问答的主流 VLM 包括：Qwen3-VL-30B（自托管最优）、Gemini 2.5 Pro（API 调用最优）、InternVL3（开源备选）。对于公式密集页面，Nougat OCR 作为补充文本通道。评估采用二维矩阵：横轴内容类型（文本段落/密集表格/图表/手写/公式），纵轴检索方法（视觉优先/OCR-then-text/混合），每个单元格计算 nDCG@5 和答案准确率。

Late interaction means every query token scores against every patch token, and the maximum score per query token is summed. You get fine-grained matching without needing a single pooled vector. A multi-vector index (Vespa, Qdrant multi-vector, or AstraDB) stores the per-patch embeddings and runs MaxSim at retrieval time.

The answerer is a vision-language model that takes the query plus the top-k retrieved pages as images and writes an answer with evidence regions (bounding boxes or page references). Qwen3-VL-30B, Gemini 2.5 Pro, and InternVL3 are the 2026 frontier choices. For equations and scientific notation, an OCR fallback (Nougat, dots.ocr) is spliced in as an optional text channel.

Evaluation is a two-dimensional matrix. One axis: content type (plain text paragraphs, dense tables, bar/line charts, handwritten notes, equations). Other axis: retrieval approach (vision-first late interaction vs OCR-then-text vs hybrid). Each cell gets nDCG@5 and answer accuracy. The report is the deliverable.

## 架构 | 架构

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

## Stack

- Page rendering: PyMuPDF (fitz) at 180 DPI, portrait-normalized
- Late-interaction model: ColQwen2.5-v0.2 or ColQwen3-omni (vidore team on Hugging Face)
- Index: Vespa with multi-vector field, or Qdrant multi-vector, or AstraDB with MaxSim
- Pruning: DocPruner 2026 policy (keep high-variance patches, 50% compression at < 0.5% accuracy loss)
- OCR fallback (equations / dense tables): dots.ocr or Nougat
- VLM answerer: Qwen3-VL-30B self-hosted or Gemini 2.5 Pro hosted; InternVL3 as fallback
- Evaluation: ViDoRe v3 benchmark, M3DocVQA for multi-page reasoning
- Viewer UI: Next.js 15 with canvas overlay for evidence regions

## 动手实现 | 动手构建

> **【中文解读】** 构建步骤分为 8 个阶段：摄取 10k 页 PDF 并渲染为 PNG、ColQwen2.5 嵌入（每页 ~2048 个 patch，dim 128）并应用 DocPruner 50% 压缩、MaxSim 检索 top-k 页面、VLM 答案合成带引用、证据区域提取与可视化、OCR 回退通道（公式密集页）、ViDoRe v3 + M3DocVQA 评估、Streamlit/Next.js 查看器。

1. **Ingest.** Walk a corpus of 10k PDF pages across 10-Ks, scientific papers, and scanned documents. Render each page to a 1536x2048 PNG. Persist `{doc_id, page_num, image_path}`.

2. **Embed.** Run ColQwen2.5-v0.2 on each page image. Output shape ~2048 patch embeddings of dim 128. Apply DocPruner to keep the highest-signal half. Write to Vespa multi-vector field or Qdrant multi-vector.

3. **Query.** For each incoming query, embed with the query tower (token-level embeddings). Run MaxSim against the index: for every query token, take the max dot-product over page patch embeddings, sum. Return top-k pages.

4. **Synthesize.** Call Qwen3-VL-30B with the query and the top-5 page images. Prompt: "Answer using only the supplied pages. Cite each claim by (doc_id, page) and name the region (figure, table, paragraph)."

5. **Evidence regions.** Post-process the answer to extract cited regions. If the VLM emits bounding boxes (Qwen3-VL does), render them as overlays in the viewer.

6. **OCR fallback.** For pages identified as equation-dense (heuristic on image variance), run Nougat or dots.ocr and pass the OCR text as an extra channel alongside the image.

7. **Eval.** Run ViDoRe v3 (retrieval nDCG@5) and M3DocVQA (multi-page QA accuracy). Also run OCR-then-text pipeline on the same corpus with the same synthesizer. Produce a content-type × approach matrix.

8. **UI.** Streamlit prototype first; Next.js 15 production viewer with page-by-page evidence-region overlay.

## 用框架实现 | 使用方法

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

## 产出物 | 部署上线

`outputs/skill-doc-qa.md` describes the deliverable: a vision-first multimodal document QA system tuned to a specific corpus and evaluated against an OCR-then-text baseline on ViDoRe v3.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | ViDoRe v3 / M3DocVQA accuracy | Benchmark numbers vs OCR-text baseline and published leaderboard |
| 20 | Evidence-region grounding | Fraction of cited regions that actually contain the answer span |
| 20 | Storage and latency engineering | DocPruner compression ratio, index p95, answer p95 |
| 20 | Multi-page reasoning | Accuracy on a hand-labeled 100-question multi-page set |
| 15 | Source-inspection UX | Viewer clarity, overlay fidelity, side-by-side comparison tools |
| **100** | | |

## 练习题 | 练习题

1. Measure ColQwen2.5-v0.2 vs ColQwen3-omni on the same corpus. Which pages does one get right and the other miss? Add a "content class" tag to the index to route by type.

2. Prune embeddings aggressively (75%, 90%). Find the compression cliff: the point where ViDoRe nDCG@5 drops below the OCR baseline.

3. Build a hybrid: run OCR-then-text and ColQwen in parallel, fuse with RRF, rerank with a cross-encoder. Does the hybrid beat either alone? Where does it help most?

4. Swap Qwen3-VL-30B for a smaller VLM (Qwen2.5-VL-7B). Measure the accuracy-per-dollar curve.

5. Add handwritten-note support. Render the handwriting corpus, embed with ColQwen, measure retrieval. Compare against a handwriting OCR pipeline.

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Late interaction | "ColPali-style retrieval" | Query tokens score against page patches independently; MaxSim aggregates |
| Multi-vector | "Per-patch embedding" | Each document has many vectors, not one pooled vector |
| MaxSim | "Late-interaction scoring" | For every query token, take max similarity over document vectors; sum |
| DocPruner | "Patch compression" | 2026 pruning that keeps 50% of patches with negligible accuracy loss |
| ViDoRe v3 | "Document-retrieval benchmark" | The 2026 standard for measuring visual-document retrieval |
| Evidence region | "Cited bounding box" | A bbox on the source page that localizes the answer span |
| OCR fallback | "Equation channel" | Text pipeline used alongside vision for equation- or table-heavy pages |

## 延伸阅读 | 延伸阅读

- [ColPali (Illuin Tech) repository](https://github.com/illuin-tech/colpali) — reference late-interaction doc retrieval
- [ColPali paper (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449) — the foundational method paper
- [ColQwen family on Hugging Face](https://huggingface.co/vidore) — production-ready checkpoints
- [M3DocRAG (Adobe)](https://arxiv.org/abs/2411.04952) — multi-page multimodal RAG baseline
- [Vespa multi-vector tutorial](https://docs.vespa.ai/en/colpali.html) — reference serving stack
- [Qdrant multi-vector support](https://qdrant.tech/documentation/concepts/vectors/#multivectors) — alternate index
- [AstraDB multi-vector](https://docs.datastax.com/en/astra-db-serverless/databases/vector-search.html) — alternate managed index
- [Nougat OCR](https://github.com/facebookresearch/nougat) — equation-capable OCR fallback
