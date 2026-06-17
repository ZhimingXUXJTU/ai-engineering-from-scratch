# Production Scaling — Queues, Checkpoints, Durability | 检查点 生产 扩展 队列

> Scaling multi-agent systems to thousands of concurrent runs requires **durable execution**. LangGraph's runtime writes a checkpoint after each super-step keyed by `thread_id` (Postgres by default); worker crashes release a lease and another worker resumes. Agents can sleep indefinitely waiting for human input. **MegaAgent** (arXiv:2408.09955) ran a per-agent producer-consumer queue with three states (Idle / Processing / Response) and two-layer coordination (intra-group chat + inter-group admin chat). **Fiber/async** beats thread-per-job for LLM streaming: threads sit idle 99% of the time waiting for tokens, fibers cooperatively yield on I/O. Counterpoint: Ashpreet Bedi's "Scaling Agentic Software" argues for **FastAPI + Postgres + nothing else** until load proves otherwise — simple architectures go further than expected. This lesson builds a durable checkpoint log, a per-agent work queue with state transitions, an async-vs-thread demo, and lands the pragmatic "start simple" rule.

> **【中文解读】** 本节介绍了多 Agent 系统的生产扩展——队列、检查点和扩展策略。

> **【拓展：production scaling queues checkpoints→具体应用】** 多 Agent 系统的生产扩展需要：(1) 消息队列——Kafka/RabbitMQ 缓冲 Agent 间的消息；(2) 检查点——定期保存系统状态以支持恢复；(3) 负载均衡——将任务均匀分配给可用的 Agent 实例；(4) 水平扩展——动态增减 Agent 数量应对负载变化。LangGraph Cloud 和 Temporal 是这一领域的两个主流选择。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `asyncio`, `sqlite3`) | **语言:** Python（标准库，`asyncio`，`sqlite3`）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 13（共享内存）

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·09（Swarm）、Phase 16·13（共享内存）、Phase 15·12（Durable Execution）、异步编程（asyncio）。多 Agent 生产扩展 = 分布式系统工程问题。
> 💡 **【类比】** 多 Agent 扩展 = "外卖平台架构"。检查点（thread_id+Postgres）= 订单状态存档；消息队列 = 餐厅订单系统；fiber/async > thread-per-job = 协程比线程适合 I/O 密集（99% 时间等 token）。务实建议：FastAPI + Postgres + 啥都不加，先跑起来。简单架构往往比预期走得远。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

A prototype multi-agent system works on one laptop with three agents in an in-memory event loop. You move to production:

> 原型多 Agent 系统在一台笔记本电脑上用三个 Agent 在内存事件循环中运行。你转向生产环境：

- Agents sometimes run for hours (long research, human-in-the-loop waits).
  中文翻译：Agent 有时运行数小时（长时间研究、人在环等待）。
- Worker processes crash. Restarting loses state.
  中文翻译：工作者进程崩溃。重启丢失状态。
- Peak load is 10x average; you need horizontal scaling.
  中文翻译：峰值负载是平均的 10 倍；你需要水平扩展。
- Users pay per agent-run; you need exactly-once semantics for charging.
  中文翻译：用户按 Agent 运行付费；你需要恰好一次的计费语义。

The in-memory event loop does none of these. You need a durable execution layer underneath. The 2026 canonical options are:

> 内存事件循环这些都做不到。你需要一个持久执行层。2026 年规范选择是：

1. A workflow engine with checkpoints (Temporal, LangGraph runtime).
   中文翻译：带检查点的工作流引擎（Temporal、LangGraph 运行时）。
2. A message queue with a state store (Postgres + SQS/RabbitMQ).
   中文翻译：带状态存储的消息队列（Postgres + SQS/RabbitMQ）。
