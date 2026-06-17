# Generative Agents and Emergent Simulation | 生成式 Agent 模拟

> Park et al. 2023 (UIST '23, arXiv:2304.03442) populated **Smallville**, a sandbox of 25 agents, with a three-part architecture: **memory stream** (natural-language log), **reflection** (higher-level syntheses the agent generates about its own stream), and **plan** (day-level behavior, then sub-plans). The landmark result was the Valentine's Day party emergence: one agent seeded with "wants to throw a Valentine's Day party," without further scripting, produced invitations spread through the population, coordinated dates, and the party happened — from 24 agents who started with no knowledge of it. Ablations show all three components are required for believability. The documented failures are spatial-norm errors (entering closed stores, sharing single-person bathrooms). This is the reference architecture for agent simulations and multi-agent social evaluation in 2026.

> **【中文解读】** 本节介绍了生成式 Agent 模拟——斯坦福的 AI 小镇实验，25 个 AI Agent 在虚拟社区中自主生活。

> **【拓展：generative agents simulation→具体应用】** 斯坦福的生成式 Agent 实验（Park et al., 2023）创建了 25 个 AI Agent 在虚拟小镇中自主生活——每天起床、上班、社交、形成关系和记忆。核心创新是记忆流架构——每个 Agent 维护按时间排序的经历序列，通过反思和总结提取高层洞察。这个实验证明了 LLM Agent 能产生涌现性的社会行为。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·04（原语）、Phase 16·13（共享内存）、Phase 11·04（Embeddings，记忆流检索用）。Stanford Smallville = 多 Agent 涌现社会行为的里程碑实验。
> 💡 **【类比】** Smallville = "AI 版模拟人生"。25 个 AI 居民各有人生、记忆、计划。情人节派对奇迹：一个 Agent 想办派对→邀请传开→其他人调整日程→派对真发生——全是涌现，无脚本。三件套：memory stream（经历日志）+ reflection（自我总结）+ plan（日计划）。三者缺一不可，去掉任一 Agent 行为变得不可信。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Most multi-agent systems are tightly-scripted teams: planner plans, coder codes, reviewer reviews. That works for well-defined tasks. It does not capture the emergent, unscripted behavior that arises when agents have memory, priorities, and an open world. Research, society simulation, and increasingly game AI need this second kind.

> 大多数多 Agent 系统是紧密脚本的团队：规划者规划、编码者编码、评审者评审。这对定义明确的任务有效。但它不能捕捉当 Agent 拥有记忆、优先级和开放世界时涌现的、非脚本的行为。研究、社会模拟和越来越多的游戏 AI 需要第二种。

The Smallville architecture is the benchmark for it. Until Park 2023, the best agent simulations were shallow script-followers; after it, the pattern is the default for generative agents in open worlds. If you build an agent simulation in 2026, you are either using Smallville's three components or explicitly justifying why you are not.

> Smallville 架构是这一类的基准。在 Park 2023 之前，最好的 Agent 模拟是浅层的脚本跟随者；之后，这种模式成为开放世界中生成式 Agent 的默认。如果你在 2026 年构建 Agent 模拟，你要么使用 Smallville 的三个组件，要么明确解释为什么不使用。

## Concept | 核心概念

### The three components

**Memory stream.** An append-only log of observations, actions, reflections, and plans. Each entry has a timestamp, a type, a description (natural language), and derived metadata: **recency**, **importance** (self-rated 1-10 by the agent), and **relevance** (cosine similarity to current query).

> **记忆流。** 一个只追加的观察、行动、反思和计划日志。每个条目有时间戳、类型、描述（自然语言）和派生元数据：**时效性**、**重要性**（Agent 自评 1-10）和**相关性**（与当前查询的余弦相似度）。

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

Memory retrieval combines the three scores: `score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`. Top-k entries enter the current prompt.

**Reflection.** Periodically (every N memories or on important events), the agent generates higher-order syntheses from recent memories. Reflection entries go back into the stream and are retrievable like any other memory. This is how agents build "understandings" — the architecture's equivalent of long-term beliefs.

> **反思。** 定期（每 N 条记忆或在重要事件时），Agent 从最近的记忆中生成高阶综合。反思条目回到流中，像其他记忆一样可检索。这是 Agent 建立"理解"的方式——架构中等同于长期信念。

**Plan.** Top-down decomposition. First, a day-level plan in broad strokes ("go to work, have dinner with Klaus"). Then hour-level plans. Then action-level plans. Plans are revisable: when an observation contradicts a plan, the agent replans the affected segment.

> **计划。** 自顶向下分解。首先，粗略的日级计划（"上班，和 Klaus 共进晚餐"）。然后是小时级计划。然后是动作级计划。计划是可修订的：当观察与计划矛盾时，Agent 重新规划受影响的部分。

### Why all three matter (ablation)

Park et al. ran ablations dropping each of observation, reflection, and plan. Each ablation hurts believability:

> Park 等人进行了消融实验，分别去掉观察、反思和计划。每个消融都损害可信度：

- Without **observation** the agent misses context and acts on stale beliefs.
  中文翻译：没有**观察**，Agent 缺失上下文，基于过时信念行动。
- Without **reflection** the agent cannot form higher-order beliefs; interactions stay shallow.
  中文翻译：没有**反思**，Agent 无法形成高阶信念；交互保持浅层。
- Without **plan** behavior becomes reactive noise; goals dissipate.
  中文翻译：没有**计划**，行为变成反应性噪声；目标消散。

Believability scores from human raters are highest with all three; dropping any one produces a measurable regression.

> 人类评分者的可信度分数在三者齐全时最高；去掉任何一个产生可测量的退化。

### The Valentine's Day emergence

One agent, Isabella Rodriguez, is seeded with the goal "wants to throw a Valentine's Day party at Hobbs Cafe on Feb 14 at 5pm." The 24 other agents receive no such seed. Over simulated days:

> 一个 Agent，Isabella Rodriguez，被植入目标"想在 2 月 14 日下午 5 点在 Hobbs Cafe 举办情人节派对"。其他 24 个 Agent 没有收到这样的种子。在模拟的几天里：

1. Isabella's plan includes inviting people.
   中文翻译：Isabella 的计划包括邀请人们。
2. Each invitation becomes an observation in a neighbor's memory stream.
   中文翻译：每个邀请成为邻居记忆流中的一个观察。
3. That neighbor's reflection generates beliefs: "Isabella is throwing a party."
   中文翻译：邻居的反思产生信念："Isabella 要办派对。"
4. The neighbor's plan incorporates "attend party on Feb 14."
   中文翻译：邻居的计划纳入"2 月 14 日参加派对"。
5. Neighbors tell other neighbors. The invitation spreads without central coordination.
   中文翻译：邻居告诉其他邻居。邀请在没有中央协调的情况下传播。
6. At 5pm on Feb 14, several agents converge at Hobbs Cafe.
   中文翻译：2 月 14 日下午 5 点，几个 Agent 汇聚到 Hobbs Cafe。

This is emergence in the technical sense: system-level behavior (a party) arose from local interactions (bilateral invitations + individual planning) without a central orchestrator.

> 这是技术意义上的涌现：系统级行为（派对）从局部交互（双边邀请 + 个体规划）中产生，没有中央编排者。

### The documented failure modes

Park et al. explicitly document:

> Park 等人明确记录了：

- **Spatial norm errors.** Agents walk into closed stores. Agents try to use the same single-person bathroom. Agents eat in rooms not intended for eating. The model does not infer social-physical norms from the environment alone.
  中文翻译：**空间规范错误。** Agent 走进关闭的商店。Agent 试图使用同一个单人浴室。Agent 在非用餐房间用餐。模型无法仅从环境推断社会-物理规范。
- **Memory overflow.** Deep simulation runs cause memory-retrieval cost to grow. Practical remedy: periodic memory compaction (summarize-and-prune) and decay on low-importance entries.
  中文翻译：**记忆溢出。** 深度模拟运行导致记忆检索成本增长。实际补救：定期记忆压缩（摘要和修剪）和低重要性条目的衰减。
- **Reflection hallucination.** Reflections can invent relationships that do not exist in the memory stream. Mitigation: include source memory ids in reflection prompts and verify at retrieval time.
  中文翻译：**反思幻觉。** 反思可能发明记忆流中不存在的关系。缓解：在反思提示中包含来源记忆 ID 并在检索时验证。

These are production-relevant failure modes: any 2026 agent simulation inherits them.

> 这些是与生产相关的失败模式：任何 2026 年的 Agent 模拟都会继承它们。

### Three-component implementation rules

1. **Memory is append-only.** Never mutate a memory entry. Corrections are new entries.
   中文翻译：**记忆只追加。** 永远不修改记忆条目。更正是新条目。
2. **Importance scores are cheap.** Call the LLM to rate importance 1-10 at write time. Cache the score.
   中文翻译：**重要性分数是廉价的。** 写入时调用 LLM 评分 1-10。缓存分数。
3. **Retrieval is ranked, not filtered.** Top-k by combined score; do not use hard filters (which lose context).
   中文翻译：**检索是排序的，不是过滤的。** 按综合分数取 top-k；不要使用硬过滤（会丢失上下文）。
4. **Reflection runs periodically.** Trigger when the sum of importance of unprocessed memories exceeds a threshold (e.g., 150).
   中文翻译：**反思定期运行。** 当未处理记忆的重要性总和超过阈值（例如 150）时触发。
5. **Plans are revisable.** When a new observation contradicts a plan, regenerate the affected segment only, not the whole plan.
   中文翻译：**计划可修订。** 当新观察与计划矛盾时，只重新生成受影响的部分，不是整个计划。

### Generative agents beyond Smallville

The 2024-2026 follow-up literature extends the architecture:

> 2024-2026 年的后续文献扩展了该架构：

- **Multi-agent social simulation for policy / market research.** Smallville-like populations simulate user behavior in response to features. Faster than A/B tests; accuracy is contested.
  中文翻译：**用于政策/市场研究的多 Agent 社会模拟。** 类似 Smallville 的人群模拟用户对功能的响应。比 A/B 测试更快；准确性有争议。
- **NPC AI for games.** RPGs with Smallville agents produce emergent storylines instead of scripted quests.
  中文翻译：**游戏 NPC AI。** 带有 Smallville Agent 的 RPG 产生涌现的故事线而非脚本化的任务。
- **Generative-agent evaluation benchmarks.** Rather than task accuracy, the metric becomes believability + coherence of behavior over long runs.
  中文翻译：**生成式 Agent 评估基准。** 而非任务准确率，指标变为长时间运行的可信度 + 行为连贯性。

The architecture is the reference. Extensions swap components (vector store for memory, retrieval-augmented reflection, neurosymbolic plan) but keep the three-part structure.

> 该架构是参考。扩展替换组件（记忆的向量存储、检索增强反思、神经符号计划）但保持三部分结构。

### Why this matters for multi-agent engineering

Smallville is the proof of concept that multi-agent emergence is cheap when the components are right. The architecture has now been replicated on open-source models (smaller LLMs lose believability gracefully, not sharply). Any production system that needs **emergent social behavior** uses this shape. Any system that needs **tight task execution** uses the supervisor / roles / primitives patterns from earlier in this phase.

> Smallville 是概念验证，表明当组件正确时，多 Agent 涌现是廉价的。该架构已在开源模型上复现（较小的 LLM 优雅地而非剧烈地失去可信度）。任何需要**涌现社会行为**的生产系统都使用这种形式。任何需要**紧密任务执行**的系统都使用本阶段早期的监督者/角色/原语模式。

## Build It | 动手构建

`code/main.py` implements the three components in stdlib Python with scripted agent policies (no real LLM). The demo reproduces the Valentine's-party emergence in miniature:

- `MemoryStream` — append-only log with recency/importance/relevance retrieval.
  中文翻译：`MemoryStream` — 带时效性/重要性/相关性检索的只追加日志。
- `reflect(stream)` — scripted reflection over recent high-importance memories.
  中文翻译：`reflect` — 对最近高重要性记忆的脚本化反思。
- `plan(agent_state)` — day-level and hour-level plans based on current beliefs.
  中文翻译：`plan` — 基于当前信念的日级和小时级计划。
- Scenario: 5 agents. Agent 1 starts with "throw party at 5pm." Over simulated ticks, the invitation spreads and agents converge.
  中文翻译：场景：5 个 Agent。Agent 1 以"下午 5 点办派对"开始。在模拟的时间步中，邀请传播，Agent 汇聚。

Run:

```
python3 code/main.py
```

Expected output: tick-by-tick trace. By the final tick, at least 3 of the 5 agents show the party in their plan, and they converge at the party location. The single seed produced the coordinated arrival without any orchestrator.

> 预期输出：逐步跟踪。在最后一个时间步，5 个 Agent 中至少 3 个在计划中显示派对，它们汇聚在派对地点。单个种子在没有编排者的情况下产生了协调到达。

## Use It | 使用方法

`outputs/skill-simulation-designer.md` designs a generative-agent simulation: number of agents, memory schema, reflection cadence, plan horizon, and evaluation metric.

> `outputs/skill-simulation-designer.md` 设计一个生成式 Agent 模拟：Agent 数量、记忆模式、反思频率、计划范围和评估指标。

## Ship It | 部署上线

Rules for production simulations:

- **Memory is the database.** Pick a real store (vector DB, Postgres) at scale. In-memory stdlib is for prototypes.
  中文翻译：**记忆是数据库。** 在规模上选择真正的存储（向量 DB、Postgres）。内存中的标准库只用于原型。
- **Log the retrieval trace.** For every action, log the top-k memories that drove it. This is your debug ability.
  中文翻译：**记录检索轨迹。** 对每个动作，记录驱动它的 top-k 记忆。这是你的调试能力。
- **Budget per-agent tokens.** Each agent's retrieve + reflect + plan per tick is O(k) LLM calls. N agents × T ticks × calls-per-tick can dwarf your budget.
  中文翻译：**预算每 Agent token。** 每个 Agent 每个时间步的检索 + 反思 + 计划是 O(k) 次 LLM 调用。N 个 Agent × T 个时间步 × 每时间步调用数可能让你的预算相形见绌。
- **Compact memory periodically.** Summarize-and-prune low-importance entries. Retention policy is a design decision, not a detail.
  中文翻译：**定期压缩记忆。** 摘要和修剪低重要性条目。保留策略是设计决策，不是细节。
- **Detect spatial / social norm violations** explicitly. The architecture does not learn them.
  中文翻译：**显式检测空间/社会规范违规。** 架构不会学习它们。

## Exercises | 练习题

1. Run `code/main.py`. Confirm 3+ agents converge at the party. Increase agents to 10 — does the emergence still happen?
   中文翻译：运行 `code/main.py`。确认 3 个以上 Agent 汇聚到派对。将 Agent 增加到 10——涌现还会发生吗？
2. Remove the reflection step. What does behavior look like? Map to the ablation finding in Park 2023.
   中文翻译：移除反思步骤。行为看起来如何？映射到 Park 2023 的消融发现。
3. Introduce a competing seeded goal ("Klaus wants to give a research talk at 5pm"). Do agents split, or does one goal dominate? What determines it?
   中文翻译：引入一个竞争的种子目标（"Klaus 想在下午 5 点做研究报告"）。Agent 会分裂还是一个目标主导？什么决定它？
4. Add spatial constraints: Hobbs Cafe holds at most 4 agents. Does the simulation handle overflow gracefully, or does it hit the "single-person bathroom" failure pattern?
   中文翻译：添加空间约束：Hobbs Cafe 最多容纳 4 个 Agent。模拟能优雅地处理溢出吗，还是会碰到"单人浴室"失败模式？
5. Read Park et al. (arXiv:2304.03442) Section 6 (emergent behavior experiments). Identify one behavior not reproducible in your miniature. What component of the architecture would you need to enhance?
   中文翻译：阅读 Park 等人（arXiv:2304.03442）第 6 节（涌现行为实验）。识别一个在你的微型版本中不可复现的行为。你需要增强架构的哪个组件？

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Further Reading | 延伸阅读

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — the reference architecture
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) — publication venue
- [Smallville code release](https://github.com/joonspk-research/generative_agents) — reference Python implementation
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) — prior art for structured-memory agents
