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

> OTel GenAI（第 23 课）给了你 schema。你仍然需要一个平台来接收 span、运行评估、存储提示版本并显示回归。三个竞争者各自强调生命周期的不同部分。

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·23（OTel GenAI Conventions）——本节是把上一节的 schema 落到具体平台上，不知道 `invoke_agent` span 长什么样你看不懂任何平台的界面；可选 Phase 14·05（Self-Refine/CRITIC）——理解 LLM-as-judge 的本质就是 CRITIC 模式，否则你会把 judge 当成"另一个 LLM 调用"而非"基于外部证据的事实核查"。


> **【中文解读】** Agent 可观测性平台提供对 Agent 执行的端到端可见性——从用户请求到最终响应的每一步。核心能力：追踪（每步执行记录）、指标（延迟/成本/成功率）、日志（详细执行过程）。主要平台包括 LangSmith、AgentOps、Braintrust 和 Phoenix。

## The Concept | 核心概念

### Langfuse (MIT)

> 💡 **【类比】** 三个观测平台像三种医院信息系统的分工：**Langfuse** 是综合医院 HIS（住院、门诊、药房全打通——tracing+prompt 管理+eval 一站式，强调"你改了提示版本 v3 后，第三天崩了的 trace 都能 bisect 到这个版本"）；**Phoenix** 是专科检验中心（专攻 RAG 检索质量、行为漂移聚类，trace clustering 能告诉你"这周 Agent 行为和上周不像了"但不管你改了哪个提示）；**Opik** 是临床试验管理系统（专做 A/B 自动优化、guardrail 强制执行，自动跑 100 次实验找最优提示）。同一份 OTel span 可以同时发给三者——不是二选一。

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

> 🤔 **【困惑】** Q: 89% 组织都说自己有 Agent 可观测性了，但为什么事故还在涨？ A: 多数团队只做了"接入 OTel → trace 进了 Langfuse"这一步，等于装了监控摄像头但没人看。真正的可观测性需要：eval 策略（哪些 trace 该被打分）、prompt 版本和 trace 强绑定（回归能 bisect）、LLM-judge 有 ground truth 校准。行业 32% 把"质量问题"列为生产首要障碍，说明装平台容易，建评估闭环难。

- **No eval strategy.** Tracing without evaluation is just expensive logging.
- **Self-rolled LLM-judge without grounding.** CRITIC pattern (Lesson 05) applies — judges need external tools for factual verification.
- **Prompt versions not tied to traces.** When prod regresses, you cannot bisect to the prompt that caused it.

> **没有评估策略。** 没有评估的追踪只是昂贵的日志。
> **自建的 LLM 评审器没有基础。** CRITIC 模式（第 5 课）适用——评审器需要外部工具进行事实核查。
> **提示版本未与追踪关联。** 当生产回归时，你无法定位到导致问题的提示。

## Build It | 动手实现

> ⚠️ **【易错点】** 场景：团队把 OTel trace 接到 Langfuse 后，写了个 LLM-judge 给每条 trace 打 1-5 分，但 rubric 只有一句"回答得好不好" → 后果：分数毫无意义，judge 把"礼貌但答错"打 5 分、"正确但简短"打 2 分，dashboard 上 95% 满意度但客户投诉暴涨 → 修复：rubric 必须分维度（factual correctness、scope adherence、tone），每维度有可操作的失败定义（如 "scope adherence: agent 是否做了用户没要求的额外操作"），且必须配 50-100 条人工标注做 baseline 校准 judge——这就是为什么 Phoenix 强调 "grounding"，Opik 强调"benchmark on your own corpus"。

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

> 输出：每会话的评估分数和失败分类，匹配 Langfuse/Phoenix/Opik 会显示的内容。

> Agent 可观测性平台提供运行时追踪、指标监控和调试工具。Langfuse、Arize Phoenix、Braintrust 是 2026 年主要的 Agent 可观测性工具。

## Use It | 用框架实现

- **Langfuse** self-hosted or cloud; wire via OTel or their SDK.
- **Arize Phoenix** self-hosted; auto-instrument OpenInference.
- **Comet Opik** self-hosted or cloud; automated optimization loop.
- **Datadog LLM Observability** for mixed ops+ML teams that already run Datadog.

## Ship It | 产出物

`outputs/skill-obs-platform-wiring.md` picks a platform and wires traces + evals + prompt versions into an existing agent.

> `outputs/skill-obs-platform-wiring.md` 选择一个平台，并将追踪 + 评估 + 提示版本接入现有 Agent。

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
