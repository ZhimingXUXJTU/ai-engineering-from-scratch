# 多 Agent 原始模型 | 多 Agent 原始

> 2026 年出货的每个多 Agent 框架——AutoGen、LangGraph、CrewAI、OpenAI Agents SDK、Microsoft Agent Framework——都是四维设计空间中的一个点。四个原语，仅此而已：Agent、交接、共享状态、编排器。本课从零构建它们，在所有四个上运行一个玩具系统，然后将每个主要框架映射到相同的轴上，这样你就可以用一段话读懂任何新发布的框架。

> **【中文解读】** 本节介绍了原始模型——多 Agent 系统的最基本构建单元和交互原语。

> **【拓展：primitive model→具体应用】** 多 Agent 系统的最小原语模型定义了 Agent 之间的基本交互模式：(1) 消息传递——Agent 通过发送消息通信；(2) 共享状态——Agent 通过读写共享存储协调；(3) 事件通知——Agent 订阅感兴趣的事件。AutoGen 用消息传递，LangGraph 用共享状态，黑板系统用事件通知。大多数实际系统混合使用多种原语。


**类型：** 学习
**语言：** Python（标准库）
**前置条件：** 第 14 阶段（Agent 工程），第 16 阶段 · 01（为什么需要多 Agent）
**时间：** ~60 分钟

## 问题引入

每六个月就有新的多 Agent 框架出货。2023 年的 AutoGen。2024 年的 CrewAI。2024 年的 LangGraph 和 OpenAI Swarm。2025 年 4 月的 Google ADK。2026 年 2 月的 Microsoft Agent Framework RC。每个新闻稿都声称是"正确的抽象"。

如果你试图一个一个地学习它们，你会耗尽精力。API 看起来不同。文档对"Agent"是什么意见不一。一个框架把共享记忆叫"黑板"，另一个叫"消息池"，第三个叫"StateGraph"。你开始怀疑这个领域只是在空转。

不是的。在营销之下，四个原语是稳定的。学一次，一段话读懂每个新框架。

## 核心概念

### 四个原语

1. **Agent** — 系统提示词加工具列表。无状态；每次运行从其系统提示词和当前消息历史开始。
2. **交接 (Handoff)** — 从一个 Agent 到另一个的结构化控制转移。机械上，是一个返回新 Agent 的工具调用或遵循条件的图边。
3. **共享状态 (Shared state)** — 多个 Agent 可以读取（有时写入）的任何数据结构。消息池、黑板、键值存储、向量记忆。
4. **编排器 (Orchestrator)** — 决定谁下一个发言的角色。选项：显式图（确定性）、LLM 发言选择器（软性）、上一个发言者的交接调用（OpenAI Swarm），或队列上的调度器（群体架构）。

这就是整个设计空间。每个框架为每个轴选择默认值；其余的是表面语法。

### 2026 年每个框架如何映射

| 框架 | Agent | 交接 | 共享状态 | 编排器 |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | 工具返回 Agent | 调用者的问题 | LLM 的下一个交接调用 |
| AutoGen v0.4 / AG2 | `ConversableAgent` | GroupChat 上的发言选择器 | 消息池 | 选择器函数（LLM 或轮询） |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | 任务输出链式连接 | 管理者 LLM 或静态顺序 |
| LangGraph | 节点函数 | 图边 + 条件 | `StateGraph` 归约器 | 图，确定性 |
| Microsoft Agent Framework | agent + 编排模式 | 模式特定 | 线程 / 上下文 | 模式特定 |
| Google ADK | agent + A2A card | A2A 任务 | A2A 产物 | 宿主决定 |

表面差异看起来巨大。底层：相同的四个旋钮。

### 为什么这很重要

一旦你看到原语，框架比较就变成了一个简短的检查清单：

- 编排器信任 LLM 来路由（Swarm）还是将路由固定在代码中（LangGraph）？
- 共享状态是完整历史（GroupChat）还是投影的（StateGraph 归约器）？
- Agent 可以修改彼此的提示词（CrewAI 管理者）还是只交接（Swarm）？

这三个问题回答了 80% 的哪个框架适合给定问题。你不再购买"最好的多 Agent 框架"，而是开始为真正关心的轴设计。

### 无状态洞察

除共享状态外的每个原语都是无状态的。Agent 是（提示词，工具）的函数。交接是函数调用。编排器是调度器。**系统中唯一有状态的东西是共享状态。** 那就是所有有趣 bug 所在的地方：记忆投毒（第 15 课）、消息排序、版本控制、写入竞争。

隐藏共享状态的框架（Swarm）将问题推给调用者。集中化共享状态的框架（LangGraph 检查点、AutoGen 池）使其可检查但将协调成本转移到共享状态实现上。

### 单个原语的解剖

#### Agent

```
Agent = (system_prompt, tools, model, optional_name)
```

没有记忆。没有状态。两个具有相同系统提示词和工具的 Agent 是可互换的。看起来像每个 Agent 状态的一切实际上都在共享状态或交接协议中。

#### 交接

```
Handoff = (from_agent, to_agent, reason, payload)
```

三种实现占主导：

- **函数返回** — 工具返回下一个 Agent。这是 OpenAI Swarm 模式。Agent 在其工具模式中携带路由。
- **图边** — LangGraph。边是声明式的。LLM 产生一个值；条件选择下一个节点。
- **发言选择** — AutoGen GroupChat。选择器函数（有时本身是 LLM 调用）读取池并选择下一个发言者。

