# 作为自主代理:权限模式和自动模式
# 独立代理人的许可模式

> 允许梯度 从审查到批准的自主程度 是如何控制一个自主代理可以做的事情, 克劳德代码,这门课程的实践例子,揭示了六种这样的模式: "计划"在每一个操作之前询问, "默认" (UI中标记为"手册") 仅要求风险的模式, "接受编辑" 自动批准文件写,但仍然确认 Shell 执行, "绕过许可" 批准一切. 自动模式`auto`允许模式 取代每行动的批准,用一个单独的分类器模型来审查每项行动,然后在执行之前,并阻止任何超出请求的情况.`max_turns`其他`max_budget_usd`提供`auto`根据计划,组织启用,模型和提供商而成,

> **【中文解读】**克劳德码 暴露七个权限模式――"计划" 每动作前询问,"默认" 仅对危险动作询问,"接受编辑" 自动批准文件写入但仍确认 Shell 执行,"绕过许可" 批准一切――自动模式(2026年3月24日) 用两阶段并行安全分类器替代每动作审核: 每动作运行单代币 快速检查;标记动作发发思链深度审查――动作预算通过`max_turns`和 `max_budget_usd`实施──自动模式 作为研究预览发布人类 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**克劳德代码的七个模式本质是"自主阶梯":计划 →默认 →接受编辑 → ... →绕过许可证.每个模式是速度与每动作审查的不同权衡.

>  **【前置】**学本节前请先掌握:阶段15·01(长视线代理) 理解为什么长程代理 需要权限系统;阶段14·27(即时注射防御) 理解为什么代理 看到的内容不能全信――本节直接讲克劳德代码的实际权限模式,是最贴近日常使用的代理安全课――

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

> **【中文解读】**克劳德代码的权限模式是代理安全控制的典型案例. 四种模式: 1) 要求用户确认每次操作; 2) 编辑文件编辑自动批准,命令需确认; 3) 操作的所有操作自动批准; 4) 计划先规划后执行.

> **【拓展：claude code permission modes】**克劳德代码的权限设计体现了2026年编码的代理的安全最佳实践――关键原则: 1) 最小权限默认只授予必要权限; 2) 渐进授权用户可以根据信任逐步放宽限制; 3) 审计追踪所有操作都有日志; 4) 紧急停止随时可以中断――这些原则也适用于其他代理系统的设计――

您的机器上一个自主编码代理是个不同的安全类别.

> 机器上的自动编码代理是独特的安全类别.

攻击表面是代理可以访问的任何文件系统,网络,凭证,剪辑板,任何浏览器标签,任何开放终端. 布鲁斯·施奈尔和其他人公开指出:计算机使用代理不是聊天机器人的"功能更新",它们是一种新的工具,具有新的风险配置.

> 攻击面是代理能触及所有文件系统,网络,凭证,剪贴板,任何浏览器标签,任何开放的终端.

克劳德代码的许可系统是人类的答案. 而不是一个"自动/非自动"开关, 设有六种模式, 跨越一个能力梯度:计划 →默认 →接受编辑 → ... →绕行权限. 每种模式是速度和每行动审查之间的不同交易. 自动模式 (2026年3月) 增加了一个单独的分类器模型,将批准移离用户的关键路径:它在运行之前审查每个操作,并阻止任何超越请求的操作.

> 克劳德代码的权限系统是人类的答案. 不是一个"自主/不自主"开关,而是跨越能力阶梯的七种模式:计划 →默认 →接受编辑 → ... →绕过许可.每个模式是速度与每动作审查的不同权衡.

>  **【类比】**克劳德码权限模式 = 银行卡额度阶梯――(1) **plan**现在我还在电话问你.**default**交易量: 交易量: 交易量: 交易量: 交易量: 交易量: 交易量: 交易量:**acceptEdits**储蓄卡 (消费自动,转账问);**bypassPermissions (YOLO)**卡卡无限―― 汽车模式:99% 交易秒过,可疑交易(异地、大额、特殊商户) 触发人工核核―― 每种模式有适用的场景YOLO模式只在隔离容器中使用,本机部署永远不用――

> ️ **【易错点】**克劳德代码权限的3个致命错误:**本机用 bypassPermissions**一个快速注射 就能 rm -rf /;只在不敏感的临时容器用──(2) **没设 max_budget_usd**一个飞行循环 1 小时烧50美元; 必须设置`max_budget_usd=5`起步──(3) **完全信任 Auto Mode 分类器**人类明确说"分类器单独不充分";高危操作(rm、转账、发邮件) 必须双重确认,即使分类器说安全──


