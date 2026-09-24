# 士师资本 单位经济学和多租户归因

> 传统的FinOps在LLM支出上断绝.成本是代币交易,而不是资源上班时间.标签不映射API调用是一个交易,而不是资产.工程决策 (即时设计,文本窗口,输出长度) 是财务决策.2026年游戏册在第一天对仪器的三个属性维度:每个用户 (`user_id`) 对于座位定价和扩展,每任务 (`task_id`其他`route`) 对于产品表面成本和优先级,`tenant_id`) 单位经济和更新. 两个代币层,一个藏的钱. 多租户产品的执行梯度:每租户的利率限制 (2-3倍预期峰值,清除429+再试);每日支出限额 (1.5-3倍合约的上限;触发加紧速度+警报);消耗点 z-score > 4 (自动暂停+开启页面). 归类模式:标签和汇总,远程测量连接器 (追踪ID →发票;最高精度),采样和抽象,基于模型的分配,事件来源,实时流媒体. 单位指标:每个解决查询的成本,每一个生成的文物的成本  不是$/M代币. 复制标签总是错失; 要求创建工具.

> **【中文解读】**传统的FinOps在 LLM 支出上失效成本是代币交易而不是资源运行时间――工程决策――提示设计,上下文窗口,输出长度) 是财务决策――2026年的Playbook 建议在第一天建立三个归因维度:按用户,按任务,按租户――四个代币层 (提示,工具,单位记忆,响应) 不能合并成一桶――标标应该为"每次解决的查询成本",而不是"每百万代币成本"――

> **【拓展：FinOps → LLM 成本优化】**在LLM应用中,成本控制是核心挑战.vLLM+量化部署可降低推理成本,模型路由,简单任务用小模型,复杂任务用大模型) 可优化性价格,语义缓存可减少重调.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)

>  **【前置】**学本节前请先掌握:阶段17·13(可观测性) 、阶段17·14(缓存) 、云FinOps 基础――LLMFinOps = 传统FinOps 失效后的新方法――
>  **【类比】**根据标签=资产; 根据标签=交易; 根据标签=交易; 三大归因维度; 一天必埋:每用户; 席位定价; 任务; 产品成本; 单位经济; 四层标签; 快速/工具/记忆/回应; 必须分桶合并一个桶会掩盖真实开销.
> ️ **【易错点】**单位指标使用$/M代币是错的,应该使用"每次解决查询的成本"――强制阶梯:限流(2-3x 峰值)→日上限(1.5-3x 合约)→杀开关(z-score>4自动暂停)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 解释传统的FinOps (标签+层次) 为什么不适用于LLM支出,并列出三个新的归属尺寸.
  中文翻译:解释为什么传统的FinOps (上级) 在LLM 支出上失效,并说出三个新归因维度.
- 列出四个代币层 (即时,工具,内存,响应) 以及为什么单桶支付隐藏成本.
  中文翻译:列举四个标志层 (提示、工具、记忆、响应),以及为什么单桶计费产生误导.
- 设计一个多租户产品的执行梯度 (利率 →支出 cap →杀死开关).
  中文翻译:设计执行阶梯(速率 -> 支出上限 -> 断开关) 用于多租户 LLM 服务。
- 选择单位指标 (每个解决的查询/文物的成本) 而不是$/M代币.
  中文翻译:选择单位指标 ((每次解决查询/产品成本) 而不是$/M代币──

## 问题 问题引入

> **【中文解读】**传统FinOps在LLM 支出中失效的核心原因:LLM 成本是代币 交易而不是资源运行时间.标签:标签:不能直接映射API调用是交易而不是资产.工程决策:提示设计,上下文窗口,输出长度) 是财务决策.你的账单显示4万美元,但你不知道:哪个租户花了多少钱,哪些产品驱动功能是否有用利用,是快速膨胀还是工具调用或记忆扩大导致的.

你的账单上写着4万美元.
- 租户花了它.
- 哪个产品特征驱动它.
- 任何个人使用者是否虐待.
- 无论是快速膨胀,工具调用,还是提升记忆力,

标签和集成在提供商侧工作云资源 (EC2,S3) 标签扩散到线条项目.LLM API呼叫不自动标签.

## 概念的核心概念

### 属性三维度

**Per-user**(`user_id`):谁是什么成本. 驱动座位的定价,扩张对话,识别电源用户.

