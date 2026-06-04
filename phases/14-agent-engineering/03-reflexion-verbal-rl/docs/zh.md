# Reflexion：语言强化学习

> 基于梯度的 RL 需要数千次试验和 GPU 集群。Reflexion (Shinn 等人, NeurIPS 2023) 用自然语言实现自我改进：每次失败后，Agent 写一段反思存入情景记忆，下一次尝试时参考这些记忆。这正是 Letta 的 sleep-time compute、Claude Code 的 CLAUDE.md 学习机制背后的模式。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**预计时间：** ~60 分钟

## 学习目标

- 掌握 Reflexion 的三个组件（执行器 Actor、评估器 Evaluator、自我反思器 Self-Reflector）和情景记忆的作用。
- 用标准库实现带二元评估器、反思缓冲区和全新重试的 Reflexion 循环。
- 为给定任务在标量、启发式和自评估反馈源之间做出选择。
- 解释为什么语言强化能捕捉到基于梯度的 RL 需要数千次试验才能修复的错误。

## 问题引入

Agent 执行任务失败。在标准 RL 中，你需要运行数千次更多试验、计算梯度、更新权重。昂贵、缓慢，大多数生产 Agent 没有针对每次失败的训练预算。

Reflexion (Shinn 等人, arXiv:2303.11366) 提出了不同的问题：如果 Agent 只是思考一下为什么失败，然后在下一次尝试的提示中带上这个思考呢？无需权重更新。无需梯度。只需在试验间存储自然语言。

结果：在 ALFWorld 上超越 ReAct 和其他非微调基线。在 HotpotQA 上改进 ReAct。在代码生成 (HumanEval/MBPP) 上达到当时的 SOTA。所有这些不需要一个梯度步骤。

## 核心概念

### 三个组件

```
执行器：生成行动轨迹（ReAct 风格循环）
评估器：评分轨迹——二元、启发式或自评估
自我反思器：写关于失败的自然语言反思
```

加上一个数据结构：

```
情景记忆：先前反思列表，前置到下一次试验的提示
```

一次试验运行执行器。评估器评分。如果分数低，自我反思器产生一段反思（"我选错了工具，因为我把问题误解为关于 X 而实际上是关于 Y"）。反思进入情景记忆。下一次试验重新开始但能看到反思。

### 三种评估器类型

1. **标量**——外部二元信号。ALFWorld 成功或失败。HumanEval 测试通过或失败。最简单、信号最强。
2. **启发式**——预定义的失败特征。"如果 Agent 连续两次产生相同行动，标记为卡住。""如果轨迹超过 50 步，标记为低效。"
3. **自评估**——LLM 评分自己的轨迹。在没有真值时需要。信号较弱；与工具验证配合使用效果好（第 05 课——CRITIC）。

2026 年的默认做法是混合：有标量时用标量，没有时用自评估，启发式作为安全护栏。

### 为什么这能泛化

Reflexion 与其说是一种新算法，不如说是一个命名模式。几乎所有生产环境的"自我修复"Agent 都运行某种变体：

- Letta 的 sleep-time compute（第 08 课）：独立 Agent 反思过去的对话并写入记忆块。
- Claude Code 的 `CLAUDE.md` / "save memory" 模式：反思被捕获为学习经验，前置到未来会话。
- LangGraph 的反思节点：一个评分输出并在需要时路由到精炼的节点。

所有这些都源自相同的洞察：自然语言是足够丰富的媒介，能跨运行传递"我从失败中学到了什么"。

> **【拓展：Reflexion → 生产环境的自我修复】** 几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体：Letta 的 sleep-time compute 异步反思、Claude Code 的 CLAUDE.md 存储学习经验、LangGraph 的反思节点。核心洞察相同：自然语言足够承载"从失败中学到了什么"。

### 何时有效，何时无效

Reflexion 在以下情况有效：

- 有明确的失败信号（测试失败、工具错误、错误答案）。
- 任务类别可重现（可以再次提出相同类型的问题）。
- 反思有改进轨迹的空间（足够的行动预算）。

Reflexion 在以下情况无帮助：

- Agent 首次就成功。
- 失败是外部的（网络断开、工具损坏）——反思"网络断开了"对未来运行没有帮助。
- 反思变成迷信——存储关于一次性不稳定运行的叙事。

2026 年的陷阱：记忆腐化。反思不断积累；部分已过时或错误；随着情景缓冲区增长，重运行变慢。缓解措施：定期压缩（第 06 课）、反思的 TTL、或独立的异步清理 Agent (Letta)。

## 动手实现

`code/main.py` 在一个玩具谜题上实现 Reflexion：产生一个 3 元素列表使其和等于目标值。执行器输出候选列表；评估器检查总和；自我反思器写一行关于哪里出错的描述。反思进入下一次试验的情景记忆。

运行：

```
python3 code/main.py
```

轨迹显示三次试验。试验 1 失败，存储反思，试验 2 看到反思并改进但仍然失败，试验 3 成功。与基线运行（无反思）比较——它卡在试验 1 的答案上。

## 用框架实现

LangGraph 将反思作为节点模式提供。Claude Code 的 `/memory` 命令和 pro-workflow 的 `/learn-rule` 将情景缓冲区外部化为 markdown 文件。Letta 的 sleep-time compute 在空闲时运行自我反思器，使主 Agent 保持延迟受限。OpenAI Agents SDK 不直接提供 Reflexion；你用自定义 Guardrail（按分数拒绝轨迹）和跨运行存活的记忆 `Session` 来构建。

## 产出物

`outputs/skill-reflexion-buffer.md` 创建并维护带有反思捕获、TTL 和去重的情景缓冲区。给定任务类别和失败，它产出真正帮助下一次试验的反思（而不是通用的"要更小心"）。

## 练习题

1. 将评估器从二元切换为返回距离度量的标量评估器。收敛更快吗？
2. 给反思添加 10 次试验的 TTL。更早的反思在之后是有害还是有益？
3. 实现启发式评估器：重复相同行动时标记为卡住。这与自我反思器如何交互？
4. 用忽略反思的对抗性执行器运行 Reflexion。最少需要什么提示工程才能迫使执行器注意到反思？
5. 阅读 Reflexion 论文第 4 节关于 AlfWorld 的内容。概念上重现 130% 成功率改进：相比原始 ReAct 的关键差异是什么？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Reflexion（反思） | 执行器 + 评估器 + 自我反思器 + 情景记忆 |
| Verbal reinforcement（语言强化） | 无需梯度的自然语言学习 |
| Episodic memory（情景记忆） | 按任务类别存储的反思缓冲区 |
| Scalar evaluator（标量评估器） | 来自真值的二元/数值评分 |
| Heuristic evaluator（启发式评估器） | 预定义的失败模式检测 |
| Self-evaluator（自评估器） | LLM 评价自身轨迹 |
| Memory rot（记忆腐化） | 情景缓冲区填满过时条目 |
| Sleep-time reflection（异步反思） | 在非关键路径上运行反思 |

## 延伸阅读

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366)
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute)
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
