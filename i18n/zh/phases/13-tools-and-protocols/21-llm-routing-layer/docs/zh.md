#                                                                                                                                                                                                                                                               

> 提供商锁定是昂贵的. 不同工具调用工作负载适合不同的模型. 路由网关提供一个API表面,重试,故障,成本跟踪和防护. 2026年将占据三种类型的主导地位:LiteLLM (开源自主托管),OpenRouter (管理SaaS),Portkey (生产级,开源于2026年3月). 这一课列出了决策标准,并通过了SDLB路由门户.

> **【中文解读】**供应商锁定成本高昂.不同的工具调用工作负载适合不同的模型. 路由网关提供统一的API接口,重试,故障转移,成本追踪和护.

> **【拓展】**解决任务复杂性自动路由至优模型 (高可用) 供应商故障自动切换 (高可用) 延迟敏感路由 (用户体验) 合规区域路由 (数据主权) A/B 测试路由 (实验) .这是人工智能工程从单个模型向多个模型架构的关键基础设施.

>  **【前置】**学习节前请先掌握:(1) 阶段13·02(函数调 Deep Dive) 理解三家供应商的API差异,本节是统一它们的方案;(2) 阶段13·17(门户) 网关和路由经常一起部署;(3) HTTP 代理基础、重试与超时机制──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, routing + failover + cost tracker) | **语言:** Python (stdlib, routing + failover + cost tracker)
**Prerequisites:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 学习目标

- 区分自主托管,管理和生产级路由选项.
  中文翻译:区分自托管、托管和生产级路由选项。
- 实施一个反弹链,以确定优先顺序重新尝试供应商故障.
  中文翻译:实现按定义优先级顺序在供应商失败时重试的回归链.
- 追踪每次请求成本和托克使用在供应商之间.
  中文翻译:跨供应商追踪每请求成本和代币使用量
- 对于给定的生产限制,选择LiteLLM,OpenRouter和Portkey之间.

> **【中文解读】**学习目标:区分自托管,托管和生产级路由选项;实现供应商故障时的回归链;跨供应商追踪每次请求成本和代币使用量;根据生产约束选择LiteLLM/OpenRouter/Portkey。

## 问题 问题引入

> **【中文解读】**路由重要场景:(1) 成本克劳德·索尼特 费用是海库的3倍,分流任务用海库足够;(2) 故障转移OpenAI 机时自动切换到人类;(3) 延迟实时聊天需要快速首代币;(4) 合规EU用户留在欧盟地区;(5) 实验A/B 两个模型――路由网关提供统一的OpenAI 兼容 API 处理一切――

提供商路由情况:

> 供应商路由重要场景:

1. **Cost.**对于一个分类任务,海库足够,对于一个合成任务,索尼特值得它. 按要求路线.
  翻译: 中文**成本。**对于分流任务,Haiku 够用;对综合任务,Sonnet 值得.

2. **Failover.**开放AI有个糟糕的时刻,每一个请求都失败了,你想要自动返回人类,而不会重新部署.
  翻译: 中文**故障转移。**你想自动回到人类,而无需重新部署.

3. **Latency.**现场聊天界面需要快速的时间到第一代代码.
  翻译: 中文**延迟。**实时聊天 UI 需要快速首发代币――批量摘要器不需要――按延迟SLA路由――

4. **Compliance.**欧盟用户必须留在欧盟地区.
  翻译: 中文**合规。**欧盟用户必须留在欧盟区域.

5. **Experimentation.**两种模型在同一工作量上,测试桶的路线.
  翻译: 中文**实验。**在同一工作负载上 A/B 两个模型.

通过手动编码,每个集成都会重复.一个路由网关给一个与OpenAI兼容的API,处理其余的.

> 每个集成手写这些都很重复.

>  **【类比】**路由网关像"万能充电转接头"――每个手机厂商 (OpenAI/Anthropic/Google) 有自己的快充协议 (快充协议) API形态),原本你出差要带三根线.路由网关是一个"中间转换器"你的代码只对USB-C接口 (OpenAI兼容API) 编程,转换器内部根据任务自动选择最快的协议协议失败时切换备用协议 (快充协议失败) 计算每度电费多少钱 (成本追踪) ⋅换手机厂商你不需要重写代码.

## 概念的核心概念

### 基于 OpenAI的代理形状

路由门户暴露了`/v1/chat/completions`通过""来实现,它可以接受OpenAI的方案,并内部代理到"人类"/"双子座"/"科赫"/"奥拉马"任何东西.

> 每个人都说开放AI 形态――路由网关曝光`/v1/chat/completions`、接受OpenAI计划、内部代理到人类/双子座/科赫尔/奥拉马/任何──客户端不关心──

### 模型姓名

