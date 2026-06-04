# 模型、系统和数据集卡片

> Three documentation formats structure AI transparency. Model Cards (Mitchell et al. 2019) — nutrition labels for models: training data, quantitative disaggregated analyses, ethical considerations, caveats; only 0.3% of Hugging Face model cards document ethical considerations (Oreamuno et al. 2023). Datasheets for Datasets (Gebru et al. 2018, CACM) — motivation, composition, collection process, labeling, distribution, maintenance; electronics-datasheet analogy. Data Cards (Pushkarna et al., Google 2022) — modular layered detail (telescopic, periscopic, microscopic) as boundary objects for diverse readers. 2024-2025 developments: automated generation via LLMs (CardGen, Liu et al. 2024); model-card detail correlates with up to 29% download increase on HF (Liang et al. 2024); verifiable attestations (Laminator, Duddu et al. 2024); sustainability reporting additions for carbon/water (Jouneaux et al. July 2025); EU/ISO regulatory cards emerging. System Cards (Sidhpurwala 2024; Meta system-level transparency; "Blueprints of Trust" arXiv:2509.20394) — end-to-end AI system documentation covering security capabilities, prompt-injection protection, data-exfiltration detection, alignment with human values.

> **【中文解读】** 本节介绍了模型/系统/数据集卡片——AI 系统透明度的标准化文档。三种文档格式各有不同透明度范围：Model Cards（Mitchell 等人 2019）——模型的营养标签；Datasheets for Datasets（Gebru 等人 2018）——数据集的电子规格书；System Cards——端到端 AI 系统文档。

> **【拓展：采用率 → 0.3% 问题】** Oreamuno 等人 2023 审计 Hugging Face 模型卡发现只有 0.3% 记录了伦理考量。Liang 等人 2024 发现详细模型卡与高达 29% 的下载增加相关——采用压力现在是市场驱动的，不仅是合规驱动的。自动化生成（CardGen, Liu 等人 2024）和可验证证明（Laminator, Duddu 等人 2024）正在解决长期采用问题。

**类型：** 构建
**语言：** Python (标准库， model-card + datasheet + system-card generator)
**前置条件：** Phase 18 · 18 (safety frameworks), Phase 18 · 24 (regulatory)
**时间：** 约 60 分钟

## 学习目标

- Describe the original Mitchell et al. 2019 model card and the Gebru et al. 2018 datasheet.
- Describe Data Cards' telescopic/periscopic/microscopic layering.
- Describe System Cards and their end-to-end coverage.
- State three 2024-2025 developments (automated generation, verifiable attestations, sustainability reporting).

## 问题引入

Regulatory frameworks (Lesson 24) and lab safety policies (Lesson 18) both require documentation. Documentation formats evolved from model-specific (model cards) to dataset-specific (datasheets) to system-specific (system cards). Each addresses a different scope of transparency. The 2024-2025 automation and verifiable-attestation work addresses the long-standing adoption problem.

## 核心概念

> **【中文解读】** Model Cards 九大板块：模型详情、预期用途、因素（相关人口或环境因素）、指标、评估数据、训练数据、定量分析（按因素分解）、伦理考量、注意事项和建议。Data Cards（Google 2022）的三层缩放：望远镜级（非专家高层摘要）、潜望镜级（ML 从业者中层概览）、显微镜级（审计员详细特征级文档）。

### Model Cards (Mitchell et al. 2019)

Sections:
- Model details.
- Intended use.
- Factors (relevant demographic or environmental factors for evaluation).
- Metrics.
- Evaluation data.
- Training data.
- Quantitative analyses (disaggregated by factors).
- Ethical considerations.
- Caveats and recommendations.

Adoption problem: Oreamuno et al. 2023 audit of Hugging Face model cards found only 0.3% document ethical considerations.

### Datasheets for Datasets (Gebru et al. 2018)

Electronics-datasheet analogy. Sections:
- Motivation (why was the dataset created).
- Composition (what is in it).
- Collection process (how was it assembled).
- Labeling (if applicable).
- Uses (intended, prohibited, risks).
- Distribution.
- Maintenance.

Published in CACM 2021. The datasheet is the upstream documentation; the model card depends on the datasheet being accurate.

### Data Cards (Pushkarna et al., Google 2022)

Modular layered detail. Three zoom levels:
- **Telescopic.** High-level summary for non-experts.
- **Periscopic.** Middle-level overview for ML practitioners.
- **Microscopic.** Detailed feature-level documentation for auditors.

Boundary-object framing: different readers extract different information from the same document.

> **【拓展：System Cards → 部署层透明度】** System Cards 的范围覆盖端到端 AI 系统——包括模型+安全栈+部署上下文。典型板块：安全能力、提示注入保护、数据外泄检测、与声明的人类价值观的对齐、事件响应。"Blueprints of Trust"（arXiv:2509.20394）将 System Card 形式化为 Model Card 的部署层补充。EU AI Act GPAI 代码实践透明度章节要求模型卡作为合规工件。

