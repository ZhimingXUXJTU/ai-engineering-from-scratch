# Handoffs and Routines — Stateless Orchestration | 编排 交接 例程 状态

> OpenAI's Swarm (October 2024) distilled multi-agent orchestration to two primitives: **routines** (instructions + tools as a system prompt) and **handoffs** (a tool that returns another Agent). No state machine, no branching DSL — the LLM routes by calling the right handoff tool. The OpenAI Agents SDK (March 2025) is the production successor. Swarm itself remains the cleanest conceptual reference — its entire source fits in a few hundred lines. The pattern is viral because the API surface is roughly "agent = prompt + tools; handoff = function returning agent." Limitation: stateless, so memory is the caller's problem.

> **【中文解读】** 本节介绍了交接和例程——Agent 间传递任务控制权的标准流程和例程。

> **【拓展：handoffs and routines→具体应用】** 交接（Handoffs）是 OpenAI Agents SDK 的核心概念——Agent A 将控制权移交给 Agent B。关键设计决策：(1) 上下文传递——B 收到多少 A 的历史？(2) 恢复机制——B 完成后控制权回到 A 还是交给 C？(3) 超时处理——B 如果卡住怎么办？Routines 是预定义的交接序列。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·04（原语模型）、Phase 14·07（工具调用）。OpenAI Swarm 把多 Agent 简化为 2 原语：routine（系统提示+工具）+ handoff（返回另一个 Agent 的工具）。
> 💡 **【类比】** Handoff = "客服转接"。用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm 的天才之处：handoff 就是一个普通工具调用（返回 Agent），LLM 自动路由。无状态机、无 DSL，几百行代码搞定。OpenAI Agents SDK 是生产版本。

## Problem | 问题引入

Every multi-agent framework wants you to learn its DSL: LangGraph nodes and edges, CrewAI crews and tasks, AutoGen GroupChat and managers. The DSLs are real abstractions, but they make the thing feel heavier than it needs to be.

> 每个多 Agent 框架都想让你学习它的 DSL：LangGraph 的节点和边、CrewAI 的团队和任务、AutoGen 的 GroupChat 和管理者。DSL 是真正的抽象，但它们让事情感觉比实际需要的更重。

DSL lock-in is the multi-agent framework tax. Each DSL has its own concepts, its own debugging tools, its own community. Once you commit, migration is expensive. Swarm's bet: skip the DSL entirely, use the model's existing tool-calling.

> DSL 锁定是多 Agent 框架税。每个 DSL 有自己的概念、自己的调试工具、自己的社区。一旦你承诺，迁移昂贵。Swarm 的赌注：完全跳过 DSL，使用模型现有的工具调用。

Swarm pushes in the opposite direction: use the tool-calling capability the model already has. Handoffs become tool calls. The orchestrator is whichever agent currently holds the conversation. The state machine is implicit in the agents' system prompts.

> Swarm 推向相反的方向：使用模型已有的工具调用能力。交接变成工具调用。编排器就是当前持有对话的 Agent。状态机隐含在 Agent 的系统提示中.

The insight is profound: you do not need an orchestration DSL because LLMs are already orchestrators. Every LLM call decides what to do next based on context. Handoffs just expose that decision as a tool the model can call.

> 洞察深刻：你不需要编排 DSL，因为 LLM 已经是编排器。每次 LLM 调用根据上下文决定下一步做什么。交接只是将该决策暴露为模型可以调用的工具。

## Concept | 核心概念

### Two primitives

**Routine.** A system prompt that defines an agent's role and available tools. Think of it like a scoped set of instructions: "you are a triage agent; if the user asks about refunds, hand off to the refund agent."

> **例程。** 定义 Agent 角色和可用工具的系统提示。把它想象成一组范围化的指令："你是一个分诊 Agent；如果用户询问退款，交接给退款 Agent。"

**Handoff.** A tool the agent can call that returns a new Agent object. The Swarm runtime detects the Agent return value and switches the active agent for the next turn.

> **交接。** Agent 可以调用的工具，返回一个新的 Agent 对象。Swarm 运行时检测 Agent 返回值并为下一轮切换活动 Agent。

That is the entire abstraction.

> 这就是整个抽象。

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

The triage agent's system prompt makes it choose the right handoff based on the user message. The LLM's tool-calling does the routing.

> 分诊 Agent 的系统提示使其根据用户消息选择正确的交接。LLM 的工具调用完成路由。

This is the elegant move: reuse the model's existing tool-calling infrastructure for orchestration. No new DSL, no graph editor, no state machine. The model already knows how to pick the right tool; handoffs are just tools that return agents.

> 这是优雅的举措：复用模型现有的工具调用基础设施进行编排。没有新 DSL、没有图编辑器、没有状态机。模型已经知道如何选择正确的工具；交接只是返回 Agent 的工具。

### Why it is viral

