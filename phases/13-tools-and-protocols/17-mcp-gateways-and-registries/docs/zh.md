# MCP 网关与注册中心 — 企业控制平面

> 企业不能让每个开发者随意安装 MCP 服务器。网关集中处理认证、RBAC、审计、限流、缓存和工具投毒检测，将合并后的工具面暴露为单一 MCP 端点。官方 MCP 注册中心（Anthropic + GitHub + PulseMCP + Microsoft，命名空间验证）是权威上游源。本课命名网关的位置，走通最小实现，并调查 2026 年供应商格局。

> **【中文解读】** 企业不能让每个开发者随意安装 MCP 服务器。网关集中处理认证、RBAC、审计、限流、缓存和工具投毒检测，将合并后的工具面暴露为单一 MCP 端点。官方 MCP 注册中心（Anthropic + GitHub + PulseMCP + Microsoft，命名空间验证）是权威上游源。

> **【拓展】** MCP 网关是企业部署 MCP 的核心架构模式。Cloudflare MCP Portals、Kong AI Gateway、IBM ContextForge 等都在 2025-2026 年推出了网关产品。网关模式将 Phase 13 · 15（工具投毒防御）和 Phase 13 · 16（OAuth 2.1）集中化执行，是企业安全合规的必备组件。

**类型：** 学习
**语言：** Python（标准库，最小网关）
**前置条件：** Phase 13 · 15（工具投毒），Phase 13 · 16（OAuth 2.1）
**时间：** 约 45 分钟

## 学习目标

- 解释 MCP 网关的位置（在 MCP 客户端和多个后端 MCP 服务器之间）。
- 实现五大网关职责：认证、RBAC、审计、限流、策略。
- 在网关层强制执行工具哈希锁定清单。
- 区分官方 MCP 注册中心与元注册中心（Glama、MCPMarket、MCP.so、Smithery、LobeHub）。

## 问题引入

一家世界 500 强企业有 30 个审批的 MCP 服务器、5000 名开发者、合规审计要求和一个希望集中策略的安全团队。让每个开发者在 IDE 中安装任意服务器是不可接受的。

网关模式：

1. 网关作为单一 Streamable HTTP 端点运行，开发者连接到此。
2. 网关持有每个后端 MCP 服务器的凭证。
3. 每个开发者请求通过网关自身的 OAuth 认证和范围限制。
4. 网关将调用路由到后端服务器并应用策略。
5. 所有调用记录用于审计。

Cloudflare MCP Portals、Kong AI Gateway、IBM ContextForge、MintMCP、TrueFoundry、Envoy AI Gateway——都在 2025-2026 年推出了网关或网关功能。

同时，官方 MCP 注册中心作为权威上游启动：经过策展、命名空间验证、反向 DNS 命名的服务器。元注册中心（Glama、MCPMarket、MCP.so、Smithery、LobeHub）聚合来自多个来源的服务器。

## 核心概念

### 五大网关职责

1. **认证。** OAuth 2.1 识别开发者，映射到用户角色。
2. **RBAC。** 每用户策略：哪些服务器、哪些工具、哪些范围。
3. **审计。** 每次调用记录谁、做了什么、何时、结果。
4. **限流。** 每用户/每工具/每服务器上限防止滥用。
5. **策略。** 拒绝投毒描述、强制 Rule of Two、脱敏 PII。

### 网关作为单一端点

对开发者来说，网关看起来像一个 MCP 服务器。内部路由到 N 个后端。Session ID（Phase 13 · 09）在边界重写。

### 凭证保险库

开发者永远看不到后端 token。网关持有它们（或代理给持有它们的身份提供商）。在网关上有 `notes:read` 的开发者可能通过网关自己的后端凭证间接访问 notes MCP 服务器——但仅在绑定间接访问的策略下。

### 网关层的工具哈希锁定

网关持有已审批工具描述的清单（SHA256 哈希）。发现时，它获取每个后端的 `tools/list`，将哈希与清单比较，移除描述已变更的任何工具。这是 Phase 13 · 15 中地毯拉扯防御的集中化应用。

### 策略即代码

高级网关用 OPA/Rego、Kyverno 或 Styra 表达策略。像"用户 `alice` 只能在 `acme` 组织的仓库上调用 `github.open_pr`"这样的规则以声明式编码。简单网关使用手写 Python。两种形状都有效。

### 会话感知路由

当用户的会话包含混合服务器时，网关多路复用：开发者的单个 MCP 会话持有 N 个后端会话，每个服务器一个。来自任何后端的通知通过网关路由到开发者的会话。

### 命名空间合并

网关合并所有后端的工具命名空间，通常在冲突时使用前缀。`github.open_pr`、`notes.search`。这使路由无歧义。

### 注册中心

