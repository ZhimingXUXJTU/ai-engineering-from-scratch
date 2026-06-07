# The Multi-Agent Primitive Model | 多 Agent 原始

> Every multi-agent framework shipping in 2026 — AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework — is a point in a four-dimensional design space. Four primitives, nothing more: the agent, the handoff, the shared state, the orchestrator. This lesson builds them from zero, runs a toy system on all four, then maps every major framework onto the same axes so you can read any new release in one paragraph.

> **【中文解读】** 本节介绍了原始模型——多 Agent 系统的最基本构建单元和交互原语。

> **【拓展：primitive model→具体应用】** 多 Agent 系统的最小原语模型定义了 Agent 之间的基本交互模式：(1) 消息传递——Agent 通过发送消息通信；(2) 共享状态——Agent 通过读写共享存储协调；(3) 事件通知——Agent 订阅感兴趣的事件。AutoGen 用消息传递，LangGraph 用共享状态，黑板系统用事件通知。大多数实际系统混合使用多种原语。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Problem | 问题引入

Every six months a new multi-agent framework ships. AutoGen in 2023. CrewAI in 2024. LangGraph and OpenAI Swarm in 2024. Google ADK in April 2025. Microsoft Agent Framework RC in February 2026. Each press release claims to be "the right abstraction."

> 每六个月就会有一个新的多 Agent 框架发布。2023 年的 AutoGen。2024 年的 CrewAI。2024 年的 LangGraph 和 OpenAI Swarm。2025 年 4 月的 Google ADK。2026 年 2 月的 Microsoft Agent Framework RC。每个新闻稿都声称自己是"正确的抽象"。

If you try to learn them one at a time you will burn out. The APIs look different. The docs disagree about what an "agent" is. One framework calls its shared memory a "blackboard," another calls it a "message pool," a third calls it a "StateGraph." You start suspecting the field is just churning.

> 如果你尝试一个一个地学习它们，你会筋疲力尽。API 看起来不同。文档对"Agent"是什么有不同看法。一个框架将其共享内存称为"黑板"，另一个称为"消息池"，第三个称为"StateGraph"。你开始怀疑这个领域只是在反复炒作。

It is not. Underneath the marketing, the four primitives are stable. Learn them once, read every new framework in one paragraph.

> 事实并非如此。在营销之下，四个原语是稳定的。学一次，就能用一个段落理解每个新框架。

## Concept | 核心概念

### The four primitives

1. **Agent** — a system prompt plus a tool list. Stateless; every run starts from its system prompt and the current message history.
   中文翻译：**Agent** — 一个系统提示加上一个工具列表。无状态；每次运行从其系统提示和当前消息历史开始。
2. **Handoff** — a structured transfer of control from one agent to another. Mechanically, a tool call that returns a new agent or a graph edge that follows a condition.
   中文翻译：**交接** — 从一个 Agent 到另一个 Agent 的结构化控制转移。机械地，一个返回新 Agent 的工具调用或遵循条件的图边。
3. **Shared state** — any data structure that more than one agent can read (sometimes write). Message pool, blackboard, key-value store, vector memory.
   中文翻译：**共享状态** — 多个 Agent 可以读取（有时写入）的任何数据结构。消息池、黑板、键值存储、向量内存。
4. **Orchestrator** — whoever decides who speaks next. Options: an explicit graph (deterministic), an LLM speaker-selector (soft), the last speaker's handoff call (OpenAI Swarm), or a scheduler over a queue (swarm architecture).
   中文翻译：**编排器** — 决定谁下一个发言的角色。选项：显式图（确定性）、LLM 发言选择器（软性）、上一个发言者的交接调用（OpenAI Swarm）或队列上的调度器（群体架构）。

That is the entire design space. Every framework picks defaults for each axis; the rest is surface syntax.

> 这就是整个设计空间。每个框架为每个轴选择默认值；其余的是表面语法。

### How every 2026 framework maps to it

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

