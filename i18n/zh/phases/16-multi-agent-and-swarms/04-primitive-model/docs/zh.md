# 复杂代理原始模型

> 四个原始,再也没有什么代理,交付,共享状态,管弦仪跨越四维设计空间, 2026年主要的多代理框架 (AutoGen,LangGraph,CrewAI,OpenAI Agents SDK,Microsoft Agent Framework) 是其中的点. 这一课将它们从零构建,运行一个玩具系统,然后将每个主要框架映射到同一轴上,

> **【中文解读】**本节介绍了原始模型多代理系统的最基本构建单元和交互原语.

> **【拓展：primitive model→具体应用】**多 代理 系统的最小原语模型定义了代理之间的基本交互模式:(1) 消息传递 代理 通过发送消息通信;(2) 共享状态 代理 通过阅读写共享存储协调;(3) 事件通知 代理 订阅感兴趣的事件。AutoGen 用消息传递,长度图 用共享状态,黑板系统用事件通知。大多数实际系统混合使用多种原语──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**學本节前请先掌握:第14阶段 (Agent 工程) 、第16阶段·01阶段 (多 Agent 动机) ──本节是第16阶段的核心4个原语(代理/赠款/共享国家/乐团主) 定义所有框架的设计空间──
>  **【类比】**4 原语 = "音乐四件套":代理 (乐手) 、手机 (手机) 独奏接力 (手机) 、共享状态 (总谱) 、管弦乐团 (管弦乐团) ٬指挥) ٬ 车机 (机器) 偏消息传递、长图 偏共享状态、 机组人员 偏角色分工都是四个原语的不同组合──学会原语后看任何新框架都能 1 段话读懂──

## 问题 问题引入

每六个月就会出发一个新的多代理框架. 2023年AutoGen. 2024年CrewAI. 2024年LangGraph和OpenAI Swarm. 2025年4月Google ADK. 2026年2月微软代理框架RC.每份新闻稿都声称是"正确的抽象".

> 每六个月就会发布一个新的多代理框架. 2023年的AutoGen. 2024年的CrewAI. 2024年的LangGraph和OpenAI群.

创新似乎往往是重命名:相同的四个按 (代理,交付,共享状态,编辑器) 具有不同的默认和语法.一旦你看到原始,营销就会掉下来.

> 变化是真实的,但底层原语没有变化. 似乎创新的东西经常是重新品牌化:相同的四个旋律:

如果你试图一次学习它们,你会被烧毁.API看起来不同.文件不同意"代理"是什么.一个框架称共享内存为"黑板",另一个称之为"消息池",第三个称之为"状态图".你开始怀疑该领域只是.

> 如果你试图一个地学习它们,你会筋疲力尽.API看起来不同.

没有.在营销下,四个原始的稳定. 一次学习它们,在一段落中阅读每一个新的框架.

> 实际上并非如此. 在营销下,四个原语是稳定的.

## 概念的核心概念

### 它们是四个原始的.

1. **Agent**系统提示加上工具列表.无状态;每次运行都从系统提示和当前消息历史开始.
   翻译: 中文**Agent** 一个系统提示加上一个工具列表――无状态;每次运行从其系统提示和当前消息历史开始――
2. **Handoff**从一个代理转移到另一个机械上,一个工具调用,返回一个新的代理或一个条件后面的图边.
   翻译: 中文**交接**从一个代理到另一个代理的结构化控制转移――机械地,一个回归新代理的工具调用或遵循条件的图边――
3. **Shared state**任何数据结构,可以读取 (有时写入) 超过一个代理. 信息池,黑板,键值存储,矢量内存.
   翻译: 中文**共享状态** 多个代理可以读取 (有时写入) 的任何数据结构.
4. **Orchestrator**选择:明确图表 (定决),LLM演讲者选择器 (软),最后演讲者传递呼叫 (OpenAI Swarm),或排队时间表 (swarm架构).
   翻译: 中文**编排器**决定谁下一个发言的角色──选项:显式图(确定性)、LLM 发言选择器(软性)、上一个发言人交接调用(OpenAI群) 或队列调调度器(群体架构)──

每个框架都选择每个轴的默认设置,其余部分是表面语法.

> 这就是整个设计空间. 每个框架为每个轴选择默认值. 其余是表面语法.

