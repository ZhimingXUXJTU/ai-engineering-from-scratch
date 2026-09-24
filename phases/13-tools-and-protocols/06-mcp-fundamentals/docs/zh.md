# MCP 基础：无状态请求与 JSON-RPC

> 现代 MCP 没有握手，也没有协议会话。每个请求必须自带足够的元数据，才能被独立地理解、授权、路由和重试。

> **【中文解读】** 现代 MCP 没有握手，也没有协议会话。每个请求必须自带足够的元数据，才能被独立地理解、授权、路由和重试。这是 2026-07-28 规范相对旧版（2025-11-25 及更早的 initialize 握手模型）最根本的范式转变：协议核心从"连接级状态"变成"请求级自描述"。

> **【拓展：MCP→协议演进时间线】** MCP 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会下的 Agentic AI Foundation 管理。旧版（到 2025-11-25 为止）是"连接 → initialize 握手 → 操作"的三阶段生命周期模型；2026-07-28 版把协议核心改为无状态：每个请求在 `params._meta` 里自带协议版本、客户端能力与身份，`initialize` 降级为旧版兼容路径。本课是这个 MCP 系列的地基，后续 07（服务器）、08（客户端）都基于这个无状态模型。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 01-05——工具接口、函数调用、Schema 设计；(2) JSON-RPC 2.0 基础（request/response/notification 三种信封）；(3) 对旧版 MCP 的 initialize 握手有整体认识（本课会解释它为何被废弃为兼容分支）。本课只讲基础协议；扩展机制在后续课程展开。

**类型：** 学习
**语言：** Python
**前置条件：** Phase 13 · 01-05
**时间：** 约 55 分钟

## 学习目标

- 区分 MCP 的服务器原语与客户端特性。
- 为 MCP `2026-07-28` 构建合法的 JSON-RPC 2.0 请求与响应。
- 为每个请求附加协议版本、客户端能力和客户端身份。
- 在无握手的前提下使用 `server/discover` 并处理 `UnsupportedProtocolVersionError`。
- 追踪一个独立请求从校验到完整结果的全程。

## 问题引入

一个 MCP 服务器可能在同一个进程或 HTTP worker 上先后收到来自不同客户端、带着不同能力的两个请求。如果服务器记住了上一个请求声明过什么，就可能套用错误的权限，或返回错误的线格式。

MCP `2026-07-28` 消除了这种歧义。协议核心是无状态的。服务器必须只依据"当前这个请求"本身来决定如何处理它，而不是依据连接历史。

这改变了心智模型。旧版的顺序是：先建连接、再握手、后操作。现代的顺序更简单：

1. 客户端发送一个自描述的请求。
2. 服务器校验该请求自带的版本与能力。
3. 服务器处理这个方法。
4. 服务器返回一个类型化结果或一个 JSON-RPC 错误。

下一个请求从头重复同样的流程。

> **【中文解读】** 旧模型的隐患在于"服务器记忆"：同一进程先后服务多个客户端时，上一个请求声明的 capabilities 会污染下一个请求的处理。新规范要求每个请求自描述（版本、能力、身份都写在 `params._meta` 里），服务器处理完即忘。这既适配无共享的多 worker 部署，也让重试和幂等变得简单——任何副本都能独立处理任何请求。

## 核心概念

### 服务器原语

MCP 服务器暴露三个主要原语：

1. **Tools** 是由模型控制的动作，用 `tools/list` 发现、用 `tools/call` 调用。
2. **Resources** 是按 URI 寻址的数据，用 `resources/list` 发现、用 `resources/read` 读取。
3. **Prompts** 是可复用模板，用 `prompts/list` 发现、用 `prompts/get` 渲染。

roots、sampling 和 logging 在 `2026-07-28` schema 中为兼容而保留，但已被废弃。新实现应当：roots 用显式的工具或资源输入替代；sampling 直接调用模型提供商 API；logging 用 stderr 或 OpenTelemetry。elicitation 仍可通过"多轮往返请求"（Multi Round-Trip Requests）使用——服务器返回一个输入请求，客户端补齐后重试原操作。现代服务器绝不主动发起独立的 JSON-RPC 请求。

