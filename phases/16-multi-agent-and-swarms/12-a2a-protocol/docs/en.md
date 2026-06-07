# A2A — The Agent-to-Agent Protocol | A2A：Agent 间通信协议

> Google announced A2A in April 2025; by April 2026 the spec is at https://a2a-protocol.org/latest/specification/ and 150+ organizations back it. A2A is the horizontal complement to MCP (Lesson 13): where MCP is vertical (agent ↔ tools), A2A is peer-to-peer (agent ↔ agent). It defines Agent Cards (discovery), tasks with artifacts (text, structured data, video), opaque task lifecycles, and auth. Production systems increasingly pair MCP with A2A. Google Cloud rolled A2A support into Vertex AI Agent Builder during 2025-2026.

> **【中文解读】** Google 在 2025 年 4 月发布 A2A 协议；到 2026 年 4 月，规范已有 150+ 组织支持。A2A 是 MCP 的水平补充：MCP 是垂直的（Agent 与工具），A2A 是点对点的（Agent 与 Agent）。定义了 Agent Card（发现）、带产物的任务、不透明任务生命周期和认证。生产系统越来越多地将 MCP 与 A2A 配对使用。

> **【拓展：A2A → Google 的 Agent 协议】** A2A 是 Google 主导的 Agent 间通信标准协议，与 Anthropic 的 MCP（Model Context Protocol）互补。MCP 解决 Agent 与工具的连接，A2A 解决 Agent 与 Agent 的协作。两者结合构成了 2026 年 Agent 生态的通信基础设施。

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Your agent needs to call another agent on another system. How? You can expose an HTTP endpoint, define a bespoke JSON schema, and hope the other side speaks it. Every pair of agents becomes a custom integration.

> 你的 Agent 需要调用另一个系统上的 Agent。怎么做？你可以暴露一个 HTTP 端点，定义一个定制 JSON 模式，并希望另一端能理解它。每对 Agent 都变成了一个定制集成。

A2A is the universal wire protocol for that call. Standard discovery, standard task model, standard transport, standard artifacts. Like HTTP+REST but for agents as first-class citizens.

> A2A 是该调用的通用线协议。标准发现、标准任务模型、标准传输、标准工件。就像 HTTP+REST，但以 Agent 为一等公民。

## Concept | 核心概念

### The four elements

**Agent Card.** A JSON document at `/.well-known/agent.json` describing the agent: name, skills, endpoints, supported modalities, auth requirements. Discovery happens by reading the card.

> **Agent 卡片。** 位于 `/.well-known/agent.json` 的 JSON 文档，描述 Agent：名称、技能、端点、支持的模态、认证要求。通过读取卡片进行发现。

**Task.** The unit of work. An async, stateful object with a lifecycle: `submitted -> working -> completed / failed / canceled`. A client sends a task, polls or subscribes for updates.

> **任务。** 工作单元。具有生命周期的异步有状态对象：`submitted -> working -> completed / failed / canceled`。客户端发送任务，轮询或订阅更新。

**Artifact.** The result type produced by a task. Text, structured JSON, image, video, audio. Artifacts are typed so different modalities are first-class.

> **工件。** 任务产生的结果类型。文本、结构化 JSON、图像、视频、音频。工件是有类型的，因此不同模态是一等公民。

**Opaque lifecycle.** A2A does not prescribe *how* the remote agent solves the task. The client sees state transitions and artifacts; the implementation is free to use any framework.

> **不透明生命周期。** A2A 不规定远程 Agent *如何* 解决任务。客户端看到状态转换和工件；实现可以自由使用任何框架。

### The MCP/A2A split

- **MCP** (Lesson 13): agent <-> tool. The agent reads/writes via JSON-RPC to a tool server. Stateless by default.
  中文翻译：**MCP**（Lesson 13）：Agent <-> 工具。Agent 通过 JSON-RPC 读写工具服务器。默认无状态。
- **A2A**: agent <-> agent. Peer protocol; both sides are agents with their own reasoning.
  中文翻译：**A2A**：Agent <-> Agent。对等协议；双方都是有自己推理的 Agent。

Production multi-agent systems use both. An A2A peer calls MCP tools on its side. The split keeps the two concerns clean.

