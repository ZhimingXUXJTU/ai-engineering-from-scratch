# Building an MCP Server: Stateless Python and TypeScript | 构建 MCP 服务器：无状态 Python 与 TypeScript

> A modern MCP server does not remember a handshake. It validates the metadata on every request, runs one handler, and returns one typed result.

> **【中文解读】** 现代 MCP 服务器不记得任何握手。它对每个请求校验元数据、执行一个 handler、返回一个类型化结果。本课用纯标准库把一个笔记服务器写两遍（Python 和 TypeScript），核心是四件事：逐请求校验 `params._meta`、必选的 `server/discover`、确定性排序的可缓存列表、以及统一的 `resultType` 结果包装。

> **【拓展：MCP 服务器→Claude 生态开发】** MCP 服务器是 Claude 生态的标准工具接口形态：Claude Desktop、Cursor、VS Code 等宿主都通过 stdio 或 HTTP 启动你的服务器并调用其工具。旧教程以 initialize 握手开场；2026-07-28 之后无状态内核反而更简单——没有连接状态要维护，任何副本都能处理任何请求。理解本课的 stdlib 实现后，迁移到官方 SDK 只是换语法。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 06（MCP 基础）——无状态请求模型、`params._meta` 三件套、`server/discover`、`resultType`/`ttlMs`/`cacheScope`；(2) Python 子进程与 stdin/stdout 逐行通信；(3) JSON-RPC 2.0 错误码（-32700/-32600/-32601/-32602/-32603 与 MCP 专属的 -32022）。

**Type:** Build | **类型:** 构建
**Languages:** Python, TypeScript | **语言:** Python, TypeScript
**Prerequisites:** Phase 13, Lesson 06 | **前置知识:** Phase 13, Lesson 06
**Time:** ~85 minutes | **时间:** ~85 分钟

## Learning Objectives | 学习目标

- Implement mandatory `server/discover` for MCP `2026-07-28`.
  中文翻译：为 MCP `2026-07-28` 实现必选的 `server/discover`。
- Validate protocol version and client capabilities on every request.
  中文翻译：在每个请求上校验协议版本和客户端能力。
- Expose tools, resources, and prompts with deterministic list ordering.
  中文翻译：以确定性列表排序暴露 tools、resources 和 prompts。
- Return `resultType`, server identity, and cache hints on the correct results.
  中文翻译：在正确的结果上返回 `resultType`、服务器身份和缓存提示。
- Serve the same stateless contract over newline-delimited stdio in Python and TypeScript.
  中文翻译：用 Python 和 TypeScript 在换行分隔的 stdio 上提供同一个无状态契约。

## The Problem | 问题引入

> **【中文解读】** 旧式服务器把第一个请求的 capabilities 存下来复用，好写但难运维：同一进程先后服务多个客户端、远程请求落到不同 worker 时，过期的能力声明会跨授权边界泄漏行为。2026-07-28 用"每个请求自描述"解决协议层的问题；你的应用仍可保留笔记、任务等持久状态，唯一禁止的是影响后续请求解码的隐藏协议状态。

A server that stores client capabilities after the first message is easy to build and hard to operate. The same process may serve sequential clients. A remote request may land on a different worker. A stale capability declaration can leak behavior across authorization boundaries.

> 一个在第一条消息后存储客户端能力的服务器容易写却难运维。同一进程可能先后服务多个客户端；一个远程请求可能落到另一个 worker 上；过期的能力声明会跨授权边界泄漏行为。

MCP `2026-07-28` solves the protocol part of that problem by making every request self-describing. Your application can still keep durable notes, jobs, or explicit state handles. What it cannot keep is hidden protocol state that changes how a later request is decoded.

> MCP `2026-07-28` 通过让每个请求自描述来解决这个问题的协议部分。你的应用仍然可以保留持久的笔记、任务或显式状态句柄。它不能保留的是会改变后续请求解码方式的隐藏协议状态。

This lesson builds a notes server twice. The Python and TypeScript versions use only their standard libraries for the protocol core. Both expose the same methods and enforce the same wire contract.

> 本课把一个笔记服务器构建两遍。Python 版和 TypeScript 版的协议核心都只使用各自的标准库。两者暴露相同的方法并执行相同的线格式契约。

## The Concept | 核心概念

### The modern dispatch loop

> **【中文解读】** 现代分发循环九步：读一行 JSON-RPC → 解析信封 → 通知不响应 → 校验本请求的 params._meta → 按方法路由 → 用 resultType 和 serverInfo 包装成功 → 写一行响应 → 忘掉请求级元数据。stdio 三条铁律不变：stdout 只写 JSON-RPC（诊断走 stderr）、换行分隔并逐条 flush、stdin EOF 即退出。进程生命周期只是传输层生命周期，不是 MCP 会话。