代码是""的.`our_smart_model`当一个提供商发送新一代时,你改变了代号服务器侧面;你的代码不会触摸任何东西.

> 你的代码不说`claude-3-5-sonnet-20251022`而是`our_smart_model`◎网关将别名映射到真实模型──当人类版发布Claude 4时,你在服务器端改别名;代码不动──

> ️ **【易错点】**场景:倒退链设置了5个供应商且没有预算限制 / 后果:上游故障时5个供应商都重试一遍,单请求成本升5倍;某些故障(如即时违规) 所有供应商都会拒绝,重试无意却烧钱 / 修复:(1) 设置全局预算 cap,超出直接拒绝;(2) 区分"重试有意义的错误"的错误(5xx、超时) 和"重试意义的错误4xx、内容违规);(3) 同一请求总重试 ≤3次;(4) 监控常规回落率,异升告警方发出.

>  **【困惑】**问:既然LiteLLM开源自托管,为什么还需要OpenRouter或Portkey?**LiteLLM**适合有 DevOps 团队的公司,自己维护可控成本,但要负责升级,监控,故障处理;**OpenRouter**适合早期项目或个人开发人员,零运维但单价更高;**Portkey**介于两者之间,开源但有商业版本――生产级――>10M/天) 通常LiteLLM自托管+商业Portkey 混合:核心流量自托管,溢出出Portkey――

### 背后链

```
primary: openai/gpt-4o
on 5xx: anthropic/claude-3-5-sonnet
on 5xx: google/gemini-1.5-pro
on 5xx: refuse
```

通过网关来定义这个配置,反试计算预算,所以反弹升不会导致成本爆炸.

> 网关在配置中定义──重试计入预算,使退级联不爆炸成本──

### 语义缓存

类似或接近相同的提示会进入缓存,而不是提供商.重复代理循环的节省率可能为30至60%.键是基于嵌入式的;几乎相同的提示共享缓存槽.

> 同样或近相同的快速命中缓存而不是供应商――重复 代理循环节省可达 30-60%――键基于嵌入式;近相同的快速共享缓存槽――

### 防护

网关级别:

> 网关级:

- **PII redaction.**在发送提示之前,通过Regex或ML.
  翻译: 中文**PII 脱敏。**发送快速前基于正则或ML的脱敏.
- **Policy violations.**拒绝禁止内容的提示.
  翻译: 中文**策略违规。**拒绝包含禁止内容的提示.
- **Output filters.**除漏的完成.
  翻译: 中文**输出过滤器。**清理补全中泄漏.

波特基和康格都拥有专注的防护护.

> 港口和港口都发布带主张的护──LiteLLM 留作可选──

### 每个关键利率限制

单个 API 关键 = 一个团队. 每个关键预算阻止一个团队消耗共享的配额.大多数网关支持这一点.

> 一个API关键 = 一个团队. 每个关键预算防止单一团队消耗共享配额.

### 自主托管与管理交易

| Factor | LiteLLM (self-hosted) | OpenRouter (managed) | Portkey (production) |
|--------|----------------------|----------------------|----------------------|
| Code | Open source, Python | Managed SaaS | Open source (Mar 2026) + managed |
| Setup | Deploy a proxy | Sign up | Either |
| Providers | 100+ | 300+ | 100+ |
| Billing | Your own keys | OpenRouter credits | Your own keys |
| Observability | OpenTelemetry | Dashboard | Full OTel + PII redaction |
| Best for | Teams that want full control | Rapid prototyping | Production with compliance |

当你有一个SRE团队并想要数据主权时,LiteLLM获胜. 当你想要单个订阅而没有过度订阅时,OpenRouter获胜. 当你需要防护线和合规时,Portkey获胜.

> 简单的LiteLLM 在你有SRE 团队并希望数据主权时胜出.

### 成本追踪

每个要求都包含`provider`现在`model`现在`input_tokens`现在`output_tokens`乘以每个模型的每个代币价格 (从门户管理的价格表中抽取).

> 每次要求携带`provider`,我知道.`model`,我知道.`input_tokens`,我知道.`output_tokens`△乘以每模型每代币价格 △从网关维护的价格表拉取) ・按用户/团队/项目聚合物

### 转换方式

网关可以导航LLM电话和MCP样本请求.当采样请求的模型偏好特定模型时,网关转化为右后端.这是阶段13·17 (MCP网关) 和本课程的路由网关有时合并成一个服务.

> 网关可同时路由LLM调用和MCP样本采集 请求──当采集 请求的模型 偏好特定模型时,网关翻译到正确后端──这是阶段13 · 17(MCP 网关) 和本课的路由网关有时合并为单一服务的地方──

### 路由策略

- **Static priority.**排名第一,回归错误.
  翻译: 中文**静态优先级。**列表中第一个;出错时回退.
