# Explicit Scope and Stateless Elicitation | 显式作用域与无状态诱导输入

> Roots are deprecated in MCP 2026-07-28 and were never a security sandbox. Put scope in visible tool arguments or resource URIs, authorize it on the server, and use MRTR when a tool genuinely needs user input. The user sees the decision, the model sees the handle, and any server instance can process the retry.

> **【中文解读】** 本课的主题在 MCP 2026-07-28 版本中发生了根本变化：Roots（根范围）被正式废弃——它从来就不是安全沙箱；作用域信息必须显式出现在工具参数或资源 URI 里，由服务器负责授权；elicitation（诱导输入）仍然存在，但当工具真的需要用户输入时，改用 MRTR（多轮往返请求）交付。用户能看到决策，模型能看到句柄，任何服务器实例都能处理重试。

> **【拓展：显式作用域→可审计的 MCP 安全模型】** 把作用域从隐藏的传输会话状态搬进可见的请求参数，换来的是可检查、可重放、可审计、可路由——这与 REST 的无状态约束一脉相承：一切影响行为的信息都在报文里。授权归服务器、路径包含检查防目录穿越、操作系统沙箱兜底，三层缺一不可。本课与 Phase 13·11（无状态 MRTR）和 Phase 13·15（MCP 安全）构成一条完整线索。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）——工具调用与能力协商的基本形态；(2) Phase 13·11（stateless MRTR）——`input_required` 结果、`requestState` 回传、无会话重试机制，本课的 elicitation 完全建立在它之上；(3) 基础的路径/URI 知识（百分号编码、路径组件、符号链接）。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 11 (stateless MRTR) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 11（无状态 MRTR）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Learning Objectives | 学习目标

- Replace deprecated Roots with explicit workspace parameters, resource URIs, or server configuration.
  中文翻译：用显式的工作区参数、资源 URI 或服务器配置取代已废弃的 Roots。
- Separate scope hints from authorization, path containment, and operating-system sandboxing.
  中文翻译：把作用域提示与授权、路径包含检查、操作系统沙箱区分开来。
- Deliver form-mode `elicitation/create` through an MRTR `input_required` result.
  中文翻译：通过 MRTR `input_required` 结果交付表单模式的 `elicitation/create`。
- Advertise elicitation support in per-request client capabilities and reject unsupported modes.
  中文翻译：在按请求的客户端能力中声明 elicitation 支持，并拒绝不支持的模式。
- Validate `accept`, `decline`, and `cancel` as distinct outcomes.
  中文翻译：把 `accept`、`decline` 和 `cancel` 当作三种不同的结局来验证。
- Bind destructive confirmation to an authenticated principal, original arguments, candidate set, and expiry.
  中文翻译：把破坏性确认绑定到已认证主体、原始参数、候选集和过期时间。

## Two Problems That Look Similar | 看似相似的两个问题

A notes tool receives this request: "Delete the old TPS report."

> 一个笔记工具收到这样的请求："删除旧的 TPS 报告。"

The server must answer two different questions.

> 服务器必须回答两个不同的问题。

1. Which workspace may this operation touch?
   中文翻译：这个操作可以触碰哪个工作区？
2. Which of three matching notes did the user mean?
   中文翻译：三条匹配的笔记里用户指的是哪一条？

The first is scope and authorization. The second is interactive disambiguation. Mixing them leads to dangerous designs, such as treating a client-provided folder as proof that the caller may delete everything inside it.

> 第一个是作用域与授权问题。第二个是交互式消歧义。把两者混在一起会导致危险的设计——比如把客户端提供的文件夹当作"调用者可以删除其中一切"的证明。

> **【中文解读】** 作用域（我能碰哪里）与消歧义（用户指哪个）是两个正交的问题。前者由服务器授权决定，后者需要用户输入。旧版 MCP 用 Roots 表达前者、用反向 elicitation 请求表达后者；2026-07-28 把两者都改成了显式、无状态的形式：作用域进参数，用户输入进 MRTR 重试。

## Roots Are a Migration Surface | Roots 是一个迁移面

Earlier MCP revisions let a client advertise Roots and notify a server when the list changed. Roots were informational guidance. They did not constrain what the server process could read, did not authorize the caller, and did not create an operating-system sandbox.

