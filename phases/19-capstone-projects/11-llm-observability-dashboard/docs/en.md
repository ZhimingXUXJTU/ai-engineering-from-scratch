# Capstone 11 — LLM Observability & Eval Dashboard | 可观测性 仪表板 结业 评估 LLM

> Langfuse went open-core. Arize Phoenix published the 2026 GenAI semconv mappings. Helicone and Braintrust both doubled down on per-user cost attribution. Traceloop's OpenLLMetry became the de-facto SDK instrumentation. The production shape is ClickHouse for traces, Postgres for metadata, Next.js for UI, and a small army of eval jobs (DeepEval, RAGAS, LLM-judge) running over sampled traces. Build one self-hosted, ingest from at least four SDK families, and demonstrate catching an injected regression in under five minutes.

> **【中文解读】** 本节是综合项目——构建 LLM 可观测性仪表板，实时监控 Agent 性能和成本。


**Type:** Capstone
**Languages:** TypeScript (UI), Python / TypeScript (ingest + evals), SQL (ClickHouse)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools), Phase 17 (infrastructure), Phase 18 (safety)
**Phases exercised:** P11 · P13 · P17 · P18
**Time:** 25 hours

## Problem

> **【中文解读】** 本节描述 LLM 可观测性的核心需求。2026 年每个运行生产流量的 AI 团队都需要一个可观测性平台：成本归因、幻觉检测、漂移监控、越狱信号、SLO 仪表盘、PII 泄漏告警。开源方案（Langfuse、Phoenix、OpenLLMetry）已统一到 OpenTelemetry GenAI 语义约定作为摄取模式。核心挑战是：给定一个故意注入的回归（提示开始产生 PII），仪表盘在 5 分钟内捕获并告警。

> **【拓展：LLM 可观测性工具生态】** 2026 年主要工具：Langfuse（开源核心，追踪+评估）、Arize Phoenix（漂移监控强项）、Helicone（每用户成本归因）、Braintrust（评估优先平台）、Traceloop OpenLLMetry（事实上的 SDK 自动仪器化）。统一基础是 OpenTelemetry GenAI 语义约定，支持 OpenAI/Anthropic/Google/LangChain/LlamaIndex/vLLM 一键仪器化。存储层通常用 ClickHouse 做 span 分析，Postgres 存元数据，S3 存原始事件归档。

Every AI team running production traffic in 2026 keeps an observability plane alongside the model. Cost attribution. Hallucination detection. Drift monitoring. Jailbreak signal. SLO dashboards. PII leak alerts. The open-source references — Langfuse, Phoenix, OpenLLMetry — converged on OpenTelemetry GenAI semantic conventions as the ingest schema. You can now instrument OpenAI, Anthropic, Google, LangChain, LlamaIndex, and vLLM with one SDK and ship compatible spans.

You will build a self-hosted dashboard that ingests from at least four SDK families, runs a small set of eval jobs over sampled traces, detects drift, and alerts. The measurement bar: given a deliberately injected regression (a prompt that starts producing PII), the dashboard catches it and fires an alert in under five minutes.

## Concept

> **【中文解读】** 摄取通过 OTLP HTTP，SDK 产生 GenAI 语义约定 span（gen_ai.system、gen_ai.request.model、input/output tokens 等）。Span 存入 ClickHouse 做列式分析，元数据存入 Postgres。评估作业对采样追踪运行 DeepEval（忠实度/毒性/答案相关性）、RAGAS（检索指标）和自定义 LLM 评委（PII 泄漏/策略违规）。漂移检测监控嵌入空间分布变化（PSI 或 KL 散度），告警通过 Prometheus Alertmanager 路由到 Slack/PagerDuty。

> **【拓展：漂移检测与 MTTR】** 漂移检测使用 PSI（Population Stability Index）比较本周与过去 4 周的提示嵌入分布，PSI > 0.2 通常表示有意义的漂移。MTTR（平均恢复时间）是可观测性的核心指标——从缺陷部署到 Slack 告警的时间。生产系统目标 MTTR < 5 分钟。尾采样策略保留 100% 的错误追踪 + 10% 的成功追踪，平衡成本和可观测性。1k span/秒的持续摄取是基本性能要求。

