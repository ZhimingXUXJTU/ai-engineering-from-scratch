# 更多的代理人应对事件, 跑本,预测检测

> 通过RAG,通过基础设施数据 (日志,运行簿,服务拓) 实现自动化调查,文档和协调阶段的LLM. 2026 建筑模式是多代理管弦乐专业代理 (日志,指标,运行书籍) 由监督者协调; AI提出假设和查询,人类批准判断调用. 数据狗比特人工智能和Azure SRE代理将这些作为管理产品. 跑本正在发展:NeuBird Hawkeye使用对抗评估 (两个模型分析相同事件;协议 =信心,不同意见 =不确定性); 操作记忆在团队变化中持续存在. 自动补救仍然谨慎:人工智能建议,人类批准. 完全自主操作是狭窄的 (重新启动,反弹特定部署) 紧密的防护 任何销售"设置并忘记"的人都在超销. 突出界限:事件前预测 麻省理工学院的研究报告显示,在历史记录+GPU时间+API错误模式上训练的LLM预测, 预测:到2026年底,企业中95%的LLM将自动转账.

> **【中文解读】**本节介绍了AI的SRE实践LLM服务的站点可靠性工程方法论.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy multi-agent incident triage simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)

>  **【前置】**学本节前请先掌握:阶段17·13(可观测性) ‧阶段17·24(混沌工程) ‧SRE 基础(跑本/事件响应) ・AI SRE = LLM 加持的故障响应。
>  **【类比】**据悉,在中国,人工智能 (AI) 已经开始使用了大量的技术,技术,技术,技术,技术,技术,技术,技术,技术,技术,技术,技术,技术,技术等技术,技术,技术,技术,技术等.
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 绘制多代理AI SRE架构:监督者+专业代理 (日志,指标,运行簿) +人体批准门.
  中文翻译:绘制多代理 AI SRE架构:主管 + 专业代理(日志、指标、运行手册) 』
- 解释为什么自动补救是狭窄的 (重新启动,重新部署) 而不是广泛的 (重建服务).
  中文翻译:解释为什么自动修复是狭窄范围的(重启Pod、回滚部署) 而不是宽范围的(重新架构) 
- 举个对抗性评估模式 (NeuBird Hawkeye):两个模型一致=信心;不同=升级.
  中文翻译:说出对抗性评估模式 (新鸟眼):两个模型一致 = 置信度;不一致 = 升级到人类.
- 提及MIT 89%早期检测结果和操作限制:没有动作的预测只是仪表板.
  中文翻译:引用MIT 89% 早期检测结果和运维约束:无历史基线的预测不可行.

## 问题 问题引入

> **【中文解读】**根据服务分组日志,关联到最近部署,匹配跑本都是RAG+工具的使用.监督式代理可以在人类开启数据库之前完成首轮分类并呈现假设.

> **【拓展：AI SRE 产品市场】**2026年 AI SRE 产品:(1) 数据狗 位 AI数据狗 内部托管 SRE副驾驶员;(2) Azure SRE 代理 Azure 原生;(3) NeuBird Hawkeye对抗性评估(两个模型独立分析同一事件,一致=高置信,不一致=升级) + 操作记忆(后死亡存入量 DB);(4) 页面职责 AIOps分类 + 去重;5) 事件.io 机器自动驾驶事件指挥官 + 协调.

电话上的工程师在凌晨3点被调用"检查时错误率很高".他们检查了Datadog,Loki,三个运行簿,部署日志.30分钟后,他们意识到根本原因是从KV缓存尖端的VLLM OOM.他们重新启动了,错误清除了.

2026年,该调查的前20分钟可自动化. 根据服务,与最近部署相关的,与运行簿相匹配的集团日志都是RAG+工具使用.监督的代理人在打开Datadog之前可以进行第一次通过分类并提出假设.

完全自主修复是一个不同的问题. 重启:安全. 扩展GPU池:安全,如果政策允许. 重新构建服务:绝对不是. 纪律是画窄的线.

## 概念的核心概念

### 多代理架构

> **【中文解读】**多 代理 AI SRE 架构:监督人将事件分为查询,分派给专业化代理 日志 搜索日志 标志 查询 预示 查询 预示 运行簿 查询文档) 监督人 综合,向人类呈现假设 + 证据  人类批准或重定向  安全自动修复范围:重启 Pod 、回滚特定部署、预批准范围内扩展池  不安全范围:更改服务拓、更改资源限制、部署新代码、更改 IAM。

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

监督者将事件分为子查询.专业代理人有工具访问 (日志搜索,PromoQL,文件检索).监督者合成,向人类提供假设 +证据.人类批准或转向.

