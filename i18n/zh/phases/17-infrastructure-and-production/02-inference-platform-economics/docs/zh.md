#                                                                                                                                                                                                                                                               

> 2026 年推断市场不再是GPU 租时间.它分为定制 (Groq,Cerebras,SambaNova),GPU 平台 (Baseten, Together, Fireworks, Modal) 和API 首选市场 (Replicate,DeepInfra).$1/hr per GPU on May 1, 2026, and $根据10T+代币/日的4B估值, 按数量驱动的模型工作.$300M Series E at $2026年1月5B. 竞争定位规则很简单:烟花优化延迟,一起优化目录宽度,Basen优化企业抛光,Modal优化Python-原生DX,复制优化多模达达,Anyscale优化分布式Python. 这一课给你一个可以交给创始人的矩阵.

> **【中文解读】**本节介绍了推理平台经济学LLM推理服务的成本结构,定价模型和经济学分析.
**Type:** Learn
**Languages:** Python (stdlib, toy per-call economics comparator)
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy per-call economics comparator) | **语言:** Python（标准库，每次调用经济性比较器）
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 01（托管 LLM 平台）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前请先掌握:阶段17·01(托管LLM 平台) 、阶段17·04(vLLM 内部) ⋅本节是2026 推理平台选型矩阵。
>  **【类比】**推理平台 = "AI 云服务商"──三类:(1) 定制芯片(Groq/Cerebras/SambaNova) = 专用CPU;(2) GPU 平台(Baseten/Together/Fireworks/Modal)=通用云;(3) API 市场(Replicate/DeepInfra)= 应用商店──选型口:Fireworks 低延迟、Together 模型多Baseten 企业级、Modal多原生、Replicate模态广、Anyscale 分布式 Python──

## 学习目标

- 列出三个市场细分 (定制,GPU平台,API首) 并将每个供应商映射到一个细分.
  中文翻译:说出三个市场细分(自研芯片、GPU 平台、API 优先),并将每个供应商映射到应对细分──
- 解释为什么"每代币"API定价模型向服务引擎的成本曲线压缩而不是硬件的成本曲线.
  中文翻译:解释为什么"按代币"API定价模型缩小到服务引擎的成本曲线而不是硬件成本.
- 计算每次请求的有效成本,至少在三个供应商中计算,并解释每分钟 (Baseten, Modal) 什么时候超过每代币.
  中文翻译:计算至少三个供应商的每次请求有效成本,并解释按分钟 (何时优于按代币).
- 确定哪个平台是给定的工作负载的默认正确的 (无服务器爆发,稳定高吞吐量,精细调节的变体,多模式).
  中文翻译:识别哪个平台是给定工作负载的正确默认选择 ((无服务器突发、稳定高吞吐、微调变体、多模态) ⋅

## 问题 问题引入

您评估了管理的超级级平台.您决定需要一个更窄,更快的供应商. 烟花为延迟, 合并为宽度, 贝塞顿为一个精细调节的定制模型. 现在您有六个真正的选择, 价格页面不排列. 烟花显示.$/M tokens; Baseten shows $演出节目$/second; Replicate shows $没有模拟工作负载,你不能把它们相比.

> 你评估托管云平台后,决定需要一个更专注的,更快的供应商火灾工作 追求延迟,一起追求广度,Baseten 追求微调自定义模型――现在你有六个真实选择,但定价页面无法直接对比――火灾工作 显示$/M tokens；Baseten 显示 $显示器$/秒；Replicate 显示 $预测──不建模工作负载就无法直接比较──

更糟糕的是,每个价格表格背后的商业模式是不同的. 烟花在共享GPU上运行了自己的定制引擎 (FireAttention);每代币的速度反映了它们的利用曲线. 基给你提供了Trus+专用GPU;每分钟反映了独占性. 模特是真实的 Python 无服务器 每秒的发票,低于秒的冷开始. 产出相同 (LLM响应),三个不同的成本函数.

> 更糟糕的是,每个定价页面背后的商业模式不同――Fireworks 在共享GPU 上运行自研引擎(FireAttention);按代币 费率反映其利用率曲线――Baseten 提供Truss + 专用GPU;按分钟反映独占性――Modal 是真正的Python 无服务器按秒计费,亚秒级冷启动――同样的输出(LLM响应),三种不同的成本函数――

这一课模拟了六个,告诉你每一个人当胜利.

> 这里有六个平台,告诉你每一个人在什么时候胜出.

> **【中文解读】**推理平台市场的核心难题是定价模型不统一――按代币 计费 火车/一起) 按分钟计费 火车) 按秒计费 模特) 按预测费 复制) 相同的LLM 响应,背后是完全不同的成本函数――不能只看单价,必须根据工作负载特征构建模才能做正确的选择――

