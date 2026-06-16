# Automated Alignment Research (Anthropic AAR) | 自动化对齐研究（Anthropic AAR）

> Anthropic ran parallel teams of Claude Opus 4.6 Autonomous Alignment Researchers in independent sandboxes, coordinating via a shared forum whose logs live outside any sandbox (so agents cannot delete their own records). On the weak-to-strong training problem, the AARs outperformed human researchers. Anthropic's own summary flags that prescribed workflows often constrain AAR flexibility and degrade performance. Automating alignment research is the compression step that compresses the timeline to the exact misalignment risks the RSP is meant to detect.

> **【中文解读】** Anthropic 在独立沙箱中并行运行多组 Claude Opus 4.6 自主对齐研究器（AAR），通过共享论坛协调——论坛日志存储在任何沙箱之外（这样 Agent 无法删除自己的记录）。在弱到强训练问题上，AAR 优于人类研究者。Anthropic 自己的总结指出规定的工作流通常限制 AAR 灵活性并降低性能。自动化对齐研究是压缩步骤，将时间线压缩到 RSP 旨在检测的确切不对齐风险。

> **【拓展：自主研究 Agent 的双重性】** AAR 的存在有"压缩"和"双重用途"两面：正面是能加速对齐研究；反面是同一系统也能自动化"破坏对齐"。RSP 把"AI R&D 自动化阈值"作为升级控制触发器，正是因为这个对称性。Anthropic 选择把日志放在 Agent 沙箱之外——这是经典的"trust-but-verify"基础设施模式（与 2026 年企业勒索软件防御用的 WORM 存储同源）。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, parallel-research-forum simulator) | **语言:** Python（标准库，并行研究论坛模拟器）
**Prerequisites:** Phase 15 · 05 (AI Scientist v2), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 05（AI Scientist v2），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·05（AI Scientist v2 开放研究）、Phase 15·04（DGM 自我修改）、Phase 18·11（Scalable Oversight 弱到强监督）。AAR = AI Scientist 用于"AI 安全研究本身"——既是工具也是风险。
> 💡 **【类比】** AAR = "AI 给自己写体检报告"。AI Scientist v2 = AI 做普通科研；AAR = AI 研究怎么让 AI 自己更安全。问题：医生能给自己开刀吗？Anthropic 的设计 = 多个 AI 在隔离沙箱里独立工作，通过"论坛"交流，但论坛日志存在沙箱外（AI 删不掉自己的工作记录）。这种 trust-but-verify 模式是关键安全机制。
> 🤔 **【困惑】** Q: 既然 AI 能做对齐研究，为什么还需要人类？— AI 能加速但无法保证完整性。弱到强监督的根本困境（Phase 18·11）：弱监督者（人类或弱 AI）可能漏掉强 AI 的隐蔽行为。AAR 是加速器不是替代品——人类仍需把关研究方向和评估标准。

## The Problem | 问题引入

> **【中文解读】** 自动化对齐研究探索 AI 系统是否能自主发现和修复自身的安全问题。核心问题是：AI 能否成为自己安全研究的助手？Anthropic 和 Redwood Research 的实验表明，LLM 可以生成对齐研究人员认为有用的安全洞见，但还不具备独立完成端到端安全研究的能力。

> **【拓展：automated alignment research】** 自动化对齐研究是 2025-2026 年 AI 安全领域的热点。Anthropic 的论文探讨了用 AI 辅助监督更强大的 AI 的可行性。关键挑战是'监督挤压'——较弱模型的监督是否能捕捉到更强模型的所有危险行为？当前证据表明，LLM 可以帮助人类研究者加速安全分析，但完全自动化的安全保证仍需要人类参与。

Alignment research is expensive in human-researcher time.

> 对齐研究在人类研究者时间方面很昂贵。

Problems like scalable oversight, reward specification, or weak-to-strong training require experiments that take weeks per iteration. As frontier capabilities advance, the alignment workload grows faster than the supply of qualified researchers.

> 可扩展监督、奖励规范或弱到强训练等问题需要每次迭代数周的实验。随着前沿能力提升，对齐工作量的增长速度超过合格研究者的供给。

