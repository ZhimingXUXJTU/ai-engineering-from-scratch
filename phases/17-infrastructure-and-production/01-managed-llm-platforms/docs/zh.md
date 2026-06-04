# 托管 LLM 平台 — Bedrock、Vertex AI、Azure OpenAI | 平台 托管 OpenAI LLM

> 三大超大规模云厂商，三种截然不同的策略。AWS Bedrock 是一个模型集市——Claude、Llama、Titan、Stability、Cohere 背后统一 API。Azure OpenAI 是与 OpenAI 的独家合作，加上预置吞吐量单位（PTU）用于专用容量。Vertex AI 以 Gemini 为优先，在长上下文和多模态方面拥有最佳表现。2026 年 Artificial Analysis 测量 Azure OpenAI 在 Llama 3.1 405B 等效模型上的中位数延迟约为 50ms，Bedrock 约为 75ms——PTU 解释了这个差距，因为专用容量优于共享按需容量。决策规则不是"哪个最快"，而是"哪个模型目录和 FinOps 表面匹配我的产品"。本课程教你在书面权衡的基础上做出选择，而不是凭感觉。

> **【中文解读】** 本节介绍了托管 LLM 平台——OpenAI、Anthropic、Google 等提供的模型服务平台的选型和对比。


**类型：** 学习
**语言：** Python（标准库，模拟成本与延迟比较器）
**前置条件：** Phase 11（LLM 工程），Phase 13（工具与协议）
**时间：** 约 60 分钟

## 学习目标

- 说出三种平台策略（集市 vs 独家 vs Gemini 优先），并将每种匹配到产品用例。
- 解释 Azure OpenAI 中预置吞吐量单位（PTU）的价值，以及为什么按需 Bedrock 在 405B 规模上通常慢约 25ms。
- 绘制每个平台的 FinOps 归因表面（Bedrock 应用推理配置文件 vs Vertex 按团队项目 vs Azure 范围 + PTU 预留）。
- 写下"双供应商最低"策略，并解释为什么单供应商锁定是 2026 年的昂贵错误。

## 问题引入

你选择了 Claude 3.7 Sonnet 作为产品模型。现在你需要部署它。你可以直接调用 Anthropic API，也可以通过 AWS Bedrock 调用，或者通过网关调用。直接 API 最简单；Bedrock 增加了 BAA、VPC 端点、IAM 和 CloudWatch 归因。网关增加了故障转移、统一计费和跨供应商速率限制。

更深层次的问题是模型目录。如果你的产品同时需要 Claude、Llama 和 Gemini，你无法从一个地方购买所有模型，除非那个地方同时是 Bedrock + Vertex + Azure OpenAI。超大规模云厂商不可互换——它们各自在模型层的归属上下了不同的赌注。

本课程映射了三种赌注、延迟差距、FinOps 差距和锁定风险。

> **【中文解读】** 选定 LLM 后，"在哪里部署"是一个基础设施级别的决策。直接调用 API 最简单，但缺乏企业级控制；通过云平台（Bedrock/Vertex/Azure）调用增加了合规、审计能力；通过网关调用则获得多供应商容灾和统一计费。核心矛盾在于：三大云厂商的模型目录不重叠，无法在单一平台获取所有前沿模型。

> **【拓展：LLM 部署模式】** 2024-2026 年 LLM 服务部署模式经历了从 "直接 API" → "云平台托管" → "AI 网关统一路由" 的演进。OpenRouter、Portkey、LiteLLM 等 AI 网关项目在 2025 年获得大量采用，核心价值是在多供应商之间提供统一接口、自动 failover 和成本优化。企业级部署中，约 60% 已采用网关模式（Gartner 2025 AI 基础设施报告）。

## 核心概念

> **【中文解读】** 三大云厂商的 LLM 平台策略截然不同：AWS Bedrock 是"模型集市"，聚合多家供应商；Azure OpenAI 是"独家合作"，专供 OpenAI 模型；Vertex AI 是"Gemini 优先"，以超长上下文和多媒体能力为卖点。理解这些策略差异是做出正确选型的基础。

