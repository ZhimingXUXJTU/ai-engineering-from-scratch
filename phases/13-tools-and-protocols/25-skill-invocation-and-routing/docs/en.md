# Skill Invocation and Routing | 技能调用与路由

> Invocation is an authority decision followed by a relevance decision. A good description helps the model choose; a good policy decides whether that choice is allowed.

> **【中文解读】** 调用（invocation）是两个独立决策的串联：先问权限——"这个角色允许请求这个技能吗"，再问相关性——"这个请求真的该路由到它吗"。好的 description 帮模型做对第二个决策，好的 policy 决定第一个决策的答案；description 写得再好也替代不了 policy。本课把"谁能调用"（人类可见性 × 模型可选性）和"该不该调用"（路由）拆成两个正交维度，并给出五阶段调用生命周期（eligible→selected→activated→executing→completed）的精确词汇。

> **【拓展：Agent Skills 子系列→本课位置】** 本课是 Agent Skills 子系列（Phase 13 · 22-27）的第三课。Lesson 22 定义技能包契约，Lesson 24 解决发现与披露，本课回答"技能如何被触发"：显式调用（用户点名）、隐式调用（模型按描述路由）、应用编排、技能间组合、评测 harness 五条通道。Lesson 26 处理调用之后的权限沙箱与信任，Lesson 27 用 near-miss 评测量化路由质量。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 24（技能发现与渐进式披露）——catalog 元数据是隐式路由的输入，Level 1 描述写法（能力分句 + 触发边界分句）来自那一课。

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 24 (Skill Discovery and Progressive Disclosure) | **前置知识:** Phase 13 · 24（技能发现与渐进式披露）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## Learning Objectives | 学习目标

- Distinguish explicit user invocation, implicit model invocation, application invocation, and skill-to-skill invocation.
  中文翻译：区分显式用户调用、隐式模型调用、应用调用与技能间调用。
- Model human visibility and model eligibility as independent policy dimensions.
  中文翻译：把"人类可见性"与"模型可选性"建模为两个独立的策略维度。
- Write routing descriptions with positive triggers and near-miss boundaries.
  中文翻译：写出带正向触发条件和近似未命中（near-miss）边界的路由描述。
- Separate eligibility, selection, activation, argument binding, and execution in traces and tests.
  中文翻译：在 trace 与测试中把资格、选择、激活、参数绑定与执行分开。
- Adapt runtime-specific invocation fields without presenting them as portable frontmatter.
  中文翻译：适配运行时专属的调用字段，而不把它们伪装成可移植的 frontmatter。

## The Problem | 问题引入

You install a `database-migration` skill. The user can run it by name, but the model also sees its description and selects it when someone asks a general database question. The skill then proposes a schema change for a task that only needed an explanation.

> 你安装了一个 `database-migration` 技能。用户可以按名运行它，但模型同样能看到它的描述，并在有人问一般性数据库问题时选中它——于是这个技能给一个只需要解释的任务提出了 schema 变更。

You add `user-invocable: false`, expecting to block people from running it manually. In another runtime, that field is ignored. You add `disable-model-invocation: true`, expecting the skill to disappear entirely. In the runtime that understands it, the user can still invoke it explicitly.

> 你加上 `user-invocable: false`，指望挡住手动运行；在另一个运行时里这个字段被直接忽略。你加上 `disable-model-invocation: true`，指望技能彻底消失；在理解它的运行时里，用户仍然可以显式调用它。

Nothing is wrong with the field names. The model is wrong. "User can see it," "model can select it," "application can preload it," and "tools inside it can execute" are separate facts. A single boolean called `invocable` cannot express them.

> 错不在字段名，错在心智模型。"用户能看见它""模型能选中它""应用能预加载它""它内部的工具能执行"是四个独立的事实，一个叫 `invocable` 的布尔值表达不了它们。

Routing has a second failure mode. If descriptions are vague, several skills become plausible. If descriptions are stuffed with keywords, unrelated tasks trigger them. The catalog is a probabilistic interface: compact enough to fit, specific enough to route.

