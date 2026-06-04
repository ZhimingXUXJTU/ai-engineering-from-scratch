# Frontier Safety Frameworks — RSP, PF, FSF | 框架 前沿 安全 RSP

> Three major-lab frameworks define the 2026 industry governance of frontier capability. Anthropic Responsible Scaling Policy v3.0 (February 2026) introduces tiered AI Safety Levels (ASL-1 through ASL-5+), modeled on biosafety levels, with ASL-3 activated May 2025 for CBRN-relevant models. OpenAI Preparedness Framework v2 (April 2025) defines five criteria for tracked capabilities and separates Capabilities Reports from Safeguards Reports. DeepMind Frontier Safety Framework v3.0 (September 2025) introduces Critical Capability Levels including a new Harmful Manipulation CCL. All three now include competitor-adjustment clauses allowing deferral if peer labs ship without comparable safeguards. Cross-lab alignment remains structural, not terminological: "Capability Thresholds," "High Capability thresholds," and "Critical Capability Levels" denote analogous constructs.

> **【中文解读】** 本节介绍了前沿安全框架——Anthropic RSP、OpenAI Preparedness、DeepMind FSF 等安全框架对比。三个实验室框架定义了 2026 年前沿能力行业治理。ASL-3 于 2025 年 5 月激活用于 CBRN 相关模型。安全案例是书面论证，在测试部署在最坏情况假设下是否可接受安全。

> **【拓展：竞争调整条款 → 竞赛动态】** 所有三个框架都包含竞争调整条款——允许在竞争对手在没有可比保障措施的情况下发货时推迟。批评者认为这创造了竞底：如果三个实验室都在竞争对手违约时减少要求，均衡向违约偏移。维护者认为替代方案（单边保障措施）在违约实验室安全意识较低时产生更差结果。

**Type:** Learn
**Languages:** none
**Prerequisites:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (deception failures)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Describe Anthropic's ASL tier structure and what activated ASL-3.
- Name the five OpenAI Preparedness Framework v2 criteria for tracked capabilities.
- Describe DeepMind's Critical Capability Level structure and the Harmful Manipulation CCL.
- Explain the competitor-adjustment clauses and why they matter for race dynamics.
- Define a safety case and describe the three-pillar structure (monitoring, illegibility, incapability).

## The Problem | 问题

Lessons 7-17 establish that deception is possible, dual-use capability exists, and evaluation has limits. A lab with a frontier-capable model needs an internal governance structure that:
- Defines thresholds for when new safeguards are required.
- Defines required evaluations before scaling.
- Describes what a safety case looks like.
- Handles the race-dynamic problem (if competitors ship without safeguards, what do you do?).

The three 2025-2026 frameworks are the state of the art — imperfect, evolving, and aligned enough across labs that the governance question is now whether the frameworks are adequate, not whether they exist.

## The Concept | 概念

> **【中文解读】** Anthropic RSP v3.0 的 ASL 结构：ASL-1 非前沿模型；ASL-2 当前前沿基线；ASL-3 大幅更高的灾难性滥用风险（CBRN），2025 年 5 月激活；ASL-4 AI R&D-2 跨越阈值（可自动化入门级 AI 研究）；ASL-5+ 高级 AI R&D（大幅加速有效扩展）。v3.0 新增前沿安全路线图（公开修订版）、季度风险报告（部分外部审查）、AI R&D 拆分为 R&D-2 和 R&D-4。

### Anthropic Responsible Scaling Policy v3.0 (February 2026)

ASL structure:
- ASL-1: not a frontier model (subsumed by weaker-than-frontier baseline).
- ASL-2: current frontier baseline; deployed with usual safeguards.
- ASL-3: substantially higher risk of catastrophic misuse; CBRN-relevant capabilities. Activated May 2025.
- ASL-4: AI R&D-2 crossing threshold; models that can automate entry-level AI research.
- ASL-5+: advanced AI R&D; models that dramatically accelerate effective scaling.

New in v3.0:
- Frontier Safety Roadmaps (public in redacted form).
- Risk Reports (quarterly, some externally reviewed).
- AI R&D is disaggregated into AI R&D-2 and AI R&D-4.
- Once AI R&D-4 is crossed, an affirmative safety case is required, identifying misalignment risks from models pursuing misaligned goals.

> **【拓展：OpenAI PF v2 → 五项追踪标准】** OpenAI 的五项追踪能力标准：（1）合理的——存在合理威胁模型；（2）可测量的——经验评估可能；（3）严重的——伤害大；（4）净新的——不是已有风险放大；（5）即时或不可补救的——伤害快速发生或无法撤销。满足所有五项的能力被追踪，其他不追踪。

### OpenAI Preparedness Framework v2 (April 15, 2025)

Five criteria for tracked capabilities:
- **Plausible.** Reasonable threat model exists.
- **Measurable.** Empirical evaluation possible.
- **Severe.** Harm is large.
- **Net-new.** Not a pre-existing risk scaled up.
- **Instantaneous-or-irremediable.** Harm occurs fast or cannot be undone.

Capabilities that meet all five are tracked. Others are not.

Other PF v2 structure:
- Separate Capabilities Reports (what the model can do) from Safeguards Reports (what controls exist).
- Safety Advisory Group reviews.
- Leadership approves; Board's Safety & Security Committee oversees.
- "Adjustment clause": OpenAI may reduce requirements if another lab ships without comparable safeguards.

