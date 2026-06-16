# MCP Security II — OAuth 2.1, Resource Indicators, Incremental Scopes | MCP 安全 II：OAuth 2.1、资源指示器与增量授权

> Remote MCP servers need authorization, not just authentication. The 2025-11-25 spec aligns with OAuth 2.1 + PKCE + resource indicators (RFC 8707) + protected-resource metadata (RFC 9728). SEP-835 adds incremental scope consent with step-up authorization on 403 WWW-Authenticate. This lesson implements the step-up flow as a state machine so you can see every hop.

> **【中文解读】** 远程 MCP 服务器需要授权（不只是认证）。2025-11-25 规范对齐 OAuth 2.1 + PKCE + 资源指示器（RFC 8707）+ 受保护资源元数据（RFC 9728）。SEP-835 增加了增量授权范围的逐步同意机制。本课将逐步授权流程实现为状态机，展示每一个步骤。

> **【拓展】** OAuth 2.1 是 MCP 远程服务器的标准认证方案。与早期 OAuth 2.0 相比，2.1 强制 PKCE、禁止隐式流程。资源指示器（RFC 8707）将 token 绑定到特定服务器，防止"混淆代理"攻击。逐步授权（Step-up）允许按需请求更多权限，而非一次性获取全部——这是最小权限原则的实践。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·09（MCP transports）——Streamable HTTP 才需要 OAuth；(2) Phase 13·15（MCP Security I）——理解威胁面；(3) OAuth 2.0/2.1 概念、PKCE 流程、JWT/Bearer token 基础；(4) RFC 8707（资源指示器）和 RFC 9728（受保护资源元数据）——本节会用到。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, OAuth state machine simulator) | **语言:** Python (stdlib, OAuth state machine simulator)
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 15 (security I) | **前置知识:** Phase 13 · 09 (transports), Phase 13 · 15 (security I)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Distinguish resource server from authorization server responsibilities.
  中文翻译：区分资源服务器和授权服务器的职责。
- Walk the PKCE-protected OAuth 2.1 authorization code flow.
  中文翻译：走通 PKCE 保护的 OAuth 2.1 授权码流程。
- Use `resource` (RFC 8707) and protected-resource metadata (RFC 9728) to prevent confused-deputy attacks.
  中文翻译：使用 `resource`（RFC 8707）和受保护资源元数据（RFC 9728）防止混淆代理攻击。
- Implement step-up authorization: server responds 403 with WWW-Authenticate asking for a higher scope; client re-prompts user consent and retries.
  中文翻译：实现逐步授权：服务器响应 403 带 WWW-Authenticate 请求更高范围；客户端重新提示用户同意并重试。

> **【中文解读】** 学习目标：区分资源服务器和授权服务器的职责；走通 PKCE 保护的 OAuth 2.1 授权码流程；使用资源指示器和受保护资源元数据防止混淆代理攻击；实现逐步授权（403 insufficient_scope 触发重新同意）。

## The Problem | 问题引入

> **【中文解读】** 早期 MCP 的远程服务器使用临时 API Key 甚至无认证。2025-11-25 规范通过完整 OAuth 2.1 配置关闭了这一差距。三个实际需求：(1) 普通远程服务器访问 Notion/GitHub/Gmail；(2) 范围升级——已有 notes:read 权限后需要 notes:write；(3) 混淆代理防御——防止服务器 A 的 token 被重放到服务器 B。

Early MCP (pre-2025) shipped remote servers with ad-hoc API keys or even no auth. The 2025-11-25 spec closes that gap with a full OAuth 2.1 profile.

> 早期 MCP（pre-2025）发布带临时 API 密钥甚至无认证的远程服务器。2025-11-25 规范用完整的 OAuth 2.1 配置关闭了这一差距。

Three real-world needs:

> 三个现实需求：

- **Ordinary remote servers.** User installs a remote MCP server that accesses their Notion / GitHub / Gmail. OAuth 2.1 with PKCE is the right shape.
  中文翻译：**普通远程服务器。** 用户安装访问其 Notion/GitHub/Gmail 的远程 MCP 服务器。带 PKCE 的 OAuth 2.1 是正确形态。