### 自动补救范围

> **【拓展：AI SRE 自动修复的安全边界】**AI SRE自动修复的安全边界划分:安全(狭域) 重启Pod、回滚特定部署、在预批准范围内扩展池、启用预批准功能旗──不安全(广域) 更改服务拓、更改资源限制、更改代码、更改IAM、更改数据库──任何声称"设置后就忘了"的供应商都过度承诺安全──集成与AI SRE成熟而扩展,但边界是真实的──2026年最佳实践是:AI 建议、人类批准只允许完全自动化的明确的狭域操作(如Pod 重启)

**Safe (narrow)**:重新启动组,反转特定部署,在预先批准的边界内进行规模积分,启用预先批准的功能旗.

**Not safe (broad)**改变服务拓,修改资源限制,部署新代码,改变IAM,改变数据库.

随着AI SRE的成熟,安全套就会增长,但边界是真实的.

### 逆境评估 (新鸟眼)

两种模型独立分析相同的事件.如果他们同意根源,信心很高.如果他们不同意,升级到人类,两个假设可见.简单的模式,有效的过对幻觉根源.

### 运行内存

团队转换是传统的SRE 部落知识叶片的沉默杀戮.AI SRE在向量DB中存储跑本+死后检测;代理人在每次新事件中获取.当新工程师加入时,AI拥有完整的历史.

### 事件前预测

通过历史记录,GPU温度,API错误模式训练的LLM预测在测试组发生前10-15分钟发生的停机量占89%.

现实检查:没有动机的预测是仪表板. 操作问题是"当我们预测时,我们会做什么?" 预防性排泄? 页面? 自动扩展?

### 2026年产品

- **Datadog Bits AI**在Datadog内部管理了SRE副飞行员.
- **Azure SRE Agent** 蓝色原生.
- **NeuBird Hawkeye**对抗性评估+运行记忆.
- **PagerDuty AIOps**分类+减倍.
- **Incident.io Autopilot**事件指挥官+协调.

### 运行书籍作为代码

> **【拓展：AI SRE 实施路径】**实施建议: 1) 首先将非结构化跑本转换为结构化标记; 2) 实现对抗性评估两个独立模型分析同一事件; 3) 建立操作记忆将进行死后+跑本存入向量DB; 4) 从"AI 建议人类批准"开始,不要直接跳到自主行动; 5) 预事件预测MIT研究显示 10-15 分钟前量,但"预测后做什么"策略定义;

运行簿从"流通"页面发展到有结构化的部分 (症状,假设,验证,行为) 的版本分类.结构化运行簿提供更好的RAG检索.通过将未结构化运行簿转化为结构化,启动任何AI-SRE推广.

### 你应该记住的数字

- 早期检测:89%的停机,10-15分钟的领先时间.
- 多代理分类:监督者+ (日志,指标,运行簿) +人.
- 安全自动补救设置:重新启动,重新部署,在限度范围内扩展.
- 矛盾的评估:两个独立的模型; 协议 = 信心.

## 用它实现框架
```figure
i4-incident-agents
```

## 用它

`code/main.py`模拟多代理分类:日志代理发现错误,测量代理发现CPU尖,运行簿代理匹配已知问题.监督员排列假设.

> `code/main.py`模拟多代理分类:日志代理发现错误,测量代理发现CPU尖,运行簿代理匹配已知问题.监督员排列假设.

> `code/main.py`模拟多代理分类:日志代理发现错误,测量代理发现CPU尖,运行簿代理匹配已知问题.监督员排列假设.

## 运送它.

这一课产生了`outputs/skill-ai-sre-plan.md`鉴于当前的调用,事件数量,团队成熟度,设计了AI SRE部署.

> 本课产出发 `outputs/skill-ai-sre-plan.md`鉴于当前的调用,事件数量,团队成熟度,设计了AI SRE部署.

## 练习题

1. 跑步`code/main.py`如果记录和计量代理人不同意, 监督员怎么解决呢?
   中文翻译:运行 `code/main.py`如果日志和指标代理不同意怎么办?主管如何仲裁?
2. 确定为您服务的三项"安全"自动补救行动.
   中文翻译:为你的服务定义三个"安全"的自动修复操作――为每个提供理由――
3. 编写一个结构化运行簿模板:部分,所需的字段,验证命令.
   中文翻译:编写结构化运行手册模板:章节、必填字段、验证命令──
4. 预测检测火灾12分钟前,你有什么政策?
   中文翻译:预测性检测在 12 分钟提前量触发.
5. 讨论3人团队是否应该在2026年采用AI SRE,或者等待.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## 继续阅读 继续阅读

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
