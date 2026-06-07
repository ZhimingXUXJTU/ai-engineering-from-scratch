# OpenTelemetry GenAI — Tracing Tool Calls End-to-End | OpenTelemetry GenAI：端到端追踪工具调用

> An agent calls five tools, three MCP servers, and two sub-agents. You need one trace across all of it. The OpenTelemetry GenAI semantic conventions (stable attributes in v1.37 and up) are the 2026 standard, natively supported by Datadog, Langfuse, Arize Phoenix, OpenLLMetry, and AgentOps. This lesson names the required attributes, walks the span hierarchy (agent -> LLM -> tool), and ships a stdlib span emitter you can plug into any OTel exporter.

> **【中文解读】** Agent 调用5个工具、3个 MCP 服务器、2个子 Agent，需要一个贯穿全程的 trace。OpenTelemetry GenAI 语义约定（v1.37+ 稳定属性）是 2026 年标准，Datadog/Langfuse/Arize Phoenix/OpenLLMetry/AgentOps 原生支持。本课命名必需属性、走通 span 层次结构（agent -> LLM -> tool），提供一个可接入任何 OTel 导出器的标准库 span 发射器。

> **【拓展】** OpenTelemetry 是 AI 应用从实验走向生产的必备可观测性基础设施。OTel GenAI 语义约定定义了稳定的属性名称，使得 Datadog、Langfuse、Phoenix 等后端都能解析相同的 span。一次仪表化，发送到任何后端。MCP 调用可通过 W3C traceparent 头传播追踪上下文。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, OTel span emitter) | **语言:** Python (stdlib, OTel span emitter)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Name the required OTel GenAI attributes for an LLM span and a tool-execution span.
  中文翻译：参见英文条目了解详情。
- Build a trace hierarchy that covers agent loop, LLM call, tool call, and MCP client dispatch.
  中文翻译：参见英文条目了解详情。
- Decide what content to capture (opt-in) vs redact (defaults).
  中文翻译：参见英文条目了解详情。
- Emit spans to a local collector (Jaeger, Langfuse) without rewriting tool code.

> **【中文解读】** 学习目标：掌握 OTel GenAI 必需属性（LLM span 和工具执行 span）；构建覆盖 Agent 循环、LLM 调用、工具调用和 MCP 客户端分发的 trace 层次；决定捕获哪些内容（opt-in）vs 脱敏（默认）；发送 span 到本地收集器。

## The Problem | 问题引入

> **【中文解读】** 调试场景：用户报告"Agent 有时30秒响应，有时3秒"。无追踪，日志只显示 LLM 调用，看不到工具分发、MCP 服务器往返、子 Agent。最终发现是一个 MCP 服务器冷启动偶尔卡住。没有端到端追踪就无法发现这类问题。

A debug from February 2026: user reports "my agent sometimes takes 30 seconds to respond; other times 3 seconds." No traces. Logs show the LLM call, but not the tool dispatch, not the MCP server round-trip, not the sub-agent. You guess. Eventually you find: one MCP server occasionally hangs on a cold-start.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

Without end-to-end tracing, you cannot find this. OTel GenAI fixes it.

> **【拓展：OTel GenAI 的可观测性生态】** OTel GenAI 规范在 2025-2026 年由 OpenTelemetry 语义约定组制定。它定义了稳定的属性名，使 Datadog、Langfuse、Phoenix、OpenLLMetry 和 AgentOps 都能解析相同的 span。一次埋点，导出到任意后端。这对多 Agent 系统特别重要——一个请求可能跨越多个 Agent、多个 MCP 服务器和多轮 LLM 调用。

The conventions settled in 2025-2026 under the OpenTelemetry semantic-conventions group. They define stable attribute names so Datadog, Langfuse, Phoenix, OpenLLMetry, and AgentOps all parse the same spans. Instrument once; ship to any backend.

> 可观测性相关内容：OpenTelemetry 在 AI 应用中的追踪和监控。

## The Concept | 核心概念

> **【中文解读】** 本节详解 span 层次结构（agent.invoke_agent -> llm.chat -> tool.execute -> mcp.call）、必需属性（gen_ai.* 命名空间）、span 类型（CLIENT/INTERNAL）、opt-in 内容捕获、span 事件、导出器、跨 MCP 传播、指标和 AgentOps 层。

### Span hierarchy

> **【中文解读】** Span 层次：agent.invoke_agent（顶层 INTERNAL span）-> llm.chat（CLIENT span）-> tool.execute（INTERNAL）-> mcp.call（CLIENT span）。整个结构嵌套在一个 trace id 下，span id 链接父子关系。

