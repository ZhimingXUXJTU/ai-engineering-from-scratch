# 结构化输出:JSON Schema、Pydantic、Zod 与约束解码

> 结构化输出通过限制解码缩小缩小了这一差距:模型字面上被阻止发出违反方案的代币.OpenAI的严格模式,Anthropic的方案类型工具使用,双胞胎的 `responseSchema`星的AI`output_type`,和佐德的`.parse`这一课构建了方案验证器,严格模式的合同学习者将用于每个生产提取管道.

> **【中文解读】**结构化输出通过束解码弥补这一差距:模型在代币级别被阻止发出违反方案的内容.`responseSchema`登特 AI`output_type`和 `.parse`是同一思想的五种表面形式.

> **【拓展：结构化输出→Function Calling 的质量保障】**结构化输出是所有数据提取管道的基础. 在函数调用场景中,结构化输出确保工具参数的JSON格式始终有效.`input_schema`在工具_使用中实现类似保证. 这消除了"模型返回无效JSON"的最常见生产故障模式.

>  **【前置】**学本节前请先掌握:(1) 阶段11·03(结构化输出) 基础;(2) 阶段13·01(工具界面) 和13·02(函数调 Deep Dive) 理解严格模式 出现前的"JSON提示"失败模式;(3) 皮坦特 v2 或 Zod 基础语法,本节会使用它们生成方案。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, JSON Schema 2020-12 subset) | **语言:** Python（标准库，JSON Schema 2020-12 子集）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 写一个JSON Schema 2020-12用于抽取目标,使用正确的限制 (enum,min/max,要求,模式).
  中文翻译:使用正确的约束(enum、min/max、required、pattern) 为提取目标编写JSON Schema 2020-12。
- 解释为什么严格模式和限制式解码提供了不同的保证与"后代有效性".
  中文翻译:解释为什么严格模式和约束解码提供与"生成后验证"不同的保证.
- 区分三个故障模式:解析错误,方案违规,模型拒绝.
  中文翻译:区分三种失败模式:解析错误、Schema 违规、模型拒绝──
- 运输一个采集管道,采用打字维修和打字拒绝处理.
  中文翻译:交付一个带有类型化修复和类型化拒绝处理的提取管道.

## 问题 问题引入

读取购买订单的电子邮件的代理人需要将免费文本转化为`{customer, line_items, total_usd}`接下来有三种方法.

> 一读取采购订单邮件的代理 需要将自由文本转换为 `{customer, line_items, total_usd}`三种方法.

**Approach one: prompt for JSON.**"用客户端,线_项目,总_usd的字段在JSON中回答". 在边界模型上,它在85-95%的时间内工作.在六种方式上失败:缺少支柱,后行逗号,错误类型,幻觉字段,在代币限制中缩小,泄露的散文如"这里是你的JSON:".

> **方法一：提示要求 JSON。**"以 JSON 格式回复,包含字段客户端、线_项目、总_usd──"在前沿模型上有效的时间为85-95%──六种失败方式:缺少大括号、尾随逗号、类型错误、幻觉字段、代码 限制处截断、泄露散文如"这是你的 JSON:"──

**Approach two: validate after generation.**根据该规则,每次试验都需要一个额外的转折,而每次试验都需要一个额外的转折.

> **方法二：生成后验证。**自由生成,解析,按计划验证,失败时重试.可靠但昂贵.每一次重试都必须付费,截断错误.每次发生,还需要一轮.

**Approach three: constrained decoding.**提供商在解码时执行该方案.不有效的代币被隐藏在样本分布中.输出保证分析并保证验证.失败崩到一个模式:拒绝 (模型决定输入不符合该方案).

> **方法三：约束解码。**提供商在解码时强制执行方案――无效代币从采样分布中被屏蔽――输出保证可解析且可验证――失败归结为一种模式:拒绝(模型判定输入不适合方案) ⋅

>  **【类比】**约束解码像填空题的"格子"约束――普通生成是写作文,想写写,可能跑题无效 JSON) ――约束解码是给你一个表格,每个格子已经标记为"姓名/年龄/邮箱",模型只能在格子里填满应对类型的内容,不会出现"年龄"那填满了"小明"――技术实现:在每个代币采用时,预先屏蔽所有导致计划违规代币,让概率为零――

