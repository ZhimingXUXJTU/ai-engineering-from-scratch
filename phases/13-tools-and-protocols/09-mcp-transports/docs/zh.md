# MCP 传输层 — stdio 与 Streamable HTTP

> stdio 只能在本地工作。Streamable HTTP (2025-03-26) 是远程标准。旧的 HTTP+SSE 传输已被弃用，将在 2026 年中期移除。选错传输层意味着一次迁移；选对则获得一个可远程部署的 MCP 服务器，具备会话连续性和 DNS 重绑定防护。

> **【中文解读】** stdio 只能在本地工作。Streamable HTTP (2025-03-26) 是远程标准。旧的 HTTP+SSE 传输已被弃用，将在 2026 年中期移除。选错传输层意味着一次迁移；选对则获得一个可远程部署的 MCP 服务器，具备会话连续性和 DNS 重绑定防护。

> **【拓展：传输层→Claude 远程 MCP】** Claude Desktop 使用 stdio 传输与本地 MCP 服务器通信。对于远程 MCP 服务器（如部署在 Cloudflare Workers 上），使用 Streamable HTTP 传输。Streamable HTTP 的单端点模式（`/mcp`）简化了部署，`Mcp-Session-Id` 头确保会话连续性，`Origin` 验证防止 DNS 重绑定攻击。

**类型：** 学习
**语言：** Python（标准库，Streamable HTTP 端点骨架）
**前置条件：** Phase 13 · 07, 08（MCP 服务器和客户端）
**时间：** 约 45 分钟

## 学习目标

- 根据部署形态（本地 vs 远程，单进程 vs 集群）在 stdio 和 Streamable HTTP 之间做出选择。
- 实现 Streamable HTTP 单端点模式：POST 用于请求，GET 用于会话流。
- 强制执行 `Origin` 验证和 session-id 语义以防御 DNS 重绑定。
- 在 2026 年中期移除截止日期之前将旧的 HTTP+SSE 服务器迁移到 Streamable HTTP。

## 问题引入

MCP 的第一个远程传输（2024-11）是 HTTP+SSE：两个端点，一个用于客户端的 POST，一个 Server-Sent-Events 通道用于服务器到客户端的流。它可以工作，但也笨拙：每个会话两个端点、在某些 CDN 前面的缓存问题、以及对一些 WAF 激进终止的长连接 SSE 的硬依赖。

2025-03-26 规范用 Streamable HTTP 替代了它：一个端点，POST 用于客户端请求，GET 用于建立会话流，两者共享一个 `Mcp-Session-Id` 头。此后构建或迁移的每个服务器都使用 Streamable HTTP。旧的 SSE 模式正在被弃用——Atlassian Rovo 于 2026 年 6 月 30 日移除；Keboola 于 2026 年 4 月 1 日移除；大多数剩余企业服务器将在 2026 年底前移除。

Stdio 对本地服务器仍然重要。Claude Desktop、VS Code 和每个 IDE 形状的客户端通过 stdio 生成服务器。正确的心智模型：stdio 用于"本机"，Streamable HTTP 用于"网络"。没有交叉。

## 核心概念

### stdio

- 子进程传输。客户端生成服务器，通过 stdin/stdout 通信。
- 每行一个 JSON 对象。换行分隔。
- 无会话 ID；进程身份就是会话。
- 无需认证（子进程继承父进程的信任边界）。
- 不要用于远程服务器——你需要 SSH 或 socat 来隧道，此时应该用 Streamable HTTP。

### Streamable HTTP

单端点 `/mcp`（或任何路径）。支持三种 HTTP 方法：

- **POST /mcp。** 客户端发送 JSON-RPC 消息。服务器用单个 JSON 响应或一个 SSE 流的多个响应回复（用于批量响应和与该请求相关的通知）。
- **GET /mcp。** 客户端打开长连接 SSE 通道。服务器用它进行服务器到客户端的请求（sampling、notifications、elicitation）。
- **DELETE /mcp。** 客户端显式终止会话。

