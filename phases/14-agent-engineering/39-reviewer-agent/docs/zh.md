# 审查者

> The agent that wrote the code cannot grade it. A reviewer is a second loop with a different system prompt, a different goal, and read-only access to everything the builder produced. The gap between builder and reviewer is where most reliability lives.


**类型：** 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 38 (Verification Gate)
**预计时间：** ~55 minutes

## 学习目标

- State why the same agent cannot reliably review its own work.
- Build a reviewer agent loop that consumes builder artifacts and emits a structured review report.
- Author a reviewer rubric that grades specific dimensions, not vibes.
- Wire the reviewer into the workbench so the human review step starts from a real artifact.

## 问题引入

> **【中文解读】** 审查者 Agent 是专门用于审查其他 Agent 工作的独立 Agent。它检查：(1) 代码质量——可读性、可维护性、性能；(2) 正确性——逻辑错误、边界条件、错误处理；(3) 安全性——注入漏洞、敏感数据泄露。独立的审查者提供第二双眼睛。

## 核心概念

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
### The reviewer is a separate role, not a separate model
You can run the reviewer with the same model as the builder. The discipline is the role separation: different system prompt, different inputs, no write access to the diff. The change in posture is the change in signal.
### The reviewer cannot edit the diff
The reviewer reads the diff, the state, the feedback, the verdict. It writes a report. It does not patch the diff. If the report says "fix this," the next builder turn does the fix; the reviewer goes back to reviewing. Mixing roles defeats the gap.
### Reviewer rubric versus verification gate
The gate (Phase 14 · 38) checks deterministic facts: did acceptance run, did rules pass, did scope hold. The reviewer makes qualitative judgments: was this the right work, is it documented, is the handoff usable. Both are required.

## 动手实现

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
## Production patterns in the wild
The receipts: Cloudflare's April 2026 AI Code Review system ran 131,246 review runs across 48,095 merge requests in 5,169 repos in 30 days. Median review completed in 3 minutes 39 seconds. Up to seven specialist reviewers (security, performance, code quality, docs, release management, compliance, Engineering Codex) ran in parallel under a Review Coordinator that deduplicated findings and judged severity. Top-tier model reserved exclusively for the coordinator; specialists ran on cheaper tiers.
Four patterns make this work at scale.
**Specialist pool, not one big reviewer.** One reviewer with a 5-dimension rubric works for solo repos. Once the codebase has security-critical, performance-critical, and docs surfaces, split into specialists with smaller prompts. The coordinator does deduplication; the specialists never run the full rubric. Model-tier separation falls out: cheap specialists, expensive coordinator.
**Bias mitigation as design requirement, not optimization.** LLM judges show four reliable biases (Adnan Masood, April 2026): position bias (GPT-4 ~40% inconsistent on (A,B) vs (B,A) ordering), verbosity bias (~15% score inflation toward longer outputs), self-preference (judges prefer outputs from the same model family), authority (judges over-rate references to known authors). Mitigations: evaluate both orderings and only count consistent wins; use 1-4 scales that explicitly reward conciseness; rotate judges across model families; strip author names before scoring.
**Calibration set, not vibes.** A 10-20 task historical set with known correct verdicts. Run the reviewer over it on every prompt change. If agreement with the historical record falls below 80%, the rubric needs revision before the reviewer ships. This is what every team eventually rediscovers; better to start with it.
**Hybrid norm with the gate.** Verification gate (Phase 14 · 38) handles the deterministic checks (did acceptance run, did tests pass, did scope hold). Reviewer handles the semantic checks (was this the right work, are assumptions documented, is the handoff usable). Anthropic's 2026 guidance is explicit on this split: don't ask the reviewer to redo what the gate already proves.

## 用框架实现

- **Claude Code subagents.** A reviewer subagent runs after the builder closes a task. It posts a comment on the PR with the rubric scores.
- **OpenAI Agents SDK handoffs.** Builder hands off to Reviewer on task completion. Reviewer can hand back with a list of findings or up to a human.
- **Two-model pairing.** Builder runs on a faster cheaper model. Reviewer runs on a stronger model with smaller context, focused on judgment.

## 产出物

`outputs/skill-reviewer-agent.md` generates a project-specific reviewer rubric, a reviewer agent stub wired to the builder's artifacts, and an integration with the verification gate so human review starts from a written report instead of a blank page.

## 练习题

1. Add a sixth dimension specific to your product domain. Defend why it is not absorbed by the existing five.
   *思考并实践此练习*
2. Run the reviewer with two different system prompts (terse, verbose). Which produces a report a human is more likely to read?
   *思考并实践此练习*
3. Add a `confidence` field per dimension. Refuse to ship the report when confidence in the lowest dimension is below 0.6.
   *思考并实践此练习*
4. Build a calibration set: 10 historical task close-outs with known correct verdicts. Run the reviewer over them. Where does it disagree with the historical record?
   *思考并实践此练习*
5. Add a "request more evidence" affordance: the reviewer can ask the builder for a specific test run before scoring. What is the right back-off so this does not loop?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Reviewer rubric | "Checklist" |
| Soft fail | "Needs revisions" |
| Hard fail | "Reject" |
| Role separation | "Different prompt" |
| Confidence floor | "Don't ship low-signal reports" |

## 延伸阅读

