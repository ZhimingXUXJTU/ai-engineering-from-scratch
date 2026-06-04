# 推理平台经济学 — Fireworks、Together、Baseten、Modal、Replicate、Anyscale | 推理 经济学

> 2026 年的推理市场不再只是 GPU 时间租赁。它分化为自研芯片（Groq、Cerebras、SambaNova）、GPU 平台（Baseten、Together、Fireworks、Modal）和 API 优先集市（Replicate、DeepInfra）。Fireworks 在 2026 年 5 月 1 日将 GPU 租赁价格提高至 $1/小时，40 亿估值和每天 10T+ token 的处理量说明以量取胜的模式是有效的。Baseten 在 2026 年 1 月完成了 $3 亿 E 轮融资，估值 $50 亿。竞争定位规则很简单：Fireworks 优化延迟，Together 优化目录广度，Baseten 优化企业品质，Modal 优化 Python 原生开发体验，Replicate 优化多模态覆盖，Anyscale 优化分布式 Python。本课程给你一个可以直接交给创始人的矩阵。

> **【中文解读】** 本节介绍了推理平台经济学——LLM 推理服务的成本结构、定价模型和经济学分析。


**类型：** 学习
**语言：** Python（标准库，模拟每次调用经济学比较器）
**前置条件：** Phase 17 · 01（托管 LLM 平台），Phase 17 · 04（vLLM 推理服务内部机制）
**时间：** 约 60 分钟

## 学习目标

- 说出三个市场细分（自研芯片、GPU 平台、API 优先）并将每个供应商映射到一个细分。
- 解释为什么"按 token"API 定价模型向服务引擎的成本曲线压缩，而不是向硬件成本曲线。
- 计算至少三个供应商的有效每请求成本，并解释按分钟（Baseten、Modal）何时胜过按 token。
- 识别哪个平台是给定工作负载（无服务器突发、稳定高吞吐、微调变体、多模态）的正确默认选择。

## 问题引入

你评估了托管超大规模云平台。你决定需要一个更窄、更快的供应商——Fireworks 为了延迟，Together 为了广度，Baseten 用于微调自定义模型。现在你有六个真正的选择，定价页面对不上。Fireworks 显示 $/M tokens；Baseten 显示 $/分钟；Modal 显示 $/秒；Replicate 显示 $/预测。你无法在不建模工作负载的情况下进行直接对比。

更糟糕的是，每个定价页面背后的商业模式不同。Fireworks 运行自己的自定义引擎（FireAttention）在共享 GPU 上；按 token 费率反映它们的利用率曲线。Baseten 给你 Truss + 专用 GPU；按分钟反映独占性。Modal 是真正的 Python 无服务器——按秒计费，亚秒级冷启动。同样的输出（LLM 响应），三种不同的成本函数。

本课程对六者进行建模，告诉你每个何时胜出。

> **【中文解读】** 推理平台市场的核心难题是定价模型不统一。按 token 计费（Fireworks/Together）、按分钟计费（Baseten）、按秒计费（Modal）、按预测计费（Replicate）——同样的 LLM 响应，背后是完全不同的成本函数。不能只看单价，必须根据工作负载特征建模才能做出正确选择。

> **【拓展：LLM 推理成本构成】** LLM 推理的成本主要由 GPU 租赁（H100 约 $2-3/hr）、电力（约 $0.3/hr/GPU）、网络带宽和运维组成。推理平台的毛利率通常在 20-40%（a16z 2025 AI 基础设施报告）。优化推理成本的关键是提高 GPU 利用率和 batch 大小——vLLM 的 continuous batching 可将利用率从 30% 提升到 80%+。

## 核心概念

> **【中文解读】** 推理平台市场分为三大细分：(1) 自研芯片（Groq LPU、Cerebras WSE、SambaNova RDU）——以 5-10x 解码速度取胜但单价更高；(2) GPU 平台（Baseten、Together、Fireworks、Modal）——运行 NVIDIA GPU，介于原始 GPU 租赁和 hyperscaler 托管服务之间；(3) API 优先市场（Replicate、DeepInfra、OpenRouter）——强调快速上手和广度。

> **【拓展：自研推理芯片竞赛】** Groq 的 LPU（Language Processing Unit）在 Llama 70B 上可实现 300+ tokens/s，是 GPU 推理的 10x。Cerebras 的 CS-3 晶圆级引擎可达 2000+ tokens/s。但这些芯片的缺点是灵活性低——只能运行特定架构的模型。2025-2026 年自研推理芯片投资超过 $50B（CB Insights），核心赌注是推理需求将超过 GPU 供给。

