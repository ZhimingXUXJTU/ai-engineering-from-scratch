# AI Gateways — LiteLLM, Portkey, Kong AI Gateway, Bifrost | 网关 LLM

> A gateway sits between your apps and model providers. Core features are provider routing, fallback, retries, rate limiting, secret references, observability, guardrails. Market split in 2026: **LiteLLM** is MIT OSS with 100+ providers, OpenAI-compatible, but breaks down around ~2000 RPS (8 GB memory, cascading failures in published benchmarks); best for Python, <500 RPS, dev/prototyping. **Portkey** is control-plane-positioned (guardrails, PII redaction, jailbreak detection, audit trails), went Apache 2.0 open-source March 2026, 20-40 ms latency overhead, $49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $100/model/month pricing (max 5 on Plus tier); enterprise-fit if you're already on Kong. **Bifrost** (Maxim AI) — automatic retries with configurable backoff, fallback to Anthropic on OpenAI 429. **Cloudflare / Vercel AI Gateways** — managed, zero-ops, basic retry. Data residency drives the self-host decision; Portkey and Kong sit in the middle with OSS + optional managed.

> **【中文解读】** 本节介绍了 AI 网关——LLM 请求的路由、负载均衡和安全网关。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Enumerate the six core gateway features (routing, fallback, retries, rate limits, secrets, observability, guardrails).
  中文翻译：Enumerate the six core gateway features (routing, fallback, retries, rate limits, secrets, observability, guardrails).
- Map four 2026 gateways (LiteLLM, Portkey, Kong AI, Bifrost) to scale ceilings and use cases.
  中文翻译：Map four 2026 gateways (LiteLLM, Portkey, Kong AI, Bifrost) to scale ceilings and use cases.
- Cite the Kong benchmark (228% vs Portkey, 859% vs LiteLLM) and explain why it matters for >500 RPS.
  中文翻译：Cite the Kong benchmark (228% vs Portkey, 859% vs LiteLLM) and explain why it matters for >500 RPS.
- Choose self-hosted vs managed given data residency and ops budget.
  中文翻译：Choose self-hosted vs managed given data residency and ops budget.

## The Problem | 问题引入

> **【中文解读】** AI 网关位于应用和模型提供商之间，解决的核心问题是多供应商统一管理。产品同时调用 OpenAI、Anthropic 和自托管 Llama，每个提供商有不同的 SDK、错误模型、速率限制和认证方案。网关层将所有这些统一为一个 OpenAI 兼容的 API，提供故障转移、统一凭证存储、统一可观测性和按租户速率限制。

> **【拓展：2026 年 AI 网关市场】** 2026 年 AI 网关市场的四个主要玩家：(1) LiteLLM——MIT 开源，100+ 提供商，但在 ~2000 RPS 时崩溃（8GB 内存）；(2) Portkey——2026 年 3 月开源 Apache 2.0，控制面定位（guardrails、PII 脱敏、越狱检测、审计追踪），20-40ms 延迟开销；(3) Kong AI Gateway——基于成熟 API 网关产品，Kong 自己的基准测试显示比 Portkey 快 228%、比 LiteLLM 快 859%；(4) Cloudflare/Vercel AI Gateway——托管、零运维、边缘部署。

Your product calls OpenAI, Anthropic, and a self-hosted Llama. Each provider has a different SDK, error model, rate limit, and auth scheme. You want failover (if OpenAI 429s, try Anthropic), a single credential store, unified observability, and rate limits per tenant.

Reinventing this at the app layer couples every service to every provider. A gateway layer consolidates it into one process with one API (typically OpenAI-compatible) that fans out to providers.

## The Concept | 核心概念

### Six core features

