# A2A — Agent 间通信协议

> MCP 是 Agent-工具协议。A2A (Agent2Agent) 是 Agent-Agent 协议——让不同框架构建的不透明 Agent 互相协作的开放协议。Google 2025年4月发布，2025年6月捐给 Linux 基金会，2026年4月发布 v1.0，150+支持者包括 AWS、Cisco、Microsoft、Salesforce、SAP、ServiceNow。吸收了 IBM 的 ACP，添加了 AP2 支付扩展。本课走通 Agent Card、Task 生命周期和两种传输绑定。

> **【中文解读】** MCP 是 Agent-工具协议，A2A 是 Agent-Agent 协议——让不同框架构建的不透明 Agent 互相协作的开放协议。Google 2025年4月发布，2025年6月捐给 Linux 基金会，2026年4月发布 v1.0，150+支持者。

> **【拓展】** A2A 与 MCP 是互补而非替代关系。MCP 用于调用具体工具（透明），A2A 用于将整个任务委托给另一个 Agent（不透明）。许多生产系统两者并用：Agent 用 MCP 作为工具层，用 A2A 作为协作层。

**类型：** 构建
**语言：** Python（标准库，Agent Card + Task 线束）
**前置条件：** Phase 13 · 06（MCP 基础），Phase 13 · 08（MCP 客户端）
**时间：** 约 75 分钟

## 学习目标

- 区分 Agent-工具（MCP）与 Agent-Agent（A2A）用例。
- 在 `/.well-known/agent.json` 发布带有技能和端点元数据的 Agent Card。
- 走通 Task 生命周期（submitted -> working -> input-required -> completed / failed / canceled / rejected）。
- 使用带 Parts（text、file、data）的 Messages 和 Artifacts 作为输出。

## 问题引入

客服 Agent 需要将报告撰写委托给专门的写作 Agent。A2A 之前的选择：

- 定制 REST API。可以工作但每对都是一次性的。
- 共享代码库。要求两个 Agent 运行同一框架。
- MCP。不适合：MCP 用于调用工具，而非两个 Agent 在保持各自不透明内部推理的同时协作。

A2A 填补了空白。它将交互建模为一个 Agent 向另一个 Agent 发送 Task，具有生命周期、消息和工件。被调用 Agent 的内部状态保持不透明——调用者只看到任务状态转换和最终输出。

A2A 是"让不同框架的 Agent 互相通信"的协议。它不替代 MCP；两者是互补的。

## 核心概念

### Agent Card

每个 A2A 兼容的 Agent 在 `/.well-known/agent.json` 发布卡片：

```json
{
  "schemaVersion": "1.0",
  "name": "research-agent",
  "description": "Summarizes academic papers and drafts citations.",
  "url": "https://research.example.com/a2a",
  "version": "1.2.0",
  "skills": [
    {
      "id": "summarize_paper",
      "name": "Summarize a paper",
      "description": "Read a paper PDF and produce a 3-paragraph summary.",
      "inputModes": ["text", "file"],
      "outputModes": ["text", "artifact"]
    }
  ],
  "capabilities": {"streaming": true, "pushNotifications": true}
}
```

发现基于 URL：获取卡片，学习 A2A 端点 URL，枚举技能。

### 签名 Agent Card（AP2）

AP2 扩展（2025年9月）为 Agent Card 添加密码学签名。发布者用自己的 JWT 签名卡片；消费者验证。防止冒充。

### Task 生命周期

```
submitted -> working -> completed | failed | canceled | rejected
             -> input_required -> working (通过消息循环)
```

客户端用 `tasks/send` 发起。被调用 Agent 通过状态转换；客户端通过 SSE 订阅状态更新或轮询。

### Messages 和 Parts

消息携带一个或多个 Parts：

- `text` — 纯内容。
- `file` — 带 mimeType 的 base64 blob。
- `data` — 类型化 JSON 载荷（被调用 Agent 的结构化输入）。

### Artifacts

输出是 Artifacts，而非原始字符串。Artifact 是命名的、类型化的输出：

```json
{
  "name": "summary",
  "parts": [{"type": "text", "text": "..."}],
  "mimeType": "text/markdown"
}
```

Artifacts 可以作为块流式传输。调用者累积。

### 两种传输绑定

1. **HTTP 上的 JSON-RPC。** `/a2a` 端点，POST 用于请求，可选 SSE 用于流式传输。默认绑定。
2. **gRPC。** 用于 gRPC 原生的企业环境。

两种绑定携带相同的逻辑消息形状。

### 不透明性保持