### 三个细分

**自研芯片** —— Groq（LPU）、Cerebras（WSE）、SambaNova（RDU）。通常比同等模型上的 GPU 集群快 5-10x 的解码。每 token 价格更高（Groq 在 2025 年底约 $0.99/M on Llama-70B），但在延迟敏感用例中无与伦比。Groq 是语音代理和实时翻译的生产选择。

**GPU 平台** —— Baseten、Together、Fireworks、Modal、Anyscale。运行在 NVIDIA（H100、H200、2026 年的 B200）或有时是 AMD 上。介于"原始 GPU 租赁"（RunPod、Lambda）和"超大规模云托管服务"（Bedrock）之间的经济层。

**API 优先集市** —— Replicate、DeepInfra、OpenRouter、Fal。广泛目录，按预测或按秒付费，强调首次调用时间。

### Fireworks —— 延迟优化的 GPU 平台

- FireAttention 引擎（自研）；宣传为在等效配置上比 vLLM 延迟低 4x。
- 批量层约为无服务器费率的 50%，用于非交互工作负载。
- 微调模型以与基础模型相同的费率提供服务——与对 LoRA 收取溢价的供应商相比，这是真正的差异化。
- 2026 年中：从 2026 年 5 月 1 日起将按需 GPU 租赁提高 $1/小时。批量定价可协商。
- 财务信号：40 亿估值，每天处理 10T+ tokens。

### Together —— 广度优化

- 200+ 模型，包括上游发布后数天内的开源版本。
- 在等效 LLM 模型上比 Replicate 便宜 50-70%——"AI 原生云"定位是以量和目录取胜。
- 一个 API 中集成推理 + 微调 + 训练。

### Baseten —— 企业品质优化

- Truss 框架：模型打包，将依赖、密钥、服务配置放在一个清单中。
- GPU 范围从 T4 到 B200。按分钟计费，合理的冷启动缓解。
- SOC 2 Type II，HIPAA 就绪。常见金融科技和医疗选择。
- $50 亿估值，2026 年 1 月 E 轮（来自 CapitalG、IVP、NVIDIA 的 $3 亿）。

### Modal —— Python 原生优化

- 纯 Python 的基础设施即代码。用 `@modal.function(gpu="A100")` 装饰一个函数，一条命令部署。
- 按秒计费。预热后冷启动 2-4 秒；小模型不到 1 秒。
- $1.1 亿 B 轮估值（2025 年）。独立调查中开发者体验评分最高。

### Replicate —— 多模态广度

- 按预测付费。图像、视频和音频模型的默认平台。
- 集成生态系统（Zapier、Vercel、CMS 插件）。
- LLM 按 token 费率竞争力较差，但在多模态种类上胜出。

### Anyscale —— Ray 原生

- 基于 Ray 构建；RayTurbo 是 Anyscale 的专有推理引擎（与 vLLM 竞争）。
- 最适合推理步骤是更大图中一个节点的分布式 Python 工作负载。
- 托管 Ray 集群；与 Ray AIR 和 Ray Serve 紧密集成。

### 按 token vs 按分钟 —— 各自何时胜出

按 token 在工作负载延迟不敏感且突发时有意义——你只为使用的部分付费。按分钟在利用率高且可预测时有意义——一旦你饱和了 GPU，按分钟就胜过按 token。

粗略规则：对于专用 GPU 上超过约 30% 持续利用率的工作负载，按分钟（Baseten、Modal）开始胜过按 token（Fireworks、Together）。低于此值，按 token 胜出，因为你避免了为空闲付费。

> **【中文解读】** 定价模型选择的核心是利用率。按 token 计费适合突发、低频场景——只付实际使用量；按分钟计费适合持续高负载场景——当 GPU 利用率超过约 30% 时，按分钟通常更便宜。30% 是经验法则，实际交叉点取决于模型大小、batch 配置和具体平台定价。

> **【拓展：推理经济学趋势】** 2024-2026 年 LLM 推理价格下降了约 90%（ARK Invest 2025 报告）。GPT-4 级别模型的推理成本从 2023 年的 $30/M tokens 降到 2025 年的 $3/M tokens。趋势驱动因素包括：模型量化（INT8/INT4）、更好的 batch 调度、自研芯片竞争和开源推理引擎（vLLM/SGLang）的成熟。预计到 2027 年，同等质量的推理成本将再降 80%。

### 自研引擎是真正的护城河

