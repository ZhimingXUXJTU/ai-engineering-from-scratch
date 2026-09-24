# Skill Discovery and Progressive Disclosure | 技能发现与渐进式披露

> A skill becomes useful before its body is loaded. Its name and description earn a place in the catalog; its deeper files earn context only when the task reaches them.

> **【中文解读】** 技能在正文被加载之前就已经开始发挥作用：名称和描述先为它在 catalog（技能目录）中赢得一席之地；更深层的文件只有当任务真正走到那一步时才进入上下文。本课解决两个工程问题：发现（discovery）不是简单的递归文件搜索——要处理作用域、校验、同名冲突和目录发布；渐进式披露（progressive disclosure）必须是有意图的分层加载，否则会退化为"渐进式困惑"。

> **【拓展：Agent Skills 子系列→本课位置】** 本课是 Agent Skills 子系列（Phase 13 · 22-27）的第二课。Lesson 22 定义了技能包的可移植契约（SKILL.md）；本课解决"宿主如何发现技能并分层加载"；Lesson 25 处理调用与路由，Lesson 26 处理权限、沙箱与信任，Lesson 27 处理评测与打包。发现与披露是每个支持 Agent Skills 的宿主（Claude Code、Codex 等）都要面对的第一个运行时问题。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 22（Agent Skills：可移植契约与运行时边界）——SKILL.md 的包结构（frontmatter + 正文 + references/scripts/assets），以及"技能是上下文而非工具"的边界。

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 22 (Agent Skills: Portable Contract and Runtime Boundary) | **前置知识:** Phase 13 · 22（Agent Skills：可移植契约与运行时边界）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## Learning Objectives | 学习目标

- Build a filesystem discovery pipeline that separates scope, validation, collision policy, and catalog publication.
  中文翻译：构建一条文件系统发现流水线，把作用域、校验、冲突策略和 catalog 发布分开处理。
- Explain the three disclosure levels: catalog metadata, active instructions, and task-specific resources.
  中文翻译：解释三级披露：catalog 元数据、活跃指令、任务特定资源。
- Design references so an agent can reach required detail directly without loading the entire package.
  中文翻译：设计引用结构，使 agent 能直达所需细节而无需加载整个包。
- Budget catalog space independently from active-skill context.
  中文翻译：为 catalog 空间与活跃技能上下文分别做预算。
- Reject path traversal and symlink escape when a skill reads its own resources.
  中文翻译：在技能读取自身资源时拒绝路径穿越（path traversal）和符号链接（symlink）逃逸。

## The Problem | 问题引入

Your agent has 200 installed skills. Loading every `SKILL.md`, reference file, script, and template at session start would bury the current task in unrelated procedure. Loading nothing would force the user to remember exact filesystem paths.

> 你的 agent 安装了 200 个技能。在会话启动时加载每个 `SKILL.md`、参考文件、脚本和模板，会把当前任务淹没在不相关的流程里；什么都不加载，又迫使用户记住精确的文件系统路径。

The usual compromise is a catalog: show the model a compact identity and routing description for each eligible skill, then load the full body only after selection. That creates two new engineering problems.

> 通常的折中方案是一个 catalog：先向模型展示每个合格技能的紧凑身份与路由描述，选中之后才加载完整正文。这带来了两个新的工程问题。

First, discovery is not just recursive file search. Skills can exist at project, user, administrator, plugin, or built-in scopes. Two packages can share a name. A symlink can point outside the trusted root. A malformed package can consume catalog space or become impossible to invoke.

> 第一，发现不只是递归文件搜索。技能可以存在于项目、用户、管理员、插件或内置作用域；两个包可能同名；一个符号链接可能指向受信根之外；一个畸形包可能占掉 catalog 空间，或者变得无法调用。

Second, progressive disclosure can become progressive confusion. If `SKILL.md` says "read the relevant guide" and the package contains twelve guides, the model must guess. If every guide points to three more files, loading becomes an unbounded graph walk.

