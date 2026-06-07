# Agent Workbench Engineering: Why Capable Models Still Fail | 工程 工作台 为什么

> A capable model is not enough. Reliable agents need a workbench: instructions, state, scope, feedback, verification, review, and handoff. Strip those away and even a frontier model produces work that is unsafe to ship.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 26 (Failure Modes) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Separate model capability from execution reliability.
- Name the seven workbench surfaces that decide whether an agent ships.
- Compare a prompt-only run against a workbench-guided run on a small repo task.
- Produce a failure-mode report that maps each missed surface to the symptom it caused.

## The Problem | 问题引入

You drop a frontier model into a real repo and ask it to add input validation. It opens four files, writes plausible code, declares success, and stops. You run the tests. Two fail. A third file is touched that had nothing to do with validation. There is no record of what the agent assumed, what it tried first, or what is left to do.

The model was not wrong about Python. It was wrong about the work. It had no idea what counted as done, where it was allowed to write, what tests were authoritative, or how the next session was supposed to pick up.


> **【中文解读】** Agent 在真实仓库中失败的原因分析：(1) 指令遵循失败——忽略约束或编造不存在的能力；(2) 上下文窗口耗尽——长代码库超出窗口导致关键信息丢失；(3) 错误累积——小错误在多步执行中雪崩式放大；(4) 缺乏项目记忆——不知道代码库的约定和架构。

This is not a model bug. It is a workbench bug. The surface around the agent is missing the parts that turn a one-shot generation into reliable, resumable engineering.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

## The Concept | 核心概念

A workbench is the operating environment that wraps the model during a task. It has seven surfaces:

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

| Surface | What it carries | Failure when missing |
|---------|-----------------|----------------------|
| Instructions | Startup rules, forbidden actions, definition of done | Agent guesses what shipping means |
| State | Current task, touched files, blockers, next action | Each session restarts from zero |
| Scope | Allowed files, forbidden files, acceptance criteria | Edits leak into unrelated code |
| Feedback | Real command output captured into the loop | Agent declares success on a 400 |
| Verification | Tests, lint, smoke run, scope check | "Looks good" reaches main |
| Review | A second pass with a different role | Builder marks own homework |
| Handoff | What changed, why, what is left | Next session re-discovers everything |


> **【中文解读】** Agent 在真实仓库中失败的原因分析：(1) 指令遵循失败——忽略约束或编造不存在的能力；(2) 上下文窗口耗尽——长代码库超出窗口导致关键信息丢失；(3) 错误累积——小错误在多步执行中雪崩式放大；(4) 缺乏项目记忆——不知道代码库的约定和架构。

The workbench is independent of the model. You can swap the model and keep the surfaces. You cannot swap the surfaces and keep reliability.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

```mermaid
flowchart LR
  Task[Task] --> Scope[Scope Contract]
  Scope --> State[Repo Memory]
  State --> Agent[Agent Loop]
  Agent --> Feedback[Runtime Feedback]
  Feedback --> Verify[Verification Gate]
  Verify --> Review[Reviewer]
  Review --> Handoff[Handoff]
  Handoff --> State
```

The loop closes on the state file, not on chat history. Chat is volatile. The repo is the system of record.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### Workbench versus prompt engineering

Prompting tells the model what you want this turn. A workbench tells the model how to do work across turns and across sessions. Most agent failure stories are workbench failures wearing prompt-engineering clothes.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### Workbench versus framework

A framework gives you a runtime (LangGraph, AutoGen, Agents SDK). A workbench gives the agent a place to work inside that runtime. You need both. This mini-track is about the second one.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### Reasoning from primitives, not from vendor taxonomies

There is a lot of writing on "harness engineering" right now. Addy Osmani, OpenAI, Anthropic, LangChain, Martin Fowler, MongoDB, HumanLayer, Augment Code, Thoughtworks, the walkinglabs awesome list, and a steady drumbeat of Medium and Hacker News pieces are all carrying it. They disagree on the boundary of what a harness is, what is in scope, and which vocabulary to use. We do not need to pick a side. The seven surfaces are a UX layer; underneath every workbench is the same set of distributed-systems primitives that hold up any reliable backend.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

Strip the agent label off for a moment. An agent run is computation that crosses time, processes, and machines. To make that reliable you need the same primitives any production system needs.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

