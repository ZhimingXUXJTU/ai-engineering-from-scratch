# 开通通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通通

> 一个代理人打电话给五个工具,三个MCP服务器, 你需要一个痕迹. 开通通讯GenAI语义公约 (v1.37及以上的稳定属性) 是2026年标准,由Datadog,Langfuse,Ariz Phoenix,OpenLLMetry和AgentOps本地支持. 这一课列出所需属性,走向跨度层次 (代理 -> LLM -> 工具),并发送一个可以连接到任何OTel出口商的 stdlib跨度发射器.

> **【中文解读】**代理调用5个工具、3个MCP 服务器、2个子 代理,需要一个穿越全程的追踪──OpenTelemetry GenAI 语义约定(v1.37+ 稳定属性) 是2026年标准,达达多格/长/Arize Phoenix/OpenLLMetry/AgentOps 原生支持──本课名必需属性、走通跨层结构(代理 -> LLM ->任何工具),提供可接入的OTEL 导器的标准库跨度发射器──

> **【拓展】**开通通信是AI应用从实验到生产的必备可观测性基础设施.OTel GenAI 语义约定定义了稳定的属性名称,使得Datadog、长、尼克斯等后端都能解析相同的跨度.一次仪表化,发送到任何后端.

>  **【前置】**学习节前请先掌握:(1) 阶段 13·07、08(MCP服务器/客户端) 要在MCP调用上加跨度;(2) 开放电气基础 基础 追踪,跨度,跨度背景,出口;(3) 分布式追踪概念 追踪_id、跨度_id、父母_id;(4) W3C追踪式 头格式跨进程上下文传播。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, OTel span emitter) | **语言:** Python (stdlib, OTel span emitter)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 指定为LLM跨度和工具执行跨度所需的OTel GenAI属性.
  中文翻译:命名 LLM 跨度和工具执行跨度的必需 OTel GenAI 属性。
- 建立一个覆盖代理循环,LLM调用,工具调用和MCP客户端发送的跟踪层次.
  中文翻译:构建覆盖 代理循环、LLM 调用、工具调用和MCP 客户端分发的痕迹层次──
- 决定要捕获 (选择) 和编辑 (默认) 内容.
  中文翻译:决定捕获哪些内容(选择)vs脱敏(默认)。
- 发送到本地收藏器 (Jaeger,Langfuse) 无需重写工具代码.

> **【中文解读】**学习目标:掌握OTel GenAI必需属性(LLM跨度和工具执行跨度);构建覆盖代理循环、LLM调用、工具调用和MCP 客户端分发的痕迹层次;决定捕获哪些内容(opt-in)vs 脱敏(默认);发送跨度到本地收集器──

## 问题 问题引入

> **【中文解读】**调试场景:用户报告"代理有时30秒响应,有时3秒"――没有追踪,日志只显示LLM调用,看不到工具分发、MCP 服务器往返、子代理――最终发现一个MCP 服务器冷启动偶尔卡住――没有端到端追踪就无法发现这种问题――

2026年2月的一个调试:用户报告"我的代理有时需要30秒来响应;有时需要3秒".没有痕迹.日志显示了LLM电话,但不是工具发送,不是MCP服务器回路,不是子代理.你猜.最终你发现:一个MCP服务器偶尔挂在冷启动上.

> 2026 年 2 月的调试:用户报告"我的代理有时30秒响应;有时3秒"――没有追踪――日志显示LLM调用,但不显示工具分发、MCP 服务器往返、子代理――你猜测――最终你发现:一个MCP 服务器在冷启动时偶尔卡住――

没有端到端追踪,你就找不到这个.

> 没有端到端追踪,你找不到这个.

>  **【类比】**分布式追踪像快递的"物流单号"――你寄一个包裹 (用户请求),途经多个中转站 (代理) → LLM →工具 (工具) → MCP服务器),每个站点扫一次单号 (生成一个跨度)――最后你能看到一个时间线:"9:01 寄出 → 9:02 收件 → 9:05 分拣 → 9:30 转运 → 9:45 送"――OTel GenAI 是快递公司约定的"扫码字段标准" 每家公司(Datadog/Langfuse) 都按相同字段(gen_ai.operation.name等) 记录,所以你换物流公司时不需要重新贴单.

根据OpenTelemetry语义会议组,这些公约在2025-2026年结合.它们定义了稳定的属性名称,因此Datadog,Langfuse,Phoenix,OpenLLMetry和AgentOps都分析相同的范围.

> 约定在 2025-2026年在OpenTelemetry 语义约定组下稳定.它们定义稳定属性名称,使数据犬,长,enix,OpenLLMetry和代理Ops都解析相同的跨度.一次仪表化;发送到任何后端.

