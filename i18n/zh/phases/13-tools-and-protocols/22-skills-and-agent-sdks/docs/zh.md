# 代理技能:可移植契约与运行时间边界

> 技能不是一个更好的文件名的长时间提示,而是一个可发现的指令,资源和可执行的辅助工具包,通过运行时间合同进入代理的环境.

> **【中文解读】**一个技能不是"换个好文件名的长提示词",而是可发现的包指令,参考资源和可执行辅助脚本.通过运行时合约进入代理的上下文.本课围绕代理技能规范.io讲三个事情:哪些前线材料 字段属于可移植核心,哪些属于主机扩展;技能 生命周期从发现到验证的八个阶段各处;以及什么时候使用技能,什么时候使用MCP工具,,普通或代码.

> **【拓展：Skill 生态的 2026 版图】**经纪人技能已从人类学中发展成跨主体开放规范:Claude Code、Codex等主体都支持按目录发现 SKILL.md 并逐步披露其资源;`npx skills`其他类型的安装器可以将课程中的技能装入任意的主人. 其他类型的抽象管道一段:MCP管道"有哪些能力可调用" (本阶段06-14课),AGENTS.md管库级约定,管事件触发的确定性逻辑,

>  **【前置】**学本课前请先掌握:(1) 第十三阶段 · 01(工具接口) 技能与工具的正交关系从这里来;(2) 第十三阶段 · 05(工具方案设计) 类型化输入输出是MCP工具的职责边界;(3) 了解YAML前线的基本语法──本课是23课毕业项目(打包层) 和24-27课 技能 生命周期各阶段) 的基点──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 01 (The Tool Interface), Phase 13 · 05 (Tool Schema Design) | **前置知识:** Phase 13 · 01（工具接口）、Phase 13 · 05（工具 Schema 设计）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## 学习目标

- 定义一个代理技能,而不用把它混为一谈, 提示,存储器指令,工具,,子器或插件.
  中文翻译:给出代理技能的定义,不与提示词、仓库说明、工具、、子器或插件混──
- 阅读手机`SKILL.md`合同和分离其与运行时间特定的延长.
  中文翻译:读懂可移植的`SKILL.md`契约,并把它与运行时专属扩展区分开.
- 解释发现,选择,激活,资源加载,工具使用和验证作为生命周期的不同阶段.
  中文翻译:把发现,选择,激活,资源加载,工具使用和验证解释为彼此独立的生命周期阶段.
- 在运行时间之前验证技能包,
  中文翻译:在运行时把技能包进代理 目录之前先验证它.
- 选择一个技能,MCP工具,子,子弹或普通代码来完成具体任务.
  中文翻译:为一个具体任务在技能、MCP 工具、、子或普通代码之间做出选择──

## 十分钟的第一场胜利.

> **【中文解读】**首先,你会创造一个最小的技能,用它.`npx skills add`把本课程的技能合同评审员 完整包装装入真实代理 宿主,显然调用它审查你的技能,再探测隐式选择,最后干净卸载.`npx`、Python 3 和一个支持技能的宿主;条件不满足时退回手工打包练习契约能学到,但宿主发现和卸载行为只能标记为"未验证".

在长时间解释之前,你会创造一个小技能,
通过使用完整的审查器捆绑到一个真正的代理主机,
结果,然后取消它. 这证明了生命周期,

> 在读长篇讲解之前先做这个. 你会创建一个小技能,把完整的评论员 包装安装到真实代理主机,调用它,验证结果,再移动它.

### 飞往真正的宿主实验室的前航班

实际主机检查点需要Node.js,`npx`选择一个
能使用技能的主机,并写入您选择的项目或用户范围
首先要检查本地命令:

> 真实宿主检查点需要 Node.js`npx`、Python 3、一个选定的支持技能的主机,以及你在安装器中选择的项目级或用户级范围的写作权.

```bash
node --version
npx --version
python3 --version
```

在安装之前,决定您将使用哪个主机和范围.
您可以在网站上阅读本课程或继续阅读
后面的手动包练习.
没有证明主机发现,调用,捆绑脚本执行,或
让这些观察留下标记.

