# CAIS, CAISI, and Societal-Scale Risk | 社会 CAIS 风险

> The Center for AI Safety (CAIS, San Francisco, founded 2022 by Hendrycks and Zhang) publishes the four-risk framework — malicious use, AI races, organizational risks, rogue AIs — and the May 2023 statement on extinction risk signed by hundreds of professors and company leaders. 2026 releases from CAIS: AI Dashboard for frontier-model evaluation, Remote Labor Index (with Scale AI), Superintelligence Strategy Paper, AI Frontiers newsletter. A distinct entity: NIST Center for AI Standards and Innovation (CAISI) — US-government-facing voluntary agreements and unclassified capability evaluations focused on cyber, bio, and chemical-weapons risks. CAIS flags organizational risk as one of four top-level risks: safety culture, rigorous audits, multi-layered defenses, and information security are foundational but routinely traded off against deployment speed. California SB-53, if signed, would be the first US state-level catastrophic-risk regulation.

> **【中文解读】** 本节介绍了 CAIS/CAISI 的社会风险评估——AI 系统对社会的潜在影响和风险分析。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Lessons 19 and 20 covered lab-internal scaling policies. Lesson 21 covered independent capability evaluation. This lesson covers the third perspective: civil society and government organizations who shape public discussion and regulatory baseline for catastrophic AI risk.

> 第 19 和 20 课涵盖了实验室内部扩展政策。第 21 课涵盖了独立能力评估。本课涵盖第三个视角：塑造公共讨论和灾难性 AI 风险监管基线的民间社会和政府组织。

Two distinct entities matter. CAIS is a non-profit research org that publishes frameworks for thinking about AI risk and coordinates public statements. CAISI is a US-government center within NIST that runs voluntary agreements with labs and unclassified capability evaluations. The names rhyme; the missions do not overlap. A practitioner should know both.

> 两个不同实体很重要。CAIS 是发布 AI 风险思考框架并协调公开声明的非营利研究组织。CAISI 是 NIST 内的美国政府中心，与实验室运行自愿协议和非密能力评估。名字押韵；任务不重叠。从业者应两者都知。

The practical content: CAIS's four-risk framework is the most widely cited societal-scale-risk taxonomy in the literature. Safety culture and organizational risk are one of those four, and this is the one most directly under a practitioner's control. SB-53 (California) would be the first US state-level catastrophic-risk regulation if signed; the bill's framing matters because state-level regulation has historically led federal action in US tech policy.

> 实用内容：CAIS 的四风险框架是文献中最广泛引用的社会规模风险分类法。安全文化和组织风险是其中之一，是最直接在从业者控制下的一项。SB-53（加州）若签署将是第一个美国州级灾难性风险监管；该法案框架重要，因为州级监管在美国科技政策中历史上领先联邦行动。

## The Concept | 核心概念

### CAIS — Center for AI Safety

- Founded: 2022 in San Francisco, by Dan Hendrycks and colleagues (the "Zhang" name refers to an early collaborator, not a current co-founder; see CAIS website for current leadership).
  中文翻译：成立：2022 年在旧金山，由 Dan Hendrycks 和同事创立（"Zhang"指早期合作者，非当前联合创始人；当前领导见 CAIS 网站）。
- Status: 501(c)(3) non-profit.
  中文翻译：状态：501(c)(3) 非营利。
- Notable 2023 output: statement on extinction risk, co-signed by hundreds of researchers and CEOs. Stated: "Mitigating the risk of extinction from AI should be a global priority alongside other societal-scale risks such as pandemics and nuclear war."
  中文翻译：2023 显著产出：灭绝风险声明，数百名研究员和 CEO 联合签署。声明："减轻 AI 灭绝风险应与流行病和核战争等其他社会规模风险并列作为全球优先。"
- 2026 outputs: AI Dashboard for frontier-model evaluation, Remote Labor Index (joint with Scale AI), Superintelligence Strategy Paper, AI Frontiers newsletter.
  中文翻译：2026 产出：前沿模型评估 AI Dashboard、Remote Labor Index（与 Scale AI 联合）、Superintelligence Strategy Paper、AI Frontiers 简报。

### The four-risk framework

CAIS's framework groups catastrophic AI risk into four top-level categories:

> CAIS 的框架将灾难性 AI 风险分为四个顶级类别：

1. **Malicious use**: a bad actor uses AI to cause harm (bioweapons synthesis, disinformation, cyberattacks).
   中文翻译：**恶意使用**：坏人使用 AI 造成伤害（生物武器合成、虚假信息、网络攻击）。
2. **AI races**: competitive pressure between labs, companies, or nations pushes deployment past the point where it is safe.
   中文翻译：**AI 竞赛**：实验室、公司或国家间的竞争压力推动部署越过安全点。
