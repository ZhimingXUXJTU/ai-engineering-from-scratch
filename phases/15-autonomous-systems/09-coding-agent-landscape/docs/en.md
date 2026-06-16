# The Autonomous Coding Agent Landscape (2026) | 自主编码 Agent 全景（2026）

> SWE-bench Verified went from 4% to 80.9% in under three years. Same Claude Sonnet 4.5 scored 43.2% on SWE-agent v1 and 59.8% on Cline autonomous — the scaffolding around the model now matters as much as the model itself. OpenHands (formerly OpenDevin) is the most active MIT-licensed platform and its CodeAct loop executes Python actions directly in a sandbox instead of JSON tool calls. The headline numbers hide a methodological issue: 161 of 500 SWE-bench Verified tasks require only a 1–2 line change, and SWE-bench Pro (10+ line tasks) sits at 23–59% for the same frontier models.

> **【中文解读】** SWE-bench Verified 在不到三年从 4% 升到 80.9%。同一 Claude Sonnet 4.5 在 SWE-agent v1 上得 43.2%，在 Cline autonomous 上得 59.8%——模型周围的脚手架现在和模型本身一样重要。OpenHands（前 OpenDevin）是最活跃的 MIT 许可平台，其 CodeAct 循环直接在沙箱中执行 Python 动作而非 JSON 工具调用。标题数字隐藏了方法论问题：500 个 SWE-bench Verified 任务中 161 个仅需 1-2 行变更，SWE-bench Pro（10+ 行任务）同一前沿模型只有 23-59%。

> **【拓展：脚手架 > 模型】** 2022-2026 的曲线表明编码 Agent 的能力提升有三个复合来源：更好的基础模型、更好的脚手架（CodeAct、反思、验证器循环）、更好的基准（Verified 去除噪声）。同等模型在不同脚手架下分数差 16.6 个绝对点——基础模型是组件，循环才是产品。这就是为什么选 Agent 不能只看模型排行榜。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·07（工具调用）、Phase 14·30+（工作台 Agent 实践）、Phase 15·01（长程 Agent）。本节是 2026 年编码 Agent 全景图——选型必读。
> 💡 **【类比】** 选编码 Agent = "选车"而不是"选发动机"。同一发动机（Claude Sonnet 4.5）装在不同车上（SWE-agent vs Cline）速度差 16 个百分点。脚手架（检索层、规划器、沙箱、edit-verify 循环）才是产品，模型只是组件。所以不要只看模型排行榜，要看"我的任务+我的脚手架"的端到端可靠性。
> ⚠️ **【易错点】** 看 SWE-bench Verified 分数选 Agent = 被基准骗了。500 个任务里 161 个只需 1-2 行修改（容易），看 SWE-bench Pro（10+ 行真实任务）分数才有参考价值。修复：选 Agent 前用自己代码库的真实 issue 测试，而不是看营销基准。

## The Problem | 问题引入

> **【中文解读】** 编码 Agent 景观是 2025-2026 年变化最快的 AI 应用领域之一。主要玩家包括 Claude Code、Cursor、GitHub Copilot、Devin、Windsurf 等。关键差异化因素：(1) 自主性级别——从补全建议到完全自主编码；(2) 上下文管理——如何处理大型代码库；(3) 工具集成——支持哪些开发工具。

> **【拓展：coding agent landscape】** 2026年编码 Agent 的竞争格局：(1) Claude Code——Anthropic 的自主编码 Agent，支持全栈开发、Git 操作和终端命令执行；(2) Cursor——基于 VS Code 的 AI 编辑器，强调人机协作；(3) Devin——Cognition AI 的全自主编码 Agent，可以独立完成开发任务；(4) Windsurf（原 Codeium）——AI 优先的 IDE。SWE-bench 上的表现是主要竞争指标。

"Which coding agent is best" is the wrong question. The right question is: on a task distribution that matches my work, with the scaffolding I will run in production, what end-to-end reliability do I get?

> "哪个编码 Agent 最好"是错误的问题。正确的问题是：在与我的工作匹配的任务分布上，使用我将在生产中运行的脚手架，我能获得什么端到端可靠性？

Between 2022 and 2026 the field learned that scaffolding — the retrieval layer, the planner, the sandbox, the edit-verify loop, the feedback format — is load-bearing. Claude Sonnet 4.5 on SWE-agent v1 scored 43.2% on SWE-bench Verified; the same model inside Cline's autonomous scaffold scored 59.8%. 16.6 absolute points of difference, same weights. The base model is a component; the loop is the product.

> 2022 到 2026 年间，领域学到脚手架——检索层、规划器、沙箱、编辑-验证循环、反馈格式——是承重的。Claude Sonnet 4.5 在 SWE-agent v1 上 SWE-bench Verified 得 43.2%；同一模型在 Cline 自主脚手架内得 59.8%。相同权重差 16.6 个绝对点。基础模型是组件；循环是产品。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The companion problem is that benchmark saturation hides regressions.

> 伴随问题是基准饱和隐藏了回归。

