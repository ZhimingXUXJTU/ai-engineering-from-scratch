# Theory of Mind and Emergent Coordination | 心智理论 协调

> Li et al. (arXiv:2310.10701) showed that LLM agents in a cooperative text game exhibit **emergent high-order Theory of Mind** (ToM) — reasoning about what another agent believes about a third agent's beliefs — but fail on long-horizon planning due to context management and hallucination. Riedl (arXiv:2510.05174) measured higher-order synergy across a population and found that **only** the ToM-prompt condition produces identity-linked differentiation and goal-directed complementarity; lower-capacity LLMs show only spurious emergence. That is, coordination emergence is prompt-conditional and model-dependent, not free. This lesson implements a minimal ToM-aware agent, runs a cooperative task with and without ToM prompting, and measures the coordination delta against the Riedl 2025 protocol.

> **【中文解读】** 本节介绍了心智理论协调——Agent 理解和预测其他 Agent 意图的协调机制。

> **【拓展：theory of mind coordination→具体应用】** 心智理论（Theory of Mind）是指理解和预测他人心理状态的能力。在多 Agent 系统中，具有心智理论的 Agent 能更好地协调——它知道其他 Agent 知道什么、想要什么、会做什么。2025-2026 年的研究表明，显式建模其他 Agent 的意图能显著提高协调效率，但也增加了计算成本。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Multi-agent coordination often looks magical: agents divide labor, anticipate each other, avoid redundancy. Usually this "emergence" is an artifact of prompt engineering — someone told the agents to "coordinate." Remove the prompt, remove the coordination.

> 多 Agent 协调通常看起来很神奇：Agent 分工、相互预判、避免冗余。通常这种"涌现"是提示工程的产物——有人告诉 Agent 要"协调"。移除提示，协调就消失。

Riedl's 2025 finding is stricter: under controlled conditions, coordination only emerges when agents are prompted to reason about **other agents' minds** (ToM). Without the ToM prompt, even strong models show coordination patterns that do not survive statistical controls. This matters for production: teams ship "multi-agent coordination" features that are prompt-dependent and brittle.

> Riedl 2025 年的发现更严格：在受控条件下，协调只在 Agent 被提示推理**其他 Agent 的心理**（ToM）时才涌现。没有 ToM 提示，即使是强模型也显示出统计控制下不存的协调模式。这对生产很重要：团队发布的"多 Agent 协调"功能依赖提示且脆弱。

This lesson treats ToM as a specific capability (reasoning about beliefs about beliefs), builds a minimal ToM-aware agent, and measures what real coordination looks like vs. what prompt dressing looks like.

> 本课将 ToM 视为一种特定能力（对关于信念的信念进行推理），构建一个最小的 ToM 感知 Agent，并测量真正的协调与提示装饰的区别。

## Concept | 核心概念

### What ToM means

Developmental psychology: a 3-year-old thinks anyone's inner world matches theirs. A 5-year-old understands others have different beliefs. A 7-year-old reasons about beliefs about beliefs ("she thinks that I think the ball is under the cup"). These are zeroth, first, and second-order ToM.

> 发展心理学：3 岁的孩子认为任何人的内心世界都与自己相同。5 岁的孩子理解他人有不同的信念。7 岁的孩子推理关于信念的信念（"她认为我认为球在杯子下面"）。这些是零阶、一阶和二阶 ToM。

For LLM agents, ToM orders map to:

> 对于 LLM Agent，ToM 阶次映射到：

- **Zeroth-order:** no model of others. The agent acts on its own observations only.
  中文翻译：**零阶：** 没有他人的模型。Agent 只根据自己的观察行动。
- **First-order:** the agent has a model of each other agent's beliefs. "Alice believes X."
  中文翻译：**一阶：** Agent 对每个其他 Agent 的信念有模型。"Alice 相信 X。"
- **Second-order:** the agent models recursive beliefs. "Alice believes that Bob believes X."
  中文翻译：**二阶：** Agent 建模递归信念。"Alice 相信 Bob 相信 X。"

Li et al. 2023 found that first- and second-order ToM emerge in LLM agents in cooperative games but degrade with long horizon and unreliable communication.

> Li 等人 2023 年发现，一阶和二阶 ToM 在合作游戏中的 LLM Agent 中涌现，但在长时间范围和不可靠通信下退化。

### The Sally-Anne test, in brief

