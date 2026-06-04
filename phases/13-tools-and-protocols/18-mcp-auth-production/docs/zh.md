# MCP 生产级认证 — DCR、JWKS 轮换与受众绑定 Token

> 第 16 课在内存中搭建了 OAuth 2.1 状态机。生产环境有三个操作缺口：动态客户端注册（RFC 7591）、授权服务器元数据发现（RFC 8414）、不会中断凌晨 3 点 token 验证的 JWKS 轮换，以及拒绝混淆代理重用的受众绑定 token。本课通过 iii 原语将所有这些连接起来，使认证面可观察、可重启、可重放。

> **【中文解读】** 第 16 课在内存中搭建了 OAuth 2.1 状态机。生产环境有三个操作缺口：注册、密钥轮换和受众绑定。本课通过 iii 原语将所有这些连接起来。

> **【拓展】** iii 原语（registerTrigger、registerFunction、state::set/get）是本课的核心抽象。每个认证端点和后台作业都是 iii 原语——HTTP 触发器返回函数输出，JWKS 轮换是 cron 触发器写入 state，JWT 验证是通过 iii.trigger 调用的函数。重启引擎后触发器注册表重建、state 存活，认证面无需手工恢复。

**类型：** 构建
**语言：** Python（标准库，iii 原语为课程环境模拟）
**前置条件：** Phase 13 · 16（OAuth 2.1 状态机），Phase 13 · 17（网关）
**时间：** 约 90 分钟

## 学习目标

- 通过 RFC 8414 元数据发现授权服务器并验证契约。
- 实现 RFC 7591 动态客户端注册使 MCP 客户端无需管理员干预即可注册。
- 使用 cron 触发器缓存和轮换 JWKS 密钥使签名验证在密钥轮换后仍然存活。
- 使用 RFC 8707 资源指示器将 token 绑定到单个 MCP 资源并拒绝混淆代理重用。
- 将每个端点和后台作业连接为 iii 原语——HTTP 触发器、cron 触发器、命名函数和 `state::*` 读取——使单次重启重建整个认证面。
- 阅读 IdP 能力矩阵并在 IdP 不能满足 MCP 认证配置时拒绝部署。

## 问题引入

第 16 课的模拟器在内存中运行 OAuth 2.1。生产环境有三个内存模拟器看不到的操作缺口。

第一个缺口是注册。真实组织运行数百个 MCP 服务器和数千个 MCP 客户端。操作者不会手工注册每个 Cursor 用户为 OAuth 客户端。RFC 7591 动态客户端注册让客户端 `POST /register` 到授权服务器并当场获得 `client_id`。服务器在 RFC 8414 元数据中发布 `registration_endpoint`；客户端无需带外配置即可发现它。

第二个缺口是密钥轮换。JWT 验证依赖授权服务器的签名密钥，以 JSON Web Key Set (JWKS) 发布。授权服务器按计划轮换这些密钥（通常每小时，事件响应时更快）。启动时只获取一次 JWKS 的 MCP 服务器在轮换窗口到来前验证正常——之后所有请求失败直到重启。生产环境需要缓存 JWKS 并设置在过期前覆盖的刷新任务，加上缓存未命中时的回退获取。

第三个缺口是受众绑定。第 16 课引入了 RFC 8707 资源指示器。在生产中，该指示器成为每个请求的硬性声明检查。MCP 服务器在每个请求上比较 `token.aud` 与自身规范资源 URL，不匹配则以 HTTP 401 拒绝。这是防御上游 MCP 服务器（或持有发给一个服务器的 token 的恶意客户端）在同一信任网格中向另一个服务器重放 token 的唯一手段。

本课将每个缺口视为 iii 原语。元数据文档是返回函数输出的 HTTP 触发器。JWKS 轮换是调用 `auth::rotate-jwks` 的 cron 触发器，写入 `state::set("auth/jwks/<issuer>", ...)`。JWT 验证是其他函数通过 `iii.trigger("auth::validate-jwt", token)` 调用的函数。MCP 服务器本身只是另一个在分发前调用验证的 HTTP 触发器。重启引擎：触发器注册表重建；state 存活；认证面无需手工恢复即可运行。