```
agent.invoke_agent  (top, INTERNAL span)
 ├── llm.chat       (CLIENT span)
 ├── tool.execute   (INTERNAL)
 │    └── mcp.call  (CLIENT span)
 ├── llm.chat       (CLIENT span)
 └── subagent.invoke (INTERNAL)
```

The whole thing nests under one trace id. Span ids link the parent-child relationships.

> 参见英文原文获取完整的技术说明。

### Required attributes

Per the 2025-2026 semconv:

- `gen_ai.operation.name` — `"chat"`, `"text_completion"`, `"embeddings"`, `"execute_tool"`, `"invoke_agent"`.
  中文翻译：参见英文条目了解详情。
- `gen_ai.provider.name` — `"openai"`, `"anthropic"`, `"google"`, `"azure_openai"`.
  中文翻译：参见英文条目了解详情。
- `gen_ai.request.model` — requested model string (e.g. `"gpt-4o-2024-08-06"`).
  中文翻译：参见英文条目了解详情。
- `gen_ai.response.model` — the model actually served.
  中文翻译：参见英文条目了解详情。
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`.
  中文翻译：参见英文条目了解详情。
- `gen_ai.response.id` — provider response id for correlation.
  中文翻译：参见英文条目了解详情。

For tool spans:

- `gen_ai.tool.name` — tool identifier.
  中文翻译：参见英文条目了解详情。
- `gen_ai.tool.call.id` — the specific call id.
  中文翻译：参见英文条目了解详情。
- `gen_ai.tool.description` — tool description (optional).
  中文翻译：参见英文条目了解详情。

For agent spans:

- `gen_ai.agent.name` / `gen_ai.agent.id` / `gen_ai.agent.description`.
  中文翻译：参见英文条目了解详情。

### Span kinds

- `SpanKind.CLIENT` for calls crossing a process boundary (LLM provider, MCP server).
  中文翻译：参见英文条目了解详情。
- `SpanKind.INTERNAL` for the agent's own loop steps and tool execution.
  中文翻译：参见英文条目了解详情。

### Opt-in content capture

By default, spans carry metrics and timing — not prompts or completions. Large payloads and PII are off by default. Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` and specific content-capture env vars to include content. Review carefully before enabling in prod.

> 规范相关内容：MCP 规范的具体条款和要求。

### Events on spans

Token-level events can be added as span events:

> 参见英文原文获取完整的技术说明。

- `gen_ai.content.prompt` — input messages.
  中文翻译：参见英文条目了解详情。
- `gen_ai.content.completion` — output messages.
  中文翻译：参见英文条目了解详情。
- `gen_ai.content.tool_call` — tool call as recorded.
  中文翻译：参见英文条目了解详情。

Events time-order within a span for detailed replay.

> 参见英文原文获取完整的技术说明。

### Exporters

OTel spans export to:

- **Jaeger / Tempo.** OSS, on-prem.
  中文翻译：**Jaeger / Tempo.** — 参见英文原文了解详情。
- **Langfuse.** LLM-observability-specific; visualizes token usage.
  中文翻译：**Langfuse.** — 参见英文原文了解详情。
- **Arize Phoenix.** Evals + tracing combined.
  中文翻译：**Arize Phoenix.** — 参见英文原文了解详情。
- **Datadog.** Commercial; natively parses `gen_ai.*` attributes.
  中文翻译：**Datadog.** — 参见英文原文了解详情。
- **Honeycomb.** Column-oriented; query-friendly.
  中文翻译：**Honeycomb.** — 参见英文原文了解详情。

All speak OTLP, the wire format. Your code does not care.

> 参见英文原文获取完整的技术说明。

### Propagation across MCP

When an MCP client calls a server, inject the W3C traceparent header into the request. Streamable HTTP supports standard headers. Stdio does not carry HTTP headers natively; the spec's 2026 roadmap discusses adding a `_meta.traceparent` field on JSON-RPC calls.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

Until that ships: include the traceparent in the `_meta` of every request manually. Server logs the trace id.

> 参见英文原文获取完整的技术说明。

### Metrics

Alongside spans, the GenAI semconv defines metrics:

> 参见英文原文获取完整的技术说明。

- `gen_ai.client.token.usage` — histogram.
  中文翻译：参见英文条目了解详情。
- `gen_ai.client.operation.duration` — histogram.
  中文翻译：参见英文条目了解详情。
- `gen_ai.tool.execution.duration` — histogram.
  中文翻译：参见英文条目了解详情。

Use these for dashboards that do not need per-call detail.

> 参见英文原文获取完整的技术说明。

### AgentOps layer

