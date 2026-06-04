# 可观测性 美国

> Three open-source agent observability platforms dominate 2026. Langfuse (MIT) — 6M+ installs/month, tracing + prompt management + evals + session replay. Arize Phoenix (Elastic 2.0) — deep agent-specific evals, RAG relevancy, OpenInference auto-instrumentation. Comet Opik (Apache 2.0) — automated prompt optimization, guardrails, LLM-judge hallucination detection.


**类型：** 学习
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 23 (OTel GenAI)
**预计时间：** ~45 minutes

## 学习目标

- Name the three top open-source agent observability platforms and their licenses.
- Distinguish what each one is strongest at: Langfuse (prompt mgmt + sessions), Phoenix (RAG + auto-instrumentation), Opik (optimization + guardrails).
- Explain why 89% of organizations report having agent observability in place by 2026.
- Implement a stdlib trace-to-dashboard pipeline with LLM-judge evaluation.

## 问题引入

> **【中文解读】** Agent 可观测性平台提供对 Agent 执行的端到端可见性——从用户请求到最终响应的每一步。核心能力：追踪（每步执行记录）、指标（延迟/成本/成功率）、日志（详细执行过程）。主要平台包括 LangSmith、AgentOps、Braintrust 和 Phoenix。

## 核心概念

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

## 动手实现

`code/main.py` implements a stdlib trace collector + LLM-judge evaluator:
- Ingest GenAI-shaped spans.
- Group by session, tag failed runs (guardrail trips, low-confidence evals).
- A scripted LLM-judge that scores agent responses on a rubric.
- A dashboard-like summary: failure rate, top failure reasons, eval score distribution.
Run it:
```
python3 code/main.py
```
Output: per-session eval scores and failure categorization matching what Langfuse/Phoenix/Opik would show.

## 用框架实现

- **Langfuse** self-hosted or cloud; wire via OTel or their SDK.
- **Arize Phoenix** self-hosted; auto-instrument OpenInference.
- **Comet Opik** self-hosted or cloud; automated optimization loop.
- **Datadog LLM Observability** for mixed ops+ML teams that already run Datadog.

## 产出物

`outputs/skill-obs-platform-wiring.md` picks a platform and wires traces + evals + prompt versions into an existing agent.

## 练习题

1. Export a week of OTel traces to Langfuse cloud (free tier). Which sessions failed? Why?
   *思考并实践此练习*
2. Write an LLM-judge rubric for your domain (factual correctness, tone, scope adherence). Test on 50 traces.
   *思考并实践此练习*
3. Compare Langfuse prompt versioning against Phoenix's trace clustering. Which tells you what broke faster?
   *思考并实践此练习*
4. Read Opik's guardrail docs. Wire a PII redaction guardrail to one of your agent runs.
   *思考并实践此练习*
5. Benchmark the three on your corpus. Ignore vendor-published numbers; measure your own.
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Tracing | "Spans collector" |
| Prompt management | "Prompt CMS" |
| LLM-as-judge | "Automated eval" |
| Session replay | "Trace playback" |
| RAG relevancy | "Retrieval quality" |
| Trace clustering | "Behavioral grouping" |
| Guardrail enforcement | "Policy at log time" |

## 延伸阅读