> 预先决定哪个主机和哪个范围. 如果任何条件不满足,可以在网站上阅读本课程,或继续下面的手工包装练习.

### 1. 在空白的工作目录中启动

在任何学习工作的父母目录中运行这些命令:

> 在你存放学习工作的任意父目录中运行下列命令:

```bash
mkdir -p agent-skills-first-run
cd agent-skills-first-run
TARGET_ROOT="$(pwd -P)"
printf 'TARGET_ROOT=%s\n' "$TARGET_ROOT"
ls -A
```

如果它打印文件,选择不同的命令.
没有任何文件,所以审查有明确的界限.

> 最后一个命令应该没有输出. 如果它打印出文件,换一个不同的空目录,让审查有明确的边界.

创建一个目录,以学习你的第一技能:

> 为了你的第一个技能 创建目录:

```bash
mkdir -p my-first-skill
```

创建`my-first-skill/SKILL.md`含有以下内容:

> 用以下内容创建`my-first-skill/SKILL.md`其他:

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

检查您是否创建文件在预期目录中:

> 验证你在预期目录中创建文件:

```bash
test -f my-first-skill/SKILL.md
```

没有输出和出口代码0意味着文件存在.

> 无输出和退出码为 0 即文件存在――

### 2. 安装完整的审核器包

留在里面`agent-skills-first-run`运行:

> 停留在`agent-skills-first-run`并运行:

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-contract-reviewer --full-depth
```

选择您使用的代理主机和范围.安装器应该列出
`skill-contract-reviewer`它们写的目的地.`--full-depth`是
需要因为这个课程的技能是一个嵌套的集群,
剧本,一个资产.

> 选择您在使用的代理 宿主和范围 装备应列出`skill-contract-reviewer`及其写入目的地`--full-depth`课程的技能是带有参考文件,脚本和资产的嵌套包.

设置`SKILL_ROOT`必须将其转移到安装器报告的绝对目录中.
包含安装的目录`SKILL.md`没有课源
目录,而不是当前的工作空间:

> 让我`SKILL_ROOT`设为安装器报告的绝对目录.`SKILL.md`课程源码目录,也不是当前工作区:

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-contract-reviewer" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\n' "$SKILL_ROOT"
```

如果代理会话已经开放,启动新的会话或使用主机的
不要假设每个主机都热重新加载了其目录.

> 如果代理会话已经开启,请新开会话或使用主人的技能重扫命令.

### 3. 直接要求

在安装的代理中,`agent-skills-first-run`作为工作
导录,使用该主机支持的语法:

> 在安装的代理中,`agent-skills-first-run`为工作目录,使用该主持人支持的语法:

| Host | Explicit invocation |
|---|---|
| Codex | `skill-contract-reviewer`, or choose it from `/skills`, then provide the review request |
| Claude Code | `/skill-contract-reviewer` followed by the review request |
| Portable fallback | `Use skill-contract-reviewer to review the target package.` |

使用打印的绝对值为 `SKILL_ROOT`其他`TARGET_ROOT`在
要求主机在执行之前扩展它们,并显示确切的
解决命令,而不是依赖进程工作目录的命令:

> 在请求中使用印制出来的`SKILL_ROOT`与`TARGET_ROOT`绝对值. 要求主机在执行前展开它们,并显示精确解析后的命令,而不是依赖于进程工作目录的命令:

```text
Use skill-contract-reviewer to review <TARGET_ROOT>/my-first-skill. The installed bundle root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/check_skill.py <TARGET_ROOT>/my-first-skill. Before running it, show the fully resolved argv. Return the validation report, selected primitives, and one sentence for each selection. Include the resolved script path, resolved target path, cwd, argv, and exit code as execution evidence.
```

解析命令应以此形式,没有留下任何位置持有符:

> 解析后的命令应呈现这种形态,不留任何占位符:

```bash
python3 "/absolute/install/path/skill-contract-reviewer/scripts/check_skill.py" \
  "/absolute/workspace/path/agent-skills-first-run/my-first-skill"
```