```text
read one JSON-RPC line
parse the envelope
if it is a notification, do not respond
validate params._meta for this request
route by method
wrap success with resultType and serverInfo
write one JSON-RPC response line
forget request-scoped metadata
```

Three stdio rules still matter:

- Write only JSON-RPC messages to stdout. Send diagnostics to stderr.
  中文翻译：只向 stdout 写 JSON-RPC 消息。诊断信息发到 stderr。
- Delimit messages with a newline and flush each response.
  中文翻译：用换行符分隔消息并逐条 flush 响应。
- Exit promptly when stdin reaches EOF.
  中文翻译：stdin 到达 EOF 时立即退出。

The process lifetime is a transport lifetime. It is not a modern MCP session.

> 进程生命周期只是传输层生命周期。它不是现代 MCP 会话。

> ⚠️ **【易错点】** 场景：调试时用 `print()` 往 stdout 打印变量 / 后果：stdout 混入非 JSON 文本，客户端解析信封失败断连；另一常见坑是忘记 `flush()` 导致响应滞留缓冲区，客户端超时 / 修复：所有诊断输出走 `sys.stderr`（或 logging，默认 stderr），每条响应 `sys.stdout.write(json.dumps(...) + "\n")` 后立即 `flush()`。

### Request validation

Every request must have:

> 每个请求必须带有：

```json
{
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "notes-client",
        "version": "1.0.0"
      }
    }
  }
}
```

The first two fields are required. `clientInfo` is recommended. Validate a present identity shape, but do not treat it as authentication.

> 前两个字段是必填的。`clientInfo` 是建议项。校验"存在时的身份形状"，但不要把它当作认证。

If the version is unsupported, return code `-32022` with `requested` and `supported`. Missing request metadata is invalid params, code `-32602`. Never fill missing fields from a previous call.

> 如果版本不受支持，返回错误码 `-32022` 并附 `requested` 与 `supported`。缺失请求元数据属于无效参数，返回 `-32602`。绝不从上一次调用补全缺失字段。

### Mandatory discovery

Modern servers must implement `server/discover`. A complete discovery result includes supported modern versions, capabilities, optional instructions, cache hints, and server identity in result `_meta`:

> 现代服务器必须实现 `server/discover`。完整的发现结果包括支持的现代版本、能力、可选的使用说明、缓存提示，以及结果 `_meta` 中的服务器身份：

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {"listChanged": false},
    "resources": {"listChanged": false, "subscribe": false},
    "prompts": {"listChanged": false}
  },
  "ttlMs": 3600000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

Discovery does not unlock the server. A client may call `tools/list` without calling discovery because `tools/list` already carries the same request metadata.

> 发现不会"解锁"服务器。客户端可以不调用发现而直接调用 `tools/list`，因为 `tools/list` 本来就携带同样的请求元数据。

### Tools

> **【中文解读】** 工具部分两条线：`tools/list` 返回确定性排序的工具描述符（稳定排序改善响应缓存并保持模型上下文稳定），结果必带 `ttlMs` 和 `cacheScope`；`tools/call` 返回内容块和 `isError`。错误有两层：协议信封或方法参数无效 → JSON-RPC error；调用合法但工具本身失败 → `isError: true`。这让模型能在上下文里读到失败原因并自我修复，而不是只收到一个连接层错误。annotations（readOnly/destructive/idempotent/openWorld）仍只是提示，宿主拿它做确认与展示，真正的授权仍要服务器自己执行。

`tools/list` returns a deterministic list of tool descriptors. Stable ordering improves response caching and keeps model context stable. The result also requires `ttlMs` and `cacheScope`.

> `tools/list` 返回确定性排序的工具描述符列表。稳定排序改善响应缓存并保持模型上下文稳定。该结果还必须带 `ttlMs` 和 `cacheScope`。

`tools/call` returns content blocks and `isError`. Use a JSON-RPC error when the protocol envelope or method parameters are invalid. Use `isError: true` when a valid tool invocation runs but the tool itself fails.

> `tools/call` 返回内容块和 `isError`。协议信封或方法参数无效时用 JSON-RPC error；合法的工具调用已执行但工具本身失败时用 `isError: true`。

Tool annotations remain hints, not enforcement:

- `readOnlyHint`
  中文翻译：`readOnlyHint`（只读提示）
- `destructiveHint`
  中文翻译：`destructiveHint`（破坏性提示）
