# MCP Transports — stdio vs Streamable HTTP vs SSE Migration | MCP 传输层：stdio 与 Streamable HTTP

> stdio works locally and nowhere else. Streamable HTTP (2025-03-26) is the remote standard. The old HTTP+SSE transport is deprecated and being removed in mid-2026. Picking the wrong transport costs a migration; picking the right one buys a remote-hostable MCP server with session continuity and DNS-rebinding protection.

> **【中文解读】** stdio 只能在本地工作。Streamable HTTP (2025-03-26) 是远程标准。旧的 HTTP+SSE 传输已被弃用，将在 2026 年中期移除。选错传输层意味着一次迁移；选对则获得一个可远程部署的 MCP 服务器，具备会话连续性和 DNS 重绑定防护。

> **【拓展：传输层→Claude 远程 MCP】** Claude Desktop 使用 stdio 传输与本地 MCP 服务器通信。对于远程 MCP 服务器（如部署在 Cloudflare Workers 上），使用 Streamable HTTP 传输。Streamable HTTP 的单端点模式（`/mcp`）简化了部署，`Mcp-Session-Id` 头确保会话连续性，`Origin` 验证防止 DNS 重绑定攻击。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07、08（MCP server 和 client）——理解 stdio 通信细节；(2) HTTP 协议基础（method、header、SSE）；(3) DNS 重绑定攻击概念——本节会讲防御；(4) 至少部署过一个 web 服务，理解 CORS/Origin 校验。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, Streamable HTTP endpoint skeleton) | **语言:** Python (stdlib, Streamable HTTP endpoint skeleton)
**Prerequisites:** Phase 13 · 07, 08 (MCP server and client) | **前置知识:** Phase 13 · 07, 08 (MCP server and client)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Pick between stdio and Streamable HTTP based on deployment shape (local vs remote, single-process vs fleet).
  中文翻译：根据部署形态（本地 vs 远程、单进程 vs 集群）在 stdio 和 Streamable HTTP 之间选择。
- Implement the Streamable HTTP single-endpoint pattern: POST for requests, GET for session stream.
  中文翻译：实现 Streamable HTTP 单端点模式：POST 用于请求、GET 用于会话流。
- Enforce `Origin` validation and session-id semantics to defeat DNS-rebinding.
  中文翻译：强制执行 `Origin` 验证和 session-id 语义以抵御 DNS 重绑定攻击。
- Migrate a legacy HTTP+SSE server to Streamable HTTP before the mid-2026 removal deadlines.
  中文翻译：在 2026 年中期移除截止前将遗留 HTTP+SSE 服务器迁移到 Streamable HTTP。

## The Problem | 问题引入

> **【中文解读】** MCP 的两种传输模式：(1) stdio——本地服务器，客户端作为子进程启动，通过 stdin/stdout 通信；(2) Streamable HTTP——远程服务器，单端点 `/mcp`，用 `Mcp-Session-Id` 管理会话。2025-03-26 规范用 Streamable HTTP 替代了旧的 HTTP+SSE 双端点模式。stdio 适用于"本机"，Streamable HTTP 适用于"网络"。

The first MCP remote transport (2024-11) was HTTP+SSE: two endpoints, one for the client's POSTs and one Server-Sent-Events channel for the server-to-client stream. It worked. It was also clumsy: two endpoints per session, broken caches in front of some CDNs, and a hard dependency on long-lived SSE connections that some WAFs terminate aggressively.

> 首个 MCP 远程传输（2024-11）是 HTTP+SSE：两个端点，一个用于客户端的 POST，一个 Server-Sent-Events 通道用于服务器到客户端流。它能工作。但也很笨拙：每会话两个端点、某些 CDN 前的缓存损坏、对长连接 SSE 的硬依赖（某些 WAF 会激进终止）。

The 2025-03-26 spec replaced it with Streamable HTTP: one endpoint, POST for client requests, GET for establishing a session stream, both sharing a `Mcp-Session-Id` header. Every server built or migrated since then uses Streamable HTTP. The old SSE mode is being deprecated — Atlassian Rovo removed it June 30, 2026; Keboola April 1, 2026; most remaining enterprise servers by end of 2026.