- **Small API.** Two concepts to learn.
  中文翻译：**小型 API。** 只需学习两个概念。
- **Uses what the model already does.** Tool calling is already production-grade across providers.
  中文翻译：**使用模型已有的能力。** 工具调用在各提供商中已经是生产级。
- **No state-machine burden.** You do not describe the graph; the agents' prompts describe who they hand off to.
  中文翻译：**无状态机负担。** 你不描述图；Agent 的提示描述它们交接给谁。

### The stateless trade

Swarm is explicitly stateless between runs. The framework keeps a message history during a run, but it does not persist anything. Memory, continuity, long-running tasks — all the caller's problem.

> Swarm 在运行之间明确是无状态的。框架在运行期间保持消息历史，但不持久化任何东西。内存、连续性、长时间运行的任务——都是调用者的问题。

The stateless design is intentional: it makes the framework trivially restartable, horizontally scalable, and debuggable (every run is independent). The cost is that long-running workflows require external state management (databases, queues, checkpoints).

> 无状态设计是有意的：它使框架可轻松重启、水平扩展和可调试（每次运行独立）。代价是长时间运行的工作流需要外部状态管理（数据库、队列、检查点）。

In production (OpenAI Agents SDK, March 2025) this was one of the main things that changed: the SDK adds built-in session management, guardrails, and tracing while keeping the handoff primitive.

> 在生产环境中（OpenAI Agents SDK，2025 年 3 月），这是主要变化之一：SDK 添加了内置会话管理、防护栏和追踪，同时保留了交接原语。

### When Swarm/handoffs fit

- **Triage patterns.** Front-line agent routes user to a specialist.
  中文翻译：**分诊模式。** 前线 Agent 将用户路由到专家。
- **Skill-based handoffs.** "If the task needs code, call the coder; if it needs research, call the researcher."
  中文翻译：**基于技能的交接。** "如果任务需要编码，调用编码器；如果需要研究，调用研究员。"
- **Short, bounded conversations.** Customer support, FAQ-to-ticket, simple workflows.
  中文翻译：**短、有界对话。** 客户支持、FAQ 到工单、简单工作流。

### When Swarm struggles

- **Long sessions with shared memory.** Handoffs reset the conversation state to the new agent's prompt plus history. No persistent state across agents without caller-managed memory.
  中文翻译：**需要共享内存的长会话。** 交接将对话状态重置为新 Agent 的提示加历史。没有调用者管理的内存就没有跨 Agent 的持久状态。
- **Parallel execution.** Handoff is one-at-a-time — the active agent switches. Parallelism requires the caller orchestrating multiple Swarm runs.
  中文翻译：**并行执行。** 交接是逐一的——活动 Agent 切换。并行性需要调用者编排多个 Swarm 运行。
- **Audit and replay.** Stateless runs are hard to replay exactly; the LLM's handoff choice is not deterministic.
  中文翻译：**审计和回放。** 无状态运行难以精确回放；LLM 的交接选择不是确定性的。

### OpenAI Agents SDK (March 2025)

The production successor adds:

> 生产继任者添加了：

- **Session state.** Persistent thread across runs.
  中文翻译：**会话状态。** 跨运行的持久线程。
- **Guardrails.** Input/output validation hooks.
  中文翻译：**防护栏。** 输入/输出验证钩子。
- **Tracing.** Every tool call and handoff is logged.
  中文翻译：**追踪。** 每次工具调用和交接都被记录。
- **Handoff filters.** Control what context transfers on handoff.
  中文翻译：**交接过滤器。** 控制交接时传输什么上下文。

The handoff primitive survives; production ergonomics get added around it.

> 交接原语存活下来；生产人体工程学围绕它添加。

This is the standard progression for viral abstractions: simple primitive ships first (Swarm), production concerns layer on top (Agents SDK). The primitive stays stable; the wrappers grow. Bet on the primitive.

> 这是病毒式抽象的标准进展：先发布简单原语（Swarm），生产关注点在其上层叠（Agents SDK）。原语保持稳定；包装器增长。押注原语。

### Swarm vs GroupChat

Both use LLM-driven routing, but they differ on **who picks next**:

> 两者都使用 LLM 驱动的路由，但在**谁选择下一个**上不同：

- GroupChat: a selector (function or LLM) picks the next speaker from outside.
  中文翻译：GroupChat：选择器（函数或 LLM）从外部选择下一个发言者。
- Swarm: the current agent picks its successor by calling a handoff tool.
  中文翻译：Swarm：当前 Agent 通过调用交接工具选择其继任者。

Swarm is "agent decides what's next"; GroupChat is "manager decides what's next." Swarm's decision lives in the active agent's tool call; GroupChat's lives in the `GroupChatManager`.

> Swarm 是"Agent 决定下一步"；GroupChat 是"管理者决定下一步"。Swarm 的决策存在于活动 Agent 的工具调用中；GroupChat 的存在于 `GroupChatManager` 中。