Automated Alignment Research (AAR) asks whether the same frontier models whose capability is outrunning alignment can contribute to closing the gap. Anthropic's 2026 report on an AAR-run weak-to-strong-training study (alignment.anthropic.com/2026/automated-w2s-researcher/) is one of the first public results from a deployed system of this class.

> 自动化对齐研究（AAR）询问能力正跑赢对齐的同一前沿模型能否贡献于闭合差距。Anthropic 2026 年关于 AAR 运行弱到强训练研究的报告是该类别部署系统的首批公开结果之一。


> **【中文解读】** 本节介绍了 AI 安全对齐技术——确保 AI 系统行为符合人类意图和价值观。

The result is genuinely positive: AARs solved a research problem better than the human baseline. The result also concentrates, in a single system, every concern this phase has developed.

> 结果是真正正面的：AAR 在研究问题上优于人类基线。但这个结果也将本阶段发展出的所有关注点集中在了一个系统中。

If alignment research can be automated, so can the parts that compromise safeguards. The RSP's thresholds for AI R&D capability are written with this loop in mind.

> 如果对齐研究可自动化，那么破坏保障措施的部分也可自动化。RSP 对 AI R&D 能力的阈值正是带着这一循环编写的。

## The Concept | 核心概念

### The architecture (as publicly described) | 架构（公开描述）

- **Parallel agents.** Multiple Claude Opus 4.6 instances run as AARs, each in an independent sandbox. Sandboxes limit filesystem, network, and process surface.
  中文翻译：**并行 Agent。** 多个 Claude Opus 4.6 实例作为 AAR 运行，每个在独立沙箱中。沙箱限制文件系统、网络和进程表面。
- **Shared forum.** Findings are published to a shared forum whose storage backend sits outside every sandbox. Agents can read the forum; agents cannot delete or edit forum records from within their own sandbox.
  中文翻译：**共享论坛。** 发现发布到共享论坛，其存储后端位于每个沙箱之外。Agent 可读论坛；Agent 不能从自己的沙箱内删除或编辑论坛记录。
- **Task allocation.** A human-designed task queue assigns research problems to AARs. AARs propose decompositions, run experiments, write up findings.
  中文翻译：**任务分配。** 人工设计的任务队列将研究问题分配给 AAR。AAR 提议分解、运行实验、撰写发现。
- **Weak-to-strong training focus.** The published study addressed weak-to-strong training — using a weaker supervisor model to train a stronger student model. AARs outperformed human researchers on this task.
  中文翻译：**弱到强训练聚焦。** 已发表的研究针对弱到强训练——使用较弱的监督模型训练较强的学生模型。AAR 在此任务上优于人类研究者。

### Why the out-of-sandbox log matters | 沙箱外日志为何重要

The log-integrity property is the difference between a controlled experiment and a potentially compromised one.

> 日志完整性属性是受控实验与可能受损实验之间的区别。

If AARs could edit their own logs, they could cover up failed or dubious experiments. Anthropic flags this directly: the property is a necessary condition for trusting the research output, and it is non-trivial to verify.

> 如果 AAR 可编辑自己的日志，它们可掩盖失败或可疑实验。Anthropic 直接指出：该属性是信任研究输出的必要条件，且验证起来并不平凡。

The analog in infrastructure terms is append-only logs with write-through to external storage (e.g. S3 object-lock, immutable Datadog logs). The agent has no credential to modify past records. This is the same pattern that 2026 corporate security teams use to make ransomware-resistant audit trails.

> 基础设施术语中的类比是写入到外部存储的仅追加日志（例如 S3 对象锁、不可变 Datadog 日志）。Agent 没有凭据修改过去记录。这是 2026 年企业安全团队用来制作抗勒索软件审计追踪的相同模式。

### The prescribed-workflow tradeoff | 规定工作流的权衡

Anthropic's report notes that prescribed workflows often constrain AAR flexibility and degrade performance.

> Anthropic 的报告指出，规定的工作流通常限制 AAR 灵活性并降低性能。

