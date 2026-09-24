# Ship a Week of Work, Not a Perfect Prompt | 交付一周的工作量，而非一个完美的提示词

> Your capstone is a governed decision workflow: sources in, claims checked, human authority preserved, and state handed off.

> **【中文解读】** 本课是 Associate（助理级）认证路线的毕业设计，标题就是方法论：要交付的是一周的"受治理决策工作流"，而不是一个精雕细琢的提示词。四个关键词定义了工作流的骨架：来源进（受治理的证据源）、论断被核查（引用必须真正支撑论断）、人的权限被保留（发布与重大决策归授权的人）、状态被交接（评审者拿到完整决策包而不是重新摸索）。全课按模拟工作周展开：周一界定决策与产品面、周二冻结并治理证据、周三分四段分解工作、周四验证与挑战、周五交接并闭环，每天以一道门收尾——门不过，就不把不确定性推给下游。

> **【拓展：五天门→第 01-07 课的综合运用】** 本课把前半程的六门课拧成一条流水线：第 01 课（选择能承载工作的最小接口面）用于周一的产品面决策，第 03 课（把请求变成可测试的契约）与第 04 课（把每类事实放进正确类型的上下文）用于周二的来源治理与周三的分段提示词契约，第 05 课（验证的是论断，不是自信）用于周四的论断-证据矩阵，第 06 课（把权限围绕能力来设计）与第 07 课（先设计交接，再设计自动化）用于治理检查与周五的人工交接。它也是助理级路线唯一被"另一个人评审"的提交物，为开发者方向毕业设计 30 铺路。

> 🔗 **【前置】** 学本课前请先掌握第 01、03、04、05、06、07 课——它们分别提供接口面选择、提示词契约、上下文分层、输出验证、权限设计、人机交接六大块，本课的每一天都是其中一块的实战复用。

**Type:** Build | **类型:** 动手构建
**Languages:** Python | **语言:** Python
**Prerequisites:** [Choose the Smallest Surface That Can Carry the Work](../../01-claude-product-and-model-landscape/), [Turn a Request Into a Testable Contract](../../03-prompting-and-task-decomposition/), [Put Each Fact in the Right Kind of Context](../../04-context-knowledge-memory-and-caching/), [Validate the Claim, Not the Confidence](../../05-output-evaluation-and-validation/), [Put Authority Around Capability](../../06-governance-safety-and-responsible-use/), [Design the Handoff Before the Automation](../../07-workflow-design-and-human-handoffs/) | **前置知识:** 第 01 课（选择能承载工作的最小接口面）、第 03 课（把请求变成可测试的契约）、第 04 课（把每类事实放进正确类型的上下文）、第 05 课（验证的是论断，不是自信）、第 06 课（把权限围绕能力来设计）、第 07 课（先设计交接，再设计自动化）
**Time:** ~4 hours across one simulated workweek | **时间:** 约 4 小时，在一个模拟工作周内完成

## Learning Objectives | 学习目标

- Combine product selection, prompting, knowledge management, validation, governance, troubleshooting, and handoff design.
  中文翻译：综合运用产品选择、提示词、知识管理、验证、治理、故障排查与交接设计。
- Build a source-backed weekly briefing workflow with explicit checkpoints.
  中文翻译：构建一个有明确检查点、以来源支撑的每周简报工作流。
- Implement a deterministic Python validator for sources, claims, governance, and handoff readiness.
  中文翻译：实现一个针对来源、论断、治理与交接就绪度的确定性 Python 验证器。
- Run normal and failure cases before recommending release.
  中文翻译：在建议发布之前先跑正常用例与失败用例。
- Produce evidence of readiness instead of claiming that a workflow is safe.
  中文翻译：产出就绪度的证据，而不是宣称工作流是安全的。

## The Problem | 问题引入

> **【中文解读】** 场景设定：你是 Northstar Field Services（虚构公司，七个区域团队）的运营负责人，每周五领导层要一份覆盖服务延误、客户影响事件、策略例外的简报，外加下周的两个决策。现状很脆：各区域格式不一、分析师手工抄录对账、三个人审批，简报偶尔漏区域或带旧数字。"用 Claude 自动化周报"这个要求本身不是方案——简报影响人员调度与客户沟通，部分输入含客户明细，策略例外需要授权负责人，一份没有证据的自信草稿反而会加速错误决策。任务因此被界定为：Claude 只做提取、比对、起草；确定性检查验证精确性质；授权的人拥有发布与重大决策。

