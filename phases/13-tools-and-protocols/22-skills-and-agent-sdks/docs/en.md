# Agent Skills: Portable Contract and Runtime Boundary | Agent Skills：可移植契约与运行时边界

> A skill is not a long prompt with a better filename. It is a discoverable package of instructions, resources, and executable helpers that enters an agent's context through a runtime contract.

> **【中文解读】** 一个 skill 不是"换了个好文件名的长提示词"，而是一个可被发现的包——指令、参考资源和可执行助手脚本——通过运行时契约进入 Agent 的上下文。本课围绕 Agent Skills 规范（agentskills.io）讲三件事：哪些 frontmatter 字段属于可移植核心、哪些属于宿主扩展；skill 生命周期从发现到验证的八个阶段各在哪一层；以及什么时候该用 skill、什么时候该用 MCP 工具、hook、subagent 或普通代码。

> **【拓展：Skill 生态的 2026 版图】** Agent Skills 已从 Anthropic 的一家格式演化为跨宿主开放规范：Claude Code、Codex 等宿主都支持按目录发现 SKILL.md 并渐进式披露其资源；`npx skills` 这类安装器可以把课程里的 skill 装进任意宿主。与之相邻的抽象各管一段：MCP 管"有哪些能力可调用"（本 Phase 06-14 课），AGENTS.md 管仓库级约定，hook 管事件触发的确定性逻辑，subagent 管隔离上下文里的委托工作。后续 24-27 课分别深化发现、调用策略、权限与发布。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13 · 01（工具接口）——skill 与工具的正交关系从这里来；(2) Phase 13 · 05（工具 Schema 设计）——类型化输入输出是 MCP 工具的职责边界；(3) 了解 YAML frontmatter 的基本语法。本课是 23 课毕业项目（打包层）与 24-27 课（skill 生命周期各阶段）的地基。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 01 (The Tool Interface), Phase 13 · 05 (Tool Schema Design) | **前置知识:** Phase 13 · 01（工具接口）、Phase 13 · 05（工具 Schema 设计）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Define an agent skill without confusing it with a prompt, repository instructions, a tool, a hook, a subagent, or a plugin.
  中文翻译：给出 Agent skill 的定义，不与提示词、仓库说明、工具、hook、subagent 或插件混淆。
- Read the portable `SKILL.md` contract and separate it from runtime-specific extensions.
  中文翻译：读懂可移植的 `SKILL.md` 契约，并把它与运行时专属扩展区分开。
- Explain discovery, selection, activation, resource loading, tool use, and verification as distinct lifecycle stages.
  中文翻译：把发现、选择、激活、资源加载、工具使用和验证解释为彼此独立的生命周期阶段。
- Validate a skill package before a runtime places it in an agent's catalog.
  中文翻译：在运行时把 skill 包放进 Agent 目录之前先验证它。
- Choose between a skill, MCP tool, hook, subagent, or ordinary code for a concrete task.
  中文翻译：为一个具体任务在 skill、MCP 工具、hook、subagent 或普通代码之间做出选择。

## Ten-Minute First Success | 十分钟首胜

> **【中文解读】** 先动手再讲理论：十分钟左右，你将创建一个最小 skill（my-first-skill/SKILL.md），用 `npx skills add` 把本课的 skill-contract-reviewer 完整包安装进真实 Agent 宿主，显式调用它审查你的 skill、再探测隐式选择，最后干净卸载。真实宿主检查点需要 Node.js、`npx`、Python 3 和一个支持 skill 的宿主；条件不满足时退回手工打包练习——契约能学到，但宿主发现与卸载行为只能标记为"未验证"。

Do this before the long explanation. You will create a small skill, install
the complete reviewer bundle into a real agent host, invoke it, verify the
result, and remove it. This proves the lifecycle with an observable result.

> 在读长篇讲解之前先做这个。你将创建一个小 skill，把完整的 reviewer 包安装进真实 Agent 宿主，调用它、验证结果、再移除它。这用一个可观察的结果证明整个生命周期。

### Preflight for the real-host lab

The real-host checkpoint requires Node.js, `npx`, Python 3, one selected
skill-capable host, and write access to the project or user scope you choose in
the installer. Verify the local commands first:

> 真实宿主检查点需要 Node.js、`npx`、Python 3、一个选定的支持 skill 的宿主，以及对你在安装器中选择的项目级或用户级 scope 的写权限。先验证本地命令：

```bash
node --version
npx --version
python3 --version
```