> 路由还有第二种失败模式：描述含糊，几个技能都显得合理；描述塞满关键词，无关任务也会触发。catalog 是一个概率接口——既要紧凑到装得下预算，又要具体到路由得对。

## The Concept | 核心概念

> **【中文解读】** 本节要点：(1) 五条通道都能启动调用生命周期——人类用户、模型/自主 agent、应用、另一个技能/子 agent、评测 harness，各有典型用途和主要风险；(2) 五个阶段词汇要精确——eligible（政策允许）/selected（被点名或被路由）/activated（指令进入上下文）/executing（开始干活）/completed（输出通过独立成功检查），只记 `skill_used=true` 会掩盖失败发生在哪个边界；(3) 人类可见 × 模型可选构成 2×2 矩阵；(4) 先过滤资格再排序相关性，否则被禁的最高分会挤掉合法的次高分。

### Five channels can start the lifecycle | 五条通道可以启动生命周期

| Actor | Invocation shape | Typical use | Main risk |
|---|---|---|---|
| Human user | Names a skill in the UI or prompt | Deliberate workflow selection | User expects availability or authority the host does not grant |
| Model or autonomous agent | Selects a catalog entry from task context | Automatic expert procedure | False-positive routing |
| Application | Activates or preloads a skill through runtime code | Fixed product workflow | Hidden coupling to one host |
| Another skill or subagent | Requests an exact skill as a workflow dependency | Composition | Cycles, missing dependency, or context bleed |
| Evaluation harness | Activates an exact skill under a fixed scenario | Repeatable measurement | Tests the skill while accidentally bypassing the production policy under study |

The portable Agent Skills specification defines the package. It does not standardize one universal slash-command UI, implicit-routing flag, application API, or subagent lifecycle.

> 可移植的 Agent Skills 规范定义的是包。它不标准化统一的斜杠命令 UI、隐式路由开关、应用 API 或子 agent 生命周期。

### The five invocation stages | 调用的五个阶段

```figure
skill-invocation-stages
```

Use these words precisely:

- **Eligible** means policy permits this actor to request the skill.
- **Selected** means the user named it or a router judged it relevant.
- **Activated** means its instructions entered the working context.
- **Executing** means the agent began model or tool work under those instructions.
- **Completed** means the output met an independent success check.

A trace that records only `skill_used=true` hides the boundary where a failure happened.

> 只记录 `skill_used=true` 的 trace 会掩盖失败发生在哪个边界。

> **【中文解读】** 这五个词是调用生命周期的"精确坐标"：eligible 由 policy 决定、selected 由人或路由器决定、activated 是上下文事件、executing 是执行事件、completed 要靠独立成功检查。评测和调试时先问"卡在哪个阶段"，比笼统说"技能没生效"有用得多。

### Human and model invocation form a 2x2 matrix | 人类调用与模型调用构成 2×2 矩阵

| Human can invoke | Model can invoke | Mode | Suitable examples |
|:---:|:---:|---|---|
| Yes | Yes | Shared | Code explanation, test planning, documentation review |
| Yes | No | Human-only | Publish preparation, billing export, destructive cleanup plan |
| No | Yes | Model-only | Internal style guide, domain reference, automatic support procedure |
| No | No | Disabled or application-only | Staged rollout, deprecated package, programmatic preload |

The matrix is a policy model, not standard YAML.

> 这个矩阵是一个策略模型，不是标准 YAML。

One current host uses `disable-model-invocation: true` for the human-only row and `user-invocable: false` for the model-only row. The default is both. Another host uses `agents/openai.yaml` with `allow_implicit_invocation: false` to keep explicit invocation while disabling implicit selection. These are runtime adapters. Unknown hosts may ignore them.

> 一个现行宿主用 `disable-model-invocation: true` 表达"仅人类"行、用 `user-invocable: false` 表达"仅模型"行，默认两者皆可；另一个宿主用 `agents/openai.yaml` 的 `allow_implicit_invocation: false` 保留显式调用、关掉隐式选择。这些都是运行时适配器，未知宿主可能直接忽略它们。