> 更早的 MCP 修订版允许客户端声明 Roots 并在列表变化时通知服务器。Roots 是信息性指引。它们不约束服务器进程能读什么、不给调用者授权、也不构成操作系统沙箱。

MCP 2026-07-28 deprecates `roots/list` and `notifications/roots/list_changed` for new designs. Prefer one of these explicit replacements:

> MCP 2026-07-28 对新设计废弃了 `roots/list` 和 `notifications/roots/list_changed`。优先选用以下显式替代方案：

- A `workspaceUri` or `directory` tool argument when scope varies per call.
  中文翻译：作用域随调用变化时，用 `workspaceUri` 或 `directory` 工具参数。
- A resource URI when the operation already targets a resource.
  中文翻译：操作本来就针对某个资源时，用资源 URI。
- Server configuration when one deployment owns one fixed workspace.
  中文翻译：一个部署只拥有一个固定工作区时，用服务器配置。
- A process sandbox or jailed filesystem when code must be technically unable to escape.
  中文翻译：当代码必须在技术上无法越界时，用进程沙箱或受限文件系统。

If an existing 2026-07-28 integration still needs `roots/list` during the deprecation window, the server embeds it in MRTR `inputRequests`. It must not send a live reverse request. That is a migration adapter; new handlers should accept explicit scope instead.

> 如果现有的 2026-07-28 集成在废弃窗口内仍需要 `roots/list`，服务器要把它嵌入 MRTR `inputRequests` 中。它不得发送活跃的反向请求。那是迁移适配器；新的处理器应当接受显式作用域。

The model can see and repeat an explicit handle. Hidden transport-session scope is harder to inspect, replay, audit, and route.

> 模型能看到并重复一个显式句柄。隐藏的传输会话作用域更难检查、重放、审计和路由。

> 💡 **【类比】** Roots 像客人进门时口头说"我只去客厅"——主人听了但不锁门；显式作用域像每张出入证上都印着房间号，门禁系统（服务器授权）逐间验票。前者只是"提示"，后者才是"凭证"。旧版把提示当边界用；新版要求把边界写成请求里看得见的参数，再由服务器真正执行授权检查。

### The three-layer rule

An explicit URI still does not authorize itself. Enforce all three layers:

> 显式 URI 本身仍不能自我授权。三层都要执行：

1. **Authorization:** Is this authenticated principal allowed to use this workspace?
   中文翻译：**授权：** 这个已认证主体是否被允许使用这个工作区？
2. **Containment:** Does the normalized target URI stay inside the authorized workspace boundary?
   中文翻译：**包含检查：** 归一化后的目标 URI 是否仍在授权工作区的边界内？
3. **Sandbox:** Can the operating system stop a compromised server from escaping anyway?
   中文翻译：**沙箱：** 操作系统是否仍能拦住一个已被攻破的服务器越界？

The runnable server keeps an allowlist of authorized workspace URIs, normalizes percent-encoded paths, checks a real path-component boundary, and re-checks containment immediately before deletion.

> 可运行的服务器维护一份已授权工作区 URI 的白名单，归一化百分号编码的路径，检查真实的路径组件边界，并在删除前一刻重新检查包含关系。

Naive string-prefix checks are wrong:

> 朴素的前缀字符串检查是错的：

```text
allowed:   file:///work/notes
attacker:  file:///work/notes-evil/secret.md
traversal: file:///work/notes/%2e%2e/private.md
```

Both hostile paths start with a misleading string. Normalize first, then compare path components. A production filesystem server must also defend against symbolic-link races and platform-specific path semantics.

> 两个恶意路径都以误导性的字符串开头。先归一化，再比较路径组件。生产环境的文件系统服务器还必须防御符号链接竞争和平台特定的路径语义。

> ⚠️ **【易错点】** 场景：用 `uri.startswith(workspace)` 做包含检查 / 后果：`file:///work/notes-evil/secret.md`（前缀撞车）和 `file:///work/notes/%2e%2e/private.md`（编码穿越）都能通过检查，造成越界读写 / 修复：先 `unquote` 归一化，再拆成路径组件逐段比较边界，删除前再查一次；真实文件系统实现还要防符号链接竞争（TOCTOU 窗口）。

