# Managed LLM Platforms — Bedrock, Vertex AI, Azure OpenAI | 平台 托管 OpenAI LLM

> Three hyperscalers, three distinct strategies. AWS Bedrock is a model marketplace — Claude, Llama, Titan, Stability, Cohere behind one API. Azure OpenAI is an exclusive OpenAI partnership plus Provisioned Throughput Units (PTUs) for dedicated capacity. Vertex AI is Gemini-first with the best long-context and multimodal story. In 2026 Artificial Analysis measures Azure OpenAI at ~50 ms median and Bedrock at ~75 ms on Llama 3.1 405B equivalents — PTUs explain the gap because dedicated capacity beats shared on-demand. The decision rule is not "which is fastest" but "which model catalog and FinOps surface match my product." This lesson teaches you to pick with the tradeoffs written down, not vibes.

> **【中文解读】** 本节介绍了托管 LLM 平台——OpenAI、Anthropic、Google 等提供的模型服务平台的选型和对比。


**Type:** Learn
**Languages:** Python (stdlib, toy cost-and-latency comparator)
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name the three platform strategies (marketplace vs exclusive vs Gemini-first) and match each to a product use case.
- Explain what Provisioned Throughput Units (PTUs) buy you in Azure OpenAI and why on-demand Bedrock typically reads ~25 ms slower at the 405B scale.
- Diagram the FinOps attribution surface for each platform (Bedrock Application Inference Profiles vs Vertex project-per-team vs Azure scopes + PTU reservations).
- Write down a "two-provider minimum" policy and explain why single-vendor lock-in is the expensive mistake in 2026.

## The Problem | 问题

You picked Claude 3.7 Sonnet for your product. Now you need to serve it. You can call the Anthropic API directly, or you can call it through AWS Bedrock, or you can go through a gateway. The direct API is the simplest; Bedrock adds BAAs, VPC endpoints, IAM, and CloudWatch attribution. The gateway adds failover, unified billing, and rate limits across providers.

The deeper question is catalog. If you need Claude and Llama and Gemini in the same product, you cannot buy them all from one place unless that place is Bedrock plus Vertex plus Azure OpenAI simultaneously. The hyperscalers are not interchangeable — they each made a different bet on who owns the model layer.

This lesson maps the three bets, the latency gap, the FinOps gap, and the lock-in risk.

> **【中文解读】** 选定 LLM 后，"在哪里部署"是一个基础设施级别的决策。直接调用 API 最简单，但缺乏企业级控制；通过云平台（Bedrock/Vertex/Azure）调用增加了合规、审计能力；通过网关调用则获得多供应商容灾和统一计费。核心矛盾在于：三大云厂商的模型目录不重叠，无法在单一平台获取所有前沿模型。

> **【拓展：LLM 部署模式】** 2024-2026 年 LLM 服务部署模式经历了从 "直接 API" → "云平台托管" → "AI 网关统一路由" 的演进。OpenRouter、Portkey、LiteLLM 等 AI 网关项目在 2025 年获得大量采用，核心价值是在多供应商之间提供统一接口、自动 failover 和成本优化。企业级部署中，约 60% 已采用网关模式（Gartner 2025 AI 基础设施报告）。

## The Concept | 概念

> **【中文解读】** 三大云厂商的 LLM 平台策略截然不同：AWS Bedrock 是"模型集市"，聚合多家供应商；Azure OpenAI 是"独家合作"，专供 OpenAI 模型；Vertex AI 是"Gemini 优先"，以超长上下文和多媒体能力为卖点。理解这些策略差异是做出正确选型的基础。

> **【拓展：全球 LLM 云平台格局】** 除三大 hyperscaler 外，2026 年值得关注的还有：Cloudflare Workers AI（边缘推理）、Together AI（开源模型推理平台，$0.18/M tokens for Llama 3.1 70B）、Groq（LPU 推理引擎，TTFT < 20ms）、Cerebras（CS-3 wafer-scale 推理，2000+ tokens/s）。国内有百度千帆、阿里百炼、火山方舟等，但模型目录与国际平台不互通。

### Three strategies

**AWS Bedrock** — the marketplace. Claude (Anthropic), Llama (Meta), Titan (AWS first-party), Stability (image), Cohere (embeddings), Mistral, plus image and embedding sub-catalogs. One API, one IAM surface, one CloudWatch export. Bedrock's bet is that customers want optionality more than they want a single model.

**Azure OpenAI** — the exclusive partnership. You get GPT-4 / 4o / 5 / o-series, DALL·E, Whisper, and fine-tuning of OpenAI models in Azure datacenters. No non-OpenAI models in the "Azure OpenAI Service" catalog — those go to Azure AI Foundry (separate product). Azure's bet is that OpenAI remains the frontier and customers want enterprise controls on that specific relationship.

**Vertex AI** — Gemini first, everything else second. Gemini 1.5 / 2.0 / 2.5 Flash and Pro, plus Model Garden (third-party). Vertex's bet is multimodal long-context — 1M-token Gemini context is the differentiator.