> 生产多 Agent 系统两者都用。A2A 对等端在其端调用 MCP 工具。这种分离保持了两个关注点的清晰。

Or with streaming: SSE subscription to `/tasks/{id}/events` for push updates.

> 或者使用流式：SSE 订阅 `/tasks/{id}/events` 获取推送更新。

### Auth

A2A supports three common patterns:

> A2A 支持三种常见模式：

- **Bearer token** — OAuth2 or opaque.
  中文翻译：**Bearer token** — OAuth2 或不透明令牌。
- **mTLS** — mutual TLS; organizations prove identity to each other.
  中文翻译：**mTLS** — 双向 TLS；组织互相证明身份。
- **Signed requests** — HMAC over the payload.
  中文翻译：**签名请求** — 对有效载荷的 HMAC。

Auth is declared in the Agent Card; clients discover and comply.

> 认证在 Agent 卡片中声明；客户端发现并遵守。

### 150+ organizations by April 2026

Enterprise adoption drove A2A scale. The headline: A2A became the way enterprise agent systems cross trust boundaries. Google Cloud shipped Vertex AI Agent Builder A2A support; Microsoft Agent Framework supports it; most major frameworks (LangGraph, CrewAI, AutoGen) ship A2A adapters.

> 企业采用推动了 A2A 的规模化。标题：A2A 成为企业 Agent 系统跨越信任边界的方式。Google Cloud 提供了 Vertex AI Agent Builder A2A 支持；Microsoft Agent Framework 支持它；大多数主要框架（LangGraph、CrewAI、AutoGen）提供 A2A 适配器。

### Where A2A wins

- **Cross-organization calls.** Agent at company A calls agent at company B. Without A2A, every pair is a bespoke contract.
  中文翻译：**跨组织调用。** 公司 A 的 Agent 调用公司 B 的 Agent。没有 A2A，每对都是定制契约。
- **Heterogeneous frameworks.** LangGraph agent calls CrewAI agent calls custom Python agent. A2A normalizes.
  中文翻译：**异构框架。** LangGraph Agent 调用 CrewAI Agent 调用自定义 Python Agent。A2A 标准化。
- **Typed artifacts.** Video result, structured JSON, audio — all first-class.
  中文翻译：**类型化工件。** 视频结果、结构化 JSON、音频——都是一等公民。
- **Long-running tasks.** Opaque lifecycle + polling makes hours-long tasks straightforward.
  中文翻译：**长时间运行的任务。** 不透明生命周期 + 轮询使小时级任务变得简单。

### Where A2A struggles

- **Latency-sensitive micro-calls.** A2A's lifecycle is async. Sub-millisecond agent-to-agent does not fit; use direct RPC.
  中文翻译：**延迟敏感的微调用。** A2A 的生命周期是异步的。亚毫秒级 Agent 对 Agent 不适合；使用直接 RPC。
- **Tight-coupled in-process agents.** If both agents run in the same Python process, A2A's HTTP round-trip is overkill.
  中文翻译：**紧耦合的进程内 Agent。** 如果两个 Agent 运行在同一个 Python 进程中，A2A 的 HTTP 往返是过度设计。
- **Small teams.** Spec overhead is real; internal-only agents may not need the formality.
  中文翻译：**小团队。** 规范开销是真实的；仅内部的 Agent 可能不需要这种正式性。

### A2A vs ACP, ANP, NLIP

Several related specs emerged in 2024-2026:

> 2024-2026 年间出现了几个相关规范：

- **ACP** (IBM/Linux Foundation) — predecessor to A2A, narrower scope.
  中文翻译：**ACP**（IBM/Linux Foundation）— A2A 的前身，范围更窄。
- **ANP** (Agent Network Protocol) — peer-discovery-heavy, decentralized-first.
  中文翻译：**ANP**（Agent Network Protocol）— 重对等发现，去中心化优先。
- **NLIP** (Ecma Natural Language Interaction Protocol, standardized December 2025) — natural-language content type.
  中文翻译：**NLIP**（Ecma 自然语言交互协议，2025 年 12 月标准化）— 自然语言内容类型。

A2A is the most-adopted peer protocol as of April 2026. See arXiv:2505.02279 (Liu et al., "A Survey of Agent Interoperability Protocols") for the comparison.