#### 共享状态

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

至少是一个消息列表。通常更多：结构化产物（CrewAI 任务输出）、类型化上下文（LangGraph 归约器）、外部记忆（MCP、向量 DB）。

两种拓扑：**完整池**（每个 Agent 看到每条消息）和**投影的**（Agent 看到角色范围的视图）。完整池简单但扩展性差。投影池可扩展但需要前置模式设计。

#### 编排器

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

四种风格：

- **静态** — 图在构建时固定（LangGraph 确定性、CrewAI 顺序）。
- **LLM 选择** — LLM 读取池并选择下一个发言者（AutoGen、CrewAI 层次化）。
- **交接驱动** — 当前 Agent 通过调用交接工具来决定（Swarm）。
- **队列驱动** — 工作器从共享队列拉取；没有显式的下一个发言者（群体架构、Matrix）。

### 框架之间什么变化

原语一旦固定，剩余的设计决策是：

- **记忆策略** — 临时 vs 持久检查点（LangGraph 检查点器）。
- **安全边界** — 谁可以批准交接（人在环中）。
- **成本核算** — 每个 Agent 的 token 预算。
- **可观察性** — 追踪交接、持久化状态以重放。

所有都可以在原语之上实现。它们中没有一个是新的原语。

## 动手构建

`code/main.py` 用约 150 行标准库 Python 实现了四个原语。没有真正的 LLM——每个 Agent 都是脚本化策略，所以重点放在协调结构上。

文件导出：

- `Agent` — 一个数据类，包含名称、系统提示词、工具、策略函数。
- `Handoff` — 返回新 Agent 的函数。
- `SharedState` — 线程安全的消息池。
- `Orchestrator` — 三个变体：`StaticOrchestrator`、`HandoffOrchestrator`、`LLMSelectorOrchestrator`（模拟）。

演示通过所有三种编排器类型运行相同的三 Agent 流水线（研究 → 编写 → 审查），并在最后打印消息池。你可以看到输出只在*谁选择下一个*上不同；Agent 和共享状态在各次运行中是相同的。

运行：

```
python3 code/main.py
```

预期输出：三次编排器运行，每种模式一次。每次都打印最终消息池。交接驱动的运行如果研究员决定提前完成，会触及更少的 Agent——那是 LLM 路由权衡的缩影。

## 用框架实现

`outputs/skill-primitive-mapper.md` 是一个技能，可以读取任何多 Agent 代码库或框架文档并返回四原语映射。在新框架发布时运行它，在深入阅读文档之前获得一段话的理解。

## 产出物

在采用新框架之前，为其编写原语映射。如果你做不到，说明文档不完整或框架在发明第五个原语（罕见——检查一下是否有你没见过的共享状态风格）。

将映射固定在你的架构文档中。当新团队成员加入时，在 API 文档之前发送映射。当框架版本变化时，比较映射差异，而不是更新日志。

## 练习题

1. 用不同的 Agent 策略运行 `code/main.py` 三次。观察编排器选择如何改变哪些 Agent 运行。
2. 实现第四种编排器类型：队列驱动的，Agent 轮询共享状态获取工作。可能发生什么死锁，你如何检测它？
3. 拿 LangGraph 快速入门（https://docs.langchain.com/oss/python/langgraph/workflows-agents）并将其重写为四个原语。LangGraph 的抽象哪些 1:1 映射，哪些是便捷包装？
4. 阅读 OpenAI Swarm 食谱（https://developers.openai.com/cookbook/examples/orchestrating_agents）。识别 Swarm 使哪个原语最符合人体工程学，以及哪个推给了调用者。
5. 在本表中找到一个完全隐藏共享状态的框架。解释当 Agent 需要跨交接协调而不重新读取历史时什么会出问题。

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Agent | "带工具的 LLM" | 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| 交接 (Handoff) | "控制转移" | 命名下一个 Agent 和可选负载的结构化调用。三种实现：函数返回、图边、发言选择。 |
| 共享状态 | "记忆" / "上下文" | 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| 编排器 | "协调器" | 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| 原语 | "抽象" | 每个框架参数化的四个轴之一。不是框架特性。 |
| 消息池 | "共享聊天历史" | 完整历史共享状态。容易推理，扩展性差。 |
| 投影状态 | "范围视图" | 共享状态的角色特定视图。可扩展，需要模式设计。 |
| 发言选择 | "谁下一个说话" | 编排器模式，其中函数（通常是 LLM）从组中选择下一个 Agent。 |

## 延伸阅读

- [OpenAI 食谱：编排 Agent — 例程和交接](https://developers.openai.com/cookbook/examples/orchestrating_agents) — 交接驱动编排的最清晰阐述
- [AutoGen 稳定文档](https://microsoft.github.io/autogen/stable/) — GroupChat + 发言选择是 LLM 选择编排的参考
- [LangGraph 工作流和 Agent](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — 图边编排和基于归约器的共享状态
- [CrewAI 简介](https://docs.crewai.com/en/introduction) — 角色-目标-背景故事的 Agent，顺序/层次化流程
- [AG2（社区 AutoGen 延续）](https://github.com/ag2ai/ag2) — Microsoft 将 v0.4 移至维护后的活跃 AutoGen v0.2 生产线
