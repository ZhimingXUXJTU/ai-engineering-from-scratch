# Case Studies and the 2026 State of the Art | 案例研究 状态

> Three production-grade references to study end-to-end, each illustrating a different slice of multi-agent engineering. **Anthropic's Research system** (orchestrator-worker, 15x tokens, +90.2% over single-agent Opus 4, rainbow deployments) is the canonical supervisor case. **MetaGPT / ChatDev** (SOP-encoded role specialization for software engineering; ChatDev's "communicative dehallucination"; MacNet extension to >1000 agents via DAGs, arXiv:2406.07155) is the canonical role-decomposition case. **OpenClaw / Moltbook** (originally Clawdbot by Peter Steinberger, November 2025; renamed twice; 247k GitHub stars by March 2026; local ReAct-loop agents; Moltbook as an agent-only social network with ~2.3M agent accounts within days of launch, acquired by Meta 2026-03-10) illustrates what happens at population scale: emergent economic activity, prompt-injection risks, state-level regulation (China restricted OpenClaw on government computers, March 2026). **Framework landscape April 2026:** LangGraph and CrewAI lead production; AG2 is the community AutoGen continuation; Microsoft AutoGen is in maintenance mode (merged into Microsoft Agent Framework, RC Feb 2026); OpenAI Agents SDK is the production Swarm successor; Google ADK (April 2025) is the A2A-native entrant. Every major framework now ships MCP support; most ship A2A. This lesson reads each case end-to-end and distills the common patterns so you can pick the right reference for your next production system.

> **【中文解读】** 本节介绍了 2026 年 SOTA 多 Agent 案例研究——最新最佳多 Agent 系统的分析。

> **【拓展：case studies 2026 sota→具体应用】** 2026年 SOTA 多 Agent 系统案例：(1) Anthropic 的 Claude Research——多 Agent 协作进行深度研究；(2) OpenAI 的 Codex——多 Agent 协作编码；(3) 微软的 AutoGen 团队——多 Agent 软件开发。共同趋势：专业化分工、层次化编排、MCP 工具使用和 A2A Agent 间通信的结合。


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Problem | 问题引入

Multi-agent engineering is a young discipline. The production references are few, and each covers a different part of the space. Reading them one at a time is useful; comparing them as a set is more useful. This lesson treats three canonical 2026 case studies as an end-to-end reading list, pins the common patterns, and maps the framework landscape so you can make framework choices from knowledge, not marketing.

> 多 Agent 工程是一个年轻的学科。生产参考很少，每个覆盖空间的不同部分。逐一阅读是有用的；作为一个集合比较更有用。本课将三个规范的 2026 年案例研究作为端到端阅读清单，确定共同模式，并映射框架景观，使你能基于知识而非营销做出框架选择。

## Concept | 核心概念

### Anthropic Research system

The production supervisor-worker case. Claude Opus 4 plans and synthesizes; Claude Sonnet 4 subagents research in parallel. Published engineering post: https://www.anthropic.com/engineering/multi-agent-research-system.

Key measured results:

> 关键测量结果：

- **+90.2%** improvement over single-agent Opus 4 on internal research evals.
  中文翻译：在内部研究评估上比单 Agent Opus 4 提升 **+90.2%**。
- **80% of BrowseComp variance** explained by **token usage alone** — multi-agent wins largely because each subagent gets a fresh context window.
  中文翻译：**80% 的 BrowseComp 方差**仅由 **token 使用量**解释——多 Agent 胜出主要因为每个子 Agent 获得新的上下文窗口。
- **15x tokens per query** vs single-agent.
  中文翻译：每查询 **15 倍 token** vs 单 Agent。
- **Rainbow deployment** because agents are long-running and stateful.
  中文翻译：**彩虹部署**因为 Agent 是长时间运行且有状态的。

Design lessons codified:

> 编码化的设计教训：

1. **Scale effort to query complexity.** Simple → 1 agent with 3-10 tool calls. Medium → 3 agents. Complex research → 10+ subagents.
   中文翻译：**按查询复杂度扩展工作量。** 简单 → 1 个 Agent 3-10 次工具调用。中等 → 3 个 Agent。复杂研究 → 10+ 子 Agent。
2. **Broad first, then narrow.** Subagents do wide searches; lead synthesizes; follow-up subagents do targeted deeps.
   中文翻译：**先广后窄。** 子 Agent 做广泛搜索；主 Agent 综合；后续子 Agent 做定向深挖。
3. **Rainbow deploys.** Keep old runtime versions alive until their in-flight agents finish.
   中文翻译：**彩虹部署。** 保持旧运行时版本活跃直到进行中的 Agent 完成。