### Latency gap at scale

Artificial Analysis runs continuous benchmarks. On equivalent Llama 3.1 405B deployments (shared on-demand), Azure OpenAI median first-token latency is around 50 ms; Bedrock is around 75 ms. The gap is not an AWS failure — it is a capacity model difference. Azure sells PTUs (Provisioned Throughput Units), which reserve GPU capacity for your tenant. Bedrock's equivalent (Provisioned Throughput) exists but starts around $21/hour per unit, and most customers stay on shared on-demand.

On-demand shared capacity competes with every other customer's traffic. Dedicated capacity does not. If your product SLA is TTFT < 100 ms at P99, you either buy PTUs on Azure, buy Bedrock Provisioned Throughput, or accept the default variance.

> **【中文解读】** 延迟差距的本质是"容量模型"差异。共享按量部署中，你的请求与所有其他客户的流量竞争 GPU 资源；专用容量（PTU）则预留了独占的 GPU。Azure PTU 在 40-60% 利用率时可节省高达 70% 成本，但空闲时仍然付费。Bedrock 的按量模式 TTFT 中位数约 75ms，Azure PTU 约 50ms，25ms 差距在高频交互场景中会被用户感知。

### Provisioned Throughput economics

Azure PTUs: a reserved block of inference compute. Up to ~70% savings vs on-demand for predictable workloads. Costs fixed per hour regardless of traffic — you pay for the reservation even when idle. The break-even is usually around 40-60% sustained utilization.

Bedrock Provisioned Throughput: $21-$50 per hour depending on model and region. Similar math — break-even is around half peak utilization. Monthly commitment required.

Vertex provisioned capacity is sold per Gemini SKU; pricing varies by model and region and is less publicly advertised.

### FinOps surface — the real differentiator

**Bedrock Application Inference Profiles** are the cleanest attribution in the marketplace. Tag a profile with `team`, `product`, `feature`; route all model invocations through it; CloudWatch breaks out cost per profile without post-processing. Added 2025, still the most granular hyperscaler native.

**Vertex** attribution is project-per-team plus labels-everywhere. You model each team as a GCP project, put labels on every resource, and use BigQuery Billing Export + DataStudio for rollups. More work, but BigQuery gives you arbitrary SQL on the cost data.

**Azure** relies on subscription/resource-group scopes plus tags, with PTU reservations as a first-class cost object. Tags are inherited from resource groups, not requests, so per-request attribution requires Application Insights custom metrics or a gateway that stamps headers.

The pattern: Bedrock is cleanest native, Vertex is most flexible via BigQuery, Azure is most opaque unless you instrument.

> **【中文解读】** FinOps（云财务运营）是 LLM 基础设施中最被低估的维度。Bedrock 的 Application Inference Profiles 是目前最精细的原生成本归因方案——按团队、产品、功能标签拆分调用成本；Vertex 通过 BigQuery 导出提供最大灵活性，可用 SQL 做任意聚合；Azure 最为不透明，除非你自行用 Application Insights 埋点。选择平台时，FinOps 能力与延迟、价格同等重要。

> **【拓展：LLM FinOps 实践】** 企业 LLM 支出在 2025 年平均增长了 300%（Flexera 2025 云状态报告）。常见 FinOps 策略包括：(1) 按 token 消耗设置团队预算告警；(2) 使用缓存层（Semantic Cache）减少重复调用约 30-40%；(3) 模型路由——简单任务用小模型、复杂任务用大模型，可节省 50%+ 成本；(4) 批量 API 在非实时场景可降低 50% 价格。

### Lock-in is the 2026 risk

Single-hyperscaler commitment was fine when one model dominated. In 2026 the frontier moves monthly — Claude 3.7 one quarter, Gemini 2.5 the next, GPT-5 the quarter after. Locking to one platform locks you out of two-thirds of the frontier.

The pattern working teams adopt: two-provider minimum for any product-critical LLM call. Bedrock plus Azure OpenAI is the common pair — Claude from one, GPT from the other, failover between them, same gateway. Cost uplift is negligible because gateway routes optimal; availability uplift during outages (like the Azure OpenAI January 2025 incident, the AWS us-east-1 outage) is decisive.

> **【中文解读】** 2026 年的最大基础设施风险是供应商锁定。前沿模型每季度都在更替——Q1 用 Claude 3.7，Q2 用 Gemini 2.5，Q3 用 GPT-5。锁定单一平台意味着错过 2/3 的前沿能力。最佳实践是"双供应商最低"策略：Bedrock + Azure OpenAI 是最常见组合，通过网关统一路由，成本增加可忽略，但在故障时的可用性提升显著。

> **【拓展：云厂商宕机事件】** 2025 年 1 月 Azure OpenAI 经历了长达数小时的全局性故障，影响所有依赖单一 Azure 的 ChatGPT 企业客户。同年 AWS us-east-1 区域也发生严重故障。多供应商策略在这些事件中证明了其价值：当一家宕机时，网关自动将流量切换到另一家，实现零感知故障转移。Cloudflare 的 2025 年可用性报告显示，多供应商架构的 LLM 服务可用性可达 99.99%，而单供应商通常为 99.9%。

