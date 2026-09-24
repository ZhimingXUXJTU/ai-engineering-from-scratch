# 失败模式 群体思维 MAST 单元文化 局错误

> 2026年的参考分类是**MAST**根据7个最新的开源MAS显示的1642个执行痕迹,**41–86.7% failure rate**三个根类别:**Specification Problems**角色模糊性,任务定义不清楚;**Coordination Failures**通信故障,状态失调;**Verification Gaps**缺失验证,缺失质量检查.**Groupthink**们的们在们的们中,都会发现,们的们在们的们中, 级例子:一次试机暴风雨,支付失败会触发一次订单试机,从而触发一次库存试机,从而压倒库存服务 (10次负载在秒钟中需要断路). 记忆中毒:一个人幻觉进入共享记忆,下游的 agents treat it as fact;准确性逐渐衰退,使根源诊断痛苦.**STRATUS**通过专业检测/诊断/验证代理报告了1.5倍的缓解成功.本课程将失败模式视为一流的工程目标.

> **【中文解读】**本节介绍多代理的失败模式和多代理系统的群体思维

> **【拓展：failure modes mast groupthink→具体应用】**多 代理 系统的特有失败模式:(1) 群体思维(群体思维)  代理 过度趋同,失多样性;(2) 信息级联 代理的错误被后续代理 放大;(3) 死锁 代理 互相等待无法继续;(4) 活锁 代理 不断改变策略但无法接受.防范措施包括:注入异见代理、随机发言顺序、设置超时.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

>  **【前置】**学生节前请先掌握:阶段16·13-15(共享内存/BFT/投票) ・MAST = 2026 多 代理 失败模式的标准分类法。
>  **【类比】**失败分类 = "医院急诊分诊"――三类根因:规格问题(42%角色不清) 、协调失败(37%通信失灵) 、验证缺失(21%无质检) ・MAST 1642 条 痕迹 显示 41-87% 失败率多 代理 不是银弹。群思 家族:单一文化崩(同基模型 全错) 、群体失明从级付联错支(修失触发重试风暴,10 秒 10 倍负载) ・复:异见代理 + 随机发言顺序 + 断路器。
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

多代理系统在实际任务上失败的时间为41.86.7% (Cemri等人2025测量了这在7个开源MAS中).这不能通过"只添加更多代理"来调试.失败有结构性原因.MAST分类学给你提供了类别.本课程将每个类别映射到一个具体的检测,诊断和缓解模式,因此数字不再看起来任意.

> 多代理系统在真实任务中,41-86.7%的时间会失败(Cemri 等人2025年在7个开源 MAS上测量) ⋅这不是"添加更多代理"就能调试的――失败有结构性原因――MAST 分类法给你类――本课将每个类别映射到具体的检查,诊断和缓解模式――

您的架构是"不够好的"直到您可以指向每个MAST类别并命名您部署的减轻.

> 2026年生产实践将成为设计输入的失败模式.

## 概念的核心概念

### 类

**Specification Problems (41.77% of failures).**代理人的任务没有被充分定义.

> **规范问题（41.77% 的失败）。**代理的任务定义不够紧密.

- 角色模糊:两个代理人都认为自己是评论员.
  中文翻译:角色模糊:两个代理都认为自己是审阅者.
- 任务被说明了以下: "总结这个"当用户想要一个特定的角度时.
  中文翻译:任务规格不足:"总结这个",但用户想要特定的角度──
- 结果是不明确的:代理人不能说它是否成功.
  中文翻译:成功标准隐含:代理无法判断是否成功.

减轻:

> 缓解措施:

- 写出明确的角色合同.每个代理的提示说明了它做什么,以及它不做什么.
  中文翻译:编写显式角色契约――每个代理的提示声明它做什么和不做什么.
- 在代理开始之前,定义"完成看起来像X".
  中文翻译:每个任务的验收测试――在代理开始前,定义"完成的样子是X"――
