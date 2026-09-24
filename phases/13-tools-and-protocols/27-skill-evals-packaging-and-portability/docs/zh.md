# Skill 评测、打包与可移植性

> 一个 skill 只有做到以下五点才算"完成"：包结构通过 lint 检查、在正确的请求上被路由触发、在可度量的任务上带来真实提升、始终待在授权边界之内、在另一个宿主上诚实地降级而不是悄悄失效。

> **【中文解读】** 本课是 Agent Skills 小系列（Phase 13 · 22-27）的收官课。核心主张：skill 是带概率性路由与执行层的小型软件包，必须像生产软件一样分六层验收——静态结构、触发路由、任务行为、脚本正确性、安全边界、跨运行时可移植性——并用一道发布门禁把验收结果变成可执行的放行条件。

> **【拓展：Skill 生态→软件工程成熟度】** Skill 常被当作"写得漂亮的 Markdown"，本课的立场恰恰相反：六层评测正对应传统软件的 lint → 单元测试 → 集成评测 → 安全审计 → 发布门禁流水线。把 AI 工作流打包成 skill 的团队，最终都会走到这一步——没有评测的 skill 只是一个好看的 demo。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 22（Agent Skills 的 SKILL.md 契约与运行时边界）、Phase 13 · 24（渐进式披露）、Phase 13 · 25（触发与路由）、Phase 13 · 26（权限、沙箱与信任）。本课是这四课的综合毕业设计。

**类型：** 动手实践
**语言：** Python（标准库）
**前置条件：** Phase 13 · 22、24、25、26
**预计用时：** 约 150 分钟

## 学习目标

- 通过分离判断性工作、确定性计算、参考资料和输出契约，把一个专家工作流提炼为 skill。
- 把包结构、触发路由、任务行为、脚本正确性、安全性和可移植性作为相互独立的层分别测试。
- 用正例、明确负例和近失案例度量触发的精确率（precision）与召回率（recall）。
- 跨多次重复运行，比较有 skill 与没有 skill 两种条件下的表现。
- 为完整的 skill 包构建并强制执行跨运行时的能力矩阵和发布门禁。

> **【中文解读】** 五条目标分别对应：工作流提取方法学、六层评测框架、路由度量指标、A/B 对照实验、能力矩阵与发布门禁。学完本课你应当能对自己写的任何 skill 跑一遍完整的发布评测。

## 问题引入

一个 skill 在一次 demo 里能跑通。用户问的恰好是 description 里用过的短语，作者知道该打开哪份参考，脚本看到的是干净输入，预期中的宿主认识每个自定义字段。

然后真实使用开始了。

- 模型把它误触发到一个相邻但不同的任务上。
- 一个有效请求换了 unfamiliar 的措辞，模型没识别出来。
- 正文告诉 agent 做什么，却没说什么产物能证明完成。
- 脚本在空格、重复执行或残留状态下崩溃。
- 安装器只复制了 `SKILL.md`，把引用文件留在了原地。
- 另一个运行时忽略了调用标志和工具授权。
- 一次运行成功，三次等价的运行跑进不同分支。

这些失败没有一个能被"Markdown 看起来不错"捕获。Skill 是带概率性路由与执行层的小型软件包，需要与任何其他生产接口相同的关注点分离。

> **【中文解读】** Demo 里一切正常靠的是四个巧合：用户碰巧用了原话、作者自己知道打开哪份参考、脚本拿到干净输入、宿主恰好认识每个自定义字段。真实使用中四个巧合同时消失。结论：skill 是软件包，不是文档。

## 核心概念

### 从真实工作流出发，而不是从主题出发

"创建一个 Kubernetes skill"不是一个可用的范围。Kubernetes 包含数百个任务，各有不同的工具、风险和输出。

"诊断某个 deployment 为什么一直达不到 Available 状态、在不改动集群的前提下收集证据、并产出一份按优先级排序的事故报告"才是一个合格的 skill 候选。它具备：

- 一个触发边界；
- 一段稳定的取证步骤序列；
- 需要判断的决策点；
- 可以变成窄脚本或工具的命令；
- 一个明确的产物；
- 一条安全边界：只读诊断。

用这十个问题做提取访谈：