You are the operations lead at Northstar Field Services, a fictional company with seven regional teams. Every Friday, the leadership group needs a brief covering service delays, customer-impacting incidents, policy exceptions, and two decisions for the next week.

> 你是 Northstar Field Services（一家有七个区域团队的虚构公司）的运营负责人。每周五，领导层需要一份简报，覆盖服务延误、影响客户的事件、策略例外，以及下周的两个决策。

The current process is fragile. Regional leads send updates in different formats. An analyst copies facts into a document, reconciles conflicting dates, and asks three people for approval. The final brief sometimes misses a region or carries a corrected number from an old message.

> 现有流程很脆弱。区域负责人提交的格式各不相同。一名分析师把事实抄进文档、核对冲突的日期，再找三个人审批。最终简报有时漏掉一个区域，有时带着旧消息里已被更正的数字。

Leadership asks you to "automate the weekly report with Claude." That request is not a solution. The brief affects staffing and customer communications. Some inputs contain customer details. Policy exceptions need an authorized owner. A confident draft without evidence could accelerate the wrong decision.

> 领导层要求你"用 Claude 把周报自动化"。这个要求本身不是方案。简报影响人员调度和客户沟通。部分输入包含客户明细。策略例外需要授权负责人。一份没有证据的自信草稿可能加速错误的决策。

Your job is to design a bounded Claude-assisted workflow. Claude may extract, compare, and draft. Deterministic checks verify exact properties. An authorized person owns publication and consequential decisions.

> 你的任务是设计一个有边界的 Claude 辅助工作流。Claude 可以提取、比对和起草。确定性检查验证精确性质。一个被授权的人拥有发布与重大决策。

## The Concept | 核心概念

### The deliverable is a chain of proof | 交付物是一条证据链

> **【中文解读】** 毕业设计要交付五件相互衔接的产物：用例与产品选择记录、受维护的来源注册表加固定周快照、分阶段提示词契约、论断-证据与治理验证结果、带回退方案的人工交接包。Mermaid 图给出模拟周节奏：周一界定与选择、周二治理来源、周三提取与起草、周四验证与挑战、周五交接与评审，失败时回流"新增评测用例"。铁律是"每天以一道门收尾"——门不过，就不要把不确定性推给下游。

You will produce five connected artifacts:

> 你将产出五件相互衔接的产物：

1. A use-case and product-selection record.
   中文翻译：用例与产品选择记录。
2. A maintained source registry and fixed weekly snapshot.
   中文翻译：受维护的来源注册表与固定的每周快照。
3. A staged prompt contract.
   中文翻译：分阶段的提示词契约。
4. A claim-evidence and governance validation result.
   中文翻译：论断-证据与治理验证结果。
5. A human handoff packet with fallback.
   中文翻译：带回退方案的人工交接包。

```mermaid
flowchart LR
    A["Monday: scope and select"] --> B["Tuesday: govern sources"]
    B --> C["Wednesday: extract and draft"]
    C --> D["Thursday: validate and challenge"]
    D --> E["Friday: hand off and review"]
    E -->|"new failure"| F["Add evaluation case"]
    F --> A
```

Each day ends at a gate. If the gate fails, do not push uncertainty downstream.

> 每一天以一道门收尾。门不过，就不要把不确定性推给下游。

### The Python validator is intentionally limited | Python 验证器刻意保持有限

> **【中文解读】** 本课的代码刻意不调用 Claude，它演示的是一条关键的架构边界：精确的工作流性质属于确定性代码。验证器检查：必填章节是否齐全；每个活跃来源是否有负责人、权威级别、日期、敏感度与稳定 ID；论断是否引用已知来源；重大论断是否有直接或计算得出的支撑；过期与冲突证据是否可见；所选产品面是否被该数据级别批准；高后果或不可逆工作是否有授权的人工负责人；交接是否写明决策、期限、回退与下一负责人。它判不了策略在伦理上是否充分、评审者是否称职、来源陈述是否为真——这些仍是组织与人的责任。

