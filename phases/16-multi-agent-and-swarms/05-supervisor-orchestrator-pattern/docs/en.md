# Supervisor / Orchestrator-Worker Pattern | 主管/编排器-工作器模式

> One lead agent plans and delegates; specialized workers execute in parallel contexts and report back. This is the pattern behind Anthropic's Research system (Claude Opus 4 as lead, Sonnet 4 as subagents), measured at +90.2% over single-agent Opus 4 on internal research evals. Anthropic's engineering post reports that 80% of the variance on BrowseComp is explained by token usage alone — multi-agent wins largely because each subagent gets a fresh context window. This lesson builds the supervisor pattern from the primitives and covers the 2026 engineering lessons from production deployments.

> **【中文解读】** 一个主管 Agent 规划并委派任务；专业化工作器在并行上下文中执行并汇报。这是 Anthropic Research 系统背后的模式（Claude Opus 4.6 主管，Sonnet 4.5 子 Agent），在内部研究评估上比单 Agent Opus 4.6 提升 90.2%。核心洞察：多 Agent 胜出主要因为每个子 Agent 获得独立的上下文窗口——80% 的 BrowseComp 方差仅由 Token 使用量解释。

> **【拓展：Supervisor 模式 → Claude DevFleet】** Claude Code 的多 Agent 编排工具 Claude DevFleet 就是 Supervisor 模式的实现——一个主 Agent 分解任务，派发到多个隔离的 worktree 中的子 Agent 并行工作，最后汇总结果。Anthropic 的生产 Research 系统也使用此模式。

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Research is the prototypical task that single-agent systems fail. You ask "what changed in multi-agent systems between 2023 and 2026?" A single agent reads five papers sequentially, fills half its context with their text, and then has to reason about all of them together. It forgets the first paper by the time it reaches the fifth. It cannot parallelize.

> 研究是单 Agent 系统失败的典型任务。你问"2023 到 2026 年间多 Agent 系统发生了什么变化？"单个 Agent 顺序阅读五篇论文，用它们的文本填满一半上下文，然后必须对它们一起推理。到它读到第五篇时已经忘了第一篇。它无法并行化。