4. **Verification is not optional.** The system was observed to hallucinate without explicit verifier roles.
   中文翻译：**验证不是可选的。** 系统在没有显式验证者角色时被观察到产生幻觉。

This is the reference case for supervisor-worker topology (Phase 16 · 05) at production scale.

### MetaGPT / ChatDev

The production SOP-role-decomposition case. Cover arXiv:2308.00352 (MetaGPT) and arXiv:2307.07924 (ChatDev).

MetaGPT encodes software-engineering SOPs as role prompts: Product Manager, Architect, Project Manager, Engineer, QA Engineer. The paper's framing: `Code = SOP(Team)`. Each role has a narrow, specialized prompt; inter-role handoffs carry structured artifacts (PRD docs, architecture docs, code).

ChatDev's contribution: **communicative dehallucination**. Agents request specifics before answering — a designer agent asks the programmer what language is intended before sketching UI, rather than guessing. The paper reports this reduces hallucination in multi-agent pipelines measurably.

MacNet (arXiv:2406.07155) extends ChatDev to **>1000 agents via DAGs**. Each DAG node is a role specialization; edges encode handoff contracts. The scale is possible because routing is explicit and offline-computable.

Design lessons:

> 设计教训：

1. **Structure matters more than size.** A tight 5-role SOP team beats a 50-agent unstructured group.
   中文翻译：**结构比规模更重要。** 紧凑的 5 角色 SOP 团队胜过 50 Agent 的非结构化组。
2. **Handoff contracts in writing.** Artifacts passed between roles follow a schema.
   中文翻译：**书面交接契约。** 角色间传递的制品遵循模式。
3. **Communicative dehallucination** is a cheap, load-bearing pattern.
   中文翻译：**交际去幻觉**是一种廉价、承重的模式。
4. **DAGs scale further than chat.** When the flow is knowable, encode it.
   中文翻译：**DAG 比聊天扩展更远。** 当流程可知时，编码它。

This is the reference case for role specialization (Phase 16 · 08) and structured topology (Phase 16 · 15).

### OpenClaw / Moltbook ecosystem

The production population-scale case. Timeline:

- **Nov 2025:** Clawdbot (Peter Steinberger's local ReAct-loop coding agent) ships.
- **Dec 2025 – Mar 2026:** renamed twice (Clawdbot → OpenClaw → continued under OpenClaw).
- **Feb 2026:** Moltbook launches as an agent-only social network on the same primitives; ~2.3M agent accounts within days.
- **Mar 2026 (2026-03-10):** Meta acquires Moltbook.
- **Mar 2026:** China restricts OpenClaw on government computers.
- **Mar 2026:** OpenClaw crosses 247k GitHub stars.

This is what multi-agent looks like when you put millions of agents on a shared substrate:

- **Emergent economic activity.** Agents buy, sell, and service each other using token-payments.
- **Prompt-injection risks at population scale.** One malicious prompt in a viral agent profile propagates to thousands of agent-to-agent interactions in hours.
- **State-level regulatory response.** Within weeks of launch, regulation reaches the ecosystem.

The design lessons from this case are partly technical, partly governance:

1. **Multi-agent at population scale is a new regime.** Individual-system best practices (verification, role clarity) still apply but are not sufficient.
2. **Prompt injection is the new XSS.** Treat agent profiles and cross-agent messages as untrusted input by default.
3. **Regulation is faster than design cycles.** Plan for it.
4. **Open-source + viral scale compounds.** 247k stars in ~4 months is unusual; design for deploy-burst-load.

See [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) and CNBC / Palo Alto Networks reporting for ecosystem detail. For the technical underpinnings, the Clawdbot / OpenClaw repos expose the local ReAct loop; Moltbook's public posts reveal the social-graph architecture on top.

### Framework landscape April 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

Every major framework now ships **MCP** support; most ship **A2A**. Protocol compatibility is no longer a differentiator.

### The common patterns across all three cases

1. **Orchestrator + workers** (Anthropic explicit supervisor, MetaGPT PM-as-supervisor, OpenClaw individual agents + network effects).
   中文翻译：**编排者 + 工作者**（Anthropic 显式监督者，MetaGPT PM 作监督者，OpenClaw 独立 Agent + 网络效应）。
2. **Structured handoff contracts** (Anthropic subagent task descriptions, MetaGPT PRD/architecture docs, OpenClaw A2A artifacts).
   中文翻译：**结构化交接契约**（Anthropic 子 Agent 任务描述，MetaGPT PRD/架构文档，OpenClaw A2A 制品）。
3. **Verification as first-class role** (Anthropic's verifier, MetaGPT's QA Engineer, OpenClaw's in-network validators).
   中文翻译：**验证作为一等角色**（Anthropic 的验证器，MetaGPT 的 QA 工程师，OpenClaw 的网络内验证器）。
4. **Scaling is topology + substrate, not just more agents** (rainbow deploys, MacNet DAGs, population-scale substrates).
   中文翻译：**扩展是拓扑 + 基底，不仅是更多 Agent**（彩虹部署，MacNet DAG，群体规模基底）。
5. **Cost is material and disclosed** (15x tokens, per-role budget in MetaGPT, per-interaction pricing in Moltbook).
   中文翻译：**成本是实质性的且已披露**（15 倍 token，MetaGPT 中每角色预算，Moltbook 中每次交互定价）。
6. **Security posture is explicit** (Anthropic's sandboxing, MetaGPT's role restrictions, OpenClaw's prompt-injection as known attack surface).
   中文翻译：**安全态势是显式的**（Anthropic 的沙盒，MetaGPT 的角色限制，OpenClaw 的提示注入作为已知攻击面）。

### Choosing a reference for your next project

- **Production research / knowledge task → Anthropic Research.** Fresh-context subagents win.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.** Roles + SOPs + handoff contracts.
- **Network-effect social product → OpenClaw / Moltbook.** Substrate + emergent economy.
- **Classic enterprise automation → CrewAI or LangGraph** (production leader, stable runtime).

### The 2026 state-of-the-art summary

Where the field is in April 2026:

- **Frameworks are converging.** MCP + A2A support is table stakes. Handoff semantics are the remaining design choice.
- **Evaluation is hardening.** SWE-bench Pro, MARBLE, STRATUS mitigation benchmarks. Pro is the current contamination-resistant reality check.
- **Production failure rates are measurable** (Cemri 2025 MAST; 41-86.7% on real MAS). The field is out of the "looks great in demo" era.
- **Cost is the central engineering constraint.** Token cost per task, wall-clock per interaction, rainbow-deploy overhead. Multi-agent wins on accuracy but loses on cost — and that trade is the business decision.
- **Regulation is a near-term input, not a background concern.** Jurisdictions are moving faster than individual deploy cycles.

## Use It | 使用方法

`outputs/skill-case-study-mapper.md` is a skill that reads a proposed multi-agent system design and maps it to the closest case study, surfacing the design decisions that case study already tested.

## Ship It | 部署上线

Starter rules for production multi-agent in 2026:

- **Start from a case study, not from scratch.** Pick the closest of Anthropic Research / MetaGPT / OpenClaw and adapt.
  中文翻译：**从案例研究开始，不是从零开始。** 选择最接近的 Anthropic Research / MetaGPT / OpenClaw 并适配。
- **Adopt MCP + A2A.** Portability across frameworks is valuable; protocol support is free.
  中文翻译：**采用 MCP + A2A。** 跨框架的可移植性有价值；协议支持是免费的。
- **Measure against SWE-bench Pro or your internal Pro-equivalent.** Verified is contaminated.
  中文翻译：**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。** Verified 已被污染。
- **Pay the verification tax.** An independent verifier costs ~20-30% of your token budget and buys measurable correctness.
  中文翻译：**支付验证税。** 独立验证器花费约 20-30% 的 token 预算，换取可测量的正确性。
- **Rainbow deploy long-running agents.** Expect multi-hour agent runs to be routine.
  中文翻译：**彩虹部署长时间运行 Agent。** 预期多小时 Agent 运行是常规。
- **Read WMAC 2026 and the MAST follow-ups.** The discipline is moving fast.
  中文翻译：**阅读 WMAC 2026 和 MAST 后续。** 这个学科在快速发展。

## Exercises | 练习题

1. Read the Anthropic Research system post end-to-end. Identify three design decisions that would change if you replaced Opus 4 with a smaller model (e.g., Haiku 4).
2. Read MetaGPT Sections 3-4 (arXiv:2308.00352). Encode one SOP from your own domain (not software) as role prompts. How many roles does the SOP imply?
3. Read ChatDev (arXiv:2307.07924). Identify the mechanism of "communicative dehallucination." Implement it in one of your existing multi-agent systems.
4. Read about OpenClaw and Moltbook. Pick one specific failure mode that emerged at population scale that would not appear in a 5-agent system. How would you engineer against it?
5. Pick your current multi-agent project. Which of the three case studies is the closest reference? Which design decisions from that case study have you NOT yet adopted? Write down one you will adopt this quarter.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## Further Reading | 延伸阅读

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — the supervisor-worker production reference
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) — SOP-role decomposition
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) — communicative dehallucination
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) — DAG-based scale
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — ecosystem overview
- [WMAC 2026](https://multiagents.org/2026/) — AAAI 2026 Bridge Program Workshop on Multi-Agent Coordination
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — production leader
- [CrewAI docs](https://docs.crewai.com/en/introduction) — role-based framework
