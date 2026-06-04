# 会话 交接 多

> The session is going to end. The work is not. The handoff packet is the artifact that turns "the agent worked for an hour" into "the next session is productive in the first minute." Build it on purpose, not as an afterthought.


**类型：** 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 34 (Repo Memory), Phase 14 · 38 (Verification), Phase 14 · 39 (Reviewer)
**预计时间：** ~50 minutes

## 学习目标

- Identify the seven fields every handoff packet needs.
- Generate a handoff from the workbench artifacts without hand-writing prose.
- Trim large feedback logs into a handoff-sized summary.
- Make the next session's first action deterministic.

## 问题引入

> **【中文解读】** 多会话交接处理 Agent 跨多个会话的连续性。当一次会话因超时、token 限制或用户中断而结束时，Agent 需要将上下文传递给下一次会话。关键技术：(1) 会话摘要——压缩关键信息；(2) 检查点——保存中间状态；(3) 恢复协议——新会话如何加载旧状态。

## 核心概念

```mermaid
flowchart LR
  State[agent_state.json] --> Generator[generate_handoff.py]
  Verdict[verification_report.json] --> Generator
  Review[review_report.json] --> Generator
  Feedback[feedback_record.jsonl] --> Generator
  Generator --> Handoff[handoff.md + handoff.json]
  Handoff --> Next[Next Session]
```
> **【中文解读】** 多会话交接处理 Agent 跨多个会话的连续性。当一次会话因超时、token 限制或用户中断而结束时，Agent 需要将上下文传递给下一次会话。关键技术：(1) 会话摘要——压缩关键信息；(2) 检查点——保存中间状态；(3) 恢复协议——新会话如何加载旧状态。
### Seven fields every handoff carries
| Field | Question it answers |
|-------|---------------------|
| `summary` | One paragraph of what was done |
| `changed_files` | The diff at a glance |
| `commands_run` | What was actually executed |
| `failed_attempts` | What was tried and why it did not work |
| `open_risks` | What could bite next session, with severity |
| `next_action` | The first concrete step next session takes |
| `verdict_pointer` | Path to the verification + review reports |
The `next_action` field is the load-bearing one. A handoff with everything except `next_action` is a status report, not a handoff.
### Handoffs are generated, not written
A hand-written handoff is a handoff that gets skipped on a hard day. The generator reads the workbench artifacts and emits the packet. The agent's job is to leave the workbench in a state the generator can summarize, not to write the summary.
### Two forms: human-readable and machine-readable
`handoff.md` is what the human reads. `handoff.json` is what the next agent loads. Both come from the same source artifacts. If they diverge, the JSON wins.
### Feedback log trimming
The full `feedback_record.jsonl` may be hundreds of entries. The handoff carries only the last K plus every entry with a non-zero exit. The next session loads the full log if it needs to, but the packet stays small.

## 动手实现

`code/main.py` implements:
- A loader that gathers state, verdict, review, and feedback into a single `WorkbenchSnapshot`.
- A `generate_handoff(snapshot) -> (markdown, payload)` function.
- A filter that picks the last K feedback entries plus all non-zero exits.
- A demo run that writes `handoff.md` and `handoff.json` next to the script.
Run it:
```
python3 code/main.py
```
Output: a printed handoff body, plus both files on disk.
## Production patterns in the wild
Codex CLI, Claude Code, and OpenCode each ship a different compaction story; the structured handoff packet sits on top of all three.
**Compaction strategies vary; the packet schema does not.** Codex CLI's POST /v1/responses/compact is a server-side opaque AES blob (fast path for OpenAI models); the fallback is a local "handoff summary" appended as a `_summary` user-role message. Claude Code runs five-stage progressive compaction at 95% of context. OpenCode does timestamp-based message hiding plus a 5-heading LLM summary. Three different mechanisms, same need: serialize what survives compression into a portable artifact. The packet is that artifact.
**Fresh-session handoff is not compaction.** Compaction extends a session; handoff closes one cleanly and starts the next. The Hermes Issue #20372 framing (April 2026) is right: when in-place compression starts degrading, the agent should write a compact handoff, end the session, and resume in fresh context. The packet is what makes that transition cheap. The mistake is to keep compressing until quality collapses; the fix is to budget for an early, clean handoff.
**One active handoff per branch and topic.** Multi-agent coordination breaks down on stale handoffs more than on bad model output. Always include `branch`, `last_known_good_commit`, and a `status` of `active | superseded | archived`. Stale handoffs are archived; only the active one drives the next session. This is the difference between handoff-as-notes and handoff-as-state.
**Wrap up before 50-75% context, not at the wall.** The hand-written-pattern playbook (CLAUDE.md + HANDOVER.md) reports best results when the session ends at 50-75% context budget instead of 95%. The packet generator runs cleanly before compression artifacts pollute the source state. Cheap to write while context is intact; expensive when the model is already losing its place.

## 用框架实现

- **Session-end hook.** The runtime fires the generator when the user closes the chat. The packet goes into `outputs/handoff/<session_id>/`.
- **PR template.** The generator's markdown is also a PR body. Reviewers read it without opening five other files.
- **Cross-agent handoff.** Build with one product (Claude Code), continue with another (Codex). The packet is the lingua franca.

## 产出物

`outputs/skill-handoff-generator.md` produces a generator tuned to a project's artifact paths, an end-of-session hook that runs it, and a `handoff.json` schema the next agent reads on startup.

## 练习题

1. Add an `assumptions_to_validate` field that surfaces every assumption the builder logged but the reviewer did not score above 1.
   *思考并实践此练习*
2. Trim the feedback summary differently for failing runs versus passing ones. Defend the asymmetry.
   *思考并实践此练习*
3. Include a "questions for the human" list. What is the threshold for a question to make it into the packet versus into a chat message?
   *思考并实践此练习*
4. Make the generator idempotent: running it twice produces the same packet. What needs to be stable for that to hold?
   *思考并实践此练习*
5. Add a "next session prereqs" section listing exactly the artifacts the next session must load before acting.
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Handoff packet | "Session summary" |
| Next action | "What to do first" |
| Feedback trim | "Log summary" |
| Status report | "What we did" |
| Verdict pointer | "Receipt" |

## 延伸阅读