1. **Provider routing** — OpenAI, Anthropic, Gemini, self-hosted, etc. behind one API.
2. **Fallback** — on 429, 5xx, or quality failure, retry elsewhere.
3. **Retries** — exponential backoff, bounded attempts.
4. **Rate limits** — per-tenant, per-key, per-model.
5. **Secret references** — pull credentials from vault at runtime (never in app).
6. **Observability** — OTel + GenAI attributes (Phase 17 · 13) + cost attribution.
7. **Guardrails** — PII redaction, jailbreak detection, allowed-topics filters.

### LiteLLM — MIT OSS, Python

- 100+ providers, OpenAI-compatible, router config, fallback, basic observability.
- Breaks down around 2000 RPS in Kong's benchmark; 8 GB memory footprint, cascading failures under sustained load.
- Best fit: Python app, <500 RPS, dev/staging gateways, experimental routing.
- Cost: $0 for OSS; cloud free tier exists.

### Portkey — control plane positioning

- Apache 2.0 OSS as of March 2026. Guardrails, PII redaction, jailbreak detection, audit trails.
- 20-40 ms per-request latency overhead.
- $49/mo for production tier with retention + SLA.
- Best fit: regulated industries needing guardrails + observability bundled.

### Kong AI Gateway — the scale play

- Built on Kong Gateway (mature API gateway product, lua+OpenResty).
- Kong's own benchmark on 12-CPU equivalent: 228% faster than Portkey, 859% faster than LiteLLM.
- Pricing: $100/model/month, max 5 on Plus tier.
- Best fit: already on Kong; >1000 RPS; willing to license.

### Bifrost (Maxim AI)

- Automatic retries with configurable backoff.
- Fallback to Anthropic on OpenAI 429 is a canonical recipe.
- Newer entrant; commercial.

### Cloudflare AI Gateway / Vercel AI Gateway

- Managed, zero-ops. Basic retry and observability.
- Best fit: Edge-serving JavaScript apps on Cloudflare/Vercel.
- Limited compared to Kong/Portkey on guardrails and rate limits.

### Self-hosted vs managed

> **【中文解读】** 自托管 vs 托管的决策驱动因素是数据驻留。医疗和金融默认自托管（LiteLLM 或 Portkey OSS 或 Kong）；消费产品默认托管（Cloudflare AI Gateway）或中间层（Portkey managed）。混合模式：受监管租户自托管，其他托管。网关延迟直接影响 TTFT——对于 TTFT P99 < 100ms 的 SLA，只能选 Kong（3-8ms 开销）或 Cloudflare（1-3ms）；对于 P99 < 500ms，任何网关都可以。

> **【拓展：网关 + 可观测性 + 路由的组合】** Phase 17·13（可观测性）+ 16（模型路由）+ 19（网关）在生产中是同一层。选择一个覆盖所有三者的工具，或仔细连接它们：大多数 2026 年部署将 Helicone（可观测性）或 Portkey（guardrails）与 Kong（规模）组合为分拆角色。Portkey 的 Apache 2.0 开源使得"自托管 guardrails + Kong 规模"的组合成为受监管行业的标准模式。

Data residency is the forcing function. Healthcare and finance default self-host (LiteLLM or Portkey OSS or Kong). Consumer products default managed (Cloudflare AI Gateway) or middle-tier (Portkey managed). Hybrid: self-hosted for regulated tenant, managed for others.

### Latency budget

> **【拓展：AI 网关延迟预算分析】** AI 网关延迟直接影响 TTFT，是选型的关键因素。2026 年各网关的延迟开销：(1) LiteLLM 5-15ms——Python 实现，简单但高并发下不稳定；(2) Portkey 20-40ms——功能最全面但延迟最高；(3) Kong 3-8ms——Go + OpenResty，延迟最低且高并发稳定；(4) Cloudflare/Vercel 1-3ms——边缘部署优势。对于 TTFT P99 < 100ms 的 SLA，只有 Kong 或 Cloudflare 可选；对于 P99 < 500ms，任何网关都在预算内。

- LiteLLM: 5-15 ms overhead typical.
- Portkey: 20-40 ms overhead.
- Kong: 3-8 ms overhead.
- Cloudflare/Vercel: 1-3 ms overhead (edge advantage).

