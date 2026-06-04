# MCP 资源与提示 — 工具之外的上下文暴露

> 工具获得了 MCP 90% 的关注，但另外两个服务器原语解决不同的问题。Resources 暴露可读数据；Prompts 暴露可复用的模板作为斜杠命令。许多服务器应该使用 resources 而非将读操作包装为 tools，使用 prompts 而非在客户端提示中硬编码工作流。本课命名决策规则并走通 `resources/*` 和 `prompts/*` 消息。

> **【中文解读】** 工具获得了 MCP 90% 的关注，但另外两个服务器原语解决不同的问题。Resources 暴露可读数据；Prompts 暴露可复用的模板作为斜杠命令。许多服务器应该使用 resources 而非将读操作包装为 tools，使用 prompts 而非在客户端提示中硬编码工作流。

> **【拓展：Resources vs Tools 选择】** 在 MCP 设计中，Resources 用于只读数据暴露（如文件内容、数据库记录），Tools 用于有副作用的操作（如创建、删除、发送）。错误地将读操作包装为 tool 会增加不必要的模型决策负担。Prompts 作为斜杠命令模板，让用户快速触发预设工作流。

**类型：** 构建
**语言：** Python（标准库，resource + prompt 处理器）
**前置条件：** Phase 13 · 07（MCP 服务器）
**时间：** 约 45 分钟

## 学习目标

- 为给定领域决定将能力暴露为 tool、resource 还是 prompt。
- 实现 `resources/list`、`resources/read`、`resources/subscribe` 并处理 `notifications/resources/updated`。
- 实现带有参数模板的 `prompts/list` 和 `prompts/get`。
- 认识宿主何时将 prompts 暴露为斜杠命令 vs 自动注入的上下文。

## 问题引入

一个简单的笔记 MCP 服务器把所有功能都暴露为工具：`notes_read`、`notes_list`、`notes_search`。这把每个数据访问都包装为模型驱动的工具调用。后果：

- 模型必须决定每个可能受益于上下文的查询是否调用 `notes_read`。
- 只读内容无法被订阅或流式传输到宿主的侧面板。
- 客户端 UI（Claude Desktop 的资源附件面板、Cursor 的"包含文件"选择器）无法展示数据。

正确的拆分：将数据暴露为 resource，将变更或计算动作暴露为 tool，将可复用的多步工作流暴露为 prompt。每种原语有其特定的 UX 呈现和访问模式。

## 核心概念

### Tools vs resources vs prompts — 决策规则

| 能力 | 原语 |
|------|------|
| 用户想搜索、过滤或转换数据 | tool |
| 用户想让宿主将数据包含为上下文 | resource |
| 用户想要可重复运行的模板化工作流 | prompt |

判断标准：如果模型在每次相关查询时都要调用它，它是工具。如果用户想把它附加到对话中，它是资源。如果整个多步工作流是用户想重复使用的单元，它是提示。

### Resources

`resources/list` 返回 `{resources: [{uri, name, mimeType, description?}]}`。`resources/read` 接收 `{uri}` 并返回 `{contents: [{uri, mimeType, text | blob}]}`。

URI 可以是任何可寻址的内容：

- `file:///Users/alice/notes/mcp.md`
- `postgres://my-db/query/SELECT ...`
- `notes://note-14`（自定义方案）
- `memory://session-2026-04-22/recent`（服务器特定）

`contents[]` 同时支持文本和二进制。二进制使用 `blob` 作为 base64 编码的字符串加上 `mimeType`。

### 资源订阅

在能力中声明 `{resources: {subscribe: true}}`。客户端调用 `resources/subscribe {uri}`。服务器在资源变化时发送 `notifications/resources/updated {uri}`。客户端重新读取。

用例：一个笔记服务器的资源是磁盘上的文件；文件监视器触发更新通知；Claude Desktop 在宿主外编辑时将文件重新拉入上下文。

### 资源模板（2025-11-25 新增）

`resourceTemplates` 让你暴露一个参数化 URI 模式：`notes://{id}`，其中 `id` 作为补全目标。客户端可以在资源选择器中自动补全 ID。

### Prompts

`prompts/list` 返回 `{prompts: [{name, description, arguments?}]}`。`prompts/get` 接收 `{name, arguments}` 并返回 `{description, messages: [{role, content}]}`。

prompt 是一个填充为消息列表的模板，宿主将其喂给模型。例如，一个 `code_review` prompt 接收一个 `file_path` 参数并返回三消息序列：一条系统消息、一条包含文件正文的用户消息和一条带有推理模板的助手启动消息。

### 宿主和 Prompts

Claude Desktop、VS Code 和 Cursor 将 prompts 在聊天 UI 中暴露为斜杠命令。用户输入 `/code_review` 并从表单中选择参数。服务器的 prompt 是"用户快捷方式"和"发送给模型的完整 prompt"之间的契约。

