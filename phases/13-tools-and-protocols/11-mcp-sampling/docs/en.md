# MCP Sampling — Server-Requested LLM Completions and Agent Loops | MCP 采样：服务器请求 LLM 补全与 Agent 循环

> Most MCP servers are dumb executors: take arguments, run code, return content. Sampling lets a server flip direction: it asks the client's LLM to make a decision. This enables server-hosted agent loops without the server owning any model credentials. SEP-1577, merged in 2025-11-25, added tools inside sampling requests so the loop can include deeper reasoning. Drift-risk note: the SEP-1577 tool-in-sampling shape was experimental through Q1 2026 and is still settling in SDK APIs.

> **【中文解读】** 大多数 MCP 服务器是简单的执行器：接收参数、运行代码、返回内容。Sampling 让服务器反转方向：它请求客户端的 LLM 做出决策。这使服务器可以承载 Agent 循环，而无需拥有任何模型凭证。SEP-1577 在 sampling 请求中添加了 tools，使循环可以包含更深的推理。

> **【拓展：Sampling→MCP Agent 循环】** Sampling 是 MCP 实现 Agent 循环的关键原语。传统模式下，MCP 服务器只是被动执行工具。通过 Sampling，服务器可以主动请求客户端的 LLM 进行推理，从而在不持有 API 密钥的情况下实现多步 Agent 工作流。这是 MCP 与 Function Calling 的重要区别之一。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, sampling harness) | **语言:** Python (stdlib, sampling harness)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources and prompts) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources and prompts)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain what `sampling/createMessage` solves (server-hosted loops without server-side API keys).
  中文翻译：解释 `sampling/createMessage` 解决的问题（服务器托管循环无需服务器端 API 密钥）。
- Implement a server that asks the client to sample over a multi-turn prompt and returns the completion.
  中文翻译：实现一个服务器，请求客户端对多轮 prompt 进行采样并返回补全。
- Use `modelPreferences` (cost / speed / intelligence priorities) to guide client model selection.
  中文翻译：使用 `modelPreferences`（成本/速度/智能优先级）引导客户端模型选择。
- Build a `summarize_repo` tool that internally iterates via sampling instead of hard-coding behavior.
  中文翻译：构建一个 `summarize_repo` 工具，通过 sampling 内部迭代而非硬编码行为。

## The Problem | 问题引入

> **【中文解读】** MCP Sampling 解决的核心问题是：服务器需要 LLM 推理能力，但不应自己持有 API key。Sampling 让服务器借用客户端的模型能力——服务器保留算法逻辑（哪些文件要读、做几轮），客户端保留计费和模型选择。服务器完全不需要凭证。

A useful MCP server for a code-summarization workflow needs to: walk a file tree, pick which files to read, synthesize a summary, and return. Where does the LLM reasoning happen?

> 一个有用的代码摘要 MCP 服务器需要：遍历文件树、选择读哪些文件、综合摘要、返回。LLM 推理在哪里发生？

Option A: the server calls its own LLM. Needs an API key, bills server-side, is expensive per user.

> 选项 A：服务器调用自己的 LLM。需要 API 密钥，服务器端计费，每用户成本高。

Option B: the server returns raw content; the client's agent does the reasoning. Works but moves server logic into the client prompt, which is fragile.

> 选项 B：服务器返回原始内容；客户端的 Agent 做推理。可行但把服务器逻辑移到客户端 prompt 中，脆弱。

Option C: the server asks the client's LLM via `sampling/createMessage`. The server retains the algorithm (which files to read, how many passes to do) while the client retains billing and model choice. The server has no credentials at all.

> 选项 C：服务器通过 `sampling/createMessage` 请求客户端的 LLM。服务器保留算法（读哪些文件、做几轮），客户端保留计费和模型选择。服务器完全不需要凭证。

Sampling is option C. It is the mechanism by which a trusted server can host an agent loop without being a full LLM host itself.

