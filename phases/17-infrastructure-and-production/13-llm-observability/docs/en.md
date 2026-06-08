# LLM Observability Stack Selection | 可观测性 选择 LLM

> The 2026 observability market splits into two categories. Development platforms (LangSmith, Langfuse, Comet Opik) bundle monitoring with evals, prompt management, session replays. Gateway/instrumentation tools (Helicone, SigNoz, OpenLLMetry, Phoenix) focus on telemetry. Langfuse is MIT-licensed core with strong OSS balance (50K events/month free cloud). Phoenix is OpenTelemetry-native under Elastic License 2.0 — excellent for drift/RAG visualization, not a persistent production backend. Arize AX uses zero-copy Iceberg/Parquet integration claiming 100x cheaper than monolithic observability. LangSmith leads for LangChain/LangGraph, $39/user/mo, self-host in Enterprise only. Helicone is proxy-based with 15-30 min setup, 100K req/mo free, but less depth on agent traces. Common production pattern: Gateway (Helicone/Portkey) + eval platform (Phoenix/TruLens) glued by OpenTelemetry.

> **【中文解读】** 本节介绍了 LLM 可观测性——监控和调试 LLM 推理服务的工具和方法。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy trace-sampling simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Distinguish development platforms (bundled: evals + prompts + sessions) from gateway/telemetry tools (traces + metrics only).
  中文翻译：区分开发平台（捆绑：评估 + 提示管理 + 会话）与网关/遥测工具（仅追踪和指标）。
- Map six major tools (Langfuse, LangSmith, Phoenix, Arize AX, Helicone, Opik) to their licensing, pricing, and sweet-spot use cases.
  中文翻译：将六个主要工具（Langfuse、LangSmith、Phoenix、Arize AX、Helicone、Opik）映射到其许可、定价和最佳用例。
- Explain the OpenTelemetry-glue pattern that lets you combine a gateway tool with a separate eval platform.
  中文翻译：解释 OpenTelemetry 胶水模式，该模式允许你将网关工具与独立评估平台组合。