Ingest is OTLP HTTP. The SDK produces GenAI-semconv spans: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.response.id`, `llm.prompts`, `llm.completions`. Spans land in ClickHouse for columnar analytics; metadata (users, sessions, apps) lands in Postgres.

Evals run as batch jobs over sampled traces. DeepEval scores faithfulness, toxicity, and answer relevance. RAGAS scores retrieval metrics when the trace carries retrieval context. Custom LLM-judges run domain-specific checks (PII leak, off-policy response). Eval runs write back to the same ClickHouse as eval spans linked to the parent trace.

Drift detection watches embedding-space distributions over time (PSI or KL divergence on prompt embeddings) plus eval-score trends. Alerts feed Prometheus Alertmanager and then Slack / PagerDuty. The UI is Next.js 15 with Recharts.

## Architecture | 架构

```
production apps:
  OpenAI SDK  +  Anthropic SDK  +  Google GenAI SDK
  LangChain + LlamaIndex + vLLM
       |
       v
  OpenTelemetry SDK with GenAI semconv
       |
       v  OTLP HTTP
  collector (ingest, sample, fan-out)
       |
       +-------------+-----------+
       v             v           v
   ClickHouse    Postgres    S3 archive
   (spans)       (metadata)  (raw events)
       |
       +---> eval jobs (DeepEval, RAGAS, LLM-judge)
       |     sampled or all-trace
       |     write eval spans back
       |
       +---> drift detector (PSI / KL on prompt embeddings)
       |
       +---> Prometheus metrics -> Alertmanager -> Slack / PagerDuty
       |
       v
   Next.js 15 dashboard (Recharts)
