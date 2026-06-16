# A2A — Agent-to-Agent Protocol | A2A：Agent 间通信协议

> MCP is agent-to-tool. A2A (Agent2Agent) is agent-to-agent — an open protocol for letting opaque agents built on different frameworks collaborate. Released by Google in April 2025, donated to the Linux Foundation in June 2025, reaching v1.0 in April 2026 with 150+ supporters including AWS, Cisco, Microsoft, Salesforce, SAP, and ServiceNow. It absorbed IBM's ACP and added the AP2 payments extension. This lesson walks the Agent Card, Task lifecycle, and the two transport bindings.

> **【中文解读】** MCP 是 Agent-工具协议，A2A 是 Agent-Agent 协议——让不同框架构建的不透明 Agent 互相协作的开放协议。Google 2025年4月发布，2025年6月捐给 Linux 基金会，2026年4月发布 v1.0，150+支持者包括 AWS、Cisco、Microsoft、Salesforce、SAP、ServiceNow。吸收了 IBM 的 ACP，添加了 AP2 支付扩展。

> **【拓展】** A2A 与 MCP 是互补而非替代关系。MCP 用于调用具体工具（透明），A2A 用于将整个任务委托给另一个 Agent（不透明）。许多生产系统两者并用：Agent 用 MCP 作为工具层，用 A2A 作为协作层。Agent Card（`/.well-known/agent.json`）类似 MCP 的工具发现机制，但描述的是 Agent 的能力而非工具。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·06（MCP fundamentals）和 13·08（MCP client）——理解 MCP 是 agent-to-tool，本节是 agent-to-agent；(2) HTTP + JSON-RPC 基础；(3) SSE 或轮询机制——A2A Task 状态订阅；(4) 异步任务概念，可参考 Phase 13·13。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, Agent Card + Task harness) | **语言:** Python (stdlib, Agent Card + Task harness)
**Prerequisites:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Distinguish agent-to-tool (MCP) from agent-to-agent (A2A) use cases.
  中文翻译：区分 Agent-工具（MCP）和 Agent-Agent（A2A）用例。
- Publish an Agent Card at `/.well-known/agent.json` with skills and endpoint metadata.
  中文翻译：在 `/.well-known/agent.json` 发布带技能和端点元数据的 Agent Card。
- Walk the Task lifecycle (submitted -> working -> input-required -> completed / failed / canceled / rejected).
  中文翻译：走通 Task 生命周期（submitted -> working -> input-required -> completed / failed / canceled / rejected）。
- Use Messages with Parts (text, file, data) and Artifacts as outputs.

> **【中文解读】** 学习目标：区分 Agent-工具（MCP）与 Agent-Agent（A2A）用例；发布 Agent Card；走通 Task 生命周期；使用带 Parts 的 Messages 和 Artifacts 输出。

## The Problem | 问题引入

> **【中文解读】** 客服 Agent 需要将报告撰写委托给专门的写作 Agent。A2A 之前的选择（定制 REST API、共享代码库、MCP）都不适合。A2A 将交互建模为一个 Agent 向另一个 Agent 发送 Task，具有生命周期、消息和工件。被调用 Agent 的内部状态保持不透明——调用者只看到任务状态转换和最终输出。

A customer-service agent needs to delegate report-writing to a specialized writer agent. Options pre-A2A:

> 客服 Agent 需要将报告撰写委托给专门的写作 Agent。A2A 之前的选项：

- Custom REST API. Works but every pairing is a one-off.
  中文翻译：定制 REST API。可行但每个配对都是一次性的。
- Shared codebase. Requires the two agents to run the same framework.
  中文翻译：共享代码库。要求两个 Agent 运行相同框架。
- MCP. Doesn't fit: MCP is for calling tools, not for two agents collaborating while preserving each agent's opaque internal reasoning.
  中文翻译：MCP。不合适：MCP 用于调用工具，而非两个 Agent 在保持各自不透明内部推理下协作。

A2A fills the gap. It models the interaction as one agent sending a Task to another, with a lifecycle, messages, and artifacts. The called agent's internal state stays opaque — the caller sees only task state transitions and eventual outputs.

> A2A 填补空白。它将交互建模为一个 Agent 向另一个发送 Task，带生命周期、消息和工件。被调用 Agent 的内部状态保持不透明——调用者只看到任务状态转换和最终输出。

A2A is the "let agents across frameworks talk to each other" protocol. It does not replace MCP; the two are complementary.

