# LLM Routing Layer — LiteLLM, OpenRouter, Portkey | LLM 路由层：LiteLLM、OpenRouter 与 Portkey

> Provider lock-in is expensive. Different tool-calling workloads suit different models. Routing gateways give one API surface, retries, failover, cost tracking, and guardrails. Three archetypes dominate 2026: LiteLLM (open-source self-hosted), OpenRouter (managed SaaS), Portkey (production-grade, open-sourced in March 2026). This lesson names the decision criteria and walks a stdlib routing gateway.

> **【中文解读】** 供应商锁定成本高昂。不同的工具调用工作负载适合不同的模型。路由网关提供统一的 API 接口、重试、故障转移、成本追踪和护栏。2026 年三大方案：LiteLLM（开源自托管）、OpenRouter（托管 SaaS）、Portkey（生产级，2026年3月开源）。本课命名决策标准并演示标准库路由网关。

> **【拓展】** LLM 路由层解决的核心问题：按任务复杂度自动路由到最优模型（成本优化）、供应商故障自动切换（高可用）、延迟敏感路由（用户体验）、合规区域路由（数据主权）、A/B 测试路由（实验）。这是 AI 工程从单模型走向多模型架构的关键基础设施。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, routing + failover + cost tracker) | **语言:** Python (stdlib, routing + failover + cost tracker)
**Prerequisites:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Distinguish self-hosted, managed, and production-grade routing options.
  中文翻译：区分自托管、托管和生产级路由选项。
- Implement a fallback chain that retries on provider failures in a defined priority order.
  中文翻译：实现按定义优先级顺序在供应商失败时重试的回退链。
- Track per-request cost and token usage across providers.
  中文翻译：跨供应商追踪每请求成本和 token 使用量。
- Decide between LiteLLM, OpenRouter, and Portkey for a given production constraint.

> **【中文解读】** 学习目标：区分自托管、托管和生产级路由选项；实现供应商故障时的回退链；跨供应商追踪每请求成本和 token 使用量；根据生产约束选择 LiteLLM/OpenRouter/Portkey。

## The Problem | 问题引入

> **【中文解读】** 路由重要的场景：(1) 成本——Claude Sonnet 费用是 Haiku 的3倍，分流任务用 Haiku 足够；(2) 故障转移——OpenAI 宕机时自动切换到 Anthropic；(3) 延迟——实时聊天需要快速首 token；(4) 合规——EU 用户留在 EU 区域；(5) 实验——A/B 两个模型。路由网关提供统一的 OpenAI 兼容 API 处理一切。

Scenarios where provider routing matters:

> 供应商路由重要的场景：

1. **Cost.** Claude Sonnet costs 3x what Haiku costs. For a triage task, Haiku is enough; for a synthesis task, Sonnet is worth it. Route per-request.
  中文翻译：**成本。** Claude Sonnet 成本是 Haiku 的 3 倍。对分流任务，Haiku 够用；对综合任务，Sonnet 值得。每请求路由。

2. **Failover.** OpenAI has a bad hour. Every request fails. You want automatic fallback to Anthropic without redeploying.
  中文翻译：**故障转移。** OpenAI 有糟糕的一小时。每请求失败。你想要自动回退到 Anthropic 而无需重新部署。

3. **Latency.** A live chat UI needs fast time-to-first-token. A batch summarizer does not. Route by latency SLA.
  中文翻译：**延迟。** 实时聊天 UI 需要快速首 token。批量摘要器不需要。按延迟 SLA 路由。

4. **Compliance.** EU users must stay in EU regions. Route by region.
  中文翻译：**合规。** EU 用户必须留在 EU 区域。按区域路由。

5. **Experimentation.** A/B two models on the same workload. Route by test bucket.
  中文翻译：**实验。** 在相同工作负载上 A/B 两个模型。按测试桶路由。

Hand-coding all of this per integration is repetitive. A routing gateway gives one OpenAI-compatible API and handles the rest.

> 每个集成手写所有这些很重复。路由网关提供统一 OpenAI 兼容 API 并处理其余。

## The Concept | 核心概念

### OpenAI-compatible proxy shape

Everyone speaks OpenAI-shape. The routing gateway exposes `/v1/chat/completions`, accepts the OpenAI schema, and internally proxies to Anthropic / Gemini / Cohere / Ollama / anything. The client does not care.

> 每个都说 OpenAI 形态。路由网关暴露 `/v1/chat/completions`、接受 OpenAI schema、内部代理到 Anthropic/Gemini/Cohere/Ollama/任何。客户端不关心。

### Model aliases

Instead of `claude-3-5-sonnet-20251022`, your code says `our_smart_model`. The gateway maps aliases to real models. When Anthropic ships Claude 4, you change the alias server-side; your code does not touch a thing.

> 你的代码不说 `claude-3-5-sonnet-20251022`，而是 `our_smart_model`。网关将别名映射到真实模型。当 Anthropic 发布 Claude 4 时，你在服务器端改别名；代码不动。