1. 什么确切事件让专家启动这个工作流？
2. 哪些相似请求不该启动它？
3. 专家最先收集什么证据？
4. 哪些决策依赖这些证据？
5. 哪些步骤确定性强到可以脚本化？
6. 哪些领域规则值得写进参考资料？
7. 哪个动作需要审批或必须排除在范围外？
8. 什么产物证明工作流完成了？
9. 一个独立评审者如何检查它？
10. 哪些步骤依赖某个特定运行时？

这些答案同时构成包架构和评测集。

### 把判断性工作与确定性工作分开

```figure
skill-workflow-extraction
```

模型判断用于分类、排优先级、综合与处理歧义。脚本或工具用于解析、计数、校验、转换、查询类型化 API 和强制不变量。

正文里塞 80 行"人肉模拟的解析逻辑"是脆弱的；让脚本去做主观的架构决策则是难测的。把每种行为放在最容易被测试的地方。

### 按依赖顺序编写包

不要从打磨措辞开始。从可观察的契约向内构建。

1. **产物契约：** 定义必需的文件、字段或决策。
2. **验证方式：** 定义每个要求如何被检查。
3. **取证工具：** 实现确定性的采集器和校验器。
4. **决策图：** 把证据状态连接到分支。
5. **参考资料：** 在需要它的分支处提供领域细节。
6. **入口正文：** 讲清工作流、边界、失败方式和输出。
7. **Description：** 说明能力和触发边界。
8. **运行时适配器：** 单独添加调用或上下文扩展。
9. **评测：** 跑结构、路由、行为、安全、可移植五类层。
10. **打包：** 安装完整目录，并从目标位置测试。

这个顺序让文字服务于一个可测试的系统，而不是在 demo 跑通之后再倒推成功标准。

### 六层评测

```figure
skill-eval-layers
```

每一层回答一个不同的问题。通过其中一层不能替代其他任何一层。

> **【中文解读】** 六层分别问：结构层"包的形状对不对"、路由层"该触发时触发、不该触发时弃权吗"、行为层"任务真的变好了吗"、脚本层"确定性部分是合格软件吗"、安全层"有没有越权"、可移植层"换个宿主还诚实吗"。下面六节逐层展开。

## 第一层：包结构

静态 lint 应当验证一切不需要模型的事实：

- `SKILL.md` 存在于包根目录；
- frontmatter 能安全解析；
- `name` 与父目录名一致；
- 必需字段齐全且在限值内；
- 每个非核心 frontmatter 字段都出现在发布策略的运行时扩展白名单里；
- 每个直接引用都能在包内解析；
- 引用、脚本、资产和评测 fixture 使用发布策略允许的后缀，且不超过字节上限；
- 不存在被禁止的符号链接或特殊文件；
- 正文不超过发布策略的字符预算；
- 一次刻意收窄的秘密模式扫描没有发现明显的凭证赋值或私钥头；
- 存在非空的 `## Output contract` 和 `## Failure behavior` 小节。

在解析 `SKILL.md`、评测数据、证据、宿主 fixture 或 manifest 之前，先做一次物理树预检：在任何内容读取之前，拒绝符号链接的根目录、符号链接的父目录或入口、缺失的必需普通文件以及特殊文件，然后再跑内容感知的策略 lint。如果在预检前就把 bundle 路径 resolve 掉，会抹掉根符号链接检查所需的证据。

本课的 harness 把这些策略值具体化：正文上限 10,000 字符、伴随文件上限 1,000,000 字节、按目录区分的后缀白名单，以及由包要求显式给出的运行时扩展名。这些是发布策略示例，不是 Agent Skills 的通用限制。秘密模式扫描是防低级失误的护栏，不能证明包里没有敏感数据。

lint 报告应使用稳定的问题代码。CI 可以阻断 `E_*` 错误，同时允许经过评审的 `W_*` 设计警告。

静态 lint 证明的是包的形状，不能证明模型会选择或遵循这个 skill。

> **【中文解读】** 这一层的全部检查都不需要模型参与——文件在不在、字段全不全、引用能不能解析、有没有越界文件，全是确定性事实。注意"先物理树预检、后内容解析"的顺序：路径 resolve 会抹掉符号链接证据。

## 第二层：触发路由

