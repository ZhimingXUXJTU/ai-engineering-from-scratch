#  简单的门,Portkey,Kong AI门,双结

> 应用程序和模型提供商之间设有网关.核心功能是提供商路由,倒退,重试,速度限制,秘密引用,可观察性,防护线. 2026 年市场分区:**LiteLLM**是与100多个提供商兼容的MIT OSS,与OpenAI兼容,但分解在2000 RPS左右 (8 GB 内存,发表基准中的级故障);最适合Python, <500 RPS,开发/原型设计. **Portkey**通过安装安装的控制平面 (防护屏, PII编辑, jailbreak检测,审计轨迹), 进入 Apache 2.0 开源3月2026年, 20-40 ms延迟过head,$49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $企业适合,如果你已经在Kong上. **Bifrost**自动重试,可配置的后退,在OpenAI429上回到人类.**Cloudflare / Vercel AI Gateways**管理,零操作,基本重试.数据居住驱动自主主机决定;Portkey和Kong坐在中间,OSS+可选管理.

> **【中文解读】**本节介绍了AI 网关LLM 请求路由,负载平衡和安全网关.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)

>  **【前置】**技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术
>  **【类比】**关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关键: 关
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 列出六个核心门口特征 (路由,倒退,重试,速度限制,秘密,可观察性,护).
  中文翻译:列举六个核心网关功能 (路由,回退,重试,速度限制,密钥管理,可观测性)
- 绘制四个2026年门户 (LiteLLM,Portkey,Kong AI,Bifrost) 进行扩展天花板和使用情况.
  中文翻译:将四个2026年网关(LiteLLM、Portkey、Kong AI、Bifrost)映射到规模上限和使用例──
- 引用康格基准则 (228%对Portkey,859%对 LiteLLM) 并解释为什么对500 RPS而言是重要的.
  中文翻译:引用 Kong 基准测试(228%对 Portkey,859%对 LiteLLM)并解释为什么在 >500 RPS 时重要.
- 选择自主托管与管理, 根据数据居住和运营预算.
  中文翻译:给定数据驻留和运维预算,选择自托管vs托管──

## 问题 问题引入

> **【中文解读】**网络关位于应用和模型提供商之间,解决核心问题是多供应商统一管理.产品同时调用OpenAI、人类和自托管Llama,每个提供商都有不同的SDK、错误模型、速度限制和认证方案.

> **【拓展：2026 年 AI 网关市场】**2026年AI网关市场的四大玩家:(1) LiteLLMMIT 开源,100+ 提供商,但在2000年RPS 时崩8GB内存);(2) Portkey2026年3月开源Apache 2.0,控制面定位(守护者、PII 脱敏、越狱检查、审计追踪),20-40ms 延迟开销;(3) Kong AI Gateway基于成熟的API网关产品,Kong 基准测试显示了自己的Portkey 快 228%、比 LiteLLM 快 859%;(4) Cloudflare/Vercel AI Gateway 托管、零运维、边缘部署.

您的产品叫做OpenAI,Anthropic,以及一个自主托管的Llama.每个提供商都有不同的SDK,错误模型,利率限制和 auth方案.您希望出现故障 (如果OpenAI 429s,试试用Anthropic),一个单个凭证存储,统一的可观察性,每个租户的利率限制.

通过重新发明应用程序层,将每个服务与每个提供商结合起来.一个门户层将其结合成一个过程,使用一个API (通常是OpenAI兼容的) 来向提供商提供.

## 概念的核心概念

### 六个核心特征

1. **Provider routing**OpenAI,人类,双胞胎,自主托管等在一个API后面.
2. **Fallback**在429,5xx或质量失败,再试在其他地方.
3. **Retries**指数式回复,有限的尝试.
4. **Rate limits**每租户,每钥匙,每模型.
5. **Secret references**在运行时间 (从未在应用程序中) 提取信誉信息.
6. **Observability** OTel + GenAI属性 (阶段17 · 13) +成本归因.
7. **Guardrails** 删除个人信息,检测 jailbreak,允许的话题过器.

### 微LLM  MIT OSS,Python

- 提供商,与OpenAI兼容,路由器配置,倒退,基本可观测性.
- 根据康格的标准, 损失约2000 RPS; 8 GB 内存足迹, 持续负载下发生断故障.
- 最好的适应:Python应用程序, <500 RPS,开发/阶段化网关,实验路由.
- 成本:OSS的价格为0美元;云免费层次存在.

### 门键 控制平面定位

- 根据2026年3月的 Apache 2.0 OSS, 监护轨道, PII编辑, 监狱突破检测, 审计轨道.
- 要求每次延迟时间 20-40 ms.
- 产品层面的每月49美元,
- 最适合:需要防护+可观测性捆绑的监管产业.

###         

- 基于 Kong Gateway (成熟的API门户产品,lua+OpenResty) 构建.
- 康格公司对12个CPU相当的基准:228%比Portkey快,859%比LiteLLM快.
- 价格:每月100美元,最高5美元,
- 适合最好的:已经在 Kong 上; > 1000 RPS;愿意许可.