### Fallback chains

```
primary: openai/gpt-4o
on 5xx: anthropic/claude-3-5-sonnet
on 5xx: google/gemini-1.5-pro
on 5xx: refuse
```

Gateways define this in a config. Retries count against a budget so fallback cascades do not explode cost.

> 网关在配置中定义。重试计入预算，使回退级联不爆炸成本。

### Semantic caching

Identical-or-near-identical prompts hit a cache instead of the provider. Savings on repeated agent loops can be 30 to 60 percent. Keys are embedding-based; near-identical prompts share a cache slot.

> 相同或近相同 prompt 命中缓存而非供应商。重复 Agent 循环节省可达 30-60%。键基于嵌入；近相同 prompt 共享缓存槽。

### Guardrails

Gateway-level:

> 网关级：

- **PII redaction.** Regex or ML-based pass before sending prompts.
  中文翻译：**PII 脱敏。** 发送 prompt 前基于正则或 ML 的脱敏。
- **Policy violations.** Reject prompts with prohibited content.
  中文翻译：**策略违规。** 拒绝包含禁止内容的 prompt。
- **Output filters.** Scrub completions for leaks.
  中文翻译：**输出过滤器。** 清理补全中的泄漏。

Portkey and Kong both ship opinionated guardrails. LiteLLM leaves them optional.

> Portkey 和 Kong 都发布带主张的护栏。LiteLLM 留作可选。

### Per-key rate limits

One API key = one team. Per-key budgets prevent one team from consuming the shared quota. Most gateways support this.

> 一个 API key = 一个团队。每密钥预算防止单一团队消耗共享配额。大多数网关支持此。

### Self-hosted vs managed trade-offs

| Factor | LiteLLM (self-hosted) | OpenRouter (managed) | Portkey (production) |
|--------|----------------------|----------------------|----------------------|
| Code | Open source, Python | Managed SaaS | Open source (Mar 2026) + managed |
| Setup | Deploy a proxy | Sign up | Either |
| Providers | 100+ | 300+ | 100+ |
| Billing | Your own keys | OpenRouter credits | Your own keys |
| Observability | OpenTelemetry | Dashboard | Full OTel + PII redaction |
| Best for | Teams that want full control | Rapid prototyping | Production with compliance |

LiteLLM wins when you have an SRE team and want data主权。OpenRouter wins when you want a single subscription and no infra. Portkey wins when you need guardrails and compliance out of the box.

> LiteLLM 在你有 SRE 团队并想要数据主权时胜出。OpenRouter 在你想要单一订阅无基础设施时胜出。Portkey 在你需要开箱即用护栏和合规时胜出。

### Cost tracking

Every request carries `provider`, `model`, `input_tokens`, `output_tokens`. Multiply by per-model per-token prices (pulled from a pricing sheet the gateway maintains). Per-user / per-team / per-project aggregation.

> 每请求携带 `provider`、`model`、`input_tokens`、`output_tokens`。乘以每模型每 token 价格（从网关维护的价格表拉取）。按用户/团队/项目聚合。

### MCP plus routing

A gateway can route both LLM calls AND MCP sampling requests. When a sampling request's modelPreferences prefer a specific model, the gateway translates to the right backend. This is where Phase 13 · 17 (MCP gateway) and this lesson's routing gateway sometimes merge into one service.

> 网关可同时路由 LLM 调用和 MCP sampling 请求。当 sampling 请求的 modelPreferences 偏好特定模型时，网关翻译到正确后端。这是 Phase 13 · 17（MCP 网关）和本课的路由网关有时合并为单一服务的地方。

### Routing strategies

- **Static priority.** First in list; fall back on error.
  中文翻译：**静态优先级。** 列表中第一个；出错时回退。
- **Load balancing.** Round-robin or weighted.
  中文翻译：**负载均衡。** 轮询或加权。
- **Cost-aware.** Pick the cheapest model meeting latency / quality.
  中文翻译：**成本感知。** 选择满足延迟/质量的最便宜模型。
- **Latency-aware.** Pick the fastest model in the last N minutes.
  中文翻译：**延迟感知。** 选最近 N 分钟最快的模型。
- **Task-aware.** Prompt classifier routes coding to one model, summarization to another.
  中文翻译：**任务感知。** Prompt 分类器将编码路由到一个模型、摘要到另一个。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 实现约150行的路由网关：接受 OpenAI 格式请求，翻译到每供应商存根，运行优先级回退链，追踪每请求成本，应用 PII 脱敏。三个场景：正常请求、主供应商宕机触发故障转移、PII 泄露被脱敏拦截。

`code/main.py` implements a routing gateway in ~150 lines: accepts OpenAI-shaped requests, translates to per-provider stubs, runs a priority fallback chain, tracks per-request cost, and applies a PII redaction pass on inputs. Run it with three scenarios: normal request, primary-provider outage triggering fallback, PII leakage caught by redaction.