Decide which host and scope you will use before installation. If any
requirement is unavailable, read this lesson on the website or continue with
the manual package exercise below. That fallback teaches the contract, but it
does not prove host discovery, invocation, bundled-script execution, or
uninstall behavior. Keep those observations marked pending.

> 安装前先决定用哪个宿主和哪个 scope。若任何条件不满足，可在网站上阅读本课，或继续下面的手工打包练习。该回退能教会你契约，但证明不了宿主发现、调用、捆绑脚本执行或卸载行为——把这些观察标记为待验证。

### 1. Start in an empty working directory

Run these commands from any parent directory where you keep learning work:

> 在你存放学习工作的任意父目录中运行以下命令：

```bash
mkdir -p agent-skills-first-run
cd agent-skills-first-run
TARGET_ROOT="$(pwd -P)"
printf 'TARGET_ROOT=%s\n' "$TARGET_ROOT"
ls -A
```

The final command should print nothing. If it prints files, choose a different
empty directory so the review has a clear boundary.

> 最后一条命令应当没有输出。如果它打印出文件，换一个不同的空目录，让审查有清晰的边界。

Create a directory for your first skill:

> 为你的第一个 skill 创建目录：

```bash
mkdir -p my-first-skill
```

Create `my-first-skill/SKILL.md` with this content:

> 用以下内容创建 `my-first-skill/SKILL.md`：

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

Verify that you created the file in the intended directory:

> 验证你把文件创建在了预期目录：

```bash
test -f my-first-skill/SKILL.md
```

No output and exit code 0 means the file exists.

> 无输出且退出码为 0 即文件存在。

### 2. Install the complete reviewer bundle

Stay in `agent-skills-first-run` and run:

> 停留在 `agent-skills-first-run` 并运行：

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-contract-reviewer --full-depth
```

Choose the agent host and scope you are using. The installer should list
`skill-contract-reviewer` and the destination it wrote. `--full-depth` is
required because this lesson's skill is a nested bundle with references, a
script, and an asset.

> 选择你在用的 Agent 宿主和 scope。安装器应列出 `skill-contract-reviewer` 及其写入的目的地。`--full-depth` 是必需的，因为本课的 skill 是一个带参考文件、脚本和资产的嵌套包。

Set `SKILL_ROOT` to the absolute directory reported by the installer. It must
be the directory containing the installed `SKILL.md`, not the lesson source
directory and not the current workspace:

> 把 `SKILL_ROOT` 设为安装器报告的绝对目录。它必须是包含已安装 `SKILL.md` 的目录，不是课程源码目录，也不是当前工作区：

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-contract-reviewer" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\n' "$SKILL_ROOT"
```

If the agent session was already open, start a new session or use that host's
skill rescan command. Do not assume every host hot-reloads its catalog.

> 如果 Agent 会话已经打开，请新开会话或使用该宿主的 skill 重扫描命令。不要假设每个宿主都会热重载它的目录。

### 3. Invoke it explicitly

In the installed agent, with `agent-skills-first-run` as the working
directory, use the syntax supported by that host:

> 在已安装的 Agent 中，以 `agent-skills-first-run` 为工作目录，使用该宿主支持的语法：

| Host | Explicit invocation |
|---|---|
| Codex | `skill-contract-reviewer`, or choose it from `/skills`, then provide the review request |
| Claude Code | `/skill-contract-reviewer` followed by the review request |
| Portable fallback | `Use skill-contract-reviewer to review the target package.` |

Use the absolute values printed for `SKILL_ROOT` and `TARGET_ROOT` in the
request. Require the host to expand them before execution and show the exact
resolved command, not a command that depends on the process working directory:

> 在请求中使用打印出来的 `SKILL_ROOT` 与 `TARGET_ROOT` 绝对值。要求宿主在执行前展开它们，并展示精确解析后的命令，而不是依赖进程工作目录的命令：

```text
Use skill-contract-reviewer to review <TARGET_ROOT>/my-first-skill. The installed bundle root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/check_skill.py <TARGET_ROOT>/my-first-skill. Before running it, show the fully resolved argv. Return the validation report, selected primitives, and one sentence for each selection. Include the resolved script path, resolved target path, cwd, argv, and exit code as execution evidence.
```

The resolved command should have this shape, with no placeholders remaining:

> 解析后的命令应呈这种形态，不留任何占位符：

```bash
python3 "/absolute/install/path/skill-contract-reviewer/scripts/check_skill.py" \
  "/absolute/workspace/path/agent-skills-first-run/my-first-skill"
```

