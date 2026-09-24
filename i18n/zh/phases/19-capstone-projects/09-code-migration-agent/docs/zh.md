# 卡普斯通 09 代码迁移代理 (重级语言 / 运行时间升级) 移动 结业 运行时 仓库

> 亚马逊的迁移 (Java 8至17),谷歌的应用引擎Py2至Py3迁移器设定了2026年. 现代的OpenRewrite在尺度上进行了确定性AST重写. 格里特对代码模式式DSL的解决方案也是如此. 生产模式结合了两种:安全重写的确定性基板,以及模糊的案例的代理层,每分支构建的沙盒,以及在公交开幕前变绿的测试带. 终点是迁移50个真实存储器,并发布一个失败类别的通过率.

> **【中文解读】**本节是综合项目构建代码迁移代理,自动将代码从一个框架迁移到另一个.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (agent), Java / Python (targets), TypeScript (dashboard) | **语言:** Python (agent), Java / Python (targets), TypeScript (dashboard)
**Prerequisites:** Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure)

>  **【前置】**顶点项目 09 = 综合阶段 5/7/11/13/14/15/17──代码迁移代理 = 亚马逊迁移 / Google应用程序引擎 迁移器 / 现代开放重写 / 格里特──
>  **【类比】**代码迁移 = "AI 翻译官"──Java 8→17、Python 2→3──生产模式:确定性 AST 重写(OpenRewrite)处理简单情况 + 代理 处理模糊情况 + 沙箱分支构建 + 测试通过才开 PR──目标:迁移 50个真实仓库+发布率+失败分类.**前置知识:**五期 (NLP),七期 (变革机),十一期 (LLM工程),十三期 (工具),十四期 (代理人),十五期 (自主),十七期 (基础设施)
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 hours

## 问题 问题引入

> **【中文解读】**本节描述大规模代码迁移的代理 应用 代码迁移是编码的代理 最干净的生产应用之一 基础真相 明确的(迁移后测试是否通过?) 奖励真实的(Java 8 舰队迁移是人力密集项目) 基准公开的(迁移Bench 50 仓库子集) 确定性工具(OpenRewrite/libcst) 处理 70-80%的机械化重写,代理层处理模糊情况:构建系统漂移、传递依赖冲突、测试动、自定义注解――

> **【拓展：代码迁移产业实践】**亚马逊迁移银行(Java 8→17,50 仓库基准) 和谷歌应用程序引擎 Py2→Py3 迁移器是2026年标杆。现代的OpenRewrite 在大规模确定性AST 重写上领先,Grit使用代码模式DSL 解决同类问题。生产模式是两层架构:确定性基底处理安全重写 + 代理层处理差异性情况──每一个仓库在Daytona沙箱中代:构建→分类失败→修复→重跑,硬限制 30 分钟/$8/20轮──

扩大代码迁移是2026年编码剂生产的最清洁应用之一. 实地真相是显而易见的 (测试套件在迁移之后是否通过?),奖励是真实的 (Java-8舰队迁移是人数规模项目),基准是公开的 (MigrationBench 50-repo子集). 现代的OpenRewrite处理了确定性方面. 代理层处理了OpenRewrite的食谱不能处理的一切:模糊的重写,构建系统漂移,长尾语法,过渡的依赖性破裂.

> 大规模代码迁移是2026年编码的代理 最干净的生产应用之一.基准真相是明显的.

您将构建一个使用Java 8 repo (或Python 2 repo) 的代理,并产生一个绿色CI迁移分支.您将测量通过率,测试覆盖保护,每次 repo 的成本,并构建一个失败类别.对决于只确定性基线的对方告诉您代理的价值实际居住在哪里.

> 你会构建一个代理,它接受一个Java 8 仓库 (或Python 2 仓库) 并产生一个绿色的CI移动分支.你会测量通过率,测试覆盖率,保持每个仓库成本,并构建一个失败分类.

## 概念的核心概念

