# MCP Auth in Production: Issuer-Bound Enrollment and Tokens | MCP 生产级认证：签发者绑定的注册与 Token

> Lesson 16 built the OAuth 2.1 state machine. This lesson hardens its production boundaries for MCP 2026-07-28: Client ID Metadata Documents first, deprecated dynamic registration only for compatibility, authorization-response issuer validation, issuer-keyed client credentials, JWKS refresh, and audience-pinned tokens on every stateless request.
>
> **Spec note (2026-07-28):** Dynamic Client Registration is deprecated in favor of Client ID Metadata Documents. DCR remains a compatibility mechanism. When it is used, the client declares the correct `application_type`. A client validates a present RFC 9207 `iss` value and never reuses credentials across authorization-server issuers.

> **【中文解读】** 第 16 课搭起了 OAuth 2.1 状态机；本课把它的边界加固到 MCP 2026-07-28 规范的生产要求：注册优先走 Client ID Metadata Document（CIMD），DCR 降级为仅作兼容的已弃用路径；授权响应必须校验 RFC 9207 `iss`；客户端凭证按签发者隔离存放；JWKS 按计划刷新；每个无状态请求都做受众绑定检查。核心变化是"每个请求独立验证"——协议会话被移除后，不存在任何可以缓存身份决定的地方。

> **【拓展：MCP 2026-07-28 的注册范式转向】** 这一版规范把注册从"推"（DCR 的 `POST /register`）改为"拉"（CIMD：授权服务器按需拉取客户端自托管的元数据文档），信任锚从 IdP 的内部状态转移到 DNS；同时凭证按签发者隔离、token 按（签发者, 资源）成对存储，堵住跨 IdP 复用凭证与跨资源重放 token 的攻击面。同一版规范还移除了协议会话（见第 23 课毕业项目），这正是"每个请求都要重新验证"的根源。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13 · 16（OAuth 2.1 状态机、PKCE、资源指示器）——本课是其生产化；(2) Phase 13 · 17（网关）；(3) JWT 结构与 JWKS 概念；(4) 本课将逐一实现的规范：RFC 8414（AS 元数据）、RFC 7591（DCR）、RFC 8707（资源指示器）、RFC 9728（PR 元数据）、RFC 9207（iss 参数）、RFC 7636（PKCE）、RFC 7662（token 内省）、RFC 7009（token 吊销）。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 16 (OAuth 2.1 state machine), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 16（OAuth 2.1 状态机）、Phase 13 · 17（网关）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Discover an authorization server through RFC 8414 metadata and verify the contract.
  中文翻译：通过 RFC 8414 元数据发现授权服务器并验证契约。
- Enroll through a Client ID Metadata Document and isolate deprecated DCR as a fallback.
  中文翻译：通过 Client ID Metadata Document 完成注册，并把已弃用的 DCR 隔离为后备路径。
- Validate RFC 9207 `iss`, key registrations by authorization-server issuer, and key resource-bound tokens by issuer plus resource.
  中文翻译：校验 RFC 9207 `iss`；注册信息按授权服务器签发者做键；资源绑定的 token 按"签发者 + 资源"成对做键。
- Cache and refresh JWKS keys on a schedule so signature verification survives key roll-over.
  中文翻译：按计划缓存并刷新 JWKS 密钥，使签名验证在密钥轮换后依然存活。
- Pin tokens to a single MCP resource using RFC 8707 resource indicators and refuse confused-deputy reuse.
  中文翻译：用 RFC 8707 资源指示器把 token 固定到单个 MCP 资源，拒绝混淆代理式重用。
- Choose JWT validation or token introspection, define revocation freshness, and fail safely when identity dependencies are unavailable.
  中文翻译：在 JWT 校验与 token 内省之间做出选择、定义吊销新鲜度，并在身份依赖不可用时安全失败。
- Separate the authorization server, resource server, and client so each enforces only its own checks.
  中文翻译：把授权服务器、资源服务器和客户端分开，使每一方只执行属于自己的检查。
- Audit an authorization server against a deployment checklist and refuse unsafe enrollment or token reuse.
  中文翻译：按部署检查清单审计授权服务器，拒绝不安全的注册或 token 复用。

## The Problem | 问题引入

> **【中文解读】** 三个生产缺口：(1) 注册与凭证隔离——CIMD 优先、DCR 仅作兼容，且凭证必须按签发者隔离；(2) 密钥轮换——JWKS 缓存必须有刷新任务加回退获取；(3) 受众绑定——`token.aud` 与资源 URL 的比对是每个请求上的硬性检查，也是唯一防跨资源重放的手段。

The Lesson 16 simulator runs OAuth 2.1 in memory. Production has three operational gaps that a memory-only simulator does not see.

> 第 16 课的模拟器在内存中运行 OAuth 2.1。生产环境有三个内存模拟器看不到的操作缺口。

The first gap is enrollment and credential isolation. A real org may run hundreds of MCP servers and thousands of MCP clients. The 2026-07-28 revision prefers a **Client ID Metadata Document**: the client uses an HTTPS URL with a path that it controls as its identifier, and the authorization server pulls the metadata. RFC 7591 dynamic registration remains only as a deprecated compatibility path. When DCR is unavoidable, the request declares the correct `application_type`. The client stores registrations under the authorization-server issuer and access tokens under the `(issuer, resource)` pair. A changed issuer means a new enrollment, and a different resource means a separately audience-bound token.

> 第一个缺口是注册与凭证隔离。真实组织可能运行数百个 MCP 服务器和数千个 MCP 客户端。2026-07-28 修订版优先采用 **Client ID Metadata Document**：客户端用一个自己控制的带路径 HTTPS URL 作为标识符，授权服务器主动拉取元数据。RFC 7591 动态注册仅作为已弃用的兼容路径保留。当 DCR 无法避免时，请求必须声明正确的 `application_type`。客户端把注册信息按授权服务器签发者存储，把 access token 按 `(issuer, resource)` 对存储。签发者变了就要重新注册；资源不同就要单独做受众绑定。

The second gap is key rotation. JWT validation depends on the authorization server's signing keys, published as a JSON Web Key Set (JWKS). The authorization server rotates these on a schedule (often hourly, sometimes faster under incident response). An MCP server that fetches JWKS once at boot validates fine until the rotation window — then every request fails until restart. Production wires JWKS as a cached value with a refresh job that overwrites the cache before the previous keys expire, plus a fall-back fetch on cache miss for the case where a token signed by a key newer than the cache arrives.

> 第二个缺口是密钥轮换。JWT 验证依赖授权服务器的签名密钥，以 JSON Web Key Set（JWKS）形式发布。授权服务器按计划轮换这些密钥（通常每小时，事件响应时更快）。只在启动时获取一次 JWKS 的 MCP 服务器在轮换窗口到来前验证正常——之后所有请求失败，直到重启。生产环境把 JWKS 连线为缓存值：刷新任务在旧密钥过期前覆盖缓存，另加缓存未命中时的回退获取，以处理"token 由比缓存更新的密钥签名"的情况。

The third gap is audience binding. Lesson 16 introduced RFC 8707 resource indicators. In production, that indicator becomes a hard claim check on every request. The MCP server compares `token.aud` against its own canonical resource URL and rejects mismatches with HTTP 401. This is the only defense against an upstream MCP server (or a malicious client holding a token meant for one server) replaying that token against another server in the same trust mesh.

> 第三个缺口是受众绑定。第 16 课引入了 RFC 8707 资源指示器。在生产中，该指示器成为每个请求上的硬性声明检查。MCP 服务器把 `token.aud` 与自身的规范资源 URL 比对，不匹配就以 HTTP 401 拒绝。这是防御上游 MCP 服务器（或持有发给某一服务器的 token 的恶意客户端）在同一信任网格内把 token 重放给另一个服务器的唯一手段。

This lesson maps each gap onto a concrete piece of the surface. The metadata document is an HTTP endpoint. JWKS cache refresh is a scheduled job plus a key-value cache. JWT validation is a routine the resource server runs before dispatching any tool. Keep the three roles separate and each one enforces only the checks it owns: the authorization server issues and rotates keys, the resource server caches and validates, the client discovers and enrolls.