> **【拓展：LLM 推理成本构成】**推理LLM的成本主要由GPU租(H100 约$2-3/hr）、电力（约 $推理平台的毛利率通常在20-40%的水平上. 推理平台的毛利率通常在20-40%的水平上. 推理成本的关键是提高GPU利用率和批量大小vLLM的连续批量.

## 概念的核心概念

> **【中文解读】**推理平台市场分为三大细分:(1) 自研芯片(Groq LPU、Cerebras WSE、SambaNova RDU) 以5-10倍解码速度取胜但单价更高;(2) GPU 平台(Baseten、Together、Fireworks、Modal) 运行NVIDIA GPU,介于原始 GPU 租和超级级级级级级级托管服务之间;(3) API 优先市场(复制、深度信息、开路由器) 强调快速手机和广度.

> **【拓展：自研推理芯片竞赛】**格洛克的LPU(语言处理单元) 在Llama 70B上可实现300多个代币/s,是GPU 推理的10x──Cerebras的CS-3晶圆级引擎可达2000多个代币/s──但这些芯片的缺点是灵活性低只能运行特定架构的模型──2025-2026年自研推理芯片投资超过50亿美元──CB见解),核心注是推理需求将超过供应.

### 三个部分

**Custom silicon**Groq (LPU),Cerebras (WSE),SambaNova (RDU).通常比 GPU 基于同一模型的集群快 5-10倍解码.高的每代币价格 (Groq在 Llama-70B 上是2025年底的 ~ 0.99 美元/M),但对于延迟敏感的使用案例来说是不可击败的.Groq是语音代理和实时翻译的生产选择.

> **自研芯片** Groq(LPU)、Cerebras(WSE)、SambaNova(RDU)。通常比模型的GPU 集群解码速度快 5-10倍──按代币价格更高(Groq 2025年末在Llama-70B上升约0.99美元/M),但对延迟敏感的使用例无可匹敌──Groq是语音代理和实时翻译的生产选择──

**GPU platforms**Baseten,Together, Fireworks,Modal,Anyscale.运行在NVIDIA (H100,H200,B200在2026年) 或有时AMD. "原料GPU租" (RunPod,Lambda) 和"超级级管理服务" (Bedrock) 之间的经济层.

> **GPU 平台** 基板、一起、火灾、Modal、Anyscale──运行在NVIDIA(2026年的H100、H200、B200) 或有时是AMD 上部──"原始GPU租"(RunPod、Lambda) 和"云托管服务"(Bedrock) 之间的经济层──

**API-first marketplaces**复制,深度信息,开路由器,FAL. 广的目录,预测或秒支付,强调时间到第一次通话.

> **API 优先市场** 复制、深度信息、开路由器、落──广泛目录,按预测或按秒付费,强调首次调用速度──

### 烟花 延迟优化的GPU平台

- 根据标准,在同等配置上,该系统的延迟速度低于vLLM的4倍.
  中文翻译:FireAttention 引擎(自研);宣传为比等效配置的vLLM 延迟低 4倍。
- 对于非互动工作负载,批量级为50%的无服务器率.
  中文翻译:批量级为无服务器费率的50%用于非交互工作负载.
- 精细调节的模型与基本模型相同的速度提供了真正的区别,而不是为您的LoRA收取溢价的提供商.
  中文翻译:微调模型按基础模型费率服务与对LoRA收取溢价的供应商相比是真正的差异化因素
- 2026年中期:按需加增1美元1小时的GPU租金,从2026年5月1日起.
  中文翻译:2026年中:自 5 月 1 日起按量GPU 租价格 $1/小时──大批量价格可协商──
- 金融信号:400亿美元的估值,每天处理10万多个代币.
  中文翻译:财务信号:$4B 估值,每天处理10T+代币.

###  宽度优化

- 超过200个模型,包括在上游发布后几天内发布的开源版本.
  中文翻译:200+ 模型,包括上游发布后几天内开源版本──
