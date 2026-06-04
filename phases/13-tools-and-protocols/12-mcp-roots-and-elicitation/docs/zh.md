# Roots 与 Elicitation — 作用域与飞行中用户输入

> 硬编码路径在用户打开不同项目时就会出问题。预填的工具参数在用户信息不足时也会出错。Roots 将服务器限定在用户控制的一组 URI 中；Elicitation 在工具调用中途暂停，通过表单或 URL 向用户请求结构化输入。两个客户端原语，修复两个常见的 MCP 失败模式。SEP-1036（URL 模式 elicitation，2025-11-25）在 2026 年上半年之前是实验性的——在使用前检查 SDK 版本。

> **【中文解读】** 硬编码路径在用户打开不同项目时就会出问题。预填的工具参数在用户信息不足时也会出错。Roots 将服务器限定在用户控制的一组 URI 中；Elicitation 在工具调用中途暂停，通过表单或 URL 向用户请求结构化输入。两个客户端原语，修复两个常见的 MCP 失败模式。

> **【拓展：Roots→MCP 安全边界】** Roots 是 MCP 安全模型的基础。客户端通过声明 roots 控制服务器可以访问的文件/资源范围。例如 Claude Desktop 只允许 MCP 服务器访问用户打开的项目目录。Elicitation 则让工具在需要额外信息时安全地向用户请求，而非假设或幻觉参数值。

**类型：** 构建
**语言：** Python（标准库，roots + elicitation 演示）
**前置条件：** Phase 13 · 07（MCP 服务器）
**时间：** 约 45 分钟

## 学习目标

- 声明 `roots` 并响应 `notifications/roots/list_changed`。
- 将服务器文件操作限制在声明的根集内的 URI。
- 使用 `elicitation/create` 在工具调用中途向用户请求确认或结构化输入。
- 在表单模式和 URL 模式 elicitation 之间做出选择（后者是实验性的；漂移风险已注明）。

## 问题引入

笔记 MCP 服务器在生产中遇到两个具体的失败。

**路径假设问题。** 服务器针对 `~/notes` 编写。另一台笔记在 `~/Documents/Notes` 的用户会得到一个静默失败的工具调用（找不到文件）或更糟的情况——写入了错误的位置。

**用户可能知道但缺失的参数。** 用户要求"删除旧的 TPS 报告笔记"。模型调用 `notes_delete(title: "TPS report")` 但有 2023、2024 和 2025 三个匹配的笔记。工具无法猜测。以"模糊"失败很烦人；三个都删除是灾难性的。

Roots 修复第一个：客户端在 `initialize` 时声明服务器可以触碰的 URI 集合。Elicitation 修复第二个：服务器暂停工具调用并发送 `elicitation/create` 让用户选择哪一个。

## 核心概念

### Roots

客户端在 `initialize` 时声明根列表：

```json
{
  "capabilities": {"roots": {"listChanged": true}}
}
```

服务器然后可以调用 `roots/list`：

```json
{"roots": [{"uri": "file:///Users/alice/Documents/Notes", "name": "Notes"}]}
```

服务器必须将 roots 视为边界：根集外的任何文件读写都应被拒绝。这不是客户端强制执行的（服务器仍是用户信任的代码），而是符合规范的服务器遵守它。

当用户添加或移除根时，客户端发送 `notifications/roots/list_changed`。服务器重新调用 `roots/list` 并更新其边界。

### 为什么 roots 是客户端原语

Roots 由客户端声明，因为它们代表用户的同意模型。用户告诉 Claude Desktop"让这个笔记服务器访问这两个目录"。服务器不能扩大该范围。

### Elicitation：表单模式默认

`elicitation/create` 接受一个表单 Schema 加上自然语言提示：

```json
{
  "method": "elicitation/create",
  "params": {
    "message": "Delete 'TPS report'? Multiple notes match; pick one.",
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
```

客户端渲染表单，收集用户回答，返回：

```json
{
  "action": "accept",
  "content": {"note_id": "note-14", "confirm": true}
}
```

三种可能的动作：`accept`（用户填写了）、`decline`（用户关闭了）、`cancel`（用户中止了整个工具调用）。

表单 Schema 是扁平的——v1 中不支持嵌套对象。SDK 通常拒绝比单层更复杂的任何内容。

### Elicitation：URL 模式（SEP-1036，实验性）

2025-11-25 新增。服务器不发送 Schema 而是发送 URL：

```json
{
  "method": "elicitation/create",
  "params": {
    "message": "Sign in to GitHub",
    "url": "https://github.com/login/oauth/authorize?client_id=..."
  }
}
```

客户端在浏览器中打开 URL，等待完成，用户回来时返回。适用于 OAuth 流程、支付授权和文档签署——表单不够用的场景。