## 概念的核心概念

> **【中文解读】**本节详解跨层结构(agent.invoke_agent -> llm.chat -> tool.execute -> mcp.call) 、必需属性(gen_ai.* 命名空间)、跨层 类型(CLIENT/INTERNAL)、opt-in 内容捕获、跨事件、导出器、跨MCP 传播、指标和 AgentOps 层。

### 跨度等级

> **【中文解读】**跨度层次:agent.invoke_agent(顶层INTERNAL span) -> llm.chat(CLIENT span) ->工具.执行(INTERNAL) -> mcp.call(CLIENT span) ――整个结构嵌套在一个追踪 id 下,跨度 id 链接子关系。

```
agent.invoke_agent  (top, INTERNAL span)
 ├── llm.chat       (CLIENT span)
 ├── tool.execute   (INTERNAL)
 │    └── mcp.call  (CLIENT span)
 ├── llm.chat       (CLIENT span)
 └── subagent.invoke (INTERNAL)
```

整个东西都在一个痕迹身份证下, 跨度身份证将父母与孩子的关系联系起来.

> 整个嵌套在一个痕迹ID 下面.

> ️ **【易错点】**场景:跨进程调用MCP服务器 时不传 traceparent / 后果:客户端的痕迹 在MCP调用处破裂,看到的是"工具.执行100ms 完成",但看不到MCP服务器 内部到底卡在哪里;多个独立的痕迹 无法串联 / 修复:(1) HTTP 调用MCP 时在头条加`traceparent: 00-<trace_id>-<span_id>-01`通过将文本序列化到JSON-RPC `params._meta.trace_context`接收端取出文本 续接跨度――没有上下文传播,分布式追踪就是空话――

>  **【困惑】**问: 里应该记录完整的快速和响应吗?**不记录**只有记得长度和符号数.原因:**隐私**即时 含用户敏感信息;(2) **存储成本**大量请求时全量记录会让后端存储爆炸;**合规**GDPR/CCPA 要求最小化数据收集.`gen_ai.content.capture=full`选择存储,加密存储+短期TL。

### 要求属性

根据2025-2026年学期:

- `gen_ai.operation.name` `"chat"`现在`"text_completion"`现在`"embeddings"`现在`"execute_tool"`现在`"invoke_agent"`现在,我们要去.
  翻译: 中文`gen_ai.operation.name`操作名`"chat"`,我知道.`"text_completion"`,我知道.`"embeddings"`,我知道.`"execute_tool"`,我知道.`"invoke_agent"`
- `gen_ai.provider.name` `"openai"`现在`"anthropic"`现在`"google"`现在`"azure_openai"`现在,我们要去.
  翻译: 中文`gen_ai.provider.name`提供商名.
- `gen_ai.request.model`要求的模型字符串 (例如 `"gpt-4o-2024-08-06"`)
  翻译: 中文`gen_ai.request.model`请求的模型字符串──
- `gen_ai.response.model`模型实际上是服务的.
  翻译: 中文`gen_ai.response.model`实际服务的模型.
- `gen_ai.usage.input_tokens`现在,`gen_ai.usage.output_tokens`现在,我们要去.
  翻译: 中文`gen_ai.usage.input_tokens`现在,`gen_ai.usage.output_tokens`输入/输出代币 数量
- `gen_ai.response.id`提供商响应ID对相关性.
  翻译: 中文`gen_ai.response.id`提供商响应 id 用于关联

对于工具跨度:

> 对工具的时间:

- `gen_ai.tool.name`工具标识符
  翻译: 中文`gen_ai.tool.name`工具标识符──
- `gen_ai.tool.call.id`具体的呼叫身份.
  翻译: 中文`gen_ai.tool.call.id`具体调用 id──
- `gen_ai.tool.description`工具描述 (可选).
  翻译: 中文`gen_ai.tool.description`工具描述 (可选)

对于代理范围:

> 对代理时间:

- `gen_ai.agent.name`现在,`gen_ai.agent.id`现在,`gen_ai.agent.description`现在,我们要去.
  翻译: 中文`gen_ai.agent.name`现在,`gen_ai.agent.id`现在,`gen_ai.agent.description`代理名/id/描述──

### 子类型

- `SpanKind.CLIENT`通过进程边界 (LLM提供商,MCP服务器) 的呼叫.
  翻译: 中文`SpanKind.CLIENT`为了跨进程边界调用 (LLM 提供商,MCP 服务器)
