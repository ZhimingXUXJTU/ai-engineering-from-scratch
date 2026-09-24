# 函数调用深入:三大供应商对比

> 在2024年,这三个边境供应商都在同一工具调用循环上汇聚,然后在其他方面分歧.`tools`其他`tool_calls`人类用品`tool_use`其他`tool_result`双胞胎使用`functionDeclarations`这一课将三个字符相对不同,以便在一个提供商上发送的代码在移植时不会破裂.

> **【中文解读】**未来三大前沿供应商将在2024年收到相同的工具调用循环,但具体实现各个差异.`tools`现在,我们要去.`tool_calls`人类用`tool_use`现在,我们要去.`tool_result`块,双胞胎用`functionDeclarations`和唯一的ID 关联──本课三路对比,让你在一个供应商上写的代码转移到另一个时不至于崩──

> **【拓展：Function Calling】**函数调用 (函数调用) 是LLM与外部世界交互的核心机制――LLM 不直接执行操作,而是输出结构化的"调备图" (调备图) 工具名+参数),由主程序执行后返回结果――三大供应商的API形状不同但语义等价:声明工具→模型选择调用→主执行→结果注入→模型继续推理――理解这一循环是构建跨平台代理的基础――

>  **【前置】**首先要掌握: 1) 阶段 13·01 (工具界面) 本节是它的展开,必须先吃四步循环; 2) 阶段 11·03 (结构化输出) 理解JSON方案,三大供应商的`parameters`现在,我们要去.`input_schema`文档――如果不会区分`tool_choice`首先,再看13.01阶段的"决策"步骤.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, schema translators) | **语言:** Python（标准库，模式翻译器）
**Prerequisites:** Phase 13 · 01 (the tool interface) | **前置知识:** Phase 13 · 01（工具接口）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 描述OpenAI,Anthropic和Gemini函数调用有效载荷 (声明,调用,结果) 之间的三个形状差异.
  说明OpenAI、人类、双子 函数调用载荷的三种形态差异(声明、调用、结果) 👇
- 翻译一个工具声明在所有三个供应商格式中,并预测严格模式限制将在哪里不同.
  将一个工具声明 译为三种供应商格式,预测严格 模式约束在哪会不同.
- 使用`tool_choice`在每个提供商中强制,禁止或自动选择工具的呼叫.
  在每个供应商中使用`tool_choice`强制禁止或自动选择工具调用
- 了解每个提供商的硬度限制 (工具数量,方案深度,参数长度) 和每一个用户在违反限制时发出错误签名.
  了解各供应商的硬限制 (工具数量,方案深度,参数长度) 以及违反限制时的错误特征.

## 问题 问题引入

要求调用函数的形状因供应商而异. 2026 年生产堆的三个具体例子:

> 函数调用请求的形式因供应商而异. 以下是2026年生产技术中的三个具体例子:

> **【中文解读】**函数调用请求的格式因供应商而异.`tools`其他`tool_calls`响应中`arguments`是需要手动解析的JSON字符串;`tool_use`现在,我们要去.`tool_result`块,`input`已经是个很好的对象; 双胞胎用嵌套的`functionDeclarations`结果通过`functionResponse`返回. 单个循环,不同的字段名,嵌套方式,字符串与物体定制和关联机制,从一个供应商转移到另一个仅仅需要两三天.

**OpenAI Chat Completions / Responses API.**你通过了`tools: [{type: "function", function: {name, description, parameters, strict}}]`模型的反应包含`choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`在哪里`arguments`必须解析的 JSON 字符串.`strict: true`) 通过限制解码来强制执行方案的合规性.

> **OpenAI Chat Completions / Responses API。**你传入`tools: [{type: "function", function: {name, description, parameters, strict}}]`△模型的响应包含`choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`在其中`arguments`是一个需要你手动解析的JSON字符串.`strict: true`通过约束解码强制执行模式合规.

