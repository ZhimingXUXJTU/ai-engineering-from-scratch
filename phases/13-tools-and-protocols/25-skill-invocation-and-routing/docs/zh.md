# 技能调用与路由

> 调用是一个权限决策加一个相关性决策。好的 description 帮模型做对选择；好的 policy 决定这个选择是否被允许。

> **【中文解读】** 本课把"谁能调用"（人类可见性 × 模型可选性）和"该不该调用"（路由）拆成两个正交维度，并给出五阶段调用生命周期（eligible→selected→activated→executing→completed）的精确词汇。核心教训：description 写得再好也替代不了 policy。

> **【拓展：Agent Skills 子系列→本课位置】** 本课是 Agent Skills 子系列（Phase 13 · 22-27）的第三课。Lesson 22 定义技能包契约，Lesson 24 解决发现与披露，本课回答"技能如何被触发"：显式调用、隐式调用、应用编排、技能间组合、评测 harness 五条通道。Lesson 26 处理调用之后的权限沙箱与信任，Lesson 27 用 near-miss 评测量化路由质量。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 24（技能发现与渐进式披露）——catalog 元数据是隐式路由的输入，Level 1 描述写法（能力分句 + 触发边界分句）来自那一课。

**类型：** 动手实践
**语言：** Python（标准库）
**前置条件：** Phase 13 · 24（技能发现与渐进式披露）
**预计用时：** 约 105 分钟

## 学习目标

- 区分显式用户调用、隐式模型调用、应用调用与技能间调用。
- 把"人类可见性"与"模型可选性"建模为两个独立的策略维度。
- 写出带正向触发条件和近似未命中（near-miss）边界的路由描述。
- 在 trace 与测试中把资格、选择、激活、参数绑定与执行分开。
- 适配运行时专属的调用字段，而不把它们伪装成可移植的 frontmatter。

## 问题引入

你安装了一个 `database-migration` 技能。用户可以按名运行它，但模型同样能看到它的描述，并在有人问一般性数据库问题时选中它——于是这个技能给一个只需要解释的任务提出了 schema 变更。

你加上 `user-invocable: false`，指望挡住手动运行；在另一个运行时里这个字段被直接忽略。你加上 `disable-model-invocation: true`，指望技能彻底消失；在理解它的运行时里，用户仍然可以显式调用它。

错不在字段名，错在心智模型。"用户能看见它""模型能选中它""应用能预加载它""它内部的工具能执行"是四个独立的事实，一个叫 `invocable` 的布尔值表达不了它们。

路由还有第二种失败模式：描述含糊，几个技能都显得合理；描述塞满关键词，无关任务也会触发。catalog 是一个概率接口——既要紧凑到装得下预算，又要具体到路由得对。

> **【中文解读】** 单布尔开关的失败是本课的出发点：可见性、可选性、可预加载、可执行是四个独立事实。把策略建成正交维度（2×2 矩阵），字段名混乱的问题就消失了。

## 核心概念

> **【中文解读】** 本节要点：五条通道启动生命周期、五个阶段精确分词、人类×模型 2×2 矩阵、资格过滤先于相关性排序。这四件事构成一套可测试的调用模型。

### 五条通道可以启动生命周期

| 角色 | 调用形态 | 典型用途 | 主要风险 |
|---|---|---|---|
| 人类用户 | 在 UI 或 prompt 里点名技能 | 刻意的工作流选择 | 用户期待宿主并不授予的可用性或权限 |
| 模型或自主 agent | 从任务上下文选中 catalog 条目 | 自动化的专家流程 | 误报路由（false-positive routing） |
| 应用 | 通过运行时代码激活或预加载技能 | 固定的产品工作流 | 与单一宿主的隐性耦合 |
| 另一个技能或子 agent | 作为工作流依赖请求一个精确技能 | 组合 | 环路、依赖缺失或上下文渗漏 |
| 评测 harness | 在固定场景下激活一个精确技能 | 可重复度量 | 评测时意外绕过了被研究的生产策略 |

可移植的 Agent Skills 规范定义的是包。它不标准化统一的斜杠命令 UI、隐式路由开关、应用 API 或子 agent 生命周期。

### 调用的五个阶段

```figure
skill-invocation-stages
```

精确使用这些词：

