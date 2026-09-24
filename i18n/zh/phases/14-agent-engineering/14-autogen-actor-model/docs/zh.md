# 机器人模型和代理框架
# 代理人的演员模式 异步消息和类型的运行时间

> 代理作为演员:异步消息交换,事件驱动处理器,故障隔离,自然同步性.AutoGen v0.4 (微软研究,2025年1月) 重新设计了围绕该模型的代理配套;框架现在处于维护模式,微软代理框架 (公众预览2025年10月) 作为其生产继任者.

> **【中文解读】**周围的演员模型重新设计了代理编排.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 描述演员模式:代理人作为演员,信息作为唯一的IPC,每演员的失败隔离.
  中文翻译:描述演员 模型:代理 作为演员,消息作为唯一的进程间通信,每个演员 独立故障隔离――
- 给AutoGen v0.4的三个API层命名 核心,代理聊天,扩展 ,每个层是什么.
  中文翻译:说出AutoGen v0.4的三个API层Core、AgentChat、扩展及各自的用途──
- 解释为什么分离处理信息的传输使得故障隔离和自然的同时发生.
  中文翻译:解释为什么将消息传递与处理解能带来故障隔离和自然并发.
- 在Python中实现一个 stdlib演员运行时间,并将两个代理代码审查流入其中.
  中文翻译:用Python 标准库实现 Actor 运行时并将双代理 代码审查流程移植到其上──

## 问题 问题引入

大多数代理框架是同步的:一个代理生产,一个代理消费,在电话堆中.失败崩堆. 交互是接的. 分布需要重写.

> 大多数代理框架是同步的:一个代理生产,一个代理消费,在调用中──失败会使崩──并发是后加的──分布式需要重写──

机器人4.4的答案:演员模型.每个代理是一个有私人收件箱的演员. 消息是唯一的交互. 运行时间分离交付与处理. 失败隔离到一个演员. 竞争是本土的. 分布只是不同的运输.

> 机器人4.4的答案:演员模型――每个代理是一个带私有收件箱的演员――消息是唯一的交互方式――运行时将交付与处理解――失败分离到一个演员――并发是原生――分布式只是不同的传输方式――

> **【中文解读】**通过传递通信,每个代理是独立的异步演员. 这与兰格拉夫的图模型或CrewAI的角色模型不同.

> **【拓展：AutoGen 的演进】**通过不同步骤的消息传递协作,自动生成是一个重大重构. 从v0.3的对话模式转向演员模型,灵感来自Erlang/Akka的并发模型.