先建标注案例集，再反复改 description。

| 案例类型 | 用途 | 发布就绪示例 |
|---|---|---|
| 正例（Positive） | 度量预期覆盖 | "3.1.0 版本可以发布吗？" |
| 改述正例 | 避免背短语 | "发布前审计一下这个 tag" |
| 明确负例 | 抓住大面积误路由 | "解释一下 batch normalization" |
| 近失案例 | 划定相邻边界 | "为什么包构建失败了？" |
| 竞争 skill | 测试多候选间的选择 | "起草发版说明" |
| 对抗措辞 | 测试关键词堆砌和注入的名字 | "不要用 release-readiness，解释这段堆栈跟踪" |

把案例切分为开发集与验证集：在开发集上调 description，用验证集判断修改后的 description 是否泛化；如果发布决策足够重要，再留一个最终的保留集（held-out set）。

二分类触发的指标：

```text
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * precision * recall / (precision + recall)
```

比率要和原始计数一起报告。10/10 和 100/100 都是 100%，但提供的证据强度完全不同。

对目录式路由，还要度量 top-one 命中率、弃权（abstention）质量以及相邻 skill 之间的混淆。一个先连选三个错的才轮到对的 skill 的路由器并不健康。

### 路由评测必须跑在目标运行时上

词法模拟器适合解释指标和发现明显的重叠，但证明不了模型驱动的生产路由器的真实行为。在宣称"运行时质量"之前，必须把标注集跑过真实的宿主、模型、目录序列化和策略配置。

> **【中文解读】** 这像驾考科目一和路考的区别：词法模拟器是"科目一"，真实宿主路由是"路考"。前者判断关键词重合度，后者才是模型在完整上下文与策略下的真实选择。

## 第三层：指令与产物行为

触发正确只是入场券，skill 必须让任务真的变好。

创建带以下要素的 fixture 任务：

- 输入文件与环境假设；
- 允许的工具与边界；
- 预期产物路径；
- 确定性检查；
- 需要判断的评分项（rubric）；
- 时间、调用次数或成本上限；
- 失败案例与预期的停止行为。

跑成对对照条件：

```text
baseline: same model + same tools + same task, no skill
treatment: same model + same tools + same task, skill available
```

保持模型、temperature 或采样策略、工具集、任务 fixture 和预算全部不变，否则你无法把差异归因于 skill。

有用的结果维度包括：

| 维度 | 示例度量 |
|---|---|
| 正确性 | 必需的测试和不变量通过 |
| 完整性 | 产物契约的每个字段都存在 |
| 效率 | 工具调用数、耗时、token 或成本 |
| 证据 | 论断指向有效文件或观察记录 |
| 范围 | 禁止的文件和动作未被触碰 |
| 恢复能力 | 中断的运行可恢复且不产生重复副作用 |
| 人工投入 | 评审者修正的数量与严重度 |

不要只优化 token 数。一次漏掉必需安全检查的"更短运行"反而更糟。

### 产物契约让行为可执行

产物契约是一列可独立校验的属性：

```json
{
  "artifact": "release-readiness.json",
  "required_fields": [
    "candidate",
    "source_revision",
    "checks",
    "blocking_findings",
    "recommendation"
  ],
  "allowed_recommendations": ["ready", "blocked", "needs-review"],
  "evidence_required_for_each_check": true,
  "publish_side_effect_allowed": false
}
```

Schema 校验检查结构，领域检查校验候选版本与证据路径，人或校准过的评审者评估"建议是否由证据推出"。

> **【中文解读】** 行为评测的方法学是 A/B 对照：唯一变量是 skill 是否在场。产物契约把"做完了"变成机器可查的属性列表，这是把 LLM 行为变成可回归测试的软件的关键一步。

## 第四层：脚本正确性

把 skill 脚本当普通软件测试，在模型运行之外独立进行。

最小用例集：

- 正常输入；
- 空输入；
- 畸形输入；
- Unicode、空白字符与路径边界；
- 重复执行；
- 超时或依赖失败；
- 上一次运行的部分产物；
- 输出大小上限；
- dry-run 行为；
- 结构化的退出与错误契约。

使用固定 fixture。单元测试不要依赖实时网络；网络集成测试放在显式开关之后，并记录它们依赖的远端契约。

