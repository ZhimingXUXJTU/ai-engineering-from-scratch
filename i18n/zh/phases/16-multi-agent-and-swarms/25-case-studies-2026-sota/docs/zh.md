# 案例研究和2026年最先进的情况

> 对于研究的结尾到结尾,每一个都说明了多代理工程的不同部分. **Anthropic's Research system**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**MetaGPT / ChatDev**(软件工程的SOP编码角色专业化;ChatDev的"沟通性幻觉化";通过DAG扩展到1000个代理, arXiv:2406.07155) 是正规的角色分解案例. **OpenClaw / Moltbook**(原本由彼得·斯坦伯格 (Peter Steinberger) 命名为Clawdbot,2025年11月;两次改名;2026年3月247万个GitHub星;本地ReAct-loop代理;Moltbook作为一个仅供代理商使用的社交网络,在发行几天内拥有约2.3万个代理账户,Meta收购2026-03-10) 说明了人口规模发生的事情:新兴的经济活动,即时注射风险,国家级监管 (中国限制了OpenClaw在政府计算机上,2026年3月).**Framework landscape April 2026:**兰格拉夫和克鲁艾的首席生产;AG2是社区的AutoGen延续;微软的AutoGen处于维护模式 (融入微软代理框架,RC Feb 2026);OpenAI代理SDK是生产Swarm的继任者;谷歌ADK (4月 2025) 是A2A原生参与者. 现在每个主要框架都提供MCP支持;大多数都提供A2A. 这一课将每个案例都读完, 并将常见的模式进行分析,

> **【中文解读】**本节介绍了2026年SOTA多代理案例研究最新最佳多代理系统分析

> **【拓展：case studies 2026 sota→具体应用】**2026年 SOTA多代理 系统案例: 1) 人类研究的克劳德多代理 协作进行深入研究; 2) OpenAI的Codex多代理 协作编码; 3) 微软的AutoGen团队多代理 软件开发.


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**本节是第十六阶段 收官课,整合 01-24 所有内容──三级生产案例:人类研究 (Anthropic Research) 监督者 典范) ‧MetaGPT/ChatDev (角色分工典范) ‧OpenClaw/Moltbook (Moltbook) 群体规模涌现典范) ‧
>  **【类比】**三个案例 = "三种规模多代理社会"――人类研究= 精小队,10个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP编码);OpenClaw/Moltbook = 城市级社会(百万个代理 涌现经济、被政府监管) ・2026 框架格局:长图 + 员工AI 领跑生产、AG2 接 AutoGen微软 已合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生、
**Time:** ~90 minutes | **时间:** ~90 分钟

## 问题 问题引入

复合代理工程是一个年轻的学科. 制作参考数量很少,每个产品都涵盖了不同的空间. 读一读一读是有用的;比较它们作为一组更有用. 这一课将三项可信的2026例证作为一个完整的阅读列表, 入了共同的模式,

> 多代理工程是一个年轻的学科.生产参考很少,每个覆盖空间的不同部分.逐一阅读是有用的;作为一个集合比较更有用. 本课将将三项规范的2026年案例研究作为端到端阅读清单,确定共同模式,并映射框架景观,让你能够基于知识而不是营销做框架选择.

## 概念的核心概念

### 人类研究系统

制作监督员工案例. 克劳德·奥普斯4计划和合成; 克劳德·索内特4副主题研究并行. 发表工程帖子: https://www.anthropic.com/engineering/multi-agent-research-system.

关键测量结果:

> 关键测量结果:

- **+90.2%**内部研究评估的单剂Opus 4的改善.
  中文翻译:在内部研究评估上比单 Agent Opus 4 提升 **+90.2%**,我知道.
- **80% of BrowseComp variance**解释**token usage alone**多代理主要因为每个子代理得到一个新的背景窗口.
  翻译: 中文**80% 的 BrowseComp 方差**仅由**token 使用量**解释多 代理 胜出主要因为每个子代理 获得新的上下文窗口.
- **15x tokens per query**对于单人代理.
  中文翻译:每查询 **15 倍 token**对于单个代理人.
- **Rainbow deployment**因为代理人是长期的,有权力.
  翻译: 中文**彩虹部署**因为代理是长时间运行和有状态的.

设计课程编码:

> 编码化的设计教训:

1. **Scale effort to query complexity.**简单 → 1 个代理,有 3-10 个工具调用. 中等 → 3 个代理. 复杂的研究 → 10+ 个子代理.
   翻译: 中文**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**子做广泛的搜索;子合成; 后续的子做针对的深度.
   翻译: 中文**先广后窄。**代理做广泛搜索; 主代理综合;后续代理做定向深挖──
3. **Rainbow deploys.**保持旧运行时间版本活着,直到他们的飞行员完成.
   翻译: 中文**彩虹部署。**保持旧运行时版本活跃直到正在进行的代理完成.
4. **Verification is not optional.**系统没有明确的验证器作用.
   翻译: 中文**验证不是可选的。**系统在没有明显验证者的角色时被观察到产生幻觉.

这就是生产规模的监督员工拓 (阶段16 · 05) 的参考案例.

### 转载数据

产品SOP角色分解案例. 覆盖 arXiv:2308.00352 (MetaGPT) 和 arXiv:2307.07924 (ChatDev).

编码软件工程SOP作为角色提示:产品经理,建筑师,项目经理,工程师,QA工程师.`Code = SOP(Team)`每个角色都有一个狭窄的专业提示; 角色间交换都包含结构化文物 (PRD文件,建筑文件,代码).

德夫的贡献: **communicative dehallucination**设计人员在设计UI之前向程序员询问该语言是什么,而不是猜测. 这一报告报告显示,多代理管道中的幻觉可测量.

现在,MacNet (arXiv:2406.07155) 扩展了ChatDev到**>1000 agents via DAGs**每个DAG节点都是角色专业化;边缘编码交换合约. 规模是可能的,因为路由是明确的和离线计算.

设计课程:

> 设计教训:

1. **Structure matters more than size.**紧密的五角色的SOP团队击败了50名非结构化团队.
   翻译: 中文**结构比规模更重要。**紧的5个角色SOP团队胜过50个代理的非结构化组.
2. **Handoff contracts in writing.**角色之间传递的文物遵循一个方案.
   翻译: 中文**书面交接契约。**角色间传递的制品遵循模式.
3. **Communicative dehallucination**它们是便宜的,承载的模式.
   翻译: 中文**交际去幻觉**这是一种廉价的模式.
4. **DAGs scale further than chat.**当流量可识别时,将其编码.
   翻译: 中文**DAG 比聊天扩展更远。**当流程可知时,编码它.

这就是角色专业化 (16 · 08) 和结构化拓学 (16 · 15) 的参考案例.

### 开关/Moltbook生态系统

产量人口规模的情况.

- **Nov 2025:**鱼 (Peter Steinberger的当地ReAct循环编码代理) 舰船.
- **Dec 2025 – Mar 2026:**改名为两次 (Clawdbot → OpenClaw →继续在 OpenClaw 下).
- **Feb 2026:**马尔特本作为一个只代理的社交网络,
- **Mar 2026 (2026-03-10):**梅塔收购了Moltbook.
- **Mar 2026:**中国限制了OpenClaw的政府计算机.
- **Mar 2026:**开关跨越了247万个GitHub星星.

它们是多元代理的,

- **Emergent economic activity.**代理商通过代币支付购买,销售和服务.
- **Prompt-injection risks at population scale.**病毒代理的一个恶意提示在几个小时内传播到成千上万的代理对代理的互动.
- **State-level regulatory response.**几个星期后, 监管进入生态系统.

设计的教训是部分技术,部分治理:

1. **Multi-agent at population scale is a new regime.**个人系统最佳实践 (验证,角色清晰度) 仍然适用,但不足.
2. **Prompt injection is the new XSS.**默认情况下,将代理人的个人资料和跨代理信息视为不可信赖的输入.
3. **Regulation is faster than design cycles.**计划一下.
4. **Open-source + viral scale compounds.**射4个月的247万颗星星是不寻常的;

看到[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)对于技术基础,Clawdbot / OpenClaw存储库揭示了本地ReAct循环;Moltbook的公开帖子显示了社交图架构.

### 框架景观2026年4月

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

现在每个主要框架都在运输.**MCP**支持;大多数船**A2A**协议兼容性不再是区别因素.

### 在所有三个案件中,

1. **Orchestrator + workers**(人类明确监督者,MetaGPT PM-as-supervisor,OpenClaw个体代理 +网络效应).
   翻译: 中文**编排者 + 工作者**                                                                                                                                                                                                                                                              
2. **Structured handoff contracts**(人类的子基任务描述,MetaGPT PRD/架构文件,OpenClaw A2A文物).
   翻译: 中文**结构化交接契约**据了解,在此次的调查中,
