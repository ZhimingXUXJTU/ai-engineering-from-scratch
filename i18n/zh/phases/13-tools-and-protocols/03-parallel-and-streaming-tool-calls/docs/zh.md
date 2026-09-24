# 随机工具与工具的通话和流媒体

> 通过三次独立的天气查询,将进行三次回路.并行运行它们,总时间将崩到最慢的单次通话.每个边境提供商现在在单次转换中发出多次工具通话. 收益是真实的;管道是微妙的. 这一课程走着两个半端:并行风扇和流动论点重新组装,强调了ID相关陷.

> **【中文解读】**三个独立的天气查询串行执行需要三次往返. 并行运行后,总时间缩小为最慢的单次调用时间. 所有前沿模型提供商现在都支持在单轮中发出多种调用工具. 收益是真实的,但管道建设却很微妙. 本课程涵盖两个部分:并行扇出和流式参数重组,重点讲解 id 关联陷.

> **【拓展：并行调用→Agent 效率优化】**随着人工智能代理的效率的关键优化. 当代理需要同时查询多个数据源时,调度可延迟降低60-70%.`disable_parallel_tool_use`参数和开放AI的`parallel_tool_calls`参数都控制着这一行为.

>  **【前置】**学本节前请先掌握:(1) 阶段13·02(函数调 Deep Dive) 掌握三个API形态差异,本节是它的并发延伸;(2) Python `concurrent.futures`或`asyncio.gather`基础,本节会使用线程池并行执行器;`arguments`是分片到达,必须积累后再.`json.loads`没有办法解决.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, thread pool + streaming harness) | **语言:** Python（标准库，线程池 + 流式线束）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 解释原因`parallel_tool_calls: true`任何可能存在的信息,以及何时将其禁用.
  中文翻译:解释为什么存在`parallel_tool_calls: true`什么时候禁用它?
- 在平行风扇中将流动的参数块与右工具调用ID相关.
  中文翻译:在并行扇出期间将流式参数块关联到正确的工具调用 id──
- 部分重组`arguments`无需提前解析,将字符串转化为完整的JSON.
  中文翻译:将部分 `arguments`字符串重组为完整的JSON,而不提前解析──
- 运行一个三个城市的天气基准, 显示序列与并行延迟.
  中文翻译:运行三城市天气基准测试,展示串行与并行延迟的对比.

## 问题 问题引入

没有相对通话,一个代理人回答"孟加拉,东京和苏黎世的天气是什么"这样做:

> 没有并行调用时,一个回答"孟加拉,东京和苏黎世的天气如何"的代理会这样做:

```
user -> LLM
LLM -> call get_weather(Bengaluru)
host -> run executor, reply with result
LLM -> call get_weather(Tokyo)
host -> run executor, reply with result
LLM -> call get_weather(Zurich)
host -> run executor, reply with result
LLM -> final text answer
```

执行员的延迟也在每个过程中, 约是理想的墙钟时间的4倍.

> 士的时间是4倍左右.

> **【中文解读】**没有并行调用时, 代理回答"孟加拉,东京和苏黎世的天气如何"需要三次LLM往返,每次还要支付执行器延迟,总耗时约为理想时间的4倍――

通过并行调用:

> 有并行调用时:

```
user -> LLM
LLM -> call get_weather(Bengaluru); call get_weather(Tokyo); call get_weather(Zurich)
host -> run all three executors concurrently, reply with three results
LLM -> final text answer
```

士师资格的高达10万美元,是我国第一届高中教育大学的高中教育专业.

> 一次LLM往返――执行器时间是三个最大值,而不是总和――OpenAI、Anthropic 和 Gemini 上的生产基准测试显示,扇出工作负载的挂钟时间减少了60-70%.

>  **【类比】**并行调用像超市结账――串行调用 = 你一个人排队买完肉、再排队买菜、再排队买酒,总时间=三个队时间相加――并行调用 = 你给三个朋友打电话"你们各排队,同时结账"",总时间=最慢的队时间――前提是三个购物任务彼此独立的 (朋友买什么也不依赖别人买什么),这就是为什么"工具间依赖"时必须串行――

