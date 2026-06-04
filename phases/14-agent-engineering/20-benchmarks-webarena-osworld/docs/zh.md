# 基准测试 WebArena OSWorld

> WebArena tests web-agent capability across four self-hosted apps. OSWorld tests desktop-agent capability across Ubuntu, Windows, macOS. At release (2023–2024) both showed a big gap between best-in-class agents and humans. The gap is narrowing; the failure modes haven't changed.


**类型：** 学习
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 19 (SWE-bench, GAIA)
**预计时间：** ~60 minutes

## 学习目标

- Describe WebArena's four self-hosted apps and why execution-based evaluation matters.
- Explain why OSWorld uses real OS screenshots instead of accessibility APIs.
- Name the two primary OSWorld failure modes: GUI grounding and operational knowledge.
- Summarize what OSWorld-G and OSWorld-Human add on top of the base benchmark.

## 问题引入

> **【中文解读】** WebArena 和 OSWorld 评估 Agent 在真实计算环境中的操作能力。WebArena 测试 Web 浏览器操作（购物、论坛、CMS）。OSWorld 测试桌面操作系统操作（文件管理、应用操作）。两者都是端到端评估——不看中间步骤，只看最终结果是否正确。
> **【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】** WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），Agent 需要像人类一样浏览和操作。2026 年 SOTA 约 35% 成功率，人类约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境，Agent 需要操作 GUI 完成任务。成功率更低，最好的 Agent 约 12%。

## 核心概念

### WebArena (Zhou et al., ICLR 2024)
- 812 long-horizon tasks across four self-hosted web apps: a shopping site, a forum, a GitLab-like dev tool, a business CMS.
- Plus utilities: map, calculator, scratchpad.
- Evaluation is execution-based via gym APIs — was the order placed, was the issue closed, was the CMS page updated?
- At release: best GPT-4 agent hit 14.41% success vs human 78.24%.
The self-hosted framing matters — the benchmark is not flaky because the target apps are pinned and reproducible.
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
### Where benchmarking goes wrong
- **Screenshot-only evals.** OSWorld is screenshot-driven; evaluating an agent that uses DOM or accessibility APIs on OSWorld misses the grounding challenge.
- **Ignoring trajectory length.** Scoring only success-rate misses the 1.4-2.7x step inefficiency OSWorld-Human surfaces.
- **Stale self-hosted apps.** WebArena's apps pin specific versions; update without re-curation breaks comparability.

## 动手实现

`code/main.py` implements a toy web-agent harness:
- A minimal "shopping app" state machine: list_items, add_to_cart, checkout.
- Gold trajectories for 3 tasks.
- A scripted agent that attempts each task.
- Execution-based evaluator (state check) and trajectory-efficiency metric (steps vs gold).
Run it:
```
python3 code/main.py
```
Output: per-task success rate and trajectory efficiency, mirroring OSWorld-Human's methodology.

## 用框架实现

- **WebArena Verified** self-hosted on an internal cluster for continuous evaluation.
- **OSWorld** in a VM fleet for desktop agents.
- **Computer-use agents** (Lesson 21) — Claude, OpenAI CUA, Gemini — all trained on workloads like these.
- **Your own product flows** — capture gold trajectories for your top 20 tasks; run agents against them weekly.

## 产出物

`outputs/skill-web-desktop-harness.md` builds a web/desktop agent harness with execution-based eval and trajectory efficiency metric.

## 练习题

1. Extend the toy harness with a second app (a forum). Write 3 tasks plus gold trajectories.
   *思考并实践此练习*
2. Add trajectory-efficiency reporting per task. On your toy, is the agent 1x, 2x, or 3x over gold?
   *思考并实践此练习*
3. Implement a "distractor" tool — one the gold trajectory never uses. Does the scripted agent get tempted?
   *思考并实践此练习*
4. Read OSWorld-G. How would you separate grounding failures from planning failures in your own evals?
   *思考并实践此练习*
5. Read WebArena's apps README. What breaks when you upgrade one of the pinned app versions?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| WebArena | "Web agent benchmark" |
| VisualWebArena | "Visual WebArena" |
| OSWorld | "Desktop agent benchmark" |
| GUI grounding | "Pixel-to-element mapping" |
| Operational knowledge | "OS know-how" |
| OSWorld-G | "Grounding suite" |
| OSWorld-Human | "Gold trajectories" |
| Trajectory efficiency | "Steps over gold" |

## 延伸阅读