成功的结果具有三个特征:

> 成功的结果具有三个特征:

1. 宿主发现了`skill-contract-reviewer`通过名字.
  中文翻译:宿主按名称找到`skill-contract-reviewer`,我知道.
2. 审查员阅读包裹合同并运行其捆绑验证器.
  中文翻译:评审者 读取包契约并运行其捆绑的验证器。
3. 答案包含了没有结构错误的验证报告
   样本,加上合理的原始选择.
  中文翻译:响应包含一个无结构性错误的验证报告,以及有依据的原语选择.

执行证据还必须指定脚本路径,目标路径,
没有这些字段的流动报告不能
证明安装的伴侣脚本运行.

> 执行证据还必须写明脚本路径、目标路径、cwd、精确参数向量和退出码──缺少这些段落的流报告证明已安装的附加脚本真的运行了──

如果主机报告该技能不可用,请验证安装
目的地,重新扫描或重新启动一次,再尝试明确的请求.
改写技能描述以掩盖安装故障.

> 如果主机报告技能不可用,先验证安装目的地,重新扫描或重新启动一次,再试一次显然请求――不要依赖改写技能 描述来掩盖安装失败――

### 4. 探测器隐含选择

开始一个新的代理转换,然后进入同一个任务,

> 开一个全新的代理轮次,输入同样的任务,但不提名技能:

```text
Review <TARGET_ROOT>/my-first-skill as a reusable agent package and tell me whether its package contract is valid.
```

如果主机暴露出选定的技能,请记录是否选择
`skill-contract-reviewer`如果主机不显示路由,
显而易见的呼唤是可移植的倒退.

> 如果主持人显示出自己选择的技能,记录它是否选择了.`skill-contract-reviewer`如果主机不透露路径,把隐式选择标记为未验证.

### 5. 清理

删除仅安装的审视器捆绑:

> 只移除已安装的评论员包:

```bash
npx skills remove skill-contract-reviewer
```

选择安装过程中使用的相同主机和范围.
会议,一个明确的要求`skill-contract-reviewer`报告
没有任何可用.`my-first-skill`对于后期课程,或取消
在你完成了轨道后,

> 选择与安装时相同的宿主和范围.`skill-contract-reviewer`显然要求应报告它不可用.`my-first-skill`给后续课程,或在学完本轨 后删掉实验目录──

## 问题 问题引入

> **【中文解读】**两种方向的错误都存在:把工作流塞进一个提示词没有稳定身份没有发现规则没有资源边界没有可测试的包装形态;或者反过来把所有可复制指令都当成技能仓库约定确定性自动化外部工具事件,委托代理各类不同的问题,全部塞进 SKILL.md只能得到一个"看起来可移植的目录 实际依赖主机未被文档化行为".第一项工程任务是分类:先决定工件是什么,再决定如何包装.

假设你的团队有一个可靠的发布工作流程. 它会找到合并的变化,检查迁移说明,更新变更日志,运行一个包装命令,并生成一个审查检查列表.

> 假设你的团队有一个可靠的发布工作流:找合并变更;检查迁移说明;更新变更记录;运行打包命令;产出审查清单.

通过将工作流放到一个提示中,它可以轻松粘贴并难以操作.提示没有稳定的身份,没有发现规则,没有资源界限,没有可测试的包装形状,并且没有答案:谁可以调用它?模型应该何时选择它?它可以运行哪些脚本?哪些文件是可信的?当环境被压缩时,什么存活?

> 把这篇工作流入一个提示词,好粘贴但运行难.提示词没有稳定身份,没有发现规则,没有资源边界,没有可测试的包装形态,也没有回答基本问题:谁可以调用它?模型应该在什么时候选择它?它可以运行的脚本?哪些文件是可信的?下面的文件被压缩后,什么能活下来?

对于这些问题来说,我们必须要把它们放在一个单独的位置,并把它们放在一个单独的位置.`SKILL.md`根据一个主机的无证行为,

