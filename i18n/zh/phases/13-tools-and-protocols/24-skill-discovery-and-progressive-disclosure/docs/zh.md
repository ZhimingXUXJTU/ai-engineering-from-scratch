# 技能发现和进步披露

> 技能在被装载之前就会变得有用.它的名称和描述在目录中获得位置;其更深层次的文件只有当任务达到它们时才获得了语境.

> **【中文解读】**技能在正文上传之前已经开始发挥作用:名称和描述先赢得了它在目录中一个位置;更深层次的文件只有当任务真正走到那一步时才进入下文. 本课解决两个工程问题:发现 (发现) 发现 (发现) 不是简单的递归文件搜索 处理作用域,试验,同名冲突和目录发布;渐进披露 (逐步披露) 必须是有意的分层加载,否则会退回为"渐进困惑" (渐进困惑).

> **【拓展：Agent Skills 子系列→本课位置】**本课是代理技能子系列的第二课程. 第13期·22-27期. 第22课定义了技能包的可移植契约.

>  **【前置】**学本课前请先掌握:第13阶段 · 22(代理技能:可移植契约与运行时边界) SKILL.md 的包结构(前面材料 + 正文 +参考文献/脚本/资产),以及"技能是上下文而不是工具"的边界。

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 22 (Agent Skills: Portable Contract and Runtime Boundary) | **前置知识:** Phase 13 · 22（Agent Skills：可移植契约与运行时边界）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## 学习目标

- 建立一个文件系统发现管道,分开范围,验证,碰撞政策和目录发布.
  中文翻译:构建一条文件系统发现流水线,把作用域,校验,冲突策略和目录发布分开处理.
- 解释三个披露水平:目录元数据,活跃指令和具体任务资源.
  中文翻译:解释三级披露:目录 元数据、活跃指令、任务特定资源──
- 设计参考,使代理人可以直接到达所需细节,而不需要装载整个包装.
  中文翻译:设计引用结构,使代理能直接达到所需细节而无需加载整个包.
- 预算目录空间独立于活跃技能背景.
  中文翻译:为目录 空间与活跃技能上下文分别做预算──
- 拒绝路径穿越和符号链接逃脱,当一个技能读取自己的资源.
  中文翻译:在技能读取自身资源时拒绝路径穿越 (穿越) 和符号链接 (逃逸).

## 问题 问题引入

你的代理人有200个技能,`SKILL.md`访问程序的内容将会被删除,并且将其运行到无关程序中.

> 你的代理人安装了200个技能.`SKILL.md`、参考文件、脚本和模板,将当前任务淹没在不相关的流程中;什么都不加载,又迫使用户记住精确的文件系统路径.

常见的妥协是目录:向模型展示每个合格技能的紧身份和路由描述,然后在选择后才加载整个机器. 这会产生两个新的工程问题.

> 通常的折中方案是一个目录:先向模型展示每个合格技能的紧身份和路由描述,然后在选中加载完整正文.

首先,发现不仅仅是复制文件搜索.技能可以存在于项目,用户,管理员,插件或内置范围.两个包可以共享一个名称.一个符号链接可以指向值得信赖的根外.一个错误的包可能耗尽目录空间或变得无法调用.

> 第一,发现不仅仅是递归文件搜索.技能可以存在于项目,用户,管理员,插件或内置作用域.两个包可能具有同名;一个符号链接可能指向接收根之外;一个形包可能占据了目录空间,或者变得无法调用.

另一方面,逐步披露可能会导致逐步的混乱.`SKILL.md`如果每个指南指向了另外三个文件,加载就会变成一个无限的图形行程.

> 第二,渐进的披露可能变成渐进的困惑.`SKILL.md`如果每一条指南又指向其他三份文件,则载荷就变成无限的图文遍历.

良好的运行时间使发现确定性,

> 很好的运行时,让发现是确定性的,

## 概念的核心概念

