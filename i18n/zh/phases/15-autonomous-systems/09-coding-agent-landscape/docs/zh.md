# 无人编码代理 风景 (2026)  无人编码代理 全景(2026)

> 在三年内,SWE-bench Verified从4%上升到80.9%. 同样的Claude Sonnet 4.5在SWE-agent v1上获得了43.2%的分数,59.8%在Cline自主,模型周围的架架现在与模型本身一样重要. 开户手 (原是OpenDevin) 是最活跃的MIT许可平台,其CodeAct循环直接执行Python操作在沙盒中,而不是JSON工具调用. 标题数字隐藏了一个方法问题:在500个SWE-bench验证任务中,161只需要12行变化,而SWE-bench Pro (10+行任务) 在相同的边界模型中占2359%

> **【中文解读】**在不到三年内,SWE-bench Verified从4%升至80.9%──同样的Claude Sonnet 4.5在SWE-agent v1上升43.2%,在Cline自主上升59.8%模型周围的脚手架现在和模型本身一样重要──OpenHands(前OpenDevin) 是最活跃的MIT许可平台,其CodeAct循环直接在沙盒中执行Python动作而不是JSON工具调用──标题数字隐藏方法论:500个SWE-bench Verified任务中,161个只需要1-2行变更,SWE-bench Pro(10+行任务) 藏了前沿模型只有23-59%──