> 相反,错误是把每条可复制指令都当成技能――仓库约定,确定性自动化,外部工具,事件和委托代理 解决了不同的问题――把它们全部塞进`SKILL.md`实际上,它依赖于某个宿主未被记录的行为目录.

首先要做的是分类,然后决定如何包装.

> 首先决定工件是什么,然后再决定如何包装.

## 概念的核心概念

### 技能编码程序知识

代理技能是一个目录,其入口点是`SKILL.md`输入文件包含YAML前列,然后是Markdown指令.目录也可以包含参考,脚本和资产.

> 代理技能是一个`SKILL.md`为入口目录.入口文件包含YAML的前面材料和随后的标记指令.目录也可以包含参考文件,脚本和资产.

```figure
skill-package-anatomy
```

文件是可部署的单元.`SKILL.md`没有引用的包装是破碎的,即使它的前面材料被解析.

> 可部署单元是目录,而不是仅仅是标记文件.`SKILL.md`如果缺少引用的资源,即使前面的问题也能解决一个坏包.

### 周边的抽象

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

释放技能可以告诉代理人如何检查释放.一个MCP服务器可以暴露释放注册表.一个子可以禁止直接推.一个副官可以独立审计候选人.这些件是由因为它们保持不同的责任组成.

> 一个发布技能可以告诉代理人如何检查发布;一个MCP服务器可以暴露发布注册表;一个子可以禁止直接推;一个子公司可以独立审计候选版本.

### 技能是两个不同的概念.

> **【中文解读】**"技能"一词指两个不同的事物:研究系统中它指学习的程序,成功轨迹或策略片段 经理在探索中创造,按任务相似度检查,执行并按反修订 (Phase 14 · 10 构建这种终身学习库);而本轨道的经理技能是一个由创建的包,有声明文件系统协议,目录元数据,渐进披露,运行时介中的调用和主管控制工具.

研究系统有时会称学习的程序,成功的轨迹或环境特定的政策碎片为技能. 代理人在探索过程中可以创建这些文物,根据任务相似性检索它们,执行它们,并根据反修改图书馆.

> 研究系统有时将学习的程序,成功轨迹或环境特定策略的段落称为技能. 代理可以在探索中创建这些工件,按任务检查相似性检查,执行它们,并按反修改库.

这部小轨道中的代理技能不同.它是一个由作者编制的包,包含声明的文件系统合同,目录元数据,渐进披露,运行时间调用调用和主机控制的工具.它可以由代理生成或改进,但学习不需要格式.

> 本小轨道中,代理技能不一样. 它是一个由作者创建的包装,带着声明文件系统契约,目录元数据,渐进披露,运行中介调用和主机控制的工具. 它可以由代理生成或改进,但这个格式本身不需要学习.

| Dimension | Agent Skill package | Learned skill library |
|---|---|---|
| Primary unit | `SKILL.md` directory | Program, policy, trajectory, or memory record |
| Creation | Authored, generated, or curated | Usually discovered from environment experience |
| Selection | Catalog description plus runtime policy | Retrieval or policy over task state |
| Execution | Model follows instructions and calls host tools | Environment runs a stored behavior or code artifact |
| Portability | Package contract can cross compatible hosts | Often tied to one environment and action space |
| Evaluation | Routing, artifact, safety, and host compatibility | Reward, success rate, transfer, and library growth |

两种想法都包含可重复使用的能力.

> 两种想法都在打包可复用能力中.

### 移动核心

> **【中文解读】**可移植核心极小:`name`(稳定标识符,必须满足命名规则和与父目录名称一致) 和 `description`两项前面内容 字段是规范必填;`license`,我知道.`compatibility`,我知道.`metadata`是核心可选字段,`allowed-tools`属实验性、宿主支持不一―― 标注down 正文载有操作指令工作流、决策点、失败行为和通往支资源的直通路径――

代理技能规范需要两个前面材料领域:

> 代理技能 规范要求两个主题 字段:

```yaml
---
name: release-readiness
description: Inspect a release candidate when the user asks whether a version is ready to publish.
---
```