| Primitive | What it is | What it carries for an agent |
|-----------|------------|------------------------------|
| Function | Typed handler. Pure where possible. Owns its inputs and outputs. | A tool call, a rule check, a verification step, a model invocation |
| Worker | Long-lived process that owns one or more functions and a lifecycle | The builder, the reviewer, the verifier, an MCP server |
| Trigger | Event source that invokes a function | Agent loop tick, HTTP request, queue message, cron, file change, hook |
| Runtime | The boundary that decides what runs where, with what timeouts and resources | Claude Code's process, LangGraph's runtime, a worker container |
| HTTP / RPC | The wire between caller and worker | Tool-call protocol, MCP request, model API |
| Queue | Durable buffer between trigger and worker; back-pressure, retry, idempotency | The task board, the feedback log, the review inbox |
| Session persistence | State that survives crashes, restarts, model swaps | `agent_state.json`, checkpoints, KV stores, the repo itself |
| Authorization policy | Who can call what function with which scope | Allowed/forbidden files, approval boundaries, MCP capability lists |

Now map the seven workbench surfaces onto those primitives.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

- **Instructions** — policy + function metadata. Rules are checks (functions). The router (`AGENTS.md`) is policy attached to the runtime's startup.
- **State** — session persistence. A keyed store the runtime reads at every step. File, KV, or DB; the persistence semantics matter, the storage backend does not.
- **Scope** — authorization policy per task. Allowed/forbidden globs are an ACL. Approvals required are a permission lattice.
- **Feedback** — invocation log written into a queue. Every shell call is a record, durable, replayable.
- **Verification** — a function. Deterministic over inputs. Triggered on task close. Fails closed.
- **Review** — a separate worker with read-only authz on builder artifacts and write-only authz on review reports.
- **Handoff** — a durable record emitted by a session-end trigger. The next session's startup trigger reads it.

The agent loop itself is a worker that consumes events (user message, tool result, timer tick), calls functions (the model, then the tools the model picks), writes records (state, feedback), and emits triggers (verify, review, handoff). No mystery; the same shape as a job processor.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### Patterns in circulation, translated to primitives

Every popular harness pattern reduces to the eight primitives. Translation table.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

| Vendor or community pattern | What it actually is |
|------------------------------|--------------------|
| Ralph Loop (Claude Code, Codex, agentic_harness book) — re-inject original intent into a fresh context window when the agent tries to stop early | A trigger that re-enqueues a task with a clean context; session persistence carries the goal forward |
| Plan / Execute / Verify (PEV) | Three workers, one per role, communicating via state and a queue between phases |
| Harness-compute separation (OpenAI Agents SDK, April 2026) — split control plane from execution plane | Restating control-plane / data-plane. Predates the agent label by decades |
| Open Agent Passport (OAP, March 2026) — sign and audit every tool call against a declarative policy before execution | An authorization policy enforced by a pre-action worker, with a signed audit queue |
| Guides and Sensors (Birgitta Böckeler / Thoughtworks) — feedforward rules + feedback observability | Authorization policy + verification functions + observability traces |
| Progressive compaction, 5-stage (Claude Code reverse engineering, April 2026) | A state-management worker that runs cron-like over session persistence to keep it within a budget |
| Hooks / middleware (LangChain, Claude Code) — intercept model and tool calls | Triggers + functions wrapped around the runtime's invocation path |
| Skills as Markdown with progressive disclosure (Anthropic, Flue) | A function registry where the function metadata is loaded into context just-in-time |
| Sandbox agents (Codex, Sandcastle, Vercel Sandbox) | The compute plane: a runtime with isolated filesystem, network, and lifecycle |
| MCP servers | Workers exposing functions over a stable RPC, with capability lists as authorization |

Every entry in that table is the agent community arriving at a primitive that already had a name in distributed systems and giving it a new one. Useful labels for marketing; not useful as engineering vocabulary.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### What the receipts actually say

The harness-over-model claim has numbers behind it now. Worth knowing, because they are also the only honest argument against "just wait for a smarter model."

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

- Terminal Bench 2.0 — same model, harness change moved a coding agent from outside the top 30 to rank five (LangChain, *Anatomy of an Agent Harness*).
- Vercel — deleted 80% of its agent's tools; success rate jumped from 80% to 100% (MongoDB).
- Harvey — legal agents more than doubled accuracy through harness optimization alone (MongoDB).
- 88% of enterprise AI agent projects fail to reach production. The failures cluster around runtime, not reasoning (preprints.org, *Harness Engineering for Language Agents*, March 2026).
- A 2025 benchmark study across three popular open-source frameworks reported ~50% task completion; long-context WebAgent collapsed from 40-50% to under 10% in long-context conditions, mostly from infinite loops and goal loss (covered widely in early 2026 writeups).