价格是相关性复杂性. 当三个通话完成时,你的结果必须保持匹配.`tool_call_id`结果流时,您必须在执行之前将部分参数碎片组装成完整的JSON.双子座3部分添加了独特的ID,以解决一个现实世界问题,其中两个对同一工具的并行调用是无法区分的.

> 价格是关联的复杂性. 当三个调用乱序完成时,结果必须带来匹配的`tool_call_id`为了模型对齐――流式场景下,必须在执行前将部分参数片段组装成完整的JSON――Gemini 3 增加唯一的ID 部分是为了了解两个同名工具的并行调用无法区分的现实问题――

> **【中文解读】**调用过程的成本是关联的复杂性.`tool_call_id`为了使模型对齐――流式场景下,必须将部分参数片段组装成完整的JSON 后才能执行――Gemini 3 增加唯一的ID 正是为了了解两个同名工具的并行调用无法区分的问题――

## 概念的核心概念

### 允许并行

> **【拓展：何时禁用并行调用】**禁用并行调用的典型场景包括: 1) 工具有顺序依赖 (如先创建文件再写入); 2) 一个调用的输出是另一个输入 (如先查询用户ID再查订单); 3) 下游 API 有速度限制,10 路扇遇导致 429 错误.

- **OpenAI.** `parallel_tool_calls: true`默认启动`false`强迫一系列.
  翻译: 中文**OpenAI。** `parallel_tool_calls: true`默认开启.`false`强制行.
- **Anthropic.**通过`disable_parallel_tool_use: false`(在Claude 3.5及以上的默认情况下).`true`为了连载.
  翻译: 中文**Anthropic。**通过`disable_parallel_tool_use: false`并行(第3.5条及以上默认) 设为`true`强制行.
- **Gemini.**总是可行;`tool_config.function_calling_config.mode = "AUTO"`让模型决定.
  翻译: 中文**Gemini。**始终支持并行;`tool_config.function_calling_config.mode = "AUTO"`让模型自己决定.

工具有顺序依赖性时,禁用并行 (`create_file`然后`write_file`),当一个调用输出通知另一个输入时,或者速度限制器无法处理风扇.

> 当工具有顺序依赖`create_file``write_file`) 、一个调用输出影响另一个输入或速度限制器无法处理扇出时,禁用并行.

> **【中文解读】**当工具有顺序依赖`create_file``write_file`) 、当一个调用输出影响另一个输入或速度限制器无法处理扇出时,应关闭并行.

>  **【困惑】**模型怎么知道哪些调节可以并行?A: 模型不知道,它只决定"现在要调整这些工具";并发执行是主机的事务――模型发出`[get_weather(Tokyo), get_weather(Zurich)]`时,主管自己判断这两个无赖可以发发;如果模型发发发`[create_file, write_file]`宿主必须串行 (通常做法是禁用并行+顺序执行,或者在执行器内做依赖检查) "是否并行"是宿主配置+模型决定共同决定的.

### 相关性

每次电话,模型发射的电话都有一个`id`没有这个,结果是模糊的.

> 模型发出的每个调用都有一个调用`id`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

- **OpenAI.** `tool_call_id`在每个工具角色信息上.
  翻译: 中文**OpenAI。**每个工具都在角色消息上`tool_call_id`,我知道.
- **Anthropic.** `tool_use_id`在每一个`tool_result`区块.
  翻译: 中文**Anthropic。**每个`tool_result`块上的`tool_use_id`,我知道.
- **Gemini.** `id`在每一个`functionResponse`(双子座3及以上;双子座2与名字相匹配,而与同名并行通话打破).
  翻译: 中文**Gemini。**每个`functionResponse`上的`id`(双子三及以上;双子二按名称匹配,同名并行调用时会出错) 〔

### 同时进行电话

接待者在自己的线程,Coroutine或远程工作者上运行每个呼叫的执行器.最简单的带使用线程池;生产使用asyncio与 `asyncio.gather`完成顺序是不可预测的  id是标识符.

