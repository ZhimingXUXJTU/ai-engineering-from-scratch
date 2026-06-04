# MCP 安全 II — OAuth 2.1、资源指示器与增量授权

> 远程 MCP 服务器需要授权（不只是认证）。2025-11-25 规范对齐 OAuth 2.1 + PKCE + 资源指示器（RFC 8707）+ 受保护资源元数据（RFC 9728）。SEP-835 增加了增量授权范围的逐步同意机制。本课将逐步授权流程实现为状态机，展示每一个步骤。

> **【中文解读】** 远程 MCP 服务器需要授权（不只是认证）。2025-11-25 规范对齐 OAuth 2.1 + PKCE + 资源指示器（RFC 8707）+ 受保护资源元数据（RFC 9728）。SEP-835 增加了增量授权范围的逐步同意机制。本课将逐步授权流程实现为状态机，展示每一个步骤。

> **【拓展】** OAuth 2.1 是 MCP 远程服务器的标准认证方案。与早期 OAuth 2.0 相比，2.1 强制 PKCE、禁止隐式流程。资源指示器（RFC 8707）将 token 绑定到特定服务器，防止"混淆代理"攻击。逐步授权（Step-up）允许按需请求更多权限，而非一次性获取全部——这是最小权限原则的实践。

**类型：** 构建
**语言：** Python（标准库，OAuth 状态机模拟器）
**前置条件：** Phase 13 · 09（传输层），Phase 13 · 15（安全 I）
**时间：** 约 75 分钟

## 学习目标

- 区分资源服务器和授权服务器的职责。
- 走通 PKCE 保护的 OAuth 2.1 授权码流程。
- 使用 `resource`（RFC 8707）和受保护资源元数据（RFC 9728）防止混淆代理攻击。
- 实现逐步授权：服务器以 403 + WWW-Authenticate 响应要求更高范围；客户端重新提示用户同意并重试。

## 问题引入

早期 MCP（2025年之前）的远程服务器使用临时 API Key 甚至无认证。2025-11-25 规范通过完整 OAuth 2.1 配置关闭了这一差距。

三个实际需求：

- **普通远程服务器。** 用户安装访问 Notion / GitHub / Gmail 的远程 MCP 服务器。OAuth 2.1 + PKCE 是正确的形状。
- **范围升级。** 授予 `notes:read` 的笔记服务器之后可能需要 `notes:write`。逐步授权（SEP-835）请求额外范围，而非重做整个流程。
- **混淆代理防御。** 客户端持有针对服务器 A 的 audience-scoped token。服务器 A 被攻陷并尝试向服务器 B 出示该 token。资源指示器（RFC 8707）将 token 绑定到其预期受众。

OAuth 2.1 不是新的。新的是 MCP 的配置：特定要求的流程（仅授权码 + PKCE；无隐式、默认无客户端凭证），每次 token 请求强制资源指示器，以及发布的受保护资源元数据让客户端知道去哪里。

## 核心概念

### 角色

- **客户端（Client）。** MCP 客户端（Claude Desktop、Cursor 等）。
- **资源服务器（Resource Server）。** MCP 服务器（notes、GitHub、Postgres 等）。
- **授权服务器（Authorization Server）。** 签发 token。可以与资源服务器是同一服务或独立的 IdP（Auth0、Keycloak、Cognito）。

### 授权码 + PKCE

流程：

1. 客户端生成 `code_verifier`（随机）和 `code_challenge`（SHA256）。
2. 客户端重定向用户到 `/authorize?response_type=code&client_id=...&redirect_uri=...&scope=notes:read&code_challenge=...&resource=https://notes.example.com`。
3. 用户同意。授权服务器重定向到 `redirect_uri?code=...`。
4. 客户端 POST 到 `/token?grant_type=authorization_code&code=...&code_verifier=...&resource=...`。
5. 授权服务器验证验证器的哈希与存储的挑战匹配并签发 access token。
6. 客户端使用 token：对资源服务器的每个请求附带 `Authorization: Bearer ...`。

PKCE 防止授权码拦截攻击。资源指示器防止 token 在其他地方有效。

### 受保护资源元数据（RFC 9728）

资源服务器发布 `.well-known/oauth-protected-resource` 文档：

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:read", "notes:write", "notes:delete"]
}
```

客户端从资源服务器发现授权服务器。减少配置——客户端只需要资源 URL。

### 资源指示器（RFC 8707）

token 请求中的 `resource` 参数将 token 绑定到目标受众。签发的 token 包含 `aud: "https://notes.example.com"`，其他 MCP 服务器检查 `aud` 并拒绝不匹配的 token。

### 范围模型

范围是空格分隔的字符串。常见 MCP 约定：

- `notes:read`、`notes:write`、`notes:delete`
- `admin:*` 用于管理员能力（谨慎使用）
- `profile:read` 用于身份

范围选择应遵循最小权限：请求现在需要的，需要更多时逐步升级。

### 逐步授权（SEP-835）

用户授予 `notes:read`。之后要求 Agent 删除笔记。服务器响应：

```
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
    scope="notes:delete", resource="https://notes.example.com"
