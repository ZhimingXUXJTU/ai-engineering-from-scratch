# Document and Diagram Understanding | 文档与图表理解

> Documents are not photos. A PDF, scientific paper, invoice, or handwritten form has layout, tables, diagrams, footnotes, headers, and semantic structure that plain image understanding cannot capture. The pre-VLM stack was a pipeline: Tesseract OCR + LayoutLMv3 + table-extraction heuristics. The VLM wave replaced that with OCR-free models — Donut (2022), Nougat (2023), DocLLM (2023) — that emit structured markup directly. By 2026 the frontier is just "feed the page image to Claude Opus 4.7 at 2576px native," and the structured-markup output comes for free. This lesson reads the three-era arc of document AI.

> **【中文解读】** 文档不是照片。PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构，普通图像理解无法捕捉。文档 AI 经历了三个时代：(1) OCR 管道（Tesseract + LayoutLMv3）；(2) OCR-free（Donut、Nougat 直接从图像生成结构化输出）；(3) VLM 原生（2026 年直接将页面图像喂给 Claude Opus 4.7 即可）。

> **【拓展：文档理解在金融领域的应用】** 金融场景是文档 AI 最重要的应用领域之一：发票解析（自动提取供应商、金额、税率）、合同审查（条款比对、风险标记）、财务报表提取（资产负债表、利润表的结构化数据抽取）、KYC 文档处理（身份证、营业执照的自动识别）。2026 年的推荐方案：纯打印发票用 LayoutLMv3（成本低），混合文档用手写用 VLM 原生（PaliGemma 2 或 Qwen2.5-VL），监管场景用 OCR + VLM 交叉验证。

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

## Learning Objectives

- Explain the three eras of document AI: OCR pipeline, OCR-free, VLM-native.
  中文翻译：解释文档 AI 的三个时代：OCR 管道、无 OCR、VLM 原生。
- Describe LayoutLMv3's three input streams: text, layout (bbox), image patches, with unified masking.
  中文翻译：描述 LayoutLMv3 的三个输入流：文本、布局（bbox）、图像 patch，配合统一掩码。
- Compare Donut (OCR-free, image → markup), Nougat (scientific paper → LaTeX), DocLLM (layout-aware generative), PaliGemma 2 (VLM-native).
  中文翻译：比较 Donut（无 OCR，图像→标记）、Nougat（科学论文→LaTeX）、DocLLM（布局感知生成）、PaliGemma 2（VLM 原生）。
- Pick a document model for a new task (invoices, scientific papers, handwritten forms, Chinese receipts).
  中文翻译：为新任务选择文档模型（发票、科学论文、手写表单、中文收据）。

## The Problem | 问题引入

"Understand this PDF" is deceptively hard. The information sits in:

> "理解这个 PDF"看似简单实则困难。信息存在于：

- Text content (90% of the signal).
  中文翻译：文本内容（90% 的信号）。
- Layout (headers, footnotes, sidebars, two-column format).
  中文翻译：布局（标题、脚注、侧边栏、双栏格式）。
- Tables (rows, columns, merged cells).
  中文翻译：表格（行、列、合并单元格）。
- Figures and diagrams.
  中文翻译：图表和图示。
- Handwritten annotations.
  中文翻译：手写注释。
- Fonts and typography (title vs body).
  中文翻译：字体和排版（标题 vs 正文）。

Raw OCR dumps the text and loses the rest. A system that cares about invoices needs to know "Total: $1,245" came from the bottom-right, not from a footnote.

> 原始 OCR 只提取文本，丢失其余信息。关心发票的系统需要知道"总计：$1,245"来自右下角，而非脚注。

## The Concept | 核心概念

> **【中文解读】** 文档和图表理解是多模态 AI 的重要应用场景：OCR、表格提取、流程图解读、公式识别等。关键技术：高分辨率输入（保留文字清晰度）、版面分析（理解文档结构）、结构化输出（将视觉信息转为可处理的格式）。

> **【拓展：文档 AI 的工业应用** 文档 AI 市场巨大：合同审核、发票处理、学术论文分析等。GPT-4o 在 DocVQA 上达到 92.8%，InternVL2-26B 达到 92.7%（开源最优）。MarkItDown （Microsoft）将文档转为 Markdown，ColPali 用视觉方法替代传统 OCR 管线。