> 本课把每个缺口映射为认证面上的一个具体构件：元数据文档是一个 HTTP 端点；JWKS 缓存刷新是一个定时任务加一个键值缓存；JWT 验证是资源服务器在分发任何工具之前执行的一道例程。保持三个角色分离，每一方只执行属于自己的检查：授权服务器签发并轮换密钥，资源服务器缓存并验证，客户端发现并注册。

## Scope: Production Enforcement After Lesson 16 | 范围：第 16 课之后的生产强化

> **【中文解读】** 本课不重新定义 OAuth 流程——授权码状态机、PKCE、受保护资源发现、资源指示器都属于第 16 课。本课从这些契约已经存在之后开始：一个已部署的资源服务器如何在密钥轮换、不透明 token、吊销、依赖故障、灰度与事件响应中持续执行这些契约。

[Lesson 16: MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md) owns the authorization-code state machine, PKCE, protected-resource discovery, resource indicators, and scope decisions. This lesson does not define a second OAuth flow. It starts after those contracts exist and asks how a deployed resource server keeps enforcing them during key rotation, opaque-token validation, revocation, dependency failure, rollout, and incident response.

> [第 16 课：MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md) 负责授权码状态机、PKCE、受保护资源发现、资源指示器和 scope 决策。本课不定义第二个 OAuth 流程。它从这些契约已经存在之后开始，追问一个已部署的资源服务器如何在密钥轮换、不透明 token 校验、吊销、依赖故障、灰度发布和事件响应期间持续执行这些契约。

The production boundary is narrower and more operational:

> 生产边界更窄、更偏运维：

- A JWT path verifies a pinned issuer, algorithm, signature key, audience, time claims, and scopes on every request while refreshing JWKS safely.
  中文翻译：JWT 路径在每个请求上校验锁定的签发者、算法、签名密钥、受众、时间声明和 scope，同时安全地刷新 JWKS。
- An opaque-token path calls the issuer's authenticated introspection endpoint and validates the returned active state, audience or resource, expiry, subject, and scopes.
  中文翻译：不透明 token 路径调用签发者经认证的内省端点，并校验返回的 active 状态、受众或资源、过期时间、subject 和 scope。
- Revocation policy defines how quickly a credential must stop working and which cache can delay that fact.
  中文翻译：吊销策略定义一个凭证必须在多短时间内失效，以及哪些缓存可以把这个事实拖慢。
- Failure policy decides what happens when discovery, JWKS, introspection, or revocation infrastructure is unavailable.
  中文翻译：故障策略决定当发现、JWKS、内省或吊销基础设施不可用时该怎么办。
- Evidence records which issuer metadata, key set or introspection response, token claims, policy version, and refusal reason drove the result without storing the token.
  中文翻译：证据记录是哪个签发者元数据、密钥集或内省响应、token 声明、策略版本和拒绝原因决定了结果，但不存储 token 本身。

This distinction keeps the lessons composable. Lesson 16 proves the flow. Lesson 18 proves that a token remains trustworthy, or is refused, after it reaches a real MCP request path.

> 这个分工让两课保持可组合：第 16 课证明流程成立；第 18 课证明一个 token 在到达真实 MCP 请求路径之后，要么仍然可信、要么被拒绝。

## The Concept | 核心概念

### RFC 8414 — OAuth Authorization Server Metadata

A document at `/.well-known/oauth-authorization-server` describes everything a client needs:

> 位于 `/.well-known/oauth-authorization-server` 的文档描述客户端需要的一切：

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "client_id_metadata_document_supported": true,
  "registration_endpoint": "https://auth.example.com/register",
  "authorization_response_iss_parameter_supported": true,
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "scopes_supported": ["mcp:tools.read", "mcp:tools.invoke"],
  "token_endpoint_auth_methods_supported": ["none", "private_key_jwt"]
}
```

A client given an MCP resource URL chains discovery: `oauth-protected-resource` from RFC 9728 (the resource server's document) names the issuer, then `oauth-authorization-server` (this RFC) names every endpoint. The client never hard-codes an authorization URL.

> 拿到 MCP 资源 URL 的客户端做链式发现：先由 RFC 9728 的 `oauth-protected-resource`（资源服务器的文档）指明签发者，再由 `oauth-authorization-server`（本 RFC）列出全部端点。客户端从不硬编码授权 URL。

For a resource identifier with a path, insert the well-known segment before that path. For example, `https://mcp.example.com/team/server` resolves protected-resource metadata at `https://mcp.example.com/.well-known/oauth-protected-resource/team/server`. Appending `/.well-known/...` after the resource path is incorrect.

> 对带路径的资源标识符，要把 well-known 段插在路径之前。例如 `https://mcp.example.com/team/server` 的受保护资源元数据位于 `https://mcp.example.com/.well-known/oauth-protected-resource/team/server`。把 `/.well-known/...` 追加在资源路径之后是错误写法。

The contract you verify before trusting an IdP for MCP:

> 在信任一个 IdP 用于 MCP 之前要验证的契约：

- `code_challenge_methods_supported` includes `S256` (PKCE per RFC 7636). The spec is explicit: if this field is **absent**, the authorization server does not support PKCE and the client **MUST** refuse to proceed.
  中文翻译：`code_challenge_methods_supported` 包含 `S256`（RFC 7636 的 PKCE）。规范写得明确：该字段**缺失**即表示授权服务器不支持 PKCE，客户端**必须**拒绝继续。
- `grant_types_supported` includes `authorization_code` and rejects `password` and `implicit`.
  中文翻译：`grant_types_supported` 包含 `authorization_code`，并拒绝 `password` 和 `implicit`。
- At least one enrollment path is available: `client_id_metadata_document_supported: true` (CIMD, preferred), a pre-registered client, or `registration_endpoint` (deprecated RFC 7591 compatibility).
  中文翻译：至少一条注册路径可用：`client_id_metadata_document_supported: true`（CIMD，首选）、预注册的客户端，或 `registration_endpoint`（已弃用的 RFC 7591 兼容路径）。
- If `authorization_response_iss_parameter_supported` is true, the client requires the returned RFC 9207 `iss` and compares it exactly with the issuer recorded before redirecting.
  中文翻译：若 `authorization_response_iss_parameter_supported` 为 true，客户端必须要求授权响应返回 RFC 9207 `iss`，并在发送任何请求前与重定向前记录的签发者做精确比对。
- `response_types_supported` is exactly `["code"]` for OAuth 2.1.
  中文翻译：对 OAuth 2.1，`response_types_supported` 恰为 `["code"]`。

If `S256` is missing, the MCP server refuses to deploy against this IdP — there is no degraded mode for PKCE. If *neither* enrollment path is advertised and you have no pre-registered `client_id`, you also cannot enroll; the deployment manifest is wrong, not the code.

> 若 `S256` 缺失，MCP 服务器拒绝在此 IdP 上部署——PKCE 没有降级模式。若两条注册路径都未公布且没有预注册的 `client_id`，同样无法注册；错的是部署清单，不是代码。

### RFC 9728 (recap) — Protected Resource Metadata

Lesson 16 covered RFC 9728. The delta in production: this document is the only place a client looks to find the authorization servers trusted by *this* MCP server. A single MCP server may accept tokens from multiple IdPs (one for staff, one for partners). RFC 9728 declares that set; RFC 8414 documents what each IdP supports.

