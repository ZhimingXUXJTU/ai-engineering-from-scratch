# 构建 MCP 客户端 — 发现、调用与会话管理

> 大多数 MCP 内容只教服务器端教程。客户端代码才是真正复杂的编排所在：进程生成、能力协商、多服务器工具列表合并、sampling 回调、重连和命名空间冲突解决。本课构建一个多服务器客户端，将三个不同的 MCP 服务器提升到一个扁平的工具命名空间中。

> **【中文解读】** 大多数 MCP 内容只教服务器端教程。客户端代码才是真正复杂的编排所在：进程生成、能力协商、多服务器工具列表合并、sampling 回调、重连和命名空间冲突解决。本课构建一个多服务器客户端，将三个不同的 MCP 服务器提升到一个扁平的工具命名空间中。

> **【拓展：MCP 客户端→Agent 编排核心】** MCP 客户端是 Agent 宿主的核心。Claude Desktop、Cursor 等都实现了 MCP 客户端，同时加载多个 MCP 服务器（如文件系统、Postgres、GitHub），将工具列表合并后提供给模型。命名空间冲突解决（前缀 vs 拒绝）是实际部署中的关键设计决策。

**类型：** 构建
**语言：** Python（标准库，多服务器 MCP 客户端）
**前置条件：** Phase 13 · 07（构建 MCP 服务器）
**时间：** 约 75 分钟

## 学习目标

- 生成 MCP 服务器作为子进程，完成 `initialize`，并发送 `notifications/initialized`。
- 维护每服务器会话状态（能力、工具列表、最近见到的通知 ID）。
- 跨多个服务器合并工具列表为一个带有冲突处理的命名空间。
- 将工具调用路由到拥有它的服务器并重组响应。

## 问题引入

一个真正的 Agent 宿主（Claude Desktop、Cursor、Goose、Gemini CLI）同时加载多个 MCP 服务器。用户可能同时运行文件系统服务器、Postgres 服务器和 GitHub 服务器。客户端的工作：

1. 生成每个服务器。
2. 独立握手每个服务器。
3. 在每个服务器上调用 `tools/list` 并扁平化结果。
4. 当模型发出 `notes_search` 时，在合并命名空间中查找并路由到正确的服务器。
5. 处理来自任何服务器的通知（`tools/list_changed`）而不阻塞。
6. 传输失败时重连。

手工实现所有这些是将"玩具"与"实用"区分开来的关键。官方 SDK 封装了这些，但心智模型必须是你的。

## 核心概念

### 子进程生成

`subprocess.Popen` 设置 `stdin=PIPE, stdout=PIPE, stderr=PIPE`。设置 `bufsize=1` 并使用文本模式逐行读取。每个服务器是一个进程；客户端为每个服务器持有一个 `Popen` 句柄。

### 每服务器会话状态

每个服务器一个 `Session` 对象持有：

- `process` — Popen 句柄。
- `capabilities` — 服务器在 `initialize` 时声明的能力。
- `tools` — 最近的 `tools/list` 结果。
- `pending` — 请求 ID 到等待响应的 promise/future 的映射。

请求本质上是异步的；在服务器 B 正在处理调用时向服务器 A 发送 `tools/call` 不能阻塞。使用带队列的线程或 asyncio。

### 合并命名空间

当客户端看到聚合工具列表时，名称可能冲突。两个服务器可能都暴露 `search`。客户端有三个选择：

1. **按服务器名前缀。** `notes/search`、`files/search`。清晰但冗长。
2. **静默先到先得。** 后加载服务器的 `search` 覆盖先加载的。风险高，隐藏冲突。
3. **碰撞拒绝。** 拒绝加载第二个服务器；通知用户。对安全敏感的宿主最安全。

Claude Desktop 使用按服务器前缀。Cursor 使用碰撞拒绝并显示清晰错误。VS Code MCP 也采用按服务器前缀。

### 路由

合并后，调度表将 `tool_name -> session` 映射起来。模型按名称发出调用；客户端找到对应 session 并向该服务器的 stdin 写入 `tools/call` 消息，然后等待响应。

### Sampling 回调

如果服务器在 `initialize` 时声明了 `sampling` 能力，它可以发送 `sampling/createMessage` 请求客户端运行其 LLM。客户端必须：

1. 阻止对该服务器的后续请求直到 sample 完成，或者如果其实现支持并发则管道化。
2. 调用其 LLM 供应商。
3. 将响应发送回服务器。

第 11 课端到端覆盖 sampling。本课为完整性而对其进行桩化。

### 通知处理

`notifications/tools/list_changed` 意味着重新调用 `tools/list`。`notifications/resources/updated` 意味着如果正在使用则重新读取资源。通知不得产生响应——不要尝试确认它们。