`name`必须符合规范的命名规则,并与母目录相匹配. `description`需要说明技能是什么,什么时候适用.

> `name`是稳定标识符,必须满足规范的命名规则并与父目录名称一致.`description`文档也是路由数据,应说明技能做什么,何时适用.

可移植的可选字段是:

> 可移植的可选字段有:

| Field | Purpose | Portability note |
|---|---|---|
| `license` | State the terms for the package | Core specification |
| `compatibility` | State environmental requirements | Core specification |
| `metadata` | Carry string-valued extension data | Core specification |
| `allowed-tools` | Suggest pre-approved tools | Experimental; host support varies |

马克唐机构拥有操作说明. 它应该定义工作流程,决策点,失败行为,以及直接通向支持资源的路径.

> 标记下载操作指令. 它应定义工作流,决策点,失败行为和通往支资源的直通路径.

```markdown
# Release readiness

Use this workflow for a release candidate, not for ordinary development builds.

1. Read `references/release-policy.md`.
2. Run `python3 scripts/inspect_release.py --format json`.
3. Stop if the report contains a blocking failure.
4. Produce the checklist from `assets/release-checklist.md`.
5. Ask for approval before any publish or tag action.
```

### 运行时间扩展是第二层

有些主机可以接受额外的前置或伴侣配置.这些字段可能是有用的,但它们不自动移植.

> 一些主机接受额外的前置或伴生配置.

| Behavior | Example host extension | Portable core? |
|---|---|:---:|
| Hide a skill from model routing while keeping direct user invocation | `disable-model-invocation` | No |
| Hide a skill from the user's command menu while allowing model routing | `user-invocable` | No |
| Show argument help in a command menu | `argument-hint` | No |
| Run the skill in delegated context | `context`, `agent` | No |
| Pin model or reasoning settings | `model`, `effort` | No |
| Register lifecycle automation | `hooks` | No |
| Disable implicit invocation in Codex | `agents/openai.yaml` policy | No |

处理每个扩展程序都像一个适配器. 保持核心工作流程没有它有效,记录下后退,并测试使用它的主机. 运行时间可能会忽视一个未知的字段,拒绝它,或保存它,而不实施行为.

> 把每个扩展作为适应器:没有它的核心工作流也必须保持有效,记录回退方式,并测试消费它的宿主――运行时可能忽略未知字段、拒绝它,或者保留它,但不实现对应行为――

### 前列是可执行的元数据

在技能体被读取之前,元数据改变系统行为.

> 据了解,在学习之前,

- 一个形的`name`发现可能会失败.
  中文翻译:格式错误的`name`让我发现失败.
- 的`description`能引导错误的请求.
  中文翻译:含糊的`description`由于错误的请求.
- 只有人类的旗可以从模型的目录中删除技能.
  中文翻译:一个"仅人类"标志能把技能从模型目录移除.
- 工具权限可以改变主机是否要求许可.
  中文翻译:工具许可能改变宿主是否请求授权──
- 文本设置可以将执行转移到单独的代理会议.
  中文翻译:上下文设置能把执行移入独立的代理会话.

检查前面物质,如配置代码,验证它,版本它,并包括其行为在评估.

> 像审查配置代码一样审查前线:验证它、给它做版本管理,并将其行为纳入评测.

### 技能生命周期

> **【中文解读】**八阶段生命周期:发现(在配置位置找候选包)→ 验证(目录发布前拒绝形或不安全的包)→ 编目(只暴露精简的名称+描述)→ 选择(判断相关性)→ 激活(把正文载入模型可见上下文)→ 披露(仅需要某分支时才读参考/资产)→ 执行(在宿主权限和隔离规则下使用主工具)→ 验证宿宿(独立于模型的声明检查产品) │把这些阶段压会导致误解智力模型:被发现的技能不等于已被发现的技能;已激活的技能不等于被授权做它的描述;被允许的工具调用不等于正确的结果.

```figure
skill-runtime-lifecycle
```

每个箭头都是一个有自己的失败模式的边界.

> 每个箭头都是带有自己的故障模式的边界.

