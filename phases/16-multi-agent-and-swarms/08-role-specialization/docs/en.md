# Role Specialization — Planner, Critic, Executor, Verifier | 专业化 批评者 计划 角色

> The most common multi-agent decomposition in 2026: one agent plans, one executes, one critiques or verifies. MetaGPT (arXiv:2308.00352) formalizes this as SOPs encoded into role prompts — Product Manager, Architect, Project Manager, Engineer, QA Engineer — following `Code = SOP(Team)`. ChatDev (arXiv:2307.07924) chains designer, programmer, reviewer, tester through a "chat chain" with "communicative dehallucination" (agents explicitly request missing details). The verifier is load-bearing: Cemri et al. (MAST, arXiv:2503.13657) show every multi-agent failure can be traced to missing or broken verification. PwC reported 7× accuracy gain (10% → 70%) from structured validation loops in CrewAI.

> **【中文解读】** 本节介绍了角色专业化——为每个 Agent 分配明确的角色和专长，提升整体团队效率。

> **【拓展：role specialization→具体应用】** 角色专业化是 CrewAI 的核心理念——每个 Agent 有角色（Role）、目标（Goal）和背景故事（Backstory）。实践表明，明确的角色定义能显著提高多 Agent 协作的效率。但过度专业化也有风险——角色边界过于严格会导致 Agent 拒绝做'不是自己职责'但必要的操作。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·04-05（原语+Supervisor）。本节是 2026 最常见的多 Agent 分解模式：Planner + Critic + Executor + Verifier。
> 💡 **【类比】** 角色专业化 = "电影制作团队"。Planner = 编剧（定方向）、Executor = 演员（执行）、Critic = 内审、Verifier = 质检员。MetaGPT、ChatDev、CrewAI 都用这种角色分解。Cemri 等人 MAST 论文：所有多 Agent 失败都能追溯到"缺少或破损的 Verifier"——验证是承重墙。PwC 案例：加 Verifier 让准确率从 10% 飙到 70%（7 倍）。

## Problem | 问题引入

Generic multi-agent systems produce generic output. Three coders in a group chat write three flavors of the same mediocre code. You can add more agents, add more rounds, and still not cross the quality threshold.

> 通用的多 Agent 系统产生通用输出。群聊中的三个编码器写出三种风味的同样平庸的代码。你可以添加更多 Agent、更多轮次，仍然无法跨越质量门槛。

The problem is not quantity but uniformity. Three identical agents given the same task will produce three similar wrong answers. They share the same blind spots because they share the same prompt and model. Adding more of the same does not help; you need agents that are different in productive ways.

> 问题不是数量而是同质性。三个相同 Agent 给定相同任务会产生三个相似错误答案。它们共享相同盲点因为共享相同提示和模型。添加更多相同没有帮助；你需要以生产方式不同的 Agent。

The fix is not more agents — it is *different* agents. Assign distinct roles. Give the critic tools the planner does not have. Give the verifier an objective test suite. Now the system has internal disagreement with grounded correction, not just parallel guessing.

> 修复方法不是更多 Agent——而是*不同*的 Agent。分配不同的角色。给批评者规划者没有的工具。给验证者一个客观的测试套件。现在系统有了基于事实纠正的内部分歧，而不是并行猜测。

The key shift: from "more agents doing the same thing" to "different agents doing different things." Parallelism without specialization is just expensive guessing. Specialization creates the asymmetry that lets the system catch its own errors.

> 关键转变：从"更多 Agent 做相同的事"到"不同 Agent 做不同的事"。没有专业化的并行性只是昂贵的猜测。专业化创造让系统捕获自己错误的不对称性。

## Concept | 核心概念

### The four canonical roles

**Planner.** Reads the goal, produces a step list or a spec. Tools: knowledge retrieval, docs. Output: structured plan.

> **规划者。** 读取目标，产生步骤列表或规范。工具：知识检索、文档。输出：结构化计划。

**Executor.** Reads one plan step at a time, produces the artifact. Tools: the actual work tools (code compiler, shell, API client). Output: the artifact.

> **执行者。** 每次读取一个计划步骤，产生工件。工具：实际工作工具（代码编译器、shell、API 客户端）。输出：工件。