A successful result has all three properties:

> 成功的结果具备全部三个属性：

1. The host finds `skill-contract-reviewer` by name.
  中文翻译：宿主按名称找到 `skill-contract-reviewer`。
2. The reviewer reads the package contract and runs its bundled validator.
  中文翻译：reviewer 读取包契约并运行其捆绑的验证器。
3. The response contains a validation report with no structural error for the
   sample, plus a justified primitive selection.
  中文翻译：响应包含一份无结构性错误的验证报告（针对样例），以及有依据的原语选择。

The execution evidence must also name the script path, target path, cwd, exact
argument vector, and exit code. A fluent report without those fields does not
prove that the installed companion script ran.

> 执行证据还必须写明脚本路径、目标路径、cwd、精确参数向量和退出码。缺这些字段的流畅报告证明不了已安装的伴随脚本真的运行了。

If the host reports that the skill is unavailable, verify the install
destination, rescan or restart once, and retry the explicit request. Do not
rewrite the skill description to hide an installation failure.

> 若宿主报告 skill 不可用，先核实安装目的地，重扫描或重启一次，再重试显式请求。不要靠改写 skill 描述来掩盖安装失败。

### 4. Probe implicit selection

Start a fresh agent turn and enter the same task without naming the skill:

> 开一个全新的 Agent 轮次，输入同一任务但不点名 skill：

```text
Review <TARGET_ROOT>/my-first-skill as a reusable agent package and tell me whether its package contract is valid.
```

If the host exposes selected skills, record whether it chose
`skill-contract-reviewer`. If the host does not expose routing, mark implicit
selection as unverified. The explicit invocation is the portable fallback.

> 如果宿主暴露所选 skill，记录它是否选择了 `skill-contract-reviewer`。如果宿主不暴露路由，把隐式选择标记为未验证。显式调用是可移植的后备手段。

### 5. Clean up

Remove only the installed reviewer bundle:

> 只移除已安装的 reviewer 包：

```bash
npx skills remove skill-contract-reviewer
```

Select the same host and scope used during installation. After a rescan or new
session, an explicit request for `skill-contract-reviewer` should report that
it is unavailable. Keep `my-first-skill` for the later lessons, or remove the
lab directory after you finish the track.

> 选择与安装时相同的宿主和 scope。重扫描或新会话之后，对 `skill-contract-reviewer` 的显式请求应报告它不可用。保留 `my-first-skill` 给后续课程，或在学完本 track 后删掉实验目录。

## The Problem | 问题引入

> **【中文解读】** 两个方向的错误都真实存在：把工作流塞进一条提示词——没有稳定身份、没有发现规则、没有资源边界、没有可测试的包形态；或者反过来把一切可复用指令都当成 skill——仓库约定、确定性自动化、外部工具、事件 hook、委托 Agent 各管不同的问题，全塞进 SKILL.md 只会得到一个"看起来可移植、实际依赖宿主未文档化行为"的目录。第一项工程任务是分类：先决定工件是什么，再决定怎么打包。

Suppose your team has a reliable release workflow. It finds merged changes, checks migration notes, updates the changelog, runs a packaging command, and produces a review checklist.

> 假设你的团队有一条可靠的发布工作流：找合并变更、检查迁移说明、更新 changelog、跑打包命令、产出审查清单。

Putting that workflow in one prompt makes it easy to paste and hard to operate. The prompt has no stable identity, no discovery rule, no resource boundary, no testable package shape, and no answer to basic questions: Who may invoke it? When should the model select it? Which scripts can it run? Which files are trusted? What survives when context is compacted?

> 把这条工作流放进一条提示词，好粘贴但难运营。提示词没有稳定身份、没有发现规则、没有资源边界、没有可测试的包形态，也回答不了基本问题：谁可以调用它？模型该在什么时候选中它？它能运行哪些脚本？哪些文件是可信的？上下文被压缩后什么能活下来？

The opposite mistake is to treat every reusable instruction as a skill. Repository conventions, deterministic automation, external tools, event hooks, and delegated agents solve different problems. Packing all of them into `SKILL.md` produces a directory that looks portable while depending on one host's undocumented behavior.

> 相反的错误是把每条可复用指令都当成 skill。仓库约定、确定性自动化、外部工具、事件 hook 和委托 Agent 解决的是不同的问题。把它们全塞进 `SKILL.md` 会得到一个看似可移植、实则依赖某个宿主未文档化行为的目录。

