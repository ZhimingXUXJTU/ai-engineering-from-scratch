# 约定 GenAI METR

> OpenTelemetry's GenAI SIG (launched April 2024) defines the standard schema for agent telemetry. Span names, attributes, and content-capture rules converge across vendors so agent traces mean the same thing in Datadog, Grafana, Jaeger, and Honeycomb.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms)
**预计时间：** ~60 minutes

## 学习目标

- Name the GenAI span categories: model/client, agent, tool.
- Distinguish `invoke_agent` CLIENT vs INTERNAL spans and when each applies.
- List the top-level GenAI attributes: provider name, request model, data-source ID.
- Explain the content-capture contract: opt-in, `OTEL_SEMCONV_STABILITY_OPT_IN`, external-reference recommendation.

## 问题引入

> **【中文解读】** 每个供应商都发明自己的 span 名称，运维团队最终需要为每个框架构建独立的仪表盘。OpenTelemetry 的 GenAI SIG 通过定义一个全生态系统的标准来解决这个问题。
> **【拓展：OTel GenAI 规范的跨平台统一】** OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义了 Agent 遥测的标准 Schema：span 名称、属性和内容捕获规则跨供应商统一，使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义。一次埋点，多后端通用。

## 核心概念

### Span categories
1. **Model / client spans.** Cover raw LLM calls. Emitted by provider SDKs (Anthropic, OpenAI, Bedrock) and framework model adapters.
2. **Agent spans.** `create_agent` (when the agent is constructed) and `invoke_agent` (when it runs).
3. **Tool spans.** One per tool invocation; connected to the agent span by parent-child relation.
### Agent span naming
- Span name: `invoke_agent {gen_ai.agent.name}` if named; fallback to `invoke_agent`.
- Span kind:
  - **CLIENT** — for remote agent services (OpenAI Assistants API, Bedrock Agents).
  - **INTERNAL** — for in-process agent frameworks (LangChain, CrewAI, local ReAct).
### Key attributes
- `gen_ai.provider.name` — `anthropic`, `openai`, `aws.bedrock`, `google.vertex`.
- `gen_ai.request.model` — the model ID.
- `gen_ai.response.model` — the resolved model (may differ from request due to routing).
- `gen_ai.agent.name` — agent identifier.
- `gen_ai.operation.name` — `chat`, `completion`, `invoke_agent`, `tool_call`.
- `gen_ai.data_source.id` — for RAG: which corpus or store was consulted.
Technology-specific conventions exist for Anthropic, Azure AI Inference, AWS Bedrock, OpenAI.
### Content capture
The default rule: instrumentations SHOULD NOT capture inputs/outputs by default. Capture is opt-in via:
- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`
Recommended production pattern: store content externally (S3, your log store), record references on spans (pointer IDs, not prose). This is the Lesson 27 content-poisoning defense wired into observability.
### Stability
Most conventions are experimental as of March 2026. Opt in to the stable preview with:
```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```
Datadog v1.37+ maps GenAI attributes natively into its LLM Observability schema. Other backends (Grafana, Honeycomb, Jaeger) support the raw attributes.
### Where this pattern goes wrong
- **Capturing full prompts in spans.** PII, secrets, customer data in traces that ops can read. Store externally.
- **No `gen_ai.provider.name`.** Multi-provider dashboards break when attribution is missing.
- **Spans without parent links.** Orphaned tool spans. Always propagate context.
- **Not setting stability opt-in.** Your attributes may get renamed on backend upgrade.

## 动手实现

`code/main.py` implements a stdlib span emitter matching GenAI conventions:
- `Span` with GenAI attribute schema.
- `Tracer` with `start_span`, nested contexts.
- A scripted agent run that emits: `create_agent`, `invoke_agent` (INTERNAL), per-tool spans, `chat` spans for LLM calls.
- A content-capture mode that stores prompts externally and records IDs on spans.
Run it:
```
python3 code/main.py
```
Output: a span tree with all required GenAI attributes, and an "external store" showing the opt-in content references.

## 用框架实现

- **Datadog LLM Observability** (v1.37+) maps attributes natively.
- **Langfuse / Phoenix / Opik** (Lesson 24) — auto-instrument the ecosystem.
- **Jaeger / Honeycomb / Grafana Tempo** — raw OTel traces; build dashboards from GenAI attributes.
- **Self-hosted** — run the OTel Collector with a GenAI processor.

## 产出物

`outputs/skill-otel-genai.md` wires OTel GenAI spans into an existing agent with content-capture defaults and external-reference storage.

## 练习题

1. Instrument your Lesson 01 ReAct loop with `invoke_agent` (INTERNAL) + per-tool spans. Send to a Jaeger instance.
   *思考并实践此练习*
2. Add content capture in "references only" mode: prompts to SQLite, span attributes carry only row IDs.
   *思考并实践此练习*
3. Read the spec for `gen_ai.data_source.id`. Wire it into your Lesson 09 Mem0 search.
   *思考并实践此练习*
4. Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` and verify your attributes don't get renamed by the collector.
   *思考并实践此练习*
5. Build a dashboard: "which tool errors correlate with which models" from GenAI attributes alone.
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| GenAI SIG | "OpenTelemetry GenAI group" |
| invoke_agent | "Agent span" |
| CLIENT span | "Remote call" |
| INTERNAL span | "In-process" |
| gen_ai.provider.name | "Provider" |
| gen_ai.data_source.id | "RAG source" |
| Content capture | "Prompt logging" |
| Stability opt-in | "Preview mode" |

## 延伸阅读

