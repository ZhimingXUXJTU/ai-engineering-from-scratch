# MCP Gateways and Registries — Enterprise Control Planes | MCP 网关与注册中心：企业控制平面

> Enterprises cannot let every dev install random MCP servers. A gateway centralizes auth, RBAC, audit, rate limiting, caching, and tool-poisoning detection, then exposes the merged tool surface as a single MCP endpoint. The Official MCP Registry (Anthropic + GitHub + PulseMCP + Microsoft, namespace-verified) is the canonical upstream. This lesson names where a gateway fits, walks a minimal implementation, and surveys the 2026 vendor landscape.

> **【中文解读】** 企业不能让每个开发者随意安装 MCP 服务器。网关集中处理认证、RBAC、审计、限流、缓存和工具投毒检测，将合并后的工具面暴露为单一 MCP 端点。官方 MCP 注册中心（Anthropic + GitHub + PulseMCP + Microsoft，命名空间验证）是权威上游源。

> **【拓展】** MCP 网关是企业部署 MCP 的核心架构模式。Cloudflare MCP Portals、Kong AI Gateway、IBM ContextForge 等都在 2025-2026 年推出了网关产品。网关模式将 Phase 13 · 15（工具投毒防御）和 Phase 13 · 16（OAuth 2.1）集中化执行，是企业安全合规的必备组件。

**Type:** Learn
**Languages:** Python (stdlib, minimal gateway)
**Prerequisites:** Phase 13 · 15 (tool poisoning), Phase 13 · 16 (OAuth 2.1)
**Time:** ~45 minutes

## Learning Objectives

- Explain where an MCP gateway sits (between MCP clients and multiple backend MCP servers).
- Implement the five gateway responsibilities: auth, RBAC, audit, rate limit, policy.
- Enforce a pinned-tool-hash manifest at the gateway layer.
- Differentiate the Official MCP Registry from metaregistries (Glama, MCPMarket, MCP.so, Smithery, LobeHub).

> **【中文解读】** 学习目标：理解网关在 MCP 客户端和多个后端 MCP 服务器之间的位置；实现五大网关职责（认证、RBAC、审计、限流、策略）；在网关层强制执行工具哈希锁定清单；区分官方 MCP 注册中心与元注册中心。

## The Problem

> **【中文解读】** Fortune 500 企业有 30 个审批的 MCP 服务器、5000 名开发者、合规审计要求。网关模式：(1) 网关作为单一 Streamable HTTP 端点运行；(2) 持有每个后端 MCP 服务器的凭证；(3) 每个开发者请求通过网关自身的 OAuth 认证和范围限制；(4) 网关路由调用到后端服务器并应用策略；(5) 所有调用记录用于审计。

A Fortune 500 has 30 approved MCP servers, 5000 developers, compliance and audit requirements, and a security team that wants centralized policy. Letting every developer install arbitrary servers in their IDEs is a non-starter.

The gateway pattern:

1. Gateway runs as a single Streamable HTTP endpoint developers connect to.
2. Gateway holds credentials for each backend MCP server.
3. Every developer request is authenticated and scoped via the gateway's own OAuth.
4. Gateway routes the call to the backend server, applying policy.
5. All calls logged for audit.

Cloudflare MCP Portals, Kong AI Gateway, IBM ContextForge, MintMCP, TrueFoundry, Envoy AI Gateway — all shipped gateways or gateway features in 2025-2026.

Meanwhile, the Official MCP Registry launched as the canonical upstream: curated, namespace-verified, reverse-DNS-named servers the gateway can pull from. Metaregistries (Glama, MCPMarket, MCP.so, Smithery, LobeHub) aggregate servers across multiple sources.

## The Concept

> **【中文解读】** 本节详解五大网关职责、网关作为单一端点、凭证保险库、工具哈希锁定、策略即代码、会话感知路由、命名空间合并、注册中心生态和供应商格局。

### Five gateway responsibilities

> **【中文解读】** 五大网关职责：(1) 认证——OAuth 2.1 识别开发者，映射到用户角色；(2) RBAC——每用户策略：哪些服务器、哪些工具、哪些范围；(3) 审计——每次调用记录谁、做了什么、何时、结果；(4) 限流——每用户/每工具/每服务器上限；(5) 策略——拒绝投毒描述、强制 Rule of Two、脱敏 PII。

1. **Auth.** OAuth 2.1 to identify the developer; maps to user roles.
2. **RBAC.** Per-user policy: which servers, which tools, which scopes.
3. **Audit.** Every call logged with who, what, when, result.
4. **Rate limit.** Per-user / per-tool / per-server caps to prevent abuse.
5. **Policy.** Reject poisoned descriptions, enforce Rule of Two, redact PII.

### Gateway as a single endpoint

