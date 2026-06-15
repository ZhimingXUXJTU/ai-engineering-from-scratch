# Long-Running Background Agents: Durable Execution | 长时后台 Agent：持久执行

> Production long-horizon agents do not run in `while True`. Every LLM call becomes an activity with checkpoint, retry, and replay. Temporal's OpenAI Agents SDK integration went GA March 2026. Claude Code Routines (Anthropic) runs scheduled Claude Code invocations without a persistent local process. Sessions pause on human-input, survive deploys, and resume from the latest checkpoint keyed by `thread_id`. Behind the new ergonomics sits an old pattern — workflow orchestration — with one new input: LLM calls as non-deterministic activities that must be deterministically replayed on recovery.

> **【中文解读】** 生产长程 Agent 不在 `while True` 中运行。每个 LLM 调用成为带检查点、重试和重放的活动。Temporal 的 OpenAI Agents SDK 集成于 2026 年 3 月 GA。Claude Code Routines（Anthropic）在无持久本地进程的情况下运行调度 Claude Code 调用。会话在人类输入时暂停、跨部署存活、从最新检查点恢复。新的工效学背后是旧模式——工作流编排——和一个新输入：LLM 调用作为必须在恢复时确定性重放的非确定性活动。

> **【拓展：LLM 调用 = 活动的精确契合】** LLM 调用完美匹配活动特征：非确定性（temperature > 0）、昂贵（金钱和延迟）、可能失败（速率限制、超时）、有副作用（调用工具）。把每个 LLM 调用包装为活动即可获得指数退避重试、跨重启检查点和可重放调试追踪。这就是为什么 Temporal、LangGraph、Cloudflare Durable Objects、Claude Code Routines 全部收敛到同一 API 形态——`thread_id` + 后端存储 + 最近检查点恢复。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

> **【中文解读】** 持久执行确保 Agent 任务在故障后能恢复。传统 Agent 在内存中运行，进程崩溃意味着从头开始。持久执行将状态保存到外部存储（数据库、文件系统），任何时刻都可以从最近的检查点恢复。Temporal 和 LangGraph 是实现持久执行的两个主流框架。

> **【拓展：durable execution】** 持久执行对长时间运行的 Agent 至关重要。如果一个需要运行 2 小时的 Agent 在第 90 分钟崩溃，没有持久执行就意味着重新开始。Temporal 通过事件溯源实现持久工作流，LangGraph 通过检查点实现持久状态图。2026 年的最佳实践是每个重要步骤后自动保存检查点。

Consider an agent that runs for four hours. It calls three tools, prompts the user twice, and makes forty LLM calls. Halfway through, the host it is running on reboots.

> 考虑一个运行四小时的 Agent。它调用三个工具、提示用户两次、进行 40 次 LLM 调用。中途，运行它的主机重启了。

What happens?

> 会发生什么？

- In a naive `while True` loop: everything is lost. The run restarts from scratch. The three tool calls (with real side effects) execute again. The user is prompted again for things they already approved. Forty LLM calls are re-billed.
  中文翻译：在朴素 `while True` 循环中：一切丢失。运行从头重启。三个工具调用（带真实副作用）再次执行。用户再次被提示已批准的事。40 个 LLM 调用重新计费。
- With durable execution: the run resumes from the most recent checkpoint. Already-completed activities are not re-executed; their results are replayed from the durable log. The user does not re-approve things they already approved. The LLM calls already made are not re-billed.
  中文翻译：有持久执行时：运行从最近检查点恢复。已完成活动不重新执行；其结果从持久日志重放。用户不重新批准已批准的事。已做的 LLM 调用不重新计费。