> **【中文解读】**本节介绍了AI代理的核心概念和实现方法. 代理是由LLM驱动的自主系统,能够观察环境,思考决策,执行行动和循环代直到完成目标.

工程问题:这个系统捕获了什么,它错过了什么,

> 工程问题:这个系统捕获什么?遗漏什么?给定任务实际适合哪种模式?

## 概念的核心概念

### 七种权限模式.
### 六种许可模式

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(上述名称与公共的克劳德码文件相匹配; UI标签`default`作为"手册")

> (上述名称匹配公开克劳德码文档;"yolo" 是宽松中间地带的非正式简写。)

### 单页的自动模式

汽车模式 (于2026年3月24日启动) 是首个授权模式,可以向模型授权每项操作的批准.

> 汽车模式 (自动模式) 是第一个将每动作审批委托给模型的权限模式.

结构:

> 结构:

1. **Stage 1 — single-token classifier.**运行在每一个拟议的行动. 廉价. 返回"安全"或"旗". 设计以与主代理循环并行运行,因此批准的行动不会排队.
   翻译: 中文**阶段 1——单 token 分类器。**在每一项提议动作上运行――廉价――返回"安全"或"标记"――为主代理设计的循环并行运行,使批准动作不排队――
2. **Stage 2 — secondary policy/safety review.**仅在标记的操作上运行. 对该行动,会议的当前状态和声明任务进行了集中政策和安全评估.如果信心低,则升级到用户HITL.
   翻译: 中文**阶段 2——二级政策/安全审查。**仅在标记动作上运行. 对动作,会话现状,声明任务执行聚焦政策和安全评估.
1. **A separate classifier model.**在执行之前,审查每项拟议的行动,根据声明任务和会议的当前状态进行判断,并阻止超越请求要求的任何东西. 阻止的行动归咎于用户.
2. **Gated availability.**无论是`auto`根据计划,组织能力,模型和提供商.

预算控制与分类器相结合:

> 预算控制与分类器并列:

- `max_turns` 会议中总代.
  翻译: 中文`max_turns`会话总代数――
- `max_budget_usd`美元限制,即会期的推迟.
  翻译: 中文`max_budget_usd`停止会话的美元上限.
- 每个工具的行动数量限制 (不超过N `WebFetch`电话等等).
  中文翻译:每工具动作数限制(不超过N 个 `WebFetch`调用等) 〔

### 系统捕获什么

- 直接向前即时注射到工具输入中,注射的指示将其映射到已知风险的操作形状.
  中文翻译:直接将提示注入工具输入,注入指示映射到已知危险动作形状──
- 复制工具循环 分类器可以看到N+1的操作几乎与N的操作相同,连续5次.
  中文翻译:重复工具循环分类器可见动作N+1 与动作N 几乎相同,连续五次。
- 显然是超出范围的命令, 只有在编辑文件的会议上.
  中文翻译:在仅文件编辑会话上明显超出范围的子命令.

### 系统可能会错过什么

- **Subtle prompt injection**直接提示注射不是一个完全可修复的漏洞 (OpenAI准备头,2025年,浏览器代理见第11课).
  翻译: 中文**微妙提示注入**在不产生单个标记动作的情况下调制行为──间接提示注入不是完全可修复的漏洞──OpenAI 准备主管,2025,关于浏览器代理见第 11 课) ──
- **Semantic-level misbehavior.**每个单独的行动都看起来安全,而构成的轨迹是有害的.
  翻译: 中文**语义级不当行为。**每个单独的动作看起来安全而组合轨迹有害.
- **Exfiltration through legitimate channels.**写数据到你拥有的文件,然后`git push`对于公众投资者来说,这是一个由允许的行动组成的问题.
  翻译: 中文**通过合法渠道泄露。**写数据到你拥有的文件,然后`git push`公共仓库是允许动作的序列,它的组合才是问题.

### 研究预览框架

作为研究预览,人类发送了自动模式. 文件明确表示,分类器是一个层,而不是解决方案:用户预计将自动模式与预算,允许表,孤立的工作空间和轨道审计结合起来 (课程1216). 预览框架还反映了记录的评估与部署差距 (课 1) 通过离线评估的分类器在用户的背景模糊的情况下,在实时会议中可以表现得不同.

> 预览框架也反映了已记录的评估部署差距 (第1课) 通过离线评估的分类器在用户下面会面模糊的真实行为中的可能不同行为.