The confusing detail matters: `user-invocable: false` does not mean "the model cannot use this." It removes direct user invocation in the host that defines it. `disable-model-invocation: true` does not mean "the skill is disabled." It removes model-initiated selection while keeping explicit user access.

> 那个容易混淆的细节很重要：`user-invocable: false` 不等于"模型不能用它"——它只是在定义它的宿主里移除直接的用户调用；`disable-model-invocation: true` 也不等于"技能被禁用"——它移除模型发起的选择，同时保留显式用户访问。

### Explicit invocation is identity-first | 显式调用以身份为先

An explicit invocation supplies identity directly:

```text
/release-readiness v2.4.0
```

or:

```text
release-readiness check v2.4.0 without publishing
```

Current Codex interfaces document `/skills` for selection and plain skill names in requests for explicit invocation. Claude Code documents `/skill-name` and host-specific argument expansion. The exact syntax, menu visibility, quoting rules, and variable expansion belong to the host.

> 现行 Codex 界面用 `/skills` 做选择、用请求中的裸技能名做显式调用；Claude Code 文档记载 `/skill-name` 和宿主专属的参数展开。精确语法、菜单可见性、引号规则与变量展开都属于宿主。

An explicit request still passes policy. Naming a skill should not bypass missing permissions, workspace constraints, approval gates, or runtime isolation.

> 显式请求仍要过策略。点名一个技能不应绕过缺失的权限、工作区约束、审批门禁或运行时隔离。

### Implicit invocation is description-first | 隐式调用以描述为先

For implicit routing, the model initially sees catalog metadata rather than the full body. The description is therefore the skill's routing interface.

> 对隐式路由而言，模型最初看到的是 catalog 元数据而不是完整正文。因此 description 就是这个技能的路由接口。

Weak:

```yaml
description: Helps with releases.
```

Over-broad:

```yaml
description: Use for release, version, package, build, deploy, publish, tag, changelog, GitHub, CI, or software tasks.
```

Bounded:

```yaml
description: Inspect an already prepared release candidate and produce a readiness report. Use when the user asks whether a version, tag, package, or image is ready to publish; do not use for ordinary build failures or feature development.
```

The bounded version contains:

1. **Capability:** inspect a prepared candidate.
2. **Output:** readiness report.
3. **Positive boundary:** asks whether a release artifact is ready.
4. **Negative boundary:** ordinary builds and development are out of scope.

Negative boundaries are useful when two nearby skills share vocabulary. They are not a replacement for near-miss evals.

> 有界版本包含四要素：(1) 能力——检查已准备好的候选版本；(2) 输出——就绪报告；(3) 正向边界——询问发布工件是否就绪；(4) 负向边界——普通构建与功能开发不在范围内。当两个相邻技能共享词汇时，负向边界很有用，但它替代不了 near-miss 评测。

### Routing is classification with an abstain option | 路由是带弃权选项的分类

For a skill `s` and request `x`, imagine a router score:

```text
score(s, x) = capability_match + trigger_match + context_match - exclusion_match - ambiguity_penalty
```

The exact scoring may be an LLM decision rather than arithmetic. The engineering principle still holds: selection should beat a threshold and a competing skill. When evidence is weak, abstain.

> 精确打分可以由 LLM 判断而非算术完成。但工程原则不变：选中必须同时赢过阈值和竞争技能；证据不足时就弃权（abstain）。

```figure
skill-routing-abstention
```

For high-impact skills, implicit routing may be inappropriate even with a strong description. Use human-only policy when the cost of a false positive exceeds the convenience of automatic selection.

> 对高影响技能，即使描述很强，隐式路由也可能不合适。当误选的代价超过自动选择的便利时，改用"仅人类"策略。

### Eligibility must precede ranking | 资格必须先于排序

