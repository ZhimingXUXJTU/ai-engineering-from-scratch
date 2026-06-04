# 思维树与 LATS：深思熟虑的搜索

> 单条思维链没有回溯空间。ToT (Yao 等人, 2023) 将推理变为带有自评估的树结构，Game of 24 从 4% 提升到 74%。LATS (Zhou 等人, 2024) 统一了 ToT、ReAct 和 Reflexion，用蒙特卡洛树搜索实现，HumanEval 达到 92.7% pass@1。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**预计时间：** ~75 分钟

## 学习目标

- 将推理框架化为搜索：节点是"思维"，边是"扩展"，值是"多大希望"。
- 用标准库实现 ToT 风格的 BFS 树搜索，带自评估评分。
- 扩展为玩具 LATS MCTS 循环，包含选择/扩展/模拟/反向传播。
- 决定何时搜索值得付出 token 倍增的代价（Game of 24、代码生成），何时单条轨迹就够了（简单问答）。

## 问题引入

思维链是线性推进的——如果第一步错了，后面每一步都基于错误前提。Game of 24（用 + − × ÷ 对四个数字得到 24）上 GPT-4 CoT 只有 4% 准确率。模型在早期选择了错误的子表达式，无法恢复。

推理需要的是：提出多个候选方案、评估它们、选择有前景的、在死胡同时回溯。这就是搜索。Tree of Thoughts 和 LATS 是两种经典表述。

> **【中文解读】** 思维链是线性推进的——如果第一步错了，后面每一步都基于错误前提。Game of 24 上 GPT-4 CoT 只有 4% 准确率。推理需要的是：提出多个候选方案、评估它们、选择有前景的、在死胡同时回溯。这就是搜索。

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】** OpenAI o1/o3 系列模型的"深度思考"本质上就是搜索——在推理空间中探索多条路径，评估并选择最佳。ToT 和 LATS 是这种搜索范式的学术先驱。2026 年的 Coding Agent 在遇到复杂 bug 时也会启用类似搜索。

## 核心概念

### Tree of Thoughts (Yao 等人, NeurIPS 2023)

每个节点是一个连贯的中间步骤（"一个思维"）。每个节点可以扩展为 K 个子思维。LLM 对每个节点自评估打分。搜索探索树——BFS、DFS 或 beam。

自评估是承重部分。论文展示了三种变体：`sure / likely / impossible` 分类、`1..10` 数值评分、候选间投票。三种都在 Game of 24 上大幅击败 CoT（4% → 74%，使用 GPT-4）。

### LATS (Zhou 等人, ICML 2024)

LATS 用 MCTS 统一了 ToT、ReAct 和 Reflexion。LLM 扮演三个角色：

- **策略 (Policy)**：提出候选下一步行动（ReAct 风格）。
- **价值函数 (Value function)**：评分部分轨迹（ToT 风格自评估）。
- **自我反思器 (Self-Reflector)**：失败时写自然语言反思（Reflexion 风格），用于重新播种未来的模拟展开。

环境反馈（观察）混入价值函数，使搜索受真实工具结果而非仅模型意见指导。

### MCTS，最小化

每次迭代四个阶段：

1. **选择**——用 UCT（树的上置信界）从根走到叶节点。
2. **扩展**——用策略生成 K 个子节点。
3. **模拟**——从子节点用策略展开，用价值函数评分叶节点。
4. **反向传播**——更新路径上的访问计数和价值估计。

UCT 公式：`Q(s, a) + c * sqrt(ln N(s) / N(s, a))`。第一项是利用；第二项是探索。

### 成本现实

搜索会爆炸 Token。ToT 在 Game of 24 上消耗 CoT 的 100-1000 倍。LATS 类似。这不是免费的；将搜索留给以下场景：

- 单条轨迹明显不足的任务（Game of 24、复杂代码）。
- 正确性比挂钟时间更重要的任务。
- 有廉价可靠价值函数的任务（代码的单元测试、数学的明确目标）。

如果你的任务只有一个正确答案且评估器有噪声，搜索往往使情况更糟——它找到"高分但错误"的答案。

### 2026 年定位

大多数生产 Agent 不运行 LATS。它们运行带工具验证的 ReAct（CRITIC，第 05 课）。搜索出现在专业领域：

- 用测试作为价值函数的编码 Agent（HumanEval 风格）。
- 探索多条查询路径的深度研究 Agent。
- LangGraph 子图内的规划密集型工作流。

AlphaEvolve（第 11 课）是 2025 年的极端：代码的进化搜索、机器可检查的适应度、前沿突破（56 年来首个 4x4 矩阵乘法改进）。

## 动手实现

`code/main.py` 实现：

- 风格化"选择算术运算"任务上的微型 ToT BFS。
- 相同任务上的玩具 LATS MCTS 循环（选择/扩展/模拟/反向传播），带 UCT 选择。
- 组合符号分数加自评估分数的价值函数。

运行：

```
python3 code/main.py
```

## 用框架实现

LangGraph 将 ToT 风格探索作为子图模式提供。LlamaIndex 提供 `TreeOfThoughts` Agent。对于大多数 2026 年生产 Agent，该模式隐藏在 `if task_complexity > threshold: use_search()` 门之后——参见第 05 课的评估器-优化器模式。

## 产出物

`outputs/skill-search-policy.md` 根据任务形状、预算和评估器保真度在线性 ReAct、ToT、LATS 和进化搜索之间选择。

## 练习题

1. 用 UCT c=0.1 和 c=2.0 分别运行 LATS。轨迹有什么变化？
2. 将价值函数替换为更嘈杂的评分器（添加随机抖动）。MCTS 还能找到最佳叶节点吗？它容忍的最小信噪比是多少？
3. 实现 beam-search ToT（每层保留 top-k），与 BFS 对比。Token 预算紧张时哪个更好？
4. 阅读 LATS 第 5.1 节。重现 HumanEval 的轨迹数量。
5. 阅读 LATS 论文关于"何时 LATS 帮助不大"的讨论。写一段决策规则映射任务形状到搜索策略。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Tree of Thoughts（思维树） | 带自评估的思维节点树 |
| LATS | 用 MCTS 统一 ToT + ReAct + Reflexion |
| UCT | 平衡利用和探索的选择公式 |
| Value function（价值函数） | 评估状态好坏 |
| Policy（策略） | 生成候选下一步行动 |
| Rollout（模拟展开） | 从节点到叶节点的模拟轨迹 |
| Backpropagate（反向传播） | 更新祖先节点的访问计数和价值 |
| Search cost（搜索成本） | Token 消耗是 CoT 的 100-1000 倍 |

## 延伸阅读

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601)
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131)
