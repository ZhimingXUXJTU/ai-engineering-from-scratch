# 影子,加拿大陆地, 及 LLM 发展发展

> 应用程序的部署结合了软件部署最困难的部分:无单元测试,分散故障模式,信号延迟. 序列是 (1) 影子模式 复制的提示请求候选模型,记录,与零用户影响比较;捕获明显的分布问题,但不是质量保证; (2) 化推广 渐进的流量转移 10% → 25% → 50% → 75% → 100% 每一步都有门;跟踪延迟百分比,成本/请求,错误/拒绝率,输出长度分布,用户反率; (3) 稳定后A/B测试不同的替代方案. 由于GPU FP非关联性加上批量大小差异,具有相同输入的运行中高达15%的精度变化. 成本是变量,不是常量 一个20%更好的模型可以每次调用成本高出3倍. 转型速度是决定性的:如果转型需要重新部署,你太慢了. 政策生活在配置/旗中;模型生活在注册表中,注册表有注册表;反转 = 翻转政策 + 逆转门 + 缩旧模型在几秒钟内.

> **【中文解读】**本节介绍了影子/金丝雀/渐进式部署LLM 服务安全上线部署策略.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

>  **【前置】**学本节前请先掌握:阶段17·13(可观测性) ‧阶段17·21(A/B 测试) ・LLM 上线 = 软件部署最难的组合:无单元测试、失败模式分散、信号延迟──
>  **【类比】**部署三步 = "飞机首飞流程"――影 = 地面模拟(复制产品 请求,零用户影响,对比但不换);加拿大 = 真飞但逐步开载客客客(10%→25%→50%→100%;A/B = 商业航班对比(稳定测试不同方案) ――关键:不确定性不可消除(GPU 浮点+批量 差异致 15% 准确率波动);成本是变量(好20%的模型可能贵3倍);秒速回滚决定性(旗级 切换不可重新部署) ――
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 区分影子模式 (零冲击比较),加拿大 (现场流量进步),A/B (稳定证实比较).
  中文翻译:区分影子模式 (区分影子模式) 零影响比较) 金丝雀 (金丝雀) 真实流量渐进) 和 A/B (统计比较) 〔中文翻译:区分影子模式〕
- 列出五项专为LLM的加拿大标准 (延迟,成本/请求,错误/拒绝,输出长度分布,用户反).
  中文翻译:列举五个 LLM 特定金丝雀指标 ((延迟、成本/请求、错误/拒绝、输出长度分布、语义质量样本)
- 解释为什么LLM非决定性 (高达15%) 改变了"稳定"在推广中意味着什么.
  中文翻译:解释为什么LLM不确定性 (高达15%) 改变了推出中"稳定"的含义.
- 设计一个需要几秒钟 (政策转换) 而不是几小时 (重新部署) 的反转路径.
  中文翻译:设计一个秒级回滚路径 (策略翻转),而不是小时级 (小时级) (重新部署)

## 问题 问题引入

> **【中文解读】**部署将软件部署中最难的部分结合在一起:没有单元测试、模糊的失败模式、延迟信号――正确的序列是:(1) 影子模式将生产请求复制到候选模型,日志对比,零用户影响;(2) 金丝雀发布10%→25%→50%→75%→100% 渐进流量切换,每个阶段都有门控标;(3) A/B测试稳定性确认后的比比比比.

> **【拓展：LLM 非确定性与部署】**在LLM的不确定性是不可约束的 同样的输入在同一模型上可能产生高达15%的准确率差异.原因:GPU FP不结合性,批量大小差异,温度 > 0的采样).

你发出了新车型. 离线评估显示了3%的准确度,你将其转换到生产中. 在24小时内,成本上升了40%,用户指下降了8%,三个客户的门票报告了"奇怪的答案". 你回头. 再部署需要3小时. 你的周末是破产的.

影模式在任何用户看到之前就会发现成本上40%的. 利将在指下移动时停止在10%的水平. 政策旗倒车将需要30秒. 纪律是填补"离线评估看起来很好"和"真实用户很开心"之间的差距.

## 概念的核心概念

### 影子模式

> **【中文解读】**影子模式候选模型接收与生产相同的请求,输出仅记录不返回用户.日志内容包括:输出内容(与生产差) 、标记数量(成本差) 、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒绝变化、硬错误――不能捕获:用户会感知到的质量差影子是烟雾测试,不是质量测试――

申请人收到与生产相同的请求;输出记录,而不是返回用户.用户影响零.记录:

- 产量含量 (与生产差异).
- 代币计数 (成本分数).
- 延迟.
- 拒绝和错误.

捕获:成本升高,长度回归,明显的拒绝变化,严重的错误. 没有捕获: 质量的德尔塔用户会感觉. 影子是一个烟雾测试,而不是质量测试.

### 卡纳里地区的部署

