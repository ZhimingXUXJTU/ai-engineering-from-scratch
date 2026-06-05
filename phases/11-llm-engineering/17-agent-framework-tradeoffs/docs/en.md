# Agent Framework Tradeoffs — LangGraph vs CrewAI vs AutoGen vs Agno | Agent 框架对比：LangGraph vs CrewAI vs AutoGen vs Agno

> Every framework sells the same demo (research agent builds a report) and hides the same bug (state schema fights with the orchestration layer). Pick the framework whose abstractions match the shape of your problem; everything else is glue you write twice.

> **【中文解读】** 每个框架都展示同样的 demo（研究 Agent 生成报告），都隐藏同样的 bug（状态 schema 与编排层冲突）。选择抽象匹配你问题形状的框架，其他的都是你要写两遍的胶水代码。

> **【拓展：框架选择→Agent工程实践】** LangGraph 适合需要精细控制的有状态工作流；CrewAI 适合多角色协作；AutoGen 适合对话式多 Agent；选错框架是 Agent 项目失败的首要原因。

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph)
**Time:** ~45 minutes

## The Problem | 问题引入

You have a task that needs more than one LLM call. Maybe it is a research workflow (plan, search, summarize, cite). Maybe it is a code-review pipeline (parse diff, critique, patch, validate). Maybe it is a multi-turn assistant that books flights, writes emails, and files expense reports. You pick a framework.

> 你有一个需要多次 LLM 调用的任务。也许是研究工作流（规划、搜索、总结、引用）。也许是代码审查流水线（解析 diff、批评、修补、验证）。你选择了一个框架。

Three days later, you discover the framework's abstractions leak. CrewAI gives you roles but fights you when the "researcher" needs to hand a structured plan to the "writer." AutoGen gives you chat between agents but has no first-class state so your checkpoint is a pickle of a conversation log. LangGraph gives you a state graph but forces you to name every transition before you know what the agent will do. Agno gives you a single-agent abstraction that screams when you try to fan out to three concurrent workers.

> 三天后，你发现框架的抽象会泄漏。CrewAI 给你角色但当"研究员"需要将结构化计划交给"作家"时会出问题。AutoGen 给你 Agent 间聊天但没有一等公民状态。LangGraph 给你状态图但迫使你在知道 Agent 会做什么之前就命名每个转换。Agno 给你单 Agent 抽象，当你尝试扇出到三个并发工作者时会出问题。

The fix is not "pick the best framework." It is to match the framework's core abstraction to the shape of your problem. This lesson draws that map.

> 修复方法不是"选择最好的框架"。而是将框架的核心抽象与你问题的形状匹配。本课绘制了这张地图。


> **【中文解读】** Agent 框架选型的三个维度：(1) 任务复杂度——简单 RAG 用 LlamaIndex，复杂 Agent 用 LangGraph；(2) 团队经验——新手用 LangChain 模板，专家用原生 API；(3) 生产要求——需要 LangSmith 集成选 LangChain 生态。


## The Concept | 核心概念

> **【中文解读】** Agent 框架的选择是工程权衡：LangChain 生态最全但复杂度高，LlamaIndex 专注 RAG，CrewAI 适合多 Agent 协作，LangGraph 适合状态机控制流，直接用 API 最灵活但要自己写更多代码。

> **【拓展：Agent 框架的选型指南】** 选型维度：(1) 任务复杂度（简单 RAG 用 LlamaIndex，复杂 Agent 用 LangGraph）；(2) 团队经验（新手用 LangChain 模板，专家用原生 API）；(3) 生产要求（LangSmith 集成选 LangChain 生态）。2025 年的趋势是框架轻量化。


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

Four frameworks dominate the 2026 landscape. Their core abstractions are not the same.

> 四个框架主导了 2026 年的格局。它们的核心抽象各不相同。

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### What "abstraction" actually means

A framework's core abstraction is the thing you draw on the whiteboard when you pitch the architecture.

> 框架的核心抽象是你推销架构时在白板上画的东西。

- **LangGraph** → you draw a graph. Nodes are steps, edges are transitions, and the state object at every point is typed. The mental model is a state machine.
  你画一个图。节点是步骤，边是转换。心智模型是状态机。
- **CrewAI** → you draw an org chart. Each role has a job description and a manager routes tasks. The mental model is a small team of specialists.
  你画一个组织图。每个角色有职责描述，经理分配任务。心智模型是小型专家团队。