> **【中文解读】**本节把"发现"建模成一个编译器流水线:文件系统是源输入,绝不把原始路径直接发布给模型.要点有五:(1) 作用域(范围) 是运行时策略可移植规范只定义技能包本身,不定义统一安装路径或优先级顺序,主持人必须明确声明搜索哪些根目录、谁有写权;(2) 同名冲突冲突冲突) 需要身份证范围和来源的身份证 之外的身份证 范围和来源需要进入目录 目录 条分;(3) 披露三级的目录 元数据 → 活跃指令 支资源),各级不同目的;

### 发现是一个编译器流水线.

处理文件系统作为源输入.不要直接发布原始路径到模型中.

> 把文件系统作为输入源. 不要直接将原始路径发布给模型.

```figure
skill-discovery-pipeline
```

每个阶段都应该产生结构化数据和结构性故障.

- 它们的根源是什么?
- 谁的候选人被发现?
- 哪些候选人被拒绝,为什么?
- 哪个包赢得了碰撞?
- 由于预算问题,哪些目录被缩短或遗漏?

没有这些证据, "模型没有使用我的技能"几乎不可能诊断.

> 没有这些证据,"模型没有我的技能"几乎无法诊断. 发现日志应回答:搜索了哪些根目录,找到哪些候选人,拒绝哪些候选人和原因,冲突中谁胜出,哪些目录因预算被缩短或省略.

### 运行时间的作用域是运行时间的策略

移动规格定义了技能包,而不是一个通用的安装路径或优先级顺序. 主机决定它在哪里搜索.

> 可移植规范是技能包而不是统一的安装路径或优先级序列.

总体运行时间可能使用以下范围:

| Scope | Example root | Intended ownership |
|---|---|---|
| Workspace | `<repo>/.agents/skills/` | Project maintainers |
| User | `<user-data>/skills/` | One developer |
| Administrator | `<system>/skills/` | Machine or organization policy |
| Plugin | A signed plugin bundle | Plugin publisher and installer |
| Built-in | Runtime package | Runtime vendor |

截至2026年8月,Codex文件将项目发现`$CWD/.agents/skills`通过祖先目录到库根,加上用户,管理员和内置位置.它支持交互式技能目录.重复名称可能都会出现而不是合并.这些是Codex行为,而不是要求的`SKILL.md`检查电流[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)在编写适配器时.

任何类目录名字都不能先决地出现. 声明为政策并测试它.`Scope`所以同一个候选人总是以同样的方式解决.

> 永远不要从目录中设想优先级.`Scope`一个显而易见的整数排名,使同一批候选人总是解析出相同的结果――表中五种作用域:Workspace=项目维护者、User=单个开发者、Administrator=机器或组织策略、Plugin=插件发布者和安装者、Built-in=运行时厂商──)

### 碰撞需要一个身份`name`需要身份证,不需要名字.

两个名为的包裹`release-readiness`一个可能是工作空间过失,另一个可能是用户默认.因此,目录入口至少需要:

```json
{
  "name": "release-readiness",
  "description": "Inspect a release candidate for this repository.",
  "scope": "workspace",
  "source": "/repo/.agents/skills/release-readiness",
  "selected": true
}
```

共同的碰撞政策包括:

| Policy | Benefit | Risk |
|---|---|---|
| Keep every candidate | Nothing is hidden | The model sees ambiguous names |
| Highest-precedence scope wins | Simple invocation | A local package can shadow a trusted one |
| Reject duplicates | No silent shadowing | Legitimate overrides stop working |
| Qualify names by source | Explicit identity | User-facing names become longer |

选择一个主机的政策.即使在模型目录中没有被拒绝或被置的候选人,也可以在诊断中保留.

> 为主机选择一个策略即可.即便被拒绝或被遮蔽的候选人不进入模型目录,也必须将它们保留在诊断信息里.

### 现在,我们要做什么?

机关的关键是每个层次都有不同的目的.

> 代理技能规范描述分阶段加载.

> **【中文解读】**三级披露各自解决不同的问题:级别1号(目录元数据) 解决"模型能否把它与邻居区分开",规范估计每条约100代币,描述要写两个分句能力是什么+什么情况触发;级别2号(活跃指令) 解决"激活后模型能否正确开工",规范建议SKILL.md 保持500 行内这是设计信号不是填满的标志,主线流程不能缩短入口文件而转载引用;级别3支资源) 引用 供阅读脚本 供确定性计算、资产 是模板而不是指令 这些字母是约定不是魔法能力,宿主仍然需要文件访问工具和执行工具.