- "AI原生云"定位量和目录.
  中文翻译:比复制 在等效 LLM 模型上便宜50-70%.
- 推理+细调+训练在一个API中.
  中文翻译:推理 + 微调 + 训练在一个API 中。

###  企业-波兰-优化

- 托拉斯框架:包含依赖性,秘密的模型包装,服务配置在一个表格中.
  中文翻译:信任框架:模型打包,包含依赖,密钥,服务配置在一个清单中.
- 按分钟计费,可缓解冷启动.
  中文翻译:GPU 范围从T4到B200──按分钟计费,有合理的冷启动缓解──
- 标准化, HIPAA准备好,一般的金融科技和医疗保健选择.
  中文翻译:SOC 2类型II、HIPAA 就绪──常见金融科技和医疗保健选择──
- $5B valuation, January 2026 Series E ($公司的资本公司,IVP,NVIDIA.
  翻译: 中文$5B 估值，2026 年 1 月 E 轮融资（来自 CapitalG、IVP、NVIDIA 的 $水,水

### 模拟  字符串原生优化

- 纯Python中的基础设施作为代码.`@modal.function(gpu="A100")`并且只有一次命令.
  中文翻译:纯Python的基础设施即代码.`@modal.function(gpu="A100")`装饰函数,一条命令部署――
- 低温为2~4秒,小型车型则<1秒.
  中文翻译:按秒计费――预热后冷启动 2-4 秒;小模型 <1 秒――
- $87M Series B at $1.1B估值 (2025). 在独立调查中,开发者经验得分最强.
  中文翻译:B轮融资$87M，估值 $独立调查中开发者体验评分最高──

### 复制 多模宽度

- 预测费用,是图像,视频和音频模型的默认平台.
  中文翻译:按预测付费;;图像、视频和音频模型的默认平台。
- 集成生态系统 (Zapier,Vercel,CMS插件).
  中文翻译:集成生态系统(扎皮尔、维尔塞尔、CMS 插件) ⋅
- 在每代币的利率上,LLM较少竞争力,但在多元化品种上获胜.
  中文翻译:LLM 按代币 费率竞争力较弱,但在多模态多样性上胜利.

### 任何规模的射线原生

- 基于Ray;RayTurbo是Anyscale专有推断引擎 (与vLLM竞争).
  中文翻译:基于Ray 构建;RayTurbo 是任何规模的专专注推理引擎(与vLLM 竞争) 。
- 最适合分布式Python工作负载,其中推断步骤是一个更大的图中的节点.
  中文翻译:最适合推理步骤是一个节点的分布式Python工作负载.
- 管理了雷集群,与雷空气和雷服务密切集成.
  中文翻译:托管雷集群;与雷空和雷服务紧密集成。

### 每个奖金时,每分钟的比分

每个代币是有意义的,当工作负载是延迟不敏感和爆你只支付你使用的东西. 每分钟是有意义的,当利用率是高的和可预测的,你打败每代币一旦你和GPU.

> 当工作负载对延迟不敏感且突发时,按代币计费更合理你只支付实际使用量――当利用率高且可预测时,按分钟计费更合理一旦GPU 和就比按代币优――

严格规则:在专用GPU持续使用的工作负载超过30%时,每分钟 (Baseten,Modal) 开始超过每代币 (Fireworks, Together).在此下,每代币获胜,因为你避免为空付款.

> 粗略规则:对于专用GPU持续利用率超过30%的工作负载,按分钟 (分钟) 按Basen、Modal) 开始优于按代币 (分钟) 按Fireworks、一起) ⋅低于此值时,按代币 (分钟) 获胜,因为避免为空付费──

> **【中文解读】**定价模型选择的核心是利用率.按代币 计费适合突发,低频场景只支付实际使用量.按分钟计费适合持续高负载场景当GPU利用率超过30%时,按分钟通常更便宜.