The first engineering task is classification. Decide what the artifact is before you decide how to package it.

> 第一项工程任务是分类。先决定工件是什么，再决定怎么打包。

## The Concept | 核心概念

### Skills encode procedural knowledge

An agent skill is a directory whose entry point is `SKILL.md`. The entry file contains YAML frontmatter followed by Markdown instructions. The directory can also contain references, scripts, and assets.

> Agent skill 是一个以 `SKILL.md` 为入口的目录。入口文件包含 YAML frontmatter 和随后的 Markdown 指令。目录还可以包含参考文件、脚本和资产。

```figure
skill-package-anatomy
```

The directory, not the Markdown file alone, is the deployable unit. A copied `SKILL.md` with missing references is a broken package even if its frontmatter parses.

> 可部署单元是目录，而不只是 Markdown 文件。一个被复制出来的 `SKILL.md` 若缺了它引用的资源，即使 frontmatter 能解析也是一个坏包。

### The neighboring abstractions

| Artifact | Primary job | Loaded or run when | What it should not impersonate |
|---|---|---|---|
| Prompt | Shape one model interaction | Included by an application or user | A versioned package with resources |
| Repository instructions | Explain one codebase's standing rules | A coding runtime enters that scope | A reusable task workflow |
| Agent skill | Supply reusable procedural knowledge | Explicit or implicit activation | A hard authorization boundary |
| MCP tool | Expose a typed remote capability | The model or application calls it | A detailed operating procedure |
| Hook | Run deterministic logic on an event | The declared event occurs | Probabilistic model routing |
| Subagent | Delegate work with separate context and state | An orchestrator creates or calls it | A static instruction bundle |
| Plugin | Distribute a larger runtime extension | The host installs or enables it | The portable skill contract itself |
| Learned skill library | Store behavior discovered through experience | A policy retrieves a prior program or trajectory | A standards-based `SKILL.md` package |

A release skill can tell the agent how to inspect a release. An MCP server can expose the release registry. A hook can forbid direct pushes. A subagent can independently audit the candidate. These pieces compose because they keep different responsibilities.

> 一个发布 skill 可以告诉 Agent 如何检查发布；一个 MCP 服务器可以暴露发布注册表；一个 hook 可以禁止直接 push；一个 subagent 可以独立审计候选版本。这些部件之所以能组合，是因为它们各守其责。

### The word "skill" names two different ideas

> **【中文解读】** "skill"一词指两件不同的事：研究系统里它指学习到的程序、成功轨迹或策略片段——Agent 在探索中创造、按任务相似度检索、执行并按反馈修订（Phase 14 · 10 构建这种终身学习库）；而本 track 的 Agent Skill 是一个被创作的包，有声明式文件系统契约、目录元数据、渐进式披露、运行时中介的调用和宿主掌控的工具。两者都打包"可复用能力"，但不能因为同名就共享实现声明。

Research systems sometimes call a learned program, successful trajectory, or environment-specific policy fragment a skill. An agent can create these artifacts during exploration, retrieve them by task similarity, execute them, and revise the library from feedback. Phase 14 · 10 builds that kind of lifelong-learning library.

> 研究系统有时把学习到的程序、成功轨迹或环境特定的策略片段称为 skill。Agent 可以在探索中创造这些工件、按任务相似度检索、执行它们，并按反馈修订库。Phase 14 · 10 构建的就是那种终身学习库。

An Agent Skill in this mini-track is different. It is an authored package with a declared filesystem contract, catalog metadata, progressive disclosure, runtime-mediated invocation, and host-controlled tools. It can be generated or improved by an agent, but learning is not required for the format.

> 本 mini-track 中的 Agent Skill 不同。它是一个被创作的包，带声明式文件系统契约、目录元数据、渐进式披露、运行时中介的调用和宿主掌控的工具。它可以由 Agent 生成或改进，但该格式本身不要求学习。

| Dimension | Agent Skill package | Learned skill library |
|---|---|---|
| Primary unit | `SKILL.md` directory | Program, policy, trajectory, or memory record |
| Creation | Authored, generated, or curated | Usually discovered from environment experience |
| Selection | Catalog description plus runtime policy | Retrieval or policy over task state |
| Execution | Model follows instructions and calls host tools | Environment runs a stored behavior or code artifact |
| Portability | Package contract can cross compatible hosts | Often tied to one environment and action space |
| Evaluation | Routing, artifact, safety, and host compatibility | Reward, success rate, transfer, and library growth |