> 第 16 课讲过 RFC 9728。生产中的增量是：这份文档是客户端查找 *此* MCP 服务器信任哪些授权服务器的唯一入口。单个 MCP 服务器可以接受来自多个 IdP 的 token（一个给员工、一个给合作伙伴）。RFC 9728 声明这个集合；RFC 8414 说明每个 IdP 支持什么。

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com", "https://partners.example.com"],
  "scopes_supported": ["mcp:tools.invoke"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://notes.example.com/docs"
}
```

### Client ID Metadata Documents (the recommended default)

> **【中文解读】** CIMD 把注册从"推"反转为"拉"：客户端用自己控制的一个带路径 HTTPS URL 直接充当 `client_id`，该 URL 解析到一份 JSON 元数据文档，授权服务器在 OAuth 流程中按需拉取。信任锚是 DNS——信任 `app.example.com` 就等于信任它托管的 client.json。没有注册往返、没有 `client_id` 命名空间可耗尽、没有需要同步的每服务器状态。两条安全事实：SSRF 防护（授权服务器拉取的是攻击者可提供的 URL）与 localhost 冒充（必须在同意页明示 redirect URI 主机名）。

CIMD inverts registration from *push* to *pull*. Instead of asking the authorization server to mint a `client_id`, the client uses an HTTPS URL it controls **as** its `client_id`. The URL resolves to a JSON metadata document; the authorization server fetches it on demand during the OAuth flow. Trust is rooted in DNS: if the server operator trusts `app.example.com`, it trusts the client served from `https://app.example.com/client.json`. No registration round-trip, no `client_id` namespace to exhaust, no per-server state to keep in sync.

> CIMD 把注册从*推*反转为*拉*。客户端不再请求授权服务器铸造一个 `client_id`，而是用自己控制的一个 HTTPS URL 直接**充当** `client_id`。该 URL 解析到一份 JSON 元数据文档，授权服务器在 OAuth 流程中按需拉取它。信任以 DNS 为根：如果服务器运营方信任 `app.example.com`，它就信任从 `https://app.example.com/client.json` 提供服务的客户端。没有注册往返、没有可耗尽的 `client_id` 命名空间、也没有需要保持同步的每服务器状态。

The metadata document the client hosts:

> 客户端托管的元数据文档：

```json
{
  "client_id": "https://app.example.com/oauth/client.json",
  "client_name": "Example MCP Client",
  "client_uri": "https://app.example.com",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:7333/callback", "http://localhost:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```

The `client_id` value in the document **MUST** equal the URL it is served from (the authorization server verifies this; mismatches are rejected). The authorization server advertises support with `client_id_metadata_document_supported: true` in its RFC 8414 metadata.

> 文档中的 `client_id` 值**必须**等于其托管 URL（授权服务器会验证这一点，不匹配即拒绝）。授权服务器在 RFC 8414 元数据中用 `client_id_metadata_document_supported: true` 公布支持。

For the current CIMD contract, `client_id`, `client_name`, and a non-empty `redirect_uris` array are required. The client identifier is an absolute HTTPS URL with a path. `application_type` may be included, but it is not a mandatory CIMD field. Do not copy the DCR requirement for `application_type` into the preferred CIMD path.

> 就当前 CIMD 契约而言，`client_id`、`client_name` 和非空的 `redirect_uris` 数组是必填项。客户端标识符必须是一个带路径的绝对 HTTPS URL。`application_type` 可以带上，但它不是 CIMD 的必填字段。不要把 DCR 对 `application_type` 的要求照搬进首选的 CIMD 路径。

Two security facts the spec is blunt about:

> 规范直言不讳的两个安全事实：

- **SSRF.** The authorization server fetches an attacker-supplied URL. It must defend against server-side request forgery (no fetches to internal/admin endpoints).
  中文翻译：**SSRF。** 授权服务器会拉取攻击者可提供的 URL，必须防御服务器端请求伪造（不得拉取内部/管理端点）。
- **localhost impersonation.** CIMD alone cannot stop a local attacker from claiming a legitimate client's metadata URL and binding any `localhost` redirect. The authorization server **MUST** clearly display the redirect URI hostname during consent and **SHOULD** warn on `localhost`-only redirects.
  中文翻译：**localhost 冒充。** 仅靠 CIMD 挡不住本地攻击者认领合法客户端的元数据 URL 并绑定任意 `localhost` redirect。授权服务器**必须**在同意页清楚展示 redirect URI 主机名，并**应当**对仅 `localhost` 的 redirect 发出警告。

Because CIMD needs no server-side state, there is no registrar to stand up the way DCR requires. The client side is read-only: serve your metadata document from a static HTTPS endpoint and let the authorization server pull it.

> 因为 CIMD 不需要服务器端状态，也就没有 DCR 那样需要架设的注册器。客户端一侧是只读的：把元数据文档放在一个静态 HTTPS 端点上，让授权服务器来拉。

If the authorization server operator has already provisioned a client identifier, use that issuer-scoped registration before trying automatic enrollment. Otherwise prefer CIMD. Use deprecated DCR only when the issuer cannot use either pre-registration or CIMD.

> 如果授权服务器运营方已经分配了客户端标识符，应先使用这个按签发者划定的注册，再去尝试自动注册。否则优先 CIMD。只有当签发者既不能预注册也不能用 CIMD 时，才使用已弃用的 DCR。

### RFC 7591: deprecated compatibility enrollment

> **【中文解读】** RFC 7591 动态客户端注册在 2026-07-28 版被正式弃用，仅为无法消费 CIMD 且预注册不现实的授权服务器保留。关键变化：`application_type` 不是装饰——回环桌面客户端声明 `native`，服务器托管客户端声明 `web` 并使用 HTTPS redirect URI。三个生产陷阱照旧：按源 IP 限流、`software_statement` 校验、`registration_access_token` 哈希存储。

DCR is deprecated in the 2026-07-28 revision. Keep it only for authorization servers that cannot consume CIMD and where pre-registration is impractical. A compatibility client posts:

> DCR 在 2026-07-28 修订版中已弃用。只对既无法消费 CIMD、预注册又不现实的授权服务器保留它。兼容客户端 POST：

```json
POST /register
Content-Type: application/json

{
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "mcp:tools.invoke",
  "client_name": "Cursor",
  "software_id": "com.cursor.cursor",
  "software_version": "0.42.0"
}
```

The server responds with `client_id` and a `registration_access_token` for later updates:

> 服务器以 `client_id` 和一个供后续更新使用的 `registration_access_token` 响应：

```json
{
  "client_id": "c_3e7f1a",
  "client_id_issued_at": 1769472000,
  "redirect_uris": ["http://127.0.0.1:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "registration_access_token": "regt_b2...",
  "registration_client_uri": "https://auth.example.com/register/c_3e7f1a"
}
```

`application_type` is not decorative. A loopback desktop client declares `native`; a server-hosted client declares `web` and uses HTTPS redirect URIs. `token_endpoint_auth_method: none` is the right default for a public native client. It gets a `client_id` only, with PKCE providing the proof-of-possession.

> `application_type` 不是摆设。回环桌面客户端声明 `native`；服务器托管客户端声明 `web` 并使用 HTTPS redirect URI。`token_endpoint_auth_method: none` 是公共原生客户端的正确默认值——它只拿到 `client_id`，由 PKCE 提供持有证明。

Three production pitfalls:

> 三个生产陷阱：

- The registration endpoint must rate-limit by source IP. Without that, a hostile actor scripts millions of fake registrations and exhausts the `client_id` namespace. Run a rate-limit check before the registrar handles the request.
  中文翻译：注册端点必须按源 IP 限流。否则恶意行为者可以脚本化发起数百万假注册，耗尽 `client_id` 命名空间。在注册器处理请求之前先跑限流检查。
- `software_statement` (a signed JWT vouching for the client) is required by some enterprise IdPs. The lesson's mock skips it; production wires a verification step that rejects unsigned registrations from anything other than localhost redirect URIs.
  中文翻译：某些企业 IdP 要求 `software_statement`（为客户端背书的签名 JWT）。本课的 mock 跳过了它；生产环境要连线一个验证步骤，拒绝来自非 localhost redirect URI 的未签名注册。
- The `registration_access_token` must be stored as a hash, not plaintext. Theft of this token means the attacker can rewrite the client's redirect URIs.
  中文翻译：`registration_access_token` 必须以哈希存储，而非明文。该 token 被盗意味着攻击者可以改写客户端的 redirect URI。

### RFC 8707 (recap) — Resource Indicators

