# OpenAI Agents SDK: Handoffs, Guardrails, Tracing | 交接 OpenAI Agent SDK

> OpenAI Agents SDK is the lightweight multi-agent framework built on the Responses API. Five primitives: Agent, Handoff, Guardrail, Session, Tracing. Handoffs are tools named `transfer_to_<agent>`. Guardrails trip on input or output. Tracing is on by default.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Name the five primitives of the OpenAI Agents SDK.
- Explain handoffs: why they are modeled as tools, what name shape the model sees, and how context transfers.
- Distinguish input guardrails, output guardrails, and tool guardrails; explain `run_in_parallel` vs blocking mode.
- Implement a stdlib runtime with handoffs + guardrails + span-style tracing.

## The Problem | 问题引入

Agents that cannot delegate cleanly end up stuffing everything into one prompt. Agents without guardrails ship PII, policy-violating output, or loop forever. OpenAI's SDK codifies the three primitives that make multi-agent work tractable.

> 无法干净地委派任务的 Agent 最终会把所有东西塞进一个提示词中。没有护栏的 Agent 会泄露 PII、输出违反政策的内容或永远循环。OpenAI 的 SDK 将使多 Agent 工作变得可管理的三个原语进行了规范化。


> **【中文解读】** OpenAI Agents SDK（原 Swarm）是 OpenAI 官方的 Agent 开发框架。三大核心概念：(1) Handoffs——Agent 之间的任务转移；(2) Guardrails——输入/输出安全护栏；(3) Tracing——内置 OpenTelemetry 追踪。SDK 的设计哲学是'简洁至上'——用最少的抽象实现最常见的 Agent 模式。

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}** OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 Handoffs 模式将多 Agent 协作建模为'接力赛'——一个 Agent 完成自己的部分后将控制权移交给下一个。这与 AutoGen 的 Actor 模型形成对比。SDK 内置的 Tracing 能力使其特别适合需要可观测性的生产环境。

> 🔗 **【前置】** 必须先掌握：Phase 14·01（Agent Loop）和 Phase 14·06（Tool Use）——OpenAI Agents SDK 就是这些概念的产品化封装。还需要熟悉 OpenAI Responses API（不是旧的 Chat Completions API），因为 SDK 是基于 Responses API 构建的。

## The Concept | 核心概念

### Five primitives

1. **Agent.** LLM + instructions + tools + handoffs.
2. **Handoff.** Delegation to another agent. Represented to the model as a tool named `transfer_to_<agent_name>`.
3. **Guardrail.** Validation on input (first agent only), output (last agent only), or tool invocation (per function tool).
4. **Session.** Automatic conversation history across turns.
5. **Tracing.** Built-in spans for LLM generations, tool calls, handoffs, guardrails.

### Handoffs as tools

The model sees `transfer_to_billing_agent` in its tool list. Calling it signals the runtime to:

> 模型在其工具列表中看到 `transfer_to_billing_agent`。调用它意味着运行时需要：

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

1. Copy the conversation context (or collapse it via `nest_handoff_history` beta).
2. Initialize the target agent with its instructions.
3. Continue the run with the target agent.

This is the supervisor pattern (Lesson 13 / Lesson 28) productized.

> 这就是产品化后的监督者模式（第 13 课 / 第 28 课）。

> 💡 **【类比】** Handoff 像医院的"分诊转诊"：分诊台（triage agent）听完病人描述后说"你去心脏科"——这就是 `transfer_to_cardiology_agent`。病人（对话上下文）从分诊台转到心脏科诊室，心脏科医生接管。**关键**：handoff 是单向的，控制权完全移交，原 agent 不再参与。这跟 LangGraph 的 supervisor 模式不同——supervisor 一直保留控制权，只是"派遣"specialist。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

### Guardrails

Three flavors:

> 三种类型：

- **Input guardrails.** Run on the first agent's input. Reject unsafe or out-of-scope requests before any LLM call.
- **Output guardrails.** Run on the last agent's output. Catch PII leaks, policy violations, malformed responses.
- **Tool guardrails.** Run per-function-tool. Validate arguments, check permissions, audit execution.

Mode:

> 模式：

- **Parallel** (default). Guardrail LLM runs alongside the main LLM. Lower tail latency. If tripped, the main LLM's work is discarded (token waste).
- **Blocking** (`run_in_parallel=False`). Guardrail LLM runs first. If tripped, no tokens wasted on the main call.

Tripwires raise `InputGuardrailTripwireTriggered` / `OutputGuardrailTripwireTriggered`.

> 触发器会抛出 `InputGuardrailTripwireTriggered` / `OutputGuardrailTripwireTriggered` 异常。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

### Tracing

On by default. Every LLM generation, tool call, handoff, and guardrail emits a span. `OPENAI_AGENTS_DISABLE_TRACING=1` opts out. `add_trace_processor(processor)` fans spans to your own backend alongside OpenAI's.

