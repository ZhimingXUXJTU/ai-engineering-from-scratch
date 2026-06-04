# ReWOO 与计划-执行模式：解耦规划

> ReAct 在一个流中交替思考和行动。ReWOO 将它们分离：先一次性制定完整计划，然后执行。Token 消耗减少 5 倍，HotpotQA 准确率提升 4%，还可以将规划器蒸馏到 7B 模型。Plan-and-Execute 是其泛化版本，Plan-and-Act 将其扩展到网页导航。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环)
**预计时间：** ~60 分钟

## 学习目标

- 解释为什么 ReWOO 的规划器 (Planner) / 工作器 (Worker) / 求解器 (Solver) 分裂比 ReAct 的交替循环更节省 token 且更健壮。
- 用标准库实现计划 DAG、依赖排序执行器和组合工作器输出的求解器。
- 使用 2026 年"五种工作流模式"框架 (Anthropic) 判断任务应该运行计划-执行还是交替 ReAct。
- 识别何时需要 Plan-and-Act 的合成计划数据来处理长程网页或移动任务。

## 问题引入

ReAct 的交替思考-行动-观察循环简单灵活，但每次工具调用都需要携带完整的历史上下文——包括之前所有的思考。Token 用量随深度二次增长。更糟糕的是：当循环中途工具失败时，模型必须从错误观察中重新推导整个计划。

ReWOO (Xu 等人, arXiv:2305.18323, 2023 年 5 月) 注意到了这一点并做了一个选择：先规划整个任务，并行获取证据，最后组合答案。一次 LLM 调用规划，N 次工具调用获取证据（可并行），一次 LLM 调用求解。权衡是灵活性降低（计划是静态的），但换来更好的 Token 效率和更清晰的失败模式。

> **【中文解读】** ReAct 的交替循环虽然简单灵活，但每次工具调用都需要携带完整的历史上下文，Token 用量随深度二次增长。ReWOO 的方案是：先一次性规划，然后并行获取证据，最后组合答案。代价是灵活性降低（计划是静态的），但换来更好的 Token 效率和更清晰的失败模式。

## 核心概念

### 三个角色

```
规划器：将用户问题转为计划 DAG
工作器：执行工具调用获取证据（可并行）
求解器：组合证据生成最终答案
```

规划器产生一个 DAG。每个节点命名一个工具、其参数以及它依赖的先前节点（用 `#E1`、`#E2` 等引用）。工作器按拓扑顺序执行节点。求解器将所有内容缝合在一起。

### 为什么节省 5 倍 Token

ReAct 的提示长度随步数线性增长。到第 10 步时，提示包含思考 1 + 行动 1 + 观察 1 + 思考 2 + 行动 2 + 观察 2，依此类推。每个中间步骤还冗余地包含原始提示。

ReWOO 需要：一次规划器提示（较大）、N 个小工作器提示（每个仅包含工具调用，无链）、一次求解器提示。在 HotpotQA 上论文测量约减少 5 倍 token，同时准确率提升 4 个百分点。

### 规划器蒸馏

论文的第二个成果：因为规划器不需要观察结果，可以将 175B 教师模型的规划输出蒸馏到 7B 模型。小模型负责规划；推理时不需要大模型。这已成为标准——许多 2026 年的生产 Agent 使用小规划器 + 大执行器，反之亦然。

> **【拓展：规划器蒸馏 → 成本优化】** 因为规划器不需要观察结果，可以将 175B 教师模型的规划输出蒸馏到 7B 模型。2026 年的生产 Agent 普遍使用"小模型规划 + 大模型执行"的混合架构来优化成本。这也是 vLLM 等推理服务支持模型路由的理论基础。

### Plan-and-Execute (LangChain, 2023)

LangChain 团队 2023 年 8 月的博文将 ReWOO 泛化为一个模式名称：Plan-and-Execute。前置规划器输出步骤列表，执行器运行每步，可选的重新规划器可以在观察结果后修改计划。这比 ReWOO 更接近 ReAct（重新规划器将观察带回规划），但保留了 token 节省。

### Plan-and-Act (Erdogan 等人, arXiv:2503.09572, ICML 2025)

Plan-and-Act 将该模式扩展到长程网页和移动 Agent。关键贡献是合成计划数据：标注轨迹生成器产生计划显式的训练数据。用于微调规划器模型，使其在 WebArena 类任务中能持续工作超过 30-50 步（单个 ReAct 轨迹会失去连贯性）。

### 何时选择哪种模式

| 模式 | 适用场景 |
|------|----------|
| ReAct | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | 长程任务 (>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | 值得付出搜索成本的场景（第 04 课） |

Anthropic 2024 年 12 月的指导：从最简单的开始。如果任务是一次工具调用加摘要，不要构建 ReWOO。如果任务是 40 步的研究作业，不要只用 ReAct。

## 动手实现

`code/main.py` 实现了一个玩具 ReWOO：

- `Planner`——从提示生成计划 DAG 的脚本策略。
- `Worker`——通过注册表分派每个节点的工具调用。
- `Solver`——读取证据并生成最终答案的脚本组合器。
- 依赖解析——`#E1` 等引用替换为先前工作器输出。

演示回答"法国首都的人口是多少，四舍五入到百万？"使用两步计划：(1) 查找首都，(2) 查找人口，然后求解。

运行：

```
python3 code/main.py
```

## 用框架实现

LangGraph 提供 Plan-and-Execute 作为配方。CrewAI 的 Flows 直接编码了该模式：你预先定义任务，Flow DAG 执行它们。Plan-and-Act 的合成数据方法目前主要在研究领域；运行时模式（显式计划 DAG）通过 LangGraph 和 CrewAI Flows 投入生产。

## 产出物

`outputs/skill-rewoo-planner.md` 从用户请求和工具目录生成 ReWOO 计划 DAG。它在交给执行器之前验证计划（无环、每个引用已解析、每个工具存在）。

## 练习题

1. 将独立计划节点的工作器并行化。在 6 节点 DAG 中 2 组并行的情况下有什么收益？
2. 添加一个在工作器返回错误时触发的重新规划节点。ReWOO 变成 Plan-and-Execute 的最小改动是什么？
3. 用小模型 (7B) 替换规划器，保留前沿模型作为求解器。对比端到端质量——分裂在哪里失败？
4. 阅读 ReWOO 论文第 4 节关于规划器蒸馏的内容。概念上重现 175B→7B 结果：需要什么训练数据？如何评估计划质量？
5. 将玩具系统移植为 Plan-and-Act 的轨迹形式：计划是序列而非 DAG。哪些权衡发生了变化？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| ReWOO | 无观察推理——规划时不依赖观察结果 |
| Plan-and-Execute | 带可选重新规划的 ReWOO |
| Plan-and-Act | 使用合成计划训练数据的长程任务模式 |
| Evidence reference（证据引用） | 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation（规划器蒸馏） | 用大模型的规划输出训练小模型 |
| Token efficiency（Token 效率） | 比 ReAct 减少 5 倍 Token |
| DAG executor（DAG 执行器） | 按依赖顺序运行计划节点 |

## 延伸阅读

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323)
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572)
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview)
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
