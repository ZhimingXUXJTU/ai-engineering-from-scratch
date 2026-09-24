# 生产运行时间:排队,事件,时间

> 制作代理运行在六种运行时间形状上:请求响应,流媒体,耐用执行,排队背景,事件驱动和计划. 在选择框架之前选择形状.可观测性在每个形状上承载.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:阶段14·13(长图) 状态图基础;阶段17(基础设施和生产) 本节是其前置概念,深入生产部署看阶段17 全部。

## 学习目标

- 列出六种生产运行时间形状,并将每一种形状与框架/产品模式相匹配.
- 解释为什么长期执行 (长图) 对长期任务很重要.
- 描述活动驱动的运行时间以及Claude Managed Agents适合时.
- 解释多步骤剂的可观测量载荷承载要求.

## 问题 问题引入

制作代理在Jupyter笔记本书不出现的方式失败:在第37步时,网络时间停止,用户在中音调中挂,机器重启时,cron工作会死亡,背景工作者会失去内存.运行时间的形状决定了哪些故障是可存活的.

> 生产代理的失败方式是 Jupyter 笔记本无法表现:第37步的网络超时,用户在语音通话中途挂,定时任务在机器重启时死亡,后台工作器内存不足.


> **【中文解读】**生产环境 运行时需要处理开发环境不需要的问题:持久化状态、容错恢复、水平扩张、速度限制、成本控制和可观测性――选择运行时(长度图、时间、自建) 取决于任务的关键性和预算――

>  **【类比】**运行时 = 6种交通工具:**request-response**租车一次一结,最简单);**streaming**车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车车**durable execution**车房间,睡觉醒来继续开放,长图检查站);**queue-based**们都在着.**event-driven**其他公司的公司,**scheduled**任务多长多复杂决定选择哪个

> ️ **【易错点】**运行时选错的3个坑:(1) **长任务用 request-response**3 小时任务挂 HTTP 请问,nginx 60s 超时切断;用耐用执行(长度图) + 后台轮询――(2) **observability 当可选**上线后发现"不知道为失败";从第一天就接着兰格斯/兰格史密斯,每个工具调用都追踪――(3) **没做 graceful shutdown**服务重启时执行任务直接死亡;使用SIGTERM 子保存检查点,重启后从检查点继续运行.

> **{【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】}**2026年生产代理运行时的选择: 1) LangGraph CloudLangGraph的托管服务,内置状态检查点和重放; 2) 临时通用工作流引擎,配合AI SDK可构建持久化代理; 3) 自建基于Redis/Kafka的消息队列 + 自定义代理循环.
## 概念的核心概念

### 要求-回应

- 用户等待完成.
- 只有短任务 (<30s) 实现.
- 堆:Agnó (Python + FastAPI),Mastra (TypeScript + Express/Hono/Fastify/Koa).
- 观察性:标准HTTP访问日志 + OTel跨度.

### 流媒体

- 通过 SSE 或 WebSocket进行渐进输出.
- 现场开户将此扩展到WebRTC语音/视频 (课2)
- 堆:任何有流媒体支持的框架+处理SSE/WS的前端.
- 观察性:每分钟时间,第一代标的延迟,尾声延迟.

### 持续执行

- 检查站每一步后,自动恢复失败.
- 机器人v0.4演员模型将失败分离为一个代理 (课 14).
- 长度图的核心分辨器 (课13).
- 基本的情况是, 步骤数量不清楚, 恢复成本高.

### 基于队列/背景

- 工作人员接待,结果通过网页或酒吧/潜水艇回流.
- 对于长视线代理 (每项任务的几十到数百步,根据人类计算机使用公告)
- 堆:菜 (Python),BullMQ (节点),SQS + Lambda (AWS),定制.
- 观察性:排队深度,每工作延迟分布,DLQ大小.

### 事件驱动

- 代理人会订阅触发器:新电子邮件,公关开,时间火.
- 克劳德管理代理人 (Claude Managed Agents) 解释了这一点 (课17).
- 工作人员AI流程 (课 15) 构建基于事件的确定性工作流程.
- 观察性:触发源,事件到启动延迟,代理延迟.

### 时间表

- 时间表的代理.
- 结合耐用执行,以使每晚一次失败的运行重启下一次.
- 堆: Kubernetes CronJob + 持久框架; 主机 (Render cron, Vercel cron).

### 2026部署模式

