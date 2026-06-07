# Tree of Thoughts and LATS: Deliberate Search | 思维树与 LATS：深思熟虑的搜索

> A single chain-of-thought trajectory has no room to backtrack. ToT (Yao et al., 2023) turns reasoning into a tree with self-evaluation on each node. LATS (Zhou et al., 2024) unifies ToT with ReAct and Reflexion under Monte Carlo Tree Search. Game of 24 goes from 4% (CoT) to 74% (ToT); LATS hits 92.7% pass@1 on HumanEval.

> **【中文解读】** 单条思维链没有回溯空间。ToT 将推理变为带有自评估的树结构，Game of 24 从 4% 提升到 74%。LATS 统一了 ToT、ReAct 和 Reflexion，用蒙特卡洛树搜索实现，HumanEval 达到 92.7% pass@1。

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】** OpenAI o1/o3 系列模型的"深度思考"本质上就是搜索——在推理空间中探索多条路径，评估并选择最佳。ToT 和 LATS 是这种搜索范式的学术先驱。2026 年的 Coding Agent 在遇到复杂 bug 时也会启用类似搜索。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Frame reasoning as search: nodes are "thoughts," edges are "expansions," value is "how promising."
  中文翻译：将推理框架为搜索：节点是"思考"，边是"扩展"，值是"有多大前景"。
- Implement a stdlib ToT-style BFS tree search with self-evaluation scoring.
  中文翻译：用标准库实现 ToT 风格的 BFS 树搜索，带自评估评分。
- Extend to a toy LATS MCTS loop with select / expand / simulate / backpropagate.
  中文翻译：扩展为玩具 LATS MCTS 循环，包含选择/扩展/模拟/反向传播。
- Decide when search is worth the token multiplier (Game of 24, code generation) and when a single trajectory is enough (simple Q&A).
  中文翻译：决定何时搜索值得付出 token 倍增成本（Game of 24、代码生成），何时单轨迹足够（简单问答）。

## The Problem | 问题引入

Chain-of-thought is a linear walk. If the first step is wrong, every subsequent step works on a bad premise. On Game of 24 (use four digits with + − × ÷ to make 24), GPT-4 CoT hits 4% accuracy. The model picks the wrong subexpression early and cannot recover.

> 思维链是线性推进的。如果第一步错了，后续每一步都基于错误前提。在 Game of 24（用四个数字和 + − × ÷ 得到 24）上，GPT-4 CoT 只有 4% 准确率。模型在早期选错子表达式后无法恢复。

What reasoning needs is the ability to propose multiple candidates, evaluate them, pick the promising ones, and backtrack when dead ends appear. That is search. Tree of Thoughts and LATS are the two canonical formulations.

> 推理需要的是：提出多个候选方案、评估它们、选择有前景的、在死胡同时回溯。这就是搜索。思维树和 LATS 是两种经典的实现方式。

> **【中文解读】** 思维链是线性推进的——如果第一步错了，后面每一步都基于错误前提。Game of 24 上 GPT-4 CoT 只有 4% 准确率。推理需要的是：提出多个候选方案、评估它们、选择有前景的、在死胡同时回溯。这就是搜索。

## The Concept | 核心概念

### Tree of Thoughts (Yao et al., NeurIPS 2023)

Each node is a coherent intermediate step ("a thought"). Each node can expand to K child thoughts. The LLM self-evaluates each node with a scoring prompt. Search explores the tree — BFS, DFS, or beam.

> 每个节点是一个连贯的中间步骤（"一个思考"）。每个节点可以扩展为 K 个子思考。LLM 用评分提示自评估每个节点。搜索探索这棵树——BFS、DFS 或 beam 搜索。

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

Self-evaluation is the load-bearing piece. The paper shows three variants: `sure / likely / impossible` classification, `1..10` numeric score, and vote among candidates. All three beat CoT substantially on Game of 24 (4% -> 74% with GPT-4).

> 自评估是核心承载部分。论文展示了三种变体：`sure / likely / impossible` 分类、`1..10` 数值评分和候选投票。三种都在 Game of 24 上大幅超越 CoT（4% -> 74%，使用 GPT-4）。

### LATS (Zhou et al., ICML 2024)

LATS unifies ToT, ReAct, and Reflexion under MCTS. The LLM plays three roles:

> LATS 在 MCTS 下统一了 ToT、ReAct 和 Reflexion。LLM 扮演三个角色：

- **Policy**: propose candidate next actions (ReAct-style).
  中文翻译：**策略**：提出候选下一步行动（ReAct 风格）。
- **Value function**: score a partial trajectory (ToT-style self-eval).
  中文翻译：**价值函数**：对部分轨迹评分（ToT 风格自评估）。
