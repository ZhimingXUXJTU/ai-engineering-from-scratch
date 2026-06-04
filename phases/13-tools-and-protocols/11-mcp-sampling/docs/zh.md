# MCP 采样 — 服务器请求 LLM 补全与 Agent 循环

> 大多数 MCP 服务器是简单的执行器：接收参数、运行代码、返回内容。Sampling 让服务器反转方向：它请求客户端的 LLM 做出决策。这使服务器可以承载 Agent 循环，而无需拥有任何模型凭证。SEP-1577（2025-11-25 合并）在 sampling 请求中添加了 tools，使循环可以包含更深的推理。漂移风险提示：SEP-1577 的 tool-in-sampling 形状在 2026 年 Q1 之前是实验性的，SDK API 仍在稳定中。

> **【中文解读】** 大多数 MCP 服务器是简单的执行器：接收参数、运行代码、返回内容。Sampling 让服务器反转方向：它请求客户端的 LLM 做出决策。这使服务器可以承载 Agent 循环，而无需拥有任何模型凭证。SEP-1577 在 sampling 请求中添加了 tools，使循环可以包含更深的推理。

> **【拓展：Sampling→MCP Agent 循环】** Sampling 是 MCP 实现 Agent 循环的关键原语。传统模式下，MCP 服务器只是被动执行工具。通过 Sampling，服务器可以主动请求客户端的 LLM 进行推理，从而在不持有 API 密钥的情况下实现多步 Agent 工作流。这是 MCP 与 Function Calling 的重要区别之一。

**类型：** 构建
**语言：** Python（标准库，sampling 线束）
**前置条件：** Phase 13 · 07（MCP 服务器），Phase 13 · 10（资源和提示）
**时间：** 约 75 分钟

## 学习目标

- 解释 `sampling/createMessage` 解决了什么问题（服务器承载循环而无需服务器端 API 密钥）。
- 实现一个服务器，请求客户端在多轮 prompt 上进行采样并返回补全。
- 使用 `modelPreferences`（成本/速度/智能优先级）引导客户端模型选择。
- 构建一个通过 sampling 内部迭代而非硬编码行为的 `summarize_repo` 工具。

## 问题引入

一个有用的 MCP 服务器用于代码摘要工作流需要：遍历文件树，选择要读取的文件，综合摘要，然后返回。LLM 推理在哪里发生？

选项 A：服务器调用自己的 LLM。需要 API key，服务器端计费，每个用户都昂贵。

选项 B：服务器返回原始内容；客户端的 Agent 做推理。可以工作但将服务器逻辑移入客户端 prompt，这很脆弱。

选项 C：服务器通过 `sampling/createMessage` 请求客户端的 LLM。服务器保留算法（哪些文件要读、做几轮）而客户端保留计费和模型选择。服务器完全没有凭证。

Sampling 就是选项 C。它是受信任的服务器可以在不作为完整 LLM 宿主的情况下承载 Agent 循环的机制。

## 核心概念

### `sampling/createMessage` 请求