> 默认开启。每次 LLM 生成、工具调用、交接和护栏都会发出一个 span。`OPENAI_AGENTS_DISABLE_TRACING=1` 可以选择退出。`add_trace_processor(processor)` 可以将 span 同时发送到你自己的后端和 OpenAI 的后端。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

### Sessions

`Session` stores conversation history in a backend (SQLite, Redis, custom). `Runner.run(agent, input, session=session)` auto-loads and appends.

> `Session` 在后端（SQLite、Redis、自定义）存储对话历史。`Runner.run(agent, input, session=session)` 自动加载和追加。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

### Where this pattern goes wrong

> ⚠️ **【易错点】** Handoff drift（交接循环）：Agent A 移交给 B，B 又移交给 A，A 再移交给 B...无限循环烧 token。**后果**：账单爆炸且任务永远不完成。**一行修复**：在 Runner 里加 hop counter（如 `max_handoffs=5`），超过就抛 `HandoffBudgetExceeded` 异常。OpenAI SDK 默认没有这个保护，必须自己加。

- **Handoff drift.** Agent A hands off to Agent B which hands back to Agent A. Add a hop counter.
- **Guardrail bypass.** Tool guardrails only fire on function tools; built-in tools (file reader, web fetch) need separate policy.
- **Over-tracing.** Sensitive content in spans. Pair with OTel GenAI content-capture rules (Lesson 23) — store externally, reference by ID.

> 🤔 **【困惑】** Q: Guardrail 的 parallel 和 blocking 模式怎么选？看起来 parallel 总是更快。 A: 不一定。Parallel 是"主 LLM 和 guardrail LLM 同时跑"——快但浪费 token（guardrail 触发时主 LLM 已经在跑了，token 已经花了）。Blocking 是"先 guardrail，过了再主 LLM"——慢但省钱。**选择规则**：如果 guardrail 触发率高（如 >20%），用 blocking 省钱；如果触发率低（如 <5%），用 parallel 省延迟。

> **交接漂移。** Agent A 交接给 Agent B，Agent B 又交接回 Agent A。添加跳数计数器。
> **护栏绕过。** 工具护栏只在函数工具上触发；内置工具（文件读取器、网页抓取）需要单独的策略。
> **过度追踪。** Span 中包含敏感内容。配合 OTel GenAI 内容捕获规则（第 23 课）使用——外部存储，按 ID 引用。

## Build It | 动手实现

`code/main.py` implements the SDK shape in stdlib:

> `code/main.py` 用标准库实现了 SDK 的形态：

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

- `Agent`, `FunctionTool`, `Handoff` (as a function tool with transfer semantics).
- `Runner` with input/output/tool guardrails, handoff dispatch, and hop counter.
- A simple span emitter to show the trace shape.
- A triage agent that hands off to billing or support based on the user's query; guardrail trips on one input.

Run it:

```
python3 code/main.py
```

The trace shows two successful handoffs, one input guardrail trip, and a span tree mirroring what the real SDK emits.

> 追踪显示两次成功的交接、一次输入护栏触发，以及一个反映真实 SDK 输出的 span 树。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

## Use It | 用框架实现

- **OpenAI Agents SDK** for OpenAI-first products.
- **Claude Agent SDK** (Lesson 17) for Claude-first products.
- **LangGraph** (Lesson 13) when you want explicit state and durable resume.
- **Custom** when you need exact control (voice, multi-provider, federated deployments).

## Ship It | 产出物

`outputs/skill-agents-sdk-scaffold.md` scaffolds an Agents SDK app with a triage agent, handoffs, input/output/tool guardrails, session store, and a trace processor.

> `outputs/skill-agents-sdk-scaffold.md` 搭建一个 Agents SDK 应用，包含分诊 Agent、交接、输入/输出/工具护栏、会话存储和追踪处理器。

> OpenAI Agents SDK 提供四种核心概念：Agents（带指令和工具的 LLM）、Handoffs（Agent 间移交）、Guardrails（输入/输出验证）、Tracing（运行追踪）。生产级 Agent 开发框架。

## Exercises | 练习题

1. Add a handoff hop counter: refuse after N transfers. Trace the behavior.
  中文翻译：思考并实践此练习。
2. Implement `nest_handoff_history` as an option — collapse prior messages into one summary before transferring.
  中文翻译：思考并实践此练习。
3. Write a blocking output guardrail. Compare latency on prompts that would trip it vs ones that pass.
  中文翻译：思考并实践此练习。
4. Wire `add_trace_processor` to a JSON logger. What shape does it emit per span?
  中文翻译：思考并实践此练习。
5. Read the SDK docs. Port your stdlib toy to `openai-agents-python`. What did you model wrong?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## Further Reading | 延伸阅读

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) — primitives, handoffs, guardrails, tracing
  中文翻译：见原文。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) — Claude-flavored counterpart
  中文翻译：见原文。
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — when to reach for handoffs at all
  中文翻译：见原文。
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the standard Agents SDK spans map to
  中文翻译：见原文。