- **Scope escalation.** A notes server granted `notes:read` can later need `notes:write` for a specific action. Instead of re-doing the whole flow, step-up (SEP-835) asks for the additional scope.
  中文翻译：**范围升级。** 已授予 `notes:read` 的笔记服务器之后可能需要 `notes:write` 执行特定动作。逐步授权（SEP-835）请求额外范围而非重做整个流程。
- **Confused deputy prevention.** Client holds a token audience-scoped for Server A. Server A is malicious and tries to present the token to Server B. Resource indicators (RFC 8707) pin the token to its intended audience.
  中文翻译：**混淆代理预防。** 客户端持有 audience-scoped 给服务器 A 的 token。服务器 A 恶意并尝试向服务器 B 呈现 token。资源指示器（RFC 8707）将 token 固定到其预期受众。

OAuth 2.1 is not new. What is new is MCP's profile: specific required flows (authorization code + PKCE only; no implicit, no client credentials by default), resource indicators mandatory on every token request, and protected-resource metadata published so clients know where to go.

> OAuth 2.1 不是新的。新的是 MCP 的配置：特定必需流程（仅授权码+PKCE；默认无隐式、无客户端凭证），每次 token 请求必须带资源指示器，发布受保护资源元数据让客户端知道去哪里。

> 💡 **【类比】** OAuth 2.1 + PKCE 像酒店代客停车。普通 OAuth 2.0（无 PKCE）像你直接把车钥匙给代客（access token），代客可去任何地方——风险高。OAuth 2.1 + PKCE：你给代客一个"专用临时钥匙"（PKCE challenge），这把钥匙只能启动你的车（resource indicator 锁定），代客没法用这把钥匙开别人的车（混淆代理防御）。Step-up 授权：代客原本只能停车，你要他顺便加油，临时升级权限（重新走同意流程），办完事降回原权限——最小权限原则。

## The Concept | 核心概念

> **【中文解读】** 本节详解 OAuth 2.1 在 MCP 中的配置：角色划分、授权码+PKCE 流程、受保护资源元数据、资源指示器、范围模型、逐步授权、token 受众验证、短期 token 与轮换、无 token 透传、混淆代理防御等。

### Roles

- **Client.** The MCP client (Claude Desktop, Cursor, etc.).
  中文翻译：**Client。** MCP 客户端（Claude Desktop、Cursor 等）。
- **Resource server.** The MCP server (notes, GitHub, Postgres, whatever).
  中文翻译：**Resource server。** MCP 服务器（笔记、GitHub、Postgres 等）。
- **Authorization server.** Issues tokens. May be the same service as the resource server or a separate IdP (Auth0, Keycloak, Cognito).
  中文翻译：**Authorization server。** 签发 token。可以是与资源服务器相同的服务或独立 IdP（Auth0、Keycloak、Cognito）。

> **【中文解读】** 三个角色：Client（MCP 客户端，如 Claude Desktop）、Resource Server（MCP 服务器）、Authorization Server（签发 token 的授权服务器，可以是独立的 IdP）。

In MCP's profile, resource and authorization servers CAN be the same host but SHOULD be distinguished by URLs.

> 在 MCP 的配置中，资源服务器和授权服务器可以是同一主机，但应通过 URL 区分。

> **【拓展：MCP OAuth 2.1 配置的独特之处】** MCP 的 OAuth 2.1 配置不是标准 OAuth——它强制要求：(1) 只允许授权码+PKCE 流程，禁止隐式和客户端凭证模式；(2) 每次 token 请求必须包含资源指示器 (RFC 8707)；(3) 发布受保护资源元数据让客户端知道去哪里认证。这使得 MCP 的 OAuth 实现比一般 OAuth 更安全。

### Authorization code + PKCE