> **【中文解读】**管道分为两层:确定性基底(OpenRewrite 处理Java的导入/方法签名/空安全/试用资源等机械化重写) 和代理层(Claude Opus 4.7 / GPT-5.4-Codex 处理构建文件升级、传递依赖冲突、测试动、自定义注解) ⋅每仓库在Daytona沙箱中独立运行,代直到全部测试通过且覆盖率不下降,否则归入失败分类.

> **【拓展：失败分类学】**50个仓库迁移失败分类是本项目的核心交付物品.典型分类:深度升级_必需的(传递依赖升级) 、建_工具_漂移(构建工具版本差异) 、定制_说明(自定义注解) 、测试_flake(无关测试动) 、语法边界情况) 、预算_耗尽的预算耗尽) ⋅每种分类附带计数和示例,为后续配方 开发提供方向.

管道有两个层.**deterministic substrate**通过使用"Java" (OpenRewrite for Java,Python) 运行了大部分机械重写的安全性:进口,方法签名,零安全性修改,尝试资源,过时的API替代. 它是快速的,产生可审核的差异.**agent layer**(OpenAI Agents SDK或LangGraph over Claude Opus 4.7和GPT-5.4-Codex) 处理配方不能的情况:构建文件升级 (Maven/Gradle/pyproject),过渡性依赖冲突,测试片,定制注释.

> 管道有两层.**确定性基底**通过Java使用OpenRewrite,Python使用libcst安全运行大量机械化重写:导入,方法签名,空安全编辑,试用资源,弃用API 替换.**Agent 层**(OpenAI Agents SDK 或基于Claude Opus 4.7 和 GPT-5.4代码的LangGraph)处理配方无法处理情况:构建文件升级(Maven/Gradle/pyproject) 传递依赖冲突、测试动、自定义注解──

每个 repo 都得到一个 Daytona 沙盒,预装目标运行时间. 代理反复执行:运行构建,分类故障,应用修复,重启. 硬限制:每次 repo 30 分钟,每次 repo 8 美元,每次 repo 20 个代理转换. 如果所有测试都通过,覆盖率三角形并不是负面,分支将打开 PR. 如果没有,则 repo 被提交在失败类中,有证据.

> 每个仓库都获得了预装目标运行时的Daytona 沙箱. 代理 代代:运行构建分类失败,应用修复,重跑. 硬性限制:每仓库30分钟,8美元,20轮 代理调用. 如果所有测试通过并且覆盖率差不值负面,分支开 PR.否则,仓库被归类为证据失败分类.

失败类别是可交付的. 在50个复制中,什么是破产的? 过渡式代码? 定制注释? 构建工具版本? 测试片段与迁移无关? 每个类别都得到了数量和示例差异. 未来的食谱作者可以针对前三.

> 失败分类学是交付物品. 在50个仓库中,什么破坏了?传递依赖?自定义注解?构建工具版本?与迁移无关的测试动?每个类别获得一个计数和一个示例差异.

## 建筑,建筑

```
target repo
      |
      v
OpenRewrite / libcst deterministic recipes
   (safe, fast, auditable, ~70-80% of fixes)
      |
      v
Daytona sandbox per branch
      |
      v
agent loop (Claude Opus 4.7 / GPT-5.4-Codex):
   - run build -> capture failures
   - classify failures (build, test, lint)
   - apply fix (patch or retry recipe)
   - rerun
   - budget: 30 min, $8, 20 turns
      |
      v
test + coverage delta gate
      |
      v (passed)
open PR
      |
      v (failed)
file under failure class + attach repro
```

##  技术

- 确定性基板:OpenRewrite (Java) 或libcst (Python)
  中文翻译:确定性基板:OpenRewrite (Java) 或libcst (Python)
- 代理:OpenAI代理SDK或LangGraph 通过Claude Opus 4.7 +GPT-5.4代码
  中文翻译:代理:OpenAI代理SDK或LangGraph 通过Claude Opus 4.7 + GPT-5.4-Codex

