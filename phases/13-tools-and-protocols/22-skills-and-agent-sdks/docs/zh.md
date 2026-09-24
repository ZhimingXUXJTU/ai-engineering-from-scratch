# Agent Skills：可移植契约与运行时边界

> 一个 skill 不是"换了个好文件名的长提示词"。它是一个可被发现的包——指令、参考资源和可执行助手脚本——通过运行时契约进入 Agent 的上下文。

> **【中文解读】** 一个 skill 不是"换了个好文件名的长提示词"，而是一个可被发现的包——指令、参考资源和可执行助手脚本——通过运行时契约进入 Agent 的上下文。本课围绕 Agent Skills 规范（agentskills.io）讲三件事：哪些 frontmatter 字段属于可移植核心、哪些属于宿主扩展；skill 生命周期从发现到验证的八个阶段各在哪一层；以及什么时候该用 skill、什么时候该用 MCP 工具、hook、subagent 或普通代码。

> **【拓展：Skill 生态的 2026 版图】** Agent Skills 已从 Anthropic 的一家格式演化为跨宿主开放规范：Claude Code、Codex 等宿主都支持按目录发现 SKILL.md 并渐进式披露其资源；`npx skills` 这类安装器可以把课程里的 skill 装进任意宿主。与之相邻的抽象各管一段：MCP 管"有哪些能力可调用"（本 Phase 06-14 课），AGENTS.md 管仓库级约定，hook 管事件触发的确定性逻辑，subagent 管隔离上下文里的委托工作。后续 24-27 课分别深化发现、调用策略、权限与发布。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13 · 01（工具接口）——skill 与工具的正交关系从这里来；(2) Phase 13 · 05（工具 Schema 设计）——类型化输入输出是 MCP 工具的职责边界；(3) 了解 YAML frontmatter 的基本语法。本课是 23 课毕业项目（打包层）与 24-27 课（skill 生命周期各阶段）的地基。

**类型：** 构建
**语言：** Python（标准库）
**前置条件：** Phase 13 · 01（工具接口）、Phase 13 · 05（工具 Schema 设计）
**时间：** 约 90 分钟

## 学习目标

- 给出 Agent skill 的定义，不与提示词、仓库说明、工具、hook、subagent 或插件混淆。
- 读懂可移植的 `SKILL.md` 契约，并把它与运行时专属扩展区分开。
- 把发现、选择、激活、资源加载、工具使用和验证解释为彼此独立的生命周期阶段。
- 在运行时把 skill 包放进 Agent 目录之前先验证它。
- 为一个具体任务在 skill、MCP 工具、hook、subagent 或普通代码之间做出选择。

## 十分钟首胜

> **【中文解读】** 先动手再讲理论：十分钟左右，你将创建一个最小 skill，把本课的 skill-contract-reviewer 完整包安装进真实 Agent 宿主，显式调用它审查你的 skill、再探测隐式选择，最后干净卸载。条件不满足时退回手工打包练习——契约能学到，但宿主发现与卸载行为只能标记为"未验证"。

在读长篇讲解之前先做这个。你将创建一个小 skill，把完整的 reviewer 包安装进真实 Agent 宿主，调用它、验证结果、再移除它。这用一个可观察的结果证明整个生命周期。

### 真实宿主实验的预检

真实宿主检查点需要 Node.js、`npx`、Python 3、一个选定的支持 skill 的宿主，以及对你在安装器中选择的项目级或用户级 scope 的写权限。先验证本地命令：

```bash
node --version
npx --version
python3 --version
```

安装前先决定用哪个宿主和哪个 scope。若任何条件不满足，可在网站上阅读本课，或继续下面的手工打包练习。该回退能教会你契约，但证明不了宿主发现、调用、捆绑脚本执行或卸载行为——把这些观察标记为待验证。

### 1. 从空工作目录开始

在你存放学习工作的任意父目录中运行以下命令：

```bash
mkdir -p agent-skills-first-run
cd agent-skills-first-run
TARGET_ROOT="$(pwd -P)"
printf 'TARGET_ROOT=%s\n' "$TARGET_ROOT"
ls -A
```