> **【拓展：全球 LLM 云平台格局】** 除三大 hyperscaler 外，2026 年值得关注的还有：Cloudflare Workers AI（边缘推理）、Together AI（开源模型推理平台，$0.18/M tokens for Llama 3.1 70B）、Groq（LPU 推理引擎，TTFT < 20ms）、Cerebras（CS-3 wafer-scale 推理，2000+ tokens/s）。国内有百度千帆、阿里百炼、火山方舟等，但模型目录与国际平台不互通。

### 三种策略

**AWS Bedrock** —— 集市模式。Claude（Anthropic）、Llama（Meta）、Titan（AWS 自研）、Stability（图像）、Cohere（嵌入）、Mistral，以及图像和嵌入子目录。一个 API，一个 IAM 表面，一个 CloudWatch 导出。Bedrock 的赌注是客户更想要可选择性而非单一模型。

**Azure OpenAI** —— 独家合作。你可以在 Azure 数据中心获得 GPT-4 / 4o / 5 / o 系列、DALL·E、Whisper 和 OpenAI 模型的微调。"Azure OpenAI 服务"目录中没有非 OpenAI 模型——那些在 Azure AI Foundry（独立产品）中。Azure 的赌注是 OpenAI 始终处于前沿，客户希望对这一特定关系进行企业级控制。

**Vertex AI** —— Gemini 优先，其他其次。Gemini 1.5 / 2.0 / 2.5 Flash 和 Pro，加上 Model Garden（第三方）。Vertex 的赌注是多模态长上下文——1M token 的 Gemini 上下文是差异化优势。

### 规模上的延迟差距

Artificial Analysis 运行持续基准测试。在等效的 Llama 3.1 405B 部署（共享按需）上，Azure OpenAI 中位数首 token 延迟约为 50ms；Bedrock 约为 75ms。这个差距不是 AWS 的失败——而是容量模型的差异。Azure 销售 PTU（预置吞吐量单位），为你的租户预留 GPU 容量。Bedrock 的等效产品（Provisioned Throughput）存在但每单位每小时约 $21 起，大多数客户使用共享按需模式。

按需共享容量与所有其他客户的流量竞争。专用容量不会。如果你的产品 SLA 是 TTFT < 100ms at P99，你要么在 Azure 上购买 PTU，要么购买 Bedrock Provisioned Throughput，要么接受默认方差。

> **【中文解读】** 延迟差距的本质是"容量模型"差异。共享按量部署中，你的请求与所有其他客户的流量竞争 GPU 资源；专用容量（PTU）则预留了独占的 GPU。Azure PTU 在 40-60% 利用率时可节省高达 70% 成本，但空闲时仍然付费。Bedrock 的按量模式 TTFT 中位数约 75ms，Azure PTU 约 50ms，25ms 差距在高频交互场景中会被用户感知。

### 预置吞吐量经济学

Azure PTU：预留的推理计算块。与按需相比，可预测工作负载下节省高达 70%。无论流量如何，每小时固定成本——空闲时也要为预留付费。盈亏平衡点通常在 40-60% 持续利用率左右。

Bedrock Provisioned Throughput：每小时 $21-$50，取决于模型和区域。类似的数学——盈亏平衡在峰值利用率的一半左右。需要月度承诺。

Vertex 预置容量按 Gemini SKU 销售；定价因模型和区域而异，公开宣传较少。

### FinOps 表面 —— 真正的差异化因素

**Bedrock 应用推理配置文件** 是集市中最精细的归因。用 `team`、`product`、`feature` 标记配置文件；将所有模型调用通过它路由；CloudWatch 按配置文件拆分成本，无需后处理。2025 年添加，仍然是超大规模云厂商中原生最精细的。

**Vertex** 归因是按团队项目加无处不在的标签。你将每个团队建模为一个 GCP 项目，在每个资源上放置标签，使用 BigQuery 计费导出 + DataStudio 进行汇总。工作更多，但 BigQuery 让你对成本数据进行任意 SQL 查询。

**Azure** 依赖订阅/资源组范围加标签，PTU 预留作为一等成本对象。标签从资源组继承，而不是从请求继承，因此按请求归因需要 Application Insights 自定义指标或在网关上标记请求头。

模式：Bedrock 原生最精细，Vertex 通过 BigQuery 最灵活，Azure 除非你自行埋点最不透明。