The capstone code does not call Claude. It demonstrates a crucial architecture boundary: exact workflow properties belong in deterministic code.

> 毕业设计代码不调用 Claude。它演示一条关键的架构边界：精确的工作流性质属于确定性代码。

The validator checks whether:

> 验证器检查：

- Required packet sections exist.
  中文翻译：必填的包章节存在。
- Every active source has an owner, authority, date, sensitivity, and stable ID.
  中文翻译：每个活跃来源都有负责人、权威级别、日期、敏感度和稳定 ID。
- Claims reference known sources.
  中文翻译：论断引用的是已知来源。
- Consequential claims use direct or calculated support.
  中文翻译：重大论断使用直接或计算得出的支撑。
- Stale and conflicting evidence is visible.
  中文翻译：过期与冲突的证据是可见的。
- The chosen surface is approved for the data class.
  中文翻译：所选产品面被批准用于该数据级别。
- High-consequence or irreversible work has an authorized human owner.
  中文翻译：高后果或不可逆的工作有授权的人工负责人。
- The handoff names a decision, deadline, fallback, and next owner.
  中文翻译：交接写明了决策、期限、回退方案与下一负责人。

It cannot decide whether a policy is ethically sufficient, whether the human reviewer is competent, or whether a source statement is true. Those remain organizational and human responsibilities.

> 它无法判定一项策略在伦理上是否充分、人工评审者是否称职、来源陈述是否为真。这些仍是组织与人的责任。

## Build It | 动手构建

## Interactive Lab | 交互实验室

```figure
29-associate-capstone-readiness
```

Use the readiness board throughout the five-day build. It connects purpose,
sources, prompt stages, claim support, authority, handoff, and fallback so a
polished brief cannot hide a failed gate.

> 在五天构建过程中全程使用就绪看板。它把目的、来源、提示词阶段、论断支撑、权限、交接与回退连接起来，让一份打磨光鲜的简报藏不住任何一道没过的门。

## Practice Lab | 练习实验室

Complete the five-day workflow below, then deliberately break the surface,
source, claim-support, authority, and handoff gates one at a time.

> 完成下面的五天工作流，然后逐个故意打破产品面、来源、论断支撑、权限与交接这五道门。

## Shipped Artifact | 交付产物

The shipped checklist and filled
[`outputs/demo-readiness-report.json`](../outputs/demo-readiness-report.json)
are the practical outputs.

> 随课附带的清单和填写好的演示就绪报告是实际产物。

## Verify It | 验证

Reproduce the passing packet and all failure-first tests with the commands below;
no network access or credentials are required. The lesson quiz is the final
individual check.

> 用下面的命令复现通过的数据包和全部"失败优先"测试；不需要网络访问或凭据。课程测验是最后的个人检查。

## Capstone Connection | 毕业设计衔接

The completed packet is the Associate route capstone evidence reviewed by
another person.

> 完成的数据包是助理级路线毕业设计的证据，由另一个人评审。

### Monday: scope the decision and product surface | 周一：界定决策与产品面

Write one sentence for the decision:

> 为决策写一句话：

```text
By Friday at 15:00, the operations director will choose no more than two
staffing or process changes for the following week using the approved regional snapshot.
```

Define what is out of scope:

> 界定范围之外的事：

- No automatic customer messages.
  中文翻译：不做自动客户消息。
- No employee performance ranking.
  中文翻译：不做员工绩效排名。
- No changes to staffing schedules.
  中文翻译：不改动人员排班。
- No legal or regulatory conclusion.
  中文翻译：不下法律或监管结论。
- No use of restricted data.
  中文翻译：不使用受限数据。

Compare candidate surfaces. A one-off chat is easy, but weak for maintained instructions and a recurring source set. A Project may fit collaborative, repeated work if its current terms, plan controls, and data handling are approved. The API may fit when programmatic ingestion, validation, and audit integration are required. Research is useful for current external facts, not for replacing internal approved policy.