> **【中文解读】** 授权码+PKCE 流程：(1) 客户端生成 code_verifier（随机）和 code_challenge（SHA256）；(2) 重定向用户到 /authorize；(3) 用户同意，授权服务器重定向回 redirect_uri?code=...；(4) 客户端 POST 到 /token；(5) 验证 PKCE 后签发 access token；(6) 客户端使用 Bearer token 访问资源服务器。PKCE 防止授权码拦截，资源指示器防止 token 在其他地方有效。

The flow:

1. Client generates `code_verifier` (random) and `code_challenge` (SHA256).
  中文翻译：客户端生成 `code_verifier`（随机）和 `code_challenge`（SHA256）。
2. Client redirects user to `/authorize?response_type=code&client_id=...&redirect_uri=...&scope=notes:read&code_challenge=...&resource=https://notes.example.com`.
  中文翻译：客户端重定向用户到 `/authorize?...`。
3. User consents. Authorization server redirects to `redirect_uri?code=...`.
  中文翻译：用户同意。授权服务器重定向到 `redirect_uri?code=...`。
4. Client POSTs to `/token?grant_type=authorization_code&code=...&code_verifier=...&resource=...`.
  中文翻译：客户端 POST 到 `/token?...`。
5. Authorization server validates the verifier's hash against the stored challenge and issues an access token.
  中文翻译：授权服务器验证 verifier 的哈希与存储的 challenge 并签发 access token。
6. Client uses the token: `Authorization: Bearer ...` on every request to the resource server.
  中文翻译：客户端使用 token：每次请求资源服务器带 `Authorization: Bearer ...`。

PKCE prevents authorization-code interception attacks. Resource indicators prevent the token from being valid elsewhere.

> PKCE 防止授权码拦截攻击。资源指示器防止 token 在其他地方有效。

> ⚠️ **【易错点】** 场景：客户端忽略 `resource` 参数 / 后果：拿到 Server A 的 token 后被 Server A 转交给 Server B 使用（混淆代理攻击），因为 token 没有 audience 锁定 / 修复：(1) 每次 `/token` 请求必须带 `resource=<服务器 URL>`；(2) 资源服务器校验 token 的 audience 字段是否匹配自己；(3) 短期 token（< 1 小时）+ refresh token 轮换；(4) 永远不要让 token 在不同服务器间共享——MCP 规范明确禁止 token 透传。

> 🤔 **【困惑】** Q: 为什么 MCP 强制用 PKCE？普通授权码流程不是也有吗？ A: 因为 MCP client 通常不是机密的——Claude Desktop、Cursor 装在用户机器上，client_secret 会被反编译出来。PKCE 让 client 不存 secret，每次请求生成临时 verifier，授权服务器只验证哈希匹配。这样即使攻击者拿到客户端代码也无法伪造请求。OAuth 2.1 把"PKCE 选填"升级为"PKCE 必填"，就是为移动/桌面端 client 设计的。

### Protected-resource metadata (RFC 9728)

> **【中文解读】** 受保护资源元数据：资源服务器发布 `.well-known/oauth-protected-resource` 文档，声明资源 URL、授权服务器列表和支持的范围。客户端从资源服务器发现授权服务器，减少配置。

The resource server publishes a `.well-known/oauth-protected-resource` document:

> 资源服务器发布 `.well-known/oauth-protected-resource` 文档：

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:read", "notes:write", "notes:delete"]
}
```

Client discovers the authorization server from the resource server. Reduces configuration — the client only needs the resource URL.

> 客户端从资源服务器发现授权服务器。减少配置——客户端只需要资源 URL。

### Resource indicators (RFC 8707)

> **【中文解读】** 资源指示器（RFC 8707）：token 请求中的 `resource` 参数将 token 绑定到目标受众。签发的 token 包含 `aud: "https://notes.example.com"`，其他 MCP 服务器检查 `aud` 并拒绝不匹配的 token。

`resource` parameter in the token request pins the token's intended audience. The issued token contains `aud: "https://notes.example.com"`. Another MCP server receiving this token checks `aud` and rejects it.

> token 请求中的 `resource` 参数将 token 固定到其预期受众。签发的 token 包含 `aud: "https://notes.example.com"`。其他 MCP 服务器收到此 token 时检查 `aud` 并拒绝。

### Scope model

Scopes are space-separated strings. Common MCP conventions:

> Scope 是空格分隔的字符串。常见 MCP 约定：

- `notes:read`, `notes:write`, `notes:delete`
  中文翻译：`notes:read`、`notes:write`、`notes:delete`——笔记读/写/删。
- `admin:*` for admin capabilities (use sparingly)
  中文翻译：`admin:*`——管理能力（谨慎使用）。
- `profile:read` for identity
  中文翻译：`profile:read`——身份信息。

Scope selection should be least-privilege: request what you need now, step up when you need more.

> Scope 选择应是最小权限：请求当前所需，需要更多时逐步升级。

### Step-up authorization (SEP-835)

> **【中文解读】** 逐步授权（SEP-835）：用户授予 notes:read 后需要删除笔记，服务器返回 403 + WWW-Authenticate 携带 insufficient_scope 错误和所需范围。客户端看到后弹出同意对话框获取额外范围，执行迷你 OAuth 流程，用新 token 重试请求。这是最小权限原则的实践。

User grants `notes:read`. They later ask the agent to delete a note. The server responds:

> 用户授予 `notes:read`。他们之后要求 Agent 删除笔记。服务器响应：

```
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
    scope="notes:delete", resource="https://notes.example.com"
```

Client sees the insufficient_scope error, prompts the user with a consent dialog for the additional scope, performs a mini OAuth flow for it, retries the request with the new token.

> 客户端看到 insufficient_scope 错误，用同意对话框提示用户授予额外范围，执行 mini OAuth 流程，用新 token 重试请求。

### Token audience validation

Every request: server checks `token.aud == self.resource_url`. Mismatch = 401. This stops cross-server token reuse.

> 每次请求：服务器检查 `token.aud == self.resource_url`。不匹配 = 401。这阻止跨服务器 token 重用。

### Short-lived tokens and rotation

Access tokens SHOULD be short-lived (1 hour default). Refresh tokens rotate on every refresh. The client handles silent refresh in the background.

> Access token 应短生命周期（默认 1 小时）。Refresh token 每次刷新轮换。客户端在后台静默刷新。

### No token passthrough

Sampling servers (Phase 13 · 11) MUST NOT pass the client's token through to other services. The sampling request is the boundary.

> Sampling 服务器（Phase 13 · 11）不得将客户端的 token 透传给其他服务。Sampling 请求是边界。

### Confused deputy prevention

Token binds to `aud`. Client binds to `client_id`. Every request validated against both. The spec explicitly bans the old "pass-the-token" pattern that was common in pre-MCP remote tool ecosystems.

> Token 绑定到 `aud`。客户端绑定到 `client_id`。每次请求对两者验证。规范明确禁止 pre-MCP 远程工具生态中常见的旧 "pass-the-token" 模式。

### Client ID discovery

Each MCP client publishes its metadata at a fixed URL. Authorization servers can fetch the client's metadata document to discover redirect URIs and contact info. This removes manual client registration.

> 每个 MCP 客户端在固定 URL 发布其元数据。授权服务器可获取客户端的元数据文档以发现 redirect URI 和联系信息。这消除了手动客户端注册。

### Gateways and OAuth

Phase 13 · 17 shows how an enterprise gateway handles OAuth: gateway holds credentials for upstream servers, tokens to the client are gateway-issued, and upstream tokens never leave the gateway. This flips the trust model — users authenticate with the gateway once; gateway handles N server authorizations.

> Phase 13 · 17 展示企业网关如何处理 OAuth：网关持有上游服务器凭证，给客户端的 token 由网关签发，上游 token 永不离开网关。这翻转了信任模型——用户与网关认证一次；网关处理 N 个服务器授权。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 将完整的 OAuth 2.1 逐步授权流程模拟为内存中的状态机：PKCE 生成、带资源指示器的授权码流程、受保护资源元数据端点、带受众检查的 token 验证、insufficient_scope 逐步升级。无 HTTP 服务器，状态机在内存中运行，便于追踪每一步。

`code/main.py` simulates the full OAuth 2.1 step-up flow as a state machine. It implements:

> `code/main.py` 将完整 OAuth 2.1 逐步授权流程模拟为状态机。它实现：

- PKCE code-verifier / challenge generation.
  中文翻译：PKCE code-verifier/challenge 生成。
- Authorization code flow with resource indicator.
  中文翻译：带资源指示器的授权码流程。
- Protected-resource metadata endpoint.
  中文翻译：受保护资源元数据端点。
- Token validation with audience check.
  中文翻译：带受众检查的 token 验证。
- Step-up on `insufficient_scope`.
  中文翻译：`insufficient_scope` 上的逐步升级。

No HTTP server in this lesson; the state machine runs in memory so you can trace every hop. Phase 13 · 17's gateway lesson wires it to an actual transport.

> 本课无 HTTP 服务器；状态机在内存中运行，便于追踪每一步。Phase 13 · 17 的网关课程将其连接到实际传输。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-oauth-scope-planner.md`——给定远程 MCP 服务器及其工具，设计范围集合、锁定规则和逐步授权策略。