- 飞行前规格检查:在发送前,一个独立的代理检查任务定义.
  中文翻译:预检规范检查:单独的代理 在分发前审查任务定义──

**Coordination Failures (36.94%).**通信或状态故障.

> **协调失败（36.94%）。**通信或状态故障.

举个例子:

> 孩子:

- 两个代理更新没有同步的共享状态.
  中文翻译:两个代理 不同步地更新共享状态――
- 代理之间丢失的消息 (排队失败,时间过关).
  中文翻译:代理间消息丢失
- 状态漂移:Agent A认为任务完成;B agent仍然执行.
  中文翻译:状态漂移:Agent A 认为任务完成;Agent B 还在执行。

减轻:

> 缓解措施:

- 版本共享状态与乐观的同时.
  中文翻译:带乐观并发的版本化共享状态──
- 显而易见的批评信息确认 (再试到被检查).
  中文翻译:关键消息的显式确认 (重试直到确认)
- 定期进行状态同步检查点; 早期检测漂移.
  中文翻译:定期状态同步检查点;早期检测漂移。

**Verification Gaps (21.30%).**没有独立检查输出.

> **验证缺口（21.30%）。**没有对输出独立检查.

举个例子:

> 孩子:

- 一个代理声称成功,没有人验证.
  中文翻译:一个代理人声称成功;没人验证――
- 连锁代理人每个信任先前的输出.
  中文翻译: 代理链中每个都信任前一个的输出――
- 测试覆盖率缺少了新兴复合行为.
  中文翻译:涌现组合行为缺少测试覆盖――

减轻:

> 缓解措施:

- 独立验证代理 (课13). 仅可阅读,独立的源码访问.
  中文翻译:独立验证代理 (第13课) 〔只读,独立源访问〕
- 显而易见的交付合同: "A的输出必须在B开始之前通过检查器C".
  中文翻译:显式交接契约:"A 的输出必须在B 开始前通过检查器C。"
- 后期分析的结果记录.
  中文翻译:结果日志用于事件后分析.

### 集团思维家族 (arXiv:2508.05687)

五种相关的失败,当代理人同质化或模仿彼此:

**Monoculture collapse.**只有三位经理在 LLM 课程中,他们都会分享幻觉.

**Conformity bias.**代理人适应最声或最自信的同龄人,即使是错误的.

**Deficient ToM.**代理人无法模拟彼此的信仰;协调失败 (课 18).

**Mixed-motive dynamics.**那些有部分优势的代理人, 倾向于妥协,

**Cascading reliability failures.**一个组件的错误模式会触发依赖组件的错误模式.

###        

经典的2026事件模式:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

解决方案是经典的:**circuit breakers**随着下游错误率超过门,将缓存或默认结果进行短路处理.

断路器是少数几个多代理故障减轻措施之一,

### 记忆中毒 (复习)

从第13课开始,一个代理的幻觉变成共享记忆的事实;下游代理人对毒害的事实进行推理.

渐渐的准确性衰退是症状.你不会碰撞,你会慢慢漂移,难以根源原因.

减轻:仅添加日志,来源,不可编写的验证器.

### 斯特拉图斯  专业的故障检测剂

 STRATUS (NeurIPS 2025) 报告了在部署时的缓解成功改善1.5倍:

- **Detection agent.**观察症状模式 (高分歧,重试,精度漂移).
- **Diagnosis agent.**鉴于症状,可能是MAST类别的根源.
- **Validation agent.**缓解症状后,检查症状是否清晰.

这种应对事件的方法是SRE,应用于代理系统.

### 失败模式审计

根据2026年最佳实践,每年 (或每次主要发布) 失败模式审计:

1. **Trace sample.**收集1000个真正的执行痕迹.
2. **Categorize.**对于每个痕迹的失败,将其映射到 MAST+集团思考类别.
3. **Compute failure-by-category rate.**你的系统中占据哪些类别?
4. **Rank mitigations.**哪个解决方案可以消除最多的失败?
5. **Pick 2-3 mitigations.**实施;下季度进行再审计.

