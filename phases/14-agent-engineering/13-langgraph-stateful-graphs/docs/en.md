# LangGraph: Stateful Graphs and Durable Execution | LangGraph：有状态图与持久执行

> LangGraph is the 2026 reference for low-level stateful orchestration. Agent is a state machine; nodes are functions; edges are transitions; state is immutable and checkpointed after every step. Resume from any failure exactly where it left off.

> **【中文解读】** LangGraph 是 2026 年底层有状态编排的参考实现。Agent 是状态机；节点是函数；边是转换；状态是不可变的且每步后检查点保存。可从任何失败处精确恢复。

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Describe LangGraph's core model: state machine with immutable state, function nodes, conditional edges, and post-step checkpoints.
  中文翻译：描述 LangGraph 的核心模型：带不可变状态、函数节点、条件边和步后检查点的状态机。
- Name the four capabilities the docs highlight: durable execution, streaming, human-in-the-loop, comprehensive memory.
  中文翻译：说出文档强调的四种能力：持久执行、流式传输、人在回路中、全面记忆。
- Explain the three orchestration topologies LangGraph supports: supervisor, peer-to-peer (swarm), hierarchical (nested subgraphs).
  中文翻译：解释 LangGraph 支持的三种编排拓扑：监督者、点对点（群体）、层次化（嵌套子图）。
- Implement a stdlib state graph with immutable state, conditional edges, and a checkpoint/resume cycle.
  中文翻译：用标准库实现带不可变状态、条件边和检查点/恢复周期的状态图。

## The Problem | 问题引入

Agents and workflows share a problem: when a 40-step run fails at step 38, you want to resume from step 38, not start over. Second-class state models leave operators hacking retries around a library that assumes fresh runs.

> Agent 和工作流共享一个问题：当 40 步运行在第 38 步失败时，你想从第 38 步恢复而不是从头开始。二等状态模型让运维围绕假设全新运行的库来拼凑重试。

LangGraph's design answer: state is a first-class typed object, mutations are explicit, and checkpoints persist after every node. Resume is a `load_state(session_id)` call.

> LangGraph 的设计答案：状态是一等公民的带类型对象，变更操作是显式的，检查点在每个节点后持久化。恢复只需调用 `load_state(session_id)`。

> **【中文解读】** Agent 和工作流共享一个问题：当 40 步运行在第 38 步失败时，你想从第 38 步恢复而不是从头开始。LangGraph 的设计答案：状态是一等公民的带类型对象，变更操作是显式的，检查点在每个节点执行后持久化。恢复只需调用 `load_state(session_id)`。

> **【拓展：LangGraph → 状态图编排】** LangGraph 是 2026 年底层有状态编排的参考实现。它将 Agent 建模为状态机——节点是函数，边是条件转换，状态在每个步骤后被检查点保存。LangChain 生态系统的核心框架，广泛用于生产级 Agent 编排。

## The Concept | 核心概念

### The graph

A graph is defined by: A typed dict (or Pydantic model) that every node reads and mutates.

> 图由以下定义：一个每个节点都读写的带类型 dict（或 Pydantic 模型）。

- **Nodes.** Pure functions `(state) -> state_update`. Updates are merged into state after return.
  中文翻译：**节点。** 纯函数 `(state) -> state_update`。更新在返回后合并到状态中。
- **Edges.** Conditional or direct transitions between nodes.
  中文翻译：**边。** 节点之间的条件或直接转换。
- **Entry and exit.** `START` and `END` sentinel nodes mark the boundary.
  中文翻译：**入口和出口。** `START` 和 `END` 哨兵节点标记边界。

> **【中文解读】** LangGraph 的图由三个要素定义：(1) 状态类型——每个节点读写的带类型 dict 或 Pydantic 模型；(2) 节点——纯函数 `(state) -> state_update`，返回值合并到状态中；(3) 边——节点之间的条件或直接转换。

Example: an agent with `classify`, `refund`, `bug`, `sales`, `done` nodes — a routing workflow as a graph.

> 示例：一个包含 `classify`、`refund`、`bug`、`sales`、`done` 节点的 Agent——路由工作流作为图。

### Durable execution

After each node returns, the runtime serializes the state and writes it to a checkpointer (SQLite, Postgres, Redis, custom). On failure at step N, the runtime can `resume(session_id)` and pick up from step N+1 with exact state.

> 每个节点返回后，运行时序列化状态并写入检查点器（SQLite、Postgres、Redis、自定义）。在步骤 N 失败时，运行时可以 `resume(session_id)` 并从步骤 N+1 用精确状态继续。

The LangGraph docs explicitly highlight production users where this matters: Klarna, Uber, J.P. Morgan. The claim isn't the graph shape; it's that the graph shape plus checkpointing makes recovery cheap.

> LangGraph 文档明确强调了对这一点的生产用户：Klarna、Uber、J.P. Morgan。声明不是图的形状；而是图的形状加上检查点使恢复成本很低。

### Streaming

Every node can yield partial output. The graph streams per-node-delta events to the caller so UIs update as the graph runs.

> 每个节点可以产生部分输出。图向调用者流式传输每节点增量事件，使 UI 在图运行时更新。

### Human-in-the-loop

Inspect and modify state between nodes. Implementations: pause before a critical node, surface state to a human, accept modifications, resume. The checkpointer makes this easy because state is already serialized.

> 在节点之间检查和修改状态。实现方式：在关键节点前暂停、向人类展示状态、接受修改、恢复。检查点器使这很容易，因为状态已经序列化。

### Memory

Short-term (within a run — conversation history in state) and long-term (across runs — persistent via the checkpointer plus a separate long-term store). LangGraph integrates with external memory systems (Mem0, custom) via tools.