## 核心概念

### RFC 8414 — OAuth 授权服务器元数据

在 `/.well-known/oauth-authorization-server` 的文档描述客户端需要的一切：

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

给定 MCP 资源 URL 的客户端链式发现：RFC 9728 的 `oauth-protected-resource`（资源服务器的文档）命名签发者，然后 `oauth-authorization-server`（本 RFC）命名每个端点。客户端永远不硬编码授权 URL。

在信任 IdP 用于 MCP 之前验证的契约：

- `code_challenge_methods_supported` 包含 `S256`（RFC 7636 PKCE）。
- `grant_types_supported` 包含 `authorization_code` 并拒绝 `password` 和 `implicit`。
- `registration_endpoint` 存在（RFC 7591 支持）。
- `response_types_supported` 正好是 `["code"]`（OAuth 2.1）。

如果任何一项缺失，MCP 服务器拒绝针对此 IdP 部署。部署清单有误，不是代码。

### RFC 9728（回顾）— 受保护资源元数据

第 16 课覆盖了 RFC 9728。生产中的增量：此文档是客户端寻找 *此* MCP 服务器信任的授权服务器的唯一位置。单个 MCP 服务器可以接受来自多个 IdP 的 token（一个给员工，一个给合作伙伴）。RFC 9728 声明该集合；RFC 8414 文档每个 IdP 支持什么。

### RFC 7591 — 动态客户端注册

没有 DCR，每个 MCP 客户端（Cursor、Claude Desktop、自定义 Agent）都需要与 IdP 管理员的带外交换。有了 DCR，客户端 POST：

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

服务器响应 `client_id` 和 `registration_access_token`：

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

`token_endpoint_auth_method: none` 是运行在用户设备上的 MCP 客户端的正确默认值。它们只获得 `client_id`——没有可泄露的 `client_secret`。PKCE 提供公共客户端所需的持有证明。

三个生产陷阱：

- 注册端点必须按源 IP 限流。否则恶意参与者脚本化数百万假注册耗尽 `client_id` 命名空间。
- 某些企业 IdP 要求 `software_statement`（为客户端担保的签名 JWT）。
- `registration_access_token` 必须存储为哈希，而非明文。此 token 的盗窃意味着攻击者可以重写客户端的重定向 URI。

### RFC 8707（回顾）— 资源指示器

第 16 课建立了形状。生产规则：每个 token 请求包含 `resource=<canonical-mcp-url>`，MCP 服务器在每个调用上验证 `token.aud` 与自身资源 URL 匹配。

### RFC 7636（回顾）— PKCE

PKCE 在 OAuth 2.1 中是强制的。本课的授权码流程始终携带 `code_challenge` 和 `code_verifier`。服务器拒绝没有验证器或验证器哈希与存储挑战不匹配的 token 请求。

### MCP 规范 2025-11-25 认证配置

MCP 规范（2025-11-25）对 MCP 服务器的授权层必须做什么有精确要求：

- 发布 `/.well-known/oauth-protected-resource`（RFC 9728）。
- 只通过 `Authorization: Bearer ...` 接受 token。
- 验证每个请求的 `aud`、`iss`、`exp` 和所需范围。
- 对每个 401 和 403 以携带 `Bearer error=...` 的 `WWW-Authenticate` 响应。
- 拒绝 `aud` 不匹配规范资源的 token。
- 拒绝 `iss` 不在受保护资源元数据的 `authorization_servers` 列表中的 token。

### IdP 能力矩阵

并非每个 IdP 都支持完整的 MCP 配置。

| IdP 类别 | RFC 8414 元数据 | RFC 7591 DCR | RFC 8707 资源 | RFC 7636 S256 PKCE | 备注 |
|---|---|---|---|---|---|
| 自托管（Keycloak） | 是 | 是 | 是（24.x 起） | 是 | 本课 MCP 配置的参考 IdP；端到端支持每个 RFC。 |
| 企业 SSO（Microsoft Entra ID） | 是 | 是（高级层） | 是 | 是 | DCR 可用性因租户层而异；在目标租户中部署前验证。 |
| 企业 SSO（Okta） | 是 | 是（Okta CIC / Auth0） | 是 | 是 | DCR 在 Auth0（现 Okta CIC）上可用；经典 Okta 组织需要管理员预注册。 |
| 社交登录 IdP（通用） | 不定 | 很少 | 很少 | 是 | 大多数社交 IdP 将客户端视为静态合作伙伴；不依赖 DCR。仅用作身份源，在其上层构建自己的 MCP 感知授权服务器。 |
| 自定义/自建 | 取决 | 取决 | 取决 | 取决 | 如果自建，请提供完整配置。跳过上述四个 RFC 中的任何一个会破坏 MCP 认证契约。 |