### DeepMind Frontier Safety Framework v3.0 (September 2025)

Critical Capability Levels (CCLs) by domain:
- Bioweapon Uplift
- Cyber Uplift
- ML R&D Acceleration
- Harmful Manipulation (new in v3.0): models that could substantially change beliefs/behavior in high-stakes contexts.

v2.0 (February 2025) added a Deceptive Alignment section and higher security levels for ML R&D CCLs.

### Cross-lab alignment

- Anthropic "Capability Thresholds."
- DeepMind "Critical Capability Levels."
- OpenAI "High Capability thresholds."

No industry-standard terminology. Structurally aligned: three tiers of frontier capability with published evaluation criteria. All three include competitor-adjustment clauses (2025 onward).

> **【中文解读】** 安全案例三支柱结构：（1）监控——如果发生坏行为，我们能检测到吗？（2）不可读性——模型是否缺乏执行连贯伤害计划的能力？（3）无能——模型是否缺乏造成相关伤害的能力？不同安全案例针对不同支柱：ASL-3 CBRN 案例主要针对无能（通过遗忘），欺骗性对齐针对监控和不可读性，网络提升则三个都相关。

### Safety cases

A safety case is a written argument that a deployment is acceptably safe under worst-case assumptions. The standard structure targets three pillars:

- **Monitoring.** Can we detect bad behaviour if it occurs?
- **Illegibility.** Does the model lack the ability to execute a coherent plan to cause harm?
- **Incapability.** Does the model lack the capability to cause the harm in question?

Different safety cases target different pillars. For a ASL-3 CBRN case, incapability (via unlearning) is the primary target. For deceptive alignment, monitoring and illegibility are targets. For cyber uplift, all three are relevant.

### The race-dynamic problem

Competitor-adjustment clauses are controversial. Critics argue they create a race to the bottom: if all three labs will reduce requirements when a competitor defects, the equilibrium shifts toward defection. Defenders argue the alternative (unilateral safeguards) produces worse outcomes if the defecting lab is less safety-conscious.

UK AISI, US CAISI, and EU AI Office (Lesson 24) are the external governance counterparts. The lab frameworks are voluntary; the regulatory frameworks are emerging.

### Where this fits in Phase 18

Lessons 17-18 are the measurement-and-governance layer on top of the deception and red-team analyses. Lessons 19-24 cover welfare, bias, privacy, watermarking, and regulatory structure. Lesson 28 maps the research ecosystem (MATS, Redwood, Apollo, METR) that operationalizes the evaluations.

> **【拓展：跨实验室对齐 → 结构性而非术语性】** 三个框架在术语上不一致但结构上对齐：Anthropic "Capability Thresholds" = DeepMind "Critical Capability Levels" = OpenAI "High Capability thresholds"。三层前沿能力、发布评估标准、竞争调整条款——结构趋同。UK AISI, US CAISI 和 EU AI Office（Lesson 24）是外部治理对应方。实验室框架是自愿的；监管框架正在出现。

## Use It | 使用方法

No code for this lesson. Read the three primary sources: RSP v3.0, PF v2, FSF v3.0. Map each lab's tier structure to the others and identify one threshold each lab defines that the others do not.

## Ship It | 部署上线

This lesson produces `outputs/skill-framework-diff.md`. Given a safety framework or release note, it compares the framework's threshold definitions, evaluations required, and safety-case structure against RSP v3.0, PF v2, FSF v3.0 and flags cross-lab gaps.

## Exercises | 练习题

1. Read RSP v3.0, PF v2, and FSF v3.0. Compile a table of each lab's CBRN threshold, each's AI R&D threshold, and each's required pre-deployment evaluation.

2. The competitor-adjustment clause is in all three frameworks (2025+). Write one paragraph arguing for it; write one paragraph arguing against. Identify the assumption each position depends on.

3. Design a safety case for a model crossing Anthropic's AI R&D-4 threshold. Name the evidence each of the three pillars (monitoring, illegibility, incapability) requires.

4. DeepMind's FSF v3.0 introduces a Harmful Manipulation CCL. Propose three empirical measurements that would indicate a model has crossed this threshold.

5. Read METR's "Common Elements of Frontier AI Safety Policies" (2025). Name the three strongest cross-lab convergences and the two largest divergences.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| RSP | "Anthropic's framework" | Responsible Scaling Policy; ASL tiers; v3.0 February 2026 |
| PF | "OpenAI's framework" | Preparedness Framework; five criteria; v2 April 2025 |
| FSF | "DeepMind's framework" | Frontier Safety Framework; CCLs; v3.0 September 2025 |
| ASL-3 | "biosafety level 3-analog" | Anthropic tier for CBRN-relevant capabilities; activated May 2025 |
| CCL | "critical capability level" | DeepMind's threshold construct; per-domain |
| Safety case | "the formal argument" | Written argument that deployment is acceptably safe under worst-case U |
| Adjustment clause | "competitor defection allowance" | Framework provision for reducing requirements if competitors ship without comparable safeguards |

## Further Reading | 延伸阅读

- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) — ASL tiers, roadmaps, AI R&D disaggregation
- [OpenAI — Updating the Preparedness Framework (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) — five criteria, adjustment clause
- [DeepMind — Strengthening our Frontier Safety Framework (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — CCL v3.0, Harmful Manipulation
- [METR — Common Elements of Frontier AI Safety Policies (2025)](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) — cross-lab comparison
