# MCP Transports — stdio vs Streamable HTTP vs SSE Migration | MCP 传输层：stdio 与 Streamable HTTP

> stdio works locally and nowhere else. Streamable HTTP (2025-03-26) is the remote standard. The old HTTP+SSE transport is deprecated and being removed in mid-2026. Picking the wrong transport costs a migration; picking the right one buys a remote-hostable MCP server with session continuity and DNS-rebinding protection.

> **【中文解读】** stdio 只能在本地工作。Streamable HTTP (2025-03-26) 是远程标准。旧的 HTTP+SSE 传输已被弃用，将在 2026 年中期移除。选错传输层意味着一次迁移；选对则获得一个可远程部署的 MCP 服务器，具备会话连续性和 DNS 重绑定防护。

> **【拓展：传输层→Claude 远程 MCP】** Claude Desktop 使用 stdio 传输与本地 MCP 服务器通信。对于远程 MCP 服务器（如部署在 Cloudflare Workers 上），使用 Streamable HTTP 传输。Streamable HTTP 的单端点模式（`/mcp`）简化了部署，`Mcp-Session-Id` 头确保会话连续性，`Origin` 验证防止 DNS 重绑定攻击。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, Streamable HTTP endpoint skeleton) | **语言:** Python (stdlib, Streamable HTTP endpoint skeleton)
**Prerequisites:** Phase 13 · 07, 08 (MCP server and client) | **前置知识:** Phase 13 · 07, 08 (MCP server and client)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Pick between stdio and Streamable HTTP based on deployment shape (local vs remote, single-process vs fleet).
  中文翻译：参见英文条目了解详情。
- Implement the Streamable HTTP single-endpoint pattern: POST for requests, GET for session stream.
  中文翻译：参见英文条目了解详情。
- Enforce `Origin` validation and session-id semantics to defeat DNS-rebinding.
  中文翻译：参见英文条目了解详情。
- Migrate a legacy HTTP+SSE server to Streamable HTTP before the mid-2026 removal deadlines.
  中文翻译：参见英文条目了解详情。

## The Problem | 问题引入

> **【中文解读】** MCP 的两种传输模式：(1) stdio——本地服务器，客户端作为子进程启动，通过 stdin/stdout 通信；(2) Streamable HTTP——远程服务器，单端点 `/mcp`，用 `Mcp-Session-Id` 管理会话。2025-03-26 规范用 Streamable HTTP 替代了旧的 HTTP+SSE 双端点模式。stdio 适用于"本机"，Streamable HTTP 适用于"网络"。

The first MCP remote transport (2024-11) was HTTP+SSE: two endpoints, one for the client's POSTs and one Server-Sent-Events channel for the server-to-client stream. It worked. It was also clumsy: two endpoints per session, broken caches in front of some CDNs, and a hard dependency on long-lived SSE connections that some WAFs terminate aggressively.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

The 2025-03-26 spec replaced it with Streamable HTTP: one endpoint, POST for client requests, GET for establishing a session stream, both sharing a `Mcp-Session-Id` header. Every server built or migrated since then uses Streamable HTTP. The old SSE mode is being deprecated — Atlassian Rovo removed it June 30, 2026; Keboola April 1, 2026; most remaining enterprise servers by end of 2026.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

And stdio still matters for local servers. Claude Desktop, VS Code, and every IDE-shaped client spawn servers via stdio. The right mental model: stdio for "this machine", Streamable HTTP for "over the network". No cross-over.

> 传输层相关内容：stdio 用于本地通信，Streamable HTTP 用于远程部署。

## The Concept | 核心概念

### stdio

- Child-process transport. Client spawns server, communicates via stdin/stdout.
  中文翻译：参见英文条目了解详情。
- One JSON object per line. Newline-delimited.
  中文翻译：参见英文条目了解详情。
- No session id; process identity is the session.
  中文翻译：参见英文条目了解详情。
