# 编排 分层 主管 模式 群体

> Four orchestration patterns recur across 2026 frameworks: supervisor-worker, swarm / peer-to-peer, hierarchical, debate. Anthropic's guidance: "It's about building the right system for your needs." Start simple; add topology only when a single agent plus five workflow patterns is insufficient.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate)
**预计时间：** ~60 minutes

## 学习目标

- Name the four recurring orchestration patterns and when each fits.
- Describe the 2026 LangChain recommendation: tool-call-based supervision vs supervisor libraries.
- Explain Anthropic's "build the right system" rule and how it gates topology choice.
- Implement all four in stdlib against a common scripted LLM.

## 问题引入

> **【中文解读】** Agent 编排模式定义了多 Agent 系统中的任务分配和协调方式。四种核心模式：(1) 顺序——任务在 Agent 之间线性传递；(2) 并行——多个 Agent 同时处理不同子任务；(3) 分层——管理者 Agent 分配任务给工作者 Agent；(4) 对等——Agent 之间平等协作。
> **【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】** Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（Prompt Chaining、Routing、Parallelization、Orchestrator-Workers）已成为标准。实际应用中，大多数系统混合使用多种模式——例如客服系统先用路由模式分类请求，再用分层模式分配给专门 Agent。LangGraph 的状态图是实现复杂编排的主流工具。

## 核心概念

### Supervisor-worker
- A central routing LLM dispatches to specialist agents.
- Decides: loop back to self, hand off to specialist, terminate.
- Specialists do not talk to each other; all routing goes through the supervisor.
Frameworks: LangGraph `create_supervisor`, Anthropic orchestrator-workers, CrewAI Hierarchical Process.
**2026 LangChain recommendation:** do supervision through direct tool calls rather than `create_supervisor`. Gives finer context engineering control — you decide exactly what each specialist sees.
### Swarm / peer-to-peer
- Agents hand off directly via a shared tool surface.
- No central router.
- Lower latency than supervisor (fewer hops).
- Harder to reason about (no single point of control).
Frameworks: LangGraph swarm topology, OpenAI Agents SDK handoffs (when all agents can hand off to all others).
### Hierarchical
- Supervisors managing sub-supervisors managing workers.
- Implemented as nested subgraphs in LangGraph; nested crews in CrewAI.
- Scales to large agent populations at the cost of operational complexity.
When you need it: when a single supervisor's context budget cannot hold descriptions of all specialists.
### Debate
- Parallel proposers + iterative cross-critique (Lesson 25).
- Not really orchestration — more verification — but shows up as a topology choice in frameworks.
### CrewAI Crew vs Flow
CrewAI formalizes two deployment modes:
- **Flow** for deterministic event-driven automation (recommended starting point for production).
- **Crew** for autonomous role-based collaboration.
This is orthogonal to the four patterns above but maps to topology: Flow is typically supervisor or hierarchical; Crew is typically supervisor with an LLM router.
### Anthropic's guidance
"Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."
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

## 动手实现

`code/main.py` implements all four patterns in stdlib against a scripted LLM:
- `Supervisor` — central router.
- `Swarm` — peer-to-peer with direct handoffs.
- `Hierarchical` — supervisors of supervisors.
- `Debate` — parallel proposers + critique.
Each pattern handles the same three-intent task (refund / bug / sales). Trace shapes differ.
Run it:
```
python3 code/main.py
```
Output: per-pattern trace + op count. Supervisor is cleanest; swarm is shortest; hierarchical is deepest; debate is most expensive.

## 用框架实现

- **LangGraph** for supervisor and hierarchical (nested subgraphs).
- **OpenAI Agents SDK** for handoffs-as-tools (supervisor-shaped).
- **CrewAI Flow** for production deterministic.
- **Custom** for debate or when you want exact control.

## 产出物

`outputs/skill-orchestration-picker.md` picks a topology and implements it.

## 练习题

1. Convert a supervisor-worker to a swarm by removing the router. What breaks? What improves?
   *思考并实践此练习*
2. Add a hop counter to the swarm: refuse after 3 handoffs. Does it catch A->B->A bouncing?
   *思考并实践此练习*
3. Build a two-level hierarchical system for a 12-specialist domain. Where does the context budget fail without nesting?
   *思考并实践此练习*
4. Profile the four patterns on a production-shaped workload. Which wins on which metric (latency, cost, accuracy, debuggability)?
   *思考并实践此练习*
5. Read Anthropic's "Building Effective Agents" post. Map each of your production flows to one of the four. Any that don't map cleanly?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Supervisor-worker | "Router + specialists" |
| Swarm | "Peer-to-peer" |
| Hierarchical | "Supervisors of supervisors" |
| Debate | "Proposer + critique" |
| Tool-call-based supervision | "Supervisor without a library" |
| Crew | "Autonomous team" |
| Flow | "Deterministic workflow" |

## 延伸阅读