- **官方 MCP 注册中心（`registry.modelcontextprotocol.io`）。** 在 Anthropic、GitHub、PulseMCP、Microsoft 管理下启动。命名空间验证（反向 DNS：`io.github.user/server`）。预过滤基本质量。
- **Glama。** 以搜索为中心的元注册中心，聚合多个来源。
- **MCPMarket。** 商业导向的目录，有供应商列表。
- **MCP.so。** 社区目录；开放提交。
- **Smithery。** 包管理器风格的安装流程。
- **LobeHub。** 在其 LobeChat 应用中集成的 UI 注册中心。

企业网关默认从官方注册中心拉取，允许管理员从元注册中心添加策展内容，拒绝任何未锁定的。

### 反向 DNS 命名

官方注册中心要求公开服务器使用反向 DNS 名称：`io.github.alice/notes`。命名空间防止占位并使信任委托更清晰。

### 供应商调查，2026 年 4 月

| 供应商 | 优势 |
|--------|------|
| Cloudflare MCP Portals | 边缘托管；OAuth 集成；免费层 |
| Kong AI Gateway | K8s 原生；细粒度策略；日志到 OpenTelemetry |
| IBM ContextForge | 企业 IAM；合规；审计导出 |
| TrueFoundry | 偏向 DevOps；指标优先 |
| MintMCP | 面向开发者平台 |
| Envoy AI Gateway | 开源；可定制过滤器 |

Phase 17（生产基础设施）深入讲解网关运维。

## 用框架实现

`code/main.py` 提供约 150 行的最小网关：通过假 Bearer token 认证用户、持有每用户 RBAC 策略、路由请求到两个后端 MCP 服务器、将每次调用写入审计日志、强制执行速率限制、拒绝描述哈希不匹配的后端工具。

关注点：

- `RBAC` 字典按 `user_id` 索引，包含允许的 `server_tool` 条目。
- `AUDIT_LOG` 是仅追加的事件列表。
- 限流使用每用户令牌桶。
- 锁定清单是 `server::tool -> hash` 的字典。

## 产出物

本课产生 `outputs/skill-gateway-bootstrap.md`。给定企业 MCP 计划（用户、后端、合规），该技能生成网关配置规格。

## 练习题

1. 运行 `code/main.py`。作为允许用户发起调用；然后作为禁止用户；然后触发速率限制超限的突发。验证三个流程。

2. 添加在返回客户端前从结果中脱敏 PII 的策略。使用简单的正则扫描 SSN 形状的字符串；注意差距（电子邮件、电话号码）。

3. 扩展审计日志以发出 OpenTelemetry GenAI span。Phase 13 · 20 覆盖确切属性。

4. 为一个 50 开发者团队设计 RBAC 策略，有 5 个后端（notes、github、postgres、jira、slack）。谁对每个后端只读？谁能写？

5. 从头到尾阅读 Cloudflare 企业 MCP 文章。识别 Cloudflare 提供的一个此标准库网关没有的功能。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 网关 | "MCP 代理" | 客户端和后端之间的集中化服务器 | Gateway |
| 凭证保险库 | "后端 token 保留在服务端" | 开发者永远看不到上游 token | Credential vaulting |
| 会话感知路由 | "多后端会话" | 网关为每个开发者会话多路复用 N 个后端会话 | Session-aware routing |
| 工具哈希锁定 | "已审批清单" | 每个已审批工具描述的 SHA256；集中阻止地毯拉扯 | Tool-hash pinning |
| 基于角色的访问控制 | "每用户策略" | 工具和服务器的角色基础访问控制 | RBAC |
| 策略即代码 | "声明式规则" | 在网关执行的 OPA/Rego、Kyverno、Styra 策略 | Policy-as-code |
| 审计日志 | "谁、什么、何时" | 用于合规的仅追加事件日志 | Audit log |
| 限流 | "每用户令牌桶" | 每分钟上限防止滥用 | Rate limit |
| 官方 MCP 注册中心 | "权威上游" | `registry.modelcontextprotocol.io`，命名空间验证 | Official MCP Registry |
| 反向 DNS 命名 | "注册中心命名空间" | `io.github.user/server` 约定 | Reverse-DNS naming |

## 延伸阅读

- [Official MCP Registry](https://registry.modelcontextprotocol.io/) — 命名空间验证的权威上游
- [Cloudflare — Enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/) — 带 OAuth 和策略的网关模式
- [agentic-community — MCP gateway registry](https://github.com/agentic-community/mcp-gateway-registry) — 开源参考网关
- [TrueFoundry — What is an MCP gateway?](https://www.truefoundry.com/blog/what-is-mcp-gateway) — 功能比较文章
- [IBM — MCP context forge](https://github.com/IBM/mcp-context-forge) — IBM 的企业网关
