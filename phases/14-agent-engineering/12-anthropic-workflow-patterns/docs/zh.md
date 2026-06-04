# Anthropic 工作流 模式

> Schluntz and Zhang (Anthropic, Dec 2024) distinguish workflows (predefined paths) from agents (dynamic tool-use). Five workflow patterns cover most cases. Start with direct API calls. Add agents only when steps cannot be predicted.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 01 (Agent Loop)
**预计时间：** ~60 minutes

## 学习目标

- Name Anthropic's five workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- Explain the agent-vs-workflow distinction and the engineering cost of each.
- Identify when to pick a workflow over an agent (and vice versa).
- Implement all five patterns in stdlib against a scripted LLM.

## 问题引入

> **【中文解读】** Anthropic 在 2024 年 12 月发布的《Building Effective Agents》定义了四种工作流模式：(1) Prompt Chaining——串行步骤链；(2) Routing——条件分支；(3) Parallelization——并行扇出扇入；(4) Orchestrator-Workers——编排器分配子任务。这些模式是构建生产 Agent 系统的基础构建块。
> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准。LangGraph 用状态图...】** Anthropic 的工作流模式分类已成为 Agent 工程的事实标准。LangGraph 用状态图实现这些模式，OpenAI Agents SDK 用 Handoffs 实现路由和编排，CrewAI 用 Crews 实现并行化。关键洞察是：不是每个任务都需要 Agent——对于确定性的多步骤流程，工作流比自主 Agent 更可靠、更便宜。

## 核心概念

### Workflows vs agents
- **Workflow.** LLMs and tools orchestrated through predefined code paths. Engineers own the graph.
- **Agent.** LLMs dynamically direct their own tools and take their own steps. The model owns the graph.
Both have their place. Workflows are cheaper, faster, and easier to debug. Agents unlock open-ended problems but make failure modes harder to reason about.
### The augmented LLM
Foundation for all five patterns: one LLM with three capabilities wired in — search (retrieval), tools (actions), memory (persistence). Any API call can use these.
### The five patterns
1. **Prompt chaining.** Output of call 1 is input to call 2. Use when a task has a clean linear decomposition. Optional programmatic gates between steps.
2. **Routing.** A classifier LLM picks which downstream LLM or tool to invoke. Use when categorically different inputs need different handling (tier-1 support vs refund vs bug vs sales).
3. **Parallelization.** Run N LLM calls concurrently, aggregate results. Two shapes: sectioning (different chunks) and voting (same prompt, N runs, majority/synthesis).
4. **Orchestrator-workers.** An orchestrator LLM dynamically decides which workers (also LLMs) to run and synthesizes their output. Similar to agent loops but the orchestrator does not loop indefinitely.
5. **Evaluator-optimizer.** One LLM proposes an answer, another LLM evaluates it. Iterate until the evaluator passes. This is Self-Refine (Lesson 05) generalized.
### Where workflows beat agents
- **Predictable tasks.** If you can enumerate the steps, you should.
- **Cost-bound tasks.** Workflows have bounded step counts; agents can spiral.
- **Compliance-bound tasks.** Auditors want to read the graph, not infer it from trajectories.
### Where agents beat workflows
- **Open-ended research.** When the next step depends on what the last step returned.
- **Variable-length tasks.** Minutes to hours of work where step count is unknown.
- **Novel domains.** When you don't yet know the right workflow — exploration first, codify later.
### The context-engineering companion
"Effective context engineering for AI agents" (Anthropic 2025) formalizes the adjacent discipline: the 200k window is a budget, not a container. What to include, when to compact, when to let context grow. Covered in detail in Phase 14 lesson on context compression (Phase 14 earlier lesson 06 in this curriculum before the renumber).

## 动手实现

`code/main.py` implements all five workflow patterns against a `ScriptedLLM`:
- `prompt_chain(input, steps)` — sequential.
- `route(input, classifier, handlers)` — classification + dispatch.
- `parallel_vote(prompt, n, aggregator)` — N runs, aggregate.
- `orchestrator_workers(task, workers)` — orchestrator picks workers.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` — loop until pass.
Run it:
```
python3 code/main.py
```
Each pattern prints its trace. Total lines of code per pattern is ~10-15; the cost of a framework is measured in thousands.

## 用框架实现

- Direct API calls for most tasks.
- Framework only when the pattern genuinely needs durable state (LangGraph), actor-model concurrency (AutoGen v0.4), or role templating (CrewAI).
- Reach for the Claude Agent SDK when you want the Claude Code harness shape without rebuilding it.

## 产出物

`outputs/skill-workflow-picker.md` picks the right pattern for a given task description, including the decision rationale and the refactor path to an agent if workflows fall short.

## 练习题

1. Implement routing with a confidence threshold. Below threshold -> escalate to human. Where does the threshold land for a tier-1 support use case?
   *思考并实践此练习*
2. Add a timeout to `parallel_vote`. What happens when one call hangs? How do you aggregate with missing votes?
   *思考并实践此练习*
3. Turn `evaluator_optimizer` into a bandit: keep the top-2 outputs across iterations so a late good result doesn't get overwritten by a late bad one.
   *思考并实践此练习*
4. Combine prompt chaining with routing: a router picks one of three chains. Measure token cost vs a single big-prompt alternative.
   *思考并实践此练习*
5. Pick one of your production features. Draw the workflow graph. Count steps. Would an agent actually be better here?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Workflow | "Predefined flow" |
| Agent | "Autonomous AI" |
| Augmented LLM | "LLM with tools" |
| Prompt chaining | "Sequential calls" |
| Routing | "Classifier dispatch" |
| Parallelization | "Fan out" |
| Orchestrator-workers | "Dispatcher agent" |
| Evaluator-optimizer | "Proposer + judge" |

## 延伸阅读