> **【拓展：文档理解的技术路线】** 文档理解有两条路线：(1) OCR-first（先用 OCR 提取文本，再用 LLM 处理）——适合纯文本文档；(2) Vision-first（直接用 VLM 处理文档图像）——适合包含图表、表格的复杂版面。GPT-4o 和 InternVL2 走 Vision-first 路线，在复杂文档理解上表现更好。


### Era 1 — OCR pipeline (pre-2021)

The classic stack:

> 经典技术栈：

1. PDF → image per page.
   中文翻译：PDF → 每页图像。
2. Tesseract (or commercial OCR) extracts text with per-word bounding boxes.
   中文翻译：Tesseract（或商业 OCR）提取文本并标注每个词的边界框。
3. Layout analyzer identifies blocks (header, table, paragraph).
   中文翻译：布局分析器识别块（标题、表格、段落）。
4. Table structure recognizer parses tables.
   中文翻译：表格结构识别器解析表格。
5. Domain rules + regex extract fields.
   中文翻译：领域规则 + 正则表达式提取字段。

Works for clean printed text. Breaks on handwriting, skewed scans, complex tables, non-English scripts. Every failure mode requires a custom exception path.

> 适用于清洁印刷文本。在手写、倾斜扫描、复杂表格、非英文文字上失败。每种失败模式都需要自定义异常处理。

### TrOCR (2021)

TrOCR (Li et al., arXiv:2109.10282) replaced Tesseract's classic CNN-CTC with a transformer encoder-decoder trained on synthetic + real text images. Clean win on handwritten and multilingual text. Still a pipeline (detector then TrOCR then layout), but the OCR step improved dramatically.

> TrOCR 用在合成+真实文本图像上训练的 Transformer 编码器-解码器替代了 Tesseract 的经典 CNN-CTC。在手写和多语言文本上取得明显优势。仍是管道（检测器→TrOCR→布局），但 OCR 步骤大幅改进。

### Era 2 — OCR-free (2022-2023)

The first OCR-free models said: skip detection entirely, map image pixels to structured output directly.

> 第一代无 OCR 模型提出：完全跳过检测，直接将图像像素映射为结构化输出。

Donut (Kim et al., arXiv:2111.15664):
- Encoder-decoder transformer, encoder is Swin-B.
- Output is JSON for form understanding, markdown for summarization, or any task-specific schema.
- No OCR, no layout, no detection.

> Donut：编码器-解码器 Transformer，编码器为 Swin-B。输出是 JSON（表单理解）、markdown（摘要）或任务特定 schema。无需 OCR、无需布局、无需检测。

Nougat (Blecher et al., arXiv:2308.13418):
- Trained specifically on scientific papers.
- Output is LaTeX / markdown.
- Handles equations, multi-column layout, figures.
- The model every arXiv-parser calls.

> Nougat：专门在科学论文上训练。输出 LaTeX/markdown。处理公式、多栏布局、图表。每个 arXiv 解析器都调用此模型。

These are specialists, not generalists. Donut on a scientific paper fails; Nougat on an invoice fails.

> 这些是专家模型，不是通才。Donut 在科学论文上失败；Nougat 在发票上失败。

### LayoutLMv3 (2022)

A different track. LayoutLMv3 (Huang et al., arXiv:2204.08387) keeps OCR but adds layout understanding:

> 不同的路线。LayoutLMv3 保留 OCR 但添加布局理解：

- Three input streams: OCR text tokens, per-token 2D bounding boxes, image patches.
  中文翻译：三个输入流：OCR 文本 token、每个 token 的 2D 边界框、图像 patch。
- Masked training objective across all three modalities (masked text, masked patches, masked layout).
  中文翻译：跨三个模态的掩码训练目标（掩码文本、掩码 patch、掩码布局）。
- Downstream: classification, entity extraction, table QA.
  中文翻译：下游任务：分类、实体提取、表格 QA。

LayoutLMv3 is the peak of OCR-based document understanding. Strong on forms and invoices. Requires OCR upstream. Best pre-VLM accuracy on standardized document benchmarks.

