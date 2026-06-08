# Phase 14: Agent 工程

> **42 节课 · ~42 小时 · 🔴高级**

现代 AI 工程的核心。从第一性原理构建 Agent。

## 学习目标

- 理解 Agent Loop（ReAct）的工作原理，掌握推理-行动-观察循环
- 构建记忆系统：虚拟上下文、向量检索、图数据库、混合记忆
- 掌握主流 Agent 框架：LangGraph、AutoGen、CrewAI、OpenAI Agents SDK、Claude Agent SDK
- 理解规划算法：HTN、进化搜索、树搜索、自反思
- 学会评估驱动开发（Eval-Driven Development）和 Agent Workbench 方法论
- 构建生产级 Agent：可观测性、故障模式、安全防护、编排模式

## 前置知识

- 完成阶段 01-13 的学习，掌握 LLM 基础、RAG、微调等核心概念
- 熟练使用 Python 异步编程（asyncio）
- 了解 REST API 和工具调用的基本概念
- 理解 Token 经济学和上下文窗口管理

## 课程清单

| # | 课程 | 类型 | 预计时间 |
|---|------|------|---------|
| 01 | Agent 循环（ReAct） | 动手 | ~60min |
| 02 | ReWOO 与规划-执行模式 | 动手 | ~60min |
| 03 | Reflexion 语言强化学习 | 动手 | ~60min |
| 04 | 思维树与 LATS | 动手 | ~75min |
| 05 | 自我精炼与 CRITIC | 动手 | ~60min |
| 06 | 工具使用与函数调用 | 动手 | ~60min |
| 07 | 记忆 — 虚拟上下文与 MemGPT | 动手 | ~75min |
| 08 | 记忆块与离线计算（Letta） | 动手 | ~75min |
| 09 | 混合记忆 — 向量+图+KV（Mem0） | 动手 | ~75min |
| 10 | 技能库与终身学习（Voyager） | 动手 | ~75min |
| 11 | HTN 规划与进化搜索 | 动手 | ~75min |
| 12 | Anthropic 工作流模式 | 学习+动手 | ~60min |
| 13 | LangGraph — 有状态图与持久执行 | 学习+动手 | ~75min |
| 14 | AutoGen v0.4 — Actor 模型 | 学习+动手 | ~75min |
| 15 | CrewAI — 基于角色的团队与流程 | 学习+动手 | ~60min |
| 16 | OpenAI Agents SDK — 交接、护栏、追踪 | 学习+动手 | ~75min |
| 17 | Claude Agent SDK — 子 Agent 与会话存储 | 学习+动手 | ~75min |
| 18 | Agno 与 Mastra — 生产运行时 | 学习 | ~45min |
| 19 | 基准测试 — SWE-bench、GAIA、AgentBench | 学习 | ~60min |
| 20 | 基准测试 — WebArena 与 OSWorld | 学习 | ~60min |
| 21-42 | 计算机操控 Agent、语音 Agent、可观测性、多 Agent 辩论、故障模式、提示注入防御、编排模式、生产运行时、评估驱动开发、Agent Workbench（12节）等 | 混合 | ~21h |

<details>
<summary>展开查看课程 21-42 完整列表</summary>

| # | 课程 | 类型 | 预计时间 |
|---|------|------|---------|
| 21 | 计算机操控 Agent（Claude、OpenAI CUA、Gemini） | 学习 | ~60min |
| 22 | 语音 Agent — Pipecat 与 LiveKit | 学习 | ~60min |
| 23 | OpenTelemetry GenAI 语义约定 | 学习+动手 | ~60min |
| 24 | Agent 可观测性 — Langfuse、Phoenix、Opik | 学习 | ~45min |
| 25 | 多 Agent 辩论与协作 | 学习+动手 | ~60min |
| 26 | 故障模式 — Agent 为什么会失败 | 学习+动手 | ~60min |
| 27 | 提示注入与 PVE 防御 | 动手 | ~75min |
| 28 | 编排模式 — 监督者、集群、分层 | 学习+动手 | ~60min |
| 29 | 生产运行时 — 队列、事件、定时任务 | 学习 | ~60min |
| 30 | 评估驱动的 Agent 开发 | 学习+动手 | ~60min |
| 31 | Agent Workbench：为什么能力强的模型仍然失败 | 学习+动手 | ~45min |
| 32 | 最小化 Agent Workbench | 动手 | ~45min |
| 33 | Agent 指令作为可执行约束 | 动手 | ~50min |
| 34 | 仓库记忆与持久状态 | 动手 | ~60min |
| 35 | Agent 初始化脚本 | 动手 | ~45min |
| 36 | 范围契约与任务边界 | 动手 | ~50min |
| 37 | 运行时反馈循环 | 动手 | ~50min |
| 38 | 验证门控 | 动手 | ~55min |
| 39 | 审查者 Agent：分离构建者与评审者 | 动手 | ~55min |
| 40 | 多会话交接 | 动手 | ~50min |
| 41 | 真实仓库上的 Workbench | 动手 | ~60min |
| 42 | 毕业项目：交付可复用的 Agent Workbench 包 | 动手 | ~75min |

</details>

## 常见困惑

- **Agent 和普通 LLM 调用有什么区别？** → Agent 引入了循环（loop）——模型不再是单次调用，而是推理→行动→观察→推理的迭代过程，直到任务完成或触发停止条件。
- **为什么需要这么多框架？** → 每个框架解决不同的痛点：LangGraph 适合复杂有状态图、CrewAI 适合角色协作、OpenAI SDK 适合快速原型。课程 12-18 会逐一拆解，帮你选择。
- **Agent Workbench 是什么？** → 这是本课程的独创方法论（课 31-42）：一个用于开发、调试和评估 Agent 的集成环境。先理解为什么强模型仍会失败（课 31），再逐步构建 Workbench 的各个组件。
- **记忆系统为什么这么复杂？** → 单一记忆方案无法覆盖所有场景。虚拟上下文适合短期对话、向量检索适合语义搜索、图数据库适合关系推理。课程 07-09 会帮你理解何时用哪种方案。

## 开始学习

→ [第一课：Agent 循环](01-the-agent-loop/docs/en.md)