会话由服务器在第一次响应时设置的 `Mcp-Session-Id` 头标识，客户端在每个后续请求中回显。Session ID 必须是密码学随机的（128+ 位）；客户端自行选择的 ID 会被拒绝。

### `Origin` 验证和 DNS 重绑定

浏览器不是 MCP 客户端（目前），但攻击者可以构造一个网页让浏览器 POST 到 `localhost:1234/mcp`——用户本地 MCP 服务器监听的地方。如果服务器不检查 `Origin`，浏览器的同源策略不会保护它，因为 `Origin: http://evil.com` 是有效的跨域。

2025-11-25 规范要求服务器拒绝 `Origin` 不在白名单上的请求。白名单通常包含 MCP 客户端主机（`https://claude.ai`、`vscode-webview://*`）和本地 UI 的 localhost 变体。

### 会话 ID 生命周期

1. 客户端发送不带 `Mcp-Session-Id` 的第一个请求。
2. 服务器分配随机 ID，在响应头中设置 `Mcp-Session-Id`。
3. 客户端在所有后续请求和 `GET /mcp` 流中回显该头。
4. 服务器可以撤销会话；客户端在后续请求上看到 404，必须重新握手。
5. 客户端可以显式 DELETE 会话进行干净关闭。

### Keepalive 和重连

SSE 连接会断开。客户端用相同的 `Mcp-Session-Id` 重新 GET 来重建连接。服务器必须排队断开期间错过的事件（在合理窗口内）并通过客户端回显的 `last-event-id` 头重放。

Phase 13 · 13 覆盖 Tasks，使长时间运行的工作即使在完整会话重连后也能存活。

### 向后兼容探测

想要同时支持新旧服务器的客户端：

1. POST 到 `/mcp`。
2. 如果响应是 `200 OK` 带 JSON 或 SSE，这是 Streamable HTTP。
3. 如果响应是 `200 OK` 带 `Content-Type: text/event-stream` 且有指向辅助端点的 `Location` 头，这是旧的 HTTP+SSE；跟随 `Location`。

### Cloudflare、ngrok 和托管

2026 年生产级远程 MCP 服务器运行在 Cloudflare Workers（使用其 MCP Agents SDK）、Vercel Functions 或容器化的 Node/Python 上。关键：你的托管必须支持长连接 HTTP 用于 SSE GET。Vercel 免费层限制 10 秒不适合。Cloudflare Workers 支持无限时长流。

### 网关组合

当你用网关（Phase 13 · 17）前置多个 MCP 服务器时，网关是一个单一的 Streamable HTTP 端点，重写 session ID 并多路复用上游。工具在网关层合并；客户端看到单个逻辑服务器。

### 传输失败模式

- **stdio SIGPIPE。** 子进程中途死亡引发 SIGPIPE；服务器应干净退出。客户端应检测 EOF 并标记会话死亡。
- **HTTP 502 / 504。** Cloudflare、nginx 和其他代理在上游故障时发出这些。Streamable HTTP 客户端应在短暂退避后重试一次。
- **SSE 连接断开。** TCP RST、代理超时或客户端网络变化关闭流。客户端用 `Mcp-Session-Id` 和可选的 `last-event-id` 重连恢复。
- **会话撤销。** 服务器使 session ID 失效；客户端在下次请求时看到 404。必须重新握手。
- **时钟偏移。** 客户端上的资源 TTL 计算与服务器偏离。客户端应以服务器时间戳为准。

### 何时绕过 Streamable HTTP

一些企业在自己的网络内部署 MCP 服务器，使用 gRPC 或消息队列传输。这是非标准的——MCP 规范没有正式定义这些。网关可以暴露 Streamable HTTP 表面给 MCP 客户端，同时内部使用 gRPC。保持外部表面符合规范；网关负责翻译。

## 用框架实现