## Elicitation Still Exists, but Delivery Changed | Elicitation 仍在，但交付方式变了

> **【中文解读】** 这是本课最大的变化点：elicitation 的方法名还是 `elicitation/create`，但线上流转方向反了。旧版（2025-11-25）服务器在工具调用中途发出一个反向 JSON-RPC 请求，需要一个活跃会话；2026-07-28 的服务器直接返回 `resultType: "input_required"` 结果，把表单请求装进 `inputRequests`，客户端渲染表单、收集答案后带着 `inputResponses` 用全新的 id 重试 `tools/call`。两次调用之间没有协议会话——状态由签名的 `requestState` 携带。

Elicitation is the current client feature for collecting user input during `tools/call`, `prompts/get`, or `resources/read`. The method name remains `elicitation/create`. What changed is the direction of the wire flow.

> Elicitation 是在 `tools/call`、`prompts/get` 或 `resources/read` 期间收集用户输入的现行客户端特性。方法名仍是 `elicitation/create`。变的是线上流转的方向。

A 2026-07-28 server does not send a reverse JSON-RPC request. It returns an `InputRequiredResult`:

> 2026-07-28 服务器不发送反向 JSON-RPC 请求。它返回一个 `InputRequiredResult`：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "delete_choice": {
        "method": "elicitation/create",
        "params": {
          "mode": "form",
          "message": "Choose one matching note and confirm deletion.",
          "requestedSchema": {
            "type": "object",
            "properties": {
              "note_id": {
                "type": "string",
                "enum": ["note-3", "note-7", "note-14"]
              },
              "confirm": {"type": "boolean"}
            },
            "required": ["note_id", "confirm"]
          }
        }
      }
    },
    "requestState": "integrity-protected-delete-state"
  }
}
```

The host renders the form. The user can accept, explicitly decline, or dismiss it. The client then retries the original `tools/call` with a fresh id:

> 宿主渲染表单。用户可以接受、明确拒绝或关闭它。然后客户端用一个全新的 id 重试原始的 `tools/call`：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "notes_delete",
    "arguments": {
      "workspaceUri": "file:///Users/alice/Documents/Notes",
      "title": "TPS report"
    },
    "inputResponses": {
      "delete_choice": {
        "action": "accept",
        "content": {"note_id": "note-14", "confirm": true}
      }
    },
    "requestState": "integrity-protected-delete-state",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {"form": {}}
      }
    }
  }
}
```

There is no protocol session between the two calls. The server verifies the echoed state, validates the response against the expected schema, checks that the selected note was in the signed candidate set, re-authorizes the workspace, re-checks containment, and then deletes.

> 两次调用之间没有协议会话。服务器验证回传的状态、按预期 schema 校验响应、检查所选笔记确实在签名的候选集里、重新授权工作区、重新检查包含关系，然后才删除。

## Capability Negotiation Is Per Request | 能力协商按请求进行

A client that supports form-mode elicitation declares:

> 支持表单模式 elicitation 的客户端这样声明：

```json
{
  "io.modelcontextprotocol/clientCapabilities": {
    "elicitation": {"form": {}}
  }
}
```

An empty elicitation capability, `"elicitation": {}`, remains equivalent to form-only support for compatibility. Explicit `"elicitation": {"form": {}}` also supports form mode. A URL-only declaration, `"elicitation": {"url": {}}`, does not. The server must not embed a mode absent from the current request's capabilities, even if an earlier request advertised it.

> 空的 elicitation 能力 `"elicitation": {}` 出于兼容性仍等价于仅支持表单。显式的 `"elicitation": {"form": {}}"` 同样支持表单模式。仅 URL 的声明 `"elicitation": {"url": {}}"` 则不支持。服务器不得嵌入当前请求能力中不存在的模式，即使更早的请求声明过它。

Every request also carries `io.modelcontextprotocol/protocolVersion`. A missing or non-string version returns `-32602`. An unsupported string returns `-32022` with exact `supported` and `requested` data. Missing or URL-only elicitation support returns `-32021` with `data.requiredCapabilities` set to `{"elicitation":{"form":{}}}`.

