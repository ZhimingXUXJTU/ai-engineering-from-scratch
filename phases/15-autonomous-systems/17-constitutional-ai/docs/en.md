# Constitutional AI and Rule Overrides | Constitutional AI 与规则覆盖

> Anthropic's January 22, 2026 Claude Constitution runs 79 pages and is CC0. It moves from rule-based to reason-based alignment and establishes a four-tier priority hierarchy: (1) safety and supporting human oversight, (2) ethics, (3) Anthropic guidelines, (4) helpfulness. Behaviours split into hardcoded prohibitions (bioweapons uplift, CSAM) that operators and users cannot override and soft-coded defaults that operators can adjust within defined bounds. The 2022 original (Bai et al.) trained harmlessness via self-critique and RLAIF against a constitution. The honest caveat: reason-based alignment relies on the model generalising principles to unanticipated situations. Anthropic's own 2023 participatory experiment showed ~50% divergence between public-sourced and corporate principles; the 2026 version did not incorporate those findings.

> **【中文解读】** Anthropic 2026 年 1 月 22 日的 Claude Constitution 79 页 CC0。从基于规则转向基于推理的对齐，建立四层优先级层次：(1) 安全和支持人类监督、(2) 伦理、(3) Anthropic 指南、(4) 有用性。行为分为操作员和用户不能覆盖的硬编码禁令（生物武器提升、CSAM）和操作员可在定义边界内调整的软编码默认。2022 原始版本（Bai 等人）通过自我批评和 RLAIF 训练无害性。诚实警告：基于推理的对齐依赖模型将原则泛化到未预期情况。Anthropic 自己 2023 年的参与式实验显示公众来源和企业原则约 50% 分歧；2026 版本未纳入这些发现。

> **【拓展：四层优先级 + 双层禁令】** 四层层次（安全 > 伦理 > 指南 > 有用性）与 Unix 优先级或网络 QoS 相同——旨在产生可预测解析。硬编码禁令是 RBA（基于规则对齐），无论操作员或用户指令都不可覆盖；其他通过四层层次基于推理。两者都是必要的：仅基于推理不能闭合尾部——攻击者让模型接受前提（"我们是持牌生物武器研究实验室"）就能绕过依赖案例推理的原则。硬编码禁令不向前提框架弯折。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·06（AAR）、Phase 15·10（权限模式）、Phase 11·10（RLHF/RLAIF 基础）。Constitutional AI = "用 AI 监督 AI"的对齐方法。
> 💡 **【类比】** Constitutional AI = "AI 的自我修养"。RLHF = 父母每次纠正孩子（人工反馈，慢且贵）；CAI = 孩子读了《学生守则》后自己批评自己（AI 反馈，便宜可扩展）。2026 Claude Constitution 79 页四层优先级：安全 > 伦理 > 公司指南 > 有用性。硬禁令（生物武器、CSAM）无论用户怎么指令都不行——这是规则；其他通过推理判断。
> 🤔 **【困惑】** Q: 推理对齐能被绕过吗？— 能！攻击者设前提"我是持牌生物武器实验室" → 模型按推理允许 → 绕过原则。修复：硬禁令不向前提弯折（无论谁说什么，CSAM 就是不能生成）。推理 + 规则两层防御：推理覆盖大多数情况，规则覆盖推理被绕过的尾部。

## The Problem | 问题引入

> **【中文解读】** Constitutional AI（CAI, Anthropic 2022）是一种通过'宪法'（一组原则）指导 AI 行为的方法。模型在生成响应时自我检查是否符合这些原则，并在违反时自我纠正。CAI 的核心创新是用 AI 反馈替代人类反馈（RLAIF），减少对人类标注的依赖。

> **【拓展：constitutional ai】** Constitutional AI 是 Anthropic 安全方法论的基石。它使用一组'宪法原则'（如'不要帮助用户做危险的事情'）让模型自我监督。流程：(1) 模型生成初始响应；(2) 用宪法原则批评自己的响应；(3) 根据批评修改响应；(4) 在修改后的响应上训练。Claude 系列模型都经过 CAI 训练。