Practical implication: Swarm is easier to debug (follow the active agent's tool calls) but harder to constrain (any agent can hand off anywhere). GroupChat is the opposite: easy to constrain (the selector function is one place to add rules), harder to debug (the selector's logic may be opaque).

> 实际影响：Swarm 更容易调试（跟踪活动 Agent 的工具调用）但更难约束（任何 Agent 可以交接任何地方）。GroupChat 相反：容易约束（选择器函数是添加规则的一个地方），更难调试（选择器的逻辑可能不透明）。

## Build It | 动手实现

`code/main.py` implements Swarm from scratch: an Agent dataclass, a handoff mechanism (tool returns Agent), and a run loop that detects agent switches.

> `code/main.py` 从头实现 Swarm：Agent 数据类、交接机制（工具返回 Agent）和检测 Agent 切换的运行循环。

Demo: a triage agent routes to refund, sales, or support specialists. Each specialist has its own tools. The run loop prints each handoff.

> 演示：分诊 Agent 路由到退款、销售或支持专家。每个专家有自己的工具。运行循环打印每次交接。

Run:

```
python3 code/main.py
```

## Use It | 用框架实现

`outputs/skill-handoff-designer.md` designs a handoff topology for a given task: which agents exist, which handoffs they can call, what context transfers.

> `outputs/skill-handoff-designer.md` 为给定任务设计交接拓扑：哪些 Agent 存在、它们可以调用哪些交接、什么上下文传输。

## Ship It | 产出物

Checklist:

> 检查清单：

- **Handoff logging.** Every handoff writes a trace event with from-agent, to-agent, context snapshot.
  中文翻译：**交接日志。** 每次交接写入跟踪事件，包含来自 Agent、到 Agent、上下文快照。
- **Context transfer rules.** Decide what moves on handoff: full history (expensive), last N messages, or a summary.
  中文翻译：**上下文传输规则。** 决定交接时传输什么：完整历史（昂贵）、最后 N 条消息或摘要。
- **Guardrail on handoff.** A handoff to a specialist with different tool permissions must be authenticated — otherwise prompt injection can force unwanted handoffs.
  中文翻译：**交接防护栏。** 交接到具有不同工具权限的专家必须被认证——否则提示注入可以强制不需要的交接。
- **Loop detection.** Two agents handing back and forth is a common failure; detect with a simple last-K ring check.
  中文翻译：**循环检测。** 两个 Agent 来回交接是常见失败；用简单的最近 K 次环形检查检测。
- **Fallback agent.** If a handoff target does not exist, fall back to a safe default.
  中文翻译：**后备 Agent。** 如果交接目标不存在，回退到安全默认值。

## Exercises | 练习题

1. Run `code/main.py`, triage to the refund agent. Confirm the second turn's active agent is refund.
   中文翻译：运行 `code/main.py`，分诊到退款 Agent。确认第二轮的活动 Agent 是退款。
2. Add a loop-detection rule: if the same two agents have handed off 3 times in a row, force an exit. Design the fallback.
   中文翻译：添加循环检测规则：如果相同的两个 Agent 连续交接 3 次，强制退出。设计后备方案。
3. Read the OpenAI Agents SDK docs on handoff filters. Implement a "summarize-on-handoff" version: the outgoing agent compresses context to a bullet summary before the incoming agent takes over.
   中文翻译：阅读 OpenAI Agents SDK 关于交接过滤器的文档。实现"交接时总结"版本：传出 Agent 在传入 Agent 接管之前将上下文压缩为要点摘要。
4. Compare the Swarm handoff to a GroupChatManager selector. Which pattern makes prompt injection worse, and why?
   中文翻译：比较 Swarm 交接与 GroupChatManager 选择器。哪种模式使提示注入更糟糕，为什么？
5. Read the Swarm cookbook. Identify one explicit design decision Swarm makes that OpenAI Agents SDK changed or kept.
   中文翻译：阅读 Swarm 手册。识别 Swarm 做出的一个明确设计决策，OpenAI Agents SDK 改变或保留了它。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Further Reading | 延伸阅读

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) — the reference articulation
  中文翻译：OpenAI 手册 — 编排 Agent：例程和交接 — 参考阐述
- [OpenAI Swarm repo](https://github.com/openai/swarm) — original implementation, kept as conceptual reference
  中文翻译：OpenAI Swarm 仓库 — 原始实现，保留为概念参考
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) — production successor with sessions and tracing
  中文翻译：OpenAI Agents SDK 文档 — 带会话和追踪的生产继任者
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) — how Claude Code subagents use a handoff-like pattern via `Task`
  中文翻译：Anthropic Claude 中的交接说明 — Claude Code 子 Agent 如何通过 `Task` 使用类似交接的模式
