# MCP 传输层：stdio 与无状态 Streamable HTTP

> 传输层只负责搬运 MCP 消息，不负责补齐协议状态。在 2026-07-28 规范中，本地 stdio 和远程 Streamable HTTP 传递的都是"自描述"请求——每个请求自带协议版本与客户端能力，不再依赖连接或会话保存上下文。

> **【中文解读】** 本课讲 MCP 的两种现代传输：stdio 面向客户端启动的本地子进程，Streamable HTTP 面向网络服务。2026-07-28 规范把传输层彻底无状态化——没有会话头、没有独立 GET 流、没有 DELETE 端点、没有 `Last-Event-ID` 恢复；取而代之的是镜像头校验、请求级 SSE 和 `subscriptions/listen` 订阅流。学完本课你应能判断该用哪种传输、如何实现现代契约、以及如何安全迁移遗留部署。

> **【拓展：传输层演进→2026-07-28 无状态化】** MCP 传输层三年三变：2024-11 的 HTTP+SSE 双端点、2025-03-26 的 Streamable HTTP（GET 流 + `Mcp-Session-Id` 会话）、再到 2026-07-28 的无状态 POST-only 契约。演进方向始终是"把状态从传输层赶出去"：会话头没了，改成请求体 `_meta` 携带版本与能力；独立 GET 流没了，改成 `subscriptions/listen` 请求级响应流。无状态让任意健康副本都能处理任意请求，是云原生横向扩展的关键。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13·07、08（MCP server 和 client）——理解 JSON-RPC 分发逻辑；(2) HTTP 协议基础（method、header、状态码）；(3) DNS 重绑定攻击概念——本课的 `Origin` 校验是防御手段；(4) 若你学过本课旧版（2025 传输：GET 流 + 会话头 + `Last-Event-ID` 重放），请先清空那套旧心智模型再往下读。

**类型：** 学习
**语言：** Python
**前置条件：** Phase 13 · 07、08（MCP 服务器与客户端）
**预计用时：** 约 65 分钟

## 学习目标

- 本地子进程选 stdio，网络服务选 Streamable HTTP。
- 实现现代的单端点、仅 POST 的 Streamable HTTP 契约。
- 把 MCP 版本、方法、名称镜像头与 JSON-RPC 请求体做比对校验。
- 正确交付请求级 SSE 流和长生命周期的 `subscriptions/listen` 流。
- 迁移基于会话的部署和遗留 HTTP+SSE 部署，且不把遗留行为冒充为现代行为。

## 问题引入

> **【中文解读】** 本节讲清"为什么要无状态"。早期 Streamable HTTP 把协议协商、连接行为、会话行为捆在一起；2026-07-28 把这些机制全部移除，让每个请求都能落在任意健康 worker 上。代价是：还在把 2025 传输当作现行规范教的服务器，教的是错误的失败模型和安全模型。

更早的 Streamable HTTP 修订版把协议协商与连接、会话行为捆绑在一起。服务器可以铸造 `Mcp-Session-Id`、暴露一个独立的 GET 流、接受 DELETE 来终止会话，并用 `Last-Event-ID` 恢复 SSE。

MCP `2026-07-28` 从现代线格式中移除了这些机制。每个请求都可以落在任意健康 worker 上，因为协议版本和客户端能力随请求体传输。HTTP 头为路由和策略镜像了部分字段，但服务器在执行前会把这些头与请求体比对校验。

结果是更容易扩展、也更容易推理。这也意味着：把 2025 传输当作现行规范来教的服务器，教的是错误的失败模型和安全模型。

> 💡 **【类比】** 无状态传输像外卖平台的订单流转。旧模式（会话式传输）像"你只能等当初接单的那个骑手"——骑手下线（副本重启），订单就卡住。新模式（2026-07-28 无状态）像"任何站点都能接手你的订单"——每张订单（请求）都完整写明地址和备注（协议版本、能力），谁接手都能继续干活；贵重物品寄存（应用状态）不塞进骑手口袋（连接亲和性），而是给一张取件码（显式状态句柄）。

## 核心概念

### stdio

> **【中文解读】** stdio 是最简单的绑定：客户端启动子进程，双方用"每行一条 JSON-RPC 消息"交换数据，诊断走 stderr，stdin 关闭就退出。注意：进程长寿不等于协议会话——进程一死，进行中的请求全部丢失，恢复手段是重启 + 重新发现 + 重试。

stdio 绑定面向客户端启动的子进程：

