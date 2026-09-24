# MCP Resources and Prompts: Addressable Context for Stateless Servers | MCP 资源与提示：无状态服务器的可寻址上下文

> Tools perform operations. Resources expose addressable content. Prompts package user-selected message templates. A good MCP server keeps those contracts separate and predictable.

> **【中文解读】** 三种服务器原语各司其职：tools 执行操作，resources 暴露可寻址的内容，prompts 打包用户选择的消息模板。一个合格的 MCP 服务器让这三份契约彼此分离、可预期。本课还把这三者放进 2026-07-28 的无状态信封：没有初始化握手，每个请求自带协议版本与能力，列表结果确定性排序，缓存提示（`ttlMs`/`cacheScope`）成为正确性的一部分。

> **【拓展：原语三分→真实产品】** 现实中的分工例子：GitHub MCP 把 issue 详情做成资源（URI 可寻址、宿主可附加到上下文），把"创建 issue"做成工具（有副作用），把"代码审查工作流"做成提示模板（用户一键触发）。2026-07-28 的新约束是：资源订阅不再用 `resources/subscribe`，而是统一的 `subscriptions/listen` 请求级响应流——与 Lesson 09 的传输层演进一脉相承。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（构建 MCP 服务器）——tools/list、tools/call 的实现；(2) Phase 13·09（MCP 传输层）——无状态信封、`_meta` 键、`subscriptions/listen` 的传输背景；(3) URI 概念（`file://`、自定义 scheme）；(4) 若学过旧版（`resources/subscribe` 订阅），注意该方法已属遗留时代。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lesson 07 (Building an MCP Server), Phase 13, Lesson 09 (MCP Transports) | **前置知识:** Phase 13 · 07（构建 MCP 服务器）、Phase 13 · 09（MCP 传输层）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Learning Objectives | 学习目标

- Choose among tools, resources, and prompts from the consumer's intent.
  中文翻译：从消费者意图出发，在工具、资源和提示之间做选择。
- Advertise the resource and prompt surface through mandatory `server/discover`.
  中文翻译：通过强制的 `server/discover` 公告资源与提示能力面。
- Build deterministic `resources/list` and `prompts/list` results.
  中文翻译：构建确定性的 `resources/list` 和 `prompts/list` 结果。
- Apply `ttlMs` and `cacheScope` without leaking user-specific data.
  中文翻译：应用 `ttlMs` 和 `cacheScope` 而不泄漏用户特定数据。
- Return JSON-RPC error `-32602` for an invalid or unknown resource URI.
  中文翻译：对无效或未知的资源 URI 返回 JSON-RPC 错误 `-32602`。
- Open a `subscriptions/listen` POST-response stream and correlate every event by subscription ID.
  中文翻译：打开 `subscriptions/listen` 的 POST 响应流，并按订阅 ID 关联每个事件。
- Treat resource content and prompt templates as untrusted server output.
  中文翻译：把资源内容和提示模板当作不可信的服务器输出。

## Start With the Consumer | 从消费者出发

> **【中文解读】** 误用 MCP 的最简单方式是从实现代码出发："这是个函数所以做成 tool""这是个文件所以做成 resource"。正确起点是"谁在选择、他期待什么"：模型/应用执行操作选 tool；宿主、应用或用户读取 URI 内容选 resource；用户通过宿主 UI 启动可复用消息工作流选 prompt。不要为了一种能力同时暴露三种原语——每个多出来的能力面都要付出发现、授权、缓存、错误处理、测试和文档的代价。

The easiest way to misuse MCP is to begin with implementation code. A database query becomes a tool because functions are familiar. A reusable workflow becomes a resource because it is stored in a file. A prompt becomes hidden policy because the host can inject it.

> 误用 MCP 的最简单方式是从实现代码出发。数据库查询成了 tool，因为函数让人熟悉。可复用工作流成了 resource，因为它存在文件里。prompt 成了隐藏策略，因为宿主可以注入它。

Begin with who chooses and what they expect.

> 从"谁在选择、他期待什么"开始。