> 中文翻译:代理:OpenAI代理SDK或LangGraph 通过Claude Opus 4.7 + GPT-5.4-Codex(翻译)

- 沙箱:每分支的Daytona开发容器,预装目标运行时间 (Java 17 / Python 3.12)
  中文翻译:沙盒:每分支的Daytona devcontainers,预装目标运行时间 (Java 17 / Python 3.12)

> 中文翻译:沙盒:每分支的Daytona devcontainers,预装目标运行时间 (Java 17 / Python 3.12)

- 构建系统:马文,格拉德,UV (字thon)
  中文翻译:构建系统:马文,格拉德尔,UV (Python)
- 标准:亚马逊迁移Bench50回复子集 (Java 8至17),谷歌应用程序引擎Py2-to-Py3回复
  中文翻译:基准:亚马逊迁移Bench50回复子集 (Java 8至17),谷歌应用程序引擎Py2-to-Py3回复

> 中文翻译:基准:亚马逊迁移Bench50回复子集 (Java 8至17),谷歌应用程序引擎Py2-to-Py3 repos(翻译)

- 测试:平行运行器,通过Jacoco (Java) 或coverage.py (Python) 覆盖
  中文翻译:测试:平行运行者,通过Jacoco (Java) 或覆盖.py (Python)
- 可观察性:每次复制的长+跟踪捆绑
  中文翻译:可观察性:每次复制的长+跟踪捆绑
- 仪表板:每个类数和示例差异的故障类别仪表板
  中文翻译:仪表板:每个类数和示例差异的失败类别仪表板

## 动手构建

> **【中文解读】**构建代码迁移代理的8个阶段:先运行确定性迁移脚本(OpenRewrite/libcst)处理70-80%的机械性变化,再让代理处理剩余的语义级迁移――每个迁移任务在戴顿沙箱中运行,构建失败时自动转移给代理――

> **【拓展：AI 代码迁移在企业中的应用】**2026年代码迁移场景:Java 8 -> 17+、Python 2 -> 3(长尾) 、AngularJS -> React、REST -> GraphQL。Amazon Q开发人员代理 专门支持 AWS 服务迁移。GPT-5 和Claude 在代码迁移中的优势在于理解跨文件依赖和API 语义变化确定性脚本只能做语法级转换,代理能理解"这个方法的签名变化,调用方需要适应新参数"――
```figure
ce-migration-funnel
```

## 建立它

1. **Recipe pass.**首先运行OpenRewrite (Java) 或libcst (Python) 配方.捕捉到机械迁移的70-80%. 作为"配方"承诺.
   中文翻译:1. **Recipe pass.**首先运行OpenRewrite (Java) 或libcst (Python) 配方.捕捉到机械迁移的70-80%. 作为"配方"承诺.

2. **Build trial.**戴顿沙箱:安装目标运行时间,运行构建.如果绿色,跳转测试.如果红色,交给代理.
   翻译: 翻译:**Build trial.**戴顿沙箱:安装目标运行时间,运行构建.如果绿色,跳转测试.如果红色,交给代理.

3. **Agent loop.**工具的LangGraph: `run_build`现在`read_file`现在`edit_file`现在`run_test`现在`git_diff`代理将故障分类 (深度,语法,测试,构建工具) 并应用针对性的修复. 复制.
   翻译: 翻译:**Agent loop.**工具的LangGraph: `run_build`现在`read_file`现在`edit_file`现在`run_test`现在`git_diff`代理将故障分类 (深度,语法,测试,构建工具) 并应用针对性的修复. 复制.

4. **Budget caps.**任何违规行为都会停止,并且在"预算_耗尽"下,
   翻译: 翻译:**Budget caps.**任何违规行为都会停止,并且在"预算_耗尽"下,

