# MCP Security II — OAuth 2.1, Resource Indicators, Incremental Scopes | MCP 安全 II：OAuth 2.1、资源指示器与增量授权

> Remote MCP servers need authorization, not just authentication. The 2025-11-25 spec aligns with OAuth 2.1 + PKCE + resource indicators (RFC 8707) + protected-resource metadata (RFC 9728). SEP-835 adds incremental scope consent with step-up authorization on 403 WWW-Authenticate. This lesson implements the step-up flow as a state machine so you can see every hop.

> **【中文解读】** 远程 MCP 服务器需要授权（不只是认证）。2025-11-25 规范对齐 OAuth 2.1 + PKCE + 资源指示器（RFC 8707）+ 受保护资源元数据（RFC 9728）。SEP-835 增加了增量授权范围的逐步同意机制。本课将逐步授权流程实现为状态机，展示每一个步骤。

> **【拓展】** OAuth 2.1 是 MCP 远程服务器的标准认证方案。与早期 OAuth 2.0 相比，2.1 强制 PKCE、禁止隐式流程。资源指示器（RFC 8707）将 token 绑定到特定服务器，防止"混淆代理"攻击。逐步授权（Step-up）允许按需请求更多权限，而非一次性获取全部——这是最小权限原则的实践。

**Type:** Build
**Languages:** Python (stdlib, OAuth state machine simulator)
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 15 (security I)
**Time:** ~75 minutes

## Learning Objectives

- Distinguish resource server from authorization server responsibilities.
- Walk the PKCE-protected OAuth 2.1 authorization code flow.
- Use `resource` (RFC 8707) and protected-resource metadata (RFC 9728) to prevent confused-deputy attacks.
- Implement step-up authorization: server responds 403 with WWW-Authenticate asking for a higher scope; client re-prompts user consent and retries.

> **【中文解读】** 学习目标：区分资源服务器和授权服务器的职责；走通 PKCE 保护的 OAuth 2.1 授权码流程；使用资源指示器和受保护资源元数据防止混淆代理攻击；实现逐步授权（403 insufficient_scope 触发重新同意）。

## The Problem | 问题引入

> **【中文解读】** 早期 MCP 的远程服务器使用临时 API Key 甚至无认证。2025-11-25 规范通过完整 OAuth 2.1 配置关闭了这一差距。三个实际需求：(1) 普通远程服务器访问 Notion/GitHub/Gmail；(2) 范围升级——已有 notes:read 权限后需要 notes:write；(3) 混淆代理防御——防止服务器 A 的 token 被重放到服务器 B。

Early MCP (pre-2025) shipped remote servers with ad-hoc API keys or even no auth. The 2025-11-25 spec closes that gap with a full OAuth 2.1 profile.

Three real-world needs:

- **Ordinary remote servers.** User installs a remote MCP server that accesses their Notion / GitHub / Gmail. OAuth 2.1 with PKCE is the right shape.
- **Scope escalation.** A notes server granted `notes:read` can later need `notes:write` for a specific action. Instead of re-doing the whole flow, step-up (SEP-835) asks for the additional scope.
- **Confused deputy prevention.** Client holds a token audience-scoped for Server A. Server A is malicious and tries to present the token to Server B. Resource indicators (RFC 8707) pin the token to its intended audience.

OAuth 2.1 is not new. What is new is MCP's profile: specific required flows (authorization code + PKCE only; no implicit, no client credentials by default), resource indicators mandatory on every token request, and protected-resource metadata published so clients know where to go.

## The Concept | 核心概念

> **【中文解读】** 本节详解 OAuth 2.1 在 MCP 中的配置：角色划分、授权码+PKCE 流程、受保护资源元数据、资源指示器、范围模型、逐步授权、token 受众验证、短期 token 与轮换、无 token 透传、混淆代理防御等。

### Roles

- **Client.** The MCP client (Claude Desktop, Cursor, etc.).
- **Resource server.** The MCP server (notes, GitHub, Postgres, whatever).
- **Authorization server.** Issues tokens. May be the same service as the resource server or a separate IdP (Auth0, Keycloak, Cognito).

> **【中文解读】** 三个角色：Client（MCP 客户端，如 Claude Desktop）、Resource Server（MCP 服务器）、Authorization Server（签发 token 的授权服务器，可以是独立的 IdP）。

In MCP's profile, resource and authorization servers CAN be the same host but SHOULD be distinguished by URLs.