最后一条命令应当没有输出。如果它打印出文件，换一个不同的空目录，让审查有清晰的边界。

为你的第一个 skill 创建目录：

```bash
mkdir -p my-first-skill
```

用以下内容创建 `my-first-skill/SKILL.md`：

```markdown
---
name: my-first-skill
description: Turn rough meeting notes into a compact decision record when the user asks to capture a technical decision.
---

# Decision record

Extract the decision, context, alternatives, owner, and next review date.
If the notes do not contain a decision, ask one clarifying question instead
of inventing one.
```

验证你把文件创建在了预期目录：

```bash
test -f my-first-skill/SKILL.md
```

无输出且退出码为 0 即文件存在。

### 2. 安装完整的 reviewer 包

停留在 `agent-skills-first-run` 并运行：

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-contract-reviewer --full-depth
```

选择你在用的 Agent 宿主和 scope。安装器应列出 `skill-contract-reviewer` 及其写入的目的地。`--full-depth` 是必需的，因为本课的 skill 是一个带参考文件、脚本和资产的嵌套包。

把 `SKILL_ROOT` 设为安装器报告的绝对目录。它必须是包含已安装 `SKILL.md` 的目录，不是课程源码目录，也不是当前工作区：

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-contract-reviewer" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\n' "$SKILL_ROOT"
```

如果 Agent 会话已经打开，请新开会话或使用该宿主的 skill 重扫描命令。不要假设每个宿主都会热重载它的目录。

### 3. 显式调用它

在已安装的 Agent 中，以 `agent-skills-first-run` 为工作目录，使用该宿主支持的语法：

| 宿主 | 显式调用 |
|---|---|
| Codex | `skill-contract-reviewer`，或从 `/skills` 中选择，然后提供审查请求 |
| Claude Code | `/skill-contract-reviewer` 加审查请求 |
| 可移植后备 | `Use skill-contract-reviewer to review the target package.` |

在请求中使用打印出来的 `SKILL_ROOT` 与 `TARGET_ROOT` 绝对值。要求宿主在执行前展开它们，并展示精确解析后的命令，而不是依赖进程工作目录的命令：

```text
Use skill-contract-reviewer to review <TARGET_ROOT>/my-first-skill. The installed bundle root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/check_skill.py <TARGET_ROOT>/my-first-skill. Before running it, show the fully resolved argv. Return the validation report, selected primitives, and one sentence for each selection. Include the resolved script path, resolved target path, cwd, argv, and exit code as execution evidence.
```

解析后的命令应呈这种形态，不留任何占位符：

```bash
python3 "/absolute/install/path/skill-contract-reviewer/scripts/check_skill.py" \
  "/absolute/workspace/path/agent-skills-first-run/my-first-skill"
```

成功的结果具备全部三个属性：

1. 宿主按名称找到 `skill-contract-reviewer`。
2. reviewer 读取包契约并运行其捆绑的验证器。
3. 响应包含一份无结构性错误的验证报告（针对样例），以及有依据的原语选择。

执行证据还必须写明脚本路径、目标路径、cwd、精确参数向量和退出码。缺这些字段的流畅报告证明不了已安装的伴随脚本真的运行了。

若宿主报告 skill 不可用，先核实安装目的地，重扫描或重启一次，再重试显式请求。不要靠改写 skill 描述来掩盖安装失败。

### 4. 探测隐式选择

开一个全新的 Agent 轮次，输入同一任务但不点名 skill：

```text
Review <TARGET_ROOT>/my-first-skill as a reusable agent package and tell me whether its package contract is valid.
```

如果宿主暴露所选 skill，记录它是否选择了 `skill-contract-reviewer`。如果宿主不暴露路由，把隐式选择标记为未验证。显式调用是可移植的后备手段。

### 5. 清理

只移除已安装的 reviewer 包：

```bash
npx skills remove skill-contract-reviewer
```

选择与安装时相同的宿主和 scope。重扫描或新会话之后，对 `skill-contract-reviewer` 的显式请求应报告它不可用。保留 `my-first-skill` 给后续课程，或在学完本 track 后删掉实验目录。