> 短期（一次运行内——状态中的对话历史）和长期（跨运行——通过检查点器加独立长期存储持久化）。LangGraph 通过工具与外部记忆系统（Mem0、自定义）集成。

### Three topologies

1. **Supervisor.** Central router LLM dispatches to specialist subagents. `create_supervisor()` in `langgraph-supervisor` (though the LangChain team in 2026 recommends doing this through tool calls directly for more context control).
   中文翻译：**监督者。** 中央路由 LLM 分派到专家子 Agent。
2. **Swarm / peer-to-peer.** Agents hand off directly via a shared tool surface. No central router.
   中文翻译：**群体/点对点。** Agent 通过共享工具接口直接移交。无中央路由。
3. **Hierarchical.** Supervisors managing sub-supervisors, implemented as nested subgraphs.
   中文翻译：**层次化。** 监督者管理子监督者，实现为嵌套子图。

### Where this pattern goes wrong

- **Checkpoints too small.** Only checkpointing conversation turns leaves tool state and memory writes unrecoverable. Full state must serialize.
  中文翻译：**检查点太小。** 仅检查点对话轮次会留下不可恢复的工具状态和记忆写入。必须序列化完整状态。
- **Non-deterministic nodes.** Resume assumes node inputs produce the same state update. Random seeds, wall-clock, external APIs must be captured.
  中文翻译：**非确定性节点。** 恢复假设节点输入产生相同的状态更新。随机种子、挂钟时间、外部 API 必须被捕获。
- **Over-use of conditional edges.** A graph with every edge conditional is a state machine that cannot be reasoned about. Prefer linear chains with occasional branches.
  中文翻译：**过度使用条件边。** 每条边都是条件的图是无法推理的状态机。优先使用带偶尔分支的线性链。

## Build It | 动手构建

`code/main.py` implements a stdlib stateful graph:

> `code/main.py` 用标准库实现了有状态图：

- `State` — a typed dict with `messages`, `step`, `route`, `output`, `human_approval`.
  中文翻译：`State`——包含 `messages`、`step`、`route`、`output`、`human_approval` 的带类型 dict。
- `Node` — callable taking state and returning an update dict.
  中文翻译：`Node`——接受状态并返回更新 dict 的可调用对象。
- `StateGraph` — nodes + edges + conditional edges + run + resume.
  中文翻译：`StateGraph`——节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer` (in-memory fake) — serializes state after every node; `load(session_id)` restores.
  中文翻译：`SQLiteCheckpointer`（内存模拟）——每个节点后序列化状态；`load(session_id)` 恢复。
- A demo graph: classify -> branch(refund / bug / sales) -> human gate -> send.
  中文翻译：演示图：classify -> branch(refund / bug / sales) -> human gate -> send。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows the first run failing at the human gate, persistence, then resume producing the final output.

> 轨迹显示第一次运行在人类门控处失败、持久化，然后恢复产生最终输出。

## Use It | 用框架实现

- **LangGraph** — the reference, production-ready. Use `create_react_agent`, `create_supervisor`, or build your own graph.
  中文翻译：**LangGraph**——参考实现，生产就绪。使用 `create_react_agent`、`create_supervisor` 或构建自己的图。
- **AutoGen v0.4** (Lesson 14) — actor model alternative for high-concurrency scenarios.
  中文翻译：**AutoGen v0.4**（第 14 课）——高并发场景的 Actor 模型替代方案。
- **Claude Agent SDK** (Lesson 17) — managed harness with built-in session store.
  中文翻译：**Claude Agent SDK**（第 17 课）——带内置会话存储的托管框架。
- **Custom** — when you need exact control over state shape or checkpointer backend.
  中文翻译：**自定义**——当你需要精确控制状态形状或检查点器后端时。

## Ship It | 产出物

`outputs/skill-state-graph.md` generates a LangGraph-shaped state graph in any target runtime with checkpointing and resume wired in.

> `outputs/skill-state-graph.md` 在任何目标运行时中生成 LangGraph 形状的状态图，内置检查点和恢复。

## Exercises | 练习题

1. Add a conditional edge from `classify` to `end` when classification confidence is below a threshold. Resume the run after a human sets `route` manually.
   中文翻译：当分类置信度低于阈值时添加从 `classify` 到 `end` 的条件边。人类手动设置 `route` 后恢复运行。
2. Swap the SQLite-like fake for a real SQLite checkpointer. Measure per-step serialization overhead.
   中文翻译：将 SQLite 模拟替换为真实 SQLite 检查点器。测量每步序列化开销。
3. Implement parallel edges: two nodes run concurrently, merge by a custom reducer. What does immutable state buy here?
   中文翻译：实现并行边：两个节点并发运行，用自定义 reducer 合并。不可变状态在这里带来什么？
4. Read `langgraph-supervisor` reference. Port the toy to `create_supervisor`. Compare the trace shapes.
   中文翻译：阅读 `langgraph-supervisor` 参考。将玩具移植为 `create_supervisor`。比较轨迹形态。
5. Add streaming: each node yields partial state while it runs. Print the deltas as they arrive.
   中文翻译：添加流式传输：每个节点运行时产生部分状态。打印到达的增量。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## Further Reading | 延伸阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — the reference docs
  中文翻译：LangGraph 概览——参考文档。
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/) — supervisor pattern API
  中文翻译：langgraph-supervisor 参考——监督者模式 API。
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) — actor-model alternative
  中文翻译：AutoGen v0.4 微软研究——Actor 模型替代方案。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) — session store and subagents
  中文翻译：Claude Agent SDK 概览——会话存储和子代理。
