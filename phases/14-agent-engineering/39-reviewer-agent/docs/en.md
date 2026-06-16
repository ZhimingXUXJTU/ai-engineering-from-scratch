# Reviewer Agent: Separate Builder from Marker | 审查者

> The agent that wrote the code cannot grade it. A reviewer is a second loop with a different system prompt, a different goal, and read-only access to everything the builder produced. The gap between builder and reviewer is where most reliability lives.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 38 (Verification Gate) | **前置知识:** 见原文
**Time:** ~55 minutes | **时间:** 见原文

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·38（Verification Gate）。本节是 gate 的 LLM 版——用第二个 Agent 审查第一个 Agent 的产出。
> 💡 **【类比】** Builder + Reviewer = 作家 + 编辑。作家写完初稿容易自我感觉良好（"我觉得很清楚"），编辑以读者视角挑刺（"这段逻辑跳跃、那个名词没解释"）。让同一个 Agent 兼任两者等于没有审查——人类作家都不行，LLM 更不行。

## Learning Objectives | 学习目标

- State why the same agent cannot reliably review its own work.
- Build a reviewer agent loop that consumes builder artifacts and emits a structured review report.
- Author a reviewer rubric that grades specific dimensions, not vibes.
- Wire the reviewer into the workbench so the human review step starts from a real artifact.

## The Problem | 问题引入

You ask the agent to fix a bug. It edits four files, runs the tests, and reports done. The verification gate (Phase 14 · 38) confirms acceptance ran and scope held. The gate says `passed: true`. You merge. Two days later you find that the fix solved the wrong half of the bug.

> 你让 Agent 修复一个 bug。它编辑了四个文件，运行测试，报告完成。验证门控（Phase 14 · 38）确认验收通过且范围保持。门控说 `passed: true`。你合并。两天后你发现修复只解决了 bug 的一半。

Acceptance is necessary, not sufficient. The reviewer asks the questions acceptance cannot ask: did this solve the right problem? Did it expand scope without flagging it? Did it document assumptions that should have been questioned? Did it leave the workbench in a state the next session can pick up?

> 验收是必要的，但不充分的。评审者问验收无法问的问题：这是否解决了正确的问题？是否在没有标记的情况下扩展了范围？是否记录了本应被质疑的假设？是否将工作台留在了下一个会话可以接手的状态？


> **【中文解读】** 审查者 Agent 是专门用于审查其他 Agent 工作的独立 Agent。它检查：(1) 代码质量——可读性、可维护性、性能；(2) 正确性——逻辑错误、边界条件、错误处理；(3) 安全性——注入漏洞、敏感数据泄露。独立的审查者提供第二双眼睛。

## The Concept | 核心概念

```mermaid
flowchart LR
  Builder[Builder Agent] --> Artifacts[diff + state + feedback + verdict]
  Artifacts --> Reviewer[Reviewer Agent]
  Reviewer --> Rubric[reviewer_checklist.md]
  Reviewer --> Report[review_report.json]
  Report --> Human[Human Sign-Off]
```


> **【中文解读】** 审查者 Agent 是专门用于审查其他 Agent 工作的独立 Agent。它检查：(1) 代码质量——可读性、可维护性、性能；(2) 正确性——逻辑错误、边界条件、错误处理；(3) 安全性——注入漏洞、敏感数据泄露。独立的审查者提供第二双眼睛。

### Reviewer rubric

Five dimensions, each scored 0 to 2.

| Dimension | Question |
|-----------|----------|
| Problem fit | Did the change solve the task as stated, not a nearby task? |
| Scope discipline | Were edits confined to the contract or was the contract grown deliberately? |
| Assumptions | Are all hidden assumptions written down somewhere reviewable? |
| Verification quality | Does the acceptance command actually prove the goal, or did it prove a weaker version? |
| Handoff readiness | Could the next session pick up cleanly from the current state? |

Total out of 10. A run below 7 is a soft fail; a run below 5 is a hard fail.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

### The reviewer is a separate role, not a separate model

You can run the reviewer with the same model as the builder. The discipline is the role separation: different system prompt, different inputs, no write access to the diff. The change in posture is the change in signal.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

### The reviewer cannot edit the diff

The reviewer reads the diff, the state, the feedback, the verdict. It writes a report. It does not patch the diff. If the report says "fix this," the next builder turn does the fix; the reviewer goes back to reviewing. Mixing roles defeats the gap.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

### Reviewer rubric versus verification gate

The gate (Phase 14 · 38) checks deterministic facts: did acceptance run, did rules pass, did scope hold. The reviewer makes qualitative judgments: was this the right work, is it documented, is the handoff usable. Both are required.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

## Build It | 动手实现

`code/main.py` implements:

- A `ReviewerInputs` dataclass bundling the artifacts the reviewer reads.
- A rubric scorer with one function per dimension. Each function is deterministic and stub-grade for the lesson; real implementations would call an LLM.
- A `review_report.json` writer with the five scores, the total, and a verdict (`pass`, `soft_fail`, `hard_fail`).
- Two demo cases: a clean change and a "right tests, wrong problem" change.

Run it:

```
python3 code/main.py
```

Output: two review reports written to disk and a console table of dimensional scores.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

## Production patterns in the wild

The receipts: Cloudflare's April 2026 AI Code Review system ran 131,246 review runs across 48,095 merge requests in 5,169 repos in 30 days. Median review completed in 3 minutes 39 seconds. Up to seven specialist reviewers (security, performance, code quality, docs, release management, compliance, Engineering Codex) ran in parallel under a Review Coordinator that deduplicated findings and judged severity. Top-tier model reserved exclusively for the coordinator; specialists ran on cheaper tiers.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