- **Self-reflector**: on failure, write a natural-language reflection (Reflexion-style) and use it to reseed future rollouts.
  中文翻译：**自我反思器**：失败时写自然语言反思（Reflexion 风格），用于重新播种未来的展开。

Environment feedback (observations) mixes into the value function so the search is informed by real tool results, not just model opinions. Results at paper time: HumanEval pass@1 92.7% with GPT-4 (SOTA), WebShop average 75.9 with GPT-3.5 (approaching gradient-based fine-tuning).

> 环境反馈（观察）混入价值函数，使搜索由真实工具结果而非仅模型观点驱动。论文发表时的结果：GPT-4 上 HumanEval pass@1 92.7%（SOTA），GPT-3.5 上 WebShop 平均 75.9（接近基于梯度的微调）。

### MCTS, minimally

Four phases per iteration:

> 每次迭代四个阶段：

1. **Select** — walk from root to a leaf using UCT (upper confidence bound for trees).
   中文翻译：**选择**——用 UCT（树的上置信界）从根走到叶节点。
2. **Expand** — generate K children via the policy.
   中文翻译：**扩展**——用策略生成 K 个子节点。
3. **Simulate** — rollout from a child using the policy, score the leaf with the value function (or environment reward).
   中文翻译：**模拟**——从子节点用策略展开，用价值函数（或环境奖励）评分叶节点。
4. **Backpropagate** — update visit counts and value estimates up the path.
   中文翻译：**反向传播**——沿路径更新访问计数和价值估计。