> 2025-03-26 规范用 Streamable HTTP 替代它：单端点、POST 用于客户端请求、GET 用于建立会话流，两者共享 `Mcp-Session-Id` 头。自此以后构建或迁移的每个服务器都使用 Streamable HTTP。旧的 SSE 模式正在被弃用——Atlassian Rovo 2026 年 6 月 30 日移除；Keboola 2026 年 4 月 1 日；大多数剩余企业服务器在 2026 年底前。

And stdio still matters for local servers. Claude Desktop, VS Code, and every IDE-shaped client spawn servers via stdio. The right mental model: stdio for "this machine", Streamable HTTP for "over the network". No cross-over.

> stdio 对本地服务器仍很重要。Claude Desktop、VS Code 和每个 IDE 形态的客户端都通过 stdio 生成服务器。正确的心智模型：stdio 用于"本机"、Streamable HTTP 用于"网络"。无交叉。

> 💡 **【类比】** stdio vs Streamable HTTP 像"打电话给楼下便利店" vs "打电话给国外分公司"。楼下便利店（本地服务器）：你直接喊一嗓子（stdin/stdout），声音在屋子里传，不用拨号、不用付费、没有窃听风险。国外分公司（远程服务器）：必须走电话网（HTTP），要拨分机号（端点）、要确认对方是分公司不是骗子（Origin 验证）、要保持通话不掉线（session-id）。两种通信方式各有适用场景，不能混用。

## The Concept | 核心概念

### stdio

- Child-process transport. Client spawns server, communicates via stdin/stdout.
  中文翻译：子进程传输。客户端生成服务器，通过 stdin/stdout 通信。
- One JSON object per line. Newline-delimited.
  中文翻译：每行一个 JSON 对象。换行分隔。
- No session id; process identity is the session.
  中文翻译：无 session id；进程身份即 session。