Both ideas package reusable competence. They should not share implementation claims merely because they share a name.

> 两个想法都在打包可复用能力。但不应仅因同名就共享实现层面的声明。

### The portable core

> **【中文解读】** 可移植核心极小：`name`（稳定标识符，须满足命名规则且与父目录名一致）和 `description`（既是文档又是路由元数据，要说清 skill 做什么、何时适用）两个 frontmatter 字段是规范必填；`license`、`compatibility`、`metadata` 是核心可选字段，`allowed-tools` 属实验性、宿主支持不一。Markdown 正文承载操作指令——工作流、决策点、失败行为和通往支撑资源的直通路径。

The Agent Skills specification requires two frontmatter fields:

> Agent Skills 规范要求两个 frontmatter 字段：

```yaml
---
name: release-readiness
description: Inspect a release candidate when the user asks whether a version is ready to publish.
---
```

`name` is the stable identifier. It must satisfy the specification's naming rules and match the parent directory. `description` is both documentation and routing metadata. It should say what the skill does and when it applies.

> `name` 是稳定标识符，必须满足规范的命名规则并与父目录名一致。`description` 既是文档也是路由元数据，应当说明 skill 做什么、何时适用。

The portable optional fields are:

> 可移植的可选字段有：

| Field | Purpose | Portability note |
|---|---|---|
| `license` | State the terms for the package | Core specification |
| `compatibility` | State environmental requirements | Core specification |
| `metadata` | Carry string-valued extension data | Core specification |
| `allowed-tools` | Suggest pre-approved tools | Experimental; host support varies |

The Markdown body holds the operational instructions. It should define the workflow, decision points, failure behavior, and direct paths to supporting resources.

> Markdown 正文承载操作指令。它应当定义工作流、决策点、失败行为和通往支撑资源的直通路径。

```markdown
# Release readiness

Use this workflow for a release candidate, not for ordinary development builds.

1. Read `references/release-policy.md`.
2. Run `python3 scripts/inspect_release.py --format json`.
3. Stop if the report contains a blocking failure.
4. Produce the checklist from `assets/release-checklist.md`.
5. Ask for approval before any publish or tag action.
```

### Runtime extensions are a second layer

Some hosts accept extra frontmatter or companion configuration. Those fields can be useful, but they are not automatically portable.

> 一些宿主接受额外的 frontmatter 或伴生配置。这些字段可能有用，但不自动可移植。

| Behavior | Example host extension | Portable core? |
|---|---|:---:|
| Hide a skill from model routing while keeping direct user invocation | `disable-model-invocation` | No |
| Hide a skill from the user's command menu while allowing model routing | `user-invocable` | No |
| Show argument help in a command menu | `argument-hint` | No |
| Run the skill in delegated context | `context`, `agent` | No |
| Pin model or reasoning settings | `model`, `effort` | No |
| Register lifecycle automation | `hooks` | No |
| Disable implicit invocation in Codex | `agents/openai.yaml` policy | No |

Treat each extension as an adapter. Keep the core workflow valid without it, document the fallback, and test the host that consumes it. A runtime may ignore an unknown field, reject it, or preserve it without implementing the behavior.

> 把每个扩展当作适配器：没有它核心工作流也要保持有效，记录回退方式，并测试消费它的宿主。运行时可能忽略未知字段、拒绝它，或者保留它但不实现对应行为。

### Frontmatter is executable metadata

Metadata changes system behavior before the skill body is read.

> 元数据在 skill 正文被读取之前就改变系统行为。

- A malformed `name` can make discovery fail.
  中文翻译：格式错误的 `name` 会让发现失败。
- A vague `description` can route the wrong requests.
  中文翻译：含糊的 `description` 会路由来错误的请求。
- A human-only flag can remove the skill from the model's catalog.
  中文翻译：一个"仅人类"标志能把 skill 从模型目录中移除。
- A tool allowance can change whether a host asks for permission.
  中文翻译：工具许可能改变宿主是否请求授权。
- A context setting can move execution into a separate agent session.
  中文翻译：上下文设置能把执行移进独立的 Agent 会话。

Review frontmatter like configuration code. Validate it, version it, and include its behavior in evals.

> 像审查配置代码一样审查 frontmatter：验证它、给它做版本管理，并把它的行为纳入评测。

### The skill lifecycle