> **【中文解读】** FinOps（云财务运营）是 LLM 基础设施中最被低估的维度。Bedrock 的 Application Inference Profiles 是目前最精细的原生成本归因方案——按团队、产品、功能标签拆分调用成本；Vertex 通过 BigQuery 导出提供最大灵活性，可用 SQL 做任意聚合；Azure 最为不透明，除非你自行用 Application Insights 埋点。选择平台时，FinOps 能力与延迟、价格同等重要。

> **【拓展：LLM FinOps 实践】** 企业 LLM 支出在 2025 年平均增长了 300%（Flexera 2025 云状态报告）。常见 FinOps 策略包括：(1) 按 token 消耗设置团队预算告警；(2) 使用缓存层（Semantic Cache）减少重复调用约 30-40%；(3) 模型路由——简单任务用小模型、复杂任务用大模型，可节省 50%+ 成本；(4) 批量 API 在非实时场景可降低 50% 价格。

### 锁定是 2026 年的风险

单一超大规模云厂商的承诺在一个模型主导时没问题。2026 年前沿模型每月都在变化——一季度是 Claude 3.7，下一季度是 Gemini 2.5，再下一季度是 GPT-5。锁定一个平台意味着错过了 2/3 的前沿能力。

成功的团队采用的模式：任何产品关键 LLM 调用的双供应商最低策略。Bedrock 加 Azure OpenAI 是最常见的组合——一个提供 Claude，另一个提供 GPT，在两者之间故障转移，同一网关。成本增加微不足道，因为网关路由最优；在宕机期间的可用性提升（如 Azure OpenAI 2025 年 1 月事件、AWS us-east-1 宕机）是决定性的。

> **【中文解读】** 2026 年的最大基础设施风险是供应商锁定。前沿模型每季度都在更替——Q1 用 Claude 3.7，Q2 用 Gemini 2.5，Q3 用 GPT-5。锁定单一平台意味着错过 2/3 的前沿能力。最佳实践是"双供应商最低"策略：Bedrock + Azure OpenAI 是最常见组合，通过网关统一路由，成本增加可忽略，但在故障时的可用性提升显著。

> **【拓展：云厂商宕机事件】** 2025 年 1 月 Azure OpenAI 经历了长达数小时的全局性故障，影响所有依赖单一 Azure 的 ChatGPT 企业客户。同年 AWS us-east-1 区域也发生严重故障。多供应商策略在这些事件中证明了其价值：当一家宕机时，网关自动将流量切换到另一家，实现零感知故障转移。Cloudflare 的 2025 年可用性报告显示，多供应商架构的 LLM 服务可用性可达 99.99%，而单供应商通常为 99.9%。

### 数据驻留、BAA 和受监管行业

Bedrock：大多数区域提供 BAA；VPC 端点；防护栏。常见金融科技默认选择。
Azure OpenAI：HIPAA、SOC 2、ISO 27001；EU 数据驻留；企业受监管默认选择。
Vertex：HIPAA、GDPR、按区域数据驻留；Google Cloud 合规栈。

三者都满足基本检查清单。差异在于数据保留策略、日志处理方式，以及滥用监控是否读取你的流量（大多数默认 opt-in；企业可选择 opt-out）。

### 你应该记住的数字

- Azure OpenAI 在 Llama 3.1 405B 等效模型上的中位数 TTFT：约 50ms（使用 PTU）。
- Bedrock 按需中位数 TTFT：约 75ms。
- Bedrock Provisioned Throughput：$21-$50/小时每单位。
- Azure PTU 盈亏平衡：约 40-60% 持续利用率。
- PTU 相比按需在高利用率时的节省：高达 70%。

## 用框架实现

`code/main.py` 在合成工作负载上比较三个平台——它建模按需 vs PTU 经济学、TTFT 方差和成本归因保真度。运行它来看看 PTU 在什么时候划算，以及集市的模型广度何时胜过 TTFT 差距。

> **【中文解读】** 实践部分通过模拟工作负载对比三大平台。关键指标包括：TTFT（首 token 延迟）、吞吐量、每百万 token 成本。通过调整利用率参数，可以直观看到 PTU 在什么负载水平下比按量计费更划算。

