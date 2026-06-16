# AutoGen v0.4: Actor Model and Agent Framework | AutoGen v0.4：Actor 模型与 Agent 框架

> AutoGen v0.4 (Microsoft Research, Jan 2025) redesigned agent orchestration around the actor model. Async message exchange, event-driven agents, fault isolation, natural concurrency. The framework is now in maintenance mode while Microsoft Agent Framework (public preview Oct 2025) becomes the successor.

> **【中文解读】** AutoGen v0.4（微软研究院，2025 年 1 月）围绕 Actor 模型重新设计了 Agent 编排。异步消息交换、事件驱动 Agent、故障隔离、天然并发。该框架目前处于维护模式，Microsoft Agent Framework（2025 年 10 月公开预览）成为继任者。

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Describe the actor model: agents as actors, messages as the only IPC, failure isolation per actor.
  中文翻译：描述 Actor 模型：Agent 作为 Actor，消息作为唯一的进程间通信，每个 Actor 独立故障隔离。
- Name AutoGen v0.4's three API layers — Core, AgentChat, Extensions — and what each is for.
  中文翻译：说出 AutoGen v0.4 的三个 API 层——Core、AgentChat、Extensions——及各自的用途。
- Explain why decoupling message delivery from handling gives fault isolation and natural concurrency.
  中文翻译：解释为什么将消息投递与处理解耦能带来故障隔离和天然并发。
- Implement a stdlib actor runtime in Python and port a two-agent code-review flow onto it.
  中文翻译：用 Python 标准库实现 Actor 运行时并将双 Agent 代码审查流程移植到其上。

## The Problem | 问题引入

Most agent frameworks are synchronous: one agent produces, one agent consumes, in a call stack. Failures crash the stack. Concurrency is bolted on. Distribution requires rewriting.

> 大多数 Agent 框架是同步的：一个 Agent 生产、一个 Agent 消费，在调用栈中。失败会使栈崩溃。并发是后加的。分布式需要重写。

AutoGen v0.4's answer: the actor model. Each agent is an actor with a private inbox. Messages are the only interaction. The runtime decouples delivery from handling. Failures isolate to one actor. Concurrency is native. Distribution is just different transport.

> AutoGen v0.4 的答案：Actor 模型。每个 Agent 是一个带私有收件箱的 Actor。消息是唯一的交互方式。运行时将投递与处理解耦。失败隔离到一个 Actor。并发是原生的。分布式只是不同的传输方式。

> **【中文解读】** AutoGen v0.4 采用 Actor 模型——每个 Agent 是一个独立的异步 Actor，通过消息传递通信。这不同于 LangGraph 的图模型或 CrewAI 的角色模型。Actor 模型的优势是天然支持并发和分布式执行，劣势是调试和可观测性更复杂。

> **【拓展：AutoGen 的演进】** AutoGen 由微软研究院开发，v0.4 (2025) 是一次重大重构。从 v0.3 的对话模式转向 Actor 模型，灵感来自 Erlang/Akka 的并发模型。核心概念：每个 Agent 是一个 Actor，有独立的状态和消息队列，通过异步消息传递协作。这使得 AutoGen 特别适合多 Agent 分布式场景。

> 🔗 **【前置】** 必须先掌握：Phase 14·01（Agent Loop）和 Phase 14·12（Anthropic Workflow Patterns）——本节是这些模式在"并发场景"下的延伸。还需要"Actor 模型"的基本概念——如果不知道 Erlang/Akka 是什么，先去补一节分布式系统课。本节硬核在"异步消息传递"而非"LLM 调用"。

## The Concept | 核心概念

### Actors

An actor has:

> 一个 Actor 有：

- A private state (never directly touched from outside).
  中文翻译：私有状态（外部永远不直接触碰）。
- An inbox (message queue).
  中文翻译：收件箱（消息队列）。
- A handler: `receive(message) -> effects` where effects can be "reply," "send to other actor," "spawn new actor," "update state," "stop self."
  中文翻译：处理器：`receive(message) -> effects`，效果可以是"回复"、"发送给其他 Actor"、"创建新 Actor"、"更新状态"、"停止自己"。

Two actors cannot share memory. They can only send messages.

> 💡 **【类比】** Actor 模型像办公室里互不相见的同事：每个人有自己的工位（私有状态）和收件箱（消息队列）。你想让同事帮忙，不能直接去翻他的工位（共享内存），只能发邮件（发消息）。同事处理完邮件可能回信（reply）、转发给另一个人（send to other）、招实习生（spawn new actor）。**关键**：一个同事生病（崩溃）不影响其他人——这就是故障隔离。

