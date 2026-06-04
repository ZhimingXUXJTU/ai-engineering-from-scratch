# Document and Diagram Understanding | 文档与图表理解

> Documents are not photos. A PDF, scientific paper, invoice, or handwritten form has layout, tables, diagrams, footnotes, headers, and semantic structure that plain image understanding cannot capture. The pre-VLM stack was a pipeline: Tesseract OCR + LayoutLMv3 + table-extraction heuristics. The VLM wave replaced that with OCR-free models — Donut (2022), Nougat (2023), DocLLM (2023) — that emit structured markup directly. By 2026 the frontier is just "feed the page image to Claude Opus 4.7 at 2576px native," and the structured-markup output comes for free. This lesson reads the three-era arc of document AI.

> **【中文解读】** 文档不是照片。PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构，普通图像理解无法捕捉。文档 AI 经历了三个时代：(1) OCR 管道（Tesseract + LayoutLMv3）；(2) OCR-free（Donut、Nougat 直接从图像生成结构化输出）；(3) VLM 原生（2026 年直接将页面图像喂给 Claude Opus 4.7 即可）。

> **【拓展：文档理解在金融领域的应用】** 金融场景是文档 AI 最重要的应用领域之一：发票解析（自动提取供应商、金额、税率）、合同审查（条款比对、风险标记）、财务报表提取（资产负债表、利润表的结构化数据抽取）、KYC 文档处理（身份证、营业执照的自动识别）。2026 年的推荐方案：纯打印发票用 LayoutLMv3（成本低），混合文档用手写用 VLM 原生（PaliGemma 2 或 Qwen2.5-VL），监管场景用 OCR + VLM 交叉验证。

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

## 学习目标

- Explain the three eras of document AI: OCR pipeline, OCR-free, VLM-native.
- Describe LayoutLMv3's three input streams: text, layout (bbox), image patches, with unified masking.
- Compare Donut (OCR-free, image → markup), Nougat (scientific paper → LaTeX), DocLLM (layout-aware generative), PaliGemma 2 (VLM-native).
- Pick a document model for a new task (invoices, scientific papers, handwritten forms, Chinese receipts).

## 问题引入

"Understand this PDF" is deceptively hard. The information sits in:

- Text content (90% of the signal).
- Layout (headers, footnotes, sidebars, two-column format).
- Tables (rows, columns, merged cells).
- Figures and diagrams.
- Handwritten annotations.
- Fonts and typography (title vs body).

Raw OCR dumps the text and loses the rest. A system that cares about invoices needs to know "Total: $1,245" came from the bottom-right, not from a footnote.

## 核心概念

> **【中文解读】** 文档和图表理解是多模态 AI 的重要应用场景：OCR、表格提取、流程图解读、公式识别等。关键技术：高分辨率输入（保留文字清晰度）、版面分析（理解文档结构）、结构化输出（将视觉信息转为可处理的格式）。

> **【拓展：文档 AI 的工业应用** 文档 AI 市场巨大：合同审核、发票处理、学术论文分析等。GPT-4o 在 DocVQA 上达到 92.8%，InternVL2-26B 达到 92.7%（开源最优）。MarkItDown （Microsoft）将文档转为 Markdown，ColPali 用视觉方法替代传统 OCR 管线。


> **【拓展：文档理解的技术路线】** 文档理解有两条路线：(1) OCR-first（先用 OCR 提取文本，再用 LLM 处理）——适合纯文本文档；(2) Vision-first（直接用 VLM 处理文档图像）——适合包含图表、表格的复杂版面。GPT-4o 和 InternVL2 走 Vision-first 路线，在复杂文档理解上表现更好。


### Era 1 — OCR pipeline (pre-2021)

The classic stack:

1. PDF → image per page.
2. Tesseract (or commercial OCR) extracts text with per-word bounding boxes.
3. Layout analyzer identifies blocks (header, table, paragraph).
4. Table structure recognizer parses tables.
5. Domain rules + regex extract fields.

Works for clean printed text. Breaks on handwriting, skewed scans, complex tables, non-English scripts. Every failure mode requires a custom exception path.

### TrOCR (2021)

TrOCR (Li et al., arXiv:2109.10282) replaced Tesseract's classic CNN-CTC with a transformer encoder-decoder trained on synthetic + real text images. Clean win on handwritten and multilingual text. Still a pipeline (detector then TrOCR then layout), but the OCR step improved dramatically.

### Era 2 — OCR-free (2022-2023)

The first OCR-free models said: skip detection entirely, map image pixels to structured output directly.

Donut (Kim et al., arXiv:2111.15664):
- Encoder-decoder transformer, encoder is Swin-B.
- Output is JSON for form understanding, markdown for summarization, or any task-specific schema.
- No OCR, no layout, no detection.

Nougat (Blecher et al., arXiv:2308.13418):
- Trained specifically on scientific papers.
- Output is LaTeX / markdown.
- Handles equations, multi-column layout, figures.
- The model every arXiv-parser calls.

These are specialists, not generalists. Donut on a scientific paper fails; Nougat on an invoice fails.