> **【中文解读】** 服务器原语仍是三个：Tools（模型可调用的动作）、Resources（按 URI 寻址的数据）、Prompts（可复用模板）。注意新版的重大变化：roots/sampling/logging 这三个旧客户端原语虽保留但已废弃；elicitation 改走"多轮往返请求"（服务器返回 input_required，客户端补齐输入后重试）。现代服务器不再主动发起任何独立 JSON-RPC 请求——控制流始终从客户端发起。

### JSON-RPC 信封

MCP 使用 JSON-RPC 2.0：

- 请求：`{jsonrpc, id, method, params}`
- 响应：`{jsonrpc, id, result}` 或 `{jsonrpc, id, error}`
- 通知：`{jsonrpc, method, params}`，没有 `id`

请求 `id` 只用于关联一个响应。它不创建协议会话。

### 必需的请求元数据

每个现代请求都在 `params` 内携带一个 `_meta` 对象：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    }
  }
}
```

协议版本和客户端能力是必填的。客户端身份是建议提供的。它是自报的展示与调试数据，不是安全凭证。

服务器不得从更早的请求、stdio 进程、HTTP 连接或单个传输层头部推断这些值。

### 完整结果与服务器身份

每个成功的现代结果都包含 `resultType`。普通最终结果用 `"complete"`。服务器还应在结果元数据中标识自己：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "resultType": "complete",
    "tools": [],
    "ttlMs": 30000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "notes-server",
        "version": "1.0.0"
      }
    }
  }
}
```

`tools/list`、`resources/list`、`prompts/list`、`resources/templates/list`、`resources/read` 和 `server/discover` 是可缓存结果，它们包含 `ttlMs` 和 `cacheScope`。安全默认值是 `ttlMs: 0` 加 `cacheScope: "private"`。列表项应有确定性排序，这样等价的响应才能产生稳定的缓存键和稳定的模型上下文。

### 无握手的发现

每个现代服务器必须实现 `server/discover`。客户端可以在调用其他方法之前先调用它，获取：

- `supportedVersions`（支持的版本集合）
- 服务器 `capabilities`（能力）
- 可选的使用 `instructions`（说明）
- 结果 `_meta` 中的服务器身份
- 缓存提示

发现很有用，但它不是闸门。客户端可以先发 `tools/list`，因为那个请求本来就携带了自己的协议版本和能力。

如果请求的版本不受支持，服务器返回 JSON-RPC 错误码 `-32022`，附带：

```json
{
  "requested": "2027-01-01",
  "supported": ["2026-07-28"]
}
```

客户端选定一个双方都支持的现代版本，用一个新的 JSON-RPC 请求 id 重试。

### 单个请求的生命周期

按以下顺序追踪一个现代请求：

1. 解析一个 JSON-RPC 信封。
2. 确认 `jsonrpc` 是 `"2.0"`、存在 `id`、`method` 是字符串、`params` 是对象。
3. 要求 `params._meta` 中有版本字符串和能力对象；元数据畸形或缺失返回 `-32602`。
4. 在 HTTP 边界处比对版本、方法和适用的名称头部与 body。不一致返回 `-32020`——即使两个版本值中有一个本身就不受支持。
5. 确认一致之后，再拒绝"一致但不受支持"的版本，返回 `-32022`。
6. 检查必需能力，然后按 `method` 路由并校验方法级参数。
7. 在 handler 运行之前对具体操作做认证与授权。
8. 返回带服务器身份的完整结果。
9. 忘掉请求级的协议元数据。

> **【中文解读】** 这个顺序本身就是安全设计：先验证信封、再验证元数据、再比对头部与 body（防"头说 notes.read、body 却是 notes.delete"的走私）、然后才授权和执行。每一步的失败都有独立的错误码，排查时能精确定位是哪一层出了问题，而不是拿到一锅粥的"400 Bad Request"。

这个顺序防止两个组件对"同一个调用"做出不同解读。网关不得授权 `Mcp-Name: notes.read` 的同时源站却执行 `params.name: notes.delete`。它还让畸形输入、头部混淆、版本协商、能力缺失、授权失败和 handler 故障各自留下独立的证据。