AgentOps (founded 2024) specializes in GenAI observability. It wraps popular frameworks (LangGraph, Pydantic AI, CrewAI) to emit OTel spans automatically. Useful if your stack uses a supported framework; use manual instrumentation otherwise.

> 可观测性相关内容：OpenTelemetry 在 AI 应用中的追踪和监控。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 向 stdout 发射 OTLP-JSON 格式的 span，覆盖一个 Agent 调用 LLM、分发两个工具、进行一次 MCP 往返。无真实导出器——课程聚焦 span 形状和属性集。关注点：trace id 跨所有 span 共享；父子链接通过 parentSpanId 编码；`gen_ai.*` 必需属性已填充；内容捕获默认关闭。

`code/main.py` emits OTel-shaped spans to stdout (in OTLP-JSON-like format) for an agent that calls an LLM, dispatches two tools, and makes one MCP round-trip. No real exporter — the lesson focuses on the span shape and attribute set. Paste the output into an OTLP-compatible viewer or just read it.

> 代码实现说明：参见 code/main.py 中的具体实现。

What to look at:

- Trace id is shared across all spans.
  中文翻译：参见英文条目了解详情。
- Parent-child links are encoded via `parentSpanId`.
  中文翻译：参见英文条目了解详情。
- Required `gen_ai.*` attributes are populated.
  中文翻译：参见英文条目了解详情。
- Content capture is off by default; one scenario turns it on via env var.
  中文翻译：参见英文条目了解详情。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-otel-genai-instrumentation.md`——给定 Agent 代码库，生成仪表化计划：在哪里添加 span、填充哪些属性、目标导出器。

This lesson produces `outputs/skill-otel-genai-instrumentation.md`. Given an agent codebase, the skill produces an instrumentation plan: where to add spans, which attributes to populate, and which exporters to target.

> 技能与打包相关内容：Agent SDK 和可复用技能的定义与分发。

## Exercises | 练习题

1. Run `code/main.py`. Count the spans and identify which is CLIENT vs INTERNAL.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Turn on content capture (env var) and confirm `gen_ai.content.prompt` and `gen_ai.content.completion` events appear. Note the implications for PII.
   中文翻译：参见英文原文了解完整练习要求。

3. Add the tool-execution metric `gen_ai.tool.execution.duration` and emit it as a histogram sample per call.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

4. Propagate a traceparent from a parent agent span into an MCP request's `_meta.traceparent` field. Verify the MCP server would see the same trace id.
   中文翻译：参见英文原文了解完整练习要求。

5. Read the OTel GenAI semconv spec. Identify one attribute listed in the semconv that this lesson's code does NOT emit. Add it.
   中文翻译：阅读相关练习。参见英文原文了解完整要求。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| OTel | "OpenTelemetry" | Open standard for traces, metrics, logs | 开放遥测标准 |
| GenAI semconv | "GenAI semantic conventions" | Stable attribute names for LLM / tool / agent spans | GenAI 语义约定 |
| `gen_ai.*` | "The attribute namespace" | All GenAI attributes share this prefix | GenAI 属性命名空间 |
| Span | "Timed operation" | A unit of work with a start, end, and attributes | Span：带属性的时间操作单元 |
| Trace | "Cross-span ancestry" | Tree of spans sharing a trace id | Trace：跨 span 的追踪树 |
| SpanKind | "CLIENT / SERVER / INTERNAL" | Hints about span direction | Span 类型：跨进程/同进程 |
| OTLP | "OpenTelemetry Line Protocol" | Wire format for exporters | OTLP：导出器线格式 |
| Opt-in content | "Prompt / completion capture" | Off by default; env var to enable | 内容捕获：默认关闭 |
| traceparent | "W3C header" | Propagates trace context across services | traceparent：跨服务追踪传播 |
| Exporter | "Backend-specific shipper" | Component that sends spans to Jaeger / Datadog / etc. | 导出器：发送到后端 |

## Further Reading | 延伸阅读

- [OpenTelemetry — GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — canonical conventions for GenAI spans, metrics, and events
  中文翻译：canonical conventions for GenAI spans, metrics, and events
- [OpenTelemetry — GenAI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/) — LLM and tool-execution span attribute list
  中文翻译：LLM and tool-execution span attribute list
- [OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) — agent-level `invoke_agent` span
  中文翻译：agent-level `invoke_agent` span
- [open-telemetry/semantic-conventions — GenAI spans](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md) — GitHub-hosted source of truth
  中文翻译：GitHub-hosted source of truth
- [Datadog — LLM OTel semantic convention](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) — production integration walkthrough
  中文翻译：production integration walkthrough
