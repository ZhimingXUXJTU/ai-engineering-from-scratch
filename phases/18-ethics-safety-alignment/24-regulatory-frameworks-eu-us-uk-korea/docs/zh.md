# 监管框架——欧盟、美国、英国、韩国

> Four primary regulatory regimes define the 2026 AI governance landscape. EU AI Act (in force 1 August 2024) — prohibited practices and AI literacy from 2 February 2025; GPAI obligations from 2 August 2025; full applicability and Article 50 transparency 2 August 2026; legacy GPAI and embedded high-risk systems 2 August 2027; penalties up to 15M EUR or 3% of global turnover. GPAI Code of Practice (10 July 2025): three chapters — Transparency, Copyright, Safety and Security — 12 commitments; enforcement begins August 2026. UK AISI -> AI Security Institute (February 2025): rename signals narrower scope. US AISI -> CAISI (June 2025): Center for AI Standards and Innovation under NIST; shift toward pro-growth posture. Korean AI Framework Act (passed December 2024, effective January 2026): Article 12 establishes AISI under MSIT; mandates local representatives for foreign AI companies, risk assessment, safety measures for high-impact and generative AI.

> **【中文解读】** 本节介绍了监管框架——欧盟 AI 法案、美国、英国、韩国的 AI 监管政策对比。EU AI Act（2024 年 8 月 1 日生效）建立风险分级结构：禁止实践、高风险系统、通用目的 AI、有限风险系统。GPAI 代码实践（2025 年 7 月 10 日）包含透明度、版权和安全三章 12 项承诺。

> **【拓展：四国监管哲学对比 → 合规挑战】** 四种竞争性监管哲学：EU——严格、风险分级、重罚（最高 1500 万欧元或全球营业额 3%）；US——创新优先、分散化、各州填补联邦空白；UK——窄化安全焦点、强评估基础设施；韩国——MSIT 主导、面向外国提供商。多司法管辖区部署者必须遵守最严格的——2026 年通常是 EU AI Act。

**类型：** 学习
**语言：** none
**前置条件：** Phase 18 · 18 (frontier frameworks), Phase 18 · 27 (data governance)
**时间：** 约 75 分钟

## 学习目标

- Describe the EU AI Act risk tiers (prohibited, high-risk, general-purpose, limited-risk) and the August 2025 / August 2026 / August 2027 timeline.
- Describe the three chapters of the GPAI Code of Practice and which providers each binds.
- Describe the 2025 rebrands: UK AISI -> AI Security Institute; US AISI -> CAISI; what each rebrand implies about policy direction.
- State the core provision of Korea's AI Framework Act.

## 问题引入

Lab frameworks (Lesson 18) are voluntary. Regulatory frameworks are compulsory. The 2024-2026 period saw the first wave of comprehensive AI regulation enter force. Deployers must map technical controls to regulatory obligations; the mapping differs by jurisdiction.

## 核心概念

> **【中文解读】** EU AI Act 时间线：2025 年 2 月 2 日——禁止实践 + AI 素养；2025 年 8 月 2 日——GPAI + 治理；2026 年 8 月 2 日——全面适用 + Article 50 透明度 + 罚款；2027 年 8 月 2 日——遗留 GPAI + 嵌入高风险。系统性风险 GPAI（>1e25 FLOP 训练计算）有额外义务，估计约束 5-15 家公司。

### EU AI Act

**In force 1 August 2024.** Risk-tier structure:

- **Prohibited practices** (Article 5). Social scoring, real-time remote biometric identification in public (with law-enforcement exceptions), exploitative manipulation of vulnerable groups. Applied 2 February 2025.
- **High-risk systems** (Annex III). Employment, education, credit, law enforcement, justice, migration. Require conformity assessment, risk management, logging, transparency.
- **General-Purpose AI (GPAI) models**. Applied 2 August 2025. All GPAI providers have obligations; systemic-risk GPAI (>1e25 FLOP training compute) have additional obligations.
- **Limited-risk systems**. Transparency obligations under Article 50 (AI-generated content labelling). Applied 2 August 2026.

Timeline:
- 2 Feb 2025: prohibited practices + AI literacy.
- 2 Aug 2025: GPAI + governance.
- 2 Aug 2026: full applicability + Article 50 transparency + penalties up to 15M EUR / 3% global turnover.
- 2 Aug 2027: legacy GPAI + embedded high-risk.

Commission proposed adjusting the high-risk timeline to 16 months in late 2025.

### GPAI 代码实践

Published 10 July 2025. Three chapters:

- **Transparency.** All GPAI providers.
- **Copyright.** All GPAI providers.
- **Safety and Security.** Systemic-risk GPAI providers (estimated 5-15 companies).

12 commitments total. A Signatory Taskforce chaired by the AI Office manages implementation. Enforcement begins 2 August 2026; until then, good-faith compliance is accepted.

### Article 50 透明度代码 for Article 50

First draft 17 December 2025. Second draft March 2026. Final version June 2026. Covers AI-generated content labelling including deepfakes — the regulatory layer that requires Lesson 23's watermarking technology.

> **【拓展：UK/US 重新命名 → 政策方向转变】** UK AISI 2025 年 2 月更名为 AI Security Institute——缩小范围：放弃算法偏见和言论自由框架，聚焦前沿能力安全。US CAISI 2025 年 6 月从 NIST 的 AI Safety Institute 转型为 Center for AI Standards and Innovation——转向"促增长 AI 政策"，减少预部署评估强调。这两个更名反映了政策优先级的变化。