- 客户端向 stdin 每行写入一条 UTF-8 JSON-RPC 消息。
- 服务器向 stdout 每行写入一条 UTF-8 JSON-RPC 消息。
- 服务器把诊断信息写入 stderr。
- stdin 出现 EOF 时服务器立即退出。
- 每个现代请求都在 `params._meta` 中携带版本和客户端能力。

进程可以存活多次调用，但它并不是现代意义上的协议会话。如果进程意外退出，进行中的请求会丢失。正确做法是：重启进程、重新发现、重新列清单、重新打开订阅，并用新的请求 id 重试安全的操作。

### 2026-07-28 的 Streamable HTTP

> **【中文解读】** 现代服务器只暴露一个接收 POST 的端点。请求的应答有两种形态：单条 JSON 响应，或"相关通知 + 最终响应"的 SSE 流；通知被接受则返回无主体的 `202 Accepted`。客户端用 `Accept` 头同时声明接受两种形态。

现代服务器暴露一个接收 POST 的 MCP 端点，例如 `/mcp`。

每条 JSON-RPC 请求或通知都是一次新的 HTTP POST。请求体包含一条 JSON-RPC 消息。客户端不向服务器发送 JSON-RPC 响应。

对于请求，服务器返回两种之一：

- `Content-Type: application/json` 带一条 JSON-RPC 响应；或
- `Content-Type: text/event-stream` 先带与该请求相关的通知，再带最终 JSON-RPC 响应。

对于被接受的通知，服务器返回不带主体的 `202 Accepted`。

客户端同时声明接受两种响应类型：

```http
Accept: application/json, text/event-stream
```

### 仅 POST 就是仅 POST

> **【中文解读】** 这是最容易踩坑的一节：现代 Streamable HTTP 没有 GET 流、没有 DELETE 端点、没有会话头、没有流恢复。请求级流中断 = 该请求丢失，唯一出路是换新 id 重试。

现代 Streamable HTTP 没有独立 GET 流，也没有 DELETE 会话端点。

- `GET /mcp` 返回 `405 Method Not Allowed`。
- `DELETE /mcp` 返回 `405 Method Not Allowed`。
- `Mcp-Session-Id` 被忽略，从不铸造也从不回显。
- `Last-Event-ID` 被忽略，因为现代流不可恢复。

如果请求级流在最终响应前中断，客户端就失去了这个进行中的请求。它可以在重试安全时用一个新 JSON-RPC id 发起新请求。它绝不能尝试流恢复。

### Origin 校验

> **【中文解读】** `Origin` 校验防的是 DNS 重绑定，不是认证。头存在且不在白名单 → `403`；非浏览器客户端可省略该头。本地服务器绑 `127.0.0.1`，网络服务另做逐请求认证。匹配必须精确——前缀检查会放行攻击者控制的后缀。

服务器在进入连接上校验 `Origin` 以防 DNS 重绑定。如果该头存在且未被显式允许，返回 `403 Forbidden`。非浏览器客户端可以省略 `Origin`，官方传输规则允许这一点。

本地服务器应绑定 `127.0.0.1`，而不是所有网卡。网络服务仍然需要对每个请求做认证和授权。Origin 校验不是认证。

在规范化配置之后使用精确的 origin 匹配。`origin.startswith("https://trusted.example")` 这类前缀检查不安全，因为它们可能接受攻击者控制的后缀。

### 必需的 HTTP 元数据头

> **【中文解读】** 三个镜像头（版本、方法、名称）是路由与策略的冗余副本，服务器执行前必须与请求体比对。`Mcp-Name` 遇到非 ASCII 值时用 Base64 哨兵编码。错误码三件套：头不匹配 `-32020`、版本不支持 `-32022`（带精确 supported/requested 数据）、未知方法 `-32601`（HTTP 404）。

每个现代 POST 请求都包含：

```http
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes_search
```

头规则：

- `MCP-Protocol-Version` 必填，且必须等于 `params._meta.io.modelcontextprotocol/protocolVersion`。
- `Mcp-Method` 必填，且必须等于 JSON-RPC `method`。
- `tools/call`、`resources/read`、`prompts/get` 必带 `Mcp-Name`。
- `Mcp-Name` 等于 `params.name`；对 `resources/read` 则等于 `params.uri`。
- 头值大小写敏感，尽管头名大小写不敏感。

不安全或非 ASCII 的 `Mcp-Name` 值使用精确的 UTF-8 Base64 哨兵格式：