> 宿主在每个调用执行器上运行自己的线程、协程或远程工作器──最简单的线束使用线程池;生产环境使用异常的`asyncio.gather`或结构化并发──完成顺序不可预测id 是标识符──

> ️ **【易错点】**场景:流式模式下对每个`arguments`片立即`json.loads`/ 后果:JSON 不完整触发 `JSONDecodeError`因为流式可能会在你身上.`{"city":"To`时就触发回调 / 修复:每个 `tool_call_id`维护一个`accumulator`字符串,所有分片`+=`后等`finish_reason="tool_calls"`才整体解析;并行时用 `{id: accumulator}`字典隔离――

答案的结果是调用列表顺序而不是完成顺序.`tool_call_id`结果被丢弃或重复,则不顺序提交使调试变得更加困难.

> 一个常见的错误:按调用列表顺序而不是完成顺序回复结果――这通常可以工作,因为模型只关心`tool_call_id`但是如果结果被丢弃或重复,乱序提交会使调试更困难.

### 流媒体工具的呼叫

> **【拓展：流式工具调用的用户体验】**流式工具调用让用户看到代理正在"思考"和执行过程,而不是等待一个黑盒操作完成. 这对于长时间的工具来说,特别有价值.

当模型流动时,`arguments`接下来,三个相对通话的分别流量在线上交互.

> 当模型流式传输时,`arguments`分片到达──三并行调用三个独立流块在传输中交错──你需要每个ID一个累加器──

提供商的形状:

> 各供应商的格式:

- **OpenAI.**每个部分都是`choices[0].delta.tool_calls[i].function.arguments`部分弦. 部分带着`index`您按指数积累,读取`id`当它第一次出现时,并解析JSON当`finish_reason = "tool_calls"`现在,我们要去.
  翻译: 中文**OpenAI。**每个块都是`choices[0].delta.tool_calls[i].function.arguments`部分字符串:块携带`index`根据索引累积,首次出现时读取`id`在`finish_reason = "tool_calls"`时解析JSON──
- **Anthropic.**流媒体事件是`message_start`然后一个`content_block_start`每块,有类型`tool_use`(包含身份证,名称,空格输入). `content_block_delta`事件的运行`input_json_delta`子.`content_block_stop`关闭每一个街区.
  翻译: 中文**Anthropic。**流事件先是`message_start`然后每个类型为`tool_use`块有一个`content_block_start`(包含 id、name、空输入)`content_block_delta`事件携带`input_json_delta`块──`content_block_stop`关闭每个块.
- **Gemini.** `streamFunctionCallArguments`双子三级以上) 发射了`functionCallId`在双子座3之前,流媒体回应一次一次一次.
  翻译: 中文**Gemini。** `streamFunctionCallArguments`发发带有 发发带有`functionCallId`,使调用可以干净地交错.

### 部分JSON和分析早期陷

你不能分析.`arguments`部分JSON,如`{"city": "Beng`合适的门是提供商的终端通话信号:OpenAI的`finish_reason = "tool_calls"`美国人文学报`content_block_stop`只有那时才尝试.`json.loads`更加强大的方法采用一个增量JSON解析器,随着结构完成时生成事件;OpenAI的流媒体指南建议为 UX使用这种方法,该指标显示了现场"思考"指标. 数计数是不可靠的,作为完整性测试 (引用字符串内或逃逸内容导致虚假阳性),并且只应作为非正式的调试数.

> 在`arguments`完成之前不能尝试解析.`{"city": "Beng`通过JSON的部分,将抛出异常.`finish_reason = "tool_calls"`类的`content_block_stop`们的流程结束事件.`json.loads`△更健壮的方法使用增量JSON解析器,在结构完成时产生事件;OpenAI的流式指南推用于显示实时"思考"指示器的UX──大括号计数作为完整性测试不可靠,引号字符串或转义内容中的括号会导致误判),只应作为非正式调试启动式方法──

> **【中文解读】**不能在`arguments`完成之前尝试解析――`{"city": "Beng`通过JSON的部分,将抛出异常.`finish_reason`类的`content_block_stop`△双子的流端) △大括号计数作为完整性测试不可靠,因为引号字符串中的括号或转义内容会导致误判──

