# 卡普斯通01 终端原生编码代理

> 到2026年,编码器的形状已经确定. 图伊带,一个状态的计划,一个沙盒的工具表面,一个循环,计划,行动,观察,恢复. 克劳德代码,课程3和开码从50英尺处看起来都是一样的. 这块顶石要求你构建一个端到一个端,  CLI,  拉出请求, 你会了解为什么最难的是不是模型调用,而是工具循环,沙盒和50转运费用上限.

> **【中文解读】**本节是综合项目构建终端原生编码代理,整合代理循环、工具使用和记忆系统──

>  **【前置】**这是19期第1个石 (Capstone) 项目,35小时工作量.前置要求覆盖整个11-17期的第一务必先做完:**不要在没学完 Phase 14 的情况下尝试本节**会完全看不懂.

**Type:** Capstone | **类型:** 综合项目
**Languages:** TypeScript / Bun (harness), Python (eval scripts) | **语言:** TypeScript / Bun（框架）, Python（评估脚本）
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and protocols), Phase 14 (agents), Phase 15 (autonomous systems), Phase 17 (infrastructure) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）, Phase 14（Agent）, Phase 15（自主系统）, Phase 17（基础设施）
**Phases exercised:**没有任何东西可以让你感到困惑.**涉及阶段:**子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子
**Time:** 35 hours | **时间:** 35 小时

## 问题 问题引入

> **【中文解读】**本节阐述编码代理面临的核心工程挑战.2026年编码代理已成为AI应用最热门的品类,Claude Code、Cursor、Devin等产品采用类似的架构:终端界面 + 工具调度 + 沙箱隔离 + 规划执行观察循环.关键瓶不在于模型能力,而在工具循环稳定性上下文窗口管理和成本控制.

> **【拓展：Coding Agent 产业格局】**2026年编码代理市场规模超过50亿美元――人类的克劳德代码 采用克系统实现生命周期管理,课程的编曲者 2 引入代理图表多任务并行,认知的Devin 专注端到端自主开发――Live-SWE-agent 在SWE-bench验证上达到79.2%的通过率(使用Opus 4.5),OpenCode 开源项目获得了112k GitHub 星标,反映了开发者对自主编码工具的巨大需求――

2026年,编码代理成为主导AI应用类别. 克劳德代码 (人类),Cursor 3与组合器2和代理图表 (Cursor),Amp (Sourcegraph),OpenCode (112k星),工厂无人机和谷歌朱尔斯所有船变化相同的架构:终端带,一个许可的工具表面,一个沙盒,和一个计划-行动观察循环围绕边界模型. 直播SWE代理达到79.2%的SWE台 验证了Opus 4.5 ,但工程工艺是宽的. 失败模式的大部分都不是模型错误. 它们是工具循环不稳定性,环境中毒,逃跑的代币成本,

> 编码代理在2026年成为AI应用的主导品类型. Claude Code(Anthropic) 带 Composer 2 和 Agent Tabs 的课件3、Amp(Sourcegraph) 、OpenCode(112k 星标) 、工厂Droids 和 Google Jules 都采用相同的架构变体:终端框架、权限工具表面、沙箱和围绕前沿模型的规划执行观察循环──前沿非常窄Live-SWE-agent 在SWE-bench 验证上使用Opus 4.5  79.2%但工程工艺很广──大多数失败模式不是模型错误,而是工具循环不稳定、上下文污染、已达到 成本失控和破坏性文件系统的操作.

你必须建造一个,在47的环节崩,当Ripgrep返回8MB的匹配,

> 你不能从外部推测这些代理. 你必须构建一个,观察循环在第47轮崩.

## 概念的核心概念

> **【中文解读】**编码代理的核心架构包含四个大模块:计划(维护待务项状态) 行为(调度工具调用) 观察(截断输出并反) 恢复(错误恢复) 2026年新增克机制8种生命周期事件子,用于注入策略、遥测和安全防护箱使用E2B或Daytona,每个任务在独立的 Git 工作树中运行,永不接触宿主文件系统

