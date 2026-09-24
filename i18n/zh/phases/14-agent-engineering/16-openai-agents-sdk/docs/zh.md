# 打开AI代理SDK: 传递,护卫,追踪

> 开放AI代理SDK是基于响应API的轻量级多代理框架.五个原始:代理,Handoff,守护轨道,会议,追踪.Handoffs是命名的工具.`transfer_to_<agent>`导入或输出时,防护轨道会发生故障.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## 学习目标

- 举个OpenAI代理SDK的五个原始元素.
- 解释交付:为什么它们被模拟为工具,模型看到什么名称形状,以及如何转移文本.
- 区分输入护,输出护和工具护;解释`run_in_parallel`阻塞模式
- 执行一个随时运行的时间,使用手柄 + 护 + 跨度式追踪.

## 问题 问题引入

无法清洁地委托的代理最终将所有内容都填入一个提示中.没有护的代理运输PII,违反政策输出或永远循环.OpenAI的SDK编码了使多代理工作易于处理的三个原始.

> 无法干净地委派任务的代理最终将所有东西塞进一个提示词中. 没有护理的代理会泄露PII,输出违反政策内容或永远循环.


> **【中文解读】**开放AI代理SDK(原 Swarm) 是OpenAI官方的代理开发框架──三大核心概念:(1) 交付代理之间的任务转移;(2) 护输入/输出安全护;(3) 追踪内置开放电识 追踪──SDK的设计哲学是'简洁至上'使用最小抽象实现最常见的代理模式──

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}**开放AI代理SDK是2025-2026年最流行的轻量级代理框架.其交付模式将多个代理合作建模为'接力赛'一个代理完成自己的部分后将控制权转移给下一个.

>  **【前置】**必须先掌握:阶段14·01(代理循环) 和阶段14·06(工具使用) OpenAI代理SDK就是这些概念的产品化封装――还需要熟悉OpenAI答案API(不是旧的聊天完成API),因为SDK是基于答案API构建的――

## 概念的核心概念

### 五个原始

1. **Agent.**士师资格:指令:工具:手工
2. **Handoff.**代表于模型作为一个名为工具`transfer_to_<agent_name>`现在,我们要去.
3. **Guardrail.**验证输入 (仅为第一代理),输出 (仅为最后代理) 或工具调用 (每个函数工具).
4. **Session.**交换时间的自动对话历史.
5. **Tracing.**专业化专业的代人,工具调用,交付,护卫.

### 作为工具的手渡

模型看到`transfer_to_billing_agent`运行时间的信号是:

> 模型在工具列表中看到`transfer_to_billing_agent`调用它意味着运行时需要:

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

1. 复制对话背景 (或通过 `nest_handoff_history`其他类型
2. 启动目标代理,并提供指示.
3. 继续与目标代理进行逃跑.

这就是监督模式 (课13/课28),

> 这就是产品化后的监督者模式 (第13课/第28课)

>  **【类比】**听完病人描述后说"你去心脏科"这就是`transfer_to_cardiology_agent`患者 (患者) 对话上下文) 从分诊台转到心脏科诊室,心脏医生接管**关键**作为一个"专家"的监督者,他只会"派遣"专家.

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

### 防护

它们有三个味道:

> 三种类型:

- **Input guardrails.**在任何LLM电话之前,拒绝不安全或不适合的请求.
- **Output guardrails.**检查了最后一个特工的输出,检查了个人信息泄露,违反政策,错误的反应.
- **Tool guardrails.**运行每个函数工具,验证参数,检查权限,审计执行.

模式:

> 模式:

- **Parallel**门线路LLM与主LLM一起运行. 低尾延迟. 如果脚,主LLM的工作会被丢弃 (代币浪费).
- **Blocking**(`run_in_parallel=False`如果,没有代币浪费在主调用.

三线电升级`InputGuardrailTripwireTriggered`现在,`OutputGuardrailTripwireTriggered`现在,我们要去.

> 触发器会抛出`InputGuardrailTripwireTriggered`现在,`OutputGuardrailTripwireTriggered`异常.

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

### 追踪

默认启动. 每一个LLM代,工具调用,交付,和防护线都发出一个跨度.`OPENAI_AGENTS_DISABLE_TRACING=1`选择退出.`add_trace_processor(processor)`粉丝的范围扩展到你自己的后端,

> 默认开启. 每次LLM 生成,工具调用,交接和护都会发出一个跨度.`OPENAI_AGENTS_DISABLE_TRACING=1`可以选择退出.`add_trace_processor(processor)`它们可以同时发送到你的后端和OpenAI后端.

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

### 会议

`Session`存储对话历史在后端 (SQLite,Redis,定制). `Runner.run(agent, input, session=session)`汽车装载和附加.

> `Session`在后端(SQLite、Redis、自定义) 存储对话历史──`Runner.run(agent, input, session=session)`自动加载和加载

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

### 在这个模式出现错误的地方

> ️ **【易错点】**转移漂移 (交接循环):Agent A 移交给B,B 又移交给A,A 再移交给B...无限循环烧代币――**后果**现在,我们必须做一个任务.**一行修复**运行者 里加跳计数器`max_handoffs=5`),超过就抛 `HandoffBudgetExceeded`异常――OpenAI SDK默认没有这个保护,必须自己加.