### LayoutLMv3 (2022)

A different track. LayoutLMv3 (Huang et al., arXiv:2204.08387) keeps OCR but adds layout understanding:

- Three input streams: OCR text tokens, per-token 2D bounding boxes, image patches.
- Masked training objective across all three modalities (masked text, masked patches, masked layout).
- Downstream: classification, entity extraction, table QA.

LayoutLMv3 is the peak of OCR-based document understanding. Strong on forms and invoices. Requires OCR upstream. Best pre-VLM accuracy on standardized document benchmarks.

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) is LayoutLM's generative sibling. Generates free-form answers conditioned on layout tokens. Better for QA on documents; still depends on OCR input.

### Era 3 — VLM-native (2024+)

2024 VLMs became good enough to replace the pipeline entirely. Feed the full page image at high resolution to a VLM, ask the question, get an answer.

- LLaVA-NeXT 336-tile AnyRes works for small documents.
- Qwen2.5-VL dynamic-resolution handles 2048+ pixels natively.
- Claude Opus 4.7 supports 2576px documents.
- PaliGemma 2 (April 2025) trains specifically for documents + handwriting.

The gap between VLM-native and OCR-pipeline closed rapidly. By 2026, VLM-native wins on:

- Scene text (hand-written + printed, mixed scripts).
- Complex tables with merged cells.
- Math equations embedded in text.
- Figures with text annotations.

OCR pipelines still win on:

- Pure-scan workloads at massive scale where per-page latency matters.
- Pipeline reliability (deterministic failures vs VLM hallucinations).
- Regulated environments requiring auditable OCR output.

### The Claude 4.7 / GPT-5 frontier

At 2576-pixel native input, frontier VLMs do document understanding at near-human accuracy. The benchmark numbers from early 2026:

- DocVQA: Claude 4.7 ~95.1, PaliGemma 2 ~88.4, Nougat ~77.3, pipelined LayoutLMv3 ~83.
- ChartQA: Claude 4.7 ~92.2, GPT-4V ~78.
- VisualMRC: Claude 4.7 ~94.

The closed-model gap is mostly resolution and base-LLM scale. Open models at 7B are a few points behind but catching up.

### Math equations and LaTeX output

Scientific papers need exact LaTeX output for equations. Nougat was trained on this. VLMs trained with LaTeX targets (Qwen2.5-VL-Math, Nougat derivatives) produce usable LaTeX. Without explicit LaTeX training, VLMs produce readable but imprecise transcriptions.

For scientific-paper pipelines in 2026: chain Nougat on the PDF, then a VLM on tricky pages.

### Handwriting

Still the hardest sub-task. Mixed printed + handwritten (doctors' notes, filled forms) is where OCR pipelines still beat VLMs for cost. Handwritten-only VLMs are improving (Claude 4.7, PaliGemma 2).

### 2026 recipe

For a new document-AI project:

- Pure-printed invoices at scale: LayoutLMv3 + rules, cost-efficient.
- Mixed documents (scientific + handwritten + forms): VLM-native (PaliGemma 2 or Qwen2.5-VL).
- Full arXiv ingestion: Nougat for math, VLM for figures.
- Regulatory: OCR pipeline + VLM validator for cross-check.

## 用框架实现

`code/main.py`:

- A toy layout-aware tokenizer: given (text, bbox) pairs, produces the LayoutLMv3-style input.
- A Donut-style task schema generator: JSON template for forms.
- A comparison of token budgets per page across OCR-pipeline, Donut, Nougat, and VLM-native.

## 产出物

This lesson produces `outputs/skill-document-ai-stack-picker.md`. Given a document-AI project (domain, scale, quality, regulatory), picks between OCR pipeline, OCR-free specialist, and VLM-native.

## 练习题

1. Your project is 10M invoices per day. Which stack minimizes cost-per-page without losing accuracy? 你的项目每天处理 1000 万张发票。哪种方案能在不损失准确率的情况下最小化每页成本？

2. Why does LayoutLMv3 outperform pure-CLIP-VLMs on form QA but underperform at scene-text? What does the bbox stream give up? 为什么 LayoutLMv3 在表单 QA 上优于纯 CLIP VLM，但在场景文本上表现不佳？bbox 流放弃了什么？

3. Nougat generates LaTeX. Propose a test case where VLM-native output beats Nougat on LaTeX fidelity, and a case where Nougat wins. Nougat 生成 LaTeX。设计一个 VLM 原生输出在 LaTeX 保真度上胜过 Nougat 的测试用例，以及一个 Nougat 胜出的用例。

4. Read PaliGemma 2 paper (Google, 2024). What was the key training-data addition that lifted document accuracy vs PaliGemma 1? 阅读 PaliGemma 2 论文。相比 PaliGemma 1，什么关键训练数据提升了文档准确率？

5. Design a regulatory-safe hybrid: OCR pipeline as primary, VLM as secondary cross-check. How do you resolve disagreement? 设计一个监管安全的混合方案：OCR 管道为主，VLM 为辅交叉检查。如何处理不一致？

## 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## 延伸阅读

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