没有审计,失败会融入噪音,

### 当系统默默失败时

最危险的故障类别是默认正确性故障.一个系统大声失败 (崩,例外,警报) 可以监控.一个系统产生可信但错误的输出不能通过例外日志检测.这就是为什么验证差距是每次故障的最昂贵类别,尽管它们仅为21.30%的数量.

投资:
- 基于样本的人类评估.
- 黄金数据集回归测试.
- 经纪人对重要输出进行检查.

### 失败与缓慢失败

一些失败是立即的;有些是缓慢的.立即失败 (时间过期,方案不匹配,作者错误) 便宜的检测.缓慢失败 (记忆中毒,单种植漂移,角色模糊性) 昂贵的检测和预防.

2026 年的工程动作:仪器缓慢故障代理,以便在它成为可见错误之前捕获漂移.协议速度,重试速度,输出长度分布和连续代理版本之间的编辑距离都是有用的代理.

## 动手构建
```figure
a5-retry-cascade
```

## 建立它

`code/main.py`执行:

- `FailureTaxonomy`将模拟事件分为MAST+集团思维类别.
- `CircuitBreaker`经典模式; 误差率超过门时开放.
- `RetryStormSimulator`显示断断;切换断路器开关/关闭.
- `DetectionAgent`编写的STRATUS类型的症状匹配器.

运行:

```
python3 code/main.py
```

预期产量:
- 没有断路器的再试风暴:库存错误爆炸 (模拟).
- 电路断电器:门;降低模式响应.
- 检测剂标记了模式并命名了MAST类别.

## 用它使用方法

`outputs/skill-mast-auditor.md`在多代理系统上进行MAST类型的故障模式审计.

## 发射上线

生产中故障模式的纪律:

- **MAST audit per quarter.**随着系统的发展,类别会变化.
  翻译: 中文**每季度 MAST 审计。**不是年度的.类型随着系统的增长而变化.
- **Circuit breakers everywhere.**每次出口通话到任何依赖服务. 默认开放门率为5-10%.
  翻译: 中文**到处都是熔断器。**每个依赖服务的出站调用――默认开值为5-10%的误差率――
- **Golden datasets.**它们每周都会进行反检查.
  翻译: 中文**黄金数据集。**周末对它们进行回归测试.
- **STRATUS trio.**检测+诊断+验证剂监测产量. 开始只使用检测剂; 添加诊断当症状有噪音时.
  翻译: 中文**STRATUS 三重奏。**检测+诊断+验证代理 监控生产――从检测代理开始;当症状杂时添加诊断――
- **Failure budget.**按类别的失败率,明确的SLO. 超过预算会引发停运对话.
  翻译: 中文**失败预算。**按类别失败率显然SLO──超出预算触发停止发布对话──

## 练习题

1. 跑步`code/main.py`确认断路封闭,重新尝试风暴,改变故障门,并观察交易.
2. 实施一个**slow-failure proxy**随着3个平行物体的相应率. 当它急剧下降时,激起警报. 通过逐步相关化物体输出来模拟单种产物漂移.
3. 阅读Jemri等 (arXiv:2503.13657). 选择他们7个MAS系统中的一个,并绘制其前3个失败类别.
4. 阅读集团思维论文 (arXiv:2508.05687). 确定五种模式中哪种最难在生产中检测. 提出代理测量.
5. 设计一个STRATUS类型的检测-诊断-验证三组,用于特定的多代理系统.检测监视哪些症状?诊断建议哪些减轻措施?验证如何确认它们有效?

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## 继续阅读 继续阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) MAST分类,NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687)单种植,合规性和五家族分类
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) NeurIPS 2025 程序入口 (检测+诊断+验证)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/)正规的断路切断器参考
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)生产故障模式的说明
