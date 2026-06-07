# MCP Auth in Production — DCR, JWKS Rotation, Audience-Pinned Tokens | MCP 生产级认证：DCR、JWKS 轮换与受众绑定 Token

> Lesson 16 stood up the OAuth 2.1 state machine in memory. By 2026, every MCP server you ship to a real org sits behind production auth: dynamic client registration (RFC 7591), authorization-server metadata discovery (RFC 8414), JWKS rotation that does not break a 3 a.m. token validation, and audience-pinned tokens that refuse confused-deputy reuse. This lesson wires all of that through iii primitives — `iii.registerTrigger` for HTTP and cron, `iii.registerFunction` for auth logic, `state::set/get` for cached keys — so the auth surface is observable, restartable, and replayable like every other workload in the engine.

> **【中文解读】** Lesson 16 在内存中搭建了 OAuth 2.1 状态机。生产环境有三个操作缺口：(1) 注册——真实组织运行数百个 MCP 服务器和数千个客户端，不能手工注册每个 OAuth 客户端；(2) 密钥轮换——JWT 验证依赖授权服务器的签名密钥（JWKS），轮换时需缓存刷新；(3) 受众绑定——RFC 8707 资源指示器成为每次请求的硬性声明检查。本课通过 iii 原语将这些全部连接起来。

> **【拓展】** iii 原语（registerTrigger、registerFunction、state::set/get）是本课的核心抽象。每个认证端点和后台作业都是 iii 原语——HTTP 触发器返回函数输出，JWKS 轮换是 cron 触发器写入 state，JWT 验证是通过 iii.trigger 调用的函数。重启引擎后触发器注册表重建、state 存活，认证面无需手工恢复。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, iii primitives mocked for the lesson environment) | **语言:** Python (stdlib, iii primitives mocked for the lesson environment)
**Prerequisites:** Phase 13 · 16 (OAuth 2.1 state machine), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 16 (OAuth 2.1 state machine), Phase 13 · 17 (gateways)
**Time:** ~90 minutes | **时间:** ~90 分钟

## Learning Objectives | 学习目标

- Discover an authorization server through RFC 8414 metadata and verify the contract.
  中文翻译：参见英文条目了解详情。
- Implement RFC 7591 dynamic client registration so MCP clients enroll without admin intervention.
  中文翻译：参见英文条目了解详情。
- Cache and rotate JWKS keys using a cron trigger so signature verification survives key roll-over.
  中文翻译：参见英文条目了解详情。
- Pin tokens to a single MCP resource using RFC 8707 resource indicators and refuse confused-deputy reuse.
  中文翻译：参见英文条目了解详情。
- Wire every endpoint and background job as iii primitives — HTTP triggers, cron triggers, named functions, and `state::*` reads — so a single restart rebuilds the auth surface.
  中文翻译：参见英文条目了解详情。
- Read an IdP capability matrix and refuse to deploy when the IdP cannot satisfy MCP's auth profile.
  中文翻译：参见英文条目了解详情。

## The Problem | 问题引入

> **【中文解读】** 三个生产缺口：(1) 注册缺口——RFC 7591 动态客户端注册让客户端 `POST /register` 即可获得 client_id；(2) 密钥轮换缺口——JWKS 轮换时需要缓存刷新 + 回退获取，否则验证失败；(3) 受众绑定缺口——MCP 服务器在每个请求上比较 `token.aud` 与自身资源 URL，拒绝不匹配的请求（HTTP 401）。

The Lesson 16 simulator runs OAuth 2.1 in memory. Production has three operational gaps that a memory-only simulator does not see.

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

The first gap is enrollment. A real org runs hundreds of MCP servers and thousands of MCP clients. Operators do not hand-register every Cursor user as an OAuth client. RFC 7591 dynamic client registration lets a client `POST /register` against the authorization server and receive a `client_id` (and optionally `client_secret`) on the spot. The server publishes `registration_endpoint` in its RFC 8414 metadata; the client discovers it without out-of-band configuration.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

The second gap is key rotation. JWT validation depends on the authorization server's signing keys, published as a JSON Web Key Set (JWKS). The authorization server rotates these on a schedule (often hourly, sometimes faster under incident response). An MCP server that fetches JWKS once at boot validates fine until the rotation window — then every request fails until restart. Production wires JWKS as a cached value with a refresh job that overwrites the cache before the previous keys expire, plus a fall-back fetch on cache miss for the case where a token signed by a key newer than the cache arrives.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