> LayoutLMv3 是基于 OCR 的文档理解的巅峰。在表单和发票上很强。需要上游 OCR。在标准化文档基准上是 VLM 前的最佳。

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) is LayoutLM's generative sibling. Generates free-form answers conditioned on layout tokens. Better for QA on documents; still depends on OCR input.

> DocLLM 是 LayoutLM 的生成式兄弟。基于布局 token 生成自由形式回答。更适合文档 QA；仍依赖 OCR 输入。

### Era 3 — VLM-native (2024+)

2024 VLMs became good enough to replace the pipeline entirely. Feed the full page image at high resolution to a VLM, ask the question, get an answer.

> 2024 年 VLM 变得足够好，可以完全替代管道。将完整页面图像以高分辨率喂给 VLM，提问，获得答案。

- LLaVA-NeXT 336-tile AnyRes works for small documents.
  中文翻译：LLaVA-NeXT 336-tile AnyRes 适用于小文档。
- Qwen2.5-VL dynamic-resolution handles 2048+ pixels natively.
  中文翻译：Qwen2.5-VL 动态分辨率原生处理 2048+ 像素。
- Claude Opus 4.7 supports 2576px documents.
  中文翻译：Claude Opus 4.7 支持 2576px 文档。
- PaliGemma 2 (April 2025) trains specifically for documents + handwriting.
  中文翻译：PaliGemma 2（2025 年 4 月）专门为文档+手写训练。

The gap between VLM-native and OCR-pipeline closed rapidly. By 2026, VLM-native wins on:

> VLM 原生和 OCR 管道之间的差距迅速缩小。到 2026 年，VLM 原生在以下方面胜出：

- Scene text (hand-written + printed, mixed scripts).
  中文翻译：场景文本（手写+印刷，混合文字）。
- Complex tables with merged cells.
  中文翻译：带合并单元格的复杂表格。
- Math equations embedded in text.
  中文翻译：嵌入文本的数学公式。
- Figures with text annotations.
  中文翻译：带文本注释的图表。

OCR pipelines still win on:

> OCR 管道仍在以下方面胜出：

- Pure-scan workloads at massive scale where per-page latency matters.
  中文翻译：大规模纯扫描工作负载，每页延迟很重要。
- Pipeline reliability (deterministic failures vs VLM hallucinations).
  中文翻译：管道可靠性（确定性失败 vs VLM 幻觉）。
- Regulated environments requiring auditable OCR output.
  中文翻译：需要可审计 OCR 输出的监管环境。

### The Claude 4.7 / GPT-5 frontier

At 2576-pixel native input, frontier VLMs do document understanding at near-human accuracy. The benchmark numbers from early 2026:

> 在 2576 像素原生输入下，前沿 VLM 以接近人类的准确率做文档理解。2026 年初的基准数据：

- DocVQA: Claude 4.7 ~95.1, PaliGemma 2 ~88.4, Nougat ~77.3, pipelined LayoutLMv3 ~83.
  中文翻译：DocVQA：Claude 4.7 约 95.1，PaliGemma 2 约 88.4，Nougat 约 77.3，管道式 LayoutLMv3 约 83。
- ChartQA: Claude 4.7 ~92.2, GPT-4V ~78.
  中文翻译：ChartQA：Claude 4.7 约 92.2，GPT-4V 约 78。
- VisualMRC: Claude 4.7 ~94.
  中文翻译：VisualMRC：Claude 4.7 约 94。

The closed-model gap is mostly resolution and base-LLM scale. Open models at 7B are a few points behind but catching up.

> 闭源模型的差距主要在分辨率和基础 LLM 规模。7B 开源模型落后几个百分点但正在追赶。

### Math equations and LaTeX output

Scientific papers need exact LaTeX output for equations. Nougat was trained on this. VLMs trained with LaTeX targets (Qwen2.5-VL-Math, Nougat derivatives) produce usable LaTeX. Without explicit LaTeX training, VLMs produce readable but imprecise transcriptions.