> 第二，渐进式披露可能变成渐进式困惑。如果 `SKILL.md` 只说"读相关指南"而包里有十二份指南，模型只能靠猜；如果每份指南又指向另外三个文件，加载就变成无界的图遍历。

A good runtime makes discovery deterministic and disclosure intentional.

> 一个好的运行时让发现是确定性的、披露是有意图的。

## The Concept | 核心概念

> **【中文解读】** 本节把"发现"建模成一条编译器流水线：文件系统是源输入，绝不把原始路径直接发布给模型。要点有五：(1) 作用域（scope）是运行时策略——可移植规范只定义技能包本身，不定义统一安装路径或优先级顺序，宿主必须显式声明搜索哪些根目录、谁对它有写权限；(2) 同名冲突（collision）需要 name 之外的身份证——scope 和 source 要进入 catalog 条目；(3) 披露分三级（catalog 元数据 → 活跃指令 → 支撑资源），各级目的不同、预算独立；(4) 引用图要浅——一跳直达胜过"读 references/ 了解更多"；(5) 资源路径是信任边界，路径包含（containment）要在解析后的真实路径上验证。

### Discovery is a compiler pipeline | 发现是一条编译器流水线

Treat the filesystem as source input. Do not publish raw paths directly to the model.

> 把文件系统当作源输入。不要把原始路径直接发布给模型。

```figure
skill-discovery-pipeline
```

Each stage should produce structured data and structured failures. A discovery log should answer:

- Which roots were searched?
- Which candidates were found?
- Which candidates were rejected, and why?
- Which package won a collision?
- Which catalog entries were shortened or omitted because of budget?

Without that evidence, "the model did not use my skill" is almost impossible to diagnose.

> 没有这些证据，"模型没有用我的技能"几乎无法诊断。（发现日志应能回答：搜索了哪些根目录、找到哪些候选、拒绝了哪些候选及原因、冲突中谁胜出、哪些 catalog 条目因预算被截短或省略。）

### Scope is runtime policy | 作用域是运行时策略

The portable specification defines a skill package, not one universal installation path or precedence order. The host decides where it searches.

> 可移植规范定义的是技能包，而不是统一的安装路径或优先级顺序。搜索哪里由宿主决定。

A generic runtime might use these scopes:

| Scope | Example root | Intended ownership |
|---|---|---|
| Workspace | `<repo>/.agents/skills/` | Project maintainers |
| User | `<user-data>/skills/` | One developer |
| Administrator | `<system>/skills/` | Machine or organization policy |
| Plugin | A signed plugin bundle | Plugin publisher and installer |
| Built-in | Runtime package | Runtime vendor |

As of August 2026, Codex documents project discovery from `$CWD/.agents/skills` through ancestor directories up to the repository root, plus user, administrator, and built-in locations. It supports symlinked skill directories. Duplicate names may both appear rather than being merged. Those are Codex behaviors, not requirements of `SKILL.md`; verify the current [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) when writing an adapter.

Never invent precedence from directory names. Declare it as policy and test it. The lesson lab uses an explicit integer rank for each `Scope` so the same candidate set always resolves the same way.

> 永远不要从目录名臆造优先级。要把它声明成策略并测试。本课实验给每个 `Scope` 一个显式整数 rank，使同一批候选总是解析出同一结果。（表中五种作用域：Workspace=项目维护者、User=单个开发者、Administrator=机器或组织策略、Plugin=插件发布者与安装者、Built-in=运行时厂商。）

### Collisions need identity beyond `name` | 同名冲突需要 name 之外的身份证

Two packages named `release-readiness` can be legitimate. One may be a workspace override and one a user default. A catalog entry therefore needs at least:

```json
{
  "name": "release-readiness",
  "description": "Inspect a release candidate for this repository.",
  "scope": "workspace",
  "source": "/repo/.agents/skills/release-readiness",
  "selected": true
}
```

