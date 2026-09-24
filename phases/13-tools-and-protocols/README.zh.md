# Phase 13: 工具与协议

> **31 节课 · ~43.5 小时 · 🟡进阶**

## 学习目标

- 理解工具接口（Tool Interface）的设计原理和函数调用机制
- 深入掌握 MCP（Model Context Protocol）协议的全栈开发：服务端、客户端、传输层
- 学习 MCP 安全机制：工具投毒防护、OAuth 2.1 认证、生产级部署
- 掌握 Agent Skills：发现、调用路由、权限沙箱、评测与打包
- 了解 A2A（Agent-to-Agent）协议和 OpenTelemetry 可观测性
- 构建完整的工具生态系统（毕业项目）

## 前置知识

- LLM 工程化基础（Phase 11：提示工程、Function Calling）
- Python 工程基础（异步编程、HTTP 服务、JSON Schema）
- Agent 基础概念（Phase 14：Agent 循环，推荐）

## 在本阶段开始（GitHub） | Start this phase on GitHub

**前置条件：** Phase 11 的 LLM 补全 API。学 MCP 或 Agent Skills 时，用下面的聚焦路线，不要默认按课程编号顺序学。

**第一课（全阶段）：** [工具接口](01-the-tool-interface/)

从仓库根目录运行：

```bash
python3 phases/13-tools-and-protocols/01-the-tool-interface/code/main.py
```

保留命令、退出码、"描述-决策-执行-观察"轨迹、被拒绝输入的证据，以及一句解释轮数限制的话。

**下一步：** 继续到 [函数调用深度解析](02-function-calling-deep-dive/)，或选择下面的 MCP / Agent Skills 路线。

## MCP 聚焦路线（2026-07-28 规范）

上游为本阶段规划了一条 17 课、约 23.25 小时的 MCP 专注路线：从自描述的 JSON-RPC 请求一路到可运维的一致性门。推荐顺序：

01（工具接口）→ 06（MCP 基础）→ 07（服务端）→ 08（客户端）→ 09（传输层）→ 28（工具契约）→ 10（资源与提示）→ 11（模型输入/MRTR）→ 12（作用域与诱导输入）→ 13（Tasks 扩展）→ 14（MCP Apps）→ 29（可靠性）→ 15-16（安全两课）→ 30（注册中心供应链）→ 17（网关与准入）→ 18（生产级认证）→ 31（一致性工程）

Agent Skills 路线：22（契约与边界）→ 24（发现与渐进式披露）→ 25（调用与路由）→ 26（权限沙箱与信任）→ 27（评测打包与可移植性）。

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 工具接口：为什么 Agent 需要结构化输入输出 | Learn | Python | ~45min |
| 02 | 函数调用深度解析 | Build | Python | ~75min |
| 03 | 并行与流式工具调用 | Build | Python | ~75min |
| 04 | 结构化输出 | Build | Python | ~75min |
| 05 | 工具 Schema 设计 | Learn | Python | ~45min |
| 06 | MCP 基础：无状态请求与 JSON-RPC | Learn | Python | ~55min |
| 07 | 构建 MCP 服务器：无状态 Python 与 TypeScript | Build | Python | ~85min |
| 08 | 构建 MCP 客户端：发现、路由与双时代回退 | Build | Python | ~85min |
| 09 | MCP 传输层：stdio 与无状态 Streamable HTTP | Learn | Python | ~65min |
| 10 | MCP 资源与提示：无状态服务器的可寻址上下文 | Build | Python | ~60min |
| 11 | MCP 模型输入：Sampling 迁移与无状态 MRTR | Build | Python | ~75min |
| 12 | 显式作用域与无状态诱导输入 | Build | Python | ~60min |
| 13 | MCP Tasks 扩展：无状态内核上的持久化任务 | Build | Python | ~90min |
| 14 | 无状态协议上的 MCP Apps | Build | Python | ~75min |
| 15 | MCP 安全：投毒元数据、路由与 MRTR 状态 | Learn | Python | ~60min |
| 16 | MCP 授权：CIMD、签发方绑定、PKCE 与逐步授权 | Build | Python | ~90min |
| 17 | 无状态 MCP 网关与注册中心准入 | Learn | Python | ~75min |
| 18 | MCP 生产级认证：签发者绑定的注册与 Token | Build | Python | ~90min |
| 19 | A2A 协议 | Build | Python | ~75min |
| 20 | OpenTelemetry GenAI | Build | Python | ~75min |
| 21 | LLM 路由层 | Learn | Python | ~45min |
| 22 | Agent Skills：可移植契约与运行时边界 | Build | Python | ~90min |
| 23 | 毕业项目：无状态工具生态系统 | Build | Python | ~120min |
| 24 | 技能发现与渐进式披露 | Build | Python | ~105min |
| 25 | 技能调用与路由 | Build | Python | ~105min |
| 26 | 技能权限、沙箱与信任 | Build | Python | ~120min |
| 27 | Skill 评测、打包与可移植性 | Build | Python | ~150min |
| 28 | MCP 工具契约与内容 | Build | Python | ~120min |
| 29 | MCP 可靠性、取消与流控 | Build | Python | ~120min |
| 30 | MCP 注册中心供应链：准入、漂移与回滚 | Build | Python | ~90min |
| 31 | MCP 一致性工程：版本化、证据与运维 | Build | Python | ~100min |

> **【中文解读】** 2026-09 上游同步把 MCP 系列整体对齐到 2026-07-28 无状态规范：initialize 握手与会话 ID 被移除，元数据逐请求携带；Sampling/Roots 被弃用，改用 MRTR 与显式参数；新增 24-27（Agent Skills 全链路）和 28-31（生产级 MCP 边界）八课。旧译文已全部按新规范重写。

## 常见困惑

- **"MCP 和 Function Calling 有什么区别？"** → Function Calling 是单次调用接口，MCP 是标准化的双向通信协议，支持资源发现、任务扩展、缓存提示等高级能力。MCP 可以理解为 Function Calling 的"升级版协议"。
- **"为什么要学 A2A 协议？"** → A2A（Agent-to-Agent）是 Google 提出的智能体间通信协议。当多个 Agent 需要协作完成复杂任务时，A2A 提供了标准化的发现、协商和执行机制。
- **"MCP 安全需要注意什么？"** → 工具投毒（Tool Poisoning）是 MCP 的核心安全风险——恶意工具可以在描述中隐藏指令。第 15-16 课讲防护，17-18 课讲网关准入与生产级认证，30 课讲注册中心供应链。
- **"新版 MCP 为什么砍掉了 initialize 握手？"** → 无状态化让每个请求可独立理解、授权、路由和重试——服务器不再需要保存会话，网关和负载均衡可以任意转发。需要连续性时用服务器签发的不透明状态句柄，作为普通参数传回。

## 开始学习

→ [第一课：工具接口](01-the-tool-interface/docs/zh.md)