### 双 (最大AI)

- 通过可配置的备份系统进行自动复试.
- 翻译为"人类"的 OpenAI 429 是一个法典的食谱.
- 新入门者,商业.

### 云飞云AI网关 / 维尔塞尔AI网关

- 经过了,零操作,基本的重试和可观察性.
- 最好的适应:在Cloudflare/Vercel上使用边缘服务的JavaScript应用程序.
- 限制在防护轨和速率限制上与 Kong/Portkey相比.

### 自主主机和管理

> **【中文解读】**自托管与托管的决策驱动因素是数据驻留――医疗和金融默认自托管 (LiteLLM或Portkey OSS或 Kong);消费产品默认托管 (Cloudflare AI Gateway) 或中层 (Portkey managed) 混合模式:受监管租户自托管,其他托管――网关延迟直接影响TTFT对于TTFT P99 <100ms的SLA,只能选择 Kong(3-8ms开销) 或Cloudflare(1-3ms);对于P99 <500ms,任何网关都可以──

> **【拓展：网关 + 可观测性 + 路由的组合】**阶段17·13(可观测性) +16(模型路由) +19(网关) 在生产中是同一层次的.选择一个覆盖所有三者的工具,或仔细连接它们:大多数2026年部署将升机 (Helicon) 观测性) 或Portkey (Portkey) 护 (Gardrails) 与 Kong (Kong) 规模组合分拆角色.

数据居住是强制功能.医疗保健和金融默认自主托管 (LiteLLM或Portkey OSS或Kong).消费品默认管理 (Cloudflare AI Gateway) 或中层 (Portkey管理).混合型:自主托管为受监管的租户,管理为他人.

### 延迟预算

> **【拓展：AI 网关延迟预算分析】**网络关延迟直接影响TTFT,是选型的关键因素.2026年各网关的延迟开销:(1) LiteLLM 5-15msPython实现,简单但高并发下不稳定;(2) 门键20-40ms功能最全面但延迟最高;(3) Kong 3-8msGo + OpenResty,延迟最低且高并发稳定;(4) Cloudflare/Vercel 1-3ms边缘部署优势.

- 平均上时间为5-15 ms.
- 开关:20-40ms上线.
- 长达3至8秒.
- 云飞/维尔塞尔: 1-3 ms的上限费用 (边缘优势).

网关延迟直接增加到TTFT.对于TTFT P99 <100 ms SLA,Kong或Cloudflare.对于P99 <500 ms,任何.

### 速度限制语义问题

简单的代币桶可以达到中等规模.多租户需要滑窗+破裂允许+每租户的层.LiteLLM运输代币桶;康格运输滑窗;波特基运输层次.

### 网关+可观测性+路由组件

阶段17 · 13 (可观察性) + 16 (模型路由) + 19 (门口) 是同一层的生产. 选择一个覆盖所有三种工具或仔细编程它们:大多数2026部署将机 (可观察性) 或Portkey (护卫) 与 Kong (尺度) 结合在一起,以分类角色.

### 你应该记住的数字

- 简单的速度:2000 RPS,8 GB 的内存.
- 关键:20-40ms上线费用; Apache 2.0自2026年3月以来.
- 港:比波特基快228%,比莱特莱姆快859%.
- 香港价格:每月100美元,最高5美元,
- 云飞/维尔塞尔:在边缘上 1-3 ms.

## 用它实现框架
```figure
mx-gateway-fallback
```

## 用它

`code/main.py`在 429/5xx 注射下模拟了3个提供商中的倒退门路由. 报告延迟,重试率和倒退撞击率.

> `code/main.py`在 429/5xx 注射下模拟了3个提供商中的倒退门路由. 报告延迟,重试率和倒退撞击率.

> `code/main.py`在 429/5xx 注射下模拟了3个提供商中的倒退门路由. 报告延迟,重试率和倒退撞击率.

## 运送它.

这一课产生了`outputs/skill-gateway-picker.md`考虑到规模,运营姿势,合规性,延迟预算,选择一个门户.

> 本课产出发 `outputs/skill-gateway-picker.md`考虑到规模,运营姿势,合规性,延迟预算,选择一个门户.

## 练习题

1. 跑步`code/main.py`设置自主托管的自动接入. 预期的受影响率为5%的供应商错误率是多少?
   中文翻译:运行 `code/main.py`设置OpenAI -> 人类 -> 自托管的回归――哪个触发条件最合理?
2. 您的SLA是TTFT P99<200ms在300ms的基线上.哪些门户保持预算内?
   中文翻译:你的SLA在300ms基线上的TTFTP99 <200ms──哪些网关在预算内?
3. 医疗保健客户需要自主托管+个人信息编辑+审计.
   中文翻译:一个医疗保健客户需要自托管 + PII 脱敏 + 审计――选择Portkey OSS或 Kong――
4. 比较LiteLLM与Kong:团队应迁移到哪个RPS上限?
   中文翻译:比较LiteLLM vs Kong:团队在什么 RPS上限下应该迁移?
5. 设计多租户SaaS的利率限制政策:免费级别,试用级别,付费级别.

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