The third gap is audience binding. Lesson 16 introduced RFC 8707 resource indicators.

> **【拓展：JWKS 密钥轮换在生产中的关键性】** JWT 验证依赖授权服务器的签名密钥（JWKS）。授权服务器按计划轮换这些密钥（通常每小时，事件响应时更快）。启动时只获取一次 JWKS 的 MCP 服务器在轮换窗口到来前验证正常——之后所有请求失败直到重启。生产环境需要：缓存 JWKS 并设置在过期前覆盖的刷新任务，加上缓存未命中时的回退获取。 In production, that indicator becomes a hard claim check on every request. The MCP server compares `token.aud` against its own canonical resource URL and rejects mismatches with HTTP 401. This is the only defense against an upstream MCP server (or a malicious client holding a token meant for one server) replaying that token against another server in the same trust mesh.

This lesson treats every one of those gaps as an iii primitive. The metadata document is an HTTP trigger that returns a function's output. JWKS rotation is a cron trigger that calls `auth::rotate-jwks`, which writes to `state::set("auth/jwks/<issuer>", ...)`. JWT validation is a function others call via `iii.trigger("auth::validate-jwt", token)`. The MCP server itself is just another HTTP trigger that calls into validation before dispatching. Restart the engine: the trigger registry rebuilds; state survives; the auth surface is operational without manual reconciliation.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## The Concept | 核心概念

> **【中文解读】** 本节详解六个核心概念：RFC 8414 授权服务器元数据、RFC 9728 受保护资源元数据（回顾）、RFC 7591 动态客户端注册、RFC 8707 资源指示器（回顾）、RFC 7636 PKCE（回顾）、MCP 规范 2025-11-25 认证配置。还包括 IdP 能力矩阵、JWKS 轮换模式、iii 原语连接、混淆代理演练和故障模式。

### RFC 8414 — OAuth Authorization Server Metadata

> **【中文解读】** RFC 8414 授权服务器元数据：在 `/.well-known/oauth-authorization-server` 发布的文档描述客户端所需的一切（issuer、各端点 URL、支持的授权类型等）。验证 IdP 合同：必须支持 S256 PKCE、authorization_code、registration_endpoint。如果任何一项缺失，MCP 服务器拒绝部署。

A document at `/.well-known/oauth-authorization-server` describes everything a client needs:

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "registration_endpoint": "https://auth.example.com/register",
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "scopes_supported": ["mcp:tools.read", "mcp:tools.invoke"],
  "token_endpoint_auth_methods_supported": ["none", "private_key_jwt"]
}
```

A client given an MCP resource URL chains discovery: `oauth-protected-resource` from RFC 9728 (the resource server's document) names the issuer, then `oauth-authorization-server` (this RFC) names every endpoint. The client never hard-codes an authorization URL.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

The contract you verify before trusting an IdP for MCP:

> 参见英文原文获取完整的技术说明。

- `code_challenge_methods_supported` includes `S256` (PKCE per RFC 7636).
  中文翻译：参见英文条目了解详情。
- `grant_types_supported` includes `authorization_code` and rejects `password` and `implicit`.
  中文翻译：参见英文条目了解详情。
- `registration_endpoint` is present (RFC 7591 support).
  中文翻译：参见英文条目了解详情。
- `response_types_supported` is exactly `["code"]` for OAuth 2.1.
  中文翻译：参见英文条目了解详情。

If any of those is missing, the MCP server refuses to deploy against this IdP. The deployment manifest is wrong, not the code.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### RFC 9728 (recap) — Protected Resource Metadata

Lesson 16 covered RFC 9728. The delta in production: this document is the only place a client looks to find the authorization servers trusted by *this* MCP server. A single MCP server may accept tokens from multiple IdPs (one for staff, one for partners). RFC 9728 declares that set; RFC 8414 documents what each IdP supports.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com", "https://partners.example.com"],
  "scopes_supported": ["mcp:tools.invoke"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://notes.example.com/docs"
}
```

### RFC 7591 — Dynamic Client Registration

> **【中文解读】** RFC 7591 动态客户端注册：无需管理员干预，MCP 客户端 `POST /register` 即可获得 client_id。公共客户端（token_endpoint_auth_method: none）适合运行在用户设备上的 MCP 客户端，PKCE 提供所需的持有证明。三个生产陷阱：注册端点必须按 IP 限流、某些企业 IdP 要求 software_statement、registration_access_token 必须哈希存储。