- No auth needed (the child inherits the parent's trust boundary).
  中文翻译：参见英文条目了解详情。
- Never use for remote servers — you would need SSH or socat to tunnel, at which point use Streamable HTTP.
  中文翻译：参见英文条目了解详情。

### Streamable HTTP

> **【拓展：Streamable HTTP 相比 SSE 的改进】** Streamable HTTP 相比旧的双端点 SSE 模式有三个改进：(1) 单端点简化了部署和 CDN 配置；(2) `Mcp-Session-Id` 头提供可靠的会话管理；(3) 支持 POST 返回单响应或 SSE 流，更灵活。大多数 MCP 服务器（包括 Atlassian Rovo、Keboola）已在 2026 年完成迁移。

Single endpoint `/mcp` (or any path). Supports three HTTP methods:

> 参见英文原文获取完整的技术说明。

- **POST /mcp.** Client sends a JSON-RPC message. Server replies with either a single JSON response, or an SSE stream of one-or-more responses (useful for batched responses and notifications related to that request).
  中文翻译：**POST /mcp.** — 参见英文原文了解详情。
- **GET /mcp.** Client opens a long-lived SSE channel. Server uses it for server-to-client requests (sampling, notifications, elicitation).
  中文翻译：**GET /mcp.** — 参见英文原文了解详情。
- **DELETE /mcp.** Client explicitly terminates the session.
  中文翻译：**DELETE /mcp.** — 参见英文原文了解详情。

Sessions are identified by the `Mcp-Session-Id` header the server sets on the first response and the client echoes on every subsequent request. Session ids MUST be cryptographically random (128+ bits); client-chosen ids are rejected for safety.

> **【中文解读】** 会话由服务器在首次响应时设置的 `Mcp-Session-Id` 头标识。Session id 必须是密码学随机的（128+ 位）；客户端自行选择的 id 会被拒绝。`Origin` 验证防止 DNS 重绑定攻击——攻击者可构造网页让浏览器 POST 到 `localhost:1234/mcp`。

### Single endpoint vs two

Two-endpoint mode from the old spec is still callable in 2026 — the spec declares it "legacy compatible". But all new servers should be single-endpoint. The official SDKs emit single-endpoint; use the legacy mode only when talking to an unmigrated remote.

> 技能与打包相关内容：Agent SDK 和可复用技能的定义与分发。

### `Origin` validation and DNS-rebinding

> **【拓展：DNS 重绑定攻击与 MCP 安全】** DNS 重绑定是一种攻击向量：攻击者构造网页让浏览器 POST 到 `localhost:1234/mcp`，如果 MCP 服务器不检查 `Origin` 头，就会执行恶意请求。2025-11-25 规范要求服务器拒绝不在白名单上的 `Origin`。白名单通常包含 MCP 客户端主机（`https://claude.ai`、`vscode-webview://*`）和 localhost 变体。

Browsers are not MCP clients (today), but an attacker can craft a webpage that convinces a browser to POST to `localhost:1234/mcp` — where the user's local MCP server listens. If the server does not check `Origin`, the browser's same-origin policy will not save it because `Origin: http://evil.com` is valid cross-origin.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

The 2025-11-25 spec requires servers to reject requests whose `Origin` is not on an allowlist. The allowlist typically contains the MCP client host (`https://claude.ai`, `vscode-webview://*`) and localhost variants for local UIs.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### Session id lifecycle

1. Client sends first request without `Mcp-Session-Id`.
  中文翻译：参见英文条目了解详情。
2. Server assigns a random id, sets `Mcp-Session-Id` on the response header.
  中文翻译：参见英文条目了解详情。
3. Client echoes that header on all subsequent requests and on `GET /mcp` for the stream.
  中文翻译：参见英文条目了解详情。
4. Session can be revoked by the server; client sees 404 on subsequent requests and must re-initialize.
  中文翻译：参见英文条目了解详情。
5. Client can explicitly DELETE the session for clean shutdown.
  中文翻译：参见英文条目了解详情。

### Keepalive and reconnect

SSE connections drop. The client re-establishes by re-GETing with the same `Mcp-Session-Id`. Server MUST queue events missed during the outage (up to a reasonable window) and replay via the `last-event-id` header the client echoes.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

Phase 13 · 13 covers Tasks, which let long-running work survive even a full-session reconnect.

> 异步任务相关内容：长时间运行工具的进度报告和任务管理。

### Backwards compatibility probe

A client that wants to support both old and new servers:

> 参见英文原文获取完整的技术说明。

1. POST to `/mcp`.
2. If response is `200 OK` with JSON or SSE, this is Streamable HTTP.
  中文翻译：参见英文条目了解详情。
3. If response is `200 OK` with `Content-Type: text/event-stream` AND a `Location` header pointing to a secondary endpoint, this is legacy HTTP+SSE; follow the `Location`.
  中文翻译：参见英文条目了解详情。

### Cloudflare, ngrok, and hosting

> **【拓展：MCP 服务器部署选择】** 2026年生产级远程 MCP 服务器主要部署在 Cloudflare Workers（使用 MCP Agents SDK）、Vercel Functions 或容器化的 Node/Python。关键要求：托管平台必须支持长连接 HTTP 连接用于 SSE GET。Vercel 免费层限制 10 秒不适合，Cloudflare Workers 支持无限时长流。

Production remote MCP servers in 2026 run on Cloudflare Workers (with their MCP Agents SDK), Vercel Functions, or containerized Node/Python. Key: your hosting must support long-lived HTTP connections for the SSE GET. Vercel's free tier caps at 10 seconds and is unsuitable. Cloudflare Workers support indefinite streams.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### Gateway composition

When you front multiple MCP servers with a gateway (Phase 13 · 17), the gateway is a single Streamable HTTP endpoint that rewrites session ids and multiplexes upstream. Tools are merged at the gateway layer; the client sees a single logical server.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### Transport failure modes

> **【中文解读】** 五种传输失败模式：(1) stdio SIGPIPE——子进程中途死亡，客户端检测 EOF 标记会话死亡；(2) HTTP 502/504——代理层上游故障，短暂退避后重试；(3) SSE 连接断开——TCP RST 或代理超时，用 `Mcp-Session-Id` 和 `last-event-id` 重连恢复；(4) 会话撤销——服务器使 session id 失效，客户端看到 404 需重新握手；(5) 时钟偏移——以服务器时间戳为准。

- **stdio SIGPIPE.** Child process death mid-write raises SIGPIPE; servers should exit cleanly. Clients should detect EOF and mark the session dead.
  中文翻译：**stdio SIGPIPE.** — 参见英文原文了解详情。
- **HTTP 502 / 504.** Cloudflare, nginx, and other proxies emit these on upstream failure. Streamable HTTP clients should retry once after a short backoff.
  中文翻译：**HTTP 502 / 504.** — 参见英文原文了解详情。
- **SSE connection drop.** TCP RST, proxy timeout, or client network change closes the stream. Client reconnects with `Mcp-Session-Id` and optional `last-event-id` to resume.
  中文翻译：**SSE connection drop.** — 参见英文原文了解详情。
- **Session revocation.** Server invalidates a session id; client sees 404 on next request. Client must re-handshake.
  中文翻译：**Session revocation.** — 参见英文原文了解详情。
- **Clock skew.** Resource-TTL calculations on the client diverge from the server. Client should treat server timestamps as authoritative.
  中文翻译：**Clock skew.** — 参见英文原文了解详情。

### When to bypass Streamable HTTP

Some enterprises deploy MCP servers behind gRPC or message-queue transports inside their own networks. This is non-standard — MCP's spec does not formally define these. Gateways can expose a Streamable HTTP surface to MCP clients while using gRPC internally. Keep the external surface spec-compliant; the gateway owns the translation.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Use It | 用框架实现

`code/main.py` implements a minimal Streamable HTTP endpoint using `http.server` (stdlib). It handles POST, GET, and DELETE on `/mcp`, sets `Mcp-Session-Id` on first response, validates `Origin`, and rejects requests from non-allowlisted origins. The handler reuses the Lesson 07 notes server's dispatch logic.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

What to look at:

- The POST handler reads the JSON-RPC body, dispatches, and writes a JSON response (the single-response variant; SSE variant is structurally similar).
  中文翻译：参见英文条目了解详情。
- The `Origin` check rejects the default `http://evil.example` probe but accepts `http://localhost`.
  中文翻译：参见英文条目了解详情。
- Session ids are random 128-bit hex strings; the server keeps per-session state in memory.
  中文翻译：参见英文条目了解详情。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-transport-migrator.md`. Given an HTTP+SSE (legacy) MCP server, the skill produces a migration plan to Streamable HTTP with session-id continuity, Origin checks, and backwards-compatible probe support.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Exercises | 练习题

1. Run `code/main.py`. POST an `initialize` from `curl` and observe the `Mcp-Session-Id` response header. POST a second request echoing the header and verify session continuity.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Add a GET handler that opens an SSE stream. Send one `notifications/progress` event every five seconds. Reconnect by re-GETing with the same session id and confirm the server accepts it.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

3. Implement the `last-event-id` replay logic. On reconnect, replay any events generated since that id.
   中文翻译：实现相关练习。参见英文原文了解完整要求。

4. Extend `Origin` validation to support a wildcard pattern (`https://*.example.com`) and confirm it accepts `https://app.example.com` but rejects `https://evil.example.com.attacker.net`.
   中文翻译：扩展相关练习。参见英文原文了解完整要求。

5. Take a legacy HTTP+SSE server from the official registry (there are several) and sketch the migration: what changes in endpoint handling, session id generation, and header semantics.
   中文翻译：参见英文原文了解完整练习要求。

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
  中文翻译：canonical reference for stdio and Streamable HTTP
- [MCP — Basic transports spec 2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) — the revision that introduced Streamable HTTP
  中文翻译：the revision that introduced Streamable HTTP
- [Cloudflare — MCP transport](https://developers.cloudflare.com/agents/model-context-protocol/transport/) — Workers-hosted Streamable HTTP patterns
  中文翻译：Workers-hosted Streamable HTTP patterns
- [AWS — MCP transport mechanisms](https://builder.aws.com/content/35A0IphCeLvYzly9Sw40G1dVNzc/mcp-transport-mechanisms-stdio-vs-streamable-http) — comparison across deployment shapes
  中文翻译：comparison across deployment shapes
- [Atlassian — HTTP+SSE deprecation notice](https://community.atlassian.com/forums/Atlassian-Remote-MCP-Server/HTTP-SSE-Deprecation-Notice/ba-p/3205484) — concrete migration deadline example
  中文翻译：concrete migration deadline example