| Primitive | Primary intent | Selection owner | Typical result |
|---|---|---|---|
| Tool | Perform an operation | Model or application | Structured action result |
| Resource | Read content at a URI | Host, application, or user | Text or binary content |
| Prompt | Start a reusable message workflow | User through host UI | One or more prompt messages |

A note at `notes://note-1` is a resource because it is addressable content. `delete_note` is a tool because it changes state. `review_note` is a prompt because a user chooses a prepared review workflow.

> `notes://note-1` 上的笔记是资源，因为它是可寻址的内容。`delete_note` 是工具，因为它改变状态。`review_note` 是提示，因为用户选择的是一个预制的审查工作流。

Do not expose one operation as all three merely to look complete. Each extra surface needs discovery, authorization, caching, error handling, tests, and documentation.

> 不要仅为显得完整就把一个操作同时暴露为三种原语。每个多出来的能力面都需要发现、授权、缓存、错误处理、测试和文档。

> 💡 **【类比】** 三原语像图书馆的三种资源：tools 是借阅台工作人员——你请他办事（查书、办卡），他执行动作、有副作用；resources 是书架上的书——URI 就是索书号，宿主可以直接取来附到上下文里，不需要每次请示；prompts 是馆内"自助导览路线"——预制好的多步骤流程，用户按一个按钮就走完全程。把书当工作人员用是浪费，把工作人员当书用是错配。

## The 2026-07-28 Stateless Envelope | 2026-07-28 无状态信封

> **【中文解读】** 本课面向 MCP 协议修订版 2026-07-28 的无状态档位：没有初始化握手、没有协议会话，每个请求用保留的 `_meta` 键自带协议版本和客户端能力。服务器必须实现 `server/discover`，其结果公告支持的版本、资源与提示能力、实现身份和缓存提示。正常结果声明 `"resultType": "complete"`；不支持的修订返回 `-32022` 并同时给出请求的修订和服务器支持的修订。设计直觉随之改变：列表不能依赖同一连接上的先前调用；授权可以改变可见集合（凭证是请求输入），但连接历史不能。

This lesson targets MCP protocol revision `2026-07-28`. There is no initialization handshake or protocol session in this profile. Every request carries its protocol version and client capabilities in reserved `_meta` keys.

> 本课面向 MCP 协议修订版 `2026-07-28`。该档位没有初始化握手，也没有协议会话。每个请求在保留的 `_meta` 键中携带自己的协议版本和客户端能力。

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

A server must implement `server/discover`. Its result advertises supported
versions, resource and prompt capabilities, implementation identity, and
cache hints. A client may call another method directly, but discovery gives it
one stable snapshot before it builds a UI.

> 服务器必须实现 `server/discover`。其结果公告支持的版本、资源与提示能力、实现身份和缓存提示。客户端可以直接调用其他方法，但发现能让它在构建 UI 之前拿到一份稳定的快照。

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "resources": {"listChanged": true, "subscribe": true},
    "prompts": {"listChanged": true}
  },
  "ttlMs": 3600000,
  "cacheScope": "public"
}
```

A normal result declares `"resultType": "complete"`. The response `_meta` identifies the serving implementation with `io.modelcontextprotocol/serverInfo`. This information is useful for diagnostics. It is not an authentication identity. A request carrying an unsupported revision returns `-32022` with both the requested revision and the server's supported revisions.

> 正常结果声明 `"resultType": "complete"`。响应 `_meta` 用 `io.modelcontextprotocol/serverInfo` 标识提供服务的实现。这些信息对诊断有用，但不是认证身份。携带不支持修订的请求返回 `-32022`，同时给出请求的修订和服务器支持的修订。

The stateless contract changes your design instincts. A list cannot depend on a prior call on one connection. Authorization may change the visible set because credentials are request input, but connection history must not.

> 无状态契约会改变你的设计直觉。列表不能依赖同一连接上的先前调用。授权可以改变可见集合，因为凭证是请求输入，但连接历史不能。

## Resources Are Stable URI Contracts | 资源是稳定的 URI 契约

> **【中文解读】** 资源是由 URI 标识的内容——先设计 URI，再写处理器。好 URI 的性质：足够稳定可收藏、按服务器域名命名空间化、独立于进程 ID 或连接、存储访问前先校验、每次读取都过授权。`resources/list` 返回调用者当前可见的资源，按稳定键（如 URI）排序——确定性排序能避免缓存噪声、快照漂移和宿主 UI 跳动。`resources/read` 对未知 URI 不返回"成功的空读"，而是 `-32602`，让客户端能区分"不存在"与"合法的空文档"。

A resource is content identified by a URI. Design the URI before the handler.

> 资源是由 URI 标识的内容。先设计 URI，再写处理器。

Good URI properties:

> 好 URI 的性质：

- Stable enough to bookmark or pass between requests.
  中文翻译：足够稳定，可收藏或在请求间传递。
- Namespaced to the server's domain.
  中文翻译：按服务器域名做命名空间。
- Independent from a process ID or connection.
  中文翻译：独立于进程 ID 或连接。
- Validated before storage access.
  中文翻译：在访问存储之前先校验。
- Authorized on every read.
  中文翻译：每次读取都做授权。

`notes://note-1` is better than `note-1` because its namespace is explicit. A file server may use `file://` URIs, but it must still check configured directory boundaries after resolving symlinks and relative segments.

