# 技能调用与路由

> 要求是当局决定后续的相关性决定.一个好的描述帮助模型选择;一个好的政策决定是否允许选择.

> **【中文解读】**调用(调用) 是两个独立决策的串联:先问权限"这个角色允许请求这个技能吗",再问相关性"这个请求真的该路由到它吗"......好描述 帮模型做对第二决策,好政策决定第一个决策的答案;描述 写再好也替代不了政策――本课把"谁能调用" ((人类可见性 × 模型可选性) 和"该不应该调用" (该不应该调用) 划成两个正维交换,并给出五阶段调用生命周期的精确词汇.

> **【拓展：Agent Skills 子系列→本课位置】**本课是代理技能子系列的第三课程. 第22课 定义技能包契约, 第24课 解决发现与披露, 本课回答"技能如何被触发":显式调用(用户名) 隐式调用(模型按描述路由) 应用编排、技能间组合、评测利用 五条通道. 第26课 处理调用后权限沙箱与信任, 第27课 用近错误评测路由质量.

>  **【前置】**学本课前请先掌握:第13阶段 · 24期 技能发现与进步披露) 目录 元数据是隐式路由的输入,

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 24 (Skill Discovery and Progressive Disclosure) | **前置知识:** Phase 13 · 24（技能发现与渐进式披露）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## 学习目标

- 区分明确的用户调用,隐含的模型调用,应用调用和技能调用.
  中文翻译:区分显式用户调用"",隐式模型调用"",应用调用与技能间调用"",
- 作为独立政策尺寸,模拟人类可见性和符合性.
  中文翻译:把"人类可见性"和"模型可选性"建模为两个独立的策略维度.
- 写出具有积极触发和近错误边界的路由描述.
  中文翻译:写出带正向触发条件和近似未命中 (近-错过) 边界的路由描述.
- 单独的资格,选择,激活,结合参数,并在线索和测试中执行.
  中文翻译:在跟踪与测试中把资格、选择、激活、参数绑定与执行分开。
- 调整运行时间特定的调用字段,而不用把它们作为可移植的前置物.
  中文翻译:适配运行时专属的调用字段,不要把它们伪装成可移植的前面物质.

## 问题 问题引入

你安装一个`database-migration`技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术: 技术:

> 你安装了一个.`database-migration`技能──用户可以按名字运行它,但模型也可以看到它的描述,并且有人问一般数据库问题时选择它于是这个技能给了一个只需要解释的任务提出了方案变化──

你还补充了`user-invocable: false`其他运行时间,该领域被忽视.`disable-model-invocation: true`在理解它的运行时间里,用户仍然可以明确地使用它.

> 你加上了`user-invocable: false`预期住手动运行; 在另一个运行时,这个字段被直接忽略.`disable-model-invocation: true`预期技能完全消失;在理解它的运行时,用户仍然可以显然调用它.

应用程序可以预装它,以及它内部的工具可以执行"是单独的事实.一个单个布鲁尔式叫做`invocable`没有办法表达它们.

> 错不在字段名,错在心智模型――"用户能看到它"",模型能选中它"",应用能预载它"",它内部的工具能执行"是四个独立的事实,一个叫`invocable`它们的价值表达不了.

路由模式有第二种失败模式.如果描述不清楚,几个技能就会变得可信.如果描述充满关键词,无关任务会触发它们.目录是一个概率界面:足够紧,足够具体的路由.

> 路由还有第二种失败模式:描述含糊,几个技能都显得合理;描述塞满关键词,无关任务也会触发;

## 概念的核心概念

> **【中文解读】**本节要点:(1) 五条通道都能启动调用生命周期人类用户、模型/自主代理、应用、另一个技能/子代理、评测利用,各有典型用途和主要风险;(2) 五阶段词汇要精确合格(政策允许) / 选择(被点名或被路由) / 激活(命令进入上下文) / 执行(开始干活) / 完成(输出通过独立成功检查),只记`skill_used=true`面对失败发生在哪个边界; 3) 人类可见 × 模型可选构成2×2矩阵; 4) 先过资格再排序相关性,否则被禁最高分会挤出法定次高分.

### 五个通道可以启动生命周期.