> 对比候选产品面。一次性聊天很容易，但对需要维护的指令和固定的来源集合来说太弱。若当前的条款、方案控制与数据处理获得批准，Project 可能适合协作式、重复性的工作。当需要程序化摄取、验证与审计集成时，API 可能更合适。Research 适合查当前的外部事实，不适合替代内部已批准的策略。

Record the decision, not just the product name:

> 记录决策本身，而不只是产品名：

```text
Surface:
Why it fits:
Data class allowed:
Current terms checked on:
Unsupported requirements:
Fallback surface or manual path:
```

Gate: the owner approves the purpose, surface, data class, and prohibited actions.

> 门：负责人批准目的、产品面、数据级别与禁止动作。

### Tuesday: freeze and govern the evidence | 周二：冻结并治理证据

Create a source registry for:

> 为以下各项创建来源注册表：

- Seven regional status files.
  中文翻译：七个区域状态文件。
- The incident system export.
  中文翻译：事件系统导出。
- The approved service policy.
  中文翻译：已批准的服务策略。
- The staffing-capacity table.
  中文翻译：人员产能表。
- The prior week's decision record.
  中文翻译：上一周的决策记录。

Every source needs a stable ID, owner, authority class, effective date, review date, and sensitivity. Mark discussion notes as reference, not policy. Remove customer names if the decision does not require them.

> 每个来源都需要稳定 ID、负责人、权威级别、生效日期、复审日期与敏感度。把讨论笔记标记为参考资料而非策略。如果决策不需要客户姓名，就去掉。

Freeze the weekly source snapshot at a documented time. A fact that changes afterward belongs in a revision or exception process. Otherwise the draft, reviewer, and leader may each see a different world.

> 在一个有记录的时间点冻结每周来源快照。之后变化的事实应进入修订或例外流程。否则草稿、评审者与领导看到的可能是三个不同的世界。

Define authority order:

> 定义权威顺序：

```text
1. Approved service policy and signed incident status
2. Current regional status submitted before the cutoff
3. Prior decision record
4. Discussion notes, for leads only and never as sole support
```

Gate: all seven regions are present or explicitly marked missing; sources pass freshness and permission checks; conflicts have an owner.

> 门：七个区域全部在场或被显式标记缺失；来源通过新鲜度与权限检查；冲突有负责人。

### Wednesday: decompose the work | 周三：分解工作

Do not ask for the final brief in one step. Use four bounded stages.

> 不要一步索要最终简报。使用四个有边界的阶段。

**Stage 1, extraction:** Return structured rows for region, delay, affected service, incident ID, policy exception, source ID, and uncertainty. Do not recommend action.

> **阶段 1，提取：**返回结构化行，包含区域、延误、受影响服务、事件 ID、策略例外、来源 ID 与不确定性。不要建议行动。

**Stage 2, reconciliation:** Check region coverage, totals, duplicate incidents, date conflicts, and unsupported fields. Stop if a blocker remains.

> **阶段 2，对账：**检查区域覆盖、合计数、重复事件、日期冲突与无支撑字段。仍有阻断项就停下。

**Stage 3, analysis:** Identify patterns and propose no more than three candidate actions. Each action needs supporting findings, policy constraints, likely benefit, downside, and an owner who could authorize it.

> **阶段 3，分析：**识别模式并提出不超过三个候选行动。每个行动都需要支撑发现、策略约束、可能收益、 downside，以及一个能授权它的负责人。

**Stage 4, drafting:** Produce the executive brief only from validated rows and approved analysis. Include decisions required, evidence, exceptions, and known uncertainty.

> **阶段 4，起草：**只基于已验证的行与已批准的分析产出高管简报。包含所需决策、证据、例外与已知的不确定性。

Use a prompt contract for every stage. Include source hierarchy, abstention behavior, output shape, and acceptance criteria. Save versions so a failed result can be reproduced.

> 每个阶段都使用提示词契约。包含来源层级、弃权行为、输出形状与验收标准。保存版本，让失败的结果可以复现。

Gate: structured extraction reconciles with the snapshot before analysis begins.

> 门：结构化提取先与快照对账，然后才开始分析。

### Thursday: validate and challenge | 周四：验证与挑战