- `idempotentHint`
  中文翻译：`idempotentHint`（幂等提示）
- `openWorldHint`
  中文翻译：`openWorldHint`（开放世界提示）

The host should use them for confirmation and presentation. The server must still enforce real authorization.

> 宿主应把它们用于确认和展示。服务器仍必须执行真正的授权。

### Resources

`resources/list` returns stable URI descriptors. `resources/read` returns typed contents. Both are cacheable in `2026-07-28`, so both include `ttlMs` and `cacheScope`.

> `resources/list` 返回稳定的 URI 描述符。`resources/read` 返回类型化内容。两者在 `2026-07-28` 中都是可缓存的，因此都包含 `ttlMs` 和 `cacheScope`。

Use `cacheScope: "private"` for user-specific note data. A shared cache must not reuse a private response across authorization contexts.

> 用户相关的笔记数据用 `cacheScope: "private"`。共享缓存不得跨授权上下文复用一个 private 响应。

Modern change delivery does not use `resources/subscribe`. A client opens `subscriptions/listen` and requests `resourceSubscriptions` or list-change categories. Lesson 10 builds that flow.

> 现代的变更投递不再使用 `resources/subscribe`。客户端打开 `subscriptions/listen` 并请求 `resourceSubscriptions` 或列表变更类别。Lesson 10 构建那个流程。

### Prompts

`prompts/list` is cacheable and deterministic. `prompts/get` renders a named prompt with arguments. The rendered prompt result is complete, but it is not one of the cacheable list or read results that requires cache hints.

> `prompts/list` 可缓存且确定性排序。`prompts/get` 用参数渲染命名 prompt。渲染出的 prompt 结果是 complete 的，但它不属于必须带缓存提示的那类可缓存列表/读取结果。

### Every successful result is typed

> **【中文解读】** 所有成功结果走同一个包装函数：打上 `resultType: "complete"` 和 `_meta` 里的 serverInfo；列表、读取和发现这三类 handler 再补 `ttlMs` 与 `cacheScope`。集中一处包装的意义是防止某个 handler 悄悄漏掉现代结果字段——漏一个字段，客户端就可能按旧时代解读你的响应。

The examples use one wrapper for every success:

```python
def complete(payload):
    return {
        "resultType": "complete",
        **payload,
        "_meta": {SERVER_INFO_KEY: SERVER_INFO},
    }
```

List, read, and discovery handlers add `ttlMs` plus `cacheScope`. Centralizing this wrapper prevents one handler from silently omitting modern result fields.

> 列表、读取和发现 handler 追加 `ttlMs` 与 `cacheScope`。把这个包装集中起来，可以防止某个 handler 悄悄漏掉现代结果字段。

### No server-initiated requests

> **【中文解读】** 现代服务器可以发两类东西：与客户端请求相关的通知、以及客户端打开的 `subscriptions/listen` 流上的通知。它不得主动发起自己的 JSON-RPC 请求。当 handler 需要 sampling、elicitation 或 roots 输入时，它返回 `input_required` 结果，由客户端补齐内嵌的输入请求后用新请求 id 重试原方法——这就是"多轮往返请求"（Multi Round-Trip Requests）模式，Lesson 11 展开。

A modern server may send notifications related to a client request, or notifications on a client-opened `subscriptions/listen` stream. It must not send its own JSON-RPC request.

> 现代服务器可以发送与客户端请求相关的通知，或在客户端打开的 `subscriptions/listen` 流上发送通知。它不得发送自己的 JSON-RPC 请求。

When a handler needs sampling, elicitation, or roots input, it returns an `input_required` result. The client fulfills the embedded input requests and retries the original method with a new request id. Lesson 11 covers that Multi Round-Trip Request pattern.

> 当 handler 需要 sampling、elicitation 或 roots 输入时，它返回 `input_required` 结果。客户端补齐内嵌的输入请求，然后用新的请求 id 重试原方法。Lesson 11 讲解那个多轮往返请求模式。

### Explicit legacy compatibility

A dual-era server may also implement the `2025-11-25` handshake on a clearly separate legacy branch. It chooses modern behavior when required modern `_meta` fields are present and legacy behavior when it receives `initialize`.

> 双时代服务器可以把 `2025-11-25` 握手实现在一条清晰分离的旧版分支上。当请求带必需的现代 `_meta` 字段时选择现代行为，收到 `initialize` 时选择旧版行为。

Do not put a `2026-07-28` request through the legacy handshake path. Do not stamp modern `resultType` fields onto legacy initialization results. The code in this lesson is deliberately modern-only so its invariants stay visible.