>  **【前置】**必须先掌握:阶段14·01(代理循环) 和阶段14·12 ((人类工作流程模式) 本节是这些模式在"并发场景"下延伸. 还需要"演员模型"的基本概念.

## 概念的核心概念

### 演员

一个演员有:

> 一个演员有:

- 个人国家 (从外面直接接触的).
  中文翻译:私有状态 (私有状态)
- 收件箱 (消息队列).
  中文翻译:收件箱
- 管理者:`receive(message) -> effects`效果可以是"回复","向其他演员发送","新演员发射","更新状态","停止自我".
  中文翻译:处理器:`receive(message) -> effects`效果可以是"回复"",发送给其他演员"",创建新演员"",更新状态"",停止自己"――

两个演员不能分享记忆,他们只能发送信息.

>  **【类比】**演员像办公室里互不见的同事:每个人都有自己的工位 (私有状态) 和收件箱 (收件队列) ⋅你想让同事帮忙,不能直接翻他的工位 (共享内存),只能发邮件 (发消息) ⋅同事处理完邮件可能回信 (回复) ⋅转发给另一个人 (发给另一个人) ⋅招生生 (招生) ⋅生 (发新演员) ⋅**关键**没有影响其他人.

> 两个演员不能分享内存.

### 在AutoGen v0.4中,有三个API层
### 三个API层

机器人4.0将其表面分为三个:

1. **Core.**低级演员框架. `AgentRuntime`现在`Agent`现在`Message`现在`Topic`基于事件的异步消息交换.
   翻译: 中文**Core。**底层演员框架`AgentRuntime`,我知道.`Agent`,我知道.`Message`,我知道.`Topic`异步消息交换,事件驱动.
2. **AgentChat.**基于任务的高级API (替代了v0.2的可转换代理). `AssistantAgent`现在`UserProxyAgent`现在`RoundRobinGroupChat`现在`SelectorGroupChat`现在,我们要去.
   翻译: 中文**AgentChat。**任务驱动的高级API(替代了V0.2的可对话的代理)`AssistantAgent`,我知道.`UserProxyAgent`,我知道.`RoundRobinGroupChat`,我知道.`SelectorGroupChat`,我知道.
3. **Extensions.**集成 OpenAI,人类,Azure,工具,内存.
   翻译: 中文**Extensions。**集成 OpenAI、人类、蓝色、工具、记忆──

### 为什么分离关系很重要

在v0.2模型中,调用`agent_a.chat(agent_b)`在v0.4中, 除了除了除了除了除了除了除.`send(agent_b, msg)`运行时间后会传递.

> 在 v0.2 模型中调用`agent_a.chat(agent_b)`在4.0中,`send(agent_b, msg)`将消息放入代理_b的收件箱并返回.运行时稍后交付.

- **Fault isolation.**运行时间抓住B的处理器失败,决定要做什么 (登录,重新尝试,死字母).
  翻译: 中文**故障隔离。**机器B 崩不会导致机器A 崩运行时在B的处理器中捕获故障并决定做什么 (日志、重试、死信) ⋅
- **Natural concurrency.**许多消息同时飞行;演员同时处理收件箱.
  翻译: 中文**天然并发。**多条消息同时传输;演员并发发处理它们的收件箱.
- **Distribution-ready.**收件箱+运输是同一抽象,无论演员是正在进行或在另一个主机上.
  翻译: 中文**分布式就绪。**收件箱+传输是相同的抽象,无论演员在过程中还是在另一个主机上.

> ️ **【易错点】**演员的模型,但忘记了"消息必须可序列化".**后果**据悉,在此次的发布中,**一行修复**所有消息必须使用pydantic/dataclass/JSON-schema定义,禁止传传 lambda、文件句柄、数据库连接等不可序列化对象──

### 拓物

- **RoundRobinGroupChat.**代理人轮流在固定转变.
  翻译: 中文**RoundRobinGroupChat。**经纪人按固定轮换顺序轮流.
- **SelectorGroupChat.**选手根据对话背景选择下一个选手.
  翻译: 中文**SelectorGroupChat。**选择器 根据对话上下文选择下一个发言人──
- **Magentic-One.**参考多代理团队用于浏览网页,执行代码,处理文件.
  翻译: 中文**Magentic-One。**基于 AgentChat 构建的文件处理.

### 可观察性

每个消息发射一个跨度;工具调用携带`gen_ai.*`根据2026年OTel GenAI语义公约的属性 (课23).

> 电信支持内置. 每条消息发出一个跨度.`gen_ai.*`属性,符合2026年 OTel GenAI 语义约定(第 23 课) ⋅

### 状态:维护模式

2026年初:AutoGen v0.7.x为研究和原型设计而稳定.微软已将主动开发转移到微软代理框架,生产后代 (公众预览2026年10月1日; 1.0 GA是2026年1季度末的目标).AutoGen模式将清洁地推进.

```figure
actor-mailbox
```

>  **【困惑】**答:学"演员模型"这个节目思想,但**别在生产上选 AutoGen**原因:(1) 微软已转向微软代理框架(MAF),AutoGen 不再获得新特性;(2) 演员模型本身是个个**经久不衰的分布式设计思想**(来自1973年休伊特论文,比 LLM老50年),理解它对你评估MAF、Erlang、Akka、Ray都有帮助.把AutoGen当"教材",把MAF或LangGraph当"生产工具".

> 2026年初:AutoGen v0.7.x 在研究和原型开发方面稳定.微软已将积极发展转移到微软代理框架.

## 动手构建

`code/main.py`执行一个STDlib演员运行时间:

> `code/main.py`用标准库实现了演员运行时:

- `Message` 输入用荷`sender`现在`recipient`现在`topic`现在`body`现在,我们要去.
  翻译: 中文`Message`带`sender`,我知道.`recipient`,我知道.`topic`,我知道.`body`带类型的载荷.
- `Actor`抽象的`receive(message, runtime)`现在,我们要去.
  翻译: 中文`Actor`带`receive(message, runtime)`抽象类型
- `Runtime`事件循环与共享队列,交付,故障隔离.
  翻译: 中文`Runtime`带共享队列,递交,故障隔离事件循环.
- 两个演员演出:`ReviewerAgent`审查代码`ChecklistAgent`它们交换信息,直到达成一致.
  中文翻译:双演员演示:`ReviewerAgent`审查代码,`ChecklistAgent`运行检查清单;它们交换消息直到达成共识.

运行它:

> 运行:

```
python3 code/main.py
```

痕迹显示了消息传递,一个演员的模拟失败,

> 轨迹显示消息传递,一个演员的模拟故障不会导致另一个崩,以及共享裁决的收获.

## 用它实现框架

- **AutoGen v0.4/v0.7**稳定研究,原型制造,多代理模式.
  翻译: 中文**AutoGen v0.4/v0.7**研究、原型、多代理 模式稳定──
- **Microsoft Agent Framework**前进道路;相同的演员模式想法在更新的API中.
  翻译: 中文**Microsoft Agent Framework**演员 模型理念:
- **Microsoft Agent Framework**生产后代 (2025年10月公开预览);相同的演员模型想法在更新的API中.
- **LangGraph swarm topology**通过分享工具的交付, 类似的模式.
  翻译: 中文**LangGraph 群体拓扑**通过共享工具移交的类似模式.
- **Custom actor runtime**需要特定的运输 (NATS,RabbitMQ,gRPC).
  翻译: 中文**自定义 Actor 运行时**当你需要特定传输时.

## 运送它.

`outputs/skill-actor-runtime.md`生成一个最小的演员运行时间加上一个团队模板 (RoundRobin或 Selector) 为给定的多代理任务.

> `outputs/skill-actor-runtime.md`为给定多个代理 任务生成最小演员 运行时加团队模板(RoundRobin或选择器) ⋅

## 练习题

1. 加入一个死字母队列:当一个操作员提升时, 停留失败信息的人类检查.
   中文翻译:添加死信队列:当处理器抛出异常时,将失败消息停放为人工检查.
2. 实施`SelectorGroupChat`选择器选择了根据对话状态处理下一个信息的演员.
   中文翻译:实现`SelectorGroupChat`根据对话状态选择谁处理下一条消息──
3. 增加分布式运输:将过程中的队列换为JSON-over-HTTP服务器,以便参与者可以在单独的过程中运行.
   中文翻译:添加分布式传输:将进程内队列替换为JSON-over-HTTP 服务器,使 Actor可以在独立进程中运行。
4. 输出每条消息的 OTel 跨度 (或无操作替代).`gen_ai.agent.name`现在`gen_ai.operation.name`根据第23课.
   中文翻译:为每条消息连接 OTel span(或无运转 替代) 按第 23 课发出 `gen_ai.agent.name`,我知道.`gen_ai.operation.name`,我知道.
5. 阅读AutoGen v0.4的架构帖子.`autogen_core`你在生产中错过了什么?
   中文翻译:阅读AutoGen v0.4的架构文章.`autogen_core`你跳过了什么重要的生产?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## 继续阅读 继续阅读

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)重新设计的位置
  中文翻译:AutoGen v0.4 微软研究院重新设计文章。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)图形替代品
  中文翻译:长图图 概览 图形替代方案──
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) 跨度自动生成默认发射
  中文翻译:开放电气基因 语义约定AutoGen默认发射跨度──