3. Actor-model frameworks (MegaAgent's producer-consumer per agent).
   中文翻译：Actor 模型框架（MegaAgent 的每 Agent 生产者-消费者）。
4. Hand-rolled FastAPI + Postgres (Bedi's argument).
   中文翻译：手工搭建的 FastAPI + Postgres（Bedi 的论点）。

This lesson builds a miniature of each.

> 本课构建每个的微型版本。

## Concept | 核心概念

### Durable execution, the pattern

A durable-execution engine persists the full program state after each "step" (super-step, in LangGraph's language). On crash:

```
worker crashes mid-step
  -> lease timeout
  -> another worker picks up the thread_id
  -> resumes from last checkpoint
  -> no duplicate side effects
```

Requirements for this to work:

- **Serializable state.** All agent state has to be persistable. Function closures with live database connections do not survive.
- **Deterministic resume.** Given the same state and same inputs, the agent produces the same actions (or defers to an external deterministic oracle for LLM calls).
- **Idempotent side effects.** External calls (tool calls, payments) must be idempotent or use a deduplication key.

LangGraph writes a checkpoint after each super-step; Temporal writes after each activity; Restate uses event-sourced journals. All three implement the same pattern.

### LangGraph's runtime

Each agent has a `thread_id`; state is a typed dict; each super-step writes a row to the checkpoints table. On resume, the runtime replays from the last checkpoint, not from scratch. Agents can `interrupt()` waiting for human input; the runtime persists and releases the worker. When input arrives, any worker can resume.

This is the reference production design in April 2026.

### MegaAgent's per-agent queue

arXiv:2408.09955 describes a scale experiment: thousands of concurrent agents in one cluster. Architecture:

```
agent i:
  state ∈ {Idle, Processing, Response}
  in_queue   <- messages addressed to agent i
  out_queue  -> replies + side effects

coordinators:
  intra-group chat  (agents in the same group)
  inter-group admin chat  (high-level routing)
```

The two-layer coordination lets intra-group conversation happen densely while inter-group stays sparse — the pattern used for keeping cost linear in thousands of agents.

### Async vs thread-per-job

LLM calls are I/O-bound. A thread waiting for the next token is idle 99% of the time. Threads cost ~1MB RAM each; at 10,000 concurrent calls, that is 10GB just for stacks.

Fibers (Python `asyncio`, Go goroutines, Rust `tokio`) cooperatively yield on I/O. The same 10,000 calls fit comfortably in process. At LLM-agent scale, async is not an optimization — it is the architecture.

Exception: CPU-bound post-processing (embedding, tokenizer tricks) still wants threads or processes. Separate your I/O layer from your CPU layer.

### Bedi's counterpoint

"Scaling Agentic Software" (Ashpreet Bedi, 2026) argues that most teams over-engineer before they have measured load. The pragmatic default:

- FastAPI + Postgres.
- Each agent run is a row; state updated in-place with optimistic concurrency.
- Background jobs via `pg_notify` or a simple Celery worker.
- Retry policy in application code.

For loads under ~100 concurrent agent-runs on manageable tasks, this is often all you need. Upgrade when you measure it failing.

The rule: adopt durable-execution frameworks when you hit a concrete problem that simple architectures cannot solve. Premature adoption burns time on ceremonies that do not pay off.

### Exactly-once semantics

For paid agent runs, you need "exactly-once effective" (at-least-once delivery + idempotent consumer). The engineering moves:

- **Dedup key per run.** Include it in every side-effect call.
- **Outbox pattern.** Side effects write to a table first, then a separate process executes them. Both steps idempotent.
- **Compensating transactions.** When a side effect succeeds but its tracking write fails, schedule a compensate.

These are database-engineering patterns, not LLM-specific. The LLM tax is only that LLM calls are slow; everything else is standard distributed systems.

### Rainbow deployment

Anthropic's multi-agent research system uses "rainbow deployments": multiple versions of the agent runtime run concurrently so long-running agents do not have to be killed on every code deploy. Canary new versions on a slice of traffic; retire old versions when their agents finish.

This is standard for long-running stateful systems; the 2026 adaptation is that agents can live for hours, so deployment cycles must accommodate.

### The canonical production checklist

- Durable state (checkpoints, snapshots, or outbox + replayable log).
- Idempotent side effects.
- Async I/O layer for LLM calls.
- At-least-once delivery with dedup.
- Rainbow/canary deployment for stateful workloads.
- Observability: per-agent traces, super-step audit, retry counter.

## Build It | 动手构建

`code/main.py` implements:

- `CheckpointStore` — SQLite-backed checkpoint log with thread-id keys. Each super-step appends a row.
- `run_with_checkpoint(agent, thread_id)` — simulates a crash mid-run; a second worker resumes from last checkpoint.
- `AgentQueue` — per-agent Idle / Processing / Response state machine with a small work queue.
- `demo_async_vs_threads()` — runs 500 concurrent simulated "LLM calls" via asyncio and via threads; reports wall-clock and peak memory (approximated).

Run:

```
python3 code/main.py
```

Expected output: checkpoint resume succeeds after simulated crash; async version handles 500 concurrent calls in < 1s; thread version takes several seconds and uses orders of magnitude more memory per concurrent unit.

## Use It | 使用方法

`outputs/skill-scaling-advisor.md` advises on durable-execution choice: FastAPI + Postgres, LangGraph runtime, Temporal, or custom. Calibrated by load, state-retention needs, and deploy frequency.

## Ship It | 部署上线

Canonical production hardening:

- **Start simple (Bedi's rule).** FastAPI + Postgres until you measure it failing.
- **Instrument everything before optimizing.** Per-run latency histogram, per-step time, retry count, failure categorization.
- **Outbox pattern for side effects.** Especially payments and external API calls.
- **Rainbow deploys.** Never kill in-flight agent runs during deploys.
- **Adopt durable-execution engines (Temporal / LangGraph / Restate) when** you hit specific problems: hour-long human-in-the-loop waits, cross-region coordination, complex retry/compensation policies.
- **Async for the I/O layer.** Threads only for CPU-bound post-processing.

## Exercises | 练习题

1. Run `code/main.py`. Confirm checkpoint resume works; measure async vs thread concurrency difference.
2. Implement an **outbox** table: every tool call writes to outbox first, then a separate goroutine/task executes. Verify idempotency by running the tool call twice.
3. Simulate a **rainbow deploy**: two concurrent runtime versions; route half of new thread_ids to each; confirm that in-flight threads on the old version are not interrupted.
4. Read LangGraph's runtime doc (linked below). Identify which features of the runtime would take the longest to replicate in a hand-rolled FastAPI + Postgres version. Is that a reason to adopt, or can you defer?
5. Read MegaAgent (arXiv:2408.09955) Section 3. The two-layer coordination (intra-group + inter-group admin chat) is explicit. Sketch how you would map this to a message queue with two queue families.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Durable execution / 持久执行 | "Persist the program state" / "持久化程序状态" | Engine writes state after each super-step; crash recovery is deterministic. / 引擎在每个超步后写入状态；崩溃恢复是确定性的。 |
| Super-step / 超步 | "Transactional boundary" / "事务边界" | Unit of work between checkpoints. LangGraph term. / 检查点之间的工作单元。LangGraph 术语。 |
| thread_id / 线程 ID | "Agent run identifier" / "Agent 运行标识符" | Key that binds checkpoints and resume logic. / 绑定检查点和恢复逻辑的键。 |
| Idempotency / 幂等性 | "Safe to retry" / "安全重试" | Repeating a side effect produces the same result as one attempt. / 重复副作用产生与一次尝试相同的结果。 |
| Outbox pattern / 发件箱模式 | "Decouple side effects" / "解耦副作用" | Write intent to a table; a separate executor performs and marks done. / 将意图写入表；单独的执行器执行并标记完成。 |
| At-least-once delivery / 至少一次投递 | "Possible duplicates" / "可能重复" | Message queue semantics; dedup key makes consumer effective-once. / 消息队列语义；去重键使消费者有效一次。 |
| Rainbow deploy / 彩虹部署 | "Overlapping versions" / "重叠版本" | Multiple runtime versions concurrent during long-running workloads. / 多个运行时版本在长时间工作负载期间并发。 |
| Async fiber / 异步纤程 | "Cooperative yielding" / "协作让步" | User-mode concurrency; cheap compared to threads for I/O-bound loads. / 用户态并发；I/O 密集负载下比线程廉价。 |
| Checkpoint / 检查点 | "State snapshot" / "状态快照" | Serialized state at a super-step boundary; key for resume. / 超步边界处的序列化状态；恢复的关键。 |

## Further Reading | 延伸阅读

- [LangChain — The runtime behind production deep agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) — LangGraph runtime design
- [MegaAgent](https://arxiv.org/abs/2408.09955) — per-agent producer-consumer queue; two-layer coordination at thousands of concurrent agents
- [Matrix](https://arxiv.org/abs/2511.21686) — decentralized framework with message queues as the coordination substrate
- [Temporal docs](https://docs.temporal.io/) — the reference workflow engine for durable execution
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — production lessons including rainbow deployment