Without DCR, every MCP client (Cursor, Claude Desktop, a custom agent) needs an out-of-band exchange with the IdP admin. With DCR, the client posts:

> MCP 客户端的核心实现：发现和调用服务器工具，管理会话和命名空间。

```json
POST /register
Content-Type: application/json

{
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

> 注册表相关内容：工具和服务器的注册与发现。

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

`token_endpoint_auth_method: none` is the right default for MCP clients that run on the user's device. They get a `client_id` only — no `client_secret` to exfiltrate. PKCE provides the proof-of-possession that public clients need.

> MCP 客户端的核心实现：发现和调用服务器工具，管理会话和命名空间。

Three production pitfalls:

- The registration endpoint must rate-limit by source IP. Without that, a hostile actor scripts millions of fake registrations and exhausts the `client_id` namespace. iii makes this trivial: the registration HTTP trigger calls a `auth::rate-limit` function before dispatching to the registrar.
  中文翻译：参见英文条目了解详情。
- `software_statement` (a signed JWT vouching for the client) is required by some enterprise IdPs. The lesson's mock skips it; production wires a verification step that rejects unsigned registrations from anything other than localhost redirect URIs.
  中文翻译：参见英文条目了解详情。
- The `registration_access_token` must be stored as a hash, not plaintext. Theft of this token means the attacker can rewrite the client's redirect URIs.
  中文翻译：参见英文条目了解详情。

### RFC 8707 (recap) — Resource Indicators

Lesson 16 established the shape. The production rule: every token request includes `resource=<canonical-mcp-url>`, and the MCP server verifies `token.aud` matches its own resource URL on every call. If the MCP server is reachable at `https://notes.example.com/mcp`, the canonical URL is `https://notes.example.com` — the path component is excluded so a single server hosts multiple paths under one audience.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### RFC 7636 (recap) — PKCE

PKCE is mandatory in OAuth 2.1. The lesson's authorization-code flow always carries `code_challenge` and `code_verifier`. The server rejects any token request without a verifier or with a verifier that does not hash to the stored challenge.

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

### MCP Spec 2025-11-25 Auth Profile

The MCP spec (2025-11-25) is precise about what an MCP server's authorization layer must do:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

- Publish `/.well-known/oauth-protected-resource` (RFC 9728).
  中文翻译：参见英文条目了解详情。
- Accept tokens only via `Authorization: Bearer ...`.
  中文翻译：参见英文条目了解详情。
- Validate `aud`, `iss`, `exp`, and required scopes per request.
  中文翻译：参见英文条目了解详情。
- Respond with `WWW-Authenticate` carrying `Bearer error=...` for every 401 and 403, including `scope=` and `resource=` parameters where applicable.
  中文翻译：参见英文条目了解详情。
- Reject tokens whose `aud` does not match the canonical resource.
  中文翻译：参见英文条目了解详情。
- Reject tokens whose `iss` is not in the protected-resource metadata's `authorization_servers` list.
  中文翻译：参见英文条目了解详情。

The OAuth 2.1 draft is the substrate; RFC 8414/7591/8707/9728 + RFC 7636 are the surface; the MCP spec is the profile.

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

### IdP capability matrix

Not every IdP supports the full MCP profile. The matrix below documents factual capability statements as of the 2025-11-25 spec. It is a *deployment gate*, not a recommendation.

> 生产部署相关内容：从开发到生产环境的关键考量。

| IdP category | RFC 8414 metadata | RFC 7591 DCR | RFC 8707 resource | RFC 7636 S256 PKCE | Notes |
|---|---|---|---|---|---|
| Self-hosted (Keycloak) | yes | yes | yes (since 24.x) | yes | Reference IdP for the MCP profile in this lesson; supports every RFC end-to-end. |
| Enterprise SSO (Microsoft Entra ID) | yes | yes (premium tiers) | yes | yes | DCR availability differs by tenant tier; verify in target tenant before deploying. |
| Enterprise SSO (Okta) | yes | yes (Okta CIC / Auth0) | yes | yes | DCR available on Auth0 (now Okta CIC); classic Okta orgs require admin pre-registration. |
| Social login IdPs (generic) | varies | rarely | rarely | yes | Most social IdPs treat clients as static partners; do not rely on DCR. Use as identity source only, layer your own MCP-aware authorization server on top. |
| Custom / homegrown | depends | depends | depends | depends | If you ship your own, ship the full profile. Skipping any one of the four RFCs above breaks the MCP auth contract. |

