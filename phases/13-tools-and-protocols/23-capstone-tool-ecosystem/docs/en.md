# Capstone — Build a Complete Tool Ecosystem | 毕业项目：构建完整的工具生态系统

> Phase 13 taught every piece. This capstone wires them into one production-shaped system: an MCP server with tools + resources + prompts + tasks + UI, OAuth 2.1 at the edge, an RBAC gateway, a multi-server client, an A2A sub-agent call, OTel tracing into a collector, tool-poisoning detection in CI, and an AGENTS.md + SKILL.md bundle. By the end you can defend every architectural choice.

> **【中文解读】** Phase 13 教了每个组件。本毕业项目将它们连线为一个生产级系统：MCP 服务器（tools+resources+prompts+tasks+UI）、边缘 OAuth 2.1、RBAC 网关、多服务器客户端、A2A 子 Agent 调用、OTel 全链路追踪、CI 中的工具投毒检测、AGENTS.md + SKILL.md 打包。完成后你能为每个架构选择辩护。

> **【拓展】** 这是 Phase 13 的集大成课程，整合了全部23课内容为一个可运行的端到端系统。架构模式：用户 -> 客户端 -> OAuth 2.1 + RBAC 网关 -> 研究 MCP 服务器（工具/资源/提示词/任务/UI/A2A 调用/OTel span）。这是 Anthropic（Claude Research）和 OpenAI（GPTs with Apps SDK）2026年发布的生产研究助手系统的精确形状。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, end-to-end ecosystem harness) | **语言:** Python (stdlib, end-to-end ecosystem harness)
**Prerequisites:** Phase 13 · 01 through 21 | **前置知识:** Phase 13 · 01 through 21
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Compose an MCP server exposing tools, resources, prompts, and a task with a `ui://` app.
  中文翻译：组合暴露工具、资源、提示和带 `ui://` 应用的任务的 MCP 服务器。
- Front the server with an OAuth 2.1 gateway that enforces RBAC and pinned hashes.
  中文翻译：用强制 RBAC 和锁定哈希的 OAuth 2.1 网关前置服务器。
- Write a multi-server client that traces with OTel GenAI attributes end-to-end.
  中文翻译：编写带 OTel GenAI 属性端到端追踪的多服务器客户端。
- Delegate part of a workload to an A2A sub-agent; verify opacity is preserved.
  中文翻译：将部分工作负载委托给 A2A 子 Agent；验证不透明性保留。
- Package the whole stack with AGENTS.md + SKILL.md so other agents can drive it.
  中文翻译：用 AGENTS.md + SKILL.md 打包整个技术栈，使其他 Agent 可以驱动它。

## The Problem | 问题引入

> **【中文解读】** 构建"研究和报告"系统：用户请求"总结2026年关于 agent 协议的被引用最多的三篇 arXiv 论文"。系统通过 MCP 搜索 arXiv，通过 A2A 将论文摘要委托给专门的写作 Agent，聚合结果，渲染交互式报告作为 MCP Apps `ui://` 资源，每步记录到 OTel。

Ship the "research and report" system:

> 发布"研究和报告"系统：

- User asks: "summarize the three most-cited 2026 arXiv papers on agent protocols."
  中文翻译：用户问："总结 2026 年 agent 协议引用最多的三篇 arXiv 论文。"
- System: search arXiv via MCP; delegate paper summarization to a specialized writer agent via A2A; aggregate results; render an interactive report as an MCP Apps `ui://` resource; log every step to OTel.
  中文翻译：系统：通过 MCP 搜索 arXiv；通过 A2A 将论文摘要委托给专门的写作 Agent；聚合结果；将交互式报告渲染为 MCP Apps `ui://` 资源；每步记录到 OTel。

All the primitives from Phase 13 show up. This is not a toy — production research-assistant systems shipped in 2026 by Anthropic (the Claude Research product), OpenAI (GPTs with Apps SDK), and third parties have this exact shape.

> Phase 13 所有原语都出现。这不是玩具——2026 年 Anthropic（Claude Research 产品）、OpenAI（带 Apps SDK 的 GPTs）和第三方发布的生产研究助手系统有此精确形态。

## The Concept | 核心概念

### Architecture

```
[user] -> [client] -> [gateway (OAuth 2.1 + RBAC)] -> [research MCP server]
                                                      |
                                                      +- MCP tool: arxiv_search (pure)
                                                      +- MCP resource: notes://recent
                                                      +- MCP prompt: /research_topic
                                                      +- MCP task: generate_report (long)
                                                      +- MCP Apps UI: ui://report/current
                                                      +- A2A call: writer-agent (tasks/send)
                                                      |
                                                      +- OTel GenAI spans
```

### Trace hierarchy