```text
=?base64?{Base64EncodedValue}?=
```

服务器先解码该值再与请求体比对。

镜像头缺失、畸形或不匹配时返回 HTTP `400` 和 JSON-RPC 错误码 `-32020`。如果头与请求体一致地指向一个服务器不支持的版本，返回 HTTP `400` 和 `-32022`，并带精确的错误数据，例如 `{"supported":["2026-07-28"],"requested":"2027-01-01"}`。

未知的现代方法返回 HTTP `404` 和 JSON-RPC `-32601`。JSON-RPC 响应体很重要，因为双时代客户端靠它区分"现代错误"与"遗留端点未命中"。

### 请求级 SSE

> **【中文解读】** SSE 现在只服务于单个长运行请求：流上只有该请求 id 的进度通知和最终响应。服务器不得在流上发送独立请求（sampling、elicitation、roots 全部改走 MRTR）；关流即取消请求；不要加事件 id 做重放。

服务器可以为单个长运行请求选择 SSE：

```text
POST tools/call id=41
  <- notifications/progress related to id=41
  <- notifications/progress related to id=41
  <- JSON-RPC response id=41
stream closes
```

服务器不得在这条流上发送独立的 JSON-RPC 请求。Sampling、elicitation 和 roots 交互使用 Multi Round-Trip Request（MRTR）结果。关闭响应流即取消该请求。

不要为重放添加 SSE 事件 id。`Last-Event-ID` 恢复不属于现代修订。

### 长生命周期变更使用 subscriptions/listen

> **【中文解读】** 订阅的方向反转了：不再是客户端开 GET 流等服务器推送，而是客户端主动 POST 一条 `subscriptions/listen`，其响应流保持打开。`notifications` 对象是允许清单，服务器不得投递未请求的通知类型；确认、每条通知和最终结果都携带等于请求 id 的 `subscriptionId`；断流后换新 id 重新 listen。

变更通知使用客户端发起的请求，而不是独立 GET：