> **【中文解读】** 顺序错误是路由实现最常见的 bug：先给所有已发现技能打分、选出最高分、再检查那一个技能的策略——被禁的最高分会挡住本可入选的合法次高分。正确顺序：先按请求角色和宿主适配器过滤资格，只对合格者打分，选最强且过阈值者，无人合格或分数不足则弃权。示例：`incident-triage` 得 0.80 但其宿主扩展禁用模型调用，`incident-review` 得 0.55 且允许——路由器应把 `incident-review` 当作最佳合格候选，而不是选 `incident-triage`、拒绝、然后停止。这个顺序还保证策略变化不会改变相关性分数的含义：资格定义候选集，相关性只给候选集排序。

Do not score every discovered skill, choose the strongest match, and check that one skill's policy afterward. A blocked top match would incorrectly prevent an eligible lower-scored candidate from being considered.

Use this order for implicit routing:

1. Filter discovered skills by the requesting actor and the active host adapter.
2. Score only the eligible candidates.
3. Select the strongest eligible match if it clears the threshold and ambiguity rules.
4. Abstain when no candidate is eligible or no eligible score is strong enough.

Suppose `incident-triage` scores `0.80` but its host extension disables model invocation. `incident-review` scores `0.55` and allows model invocation. The router should evaluate `incident-review` as the best eligible candidate. It should not choose `incident-triage`, deny it, and stop.

This ordering also keeps policy changes from altering the meaning of a relevance score. Eligibility defines the selection set. Relevance ranks that set.

> 这个顺序还让策略变化不至于改变相关性分数的含义：资格定义候选集，相关性只给候选集排序。

### Routing evals need near misses | 路由评测需要近似未命中样本

Positive cases prove recall:

```json
{"prompt":"Is version 2.4.0 ready to publish?","expected":"release-readiness"}
```

Clear negatives prove basic precision:

```json
{"prompt":"Explain rotary position embeddings.","expected":null}
```

Near misses expose boundary quality:

```json
{"prompt":"Why did today's package build fail?","expected":"build-diagnostics"}
```

The near miss shares `package` and `build` with the release skill but belongs elsewhere. A routing set made only of obvious positives and unrelated negatives will overstate quality.

> 近似未命中样本与发布技能共享 `package`、`build` 词汇，却属于另一个工作流。只由明显正样本和无关负样本组成的路由集会高估质量。（三类样本各证明一件事：正样本证明召回、明显负样本证明基础精确率、near miss 暴露边界质量。）

### Arguments have three representations | 参数有三种表示

An invocation argument crosses several boundaries:

```figure
skill-argument-boundaries
```

At each boundary, preserve intent without treating text as code.

- The host parser decides command syntax and quoting.
- The skill receives bound text or variables according to host rules.
- The instructions validate required values and defaults.
- A tool call converts values to a typed schema and revalidates them.

Do not interpolate raw arguments into shell commands. Prefer a script invoked with an argument vector or a typed MCP tool.

> 不要把原始参数插值进 shell 命令。优先选择以参数向量调用的脚本或有类型的 MCP 工具。

### Application invocation is explicit orchestration | 应用调用是显式编排

A product can activate a skill because its workflow already knows the task type. For example, a pull-request review service can preload `pull-request-risk-review` after the user presses Review.

> 产品可以激活技能，因为它的流程已经知道任务类型。例如 pull-request 评审服务可以在用户按下 Review 后预加载 `pull-request-risk-review`。

This removes routing uncertainty but creates a dependency on the runtime API. Keep that adapter outside the portable body:

```figure
skill-host-adapter
```

The skill should remain intelligible when opened by a different compliant client.

> 当另一个合规客户端打开这个技能时，它仍应可读可用。

### Skill-to-skill invocation is a tool-like edge | 技能间调用是一条工具型边

Suppose `release-readiness` asks for `security-change-review` when dependency files changed.

The caller should provide:

- the target skill identity;
- a bounded task and artifact paths;
- the expected response contract;
- the reason for invocation;
- a fallback if unavailable;
- a maximum depth or cycle rule.

