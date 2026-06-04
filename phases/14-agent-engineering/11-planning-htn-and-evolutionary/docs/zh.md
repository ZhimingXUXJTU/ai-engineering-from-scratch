# HTN 与进化搜索规划

> 符号规划处理计划可证明正确的情况。进化代码搜索处理适应度函数可机器检查的情况。ChatHTN (2025) 和 AlphaEvolve (2025) 展示了各自与 LLM 配对时释放了什么。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 02 (ReWOO 和计划-执行)
**预计时间：** ~75 分钟

## 学习目标

- 解释分层任务网络 (Hierarchical Task Networks)：任务、方法、操作符、前置条件、效果。
- 描述 ChatHTN 的混合循环——符号搜索配合 LLM 回退分解。
- 解释 AlphaEvolve 的进化循环以及为什么它只在有程序化评估器时有效。
- 用标准库实现玩具 HTN 规划器和玩具进化搜索。

## 问题引入

ReWOO（第 02 课）、Plan-and-Execute 和 ReAct 覆盖了大多数 Agent 规划。两种它们覆盖不好的情况：

1. **可证明正确性的计划。** 调度、飞行路线、合规工作流——计划必须在构造上正确。
2. **有机器可检查适应度函数的优化。** 矩阵乘法、调度启发式、编译器 pass——目标不是“一个正确的计划”而是“最好的计划”。

## 核心概念

详见英文版本 en.md 中的完整内容。以下为关键概念的中文摘要：

### 分层任务网络 (HTN)

- **任务**——复合（待分解）和原语（可直接执行）。
- **方法**——将复合任务分解为子任务的方式，带前置条件。
- **操作符**——带前置条件和效果的原语操作。
- **状态**——一组事实。

### ChatHTN

交替符号 HTN 与 LLM 查询：尝试用现有方法分解复合任务，如果没有方法适用则询问 LLM。核心主张：每个产出的计划都是可证明正确的。

### AlphaEvolve

Gemini 2.0 Flash/Pro 集群编排的进化代码搜索。56 年来首个 4x4 矩阵乘法改进。硬约束：适应度函数必须可机器检查。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| HTN | 带操作符、前置条件、效果的任务分解 |
| ChatHTN | 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | 集群 LLM 变异代码；确定性评估器选择 |
| Fitness function（适应度函数） | 输出上的确定性、机器可检查的分数 |

## 延伸阅读

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814)
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131)
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
