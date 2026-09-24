# 克劳德特工: 副部长和会议商店
#  套装和会议店

> 您可以进口的带:内置工具,环境隔离的子管,子,W3C痕迹传播,会议持久性. 克劳德代理SDK是参考例子 克劳德代码带的库形式 克劳德管理代理是长期的异步工作的托管替代品.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## 学习目标

- 解释Anthropic Client SDK (原料API) 和Claude Agent SDK (形) 的区别.
- 描述子体并行和背景隔离以及何时达到它们.
- 命名Python SDK的会议存储表面 (`append`现在`load`现在`list_sessions`现在`delete`现在`list_subkeys`) 和 `--session-mirror`现在,我们要去.
- 实现一个有内置工具的 stdlib 带,一个孤立的背景,生命周期子,和一个会议商店的子弹.

## 问题 问题引入

制作代理需要工具执行,MCP服务器,生命周期,子弹生殖,会议持续性,痕迹传播.Claude Agent SDK将这种形状作为库相同的使用工具Claude Code,暴露于定制代理.

> 原始LLM API只能给你一次回调调.生产级代理 需要工具执行,MCP 服务器,生命周期子,子代理 生成,会话持久化,追踪传播.


> **【中文解读】**克劳德代理SDK 是人类官方的代理开发框架.核心特性:(1) 内置工具;文件读写;代码执行等;(2) 子 代理支持; 代理可以生成子 代理处理子任务;(3) 生命周期子在代理执行的关键节点插入自定义逻辑.

> **{【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】}**克劳德代理SDK是2026年克劳德生态的核心开发工具. 与OpenAI代理SDK相比,它更重视深入集成克劳德的独特能力 (如扩展思维,计算机使用) ⋅SDK的子代理模式允许代理将复杂任务分解成子任务,每个子任务由专门子代理处理,类似于组织中的部门分工.

>  **【前置】**必须先掌握:阶段14·01(代理循环) 和阶段14·10(技能图书馆) Claude Agent SDK内置了技能系统作为子代理的标准模式.如果你没有使用Claude Code CLI,强烈建议先使用几天本SDK就是Claude Code的库形式,理解CLI的行为模式对学习SDK的事半功倍.

## 概念的核心概念

### 客户端 SDK VS 代理 SDK

- **Client SDK (`anthropic`).**你拥有循环,工具,状态.
- **Agent SDK (`claude-agent-sdk`).**集成的工具执行,MCP连接,子,子弹产,会议存储.

> **Client SDK（`anthropic`）。**您自己管理循环、工具和状态──
> **Agent SDK（`claude-agent-sdk`）。**内置工具执行、MCP 连接、子、子 代理 生成、会话存储──Claude Code 循环库形式──

### 嵌入式工具

 SDK 运输出10多种工具:文件阅读/写, shell, grep, glob, web fetch等. 通过标准工具方案接口进行自定义工具注册.

>  SDK 开箱提供 10+ 工具:文件读写, shell,grep,glob,网页抓取等.

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

### 子

两种目的由人类记录:

> 人类文档记录了两个用途:

1. **Parallelization.**同时执行独立工作. "找到每个20个模块的测试文件"是20个并行的子组任务.
2. **Context isolation.**们使用自己的背景窗口;只有结果返回管家.管家的预算被保存.

最近添加的Python SDK: `list_subagents()`现在`get_subagent_messages()`阅读副本文稿.

> 现在,我们可以在 Python SDK 上找到一个新的功能.`list_subagents()`,我知道.`get_subagent_messages()`为了读取代理的对话记录.

>  **【类比】**作为一个大公司的"项目组":CEO (主代理) 抓取整个局面,但每个具体项目由专门的项目组 (子代理) 执行,项目组有独立会议室 (独立上下文窗口) .**关键收益是上下文隔离**经验人员:如果"调研竞标"这样的工作要读100篇文章塞满上下文,主经理自己做就会被淹没;交给子经纪人,子经纪人100篇文章阅读不会污染主经纪人的视野,只返回"竞标分析的3个结论"――

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

### 会议商店

与TypeScript的协议平衡:

> 与TypeScript版本的协议对等:

- `append(session_id, message)`加一个转.
- `load(session_id)`恢复对话.
- `list_sessions()`列出.
- `delete(session_id)`                     
- `list_subkeys(session_id)`列出子键.

`--session-mirror`通过传输,将转录映射到外部文件中,用于调试.

> `--session-mirror`通过传输过程将对话记录镜像到外部文件中,用于调试.

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

### 子

您可以注册的生命周期:

> 可注册的生命周期子:

- `PreToolUse`现在`PostToolUse` 门户或审计工具的通话.
- `SessionStart`现在`SessionEnd`建立和拆除.
- `UserPromptSubmit`在模型看到之前,在用户输入上采取行动.
- `PreCompact`在文本紧缩之前运行.
- `Stop`在代理出口时进行清理.
- `Notification`侧通道警报.

子是如何支持工作流程 (阶段14课程参考) 和类似的系统增加跨界行为.

> 子是专业工作流 (第14阶段课程参考) 和类似系统添加横切行为方式.

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

###  W3C 追踪环境

通过W3C跟踪语境标题,在调用器上活动的OTel跨度通过CLI子进程传播到后端.整个多进程跟踪显示为一个跟踪.

