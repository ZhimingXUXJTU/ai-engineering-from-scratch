# Phase 13: 工具与协议

> **23 节课 · ~24.5 小时 · 🟡进阶**

## 学习目标

- 理解工具接口（Tool Interface）的设计原理和函数调用机制
- 深入掌握 MCP（Model Context Protocol）协议的全栈开发：服务端、客户端、传输层
- 学习 MCP 安全机制：工具投毒防护、OAuth 2.1 认证、生产级部署
- 了解 A2A（Agent-to-Agent）协议和 OpenTelemetry 可观测性
- 构建完整的工具生态系统（毕业项目）

## 前置知识

- LLM 工程化基础（Phase 11：提示工程、Function Calling）
- Python 工程基础（异步编程、HTTP 服务、JSON Schema）
- Agent 基础概念（Phase 14：Agent 循环，推荐）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 工具接口 | Learn | Python | ~45min |
| 02 | 函数调用深度解析 | Build | Python | ~75min |
| 03 | 并行与流式工具调用 | Build | Python | ~75min |
| 04 | 结构化输出 | Build | Python | ~75min |
| 05 | 工具 Schema 设计 | Build | Python | ~45min |
| 06 | MCP 基础 | Learn | Python | ~45min |
| 07 | 构建 MCP 服务端 | Build | Python | ~75min |
| 08 | 构建 MCP 客户端 | Build | Python | ~75min |
| 09 | MCP 传输层 | Build | Python | ~45min |
| 10 | MCP 资源与提示 | Build | Python | ~45min |
| 11 | MCP 采样 | Build | Python | ~75min |
| 12 | MCP Roots 与 Elicitation | Learn | Python | ~45min |
| 13 | MCP 异步任务 | Build | Python | ~75min |
| 14 | MCP 应用开发 | Build | Python | ~75min |
| 15 | MCP 安全 I — 工具投毒 | Learn | Python | ~45min |
| 16 | MCP 安全 II — OAuth 2.1 | Build | Python | ~75min |
| 17 | MCP 网关与注册中心 | Build | Python | ~45min |
| 18 | MCP 生产级认证 — DCR + JWKS | Build | Python | ~90min |
| 19 | A2A 协议 | Learn | Python | ~75min |
| 20 | OpenTelemetry GenAI | Build | Python | ~75min |
| 21 | LLM 路由层 | Build | Python | ~45min |
| 22 | Skills 与 Agent SDK | Learn | Python | ~45min |
| 23 | 毕业项目 — 工具生态系统 | Build | Python | ~120min |

## 常见困惑

- **"MCP 和 Function Calling 有什么区别？"** → Function Calling 是单次调用接口，MCP 是标准化的双向通信协议，支持资源发现、采样、长连接等高级能力。MCP 可以理解为 Function Calling 的"升级版协议"。
- **"为什么要学 A2A 协议？"** → A2A（Agent-to-Agent）是 Google 提出的智能体间通信协议。当多个 Agent 需要协作完成复杂任务时，A2A 提供了标准化的发现、协商和执行机制。
- **"MCP 安全需要注意什么？"** → 工具投毒（Tool Poisoning）是 MCP 的核心安全风险——恶意工具可以在描述中隐藏指令。第 15-18 课会详细讲解防护措施和生产级认证方案。

## 开始学习

→ [第一课：工具接口](01-the-tool-interface/docs/zh.md)
