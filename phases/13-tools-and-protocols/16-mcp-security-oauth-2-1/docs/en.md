# MCP Authorization: CIMD, Issuer Binding, PKCE, and Step-Up | MCP 授权：CIMD、签发方绑定、PKCE 与逐步授权

> A remote MCP request is stateless, but its authorization is not anonymous. Bind every credential to the issuer that created it and every token to the resource that receives it.

> **【中文解读】** 远程 MCP 请求是无状态的，但授权不是匿名的。2026-07-28 授权配置的两大支柱：把每份凭证绑定到签发它的 issuer（签发方），把每个 token 绑定到接收它的 resource（资源）。本课在进程内完整模拟受保护资源元数据发现、注册优先级（CIMD 优先、DCR 弃用兼容）、PKCE、`iss` 校验、资源绑定 token 与逐步授权。

> **【拓展】** OAuth 2.1 合并了多年安全最佳实践：强制 PKCE、禁止隐式流程。MCP 在其上叠加自己的配置：注册优先级（预注册 > CIMD > 弃用的 DCR）、RFC 9207 的 `iss` 参数精确校验、禁止跨 issuer 复用凭证。CIMD（Client ID Metadata Document，客户端 ID 元数据文档）是新一代注册机制——客户端自托管一个 HTTPS 元数据文档，文档 URL 本身就是 client_id，免去每次首接触都要动态注册的旧负担。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 09（transports）——只有远程 Streamable HTTP 才需要 OAuth，本地 stdio 不用；(2) Phase 13 · 15（security）——先理解威胁面与主体（principal）概念；(3) OAuth 2.0/2.1、PKCE、Bearer token 基础；(4) RFC 9728 / RFC 8707 / RFC 9207 三份 RFC——本课逐一实现其关键校验。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 15 (security) | **前置知识:** Phase 13 · 09（传输层）、Phase 13 · 15（安全）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Discover authorization servers through protected-resource metadata.
  中文翻译：通过受保护资源元数据发现授权服务器。
- Prefer Client ID Metadata Documents over deprecated Dynamic Client Registration.
  中文翻译：优先使用客户端 ID 元数据文档（CIMD），而非已弃用的动态客户端注册（DCR）。
- Declare the correct `application_type` when a DCR compatibility path is unavoidable.
  中文翻译：当 DCR 兼容路径不可避免时，声明正确的 `application_type`。
- Validate authorization response `iss` and isolate credentials by issuer.
  中文翻译：校验授权响应的 `iss`，并按签发方隔离凭证。
- Use PKCE, resource indicators, audience validation, and incremental scopes.
  中文翻译：使用 PKCE、资源指示器、受众校验和增量权限范围。
- Send authorized MCP 2026-07-28 requests without protocol sessions.
  中文翻译：在无协议会话的情况下发送已授权的 MCP 2026-07-28 请求。

> **【中文解读】** 学习目标主线：元数据发现 → 注册优先级（CIMD 优先）→ DCR 兼容路径的正确姿势 → `iss` 校验与 issuer 隔离 → PKCE/资源指示器/受众/增量 scope 四件套 → 无状态授权请求。六个目标串起来就是一条完整的远程 MCP 授权流水线。

## The Problem | 问题引入

> **【中文解读】** 认证回答"谁出示了凭证"，授权还要回答五个问题：哪个授权服务器签发？token 给哪个 MCP 资源？哪个客户端和重定向 URI 完成流程？用户批准了哪些操作？这个请求是否仍在批准范围内？2026-07-28 授权配置强化注册与 issuer 处理来回答这些问题，且不恢复握手或 `Mcp-Session-Id`。

A remote MCP server may read private records, write external systems, or trigger costly work. Authentication tells it who presented a credential. Authorization must also answer:

> 远程 MCP 服务器可能读取隐私记录、写入外部系统或触发昂贵操作。认证告诉它谁出示了凭证。授权还必须回答：

- Which authorization server issued the credential?
  中文翻译：哪个授权服务器签发了这份凭证？
- Which MCP resource is the token for?
  中文翻译：这个 token 是给哪个 MCP 资源的？