服务器发送：

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "sampling/createMessage",
  "params": {
    "messages": [{"role": "user", "content": {"type": "text", "text": "..."}}],
    "systemPrompt": "...",
    "includeContext": "none",
    "modelPreferences": {
      "costPriority": 0.3,
      "speedPriority": 0.2,
      "intelligencePriority": 0.5,
      "hints": [{"name": "claude-3-5-sonnet"}]
    },
    "maxTokens": 1024
  }
}
```

客户端运行其 LLM，返回：

```json
{"jsonrpc": "2.0", "id": 42, "result": {
  "role": "assistant",
  "content": {"type": "text", "text": "..."},
  "model": "claude-3-5-sonnet-20251022",
  "stopReason": "endTurn"
}}
```

### `modelPreferences`

三个浮点数之和为 1.0：

- `costPriority`：偏好更便宜的模型。
- `speedPriority`：偏好更快的模型。
- `intelligencePriority`：偏好更有能力的模型。

加上 `hints`：服务器偏好的命名模型。客户端可能遵守也可能不遵守提示；客户端的用户配置总是优先。

### `includeContext`

三个值：

- `"none"` — 仅服务器提供的消息。默认。
- `"thisServer"` — 包含此服务器会话中的先前消息。
- `"allServers"` — 包含所有会话上下文。

`includeContext` 在 2025-11-25 起已被软弃用，因为它泄漏跨服务器上下文，存在安全隐患。偏好 `"none"` 并在消息中传递显式上下文。

### 带工具的 Sampling（SEP-1577）

2025-11-25 新增：sampling 请求可以包含 `tools` 数组。客户端使用这些工具运行完整的工具调用循环。这让服务器可以通过客户端的模型承载 ReAct 风格的 Agent 循环。

客户端循环：采样，如果调用了工具则执行，再次采样，返回最终助手消息。这在 2026 年 Q1 之前是实验性的；SDK 签名可能仍有变化。

### 人在回路

客户端必须在运行 sample 之前向用户展示服务器要求模型做什么。恶意服务器可以使用 sampling 操纵用户会话（"对用户说 X 让他们点击 Y"）。Claude Desktop、VS Code 和 Cursor 将 sampling 请求显示为用户可以拒绝的确认对话框。

2026 年共识：没有人工确认的 sampling 是一个危险信号。网关（Phase 13 · 17）可以自动批准低风险 sampling 并自动拒绝可疑的。

### 服务器承载的无需 API 密钥的循环

经典用例：一个没有自己 LLM 访问权限的代码摘要 MCP 服务器。它做：

1. 遍历仓库结构。
2. 调用 `sampling/createMessage`："选择最可能描述此仓库用途的五个文件。"
3. 读取这些文件。
4. 用文件内容调用 `sampling/createMessage`："用三段话总结仓库。"
5. 将摘要作为 `tools/call` 结果返回。

服务器从未触碰 LLM API。客户端的用户使用自己的凭证为补全付费。

### 安全风险（Unit 42 披露，2026 Q1）

- **隐蔽采样。** 一个总是调用 sampling 说"用会话上下文中用户的电子邮件回复"的工具。Phase 13 · 15 覆盖攻击向量。
- **通过采样的资源盗窃。** 服务器要求客户端摘要攻击者的载荷，用户承担费用。
- **循环炸弹。** 服务器在紧密循环中调用 sampling。客户端必须强制执行每会话速率限制。

## 用框架实现

`code/main.py` 提供了一个假的服务器到客户端 sampling 线束。一个模拟的"summarize_repo"工具调用两轮 sampling（选择文件，然后摘要），假客户端返回预设响应。线束展示：

- 服务器发送带有 `modelPreferences` 的 `sampling/createMessage`。
- 客户端返回一个补全。
- 服务器继续其循环。
- 速率限制器限制每次工具调用的总采样调用数。

关注点：

- 服务器只暴露一个工具（`summarize_repo`）；所有推理发生在 sampling 调用中。
- 模型偏好加权客户端的模型选择；提示列出偏好的模型。
- 循环在 `stopReason: "endTurn"` 时终止。
- `max_samples_per_tool = 5` 限制捕获失控循环。

## 产出物

本课产生 `outputs/skill-sampling-loop-designer.md`。给定一个需要 LLM 调用的服务器端算法（研究、摘要、规划），该技能设计基于 sampling 的实现，包含正确的 modelPreferences、速率限制和安全确认。

## 练习题

1. 运行 `code/main.py`。将 `max_samples_per_tool` 改为 2 并观察速率限制截断。

2. 实现 SEP-1577 的 tool-in-sampling 变体：sampling 请求携带 `tools` 数组。验证客户端循环在返回最终补全前执行这些工具。注意漂移风险：SDK 签名在 2026 年上半年之前可能仍有变化。

3. 添加人在回路确认：在服务器第一次 `sampling/createMessage` 之前，暂停并等待用户批准。被拒绝的调用返回类型化的拒绝。

4. 添加按客户端会话键控的每用户速率限制器。同一用户的同服务器循环应共享预算。

5. 设计一个使用 sampling 选择要包含的块的 `summarize_pdf` 工具。勾画发送的消息。`modelPreferences.intelligencePriority` 在 0.1 vs 0.9 时如何改变行为？

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 采样 | "服务器到客户端 LLM 调用" | 服务器请求客户端模型进行补全 | Sampling |
| `sampling/createMessage` | "那个方法" | 采样请求的 JSON-RPC 方法 | Sampling request method |
| `modelPreferences` | "模型优先级" | 成本/速度/智能权重加名称提示 | Model preferences |
| `includeContext` | "跨会话泄漏" | 软弃用的上下文包含模式 | Include context |
| SEP-1577 | "采样中的工具" | 允许采样中的工具用于服务器承载的 ReAct | Tools in sampling |
| 人在回路 | "用户确认" | 客户端在运行前向用户展示采样请求 | Human-in-the-loop |
| 循环炸弹 | "失控采样" | 服务器端无限采样循环；客户端必须限速 | Loop bomb |
| 隐蔽采样 | "隐藏推理" | 恶意服务器在采样提示中隐藏意图 | Covert sampling |
| 资源盗用 | "使用用户的 LLM 预算" | 服务器强制客户端在不需要的采样上花费 | Resource theft |
| `stopReason` | "生成为什么停止" | `endTurn`、`stopSequence` 或 `maxTokens` | Stop reason |

## 延伸阅读

- [MCP — Concepts: Sampling](https://modelcontextprotocol.io/docs/concepts/sampling) — 采样的高级概述
- [MCP — Client sampling spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling) — 权威的 `sampling/createMessage` 形状
- [MCP — GitHub SEP-1577](https://github.com/modelcontextprotocol/modelcontextprotocol) — 采样中工具的规范演进提案（实验性）
- [Unit 42 — MCP attack vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) — 隐蔽采样和资源盗窃模式
- [Speakeasy — MCP sampling core concept](https://www.speakeasy.com/mcp/core-concepts/sampling) — 带客户端代码示例的演练