### 订单外完成

```
call_A: fast API, returns first
call_B: slow API, returns second
call_C: median API, returns third
```

接待者答复必须引用以下身份证:

> 宿主回复仍需引用 id:

```
[{role: "tool", tool_call_id: "call_A", content: ...},
 {role: "tool", tool_call_id: "call_B", content: ...},
 {role: "tool", tool_call_id: "call_C", content: ...}]
```

答案中的顺序对OpenAI或Anthropic的准确性并不重要.只要ID匹配,双胞胎会接受任何订单.

> 回复中的顺序对OpenAI或人类的正确性无关紧要――双子女接受任何顺序,只要 id 匹配――

### 基准:连续对平行

带里面`code/main.py`模拟三个执行器,400,600和800ms延迟. 序列运行在1800ms总. 并行运行在最大400,600,800) =800ms. 差异是恒定,不成比例,因此节省随着工具数量增长.

> `code/main.py`中线束模拟三个延迟分别为400、600和800毫秒的执行器.

现实世界警告:并行通话压力下游API.一个10个方式的风扇到一个限速服务将失败.13 · 17阶段涵盖门口级压力;重试语义计划在未来阶段.

> 现实注意事项:并行调用会给下游API施加压力──10 路扇出到速率限制的服务会失败──13 阶段 · 17 涵盖网关级背压;重试语义计划在未来阶段 中──

### 流动风扇外墙钟

如果模型本身流,你可以在一个调用的参数完成后开始执行,而不是等待所有调用完成.这是一个优化 OpenAI 文档,但不是所有的 SDK 暴露.本课程中的杆是这样做的:一旦模拟流产生完整的参数对象,主机启动了调用.

> 如果模型本身是流式的,你可以在调用参数完成后立即开始执行,而不必等待所有调用完成.这是OpenAI记录的一种优化,但并不是所有的SDK都暴露了这种能力.本课程的线束已经实现了这一点:一旦模拟流产生完整的参数对象,主机就开始调用.

## 用它实现框架
```figure
tp-parallel-fanout
```

## 用它

`code/main.py`首先,它运行了三个模拟的天气调用,`concurrent.futures.ThreadPoolExecutor`另一半重复了一个假的流媒体响应`arguments`在一个流中交互的三个并行调用,并将它们重新组装成每个ID`StreamAccumulator`没有法学士,没有网络,只是重新组装逻辑.

> `code/main.py`有两个部分.`concurrent.futures.ThreadPoolExecutor`顺序和并行运行三模拟天气调调,并印挂钟时间――第二部分回放一个假的流式响应三并行调调`arguments`块在一个流上交错并使用`StreamAccumulator`按 id 重组──不需要LLM,不需要网络,只是重组逻辑──

什么要看:

> 需要关注的点:

- 顺序计时器达到1.8秒,并行计时器达到0.8秒,
  中文翻译:串行计时器达到1.8秒.并行计时器在相同假延迟下达到0.8秒.
- 积累器只处理到达不顺序的块,通过按标识缓冲和解析,
  中文翻译:累加器通过按 id 缓冲乱序到达的块来处理,只在每个调用的JSON 完成时才解析。
- 执行器在所有流程结束后,不但在ID的论点完成后就开始.
  中文翻译:执行器在一个 id 的参数完成后立即启动,而不是所有流结束后.

## 运送它.

这一课产生了`outputs/skill-parallel-call-safety-check.md`鉴于工具登记,技能审计是哪些工具可以安全地并行化,有订单依赖性,并且会压倒下游利率限制 每工具的修订登记 `parallel_safe`旗.

> 本课产出发 `outputs/skill-parallel-call-safety-check.md`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │`parallel_safe`标志的修订注册表

## 练习题

1. 跑步`code/main.py`确认平行到序列比率是大约`max/sum`(实际运行因线程安排,串行和带上层费而略有偏离于理想).
   中文翻译:运行 `code/main.py`并改变模拟延迟.确认并行与串行比率约为`max/sum`(实际运行因线程调度,序列化和线束开销与理想值有略偏差) 什么延迟分布下并行不再有意义?