```

## Stack

- Ingest: OpenTelemetry SDKs + GenAI semantic conventions; OTLP HTTP transport
- Collector: OpenTelemetry Collector with tail-sampling processor (for cost control)
- Storage: ClickHouse for spans, Postgres for metadata, S3 for raw event archive
- Evals: DeepEval, RAGAS 0.2, Arize Phoenix evaluator pack, custom LLM-judge
- Drift: PSI / KL on pooled prompt embeddings (sentence-transformers) weekly
- Alerting: Prometheus Alertmanager -> Slack / PagerDuty
- UI: Next.js 15 App Router + Recharts + server actions
- SDKs supported out of the box: OpenAI, Anthropic, Google GenAI, LangChain, LlamaIndex, vLLM

## Build It | 动手构建

> **【中文解读】** 构建 LLM 可观测性仪表板的 8 个阶段：OTel Collector 配置（100% 错误追踪 + 10% 成功采样）、ClickHouse schema（GenAI 语义约定列）、成本仪表板（按模型/用户/应用聚合 token 和美元）、质量仪表板（幻觉率和工具成功率）、延迟热力图、用户级审计追踪、告警规则和 SLO 仪表板。

> **【拓展：LLM 可观测性在 2026 年的关键指标】** Braintrust、Langfuse、Helicone 等平台追踪的核心指标：1）token 成本（input/output/推理 分别计费）；2）幻觉率（通过自动验证或用户反馈检测）；3）P50/P95/P99 延迟（特别是首 token 延迟 TTFT）；4）工具调用成功率（Agent 场景特有）；5）用户满意度（thumbs up/down 或 implicit signal）。本课的 ClickHouse + Grafana 架构是这些平台的开源自建替代。

1. **Collector config.** OpenTelemetry Collector with the OTLP HTTP receiver, a tail-sampler keeping 100% of errored traces and 10% of successes, and exporters to ClickHouse and S3.

2. **ClickHouse schema.** Table `spans` with columns mirroring GenAI semconv: `gen_ai_system`, `gen_ai_request_model`, `input_tokens`, `output_tokens`, `latency_ms`, `prompt_hash`, `trace_id`, `parent_span_id`, plus JSON bag for long payloads. Add secondary indexes by user_id and app_id.

3. **SDK coverage test.** Write a small client app using each SDK (OpenAI, Anthropic, Google, LangChain, LlamaIndex, vLLM) with OpenLLMetry auto-instrument. Verify each produces canonical GenAI spans that land in ClickHouse.

4. **Eval jobs.** A scheduled job reads last-15-min sampled traces and runs DeepEval faithfulness, toxicity, and answer relevance. Outputs are eval spans linked to the parent trace.

5. **Custom LLM-judge.** A PII-leak judge: given a response, call a guard LLM to score likelihood of PII leak. High-score responses land in a triage queue.

6. **Drift detection.** Weekly job computes PSI between this week's pooled prompt embeddings and the trailing 4-week baseline. If PSI above threshold, alert.

7. **Dashboard.** Next.js 15 with pages: overview (spans/sec, cost/user, p95 latency), traces (search + waterfall), evals (faithfulness trend, toxicity), drift (PSI over time), alerts.

8. **Alerting chain.** Prometheus exporter reads eval score aggregates and latency percentiles; Alertmanager routes to Slack for warnings and PagerDuty for critical breaches.

9. **Regression probe.** Inject a bug: the evaluated chatbot starts leaking fake SSNs 1% of the time. Measure MTTR: from bug deployed to Slack alert.

## Use It | 使用方法

```
$ curl -X POST https://my-otel-collector/v1/traces -d @trace.json
[collector]  accepted 1 trace, 3 spans
[clickhouse] inserted 3 spans (app=chat, user=u_42)
[eval]       DeepEval faithfulness 0.82, toxicity 0.03
[drift]      weekly PSI 0.08 (below 0.2 threshold)
[ui]         live at https://obs.example.com
```

## Ship It | 部署上线

`outputs/skill-llm-observability.md` is the deliverable. Given an LLM application, the dashboard ingests its traces, runs evals, alerts on drift, and surfaces cost/user breakdown in Next.js.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Trace-schema coverage | Number of SDK families producing canonical GenAI spans (target: 6+) |
| 20 | Eval correctness | DeepEval / RAGAS scores vs hand-labeled set |
| 20 | Dashboard UX | MTTR on injected regression (under 5 minutes target) |
| 20 | Cost / scale | Sustained ingest at 1k spans/sec without backlog |
| 15 | Alerting + drift detection | Prometheus/Alertmanager chain exercised end to end |
| **100** | | |

## Exercises | 练习题

1. Add custom instrumentation for the Haystack framework. Verify canonical spans land in ClickHouse with faithful `gen_ai.*` attributes.

2. Swap DeepEval for Phoenix evaluators on the same traces. Measure score drift between the two eval engines.

3. Sharpen the drift detector: compute PSI per app-id rather than globally. Show per-app drift trails.

4. Add a "user impact" page: cost-per-user and failure-rate-per-user with sparklines.

5. Build a tail-sampling policy that keeps 100% of traces with toxicity > 0.5 plus a 10% stratified sample of the rest. Measure sampling bias introduced.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| GenAI semconv | "OTel LLM attributes" | 2025 OpenTelemetry spec for LLM span attributes (system, model, tokens) |
| Tail sampling | "Post-trace sample" | Collector decides to keep or drop a trace after it completes (can peek errors) |
| PSI | "Population stability index" | Drift metric comparing two distributions; > 0.2 typically signals meaningful drift |
| LLM-judge | "Eval as model" | An LLM scoring another LLM's output on a rubric (faithfulness, toxicity, PII) |
| Tail-sampling policy | "Keep-rule" | Rule that decides which traces to persist vs drop; errored + sample-rate |
| Eval span | "Linked eval trace" | Child span carrying an eval score linked to the original LLM call span |
| Cost per user | "Unit economics" | Dollar cost attributed to a user_id over a window; key product metric |

## Further Reading | 延伸阅读

- [Langfuse](https://github.com/langfuse/langfuse) — the reference open-core observability platform
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — alternate reference with strong drift support
- [OpenLLMetry (Traceloop)](https://github.com/traceloop/openllmetry) — auto-instrumentation SDK family
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the ingest schema
- [Helicone](https://www.helicone.ai) — alternate hosted observability
- [Braintrust](https://www.braintrust.dev) — alternate eval-first platform
- [ClickHouse documentation](https://clickhouse.com/docs) — columnar span store
- [DeepEval](https://github.com/confident-ai/deepeval) — evaluator library