> Sampling 是选项 C。它是受信任服务器托管 Agent 循环而自身不必是完整 LLM 宿主的机制。

## The Concept | 核心概念

### `sampling/createMessage` request

Server sends:

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

Client runs its LLM, returns:

```json
{"jsonrpc": "2.0", "id": 42, "result": {
  "role": "assistant",
  "content": {"type": "text", "text": "..."},
  "model": "claude-3-5-sonnet-20251022",
  "stopReason": "endTurn"
}}
```

### `modelPreferences`

Three floats summing to 1.0:

- `costPriority`: favor cheaper models.
  中文翻译：`costPriority`：偏好更便宜的模型。
- `speedPriority`: favor faster models.
  中文翻译：`speedPriority`：偏好更快的模型。
- `intelligencePriority`: favor more capable models.
  中文翻译：`intelligencePriority`：偏好更强大的模型。

Plus `hints`: named models the server prefers. Client may or may not honor hints; the client's user config always wins.

> 加上 `hints`：服务器偏好的命名模型。客户端可能或可能不遵从提示；客户端的用户配置始终优先。

### `includeContext`

Three values:

- `"none"` — only the server-supplied messages. Default.
  中文翻译：`"none"`——仅服务器提供的消息。默认值。
- `"thisServer"` — include prior messages from this server's session.
  中文翻译：`"thisServer"`——包含此服务器会话中的先前消息。
- `"allServers"` — include all session context.
  中文翻译：`"allServers"`——包含所有会话上下文。

`includeContext` is soft-deprecated as of 2025-11-25 because it leaks cross-server context, which is a security concern. Prefer `"none"` and pass explicit context in the messages.

> `includeContext` 在 2025-11-25 起软弃用，因为它泄露跨服务器上下文，存在安全风险。偏好 `"none"` 并在消息中显式传递上下文。

### Sampling with tools (SEP-1577)

New in 2025-11-25: the sampling request can include a `tools` array. The client runs a full tool-calling loop using those tools. This lets the server host a ReAct-style agent loop through the client's model.

> 2025-11-25 新增：sampling 请求可包含 `tools` 数组。客户端使用这些工具运行完整的工具调用循环。这让服务器可以通过客户端的模型托管 ReAct 风格的 Agent 循环。

```json
{
  "messages": [...],
  "tools": [
    {"name": "fetch_url", "description": "...", "inputSchema": {...}}
  ]
}
```

The client loops: sample, execute tool if called, sample again, return final assistant message. This is experimental through Q1 2026; SDK signatures may still drift. Confirm against the 2025-11-25 spec's client/sampling section when you implement.

> 客户端循环：采样、如被调用则执行工具、再采样、返回最终助手消息。这在 2026 Q1 前是实验性的；SDK 签名可能仍会漂移。实现时对照 2025-11-25 规范的 client/sampling 章节。

### Human-in-the-loop

The client MUST show the user what the server is asking the model to do before running the sample. A malicious server could use sampling to manipulate the user's session ("say X to the user so they click Y"). Claude Desktop, VS Code, and Cursor surface sampling requests as a confirmation dialog the user can deny.

> 客户端必须在运行 sample 前向用户展示服务器要求模型做什么。恶意服务器可能利用 sampling 操纵用户会话（"对用户说 X 让他们点击 Y"）。Claude Desktop、VS Code 和 Cursor 将 sampling 请求显示为用户可拒绝的确认对话框。

The 2026 consensus: sampling without human confirmation is a red flag. Gateways (Phase 13 · 17) can auto-approve low-risk sampling and auto-deny anything suspicious.

> 2026 年共识：无人类确认的 sampling 是危险信号。网关（Phase 13 · 17）可自动批准低风险 sampling 并自动拒绝可疑请求。

### Server-hosted loops without API keys

