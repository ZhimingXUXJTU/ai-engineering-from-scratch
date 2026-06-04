# 生产 运行时 欧盟

> Production agents run on six runtime shapes: request-response, streaming, durable execution, queue-based background, event-driven, and scheduled. Pick the shape before you pick the framework. Observability is load-bearing at every shape.


**类型：** 学习
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice)
**预计时间：** ~60 minutes

## 学习目标

- Name the six production runtime shapes and match each to a framework / product pattern.
- Explain why durable execution (LangGraph) matters for long-horizon tasks.
- Describe the event-driven runtime and when Claude Managed Agents fits.
- Explain the observability-as-load-bearing claim for multi-step agents.

## 问题引入

> **【中文解读】** 生产环境 Agent 运行时需要处理开发环境不需要的问题：持久化状态、容错恢复、水平扩展、速率限制、成本控制和可观测性。选择运行时（LangGraph、Temporal、自建）取决于任务的关键性和预算。
> **【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】** 2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGraph 的托管服务，内置状态检查点和重放；(2) Temporal——通用工作流引擎，配合 AI SDK 可构建持久化 Agent；(3) 自建——基于 Redis/Kafka 的消息队列 + 自定义 Agent 循环。关键决策因素是是否需要持久化执行——如果 Agent 可能运行数小时甚至数天，Temporal 或 LangGraph 是更安全的选择。

## 核心概念

### Request-response
- Synchronous HTTP. User waits for completion.
- Only viable for short tasks (<30s).
- Stacks: Agno (Python + FastAPI), Mastra (TypeScript + Express/Hono/Fastify/Koa).
- Observability: standard HTTP access logs + OTel spans.
### Streaming
- SSE or WebSocket for progressive output.
- LiveKit extends this to WebRTC for voice/video (Lesson 22).
- Stacks: any framework with streaming support + a frontend that handles SSE/WS.
- Observability: per-chunk timing, first-token latency, tail latency.
### Durable execution
- State checkpointed after every step; auto-resumes on failure.
- AutoGen v0.4 actor model isolates failures to one agent (Lesson 14).
- LangGraph's core differentiator (Lesson 13).
- Essential when step count is unknown and recovery cost is high.
### Queue-based / background
- Job enters a queue, workers pick up, results flow back via webhooks or pub/sub.
- Essential for long-horizon agents (dozens-to-hundreds of steps per task, per Anthropic's computer use announcement).
- Stacks: Celery (Python), BullMQ (Node), SQS + Lambda (AWS), custom.
- Observability: queue depth, per-job latency distribution, DLQ size.
### Event-driven
- Agents subscribe to triggers: new email, PR opened, cron fire.
- Claude Managed Agents covers this out of the box (Lesson 17).
- CrewAI Flows (Lesson 15) structures event-driven deterministic workflows.
- Observability: trigger source, event-to-start latency, agent latency.
### Scheduled
- Cron-shaped agents that run periodically.
- Combine with durable execution so a failing nightly run resumes next tick.
- Stacks: Kubernetes CronJob + a durable framework; hosted (Render cron, Vercel cron).
### 2026 deployment patterns
- **CrewAI Flows** for event-driven production.
- **Agno** stateless FastAPI for Python microservices.
- **Mastra** server adapters (Express, Hono, Fastify, Koa) for embedding.
- **Pipecat Cloud / LiveKit Cloud** for managed voice (Lesson 22).
- **Claude Managed Agents** for hosted long-running async.
### Observability is load-bearing
Without OpenTelemetry GenAI spans (Lesson 23) plus a Langfuse/Phoenix/Opik backend (Lesson 24), you cannot debug a multi-step agent that failed at step 40. This is not optional for production. It's the difference between "we debug fast" and "we replay from scratch with more logging."
### Where production runtimes fail
- **Wrong shape choice.** Picking request-response for a 5-minute task. Users hang up; workers pile up; retries compound.
- **No DLQ.** Queue workers without dead-letter. Failed jobs vanish.
- **Opaque background work.** Background agent runs without trace export. Failures are invisible until the user reports them.
- **Skipping durable state.** Any run > 30 seconds where you can't afford to restart needs durable execution.

## 动手实现

`code/main.py` is a stdlib multi-shape demo:
- Request-response endpoint (plain function).
- Streaming handler (generator).
- Queue-based worker with DLQ.
- Event trigger registry.
- Cron-shaped scheduler.
Run it:
```bash
python3 code/main.py
```
Output: five traces showing each shape's behavior on the same task. Same agent logic, different outer shells. Durable execution (the sixth shape) is intentionally covered in Lesson 13 with LangGraph checkpointing.

## 用框架实现

- **Request-response** for chat-style UX.
- **Streaming** for progressive responses.
- **Durable** for long-horizon tasks.
- **Queue** for batch / async / long-running.
- **Event** for agent reactivity.
- **Cron** for housekeeping (memory consolidation, evals, cost reports).

## 产出物

`outputs/skill-runtime-shape.md` picks a runtime shape for a task and wires the observability requirements.

## 练习题

1. Port your Lesson 01 ReAct loop to all six shapes in your stack. Which shape fits which product surface?
   *思考并实践此练习*
2. Add a DLQ to the queue-based demo. Simulate 10% job failure; surface DLQ size.
   *思考并实践此练习*
3. Write a cron-triggered eval agent that runs nightly against your top 20 traces from the day.
   *思考并实践此练习*
4. Implement streaming with backpressure: if the client is slow, pause the agent. How does this interact with a turn budget?
   *思考并实践此练习*
5. Read Claude Managed Agents docs. When would you move a self-hosted long-horizon agent to managed?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Request-response | "Synchronous" |
| Streaming | "SSE / WS" |
| Durable execution | "Resume from failure" |
| Queue-based | "Background jobs" |
| Event-driven | "Trigger-based" |
| DLQ | "Dead-letter queue" |
| Claude Managed Agents | "Hosted harness" |

## 延伸阅读