- Which client and redirect URI completed the flow?
  中文翻译：哪个客户端和重定向 URI 完成了流程？
- Which operations did the user approve?
  中文翻译：用户批准了哪些操作？
- Does this exact request still fit that approval?
  中文翻译：这个请求是否仍在该批准范围内？

The 2026-07-28 authorization profile hardens client enrollment and issuer handling. It prefers Client ID Metadata Documents, deprecates Dynamic Client Registration, requires the right `application_type` on DCR, validates RFC 9207 issuer responses, and forbids credential reuse across issuers.

> 2026-07-28 授权配置强化了客户端注册与 issuer 处理：优先 CIMD、弃用 DCR、要求 DCR 声明正确的 `application_type`、校验 RFC 9207 issuer 响应、禁止跨 issuer 复用凭证。

These rules complement the stateless core. They do not restore a core handshake or `Mcp-Session-Id`.

> 这些规则与无状态核心互补，不恢复核心握手或 `Mcp-Session-Id`。

> 💡 **【类比】** token 像会员卡，资源指示器（RFC 8707）相当于在卡上印"仅限本店使用"（aud 受众锁定）；issuer 绑定则是"每家店的会员卡分开办"——健身房的卡拿到超市刷不开，超市也不会把你的会员信息共享给健身房。CIMD 像"自带的电子名片"：你的名片 URL 就是身份，到任何一家新店出示名片即可入会，不用每家店重新填表登记（DCR）；但消费记录仍按店（issuer）分开保存，换店时旧积分（旧凭证）不带过去。

## The Concept | 核心概念

> **【中文解读】** 本节主线：三角色 → 授权只管 HTTP → RFC 9728 元数据发现 → 授权服务器元数据校验 → 注册优先级（预注册/CIMD/DCR）→ 按 issuer 隔离存储凭证 → PKCE 授权码流程 → `iss` 精确校验 → MCP 服务器端受众校验 → 最小 scope 与逐步授权 → 无状态授权请求的错误信封 → 禁止 token 透传 → refresh token。

### Know the three roles

- **MCP client:** sends requests on behalf of a resource owner.
  中文翻译：**MCP 客户端：** 代表资源所有者发送请求。
- **MCP resource server:** accepts the access token and serves the MCP endpoint.
  中文翻译：**MCP 资源服务器：** 接受 access token 并提供 MCP 端点。
- **Authorization server:** authenticates the resource owner, collects consent, and issues tokens.
  中文翻译：**授权服务器：** 认证资源所有者、收集同意并签发 token。

The resource server and authorization server can be operated together, but keep their identifiers and validation responsibilities separate.

> 资源服务器和授权服务器可以一起运营，但它们的标识符和校验职责要保持分离。

### Authorization applies to HTTP

The MCP authorization specification applies to HTTP-based transports. A local stdio server runs under the process and operating-system trust boundary. Do not add a fake browser OAuth flow to stdio merely for symmetry.

> MCP 授权规范只适用于 HTTP 系传输。本地 stdio 服务器运行在进程与操作系统的信任边界内，不要为了"对称"给 stdio 加一个假浏览器 OAuth 流程。

For remote Streamable HTTP, send the bearer token in the `Authorization` header on every request. Never place it in the URL.

> 对远程 Streamable HTTP，每个请求都把 bearer token 放在 `Authorization` 头里发送，绝不放进 URL。

### Start with protected-resource metadata

> **【中文解读】** RFC 9728 受保护资源元数据是整个流程的起点：客户端从 MCP 资源 URL 出发，拉取 `.well-known/oauth-protected-resource/mcp`（注意保留资源路径后缀），从中选择授权服务器，再拉取它的 OAuth/OIDC 元数据。不要按主机名猜授权服务器，也不要跟随未校验错误体里发现的 issuer。

The resource server publishes RFC 9728 metadata:

```json
{
  "resource": "https://notes.example.com/mcp",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:delete", "notes:read", "notes:write"]
}
```

The client starts from the MCP resource URL, fetches this document, selects an advertised authorization server, and then fetches that server's OAuth or OpenID Connect metadata.