> **【拓展：推理经济学趋势】**2024-2026年LLM推理价格下降了约90% ((ARK Invest 2025 报告) ・GPT-4级模型推理成本从2023年起$30/M tokens 降到 2025 年的 $预计到2027年,同等质量的推理成本将再次下降80%──

### 定制发动机是真正的沟

根据VLLM和SGLang的定义,VLLM+SGLang的产品均占产品开源推理的80%左右,平台层的区别是DX,归因和SLA.

> 每个超越VLLM和SGLang的平台都声称有自研引擎――FireAttention、RayTurbo、Baseten的推理――自研引擎声明有营销成分诚实说法是VLLM+SGLang占生产环境开源推理的80%左右,平台层的差异因素是开发者体验、归因和SLA――

### 你应该记住的数字

- 烟花GPU租: $1/小时加息,从2026年5月1日起.
  中文翻译:火灾GPU租:自2026年 5月1日起价$1/小时。
- 烟花声称:在相当配置上,延迟比vLLM低4倍.
  中文翻译:火灾 声称:等效配置下比vLLM 延迟低 4倍──
- 合计:比在 LLM上复制品便宜50-70%.
  中文翻译:一起:LLM 上比复制便宜 50-70%──
- 基质估值: $5B (Series E, Jan 2026, $周围的300米.
  中文翻译:Baseten 估值:$5B（E 轮，2026 年 1 月，$轮次300万
- 资产估值:1.1亿美元 (B系列,2025年).
  中文翻译:模型估值:$1.1B(B轮,2025)。
- 每分钟的比率超过持续使用率的30%
  中文翻译:持续利用率超过约30% 时分钟优于代币.

## 用它实现框架
```figure
cost-per-token
```

## 用它

`code/main.py`报告 报告 报告 报告 报告 报告 报告 报告 报告 报告 报告$/day and effective $运行它,以找到每代币和每分钟之间的平衡.

> `code/main.py`报告中对六家供应商的定价模型进行了比较.$/天和等效 $运行它按代币找到和按分钟的亏平衡点.

> **【中文解读】**实践部分通过模拟工作负载对比六家供应商的定价模型――关键输出是每天成本$/day）和等效每百万 token 成本（$根据标志和分钟计费的交叉点.

## 运送它.

这一课产生了`outputs/skill-inference-platform-picker.md`根据工作负载配置,SLA和预算,选择主要推断平台并命名下位.

> 本课产出发 `outputs/skill-inference-platform-picker.md`△给定工作负载配置、SLA 和预算,选择主要推理平台并命名备选──

> **【拓展：推理平台选型决策树】**选型决策路径:(1) 是否需要 <50ms TTFT?是 → Groq/Cerebras;(2) 是否需要自托管/合规?是 → Baseten/Modal;(3) 是否需要最大模型广度?是 → Together/OpenRouter;(4) 是否需要多媒体模型?是 → 复制/错误;(5) 默认 → 烟花火works(延迟优化) 或 Together(成本优化)

## 练习题

1. 跑步`code/main.py`根据"H100"的70B模型,巴塞顿 (每分钟) 比"烟花" (每代币) 更多.
   中文翻译:运行 `code/main.py`△BASETEN (按分钟) 在什么持续利用率下对一台H100上70B模型优于烟花?自行推导交叉点并与经验法则比较──
2. 您的产品提供图像生成,聊天,语音与文字,
   中文翻译:你的产品提供图像生成,聊天和语音转文字.
3. 假如您的 40% 的流量转移到批量级 (50%折扣).
   中文翻译:火灾工程将主要模型价$1/小时──如果40%的流量转移到批量层次价半价,建模混合成本影响──
4. 监管的客户需要SOC 2类型II+HIPAA+专用GPU.哪三个平台是可行的,哪个在FinOps中赢得胜利?
   中文翻译:一个受监管客户需要SOC 2类 II+HIPAA+专用GPU──哪三个平台可行,哪个在FinOps上获胜?
5. 根据Llama 3.1 70B的1000个预测, 价格比较于火箭无服务器, 随需, 专用Baseten和复制API.
   中文翻译:比较Llama 3.1 70B 在烟花无服务器、一起按量、Baseten 专用和复制API 上每1000次预测的成本──每天10次预测哪个最便宜?每天10,000次呢?

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Fireworks Pricing](https://fireworks.ai/pricing)每代币的价格,批次级别,GPU租.
- [Baseten Pricing](https://www.baseten.co/pricing/)每分钟的利率,承诺能力,企业层次.
- [Modal Pricing](https://modal.com/pricing)每秒GPU速度和免费级别.
- [Together AI Pricing](https://www.together.ai/pricing)模型目录和每代币价格.
- [Anyscale Pricing](https://www.anyscale.com/pricing)雷土博和雷管理价格.
- [Northflank — Fireworks AI Alternatives](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference)比较评估.
- [Infrabase — AI Inference API Providers 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared)供应商景观.