2. 扩展蓄积器以处理"中流取消电话"的情况下,`cancelled`哪个提供商明确记录了这个案例?`content_block_stop`语义和OpenAI的研究`finish_reason: "length"`如何表现?
   中文翻译:扩展累加器以处理"调用在流中被取消"的情况,丢弃其缓冲区并发出`cancelled`事件──哪个供应商确实记录了这种情况?`content_block_stop`语义和开放AI 的`finish_reason: "length"`行为

3. 替换线池为`asyncio.gather`由于下文交换成本,你应该看到小的胜利,但只有执行器做真正的I/O.
   中文翻译:用`asyncio.gather`换线程池――对两者进行基准测试――你应该看到不同步骤有小优势,因为下文换代成本较低,但前提是执行器做真正的I/O――

4. 选择两个不应该平行的工具 (例如:`create_file`然后`write_file`添加一个`ordering_dependency`对于依赖意识的规划,这是一个未来的代理工程阶段正式化的最低机械.
   中文翻译:选择两个不应该并行化的工具`create_file`然后`write_file` 加入注册表中`ordering_dependency`图,并基于图门控制并行扇出.这是依赖感觉调度的最小机制,未来的代理工程阶段将会形式化.

5. 阅读OpenAI的并行函数调用部分和Anthropic的部分.`disable_parallel_tool_use`鉴定人类推禁用并行性 (提示:同一资源的后果突变).
   中文翻译:阅读OpenAI的并行函数调用章节和人类的 `disable_parallel_tool_use`文档──找出 建议禁用并行的一种真实工具类型──提示:对同一资源的后果性修改──)

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Parallel tool calls | "Fan-out in one turn" | Model emits multiple tool calls in a single assistant message | 并行工具调用 |
| `parallel_tool_calls` | "OpenAI's flag" | Enable or disable multi-call emission | OpenAI 并行调用开关 |
| `disable_parallel_tool_use` | "Anthropic's inverse" | Opt-out flag; default is parallel enabled | Anthropic 并行禁用开关 |
| Tool call id | "Correlation handle" | Per-call identifier the result message must echo | 工具调用标识符 |
| Accumulator | "Stream buffer" | Per-id string buffer for partial `arguments` chunks | 流式累加器 |
| Out-of-order completion | "Fastest first" | Parallel calls finish in unpredictable order; ids are the glue | 乱序完成 |
| Dependency graph | "Ordering constraints" | Tools whose outputs feed into inputs of other tools; cannot parallelize | 依赖图 |
| Parse-early trap | "JSON.parse exploded" | Attempting to parse an incomplete `arguments` string | 过早解析陷阱 |
| `streamFunctionCallArguments` | "Gemini 3 feature" | Streamed argument chunks with unique id per call | Gemini 3 流式参数 |
| Completion-order reply | "Don't wait for all" | Reply with results as they arrive, keyed by id | 按完成顺序回复 |

## 继续阅读 继续阅读

- [OpenAI — Parallel function calling](https://platform.openai.com/docs/guides/function-calling#parallel-function-calling)默认行为和选择退出标志
  中文翻译:默认行为和退出标志
- [Anthropic — Tool use: implementing tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implementing-tool-use) `disable_parallel_tool_use`结果批量
  翻译: 中文`disable_parallel_tool_use`和结果批处理
- [Google — Gemini function calling parallel section](https://ai.google.dev/gemini-api/docs/function-calling)来自双子座3的ID相关的并行电话
  中文翻译:Gemini 3 的 id 关联并行调用
- [OpenAI — Streaming responses with tools](https://platform.openai.com/docs/api-reference/responses-streaming) 对于OpenAI流的分断参数重组
  中文翻译:OpenAI流的分块参数重组
- [Anthropic — Streaming messages](https://docs.anthropic.com/en/api/messages-streaming) `content_block_delta`随着`input_json_delta`
  中文翻译:带 `input_json_delta`的`content_block_delta`
