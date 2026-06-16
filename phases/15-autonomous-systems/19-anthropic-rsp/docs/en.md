# Anthropic Responsible Scaling Policy v3.0 | Anthropic 负责任扩展政策 v3.0

> RSP v3.0 went into effect February 24, 2026, replacing the 2023 policy. Two-tier mitigation: what Anthropic will do unilaterally vs what is framed as an industry-wide recommendation (including RAND SL-4 security standards). Adds Frontier Safety Roadmaps and Risk Reports as standing documents rather than one-off deliverables. Drops the 2023 pause commitment. Introduces the AI R&D-4 threshold: once crossed, Anthropic must publish an affirmative case identifying misalignment risks and mitigations. Claude Opus 4.6 does not cross it. Anthropic states in the v3.0 announcement that "confidently ruling this out is becoming difficult." SaferAI rated the 2023 RSP at 2.2; they downgraded v3.0 to 1.9, putting Anthropic in the "weak" RSP category alongside OpenAI and DeepMind. Qualitative thresholds replaced the 2023 quantitative commitments; removing the pause clause is the sharpest regression.

> **【中文解读】** RSP v3.0 于 2026 年 2 月 24 日生效，替代 2023 政策。两层缓解：Anthropic 单边做什么 vs 行业范围建议（包括 RAND SL-4 安全标准）。添加 Frontier Safety Roadmaps 和 Risk Reports 作为常设文档而非一次性交付物。删除 2023 暂停承诺。引入 AI R&D-4 阈值：一旦跨越，Anthropic 必须发布识别不对齐风险和缓解的肯定案例。Claude Opus 4.6 未跨越它。Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"。SaferAI 评 2023 RSP 为 2.2；他们降级 v3.0 至 1.9，将 Anthropic 与 OpenAI 和 DeepMind 一起放入"弱"RSP 类别。定性阈值替代 2023 定量承诺；删除暂停条款是最尖锐的回归。

> **【拓展：v3.0 的核心改动】** 三个关键变化：(1) 添加——前沿安全路线图、风险报告、AI R&D-4 阈值；(2) 删除——2023 暂停承诺；(3) 重构——两层缓解时间表（Anthropic 单边 vs 行业建议）。SaferAI 的降级因素：定性阈值替代定量、暂停承诺删除、AI R&D-4 缓解描述为"肯定案例"而非具体措施、审查机制依赖 Anthropic 的安全咨询组缺乏独立监督。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·06（AAR）、Phase 15·07（RSI）、Phase 15·08（Bounded RSI）。RSP = 前沿实验室的"安全扩展承诺"——既是技术文档也是治理信号。
> 💡 **【类比】** RSP = "AI 公司的安全宪法"。2023 版 = 严格（定量阈值+暂停承诺）；v3.0 = 灵活（定性阈值+删除暂停）。SaferAI 评分从 2.2 降到 1.9（"弱"类别）。新增 AI R&D-4 阈值 = 一旦 AI 能自动化 AI 研发达到某水平，必须强制披露——这是 RSI 的刹车。
> 🤔 **【困惑】** Q: 为什么删除暂停承诺？— 商业压力。暂停 = 竞争对手超越你。OpenAI、Google 都没暂停，Anthropic 单方面暂停=自杀。修复：行业协调（RAND SL-4 标准）+ 监管介入（EU AI Act）才能避免囚徒困境。

## The Problem | 问题引入

Frontier labs publish scaling policies that are partly technical documents, partly governance documents, and partly signals to regulators.

> 前沿实验室发布的扩展政策部分是技术文档、部分是治理文档、部分是向监管者的信号。

RSP v3.0 is the current Anthropic document. Reading it closely matters not because compliance with it is binding (it is not), but because the framing shapes how a lab conceives of catastrophic risk and how they communicate trade-offs to the public.

> RSP v3.0 是当前 Anthropic 文档。仔细阅读重要不是因为合规具有约束力（不具），而是因为框架塑造实验室如何构想灾难性风险以及如何向公众传达权衡。

The v3.0 vs v2.0 diff is the useful unit. What got added: Frontier Safety Roadmaps, Risk Reports, the AI R&D-4 threshold. What got removed: the 2023 pause commitment.

> v3.0 与 v2.0 的差异是有用单位。新增：前沿安全路线图、风险报告、AI R&D-4 阈值。删除：2023 暂停承诺。

What got reframed: a two-tier mitigation schedule split between Anthropic-unilateral and industry-recommendation. External review — SaferAI — downgraded the score from 2.2 (v2) to 1.9 (v3.0). This is how a scaling policy can get less rigorous while looking more polished.

> 重构：分为 Anthropic 单边和行业建议的两层缓解时间表。外部审查——SaferAI——将分数从 2.2（v2）降级到 1.9（v3.0）。这就是扩展政策如何能在看起来更精炼的同时变得更不严谨。