> 两个 Actor 不能共享内存。它们只能发送消息。

### Three API layers in AutoGen v0.4

1. **Core.** Low-level actor framework. `AgentRuntime`, `Agent`, `Message`, `Topic`. Async message exchange, event-driven.
   中文翻译：**Core。** 底层 Actor 框架。`AgentRuntime`、`Agent`、`Message`、`Topic`。异步消息交换，事件驱动。
2. **AgentChat.** Task-driven high-level API (replacement for v0.2's ConversableAgent). `AssistantAgent`, `UserProxyAgent`, `RoundRobinGroupChat`, `SelectorGroupChat`.
   中文翻译：**AgentChat。** 任务驱动的高级 API（替代 v0.2 的 ConversableAgent）。`AssistantAgent`、`UserProxyAgent`、`RoundRobinGroupChat`、`SelectorGroupChat`。
3. **Extensions.** Integrations — OpenAI, Anthropic, Azure, tools, memory.
   中文翻译：**Extensions。** 集成——OpenAI、Anthropic、Azure、工具、记忆。

### Why decoupling matters

In the v0.2 model, calling `agent_a.chat(agent_b)` synchronously blocks agent_a until agent_b returns. In v0.4, `send(agent_b, msg)` puts the message in agent_b's inbox and returns. The runtime delivers later. Three consequences:

> 在 v0.2 模型中，调用 `agent_a.chat(agent_b)` 同步阻塞 agent_a 直到 agent_b 返回。在 v0.4 中，`send(agent_b, msg)` 将消息放入 agent_b 的收件箱并返回。运行时稍后投递。三个后果：

- **Fault isolation.** Agent B crashing does not crash Agent A — the runtime catches the failure in B's handler and decides what to do (log, retry, dead-letter).
  中文翻译：**故障隔离。** Agent B 崩溃不会导致 Agent A 崩溃——运行时在 B 的处理器中捕获故障并决定做什么（日志、重试、死信）。
- **Natural concurrency.** Many messages in flight at once; actors process their inbox concurrently.
  中文翻译：**天然并发。** 多条消息同时传输；Actor 并发处理它们的收件箱。
- **Distribution-ready.** Inbox + transport is the same abstraction whether the actor is in-process or on another host.
  中文翻译：**分布式就绪。** 收件箱 + 传输是相同的抽象，无论 Actor 在进程内还是在另一台主机上。

> ⚠️ **【易错点】** 用 Actor 模型但忘了"消息必须可序列化"。**后果**：本地开发跑通（消息传递的是 Python 对象引用），上生产分布到多机就崩——对方进程拿不到你的对象。**一行修复**：所有消息必须用 pydantic/dataclass/JSON-schema 定义，禁止传 lambda、文件句柄、数据库连接等不可序列化对象。

### Topologies

- **RoundRobinGroupChat.** Agents take turns in a fixed rotation.
  中文翻译：**RoundRobinGroupChat。** Agent 按固定轮换顺序轮流。
- **SelectorGroupChat.** A selector agent picks who goes next based on conversation context.
  中文翻译：**SelectorGroupChat。** 选择器 Agent 根据对话上下文选择下一个发言者。
- **Magentic-One.** Reference multi-agent team for web browsing, code execution, file handling. Built on AgentChat.
  中文翻译：**Magentic-One。** 用于网页浏览、代码执行、文件处理的参考多 Agent 团队。基于 AgentChat 构建。

### Observability

OpenTelemetry support is built in. Every message emits a span; tool calls carry `gen_ai.*` attributes per the 2026 OTel GenAI semantic conventions (Lesson 23).

> OpenTelemetry 支持内置。每条消息发出一个 span；工具调用携带 `gen_ai.*` 属性，符合 2026 年 OTel GenAI 语义约定（第 23 课）。

### Status: maintenance mode

Early 2026: AutoGen v0.7.x is stable for research and prototyping. Microsoft has shifted active development to the Microsoft Agent Framework (public preview Oct 1 2025; 1.0 GA targeted end of Q1 2026). AutoGen patterns port forward cleanly — the actor model is the durable idea.

> 🤔 **【困惑】** Q: AutoGen 已经进入维护模式了，我还该学吗？ A: 学"Actor 模型"这一节思想，但**别在生产上选 AutoGen**。原因：(1) 微软已转向 Microsoft Agent Framework（MAF），AutoGen 不再获得新特性；(2) Actor 模型本身是个**经久不衰的分布式设计思想**（来自 1973 年 Hewitt 论文，比 LLM 老 50 年），理解它对你评估 MAF、Erlang、Akka、Ray 都有帮助。把 AutoGen 当"教材"，把 MAF 或 LangGraph 当"生产工具"。

> 2026 年初：AutoGen v0.7.x 在研究和原型开发方面稳定。微软已将活跃开发转移到 Microsoft Agent Framework（2025 年 10 月 1 日公开预览；1.0 GA 目标 2026 年 Q1 末）。AutoGen 模式可以干净地向前移植——Actor 模型是持久的理念。

## Build It | 动手构建

`code/main.py` implements a stdlib actor runtime:

> `code/main.py` 用标准库实现了 Actor 运行时：

- `Message` — typed payload with `sender`, `recipient`, `topic`, `body`.
  中文翻译：`Message`——带 `sender`、`recipient`、`topic`、`body` 的带类型载荷。
- `Actor` — abstract with `receive(message, runtime)`.
  中文翻译：`Actor`——带 `receive(message, runtime)` 的抽象类。
- `Runtime` — event loop with a shared queue, delivery, failure isolation.
  中文翻译：`Runtime`——带共享队列、投递、故障隔离的事件循环。
- A two-actor demo: `ReviewerAgent` reviews code, `ChecklistAgent` runs a checklist; they exchange messages until consensus.
  中文翻译：双 Actor 演示：`ReviewerAgent` 审查代码，`ChecklistAgent` 运行检查清单；它们交换消息直到达成共识。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows message delivery, a simulated failure in one actor that does not crash the other, and convergence on a shared verdict.

> 轨迹显示消息投递、一个 Actor 中的模拟故障不会导致另一个崩溃，以及共享裁决的收敛。

## Use It | 用框架实现

- **AutoGen v0.4/v0.7** (maintenance) — stable for research, prototyping, multi-agent patterns.
  中文翻译：**AutoGen v0.4/v0.7**（维护中）——研究、原型、多 Agent 模式稳定。
- **Microsoft Agent Framework** (public preview) — the forward path; same actor-model ideas in a refreshed API.
  中文翻译：**Microsoft Agent Framework**（公开预览）——前进方向；在更新的 API 中体现相同的 Actor 模型理念。
- **LangGraph swarm topology** (Lesson 13) — similar pattern via shared-tool handoffs.
  中文翻译：**LangGraph 群体拓扑**（第 13 课）——通过共享工具移交的类似模式。
- **Custom actor runtime** — when you need specific transport (NATS, RabbitMQ, gRPC).
  中文翻译：**自定义 Actor 运行时**——当你需要特定传输（NATS、RabbitMQ、gRPC）时。

## Ship It | 产出物

`outputs/skill-actor-runtime.md` generates a minimal actor runtime plus a team template (RoundRobin or Selector) for a given multi-agent task.

> `outputs/skill-actor-runtime.md` 为给定多 Agent 任务生成最小 Actor 运行时加团队模板（RoundRobin 或 Selector）。

## Exercises | 练习题

1. Add a dead-letter queue: when a handler raises, park the failing message for human inspection. How often does DLQ get hit in your toy?
   中文翻译：添加死信队列：当处理器抛出异常时，将失败消息停放供人工检查。你的玩具中 DLQ 被触发的频率如何？
2. Implement `SelectorGroupChat`: a selector actor picks who processes the next message based on conversation state.
   中文翻译：实现 `SelectorGroupChat`：选择器 Actor 根据对话状态选择谁处理下一条消息。
3. Add distributed transport: swap the in-process queue for a JSON-over-HTTP server so actors can run in separate processes.
   中文翻译：添加分布式传输：将进程内队列替换为 JSON-over-HTTP 服务器，使 Actor 可以在独立进程中运行。
4. Wire an OTel span per message (or a no-op stand-in). Emit `gen_ai.agent.name`, `gen_ai.operation.name` per Lesson 23.
   中文翻译：为每条消息连接 OTel span（或 no-op 替代）。按第 23 课发出 `gen_ai.agent.name`、`gen_ai.operation.name`。
5. Read AutoGen v0.4's architecture post. Port your toy to the real `autogen_core` API. What did you skip that matters in production?
   中文翻译：阅读 AutoGen v0.4 的架构文章。将玩具移植到真正的 `autogen_core` API。你跳过了什么在生产中重要的东西？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## Further Reading | 延伸阅读

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) — the redesign post
  中文翻译：AutoGen v0.4 微软研究院——重新设计文章。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — graph-shaped alternative
  中文翻译：LangGraph 概览——图形替代方案。
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — spans AutoGen emits by default
  中文翻译：OpenTelemetry GenAI 语义约定——AutoGen 默认发出的 span。
