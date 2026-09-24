# 构建 MCP 服务器：无状态 Python 与 TypeScript

> 现代 MCP 服务器不记得任何握手。它对每个请求校验元数据、执行一个 handler、返回一个类型化结果。

> **【中文解读】** 现代 MCP 服务器不记得任何握手。它对每个请求校验元数据、执行一个 handler、返回一个类型化结果。本课用纯标准库把一个笔记服务器写两遍（Python 和 TypeScript），核心是四件事：逐请求校验 `params._meta`、必选的 `server/discover`、确定性排序的可缓存列表、以及统一的 `resultType` 结果包装。

> **【拓展：MCP 服务器→Claude 生态开发】** MCP 服务器是 Claude 生态的标准工具接口形态：Claude Desktop、Cursor、VS Code 等宿主都通过 stdio 或 HTTP 启动你的服务器并调用其工具。旧教程以 initialize 握手开场；2026-07-28 之后无状态内核反而更简单——没有连接状态要维护，任何副本都能处理任何请求。理解本课的 stdlib 实现后，迁移到官方 SDK 只是换语法。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 06（MCP 基础）——无状态请求模型、`params._meta` 三件套、`server/discover`、`resultType`/`ttlMs`/`cacheScope`；(2) Python 子进程与 stdin/stdout 逐行通信；(3) JSON-RPC 2.0 错误码（-32700/-32600/-32601/-32602/-32603 与 MCP 专属的 -32022）。

**类型：** 构建
**语言：** Python、TypeScript
**前置条件：** Phase 13 · 06
**时间：** 约 85 分钟

## 学习目标

- 为 MCP `2026-07-28` 实现必选的 `server/discover`。
- 在每个请求上校验协议版本和客户端能力。
- 以确定性列表排序暴露 tools、resources 和 prompts。
- 在正确的结果上返回 `resultType`、服务器身份和缓存提示。
- 用 Python 和 TypeScript 在换行分隔的 stdio 上提供同一个无状态契约。

## 问题引入

一个在第一条消息后存储客户端能力的服务器容易写却难运维。同一进程可能先后服务多个客户端；一个远程请求可能落到另一个 worker 上；过期的能力声明会跨授权边界泄漏行为。

MCP `2026-07-28` 通过让每个请求自描述来解决这个问题的协议部分。你的应用仍然可以保留持久的笔记、任务或显式状态句柄。它不能保留的是会改变后续请求解码方式的隐藏协议状态。

本课把一个笔记服务器构建两遍。Python 版和 TypeScript 版的协议核心都只使用各自的标准库。两者暴露相同的方法并执行相同的线格式契约。

> **【中文解读】** 旧式服务器把第一个请求的 capabilities 存下来复用，好写但难运维：同一进程先后服务多个客户端、远程请求落到不同 worker 时，过期的能力声明会跨授权边界泄漏行为。2026-07-28 用"每个请求自描述"解决协议层的问题；你的应用仍可保留笔记、任务等持久状态，唯一禁止的是影响后续请求解码的隐藏协议状态。

## 核心概念

### 现代分发循环

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

三条 stdio 铁律依然重要：

- 只向 stdout 写 JSON-RPC 消息。诊断信息发到 stderr。
- 用换行符分隔消息并逐条 flush 响应。
- stdin 到达 EOF 时立即退出。

进程生命周期只是传输层生命周期。它不是现代 MCP 会话。

### 请求校验

每个请求必须带有：

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

前两个字段是必填的。`clientInfo` 是建议项。校验"存在时的身份形状"，但不要把它当作认证。

如果版本不受支持，返回错误码 `-32022` 并附 `requested` 与 `supported`。缺失请求元数据属于无效参数，返回 `-32602`。绝不从上一次调用补全缺失字段。

### 必选的发现

现代服务器必须实现 `server/discover`。完整的发现结果包括支持的现代版本、能力、可选的使用说明、缓存提示，以及结果 `_meta` 中的服务器身份：

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

发现不会"解锁"服务器。客户端可以不调用发现而直接调用 `tools/list`，因为 `tools/list` 本来就携带同样的请求元数据。

### Tools

`tools/list` 返回确定性排序的工具描述符列表。稳定排序改善响应缓存并保持模型上下文稳定。该结果还必须带 `ttlMs` 和 `cacheScope`。

`tools/call` 返回内容块和 `isError`。协议信封或方法参数无效时用 JSON-RPC error；合法的工具调用已执行但工具本身失败时用 `isError: true`。

工具注解仍然只是提示，不是强制：

- `readOnlyHint`
- `destructiveHint`
- `idempotentHint`
- `openWorldHint`

宿主应把它们用于确认和展示。服务器仍必须执行真正的授权。

> **【中文解读】** 工具部分两条线：`tools/list` 的确定性排序让等价的响应产生稳定的缓存键和稳定的模型上下文；`tools/call` 的错误分两层——协议级错误走 JSON-RPC error，工具级失败走 `isError: true`，后者让模型能在上下文里读到失败原因并自我修复。annotations（readOnly/destructive/idempotent/openWorld）只是给宿主的 UX 提示，真正的授权必须由服务器在执行器里自己执行。