- **Eligible（合格）**：策略允许该角色请求这个技能。
- **Selected（选中）**：用户点名了它，或路由器判断它相关。
- **Activated（激活）**：它的指令进入了工作上下文。
- **Executing（执行中）**：agent 在这些指令下开始了模型或工具工作。
- **Completed（完成）**：输出通过了独立成功检查。

只记录 `skill_used=true` 的 trace 会掩盖失败发生在哪个边界。

> **【中文解读】** 这五个词是调用生命周期的"精确坐标"：eligible 由 policy 决定、selected 由人或路由器决定、activated 是上下文事件、executing 是执行事件、completed 要靠独立成功检查。评测和调试时先问"卡在哪个阶段"，比笼统说"技能没生效"有用得多。

### 人类调用与模型调用构成 2×2 矩阵

| 人类可调用 | 模型可调用 | 模式 | 合适示例 |
|:---:|:---:|---|---|
| 是 | 是 | 共享 | 代码解释、测试规划、文档评审 |
| 是 | 否 | 仅人类 | 发布准备、账单导出、破坏性清理计划 |
| 否 | 是 | 仅模型 | 内部风格指南、领域参考、自动支持流程 |
| 否 | 否 | 禁用或仅应用 | 分阶段放量、废弃包、程序化预加载 |

这个矩阵是一个策略模型，不是标准 YAML。

一个现行宿主用 `disable-model-invocation: true` 表达"仅人类"行、用 `user-invocable: false` 表达"仅模型"行，默认两者皆可。另一个宿主用 `agents/openai.yaml` 的 `allow_implicit_invocation: false` 保留显式调用、关掉隐式选择。这些都是运行时适配器，未知宿主可能直接忽略它们。

那个容易混淆的细节很重要：`user-invocable: false` 不等于"模型不能用它"——它只是在定义它的宿主里移除直接的用户调用；`disable-model-invocation: true` 也不等于"技能被禁用"——它移除模型发起的选择，同时保留显式用户访问。

> 💡 **【类比】** 2×2 矩阵像"餐厅的两种入口"：人类可调用=顾客能直接走进后厨点菜（显式下单），模型可调用=服务员（AI）看到菜单描述后主动推荐这道菜。`user-invocable: false` 是关掉顾客直接下单的窗口（菜还留在服务员能推荐的菜单上），`disable-model-invocation: true` 是把它从服务员的推荐单里撤下（顾客点名仍然能点）。两个开关各管一扇门，别指望一个开关管两扇。

### 显式调用以身份为先

显式调用直接给出身份：

```text
/release-readiness v2.4.0
```

或者：

```text
release-readiness check v2.4.0 without publishing
```

现行 Codex 界面用 `/skills` 做选择、用请求中的裸技能名做显式调用；Claude Code 文档记载 `/skill-name` 和宿主专属的参数展开。精确语法、菜单可见性、引号规则与变量展开都属于宿主。

显式请求仍要过策略。点名一个技能不应绕过缺失的权限、工作区约束、审批门禁或运行时隔离。

### 隐式调用以描述为先

对隐式路由而言，模型最初看到的是 catalog 元数据而不是完整正文。因此 description 就是这个技能的路由接口。

弱：

```yaml
description: Helps with releases.
```

过宽：

```yaml
description: Use for release, version, package, build, deploy, publish, tag, changelog, GitHub, CI, or software tasks.
```

有界：

```yaml
description: Inspect an already prepared release candidate and produce a readiness report. Use when the user asks whether a version, tag, package, or image is ready to publish; do not use for ordinary build failures or feature development.
```

有界版本包含四要素：

1. **能力：** 检查已准备好的候选版本。
2. **输出：** 就绪报告。
3. **正向边界：** 询问发布工件是否就绪。
4. **负向边界：** 普通构建与功能开发不在范围内。

当两个相邻技能共享词汇时，负向边界很有用，但它替代不了 near-miss 评测。

### 路由是带弃权选项的分类

对技能 `s` 和请求 `x`，设想一个路由分数：

```text
score(s, x) = capability_match + trigger_match + context_match - exclusion_match - ambiguity_penalty
```

精确打分可以由 LLM 判断而非算术完成。但工程原则不变：选中必须同时赢过阈值和竞争技能；证据不足时就弃权（abstain）。

```figure
skill-routing-abstention
```

对高影响技能，即使描述很强，隐式路由也可能不合适。当误选的代价超过自动选择的便利时，改用"仅人类"策略。