> **【中文解读】** Anthropic 的负责任扩展政策（RSP, Responsible Scaling Policy）定义了在 AI 能力增长时保持安全的框架。核心承诺：(1) 评估前沿——定期评估模型是否达到新的危险能力阈值；(2) 安全等级——定义与能力匹配的安全措施；(3) 暂停承诺——如果评估失败则暂停扩展。

## The Concept | 核心概念

### The two-tier mitigation schedule | 两层缓解时间表

- **Anthropic unilateral actions**: what Anthropic will do regardless of what other labs do. Training stops above a threshold, specific security measures, specific deployment gates.
  中文翻译：**Anthropic 单边动作**：不论其他实验室做什么 Anthropic 会做的。阈值以上训练停止、特定安全措施、特定部署门。
- **Industry-wide recommendations**: what Anthropic thinks the industry should do collectively. Includes RAND SL-4 security standards. These are not commitments on Anthropic's side; they are policy advocacy.
  中文翻译：**行业范围建议**：Anthropic 认为行业应集体做的。包括 RAND SL-4 安全标准。这些不是 Anthropic 侧的承诺；是政策倡导。

The two-tier structure was not in v2. It means that a reader needs to look at which column each commitment lives in. A security measure in the "industry-wide recommendation" column is not Anthropic's promise; it is Anthropic's hope.

> 两层结构在 v2 中没有。这意味着读者需看每个承诺在哪一列。"行业范围建议"列中的安全措施不是 Anthropic 的承诺；是 Anthropic 的希望。

### The AI R&D-4 threshold | AI R&D-4 阈值

This is the capability level RSP v3.0 names as the important next threshold. Specifically: a model that could automate a substantial fraction of AI research at competitive cost. Once Anthropic believes a model crosses it, they must publish an affirmative case identifying misalignment risks and mitigations before continued scaling.

> 这是 RSP v3.0 命名为重要下一阈值的能力级别。具体：能以竞争成本自动化相当部分 AI 研究的模型。Anthropic 一旦相信模型跨越它，必须在继续扩展前发布识别不对齐风险和缓解的肯定案例。

Claude Opus 4.6 does not cross it per the v3.0 announcement. The document adds: "confidently ruling this out is becoming difficult." That phrasing matters; it concedes that the threshold is close enough to be a live concern, not a speculative limit.

> Claude Opus 4.6 据 v3.0 公告未跨越它。文档添加："自信地排除这变得困难。"该措辞重要；它承认阈值足够接近以致是现实关切，不是推测性限制。

Lesson 6 (Automated Alignment Research) and Lesson 7 (Recursive Self-Improvement) feed directly into this threshold. Automated alignment researchers crossing research-quality bars is evidence that the AI R&D-4 threshold is approaching.

> 第 6 课（自动化对齐研究）和第 7 课（递归自我改进）直接喂入此阈值。自动化对齐研究器跨越研究质量栏是 AI R&D-4 阈值正在接近的证据。

### Frontier Safety Roadmaps and Risk Reports | 前沿安全路线图和风险报告

v3.0 elevates two artifact types to standing documents:

> v3.0 将两类制品提升为常设文档：

- **Frontier Safety Roadmap**: forward-looking document describing planned safety work, capability expectations, and mitigation research.
  中文翻译：**前沿安全路线图**：描述计划安全工作、能力预期和缓解研究的前瞻文档。
- **Risk Report**: retrospective document on specific models after release, describing observed capability and residual risk.
  中文翻译：**风险报告**：发布后特定模型的事后文档，描述观察能力和剩余风险。

Both are public. Both are updated on a declared cadence. The utility is: reader can track how what Anthropic said they would do in a Roadmap compares to what they report in a Risk Report.

> 两者公开。两者按声明节奏更新。效用：读者可追踪 Anthropic 在路线图中说会做的与在风险报告中报告的如何对比。

### Removing the pause clause | 删除暂停条款

The 2023 RSP included an explicit pause commitment: if a model crossed specific capability thresholds, training would pause until mitigations were in place. v3.0 replaces the explicit pause with a softer formulation (publish an affirmative case, proceed if mitigations are adequate). SaferAI and other analysts called this out directly as the strongest regression in the new document.

> 2023 RSP 包含显式暂停承诺：如果模型跨越特定能力阈值，训练将暂停直到缓解就位。v3.0 用更软表述（发布肯定案例，如缓解充分则继续）替代显式暂停。SaferAI 和其他分析师直接指出这是新文档中最强回归。

The policy argument for the change: quantitative thresholds in 2023 turned out to be unreachable by 2026-era capability benchmarks because the benchmarks themselves were re-scaled. The counter-argument: a pause clause in a scaling policy is a commitment device; removing it removes the credibility of the policy.

> 变更的政策论据：2023 的定量阈值被 2026 时代能力基准证明不可达，因为基准本身被重缩放。反论：扩展政策中的暂停条款是承诺装置；移除它移除政策可信度。

### SaferAI's downgrade | SaferAI 的降级

SaferAI is an independent organization that rates RSP-style documents. Their public rating: 2023 Anthropic RSP scored 2.2 (out of a scale where 4.0 is the best current RSP and 1.0 is nominal). v3.0 scored 1.9. This moved Anthropic from "moderate" to "weak," joining OpenAI and DeepMind in the weak category.

