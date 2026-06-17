# Inference Platform Economics — Fireworks, Together, Baseten, Modal, Replicate, Anyscale | 推理 经济学

> The 2026 inference market is no longer GPU time rental. It bifurcates into custom silicon (Groq, Cerebras, SambaNova), GPU platforms (Baseten, Together, Fireworks, Modal), and API-first marketplaces (Replicate, DeepInfra). Fireworks raised price $1/hr per GPU on May 1, 2026, and $4B valuation on 10T+ tokens/day tells you the volume-driven model works. Baseten closed $300M Series E at $5B in January 2026. The competitive positioning rule is simple: Fireworks optimizes latency, Together optimizes catalog breadth, Baseten optimizes enterprise polish, Modal optimizes Python-native DX, Replicate optimizes multimodal reach, Anyscale optimizes distributed Python. This lesson gives you a matrix you can hand a founder.

> **【中文解读】** 本节介绍了推理平台经济学——LLM 推理服务的成本结构、定价模型和经济学分析。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy per-call economics comparator) | **语言:** Python（标准库，每次调用经济性比较器）
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 01（托管 LLM 平台）, Phase 17 · 04（vLLM 服务内部）

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·01（托管 LLM 平台）、Phase 17·04（vLLM 内部）。本节是 2026 推理平台选型矩阵。
> 💡 **【类比】** 推理平台 = "AI 云服务商"。三类：(1) 定制芯片（Groq/Cerebras/SambaNova）= 专用 CPU；(2) GPU 平台（Baseten/Together/Fireworks/Modal）= 通用云；(3) API 市场（Replicate/DeepInfra）= 应用商店。选型口诀：Fireworks 低延迟、Together 模型多、Baseten 企业级、Modal Python 原生、Replicate 多模态广、Anyscale 分布式 Python。

## Learning Objectives | 学习目标

- Name the three market segments (custom silicon, GPU platforms, API-first) and map each vendor to a segment.
  中文翻译：说出三个市场细分（自研芯片、GPU 平台、API 优先），并将每个供应商映射到对应细分。
- Explain why the "per-token" API pricing model compresses toward the serving engine's cost curve, not the hardware's.
  中文翻译：解释为什么"按 token"API 定价模型压缩到服务引擎的成本曲线而非硬件成本。
- Compute effective cost per request across at least three vendors and explain when per-minute (Baseten, Modal) beats per-token.
  中文翻译：计算至少三个供应商的每次请求有效成本，并解释按分钟（Baseten、Modal）何时优于按 token。
- Identify which platform is the right default for a given workload (serverless bursty, steady high-throughput, fine-tuned variants, multimodal).
  中文翻译：识别哪个平台是给定工作负载的正确默认选择（无服务器突发、稳定高吞吐、微调变体、多模态）。

## The Problem | 问题引入

You evaluated managed hyperscaler platforms. You decided you need a narrower, faster provider — Fireworks for latency, Together for breadth, Baseten for a fine-tuned custom model. Now you have six real choices and the pricing pages do not line up. Fireworks shows $/M tokens; Baseten shows $/minute; Modal shows $/second; Replicate shows $/prediction. You cannot compare them head-to-head without modeling the workload.

> 你评估了托管云平台后，决定需要一个更专注、更快的供应商——Fireworks 追求延迟、Together 追求广度、Baseten 追求微调自定义模型。现在你有六个真实选择，但定价页面无法直接对比。Fireworks 显示 $/M tokens；Baseten 显示 $/分钟；Modal 显示 $/秒；Replicate 显示 $/预测。不建模工作负载就无法直接比较。

Worse, the business model behind each pricing page is different. Fireworks runs its own custom engine (FireAttention) on shared GPUs; the per-token rate reflects their utilization curve. Baseten gives you Truss + dedicated GPUs; per-minute reflects exclusivity. Modal is true Python serverless — per-second billing with sub-second cold starts. Same output (an LLM response), three different cost functions.

> 更糟糕的是，每个定价页面背后的商业模式不同。Fireworks 在共享 GPU 上运行自研引擎（FireAttention）；按 token 费率反映其利用率曲线。Baseten 提供 Truss + 专用 GPU；按分钟反映独占性。Modal 是真正的 Python 无服务器——按秒计费，亚秒级冷启动。同样的输出（LLM 响应），三种不同的成本函数。

This lesson models the six and tells you when each wins.

> 本课建模六个平台，告诉你每个在何时胜出。

> **【中文解读】** 推理平台市场的核心难题是定价模型不统一。按 token 计费（Fireworks/Together）、按分钟计费（Baseten）、按秒计费（Modal）、按预测计费（Replicate）——同样的 LLM 响应，背后是完全不同的成本函数。不能只看单价，必须根据工作负载特征建模才能做出正确选择。

