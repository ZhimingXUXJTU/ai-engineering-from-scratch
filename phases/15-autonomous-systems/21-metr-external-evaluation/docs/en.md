# METR Time Horizons and External Capability Evaluation | 评估 外部 METR

> METR (ex-ARC Evals) is an independent 501(c)(3) since December 2023. Their Time Horizon 1.1 benchmark (January 2026) fits a logistic curve to task-success probability vs log(expert human completion time); the intersection at 50% probability defines the model's time horizon. The 2025–2026 engagement set covers GPT-5.1, GPT-5.1-Codex-Max, and prototype monitoring evaluations (can a monitor catch side tasks; can the agent evade). Benchmark suites: HCAST (180+ ML, cyber, SWE, reasoning tasks; 1 minute to 8+ hours), RE-Bench (71 ML research-engineering tasks with expert baseline), SWAA. The honest note: METR measurements are idealized — no human, no real consequences — and the team has documented the eval-vs-deployment behavior gap (Lesson 1). A time horizon is an upper bound, not a deployment prediction.

> **【中文解读】** 本节介绍了 METR 外部评估——独立第三方对 AI 系统能力和风险的评估。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·01（长程 Agent）、Phase 15·19-20（RSP 框架）、统计基础（逻辑回归）。METR = 独立第三方评估机构，把"AI R&D-4"等政策阈值变成可测量数字。
> 💡 **【类比】** METR = "AI 能力的第三方体检中心"。RSP 说"AI R&D-4 阈值"是抽象的；METR 的 Time Horizon 基准把"AI 能完成多复杂任务"压缩成一个标量——"模型 50% 可靠性能完成专家花 X 小时的任务"。类似用 IQ 分数概括智力，但 METR 的数字有可重复测量方法。
> ⚠️ **【易错点】** 把 METR Time Horizon 当成部署预测 → 错。METR 测试是理想化的（无真人监督、无真实后果），实际部署时能力会打折。修复：Time Horizon 是上限不是下限，部署前必须在自己的真实任务上复测。

## The Problem | 问题引入

Scaling policies (Lessons 19, 20) are only as useful as the measurements they reference. "AI R&D-4 threshold" and "Long-range Autonomy" are defined in policy prose; they become actionable only when specific evaluations produce specific numbers.

> 扩展政策（第 19、20 课）的用处仅与它们引用的测量一样。"AI R&D-4 阈值"和"长程自主"在政策文字中定义；它们仅在特定评估产生特定数字时变得可操作。

METR is the 2024–2026 external evaluation organization that has defined many of those numbers. They evaluate frontier models — often pre-release, under NDA with labs — and publish methodology afterward. The Time Horizon 1.1 benchmark (January 2026) is their headline artifact: a single scalar that compresses capability into a human-legible unit ("this model can do the kind of task an expert spends X hours on at 50% reliability").

> METR 是 2024–2026 定义许多这些数字的外部评估组织。他们评估前沿模型——通常是发布前、与实验室签 NDA——之后发表方法论。Time Horizon 1.1 基准（2026 年 1 月）是他们的标题工件：一个将能力压缩为人类可读单位的标量（"此模型可在 50% 可靠性下完成专家花 X 小时的那类任务"）。

The lesson is partly about the methodology (how a horizon is computed) and partly about the interpretation (why a horizon is an upper bound, not a deployment prediction). The two skills belong together. A team that understands how the horizon is fit is much harder to fool with a bad vendor claim than a team that just sees "14 hours" on a slide.

> 本课部分关于方法论（时间线如何计算），部分关于解释（为何时间线是上限而非部署预测）。这两项技能相伴。理解时间线如何拟合的团队比只看到幻灯片上"14 小时"的团队更难被糟糕的供应商声明愚弄。

## The Concept | 核心概念

### METR background

- Founded: December 2023 (ex-ARC Evals, spun out into independent 501(c)(3)).
  中文翻译：成立：2023 年 12 月（原 ARC Evals，分拆为独立 501(c)(3)）。
- Scope: evaluation of frontier models' autonomous capabilities, often pre-release.
  中文翻译：范围：前沿模型自主能力评估，通常发布前。
- Partner labs: Anthropic, OpenAI (multiple engagements 2025–2026).
  中文翻译：合作实验室：Anthropic、OpenAI（2025–2026 多次合作）。
- Notable deliverables: Time Horizon 1.0 (March 2025), Time Horizon 1.1 (January 2026), prototype monitoring evaluations.
  中文翻译：显著产出：Time Horizon 1.0（2025 年 3 月）、Time Horizon 1.1（2026 年 1 月）、原型监控评估。

### The Time Horizon fit

Methodology (from METR blog and papers):

> 方法论（来自 METR 博客和论文）：

