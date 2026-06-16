# MCP Gateways and Registries — Enterprise Control Planes | MCP 网关与注册中心：企业控制平面

> Enterprises cannot let every dev install random MCP servers. A gateway centralizes auth, RBAC, audit, rate limiting, caching, and tool-poisoning detection, then exposes the merged tool surface as a single MCP endpoint. The Official MCP Registry (Anthropic + GitHub + PulseMCP + Microsoft, namespace-verified) is the canonical upstream. This lesson names where a gateway fits, walks a minimal implementation, and surveys the 2026 vendor landscape.

> **【中文解读】** 企业不能让每个开发者随意安装 MCP 服务器。网关集中处理认证、RBAC、审计、限流、缓存和工具投毒检测，将合并后的工具面暴露为单一 MCP 端点。官方 MCP 注册中心（Anthropic + GitHub + PulseMCP + Microsoft，命名空间验证）是权威上游源。

> **【拓展】** MCP 网关是企业部署 MCP 的核心架构模式。Cloudflare MCP Portals、Kong AI Gateway、IBM ContextForge 等都在 2025-2026 年推出了网关产品。网关模式将 Phase 13 · 15（工具投毒防御）和 Phase 13 · 16（OAuth 2.1）集中化执行，是企业安全合规的必备组件。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·09（MCP transports）——网关对外暴露为 Streamable HTTP；(2) Phase 13·15（Tool Poisoning）和 13·16（OAuth 2.1）——网关的核心职责就是集中执行这两节的安全机制；(3) RBAC、限流、审计日志基础概念。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal gateway) | **语言:** Python (stdlib, minimal gateway)
**Prerequisites:** Phase 13 · 15 (tool poisoning), Phase 13 · 16 (OAuth 2.1) | **前置知识:** Phase 13 · 15 (tool poisoning), Phase 13 · 16 (OAuth 2.1)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Explain where an MCP gateway sits (between MCP clients and multiple backend MCP servers).
  中文翻译：解释 MCP 网关的位置（在 MCP 客户端和多个后端 MCP 服务器之间）。
- Implement the five gateway responsibilities: auth, RBAC, audit, rate limit, policy.
  中文翻译：实现五大网关职责：认证、RBAC、审计、限流、策略。
- Enforce a pinned-tool-hash manifest at the gateway layer.
  中文翻译：在网关层强制执行锁定的工具哈希清单。
- Differentiate the Official MCP Registry from metaregistries (Glama, MCPMarket, MCP.so, Smithery, LobeHub).

> **【中文解读】** 学习目标：理解网关在 MCP 客户端和多个后端 MCP 服务器之间的位置；实现五大网关职责（认证、RBAC、审计、限流、策略）；在网关层强制执行工具哈希锁定清单；区分官方 MCP 注册中心与元注册中心。

## The Problem | 问题引入

> **【中文解读】** Fortune 500 企业有 30 个审批的 MCP 服务器、5000 名开发者、合规审计要求。网关模式：(1) 网关作为单一 Streamable HTTP 端点运行；(2) 持有每个后端 MCP 服务器的凭证；(3) 每个开发者请求通过网关自身的 OAuth 认证和范围限制；(4) 网关路由调用到后端服务器并应用策略；(5) 所有调用记录用于审计。

A Fortune 500 has 30 approved MCP servers, 5000 developers, compliance and audit requirements, and a security team that wants centralized policy. Letting every developer install arbitrary servers in their IDEs is a non-starter.

> Fortune 500 企业有 30 个批准的 MCP 服务器、5000 名开发者、合规审计要求，以及想要集中策略的安全团队。让每个开发者在其 IDE 中安装任意服务器不可行。

The gateway pattern:

> 网关模式：

1. Gateway runs as a single Streamable HTTP endpoint developers connect to.
  中文翻译：网关作为单一 Streamable HTTP 端点运行，开发者连接到它。
2. Gateway holds credentials for each backend MCP server.
  中文翻译：网关持有每个后端 MCP 服务器的凭证。
3. Every developer request is authenticated and scoped via the gateway's own OAuth.
  中文翻译：每个开发者请求通过网关自身的 OAuth 认证和范围限制。
4. Gateway routes the call to the backend server, applying policy.
  中文翻译：网关将调用路由到后端服务器，应用策略。
5. All calls logged for audit.
  中文翻译：所有调用记录用于审计。

Cloudflare MCP Portals, Kong AI Gateway, IBM ContextForge, MintMCP, TrueFoundry, Envoy AI Gateway — all shipped gateways or gateway features in 2025-2026.

> Cloudflare MCP Portals、Kong AI Gateway、IBM ContextForge、MintMCP、TrueFoundry、Envoy AI Gateway——都在 2025-2026 年发布了网关或网关功能。

