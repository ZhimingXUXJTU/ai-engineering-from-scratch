# Agent Observability: Langfuse, Phoenix, Opik | 可观测性 美国

> Three open-source agent observability platforms dominate 2026. Langfuse (MIT) — 6M+ installs/month, tracing + prompt management + evals + session replay. Arize Phoenix (Elastic 2.0) — deep agent-specific evals, RAG relevancy, OpenInference auto-instrumentation. Comet Opik (Apache 2.0) — automated prompt optimization, guardrails, LLM-judge hallucination detection.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 23 (OTel GenAI) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Name the three top open-source agent observability platforms and their licenses.
- Distinguish what each one is strongest at: Langfuse (prompt mgmt + sessions), Phoenix (RAG + auto-instrumentation), Opik (optimization + guardrails).
- Explain why 89% of organizations report having agent observability in place by 2026.
- Implement a stdlib trace-to-dashboard pipeline with LLM-judge evaluation.

## The Problem | 问题引入

OTel GenAI (Lesson 23) gives you the schema. You still need the platform that ingests spans, runs evaluations, stores prompt versions, and surfaces regressions. The three contenders each emphasize different parts of the lifecycle.


> **【中文解读】** Agent 可观测性平台提供对 Agent 执行的端到端可见性——从用户请求到最终响应的每一步。核心能力：追踪（每步执行记录）、指标（延迟/成本/成功率）、日志（详细执行过程）。主要平台包括 LangSmith、AgentOps、Braintrust 和 Phoenix。

## The Concept | 核心概念

### Langfuse (MIT)

- 6M+ SDK installs/month, 19k+ GitHub stars.
- Features: tracing, prompt management with versioning + playground, evaluations (LLM-as-judge, user feedback, custom), session replays.
- June 2025: formerly commercial modules (LLM-as-a-judge, annotation queues, prompt experiments, Playground) open-sourced under MIT.
- Strongest for: end-to-end observability with tight prompt-management loop.

### Arize Phoenix (Elastic License 2.0)

- Deeper agent-specific evaluation: trace clustering, anomaly detection, retrieval relevancy for RAG.
- Native OpenInference auto-instrumentation.
- Pairs with managed Arize AX for production.
- No prompt versioning — positioned as a drift/behavioral-regression tool alongside broader platforms.
- Strongest for: RAG relevancy, behavioral drift, anomaly detection.

### Comet Opik (Apache 2.0)

- Automated prompt optimization through A/B experiments.
- Guardrails (PII redaction, topical constraints).
- LLM-judge hallucination detection.
- Benchmark from Comet's own measurement: Opik logs + evals in 23.44s vs Langfuse 327.15s (~14x gap) — take vendor benchmarks as directional.
- Strongest for: optimization loop, automated experimentation, guardrail enforcement.

### Industry data

Per Maxim (2026 field analysis): 89% of organizations have agent observability in place; quality issues are the top production barrier (32% of respondents cite them).

> Agent 可观测性平台提供运行时追踪、指标监控和调试工具。Langfuse、Arize Phoenix、Braintrust 是 2026 年主要的 Agent 可观测性工具。

### Picking one

| Need | Pick |
|------|------|
| All-in-one with prompt management | Langfuse |
| Deep RAG evaluation + drift | Phoenix |
| Automated optimization + guardrails | Opik |
| Open licensing, no ELv2 | Langfuse (MIT) or Opik (Apache 2.0) |
| Datadog / New Relic integration | Any — they all export OTel |

### Where this pattern goes wrong

- **No eval strategy.** Tracing without evaluation is just expensive logging.
- **Self-rolled LLM-judge without grounding.** CRITIC pattern (Lesson 05) applies — judges need external tools for factual verification.
- **Prompt versions not tied to traces.** When prod regresses, you cannot bisect to the prompt that caused it.

## Build It | 动手实现

`code/main.py` implements a stdlib trace collector + LLM-judge evaluator:

> Agent 可观测性平台提供运行时追踪、指标监控和调试工具。Langfuse、Arize Phoenix、Braintrust 是 2026 年主要的 Agent 可观测性工具。

- Ingest GenAI-shaped spans.
- Group by session, tag failed runs (guardrail trips, low-confidence evals).
- A scripted LLM-judge that scores agent responses on a rubric.
- A dashboard-like summary: failure rate, top failure reasons, eval score distribution.

Run it:

```
python3 code/main.py
```

Output: per-session eval scores and failure categorization matching what Langfuse/Phoenix/Opik would show.

> Agent 可观测性平台提供运行时追踪、指标监控和调试工具。Langfuse、Arize Phoenix、Braintrust 是 2026 年主要的 Agent 可观测性工具。

## Use It | 用框架实现

- **Langfuse** self-hosted or cloud; wire via OTel or their SDK.
- **Arize Phoenix** self-hosted; auto-instrument OpenInference.
- **Comet Opik** self-hosted or cloud; automated optimization loop.
- **Datadog LLM Observability** for mixed ops+ML teams that already run Datadog.

## Ship It | 产出物

`outputs/skill-obs-platform-wiring.md` picks a platform and wires traces + evals + prompt versions into an existing agent.

> Agent 可观测性平台提供运行时追踪、指标监控和调试工具。Langfuse、Arize Phoenix、Braintrust 是 2026 年主要的 Agent 可观测性工具。

## Exercises | 练习题

1. Export a week of OTel traces to Langfuse cloud (free tier). Which sessions failed? Why?
  中文翻译：思考并实践此练习。
2. Write an LLM-judge rubric for your domain (factual correctness, tone, scope adherence). Test on 50 traces.
  中文翻译：思考并实践此练习。
3. Compare Langfuse prompt versioning against Phoenix's trace clustering. Which tells you what broke faster?
  中文翻译：思考并实践此练习。
4. Read Opik's guardrail docs. Wire a PII redaction guardrail to one of your agent runs.
  中文翻译：思考并实践此练习。
5. Benchmark the three on your corpus. Ignore vendor-published numbers; measure your own.
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Tracing | "Spans collector" | Ingest OTel / SDK spans; index by session |  |
| Prompt management | "Prompt CMS" | Versioned prompts tied to traces |  |
| LLM-as-judge | "Automated eval" | Separate LLM scores agent output against a rubric |  |
| Session replay | "Trace playback" | Step through past runs for debugging |  |
| RAG relevancy | "Retrieval quality" | Does the retrieved context match the query |  |
| Trace clustering | "Behavioral grouping" | Cluster similar runs for drift detection |  |
| Guardrail enforcement | "Policy at log time" | PII/toxicity/scope checks on logged content |  |

## Further Reading | 延伸阅读

- [Langfuse docs](https://langfuse.com/) — tracing, evals, prompt mgmt
  中文翻译：见原文。
- [Arize Phoenix docs](https://docs.arize.com/phoenix) — auto-instrumentation, drift
  中文翻译：见原文。
- [Comet Opik](https://www.comet.com/site/products/opik/) — optimization + guardrails
  中文翻译：见原文。
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the schema all three consume
  中文翻译：见原文。
