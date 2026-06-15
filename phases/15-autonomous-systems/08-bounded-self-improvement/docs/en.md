# Bounded Self-Improvement Designs | 有界自我改进设计

> Research has converged on four primitives for bounding a self-improvement loop. Formal invariants that must hold across every edit. Alignment anchors that cannot be modified. Multi-objective constraints where every dimension (safety, fairness, robustness) must hold, not just performance. Regression detection that pauses the loop when historical metrics suggest capability loss. None of them is a proof of safety — information-theoretic results (Kolmogorov complexity, Lob's theorem) bound what any system can prove about its own successors. They are mitigations that raise the cost of silent failure.

> **【中文解读】** 研究已收敛到四个约束自我改进循环的原语。每次编辑必须成立的形式不变量。不能被修改的对齐锚点。每个维度（安全、公平、鲁棒）都必须成立的多目标约束而非仅性能。当历史指标表明能力损失时暂停循环的回归检测。它们都不是安全证明——信息论结果（Kolmogorov 复杂性、Lob 定理）限制了任何系统能对其自身后继者证明的内容。它们是提高静默失败成本的缓解。

> **【拓展：四个原语 → 一个守门栈】** 实际部署中四个原语组合成"守门栈"——每次自修改要落地必须依次通过：不变量检查（模块哈希、工具权限清单、宪法头）→ 对齐锚点检查（目标陈述匹配批准版本）→ 多目标评估（性能、安全、公平、鲁棒）→ 回归检测（无轴下降超阈值）。任一失败即暂停循环。这是 ICLR 2026 RSI 工作坊、Anthropic RSP v3.0、DeepMind FSF v3 共同采纳的设计共识。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Lesson 7's race simulator showed that small rate differences compound into large gaps. Lesson 4's DGM case study showed that loops can actively game their own evaluators.

> 第 7 课的赛跑模拟器显示小的速率差异复合成大差距。第 4 课的 DGM 案例显示循环可以主动博弈自己的评估器。

Both results point to the same engineering question: what constraints can you put on a self-improvement loop such that the constraints cannot be silently weakened by the loop itself?

> 两个结果指向同一工程问题：你能在自我改进循环上施加什么约束，使这些约束不能被循环自身静默削弱？

The ICLR 2026 RSI Workshop summary (openreview.net/pdf?id=OsPQ6zTQXV) identifies four such primitives. Anthropic's RSP v3.0 (Lesson 19) and DeepMind's FSF v3 (Lesson 20) both reference them in capability thresholds. The Meta HyperAgents work and community frameworks like SAHOO (March 2026) implement subsets in production.

> ICLR 2026 RSI 工作坊摘要（openreview.net/pdf?id=OsPQ6zTQXV）识别四个此类原语。Anthropic 的 RSP v3.0（第 19 课）和 DeepMind 的 FSF v3（第 20 课）都在能力阈值中引用它们。Meta HyperAgents 工作和 SAHOO（2026 年 3 月）等社区框架在生产中实现子集。

> **【中文解读】** 有界自我改进探讨 AI 系统在安全边界内改进自身能力的可能性和限制。核心问题：(1) 改进循环是否可验证——系统能否证明改进后的版本等价或更优？(2) 边界如何定义——哪些方面的改进是允许的？(3) 是否存在收敛保证——改进是否会收敛到某个上限？

The honest framing: these are mitigations. Information-theoretic results bound what any system can prove about its own successor, and no current design closes the problem formally.

> 诚实的框架：这些是缓解措施。信息论结果限制了任何系统对其自身后继者能证明的内容。

A well-bounded loop is safer than an unbounded one, not safe in absolute terms.

> 良好有界的循环比无界的更安全，不是绝对安全。

## The Concept | 核心概念

### Primitive 1: formal invariants | 原语 1：形式不变量

An invariant is a property that must hold before and after every self-modification.

> 不变量是每次自我修改前后必须成立的属性。

Examples:

> 例子：

- Output distribution is conditioned on a fixed constitution header (Lesson 17).
  中文翻译：输出分布以固定宪法头为条件（第 17 课）。
- No tool call goes to an unauthorized endpoint.
  中文翻译：没有工具调用到达未授权端点。
- Memory writes go through a logged, signed path.
  中文翻译：内存写入通过记录、签名路径。
- The evaluator's module hash matches the approved version.
  中文翻译：评估器的模块哈希匹配批准版本。

Invariants are checked by external code the loop cannot edit. If a proposed modification violates an invariant, it is rejected. This catches the DGM-style evaluator-tampering mode (Lesson 4).

> 不变量由循环无法编辑的外部代码检查。如果提议的修改违反不变量，被拒绝。这捕获 DGM 式评估器篡改模式（第 4 课）。

The hard part is choosing invariants that are necessary for safety and computable in reasonable time. Over-specifying stalls progress; under-specifying lets the loop walk past important properties.

> 困难部分是选择对安全必要且可在合理时间内计算的不变量。过度规范阻碍进展；规范不足让循环走过重要属性。

### Primitive 2: alignment anchors | 原语 2：对齐锚点

An alignment anchor is an immutable representation of the loop's core objective, pinned outside the loop's edit surface.

> 对齐锚点是循环核心目标的不可变表示，固定在循环编辑面之外。

Examples:

> 例子：

- A constitutional text (Lesson 17) that is loaded from a read-only location on every invocation.
  中文翻译：每次调用从只读位置加载的宪法文本（第 17 课）。
- An evaluator in a separate repository with independent access control.
  中文翻译：在独立访问控制的独立仓库中的评估器。
- A tool-permission manifest signed by a human and re-verified each cycle.
  中文翻译：由人类签名每周期重新验证的工具权限清单。

The anchor's role is to prevent objective drift. The loop may improve how it pursues the objective, but cannot edit what the objective is.

> 锚点的作用是防止目标漂移。循环可改进它如何追求目标，但不能编辑目标是什么。

The subtle failure mode: an anchor the loop cannot edit can still be reinterpreted by a loop that drifts in how it reads the anchor. Constitutional AI (Lesson 17) is explicitly reason-based to handle novel situations; that reasoning layer is where interpretation drift lives. Anchors are necessary, not sufficient.

> 微妙的失败模式：循环无法编辑的锚点仍可被在读取锚点方式上漂移的循环重新解释。Constitutional AI（第 17 课）明确基于推理以处理新情况；该推理层是解释漂移所在。锚点必要但不充分。

### Primitive 3: multi-objective constraints | 原语 3：多目标约束

A loop that optimizes a single scalar score will find shortcuts. A loop that must simultaneously satisfy multiple hard constraints has fewer shortcuts available.

> 优化单一标量分数的循环会找到捷径。必须同时满足多个硬约束的循环可用的捷径更少。

Typical axes:

> 典型轴：

- Performance (task-level benchmark)
  中文翻译：性能（任务级基准）
- Safety (red-team evaluations, refusal rate on known-bad)
  中文翻译：安全（红队评估、已知坏例的拒绝率）
- Fairness (disparate-impact bounds on sensitive subgroups)
  中文翻译：公平（敏感子群体上的差异影响边界）
- Robustness (OOD test sets, adversarial input handling)
  中文翻译：鲁棒性（OOD 测试集、对抗输入处理）

A modification is accepted only if every constraint holds. Lesson 13's cost governor stacks this with financial constraints. Lesson 18's Llama Guard plugs in as a safety axis.

> 修改仅在所有约束成立时被接受。第 13 课的成本治理器将其与金融约束叠加。第 18 课的 Llama Guard 作为安全轴插入。

### Primitive 4: regression detection | 原语 4：回归检测

Each cycle's scores are compared against historical distributions. A drop beyond configured tolerance pauses the loop. This catches silent capability loss that would otherwise be absorbed into the running average as the loop "improved past" it.

> 每周期的分数与历史分布比较。超出配置容忍度的下降暂停循环。这捕获会被循环"改进越过"而吸收到运行平均中的静默能力损失。

A practical implementation: store the last N cycles' per-task scores. Each new cycle computes a per-task delta. If any delta drops below a threshold, the cycle is rejected and a human reviews.

> 实际实现：存储最近 N 个周期的每任务分数。每个新周期计算每任务增量。如果任何增量降到阈值以下，周期被拒绝并由人类审查。

### Information-theoretic limits | 信息论极限

Kolmogorov complexity and Lob's theorem set upper bounds on what a system can prove about itself. Schmidhuber's formal Godel Machine (Lesson 4) aimed for the highest such bound; nobody has completed a non-trivial proof. Lob's result says: if a system provably believes "I will do X if I prove I should do X," it will do X without proving it should, a well-known self-reference failure.

> Kolmogorov 复杂性和 Lob 定理为系统能对自己证明的内容设置上限。Schmidhuber 的形式 Godel Machine（第 4 课）瞄准最高此类边界；没人完成过非平凡证明。Lob 结果说：如果系统可证地相信"如果证明我应该做 X，我会做 X"，它会做 X 而不证明应该，一个已知的自引用失败。

The implication for our primitives: they cannot close the safety problem. They make silent failure more expensive. A malicious or drifted loop that would quietly bypass a missing check must now actively undermine an explicit one, which is a more detectable signature.

> 对我们原语的含义：它们不能闭合安全问题。它们让静默失败更昂贵。会静默绕过缺失检查的恶意或漂移循环现在必须主动破坏显式检查，这是更可检测的签名。

### A worked example | 一个工作示例

Suppose an agent proposes an edit. The gating stack:

> 假设 Agent 提议一个编辑。守门栈：

1. Invariant checks: module hashes, tool-permission manifest, constitutional header.
   中文翻译：不变量检查：模块哈希、工具权限清单、宪法头。
2. Anchor check: objective statement matches approved version (byte-wise or semantically).
   中文翻译：锚点检查：目标陈述匹配批准版本（字节或语义）。
3. Multi-objective evaluation: performance, safety, fairness, robustness axes.
   中文翻译：多目标评估：性能、安全、公平、鲁棒轴。
4. Regression detection: no axis drops more than tolerance.
   中文翻译：回归检测：无轴下降超容忍度。

All four must pass for the edit to land. Any single failure pauses the loop.

> 全部四个必须通过编辑才能落地。任一失败暂停循环。

## Use It | 用框架实现

`code/main.py` runs a bounded self-improvement loop on the DGM-style toy from Lesson 4, but with the four primitives layered on top. Each primitive can be enabled or disabled individually. The demonstration is that each primitive catches a specific failure class, and that removing any one of them lets that failure class through.

> `code/main.py` 在第 4 课的 DGM 式玩具上运行有界自我改进循环，但在上面叠加四个原语。每个原语可单独启用或禁用。演示是每个原语捕获特定失败类，移除任何一个让该失败类通过。

## Ship It | 产出物

`outputs/skill-bounded-loop-review.md` audits a proposed bounded loop and scores which of the four primitives it actually implements versus claims to.

> `outputs/skill-bounded-loop-review.md` 审计提议的有界循环并评分它实际实现四个原语中的哪些 vs 声称的。

## Exercises | 练习题

1. Run `code/main.py` with all primitives enabled. Confirm the loop still improves on the primary metric without letting the hack win.
   中文翻译：启用所有原语运行 `code/main.py`。确认循环仍在主指标上改进而不让篡改获胜。

2. Disable regression detection. Construct an input where this leads to silent capability loss being accepted.
   中文翻译：禁用回归检测。构造一个这导致接受静默能力损失的输入。

3. Disable the multi-objective constraint. Show the loop converges on the performance axis while a safety axis drops.
   中文翻译：禁用多目标约束。展示循环在性能轴收敛而安全轴下降。

4. Design an alignment anchor for a coding agent. What text, stored where, checked how?
   中文翻译：为编码 Agent 设计对齐锚点。什么文本、存储何处、如何检查？

5. Read the ICLR 2026 RSI Workshop summary. Pick one of the four primitives and propose a concrete improvement to the current state of the art.
   中文翻译：阅读 ICLR 2026 RSI 工作坊摘要。选四个原语之一并对当前技术水平提出具体改进。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Further Reading | 延伸阅读

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) — the four-primitive convergence.
  中文翻译：四原语收敛。
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — multi-objective capability thresholds.
  中文翻译：多目标能力阈值。
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — deceptive-alignment monitoring as an invariant primitive.
  中文翻译：作为不变量原语的欺骗性对齐监控。
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) — the formal-proof ancestor of these primitives.
  中文翻译：这些原语的形式证明祖先。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — the reason-based alignment anchor.
  中文翻译：基于推理的对齐锚点。
