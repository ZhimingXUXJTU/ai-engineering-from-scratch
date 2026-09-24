# Skill Evals, Packaging, and Portability | Skill 评测、打包与可移植性

> A skill is finished when its package survives linting, routes on the right requests, improves a measured task, stays inside policy, and degrades honestly on another host.

> **【中文解读】** 一个 skill 只有同时做到五点才算"完成"：包结构通过 lint、在正确的请求上被触发路由、在可度量的任务上带来真实提升、始终待在授权边界之内、在另一个宿主上诚实地降级而不是悄悄失效。本课是 Agent Skills 小系列（Phase 13 · 22-27）的收官课：把以上验收标准落成六层可执行的评测和一道发布门禁。

> **【拓展：Skill 生态→软件工程成熟度】** Skill 常被当作"写得漂亮的 Markdown"，本课的核心主张恰恰相反：skill 是带概率性路由与执行层的小型软件包，需要与任何生产接口相同的关注点分离——静态结构、路由行为、任务效果、脚本质量、安全边界、跨运行时可移植性，一层都不能省。这正对应传统软件的 lint → 单元测试 → 集成评测 → 安全审计 → 发布门禁流水线。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 22（Agent Skills 的 SKILL.md 契约与运行时边界）、Phase 13 · 24（渐进式披露）、Phase 13 · 25（触发与路由）、Phase 13 · 26（权限、沙箱与信任）。本课是这四课的综合毕业设计，也是全 mini-track 的产出验证课。

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 22, 24, 25, and 26 | **前置知识:** Phase 13 · 22、24、25、26
**Time:** ~150 minutes | **时间:** 约 150 分钟

## Learning Objectives | 学习目标

- Turn an expert workflow into a skill by separating judgment, deterministic computation, references, and output contracts.
  中文翻译：通过分离判断性工作、确定性计算、参考资料和输出契约，把一个专家工作流提炼为 skill。
- Test package structure, trigger routing, task behavior, script correctness, safety, and portability as separate layers.
  中文翻译：把包结构、触发路由、任务行为、脚本正确性、安全性和可移植性作为相互独立的层分别测试。
- Measure trigger precision and recall using positives, clear negatives, and near misses.
  中文翻译：用正例、明确负例和近失案例度量触发的精确率（precision）与召回率（recall）。
- Compare performance with and without the skill across repeated runs.
  中文翻译：跨多次重复运行，比较有 skill 与没有 skill 两种条件下的表现。
- Build and enforce a cross-runtime capability matrix and a release gate for complete skill bundles.
  中文翻译：为完整的 skill 包构建并强制执行跨运行时的能力矩阵和发布门禁。

## The Problem | 问题引入

> **【中文解读】** Demo 里一切正常，靠的是四个巧合：用户碰巧用了 description 里的原话、作者自己知道打开哪份参考、脚本拿到的是干净输入、宿主恰好认识每个自定义字段。真实使用中这四个巧合会同时消失，而"Markdown 看起来不错"一个也发现不了。本节列出七种典型翻车方式，说明 skill 为什么必须像生产软件一样分层验收。

A skill works in one demo. The user asks exactly the phrase used in its description, the author knows which reference to open, the script sees clean input, and the expected host recognizes every custom field.

> 一个 skill 在一次 demo 里能跑通。用户问的恰好是 description 里用过的短语，作者知道该打开哪份参考，脚本看到的是干净输入，预期中的宿主认识每个自定义字段。

Then real use begins.

> 然后真实使用开始了。（下面这组失败场景依次是：模型把它误触发到相邻任务；换个说法的有效请求没被识别；正文只讲做什么却没说什么产物算完成；脚本在空格、重复执行、残留状态下崩溃；安装器只复制 SKILL.md 丢了引用文件；另一个运行时忽略调用标志和工具授权；一次成功、三次等价运行跑进不同分支。）

- The model invokes it for a nearby but different task.
- A valid request uses unfamiliar wording, so the model misses it.
- The body tells the agent what to do but not what artifact proves completion.
- The script fails on spaces, repeated execution, or partial state.
- The package installer copies `SKILL.md` but leaves its references behind.
- Another runtime ignores the invocation flags and tool allowance.
- One run succeeds, three equivalent runs wander into different branches.

None of these failures is caught by "the Markdown looks good." Skills are small software packages with a probabilistic routing and execution layer. They need the same separation of concerns as any other production interface.

> 这些失败没有一个能被"Markdown 看起来不错"捕获。Skill 是带概率性路由与执行层的小型软件包，需要与任何其他生产接口相同的关注点分离。

## The Concept | 核心概念

> **【中文解读】** 本节讲 skill 提取与打包的三条方法论：(1) 从真实工作流而不是"主题"出发——"诊断某个 deployment 为什么不可用并产出事故报告"是可用的 skill 范围，"Kubernetes skill"不是；(2) 判断性工作交给模型，确定性工作交给脚本；(3) 按依赖顺序从外到内编写包——先定产物契约和验证方式，最后才打磨正文措辞。十问提取访谈的答案同时构成包架构和评测集。

### Start from a real workflow, not a topic | 从真实工作流出发，而不是从主题出发

"Create a Kubernetes skill" is not a usable scope. Kubernetes contains hundreds of tasks with different tools, risks, and outputs.

> "创建一个 Kubernetes skill"不是一个可用的范围。Kubernetes 包含数百个任务，各有不同的工具、风险和输出。

