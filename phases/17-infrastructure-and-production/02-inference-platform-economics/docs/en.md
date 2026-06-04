# Inference Platform Economics — Fireworks, Together, Baseten, Modal, Replicate, Anyscale | 推理 经济学

> The 2026 inference market is no longer GPU time rental. It bifurcates into custom silicon (Groq, Cerebras, SambaNova), GPU platforms (Baseten, Together, Fireworks, Modal), and API-first marketplaces (Replicate, DeepInfra). Fireworks raised price $1/hr per GPU on May 1, 2026, and $4B valuation on 10T+ tokens/day tells you the volume-driven model works. Baseten closed $300M Series E at $5B in January 2026. The competitive positioning rule is simple: Fireworks optimizes latency, Together optimizes catalog breadth, Baseten optimizes enterprise polish, Modal optimizes Python-native DX, Replicate optimizes multimodal reach, Anyscale optimizes distributed Python. This lesson gives you a matrix you can hand a founder.

> **【中文解读】** 本节介绍了推理平台经济学——LLM 推理服务的成本结构、定价模型和经济学分析。


**Type:** Learn
**Languages:** Python (stdlib, toy per-call economics comparator)
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name the three market segments (custom silicon, GPU platforms, API-first) and map each vendor to a segment.
- Explain why the "per-token" API pricing model compresses toward the serving engine's cost curve, not the hardware's.
- Compute effective cost per request across at least three vendors and explain when per-minute (Baseten, Modal) beats per-token.
- Identify which platform is the right default for a given workload (serverless bursty, steady high-throughput, fine-tuned variants, multimodal).

## The Problem | 问题

You evaluated managed hyperscaler platforms. You decided you need a narrower, faster provider — Fireworks for latency, Together for breadth, Baseten for a fine-tuned custom model. Now you have six real choices and the pricing pages do not line up. Fireworks shows $/M tokens; Baseten shows $/minute; Modal shows $/second; Replicate shows $/prediction. You cannot compare them head-to-head without modeling the workload.

Worse, the business model behind each pricing page is different. Fireworks runs its own custom engine (FireAttention) on shared GPUs; the per-token rate reflects their utilization curve. Baseten gives you Truss + dedicated GPUs; per-minute reflects exclusivity. Modal is true Python serverless — per-second billing with sub-second cold starts. Same output (an LLM response), three different cost functions.

This lesson models the six and tells you when each wins.

> **【中文解读】** 推理平台市场的核心难题是定价模型不统一。按 token 计费（Fireworks/Together）、按分钟计费（Baseten）、按秒计费（Modal）、按预测计费（Replicate）——同样的 LLM 响应，背后是完全不同的成本函数。不能只看单价，必须根据工作负载特征建模才能做出正确选择。

> **【拓展：LLM 推理成本构成】** LLM 推理的成本主要由 GPU 租赁（H100 约 $2-3/hr）、电力（约 $0.3/hr/GPU）、网络带宽和运维组成。推理平台的毛利率通常在 20-40%（a16z 2025 AI 基础设施报告）。优化推理成本的关键是提高 GPU 利用率和 batch 大小——vLLM 的 continuous batching 可将利用率从 30% 提升到 80%+。

## The Concept | 概念

> **【中文解读】** 推理平台市场分为三大细分：(1) 自研芯片（Groq LPU、Cerebras WSE、SambaNova RDU）——以 5-10x 解码速度取胜但单价更高；(2) GPU 平台（Baseten、Together、Fireworks、Modal）——运行 NVIDIA GPU，介于原始 GPU 租赁和 hyperscaler 托管服务之间；(3) API 优先市场（Replicate、DeepInfra、OpenRouter）——强调快速上手和广度。

> **【拓展：自研推理芯片竞赛】** Groq 的 LPU（Language Processing Unit）在 Llama 70B 上可实现 300+ tokens/s，是 GPU 推理的 10x。Cerebras 的 CS-3 晶圆级引擎可达 2000+ tokens/s。但这些芯片的缺点是灵活性低——只能运行特定架构的模型。2025-2026 年自研推理芯片投资超过 $50B（CB Insights），核心赌注是推理需求将超过 GPU 供给。

### The three segments

**Custom silicon** — Groq (LPU), Cerebras (WSE), SambaNova (RDU). Typically 5-10x faster decode than a GPU-based cluster on the same model. Higher per-token price (Groq was ~$0.99/M on Llama-70B late 2025) but unbeatable for latency-sensitive use cases. Groq is the production pick for voice agents and real-time translation.