## 产出物

本课程产出 `outputs/skill-managed-platform-picker.md`。给定工作负载配置文件（所需模型、TTFT SLA、日流量、合规要求），它推荐主平台、备选方案和 FinOps 埋点计划。

> **【拓展：生产环境平台选型 Checklist】** 生产环境 LLM 平台选型应考虑：(1) 模型目录是否覆盖所需模型；(2) 延迟 SLA 是否满足用户体验要求（对话 < 200ms TTFT，批处理无严格要求）；(3) 合规认证（HIPAA/SOC2/ISO27001）；(4) 数据驻留（GDPR 要求 EU 区域存储）；(5) 成本归因粒度（能否按团队/产品拆分账单）；(6) 容灾方案（多区域/多供应商 failover）。

## 练习题

1. 运行 `code/main.py`。Azure PTU 在什么持续利用率下对 70B 级别模型比按需更便宜？计算盈亏平衡点并与宣传的 40-60% 范围进行比较。
2. 你的产品需要 Claude 3.7 Sonnet 和 GPT-4o。设计双供应商部署——哪个去哪个超大规模云厂商，前面放什么网关，故障转移策略是什么？
3. 受监管的医疗保健客户需要 BAA、US-East 数据驻留和低于 100ms 的 P99 TTFT。选择一个平台并用三个具体功能来论证。
4. 你发现 Bedrock 本月账单上涨了 4 倍，但流量没有变化。没有 Application Inference Profiles 时，你如何找到罪魁祸首？有了配置文件，需要多长时间？
5. 阅读 Azure OpenAI 和 Bedrock 定价页面。对于每月 1 亿 token 的 Claude 工作负载，哪个更便宜——直接 Anthropic API、Bedrock 按需还是 Bedrock Provisioned Throughput？

## 术语速查表

| 术语 | 人们常说的 | 实际含义 | 英文原文 |
|------|-----------|---------|---------|
| Bedrock | "AWS LLM 服务" | 跨 Claude、Llama、Titan、Mistral、Cohere 的模型集市 | Model marketplace across Claude, Llama, Titan, Mistral, Cohere |
| Azure OpenAI | "Azure 的 ChatGPT" | Azure 数据中心中的独家 OpenAI 模型，带企业级控制 | Exclusive OpenAI models in Azure datacenters with enterprise controls |
| Vertex AI | "Google 的 LLM" | Gemini 优先平台，Model Garden 提供第三方模型 | Gemini-first platform with Model Garden for third-party models |
| PTU | "专用容量" | 预置吞吐量单位——预留推理 GPU，按小时定价 | Provisioned Throughput Unit — reserved inference GPUs, priced per hour |
| Application Inference Profile | "Bedrock 标签" | 按产品的成本/使用配置文件，带标签，CloudWatch 原生 | Per-product cost/usage profile with tags, CloudWatch-native |
| Model Garden | "Vertex 目录" | Vertex AI 的第三方模型部分，独立于 Gemini | Vertex AI's third-party model section, separate from Gemini |
| Two-provider minimum | "LLM 冗余" | 每个关键 LLM 调用跨 ≥2 个超大规模云厂商运行的策略 | Policy of running every critical LLM path across ≥2 hyperscalers |
| BAA | "HIPAA 文件" | 业务关联协议；PHI 必需；三者都提供 | Business Associate Agreement; required for PHI; provided by all three |
| Abuse monitoring | "日志监控器" | 供应商端的 prompt/输出安全扫描；企业可选择 opt-out | Provider-side safety scan on prompts/outputs; opt-out in enterprise |

## 延伸阅读

- [AWS Bedrock 定价](https://aws.amazon.com/bedrock/pricing/) — 权威费率卡和 Provisioned Throughput 定价。
- [Azure OpenAI 服务定价](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) — PTU 经济学和费率卡。
- [Vertex AI 生成式 AI 定价](https://cloud.google.com/vertex-ai/generative-ai/pricing) — Gemini 层级和 Model Garden 附加费。
- [Artificial Analysis LLM 排行榜](https://artificialanalysis.ai/) — 跨供应商的持续延迟和吞吐基准测试。
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO 指南 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) — 企业决策框架。
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) — 归因机制并排对比。