- **Handoff drift.**代理A向B递交,B向A递交.
- **Guardrail bypass.**工具防护只会在功能工具上使用;内置工具 (文件阅读器,网页搜索) 需要单独的政策.
- **Over-tracing.**结与OTel GenAI内容捕获规则 (课3) 存储外部,引用通过ID.

>  **【困惑】**答:不一定. 平行是主 LLM 和 guardrail LLM 同时运行"快但浪费代币"快但浪费代币(guardrail 触发时主 LLM 已经在运行,代币已花费) ・ 阻行是"先的 guardrail,过了重复主 LLM"慢但省钱.**选择规则**防护 触发率高 (如 >20%),用阻省钱;如果触发率低 (如 <5%),用平行省延迟。

> **交接漂移。**代理A交给B,代理B又交给A.
> **护栏绕过。**工具护只需要在函数工具上触发;内置工具 (文件读取器,网页抓取) 需要单独的策略.
> **过度追踪。**包含敏感内容. 配合OTel GenAI 内容捕获规则.

## 建立它,实现它.
```figure
ae-agent-handoff
```

## 建立它

`code/main.py`在 stdlib 中实现SDK形状:

> `code/main.py`用标准库实现了SDK的形态:

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

- `Agent`现在`FunctionTool`现在`Handoff`(作为一个功能工具,具有传输语义).
- `Runner`配备输入/输出/工具防护,送货和跳转计数器.
- 简单的跨度发射器显示痕迹形状.
- 根据用户的查询,交付账单或支持的分类代理;在一个输入时,防护轨道旅行.

运行它:

```
python3 code/main.py
```

痕迹显示了两次成功的转让, 一次输入护旅行,

> 追踪显示了两次成功的交互,一次输入,以及一个反映了真实的SDK输出跨度.

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

## 用它实现框架

- **OpenAI Agents SDK**对于OpenAI首批产品.
- **Claude Agent SDK**(课 17) 对克劳德第一产品.
- **LangGraph**需要明确的状态和持久的简历.
- **Custom**当你需要精确的控制 (语音,多供应商,联合部署).

## 运送它.

`outputs/skill-agents-sdk-scaffold.md`配备一个Agents SDK应用程序,包括分类代理,手持,输入/输出/工具护,会议存储器和追踪处理器.

> `outputs/skill-agents-sdk-scaffold.md`建立一个代理 SDK 应用程序,包含分诊 Agent、交接、输入/输出/工具护、会话存储和追踪处理器──

> 提供四种核心概念:代理 (带指令和工具的LLM) ‧ 交付 (Handoffs) ‧ 代理 (间移交) ‧ 护卫 (Gardrails) ‧输入/输出验证) ‧ 追踪 (运行追踪) ‧ 生产级 代理 (开发框架)).

## 练习题

1. 加入一个转发跳计:N转移后拒绝.
  中文翻译:思考并实践此练习──
2. 实施`nest_handoff_history`在转移之前,将先前的信息分解成一个总结.
  中文翻译:思考并实践此练习──
3. 写一个阻断输出防护护,比较会使它脚的提示和通过的提示的延迟.
  中文翻译:思考并实践此练习──
4. 电线`add_trace_processor`它们每次发射的形状是什么?
  中文翻译:思考并实践此练习──
5. 读取 SDK 文件,将你的玩具移植到`openai-agents-python`你错了什么模型?
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## 继续阅读 继续阅读

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)原始品,手渡,护卫,追踪
  中文翻译:见原文.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) 克劳德味的同类
  中文翻译:见原文.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)什么时候可以向人提供手柄
  中文翻译:见原文.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)标准的代理SDK范围为
  中文翻译:见原文.
