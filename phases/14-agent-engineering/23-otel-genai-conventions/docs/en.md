# OpenTelemetry GenAI Semantic Conventions | 约定 GenAI METR

> OpenTelemetry's GenAI SIG (launched April 2024) defines the standard schema for agent telemetry. Span names, attributes, and content-capture rules converge across vendors so agent traces mean the same thing in Datadog, Grafana, Jaeger, and Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Name the GenAI span categories: model/client, agent, tool.
- Distinguish `invoke_agent` CLIENT vs INTERNAL spans and when each applies.
- List the top-level GenAI attributes: provider name, request model, data-source ID.
- Explain the content-capture contract: opt-in, `OTEL_SEMCONV_STABILITY_OPT_IN`, external-reference recommendation.

## The Problem | 问题引入

> **【中文解读】** 每个供应商都发明自己的 span 名称，运维团队最终需要为每个框架构建独立的仪表盘。OpenTelemetry 的 GenAI SIG 通过定义一个全生态系统的标准来解决这个问题。

Every vendor invents their own span names. Ops teams end up building per-framework dashboards. OpenTelemetry's GenAI SIG fixes this by defining one standard the whole ecosystem targets.

> 每个供应商都发明自己的 span 名称。运维团队最终需要为每个框架构建独立的仪表盘。OpenTelemetry 的 GenAI SIG 通过定义一个全生态系统遵循的标准来解决这个问题。

> **【拓展：OTel GenAI 规范的跨平台统一】** OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义了 Agent 遥测的标准 Schema：span 名称、属性和内容捕获规则跨供应商统一，使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义。一次埋点，多后端通用。

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·01（Agent Loop）——你需要先有 Agent 才能给它埋点；Phase 14·13（LangGraph）——理解状态图，因为 span 的父子层级就是图遍历的镜像。如果完全没接触过 OpenTelemetry（不知道什么是 span、trace、context propagation），先去看 OTel 官方 Python 快速入门——本节只讲 GenAI 专属约定，不重讲 OTel 基础。

## The Concept | 核心概念

### Span categories

> 💡 **【类比】** OTel GenAI 的三类 span 像医院的分级诊疗记录：**Model span** 是化验单（最底层，记录"抽了多少血、用什么仪器、结果多少"——对应 token 数、模型名、延迟）；**Agent span** 是门诊病历（这次看病从挂号到离开的全过程，包含多次化验）；**Tool span** 是检查项目（心电图、CT，每次都是独立的一次操作）。父子里包含多次子记录，子记录通过 `parent_span_id` 链回父记录——这样 Datadog 里你能展开看：整个 Agent 调用 → 5 次工具调用 → 每次工具调用里 2 次 LLM 调用。

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

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

### Content capture

The default rule: instrumentations SHOULD NOT capture inputs/outputs by default. Capture is opt-in via:

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

Recommended production pattern: store content externally (S3, your log store), record references on spans (pointer IDs, not prose). This is the Lesson 27 content-poisoning defense wired into observability.

> 推荐的生产模式：将内容外部存储（S3、你的日志存储），在 span 上记录引用（指针 ID，不是原文）。这就是将第 27 课内容投毒防御整合到可观测性中。

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

### Stability

Most conventions are experimental as of March 2026. Opt in to the stable preview with:

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

Datadog v1.37+ maps GenAI attributes natively into its LLM Observability schema. Other backends (Grafana, Honeycomb, Jaeger) support the raw attributes.

> Datadog v1.37+ 原生将 GenAI 属性映射到其 LLM Observability schema。其他后端（Grafana、Honeycomb、Jaeger）支持原始属性。

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

### Where this pattern goes wrong

- **Capturing full prompts in spans.** PII, secrets, customer data in traces that ops can read. Store externally.
- **No `gen_ai.provider.name`.** Multi-provider dashboards break when attribution is missing.
- **Spans without parent links.** Orphaned tool spans. Always propagate context.
- **Not setting stability opt-in.** Your attributes may get renamed on backend upgrade.

> **在 span 中捕获完整提示。** 运维可以读取的追踪中包含 PII、密钥、客户数据。外部存储。
> **缺少 `gen_ai.provider.name`。** 缺少归属时，多供应商仪表盘会出错。
> **没有父链接的 span。** 孤立的工具 span。始终传播上下文。
> **不设置稳定性选择加入。** 你的属性可能在后端升级时被重命名。

## Build It | 动手实现

`code/main.py` implements a stdlib span emitter matching GenAI conventions:

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

- `Span` with GenAI attribute schema.
- `Tracer` with `start_span`, nested contexts.
- A scripted agent run that emits: `create_agent`, `invoke_agent` (INTERNAL), per-tool spans, `chat` spans for LLM calls.
- A content-capture mode that stores prompts externally and records IDs on spans.

Run it:

```
python3 code/main.py
```

Output: a span tree with all required GenAI attributes, and an "external store" showing the opt-in content references.

> 输出：一个包含所有必需 GenAI 属性的 span 树，以及一个显示选择加入内容引用的"外部存储"。

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

## Use It | 用框架实现

- **Datadog LLM Observability** (v1.37+) maps attributes natively.
- **Langfuse / Phoenix / Opik** (Lesson 24) — auto-instrument the ecosystem.
- **Jaeger / Honeycomb / Grafana Tempo** — raw OTel traces; build dashboards from GenAI attributes.
- **Self-hosted** — run the OTel Collector with a GenAI processor.

## Ship It | 产出物

`outputs/skill-otel-genai.md` wires OTel GenAI spans into an existing agent with content-capture defaults and external-reference storage.

> `outputs/skill-otel-genai.md` 将 OTel GenAI span 接入现有 Agent，包含内容捕获默认值和外部引用存储。

> OpenTelemetry GenAI 语义约定定义了 LLM 和 Agent 的可观测性标准。关键属性包括 `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.agent.name` 等。

## Exercises | 练习题

1. Instrument your Lesson 01 ReAct loop with `invoke_agent` (INTERNAL) + per-tool spans. Send to a Jaeger instance.
  中文翻译：思考并实践此练习。
2. Add content capture in "references only" mode: prompts to SQLite, span attributes carry only row IDs.
  中文翻译：思考并实践此练习。
3. Read the spec for `gen_ai.data_source.id`. Wire it into your Lesson 09 Mem0 search.
  中文翻译：思考并实践此练习。
4. Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` and verify your attributes don't get renamed by the collector.
  中文翻译：思考并实践此练习。
5. Build a dashboard: "which tool errors correlate with which models" from GenAI attributes alone.
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## Further Reading | 延伸阅读

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the spec
  中文翻译：见原文。
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — GenAI spans by default
  中文翻译：见原文。
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) — OTel spans built in
  中文翻译：见原文。
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) — W3C trace context propagation
  中文翻译：见原文。