> | 框架 | Agent | 交接 | 共享状态 | 编排器 |
> |------|-------|------|----------|--------|
> | OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | 工具返回 Agent | 调用者的问题 | LLM 的下一个交接调用 |
> | AutoGen v0.4 / AG2 | `ConversableAgent` | GroupChat 上的发言选择器 | 消息池 | 选择器函数（LLM 或轮询） |
> | CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | 任务输出链式 | 经理 LLM 或静态顺序 |
> | LangGraph | 节点函数 | 图边 + 条件 | `StateGraph` 归约器 | 图，确定性 |
> | Microsoft Agent Framework | agent + 编排模式 | 模式特定 | 线程 / 上下文 | 模式特定 |
> | Google ADK | agent + A2A 卡片 | A2A 任务 | A2A 工件 | 主机决定 |

Surface differences look huge. Underneath: same four knobs.

> 表面差异看起来很大。底层：相同的四个旋钮。

### Why this matters

Once you see the primitives, framework comparison becomes a short checklist:

> 一旦你看到了原语，框架比较就变成了一个简短的检查清单：

- Does the orchestrator trust the LLM to route (Swarm) or does it pin routing in code (LangGraph)?
  中文翻译：编排器是信任 LLM 来路由（Swarm）还是在代码中固定路由（LangGraph）？
- Is shared state full-history (GroupChat) or projected (StateGraph reducer)?
  中文翻译：共享状态是完整历史（GroupChat）还是投影的（StateGraph 归约器）？
- Can agents modify each other's prompts (CrewAI manager) or only hand off (Swarm)?
  中文翻译：Agent 能否修改彼此的提示（CrewAI 经理）还是只能交接（Swarm）？

Those three questions answer 80% of which framework fits a given problem. You stop shopping for "the best multi-agent framework" and start designing for the axis you actually care about.

> 这三个问题回答了 80% 的哪个框架适合给定问题。你不再购买"最好的多 Agent 框架"，而是开始为你真正关心的轴设计。

### The stateless insight

Every primitive except shared state is stateless. Agent is a function of (prompt, tools). Handoff is a function call. Orchestrator is a scheduler. **The only stateful thing in the system is shared state.** That is where all the interesting bugs live: memory poisoning (Lesson 15), message ordering, versioning, write contention.

> 除共享状态外，每个原语都是无状态的。Agent 是 (prompt, tools) 的函数。交接是函数调用。编排器是调度器。**系统中唯一有状态的东西是共享状态。** 这就是所有有趣的 bug 所在的地方：内存污染（Lesson 15）、消息排序、版本控制、写冲突。

Frameworks that hide shared state (Swarm) push the problem to the caller. Frameworks that centralize it (LangGraph checkpoint, AutoGen pool) make it inspectable but shift coordination cost onto the shared-state implementation.

> 隐藏共享状态的框架（Swarm）将问题推给调用者。集中化它的框架（LangGraph 检查点、AutoGen 池）使其可检查但将协调成本转移到共享状态实现上。

### Anatomy of a single primitive

#### Agent

```
Agent = (system_prompt, tools, model, optional_name)
```

No memory. No state. Two agents with the same system prompt and tools are interchangeable. Everything that looks like per-agent state is actually in shared state or the handoff protocol.

> 没有记忆。没有状态。具有相同系统提示和工具的两个 Agent 是可互换的。看起来像每个 Agent 状态的一切实际上都在共享状态或交接协议中。

#### Handoff

```
Handoff = (from_agent, to_agent, reason, payload)
```

Three implementations dominate:

> 三种实现占主导地位：

- **Function return** — the tool returns the next agent. This is the OpenAI Swarm pattern. Agents carry routing in their tool schemas.
  中文翻译：**函数返回** — 工具返回下一个 Agent。这是 OpenAI Swarm 的模式。Agent 在其工具模式中携带路由。
- **Graph edge** — LangGraph. Edges are declarative. The LLM produces a value; a condition selects the next node.
  中文翻译：**图边** — LangGraph。边是声明式的。LLM 产生一个值；条件选择下一个节点。
