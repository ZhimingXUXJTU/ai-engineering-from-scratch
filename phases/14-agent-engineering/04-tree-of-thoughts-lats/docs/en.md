# Tree of Thoughts and LATS: Deliberate Search | 思维树与 LATS：深思熟虑的搜索

> A single chain-of-thought trajectory has no room to backtrack. ToT (Yao et al., 2023) turns reasoning into a tree with self-evaluation on each node. LATS (Zhou et al., 2024) unifies ToT with ReAct and Reflexion under Monte Carlo Tree Search. Game of 24 goes from 4% (CoT) to 74% (ToT); LATS hits 92.7% pass@1 on HumanEval.

> **【中文解读】** 单条思维链没有回溯空间。ToT 将推理变为带有自评估的树结构，Game of 24 从 4% 提升到 74%。LATS 统一了 ToT、ReAct 和 Reflexion，用蒙特卡洛树搜索实现，HumanEval 达到 92.7% pass@1。

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】** OpenAI o1/o3 系列模型的"深度思考"本质上就是搜索——在推理空间中探索多条路径，评估并选择最佳。ToT 和 LATS 是这种搜索范式的学术先驱。2026 年的 Coding Agent 在遇到复杂 bug 时也会启用类似搜索。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes

## Learning Objectives

- Frame reasoning as search: nodes are "thoughts," edges are "expansions," value is "how promising."
- Implement a stdlib ToT-style BFS tree search with self-evaluation scoring.
- Extend to a toy LATS MCTS loop with select / expand / simulate / backpropagate.
- Decide when search is worth the token multiplier (Game of 24, code generation) and when a single trajectory is enough (simple Q&A).

## The Problem | 问题

Chain-of-thought is a linear walk. If the first step is wrong, every subsequent step works on a bad premise. On Game of 24 (use four digits with + − × ÷ to make 24), GPT-4 CoT hits 4% accuracy. The model picks the wrong subexpression early and cannot recover.

What reasoning needs is the ability to propose multiple candidates, evaluate them, pick the promising ones, and backtrack when dead ends appear. That is search. Tree of Thoughts and LATS are the two canonical formulations.

> **【中文解读】** 思维链是线性推进的——如果第一步错了，后面每一步都基于错误前提。Game of 24 上 GPT-4 CoT 只有 4% 准确率。推理需要的是：提出多个候选方案、评估它们、选择有前景的、在死胡同时回溯。这就是搜索。

## The Concept

### Tree of Thoughts (Yao et al., NeurIPS 2023)

Each node is a coherent intermediate step ("a thought"). Each node can expand to K child thoughts. The LLM self-evaluates each node with a scoring prompt. Search explores the tree — BFS, DFS, or beam.

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

Self-evaluation is the load-bearing piece. The paper shows three variants: `sure / likely / impossible` classification, `1..10` numeric score, and vote among candidates. All three beat CoT substantially on Game of 24 (4% -> 74% with GPT-4).

### LATS (Zhou et al., ICML 2024)

LATS unifies ToT, ReAct, and Reflexion under MCTS. The LLM plays three roles:

- **Policy**: propose candidate next actions (ReAct-style).
- **Value function**: score a partial trajectory (ToT-style self-eval).
- **Self-reflector**: on failure, write a natural-language reflection (Reflexion-style) and use it to reseed future rollouts.

Environment feedback (observations) mixes into the value function so the search is informed by real tool results, not just model opinions. Results at paper time: HumanEval pass@1 92.7% with GPT-4 (SOTA), WebShop average 75.9 with GPT-3.5 (approaching gradient-based fine-tuning).

### MCTS, minimally

Four phases per iteration:

1. **Select** — walk from root to a leaf using UCT (upper confidence bound for trees).  # 选择——用 UCT 从根走到叶节点
2. **Expand** — generate K children via the policy.                                       # 扩展——用策略生成 K 个子节点
3. **Simulate** — rollout from a child using the policy, score the leaf with the value function (or environment reward).  # 模拟——从子节点展开并评分
4. **Backpropagate** — update visit counts and value estimates up the path.                # 反向传播——更新路径上的访问计数和价值估计