> **【拓展：Plan-Act-Observe 循环】**这一架构源于ReAct论文 ((Yao et al., 2023),后被所有主流编码代理采用――Claude Code的 TodoWrite 工具将计划状态持久化`.claude/state.json`支持崩恢复――成本控制分三层:每轮代币上限、每会话美元预算、硬性轮次上限(通常是50轮) 实际数据显示,一次SWE-台 任务的中位数 成本约$0.40-2.00，但尾部可达 $五,因此成本至关重要.

带有四个表面.**Plan**保持一个 TodoWrite 样式状态对象,模型每次转换. **Act**发送工具调用 (阅读,编辑,运行,搜索, Git).**Observe**捕获/stderr/出口代码,缩小,并将总结回放. **Recover**没有打破文本窗口或永远循环处理工具错误. 2026 形状增加了另一个东西: **hooks**现在,我们要去.`PreToolUse`现在`PostToolUse`现在`SessionStart`现在`SessionEnd`现在`UserPromptSubmit`现在`Notification`现在`Stop`其他`PreCompact`可配置的延伸点,操作员注入的政策,远程测量和防护.

> 框架有四个表面.**Plan**维护一个全写风格状态对象,模型每轮重写――**Act**调度工具调用(读取、编辑、运行、搜索、git) **Observe**捕获 stdout/stderr/退出码,截断并反摘要──**Recover**处理工具错误不破坏上下文窗户或无限循环――2026年增加了一个形态:**hooks**,我知道.`PreToolUse`,我知道.`PostToolUse`,我知道.`SessionStart`,我知道.`SessionEnd`,我知道.`UserPromptSubmit`,我知道.`Notification`,我知道.`Stop`和 `PreCompact`可配置的扩展点,操作员在此注入策略,遥测和护.

沙箱是E2B或戴顿. 每个任务都运行在一个新的 devcontainer, 连接器永远不会触及主机文件系统. 工作树在成功或失败时会被撕毁. 成本控制是通过三个层次执行的:每轮代币上限,每次会议的美元预算,以及硬转限 (通常是50). 观察性层是与GenAI语义公约的OpenTelemetry跨度,

> 沙箱使用E2B或Daytona──每个任务都在带有 git工作树 挂载为读的全新开发集装箱 中运行──框架从未接触主机文件系统──工作树在成功或失败后被拆除──成本控制分为三层强制执行:每轮代币上限、每会话美元预算和硬性轮次限制(通常为50)──可观测层是带有 GenAI 语义约定的OpenTelemetry跨度,发送到自托管的Langfuse──

## 建筑,建筑

```
  user CLI  ->  harness (Bun + Ink TUI)
                  |
                  v
           plan / act / observe loop  <--->  Claude Sonnet 4.7 / GPT-5.4-Codex / Gemini 3 Pro
                  |                          (via OpenRouter, model-agnostic)
                  v
           tool dispatcher (MCP StreamableHTTP client)
                  |
     +------------+------------+----------+
     v            v            v          v
  read/edit    ripgrep     tree-sitter   git/run
     |            |            |          |
     +------------+------------+----------+
                  |
                  v
           E2B / Daytona sandbox  (worktree isolated)
                  |
                  v
           hooks: Pre/Post, Session, Prompt, Compact
                  |
                  v
           OpenTelemetry -> Langfuse (spans, tokens, $)
                  |
                  v
           PR via GitHub app
```

##  技术

- 带运行时间: Bun 1.2 + Ink 5 (终端反应)
  中文翻译:运行时间: Bun 1.2 + 墨水 5 (反应在终端)
- 模型访问:OpenRouter与Claude Sonnet 4.7,GPT-5.4-Codex,Gemini 3 Pro,Opus 4.5 (用于最困难的任务)
  中文翻译:模式访问:OpenRouter与Claude Sonnet 4.7,GPT-5.4-Codex,Gemini 3 Pro,Opus 4.5 (用于最困难的任务)
- 工具运输:模式语境协议 StreamableHTTP (MCP 2026修订)
  中文翻译:工具运输:模式语境协议流动HTTP (MCP 2026修订)

> 中文翻译:工具运输:模型语境协议流动HTTP (MCP 2026修订)

- 沙箱:E2B沙箱 (JS SDK) 或戴tona开发集装箱
  中文翻译:沙盒:E2B沙盒 (JS SDK) 或戴顿娜的开发集装箱
- 代码搜索: ripgrep子工艺,17种语言的树守护器 (预编译)
  中文翻译:代码搜索: ripgrep子进程,树守护者解析器17种语言 (预编译)
- 隔离:`git worktree add`按任务,成功/失败的清理
  中文翻译:孤立: `git worktree add`按任务,成功/失败的清理
- 杆:SWE-bench Pro (验证子集) +终端-Bench 2.0 +您自己的30任务持有
  中文翻译:同等式:SWE-bench Pro (验证子集) +终端-Bench 2.0 +你自己的30任务持久

> 中文翻译:平衡套件:SWE-bench Pro (验证子集) +终端-Bench 2.0 +你自己30任务的持有器 (翻译)

- 可观察性: 开放Telemetry SDK`gen_ai.*`semconv → 自主主办的Langfuse
  中文翻译:可观察性:OpenTelemetry SDK与 `gen_ai.*`semconv → 自主主办的Langfuse

> 中文翻译:可观察性:OpenTelemetry SDK与 `gen_ai.*`标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

- 公共关系发布:GitHub应用程序,具有细粒度的代币,范围仅限于目标回复
  中文翻译:PR发布:GitHub应用程序具有细粒度的代币,范围仅限于目标备用程序

## 动手构建

> **【中文解读】**构建步骤分为8个阶段:从TUI 界面构建开始,逐步实现计划状态管理六大工具文件读写/搜索/符号解析/Shell/Git)  E2B 沙箱包装,8种子子、SWE-bench 评估、成本控制到最终 PR 提交.

