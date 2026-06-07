# Anthropic's Workflow Patterns: Simple Over Complex | Anthropic 工作流模式：简单优于复杂

> Schluntz and Zhang (Anthropic, Dec 2024) distinguish workflows (predefined paths) from agents (dynamic tool-use). Five workflow patterns cover most cases. Start with direct API calls. Add agents only when steps cannot be predicted.

> **【中文解读】** Anthropic 在 2024 年 12 月的文章中区分了工作流（预定义路径）和 Agent（动态工具使用）。五种工作流模式覆盖了大多数场景。从直接 API 调用开始。只在步骤无法预测时才添加 Agent。

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Name Anthropic's five workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
  中文翻译：说出 Anthropic 的五种工作流模式：提示链、路由、并行化、编排器-工作者、评估器-优化器。
- Explain the agent-vs-workflow distinction and the engineering cost of each.
  中文翻译：解释 Agent 与工作流的区别及各自的工程成本。
- Identify when to pick a workflow over an agent (and vice versa).
  中文翻译：识别何时选择工作流而非 Agent（反之亦然）。
- Implement all five patterns in stdlib against a scripted LLM.
  中文翻译：用标准库针对脚本 LLM 实现所有五种模式。

## The Problem | 问题引入

Teams reach for multi-agent frameworks for problems that want a single function call. The cost is real: frameworks add layers that obscure prompts, hide control flow, and invite premature complexity. Schluntz and Zhang's Dec 2024 post is the most-cited industry pushback: start simple, add complexity only when it earns its cost.

> 团队为只需要一次函数调用的问题选择多 Agent 框架。代价是真实的：框架添加了模糊提示、隐藏控制流、引入过早复杂性的层。Schluntz 和 Zhang 2024 年 12 月的文章是被引用最多的行业反思：从简单开始，只在复杂性值得其成本时才添加。

> **【中文解读】** Anthropic 在 2024 年 12 月发布的《Building Effective Agents》定义了四种工作流模式：(1) Prompt Chaining——串行步骤链；(2) Routing——条件分支；(3) Parallelization——并行扇出扇入；(4) Orchestrator-Workers——编排器分配子任务。这些模式是构建生产 Agent 系统的基础构建块。

> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准】** LangGraph 用状态图实现这些模式，OpenAI Agents SDK 用 Handoffs 实现路由和编排，CrewAI 用 Crews 实现并行化。关键洞察是：不是每个任务都需要 Agent——对于确定性的多步骤流程，工作流比自主 Agent 更可靠、更便宜。

## The Concept | 核心概念

### Workflows vs agents

- **Workflow.** LLMs and tools orchestrated through predefined code paths. Engineers own the graph.
  中文翻译：**工作流。** 通过预定义代码路径编排的 LLM 和工具。工程师拥有图。
- **Agent.** LLMs dynamically direct their own tools and take their own steps. The model owns the graph.
  中文翻译：**Agent。** LLM 动态指导自己的工具和步骤。模型拥有图。

Both have their place. Workflows are cheaper, faster, and easier to debug. Agents unlock open-ended problems but make failure modes harder to reason about.

> 两者都有其用武之地。工作流更便宜、更快、更容易调试。Agent 解锁开放式问题但使失败模式更难推理。

### The augmented LLM

Foundation for all five patterns: one LLM with three capabilities wired in — search (retrieval), tools (actions), memory (persistence). Any API call can use these.

> 所有五种模式的基础：一个 LLM 配备三种能力——搜索（检索）、工具（行动）、记忆（持久化）。任何 API 调用都可以使用这些。

### The five patterns

1. **Prompt chaining.** Output of call 1 is input to call 2. Use when a task has a clean linear decomposition. Optional programmatic gates between steps.
   中文翻译：**提示链。** 调用 1 的输出是调用 2 的输入。当任务有清晰的线性分解时使用。步骤间可选编程门控。
