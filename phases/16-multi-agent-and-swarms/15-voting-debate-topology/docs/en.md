# Voting, Self-Consistency, and Debate Topology | 拓扑 辩论 投票

> The cheapest aggregation: sample N independent agents, majority-vote. Wang et al. 2022 self-consistency did this with one model sampled N times. Multi-agent extends it with **heterogeneous** agents to escape monoculture — different models, different prompts, different temperatures, different contexts. Beyond majority vote, debate topology matters: MultiAgentBench (arXiv:2503.01935, ACL 2025) evaluated star / chain / tree / graph coordination and found **graph best for research**, with a "coordination tax" past ~4 agents. AgentVerse (ICLR 2024) documents two emergent patterns — volunteer behaviors and conformity behaviors — and conformity is both a feature (finding consensus) and a risk (groupthink, Lesson 24). This lesson maps the topology space, builds each variant, and measures the coordination tax.

> **【中文解读】** 本节介绍了投票和辩论拓扑——多 Agent 通过投票或辩论来决策的组织结构。

> **【拓展：voting debate topology→具体应用】** 投票和辩论拓扑定义了多 Agent 决策的结构。三种常见拓扑：(1) 星形——所有 Agent 独立投票，中心聚合；(2) 链形——Agent 依次修改前一个 Agent 的输出；(3) 图形——Agent 形成讨论网络，多轮交互。研究表明，图形拓扑在复杂推理任务上效果最好，但协调成本最高。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·07（辩论）、Phase 16·14（BFT 共识）、Phase 13·03（Self-Consistency CoT）。投票拓扑 = 多 Agent 决策的几何形状。
> 💡 **【类比】** 投票拓扑 = "会议桌摆放方式"。星形 = 圆桌投票（独立）；链形 = 接力修改（前面 Agent 的输出传给下一个）；图形 = 圆桌讨论（多轮交互）。MultiAgentBench 结论：图形适合研究任务但有"协调税"（>4 个 Agent 性价比下降）。异质性是关键——不同模型/温度/prompt 防单一文化错误。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Debate can improve accuracy (Du et al., arXiv:2305.14325). It can also degrade it. Whether debate helps depends on four structural choices:

> 辩论可以提高准确性（Du 等人，arXiv:2305.14325），也可能降低准确性。辩论是否有帮助取决于四个结构性选择：

1. Who talks to whom (topology).
   中文翻译：谁和谁对话（拓扑）。
2. How many rounds (Du 2023: both rounds and agents matter independently).
   中文翻译：多少轮次（Du 2023：轮次和 Agent 数量都独立重要）。
3. Whether agents are heterogeneous (different base models break monoculture).
   中文翻译：Agent 是否异构（不同基础模型打破单一文化）。
4. Whether an adversarial voice is present (steel-manning vs. straw-manning).
   中文翻译：是否存在对抗性声音（钢铁侠论证 vs 稻草人论证）。

Teams that bolt "run 5 agents and vote" onto a task often regress vs. a single agent. The failures are not random. They track topology and heterogeneity. This lesson is the topology map.

> 团队将"运行 5 个 Agent 并投票"硬加到任务上，往往比单 Agent 表现更差。失败不是随机的。它们追踪拓扑和异构性。本课就是拓扑地图。

## Concept | 核心概念

### Self-consistency, the single-model baseline

Wang et al. 2022 ("Self-Consistency Improves Chain of Thought Reasoning") sampled the same model N times at temperature > 0 and majority-voted on reasoning-path answers. The result on GSM8K: substantial gains with N=40 samples over a single greedy decode. Self-consistency is the single-agent precursor to multi-agent voting.

> Wang 等人 2022 年（"自一致性改进思维链推理"）在 temperature > 0 的条件下对同一模型采样 N 次，并对推理路径答案进行多数投票。GSM8K 上的结果：N=40 次采样比单次贪心解码有显著提升。自一致性是单 Agent 投票的多 Agent 前身。

Limit: self-consistency uses one base model. Errors are correlated by construction. If the model has a systematic bias, all N samples share it.

> 局限：自一致性使用一个基础模型。错误在构造上就是相关的。如果模型有系统性偏差，所有 N 个样本都共享它。

### Multi-agent vote, the heterogeneous extension

