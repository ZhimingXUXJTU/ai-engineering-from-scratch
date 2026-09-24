# 开通电气通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通讯通

> 开通通信的GenAI SIG (于2024年4月推出) 定义了代理遥测标准方案.跨域名称,属性和内容捕获规则在供应商之间融合,因此代理痕迹在Datadog,Grafana,Jaeger和Honeycomb中意味着相同的东西.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## 学习目标

- 命名GenAI跨度类别:模型/客户端,代理,工具.
- 区分`invoke_agent`客户与内部范围,以及当每一个应用时.
- 列出最高级别的GenAI属性:提供商名称,请求模型,数据源ID.
- 解释内容捕获合同:选择,`OTEL_SEMCONV_STABILITY_OPT_IN`其他国家

## 问题 问题引入

> **【中文解读】**每个供应商都发明了自己的跨度名称,运维团队最终需要为每个框架构建独立的仪表盘.

每个供应商都发明了自己的跨度名称. 运营团队最终构建每个框架的仪表板. OpenTelemetry的GenAI SIG通过定义一个标准来解决这个问题.

> 每个供应商都发明了自己的跨度名称――运维团队最终需要为每个框架构建独立的仪表盘――OpenTelemetry的GENAI SIG通过定义一个全生态系统遵循的标准来解决这个问题――

> **【拓展：OTel GenAI 规范的跨平台统一】**开通通讯GenAI语义约定 (2024年4月启动) 定义了代理遥测的标准方案:跨供应商统一范围名称,属性和内容捕获规则,使代理追踪在数据狗、图形、杰克和蜂蜜中具有相同语义──一次埋点,多后端通用──

>  **【前置】**学本节前请先掌握:阶段14·01(代理循环) 你需要先有代理才能给它埋点;阶段14·13(长图) 理解状态图,因为跨度的父子层级就是图遍历的镜像.如果完全没有接触过OpenTelemetry(不知道是什么跨度、痕迹、文本传播),先看OTel 官方Python 快速进入本节只讲GenAI 专属约定,不重讲OT基础.

## 概念的核心概念

### 跨度类别

>  **【类比】**医院的分级诊断记录:**Model span**是化验单(最底层,记录"抽了多少血"",用什么仪器"",结果多少"对应代币 数"",模型名"",延迟);**Agent span**是门诊病历 (从挂号到离开的整个过程,包括多次化验);**Tool span**是检查项目,每次都是独立的操作.`parent_span_id`链回父记录这样的数据库里你能展开看:整个代理调用 → 5次工具调用 → 每次工具调用里 2次 LLM调用。

1. **Model / client spans.**覆盖原始的LLM调用.由供应商SDK (Anthropic,OpenAI,Bedrock) 和框架模型适配器发行.
2. **Agent spans.** `create_agent`(当代理人构建时) 和`invoke_agent`它们在运行时.
3. **Tool spans.**通过父母-孩子关系连接到代理跨度.

### 代理跨度命名

- 标签:`invoke_agent {gen_ai.agent.name}`如果有名称; 返回`invoke_agent`现在,我们要去.
- 的类型:
  - **CLIENT**用于远程代理服务 (OpenAI助理API,Bedrock代理).
  - **INTERNAL**用于正在进行的代理框架 (LangChain, CrewAI,本地ReAct).

### 关键属性

- `gen_ai.provider.name` `anthropic`现在`openai`现在`aws.bedrock`现在`google.vertex`现在,我们要去.
- `gen_ai.request.model`模型身份证.
- `gen_ai.response.model`解决模型 (可能因路由而不同于请求).
- `gen_ai.agent.name`代理身份证.
- `gen_ai.operation.name` `chat`现在`completion`现在`invoke_agent`现在`tool_call`现在,我们要去.
- `gen_ai.data_source.id`用于RAG:咨询了哪个库或商店.

技术特定的公约存在于人类,Azure AI 推理,AWS 床床,OpenAI.

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

### 内容捕获