> **【拓展：LLM 推理成本构成】** LLM 推理的成本主要由 GPU 租赁（H100 约 $2-3/hr）、电力（约 $0.3/hr/GPU）、网络带宽和运维组成。推理平台的毛利率通常在 20-40%（a16z 2025 AI 基础设施报告）。优化推理成本的关键是提高 GPU 利用率和 batch 大小——vLLM 的 continuous batching 可将利用率从 30% 提升到 80%+。

## The Concept | 核心概念

> **【中文解读】** 推理平台市场分为三大细分：(1) 自研芯片（Groq LPU、Cerebras WSE、SambaNova RDU）——以 5-10x 解码速度取胜但单价更高；(2) GPU 平台（Baseten、Together、Fireworks、Modal）——运行 NVIDIA GPU，介于原始 GPU 租赁和 hyperscaler 托管服务之间；(3) API 优先市场（Replicate、DeepInfra、OpenRouter）——强调快速上手和广度。

> **【拓展：自研推理芯片竞赛】** Groq 的 LPU（Language Processing Unit）在 Llama 70B 上可实现 300+ tokens/s，是 GPU 推理的 10x。Cerebras 的 CS-3 晶圆级引擎可达 2000+ tokens/s。但这些芯片的缺点是灵活性低——只能运行特定架构的模型。2025-2026 年自研推理芯片投资超过 $50B（CB Insights），核心赌注是推理需求将超过 GPU 供给。

### The three segments

**Custom silicon** — Groq (LPU), Cerebras (WSE), SambaNova (RDU). Typically 5-10x faster decode than a GPU-based cluster on the same model. Higher per-token price (Groq was ~$0.99/M on Llama-70B late 2025) but unbeatable for latency-sensitive use cases. Groq is the production pick for voice agents and real-time translation.

> **自研芯片** —— Groq（LPU）、Cerebras（WSE）、SambaNova（RDU）。通常比同模型的 GPU 集群解码速度快 5-10 倍。按 token 价格更高（Groq 2025 年末在 Llama-70B 上约 $0.99/M），但对延迟敏感用例无可匹敌。Groq 是语音代理和实时翻译的生产选择。

**GPU platforms** — Baseten, Together, Fireworks, Modal, Anyscale. Run on NVIDIA (H100, H200, B200 in 2026) or sometimes AMD. The economic layer between "raw GPU rental" (RunPod, Lambda) and "hyperscaler managed service" (Bedrock).

> **GPU 平台** —— Baseten、Together、Fireworks、Modal、Anyscale。运行在 NVIDIA（2026 年的 H100、H200、B200）或有时是 AMD 上。"原始 GPU 租赁"（RunPod、Lambda）和"云托管服务"（Bedrock）之间的经济层。

**API-first marketplaces** — Replicate, DeepInfra, OpenRouter, Fal. Broad catalog, pay-per-prediction or pay-per-second, emphasize time-to-first-call.

> **API 优先市场** —— Replicate、DeepInfra、OpenRouter、Fal。广泛目录，按预测或按秒付费，强调首次调用速度。

### Fireworks — latency-optimized GPU platform

- FireAttention engine (custom); marketed as 4x lower latency than vLLM on equivalent configs.
  中文翻译：FireAttention 引擎（自研）；宣传为比等效配置的 vLLM 延迟低 4 倍。
- Batch tier at ~50% of serverless rate for non-interactive workloads.
  中文翻译：批量层级约为无服务器费率的 50%，用于非交互工作负载。
- Fine-tuned model served at the same rate as the base model — a real differentiator versus providers that charge a premium for your LoRA.
  中文翻译：微调模型按基础模型费率服务——与对 LoRA 收取溢价的供应商相比是真正的差异化因素。
- Mid-2026: raised on-demand GPU rental $1/hour effective May 1, 2026. Volume pricing negotiable at scale.
  中文翻译：2026 年中：自 5 月 1 日起按量 GPU 租赁涨价 $1/小时。大批量价格可协商。
- Financial signal: $4B valuation, 10T+ tokens/day handled.
  中文翻译：财务信号：$4B 估值，每日处理 10T+ token。

### Together — breadth-optimized

- 200+ models including open-source releases within days of upstream publication.
  中文翻译：200+ 模型，包括上游发布后数天内的开源版本。
- 50-70% cheaper than Replicate on equivalent LLM models — the "AI Native Cloud" positioning is volume and catalog.
  中文翻译：比 Replicate 在等效 LLM 模型上便宜 50-70%——"AI 原生云"定位是规模和目录。