## 问题引入

> **【中文解读】** 两个方向的错误都真实存在：把工作流塞进一条提示词——没有稳定身份、没有发现规则、没有资源边界、没有可测试的包形态；或者反过来把一切可复用指令都当成 skill。第一项工程任务是分类：先决定工件是什么，再决定怎么打包。

假设你的团队有一条可靠的发布工作流：找合并变更、检查迁移说明、更新 changelog、跑打包命令、产出审查清单。

把这条工作流放进一条提示词，好粘贴但难运营。提示词没有稳定身份、没有发现规则、没有资源边界、没有可测试的包形态，也回答不了基本问题：谁可以调用它？模型该在什么时候选中它？它能运行哪些脚本？哪些文件是可信的？上下文被压缩后什么能活下来？

相反的错误是把每条可复用指令都当成 skill。仓库约定、确定性自动化、外部工具、事件 hook 和委托 Agent 解决的是不同的问题。把它们全塞进 `SKILL.md` 会得到一个看似可移植、实则依赖某个宿主未文档化行为的目录。

第一项工程任务是分类。先决定工件是什么，再决定怎么打包。

## 核心概念

> **【中文解读】** 本节铺开七块内容：skill 是什么（编码流程性知识的目录包）；相邻抽象的分工表（提示词/仓库说明/skill/MCP 工具/hook/subagent/插件/学习型 skill 库）；"skill"一词的两层含义；可移植核心契约；运行时扩展第二层；frontmatter 是可执行元数据；以及八阶段生命周期与"skill 和工具正交""skill 与仓库说明不同 scope""skill 之间不 import"三条边界规则。

### Skills 编码流程性知识

Agent skill 是一个以 `SKILL.md` 为入口的目录。入口文件包含 YAML frontmatter 和随后的 Markdown 指令。目录还可以包含参考文件、脚本和资产。

```figure
skill-package-anatomy
```

可部署单元是目录，而不只是 Markdown 文件。一个被复制出来的 `SKILL.md` 若缺了它引用的资源，即使 frontmatter 能解析也是一个坏包。

### 相邻的抽象

| 工件 | 主要职责 | 何时加载或运行 | 不应冒充的东西 |
|---|---|---|---|
| 提示词 | 塑造一次模型交互 | 被应用或用户引入 | 带资源的版本化包 |
| 仓库说明 | 解释一个代码库的长期规则 | 编码运行时进入该 scope | 可复用任务工作流 |
| Agent skill | 提供可复用的流程性知识 | 显式或隐式激活 | 硬性授权边界 |
| MCP 工具 | 暴露类型化的远程能力 | 模型或应用调用它 | 详细操作流程 |
| Hook | 在事件上运行确定性逻辑 | 声明的事件发生时 | 概率性的模型路由 |
| Subagent | 用独立上下文和状态委托工作 | 编排者创建或调用它 | 静态指令包 |
| 插件 | 分发更大的运行时扩展 | 宿主安装或启用它 | 可移植 skill 契约本身 |
| 学习型 skill 库 | 存储经验中发现的行为 | 策略检索先前的程序或轨迹 | 基于标准的 `SKILL.md` 包 |

一个发布 skill 可以告诉 Agent 如何检查发布；一个 MCP 服务器可以暴露发布注册表；一个 hook 可以禁止直接 push；一个 subagent 可以独立审计候选版本。这些部件之所以能组合，是因为它们各守其责。

### "skill"一词指两件不同的事

> **【中文解读】** 研究系统里的 skill 指学习产物——程序、轨迹、策略片段；本 track 的 Agent Skill 指被创作的包。两者都打包"可复用能力"，但实现声明不能共享。

研究系统有时把学习到的程序、成功轨迹或环境特定的策略片段称为 skill。Agent 可以在探索中创造这些工件、按任务相似度检索、执行它们，并按反馈修订库。Phase 14 · 10 构建的就是那种终身学习库。