> **【拓展：SWE-bench 评估体系】**据悉,SWE-bench是目前编码的代理 最权威的评测基准,包含真实GitHub问题和对应补丁.
```figure
ce-agent-loop
```

## 建立它

1. **TUI and command loop.**布一个子项目用墨水.接受.`agent run <repo> "<task>"`打印分类视图:计划表 (上),工具调用流 (中),代币预算 (下). 添加取消在Ctrl-C上开启 `SessionEnd`在出口前.
   中文翻译:1. **TUI and command loop.**布一个子项目用墨水.接受.`agent run <repo> "<task>"`打印分类视图:计划表 (上),工具调用流 (中),代币预算 (下). 添加取消在Ctrl-C上开启 `SessionEnd`在出口前.

2. **Plan state.**定义输入的 TodoWrite 方案 (悬而未决 / in_progress /完成的项目与笔记).模型每次重写完整状态作为工具调用. 不要让它逐步变化. 继续计划`.agent/state.json`让车恢复.
   翻译: 翻译:**Plan state.**定义输入的 TodoWrite 方案 (悬而未决 / in_progress /完成的项目与笔记).模型每次重写完整状态作为工具调用. 不要让它逐步变化. 继续计划`.agent/state.json`让车恢复.

3. **Tool surface.**定义六种工具:`read_file`现在`edit_file`其他地方的`ripgrep`现在`tree_sitter_symbols`现在`run_shell`通过时间限制,`git`(status/diff/commit/push). 通过MCP StreamableHTTP将其曝光,使其具有交通不知性.每个工具都会返回缩小输出 (每次通话的4k代币限制).
   翻译: 翻译:**Tool surface.**定义六种工具:`read_file`现在`edit_file`其他地方的`ripgrep`现在`tree_sitter_symbols`现在`run_shell`通过时间限制,`git`(status/diff/commit/push). 通过MCP StreamableHTTP将其曝光,使其具有交通不知性.每个工具都会返回缩小输出 (每次通话的4k代币限制).

4. **Sandbox wrapping.**每个任务都会产生一个E2B沙箱.`git worktree add -b agent/$TASK_ID`现在,我们在一个新的分支.所有工具调用都在沙盒内执行. 主机文件系统是不可访问的.
   翻译: 翻译:**Sandbox wrapping.**每个任务都会产生一个E2B沙箱.`git worktree add -b agent/$TASK_ID`现在,我们在一个新的分支.所有工具调用都在沙盒内执行. 主机文件系统是不可访问的.

5. **Hooks.**实现2026年所有八种子类型. 连接至少四种用户授权的子: (a) `PreToolUse`破坏性指挥卫队,阻止了`rm -rf`在工作树外,`PostToolUse`标志性会计, (c) `SessionStart`预算初始化,`Stop`写出最后一个痕迹.
   翻译: 五.**Hooks.**实现2026年所有八种子类型. 连接至少四种用户授权的子: (a) `PreToolUse`破坏性指挥卫队,阻止了`rm -rf`在工作树外,`PostToolUse`标志性会计, (c) `SessionStart`预算初始化,`Stop`写出最后一个痕迹.

