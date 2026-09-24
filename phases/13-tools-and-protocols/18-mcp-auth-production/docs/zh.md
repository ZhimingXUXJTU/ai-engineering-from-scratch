# MCP 生产级认证：签发者绑定的注册与 Token

> 第 16 课搭起了 OAuth 2.1 状态机。本课按 MCP 2026-07-28 规范加固它的生产边界：注册优先走 Client ID Metadata Document，已弃用的动态注册仅作兼容；授权响应要做签发者校验（RFC 9207）；客户端凭证按签发者隔离；JWKS 按计划刷新；每个无状态请求都做受众绑定。
>
> **规范说明（2026-07-28）：** 动态客户端注册（DCR）已被弃用，由 Client ID Metadata Documents 取代。DCR 保留为兼容机制。使用它时，客户端必须声明正确的 `application_type`。客户端要校验授权响应中出现的 RFC 9207 `iss` 值，并且绝不跨授权服务器签发者复用凭证。

> **【中文解读】** 第 16 课搭起了 OAuth 2.1 状态机；本课把它的边界加固到 MCP 2026-07-28 规范的生产要求：注册优先走 CIMD，DCR 降级为仅作兼容的已弃用路径；授权响应必须校验 RFC 9207 `iss`；客户端凭证按签发者隔离存放；JWKS 按计划刷新；每个无状态请求都做受众绑定检查。核心变化是"每个请求独立验证"——协议会话被移除后，不存在任何可以缓存身份决定的地方。

> **【拓展：MCP 2026-07-28 的注册范式转向】** 这一版规范把注册从"推"（DCR 的 `POST /register`）改为"拉"（CIMD：授权服务器按需拉取客户端自托管的元数据文档），信任锚从 IdP 的内部状态转移到 DNS；同时凭证按签发者隔离、token 按（签发者, 资源）成对存储，堵住跨 IdP 复用凭证与跨资源重放 token 的攻击面。同一版规范还移除了协议会话（见第 23 课毕业项目），这正是"每个请求都要重新验证"的根源。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13 · 16（OAuth 2.1 状态机、PKCE、资源指示器）——本课是其生产化；(2) Phase 13 · 17（网关）；(3) JWT 结构与 JWKS 概念；(4) 本课将逐一实现的规范：RFC 8414、RFC 7591、RFC 8707、RFC 9728、RFC 9207、RFC 7636、RFC 7662、RFC 7009。

**类型：** 构建
**语言：** Python（标准库）
**前置条件：** Phase 13 · 16（OAuth 2.1 状态机）、Phase 13 · 17（网关）
**时间：** 约 90 分钟

## 学习目标

- 通过 RFC 8414 元数据发现授权服务器并验证契约。
- 通过 Client ID Metadata Document 完成注册，并把已弃用的 DCR 隔离为后备路径。
- 校验 RFC 9207 `iss`；注册信息按授权服务器签发者做键；资源绑定的 token 按"签发者 + 资源"成对做键。
- 按计划缓存并刷新 JWKS 密钥，使签名验证在密钥轮换后依然存活。
- 用 RFC 8707 资源指示器把 token 固定到单个 MCP 资源，拒绝混淆代理式重用。
- 在 JWT 校验与 token 内省之间做出选择、定义吊销新鲜度，并在身份依赖不可用时安全失败。
- 把授权服务器、资源服务器和客户端分开，使每一方只执行属于自己的检查。
- 按部署检查清单审计授权服务器，拒绝不安全的注册或 token 复用。

## 问题引入

> **【中文解读】** 三个生产缺口：(1) 注册与凭证隔离——CIMD 优先、DCR 仅作兼容，且凭证必须按签发者隔离；(2) 密钥轮换——JWKS 缓存必须有刷新任务加回退获取；(3) 受众绑定——`token.aud` 与资源 URL 的比对是每个请求上的硬性检查，也是唯一防跨资源重放的手段。

第 16 课的模拟器在内存中运行 OAuth 2.1。生产环境有三个内存模拟器看不到的操作缺口。

第一个缺口是注册与凭证隔离。真实组织可能运行数百个 MCP 服务器和数千个 MCP 客户端。2026-07-28 修订版优先采用 **Client ID Metadata Document**：客户端用一个自己控制的带路径 HTTPS URL 作为标识符，授权服务器主动拉取元数据。RFC 7591 动态注册仅作为已弃用的兼容路径保留。当 DCR 无法避免时，请求必须声明正确的 `application_type`。客户端把注册信息按授权服务器签发者存储，把 access token 按 `(issuer, resource)` 对存储。签发者变了就要重新注册；资源不同就要单独做受众绑定。

第二个缺口是密钥轮换。JWT 验证依赖授权服务器的签名密钥，以 JSON Web Key Set（JWKS）形式发布。授权服务器按计划轮换这些密钥（通常每小时，事件响应时更快）。只在启动时获取一次 JWKS 的 MCP 服务器在轮换窗口到来前验证正常——之后所有请求失败，直到重启。生产环境把 JWKS 连线为缓存值：刷新任务在旧密钥过期前覆盖缓存，另加缓存未命中时的回退获取，以处理"token 由比缓存更新的密钥签名"的情况。

