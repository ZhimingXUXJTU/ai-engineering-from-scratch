# Benchmarks: WebArena and OSWorld | 基准测试 WebArena OSWorld

> WebArena tests web-agent capability across four self-hosted apps. OSWorld tests desktop-agent capability across Ubuntu, Windows, macOS. At release (2023–2024) both showed a big gap between best-in-class agents and humans. The gap is narrowing; the failure modes haven't changed.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 19 (SWE-bench, GAIA) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Describe WebArena's four self-hosted apps and why execution-based evaluation matters.
- Explain why OSWorld uses real OS screenshots instead of accessibility APIs.
- Name the two primary OSWorld failure modes: GUI grounding and operational knowledge.
- Summarize what OSWorld-G and OSWorld-Human add on top of the base benchmark.

## The Problem | 问题引入

Generalist agents can call tools. Can they drive a browser across 20 clicks to complete a shopping checkout? Can they configure a Linux box using only keyboard and mouse? These are the questions WebArena and OSWorld answer.


> **【中文解读】** WebArena 和 OSWorld 评估 Agent 在真实计算环境中的操作能力。WebArena 测试 Web 浏览器操作（购物、论坛、CMS）。OSWorld 测试桌面操作系统操作（文件管理、应用操作）。两者都是端到端评估——不看中间步骤，只看最终结果是否正确。

> **{【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】}** WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），Agent 需要像人类一样浏览和操作。2026 年 SOTA 约 35% 成功率，人类约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境，Agent 需要操作 GUI 完成任务。成功率更低，最好的 Agent 约 12%。
## The Concept | 核心概念

### WebArena (Zhou et al., ICLR 2024)

- 812 long-horizon tasks across four self-hosted web apps: a shopping site, a forum, a GitLab-like dev tool, a business CMS.
- Plus utilities: map, calculator, scratchpad.
- Evaluation is execution-based via gym APIs — was the order placed, was the issue closed, was the CMS page updated?
- At release: best GPT-4 agent hit 14.41% success vs human 78.24%.

The self-hosted framing matters — the benchmark is not flaky because the target apps are pinned and reproducible.

> WebArena 和 OSWorld 是计算机使用 Agent 的评估环境。WebArena 模拟网页操作，OSWorld 模拟完整桌面环境。两者都测试 Agent 在真实 GUI 中的操作能力。

### Extensions

- **VisualWebArena** — visually grounded tasks where success depends on interpreting images (screenshots as first-class observations).
- **TheAgentCompany** (Dec 2024) — adds terminal + coding; more like a real remote-work environment.

### OSWorld (Xie et al., NeurIPS 2024)

- 369 real computer tasks across Ubuntu, Windows, macOS.
- Free-form keyboard and mouse control of real applications.
- 1920×1080 screenshots as the observation.
- At release: best model 12.24% vs human 72.36%.

### Primary failure modes

1. **GUI grounding.** Pixel → element mapping. Models struggle to localize UI elements reliably in 1920×1080.
2. **Operational knowledge.** Which menu has the setting, which keyboard shortcut, which preference pane. Knowledge tail that humans build over years.

### Follow-ups

- **OSWorld-G** — 564-sample grounding suite + Jedi training set. Decomposes grounding from planning so you can measure them separately.
- **OSWorld-Human** — manually curated gold action trajectories. Shows top agents use 1.4-2.7x more steps than necessary (the trajectory-efficiency gap).

### Why this matters

Claude computer use, OpenAI CUA, Gemini 2.5 Computer Use (Lesson 21) all train on workloads shaped by WebArena and OSWorld. The benchmarks are the target; the production models are the shipped answer.

> WebArena 和 OSWorld 是计算机使用 Agent 的评估环境。WebArena 模拟网页操作，OSWorld 模拟完整桌面环境。两者都测试 Agent 在真实 GUI 中的操作能力。

### Where benchmarking goes wrong