- `SpanKind.INTERNAL`对于代理人的自行循环步骤和工具执行.
  翻译: 中文`SpanKind.INTERNAL`用于执行代理自身的循环步骤和工具.

### 选择内容捕获

默认情况下,跨度载有指标和时间,而不是提示或完成. 大型有效载荷和 PII默认关闭. 设置 `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`内容的含量,在启用中仔细审查.

> 默认情况下, 跨度 携带标标和计时而不是快速或补充全.`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`和特定内容捕获环境变化以包含内容. 在生产中启动前仔细审查.

### 跨度事件

代币级事件可以作为跨度事件添加:

> 标签 级事件可作为跨度 事件添加:

- `gen_ai.content.prompt`输入信息.
  翻译: 中文`gen_ai.content.prompt`输入消息.
- `gen_ai.content.completion`输出消息.
  翻译: 中文`gen_ai.content.completion`输出消息.
- `gen_ai.content.tool_call` 工具调用记录.
  翻译: 中文`gen_ai.content.tool_call`记录的工具调用――

事件时间顺序在一个时间段内进行详细重播.

> 事件在时间内按时间排序,用于详细回放.

### 出口商

欧特尔向:

- **Jaeger / Tempo.**局部,现场.
  翻译: 中文**Jaeger / Tempo。**开源,本地部署
- **Langfuse.**具有可观性特异性;可视化代币使用.
  翻译: 中文**Langfuse。**专业可观测性;可观化代币使用
- **Arize Phoenix.**总数: 总数:
  翻译: 中文**Arize Phoenix。**评估+追踪结合――
- **Datadog.**商业;本地解析`gen_ai.*`它们的属性.
  翻译: 中文**Datadog。**商业;原生解析`gen_ai.*`属性
- **Honeycomb.**专导向; 查询友好.
  翻译: 中文**Honeycomb。**列式存储;查询友好──

它们都用OTLP,电线格式.

> 您的代码不关心.

### 跨MCP传播

当MCP客户端调用服务器时,将W3C追踪头标注入请求中.流式HTTP支持标准头标.Stdio不原生地携带HTTP头标;规范的2026路线图讨论添加一个`_meta.traceparent`在JSON-RPC调用时的字段.

> 当MCP 客户端调用服务器时,将 W3C 追踪头注入请求――可流动的 HTTP 支持标准头――studio 原生不携带 HTTP 头;规范 2026 路线图讨论在 JSON-RPC 调用上添加`_meta.traceparent`字段.

加入其后方的 `_meta`服务器将记录了追踪身份.

> 直到那时:手动在每一个请求.`_meta`中包含追踪者──服务器记录追踪身份──

### 计量

除了跨度之外,GenAI semconv也定义了指标:

> 除了跨度外,GenAI 语义约定定义指标:

- `gen_ai.client.token.usage`    
  翻译: 中文`gen_ai.client.token.usage`直方图──
- `gen_ai.client.operation.duration`    
  翻译: 中文`gen_ai.client.operation.duration`直方图──
- `gen_ai.tool.execution.duration`    
  翻译: 中文`gen_ai.tool.execution.duration`直方图──

对于不需要每次通话的详细信息的仪表板,使用这些.

> 用这些做不需要每调用详细的仪表盘.

### 代理Ops 层

代理Ops (成立于2024年) 专注于GenAI可观测性.它包裹着受欢迎的框架 (LangGraph,Pydantic AI,CrewAI) 以自动发射OTel跨度.如果您的堆使用支持的框架,则有用;否则使用手动仪器.

> 专注于GenAI可观测性――它包装流行框架(长图、皮达因 AI、 CrewAI) 自动发出OTel跨度――如果你的技术使用支持的框架则有用;否则使用手动仪表化――

## 用它实现框架

> **【中文解读】** `code/main.py`向 stdout 发射 OTLP-JSON 格式的跨度,覆盖一个代理 调用LLM、分发两个工具、进行一次MCP 往返──无真实导出器课程聚焦跨度 形状和属性集──关注点:追踪 id 跨所有跨度 共享;父子链接通过 parentSpanId 编码;`gen_ai.*`必须属性已填充;内容获取默认关闭.
```figure
t3-span-waterfall
```

## 用它

`code/main.py`发出OTel形状的跨度到stdout (OTLP-JSON类似格式) 代理调用LLM,发送两个工具,并完成一个MCP回路.没有真正的出口商课程专注于跨度形状和属性集.将输出粘贴到OTLP兼容的观众中或简单地阅读.