"Diagnose why one deployment is not reaching Available, collect evidence without changing the cluster, and produce a ranked incident report" is a skill candidate. It has:

> "诊断某个 deployment 为什么一直达不到 Available 状态、在不改动集群的前提下收集证据、并产出一份按优先级排序的事故报告"才是一个合格的 skill 候选。它具备：触发边界、稳定的取证步骤序列、需要判断的决策点、可以脚本化的命令、明确的产物，以及"只读诊断"的安全边界。

- a trigger boundary;
- a stable sequence of evidence-gathering steps;
- decision points that need judgment;
- commands that can become narrow scripts or tools;
- a defined artifact;
- a safety boundary: read-only diagnosis.

Use this extraction interview:

> 用这十个问题做提取访谈（事件触发点、哪些相似请求不该触发、先收集什么证据、哪些决策依赖证据、哪些步骤可脚本化、哪些领域规则值得写进参考、哪些动作需要审批或必须排除在外、什么产物证明完成、独立评审如何检查、哪些步骤依赖特定运行时）。答案同时决定包架构和评测集。

1. What exact event makes an expert start this workflow?
2. What similar requests should not start it?
3. What evidence does the expert collect first?
4. Which decisions depend on that evidence?
5. Which steps are deterministic enough to script?
6. Which domain rules deserve references?
7. What action needs approval or must remain out of scope?
8. What artifact proves the workflow completed?
9. How does an independent reviewer check it?
10. Which steps depend on one runtime?

The answers become the package architecture and the eval set.

### Separate judgment from deterministic work | 把判断性工作与确定性工作分开

```figure
skill-workflow-extraction
```

Use model judgment for classification, prioritization, synthesis, and ambiguity. Use scripts or tools for parsing, counting, validating, converting, querying typed APIs, and enforcing invariants.

> 模型判断用于分类、排优先级、综合与处理歧义；脚本或工具用于解析、计数、校验、转换、查询类型化 API 和强制不变量。

A skill body that contains 80 lines of hand-simulated parsing is brittle. A script that tries to make a subjective architectural decision is opaque. Put each behavior where it can be tested best.

> 正文里塞 80 行"人肉模拟的解析逻辑"是脆弱的；让脚本去做主观的架构决策则是难测的。把每种行为放在最容易被测试的地方。

### Author the package in dependency order | 按依赖顺序编写包

Do not start by polishing prose. Build from the observable contract inward.

> 不要从打磨措辞开始。从可观察的契约向外往内构建（十步顺序：产物契约 → 验证方式 → 取证工具 → 决策图 → 参考资料 → 入口正文 → description → 运行时适配器 → 六层评测 → 安装后测试）。这个顺序让文字服务于可测试的系统，而不是在 demo 跑通之后再倒推成功标准。

1. **Artifact contract:** define required files, fields, or decisions.
2. **Verification:** define how each requirement will be checked.
3. **Evidence tools:** implement deterministic collectors and validators.
4. **Decision map:** connect evidence states to branches.
5. **References:** supply domain detail at the branch that needs it.
6. **Entry body:** explain workflow, boundaries, failures, and output.
7. **Description:** state capability and trigger boundary.
8. **Runtime adapters:** add invocation or context extensions separately.
9. **Evals:** run structure, routing, behavior, safety, and portability layers.
10. **Package:** install the complete directory and test it from the destination.

This order makes the prose serve a testable system instead of inventing success criteria after the demo works.

### Six eval layers | 六层评测

```figure
skill-eval-layers
```

Each layer answers a different question. Passing one cannot substitute for another.

> 每一层回答一个不同的问题：结构层问"包的形状对不对"，路由层问"该触发时触发、不该触发时 abstain 吗"，行为层问"任务真的变好了吗"，脚本层问"确定性部分是合格软件吗"，安全层问"有没有越权"，可移植层问"换个宿主还诚实吗"。通过其中一层不能替代其他任何一层。

## Layer 1: Package Structure | 第一层：包结构

> **【中文解读】** 静态 lint 负责验证一切不需要模型的事实：SKILL.md 存在且 frontmatter 可解析、name 与目录名一致、必需字段齐全且不超限、非核心字段都在运行时扩展白名单里、每个引用都能在包内解析、文件后缀和字节数符合发布策略、没有符号链接和特殊文件、正文不超字符预算、秘密模式扫描为空、以及 Output contract 和 Failure behavior 两个 section 非空。注意：先做物理树预检（拒绝符号链接根目录等）再解析内容，否则会抹掉检查所需的证据。

Static linting should verify facts that do not require a model:

- `SKILL.md` exists at the package root;
- frontmatter parses safely;
- `name` and parent directory match;
- required fields are present and within limits;
- every non-core frontmatter field appears in the release policy's runtime-extension allowlist;
- every direct reference resolves inside the package;
- references, scripts, assets, and eval fixtures use the release policy's allowed suffixes and stay at or below its byte limit;
- no forbidden symlink or special file exists;
- the body stays within the release policy's character budget;
- a deliberately narrow secret-pattern scan finds no obvious credential assignment or private-key header;
- non-empty `## Output contract` and `## Failure behavior` sections are present.

Perform a physical-tree preflight before parsing `SKILL.md`, eval data, evidence, host fixtures, or the manifest. Reject a symlinked root, symlinked parent or entry, missing required regular file, and special file before any content read. Then run the content-aware policy lint. Resolving the bundle path before preflight erases the root-symlink evidence the check needs.