结果是:没有"最佳"多代理框架.只有"最适合您的任务轴的偏好".一个框架,为确定性管道进行编排 (长图) 是对新兴对话 (使用AutoGen) 错误的.了解您的轴,然后选择.

> 含义:没有"最佳"多代理框架.只有"最适合你的任务轴偏好的"框架. 在确定性流水线上钉住编排的框架.

### 如何每一个2026年框架都将其映射到

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

> 框架 代理 交互 分享状态 编辑器
> 现在,我们在做什么?
> 现在,我们在这个世界里,`Agent(instructions, tools)`工具回复代理调用人问题
> 现在,我们可以在这个地方做一些事情.`ConversableAgent`群众聊天的发言器 信息池 选择器函数
> 现在,我们在做什么?`Agent(role, goal, backstory)`现在,我在做什么?`Process.Sequential / Hierarchical`任务输出链接 管理LLM或静态顺序
> 现在,我们可以看到一个图像,一个图像,一个图像,一个图像.`StateGraph`归结器,确定性
> 微软代理框架 代理 编排模式 模式 特定 线程 / 上下模式 特定
> 现在,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看.

表面的差异看起来很大,下面:相同的四个扣.

> 表面差异看起来很大.

### 为什么这很重要

一旦你看到原始的,框架比较变成一个简短的检查列表:

> 一旦你看到原语,框架比较就变成了一个简单的检查单:

- 调整者是否信任LLM进行路由 (Swarm) 或是将路由编码 (LangGraph)?
  中文翻译:编排器是信任 LLM 来路由(Swarm) 还在代码中固定路由(长图)?
- 共有状态是完整的历史 (GroupChat) 或预测 (StateGraph减小器)?
  中文翻译:共享状态是完整历史?
- 机关可以修改彼此的提示 (CrewAI管理员) 或只交手 (Swarm)?
  中文翻译:代理能否修改彼此的提示?

你停止购买"最好的多代理框架",开始为你真正关心的轴设计.

> 这三个问题回答了80%的哪个框架适合给定的问题――你不再购买"最好的多代理框架",而是开始为你真正关心的轴设计――

如果您已经使用过的框架,请跳过迁移.如果它们在您关心的轴上不同,请评估.大多数新的框架都是重新包装,而不是创新.

> 当2027年新框架发布时,对其运行提出了三个问题. 如果答案与你已经使用的框架相匹配,

### 无国无国的洞察力

任何原始除了共享状态之外都是无状态的. 代理是函数 (提示,工具). 交付是函数调用. 管弦仪是调度器. **The only stateful thing in the system is shared state.**这就是所有有趣的错误的所在:记忆中毒 (课15),消息订单,版本编辑,写作纠纷.

> 除了共享状态外,每个原语都是无状态的.**系统中唯一有状态的东西是共享状态。**这就是所有有趣的错误所在的地方:内存污染 (内存污染)

这种洞察力驱动了调试策略:当多代理系统行为不当时,首先要看共享状态.消息池有毒吗?写字是正确的?该方案是否得到尊重?无国籍代理人很少会导致微妙的错误;共享状态会不断导致它们.

> 这个洞察驱动调试策略:当多个代理 系统行为异常时,首先查看共享状态.消息池是否受到污染?写入顺序是否正确?模式是否遵守?无状态 代理 很少导致微妙的错误;共享状态不断导致它们.

隐藏共享状态的框架 (Swarm) 将问题推向调用者. 集中它的框架 (LangGraph检查点,AutoGen池) 使其可检查,但将协调成本转移到共享状态实现.

> 隐藏共享状态的框架(Swarm) 将问题推向调用者──集中其框架(LangGraph 检查点、AutoGen 池) 使其可检查但将协调成本转移到共享状态实现上──

### 单一原始人的解剖学

#### 代理

```
Agent = (system_prompt, tools, model, optional_name)
```

没有记忆,没有状态,两个具有相同的系统提示和工具的代理人是可替换的,一切看起来像每个代理状态的实际状态是共享状态或交付协议.

> 没有记忆.没有状态. 具有相同的系统提示和工具的两个代理是可互换的. 看起来每个代理状态的一切实际上都在共享状态或交互协议中.

无国有代理人是微不足道的可并行,可重启,可交换的.你可以转换100份相同的代理人,他们都表现得相同.