Refusal rule for the deployment manifest: if the chosen IdP does not return `registration_endpoint` and does not list `S256` in `code_challenge_methods_supported`, the MCP server refuses to start. There is no degraded mode.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### JWKS rotation pattern with iii

> **【中文解读】** JWKS 轮换模式：生产故障模式是 JWKS 缓存过期。解决方案是 cron 触发器 + state 缓存。每6小时 cron 调用 `auth::rotate-jwks`，获取新密钥并写入 state。验证器从 state 读取。如果 token 的 kid 不在缓存中，同步触发一次轮换作为回退。稳态下缓存同时持有两个密钥（新旧重叠），确保旧密钥签发的 token 在过期前仍然有效。

The production failure mode is a stale JWKS cache. Solve it with a cron trigger and a `state::*` cache:

> 重连与故障恢复相关内容：传输层失败后的自动恢复。

```python
iii.registerTrigger(
    "cron",
    {"schedule": "0 */6 * * *", "name": "auth::jwks-refresh"},
    "auth::rotate-jwks",
)
```

Every six hours, the cron trigger calls `auth::rotate-jwks`, which fetches `<issuer>/.well-known/jwks.json` and writes to `state::set("auth/jwks/<issuer>", {keys, fetched_at})`. The validator reads from `state::get`. A token whose `kid` is missing from the cache triggers a synchronous `auth::rotate-jwks` call as a fall-back. This handles two cases at once: scheduled rotation (cron) and key-overlap windows (synchronous fall-back).

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

The state shape:

```json
{
  "auth/jwks/https://auth.example.com": {
    "keys": [
      {"kid": "k_2026_03", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"},
      {"kid": "k_2026_04", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"}
    ],
    "fetched_at": 1772668800
  }
}
```

Two keys at once is the steady state. Authorization servers rotate by introducing the next key (`k_2026_04`) before retiring the previous (`k_2026_03`), so tokens issued under the old key remain valid until they expire. The cache holds the union; the validator picks by `kid`.

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

### iii primitive wiring (the part this lesson is actually about)

> **【中文解读】** iii 原语连接：五个原语组成认证面——(1) RFC 8414 元数据文档 HTTP 触发器；(2) RFC 7591 DCR HTTP 触发器；(3) JWT 验证可调用函数；(4) SEP-835 逐步授权函数；(5) cron 驱动的 JWKS 轮换。MCP 服务器本身通过 `iii.trigger("auth::validate-jwt", ...)` 调用验证，间接性是 iii 的核心设计——可以轻松替换验证器、添加 span 发射器或缓存正面验证。

Five primitives compose the auth surface:

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

```python
# 1. RFC 8414 metadata document
iii.registerTrigger(
    "http",
    {"path": "/.well-known/oauth-authorization-server", "method": "GET"},
    "auth::serve-asm",
)

# 2. RFC 7591 dynamic client registration
iii.registerTrigger(
    "http",
    {"path": "/register", "method": "POST"},
    "auth::register-client",
)

# 3. JWT validation as a callable function (the resource server triggers it)
iii.registerFunction("auth::validate-jwt", validate_jwt_handler)

# 4. Step-up issuance for incremental scope (SEP-835 from L16)
iii.registerFunction("auth::issue-step-up", issue_step_up_handler)

# 5. Cron-driven JWKS rotation
iii.registerTrigger(
    "cron",
    {"schedule": "0 */6 * * *"},
    "auth::rotate-jwks",
)
iii.registerFunction("auth::rotate-jwks", rotate_jwks_handler)
```

The MCP server itself never calls validation directly. It does:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

```python
result = iii.trigger("auth::validate-jwt", {"token": bearer_token, "resource": self.resource})
if not result["valid"]:
    return {"status": 401, "WWW-Authenticate": result["www_authenticate"]}
```

This indirection is the iii bet. Tomorrow you swap the validator for a fanout that consults two IdPs in parallel, or you add a span emitter, or you cache positive validations. The MCP server does not change.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### Confused-deputy walkthrough with audience binding

> **【中文解读】** 混淆代理演练：Server A（notes.example.com）和 Server B（tasks.example.com）共享同一授权服务器。Server A 被攻陷，攻击者拿到用户 notes token 重放到 Server B。Server B 的验证器解码 JWT 后检查 `aud == "https://tasks.example.com"` 失败（token 的 aud 是 notes.example.com），返回 401。受众声明是协议层防御此攻击的唯一手段。

