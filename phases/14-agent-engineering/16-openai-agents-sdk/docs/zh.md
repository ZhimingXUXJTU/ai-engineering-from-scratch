# 交接 OpenAI Agent SDK

> OpenAI Agents SDK is the lightweight multi-agent framework built on the Responses API. Five primitives: Agent, Handoff, Guardrail, Session, Tracing. Handoffs are tools named `transfer_to_<agent>`. Guardrails trip on input or output. Tracing is on by default.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use)
**预计时间：** ~75 minutes

## 学习目标

- Name the five primitives of the OpenAI Agents SDK.
- Explain handoffs: why they are modeled as tools, what name shape the model sees, and how context transfers.
- Distinguish input guardrails, output guardrails, and tool guardrails; explain `run_in_parallel` vs blocking mode.
- Implement a stdlib runtime with handoffs + guardrails + span-style tracing.

## 问题引入

> **【中文解读】** OpenAI Agents SDK（原 Swarm）是 OpenAI 官方的 Agent 开发框架。三大核心概念：(1) Handoffs——Agent 之间的任务转移；(2) Guardrails——输入/输出安全护栏；(3) Tracing——内置 OpenTelemetry 追踪。SDK 的设计哲学是'简洁至上'——用最少的抽象实现最常见的 Agent 模式。
> **【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】** OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 Handoffs 模式将多 Agent 协作建模为'接力赛'——一个 Agent 完成自己的部分后将控制权移交给下一个。这与 AutoGen 的 Actor 模型形成对比。SDK 内置的 Tracing 能力使其特别适合需要可观测性的生产环境。

## 核心概念

### Five primitives
1. **Agent.** LLM + instructions + tools + handoffs.
2. **Handoff.** Delegation to another agent. Represented to the model as a tool named `transfer_to_<agent_name>`.
3. **Guardrail.** Validation on input (first agent only), output (last agent only), or tool invocation (per function tool).
4. **Session.** Automatic conversation history across turns.
5. **Tracing.** Built-in spans for LLM generations, tool calls, handoffs, guardrails.
### Handoffs as tools
The model sees `transfer_to_billing_agent` in its tool list. Calling it signals the runtime to:
1. Copy the conversation context (or collapse it via `nest_handoff_history` beta).
2. Initialize the target agent with its instructions.
3. Continue the run with the target agent.
This is the supervisor pattern (Lesson 13 / Lesson 28) productized.
### Guardrails
Three flavors:
- **Input guardrails.** Run on the first agent's input. Reject unsafe or out-of-scope requests before any LLM call.
- **Output guardrails.** Run on the last agent's output. Catch PII leaks, policy violations, malformed responses.
- **Tool guardrails.** Run per-function-tool. Validate arguments, check permissions, audit execution.
Mode:
- **Parallel** (default). Guardrail LLM runs alongside the main LLM. Lower tail latency. If tripped, the main LLM's work is discarded (token waste).
- **Blocking** (`run_in_parallel=False`). Guardrail LLM runs first. If tripped, no tokens wasted on the main call.
Tripwires raise `InputGuardrailTripwireTriggered` / `OutputGuardrailTripwireTriggered`.
### Tracing
On by default. Every LLM generation, tool call, handoff, and guardrail emits a span. `OPENAI_AGENTS_DISABLE_TRACING=1` opts out. `add_trace_processor(processor)` fans spans to your own backend alongside OpenAI's.
### Sessions
`Session` stores conversation history in a backend (SQLite, Redis, custom). `Runner.run(agent, input, session=session)` auto-loads and appends.
### Where this pattern goes wrong
- **Handoff drift.** Agent A hands off to Agent B which hands back to Agent A. Add a hop counter.
- **Guardrail bypass.** Tool guardrails only fire on function tools; built-in tools (file reader, web fetch) need separate policy.
- **Over-tracing.** Sensitive content in spans. Pair with OTel GenAI content-capture rules (Lesson 23) — store externally, reference by ID.

## 动手实现

`code/main.py` implements the SDK shape in stdlib:
- `Agent`, `FunctionTool`, `Handoff` (as a function tool with transfer semantics).
- `Runner` with input/output/tool guardrails, handoff dispatch, and hop counter.
- A simple span emitter to show the trace shape.
- A triage agent that hands off to billing or support based on the user's query; guardrail trips on one input.
Run it:
```
python3 code/main.py
```
The trace shows two successful handoffs, one input guardrail trip, and a span tree mirroring what the real SDK emits.

## 用框架实现

- **OpenAI Agents SDK** for OpenAI-first products.
- **Claude Agent SDK** (Lesson 17) for Claude-first products.
- **LangGraph** (Lesson 13) when you want explicit state and durable resume.
- **Custom** when you need exact control (voice, multi-provider, federated deployments).

## 产出物

`outputs/skill-agents-sdk-scaffold.md` scaffolds an Agents SDK app with a triage agent, handoffs, input/output/tool guardrails, session store, and a trace processor.

## 练习题

1. Add a handoff hop counter: refuse after N transfers. Trace the behavior.
   *思考并实践此练习*
2. Implement `nest_handoff_history` as an option — collapse prior messages into one summary before transferring.
   *思考并实践此练习*
3. Write a blocking output guardrail. Compare latency on prompts that would trip it vs ones that pass.
   *思考并实践此练习*
4. Wire `add_trace_processor` to a JSON logger. What shape does it emit per span?
   *思考并实践此练习*
5. Read the SDK docs. Port your stdlib toy to `openai-agents-python`. What did you model wrong?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Agent | "LLM + instructions" |
| Handoff | "Transfer" |
| Guardrail | "Policy check" |
| Tripwire | "Guardrail trip" |
| Session | "History store" |
| Tracing | "Spans" |
| Blocking guardrail | "Sequential check" |
| Parallel guardrail | "Concurrent check" |

## 延伸阅读