In other words: if the human designer writes the research plan step-by-step, AARs do worse than if given high-level goals and freedom to decompose. This is consistent with results across agentic research (LangGraph, Microsoft's Agent Framework) — overspecified scaffolds hurt capable agents.

> 换句话说：如果人类设计者逐步编写研究计划，AAR 表现不如给高层目标和分解自由。这与 Agent 式研究的结果一致（LangGraph、Microsoft 的 Agent Framework）——过度规范的脚手架伤害有能力 Agent。

The safety implication is subtle. The flexibility that improves AAR performance is also the flexibility that allows unsanctioned decomposition, novel tool use, and goal-drift. The tradeoff is a design-space decision: how much flexibility buys enough capability to beat humans, without handing the agent room to generalize goals off-distribution?

> 安全含义微妙。提升 AAR 性能的灵活性也是允许未授权分解、新工具使用和目标漂移的灵活性。权衡是设计空间决策：多少灵活性买到足够击败人类的能力，而不给 Agent 在分布外泛化目标的空间？

### The compression risk | 压缩风险

RSP v3.0 (Lesson 19) introduces an AI R&D capability threshold: the ability to fully automate the AI R&D pipeline at competitive cost vs human + AI tools. DeepMind's FSF v3 includes an analogous ML R&D autonomy level. Both frameworks treat this threshold as the trigger for elevated controls.

> RSP v3.0（第 19 课）引入 AI R&D 能力阈值：在与人类 + AI 工具竞争的成本下完全自动化 AI R&D 管道的能力。DeepMind 的 FSF v3 包含类似的 ML R&D 自主级别。两个框架都将此阈值视为升级控制的触发器。

AAR is one step short of the threshold: it automates part of the pipeline (alignment research on specific, well-scoped tasks) but not the end-to-end capability development loop. The timeline question is how fast the gap closes.

> AAR 离阈值一步之遥：它自动化管道的一部分（特定、范围明确任务上的对齐研究）而非端到端能力开发循环。时间线问题是差距多快闭合。

Compressed timelines are the compounding-failure concern. If alignment research and capability research compound at similar rates, the misalignment risk surface grows at least as fast as capability. If capability compounds faster (the historical trend), the gap widens. This is the argument for AAR being a qualified good: each additional alignment result reduces the gap if and only if the research process is trustworthy.

> 压缩时间线是复利失败担忧。如果对齐研究和能力研究以相似速率复利，不对齐风险表面至少和能力一样快地增长。如果能力更快复利（历史趋势），差距扩大。这是 AAR 作为"有限好"的论据：每个额外对齐结果减少差距，当且仅当研究过程可信。

### What AAR does not replace | AAR 不替代什么

Human researchers set the task queue, review results, and hold the constitutional authority.

> 人类研究者设置任务队列、审查结果并持有宪法权威。

The AARs accelerate the middle of the pipeline, not the ends. Anthropic's published outputs include both AAR contributions and human-researcher judgement on what to publish, what to retract, and what to refine.

> AAR 加速管道中间部分，而非两端。Anthropic 已发表的输出包括 AAR 贡献和人类研究者关于发表什么、撤回什么、完善什么的判断。

This matches the propose-then-commit pattern from Lesson 15 applied to research itself: AARs propose; humans commit.

> 这与第 15 课的 propose-then-commit 模式应用于研究本身匹配：AAR 提议；人类承诺。

## Use It | 用框架实现

`code/main.py` simulates a multi-AAR research forum. Three independent "research agents" run in parallel, posting findings to an append-only forum with optional tamper attempts.

> `code/main.py` 模拟多 AAR 研究论坛。三个独立"研究 Agent"并行运行，将发现发布到带可选篡改尝试的仅追加论坛。

Watch:

> 观察：

- How out-of-sandbox logging catches log-tampering attempts.
  中文翻译：沙箱外日志如何捕获日志篡改尝试。
- How task allocation with free decomposition outperforms fixed workflows on harder problems.
  中文翻译：带自由分解的任务分配如何在更难问题上优于固定工作流。
- How a single compromised AAR can contaminate the forum's signal if the log is not tamper-evident.
  中文翻译：日志不可篡改时，单个被攻破的 AAR 如何污染论坛信号。

## Ship It | 产出物

`outputs/skill-aar-deployment-review.md` is a pre-deployment review of an automated-alignment-research pipeline.

> `outputs/skill-aar-deployment-review.md` 是自动化对齐研究管道的部署前审查。

## Exercises | 练习题

1. Run `code/main.py`. Compare the "fixed-workflow" vs "free-decomposition" settings. Does free decomposition always win, or are there problem classes where the fixed workflow is competitive?
   中文翻译：运行 `code/main.py`。比较"固定工作流"与"自由分解"设置。自由分解总是胜出吗，还是有固定工作流有竞争力的问题类？

2. Modify the simulator so one agent attempts log tampering. Confirm the append-only log detects it. Write one paragraph describing exactly what the detection signature looks like in the log.
   中文翻译：修改模拟器让一个 Agent 尝试日志篡改。确认仅追加日志检测到。写一段准确描述日志中检测签名的外观。

3. Read Anthropic's weak-to-strong AAR report. Identify the specific sub-task the AARs beat human researchers on. What made it amenable to automation?
   中文翻译：阅读 Anthropic 弱到强 AAR 报告。识别 AAR 击败人类研究者的具体子任务。什么让它适合自动化？

4. Design a task-queue allocation policy that balances AAR flexibility (better results) against prescribed-workflow constraints (easier audit). Describe how you would A/B test the two.
   中文翻译：设计平衡 AAR 灵活性（更好结果）与规定工作流约束（更易审计）的任务队列分配策略。描述如何 A/B 测试两者。

5. Read RSP v3.0's AI R&D-4 threshold. In one paragraph, describe what you think would cross it that AAR currently does not.
   中文翻译：阅读 RSP v3.0 的 AI R&D-4 阈值。用一段描述你认为什么会跨越它而 AAR 目前不跨越。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AAR | "Automated Alignment Researcher" | Claude Opus 4.6 instance operated autonomously on alignment problems |
| AAR | "自动化对齐研究器" | 在对齐问题上自主操作的 Claude Opus 4.6 实例 |
| Weak-to-strong training | "Training a stronger model with a weaker supervisor" | Classic scalable-oversight benchmark AARs outperformed humans on |
| 弱到强训练 | "用较弱监督者训练较强模型" | AAR 击败人类的经典可扩展监督基准 |
| Shared forum | "Where agents publish findings" | Append-only, out-of-sandbox storage |
| 共享论坛 | "Agent 发布发现之处" | 仅追加、沙箱外存储 |
| Out-of-sandbox log | "Agent cannot edit its own record" | Tamper-evident write-through to external storage |
| 沙箱外日志 | "Agent 不能编辑自己的记录" | 写入外部存储的防篡改透写 |
| Prescribed workflow | "Step-by-step plan from human designer" | Constrains AAR; often degrades performance vs free decomposition |
| 规定工作流 | "人类设计者的逐步计划" | 约束 AAR；通常比自由分解降低性能 |
| Free decomposition | "Agent decides how to break the task" | More capable, harder to audit |
| 自由分解 | "Agent 决定如何拆分任务" | 更有能力，更难审计 |
| AI R&D threshold | "RSP/FSF capability level" | Full automation of R&D pipeline at competitive cost |
| AI R&D 阈值 | "RSP/FSF 能力级别" | 在竞争成本下完全自动化 R&D 管道 |
| Compressed timeline | "Alignment vs capability race" | If capability compounds faster than alignment, misalignment risk grows |
| 压缩时间线 | "对齐与能力竞赛" | 若能力比对齐复利更快，不对齐风险增长 |

## Further Reading | 延伸阅读

- [Anthropic — Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) — primary source.
  中文翻译：主要来源。
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — AI R&D threshold framing.
  中文翻译：AI R&D 阈值框架。
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) — broader agent-autonomy framing.
  中文翻译：更宽的 Agent 自主性框架。
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — ML R&D autonomy levels parallel to RSP.
  中文翻译：与 RSP 平行的 ML R&D 自主级别。
- [Burns et al. (2023). Weak-to-Strong Generalization (OpenAI)](https://openai.com/index/weak-to-strong-generalization/) — the underlying problem AARs attacked.
  中文翻译：AAR 攻击的底层问题。