- **CrewAI Flows**对于活动驱动的生产.
- **Agno**无国有的Python微服务FastAPI.
- **Mastra**服务器适配器 (Express,Hono,Fastify,Koa) 用于嵌入.
- **Pipecat Cloud / LiveKit Cloud**对于管理声音 (课2)
- **Claude Managed Agents**对于长期运行的主机异步.

### 可观测性是承载性

没有OpenTelemetry GenAI跨度 (课3) 加上Langfuse/Phoenix/Opik后端 (课24),你不能调试40步失败的多步骤代理.这不是生产的选择性.这是"我们快速调试"和"我们从零开始重复,更多的记录".

> 没有OpenTelemetry GenAI跨度 ((第23课) 加上Langfuse/Phoenix/Opik后端 ((第24课),你不能调试在第40步失败的多步代理――这对生产环境是不可选的――这是"快速调试"和"从头重放并添加更多日志"之间的区别――

> 生产运行时处理 代理部署,扩张和可靠性.

### 生产运行时间失败

- **Wrong shape choice.**选取5分钟的任务的请求-响应.用户挂了电话,工人堆积了,重复试验复杂.
- **No DLQ.**没有死字的员工排队,失败的工作消失.
- **Opaque background work.**后台代理运行,没有出口痕迹. 失败是不可见的,直到用户报告它们.
- **Skipping durable state.**任何运行超过30秒,你无法再启动的运行需要持久的执行.

> **错误的形态选择。**为 5 分钟任务选择请求-响应――用户挂断;工作器堆积;重试叠加――
> **没有 DLQ。**队列工作器没有死信队列――失败的任务消失――
> **不透明的后台工作。**后台 运行没有追踪导出. 失败不可见直到用户报告.
> **跳过持久化状态。**任何超过30秒的无法承受重启运行都需要持续执行.

## 建立它,实现它.
```figure
wb-runtime-shapes
```

## 建立它

`code/main.py`是一个多形体现式的 stdlib:

- 要求响应终端点 (平函数).
- 流动处理器 (发电机).
- 排队员,有DLQ.
- 事件触发程序.
- 时间表表表.

运行它:

```bash
python3 code/main.py
```

输出:五个痕迹显示每个形状的行为在同一任务上.相同的代理逻辑,不同的外层.持续执行 (第六个形状) 是故意在13课中通过LangGraph检查点覆盖的.

> 输出:五种追踪显示每个形式在同一任务上的行为――相同的代理逻辑,不同的外──持久化执行――第六种形态) 有意在第十三课中通过LangGraph 检查点覆盖――

> 生产运行时处理 代理部署,扩张和可靠性.

## 用它实现框架

- **Request-response**对于聊天式的UX.
- **Streaming**对于渐进的反应.
- **Durable**对于长远任务.
- **Queue**对于批量/异步/长期使用.
- **Event**对于代理反应性.
- **Cron**对于家庭管理 (内存整合,评估,成本报告).

## 运送它.

`outputs/skill-runtime-shape.md`选择一个任务的运行时间形状,并线索可观测性要求.

> `outputs/skill-runtime-shape.md`为任务选择一个运行时形态并连接可观测性要求.

> 生产运行时处理 代理部署,扩张和可靠性.

## 练习题

1. 根据你的学习方法,你需要在一个模型中找到一个模型.
  中文翻译:思考并实践此练习──
2. 加入一个DLQ到排队的演示. 模拟10%的失败工作;表面DLQ大小.
  中文翻译:思考并实践此练习──
3. 写一个 cron-触发的评估代理, 每晚都会对照你当天的前20个痕迹.
  中文翻译:思考并实践此练习──
4. 执行反压的流媒体:如果客户端缓慢,请暂停代理.
  中文翻译:思考并实践此练习──
5. 你什么时候会把一个自主主持的长视线代理转移到管理?
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Request-response | "Synchronous" | User waits; short tasks only |  |
| Streaming | "SSE / WS" | Progressive output; better UX; latency observable per chunk |  |
| Durable execution | "Resume from failure" | Checkpointed state; restart at last step |  |
| Queue-based | "Background jobs" | Producer / worker pool / DLQ |  |
| Event-driven | "Trigger-based" | Agent reacts to external events |  |
| DLQ | "Dead-letter queue" | Parking lot for failed jobs |  |
| Claude Managed Agents | "Hosted harness" | Anthropic-hosted long-running async with caching + compaction |  |

## 继续阅读 继续阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)持续执行细节
  中文翻译:见原文.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)长期的主机异步
  中文翻译:见原文.
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) "每项任务每次的几十到数百步"
  中文翻译:见原文.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)演员模型故障隔离
  中文翻译:见原文.