- **AutoGen** → you draw a Slack DM. Two agents message each other; a third joins if you need a moderator. The mental model is chat.
  你画一个 Slack 私信。两个 Agent 互发消息。心智模型是聊天。
- **Agno** → you draw a single box with tools hanging off it. Put boxes next to each other for a team. The mental model is "agent with batteries included."
  你画一个挂着工具的方框。心智模型是"开箱即用的 Agent"。

### The state question

State is where most framework choices break down in production.

> 状态是大多数框架选择在生产中出问题的地方。

- **LangGraph.** Typed state (`TypedDict` or Pydantic model), per-field reducers, first-class checkpointer (SQLite/Postgres/Redis). Resume, interrupt, and time-travel are free. *(See Phase 11 · 16.)*
- **CrewAI.** State flows as strings between tasks via the `context` field, or structured through `output_pydantic`. No durable per-crew store out of the box; you bolt on your own if the crew must survive a restart.
- **AutoGen.** State is the chat history and any user-defined `context`. Conversation transcripts persist; arbitrary workflow state does not unless you write adapters.
- **Agno.** Built-in storage drivers (SQLite, Postgres, Mongo, Redis, DynamoDB) attached to an `Agent` via `storage=` — conversation sessions and user memories persist automatically. Not a full graph checkpointer; a session store.

### The branching question

Every non-trivial agent branches. Who decides the branch matters.

> 每个非平凡的 Agent 都有分支。谁决定分支很重要。

- **LangGraph** — you decide, via conditional edges. Routing is a Python function with named branches. Branches are first-class in the compiled graph; the checkpointer records which branch was taken.
- **CrewAI** — the manager decides in hierarchical mode; in sequential mode you decide at build time. Routing is implicit in the task list; there is no first-class "if" outside the manager's prompt.
- **AutoGen** — the agents decide via chat. Branching is emergent from who speaks next. `GroupChatManager` selects the next speaker; you can hand-write a `speaker_selection_method` but the default is LLM-driven.
- **Agno** — the agent decides by which tool to call next. Teams have a coordinator/router/collaborator mode; branching beyond that is the developer's responsibility.

### The observability question

> 可观测性问题

- **LangGraph** — OpenTelemetry via LangSmith or any OTel exporter. Every node transition is a trace span; checkpoints double as replayable traces. LangSmith is the first-party option; Langfuse/Phoenix also have adapters.
- **CrewAI** — first-class OpenTelemetry since late-2025; integrations with Langfuse, Phoenix, Opik, AgentOps.
- **AutoGen** — OpenTelemetry integration via `autogen-core`; AgentOps and Opik have connectors. Tracing granularity is per-agent-message, not per-node.
- **Agno** — built-in `monitoring=True` flag plus OpenTelemetry exporters; tight integration with Langfuse for session traces.

### Cost and latency

All four frameworks add per-call overhead (framework logic, validation, serialization). Rough order of increasing overhead: Agno ≈ LangGraph < CrewAI ≈ AutoGen. The difference is dominated by how much extra LLM routing the framework does. CrewAI's hierarchical manager spends tokens deciding who goes next; AutoGen's `GroupChatManager` likewise. LangGraph only spends tokens where you write `llm.invoke`. Agno's single-agent path is thin.

> 四个框架都会增加每次调用的开销。开销递增的大致顺序：Agno ≈ LangGraph < CrewAI ≈ AutoGen。差异主要由框架做多少额外的 LLM 路由决定。

When cost per run matters, prefer explicit routing (LangGraph edges, AutoGen `speaker_selection_method`) over LLM-selected routing.

> 当每次运行成本重要时，优先使用显式路由而非 LLM 选择路由。

### Interoperability

> 互操作性

- **LangGraph** ↔ **LangChain** tools, retrievers, LLMs. First-class MCP adapter (tools imported as MCP servers).
- **CrewAI** ↔ tools inherit from `BaseTool`; LangChain tools, LlamaIndex tools, and MCP tools all adapt in. Crew-to-crew delegation via `allow_delegation=True`.
- **AutoGen** → `FunctionTool` wraps any Python callable; MCP adapter available. Tight coupling to AG2 ecosystem for agent-to-agent patterns.
- **Agno** → `@tool` decorator or BaseTool subclass; MCP adapter; tools can be shared across agents and teams.

## The Skill

> You can explain, in one sentence, why a given framework is right for a given agent problem.

Pre-build checklist:

> 构建前检查清单：