> 截至 2026 年 4 月，A2A 是采用最广泛的对等协议。参见 arXiv:2505.02279（Liu 等人，"Agent 互操作性协议综述"）进行比较。

## Build It | 动手实现

`code/main.py` implements an A2A-minimal server and client using `http.server` and JSON. The server:

> `code/main.py` 使用 `http.server` 和 JSON 实现 A2A 最小服务器和客户端。服务器：

- exposes `/.well-known/agent.json`,
  中文翻译：暴露 `/.well-known/agent.json`，
- accepts `POST /tasks`,
  中文翻译：接受 `POST /tasks`，
- manages task state,
  中文翻译：管理任务状态，
- returns artifacts on `GET /tasks/{id}`.
  中文翻译：在 `GET /tasks/{id}` 上返回工件。

The client:

> 客户端：

- fetches the Agent Card,
  中文翻译：获取 Agent 卡片，
- submits a task,
  中文翻译：提交任务，
- polls until completion,
  中文翻译：轮询直到完成，
- reads the artifact.
  中文翻译：读取工件。

The script starts the server in a background thread, then runs the client against it. You see the complete flow: discovery, submit, poll, artifact.

> 脚本在后台线程中启动服务器，然后运行客户端。你看到完整流程：发现、提交、轮询、工件。

## Use It | 用框架实现

`outputs/skill-a2a-integrator.md` designs an A2A integration: Agent Card contents, task schemas, auth choice, streaming vs polling.

> `outputs/skill-a2a-integrator.md` 设计 A2A 集成：Agent 卡片内容、任务模式、认证选择、流式 vs 轮询。

## Ship It | 产出物

Checklist:

> 检查清单：

- **Pin the spec version.** A2A is still evolving; the Agent Card should declare the protocol version.
  中文翻译：**固定规范版本。** A2A 仍在演进；Agent 卡片应声明协议版本。
- **Idempotent task creation.** Duplicate submissions (network retries) should produce one task.
  中文翻译：**幂等任务创建。** 重复提交（网络重试）应产生一个任务。
- **Artifact schemas.** Declare what shapes the agent returns; consumers should validate.
  中文翻译：**工件模式。** 声明 Agent 返回什么形状；消费者应验证。
- **Rate limits + auth.** A2A is public-facing; apply standard web security.
  中文翻译：**速率限制 + 认证。** A2A 面向公众；应用标准 Web 安全。
- **Dead-letter for failed tasks.** Inspect patterns over time for recurring failure types.
  中文翻译：**失败任务死信。** 随时间检查模式以发现反复出现的失败类型。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the client discovers the server and receives the correct artifact.
   中文翻译：运行 `code/main.py`。确认客户端发现服务器并接收正确的工件。
2. Add a second skill to the server (e.g., "summarize"). Update the Agent Card. Write a client that picks the skill based on task type.
   中文翻译：向服务器添加第二个技能（如"summarize"）。更新 Agent 卡片。编写根据任务类型选择技能的客户端。
3. Implement an SSE streaming endpoint: `/tasks/{id}/events` that emits state changes. What does the client need to do differently?
   中文翻译：实现 SSE 流式端点：`/tasks/{id}/events`，发射状态变化。客户端需要做什么不同的事？
4. Read the A2A spec. Identify three things the spec mandates that this demo does not implement.
   中文翻译：阅读 A2A 规范。识别规范要求的三个此演示未实现的东西。
5. Compare A2A (Agent Card discovery) to MCP (server-side capability listing via `listTools`). What is the tradeoff between self-describing agents and capability-probing?
   中文翻译：比较 A2A（Agent 卡片发现）与 MCP（通过 `listTools` 的服务器端能力列表）。自描述 Agent 和能力探测之间的权衡是什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Further Reading | 延伸阅读

- [A2A specification](https://a2a-protocol.org/latest/specification/) — the canonical spec
  中文翻译：A2A 规范 — 权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — April 2025 launch post
  中文翻译：Google 开发者博客 — A2A 公告 — 2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) — reference implementations and SDKs
  中文翻译：A2A GitHub 仓库 — 参考实现和 SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) — MCP, ACP, A2A, ANP comparison
  中文翻译：Liu 等人 — Agent 互操作性协议综述 — MCP、ACP、A2A、ANP 比较