> `notes://note-1` 优于 `note-1`，因为它的命名空间是显式的。文件服务器可以用 `file://` URI，但在解析符号链接和相对段之后，仍必须检查配置的目录边界。

`resources/list` returns the resources currently visible to the caller. Sort by a stable key such as URI. Deterministic order prevents noisy cache misses, changing snapshots, and host UIs that jump between refreshes.

> `resources/list` 返回调用者当前可见的资源。按稳定键（如 URI）排序。确定性排序可防止嘈杂的缓存未命中、不断变化的快照，以及在两次刷新之间跳来跳去的宿主 UI。

```json
{
  "resultType": "complete",
  "resources": [
    {
      "uri": "notes://note-1",
      "name": "Architecture decision",
      "description": "Why the service uses a stateless boundary",
      "mimeType": "text/markdown"
    }
  ],
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

`resources/read` returns one or more content items. An unknown URI is not a successful empty read. The current Resources specification assigns invalid or unknown resource URIs to JSON-RPC invalid parameters, code `-32602`.

> `resources/read` 返回一个或多个内容项。未知 URI 不等于一次成功的空读。现行 Resources 规范把无效或未知的资源 URI 归入 JSON-RPC 无效参数，错误码 `-32602`。

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Unknown or invalid resource URI",
    "data": {
      "uri": "notes://missing"
    }
  }
}
```

That distinction lets a client separate absence from a valid empty document. It also prevents accidental fallback to a broader lookup.

> 这一区别让客户端能把"不存在"与"合法的空文档"分开。它还防止意外回退到更宽泛的查找。

### Resource templates

> **【中文解读】** 资源模板描述一族参数化 URI，适用于"列出每个具体项代价高昂或无上界"的场景。模板不放松校验：解析变量、过授权、限长度和字符集、用类型化参数构造存储查询——绝不把任意 URI 尾巴拼进文件路径或数据库语句。

A resource template describes a family of parameterized URIs. Use one when listing every concrete item would be expensive or unbounded. For example, `notes://projects/{project}/decisions/{decision}` tells a client how to form a valid address without returning every decision.

> 资源模板描述一族参数化的 URI。当列出每个具体项代价高昂或无上界时使用。例如 `notes://projects/{project}/decisions/{decision}` 告诉客户端如何构造合法地址，而不用返回每一条决策。

A template does not weaken validation. Parse variables, apply authorization, enforce length and character limits, and construct storage queries with typed parameters. Never concatenate an arbitrary URI tail into a filesystem path or database statement.

> 模板不会放松校验。解析变量、应用授权、强制长度和字符限制，并用类型化参数构造存储查询。绝不要把任意 URI 尾巴拼接进文件系统路径或数据库语句。

### Content is not trusted instruction