> **【中文解读】**第三种方法约束解码在解码时强制执行方案──无效代币被从采样分布中屏蔽──输出保证可解析且可验证──失败只归结为一种模式:拒绝(模型认为输入不符合方案)──

每一个2026年边境提供商都会提供某种方式.

> 2026年,每一个前沿供应商都发布了某种形式的方法.

- **OpenAI.** `response_format: {type: "json_schema", strict: true}`另外`refusal`如果模型下降,
  翻译: 中文**OpenAI。** `response_format: {type: "json_schema", strict: true}`如果模型拒绝,则在反应中加上.`refusal`,我知道.
- **Anthropic.**实施方案`tool_use`输入`stop_reason: "refusal"`没有什么问题,但`end_turn`没有工具的呼叫是信号.
  翻译: 中文**Anthropic。**在`tool_use`输入上强制执行方案;`stop_reason: "refusal"`没有,但没有调用工具`end_turn`是信号.
- **Gemini.** `responseSchema`在要求水平上;在2026年,双子公司将为选定的类型发出代币级语法限制.
  翻译: 中文**Gemini。**要求级别`responseSchema`2026年双胞胎为选定类型提供了代号语法约束.
- **Pydantic AI.** `output_type=InvoiceModel`发出结构化`RunResult`标签:`InvoiceModel`现在,我们要去.
  翻译: 中文**Pydantic AI。** `output_type=InvoiceModel`发发出类型化为`InvoiceModel`结构化`RunResult`,我知道.
- **Zod (TypeScript).**运行时间解析器,与Zod方案进行供应商输出验证;与OpenAI的配对`beta.chat.completions.parse`现在,我们要去.
  翻译: 中文**Zod (TypeScript)。**根据Zod Schema 验证提供商输出运行时解析器;与OpenAI的`beta.chat.completions.parse`配合使用.

共同的线程:一次宣布方案,

> 共同主线:声明方案 一次,端到端强制执行.

## 概念的核心概念

### 语法语 2020-12

> **【中文解读】** JSON Schema 2020-12 是所有供应商共同接受的 Schema 语言.`type`类型`properties`没有任何其他方法.`required`没有任何其他方法.`enum`子,子,子,子,子,子`minimum`现在,我们要去.`maximum`它们的数值范围`pattern`开放AI严格模式 额外要求所有属性必须在`required`中列出,所有层次`additionalProperties: false`必须使用未解析的`$ref`,我知道.

每个提供商都接受JSON Schema 2020-12.

> 每个供应商都接受了2020-12 JSON方案.

- `type`其中一个`object`现在`array`现在`string`现在`number`现在`integer`现在`boolean`现在`null`现在,我们要去.
  翻译: 中文`type`其他:`object`,我知道.`array`,我知道.`string`,我知道.`number`,我知道.`integer`,我知道.`boolean`,我知道.`null`之一.
- `properties`: 字段名称地图到子方案.
  翻译: 中文`properties`字段名到子方案的映射──
- `required`:必须出现的字段名称列表.
  翻译: 中文`required`必须出现的字段名列表
- `enum`: 允许的值的闭合集合.
  翻译: 中文`enum`允许值的封闭集合――
- `minimum`现在,`maximum`其他国家`minLength`现在,`maxLength`现在,`pattern`现在,我们要去看看.
  翻译: 中文`minimum`现在,`maximum`没有任何其他方法`minLength`现在,`maxLength`现在,`pattern`现在,我在做什么?
- `items`:对每个数组元素的子方案.
  翻译: 中文`items`应用于每个数组元素的子方案.
- `additionalProperties`其他`false`禁止额外的字段 (默认取决于模式).
  翻译: 中文`additionalProperties`其他:`false`禁止额外字段 (默认值因模式而异)

开放AI严格模式增加了三个要求:每个财产必须在`required`现在`additionalProperties: false`没有一个未解决的问题.`$ref`如果你打破这些,API会在请求时返回400个.

> 开放AI严格模式增加了三个要求:每个属性都必须列在`required`任何一个层次`additionalProperties: false`必须使用未解析的`$ref`如果违反这些要求,API会在请求时返回400.

> ️ **【易错点】**场景:开启AI严格模式 下用Pydantic 的 `Optional[int] = None`后果:API 返回 400 报"额外属性或要求"错误,因为严格模式 要求**所有**字段在`required`虽然可选 / 修复:用 `Union[int, None]`显然没有`required=[..., "field_name"]`,或者Pydantic AI 框架会自动处理这个转换;最佳实践是定义所有字段都必填,缺省值用空字符串/零而不是"省略"――