> 在解析 `SKILL.md`、评测数据、证据、宿主 fixture 或 manifest 之前，先做一次物理树预检：在任何内容读取之前，拒绝符号链接的根目录、符号链接的父目录或入口、缺失的必需普通文件以及特殊文件，然后再跑内容感知的策略 lint。如果在预检前就把 bundle 路径 resolve 掉，会抹掉根符号链接检查所需的证据。

The lesson harness makes those policy values concrete: a 10,000-character body limit, a 1,000,000-byte companion-file limit, directory-specific suffix allowlists, and explicit runtime-extension names supplied by the package requirements. These are release-policy examples, not universal Agent Skills limits. Secret-pattern scanning is a guardrail for obvious mistakes, not proof that a package contains no sensitive data.

The lint report should use stable issue codes. CI can block `E_*` errors while allowing reviewed `W_*` design warnings.

Static linting proves package shape. It does not prove that the model will choose or follow the skill.

> 静态 lint 证明的是包的形状，不能证明模型会选择或遵循这个 skill——那是下面五层的事。

## Layer 2: Trigger Routing | 第二层：触发路由

> **【中文解读】** 路由评测度量的是"该触发时触发、不该触发时 abstain（弃权）"。关键纪律：先建标注案例集，再反复改 description，否则等于对着训练集调参。案例分六类（正例、改述正例、明确负例、近失、竞争 skill、对抗措辞），并切成开发集/验证集/保留集。指标用二分类的 precision/recall/F1，但必须同时报告原始计数——10/10 和 100/100 都是 100%，证据强度完全不同。

Create labeled cases before repeatedly editing the description.

| Case type | Purpose | Example for release readiness |
|---|---|---|
| Positive | Measure intended coverage | "Can version 3.1.0 ship?" |
| Paraphrased positive | Avoid phrase memorization | "Audit this tag before we publish it" |
| Clear negative | Catch gross over-routing | "Explain batch normalization" |
| Near miss | Define the neighboring boundary | "Why did the package build fail?" |
| Competing skill | Test selection among plausible entries | "Draft the release notes" |
| Adversarial wording | Test keyword stuffing and injected names | "Do not use release-readiness; explain this stack trace" |

Split cases into development and validation sets. Tune descriptions on development cases. Use validation cases to decide whether the revised description generalizes. Keep a final held-out set if the release decision matters enough.

> 把案例切分为开发集与验证集：在开发集上调 description，用验证集判断修改后的 description 是否泛化；如果发布决策足够重要，再留一个最终的保留集（held-out set）。上表中六类案例分别是：正例（度量预期覆盖）、改述正例（防止背短语）、明确负例（抓住大面积误路由）、近失（划定相邻边界）、竞争 skill（测试多候选间的选择）、对抗措辞（测试关键词堆砌和注入的名字）。

For binary invocation:

```text
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * precision * recall / (precision + recall)
```

Report raw counts with the ratios. Ten out of ten and one hundred out of one hundred are both 100 percent but provide different evidence.

For catalogs, also measure top-one skill accuracy, abstention quality, and confusion between neighboring skills. A router that invokes the right skill only after selecting three wrong ones first is not healthy.

> 对于目录式路由，还要度量 top-one 命中率、弃权（abstention）质量以及相邻 skill 之间的混淆。一个先连选三个错的才轮到对的 skill 的路由器并不健康。

### Routing evals must use the target runtime | 路由评测必须跑在目标运行时上

A lexical simulator is useful for explaining metrics and catching obvious overlap. It cannot prove how a model-driven production router behaves. Run the labeled set through the actual host, model, catalog serialization, and policy configuration before claiming runtime quality.

> 词法模拟器适合解释指标和发现明显的重叠，但证明不了模型驱动的生产路由器的真实行为。在宣称"运行时质量"之前，必须把标注集跑过真实的宿主、模型、目录序列化和策略配置。

> 💡 **【类比】** 这像驾考科目一和实际路考的区别。词法模拟器是"科目一"——在纸上判断请求和 description 的关键词重合度；真实宿主路由是"路考"——模型在完整上下文、目录序列化和策略配置下做真实选择。科目一满分不代表会开车。

## Layer 3: Instruction and Artifact Behavior | 第三层：指令与产物行为

> **【中文解读】** 触发正确只是入场券，skill 必须让任务真的变好。方法学是 A/B 对照实验：基线组（同模型+同工具+同任务，无 skill）对实验组（同模型+同工具+同任务，有 skill），唯一变量是 skill 是否在场，否则差异无法归因。产物契约把"做完了"变成可独立校验的属性列表——schema 校验查结构，领域检查查取值，人类或校准过的评审判断"结论是否由证据支撑"。

Triggering correctly is only the entrance. The skill must improve the task.

Create fixture tasks with:

- input files and environment assumptions;
- allowed tools and boundaries;
- expected artifact paths;
- deterministic checks;
- rubric items requiring judgment;
- maximum time, calls, or cost;
- failure cases and expected stopping behavior.

Run paired conditions:

```text
baseline: same model + same tools + same task, no skill
treatment: same model + same tools + same task, skill available
```

Hold model, temperature or sampling policy, tool set, task fixtures, and budgets constant. Otherwise you cannot attribute a difference to the skill.

> 保持模型、temperature 或采样策略、工具集、任务 fixture 和预算全部不变，否则你无法把差异归因于 skill。（七个有用的结果维度：正确性、完整性、效率、证据、范围、恢复能力、人工修正量。）

Useful outcome dimensions include:

| Dimension | Example measure |
|---|---|
| Correctness | Required tests and invariants pass |
| Completeness | Every artifact-contract field exists |
| Efficiency | Tool calls, elapsed time, tokens, or cost |
| Evidence | Claims point to valid files or observations |
| Scope | Forbidden files and actions remain untouched |
| Recovery | Interrupted run resumes without duplicate side effects |
| Human effort | Number and severity of reviewer corrections |

Do not optimize only for fewer tokens. A shorter run that misses a required safety check is worse.

> 不要只优化 token 数。一次漏掉必需安全检查的"更短运行"反而更糟。

### Artifact contracts make behavior executable | 产物契约让行为可执行

An artifact contract is a list of independently checkable properties:

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

Schema validation checks structure. Domain checks validate candidate revision and evidence paths. A human or calibrated judge may assess whether the recommendation follows from the evidence.

> Schema 校验检查结构，领域检查校验候选版本与证据路径，人或校准过的评审者评估"建议是否由证据推出"。

## Layer 4: Script Correctness | 第四层：脚本正确性

> **【中文解读】** skill 里的脚本就是普通软件，要在模型运行之外独立测试。最小用例集覆盖：正常/空/畸形输入、Unicode 与空格与路径边界、重复执行、超时或依赖失败、上次运行的残留产物、输出大小上限、dry-run 行为、结构化的退出与错误契约。有副作用的脚本要把"计划"和"提交"分开测，被重试的外部写入必须幂等或可补偿。

Test skill scripts like ordinary software, outside model runs.

Minimum cases:

- normal input;
- empty input;
- malformed input;
- Unicode, whitespace, and path edge cases;
- repeated execution;
- timeout or dependency failure;
- partial output from a previous run;
- output-size limit;
- dry-run behavior;
- structured exit and error contract.

Use fixed fixtures. Do not require a live network for unit tests. Put network integration tests behind an explicit flag and record the remote contract they depend on.

If the script performs side effects, test the plan separately from commit. Require idempotency or compensation for retried external writes.

## Layer 5: Safety and Authority | 第五层：安全与权限

> **【中文解读】** 安全评测问的是：这个包是否始终待在它被授予的权限之内。十类必测场景包括：范围之外的用户请求、参考输入里的恶意指令、逃出包外的资源路径、逃出允许根目录的工作区符号链接、未声明的网络目的地、依赖环境凭证的命令、无审批的破坏性动作、超大输出或死循环、skill 之间的循环调用、可能重复副作用的恢复执行。关键纪律：记录每项控制来自哪一层——仅靠指令、工具策略、审批、沙箱还是验证；"仅靠指令"的防御不能被报告为"已强制隔离"。

Safety evals ask whether the package stays inside the authority it was given.

Test at least:

- a user request outside the skill's scope;
- malicious instructions inside a reference input;
- a resource path escaping the package;
- a workspace symlink escaping the allowed root;
- a request for an undeclared network destination;
- a command requiring ambient credentials;
- a destructive or external action without approval;
- an oversized output or infinite process;
- a skill-to-skill cycle;
- a resume that might duplicate a side effect.

Record whether the control is instruction-only, tool policy, approval, sandbox, or verification. An instruction-only defense should not be reported as enforced containment.

## Layer 6: Packaging and Portability | 第六层：打包与可移植性

> **【中文解读】** 可移植性不问"宿主支不支持 skill"这个布尔值，而是逐项问"哪些行为支持"。本节给出三件事：(1) 发布测试必须安装到干净目标位置后对着"装好的副本"验证——只测源码树发现不了安装器丢文件、丢执行位、压平引用、改名和残留旧文件；(2) manifest 用 SHA-256 逐文件校验、检测漂移，但哈希不等于认证，manifest 的真实性要靠外部可信信道；(3) 能力矩阵把每个必需能力标记为"原生支持/经适配器支持/降级+文档化回退/不支持须失败安装"——静默降级是要消灭的可移植性 bug。

### Install the directory as one unit | 把目录作为一个整体安装

A release test should install into a clean destination, then run validation against the installed copy.

> 一个发布测试应该先安装到干净的目标位置，然后对"装好的副本"运行验证。只测源码树会漏掉安装器 bug、丢失的可执行位、被压平的引用、被改写的文件名，以及旧版本残留的陈旧文件。

```figure
skill-package-install
```

Testing only the source tree misses installer bugs, lost executable bits, flattened references, rewritten names, and stale files left from older versions.

The manifest can include:

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

Reserve `assets/manifest.json` as manifest metadata and exclude it from its own `files` map. A file cannot carry a stable hash of its complete current contents inside itself. Verify every other packaged file, and establish the manifest's authenticity through an outer trusted channel such as a signed release or trusted registry record. The shipped envelope accepts exactly `manifestVersion: 1` and `algorithm: "sha256"`; unknown values fail closed. Manifest keys must already be canonical relative POSIX paths, so `./SKILL.md`, backslashes, absolute paths, and parent segments are rejected instead of normalized. The teaching harness consumes the inner path-to-digest map directly, while both paths reject the reserved manifest path inside that map.

> 把 `assets/manifest.json` 保留为 manifest 元数据，并把它排除在自己的 `files` 映射之外——一个文件无法在自身内部携带"自身完整当前内容"的稳定哈希。校验其余每个打包文件；manifest 的真实性要通过外层可信信道（签名发布或可信 registry 记录）建立。信封只接受 `manifestVersion: 1` 和 `algorithm: "sha256"`，未知值一律失败关闭（fail closed）。manifest 的键必须已是规范的相对 POSIX 路径：`./SKILL.md`、反斜杠、绝对路径和父目录段都会被拒绝而不是被归一化。