**Anthropic Messages API.**你通过了`tools: [{name, description, input_schema}]`答案是:`content: [{type: "text"}, {type: "tool_use", id, name, input}]`现在,我们要去.`input`您用新的字符串回复`user`包含一个信息`{type: "tool_result", tool_use_id, content}`区块.

> **Anthropic Messages API。**你传入`tools: [{name, description, input_schema}]`应对`content: [{type: "text"}, {type: "tool_use", id, name, input}]`形式返回.`input`已被解析了,是一个对象,不是字符串.`{type: "tool_result", tool_use_id, content}`块的新`user`消息回复.

**Google Gemini API.**你通过了`tools: [{functionDeclarations: [{name, description, parameters}]}]`(在下面嵌`functionDeclarations`答案是`candidates[0].content.parts: [{functionCall: {name, args, id}}]`在哪里`id`双子座3级以上的通话相关性.`{functionResponse: {name, id, response}}`现在,我们要去.

> **Google Gemini API。**你传入`tools: [{functionDeclarations: [{name, description, parameters}]}]`(嵌套在`functionDeclarations`下) 应应`candidates[0].content.parts: [{functionCall: {name, args, id}}]`形式到达,其中`id`在双子座3及以上版本中是唯一的,用于并行调用关联.`{functionResponse: {name, id, response}}`复制

另一组在OpenAI上写了一篇天气报道,为安特罗皮克支付了两天的港口,另一个天给双胞胎只为管道.

> 同样的循环――不同的字段名,不同的嵌套方式,不同的字符串与对象约定,不同的关联机制――一个在OpenAI上写天气代理的团队移植到人类需要两天,再到双胞胎还需要一天只是管道工程――

>  **【类比】**三大供应商像三种不同的快递公司──都能寄包裹,但运输单格式不同:OpenAI 把物品清单写在面单上需要收件人自己看`arguments`是JSON字符串);人类把清单内容已经填好直接看(`input`已解析对象);Gemini 用专门运单号 UUID 区分包裹(Gemini 3+) ⋅本质都是寄快递,但每个公司运单设计不同,所以你需要一个"统一运单翻译器"才能在多家公司间切换――

这一课程建立了一个翻译器,将三个格式统一成一个正规工具声明和边缘路线.

> 本课程构建一个翻译器,将三种形式统一成一个规范的工具声明,并通过.

## 概念的核心概念

### 公共结构

每个提供商都需要五件事:

> 每个供应商都需要五种东西:

1. **Tool list.**每个工具名称,描述和输入方案.
   翻译: 中文**工具列表。**每个工具的名称,描述和输入模式.
2. **Tool choice.**强迫一个特定的工具,禁止工具,或者让模型决定.
   翻译: 中文**工具选择。**强制使用特定工具,禁止使用工具或让模型自行决定.
3. **Call emission.**结构化输出名称工具和参数.
   翻译: 中文**调用输出。**命名工具和参数的结构化输出
4. **Call id.**相关答案与正确的呼叫 (对平行的情况).
   翻译: 中文**调用 ID。**应关联到正确调调 (关键)
5. **Result injection.**结果与电话联系的消息或封锁.
   翻译: 中文**结果注入。**将结果绑定回调用消息或块.

> **【中文解读】**每个供应商都需要五样东西:工具列表 (名称+描述+输入方案) 工具选择 (强制/禁止/自动) 调用输出 (结构化工具名称和参数) 调用 ID (关联响应到正确调用,并行时关键) 结果注入 (将结果绑定调用消息或块) ⋅

### 形状差异,场次

> ️ **【易错点】**场景:把OpenAI代码原样贴到人类 / 后果:`tool_calls`字段不存在导致`KeyError`开放AI 的`arguments`是字符串需要`json.loads()`人类的`input`已是指,直接访问会得到字符串而不是字段值 / 修复:必须写适配层或使用LiteLLM 这类统一SDK;若手写,每个供应商独立测试用例覆盖──

