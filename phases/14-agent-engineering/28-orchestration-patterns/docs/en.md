# Orchestration Patterns: Supervisor, Swarm, Hierarchical | 编排 分层 主管 模式 群体

> Four orchestration patterns recur across 2026 frameworks: supervisor-worker, swarm / peer-to-peer, hierarchical, debate. Anthropic's guidance: "It's about building the right system for your needs." Start simple; add topology only when a single agent plus five workflow patterns is insufficient.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Name the four recurring orchestration patterns and when each fits.
- Describe the 2026 LangChain recommendation: tool-call-based supervision vs supervisor libraries.
- Explain Anthropic's "build the right system" rule and how it gates topology choice.
- Implement all four in stdlib against a common scripted LLM.

## The Problem | 问题引入

Teams reach for "multi-agent" before they need it. Four patterns recur across frameworks; once you can name them, you can pick the right one — or skip topology entirely.

> 团队在不必要的时候就使用了"多 Agent"。四种模式在框架中反复出现；一旦你能命名它们，你就能选择正确的一个——或者完全跳过拓扑。


> **【中文解读】** Agent 编排模式定义了多 Agent 系统中的任务分配和协调方式。四种核心模式：(1) 顺序——任务在 Agent 之间线性传递；(2) 并行——多个 Agent 同时处理不同子任务；(3) 分层——管理者 Agent 分配任务给工作者 Agent；(4) 对等——Agent 之间平等协作。

> **{【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】}** Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（Prompt Chaining、Routing、Parallelization、Orchestrator-Workers）已成为标准。实际应用中，大多数系统混合使用多种模式——例如客服系统先用路由模式分类请求，再用分层模式分配给专门 Agent。LangGraph 的状态图是实现复杂编排的主流工具。
## The Concept | 核心概念

### Supervisor-worker

- A central routing LLM dispatches to specialist agents.
- Decides: loop back to self, hand off to specialist, terminate.
- Specialists do not talk to each other; all routing goes through the supervisor.

Frameworks: LangGraph `create_supervisor`, Anthropic orchestrator-workers, CrewAI Hierarchical Process.

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

**2026 LangChain recommendation:** do supervision through direct tool calls rather than `create_supervisor`. Gives finer context engineering control — you decide exactly what each specialist sees.

> **2026 年 LangChain 建议：** 通过直接工具调用而不是 `create_supervisor` 来实现监督。提供更精细的上下文工程控制——你可以精确决定每个专家看到什么。

### Swarm / peer-to-peer

- Agents hand off directly via a shared tool surface.
- No central router.
- Lower latency than supervisor (fewer hops).
- Harder to reason about (no single point of control).

Frameworks: LangGraph swarm topology, OpenAI Agents SDK handoffs (when all agents can hand off to all others).

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

### Hierarchical

- Supervisors managing sub-supervisors managing workers.
- Implemented as nested subgraphs in LangGraph; nested crews in CrewAI.
- Scales to large agent populations at the cost of operational complexity.

When you need it: when a single supervisor's context budget cannot hold descriptions of all specialists.

> 何时需要：当单个监督者的上下文预算无法容纳所有专家的描述时。

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

### Debate

- Parallel proposers + iterative cross-critique (Lesson 25).
- Not really orchestration — more verification — but shows up as a topology choice in frameworks.

### CrewAI Crew vs Flow

CrewAI formalizes two deployment modes:

- **Flow** for deterministic event-driven automation (recommended starting point for production).
- **Crew** for autonomous role-based collaboration.

This is orthogonal to the four patterns above but maps to topology: Flow is typically supervisor or hierarchical; Crew is typically supervisor with an LLM router.

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

### Anthropic's guidance

"Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

Decision order:

1. Single agent + workflow patterns (Lesson 12) — start here.
2. Supervisor-worker — when you have 2-4 specialists.
3. Swarm — when latency matters more than reasoning clarity.
4. Hierarchical — only when supervisor context budget fails.
5. Debate — when accuracy matters more than cost.

### Where this pattern goes wrong

- **Topology-first thinking.** "We need multi-agent" before identifying what problem multi-agent solves.
- **Bouncing handoffs in swarm.** A -> B -> A -> B. Use hop counters.
- **Fake hierarchy.** Three layers because "enterprise"; two actual teams. Collapse.

> **拓扑优先思维。** 在确定多 Agent 解决什么问题之前就说"我们需要多 Agent"。
> **群体中弹跳交接。** A -> B -> A -> B。使用跳数计数器。
> **虚假层级。** 因为"企业级"就设三层；实际只有两个团队。合并。

## Build It | 动手实现

`code/main.py` implements all four patterns in stdlib against a scripted LLM:

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

- `Supervisor` — central router.
- `Swarm` — peer-to-peer with direct handoffs.
- `Hierarchical` — supervisors of supervisors.
- `Debate` — parallel proposers + critique.

Each pattern handles the same three-intent task (refund / bug / sales). Trace shapes differ.

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

Run it:

```
python3 code/main.py
```

Output: per-pattern trace + op count. Supervisor is cleanest; swarm is shortest; hierarchical is deepest; debate is most expensive.

> 输出：每模式追踪 + 操作数。监督者最清晰；群体最短；层级最深；辩论最昂贵。

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

## Use It | 用框架实现

- **LangGraph** for supervisor and hierarchical (nested subgraphs).
- **OpenAI Agents SDK** for handoffs-as-tools (supervisor-shaped).
- **CrewAI Flow** for production deterministic.
- **Custom** for debate or when you want exact control.

## Ship It | 产出物

`outputs/skill-orchestration-picker.md` picks a topology and implements it.

> `outputs/skill-orchestration-picker.md` 选择一个拓扑并实现它。

> 编排模式描述多 Agent 系统的组织方式。主要模式包括：监督者（中央路由）、群体（点对点移交）、层次化（嵌套监督）、管道（顺序处理）。

## Exercises | 练习题

1. Convert a supervisor-worker to a swarm by removing the router. What breaks? What improves?
  中文翻译：思考并实践此练习。
2. Add a hop counter to the swarm: refuse after 3 handoffs. Does it catch A->B->A bouncing?
  中文翻译：思考并实践此练习。
3. Build a two-level hierarchical system for a 12-specialist domain. Where does the context budget fail without nesting?
  中文翻译：思考并实践此练习。
4. Profile the four patterns on a production-shaped workload. Which wins on which metric (latency, cost, accuracy, debuggability)?
  中文翻译：思考并实践此练习。
5. Read Anthropic's "Building Effective Agents" post. Map each of your production flows to one of the four. Any that don't map cleanly?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Supervisor-worker | "Router + specialists" | Central LLM dispatches to specialists; they don't talk to each other |  |
| Swarm | "Peer-to-peer" | Direct handoffs via shared tools; no central router |  |
| Hierarchical | "Supervisors of supervisors" | Nested subgraphs for large populations |  |
| Debate | "Proposer + critique" | Parallel proposers, cross-critique (Lesson 25) |  |
| Tool-call-based supervision | "Supervisor without a library" | Implement supervisor as direct tool calls for context control |  |
| Crew | "Autonomous team" | CrewAI's role-based collaboration mode |  |
| Flow | "Deterministic workflow" | CrewAI's event-driven production mode |  |

## Further Reading | 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — five patterns + agent vs workflow
  中文翻译：见原文。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — supervisor, swarm, hierarchical
  中文翻译：见原文。
- [CrewAI docs](https://docs.crewai.com/en/introduction) — Crew vs Flow
  中文翻译：见原文。
- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) — debate pattern
  中文翻译：见原文。
