# 自主编码 Agent 全景（2026 年）

> SWE-bench Verified 在不到三年内从 4% 提升到 80.9%。相同的 Claude Sonnet 4.5 在 SWE-agent v1 上得分 43.2%，在 Cline 自主模式下得分 59.8%——模型周围的脚手架现在和模型本身一样重要。OpenHands（原 OpenDevin）是最活跃的 MIT 许可平台，其 CodeAct 循环直接在沙箱中执行 Python 操作而非 JSON 工具调用。头条数字隐藏了一个方法论问题：500 个 SWE-bench Verified 任务中有 161 个只需要 1-2 行修改，而 SWE-bench Pro（10+ 行修改的任务）对相同的前沿模型在 23-59% 的范围。

**类型：** 学习
**语言：** Python（标准库，CodeAct vs JSON 工具调用对比）
**前置条件：** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**时间：** ~45 分钟

## 问题引入

> **【中文解读】** 编码 Agent 景观是 2025-2026 年变化最快的 AI 应用领域之一。主要玩家包括 Claude Code、Cursor、GitHub Copilot、Devin、Windsurf 等。关键差异化因素：(1) 自主性级别——从补全建议到完全自主编码；(2) 上下文管理——如何处理大型代码库；(3) 工具集成——支持哪些开发工具。

> **【拓展：coding agent landscape】** 2026年编码 Agent 的竞争格局：(1) Claude Code——Anthropic 的自主编码 Agent，支持全栈开发、Git 操作和终端命令执行；(2) Cursor——基于 VS Code 的 AI 编辑器，强调人机协作；(3) Devin——Cognition AI 的全自主编码 Agent，可以独立完成开发任务；(4) Windsurf（原 Codeium）——AI 优先的 IDE。SWE-bench 上的表现是主要竞争指标。

"哪个编码 Agent 最好"是错误的问题。正确的问题是：在匹配我工作的任务分布上，使用我将在生产中运行的脚手架，我能获得什么端到端可靠性？

在 2022 到 2026 年间，该领域学到了脚手架 (scaffolding)——检索层、规划器、沙箱、编辑-验证循环、反馈格式——是承重的。Claude Sonnet 4.5 在 SWE-agent v1 上 SWE-bench Verified 得分 43.2%；同一模型在 Cline 的自主脚手架中得分 59.8%。16.6 个百分点的绝对差异，相同的权重。基础模型是一个组件；循环才是产品。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

伴随的问题是基准饱和隐藏了回归。SWE-bench Verified 接近饱和，简单任务尾部（500 个任务中有 161 个需要 <=2 行）拉高了顶级分数。真实世界的质量更好地在 SWE-bench Pro（10+ 行修改）等分布上衡量，相同的领先者仍处于 23-59% 的范围。

## 核心概念

### SWE-bench，一段话讲清楚

SWE-bench（Jimenez 等人）取真实的 GitHub issue 及其 ground-truth 补丁，要求 Agent 生成使测试套件通过的补丁。SWE-bench Verified（OpenAI，2024）是一个人工策划的 500 个任务子集，移除了模糊和损坏的任务。SWE-bench Pro 是更难的继任者——需要 10+ 行修改的任务，当前前沿 Agent 在 23-59%。

### 2022 → 2026 曲线实际展示的内容

- **2022 年**：研究模型在原始 SWE-bench 上约 4%。
- **2024 年**：GPT-4 + Devin 式脚手架约 14%；SWE-agent 约 12%。
- **2025 年**：Claude 3.5/3.7 Sonnet 在 Aider 和 SWE-agent 中推入 40-55% 范围。
- **2026 年**：Claude Sonnet 4.5 和前沿竞争者在 SWE-bench Verified 上 70-80%+。Epoch AI 的排行榜实时跟踪。

斜率来自三个复合来源：更好的基础模型、更好的脚手架（CodeAct、反思、验证器循环）和更好的基准（Verified 移除了噪声）。

### CodeAct vs JSON 工具调用

OpenHands（All-Hands-AI，arXiv:2407.16741，原 OpenDevin）做了一个具体的架构赌注：不是模型发出 JSON 工具调用由宿主解码执行，而是模型发出 Python 代码，由 Jupyter 风格内核在沙箱中运行。Agent 可以在一个操作中循环文件、链式调用工具并捕获自己的异常。

权衡：

- **JSON 工具调用**：每个操作是一轮；容易审计；有限的组合性；默认安全，因为每个调用都经过显式验证器。
- **CodeAct**：一个操作可以是一个完整的程序；可组合；需要加固的沙箱（OpenHands 使用 Docker 隔离）；失败模式包括沙箱运行时允许的任何内容。