- Inference + fine-tuning + training in one API.
  中文翻译：推理 + 微调 + 训练在一个 API 中。

### Baseten — enterprise-polish-optimized

- Truss framework: model packaging with dependencies, secrets, serving config in one manifest.
  中文翻译：Truss 框架：模型打包，包含依赖、密钥、服务配置在一个清单中。
- GPU range from T4 through B200. Per-minute billing with reasonable cold-start mitigation.
  中文翻译：GPU 范围从 T4 到 B200。按分钟计费，有合理的冷启动缓解。
- SOC 2 Type II, HIPAA-ready. Common fintech and healthcare pick.
  中文翻译：SOC 2 Type II、HIPAA 就绪。常见金融科技和医疗保健选择。
- $5B valuation, January 2026 Series E ($300M from CapitalG, IVP, NVIDIA).
  中文翻译：$5B 估值，2026 年 1 月 E 轮融资（来自 CapitalG、IVP、NVIDIA 的 $300M）。

### Modal — Python-native-optimized

- Infrastructure-as-code in pure Python. Decorate a function with `@modal.function(gpu="A100")` and deploy with one command.
  中文翻译：纯 Python 的基础设施即代码。用 `@modal.function(gpu="A100")` 装饰函数，一条命令部署。
- Per-second billing. Cold starts 2-4s with pre-warming; <1s for small models.
  中文翻译：按秒计费。预热后冷启动 2-4 秒；小模型 <1 秒。
- $87M Series B at $1.1B valuation (2025). Strongest developer experience score in independent surveys.
  中文翻译：B 轮融资 $87M，估值 $1.1B（2025）。独立调查中开发者体验评分最高。

### Replicate — multimodal breadth

- Pay-per-prediction. The default platform for image, video, and audio models.
  中文翻译：按预测付费。图像、视频和音频模型的默认平台。
- Integration ecosystem (Zapier, Vercel, CMS plugins).
  中文翻译：集成生态系统（Zapier、Vercel、CMS 插件）。
- Less competitive on LLM per-token rates but wins on multimodal variety.
  中文翻译：LLM 按 token 费率竞争力较弱，但在多模态多样性上获胜。

### Anyscale — Ray-native

- Built on Ray; RayTurbo is Anyscale's proprietary inference engine (competes with vLLM).
  中文翻译：基于 Ray 构建；RayTurbo 是 Anyscale 的专有推理引擎（与 vLLM 竞争）。
- Best for distributed Python workloads where the inference step is one node in a larger graph.
  中文翻译：最适合推理步骤是更大图中一个节点的分布式 Python 工作负载。
- Managed Ray clusters; tight integration with Ray AIR and Ray Serve.
  中文翻译：托管 Ray 集群；与 Ray AIR 和 Ray Serve 紧密集成。

### Per-token versus per-minute — when each wins

Per-token makes sense when the workload is latency-insensitive and bursty — you only pay for what you use. Per-minute makes sense when utilization is high and predictable — you beat per-token once you're saturating the GPU.

> 当工作负载对延迟不敏感且突发时，按 token 计费更合理——你只付实际使用量。当利用率高且可预测时，按分钟计费更合理——一旦 GPU 饱和就优于按 token。

Rough rule: for workloads above ~30% sustained utilization of a dedicated GPU, per-minute (Baseten, Modal) starts to beat per-token (Fireworks, Together). Below that, per-token wins because you avoid paying for idle.

> 粗略规则：对于专用 GPU 持续利用率超过约 30% 的工作负载，按分钟（Baseten、Modal）开始优于按 token（Fireworks、Together）。低于此值时，按 token 获胜，因为避免了为空闲付费。

> **【中文解读】** 定价模型选择的核心是利用率。按 token 计费适合突发、低频场景——只付实际使用量；按分钟计费适合持续高负载场景——当 GPU 利用率超过约 30% 时，按分钟通常更便宜。30% 是经验法则，实际交叉点取决于模型大小、batch 配置和具体平台定价。

> **【拓展：推理经济学趋势】** 2024-2026 年 LLM 推理价格下降了约 90%（ARK Invest 2025 报告）。GPT-4 级别模型的推理成本从 2023 年的 $30/M tokens 降到 2025 年的 $3/M tokens。趋势驱动因素包括：模型量化（INT8/INT4）、更好的 batch 调度、自研芯片竞争和开源推理引擎（vLLM/SGLang）的成熟。预计到 2027 年，同等质量的推理成本将再降 80%。

### Custom engine is the real moat