Replace N samples with N *different* agents. Different base models (Claude, GPT, Llama), different prompts, different tool access. The benefit: uncorrelated errors. The cost: different agents cost different amounts; coordinating them adds overhead.

> 将 N 个样本替换为 N 个*不同*的 Agent。不同的基础模型（Claude、GPT、Llama），不同的提示，不同的工具访问。好处：不相关的错误。代价：不同 Agent 的成本不同；协调它们增加开销。

The canonical 2026 name for heterogeneous debate is **A-HMAD** — Adversarial Heterogeneous Multi-Agent Debate. Not universally adopted, but papers use the term for "different models debate, which reduces correlated errors from monoculture collapse."

> 2026 年异构辩论的规范名称是 **A-HMAD**——对抗性异构多 Agent 辩论。并非普遍采用，但论文用这个词指"不同模型辩论，减少单一文化崩溃的相关错误"。

### The four topologies

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Star: one hub, all others talk only to hub. Equivalent to supervisor-worker without back-channel.
Chain: linear, each agent sees the prior one's output. Pipeline-like.
Tree: hierarchical, used by hierarchical agent systems (Lesson 06).
Graph: any-to-any. Includes fully-connected clique and arbitrary DAGs.

> 星形：一个中心，所有其他 Agent 只与中心对话。相当于没有反馈通道的监督者-工作者。
> 链形：线性，每个 Agent 看到前一个 Agent 的输出。类似流水线。
> 树形：层次化，用于层次化 Agent 系统（第 06 课）。
> 图形：任意到任意。包括完全连接的团和任意 DAG。

### The coordination tax (MultiAgentBench)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) benchmarked star, chain, tree, graph on a task suite including research, coding, and planning. Key measured results:

> MultiAgentBench（MARBLE，ACL 2025，arXiv:2503.01935）在包括研究、编码和规划的任务套件上对星形、链形、树形、图形进行了基准测试。关键测量结果：

- **Graph** topology wins on research tasks. Information flows any-to-any; agents can critique each other.
  中文翻译：**图形**拓扑在研究任务上获胜。信息任意流动；Agent 可以互相批评。
- **Star** wins on fast-answer factual tasks. Hub filters and consolidates.
  中文翻译：**星形**在快速回答的事实性任务上获胜。中心过滤和整合。
- **Chain** wins on stepwise pipelines (staged refinement).
  中文翻译：**链形**在逐步流水线（分阶段改进）上获胜。
- **Coordination tax** appears past ~4 agents in graph topology. Wall-clock and token cost grow faster than quality.
  中文翻译：**协调税**在图形拓扑约 4 个 Agent 后出现。挂钟时间和 token 成本增长快于质量。

The 4-agent ceiling is empirical, not fundamental. It reflects 2026 LLM context capacity: each agent's context fills with peers' outputs, and marginal value of adding agent N+1 drops once everyone can see everyone.

> 4 Agent 上限是经验性的，不是根本性的。它反映了 2026 年 LLM 上下文容量：每个 Agent 的上下文填满了同伴的输出，一旦每个人都能看到每个人，添加第 N+1 个 Agent 的边际价值就下降。

### Multi-Agent Debate Strategies ("Should we be going MAD?")

arXiv:2311.17371 is the 2023 survey of MAD strategies. Key finding replicated by others: MAD variants that are *structurally similar* to self-consistency (independent sampling + aggregation) often underperform self-consistency when using the same budget. MAD helps most when agents are genuinely heterogeneous and the debate has adversarial structure (one agent argues against).

> arXiv:2311.17371 是 2023 年 MAD 策略综述。关键发现已被他人复现：在结构上与自一致性相似的 MAD 变体（独立采样 + 聚合）在使用相同预算时往往不如自一致性。MAD 在 Agent 真正异构且辩论具有对抗结构时帮助最大。

### AgentVerse emergent patterns

AgentVerse (ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) documents two behaviors that emerge from multi-agent debate even without explicit design:

- **Volunteer.** An agent offers help ("I can take the next step") unprompted. Useful: it allocates work to the most-capable agent for a subtask.
  中文翻译：**自愿者。** Agent 主动提供帮助（"我可以进行下一步"）。有用：将工作分配给子任务最有能力的 Agent。