6. **Eval loop.**复制一个30个版本的SWE-bench Pro Python子集. 运行你的束对每一个. 通过@1,转换每任务和$-per-task上进行微型Swe-agent (最小基线) 的比较. 写结果到`eval/results.jsonl`现在,我们要去.
   翻译: 七个字**Eval loop.**复制一个30个版本的SWE-bench Pro Python子集. 运行你的束对每一个. 通过@1,转换每任务和$-per-task上进行微型Swe-agent (最小基线) 的比较. 写结果到`eval/results.jsonl`现在,我们要去.

7. **Cost control.**硬切割:50轮,200万语境,每任务5美元.`PreCompact`子总结了旧的转变,成为一个前状态块, 在150k的标志, 给新的观测空间,
   翻译:7.**Cost control.**硬切割:50轮,200万语境,每任务5美元.`PreCompact`子总结了旧的转变,成为一个前状态块, 在150k的标志, 给新的观测空间,

8. **PR posting.**对于成功,最后一步是`git push`+一个GitHub API调用,将计划和体内的差异总结打开一个 PR.
   翻译:8.**PR posting.**对于成功,最后一步是`git push`+一个GitHub API调用,将计划和体内的差异总结打开一个 PR.

## 用它使用方法

```
$ agent run ./my-repo "Fix the race condition in worker.rs"
[plan]  1 locate worker.rs and enumerate mutex uses
        2 identify shared state under contention
        3 propose fix, verify tests
[tool]  ripgrep mutex.*lock -t rust           (44 matches, truncated)
[tool]  read_file src/worker.rs 120..180
[tool]  edit_file src/worker.rs (+8 -3)
[tool]  run_shell cargo test worker::          (passed)
[plan]  1 done · 2 done · 3 done
[done]  PR opened: #482   turns=9   tokens=38k   cost=$0.41
```

## 发射上线

能得到的技能生活在`outputs/skill-terminal-coding-agent.md`根据备忘录路径和任务描述,它将在沙盒中运行完整的计划-行为-观察循环,并返回一个 PR URL 加上一个追踪捆绑.

> 交付物品技能 位于`outputs/skill-terminal-coding-agent.md`△ 给定仓库路径和任务描述,它在沙箱中运行完整的规划执行观察循环,返回 PR URL 和追踪包──本结业项目评分标准:

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 vs baseline | Your harness vs mini-swe-agent on 30 matched Python tasks |
| 25 | SWE-bench Pro pass@1 对比基线 | 你的框架 vs mini-swe-agent 在 30 个匹配 Python 任务上 |
| 20 | Architecture clarity | Plan/act/observe separation, hook surface, tool schema — reviewed against Live-SWE-agent layout |
| 20 | 架构清晰度 | Plan/act/observe 分离、hook 表面、tool schema——对照 Live-SWE-agent 布局审查 |
| 20 | Safety | Sandbox escape tests, permission prompts, destructive-command guard passes red-team |
| 20 | 安全性 | 沙箱逃逸测试、权限提示、破坏性命令守卫通过红队测试 |
| 20 | Observability | Trace completeness (100% of tool calls spanned), token accounting per turn |
| 20 | 可观测性 | 追踪完整性（100% 工具调用被 span 覆盖）、每轮 token 计费 |
| 15 | Developer UX | Cold-start < 2s, crash recovery resumes plan, Ctrl-C cancels mid-tool cleanly |
| 15 | 开发者体验 | 冷启动 < 2s、崩溃恢复续接计划、Ctrl-C 干净取消工具调用 |
| **100** | | |

## 练习题

1. 换取支持模型从Claude Sonnet 4.7到vLLM上提供的Qwen3-Coder-30B.比较pass@1和$-per-task.报告开放模型的性能低.
   中文翻译:将支持模型从Claude Sonnet 4.7 换为vLLM 上的Qwen3-Coder-30B──比较pass@1 和每任务成本──报告开源模型表现不佳的处处──

> 中文翻译:将支持模型从Claude Sonnet 4.7 换为vLLM 上的Qwen3-Coder-30B──比较pass@1 和每任务成本──报告开源模型表现不佳之处──(翻译)


2. 添加一个`reviewer`测量假阳性评价是否降低SWE位通过率低于单代理基线 (提示:通常是的).
   中文翻译:添加一个`reviewer`经理,在 PR 发布前读取不同并可要求修改循环――测量误报审查是否会降低SWE-位通过率