> **【中文解读】** 周四的节奏是"先跑通、再故意打破"：先运行验证器让演示包返回 `ready_for_human_review`，再逐个制造失败（把 `approved_surface` 改为 false、删掉来源负责人、引用不存在的来源 ID、把重大论断标成推测、删掉决策负责人、把动作改成不可逆），看验证器是否都拦得住。随后为真实草稿建论断-证据矩阵：引用必须支撑确切的论断；合计数用代码或表格核对，不用模型评分器；把评分标准和证据交给独立评审者，要求它报告发现而不是默默改稿。发布分级也要背：阻断（未批准的数据/产品面、未知来源、合计数错误、无支撑的重大论断、缺决策权限）、修订（覆盖不完整、冲突未解决、来源过期、不确定性不清晰）、质量改进（重复、弱标题、非关键语气）。

Run the included validator:

> 运行附带的验证器：

```bash
cd certifications/claude/lessons/29-associate-workflow-capstone
python3 code/main.py
```

The demonstration packet should return a `ready_for_human_review` status. Now break it deliberately:

> 演示数据包应返回 `ready_for_human_review` 状态。现在故意打破它：

- Set `approved_surface` to false.
  中文翻译：把 `approved_surface` 设为 false。
- Remove a source owner.
  中文翻译：删掉一个来源负责人。
- Reference a source ID that does not exist.
  中文翻译：引用一个不存在的来源 ID。
- Mark a consequential claim as speculative.
  中文翻译：把一个重大论断标记为推测。
- Remove the decision owner.
  中文翻译：删掉决策负责人。
- Make the action irreversible.
  中文翻译：把动作改成不可逆。

Run the unit tests:

> 运行单元测试：

```bash
python3 -m unittest discover -s code/tests -v
```

Then create a claim-evidence matrix for the actual draft. A citation must support the exact claim. Verify totals with code or a spreadsheet, not a model grader. Give a separate reviewer the rubric and evidence. Ask it to report findings, not silently rewrite the draft.

> 然后为实际草稿建一个论断-证据矩阵。引用必须支撑确切的论断。用代码或电子表格核对合计数，而不是模型评分器。把评分标准和证据交给一位独立评审者。要求它报告发现，而不是默默重写草稿。

Use release levels:

> 使用发布分级：

- **Block:** unapproved data or surface, unknown source, invalid total, unsupported consequential claim, missing decision authority.
  中文翻译：**阻断：**未批准的数据或产品面、未知来源、合计数错误、无支撑的重大论断、缺失决策权限。
- **Revise:** incomplete coverage, unresolved conflict, stale source, unclear uncertainty.
  中文翻译：**修订：**覆盖不完整、冲突未解决、来源过期、不确定性不清晰。
- **Quality improvement:** repetition, weak heading, or noncritical tone issue.
  中文翻译：**质量改进：**重复、弱标题或非关键的语气问题。

Gate: every blocker is resolved. Remaining uncertainty is visible in the human packet.

> 门：所有阻断项都已解决。剩余的不确定性在人工数据包中可见。

### Friday: hand off and close the loop | 周五：交接并闭环

Complete [`outputs/checklist.md`](../outputs/checklist.md). Build the review packet:

> 填写清单。构建评审数据包：

```text
Decision: Choose up to two next-week interventions.
Owner: Operations director.
Deadline: Friday 15:00.
Snapshot: Weekly source registry version and cutoff.
Candidate: Brief version and prompt version.
Evidence: Claim IDs, source IDs, calculations.
Checks: Passed, failed, and manually reviewed.
Uncertainty: Missing region, conflicting date, or weak support.
Options: Approve, revise, reject, escalate.
Fallback: Publish the manual template or delay with notice.
```

The director approves the decision, not "the AI." Record who approved what, based on which snapshot. If the source changes after approval, invalidate the publication gate and review the delta.

> 批准决策的是总监，不是"AI"。记录谁基于哪个快照批准了什么。如果批准之后来源发生变化，让发布门失效并复审增量。

After the simulated release, run a short retrospective:

> 模拟发布之后，做一次简短的复盘：

- Which stage consumed the most human time?
  中文翻译：哪个阶段消耗的人工时间最多？
