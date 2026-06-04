# 自我精炼与 CRITIC：迭代式输出改进

> Self-Refine (Madaan 等人, 2023) 让一个 LLM 扮演三个角色——生成、反馈、精炼——循环改进。7 个任务平均提升 20 个百分点。CRITIC (Gou 等人, 2023) 将验证步骤通过外部工具（搜索、代码解释器、计算器）进行强化。2026 年这已成为每个框架的标配——Anthropic 称为"评估器-优化器"，OpenAI Agents SDK 称为"输出护栏"。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**预计时间：** ~60 分钟

## 学习目标

- 掌握 Self-Refine 的三个提示（生成、反馈、精炼），并解释为什么历史对精炼提示至关重要。
- 解释 CRITIC 的关键洞察：LLM 在没有外部验证的情况下自我验证不可靠。
- 用标准库实现带历史和可选外部验证器的 Self-Refine 循环。
- 将此模式映射到 Anthropic 的"评估器-优化器"工作流和 OpenAI Agents SDK 的输出护栏。

## 问题引入

Agent 产出了几乎正确的答案。可能一行代码有语法错误。可能摘要太长。可能计划遗漏了边界情况。你想要的是：Agent 批评自己的输出，然后修复它。

Self-Refine 证明了这在单一模型、无需训练数据、无需 RL 的情况下可行。但有一个陷阱：LLM 在硬事实上自我验证不可靠。CRITIC 命名了修复方案——通过外部工具（搜索、代码解释器、计算器、测试运行器）路由验证步骤。

两者共同定义了 2026 年的迭代改进标准：生成 → 验证（尽可能外部验证）→ 精炼 → 验证通过则停止。

> **【拓展：CRITIC → Claude Code 的自我修复】** Claude Code 在编写代码后会自动运行测试验证——这就是 CRITIC 模式的生产实现。当测试失败时，它基于错误反馈修正代码，直到测试通过。

## 核心概念

### Self-Refine (Madaan 等人, NeurIPS 2023)

一个 LLM，三个角色：

```
generate(task)            -> output_0       # 生成初始输出
feedback(task, output_0)  -> critique_0     # 自我批评
refine(task, output_0, critique_0, history) -> output_1  # 根据批评精炼
...                                           # 循环
stop when feedback says "no issues" or budget exhausted.  # 停止条件
```

关键细节：`refine` 看到完整历史——所有先前输出和批评——所以它不会重复错误。论文消融了这一点：去掉历史，质量急剧下降。

标题数据：在 7 个任务（数学、代码、缩写、对话）上平均 +20 个百分点绝对提升，包括 GPT-4。无需训练，无需外部工具，单一模型。

### CRITIC (Gou 等人, arXiv:2305.11738, v4 2024 年 2 月)

Self-Refine 的弱点：反馈步骤是 LLM 评分自己。对于事实性声明，这不可靠（幻觉对产生它的模型来说往往看起来有说服力）。CRITIC 将 `feedback(task, output)` 替换为 `verify(task, output, tools)`，其中 `tools` 包括：

- 搜索引擎验证事实
- 代码解释器验证代码
- 计算器验证算术
- 领域验证器（单元测试、类型检查器、linter）

验证器产生基于工具结果的结构化批评。精炼器然后基于此批评进行条件化。

标题数据：CRITIC 在事实性任务上优于 Self-Refine，因为批评有根基。在没有外部验证器的任务上（创意写作、格式化），CRITIC 退化为 Self-Refine。

### 停止条件

两种常见形式：

1. **验证器通过。** 外部测试返回成功。有则首选（单元测试、类型检查器、护栏断言）。
2. **无反馈发出。** 模型说"输出没问题"。更便宜但不可靠；配合最大迭代上限。

2026 年默认做法：组合两者。"验证器通过或模型说没问题且迭代 >= 2 或迭代 >= 最大迭代次数时停止。"

### 2026 年陷阱

- **橡皮图章循环。** 同一模型用相同提示风格做生成和批评，收敛于"看起来没问题"。使用结构不同的提示，或更小更便宜的模型做批评。
- **过度精炼。** 每次精炼轮次增加延迟和 token。预算 1-3 轮；之后升级到人工审查。
- **在简单任务上用 CRITIC。** 如果没有外部验证器，CRITIC 退化为 Self-Refine；不要为桩验证器付出延迟代价。

## 动手实现

`code/main.py` 在玩具任务上实现 Self-Refine 和 CRITIC：给定主题生成短要点列表。验证器检查格式（3 个要点，每个不超过 60 字符）。CRITIC 添加外部"事实验证器"，惩罚已知幻觉。

运行：

```
python3 code/main.py
```

## 用框架实现

Anthropic 的评估器-优化器是此模式的 Claude 友好语言。OpenAI Agents SDK 的输出护栏是 CRITIC 形式（护栏可以调用工具）。LangGraph 提供类似 Self-Refine 的反思节点。Google 的 Gemini 2.5 Computer Use 添加了每步安全评估器——这是 CRITIC 变体：每个行动在提交前都经过验证。

## 产出物

`outputs/skill-refine-loop.md` 根据任务形状、验证器可用性和迭代预算配置评估器-优化器循环。输出生成器、评估器/验证器和优化器的提示，加上停止策略。

## 练习题

1. 用 max_iterations=1 运行。CRITIC 仍然有帮助吗？
2. 将外部验证器替换为嘈杂的版本（30% 误报）。循环会做什么？这是 2026 年大多数护栏栈的现实。
3. 实现"不同模型的生成-批评"变体：大模型生成，小模型批评。比同模型更好吗？
4. 阅读 CRITIC 第 3 节 (arXiv:2305.11738 v4)。说出三种验证工具类别并各举一例。
5. 将 OpenAI Agents SDK 的 `output_guardrails` 映射到 CRITIC 的验证器角色。SDK 哪里做得好，哪里不够？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Self-Refine（自我精炼） | 一个模型内的生成→反馈→精炼循环 |
| CRITIC | 用外部工具替代自我反馈 |
| Evaluator-Optimizer（评估器-优化器） | Anthropic 的工作流模式 |
| Output guardrail（输出护栏） | Agent 输出后的验证器 |
| Verify step（验证步骤） | 基于外部工具还是自我评价 |
| Refine history（精炼历史） | 之前输出和批评的记录 |
| Rubber-stamp loop（橡皮图章循环） | 自我认同导致无法发现问题 |
| Stop condition（停止条件） | 验证通过或达到迭代上限 |

## 延伸阅读

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651)
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738)
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)