> ⚠️ **【易错点】** 场景：把资源文本当指令执行，或让 prompt 成为绕过资源授权的旁路 / 后果：资源文本可能含提示注入、秘密、误导性命令或畸形标记；未授权的字段泄漏给调用者 / 修复：宿主保留出处信息并把资源内容当数据；服务器限制内容大小、返回准确 MIME 类型、脱敏调用者无权访问的字段、不返回无关记录；prompt 的 URI 参数过与直接资源读取相同的授权检查。

Resource text may contain prompt injection, secrets, misleading commands, or malformed markup. The host should preserve provenance and treat resource content as data. The server should limit content size, return an accurate MIME type, redact fields the caller cannot access, and avoid returning unrelated records.

> 资源文本可能包含提示注入、秘密、误导性命令或畸形标记。宿主应保留出处信息并把资源内容当作数据。服务器应限制内容大小、返回准确的 MIME 类型、脱敏调用者无权访问的字段，并避免返回无关记录。

## Prompts Are User-Controlled Templates | 提示是用户控制的模板

> **【中文解读】** MCP prompts 面向显式的用户选择：宿主可以渲染成斜杠命令、菜单项或工作流按钮，协议不限定 UI。`prompts/list` 对相同请求授权应保持确定性；每个提示要有稳定名称、有用描述和参数声明，让宿主在 `prompts/get` 之前收集输入。`prompts/get` 把参数解析成消息，但不取代宿主的系统指令——宿主决定返回的消息如何进入模型上下文，并让自己的可信策略保持更高优先级。在服务器边界校验提示参数；提示 URI 要通过与直接资源读取相同的授权检查，别让提示变成绕过资源访问的旁路。

MCP prompts are designed for explicit user selection. A host may render them as slash commands, menu items, or workflow buttons. The protocol does not require one UI.

> MCP prompts 为显式的用户选择而设计。宿主可以把它们渲染成斜杠命令、菜单项或工作流按钮。协议不要求某种特定 UI。

`prompts/list` should be deterministic for the same request authorization. Each prompt needs a stable name, a useful description, and argument declarations that let the host collect input before `prompts/get`.

> `prompts/list` 对相同的请求授权应保持确定性。每个提示需要稳定的名称、有用的描述和参数声明，让宿主能在 `prompts/get` 之前收集输入。

```json
{
  "resultType": "complete",
  "prompts": [
    {
      "name": "review_note",
      "title": "Review a note",
      "description": "Review one note for a named concern",
      "arguments": [
        {
          "name": "uri",
          "description": "The note resource URI",
          "required": true
        }
      ]
    }
  ],
  "ttlMs": 600000,
  "cacheScope": "public"
}
```

`prompts/get` resolves arguments into messages. It does not replace the host's system instructions. The host decides how returned messages enter model context and keeps its own trusted policy at higher priority.

> `prompts/get` 把参数解析成消息。它不取代宿主的系统指令。宿主决定返回的消息如何进入模型上下文，并让自己的可信策略保持更高优先级。

Validate prompt arguments at the server boundary. A prompt URI should pass the same authorization check as a direct resource read. Do not make a prompt a side channel around resource access.

> 在服务器边界校验提示参数。提示 URI 应通过与直接资源读取相同的授权检查。不要让提示成为绕过资源访问的旁路。

## Cache Hints Are Part of Correctness | 缓存提示是正确性的一部分

> **【中文解读】** `ttlMs` 告诉客户端结果可复用多久，`cacheScope` 描述谁可以共享缓存值。MCP 只定义 `public` 和 `private` 两种 `cacheScope`；携带秘密或快速变化的结果用 `private` + `ttlMs: 0`，更严格的 no-store 规则由宿主缓存策略实现——`no-store` 不是 MCP 的 `cacheScope` 值。缓存提示永远不能取代授权：缓存键必须包含所有改变可见性的请求维度（租户、用户、范围、语言、分页游标）；共享缓存表达不了这些维度时，就用 `private` + 零 TTL + 宿主级 no-store。

`ttlMs` tells a client how long a result may be reused. `cacheScope` describes who may share that cached value.

> `ttlMs` 告诉客户端一个结果可以被复用多久。`cacheScope` 描述谁可以共享该缓存值。

| Scope | Meaning | Typical use |
|---|---|---|
| `public` | May be reused across users when authorization permits | Public prompt catalog |
| `private` | Bound to the requesting user or credential context | User-owned note content |