Four patterns make this work at scale.

**Specialist pool, not one big reviewer.** One reviewer with a 5-dimension rubric works for solo repos. Once the codebase has security-critical, performance-critical, and docs surfaces, split into specialists with smaller prompts. The coordinator does deduplication; the specialists never run the full rubric. Model-tier separation falls out: cheap specialists, expensive coordinator.

**Bias mitigation as design requirement, not optimization.** LLM judges show four reliable biases (Adnan Masood, April 2026): position bias (GPT-4 ~40% inconsistent on (A,B) vs (B,A) ordering), verbosity bias (~15% score inflation toward longer outputs), self-preference (judges prefer outputs from the same model family), authority (judges over-rate references to known authors). Mitigations: evaluate both orderings and only count consistent wins; use 1-4 scales that explicitly reward conciseness; rotate judges across model families; strip author names before scoring.

**Calibration set, not vibes.** A 10-20 task historical set with known correct verdicts. Run the reviewer over it on every prompt change. If agreement with the historical record falls below 80%, the rubric needs revision before the reviewer ships. This is what every team eventually rediscovers; better to start with it.

**Hybrid norm with the gate.** Verification gate (Phase 14 · 38) handles the deterministic checks (did acceptance run, did tests pass, did scope hold). Reviewer handles the semantic checks (was this the right work, are assumptions documented, is the handoff usable). Anthropic's 2026 guidance is explicit on this split: don't ask the reviewer to redo what the gate already proves.

## Use It | 用框架实现

Production patterns:

- **Claude Code subagents.** A reviewer subagent runs after the builder closes a task. It posts a comment on the PR with the rubric scores.
- **OpenAI Agents SDK handoffs.** Builder hands off to Reviewer on task completion. Reviewer can hand back with a list of findings or up to a human.
- **Two-model pairing.** Builder runs on a faster cheaper model. Reviewer runs on a stronger model with smaller context, focused on judgment.

The reviewer is the second pair of eyes the workbench grows when humans cannot do every review themselves.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

## Ship It | 产出物

`outputs/skill-reviewer-agent.md` generates a project-specific reviewer rubric, a reviewer agent stub wired to the builder's artifacts, and an integration with the verification gate so human review starts from a written report instead of a blank page.

> 审查者 Agent（Reviewer Agent）专门审查其他 Agent 的输出。它从质量、安全、合规等维度评估工作成果，确保输出符合标准。

## Exercises | 练习题

1. Add a sixth dimension specific to your product domain. Defend why it is not absorbed by the existing five.
  中文翻译：思考并实践此练习。
2. Run the reviewer with two different system prompts (terse, verbose). Which produces a report a human is more likely to read?
  中文翻译：思考并实践此练习。
3. Add a `confidence` field per dimension. Refuse to ship the report when confidence in the lowest dimension is below 0.6.
  中文翻译：思考并实践此练习。
4. Build a calibration set: 10 historical task close-outs with known correct verdicts. Run the reviewer over them. Where does it disagree with the historical record?
  中文翻译：思考并实践此练习。
5. Add a "request more evidence" affordance: the reviewer can ask the builder for a specific test run before scoring. What is the right back-off so this does not loop?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Reviewer rubric | "Checklist" | Five-dimension 0-2 scoring with a written question per dimension |  |
| Soft fail | "Needs revisions" | Total below 7; builder gets findings to address |  |
| Hard fail | "Reject" | Total below 5 or any dimension at 0; halt and surface to human |  |
| Role separation | "Different prompt" | Same model can be both roles; the discipline is inputs and posture |  |
| Confidence floor | "Don't ship low-signal reports" | Refuse to emit a verdict when the rubric is uncertain |  |

## Further Reading | 延伸阅读

- [OpenAI Agents SDK handoffs](https://platform.openai.com/docs/guides/agents-sdk/handoffs)
  中文翻译：见原文。
- [Anthropic Claude Code subagents](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/sub-agents)
  中文翻译：见原文。
- [Cloudflare, Orchestrating AI Code Review at Scale](https://blog.cloudflare.com/ai-code-review/) — 7-specialist + coordinator architecture, 131k runs / 30 days
  中文翻译：见原文。
- [Agent-as-a-Judge: Evaluating Agents with Agents (OpenReview / ICLR)](https://openreview.net/forum?id=DeVm3YUnpj) — DevAI benchmark, 366 hierarchical solution requirements
  中文翻译：见原文。
- [Adnan Masood, Rubric-Based Evaluations and LLM-as-a-Judge: Methodologies, Biases, Empirical Validation](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80) — the 4 biases and mitigations
  中文翻译：见原文。
- [MLflow, LLM-as-a-Judge Evaluation](https://mlflow.org/llm-as-a-judge) — production tooling for separated builder/evaluator
  中文翻译：见原文。
- [LangChain, How to Calibrate LLM-as-a-Judge with Human Corrections](https://www.langchain.com/articles/llm-as-a-judge) — calibration-set workflow
  中文翻译：见原文。
- [Evidently AI, LLM-as-a-judge: a complete guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
  中文翻译：见原文。
- [Arize, LLM as a Judge — Primer and Pre-Built Evaluators](https://arize.com/llm-as-a-judge/)
  中文翻译：见原文。
- Phase 14 · 05 — Self-Refine and CRITIC (single-agent self-review baseline)
- Phase 14 · 30 — Eval-driven agent development (calibration set generator)
- Phase 14 · 38 — the verification gate the reviewer reads
- Phase 14 · 40 — the handoff packet the reviewer report feeds
