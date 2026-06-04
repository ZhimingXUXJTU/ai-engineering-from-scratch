# ColPali and Vision-Native Document RAG | ColPali 视觉原生文档 RAG

> Traditional RAG parses PDFs into text, splits into chunks, embeds chunks, stores vectors. Every step loses signal: OCR drops chart data, chunking breaks table rows, text embeddings ignore figures. ColPali (Faysse et al., July 2024) asked the simpler question: why extract text at all? Embed the page image directly via PaliGemma, use ColBERT-style late interaction for retrieval, and keep all the layout, figures, fonts, and formatting signal the document carries. Published benchmarks: 20-40% better end-to-end accuracy than text-RAG on visually-rich documents. ColQwen2, ColSmol, and VisRAG extended the pattern. This lesson reads the vision-native RAG thesis and builds a tiny ColPali-like indexer.

> **【中文解读】** 传统 RAG 在 PDF 上表现差，因为每一步都在丢失信号：OCR 丢图表、分块破坏表格行、文本嵌入忽略图片。ColPali 问了一个更简单的问题：为什么要提取文本？直接用 PaliGemma 嵌入页面图像，用 ColBERT 风格的 MaxSim 延迟交互进行检索，保留文档的全部布局、图表、字体和格式信号。在视觉丰富文档上比文本 RAG 准确率高 20-40%。

> **【拓展：ColPali 在金融 RAG 中的应用】** 金融报告是最典型的视觉丰富文档——Q3 营收增长通常在图表中，合同签名块是布局事实而非文本事实。ColPali 直接嵌入页面图像，保留了完整的视觉信号，非常适合金融报告、合同、发票等场景。存储开销约为文本 RAG 的 5-10 倍（经 PQ 压缩后），但在准确率上的提升通常值得这个成本。

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

## 学习目标

- Explain the difference between bi-encoder retrieval (one vector per document) and late-interaction retrieval (many vectors per document).
- Describe ColBERT's MaxSim operation and how ColPali generalizes it from text tokens to image patches.
- Build a tiny ColPali-like indexer: page → patch embeddings → MaxSim over query-term embeddings → top-k pages.
- Compare ColPali + Qwen2.5-VL generator vs text-RAG + GPT-4 on an invoices / financial reports use case.

## 问题引入

Text-RAG on PDFs throws away most of the document. A financial report's Q3 revenue growth is usually in a chart; a medical report's findings are in annotated images; a legal contract's signature block is a layout fact, not a text fact.

The text-RAG pipeline:

1. PDF → text via OCR / pdftotext.
2. Text → 300-500 token chunks.
3. Chunk → bi-encoder embedding (one vector).
4. User query → embedding → cosine similarity → top-k chunks.
5. Chunks + query → LLM.

Five lossy steps. Charts not captured. Tables broken across chunks. Multi-column layout flattens. Figure annotations disappear.

ColPali's fix: skip OCR, embed the page image directly. Use ColBERT-style late interaction for retrieval so the model can attend to fine-grained patches at query time.

## 核心概念

> **【中文解读】** ColPali 用纯视觉方法实现 RAG：不经过 OCR，直接将文档页面作为图像编码为向量，用视觉相似度检索。ColPali 的核心创新是 MaxSim 模式——query 的每个 token 嵌入与文档页面的每个 patch 嵌入做最大相似度匹配，然后求和。

> **【拓展：视觉原生 RAG 的优势** 传统 RAG 管线（OCR -> 文本 -> 嵌入 -> 检索）在复杂版面（表格、图表、公式）上经常失败。ColPali 直接在视觉层面匹配，无需 OCR，在包含图表和表格的文档检索上比传统方法提升 30-50%。缺点是需要更多存储（每页一个向量）。


> **【拓展：ColPali 的效率分析】** ColPali 在检索延迟上与传统方法相当（约 50ms/query），但在包含图表和表格的文档上准确率提升 30-50%。缺点是索引存储成本更高——每页需要一个 1280 维向量而非传统方法的 768 维。ColPali-2 进一步提升了效率并支持跨语言文档检索。


### ColBERT (2020)

ColBERT (Khattab & Zaharia, arXiv:2004.12832) is a text retrieval method. Instead of one vector per document, it produces one vector per token. At query time:

- Query tokens get their own embeddings (N_q vectors).
- Document tokens get embeddings (N_d vectors, typically cached).
- Score = sum over query tokens of max over document tokens of cosine similarity: Σ_i max_j cos(q_i, d_j).

This is the MaxSim operation. Each query token "picks" its best-matching document token. The final score is the sum.

Pros: strong recall, handles term-level semantics. Cons: N_d vectors per document, storage expensive.

### ColPali

ColPali (Faysse et al., arXiv:2407.01449) applies the ColBERT pattern to images.