Choose a TTL from the data's change rate and the damage of staleness. Five minutes may suit a public prompt catalog. A private note read may use one minute.

> 依据数据的变化速率和过时的代价选择 TTL。公共提示目录五分钟可能合适；私人笔记读取可能用一分钟。

MCP defines only `public` and `private` as `cacheScope` values. For a secret-bearing or rapidly changing result, return `cacheScope: "private"` with `ttlMs: 0`, then apply any stricter no-store rule in the host cache policy. `no-store` itself is not an MCP `cacheScope` value.

> MCP 只定义 `public` 和 `private` 作为 `cacheScope` 值。对携带秘密或快速变化的结果，返回 `cacheScope: "private"` 加 `ttlMs: 0`，然后在宿主缓存策略中应用任何更严格的 no-store 规则。`no-store` 本身不是 MCP 的 `cacheScope` 值。

Cache hints never replace authorization. A cache key must include every request dimension that changes visibility, including tenant, user, scope, locale, and pagination cursor. If a shared cache cannot express those dimensions safely, use `private` with a zero TTL and a host-level no-store policy.

> 缓存提示永远不能取代授权。缓存键必须包含每一个改变可见性的请求维度，包括租户、用户、范围、语言和分页游标。如果共享缓存无法安全表达这些维度，就使用 `private` 加零 TTL 和宿主级 no-store 策略。

## Subscriptions Use a Client-Opened Response Stream | 订阅使用客户端打开的响应流

> **【中文解读】** 现代订阅模式取代了旧的 `resources/subscribe` RPC 和旧的 HTTP GET 事件端点。客户端把 `subscriptions/listen` 作为普通 JSON-RPC 请求发出；在 Streamable HTTP 上，这是一个 POST，其响应保持打开成为 SSE 流。`notifications` 对象是允许清单——服务器不得投递未被请求的通知类型。请求 ID 就是订阅 ID；在任何被请求的事件之前，服务器先发 `notifications/subscriptions/acknowledged`，其过滤器只含服务器接受的子集；流上后续每个事件都携带相同的 `subscriptionId` 元数据。通知只说"资源变了"，客户端要通过 `resources/read` 重新读取并重新过当前授权——不要假设事件里带着新文档。不要把订阅流当协议会话用：后续读取仍是可落到任意健康实例的完整请求。

The modern subscription pattern replaces the former `resources/subscribe` RPC and the old HTTP GET event endpoint.

> 现代订阅模式取代了先前的 `resources/subscribe` RPC 和旧的 HTTP GET 事件端点。

The client sends `subscriptions/listen` as a normal JSON-RPC request. Over Streamable HTTP this is a POST whose response remains open as an SSE stream. The `notifications` object is an allowlist. A server must not deliver notification types that were not requested.

> 客户端把 `subscriptions/listen` 作为普通 JSON-RPC 请求发送。在 Streamable HTTP 上，这是一个 POST，其响应保持打开成为 SSE 流。`notifications` 对象是允许清单。服务器不得投递未被请求的通知类型。

```json
{
  "jsonrpc": "2.0",
  "id": 17,
  "method": "subscriptions/listen",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    },
    "notifications": {
      "resourcesListChanged": true,
      "promptsListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

The request ID is the subscription ID. Before any requested event, the server sends `notifications/subscriptions/acknowledged`. Its filter contains only the subset the server accepted.

> 请求 ID 就是订阅 ID。在任何被请求的事件之前，服务器发送 `notifications/subscriptions/acknowledged`。其过滤器只包含服务器接受的子集。

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/acknowledged",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "notifications": {
      "resourcesListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

Every later event on that stream carries the same metadata.

> 该流上后续的每个事件都携带相同的元数据。

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "uri": "notes://note-1"
  }
}
```

The notification says the resource changed. The client reads it again through `resources/read`, subject to current authorization. It does not assume the event contains the new document.

> 通知说的是"资源变了"。客户端通过 `resources/read` 重新读取，并接受当前授权的约束。它不假设事件里包含新文档。