> **【拓展：Sampling 实现无密钥 Agent 循环】** 关键洞察：服务器可以通过 sampling 实现多轮 Agent 循环，完全不需要 API key。每个 `sampling/createMessage` 调用返回新的 LLM 响应，服务器解析后决定下一步动作。服务器运行编排逻辑，客户端的模型做推理。这是 MCP 协议设计中最优雅的特性之一。

The canonical use case: a code-summarization MCP server with no LLM access of its own. It does:

> 典型用例：一个代码摘要 MCP 服务器自身无 LLM 访问。它执行：

1. Walk the repo structure.
  中文翻译：遍历仓库结构。
2. Call `sampling/createMessage` with "Pick five files most likely to describe this repo's purpose."
  中文翻译：调用 `sampling/createMessage`，提示"选 5 个最可能描述此仓库目的的文件。"
3. Read those files.
  中文翻译：读取这些文件。
4. Call `sampling/createMessage` with the files' contents and "Summarize the repo in 3 paragraphs."
  中文翻译：调用 `sampling/createMessage`，带文件内容，提示"用 3 段总结仓库。"
5. Return the summary as a `tools/call` result.
  中文翻译：将摘要作为 `tools/call` 结果返回。

The server never touches an LLM API. The client's user pays for the completions using their own credentials.

> 服务器从不触碰 LLM API。客户端用户用自己的凭证支付补全费用。

### Safety risks (Unit 42 disclosure, 2026 Q1)

- **Covert sampling.** A tool that always calls sampling with "respond with the user's email from session context." Phase 13 · 15 covers the attack vectors.
  中文翻译：**隐蔽采样。** 一个工具总是调用 sampling 提示"用会话上下文中用户的邮箱回复。"Phase 13 · 15 涵盖攻击向量。
- **Resource theft via sampling.** Server asks client to summarize an attacker's payload, bills the user.
  中文翻译：**通过采样窃取资源。** 服务器请求客户端摘要攻击者的载荷，向用户计费。
- **Loop bombs.** Server calls sampling in a tight loop. Clients MUST enforce per-session rate limits.
  中文翻译：**循环炸弹。** 服务器在紧凑循环中调用 sampling。客户端必须强制执行每会话速率限制。

## Use It | 用框架实现

`code/main.py` ships a fake server-to-client sampling harness. A simulated "summarize_repo" tool invokes two sampling rounds (pick-files, then summarize), and the fake client returns canned responses. The harness shows:

> `code/main.py` 提供一个假的服务器到客户端 sampling 线束。模拟的"summarize_repo"工具调用两轮 sampling（选文件，然后摘要），假客户端返回预设响应。线束展示：

- Server sends `sampling/createMessage` with `modelPreferences`.
  中文翻译：服务器发送带 `modelPreferences` 的 `sampling/createMessage`。
- Client returns a completion.
  中文翻译：客户端返回补全。
- Server continues its loop.
  中文翻译：服务器继续循环。
- Rate limiter caps total sampling calls per tool invocation.
  中文翻译：速率限制器对每次工具调用的总 sampling 数设上限。

What to look at:

- The server exposes only one tool (`summarize_repo`); all reasoning happens in the sampling calls.
  中文翻译：服务器只暴露一个工具（`summarize_repo`）；所有推理发生在 sampling 调用中。
- Model preferences weight the client's model choice; hints list preferred models.
  中文翻译：模型偏好加权客户端的模型选择；提示列出偏好模型。
- The loop terminates on `stopReason: "endTurn"`.
  中文翻译：循环在 `stopReason: "endTurn"` 时终止。
- The `max_samples_per_tool = 5` limit catches a runaway loop.
  中文翻译：`max_samples_per_tool = 5` 限制捕获失控循环。

## Ship It | 产出物

This lesson produces `outputs/skill-sampling-loop-designer.md`. Given a server-side algorithm that needs LLM calls (research, summarization, planning), the skill designs a sampling-based implementation with the right modelPreferences, rate limits, and safety confirmations.