第三个缺口是受众绑定。第 16 课引入了 RFC 8707 资源指示器。在生产中，该指示器成为每个请求上的硬性声明检查。MCP 服务器把 `token.aud` 与自身的规范资源 URL 比对，不匹配就以 HTTP 401 拒绝。这是防御上游 MCP 服务器（或持有发给某一服务器的 token 的恶意客户端）在同一信任网格内把 token 重放给另一个服务器的唯一手段。

本课把每个缺口映射为认证面上的一个具体构件：元数据文档是一个 HTTP 端点；JWKS 缓存刷新是一个定时任务加一个键值缓存；JWT 验证是资源服务器在分发任何工具之前执行的一道例程。保持三个角色分离，每一方只执行属于自己的检查：授权服务器签发并轮换密钥，资源服务器缓存并验证，客户端发现并注册。

## 范围：第 16 课之后的生产强化

> **【中文解读】** 本课不重新定义 OAuth 流程——授权码状态机、PKCE、受保护资源发现、资源指示器都属于第 16 课。本课从这些契约已经存在之后开始：一个已部署的资源服务器如何在密钥轮换、不透明 token、吊销、依赖故障、灰度与事件响应中持续执行这些契约。

[第 16 课：MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md) 负责授权码状态机、PKCE、受保护资源发现、资源指示器和 scope 决策。本课不定义第二个 OAuth 流程。它从这些契约已经存在之后开始，追问一个已部署的资源服务器如何在密钥轮换、不透明 token 校验、吊销、依赖故障、灰度发布和事件响应期间持续执行这些契约。

生产边界更窄、更偏运维：

- JWT 路径在每个请求上校验锁定的签发者、算法、签名密钥、受众、时间声明和 scope，同时安全地刷新 JWKS。
- 不透明 token 路径调用签发者经认证的内省端点，并校验返回的 active 状态、受众或资源、过期时间、subject 和 scope。
- 吊销策略定义一个凭证必须在多短时间内失效，以及哪些缓存可以把这个事实拖慢。
- 故障策略决定当发现、JWKS、内省或吊销基础设施不可用时该怎么办。
- 证据记录是哪个签发者元数据、密钥集或内省响应、token 声明、策略版本和拒绝原因决定了结果，但不存储 token 本身。

这个分工让两课保持可组合：第 16 课证明流程成立；第 18 课证明一个 token 在到达真实 MCP 请求路径之后，要么仍然可信、要么被拒绝。

## 核心概念

> **【中文解读】** 本节逐个拆解生产认证面的构件：RFC 8414 授权服务器元数据、RFC 9728 受保护资源元数据（回顾）、CIMD（推荐默认注册）、RFC 7591（已弃用的兼容路径）、RFC 8707 资源指示器（回顾）、RFC 7636 PKCE（回顾）、MCP 2026-07-28 授权配置档、部署能力检查清单、JWKS 刷新模式、验证例程、不透明 token 内省、吊销新鲜度、依赖故障决策、受众重放演练、mix-up 攻击与故障模式。

### RFC 8414 — OAuth 授权服务器元数据

位于 `/.well-known/oauth-authorization-server` 的文档描述客户端需要的一切：

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

拿到 MCP 资源 URL 的客户端做链式发现：先由 RFC 9728 的 `oauth-protected-resource`（资源服务器的文档）指明签发者，再由 `oauth-authorization-server`（本 RFC）列出全部端点。客户端从不硬编码授权 URL。

对带路径的资源标识符，要把 well-known 段插在路径之前。例如 `https://mcp.example.com/team/server` 的受保护资源元数据位于 `https://mcp.example.com/.well-known/oauth-protected-resource/team/server`。把 `/.well-known/...` 追加在资源路径之后是错误写法。

在信任一个 IdP 用于 MCP 之前要验证的契约：

- `code_challenge_methods_supported` 包含 `S256`（RFC 7636 的 PKCE）。规范写得明确：该字段**缺失**即表示授权服务器不支持 PKCE，客户端**必须**拒绝继续。
- `grant_types_supported` 包含 `authorization_code`，并拒绝 `password` 和 `implicit`。
- 至少一条注册路径可用：`client_id_metadata_document_supported: true`（CIMD，首选）、预注册的客户端，或 `registration_endpoint`（已弃用的 RFC 7591 兼容路径）。
- 若 `authorization_response_iss_parameter_supported` 为 true，客户端必须要求授权响应返回 RFC 9207 `iss`，并在发送任何请求前与重定向前记录的签发者做精确比对。
- 对 OAuth 2.1，`response_types_supported` 恰为 `["code"]`。

若 `S256` 缺失，MCP 服务器拒绝在此 IdP 上部署——PKCE 没有降级模式。若两条注册路径都未公布且没有预注册的 `client_id`，同样无法注册；错的是部署清单，不是代码。