关闭 stdin 或返回 HTTP 响应只是结束传输层活动。它并不终止协议会话，因为现代 MCP 根本没有协议会话。

### 显式旧版兼容

到 `2025-11-25` 为止的版本使用 `initialize`、`notifications/initialized`、连接级能力，以及在早期 Streamable HTTP 上可选的协议会话。当双时代客户端要对接旧服务器时，这些行为仍然相关。

把两个时代分开。现代请求由必需的逐请求元数据识别。旧版连接只能通过文档规定的回退路径选择。不要把 `initialize` 当作发给 `2026-07-28` 服务器的默认行为。

因此"无状态"有时代特定的含义。在 `2026-07-28` 中它是协议不变式：每个普通请求都可独立解读，不存在 MCP 会话。在到 `2025-11-25` 为止的版本中，初始化和协商出的能力属于连接，所以兼容适配器可以保留那份旧版连接状态。双时代实现不是一台"什么都能容"的状态机，而是：一个无状态的现代内核，旁边挂一个隔离的旧版适配器，在任何解析器运行之前先做一次显式的时代选择。

两种含义都不禁止持久的应用状态。工作流、任务或草稿可以活在共享存储中的一个不透明句柄后面。客户端把这个句柄当普通输入发送，每个副本都对它的使用做认证与授权。协议上下文不得作为被移除会话的替身泄漏进那个存储。

> **【拓展：双时代并存的现实】** "无状态"绝不等于"不能有业务状态"——这是最常见的误读。笔记、任务、工作流照常存库；被禁止的只是"把协议上下文当隐式会话用"（例如靠"这条连接上次声明过什么能力"来解码下一条请求）。分清"应用状态（可以持久）"与"协议会话状态（已移除）"，就抓住了 2026-07-28 版的精神。

## 用框架实现

`code/main.py` 在不借助任何框架的情况下构建、校验、追踪并分发现代 MCP 消息。运行：

```bash
python3 code/main.py
python3 -m unittest discover code/tests -v
```

在输出中关注三个不变式：

- 每个请求都重复携带自己的 `_meta` 字段。
- 每个成功结果都是 `resultType: "complete"` 且包含服务器身份。
- 列表结果有确定性排序并带显式缓存提示。

## 产出物

本课交付 `outputs/skill-mcp-handshake-tracer.md`。文件名沿用历史名称，但产物现在是一个无状态请求追踪器：它独立审计每条消息，只有当握手流量真实出现时才标注为 legacy。

## 练习题

1. 把某个请求的协议版本改成 `2027-01-01`。确认错误码是 `-32022` 且 data 中公示了受支持的版本。

2. 从第二个请求中移除 `io.modelcontextprotocol/clientCapabilities`。确认服务器不会复用第一个请求的能力声明。

3. 反转内存中的工具注册表。确认 `tools/list` 仍返回同样的确定性顺序。

4. 把 `cacheScope` 从 `public` 改成 `private`。解释两种情况下哪些授权上下文可以复用该响应。

5. 添加一个可选的 `clientInfo` 缺省测试。该请求应当仍然合法，因为客户端身份是建议项而非必填项。

## 术语速查表

| 术语 | 含义 |
|------|------|
| 无状态协议 | 每个请求自带解读自身所需的元数据 |
| 请求元数据 | `params._meta` 中的版本、客户端能力与建议的客户端身份 |
| `server/discover` | 必选的服务器方法，公示版本、能力、说明与身份 |
| `resultType` | 每个成功现代结果上的判别字段 |
| 可缓存结果 | 必含 `ttlMs` 与 `cacheScope` 提示的结果 |
| 协议时代 | 现代逐请求元数据，或旧版连接级初始化 |
| 传输层生命周期 | 进程、连接或响应流的存活期，不是协议会话状态 |
| `-32022` | 不支持的协议版本错误，附 requested 与 supported |

## 延伸阅读

- [MCP Architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture) — MCP 架构文档（2026-07-28 版）
- [MCP Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic) — MCP 基础协议（JSON-RPC 信封、元数据、生命周期）
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — server/discover 方法规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — 2026-07-28 版变更日志（相对旧版的核心差异清单）