Every platform above vLLM and SGLang claims a custom engine. FireAttention, RayTurbo, Baseten's inference stack. Custom-engine claims shade marketing — the honest framing is that vLLM + SGLang represent about 80% of production open-source inference, and the differentiators at the platform layer are DX, attribution, and SLAs.

> 每个超越 vLLM 和 SGLang 的平台都声称有自研引擎。FireAttention、RayTurbo、Baseten 的推理栈。自研引擎声明有营销成分——诚实的说法是 vLLM + SGLang 占生产环境开源推理的约 80%，平台层的差异化因素是开发者体验、归因和 SLA。

### Numbers you should remember

- Fireworks GPU rental: $1/hr raise effective May 1, 2026.
  中文翻译：Fireworks GPU 租赁：自 2026 年 5 月 1 日起涨价 $1/小时。
- Fireworks claim: 4x lower latency than vLLM on equivalent configs.
  中文翻译：Fireworks 声称：等效配置下比 vLLM 延迟低 4 倍。
- Together: 50-70% cheaper than Replicate on LLMs.
  中文翻译：Together：LLM 上比 Replicate 便宜 50-70%。
- Baseten valuation: $5B (Series E, Jan 2026, $300M round).
  中文翻译：Baseten 估值：$5B（E 轮，2026 年 1 月，$300M 轮次）。
- Modal valuation: $1.1B (Series B, 2025).
  中文翻译：Modal 估值：$1.1B（B 轮，2025）。
- Per-minute beats per-token above ~30% sustained utilization.
  中文翻译：持续利用率超过约 30% 时按分钟优于按 token。

## Use It | 用框架实现

`code/main.py` compares the six vendors on a synthetic workload across pricing models. Reports $/day and effective $/M tokens. Run it to find the break-even between per-token and per-minute.

> `code/main.py` 在合成工作负载上比较六个供应商的定价模型。报告 $/天和等效 $/M tokens。运行它找到按 token 和按分钟的盈亏平衡点。

> **【中文解读】** 实践部分通过模拟工作负载对比六个供应商的定价模型。关键输出是每天成本（$/day）和等效每百万 token 成本（$/M tokens），帮助你找到按 token 和按分钟计费的交叉点。

## Ship It | 产出物

This lesson produces `outputs/skill-inference-platform-picker.md`. Given workload profile, SLA, and budget, picks the primary inference platform and names the runner-up.

> 本课产出 `outputs/skill-inference-platform-picker.md`。给定工作负载配置、SLA 和预算，选择主要推理平台并命名备选。

> **【拓展：推理平台选型决策树】** 选型决策路径：(1) 是否需要 < 50ms TTFT？是 → Groq/Cerebras；(2) 是否需要自托管/合规？是 → Baseten/Modal；(3) 是否需要最大模型广度？是 → Together/OpenRouter；(4) 是否需要多媒体模型？是 → Replicate/Fal；(5) 默认 → Fireworks（延迟优化）或 Together（成本优化）。

## Exercises | 练习题

1. Run `code/main.py`. At what sustained utilization does Baseten (per-minute) beat Fireworks (per-token) for a 70B model on one H100? Derive the crossover yourself and compare to the rule of thumb.
   中文翻译：运行 `code/main.py`。Baseten（按分钟）在什么持续利用率下对一台 H100 上的 70B 模型优于 Fireworks（按 token）？自行推导交叉点并与经验法则比较。
2. Your product serves image generation plus chat plus speech-to-text. Pick platforms for each modality and name the gateway pattern that unifies them.
   中文翻译：你的产品提供图像生成、聊天和语音转文字。为每种模态选择平台并命名统一它们的网关模式。
3. Fireworks raises prices by $1/hr on your primary model. Model the blended cost impact if 40% of your traffic moves to batch tier (50% off).
   中文翻译：Fireworks 将你的主要模型涨价 $1/小时。如果 40% 的流量转移到批量层级（半价），建模混合成本影响。
4. A regulated customer requires SOC 2 Type II + HIPAA + dedicated GPUs. Which three platforms are viable and which one wins on FinOps?
   中文翻译：一个受监管客户需要 SOC 2 Type II + HIPAA + 专用 GPU。哪三个平台可行，哪个在 FinOps 上获胜？
5. Compare cost per 1,000 predictions for Llama 3.1 70B on Fireworks serverless, Together on-demand, Baseten dedicated, and Replicate API. Which is cheapest at 10 predictions/day? At 10,000?
   中文翻译：比较 Llama 3.1 70B 在 Fireworks 无服务器、Together 按量、Baseten 专用和 Replicate API 上每 1,000 次预测的成本。每天 10 次预测哪个最便宜？每天 10,000 次呢？

## Key Terms | 术语速查表

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