> **【拓展：MCP OAuth 2.1 配置的独特之处】** MCP 的 OAuth 2.1 配置不是标准 OAuth——它强制要求：(1) 只允许授权码+PKCE 流程，禁止隐式和客户端凭证模式；(2) 每次 token 请求必须包含资源指示器 (RFC 8707)；(3) 发布受保护资源元数据让客户端知道去哪里认证。这使得 MCP 的 OAuth 实现比一般 OAuth 更安全。

### Authorization code + PKCE

> **【中文解读】** 授权码+PKCE 流程：(1) 客户端生成 code_verifier（随机）和 code_challenge（SHA256）；(2) 重定向用户到 /authorize；(3) 用户同意，授权服务器重定向回 redirect_uri?code=...；(4) 客户端 POST 到 /token；(5) 验证 PKCE 后签发 access token；(6) 客户端使用 Bearer token 访问资源服务器。PKCE 防止授权码拦截，资源指示器防止 token 在其他地方有效。

The flow:

1. Client generates `code_verifier` (random) and `code_challenge` (SHA256).
2. Client redirects user to `/authorize?response_type=code&client_id=...&redirect_uri=...&scope=notes:read&code_challenge=...&resource=https://notes.example.com`.
3. User consents. Authorization server redirects to `redirect_uri?code=...`.
4. Client POSTs to `/token?grant_type=authorization_code&code=...&code_verifier=...&resource=...`.
5. Authorization server validates the verifier's hash against the stored challenge and issues an access token.
6. Client uses the token: `Authorization: Bearer ...` on every request to the resource server.

PKCE prevents authorization-code interception attacks. Resource indicators prevent the token from being valid elsewhere.

### Protected-resource metadata (RFC 9728)

> **【中文解读】** 受保护资源元数据：资源服务器发布 `.well-known/oauth-protected-resource` 文档，声明资源 URL、授权服务器列表和支持的范围。客户端从资源服务器发现授权服务器，减少配置。

The resource server publishes a `.well-known/oauth-protected-resource` document:

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:read", "notes:write", "notes:delete"]
}
```

Client discovers the authorization server from the resource server. Reduces configuration — the client only needs the resource URL.

### Resource indicators (RFC 8707)

> **【中文解读】** 资源指示器（RFC 8707）：token 请求中的 `resource` 参数将 token 绑定到目标受众。签发的 token 包含 `aud: "https://notes.example.com"`，其他 MCP 服务器检查 `aud` 并拒绝不匹配的 token。

`resource` parameter in the token request pins the token's intended audience. The issued token contains `aud: "https://notes.example.com"`. Another MCP server receiving this token checks `aud` and rejects it.

### Scope model

Scopes are space-separated strings. Common MCP conventions:

- `notes:read`, `notes:write`, `notes:delete`
- `admin:*` for admin capabilities (use sparingly)
- `profile:read` for identity

Scope selection should be least-privilege: request what you need now, step up when you need more.

### Step-up authorization (SEP-835)

> **【中文解读】** 逐步授权（SEP-835）：用户授予 notes:read 后需要删除笔记，服务器返回 403 + WWW-Authenticate 携带 insufficient_scope 错误和所需范围。客户端看到后弹出同意对话框获取额外范围，执行迷你 OAuth 流程，用新 token 重试请求。这是最小权限原则的实践。

User grants `notes:read`. They later ask the agent to delete a note. The server responds:

```
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
    scope="notes:delete", resource="https://notes.example.com"