本 mini-track 中的 Agent Skill 不同。它是一个被创作的包，带声明式文件系统契约、目录元数据、渐进式披露、运行时中介的调用和宿主掌控的工具。它可以由 Agent 生成或改进，但该格式本身不要求学习。

| 维度 | Agent Skill 包 | 学习型 skill 库 |
|---|---|---|
| 基本单元 | `SKILL.md` 目录 | 程序、策略、轨迹或记忆记录 |
| 创建方式 | 创作、生成或整理 | 通常从环境经验中发现 |
| 选择方式 | 目录描述加运行时策略 | 基于任务状态的检索或策略 |
| 执行方式 | 模型遵循指令并调用宿主工具 | 环境运行存储的行为或代码工件 |
| 可移植性 | 包契约可跨兼容宿主 | 常绑定一个环境与动作空间 |
| 评估方式 | 路由、工件、安全与宿主兼容性 | 奖励、成功率、迁移与库增长 |

两个想法都在打包可复用能力。但不应仅因同名就共享实现层面的声明。

### 可移植核心

> **【中文解读】** 可移植核心极小而精确：`name` 与 `description` 两个必填字段构成身份与路由；`license`/`compatibility`/`metadata` 是核心可选字段；`allowed-tools` 属实验性。正文承载操作指令。这个"小核心 + 扩展层"的分层是跨宿主可移植的关键。

Agent Skills 规范要求两个 frontmatter 字段：

```yaml
---
name: release-readiness
description: Inspect a release candidate when the user asks whether a version is ready to publish.
---
```

`name` 是稳定标识符，必须满足规范的命名规则并与父目录名一致。`description` 既是文档也是路由元数据，应当说明 skill 做什么、何时适用。

可移植的可选字段有：

| 字段 | 用途 | 可移植性说明 |
|---|---|---|
| `license` | 声明包的条款 | 核心规范 |
| `compatibility` | 声明环境要求 | 核心规范 |
| `metadata` | 携带字符串值的扩展数据 | 核心规范 |
| `allowed-tools` | 建议预批准的工具 | 实验性；宿主支持不一 |

Markdown 正文承载操作指令。它应当定义工作流、决策点、失败行为和通往支撑资源的直通路径。

```markdown
# Release readiness

Use this workflow for a release candidate, not for ordinary development builds.

1. Read `references/release-policy.md`.
2. Run `python3 scripts/inspect_release.py --format json`.
3. Stop if the report contains a blocking failure.
4. Produce the checklist from `assets/release-checklist.md`.
5. Ask for approval before any publish or tag action.
```

### 运行时扩展是第二层

一些宿主接受额外的 frontmatter 或伴生配置。这些字段可能有用，但不自动可移植。

| 行为 | 宿主扩展示例 | 可移植核心？ |
|---|---|:---:|
| 对模型路由隐藏 skill 但保留用户直接调用 | `disable-model-invocation` | 否 |
| 对用户命令菜单隐藏但允许模型路由 | `user-invocable` | 否 |
| 在命令菜单中显示参数帮助 | `argument-hint` | 否 |
| 在委托上下文中运行 skill | `context`、`agent` | 否 |
| 锁定模型或推理设置 | `model`、`effort` | 否 |
| 注册生命周期自动化 | `hooks` | 否 |
| 在 Codex 中禁用隐式调用 | `agents/openai.yaml` 策略 | 否 |

把每个扩展当作适配器：没有它核心工作流也要保持有效，记录回退方式，并测试消费它的宿主。运行时可能忽略未知字段、拒绝它，或者保留它但不实现对应行为。

### Frontmatter 是可执行的元数据

元数据在 skill 正文被读取之前就改变系统行为。

- 格式错误的 `name` 会让发现失败。
- 含糊的 `description` 会路由来错误的请求。
- 一个"仅人类"标志能把 skill 从模型目录中移除。
- 工具许可能改变宿主是否请求授权。
- 上下文设置能把执行移进独立的 Agent 会话。

像审查配置代码一样审查 frontmatter：验证它、给它做版本管理，并把它的行为纳入评测。

### skill 生命周期