Gateway latency directly adds to TTFT. For TTFT P99 < 100 ms SLA, Kong or Cloudflare. For P99 < 500 ms, any.

### Rate-limit semantics matter

Simple token-bucket works up to moderate scale. Multi-tenant requires sliding-window + burst allowance + per-tenant tiering. LiteLLM ships token-bucket; Kong ships sliding-window; Portkey ships tiered.

### Gateway + observability + routing compose

Phase 17 · 13 (observability) + 16 (model routing) + 19 (gateways) are the same layer in production. Pick one tool that covers all three or wire them carefully: most 2026 deployments combine Helicone (observability) or Portkey (guardrails) with Kong (scale) for split roles.

### Numbers you should remember

- LiteLLM: breaks at ~2000 RPS, 8 GB memory.
- Portkey: 20-40 ms overhead; Apache 2.0 since March 2026.
- Kong: 228% faster than Portkey, 859% faster than LiteLLM.
- Kong pricing: $100/model/month, 5 max on Plus tier.
- Cloudflare/Vercel: 1-3 ms overhead at the edge.

## Use It | 用框架实现

`code/main.py` simulates gateway routing with fallback across 3 providers under 429/5xx injection. Reports latency, retry rate, and fallback hit rate.

> `code/main.py` simulates gateway routing with fallback across 3 providers under 429/5xx injection. Reports latency, retry rate, and fallback hit rate.

> `code/main.py` simulates gateway routing with fallback across 3 providers under 429/5xx injection. Reports latency, retry rate, and fallback hit rate.

## Ship It | 产出物

This lesson produces `outputs/skill-gateway-picker.md`. Given scale, ops posture, compliance, latency budget, picks a gateway.

> 本课产出 `outputs/skill-gateway-picker.md`. Given scale, ops posture, compliance, latency budget, picks a gateway.

## Exercises | 练习题

1. Run `code/main.py`. Configure fallback from OpenAI→Anthropic→self-hosted. What's the expected hit rate at 5% provider error rate?
   中文翻译：Run `code/main.py`. Configure fallback from OpenAI→Anthropic→self-hosted. What's the expected hit rate at 5% provider error rate?
2. Your SLA is TTFT P99 < 200 ms on a 300 ms baseline. Which gateways stay within budget?
   中文翻译：Your SLA is TTFT P99 < 200 ms on a 300 ms baseline. Which gateways stay within budget?
3. A healthcare customer requires self-hosted + PII redaction + audit. Pick Portkey OSS or Kong.
   中文翻译：A healthcare customer requires self-hosted + PII redaction + audit. Pick Portkey OSS or Kong.
4. Compare LiteLLM vs Kong: at what RPS ceiling should a team migrate?
   中文翻译：Compare LiteLLM vs Kong: at what RPS ceiling should a team migrate?
5. Design a rate-limit policy for a multi-tenant SaaS: free tier, trial tier, paid tier. Token-bucket or sliding-window?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Gateway | "API broker" | Process sitting between apps and providers |
| LiteLLM | "the MIT one" | Python OSS, 100+ providers, breaks at 2K RPS |
| Portkey | "guardrails gateway" | Control plane + observability, Apache 2.0 |
| Kong AI Gateway | "the scale one" | Built on Kong Gateway, benchmark leader |
| Bifrost | "Maxim's gateway" | Retries + Anthropic fallback recipe |
| Cloudflare AI Gateway | "edge managed" | Edge-deployed managed gateway, zero-ops |
| PII redaction | "data scrub" | Regex + NER mask before sending to model |
| Jailbreak detection | "prompt injection guard" | Classifier on user input |
| Audit trail | "regulated log" | Immutable record of every LLM call |
| Token-bucket | "simple rate limit" | Refill-based rate limiter |
| Sliding-window | "precise rate limit" | Time-windowed rate limiter; better fairness |

## Further Reading | 延伸阅读

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