### RFC 9728（回顾）— 受保护资源元数据

第 16 课讲过 RFC 9728。生产中的增量是：这份文档是客户端查找 *此* MCP 服务器信任哪些授权服务器的唯一入口。单个 MCP 服务器可以接受来自多个 IdP 的 token（一个给员工、一个给合作伙伴）。RFC 9728 声明这个集合；RFC 8414 说明每个 IdP 支持什么。

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com", "https://partners.example.com"],
  "scopes_supported": ["mcp:tools.invoke"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://notes.example.com/docs"
}
```

### Client ID Metadata Documents（推荐默认）

> **【中文解读】** CIMD 把注册从"推"反转为"拉"：客户端用自己控制的一个带路径 HTTPS URL 直接充当 `client_id`，该 URL 解析到一份 JSON 元数据文档，授权服务器在 OAuth 流程中按需拉取。信任锚是 DNS。两条安全红线：SSRF 防护与 localhost 冒充警告。

CIMD 把注册从*推*反转为*拉*。客户端不再请求授权服务器铸造一个 `client_id`，而是用自己控制的一个 HTTPS URL 直接**充当** `client_id`。该 URL 解析到一份 JSON 元数据文档，授权服务器在 OAuth 流程中按需拉取它。信任以 DNS 为根：如果服务器运营方信任 `app.example.com`，它就信任从 `https://app.example.com/client.json` 提供服务的客户端。没有注册往返、没有可耗尽的 `client_id` 命名空间、也没有需要保持同步的每服务器状态。

客户端托管的元数据文档：

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

文档中的 `client_id` 值**必须**等于其托管 URL（授权服务器会验证这一点，不匹配即拒绝）。授权服务器在 RFC 8414 元数据中用 `client_id_metadata_document_supported: true` 公布支持。

就当前 CIMD 契约而言，`client_id`、`client_name` 和非空的 `redirect_uris` 数组是必填项。客户端标识符必须是一个带路径的绝对 HTTPS URL。`application_type` 可以带上，但它不是 CIMD 的必填字段。不要把 DCR 对 `application_type` 的要求照搬进首选的 CIMD 路径。

规范直言不讳的两个安全事实：

- **SSRF。** 授权服务器会拉取攻击者可提供的 URL，必须防御服务器端请求伪造（不得拉取内部/管理端点）。
- **localhost 冒充。** 仅靠 CIMD 挡不住本地攻击者认领合法客户端的元数据 URL 并绑定任意 `localhost` redirect。授权服务器**必须**在同意页清楚展示 redirect URI 主机名，并**应当**对仅 `localhost` 的 redirect 发出警告。

因为 CIMD 不需要服务器端状态，也就没有 DCR 那样需要架设的注册器。客户端一侧是只读的：把元数据文档放在一个静态 HTTPS 端点上，让授权服务器来拉。

如果授权服务器运营方已经分配了客户端标识符，应先使用这个按签发者划定的注册，再去尝试自动注册。否则优先 CIMD。只有当签发者既不能预注册也不能用 CIMD 时，才使用已弃用的 DCR。

### RFC 7591：已弃用的兼容注册

> **【中文解读】** RFC 7591 动态客户端注册在 2026-07-28 版被正式弃用，仅为无法消费 CIMD 且预注册不现实的授权服务器保留。关键变化：`application_type` 不是装饰——回环桌面客户端声明 `native`，服务器托管客户端声明 `web` 并使用 HTTPS redirect URI。

DCR 在 2026-07-28 修订版中已弃用。只对既无法消费 CIMD、预注册又不现实的授权服务器保留它。兼容客户端 POST：

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

服务器以 `client_id` 和一个供后续更新使用的 `registration_access_token` 响应：

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

`application_type` 不是摆设。回环桌面客户端声明 `native`；服务器托管客户端声明 `web` 并使用 HTTPS redirect URI。`token_endpoint_auth_method: none` 是公共原生客户端的正确默认值——它只拿到 `client_id`，由 PKCE 提供持有证明。

三个生产陷阱：

- 注册端点必须按源 IP 限流。否则恶意行为者可以脚本化发起数百万假注册，耗尽 `client_id` 命名空间。在注册器处理请求之前先跑限流检查。
- 某些企业 IdP 要求 `software_statement`（为客户端背书的签名 JWT）。本课的 mock 跳过了它；生产环境要连线一个验证步骤，拒绝来自非 localhost redirect URI 的未签名注册。
- `registration_access_token` 必须以哈希存储，而非明文。该 token 被盗意味着攻击者可以改写客户端的 redirect URI。

### RFC 8707（回顾）— 资源指示器