Common collision policies include:

| Policy | Benefit | Risk |
|---|---|---|
| Keep every candidate | Nothing is hidden | The model sees ambiguous names |
| Highest-precedence scope wins | Simple invocation | A local package can shadow a trusted one |
| Reject duplicates | No silent shadowing | Legitimate overrides stop working |
| Qualify names by source | Explicit identity | User-facing names become longer |

Choose one policy for the host. Preserve the rejected or shadowed candidates in diagnostics even when they are absent from the model catalog.

> 为宿主选定一种策略即可。即便被拒或被遮蔽的候选不进模型 catalog，也要把它们保留在诊断信息里。（四种常见冲突策略：保留全部候选=不隐藏任何东西但模型看到歧义名；最高优先级作用域胜出=调用简单但本地包可能遮蔽受信包；拒绝重复=没有静默遮蔽但合法覆盖失效；按来源限定名=身份显式但用户可见的名字变长。）

### Three disclosure levels | 三级披露

The Agent Skills specification describes staged loading. The key is that each level has a different purpose.

> Agent Skills 规范描述的是分阶段加载。关键是每一级的目的都不同。

> **【中文解读】** 三级披露各自解决不同的问题：Level 1（catalog 元数据）解决"模型能否把它和邻居区分开"，规范估算每条约 100 token，描述要写两个分句——能力是什么 + 什么情况触发；Level 2（活跃指令）解决"激活后模型能否正确开工"，规范建议 SKILL.md 保持 500 行以内——这是设计信号不是要填满的指标，主线流程不能为了缩短入口文件而挪进引用；Level 3（支撑资源）里 references 供阅读、scripts 供确定性计算、assets 是模板而非指令——这些名字是约定不是魔法能力，宿主仍需文件访问工具和执行工具。

```figure
skill-disclosure-levels
```

#### Level 1: catalog metadata | Level 1：catalog 元数据

The model needs enough information to distinguish the skill from neighbors. The specification estimates roughly 100 tokens per catalog entry, but actual serialization and tokenization belong to the host.

A useful description has two clauses:

```yaml
description: Validate a release candidate and produce a readiness report. Use when the user asks whether a version, tag, or package is ready to publish.
```

The first clause states the capability. The second states the trigger boundary. Lesson 25 evaluates this boundary with positive and near-miss prompts.

> 第一个分句陈述能力，第二个分句陈述触发边界。Lesson 25 会用正向与近似未命中（near-miss）prompt 来评测这条边界。

#### Level 2: active instructions | Level 2：活跃指令

After activation, the body should function as a map and a procedure. The specification recommends keeping `SKILL.md` under 500 lines. That is a design signal, not a target to fill.

> 激活之后，正文应当同时充当一张地图和一套流程。规范建议 `SKILL.md` 保持在 500 行以内——这是一个设计信号，不是要填满的指标。

The body should contain:

- the task boundary;
- the default workflow;
- branch conditions;
- direct references to deeper files;
- tool and script contracts;
- failure and stopping behavior;
- the expected output and its verification.

Do not move the central workflow into a reference merely to make the entry file short. Activation must give the model enough context to begin correctly.

> 不要为了缩短入口文件而把核心流程挪进引用。激活必须给模型足够的上下文让它正确起步。

#### Level 3: supporting resources | Level 3：支撑资源

References supply prose or data. Scripts provide deterministic computation. Assets are copied, filled, or transformed into deliverables rather than treated as instructions.

> 引用（references）提供文字或数据；脚本（scripts）提供确定性计算；资产（assets）被复制、填充或转换成交付物，而不是被当作指令。

| Directory | Model reads it? | Model executes it? | Typical content |
|---|:---:|:---:|---|
| `references/` | Yes, when needed | No | schemas, policies, domain guides |
| `scripts/` | May inspect it | Through a permitted tool | validators, converters, collectors |
| `assets/` | Only if useful | No | templates, fixtures, images, starter files |