**Critic.** Reads the executor's output against the planner's intent. Tools: read-only access to the artifact, static analysis. Output: accept/reject with reasons.

> **批评者。** 根据规划者的意图阅读执行者的输出。工具：对工件的只读访问、静态分析。输出：接受/拒绝及原因。

**Verifier.** Reads the artifact and runs a deterministic check. Tools: test runner, type checker, schema validator. Output: pass/fail with evidence.

> **验证者。** 读取工件并运行确定性检查。工具：测试运行器、类型检查器、模式验证器。输出：通过/失败及证据。

Critic is subjective, opinionated, often LLM-based. Verifier is objective, deterministic, often code-based. They are not the same role.

> 批评者是主观的、有观点的，通常基于 LLM。验证者是客观的、确定性的，通常基于代码。它们不是同一个角色。

Conflating them is the most common multi-agent design error. A system with only critics (LLM reviewers) gets plausible-but-wrong output. A system with only verifiers (code checks) gets correct-but-ugly output. You need both: critic for taste, verifier for correctness.

> 将它们混为一谈是最常见的多 Agent 设计错误。只有批评者（LLM 审阅者）的系统得到似是而非但错误的输出。只有验证者（代码检查）的系统得到正确但丑陋的输出。两者都需要：批评者负责品味，验证者负责正确性。

### MetaGPT's SOP pattern

MetaGPT (arXiv:2308.00352) encodes software engineering SOPs as role prompts:

> MetaGPT（arXiv:2308.00352）将软件工程 SOP 编码为角色提示：

The "SOP" framing is borrowed from human organizations: Standard Operating Procedures turn ad-hoc work into repeatable process. MetaGPT applies this to LLMs — the SOP becomes a system prompt that constrains the LLM to a specific role with specific outputs.

> "SOP"框架借鉴自人类组织：标准操作流程将临时工作转化为可重复流程。MetaGPT 将此应用于 LLM——SOP 成为将 LLM 约束到具有特定输出的特定角色的系统提示。

- **Product Manager** writes the PRD.
  中文翻译：**产品经理**编写 PRD。
- **Architect** produces the system design.
  中文翻译：**架构师**产生系统设计。
- **Project Manager** splits tasks.
  中文翻译：**项目经理**拆分任务。
- **Engineer** implements.
  中文翻译：**工程师**实现。
- **QA Engineer** runs tests.
  中文翻译：**QA 工程师**运行测试。

Each role has a strict input/output schema. The role prompt says what the role *is* and what it *must produce*. The `Code = SOP(Team)` formulation — deterministic SOPs turn a team of LLMs into a predictable pipeline.

> 每个角色有严格的输入/输出模式。角色提示说角色*是什么*和*必须产生什么*。`Code = SOP(Team)` 公式——确定性 SOP 将一个 LLM 团队变成一个可预测的流水线。

The key insight: encode the team's workflow as code, not as conversation. Each LLM role is a node in a deterministic graph; the graph structure is human-authored. The LLMs do the local work; humans own the global workflow.

> 关键洞察：将团队工作流编码为代码，而不是对话。每个 LLM 角色是确定性图中的节点；图结构由人类编写。LLM 做局部工作；人类拥有全局工作流。

### ChatDev's communicative dehallucination

ChatDev adds a key move: when an executor needs a specific detail that was not in the plan, it explicitly asks the designer before continuing. This prevents the classic LLM failure of plausibly inventing the detail.

> ChatDev 添加了一个关键举措：当执行者需要一个计划中没有的具体细节时，它在继续之前明确询问设计者。这防止了 LLM 经典的似是而非地发明细节的失败。

The pattern catches hallucinations at their source. Instead of detecting fabricated details after the fact (hard), it prevents fabrication by requiring the executor to ask before assuming. The cost is an extra round-trip; the benefit is correctness.

> 该模式在源头捕获幻觉。不是事后检测虚构细节（难），而是通过要求执行者在假设前询问来防止虚构。成本是额外往返；收益是正确性。

Implementation: the role prompt includes "when you need specific information you were not given, ask the relevant role by name before producing output."

> 实现：角色提示包括"当你需要你未被提供的具体信息时，在产生输出之前按名称询问相关角色。"