```
agent.invoke_agent
 ├── llm.chat (kick off)
 ├── mcp.call -> tools/call arxiv_search
 ├── mcp.call -> resources/read notes://recent
 ├── mcp.call -> prompts/get research_topic
 ├── a2a.tasks/send -> writer-agent
 │    └── task transitions (opaque internals)
 ├── mcp.call -> tools/call generate_report (task-augmented)
 │    └── tasks/status polling
 │    └── tasks/result (completed, returns ui:// resource)
 └── llm.chat (final synthesis)
```

One trace id. Every span has the right `gen_ai.*` attributes.

> 一个 trace id。每个 span 有正确的 `gen_ai.*` 属性。

### Security posture

- OAuth 2.1 + PKCE with resource indicator pinning audience to gateway.
  中文翻译：OAuth 2.1 + PKCE 带资源指示器将受众固定到网关。
- Gateway holds upstream credentials; user never sees them.
  中文翻译：网关持有上游凭证；用户永不见它们。
- RBAC: `alice` has `research:read`, `research:write`, can call all tools. `bob` has `research:read`, cannot call `generate_report`.
  中文翻译：RBAC：`alice` 有 `research:read`、`research:write`，可调用所有工具。`bob` 有 `research:read`，不能调用 `generate_report`。
- Pinned description manifest: dropped any server whose tool hashes changed.
  中文翻译：锁定描述清单：丢弃任何工具哈希变更的服务器。
- Rule of Two audit: no tool combines untrusted input, sensitive data, and consequential action.
  中文翻译：Rule of Two 审计：无工具组合不受信输入、敏感数据和后果性动作。

### Rendering

The final `generate_report` task returns content blocks plus a `ui://report/current` resource. The client's host (Claude Desktop, etc.) renders the interactive dashboard in a sandbox iframe. The dashboard contains a sorted paper list, citation counts, and a button that calls `host.callTool('summarize_paper', {arxiv_id})` for any paper the user clicks.

> 最终 `generate_report` 任务返回内容块加 `ui://report/current` 资源。客户端宿主（Claude Desktop 等）在沙盒 iframe 中渲染交互式仪表盘。仪表盘包含排序的论文列表、引用计数，以及用户点击任何论文时调用 `host.callTool('summarize_paper', {arxiv_id})` 的按钮。

### Packaging

The whole thing ships as:

```
research-system/
  AGENTS.md                     # project conventions
  skills/
    run-research/
      SKILL.md                  # the top-level workflow
  servers/
    research-mcp/               # the MCP server
      pyproject.toml
      src/
  agents/
    writer/                     # the A2A agent
  gateway/
    config.yaml                 # RBAC + pinned manifest
```

Users deploy with `docker compose up`. Claude Code, Cursor, Codex, and opencode users can drive the system by invoking the `run-research` skill.

> 用户用 `docker compose up` 部署。Claude Code、Cursor、Codex 和 opencode 用户可通过调用 `run-research` 技能驱动系统。

### What each Phase 13 lesson contributed

| Lesson | What the capstone uses |
|--------|------------------------|
| 01-05 | Tool interface, provider-portability, parallel calls, schemas, linting |
| 06-10 | MCP primitives, server, client, transports, resources + prompts |
| 11-14 | Sampling, roots + elicitation, async tasks, `ui://` apps |
| 15-17 | Tool poisoning, OAuth 2.1, gateway + registry |
| 18 | A2A sub-agent delegation |
| 19 | OTel GenAI tracing |
| 20 | Routing gateway for the LLM layer |
| 21 | SKILL.md + AGENTS.md packaging |

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 将前课模式缝合为一个可运行的端到端演示。全部标准库，全部进程内运行便于从头到尾阅读。完整流程：网关握手、模拟 OAuth 2.1、合并 tools/list、generate_report 作为任务、A2A 调用写作 Agent、返回 ui:// 资源、发射 OTel span。关注点：一个 trace id 贯穿每跳；网关策略阻止第二个用户写入；任务生命周期 working -> completed 返回文本和 ui:// 内容；A2A 调用内部状态对编排者不透明；AGENTS.md 和 SKILL.md 是其他 Agent 复现工作流所需的唯一文件。

`code/main.py` stitches the previous lessons' patterns into one runnable demo. All stdlib, all in-process so you can read it end to end. It runs the full flow for the research-and-report scenario: handshake with gateway, OAuth 2.1 simulated, tools/list merged, generate_report as a task, A2A call to writer, ui:// resource returned, OTel spans emitted.

> `code/main.py` 将前课模式缝合为一个可运行 demo。全部标准库、全部进程内运行，便于端到端阅读。它运行研究和报告场景的完整流程：与网关握手、OAuth 2.1 模拟、合并 tools/list、generate_report 作为任务、A2A 调用写作器、返回 ui:// 资源、发出 OTel span。

