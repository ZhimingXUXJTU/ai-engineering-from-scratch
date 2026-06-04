# Failure Modes: Why Agents Break | 失败模式 Agent 为什么

> MASFT (Berkeley, 2025) catalogs 14 multi-agent failure modes in 3 categories. Microsoft's Taxonomy documents how existing AI failures amplify in agentic settings. Industry field data converges on five recurring modes: hallucinated actions, scope creep, cascading errors, context loss, tool misuse.

**Type:** Learn + Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 05 (Self-Refine and CRITIC), Phase 14 · 24 (Observability)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name MASFT's three failure categories and at least four specific modes in each.
- Explain why agentic failure amplifies existing AI failure modes (bias, hallucination).
- Describe the five industry-recurring modes and their mitigations.
- Implement a stdlib detector that tags agent traces with failure-mode labels.

## The Problem | 问题

Teams ship agents that work on 90% of traces. The 10% failures are not random noise — they fall into a small number of recurring categories. Once you can name them, you can monitor for them and fix them.


> **【中文解读】** Agent 系统的失败模式与普通软件不同：(1) 级联失败——一个错误决策触发后续一系列错误；(2) 目标漂移——Agent 在长链执行中偏离原始目标；(3) 过度自信——Agent 在错误结果上编造成功叙事。理解这些模式是构建可靠 Agent 的前提。

> **{【拓展：2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Ag...】}** 2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Agent 修改了无关文件导致系统崩溃（级联失败）；(2) 研究 Agent 在第 15 步开始讨论哲学问题（目标漂移）；(3) 客服 Agent 告诉用户'操作成功'但实际未执行（过度自信）。解决这些需要熔断器、意图验证和结果检查。
## The Concept | 概念

### MASFT (Berkeley, arXiv:2503.13657)

Multi-Agent System Failure Taxonomy. 14 failure modes clustered into 3 categories. Inter-annotator Cohen's Kappa 0.88 — the categories are reliably distinguishable.

Central claim: failures are fundamental design flaws in multi-agent systems, not LLM limitations to be fixed with better base models.

### Microsoft Taxonomy of Failure Mode in Agentic AI Systems

- Existing AI failures (bias, hallucination, data leakage) amplify in agentic settings.
- New failures emerge from autonomy: unintended action at scale, tool misuse, mission drift.
- The whitepaper is the risk register for agentic products.

### Characterizing Faults in Agentic AI (arXiv:2603.06847)

- Failures arise from orchestration, internal state evolution, and environment interaction.
- Not just "bad code" or "bad model output."

### LLM Agent Hallucinations Survey (arXiv:2509.18970)

Two primary manifestations:

1. **Instruction-following Deviation** — agent doesn't follow the system prompt.
2. **Long-range Contextual Misuse** — agent forgets or misapplies context from earlier turns.

Sub-intention errors: Omission (missed step), Redundancy (repeated step), Disorder (out-of-order steps).

### The five industry-recurring modes

Arize, Galileo, NimbleBrain 2024-2026 field analyses converge on:

1. **Hallucinated actions.** Agent invokes a tool that doesn't exist or fabricates arguments.
2. **Scope creep.** Agent expands task beyond the user's ask (creates extra PRs, sends extra emails).
3. **Cascading errors.** One wrong call triggers downstream effects. A phantom SKU hallucination triggers four API calls — a multi-system incident.
4. **Context loss.** Long-horizon tasks forget early-turn constraints.
5. **Tool misuse.** Calls the right tool with wrong arguments, or the wrong tool entirely.

Cascading is the killer. Agents cannot distinguish "I failed" from "the task is impossible" and often hallucinate a success message on 400 errors to close the loop.

### Mitigation: gates at every step

Automated verification gates at every step of a reasoning chain, checking factual grounding against environment state. Concretely:

- Per-step safety classifier (Lesson 21).
- Tool-call argument validation (Lesson 06).
- Cross-check retrieved content against known facts (Lesson 05, CRITIC).
- Detect success hallucination by re-probing state (was the file actually created?).

### Where failure monitoring goes wrong

- **Tagging only crashes.** Most agent failures produce valid-looking output. Need content-level checks.
- **No baseline.** Drift detection needs a last-known-good; without it you cannot say "this is getting worse."
- **Over-alerting.** Every failure produces a page. Cluster and rate-limit.

## Build It | 动手构建

`code/main.py` implements a stdlib failure-mode tagger:

- A synthetic trace dataset covering the five modes.
- Detector functions per mode (signature patterns on tool calls, outputs, repeat actions).
- A tagger that labels each trace and reports mode distribution.

Run it:

```
python3 code/main.py
```

Output: per-trace labels + aggregate distribution, a cheap reproduction of what Phoenix's trace clustering surfaces.

## Use It | 使用方法

- **Phoenix** for production drift clustering (Lesson 24).
- **Langfuse** for session replay + annotation.
- **Custom** for domain-specific signatures your observability platform can't detect.

## Ship It | 部署上线

`outputs/skill-failure-detector.md` generates failure-mode detectors tailored to your domain, wired to a trace store.

## Exercises | 练习题

1. Add a detector for "success hallucination": agent returns success but the target state is unchanged.
   *思考并实践此练习*
2. Tag 100 real traces from a product you've built. Which mode dominates? What's the cost of fixing it?
   *思考并实践此练习*
3. Implement a "cascade radius" metric: given a failure at step N, how many downstream steps did it affect?
   *思考并实践此练习*
4. Read MASFT's 14 failure modes. Pick three that apply to your product. Write detectors.
   *思考并实践此练习*
5. Wire one detector into a CI job: fail the build if >=5% of traces tag a mode.
   *思考并实践此练习*

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| MASFT | "Multi-agent failure taxonomy" | Berkeley 14-mode categorization |  |
| Cascading error | "Ripple failure" | One early mistake propagates through N steps |  |
| Context loss | "Forgot the constraint" | Long-horizon turn drops early-turn facts |  |
| Tool misuse | "Wrong tool / wrong args" | Valid call, wrong invocation |  |
| Success hallucination | "Faked completion" | Agent claims success on a 400; state unchanged |  |
| Scope creep | "Overreach" | Agent does more than asked |  |
| Instruction-following deviation | "Disobedience" | Ignores system prompt or user constraint |  |
| Sub-intention errors | "Plan bugs" | Omission, redundancy, disorder in plan execution |  |

## Further Reading | 延伸阅读

- [Cemri et al., MASFT (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657) — 14 failure modes, 3 categories
- [Microsoft, Taxonomy of Failure Mode in Agentic AI Systems](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) — risk register
- [Arize Phoenix](https://docs.arize.com/phoenix) — drift clustering in practice
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — when simpler patterns avoid modes entirely
