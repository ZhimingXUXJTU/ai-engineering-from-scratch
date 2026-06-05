# LangGraph — State Machines for Agents | LangGraph：Agent 的状态机

> A ReAct loop written by hand is a `while True`. A ReAct loop written in LangGraph is a graph you can checkpoint, interrupt, branch, and time-travel through. The agent hasn't changed. The harness around it has.

> **【中文解读】** 手写的 ReAct 循环就是一个 `while True`。用 LangGraph 写的 ReAct 循环是一个图——可以检查点保存、中断、分支、时间旅行。Agent 没变，但围绕它的框架变了。

> **【拓展：LangGraph→Agent工程】** LangGraph 是目前最成熟的 Agent 编排框架，将 Agent 执行建模为状态图（StateGraph），支持人机协作、分支逻辑和持久化状态。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol)
**Time:** ~75 minutes

## The Problem | 问题引入

You ship a function-calling agent. It works for three turns, then something goes wrong: the model tries a tool that returns 500, the user changes their mind mid-task, or the agent decides to refund an order without a human signing off. The `while True:` loop has no hooks. You can't pause it, you can't rewind it, and you can't branch off into "what if the model had picked the other tool." The moment you ship this past a demo, the agent becomes a black box that either worked or didn't.

> 你发布了一个函数调用 Agent。它工作了三轮，然后出了问题：模型尝试了一个返回 500 的工具，用户中途改变主意，或者 Agent 决定在没有人工签字的情况下退款。`while True:` 循环没有钩子。你无法暂停它、倒回它、或分支到"如果模型选了另一个工具会怎样"。一旦你把这样的东西发布出 demo，Agent 就变成了一个黑盒。

The next step is obvious once you see it. The agent is already a state machine — system prompt plus message history plus pending tool calls plus the next action. Make the state machine explicit: nodes for "the model thinks," "a tool runs," "a human approves," and edges for the conditional transitions between them. Once the graph is explicit, the harness gets four things for free: checkpointing (save state between steps), interrupts (pause for a human), streaming (stream tokens and intermediate events), and time-travel (rewind to a prior state and try a different branch).

> 一旦你看到了，下一步就显而易见了。Agent 本身就是一个状态机——系统提示加消息历史加待处理的工具调用加上下一步动作。让状态机显式化：节点代表"模型思考"、"工具运行"、"人工审批"，边代表它们之间的条件转换。

LangGraph is the library that ships this abstraction. It is not an agent framework in the LangChain sense ("here is an AgentExecutor, good luck"). It is a graph runtime with first-class state, first-class persistence, and first-class interrupts. The agent loop is something you draw, not something you hand-write.

> LangGraph 是提供这种抽象的库。它不是 LangChain 意义上的 Agent 框架。它是一个具有一等公民状态、一等公民持久化和一等公民中断的图运行时。Agent 循环是你画出来的，而不是手写的。


> **【中文解读】** LangGraph 的核心优势是支持复杂控制流：循环（Agent 遇到错误时重试）、条件分支（根据任务类型选择不同工具）、人工审批（高风险操作需人工确认）。简单的 LangChain Chain 无法表达这些复杂逻辑。


## The Concept | 核心概念

> **【中文解读】** LangGraph 将 LLM Agent 建模为状态机（State Machine）：定义状态节点（如检索、生成、验证）和转换边（条件分支）。相比简单的链式调用，状态机支持循环、条件分支、人工审批等复杂控制流。

> **【拓展：LangGraph 与 Agent 编排】** LangGraph 是 LangChain 团队推出的 Agent 编排框架，支持：多 Agent 协作、人工介入（Human-in-the-loop）、持久化状态、时间旅行调试。与 CrewAI（角色扮演 Agent）和 AutoGen（多 Agent 对话）相比，LangGraph 更适合需要精确控制流的复杂业务场景。


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

A `StateGraph` has three things.

> `StateGraph` 有三样东西。

1. **State.** A typed dict (TypedDict or Pydantic model) that flows through the graph. Every node receives the full state and returns a partial update, which LangGraph merges using a *reducer* per field — `operator.add` for lists that should accumulate, overwrite by default.
   **状态。** 流过图的类型化字典。每个节点接收完整状态并返回部分更新。
2. **Nodes.** Python functions `state -> partial_state`. Each is a discrete step: "call the model," "run tools," "summarize."
   **节点。** Python 函数 `state -> partial_state`。每个是一个离散步骤。
3. **Edges.** Transitions between nodes. Static edges go one place. Conditional edges take a router function `state -> next_node_name` so the graph can branch on model output.
   **边。** 节点之间的转换。静态边去一个地方。条件边接受路由函数以在模型输出上分支。

You compile the graph. Compile binds the topology, attaches a checkpointer (optional but essential for production), and returns a runnable. You invoke it with an initial state and a `thread_id`. Every step of execution persists a checkpoint keyed on `(thread_id, checkpoint_id)`.

