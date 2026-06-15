# Shared Memory and Blackboard Patterns | 黑板 模式 记忆 共享

> Two approaches coexist in 2026 multi-agent systems: the **message pool** (everyone sees everyone's messages, as in AutoGen GroupChat or MetaGPT) and the **blackboard with subscription** (agents subscribe to relevant events, as in Context-Aware MCP or the Matrix framework). Both are the only stateful part of a multi-agent system — which means both are where the interesting bugs live. The reference failure mode is **memory poisoning**: one agent hallucinates a "fact," other agents treat it as verified, and accuracy decays gradually in a way that is much harder to debug than an immediate crash. This lesson builds both structures from stdlib, injects a poisoning attack, and shows the three mitigations that actually work in production.

> **【中文解读】** 本节介绍了共享记忆和黑板系统——多 Agent 系统中的共享知识库和协调机制。

> **【拓展：shared memory blackboard→具体应用】** 共享记忆/黑板模型是多 Agent 系统的经典协调机制——所有 Agent 读写一个共享的知识库。黑板模型源自 1980 年代的 Hearsay-II 语音识别系统。现代实现包括 Redis 共享状态、向量数据库和 MCP Resources。优势是简单，劣势是竞态条件（多个 Agent 同时写入）。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Multi-agent systems need a place for agents to share facts. A literal option is "pass everything in messages" — but that reinvents shared state with extra copying. Another is "give everyone a global log" — but global logs grow unbounded and poison easily. A third is "project a view per agent" — scalable but schema-heavy.

> 多 Agent 系统需要一个地方让 Agent 共享事实。一个字面选项是"在消息中传递所有东西"——但这等于重新发明带额外复制的共享状态。另一个是"给每个人一个全局日志"——但全局日志无限增长且容易被污染。第三个是"为每个 Agent 投射一个视图"——可扩展但需要大量模式设计。

The three options trace a classic distributed-systems tradeoff: cheap-but-fragile (messages), simple-but-unscalable (global log), scalable-but-rigid (per-agent projections). No option dominates. Real systems mix: a small global pool for planning, projected views for workers.

> 三个选项追溯经典分布式系统权衡：廉价但脆弱（消息）、简单但不可扩展（全局日志）、可扩展但僵化（每 Agent 投影）。没有选项占主导。真实系统混合：用于规划的小全局池、用于工作器的投影视图。

When one of the agents hallucinates and writes the hallucination to shared state, every downstream agent that reads that state adopts the hallucination as fact. By the time the human notices, the reasoning chain is five steps deep and the root cause is the third message ever written. Debugging multi-agent accuracy decay is harder than debugging a crash.

> 当其中一个 Agent 幻觉并将幻觉写入共享状态时，每个读取该状态的下游 Agent 都会将幻觉作为事实采纳。当人类注意到时，推理链已经有五步深，而根本原因是第三条消息。调试多 Agent 准确性衰减比调试崩溃更难。

A crash gives you a stack trace. Memory poisoning gives you a confidently wrong report. The first is detectable in seconds; the second may take days of forensic work to trace back to the originating hallucination.

> 崩溃给你堆栈跟踪。内存污染给你自信错误的报告。第一个几秒钟可检测；第二个可能需要几天的取证工作才能追溯到原始幻觉。

This is memory poisoning. It is the second-most-documented failure family in the MAST taxonomy (Cemri et al., arXiv:2503.13657) and it is structural: any shared-memory design without provenance and an unwritable verifier will exhibit it eventually.

> 这就是内存污染。它是 MAST 分类法中第二大记录在案的失败家族（Cemri 等人，arXiv:2503.13657），而且是结构性的：任何没有来源追溯和不可写验证器的共享内存设计最终都会出现这个问题。

## Concept | 核心概念

### The two main topologies

**Full message pool.** Every agent reads every message. AutoGen GroupChat and MetaGPT use this. Simple, transparent, inspectable, but does not scale past ~10 agents because each agent's context fills with other agents' work.

> **完整消息池。** 每个 Agent 读取每条消息。AutoGen GroupChat 和 MetaGPT 使用这种方式。简单、透明、可检查，但不能扩展到约 10 个 Agent 以上，因为每个 Agent 的上下文会填满其他 Agent 的工作。

**Blackboard with subscription.** Agents declare interest in topics; the substrate routes only relevant messages. CA-MCP (arXiv:2601.11595) and the Matrix decentralized framework (arXiv:2511.21686) use this. Scales further, but requires upfront schema design to make subscriptions meaningful.

> **带订阅的黑板。** Agent 声明对主题的兴趣；底层只路由相关消息。CA-MCP（arXiv:2601.11595）和 Matrix 去中心化框架（arXiv:2511.21686）使用这种方式。扩展性更好，但需要前期模式设计使订阅有意义。

### When each wins

- **Full pool** wins when agents are few (< 10), heterogeneous, and the conversation is short-horizon. Reasoning about who said what is trivial when everyone sees everything.
  中文翻译：**完整池** 在 Agent 少（< 10）、异构且对话短时时胜出。当每个人看到一切时，推理谁说了什么是简单的。
- **Blackboard** wins when agents are many, homogeneous in role but numerous in instance (swarms), and the conversation is long-running. Routing saves token cost and context pollution.
  中文翻译：**黑板** 在 Agent 很多、角色同质但实例众多（群体）、对话长时间运行时胜出。路由节省 token 成本和上下文污染。

Production systems often mix: a small full pool at the top (planning layer), blackboards below (worker layer).

> 生产系统通常混合使用：顶部一个小的完整池（规划层），下面是黑板（工作器层）。

This hybrid is what Anthropic's Research system does: a supervisor (full pool among a few lead agents) delegates to subagents (each its own scoped context, isolated from siblings). The top needs full transparency for synthesis; the workers need isolation for focus.

> 这种混合是 Anthropic 研究系统所做的：监督者（少数主导 Agent 之间的完整池）委派给子 Agent（每个有自己的范围上下文，与同级隔离）。顶部需要完全透明以进行综合；工作器需要隔离以专注。

### Memory poisoning, in one scenario

Three agents work on a research task. Agent A is a retrieval agent. Agent B is a summarizer. Agent C is an analyst.

> 三个 Agent 处理一个研究任务。Agent A 是检索 Agent。Agent B 是摘要器。Agent C 是分析师。

1. A fetches a page and writes a message to shared state: "The study reports a 42% accuracy improvement."
   中文翻译：A 获取一个页面并向共享状态写入消息："研究报告了 42% 的准确率提升。"
2. The fetched page actually said "4.2% improvement." A hallucinated a decimal.
   中文翻译：获取的页面实际上说的是"4.2% 提升。"A 幻觉了一个小数点。
3. B, reading shared state, writes: "Large 42% accuracy gain reported (source: A)."
   中文翻译：B 读取共享状态，写入："报告了大幅 42% 准确率提升（来源：A）。"
4. C, reading shared state, writes: "Recommend adoption — 42% lift is transformative."
   中文翻译：C 读取共享状态，写入："建议采纳——42% 的提升是变革性的。"
5. The final report cites a 42% number that never existed.
   中文翻译：最终报告引用了一个从未存在的 42% 数字。

No agent crashed. No test failed. The system "worked." The hallucination crossed from one agent's context into every downstream agent's reasoning via shared state.

> 没有 Agent 崩溃。没有测试失败。系统"工作"了。幻觉通过共享状态从一个 Agent 的上下文进入了每个下游 Agent 的推理。

This is why memory poisoning is insidious: there is no crash, no error, no warning. The system produces a confidently wrong report. The only way to detect it is to re-derive each fact from primary sources — which defeats the point of having agents.

> 这就是为什么内存污染阴险：没有崩溃、没有错误、没有警告。系统产生自信错误的报告。检测它的唯一方法是从原始来源重新推导每个事实——这违背了拥有 Agent 的意义。

### Why this is structural

Without shared state, agent A's hallucination stays in A's context. Downstream agents would re-fetch or re-derive and might catch the error. With naive shared state, A's context becomes everyone's context, and the hallucination is laundered into fact.

> 没有共享状态，Agent A 的幻觉停留在 A 的上下文中。下游 Agent 会重新获取或重新推导并可能捕获错误。有了朴素的共享状态，A 的上下文变成了每个人的上下文，幻觉被洗白为事实。

The problem is not shared state per se — it is shared state **without provenance and without an independent verifier**. Three mitigations address this:

> 问题不是共享状态本身——而是**没有来源追溯和没有独立验证器**的共享状态。三种缓解措施解决这个问题：

Each mitigation targets a different failure mode. Provenance lets you trace errors back. Versioning preserves the audit trail. The unwritable verifier provides an independent check. Together, they form defense in depth against poisoning.

> 每种缓解措施针对不同失败模式。来源追溯让你追溯错误。版本控制保留审计跟踪。不可写验证器提供独立检查。它们共同形成针对污染的纵深防御。

1. **Attribute provenance on every write.** Every entry in shared state records who wrote it, when, under what prompt, and (if applicable) what source the agent cited. Downstream agents read with skepticism keyed to provenance.
   中文翻译：**每次写入时归属来源。** 共享状态中的每个条目记录谁写的、何时、在什么提示下、以及（如果适用）Agent 引用了什么来源。下游 Agent 根据来源以怀疑态度阅读。
2. **Version writes; treat them as append-only.** A correction is a new entry that supersedes the old, not an in-place update. The audit trail is preserved.
   中文翻译：**版本化写入；视为仅追加。** 修正是一个取代旧条目的新条目，不是原地更新。审计跟踪被保留。
3. **Keep at least one agent that cannot write to shared state.** A read-only verifier agent samples entries, re-fetches sources, and flags inconsistencies. Because it cannot write to the pool, it cannot be poisoned by the pool.
   中文翻译：**保留至少一个不能写入共享状态的 Agent。** 只读验证器 Agent 采样条目、重新获取来源并标记不一致。因为它不能写入池，所以不能被池污染。

### Blackboard precedent (Hayes-Roth, 1985)

The blackboard pattern predates LLM agents by four decades. Hayes-Roth (1985, "A Blackboard Architecture for Control") described specialist Knowledge Sources that observe a global blackboard, contribute partial solutions, and trigger other sources. The 2026 blackboard (CA-MCP, Matrix) is the same pattern with LLM agents as Knowledge Sources and JSON blobs as partial solutions. The old literature has documented solutions to write contention, opportunistic control, and consistency that modern systems rediscover.

> 黑板模式比 LLM Agent 早了四十年。Hayes-Roth（1985，"A Blackboard Architecture for Control"）描述了观察全局黑板、贡献部分解决方案并触发其他来源的专业知识源。2026 年的黑板（CA-MCP、Matrix）是相同的模式，只是以 LLM Agent 作为知识源、以 JSON blob 作为部分解决方案。旧文献中记录的写冲突、机会控制和一致性解决方案正被现代系统重新发现。

The lesson from Hearsay-II (the 1970s speech recognition blackboard): opportunistic control — letting any Knowledge Source trigger when its trigger condition matches — produces emergent problem-solving. Modern agent systems that hard-code workflow graphs lose this. The blackboard's flexibility is its core innovation.

> Hearsay-II（1970 年代语音识别黑板）的教训：机会控制——让任何知识源在其触发条件匹配时触发——产生涌现问题解决。硬编码工作流图的现代 Agent 系统失去了这一点。黑板的灵活性是其核心创新。

### Projection vs full view

A pure blackboard gives every subscriber the same projection (topic-scoped). A more aggressive design is **per-agent projection**: each agent gets a view customized to its role. LangGraph's state reducers are the canonical 2026 implementation — the reducer function folds global state into a role-specific slice.

> 纯黑板给每个订阅者相同的投影（主题范围）。更激进的设计是**每个 Agent 投影**：每个 Agent 获得根据其角色定制的视图。LangGraph 的状态归约器是 2026 年的典型实现——归约器函数将全局状态折叠为角色特定的切片。

Per-agent projection scales further but needs a schema. Without one, you rebuild ad-hoc projection in every agent's prompt.

> 每个 Agent 投影扩展性更好但需要模式。没有模式，你在每个 Agent 的提示中重建临时投影。

### Write-contention patterns

Multiple agents writing simultaneously is a concurrency problem, not just an LLM problem. Three patterns work:

> 多个 Agent 同时写入是一个并发问题，不仅仅是 LLM 问题。三种模式有效：

- **Sequential writer (single producer).** All writes go through one coordinator agent that serializes. Simple, but a bottleneck.
  中文翻译：**顺序写入者（单一生产者）。** 所有写入通过一个协调 Agent 串行化。简单，但是瓶颈。
- **Optimistic concurrency with versioning.** Each entry has a version; writers fail on version mismatch and retry. Classic database technique.
  中文翻译：**带版本控制的乐观并发。** 每个条目有版本；写入者在版本不匹配时失败并重试。经典数据库技术。
- **Topic partitioning.** Different agents own different topics. No cross-topic contention. Requires designed partition boundaries.
  中文翻译：**主题分区。** 不同 Agent 拥有不同主题。没有跨主题冲突。需要设计的分区边界。

Most 2026 frameworks default to sequential writer because LLM calls are slow enough that contention is rare and the bottleneck does not hurt.

> 大多数 2026 框架默认使用顺序写入者，因为 LLM 调用足够慢，冲突很少，瓶颈不影响.

When you do hit contention (high-throughput swarm, parallel research agents writing findings), topic partitioning is usually the cheapest fix. Give each agent its own topic; merges happen at synthesis time.

> 当你确实遇到冲突（高吞吐量群体、并行研究 Agent 写入发现）时，主题分区通常是最廉价的修复。给每个 Agent 自己的主题；合并在综合时发生。

### The unwritable verifier

The most load-bearing mitigation is the read-only verifier. Implementation rules:

> 最重要的缓解措施是只读验证器。实现规则：

- Verifier shares state with the team (reads the blackboard or pool).
  中文翻译：验证者与团队共享状态（读取黑板或池）。
- Verifier has no write handle to shared state — only to a separate verification channel.
  中文翻译：验证者没有对共享状态的写入句柄——只有一个单独的验证通道。
- Verifier independently fetches sources cited in writes. Flags disagreement.
  中文翻译：验证者独立获取写入中引用的来源。标记不一致。
- Verifier's own outputs are routed to a human or a separate decision agent, never fed back into the pool.
  中文翻译：验证者自己的输出路由到人类或单独的决策 Agent，永远不回馈到池中。

Without this separation, the verifier's outputs become new entries in the pool, which means a poisoned pool poisons the verifier, which poisons its verifications.

> 没有这种分离，验证者的输出变成池中的新条目，这意味着被污染的池污染了验证者，进而污染了它的验证。

This is the unwritable-verifier principle: the auditor must be read-only with respect to the system being audited. Compromise the auditor and you compromise the audit. The principle applies to any verification role — keep its outputs separate from the system it checks.

> 这是不可写验证者原则：审计者必须对被审计系统只读。攻陷审计者就攻陷了审计。该原则适用于任何验证角色——保持其输出与它检查的系统分离。

## Build It | 动手实现

`code/main.py` implements both topologies in stdlib Python plus a toy poisoning attack and the three mitigations.

> `code/main.py` 用标准库 Python 实现了两种拓扑以及一个玩具污染攻击和三种缓解措施。

- `MessagePool` — thread-safe append-only log with full read-out.
  中文翻译：`MessagePool` — 线程安全的仅追加日志，支持完整读取。
- `Blackboard` — topic-keyed pub/sub with per-agent subscriptions.
  中文翻译：`Blackboard` — 基于主题的发布/订阅，支持每个 Agent 的订阅。
- `ProvenanceEntry` — every write records (writer, timestamp, prompt_hash, source_uri).
  中文翻译：`ProvenanceEntry` — 每次写入记录（写入者、时间戳、prompt_hash、source_uri）。
- `PoisoningScenario` — runs a three-agent research task where agent A hallucinates a decimal. Prints final report.
  中文翻译：`PoisoningScenario` — 运行三 Agent 研究任务，其中 Agent A 幻觉一个小数点。打印最终报告。
- `Verifier` — a read-only agent that re-fetches sources and flags inconsistencies. Runs the same scenario with the verifier present.
  中文翻译：`Verifier` — 一个重新获取来源并标记不一致的只读 Agent。在验证者存在的情况下运行相同场景。

Expected output:
- Run 1 (no verifier): the hallucinated 42% propagates to the final report.
  中文翻译：运行 1（无验证者）：幻觉的 42% 传播到最终报告。
- Run 2 (with verifier): the verifier flags the inconsistency, the pool is labeled "flagged", the final report includes a retraction.
  中文翻译：运行 2（有验证者）：验证者标记不一致，池被标记为"已标记"，最终报告包含撤回。

## Use It | 用框架实现

`outputs/skill-memory-auditor.md` is a skill that audits any multi-agent system's shared-memory design for provenance, versioning, and verifier separation. Run it on new multi-agent architectures before production.

> `outputs/skill-memory-auditor.md` 是一个技能，审计任何多 Agent 系统的共享内存设计中的来源追溯、版本控制和验证者分离。在生产前对新多 Agent 架构运行它。

## Ship It | 产出物

For any shared-memory design:

> 对于任何共享内存设计：

- Record provenance on every write: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`.
  中文翻译：每次写入时记录来源：`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`。
- Make the log append-only. Corrections are new entries that reference the superseded one.
  中文翻译：使日志仅追加。修正项是引用被取代项的新条目。
- Deploy at least one read-only verifier agent with independent source access.
  中文翻译：部署至少一个具有独立来源访问的只读验证者 Agent。
- Route verifier output to a separate channel, not back into the shared pool.
  中文翻译：将验证者输出路由到单独的通道，而不是回馈到共享池。
- Log the ratio of writes that are supersessions — a rising ratio is early evidence of hallucination patterns.
  中文翻译：记录覆盖写入的比例——上升的比例是幻觉模式的早期证据。

## Exercises | 练习题

1. Run `code/main.py`. Confirm run 1 propagates the hallucination and run 2 catches it.
   中文翻译：运行 `code/main.py`。确认运行 1 传播幻觉且运行 2 捕获了它。
2. Add a second hallucination: agent B invents a dataset size. The verifier should catch both without being hand-tuned for either.
   中文翻译：添加第二个幻觉：Agent B 虚构一个数据集大小。验证者应该捕获两者而无需针对任何一个手动调优。
3. Switch the full pool to a blackboard with topic partitions (`prices`, `summaries`, `analyses`). Which poisoning scenarios does topic partitioning make harder to pull off, and which does it not help with?
   中文翻译：将完整池切换为带主题分区的黑板（`prices`、`summaries`、`analyses`）。主题分区使哪些投毒场景更难实施，哪些没有帮助？
4. Read Hayes-Roth (1985, "A Blackboard Architecture for Control"). Identify two control patterns from the paper not discussed in this lesson that 2026 systems would benefit from.
   中文翻译：阅读 Hayes-Roth（1985，"A Blackboard Architecture for Control"）。识别论文中两个本课未讨论的 2026 年系统会受益的控制模式。
5. Read CA-MCP (arXiv:2601.11595). Map its Shared Context Store to either the MessagePool or Blackboard class in `code/main.py`. Which primitives does CA-MCP add on top?
   中文翻译：阅读 CA-MCP（arXiv:2601.11595）。将其共享上下文存储映射到 `code/main.py` 中的 MessagePool 或 Blackboard 类。CA-MCP 在其之上添加了哪些原语？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Further Reading | 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) — MAST taxonomy; memory poisoning is a coordination-failure sub-family
  中文翻译：Cemri 等人 — 为什么多 Agent LLM 系统会失败？— MAST 分类法；内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) — Shared Context Store for coordinated MCP servers
  中文翻译：CA-MCP — 上下文感知多服务器 MCP — 协调 MCP 服务器的共享上下文存储
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) — message-queue-based blackboard without a central orchestrator
  中文翻译：Matrix — 去中心化多 Agent 框架 — 基于消息队列的黑板，无中央编排器
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — the per-agent projection pattern in production
  中文翻译：LangGraph 状态和归约器 — 生产中的每个 Agent 投影模式
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — provenance and verification notes from a production deployment
  中文翻译：Anthropic — 我们如何构建多 Agent 研究系统 — 来自生产部署的来源追溯和验证笔记