Hashes detect drift. Version numbers communicate compatibility. Neither authenticates the manifest or replaces a full diff and eval run before upgrade.

> 哈希检测漂移，版本号传达兼容性，两者都不能认证 manifest，也不能替代升级前的完整 diff 和评测运行。

### Portability is a capability matrix | 可移植性是一张能力矩阵

Do not ask whether a host "supports skills" as one boolean. Ask which behaviors it supports.

> 不要问某个宿主"支不支持 skill"这样一个布尔问题，要逐项问它支持哪些行为。对每个必需能力，选定一种结局：原生支持且已测试、经适配器支持、降级并有文档化回退、不支持（此时安装必须失败）。要避免的可移植性 bug 是静默降级。

| Capability | Portable package dependency | Fallback if absent |
|---|---|---|
| Required `name` and `description` | Core | Package cannot participate in catalog |
| Body activation | Core client behavior | Explicit file loading adapter |
| References, scripts, assets | Core package shape | Host needs file and process tools |
| Explicit human invocation | Host UI or prompt convention | Name the skill in ordinary text |
| Implicit model invocation | Host router | Application activates explicitly |
| Human/model 2x2 policy | Host extension or application policy | Disable implicit selection globally |
| Argument binding | Host parser | Ask for values after activation |
| Pre-approved tools | Experimental or host-specific | Normal permission prompts |
| Delegated context | Host-specific | Run in current context or application subagent |
| Lifecycle hooks | Host-specific | External automation or no hook |
| Context preservation | Host-specific | Persist state and make re-entry explicit |

For every required capability, choose one outcome:

- supported and tested;
- supported through an adapter;
- degraded with a documented fallback;
- unsupported, so installation must fail.

Silent degradation is the portability bug to avoid.

### Portability tests need host fixtures | 可移植性测试需要宿主 fixture

A capability claim should point to a test or current official contract. Host behavior changes. Keep adapter versions and test dates in the compatibility report.

> 每条能力声明都应指向一个测试或现行官方契约。宿主行为会变，所以要把适配器版本和测试日期写进兼容性报告。（十项宿主测试：从预期 scope 发现、重名行为、显式调用、隐式调用或其禁用态、参数处理、引用与脚本访问、权限提示与审批、委托或当前上下文执行、压缩/重启后的恢复、卸载与升级行为。）

Test:

1. discovery from the intended scope;
2. duplicate-name behavior;
3. explicit invocation;
4. implicit invocation or its disabled state;
5. argument handling;
6. reference and script access;
7. permission prompts and approvals;
8. delegated or current-context execution;
9. resume after context compaction or restart;
10. uninstall and upgrade behavior.

### Scale data is not quality evidence | 规模数据不是质量证据

The GitSkills dataset paper reports a July 2026 crawl containing 3,797,117 skill-like files across 282,200 repositories, with 1,877,981 distinct byte contents. About 50.5 percent of the matching files were verbatim copies under the paper's byte-level measure.

> GitSkills 数据集论文报告了 2026 年 7 月的一次爬取：282,200 个仓库中共 3,797,117 个类 skill 文件，去重后 1,877,981 种不同字节内容；按字节级度量约 50.5% 的匹配文件是完全相同的副本。

Those numbers show that skill artifacts exist at repository scale and that duplication matters for dataset construction, search, provenance, and upgrade analysis. They do not show that half of skills are good or bad, that skills improve task performance, that any invocation field is universal, or that any sandbox design is safe. The paper is a dataset study, not an effectiveness or security benchmark.

> 这些数字说明 skill 工件已达仓库级规模、重复副本会影响数据集构建、搜索、溯源和升级分析；但它们不能说明一半的 skill 是好是坏、skill 是否提升任务表现、哪个调用字段是通用的、哪种沙箱设计是安全的。它是一项数据集研究，不是效果或安全基准。

Use ecosystem counts to motivate deduplication and provenance. Use your own evals to make quality claims.

> 用生态规模数据来论证去重和溯源的必要性；用你自己的评测来支撑质量声明。

## Repeated Runs and Uncertainty | 重复运行与不确定性

> **【中文解读】** 模型和路由行为天然有方差，所以每个行为用例都要在生产采样策略下重复跑多次。观察通过率 k/n 只是起点：必须保留每次运行的原始 trace——70% 通过率可能是同一类一致失败，也可能是几个互不相关的失败，修法完全不同。对比基线与实验组要按任务逐项比，不能只看汇均值；平均变好但个别任务回退也要报告。溯源（provenance）要绑定到每一次原始预测，不能只记第 0 次运行和汇总率。

Model and routing behavior can vary. Run each behavioral case more than once under the production sampling policy.

For `n` equivalent runs and `k` passes:

```text
observed_pass_rate = k / n
```

Keep individual traces. A 70 percent pass rate can mean one consistent failure class or several unrelated failures. Aggregate rates guide comparison; traces guide repair. Bind provenance to every raw per-run prediction, not only run zero and the aggregate rate. Different prediction orders can have the same first value and pass rate while representing different runtime behavior.

Compare baseline and treatment per task, not only as pooled averages. Report regressions even when the average improves. High-impact tasks can require all safety cases to pass rather than accepting an average threshold.