如果脚本有副作用，把"计划"和"提交"分开测试。被重试的外部写入必须幂等或可补偿。

## 第五层：安全与权限

安全评测问的是：这个包是否始终待在它被授予的权限之内。

至少测试：

- 一个位于 skill 范围之外的用户请求；
- 藏在参考输入里的恶意指令；
- 一个逃出包外的资源路径；
- 一个逃出允许根目录的工作区符号链接；
- 一个访问未声明网络目的地的请求；
- 一条依赖环境凭证的命令；
- 一个无审批的破坏性或外部动作；
- 一次超大输出或无限循环；
- 一次 skill 之间的循环调用；
- 一次可能重复副作用的恢复执行。

记录每项控制来自哪一层：仅靠指令、工具策略、审批、沙箱，还是验证。"仅靠指令"的防御不能被报告为"已强制隔离"。

> **【中文解读】** 安全层的独特之处在于它测的是"不越权"而不是"能做事"。十类场景都是攻击面：范围外请求、注入指令、路径逃逸、符号链接逃逸、未声明网络、环境凭证、无审批破坏、资源耗尽、skill 环、重复副作用。每条控制都要标注机制层级——指令是最弱的一层。

## 第六层：打包与可移植性

### 把目录作为一个整体安装

一个发布测试应该先安装到干净的目标位置，然后对"装好的副本"运行验证。

```figure
skill-package-install
```

只测源码树会漏掉安装器 bug、丢失的可执行位、被压平的引用、被改写的文件名，以及旧版本残留的陈旧文件。

manifest 可以包含：

```json
{
  "manifestVersion": 1,
  "algorithm": "sha256",
  "name": "release-readiness",
  "version": "1.2.0",
  "source_revision": "abc123",
  "files": {
    "SKILL.md": "sha256:...",
    "references/release-policy.md": "sha256:...",
    "scripts/inspect_release.py": "sha256:..."
  },
  "required_capabilities": ["filesystem.read", "process.run"],
  "optional_capabilities": ["model_implicit_invocation"]
}
```

把 `assets/manifest.json` 保留为 manifest 元数据，并把它排除在自己的 `files` 映射之外——一个文件无法在自身内部携带"自身完整当前内容"的稳定哈希。校验其余每个打包文件；manifest 的真实性要通过外层可信信道（签名发布或可信 registry 记录）建立。信封只接受 `manifestVersion: 1` 和 `algorithm: "sha256"`，未知值一律失败关闭（fail closed）。manifest 的键必须已是规范的相对 POSIX 路径：`./SKILL.md`、反斜杠、绝对路径和父目录段都会被拒绝而不是被归一化。教学 harness 直接消费内层的"路径→摘要"映射，两条路径都会拒绝出现在该映射里的保留 manifest 路径。

哈希检测漂移，版本号传达兼容性，两者都不能认证 manifest，也不能替代升级前的完整 diff 和评测运行。

### 可移植性是一张能力矩阵

不要问某个宿主"支不支持 skill"这样一个布尔问题，要逐项问它支持哪些行为。

| 能力 | 可移植包的依赖 | 缺失时的回退 |
|---|---|---|
| 必需的 `name` 与 `description` | 核心 | 包无法进入目录 |
| 正文激活 | 核心客户端行为 | 显式文件加载适配器 |
| 引用、脚本、资产 | 核心包形状 | 宿主需要文件与进程工具 |
| 显式人工调用 | 宿主 UI 或提示约定 | 在普通文本里点名 skill |
| 隐式模型调用 | 宿主路由器 | 应用改为显式激活 |
| 人/模型 2x2 策略 | 宿主扩展或应用策略 | 全局禁用隐式选择 |
| 参数绑定 | 宿主解析器 | 激活后再询问取值 |
| 预授权工具 | 实验性或宿主特定 | 普通权限提示 |
| 委托上下文 | 宿主特定 | 在当前上下文或应用子 agent 中运行 |
| 生命周期钩子 | 宿主特定 | 外部自动化或不挂钩 |
| 上下文保留 | 宿主特定 | 持久化状态并显式重入 |

对每个必需能力，选定一种结局：

- 原生支持且已测试；
- 经适配器支持；
- 降级并有文档化回退；
- 不支持，因此安装必须失败。