```figure
skill-disclosure-levels
```

#### 级别1:目录元数据

模型需要足够的信息来区分技能与邻居.规格估计每一条目录的约100个代币,但实际的序列化和代币化属于主机.

有用的描述有两个条款:

```yaml
description: Validate a release candidate and produce a readiness report. Use when the user asks whether a version, tag, or package is ready to publish.
```

第一个条款规定了能力. 第二条规定了触发界限. 第25课程评估了这个界限,通过积极和接近错误的提示.

> 第一个分句陈述能力,第二个分句陈述触发边界―― 第25课 会用正向与近似未命中 (近-错过) 快速来评测这个边界――

#### 活动指令2级.

激活后,该机体应作为一个地图和程序.`SKILL.md`这是一个设计信号,而不是一个填充目标.

> 激活后,正文应同时充满一张地图和一套流程.`SKILL.md`保持在500行内.这是一个设计信号,不是填写标志.

身体应包含:

- 任务界限;
- 默认工作流程;
- 部门条件;
- 直接引用更深层次的文件;
- 工具和脚本合同;
- 失败和停止行为;
- 预期产量和其验证.

仅仅是为了使输入文件短暂,不要将中央工作流转换为参考.

> 为了缩短输入文件, 让核心流程转入引用.

#### 支持资源的第三级.

引用提供散文或数据.脚本提供确定性计算.资产被复制,填写或转化为交付物而不是作为说明.

> 引用) 提供文字或数据;脚本) 提供确定性计算;资产) 资产) 被复制,填充或转换为交付物,而不是被当作命令.

| Directory | Model reads it? | Model executes it? | Typical content |
|---|:---:|:---:|---|
| `references/` | Yes, when needed | No | schemas, policies, domain guides |
| `scripts/` | May inspect it | Through a permitted tool | validators, converters, collectors |
| `assets/` | Only if useful | No | templates, fixtures, images, starter files |

它们是规范,而不是魔术功能.

> 这些名字是约定,不是魔法能力.

### 专业引用超过专题排放. 分支特定引用胜过专题大杂.

写入文件作为决策地图:

```markdown
## Choose the path

- For a Python package, read `references/python-release.md`.
- For a container image, read `references/container-release.md`.
- For a documentation-only release, read `references/docs-release.md`.
- If the release combines artifact types, read only the guides for those artifacts.
```

这使得每个引用都能观察到的负载条件.`references/`没有.

> 这让每个引用都有一个可观察的加载条件.`references/`了解更多"则没有.

官方指南建议直接链接到`SKILL.md`一次跳跃使得可访问性可测试,

> 保持引用图浅──官方指南建议从 `SKILL.md`直接链接、避免深链──一跳(一跳) 让可达性可测试,也降低"必要的约束从未进入上下文"的概率──

```figure
skill-reference-map
```

### 产品表预算和活动背景是不同的预算.

让我们`c_i`作为一个系列化目录的技能成本`i`现在`B_c`产品表预算`b_j`活动体成本,`r_k`实际上,资源的装载量.

```text
catalog_cost = sum(c_i for every published skill)
active_cost = sum(b_j for every activated skill) + sum(r_k for every disclosed resource)
```

减少一个预算不会自动减少另一个.简短的描述可以节省目录空间,而一个激活的900行体仍然压倒任务.将体积分为参考可以减少活动成本,只有当运行时间和说明实际避免加载无关的分支时.

> 削减一笔预算不会自动削减另一笔. 短描述能省份目录空间,但在激活后的900 行正文照样淹没任务;把正文分解到引用时,只有当运行时和指示确实避免加载无关分支时,才能真正降低活跃成本.

目前,Codex将初步技能列表的预算为
设置一个窗口,当背景窗口大小已知.
只有当该尺寸不清楚时,只有当该尺寸不清楚时;它不是第二个盖子,结合
如果目录超过适用的预算,
描述可能会缩短或遗漏.
编码政策,不是代理技能标准的属性.