> **【中文解读】** 八阶段：发现 → 验证 → 编目 → 选择 → 激活 → 披露 → 执行 → 验证。每个箭头都是一个带自身故障模式的边界。把这些阶段压扁会造成错误心智模型：被发现的 skill 不等于已激活；已激活的 skill 不等于被授权做它描述的一切；被允许的工具调用不等于结果正确。

```figure
skill-runtime-lifecycle
```

每个箭头都是一个带自身故障模式的边界。

1. **发现（Discovery）**在配置的位置寻找可能的包。
2. **验证（Validation）**在目录发布之前拒绝畸形或不安全的包。
3. **编目（Cataloging）**只暴露精简的 `name` 和 `description`，不是完整包。
4. **选择（Selection）**决定 skill 是否相关。
5. **激活（Activation）**把正文载入模型可见的上下文。
6. **披露（Disclosure）**只在某个分支需要时才读取参考或资产。
7. **执行（Execution）**在宿主的权限与隔离规则下使用宿主工具。
8. **验证（Verification）**独立于模型的声明检查产出的工件。

把这些阶段压扁会造成糟糕的心智模型：被发现的 skill 并未激活；激活的 skill 并未被授权做它描述的一切；被允许的工具调用并不能证明结果正确。

### skill 与工具正交

MCP 回答"这个应用能调用哪些能力、它们的 schema 是什么"；skill 回答"Agent 应如何着手这类任务"。

```figure
skill-tool-orthogonality
```

skill 可以点名某个工具，但真正的能力注册表归宿主所有。若工具缺席，skill 应声明回退或干脆失败，绝不应暗示"点名一个能力就创造了它"。

### skill 与仓库说明是不同的 scope

仓库说明描述你已在其中的环境：命令、约定、生成文件和边界；skill 为一个可能跨许多仓库出现的任务提供可复用流程。

当两者同时适用时，当前用户请求和仓库规则约束 skill。一个通用重构 skill 不得凌驾于"禁止编辑生成文件"的仓库规则之上。

### skill 之间不 import

一个 skill 可以引导 Agent 去调用另一个 skill，但这不是语言级的 import。第二个 skill 仍要经过运行时发现、资格判定、激活、权限和上下文处理。

把跨 skill 依赖写成可观察的工作流边：

```markdown
After producing the candidate changelog, invoke the `release-risk-review` skill.
Pass the candidate path and require a blocking or non-blocking verdict.
If that skill is unavailable, stop and report the missing dependency.
```

这让依赖变得可测试，也给宿主一个执行策略的机会。

## 动手构建

> **【中文解读】** `code/main.py` 实现一个小型面向规范的验证器和一个原语选择器，全程仅用标准库让每条规则可见。验证器返回结构化证据而非一个不透明布尔值；选择器把任务需求映射到正确的原语。验证顺序有讲究：先廉价结构事实，再深层内容规则。

`code/main.py` 实现一个小型面向规范的验证器和一个工件选择器。它保持仅标准库，让每条规则都可见。

验证器暴露：

- `parse_frontmatter(text)`——把元数据与正文分开。
- `validate_skill_text(text, directory_name, allowed_runtime_extensions=())`——检查必填字段、命名、未知扩展、正文存在性和可移植限制。
- `ValidationIssue` 和 `SkillReport`——返回结构化证据而非一个不透明布尔值。
- `FrontmatterSyntaxError`——针对无法安全解释的输入。

选择器暴露 `TaskShape` 和 `select_primitives(task)`。它把任务的需求映射到普通代码、仓库说明、skill、hook、subagent 或 MCP 工具。

运行实验：

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/22-skills-and-agent-sdks
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

这个命令块需要本地克隆，且必须从克隆内的任意位置开始，`git rev-parse --show-toplevel` 才能解析出仓库根目录。

演示为一个合法的可移植 skill、一个带宿主扩展的 skill、一个非法包和若干任务形态决策打印 JSON。研究那些 issue 代码：包验证器应当解释如何修复工件，而不是替作者瞎猜。

### 验证顺序很重要

先验证廉价的结构事实，再上更深的内容规则：

```figure
skill-validation-order
```