These names are conventions, not magic capabilities. The host still needs file access and an execution tool.

> 这些名字是约定，不是魔法能力。宿主仍然需要文件访问工具和执行工具。

### Branch-specific references beat topic dumps | 分支特定的引用胜过主题大杂烩

Write the entry file as a decision map:

```markdown
## Choose the path

- For a Python package, read `references/python-release.md`.
- For a container image, read `references/container-release.md`.
- For a documentation-only release, read `references/docs-release.md`.
- If the release combines artifact types, read only the guides for those artifacts.
```

This gives every reference an observable load condition. "Read `references/` for more" does not.

> 这让每个引用都有一个可观察的加载条件（什么情况读哪个文件）。"读 `references/` 了解更多"则没有。

Keep the reference graph shallow. The official guidance recommends direct links from `SKILL.md` and avoiding deep chains. One hop makes reachability testable and reduces the chance that a needed constraint never enters context.

> 保持引用图浅。官方指南建议从 `SKILL.md` 直接链接、避免深链。一跳（one hop）让可达性可测试，也降低"必要的约束从未进入上下文"的概率。

```figure
skill-reference-map
```

### Catalog budget and active context are different budgets | catalog 预算与活跃上下文是两笔不同的预算

Let `c_i` be the serialized catalog cost of skill `i`, `B_c` the catalog budget, `b_j` the active body cost, and `r_k` the resources actually loaded.

```text
catalog_cost = sum(c_i for every published skill)
active_cost = sum(b_j for every activated skill) + sum(r_k for every disclosed resource)
```

Reducing one budget does not automatically reduce the other. Short descriptions can save catalog space while an activated 900-line body still overwhelms the task. Splitting the body into references can reduce active cost only when the runtime and instructions actually avoid loading irrelevant branches.

> 削减一笔预算不会自动削减另一笔。短描述能省 catalog 空间，但激活后的 900 行正文照样淹没任务；把正文拆进引用只有当运行时和指令确实避免加载无关分支时，才能真正降低活跃成本。（catalog_cost 是所有已发布技能的序列化成本之和；active_cost 是所有已激活技能的正文成本加上所有已披露资源的成本之和。）

Codex currently budgets the initial skill list at 2 percent of the context
window when the context-window size is known. The 8,000-character value is a
fallback only when that size is unknown; it is not a second cap combined with
the 2 percent rule. When the catalog exceeds the applicable budget,
descriptions may be shortened or omitted. Treat those figures as current
Codex policy, not a property of the Agent Skills standard.

> Codex 目前在已知上下文窗口大小时，把初始技能列表的预算定为窗口的 2%；8,000 字符只是大小未知时的回退值，不是与 2% 叠加的第二道上限。catalog 超出适用预算时，描述可能被截短或省略。这些数字是 Codex 的现行策略，不是 Agent Skills 标准的属性。

### Resource paths are a trust boundary | 资源路径是一条信任边界

> **【中文解读】** 技能只应读取自己包内的文件，而字面字符串前缀检查是不够的——`references/../../../../.ssh/config`（路径穿越）和指向包外的符号链接都能骗过前缀判断。正确做法：用文件系统语义解析包根目录与候选路径、拒绝绝对路径输入、验证解析后的候选仍在解析后的根之下；符号链接是否允许要在发现之前决定，允许则每次校验解析后的目标。另注意：路径包含只证明"文件在包里"，不证明"内容可信"——包内引用照样可能藏着恶意指令，那是 Lesson 26 的威胁模型。

A skill should read only files inside its package. Literal string-prefix checks are not enough:

```text
references/../../../../.ssh/config
references/external-link -> /private/company-secrets
```