- **Screenshot-only evals.** OSWorld is screenshot-driven; evaluating an agent that uses DOM or accessibility APIs on OSWorld misses the grounding challenge.
- **Ignoring trajectory length.** Scoring only success-rate misses the 1.4-2.7x step inefficiency OSWorld-Human surfaces.
- **Stale self-hosted apps.** WebArena's apps pin specific versions; update without re-curation breaks comparability.

## Build It | 动手实现

`code/main.py` implements a toy web-agent harness:

> WebArena 和 OSWorld 是计算机使用 Agent 的评估环境。WebArena 模拟网页操作，OSWorld 模拟完整桌面环境。两者都测试 Agent 在真实 GUI 中的操作能力。

- A minimal "shopping app" state machine: list_items, add_to_cart, checkout.
- Gold trajectories for 3 tasks.
- A scripted agent that attempts each task.
- Execution-based evaluator (state check) and trajectory-efficiency metric (steps vs gold).

Run it:

```
python3 code/main.py
```

Output: per-task success rate and trajectory efficiency, mirroring OSWorld-Human's methodology.

> WebArena 和 OSWorld 是计算机使用 Agent 的评估环境。WebArena 模拟网页操作，OSWorld 模拟完整桌面环境。两者都测试 Agent 在真实 GUI 中的操作能力。

## Use It | 用框架实现

- **WebArena Verified** self-hosted on an internal cluster for continuous evaluation.
- **OSWorld** in a VM fleet for desktop agents.
- **Computer-use agents** (Lesson 21) — Claude, OpenAI CUA, Gemini — all trained on workloads like these.
- **Your own product flows** — capture gold trajectories for your top 20 tasks; run agents against them weekly.

## Ship It | 产出物

`outputs/skill-web-desktop-harness.md` builds a web/desktop agent harness with execution-based eval and trajectory efficiency metric.

> WebArena 和 OSWorld 是计算机使用 Agent 的评估环境。WebArena 模拟网页操作，OSWorld 模拟完整桌面环境。两者都测试 Agent 在真实 GUI 中的操作能力。

## Exercises | 练习题

1. Extend the toy harness with a second app (a forum). Write 3 tasks plus gold trajectories.
  中文翻译：思考并实践此练习。
2. Add trajectory-efficiency reporting per task. On your toy, is the agent 1x, 2x, or 3x over gold?
  中文翻译：思考并实践此练习。
3. Implement a "distractor" tool — one the gold trajectory never uses. Does the scripted agent get tempted?
  中文翻译：思考并实践此练习。
4. Read OSWorld-G. How would you separate grounding failures from planning failures in your own evals?
  中文翻译：思考并实践此练习。
5. Read WebArena's apps README. What breaks when you upgrade one of the pinned app versions?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| WebArena | "Web agent benchmark" | 812 tasks across 4 self-hosted apps; gym-style evaluation |  |
| VisualWebArena | "Visual WebArena" | Visually grounded WebArena; screenshots are observations |  |
| OSWorld | "Desktop agent benchmark" | 369 tasks on real Ubuntu/Windows/macOS |  |
| GUI grounding | "Pixel-to-element mapping" | Model localizing UI elements in 1920x1080 |  |
| Operational knowledge | "OS know-how" | Which menu, which shortcut, which preference pane |  |
| OSWorld-G | "Grounding suite" | 564 grounding-only samples + training set |  |
| OSWorld-Human | "Gold trajectories" | Manual expert action sequences to measure efficiency |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human minimum |  |

## Further Reading | 延伸阅读

- [Zhou et al., WebArena (arXiv:2307.13854)](https://arxiv.org/abs/2307.13854) — four-app web benchmark
  中文翻译：见原文。
- [Xie et al., OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) — cross-OS desktop benchmark
  中文翻译：见原文。
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) — Claude's benchmark-shaped capability
  中文翻译：见原文。
- [OpenAI, Computer-Using Agent](https://openai.com/index/computer-using-agent/) — OSWorld and WebArena numbers
  中文翻译：见原文。