> `code/main.py`向stdout 发出OTel 形态的跨度(OTLP-JSON 类型),用于调用LLM、分发两个工具、进行一次MCP 往返的代理──无真导出器课程聚焦跨度 形态和属性集──将输出粘贴到OTLP 兼容查看器或直接阅读──

什么要看:

- 随着所有区域的测量,
  中文翻译: 跨所有跨跨共享──
- 通过 编码的父母与孩子的链接`parentSpanId`现在,我们要去.
  中文翻译:父子链接通过 `parentSpanId`编码.
- 需要`gen_ai.*`属性已被填充.
  中文翻译:必需的`gen_ai.*`属性已填充.
- 默认情况下,内容捕获是关闭的;一个情况通过envvar启动.
  中文翻译:内容捕获默认关闭;一个场景通过环境变量开启.

## 运送它.

> **【中文解读】**本课产出发 `outputs/skill-otel-genai-instrumentation.md`给定代理代码库,生成仪表化计划:在哪里添加跨度,填充哪些属性,目标导出器.

这一课产生了`outputs/skill-otel-genai-instrumentation.md`鉴于代理代码基础,技能产生了一个仪器计划:在哪里添加范围,哪些属性被占用,哪些出口者被目标.

> 本课产出发 `outputs/skill-otel-genai-instrumentation.md`◎ 应指定代理 代码库,该技能 生成仪表化计划:在哪里加长时间,填充哪些属性,目标哪些导出器.

## 练习题

1. 跑步`code/main.py`计算时间,确定哪个是客户与内部.
   中文翻译:运行 `code/main.py`△计数跨度并识别哪些是客户与内部.

2. 启用内容捕获 (env var) 并确认`gen_ai.content.prompt`其他`gen_ai.content.completion`观察对 PII 的影响.
   中文翻译:开启内容捕获 (环境变量)并确认`gen_ai.content.prompt`和 `gen_ai.content.completion`事件出现.注意 PII的影响.

3. 添加工具执行指标`gen_ai.tool.execution.duration`并且以每次通话的 histogram 样本发射.
   中文翻译:添加工具执行指标 `gen_ai.tool.execution.duration`并每次调用为直方图样本发出.

4. 传播一个从母体代理跨度到MCP请求的追踪父母`_meta.traceparent`检查MCP服务器会看到相同的追踪身份.
   中文翻译:将追踪父母从父代理跨度 传播到MCP 请求的 `_meta.traceparent`字段──验证 MCP 服务器看到相同的痕迹ID──

5. 读取OTel GenAI semconv规范. 确定本课程代码中没有发射的 semconv中列出的一个属性. 添加它.
   中文翻译:阅读 OTel GenAI 语义约定规范──识别语义约定中列出但本课代码未发出一个属性──添加它──

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| OTel | "OpenTelemetry" | Open standard for traces, metrics, logs | 开放遥测标准 |
| GenAI semconv | "GenAI semantic conventions" | Stable attribute names for LLM / tool / agent spans | GenAI 语义约定 |
| `gen_ai.*` | "The attribute namespace" | All GenAI attributes share this prefix | GenAI 属性命名空间 |
| Span | "Timed operation" | A unit of work with a start, end, and attributes | Span：带属性的时间操作单元 |
| Trace | "Cross-span ancestry" | Tree of spans sharing a trace id | Trace：跨 span 的追踪树 |
| SpanKind | "CLIENT / SERVER / INTERNAL" | Hints about span direction | Span 类型：跨进程/同进程 |
| OTLP | "OpenTelemetry Line Protocol" | Wire format for exporters | OTLP：导出器线格式 |
| Opt-in content | "Prompt / completion capture" | Off by default; env var to enable | 内容捕获：默认关闭 |
| traceparent | "W3C header" | Propagates trace context across services | traceparent：跨服务追踪传播 |
| Exporter | "Backend-specific shipper" | Component that sends spans to Jaeger / Datadog / etc. | 导出器：发送到后端 |

## 继续阅读 继续阅读

- [OpenTelemetry — GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/)基因科学界范围,指标和事件的常规公约
  中文翻译:GenAI跨度、指标和事件的权威约定
- [OpenTelemetry — GenAI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/) LLM和工具执行跨度属性列表
  中文翻译:LLM 和工具执行跨度属性列表
- [OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)代理级`invoke_agent`跨度
  中文翻译:代理级`invoke_agent`跨度
- [open-telemetry/semantic-conventions — GenAI spans](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md) GitHub 托管的真相来源
  中文翻译:GitHub 托管的真相源
- [Datadog — LLM OTel semantic convention](https://www.datadoghq.com/blog/llm-otel-semantic-convention/)生产集成步行
  中文翻译:生产集成演练