- No auth needed (the child inherits the parent's trust boundary).
  中文翻译：无需认证（子进程继承父进程的信任边界）。
- Never use for remote servers — you would need SSH or socat to tunnel, at which point use Streamable HTTP.
  中文翻译：绝不要用于远程服务器——你需要 SSH 或 socat 隧道，那种情况直接用 Streamable HTTP。

### Streamable HTTP

> **【拓展：Streamable HTTP 相比 SSE 的改进】** Streamable HTTP 相比旧的双端点 SSE 模式有三个改进：(1) 单端点简化了部署和 CDN 配置；(2) `Mcp-Session-Id` 头提供可靠的会话管理；(3) 支持 POST 返回单响应或 SSE 流，更灵活。大多数 MCP 服务器（包括 Atlassian Rovo、Keboola）已在 2026 年完成迁移。

Single endpoint `/mcp` (or any path). Supports three HTTP methods:

> 单端点 `/mcp`（或任何路径）。支持三种 HTTP 方法：

- **POST /mcp.** Client sends a JSON-RPC message. Server replies with either a single JSON response, or an SSE stream of one-or-more responses (useful for batched responses and notifications related to that request).
  中文翻译：**POST /mcp。** 客户端发送 JSON-RPC 消息。服务器回复单个 JSON 响应，或一个或多个响应的 SSE 流（用于批量响应和与该请求相关的通知）。
- **GET /mcp.** Client opens a long-lived SSE channel. Server uses it for server-to-client requests (sampling, notifications, elicitation).
  中文翻译：**GET /mcp。** 客户端打开长连接 SSE 通道。服务器用它发送服务器到客户端的请求（sampling、通知、elicitation）。

> 🤔 **【困惑】** Q: 既然 stdio 简单又安全，为什么还要搞 Streamable HTTP？ A: 因为 stdio 强制"服务器必须和客户端在同一台机器"，这在三种场景下不可行：(1) **远程托管**——MCP server 在云端、Claude Desktop 在本地，必须走网络；(2) **多用户共享**——一个公司部署一个 GitHub MCP，所有员工共用，stdio 要每人起一个；(3) **沙盒隔离**——服务器要在容器里跑防止访问本机文件。Streamable HTTP 是远程协作的必需品。
- **DELETE /mcp.** Client explicitly terminates the session.
  中文翻译：**DELETE /mcp。** 客户端显式终止会话。

Sessions are identified by the `Mcp-Session-Id` header the server sets on the first response and the client echoes on every subsequent request. Session ids MUST be cryptographically random (128+ bits); client-chosen ids are rejected for safety.

> **【中文解读】** 会话由服务器在首次响应时设置的 `Mcp-Session-Id` 头标识。Session id 必须是密码学随机的（128+ 位）；客户端自行选择的 id 会被拒绝。`Origin` 验证防止 DNS 重绑定攻击——攻击者可构造网页让浏览器 POST 到 `localhost:1234/mcp`。

### Single endpoint vs two

Two-endpoint mode from the old spec is still callable in 2026 — the spec declares it "legacy compatible". But all new servers should be single-endpoint. The official SDKs emit single-endpoint; use the legacy mode only when talking to an unmigrated remote.

> 旧规范的双端点模式在 2026 年仍可调用——规范将其声明为"legacy compatible"。但所有新服务器都应是单端点。官方 SDK 发出单端点；仅在与未迁移的远程通信时使用 legacy 模式。

### `Origin` validation and DNS-rebinding

> **【拓展：DNS 重绑定攻击与 MCP 安全】** DNS 重绑定是一种攻击向量：攻击者构造网页让浏览器 POST 到 `localhost:1234/mcp`，如果 MCP 服务器不检查 `Origin` 头，就会执行恶意请求。2025-11-25 规范要求服务器拒绝不在白名单上的 `Origin`。白名单通常包含 MCP 客户端主机（`https://claude.ai`、`vscode-webview://*`）和 localhost 变体。

Browsers are not MCP clients (today), but an attacker can craft a webpage that convinces a browser to POST to `localhost:1234/mcp` — where the user's local MCP server listens. If the server does not check `Origin`, the browser's same-origin policy will not save it because `Origin: http://evil.com` is valid cross-origin.

> 浏览器（今天）不是 MCP 客户端，但攻击者可以构造一个网页让浏览器 POST 到 `localhost:1234/mcp`——用户本地 MCP 服务器监听的地方。如果服务器不检查 `Origin`，浏览器的同源策略救不了它，因为 `Origin: http://evil.com` 是有效的跨源。

The 2025-11-25 spec requires servers to reject requests whose `Origin` is not on an allowlist. The allowlist typically contains the MCP client host (`https://claude.ai`, `vscode-webview://*`) and localhost variants for local UIs.

> 2025-11-25 规范要求服务器拒绝 `Origin` 不在白名单上的请求。白名单通常包含 MCP 客户端宿主（`https://claude.ai`、`vscode-webview://*`）和本地 UI 的 localhost 变体。

> ⚠️ **【易错点】** 场景：Streamable HTTP server 忽略 `Origin` 校验 / 后果：DNS 重绑定攻击——攻击者把 evil.com 解析到 127.0.0.1，用户访问 evil.com 后浏览器 POST 到 localhost:3000/mcp，server 直接执行；用户完全无感 / 修复：(1) 服务端在所有请求入口校验 `Origin` 头是否在白名单；(2) localhost 调试模式必须要求 `Mcp-Session-Id` 才放行；(3) session-id 必须服务器生成（128 位以上随机），拒绝客户端自选 id。

### Session id lifecycle

1. Client sends first request without `Mcp-Session-Id`.
  中文翻译：客户端发送第一个请求时不带 `Mcp-Session-Id`。
2. Server assigns a random id, sets `Mcp-Session-Id` on the response header.
  中文翻译：服务器分配随机 id，在响应头设置 `Mcp-Session-Id`。
3. Client echoes that header on all subsequent requests and on `GET /mcp` for the stream.
  中文翻译：客户端在所有后续请求以及 `GET /mcp` 流上回显该头。
4. Session can be revoked by the server; client sees 404 on subsequent requests and must re-initialize.
  中文翻译：会话可被服务器撤销；客户端在后续请求中看到 404，必须重新初始化。
5. Client can explicitly DELETE the session for clean shutdown.
  中文翻译：客户端可显式 DELETE 会话以干净关闭。

### Keepalive and reconnect

SSE connections drop. The client re-establishes by re-GETing with the same `Mcp-Session-Id`. Server MUST queue events missed during the outage (up to a reasonable window) and replay via the `last-event-id` header the client echoes.

> SSE 连接会断开。客户端通过重新 GET（带相同 `Mcp-Session-Id`）重建。服务器必须排队（在合理窗口内）断连期间错过的事件并通过客户端回显的 `last-event-id` 头重放。

Phase 13 · 13 covers Tasks, which let long-running work survive even a full-session reconnect.

> Phase 13 · 13 涵盖 Tasks，让长运行工作即使全会话重连也能存活。

### Backwards compatibility probe

A client that wants to support both old and new servers:

> 想同时支持旧服务器和新服务器的客户端：

1. POST to `/mcp`.
2. If response is `200 OK` with JSON or SSE, this is Streamable HTTP.
  中文翻译：如果响应是 `200 OK` 带 JSON 或 SSE，这是 Streamable HTTP。
3. If response is `200 OK` with `Content-Type: text/event-stream` AND a `Location` header pointing to a secondary endpoint, this is legacy HTTP+SSE; follow the `Location`.
  中文翻译：如果响应是 `200 OK` 带 `Content-Type: text/event-stream` 且有指向二级端点的 `Location` 头，这是 legacy HTTP+SSE；跟随 `Location`。

### Cloudflare, ngrok, and hosting

> **【拓展：MCP 服务器部署选择】** 2026年生产级远程 MCP 服务器主要部署在 Cloudflare Workers（使用 MCP Agents SDK）、Vercel Functions 或容器化的 Node/Python。关键要求：托管平台必须支持长连接 HTTP 连接用于 SSE GET。Vercel 免费层限制 10 秒不适合，Cloudflare Workers 支持无限时长流。

Production remote MCP servers in 2026 run on Cloudflare Workers (with their MCP Agents SDK), Vercel Functions, or containerized Node/Python. Key: your hosting must support long-lived HTTP connections for the SSE GET. Vercel's free tier caps at 10 seconds and is unsuitable. Cloudflare Workers support indefinite streams.

> 2026 年生产级远程 MCP 服务器运行在 Cloudflare Workers（带 MCP Agents SDK）、Vercel Functions 或容器化的 Node/Python 上。关键：你的托管必须支持 SSE GET 的长连接 HTTP。Vercel 免费层上限 10 秒不合适。Cloudflare Workers 支持无限时长流。

### Gateway composition

When you front multiple MCP servers with a gateway (Phase 13 · 17), the gateway is a single Streamable HTTP endpoint that rewrites session ids and multiplexes upstream. Tools are merged at the gateway layer; the client sees a single logical server.

> 当你用网关（Phase 13 · 17）前置多个 MCP 服务器时，网关是一个单一的 Streamable HTTP 端点，重写 session id 并多路复用上游。工具在网关层合并；客户端看到单个逻辑服务器。

### Transport failure modes

> **【中文解读】** 五种传输失败模式：(1) stdio SIGPIPE——子进程中途死亡，客户端检测 EOF 标记会话死亡；(2) HTTP 502/504——代理层上游故障，短暂退避后重试；(3) SSE 连接断开——TCP RST 或代理超时，用 `Mcp-Session-Id` 和 `last-event-id` 重连恢复；(4) 会话撤销——服务器使 session id 失效，客户端看到 404 需重新握手；(5) 时钟偏移——以服务器时间戳为准。

- **stdio SIGPIPE.** Child process death mid-write raises SIGPIPE; servers should exit cleanly. Clients should detect EOF and mark the session dead.
  中文翻译：**stdio SIGPIPE。** 子进程在写入中途死亡引发 SIGPIPE；服务器应干净退出。客户端应检测 EOF 并将会话标记为死亡。
- **HTTP 502 / 504.** Cloudflare, nginx, and other proxies emit these on upstream failure. Streamable HTTP clients should retry once after a short backoff.
  中文翻译：**HTTP 502 / 504。** Cloudflare、nginx 等代理在上游失败时发出这些。Streamable HTTP 客户端应在短暂退避后重试一次。
- **SSE connection drop.** TCP RST, proxy timeout, or client network change closes the stream. Client reconnects with `Mcp-Session-Id` and optional `last-event-id` to resume.
  中文翻译：**SSE 连接断开。** TCP RST、代理超时或客户端网络变更关闭流。客户端用 `Mcp-Session-Id` 和可选的 `last-event-id` 重连恢复。
- **Session revocation.** Server invalidates a session id; client sees 404 on next request. Client must re-handshake.
  中文翻译：**会话撤销。** 服务器使 session id 失效；客户端在下次请求看到 404。客户端必须重新握手。
- **Clock skew.** Resource-TTL calculations on the client diverge from the server. Client should treat server timestamps as authoritative.
  中文翻译：**时钟偏移。** 客户端的 Resource-TTL 计算与服务器偏离。客户端应将服务器时间戳视为权威。

### When to bypass Streamable HTTP

Some enterprises deploy MCP servers behind gRPC or message-queue transports inside their own networks. This is non-standard — MCP's spec does not formally define these. Gateways can expose a Streamable HTTP surface to MCP clients while using gRPC internally. Keep the external surface spec-compliant; the gateway owns the translation.

> 某些企业在自己的网络内通过 gRPC 或消息队列传输部署 MCP 服务器。这是非标准的——MCP 规范未正式定义这些。网关可以向 MCP 客户端暴露 Streamable HTTP 表面，同时内部使用 gRPC。保持外部表面规范合规；网关拥有翻译。

`code/main.py` implements a minimal Streamable HTTP endpoint using `http.server` (stdlib). It handles POST, GET, and DELETE on `/mcp`, sets `Mcp-Session-Id` on first response, validates `Origin`, and rejects requests from non-allowlisted origins. The handler reuses the Lesson 07 notes server's dispatch logic.

> `code/main.py` 用 `http.server`（标准库）实现最小 Streamable HTTP 端点。它在 `/mcp` 上处理 POST、GET 和 DELETE，在首次响应设置 `Mcp-Session-Id`，验证 `Origin`，拒绝非白名单源的请求。该处理器复用 Lesson 07 笔记服务器的分发逻辑。

## Use It | 用框架实现

`code/main.py` implements a minimal Streamable HTTP endpoint using `http.server` (stdlib). It handles POST, GET, and DELETE on `/mcp`, sets `Mcp-Session-Id` on first response, validates `Origin`, and rejects requests from non-allowlisted origins. The handler reuses the Lesson 07 notes server's dispatch logic.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

What to look at:

- The POST handler reads the JSON-RPC body, dispatches, and writes a JSON response (the single-response variant; SSE variant is structurally similar).
  中文翻译：POST 处理器读取 JSON-RPC 体、分发，并写 JSON 响应（单响应变体；SSE 变体结构相似）。
- The `Origin` check rejects the default `http://evil.example` probe but accepts `http://localhost`.
  中文翻译：`Origin` 检查拒绝默认的 `http://evil.example` 探测但接受 `http://localhost`。
- Session ids are random 128-bit hex strings; the server keeps per-session state in memory.
  中文翻译：Session id 是随机 128 位十六进制字符串；服务器在内存中保存每会话状态。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-transport-migrator.md`. Given an HTTP+SSE (legacy) MCP server, the skill produces a migration plan to Streamable HTTP with session-id continuity, Origin checks, and backwards-compatible probe support.

> 本课产出 `outputs/skill-mcp-transport-migrator.md`。给定一个 HTTP+SSE（遗留）MCP 服务器，该 skill 生成到 Streamable HTTP 的迁移计划，包含 session-id 连续性、Origin 检查和向后兼容探测支持。

## Exercises | 练习题

1. Run `code/main.py`. POST an `initialize` from `curl` and observe the `Mcp-Session-Id` response header. POST a second request echoing the header and verify session continuity.
   中文翻译：运行 `code/main.py`。用 `curl` POST 一个 `initialize`，观察 `Mcp-Session-Id` 响应头。POST 第二个请求回显该头并验证会话连续性。

2. Add a GET handler that opens an SSE stream. Send one `notifications/progress` event every five seconds. Reconnect by re-GETing with the same session id and confirm the server accepts it.
   中文翻译：添加 GET 处理器打开 SSE 流。每 5 秒发一个 `notifications/progress` 事件。用相同 session id 重新 GET 重连并确认服务器接受。

3. Implement the `last-event-id` replay logic. On reconnect, replay any events generated since that id.
   中文翻译：实现 `last-event-id` 重放逻辑。重连时重放该 id 之后生成的所有事件。

4. Extend `Origin` validation to support a wildcard pattern (`https://*.example.com`) and confirm it accepts `https://app.example.com` but rejects `https://evil.example.com.attacker.net`.
   中文翻译：扩展 `Origin` 验证支持通配符模式（`https://*.example.com`），确认接受 `https://app.example.com` 但拒绝 `https://evil.example.com.attacker.net`。

5. Take a legacy HTTP+SSE server from the official registry (there are several) and sketch the migration: what changes in endpoint handling, session id generation, and header semantics.
   中文翻译：从官方注册表取一个遗留 HTTP+SSE 服务器（有几个），勾勒迁移：端点处理、session id 生成和头语义的变化。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| stdio transport | "Local child process" | JSON-RPC over stdin/stdout, newline-delimited | stdio 传输 |
| Streamable HTTP | "The remote transport" | Single-endpoint POST + GET + optional SSE, 2025-03-26 spec | Streamable HTTP 传输 |
| HTTP+SSE | "Legacy" | Two-endpoint model being removed in mid-2026 | HTTP+SSE（已弃用） |
| `Mcp-Session-Id` | "Session header" | Server-assigned random id echoed on every subsequent request | 会话标识头 |
| `Origin` allowlist | "DNS-rebinding defense" | Reject requests whose Origin is not approved | Origin 白名单 |
| Single endpoint | "One URL" | `/mcp` handles POST / GET / DELETE for all session operations | 单端点模式 |
| `last-event-id` | "SSE replay" | Header used to resume a dropped stream without missing events | SSE 重放标识 |
| Backwards-compat probe | "Old vs new detection" | Client response-shape check that auto-selects transport | 向后兼容探测 |
| Long-lived HTTP | "SSE streaming" | Server pushes events for minutes or hours on one TCP connection | 长连接 HTTP |
| Session revocation | "Force re-init" | Server invalidates a session id; client must handshake again | 会话撤销 |

## Further Reading | 延伸阅读

- [MCP — Basic transports spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) — canonical reference for stdio and Streamable HTTP
  中文翻译：stdio 和 Streamable HTTP 的权威参考
- [MCP — Basic transports spec 2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) — the revision that introduced Streamable HTTP
  中文翻译：引入 Streamable HTTP 的规范修订
- [Cloudflare — MCP transport](https://developers.cloudflare.com/agents/model-context-protocol/transport/) — Workers-hosted Streamable HTTP patterns
  中文翻译：Workers 托管的 Streamable HTTP 模式
- [AWS — MCP transport mechanisms](https://builder.aws.com/content/35A0IphCeLvYzly9Sw40G1dVNzc/mcp-transport-mechanisms-stdio-vs-streamable-http) — comparison across deployment shapes
  中文翻译：跨部署形态的对比
- [Atlassian — HTTP+SSE deprecation notice](https://community.atlassian.com/forums/Atlassian-Remote-MCP-Server/HTTP-SSE-Deprecation-Notice/ba-p/3205484) — concrete migration deadline example
  中文翻译：具体的迁移截止日期示例