2. **Routing.** A classifier LLM picks which downstream LLM or tool to invoke. Use when categorically different inputs need different handling (tier-1 support vs refund vs bug vs sales).
   中文翻译：**路由。** 分类器 LLM 选择调用哪个下游 LLM 或工具。当不同类别的输入需要不同处理时使用。
3. **Parallelization.** Run N LLM calls concurrently, aggregate results. Two shapes: sectioning (different chunks) and voting (same prompt, N runs, majority/synthesis).
   中文翻译：**并行化。** 并发运行 N 个 LLM 调用，聚合结果。两种形式：分段（不同块）和投票（相同提示，N 次运行，多数/综合）。
4. **Orchestrator-workers.** An orchestrator LLM dynamically decides which workers (also LLMs) to run and synthesizes their output. Similar to agent loops but the orchestrator does not loop indefinitely.
   中文翻译：**编排器-工作者。** 编排器 LLM 动态决定运行哪些工作者（也是 LLM）并综合其输出。类似于 Agent 循环但编排器不会无限循环。
5. **Evaluator-optimizer.** One LLM proposes an answer, another LLM evaluates it. Iterate until the evaluator passes. This is Self-Refine (Lesson 05) generalized.
   中文翻译：**评估器-优化器。** 一个 LLM 提出答案，另一个 LLM 评估它。迭代直到评估器通过。这是 Self-Refine（第 5 课）的泛化。

### Where workflows beat agents

> 工作流优于 Agent 的场景：

- **Predictable tasks.** If you can enumerate the steps, you should.
  中文翻译：**可预测任务。** 如果你能枚举步骤，你就应该枚举。
- **Cost-bound tasks.** Workflows have bounded step counts; agents can spiral.
  中文翻译：**成本受限任务。** 工作流有有限步数；Agent 可能失控。
- **Compliance-bound tasks.** Auditors want to read the graph, not infer it from trajectories.
  中文翻译：**合规受限任务。** 审计员想要阅读图，而不是从轨迹推断。

### Where agents beat workflows

> Agent 优于工作流的场景：

- **Open-ended research.** When the next step depends on what the last step returned.
  中文翻译：**开放式研究。** 当下一步取决于上一步返回了什么。
- **Variable-length tasks.** Minutes to hours of work where step count is unknown.
  中文翻译：**可变长度任务。** 几分钟到几小时的工作，步数未知。
- **Novel domains.** When you don't yet know the right workflow — exploration first, codify later.
  中文翻译：**新领域。** 当你还不知道正确的工作流时——先探索，后编纂。

### The context-engineering companion

"Effective context engineering for AI agents" (Anthropic 2025) formalizes the adjacent discipline: the 200k window is a budget, not a container. What to include, when to compact, when to let context grow. Covered in detail in Phase 14 lesson on context compression.

> "AI Agent 的有效上下文工程"（Anthropic 2025）形式化了相邻学科：200k 窗口是预算而非容器。包含什么、何时压缩、何时让上下文增长。

## Build It | 动手构建

`code/main.py` implements all five workflow patterns against a `ScriptedLLM`:

> `code/main.py` 针对 `ScriptedLLM` 实现了所有五种工作流模式：