- **Load balancing.**圆或重量.
  翻译: 中文**负载均衡。**轮询或加权.
- **Cost-aware.**选择最便宜的模型,满足延迟/质量.
  翻译: 中文**成本感知。**选择满足延迟/质量的最便宜模型――
- **Latency-aware.**在最后的9分钟中选择最快的模型.
  翻译: 中文**延迟感知。**选最近的N 分钟最快的模型――
- **Task-aware.**快速分类器路线编码到一个模型,总结到另一个模型.
  翻译: 中文**任务感知。**快速分类器将编码路由到一个模型,摘要到另一个.

## 用它实现框架

> **【中文解读】** `code/main.py`实现约150行路由网关:接受OpenAI格式请求,翻译成每供应商存储根,运行优先级回归链,追踪每次请求成本,应用PII 脱敏――三个场景:正常请求、主供应商机触发故障转移、PII 泄露被脱敏拦截――
```figure
tp-router-failover
```

## 用它

`code/main.py`执行一个路由门口在150行:接受OpenAI形状的请求,转换为每个提供商的条,运行优先回归链,追踪每请求成本,并对输入应用PII编辑通行.运行它三个场景:正常请求,主要提供商中断引发回归,编辑捕获的PII泄漏.

> `code/main.py`实现约150 行的路由网关:接受OpenAI 形态请求"",翻译为每一个供应商存储根"",运行优先级回归链"",追踪每一个请求成本"",对输入应用 PII 脱敏――使用三个场景运行:正常请求"",主要供应商机触发故障转移"",PII 泄露被脱敏捕――

什么要看:

- `ROUTES`标签: alias -> 具体供应商优先排序列表.
  翻译: 中文`ROUTES`字典:别名 -> 优先级排序的具体供应商列表
- 倒退循环在5xx上重新尝试.
  中文翻译:回退循环在5xx上重试――
- 成本跟踪器乘以每个模型的价格乘以代币使用率.
  中文翻译:成本追踪器将代号 用量乘以每模型费率.
- 信息编辑器在转发之前扫除SSN形状的模式.
  中文翻译:PII 脱敏器在转发前清理SSN 形状模式。

## 运送它.

> **【中文解读】**本课产出发 `outputs/skill-routing-config-designer.md`给定工作负载配置 (延迟、成本、合规),选择LiteLLM/OpenRouter/Portkey并生成路由配置――

这一课产生了`outputs/skill-routing-config-designer.md`鉴于工作负载配置 (延迟,成本,合规性),技能选择LiteLLM/OpenRouter/Portkey并生成路由配置.

> 本课产出发 `outputs/skill-routing-config-designer.md`△给定工作负载配置(延迟、成本、合规),该技能 选择LiteLLM/OpenRouter/Portkey 并生成路由配置──

## 练习题

1. 跑步`code/main.py`引发停机情况;确认第二家供应商出现逆转,并将成本正确归因.
   中文翻译:运行 `code/main.py`◎触发机场景;确认回归于第二供应商,成本正确归属.

2. 添加语义缓存:提示的SHA256是一个搜索密钥;缓存击中即时返回. 测量重复通话的成本节省.
   中文翻译:添加语义缓存:快速的 SHA256 是查找键;缓存命中立即返回――测量重复调用成本节省――

3. 添加一个快速分类器,将"代码"...的提示传递到一个支持智能的名,
   中文翻译:添加快速 分类器,将"代码 ..."快速 路由到偏好智能的别名"",总结 ..."路由到偏好速度的别名。

4. 设计每组预算:每个团队都有一个月度支出限制;一旦达到限制,网关拒绝请求.选择执行细节性 (按要求或窗口).
   中文翻译:设计每团队预算:每团队有月度支出上限;网关在达到上限时拒绝请求――选择执行分数(每请求或窗口) 』

5. 阅读LiteLLM,OpenRouter和Portkey文件.
   中文翻译:并排阅读LiteLLM、OpenRouter 和 Portkey 文档──命名为每一个发布的,但其他两个没有一个功能──

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [LiteLLM — docs](https://docs.litellm.ai/)自主托管的路由门户
  中文翻译:自托管路由网关
- [OpenRouter — quickstart](https://openrouter.ai/docs/quickstart)管理的路由SaaS
  中文翻译:托管路由SaaS
- [Portkey — docs](https://portkey.ai/docs)生产路由,有护
  中文翻译:带护的生产路由
- [TrueFoundry — LiteLLM vs OpenRouter](https://www.truefoundry.com/blog/litellm-vs-openrouter)决策指南
  中文翻译:决策指南
- [Relayplane — LLM gateway comparison 2026](https://relayplane.com/blog/llm-gateway-comparison-2026)供应商调查
  中文翻译:供应商调研