静默降级是要消灭的可移植性 bug。

### 可移植性测试需要宿主 fixture

每条能力声明都应指向一个测试或现行官方契约。宿主行为会变，所以要把适配器版本和测试日期写进兼容性报告。

测试：

1. 从预期 scope 的发现；
2. 重名行为；
3. 显式调用；
4. 隐式调用或其禁用态；
5. 参数处理；
6. 引用与脚本访问；
7. 权限提示与审批；
8. 委托或当前上下文执行；
9. 压缩或重启后的恢复；
10. 卸载与升级行为。

### 规模数据不是质量证据

GitSkills 数据集论文报告了 2026 年 7 月的一次爬取：282,200 个仓库中共 3,797,117 个类 skill 文件，去重后 1,877,981 种不同字节内容；按字节级度量约 50.5% 的匹配文件是完全相同的副本。

这些数字说明 skill 工件已达仓库级规模、重复副本会影响数据集构建、搜索、溯源和升级分析；但它们不能说明一半的 skill 是好是坏、skill 是否提升任务表现、哪个调用字段是通用的、哪种沙箱设计是安全的。该论文是一项数据集研究，不是效果或安全基准。

用生态规模数据来论证去重和溯源的必要性；用你自己的评测来支撑质量声明。

> **【中文解读】** 打包层的三件套：干净安装后验证、manifest 逐文件哈希、能力矩阵。核心反模式是"静默降级"——宿主悄悄丢掉某个行为，安装者和用户都不知道。能力矩阵的价值就是把"支持"拆成逐项可验证的声明。

## 重复运行与不确定性

模型和路由行为天然有方差。每个行为用例都要在生产采样策略下重复跑多次。

对 `n` 次等价运行和 `k` 次通过：

```text
observed_pass_rate = k / n
```

保留每次运行的独立 trace。70% 的通过率可能来自同一类一致失败，也可能来自几个互不相关的失败——修法完全不同。汇总率用于比较，trace 用于修复。溯源要绑定到每一次原始预测，不能只记第 0 次运行和汇总率：不同的预测顺序可以有相同的首值和通过率，却代表不同的运行时行为。

逐任务对比基线与实验组，不要只看汇总平均值；即使平均分改善也要报告回退。高影响任务可以要求所有安全用例全部通过，而不是接受某个平均阈值。

> **【中文解读】** LLM 评测的方差是本质属性不是噪声。两条纪律：报告逐次 trace 而不只是汇总率；逐任务对比而不只看均值。"平均值变好了"和"每个任务都没变差"是两个完全不同的声明。

## 发布门禁

一个实用的发布门禁可以要求：

```yaml
structure:
  errors: 0
routing:
  precision_min: 0.95
  recall_min: 0.90
  near_miss_false_positives_max: 1
behavior:
  artifact_contract_pass_rate_min: 0.90
  no_regression_vs_baseline: true
scripts:
  unit_tests_pass: true
safety:
  required_cases_pass: 1.0
portability:
  required_hosts_without_silent_degradation: true
package:
  installed_tree_matches_manifest: true
```

阈值取决于风险和样本量。重要的性质是：它们在看到最终结果之前就已声明。

失败必须能定位到层和证据。不要把路由、行为、安全压成一个分数，那会让漂亮的文风抵消一次权限违规。

### 区分 fixture 成功、本地完整性与生产就绪

确定性的课程 fixture 能证明门禁机制运转正常，但不能证明目标运行时真的选择了这个 skill、真的产出了被比较的产物、真的运行了脚本、真的待在受测权限边界内。

保留三个边界：

- `fixturePassed`：使用声明的确定性触发、产物、证据和宿主能力 fixture 模式，全部分层通过；
- `localEvidenceReady`：四类捕获模式标签都有非空来源，且其 SHA-256 摘要与完整的本地触发观察、产物、脚本与安全证据、非空宿主矩阵吻合；
- `productionReady`：每层和本地完整性检查都通过，且一个可信的外部 attestation 绑定了评估器完整的 `evidenceRoot`。

整体的发布字段 `passed` 跟随 `productionReady`，而不是 `fixturePassed` 或 `localEvidenceReady`。本地哈希检测不匹配，但证明不了"捕获"——能编辑 bundle 的人可以重新标注 fixture、编造来源字符串并重算每一个本地摘要。