```

Client sees the insufficient_scope error, prompts the user with a consent dialog for the additional scope, performs a mini OAuth flow for it, retries the request with the new token.

### Token audience validation

Every request: server checks `token.aud == self.resource_url`. Mismatch = 401. This stops cross-server token reuse.

### Short-lived tokens and rotation

Access tokens SHOULD be short-lived (1 hour default). Refresh tokens rotate on every refresh. The client handles silent refresh in the background.

### No token passthrough

Sampling servers (Phase 13 · 11) MUST NOT pass the client's token through to other services. The sampling request is the boundary.

### Confused deputy prevention

Token binds to `aud`. Client binds to `client_id`. Every request validated against both. The spec explicitly bans the old "pass-the-token" pattern that was common in pre-MCP remote tool ecosystems.

### Client ID discovery

Each MCP client publishes its metadata at a fixed URL. Authorization servers can fetch the client's metadata document to discover redirect URIs and contact info. This removes manual client registration.

### Gateways and OAuth

Phase 13 · 17 shows how an enterprise gateway handles OAuth: gateway holds credentials for upstream servers, tokens to the client are gateway-issued, and upstream tokens never leave the gateway. This flips the trust model — users authenticate with the gateway once; gateway handles N server authorizations.

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 将完整的 OAuth 2.1 逐步授权流程模拟为内存中的状态机：PKCE 生成、带资源指示器的授权码流程、受保护资源元数据端点、带受众检查的 token 验证、insufficient_scope 逐步升级。无 HTTP 服务器，状态机在内存中运行，便于追踪每一步。

`code/main.py` simulates the full OAuth 2.1 step-up flow as a state machine. It implements:

- PKCE code-verifier / challenge generation.
- Authorization code flow with resource indicator.
- Protected-resource metadata endpoint.
- Token validation with audience check.
- Step-up on `insufficient_scope`.

No HTTP server in this lesson; the state machine runs in memory so you can trace every hop. Phase 13 · 17's gateway lesson wires it to an actual transport.

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-oauth-scope-planner.md`——给定远程 MCP 服务器及其工具，设计范围集合、锁定规则和逐步授权策略。

This lesson produces `outputs/skill-oauth-scope-planner.md`. Given a remote MCP server with tools, the skill designs the scope set, pinning rules, and step-up policy.

## Exercises | 练习题

1. Run `code/main.py`. Trace the two-scope step-up flow. Note which hops repeat on step-up.

2. Add refresh-token rotation: every refresh issues a new refresh token and invalidates the old one. Simulate a stolen refresh token being used after rotation and confirm it fails.

3. Implement the protected-resource metadata endpoint as a real HTTP response using stdlib http.server. Mirror the /mcp endpoint from Lesson 09.

4. Design a scope hierarchy for a GitHub MCP server: read repo, write PR, approve PR, merge PR, admin. Use step-up between each level.

5. Read RFC 8707 and RFC 9728. Identify the one field in 9728 that MCP uses differently from the RFC's example. (Hint: it concerns `scopes_supported`.)

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| OAuth 2.1 | "Modern OAuth" | Consolidated RFC that mandates PKCE and forbids implicit flow | 现代 OAuth，强制 PKCE，禁止隐式流程 |
| PKCE | "Proof-of-possession" | Code verifier + challenge defeating authorization-code interception | 授权码交换证明密钥，防拦截 |
| Resource indicator | "Token audience" | RFC 8707 `resource` parameter pinning token to one server | 资源指示器，将 token 绑定到单个服务器 |
| Protected-resource metadata | "Discovery doc" | RFC 9728 `.well-known/oauth-protected-resource` | 受保护资源元数据发现文档 |
| Step-up authorization | "Incremental consent" | SEP-835 flow for adding scopes on demand | 逐步授权：按需增加权限范围 |
| `insufficient_scope` | "403 with WWW-Authenticate" | Server signal to re-consent for a larger scope | 权限不足信号，触发重新授权 |
| Confused deputy | "Token reuse across services" | Attack where a trusted holder forwards a token inappropriately | 混淆代理：token 跨服务重放攻击 |
| Short-lived token | "Access token TTL" | Bearer that expires quickly; refresh token renews | 短期 token，由 refresh token 续期 |
| Scope hierarchy | "Least privilege stack" | Graduated scope set with step-up between levels | 范围层级：最小权限堆栈 |
| Client ID metadata | "Client discovery doc" | URL at which the client publishes its own OAuth metadata | 客户端 ID 元数据发现文档 |

## Further Reading | 延伸阅读

- [MCP — Authorization spec](https://modelcontextprotocol.io/specification/draft/basic/authorization) — canonical MCP OAuth profile
- [den.dev — MCP November authorization spec](https://den.dev/blog/mcp-november-authorization-spec/) — walkthrough of the 2025-11-25 changes
- [RFC 8707 — Resource indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — the audience-pinning RFC
- [RFC 9728 — OAuth 2.0 protected resource metadata](https://datatracker.ietf.org/doc/html/rfc9728) — the discovery-document RFC
- [Aembit — MCP OAuth 2.1, PKCE and the future of AI authorization](https://aembit.io/blog/mcp-oauth-2-1-pkce-and-the-future-of-ai-authorization/) — practical step-up-flow walk-through
