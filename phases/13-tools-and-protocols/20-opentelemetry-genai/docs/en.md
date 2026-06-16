# OpenTelemetry GenAI — Tracing Tool Calls End-to-End | OpenTelemetry GenAI：端到端追踪工具调用

> An agent calls five tools, three MCP servers, and two sub-agents. You need one trace across all of it. The OpenTelemetry GenAI semantic conventions (stable attributes in v1.37 and up) are the 2026 standard, natively supported by Datadog, Langfuse, Arize Phoenix, OpenLLMetry, and AgentOps. This lesson names the required attributes, walks the span hierarchy (agent -> LLM -> tool), and ships a stdlib span emitter you can plug into any OTel exporter.

> **【中文解读】** Agent 调用5个工具、3个 MCP 服务器、2个子 Agent，需要一个贯穿全程的 trace。OpenTelemetry GenAI 语义约定（v1.37+ 稳定属性）是 2026 年标准，Datadog/Langfuse/Arize Phoenix/OpenLLMetry/AgentOps 原生支持。本课命名必需属性、走通 span 层次结构（agent -> LLM -> tool），提供一个可接入任何 OTel 导出器的标准库 span 发射器。

> **【拓展】** OpenTelemetry 是 AI 应用从实验走向生产的必备可观测性基础设施。OTel GenAI 语义约定定义了稳定的属性名称，使得 Datadog、Langfuse、Phoenix 等后端都能解析相同的 span。一次仪表化，发送到任何后端。MCP 调用可通过 W3C traceparent 头传播追踪上下文。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07、08（MCP server/client）——要在 MCP 调用上加 span；(2) OpenTelemetry 基础（trace、span、span context、exporter）；(3) 分布式追踪概念（trace_id、span_id、parent_id）；(4) W3C traceparent 头格式——跨进程上下文传播。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, OTel span emitter) | **语言:** Python (stdlib, OTel span emitter)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Name the required OTel GenAI attributes for an LLM span and a tool-execution span.
  中文翻译：命名 LLM span 和工具执行 span 的必需 OTel GenAI 属性。
- Build a trace hierarchy that covers agent loop, LLM call, tool call, and MCP client dispatch.
  中文翻译：构建覆盖 Agent 循环、LLM 调用、工具调用和 MCP 客户端分发的 trace 层次。
- Decide what content to capture (opt-in) vs redact (defaults).
  中文翻译：决定捕获哪些内容（opt-in）vs 脱敏（默认）。
- Emit spans to a local collector (Jaeger, Langfuse) without rewriting tool code.

> **【中文解读】** 学习目标：掌握 OTel GenAI 必需属性（LLM span 和工具执行 span）；构建覆盖 Agent 循环、LLM 调用、工具调用和 MCP 客户端分发的 trace 层次；决定捕获哪些内容（opt-in）vs 脱敏（默认）；发送 span 到本地收集器。

## The Problem | 问题引入

> **【中文解读】** 调试场景：用户报告"Agent 有时30秒响应，有时3秒"。无追踪，日志只显示 LLM 调用，看不到工具分发、MCP 服务器往返、子 Agent。最终发现是一个 MCP 服务器冷启动偶尔卡住。没有端到端追踪就无法发现这类问题。

A debug from February 2026: user reports "my agent sometimes takes 30 seconds to respond; other times 3 seconds." No traces. Logs show the LLM call, but not the tool dispatch, not the MCP server round-trip, not the sub-agent. You guess. Eventually you find: one MCP server occasionally hangs on a cold-start.

> 2026 年 2 月的调试：用户报告"我的 Agent 有时 30 秒响应；有时 3 秒"。无追踪。日志显示 LLM 调用，但不显示工具分发、MCP 服务器往返、子 Agent。你猜测。最终你发现：一个 MCP 服务器在冷启动时偶尔卡住。

Without end-to-end tracing, you cannot find this. OTel GenAI fixes it.

> 没有端到端追踪，你找不到这个。OTel GenAI 修复它。