```json
{
  "jsonrpc": "2.0",
  "id": "listen-1",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true,
      "resourceSubscriptions": ["notes://note-1"]
    },
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

POST 的响应是一条长生命周期 SSE 流。它的第一条协议消息是 `notifications/subscriptions/acknowledged`。确认消息、每条变更通知和最终结果都在 `_meta` 中携带 `io.modelcontextprotocol/subscriptionId`，其值等于 listen 请求的 id。服务器可以用 SSE 注释作为保活。当流断开时，客户端用新的请求 id 重新发出 `subscriptions/listen` 并重新拉取受影响的数据。

`resources/subscribe` 和 `resources/unsubscribe` 属于遗留时代。不要在现代连接上使用它们。

### 显式应用状态

> **【中文解读】** 无协议会话 ≠ 无状态工作流。状态可以有，但必须显式：服务器铸造不透明句柄、作为普通工具结果返回、客户端显式传回。句柄绑定主体、可过期、逐次授权。藏在连接亲和性里的状态在多副本环境下必然失败——本节的五步失败链条值得背下来。

移除协议会话并不禁止带状态的工作流。服务器可以铸造一个不透明的状态句柄，并作为普通工具结果返回。客户端在后续调用中把这个句柄作为显式参数传入。

把句柄绑定到已认证主体，使其不可猜测、可过期，并对每次使用做授权。这让状态在应用层可见，而不是藏在传输亲和性里。

由隐藏的副本状态导致的失败是机械性的：

1. 请求 A 到达副本 1，在该进程内存中创建草稿。
2. 响应不返回草稿句柄，因为实现假设"连接"能标识草稿。
3. 请求 B 是一次全新的 POST，到达副本 2。
4. 副本 2 持有合法的协议元数据，却无法命名或加载草稿，于是工作流失败或读到错误的本地对象。
5. 粘性路由看似修复了症状，直到某次重启、发布、重调度或故障转移挪走了下一个请求。

正确的边界有两部分。协议上下文留在每个请求里。持久的应用状态存放在共享存储中，由服务器铸造句柄返回给客户端。下一次调用提供该句柄，任意副本都能加载同一条记录，授权把记录绑定到已认证主体和租户。副本内存可以缓存记录，但不能成为正确性所依赖的唯一副本。

按生命周期选择状态机制。请求局部变量可以服务单次调用。短的 MRTR 延续可以使用带完整性保护的 `requestState`。草稿或持久任务需要显式句柄，外加共享持久化、过期、并发控制和幂等性。这些对象没有一个是 MCP 协议会话。

### HTTP 双时代兼容

> **【中文解读】** 兼容策略的黄金法则：先现代 POST，看响应体再定论。能识别的现代 JSON-RPC 错误 = 服务器是现代的，绝不降级；空体/不认识 = 才可能是遗留服务器，才去试旧 GET。迁移期可双轨并存，但描述上绝不能把遗留行为说成 2026-07-28 的一部分。

同时支持现代和遗留服务器的客户端先尝试现代 POST。如果收到 HTTP `400`、`404` 或 `405`，就检查响应体：

- 识别出的现代 JSON-RPC 错误证明服务器是现代的。修正请求或重试一个已公告的版本。绝不降级。
- 空体或无法识别的响应可能表明这是遗留 HTTP+SSE 服务器。只有此时才去尝试旧的 GET 端点并期待它的遗留 `endpoint` 事件。

服务器在迁移期可以同时支持两个时代：把现代元数据路由到现代 POST-only 实现，为老客户端保留独立的遗留端点。绝不要把遗留的 GET、DELETE、会话 id 或重放行为描述为 `2026-07-28` 的一部分。

```figure
tp-transport-handshake
```

## 用框架实现

> **【中文解读】** 示例代码用纯标准库实现了一个可运行的现代 Streamable HTTP 服务器，并用 `--probe` 自检把规范条款逐条变成可验证断言——这是把规范读成测试的好范例。

`code/main.py` 用 Python 标准库实现了一个有限、现代的 Streamable HTTP 服务器。它校验 Origin 和镜像头，忽略已移除的会话头，普通调用返回 JSON，并演示一条有限的 `subscriptions/listen` SSE 流。

```bash
cd code
python3 main.py --probe
python3 -m unittest discover tests -v
```

自检检查以下各项：

- 非法 Origin 被拒绝；
- 无需会话 id 即可完成发现；
- `Mcp-Session-Id` 和 `Last-Event-ID` 被忽略；
- 头不匹配返回 `-32020`；
- 不支持的版本返回 `-32022` 并带精确的 `supported` 和 `requested` 数据；
- 被接受的无 id 通知返回 HTTP `202` 且无主体；
- GET 和 DELETE 返回 `405`；
- `subscriptions/listen` 是一条 POST 响应流，其确认、通知和最终结果都携带订阅 id。

## 产出物

本课产出 `outputs/skill-mcp-transport-migrator.md`。它移除现代协议会话、加入头-体校验、用 `subscriptions/listen` 取代独立 GET，并让任何遗留桥接保持显眼隔离。

## 练习题

1. 从 POST 中移除 `Mcp-Method`。确认 HTTP `400` 和错误 `-32020`。
2. 发送头与体一致的版本 `2027-01-01`。确认 HTTP `400`、错误 `-32022` 和精确数据 `{"supported":["2026-07-28"],"requested":"2027-01-01"}`。
3. 为非 ASCII 资源 URI 发送 Base64 哨兵 `Mcp-Name`。确认解码后的值与 `params.uri` 比对。
4. 在最终响应前打断有限的 listen 流。用新 JSON-RPC id 重新发出并重新拉取工具。
5. 给 ping 工具加一个显式工作流句柄。不用连接亲和性，把它绑定到一个授权主体。

## 术语速查表

| 术语 | 含义 |
|------|------|
| stdio | 客户端启动的子进程上按行分隔的 JSON-RPC |
| Streamable HTTP | 每条现代消息都是一次新 POST 的单一端点 |
| 请求级 SSE 流 | 包含相关通知和最终响应的 POST 响应流 |
| `subscriptions/listen` | 请求选定的变更通知的长生命周期 POST 请求 |
| 头不匹配错误 | 镜像头与请求体不一致时的 HTTP `400` 和 JSON-RPC `-32020` |
| Origin 校验 | 面向进入连接的 DNS 重绑定防御，不是认证 |
| 显式状态句柄 | 作为普通参数传递的应用层令牌，取代隐藏的会话状态 |
| 遗留桥接 | 仅为兼容而保留的、显眼隔离的早期时代行为 |

## 延伸阅读

- [MCP Transport Overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) — 两种现代传输的权威入口
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio) — stdio 传输的完整规范
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) — Streamable HTTP 的 POST-only 契约细节
- [MCP Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions) — `subscriptions/listen` 订阅模式规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — 会话移除的官方变更清单