| Aspect | OpenAI | Anthropic | Gemini |
|--------|--------|-----------|--------|
| 方面 | OpenAI | Anthropic | Gemini |
| Declaration envelope | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| 声明信封 | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| Schema field | `parameters` | `input_schema` | `parameters` |
| Schema 字段 | `parameters` | `input_schema` | `parameters` |
| Response container | `tool_calls[]` on assistant message | `content[]` of type `tool_use` | `parts[]` of type `functionCall` |
| 响应容器 | assistant 消息上的 `tool_calls[]` | `content[]` 中类型为 `tool_use` 的块 | `parts[]` 中类型为 `functionCall` 的条目 |
| Arguments type | stringified JSON | parsed object | parsed object |
| 参数类型 | 字符串化 JSON | 已解析对象 | 已解析对象 |
| Id format | `call_...` (OpenAI generates) | `toolu_...` (Anthropic) | UUID (Gemini 3+) |
| ID 格式 | `call_...`（OpenAI 生成） | `toolu_...`（Anthropic） | UUID（Gemini 3+） |
| Result block | role `tool`, `tool_call_id` | `user` with `tool_result`, `tool_use_id` | `functionResponse` with matching `id` |
| 结果块 | 角色 `tool`，`tool_call_id` | 带有 `tool_result` 的 `user` 消息，`tool_use_id` | 带有匹配 `id` 的 `functionResponse` |
| Force-a-tool | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| 强制工具 | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| Forbid tools | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| 禁止工具 | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| Strict schema | `strict: true` | schema-is-schema (always enforced) | `responseSchema` at request level |
| 严格模式 | `strict: true` | 模式即模式（始终强制执行） | 请求级别的 `responseSchema` |

### 你会真正达到的限制.

> **【中文解读】**开放AI:128 个工具/请求,Schema深度 5,参数字符串 ≤8192 字节,严格 模式不支持 `$ref`现在,我们要去.`oneOf`等重叠组合──人类:64 个工具/请求,Schema 深度无硬限制但实际约10,无严格的模式标志但模型倾向于遵守──Gemini:64 个函数/请求,使用OpenAPI 3.0 子集(与JSON Schema 2020-12 有微小差异),Gemini 3起支持唯一的ID──

- **OpenAI.**参数字符串 <= 8192字节. 严格模式不需要 `$ref`没有`oneOf`现在,我们要去.`anyOf`现在,我们要去.`allOf`任何物件都在`required`现在,我们要去.
  翻译: 中文**OpenAI。**每个请求 128 个工具――方案深度 5――参数符串 ≤ 8192 字节――严格模式要求无`$ref`没有重叠的`oneOf`现在,我们要去.`anyOf`现在,我们要去.`allOf`它们的每个属性都在`required`在中.
- **Anthropic.**没有严格模式的旗;该方案是合同的,模型往往符合.
  翻译: 中文**Anthropic。**每个请求64个工具――方案深度实际上无限制,但实际上约有10个――没有严格的模式标志;模式是契约,模型倾向于遵守――
- **Gemini.**根据要求,可执行 64 个函数. 方案类型是OpenAPI 3.0 子集 (与 JSON Schema 2020-12 略有差异).
  翻译: 中文**Gemini。**每个请求 64 个函数──Schema 类型是 OpenAPI 3.0 子集(与 JSON Schema 2020-12 有微小的差异──Gemini 3 起支持并行调用的唯一 ID──

>  **【困惑】**问:既然有三种不同形状,为什么不直接使用LangChain或LiteLLM抽象掉?`$ref`) `tool_choice`没有人性`required`◎ 错误格式差异不会被抽象化. ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

### `tool_choice`行为

每个人都支持的三个模式,不同的名称.

> 供应商都支持三种模式,但名称不同.

- **Auto.**模型选择工具或文字.默认.
  翻译: 中文**自动。**模型选择工具或文本──默认值──
- **Required / Any.**模型必须至少调用一个工具.
  翻译: 中文**必需 / 任意。**模型必须至少调用一个工具.