```

客户端看到 insufficient_scope 错误，弹出同意对话框获取额外范围，执行迷你 OAuth 流程，用新 token 重试请求。

### Token 受众验证

每个请求：服务器检查 `token.aud == self.resource_url`。不匹配 = 401。这阻止跨服务器 token 重用。

### 短期 token 和轮换

Access token 应该短期（默认 1 小时）。Refresh token 在每次刷新时轮换。客户端在后台处理静默刷新。

### 禁止 token 透传

采样服务器（Phase 13 · 11）不得将客户端的 token 透传给其他服务。采样请求是边界。

### 混淆代理防御

Token 绑定到 `aud`。客户端绑定到 `client_id`。每个请求对两者都验证。规范明确禁止了 MCP 前远程工具生态中常见的旧"传递 token"模式。

### 客户端 ID 发现

每个 MCP 客户端在固定 URL 发布其元数据。授权服务器可以获取客户端的元数据文档来发现重定向 URI 和联系信息。这消除了手动客户端注册。

### 网关和 OAuth

Phase 13 · 17 展示企业网关如何处理 OAuth：网关持有上游服务器的凭证，给客户端的 token 是网关签发的，上游 token 永远不离开网关。这翻转了信任模型——用户与网关认证一次；网关处理 N 个服务器授权。

## 用框架实现

`code/main.py` 将完整的 OAuth 2.1 逐步授权流程模拟为内存中的状态机。它实现了：

- PKCE code-verifier / challenge 生成。
- 带资源指示器的授权码流程。
- 受保护资源元数据端点。
- 带受众检查的 token 验证。
- `insufficient_scope` 上的逐步升级。

本课无 HTTP 服务器；状态机在内存中运行，便于追踪每一步。Phase 13 · 17 的网关课程将其连接到实际传输。

## 产出物

本课产生 `outputs/skill-oauth-scope-planner.md`。给定一个带有工具的远程 MCP 服务器，该技能设计范围集合、锁定规则和逐步授权策略。

## 练习题

1. 运行 `code/main.py`。追踪两范围逐步授权流程。注意逐步升级时哪些步骤重复。

2. 添加 refresh-token 轮换：每次刷新签发新 refresh token 并使旧的失效。模拟轮换后使用被盗 refresh token 并确认失败。

3. 使用标准库 http.server 将受保护资源元数据端点实现为真实 HTTP 响应。镜像第 09 课的 `/mcp` 端点。

4. 为 GitHub MCP 服务器设计范围层级：读仓库、写 PR、审批 PR、合并 PR、管理员。在每个级别之间使用逐步升级。

5. 阅读 RFC 8707 和 RFC 9728。识别 9728 中 MCP 使用方式与 RFC 示例不同的一个字段。（提示：与 `scopes_supported` 相关。）

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| OAuth 2.1 | "现代 OAuth" | 强制 PKCE 并禁止隐式流程的合并 RFC | OAuth 2.1 |
| PKCE | "持有证明" | code verifier + challenge 防止授权码拦截 | Proof Key for Code Exchange |
| 资源指示器 | "token 受众" | RFC 8707 `resource` 参数将 token 绑定到单个服务器 | Resource indicator |
| 受保护资源元数据 | "发现文档" | RFC 9728 `.well-known/oauth-protected-resource` | Protected-resource metadata |
| 逐步授权 | "增量同意" | SEP-835 按需增加范围的流程 | Step-up authorization |
| 权限不足信号 | "带 WWW-Authenticate 的 403" | 服务器触发重新授权更大范围的信号 | `insufficient_scope` |
| 混淆代理 | "跨服务 token 重放" | 受信持有者不适当地转发 token 的攻击 | Confused deputy |
| 短期 token | "access token TTL" | 快速过期的 Bearer；refresh token 续期 | Short-lived token |
| 范围层级 | "最小权限堆栈" | 带逐步升级的渐进范围集 | Scope hierarchy |
| 客户端 ID 元数据 | "客户端发现文档" | 客户端发布自己 OAuth 元数据的 URL | Client ID metadata |

## 延伸阅读

- [MCP — Authorization spec](https://modelcontextprotocol.io/specification/draft/basic/authorization) — 权威 MCP OAuth 配置
- [den.dev — MCP November authorization spec](https://den.dev/blog/mcp-november-authorization-spec/) — 2025-11-25 变更演练
- [RFC 8707 — Resource indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — 受众绑定 RFC
- [RFC 9728 — OAuth 2.0 protected resource metadata](https://datatracker.ietf.org/doc/html/rfc9728) — 发现文档 RFC
- [Aembit — MCP OAuth 2.1, PKCE and the future of AI authorization](https://aembit.io/blog/mcp-oauth-2-1-pkce-and-the-future-of-ai-authorization/) — 实践中的逐步授权流程演练