一个常见客户端 bug：在 `tools/call` 上阻塞读取循环，而通知排在流中。使用后台读取线程将每条消息推入队列；主线程出队并分发。

### 重连

传输可能因服务器崩溃、OS 杀进程或 stdio 管道断裂而失败。客户端检测 stdout 上的 EOF 并将会话标记为死亡。选项：

- 静默重启服务器并重新握手——适合纯只读服务器。
- 向用户报告失败——适合有状态和用户可见会话的服务器。

Phase 13 · 09 覆盖 Streamable HTTP 重连语义；stdio 更简单。

### Keepalive 和会话 ID

Streamable HTTP 使用 `Mcp-Session-Id` 头。Stdio 没有会话 ID——进程身份就是会话。Keepalive ping 是可选的；stdio 管道在非活动状态下不会断裂。

## 用框架实现

`code/main.py` 生成三个模拟 MCP 服务器作为子进程，与每个握手，合并它们的工具列表，并将工具调用路由到正确的服务器。"服务器"实际上是运行玩具响应器的其他 Python 进程（无真实 LLM）。运行它可以看到：

- 三次初始化，每次有自己的能力集。
- 三个 `tools/list` 结果合并为一个 7 工具命名空间。
- 基于工具名称的路由决策。
- 通过命名空间前缀防止的冲突。

关注点：

- `Session` dataclass 干净地持有每服务器状态。
- 后台读取线程将 stdout 上的每一行出队而不阻塞主线程。
- 调度表是一个简单的 `dict[str, Session]`。
- 冲突处理是显式的：当两个服务器声明相同名称时，后来的用前缀重命名。

## 产出物

本课产生 `outputs/skill-mcp-client-harness.md`。给定一个 MCP 服务器的声明式列表（名称、命令、参数），该技能生成一个线束，生成它们，合并工具列表，并提供带有冲突解决的路由函数。

## 练习题

1. 运行 `code/main.py` 并观察服务器生成日志。用 SIGTERM 杀掉一个模拟服务器进程，观察客户端如何检测 EOF 并将该会话标记为死亡。

2. 实现命名空间前缀。当两个服务器暴露 `search` 时，将第二个重命名为 `<server>/search`。更新调度表并验证工具调用正确路由。

3. 为服务器重启添加连接池风格的退避：连续失败时的指数退避，上限 30 秒，三次失败后向用户发出通知。

4. 勾画一个支持 100 个并发 MCP 服务器的客户端。什么数据结构替代简单的调度字典？（提示：用于前缀命名空间的 trie，加上每服务器工具计数指标。）

5. 将客户端迁移到官方 MCP Python SDK。SDK 封装了 `stdio_client` 和 `ClientSession`。代码应从约 200 行缩减到约 40 行，同时保留多服务器路由。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| MCP 客户端 | "Agent 宿主" | 生成服务器并编排工具调用的进程 | MCP client |
| 会话状态 | "每服务器状态" | 能力、工具列表和待处理请求簿记 | Session |
| 合并命名空间 | "一个工具列表" | 跨所有活动服务器的扁平工具名称集 | Merged namespace |
| 命名空间冲突 | "两个服务器同工具" | 客户端必须前缀、拒绝或先到先得 | Namespace collision |
| 工具路由 | "谁接收这个调用？" | 从工具名到拥有服务器的分发 | Routing |
| 后台读取线程 | "非阻塞 stdout" | 将服务器 stdout 排入队列的线程或任务 | Background reader |
| 采样回调 | "LLM 即服务" | 来自服务器的 `sampling/createMessage` 的客户端处理器 | Sampling callback |
| `notifications/*_changed` | "原语变更" | 客户端必须重新发现或重新读取的信号 | Mutation events |
| 重连策略 | "服务器死亡时" | 传输失败时的重启语义 | Reconnection policy |
| stdio 会话 | "进程=会话" | 无会话 ID；子进程生命周期就是会话 | Stdio session |

## 延伸阅读

- [Model Context Protocol — Client spec](https://modelcontextprotocol.io/specification/2025-11-25/client) — 权威客户端行为
- [MCP — Quickstart client guide](https://modelcontextprotocol.io/quickstart/client) — 使用 Python SDK 的 hello-world 客户端教程
- [MCP Python SDK — client module](https://github.com/modelcontextprotocol/python-sdk) — 权威 `ClientSession` 和 `stdio_client`
- [MCP TypeScript SDK — Client](https://github.com/modelcontextprotocol/typescript-sdk) — TS 并行实现
- [VS Code — MCP in extensions](https://code.visualstudio.com/api/extension-guides/ai/mcp) — VS Code 如何在单个编辑器宿主中多路复用多个 MCP 服务器