- **None.**模型不能叫工具.
  翻译: 中文**无。**模型必须调用工具.

另外,每个提供商都有一个独特的模式:

> 另外,每个供应商都有一个独特模式:

- **OpenAI.**强迫一个特定的工具,以名字.
  翻译: 中文**OpenAI。**按名称强制特定工具.
- **Anthropic.**强制使用一个特定的工具,以名字;`disable_parallel_tool_use`标志分开单个与多个.
  翻译: 中文**Anthropic。**按名称强制特定工具;`disable_parallel_tool_use`标志区分单次和多次调用――
- **Gemini.** `mode: "VALIDATED"`通过一个方案验证器,无论模型意图如何,将每个响应路由.
  翻译: 中文**Gemini。** `mode: "VALIDATED"`通过模式验证器,不管模型意图如何.

### 并行通话

> **【拓展：并行调用的生产实践】**调度可显著减少端到端延迟.例如,一个旅行规划代理需要同时查询航班,酒店,天气三个独立API,串行需要3轮LLM调度 (约15秒),并行只需要1轮 (约5秒) .但请注意:并行调度会增加代币消耗和执行复杂性,并且需要正确处理序列结果.

开放AI的`parallel_tool_calls: true`您运行它们全部,并以包含每条条目的工具角色消息回复.`tool_call_id`历史上,人类一直在一次性呼叫.`disable_parallel_tool_use: false`双子座2允许并行调用,但没有提供稳定的ID;双子座3添加 UUID,因此异常响应与其相关.

> 开放AI 的`parallel_tool_calls: true`发出多个调用. 你运行所有调用,然后回复一个批量工具角色消息,每个.`tool_call_id`一条目:人类历史上只做单次调用`disable_parallel_tool_use: false`(Claude 3.5 起默认) 启用多次调用.Gemini 2 允许并行调用但没有稳定的ID;Gemini 3 添加了 UUID,使乱序响应可以干净地关联.

### 流媒体

电话形式不同:

> 三者都支持流式工具调用──传输形式有不同:

- **OpenAI.**的`tool_calls[i].function.arguments`它们会逐步到达,`finish_reason: "tool_calls"`现在,我们要去.
  翻译: 中文**OpenAI。** `tool_calls[i].function.arguments`增量块逐步到达.`finish_reason: "tool_calls"`,我知道.
- **Anthropic.**阻塞启动/阻塞 delta/阻塞停止事件. `input_json_delta`部分部分的论点.
  翻译: 中文**Anthropic。**块开始 / 块增量 / 块停止事件──`input_json_delta`块携带部分参数――
- **Gemini.** `streamFunctionCallArguments`它们是的.`functionCallId`为了让多个并行通话可以相互间歇.
  翻译: 中文**Gemini。** `streamFunctionCallArguments`发出带有`functionCallId`,让多个并行调用可以交错.

第13期 · 03期深入研究并行+流动重组.本课程重点关注声明和单次调用形状.

> 第13阶段 · 03深入讲解并行和流式重组――本课重点集中在声明和单调式――

### 错误和修复

> **【拓展：JSON Repair 的工业实践】**生产环境中的模型返回无效 JSON 是常见的问题.`json-repair`通过约束解码在代币生成阶段就保证格式正确,从根本上消除了 JSON 解析失败风险.

无效论证错误也看起来不一样.

> 无效参数的错误表现也不同.

- **OpenAI (non-strict).**模型返回`arguments: "{bad json}"`如果您的JSON解析失败,您将注入一个错误信息,然后重新调用.
  翻译: 中文**OpenAI（非严格模式）。**模型返回`arguments: "{bad json}"`您的JSON解析失败,您注入错误消息并重新调用.
- **OpenAI (strict).**验证发生在解码过程中;不有效的JSON是不可能的,但 `refusal`现在,我们可以出现.
  翻译: 中文**OpenAI（严格模式）。**验证在解码期间进行;无效 JSON 不可能出现,但可能出现`refusal`,我知道.