这个顺序防止次生错误淹没第一条被破坏的不变式。

## 实际运用

> **【中文解读】** 写 skill 之前先填决策卡：可复用模型判断 → Skill；事件必达 → Hook；类型化外部能力 → 工具/MCP；隔离上下文 → Subagent；单仓库指引 → 仓库说明；一次交互 → 提示词。很多生产工作流会用不止一行——这张卡防止一个工件假装提供所有属性。

写 skill 之前，先填这张决策卡：

| 问题 | 若是 | 可能的原语 |
|---|---|---|
| 需要跨多步的可复用模型判断？ | 流程稳定但决策多变 | Skill |
| 事件每次触发都必须执行？ | 漏一次执行不可接受 | Hook 或应用代码 |
| 模型需要带类型输入的外部能力？ | 操作在模型上下文之外 | 工具或 MCP 服务器 |
| 工作需要隔离的上下文、状态或所有权？ | 独立 worker 返回有界结果 | Subagent |
| 指引只针对一个仓库？ | 描述本地命令与约束 | 仓库说明 |
| 一次交互就够？ | 不需要包生命周期 | 提示词 |

许多生产工作流会用不止一行。这张卡防止一个工件假装自己提供所有属性。

## 产出物

本课产出 `outputs/` 下的 `skill-contract-reviewer` 包。它包含：

- 一个审查候选 skill 包的可移植 `SKILL.md`；
- 针对可移植契约与原语选择的参考清单；
- 一个确定性验证脚本；
- 覆盖提示词、skill、工具、hook、普通代码和 subagent 的任务形态夹具。

安装完整包，而不只是入口文件：

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/install_skills.py /tmp/aiefs-skills --phase 13 --type skill
```

课程安装器报告每个复制的 Phase 13 skill 并写入 `/tmp/aiefs-skills/manifest.json`。这个干净的目的地检查包形态；上面的十分钟首胜循环检查真实宿主中的发现与调用。

后续课程逐层深化生命周期各阶段：第 24 课构建发现与渐进式披露；第 25 课构建调用策略与路由；第 26 课把权限与沙箱分开；第 27 课把整个包变成经评测的发布工件。

## 练习题

1. 用 `TaskShape` 分类你所在团队的五条工作流。为每一个选择了多个原语的案例给出辩护。

2. 添加边界测试，证明 500 字符的 `compatibility` 值通过、501 字符的值以规范错误失败。

3. 向允许列表添加一个运行时扩展。写一个测试证明同一文件仍能与纯可移植 skill 区分开。

4. 把一个 400 行的提示词拆成 `SKILL.md`、一个参考文件、一个脚本契约和一个输出模板。让每个文件只负责一类信息。

5. 为引用了不可用 MCP 工具的 skill 设计失败响应。不要悄悄替换成权限更宽的工具。

6. 审查一个现成 skill，把每句话标注为路由、流程、策略、参考指针或输出契约。移走一切不属于的内容。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| Agent skill | "存下来的提示词" | 由流程性指令和可选资源构成的可发现目录 | Agent skill |
| 可移植核心 | "每个运行时共享的字段" | Agent Skills 规范定义的契约 | Portable core |
| 运行时扩展 | "额外 frontmatter" | 行为需要兼容适配器的宿主专属配置 | Runtime extension |
| 激活 | "skill 跑起来了" | skill 正文进入了模型可见上下文；执行可能稍后发生 | Activation |
| skill 依赖 | "import 另一个 skill" | 带可用性与策略检查的运行时中介调用边 | Skill dependency |
| 工具契约 | "一个函数 schema" | 一个能力的输入、输出、权限、副作用、错误与证据 | Tool contract |

## 延伸阅读

- [Agent Skills 规范](https://agentskills.io/specification)——可移植目录与 frontmatter 契约的出处
- [Agent Skills 最佳实践](https://agentskills.io/skill-creation/best-practices)——范围、指令与资源组织
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)——Codex 当前的发现与调用行为
- [Claude Code skills](https://code.claude.com/docs/en/skills)——一个运行时的调用、参数、工具与委托上下文扩展