Resolve the package root and candidate with filesystem semantics, reject absolute inputs, and verify that the resolved candidate remains under the resolved root. Decide whether symlinks are allowed before discovery. If allowed, check the resolved target every time.

> 用文件系统语义解析包根目录和候选路径，拒绝绝对路径输入，并验证解析后的候选仍在解析后的根之下。是否允许符号链接要在发现之前决定；如果允许，每次都检查解析后的目标。

```figure
skill-resource-containment
```

Path containment does not establish content trust. A valid in-package reference can still contain malicious instructions. Lesson 26 handles that threat.

> 路径包含不等于内容可信。一个合法的包内引用仍可能包含恶意指令——这个威胁由 Lesson 26 处理。

### Loading must be observable | 加载必须可观察

Record disclosure events without logging secrets:

```json
{
  "event": "skill.resource.loaded",
  "skill": "release-readiness",
  "resource": "references/python-release.md",
  "reason": "candidate contains pyproject.toml",
  "bytes": 2840
}
```

The reason turns a context choice into reviewable evidence. It also helps identify instructions that cause the agent to load every file "just in case."

> reason 字段把一次上下文选择变成可评审的证据，也能帮助定位那些让 agent "以防万一"加载每个文件的指令。

## Build It | 动手实现

> **【中文解读】** `code/main.py` 构建一个确定性的发现与披露引擎。发现侧：`Scope`（来源与优先级元数据）、`SkillCandidate`（未校验的文件系统候选）、`discover_scope`（枚举直接子目录里的技能）、`resolve_collisions`（应用一条已声明的冲突策略）、`CatalogEntry` + `build_catalog`（发布有界元数据）、`CatalogBudget`（核算序列化条目，而不是假装字符数等于通用 token 数）。披露侧：`load_skill_body`（Level 2 激活）、`validate_reference`（路径包含校验）、`load_reference`（有界的 Level 3 读取）。demo 会创建临时项目与用户作用域、插入一个冲突、在刻意调小的预算下构建 catalog、激活一个技能，并分别尝试一次合法引用读取和一次穿越逃逸——不安装任何永久文件。

`code/main.py` builds a deterministic discovery and disclosure engine.

The discovery surface includes:

- `Scope` for source and precedence metadata;
- `SkillCandidate` for an unvalidated filesystem candidate;
- `discover_scope(scope)` to enumerate immediate skill directories;
- `resolve_collisions(candidates, precedence)` to apply one declared policy;
- `CatalogEntry` and `build_catalog(...)` to publish bounded metadata;
- `CatalogBudget` to account for serialized entries without pretending characters are universal tokens.

The disclosure surface includes:

- `load_skill_body(entry, ...)` for Level 2 activation;
- `validate_reference(skill_dir, reference)` for path containment;
- `load_reference(...)` for bounded Level 3 reads.

Run the lab:

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

This block requires a local clone and resolves the repository root from any
working directory inside that clone.

The demo creates temporary project and user scopes, inserts a collision, builds a catalog under a deliberately small budget, activates one skill, and attempts both a valid reference read and a traversal escape. No permanent files are installed.

### Why discovery is shallow | 为什么发现是浅层的

`discover_scope` checks immediate child directories for `SKILL.md`. It does not recursively treat every nested `SKILL.md` as a separate package. This preserves the package boundary and avoids accidentally publishing examples or fixtures inside an installed skill.

> `discover_scope` 只检查直接子目录里的 `SKILL.md`，不把每个嵌套的 `SKILL.md` 递归地当作独立包。这保住了包边界，避免意外发布已安装技能内部的示例或 fixture。

### Why the lab does not parse arbitrary YAML | 为什么实验不解析任意 YAML

The lab supports the scalar frontmatter needed for its catalog. A production runtime should use a safe YAML parser with an explicit schema, size limits, and disabled custom object construction. "Stdlib-only" is a teaching constraint, not permission to invent a partial YAML dialect silently.