> 目前已知上下文窗口大小时,把初始技能列表的预算定为窗口的2%;8,000 字符只是大小未知的时代的回归值,不是与2% 叠加的第二道上限.

### 资源路径是一个信任边界.

> **【中文解读】**技能只应读取自己包装中的文件,而字面字符串前检查是不够的`references/../../../../.ssh/config`实际做法:用文件系统语义解析包根目录和候选路径,绝对拒绝输入路径,验证解析后的候选人仍在解析后的根底下;符号链接是否允许在发现之前决定,允许每次校验解析后的目标.

技能只需要阅读包装中的文件.

```text
references/../../../../.ssh/config
references/external-link -> /private/company-secrets
```

通过文件系统语义来解决包根和候选,拒绝绝绝对输入,并验证已解决的候选仍然存在于已解决的根下. 确定是否允许在发现之前符号链接. 如果允许,每次都检查已解决的目标.

> 用文件系统语义解析包根目录和候选路径,绝对拒绝输入路径,并验证解析后的候选人仍然在解析后的根底下──是否允许符号链接在发现之前决定;如果允许,每次检查解析后的目标──

```figure
skill-resource-containment
```

路径封锁不会建立内容信任.一个有效的包装引用仍然可能包含恶意指令. 第26课处理这种威胁.

> 路径包含不等于内容可信. 法律包内引用仍可能包含恶意指令.

### 载荷必须可观看.

记录披露事件,没有记录秘密:

```json
{
  "event": "skill.resource.loaded",
  "skill": "release-readiness",
  "resource": "references/python-release.md",
  "reason": "candidate contains pyproject.toml",
  "bytes": 2840
}
```

原因是,它将文本选择转化为可审查的证据.

> 原因 字段将一次上下文选择变成可审核的证据,也可以帮助确定让代理"防止万一"加载每个文件的指令.

## 建立它,实现它.

> **【中文解读】** `code/main.py`构建一个确定性发现与披露引擎.`Scope`(来源与优先级元数据)`SkillCandidate`文件系统候选人`discover_scope`没有任何其他方法.`resolve_collisions`(应用一条已声明的冲突策略)`CatalogEntry`其他`build_catalog`(发布有界元数据)`CatalogBudget`(核算序列化条目,而不是假象字符数等于通用代币数)`load_skill_body`(第二级激活)`validate_reference`(路径包含校验)`load_reference`(有界的3级读取)  Demo 会创建临时项目与用户作用域插入一个冲突 根据小预算构建目录 激活一个技能,并分别尝试一次合法引用读取和一次穿越逃逸 不安装任何永久文件

`code/main.py`建立一个确定性发现和披露引擎.

发现表面包括:

- `Scope`对于源和优先级的元数据;
- `SkillCandidate`对于未经验证的文件系统候选人;
- `discover_scope(scope)`列出直接技能目录;
- `resolve_collisions(candidates, precedence)`实施一个声明的政策;
- `CatalogEntry`其他`build_catalog(...)`发布有限的元数据;
- `CatalogBudget`为了解释连续化输入,而没有假装字符是通用代币.

透露表面包括:

- `load_skill_body(entry, ...)`对于2级激活;
- `validate_reference(skill_dir, reference)`对于路径封锁;
- `load_reference(...)`对于有边界的3级读数.

运行实验室:

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

这个区块需要一个本地克隆,并解决任何存储库的根
在那个克隆内部的工作目录.

演示程序创建了临时项目和用户范围,插入了碰撞,在故意小预算下构建了目录,激活了一个技能,并尝试了有效的参考阅读和穿越逃逸.没有永久文件安装.

### 为什么发现是浅的?

`discover_scope`检查了儿童直接目录`SKILL.md`它不会反复治疗每一个子.`SKILL.md`作为单独的包装,从而保护包装边界,避免在安装的技能内意外发布示例或装置.