第 16 课确立了形态。生产规则：每个 token 请求都带 `resource=<canonical-mcp-url>`，MCP 服务器在每次调用上验证 `token.aud` 与自身资源 URL 匹配。规范 URI 是服务器的*最具体*标识符：scheme 与 host 小写、无 fragment、按惯例无尾部斜杠。路径组件**不**按规则剥除——当需要标识单个 MCP 服务器时规范会保留它。`https://mcp.example.com`、`https://mcp.example.com/mcp`、`https://mcp.example.com:8443`、`https://mcp.example.com/server/mcp` 都是合法的规范 URI。每个服务器选定一个，并把 `aud` 精确固定到它。（本课 mock 为简洁起见用裸主机受众如 `https://notes.example.com`；在同一 origin 下托管多个 MCP 服务器的部署靠路径区分它们。）

### RFC 7636（回顾）— PKCE

PKCE 在 OAuth 2.1 中是强制的。本课的授权码流程始终携带 `code_challenge` 和 `code_verifier`。服务器拒绝任何缺少 verifier、或 verifier 哈希后与存储的 challenge 不符的 token 请求。

### MCP 2026-07-28 授权配置档

> **【中文解读】** 当前修订版保持 OAuth 资源服务器边界，同时把 MCP 传输变为无状态：没有可以缓存身份决定的协议会话，授权层因此对每个请求独立验证。CIMD 优先、DCR 已弃用、凭证按签发者隔离是本版的三个签名式变化。

当前 MCP 修订版保持 OAuth 资源服务器边界，同时把 MCP 传输变为无状态。没有可以用来缓存身份决定的协议会话，授权层因此对每个请求独立验证：

- 实现 RFC 9728 受保护资源元数据，其位置要么通过 401 上的 `WWW-Authenticate: Bearer resource_metadata="..."` 头给出，**要么**用 well-known URI `/.well-known/oauth-protected-resource`（SEP-985 把该头变为可选并配 well-known 回退）。元数据的 `authorization_servers` 字段**必须**至少列出一个服务器。
- 只在**每个**请求上经 `Authorization: Bearer ...` 接受 token——绝不放进查询串，绝不能只在会话开始时验证一次。
- 每个请求都验证 `aud`、`iss`、`exp` 和必需的 scope。服务器**必须**验证 token 是专门为它签发的（受众）；`aud` 缺失或不匹配一律拒绝，绝不当作通配符。
- 在 401/403 上返回 `WWW-Authenticate: Bearer`，携带 `error=...`、`resource_metadata="<PRM-URL>"` 参数（元数据文档的 URL，*而非*裸资源），403 的 `insufficient_scope` 再加 `scope="..."`。注意：该参数叫 `resource_metadata`，是一个发现指针——challenge 里没有 `resource` 参数。
- 授权服务器发现**既**接受 RFC 8414 OAuth 元数据，**也**接受 OpenID Connect Discovery 1.0；客户端必须按优先级依次尝试两种 well-known 后缀。
- **mix-up 攻击**由客户端（而非服务器）防御：重定向前记录预期的 `issuer`，在兑换 code 之前校验实际授权响应中返回的 `iss` 值（RFC 9207）。仅靠 PKCE 挡不住 mix-up，因为客户端会把 `code_verifier` 交给它被引去的那家 token 端点。
- 一个客户端凭证只属于一个授权服务器签发者。若发现解析到了另一个签发者，客户端应重新注册，而不是拿旧的 `client_id`、注册 token 或 access token 去硬闯。
- CIMD 是首选注册机制。DCR 已弃用；兼容用的 DCR 请求仍要声明正确的 `application_type`。

OAuth 2.1 草案是底座；RFC 8414/7591/8707/9728/9207 + RFC 7636 + CIMD 是表层；MCP 规范是配置档。

### 部署能力检查清单

> **【中文解读】** 不要信厂商功能表，要信实际部署的授权服务器返回的元数据。门控是机械的：逐项核对签发者、PKCE、注册路径、`iss` 校验、资源绑定、凭证存储键与 DCR 兼容声明；必填字段缺失就失败关闭。

厂商功能表很快过期。改为检查你实际要部署的那个授权服务器返回的元数据。门控是机械的：

| 检查项 | 必须的决策 |
|---|---|
| 发现的签发者 | 与策略预期的 HTTPS 签发者精确一致 |
| PKCE | 公布了 `S256`；否则停止 |
| 注册 | CIMD 优先、预注册可接受、DCR 仅作已弃用兼容 |
| 授权响应 | 出现或已公布即校验 RFC 9207 `iss` |
| 资源绑定 | token 请求携带 `resource`；资源服务器要求匹配的 `aud` |
| 凭证存储 | client ID 与注册凭证按签发者做键；access token 按签发者加资源做键 |
| DCR 兼容 | 声明 `native` 或 `web`；拒绝与声明的应用类型不符的 redirect URI |

不要从产品名或定价档推断支持能力。把发现的文档捕获进部署证据，必填字段缺失时失败关闭。

### JWKS 刷新模式（AS 轮换，资源服务器刷新）

> **【中文解读】** 区分两个动词：**轮换（rotate）**是授权服务器的事；**刷新（refresh）**是资源服务器唯一能做的事。缓存未命中的回退必须是幂等的"重新拉取"，绝不能是"轮换并铸造"——后者既造不出缺失的 `kid`，还会被随机 `kid` 喷射打成自伤式 DoS。