> 实验只支持 catalog 所需的标量 frontmatter。生产运行时应使用安全的 YAML 解析器——显式 schema、大小限制、禁用自定义对象构造。"仅标准库"是教学约束，不是默许悄悄发明一种残缺的 YAML 方言。

## Use It | 学以致用

Apply this checklist to any discovery adapter:

1. List every configured root and who can write to it.
2. State whether symlinked packages are allowed.
3. Validate package name, directory name, required metadata, and entry-body size.
4. Preserve source and scope in the internal identity.
5. Declare and test duplicate-name behavior.
6. Measure the exact serialized catalog sent to the model.
7. Record why a body or resource was loaded.
8. Keep resource reads inside the resolved package root.
9. Fail clearly when a referenced file is missing.
10. Rebuild the catalog when installations or policies change.

## Ship It | 产出物

This lesson produces the `skill-catalog-builder` bundle. It scans explicitly ordered roots, rejects symlinked entry files and name-directory mismatches, resolves cross-scope collisions, rejects equal-precedence duplicates, and fits selected metadata into declared entry, description, and serialized-character budgets.

> 本课产出 `skill-catalog-builder` 包：按显式声明的顺序扫描根目录，拒绝符号链接入口文件和名字-目录不匹配，解析跨作用域冲突，拒绝同等优先级的重复项，并把选中的元数据装进已声明的条目数、描述长度和序列化字符预算。

Its JSON report contains selected entries, shadowed candidates, omitted entries, validation errors, precedence, and budget use. Body and reference loading remain separate runtime operations, so the catalog builder does not execute scripts or admit the whole package into context.

> 它的 JSON 报告包含选中的条目、被遮蔽的候选、被省略的条目、校验错误、优先级和预算占用。正文与引用的加载仍是独立的运行时操作——catalog 构建器不执行脚本，也不把整个包放进上下文。

## Exercises | 练习

1. Add a plugin scope and place it between user and built-in precedence. Prove the collision result with a test.
2. Change the collision policy from highest precedence to qualified names. Preserve both entries in the catalog.
3. Add a byte-size limit to `load_reference`. Test a file exactly at the limit and one byte above it.
4. Create two descriptions that sound nearly identical. Rewrite them so the trigger boundaries do not overlap.
5. Add a manifest containing hashes for every reference and script. Detect a modified resource before loading it.
6. Instrument the demo to report Level 1, Level 2, and Level 3 byte counts separately.

## Key Terms | 关键术语

> 下表左列是术语、中列是"人们常说的"、右列是"实际含义"。注意 Progressive disclosure 不等于"懒加载"——它是从 catalog 到正文到分支资源的分阶段上下文准入；Path containment 不等于"待在文件夹里"——它要在解析后的真实路径上验证。

| Term | What people say | What it actually means |
|---|---|---|
| Skill discovery | "Find every SKILL.md" | Search configured scopes, validate packages, attach provenance, and apply policy |
| Skill catalog | "The list of installed skills" | Compact model-visible routing metadata for eligible packages |
| Collision policy | "Which duplicate wins" | A declared rule for same-name candidates from different sources |
| Progressive disclosure | "Lazy loading" | Staged context admission from catalog to body to branch-specific resources |
| Reference graph | "Files linked by the skill" | The reachable resource structure and its load conditions |
| Path containment | "Stay in the folder" | Verify resolved resource targets remain inside the resolved package root |

## Further Reading | 延伸阅读

- [Agent Skills specification](https://agentskills.io/specification) for package shape and progressive disclosure levels.
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) for catalog routing metadata.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) for direct references and entry-file size.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) for current Codex discovery scopes and catalog limits.

> 阅读顺序建议：先读 Agent Skills 规范掌握包形状与披露分级；再用 optimizing-descriptions 学写路由描述；best-practices 讲直接引用与入口文件大小；最后查 Codex 文档了解某个宿主当前的发现作用域与 catalog 限额。
