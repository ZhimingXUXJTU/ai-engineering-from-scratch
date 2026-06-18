# Capstone Lesson 28: Observability with OTel GenAI Spans and Prometheus Metrics | 可观测性 结业 指标 GenAI OpenTelemetry 欧盟

> An agent harness without observability is a black box that costs money. This lesson hand-rolls a span builder that emits records compliant with the OpenTelemetry GenAI semantic conventions, writes them to a JSON-Lines file one span per line, and exposes counters and histograms in Prometheus text format. The whole thing is stdlib Python and runs offline.

> **【中文解读】** 本节是综合项目——构建 OpenTelemetry 追踪可观测性。


**Type:** Build | **类型:** Build
**Languages:** Python (stdlib) | **语言:** Python (stdlib)
**Prerequisites:** Phase 19 · 25 (verification gates), Phase 19 · 26 (sandbox), Phase 19 · 27 (eval harness), Phase 13 · 20 (OpenTelemetry GenAI), Phase 14 · 23 (OTel GenAI conventions) | **前置知识:** Phase 19 · 25 (verification gates), Phase 19 · 26 (sandbox), Phase 19 · 27 (eval harness), Phase 13 · 20 (OpenTelemetry GenAI), Phase 14 · 23 (OTel GenAI conventions)

> 🔗 【前置】Agent Harness 9/10。参考 Phase 13·20（OTel GenAI）+ Phase 14·23（OTel 约定）。
> 💡 可观测性 = "黑盒的玻璃外壳"。手写 span builder 生成 OTel GenAI 兼容记录→JSON-Lines（一行一 span）+ Prometheus 计数器+直方图。纯 stdlib Python 离线跑。无观测的 harness=烧钱的黑盒。
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标

- Build a span data class shaped to the OpenTelemetry GenAI semantic conventions.
  中文翻译：Build a span data class shaped to the OpenTelemetry GenAI semantic conventions.
- Implement a JSONL exporter that writes one self-contained span per line.
  中文翻译：Implement a JSONL exporter that writes one self-contained span per line.
- Build counters and histograms with labels and Prometheus text-format exposition.
  中文翻译：Build counters and histograms with labels and Prometheus text-format exposition.
- Wrap any callable in a span context manager that records duration, status, and exceptions.
  中文翻译：Wrap any callable in a span context manager that records duration, status, and exceptions.
- Verify that the emitted spans roundtrip through `json.loads` and match the spec shape.
  中文翻译：Verify that the emitted spans roundtrip through `json.loads` and match the spec shape.

## The Problem | 问题

> **【中文解读】** 生产中的编码 Agent 每轮产生三类产物：模型调用、工具执行和验证门决策。没有结构化遥测，三类故障无法解决：1）缺失追踪——只有 500 行聊天日志，无工具运行记录、token 消耗和门拒绝信息；2）不可解析的追踪——使用自设字段名，Grafana/Honeycomb/Jaeger 无法读取；3）未聚合的度量——可以看到单个慢工具调用，但无法回答"read_file 调用过去一小时的 p95 延迟是多少？"

> **【拓展：OpenTelemetry GenAI 语义约定在 LLM 可观测性中的地位】** OpenTelemetry 的 GenAI 语义约定定义了标准属性键：`gen_ai.system`（提供商）、`gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.usage.output_tokens` 等。LangChain、LlamaIndex 和 Anthropic SDK 都在集成这些约定。本课从零构建的 span builder 教会你线路格式——生产中接入真正的 OTel SDK 后获得 OTLP 导出器、批处理和资源检测。

A coding agent in production produces three classes of artifact every turn: a model call, a tool execution, and a verification gate decision. None of these are useful without structured telemetry.

> 一个coding agent in production produces three classes of artifact every turn: a model call, a tool execution, and a verification gate decision. None of these are useful without structured telemetry.


The first failure mode is the missing trace. Something went wrong on Tuesday but the only record is a 500-line chat log. There is no record of which tool ran, how long it took, how many tokens went into the prompt, or whether the gate refused anything. The agent author has to guess.

> first failure mode is the missing trace. Something went wrong on Tuesday but the only record is a 500-line chat log. There is no record of which tool ran, how long it took, how many tokens went into the prompt, or whether the gate refused anything. The agent author has to guess.


The second failure mode is the unparseable trace. The harness wrote spans but used its own ad-hoc field names. Nothing in Grafana, Honeycomb, Jaeger, or the local CLI can read them. Whatever tooling exists in the team's stack is wasted because the spans are non-standard.

> second failure mode is the unparseable trace. The harness wrote spans but used its own ad-hoc field names. Nothing in Grafana, Honeycomb, Jaeger, or the local CLI can read them. Whatever tooling exists in the team's stack is wasted because the spans are non-standard.