把两个动词分开，混用它们是真实的生产 bug：

- **轮换（rotate）**是*授权服务器*做的事：铸造新签名密钥、发布进 JWKS、稍后退役旧密钥。资源服务器与此无关也做不到——它不持有 IdP 的私钥。
- **刷新（refresh）**是*资源服务器*做的事：重新 `GET` 已发布的 JWKS 进缓存。这是资源服务器唯一会执行的 JWKS 操作。

生产故障模式是缓存过期。用一个定时刷新任务加一个键值缓存解决。资源服务器运行一个作业（cron、timer，运行时提供什么都行），按固定间隔拉取 `<issuer>/.well-known/jwks.json` 并覆盖 `cache[issuer] = {keys, fetched_at}`。验证器从该缓存读取。某个 token 的 `kid` 不在缓存中时，触发**一次**同步刷新作为回退，然后复查。这同时覆盖两种情况：计划内刷新，以及"由全新密钥签名的 token 在下一次计划刷新之前到达"的密钥重叠窗口。

回退**必须是重新拉取，绝不许是轮换**。若把缓存未命中路径接到"轮换并铸造"，会坏两件事：(1) 铸造新密钥得到的 `kid` *仍然*匹配不上 token，查找照样失败；(2) 攻击者用随机 `kid` 喷射 token，逼出无上限的密钥创建——自伤式 DoS。重新拉取是幂等的，伪造的 `kid` 最多浪费一次拉取。

缓存形态：

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

同时持有两个密钥是稳态。授权服务器轮换时先引入下一个密钥（`k_2026_04`），再退役前一个（`k_2026_03`），因此旧密钥签发的 token 在过期前仍然有效。缓存持有两者的并集；验证器按 `kid` 选用。

> 💡 **【类比】** JWKS 刷新像消防站的暗号本。授权局（消防局）定期换暗号（签名密钥），各消防站（MCP 服务器）必须人手一册最新暗号本，否则夜间演习（凌晨 3 点的用户请求）全部认证失败。正确姿势：各站订阅定时换发（cron 刷新）；新旧暗号并行一段时间（重叠窗口）；有人拿新暗号敲门而本子还没更新时，现场打电话核实一次（缓存未命中同步回退）——而不是自己编一个新暗号（rotate-as-fallback）。

### 验证例程

MCP 服务器在分发任何工具之前先跑验证。`code/main.py` 的形态：

```python
result = server.validate(bearer_token, required_scope="mcp:tools.invoke")
if not result["valid"]:
    return {"status": result["status"], "WWW-Authenticate": result["www_authenticate"]}
```

`validate` 解码 JWT，从 JWKS 缓存解析签名密钥（未命中时刷新一次），验证签名，然后把 `iss` 对照允许列表、把 `aud` 对照本服务器的规范资源、再查 `exp` 和必需 scope——第一次失败即返回 `WWW-Authenticate` challenge。把它保持为资源服务器上的单一例程，意味着每个入口（每次工具调用、每种传输）都经过同一套检查；不存在未经验证就触达工具的路径。

### 不透明 token 用内省，不是猜测

> **【中文解读】** 不是所有 access token 都是 JWT。不透明 token 必须经 RFC 7662 内省端点验证；缓存键用"签发者 + token 单向摘要 + MCP 资源"；验证模式不能由 token 内容决定——攻击者可控的内容不能选择验证路径。

不是每个 access token 都是 JWT。如果签发者发布的是不透明 token，资源服务器无法把它解码成可信声明。它把 token 经认证的后端通道发到签发者的 RFC 7662 内省端点，并要求 `active: true`、预期的签发者上下文、精确的 MCP 受众或资源、未过期的时间声明，以及该具体工具所需的 scope。

内省缓存按签发者、token 单向摘要和 MCP 资源做键。绝不用明文 token 当日志或缓存标签。正向缓存条目的有效期取"token 过期时间、签发者缓存指引、部署的吊销新鲜度目标"三者中最早者。负向缓存要足够短，以免新签发的 token 被误判为不活跃。针对某一资源的内省结果不能授权另一个资源——即使不透明 token 字符串完全相同。

不要根据攻击者可控的 token 内容选择验证模式。把"JWT 还是内省"钉死在已验证的签发者元数据与部署配置上。JWT 路径上，锁死接受的算法与可信的 `jwks_uri`；绝不跟随仅由 token 头指定的密钥 URL 或算法。

### 吊销是新鲜度契约

> **【中文解读】** RFC 7009 的吊销请求不会抹掉各资源服务器已缓存的副本。要定义"最大可接受吊销延迟"并让所有缓存遵守它。验证语句"至多在声明的吊销窗口之后，每个副本都拒绝该凭证"要通过负载均衡器测试，而不是只测一个热进程。

RFC 7009 允许客户端请求授权服务器吊销 token。但该请求不会抹掉已被每个资源服务器缓存的副本。定义最大可接受的吊销延迟，并让每个缓存都遵守它。

