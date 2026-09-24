# 技能发现与渐进式披露

> 一个技能在正文被加载之前就已经开始发挥作用：名称和描述先为它在 catalog（技能目录）中赢得一席之地；更深层的文件只有当任务真正走到那一步时才进入上下文。

> **【中文解读】** 本课解决两个工程问题：发现（discovery）不是简单的递归文件搜索——要处理作用域、校验、同名冲突和目录发布；渐进式披露（progressive disclosure）必须是有意图的分层加载，否则会退化为"渐进式困惑"。

> **【拓展：Agent Skills 子系列→本课位置】** 本课是 Agent Skills 子系列（Phase 13 · 22-27）的第二课。Lesson 22 定义了技能包的可移植契约（SKILL.md）；本课解决"宿主如何发现技能并分层加载"；Lesson 25 处理调用与路由，Lesson 26 处理权限、沙箱与信任，Lesson 27 处理评测与打包。发现与披露是每个支持 Agent Skills 的宿主（Claude Code、Codex 等）都要面对的第一个运行时问题。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 22（Agent Skills：可移植契约与运行时边界）——SKILL.md 的包结构（frontmatter + 正文 + references/scripts/assets），以及"技能是上下文而非工具"的边界。

**类型：** 动手实践
**语言：** Python（标准库）
**前置条件：** Phase 13 · 22（Agent Skills：可移植契约与运行时边界）
**预计用时：** 约 105 分钟

## 学习目标

- 构建一条文件系统发现流水线，把作用域、校验、冲突策略和 catalog 发布分开处理。
- 解释三级披露：catalog 元数据、活跃指令、任务特定资源。
- 设计引用结构，使 agent 能直达所需细节而无需加载整个包。
- 为 catalog 空间与活跃技能上下文分别做预算。
- 在技能读取自身资源时拒绝路径穿越（path traversal）和符号链接（symlink）逃逸。

## 问题引入

你的 agent 安装了 200 个技能。在会话启动时加载每个 `SKILL.md`、参考文件、脚本和模板，会把当前任务淹没在不相关的流程里；什么都不加载，又迫使用户记住精确的文件系统路径。

通常的折中方案是一个 catalog：先向模型展示每个合格技能的紧凑身份与路由描述，选中之后才加载完整正文。这带来了两个新的工程问题。

第一，发现不只是递归文件搜索。技能可以存在于项目、用户、管理员、插件或内置作用域；两个包可能同名；一个符号链接可能指向受信根之外；一个畸形包可能占掉 catalog 空间，或者变得无法调用。

第二，渐进式披露可能变成渐进式困惑。如果 `SKILL.md` 只说"读相关指南"而包里有十二份指南，模型只能靠猜；如果每份指南又指向另外三个文件，加载就变成无界的图遍历。

一个好的运行时让发现是确定性的、披露是有意图的。

> **【中文解读】** "全量加载"与"零加载"都不可行，catalog 是必然的中间层。但它把问题从"加载多少"转移成"如何发现、如何披露"——这两个问题做不好，catalog 反而制造歧义与困惑。

## 核心概念

> **【中文解读】** 本节把"发现"建模成一条编译器流水线：文件系统是源输入，绝不把原始路径直接发布给模型。要点有五：(1) 作用域是运行时策略；(2) 同名冲突需要 name 之外的身份证；(3) 披露分三级、各级目的不同、预算独立；(4) 引用图要浅；(5) 资源路径是信任边界。

### 发现是一条编译器流水线

把文件系统当作源输入。不要把原始路径直接发布给模型。

```figure
skill-discovery-pipeline
```

每个阶段都应产出结构化数据和结构化失败。一份发现日志应能回答：

- 搜索了哪些根目录？
- 找到了哪些候选？
- 哪些候选被拒绝，为什么？
- 冲突中哪个包胜出？
- 哪些 catalog 条目因预算被截短或省略？

没有这些证据，"模型没有用我的技能"几乎无法诊断。

### 作用域是运行时策略

可移植规范定义的是技能包，而不是统一的安装路径或优先级顺序。搜索哪里由宿主决定。

一个通用运行时可能使用这些作用域：

