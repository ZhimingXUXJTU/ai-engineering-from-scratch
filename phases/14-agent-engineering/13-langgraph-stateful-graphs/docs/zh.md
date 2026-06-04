# LangGraph：有状态图与持久执行

> LangGraph is the 2026 reference for low-level stateful orchestration. Agent is a state machine; nodes are functions; edges are transitions; state is immutable and checkpointed after every step. Resume from any failure exactly where it left off.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns)
**预计时间：** ~75 minutes

## 学习目标

- Describe LangGraph's core model: state machine with immutable state, function nodes, conditional edges, and post-step checkpoints.
- Name the four capabilities the docs highlight: durable execution, streaming, human-in-the-loop, comprehensive memory.
- Explain the three orchestration topologies LangGraph supports: supervisor, peer-to-peer (swarm), hierarchical (nested subgraphs).
- Implement a stdlib state graph with immutable state, conditional edges, and a checkpoint/resume cycle.

## 问题引入

> **【中文解读】** Agent 和工作流共享一个问题：当 40 步运行在第 38 步失败时，你想从第 38 步恢复而不是从头开始。LangGraph 的设计答案：状态是一等公民的带类型对象，变更操作是显式的，检查点在每个节点执行后持久化。恢复只需调用 `load_state(session_id)`。
> **【中文解读】** Agent 和工作流共享一个问题：当 40 步运行在第 38 步失败时，你想从第 38 步恢复而不是从头开始。LangGraph 的设计答案：状态是一等公民的带类型对象，变更操作是显式的，检查点在每个节点执行后持久化。恢复只需调用 `load_state(session_id)`。
> **【拓展：LangGraph → 状态图编排】** LangGraph 是 2026 年底层有状态编排的参考实现。它将 Agent 建模为状态机——节点是函数，边是条件转换，状态在每个步骤后被检查点保存。LangChain 生态系统的核心框架，广泛用于生产级 Agent 编排。

## 核心概念

### The graph
> **【中文解读】** LangGraph 的图由三个要素定义：(1) 状态类型——每个节点读写的带类型 dict 或 Pydantic 模型；(2) 节点——纯函数 `(state) -> state_update`，返回值合并到状态中；(3) 边——节点之间的条件或直接转换。
A graph is defined by: A typed dict (or Pydantic model) that every node reads and mutates.
- **Nodes.** Pure functions `(state) -> state_update`. Updates are merged into state after return.
- **Edges.** Conditional or direct transitions between nodes.
- **Entry and exit.** `START` and `END` sentinel nodes mark the boundary.
Example: an agent with `classify`, `refund`, `bug`, `sales`, `done` nodes — a routing workflow as a graph.
### Durable execution
After each node returns, the runtime serializes the state and writes it to a checkpointer (SQLite, Postgres, Redis, custom). On failure at step N, the runtime can `resume(session_id)` and pick up from step N+1 with exact state.
The LangGraph docs explicitly highlight production users where this matters: Klarna, Uber, J.P. Morgan. The claim isn't the graph shape; it's that the graph shape plus checkpointing makes recovery cheap.
### Streaming
Every node can yield partial output. The graph streams per-node-delta events to the caller so UIs update as the graph runs.
### Human-in-the-loop
Inspect and modify state between nodes. Implementations: pause before a critical node, surface state to a human, accept modifications, resume. The checkpointer makes this easy because state is already serialized.
### Memory
Short-term (within a run — conversation history in state) and long-term (across runs — persistent via the checkpointer plus a separate long-term store). LangGraph integrates with external memory systems (Mem0, custom) via tools.
### Three topologies
1. **Supervisor.** Central router LLM dispatches to specialist subagents. `create_supervisor()` in `langgraph-supervisor` (though the LangChain team in 2026 recommends doing this through tool calls directly for more context control).
2. **Swarm / peer-to-peer.** Agents hand off directly via a shared tool surface. No central router.
3. **Hierarchical.** Supervisors managing sub-supervisors, implemented as nested subgraphs.
### Where this pattern goes wrong
- **Checkpoints too small.** Only checkpointing conversation turns leaves tool state and memory writes unrecoverable. Full state must serialize.
- **Non-deterministic nodes.** Resume assumes node inputs produce the same state update. Random seeds, wall-clock, external APIs must be captured.
- **Over-use of conditional edges.** A graph with every edge conditional is a state machine that cannot be reasoned about. Prefer linear chains with occasional branches.

## 动手实现

`code/main.py` implements a stdlib stateful graph:
- `State` — a typed dict with `messages`, `step`, `route`, `output`, `human_approval`.
- `Node` — callable taking state and returning an update dict.
- `StateGraph` — nodes + edges + conditional edges + run + resume.
- `SQLiteCheckpointer` (in-memory fake) — serializes state after every node; `load(session_id)` restores.
- A demo graph: classify -> branch(refund / bug / sales) -> human gate -> send.
Run it:
```
python3 code/main.py
```
The trace shows the first run failing at the human gate, persistence, then resume producing the final output.

## 用框架实现

- **LangGraph** — the reference, production-ready. Use `create_react_agent`, `create_supervisor`, or build your own graph.
- **AutoGen v0.4** (Lesson 14) — actor model alternative for high-concurrency scenarios.
- **Claude Agent SDK** (Lesson 17) — managed harness with built-in session store.
- **Custom** — when you need exact control over state shape or checkpointer backend.

## 产出物

`outputs/skill-state-graph.md` generates a LangGraph-shaped state graph in any target runtime with checkpointing and resume wired in.

## 练习题

1. Add a conditional edge from `classify` to `end` when classification confidence is below a threshold. Resume the run after a human sets `route` manually.
   *思考并实践此练习*
2. Swap the SQLite-like fake for a real SQLite checkpointer. Measure per-step serialization overhead.
   *思考并实践此练习*
3. Implement parallel edges: two nodes run concurrently, merge by a custom reducer. What does immutable state buy here?
   *思考并实践此练习*
4. Read `langgraph-supervisor` reference. Port the toy to `create_supervisor`. Compare the trace shapes.
   *思考并实践此练习*
5. Add streaming: each node yields partial state while it runs. Print the deltas as they arrive.
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| State graph | "Agent as state machine" |
| Checkpointer | "Persistence backend" |
| Reducer | "State merger" |
| Conditional edge | "Branch" |
| Subgraph | "Nested graph" |
| Durable execution | "Resume from failure" |
| Supervisor | "Router LLM" |
| Swarm | "P2P agents" |

## 延伸阅读