并非每个客户端都支持 prompts——检查能力协商。声明了 prompt 能力但客户端不支持 prompt 的服务器只是看不到斜杠命令。

### "列表变更"通知

Resources 和 prompts 都在集合变化时发出 `notifications/list_changed`。一个刚导入了 20 条新笔记的笔记服务器发出 `notifications/resources/list_changed`；客户端重新调用 `resources/list` 来获取新增内容。

### 内容类型约定

文本：`mimeType: "text/plain"`、`text/markdown`、`application/json`。
二进制：`image/png`、`application/pdf`，加上 `blob` 字段。
MCP Apps（第 14 课）：`text/html;profile=mcp-app` 在 `ui://` URI 中。

### 动态资源

资源 URI 不必对应静态文件。`notes://recent` 可以每次读取时返回最新 5 条笔记。`db://query/users/active` 可以执行参数化查询。服务器可以自由地动态计算内容。

规则：如果客户端可以按 URI 缓存，则 URI 必须稳定。如果是一次性计算，URI 应包含时间戳或随机数以避免缓存过期。

### 订阅 vs 轮询

支持订阅的客户端通过 `notifications/resources/updated` 获得服务器推送。不支持订阅的客户端或不支持它的宿主通过重新读取来轮询。两者都符合规范。服务器的能力声明告诉客户端它支持哪种。

订阅的成本：服务器上的每会话状态（谁订阅了什么）。保持订阅集合有界；断开连接的客户端应该超时。

### Prompts vs 系统 Prompts

MCP 中的 Prompts 不是系统提示。宿主的系统提示（自己的操作指令）和 MCP prompts（服务器提供的模板，由用户调用）并存。行为良好的客户端不会让服务器 prompt 覆盖自己的系统提示；它将它们分层叠加。

## 用框架实现

`code/main.py` 用以下内容扩展了第 07 课的笔记服务器：

- 每笔记资源（`notes://note-1` 等），支持 `resources/subscribe`。
- 一个渲染为三消息模板的 `review_note` prompt。
- 一个在笔记被修改时发出 `notifications/resources/updated` 的文件监视器模拟。
- 一个始终返回最新 5 条笔记的 `notes://recent` 动态资源。

运行演示查看完整流程。

## 产出物

本课产生 `outputs/skill-primitive-splitter.md`。给定一个拟议的 MCP 服务器，该技能将每个能力分类为 tool / resource / prompt 并附上理由。

## 练习题

1. 运行 `code/main.py`。观察初始资源列表，然后触发一次笔记编辑并验证 `notifications/resources/updated` 事件触发。

2. 添加一个 `resources/list_changed` 发射器：创建新笔记时，发送通知让客户端重新发现。

3. 为 GitHub MCP 服务器设计三个 prompts：`summarize_pr`、`triage_issue`、`release_notes`。每个都带参数 Schema。prompt 正文应该无需进一步编辑即可运行。

4. 取第 07 课服务器中的一个现有工具，分类它应该保持为工具还是拆分为 resource + tool 对。用一句话说明理由。

5. 阅读规范的 `server/resources` 和 `server/prompts` 部分。识别 `resources/read` 中一个很少填充但规范支持的字段。提示：查看资源内容上的 `_meta`。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 资源 | "暴露的数据" | 宿主可以读取的 URI 可寻址内容 | Resource |
| 资源 URI | "数据指针" | 带方案前缀的标识符（`file://`、`notes://` 等） | Resource URI |
| `resources/subscribe` | "监视变更" | 对特定 URI 的客户端选择加入的服务器推送更新 | Resource subscribe |
| `notifications/resources/updated` | "资源变了" | 向客户端发出已订阅资源有新内容的信号 | Resource updated notification |
| 资源模板 | "参数化 URI" | 带有宿主选择器补全提示的 URI 模式 | Resource template |
| 提示模板 | "斜杠命令模板" | 带有参数槽的命名多消息模板 | Prompt |
| 提示参数 | "模板输入" | 宿主在渲染前收集的类型化参数 | Prompt arguments |
| `prompts/get` | "渲染模板" | 服务器返回填充后的消息列表 | Render prompt |
| 内容块 | "类型化块" | `{type: text | image | resource | ui_resource}` | Content block |
| 斜杠命令 UX | "用户快捷方式" | 宿主将 prompts 显示为以 `/` 开头的命令 | Slash-command UX |

## 延伸阅读

- [MCP — Concepts: Resources](https://modelcontextprotocol.io/docs/concepts/resources) — 资源 URI、订阅和模板
- [MCP — Concepts: Prompts](https://modelcontextprotocol.io/docs/concepts/prompts) — 提示模板和斜杠命令集成
- [MCP — Server resources spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/resources) — 完整的 `resources/*` 消息参考
- [MCP — Server prompts spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/prompts) — 完整的 `prompts/*` 消息参考
- [MCP — Protocol info site: resources](https://modelcontextprotocol.info/docs/concepts/resources/) — 扩展官方文档的社区指南