关键设计原则：被调用 Agent 的内部状态是不透明的。调用者看到任务状态和工件。被调用 Agent 的链式思考、工具调用、子 Agent 委托——全部不可见。这与 MCP 不同，MCP 的工具调用是透明的。

理由：A2A 使竞争对手可以协作而不暴露内部实现。A2A 可以是"调用这个客服 Agent"而调用者不知道该 Agent 如何实现服务。

### 时间线

- **2025-04-09。** Google 宣布 A2A。
- **2025-06-23。** 捐赠给 Linux 基金会。
- **2025-08。** 吸收 IBM 的 ACP。
- **2025-09。** AP2 扩展（Agent 支付）发布。
- **2026-04。** v1.0 发布，150+ 支持组织。

### 与 MCP 的关系

| 维度 | MCP | A2A |
|------|-----|-----|
| 用例 | Agent-工具 | Agent-Agent |
| 不透明性 | 透明工具调用 | 不透明内部推理 |
| 典型调用者 | Agent 运行时 | 另一个 Agent |
| 状态 | 工具调用结果 | 带生命周期的 Task |
| 授权 | OAuth 2.1（Phase 13 · 16） | JWT 签名的 Agent Card（AP2） |
| 传输层 | Stdio / Streamable HTTP | HTTP 上的 JSON-RPC / gRPC |

需要调用特定工具时用 MCP。需要将整个任务委托给另一个 Agent 时用 A2A。许多生产系统两者并用：Agent 用 MCP 作为工具层，用 A2A 作为协作层。

## 用框架实现

`code/main.py` 实现最小 A2A 线束：研究 Agent 发布卡片，写作 Agent 接收 `tasks/send`（含 PDF 和文本指令的 Parts），经历 working -> input_required -> working -> completed 生命周期，返回文本 Artifact。全部标准库；使用内存传输聚焦消息形状。

关注点：

- Agent Card JSON 形状。
- Task id 分配和状态转换。
- 带混合类型 parts 的消息。
- 任务中途的 input-required 分支。
- 完成时的 Artifact 返回。

## 产出物

本课产生 `outputs/skill-a2a-agent-spec.md`。给定一个新的可被其他 Agent 调用的 Agent，该技能生成 Agent Card JSON、技能模式和端点蓝图。

## 练习题

1. 运行 `code/main.py`。追踪完整 Task 生命周期，包括被调用 Agent 请求澄清的 input-required 暂停。

2. 添加签名 Agent Card。用 HMAC 对卡片规范 JSON 签名。编写验证器并确认它在变更的卡片上失败。

3. 实现任务流式传输：写作 Agent 通过 SSE 发出三个增量 artifact 块，调用者累积它们。

4. 设计一个包装 MCP 服务器的 A2A Agent。将每个 MCP 工具映射为 A2A 技能。注意权衡——损失了什么不透明性？

5. 阅读 A2A v1.0 公告并识别截至 2026 年 4 月尚未被任何框架实现的一个功能。（提示：与多跳任务委托有关。）

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| A2A | "Agent 间协议" | 不透明 Agent 协作的开放协议 | Agent-to-Agent Protocol |
| Agent Card | "`.well-known/agent.json`" | 描述 Agent 技能和端点的发布元数据 | Agent Card |
| 技能 | "可调用单元" | Agent 支持的命名操作（类似 MCP 工具） | Skill |
| 任务 | "委托单元" | 带生命周期和最终工件的作业项 | Task |
| 消息 | "任务输入" | 携带 Parts（text、file、data） | Message |
| 部件 | "类型化块" | 消息的 `text` / `file` / `data` 元素 | Part |
| 工件 | "任务输出" | 完成时返回的命名类型化输出 | Artifact |
| AP2 | "Agent 支付协议" | 用于信任和支付的签名 Agent Card 扩展 | Agent Payments Protocol |
| 不透明性 | "黑盒协作" | 被调用方内部对调用者隐藏 | Opacity |
| 输入要求 | "任务暂停" | Agent 需要更多信息时的生命周期状态 | Input-required |

## 延伸阅读

- [a2a-protocol.org](https://a2a-protocol.org/latest/) — 权威 A2A 规范
- [a2aproject/A2A — GitHub](https://github.com/a2aproject/A2A) — 权威实现和 SDK
- [Linux Foundation — A2A launch press release](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) — 2025 年 6 月治理转移
- [Google Cloud — A2A protocol upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade) — 路线图和合作伙伴势头
- [Google Dev — A2A 1.0 milestone](https://discuss.google.dev/t/the-a2a-1-0-milestone-ensuring-and-testing-backward-compatibility/352258) — v1.0 发布说明和向后兼容指南