UCT formula: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`. First term is exploitation; second is exploration. Tune `c` per task.

### The cost reality

Search explodes tokens. ToT on Game of 24 uses 100–1000x the tokens of CoT. LATS is similar. This is not free; reserve search for:

- Tasks where a single trajectory is demonstrably insufficient (Game of 24, complex code).
- Tasks where wall-clock is less important than correctness.
- Tasks with a cheap, reliable value function (unit tests for code, explicit target for math).

If your task has a single right answer and a noisy evaluator, search often makes things worse — it finds a "good-scoring" wrong answer.

> **【中文解读】** 搜索会爆炸 Token——ToT 在 Game of 24 上消耗 CoT 的 100-1000 倍。只在以下场景使用搜索：单轨迹明显不足、正确性比速度重要、有廉价可靠的价值函数。如果评估器有噪声，搜索可能找到"高分但错误"的答案。

### 2026 positioning

Most production agents do not run LATS. They run ReAct with tool-grounded verification (CRITIC, Lesson 05). Search shows up in specialized niches:

- Coding agents that run tests as the value function (HumanEval-style).
- Deep-research agents that explore multiple query paths.
- Planning-heavy workflows inside LangGraph subgraphs.

AlphaEvolve (Lesson 11) is the 2025 extreme: evolutionary search over code, machine-checkable fitness, frontier gains (first 4x4 matmul improvement in 56 years).

## Build It

`code/main.py` implements:

- A tiny ToT BFS on a stylized "pick arithmetic ops" task.
- A toy LATS MCTS loop on the same task (Select / Expand / Simulate / Backpropagate) with UCT selection.
- A value function that composes a symbolic score plus a self-eval score.

Run it:

```
python3 code/main.py
```

The trace shows ToT expanding three candidates per node with BFS, compared to LATS converging on the best rollout via MCTS. Token counts printed for both.

## Use It

LangGraph ships ToT-style exploration as subgraph patterns; the LangChain team's blog on LATS (May 2024) is the reference tutorial. LlamaIndex ships a `TreeOfThoughts` agent. For most 2026 production agents this pattern lives behind an `if task_complexity > threshold: use_search()` gate — see the evaluator-optimizer pattern in Lesson 05.

## Ship It

`outputs/skill-search-policy.md` selects between linear ReAct, ToT, LATS, and evolutionary search given task shape, budget, and evaluator fidelity.

## Exercises | 练习题

1. Run the toy LATS with UCT c=0.1 vs c=2.0. What changes in the trace?
   *用 UCT c=0.1 和 c=2.0 分别运行 LATS。轨迹有什么变化？*
2. Swap the value function for a noisier scorer (add random jitter). Does MCTS still find the best leaf? What is the minimum signal-to-noise it tolerates?
   *将价值函数替换为更嘈杂的评分器。MCTS 还能找到最佳叶节点吗？*
3. Implement beam-search ToT (keep top-k at each level) and compare to BFS. Which is better on a tight token budget?
   *实现 beam-search ToT（每层保留 top-k），与 BFS 对比。Token 预算紧张时哪个更好？*
4. Read LATS Section 5.1. Reproduce the HumanEval trajectory count: how many rollouts does it take to hit the reported pass@1?
   *阅读 LATS 第 5.1 节。重现 HumanEval 的轨迹数量。*
5. Read the LATS paper's discussion on "when LATS helps less." Write a one-paragraph decision rule mapping task shape to search strategy.
   *阅读 LATS 论文关于"何时 LATS 帮助不大"的讨论。写一段决策规则映射任务形状到搜索策略。*

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Tree of Thoughts | "Branching CoT" | Yao et al. — tree of thought nodes with self-evaluation | 思维树——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS | LATS——用 MCTS 统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" | Select formula balancing exploitation (Q) and exploration (ln N / n) | UCT——平衡利用和探索的选择公式 |
| Value function | "How good is this state" | Prompted LLM score or environment reward; feeds backprop | 价值函数——评估状态好坏 |
| Policy | "Action proposer" | ReAct-style generator; emits candidate next thoughts/actions | 策略——生成候选下一步行动 |
| Rollout | "Simulated trajectory" | Walk from a node to a leaf using policy, score with value | 模拟展开——从节点到叶节点的模拟轨迹 |
| Backpropagate | "Update ancestors" | Push the leaf's reward up the path, updating visit counts and Q | 反向传播——更新祖先节点的访问计数和价值 |
| Search cost | "Token explosion" | 100-1000x CoT on Game of 24; budget before you adopt | 搜索成本——Token 消耗是 CoT 的 100-1000 倍 |

## Further Reading

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) — the canonical paper
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) — MCTS with Reflexion feedback
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — subgraph patterns for search
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) — evolutionary search with programmatic evaluators