What to look at:

- One trace id across every hop.
  中文翻译：一个 trace id 跨每跳。
- Gateway policy blocks a second user from writing.
  中文翻译：网关策略阻止第二个用户写。
- Task lifecycle goes working → completed and returns both text and ui:// content.
  中文翻译：Task 生命周期走 working → completed，返回文本和 ui:// 内容。
- A2A call's inner state is opaque to the orchestrator.
  中文翻译：A2A 调用的内部状态对编排者不透明。
- AGENTS.md and SKILL.md are the only files another agent needs to reproduce the workflow.
  中文翻译：AGENTS.md 和 SKILL.md 是另一个 Agent 复现工作流所需的唯一文件。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-ecosystem-blueprint.md`——给定产品需求（研究、摘要、自动化），生成完整架构：哪些 MCP 原语、哪些网关控制、哪些 A2A 调用、哪些遥测、哪些打包。

This lesson produces `outputs/skill-ecosystem-blueprint.md`. Given a product need (research, summarization, automation), the skill produces the full architecture: which MCP primitives, which gateway controls, which A2A calls, which telemetry, which packaging.

> 本课产出 `outputs/skill-ecosystem-blueprint.md`。给定产品需求（研究、摘要、自动化），该 skill 生成完整架构：哪些 MCP 原语、哪些网关控制、哪些 A2A 调用、哪些遥测、哪些打包。

## Exercises | 练习题

1. Run `code/main.py`. Note the single trace id and how spans nest. Count how many primitives from Phase 13 the demo touches.
   中文翻译：运行 `code/main.py`。注意单一 trace id 和 span 如何嵌套。计数 demo 触及 Phase 13 多少个原语。

2. Extend the demo: add a second backend MCP server (e.g. `bibliography`) and confirm the gateway merges its tools into the same namespace.
   中文翻译：扩展 demo：添加第二个后端 MCP 服务器（如 `bibliography`），确认网关合并其工具到相同命名空间。

3. Replace the fake A2A writer agent with a real one running on a subprocess. Use the Lesson 19 harness.
   中文翻译：将假 A2A 写作 Agent 替换为在子进程上运行的真实 Agent。使用 Lesson 19 的线束。

4. Add a PII redaction step in the routing gateway between the orchestrator and the LLM. Confirm emails in the user query get scrubbed.
   中文翻译：在编排者和 LLM 之间的路由网关添加 PII 脱敏步骤。确认用户查询中的邮箱被清理。

5. Write an AGENTS.md for a teammate who will maintain this system. It should take under five minutes to read and give them everything they need to drive the capstone in Cursor or Codex.
   中文翻译：为将维护此系统的队友写 AGENTS.md。应 5 分钟内读完，给他们驱动 Cursor 或 Codex 中 capstone 所需的一切。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| Capstone | "Phase-13 integration demo" | End-to-end system using every primitive | 毕业项目：Phase 13 集成演示 |
| Research and report | "The scenario" | Search, summarize, render pattern | 研究与报告：搜索-摘要-渲染模式 |
| Ecosystem | "All the pieces together" | Server + client + gateway + sub-agent + telemetry + package | 生态系统：所有组件的整合 |
| Trace hierarchy | "Single trace id" | Every hop's span shares the trace; parent-child via span ids | 追踪层次：单一 trace id |
| Gateway-issued token | "Transitive auth" | Client sees only gateway's token; gateway holds upstream creds | 网关签发 token：传递式认证 |
| Merged namespace | "All tools in one flat list" | Multi-server merge at the gateway, prefix-on-collision | 合并命名空间：多服务器工具列表 |
| Opacity boundary | "A2A call hides internals" | Sub-agent's reasoning invisible to orchestrator | 不透明边界：A2A 隐藏内部推理 |
| Three-layer stack | "AGENTS.md + SKILL.md + MCP" | Project context + workflow + tools | 三层堆栈：项目上下文+工作流+工具 |
| Defense-in-depth | "Multiple security layers" | Pinned hashes, OAuth, RBAC, Rule of Two, audit log | 纵深防御：多层安全 |
| Spec compliance matrix | "What we ship that the spec requires" | Checklist mapping deliverables to 2025-11-25 requirements | 规范合规矩阵 |

## Further Reading | 延伸阅读

- [MCP — Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — consolidated reference
  中文翻译：合并参考
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — where the protocol is heading
  中文翻译：协议走向
- [a2a-protocol.org](https://a2a-protocol.org/latest/) — A2A v1.0 reference
  中文翻译：A2A v1.0 参考
- [OpenTelemetry — GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — canonical tracing conventions
  中文翻译：权威追踪约定
- [Anthropic — Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) — production agent runtime patterns
  中文翻译：生产 Agent 运行时模式