A fielded agent sees inputs that its designers never saw. No rule list is long enough to cover them.

> 部署的 Agent 会看到设计师从未见过的输入。没有规则列表足以覆盖它们。

No rule list is short enough to apply quickly under compute pressure. The practical question: how do you align an agent to principles that survive both a long tail of cases and fast inference?

> 没有规则列表短到能在计算压力下快速应用。实际问题：如何将 Agent 对齐到能在长尾案例和快速推理下都存活的原则？

Rule-based alignment (RBA): list every disallowed thing. Fast to check, easy to audit, impossible to keep current, often over-refuses on close analogs it didn't anticipate. Reason-based alignment (the 2026 Claude Constitution): encode principles, let the model reason. Scales across unseen cases, harder to audit, failure mode is principle-misapplication rather than miss-the-rule.

> 基于规则对齐（RBA）：列出每个禁止的事。检查快、审计易、不可能保持当前、常对未预期的近似物过度拒绝。基于推理对齐（2026 Claude Constitution）：编码原则让模型推理。跨未见案例扩展、更难审计、失败模式是原则误用而非遗漏规则。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The 2026 Constitution takes an explicit middle position. Hardcoded prohibitions are RBA: never, regardless of operator or user instruction.

> 2026 年宪法采取了明确的中间立场。硬编码禁令是 RBA：无论操作员或用户指令如何都不允许。

Everything else is reason-based within a four-tier hierarchy: safety and supporting human oversight first; ethics second; Anthropic-declared guidelines third; helpfulness last. Operators can adjust defaults within the soft-coded zone but cannot touch the hardcoded prohibitions.

> 其他一切在四层层次内基于推理：安全和支持人类监督优先；伦理其次；Anthropic 声明的指南第三；有用性最后。操作员可在软编码区内调整默认但不能触及硬编码禁令。

## The Concept | 核心概念

### The four-tier priority hierarchy | 四层优先级层次

1. **Safety and supporting human oversight.** Highest. The model prioritises not undermining the ability of humans and Anthropic to supervise and correct AI. This is not "be cautious"; it is specifically "do not act in ways that make human oversight harder."
   中文翻译：**安全和支持人类监督。** 最高。模型优先不破坏人类和 Anthropic 监督和纠正 AI 的能力。不是"谨慎"；具体是"不以使人类监督更难的方式行动"。
2. **Ethics.** Honesty, avoiding harm to persons, not deceiving, not manipulating. Supersedes Anthropic's guidelines when they conflict.
   中文翻译：**伦理。** 诚实、避免对人伤害、不欺骗、不操纵。冲突时取代 Anthropic 指南。
3. **Anthropic guidelines.** Operational norms Anthropic has decided matter: product scope, interaction patterns, what tools to use when.
   中文翻译：**Anthropic 指南。** Anthropic 决定重要的运营规范：产品范围、交互模式、何时用何工具。
4. **Helpfulness.** Lowest. Be as useful as possible within the higher priorities.
   中文翻译：**有用性。** 最低。在更高优先级内尽可能有用。

When tiers conflict, higher wins. This is the same shape as Unix priorities or network QoS — the framing is meant to produce predictable resolution, not necessarily best-case behaviour on any single axis.

> 层冲突时高者赢。这与 Unix 优先级或网络 QoS 相同形状——框架旨在产生可预测解析，而非任一轴上的最佳行为。

### Hardcoded prohibitions vs soft-coded defaults | 硬编码禁令 vs 软编码默认

**Hardcoded:**

> **硬编码：**

- Bioweapons / CBRN uplift
  中文翻译：生物武器 / CBRN 提升
- CSAM
  中文翻译：CSAM（儿童性虐待材料）
- Attacks on critical infrastructure
  中文翻译：对关键基础设施的攻击
- Deception of users about the model's identity when asked directly
  中文翻译：被直接询问时对模型身份欺骗用户

The operator cannot override these. The user cannot override these. They are enforced at the model-weights level where possible (RLHF / Constitutional AI training) and at the inference layer where not.