> 💡 **【类比】** 分布式追踪像快递的"物流单号"。你寄一个包裹（user 请求），途经多个中转站（agent → LLM → tool → MCP server），每个站点扫一次单号（生成一个 span）。最后你能看到一个时间线："9:01 寄出 → 9:02 收件 → 9:05 分拣 → 9:30 转运 → 9:45 派送"。OTel GenAI 是快递公司约定的"扫码字段标准"——每家公司（Datadog/Langfuse）都按相同字段（gen_ai.operation.name 等）记录，所以你换物流公司时不需要重新贴单。

The conventions settled in 2025-2026 under the OpenTelemetry semantic-conventions group. They define stable attribute names so Datadog, Langfuse, Phoenix, OpenLLMetry, and AgentOps all parse the same spans. Instrument once; ship to any backend.

> 约定在 2025-2026 年在 OpenTelemetry 语义约定组下稳定。它们定义稳定属性名，使 Datadog、Langfuse、Phoenix、OpenLLMetry 和 AgentOps 都解析相同 span。一次仪表化；发送到任何后端。

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

> 整个嵌套在一个 trace id 下。Span id 链接父子关系。

> ⚠️ **【易错点】** 场景：跨进程调用 MCP server 时不传 traceparent / 后果：客户端的 trace 在 MCP 调用处断裂，看到的是"tool.execute 100ms 完成"，但看不到 MCP server 内部到底卡在哪；多个独立 trace 无法串联 / 修复：(1) HTTP 调用 MCP 时在 header 加 `traceparent: 00-<trace_id>-<span_id>-01`；(2) stdio MCP 把 trace context 序列化到 JSON-RPC `params._meta.trace_context`；(3) 接收端取出 context 续接 span。没有上下文传播，分布式追踪就是空话。

> 🤔 **【困惑】** Q: span 里应该记录完整的 prompt 和 response 吗？便于调试。 A: 默认**不记录**，只记长度和 token 数。原因：(1) **隐私**——prompt 含用户敏感信息；(2) **存储成本**——大量请求时全量记录会让 trace 后端存储爆炸；(3) **合规**——GDPR/CCPA 要求最小化数据收集。做法：默认 redact，生产环境通过显式 `gen_ai.content.capture=full` opt-in 才记录，且加密存储 + 短期 TTL。

### Required attributes

Per the 2025-2026 semconv:

- `gen_ai.operation.name` — `"chat"`, `"text_completion"`, `"embeddings"`, `"execute_tool"`, `"invoke_agent"`.
  中文翻译：`gen_ai.operation.name`——操作名（`"chat"`、`"text_completion"`、`"embeddings"`、`"execute_tool"`、`"invoke_agent"`）。
- `gen_ai.provider.name` — `"openai"`, `"anthropic"`, `"google"`, `"azure_openai"`.
  中文翻译：`gen_ai.provider.name`——提供商名。
- `gen_ai.request.model` — requested model string (e.g. `"gpt-4o-2024-08-06"`).
  中文翻译：`gen_ai.request.model`——请求的模型字符串。
- `gen_ai.response.model` — the model actually served.
  中文翻译：`gen_ai.response.model`——实际服务的模型。
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`.
  中文翻译：`gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`——输入/输出 token 数。
- `gen_ai.response.id` — provider response id for correlation.
  中文翻译：`gen_ai.response.id`——提供商响应 id 用于关联。

For tool spans:

> 对工具 span：

- `gen_ai.tool.name` — tool identifier.
  中文翻译：`gen_ai.tool.name`——工具标识符。
- `gen_ai.tool.call.id` — the specific call id.
  中文翻译：`gen_ai.tool.call.id`——具体调用 id。
- `gen_ai.tool.description` — tool description (optional).
  中文翻译：`gen_ai.tool.description`——工具描述（可选）。

For agent spans:

> 对 Agent span：

- `gen_ai.agent.name` / `gen_ai.agent.id` / `gen_ai.agent.description`.
  中文翻译：`gen_ai.agent.name` / `gen_ai.agent.id` / `gen_ai.agent.description`——Agent 名/id/描述。

### Span kinds

- `SpanKind.CLIENT` for calls crossing a process boundary (LLM provider, MCP server).
  中文翻译：`SpanKind.CLIENT` 用于跨进程边界的调用（LLM 提供商、MCP 服务器）。
- `SpanKind.INTERNAL` for the agent's own loop steps and tool execution.
  中文翻译：`SpanKind.INTERNAL` 用于 Agent 自身的循环步骤和工具执行。

### Opt-in content capture

By default, spans carry metrics and timing — not prompts or completions. Large payloads and PII are off by default. Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` and specific content-capture env vars to include content. Review carefully before enabling in prod.