The third failure mode is the unaggregated metric. You can see one slow tool call in the trace, but you cannot answer "what is the p95 latency of read_file calls over the last hour?" because there are no metrics, only traces.

> third failure mode is the unaggregated metric. You can see one slow tool call in the trace, but you cannot answer "what is the p95 latency of read_file calls over the last hour?" because there are no metrics, only traces.


The OpenTelemetry GenAI semantic conventions exist exactly for this. They define a small set of standard attributes that span emitters across LLM frameworks share. If your harness writes those attributes, every OTel-compatible backend can read them.

> OpenTelemetry GenAI semantic conventions exist exactly for this. They define a small set of standard attributes that span emitters across LLM frameworks share. If your harness writes those attributes, every OTel-compatible backend can read them.


## The Concept | 概念

> **【中文解读】** Harness 中的每个操作产生一个 span。Span 有 trace id（整个 Agent 调用）、span id（单个操作）、name（如 gen_ai.chat、gen_ai.tool.execution）、遵循 GenAI 约定的属性、起止时间和状态。导出器写入 JSONL——每行一个 JSON 对象，最简单且下游工具可流式读取、grep 和导入。度量与追踪并行：计数器记录每个工具调用次数，直方图记录延迟，两者序列化为 Prometheus 文本格式。

```mermaid
flowchart TD
  Call[tool call / model call / gate decision] --> Span["SpanBuilder.span()<br/>context manager"]
  Span --> GenAI[GenAISpan<br/>trace_id / span_id / name<br/>attributes:<br/>gen_ai.system<br/>gen_ai.request.*<br/>gen_ai.usage.*<br/>start, end, status]
  GenAI --> Writer[JSONLWriter]
  GenAI --> Metrics[MetricsRegistry]
  Writer --> Traces[traces.jsonl]
  Metrics --> Prom[/metrics text/]
```

Every operation in the harness produces a span. A span has a trace id (the whole agent invocation), a span id (this one operation), a name (e.g. `gen_ai.chat`, `gen_ai.tool.execution`), attributes that follow the GenAI conventions, a start and end time, and a status.

> 每个operation in the harness produces a span. A span has a trace id (the whole agent invocation), a span id (this one operation), a name (e.g. `gen_ai.chat`, `gen_ai.tool.execution`), attributes that follow the GenAI conventions, a start and end time, and a status.


The GenAI conventions standardise these attribute keys: `gen_ai.system` (which provider, e.g. `anthropic`, `openai`), `gen_ai.request.model` (the model id), `gen_ai.request.max_tokens`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.model`, `gen_ai.response.id`, `gen_ai.operation.name`, plus tool-specific keys `gen_ai.tool.name` and `gen_ai.tool.call.id`.

> GenAI conventions standardise these attribute keys: `gen_ai.system` (which provider, e.g. `anthropic`, `openai`), `gen_ai.request.model` (the model id), `gen_ai.request.max_tokens`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.model`, `gen_ai.response.id`, `gen_ai.operation.name`, plus tool-specific keys `gen_ai.tool.name` and `gen_ai.tool.call.id`.


The exporter writes JSONL. One JSON object per line. This is the simplest possible format that downstream tooling can stream, grep, and import. A real OTel exporter would speak OTLP gRPC; the lesson's JSONL exporter is the offline equivalent and exits zero on every workstation.

> exporter writes JSONL. One JSON object per line. This is the simplest possible format that downstream tooling can stream, grep, and import. A real OTel exporter would speak OTLP gRPC; the lesson's JSONL exporter is the offline equivalent and exits zero on every workstation.


Metrics live next to traces. A counter increments on each tool call: `tools_called_total{tool="read_file"}`. A histogram records the observed latency: `tool_latency_ms{tool="read_file"}`. Both serialise into Prometheus text exposition format, which is the de-facto standard for pull-based metrics.

> Metrics live next to traces.


## Architecture | 架构

> **【拓展：LLM 可观测性平台生态】** 2026 年的 LLM 可观测性平台包括：Langfuse（开源，追踪 + 评估）、Helicone（代理层追踪）、Arize AI（Phoenix，模型评估）、Braintrust（评估 + 日志）。它们都采用相同的架构：span-based 追踪 + 度量聚合 + 仪表板。本课的 JSONL 导出器 + Prometheus 文本格式是这些平台核心功能的从零构建版本，直接教会你它们的数据模型。

```mermaid
flowchart LR
  Harness[AgentHarness<br/>lessons 25-27] --> Span[SpanBuilder<br/>context mgr / attrs / status]
  Span --> Exporter[JSONLExporter<br/>traces.jsonl]
  Span --> Metrics[MetricsRegistry<br/>counters / histograms]
  Metrics --> Prom[Prometheus text<br/>exposition]
```