### 资格必须先于排序

> **【中文解读】** 顺序错误是路由实现最常见的 bug：先给所有已发现技能打分、选出最高分、再检查那一个技能的策略——被禁的最高分会挡住本可入选的合法次高分。正确顺序：先过滤资格、只对合格者打分、选最强且过阈值者、无人合格则弃权。资格定义候选集，相关性只给候选集排序。

不要先给所有已发现技能打分、选出最强匹配、然后再检查那一个技能的策略。被禁的最高分会错误地挡住本可入选的合法次高分。

隐式路由使用这个顺序：

1. 按请求角色和活跃的宿主适配器过滤已发现技能。
2. 只给合格候选打分。
3. 若最强合格匹配过了阈值和歧义规则，选中它。
4. 没有合格候选或合格分数不够强时，弃权。

假设 `incident-triage` 得分 `0.80`，但它的宿主扩展禁用了模型调用；`incident-review` 得分 `0.55` 且允许模型调用。路由器应把 `incident-review` 当作最佳合格候选，而不是选 `incident-triage`、拒绝、然后停止。

这个顺序还让策略变化不至于改变相关性分数的含义：资格定义候选集，相关性只给候选集排序。

### 路由评测需要近似未命中样本

正样本证明召回：

```json
{"prompt":"Is version 2.4.0 ready to publish?","expected":"release-readiness"}
```

明显的负样本证明基础精确率：

```json
{"prompt":"Explain rotary position embeddings.","expected":null}
```

近似未命中暴露边界质量：

```json
{"prompt":"Why did today's package build fail?","expected":"build-diagnostics"}
```

近似未命中样本与发布技能共享 `package`、`build` 词汇，却属于另一个工作流。只由明显正样本和无关负样本组成的路由集会高估质量。

> **【中文解读】** 三类样本各证明一件事：正样本证明召回、明显负样本证明基础精确率、near miss 暴露边界质量。near miss 是"词汇重叠但工作流不同"的请求，它考验的是描述里的负向边界。

### 参数有三种表示

调用参数要跨越多道边界：

```figure
skill-argument-boundaries
```

在每道边界上，保持意图而不把文本当代码：

- 宿主解析器决定命令语法与引号规则。
- 技能按宿主规则收到绑定的文本或变量。
- 指令校验必需值与默认值。
- 工具调用把值转换成有类型 schema 并重新校验。

不要把原始参数插值进 shell 命令。优先选择以参数向量调用的脚本或有类型的 MCP 工具。

### 应用调用是显式编排

产品可以激活技能，因为它的流程已经知道任务类型。例如 pull-request 评审服务可以在用户按下 Review 后预加载 `pull-request-risk-review`。

这消除了路由不确定性，但也产生了对运行时 API 的依赖。把那个适配器放在可移植正文之外：

```figure
skill-host-adapter
```

当另一个合规客户端打开这个技能时，它仍应可读可用。

### 技能间调用是一条工具型边

假设 `release-readiness` 在依赖文件变化时请求 `security-change-review`。

调用方应提供：

- 目标技能身份；
- 有界的任务与工件路径；
- 期望的响应契约；
- 调用原因；
- 不可用时的回退；
- 最大深度或环路规则。

```json
{
  "target_skill": "security-change-review",
  "task": "Review dependency changes in the candidate diff",
  "inputs": ["artifacts/release.diff"],
  "expected": "risk-report.json",
  "max_depth": 2
}
```

第二个技能不会被盲目粘贴进第一个。宿主决定如何激活它、它共享上下文、在分叉中运行，还是通过工具结果返回。

### 上下文生命周期是宿主专属

激活之后，技能正文可能留在对话里、在压缩时被摘要，或在委托上下文中运行。工具许可可能只持续一回合，而指令存活更久；子 agent 可能收到技能但没有父级的全部历史。

不要写依赖隐形生命周期假设的技能。把持久输出放进文件或有类型状态、让重入安全、并写明中断后必须重载什么。

```markdown
On resume, read `artifacts/release-readiness.json` if it exists.
Revalidate the candidate commit before continuing.
Do not repeat an external write whose idempotency key is already recorded.
```

## 动手实现

`code/main.py` 把策略与路由实现为两个分离的适配器。

模型包括：