不透明 token 部署可以对每次高风险调用都做内省或使用短正向缓存，实现更紧的吊销。自包含 JWT 部署通常组合使用：短 access token 有效期 + refresh token 吊销、面向全签发者事件的密钥退役，以及应急本地拒绝用的 subject/session/token-id denylist。签名的 JWT 在过期前密码学上始终有效——除非资源服务器握有当前的外部吊销证据。

登出、账号停用、撤回同意和事件响应是不同的触发器，但必须收敛为一句可度量的陈述：至多在声明的吊销窗口之后，每个副本都拒绝该凭证。这句话要通过负载均衡器验证，而不是只对着一个热进程。

### 依赖故障需要预先声明的决策

> **【中文解读】** 可用性策略不能在异常处理器里即兴发挥。依赖故障与无效凭证必须分开分类：前者是带健康与重试策略的运维错误，后者是授权拒绝——两者都到不了工具处理器，也都不许把 token 内容泄漏进审计证据。

绝不在异常处理器里即兴制定可用性策略。

| 故障 | 安全生产行为 |
|---|---|
| 定时 JWKS 刷新失败，已知 `kid` 仍在有界有效的缓存中 | 只在声明的 stale-on-error 窗口内继续，并输出降级健康证据 |
| token 的 `kid` 未知且唯一允许的刷新失败 | 拒绝；绝不接受无法验证的签名 |
| 内省不可用 | 受保护调用失败关闭；不把网络故障转成 `active: true` |
| 受保护资源或签发者元数据意外变更 | 停止新注册与 token 获取；只在有界事件策略下保留显式锁定且未过期的配置 |
| 吊销端点不可用 | 如实报告登出/吊销未完成，尽可能在本地把凭证标记为不可用，不得声称全局吊销成功 |
| 时钟源或声明类型无效 | 拒绝，而不是放宽偏差直到 token 通过 |

把依赖故障与无效凭证分开分类。依赖中断是带健康与重试策略的运维错误；坏的签名、签发者、受众、过期时间或 scope 是授权拒绝。两者都到不了工具处理器，也都不应把 token 内容泄漏进审计证据。

### 受众重放演练（access token 特权限制）

> **【中文解读】** Server A 与 Server B 注册到同一授权服务器；A 被攻陷后攻击者拿用户的 notes token 去敲 B。B 的验证器在 `aud` 检查处失败，返回 401 并带 `resource_metadata` 指针。受众声明是协议层对这类攻击的唯一防御——规范称之为 **access-token privilege restriction**。

服务器 A（`notes.example.com`）与服务器 B（`tasks.example.com`）都注册到同一个授权服务器。服务器 A 被攻陷。攻击者拿到用户的 notes token 并向服务器 B 重放。

服务器 B 的验证器：

1. 解码 JWT，按 `kid` 取 JWKS，验证签名。
2. 把 `iss` 对照其受保护资源元数据的 `authorization_servers`。（通过——同一 IdP。）
3. 检查 `aud == "https://tasks.example.com"`。（失败——token 的 `aud` 是 `https://notes.example.com`。）
4. 返回 401，带 `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`。

受众声明是协议层防御此攻击的唯一手段。为性能跳过它是最常见的生产错误；验证器必须在每个请求上运行，而不是只在会话开始时。规范称之为 **access-token privilege restriction**（access token 特权限制）：MCP 服务器 `MUST` 拒绝任何受众中未点名它的 token。

> **命名说明。** 规范把 *confused deputy*（混淆代理）一词留给另一个相关但不同的问题：MCP 服务器作为第三方 API 的 OAuth **代理**、使用静态 client ID、在未取得每客户端用户同意的情况下转发 token。受众绑定修复上面的重放；混淆代理的修复是每客户端同意**加上**绝不把入站 token 直接透传给上游 API（MCP 服务器 `MUST` 为自己获取单独的上游 token）。

### mix-up 攻击（服务器给不了的客户端侧防御）

客户端一生会与许多授权服务器打交道。恶意 AS 可以设法让客户端把诚实 AS 的授权码拿到攻击者的 token 端点去兑换。受众绑定在这里帮不上忙——攻击发生在任何 token 存在之前。防御在客户端一侧（RFC 9207）：

1. 重定向之前，客户端从已验证的 AS 元数据记录预期的 `issuer`。
2. 收到授权响应时，客户端在任何地方发送 code 之前，把返回的 `iss` 参数与记录的签发者比对（简单字符串比较，不做规范化）。
3. 不匹配（或 AS 已公布 `authorization_response_iss_parameter_supported` 却缺少 `iss`）→ 拒绝，连 `error` 字段都不要展示。

仅 PKCE 挡不住 mix-up，因为客户端会把 `code_verifier` 交给它被引去的那家 token 端点。这正是规范把签发者与 PKCE verifier、`state` 一起按请求记录的原因。

### 故障模式