两种架构都在生产中。CodeAct 在开放平台中占主导（OpenHands、smolagents）。JSON 工具调用在托管服务中仍占主导（Anthropic Managed Agents、OpenAI Assistants），其中提供商控制执行器。

### 2026 年全景中的脚手架

| 脚手架 | 许可证 | 执行模型 | 显著特性 |
|---|---|---|---|
| OpenHands (OpenDevin) | MIT | Docker 中的 CodeAct | 最活跃的开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | 本地仓库中的 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | 专有 | 托管 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### 为什么脚手架占主导

编码运行是一个长程轨迹（第 1 课）。可靠性在步骤间复合。脚手架在三个地方赚取分数：

1. **检索**：找到正确的文件读取是静默瓶颈。SWE-agent 的 ACI、OpenHands 的文件索引和 Aider 的仓库地图都在攻击这个问题。
2. **验证器循环**：运行测试、阅读堆栈跟踪和重试在 SWE-bench 上是 10+ 个百分点的差异。
3. **失败遏制**：出错时回滚的沙箱防止复合损害。相同模型有和没有验证器循环看起来像两个不同的产品。

### 基准饱和和真实分布

OpenHands 作者和 Epoch AI 都指出 SWE-bench Verified 有一个简单尾部：500 个任务中有 161 个只需要 1-2 行修改。高分部分由这个尾部驱动。SWE-bench Pro 限制在 10+ 行修改，即使前沿系统也返回 23-59% 的分数。你的生产分布几乎可以肯定更接近 Pro 而不是 Verified。

选择 Agent 的含义：在你自己的 bug 积压中运行一个类似 Pro 的子集。重要的分数是在代表你发布内容的任务上的分数。

## 用框架实现

`code/main.py` 在固定的迷你任务分布上比较两个玩具 Agent 脚手架：

1. 一个**JSON 工具调用**脚手架，每轮采取一个操作。
2. 一个**CodeAct**脚手架，每个操作可以发出一个小的 Python 代码片段。

两者都使用存根"模型"（确定性规则），因此比较将脚手架与模型质量隔离。输出显示 CodeAct 脚手架在更少轮次中解决更多任务，代价是更大的每操作爆炸半径。

## 产出物

`outputs/skill-scaffold-audit.md` 帮助你在采用前审计一个提议的编码 Agent 脚手架：检索质量、验证器存在、沙箱隔离和基准到分布的匹配度。

## 练习题

1. 运行 `code/main.py`。每个脚手架在相同任务集上需要多少轮？每个的每操作爆炸半径是多少？
   *思考并实践此练习*

2. 阅读 OpenHands 论文（arXiv:2407.16741）。论文论证 CodeAct 在复杂任务上优于 JSON 工具调用。识别论文承认的一个失败模式，并写一句话说明该模式何时会在生产中占主导。
   *思考并实践此练习*

3. 从你的 bug 积压中选择一个需要跨两个文件修改 10+ 行的任务。估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率。论证差距。
   *思考并实践此练习*

4. SWE-bench Verified 有 161 个单文件、1-2 行修改的任务。构建一个排除它们的评分。排行榜如何重新洗牌？
   *思考并实践此练习*

5. 阅读"Introducing SWE-bench Verified"（OpenAI）。解释用于移除模糊任务的具体方法论，并命名策划会遗漏的一个类别。
   *思考并实践此练习*

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|---|---|---|
| SWE-bench | "编码基准" | 带有 ground-truth 补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "清理后的子集" | 500 个人工策划的任务，简单尾部存在 |
| SWE-bench Pro | "更难的子集" | 10+ 行修改；前沿在 23-59% |
| CodeAct | "代码即操作" | Agent 发出 Python；Jupyter 风格内核在沙箱中执行 |
| JSON 工具调用 (JSON Tool Call) | "函数调用" | 每个操作是执行前验证的结构化 JSON 载荷 |
| 脚手架 (Scaffold) | "Agent 框架" | 基础模型周围的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent 的格式" | 为 LLM 人体工程学设计的命令集，不是人类 shell |
| 验证器循环 (Verifier Loop) | "测试并重试" | 运行测试、读输出、修改补丁；最大的非模型可靠性增益 |

## 延伸阅读

- [Jimenez 等人 — SWE-bench](https://www.swebench.com/) — 原始基准和方法论。
- [OpenAI — 介绍 SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — 策划子集如何构建。
- [Wang 等人 — OpenHands：AI 软件开发者的开放平台](https://arxiv.org/abs/2407.16741) — CodeAct 架构和事件流设计。
- [Epoch AI — SWE-bench 排行榜](https://epoch.ai/benchmarks) — 实时跟踪的分数。
- [Anthropic — 测量 Agent 自主性](https://www.anthropic.com/research/measuring-agent-autonomy) — 长程编码 Agent 可靠性框架。