Meanwhile, the Official MCP Registry launched as the canonical upstream: curated, namespace-verified, reverse-DNS-named servers the gateway can pull from. Metaregistries (Glama, MCPMarket, MCP.so, Smithery, LobeHub) aggregate servers across multiple sources.

> 同时，官方 MCP 注册中心作为权威上游发布：策展、命名空间验证、反向 DNS 命名的服务器，网关可从中拉取。元注册中心（Glama、MCPMarket、MCP.so、Smithery、LobeHub）聚合多个来源的服务器。

> 💡 **【类比】** MCP 网关像公司的"采购中心"。员工（开发者）不能自己淘宝下单买工具（直连各 MCP server），所有采购走采购中心：采购中心谈好合同（持有后端凭证）、限制每人能买什么（RBAC）、记录谁买了什么（审计）、防止供应商偷偷换货（哈希锁定）、超量限购（限流）。员工只看到一个"内部采购网站"（单一 MCP 端点），背后是采购中心和众多供应商打交道。注册中心像"行业白名单"——官方 Registry 是 ISO 认证目录，元注册中心是各类比价网站。

## The Concept | 核心概念

> **【中文解读】** 本节详解五大网关职责、网关作为单一端点、凭证保险库、工具哈希锁定、策略即代码、会话感知路由、命名空间合并、注册中心生态和供应商格局。

### Five gateway responsibilities

> **【中文解读】** 五大网关职责：(1) 认证——OAuth 2.1 识别开发者，映射到用户角色；(2) RBAC——每用户策略：哪些服务器、哪些工具、哪些范围；(3) 审计——每次调用记录谁、做了什么、何时、结果；(4) 限流——每用户/每工具/每服务器上限；(5) 策略——拒绝投毒描述、强制 Rule of Two、脱敏 PII。

1. **Auth.** OAuth 2.1 to identify the developer; maps to user roles.
  中文翻译：**认证。** OAuth 2.1 识别开发者；映射到用户角色。
2. **RBAC.** Per-user policy: which servers, which tools, which scopes.
  中文翻译：**RBAC。** 每用户策略：哪些服务器、哪些工具、哪些范围。
3. **Audit.** Every call logged with who, what, when, result.
  中文翻译：**审计。** 每次调用记录谁、做了什么、何时、结果。
4. **Rate limit.** Per-user / per-tool / per-server caps to prevent abuse.
  中文翻译：**限流。** 每用户/每工具/每服务器上限防止滥用。
5. **Policy.** Reject poisoned descriptions, enforce Rule of Two, redact PII.
  中文翻译：**策略。** 拒绝投毒描述、强制 Rule of Two、脱敏 PII。

### Gateway as a single endpoint

To developers, the gateway looks like one MCP server. Internally it routes to N backends. Session ids (Phase 13 · 09) are rewritten at the boundary.

> 对开发者而言，网关看起来像一个 MCP 服务器。内部它路由到 N 个后端。Session id（Phase 13 · 09）在边界重写。

### Credential vaulting

Developers never see backend tokens. The gateway holds them (or proxies to an identity provider that does). A developer with `notes:read` on the gateway may transitively access the notes MCP server with the gateway's own backend credentials — but only under policy that binds the transitive access.

> 开发者永不见后端 token。网关持有它们（或代理给身份提供商）。开发者在网关上有 `notes:read` 可以传递地用网关自身的后端凭证访问 notes MCP 服务器——但仅在绑定传递访问的策略下。

### Tool-hash pinning at the gateway

The gateway holds a manifest of approved tool descriptions (SHA256 hashes). At discovery time, it fetches each backend's `tools/list`, compares hashes to the manifest, and removes any tool whose description has mutated. This is the rug-pull defense from Phase 13 · 15 applied centrally.

> 网关持有批准工具描述的清单（SHA256 哈希）。发现时，它获取每个后端的 `tools/list`，比较哈希与清单，移除描述变更的工具。这是 Phase 13 · 15 地毯拉扯防御的集中应用。

> ⚠️ **【易错点】** 场景：网关只做认证不做工具哈希校验 / 后果：后端 MCP server 暗中更新工具描述（rug pull 投毒），网关无感知透传给所有用户；个人用户无法自己审计 / 修复：(1) 网关必须维护 `tool_hashes.json` 清单文件；(2) 每次 tools/list 比对，不匹配的 tool 标记为 disabled 并告警安全团队；(3) 清单更新走 code review 流程而非自动同步——这是企业纵深防御的关键一层。

> 🤔 **【困惑】** Q: 网关集中化会不会成为单点故障？ A: 会，所以必须做高可用：(1) 网关水平扩展（多个实例 + 负载均衡）；(2) 状态外置（Redis/Postgres，不在实例内存）；(3) 优雅降级——网关挂了各 IDE 可以临时直连"白名单内"的本地 MCP server 应急；但安全策略（哈希、限流）必须失效关闭（fail-closed）而非失效开放。生产建议至少 99.9% SLA。