| Actor | Invocation shape | Typical use | Main risk |
|---|---|---|---|
| Human user | Names a skill in the UI or prompt | Deliberate workflow selection | User expects availability or authority the host does not grant |
| Model or autonomous agent | Selects a catalog entry from task context | Automatic expert procedure | False-positive routing |
| Application | Activates or preloads a skill through runtime code | Fixed product workflow | Hidden coupling to one host |
| Another skill or subagent | Requests an exact skill as a workflow dependency | Composition | Cycles, missing dependency, or context bleed |
| Evaluation harness | Activates an exact skill under a fixed scenario | Repeatable measurement | Tests the skill while accidentally bypassing the production policy under study |

移动代理技能规范定义了包.它不标准化一个通用切片命令UI,隐含路由旗,应用 API或子代码生命周期.

> 可移植的代理技能规范定义为包──它不标准化统一的斜命令 UI、隐式路由开关、应用API或子代理 生命周期──

### 调用五个阶段

```figure
skill-invocation-stages
```

准确使用这些词:

- **Eligible**政策允许这个演员要求技能.
- **Selected**意思是用户命名或路由器认为它有意义.
- **Activated**代表其指示进入工作环境.
- **Executing**代表根据这些指示开始模拟或工具工作.
- **Completed**产量已通过独立的成功检查.

只有记录的痕迹`skill_used=true`隐藏了失败发生的地方的边界.

> 只有记录`skill_used=true`失败发生在哪个边界.

> **【中文解读】**这五个词是调用生命周期的"精确坐标":受理由政策决定"",被人或路由器决定"",被激活 是上下文事件"",执行 是执行事件"",完成要依赖独立的成功检查――评测和调试时先问"卡在哪个阶段",比统说"技能没有生效"有用得多――

### 人类调用和模型调用构成2×2矩阵

| Human can invoke | Model can invoke | Mode | Suitable examples |
|:---:|:---:|---|---|
| Yes | Yes | Shared | Code explanation, test planning, documentation review |
| Yes | No | Human-only | Publish preparation, billing export, destructive cleanup plan |
| No | Yes | Model-only | Internal style guide, domain reference, automatic support procedure |
| No | No | Disabled or application-only | Staged rollout, deprecated package, programmatic preload |

矩阵是一个政策模型,而不是标准的YAML.

> 这个矩阵是一个策略模型,不是标准的.

一个当前的主机使用`disable-model-invocation: true`对于只使用人为排列的`user-invocable: false`默认的是两个.另一个主机使用`agents/openai.yaml`随着`allow_implicit_invocation: false`它们是运行时间适配器,未知的主机可能会忽略它们.

> 一个现行宿主使用`disable-model-invocation: true`为了表达"只为人类"行、用`user-invocable: false`表达"仅模型"行,默认两者皆可;另一个主机使用 `agents/openai.yaml`的`allow_implicit_invocation: false`保持显式调节、关掉隐式选择──这些都是运行时适配器,未知主机可能直接忽略它们──

很难理解的细节:`user-invocable: false`它删除了定义它的主机中直接用户调用. `disable-model-invocation: true`没有意味着"技能已被禁用". 它删除了模型启动的选择,同时保持了用户的明确访问.

> 很容易混的细节很重要:`user-invocable: false`不等于"模型不能使用它"它只是在定义其主机中移动直接用户调用;`disable-model-invocation: true`也不等于"技能被禁用"它移除了发起的选择,同时保留了明显的用户访问.

### 显然,被调用为身份的先驱.

明确的呼叫直接提供身份:

```text
/release-readiness v2.4.0
```

或:

```text
release-readiness check v2.4.0 without publishing
```

目前的Codex界面文件 `/skills`对于选择和明确调用请求中简单技能名称.`/skill-name`精确的语法,菜单可见性,引用规则和变量扩展属于主机.

> 现行 代码界面用 `/skills`做选择 采用请求中的裸技能名做显然调用 Claude Code 文档记载 `/skill-name`和宿主专属参数展开――精确语法、菜单可见性、引号规则和变量展开都属于宿主――

要求仍然通过政策. 命名技能不应该绕过缺失权限,工作空间限制,批准门户或运行时间隔离.