UCT formula: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`. First term is exploitation; second is exploration. Tune `c` per task.

> UCT 公式：`Q(s, a) + c * sqrt(ln N(s) / N(s, a))`。第一项是利用；第二项是探索。按任务调整 `c`。

### The cost reality

Search explodes tokens. ToT on Game of 24 uses 100–1000x the tokens of CoT. LATS is similar. This is not free; reserve search for:

> 搜索会爆炸 token。ToT 在 Game of 24 上消耗 CoT 的 100-1000 倍 token。LATS 类似。这不是免费的；将搜索留给：

- Tasks where a single trajectory is demonstrably insufficient (Game of 24, complex code).
  中文翻译：单轨迹明显不足的任务（Game of 24、复杂代码）。
- Tasks where wall-clock is less important than correctness.
  中文翻译：正确性比耗时更重要的任务。
- Tasks with a cheap, reliable value function (unit tests for code, explicit target for math).
  中文翻译：有廉价可靠价值函数的任务（代码的单元测试、数学的明确目标）。

If your task has a single right answer and a noisy evaluator, search often makes things worse — it finds a "good-scoring" wrong answer.

> 如果你的任务只有一个正确答案但评估器有噪声，搜索往往使情况更糟——它会找到一个"高分但错误"的答案。

> **【中文解读】** 搜索会爆炸 Token——ToT 在 Game of 24 上消耗 CoT 的 100-1000 倍。只在以下场景使用搜索：单轨迹明显不足、正确性比速度重要、有廉价可靠的价值函数。如果评估器有噪声，搜索可能找到"高分但错误"的答案。

### 2026 positioning

Most production agents do not run LATS. They run ReAct with tool-grounded verification (CRITIC, Lesson 05). Search shows up in specialized niches:

> 大多数生产 Agent 不运行 LATS。它们运行带工具锚定验证的 ReAct（CRITIC，第 5 课）。搜索出现在专门领域：

- Coding agents that run tests as the value function (HumanEval-style).
  中文翻译：以测试作为价值函数的编码 Agent（HumanEval 风格）。
- Deep-research agents that explore multiple query paths.
  中文翻译：探索多个查询路径的深度研究 Agent。
- Planning-heavy workflows inside LangGraph subgraphs.
  中文翻译：LangGraph 子图内的重规划工作流。

AlphaEvolve (Lesson 11) is the 2025 extreme: evolutionary search over code, machine-checkable fitness, frontier gains (first 4x4 matmul improvement in 56 years).

> AlphaEvolve（第 11 课）是 2025 年的极端案例：代码上的进化搜索、机器可检查的适应度、前沿突破（56 年来首次 4x4 矩阵乘法改进）。

## Build It | 动手实现

`code/main.py` implements:

> `code/main.py` 实现了：

- A tiny ToT BFS on a stylized "pick arithmetic ops" task.
  中文翻译：在风格化"选算术运算"任务上的微型 ToT BFS。
- A toy LATS MCTS loop on the same task (Select / Expand / Simulate / Backpropagate) with UCT selection.
  中文翻译：同一任务上的玩具 LATS MCTS 循环（选择/扩展/模拟/反向传播），带 UCT 选择。
- A value function that composes a symbolic score plus a self-eval score.
  中文翻译：一个组合符号评分和自评估评分的价值函数。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows ToT expanding three candidates per node with BFS, compared to LATS converging on the best rollout via MCTS. Token counts printed for both.

> 轨迹显示 ToT 用 BFS 每个节点扩展三个候选，与 LATS 通过 MCTS 收敛到最佳展开对比。两者都打印了 token 计数。

## Use It | 用框架实现

LangGraph ships ToT-style exploration as subgraph patterns; the LangChain team's blog on LATS (May 2024) is the reference tutorial. LlamaIndex ships a `TreeOfThoughts` agent. For most 2026 production agents this pattern lives behind an `if task_complexity > threshold: use_search()` gate — see the evaluator-optimizer pattern in Lesson 05.

> LangGraph 将 ToT 风格的探索作为子图模式提供；LangChain 团队关于 LATS 的博客（2024 年 5 月）是参考教程。LlamaIndex 提供了 `TreeOfThoughts` Agent。对于大多数 2026 年的生产 Agent，这个模式存在于 `if task_complexity > threshold: use_search()` 门控之后——参见第 5 课的评估器-优化器模式。

## Ship It | 产出物

`outputs/skill-search-policy.md` selects between linear ReAct, ToT, LATS, and evolutionary search given task shape, budget, and evaluator fidelity.

> `outputs/skill-search-policy.md` 根据任务形状、预算和评估器保真度，在线性 ReAct、ToT、LATS 和进化搜索之间选择。

## Exercises | 练习题

1. Run the toy LATS with UCT c=0.1 vs c=2.0. What changes in the trace?
   中文翻译：用 UCT c=0.1 和 c=2.0 分别运行 LATS。轨迹有什么变化？
2. Swap the value function for a noisier scorer (add random jitter). Does MCTS still find the best leaf? What is the minimum signal-to-noise it tolerates?
   中文翻译：将价值函数替换为更嘈杂的评分器。MCTS 还能找到最佳叶节点吗？它能容忍的最小信噪比是多少？
3. Implement beam-search ToT (keep top-k at each level) and compare to BFS. Which is better on a tight token budget?
   中文翻译：实现 beam-search ToT（每层保留 top-k），与 BFS 对比。Token 预算紧张时哪个更好？
4. Read LATS Section 5.1. Reproduce the HumanEval trajectory count: how many rollouts does it take to hit the reported pass@1?
   中文翻译：阅读 LATS 第 5.1 节。重现 HumanEval 的轨迹数量：达到报告的 pass@1 需要多少次展开？
5. Read the LATS paper's discussion on "when LATS helps less." Write a one-paragraph decision rule mapping task shape to search strategy.
   中文翻译：阅读 LATS 论文关于"何时 LATS 帮助不大"的讨论。写一段决策规则映射任务形状到搜索策略。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tree of Thoughts | "Branching CoT" / "分支思维链" | Yao et al. — tree of thought nodes with self-evaluation / Yao 等人——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" / "LLM 的 MCTS" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS / Zhou 等人——在 MCTS 下统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" / "上置信界" | Select formula balancing exploitation (Q) and exploration (ln N / n) / 平衡利用(Q)和探索(ln N/n)的选择公式 |
| Value function | "How good is this state" / "状态有多好" | Prompted LLM score or environment reward; feeds backprop / 提示的 LLM 评分或环境奖励；驱动反向传播 |
| Policy | "Action proposer" / "行动提议器" | ReAct-style generator; emits candidate next thoughts/actions / ReAct 风格生成器；发出候选下一步思考/行动 |
| Rollout | "Simulated trajectory" / "模拟轨迹" | Walk from a node to a leaf using policy, score with value / 用策略从节点走到叶节点，用价值函数评分 |
| Backpropagate | "Update ancestors" / "更新祖先" | Push the leaf's reward up the path, updating visit counts and Q / 将叶节点的奖励沿路径上推，更新访问计数和 Q 值 |
| Search cost | "Token explosion" / "Token 爆炸" | 100-1000x CoT on Game of 24; budget before you adopt / Game of 24 上是 CoT 的 100-1000 倍；采用前先做预算 |

## Further Reading | 延伸阅读

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) — the canonical paper
  中文翻译：思维树经典论文。
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) — MCTS with Reflexion feedback
  中文翻译：LATS——带 Reflexion 反馈的蒙特卡洛树搜索。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — subgraph patterns for search
  中文翻译：LangGraph 概览——搜索的子图模式。
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) — evolutionary search with programmatic evaluators
  中文翻译：AlphaEvolve——带程序化评估器的进化搜索。
