# 基准测试 GAIA

> Three benchmarks anchor agent evaluation in 2026. SWE-bench tests code patching. GAIA tests generalist tool use. AgentBench tests multi-environment reasoning. Know their composition, their contamination story, and what they do not measure.


**类型：** 学习
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 06 (Tool Use)
**预计时间：** ~60 minutes

## 学习目标

- Name SWE-bench's test harness (FAIL_TO_PASS) and explain why it gates on unit tests.
- Explain why SWE-bench Verified (OpenAI, 500 tasks) exists and what it removes.
- Describe GAIA's design: simple for humans, hard for AI; three difficulty levels.
- Name AgentBench's eight environments and its primary blocker for open-source LLMs.
- Summarize the SWE-bench+ contamination finding and its implications.

## 问题引入

- Whether the benchmark is contaminated (solutions in training data, test leakage).
- Whether the benchmark measures what you care about (code vs browsing vs generalist).
- Whether the evaluator is robust (AST matching, state checks, human review).
> **【中文解读】** SWE-bench 和 GAIA 是 2026 年最重要的两个 Agent 能力基准。SWE-bench 评估 Agent 修复真实 GitHub issue 的能力（软件工程）。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题的能力（通用推理）。两者共同定义了 Agent 的能力边界。
> **【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】** SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub issue，Agent 必须在真实代码库中定位 bug、编写修复并通过测试。2026 年 SOTA 是 72% 解决率（OpenAI 的 Codex）。GAIA (Meta, 2023) 的 466 个问题需要 web 搜索、文件处理、代码执行等工具。人类平均 92%，最好的 Agent 约 70%。

## 核心概念

### SWE-bench (Jimenez et al., ICLR 2024 oral)
- 2,294 real GitHub issues from 12 popular Python repos.
- Agent gets: the codebase at the pre-fix commit + natural-language issue description.
- Agent produces: a patch.
- Evaluator: apply patch, run the repo's test suite. The patch must flip FAIL_TO_PASS tests (previously failing, now passing) without breaking PASS_TO_PASS tests.
SWE-agent (Yang et al., 2024) hit 12.5% at release by emphasizing agent-computer interfaces (file editor commands, search syntax the model understands).
### SWE-bench Verified
OpenAI, Aug 2024. Human-curated 500-task subset. Removes ambiguous issues, unreliable tests, and tasks where the fix was unclear. Primary benchmark for "does your agent ship real patches?"
### Contamination
- Over 94% of SWE-bench issues predate most model cutoffs.
- **SWE-bench+** found 32.67% of successful patches leaked solutions in the issue text (model saw the fix in the description), and 31.08% were suspicious due to weak test coverage.
- Verified is cleaner but not contamination-free.
Practical implication: a model that scores 50% on SWE-bench may score 35% on SWE-bench+. Always report both if you claim SWE-bench performance.
### GAIA (Mialon et al., Nov 2023)
- 466 questions; 300 retained for the private leaderboard at huggingface.co/gaia-benchmark.
- Design philosophy: "conceptually simple for humans (92%) but hard for AI (GPT-4 with plugins: 15%)."
- Tests reasoning, multi-modality, web, tool use.
- Three difficulty levels; Level 3 requires long tool chains across modalities.
GAIA is what you run to measure "generalist capability." Do not confuse with code-specific benchmarks.
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

## 动手实现

`code/main.py` implements a toy SWE-bench-like harness:
- Synthetic bug-fix tasks (3 tasks).
- A scripted "agent" that proposes patches.
- A test runner that checks FAIL_TO_PASS (bug now fixed) and PASS_TO_PASS (nothing broken).
- A GAIA-style difficulty classifier based on question decomposition depth.
Run it:
```
python3 code/main.py
```
The output shows resolution rate per task + per difficulty and makes the evaluator rules concrete.

## 用框架实现

- **SWE-bench Verified** for code agents. Always report Verified scores.
- **GAIA** for generalist agents. Use the private leaderboard split.
- **AgentBench** for multi-environment comparison.
- **Custom evals** (Lesson 30) for your product's actual shape.

## 产出物

`outputs/skill-benchmark-harness.md` builds a SWE-bench-style harness for any codebase-task pair with FAIL_TO_PASS / PASS_TO_PASS gating.

## 练习题

1. Port the toy harness to run on a real repo (pick one of yours). Write 3 FAIL_TO_PASS tests for known bugs.
   *思考并实践此练习*
2. Add a step-count metric. On your 3 tasks, how many agent steps per resolution?
   *思考并实践此练习*
3. Read the SWE-bench+ paper. Implement a solution-leakage check (pattern-match the issue text against the diff).
   *思考并实践此练习*
4. Download a GAIA question from the public split. Trace what a GPT-4-class agent would do. What tools does it need?
   *思考并实践此练习*
5. Read AgentBench's per-environment breakdown. Which environment mirrors your product surface? What does "SOTA" look like there?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| SWE-bench | "Code agent benchmark" |
| SWE-bench Verified | "Clean SWE-bench" |
| FAIL_TO_PASS | "Fix gate" |
| PASS_TO_PASS | "No-regression gate" |
| GAIA | "Generalist benchmark" |
| AgentBench | "Multi-env benchmark" |
| Contamination | "Training-set leak" |
| SWE-bench+ | "Contamination audit" |

## 延伸阅读