SWE-bench Verified is close to saturated, and the easy-task tail (161 of 500 tasks requiring ≤2 lines) pulls top scores up. Real-world quality is better measured on distributions like SWE-bench Pro (10+ line changes), where the same leaders still sit at 23–59%.

> SWE-bench Verified 接近饱和，简单任务尾部（500 个任务中 161 个需 ≤2 行）拉高顶级分数。现实世界质量在 SWE-bench Pro（10+ 行变更）等分布上测量更好，同一领先者仍只有 23-59%。

## The Concept | 核心概念

### SWE-bench, one paragraph | SWE-bench 一段话

SWE-bench (Jimenez et al.) takes real GitHub issues with ground-truth patches and asks an agent to produce a patch that makes the test suite pass. SWE-bench Verified (OpenAI, 2024) is a human-curated 500-task subset with the ambiguous and broken tasks removed. SWE-bench Pro is the harder successor — tasks requiring 10+ lines of change, where current frontier agents sit at 23–59%.

> SWE-bench（Jimenez 等人）取带真实补丁的真实 GitHub issue，要求 Agent 产生使测试套件通过的补丁。SWE-bench Verified（OpenAI，2024）是人工策划的 500 任务子集，去除了模糊和损坏的任务。SWE-bench Pro 是更难的继任者——需 10+ 行变更的任务，当前前沿 Agent 在 23-59%。

### What the 2022 → 2026 curve actually shows | 2022→2026 曲线实际展示什么

- **2022**: research models at ~4% on raw SWE-bench.
  中文翻译：**2022**：研究模型在原始 SWE-bench 上约 4%。
- **2024**: GPT-4 + Devin-style scaffolding at ~14%; SWE-agent at ~12%.
  中文翻译：**2024**：GPT-4 + Devin 式脚手架约 14%；SWE-agent 约 12%。
- **2025**: Claude 3.5/3.7 Sonnet inside Aider and SWE-agent push into the 40–55% range.
  中文翻译：**2025**：Claude 3.5/3.7 Sonnet 在 Aider 和 SWE-agent 内推入 40-55% 范围。
- **2026**: Claude Sonnet 4.5 and frontier competitors at 70–80%+ on SWE-bench Verified. Epoch AI's leaderboard tracks this live.
  中文翻译：**2026**：Claude Sonnet 4.5 和前沿竞争者在 SWE-bench Verified 上 70-80%+。Epoch AI 的排行榜实时跟踪。

The slope came from three compounding sources: better base models, better scaffolding (CodeAct, reflection, verifier loops), and better benchmarks (Verified removing noise).

> 斜率来自三个复合源：更好的基础模型、更好的脚手架（CodeAct、反思、验证器循环）、更好的基准（Verified 去除噪声）。

### CodeAct vs JSON tool calls | CodeAct vs JSON 工具调用

OpenHands (All-Hands-AI, arXiv:2407.16741, formerly OpenDevin) took a specific architectural bet: instead of the model emitting JSON tool calls that a host decodes and executes, the model emits Python code and a Jupyter-style kernel runs it in a sandbox. The agent can loop over files, chain tools, and catch its own exceptions inside one action.

> OpenHands（All-Hands-AI，arXiv:2407.16741，前 OpenDevin）下了特定架构赌注：模型不再发出由宿主解码执行的 JSON 工具调用，而是发出 Python 代码，由 Jupyter 风格内核在沙箱中运行。Agent 可在一个动作内循环文件、链式工具、捕获自己的异常。

The trade-off:

> 权衡：

- **JSON tool calls**: every action is one turn; easy to audit; limited compositionality; safe by default because each call goes through an explicit validator.
  中文翻译：**JSON 工具调用**：每个动作一轮；易审计；组合性有限；默认安全因为每次调用经过显式验证器。
- **CodeAct**: one action can be a whole program; compositional; requires a hardened sandbox (OpenHands uses Docker isolation); failure modes include anything the sandbox runtime allows.
  中文翻译：**CodeAct**：一个动作可以是整个程序；可组合；需要加固沙箱（OpenHands 使用 Docker 隔离）；失败模式包括沙箱运行时允许的任何事。

Both architectures are in production. CodeAct is dominant in open platforms (OpenHands, smolagents). JSON tool calls remain dominant in managed services (Anthropic Managed Agents, OpenAI Assistants) where the provider controls the executor.

> 两种架构都在生产中。CodeAct 在开放平台（OpenHands、smolagents）主导。JSON 工具调用在管理服务（Anthropic Managed Agents、OpenAI Assistants）主导，那里提供商控制执行器。

### Scaffolds in the 2026 landscape | 2026 全景中的脚手架

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### Why scaffolding dominates | 为什么脚手架主导

A coding run is a long-horizon trajectory (Lesson 1). Reliability compounds across steps. Three places where scaffolding buys points:

> 编码运行是长程轨迹（第 1 课）。可靠性跨步骤复合。脚手架买入分数的三个地方：

1. **Retrieval**: finding the right files to read is the silent bottleneck. SWE-agent's ACI, OpenHands' file-index, and Aider's repo-map all attack this.
   中文翻译：**检索**：找到要读的正确文件是静默瓶颈。SWE-agent 的 ACI、OpenHands 的文件索引、Aider 的 repo-map 都攻击这一点。