> 中文翻译:添加一个`reviewer`测量误报审查是否会降至单个代理基线以下


3. 压力测试沙盒:写一个试图完成的任务`curl`确认两个被 PreToolUse 锁.记录尝试.
   中文翻译:压力测试沙箱:编写一个尝试 `curl`外部URL的任务和一个在工作树外写入的任务──确认两者都被 PreToolUse hook 阻止──记录尝试──

> 中文翻译:压力测试沙箱:编写一个尝试 `curl`外部URL的任务和一个在工作树外写入的任务──确认两者都被 PreTool使用锁阻止──记录尝试──(翻译)


4. 实施`PreCompact`通过较小的模型来总结 (海库4.5). 测量在3x紧缩时损失了多少计划忠诚度.
   中文翻译:用更小的模型(海库4.5)实现`PreCompact`摘要――测量3倍压缩后计划保真度损失多少――

> 中文翻译:用更小的模型(海库4.5)实现`PreCompact`摘要──测量3倍压缩后计划保真度损失多少──(翻译)


5. 换MCP流动HTTP输送为工作室. 标记冷启动和每次通话延迟. 选择一个获胜者仅用于本地使用.
   中文翻译:将 MCP StreamableHTTP 传输换为studio。基准测试冷启动和每次调用延迟。为纯本地使用选择胜者。

> 中文翻译:将 MCP StreamableHTTP 传输换为stdio。基准测试冷启动和每次调用延迟。为纯本地使用选择胜者。(翻译)


## 关键词 关键词

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Harness | "The agent loop" | The code surrounding the model that dispatches tools, maintains plan state, and enforces budgets |
| 框架 | "Agent 循环" | 围绕模型的代码，调度工具、维护计划状态和强制预算 |
| Hook | "Agent event listener" | A user-authored script run on one of eight lifecycle events by the harness |
| 钩子 | "Agent 事件监听器" | 在框架的八种生命周期事件之一上运行的用户编写脚本 |
| Worktree | "Git sandbox" | A linked git checkout at a separate path; disposable without touching the main clone |
| 工作树 | "Git 沙箱" | 在独立路径上的链接 git 检出；可丢弃而不影响主克隆 |
| TodoWrite | "Plan state" | A typed list of pending/in-progress/done items the model rewrites each turn |
| TodoWrite | "计划状态" | 模型每轮重写的待处理/进行中/已完成项的类型化列表 |
| StreamableHTTP | "MCP transport" | 2026 MCP revision: long-lived HTTP connection with bidirectional streaming; replaces SSE |
| StreamableHTTP | "MCP 传输" | 2026 MCP 修订版：支持双向流式的长连接 HTTP 连接；替代 SSE |
| Token ceiling | "Context budget" | Per-turn or per-session cap on input+output tokens; triggers compaction or termination |
| Token 上限 | "上下文预算" | 每轮或每会话的输入+输出 token 上限；触发压缩或终止 |
| pass@1 | "Single-attempt pass rate" | Fraction of SWE-bench tasks solved on the first run without retry or test-set peeking |
| pass@1 | "单次通过率" | 首次运行（无重试或偷看测试集）解决的 SWE-bench 任务比例 |

## 继续阅读 继续阅读

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)来自Anthropic的参考带
  中文翻译:人类的参考框架
- [Cursor 3 changelog](https://cursor.com/changelog) 代理 标签和作曲器2产品说明
  中文翻译:代理标签 和 编曲者 2 产品说明
- [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)SWE-板的最低基准比较
  中文翻译:SWE-bench 框架对比的最小基线
- [Live-SWE-agent](https://github.com/OpenAutoCoder/live-swe-agent) 79.2% SWE  通过 Opus 4.5 验证
  中文翻译:使用Opus 4.5 在SWE-bench 验证上达到79.2%
- [OpenCode](https://opencode.ai)开放的带,112千颗星星
  中文翻译:开源框架,112k 星标
- [SWE-bench Pro leaderboard](https://www.swebench.com)本标题的评估目标
  中文翻译:本结业项目目标的评估排行榜
- [Model Context Protocol 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)流式HTTP,功能元数据
  中文翻译:可流动HTTP、能力元数据
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)工具调用和代币使用的跨度方案
  中文翻译:工具调用和标志 使用的跨度模式