- Each page is encoded by PaliGemma (ViT + language) into patch embeddings: N_p vectors per page.
- Each user query (text) is encoded into query-token embeddings: N_q vectors.
- Score = Σ_i max_j cos(q_i, p_j), i.e., MaxSim over query-text-tokens and page-image-patches.
- Retrieve top-k pages by total score.

At document-ingestion time: embed every page with PaliGemma, store all patch embeddings. At query time: embed the query tokens, compute MaxSim against all stored page embeddings, return top-k pages.

Pros: end-to-end beats text-RAG by 20-40% on visually rich documents. Each patch-vector captures local layout and content.

Cons: N_p patches × 4-byte floats × D-dim vectors per page = storage grows fast. Mitigated by PQ / OPQ quantization.

### ColQwen2 and ColSmol

ColQwen2 (illuin-tech, 2024-2025) swaps PaliGemma for Qwen2-VL. Better base encoder, better retrieval.

ColSmol is the smaller-scale variant for local / edge use. A ColSmol retriever at ~1B params runs on consumer GPU.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) is a different variant: instead of MaxSim on patches, pool each page into a single vector with a VLM then bi-encoder retrieve. Faster indexing + smaller storage, weaker recall.

The quality-vs-cost trade-off: ColPali for quality, VisRAG for scale.

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) extends multi-modal retrieval to multi-page multi-document reasoning. Retrieves pages across documents, composes a multi-page context for the VLM.

### ViDoRe — the benchmark

ColPali's companion benchmark. Visual Document Retrieval Evaluation. Tasks include financial reports, scientific papers, administrative documents, medical records, manuals. Metric: nDCG@5.

ColPali-v1 scores ~80% nDCG@5 on ViDoRe; text-RAG on the same documents scores ~50-60%.

### The end-to-end RAG pipeline

For a vision-native RAG:

1. Ingest: PDF → page images → PaliGemma encoding → store all patch embeddings.
2. Query: user text → query-token embeddings → MaxSim against all indexed pages → top-k pages.
3. Generate: top-k page images + query → VLM (Qwen2.5-VL or Claude) → answer.

No OCR anywhere. Figures, charts, fonts, layout all flow into the answer.

### Storage math

A 50-page financial report with 729 patches per page and 128-dim embeddings:

- ColPali: 50 * 729 * 128 * 4 bytes = ~18 MB raw, ~4 MB after PQ.
- Text-RAG: 50 chunks * 768-dim * 4 bytes = ~150 kB.

ColPali is ~30x more storage per document. At scale, OPQ / PQ brings it down to ~5-10x, usually tolerable.

### When text-RAG still wins

- Pure-text documents with no layout signal (wiki articles, chat logs). Text-RAG is simpler and storage-cheaper.
- Multi-million-page archives where storage dominates cost.
- Strict regulatory requirements demanding extractable OCR text alongside the retrieval.

For everything else in 2026 — financial reports, scientific papers, legal contracts, medical records, UX documentation — vision-native RAG wins.

## 用框架实现

`code/main.py`:

- Toy patch encoder: maps a "page" (small grid of feature vectors) to an array of patch embeddings.
- MaxSim scorer: computes the ColBERT-style score between a query token embedding set and a page patch set.
- Indexes 5 toy pages, runs 3 queries, returns top-k with scores.

## 产出物

This lesson produces `outputs/skill-vision-rag-designer.md`. Given a document-RAG project, picks ColPali / ColQwen2 / VisRAG / text-RAG and sizes the storage.

## 练习题

1. A 200-page annual report at 729 patches per page, 128-dim emb, 4-byte floats. Compute raw storage and PQ-compressed (8x) storage. 200 页年报，729 patch/页，128 维嵌入，4 字节浮点。计算原始存储和 PQ 压缩（8 倍）后的存储。

2. MaxSim is Σ_i max_j cos(q_i, p_j). What does this sum capture that a simple mean similarity does not? MaxSim 是 Σ_i max_j cos(q_i, p_j)。这个求和捕获了什么简单均值相似度无法捕获的信息？

3. ColPali indexes pages as patch sets. What changes if we instead index at the word level (as ColBERT does)? Trade-offs? ColPali 以 patch 集索引页面。如果改为词级别索引（如 ColBERT），会怎样？有什么取舍？

4. Design the end-to-end pipeline for a 1M-page corpus with a latency budget of 500ms per query. Pick ColQwen2 / VisRAG and justify. 设计 100 万页语料库的端到端管道，每查询延迟预算 500ms。选择 ColQwen2 / VisRAG 并论证。

5. Read M3DocRAG (arXiv:2411.04952). Describe the multi-page attention pattern and how it differs from single-page ColPali retrieval. 阅读 M3DocRAG。描述其多页注意力模式及与单页 ColPali 检索的区别。

## 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## 延伸阅读

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