> `discover_scope`查看直播目录中的`SKILL.md`没有把每个嵌套`SKILL.md`归归地作为独立包. 这保持包边界,避免意外发布已安装技能内部的示例或固定.

### 为什么实验室不解析任意的YAML

实验室支持其目录所需的 skalar frontmatter.生产运行时间应使用一个安全的YAML解析器,具有明确的方案,尺寸限制和禁用的自定义对象构建. "仅Stdlib"是教学约束,而不是允许默默地发明部分YAML方言.

> 实验只支持目录所需标量前材料――生产运行时应使用安全的YAML解析器显式方案、大小限制、禁用自定义对象构建――"仅标准库"是教学约束,不是默许发明一种缺陷的YAML方言――

## 让它变得更好.

应用此检查列表到任何发现适配器:

1. 列出每个配置的根和谁可以写到它.
2. 说明是否允许连接包裹.
3. 验证包名,目录名称,所需的元数据和输入体尺寸.
4. 保持内部身份的来源和范围.
5. 声明和测试复制名称行为.
6. 测量向模型发送的精确序列目录.
7. 记录为什么一个尸体或资源被装载.
8. 保持资源读数在解决包根内.
9. 当引用文件缺失时,显然失败.
10. 修改安装或政策时重建目录.

## 运送它.

这一课产生了`skill-catalog-builder`包.它扫描了明确排序的根,拒绝了链接的输入文件和名称目录不匹配,解决了跨范围的碰撞,拒绝了相同优先级的重复,并将选定的元数据纳入了声明的输入,描述和序列化字符预算.

> 本课产出发 `skill-catalog-builder`包:按明确声明的顺序扫描根目录,拒绝符号链接入口文件和名字目录不匹配,解析跨作用域冲突,拒绝等级重复项,并将选中的元数据装入已声明的条目数量"",描述长度和序列字符预算".""

它的JSON报告包含选定的输入,阴影的候选人,遗漏的输入,验证错误,优先级和预算使用.体体和参考加载仍然是分离的运行时间操作,因此目录构建器不会执行脚本或将整个包放入文本中.

> 它的JSON 报告包含选中的条目,被遮蔽的候选人,被省略的条目,校验错误,优先级和预算占用.

## 练习,练习.

1. 添加一个插件范围,将其放在用户和内置优先级之间.
2. 改变碰撞政策,从最优先级到合格名称.
3. 添加字节大小限制`load_reference`检查一个文件的极限和一个字节以上.
4. 创建两个几乎相同的描述,重新写它们,以免触发器界限重叠.
5. 添加一个包含每个引用和脚本的哈希表. 在加载之前检测修改的资源.
6. 仪器显示,报告级别1,级别2,级别3的字节分别计数.

## 关键词 关键词

> 下表左列是术语、中列是"人们常说的"",右列是"实际含义"",注意 渐进式披露不等于"加载"它是从目录到正文到分支资源的分阶段上下文进入; 路径包含不等于"在文件里等待"它在解析后的真实路径上验证──

| Term | What people say | What it actually means |
|---|---|---|
| Skill discovery | "Find every SKILL.md" | Search configured scopes, validate packages, attach provenance, and apply policy |
| Skill catalog | "The list of installed skills" | Compact model-visible routing metadata for eligible packages |
| Collision policy | "Which duplicate wins" | A declared rule for same-name candidates from different sources |
| Progressive disclosure | "Lazy loading" | Staged context admission from catalog to body to branch-specific resources |
| Reference graph | "Files linked by the skill" | The reachable resource structure and its load conditions |
| Path containment | "Stay in the folder" | Verify resolved resource targets remain inside the resolved package root |

## 继续阅读 继续阅读

- [Agent Skills specification](https://agentskills.io/specification)包装形状和逐步披露水平.
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)对于目录路由元数据.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)直接引用和输入文件大小.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)对于目前的Codex发现范围和目录限制.

> 阅读顺序建议:先阅读 代理技能 规范掌握包形状与披露分级;再使用优化描述 学写路由描述;最佳实践 讲直接引用与入口文件大小;最后查看 Codex 文档了解某个宿主当前发现作用域和目录 限量――