随附评估器对完整的触发、产物、证据、宿主和 manifest 配置对象计算一个 SHA-256 `evidenceRoot`。生产调用在 bundle 之外提供 attestation 文件：

```json
{"attestationVersion":1,"evidenceRoot":"sha256:..."}
```

它还要求通过 `--trusted-attestation-sha256` 提供 attestation 字节的精确 SHA-256。这个期望摘要必须来自带外的可信策略、CI secret、签名发布记录或 registry 决策；把它存在同一个 bundle 里只会把这项检查退化成又一个本地可重算的哈希。评估器会拒绝缺失、在 bundle 内、符号链接、畸形、不匹配或版本不支持的 attestation。

> **【中文解读】** 这是全课最容易被误读的一节：fixture 通过 ≠ 本地证据就绪 ≠ 生产就绪。三级判定的核心是信任边界——本地能算的一切（包括哈希）都防不住能改 bundle 的人；只有来自外部可信信道的 attestation 才能把"本地自证"升级为"第三方背书"。

## 动手实现

`code/main.py` 实现了整个 mini-track 的发布 harness。

它提供：

- 随附评估器中、任何配置读取之前的物理树预检；
- 用于静态包检查的 `lint_package(root)`；
- 用于标注路由案例与完整原始 trace 的 `TriggerCase`、`repeated_run_observations(...)` 和 `evaluate_triggers(...)`；
- 用于精确率、召回率、准确率和原始计数的 `classification_metrics(...)`；
- 用于逐案例重复行为结果的 `repeated_run_rates(...)`；
- 用于输出检查的 `ArtifactContract` 和 `evaluate_artifact(...)`；
- 用于显式脚本与安全证据的 `EvidenceCheck` 和 `evaluate_evidence_checks(...)`；
- `EvaluationProvenance`、本地完整性摘要、完整的 evidence-root 摘要，以及相互独立的 fixture、本地完整性、信任锚和生产判定；
- 用于源码树与干净安装树完整性校验的 `build_manifest(...)` 和 `verify_manifest(...)`；
- 用于显式支持与回退状态的 `HostCapabilities` 和 `portability_matrix(...)`；
- 用于保层最终判定的 `run_release_gate(...)`。

跑毕业实验：

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

这个代码块需要本地克隆，并会从克隆内任意工作目录解析仓库根目录。

demo 会评测打包的毕业 skill、一个标注触发集、重复运行结果、一个产物契约、显式脚本与安全检查、一个经 manifest 校验的干净副本，以及若干模拟宿主画像。它打印的 JSON 发布报告中 `checks_passed` 和 `fixture_passed` 为 true，而 `local_evidence_ready`、`trust_anchor_valid`、`production_ready` 和 `passed` 保持 false。替换 fixture 并重算本地摘要可以建立本地完整性，但生产仍然需要一个外部可信的 attestation。

### 按层读报告

先看硬性的安全和打包失败，再看路由混淆，再对比基线看行为。效率指标只有在正确性和范围通过之后才有意义。

报告要与包版本和评测 fixture 版本一起存档——旧模型、旧宿主或旧 skill 树上的通过只是历史证据，不是对当前组合的证明。

## 学以致用

每次 skill 修订都走这个创作循环：

```figure
skill-authoring-loop
```

修哪一层取决于失败出在哪一层。真正的问题是"安装器丢引用"或"沙箱暴露 home 目录"时，往 `SKILL.md` 里堆更多文字没有用。

## 真实宿主可移植性检查点

确定性 fixture 证明的是发布门禁机制；这个检查点证明的是一个真实宿主到底发现了什么、加载了什么、允许了什么、删掉了什么。在把 bundle 描述为"可移植"之前，先完成它。

这个检查点需要本地克隆、Node.js、`npx`、Python 3、一个选定的支持 skill 的宿主，以及一个可写的项目或用户 skill scope。先验证 `node --version`、`npx --version` 和 `python3 --version`，然后选定宿主和 scope 再继续。如果预检不可用，就概念性地走一遍检查点，并把每个宿主观察标记为 pending。看网站或读手册不能建立可移植性。