Several subscriptions can share one stdio channel. The subscription ID lets the client demultiplex them. Over HTTP, closing the response stream cancels the subscription. A server that ends the stream gracefully returns a final `resultType: "complete"` response correlated to the original request.

> 多个订阅可以共享一条 stdio 通道。订阅 ID 让客户端能对它们做分流。在 HTTP 上，关闭响应流即取消订阅。优雅结束流的服务器返回一个与原始请求关联的最终 `resultType: "complete"` 响应。

Do not use a subscription stream as a protocol session. A later read is still a complete request that can reach any healthy server instance.

> 不要把订阅流当协议会话用。后续读取仍是可到达任意健康服务器实例的完整请求。

```figure
t3-primitive-sort
```

## Interactive Lab | 互动练习

Use the figure to classify five capabilities from a project tracker: issue details, create issue, sprint review template, project policy, and close issue. Then decide which lists can be cached publicly, which reads must remain private, and which resources deserve update notifications.

> 用图对项目跟踪器的五种能力分类：issue 详情、创建 issue、迭代评审模板、项目政策、关闭 issue。然后决定哪些列表可以公开缓存、哪些读取必须保持私有、哪些资源值得更新通知。

For every classification, name the chooser. If the model performs an action, use a tool. If a host reads URI-addressed content, use a resource. If the user starts a prepared message workflow, use a prompt.

> 对每个分类，说出"谁在选择"。模型执行动作用工具；宿主读取 URI 寻址的内容用资源；用户启动预制消息工作流用提示。

## Practice Lab | 实践练习

> **【中文解读】** 按给定顺序检查转录：发现公告当前修订和两种能力；两个列表结果有序且 `resultType: "complete"`；列表和读取结果带刻意设置的缓存提示；把读取 URI 改成 `notes://missing` 观察 `-32602`；订阅确认先于资源事件；事件与优雅关闭都携带订阅 ID 5。注意：Python 模型不开真实 HTTP 连接，它呈现的是 SDK 必须放到请求级响应流上的消息；生产环境用官方 SDK 做组帧与传输。

Run the simulator from the repository root:

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

Inspect the transcript in this order:

1. Confirm `server/discover` advertises the current revision and both capabilities.
   中文翻译：确认 `server/discover` 公告当前修订和两种能力。
2. Confirm both list results are sorted and use `resultType: "complete"`.
   中文翻译：确认两个列表结果有序且使用 `resultType: "complete"`。
3. Confirm the list and read results carry intentional cache hints.
   中文翻译：确认列表和读取结果带有刻意设置的缓存提示。
4. Change the read URI to `notes://missing` and observe `-32602`.
   中文翻译：把读取 URI 改成 `notes://missing`，观察 `-32602`。
5. Confirm the subscription acknowledgment precedes the resource event.
   中文翻译：确认订阅确认先于资源事件。
6. Confirm the event and graceful close both carry subscription ID `5`.
   中文翻译：确认事件与优雅关闭都携带订阅 ID `5`。

The Python model does not open a real HTTP connection. It represents the messages an SDK must place on the request-scoped response stream. Use an official SDK for framing and transport in production.

> Python 模型不开真实的 HTTP 连接。它呈现的是 SDK 必须放到请求级响应流上的消息。生产环境中用官方 SDK 做组帧和传输。

## Shipped Artifact | 产出物

`outputs/skill-primitive-splitter.md` is a reusable design review for MCP primitive selection. It now checks deterministic discovery, cache scope, invalid URI behavior, and modern subscription filters.

> `outputs/skill-primitive-splitter.md` 是一份可复用的 MCP 原语选择设计评审。它现在检查确定性发现、缓存范围、无效 URI 行为和现代订阅过滤器。

The lesson also ships `assets/primitive-split.svg`, a static version of the primitive and subscription boundary for offline study.

> 本课还附带 `assets/primitive-split.svg`，是原语与订阅边界的静态版本，供离线学习。

## Verify It | 验证

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

Expected result: the main program prints a JSON transcript and the test command reports at least twelve passing tests.

> 预期结果：主程序打印一份 JSON 转录，测试命令报告至少十二个通过的测试。