### 丹,Python绑定

> **【拓展：Pydantic AI 在结构化输出中的地位】**皮达尼克人工智能是2024-2025年兴起的Python代理框架,其核心竞争力是利用Pydantic v2`model_json_schema()`开发者只需要定义一个`BaseModel`类,框架自动处理 严格模式 兼容性 类验证和拒绝处理. 据统计,Pydantic AI 在 2025 年 GitHub 增长最快的AI 框架排名三.

通过  数据类型模型生成JSON Schema`model_json_schema()`皮达尼斯人工智能将这封面包成一个字幕:

> 通过Pydantic v2`model_json_schema()`通过数据类型模型生成JSON Schema──Pydantic AI 封装了这一点,你只需要写:

```python
class Invoice(BaseModel):
    customer: str
    line_items: list[LineItem]
    total_usd: Decimal
```

通过"机器人框架"将该方案转化为"OpenAI严格模式",`input_schema`两个双胞胎`responseSchema`模型的输出是打字的.`Invoice`验证错误增加`ValidationError`输入错误路径.

> 然后代理 框架在边缘将 Schema 翻译为 OpenAI 严格模式、人类`input_schema`或是双子座`responseSchema`△模型的输出以类型化`Invoice`实例回应――验证错误会引发带有类型化错误路径的`ValidationError`,我知道.