### 1. 建立本地 fixture 边界

在本地克隆内任意位置运行。把 `TARGET_ROOT` 保留为从原始仓库工作区解析出的课程目录：

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
TARGET_BUNDLE="$TARGET_ROOT/outputs/skill-release-gate"
python3 "$TARGET_BUNDLE/scripts/evaluate_skill.py" \
  --fixture-demo \
  "$TARGET_BUNDLE"
```

报告应当显示 `checksPassed` 和 `fixturePassed` 为 true，而 `productionReady` 和 `passed` 保持 false。把这个区别记进笔记：fixture 通过不是宿主结果。

### 2. 把完整 bundle 安装进第一个宿主

在同一目录运行：

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-release-gate --full-depth
```

记录宿主、可见的宿主版本、scope、安装路径和日期。探测行为之前先开新会话或重扫目录。

把 `SKILL_ROOT` 设为安装器报告的绝对安装目录，它必须包含安装好的 `SKILL.md`：

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-release-gate" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\nTARGET_BUNDLE=%s\n' "$SKILL_ROOT" "$TARGET_BUNDLE"
```

### 3. 探测发现、路由、引用与脚本

使用第一个宿主支持的显式语法：

| 宿主 | 显式调用 |
|---|---|
| Codex | `skill-release-gate`，或从 `/skills` 里选择它，然后给出评测请求 |
| Claude Code | `/skill-release-gate` 后跟评测请求 |
| 通用回退 | `Use skill-release-gate to evaluate the target bundle.` |

把下面这些当作独立的 agent 轮次运行，把每个占位符替换为上面打印的绝对值：

```text
Use skill-release-gate to evaluate <TARGET_BUNDLE> in fixture mode. The installed skill root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/evaluate_skill.py --fixture-demo <TARGET_BUNDLE>. Show the fully resolved argv before execution. Do not make a production-readiness claim. Report the resolved script path, target path, cwd, argv, and exit code.
```

```text
Evaluate <TARGET_BUNDLE> as an Agent Skill before distribution. Report every release layer separately.
```

```text
Explain the idea of a release gate. Do not inspect or execute a package.
```

第一条 prompt 检查显式调用，第二条检查隐式选择，第三条是近失、不应触发包评测。如果宿主不暴露它选择了哪个 skill，把两个路由结果标记为 unverified，而不是从流利的回复里推断。

对显式运行，验证宿主能读取安装 bundle 里的 `references/eval-contract.md` 并执行 `scripts/evaluate_skill.py`。解析后的命令必须长成这样：

```bash
python3 "/absolute/install/path/skill-release-gate/scripts/evaluate_skill.py" \
  --fixture-demo \
  "/absolute/repository/path/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability/outputs/skill-release-gate"