`code/main.py` 使用 `http.server`（标准库）实现了一个最小的 Streamable HTTP 端点。它处理 `/mcp` 上的 POST、GET 和 DELETE，在第一次响应时设置 `Mcp-Session-Id`，验证 `Origin`，并拒绝来自非白名单来源的请求。处理器复用了第 07 课笔记服务器的分发逻辑。

关注点：

- POST 处理器读取 JSON-RPC 请求体，分发，并写入 JSON 响应（单响应变体；SSE 变体在结构上类似）。
- `Origin` 检查拒绝默认的 `http://evil.example` 探测但接受 `http://localhost`。
- Session ID 是随机的 128 位十六进制字符串；服务器在内存中保持每会话状态。

## 产出物

本课产生 `outputs/skill-mcp-transport-migrator.md`。给定一个 HTTP+SSE（旧版）MCP 服务器，该技能生成迁移到 Streamable HTTP 的计划，包含 session-id 连续性、Origin 检查和向后兼容探测支持。

## 练习题

1. 运行 `code/main.py`。用 `curl` POST 一个 `initialize` 并观察 `Mcp-Session-Id` 响应头。POST 第二个请求回显该头并验证会话连续性。

2. 添加一个打开 SSE 流的 GET 处理器。每五秒发送一个 `notifications/progress` 事件。用相同的 session ID 重新 GET 并确认服务器接受。

3. 实现 `last-event-id` 重放逻辑。重连时重放自该 ID 以来生成的所有事件。

4. 扩展 `Origin` 验证以支持通配符模式（`https://*.example.com`），确认它接受 `https://app.example.com` 但拒绝 `https://evil.example.com.attacker.net`。

5. 从官方注册中心取一个旧的 HTTP+SSE 服务器并勾画迁移：端点处理、session ID 生成和头语义有什么变化。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| stdio 传输 | "本地子进程" | 通过 stdin/stdout 的 JSON-RPC，换行分隔 | stdio transport |
| Streamable HTTP | "远程传输" | 单端点 POST + GET + 可选 SSE，2025-03-26 规范 | Streamable HTTP |
| HTTP+SSE | "旧版" | 2026 年中期移除的双端点模型 | HTTP+SSE (deprecated) |
| `Mcp-Session-Id` | "会话头" | 服务器分配的在每个后续请求中回显的随机 ID | Session header |
| `Origin` 白名单 | "DNS 重绑定防御" | 拒绝来源未经批准的请求 | Origin allowlist |
| 单端点模式 | "一个 URL" | `/mcp` 处理所有会话操作的 POST / GET / DELETE | Single endpoint |
| `last-event-id` | "SSE 重放" | 用于恢复断开流而不丢失事件的头 | SSE replay id |
| 向后兼容探测 | "新旧检测" | 自动选择传输的客户端响应形状检查 | Backwards-compat probe |
| 长连接 HTTP | "SSE 流" | 服务器在一个 TCP 连接上推送事件数分钟或数小时 | Long-lived HTTP |
| 会话撤销 | "强制重新初始化" | 服务器使 session ID 失效；客户端必须重新握手 | Session revocation |

## 延伸阅读

- [MCP — Basic transports spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) — stdio 和 Streamable HTTP 的权威参考
- [MCP — Basic transports spec 2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) — 引入 Streamable HTTP 的修订版
- [Cloudflare — MCP transport](https://developers.cloudflare.com/agents/model-context-protocol/transport/) — Workers 托管的 Streamable HTTP 模式
- [AWS — MCP transport mechanisms](https://builder.aws.com/content/35A0IphCeLvYzly9Sw40G1dVNzc/mcp-transport-mechanisms-stdio-vs-streamable-http) — 跨部署形态的比较
- [Atlassian — HTTP+SSE deprecation notice](https://community.atlassian.com/forums/Atlassian-Remote-MCP-Server/HTTP-SSE-Deprecation-Notice/ba-p/3205484) — 具体的迁移截止日期示例