- **Anthropic.** `input`系统可能包含意想不到的字段; 方案是建议的. 验证服务器侧.
  翻译: 中文**Anthropic。** `input`可能包含意外字段;模式是建议性的.
- **Gemini.**开放API 3.0 的特点:`enum`在被默默忽视的对象领域, 验证自己.
  翻译: 中文**Gemini。**怪癖:对象字段上的`enum`现在,我们已经开始了.

### 翻译器模式

> **【中文解读】**翻译器模式:定义一个规范的`Tool`数据类,三小函数分别翻译为三种供应商的声明形式――生产团队将其包装为`AbstractToolset`它们是什么?`UniversalToolNode`长度图`BaseTool`(LlamaIndex) ・第13阶段17课会构建一个网关,在前端暴露开放AI格式API,后端对接任意供应商.

在你的代码中,一个可信工具声明是这样的 (你选择了形状):

```python
Tool(
    name="get_weather",
    description="Use when ...",
    input_schema={"type": "object", "properties": {...}, "required": [...]},
    strict=True,
)
```

它们可以将其转化为三种提供商形状.`code/main.py`没有网络需要这个课程教导了形状,而不是HTTP.

> 三个小函数将其翻译为三种供应商格式.`code/main.py`通过每个供应商的响应格式,返回一次假的工具调用.

制作团队将这位翻译包装在`AbstractToolset`它们是的.`UniversalToolNode`其他国家`BaseTool`通过"LlamaIndex" (LlamaIndex) 实现了第13期的运输,

> 生产团队将此翻译器包装为`AbstractToolset`它们是什么?`UniversalToolNode`长度图`BaseTool`发布一个网关,在三个供应商中的任何一个之前暴露了OpenAI格式的API.

## 用它实现框架
```figure
function-call-args
```

## 用它

`code/main.py`定义一个法典`Tool`通过数据类和三个翻译器发射OpenAI,Anthropic和Gemini声明JSON.然后它将每个形状的手工供应商响应解析到同一定性呼叫对象中,证明语义在皮肤下是相同的.运行它并对三个声明隔离.

> `code/main.py`定义一个规范`Tool`数据类和三个翻译器,分别输出OpenAI、人类和双胞胎的声明 JSON──然后它将每个形式的手工制作供应商响应解析为相同的规范调用对象,证明表层下语义是相同的──运行它并并排行比较三个声明──

什么要看:

> 需要关注的点:

- 声明区的三个区块仅因封面和字段名称而不同.
  中文翻译:三个声明块只在信封和字段名上不同.
- 响应区分不同于电话的位置 (顶级级`tool_calls`现在`content[]`区块`parts[]`输入
  中文翻译:三个响应块在调用所在位置上不同层`tool_calls`,我知道.`content[]`块,`parts[]`条目) 〔
- 一个`canonical_call()`功能摘录`{id, name, args}`通过所有三种反应形式.
  中文翻译:一个`canonical_call()`函数从所有三种响应格式中提取 `{id, name, args}`,我知道.

## 运送它.

这一课产生了`outputs/skill-provider-portability-audit.md`由于一个提供商的功能调用集成,技能产生了可移植性审计:哪个提供商限制其依赖,哪些领域需要更名,以及当转移到其他提供商时会发生什么断裂.

> 本课产出发 `outputs/skill-provider-portability-audit.md`应对供应商的调用函数集成,这种技能产生可移植性审计:依赖于供应商的限制,需要重新命名的部分以及转移到其他供应商时发生什么错误.

## 练习题

1. 跑步`code/main.py`检查三个提供商声明JSON所有串行相同的基础`Tool`修改可行工具,增加一个enum参数,并确认只有双子翻译需要处理OpenAPI奇怪.
   运行代码,验证三个供应商声明 JSON 都序列化同一个`Tool`对象──添加参数,确认只有双子座 翻译器需处理 OpenAPI 怪癖──