### UK AI Security Institute (February 2025)

Renamed from AI Safety Institute. The rebrand narrows scope: drops algorithmic bias and free-speech framings; focuses on frontier capability security. Open-sourced the Inspect evaluation tool (May 2024). Collaborates with Redwood (Lesson 10) on control safety cases.

### US CAISI (June 2025)

Trump administration transforms NIST's AI Safety Institute into the Center for AI Standards and Innovation. Shift toward "pro-growth AI policies" per VP Vance's Paris AI Action Summit remarks. Reduced emphasis on pre-deployment evaluation; emphasis on standards and innovation support. Domestic counterweight to EU AI Act's regulatory posture.

> **【中文解读】** 韩国 AI 框架法（2024 年 12 月通过，2026 年 1 月生效）：合并了 19 项独立的 AI 法案。第 12 条在科技通信部（MSIT）下设立 AISI。要求外国 AI 公司在韩国设立本地代表、对"高影响"AI 系统进行风险评估、对生成式 AI 和高影响 AI 采取安全措施。这是亚洲第一个综合水平 AI 监管。

### 韩国 AI 框架法

Passed December 2024. Enacted January 2025. Effective January 2026. Consolidates 19 separate AI bills.

Article 12 establishes an AISI under the Ministry of Science and ICT (MSIT). Mandates:
- Local representatives for foreign AI companies operating in Korea.
- Risk assessment for "high-impact" AI systems.
- Safety measures for generative AI and high-impact AI.

First Asian jurisdiction with a comprehensive horizontal AI regulation.

### 跨司法管辖区动态

- EU: strict, risk-tiered, heavy penalties. Benchmark for privacy-adjacent regulation.
- US: innovation-favouring, decentralized, states (e.g., California AB 2013 — Lesson 27) fill federal gaps.
- UK: narrow security focus, strong evaluation infrastructure.
- Korea: MSIT-led, foreign-provider-focused.

Competing regulatory philosophies. Deployers in multiple jurisdictions have to comply with the strictest, which in 2026 is typically the EU AI Act.

### 在 Phase 18 中的位置 in Phase 18

Lesson 18 is lab-voluntary governance; Lesson 24 is regulatory; Lesson 25 is an emerging class of CVEs for AI systems; Lessons 26-27 cover documentation (cards) and training-data governance.

> **【拓展：GPAI 代码实践 → 透明度/版权/安全】** 2025 年 7 月 10 日发布的 GPAI 代码实践包含三章：透明度——所有 GPAI 提供商；版权——所有 GPAI 提供商；安全和安全——仅系统性风险 GPAI 提供商（估计 5-15 家公司）。12 项总承诺。签名任务组由 AI 办公室主持管理实施。执法从 2026 年 8 月 2 日开始——在此之前善意合规被接受。

## 用框架实现

No code. Read the EU AI Act primary sources: the regulation text, the GPAI Code of Practice, the UK AISI Inspect framework. Map your deployment to the applicable obligations for each jurisdiction.

## 产出物

This lesson produces `outputs/skill-regulatory-map.md`. Given a deployment description, it maps the applicable jurisdictions, the tier classifications in each, the per-jurisdiction obligations, and the deadline structure.

## 练习题

1. 阅读 the EU AI Act (regulation 2024/1689) and the GPAI Code of Practice (10 July 2025). Identify three obligations that apply to every GPAI provider and three that apply only to systemic-risk GPAI.

2. A deployment is made by a US company, runs on EU infrastructure, and serves Korean users. Which three jurisdictions' rules apply, and which rule binds on each substantive question?

3. The UK AI Security Institute's rename narrows scope. Argue for and against the narrower framing. Identify the policy assumption each position depends on.

4. CAISI's "pro-growth" framing is a departure from the 2022-2024 AI safety institute model. Identify two measurable policy shifts that would follow from this framing.

5. Korea's AI Framework Act requires local representatives for foreign providers. Describe the operational implications for a Bay Area company serving Korean users.

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| EU AI Act | "the regulation" | Risk-tier-based horizontal AI regulation; in force Aug 2024 |
| GPAI | "general-purpose AI" | Large foundation models; systemic-risk subset has additional obligations |
| Article 50 | "transparency obligations" | AI-generated content labelling; applies Aug 2026 |
| UK AISI | "AI Security Institute" | Renamed Feb 2025; narrower frontier-security focus |
| CAISI | "US center for AI standards" | Renamed Jun 2025 from AI Safety Institute; pro-growth posture |
| Korean AI Framework Act | "MSIT horizontal regulation" | First Asian comprehensive AI law; effective Jan 2026 |
| Systemic-risk GPAI | "the 1e25 FLOP threshold" | Additional obligations tier; estimated 5-15 companies bound |

## 延伸阅读

- [EU AI Act text (Regulation 2024/1689)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — the regulation and timeline
- [GPAI Code of Practice (10 July 2025)](https://digital-strategy.ec.europa.eu/en/library/final-version-general-purpose-ai-code-practice) — three-chapter code
- [UK AI Security Institute (renamed Feb 2025)](https://www.gov.uk/government/organisations/ai-security-institute) — official page
- [CSET — South Korea AI Framework Act Analysis (2025)](https://cset.georgetown.edu/publication/south-korea-ai-law-2025/) — Korean framework analysis