- **Speaker selection** — AutoGen GroupChat. A selector function (sometimes itself an LLM call) reads the pool and picks who speaks next.
  中文翻译：**发言者选择** — AutoGen GroupChat。选择器函数（有时本身是 LLM 调用）读取池并选择下一个发言者。

#### Shared state

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

At minimum, a list of messages. Often more: structured artifacts (CrewAI Task outputs), typed context (LangGraph reducers), external memory (MCP, vector DB).

> 至少是一个消息列表。通常更多：结构化工件（CrewAI Task 输出）、类型化上下文（LangGraph 归约器）、外部内存（MCP、向量 DB）。

Two topologies: **full pool** (every agent sees every message) and **projected** (agents see a role-scoped view). Full pools are simple and scale badly. Projected pools scale but require upfront schema design.

> 两种拓扑：**完整池**（每个 Agent 看到每条消息）和**投影**（Agent 看到角色范围的视图）。完整池简单但扩展性差。投影池可扩展但需要前期模式设计。

#### Orchestrator

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Four flavors:

> 四种风格：

- **Static** — the graph is fixed at build time (LangGraph deterministic, CrewAI Sequential).
  中文翻译：**静态** — 图在构建时固定（LangGraph 确定性、CrewAI Sequential）。
- **LLM-selected** — an LLM reads the pool and picks the next speaker (AutoGen, CrewAI Hierarchical).
  中文翻译：**LLM 选择** — LLM 读取池并选择下一个发言者（AutoGen、CrewAI Hierarchical）。
- **Handoff-driven** — the current agent decides by calling a handoff tool (Swarm).
  中文翻译：**交接驱动** — 当前 Agent 通过调用交接工具决定（Swarm）。
- **Queue-driven** — workers pull from a shared queue; no explicit next-speaker (swarm architectures, Matrix).
  中文翻译：**队列驱动** — 工作器从共享队列拉取；没有明确的下一个发言者（群体架构、Matrix）。

### What changes between frameworks

Once the primitives are fixed, the remaining design decisions are:

> 一旦原语固定，剩余的设计决策是：

- **Memory strategy** — ephemeral vs durable checkpointing (LangGraph checkpointer).
  中文翻译：**内存策略** — 临时 vs 持久检查点（LangGraph checkpointer）。
- **Safety boundary** — who can approve a handoff (human-in-the-loop).
  中文翻译：**安全边界** — 谁可以批准交接（人在循环中）。
- **Cost accounting** — per-agent token budgets.
  中文翻译：**成本核算** — 每个 Agent 的 token 预算。
- **Observability** — tracing handoffs, persisting state for replay.
  中文翻译：**可观测性** — 跟踪交接、持久化状态以便回放。

All implementable on top of the primitives. None of them are new primitives.

> 所有都可以在原语之上实现。它们中没有新的原语。

## Build It | 动手实现

`code/main.py` implements the four primitives in ~150 lines of stdlib Python. No real LLM — each agent is a scripted policy so the focus stays on the coordination structure.

> `code/main.py` 用约 150 行标准库 Python 实现了四个原语。没有真正的 LLM — 每个 Agent 是一个脚本化策略，使焦点保持在协调结构上。

The file exports:

> 文件导出：

- `Agent` — a dataclass of name, system prompt, tools, policy function.
  中文翻译：`Agent` — 名称、系统提示、工具、策略函数的数据类。
- `Handoff` — a function that returns a new agent.
  中文翻译：`Handoff` — 返回新 Agent 的函数。
- `SharedState` — a thread-safe message pool.
  中文翻译：`SharedState` — 线程安全的消息池。
- `Orchestrator` — three variants: `StaticOrchestrator`, `HandoffOrchestrator`, `LLMSelectorOrchestrator` (simulated).
  中文翻译：`Orchestrator` — 三种变体：`StaticOrchestrator`、`HandoffOrchestrator`、`LLMSelectorOrchestrator`（模拟）。

The demo runs the same three-agent pipeline (research -> write -> review) through all three orchestrator types and prints the message pool at the end. You can see that the outputs differ only in *who picks next*; the agents and shared state are identical across runs.