3. **Verification as first-class role**(Anthropic的验证器,MetaGPT的QA工程师,OpenClaw的网络验证器).
   翻译: 中文**验证作为一等角色**技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持: 技术支持
4. **Scaling is topology + substrate, not just more agents**(彩虹部署,MacNet DAGs,人口规模基板).
   翻译: 中文**扩展是拓扑 + 基底，不仅是更多 Agent**据报道, 据报道,
5. **Cost is material and disclosed**对于每一个角色的预算,Moltbook的交互价格.
   翻译: 中文**成本是实质性的且已披露**据报道,该公司的资产额为5倍.
6. **Security posture is explicit**(人类的沙盒,MetaGPT的角色限制,OpenClaw的即时注射作为已知攻击表面).
   翻译: 中文**安全态势是显式的**(人类的沙盒,MetaGPT的角色限制,OpenClaw的提示注入作为已知攻击面)

### 选择下一个项目参考

- **Production research / knowledge task → Anthropic Research.**新文本的子集赢了.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**角色+SOP+交换合同
- **Network-effect social product → OpenClaw / Moltbook.**基层+新兴经济.
- **Classic enterprise automation → CrewAI or LangGraph**(生产领导者,稳定运行时间).

### 2026年最新总结

在2026年4月的场地:

- **Frameworks are converging.**支持MCP+A2A是桌面投注. 交换语义是剩下的设计选择.
- **Evaluation is hardening.**现在的防污现实检查.
- **Production failure rates are measurable**现实MAS的比例为41%-86.7%,
- **Cost is the central engineering constraint.**代币成本每任务,墙钟每交互,彩虹部署的上海费用.多代理赢得准确性,但损失成本,交易是商业决定.
- **Regulation is a near-term input, not a background concern.**司法管辖区的速度比个体部署周期更快.

## 用它使用方法
```figure
a5-orchestrator-scale
```

## 用它

`outputs/skill-case-study-mapper.md`是阅读拟议的多代理系统设计并将其映射到最近的案例研究中,并将已经测试的案例研究的设计决定呈现出来.

## 发射上线

2026年生产多代理的初步规则:

- **Start from a case study, not from scratch.**选择最接近的人类研究/ MetaGPT/ OpenClaw 的方法,并适应.
  翻译: 中文**从案例研究开始，不是从零开始。**选择最接近的人类研究 / MetaGPT / OpenClaw 并适配
- **Adopt MCP + A2A.**跨框架的可移植性是有价值的;协议支持是免费的.
  翻译: 中文**采用 MCP + A2A。**跨框架可移植性有价值;协议支持是免费的.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**检测到是受污染的.
  翻译: 中文**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**已被污染的情况已被验证
- **Pay the verification tax.**独立验证器的成本是您的代币预算的20-30%,并且可以测量准确度.
  翻译: 中文**支付验证税。**独立验证器花费约20-30%的代币预算,换取可测量的正确性.
- **Rainbow deploy long-running agents.**预计多小时的代理运行将是常规的.
  翻译: 中文**彩虹部署长时间运行 Agent。**预期多小时 运行是常规的.
- **Read WMAC 2026 and the MAST follow-ups.**纪律正在迅速发展.
  翻译: 中文**阅读 WMAC 2026 和 MAST 后续。**这个学科正在快速发展.

## 练习题

1. 阅读人类研究系统的完整内容. 确定如果您将Opus 4取代于较小的模型 (例如,海库 4) 改变的三个设计决定.
2. 阅读 MetaGPT 第3-4节 (arXiv:2308.00352).从您自己的域名 (而不是软件) 编码一个SOP作为角色提示.SOP意味着多少角色?
3. 查看ChatDev (arXiv:2307.07924). 确定"沟通性幻觉"的机制.
4. 阅读OpenClaw和Moltbook. 选择一个特定的失败模式,在人口规模上出现,
5. 选择您目前的多代理项目. 在三个案例研究中,哪个是最接近参考?从该案例研究中,您尚未采取哪些设计决定? 写下您将在本季度采取的一个.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## 继续阅读 继续阅读

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)监督工人的生产参考
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) SOP作用分解
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924)沟通性幻觉
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) DAG基础的规模
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)生态系统概况
- [WMAC 2026](https://multiagents.org/2026/)AAAI2026年多代理协调桥梁计划研讨会
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents)生产领导者
- [CrewAI docs](https://docs.crewai.com/en/introduction)基于角色的框架