> 显然要求仍需要策略――点名一个技能不应绕过缺失权限――工作区约束――审批门禁或运行时隔离――

### 隐式调用以描述为先

对于隐含路由,模型最初看到的是目录元数据而不是整个体.因此,描述是技能的路由界面.

> 对于隐式路径来说,模型最初看到的是目录元数据而不是完整正文.

弱势:

```yaml
description: Helps with releases.
```

超宽:

```yaml
description: Use for release, version, package, build, deploy, publish, tag, changelog, GitHub, CI, or software tasks.
```

限制:

```yaml
description: Inspect an already prepared release candidate and produce a readiness report. Use when the user asks whether a version, tag, package, or image is ready to publish; do not use for ordinary build failures or feature development.
```

限量版本包含:

1. **Capability:**检查已准备的候选人.
2. **Output:**准备报告.
3. **Positive boundary:**问是否准备好释放器件.
4. **Negative boundary:**其他地方的建筑和发展都不适用.

两个近距离技能共享词汇,而负面界限是有用的.

> 有界版本包含四个元素: 1) 能力检查已准备好候选版本; 2) 输出就绪报告; 3) 正向边界询问发布工件是否就绪; 4) 负向边界普通构建与功能开发不在范围之内.

### 路由是带弃权选项的分类

为了一个技能`s`要求`x`设想一个路由器的分数:

```text
score(s, x) = capability_match + trigger_match + context_match - exclusion_match - ambiguity_penalty
```

精确的分数可能是LLM决策而不是算术.工程原则仍然是如此:选择应该超过一个门和竞争技能.当证据很弱时,避免.

> 精确打分可以由LLM判断而不是算术完成.但工程原则不变:选中必须同时赢得过值和竞争技能;证据不足时就弃权 (弃) .

```figure
skill-routing-abstention
```

对于高影响能力,隐含路由可能不合适,即使有强烈的描述.当假阳性的成本超过自动选择的便利时,只使用人为政策.

> 对于高影响技能,即使描述很强,隐式路由也可能不合适.

### 资格必须先排名.

> **【中文解读】**顺序错误是实现最常见的错误:先给所有发现的技能打分分,选择最高分,再检查一个技能的策略被禁的最高分会住本可入选的合法次高分.正确顺序:先按要求角色和宿主适配器过资格,只对合格者打分,选择最强而过者,无人合格或分数不足弃权.示例:`incident-triage`现在,我们已经开始使用了它.`incident-review`通过 0.55 允许路由器应把`incident-review`当作最佳合格候选人,而不是选`incident-triage`、拒绝、然后停止──这个顺序还保证了策略变化不会改变相关性分数的含义:

没有得到每一个发现的技能,选择最强的比赛,然后检查一个技能的政策.一个被阻止的顶级比赛会错误地阻止一个符合条件的低分的候选人被考虑.

通过下列列列表来实现暗示路由:

1. 选器发现了要求演员和主机适配器的技能.
2. 只有合格的候选人得到分数.
3. 选择最强的符合条件的比赛,如果它清除了门和模糊性规则.
4. 如果没有候选人符合条件或没有合格得分足够强,则避免.

假设`incident-triage`评分`0.80`但它的主机扩展禁用模型调用. `incident-review`评分`0.55`路由器应该评估`incident-review`作为最好的资格候选人.`incident-triage`否认,然后停止.

根据该规则,在选择组中,有了相关性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性,可选性等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等

> 这一序列也让策略变化不仅仅是改变相关分数的含义:资格定义候选人群,相关性只给候选人群排列.

### 路由评价需要近似未定样本

积极的案例证明召回:

```json
{"prompt":"Is version 2.4.0 ready to publish?","expected":"release-readiness"}
```

显而易见的负面结果证明了基本的精确性:

```json
{"prompt":"Explain rotary position embeddings.","expected":null}
```

接近错误会暴露出边界质量:

```json
{"prompt":"Why did today's package build fail?","expected":"build-diagnostics"}
```

几乎没有什么股票`package`其他`build`只有明显的积极和无关的负面的路由组将夸大质量.

> 近似未命中样本与发布技能共享`package`,我知道.`build`词汇,却属于另一个工作流. 只有由明显正样本和无关负面样本组成的路由集会高估质量.