> 每个请求还携带 `io.modelcontextprotocol/protocolVersion`。缺失或非字符串的版本返回 `-32602`。不支持的字符串返回 `-32022`，并附带精确的 `supported` 与 `requested` 数据。缺失或仅 URL 的 elicitation 支持返回 `-32021`，`data.requiredCapabilities` 设为 `{"elicitation":{"form":{}}}`。

An envelope without a JSON-RPC `id` is a notification. Process it without emitting a JSON-RPC success or error response. On Streamable HTTP, an accepted notification receives `202 Accepted` with no body.

> 没有 JSON-RPC `id` 的信封是通知。处理它但不发出 JSON-RPC 成功或错误响应。在 Streamable HTTP 上，被接受的通知收到没有响应体的 `202 Accepted`。

`clientInfo` should be included for diagnostics, but it is self-reported and cannot identify the user for authorization.

> `clientInfo` 应当包含以便诊断，但它是自报的数据，不能用作授权意义上的用户身份。

The server implements `server/discover` and returns `supportedVersions`, capabilities, `ttlMs`, and `cacheScope` with `resultType: "complete"`. It does not advertise Roots for this modern design. Because it advertises tools, it also implements mandatory `tools/list`. That result returns the deterministic `notes_delete` descriptor, a valid object `inputSchema`, server identity metadata, and public cache hints.

> 服务器实现 `server/discover`，返回 `supportedVersions`、能力、`ttlMs` 和 `cacheScope`，`resultType` 为 `"complete"`。在这个现代设计里它不声明 Roots。因为它声明了 tools，所以也实现强制的 `tools/list`。该结果返回确定性的 `notes_delete` 描述符、合法的对象 `inputSchema`、服务器身份元数据和公开缓存提示。

> 🤔 **【困惑】** Q: 客户端上一次请求明明声明过支持表单 elicitation，服务器这次为什么还要再检查一遍？ A: 因为 2026-07-28 没有会话——每个请求都是独立宇宙，能力声明只对当前请求有效。服务器若依赖"上一个请求说过支持"，就是隐式依赖了不存在的会话状态，重试被路由到另一个服务器实例时会出错。规则：读能力只读当前请求的 `_meta`。

## Form Mode | 表单模式

> **【中文解读】** 表单模式用受限的扁平 JSON Schema 描述"用户要填什么"：根是对象，属性只能是扁平的原始字段或枚举数组。定位是"小而可用的确认对话框"，不是通用表单引擎——消歧义、破坏性确认、非敏感偏好收集是它的主场。密码、API 密钥、支付凭据绝对不能走表单：这些秘密会经过 MCP 客户端，可能落入日志或模型上下文。

Form mode uses a restricted JSON Schema designed for usable dialogs. The root is an object and its properties are flat primitive fields or supported enum arrays. Deeply nested objects and general-purpose document schemas do not belong in a confirmation dialog.

> 表单模式使用为可用对话框设计的受限 JSON Schema。根是对象，属性是扁平的原始字段或受支持的枚举数组。深层嵌套对象和通用文档 schema 不属于确认对话框。

Use form mode for:

> 表单模式适用于：

- choosing one of several candidates;
  中文翻译：从多个候选中选择一个；
- confirming a destructive operation;
  中文翻译：确认一个破坏性操作；
- collecting non-sensitive preferences;
  中文翻译：收集非敏感偏好；
- gathering a small number of values the user, not the model, must decide.
  中文翻译：收集少量必须由用户（而非模型）决定的值。

Do not use form mode for passwords, API keys, access tokens, or payment credentials. Those secrets would pass through the MCP client and could reach logs or model context.

> 不要用表单模式收集密码、API 密钥、访问令牌或支付凭据。这些秘密会经过 MCP 客户端，可能进入日志或模型上下文。

The server validates the returned content again. Client-side form validation improves UX but does not create trust.

> 服务器要再次校验返回的内容。客户端表单校验改善 UX，但不产生信任。

## URL Mode | URL 模式

URL mode sends a secure web URL for an out-of-band interaction:

> URL 模式发送一个安全的 Web URL，用于带外交互：

```json
{
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "message": "Connect the report service to continue.",
    "url": "https://mcp.example.com/connect/report-service"
  }
}
```