> **【中文解读】** 八个故障模式速记：过期 JWKS、把"轮换"当回退、缺失 `aud`、缺 `iss` 检查、scope 升级竞态、注册 token 被盗、`iss` 未锁定、凭证/token 缓存键碰撞。最后一条是 2026-07-28 版新增：注册按签发者做键、token 按（签发者, 资源）做键，签发者一变就重新注册。

- **过期 JWKS。** AS 轮换密钥后验证器拒绝有效 token。修复是上面的定时刷新 + 未命中重拉模式。绝不在没有刷新任务的情况下缓存 JWKS。
- **把轮换当回退。** 把缓存未命中路径接到"轮换并铸造"而不是重新拉取是真实的 bug：它永远造不出缺失的 `kid`，还会把攻击者可控的 `kid` 值变成密钥创建 DoS。回退必须是幂等的 `refresh-jwks`。
- **缺失 `aud` 声明。** 一些 IdP 默认省略 `aud`，除非 token 请求中带了 `resource`。验证器必须拒绝缺失 `aud` 的 token，而不是把缺失当通配符。
- **缺 `iss` 检查导致 mix-up。** 不把 RFC 9207 `iss` 授权响应参数与重定向前记录的签发者比对的客户端，可能被引到攻击者的 token 端点去兑换诚实 AS 的 code。这是客户端侧的失败；资源服务器无法补救。
- **scope 升级竞态。** 同一用户的两个并发 step-up 流程都可能成功，产生两个 scope 不同的 access token。验证器必须使用请求上呈现的那个 token，而不是去查"用户当前 scope"——那会打开 TOCTOU 窗口。
- **注册 token 被盗。** 泄漏的 `registration_access_token` 让攻击者可以改写 redirect URI。静态哈希存储；要求客户端每次更新出示明文；一有怀疑就轮换。
- **`iss` 未锁定。** 接受任意 `iss` 的验证器会让攻击者自建授权服务器、为目标受众注册客户端并签发 token。受保护资源元数据的 `authorization_servers` 列表就是允许列表；强制执行它。
- **凭证或 token 缓存碰撞。** 只按资源给注册做键的客户端，会把一个授权服务器的身份递给另一个；只按签发者给 access token 做键的客户端，会把 token 重放到错误的受众。注册按已验证的签发者做键，access token 按 `(issuer, resource)` 做键，签发者一变就重新注册。

```figure
t3-jwks-rotate
```

## 用框架实现

> **【中文解读】** `code/main.py` 用标准库 Python 和三个角色（`AuthorizationServer`、`ResourceServer`、`Client`）走完整生产流程：发布元数据 → 检查注册选项与 S256 → 预注册/CIMD 优先、DCR 单独可测 → 校验授权响应 `iss` → PKCE + 资源指示器 → Bearer 调用工具 → JWKS 缓存验证 → 密钥轮换后无需重启继续验证 → 受众重放得到 401。

`code/main.py` 用标准库 Python 和三个角色——`AuthorizationServer`、`ResourceServer`、`Client`——走完整生产流程。流程：

在仓库根目录运行：

```bash
cd phases/13-tools-and-protocols/18-mcp-auth-production
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

第一条命令打印签发者绑定的注册与 token 验证记录；第二条报告 18 项通过的检查。两条命令都不打开网络监听、不写入凭证。

1. 授权服务器在 `/.well-known/oauth-authorization-server` 发布 RFC 8414 元数据。
2. MCP 客户端调用元数据端点，检查注册选项（CIMD 看 `client_id_metadata_document_supported`，DCR 看 `registration_endpoint`）与 `S256` PKCE 支持。
3. 客户端先查按签发者划定的预注册，否则用它的 HTTPS Client ID Metadata Document 注册。已弃用的 DCR 仍保留为可单独测试的兼容方法。
4. 客户端记录已验证的签发者，创建 S256 challenge，收到一次性授权码和 `iss`，校验返回的签发者，再用原始 verifier 和 RFC 8707 `resource` 指示器兑换 code。
5. MCP 客户端以 `Authorization: Bearer ...` 调用 MCP 服务器上的工具。
6. MCP 服务器运行 `validate`，从 JWKS 缓存解析签名密钥。
7. IdP 轮换一个密钥；定时刷新把 JWKS 重新拉进缓存。
8. 下一次调用无需重启即针对刷新后的密钥验证，且旧 token 在重叠窗口内仍然有效。
9. 针对另一个 MCP 资源的受众重放尝试得到 401，带 `audience mismatch` 和 `resource_metadata` 指针。

这里的 JWT 用 HS256 加共享密钥（使本课仅在标准库上运行）。生产使用 RS256 或 EdDSA 加上述 JWKS 模式；验证逻辑其余完全相同。因为 IdP 与资源服务器同在一个进程，`refresh_jwks` 直接读授权服务器的密钥表；走线缆时它就是对 `jwks_uri` 的一次 HTTP `GET`。

## 产出物

本课产出 `outputs/skill-mcp-auth.md`。给定 MCP 服务器配置和 IdP 能力集，该 skill 生成需要架设的认证面——受保护资源元数据、该用的注册路径（CIMD、预注册或 DCR 后备）、JWKS 刷新计划、scope 映射，以及 IdP 不满足完整 RFC 配置时的拒绝规则。

## 练习题

1. 运行 `code/main.py`，追踪流程。注意第 6 步 IdP 如何轮换密钥、定时 `refresh_jwks` 如何重拉已发布的密钥集，以及旧 token（重叠窗口）与新 token 如何都无需重启即可验证。

2. 向受保护资源元数据的 `authorization_servers` 列表添加新 IdP。签发一个由新 IdP 签名的 token，确认验证器接受；再签发一个由未列出的 IdP 签名的 token，确认验证器以 `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"` 拒绝。