5. **Test + coverage gate.**构建绿色后,运行测试套件. 进行覆盖与基 repo 的比较. 如果覆盖下降超过 2%,请在"覆盖_回归"下文件.
   翻译: 五.**Test + coverage gate.**构建绿色后,运行测试套件. 进行覆盖与基 repo 的比较. 如果覆盖下降超过 2%,请在"覆盖_回归"下文件.

6. **PR open.**通过不同和简要的做法, 执行该经纪人的承诺.
   翻译: 七个字**PR open.**通过不同和简要的做法, 执行该经纪人的承诺.

7. **Failure taxonomy.**对于每一个失败的回复, 标签一个类别:`dep_upgrade_required`现在`build_tool_drift`现在`custom_annotation`现在`test_flake`现在`syntax_edge_case`现在`budget_exhausted`建立一个仪表板.
   翻译:7.**Failure taxonomy.**对于每一个失败的回复, 标签一个类别:`dep_upgrade_required`现在`build_tool_drift`现在`custom_annotation`现在`test_flake`现在`syntax_edge_case`现在`budget_exhausted`建立一个仪表板.

8. **50-repo run.**执行在移动银行子集中. 报告每类通过率,每次报价,覆盖性-保存,以及仅对比与确定性的基线.
   翻译:8.**50-repo run.**执行在移动银行子集中. 报告每类通过率,每次报价,覆盖性-保存,以及仅对比与确定性的基线.

## 用它使用方法

```
$ migrate legacy-java-service --target java17
[recipe]   27 rewrites applied (JUnit 4->5, HashMap initializer, try-with-resources)
[build]    FAIL: cannot find symbol sun.misc.BASE64Encoder
[agent]    turn 1 classify: removed_jdk_api
[agent]    turn 2 apply: sun.misc.BASE64Encoder -> java.util.Base64
[build]    OK
[tests]    412/412 passing; coverage 84.1% -> 84.3%
[pr]       opened #1841  cost=$3.20  turns=4
```

## 发射上线

`outputs/skill-migration-agent.md`给出一个 repo,它执行确定性食谱,然后执行代理循环来产生绿色迁移分支,或者在一个类别下文件 repo.

> `outputs/skill-migration-agent.md`交付物品. 给定仓库,它执行确定性配方,然后代理循环产生绿色迁移分支,或将仓库归类为学分类.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | MigrationBench pass rate | 50-repo subset pass@1 |
| 25 | MigrationBench 通过率 | 50 仓库子集 pass@1 |
| 20 | Test-coverage preservation | Mean coverage delta vs base |
| 20 | 测试覆盖率保持 | 与基础仓库的平均覆盖率差值 |
| 20 | Cost per migrated repo | $/repo on passing runs |
| 20 | 每迁移仓库成本 | 通过运行中的 $/仓库 |
| 20 | Agent / deterministic-tool integration | Fraction of fixes that OpenRewrite handled vs agent authored |
| 20 | Agent / 确定性工具集成 | OpenRewrite 处理的修复比例 vs Agent 编写的 |
| 15 | Failure analysis write-up | Taxonomy completeness with exemplars |
| 15 | 失败分析报告 | 带示例的分类学完整性 |
| **100** | | |

## 练习题

1. 运行迁移管道只使用OpenRewrite (没有代理).将通过率与整个管道进行比较. 确定只有代理才是区别的情况.
   中文翻译:仅用OpenRewrite(无代理)运行迁移管道――将通过率与完整管道比较――识别仅代理是差异的情况――

> 中文翻译:仅用OpenRewrite(无代理)运行迁移管道――将通过率与完整管道比较――识别仅代理是差异的情况――(翻译)


2. 执行" lint-clean"检查:迁移后,运行一个风格linter (Java无点,Python无).如果出现新的 lint 错误,则失败 PR.测量覆盖性保存但风格重回率.
   中文翻译:实现"清"检查:迁移后运行风格linter(Java 用无,Python 用 ruff) ・・・如果出现新的 错则 PR 失败――测量覆盖率保持但风格退化的比率――