> 科学论文需要精确的 LaTeX 公式输出。Nougat 在此上训练。使用 LaTeX 目标训练的 VLM（Qwen2.5-VL-Math、Nougat 衍生物）产生可用的 LaTeX。没有显式 LaTeX 训练的 VLM 产生可读但不精确的转录。

For scientific-paper pipelines in 2026: chain Nougat on the PDF, then a VLM on tricky pages.

> 2026 年科学论文管道建议：先用 Nougat 处理 PDF，再用 VLM 处理棘手页面。

### Handwriting

Still the hardest sub-task. Mixed printed + handwritten (doctors' notes, filled forms) is where OCR pipelines still beat VLMs for cost. Handwritten-only VLMs are improving (Claude 4.7, PaliGemma 2).

> 仍然是最难的子任务。印刷+手写混合（医生笔记、填写的表单）是 OCR 管道在成本上仍然胜过 VLM 的场景。纯手写 VLM 正在改进（Claude 4.7、PaliGemma 2）。

### 2026 recipe

For a new document-AI project:

> 对于新的文档 AI 项目：

- Pure-printed invoices at scale: LayoutLMv3 + rules, cost-efficient.
  中文翻译：大规模纯印刷发票：LayoutLMv3 + 规则，成本高效。
- Mixed documents (scientific + handwritten + forms): VLM-native (PaliGemma 2 or Qwen2.5-VL).
  中文翻译：混合文档（科学+手写+表单）：VLM 原生（PaliGemma 2 或 Qwen2.5-VL）。
- Full arXiv ingestion: Nougat for math, VLM for figures.
  中文翻译：完整 arXiv 处理：Nougat 处理数学，VLM 处理图表。
- Regulatory: OCR pipeline + VLM validator for cross-check.
  中文翻译：监管场景：OCR 管道 + VLM 验证器交叉检查。

## Use It | 用框架实现

`code/main.py`:

- A toy layout-aware tokenizer: given (text, bbox) pairs, produces the LayoutLMv3-style input.
  中文翻译：玩具布局感知分词器：给定 (text, bbox) 对，生成 LayoutLMv3 风格的输入。
- A Donut-style task schema generator: JSON template for forms.
  中文翻译：Donut 风格的任务 schema 生成器：表单的 JSON 模板。
- A comparison of token budgets per page across OCR-pipeline, Donut, Nougat, and VLM-native.
  中文翻译：OCR 管道、Donut、Nougat 和 VLM 原生之间每页 token 预算的比较。

## Ship It | 产出物

This lesson produces `outputs/skill-document-ai-stack-picker.md`. Given a document-AI project (domain, scale, quality, regulatory), picks between OCR pipeline, OCR-free specialist, and VLM-native.

> 本课产出 `outputs/skill-document-ai-stack-picker.md`。给定文档 AI 项目（领域、规模、质量、监管），在 OCR 管道、无 OCR 专家和 VLM 原生之间选择。

## Exercises | 练习题

1. Your project is 10M invoices per day. Which stack minimizes cost-per-page without losing accuracy? 你的项目每天处理 1000 万张发票。哪种方案能在不损失准确率的情况下最小化每页成本？

2. Why does LayoutLMv3 outperform pure-CLIP-VLMs on form QA but underperform at scene-text? What does the bbox stream give up? 为什么 LayoutLMv3 在表单 QA 上优于纯 CLIP VLM，但在场景文本上表现不佳？bbox 流放弃了什么？

3. Nougat generates LaTeX. Propose a test case where VLM-native output beats Nougat on LaTeX fidelity, and a case where Nougat wins. Nougat 生成 LaTeX。设计一个 VLM 原生输出在 LaTeX 保真度上胜过 Nougat 的测试用例，以及一个 Nougat 胜出的用例。

4. Read PaliGemma 2 paper (Google, 2024). What was the key training-data addition that lifted document accuracy vs PaliGemma 1? 阅读 PaliGemma 2 论文。相比 PaliGemma 1，什么关键训练数据提升了文档准确率？

5. Design a regulatory-safe hybrid: OCR pipeline as primary, VLM as secondary cross-check. How do you resolve disagreement? 设计一个监管安全的混合方案：OCR 管道为主，VLM 为辅交叉检查。如何处理不一致？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Further Reading | 延伸阅读

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