> 操作员不能覆盖这些。用户不能覆盖这些。它们在可能处在模型权重层（RLHF / Constitutional AI 训练）和不可能处在推理层强制。

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Response length defaults
  中文翻译：响应长度默认
- Topical scope (the model can refuse topics outside the operator's deployment)
  中文翻译：主题范围（模型可拒绝操作员部署外的主题）
- Style (formal vs casual)
  中文翻译：风格（正式 vs 随意）
- Tool-use patterns
  中文翻译：工具使用模式

Operator adjustments happen inside a declared bound. The operator cannot remove the hardcoded prohibitions by renaming them.

> 操作员调整发生在声明边界内。操作员不能通过重命名移除硬编码禁令。

### The 2022 CAI training | 2022 CAI 训练

The original Constitutional AI (Bai et al., 2022) trained harmlessness:

> 原始 Constitutional AI（Bai 等人，2022）训练无害性：

1. Generate responses to a set of prompts.
   中文翻译：对一组提示生成响应。
2. Ask the model to critique each response against a constitution (explicit principles).
   中文翻译：要求模型对照宪法（显式原则）批评每个响应。
3. Revise the response based on the critique.
   中文翻译：基于批评修订响应。
4. RLAIF (reinforcement learning from AI feedback) on the revised pairs.
   中文翻译：在修订对上 RLAIF（来自 AI 反馈的强化学习）。

Result: a model that refuses harmful requests with principled explanations, not blanket refusals. The 2026 Constitution uses a descendant of this training plus additional post-training on the explicit tier hierarchy.

> 结果：以原则性解释而非一概拒绝来拒绝有害请求的模型。2026 宪法使用此训练的后代加额外对显式层层次的训练后。

### What reason-based alignment catches and misses | 基于推理对齐捕获和遗漏什么

**Catches:**

> **捕获：**

- Unanticipated combinations of allowed primitives where the principle applies clearly.
  中文翻译：原则清晰适用的允许原语的未预期组合。
- Novel requests that are close analogs of prohibited ones.
  中文翻译：禁止请求的近似类似物的新请求。
- Social-engineering attacks that rely on "you didn't say X was disallowed."
  中文翻译：依赖"你没说 X 被禁止"的社会工程攻击。

**Misses:**

> **遗漏：**

- Attacks that exploit principle ambiguity ("the user asked for this so helpfulness says yes").
  中文翻译：利用原则模糊的攻击（"用户要这个所以有用性说可以"）。
- Scenarios where two principles conflict in an unanticipated way, and the tier order is ambiguous.
  中文翻译：两个原则以未预期方式冲突且层次顺序模糊的场景。
- Slow drift in principle interpretation over training cycles (reinterpretation).
  中文翻译：跨训练周期的原则解释缓慢漂移（重新解释）。

### The 2023 participatory experiment | 2023 参与式实验

Anthropic ran a 2023 experiment comparing a corporate-authored constitution to one generated via public input (~1,000 US respondents). The two versions agreed on ~50% of principles. Where they diverged, the public-sourced version was more restrictive on some issues (political-content handling) and less restrictive on others (self-disclosure of AI identity). The 2026 Constitution did not incorporate the public-sourced findings. This is a documented tension in the approach.

> Anthropic 2023 年运行实验比较企业编写宪法与公众输入生成的宪法（约 1,000 美国受访者）。两版约 50% 原则一致。分歧处，公众版在某些问题上更严（政治内容处理）在其他上更宽（AI 身份自我披露）。2026 宪法未纳入公众版发现。这是方法中的已记录张力。

### Why hardcoded prohibitions are necessary | 为什么硬编码禁令必要

Reason-based alignment alone cannot close the tail. An attacker who can get the model to accept a premise (e.g., "we are a licensed bioweapons research lab") can often talk past principles that depend on case reasoning. Hardcoded prohibitions do not bend to premise framing. They are the Lesson 14 "hard constitutional limit" at the alignment layer.

> 仅基于推理对齐不能闭合尾部。能让模型接受前提（例如"我们是持牌生物武器研究实验室"）的攻击者常可绕过依赖案例推理的原则。硬编码禁令不向前提框架弯折。它们是第 14 课对齐层的"硬宪法限制"。

### Where the Constitution sits in the stack | 宪法在栈中的位置

The Constitution is not Lesson 14's kill switch. It lives at the model layer.

> 宪法不是第 14 课的终止开关。它存在于模型层。

It lives at the model layer: what the model's weights are trained to prefer. Kill switches and canary tokens live at the runtime layer: what the runtime permits. Both are required. A runtime that fires all the wrong actions because the model weights are permissive is a runtime problem. A model that refuses all the right actions because the runtime is over-restrictive is a runtime problem. Layers cover different classes.

> 它存在于模型层：模型权重被训练偏好什么。终止开关和金丝雀 token 在运行时层：运行时允许什么。两者都需要。因模型权重宽松而触发所有错误动作的运行时是运行时问题。因运行时过度限制而拒绝所有正确动作的模型是运行时问题。层覆盖不同类别。

## Use It | 用框架实现

`code/main.py` implements a minimal four-tier priority resolver. The resolver takes a proposed action and a set of principle-evaluations (safety, ethics, guidelines, helpfulness) and returns the action, a refusal, or a modified action. The driver runs a small case set: clear allow, clear disallow, hardcoded prohibition, ambiguous case across tiers.

> `code/main.py` 实现最小四层优先级解析器。解析器取提议动作和一组原则评估（安全、伦理、指南、有用性）并返回动作、拒绝或修改动作。驱动器运行小案例集：清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例。

## Ship It | 产出物

`outputs/skill-constitution-review.md` audits a deployment's constitutional layer: what is hardcoded, what is soft-coded, where the operator can adjust, and whether the four-tier hierarchy is actually the resolution order.

> `outputs/skill-constitution-review.md` 审计部署的宪法层：什么硬编码、什么软编码、操作员在哪可调、四层层次是否真是解析顺序。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the hardcoded prohibition fires even when helpfulness is high. Modify the resolver to weight helpfulness above ethics; observe the failure mode.
   中文翻译：运行 `code/main.py`。确认有用性高时硬编码禁令仍触发。修改解析器将有用性置于伦理之上；观察失败模式。

2. Read the Claude Constitution (public, 79 pages, CC0). Identify one principle you believe is under-specified. Write two paragraphs explaining the specific ambiguity and proposing a tighter formulation.
   中文翻译：阅读 Claude Constitution（公开，79 页，CC0）。识别你认为欠规范的一个原则。写两段解释具体模糊并提议更紧的表述。

3. Design a soft-coded default set for a customer-support agent. What does the operator adjust? What can the operator not touch? Justify each boundary.
   中文翻译：为客服 Agent 设计软编码默认集。操作员调什么？操作员不能触什么？论证每个边界。

4. Read the Bai et al. 2022 CAI paper. Describe one case where Constitutional AI's critique-and-revise loop would produce a worse outcome than a blanket rule. Identify the class.
   中文翻译：阅读 Bai 等人 2022 CAI 论文。描述 Constitutional AI 批评-修订循环产生比一概规则更差结果的一个案例。识别类别。

5. Anthropic's 2023 participatory experiment found ~50% divergence between public and corporate principles. Pick one category where this matters for production deployment (e.g., political neutrality). Propose a design that lets operators express their own values while the hardcoded prohibitions remain untouched.
   中文翻译：Anthropic 2023 参与式实验发现公众和企业原则约 50% 分歧。选一个对生产部署重要的类别（例如政治中立）。提议让操作员表达自己价值观同时硬编码禁令不变的设计。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Further Reading | 延伸阅读

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — the 79-page CC0 document.
  中文翻译：79 页 CC0 文档。
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) — 2022 original.
  中文翻译：2022 原始版本。
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) — participatory experiment.
  中文翻译：参与式实验。
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — where the Constitution sits in the RSP stack.
  中文翻译：宪法在 RSP 栈中的位置。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — Constitution's role in long-horizon deployments.
  中文翻译：宪法在长程部署中的角色。