2. **Verifier loop**: running tests, reading stack traces, and re-attempting is a 10+ point delta on SWE-bench.
   中文翻译：**验证器循环**：运行测试、读堆栈跟踪、重试在 SWE-bench 上是 10+ 点增量。
3. **Failure containment**: a sandbox that rolls back on error prevents compounding damage. The same model with and without a verifier loop looks like two different products.
   中文翻译：**失败遏制**：错误时回滚的沙箱防止复合损害。同一模型有和无验证器循环看起来像两个不同产品。

### Benchmark saturation and the real distribution | 基准饱和与真实分布

The OpenHands authors and Epoch AI both flag that SWE-bench Verified has an easy tail: 161 of 500 tasks need only 1–2 lines of change. High scores are driven partly by this tail. SWE-bench Pro restricts to 10+ line changes and returns scores in the 23–59% range even for frontier systems. Your production distribution is almost certainly closer to Pro than to Verified.

> OpenHands 作者和 Epoch AI 都标记 SWE-bench Verified 有简单尾部：500 个任务中 161 个仅需 1-2 行变更。高分部分由该尾部驱动。SWE-bench Pro 限制 10+ 行变更，即使前沿系统也返回 23-59% 范围。你的生产分布几乎肯定更接近 Pro 而非 Verified。

Implication for choosing an agent: run a Pro-like subset of your own bug backlog. The score that matters is the score on tasks representative of what you ship.

> 选择 Agent 的含义：在你自己的 bug 积压上运行 Pro 类子集。重要的分数是代表你发布任务的分数。

## Use It | 用框架实现

`code/main.py` compares two toy agent scaffolds on a fixed mini-task distribution:

> `code/main.py` 在固定迷你任务分布上比较两个玩具 Agent 脚手架：

1. A **JSON tool-call** scaffold that takes one action per turn.
   中文翻译：**JSON 工具调用**脚手架，每轮一个动作。
2. A **CodeAct** scaffold that can emit a small Python snippet per action.
   中文翻译：**CodeAct** 脚手架，每动作可发出小 Python 代码片段。

Both use a stub "model" (deterministic rules) so the comparison isolates the scaffold from model quality. The output shows the CodeAct scaffold solves more tasks in fewer turns at the cost of a larger per-action blast radius.

> 两者使用存根"模型"（确定性规则）以使比较将脚手架与模型质量隔离。输出显示 CodeAct 脚手架以更大每动作爆炸半径为代价在更少轮次解决更多任务。

## Ship It | 产出物

`outputs/skill-scaffold-audit.md` helps you audit a proposed coding-agent scaffold before adoption: retrieval quality, verifier presence, sandbox isolation, and benchmark-to-distribution fit.

> `outputs/skill-scaffold-audit.md` 帮助你在采用前审计提议的编码 Agent 脚手架：检索质量、验证器存在、沙箱隔离、基准到分布契合。

## Exercises | 练习题

1. Run `code/main.py`. How many turns does each scaffold take on the same task set? What is the per-action blast radius of each?
   中文翻译：运行 `code/main.py`。每个脚手架在同一任务集上多少轮？每个的每动作爆炸半径多大？

2. Read the OpenHands paper (arXiv:2407.16741). The paper argues CodeAct beats JSON tool calls on complex tasks. Identify one failure mode the paper acknowledges and write one sentence on when that mode would dominate in production.
   中文翻译：阅读 OpenHands 论文（arXiv:2407.16741）。论文论证 CodeAct 在复杂任务上胜过 JSON 工具调用。识别论文承认的一个失败模式并写一句该模式在生产中何时主导。

3. Pick one task from your bug backlog that would require 10+ lines of change across two files. Estimate the end-to-end success probability for a frontier model under (a) JSON tool calls and (b) CodeAct. Justify the gap.
   中文翻译：从你的 bug 积压中选一个需跨两文件 10+ 行变更的任务。估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率。论证差距。

4. SWE-bench Verified has 161 single-file, 1–2 line tasks. Construct a score that excludes them. How does the leaderboard shuffle?
   中文翻译：SWE-bench Verified 有 161 个单文件 1-2 行任务。构造排除它们的分数。排行榜如何重排？

5. Read "Introducing SWE-bench Verified" (OpenAI). Explain the specific methodology used to remove ambiguous tasks, and name one category the curation would miss.
   中文翻译：阅读"Introducing SWE-bench Verified"（OpenAI）。解释用于去除模糊任务的具体方法论，命名策划会遗漏的一个类别。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Further Reading | 延伸阅读

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) — the original benchmark and methodology.
  中文翻译：原始基准和方法论。
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — how the curated subset was built.
  中文翻译：策划子集如何构建。
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) — CodeAct architecture and event-stream design.
  中文翻译：CodeAct 架构和事件流设计。
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks) — live-tracked scores.
  中文翻译：实时跟踪分数。
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) — long-horizon coding-agent reliability framing.
  中文翻译：长程编码 Agent 可靠性框架。