Use it when sensitive information must go directly to a server-controlled web flow, such as third-party authorization. The client shows the full destination and obtains consent before opening it. It must not prefetch the URL.

> 当敏感信息必须直接进入服务器控制的 Web 流程（如第三方授权）时使用它。客户端展示完整目标地址并在打开前征得同意。它不得预取该 URL。

An `accept` response means the user agreed to open the URL. It does not prove the external flow completed. On retry, the server checks its own state and either completes or returns another `input_required` result.

> `accept` 响应表示用户同意打开该 URL。它不证明外部流程已完成。重试时，服务器检查自己的状态，要么完成操作，要么返回另一个 `input_required` 结果。

URL elicitation is not a replacement for authorization between the MCP client and MCP server. It is for an external interaction the MCP server needs to perform on the user's behalf. The server must bind the browser user to the same authenticated principal that began the MCP operation.

> URL elicitation 不是 MCP 客户端与 MCP 服务器之间授权的替代品。它用于 MCP 服务器代表用户执行的外部交互。服务器必须把浏览器里的用户绑定到发起该 MCP 操作的同一已认证主体。

## Response Branches | 响应分支

Treat the actions as product decisions, not aliases:

> 把这些动作当作产品决策，而非同义词：

| Action | Meaning | Safe server behavior |
|--------|---------|----------------------|
| `accept` | User submitted the interaction | Validate content and continue |
| `decline` | User explicitly refused | Return a complete, non-error refusal outcome |
| `cancel` | User dismissed or could not finish | Stop safely and allow a later retry |

> **【中文解读】** 表格对照（zh 版）：`accept` = 用户提交了交互——先校验内容再继续；`decline` = 用户明确拒绝——返回完整的非错误拒绝结果（本课实现中为终态）；`cancel` = 用户关闭或未能完成——安全停止，允许稍后重试。

Never interpret missing content as consent. Never convert decline into a repeated prompt loop.

> 永远不要把缺失内容解释为同意。永远不要把 decline 变成重复弹窗的循环。

## Protecting Destructive MRTR State | 保护破坏性 MRTR 状态

The candidate list cannot live only in a prompt or unsigned Base64 value. A client controls everything it sends back.

> 候选列表不能只活在提示词或未签名的 Base64 值里。客户端控制它发回的一切。

The lesson signs a state payload containing:

> 本课对包含以下内容的状态载荷签名：

- authenticated principal;
  中文翻译：已认证主体；
- originating method;
  中文翻译：发起方法；
- digest of `workspaceUri` and `title`;
  中文翻译：`workspaceUri` 和 `title` 的摘要；
- allowed note ids shown in the form;
  中文翻译：表单中展示的允许笔记 id 集合；
- operation phase;
  中文翻译：操作阶段；
- short expiry.
  中文翻译：较短的过期时间。

Before mutation, the server also checks the live note record. This catches deletion races and a target moved outside the workspace after the form was shown.

> 在变更之前，服务器还会检查活跃的笔记记录。这能捕获删除竞争，以及表单展示后目标被移出工作区的情况。

For a one-time financial or irreversible action, HMAC alone does not prevent a valid state from being replayed within its expiry. Store and consume a nonce exactly once in a replay store shared by every handler instance. The lesson injects a bounded, TTL-pruned store and holds its atomic claim while performing the in-memory deletion. A production database should couple the nonce claim and mutation in one transaction or equivalent conditional-write boundary.

> 对于一次性的金融操作或不可逆操作，仅靠 HMAC 不能阻止一个有效状态在过期时间内被重放。要在所有处理器实例共享的重放存储中，恰好存储并消耗一次 nonce。本课注入了一个有界、按 TTL 清理的存储，并在执行内存删除期间持有其原子声明。生产数据库应当把 nonce 声明与变更耦合进一个事务或等价的条件写边界。

Validate the interaction before claiming the nonce. A malformed response or `cancel` performs no mutation and leaves the state retryable until expiry. An explicit `decline` is terminal, so the lesson consumes the nonce without deleting anything.

> 在声明 nonce 之前先校验交互。格式错误的响应或 `cancel` 不执行变更，状态在过期前保持可重试。显式 `decline` 是终态，因此本课在不删除任何东西的情况下消耗 nonce。