> 你编译图。编译绑定拓扑、附加检查点器并返回一个可运行对象。你用初始状态和 `thread_id` 调用它。执行的每一步都会持久化一个检查点。

### The four superpowers

**Checkpointing.** Every node transition writes the new state to a store (in-memory for tests, Postgres/Redis/SQLite for prod). Resume by calling the graph again with the same `thread_id`. The graph picks up where it paused.

> **检查点。** 每个节点转换将新状态写入存储。通过使用相同的 `thread_id` 再次调用图来恢复。

**Interrupts.** Mark a node with `interrupt_before=["human_review"]` and execution stops before that node runs. The state persists. Your API responds to the user with "awaiting approval." A later request to the same `thread_id` with `Command(resume=...)` resumes execution.

> **中断。** 用 `interrupt_before` 标记一个节点，执行在该节点运行前停止。状态被持久化。后续请求可恢复执行。

**Streaming.** `graph.stream(state, mode="updates")` yields state deltas as they happen. `mode="messages"` streams the LLM tokens inside model nodes. `mode="values"` yields full snapshots. You pick what to surface in your UI.

> **流式输出。** `graph.stream` 按发生顺序产出状态增量。你选择在 UI 中显示什么。

**Time-travel.** `graph.get_state_history(thread_id)` returns the full checkpoint log. Pass any prior `checkpoint_id` to `graph.invoke` and you fork from that point. Great for debugging ("what if the model had picked tool B instead?") and for regression tests that replay production traces.

> **时间旅行。** 返回完整的检查点日志。传入任何先前的 `checkpoint_id`，你从那个点分叉。用于调试和回归测试。

### Reducers are the point

Every state field has a reducer. Most defaults are fine — a new value overwrites the old. But message lists need `operator.add` so new messages append instead of replacing. Parallel edges merge their updates through the reducer. If two nodes both update `messages` and you forgot the `Annotated[list, add_messages]`, the second wins silently and you lose half the turn. The reducer is the only subtle thing in the library; get it right and the rest composes.

> 每个状态字段都有一个 reducer。消息列表需要 `operator.add` 以便新消息追加而不是替换。Reducer 是这个库中唯一微妙的东西；搞对了，其余的自然组合。

### The ReAct graph in four nodes

A production ReAct agent is four nodes and two edges:

> 一个生产级 ReAct Agent 是四个节点和两条边：

1. `agent` — calls the LLM with the current message history. Returns the assistant message (which may contain tool_calls).
2. `tools` — executes any tool_calls in the last assistant message, appends the tool results as tool messages.
3. A conditional edge from `agent` that routes to `tools` if the last message has tool_calls, else to `END`.
4. A static edge from `tools` back to `agent`.

That is it. You get the full ReAct loop (Thought → Action → Observation → Thought → …) with checkpointing, interrupts, and streaming, in roughly 40 lines of code.

> 就是这样。你得到了完整的 ReAct 循环（思考 → 行动 → 观察 → 思考 → ...），带检查点、中断和流式输出，大约 40 行代码。

### StateGraph vs Send (fanout)

`Send(node_name, state)` lets a node dispatch parallel subgraphs. Example: the agent decides to query three retrievers at once. Each `Send` spawns a parallel execution of the target node; their outputs merge through the state reducer. This is how LangGraph expresses the orchestrator-workers pattern without threading primitives.

> `Send(node_name, state)` 让一个节点分派并行子图。每个 `Send` 生成目标节点的并行执行；它们的输出通过状态 reducer 合并。

### Subgraphs

A compiled graph can be a node in another graph. The outer graph sees a single node; the inner graph has its own state and its own checkpoints. This is how teams build supervisor-worker agents: the supervisor graph routes user intent to a per-domain worker subgraph.

> 编译后的图可以是另一个图中的节点。外层图看到一个单一节点；内层图有自己的状态和检查点。这是团队构建 supervisor-worker Agent 的方式。

## Build It | 动手实现