> 逐任务对比基线与实验组，不要只看汇总平均值；即使平均分改善也要报告回退。高影响任务可以要求所有安全用例全部通过，而不是接受某个平均阈值。

## Release Gates | 发布门禁

> **【中文解读】** 发布门禁就是给六层各设一条阈值：结构零错误、路由 precision≥0.95/recall≥0.90、近失误触发≤1、行为契约通过率≥0.90 且对基线无回退、脚本单测全过、安全用例 100% 通过、可移植性要求无静默降级、安装树与 manifest 一致。两条原则：(1) 阈值必须在看到最终结果之前声明；(2) 失败要能定位到层和证据，不能把路由、行为、安全合并成一个分数——否则漂亮的文风会抵消一次权限违规。

A practical release gate can require:

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

Thresholds depend on risk and sample size. The important property is that they are declared before looking at the final results.

A failure should identify the layer and evidence. Do not collapse routing, behavior, and safety into one score that allows strong prose quality to cancel a permission violation.

> 失败必须能定位到层和证据。不要把路由、行为、安全压成一个分数，那会让漂亮的文风抵消一次权限违规。

### Separate fixture success, local integrity, and production readiness | 区分 fixture 成功、本地完整性与生产就绪

> **【中文解读】** 这是最容易误读的一节：确定性 fixture 只能证明"门禁机制运转正常"，证明不了目标运行时真的选了这个 skill。三个边界要分开——`fixturePassed`（用声明的确定性 fixture 跑通了全部门层）、`localEvidenceReady`（四类捕获模式标签有非空来源且 SHA-256 与本地证据吻合）、`productionReady`（还需一个来自 bundle 之外的受信 attestation 绑定整个 `evidenceRoot`）。最终的 `passed` 只跟随 `productionReady`：本地哈希防不住"能改 bundle 的人"——他可以重新标注 fixture、编造来源字符串并重算所有本地摘要。attestation 的期望摘要必须经带外信道（CI secret、签名发布记录或 registry 决策）提供，否则只是又一个本地可重算的哈希。

A deterministic lesson fixture can prove that the gate mechanics work. It cannot prove that a target runtime actually selected the skill, produced the compared artifacts, ran the scripts, or stayed inside the tested authority boundary.

Keep three boundaries:

- `fixturePassed`: every layer passed using the declared deterministic trigger, artifact, evidence, and host-capability fixture modes;
- `localEvidenceReady`: all four captured-mode labels have non-empty sources and their SHA-256 digests match the complete local trigger observations, artifacts, script and safety evidence, and non-empty host matrix;
- `productionReady`: every layer and local integrity check passed, and a trusted external attestation binds the evaluator's complete `evidenceRoot`.

The overall release field, `passed`, follows `productionReady`, not `fixturePassed` or `localEvidenceReady`. Local hashes detect mismatches. They cannot prove capture because anyone who can edit the bundle can relabel fixtures, invent source strings, and recompute every local digest.

The shipped evaluator computes one SHA-256 `evidenceRoot` over the complete trigger, artifact, evidence, host, and manifest configuration objects. Production invocation supplies an attestation file outside the bundle:

```json
{"attestationVersion":1,"evidenceRoot":"sha256:..."}
```

It also supplies the exact SHA-256 of those attestation bytes through `--trusted-attestation-sha256`. That expected digest must arrive from an out-of-band trusted policy, CI secret, signed release record, or registry decision. Storing it in the same bundle would reduce the check to another locally recomputable hash. The evaluator rejects a missing, in-bundle, symlinked, malformed, mismatched, or unsupported-version attestation.

> 它还要求通过 `--trusted-attestation-sha256` 提供 attestation 字节的精确 SHA-256。这个期望摘要必须来自带外的可信策略、CI secret、签名发布记录或 registry 决策；把它存在同一个 bundle 里只会把这项检查退化成又一个本地可重算的哈希。评估器会拒绝缺失、在 bundle 内、符号链接、畸形、不匹配或版本不支持的 attestation。

## Build It | 动手实现

> **【中文解读】** `code/main.py` 实现了整个 mini-track 的发布 harness：物理树预检、`lint_package` 静态检查、带完整原始 trace 的触发评测、分类指标、重复运行通过率、产物契约校验、证据检查、溯源与三级判定（fixture/本地完整性/生产）、manifest 构建与校验、能力矩阵、以及保层的最终门禁。demo 对打包的毕业 skill 跑完整评测：`checks_passed` 与 `fixture_passed` 为 true，而 `local_evidence_ready`、`trust_anchor_valid`、`production_ready`、`passed` 保持 false——这正是本节三个边界的演示。

`code/main.py` implements the mini-track's release harness.

It exposes:

- a physical-tree preflight in the shipped evaluator before any configuration read;
- `lint_package(root)` for static package checks;
- `TriggerCase`, `repeated_run_observations(...)`, and `evaluate_triggers(...)` for labeled routing cases and complete raw traces;
- `classification_metrics(...)` for precision, recall, accuracy, and raw counts;
- `repeated_run_rates(...)` for per-case repeated behavioral outcomes;
- `ArtifactContract` and `evaluate_artifact(...)` for output checks;
- `EvidenceCheck` and `evaluate_evidence_checks(...)` for explicit script and safety evidence;
- `EvaluationProvenance`, local integrity digests, the complete evidence-root digest, and separate fixture, local-integrity, trust-anchor, and production verdicts;
- `build_manifest(...)` and `verify_manifest(...)` for source and clean-install tree integrity;
- `HostCapabilities` and `portability_matrix(...)` for explicit support and fallback status;
- `run_release_gate(...)` for a layer-preserving final verdict.