## Capstone Connection | 毕业项目衔接

Use this contract when your capstone server exposes addressable knowledge beside actions. Include one deterministic catalog snapshot, one authorized resource read, one prompt resolution, one invalid URI case, and one subscription transcript.

> 当你的毕业项目服务器在动作之外暴露可寻址知识时，使用本契约。包含一份确定性目录快照、一次授权的资源读取、一次提示解析、一个无效 URI 用例和一份订阅转录。

Your evidence should show that no list depends on connection history and that a subscription event never grants access to the underlying resource.

> 你的证据应表明：没有任何列表依赖连接历史，且订阅事件绝不授予对底层资源的访问。

## Exercises | 练习题

1. Add a `notes://projects/{project}/notes/{id}` resource template and validate both variables.
   中文翻译：添加 `notes://projects/{project}/notes/{id}` 资源模板并校验两个变量。
2. Add pagination to `resources/list` while preserving deterministic order.
   中文翻译：给 `resources/list` 加分页，同时保持确定性排序。
3. Change one resource to `cacheScope: "private"` with `ttlMs: 0`, add a host-level no-store policy, and explain the threat that justifies both controls.
   中文翻译：把一个资源改为 `cacheScope: "private"` 加 `ttlMs: 0`，添加宿主级 no-store 策略，并解释同时需要这两个控件的威胁模型。
4. Add a prompt-list change subscription and prove no event is sent when the filter omits `promptsListChanged`.
   中文翻译：添加提示列表变更订阅，并证明过滤器省略 `promptsListChanged` 时不发送事件。
5. Create two simultaneous subscriptions and prove each event carries the correct request ID.
   中文翻译：创建两个同时存在的订阅，证明每个事件携带正确的请求 ID。
6. Add an authorization subject to the read handler and prove a cache entry cannot cross subjects.
   中文翻译：给读取处理器加授权主体，并证明缓存条目不能跨主体。

## Key Terms | 术语速查表

- **Resource:** URI-addressed content exposed by an MCP server.
  中文翻译：资源——MCP 服务器暴露的 URI 寻址内容。
- **Prompt:** A user-controlled message template exposed by an MCP server.
  中文翻译：提示——MCP 服务器暴露的用户控制消息模板。
- **Deterministic list:** A discovery result with stable membership and ordering for the same request inputs.
  中文翻译：确定性列表——对相同请求输入具有稳定成员和排序的发现结果。
- **`ttlMs`:** Cache freshness duration in milliseconds.
  中文翻译：缓存新鲜期，单位毫秒。
- **`cacheScope`:** The sharing boundary for a cached result.
  中文翻译：缓存结果的共享边界。
- **`subscriptions/listen`:** A long-lived request whose response stream delivers explicitly filtered notifications.
  中文翻译：长生命周期请求，其响应流投递经过显式过滤的通知。
- **Subscription ID:** The original listen request ID, repeated in notification metadata.
  中文翻译：订阅 ID——原始 listen 请求 ID，在通知元数据中重复出现。
- **Invalid parameters:** JSON-RPC error `-32602`, used for an invalid or unknown resource URI.
  中文翻译：无效参数——JSON-RPC 错误 `-32602`，用于无效或未知的资源 URI。
- **Unsupported protocol version:** JSON-RPC error `-32022`, including `supported` and `requested` revisions.
  中文翻译：不支持的协议版本——JSON-RPC 错误 `-32022`，包含 `supported` 和 `requested` 修订。
- **`server/discover`:** Mandatory server method that returns supported revisions, capabilities, identity, and optional cache hints.
  中文翻译：强制的服务器方法，返回支持的修订、能力、身份和可选的缓存提示。

## Further Reading | 延伸阅读

- [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  中文翻译：资源契约的权威规范（列表、读取、模板、`-32602` 语义）
- [MCP 2026-07-28 Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  中文翻译：提示契约的权威规范
- [MCP 2026-07-28 Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  中文翻译：`subscriptions/listen` 订阅模式规范
- [MCP 2026-07-28 Caching](https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/caching)
  中文翻译：`ttlMs`/`cacheScope` 缓存提示语义