### Policy-as-code

Advanced gateways express policy in OPA/Rego, Kyverno, or Styra. Rules like "user `alice` may call `github.open_pr` only on repos in org `acme`" are encoded declaratively. Simple gateways use hand-coded Python. Both shapes are valid.

> 高级网关用 OPA/Rego、Kyverno 或 Styra 表达策略。规则如"user `alice` 只能在 `acme` 组织的 repo 上调用 `github.open_pr`"声明式编码。简单网关用手写 Python。两种形态都有效。

### Session-aware routing

When a user's session includes a mix of servers, the gateway multiplexes: the developer's single MCP session holds N backend sessions, one per server. Notifications from any backend route through the gateway to the developer's session.

> 当用户会话包含多服务器混合时，网关多路复用：开发者的单个 MCP 会话持有 N 个后端会话，每个服务器一个。任何后端的通知通过网关路由到开发者的会话。

### Namespace merging

Gateways merge tool namespaces from all backends, typically with prefix-on-collision. `github.open_pr`, `notes.search`. This makes routing unambiguous.

> 网关合并所有后端的工具命名空间，通常冲突时加前缀。`github.open_pr`、`notes.search`。这使路由无歧义。

### Registries

- **Official MCP Registry (`registry.modelcontextprotocol.io`).** Launched under Anthropic, GitHub, PulseMCP, Microsoft stewardship. Namespace-verified (reverse-DNS: `io.github.user/server`). Pre-filtered for basic quality.
  中文翻译：**官方 MCP 注册中心。** 在 Anthropic、GitHub、PulseMCP、Microsoft 管理下启动。命名空间验证（反向 DNS：`io.github.user/server`）。预过滤基本质量。
- **Glama.** Search-centric metaregistry aggregating many sources.
  中文翻译：**Glama。** 以搜索为中心的元注册中心，聚合多来源。
- **MCPMarket.** Commercial-leaning directory with vendor listings.
  中文翻译：**MCPMarket。** 商业倾向目录，带供应商列表。
- **MCP.so.** Community directory; open submissions.
  中文翻译：**MCP.so。** 社区目录；开放提交。
- **Smithery.** Package-manager-style installation flow.
  中文翻译：**Smithery。** 包管理器风格安装流程。
- **LobeHub.** UI-integrated registry in their LobeChat app.
  中文翻译：**LobeHub。** 在其 LobeChat 应用中 UI 集成的注册中心。

Enterprise gateways pull from the Official Registry by default, allow admin-curated additions from metaregistries, and reject anything unpinned.

> 企业网关默认从官方注册中心拉取，允许管理员策展从元注册中心添加，拒绝任何未锁定的。

### Reverse-DNS naming

Official Registry mandates reverse-DNS names for public servers: `io.github.alice/notes`. Namespaces prevent squatting and make trust delegation clearer.

> 官方注册中心要求公共服务器使用反向 DNS 名：`io.github.alice/notes`。命名空间防止抢注并使信任委托更清晰。

### Vendor survey, April 2026

| Vendor | Strength |
|--------|----------|
| Cloudflare MCP Portals | Edge-hosted; OAuth integrated; free tier |
| Kong AI Gateway | K8s-native; fine-grained policy; logs to OpenTelemetry |
| IBM ContextForge | Enterprise IAM; compliance; audit export |
| TrueFoundry | DevOps-leaning; metrics-first |
| MintMCP | Developer-platform oriented |
| Envoy AI Gateway | Open-source; customizable filters |

Phase 17 (production infrastructure) dives deeper on gateway operations.

> Phase 17（生产基础设施）深入讲解网关运维。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 实现约150行的最小网关：通过 Bearer token 认证用户、每用户 RBAC 策略、路由到两个后端 MCP 服务器、写入审计日志、令牌桶限流、拒绝描述哈希不匹配的后端工具。关注点：RBAC 字典按 user_id 索引、AUDIT_LOG 是追加事件列表、令牌桶限流每用户、锁定清单为 server::tool -> hash 映射。

`code/main.py` ships a minimal gateway in ~150 lines: authenticates users by a fake Bearer token, holds a per-user RBAC policy, routes requests to two backend MCP servers, writes every call to an audit log, enforces a rate limit, and rejects any backend tool whose description hash does not match a pinned manifest.

> `code/main.py` 提供约 150 行的最小网关：用假 Bearer token 认证用户、持有每用户 RBAC 策略、路由请求到两个后端 MCP 服务器、每次调用写入审计日志、强制速率限制，拒绝描述哈希不匹配锁定清单的后端工具。

