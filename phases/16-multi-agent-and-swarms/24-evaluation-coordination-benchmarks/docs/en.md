# Evaluation and Coordination Benchmarks | 协调基准 评估

> Five 2025-2026 benchmarks cover the multi-agent evaluation space. **MultiAgentBench / MARBLE** (ACL 2025, arXiv:2503.01935) evaluates star/chain/tree/graph topologies with milestone KPIs; **graph is best for research**, cognitive planning adds ~3% milestone achievement. **COMMA** evaluates multimodal asymmetric-information coordination; state-of-the-art models including GPT-4o struggle to beat a random baseline. **MedAgentBoard** (arXiv:2505.12371) covers four medical task categories and often finds multi-agent does not dominate single-LLM. **AgentArch** (arXiv:2509.10769) benchmarks enterprise agent architectures combining tool-use + memory + orchestration. **SWE-bench Pro** ([arXiv:2509.16941](https://arxiv.org/abs/2509.16941)) has 1865 problems across 41 repos spanning business apps, B2B services, and developer tools; frontier models score ~23% on Pro vs 70%+ on Verified — a reality check on contamination. Claude Opus 4.7 (April 2026) is reported at **64.3%** on Pro with explicit agent-teams coordination (no Anthropic primary source published yet — treat as preliminary); Verdent (agent scaffold) hits **76.1% pass@1** on Verified ([Verdent technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report)). **AAAI 2026 Bridge Program WMAC** (https://multiagents.org/2026/) is the 2026 community focal point. This lesson builds on MARBLE's metrics, runs a topology-vs-metric sweep, and pins the "just passing SWE-bench Verified is not evidence of generalization" rule.

> **【中文解读】** 本节介绍了协调基准评估——衡量多 Agent 系统协调能力的评估方法。

> **【拓展：evaluation coordination benchmarks→具体应用】** 多 Agent 协调评估基准：(1) AgentBench——多 Agent 任务完成度评估；(2) CLEVA——LLM Agent 评估框架；(3) SWE-bench——多 Agent 协作修复 bug。关键评估维度：任务完成率、协调效率（步数/成本）、鲁棒性（Agent 故障时的表现）和可扩展性（Agent 数量增加时的性能变化）。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 15 (Voting and Debate Topology), Phase 16 · 23 (Failure Modes) | **前置知识:** Phase 16 · 15（投票与辩论拓扑），Phase 16 · 23（失败模式）

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·15（投票拓扑）、Phase 16·23（失败模式）、SWE-bench 概念。5 个 2026 主流多 Agent 基准横向对比。
> 💡 **【类比】** 多 Agent 基准 = "AI 团队的标准化考试"。MARBLE 测拓扑（图最佳做研究）；COMMA 测多模态不对称信息协调（GPT-4o 都难超随机基线）；MedAgentBoard 测医疗（多 Agent 常不胜单 LLM）；SWE-bench Pro 测真实代码（1865 题/41 仓库，前沿模型仅 23%，对比 Verified 70%+，揭露污染问题）。Claude Opus 4.7 多 Agent 协调达 64.3%。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

When a paper claims "our multi-agent system is better," the question is: better than what, on what, measured how? The 2023-2024 era of multi-agent evaluation was chaos — everyone picked their own metrics, their own baselines, and their own task sets. The 2025-2026 benchmarks imposed structure.

> 当论文声称"我们的多 Agent 系统更好"时，问题是：比什么更好，在什么上更好，用什么衡量？2023-2024 年的多 Agent 评估是混乱的——每个人都选择自己的指标、基线和任务集。2025-2026 年基准测试引入了结构。

Without shared benchmarks, you cannot compare two multi-agent systems meaningfully. Worse, without hold-out benchmarks, frontier models can contaminate. SWE-bench Verified became partially contaminated in training corpora by mid-2025; frontier scores inflated; Pro was designed as an uncontaminated reality check.

> 没有共享基准，你无法有意义地比较两个多 Agent 系统。更糟的是，没有保留基准，前沿模型可能被污染。SWE-bench Verified 在 2025 年中期部分污染了训练语料；前沿分数膨胀；Pro 被设计为无污染的现实检验。

This lesson enumerates the five canonical 2026 benchmarks, names what each measures, and teaches you to read benchmark claims skeptically.

> 本课列举了五个规范的 2026 年基准测试，命名每个测量什么，并教你持怀疑态度阅读基准声明。

## Concept | 核心概念

### MultiAgentBench (MARBLE) — ACL 2025

arXiv:2503.01935. Evaluates four coordination topologies (star, chain, tree, graph) on research, coding, and planning tasks. Milestone-based KPIs track partial progress rather than only final success.

Measured results:

- **Graph** topology best for research scenarios; supports any-to-any critique.
- **Chain** best for stepwise-refinement coding.
- **Star** best for fast-factual consolidation.
- **Coordination tax** appears past ~4 agents on graph.
- **Cognitive planning** adds ~3% milestone achievement across topologies.

Use when: you want to compare coordination topologies apples-to-apples. The MARBLE repo (https://github.com/ulab-uiuc/MARBLE) provides the evaluator.

### COMMA — multimodal asymmetric information

Covers tasks where agents have different observation modalities and must coordinate without full information sharing. The reported result is uncomfortable: frontier models including GPT-4o struggle to beat a **random baseline** on agent-agent collaboration in COMMA. The signal is that multi-agent modalities are under-trained and under-evaluated — LLMs handle single-modality cooperation reasonably; multi-modality coordination collapses.

Use when: your system has multimodal or asymmetric-information coordination. The null result from COMMA is a warning to measure before claiming.

### MedAgentBoard — domain stress test

arXiv:2505.12371. Four medical task categories: diagnosis, treatment planning, report generation, patient communication. Compares multi-agent vs single-LLM vs conventional rule-based systems.

Finding: multi-agent does NOT dominate single-LLM on most categories. The multi-agent advantage is narrow — task decomposition helps when the subtasks are clearly separable (diagnosis + treatment); it hurts when coordination overhead exceeds specialization gain (report generation).

Use when: your domain has clear-cut single-LLM baselines. If MedAgentBoard's lesson generalizes, many proposed multi-agent systems are over-engineered.

### AgentArch — enterprise architectures

arXiv:2509.10769. Enterprise settings with tool use, memory, and orchestration layered together. Benchmark isolates the contribution of each layer: how much does adding tools help? Adding memory? Adding multi-agent orchestration?

Use when: you are designing an enterprise agent stack and need to justify each layer. AgentArch helps avoid buying features you cannot measure the value of.

### SWE-bench Pro — the reality check

arXiv:2509.16941. 1865 problems across 41 repositories spanning business apps, B2B services, and developer tools. Designed to be **uncontaminated** with later training cutoffs. Frontier models score ~23% on Pro vs 70%+ on Verified. The gap is the contamination signal.

April 2026 scores:
- Claude Opus 4.7 on Pro: **64.3%** (reported with explicit agent-teams coordination; no Anthropic primary source published yet — treat as preliminary).
- Verdent (agent scaffold) on Verified: **76.1% pass@1** ([technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report)).
- Frontier raw scores on Pro without agent scaffolding: ~23-35% ([SWE-bench Pro paper](https://arxiv.org/abs/2509.16941)).

The takeaway: "we beat SWE-bench Verified" is no longer evidence of capability. Pro is the current gating test. Agent-team scaffolding produces measurable gains on Pro (~30-40 point delta), which is one of the strongest empirical arguments for multi-agent coordination in 2026.

### AAAI 2026 WMAC

AAAI 2026 Bridge Program — Workshop on Multi-Agent Coordination (https://multiagents.org/2026/). The 2026 community focal point for multi-agent AI research. Accepted papers and workshop proceedings are the canonical venue for evaluating new methods; defer to WMAC-accepted claims over arXiv preprints for production decisions.

### Read benchmark claims skeptically — the 2026 checklist

When someone claims a multi-agent result:

1. **Which benchmark, which split?** SWE-bench Verified vs Pro matters a lot. A number reported on the wrong split is worthless.
   中文翻译：**哪个基准，哪个分割？** SWE-bench Verified vs Pro 差别很大。在错误分割上报告的数字毫无价值。
2. **Contamination check.** Was the benchmark released after the model's training cutoff? If not, treat with caution.
   中文翻译：**污染检查。** 基准是否在模型训练截止日期之后发布？如果不是，谨慎对待。
3. **Baseline comparison.** Vs single-LLM baseline, vs random, vs prior multi-agent work. Not "vs untuned version of the same system."
   中文翻译：**基线比较。** 对比单 LLM 基线、随机、先前多 Agent 工作。不是"对比同一系统的未调优版本。"
4. **Statistical significance.** N trials, p-value, confidence interval. Frontier models are high-variance; single runs mislead.
   中文翻译：**统计显著性。** N 次试验、p 值、置信区间。前沿模型是高方差的；单次运行误导。
5. **Task diversity.** One task or many? Generalization matters for production.
   中文翻译：**任务多样性。** 一个任务还是多个？泛化对生产重要。
6. **Cost disclosure.** Tokens per task, wall-clock. A 90% solution at 20x cost is a business decision, not a capability claim.
   中文翻译：**成本披露。** 每任务 token、挂钟时间。20 倍成本的 90% 解决方案是商业决策，不是能力声明。

### What none of the benchmarks measure well

- **Long-horizon coordination.** Days of wall-clock interaction. All current benchmarks run short.
- **Adversarial resilience.** What happens when one agent is malicious or compromised?
- **Drift under deployment.** Benchmarks are static; production distributions shift.
- **Cost-normalized performance.** Most benchmarks report raw accuracy, not accuracy-per-dollar.

Building your own internal benchmark for the axis you actually care about is often the right move.

## Build It | 动手构建

`code/main.py` is a non-interactive walk-through:

- Simulates 3 multi-agent systems on a toy task.
- Computes MARBLE-style milestone metrics for each.
- Runs a contamination check by withholding tasks from a "training" set.
- Compares to a random baseline explicitly.
- Prints a benchmark-claims scorecard.

Run:

```bash
python3 code/main.py
```

Expected output: system scorecard with raw accuracy, milestone achievement, cost-per-task, vs-random baseline delta, and a contamination-check note.

## Use It | 使用方法

`outputs/skill-benchmark-reader.md` reads any multi-agent benchmark claim and applies the scrutiny checklist. Output: a grade and caveats.

## Ship It | 部署上线

Production evaluation discipline:

- **Build an internal benchmark** that reflects your actual production distribution. Public benchmarks inform but do not substitute.
  中文翻译：**构建内部基准**反映你的实际生产分布。公共基准提供信息但不能替代。
- **Include a random baseline** in every comparison. If you cannot beat random by a large margin on a coordination task, the task may be ill-posed.
  中文翻译：**在每个比较中包含随机基线。** 如果你不能在协调任务上大幅超越随机，任务可能定义不当。
- **Report cost alongside accuracy.** Token cost and wall-clock. Ops teams need both.
  中文翻译：**同时报告成本和准确率。** Token 成本和挂钟时间。运维团队都需要。
- **Rebuild the benchmark quarterly.** Production distribution shifts; stale benchmarks mislead.
  中文翻译：**每季度重建基准。** 生产分布偏移；过时的基准会误导。
- **Avoid published-benchmark overfitting.** If your team is optimizing specifically for SWE-bench Pro numbers, you will regress on production.
  中文翻译：**避免公开基准过拟合。** 如果你的团队专门优化 SWE-bench Pro 数字，你会在生产上退化。

## Exercises | 练习题

1. Run `code/main.py`. Identify which of the three simulated systems has the best cost-per-milestone. Does it match the highest raw-accuracy system?
2. Read MultiAgentBench (arXiv:2503.01935). For your own task domain, decide which of the four topologies MARBLE would recommend. Justify from the paper's results.
3. Read the SWE-bench Pro paper. What specifically makes it contamination-resistant? Could the same technique be applied to other benchmarks you care about?
4. Read COMMA's finding on multimodal coordination. Design a simple multimodal coordination task you could add to your internal benchmark. What would count as a useful signal?
5. Apply the benchmark-claims checklist to one recent multi-agent paper's headline result. What grade would you give the claim?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARBLE | "MultiAgentBench" / "多 Agent 基准" | ACL 2025; star/chain/tree/graph topologies with milestone KPIs. / ACL 2025；星形/链形/树形/图形拓扑，带里程碑 KPI。 |
| COMMA | "Multimodal benchmark" / "多模态基准" | Multimodal asymmetric-info coordination; frontier models struggle vs random. / 多模态不对称信息协调；前沿模型难以超越随机基线。 |
| MedAgentBoard | "Domain stress test" / "领域压力测试" | Four medical categories; often finds multi-agent does not dominate single-LLM. / 四个医疗类别；常发现多 Agent 不优于单 LLM。 |
| AgentArch | "Enterprise benchmark" / "企业基准" | Tools + memory + orchestration layered. / 工具 + 记忆 + 编排分层。 |
| SWE-bench Pro | "Contamination-resistant" / "抗污染" | 1865 problems, 41 repos; ~23% vs 70%+ on Verified (the contamination signal). / 1865 个问题，41 个仓库；~23% vs Verified 上 70%+（污染信号）。 |
| Milestone achievement / 里程碑达成 | "Partial credit" / "部分积分" | Benchmarks that reward progress, not only final success. / 奖励进展而非仅最终成功的基准。 |
| Contamination / 污染 | "Benchmark leaked into training" / "基准泄露到训练" | Post-release, benchmarks drift into training corpora; scores inflate. / 发布后，基准渗入训练语料；分数膨胀。 |
| WMAC | "AAAI 2026 Bridge Program" / "AAAI 2026 桥接项目" | Workshop on Multi-Agent Coordination; community focal point. / 多 Agent 协调研讨会；社区焦点。 |

## Further Reading | 延伸阅读

- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) — topology benchmark with milestone KPIs
- [MARBLE repository](https://github.com/ulab-uiuc/MARBLE) — reference implementation
- [MedAgentBoard](https://arxiv.org/abs/2505.12371) — domain stress test; multi-agent often does not dominate
- [AgentArch](https://arxiv.org/abs/2509.10769) — enterprise agent architectures
- [SWE-bench leaderboards](https://www.swebench.com/) — Verified and Pro scores for frontier models
- [AAAI 2026 WMAC](https://multiagents.org/2026/) — the 2026 community focal point