### 参数有三个表示.

调用参数跨越了几个界限:

```figure
skill-argument-boundaries
```

在每一个边界,保持意图,而不是把文本作为代码.

- 接待者决定命令语法和引用.
- 根据主机规则,技能会接收绑定文本或变量.
- 指示验证所需的值和默认值.
- 工具调用将值转换为输入的方案,并重新验证它们.

不要将原始参数插入 shell 命令中. 宁愿使用参数向量或输入MCP工具调用的脚本.

> 不要把原始参数插入 shell 命令中.优先选择使用参数向量调调的脚本或有类型的MCP 工具.

### 应用调用是显而易见的编排

产品可以激活技能,因为其工作流程已经知道任务类型.例如,一个拉动请求审查服务可以预装`pull-request-risk-review`用户按 Review后.

> 产品可以激活技能,因为它的流程已经知道任务类型.例如拉动请求 评审服务可以在用户按下 评审 后预载`pull-request-risk-review`,我知道.

这消除了路由不确定性,但会对运行时间API产生依赖.

```figure
skill-host-adapter
```

其他符合要求的客户开放时,该技能应该保持可理解性.

> 其他合规客户端开启这个技能时,它仍然可以读取.

### 技能调用是一种工具类型.

假设`release-readiness`要求`security-change-review`在依赖文件发生变化时.

调用人应提供:

- 目标技能身份;
- 设置任务和文物路径;
- 预期应对合同;
- 要求的理由;
- 如果无法实现,则会出现倒退;
- 极度深度或周期规则.

```json
{
  "target_skill": "security-change-review",
  "task": "Review dependency changes in the candidate diff",
  "inputs": ["artifacts/release.diff"],
  "expected": "risk-report.json",
  "max_depth": 2
}
```

接待者决定如何激活它,以及它是否分享文本,运行在叉子中,或者通过工具结果返回.

> 第二个技能不会被盲目粘贴在第一个. 主人决定如何激活它.它在分叉中运行,还是通过工具结果返回.

### 接下来的生命周期是主机专属的.

启动后,技能体可以留在对话中,在缩小过程中总结,或运行在委托文本中.工具权限可能持续一轮,而指示持续更长时间.一个子女可能没有父母的整个历史获得技能.

> 激活后,正文技能可能留在对话中,在压缩时被摘要,或在委托下文中运行.

不要写出依赖于一个隐形的终身假设的技能. 把持久的输出输入文件或打字状态,确保重新进入安全,并说明在中断后需要重新加载什么.

> 不要依赖隐形生命周期假设的技能. 让长期输出进入文件或有类型状态,让重复进入安全性,并写明断后必须重载什么.

```markdown
On resume, read `artifacts/release-readiness.json` if it exists.
Revalidate the candidate commit before continuing.
Do not repeat an external write whose idempotency key is already recorded.
```

## 建立它,实现它.

> **【中文解读】** `code/main.py`将策略与路由实现分为两个分离的适应器:`CorePolicyAdapter`只有认可应用提供的策略,没有任何主机扩展;`ExtensionPolicyAdapter`识别一组明确的宿主字段(如 `disable-model-invocation`)并记录是哪个字段改变了决定的意义.分离的意义:如果同一个解析器给了所有见过的前线字段都赋值,它就把运行时间约定升级为假标准.

`code/main.py`执行政策和路由作为独立的适配器.

该模型包括:

- `Actor`对于人,模型,自动操作者,应用,技能和使用者;
- `SkillMetadata`路由身份;
- `InvocationPolicy`对人/模型矩阵;
- `InvocationRequest`其他`InvocationDecision`对于可追踪的输入和结果;
- `CorePolicyAdapter`对于无主机扩展的便携式行为;
- `ExtensionPolicyAdapter`对于已认可的运行时间场所;
- `build_invocation_matrix(policy)`对于2×2视图;
- `route_request(skills, request, adapter)`在相关性排名,选择和拒绝之前进行资格过.

运行它:

```bash
cd phases/13-tools-and-protocols/25-skill-invocation-and-routing
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

演示程序将打印一个矩阵和决定, 显而易见的人类,隐含模型,自主代理,应用,技能组成和利用道. 扩展适配器的结果显示,在符合条件的替代品排名之前,被删除了封锁的顶级词汇匹配. 它还包括确切名称的允许名单. 没有模型API. 确定性路由器是为了使政策界限可检查,而不是说词汇匹配重复生产模型路由.

### 为什么核心和扩展适配器是分开的

如果一个解析器将每个观察到的前物质字段分配到意义,它会默默地将运行时间公约推广到一个虚假标准. 单独的适配器迫使调用者命名哪些主机语义是活跃的.

> 如果一个解析器给了每一个前线的字段都赋值,它就把运行时约定升级为假标准.

其他`CorePolicyAdapter`应用程序只使用申请提供的政策.`ExtensionPolicyAdapter`识别了明确的主机场和记录,该场改变了决定.

> `CorePolicyAdapter`只有使用应用提供的策略.`ExtensionPolicyAdapter`识别一组明确的宿主字段,并记录是哪个字段改变了决定.

## 让它变得更好.

在发布技能之前,请写一个招聘合同:

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

合同是适配器和测试器的设计文件.`SKILL.md`标准明确采用它以外,

> 只有一个标准可以被明确采用,它不能移植.`SKILL.md`面部材料

## 运送它.

这一课产生了`skill-invocation-router`包装.它包括一个调用模型参考,一个举例的主机政策,以及一个不执行的CLI,该CLI评估一个人,模型,自主代理,应用程序,技能组合或利用请求,并返回一个JSON决定,包括道,适配器,分数和理由.

> 本课产出发 `skill-invocation-router`包:一个调用模型参考,一个示例主机策略,以及一个不执行任何东西的CLI评估一个人类,模型,自主代理,应用,技能组合或利用 请求,返回带通道,适配器,分数和原因的JSON决定.

单次请求的CLI是政策调查,而不是一个完整的触发评估. 使用27课中标记的正面和接近错误设计来计算混乱数量,精度,召回和重复运行稳定性.

> 单请求CLI是一个策略探针,不是完整的触发评测. 用27课的正确样本+近错误标签设计来计算混计数,精确率,召回率和重复运行稳定性.

## 练习,练习.

1. 创建人类/模型矩阵的四行,并为每行写出一个合法的使用情况.
2. 添加仅用于应用的激活`CorePolicyAdapter`证明人类和模特的呼叫仍然被拒绝.
3. 写出10个近错失的部署技能. 每个提示都必须与技能分享词汇,同时属于不同的工作流程.
4. 添加前两个路由分数之间的模糊差距. 返回 `ask`如果边缘太小,
5. 增加最大的组成深度技能到技能要求,检测两个技能周期.
6. 通过核心和扩展适配器运行相同的标签集.

## 关键词 关键词

> 下表左列是术语,中列是"人们常说的"、右列是"实际含义"",最容易踩的两行:`user-invocable`是主管专属字段而非核心标准;弃权是一种正当的路由结果,不是故障.

| Term | What people say | What it actually means |
|---|---|---|
| Explicit invocation | "Slash command" | An actor supplies skill identity directly, subject to policy |
| Implicit invocation | "The model chooses" | A router selects from eligible catalog metadata based on task context |
| User-invocable | "Humans can use it" | A host-specific menu or direct-invocation property, not a core field |
| Model-invocable | "The agent can use it" | Eligibility for implicit model selection under host policy |
| Invocation adapter | "Frontmatter parser" | Code that maps a host's fields and APIs into a declared policy model |
| Near miss | "Hard negative" | A non-triggering request that resembles a skill's intended inputs |
| Abstention | "No skill selected" | A deliberate routing result when evidence is absent or ambiguous |

## 继续阅读 继续阅读

- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)对于积极的触发因素,具体性和评估.
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)对于触发和输出评估设计.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)对于目前的Codex明确和隐含的调用控制.
- [Claude Code skills](https://code.claude.com/docs/en/skills)对于一个宿主而言`user-invocable`现在`disable-model-invocation`其他问题,

> 阅读顺序建议:先阅读优化描述 掌握触发边界写法;再阅读评估技能 学触发与输出评测设计;最后对照Codex与Claude Code 两份主体文档,看同一个策略维度在不同主体中的字段名差异──