### Why verifier matters most

Cemri et al. (MAST) traced 1642 multi-agent execution failures. 21.3% were verification gaps — the system shipped an answer no one had checked. The remaining 79% often trace back to "there was a check that failed silently or was never run." Verification is the load-bearing role.

> Cemri 等人（MAST）追踪了 1642 个多 Agent 执行失败。21.3% 是验证缺口——系统发布了没有人检查过的答案。其余 79% 通常追溯到"有一个检查静默失败或从未运行"。验证是承重角色。

The 21.3% number is the single most cited statistic in 2026 multi-agent engineering. It says: if you only add one role to your system, make it a verifier. Not a critic, not a planner — a deterministic verifier with code-level checks.

> 21.3% 这个数字是 2026 年多 Agent 工程中被引用最多的统计。它说：如果你只在系统中添加一个角色，让它成为验证者。不是批评者，不是规划者——一个带代码级检查的确定性验证者。

PwC reported (CrewAI deployments, 2025) that adding a structured validation loop moved accuracy from 10% to 70%. 7x gain from one role.

> PwC 报告（CrewAI 部署，2025）添加结构化验证循环将准确率从 10% 提高到 70%。一个角色带来 7 倍提升。

### Critic vs verifier

- A critic is an LLM reviewing an artifact for quality. Subjective. Can be fooled by plausible prose.
  中文翻译：批评者是一个审查工件质量的 LLM。主观的。可以被似是而非的散文愚弄。
- A verifier is a deterministic program running on the artifact. Objective. Gives pass/fail with evidence.
  中文翻译：验证者是在工件上运行的确定性程序。客观的。给出通过/失败及证据。

Use both. Critic catches taste issues the verifier cannot articulate. Verifier catches bugs the critic cannot see because they show up only at runtime.

> 两者都用。批评者捕获验证者无法表达的质量问题。验证者捕获批评者看不到的 bug，因为它们只在运行时出现。

A common ordering: verifier first (fast, kills obviously broken work), then critic (slow, refines quality). Some teams flip the order to catch taste issues before spending compute on broken code. Test which works for your task.

> 常见顺序：先验证者（快，杀死明显破损的工作），然后批评者（慢，精炼质量）。一些团队翻转顺序以在花计算资源修复破损代码之前捕获质量问题。测试哪种适合你的任务。

### The anti-pattern

Every role in your system is an LLM and every role's output is "looks good to me." Classic MAST failure mode. Add at least one verifier whose pass/fail is decided by code, not by an LLM.

> 你系统中每个角色都是 LLM，每个角色的输出都是"看起来不错"。经典的 MAST 失败模式。至少添加一个由代码而不是 LLM 决定通过/失败的验证者。

### Framework mappings

- **CrewAI** — `Agent(role, goal, backstory)` is the textbook specialization surface.
  中文翻译：**CrewAI** — `Agent(role, goal, backstory)` 是教科书式的专业化表面。
- **LangGraph** — nodes can have specialized prompts; edges enforce the pipeline.
  中文翻译：**LangGraph** — 节点可以有专门的提示；边强制流水线。
- **AutoGen** — role-specific ConversableAgents with one-word names in a GroupChat.
  中文翻译：**AutoGen** — 在 GroupChat 中具有单词名称的角色特定 ConversableAgent。
- **OpenAI Agents SDK** — handoff tools between role-specialized Agents.
  中文翻译：**OpenAI Agents SDK** — 角色专业化 Agent 之间的交接工具。

## Build It | 动手实现

`code/main.py` implements a 4-role pipeline building a simple Python function:

> `code/main.py` 实现了一个构建简单 Python 函数的 4 角色流水线：

- **Planner** produces a spec.
  中文翻译：**规划者**产生规范。
- **Executor** generates a code string.
  中文翻译：**执行者**生成代码字符串。
- **Critic** (LLM-simulated) flags obvious issues.
  中文翻译：**批评者**（LLM 模拟）标记明显问题。
- **Verifier** runs the generated code in a sandbox (`exec`) against a test case.
  中文翻译：**验证者**在沙箱（`exec`）中针对测试用例运行生成的代码。