> 默认情况下，span 携带指标和计时——而非 prompt 或补全。大负载和 PII 默认关闭。设置 `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` 和特定内容捕获环境变量以包含内容。在生产中启用前仔细审查。

### Events on spans

Token-level events can be added as span events:

> Token 级事件可作为 span 事件添加：

- `gen_ai.content.prompt` — input messages.
  中文翻译：`gen_ai.content.prompt`——输入消息。
- `gen_ai.content.completion` — output messages.
  中文翻译：`gen_ai.content.completion`——输出消息。
- `gen_ai.content.tool_call` — tool call as recorded.
  中文翻译：`gen_ai.content.tool_call`——记录的工具调用。

Events time-order within a span for detailed replay.

> 事件在 span 内按时间排序，用于详细回放。

### Exporters

OTel spans export to:

- **Jaeger / Tempo.** OSS, on-prem.
  中文翻译：**Jaeger / Tempo。** 开源，本地部署。
- **Langfuse.** LLM-observability-specific; visualizes token usage.
  中文翻译：**Langfuse。** LLM 可观测性专用；可视化 token 使用。
- **Arize Phoenix.** Evals + tracing combined.
  中文翻译：**Arize Phoenix。** 评估+追踪结合。
- **Datadog.** Commercial; natively parses `gen_ai.*` attributes.
  中文翻译：**Datadog。** 商业；原生解析 `gen_ai.*` 属性。
- **Honeycomb.** Column-oriented; query-friendly.
  中文翻译：**Honeycomb。** 列式存储；查询友好。

All speak OTLP, the wire format. Your code does not care.

> 全部说 OTLP，线格式。你的代码不关心。

### Propagation across MCP

When an MCP client calls a server, inject the W3C traceparent header into the request. Streamable HTTP supports standard headers. Stdio does not carry HTTP headers natively; the spec's 2026 roadmap discusses adding a `_meta.traceparent` field on JSON-RPC calls.

> 当 MCP 客户端调用服务器时，将 W3C traceparent 头注入请求。Streamable HTTP 支持标准头。stdio 原生不携带 HTTP 头；规范 2026 路线图讨论在 JSON-RPC 调用上添加 `_meta.traceparent` 字段。

Until that ships: include the traceparent in the `_meta` of every request manually. Server logs the trace id.

> 直到那时：手动在每个请求的 `_meta` 中包含 traceparent。服务器记录 trace id。

### Metrics

Alongside spans, the GenAI semconv defines metrics:

> 除 span 外，GenAI 语义约定定义指标：

- `gen_ai.client.token.usage` — histogram.
  中文翻译：`gen_ai.client.token.usage`——直方图。
- `gen_ai.client.operation.duration` — histogram.
  中文翻译：`gen_ai.client.operation.duration`——直方图。
- `gen_ai.tool.execution.duration` — histogram.
  中文翻译：`gen_ai.tool.execution.duration`——直方图。

Use these for dashboards that do not need per-call detail.

> 用这些做不需要每调用详情的仪表盘。

### AgentOps layer

AgentOps (founded 2024) specializes in GenAI observability. It wraps popular frameworks (LangGraph, Pydantic AI, CrewAI) to emit OTel spans automatically. Useful if your stack uses a supported framework; use manual instrumentation otherwise.