- **Conformity.** An agent adjusts its stance to match a critic, even when the critic is wrong. This is the debate-equivalent of sycophancy (Lesson 14).
  中文翻译：**从众。** Agent 调整立场以匹配批评者，即使批评者是错的。这是辩论中谄媚行为的等价物（第 14 课）。

Conformity is why debate-until-agreement rewards bullies. Bounded rounds with a separate judge mitigate.

> 从众是为什么"辩论到同意"会奖励强势者。有界轮次加上独立评委可以缓解。

### Heterogeneity: the actual knob that moves accuracy

A 2024-2026 pattern in the practical literature: swapping one of your N agents for a different base model gives a bigger accuracy bump than increasing N by 1. The intuition is monoculture — each new independent-error source is worth more than an additional correlated sample.

> 2024-2026 年实用文献中的一个模式：将 N 个 Agent 中的一个换成不同基础模型比增加 N+1 个 Agent 带来更大的准确率提升。直觉是单一文化——每个新的独立错误源比额外的相关样本更有价值。

In the limit, heterogeneity beats numerosity. Three different models beat five copies of one model on most tasks that have clean ground truth.

> 在极限情况下，异构性胜过数量。在大多数有明确标准答案的任务上，三个不同模型胜过五个同一模型的副本。

### Jury methods

The Sibyl framework (cited in Minsky-LLM literature) formalizes a "jury" — a small set of specialized agents that refine answers by voting at each stage. Unlike plain majority vote, a jury has roles: one agent cross-examines, one supplies context, one scores plausibility. Jury methods are a midpoint between plain vote (cheap, monoculture-prone) and full MAD (expensive, conformity-prone).

> Sibyl 框架（在 Minsky-LLM 文献中引用）形式化了"陪审团"——一小组专业化 Agent 通过每阶段投票来改进答案。与简单多数投票不同，陪审团有角色：一个 Agent 交叉质询，一个提供上下文，一个评分合理性。陪审团方法介于简单投票（便宜，易单一文化）和完整 MAD（昂贵，易从众）之间。

### When vote-with-debate dominates

- The question has ground truth (fact, math, code behavior). Vote convergence is meaningful.
  中文翻译：问题有标准答案（事实、数学、代码行为）。投票收敛是有意义的。
- Agents can access different sources or tools (heterogeneity is available).
  中文翻译：Agent 可以访问不同的来源或工具（异构性可用）。
- Rounds are bounded (2-3 typical) and there is a separate judge or verifier.
  中文翻译：轮次有界（通常 2-3 轮），有独立的评委或验证器。
- Budget allows 3-5 agents. Beyond 5-7 on graph topology, coordination tax dominates.
  中文翻译：预算允许 3-5 个 Agent。在图形拓扑上超过 5-7 个时，协调税占主导。

### When vote-with-debate hurts

- The question is opinion-shaped. Agents converge to whichever answer looks most confident, not most correct.
  中文翻译：问题是意见型的。Agent 收敛到看起来最自信的答案，而非最正确的。
- All agents share a base model. Monoculture makes consensus meaningless.
  中文翻译：所有 Agent 共享基础模型。单一文化使共识毫无意义。
- Rounds are unbounded. Conformity wins every time.
  中文翻译：轮次无界。从众每次都赢。
- The task is simple. A single agent with self-consistency at N=5 is cheaper and as accurate.
  中文翻译：任务简单。单 Agent 在 N=5 时的自一致性更便宜且同样准确。

## Build It | 动手构建

`code/main.py` implements:

- `run_star(agents, hub, question)` — hub polls each worker, aggregates.
  中文翻译：`run_star` — 中心轮询每个工作者并聚合。
- `run_chain(agents, question)` — sequential refinement.
  中文翻译：`run_chain` — 顺序改进。
- `run_tree(root, children, question)` — hierarchical with depth-2 aggregation.
  中文翻译：`run_tree` — 层次化，深度 2 聚合。
- `run_graph(agents, question, rounds)` — all-to-all debate, bounded rounds.
  中文翻译：`run_graph` — 全对全辩论，有界轮次。
- A scripted heterogeneity dial: each agent has an `error_bias` indicating its systematic wrongness.
  中文翻译：脚本化的异构度旋钮：每个 Agent 有一个 `error_bias` 表示其系统性错误。