3. 给 `register_client` 加一个在注册器接受请求之前运行的限流检查。用按源 IP 做键的小字典实现每 IP 令牌桶。

4. 阅读 RFC 7591，找出本课 `/register` 处理器未验证的两个字段并补上验证。（提示：`software_statement` 与 `redirect_uris` 的 URI scheme。）

5. 添加第二个授权服务器。确认客户端存了独立的按签发者做键的注册，并拒绝复用第一个签发者的 token 或 `client_id`。

6. 证明 DoS 修复。给验证器送一个随机 `kid` 的 token，确认 `refresh_jwks` 至多运行一次且授权服务器的密钥数不增长。然后故意把回退改接"轮换并铸造"，看密钥数随每个伪造 token 上升——最后恢复重新拉取。

7. 用 `native` 和 `web` 两种客户端演练已弃用的 DCR。确认带 HTTP redirect URI 的 web 客户端与没有精确回环 redirect 的 native 客户端都被拒绝。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| ASM | "OAuth 元数据文档" | RFC 8414 `/.well-known/oauth-authorization-server` JSON | Authorization Server Metadata |
| CIMD | "客户端元数据 URL" | Client ID Metadata Document：充当 `client_id` 的 HTTPS URL，由 AS 拉取 JSON。MCP 2026-07-28 首选注册方式 | Client ID Metadata Document |
| DCR | "自助客户端注册" | RFC 7591 `POST /register`；在当前 MCP 中已弃用，仅作兼容保留 | Dynamic Client Registration |
| JWKS | "JWT 验证公钥" | JSON Web Key Set，从 `jwks_uri` 获取，按 `kid` 索引 | JSON Web Key Set |
| 轮换 vs 刷新 | "更新密钥" | 轮换 = AS 铸造/退役签名密钥；刷新 = 资源服务器重新拉取已发布的集合。资源服务器只会刷新 | Rotate vs refresh |
| 资源指示器 | "受众参数" | RFC 8707 `resource` 参数，把 token 固定到一个服务器 | Resource indicator |
| `aud` 声明 | "受众" | 验证器与规范资源 URL 比对的 JWT 声明 | `aud` claim |
| 受众重放 | "token 重放" | 为服务器 A 签发的 token 被呈现给服务器 B；由受众校验防御（规范：access-token privilege restriction） | Audience replay |
| 混淆代理 | "代理 token 滥用" | 使用静态 client ID 的 MCP 代理未经每客户端同意转发 token；与受众重放不同 | Confused deputy |
| mix-up 攻击 | "错误的 token 端点" | 客户端被引到攻击者端点兑换诚实 AS 的 code；由客户端经 RFC 9207 `iss` 防御 | Mix-up attack |
| `iss` 允许列表 | "受信授权服务器" | 受保护资源元数据 `authorization_servers` 中命名的集合 | `iss` allow-list |
| `resource_metadata` | "PRM 文档在哪" | 401/403 上指向 RFC 9728 元数据 URL 的 `WWW-Authenticate` 参数 | resource_metadata |
| 公共客户端 | "原生或浏览器客户端" | 无 `client_secret` 的 OAuth 客户端；由 PKCE 补偿 | Public client |
| `WWW-Authenticate` | "401/403 响应头" | 携带 `Bearer error=...` 指令，驱动客户端恢复 | WWW-Authenticate |

## 延伸阅读

- [MCP 授权规范（2026-07-28）](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)——本课实现的当前 MCP 授权配置档
- [MCP 2026-07-28 变更日志](https://modelcontextprotocol.io/specification/2026-07-28/changelog)——CIMD、签发者校验、DCR 弃用与按签发者做键的凭证变更
- [OAuth Client ID Metadata Document 草案](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00)——CIMD："URL 即 client_id"的注册机制
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414)——发现契约
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591)——DCR（后备路径）
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636)——公共客户端持有证明
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707)——受众固定
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728)——资源服务器发现
- [RFC 9207 — OAuth 2.0 Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207)——防御 mix-up 攻击的 `iss` 参数
- [RFC 7662 — OAuth 2.0 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)——不透明 token 的内省端点
- [RFC 7009 — OAuth 2.0 Token Revocation](https://datatracker.ietf.org/doc/html/rfc7009)——token 吊销，本课的"新鲜度契约"