Server A (`notes.example.com`) and Server B (`tasks.example.com`) both register against the same authorization server. Server A is compromised. The attacker takes a user's notes token and replays it against Server B.

> 认证与授权相关内容：OAuth 2.1 协议在 MCP 中的应用。

Server B's validator:

1. Decode JWT, fetch JWKS by `kid`, verify signature.
  中文翻译：参见英文条目了解详情。
2. Check `iss` against its protected-resource metadata's `authorization_servers`. (Pass — same IdP.)
  中文翻译：参见英文条目了解详情。
3. Check `aud == "https://tasks.example.com"`. (Fail — token's `aud` is `https://notes.example.com`.)
  中文翻译：参见英文条目了解详情。
4. Return 401 with `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch"`.
  中文翻译：参见英文条目了解详情。

The audience claim is the only defense against this attack at the protocol layer. Skipping it for performance is the most common production mistake; the validator must run on every request, not just at session start.

> 安全相关内容：工具投毒防护、认证机制和攻击防御策略。

### Failure modes

> **【中文解读】** 故障模式：(1) 过期 JWKS——轮换后验证器拒绝有效 token，需 cron+回退模式解决；(2) 缺失 aud 声明——验证器必须拒绝缺失 aud 的 token，而非视为通配符；(3) 范围升级竞态——并发逐步授权产生不同范围的 token，验证器必须使用请求中呈现的 token；(4) 注册令牌盗窃——攻击者重写 redirect URI；(5) iss 未锁定——攻击者自建授权服务器。

- **Stale JWKS.** The validator rejects valid tokens after key rotation. The fix is the cron+fall-back pattern above. Never cache JWKS without a refresh job.
  中文翻译：**Stale JWKS.** — 参见英文原文了解详情。
- **Missing `aud` claim.** Some IdPs default to omitting `aud` unless `resource` is present in the token request. The validator must reject tokens with missing `aud`, not treat absence as wildcard.
  中文翻译：**Missing `aud` claim.** — 参见英文原文了解详情。
- **Scope upgrade race.** Two concurrent step-up flows for the same user can both succeed and produce two access tokens with different scopes. The validator must use the token presented on the request, not look up "the user's current scope" — that creates a TOCTOU window.
  中文翻译：**Scope upgrade race.** — 参见英文原文了解详情。
- **Registration token theft.** A leaked `registration_access_token` lets the attacker rewrite redirect URIs. Hash these at rest; require the client to present the cleartext on every update; rotate on suspicion.
  中文翻译：**Registration token theft.** — 参见英文原文了解详情。
- **`iss` not pinned.** A validator that accepts any `iss` lets an attacker stand up their own authorization server, register a client for the target audience, and issue tokens. The protected-resource metadata's `authorization_servers` list is the allow-list; enforce it.
  中文翻译：**`iss` not pinned.** — 参见英文原文了解详情。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 用标准库 Python 和小型 iii_mock 注册表演示完整的生产流程：授权服务器发布 RFC 8414 元数据 -> 客户端发现注册端点 -> DCR 注册获得 client_id -> PKCE 授权码流程 -> Bearer token 调用工具 -> JWT 验证读取 JWKS 缓存 -> cron 触发 JWKS 轮换 -> 新密钥验证通过 -> 混淆代理尝试返回 401。

`code/main.py` walks the full production flow with stdlib Python and a small `iii_mock` registry that mimics `iii.registerFunction`, `iii.registerTrigger`, `iii.trigger`, and `state::set/get`. The flow:

> 代码实现说明：参见 code/main.py 中的具体实现。

1. Authorization server publishes RFC 8414 metadata at `/.well-known/oauth-authorization-server`.
  中文翻译：参见英文条目了解详情。
2. MCP client calls the metadata endpoint, discovers the registration endpoint.
  中文翻译：参见英文条目了解详情。
3. MCP client posts to `/register` (RFC 7591) and receives a `client_id`.
  中文翻译：参见英文条目了解详情。
4. MCP client runs PKCE-protected authorization code flow (RFC 7636) with `resource` indicator (RFC 8707).
  中文翻译：参见英文条目了解详情。
5. MCP client calls a tool on the MCP server with `Authorization: Bearer ...`.
  中文翻译：参见英文条目了解详情。
6. MCP server triggers `auth::validate-jwt`, which reads JWKS from `state::get`.
  中文翻译：参见英文条目了解详情。
7. The cron trigger fires `auth::rotate-jwks`, replacing the JWKS in state.
  中文翻译：参见英文条目了解详情。
8. The next call validates against the new keys without restart.
  中文翻译：参见英文条目了解详情。
9. A confused-deputy attempt against a different MCP resource gets 401 with audience mismatch.
  中文翻译：参见英文条目了解详情。

The mock JWT here uses HS256 with a shared secret (so the lesson runs on stdlib only). Production uses RS256 or EdDSA with the JWKS pattern above; the validation logic is otherwise identical.

> 生产部署相关内容：从开发到生产环境的关键考量。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-mcp-auth-iii.md`——给定 MCP 服务器配置和 IdP 能力集，生成 iii 原语注册方案、JWKS 轮换计划、范围映射和 IdP 不满足 RFC 配置时的拒绝规则。

This lesson produces `outputs/skill-mcp-auth-iii.md`. Given an MCP server config and an IdP capability set, the skill emits the iii primitives to register, the JWKS rotation schedule, the scope mapping, and the refusal rules to apply when the IdP does not support the full RFC profile.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Exercises | 练习题

1. Run `code/main.py`. Trace the 9-step flow. Note where `state::get` returns stale data immediately before `auth::rotate-jwks` overwrites it, and how the next request now validates against the new key.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Add a new IdP to the protected-resource metadata's `authorization_servers` list. Issue a token signed by the new IdP and confirm the validator accepts it. Issue a token signed by an unlisted IdP and confirm the validator rejects with `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

3. Implement `auth::rate-limit` as an iii function and call it from inside the registration HTTP trigger before the registrar runs. Use a token-bucket per source IP held in `state::set("auth/ratelimit/<ip>", ...)`.
   中文翻译：实现相关练习。参见英文原文了解完整要求。

4. Read RFC 7591 and identify two fields the lesson's `/register` handler does not validate. Add the validation. (Hint: `software_statement` and `redirect_uris` URI scheme.)
   中文翻译：阅读相关练习。参见英文原文了解完整要求。

5. Read the MCP spec 2025-11-25 authorization section. Find the one normative requirement on `WWW-Authenticate` headers that the lesson's validator does not currently emit. Add it.
   中文翻译：阅读相关练习。参见英文原文了解完整要求。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| ASM | "OAuth metadata document" | RFC 8414 `/.well-known/oauth-authorization-server` JSON | 授权服务器元数据文档 |
| DCR | "Self-service client registration" | RFC 7591 `POST /register` flow | 动态客户端注册 |
| JWKS | "Public keys for JWT validation" | JSON Web Key Set, fetched from `jwks_uri`, indexed by `kid` | JWT 验证公钥集 |
| Resource indicator | "Audience parameter" | RFC 8707 `resource` parameter pinning the token to one server | 资源指示器：token 受众绑定参数 |
| `aud` claim | "Audience" | JWT claim the validator compares against the canonical resource URL | 受众声明：验证器比对目标资源 |
| Confused deputy | "Token replay" | Attack where a token issued for Server A is presented to Server B | 混淆代理：token 重放攻击 |
| `iss` allow-list | "Trusted authorization servers" | The set named in protected-resource metadata's `authorization_servers` | 签发者白名单 |
| Key rotation | "Rolling JWKS" | Periodic replacement of signing keys with overlap windows | 密钥轮换：带重叠窗口的 JWKS 更替 |
| Public client | "Native or browser client" | OAuth client with no `client_secret`; PKCE compensates | 公共客户端：无 client_secret，PKCE 补偿 |
| `WWW-Authenticate` | "401/403 response header" | Carries `Bearer error=...` directives that drive client recovery | 401/403 响应头，携带错误恢复指令 |

## Further Reading | 延伸阅读

- [MCP — Authorization spec (2025-11-25)](https://modelcontextprotocol.io/specification/draft/basic/authorization) — the MCP auth profile this lesson implements
  中文翻译：the MCP auth profile this lesson implements
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) — discovery contract
  中文翻译：discovery contract
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591) — DCR
  中文翻译：DCR
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636) — public-client proof-of-possession
  中文翻译：public-client proof-of-possession
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — audience pinning
  中文翻译：audience pinning
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) — resource server discovery
  中文翻译：resource server discovery
- [OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) — the consolidated OAuth substrate
  中文翻译：the consolidated OAuth substrate