1. **Discovery**在配置位置找到可能的包裹.
  翻译: 中文**发现**在配置位置寻找可能的包.
2. **Validation**在目录发布前拒绝错误的或不安全的包装.
  翻译: 中文**验证**在目录发布之前拒绝形或不安全的包.
3. **Cataloging**揭露了一个紧的`name`其他`description`没有完整的包裹.
  翻译: 中文**编目**简单的说明`name`和 `description`没有完整包.
4. **Selection**决定技能是否相关.
  翻译: 中文**选择**决定是否相关的技能.
5. **Activation**载体进入可见模型的环境中.
  翻译: 中文**激活**把正文载入可见的模型上下文.
6. **Disclosure**只有分支机构要求阅读参考或资产.
  翻译: 中文**披露**只有在某个分支需要时才读取参考或资产.
7. **Execution**使用主机工具,根据主机的许可和隔离规则.
  翻译: 中文**执行**在主权与隔离规则下使用主工具.
8. **Verification**检查生产的文物,不论模型的要求如何.
  翻译: 中文**验证**独立于模型的声明检查产生的工件――

由于这些阶段的崩导致了不良的心理模型.一个发现的技能是不活跃的.一个活跃的技能不被授权做它描述的一切.一个允许的工具呼叫不是证明结果是正确的.

> 压力这些阶段会造成糟糕的心理模型:被发现的技能没有被激活;激活的技能没有授权做它描述的一切;被允许的工具调用不能证明结果是正确的.

### 技能和工具是直角的

技术人员回答:"该应用程序可以要求哪些功能,以及它们的方案是什么?"一个技能回答",代理应该如何处理这个类型的任务?"

> 技术 答"应如何完成此类任务"――

```figure
skill-tool-orthogonality
```

技能可能会命名工具,但主机拥有实际能力登记册.如果工具不存在,技能应该明确表示倒退或失败.它永远不应该意味着命名能力创造它.

> 技能可以点名某种工具,但真正的能力注册表归宿主所有.若工具缺席,技能应声明退回或简直失败,绝不应暗示"点名一个能力就创造了它".

### 技能和存储指令是不同的范围

库存指令描述了你已经处于的环境:命令,会议,生成的文件和边界.一个技能为许多库存中可能发生的任务提供可重复使用的程序.

> 仓库说明描述你已经在环境中:命令,约定,生成文件和边界;技能为一个可能跨许多仓库出现的任务提供可复用流程.

当这两种应用时,活跃用户请求和存储器规则限制了技能.一个通用的重构技能不能取代禁止编辑生成文件的存储器规则.

> 当两者同时适用时,当前用户请求和仓库规则限制了技能――一个通用重构技能不应超过"禁止编辑生成文件"的仓库规则――

### 技能不互相进口

一个技能可以引导代理调用另一个,但这不是语言级进口.第二个技能仍然通过运行时间发现,资格,激活,权限和文本处理.

> 一个技能可以引导代理调用另一个技能,但这不是语言级的进口.

写出跨技能依赖性作为可观察的工作流边缘:

> 跨技能,依赖于可观察的工作流程:

```markdown
After producing the candidate changelog, invoke the `release-risk-review` skill.
Pass the candidate path and require a blocking or non-blocking verdict.
If that skill is unavailable, stop and report the missing dependency.
```

这使得依赖性可测试,并给主机执行政策的机会.

> 这让依赖变得可测试,也给主机一个执行策略的机会.

## 动手构建

> **【中文解读】** `code/main.py`实现一个小型面向规范的验证器和一个原语选择器,全程只使用标准库让每个条例可见.`parse_frontmatter`,我知道.`validate_skill_text`,我知道.`ValidationIssue`现在,我们要去.`SkillReport`(结构性证据而不是一个不透明的布尔值) 和`FrontmatterSyntaxError`;选择器提供 `TaskShape`与`select_primitives`试验顺序有讲究:先验证廉价的结构事实,再上层内容规则,避免一次生错淹没第一条被破坏的不变式――