漂移风险提示：SEP-1036 响应形状仍在稳定中；一些 SDK 返回回调 URL，其他返回完成令牌。在生产中使用 URL 模式前阅读 SDK 的发布说明。

### 何时使用 elicitation

- 破坏性操作前的用户确认（destructive hint + elicitation）。
- 消歧义（从 N 个匹配中选择一个）。
- 首次运行设置（API 密钥、目录、偏好）。
- OAuth 风格的流程（URL 模式）。

### 何时不使用 elicitation

- 填充模型本可以用散文询问的工具必填参数。使用正常的重新提问，而非 elicitation 对话。
- 高频调用。Elicitation 中断对话；不要在循环中触发它。
- 服务器可以在事后验证的任何内容。验证，返回错误，让模型用文本向用户询问。

### 人在回路桥梁

Elicitation 加 sampling 一起构成了 MCP 的"人在回路"模型。服务器的 Agent 循环可以暂停以获取用户输入（elicitation）或模型推理（sampling）。Phase 13 · 11 覆盖了 sampling；本课覆盖 elicitation。将它们放在一起实现完整的飞行中控制。

## 用框架实现

`code/main.py` 用以下内容扩展了笔记服务器：

- `roots/list` 响应，服务器在根列表变更通知后重新查询。
- 一个在多个笔记匹配时使用 `elicitation/create` 消歧义的 `notes_delete` 工具。
- 一个使用 URL 模式 elicitation 打开首次运行配置页面（模拟）的 `notes_setup` 工具。
- 一个拒绝在声明的 roots 之外的 URI 操作的边界检查。

演示运行三个场景：正常路径（一个匹配）、消歧义（三个匹配，elicitation 触发）、根外写入（被拒绝）。

## 产出物

本课产生 `outputs/skill-elicitation-form-designer.md`。给定一个可能需要用户确认或消歧义的工具，该技能设计 elicitation 表单 Schema 和消息模板。

## 练习题

1. 运行 `code/main.py`。触发消歧义路径；确认模拟的用户答案被路由回工具。

2. 添加一个每次都需要 elicitation 确认的新工具 `notes_archive`（destructive hint）。检查 UX：这与模型用文本重新询问相比如何？

3. 为首次运行 OAuth 流程实现 URL 模式 elicitation。注意漂移风险并添加 SDK 版本守卫。

4. 扩展 `roots/list` 处理：当通知到达时，服务器应原子性地重新读取并重新扫描可能现在超出范围的打开文件句柄。

5. 阅读 GitHub 上的 SEP-1036 议题讨论线程。识别一个影响服务器应如何处理 URL 模式回调的开放问题。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 根路径 | "同意边界" | 客户端允许服务器触碰的 URI | Root |
| 查询根路径 | "服务器请求范围" | 客户端返回当前根集 | `roots/list` |
| 根路径变更通知 | "用户更改了范围" | 客户端发出根集已变化的信号 | `notifications/roots/list_changed` |
| 用户征询 | "在调用中问用户" | 服务器发起的结构化用户输入请求 | Elicitation |
| 征询请求方法 | "那个方法" | elicitation 请求的 JSON-RPC 方法 | `elicitation/create` |
| 表单模式 | "Schema 驱动表单" | 在客户端 UI 中渲染为表单的扁平 JSON Schema | Form mode |
| URL 模式 | "浏览器重定向" | SEP-1036 实验性；打开 URL 并等待 | URL mode |
| 接受/拒绝/取消 | "用户响应结果" | 服务器处理的三个分支 | Accept/Decline/Cancel |
| 消歧义 | "选一个" | 工具有 N 个候选项时的常见 elicitation 用例 | Disambiguation |
| 扁平表单 | "仅顶层属性" | Elicitation Schema 不能嵌套 | Flat form |

## 延伸阅读

- [MCP — Client roots spec](https://modelcontextprotocol.io/specification/draft/client/roots) — 权威 roots 参考
- [MCP — Client elicitation spec](https://modelcontextprotocol.io/specification/draft/client/elicitation) — 权威 elicitation 参考
- [Cisco — What's new in MCP elicitation, structured content, OAuth enhancements](https://blogs.cisco.com/developer/whats-new-in-mcp-elicitation-structured-content-and-oauth-enhancements) — 2025-11-25 新增内容演练
- [MCP — GitHub SEP-1036](https://github.com/modelcontextprotocol/modelcontextprotocol) — URL 模式 elicitation 提案（实验性，漂移风险）
- [The New Stack — How elicitation brings human-in-the-loop to AI tools](https://thenewstack.io/how-elicitation-in-mcp-brings-human-in-the-loop-to-ai-tools/) — UX 演练