> 中文翻译:实现"清"检查:迁移后运行风格linter(Java 用无,Python 用 ruff) ・・・如果出现新的 错则 PR 失败――测量覆盖率保持但风格退化的比率――(翻译)


3. 添加"最小差异"优化器:经过经验后,经验者分支通过第二次通过,切除不必要的变化.报告差异大小的减少.
   中文翻译:添加"最小差"优化器:经过测试后,使用第二轮修剪不必要的变更.

> 中文翻译:添加"最小差"优化器:经过测试后,用第二轮修剪不必要的变更.


4. 扩展到第三次迁移:节点18至节点22. 再利用沙盒包装;换取配方层进行定制代码模式.
   中文翻译:扩展到第三种迁移:Node 18到Node 22──复用沙箱包装;将配方层换为自定义代码模式──

5. 测量时间到第一绿色构建 (TTFGB) 作为UX指标.目标:p50在10分钟以下.
   中文翻译:测量首次绿色构建时间 (TTFGB) 作为UX 指标.目标:p50 低于10分钟.

## 关键词 关键词

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Deterministic substrate | "Recipe engine" | OpenRewrite / libcst: declarative AST rewrites with safety guarantees |
| 确定性基底 | "配方引擎" | OpenRewrite / libcst：带安全保证的声明式 AST 重写 |
| Codemod | "Code-modifying program" | A rewrite rule that changes source code mechanically |
| Codemod | "代码修改程序" | 机械地改变源代码的重写规则 |
| Build drift | "Tool version skew" | Subtle Maven / Gradle / uv behavior changes between major versions |
| 构建漂移 | "工具版本偏差" | 主要版本之间 Maven / Gradle / uv 的细微行为变化 |
| Failure class | "Taxonomy bucket" | A labeled reason a repo did not migrate: dep, syntax, test, build-tool, budget |
| 失败分类 | "分类学桶" | 仓库未能迁移的标记原因：依赖、语法、测试、构建工具、预算 |
| Coverage delta | "Coverage preservation" | Change in test coverage % from base to migrated branch |
| 覆盖率差值 | "覆盖率保持" | 从基础到迁移分支的测试覆盖率变化 |
| Agent turn | "Tool-call round" | One plan -> act -> observe cycle in the agent loop |
| Agent 轮次 | "工具调用轮" | Agent 循环中的一个规划 -> 执行 -> 观察周期 |
| Budget exhaustion | "Hit the ceiling" | The repo consumed its 30-min / $8 / 20-turn limit without passing |
| 预算耗尽 | "触及上限" | 仓库消耗了 30 分钟 / $8 / 20 轮限制但未通过 |

## 继续阅读 继续阅读

- [Amazon MigrationBench](https://aws.amazon.com/blogs/devops/amazon-introduces-two-benchmark-datasets-for-evaluating-ai-agents-ability-on-code-migration/)2026年法典基准
  中文翻译:2026年规范基准
- [Moderne.io OpenRewrite platform](https://www.moderne.io)确定性基板参考
  中文翻译:确定性基底参考
- [OpenRewrite documentation](https://docs.openrewrite.org) 制订食谱
  中文翻译:配方编写
- [Grit.io](https://www.grit.io)替代代代码模式DSL
  中文翻译:备选代码模式 DSL
- [OpenAI sandboxed migration cookbook](https://developers.openai.com/cookbook/examples/agents_sdk/sandboxed-code-migration/sandboxed_code_migration_agent) 代理人 SDK参考
  中文翻译:代理 SDK 参考
- [Google App Engine Py2 to Py3 migrator](https://cloud.google.com/appengine)替代迁移基准
  中文翻译:备选迁移基准
- [libcst](https://github.com/Instagram/LibCST) Python 确定性基板
  中文翻译:字thon 确定性基底
- [Daytona sandboxes](https://daytona.io)每分支的参考沙盒
  中文翻译:参考每分支沙箱