> AgentOps（2024 年成立）专注 GenAI 可观测性。它包装流行框架（LangGraph、Pydantic AI、CrewAI）自动发出 OTel span。如果你的技术栈使用支持的框架则有用；否则使用手动仪表化。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 向 stdout 发射 OTLP-JSON 格式的 span，覆盖一个 Agent 调用 LLM、分发两个工具、进行一次 MCP 往返。无真实导出器——课程聚焦 span 形状和属性集。关注点：trace id 跨所有 span 共享；父子链接通过 parentSpanId 编码；`gen_ai.*` 必需属性已填充；内容捕获默认关闭。

`code/main.py` emits OTel-shaped spans to stdout (in OTLP-JSON-like format) for an agent that calls an LLM, dispatches two tools, and makes one MCP round-trip. No real exporter — the lesson focuses on the span shape and attribute set. Paste the output into an OTLP-compatible viewer or just read it.

> `code/main.py` 向 stdout 发出 OTel 形态的 span（OTLP-JSON 类格式），用于调用 LLM、分发两个工具、进行一次 MCP 往返的 Agent。无真实导出器——课程聚焦 span 形态和属性集。将输出粘贴到 OTLP 兼容查看器或直接阅读。

What to look at:

- Trace id is shared across all spans.
  中文翻译：Trace id 跨所有 span 共享。
- Parent-child links are encoded via `parentSpanId`.
  中文翻译：父子链接通过 `parentSpanId` 编码。
- Required `gen_ai.*` attributes are populated.
  中文翻译：必需的 `gen_ai.*` 属性已填充。
- Content capture is off by default; one scenario turns it on via env var.
  中文翻译：内容捕获默认关闭；一个场景通过环境变量开启。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-otel-genai-instrumentation.md`——给定 Agent 代码库，生成仪表化计划：在哪里添加 span、填充哪些属性、目标导出器。

This lesson produces `outputs/skill-otel-genai-instrumentation.md`. Given an agent codebase, the skill produces an instrumentation plan: where to add spans, which attributes to populate, and which exporters to target.

> 本课产出 `outputs/skill-otel-genai-instrumentation.md`。给定 Agent 代码库，该 skill 生成仪表化计划：在哪里加 span、填充哪些属性、目标哪些导出器。

## Exercises | 练习题

1. Run `code/main.py`. Count the spans and identify which is CLIENT vs INTERNAL.
   中文翻译：运行 `code/main.py`。计数 span 并识别哪些是 CLIENT vs INTERNAL。

2. Turn on content capture (env var) and confirm `gen_ai.content.prompt` and `gen_ai.content.completion` events appear. Note the implications for PII.
   中文翻译：开启内容捕获（环境变量）并确认 `gen_ai.content.prompt` 和 `gen_ai.content.completion` 事件出现。注意对 PII 的影响。

3. Add the tool-execution metric `gen_ai.tool.execution.duration` and emit it as a histogram sample per call.
   中文翻译：添加工具执行指标 `gen_ai.tool.execution.duration` 并每次调用作为直方图样本发出。

4. Propagate a traceparent from a parent agent span into an MCP request's `_meta.traceparent` field. Verify the MCP server would see the same trace id.
   中文翻译：将 traceparent 从父 Agent span 传播到 MCP 请求的 `_meta.traceparent` 字段。验证 MCP 服务器看到相同 trace id。

5. Read the OTel GenAI semconv spec. Identify one attribute listed in the semconv that this lesson's code does NOT emit. Add it.
   中文翻译：阅读 OTel GenAI 语义约定规范。识别语义约定中列出但本课代码未发出的一个属性。添加它。

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
  中文翻译：GenAI span、指标和事件的权威约定
- [OpenTelemetry — GenAI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/) — LLM and tool-execution span attribute list
  中文翻译：LLM 和工具执行 span 属性列表
- [OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) — agent-level `invoke_agent` span
  中文翻译：Agent 级 `invoke_agent` span
- [open-telemetry/semantic-conventions — GenAI spans](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md) — GitHub-hosted source of truth
  中文翻译：GitHub 托管的真相源
- [Datadog — LLM OTel semantic convention](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) — production integration walkthrough
  中文翻译：生产集成演练