> 调用方上活跃的OTel跨度 通过W3C 追踪上下文头传播到CLI 子进程――整个多进程追踪在你的后端显示为一个追踪――

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

### 克劳德管理了代理人

托管的替代方案 (beta 头条`managed-agents-2026-04-01`长期的异步工作,内置快速缓存,内置紧缩,管理基础设施的贸易控制.

> 托管替代方案`managed-agents-2026-04-01`长时间运行的异步工作,内置提示缓存,内置压缩――使用控制权换取托管基础设施――

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

### 在这个模式出现错误的地方

> ️ **【易错点】**最常见的灾难:为100个小任务生成100个子代理.**后果**个子代理有自己的系统提示+工具注册+上下文初始化,开销30-60秒/个,100个就是1小时;并发又有限制(人类每分钟代币限制),最终任务跑一晚上。**一行修复**只有真正需要"独立上下文窗口"的任务 (如深度调研)才能产生子代理──

- **Subagent over-spawn.**让100个小任务完成100个小任务. 总体占主导地位.
- **Hook creep.**每个团队都会增加子,启动时间气球,每季度检查子.
- **Session bloat.**会议积累,规模增加.`list_sessions`退出政策

>  **【困惑】**问:Claude Agent SDK 和直接使用人类的Python SDK 写代理循环 有什么本质区别?为什么要使用 SDK?**内置工具开箱即用**文件,,等 10+ 工具,自己写至少两天);(2) **Session 持久化协议**(包括子代理 会话级联删除);(3) **Hook 生命周期**如果你的代理人只是简单的问题,用人类 SDK就足够了;如果要写克劳德代码那种生产级代理,SDK省你几周工程时间.

> **子 Agent 过度生成。**为100个小任务生成100个小任务代理――开销占主导――转换为批量处理――
> **钩子膨胀。**每个团队都加子;启动时间膨胀.
> **会话膨胀。**会话不断积累;大小增长──使用 `list_sessions`过期策略――

## 建立它,实现它.
```figure
ae-subagent-isolation
```

## 建立它

`code/main.py`在 stdlib 中实现SDK形状:

> `code/main.py`用标准库实现了SDK的形态:

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

- `Tool`现在`ToolRegistry`具有内置的`read_file`现在`write_file`现在`list_dir`现在,我们要去.
- `Subagent`私人环境,孤立运行,结果返回.
- `SessionStore`添加,加载,列表,删除,列表_子键.
- `Hooks` `pre_tool_use`现在`post_tool_use`现在`session_start`现在`session_end`现在,我们要去.
- 演示:主代理并行生成3个子组 (每个单独),总结结果,持续会议.

运行它:

```
python3 code/main.py
```

痕迹显示了亚级文本隔离 (乐队主持人文本尺寸保持限制),执行和会议持久性.

> 追踪显示子 代理的上下文隔离 编排者上下文大小保持有界) 子执行和会话持久化

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

## 用它实现框架

- **Claude Agent SDK**对于需要Cloed Code的产品来说,
- **Claude Managed Agents**对于长期的主机无同步工作.
- **OpenAI Agents SDK**(第16课) 对OpenAI首批对手.
- **LangGraph + custom tools**如果您想要图形状态机,

## 运送它.

`outputs/skill-claude-agent-scaffold.md`提供了Claude Agent SDK应用程序,包括子弹,子,会议存储,MCP服务器附件,以及W3C的痕迹传播.

> `outputs/skill-claude-agent-scaffold.md`建立一个Claude Agent SDK 应用程序,包含子 Agent、子、会话存储、MCP 服务器连接和W3C 追踪传播──

> 劳德代理SDK 是人类的官方代理 框架──核心概念:代理 带系统提示和工具的LLM) 工具 可调用函数) 配套 子代理委派) 会议商店 会话持久化) ⋅

## 练习题

1. 加入一个分组分组分20项任务为5个平行分组分组的分组分组分组. 测量管弦器背景大小与每项任务的一个.
  中文翻译:思考并实践此练习──
2. 实施一个`PreToolUse`住这些利率限制`write_file`追踪行为.
  中文翻译:思考并实践此练习──
3. 电线`list_subkeys`树的树是什么样子?
  中文翻译:思考并实践此练习──
4. 把玩具带到真实世界里`claude-agent-sdk`工具注册的变化是什么?
  中文翻译:思考并实践此练习──
5. 你从自主托管转到管理的时间?
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent SDK | "Claude Code as a library" | Harness shape: tools, MCP, hooks, subagents, session store |  |
| Subagent | "Child agent" | Separate context, own budget; results bubble up |  |
| Session store | "Conversation DB" | Persist, load, list, delete turns with subagent cascade |  |
| Hook | "Lifecycle callback" | Pre/post tool, session, prompt submit, compact, stop |  |
| W3C trace context | "Cross-process trace" | Parent span propagates into CLI subprocess |  |
| Managed Agents | "Hosted harness" | Anthropic-hosted long-running async work |  |
| `--session-mirror` | "Transcript mirror" | Writes session turns to an external file as they stream |  |
| MCP server | "Tool surface" | External tool/resource source attached to the agent |  |

## 继续阅读 继续阅读

- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)克劳德代码的图书馆形式
  中文翻译:见原文.
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)生产模式
  中文翻译:见原文.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) 接待的替代方案
  中文翻译:见原文.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)对应
  中文翻译:见原文.
