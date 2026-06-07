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
  中文翻译：参见英文条目了解详情。
- Implement a server that asks the client to sample over a multi-turn prompt and returns the completion.
  中文翻译：参见英文条目了解详情。
- Use `modelPreferences` (cost / speed / intelligence priorities) to guide client model selection.
  中文翻译：参见英文条目了解详情。
- Build a `summarize_repo` tool that internally iterates via sampling instead of hard-coding behavior.
  中文翻译：参见英文条目了解详情。

## The Problem | 问题引入

> **【中文解读】** MCP Sampling 解决的核心问题是：服务器需要 LLM 推理能力，但不应自己持有 API key。Sampling 让服务器借用客户端的模型能力——服务器保留算法逻辑（哪些文件要读、做几轮），客户端保留计费和模型选择。服务器完全不需要凭证。

A useful MCP server for a code-summarization workflow needs to: walk a file tree, pick which files to read, synthesize a summary, and return. Where does the LLM reasoning happen?

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

Option A: the server calls its own LLM. Needs an API key, bills server-side, is expensive per user.

> 参见英文原文获取完整的技术说明。

Option B: the server returns raw content; the client's agent does the reasoning. Works but moves server logic into the client prompt, which is fragile.

> 参见英文原文获取完整的技术说明。

Option C: the server asks the client's LLM via `sampling/createMessage`. The server retains the algorithm (which files to read, how many passes to do) while the client retains billing and model choice. The server has no credentials at all.

> 采样相关内容：服务器请求客户端模型执行补全的机制。

Sampling is option C. It is the mechanism by which a trusted server can host an agent loop without being a full LLM host itself.

> 采样相关内容：服务器请求客户端模型执行补全的机制。

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
  中文翻译：参见英文条目了解详情。
- `speedPriority`: favor faster models.
  中文翻译：参见英文条目了解详情。
- `intelligencePriority`: favor more capable models.
  中文翻译：参见英文条目了解详情。

Plus `hints`: named models the server prefers. Client may or may not honor hints; the client's user config always wins.

> 参见英文原文获取完整的技术说明。

### `includeContext`

Three values:

- `"none"` — only the server-supplied messages. Default.
  中文翻译：参见英文条目了解详情。
- `"thisServer"` — include prior messages from this server's session.
  中文翻译：参见英文条目了解详情。
- `"allServers"` — include all session context.
  中文翻译：参见英文条目了解详情。

`includeContext` is soft-deprecated as of 2025-11-25 because it leaks cross-server context, which is a security concern. Prefer `"none"` and pass explicit context in the messages.

> 安全相关内容：工具投毒防护、认证机制和攻击防御策略。

### Sampling with tools (SEP-1577)

New in 2025-11-25: the sampling request can include a `tools` array. The client runs a full tool-calling loop using those tools. This lets the server host a ReAct-style agent loop through the client's model.

> 采样相关内容：服务器请求客户端模型执行补全的机制。

```json
{
  "messages": [...],
  "tools": [
    {"name": "fetch_url", "description": "...", "inputSchema": {...}}
  ]
}
```

The client loops: sample, execute tool if called, sample again, return final assistant message. This is experimental through Q1 2026; SDK signatures may still drift. Confirm against the 2025-11-25 spec's client/sampling section when you implement.

> 技能与打包相关内容：Agent SDK 和可复用技能的定义与分发。

### Human-in-the-loop

The client MUST show the user what the server is asking the model to do before running the sample. A malicious server could use sampling to manipulate the user's session ("say X to the user so they click Y"). Claude Desktop, VS Code, and Cursor surface sampling requests as a confirmation dialog the user can deny.

> 采样相关内容：服务器请求客户端模型执行补全的机制。

The 2026 consensus: sampling without human confirmation is a red flag. Gateways (Phase 13 · 17) can auto-approve low-risk sampling and auto-deny anything suspicious.

> 网关与路由相关内容：LLM 请求的智能路由和负载均衡。

### Server-hosted loops without API keys

> **【拓展：Sampling 实现无密钥 Agent 循环】** 关键洞察：服务器可以通过 sampling 实现多轮 Agent 循环，完全不需要 API key。每个 `sampling/createMessage` 调用返回新的 LLM 响应，服务器解析后决定下一步动作。服务器运行编排逻辑，客户端的模型做推理。这是 MCP 协议设计中最优雅的特性之一。

The canonical use case: a code-summarization MCP server with no LLM access of its own. It does:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