> 不要让 `2026-07-28` 请求走旧版握手路径。不要把现代 `resultType` 字段盖到旧版初始化结果上。本课代码刻意只做现代版，好让不变式保持可见。

> 💡 **【类比】** 双时代服务器像机场的双通道边检：一条"电子护照自助通道"（现代：刷护照自描述通过），一条"人工柜台"（旧版：排队登记握手）。旅客走哪条由"出示什么证件"一次性判定（有 `_meta` 三件套 → 现代；发 `initialize` → 旧版），两条通道物理隔离、互不借用流程。最忌讳的是开一条"混合通道"——现代请求被拉去排队握手，或旧版结果被贴上电子通道的标签。

```figure
t3-dispatch-loop
```

## Use It | 用框架实现

Run the Python server's finite demo and tests:

> 运行 Python 服务器的有限演示和测试：

```bash
cd code
python3 main.py --demo
python3 -m unittest discover tests -v
```

Run the TypeScript port with a TypeScript runner:

> 用 TypeScript 运行器跑 TypeScript 移植版：

```bash
npx tsx main.ts --demo
```

The demo sends `server/discover`, lists each primitive, invokes tools, and shows an unsupported-version error. Every modern request repeats metadata. Every success includes server identity.

> 演示发送 `server/discover`，逐个列出原语，调用工具，并展示一个不支持的版本错误。每个现代请求都重复携带元数据。每个成功结果都包含服务器身份。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-server-scaffolder.md`. It produces a modern server plan with a discovery contract, per-request validation, deterministic cacheable lists, and an optional isolated legacy adapter.

> 本课交付 `outputs/skill-mcp-server-scaffolder.md`。它产出一份现代服务器规划：发现契约、逐请求校验、确定性的可缓存列表，以及一个可选的隔离旧版适配器。

## Exercises | 练习题

1. Remove capabilities from one request and prove the server does not reuse the previous request's declaration.
   中文翻译：从某个请求中移除 capabilities，证明服务器不会复用上一个请求的声明。

2. Reverse the `TOOLS`, `PROMPTS`, and note insertion order. Confirm all list results remain stable.
   中文翻译：反转 `TOOLS`、`PROMPTS` 和笔记的插入顺序。确认所有列表结果保持稳定。

3. Add a destructive `notes_delete` tool and require an authorization check inside the executor. Keep `destructiveHint` as a UX hint only.
   中文翻译：添加一个破坏性的 `notes_delete` 工具，并要求在执行器内部做授权检查。`destructiveHint` 只保留为 UX 提示。

4. Add `resources/templates/list` with `ttlMs`, `cacheScope`, and deterministic ordering.
   中文翻译：添加带 `ttlMs`、`cacheScope` 和确定性排序的 `resources/templates/list`。

5. Build a separate legacy adapter for `2025-11-25`. Add tests proving a modern request never enters it.
   中文翻译：为 `2025-11-25` 构建一个独立的旧版适配器。添加测试证明现代请求绝不会进入它。

## Key Terms | 术语速查表

| Term | Meaning |
|------|---------|
| Stateless server | Handles each request from its own metadata without protocol-session memory |
| `server/discover` | Mandatory modern method that advertises versions and capabilities |
| Complete result | Successful modern result with `resultType: "complete"` |
| Cacheable result | Discovery, list, or resource-read result with `ttlMs` and `cacheScope` |
| Deterministic list | Same logical registry produces the same item order |
| Server identity | Recommended `io.modelcontextprotocol/serverInfo` in result `_meta` |
| Tool error | Valid tool call that returns content with `isError: true` |
| Protocol error | Invalid JSON-RPC or MCP request returned through `error` |

> 术语中文对照：Stateless server=无状态服务器（只凭请求自身元数据处理，无协议会话记忆）；server/discover=服务器发现（必选现代方法，公示版本与能力）；Complete result=完整结果（带 `resultType: "complete"` 的成功现代结果）；Cacheable result=可缓存结果（发现/列表/资源读取结果，带 `ttlMs` 与 `cacheScope`）；Deterministic list=确定性列表（同一逻辑注册表产出同一顺序）；Server identity=服务器身份（结果 `_meta` 中建议的 serverInfo）；Tool error=工具错误（合法调用返回内容且 `isError: true`）；Protocol error=协议错误（非法 JSON-RPC 或 MCP 请求，经 `error` 返回）。

## Further Reading | 延伸阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)
  中文翻译：MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译：server/discover 方法规范
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  中文翻译：tools 原语规范
- [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  中文翻译：resources 原语规范
- [MCP Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  中文翻译：prompts 原语规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  中文翻译：stdio 传输层规范