### Resources

`resources/list` 返回稳定的 URI 描述符。`resources/read` 返回类型化内容。两者在 `2026-07-28` 中都是可缓存的，因此都包含 `ttlMs` 和 `cacheScope`。

用户相关的笔记数据用 `cacheScope: "private"`。共享缓存不得跨授权上下文复用一个 private 响应。

现代的变更投递不再使用 `resources/subscribe`。客户端打开 `subscriptions/listen` 并请求 `resourceSubscriptions` 或列表变更类别。Lesson 10 构建那个流程。

### Prompts

`prompts/list` 可缓存且确定性排序。`prompts/get` 用参数渲染命名 prompt。渲染出的 prompt 结果是 complete 的，但它不属于必须带缓存提示的那类可缓存列表/读取结果。

### 每个成功结果都是类型化的

示例为所有成功结果使用同一个包装：

```python
def complete(payload):
    return {
        "resultType": "complete",
        **payload,
        "_meta": {SERVER_INFO_KEY: SERVER_INFO},
    }
```

列表、读取和发现 handler 追加 `ttlMs` 与 `cacheScope`。把这个包装集中起来，可以防止某个 handler 悄悄漏掉现代结果字段。

### 服务器不主动发起请求

现代服务器可以发送与客户端请求相关的通知，或在客户端打开的 `subscriptions/listen` 流上发送通知。它不得发送自己的 JSON-RPC 请求。

当 handler 需要 sampling、elicitation 或 roots 输入时，它返回 `input_required` 结果。客户端补齐内嵌的输入请求，然后用新的请求 id 重试原方法。Lesson 11 讲解那个多轮往返请求模式。

> **【中文解读】** "服务器不主动发起请求"是 2026-07-28 的硬边界：服务器能发的只有两类通知——与客户端请求相关的、以及客户端打开的 `subscriptions/listen` 流上的。需要模型补全或用户输入时不再反向调用客户端，而是返回 `input_required` 把控制流还给客户端。这使网关、鉴权和缓存都可以按"请求-响应"模型统一处理。

### 显式旧版兼容

双时代服务器可以把 `2025-11-25` 握手实现在一条清晰分离的旧版分支上。当请求带必需的现代 `_meta` 字段时选择现代行为，收到 `initialize` 时选择旧版行为。

不要让 `2026-07-28` 请求走旧版握手路径。不要把现代 `resultType` 字段盖到旧版初始化结果上。本课代码刻意只做现代版，好让不变式保持可见。

## 用框架实现

运行 Python 服务器的有限演示和测试：

```bash
cd code
python3 main.py --demo
python3 -m unittest discover tests -v
```

用 TypeScript 运行器跑 TypeScript 移植版：

```bash
npx tsx main.ts --demo
```

演示发送 `server/discover`，逐个列出原语，调用工具，并展示一个不支持的版本错误。每个现代请求都重复携带元数据。每个成功结果都包含服务器身份。

## 产出物

本课交付 `outputs/skill-mcp-server-scaffolder.md`。它产出一份现代服务器规划：发现契约、逐请求校验、确定性的可缓存列表，以及一个可选的隔离旧版适配器。

## 练习题

1. 从某个请求中移除 capabilities，证明服务器不会复用上一个请求的声明。

2. 反转 `TOOLS`、`PROMPTS` 和笔记的插入顺序。确认所有列表结果保持稳定。

3. 添加一个破坏性的 `notes_delete` 工具，并要求在执行器内部做授权检查。`destructiveHint` 只保留为 UX 提示。

4. 添加带 `ttlMs`、`cacheScope` 和确定性排序的 `resources/templates/list`。

5. 为 `2025-11-25` 构建一个独立的旧版适配器。添加测试证明现代请求绝不会进入它。

## 术语速查表

| 术语 | 含义 |
|------|------|
| 无状态服务器 | 只凭请求自身元数据处理每个请求，没有协议会话记忆 |
| `server/discover` | 必选的现代方法，公示版本与能力 |
| 完整结果 | 带 `resultType: "complete"` 的成功现代结果 |
| 可缓存结果 | 发现、列表或资源读取结果，带 `ttlMs` 和 `cacheScope` |
| 确定性列表 | 同一逻辑注册表产出相同的条目顺序 |
| 服务器身份 | 结果 `_meta` 中建议的 `io.modelcontextprotocol/serverInfo` |
| 工具错误 | 合法工具调用返回内容且 `isError: true` |
| 协议错误 | 非法 JSON-RPC 或 MCP 请求，经 `error` 返回 |

## 延伸阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/) — MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — server/discover 方法规范
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) — tools 原语规范
- [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) — resources 原语规范
- [MCP Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts) — prompts 原语规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio) — stdio 传输层规范