To developers, the gateway looks like one MCP server. Internally it routes to N backends. Session ids (Phase 13 · 09) are rewritten at the boundary.

### Credential vaulting

Developers never see backend tokens. The gateway holds them (or proxies to an identity provider that does). A developer with `notes:read` on the gateway may transitively access the notes MCP server with the gateway's own backend credentials — but only under policy that binds the transitive access.

### Tool-hash pinning at the gateway

The gateway holds a manifest of approved tool descriptions (SHA256 hashes). At discovery time, it fetches each backend's `tools/list`, compares hashes to the manifest, and removes any tool whose description has mutated. This is the rug-pull defense from Phase 13 · 15 applied centrally.

### Policy-as-code

Advanced gateways express policy in OPA/Rego, Kyverno, or Styra. Rules like "user `alice` may call `github.open_pr` only on repos in org `acme`" are encoded declaratively. Simple gateways use hand-coded Python. Both shapes are valid.

### Session-aware routing

When a user's session includes a mix of servers, the gateway multiplexes: the developer's single MCP session holds N backend sessions, one per server. Notifications from any backend route through the gateway to the developer's session.

### Namespace merging

Gateways merge tool namespaces from all backends, typically with prefix-on-collision. `github.open_pr`, `notes.search`. This makes routing unambiguous.

### Registries

- **Official MCP Registry (`registry.modelcontextprotocol.io`).** Launched under Anthropic, GitHub, PulseMCP, Microsoft stewardship. Namespace-verified (reverse-DNS: `io.github.user/server`). Pre-filtered for basic quality.
- **Glama.** Search-centric metaregistry aggregating many sources.
- **MCPMarket.** Commercial-leaning directory with vendor listings.
- **MCP.so.** Community directory; open submissions.
- **Smithery.** Package-manager-style installation flow.
- **LobeHub.** UI-integrated registry in their LobeChat app.

Enterprise gateways pull from the Official Registry by default, allow admin-curated additions from metaregistries, and reject anything unpinned.

### Reverse-DNS naming

Official Registry mandates reverse-DNS names for public servers: `io.github.alice/notes`. Namespaces prevent squatting and make trust delegation clearer.

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

## Use It

> **【中文解读】** `code/main.py` 实现约150行的最小网关：通过 Bearer token 认证用户、每用户 RBAC 策略、路由到两个后端 MCP 服务器、写入审计日志、令牌桶限流、拒绝描述哈希不匹配的后端工具。关注点：RBAC 字典按 user_id 索引、AUDIT_LOG 是追加事件列表、令牌桶限流每用户、锁定清单为 server::tool -> hash 映射。

`code/main.py` ships a minimal gateway in ~150 lines: authenticates users by a fake Bearer token, holds a per-user RBAC policy, routes requests to two backend MCP servers, writes every call to an audit log, enforces a rate limit, and rejects any backend tool whose description hash does not match a pinned manifest.

What to look at:

- `RBAC` dict keyed by `user_id` with allowed `server_tool` entries.
- `AUDIT_LOG` is an append-only list of events.
- Rate limit uses a token bucket per user.
- Pinned manifest is a dict of `server::tool -> hash`.

## Ship It

> **【中文解读】** 本课产出 `outputs/skill-gateway-bootstrap.md`——给定企业 MCP 计划（用户、后端、合规要求），生成网关配置规格。

This lesson produces `outputs/skill-gateway-bootstrap.md`. Given an enterprise MCP plan (users, backends, compliance), the skill produces a gateway configuration spec.

## Exercises

1. Run `code/main.py`. Make a call as an allowed user; then as a disallowed user; then a rate-limit-exceeded burst. Verify all three flows.

2. Add a policy that redacts PII from results before returning to the client. Use a simple regex pass for SSN-shaped strings; note the gap (emails, phone numbers).

3. Extend the audit log to emit OpenTelemetry GenAI spans. Phase 13 · 20 covers the exact attributes.

4. Design an RBAC policy for a 50-developer team with five backends (notes, github, postgres, jira, slack). Who gets read-only on each? Who gets write?

5. Read the Cloudflare enterprise MCP post top to bottom. Identify one feature Cloudflare ships that this stdlib gateway does not.

## Key Terms

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

## Further Reading

- [Official MCP Registry](https://registry.modelcontextprotocol.io/) — canonical upstream, namespace-verified
- [Cloudflare — Enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/) — gateway pattern with OAuth and policy
- [agentic-community — MCP gateway registry](https://github.com/agentic-community/mcp-gateway-registry) — open-source reference gateway
- [TrueFoundry — What is an MCP gateway?](https://www.truefoundry.com/blog/what-is-mcp-gateway) — feature comparison article
- [IBM — MCP context forge](https://github.com/IBM/mcp-context-forge) — enterprise gateway from IBM