> 这反直觉但强大:无状态代理可以轻松并行化,重启和替换.你可以启动同一代理的100副本,它们的行为完全相同.

#### 交付

```
Handoff = (from_agent, to_agent, reason, payload)
```

实施的三个主导:

> 三种实现主导地位:

- **Function return**工具返回下一个代理.这是OpenAI群体模式.代理在工具方案中携带路由.
  翻译: 中文**函数返回** 工具返回下一个代理──这是OpenAI群众的模式──代理在其工具模式中携带路由──
- **Graph edge** 兰格拉夫.边缘是声明性的.LLM产生一个值;一个条件选择下一个节点.
  翻译: 中文**图边** 兰格拉夫──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection** AutoGen GroupChat. 选号函数 (有时本身就是一个LLM调用) 阅读游泳池并选择接下来说谁.
  翻译: 中文**发言者选择** 汽车代集团聊天──选择器函数(有时本身就是LLM调用)读取池并选择下一个发言人──

#### 共同国家

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

最少是信息列表.通常更多的是:结构化文物 (CrewAI任务输出),输入文本 (长度图减小器),外部内存 (MCP,向量DB).

> 至少是一个消息列表――通常更多:结构化工件(CrewAI任务输出) 类型化上下文(长图归约器) 外部内存(MCP、向量DB) ⋅

共有状态的形状决定了什么类型的协调是可能的.一个平坦的消息列表使广播变得容易,但角色特定的过很难.一个打字的方案使过变得微不足道,但需要事先设计.没有免费午餐.

> 共享状态的形状决定了什么样的协调可能. 简单的消息列表使广播容易,但角色特定的过难.

两个拓:**full pool**(每个代理都看到每一个消息)**projected**预测的池是规模化的,但需要先前的方案设计.

> 两种拓:**完整池**(每个代理 看到每条消息) 和**投影**投影池可扩展但需要前期模式设计.

#### 乐团主持人

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

它们有四种味道:

> 的风格:

- **Static**图是在构建时间 (长图确定性, CrewAI序列) 固定.
  翻译: 中文**静态**图在构建时固定 (长图 确定性 创建机器人序列)
- **LLM-selected**一个法学士读出游泳池,然后选择下一个讲者 (AutoGen, CrewAI等级).
  翻译: 中文**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI层次) 』
- **Handoff-driven**当前代理通过调用交付工具 (Swarm) 决定.
  翻译: 中文**交接驱动** 当前代理 通过调用交接工具决定(群众) ⋅
- **Queue-driven**从共享队列中拉出工人;没有明确的下一个扬声器 (群众架构,矩阵).
  翻译: 中文**队列驱动** 工作器从共享队列拉取;没有明确的下一个发言人

### 框架之间的变化

一旦原始的定位,剩下的设计决定是:

> 一旦原语固定,剩余的设计决策是:

- **Memory strategy**短暂对耐用检查点 (长图检查点).
  翻译: 中文**内存策略** 临时对持久检查点 (长图检查点)
- **Safety boundary**可以批准转让 (人在循环中).
  翻译: 中文**安全边界**谁可以批准交接?
- **Cost accounting**每位代理的代币预算.
  翻译: 中文**成本核算**每一个代理的代币预算.
- **Observability**追踪传递,持续状态重播.
  翻译: 中文**可观测性**跟踪交接,保持状态以便回放.

它们都可在原始上实现.

> 所有的东西都在原语之上实现.

当一个框架宣传一个"新"功能 (人在循环中,重新尝试,代币预算),检查它是否实际上引入了一个新的原始或只是构成四个.几乎总是后者.四个原始是稳定的;其他一切都是构成.

> 当框架宣传"新"功能时,检查它是否真的引入新原语或只是组合了四种.

## 建立它,实现它.
```figure
a5-primitive-radar
```

## 建立它

`code/main.py`执行四个原始在约150行的Stdlib Python. 没有真正的LLM每个代理都是一个脚本的政策,所以重点仍然是协调结构.

> `code/main.py`用约150行标准库 Python 实现了四种原语.没有真正的 LLM. 每个代理都是一个脚本化策略,使焦点保持在协调结构.

文件出口:

> 文件导出:

- `Agent`一个数据类名称,系统提示,工具,政策功能.
  翻译: 中文`Agent` 名称、系统提示、工具、策略函数的数据类型──