The span builder is a small class with a `span(name, attrs)` method that returns a context manager. The context manager records start time on enter, records end time on exit, attaches an exception if one was raised, and pushes the finalised span to the exporter.

> span builder is a small class with a `span(name, attrs)` method that returns a context manager. The context manager records start time on enter, records end time on exit, attaches an exception if one was raised, and pushes the finalised span to the exporter.


The metrics registry is two dicts. Counters are `{(name, frozen_labels): int}`. Histograms keep raw samples in a list and serialise to Prometheus histogram buckets at exposition time.

> metrics registry is two dicts. Counters are `{(name, frozen_labels): int}`. Histograms keep raw samples in a list and serialise to Prometheus histogram buckets at exposition time.


## What you will build

`main.py` ships:

1. `GenAISpan` dataclass: trace_id, span_id, parent_span_id, name, attributes, start_unix_nano, end_unix_nano, status, status_message, events.
2. `SpanBuilder` class with `span(name, attrs, parent=None)` context manager.
3. `JSONLExporter` class with `export(span)` that appends one line.
4. `Counter` and `Histogram` classes plus `MetricsRegistry`.
5. `prometheus_exposition(registry)` that produces text-format output.
6. `wrap_tool_call(name)` decorator that emits a span and updates metrics.
7. Demo: synthesises a complete agent invocation (gen_ai.chat span around tool spans), writes traces.jsonl, prints the Prometheus exposition, exits zero.

The span id and trace id are 16-byte hex strings, generated from `os.urandom`. That matches OTel's W3C trace context. The exporter never throws; IO errors are surfaced but the harness keeps running.

> span id and trace id are 16-byte hex strings, generated from `os.urandom`. That matches OTel's W3C trace context. The exporter never throws; IO errors are surfaced but the harness keeps running.


The histogram has a fixed bucket set (the OTel default for latency in milliseconds: 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, +Inf). Samples are stored as a list; exposition computes per-bucket counts on demand.

> histogram has a fixed bucket set (the OTel default for latency in milliseconds: 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, +Inf). Samples are stored as a list; exposition computes per-bucket counts on demand.


## Why hand-rolled instead of opentelemetry-sdk

> **【中文解读】** OTel Python SDK 是几千行代码、需要多进程运行 OTLP 导出器、运行时代价超过课程预算。手写版本教授线路格式——生产中将相同属性接入真正 SDK 获得 OTLP 导出器和批处理。语义约定是稳定的——本课发出的线路格式在 2030 年仍能被解析，因为 OTel 永远不会破坏 GenAI 属性名，只会添加新的。

The OTel Python SDK is a real dependency. It is also several thousand lines of code, multiple processes for the OTLP exporter, and a runtime cost that swamps a lesson budget. The hand-rolled version teaches the wire format. In production you wire the same attributes into the real SDK and get the OTLP exporter, batching, and resource detection for free.

> OTel Python SDK is a real dependency. It is also several thousand lines of code, multiple processes for the OTLP exporter, and a runtime cost that swamps a lesson budget. The hand-rolled version teaches the wire format. In production you wire the same attributes into the real SDK and get the OTLP exporter, batching, and resource detection for free.


The conventions are stable. The wire format the lesson emits will keep parsing in 2030 because OTel never breaks GenAI attribute names; they only add new ones.

> conventions are stable. The wire format the lesson emits will keep parsing in 2030 because OTel never breaks GenAI attribute names; they only add new ones.


## How this composes with the rest of Track A

Lesson 25 produced the gate chain. Lesson 26 produced the sandbox. Lesson 27 produced the eval harness. Lesson 28 makes all three observable. Lesson 29 wraps every step of the end-to-end demo in spans and prints the Prometheus text at the end.

> Lesson 25 produced the gate chain.


## Running it | 运行

```bash
cd phases/19-capstone-projects/28-observability-otel-traces
python3 code/main.py
python3 -m pytest code/tests/ -v
```

The demo emits a `traces.jsonl` in the lesson's working dir (cleaned up at the end), then prints a sample of three spans, then prints the Prometheus exposition for the counters and histograms. The tests verify that spans serialise round-trip, that the canonical GenAI attributes are present, that counters increment correctly, and that the histogram exposition contains the expected bucket counts.

> demo emits a `traces.jsonl` in the lesson's working dir (cleaned up at the end), then prints a sample of three spans, then prints the Prometheus exposition for the counters and histograms. The tests verify that spans serialise round-trip, that the canonical GenAI attributes are present, that counters increment correctly, and that the histogram exposition contains the expected bucket counts.