### 在你的工作流程中,这个阶梯是你的工作流中的位置.

- 开始工作`plan`阅读计划比回头不好.
  中文翻译:不熟悉任务:在`plan`中开始──读计划比回滚坏运行便宜──
- 已知的变体:`acceptEdits`节省了很多确认点击.
  中文翻译:已知重构:`acceptEdits`省份大量确认点击.
- 无人监视的背景运行: `autoMode`只有在您测量的爆炸半径的工作空间内 (没有凭证,没有生产装备,没有您选择的出口).
  中文翻译:无人值守后台运行:仅在爆炸半径已测量工作区内`autoMode`(无证书,无生产挂载,无未选出口)
- 缩容器: `yolo`现在,`bypassPermissions`如果容器及其凭证可处置,并且只有当容器和其凭证可处置时才可接受.
  中文翻译:临时容器:`yolo`现在,`bypassPermissions`可接受,只可作为容器及其证书被丢弃.
- 无人监视的背景运行: `auto`只有在您测量的爆炸半径的工作空间内 (没有凭证,没有生产装备,没有您选择的出口).
- 缩容器: `dontAsk`现在,`bypassPermissions`如果容器及其凭证可处置,并且只有当容器和其凭证可处置时才可接受.

```figure
autonomy-oversight
```

## 用它实现框架

`code/main.py`模拟一个行动审查分类器作为一个两阶段的管道 一个教学简化;`auto`操作模式由单独的分类器模型支持,而不是文档的两阶段合同.第一阶段是对拟议的行动进行廉价关键字规则;第二阶段是较慢的多规则审查器.司机通过短的合成轨迹 (安全的行动,即时注射尝试,重复循环) 进行取,并显示分类器在哪里抓住,错过.

> `code/main.py`模拟两阶段分类器──阶段1是提议动作上的廉价关键词规则;阶段2是较慢的多规则审查器──驱动器入短合成轨迹(安全动作、提示注入尝试、重复循环) 并展示分类器捕获和遗漏的处境──

## 运送它.

`outputs/skill-permission-mode-picker.md`任务描述与正确的许可模式,预算限制和所需的隔离相匹配.

> `outputs/skill-permission-mode-picker.md`描述任务的匹配到正确权限模式,预算上限和需要的隔离.

## 练习题

1. 跑步`code/main.py`哪种合成行动类型从来没有被第一阶段标记,但总是被第二阶段捕获?
   中文翻译:运行 `code/main.py`◎哪种合成动作类型从未被标记过,但总被捕获过?

2. 扩大设置的第一阶段规则,以捕捉特定已知坏形状 (例如,`curl $ATTACKER/exfil`) 测量良性作用样本的假阳性率.
   中文翻译:扩展阶段 1 规则集以捕获特定已知坏形状`curl $ATTACKER/exfil` 测量假阳性率

3. 阅读Anthropic的"代理循环如何工作"文件.`default`在运行之前,你需要单独关门.`autoMode`没有监督?
   中文翻译:阅读人类的"代理循环如何工作"文档――列出`default`模式下 代理默认触及的每一个外部状态.`autoMode`需要单独控制什么?
3. 阅读Anthropic的"代理循环如何工作"文件.`default`在运行之前,你需要单独关门.`auto`没有监督?

4. 设计一个24小时无监督运行预算: `max_turns`现在`max_budget_usd`按工具盖,允许,证明每个数字.
   中文翻译:设计 24 小时无人值守运行预算:`max_turns`,我知道.`max_budget_usd`、每一个工具上限、允许列表――论证每一个数字――

5. 描述一个轨迹,每个单独的行动都被第一阶段和第二阶段批准,但组合的行为是错误的. (课程14涵盖了杀死开关和加拿大代币如何解决这个问题.)
   中文翻译:描述一条轨迹,每个单独动作都被批准的阶段1 和阶段2 ,但组合行为不对齐.
5. 描述一个行径,其中每个单个行动都被分类器批准,但组合的行为是错误的. (课程14涵盖杀死开关和加拿大代币如何解决这个问题.)

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## 继续阅读 继续阅读

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)许可模式,预算,行动格式.
  中文翻译:权限模式、预算、动作格式──
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)管理服务执行模式.
  中文翻译:管理服务执行模型。
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code)功能表面和自动模式公告.
  中文翻译:功能面和自动模式公告──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution)基于理性的层,塑造分类者判断.
  中文翻译:塑造分类器判断的基于推理的层次.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy)长视野许可设计的内部观点.
  中文翻译:长程权限设计的内部视角──