> **【中文解读】** 八阶段生命周期：发现（在配置的位置找候选包）→ 验证（目录发布前拒绝畸形或不安全的包）→ 编目（只暴露精简的 name+description）→ 选择（判断相关性）→ 激活（把正文载入模型可见上下文）→ 披露（仅在需要某分支时才读参考/资产）→ 执行（在宿主权限与隔离规则下使用宿主工具）→ 验证（独立于模型的声明检查产物）。把这些阶段压扁会造成错误心智模型：被发现的 skill 不等于已激活；已激活的 skill 不等于被授权做它描述的一切；被允许的工具调用不等于结果正确。

```figure
skill-runtime-lifecycle
```

Each arrow is a boundary with its own failure modes.

> 每个箭头都是一个带自身故障模式的边界。

1. **Discovery** finds possible packages in configured locations.
  中文翻译：**发现**在配置的位置寻找可能的包。
2. **Validation** rejects malformed or unsafe packages before catalog publication.
  中文翻译：**验证**在目录发布之前拒绝畸形或不安全的包。
3. **Cataloging** exposes a compact `name` and `description`, not the full package.
  中文翻译：**编目**只暴露精简的 `name` 和 `description`，不是完整包。
4. **Selection** decides whether the skill is relevant.
  中文翻译：**选择**决定 skill 是否相关。
5. **Activation** loads the body into model-visible context.
  中文翻译：**激活**把正文载入模型可见的上下文。
6. **Disclosure** reads references or assets only when a branch requires them.
  中文翻译：**披露**只在某个分支需要时才读取参考或资产。
7. **Execution** uses host tools under the host's permission and isolation rules.
  中文翻译：**执行**在宿主的权限与隔离规则下使用宿主工具。
8. **Verification** checks the produced artifact independently of the model's claim.
  中文翻译：**验证**独立于模型的声明检查产出的工件。

Collapsing these stages causes bad mental models. A discovered skill is not active. An active skill is not authorized to do everything it describes. A permitted tool call is not proof that the result is correct.

> 把这些阶段压扁会造成糟糕的心智模型：被发现的 skill 并未激活；激活的 skill 并未被授权做它描述的一切；被允许的工具调用并不能证明结果正确。

### Skills and tools are orthogonal

MCP answers, "Which capabilities can this application call, and what are their schemas?" A skill answers, "How should an agent approach this class of task?"

> MCP 回答"这个应用能调用哪些能力、它们的 schema 是什么"；skill 回答"Agent 应如何着手这类任务"。

```figure
skill-tool-orthogonality
```

The skill may name a tool, but the host owns the actual capability registry. If the tool is absent, the skill should state a fallback or fail clearly. It should never imply that naming a capability creates it.

> skill 可以点名某个工具，但真正的能力注册表归宿主所有。若工具缺席，skill 应声明回退或干脆失败，绝不应暗示"点名一个能力就创造了它"。

### Skills and repository instructions are different scopes

Repository instructions describe the environment you are already in: commands, conventions, generated files, and boundaries. A skill provides reusable procedure for a task that may occur across many repositories.

> 仓库说明描述你已在其中的环境：命令、约定、生成文件和边界；skill 为一个可能跨许多仓库出现的任务提供可复用流程。

When both apply, the active user request and repository rules constrain the skill. A generic refactoring skill must not override a repository rule that forbids editing generated files.

> 当两者同时适用时，当前用户请求和仓库规则约束 skill。一个通用重构 skill 不得凌驾于"禁止编辑生成文件"的仓库规则之上。

### Skills do not import one another

One skill can direct the agent to invoke another, but this is not a language-level import. The second skill still goes through runtime discovery, eligibility, activation, permissions, and context handling.

> 一个 skill 可以引导 Agent 去调用另一个 skill，但这不是语言级的 import。第二个 skill 仍要经过运行时发现、资格判定、激活、权限和上下文处理。

Write cross-skill dependencies as observable workflow edges:

> 把跨 skill 依赖写成可观察的工作流边：

```markdown
After producing the candidate changelog, invoke the `release-risk-review` skill.
Pass the candidate path and require a blocking or non-blocking verdict.
If that skill is unavailable, stop and report the missing dependency.
```

This makes the dependency testable and gives the host a chance to enforce policy.

> 这让依赖变得可测试，也给宿主一个执行策略的机会。

## Build It | 动手构建