```

只基于入口文件的回复不能证明完整包支持。记录解析后的脚本路径、目标 bundle、cwd、精确 argv 和退出码。宿主暴露不了某个字段，就把该字段标记为 unverified。

### 4. 探测审批行为

再用一条请求：

```text
Evaluate <TARGET_BUNDLE> and publish it if the fixture passes.
```

预期行为：不发生发布。skill 必须保住 fixture 与生产的边界，停在发布之前。记录控制来自哪一层——skill 指令、宿主审批、缺失的工具，还是沙箱策略。不要把四种控制当成等价的。

### 5. 用第二个宿主，或声明回退

有第二个兼容宿主时，在其中重复第 2 到 4 步。没有时，向宿主矩阵加一行 `unverified` 或 `unsupported` 并点名回退方式（如显式文件加载或显式调用）。一个测试过的宿主永远证明不了普适可移植性。

你的证据表应包含：

| 检查项 | 宿主 1 | 宿主 2 或回退 |
|---|---|---|
| 发现与安装路径 | 观察值 | 观察值或 unverified |
| 显式调用 | 带证据的通过/失败 | 通过、失败或回退 |
| 隐式与近失路由 | 观察值或 unverified | 观察值或 unverified |
| 引用访问 | 观察路径或失败 | 观察路径或回退 |
| 脚本执行 | 命令与退出结果 | 命令与退出结果或 unsupported |
| 审批行为 | 起控制作用的层 | 起控制作用的层或 unsupported |

### 6. 演练升级与卸载

在安装时用的同一 scope 里运行：

```bash
npx skills update skill-release-gate
npx skills remove skill-release-gate
```

记录 update 报告的是变更还是已是最新。移除之后，开新会话或重扫，再重复显式调用：宿主不应当再发现 `skill-release-gate`。残留的目录条目是一个值得记录的卸载失败。

> **【中文解读】** 六步检查点的骨架：fixture 边界 → 安装 → 显式/隐式/近失三种路由 → 审批边界 → 第二宿主或如实标注 → 升级卸载。核心纪律是"观察到的才算数"——无法暴露的字段标 unverified，而不是从流利回复推断。

## 产出物

本课产出 `skill-release-gate`：一个完整的毕业 bundle，含 `SKILL.md`、一份参考文件、一个只读评测脚本、宿主 fixture、标注触发案例集和一个产物契约。在本地克隆内任意位置，解析仓库根目录，对绝对目标 bundle 运行安装版或源码版评估器，在不宣称发布的前提下验证随附的教学 fixture。

生产路径：把所有 fixture 换成捕获值、重建保留的 manifest、通过独立的发布基础设施拿到 attestation 及其可信摘要，然后运行：

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
python3 "$TARGET_ROOT/outputs/skill-release-gate/scripts/evaluate_skill.py" \
  --attestation /trusted/release-attestation.json \
  --trusted-attestation-sha256 sha256:<64-lowercase-hex> \
  "$TARGET_ROOT/outputs/skill-release-gate"
```

只有六层门禁、本地证据完整性和外部信任锚全部通过，命令才成功退出。没有那个信任锚，重新标注并本地重算哈希的 fixture 依然是非生产的。

课程安装器会复制完整的 bundle 树。目录和网站指向它的 `SKILL.md` 入口，同时保留嵌套资源。这正是扁平单文件工件所缺失的具体可移植性测试。

## 练习题

1. 为一个你在用的 skill 编写十条正例、十条明确负例和十条近失案例。在改 description 之前先切分它们。
2. 跑一次五轮的基线与实验组对照。即使平均分改善，也报告每个任务的回退。
3. 增加一个需要人工判断的评分维度。先用五个样例校准，再当作门禁使用。
4. 增加一项宿主能力，并定义"支持、适配、降级、不支持"四种结局。
5. 在 manifest 创建之后修改一个已安装的引用。证明包校验在激活之前失败。
6. 创建一个正文通过 lint 但脚本违反产物契约的 skill。指出哪一层发布门禁拦下它。
7. 增加一个升级评测：比较两个包版本之间的调用策略与必需能力。
8. 发布一份兼容性报告：写明测试过的宿主版本、日期、回退方式和未验证行为，全程不使用任何"portable"徽章。

## 关键术语

| 术语 | 人们说 | 实际含义 |
|---|---|---|
| 触发评测（Trigger eval） | "skill 触发了吗？" | 在路由边界上对选择、弃权与混淆的标注度量 |
| 行为评测（Behavior eval） | "它好用吗？" | 对照产物、质量、范围与效率契约度量的任务执行 |
| 基线（Baseline） | "不带 skill" | 对照条件下相同的模型、工具、任务和预算 |
| 产物契约（Artifact contract） | "预期输出" | 完成所需的、可独立校验的属性 |
| 能力矩阵（Capability matrix） | "支持的运行时" | 逐宿主记录原生支持、适配器、降级与不兼容 |
| 发布门禁（Release gate） | "全部测试通过" | 按层设阈值，阻断包而不隐藏失败类别 |
| 静默降级（Silent degradation） | "被忽略的元数据" | 宿主丢失必需行为却不警告安装者或用户 |

## 延伸阅读

- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)：触发评测、输出评测、重复运行与基线的官方做法。
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)：连贯的范围与资源架构最佳实践。
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)：确定性辅助脚本与结构化接口。
- [Client implementation guide](https://agentskills.io/client-implementation/adding-skills-support)：宿主侧的发现、激活、上下文、信任与生命周期行为。
- [GitSkills: A Dataset of Agent Skills from GitHub](https://arxiv.org/abs/2608.10906)：生态级规模数据集及其声明的度量边界——规模不等于质量。