> 客户端从 MCP 资源 URL 出发，获取这份文档，选择一个声明的授权服务器，再获取该服务器的 OAuth 或 OpenID Connect 元数据。

Preserve the resource path when constructing the RFC 9728 well-known URL. For the resource `https://notes.example.com/mcp`, this lesson uses `https://notes.example.com/.well-known/oauth-protected-resource/mcp`. Dropping the `/mcp` suffix can select metadata for a different protected resource on the same origin.

> 构造 RFC 9728 well-known URL 时要保留资源路径。资源 `https://notes.example.com/mcp` 对应 `https://notes.example.com/.well-known/oauth-protected-resource/mcp`。丢掉 `/mcp` 后缀可能选中同源上另一个受保护资源的元数据。

Do not guess the authorization server from a hostname. Do not follow an issuer discovered from an unvalidated error body. Keep a policy for which issuers the client is willing to trust.

> 不要从主机名猜授权服务器；不要跟随来自未校验错误体的 issuer；保留一份"客户端愿意信任哪些 issuer"的策略。

### Verify authorization server metadata

The metadata should expose endpoints and supported controls:

> 元数据应暴露端点与受支持的控制项：

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "code_challenge_methods_supported": ["S256"],
  "authorization_response_iss_parameter_supported": true,
  "client_id_metadata_document_supported": true
}
```

Require S256 for PKCE. Record the exact issuer string. That exact value becomes the key for registration and token storage.

> PKCE 要求 S256。记录精确的 issuer 字符串——这个精确值将成为注册与 token 存储的键。

### Follow the registration priority

> 注册优先级是 2026-07-28 的关键变化：已有明确关系用预注册信息；否则在授权服务器声明支持时优先 CIMD；DCR 只作弃用的兼容回退；都不行才提示输入客户端信息。顺序不可颠倒，更不能在校验失败后"静默降级"到 DCR。

Use pre-registered client information when the client already has an explicit relationship with the selected issuer. Otherwise prefer Client ID Metadata Documents when the authorization server advertises support. Use DCR only as the deprecated compatibility fallback, then prompt for client information if none of those mechanisms is available.

> 客户端与所选 issuer 已有明确关系时用预注册信息；否则在授权服务器声明支持时优先 CIMD；DCR 只作弃用的兼容回退；这些机制都不可用时才提示输入客户端信息。

### Prefer Client ID Metadata Documents

> **【中文解读】** CIMD：给授权服务器一个 HTTPS URL，它既是客户端标识又是元数据所在。授权服务器拉取并校验文档：`client_id` 必须是带路径的 HTTPS URL，且文档内的值与该 URL 完全相等；必填字段是 `client_id`、`client_name`、`redirect_uris`。CIMD 免去首次接触时铸造动态标识，但不免除重定向 URI 校验、issuer 策略和用户同意。拉取文档本身是 SSRF 敏感操作，要当心。

A Client ID Metadata Document gives the authorization server an HTTPS URL that is both the client identifier and the location of its metadata:

> 客户端 ID 元数据文档给授权服务器一个 HTTPS URL，它既是客户端标识又是其元数据的位置：

```json
{
  "client_id": "https://client.example.com/oauth/metadata.json",
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

The authorization server fetches and validates the document. The `client_id` must be an HTTPS URL with a path, and the value inside the document must equal that URL exactly. The required document fields are `client_id`, `client_name`, and `redirect_uris`. `application_type` appears in this example but is not a CIMD requirement. Its new mandatory use is specifically the DCR path.

> 授权服务器拉取并校验该文档。`client_id` 必须是带路径的 HTTPS URL，且文档内的值与该 URL 完全相等。文档必填字段为 `client_id`、`client_name`、`redirect_uris`。`application_type` 出现在示例中但不是 CIMD 的必填项——它的新强制用途专门在 DCR 路径上。

Treat fetching the document as an SSRF-sensitive operation. Resolve and validate the destination, reject loopback, private, link-local, and otherwise disallowed addresses, re-check after redirects and DNS changes, limit redirects, bytes, and time, require JSON, and cache only according to validated HTTP cache controls. Treat `client_name` and other display fields as untrusted text.

> 把拉取文档当作 SSRF 敏感操作：解析并校验目的地，拒绝回环、私网、链路本地等禁用地址，重定向与 DNS 变化后复检，限制重定向次数、字节与时间，强制 JSON，只按已校验的 HTTP 缓存控制来缓存。`client_name` 等展示字段按不可信文本处理。

> ⚠️ **【易错点】** 场景：把拉取 CIMD 文档当成普通 GET，不校验目标地址 / 后果：SSRF——攻击者把 `client_id` 指向内网地址（如云元数据服务 169.254.169.254、内网管理面板），授权服务器替攻击者发起请求并把结果写入注册记录 / 修复：(1) 解析后校验 IP，拒绝回环/私网/链路本地段；(2) 限制重定向次数、响应字节与超时，重定向和 DNS 变化后重新校验；(3) 强制要求 JSON 内容类型，按已验证的 Cache-Control 缓存；(4) 展示字段（`client_name` 等）一律按不可信文本转义。

CIMD removes the need to mint a fresh dynamic identifier for every first contact. It does not remove redirect URI validation, issuer policy, or user consent.

> CIMD 免去了每次首次接触都铸造新动态标识的需要，但不免除重定向 URI 校验、issuer 策略或用户同意。

### DCR is a compatibility path

Dynamic Client Registration remains available for older authorization servers, but it is deprecated for new MCP implementations.

> 动态客户端注册（DCR）对较旧的授权服务器仍然可用，但对新的 MCP 实现已弃用。

When using DCR, declare `application_type`:

> 使用 DCR 时，声明 `application_type`：

```json
{
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

- Desktop, mobile, command-line, and loopback clients use `native`.
  中文翻译：桌面、移动、命令行和回环客户端用 `native`。
- Remotely hosted browser applications use `web` and remote HTTPS redirects.
  中文翻译：远程托管的浏览器应用用 `web` 和远程 HTTPS 重定向。

Omitting the field can default to `web` in an OpenID Connect registration implementation and make a legitimate loopback redirect fail.

> 省略该字段时，OpenID Connect 注册实现可能默认 `web`，导致合法的回环重定向失败。

Keep DCR code behind an explicit fallback decision. Do not silently fall back after an arbitrary CIMD validation failure. That could turn a security failure into a weaker enrollment path.

> DCR 代码要放在显式的回退决策之后。不要在 CIMD 校验任意失败后静默回退——那可能把一次安全失败变成更弱的注册路径。

### Bind credentials to the issuer

> **【中文解读】** 凭证按精确 issuer 隔离存储：`issuer_credentials[issuer]` 与 `tokens[(issuer, resource)]`。发现结果从 auth-one 换成 auth-two 时要重新评估信任——绝不把第一个 issuer 的 client secret、DCR client id、注册访问令牌、refresh token 或 access token 发给第二个。CIMD 是例外：它本身是自托管 URL 而非 issuer 铸造的凭证，同一 URL 可移植到新 issuer，但授权响应与 token 仍按新 issuer 校验和存储。

Store issuer-minted enrollment material under the exact issuer:

> 把 issuer 铸造的注册材料存到精确的 issuer 名下：

```text
issuer_credentials[issuer] = pre_registered_or_dcr_client
tokens[(issuer, resource)] = access_token
```

If protected-resource discovery changes from `https://auth-one.example` to `https://auth-two.example`, re-evaluate trust. Never send the first issuer's client secret, DCR client id, registration access token, refresh token, or access token to the second. Pre-registered and DCR clients must use credentials issued for the new issuer.

> 如果受保护资源发现的结果从 `https://auth-one.example` 变成 `https://auth-two.example`，要重新评估信任。绝不把第一个 issuer 的 client secret、DCR client id、注册访问令牌、refresh token 或 access token 发给第二个。预注册和 DCR 客户端必须使用新 issuer 签发的凭证。

A CIMD client id is different because it is a self-hosted HTTPS URL, not a credential minted by an authorization server. The same CIMD URL is portable: a new trusted issuer fetches and validates the document without DCR re-registration. Authorization responses and tokens are still validated and stored under the new issuer.

> CIMD client id 不同：它是自托管的 HTTPS URL，不是授权服务器铸造的凭证。同一个 CIMD URL 可移植——新的受信 issuer 拉取并校验文档即可，无需 DCR 重新注册。但授权响应与 token 仍在新 issuer 名下校验和存储。

### Authorization code with PKCE

The interactive flow is:

> 交互式流程是：

1. Generate a high-entropy `code_verifier`.
  中文翻译：生成高熵 `code_verifier`。
2. Derive the S256 `code_challenge`.
  中文翻译：派生 S256 `code_challenge`。
3. Send the authorization request with exact `client_id`, `redirect_uri`, `scope`, `code_challenge`, and `resource`.
  中文翻译：发送授权请求，带精确的 `client_id`、`redirect_uri`、`scope`、`code_challenge` 和 `resource`。
4. Receive an authorization response containing `code` and, when provided, `iss`.
  中文翻译：接收包含 `code` 与（若提供）`iss` 的授权响应。
5. Validate `iss` against the exact recorded issuer before using any response field.
  中文翻译：在使用任何响应字段之前，先对照精确记录的 issuer 校验 `iss`。
6. Exchange the code with `code_verifier`, the same redirect URI, and the same `resource`.
  中文翻译：用 `code_verifier`、同一 redirect URI 和同一 `resource` 换取 token。
7. Store the resulting token under `(issuer, resource)`.
  中文翻译：把得到的 token 存到 `(issuer, resource)` 名下。

The `resource` parameter from RFC 8707 appears in both authorization and token requests. It identifies the canonical MCP server URI.

> 来自 RFC 8707 的 `resource` 参数同时出现在授权请求与 token 请求中，标识规范的 MCP 服务器 URI。

### Validate `iss` exactly

RFC 9207 prevents an authorization response from one issuer being confused with a response from another.

> RFC 9207 防止一个 issuer 的授权响应与另一个 issuer 的响应相混淆。

When `iss` is present, compare it to the recorded issuer without case folding, trailing-slash changes, default-port removal, or percent-encoding normalization. On mismatch, do not act on the code or even display attacker-controlled error details from that response.

> `iss` 存在时，与记录的 issuer 比较——不折叠大小写、不改尾斜杠、不去默认端口、不做百分号编码规范化。不匹配时，不要使用 code，甚至不要展示该响应中攻击者可控的错误详情。

An authorization server that includes `iss` advertises `authorization_response_iss_parameter_supported: true`. Current clients still validate a present `iss` even when that advertisement is missing.

> 包含 `iss` 的授权服务器会声明 `authorization_response_iss_parameter_supported: true`。即使缺少该声明，当前客户端仍要校验存在的 `iss`。

> 🤔 **【困惑】** Q: 为什么"精确字符串比较"这么较真？差个尾斜杠不行吗？A: 不行。issuer 是所有凭证与 token 存储的键。若 `https://auth.example.com` 与 `https://auth.example.com/` 视为相等，攻击者注册带尾斜杠的相似 issuer 就能挤进同一存储槽位、继承别人的凭证。OAuth 历史上多次账号接管都源于"规范化一下再比"的善意。RFC 9207 的设计就是字节级相等。

### Validate audience at the MCP server

The resource server accepts only tokens issued for itself:

> 资源服务器只接受为自己签发的 token：

```text
token.issuer == configured_authorization_server
token.audience == canonical_mcp_resource
```

Invalid, expired, wrong-issuer, or wrong-audience tokens receive 401. The MCP server must not accept or transit a token meant for another service.

> 无效、过期、错 issuer、错受众的 token 一律 401。MCP 服务器不得接受或转运给其他服务签发的 token。

### Request the smallest current scope

> **【中文解读】** 最小权限的落地：先请求当下所需 scope；后续工具需要更多时，服务器返回 403 + 权威 scope 挑战（`WWW-Authenticate` 带 `scope` 与 `resource_metadata`）。客户端解释新权限、取得同意、用合并 scope 集重跑授权流程、用新 JSON-RPC id 重试。不要假设被挑战的 scope 是 `scopes_supported` 的子集——挑战对当前操作是权威的。

Start with the scope needed now. If a later tool requires more, the server returns 403 with an authoritative scope challenge:

> 先请求现在需要的 scope。如果后续工具需要更多，服务器返回带权威 scope 挑战的 403：

```text
WWW-Authenticate: Bearer error="insufficient_scope",
  scope="notes:delete",
  resource_metadata="https://notes.example.com/.well-known/oauth-protected-resource/mcp"
```

The client explains the new permission, obtains consent, performs a new authorization flow with the combined scope set, and retries the MCP request with a new JSON-RPC id.

> 客户端向用户解释新权限、取得同意、用合并后的 scope 集执行新的授权流程，然后用新的 JSON-RPC id 重试 MCP 请求。

Do not assume the challenged scope is a subset of `scopes_supported`. The challenge is authoritative for the current operation.

> 不要假设被挑战的 scope 是 `scopes_supported` 的子集。挑战对当前操作是权威的。

### Authorization and the stateless MCP wire

> **【中文解读】** 授权与协议协商正交：token 授权主体，请求元数据协商协议行为，互不替代。线上校验固定顺序：JSON-RPC 与元数据类型 → 头文相等 → 版本支持。路由/版本头不匹配返回 400 `-32020`；头文一致但版本不支持返回 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法 404 `-32601`。每个请求错误（含 401/403）都是带原请求 id 的 JSON-RPC 错误信封；`WWW-Authenticate` 留在 HTTP 头；通知无 id，接受后 202 空体。

An authorized tool call still carries the complete current request envelope:

> 已授权的工具调用仍要携带完整的当前请求信封：

```text
POST /mcp
Authorization: Bearer <access-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.delete
```

```json
{
  "jsonrpc": "2.0",
  "id": 12,
  "method": "tools/call",
  "params": {
    "name": "notes.delete",
    "arguments": {"id": "note-7"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "oauth-lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

The token authorizes the principal. The request metadata negotiates protocol behavior. Neither substitutes for the other.

> token 授权主体；请求元数据协商协议行为。两者互不替代。

Validate the wire in a fixed order: JSON-RPC and metadata types, header and body equality, then protocol support. A routing or version-header mismatch returns HTTP 400 with `-32020`. If header and body agree on an unsupported version, return HTTP 400 with `-32022` and `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}`. An unknown method returns HTTP 404 with `-32601`.

> 按固定顺序校验线上格式：JSON-RPC 与元数据类型、头与正文相等、然后协议支持。路由或版本头不匹配返回 HTTP 400 `-32020`；头文一致但版本不支持，返回 HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法返回 HTTP 404 `-32601`。

Every request error, including 401 invalid token and 403 insufficient scope, is a JSON-RPC error envelope with the original request `id`. Structured recovery information belongs in optional error `data`; `WWW-Authenticate` remains an HTTP response header. A notification has no `id`, so it receives no JSON-RPC body. An accepted HTTP notification returns 202 with an empty body.

> 每个请求错误——包括 401 无效 token 和 403 权限不足——都是带原请求 `id` 的 JSON-RPC 错误信封。结构化恢复信息放在可选的 error `data` 里；`WWW-Authenticate` 仍是 HTTP 响应头。通知没有 `id`，不收 JSON-RPC 正文；被接受的 HTTP 通知返回 202 空体。

The server implements `server/discover` and advertises tools, so it also implements the mandatory `tools/list` method. Its tool descriptors have stable names, descriptions, and object-root `inputSchema` values. The list is deterministic and returns `resultType`, server identity metadata, a bounded `ttlMs`, and `cacheScope`. Discovery and a user-independent tool list can be available before authorization. Apply normal policy and private caching if either varies by principal.

> 服务器实现 `server/discover` 并通告工具，因此也实现必需的 `tools/list` 方法。工具描述符有稳定的名称、描述和对象根 `inputSchema`。列表是确定性的，返回 `resultType`、服务器身份元数据、有界的 `ttlMs` 和 `cacheScope`。发现与不随用户变化的工具列表可以在授权前提供；若任一随主体变化，就要应用常规策略和私有缓存。

### No token passthrough

An MCP server must not forward the client's MCP access token to a downstream API. Obtain a separate downstream token with the right audience or use an explicit token-exchange design. Audience validation only works when services refuse tokens minted for someone else.

> MCP 服务器不得把客户端的 MCP access token 转发给下游 API。要么获取受众正确的独立下游 token，要么使用显式的 token 交换设计。受众校验只有在各服务拒绝"为别人签发的 token"时才有效。

### Refresh tokens

Refresh tokens are optional. When issued, store them confidentially and key them by issuer and resource. Do not assume they exist. Rotate them when the authorization server supports rotation and detect reuse of invalidated values.

> Refresh token 是可选的。签发时按 issuer 和 resource 为键机密存储；不要假设它们存在。授权服务器支持轮换时就轮换，并检测失效值被重用。

```figure
t3-scope-stepup
```

## Build It | 动手构建

> **【中文解读】** `code/main.py` 是进程内协议与授权模拟器：受保护资源发现、授权服务器元数据、CIMD 注册、版本门控的 DCR 回退、application type 检查、PKCE、issuer 校验、资源绑定 token、scope 逐步升级、`server/discover`、`tools/list` 与无状态工具请求一次跑通。模型接收已解析的请求正文与路由头，不是完整 HTTP 适配器——传输层契约归 Lesson 09。

`code/main.py` is an in-process protocol and authorization simulator. It implements protected-resource discovery, authorization server metadata, CIMD enrollment, version-gated DCR fallback, application type checks, PKCE, issuer validation, resource-bound tokens, scope step-up, `server/discover`, `tools/list`, and a stateless tool request.

> `code/main.py` 是进程内协议与授权模拟器：受保护资源发现、授权服务器元数据、CIMD 注册、版本门控的 DCR 回退、application type 检查、PKCE、issuer 校验、资源绑定 token、scope 逐步升级、`server/discover`、`tools/list` 和一个无状态工具请求。

The model receives parsed request bodies and routing headers. It is not a complete HTTP adapter and does not parse `Content-Type` or `Accept`. Connect it to Lesson 09's Streamable HTTP adapter, which requires `Content-Type: application/json` and an `Accept` value containing both `application/json` and `text/event-stream`.

> 模型接收已解析的请求正文与路由头，不是完整 HTTP 适配器，不解析 `Content-Type` 或 `Accept`。把它接到 Lesson 09 的 Streamable HTTP 适配器上——那边要求 `Content-Type: application/json`，且 `Accept` 同时包含 `application/json` 与 `text/event-stream`。

Run it:

> 运行：

```bash
cd phases/13-tools-and-protocols/16-mcp-security-oauth-2-1
python3 code/main.py
python3 -m unittest discover code/tests -v
```

The output shows discovery first, CIMD enrollment, an ordinary read, two separate scope step-ups, and issuer-keyed credential storage.

> 输出依次展示：发现流程、CIMD 注册、一次普通读取、两次独立的 scope 逐步升级，以及按 issuer 为键的凭证存储。

## Use It | 实际使用

Map the simulator objects to production components:

> 把模拟器对象映射到生产组件：

- `ResourceServer.protected_resource_metadata` becomes the RFC 9728 endpoint.
  中文翻译：`ResourceServer.protected_resource_metadata` 对应 RFC 9728 端点。
- `AuthorizationServer.metadata` becomes RFC 8414 or OpenID Connect discovery.
  中文翻译：`AuthorizationServer.metadata` 对应 RFC 8414 或 OpenID Connect 发现。
- `Client.enroll` becomes CIMD resolution plus an explicit DCR compatibility branch.
  中文翻译：`Client.enroll` 对应 CIMD 解析加显式的 DCR 兼容分支。
- Issuer-minted client credentials and `tokens_by_issuer_resource` become encrypted records. A CIMD URL may remain portable while its authorization results remain issuer-bound.
  中文翻译：issuer 铸造的客户端凭证和 `tokens_by_issuer_resource` 对应加密记录。CIMD URL 可保持可移植，而其授权结果保持 issuer 绑定。
- `ResourceServer.handle` becomes middleware that validates current MCP headers, token, and tool scope before dispatch while keeping every request error in a matching JSON-RPC envelope.
  中文翻译：`ResourceServer.handle` 对应中间件——分发前校验当前 MCP 头、token 和工具 scope，并让每个请求错误都落在匹配的 JSON-RPC 错误信封里。

## Ship It | 产出物

This lesson ships `outputs/skill-oauth-scope-planner.md`. It now designs enrollment priority, issuer-bound credential storage, application type, PKCE, resource indicators, scope challenges, and the current stateless request boundary.

> 本课产出 `outputs/skill-oauth-scope-planner.md`。它现在设计的内容包括：注册优先级、issuer 绑定的凭证存储、application type、PKCE、资源指示器、scope 挑战，以及当前的无状态请求边界。

## Exercises | 练习题

1. Add refresh-token rotation and reject reuse of the previous refresh token.
   中文翻译：添加 refresh token 轮换，并拒绝上一个 refresh token 的重用。
2. Add an issuer allowlist. On issuer change, reuse only a portable CIMD URL; refuse all prior issuer-minted credentials and tokens.
   中文翻译：添加 issuer 允许列表。issuer 变更时只复用可移植的 CIMD URL，拒绝之前所有 issuer 铸造的凭证与 token。
3. Add an expiry to authorization codes and confirm a late exchange fails.
   中文翻译：给授权码加过期时间，确认迟到换取失败。
4. Build a web client variant with a remote HTTPS redirect and compare its DCR metadata to the native client.
   中文翻译：构建带远程 HTTPS 重定向的 web 客户端变体，并比较其 DCR 元数据与 native 客户端的差异。
5. Add a second resource under the same issuer. Confirm its access token cannot be used at the first resource.
   中文翻译：在同一 issuer 下添加第二个资源。确认它的 access token 不能用在第一个资源上。

## Key Terms | 术语速查表

| Term | Meaning | 中文 |
|------|---------|------|
| Protected-resource metadata | RFC 9728 document that identifies the resource and authorization servers | 受保护资源元数据：标识资源与授权服务器的 RFC 9728 文档 |
| CIMD | HTTPS metadata document whose URL is the OAuth client identifier | 客户端 ID 元数据文档：URL 即 OAuth 客户端标识的 HTTPS 元数据文档 |
| DCR | Deprecated dynamic client enrollment retained for compatibility | 动态客户端注册：已弃用、仅作兼容保留的动态注册 |
| `application_type` | `native` or `web`, used to validate redirect URI rules | 应用类型：`native` 或 `web`，用于校验重定向 URI 规则 |
| PKCE | Verifier and S256 challenge that protect an intercepted authorization code | 授权码交换证明密钥：保护被拦截授权码的 verifier 与 S256 challenge |
| `iss` | RFC 9207 authorization response issuer identifier | RFC 9207 授权响应签发方标识 |
| Resource indicator | RFC 8707 parameter that binds a token request to an MCP resource | 资源指示器：把 token 请求绑定到 MCP 资源的 RFC 8707 参数 |
| Audience | Resource for which a token is valid | 受众：token 对之有效的资源 |
| Step-up | New consent and token issuance for an additional current-operation scope | 逐步授权：为额外的当前操作 scope 进行的重新同意与 token 签发 |
| Issuer-bound credentials | Registration and token records isolated by exact authorization server issuer | 签发方绑定凭证：按精确授权服务器 issuer 隔离的注册与 token 记录 |

## Further Reading | 延伸阅读

- [MCP 2026-07-28 authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
  中文说明：MCP 授权规范正文——本课全部规则的权威来源。
- [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728)
  中文说明：受保护资源元数据 RFC——发现流程的起点。
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
  中文说明：资源指示器 RFC——token 受众绑定。
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207)
  中文说明：授权响应 `iss` 参数 RFC——防 issuer 混淆。
- [OAuth Client ID Metadata Document draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)
  中文说明：CIMD 草案——以 URL 为客户端标识的新注册机制。