`code/main.py`它们只能使用一个标准化验证器和一个选件选件器.

> `code/main.py`实现一个小型的规范面向验证器和一个工件选择器.

验证器揭示:

> 验证器曝光:

- `parse_frontmatter(text)`为了将元数据与身体分开.
  翻译: 中文`parse_frontmatter(text)`把元数据与正文分开.
- `validate_skill_text(text, directory_name, allowed_runtime_extensions=())`检查所需的字段,命名,未知的扩展,体体存在和可移植的限制.
  翻译: 中文`validate_skill_text(text, directory_name, allowed_runtime_extensions=())`检查必填字段"",命名"",未知扩展"",正文存在性和可移植限制"",
- `ValidationIssue`其他`SkillReport`返回结构化证据,而不是一个不透明的布鲁尔式.
  翻译: 中文`ValidationIssue`和 `SkillReport`回归结构化证据而不是一个不透明的布尔值.
- `FrontmatterSyntaxError`对于无法安全解释的输入.
  翻译: 中文`FrontmatterSyntaxError`针对无法安全解释的输入.

选择者会发现`TaskShape`其他`select_primitives(task)`它将任务的需求映射到普通代码,存储器指令,技能,,子器或MCP工具.

> 选择器暴露`TaskShape`和 `select_primitives(task)`△它将任务的需求映射到普通代码,仓库说明,技能,,子器或MCP工具.

运行实验室:

> 运行实验:

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/22-skills-and-agent-sdks
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

这个命令区块需要一个本地克隆,必须从内部开始.
这种克隆是如此`git rev-parse --show-toplevel`它们可以解决存储库根.

> 这块命令需要本地克隆,必须从克隆中的任何位置开始,`git rev-parse --show-toplevel`才能解析出仓库根目录.

演示程序将JSON打印为一个有效的便携技能,一个扩展的主机技能,一个不有效的包,以及几个任务形状决策.检查问题代码.一个包验证器应该解释如何修复一个文物,而不代表作者猜测.

> 展示一个合法的可移植技能,一个带宿主扩展技能,一个非法包和一些任务形态决策印制JSON――研究这些问题 代码:包验证器应解释如何修复工件,而不是替代作者盲猜――

### 验证命令的问题

在更深入的内容规则之前验证廉价结构性事实:

> 首先验证廉价的结构事实,再上更深入的内容规则:

```figure
skill-validation-order
```

由于此次测试的结果,

> 这种顺序防止下生错误淹没第一条被破坏的不变式.

## 实际使用

> **【中文解读】**写技能 之前先填一张决策卡:需要跨多步的可复用模型判断?→技能──事件每次触发都必须执行?→或应用代码──需要带类型输入的外部能力?→工具或MCP 服务器──需要隔离的上下文/状态/所有权?→ 库存说明──一次交互就够了?→提示词──很多生产工作流会不停一行使用这个卡,防止一个工件假装提供所有属性──

在写出技能之前,填写下面的决定卡:

> 写技能 之前,先填写这个决策卡:

| Question | If yes | Likely primitive |
|---|---|---|
| Does this need reusable model judgment across several steps? | The procedure is stable but decisions vary | Skill |
| Must this happen every time an event fires? | Missing one execution is unacceptable | Hook or application code |
| Does the model need an external capability with typed inputs? | The operation lives outside model context | Tool or MCP server |
| Does the work need isolated context, state, or ownership? | A separate worker returns a bounded result | Subagent |
| Is this guidance specific to one repository? | It describes local commands and constraints | Repository instructions |
| Is one interaction enough? | No package lifecycle is needed | Prompt |

许多生产工作流程使用多行,卡片阻止一个文物假装提供所有属性.

> 许多生产工作流会使用不止一行.

## 运送它.

这一课产生了`skill-contract-reviewer`包装下面`outputs/`它包含:

> 本课产出发 `outputs/`下一个`skill-contract-reviewer`包──它包含:

- 一个便携式`SKILL.md`审查拟议的技能包;
  中文翻译:一个审查候选人技能包的可移植`SKILL.md`其他