1. **Draw the shape.** Is this a graph (typed state, named transitions)? A role play (specialists hand off work)? A chat (agents talk until done)? A single agent with tools?
   **画出形状。** 这是一个图？角色扮演？聊天？还是带工具的单 Agent？
2. **Decide who branches.** Developer-decided branching → LangGraph. Manager-agent-decided → CrewAI hierarchical. Chat-emergent → AutoGen. Tool-call-decided → Agno.
   **决定谁分支。** 开发者决定 → LangGraph。经理 Agent 决定 → CrewAI。聊天涌现 → AutoGen。工具调用决定 → Agno。
3. **Check the state budget.** Do you need resume-from-checkpoint? Time-travel? Human interrupts mid-run? If yes, LangGraph is the default; Agno sessions cover conversation-scoped state.
   **检查状态预算。** 你需要从检查点恢复吗？时间旅行？运行中人工中断？
4. **Check the cost budget.** LLM-selected routing costs extra tokens per turn. If the agent runs thousands of times a day, prefer explicit routing.
   **检查成本预算。** LLM 选择的路由每轮额外消耗 token。
5. **Budget the framework overhead.** Every framework is another dependency. If the task is two LLM calls and a tool, write 30 lines of plain Python; no framework is cheaper than no framework.
   **预算框架开销。** 每个框架都是另一个依赖。如果任务只是两次 LLM 调用一个工具，写 30 行纯 Python。

Refuse to reach for a framework before you can draw the graph, the org chart, the chat, or the agent box. Refuse to pick one that forces you to fight its state model for the thing you actually need.

> 在你能画出图、组织图、聊天或 Agent 框之前，不要伸手拿框架。不要选择一个迫使你为其状态模型而战的东西。

## The Decision Matrix

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

## Exercises | 练习题

1. **Easy.** Take the same task — "research Anthropic's headquarters, write a 200-word brief, cite sources" — and implement it in LangGraph (four nodes: plan, search, write, cite) and in CrewAI (three roles: researcher, writer, editor). Report token cost per run and lines of code.
   用同一个任务在 LangGraph 和 CrewAI 中实现，报告每次运行的 token 成本和代码行数。
2. **Medium.** Build the same task in AutoGen (researcher ↔ writer chat, editor joins via `GroupChat`) and Agno (a single agent with `search_tools` and `write_tools`, plus a session store). Rank the four implementations on (a) cost per run, (b) ability to resume after a crash, (c) ability to inject a human approval before the write step.
   在 AutoGen 和 Agno 中实现相同任务，按成本、崩溃恢复能力、人工审批注入能力排名。
3. **Hard.** Build a decision-tree script `pick_framework.py` that takes a short problem description (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`) and returns a recommendation with one-sentence justification. Verify it on six cases you design yourself.
   构建决策树脚本，根据问题描述返回框架推荐。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Further Reading | 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — StateGraph, checkpointers, interrupts, time-travel.
  LangGraph 文档——StateGraph、检查点、中断、时间旅行。
- [CrewAI documentation](https://docs.crewai.com/) — Crews, Flows, Agents, Tasks, Processes.
  CrewAI 文档——Crew、Flow、Agent、Task、Process。
- [AutoGen documentation](https://microsoft.github.io/autogen/) — ConversableAgent, GroupChat, teams, tools.
  AutoGen 文档——ConversableAgent、GroupChat、teams、tools。
- [Agno documentation](https://docs.agno.com/) — Agent, Team, Workflow, storage, memory.
  Agno 文档——Agent、Team、Workflow、storage、memory。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) — pattern library (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) framework-agnostic.
  Anthropic 关于构建有效 Agent 的模式库，框架无关。
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) — the loop every framework dresses up.
  每个框架都在包装的 ReAct 循环的原始论文。
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) — AutoGen's design paper.
  AutoGen 的设计论文。
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442) — role-play foundation that CrewAI-style persona stacks build on.
  CrewAI 风格角色堆栈所基于的角色扮演基础。
- Phase 11 · 16 (LangGraph) — the framework this lesson benchmarks against.
  本课对比的基准框架。
- Phase 11 · 19 (Reflexion) — a pattern that maps cleanly to LangGraph but awkwardly to CrewAI.
  一个在 LangGraph 中清晰映射但在 CrewAI 中笨拙的模式。
- Phase 11 · 22 (Production observability) — how to instrument whichever framework you pick.
  如何为你选择的任何框架添加可观测性。