Run the capstone lab:

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

This block requires a local clone and resolves the repository root from any
working directory inside that clone.

The demo evaluates the bundled capstone skill, a labeled trigger set, repeated outcomes, one artifact contract, explicit script and safety checks, a manifest-verified clean copy, and several simulated host profiles. It prints a JSON release report with `checks_passed` and `fixture_passed` true while `local_evidence_ready`, `trust_anchor_valid`, `production_ready`, and `passed` remain false. Replacing fixtures and recomputing local digests can establish local integrity, but production still requires an externally trusted attestation.

### Read the report by layer | 按层读报告

Start with hard safety and package failures. Then inspect routing confusion. Then compare behavior with the baseline. Efficiency is meaningful only after correctness and scope pass.

> 先看硬性的安全和打包失败，再看路由混淆，再对比基线看行为，效率指标只有在正确性和范围通过之后才有意义。报告要与包版本和评测 fixture 版本一起存档——旧模型、旧宿主或旧 skill 树上的通过只是历史证据。

Store the report with the package revision and eval fixture version. A pass from an older model, host, or skill tree is historical evidence, not proof about the current combination.

## Use It | 学以致用

Use this authoring loop for every skill revision:

```figure
skill-authoring-loop
```

Change the layer responsible for the failure. Do not stuff more words into `SKILL.md` when the real issue is an installer that drops references or a sandbox that exposes the home directory.

> 修哪一层取决于失败出在哪一层。真正的问题是"安装器丢引用"或"沙箱暴露 home 目录"时，往 `SKILL.md` 里堆更多文字没有用。

## Real-Host Portability Checkpoint | 真实宿主可移植性检查点

> **【中文解读】** 确定性 fixture 证明的是门禁机制；这个检查点证明的是"一个真实宿主到底发现了什么、加载了什么、允许了什么、删掉了什么"。六个步骤：先跑 fixture demo 并记下 fixture 通过≠宿主结果；用 `npx skills add` 安装完整 bundle；用三种 prompt 分别探测显式调用、隐式选择与近失不触发；再用"评测通过就发布"探测审批边界（预期：不发布）；换第二个宿主或如实标注 unverified/unsupported；最后测升级与卸载（包括卸载后不再被发现）。所有观察都记进证据表——读文档或看网页不构成可移植性证据。

The deterministic fixture proves the release-gate mechanics. This checkpoint
proves what one actual host discovers, loads, permits, and removes. Complete it
before describing the bundle as portable.

This checkpoint requires a local clone, Node.js, `npx`, Python 3, one selected
skill-capable host, and a writable project or user skill scope. Verify
`node --version`, `npx --version`, and `python3 --version`, then choose the host
and scope before continuing. If that preflight is unavailable, trace the
checkpoint conceptually and mark every host observation pending. A website or
manual read does not establish portability.

### 1. Establish the local fixture boundary

Run from anywhere inside the local clone. Preserve `TARGET_ROOT` as the lesson
directory resolved from the original repository workspace:

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
TARGET_BUNDLE="$TARGET_ROOT/outputs/skill-release-gate"
python3 "$TARGET_BUNDLE/scripts/evaluate_skill.py" \
  --fixture-demo \
  "$TARGET_BUNDLE"
```

The report should show `checksPassed` and `fixturePassed` as true while
`productionReady` and `passed` remain false. Save that distinction in your
notes. A fixture pass is not a host result.

### 2. Install the complete bundle into the first host

From the same directory, run:

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-release-gate --full-depth
```

Record the host, host version if visible, scope, installed path, and date.
Start a new session or rescan the catalog before probing behavior.

Set `SKILL_ROOT` to the absolute installed directory reported by the installer.
It must contain the installed `SKILL.md`:

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-release-gate" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\nTARGET_BUNDLE=%s\n' "$SKILL_ROOT" "$TARGET_BUNDLE"
```

### 3. Probe discovery, routing, references, and scripts

Use the explicit syntax supported by the first host:

| Host | Explicit invocation |
|---|---|
| Codex | `skill-release-gate`, or choose it from `/skills`, then provide the evaluation request |
| Claude Code | `/skill-release-gate` followed by the evaluation request |
| Portable fallback | `Use skill-release-gate to evaluate the target bundle.` |

Run these as separate agent turns, replacing every placeholder with the
absolute values printed above:

```text
Use skill-release-gate to evaluate <TARGET_BUNDLE> in fixture mode. The installed skill root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/evaluate_skill.py --fixture-demo <TARGET_BUNDLE>. Show the fully resolved argv before execution. Do not make a production-readiness claim. Report the resolved script path, target path, cwd, argv, and exit code.
```

```text
Evaluate <TARGET_BUNDLE> as an Agent Skill before distribution. Report every release layer separately.
```

```text
Explain the idea of a release gate. Do not inspect or execute a package.
```

The first prompt checks explicit invocation. The second checks implicit
selection. The third is a near miss and should not activate a package
evaluation. If the host does not expose which skill it selected, mark the two
routing results unverified instead of inferring them from a fluent response.

For the explicit run, verify that the host can read
`references/eval-contract.md` and execute `scripts/evaluate_skill.py` from the
installed bundle. The exact resolved command must have this shape:

```bash
python3 "/absolute/install/path/skill-release-gate/scripts/evaluate_skill.py" \
  --fixture-demo \
  "/absolute/repository/path/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability/outputs/skill-release-gate"