Demo runs twice: once where the executor produces correct code (critic + verifier both pass), once where the executor produces off-spec code (critic misses the bug because it looks plausible, verifier catches it because the test fails).

> 演示运行两次：一次执行者产生正确的代码（批评者 + 验证者都通过），一次执行者产生偏离规范的代码（批评者因为看起来合理而错过了 bug，验证者因为测试失败而捕获了它）。

## Use It | 用框架实现

`outputs/skill-role-designer.md` takes a task and produces the role roster (3-5 roles), the input/output schema per role, and the verifier check. Use this before wiring agents into a framework.

> `outputs/skill-role-designer.md` 接收任务并产生角色名册（3-5 个角色）、每个角色的输入/输出模式和验证者检查。在将 Agent 连接到框架之前使用。

## Ship It | 产出物

Checklist:

> 检查清单：

- **At least one deterministic verifier.** Never all-LLM.
  中文翻译：**至少一个确定性验证者。** 永远不要全 LLM。
- **Explicit I/O schema per role.** The planner returns a spec, not prose; the executor reads that schema.
  中文翻译：**每个角色有明确的 I/O 模式。** 规划者返回规范，不是散文；执行者读取该模式。
- **Communicative dehallucination.** Executor must ask the planner when info is missing; never invent it.
  中文翻译：**交流去幻觉。** 执行者在信息缺失时必须询问规划者；永远不要发明。
- **Critic/verifier ordering.** Run critic first (cheap, catches design issues), verifier second (slow, catches bugs).
  中文翻译：**批评者/验证者顺序。** 先运行批评者（便宜，捕获设计问题），再运行验证者（慢，捕获 bug）。
- **Loop budget.** Max 2 critic-executor revision rounds before escalating to human.
  中文翻译：**循环预算。** 在升级到人类之前最多 2 个批评者-执行者修订轮。

## Exercises | 练习题

1. Run `code/main.py` and observe how the verifier catches the bug the critic missed. Add a static-analysis check (count occurrences of `return`) as an additional verifier. What does it catch that the runtime test misses?
   中文翻译：运行 `code/main.py` 并观察验证者如何捕获批评者错过的 bug。添加一个静态分析检查（计算 `return` 的出现次数）作为额外验证者。它捕获了运行时测试错过的什么？
2. Add a 5th role: "requirements analyst" that translates user wish into planner-ready spec. What communicative dehallucination requests should flow up to it?
   中文翻译：添加第 5 个角色："需求分析师"，将用户愿望翻译为规划者可用的规范。什么样的交流去幻觉请求应该流向上方？
3. Read MetaGPT Section 3 ("Agents"). List the input/output schema of each of MetaGPT's 5 roles.
   中文翻译：阅读 MetaGPT 第 3 节（"Agent"）。列出 MetaGPT 5 个角色中每个的输入/输出模式。
4. Read ChatDev's chat-chain diagram (arXiv:2307.07924 Figure 3). Identify where communicative dehallucination breaks a loop that would otherwise be infinite.
   中文翻译：阅读 ChatDev 的聊天链图（arXiv:2307.07924 图 3）。识别交流去幻觉在哪里打破了否则会是无限的循环。
5. PwC's 7x accuracy gain came from verification loops. Hypothesize three tasks where adding a verifier would not help — where deterministic checking of correctness is impossible or prohibitively expensive.
   中文翻译：PwC 的 7 倍准确率提升来自验证循环。假设三个添加验证者不会有帮助的任务——确定性正确性检查不可能或代价过高的任务。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Further Reading | 延伸阅读

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) — the SOP-as-role-prompt reference paper
  中文翻译：Hong 等人 — MetaGPT：多 Agent 协作的元编程 — SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) — chat chain + communicative dehallucination
  中文翻译：Qian 等人 — 软件开发的通信 Agent（ChatDev）— 聊天链 + 交流去幻觉
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) — MAST taxonomy; verification gaps are 21.3% of failures
  中文翻译：Cemri 等人 — 为什么多 Agent LLM 系统会失败？— MAST 分类法；验证缺口占失败的 21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) — production role specification surface
  中文翻译：CrewAI 文档 — Agent 角色 — 生产角色规范表面