> SaferAI 是评 RSP 式文档的独立组织。其公开评分：2023 Anthropic RSP 得 2.2（4.0 是当前最佳 RSP，1.0 是名义的量表上）。v3.0 得 1.9。这把 Anthropic 从"中等"移到"弱"，与 OpenAI 和 DeepMind 一起进入弱类别。

The downgrade factors per SaferAI:

> SaferAI 列出的降级因素：

- Qualitative thresholds replaced quantitative ones.
  中文翻译：定性阈值替代定量。
- Pause commitment removed.
  中文翻译：暂停承诺移除。
- AI R&D-4 threshold mitigations are described as "affirmative case" rather than specific measures.
  中文翻译：AI R&D-4 阈值缓解描述为"肯定案例"而非具体措施。
- Review mechanisms depend on Anthropic's Safety Advisory Group, with limited independent oversight.
  中文翻译：审查机制依赖 Anthropic 的安全咨询组，独立监督有限。

### What this lesson is not | 这课不是什么

This is not a lesson in compliance. RSP v3.0 is not a regulation; nothing forces Anthropic to follow it.

> 这不是合规课程。RSP v3.0 不是法规；无东西强制 Anthropic 遵循。

The lesson is in reading the document with the specificity and skepticism it deserves. Scaling policies are the primary public signal frontier labs emit about catastrophic-risk posture. Reading them well is a practical skill for anyone whose work depends on frontier capabilities.

> 课程是用它应得的特异性和怀疑论阅读文档。扩展政策是前沿实验室发出关于灾难性风险姿态的主要公开信号。读好它们对任何工作依赖前沿能力的人是实用技能。

## Use It | 用框架实现

`code/main.py` implements a small decision engine that mirrors the RSP threshold-evaluation shape: given a candidate model and a set of capability measurements, return whether the AI R&D-4 threshold is crossed, the required affirmative-case sections, and whether deployment can proceed. It's intentionally simple; the point is to make the document's logic explicit.

> `code/main.py` 实现镜像 RSP 阈值评估形状的小决策引擎：给定候选模型和一组能力测量，返回 AI R&D-4 阈值是否跨越、所需肯定案例节、部署是否可继续。它故意简单；点是让文档逻辑显式。

## Ship It | 产出物

`outputs/skill-scaling-policy-review.md` reviews a scaling policy (Anthropic, OpenAI, DeepMind, or internal) against the v3.0 reference: two-tier structure, thresholds, pause commitments, independent review.

> `outputs/skill-scaling-policy-review.md` 对照 v3.0 参考审查扩展政策（Anthropic、OpenAI、DeepMind 或内部）：两层结构、阈值、暂停承诺、独立审查。

## Exercises | 练习题

1. Run `code/main.py`. Feed in three synthetic models at different capability levels. Confirm the threshold evaluator behaves as expected and produces the right affirmative-case template.
   中文翻译：运行 `code/main.py`。喂入三个不同能力级别的合成模型。确认阈值评估器按预期行为并产生正确肯定案例模板。

2. Read RSP v3.0 in full (32 pages). Identify every commitment that lives in the "industry-wide recommendation" tier. Which of those commitments would have been "Anthropic unilateral" in v2?
   中文翻译：全文阅读 RSP v3.0（32 页）。识别"行业范围建议"层中的每个承诺。v2 中哪些会是"Anthropic 单边"？

3. Read SaferAI's RSP grading methodology. Reproduce their 1.9 score for v3.0 by applying their rubric to the document. Which rubric row drove the downgrade most?
   中文翻译：阅读 SaferAI 的 RSP 评分方法论。通过将评分量表应用于文档复现 v3.0 的 1.9 分。哪个量表行驱动降级最多？

4. The 2023 pause commitment was removed. Propose a replacement commitment that preserves the credibility of the policy while acknowledging the 2026 benchmark-rescaling problem.
   中文翻译：2023 暂停承诺被移除。提议保留政策可信度同时承认 2026 基准重缩放问题的替代承诺。

5. Compare RSP v3.0 to OpenAI Preparedness Framework v2 (Lesson 20). Pick one area where v3.0 is stronger. Pick one area where the Preparedness Framework is stronger.
   中文翻译：比较 RSP v3.0 与 OpenAI Preparedness Framework v2（第 20 课）。选一个 v3.0 更强的领域。选一个 Preparedness Framework 更强的领域。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Further Reading | 延伸阅读

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — the full 32-page policy.
  中文翻译：完整 32 页政策。
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) — summary of changes from v2.
  中文翻译：v2 变更摘要。
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) — standing document linked from RSP v3.0.
  中文翻译：RSP v3.0 链接的常设文档。
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) — retrospective on the current frontier model.
  中文翻译：当前前沿模型的事后。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — connects AI R&D-4 to measured autonomy.
  中文翻译：将 AI R&D-4 连接到测量的自主性。