### JWKS 轮换模式与 iii

生产故障模式是过期 JWKS 缓存。用 cron触发器和 `state::*` 缓存解决：

```python
iii.registerTrigger(
    "cron",
    {"schedule": "0 */6 * * *", "name": "auth::jwks-refresh"},
    "auth::rotate-jwks",
)
```

每 6 小时，cron 触发器调用 `auth::rotate-jwks`，获取 `<issuer>/.well-known/jwks.json` 并写入 `state::set("auth/jwks/<issuer>", {keys, fetched_at})`。验证器从 `state::get` 读取。`kid` 不在缓存中的 token 触发同步 `auth::rotate-jwks` 调用作为回退。

两个密钥同时存在是稳态。授权服务器通过在退休前引入下一个密钥来轮换，因此旧密钥签发的 token 在过期前仍然有效。

### iii 原语连接

五个原语组成认证面：

```python
# 1. RFC 8414 元数据文档 HTTP 触发器
iii.registerTrigger("http", {"path": "/.well-known/oauth-authorization-server", "method": "GET"}, "auth::serve-asm")
# 2. RFC 7591 DCR HTTP 触发器
iii.registerTrigger("http", {"path": "/register", "method": "POST"}, "auth::register-client")
# 3. JWT 验证可调用函数
iii.registerFunction("auth::validate-jwt", validate_jwt_handler)
# 4. SEP-835 逐步授权
iii.registerFunction("auth::issue-step-up", issue_step_up_handler)
# 5. cron 驱动的 JWKS 轮换
iii.registerTrigger("cron", {"schedule": "0 */6 * * *"}, "auth::rotate-jwks")
iii.registerFunction("auth::rotate-jwks", rotate_jwks_handler)
```

MCP 服务器本身从不直接调用验证：

```python
result = iii.trigger("auth::validate-jwt", {"token": bearer_token, "resource": self.resource})
if not result["valid"]:
    return {"status": 401, "WWW-Authenticate": result["www_authenticate"]}
```

这种间接性是 iii 的赌注。明天你把验证器换成向两个 IdP 并行查询的扇出，或添加 span 发射器，或缓存正面验证。MCP 服务器不变。

### 混淆代理演练

服务器 A（`notes.example.com`）和服务器 B（`tasks.example.com`）都注册到同一授权服务器。服务器 A 被攻陷。攻击者拿到用户的 notes token 并重放到服务器 B。

服务器 B 的验证器：

1. 解码 JWT，按 `kid` 获取 JWKS，验证签名。
2. 检查 `iss` 与受保护资源元数据的 `authorization_servers`。（通过——同一 IdP。）
3. 检查 `aud == "https://tasks.example.com"`。（失败——token 的 `aud` 是 `https://notes.example.com`。）
4. 返回 401 和 `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch"`。

受众声明是协议层防御此攻击的唯一手段。为性能跳过它是最常见的生产错误；验证器必须在每个请求上运行，而非仅在会话开始时。

### 故障模式

- **过期 JWKS。** 验证器在密钥轮换后拒绝有效 token。修复是 cron+回退模式。永远不要缓存 JWKS 而没有刷新任务。
- **缺失 `aud` 声明。** 一些 IdP 默认省略 `aud`，除非 token 请求中有 `resource`。验证器必须拒绝缺失 `aud` 的 token，而非将缺失视为通配符。
- **范围升级竞态。** 同一用户两个并发逐步升级流程都可以成功并产生两个不同范围的 access token。验证器必须使用请求中呈现的 token，而非查找"用户当前范围"——这会产生 TOCTOU 窗口。
- **注册令牌盗窃。** 泄露的 `registration_access_token` 让攻击者重写重定向 URI。静态存储哈希；要求客户端在每次更新时呈现明文；怀疑时轮换。
- **`iss` 未锁定。** 接受任何 `iss` 的验证器让攻击者自建授权服务器，注册目标受众的客户端并签发 token。受保护资源元数据的 `authorization_servers` 列表是白名单；强制执行它。