3. **Organizational risks**: internal lab dynamics (safety-culture failures, insufficient audit, under-resourced security) produce a bad deployment.
   中文翻译：**组织风险**：内部实验室动态（安全文化失败、审计不足、安全资源不足）产生糟糕部署。
4. **Rogue AIs**: a sufficiently capable AI pursues goals that conflict with human welfare.
   中文翻译：**失控 AI**：足够能力的 AI 追求与人类福祉冲突的目标。

This is not the only taxonomy; it is the most cited. The categories are not mutually exclusive — a rogue AI produced by an organization that traded audit for speed in a race is all four.

> 这不是唯一分类法；它是最常被引用的。类别不互斥——一个由竞赛中用审计换速度的组织产生的失控 AI 是全部四类。

### Where organizational risk lives

Of the four categories, organizational risk is the most actionable for practitioners. A lab's safety culture, audit rigor, defense layering, and information security decide whether their model ships with the controls of Lessons 10–18 actually in place, or whether those controls are checklist items nobody verified.

> 在四个类别中，组织风险对从业者来说最具可操作性。实验室的安全文化、审计严格性、防御分层和信息安全决定他们的模型是带着第 10–18 课的控件实际就位发布，还是这些控件是无人验证的清单项。

The concrete organizational-risk levers:

> 具体组织风险杠杆：

- **Safety culture**: do team members feel able to escalate a concern without career cost? CAIS surveys find this is a strong predictor of the other levers.
  中文翻译：**安全文化**：团队成员能否在不付出职业代价的情况下升级担忧？CAIS 调查发现这是其他杠杆的强预测因子。
- **Rigorous audits**: external and internal. Internal-only audits produce optimistic reports.
  中文翻译：**严格审计**：外部和内部。仅内部审计产生乐观报告。
- **Multi-layered defenses**: no single layer is sufficient (the running theme of Phase 15).
  中文翻译：**多层防御**：无单层足够（Phase 15 贯穿主题）。
- **Information security**: model weights leaking, eval data leaking, monitor-bypass techniques leaking. RAND SL-4 in Lesson 19 is a specific standard.
  中文翻译：**信息安全**：模型权重泄漏、评估数据泄漏、监控规避技术泄漏。第 19 课的 RAND SL-4 是特定标准。

### CAISI — Center for AI Standards and Innovation

- Operates within NIST.
  中文翻译：在 NIST 内运营。
- Runs voluntary agreements with frontier labs.
  中文翻译：与前沿实验室运行自愿协议。
- Publishes unclassified capability evaluations focused on cyber, bio, and chemical-weapons risks.
  中文翻译：发布聚焦网络、生物和化学武器风险的非密能力评估。
- Distinct from CAIS; the acronyms collide; check the URL (nist.gov) to confirm which one you are reading.
  中文翻译：与 CAIS 不同；首字母缩写冲突；检查 URL（nist.gov）确认你在读哪个。

CAISI's role is the public, government-facing counterpart to METR's private lab engagements (Lesson 21). CAISI reports are unclassified; METR reports are often NDA-gated. A practitioner reading both gets a fuller picture.

> CAISI 的角色是 METR 私人实验室合作（第 21 课）的公共、面向政府对应物。CAISI 报告非密；METR 报告通常 NDA 门控。读两者的从业者得到更完整图景。

### California SB-53

The California Senate bill (2025–2026 session) addresses catastrophic risk from frontier models. Key provisions as drafted:

> 加州参议院法案（2025–2026 会期）处理前沿模型的灾难性风险。起草的关键条款：

- Specific capability thresholds that trigger state-level obligations.
  中文翻译：触发州级义务的特定能力阈值。
- Whistleblower protections for AI lab employees.
  中文翻译：AI 实验室员工举报人保护。
- Incident reporting requirements for catastrophic failures.
  中文翻译：灾难性失败的事故报告要求。

If signed, it would be the first US state-level catastrophic-risk regulation. Regardless of signing status, the bill's framing shapes how other state legislatures approach the problem. Practitioners in California should track the bill's status; practitioners elsewhere should read it to understand what US state-level regulation will likely look like.

> 若签署，它将是第一个美国州级灾难性风险监管。无论签署状态，该法案的框架塑造其他州立法机构如何处理问题。加州的从业者应跟踪法案状态；其他地方的从业者应阅读以理解美国州级监管可能的样子。

### Societal-scale risk is not a single-layer problem

The running theme of Phase 15 — defense in depth — applies at the societal layer too. No single organization, regulation, or framework closes catastrophic risk. The ecosystem functions only when:

> 第 15 阶段的贯穿主题——深度防御——也适用于社会层。没有单一的组织、法规或框架能关闭灾难性风险。生态系统仅在以下情况运转：

- Labs ship scaling policies (Lessons 19, 20).
  中文翻译：实验室发布扩展政策（第 19、20 课）。
- External evaluators produce measurements (Lesson 21).
  中文翻译：外部评估者产出测量（第 21 课）。