> ⚠️ **【易错点】** 场景：只做 HMAC 签名、不做一次性 nonce / 后果：攻击者（或重复的客户端重试）在过期窗口内原样重放同一份 `requestState` + `inputResponses`，同一个删除被确认两次；多实例部署下更难察觉 / 修复：签名只解决"状态未被篡改"，不解决"状态只用一次"；把"声明 nonce + 执行变更"放进同一原子边界（事务或条件写），并让全部实例共享同一个重放存储。

```figure
t3-roots-boundary
```

## Build It | 动手构建

`code/main.py` demonstrates a modern `notes_delete` tool:

> `code/main.py` 演示一个现代的 `notes_delete` 工具：

- `tools/list` returns a deterministic, cacheable descriptor with the required workspace and title schema.
  中文翻译：`tools/list` 返回带必需 workspace 与 title schema 的确定性、可缓存描述符。
- Scope is an explicit `workspaceUri` argument.
  中文翻译：作用域是显式的 `workspaceUri` 参数。
- Server configuration authorizes that workspace for the lesson principal.
  中文翻译：服务器配置为课程主体授权该工作区。
- URI normalization rejects prefix confusion and encoded traversal.
  中文翻译：URI 归一化拒绝前缀混淆和编码穿越。
- Every destructive deletion requires form-mode elicitation.
  中文翻译：每次破坏性删除都要求表单模式 elicitation。
- The elicitation travels inside `resultType: "input_required"`.
  中文翻译：elicitation 装在 `resultType: "input_required"` 里传输。
- Signed `requestState` binds the exact candidate list and original arguments.
  中文翻译：签名的 `requestState` 绑定精确的候选列表和原始参数。
- An injected replay store rejects the same accepted or declined state across server instances.
  中文翻译：注入的重放存储跨服务器实例拒绝同一个已接受或已拒绝的状态。
- The retry uses a fresh request id and returns `resultType: "complete"`.
  中文翻译：重试使用全新的请求 id 并返回 `resultType: "complete"`。

The data store is in memory so the protocol behavior is easy to inspect. The security rules remain the same with a database.

> 数据存储在内存中，便于检查协议行为。换成数据库后安全规则不变。

## Use It | 运行验证

From the repository root:

> 从仓库根目录：

```bash
cd phases/13-tools-and-protocols/12-mcp-roots-and-elicitation/code
python3 main.py
python3 -m unittest discover tests -v
```

Expected checkpoints:

> 预期检查点：

- Discovery advertises tools without Roots.
  中文翻译：发现结果声明 tools 而没有 Roots。
- Tool discovery returns `notes_delete` with `resultType`, server identity, and cache hints.
  中文翻译：工具发现返回带 `resultType`、服务器身份和缓存提示的 `notes_delete`。
- Request id `1` returns the form in `inputRequests.delete_choice`.
  中文翻译：请求 id `1` 在 `inputRequests.delete_choice` 中返回表单。
- Request id `2` echoes the signed state and completes the deletion.
  中文翻译：请求 id `2` 回传签名状态并完成删除。
- A prefix path and an encoded traversal path both fail containment.
  中文翻译：前缀路径和编码穿越路径都未通过包含检查。
- A changed title cannot reuse the original confirmation state.
  中文翻译：改过的标题不能复用原始确认状态。
- A decline leaves the note unchanged.
  中文翻译：decline 之后笔记保持不变。
- Two server objects sharing note and replay state cannot both execute one confirmation.
  中文翻译：共享笔记与重放状态的两个服务器对象不能都执行同一个确认。
- Empty and explicit form declarations work, while URL-only support returns exact `-32021` form requirements.
  中文翻译：空声明和显式表单声明都能工作，而仅 URL 支持返回精确的 `-32021` 表单要求。
- Unsupported version failures use the exact `-32022` data shape.
  中文翻译：不支持的版本失败使用精确的 `-32022` 数据形状。
- An id-less notification produces no JSON-RPC response.
  中文翻译：无 id 的通知不产生 JSON-RPC 响应。

## Ship It | 产出物