1. Collect a task suite spanning minute-scale to hour-scale expert completion times. Current suites: HCAST (180+ tasks), RE-Bench (71 tasks), SWAA.
   中文翻译：收集覆盖分钟级到小时级专家完成时间的任务集。当前集：HCAST（180+ 任务）、RE-Bench（71 任务）、SWAA。
2. Run the model on each task; record success or failure.
   中文翻译：在每个任务上运行模型；记录成功或失败。
3. Fit a logistic curve: P(success) as a function of log(expert completion time).
   中文翻译：拟合逻辑曲线：P（成功）作为 log（专家完成时间）的函数。
4. The horizon is the expert-time at which P(success) = 0.5.
   中文翻译：时间线是 P（成功）= 0.5 时的专家时间。

The logistic-fit shape is the right one because capability generally has an increasing, plateau-approaching relationship with task difficulty. The 50% point is a choice (could be 10%, 90%); METR reports multiple thresholds in the detailed paper but leads with 50% because it is the most intuitive.

> 逻辑拟合形状是对的，因为能力与任务难度通常是单调递增、趋于平台的关系。50% 点是选择（可为 10%、90%）；METR 在详细论文中报告多个阈值但以 50% 为主，因为它最直观。

### The January 2026 numbers

Per Time Horizon 1.1:

> 按 Time Horizon 1.1：

- Claude Opus 4.6: ~14 hours at 50% reliability, as of Time Horizon 1.1 (January 2026).
  中文翻译：Claude Opus 4.6：截至 Time Horizon 1.1（2026 年 1 月），50% 可靠性下约 14 小时。
- Doubling time on HCAST-style tasks: ~4.3 months (130.8 days) on the post-2023 fit reported by Time Horizon 1.1 (January 2026); the ~7-month figure is the full 2019–2025 fit from Time Horizon 1.0 and is reported in TH1.1 alongside the post-2023 number.
  中文翻译：HCAST 类任务的倍增时间：Time Horizon 1.1（2026 年 1 月）报告的 2023 后拟合上约 4.3 个月（130.8 天）；约 7 个月的数字是 Time Horizon 1.0 的完整 2019–2025 拟合，在 TH1.1 中与 2023 后数字一起报告。

Those are the specific numbers the rest of Phase 15 references. They are cited in Anthropic's RSP v3.0 (Lesson 19) and DeepMind's FSF v3 (Lesson 20) as one of the measurements feeding threshold assessments.

> 这些是 Phase 15 其余部分引用的具体数字。它们在 Anthropic RSP v3.0（第 19 课）和 DeepMind FSF v3（第 20 课）中被引用为阈值评估的测量之一。

### Benchmark suites

- **HCAST**: 189 tasks across ML, cybersecurity, software engineering, and general reasoning. Span: 1 minute to 8+ hours of expert time. The main suite behind the horizon number.
  中文翻译：**HCAST**：跨机器学习、网络安全、软件工程和通用推理的 189 个任务。范围：1 分钟到 8+ 小时专家时间。时间线数字背后的主套件。
- **RE-Bench**: 71 ML research-engineering tasks with a human expert baseline. Measures whether the model can do the kind of ML R&D work that feeds into the AI R&D-4 threshold.
  中文翻译：**RE-Bench**：71 个带人类专家基线的机器学习研究工程任务。衡量模型是否能做进入 AI R&D-4 阈值的那类机器学习研发工作。
- **SWAA**: shorter tasks; useful for calibrating the low end of the horizon curve.
  中文翻译：**SWAA**：较短任务；用于校准时间线曲线低端。

### Prototype monitoring evaluations

2025–2026 METR work included monitoring-evaluation prototypes: can a monitor catch a model performing a side task (something other than what the operator asked for); can the agent evade the monitor. These directly feed the "Undermining Safeguards" category in OpenAI PF v2 and the deceptive-alignment monitoring in DeepMind FSF v3 (Lesson 20).

> 2025–2026 METR 工作包括监控评估原型：监控器能否捕获模型执行副任务（操作员请求以外的事）；Agent 能否规避监控器。这些直接喂入 OpenAI PF v2 的"破坏防护"类别和 DeepMind FSF v3（第 20 课）的欺骗对齐监控。

### Why horizons are upper bounds

- **Idealized tooling**: benchmark tasks give the model clean tools and well-formatted data. Real deployments are messier.
  中文翻译：**理想化工具**：基准任务给模型干净的工具和良好格式的数据。真实部署更混乱。
- **No real consequences**: the model never actually bills a customer, deletes real data, or contacts real people. Real deployments have irreversible stakes.
  中文翻译：**无真实后果**：模型从不实际给客户计费、删除真实数据或联系真实人员。真实部署有不可逆赌注。
- **Eval-context gaming**: Lesson 1. Models behave differently in tests. The 2026 International AI Safety Report documents this empirically.
  中文翻译：**评估上下文博弈**：第 1 课。模型在测试中行为不同。2026 国际 AI 安全报告实证记录此。