- `prompt_chain(input, steps)` — sequential.
- `route(input, classifier, handlers)` — classification + dispatch.
- `parallel_vote(prompt, n, aggregator)` — N runs, aggregate.
- `orchestrator_workers(task, workers)` — orchestrator picks workers.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` — loop until pass.

Run it:

> 运行：

```
python3 code/main.py
```

Each pattern prints its trace. Total lines of code per pattern is ~10-15; the cost of a framework is measured in thousands.

> 每种模式打印其轨迹。每种模式的代码行数约 10-15 行；框架的成本以千行计。

## Use It | 用框架实现

- Direct API calls for most tasks.
  中文翻译：大多数任务使用直接 API 调用。
- Framework only when the pattern genuinely needs durable state (LangGraph), actor-model concurrency (AutoGen v0.4), or role templating (CrewAI).
  中文翻译：只在模式真正需要持久状态（LangGraph）、Actor 模型并发（AutoGen v0.4）或角色模板（CrewAI）时使用框架。
- Reach for the Claude Agent SDK when you want the Claude Code harness shape without rebuilding it.
  中文翻译：当你想要 Claude Code 框架形态而不重新构建时选择 Claude Agent SDK。

## Ship It | 产出物

`outputs/skill-workflow-picker.md` picks the right pattern for a given task description, including the decision rationale and the refactor path to an agent if workflows fall short.

> `outputs/skill-workflow-picker.md` 为给定任务描述选择正确的模式，包括决策理由和工作流不足时重构为 Agent 的路径。

## Exercises | 练习题

1. Implement routing with a confidence threshold. Below threshold -> escalate to human. Where does the threshold land for a tier-1 support use case?
   中文翻译：实现带置信度阈值的路由。低于阈值 -> 升级给人类。一级支持用例的阈值在哪里？
2. Add a timeout to `parallel_vote`. What happens when one call hangs? How do you aggregate with missing votes?
   中文翻译：为 `parallel_vote` 添加超时。当一个调用挂起时怎么办？如何聚合缺失的投票？
3. Turn `evaluator_optimizer` into a bandit: keep the top-2 outputs across iterations so a late good result doesn't get overwritten by a late bad one.
   中文翻译：将 `evaluator_optimizer` 变成 bandit：跨迭代保留 top-2 输出，避免后期好结果被后期坏结果覆盖。
4. Combine prompt chaining with routing: a router picks one of three chains. Measure token cost vs a single big-prompt alternative.
   中文翻译：组合提示链和路由：路由器选择三条链之一。对比单一大提示替代方案的 token 成本。
5. Pick one of your production features. Draw the workflow graph. Count steps. Would an agent actually be better here?
   中文翻译：选择一个你的生产功能。画出工作流图。计算步骤。Agent 真的更好吗？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Predefined flow" / "预定义流程" | Engineer-owned graph of LLM and tool calls / 工程师拥有的 LLM 和工具调用图 |
| Agent | "Autonomous AI" / "自主 AI" | Model-owned graph; dynamic tool direction / 模型拥有的图；动态工具指导 |
| Augmented LLM | "LLM with tools" / "带工具的 LLM" | LLM + search + tools + memory; the atomic unit / LLM + 搜索 + 工具 + 记忆；原子单元 |
| Prompt chaining | "Sequential calls" / "串行调用" | Output of call N is input to call N+1 / 调用 N 的输出是调用 N+1 的输入 |
| Routing | "Classifier dispatch" / "分类分派" | Pick which chain/model handles the input / 选择哪个链/模型处理输入 |
| Parallelization | "Fan out" / "扇出" | N concurrent calls; aggregate by sectioning or voting / N 个并发调用；按分段或投票聚合 |
| Orchestrator-workers | "Dispatcher agent" / "分派 Agent" | Orchestrator LLM picks specialist LLMs dynamically / 编排器 LLM 动态选择专家 LLM |
| Evaluator-optimizer | "Proposer + judge" / "提议者 + 评判者" | Iterate until evaluator passes; Self-Refine generalized / 迭代直到评估器通过；Self-Refine 的泛化 |

## Further Reading | 延伸阅读

- [Anthropic, Building Effective Agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) — the five workflow patterns
  中文翻译：Anthropic 关于构建有效 Agent 的文章——五种工作流模式。
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — the companion discipline
  中文翻译：Anthropic 关于 AI Agent 有效上下文工程的文章——伴随学科。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — when stateful graphs earn their cost
  中文翻译：LangGraph 概览——有状态图何时值得其成本。
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — the orchestrator-workers pattern, productized
  中文翻译：OpenAI Agents SDK——编排器-工作者模式的产品化。