> `code/main.py` 实现约 150 行的路由网关：接受 OpenAI 形态请求、翻译到每供应商存根、运行优先级回退链、追踪每请求成本、对输入应用 PII 脱敏。用三个场景运行：正常请求、主供应商宕机触发故障转移、PII 泄露被脱敏捕获。

What to look at:

- `ROUTES` dict: alias -> priority-ordered list of concrete providers.
  中文翻译：`ROUTES` 字典：别名 -> 优先级排序的具体供应商列表。
- Fallback loop retries on 5xx.
  中文翻译：回退循环在 5xx 上重试。
- Cost tracker multiplies token usage by per-model rates.
  中文翻译：成本追踪器将 token 用量乘以每模型费率。
- PII redactor scrubs SSN-shaped patterns before forwarding.
  中文翻译：PII 脱敏器在转发前清理 SSN 形状模式。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-routing-config-designer.md`——给定工作负载配置（延迟、成本、合规），选择 LiteLLM/OpenRouter/Portkey 并生成路由配置。

This lesson produces `outputs/skill-routing-config-designer.md`. Given a workload profile (latency, cost, compliance), the skill picks LiteLLM / OpenRouter / Portkey and produces a routing config.

> 本课产出 `outputs/skill-routing-config-designer.md`。给定工作负载配置（延迟、成本、合规），该 skill 选择 LiteLLM/OpenRouter/Portkey 并生成路由配置。

## Exercises | 练习题

1. Run `code/main.py`. Trigger the outage scenario; confirm fallback lands on the second provider and cost is attributed correctly.
   中文翻译：运行 `code/main.py`。触发宕机场景；确认回退落在第二个供应商上、成本正确归属。

2. Add semantic caching: SHA256 of the prompt is a lookup key; cache hits return instantly. Measure cost savings on a repeated call.
   中文翻译：添加语义缓存：prompt 的 SHA256 是查找键；缓存命中立即返回。测量重复调用的成本节省。

3. Add a prompt classifier that routes "code ..." prompts to an alias favoring intelligence and "summarize ..." prompts to an alias favoring speed.
   中文翻译：添加 prompt 分类器，将 "code ..." prompt 路由到偏好智能的别名、"summarize ..." 路由到偏好速度的别名。

4. Design per-team budgets: each team has a monthly spend cap; gateway refuses requests once cap is hit. Pick an enforcement granularity (per-request or windowed).
   中文翻译：设计每团队预算：每团队有月度支出上限；网关在达到上限时拒绝请求。选择执行粒度（每请求或窗口）。

5. Read LiteLLM, OpenRouter, and Portkey docs side by side. Name the one feature each ships that the other two do not.
   中文翻译：并排阅读 LiteLLM、OpenRouter 和 Portkey 文档。命名每个发布的但其他两个没有的一个功能。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| Routing gateway | "LLM proxy" | One-API-surface layer in front of many providers | 路由网关：多供应商统一 API |
| OpenAI-compatible | "Speaks the OpenAI schema" | Accepts `/v1/chat/completions` shape, translates to any backend | OpenAI 兼容接口 |
| Model alias | "our_smart_model" | Name in your code that the gateway maps to a concrete model | 模型别名：代码中的抽象名 |
| Fallback chain | "Retry list" | Ordered list of providers attempted on failure | 回退链：失败时的有序重试列表 |
| Semantic caching | "Prompt-embedding cache" | Key is embedding of the prompt; near-duplicates share a cache hit | 语义缓存：嵌入向量近似匹配 |
| Guardrails | "Input/output filters" | Redact PII, reject policy violations | 护栏：输入输出过滤器 |
| Per-key rate limit | "Team budget" | Quota scoped to an API key | 按密钥限流：团队预算 |
| Cost tracking | "Per-request spend" | Aggregate token usage x price per model | 成本追踪：每请求费用 |
| LiteLLM | "The open proxy" | Self-hostable OSS routing gateway | LiteLLM：开源自托管路由网关 |
| OpenRouter | "The managed SaaS" | Hosted gateway with credit-based billing | OpenRouter：托管 SaaS 路由 |
| Portkey | "The production option" | Open-source + managed with guardrails built in | Portkey：生产级路由+护栏 |

## Further Reading | 延伸阅读

- [LiteLLM — docs](https://docs.litellm.ai/) — self-hosted routing gateway
  中文翻译：自托管路由网关
- [OpenRouter — quickstart](https://openrouter.ai/docs/quickstart) — managed routing SaaS
  中文翻译：托管路由 SaaS
- [Portkey — docs](https://portkey.ai/docs) — production routing with guardrails
  中文翻译：带护栏的生产路由
- [TrueFoundry — LiteLLM vs OpenRouter](https://www.truefoundry.com/blog/litellm-vs-openrouter) — decision guide
  中文翻译：决策指南
- [Relayplane — LLM gateway comparison 2026](https://relayplane.com/blog/llm-gateway-comparison-2026) — vendor survey
  中文翻译：供应商调研