- Civil society tracks and publicizes (CAIS).
  中文翻译：民间社会跟踪和宣传（CAIS）。
- Government runs voluntary programs and baseline regulation (CAISI, SB-53).
  中文翻译：政府运行自愿计划和基线监管（CAISI、SB-53）。
- Practitioners build multi-layered controls (Lessons 10–18).
  中文翻译：从业者构建多层控件（第 10–18 课）。

This is the final synthesis for the phase: every previous lesson is one layer in a stack whose completeness matters more than any single layer's strength.

> 这是阶段的最终综合：之前的每节课是堆栈中的一层，其完整性比任何单层的强度更重要。

## Use It | 用框架实现

`code/main.py` implements a small risk-inventory tool. Given a proposed deployment, it tags the deployment against the four-risk categories and returns a mitigation checklist. It's a reading aid for the framework, not a substitute for human judgment.

> `code/main.py` 实现小型风险盘点工具。给定提议的部署，它对四风险类别标记部署并返回缓解清单。这是框架的阅读辅助，非人类判断的替代。

## Ship It | 产出物

`outputs/skill-societal-risk-review.md` reviews a deployment for societal-scale-risk posture: which of the four categories it touches, what mitigations are in place, what the organizational-risk exposure is.

> `outputs/skill-societal-risk-review.md` 审查部署的社会规模风险姿态：触及四个类别中的哪些、已有哪些缓解、组织风险暴露是什么。

## Exercises | 练习题

1. Run `code/main.py`. Feed in three synthetic deployments at different scales. Confirm the four-risk tags match what you would expect; identify one case where the tool under- or over-tags.
   中文翻译：运行 `code/main.py`。输入三个不同规模的合成部署。确认四风险标记符合预期；识别工具欠标记或过标记的一个案例。

2. Read the CAIS four-risk paper in full. Pick one risk category and write two paragraphs on what you believe is the most important 2026 development in that category.
   中文翻译：完整阅读 CAIS 四风险论文。选一个风险类别，写两段关于你认为该类别 2026 最重要发展。

3. Read a current draft of California SB-53. Identify one provision you believe strengthens the catastrophic-risk posture and one you believe weakens it. Justify both.
   中文翻译：阅读加州 SB-53 当前草案。识别你认为强化灾难性风险姿态的一个条款和弱化的一个。论证两者。

4. Pick a production AI deployment you know (yours or a published one). Score it against the organizational-risk sub-levers: safety culture, audit rigor, multi-layered defenses, information security. Which is weakest? What would it cost to bring it to par?
   中文翻译：选一个你知道的生产 AI 部署（你的或公开的）。对组织风险子杠杆打分：安全文化、审计严格性、多层防御、信息安全。哪个最弱？达到标准需多少成本？

5. Sketch a 2028 version of the four-risk framework that reflects one year of additional capability and one year of additional deployment experience. What would you add, remove, or regroup?
   中文翻译：勾勒反映一年额外能力和一年额外部署经验的四风险框架 2028 版本。你会添加、移除或重组什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| CAIS | "Center for AI Safety" | Non-profit; four-risk framework; 2023 extinction statement | CAIS：非营利，四风险框架 |
| CAISI | "US government AI safety" | NIST Center; voluntary agreements; unclassified evals | CAISI：NIST 中心，自愿协议 |
| Four-risk framework | "CAIS's taxonomy" | malicious use, AI races, organizational risks, rogue AIs | 四风险框架：恶意使用/AI 竞赛/组织风险/失控 AI |
| Malicious use | "Bad actor uses AI" | Bioweapons, disinformation, cyberattacks | 恶意使用：生物武器、虚假信息、网络攻击 |
| AI races | "Competitive pressure" | Labs/companies/nations push deployment past safety | AI 竞赛：竞争压力推动部署越过安全 |
| Organizational risk | "Lab internal failure" | Safety culture, audit, defenses, infosec | 组织风险：安全文化、审计、防御、信息安全 |
| Rogue AI | "Misaligned agent" | Capable AI pursuing goals conflicting with human welfare | 失控 AI：追求冲突目标的强大 AI |
| California SB-53 | "State-level regulation" | 2025–2026 bill; first US state catastrophic-risk regulation if signed | 加州 SB-53：州级灾难性风险监管法案 |

## Further Reading | 延伸阅读

- [Center for AI Safety](https://safe.ai/) — institutional home of the four-risk framework.
  中文翻译：四风险框架的机构之家
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) — the four-risk paper.
  中文翻译：四风险论文
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) — short joint statement.
  中文翻译：简短联合声明
- [NIST CAISI](https://www.nist.gov/caisi) — government-facing AI standards and innovation center.
  中文翻译：面向政府的 AI 标准和创新中心
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — connects lab-level commitments to societal-scale framing.
  中文翻译：连接实验室级承诺与社会规模框架