> A2A 是"让跨框架 Agent 互相交谈"的协议。它不替代 MCP；两者互补。

> 💡 **【类比】** A2A vs MCP 像公司"外包项目" vs "公司内调用工具"。MCP 是工程师（agent）用计算器（tool）——他知道计算器怎么工作、用完就完了，是工具调用。A2A 是公司 A 把整个项目（task）外包给公司 B（另一个 agent）——A 不知道 B 内部怎么做的（不透明），只看交付物（artifact）；B 是独立法人有自己的工作流、自己的工具、自己的内部状态。A2A 关心的是任务边界、交付格式、状态回报，不关心 B 用什么框架（LangChain 还是 AutoGen）实现。

## The Concept | 核心概念

### Agent Card

> **【中文解读】** Agent Card：每个 A2A 兼容的 Agent 在 `/.well-known/agent.json` 发布卡片，包含名称、描述、URL、版本、技能列表和能力声明。发现是基于 URL 的——获取卡片，学习 A2A 端点 URL，枚举技能。

Every A2A-compliant agent publishes a card at `/.well-known/agent.json`:

> 每个 A2A 兼容 Agent 在 `/.well-known/agent.json` 发布卡片：

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

Discovery is URL-based: fetch the card, learn the URL of the A2A endpoint, enumerate skills.

> 发现基于 URL：获取卡片、学习 A2A 端点 URL、枚举技能。

### Signed Agent Cards (AP2)

The AP2 extension (September 2025) adds cryptographic signatures to Agent Cards. A publisher signs its own card with a JWT; consumers verify. Prevents impersonation.

> AP2 扩展（2025 年 9 月）为 Agent Card 添加加密签名。发布者用 JWT 签署自己的卡片；消费者验证。防止冒充。

### Task lifecycle

> **【中文解读】** Task 生命周期：submitted -> working -> completed | failed | canceled | rejected；working 中可暂停为 input_required（需要更多信息），通过消息循环回到 working。客户端通过 `tasks/send` 发起，通过 SSE 订阅状态更新或轮询。

```
submitted -> working -> completed | failed | canceled | rejected
             -> input_required -> working (loop via message)
```

Clients initiate with `tasks/send`. The called agent transitions through states; clients subscribe to state updates via SSE or poll.

> 客户端用 `tasks/send` 发起。被调用 Agent 通过状态转换；客户端通过 SSE 或轮询订阅状态更新。

> ⚠️ **【易错点】** 场景：A2A 调用方在 `submitted` 状态后立刻等 `completed` 而不处理 `input_required` / 后果：被调用 Agent 需要补充信息时卡在 `input_required`，调用方误以为还在 `working` 永久等待，整个工作流死锁 / 修复：(1) 调用方必须实现完整的 task 生命周期状态机，每个状态都有 handler；(2) `input_required` 时主动拉取消息内容并触发新一轮 `tasks/send`；(3) 设置总超时（如 10 分钟），到达后 cancel task 并报错。

> 🤔 **【困惑】** Q: 既然 A2A 是 agent-to-agent，那 agent A 怎么知道 agent B 信任它、会不会拒绝？ A: 信任通过 Agent Card + AP2 签名建立：(1) Agent Card 描述能力，AP2 用 JWT 签名防冒充；(2) 调用前 A 通常已通过 OAuth 等机制拿到 B 的访问 token；(3) B 可以拒绝（`rejected` 状态），如调用方没付费（AP2 支付扩展）、权限不足、负载过满；(4) A 需要实现拒绝后的降级路径——找别的 agent 或回退到本地处理。A2A 假设"协作但有边界"。

### Messages and Parts

A message carries one or more Parts:

> 一条消息携带一个或多个 Part：

- `text` — plain content.
  中文翻译：`text`——纯文本内容。
- `file` — base64 blob with mimeType.
  中文翻译：`file`——base64 blob 带 mimeType。
- `data` — typed JSON payload (structured input for the called agent).
  中文翻译：`data`——类型化 JSON 负载（被调用 Agent 的结构化输入）。

Example:

```json
{
  "role": "user",
  "parts": [
    {"type": "text", "text": "Summarize this paper."},
    {"type": "file", "file": {"name": "paper.pdf", "mimeType": "application/pdf", "bytes": "..."}},
    {"type": "data", "data": {"targetLength": "3 paragraphs"}}
  ]
}
```

### Artifacts

Outputs are Artifacts, not raw strings. An Artifact is a named, typed output:

> 输出是 Artifact，而非裸字符串。Artifact 是命名的类型化输出：

```json
{
  "name": "summary",
  "parts": [{"type": "text", "text": "..."}],
  "mimeType": "text/markdown"
}
```

Artifacts can be streamed as chunks. The caller accumulates.

> Artifact 可作为块流式传输。调用者累积。

### Two transport bindings

1. **JSON-RPC over HTTP.** `/a2a` endpoint, POST for requests, optional SSE for streaming. Default binding.
  中文翻译：**JSON-RPC over HTTP。** `/a2a` 端点、POST 用于请求、可选 SSE 用于流式。默认绑定。
2. **gRPC.** For enterprise environments where gRPC is native.
  中文翻译：**gRPC。** 用于 gRPC 原生的企业环境。

Both bindings carry the same logical message shape.

> 两种绑定携带相同逻辑消息形态。

### Opacity preservation

> **【中文解读】** 不透明性保持：被调用 Agent 的内部状态是不透明的。调用者只看到任务状态和工件，看不到链式思考、工具调用或子 Agent 委托。这让竞争对手可以协作而不暴露内部实现。

A key design principle: the called agent's internal state is opaque. The caller sees task state and artifacts. The called agent's chain-of-thought, its tool calls, its sub-agent delegation — all invisible. This is different from MCP, where tool calls are transparent.

> 关键设计原则：被调用 Agent 的内部状态不透明。调用者看到任务状态和工件。被调用 Agent 的思维链、工具调用、子 Agent 委托——全部不可见。这与 MCP 不同，MCP 的工具调用是透明的。

Rationale: A2A enables competitors to collaborate without revealing internals. A2A can be "call this customer-service agent" without the caller learning how that agent implements the service.

> 原理：A2A 让竞争对手在不暴露内部的情况下协作。A2A 可以是"调用此客服 Agent"，而调用者不需学习该 Agent 如何实现服务。

### Timeline

- **2025-04-09.** Google announces A2A.
  中文翻译：**2025-04-09。** Google 宣布 A2A。
- **2025-06-23.** Donated to Linux Foundation.
  中文翻译：**2025-06-23。** 捐给 Linux 基金会。
- **2025-08.** Absorbs IBM's ACP.
  中文翻译：**2025-08。** 吸收 IBM 的 ACP。
- **2025-09.** AP2 extension (Agent Payments) ships.
  中文翻译：**2025-09。** AP2 扩展（Agent 支付）发布。
- **2026-04.** v1.0 released with 150+ supporting organizations.
  中文翻译：**2026-04。** v1.0 发布，150+ 支持组织。

### Relationship to MCP

| Dimension | MCP | A2A |
|-----------|-----|-----|
| Use case | Agent-to-tool | Agent-to-agent |
| Opacity | Transparent tool calls | Opaque inner reasoning |
| Typical caller | Agent runtime | Another agent |
| State | Tool-call result | Task with lifecycle |
| Authorization | OAuth 2.1 (Phase 13 · 16) | JWT-signed Agent Cards (AP2) |
| Transport | Stdio / Streamable HTTP | JSON-RPC over HTTP / gRPC |

Use MCP when you want to invoke a specific tool. Use A2A when you want to delegate a whole task to another agent. Many production systems use both: an agent uses MCP for its tool layer and A2A for its collaboration layer.

> 想调用特定工具时用 MCP。想将整个任务委托给另一个 Agent 时用 A2A。许多生产系统两者都用：Agent 用 MCP 作工具层、用 A2A 作协作层。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 实现最小 A2A 线束：研究 Agent 发布卡片，写作 Agent 接收 `tasks/send`（含 PDF 和文本指令的 Parts），经历 working -> input_required -> working -> completed 生命周期，返回文本 Artifact。全部标准库，使用内存传输关注消息形状。

`code/main.py` implements a minimal A2A harness: a research agent publishes its card, a writer agent receives a `tasks/send` with parts including a PDF and a text instruction, transitions through working → input_required → working → completed, and returns a text artifact. All stdlib; uses an in-memory transport to focus on message shapes.

> `code/main.py` 实现最小 A2A 线束：研究 Agent 发布卡片、写作 Agent 接收 `tasks/send`（包含 PDF 和文本指令的 parts）、经历 working → input_required → working → completed、返回文本 Artifact。全部标准库；使用内存传输以聚焦消息形态。

What to look at:

- Agent Card JSON shape.
  中文翻译：Agent Card JSON 形态。