`outputs/skill-elicitation-form-designer.md` designs the explicit scope, authorization checks, MRTR form, response branches, and state binding. It refuses to treat deprecated Roots as a sandbox or to collect secrets through form mode.

> `outputs/skill-elicitation-form-designer.md` 设计显式作用域、授权检查、MRTR 表单、响应分支和状态绑定。它拒绝把已废弃的 Roots 当沙箱，也拒绝通过表单模式收集秘密。

## Exercises | 练习题

1. Replace the in-memory replay store with SQLite. Use one transaction to claim the nonce and delete the note, then prove two processes cannot both commit.
   中文翻译：把内存重放存储换成 SQLite。用一个事务声明 nonce 并删除笔记，然后证明两个进程不能都提交成功。
2. Add `url` capability negotiation and an out-of-band setup flow. Keep third-party credentials out of `inputResponses`.
   中文翻译：添加 `url` 能力协商和一个带外设置流程。让第三方凭据远离 `inputResponses`。
3. Replace the in-memory note map with a temporary SQLite database. Re-check authorization and containment inside the mutation transaction.
   中文翻译：把内存笔记映射换成临时 SQLite 数据库。在变更事务内部重新检查授权和包含关系。
4. Add a symbolic-link policy for a real filesystem implementation. Explain why URI lexical containment alone cannot stop a symlink escape.
   中文翻译：为真实文件系统实现添加符号链接策略。解释为什么仅靠 URI 词法包含检查挡不住符号链接逃逸。
5. Design a 2025-11-25 adapter that maps modern MRTR handler output to legacy server-initiated elicitation. Keep it isolated from the current handler.
   中文翻译：设计一个 2025-11-25 适配器，把现代 MRTR 处理器输出映射为旧版服务器发起的 elicitation。让它与当前处理器隔离。

## Key Terms | 术语速查表

| Term | Meaning in 2026-07-28 |
|------|------------------------|
| Roots | Deprecated informational workspace hints, not authorization or sandboxing |
| Explicit scope | Workspace, directory, or resource handle visible in request arguments |
| Containment | Normalized path-component check that keeps a target inside a boundary |
| Elicitation | Client feature for obtaining user input during an MCP operation |
| Form mode | In-band structured user input using a restricted flat schema |
| URL mode | Out-of-band interaction for sensitive or external workflows |
| MRTR | Stateless input-required result followed by a fresh retry |
| `requestState` | Opaque state echoed exactly and integrity-checked by the server |
| Decline | Explicit user refusal |
| Cancel | Dismissal or incomplete interaction without approval |

> **【中文解读】** 术语速查（中英对照）：Roots=已废弃的信息性工作区提示，不是授权也不是沙箱；Explicit scope=显式作用域，请求参数中可见的工作区/目录/资源句柄；Containment=包含检查，归一化路径组件检查；Elicitation=诱导输入，MCP 操作期间获取用户输入的客户端特性；Form mode=表单模式；URL mode=带外交互；MRTR=无状态的 input_required 结果加全新重试；requestState=原样回传并由服务器做完整性校验的不透明状态；Decline=明确拒绝；Cancel=未完成的关闭。

## Legacy Compatibility | 旧版兼容

For a peer pinned to 2025-11-25, `roots/list`, `notifications/roots/list_changed`, and live server-initiated `elicitation/create` may still exist. Label that adapter legacy. Do not allow a legacy Root list to bypass server authorization, and do not carry protocol-session assumptions into the modern handler.

> 对于锁定在 2025-11-25 的对端，`roots/list`、`notifications/roots/list_changed` 和活跃的服务器发起 `elicitation/create` 可能仍然存在。给那个适配器贴上 legacy 标签。不要允许旧版 Root 列表绕过服务器授权，也不要把协议会话的假设带进现代处理器。

## Further Reading | 延伸阅读

- [MCP 2026-07-28 Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)
  中文翻译：2026-07-28 版 elicitation 官方规范。
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译：MRTR（多轮往返请求）模式规范，`input_required` 结果的权威定义。
- [MCP 2026-07-28 Roots deprecation](https://modelcontextprotocol.io/specification/2026-07-28/client/roots)
  中文翻译：Roots 废弃说明。
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译：`server/discover` 发现机制规范。