This lesson produces `outputs/skill-oauth-scope-planner.md`. Given a remote MCP server with tools, the skill designs the scope set, pinning rules, and step-up policy.

> 本课产出 `outputs/skill-oauth-scope-planner.md`。给定一个带工具的远程 MCP 服务器，该 skill 设计 scope 集合、固定规则和逐步授权策略。

## Exercises | 练习题

1. Run `code/main.py`. Trace the two-scope step-up flow. Note which hops repeat on step-up.
   中文翻译：运行 `code/main.py`。追踪双 scope 逐步授权流程。注意哪些步骤在升级时重复。

2. Add refresh-token rotation: every refresh issues a new refresh token and invalidates the old one. Simulate a stolen refresh token being used after rotation and confirm it fails.
   中文翻译：添加 refresh-token 轮换：每次刷新签发新 refresh token 并使旧 token 失效。模拟偷来的 refresh token 在轮换后被使用，确认它失败。

3. Implement the protected-resource metadata endpoint as a real HTTP response using stdlib http.server. Mirror the /mcp endpoint from Lesson 09.
   中文翻译：用 stdlib http.server 实现受保护资源元数据端点为真实 HTTP 响应。镜像 Lesson 09 的 `/mcp` 端点。

4. Design a scope hierarchy for a GitHub MCP server: read repo, write PR, approve PR, merge PR, admin. Use step-up between each level.
   中文翻译：为 GitHub MCP 服务器设计 scope 层级：read repo、write PR、approve PR、merge PR、admin。每层之间使用逐步授权。

5. Read RFC 8707 and RFC 9728. Identify the one field in 9728 that MCP uses differently from the RFC's example. (Hint: it concerns `scopes_supported`.)
   中文翻译：阅读 RFC 8707 和 RFC 9728。识别 9728 中 MCP 与 RFC 示例使用不同的一个字段。（提示：与 `scopes_supported` 有关。）

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
  中文翻译：权威 MCP OAuth 配置
- [den.dev — MCP November authorization spec](https://den.dev/blog/mcp-november-authorization-spec/) — walkthrough of the 2025-11-25 changes
  中文翻译：2025-11-25 变更演练
- [RFC 8707 — Resource indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — the audience-pinning RFC
  中文翻译：受众固定 RFC
- [RFC 9728 — OAuth 2.0 protected resource metadata](https://datatracker.ietf.org/doc/html/rfc9728) — the discovery-document RFC
  中文翻译：发现文档 RFC
- [Aembit — MCP OAuth 2.1, PKCE and the future of AI authorization](https://aembit.io/blog/mcp-oauth-2-1-pkce-and-the-future-of-ai-authorization/) — practical step-up-flow walk-through
  中文翻译：实用逐步授权流程演练