> 演示通过所有三种编排器类型运行相同的三 Agent 流水线（研究 -> 编写 -> 审阅），并在最后打印消息池。你可以看到输出仅在*谁选择下一个*上不同；Agent 和共享状态在所有运行中是相同的。

Run it:

```
python3 code/main.py
```

Expected output: three orchestrator runs, one per pattern. Each prints the final message pool. The handoff-driven run reaches fewer agents if the researcher decides it is done early — that is the LLM-routing tradeoff in miniature.

> 预期输出：三次编排器运行，每种模式一次。每次打印最终消息池。如果研究员决定提前完成，交接驱动的运行会触及更少的 Agent — 这就是 LLM 路由权衡的缩影。

## Use It | 用框架实现

`outputs/skill-primitive-mapper.md` is a skill that reads any multi-agent codebase or framework doc and returns the four-primitive mapping. Run it on a new framework release to get a one-paragraph understanding before reading docs in depth.

> `outputs/skill-primitive-mapper.md` 是一个技能，读取任何多 Agent 代码库或框架文档并返回四原语映射。在新框架发布时运行它，在深入阅读文档之前获得一段式的理解。

## Ship It | 产出物

Before adopting a new framework, write the primitive mapping for it. If you cannot, the docs are incomplete or the framework is inventing a fifth primitive (rare — check for a shared-state flavor you have not seen).

> 在采用新框架之前，为其编写原语映射。如果你做不到，说明文档不完整或框架正在发明第五个原语（罕见——检查你未见过的共享状态变体）。

Pin the mapping in your architecture doc. When a new team member joins, send them the mapping before the API docs. When framework versions change, diff the mapping, not the changelog.

> 将映射固定在架构文档中。当新团队成员加入时，在 API 文档之前发送映射。当框架版本变化时，对比映射，而不是变更日志。

## Exercises | 练习题

1. Run `code/main.py` three times with different agent policies. Observe how the orchestrator choice changes which agents run.
   中文翻译：用不同的 Agent 策略运行 `code/main.py` 三次。观察编排器选择如何改变哪些 Agent 运行。
2. Implement a fourth orchestrator type: a queue-driven one where agents poll shared state for work. What deadlock can happen, and how do you detect it?
   中文翻译：实现第四种编排器类型：队列驱动的，Agent 轮询共享状态获取工作。可能发生什么死锁，你如何检测？
3. Take the LangGraph quickstart and rewrite it as the four primitives. Which of LangGraph's abstractions map 1:1 and which are convenience wrappers?
   中文翻译：将 LangGraph 快速入门改写为四个原语。LangGraph 的哪些抽象是 1:1 映射，哪些是便利包装器？
4. Read the OpenAI Swarm cookbook. Identify which of the four primitives Swarm makes most ergonomic, and which one it pushes to the caller.
   中文翻译：阅读 OpenAI Swarm 手册。识别四个原语中 Swarm 使哪个最符合人体工程学，哪个推给调用者。
5. Find one framework in this table that hides shared state entirely. Explain what breaks when agents need to coordinate across handoffs without re-reading history.
   中文翻译：在表中找到一个完全隐藏共享状态的框架。解释当 Agent 需要在不重新读取历史的情况下跨交接协调时会出现什么问题。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Further Reading | 延伸阅读

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) — the clearest articulation of handoff-driven orchestration
  中文翻译：OpenAI 手册：编排 Agent — 例程和交接 — 交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) — GroupChat + speaker selection is the reference for LLM-selected orchestration
  中文翻译：AutoGen 稳定文档 — GroupChat + 发言者选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — graph-edge orchestration and reducer-based shared state
  中文翻译：LangGraph 工作流和 Agent — 图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction) — role-goal-backstory agents, Sequential / Hierarchical processes
  中文翻译：CrewAI 介绍 — 角色-目标-背景故事 Agent，Sequential / Hierarchical 流程
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) — the live AutoGen v0.2 line after Microsoft moved v0.4 into maintenance
  中文翻译：AG2（社区 AutoGen 延续）— 微软将 v0.4 移入维护后的活跃 AutoGen v0.2 线