This is the same pattern workflow engines have shipped for a decade (Temporal, Cadence, Uber's Cherami). What's new is that LLM calls are now a kind of activity — non-deterministic, expensive, with side effects — and they fit this pattern cleanly.

> 这是工作流引擎出货十年的相同模式（Temporal、Cadence、Uber 的 Cherami）。新的是 LLM 调用现在是一种活动——非确定性、昂贵、有副作用——它们干净地契合此模式。

> **【中文解读】** 持久化执行解决长程 Agent 的可靠性问题：四小时运行中主机重启时，朴素循环丢失一切（工具重新执行、用户重新审批、LLM 重新计费），而持久化执行从最近的检查点恢复，已完成的活动从持久日志重放而非重新执行。Temporal 的 OpenAI Agents SDK 集成于 2026 年 3 月 GA。核心洞察：LLM 调用是一种非确定性、昂贵、有副作用的活动，完美适配工作流引擎的模式。

The running theme of the lesson: long-horizon reliability decays (METR observes a "35-minute degradation" — success rate drops roughly quadratically with horizon). Durable execution enables runs that are longer than the reliability profile supports, which is a new way to fail safely if the design is right and unsafely if the design is wrong.

> 本课的运行主题：长程可靠性衰减（METR 观察到"35 分钟衰减"——成功率与时间线大致平方反比下降）。持久执行启用比可靠性档案支持的更长运行，这是设计正确时安全失败、设计错误时不安全失败的新方式。

## The Concept | 核心概念

### Activities, workflows, and replay | 活动、工作流和重放

- **Workflow**: deterministic orchestration code. Defines the sequence of activities, the branches, the waits. Must be deterministic so it can be replayed from the event log without surprising divergence.
  中文翻译：**工作流**：确定性编排代码。定义活动序列、分支、等待。必须确定性以便能从事件日志重放而无意外分歧。
- **Activity**: a non-deterministic, potentially failing unit of work. LLM call, tool call, file write, HTTP request. Each activity is logged with its inputs and (once complete) its outputs.
  中文翻译：**活动**：非确定性、可能失败的工作单元。LLM 调用、工具调用、文件写、HTTP 请求。每个活动记录其输入和（完成时）输出。
- **Event log**: the durable backing store. Every activity start, complete, fail, retry, and every workflow decision is recorded.
  中文翻译：**事件日志**：持久后端存储。每个活动开始、完成、失败、重试和每个工作流决策被记录。
- **Replay**: on recovery, the workflow code re-runs from the start; every activity that already completed returns its logged result without re-executing. Only activities that had not completed are actually run.
  中文翻译：**重放**：恢复时，工作流代码从头重跑；每个已完成活动返回其记录结果而不重新执行。只有未完成的活动实际运行。

This is the same shape as React re-rendering against a virtual DOM, or Git rebuilding a working tree from commits. Determinism in the orchestrator is what makes durability cheap.

> 这与 React 针对虚拟 DOM 重渲染或 Git 从提交重建工作树的形状相同。编排器的确定性使持久性廉价。

### Why LLM calls fit the pattern | 为什么 LLM 调用契合此模式

LLM calls are:

> LLM 调用是：

- Non-deterministic (temperature > 0; even temperature 0 drifts across model versions).
  中文翻译：非确定性（temperature > 0；即使 temperature 0 跨模型版本漂移）。
- Expensive (money and latency).
  中文翻译：昂贵（金钱和延迟）。
- Potentially failing (rate limits, timeouts).
  中文翻译：可能失败（速率限制、超时）。
- Side-effectful (if they invoke tools).
  中文翻译：有副作用（如果调用工具）。

This is exactly the activity profile. Wrapping every LLM call as an activity gives you retry with exponential backoff, checkpointing across restarts, and a replayable trace for debugging.

> 这正是活动档案。将每个 LLM 调用包装为活动给你指数退避重试、跨重启检查点和可重放调试追踪。

### Checkpoints keyed by `thread_id` | 以 `thread_id` 为键的检查点

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects, and Claude Code Routines all converged on the same API shape: a `thread_id` (or equivalent) identifies the session; each state transition persists to a backend (PostgreSQL default, SQLite for dev, Redis for cache); resume reads the latest checkpoint.

> LangGraph、Microsoft Agent Framework、Cloudflare Durable Objects 和 Claude Code Routines 都收敛到同一 API 形态：`thread_id`（或等价物）识别会话；每个状态转换持久化到后端（默认 PostgreSQL、dev 用 SQLite、缓存用 Redis）；恢复读最新检查点。

The backend choice matters:

> 后端选择重要：

- **PostgreSQL**: durable, queryable, survives deploys. Default for LangGraph.
  中文翻译：**PostgreSQL**：持久、可查询、跨部署存活。LangGraph 默认。
- **SQLite**: local-dev only; loses data across hosts.
  中文翻译：**SQLite**：仅本地开发；跨主机丢数据。
- **Redis**: fast but ephemeral unless AOF/snapshot configured.
  中文翻译：**Redis**：快但临时，除非配置 AOF/快照。
- **Cloudflare Durable Objects**: transparently distributed; scoped by a unique key; survives for hours to weeks.
  中文翻译：**Cloudflare Durable Objects**：透明分布式；以唯一键为范围；存活数小时到数周。

### Human-input as a first-class state | 人类输入作为一等公民状态

Propose-then-commit (Lesson 15) requires a durable "waiting on human" state. The workflow pauses, the external queue holds the pending request, and an approval resumes from exactly that point. Without durability this is best-effort; with it, an overnight approval arrives and the workflow picks up in the morning.

> Propose-then-commit（第 15 课）需要持久"等待人类"状态。工作流暂停，外部队列持有挂起请求，批准从该精确点恢复。无持久性时这是尽力而为；有持久性时，隔夜批准到达，工作流早上拾起。

### The 35-minute degradation | 35 分钟衰减

METR observed that every agent class measured shows reliability decay beyond ~35 minutes of continuous operation.

> METR 观察到每个测量的 Agent 类别在约 35 分钟连续运行后都显示可靠性衰减。

Doubling the task duration roughly quadruples the failure rate. Durable execution does not fix this; it lets you run longer than the reliability profile supports. The safe pattern is to combine durability with checkpoints that require fresh HITL on re-entry, and with budget kill switches (Lesson 13) that cap total compute regardless of wall-clock time.

> 任务时长翻倍大致使失败率四倍。持久执行不修复此；它让你跑得比可靠性档案支持的更久。安全模式是将持久性与重新进入时需新鲜 HITL 的检查点结合，与不论墙钟时间封顶总计算的预算终止开关（第 13 课）结合。

### When durable execution is the wrong answer | 持久执行不是答案时

- Runs shorter than a few minutes with no human input. Overhead > benefit.
  中文翻译：短于几分钟无人类输入的运行。开销 > 收益。
- Strictly read-only information retrieval.
  中文翻译：严格只读信息检索。
- Tasks where correctness requires end-to-end within one context window (some reasoning tasks; some one-shot generation).
  中文翻译：正确性需在一个上下文窗口内端到端的任务（某些推理任务；某些一次性生成）。

## Use It | 用框架实现

`code/main.py` implements a minimal durable-execution engine in stdlib Python. It supports:

> `code/main.py` 用标准库 Python 实现最小持久执行引擎。它支持：

- `@activity` decorator that logs inputs and outputs to a JSON event log.
  中文翻译：`@activity` 装饰器将输入输出记录到 JSON 事件日志。
- A workflow function that sequences activities.
  中文翻译：将活动排序的工作流函数。
- A `run_or_replay(workflow, event_log)` function that replays completed activities without re-executing them.
  中文翻译：`run_or_replay(workflow, event_log)` 函数重放已完成活动而不重新执行。

The driver simulates a three-activity workflow, crashes halfway through, and shows (a) a naive retry re-executing everything versus (b) a replay running only the missing activity.

> 驱动器模拟三活动工作流，中途崩溃，展示 (a) 朴素重试重新执行一切 vs (b) 重放只运行缺失活动。

## Ship It | 产出物

`outputs/skill-durable-execution-review.md` reviews a proposed long-running agent deployment for correct durable-execution shape: activities, determinism, checkpoint backend, human-input state, and HITL-on-resume policy.

> `outputs/skill-durable-execution-review.md` 审查提议的长时运行 Agent 部署的正确持久执行形状：活动、确定性、检查点后端、人类输入状态和恢复时 HITL 策略。

## Exercises | 练习题

1. Run `code/main.py`. Observe the difference in activity-execution count between naive retry and replay. Change the crash point and show the replay count changes accordingly.
   中文翻译：运行 `code/main.py`。观察朴素重试和重放间活动执行计数差异。改变崩溃点并展示重放计数相应变化。

2. Convert the toy engine to use `thread_id` explicitly. Simulate two concurrent sessions sharing the engine and confirm their event logs do not collide.
   中文翻译：将玩具引擎转为显式使用 `thread_id`。模拟共享引擎的两个并发会话并确认其事件日志不冲突。

3. Take one activity in the toy engine. Introduce a non-determinism (a wall-clock timestamp inside a workflow decision). Demonstrate the divergence on replay. Explain how real engines handle this (side-effect registration, `Workflow.now()` APIs).
   中文翻译：在玩具引擎中取一个活动。引入非确定性（工作流决策内的墙钟时间戳）。演示重放上的分歧。解释真实引擎如何处理（副作用注册、`Workflow.now()` API）。

4. Read the LangChain "Runtime behind production deep agents" post. List every state that the runtime persists and name which failure mode each covers.
   中文翻译：阅读 LangChain 的"Runtime behind production deep agents"文章。列出运行时持久化的每个状态并命名各覆盖的失败模式。

5. Design a checkpoint policy for a 6-hour autonomous coding task. Where do you checkpoint? What does resume-on-crash look like? What requires fresh HITL?
   中文翻译：为 6 小时自主编码任务设计检查点策略。你在哪检查点？崩溃恢复什么样？什么需新鲜 HITL？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Further Reading | 延伸阅读

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) — budget, turns, and resume semantics.
  中文翻译：预算、轮次和恢复语义。
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — RequestInfoEvent shape.
  中文翻译：RequestInfoEvent 形态。
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) — concrete runtime requirements.
  中文翻译：具体运行时要求。
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) — activity shape for LLM calls.
  中文翻译：LLM 调用的活动形态。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — the 35-minute degradation reference.
  中文翻译：35 分钟衰减参考。