```json
{
  "target_skill": "security-change-review",
  "task": "Review dependency changes in the candidate diff",
  "inputs": ["artifacts/release.diff"],
  "expected": "risk-report.json",
  "max_depth": 2
}
```

The second skill is not pasted blindly into the first. The host decides how to activate it and whether it shares context, runs in a fork, or returns through a tool result.

> 第二个技能不会被盲目粘贴进第一个。宿主决定如何激活它、它共享上下文、在分叉中运行，还是通过工具结果返回。（调用方要提供的清单：目标技能身份、有界的任务与工件路径、期望的响应契约、调用原因、不可用时的回退、最大深度或环路规则。）

### Context lifecycle is host-specific | 上下文生命周期是宿主专属

After activation, the skill body may remain in the conversation, be summarized during compaction, or run in a delegated context. Tool allowances may last one turn while instructions persist longer. A subagent may receive the skill without the parent's entire history.

> 激活之后，技能正文可能留在对话里、在压缩时被摘要，或在委托上下文中运行。工具许可可能只持续一回合，而指令存活更久；子 agent 可能收到技能但没有父级的全部历史。

Do not write a skill that depends on an invisible lifetime assumption. Put durable outputs in files or typed state, make re-entry safe, and state what must be reloaded after interruption.

> 不要写依赖隐形生命周期假设的技能。把持久输出放进文件或有类型状态、让重入安全、并写明中断后必须重载什么。

```markdown
On resume, read `artifacts/release-readiness.json` if it exists.
Revalidate the candidate commit before continuing.
Do not repeat an external write whose idempotency key is already recorded.
```

## Build It | 动手实现

> **【中文解读】** `code/main.py` 把策略与路由实现为两个分离的适配器：`CorePolicyAdapter` 只认应用提供的策略、不带任何宿主扩展；`ExtensionPolicyAdapter` 识别一组明确的宿主字段（如 `disable-model-invocation`）并记录是哪个字段改变了决定。分离的意义：如果同一个解析器给所有见过的 frontmatter 字段都赋义，它就把运行时约定悄悄提升成了假标准。demo 打印一个 2×2 矩阵和六条通道（显式人类、隐式模型、自主 agent、应用、技能组合、harness）的决策；扩展适配器的结果会展示被禁的最高词法匹配如何在排序前被移除、合法替代者如何入选。确定性路由器的存在是为了让策略边界可检查，不是宣称词法匹配能复现生产环境的模型路由。

`code/main.py` implements policy and routing as separate adapters.

The model includes:

- `Actor` for human, model, autonomous agent, application, skill, and harness callers;
- `SkillMetadata` for routing identity;
- `InvocationPolicy` for the human/model matrix;
- `InvocationRequest` and `InvocationDecision` for traceable inputs and outcomes;
- `CorePolicyAdapter` for portable behavior with no host extensions;
- `ExtensionPolicyAdapter` for recognized runtime fields;
- `build_invocation_matrix(policy)` for the 2x2 view;
- `route_request(skills, request, adapter)` for eligibility filtering before relevance ranking, selection, and denial.

Run it:

```bash
cd phases/13-tools-and-protocols/25-skill-invocation-and-routing
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

The demo prints one matrix and decisions for explicit human, implicit model, autonomous-agent, application, skill-composition, and harness channels. Its extension-adapter results show a blocked top lexical match being removed before an eligible alternative is ranked. It also includes exact-name allowlists. No model API is required. The deterministic router exists to make policy boundaries inspectable, not to claim that lexical matching reproduces production model routing.

### Why core and extension adapters are separate | 为什么核心适配器与扩展适配器要分开

If one parser assigns meaning to every observed frontmatter field, it silently promotes runtime conventions into a fake standard. Separate adapters force the caller to name which host semantics are active.

> 如果一个解析器给见过的每个 frontmatter 字段都赋义，它就把运行时约定悄悄提升成了假标准。分离的适配器强迫调用方说出当前激活的是哪个宿主的语义。

The `CorePolicyAdapter` uses only application-supplied policy. The `ExtensionPolicyAdapter` recognizes an explicit set of host fields and records which field changed the decision.

> `CorePolicyAdapter` 只使用应用提供的策略。`ExtensionPolicyAdapter` 识别一组明确的宿主字段，并记录是哪个字段改变了决定。

## Use It | 学以致用

Write an invocation contract before publishing a skill:

```yaml
actors:
  human: allow
  model: deny
  application: allow
  skill: deny