> **【中文解读】** `code/main.py` 实现一个小型面向规范的验证器和一个原语选择器，全程仅用标准库让每条规则可见。验证器提供 `parse_frontmatter`、`validate_skill_text`、`ValidationIssue`/`SkillReport`（结构化证据而非一个不透明布尔值）和 `FrontmatterSyntaxError`；选择器提供 `TaskShape` 与 `select_primitives`，把任务需求映射到普通代码、仓库说明、skill、hook、subagent 或 MCP 工具。验证顺序有讲究：先验证廉价的结构事实，再上深层内容规则，避免次生错误淹没第一条被破坏的不变式。

`code/main.py` implements a small standards-oriented validator and an artifact chooser. It stays stdlib-only so every rule is visible.

> `code/main.py` 实现一个小型面向规范的验证器和一个工件选择器。它保持仅标准库，让每条规则都可见。

The validator exposes:

> 验证器暴露：

- `parse_frontmatter(text)` to separate metadata from the body.
  中文翻译：`parse_frontmatter(text)`——把元数据与正文分开。
- `validate_skill_text(text, directory_name, allowed_runtime_extensions=())` to check required fields, naming, unknown extensions, body presence, and portable limits.
  中文翻译：`validate_skill_text(text, directory_name, allowed_runtime_extensions=())`——检查必填字段、命名、未知扩展、正文存在性和可移植限制。
- `ValidationIssue` and `SkillReport` to return structured evidence instead of one opaque boolean.
  中文翻译：`ValidationIssue` 和 `SkillReport`——返回结构化证据而非一个不透明布尔值。
- `FrontmatterSyntaxError` for input that cannot be interpreted safely.
  中文翻译：`FrontmatterSyntaxError`——针对无法安全解释的输入。

The chooser exposes `TaskShape` and `select_primitives(task)`. It maps a task's needs to ordinary code, repository instructions, a skill, a hook, a subagent, or an MCP tool.

> 选择器暴露 `TaskShape` 和 `select_primitives(task)`。它把任务的需求映射到普通代码、仓库说明、skill、hook、subagent 或 MCP 工具。

Run the lab:

> 运行实验：

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/22-skills-and-agent-sdks
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

This command block requires a local clone and must start from anywhere inside
that clone so `git rev-parse --show-toplevel` can resolve the repository root.

> 这个命令块需要本地克隆，且必须从克隆内的任意位置开始，`git rev-parse --show-toplevel` 才能解析出仓库根目录。

The demo prints JSON for one valid portable skill, one host-extended skill, one invalid package, and several task-shape decisions. Inspect the issue codes. A package validator should explain how to fix an artifact without guessing on the author's behalf.

> 演示为一个合法的可移植 skill、一个带宿主扩展的 skill、一个非法包和若干任务形态决策打印 JSON。研究那些 issue 代码：包验证器应当解释如何修复工件，而不是替作者瞎猜。

### Validation order matters

Validate cheap structural facts before deeper content rules:

> 先验证廉价的结构事实，再上更深的内容规则：

```figure
skill-validation-order
```

This order prevents secondary errors from obscuring the first broken invariant.

> 这个顺序防止次生错误淹没第一条被破坏的不变式。

## Use It | 实际运用

> **【中文解读】** 写 skill 之前先填一张决策卡：需要跨多步的可复用模型判断？→ Skill。事件每次触发都必须执行？→ Hook 或应用代码。需要带类型输入的外部能力？→ 工具或 MCP 服务器。需要隔离的上下文/状态/所有权？→ Subagent。指引只针对一个仓库？→ 仓库说明。一次交互就够？→ 提示词。很多生产工作流会用不止一行——这张卡防止一个工件假装提供所有属性。

Before writing a skill, fill out this decision card:

> 写 skill 之前，先填这张决策卡：

| Question | If yes | Likely primitive |
|---|---|---|
| Does this need reusable model judgment across several steps? | The procedure is stable but decisions vary | Skill |
| Must this happen every time an event fires? | Missing one execution is unacceptable | Hook or application code |
| Does the model need an external capability with typed inputs? | The operation lives outside model context | Tool or MCP server |
| Does the work need isolated context, state, or ownership? | A separate worker returns a bounded result | Subagent |
| Is this guidance specific to one repository? | It describes local commands and constraints | Repository instructions |
| Is one interaction enough? | No package lifecycle is needed | Prompt |

Many production workflows use more than one row. The card prevents one artifact from pretending to provide every property.

> 许多生产工作流会用不止一行。这张卡防止一个工件假装自己提供所有属性。

## Ship It | 产出物

This lesson produces the `skill-contract-reviewer` bundle under `outputs/`. It contains:

> 本课产出 `outputs/` 下的 `skill-contract-reviewer` 包。它包含：