- A measurement harness that runs each topology at N=3, 5, 7 and reports (accuracy, total_tokens, wallclock_simulated).
  中文翻译：测量工具在 N=3, 5, 7 时运行每个拓扑并报告（准确率，总 token，模拟挂钟时间）。

Run:

```
python3 code/main.py
```

Expected output: a table of topology × N → (accuracy, tokens, latency). Graph wins at N=3-5 on the research-style tasks; star wins on the fast-factual tasks; graph at N=7 shows the coordination tax (latency inflates faster than accuracy).

> 预期输出：拓扑 × N →（准确率，token，延迟）表格。图形在 N=3-5 的研究风格任务上获胜；星形在快速事实性任务上获胜；图形在 N=7 时显示协调税（延迟膨胀快于准确率）。

## Use It | 使用方法

`outputs/skill-topology-picker.md` is a skill that reads a task description and recommends a topology (star / chain / tree / graph), an N (number of agents), a heterogeneity profile (base models to use), and a round bound.

> `outputs/skill-topology-picker.md` 是一个 skill，读取任务描述并推荐拓扑（星形/链形/树形/图形）、N（Agent 数量）、异构配置（使用的基础模型）和轮次上限。

## Ship It | 部署上线

For any ensemble:

- Start with **self-consistency at N=5** using one strong base model. It is the cheap baseline.
  中文翻译：从一个强基础模型的 **N=5 自一致性**开始。这是廉价基线。
- Upgrade to **heterogeneous voting at N=3** if accuracy matters. Measure the delta.
  中文翻译：如果准确率重要，升级到 **N=3 异构投票**。测量增量。
- Only upgrade to **debate topology** if the task has structure (research, multi-step) and bounded rounds are feasible.
  中文翻译：只有在任务有结构（研究、多步骤）且有界轮次可行时才升级到**辩论拓扑**。
- Always log the minority cluster. When a minority is persistently right, you have a diversity signal.
  中文翻译：始终记录少数派簇。当少数派持续正确时，你就有多样性信号。
- Benchmark wall-clock and tokens alongside accuracy. "Better accuracy at 10x cost" is a business decision.
  中文翻译：基准测试挂钟时间和 token 以及准确率。"10 倍成本的更好准确率"是商业决策。

## Exercises | 练习题

1. Run `code/main.py`. Plot the coordination-tax curve for graph topology: accuracy vs N, tokens vs N. At what N does the curve inflect?
   中文翻译：运行 `code/main.py`。绘制图形拓扑的协调税曲线：准确率 vs N，token vs N。曲线在哪个 N 处拐折？
2. Implement A-HMAD: three agents with deliberately different biases. How does the all-same-bias baseline compare to A-HMAD on the monoculture attack from Lesson 14?
   中文翻译：实现 A-HMAD：三个具有故意不同偏差的 Agent。全同偏差基线与 A-HMAD 在第 14 课的单一文化攻击上如何比较？
3. Add a "judge" role to the graph topology that does not vote, only scores the final consensus. Does this change the emergent conformity behavior?
   中文翻译：在图形拓扑中添加一个"评委"角色，不投票只评分最终共识。这会改变涌现的从众行为吗？
4. Read the AgentVerse paper (ICLR 2024). Identify which emergent behavior your implementation exhibits most strongly. Can you elicit the opposite behavior by a prompt change?
   中文翻译：阅读 AgentVerse 论文（ICLR 2024）。识别你的实现最强烈地展现哪种涌现行为。你能通过提示变更激发相反的行为吗？
5. Read MultiAgentBench (arXiv:2503.01935) Section 4 (topology experiments). Reproduce the "graph-wins-research" result on one task from the paper using your harness.
   中文翻译：阅读 MultiAgentBench（arXiv:2503.01935）第 4 节（拓扑实验）。用你的工具复现论文中一个任务上的"图形胜于研究"结果。

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Further Reading | 延伸阅读

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) — single-model baseline
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) — both agents AND rounds matter independently
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) — topology benchmark showing graph best for research, chain for pipelines
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) — MAD-strategy survey; finds MAD often loses to self-consistency at equal budget
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) — volunteer and conformity emergent patterns
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) — reference benchmark implementation