### System Cards

Scope: end-to-end AI system including model + safety stack + deployment context. Sections typically include:
- Security capabilities.
- Prompt-injection protection.
- Data-exfiltration detection.
- Alignment with stated human values.
- Incident response.

Sidhpurwala 2024 and Meta system-level transparency work. "Blueprints of Trust" (arXiv:2509.20394) formalizes the System Card as the deployment-layer complement to Model Cards.

> **【中文解读】** 2024-2025 年发展：CardGen（Liu 等人 2024）通过 LLM 自动生成模型卡，报告比许多人工卡片更高的客观性；Laminator（Duddu 等人 2024）通过硬件 TEE/加密签名实现可验证证明——允许模型卡携带声明证明而非仅仅是声明；可持续性字段（Jouneaux 等人 2025 年 7 月）新增碳、水和计算能足迹，对应新兴 ISO 标准。

### 2024-2025 developments

- **CardGen (Liu et al. 2024).** Automated model-card generation via LLMs; reports higher objectivity than many human-authored cards on the standardized Mitchell 2019 fields.
- **Download correlation (Liang et al. 2024).** Detailed model cards correlate with up to 29% higher download rates on HF — adoption pressure is now market-driven, not only compliance-driven.
- **Laminator (Duddu et al. 2024).** Verifiable attestations via hardware TEE / cryptographic signatures — allows the model card to carry a proof-of-claim, not just a claim.
- **Sustainability (Jouneaux et al. July 2025).** Additions for carbon, water, and compute-energy footprint; emerging ISO standards.
- **Regulatory cards.** EU AI Act (Lesson 24) GPAI Code of Practice Transparency chapter requires model cards as a compliance artifact.

### 在 Phase 18 中的位置 in Phase 18

Lessons 24-25 are regulatory and CVE layers. Lesson 26 is the documentation layer. Lesson 27 is training-data governance, which is the datasheet's upstream. Lesson 28 is the research ecosystem that produces evaluations referenced in cards.

> **【拓展：可验证证明 → Laminator】** Laminator（Duddu 等人 2024）使用硬件 TEE / 加密签名实现可验证证明——允许模型卡携带声明证明而非仅仅是声明。例如，一个模型卡字段可以携带"在数据集 X 上的准确率为 Y%"的加密证明，验证者可以检查证明而不需要重新运行评估。这对于监管合规（EU AI Act, Lesson 24）特别重要。

## 用框架实现

`code/main.py` generates a minimal model card, datasheet, and system card for a toy deployment. Each follows the canonical section structure. You can inspect the format and compare the three scopes.

## 产出物

This lesson produces `outputs/skill-card-audit.md`. Given a model card, datasheet, or system card, it audits section coverage, numerical disaggregation, and whether verifiable attestations are present.

## 练习题

1. 运行 `code/main.py`. Inspect the generated cards. Identify sections that are weak (placeholder-only) and specify what evidence would strengthen them.

2. 扩展the model card with a quantitative disaggregated analysis across two demographic groups (Lesson 20).

3. 阅读 Oreamuno et al. 2023 on the 0.3% adoption rate. Propose one structural change to the model card specification that would increase ethical-considerations adoption.

4. Laminator (Duddu et al. 2024) uses TEEs for verifiable attestations. Design a model-card field that carries a cryptographic attestation of an evaluation result and describe the verifier's role.

5. 编写a System Card (System Card, not Model Card) for one of your past projects or a hypothetical deployment. Identify the highest-value section for third-party auditors.

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Model Card | "the Mitchell card" | Mitchell et al. 2019 standard documentation for ML models |
| Datasheet | "the Gebru datasheet" | Gebru et al. 2018 standard documentation for datasets |
| Data Card | "the Pushkarna card" | Google 2022 modular layered data documentation |
| System Card | "the deployment card" | End-to-end AI system documentation including safety stack |
| Boundary object | "different readers, one doc" | Data Cards framing: same document serves diverse audiences |
| Verifiable attestation | "the Laminator attestation" | Cryptographic or TEE proof attached to a documentation claim |
| Sustainability field | "carbon / water footprint" | Emerging 2025 addition for environmental accounting |

## 延伸阅读

- [Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993, FAT* 2019)](https://arxiv.org/abs/1810.03993) — the canonical model card
- [Gebru et al. — Datasheets for Datasets (CACM 2021, arXiv:1803.09010)](https://arxiv.org/abs/1803.09010) — datasheet paper
- [Pushkarna et al. — Data Cards (Google 2022)](https://arxiv.org/abs/2204.01075) — layered data documentation
- [Sidhpurwala et al. — Blueprints of Trust (arXiv:2509.20394)](https://arxiv.org/abs/2509.20394) — System Card formalization
