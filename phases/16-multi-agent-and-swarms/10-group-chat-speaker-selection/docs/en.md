# Group Chat and Speaker Selection | 群聊 选择 发言者

> AutoGen GroupChat and AG2 GroupChat share one conversation across N agents; a selector function (LLM, round-robin, or custom) picks who speaks next. This is the archetype of emergent multi-agent conversation — agents do not know their role in a static graph, they just react to the shared pool. AutoGen v0.2's GroupChat semantics were preserved in the AG2 fork; AutoGen v0.4 rewrote it as an event-driven actor model. Microsoft put AutoGen into maintenance mode in February 2026 and merged it with Semantic Kernel into Microsoft Agent Framework (RC February 2026). The GroupChat primitive survives in both AG2 and Microsoft Agent Framework — learn it once, use it everywhere.

> **【中文解读】** 本节介绍了群聊发言者选择——多 Agent 讨论中决定谁发言、何时发言的机制。

> **【拓展：group chat speaker selection→具体应用】** 群聊发言者选择是多 Agent 讨论中的关键问题——谁发言、什么时候发言、发言多久。三种主要策略：(1) 轮流制——按固定顺序发言；(2) 相关性制——最相关的 Agent 发言；(3) 仲裁制——一个专门的协调者决定谁发言。AutoGen 的 GroupChat 使用 LLM 作为仲裁者。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·04（原语模型）、AutoGen 基础。群聊 = N 个 Agent 共享一个对话池，发言者选择决定谁说话。
> 💡 **【类比】** 群聊发言者选择 = "会议主持"。轮流制 = 圆桌按序；相关性制 = 谁懂谁说；仲裁制 = 主持人指定。AutoGen GroupChat 用 LLM 当主持人——成本高但灵活。2026 注意：AutoGen 已被微软合并到 Microsoft Agent Framework，AG2 是社区 fork，两者都保留 GroupChat 原语。

## Problem | 问题引入

Static graphs (LangGraph) are great when the workflow is known. Real conversations are not static: sometimes the coder asks the reviewer, sometimes the researcher, sometimes the writer. Hardcoding every possible handoff produces an edge explosion. You want *agents reacting to a shared pool*, with some function deciding who talks next.

> 静态图（LangGraph）在工作流已知时很好。真实对话不是静态的：有时编码器问审阅者，有时问研究员，有时问写作者。硬编码每个可能的交接会产生边爆炸。你想要*Agent 对共享池做出反应*，由某个函数决定谁下一个发言。

The edge-explosion problem is real: a 5-agent system with all possible handoffs has 25 directed edges. Add a sixth agent and you have 36. The graph approach does not scale to emergent conversations; you need a pool.

> 边爆炸问题是真实的：带所有可能交接的 5 Agent 系统有 25 条有向边。添加第六个 Agent 就有 36 条。图方法不能扩展到涌现对话；你需要池。

That is exactly what AutoGen GroupChat does.

> 这正是 AutoGen GroupChat 所做的。

## Concept | 核心概念

### The shape

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Every agent sees every message. A selector function is invoked at each turn to pick who speaks next.

> 每个 Agent 看到每条消息。每轮调用选择器函数来选择下一个发言者。

The full-transparency pool is both the strength and weakness of GroupChat. Strength: any agent can react to anything anyone said. Weakness: after 20 turns, every agent's context is huge, expensive, and diluted. Mitigations: project scoped views per agent (Lesson 15) or terminate early.

> 完全透明的池既是 GroupChat 的优势也是弱点。优势：任何 Agent 可以对任何人说的任何事做出反应。弱点：20 轮后，每个 Agent 的上下文巨大、昂贵且稀释。缓解措施：为每个 Agent 投影范围视图（Lesson 15）或提前终止。

### The three selector flavors

**Round-robin.** Fixed cycle. Deterministic. Scales linearly in N but ignores context — a coder gets the turn even when the topic is legal review.

> **轮询。** 固定循环。确定性。按 N 线性扩展但忽略上下文——即使主题是法务审阅，编码器也能获得发言权。

**LLM-selected.** A call to an LLM that reads the recent pool and returns the best next speaker. Context-aware but slow: every turn adds an LLM call. AutoGen's default.

> **LLM 选择。** 调用 LLM 读取最近的池并返回最佳下一个发言者。上下文感知但慢：每轮增加一次 LLM 调用。AutoGen 的默认选择。

**Custom.** A Python function with whatever logic you want. Typical: LLM-selected with fallback rules (e.g., "always give the verifier the turn after the coder").

> **自定义。** 一个 Python 函数，使用你想要的任何逻辑。典型：LLM 选择带回退规则（例如，"总是在编码器之后给验证者发言权"）。