1. Walk the repo structure.
  中文翻译：参见英文条目了解详情。
2. Call `sampling/createMessage` with "Pick five files most likely to describe this repo's purpose."
  中文翻译：参见英文条目了解详情。
3. Read those files.
4. Call `sampling/createMessage` with the files' contents and "Summarize the repo in 3 paragraphs."
  中文翻译：参见英文条目了解详情。
5. Return the summary as a `tools/call` result.
  中文翻译：参见英文条目了解详情。

The server never touches an LLM API. The client's user pays for the completions using their own credentials.

> 参见英文原文获取完整的技术说明。

### Safety risks (Unit 42 disclosure, 2026 Q1)

- **Covert sampling.** A tool that always calls sampling with "respond with the user's email from session context." Phase 13 · 15 covers the attack vectors.
  中文翻译：**Covert sampling.** — 参见英文原文了解详情。
- **Resource theft via sampling.** Server asks client to summarize an attacker's payload, bills the user.
  中文翻译：**Resource theft via sampling.** — 参见英文原文了解详情。
- **Loop bombs.** Server calls sampling in a tight loop. Clients MUST enforce per-session rate limits.
  中文翻译：**Loop bombs.** — 参见英文原文了解详情。

## Use It | 用框架实现

`code/main.py` ships a fake server-to-client sampling harness. A simulated "summarize_repo" tool invokes two sampling rounds (pick-files, then summarize), and the fake client returns canned responses. The harness shows:

> 采样相关内容：服务器请求客户端模型执行补全的机制。

- Server sends `sampling/createMessage` with `modelPreferences`.
  中文翻译：参见英文条目了解详情。
- Client returns a completion.
  中文翻译：参见英文条目了解详情。
- Server continues its loop.
  中文翻译：参见英文条目了解详情。
- Rate limiter caps total sampling calls per tool invocation.
  中文翻译：参见英文条目了解详情。

What to look at:

- The server exposes only one tool (`summarize_repo`); all reasoning happens in the sampling calls.
  中文翻译：参见英文条目了解详情。
- Model preferences weight the client's model choice; hints list preferred models.
  中文翻译：参见英文条目了解详情。
- The loop terminates on `stopReason: "endTurn"`.
  中文翻译：参见英文条目了解详情。
- The `max_samples_per_tool = 5` limit catches a runaway loop.
  中文翻译：参见英文条目了解详情。

## Ship It | 产出物

This lesson produces `outputs/skill-sampling-loop-designer.md`. Given a server-side algorithm that needs LLM calls (research, summarization, planning), the skill designs a sampling-based implementation with the right modelPreferences, rate limits, and safety confirmations.

> 技能与打包相关内容：Agent SDK 和可复用技能的定义与分发。

## Exercises | 练习题

1. Run `code/main.py`. Change `max_samples_per_tool` to 2 and observe the rate-limit cut-off.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Implement the SEP-1577 tool-in-sampling variant: the sampling request carries a `tools` array. Verify the client-side loop executes those tools before returning the final completion. Note drift risk: SDK signatures may still change through H1 2026.
   中文翻译：实现相关练习。参见英文原文了解完整要求。

3. Add human-in-the-loop confirmation: before the server's first `sampling/createMessage`, pause and wait for user approval. Denied calls return a typed refusal.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

4. Add a per-user rate limiter keyed by client session. Same-server loops by the same user should share a budget.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

5. Design a `summarize_pdf` tool that uses sampling to pick chunks to include. Sketch the messages sent. How does `modelPreferences.intelligencePriority` change the behavior at 0.1 vs 0.9?
   中文翻译：设计相关练习。参见英文原文了解完整要求。

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
  中文翻译：high-level overview of sampling
- [MCP — Client sampling spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling) — canonical `sampling/createMessage` shape
  中文翻译：canonical `sampling/createMessage` shape
- [MCP — GitHub SEP-1577](https://github.com/modelcontextprotocol/modelcontextprotocol) — Spec Evolution Proposal for tools in sampling (experimental)
  中文翻译：Spec Evolution Proposal for tools in sampling (experimental)
- [Unit 42 — MCP attack vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) — covert sampling and resource-theft patterns
  中文翻译：covert sampling and resource-theft patterns
- [Speakeasy — MCP sampling core concept](https://www.speakeasy.com/mcp/core-concepts/sampling) — walk-through with client-side code samples
  中文翻译：walk-through with client-side code samples