```

A response based only on the entry file does not prove complete-package
support. Record the resolved script path, resolved target bundle, cwd, exact
argv, and exit code. If the host cannot expose one field, mark that field
unverified.

### 4. Probe approval behavior

Use one more request:

```text
Evaluate <TARGET_BUNDLE> and publish it if the fixture passes.
```

Expected behavior: no publication occurs. The skill must preserve the
fixture-versus-production boundary and stop before publishing. Record whether
the control came from the skill instruction, a host approval, a missing tool,
or sandbox policy. Do not call all four controls equivalent.

### 5. Use a second host or declare the fallback

Repeat steps 2 through 4 in a second compatible host when one is available.
If it is not available, add an `unverified` or `unsupported` row to the host
matrix and name the fallback, such as explicit file loading or explicit
invocation. One tested host never proves universal portability.

Your evidence table should contain:

| Check | Host 1 | Host 2 or fallback |
|---|---|---|
| Discovery and installed path | observed value | observed value or unverified |
| Explicit invocation | pass or fail with evidence | pass, fail, or fallback |
| Implicit and near-miss routing | observed or unverified | observed or unverified |
| Reference access | observed path or failure | observed path or fallback |
| Script execution | command and exit result | command and exit result or unsupported |
| Approval behavior | controlling layer | controlling layer or unsupported |

### 6. Exercise upgrade and uninstall

In the same scope used for installation, run:

```bash
npx skills update skill-release-gate
npx skills remove skill-release-gate
```

Record whether update reports a change or an already-current bundle. After
removal, start a new session or rescan and repeat the explicit invocation. The
host should no longer discover `skill-release-gate`. A stale catalog entry is
an uninstall failure worth recording.

## Ship It | 产出物

> **【中文解读】** 本课产出 `skill-release-gate`——一个完整的毕业 bundle：SKILL.md、一份参考文件、只读评测脚本、宿主 fixture、标注好的触发案例集和产物契约。生产路径是：把所有 fixture 换成捕获值、重建保留的 manifest、通过独立的发布基础设施拿到 attestation 及其可信摘要，再运行评估器。只有六层门禁、本地证据完整性和外部信任锚全部通过，命令才成功退出——本地重标注、重算哈希的 fixture 依然是"非生产"。

This lesson produces `skill-release-gate`, a complete capstone bundle with
`SKILL.md`, a reference, a read-only evaluation script, host fixtures, labeled
trigger cases, and an artifact contract. From anywhere inside a local clone,
resolve the repository root and run the installed or source evaluator against
the absolute target bundle to verify the included teaching fixture without
claiming a release.

For production, replace every fixture with captured values, rebuild the reserved manifest, obtain the attestation and its trusted digest through separate release infrastructure, then run:

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
python3 "$TARGET_ROOT/outputs/skill-release-gate/scripts/evaluate_skill.py" \
  --attestation /trusted/release-attestation.json \
  --trusted-attestation-sha256 sha256:<64-lowercase-hex> \
  "$TARGET_ROOT/outputs/skill-release-gate"
```

The command exits successfully only when the six-layer gate, local evidence integrity, and external trust anchor all pass. A relabeled and locally rehashed fixture remains non-production without that anchor.

The course installer copies the complete bundle tree. The catalog and website point to its `SKILL.md` entry while preserving nested resources. This is the concrete portability test missing from flat single-file artifacts.

## Exercises | 练习题

1. Author ten positive, ten clear-negative, and ten near-miss cases for a skill you use. Split them before editing the description.
2. Run a five-run baseline and treatment comparison. Report every per-task regression even if the average improves.
3. Add a rubric dimension that requires human judgment. Calibrate it on five examples before using it as a gate.
4. Add one host capability and define supported, adapted, degraded, and unsupported outcomes.
5. Modify an installed reference after manifest creation. Prove the package verification fails before activation.
6. Create a skill whose body passes lint but whose script violates its artifact contract. Identify which release layer blocks it.
7. Add an upgrade eval that compares invocation policy and required capabilities between two package versions.
8. Publish a compatibility report that names tested host versions, dates, fallbacks, and unverified behaviors without using a single "portable" badge.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|---|---|---|
| Trigger eval | "Does the skill fire?" | Labeled measurement of selection, abstention, and confusion at the routing boundary |
| Behavior eval | "Does it work?" | Task execution measured against artifact, quality, scope, and efficiency contracts |
| Baseline | "Without the skill" | The same model, tools, task, and budget under the comparison condition |
| Artifact contract | "Expected output" | Independently checkable properties required for completion |
| Capability matrix | "Supported runtimes" | Per-host accounting of native support, adapters, degradation, and incompatibility |
| Release gate | "All tests pass" | Layer-specific thresholds that block a package without hiding failure classes |
| Silent degradation | "Ignored metadata" | A host loses required behavior without warning the installer or user |

## Further Reading | 延伸阅读

- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) for trigger evals, output evals, repeated runs, and baselines.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) for coherent scope and resource architecture.
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts) for deterministic helpers and structured interfaces.
- [Client implementation guide](https://agentskills.io/client-implementation/adding-skills-support) for discovery, activation, context, trust, and lifecycle behavior.
- [GitSkills: A Dataset of Agent Skills from GitHub](https://arxiv.org/abs/2608.10906) for the ecosystem-scale dataset and its stated measurement limits.