2. 添加一个`ListToolsResponse`分析器为每一个提供商,从工具列表中提取工具,模型在一个 `list_tools`开放AI没有一个本地;请注意这种不对称性.
   为每一个供应商添加`ListToolsResponse`解析器──注意OpenAI原生不支持这一功能的非对称性──

3. 实施`tool_choice`转换:绘制一个法典`ToolChoice(mode="force", tool_name="x")`它们可以在三种形式中进行.`mode="any"`其他`mode="none"`检查课程的分数表.
   实现`tool_choice`转换:将规范的`ToolChoice`映射到三种供应商格式,覆盖力/任何/没有模式

4. 选择三个提供商之一,并阅读其函数调用指南. 在其方案规格中找到一个两个其他不支持的字段. 候选人:OpenAI `strict`人类学`disable_parallel_tool_use`双子座`function_calling_config.allowed_function_names`现在,我们要去.
   选择一个供应商阅读其函数调用指南,找出其他两个不支持的字段.

5. 写一个测试向量:一个工具调用,其参数违反了声明的方案.通过每个提供商的验证器运行它 (课01中的stdlib将作为代理) 并记录哪些错误发生. 文件是哪个提供商将使用在生产中以确定严格性.
   编写违反方案的测试向量,通过各供应商验证器运行,记录哪些错误触发.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" | Provider-level API for structured tool-call emission |
| 函数调用 | "工具使用" | 提供商级别的结构化工具调用输出 API |
| Tool declaration | "Tool spec" | Name + description + JSON Schema input payload |
| 工具声明 | "工具规格" | 名称 + 描述 + JSON Schema 输入负载 |
| `tool_choice` | "Force / forbid" | Auto / required / none / specific-name modes |
| `tool_choice` | "强制 / 禁止" | 自动 / 必需 / 无 / 指定名称模式 |
| Strict mode | "Schema enforcement" | OpenAI flag that constrains decoding to match schema |
| 严格模式 | "Schema 强制执行" | OpenAI 约束解码以匹配模式的标志 |
| `tool_use` block | "Anthropic's call shape" | Inline content block with id, name, input |
| `tool_use` 块 | "Anthropic 的调用格式" | 包含 id、name、input 的内联内容块 |
| `functionCall` part | "Gemini's call shape" | A `parts[]` entry containing name, args, and id |
| `functionCall` 部分 | "Gemini 的调用格式" | 包含 name、args 和 id 的 `parts[]` 条目 |
| Arguments-as-string | "Stringified JSON" | OpenAI returns args as a JSON string, not an object |
| 参数为字符串 | "字符串化 JSON" | OpenAI 以 JSON 字符串而非对象返回参数 |
| Parallel tool calls | "Fan-out in one turn" | Multiple tool calls in one assistant message |
| 并行工具调用 | "一回合扇出" | 一条 assistant 消息中的多个工具调用 |
| Refusal | "Model declines" | Strict-mode-only refusal block instead of a call |
| 拒绝 | "模型拒绝" | 仅严格模式下的拒绝块，替代调用 |
| OpenAPI 3.0 subset | "Gemini schema quirk" | Gemini uses a JSON-Schema-like dialect with minor differences |
| OpenAPI 3.0 子集 | "Gemini Schema 怪癖" | Gemini 使用类似 JSON Schema 的方言，存在细微差异 |

## 继续阅读 继续阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling)包括严格模式和并行调用的法典引用
  中文翻译:包含严格模式和并行调用权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) `tool_use`其他`tool_result`区块语义
  翻译: 中文`tool_use`和 `tool_result`块语义
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)并行调用,唯一的ID和OpenAPI子集
  中文翻译:并行调用、唯一ID 和 OpenAPI 子集
- [Vertex AI — Function calling reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)双子座的企业表面
  中文翻译:双子座的企业级接口
- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs)严格模式方案执行细节
  中文翻译:严格模式方案 强制执行细节