**GPU platforms** — Baseten, Together, Fireworks, Modal, Anyscale. Run on NVIDIA (H100, H200, B200 in 2026) or sometimes AMD. The economic layer between "raw GPU rental" (RunPod, Lambda) and "hyperscaler managed service" (Bedrock).

**API-first marketplaces** — Replicate, DeepInfra, OpenRouter, Fal. Broad catalog, pay-per-prediction or pay-per-second, emphasize time-to-first-call.

### Fireworks — latency-optimized GPU platform

- FireAttention engine (custom); marketed as 4x lower latency than vLLM on equivalent configs.
- Batch tier at ~50% of serverless rate for non-interactive workloads.
- Fine-tuned model served at the same rate as the base model — a real differentiator versus providers that charge a premium for your LoRA.
- Mid-2026: raised on-demand GPU rental $1/hour effective May 1, 2026. Volume pricing negotiable at scale.
- Financial signal: $4B valuation, 10T+ tokens/day handled.

### Together — breadth-optimized

- 200+ models including open-source releases within days of upstream publication.
- 50-70% cheaper than Replicate on equivalent LLM models — the "AI Native Cloud" positioning is volume and catalog.
- Inference + fine-tuning + training in one API.

### Baseten — enterprise-polish-optimized

- Truss framework: model packaging with dependencies, secrets, serving config in one manifest.
- GPU range from T4 through B200. Per-minute billing with reasonable cold-start mitigation.
- SOC 2 Type II, HIPAA-ready. Common fintech and healthcare pick.
- $5B valuation, January 2026 Series E ($300M from CapitalG, IVP, NVIDIA).

### Modal — Python-native-optimized

- Infrastructure-as-code in pure Python. Decorate a function with `@modal.function(gpu="A100")` and deploy with one command.
- Per-second billing. Cold starts 2-4s with pre-warming; <1s for small models.
- $87M Series B at $1.1B valuation (2025). Strongest developer experience score in independent surveys.

### Replicate — multimodal breadth

- Pay-per-prediction. The default platform for image, video, and audio models.
- Integration ecosystem (Zapier, Vercel, CMS plugins).
- Less competitive on LLM per-token rates but wins on multimodal variety.

### Anyscale — Ray-native

- Built on Ray; RayTurbo is Anyscale's proprietary inference engine (competes with vLLM).
- Best for distributed Python workloads where the inference step is one node in a larger graph.
- Managed Ray clusters; tight integration with Ray AIR and Ray Serve.

### Per-token versus per-minute — when each wins

Per-token makes sense when the workload is latency-insensitive and bursty — you only pay for what you use. Per-minute makes sense when utilization is high and predictable — you beat per-token once you're saturating the GPU.

Rough rule: for workloads above ~30% sustained utilization of a dedicated GPU, per-minute (Baseten, Modal) starts to beat per-token (Fireworks, Together). Below that, per-token wins because you avoid paying for idle.

> **【中文解读】** 定价模型选择的核心是利用率。按 token 计费适合突发、低频场景——只付实际使用量；按分钟计费适合持续高负载场景——当 GPU 利用率超过约 30% 时，按分钟通常更便宜。30% 是经验法则，实际交叉点取决于模型大小、batch 配置和具体平台定价。

> **【拓展：推理经济学趋势】** 2024-2026 年 LLM 推理价格下降了约 90%（ARK Invest 2025 报告）。GPT-4 级别模型的推理成本从 2023 年的 $30/M tokens 降到 2025 年的 $3/M tokens。趋势驱动因素包括：模型量化（INT8/INT4）、更好的 batch 调度、自研芯片竞争和开源推理引擎（vLLM/SGLang）的成熟。预计到 2027 年，同等质量的推理成本将再降 80%。

### Custom engine is the real moat

Every platform above vLLM and SGLang claims a custom engine. FireAttention, RayTurbo, Baseten's inference stack. Custom-engine claims shade marketing — the honest framing is that vLLM + SGLang represent about 80% of production open-source inference, and the differentiators at the platform layer are DX, attribution, and SLAs.

### Numbers you should remember