- Which check caught the most serious defect?
  中文翻译：哪项检查抓住了最严重的缺陷？
- Did any important judgment become harder?
  中文翻译：有没有哪个重要判断变得更难了？
- Which source needs better ownership?
  中文翻译：哪个来源需要更好的归属？
- Which failure should enter the evaluation set?
  中文翻译：哪个失败应该进入评测集？
- Should the workflow remain assisted, move to limited automation, or return to manual?
  中文翻译：工作流应该保持辅助、走向有限自动化，还是回到手工？

## Use It | 运行验证

### A complete evidence package | 一份完整的证据包

Your submission should contain:

> 你的提交应包含：

- A surface-selection record with verification date.
  中文翻译：带核实日期的产品面选择记录。
- A ten-source registry or a smaller equivalent with every required source class represented.
  中文翻译：十个来源的注册表，或覆盖全部必需来源类别的较小等价物。
- Four prompt-stage contracts.
  中文翻译：四份提示词阶段契约。
- At least ten evaluation cases: four normal, three edge, three governance or adversarial.
  中文翻译：至少十个评测用例：四个正常、三个边界、三个治理或对抗。
- A claim-evidence matrix for every consequential claim.
  中文翻译：每个重大论断的论断-证据矩阵。
- Validator output for one passing and three failing packets.
  中文翻译：一个通过与三个失败数据包的验证器输出。
- Passing unit-test output.
  中文翻译：通过的单元测试输出。
- A completed human handoff checklist.
  中文翻译：填写完成的人工交接清单。
- A one-page retrospective with one concrete workflow change.
  中文翻译：一页复盘，含一条具体的工作流改动。

### Capstone decision patterns | 毕业设计决策模式

> **【中文解读】** 六条决策模式是本课的精华，也是考试场景题的答题模板：没有批准的目的就停下（能力不创造许可）；没有权威证据就弃权或升级（更多提示词变不出一个来源）；精确性质用确定性检查（合计数和 schema 不需要主观评分）；高后果交人工权限（给这个人证据和否决权）；反复失败就修系统（加用例、控制或来源规则）；会变的产品事实要现场核实（记录产品面、日期与出处）。

Use these when reviewing your work or answering exam scenarios:

> 在检查自己的工作或回答考试场景题时使用这些模式：

1. **No approved purpose, stop.** Capability does not create permission.
   中文翻译：**没有批准的目的，停下。**能力不创造许可。
2. **No authoritative evidence, abstain or escalate.** More prompting does not create a source.
   中文翻译：**没有权威证据，弃权或升级。**更多提示词变不出一个来源。
3. **Exact property, deterministic check.** Totals and schemas do not need subjective grading.
   中文翻译：**精确性质，确定性检查。**合计数和 schema 不需要主观评分。
4. **High consequence, human authority.** Give the person evidence and power to reject.
   中文翻译：**高后果，人工权限。**给这个人证据和否决权。
5. **Repeated failure, repair the system.** Add a case, control, or source rule.
   中文翻译：**反复失败，修系统。**增加用例、控制或来源规则。
6. **Changeable product fact, verify live.** Record surface, date, and source.
   中文翻译：**会变的产品事实，现场核实。**记录产品面、日期与出处。

### Common traps | 常见陷阱

- **Starting with the final prompt:** Scope and source failures become prose problems.
  中文翻译：**从最终提示词开始：**范围与来源的失败变成了散文问题。
- **Uploading the archive:** Superseded evidence competes with active policy.
  中文翻译：**上传整个档案库：**被取代的证据与现行策略竞争。
- **Trusting citation syntax:** The cited source may not entail the claim.
  中文翻译：**信任引用格式：**被引用的来源未必能推出该论断。
- **Letting the reviewer rediscover state:** Handoff time consumes the promised savings.
  中文翻译：**让评审者重新摸索状态：**交接时间吃掉了承诺的节省。
- **Automating publication first:** Reversibility and authority are ignored.
  中文翻译：**先自动化发布：**可逆性与权限被忽略。
- **Treating tests as proof of safety:** Unit tests cover implemented rules, not organizational truth.
  中文翻译：**把测试当安全证明：**单元测试覆盖已实现的规则，不覆盖组织层面的事实。