| 作用域 | 示例根目录 | 归谁所有 |
|---|---|---|
| Workspace（工作区） | `<repo>/.agents/skills/` | 项目维护者 |
| User（用户） | `<user-data>/skills/` | 单个开发者 |
| Administrator（管理员） | `<system>/skills/` | 机器或组织策略 |
| Plugin（插件） | 已签名的插件包 | 插件发布者与安装者 |
| Built-in（内置） | 运行时包 | 运行时厂商 |

截至 2026 年 8 月，Codex 文档记载的项目级发现从 `$CWD/.agents/skills` 沿祖先目录向上直到仓库根，外加用户、管理员和内置位置；它支持符号链接的技能目录；同名技能可能同时出现而不是被合并。这些是 Codex 的行为，不是 `SKILL.md` 的要求；编写适配器时请核对最新的 [Codex 技能文档](https://learn.chatgpt.com/docs/build-skills)。

永远不要从目录名臆造优先级。要把它声明成策略并测试。本课实验给每个 `Scope` 一个显式整数 rank，使同一批候选总是解析出同一结果。

### 同名冲突需要 name 之外的身份证

两个都叫 `release-readiness` 的包可以都是合法的：一个是工作区覆盖，一个是用户默认值。因此一个 catalog 条目至少需要：

```json
{
  "name": "release-readiness",
  "description": "Inspect a release candidate for this repository.",
  "scope": "workspace",
  "source": "/repo/.agents/skills/release-readiness",
  "selected": true
}
```

常见的冲突策略包括：

| 策略 | 收益 | 风险 |
|---|---|---|
| 保留全部候选 | 不隐藏任何东西 | 模型看到歧义名 |
| 最高优先级作用域胜出 | 调用简单 | 本地包可能遮蔽受信包 |
| 拒绝重复 | 没有静默遮蔽 | 合法的覆盖失效 |
| 按来源限定名字 | 身份显式 | 用户可见的名字变长 |

为宿主选定一种策略即可。即便被拒或被遮蔽的候选不进模型 catalog，也要把它们保留在诊断信息里。

### 三级披露

Agent Skills 规范描述的是分阶段加载。关键是每一级的目的都不同。

```figure
skill-disclosure-levels
```

> **【中文解读】** Level 1 解决"模型能否把它和邻居区分开"，Level 2 解决"激活后模型能否正确开工"，Level 3 解决"细节在哪里、何时加载"。三级是三个不同的设计问题，不是一个开关的三档。

#### Level 1：catalog 元数据

模型需要刚好够用的信息把该技能与邻居区分开。规范估算每条约 100 token，但实际序列化和分词方式由宿主决定。

一条有用的描述有两个分句：

```yaml
description: Validate a release candidate and produce a readiness report. Use when the user asks whether a version, tag, or package is ready to publish.
```

第一个分句陈述能力，第二个分句陈述触发边界。Lesson 25 会用正向与近似未命中（near-miss）prompt 来评测这条边界。

#### Level 2：活跃指令

激活之后，正文应当同时充当一张地图和一套流程。规范建议 `SKILL.md` 保持在 500 行以内——这是一个设计信号，不是要填满的指标。

正文应当包含：

- 任务边界；
- 默认工作流；
- 分支条件；
- 指向更深文件的直接引用；
- 工具与脚本契约；
- 失败与停止行为；
- 期望输出及其验证方式。

不要为了缩短入口文件而把核心流程挪进引用。激活必须给模型足够的上下文让它正确起步。

#### Level 3：支撑资源

引用（references）提供文字或数据；脚本（scripts）提供确定性计算；资产（assets）被复制、填充或转换成交付物，而不是被当作指令。

| 目录 | 模型读它？ | 模型执行它？ | 典型内容 |
|---|:---:|:---:|---|
| `references/` | 是，需要时 | 否 | schema、策略、领域指南 |
| `scripts/` | 可以查看 | 通过被许可的工具 | 校验器、转换器、采集器 |
| `assets/` | 仅当有用 | 否 | 模板、fixture、图片、起始文件 |

这些名字是约定，不是魔法能力。宿主仍然需要文件访问工具和执行工具。

### 分支特定的引用胜过主题大杂烩

把入口文件写成一张决策地图：

```markdown
## Choose the path

- For a Python package, read `references/python-release.md`.
- For a container image, read `references/container-release.md`.
- For a documentation-only release, read `references/docs-release.md`.
- If the release combines artifact types, read only the guides for those artifacts.
```

这让每个引用都有一个可观察的加载条件（什么情况读哪个文件）。"读 `references/` 了解更多"则没有。

保持引用图浅。官方指南建议从 `SKILL.md` 直接链接、避免深链。一跳（one hop）让可达性可测试，也降低"必要的约束从未进入上下文"的概率。

```figure
skill-reference-map
```

> **【中文解读】** 引用设计的检验标准是可测试性："Python 包 → 读 python-release.md"是一条可写成断言的规则；"读相关指南"不是。决策地图同时是加载策略和评测用例的来源。

### catalog 预算与活跃上下文是两笔不同的预算

设 `c_i` 为技能 `i` 的序列化 catalog 成本、`B_c` 为 catalog 预算、`b_j` 为活跃正文成本、`r_k` 为实际加载的资源：

```text
catalog_cost = sum(c_i for every published skill)
active_cost = sum(b_j for every activated skill) + sum(r_k for every disclosed resource)
```

削减一笔预算不会自动削减另一笔。短描述能省 catalog 空间，但激活后的 900 行正文照样淹没任务；把正文拆进引用只有当运行时和指令确实避免加载无关分支时，才能真正降低活跃成本。

Codex 目前在已知上下文窗口大小时，把初始技能列表的预算定为窗口的 2%；8,000 字符只是大小未知时的回退值，不是与 2% 叠加的第二道上限。catalog 超出适用预算时，描述可能被截短或省略。这些数字是 Codex 的现行策略，不是 Agent Skills 标准的属性。

> **【中文解读】** 两笔预算对应两个不同的问题：catalog 预算管"模型每次都能看到什么"（持续性成本），活跃上下文预算管"当前任务被什么淹没"（一次性成本）。优化其中一笔时必须分别度量，不能想当然。

### 资源路径是一条信任边界

> **【中文解读】** 字面字符串前缀检查是不够的——路径穿越和指向包外的符号链接都能骗过前缀判断。路径包含只证明"文件在包里"，不证明"内容可信"；内容信任由 Lesson 26 的威胁模型处理。

技能只应读取自己包内的文件。字面前缀检查是不够的：

```text
references/../../../../.ssh/config
references/external-link -> /private/company-secrets
```

用文件系统语义解析包根目录和候选路径，拒绝绝对路径输入，并验证解析后的候选仍在解析后的根之下。是否允许符号链接要在发现之前决定；如果允许，每次都检查解析后的目标。

```figure
skill-resource-containment
```

路径包含不等于内容可信。一个合法的包内引用仍可能包含恶意指令——这个威胁由 Lesson 26 处理。

### 加载必须可观察

在不记录秘密的前提下记录披露事件：

```json
{
  "event": "skill.resource.loaded",
  "skill": "release-readiness",
  "resource": "references/python-release.md",
  "reason": "candidate contains pyproject.toml",
  "bytes": 2840
}
```

reason 字段把一次上下文选择变成可评审的证据，也能帮助定位那些让 agent "以防万一"加载每个文件的指令。

## 动手实现

`code/main.py` 构建一个确定性的发现与披露引擎。

发现侧的接口包括：

- `Scope`：来源与优先级元数据；
- `SkillCandidate`：未校验的文件系统候选；
- `discover_scope(scope)`：枚举直接子目录里的技能；
- `resolve_collisions(candidates, precedence)`：应用一条已声明的冲突策略；
- `CatalogEntry` 与 `build_catalog(...)`：发布有界元数据；
- `CatalogBudget`：核算序列化条目，而不是假装字符数等于通用 token 数。

披露侧的接口包括：

- `load_skill_body(entry, ...)`：Level 2 激活；
- `validate_reference(skill_dir, reference)`：路径包含校验；
- `load_reference(...)`：有界的 Level 3 读取。

运行实验：

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

这个代码块需要本地克隆，并从克隆内任意工作目录解析仓库根。

demo 会创建临时项目与用户作用域、插入一个冲突、在刻意调小的预算下构建 catalog、激活一个技能，并分别尝试一次合法引用读取和一次穿越逃逸。不安装任何永久文件。

### 为什么发现是浅层的

`discover_scope` 只检查直接子目录里的 `SKILL.md`，不把每个嵌套的 `SKILL.md` 递归地当作独立包。这保住了包边界，避免意外发布已安装技能内部的示例或 fixture。

### 为什么实验不解析任意 YAML

实验只支持 catalog 所需的标量 frontmatter。生产运行时应使用安全的 YAML 解析器——显式 schema、大小限制、禁用自定义对象构造。"仅标准库"是教学约束，不是默许悄悄发明一种残缺的 YAML 方言。

> **【中文解读】** 实验代码的两处"刻意简化"都有教学理由：浅层发现保住包边界；不写完整 YAML 解析器是为了不把教学约束变成隐性标准。真实运行时在这两处都应替换为经过审计的实现。

## 学以致用

把这份清单套用到任何发现适配器上：

1. 列出每个已配置的根目录，以及谁对它有写权限。
2. 声明是否允许符号链接的技能包。
3. 校验包名、目录名、必需元数据和入口正文大小。
4. 在内部身份中保留来源与作用域。
5. 声明并测试同名行为。
6. 度量发给模型的精确序列化 catalog。
7. 记录正文或资源被加载的原因。
8. 让资源读取留在解析后的包根之内。
9. 引用的文件缺失时清晰失败。
10. 安装或策略变化时重建 catalog。

## 产出物

本课产出 `skill-catalog-builder` 包。它按显式声明的顺序扫描根目录，拒绝符号链接入口文件和名字-目录不匹配，解析跨作用域冲突，拒绝同等优先级的重复项，并把选中的元数据装进已声明的条目数、描述长度和序列化字符预算。

它的 JSON 报告包含选中的条目、被遮蔽的候选、被省略的条目、校验错误、优先级和预算占用。正文与引用的加载仍是独立的运行时操作——catalog 构建器不执行脚本，也不把整个包放进上下文。

## 练习

1. 增加一个插件作用域，放在用户与内置优先级之间，用测试证明冲突结果。
2. 把冲突策略从"最高优先级胜出"改为"按来源限定名"，让两个条目都保留在 catalog 里。
3. 给 `load_reference` 增加字节大小上限。测试恰好等于上限的文件和超出一字节的文件。
4. 写两条听起来几乎一样的描述，改写它们使触发边界不再重叠。
5. 增加一个包含全部引用与脚本哈希的 manifest，在加载前检测被修改的资源。
6. 给 demo 加仪表，分别报告 Level 1、Level 2、Level 3 的字节数。

## 关键术语

| 术语 | 人们常说的 | 实际含义 |
|---|---|---|
| 技能发现（Skill discovery） | "找到每个 SKILL.md" | 搜索已配置作用域、校验包、附加来源、应用策略 |
| 技能 catalog | "已安装技能的列表" | 面向模型的紧凑路由元数据，只含合格包 |
| 冲突策略（Collision policy） | "哪个重名者胜出" | 一条已声明的、处理来自不同来源同名候选的规则 |
| 渐进式披露（Progressive disclosure） | "懒加载" | 从 catalog 到正文到分支资源的分阶段上下文准入 |
| 引用图（Reference graph） | "技能链接的文件" | 可达的资源结构及其加载条件 |
| 路径包含（Path containment） | "待在文件夹里" | 验证解析后的资源目标仍在解析后的包根之内 |

## 延伸阅读

- [Agent Skills 规范](https://agentskills.io/specification)：包形状与渐进式披露分级的规范原文。
- [优化技能描述](https://agentskills.io/skill-creation/optimizing-descriptions)：catalog 路由元数据的写法。
- [Agent Skills 最佳实践](https://agentskills.io/skill-creation/best-practices)：直接引用与入口文件大小。
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)：Codex 当前的作用域发现与 catalog 限额。