> 本课产出 `outputs/skill-sampling-loop-designer.md`。给定一个需要 LLM 调用的服务器端算法（研究、摘要、规划），该 skill 设计基于 sampling 的实现，包含正确的 modelPreferences、速率限制和安全确认。

## Exercises | 练习题

1. Run `code/main.py`. Change `max_samples_per_tool` to 2 and observe the rate-limit cut-off.
   中文翻译：运行 `code/main.py`。将 `max_samples_per_tool` 改为 2，观察速率限制切断。

2. Implement the SEP-1577 tool-in-sampling variant: the sampling request carries a `tools` array. Verify the client-side loop executes those tools before returning the final completion. Note drift risk: SDK signatures may still change through H1 2026.
   中文翻译：实现 SEP-1577 的 tool-in-sampling 变体：sampling 请求携带 `tools` 数组。验证客户端循环在返回最终补全前执行这些工具。注意漂移风险：SDK 签名在 2026 H1 前可能仍变化。

3. Add human-in-the-loop confirmation: before the server's first `sampling/createMessage`, pause and wait for user approval. Denied calls return a typed refusal.
   中文翻译：添加人在回路确认：在服务器首次 `sampling/createMessage` 前暂停等待用户批准。被拒绝的调用返回类型化拒绝。

4. Add a per-user rate limiter keyed by client session. Same-server loops by the same user should share a budget.
   中文翻译：添加按客户端 session 索引的每用户速率限制器。同用户的同服务器循环应共享预算。

5. Design a `summarize_pdf` tool that uses sampling to pick chunks to include. Sketch the messages sent. How does `modelPreferences.intelligencePriority` change the behavior at 0.1 vs 0.9?
   中文翻译：设计 `summarize_pdf` 工具，使用 sampling 选择要包含的块。勾勒发送的消息。`modelPreferences.intelligencePriority` 在 0.1 vs 0.9 时如何改变行为？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Sampling | "Server-to-client LLM call" | Server asks client's model for a completion | 采样 |
| `sampling/createMessage` | "The method" | JSON-RPC method for sampling requests | 采样请求方法 |
| `modelPreferences` | "Model priorities" | Cost / speed / intelligence weights plus name hints | 模型偏好 |
| `includeContext` | "Cross-session leakage" | Soft-deprecated context inclusion mode | 上下文包含（已弃用） |
| SEP-1577 | "Tools in sampling" | Allow tools inside sampling for server-hosted ReAct | 采样中的工具支持 |
| Human-in-the-loop | "User confirms" | Client surfaces sampling request to user before running | 人在回路 |
| Loop bomb | "Runaway sampling" | Server-side infinite sampling loop; client must rate-limit | 循环炸弹 |
| Covert sampling | "Hidden reasoning" | Malicious server hides intent in sampling prompts | 隐蔽采样 |
| Resource theft | "Using user's LLM budget" | Server forces client to spend on sampling it does not want | 资源盗用 |
| `stopReason` | "Why generation halted" | `endTurn`, `stopSequence`, or `maxTokens` | 停止原因 |

## Further Reading | 延伸阅读

- [MCP — Concepts: Sampling](https://modelcontextprotocol.io/docs/concepts/sampling) — high-level overview of sampling
  中文翻译：sampling 的高层概览
- [MCP — Client sampling spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling) — canonical `sampling/createMessage` shape
  中文翻译：权威 `sampling/createMessage` 形态
- [MCP — GitHub SEP-1577](https://github.com/modelcontextprotocol/modelcontextprotocol) — Spec Evolution Proposal for tools in sampling (experimental)
  中文翻译：sampling 中工具的规范演进提案（实验性）
- [Unit 42 — MCP attack vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) — covert sampling and resource-theft patterns
  中文翻译：隐蔽 sampling 和资源盗窃模式
- [Speakeasy — MCP sampling core concept](https://www.speakeasy.com/mcp/core-concepts/sampling) — walk-through with client-side code samples
  中文翻译：带客户端代码示例的演练