- Task id assignment and state transitions.
  中文翻译：Task id 分配和状态转换。
- Messages with mixed-type parts.
  中文翻译：带混合类型 part 的消息。
- Input-required branch mid-task.
  中文翻译：任务中的输入要求分支。
- Artifact return on completion.
  中文翻译：完成时返回 Artifact。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-a2a-agent-spec.md`——给定一个新的可被其他 Agent 调用的 Agent，生成 Agent Card JSON、技能模式和端点蓝图。

This lesson produces `outputs/skill-a2a-agent-spec.md`. Given a new agent that should be callable by other agents, the skill produces the Agent Card JSON, skills schema, and endpoint blueprint.

> 本课产出 `outputs/skill-a2a-agent-spec.md`。给定一个可被其他 Agent 调用的新 Agent，该 skill 生成 Agent Card JSON、技能 schema 和端点蓝图。

## Exercises | 练习题

1. Run `code/main.py`. Trace the full Task lifecycle, including the input-required pause where the called agent asks for a clarification.
   中文翻译：运行 `code/main.py`。追踪完整 Task 生命周期，包括被调用 Agent 请求澄清的 input-required 暂停。

2. Add a signed Agent Card. Sign with HMAC over the card's canonical JSON. Write a verifier and confirm it fails on a mutated card.
   中文翻译：添加签名 Agent Card。用 HMAC 对卡片的规范 JSON 签名。写验证器，确认对变异卡片失败。

3. Implement task streaming: the writer agent emits three incremental artifact chunks over SSE and the caller accumulates them.
   中文翻译：实现任务流式：写作 Agent 通过 SSE 发出三个增量 artifact 块，调用者累积它们。

4. Design an A2A agent that wraps an MCP server. Map each MCP tool to an A2A skill. Note the trade-offs — what opacity is lost?
   中文翻译：设计包装 MCP 服务器的 A2A Agent。将每个 MCP 工具映射到 A2A 技能。注意权衡——丢失了什么不透明性？

5. Read the A2A v1.0 announcement and identify the one feature that is not yet implemented by any framework as of April 2026. (Hint: it relates to multi-hop task delegation.)
   中文翻译：阅读 A2A v1.0 公告，识别截至 2026 年 4 月尚未被任何框架实现的一个功能。（提示：与多跳任务委托有关。）

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| A2A | "Agent-to-Agent protocol" | Open protocol for opaque agent collaboration | Agent 间通信协议 |
| Agent Card | "`.well-known/agent.json`" | Published metadata describing an agent's skills and endpoint | Agent 卡片：发布能力元数据 |
| Skill | "A callable unit" | A named operation the agent supports (analog to MCP tool) | 技能：Agent 支持的可调用操作 |
| Task | "Unit of delegation" | A work item with a lifecycle and final artifact | 任务：带生命周期的委托工作单元 |
| Message | "Task input" | Carries Parts (text, file, data) | 消息：携带 Parts 的任务输入 |
| Part | "Typed chunk" | `text` / `file` / `data` element of a message | 部件：消息的类型化元素 |
| Artifact | "Task output" | Named, typed output returned on completion | 工件：完成时返回的命名类型化输出 |
| AP2 | "Agent Payments Protocol" | Signed Agent Cards extension for trust and payments | Agent 支付协议：签名卡片扩展 |
| Opacity | "Black-box collaboration" | Called agent's internals are hidden from caller | 不透明性：被调用方内部隐藏 |
| Input-required | "Task pause" | Lifecycle state when the agent needs more info | 输入要求：任务暂停等待更多信息 |

## Further Reading | 延伸阅读

- [a2a-protocol.org](https://a2a-protocol.org/latest/) — canonical A2A specification
  中文翻译：权威 A2A 规范
- [a2aproject/A2A — GitHub](https://github.com/a2aproject/A2A) — reference implementations and SDKs
  中文翻译：参考实现和 SDK
- [Linux Foundation — A2A launch press release](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) — June 2025 governance transfer
  中文翻译：2025 年 6 月治理转移
- [Google Cloud — A2A protocol upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade) — roadmap and partner momentum
  中文翻译：路线图和伙伴势头
- [Google Dev — A2A 1.0 milestone](https://discuss.google.dev/t/the-a2a-1-0-milestone-ensuring-and-testing-backward-compatibility/352258) — v1.0 release notes and backward-compat guidance
  中文翻译：v1.0 发行说明和向后兼容指南