- Name the 2026 cost differentiator (Arize AX's zero-copy approach vs monolithic ingest) and state the rough 100x multiplier.
  中文翻译：说出 2026 年的成本差异化因素（Arize AX 的零拷贝方法 vs 单体式摄入）并说明大约 100 倍的乘数。

## The Problem | 问题引入

> **【中文解读】** LLM 可观测性工具分为两类：(1) 开发平台（LangSmith、Langfuse、Opik）——捆绑监控、评估、提示管理、会话回放；(2) 网关/遥测工具（Helicone、SigNoz、OpenLLMetry、Phoenix）——专注于遥测采集。选择涉及四个维度：技术栈（LangChain？原始 SDK？）、许可证（MIT only？商业可接受？）、预算、自托管需求。

> **【拓展：LLM 可观测性市场格局】** 2026 年 LLM 可观测性市场的关键玩家：(1) Langfuse（MIT 开源，50K events/month 免费云）——LangSmith 级功能但可自托管；(2) LangSmith（商业，$39/user/month）——LangChain 生态最佳；(3) Phoenix（Elastic License 2.0）——RAG/漂移可视化优秀；(4) Arize AX（商业）——zero-copy Iceberg/Parquet，号称比单体可观测性便宜 100x；(5) Helicone（MIT，100K req/month 免费）——proxy-based，15-30 分钟设置。生产常见模式是：网关（Helicone/Portkey）+ 评估平台（Phoenix/TruLens），通过 OpenTelemetry 胶水连接。

You shipped an LLM feature. It works. You have no visibility into prompt failures, tool loops, latency regressions, cost spikes, or prompt-cache hit rate. You Google "LLM observability" and get eight tools all claiming they solve the same problem at three different price points.

They don't solve the same problem. LangSmith answers "why did this LangGraph run fail?" Phoenix answers "is my RAG pipeline drifting?" Helicone answers "which app is burning tokens?" Langfuse answers "can I self-host the whole thing?" Different tools, different audiences.

Picking involves four axes: stack (LangChain? raw SDK? multi-vendor?), license tolerance (MIT only? Elastic OK? commercial fine?), budget (free tier? $100/mo? $1000/mo?), and self-host (must? nice-to-have? never?).

## The Concept | 核心概念

### Two categories

**Development platforms** bundle observability with evals, prompt management, dataset versioning, session replay. You run experiments, see which prompt worked, dataset-regression a new prompt against old winners. LangSmith, Langfuse, Comet Opik.

**Gateway/telemetry tools** instrument inference calls — prompt, response, tokens, latency, model, cost. Helicone, SigNoz, OpenLLMetry, Phoenix. Minimalist. Can be combined with a separate eval tool via OpenTelemetry.

### Langfuse — OSS balance

> **【拓展：LLM 可观测性工具选型决策】** 2026 年 LLM 可观测性工具选型的关键维度：(1) 技术栈——LangChain/LangGraph 生态优先选 LangSmith；自研 SDK 选 Langfuse 或 Phoenix；(2) 许可证——要求 MIT 选 Langfuse/Opik；Elastic License 2.0 可接受选 Phoenix；商业可接受选 LangSmith；(3) 自托管——必须自托管选 Langfuse 或 Opik（Docker 部署）；(4) 预算——免费层 Langfuse 50K events/month、Helicone 100K req/month；(5) 规模——>10M traces/day 选 Arize AX 的 zero-copy 架构。

- Core Apache / MIT licensed; self-host via Docker.
- Cloud free tier: 50K events/month. Paid: $29/mo for team.
- Evals, prompt management, traces, datasets. Reasonable coverage of all four dev-platform features.
- Sweet spot: you want LangSmith-class features but must self-host or stay on OSS license.

### Phoenix (Arize) — telemetry-first, OpenTelemetry-native

- Elastic License 2.0; self-host trivial.
- Excellent at RAG and drift visualization. Embedding-space scatter plots shipped as first-class.
- Not designed as persistent production backend — primarily development-time observability.
- Sweet spot: RAG pipeline development, drift debugging, pairs with a separate gateway for production.

### Arize AX — the scale play

- Commercial. Zero-copy data lake integration via Iceberg/Parquet.
- Claims ~100x cheaper than monolithic observability (Datadog-class) at scale. The math: you store traces in your own Parquet on S3; Arize reads directly.
- Sweet spot: >10M traces/day, existing data lake, want LLM-specific dashboards without Datadog pricing.

### LangSmith — LangChain/LangGraph first

- Commercial, $39/user/month. Self-host only on Enterprise.
- Best-in-class for LangChain and LangGraph stacks. If you are not on either, it is less compelling.
- Sweet spot: team committed to LangChain, willing to pay.

### Helicone — proxy-based minimum viable

- 15-30 minute setup by swapping your `OPENAI_API_BASE` to Helicone proxy.
- MIT licensed; 100K req/mo free, paid $20/mo+.
- Includes failover, caching, rate limits — acts as a gateway too.
- Less depth on agent / multi-step traces.
- Sweet spot: quick start, single-stack app, need gateway + observability in one.

### Opik (Comet) — OSS dev platform

- Apache 2.0, fully OSS.
- Similar feature set to Langfuse with Comet heritage.
- Sweet spot: ML teams already on Comet, want LLM observability in the same pane.

### SigNoz — OpenTelemetry-first full APM

- Apache 2.0. Handles general APM plus LLM via OpenTelemetry.
- Sweet spot: unified observability across services and LLM calls.

### The glue: OpenTelemetry + GenAI semantic conventions

> **【中文解读】** OpenTelemetry 在 2025 年末发布了 GenAI 语义约定（`gen_ai.system`、`gen_ai.request.model`、`gen_ai.usage.input_tokens`），让不同工具可以互操作。2026 年的生产模式是：(1) 从每个 LLM 调用发出带 GenAI 约定的 OTel；(2) 路由到网关（Helicone/Portkey）做日常监控；(3) 双写到评估平台（Phoenix/Langfuse）做回归检测；(4) 存档到数据湖（Iceberg）通过 Arize AX 或 DuckDB 做长期分析。

> **【拓展：LLM 可观测性的成本控制】** 在 >1M 请求/天的规模下，全量 trace 保留的成本超过 LLM 调用本身。采样策略：100% 错误、100% 高成本请求、5% 成功请求。始终保留聚合数据，只对长尾保留原始 trace。Langfuse 50K events/month 免费层适合小团队；大规模部署建议使用 OpenTelemetry Collector + 自有数据湖架构，成本可降低 80%+。

OpenTelemetry published GenAI semantic conventions in late 2025 (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`). Tools that consume OTel can interoperate. The production pattern emerging:

1. Emit OTel with GenAI conventions from every LLM call.
2. Route to gateway (Helicone / Portkey) for day-to-day.
3. Dual-ship to eval platform (Phoenix / Langfuse) for regressions.
4. Archive in data lake (Iceberg) for long-term analysis via Arize AX or DuckDB.

### The trap: instrumenting at the wrong layer

> **【中文解读】** 埋点层级的选择：在 Agent 框架内埋点（如添加 LangSmith traces）会耦合到该框架；在 HTTP/OpenAI-SDK 层埋点（通过 OpenLLMetry 或网关）则可移植。2026 年的最佳实践是在协议层埋点——无论底层使用什么框架，都通过 OpenTelemetry + GenAI 语义约定统一采集。

Instrumenting inside your agent framework (e.g., adding LangSmith traces) couples you to that framework. Instrumenting at the HTTP/OpenAI-SDK layer (via OpenLLMetry or your gateway) is portable.

### Sampling — you can't keep everything

At >1M requests/day, full-trace retention costs more than the LLM calls. Sample by rules: 100% errors, 100% high-cost, 5% success. Keep aggregates always; keep raw for the long tail.

### Numbers you should remember

- Langfuse free cloud: 50K events/month.
- LangSmith: $39/user/month.
- Helicone free: 100K req/month.
- Arize AX claim: ~100x cheaper than monolithic at scale.
- OpenTelemetry GenAI conventions: 2025 shipping, 2026 widely adopted.

## Use It | 用框架实现

`code/main.py` simulates a 1M-trace day across retention strategies (100% ingest, sampling, sampling + errors). Reports storage cost and what's lost under each.

> `code/main.py` simulates a 1M-trace day across retention strategies (100% ingest, sampling, sampling + errors). Reports storage cost and what's lost under each.

> `code/main.py` simulates a 1M-trace day across retention strategies (100% ingest, sampling, sampling + errors). Reports storage cost and what's lost under each.

## Ship It | 产出物

This lesson produces `outputs/skill-observability-stack.md`. Given stack, scale, budget, license posture, picks the tool(s).

> 本课产出 `outputs/skill-observability-stack.md`. Given stack, scale, budget, license posture, picks the tool(s).

## Exercises | 练习题

1. Your team on LangChain wants OSS self-hosted observability. Pick Langfuse or Opik and justify.
   中文翻译：你的团队使用 LangChain，想要开源自托管可观测性。选择 Langfuse 或 Opik 并说明理由。
2. At 5M traces/day with Datadog quotes $150K/month, compute break-even for Arize AX.
   中文翻译：在 5M traces/day 规模下，Datadog 报价 $150K/月，计算 Arize AX 零拷贝方案的盈亏平衡点。
3. Design an OpenTelemetry GenAI attribute set your org's guideline should mandate on every LLM call.
   中文翻译：设计一个你的组织指南应强制要求每次 LLM 调用包含的 OpenTelemetry GenAI 属性集。
4. Argue whether Phoenix alone is sufficient for production. When does it not suffice?
   中文翻译：论证 Phoenix 单独使用是否足以满足生产需求。它在什么情况下不够用？
5. Helicone is 20ms proxy overhead. At P99 TTFT 300 ms, is that acceptable? What if SLA is 100 ms?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| OpenLLMetry | "OTel for LLMs" | Open-source OpenTelemetry instrumentation for LLMs |
| GenAI conventions | "OTel attributes" | Standard OTel attribute names for LLM calls |
| LangSmith | "LangChain observability" | Commercial platform bundled with LangChain ecosystem |
| Langfuse | "OSS LangSmith" | MIT OSS with similar feature set |
| Phoenix | "Arize dev tool" | OpenTelemetry-native dev/eval platform |
| Arize AX | "scale observability" | Commercial zero-copy Iceberg/Parquet observability |
| Helicone | "proxy observability" | HTTP proxy collecting LLM telemetry + gateway features |
| Opik | "Comet LLM" | Apache 2.0 OSS dev platform from Comet |
| Session replay | "trace rerun" | Replay a full agent session with tool calls |
| Eval | "offline test" | Running candidate model/prompt over labeled dataset |

## Further Reading | 延伸阅读

- [SigNoz — Top LLM Observability Tools 2026](https://signoz.io/comparisons/llm-observability-tools/)
- [Langfuse — Arize AX Alternative analysis](https://langfuse.com/faq/all/best-phoenix-arize-alternatives)
- [PremAI — Setting Up Langfuse, LangSmith, Helicone, Phoenix](https://blog.premai.io/llm-observability-setting-up-langfuse-langsmith-helicone-phoenix/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [Helicone docs](https://docs.helicone.ai/)