- Fireworks GPU rental: $1/hr raise effective May 1, 2026.
- Fireworks claim: 4x lower latency than vLLM on equivalent configs.
- Together: 50-70% cheaper than Replicate on LLMs.
- Baseten valuation: $5B (Series E, Jan 2026, $300M round).
- Modal valuation: $1.1B (Series B, 2025).
- Per-minute beats per-token above ~30% sustained utilization.

## Use It | 使用方法

`code/main.py` compares the six vendors on a synthetic workload across pricing models. Reports $/day and effective $/M tokens. Run it to find the break-even between per-token and per-minute.

> **【中文解读】** 实践部分通过模拟工作负载对比六个供应商的定价模型。关键输出是每天成本（$/day）和等效每百万 token 成本（$/M tokens），帮助你找到按 token 和按分钟计费的交叉点。

## Ship It | 部署上线

This lesson produces `outputs/skill-inference-platform-picker.md`. Given workload profile, SLA, and budget, picks the primary inference platform and names the runner-up.

> **【拓展：推理平台选型决策树】** 选型决策路径：(1) 是否需要 < 50ms TTFT？是 → Groq/Cerebras；(2) 是否需要自托管/合规？是 → Baseten/Modal；(3) 是否需要最大模型广度？是 → Together/OpenRouter；(4) 是否需要多媒体模型？是 → Replicate/Fal；(5) 默认 → Fireworks（延迟优化）或 Together（成本优化）。

## Exercises | 练习题

1. Run `code/main.py`. At what sustained utilization does Baseten (per-minute) beat Fireworks (per-token) for a 70B model on one H100? Derive the crossover yourself and compare to the rule of thumb.
2. Your product serves image generation plus chat plus speech-to-text. Pick platforms for each modality and name the gateway pattern that unifies them.
3. Fireworks raises prices by $1/hr on your primary model. Model the blended cost impact if 40% of your traffic moves to batch tier (50% off).
4. A regulated customer requires SOC 2 Type II + HIPAA + dedicated GPUs. Which three platforms are viable and which one wins on FinOps?
5. Compare cost per 1,000 predictions for Llama 3.1 70B on Fireworks serverless, Together on-demand, Baseten dedicated, and Replicate API. Which is cheapest at 10 predictions/day? At 10,000?

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Custom silicon | "non-GPU chips" | Groq LPU, Cerebras WSE, SambaNova RDU — optimized for decode | 自研推理芯片——Groq LPU、Cerebras WSE 等 |
| FireAttention | "Fireworks engine" | Custom attention kernel; marketed at 4x lower latency than vLLM | Fireworks 自研注意力引擎，号称比 vLLM 快 4x |
| Truss | "Baseten's format" | Model packaging manifest; dependencies + secrets + serving config | Baseten 的模型打包格式，包含依赖、密钥、服务配置 |
| Per-token | "API pricing" | Charge by tokens consumed; pay for no idle | 按 token 计费——只付实际使用量 |
| Per-minute | "dedicated pricing" | Charge by wall-clock GPU time; wins at high utilization | 按分钟计费——高利用率时更划算 |
| Per-prediction | "Replicate pricing" | Charge per model invocation; common for image/video | 按预测次数计费——常见于图像/视频模型 |
| RayTurbo | "Anyscale engine" | Proprietary inference on Ray; competes with vLLM on Ray clusters | Anyscale 基于 Ray 的自研推理引擎 |
| Batch tier | "50% off" | Non-interactive queue at reduced rate; common on Fireworks, OpenAI | 批量推理队列——半价用于非交互任务 |
| Fine-tuned at base rate | "Fireworks LoRA" | Charge LoRA-served requests at base model's rate (differentiator) | 微调模型按基础模型费率计费 |

## Further Reading | 延伸阅读

- [Fireworks Pricing](https://fireworks.ai/pricing) — per-token rates, batch tier, GPU rental.
- [Baseten Pricing](https://www.baseten.co/pricing/) — per-minute rates, committed capacity, enterprise tiers.
- [Modal Pricing](https://modal.com/pricing) — per-second GPU rates and free tier.
- [Together AI Pricing](https://www.together.ai/pricing) — model catalog and per-token rates.
- [Anyscale Pricing](https://www.anyscale.com/pricing) — RayTurbo and managed Ray pricing.
- [Northflank — Fireworks AI Alternatives](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference) — comparative assessment.
- [Infrabase — AI Inference API Providers 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) — vendor landscape.
