# Benchmarks: SWE-bench, GAIA, AgentBench | 基准测试 GAIA

> Three benchmarks anchor agent evaluation in 2026. SWE-bench tests code patching. GAIA tests generalist tool use. AgentBench tests multi-environment reasoning. Know their composition, their contamination story, and what they do not measure.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Name SWE-bench's test harness (FAIL_TO_PASS) and explain why it gates on unit tests.
- Explain why SWE-bench Verified (OpenAI, 500 tasks) exists and what it removes.
- Describe GAIA's design: simple for humans, hard for AI; three difficulty levels.
- Name AgentBench's eight environments and its primary blocker for open-source LLMs.
- Summarize the SWE-bench+ contamination finding and its implications.

## The Problem | 问题引入

Leaderboards tell you which model wins on one benchmark. They do not tell you:

> 排行榜告诉你哪个模型在某个基准上获胜。它们不会告诉你：

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

- Whether the benchmark is contaminated (solutions in training data, test leakage).
- Whether the benchmark measures what you care about (code vs browsing vs generalist).
- Whether the evaluator is robust (AST matching, state checks, human review).


> **【中文解读】** SWE-bench 和 GAIA 是 2026 年最重要的两个 Agent 能力基准。SWE-bench 评估 Agent 修复真实 GitHub issue 的能力（软件工程）。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题的能力（通用推理）。两者共同定义了 Agent 的能力边界。

> **{【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】}** SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub issue，Agent 必须在真实代码库中定位 bug、编写修复并通过测试。2026 年 SOTA 是 72% 解决率（OpenAI 的 Codex）。GAIA (Meta, 2023) 的 466 个问题需要 web 搜索、文件处理、代码执行等工具。人类平均 92%，最好的 Agent 约 70%。
Know the three anchoring benchmarks and their failure modes before you quote a number.

> 在引用数据之前，先了解这三个基准测试及其失败模式。

> 🔗 **【前置】** 建议先过：Phase 14·06（Tool Use）——理解 Agent 如何调用工具是看懂 GAIA 的前提；以及基本的"机器学习评估方法论"——precision/recall、contamination（数据污染）、test set leakage。如果你引用过模型 benchmark 但不知道 contamination 是什么，本节必须学。

## The Concept | 核心概念

### SWE-bench (Jimenez et al., ICLR 2024 oral)

- 2,294 real GitHub issues from 12 popular Python repos.
- Agent gets: the codebase at the pre-fix commit + natural-language issue description.
- Agent produces: a patch.
- Evaluator: apply patch, run the repo's test suite. The patch must flip FAIL_TO_PASS tests (previously failing, now passing) without breaking PASS_TO_PASS tests.

SWE-agent (Yang et al., 2024) hit 12.5% at release by emphasizing agent-computer interfaces (file editor commands, search syntax the model understands).

> 💡 **【类比】** SWE-bench 像考"开卷实操"：给 Agent 一个真实的代码库（开卷）、一个 issue 描述（考题）、一套已有的单元测试（评分标准）。Agent 要像人类工程师一样——读代码定位 bug、写补丁、跑测试。**关键设计**：测试用 FAIL_TO_PASS（修复前失败、修复后通过）+ PASS_TO_PASS（不能破坏已有功能），杜绝"修了 A 破了 B"的伪通过。

> SWE-agent（Yang 等，2024）在发布时达到 12.5%，通过强调 Agent-计算机接口（文件编辑器命令、模型能理解的搜索语法）。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

### SWE-bench Verified

OpenAI, Aug 2024. Human-curated 500-task subset. Removes ambiguous issues, unreliable tests, and tasks where the fix was unclear. Primary benchmark for "does your agent ship real patches?"

> OpenAI，2024 年 8 月。人工策划的 500 个任务子集。移除了模糊的 issue、不可靠的测试和修复不明确的任务。"你的 Agent 能交付真实的补丁吗？"的主要基准。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

### Contamination

- Over 94% of SWE-bench issues predate most model cutoffs.
- **SWE-bench+** found 32.67% of successful patches leaked solutions in the issue text (model saw the fix in the description), and 31.08% were suspicious due to weak test coverage.
- Verified is cleaner but not contamination-free.

Practical implication: a model that scores 50% on SWE-bench may score 35% on SWE-bench+. Always report both if you claim SWE-bench performance.

> ⚠️ **【易错点】** 引用 SWE-bench 分数时不提 Verified/SWE-bench+。**后果**：被审稿人/同事/客户当场打脸——SWE-bench 50% 中可能有 32% 是"模型在 issue 文本里看到了答案"（contamination）。这是 AI 圈最普遍的"虚高分数"陷阱。**一行修复**：任何引用 SWE-bench 数字时，必须同时给出 Verified 子集分数和 SWE-bench+（去污染版）分数，注明数据来源日期。

> 实际影响：一个在 SWE-bench 上得分 50% 的模型在 SWE-bench+ 上可能只得到 35%。如果你声称 SWE-bench 性能，请务必同时报告两者。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

### GAIA (Mialon et al., Nov 2023)

- 466 questions; 300 retained for the private leaderboard at huggingface.co/gaia-benchmark.
- Design philosophy: "conceptually simple for humans (92%) but hard for AI (GPT-4 with plugins: 15%)."
- Tests reasoning, multi-modality, web, tool use.
- Three difficulty levels; Level 3 requires long tool chains across modalities.

GAIA is what you run to measure "generalist capability." Do not confuse with code-specific benchmarks.