Lesson 16 established the shape. The production rule: every token request includes `resource=<canonical-mcp-url>`, and the MCP server verifies `token.aud` matches its own resource URL on every call. The canonical URI is the *most specific* identifier for the server: it uses lowercase scheme and host, no fragment, and conventionally no trailing slash. The path component is **not** stripped by rule — the spec keeps it when it is needed to identify an individual MCP server. `https://mcp.example.com`, `https://mcp.example.com/mcp`, `https://mcp.example.com:8443`, and `https://mcp.example.com/server/mcp` are all valid canonical URIs. Pick one per server and pin `aud` to exactly that. (This lesson's mock uses bare-host audiences like `https://notes.example.com` for brevity; a deployment that co-hosts several MCP servers under one origin distinguishes them by path.)

> 第 16 课确立了形态。生产规则：每个 token 请求都带 `resource=<canonical-mcp-url>`，MCP 服务器在每次调用上验证 `token.aud` 与自身资源 URL 匹配。规范 URI 是服务器的*最具体*标识符：scheme 与 host 小写、无 fragment、按惯例无尾部斜杠。路径组件**不**按规则剥除——当需要标识单个 MCP 服务器时规范会保留它。`https://mcp.example.com`、`https://mcp.example.com/mcp`、`https://mcp.example.com:8443`、`https://mcp.example.com/server/mcp` 都是合法的规范 URI。每个服务器选定一个，并把 `aud` 精确固定到它。（本课 mock 为简洁起见用裸主机受众如 `https://notes.example.com`；在同一 origin 下托管多个 MCP 服务器的部署靠路径区分它们。）

### RFC 7636 (recap) — PKCE

PKCE is mandatory in OAuth 2.1. The lesson's authorization-code flow always carries `code_challenge` and `code_verifier`. The server rejects any token request without a verifier or with a verifier that does not hash to the stored challenge.

> PKCE 在 OAuth 2.1 中是强制的。本课的授权码流程始终携带 `code_challenge` 和 `code_verifier`。服务器拒绝任何缺少 verifier、或 verifier 哈希后与存储的 challenge 不符的 token 请求。

### MCP 2026-07-28 authorization profile

> **【中文解读】** 2026-07-28 版保持 OAuth 资源服务器边界，但把 MCP 传输变成无状态：没有可以缓存身份决定的协议会话，授权层因此对每个请求独立验证。要点：PRM 元数据位置可经 401 头或 well-known URI 获取；token 只能走 `Authorization: Bearer` 且每个请求都要验证 `aud`/`iss`/`exp`/scope；401/403 的 challenge 用 `resource_metadata` 指针（没有 `resource` 参数）；发现同时接受 RFC 8414 与 OIDC Discovery；mix-up 防御在客户端（RFC 9207）；凭证按签发者隔离；CIMD 优先、DCR 已弃用。

The current MCP revision keeps the OAuth resource-server boundary while making MCP transport stateless. There is no protocol session on which to cache an identity decision. The authorization layer therefore validates each request independently:

> 当前 MCP 修订版保持 OAuth 资源服务器边界，同时把 MCP 传输变为无状态。没有可以用来缓存身份决定的协议会话，授权层因此对每个请求独立验证：

- Implement RFC 9728 protected-resource metadata, and provide its location either through the `WWW-Authenticate: Bearer resource_metadata="..."` header on a 401 **or** the well-known URI `/.well-known/oauth-protected-resource` (SEP-985 made the header optional with a well-known fallback). The metadata `authorization_servers` field **MUST** name at least one server.
  中文翻译：实现 RFC 9728 受保护资源元数据，其位置要么通过 401 上的 `WWW-Authenticate: Bearer resource_metadata="..."` 头给出，**要么**用 well-known URI `/.well-known/oauth-protected-resource`（SEP-985 把该头变为可选并配 well-known 回退）。元数据的 `authorization_servers` 字段**必须**至少列出一个服务器。
- Accept tokens only via `Authorization: Bearer ...` on **every** request — never in a query string, never validated only at session start.
  中文翻译：只在**每个**请求上经 `Authorization: Bearer ...` 接受 token——绝不放进查询串，绝不能只在会话开始时验证一次。
- Validate `aud`, `iss`, `exp`, and required scopes per request. The server **MUST** validate that the token was issued specifically for it (audience); a missing or mismatched `aud` is rejected, never treated as wildcard.
  中文翻译：每个请求都验证 `aud`、`iss`、`exp` 和必需的 scope。服务器**必须**验证 token 是专门为它签发的（受众）；`aud` 缺失或不匹配一律拒绝，绝不当作通配符。
- On 401/403, return `WWW-Authenticate: Bearer` carrying `error=...`, the `resource_metadata="<PRM-URL>"` parameter (the URL of the metadata document, *not* the bare resource), and `scope="..."` on `insufficient_scope` (403). Note: the parameter is `resource_metadata`, a discovery pointer — there is no `resource` parameter in the challenge.
  中文翻译：在 401/403 上返回 `WWW-Authenticate: Bearer`，携带 `error=...`、`resource_metadata="<PRM-URL>"` 参数（元数据文档的 URL，*而非*裸资源），403 的 `insufficient_scope` 再加 `scope="..."`。注意：该参数叫 `resource_metadata`，是一个发现指针——challenge 里没有 `resource` 参数。
- Authorization-server discovery accepts **either** RFC 8414 OAuth metadata **or** OpenID Connect Discovery 1.0; clients must try both well-known suffixes in priority order.
  中文翻译：授权服务器发现**既**接受 RFC 8414 OAuth 元数据，**也**接受 OpenID Connect Discovery 1.0；客户端必须按优先级依次尝试两种 well-known 后缀。
- The client (not the server) defends against **mix-up attacks**: it records the expected `issuer` before redirecting and validates the `iss` value returned in the actual authorization response (RFC 9207) before redeeming the code. PKCE alone does not stop mix-up, because the client hands its `code_verifier` to whatever token endpoint it was steered to.
  中文翻译：**mix-up 攻击**由客户端（而非服务器）防御：重定向前记录预期的 `issuer`，在兑换 code 之前校验实际授权响应中返回的 `iss` 值（RFC 9207）。仅靠 PKCE 挡不住 mix-up，因为客户端会把 `code_verifier` 交给它被引去的那家 token 端点。
- A client credential belongs to one authorization-server issuer. If discovery resolves to a different issuer, the client re-enrolls instead of presenting the old `client_id`, registration token, or access token.
  中文翻译：一个客户端凭证只属于一个授权服务器签发者。若发现解析到了另一个签发者，客户端应重新注册，而不是拿旧的 `client_id`、注册 token 或 access token 去硬闯。
- CIMD is the preferred enrollment mechanism. DCR is deprecated; a compatibility DCR request still declares the correct `application_type`.
  中文翻译：CIMD 是首选注册机制。DCR 已弃用；兼容用的 DCR 请求仍要声明正确的 `application_type`。

The OAuth 2.1 draft is the substrate; RFC 8414/7591/8707/9728/9207 + RFC 7636 + CIMD are the surface; the MCP spec is the profile.

> OAuth 2.1 草案是底座；RFC 8414/7591/8707/9728/9207 + RFC 7636 + CIMD 是表层；MCP 规范是配置档。

### Deployment capability checklist

Vendor feature tables become stale quickly. Inspect the metadata returned by the authorization server you will actually deploy instead. The gate is mechanical:

> 厂商功能表很快过期。改为检查你实际要部署的那个授权服务器返回的元数据。门控是机械的：

| Check | Required decision |
|---|---|
| Discovered issuer | Exact HTTPS issuer expected by policy |
| PKCE | `S256` advertised; otherwise stop |
| Enrollment | CIMD preferred, pre-registration accepted, DCR only as deprecated compatibility |
| Authorization response | Validate RFC 9207 `iss` when present or advertised |
| Resource binding | Token request carries `resource`; resource server requires the matching `aud` |
| Credential storage | Key client IDs and registration credentials by issuer; key access tokens by issuer plus resource |
| DCR compatibility | Declare `native` or `web`; reject redirect URIs that do not fit the declared application type |

Do not infer support from a product name or pricing tier. Capture the discovered document in deployment evidence and fail closed when a mandatory field is absent.

> 不要从产品名或定价档推断支持能力。把发现的文档捕获进部署证据，必填字段缺失时失败关闭。

### JWKS refresh pattern (rotate at the AS, refresh at the resource server)

> **【中文解读】** 区分两个动词：**轮换（rotate）**是授权服务器的事——铸造新密钥、发布进 JWKS、稍后退役旧密钥；**刷新（refresh）**是资源服务器唯一能做的事——重新 GET 已发布的 JWKS 进缓存。生产故障模式是缓存过期：定时刷新任务在旧密钥过期前覆盖缓存；`kid` 未命中时做**一次**同步刷新作回退再复查。回退必须是幂等的"重新拉取"，绝不能是"轮换并铸造"——后者既造不出缺失的 `kid`，还会被随机 `kid` 的 token 喷射打成自伤式 DoS。

Keep two verbs separate, because conflating them is a real production bug:

> 把两个动词分开，混用它们是真实的生产 bug：

- **Rotate** is what the *authorization server* does: mint a new signing key, publish it in the JWKS, retire the old one later. The resource server has no part in this and cannot do it — it does not hold the IdP's private keys.
  中文翻译：**轮换**是*授权服务器*做的事：铸造新签名密钥、发布进 JWKS、稍后退役旧密钥。资源服务器与此无关也做不到——它不持有 IdP 的私钥。
- **Refresh** is what the *resource server* does: re-`GET` the published JWKS into its cache. That is the only JWKS action a resource server ever performs.
  中文翻译：**刷新**是*资源服务器*做的事：重新 `GET` 已发布的 JWKS 进缓存。这是资源服务器唯一会执行的 JWKS 操作。

The production failure mode is a stale cache. Solve it with a scheduled refresh job plus a key-value cache. The resource server runs a job (cron, timer, whatever your runtime offers) that, on a fixed interval, fetches `<issuer>/.well-known/jwks.json` and overwrites `cache[issuer] = {keys, fetched_at}`. The validator reads from that cache. A token whose `kid` is missing from the cache triggers **one** synchronous refresh as a fall-back, then re-checks. This handles two cases at once: the scheduled refresh, and key-overlap windows where a token signed by a brand-new key arrives before the next scheduled refresh.

> 生产故障模式是缓存过期。用一个定时刷新任务加一个键值缓存解决。资源服务器运行一个作业（cron、timer，运行时提供什么都行），按固定间隔拉取 `<issuer>/.well-known/jwks.json` 并覆盖 `cache[issuer] = {keys, fetched_at}`。验证器从该缓存读取。某个 token 的 `kid` 不在缓存中时，触发**一次**同步刷新作为回退，然后复查。这同时覆盖两种情况：计划内刷新，以及"由全新密钥签名的 token 在下一次计划刷新之前到达"的密钥重叠窗口。

The fall-back **must be a re-fetch, never a rotate**. If you wire the cache-miss path to a rotate-and-mint, two things break: (1) minting a fresh key produces a `kid` that *still* does not match the token, so the lookup fails anyway; and (2) an attacker who sprays tokens with random `kid` values forces an unbounded series of key creations — a self-inflicted DoS. A re-fetch is idempotent, so a bogus `kid` costs at most one wasted fetch.

> 回退**必须是重新拉取，绝不许是轮换**。若把缓存未命中路径接到"轮换并铸造"，会坏两件事：(1) 铸造新密钥得到的 `kid` *仍然*匹配不上 token，查找照样失败；(2) 攻击者用随机 `kid` 喷射 token，逼出无上限的密钥创建——自伤式 DoS。重新拉取是幂等的，伪造的 `kid` 最多浪费一次拉取。

The cache shape:

> 缓存形态：

```json
{
  "https://auth.example.com": {
    "keys": [
      {"kid": "k_2026_03", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"},
      {"kid": "k_2026_04", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"}
    ],
    "fetched_at": 1772668800
  }
}
```

Two keys at once is the steady state. Authorization servers rotate by introducing the next key (`k_2026_04`) before retiring the previous (`k_2026_03`), so tokens issued under the old key remain valid until they expire. The cache holds the union; the validator picks by `kid`.

> 同时持有两个密钥是稳态。授权服务器轮换时先引入下一个密钥（`k_2026_04`），再退役前一个（`k_2026_03`），因此旧密钥签发的 token 在过期前仍然有效。缓存持有两者的并集；验证器按 `kid` 选用。

> 💡 **【类比】** JWKS 刷新像消防站的暗号本。授权局（消防局）定期换暗号（签名密钥），各消防站（MCP 服务器）必须人手一册最新暗号本，否则夜间演习（凌晨 3 点的用户请求）全部认证失败。正确姿势：各站订阅定时换发（cron 刷新）；新旧暗号并行一段时间（重叠窗口）；有人拿新暗号敲门而本子还没更新时，现场打电话核实一次（缓存未命中同步回退）——而不是自己编一个新暗号（rotate-as-fallback，会把随机敲门变成无休止的印刷新暗号）。

### The validation routine

The MCP server runs validation before dispatching any tool. The shape `code/main.py` uses:

> MCP 服务器在分发任何工具之前先跑验证。`code/main.py` 的形态：

```python
result = server.validate(bearer_token, required_scope="mcp:tools.invoke")
if not result["valid"]:
    return {"status": result["status"], "WWW-Authenticate": result["www_authenticate"]}
```

`validate` decodes the JWT, resolves the signing key from the JWKS cache (refreshing once on a miss), verifies the signature, then checks `iss` against the allow-list, `aud` against this server's canonical resource, `exp`, and the required scope — returning a `WWW-Authenticate` challenge on the first failure. Keeping it a single routine on the resource server means every entry point (every tool call, every transport) goes through the same checks; there is no path that reaches a tool without validating first.

> `validate` 解码 JWT，从 JWKS 缓存解析签名密钥（未命中时刷新一次），验证签名，然后把 `iss` 对照允许列表、把 `aud` 对照本服务器的规范资源、再查 `exp` 和必需 scope——第一次失败即返回 `WWW-Authenticate` challenge。把它保持为资源服务器上的单一例程，意味着每个入口（每次工具调用、每种传输）都经过同一套检查；不存在未经验证就触达工具的路径。

### Opaque tokens use introspection, not guesswork

> **【中文解读】** 不是所有 access token 都是 JWT。签发者若发布的是不透明 token，资源服务器无法解码出可信声明，必须把 token 经认证的后端通道送到签发者的 RFC 7662 内省端点，要求 `active: true`、预期的签发者上下文、精确的 MCP 受众或资源、未过期的时间和该工具所需的 scope。缓存按"签发者 + token 单向摘要 + MCP 资源"做键，绝不用明文 token 做日志或缓存标签。验证模式不能由 token 内容决定——攻击者可控的内容不能选择验证路径。

Not every access token is a JWT. If the issuer documents an opaque token, the resource server cannot decode it into trustworthy claims. It sends the token to the issuer's RFC 7662 introspection endpoint over an authenticated backchannel and requires `active: true`, the expected issuer context, the exact MCP audience or resource, unexpired time claims, and the scopes required by the concrete tool.

> 不是每个 access token 都是 JWT。如果签发者发布的是不透明 token，资源服务器无法把它解码成可信声明。它把 token 经认证的后端通道发到签发者的 RFC 7662 内省端点，并要求 `active: true`、预期的签发者上下文、精确的 MCP 受众或资源、未过期的时间声明，以及该具体工具所需的 scope。

Cache introspection by issuer, a one-way token digest, and MCP resource. Never use the clear token as a log or cache label. Bound a positive cache entry by the earliest of token expiry, issuer cache guidance, and the deployment's revocation freshness objective. Keep negative caching short enough that a newly issued token does not remain falsely inactive. A result for one resource cannot authorize another resource even when the opaque token string is identical.

> 内省缓存按签发者、token 单向摘要和 MCP 资源做键。绝不用明文 token 当日志或缓存标签。正向缓存条目的有效期取"token 过期时间、签发者缓存指引、部署的吊销新鲜度目标"三者中最早者。负向缓存要足够短，以免新签发的 token 被误判为不活跃。针对某一资源的内省结果不能授权另一个资源——即使不透明 token 字符串完全相同。

Do not choose validation mode from attacker-controlled token contents. Pin JWT versus introspection behavior to validated issuer metadata and deployment configuration. On the JWT path, pin accepted algorithms and trusted `jwks_uri`; never follow a key URL or algorithm selected only by the token header.

> 不要根据攻击者可控的 token 内容选择验证模式。把"JWT 还是内省"钉死在已验证的签发者元数据与部署配置上。JWT 路径上，锁死接受的算法与可信的 `jwks_uri`；绝不跟随仅由 token 头指定的密钥 URL 或算法。

### Revocation is a freshness contract

RFC 7009 lets a client ask an authorization server to revoke a token. That request does not erase copies already cached by every resource server. Define the maximum acceptable revocation delay and make every cache honor it.

> RFC 7009 允许客户端请求授权服务器吊销 token。但该请求不会抹掉已被每个资源服务器缓存的副本。定义最大可接受的吊销延迟，并让每个缓存都遵守它。

Opaque-token deployments can achieve tighter revocation by introspecting on each high-risk call or using a short positive cache. Self-contained JWT deployments usually combine short access-token lifetimes with refresh-token revocation, key retirement for issuer-wide incidents, and an optional subject, session, or token-id denylist for emergency local refusal. A signed JWT remains cryptographically valid until expiry unless the resource server has current external revocation evidence.

> 不透明 token 部署可以对每次高风险调用都做内省或使用短正向缓存，实现更紧的吊销。自包含 JWT 部署通常组合使用：短 access token 有效期 + refresh token 吊销、面向全签发者事件的密钥退役，以及应急本地拒绝用的 subject/session/token-id denylist。签名的 JWT 在过期前密码学上始终有效——除非资源服务器握有当前的外部吊销证据。

Logout, account disablement, consent withdrawal, and incident response are different triggers but must converge on one measurable statement: after at most the declared revocation window, every replica refuses the credential. Test that statement through the load balancer, not only against one warm process.

> 登出、账号停用、撤回同意和事件响应是不同的触发器，但必须收敛为一句可度量的陈述：至多在声明的吊销窗口之后，每个副本都拒绝该凭证。这句话要通过负载均衡器验证，而不是只对着一个热进程。

### Dependency failure needs a declared decision

> **【中文解读】** 可用性策略不能在异常处理器里即兴发挥。表格给出六类依赖故障的安全生产行为（JWKS 刷新失败但缓存仍有界有效→在声明的 stale-on-error 窗口内继续并输出降级健康证据；未知 `kid` 且唯一回退失败→拒绝；内省不可用→失败关闭；元数据意外变更→停止新注册；吊销端点不可用→如实报告未完成；时钟源或声明类型无效→拒绝而非放宽偏差）。依赖故障与无效凭证必须分开分类：前者是带健康与重试策略的运维错误，后者是授权拒绝——两者都到不了工具处理器，也都不许把 token 内容泄漏进审计证据。

Never improvise availability policy inside an exception handler.

> 绝不在异常处理器里即兴制定可用性策略。

| Failure | Safe production behavior |
|---|---|
| Scheduled JWKS refresh fails, known `kid` remains in a still-valid bounded cache | Continue only within the declared stale-on-error window and emit degraded health evidence |
| Token has an unknown `kid` and the one allowed refresh fails | Reject; never accept an unverifiable signature |
| Introspection is unavailable | Fail closed for protected calls; do not convert network failure into `active: true` |
| Protected-resource or issuer metadata changes unexpectedly | Stop new enrollment and token acquisition; keep only explicitly pinned, unexpired configuration under a bounded incident policy |
| Revocation endpoint is unavailable | Report logout or revocation as incomplete, retain the credential locally as unusable when possible, and do not claim global revocation succeeded |
| Clock source or claim type is invalid | Reject rather than widening skew until the token passes |

Classify failures separately from invalid credentials. A dependency outage is an operational error with health and retry policy. A bad signature, issuer, audience, expiry, or scope is an authorization refusal. Neither reaches the tool handler, and neither should leak token contents into audit evidence.

> 把依赖故障与无效凭证分开分类。依赖中断是带健康与重试策略的运维错误；坏的签名、签发者、受众、过期时间或 scope 是授权拒绝。两者都到不了工具处理器，也都不应把 token 内容泄漏进审计证据。

### Audience-replay walkthrough (access-token privilege restriction)

> **【中文解读】** 受众重放演练：Server A（notes.example.com）与 Server B（tasks.example.com）注册到同一授权服务器；A 被攻陷后攻击者拿用户的 notes token 去敲 B。B 的验证器在第三步检查 `aud == "https://tasks.example.com"` 失败，返回 401 并带 `resource_metadata` 指针。受众声明是协议层对这类攻击的唯一防御——规范称之为 **access-token privilege restriction**：MCP 服务器 `MUST` 拒绝任何受众里没有点它名字的 token。注意术语：*confused deputy* 留给了另一个问题——MCP 代理用静态 client ID 转发 token 且未取得每客户端同意。

Server A (`notes.example.com`) and Server B (`tasks.example.com`) both register against the same authorization server. Server A is compromised. The attacker takes a user's notes token and replays it against Server B.

> 服务器 A（`notes.example.com`）与服务器 B（`tasks.example.com`）都注册到同一个授权服务器。服务器 A 被攻陷。攻击者拿到用户的 notes token 并向服务器 B 重放。

Server B's validator:

> 服务器 B 的验证器：

1. Decode JWT, fetch JWKS by `kid`, verify signature.
  中文翻译：解码 JWT，按 `kid` 取 JWKS，验证签名。
2. Check `iss` against its protected-resource metadata's `authorization_servers`. (Pass — same IdP.)
  中文翻译：把 `iss` 对照其受保护资源元数据的 `authorization_servers`。（通过——同一 IdP。）
3. Check `aud == "https://tasks.example.com"`. (Fail — token's `aud` is `https://notes.example.com`.)
  中文翻译：检查 `aud == "https://tasks.example.com"`。（失败——token 的 `aud` 是 `https://notes.example.com`。）
4. Return 401 with `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`.
  中文翻译：返回 401，带 `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`。

The audience claim is the only defense against this attack at the protocol layer. Skipping it for performance is the most common production mistake; the validator must run on every request, not just at session start. The spec calls this **access-token privilege restriction**: an MCP server `MUST` reject any token that does not name it in the audience.

> 受众声明是协议层防御此攻击的唯一手段。为性能跳过它是最常见的生产错误；验证器必须在每个请求上运行，而不是只在会话开始时。规范称之为 **access-token privilege restriction**（access token 特权限制）：MCP 服务器 `MUST` 拒绝任何受众中未点名它的 token。

> **Naming note.** The spec reserves the term *confused deputy* for a related-but-distinct problem: an MCP server acting as an OAuth **proxy** to a third-party API, using a static client ID, that forwards a token without obtaining per-client user consent. Audience binding fixes the replay above; the confused-deputy fix is per-client consent **plus** never passing the inbound token through to upstream APIs (the MCP server `MUST` get its own separate upstream token).

### Mix-up attacks (a client-side defense the server cannot provide)

A client talks to many authorization servers over its life. A malicious AS can try to make the client redeem an honest AS's authorization code at the attacker's token endpoint. Audience binding does not help here — the attack happens before any token exists. The defense lives in the client (RFC 9207):

> 客户端一生会与许多授权服务器打交道。恶意 AS 可以设法让客户端把诚实 AS 的授权码拿到攻击者的 token 端点去兑换。受众绑定在这里帮不上忙——攻击发生在任何 token 存在之前。防御在客户端一侧（RFC 9207）：

1. Before redirecting, the client records the expected `issuer` from the validated AS metadata.
  中文翻译：重定向之前，客户端从已验证的 AS 元数据记录预期的 `issuer`。
2. On the authorization response, the client compares the returned `iss` parameter against that recorded issuer (simple string comparison, no normalization) before sending the code anywhere.
  中文翻译：收到授权响应时，客户端在任何地方发送 code 之前，把返回的 `iss` 参数与记录的签发者比对（简单字符串比较，不做规范化）。
3. Mismatch (or `iss` absent when the AS advertised `authorization_response_iss_parameter_supported`) → reject, and do not even display the `error` fields.
  中文翻译：不匹配（或 AS 已公布 `authorization_response_iss_parameter_supported` 却缺少 `iss`）→ 拒绝，连 `error` 字段都不要展示。

PKCE alone does not stop mix-up, because the client hands its `code_verifier` to whatever token endpoint it was steered to. This is why the spec records the issuer per-request alongside the PKCE verifier and `state`.

> 仅 PKCE 挡不住 mix-up，因为客户端会把 `code_verifier` 交给它被引去的那家 token 端点。这正是规范把签发者与 PKCE verifier、`state` 一起按请求记录的原因。

### Failure modes

- **Stale JWKS.** The validator rejects valid tokens after the AS rotates a key. The fix is the cron-refresh + cache-miss-refetch pattern above. Never cache JWKS without a refresh job.
  中文翻译：**过期 JWKS。** AS 轮换密钥后验证器拒绝有效 token。修复是上面的定时刷新 + 未命中重拉模式。绝不在没有刷新任务的情况下缓存 JWKS。
- **Rotate-as-fall-back.** Wiring the cache-miss path to a rotate-and-mint instead of a re-fetch is a real bug: it never produces the missing `kid`, and it turns attacker-controlled `kid` values into a key-creation DoS. The fall-back must be the idempotent `refresh-jwks`.
  中文翻译：**把轮换当回退。** 把缓存未命中路径接到"轮换并铸造"而不是重新拉取是真实的 bug：它永远造不出缺失的 `kid`，还会把攻击者可控的 `kid` 值变成密钥创建 DoS。回退必须是幂等的 `refresh-jwks`。
- **Missing `aud` claim.** Some IdPs default to omitting `aud` unless `resource` is present in the token request. The validator must reject tokens with missing `aud`, not treat absence as wildcard.
  中文翻译：**缺失 `aud` 声明。** 一些 IdP 默认省略 `aud`，除非 token 请求中带了 `resource`。验证器必须拒绝缺失 `aud` 的 token，而不是把缺失当通配符。
- **Mix-up via missing `iss` check.** A client that does not validate the RFC 9207 `iss` authorization-response parameter against the issuer it recorded before redirecting can be steered into redeeming an honest AS's code at an attacker's token endpoint. This is a client-side failure; the resource server cannot compensate for it.
  中文翻译：**缺 `iss` 检查导致 mix-up。** 不把 RFC 9207 `iss` 授权响应参数与重定向前记录的签发者比对的客户端，可能被引到攻击者的 token 端点去兑换诚实 AS 的 code。这是客户端侧的失败；资源服务器无法补救。
- **Scope upgrade race.** Two concurrent step-up flows for the same user can both succeed and produce two access tokens with different scopes. The validator must use the token presented on the request, not look up "the user's current scope" — that creates a TOCTOU window.
  中文翻译：**scope 升级竞态。** 同一用户的两个并发 step-up 流程都可能成功，产生两个 scope 不同的 access token。验证器必须使用请求上呈现的那个 token，而不是去查"用户当前 scope"——那会打开 TOCTOU 窗口。
- **Registration token theft.** A leaked `registration_access_token` lets the attacker rewrite redirect URIs. Hash these at rest; require the client to present the cleartext on every update; rotate on suspicion.
  中文翻译：**注册 token 被盗。** 泄漏的 `registration_access_token` 让攻击者可以改写 redirect URI。静态哈希存储；要求客户端每次更新出示明文；一有怀疑就轮换。
- **`iss` not pinned.** A validator that accepts any `iss` lets an attacker stand up their own authorization server, register a client for the target audience, and issue tokens. The protected-resource metadata's `authorization_servers` list is the allow-list; enforce it.
  中文翻译：**`iss` 未锁定。** 接受任意 `iss` 的验证器会让攻击者自建授权服务器、为目标受众注册客户端并签发 token。受保护资源元数据的 `authorization_servers` 列表就是允许列表；强制执行它。
- **Credential or token cache collision.** A client that keys registrations only by resource can present one authorization server's identity to another. A client that keys access tokens only by issuer can replay a token at the wrong audience. Key registrations by validated issuer, key access tokens by `(issuer, resource)`, and re-enroll whenever the issuer changes.
  中文翻译：**凭证或 token 缓存碰撞。** 只按资源给注册做键的客户端，会把一个授权服务器的身份递给另一个；只按签发者给 access token 做键的客户端，会把 token 重放到错误的受众。注册按已验证的签发者做键，access token 按 `(issuer, resource)` 做键，签发者一变就重新注册。

```figure
t3-jwks-rotate
```

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 用标准库 Python 和三个角色（`AuthorizationServer`、`ResourceServer`、`Client`）走完整生产流程：发布 RFC 8414 元数据 → 检查注册选项与 S256 → 优先 issuer 级预注册/CIMD、DCR 单独可测 → 记录签发者并校验授权响应 `iss` → PKCE + RFC 8707 资源指示器 → Bearer 调用工具 → JWKS 缓存验证 → 密钥轮换后无需重启继续验证 → 受众重放得到 401。

`code/main.py` walks the full production flow with stdlib Python and three roles: `AuthorizationServer`, `ResourceServer`, and `Client`. The flow:

> `code/main.py` 用标准库 Python 和三个角色——`AuthorizationServer`、`ResourceServer`、`Client`——走完整生产流程。流程：

From the repository root, run:

> 在仓库根目录运行：

```bash
cd phases/13-tools-and-protocols/18-mcp-auth-production
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

The first command prints the issuer-bound enrollment and token-validation
transcript. The second reports eighteen passing checks. Neither command opens a
network listener or writes credentials.

> 第一条命令打印签发者绑定的注册与 token 验证记录；第二条报告 18 项通过的检查。两条命令都不打开网络监听、不写入凭证。

1. Authorization server publishes RFC 8414 metadata at `/.well-known/oauth-authorization-server`.
  中文翻译：授权服务器在 `/.well-known/oauth-authorization-server` 发布 RFC 8414 元数据。
2. MCP client calls the metadata endpoint and checks its enrollment options (`client_id_metadata_document_supported` for CIMD, `registration_endpoint` for DCR) and `S256` PKCE support.
  中文翻译：MCP 客户端调用元数据端点，检查注册选项（CIMD 看 `client_id_metadata_document_supported`，DCR 看 `registration_endpoint`）与 `S256` PKCE 支持。
3. The client checks for an issuer-scoped pre-registration, otherwise enrolls with its HTTPS Client ID Metadata Document. Deprecated DCR remains a separately testable compatibility method.
  中文翻译：客户端先查按签发者划定的预注册，否则用它的 HTTPS Client ID Metadata Document 注册。已弃用的 DCR 仍保留为可单独测试的兼容方法。
4. The client records the validated issuer, creates an S256 challenge, receives a one-time authorization code plus `iss`, validates that returned issuer, and redeems the code with the original verifier and RFC 8707 `resource` indicator.
  中文翻译：客户端记录已验证的签发者，创建 S256 challenge，收到一次性授权码和 `iss`，校验返回的签发者，再用原始 verifier 和 RFC 8707 `resource` 指示器兑换 code。
5. MCP client calls a tool on the MCP server with `Authorization: Bearer ...`.
  中文翻译：MCP 客户端以 `Authorization: Bearer ...` 调用 MCP 服务器上的工具。
6. MCP server runs `validate`, resolving the signing key from the JWKS cache.
  中文翻译：MCP 服务器运行 `validate`，从 JWKS 缓存解析签名密钥。
7. The IdP rotates a key; the scheduled refresh re-pulls the JWKS into the cache.
  中文翻译：IdP 轮换一个密钥；定时刷新把 JWKS 重新拉进缓存。
8. The next call validates against the refreshed keys without restart, and the previous token still validates during the overlap window.
  中文翻译：下一次调用无需重启即针对刷新后的密钥验证，且旧 token 在重叠窗口内仍然有效。
9. An audience-replay attempt against a different MCP resource gets 401 with `audience mismatch` and a `resource_metadata` pointer.
  中文翻译：针对另一个 MCP 资源的受众重放尝试得到 401，带 `audience mismatch` 和 `resource_metadata` 指针。

The JWT here uses HS256 with a shared secret (so the lesson runs on stdlib only). Production uses RS256 or EdDSA with the JWKS pattern above; the validation logic is otherwise identical. Because the IdP and resource server live in one process, `refresh_jwks` reads the authorization server's key list directly; over the wire it is an HTTP `GET` to `jwks_uri`.

> 这里的 JWT 用 HS256 加共享密钥（使本课仅在标准库上运行）。生产使用 RS256 或 EdDSA 加上述 JWKS 模式；验证逻辑其余完全相同。因为 IdP 与资源服务器同在一个进程，`refresh_jwks` 直接读授权服务器的密钥表；走线缆时它就是对 `jwks_uri` 的一次 HTTP `GET`。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-auth.md`. Given an MCP server config and an IdP capability set, the skill emits the auth surface to stand up — the protected-resource metadata, the enrollment path to use (CIMD, pre-registration, or DCR fallback), the JWKS refresh schedule, the scope mapping, and the refusal rules to apply when the IdP does not support the full RFC profile.

> 本课产出 `outputs/skill-mcp-auth.md`。给定 MCP 服务器配置和 IdP 能力集，该 skill 生成需要架设的认证面——受保护资源元数据、该用的注册路径（CIMD、预注册或 DCR 后备）、JWKS 刷新计划、scope 映射，以及 IdP 不满足完整 RFC 配置时的拒绝规则。

## Exercises | 练习题

1. Run `code/main.py`. Trace the flow. Note how the IdP rotates a key in step 6, the scheduled `refresh_jwks` re-pulls the published set, and both the old token (overlap window) and a fresh token validate without restart.
   中文翻译：运行 `code/main.py`，追踪流程。注意第 6 步 IdP 如何轮换密钥、定时 `refresh_jwks` 如何重拉已发布的密钥集，以及旧 token（重叠窗口）与新 token 如何都无需重启即可验证。

2. Add a new IdP to the protected-resource metadata's `authorization_servers` list. Issue a token signed by the new IdP and confirm the validator accepts it. Issue a token signed by an unlisted IdP and confirm the validator rejects with `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`.
   中文翻译：向受保护资源元数据的 `authorization_servers` 列表添加新 IdP。签发一个由新 IdP 签名的 token，确认验证器接受；再签发一个由未列出的 IdP 签名的 token，确认验证器以 `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"` 拒绝。

3. Add a rate-limit check to `register_client` that runs before the registrar accepts a request. Use a token-bucket per source IP held in a small dict keyed by IP.
   中文翻译：给 `register_client` 加一个在注册器接受请求之前运行的限流检查。用按源 IP 做键的小字典实现每 IP 令牌桶。

4. Read RFC 7591 and identify two fields the lesson's `/register` handler does not validate. Add the validation. (Hint: `software_statement` and `redirect_uris` URI scheme.)
   中文翻译：阅读 RFC 7591，找出本课 `/register` 处理器未验证的两个字段并补上验证。（提示：`software_statement` 与 `redirect_uris` 的 URI scheme。）

5. Add a second authorization server. Confirm the client stores a separate issuer-keyed enrollment and refuses to reuse the first issuer's token or `client_id`.
   中文翻译：添加第二个授权服务器。确认客户端存了独立的按签发者做键的注册，并拒绝复用第一个签发者的 token 或 `client_id`。

6. Prove the DoS fix. Send the validator a token with a random `kid` and confirm `refresh_jwks` runs at most once and the authorization server's key count does not grow. Then deliberately re-wire the fall-back to a rotate-and-mint and watch the key count climb per bogus token — restore the re-fetch afterward.
   中文翻译：证明 DoS 修复。给验证器送一个随机 `kid` 的 token，确认 `refresh_jwks` 至多运行一次且授权服务器的密钥数不增长。然后故意把回退改接"轮换并铸造"，看密钥数随每个伪造 token 上升——最后恢复重新拉取。

7. Exercise deprecated DCR with both `native` and `web` clients. Confirm a web client with an HTTP redirect URI and a native client without an exact loopback redirect are rejected.
   中文翻译：用 `native` 和 `web` 两种客户端演练已弃用的 DCR。确认带 HTTP redirect URI 的 web 客户端与没有精确回环 redirect 的 native 客户端都被拒绝。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| ASM | "OAuth metadata document" | RFC 8414 `/.well-known/oauth-authorization-server` JSON |
| CIMD | "Client metadata URL" | Client ID Metadata Document: an HTTPS URL used as the `client_id`; the AS pulls the JSON. Preferred enrollment in MCP 2026-07-28 |
| DCR | "Self-service client registration" | RFC 7591 `POST /register`; deprecated for current MCP and retained only for compatibility |
| JWKS | "Public keys for JWT validation" | JSON Web Key Set, fetched from `jwks_uri`, indexed by `kid` |
| Rotate vs refresh | "Updating the keys" | *Rotate* = AS mints/retires signing keys; *refresh* = resource server re-fetches the published set. Resource servers only ever refresh |
| Resource indicator | "Audience parameter" | RFC 8707 `resource` parameter pinning the token to one server |
| `aud` claim | "Audience" | JWT claim the validator compares against the canonical resource URL |
| Audience replay | "Token replay" | Token issued for Server A presented to Server B; defended by audience validation (spec: access-token privilege restriction) |
| Confused deputy | "Proxy token misuse" | An MCP proxy with a static client ID forwarding a token without per-client consent; distinct from audience replay |
| Mix-up attack | "Wrong token endpoint" | Client steered to redeem an honest AS's code at an attacker's endpoint; defended client-side via RFC 9207 `iss` |
| `iss` allow-list | "Trusted authorization servers" | The set named in protected-resource metadata's `authorization_servers` |
| `resource_metadata` | "Where to find the PRM doc" | `WWW-Authenticate` parameter naming the RFC 9728 metadata URL on a 401/403 |
| Public client | "Native or browser client" | OAuth client with no `client_secret`; PKCE compensates |
| `WWW-Authenticate` | "401/403 response header" | Carries `Bearer error=...` directives that drive client recovery |

## Further Reading | 延伸阅读

- [MCP authorization specification (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) - the current MCP authorization profile
  中文翻译：MCP 授权规范（2026-07-28）——本课实现的当前 MCP 授权配置档
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) - CIMD, issuer validation, DCR deprecation, and issuer-keyed credential changes
  中文翻译：MCP 2026-07-28 变更日志——CIMD、签发者校验、DCR 弃用与按签发者做键的凭证变更
- [OAuth Client ID Metadata Document (draft-ietf-oauth-client-id-metadata-document-00)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00) — CIMD
  中文翻译：CIMD 草案——"URL 即 client_id"的注册机制
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) — discovery contract
  中文翻译：RFC 8414——发现契约
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591) — DCR (fallback path)
  中文翻译：RFC 7591——DCR（后备路径）
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636) — public-client proof-of-possession
  中文翻译：RFC 7636——PKCE，公共客户端持有证明
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — audience pinning
  中文翻译：RFC 8707——资源指示器，受众固定
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) — resource server discovery
  中文翻译：RFC 9728——资源服务器发现
- [RFC 9207 — OAuth 2.0 Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207) — the `iss` parameter that defends against mix-up attacks
  中文翻译：RFC 9207——防御 mix-up 攻击的 `iss` 参数
- [RFC 7662: OAuth 2.0 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
  中文翻译：RFC 7662——不透明 token 的内省端点
- [RFC 7009: OAuth 2.0 Token Revocation](https://datatracker.ietf.org/doc/html/rfc7009)
  中文翻译：RFC 7009——token 吊销，本课的"新鲜度契约"