What to look at:

- `RBAC` dict keyed by `user_id` with allowed `server_tool` entries.
  中文翻译：`RBAC` 字典按 `user_id` 索引，带允许的 `server_tool` 条目。
- `AUDIT_LOG` is an append-only list of events.
  中文翻译：`AUDIT_LOG` 是仅追加的事件列表。
- Rate limit uses a token bucket per user.
  中文翻译：限流使用每用户的令牌桶。
- Pinned manifest is a dict of `server::tool -> hash`.
  中文翻译：锁定清单是 `server::tool -> hash` 的字典。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-gateway-bootstrap.md`——给定企业 MCP 计划（用户、后端、合规要求），生成网关配置规格。

This lesson produces `outputs/skill-gateway-bootstrap.md`. Given an enterprise MCP plan (users, backends, compliance), the skill produces a gateway configuration spec.

> 本课产出 `outputs/skill-gateway-bootstrap.md`。给定企业 MCP 计划（用户、后端、合规），该 skill 生成网关配置规格。

## Exercises | 练习题

1. Run `code/main.py`. Make a call as an allowed user; then as a disallowed user; then a rate-limit-exceeded burst. Verify all three flows.
   中文翻译：运行 `code/main.py`。作为允许的用户调用；然后作为不允许的用户；然后超过限流的突发。验证三种流程。

2. Add a policy that redacts PII from results before returning to the client. Use a simple regex pass for SSN-shaped strings; note the gap (emails, phone numbers).
   中文翻译：添加在返回客户端前脱敏 PII 的策略。对 SSN 形状字符串使用简单正则；注意差距（邮箱、电话号码）。

3. Extend the audit log to emit OpenTelemetry GenAI spans. Phase 13 · 20 covers the exact attributes.
   中文翻译：扩展审计日志发出 OpenTelemetry GenAI span。Phase 13 · 20 涵盖精确属性。

4. Design an RBAC policy for a 50-developer team with five backends (notes, github, postgres, jira, slack). Who gets read-only on each? Who gets write?
   中文翻译：为 50 开发者团队设计带五个后端的 RBAC 策略（notes、github、postgres、jira、slack）。谁在每个上有只读？谁有写？

5. Read the Cloudflare enterprise MCP post top to bottom. Identify one feature Cloudflare ships that this stdlib gateway does not.
   中文翻译：从头到尾阅读 Cloudflare 企业 MCP 帖子。识别 Cloudflare 发布但此标准库网关未提供的一个功能。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| Gateway | "MCP proxy" | Centralizing server between clients and backends | 网关：客户端和后端之间的集中化服务器 |
| Credential vaulting | "Backend tokens stay server-side" | Developers never see upstream tokens | 凭证保险库：后端 token 保留在服务端 |
| Session-aware routing | "Multi-backend session" | Gateway multiplexes N backend sessions per developer session | 会话感知路由：每开发者会话多路复用 N 个后端 |
| Tool-hash pinning | "Approved manifest" | SHA256 of every approved tool description; blocks rug-pulls centrally | 工具哈希锁定：审批清单防止地毯拉扯 |
| RBAC | "Per-user policy" | Role-based access control for tools and servers | 基于角色的访问控制 |
| Policy-as-code | "Declarative rules" | OPA/Rego, Kyverno, Styra policies enforced at gateway | 策略即代码：声明式规则在网关执行 |
| Audit log | "Who, what, when" | Append-only event log for compliance | 审计日志：仅追加的事件日志 |
| Rate limit | "Per-user token bucket" | Per-minute caps to prevent abuse | 限流：令牌桶算法防止滥用 |
| Official MCP Registry | "Canonical upstream" | `registry.modelcontextprotocol.io`, namespace-verified | 官方 MCP 注册中心：命名空间验证的权威源 |
| Reverse-DNS naming | "Registry namespace" | `io.github.user/server` convention | 反向 DNS 命名：注册中心命名空间约定 |

## Further Reading | 延伸阅读

- [Official MCP Registry](https://registry.modelcontextprotocol.io/) — canonical upstream, namespace-verified
  中文翻译：权威上游，命名空间验证
- [Cloudflare — Enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/) — gateway pattern with OAuth and policy
  中文翻译：带 OAuth 和策略的网关模式
- [agentic-community — MCP gateway registry](https://github.com/agentic-community/mcp-gateway-registry) — open-source reference gateway
  中文翻译：开源参考网关
- [TrueFoundry — What is an MCP gateway?](https://www.truefoundry.com/blog/what-is-mcp-gateway) — feature comparison article
  中文翻译：功能对比文章
- [IBM — MCP context forge](https://github.com/IBM/mcp-context-forge) — enterprise gateway from IBM
  中文翻译：IBM 的企业网关