explicit_name: release-readiness
arguments:
  candidate: required
  publish: fixed_false
ambiguity: ask_user
missing_dependency: stop
context:
  durable_state: artifacts/release-readiness.json
  max_composition_depth: 2
```

This contract is design documentation for adapters and tests. It is not portable `SKILL.md` frontmatter unless a standard explicitly adopts it.

> 这份契约是给适配器和测试看的设计文档。除非某标准显式采纳，它不是可移植的 `SKILL.md` frontmatter。

## Ship It | 产出物

This lesson produces the `skill-invocation-router` bundle. It includes an invocation-model reference, an example host policy, and a non-executing CLI that evaluates one human, model, autonomous-agent, application, skill-composition, or harness request and returns a JSON decision with channel, adapter, score, and reason.

> 本课产出 `skill-invocation-router` 包：一个调用模型参考、一份示例宿主策略，以及一个不执行任何东西的 CLI——评估一条人类、模型、自主 agent、应用、技能组合或 harness 请求，返回带通道、适配器、分数和原因的 JSON 决定。

The one-request CLI is a policy probe, not a full trigger evaluation. Use the labeled positive and near-miss design in Lesson 27 to compute confusion counts, precision, recall, and repeated-run stability.

> 单请求 CLI 是一个策略探针，不是完整的触发评测。用 Lesson 27 的正样本 + near-miss 标注设计来计算混淆计数、精确率、召回率和重复运行稳定性。

## Exercises | 练习

1. Create all four rows of the human/model matrix and write one legitimate use case for each.
2. Add application-only activation to `CorePolicyAdapter`. Prove that human and model callers remain denied.
3. Write ten near misses for a deployment skill. Each prompt must share vocabulary with the skill while belonging to a different workflow.
4. Add an ambiguity margin between the top two routing scores. Return `ask` when the margin is too small.
5. Add a maximum composition depth to skill-to-skill requests and detect a two-skill cycle.
6. Run the same labeled set through core and extension adapters. Explain every changed decision.

## Key Terms | 关键术语

> 下表左列是术语、中列是"人们常说的"、右列是"实际含义"。最容易踩的两行：`user-invocable` 是宿主专属字段而非核心标准；Abstention（弃权）是一个正当的路由结果，不是故障。

| Term | What people say | What it actually means |
|---|---|---|
| Explicit invocation | "Slash command" | An actor supplies skill identity directly, subject to policy |
| Implicit invocation | "The model chooses" | A router selects from eligible catalog metadata based on task context |
| User-invocable | "Humans can use it" | A host-specific menu or direct-invocation property, not a core field |
| Model-invocable | "The agent can use it" | Eligibility for implicit model selection under host policy |
| Invocation adapter | "Frontmatter parser" | Code that maps a host's fields and APIs into a declared policy model |
| Near miss | "Hard negative" | A non-triggering request that resembles a skill's intended inputs |
| Abstention | "No skill selected" | A deliberate routing result when evidence is absent or ambiguous |

## Further Reading | 延伸阅读

- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) for positive triggers, specificity, and evaluation.
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) for trigger and output eval design.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) for current Codex explicit and implicit invocation controls.
- [Claude Code skills](https://code.claude.com/docs/en/skills) for one host's `user-invocable`, `disable-model-invocation`, arguments, and delegated context.

> 阅读顺序建议：先读 optimizing-descriptions 掌握触发边界写法；再读 evaluating-skills 学触发与输出评测设计；最后对照 Codex 与 Claude Code 两份宿主文档，看同一种策略维度在不同宿主里的字段名差异。