- `Actor`：人类、模型、自主 agent、应用、技能与 harness 调用方；
- `SkillMetadata`：路由身份；
- `InvocationPolicy`：人类/模型矩阵；
- `InvocationRequest` 与 `InvocationDecision`：可追溯的输入与结果；
- `CorePolicyAdapter`：不带宿主扩展的可移植行为；
- `ExtensionPolicyAdapter`：识别运行时字段；
- `build_invocation_matrix(policy)`：2×2 视图；
- `route_request(skills, request, adapter)`：先资格过滤、再相关性排序、选择与拒绝。

运行：

```bash
cd phases/13-tools-and-protocols/25-skill-invocation-and-routing
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

demo 打印一个矩阵和六条通道（显式人类、隐式模型、自主 agent、应用、技能组合、harness）的决策。扩展适配器的结果会展示被禁的最高词法匹配如何在排序前被移除、合法替代者如何入选。它还包含精确名的允许清单。不需要模型 API。确定性路由器的存在是为了让策略边界可检查，不是宣称词法匹配能复现生产环境的模型路由。

### 为什么核心适配器与扩展适配器要分开

如果一个解析器给见过的每个 frontmatter 字段都赋义，它就把运行时约定悄悄提升成了假标准。分离的适配器强迫调用方说出当前激活的是哪个宿主的语义。

`CorePolicyAdapter` 只使用应用提供的策略。`ExtensionPolicyAdapter` 识别一组明确的宿主字段，并记录是哪个字段改变了决定。

> **【中文解读】** 适配器分离对应本课的主线："哪个宿主的语义在生效"必须是一个显式决定。demo 里的词法打分器只是让排序过程可复现——它的存在是为了让资格/相关性边界可测试。

## 学以致用

发布技能前先写一份调用契约：

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

这份契约是给适配器和测试看的设计文档。除非某标准显式采纳，它不是可移植的 `SKILL.md` frontmatter。

## 产出物

本课产出 `skill-invocation-router` 包：一个调用模型参考、一份示例宿主策略，以及一个不执行任何东西的 CLI——评估一条人类、模型、自主 agent、应用、技能组合或 harness 请求，返回带通道、适配器、分数和原因的 JSON 决定。

单请求 CLI 是一个策略探针，不是完整的触发评测。用 Lesson 27 的正样本 + near-miss 标注设计来计算混淆计数、精确率、召回率和重复运行稳定性。

## 练习

1. 建出人类/模型矩阵的全部四行，并为每行写一个合法用例。
2. 给 `CorePolicyAdapter` 增加"仅应用"激活，证明人类与模型调用方仍被拒绝。
3. 为一个部署技能写十条 near miss。每条 prompt 必须与该技能共享词汇，却属于另一个工作流。
4. 给前两个路由分数之间加一个歧义边界，边界过小时返回 `ask`。
5. 给技能间请求加最大组合深度，并检测一个两技能环路。
6. 把同一份标注集分别跑过核心适配器和扩展适配器，解释每一个变化的决策。

## 关键术语

| 术语 | 人们常说的 | 实际含义 |
|---|---|---|
| 显式调用（Explicit invocation） | "斜杠命令" | 某个角色直接给出技能身份，仍受策略约束 |
| 隐式调用（Implicit invocation） | "模型自己选" | 路由器基于任务上下文从合格 catalog 元数据中选择 |
| User-invocable | "人类能用" | 宿主专属的菜单或直接调用属性，不是核心字段 |
| Model-invocable | "agent 能用" | 在宿主策略下具备隐式模型选择的资格 |
| 调用适配器（Invocation adapter） | "frontmatter 解析器" | 把宿主的字段与 API 映射进已声明策略模型的代码 |
| 近似未命中（Near miss） | "难负样本" | 与技能预期输入相似、但不该触发它的请求 |
| 弃权（Abstention） | "没有选中技能" | 证据缺失或歧义时一个刻意的路由结果 |

## 延伸阅读

- [优化技能描述](https://agentskills.io/skill-creation/optimizing-descriptions)：正向触发、具体性与评测。
- [评测技能](https://agentskills.io/skill-creation/evaluating-skills)：触发与输出评测设计。
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)：Codex 当前的显式与隐式调用控制。
- [Claude Code skills](https://code.claude.com/docs/en/skills)：一个宿主的 `user-invocable`、`disable-model-invocation`、参数与委托上下文。