### Data residency, BAAs, and regulated industries

Bedrock: BAAs in most regions; VPC endpoints; guardrails. Common fintech default.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; EU data residency; the enterprise-regulated default.
Vertex: HIPAA, GDPR, data residency per region; Google Cloud's compliance stack.

All three meet the basic checkbox. The differences are in data retention policies, how logs are handled, and whether abuse-monitoring reads your traffic (default opt-in on most; opt-out available for enterprise).

### Numbers you should remember

- Azure OpenAI median TTFT on Llama 3.1 405B equivalents: ~50 ms (with PTUs).
- Bedrock median TTFT on-demand: ~75 ms.
- Bedrock Provisioned Throughput: $21-$50/hr per unit.
- Azure PTU break-even: ~40-60% sustained utilization.
- PTU savings vs on-demand at high utilization: up to 70%.

## Use It | 使用方法

`code/main.py` compares the three platforms on a synthetic workload — it models on-demand vs PTU economics, TTFT variance, and cost attribution fidelity. Run it to see where PTUs pay off and where the marketplace's model breadth outweighs a TTFT gap.

> **【中文解读】** 实践部分通过模拟工作负载对比三大平台。关键指标包括：TTFT（首 token 延迟）、吞吐量、每百万 token 成本。通过调整利用率参数，可以直观看到 PTU 在什么负载水平下比按量计费更划算。

## Ship It | 部署上线

This lesson produces `outputs/skill-managed-platform-picker.md`. Given a workload profile (models needed, TTFT SLA, daily volume, compliance requirements), it recommends a primary platform, a fallback, and a FinOps instrumentation plan.

> **【拓展：生产环境平台选型 Checklist】** 生产环境 LLM 平台选型应考虑：(1) 模型目录是否覆盖所需模型；(2) 延迟 SLA 是否满足用户体验要求（对话 < 200ms TTFT，批处理无严格要求）；(3) 合规认证（HIPAA/SOC2/ISO27001）；(4) 数据驻留（GDPR 要求 EU 区域存储）；(5) 成本归因粒度（能否按团队/产品拆分账单）；(6) 容灾方案（多区域/多供应商 failover）。

## Exercises | 练习题

1. Run `code/main.py`. At what sustained utilization does Azure PTU beat on-demand for a 70B class model? Compute the break-even and compare to the advertised 40-60% band.
2. Your product needs Claude 3.7 Sonnet and GPT-4o. Design a two-provider deployment — which goes to which hyperscaler, what gateway sits in front, what is the failover policy?
3. A regulated healthcare customer requires BAAs, US-East data residency, and sub-100ms P99 TTFT. Pick a platform and justify with three specific features.
4. You discover your Bedrock bill is up 4x this month with no traffic change. Without Application Inference Profiles, how would you find the culprit? With profiles, how long does it take?
5. Read the Azure OpenAI and Bedrock pricing pages. For a 100M-token/month Claude workload, which is cheaper — direct Anthropic API, Bedrock on-demand, or Bedrock Provisioned Throughput?

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Bedrock | "AWS LLM service" | Model marketplace across Claude, Llama, Titan, Mistral, Cohere | AWS 的 LLM 模型集市平台 |
| Azure OpenAI | "Azure's ChatGPT" | Exclusive OpenAI models in Azure datacenters with enterprise controls | Azure 独家托管 OpenAI 模型的企业服务 |
| Vertex AI | "Google's LLM" | Gemini-first platform with Model Garden for third-party models | Google 的 Gemini 优先 AI 平台 |
| PTU | "dedicated capacity" | Provisioned Throughput Unit — reserved inference GPUs, priced per hour | 预置吞吐量单位——独占推理 GPU 容量 |
| Application Inference Profile | "Bedrock tagging" | Per-product cost/usage profile with tags, CloudWatch-native | Bedrock 按产品归因的推理配置文件 |
| Model Garden | "Vertex catalog" | Vertex AI's third-party model section, separate from Gemini | Vertex AI 第三方模型目录 |
| Two-provider minimum | "LLM redundancy" | Policy of running every critical LLM path across ≥2 hyperscalers | 双供应商最低策略——关键 LLM 调用跨 2+ 云商 |
| BAA | "HIPAA paperwork" | Business Associate Agreement; required for PHI; provided by all three | 业务关联协议——HIPAA 合规必需 |
| Abuse monitoring | "the log watcher" | Provider-side safety scan on prompts/outputs; opt-out in enterprise | 平台侧的 prompt/输出安全扫描 |

## Further Reading | 延伸阅读

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) — authoritative rate card and Provisioned Throughput pricing.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) — PTU economics and rate cards.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) — Gemini tiers and Model Garden surcharges.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) — continuous latency and throughput benchmarks across providers.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) — enterprise decision framework.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) — attribution mechanics side-by-side.