### Step 1: state and nodes

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages` is the reducer that makes the message list accumulate instead of overwrite. Forgetting it is the most common LangGraph bug.

> `add_messages` 是让消息列表累积而非覆盖的 reducer。忘记它是最常见的 LangGraph bug。

### Step 2: run with a thread

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Every update is a dict `{node_name: state_delta}`. Your frontend can stream these to the UI so users see "agent is thinking… calling search_web… got result… answering."

### Step 3: add a human-in-the-loop interrupt

Mark a node so execution pauses before it runs.

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

The state, the checkpoint, and the thread all persist across the interrupt. Nothing is in memory except during execution.

> 状态、检查点和线程在中断期间全部持久化。除了执行期间，没有东西在内存中。

### Step 4: time-travel for debugging

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Passing `None` as the input replays from the given checkpoint; passing a value appends it as an update to that checkpoint's state before resuming. This is how you reproduce a bad agent run without re-running the whole conversation.

> 传入 `None` 作为输入从给定检查点重放；传入值则在恢复前将其作为更新附加到该检查点的状态。这就是如何在不重新运行整个对话的情况下复现一个错误的 Agent 运行。

### Step 5: swap the checkpointer for production

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis, and Postgres are shipped. `MemorySaver` is for tests. Anything that persists across restarts wants a real store.

> SQLite、Redis 和 Postgres 已提供。`MemorySaver` 用于测试。任何需要跨重启持久化的东西都需要真正的存储。

## The Skill

> You build agents as graphs, not as `while True` loops.

Before you reach for LangGraph, do a 60-second design:

> 在使用 LangGraph 之前，做一个 60 秒的设计：

1. **Name the nodes.** Every discrete decision or side-effecting action is a node. "Agent thinks," "tool runs," "reviewer approves," "response streams." If you can't list them, the task is not agent-shaped yet.
   **命名节点。** 每个离散决策或副作用动作都是一个节点。
2. **Declare the state.** Minimal TypedDict with a reducer for every list field. Do not stuff everything into `messages`; hoist task-specific fields (a working `plan`, a `budget` counter, a `retrieved_docs` list) to the top level.
   **声明状态。** 最小 TypedDict，每个列表字段有 reducer。
3. **Draw the edges.** Static unless the next step depends on model output. Every conditional edge needs a router function with named branches.
   **画边。** 除非下一步依赖模型输出，否则使用静态边。
4. **Choose a checkpointer up front.** `MemorySaver` for tests, Postgres/Redis/SQLite for anything else. Do not ship without one — no checkpointer means no resume, no interrupt, no time-travel.
   **提前选择检查点器。** 测试用 `MemorySaver`，其他用 Postgres/Redis/SQLite。
5. **Decide interrupts before tools run, not after.** Approvals go on the edge into a side-effecting node so you can cancel before harm; validation goes on the edge out of the model so you can reject bad calls cheaply.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"` for the UI, `mode="messages"` for token-level streaming inside model nodes, `mode="values"` for full snapshots during eval.
   **默认使用流式输出。**

Refuse to ship a LangGraph agent that has no checkpointer. Refuse to ship one that interrupts *after* the side effect. Refuse to ship a `messages` field without `add_messages` as its reducer.

> 拒绝发布没有检查点器的 LangGraph Agent。拒绝发布在副作用之后中断的 Agent。拒绝发布没有 `add_messages` 作为 reducer 的 `messages` 字段。

## Exercises | 练习题

1. **Easy.** Implement the four-node ReAct graph above with a calculator tool and a web-search tool. Verify that `list(app.get_state_history(config))` returns at least four checkpoints for a two-turn conversation.
   **简单。** 实现上述四节点 ReAct 图，验证检查点历史记录。
2. **Medium.** Add a `planner` node that runs before `agent` and writes a structured `plan: list[str]` into state. Have `agent` mark plan steps as done. Fail the test if `plan` is lost across a checkpoint resume (wrong reducer).
   **中等。** 添加一个在 `agent` 之前运行的 `planner` 节点，写入结构化计划到状态中。
3. **Hard.** Build a supervisor graph that routes between three subgraphs (`researcher`, `writer`, `reviewer`) using `Send`. Each subgraph has its own state and checkpointer. Add an `interrupt_before=["writer"]` on the outer graph so a human can approve the research brief. Confirm that time-travel from a prior checkpoint re-runs only the forked branch.
   **困难。** 构建一个 supervisor 图，在三个子图之间使用 `Send` 路由。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## Further Reading | 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — canonical reference for StateGraph, reducers, checkpointers, and interrupts.
  LangGraph 文档——StateGraph、reducer、检查点器和中断的权威参考。
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) — the mental model this lesson uses, straight from the source.
  LangGraph 概念：状态、reducer、检查点器。
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) — the detail on Postgres/SQLite/Redis stores, checkpoint namespaces, and thread IDs.
  LangGraph 持久化和检查点详情。
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) — `interrupt_before`, `interrupt_after`, `Command(resume=...)`, and the edit-state pattern.
  LangGraph 人机协作——interrupt 和 resume 模式。
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) — the pattern every LangGraph agent implements; read it for the reasoning trace rationale.
  每个 LangGraph Agent 实现的 ReAct 模式。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) — which graph shapes (chain, router, orchestrator-workers, evaluator-optimizer) to prefer and when.
  Anthropic 关于选择哪种图形状以及何时使用的指南。
- Phase 11 · 09 (Function Calling) — the tool-call primitive every LangGraph agent node reuses.
  第 11 阶段 · 09（函数调用）——每个 LangGraph Agent 节点重用的工具调用原语。
- Phase 11 · 14 (Model Context Protocol) — external tool discovery that plugs into a LangGraph `ToolNode` via the MCP adapter.
  第 11 阶段 · 14（MCP）——通过 MCP 适配器插入 LangGraph `ToolNode` 的外部工具发现。
- Phase 11 · 17 (Agent framework tradeoffs) — when to pick LangGraph over CrewAI, AutoGen, or Agno.
  第 11 阶段 · 17（Agent 框架对比）——何时选择 LangGraph。