### The ConversableAgent API

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager` holds the selector. When an agent completes a turn, the manager calls the selector, which returns the next agent. Loop continues until a termination condition.

> `GroupChatManager` 持有选择器。当 Agent 完成一轮时，管理者调用选择器，返回下一个 Agent。循环继续直到终止条件。

The selector function is the heart of GroupChat. Swap it out, change the orchestration style. Round-robin selector = deterministic. LLM selector = adaptive. Custom selector = whatever rules you encode. Same primitives, different orchestration.

> 选择器函数是 GroupChat 的核心。换掉它，改变编排风格。轮询选择器 = 确定性。LLM 选择器 = 自适应。自定义选择器 = 你编码的任何规则。相同原语，不同编排。

### Termination

Three common patterns:

> 三种常见模式：

- **Max rounds.** Hard cap on total turns.
  中文翻译：**最大轮数。** 总轮数的硬上限。
- **"TERMINATE" token.** Agents can emit a sentinel message; the manager stops when one appears.
  中文翻译：**"TERMINATE" 标记。** Agent 可以发出哨兵消息；管理者在出现时停止。
- **Goal-reached check.** A lightweight verifier runs each turn and stops the chat when done.
  中文翻译：**目标达成检查。** 轻量级验证者每轮运行并在完成时停止聊天。

### The AutoGen -> AG2 split and the Microsoft Agent Framework merge

In early 2025, Microsoft began a major rewrite of AutoGen (v0.4) around an event-driven actor model. The community forked AutoGen v0.2's GroupChat semantics as AG2, preserving the API that early adopters had integrated.

> 2025 年初，微软开始围绕事件驱动 actor 模型对 AutoGen (v0.4) 进行重大重写。社区将 AutoGen v0.2 的 GroupChat 语义分叉为 AG2，保留了早期采用者已集成的 API。

The fork was necessary because v0.4 broke backward compatibility in fundamental ways. AG2 keeps the original `GroupChat`, `ConversableAgent`, and `GroupChatManager` API stable, while v0.4 introduces new event-driven primitives. Both lines are actively maintained as of 2026.

> 分叉是必要的，因为 v0.4 在基本方面破坏了向后兼容性。AG2 保持原始 `GroupChat`、`ConversableAgent` 和 `GroupChatManager` API 稳定，而 v0.4 引入新的事件驱动原语。截至 2026 年，两条线都积极维护。

In February 2026, Microsoft announced AutoGen would go to maintenance mode, with the event-driven actor model merging into **Microsoft Agent Framework** (RC February 2026, now merged with Semantic Kernel). The GroupChat concept survives in both tracks; the implementation details differ. AG2 is the preferred upstream for v0.2-compatible code.

> 2026 年 2 月，微软宣布 AutoGen 进入维护模式，事件驱动 actor 模型合并到 **Microsoft Agent Framework**（2026 年 2 月 RC，现已与 Semantic Kernel 合并）。GroupChat 概念在两个轨道中存活；实现细节不同。AG2 是 v0.2 兼容代码的首选上游。

The lesson: API surface outlasts frameworks. Code written against AutoGen v0.2's GroupChat API in 2024 still runs unchanged via AG2 in 2026. Frameworks churn; the primitives (shared pool + selector) do not. Bet on the primitives.

> 教训：API 表面比框架持久。2024 年针对 AutoGen v0.2 GroupChat API 编写的代码在 2026 年通过 AG2 仍然不变运行。框架变化；原语（共享池 + 选择器）不变。押注原语。

### When GroupChat fits

- **Emergent conversations.** You do not want to pre-wire every possible next-speaker.
  中文翻译：**涌现对话。** 你不想预先连接每个可能的下一个发言者。
- **Role-mixing tasks.** Coder asks researcher, researcher asks archivist, archivist asks coder back. Flow is not a DAG.
  中文翻译：**角色混合任务。** 编码器问研究员，研究员问档案员，档案员反问编码器。流程不是 DAG。
- **Exploratory problem-solving.** Think "brainstorm meeting," not "assembly line."
  中文翻译：**探索性问题解决。** 想想"头脑风暴会议"，而不是"装配线"。

### When it fails

- **Strict determinism.** The LLM selector can be inconsistent. Same prompt, different runs, different next speakers.
  中文翻译：**严格确定性。** LLM 选择器可能不一致。相同提示，不同运行，不同下一个发言者。
- **Sycophancy cascades.** Agents defer to whoever spoke most confidently. Counter-prompt explicitly.
  中文翻译：**谄媚级联。** Agent 屈从于最自信的发言者。明确反提示。
- **Context bloat.** Every agent reads every message; after 10 turns the context is huge. Use projections (Lesson 15) to scope views.
  中文翻译：**上下文膨胀。** 每个 Agent 读取每条消息；10 轮后上下文巨大。使用投影（Lesson 15）来限定视图。
- **Hot speakers.** One agent dominates the conversation because the selector favors its specialties. Introduce speaker balance as a selector feature.
  中文翻译：**热发言者。** 一个 Agent 主导对话，因为选择器偏向其专长。引入发言者平衡作为选择器特性。

### Group chat vs supervisor

Same primitives, different defaults:

> 相同原语，不同默认值：

- Supervisor: one agent plans and others execute. Selector is "ask the planner what to do."
  中文翻译：监督者：一个 Agent 规划，其他执行。选择器是"问规划者做什么。"
- Group chat: all agents are peers; selector is a function over the shared pool.
  中文翻译：群聊：所有 Agent 是对等的；选择器是共享池上的函数。

Both use the four primitives from Lesson 04. Group chat defaults to LLM-selected orchestration and full-pool shared state.

> 两者都使用 Lesson 04 的四个原语。群聊默认使用 LLM 选择的编排和全池共享状态。

The choice between supervisor and group chat is mostly about *who holds the plan*. Supervisor: one agent owns the plan and delegates. Group chat: the plan is implicit, emergent from the conversation. The first is more controllable; the second is more flexible.

> 监督者和群聊之间的选择主要是关于*谁持有计划*。监督者：一个 Agent 拥有计划并委派。群聊：计划是隐式的，从对话中涌现。前者更可控；后者更灵活。

## Build It | 动手实现

`code/main.py` implements a GroupChat from scratch in stdlib. Three agents (coder, reviewer, manager), round-robin and LLM-selected variants, and a termination on a `TERMINATE` token.

> `code/main.py` 用标准库从头实现一个 GroupChat。三个 Agent（编码器、审阅者、管理者），轮询和 LLM 选择变体，以及在 `TERMINATE` 标记上终止。

The demo prints the conversation transcript plus the selector's decision trace for both variants.

> 演示打印对话记录以及两种变体的选择器决策追踪。

## Use It | 用框架实现

`outputs/skill-groupchat-selector.md` configures a GroupChat selector for a given task — round-robin vs LLM-selected vs custom, and what selector inputs (recent messages, agent specialties, turn counts) to use.

> `outputs/skill-groupchat-selector.md` 为给定任务配置 GroupChat 选择器——轮询 vs LLM 选择 vs 自定义，以及使用什么选择器输入（最近消息、Agent 专长、轮次计数）。

## Ship It | 产出物

Checklist:

> 检查清单：

- **Max rounds cap.** Always. 10-20 for typical tasks.
  中文翻译：**最大轮数上限。** 总是使用。典型任务 10-20。
- **Speaker-balance metric.** Track turns per agent; alert when imbalance exceeds a threshold.
  中文翻译：**发言者平衡指标。** 跟踪每个 Agent 的轮次；当不平衡超过阈值时告警。
- **Termination token.** `TERMINATE` or a dedicated verifier agent.
  中文翻译：**终止标记。** `TERMINATE` 或专门的验证者 Agent。
- **Projection or scoped memory.** After ~10 messages, consider giving each agent only a scoped view to prevent context bloat.
  中文翻译：**投影或范围内存。** 约 10 条消息后，考虑给每个 Agent 只一个范围视图以防止上下文膨胀。
- **Selector logging.** For LLM-selected variants, log both the selector's input and its choice. Otherwise debugging is impossible.
  中文翻译：**选择器日志。** 对于 LLM 选择变体，记录选择器的输入和选择。否则调试不可能。

## Exercises | 练习题

1. Run `code/main.py`. Compare the conversation under round-robin vs LLM-selected. Which agent dominates under each?
   中文翻译：运行 `code/main.py`。比较轮询 vs LLM 选择下的对话。每种模式下哪个 Agent 占主导？
2. Add a "max-speaks-per-agent" rule in the selector. How does it affect the transcript?
   中文翻译：在选择器中添加"每个 Agent 最大发言次数"规则。它如何影响记录？
3. Implement a goal-reached termination: stop when the reviewer returns "approved." How often does it trigger before the round cap?
   中文翻译：实现目标达成终止：当审阅者返回"approved"时停止。它在轮数上限之前多久触发？
4. Read the AutoGen stable docs on GroupChat. Identify the default selector used by `GroupChatManager`.
   中文翻译：阅读 AutoGen 稳定文档中的 GroupChat。识别 `GroupChatManager` 使用的默认选择器。
5. Read the AG2 repo and compare its v0.2 GroupChat to the v0.4 event-driven version. What concrete property (throughput, fault-tolerance, composability) does v0.4 add?
   中文翻译：阅读 AG2 仓库并比较其 v0.2 GroupChat 与 v0.4 事件驱动版本。v0.4 添加了什么具体属性（吞吐量、容错、可组合性）？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Further Reading | 延伸阅读

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) — the reference implementation
  中文翻译：AutoGen 群聊文档 — 参考实现
- [AG2 repo](https://github.com/ag2ai/ag2) — community AutoGen v0.2 continuation
  中文翻译：AG2 仓库 — 社区 AutoGen v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) — the merged successor, RC February 2026
  中文翻译：Microsoft Agent Framework 文档 — 合并后的继任者，2026 年 2 月 RC
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) — event-driven actor model rewrite details
  中文翻译：AutoGen v0.4 发布说明 — 事件驱动 actor 模型重写详情