> **【拓展：LLM 金丝雀发布的五个门控指标】**丝雀发布必须监控的五门控标:(1) 延迟百分位(P50/P95/P99) 可纳 P99 > 1.5x 基线则触发;(2) 每次请求成本>20% 高于基线则触发;(3) 错误/拒绝率2x 基线则触发;(4) 输出长度分布均值 + P99 分布偏移值则触发;(5) 用户反率指/工单 1.5x 基线则触发;;典型进度 1%→10%→25%→50%→75%→100%,每个阶段积累足够本5-15 分钟 分样检查间隔) ⋅

随着门的转移,流量逐步转移.典型的进步:1% → 10% → 25% → 50% → 75% → 100%.每步5个指标的门:

1. **Latency percentiles** P50, P95, P99. 违规性:鱼的P99> 1.5x基线.
2. **Cost per request**混合. 违规:超过原线20%
3. **Error / refusal rate**5xx加上明确拒绝.
4. **Output length distribution**平均值+P99. 违规性:分布转移.
5. **User-feedback rate**指/票票申请. 违规:1.5倍的基线.

### 无决定主义是新的变化

相同的输入产生的输出不相同.

-  GPU FP非关联性 (浮点降低顺序因批量而异).
- 批量差异 (在128批量和16批量时相同的提示).
- 采样 (温度 > 0).

测量:在相同的评估集中,可进行最大15%的精度变化.在推出中"稳定"意味着指标在预期变化范围内,不与基线相同.设置门在噪音地面以上.

### 成本是变量

通过"更好的"模型,每次通话都会有3倍的成本.成本/请求是五个门口之一.

### 滚动是武器

- 政策标志 (功能标志系统):配置中的翻转百分比;需要几秒钟.
- 模型点 (注册表消化):点模型不会自动升级.
- 翻转=反转旗+设置固定的消化到之前.

如果你的堆需要重新部署,然后在滚动之前修复.

### 工具

> **【拓展：LLM 渐进式部署工具链】**2026年LLM 渐进式部署的工具选择:(1) Argo Rollouts / FlaggerKubernetes 原生渐进式部署控制器,与 Istio/Linkerd 加权路由集成;(2) Istio 重量路由服务网格级流量切分;(3) KServe / Seldon Core模型服务自带卡纳里功能;(4) 功能旗 发射暗藏、旗手、释放,策略级翻转无需重新部署──回滚基础设施:策略标志标志 功能系统) 翻转百分比在配置中秒级) 模型注册摘要 固定尾不自动升级) ◎如果您需要堆重新部署回滚,请再上线重新部署.

**Argo Rollouts**现在,**Flagger** Kubernetes 渐进式交货控制器. 集成到Istio/Linkerd权重路由.

**Istio weighted routing**服务网层面的交通分区.

**KServe / Seldon Core**模型提供内置的菜.

**Feature flags**发射,暗,旗,释放.

### 计量序列

卡纳里大门根据流量每5-15分钟检查.1%的流量每窗口提供50-150个数据点,但对用户反来说足够.10%的数据提供了10倍多.进步应该停留足够长时间,以在每个步骤上积累足够的样本.

### 选项:A/B

如果新型号明显不同 (不同行为,不同的成本曲线,不同的调度),在鱼通过后,A/B测试它50%;如果它只是一个改进的版本,当鱼门通过时,跳到100%.

### 你应该记住的数字

- 鱼进展:1% → 10% → 25% → 50% → 75% → 100%.
- 无决定性性上限:在相同输入中,可达15%的连续变异.
- 五个可取量指标:延迟,成本,错误/拒绝,输出长度,用户反.
- 成本门:超过原线20%是违规行为.
- 秒钟,不是几个小时.

## 用它实现框架
```figure
i4-canary-ramp
```

## 用它

`code/main.py`报告中,哪个阶段的推出停止,哪个门启动.

> `code/main.py`报告中,哪个阶段的推出停止,哪个门启动.

> `code/main.py`报告中,哪个阶段的推出停止,哪个门启动.

## 运送它.

这一课产生了`outputs/skill-rollout-runbook.md`鉴于候选模型,基线和风险耐受性,设计了 shadow→canary→100%计划.

> 本课产出发 `outputs/skill-rollout-runbook.md`鉴于候选模型,基线和风险耐受性,设计了 shadow→canary→100%计划.

## 练习题

1. 跑步`code/main.py`鱼在哪个阶段停止?
   中文翻译:运行 `code/main.py`注入25% 成本回归 金丝雀在哪阶段捕获它?
2. 您的新型号在线上获得3%的准确度,但成本/请求是+18%.
   中文翻译:你的新模型离线精度提高了3%,但成本/请求+18%──值得上线吗?取决于产品上下文──
3. 设计一个不到60秒的回滚,并列出所需的基础设施.
   中文翻译:设计端到端 60秒内回滚.
4. 没有确定性在你的评估中显示 ±7% 设置鱼门,所以你不会错误报警.你使用什么乘法?
   中文翻译:非确定性显示+/-7%──设金丝雀门控以避免误报──
5. 影子模式在鱼之前,成本上升了40%.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## 继续阅读 继续阅读

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