- `Handoff`一个返回新代理的函数.
  翻译: 中文`Handoff` 返回新代理的函数──
- `SharedState`一个安全的线程信息池.
  翻译: 中文`SharedState` 线程安全的消息池
- `Orchestrator`三个变体:`StaticOrchestrator`现在`HandoffOrchestrator`现在`LLMSelectorOrchestrator`它们是的.
  翻译: 中文`Orchestrator` 三种变体:`StaticOrchestrator`,我知道.`HandoffOrchestrator`,我知道.`LLMSelectorOrchestrator`现在,我在做什么?

演示程序通过三个管弦组类型运行相同的三位代理管道 (搜索 -> 写 -> 审查) 并在最后打印了消息池.你可以看到输出仅在 *谁选择下一个* 中不同; 代理和共享状态在运行中相同.

> 演示通过所有三种编排器类型运行相同的三种代理流水线(研究 -> 编写 -> 审阅),最后打印消息池――你可以看到输出只有在*谁选择下一个*上不同;代理和共享状态在所有运行中是相同的――

运行它:

```
python3 code/main.py
```

预期输出:三个管弦乐器运行,每一个模式.每个打印最后的消息池.如果研究人员决定提前完成,转发运行会达到较少的代理人.

> 预期输出:三次编排器运行,每种模式一次――每次打印最终消息池――如果研究员决定提前完成,交互驱动的运行将触及更少的代理 这就是LLM路由权衡的缩影――

## 用它实现框架

`outputs/skill-primitive-mapper.md`通过使用一个新框架版本运行它,才能在阅读文件之前获得一段落的理解.

> `outputs/skill-primitive-mapper.md`是一个技能,读取任何多个代理代码库或框架文档并返回四原语映射. 在新框架发布时运行它,在深入阅读文档之前获得一段式的理解.

## 运送它.

在采用新框架之前,请为它写原始地图.如果您无法,则文件是不完整的,或者框架正在发明第五个原始 (罕见的查找您未见的共享状态口味).

> 在采用新框架之前,为其编写原语映射.如果你做不到,说明文档不完整或框架正在发明第五个原语.

编写地图在您的架构文档中.当新团队成员加入时,请在API文档之前发送地图.当框架版本发生变化时,将地图区分,而不是变更日志.

> 将映射固定在架构文档中. 当新团队成员加入时,在API文档之前发送映射. 当框架版本变化时,对比映射,而不是变更日志.

## 练习题

1. 跑步`code/main.py`观察主管如何改变哪些代理运行.
   中文翻译:用不同的代理 策略运行 `code/main.py`三次――观察编排器选择如何改变哪些代理运行――
2. 执行第四种管弦乐器类型:排队驱动的, 代理人投票分享工作状态.
   中文翻译:实现第四种编排器类型:队列驱动的,代理轮询共享状态获取工作.
3. 根据LangGraph的简单图,我们可以将它写成四个原始图.
   中文翻译:将LangGraph 快速入门改写为四个原语――LangGraph的哪些抽象是 1:1映射,哪些是便利包装器?
4. 阅读OpenAI Swarm的厨师书籍. 确定四种原始物中哪种是最能干的,
   中文翻译:阅读OpenAI Swarm 手册──识别四个原语中 Swarm 使哪个最符合人体工程学,哪个推给调用者──
5. 在这个表中找到一个完全隐藏共享状态的框架. 解释什么是打断的,当代理人需要在传递中协调,而不需要重新阅读历史.
   中文翻译:在表中找到一个完全隐藏的共享状态的框架――解释当代理需要在未重新阅读历史的情况下跨交协协调时会出现什么问题――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## 继续阅读 继续阅读

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents)最清楚的交付驱动的管弦乐
  中文翻译:OpenAI 手册:编排代理  例例和交接 交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/)集团聊天+演讲者选择是LLM选择的管弦乐队的参考
  中文翻译:AutoGen 稳定文档  群众聊天 + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)图边管弦和基于减小器的共享状态
  中文翻译:长图 工作流和代理 图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction)角色目标背景经纪人,序列/层次流程
  中文翻译:CrewAI 介绍  角色-目标-背景故事 代理,序列/层次流程
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2)微软将0.4转移到维护后的AutoGen v0.2直播线
  中文翻译:AG2(社区AutoGen 延续)  微软将 v0.4 移入维护后的活跃AutoGen v0.2 线