> **【拓展：脚手架 > 模型】**2022-2026年曲线表明编码代理的能力提升有三个复杂来源:更好的基础模型,更好的脚手架 ((CodeAct、反思、验证器循环) ‧更好的基准 ((验证除噪声) ⋅不同脚手架下分数差异 16.6 个绝对点

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**学本节前请先掌握:阶段14·07(工具调用) 、阶段14·30+(工作台 代理实践) 、阶段15·01(长程代理) ⋅本节是2026年编码代理 全景图选型必读──
>  **【类比】**选编码代理 = "选车"而不是"选发动机"――同一个发动机(Claude Sonnet 4.5) 装在不同车上(SWE-agent vs Cline) 速度差16个百分点――脚手架(检索层、规划器、沙箱、编辑-验证 循环) 才是产品,模型只是组件――所以不要只看模型排行榜,看"我的任务+我的脚手架"的端到端可靠性――
> ️ **【易错点】**看SWE-bench 验证分数选中代理 = 被基准骗了──500 个任务里 161 个只需要1-2 行修改(容易),看SWE-bench Pro(10+ 行真实任务) 分数才有参考值──修复:选中代理 前用自己代码库的真实问题 测试,而不是看营销基准──

## 问题 问题引入

> **【中文解读】**编码代理景观是2025-2026年最快变化的人工智能应用领域之一.主要玩家包括克劳德代码,Cursor,GitHub 副驾驶员,Devin,Windsurf等.

> **【拓展：coding agent landscape】**2026年编码 代理的竞争格局:(1) 克劳德代码人类的自主编码 代理,支持全开发、Git操作和终端命令执行;(2) 课件基于 VS代码的AI编辑器,强调人机协作;(3) 德文认知 AI的全自主编码 代理,可以独立完成开发任务;(4) 风冲浪(原代码) AI优先的IDE──SWE-bench 上面的表现是主要竞争指标.

问题是:在一个与我工作相匹配的任务分配下,

> 问题是:在与我的工作相匹配的任务分布上,我使用在生产中运行的脚本架,我能获得什么端到端可靠性?

在2022年至2026年间,该领域学会了架,检索层,规划器,沙盒,编辑-验证循环,反格式, 在SWE-agent v1上,Claude Sonnet 4.5在SWE-bench Verified上获得了43.2%的分数;在Cline的自动架子内,同样的模型获得了59.8%. 16.6 绝对差异点,重量相同. 基本模型是一个组成部分,循环是产品.

> 截至2026年间,领域学到脚手架检索层,规划器,沙箱,编辑验证循环,反格式是承担的.

> **【中文解读】**本节介绍了AI代理的核心概念和实现方法. 代理是由LLM驱动的自主系统,能够观察环境,思考决策,执行行动和循环代直到完成目标.

随机问题是,基准度隐藏了回归.

> 伴随的问题是基准和隐藏回归.

现实世界质量更好地测量在SWE-bench Pro (10+线变化) 等分布上,其中相同的领导者仍然保持2359%.

> 现实世界质量在SWE-bench Pro(10+ 行变更)等分布上测量更好,同一个领先者仍然只有23-59%──

## 概念的核心概念

### ,一个段落.

通过基因真相补丁,SWE-bench (Jimenez等) 将真正的GitHub问题处理,并要求代理制作一个补丁,使测试套件通过.SWE-bench Verified (OpenAI, 2024) 是由人类策划的500个任务子集,其中模糊和破解的任务被删除.SWE-bench Pro是更难的继承者.需要10+行变化的任务,目前的边境代理处于2359%.

> 通过GitHub问题,要求代理产生使测试套件通过补丁. 通过SWE-bench 验证. 开放AI,2024) 是人工策划的500个任务子集,消除模糊和损坏的任务.

### 什么是2022→2026曲线实际显示什么

- **2022**的研究模型在原材料中占~4%.
  翻译: 中文**2022**研究模型在原始SWE-台上约4%──
- **2024**:GPT-4 + 德文式架在 ~ 14%;SWE剂在 ~ 12%
  翻译: 中文**2024**据报道,该公司的数据显示,
- **2025**: 克劳德3.5/3.7 内和SWE剂推进到4055%的范围.
  翻译: 中文**2025**子在Aider和SWE代理内推进 40-55% 范围.
- **2026**欧盟的领导者:Claude Sonnet 4.5和边界竞争对手在SWE-bench Verified上以7080%以上的价格.
  翻译: 中文**2026**据悉,在中国,中国的智能技术技术的发展趋势是非常突出的.

倾斜来自三个组合来源:更好的基模型,更好的架构 (CodeAct,反射,验证循环) 和更好的基准 (验证消除噪音).

> 斜率来自三个复合源:更好的基础模型,更好的脚手架,更好的基准,更好的验证器循环.

### 代码Act与JSON工具调用

开手 (All-Hands-AI, arXiv:2407.16741,以前是OpenDevin) 采取了特定的架构投注:而不是模型发射一个主机解码和执行的JSON工具调用,模型发射了Python代码,一个Jupyter式内核将其运行在一个沙盒中.代理可以循环文件,链工具,并在一个操作中捕获自己的例外.

> 模型不再由主机解码执行的JSON工具调用发行,而是发出Python代码,由Jupyter 风格内核在沙箱中运行.

交易:

> 权衡:

- **JSON tool calls**:每次行动都是一次回复的;易于进行审计;具有有限的组合性;默认安全,因为每次调用都通过了明确的验证器.
  翻译: 中文**JSON 工具调用**通过显式验证器进行的调用,
- **CodeAct**操作可能是整个程序; 构成; 需要硬化的沙盒 (OpenHands使用Docker隔离); 失败模式包括沙盒运行时间允许的任何东西.
  翻译: 中文**CodeAct**动作可以是整个程序;可组合;需要加固沙箱;失败模式包括沙箱运行时允许的任何事情.

两个架构都在生产中. CodeAct 在开放平台 (OpenHands, smolagents) 中占主导地位. JSON 工具调用仍然占主导地位在管理服务 (人类管理代理,OpenAI助理) 中,供应商控制执行者.

> 两种架构都在生产中. 编码在开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上. 开放平台上.

### 布架在2026年景观中.

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### 为什么脚架主导?

编码运行是一个长视线轨迹 (课 1) 可靠性化合物跨步骤.三个地方,架架购买点:

> 编码运行是长程轨迹 (第1课) ⋅可靠性跨步骤复合――脚手架买入分数的三个地方:

1. **Retrieval**现在,我们需要一个新的方法来找到正确的文件,
   翻译: 中文**检索**为了找到需要阅读的正确文件,SWE代理的ACI,OpenHands的文件索引,Aider的 repo-map都攻击了这一点.
2. **Verifier loop**测试,阅读堆痕迹,再试一次是10+点的三角形.
   翻译: 中文**验证器循环**运行测试、读堆跟踪、重试在SWE-bench 上是10+点增量──
3. **Failure containment**由于这种情况,我们可以看到一个系统的变化,但它不能变化.
   翻译: 中文**失败遏制**错误时回滚的沙箱防止复合损害――相同的模型有和无验证器循环看起来像两个不同的产品――

### 基准和与真实分布

开手作者和Epoch AI都指出,SWE-bench Verified具有一个简单的尾声:500项任务中161只需要12行变化.高分数部分是由这个尾声驱动的.SWE-bench Pro限制到10+行变化,即使是边界系统也会返回2359%的分数.您的生产分布几乎肯定更接近Pro而不是 Verified.

> 开手作者和时代AI都标记了SWE-bench Verified 有简单尾部:500个任务中,161个只需要1-2 行变更。高分部分由该尾部驱动。SWE-bench Pro 限制10+ 行变更,即使前沿系统也返回23-59% 范围──你的生产分布几乎肯定更接近Pro而不是 Verified。

选择代理的含义:运行您自己的 bug 后备的 Pro 类子集.重要的是您运送的任务的分数.

> 选择代理的含义:你自己在运行的错误 积压上运行  Pro 类子集──重要分数是代表你发布任务的分数──

## 用它实现框架
```figure
a5-scaffold-delta
```

## 用它

`code/main.py`根据固定的迷你任务分布,比较两个玩具代理架子:

> `code/main.py`在固定迷你任务分布上比较两个玩具代理脚手架:

1. **JSON tool-call**架每轮都需要一次行动.
   翻译: 中文**JSON 工具调用**脚手架,每轮一个动作.
2. **CodeAct**通过一个脚架,每次操作可以发出一个小的Python截图.
   翻译: 中文**CodeAct**脚手架,每动作可发出小的字符串片段.

两者都使用一个"模型" (确定性规则) 杆,因此比较将架架与模型质量隔离.输出显示,CodeAct架架以更大的每动作爆炸半径的成本在更少的转折中解决更多任务.

> 两者使用存根模型 (确定性规则) 进行比较,以将脚架与模型质量隔离.

## 运送它.

`outputs/skill-scaffold-audit.md`帮助您在采用之前审核拟议的编码代理架构:检索质量,验证器存在,沙盒隔离和基准配送适合性.

> `outputs/skill-scaffold-audit.md`帮助您在采用前审计提议编码 代理 脚手架:检索质量、验证器存在、沙箱隔离、基准到分布契合――

## 练习题

1. 跑步`code/main.py`每个脚架都在同一任务中做多少转?
   中文翻译:运行 `code/main.py`每个动作爆炸半径是多少轮?

2. 阅读OpenHands论文 (arXiv:2407.16741).论文认为 CodeAct 比复杂任务的JSON工具调用更好. 确定一种失败模式,该论文承认,并写一句话,当该模式在生产中占主导地位时.
   中文翻译:阅读OpenHands 论文(arXiv:2407.16741) ・论文论证 CodeAct 在复杂任务上胜过JSON 工具调用――识别论文承认一个失败模式并写一句该模式在生产中何时主导――

3. 在您的 bug 后备中选择一个任务,需要在两个文件中进行10+ 个变化行.根据 (a) JSON 工具调用和 (b) CodeAct 估计边界模型的端到端成功概率.证明差距.
   中文翻译:从你的bug 积压中选一个需要跨两文件 10+ 行变更的任务――估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率――论证差距――

4. 通过SWE-bench Verified,我们可以完成161个单文件,12行任务. 构建一个排列表的分数,排除它们.
   中文翻译:SWE-bench Verified 有 161 个单文件 1-2 行任务――构建排除它们的分数――排行榜如何重排?

5. 阅读"引入SWE-bench Verified" (OpenAI). 解释消除模糊任务所使用的具体方法,并命名一个类别,策展会错过.
   中文翻译:阅读"引入SWE-bench Verified" (OpenAI) 解释用于除模糊任务的具体方法论,命名策划会遗漏的一个类别.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## 继续阅读 继续阅读

- [Jimenez et al. — SWE-bench](https://www.swebench.com/)原始基准和方法.
  中文翻译:原始基准和方法论──
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)如何构建选定的子集.
  中文翻译:策划子集如何构建──
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) CodeAct 架构和事件流设计.
  中文翻译:CodeAct 架构和事件流设计.
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks)现场记录.
  中文翻译:实时跟踪分数――
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy)长视野编码剂可靠性框架.
  中文翻译:长程编码 代理可靠性框架――