- a portable `SKILL.md` that reviews a proposed skill package;
  中文翻译：一个审查候选 skill 包的可移植 `SKILL.md`；
- reference checklists for the portable contract and primitive selection;
  中文翻译：针对可移植契约与原语选择的参考清单；
- a deterministic validation script;
  中文翻译：一个确定性验证脚本；
- task-shape fixtures covering prompts, skills, tools, hooks, ordinary code, and subagents.
  中文翻译：覆盖提示词、skill、工具、hook、普通代码和 subagent 的任务形态夹具。

Install the full bundle, not only its entry file:

> 安装完整包，而不只是入口文件：

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/install_skills.py /tmp/aiefs-skills --phase 13 --type skill
```

The course installer reports each copied Phase 13 skill and writes
`/tmp/aiefs-skills/manifest.json`. This clean destination checks package shape;
the first-success loop above checks discovery and invocation in a real host.

> 课程安装器报告每个复制的 Phase 13 skill 并写入 `/tmp/aiefs-skills/manifest.json`。这个干净的目的地检查包形态；上面的十分钟首胜循环检查真实宿主中的发现与调用。

The following lessons deepen each lifecycle stage. Lesson 24 builds discovery and progressive disclosure. Lesson 25 builds invocation policy and routing. Lesson 26 separates permissions from sandboxing. Lesson 27 turns the whole package into an evaluated release artifact.

> 后续课程逐层深化生命周期各阶段：第 24 课构建发现与渐进式披露；第 25 课构建调用策略与路由；第 26 课把权限与沙箱分开；第 27 课把整个包变成经评测的发布工件。

## Exercises | 练习题

1. Classify five workflows from your own team using `TaskShape`. Defend every case where you choose more than one primitive.
   中文翻译：用 `TaskShape` 分类你所在团队的五条工作流。为每一个选择了多个原语的案例给出辩护。

2. Add boundary tests proving that a 500-character `compatibility` value passes and a 501-character value fails as a specification error.
   中文翻译：添加边界测试，证明 500 字符的 `compatibility` 值通过、501 字符的值以规范错误失败。

3. Add one runtime extension to the allowlist. Write a test proving the same file is still distinguishable from a portable-only skill.
   中文翻译：向允许列表添加一个运行时扩展。写一个测试证明同一文件仍能与纯可移植 skill 区分开。

4. Split a 400-line prompt into `SKILL.md`, one reference, one script contract, and one output template. Keep every file responsible for one kind of information.
   中文翻译：把一个 400 行的提示词拆成 `SKILL.md`、一个参考文件、一个脚本契约和一个输出模板。让每个文件只负责一类信息。

5. Design a failure response for a skill that references an unavailable MCP tool. Do not silently substitute a tool with broader permissions.
   中文翻译：为引用了不可用 MCP 工具的 skill 设计失败响应。不要悄悄替换成权限更宽的工具。

6. Review an existing skill and label every sentence as routing, procedure, policy, reference pointer, or output contract. Move anything that does not belong.
   中文翻译：审查一个现成 skill，把每句话标注为路由、流程、策略、参考指针或输出契约。移走一切不属于的内容。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| Agent skill | "A saved prompt" | A discoverable directory of procedural instructions and optional resources |
| Portable core | "Fields every runtime shares" | The contract defined by the Agent Skills specification |
| Runtime extension | "Extra frontmatter" | Host-specific configuration whose behavior requires a compatible adapter |
| Activation | "The skill ran" | The skill body entered model-visible context; execution may come later |
| Skill dependency | "Import another skill" | A runtime-mediated invocation edge with availability and policy checks |
| Tool contract | "A function schema" | Inputs, outputs, permissions, side effects, errors, and evidence for a capability |

## Further Reading | 延伸阅读

- [Agent Skills specification](https://agentskills.io/specification) for the portable directory and frontmatter contract.
  中文翻译：Agent Skills 规范——可移植目录与 frontmatter 契约的出处
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) for scope, instructions, and resource organization.
  中文翻译：Agent Skills 最佳实践——范围、指令与资源组织
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) for current Codex discovery and invocation behavior.
  中文翻译：OpenAI 构建 skills——Codex 当前的发现与调用行为
- [Claude Code skills](https://code.claude.com/docs/en/skills) for one runtime's invocation, argument, tool, and delegated-context extensions.
  中文翻译：Claude Code skills——一个运行时的调用、参数、工具与委托上下文扩展