> GAIA 是用来衡量"通用能力"的基准。不要与代码专用基准混淆。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

### AgentBench (Liu et al., ICLR 2024)

- 8 environments across code (Bash, DB, KG), games (Alfworld, LTP), web (WebShop, Mind2Web), and open-ended generation.
- Multi-turn, ~4k-13k turns per split.
- Primary finding: long-term reasoning, decision-making, and instruction following are the blockers for OSS LLMs catching up to commercial.

### What these do not measure

- Real-world operational cost (tokens, wall-clock).
- Safety behavior in adversarial conditions.
- Performance on your domain (use your own evals, Lesson 30).
- Tail failures (benchmarks average; production operators care about the worst 1%).

### Where benchmarking goes wrong

- **Single-number fixation.** SWE-bench 50% tells you less than the P50/P75/P95 cost + step distribution.
- **Contaminated claims.** Reporting SWE-bench without mentioning Verified or SWE-bench+ is misleading.
- **Benchmark-as-development-target.** Optimizing for the benchmark diverges from production usefulness.

> 🤔 **【困惑】** Q: SWE-bench Verified 上 70%+ 的模型出来了，是不是说软件工程师要失业了？ A: 还早。三个原因：(1) SWE-bench 的 issue 都是"有明确测试用例、有清晰复现路径"的 well-formed issue，生产中 50% 的 issue 不满足；(2) 70% 意味着每 3 个任务失败 1 个，生产环境失败修复的成本远高于成功修复的收益；(3) **生产代码库比 SWE-bench 的 12 个开源 Python 仓库复杂得多**——私有代码、跨语言、几十年遗留代码。Benchmark 上的 70% 不等于生产环境的 70%。

> **单一数字执念。** SWE-bench 50% 告诉你的信息少于 P50/P75/P95 成本 + 步骤分布。
> **污染声明。** 报告 SWE-bench 时不提及 Verified 或 SWE-bench+ 是误导性的。
> **基准作为开发目标。** 为基准优化会偏离生产实用性。

## Build It | 动手实现

`code/main.py` implements a toy SWE-bench-like harness:

> `code/main.py` 实现了一个类似 SWE-bench 的玩具测试工具：

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

- Synthetic bug-fix tasks (3 tasks).
- A scripted "agent" that proposes patches.
- A test runner that checks FAIL_TO_PASS (bug now fixed) and PASS_TO_PASS (nothing broken).
- A GAIA-style difficulty classifier based on question decomposition depth.

Run it:

```
python3 code/main.py
```

The output shows resolution rate per task + per difficulty and makes the evaluator rules concrete.

> 输出显示每个任务和每个难度级别的解决率，并使评估器规则具体化。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

## Use It | 用框架实现

- **SWE-bench Verified** for code agents. Always report Verified scores.
- **GAIA** for generalist agents. Use the private leaderboard split.
- **AgentBench** for multi-environment comparison.
- **Custom evals** (Lesson 30) for your product's actual shape.

## Ship It | 产出物

`outputs/skill-benchmark-harness.md` builds a SWE-bench-style harness for any codebase-task pair with FAIL_TO_PASS / PASS_TO_PASS gating.

> `outputs/skill-benchmark-harness.md` 为任何代码库-任务对构建一个 SWE-bench 风格的测试工具，带有 FAIL_TO_PASS / PASS_TO_PASS 门控。

> SWE-bench 和 GAIA 是 Agent 能力的两个核心基准。SWE-bench 评估代码修复能力，GAIA 评估通用推理能力。2026 年的 Agent 评估正在从单任务指标转向端到端轨迹评估。

## Exercises | 练习题

1. Port the toy harness to run on a real repo (pick one of yours). Write 3 FAIL_TO_PASS tests for known bugs.
  中文翻译：思考并实践此练习。
2. Add a step-count metric. On your 3 tasks, how many agent steps per resolution?
  中文翻译：思考并实践此练习。
3. Read the SWE-bench+ paper. Implement a solution-leakage check (pattern-match the issue text against the diff).
  中文翻译：思考并实践此练习。
4. Download a GAIA question from the public split. Trace what a GPT-4-class agent would do. What tools does it need?
  中文翻译：思考并实践此练习。
5. Read AgentBench's per-environment breakdown. Which environment mirrors your product surface? What does "SOTA" look like there?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| SWE-bench | "Code agent benchmark" | 2,294 GitHub issues; patch must flip FAIL_TO_PASS tests |  |
| SWE-bench Verified | "Clean SWE-bench" | 500 human-curated tasks, OpenAI |  |
| FAIL_TO_PASS | "Fix gate" | Tests previously failing that must pass after the patch |  |
| PASS_TO_PASS | "No-regression gate" | Tests that were passing and must still pass |  |
| GAIA | "Generalist benchmark" | 466 human-easy / AI-hard multi-tool questions |  |
| AgentBench | "Multi-env benchmark" | 8 environments; long-horizon multi-turn |  |
| Contamination | "Training-set leak" | Benchmark tasks present in model training |  |
| SWE-bench+ | "Contamination audit" | 32.67% solution leakage found in successful SWE-bench patches |  |

## Further Reading | 延伸阅读

- [Jimenez et al., SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) — the original benchmark
  中文翻译：见原文。
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — the curated subset
  中文翻译：见原文。
- [Mialon et al., GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) — generalist benchmark
  中文翻译：见原文。
- [Liu et al., AgentBench (arXiv:2308.03688)](https://arxiv.org/abs/2308.03688) — multi-environment suite
  中文翻译：见原文。