vLLM 和 SGLang 之上的每个平台都声称有自研引擎。FireAttention、RayTurbo、Baseten 的推理栈。自研引擎的说法带有营销色彩——诚实的说法是 vLLM + SGLang 代表了大约 80% 的生产开源推理，平台层的差异化在于开发体验（DX）、归因和 SLA。

### 你应该记住的数字

- Fireworks GPU 租赁：2026 年 5 月 1 日起提价 $1/小时。
- Fireworks 声称：等效配置上比 vLLM 延迟低 4x。
- Together：LLM 上比 Replicate 便宜 50-70%。
- Baseten 估值：$50 亿（E 轮，2026 年 1 月，$3 亿轮）。
- Modal 估值：$1.1 亿（B 轮，2025 年）。
- 按分钟在超过约 30% 持续利用率时胜过按 token。

## 用框架实现

`code/main.py` 在定价模型上跨合成工作负载比较六个供应商。报告 $/天和有效 $/M tokens。运行它来找到按 token 和按分钟计费之间的盈亏平衡点。

> **【中文解读】** 实践部分通过模拟工作负载对比六个供应商的定价模型。关键输出是每天成本（$/day）和等效每百万 token 成本（$/M tokens），帮助你找到按 token 和按分钟计费的交叉点。

## 产出物

本课程产出 `outputs/skill-inference-platform-picker.md`。给定工作负载配置文件、SLA 和预算，选择主推理平台并命名备选。

> **【拓展：推理平台选型决策树】** 选型决策路径：(1) 是否需要 < 50ms TTFT？是 → Groq/Cerebras；(2) 是否需要自托管/合规？是 → Baseten/Modal；(3) 是否需要最大模型广度？是 → Together/OpenRouter；(4) 是否需要多媒体模型？是 → Replicate/Fal；(5) 默认 → Fireworks（延迟优化）或 Together（成本优化）。

## 练习题

1. 运行 `code/main.py`。Baseten（按分钟）在什么持续利用率下对 H100 上的 70B 模型胜过 Fireworks（按 token）？自己推导交叉点并与经验法则比较。
2. 你的产品提供图像生成 + 聊天 + 语音转文本。为每种模态选择平台并命名统一它们的网关模式。
3. Fireworks 将你主要模型的价格提高 $1/小时。如果 40% 的流量转移到批量层（50% 折扣），建模混合成本影响。
4. 受监管客户需要 SOC 2 Type II + HIPAA + 专用 GPU。哪三个平台可行，哪个在 FinOps 上胜出？
5. 比较 Llama 3.1 70B 在 Fireworks 无服务器、Together 按需、Baseten 专用和 Replicate API 上的每 1000 预测成本。每天 10 次预测时哪个最便宜？每天 10,000 次呢？

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Custom silicon | "非 GPU 芯片" | Groq LPU、Cerebras WSE、SambaNova RDU——为解码优化 |
| FireAttention | "Fireworks 引擎" | 自研注意力内核；宣传比 vLLM 延迟低 4x |
| Truss | "Baseten 格式" | 模型打包清单；依赖 + 密钥 + 服务配置 |
| Per-token | "API 定价" | 按消耗的 token 计费；不为空闲付费 |
| Per-minute | "专用定价" | 按挂钟 GPU 时间计费；高利用率时胜出 |
| Per-prediction | "Replicate 定价" | 按模型调用计费；图像/视频常见 |
| RayTurbo | "Anyscale 引擎" | 基于 Ray 的专有推理；在 Ray 集群上与 vLLM 竞争 |
| Batch tier | "50% 折扣" | 折扣费率的非交互队列；Fireworks、OpenAI 常见 |
| Fine-tuned at base rate | "Fireworks LoRA" | LoRA 服务请求按基础模型费率计费（差异化） |

## 延伸阅读

- [Fireworks 定价](https://fireworks.ai/pricing) — 按 token 费率、批量层、GPU 租赁。
- [Baseten 定价](https://www.baseten.co/pricing/) — 按分钟费率、承诺容量、企业层级。
- [Modal 定价](https://modal.com/pricing) — 按秒 GPU 费率和免费层。
- [Together AI 定价](https://www.together.ai/pricing) — 模型目录和按 token 费率。
- [Anyscale 定价](https://www.anyscale.com/pricing) — RayTurbo 和托管 Ray 定价。
- [Northflank — Fireworks AI 替代方案](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference) — 比较评估。
- [Infrabase — AI 推理 API 供应商 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) — 供应商格局。