> ️ **【易错点】**场景:开发者图省事在`invoke_agent`后果:运维在Jaeger网页里点开就能看到所有明文,Datadog还会索引做全文检索,等于把合规风险扩散到整个观测链路 → 修复:默认关闭内容捕获,需要时只在跨度里存指标 ID(`gen_ai.input.message_id=row42`转发授权访问. 这就是本节反复强调的"外部参考建议".

默认规则:仪器不应默认捕获输入/输出.捕获通过:

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

建议的生产模式:将内容存储外部 (S3,您的日志存储),记录引用在跨度 (指标标识别,而不是散文).这是27课内容中毒防御,以实现可观测性.

> 推的生产模式:将内容外存储 (S3、你的日志存储),在跨度上记录引用 (Index ID,不是原文) .

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

### 稳定性

根据2026年3月的实验性情况,大多数会议都会进行实验性.

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

基因AI在其LLM观察性方案中原生归因.其他后台 (Grafana,Honeycomb,Jaeger) 支持原始属性.

>  **【困惑】**问: `invoke_agent`长时间标签客户端,长时间标签内部?看起来很绕绕着. A: 看被调用的代理不是"另一个进程/服务"――如果你直接在Python 进程中导入LangChain 运行一个 ReAct,这是内部你自己代码内的子调用――如果你调用OpenAI助理API或AWS床包代理,那么远程的HTTP调用,标签客户端――CLIENT 长度也会自动带 RPC 相关属性如(`rpc.system`,我知道.`rpc.service`),方便和传统微服务追踪对齐.

> 基因的原生将 属性映射到其LLM可观测性方案──其他后端(Grafana、Honeycomb、Jaeger) 支持原始属性──

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

### 在这个模式出现错误的地方

- **Capturing full prompts in spans.**信息,秘密,客户数据,可以被操作人员读取.
- **No `gen_ai.provider.name`.**由于缺乏属性,多供应商仪表板会断裂.
- **Spans without parent links.**孤儿工具的范围,总是传播背景.
- **Not setting stability opt-in.**在后端升级时,你的属性可能会被改名.

> **在 span 中捕获完整提示。**运维可读取的追踪包含PII、密钥、客户数据──外部存储──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具跨度──始终传播上下文──
> **不设置稳定性选择加入。**你的属性可能会在后期升级时被重新命名.

## 建立它,实现它.
```figure
ae-genai-span-tree
```

## 建立它

`code/main.py`执行与GenAI公约相匹配的 stdlib跨度发射器:

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

- `Span`通过Genai属性方案.
- `Tracer`随着`start_span`它们是嵌的.
- 发射一个编写的代理:`create_agent`现在`invoke_agent`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`chat`对于法学士的电话.
- 内容捕获模式,可以将外部提示存储并记录跨度上的身份证.

运行它:

```
python3 code/main.py
```

输出:包含所有所需的GenAI属性的跨度树,以及显示选择内容引用的"外部存储器".

> 输出:一个包含所有必需的GenAI属性跨度树,以及一个显示选择加入内容引用的"外部存储".

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

## 用它实现框架

- **Datadog LLM Observability**图表属性原生.
- **Langfuse / Phoenix / Opik**自动工具生态系统.
- **Jaeger / Honeycomb / Grafana Tempo**原始 OTel 痕迹;从GenAI属性构建仪表板.
- **Self-hosted**使用GenAI处理器运行OTel收藏器.

## 运送它.

`outputs/skill-otel-genai.md`电线 OTel GenAI 扩展到现有代理,具有内容捕获默认和外部参考存储.

> `outputs/skill-otel-genai.md`将 OTel GenAI跨度 接入现有代理,包含内容捕获默认值和外部引用存储.

> 开放电气 GenAI 语义约定定义了LLM和代理的可观测性标准.`gen_ai.request.model`,我知道.`gen_ai.usage.input_tokens`,我知道.`gen_ai.agent.name`其他

## 练习题

1. 工具你的课01 复制循环`invoke_agent`通过一个Jaeger实例来传输.
  中文翻译:思考并实践此练习──
2. 在"仅引用"模式中添加内容捕获:提示到SQLite,跨度属性只包含行ID.
  中文翻译:思考并实践此练习──
3. 阅读规格`gen_ai.data_source.id`把它带到你的第09课时的搜索中.
  中文翻译:思考并实践此练习──
4. 设置`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`检查你的属性不会被收藏人改名.
  中文翻译:思考并实践此练习──
5. 构建仪表板:仅仅从GenAI属性中"哪些工具错误与哪些模型相关".
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## 继续阅读 继续阅读

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)规格
  中文翻译:见原文.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) 默认的GENAI范围
  中文翻译:见原文.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) 内部的OTel跨度
  中文翻译:见原文.
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) W3C 追踪环境传播
  中文翻译:见原文.