- **Freezing current product details in the design:** Terms, features, models, costs, and limits drift.
  中文翻译：**把当前产品细节冻结进设计：**条款、功能、模型、成本与限额都会漂移。

### Exercises | 练习

1. Replace the fictional scenario with one real recurring task, preserving the five-day gates.
   中文翻译：把虚构场景换成一个真实的周期性任务，保留五天的门。
2. Add a validator rule for a policy unique to your workflow.
   中文翻译：为你的工作流独有的一条策略增加一条验证器规则。
3. Write a failing test before implementing that rule.
   中文翻译：先写一个失败的测试，再实现那条规则。
4. Compare one giant prompt with the four-stage flow across the same ten cases.
   中文翻译：在同样十个用例上，对比单个巨型提示词与四阶段流程。
5. Ask a reviewer to complete the handoff using only your packet. Record every fact they had to request.
   中文翻译：让一位评审者只用你的数据包完成交接。记录他们不得不索要的每一个事实。
6. Calculate cost per accepted brief, including review and rework time.
   中文翻译：计算每份被接受简报的成本，计入评审与返工时间。

## Key Terms | 关键术语

- **Decision workflow:** A sequence that turns governed evidence into a reviewed action or recommendation.
  中文翻译：**决策工作流：**把受治理的证据变成经过评审的行动或建议的序列。
- **Source snapshot:** The fixed, versioned evidence set used for one run.
  中文翻译：**来源快照：**一次运行所使用的固定、版本化的证据集。
- **Consequential claim:** A claim that materially affects a decision or action.
  中文翻译：**重大论断：**实质影响某个决策或行动的论断。
- **Validation packet:** Structured sources, claims, governance, and handoff state checked before release.
  中文翻译：**验证数据包：**发布前接受检查的结构化来源、论断、治理与交接状态。
- **Release level:** Block, revise, or quality status based on consequence.
  中文翻译：**发布分级：**基于后果判定的阻断、修订或质量状态。
- **Decision owner:** The person with authority and accountability for the final choice.
  中文翻译：**决策负责人：**对最终选择拥有权限并承担责任的人。
- **Delta review:** Revalidating changes introduced after an earlier approval.
  中文翻译：**增量复审：**重新验证早先批准之后引入的变更。
- **Evidence of readiness:** Test results, failure cases, approvals, and fallback proof, not a general assurance.
  中文翻译：**就绪证据：**测试结果、失败用例、批准与回退证明，而不是一句泛泛的保证。

## Further Reading | 延伸阅读

- [Claude Certified Associate Foundations Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542847%2FClaude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf)
  中文翻译：Claude 认证助理基础考试指南——本课对齐的官方蓝图
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  中文翻译：Anthropic：构建有效的 Agent——工作流与 Agent 选择的官方文章
- [Anthropic: Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
  中文翻译：Anthropic：定义成功标准并构建评测——官方评测指南
- [Anthropic: API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)
  中文翻译：Anthropic：API 与数据保留——数据级别的官方依据
- [AI Engineering from Scratch: Scope Contracts](../../../../../phases/14-agent-engineering/36-scope-contracts/)
  中文翻译：AI Engineering from Scratch：范围契约——Phase 14 第 36 课
- [AI Engineering from Scratch: Verification Gates](../../../../../phases/14-agent-engineering/38-verification-gates/)
  中文翻译：AI Engineering from Scratch：验证门——Phase 14 第 38 课
- [AI Engineering from Scratch: Multi-Session Handoff](../../../../../phases/14-agent-engineering/40-multi-session-handoff/)
  中文翻译：AI Engineering from Scratch：多会话交接——Phase 14 第 40 课

The official exam blueprint and Claude product behavior can change. This capstone is aligned to the guide effective July 2026 and sources checked on 2026-08-08. Confirm the current guide, product terms, models, limits, and controls before relying on release-specific facts.

> 官方考试蓝图和 Claude 产品行为可能变化。本毕业设计对齐 2026 年 7 月生效的指南，来源核实于 2026-08-08。在依赖版本相关的事实之前，请确认当前指南、产品条款、模型、限额与控制。