- 移动合同和原始选择的参考检查列表;
  中文翻译:针对可移植契约与原语选择的参考清单;
- 确定性验证脚本;
  中文翻译:一个确定性验证脚本;
- 任务形状装置,包括提示,技能,工具,,普通代码和副标.
  中文翻译:覆盖提示词、技能、工具、克、普通代码和子代码的任务形态具──

装备全部包,不仅仅是其输入文件:

> 装完整包,而不仅仅是入口文件:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/install_skills.py /tmp/aiefs-skills --phase 13 --type skill
```

课程安装器报告了每一个复制的13期技能,并写
`/tmp/aiefs-skills/manifest.json`. 这种清洁目的地检查包装形状;
在上面的首次成功循环检查了实在的主机中发现和调用.

> 课程安装器报告每一副本的13期技能并写入`/tmp/aiefs-skills/manifest.json` 净的目的地检查包装形态;上述10分钟的首次胜利循环检查真实宿主中发现和调用

下面的课程深化了生命周期的每个阶段.第24课程建立了发现和逐步披露.第25课程建立了调用政策和路由.第26课程将权限与沙盒分开.第27课程将整个包装变成了一个评估的释放文物.

> 后续课程逐步深化生命周期各阶段:第24课 构建发现和渐进的披露;第25课 构建调整策略和路由;第26课 权限与沙箱分开;第27课 将整个包装变成经评测的发布工件──

## 练习题

1. 通过使用 `TaskShape`捍卫每一个你选择多个原始的案件.
   中文翻译:用`TaskShape`分类你在团队中的五条工作流.

2. 添加一个500字符的边界测试证明`compatibility`值通过,501字符值失败为规格错误.
   中文翻译:添加边界测试,证明500字符的`compatibility`通过 字符的值以规范错误失败.

3. 添加一个运行时间扩展到允许列表. 写一个测试证明相同的文件仍然可以区分于只可移植的技能.
   中文翻译:向允许列表添加一个运行时扩展――写一个测试证明同一文件仍然可以与纯可移植技能区分开――

4. 分成400行提示`SKILL.md`让每个文件都负责一个类型的信息.
   中文翻译:把一个400 行的提示词拆成`SKILL.md`、一个参考文件、一个脚本协议和一个输出模板――让每个文件只负责一个类信息――

5. 设计一个不存在的MCP工具的技能失败响应. 不要默默地用更广泛的权限替代工具.
   中文翻译:为引用不可用的MCP工具的技能设计失败响应――不要替换为权限更宽的工具――

6. 检查现有技能,并将每个句子标记为路由,程序,政策,参考指针或输出合同.
   中文翻译:审查现成的技能,把每个句子标记为路由,流程,策略,参考指针或输出契约――移走一切不属于内容――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| Agent skill | "A saved prompt" | A discoverable directory of procedural instructions and optional resources |
| Portable core | "Fields every runtime shares" | The contract defined by the Agent Skills specification |
| Runtime extension | "Extra frontmatter" | Host-specific configuration whose behavior requires a compatible adapter |
| Activation | "The skill ran" | The skill body entered model-visible context; execution may come later |
| Skill dependency | "Import another skill" | A runtime-mediated invocation edge with availability and policy checks |
| Tool contract | "A function schema" | Inputs, outputs, permissions, side effects, errors, and evidence for a capability |

## 继续阅读 继续阅读

- [Agent Skills specification](https://agentskills.io/specification)对于可移植目录和前置材料合同.
  中文翻译:代理技能 规范可移植目录与前面材料 契约的出处
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)对于范围,指令和资源组织.
  中文翻译:代理技能 最佳实践范围、指令与资源组织
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)对于目前的Codex发现和呼唤行为.
  中文翻译:OpenAI 构建技能 编辑 当前的发现和调用行为
- [Claude Code skills](https://code.claude.com/docs/en/skills)对于一个运行时间的调用,参数,工具和委托文本扩展.
  中文翻译:Claude 编码技能一个运行时调用,参数,工具与委托上下文扩展