## 用框架实现

`code/main.py` 用标准库 Python 和小型 `iii_mock` 注册表演示完整的生产流程：授权服务器发布 RFC 8414 元数据 -> 客户端发现注册端点 -> DCR 注册获得 client_id -> PKCE 授权码流程 -> Bearer token 调用工具 -> JWT 验证读取 JWKS 缓存 -> cron 触发 JWKS 轮换 -> 新密钥验证通过 -> 混淆代理尝试返回 401。

模拟 JWT 使用 HS256 和共享密钥（使课程仅用标准库运行）。生产使用 RS256 或 EdDSA 和上述 JWKS 模式；验证逻辑在其他方面完全相同。

## 产出物

本课产生 `outputs/skill-mcp-auth-iii.md`。给定 MCP 服务器配置和 IdP 能力集，该技能生成 iii 原语注册方案、JWKS 轮换计划、范围映射和 IdP 不满足 RFC 配置时的拒绝规则。

## 练习题

1. 运行 `code/main.py`。追踪 9 步流程。注意 `state::get` 在 `auth::rotate-jwks` 覆盖它之前立即返回过期数据，以及下一个请求如何现在用新密钥验证。

2. 向受保护资源元数据的 `authorization_servers` 列表添加新 IdP。签发由新 IdP 签名的 token 并确认验证器接受。签发由未列出 IdP 签名的 token 并确认验证器以 `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"` 拒绝。

3. 将 `auth::rate-limit` 实现为 iii 函数并从注册 HTTP 触发器内部在注册器运行前调用它。使用 `state::set("auth/ratelimit/<ip>", ...)` 持有的每源 IP 令牌桶。

4. 阅读 RFC 7591 并识别本课 `/register` 处理器未验证的两个字段。添加验证。（提示：`software_statement` 和 `redirect_uris` URI 方案。）

5. 阅读 MCP 规范 2025-11-25 认证部分。找到本课验证器当前未发出的 `WWW-Authenticate` 头上的一个规范性要求。添加它。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| ASM | "OAuth 元数据文档" | RFC 8414 `/.well-known/oauth-authorization-server` JSON | Authorization Server Metadata |
| DCR | "自助客户端注册" | RFC 7591 `POST /register` 流程 | Dynamic Client Registration |
| JWKS | "JWT 验证公钥" | 从 `jwks_uri` 获取的 JSON Web Key Set，按 `kid` 索引 | JSON Web Key Set |
| 资源指示器 | "受众参数" | RFC 8707 `resource` 参数将 token 绑定到单个服务器 | Resource indicator |
| `aud` 声明 | "受众" | 验证器与规范资源 URL 比对的 JWT 声明 | `aud` claim |
| 混淆代理 | "token 重放" | 为服务器 A 签发的 token 被呈现给服务器 B 的攻击 | Confused deputy |
| 签发者白名单 | "受信授权服务器" | 受保护资源元数据的 `authorization_servers` 中命名的集合 | `iss` allow-list |
| 密钥轮换 | "滚动 JWKS" | 带重叠窗口的签名密钥周期性替换 | Key rotation |
| 公共客户端 | "原生或浏览器客户端" | 无 `client_secret` 的 OAuth 客户端；PKCE 补偿 | Public client |
| `WWW-Authenticate` | "401/403 响应头" | 携带 `Bearer error=...` 指令驱动客户端恢复 | WWW-Authenticate |

## 延伸阅读

- [MCP — Authorization spec (2025-11-25)](https://modelcontextprotocol.io/specification/draft/basic/authorization) — 本课实现的 MCP 认证配置
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) — 发现契约
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591) — DCR
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636) — 公共客户端持有证明
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — 受众绑定
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) — 资源服务器发现
- [OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) — 合并的 OAuth 基础