The takeaway is not "harness wins forever." Models do absorb harness tricks over time. The takeaway is that today, the load-bearing engineering is around the model, not inside it, and the primitives that carry that load are the ones every production system has always needed.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

### Where vendor writeups stop short

This is the part you do not need to be polite about.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

- LangChain's *Anatomy of an Agent Harness* enumerates eleven components — prompts, tools, hooks, sandboxes, orchestration, memory, skills, subagents, and a runtime "dumb loop." It does not name queues, workers as a deployment unit, trigger semantics, session persistence as a separate concern, or authorization policy. It treats the harness as an object you configure, not as a system you deploy.
- Addy Osmani's *Agent Harness Engineering* lands the framing `Agent = Model + Harness` and the ratchet pattern, but stops short of saying what a harness is built out of. It reads as a stance, not a spec.
- Anthropic and OpenAI go deepest on the surfaces but stay inside their own runtimes. The "harness-compute separation" announcement in the April 2026 Agents SDK is the first vendor piece that explicitly endorses the control-plane / data-plane split. That is a primitive idea, not a new one.
- The agentic_harness book treats harness as a config object (Jaymin West's *Agentic Engineering*, chapter 6) and the strongest line in it is "the harness is the primary security boundary in an agentic system." That is just authorization policy, restated.
- Hacker News threads keep arriving at the same place. The April 2026 thread *The agent harness belongs outside the sandbox* argues the harness should sit "more like a hypervisor that sits outside everything and authorises access based on context and user." That is, again, authorization policy as a separate plane.

You do not need to disagree with any of these pieces to notice the gap. They are writing UX descriptions of a system that already exists. We are writing the system. When the system is built right, the seven surfaces fall out of the primitives. When it is built wrong, no amount of `AGENTS.md` polish fixes the missing queue.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

So when you hear "harness engineering" elsewhere, translate to primitives. Prompts and rules are policy and functions. Scaffolding is the runtime. Guardrails are authorization + verification. Hooks are triggers. Memory is session persistence. The Ralph Loop is requeue. Subagents are workers. Sandboxes are compute planes. The vocabulary changes; the engineering does not. The workbench is the agent-facing UX; the harness, in the sense that survives the next vendor reframe, is functions, workers, triggers, runtimes, queues, persistence, and policy wired together correctly.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

## Build It | 动手实现

`code/main.py` runs a tiny repo task twice. First as prompt only, then with the seven surfaces wired in. Same model, same task. The script counts which surfaces were missing on the failed run and prints a failure-mode report.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

The repo task is small on purpose: add input validation to a one-file FastAPI-style handler and write a passing test.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

Run it:

```
python3 code/main.py
```

Output: a side-by-side log of the two runs, a `failure_modes.json` summarizing the prompt-only run, and a one-line verdict for the workbench run.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

The agent is a tiny rule-based stub; the point is the surfaces, not the model. Across the rest of this mini-track you will rebuild each surface as a real, reusable artifact.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

## Use It | 用框架实现

Three places workbench surfaces already exist in the wild, even if no one calls them that:

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

- **Claude Code, Codex, Cursor.** `AGENTS.md` and `CLAUDE.md` are the instructions surface. Slash commands are scope. Hooks are verification.
- **LangGraph, OpenAI Agents SDK.** Checkpoints and session stores are the state surface. Handoffs are the handoff surface.
- **CI on a real repo.** Tests, lint, and type-check are verification. The PR template is handoff. CODEOWNERS is review.

Workbench engineering is the discipline of making those surfaces explicit and reusable, instead of leaving each team to rediscover them.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

## Ship It | 产出物

`outputs/skill-workbench-audit.md` is a portable skill that audits an existing repo for the seven workbench surfaces and reports which are missing, which are partial, and which are healthy. Drop it next to any agent setup; it tells you what to fix first.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

## Exercises | 练习题

1. Pick a repo where you already run an agent. Score the seven surfaces from 0 (missing) to 2 (healthy). What is your weakest surface?
  中文翻译：思考并实践此练习。
2. Extend `main.py` so the prompt-only run also produces a fake "success" claim. Verify the verification gate would have caught it.
  中文翻译：思考并实践此练习。
3. Add an eighth surface for your own product. Justify why it does not collapse into one of the existing seven.
  中文翻译：思考并实践此练习。
4. Re-run the script with a different stub agent that hallucinates an extra file write. Which surface catches it first?
  中文翻译：思考并实践此练习。
5. Map the five industry-recurring failure modes from Phase 14 · 26 onto the seven surfaces. Which mode is each surface designed to absorb?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Workbench | "The setup" | Engineered surfaces around the model that make work reliable |  |
| Surface | "A doc" or "a script" | A named, machine-readable input the agent reads or writes every turn |  |
| System of record | "The notes" | The file the agent treats as truth when chat history is gone |  |
| Definition of done | "Acceptance" | An objective, file-backed checklist the agent cannot fake |  |
| Workbench audit | "Repo readiness check" | A pass over the seven surfaces that flags missing pieces before work begins |  |

## Further Reading | 延伸阅读

Read these as data points, not as authorities. Each one is a partial taxonomy. Translate every concept back to a primitive (function, worker, trigger, runtime, HTTP/RPC, queue, persistence, policy) before deciding whether to adopt it.

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

Vendor framings:

- [Addy Osmani, Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — `Agent = Model + Harness` and the ratchet pattern; thin on infrastructure
  中文翻译：见原文。
- [LangChain, The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) — eleven components: prompts, tools, hooks, orchestration, sandboxes, memory, skills, subagents, runtime; omits queues, deployment, authz
  中文翻译：见原文。
- [OpenAI, Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — Codex team's view of the surfaces around their runtime
  中文翻译：见原文。
- [OpenAI, Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) — the agent loop reduced to a `while` over function calls
  中文翻译：见原文。
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — long-horizon surfaces inside a specific runtime
  中文翻译：见原文。
- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — applied design notes
  中文翻译：见原文。
- [LangChain Deep Agents harness capabilities](https://docs.langchain.com/oss/python/deepagents/harness) — runtime config surface
  中文翻译：见原文。

Practitioner pieces with usable detail:

- [Martin Fowler / Birgitta Böckeler, Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) — guides (feedforward) + sensors (feedback); the cleanest control-theory framing
  中文翻译：见原文。
- [HumanLayer, Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) — "it's not a model problem, it's a configuration problem"
  中文翻译：见原文。
- [MongoDB, The Agent Harness: Why the LLM Is the Smallest Part of Your Agent System](https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system) — receipts: Vercel 80% to 100%, Harvey 2x accuracy, Terminal Bench Top 30 to Top 5
  中文翻译：见原文。
- [Augment Code, Harness Engineering for AI Coding Agents](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) — constraint-first walkthrough
  中文翻译：见原文。
- [Sequoia podcast, Harrison Chase on Context Engineering Long-Horizon Agents](https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/) — runtime concerns over model concerns
  中文翻译：见原文。

Books, papers, and reference implementations:

- [Jaymin West, Agentic Engineering — Chapter 6: Harnesses](https://www.jayminwest.com/agentic-engineering-book/6-harnesses) — book-length treatment, treats harness as the primary security boundary
  中文翻译：见原文。
- [preprints.org, Harness Engineering for Language Agents (March 2026)](https://www.preprints.org/manuscript/202603.1756) — academic framing as control / agency / runtime
  中文翻译：见原文。
- [walkinglabs/awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering) — curated reading list across context, evaluation, observability, orchestration
  中文翻译：见原文。
- [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) — alternate curated list (tools, evals, memory, MCP, permissions)
  中文翻译：见原文。
- [andrewgarst/agentic_harness](https://github.com/andrewgarst/agentic_harness) — production-ready reference implementation with Redis-backed memory and eval suite
  中文翻译：见原文。
- [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) — open agent harness with built-in personal agent
  中文翻译：见原文。

Hacker News threads worth reading for the disagreements, not the consensus:

> Agent Workbench 分析模型失败的根本原因。主要失败模式包括：指令遵循失败、工具使用错误、上下文丢失和推理链断裂。

- [HN: Effective harnesses for long-running agents](https://news.ycombinator.com/item?id=46081704)
  中文翻译：见原文。
- [HN: Improving 15 LLMs at Coding in One Afternoon. Only the Harness Changed](https://news.ycombinator.com/item?id=46988596)
  中文翻译：见原文。
- [HN: The agent harness belongs outside the sandbox](https://news.ycombinator.com/item?id=47990675) — argues for authorization as a separate plane
  中文翻译：见原文。

Cross-references inside this curriculum:

- Phase 14 · 23 — OpenTelemetry GenAI conventions: the observability layer the sensors literature points at
- Phase 14 · 26 — Failure modes catalog the seven surfaces are designed to absorb
- Phase 14 · 27 — Prompt injection defenses that sit at the authorization-policy primitive
- Phase 14 · 29 — Production runtimes (queue, event, cron): where the primitives in this lesson live in deployment
