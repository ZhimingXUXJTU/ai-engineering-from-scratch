# Bounded Self-Improvement Designs | 自我改进 有界

> Research has converged on four primitives for bounding a self-improvement loop. Formal invariants that must hold across every edit. Alignment anchors that cannot be modified. Multi-objective constraints where every dimension (safety, fairness, robustness) must hold, not just performance. Regression detection that pauses the loop when historical metrics suggest capability loss. None of them is a proof of safety — information-theoretic results (Kolmogorov complexity, Lob's theorem) bound what any system can prove about its own successors. They are mitigations that raise the cost of silent failure.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python (stdlib, bounded-loop with invariant check)
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM)
**Time:** ~60 minutes | **时间:** ~60 minutes

## The Problem | 问题引入

Lesson 7's race simulator showed that small rate differences compound into large gaps. Lesson 4's DGM case study showed that loops can actively game their own evaluators.

> 第 7 课的竞赛模拟器显示小的速率差异会复合成大差距。第 4 课的 DGM 案例显示循环可以主动博弈自己的评估器。 Lesson 4's DGM case study showed that loops can actively game their own evaluators. Both results point to the same engineering question: what constraints can you put on a self-improvement loop such that the constraints cannot be silently weakened by the loop itself?

The ICLR 2026 RSI Workshop summary (openreview.net/pdf?id=OsPQ6zTQXV) identifies four such primitives. Anthropic's RSP v3.0 (Lesson 19) and DeepMind's FSF v3 (Lesson 20) both reference them in capability thresholds. The Meta HyperAgents work and community frameworks like SAHOO (March 2026) implement subsets in production.


> **【中文解读】** 有界自我改进探讨 AI 系统在安全边界内改进自身能力的可能性和限制。核心问题：(1) 改进循环是否可验证——系统能否证明改进后的版本等价或更优？(2) 边界如何定义——哪些方面的改进是允许的？(3) 是否存在收敛保证——改进是否会收敛到某个上限？

The honest framing: these are mitigations. Information-theoretic results bound what any system can prove about its own successor, and no current design closes the problem formally.

> 诚实的框架：这些是缓解措施。信息论结果限制了任何系统对其自身后继者能证明的内容。 Information-theoretic results bound what any system can prove about its own successor, and no current design closes the problem formally. A well-bounded loop is safer than an unbounded one, not safe in absolute terms.

## The Concept | 核心概念

### Primitive 1: formal invariants

An invariant is a property that must hold before and after every self-modification.

> 不变量是每次自我修改前后必须成立的属性。例如：输出分布以固定宪法头为条件；没有工具调用到达未授权端点。 Examples:

- Output distribution is conditioned on a fixed constitution header (Lesson 17).
- No tool call goes to an unauthorized endpoint.
- Memory writes go through a logged, signed path.
- The evaluator's module hash matches the approved version.

Invariants are checked by external code the loop cannot edit. If a proposed modification violates an invariant, it is rejected. This catches the DGM-style evaluator-tampering mode (Lesson 4).

The hard part is choosing invariants that are necessary for safety and computable in reasonable time. Over-specifying stalls progress; under-specifying lets the loop walk past important properties.

### Primitive 2: alignment anchors

An alignment anchor is an immutable representation of the loop's core objective, pinned outside the loop's edit surface.

> 对齐锚点是循环核心目标的不可变表示，固定在循环编辑面之外。锚点的作用是防止目标漂移。, pinned outside the loop's edit surface. Examples:

- A constitutional text (Lesson 17) that is loaded from a read-only location on every invocation.
- An evaluator in a separate repository with independent access control.
- A tool-permission manifest signed by a human and re-verified each cycle.

The anchor's role is to prevent objective drift. The loop may improve how it pursues the objective, but cannot edit what the objective is.

The subtle failure mode: an anchor the loop cannot edit can still be reinterpreted by a loop that drifts in how it reads the anchor. Constitutional AI (Lesson 17) is explicitly reason-based to handle novel situations; that reasoning layer is where interpretation drift lives. Anchors are necessary, not sufficient.

### Primitive 3: multi-objective constraints

A loop that optimizes a single scalar score will find shortcuts. A loop that must simultaneously satisfy multiple hard constraints has fewer shortcuts available.

> 优化单一标量分数的循环会找到捷径。必须同时满足多个硬约束的循环可用的捷径更少。 A loop that must simultaneously satisfy multiple hard constraints has fewer shortcuts available. Typical axes:

- Performance (task-level benchmark)
- Safety (red-team evaluations, refusal rate on known-bad)
- Fairness (disparate-impact bounds on sensitive subgroups)
- Robustness (OOD test sets, adversarial input handling)

A modification is accepted only if every constraint holds. Lesson 13's cost governor stacks this with financial constraints. Lesson 18's Llama Guard plugs in as a safety axis.

### Primitive 4: regression detection

Each cycle's scores are compared against historical distributions. A drop beyond configured tolerance pauses the loop. This catches silent capability loss that would otherwise be absorbed into the running average as the loop "improved past" it.

A practical implementation: store the last N cycles' per-task scores. Each new cycle computes a per-task delta. If any delta drops below a threshold, the cycle is rejected and a human reviews.

### Information-theoretic limits

Kolmogorov complexity and Lob's theorem set upper bounds on what a system can prove about itself. Schmidhuber's formal Godel Machine (Lesson 4) aimed for the highest such bound; nobody has completed a non-trivial proof. Lob's result says: if a system provably believes "I will do X if I prove I should do X," it will do X without proving it should, a well-known self-reference failure.

The implication for our primitives: they cannot close the safety problem. They make silent failure more expensive. A malicious or drifted loop that would quietly bypass a missing check must now actively undermine an explicit one, which is a more detectable signature.

### A worked example

Suppose an agent proposes an edit. The gating stack:

1. Invariant checks: module hashes, tool-permission manifest, constitutional header.
2. Anchor check: objective statement matches approved version (byte-wise or semantically).
3. Multi-objective evaluation: performance, safety, fairness, robustness axes.
4. Regression detection: no axis drops more than tolerance.

All four must pass for the edit to land. Any single failure pauses the loop.

## Use It | 用框架实现

`code/main.py` runs a bounded self-improvement loop on the DGM-style toy from Lesson 4, but with the four primitives layered on top. Each primitive can be enabled or disabled individually. The demonstration is that each primitive catches a specific failure class, and that removing any one of them lets that failure class through.

## Ship It | 产出物

`outputs/skill-bounded-loop-review.md` audits a proposed bounded loop and scores which of the four primitives it actually implements versus claims to.

## Exercises | 练习题

1. Run `code/main.py` with all primitives enabled. Confirm the loop still improves on the primary metric without letting the hack win.

2. Disable regression detection. Construct an input where this leads to silent capability loss being accepted.

3. Disable the multi-objective constraint. Show the loop converges on the performance axis while a safety axis drops.

4. Design an alignment anchor for a coding agent. What text, stored where, checked how?

5. Read the ICLR 2026 RSI Workshop summary. Pick one of the four primitives and propose a concrete improvement to the current state of the art.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |  |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |  |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |  |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |  |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |  |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |  |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |  |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |  |

## Further Reading | 延伸阅读

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) — the four-primitive convergence.
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — multi-objective capability thresholds.
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — deceptive-alignment monitoring as an invariant primitive.
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) — the formal-proof ancestor of these primitives.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — the reason-based alignment anchor.