**Per-task**(`task_id`其他`route`车辆具有优先级,杀死成本的决定.

**Per-tenant**(`tenant_id`):哪个客户是利的. 驱动单位经济,续航定价,层次门.

仪器三位都在电话站第一天.

### 象征的四层

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

它们在属性方案中被分解.

### 执行阶梯

> **【中文解读】**多租户产品的三级强制阶梯:(1) 速率限制每租户2~3倍 预期峰值,返回429+退休后,租户感受到摩擦但无意外账单;(2) 日支出上限每租户1.5~3倍 合约上限,触发时收紧率限制 + 告警客户成功团队;(3) 关闭开关当支出 z-score > 4(相对租户基线) 当自动暂停租户,通知班级,升级到运维和客户成功.

> **【拓展：LLM FinOps 的复合优化栈】**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

1. **Rate limit**预期峰值的2~3倍. 返回429个`Retry-After`租户看到摩擦,没有意外账单.

2. **Daily spend cap**预测,每租户的收费率为1.5-3倍,

3. **Kill switch**租户自动暂停租户; 电话页面;升级到运营+CS.

### 归因模式

- **Tag-and-aggregate**简单,粗略. 简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单,简单
- **Telemetry joiner**通过追踪身份证将痕迹连接到账单.
- **Sampling + extrapolation**平均成本: 样本5-10%,乘以. 成本效益较高,不用排尾.
- **Model-based allocation**对于没有标签的遗留数据.
- **Event-sourced**实时的事件 (Kafka/Kinesis).
- **Real-time streaming**仪表板更新次下.

### 每个X的成本是单位指数

> **【中文解读】**美元/M代币是供应商语言──产品指标应该是:(1) 每解决的支持工单成本;(2) 每生成文章成本;(3) 每成功的代理 任务成本;(4) 每用户会话分钟成本──将成本绑定到产品产出,否则优化没有点──关键原则:在请求创建时就埋埋点──反动标签总是遗漏,不要事后补充归因──

货币的价格是卖家的价格.

- 解决的支持票的成本.
- 产品成本
- 通过成功的代理任务的成本.
- 按用户会议分钟的成本.

关键成本与产品结果,否则优化是无关的.

### 成本归因的痕迹形状

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

通过每次通话发射. 存储在数据湖中. 按维度汇总. 17 期 13 期可观测性堆是这个生活的地方.

### 合金储蓄堆

堆积:缓存+批量+路线+网关.
- 缓存 L2 (阶段17 · 14):输入价格低于10倍.
- 批量 (阶段17·15):50%折扣.
- 路线到廉价型号 (阶段17·16):成本降低60%.
- 网关效率 (阶段17·19):冗余性+重试.

最好的情况: 起的基线是5-10%. 大多数团队都使用了2-3个杆;少数团队都使用了四个杆.

### 你应该记住的数字

- 分配尺寸:每用户,每任务,每租户.
- 快速,工具,内存,响应.
- 关闭开关:使用z分数> 4.
- 单位指标:每个解决查询的成本,而不是$/M代币.
- 堆积优化:可能的基线5%~10%

## 用它实现框架
```figure
i4-spend-ladder
```

## 用它

`code/main.py`模拟一个多租户的LLM服务,使用三层级的执行梯度. 注射一个虐待租户,并证明杀死开关的射击.

> `code/main.py`模拟一个多租户的LLM服务,使用三层级的执行梯度. 注射一个虐待租户,并证明杀死开关的射击.

> `code/main.py`模拟一个多租户的LLM服务,使用三层级的执行梯度. 注射一个虐待租户,并证明杀死开关的射击.

## 运送它.

这一课产生了`outputs/skill-finops-plan.md`根据产品和规模,设计了归属方案和执行阶梯.

> 本课产出发 `outputs/skill-finops-plan.md`根据产品和规模,设计了归属方案和执行阶梯.

## 练习题

1. 跑步`code/main.py`杀人开关在哪个点射?
   中文翻译:运行 `code/main.py`断开关在什么z-score下触发?如何防止错误报道?
2. 设计一个每租户,每任务成本仪表板.
   中文翻译:按租户设计,按任务的成本仪表板.你首先构建哪个视图?
3. 你最大的租户是单位经济负, 根据客户影响,提出三个干预措施.
   中文翻译:你最大的租户单位经济学为负.
4. 计算支持产品的解决门票的成本: 3M代币/门票,每天约800门票,GPT-5缓存率.
   中文翻译:计算支持产品的每解决工单成本:3M代币/工单,约2.5次重试――单位经济学可行吗?
5. 提议是否可以回归标签.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## 继续阅读 继续阅读

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