### 编程:

 (`z.object({customer: z.string(), ...})`开放AI的 Node SDK 揭示了`zodResponseFormat(Invoice)`转换为API的JSON方案有效载荷.

>  (`z.object({customer: z.string(), ...})`) 是TypeScript的等价方案.`zodResponseFormat(Invoice)`将其翻译为 API 的 JSON 方案 负载.

### 拒绝

严格模式不能迫使模型回答. 如果输入无法符合方案 ("电子邮件是一个诗,而不是一个账单"),模型会发出一个`refusal`您的代码必须把此处理为一流的结果,而不是失败.拒绝也作为安全信号有用:一个要求从受保护内容的电子邮件中提取信用卡号码的模型将附上安全理由返回拒绝.

>  **【困惑】**答:拒绝算"成功"还是"失败"?返回什么 HTTP 状态码?**业务成功**由于模型按计划约定给出正确的"无法处理"信号,`Result<T, Refusal>`处理:要么走"拒绝分支" (如记录到日志、回归到人工审核),要么再次提示用户──把拒绝当500 错误是新手最常见的误判,会导致监控告警噪声──


> 严格模式 不能强制模型回答. 如果输入无法适应 Schema (("邮件是诗歌而不是发票"),模型会发出包含原因.`refusal`字段──你的代码必须作为一级公民结果处理,而不是失败──拒绝也可用作安全信号:当模型被要求从受保护内容邮件中提取信用卡号时,将返回附带安全原因的拒绝──

> **【中文解读】**严格模式 不能强制模型回答. 如果输入无法适应方案,如"邮件是诗歌而不是发票"),模型会发出.`refusal`字段──拒绝不是失败,而是同等公民类型的回报结果──拒绝也可用作安全信号:当模型被要求从受保护内容中提取信用卡号时,将回归附有安全原因的拒绝──

### 开放式限制解码

> **【拓展：开源约束解码工具对比】**主要开源工具包括:`outlines`基于有限状态自动机构建代币掩码;`guidance`微软出品: 模板语言控制生成`lm-format-enforcer`通过流式JSON解析器计算有效下一代币集合――2026年最新进展是这些工具的速度已经接近无约生成,短结构化输出场景甚至更快 (因为减少采样空间)

开放权重的实施使用三个技术.

> 开源权重实现使用三种技术.

1. **Grammar-based decoding**(`outlines`现在`guidance`现在`lm-format-enforcer`):从该方案中构建一个定制性有限的自动机;在每一步上,掩盖违反FSM的代币的logits.
   翻译: 中文**基于语法的解码**(`outlines`,我知道.`guidance`,我知道.`lm-format-enforcer`):从计划 构建确定性有限自动机;每一步屏蔽会违反FSM的代币的逻辑.
2. **Logit masking with a JSON parser**运行一个流媒体JSON解析器,按模型锁步;在每一步计算有效-下一个代码.
   翻译: 中文**带 JSON 解析器的 Logit 屏蔽**模型与运行流式 JSON 解析器;每一步计算有效的下一代标记集合──
3. **Speculative decoding with a verifier**廉价的草案模型提出代币,验证器执行方案.
   翻译: 中文**带验证器的推测解码**价格低的草稿模型提出标志,验证器强制执行方案.

商业供应商在幕后选择其中一个. 2026 年的最新技术速度比普通的短结构产品更快,长产品的速度也大致相同.

> 商业供应商在幕后选择其中一个.2026年最先进的技术对于短结构化输出比普通的生产更快,对于长输出大致相同.

### 失败的三个模式

1. **Parse error.**输出是不有效的JSON.不能发生在严格模式下.仍然可以发生在非严格的提供商.
   翻译: 中文**解析错误。**输出不是有效的 JSON――严格模式下不可能发生――非严格 提供商仍然可能发生――
2. **Schema violation.**输出解析,但违反了方案.不能在严格模式下发生.
   翻译: 中文**Schema 违规。**输出可解析但违反了规划. 严格模式下不可能发生.
3. **Refusal.**模型下降,必须被处理为一个输入结果.
   翻译: 中文**拒绝。**模型拒绝.必须作为类型化结果处理.

### 复试策略

> **【中文解读】**不严格模式 下的恢复模式是"生成→解析→验证→失败则注入错误重试,最多3次"――通常一次重试就够了,三次覆盖弱模型的偶然失败――超过三次说明方案 设计有问题,需要修改即时或方案――

当你在严格模式之外 (人类工具使用,非严格的OpenAI,旧的双胞胎),恢复模式是:

> 当你不在严格模式下时(人类工具使用、非严格的OpenAI、旧版双子),恢复模式是:

```
generate -> parse -> validate -> if fail, inject error and retry, max 3x
```

一次重试通常足够.三次重试会发现模型的弱点.三次重试是不良方案的迹象:模型无法满足某些输入,提示或方案需要修复.

> 一次重试通常就够了――三次重试覆盖弱模型的偶然失败――超过三次说明方案设计有问题:模型对某些输入无法满足,需要修改即时或方案――

### 支持小型模型

限制式解码在小型模型上运行.一个具有语法强制性的3B参数开放模型比70B参数模型更有效,并且在结构化任务上具有原始提示性.这是结构化输出的主要原因:它将可靠性与模型大小分离.

> 约束解码也适用于小模型――一个配合语法强制的3B参数开源模型,在结构化任务上可超过70B参数模型的纯提示方法――这是结构化输出在生产中重要的主因:它解了可靠性和模型大小――

> **【中文解读】**约束解码也适用于小模型――一个3B参数的开源模型配合语法强制性,在结构化任务上可超过70B参数模型的纯提示方法――这是结构化输出在生产中重要的主因:它解了可靠性和模型大小――

## 用它实现框架
```figure
constrained-decoding
```

## 用它

`code/main.py`通过使用JSON Schema 2020-12验证器,它将一个最小的JSON Schema 2020-12验证器运送到 stdlib (类型,要求, enum, min/max,模式,项目,额外属性).`Invoice`通过验证器运行一个假的LLM输出,显示解析错误,方案违规和拒绝路径.

> `code/main.py`提供一个标准库实现的最小JSON方案 2020-12验证器 (类型,必填,枚举,最小/最大值,模式,项目,附加属性)`Invoice`计划并将通过验证器运行,演示解析错误,方案违规和拒绝路径进行假输出,以替代任何供应商的真实反应.

什么要看:

> 需要关注的点:

- 验证器返回输入的 `[ValidationError]`列表包含路径和消息. 这就是你想要在重试提示时出现的形状.
  中文翻译:验证器回归一个带有路径和消息的类型化`[ValidationError]`这就是你想要显示的重试提示中的格式.
- 拒绝分支不会再尝试.它记录并返回输入的拒绝.14 · 09阶段使用拒绝作为安全信号.
  中文翻译:拒绝分支不会重试――它记录日志并返回类型化拒绝――阶段14 · 09 使用拒绝作为安全信号――
- 其他`additionalProperties: false`检查对抗性测试输入的火灾,说明严格模式为什么会关闭幻觉场所的门.
  翻译: 中文`additionalProperties: false`检查对抗性测试输入的触发,展示了为什么严格模式关闭幻觉字段的大门.

## 运送它.

这一课产生了`outputs/skill-structured-output-designer.md`鉴于自由文本提取目标 (发票,支持门票,简历等),该技能产生了一个严格模式兼容的JSON Schema 2020-12和一个反射的Pydantic模型,输入拒绝和重新尝试处理.

> 本课产出发 `outputs/skill-structured-output-designer.md`△给定一个自由文本提取目标 (发票、支持工单、简历等),该技能产生一个严格的模式 兼容的JSON Schema 2020-12 和一个镜像的Pydantic 模型,并预设的类型化拒绝和重试处理──

## 练习题

1. 跑步`code/main.py`添加一个第四个试验案例`total_usd`确认验证器拒绝了它`minimum`限制路径.
   中文翻译:运行 `code/main.py`加上第四个试用例,`total_usd`负数: 确认验证器`minimum`约束路径拒绝它.

2. 扩展验证器到支持`oneOf`常见情况:`line_item`是一个产品或服务,标记为 `kind`严格模式有细节的规则;请查看OpenAI的结构化输出指南.
   中文翻译:扩展验证器以支持带判判器的`oneOf`常见使用例:`line_item`是产品或服务,由`kind`标记――严格模式 在此有微妙的规则;查看OpenAI的结构化输出指南――

3. 写出与Pydantic BaseModel相同的发票方案,并比较`model_json_schema()`默认的识别一个字段Pydantic设置,手动滚动版本遗漏.
   中文翻译:将相同的发票方案 写成Pydantic基模型,比较 `model_json_schema()`输出与手写方案──找出Pydantic 默认设置但手写版本遗漏的字段──

4. 测量拒绝率. 构建不应该提取的十个输入 (歌词,数学证明,空白电子邮件) 并通过严格模式的真实提供商运行它们. 计算拒绝与幻觉输出. 这是拒绝意识的重试的基本真理.
   中文翻译:测量拒绝率──构造十个不应可提取的输入 (歌词,数学证明,空白邮件),通过严格模式的真实提供商运行──统计拒绝与幻觉输出量──这是拒绝感知重试的基准事实──

5. 阅读OpenAI的结构化输出指南. 识别它明确禁止的构建,在简单的JSON方案允许的严格模式下.然后设计一个不必要的设计方案,并重新构建它以严格兼容.
   中文翻译:从头到尾阅读OpenAI的结构化输出指南――找出它在严格模式中明确禁止但普通JSON方案允许构建――然后设计一个不必要使用该禁止构建的方案,并重构为严格兼容――

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| JSON Schema 2020-12 | "The schema spec" | IETF-draft schema dialect every modern provider speaks | JSON Schema 2020-12 规范 |
| Strict mode | "Guaranteed schema" | OpenAI flag that enforces schema via constrained decoding | 严格模式 |
| Constrained decoding | "Logit masking" | Decode-time enforcement that masks invalid next-tokens | 约束解码 |
| Refusal | "Model declines" | Typed outcome when input cannot fit the schema | 模型拒绝 |
| Parse error | "Invalid JSON" | Output did not parse as JSON; impossible under strict | 解析错误 |
| Schema violation | "Wrong shape" | Parsed but violated types / required / enum / range | Schema 违规 |
| `additionalProperties: false` | "No extras allowed" | Forbids unknown fields; required in OpenAI strict | 禁止额外属性 |
| Pydantic BaseModel | "Typed output" | Python class that emits and validates JSON Schema | Pydantic 基础模型 |
| Zod schema | "TypeScript output type" | TS runtime schema for provider output validation | Zod 类型定义 |
| Grammar enforcement | "Open-weights constrained decode" | FSM-based logit masking, as in outlines / guidance | 语法强制 |

## 继续阅读 继续阅读

- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs)严格的模式,拒绝和方案要求
  中文翻译:严格模式、拒绝和方案 要求
- [OpenAI — Introducing structured outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) 2024 年 8 月启动后,解释了解码保证
  中文翻译:2024年8月发布博文,解释解码保证
- [Pydantic AI — Output](https://ai.pydantic.dev/output/)输出_类型的键字,将其连续到每个提供商
  中文翻译:序列化到各供应商的类型化输出_类型 绑定
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes)法典规范
  中文翻译:规范权威文档
- [Microsoft — Structured outputs in Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)企业部署说明和严格模式警告
  中文翻译:企业部署说明和严格模式 注意事项