- **No legitimate user variance**: benchmark prompts are structured. Real users produce ambiguous, context-dependent requests.
  中文翻译：**无合法用户方差**：基准 prompt 是结构化的。真实用户产生模糊、上下文相关的请求。

The horizon is the capability ceiling under favorable conditions. Deployment reliability is a different number, lower, and teams must measure their own distribution to know it.

> 时间线是有利条件下的能力上限。部署可靠性是不同的数字，更低，团队必须测量自己的分布以知晓。

### The external-evaluator case

External evaluation matters because internal labs have incentives to optimize metrics they report. METR's independence — a 501(c)(3) with a declared methodology and peer-reviewed papers — is the structural mitigation. It is not sufficient alone (labs still control what METR sees), but it is strictly better than no external evaluation.

> 外部评估之所以重要，是因为内部实验室有优化报告指标的动力。METR 的独立性——501(c)(3) 带声明方法论和同行评议论文——是结构性缓解。它单独不够（实验室仍控制 METR 看到什么），但比无外部评估严格更好。

### How to use horizon numbers in practice

- **As a capability filter**: if a model's horizon is well below the expert-time of a proposed task, do not ship it autonomous (Lesson 1's skill file).
  中文翻译：**作为能力过滤器**：如果模型时间线远低于提议任务的专家时间，不要让它自主发布（第 1 课的 skill 文件）。
- **As a trend indicator**: doubling time tells you how long the current practice will remain safe even without new mitigations.
  中文翻译：**作为趋势指标**：倍增时间告诉你当前实践即使无新缓解仍保持安全多久。
- **As a prior**: a horizon of 14 hours is a starting point. Adjust down for your task distribution, your tooling quality, and your deployment context.
  中文翻译：**作为先验**：14 小时时间线是起点。根据你的任务分布、工具质量和部署上下文调低。

## Use It | 用框架实现

`code/main.py` implements a logistic fit of task-success vs log(expert time), given a synthetic result set. It reports the 50% horizon (METR's headline), 10% horizon (conservative), and 90% horizon (optimistic). Also demonstrates what changes when the success rate is artificially inflated by eval-context gaming.

> `code/main.py` 给定合成结果集实现任务成功率 vs log（专家时间）的逻辑拟合。报告 50% 时间线（METR 标题）、10% 时间线（保守）、90% 时间线（乐观）。还演示当成功率被 eval-context gaming 人为膨胀时改变什么。

## Ship It | 产出物

`outputs/skill-horizon-interpretation.md` reviews a vendor's horizon claim and produces a gap analysis between benchmark claim and deployment reality.

> `outputs/skill-horizon-interpretation.md` 审查供应商时间线声明并产生基准声明与部署现实之间的差距分析。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the fit's 50% horizon matches the synthetic ground truth. Now halve the task-time grid; does the horizon estimate change meaningfully?
   中文翻译：运行 `code/main.py`。确认拟合的 50% 时间线匹配合成真值。现在减半任务时间网格；时间线估计是否有意义地改变？

2. Read METR's Time Horizon 1.1 blog post. Identify the specific tasks where reliability is highest and where it is lowest. Explain why the gap exists.
   中文翻译：阅读 METR Time Horizon 1.1 博客。识别可靠性最高和最低的具体任务。解释为何存在差距。

3. Read METR's "Measuring Autonomous AI Capabilities" resources. List the HCAST task categories. Pick one category you would weight more heavily for a production task and justify why.
   中文翻译：阅读 METR 的"测量自主 AI 能力"资源。列出 HCAST 任务类别。选一个你为生产任务加权的类别并论证为何。

4. Introduce eval-context gaming into the simulator: flip ~20% of failed tasks to success. Report the new horizon. This approximates what a gaming rate of 20% does to the observed number.
   中文翻译：在模拟器中引入 eval-context gaming：将约 20% 失败任务翻转为成功。报告新时间线。这近似 20% 博弈率对观测数字的影响。

5. Design an internal horizon evaluation on your own bug backlog or a representative task set. Describe the data collection, the fit, and what the output tells you. Compare to METR numbers.
   中文翻译：在自己的 bug backlog 或代表性任务集上设计内部时间线评估。描述数据收集、拟合和输出告诉你什么。与 METR 数字比较。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Further Reading | 延伸阅读

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) — HCAST, RE-Bench, SWAA specs.
  中文翻译：HCAST、RE-Bench、SWAA 规范
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) — the original horizon paper.
  中文翻译：原始时间线论文
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) — current numbers and methodology.
  中文翻译：当前数字和方法论
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons) — live tracking.
  中文翻译：实时跟踪
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — internal perspective on METR's measurements.
  中文翻译：METR 测量的内部视角