The single-agent failure is structural, not fixable with better prompts. No matter how good the system prompt is, the context window fills up. The information needed for synthesis (all five papers' key findings) physically does not fit alongside the raw text of the papers.

> 单 Agent 失败是结构性的，无法用更好的提示修复。无论系统提示多好，上下文窗口都会填满。综合所需的信息（所有五篇论文的关键发现）物理上无法与论文原始文本并存。

The supervisor pattern fixes this: one lead agent plans the search, delegates each sub-question to a worker, and synthesizes. Each worker gets its own 200k-token window for a narrow question. The lead never sees the raw papers — only the worker summaries.

> 监督者模式修复了这个问题：一个主导 Agent 规划搜索，将每个子问题委派给一个工作器，然后综合。每个工作器获得自己的 200k token 窗口用于一个狭窄的问题。主导者永远不看到原始论文——只看到工作器摘要。

The information flow is the design: raw data stays in worker contexts; only compressed findings reach the lead. The lead's context is dedicated to synthesis, not data loading. This is the architectural win — separation of data-heavy work from synthesis-heavy work.

> 信息流是设计：原始数据留在工作器上下文中；只有压缩的发现到达主导者。主导者的上下文专注于综合，而不是数据加载。这是架构胜利——数据密集工作与综合密集工作的分离。

Anthropic's production Research system reports +90.2% on internal research evals vs a single Opus 4. The same post notes that 80% of the BrowseComp variance is explained by *token usage alone*. Fresh context per subagent is the main mechanism.

> Anthropic 的生产研究系统报告在内部研究评估上比单个 Opus 4 提升 +90.2%。同一篇文章指出 BrowseComp 方差的 80% 仅由 *token 使用量* 解释。每个子 Agent 的清新上下文是主要机制。

The 80% number is the headline finding: model choice, prompt engineering, and tooling together explain only 20% of the variance. If you want better research-agent performance, spend more tokens (more subagents, larger contexts) before tweaking prompts. Cost, not cleverness, is the lever.

> 80% 这个数字是标题发现：模型选择、提示工程和工具加起来只解释 20% 的方差。如果你想要更好的研究 Agent 性能，在调整提示之前花更多 token（更多子 Agent、更大上下文）。成本，不是聪明，是杠杆。

## Concept | 核心概念

### The pattern

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

The lead never reads the raw materials. The workers never see each other's work until the lead synthesizes. Each arrow is a handoff with a narrow artifact.

> 主导者永远不读取原始材料。工作器在主导者综合之前永远不看到彼此的工作。每个箭头是一个带有狭窄工件的交接。

This information isolation is the core design choice. The lead's context window stays focused on planning and synthesis — never polluted by 200k tokens of raw search results. Workers each get a clean 200k budget for their narrow question.

> 这种信息隔离是核心设计选择。主导者的上下文窗口保持专注于规划和综合——永远不被 200k token 的原始搜索结果污染。工作器每个都获得针对其狭窄问题的干净 200k 预算。

### Why it wins

Three mechanisms:

> 三个机制：

1. **Fresh context per subagent.** A worker exploring "FIPA-ACL heritage" does not carry the 40k tokens the lead spent planning. It gets a 200k window for one question.
   中文翻译：**每个子 Agent 的清新上下文。** 探索"FIPA-ACL 遗产"的工作器不携带主导者用于规划的 40k token。它获得一个用于一个问题的 200k 窗口。
2. **Specialization via prompt.** The lead's prompt is "decompose and synthesize," not "research." Each worker's prompt is narrow: "find what changed in X." Focused prompts produce focused outputs.
   中文翻译：**通过提示专业化。** 主导者的提示是"分解和综合"，而不是"研究"。每个工作器的提示是狭窄的："找出 X 发生了什么变化。"聚焦的提示产生聚焦的输出。
3. **Parallelism.** Workers run concurrently. Wall-clock time is roughly `max(worker_times) + plan + synthesis`, not `sum(worker_times)`.
   中文翻译：**并行性。** 工作器并发运行。挂钟时间大约是 `max(worker_times) + plan + synthesis`，而不是 `sum(worker_times)`。

### Engineering lessons (Anthropic 2025)

The Anthropic post lists several production lessons that are still 2026-relevant:

> Anthropic 的文章列出了几条仍然适用于 2026 年的生产经验：

- **Scale effort to query complexity.** Simple queries: one agent, 3-10 tool calls. Complex queries: 10+ agents. The lead must estimate this, not the caller.
  中文翻译：**按查询复杂度缩放工作量。** 简单查询：一个 Agent，3-10 次工具调用。复杂查询：10+ 个 Agent。主导者必须估计这一点，而不是调用者。
- **Broad then narrow.** Decompose into broad sub-questions first, then spawn more workers per sub-question if the answer warrants depth.
  中文翻译：**先宽后窄。** 先分解为广泛的子问题，如果答案需要深度，则为每个子问题生成更多工作器。
- **Rainbow deployments.** Agents are long-running and stateful. Traditional blue-green does not work. Anthropic uses rainbow: gradual rollout of new versions while old ones drain.
  中文翻译：**彩虹部署。** Agent 是长时间运行且有状态的。传统的蓝绿部署不起作用。Anthropic 使用彩虹：新版本的渐进推出，同时旧版本排空。
- **Token usage dominates.** Multi-agent is ~15x the tokens of single-agent. Only run it when the task value justifies the cost.
  中文翻译：**Token 使用量占主导。** 多 Agent 是单 Agent 的约 15 倍 token。只在任务价值证明成本合理时运行它。

### The LangGraph turn

LangGraph originally shipped a `langgraph-supervisor` library with a high-level `create_supervisor` helper. In 2025 LangChain moved the recommendation to implementing the supervisor pattern via tool-calling directly, because tool calls give more control over *what the supervisor sees* (context engineering). The library still works; the docs now recommend the tool-calling form.

> LangGraph 最初发布了一个带有高级 `create_supervisor` 助手的 `langgraph-supervisor` 库。2025 年 LangChain 将建议改为通过工具调用直接实现监督者模式，因为工具调用对*监督者看到什么*（上下文工程）提供更多控制。库仍然有效；文档现在推荐工具调用形式。

The shift reflects a 2025-2026 insight: context engineering matters more than orchestration engineering. What the supervisor sees determines what it can plan. Passing raw worker context kills the lead's planning ability; passing narrow summaries preserves it.

> 这种转变反映了 2025-2026 年的洞察：上下文工程比编排工程更重要。监督者看到什么决定了它能规划什么。传递原始工作器上下文杀死主导者的规划能力；传递狭窄摘要保留它。

### The failure modes

- **Lead hallucinates the plan.** If the lead generates sub-questions that do not decompose the real question, workers do precise research on the wrong target.
  中文翻译：**主导者幻觉计划。** 如果主导者生成的子问题没有分解真正的问题，工作器会在错误的目标上做精确研究。
- **Workers over-explore.** Without explicit scope boundaries, workers drift beyond their assigned sub-question and pollute the synthesis step.
  中文翻译：**工作器过度探索。** 没有明确的范围边界，工作器会漂移超出其分配的子问题并污染综合步骤。
- **Synthesis conflicts.** Two workers return contradictory facts. The lead must either re-ask (add a round) or note the disagreement explicitly. Silent picking of one side is the worst failure: the user never knows disagreement happened.
  中文翻译：**综合冲突。** 两个工作器返回矛盾的事实。主导者必须重新询问（增加一轮）或明确记录分歧。静默选择一方是最糟糕的失败：用户永远不知道发生了分歧。

### When supervisor is wrong

- **Sequential tasks.** If step 2 literally needs step 1's output, parallelism buys nothing. Use a pipeline (CrewAI Sequential, LangGraph linear graph).
  中文翻译：**顺序任务。** 如果步骤 2 确实需要步骤 1 的输出，并行性没有帮助。使用流水线（CrewAI Sequential、LangGraph 线性图）。
- **Simple queries.** Single-agent handles them faster and cheaper. Use the lead's "scale effort" check before spawning workers.
  中文翻译：**简单查询。** 单 Agent 更快更便宜地处理它们。在生成工作器之前使用主导者的"缩放工作量"检查。
- **Strict determinism.** Supervisor uses LLM-selected delegation. Static graphs are better when audit/replay matter more than adaptability.
  中文翻译：**严格确定性。** 监督者使用 LLM 选择的委派。当审计/回放比适应性更重要时，静态图更好。

## Build It | 动手实现

`code/main.py` implements a supervisor of three parallel workers using `threading`. The lead decomposes a query into sub-questions, workers run concurrently on each sub-question, and the lead synthesizes. No real LLMs — the workers are scripted to simulate fetch-and-summarize.

> `code/main.py` 使用 `threading` 实现了一个三个并行工作器的监督者。主导者将查询分解为子问题，工作器在每个子问题上并发运行，主导者综合。没有真正的 LLM — 工作器被脚本化以模拟获取和总结。

Key structure:

> 关键结构：

- `Lead.plan(query)` splits a query into 3 sub-questions.
  中文翻译：`Lead.plan(query)` 将查询拆分为 3 个子问题。
- `Worker.run(sub_q)` returns a fake summary (could be any tool-using agent in production).
  中文翻译：`Worker.run(sub_q)` 返回一个假摘要（在生产中可以是任何使用工具的 Agent）。
- `Lead.run(query)` kicks off workers in threads, joins, and synthesizes.
  中文翻译：`Lead.run(query)` 在线程中启动工作器，等待，然后综合。

Run:

```
python3 code/main.py
```

Output shows the plan, the parallel worker traces with start/end timestamps, and the final synthesis. You can see the wall-clock wins: three 0.3-second workers run in ~0.35 seconds, not 0.9.

> 输出显示计划、带有开始/结束时间戳的并行工作器跟踪和最终综合。你可以看到挂钟时间优势：三个 0.3 秒的工作器在约 0.35 秒内运行，而不是 0.9 秒。

## Use It | 用框架实现

`outputs/skill-supervisor-designer.md` takes a user query and produces a supervisor-pattern design: lead system prompt, worker roles, sub-question decomposition rules, and the synthesis template. Use this before building a new research-style agent system.

> `outputs/skill-supervisor-designer.md` 接收用户查询并生成监督者模式设计：主导系统提示、工作器角色、子问题分解规则和综合模板。在构建新的研究风格 Agent 系统之前使用。

## Ship It | 产出物

Checklist before deploying a supervisor pattern:

> 部署监督者模式之前的检查清单：

- **Model pairing.** Lead on a reasoning-tier model (Opus class, `o3` class). Workers on a faster, cheaper model (Sonnet, `o4-mini`).
  中文翻译：**模型配对。** 主导者使用推理级模型（Opus 类、`o3` 类）。工作器使用更快、更便宜的模型（Sonnet、`o4-mini`）。
- **Worker timeout.** Any worker that exceeds 2x median runtime gets killed; the lead either re-spawns with narrower scope or proceeds without it.
  中文翻译：**工作器超时。** 超过 2 倍中位运行时间的任何工作器被终止；主导者要么以更窄的范围重新生成，要么不使用它继续。
- **Token cap per worker.** Hard limit (say 10x the expected synthesis input) prevents a runaway worker from blowing the budget.
  中文翻译：**每个工作器的 Token 上限。** 硬限制（比如预期综合输入的 10 倍）防止失控工作器耗尽预算。
- **Observability.** Trace the lead's plan, each worker's tool calls, and the synthesis. This is the basis for any post-hoc debugging.
  中文翻译：**可观测性。** 跟踪主导者的计划、每个工作器的工具调用和综合。这是任何事后调试的基础。
- **Rainbow rollout.** Stateful long-running agents need gradual version transition, not hot swap.
  中文翻译：**彩虹推出。** 有状态的长时间运行 Agent 需要渐进版本过渡，而不是热交换。

## Exercises | 练习题

1. Run `code/main.py`, then modify the lead to spawn 5 workers instead of 3. Observe the wall-clock effect. At what worker count does spawn overhead exceed parallel savings in this demo?
   中文翻译：运行 `code/main.py`，然后修改主导者以生成 5 个而不是 3 个工作器。观察挂钟时间效应。在这个演示中，工作器数量达到多少时生成开销超过并行节省？
2. Implement a worker timeout: kill any worker that runs longer than 0.5 seconds and have the lead synthesize the remaining results. What observability do you need to know a worker was cut?
   中文翻译：实现工作器超时：终止任何运行超过 0.5 秒的工作器，让主导者综合剩余结果。你需要什么可观测性来知道工作器被截断？
3. Add a conflict-detection step to the lead's synthesis: if two workers return contradictory answers, the lead notes the disagreement rather than picking one. How do you detect contradiction without calling an LLM?
   中文翻译：在主导者的综合中添加冲突检测步骤：如果两个工作器返回矛盾的答案，主导者记录分歧而不是选择其中一个。你如何在不调用 LLM 的情况下检测矛盾？
4. Read Anthropic's Research-system engineering post. List three practices that this toy demo would need to adopt to run in production.
   中文翻译：阅读 Anthropic 的研究系统工程文章。列出这个玩具演示需要在生产中采用的三种做法。
5. Compare LangGraph's `create_supervisor` (legacy) vs the new tool-calling recommendation. Which gives you better control over what the supervisor sees? Why does Anthropic explicitly pass only sub-answers and not raw worker context into synthesis?
   中文翻译：比较 LangGraph 的 `create_supervisor`（旧版）与新的工具调用建议。哪个让你更好地控制监督者看到什么？为什么 Anthropic 明确只传递子答案而不是原始工作器上下文到综合中？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Further Reading | 延伸阅读

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — the production reference for supervisor pattern
  中文翻译：Anthropic 工程 — 我们如何构建多 Agent 研究系统 — 监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — tool-calling supervisor is now the recommended form
  中文翻译：LangGraph 工作流和 Agent — 工具调用监督者现在是推荐的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) — the legacy helper, still used in 2026 production
  中文翻译：LangGraph 监督者参考 — 旧版助手，仍用于 2026 年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) — handoff-based supervisor variant
  中文翻译：OpenAI 手册 — 编排 Agent：例程和交接 — 基于交接的监督者变体