A 1985 false-belief test: Sally puts a marble in basket A, leaves. Anne moves it to basket B. Where will Sally look when she returns? A child with first-order ToM says basket A (Sally's belief differs from reality). A child without says basket B.

> 1985 年的错误信念测试：Sally 把弹珠放在篮子 A 里，离开。Anne 把它移到篮子 B。Sally 回来时会去哪里找？有一阶 ToM 的孩子说篮子 A（Sally 的信念与现实不同）。没有的孩子说篮子 B。

GPT-4-era LLMs pass Sally-Anne-style tests when posed plainly. They fail when the narrative is long, the scene changes several times, or the question is phrased indirectly. That is the practical 2026 state of ToM in production LLMs.

> GPT-4 时代的 LLM 在直接提问时通过 Sally-Anne 风格测试。当叙述很长、场景多次变化或问题间接表达时失败。这就是 2026 年生产 LLM 中 ToM 的实际状态。

### Riedl's coordination measurement

Riedl (arXiv:2510.05174) built a population-scale test: N agents, a cooperative objective, variable prompt conditions. Measure:

> Riedl（arXiv:2510.05174）构建了群体规模测试：N 个 Agent，合作目标，可变提示条件。测量：

1. **Identity-linked differentiation.** Do agents develop stable role distinctions over time?
   中文翻译：**身份关联分化。** Agent 随时间发展稳定的角色区分吗？
2. **Goal-directed complementarity.** Do agents' actions complement each other (different subtasks) rather than duplicate?
   中文翻译：**目标导向互补性。** Agent 的行为是互补的（不同子任务）而非重复的吗？
3. **Higher-order synergy.** A statistical measure of whether the group achieves what no subset could.
   中文翻译：**高阶协同。** 群体是否达成了任何子集都无法达成的统计度量。

Result: only under the ToM prompt condition do all three metrics produce signal above baseline. Without ToM prompting, metrics hover near chance for moderate-capacity models. Large models show some coordination without explicit ToM prompting but the effect is smaller than with explicit prompting.

> 结果：只有在 ToM 提示条件下，三个指标才产生高于基线的信号。没有 ToM 提示时，中等能力模型的指标在随机水平附近徘徊。大模型在没有显式 ToM 提示时显示出一些协调，但效果比显式提示小。

### The coordination illusion

Without statistical controls, "emergent coordination" in demos often reflects:

> 没有统计控制，演示中的"涌现协调"通常反映的是：

- Prompt engineering that bakes in coordination (system prompts that say "work together").
  中文翻译：嵌入协调的提示工程（系统提示说"一起工作"）。
- Observer bias (we see patterns we expect).
  中文翻译：观察者偏差（我们看到期望的模式）。
- Post-hoc selection of successful runs.
  中文翻译：成功运行的事后选择。

Production systems that market "emergent coordination" without measurable signal should be treated as marketing. Measure before claiming.

> 没有可测量信号就宣传"涌现协调"的生产系统应该被视为营销。先测量再声称。

### A minimal ToM-aware agent

Structure:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

The `other_models` attribute is the ToM state. First-order ToM keeps just one level. Second-order adds `other_models[i][other_models_of_j]` — what I think agent i thinks agent j believes.

### Why long-horizon hurts

Li et al. document: context limits cause agents to forget which belief belongs to whom. Hallucination adds false beliefs to other-agent models. Both produce "I thought he thought X" errors that compound over time.

Mitigations documented in the paper and in 2024-2026 follow-ups:

- **Explicit ToM state in the prompt.** Structured format: `{agent_id: belief_list}`. Forces retrieval to preserve identity-belief binding.
- **Shorter reasoning chains.** Fewer ToM updates per turn reduce compounding hallucination.
- **External ToM store.** Maintain the model outside the LLM context; inject only relevant parts per turn.

### Where ToM fails in production

- **Adversarial settings.** Agents with good ToM are easier to manipulate (you can model what they model of you, then exploit).
- **Heterogeneous teams.** When models are different, the ToM model that works for one opponent does not generalize.
- **Ground-truth-dependent tasks.** ToM is about beliefs; if correctness depends on facts, ToM can be a distraction.

### The coordination you can actually measure

Three practical signals a team's coordination is real rather than prompt-dressed:

1. **Complementarity over time.** Over a multi-turn task, do agents' actions cover disjoint sub-tasks?
2. **Anticipation.** Does agent A's action at turn T+1 depend on a prediction about B's action at T+2 that turned out correct?
3. **Correction.** When A misreads B's belief at turn T, does A correct by turn T+2?

These are measurable in a logged multi-agent system. They are the substantive version of the "coordination" narrative.

## Build It | 动手构建

`code/main.py` implements:

- `ToMAgent` — tracks own beliefs and per-other-agent belief models.
  中文翻译：`ToMAgent` — 跟踪自身信念和每个其他 Agent 的信念模型。
- A cooperative task: three agents must collect three tokens from three boxes; each box can hold one token. Agents cannot communicate; they infer intent from each other's actions.
  中文翻译：合作任务：三个 Agent 必须从三个盒子中收集三个 token；每个盒子只能放一个 token。Agent 不能通信；它们从彼此的行为推断意图。
- Two configurations: `zeroth_order` (no ToM) and `first_order` (ToM with one-level belief model).
  中文翻译：两种配置：`zeroth_order`（无 ToM）和 `first_order`（带一层信念模型的 ToM）。
- Measurement over 200 randomized trials: completion rate, duplication rate (two agents targeting the same box), average turns to completion.
  中文翻译：200 次随机试验的测量：完成率、重复率（两个 Agent 瞄准同一个盒子）、平均完成轮次。

Run:

```
python3 code/main.py
```

Expected output: zeroth-order agents duplicate effort at ~35% rate and complete ~60% of trials in 10 turns. First-order ToM agents duplicate at ~5% and complete ~95%. The delta is the measurable coordination effect.

> 预期输出：零阶 Agent 以约 35% 的比率重复工作并在 10 轮内完成约 60% 的试验。一阶 ToM Agent 以约 5% 的比率重复并完成约 95%。差异就是可测量的协调效果。

## Use It | 使用方法

`outputs/skill-tom-auditor.md` is a skill that audits a multi-agent system's claim of "emergent coordination." Checks for prompt dressing, statistical significance against a control, and measured complementarity.

> `outputs/skill-tom-auditor.md` 是一个审计多 Agent 系统"涌现协调"声明的 skill。检查提示装饰、相对对照组的统计显著性和测量的互补性。

## Ship It | 部署上线

Coordination claims checklist:

- **Control condition.** A version of your system without the coordination prompt. Measure both.
  中文翻译：**对照条件。** 没有协调提示的系统版本。两者都测量。
- **Statistical test.** Is the difference between system and control significant at `p < 0.05` on your metric?
  中文翻译：**统计测试。** 系统和对照的差异在你的指标上是否在 `p < 0.05` 水平显著？
- **Complementarity measure.** Action-disjointness over time, not just final success.
  中文翻译：**互补性测量。** 随时间的动作不交性，不仅是最终成功。
- **Failure-case log.** When agents miscoordinate, what does the ToM state look like?
  中文翻译：**失败案例日志。** 当 Agent 协调失败时，ToM 状态是什么样的？
- **Model-capacity disclosure.** If the effect vanishes on smaller models, say so.
  中文翻译：**模型能力披露。** 如果效果在较小模型上消失，说明这一点。

## Exercises | 练习题

1. Run `code/main.py`. Confirm first-order ToM reduces duplication rate by ~7x. Does the gap persist when you scale to 5 agents and 5 boxes?
   中文翻译：运行 `code/main.py`。确认一阶 ToM 将重复率降低约 7 倍。扩展到 5 个 Agent 和 5 个盒子时差距仍然存在吗？
2. Implement second-order ToM (agent A models what B thinks about C). Does it improve over first-order? On what tasks?
   中文翻译：实现二阶 ToM（Agent A 建模 B 对 C 的想法）。它比一阶改进了吗？在什么任务上？
3. Inject a **hallucination** into the ToM state: randomly flip one belief per turn. How much does this degrade first-order performance?
   中文翻译：向 ToM 状态注入**幻觉**：每轮随机翻转一个信念。这会使一阶性能下降多少？
4. Read Li et al. (arXiv:2310.10701). Reproduce the "long-horizon degradation" finding: as turns grow from 10 to 30, how does your first-order ToM performance change?
   中文翻译：阅读 Li 等人（arXiv:2310.10701）。复现"长期退化"发现：当轮次从 10 增长到 30 时，你的一阶 ToM 性能如何变化？
5. Read Riedl 2025 (arXiv:2510.05174). Implement the higher-order synergy statistic on your simulation logs. Is the effect present without the ToM prompt condition?
   中文翻译：阅读 Riedl 2025（arXiv:2510.05174）。在你的模拟日志上实现高阶协同统计。没有 ToM 提示条件下效果存在吗？

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Further Reading | 延伸阅读

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) — emergent ToM in cooperative games; long-horizon failure modes
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) — population-scale measurement; ToM prompting is the load-bearing condition
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) — the 1978 origin of the ToM concept
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-autistic-child-have-a-theory-of-mind/) — the Sally-Anne paper (1985)
