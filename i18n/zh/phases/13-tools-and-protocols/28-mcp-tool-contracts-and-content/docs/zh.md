# 关于MCP工具合同和内容

> 发现,论证,结果,页面化和运输元数据在一个合同时才安全自动化工具.

> **【中文解读】**一个工具只有当发现,参数,结果,分页和传输元数据在同一协议上,才适合交付AI自动调用.本课程基于MCP 2026-07-28规范,把一次工具调用拆成五道禁 (发现,准入,调用,执行,消费),逐门讲清校验责任归归谁:宿主有两门进入和消费,服务器无法强迫客户端信任自己的注解,方案或输出.

> **【拓展：MCP→真实生产链路】**这五门对应真实的AI网关的分层:描述者校验是网关的"工具准入",`x-mcp-header`镜像是按区域路由的负载平衡,分页游标是目录同步的基础,完成是单单自动补充的授权面面──第13期·17期网关与注册中心) 和第13期·23期毕业项目) 都会重复本课的准入核心──

>  **【前置】**学本课前请先掌握:第13阶段 · 07(MCP 服务器) 第13阶段 · 09(MCP 传输:可流式HTTP 细节) 第13阶段 · 10(资源与提示,完成的引用对象来自这里) ⋅

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07, 09, and 10 | **前置知识:** Phase 13 · 07、09、10
**Time:** ~120 minutes | **时间:** 约 120 分钟

## 学习目标

- 定义工具输入和输出,使用JSON Schema 2020-12.
  中文翻译:用JSON Schema 2020-12 定义工具的输入和输出──
- 验证结构化结果,而不假设它们是JSON对象.
  中文翻译:校验结构化结果,而不预设它们一定是JSON对象.
- 选择文本,图像,音频,资源链接和嵌入式资源.
  中文翻译:在文本,图像,音频,资源链接和内嵌资源之间做出选择.
- 拒绝不安全`x-mcp-header`在工具达到模型之前,定义.
  中文翻译:在不安全的`x-mcp-header`定义到达模型之前把它拒绝掉.
- 编码参数标题值并验证标题对体的准确平衡.
  中文翻译:对参数头部值编码,并验证头部与请求体的精确一致性.
- 通过线程页面化,而不解释线程值.
  中文翻译:遍历游标分页而不去解释游标的取值──
- 绑定和授权`completion/complete`提供建议.
  中文翻译:为 `completion/complete`补全建议设界并做授权.

## 问题 问题引入

> **【中文解读】**本课程的开始点:调用本地Python 函数是简单的,而通过AI 宿主调用远端能力是一个契约问题.链接上有六个角色.服务器发布描述器,客户端将其转化为模型上下文和UI,模型生成参数,网关可能根据镜头头路由请求,服务器执行工具,客户端重新决定结果是否有效,可以返回模型.

通过人工智能主机调用远程功能是一个合同问题.

> 调用一个Python 函数很容易.通过AI 宿主调用一个远端能力,则是一个契约问题.

服务器发布描述器.客户端将描述器转换为模型文本和用户界面.模型创建参数.一个门户端可以从镜头标题中引导请求.服务器执行工具.客户端然后决定结果是否安全和有效足以返回模型.

> 服务器发布描述器;客户端把描述器转换为模型上下文和用户界面;模型生成参数;网关可能根据镜头部路由请求;服务器执行工具;客户端再决定这个结果是否足够安全"",足够有效,可以返回模型。

一个弱的边界破坏了整个链.

考虑五种失败:

- 描述符说结果是对象,但服务器返回了阵列.
- 客户端停止页面化时`nextCursor`没有任何东西.
- 标志参数被反射到HTTP标题中,并成为中间人可见的.
- 作为原始标题,发送一个Unicode路由值,然后门口和来源解释不同的字节.
- 完成终点向无法访问的通话者提供生产环境.

任何这些故障都不能通过更好的提示来解决.

> 这五种失败没有一种可以靠"更好的提示词"修复的方法,它们需要明显的协议契约和应用契约.`nextCursor`为空字符串时客户端停止分页;代码 参数被镜像进入 HTTP 头并对中间人可见; 无码路由值以原始头发送导致网关和源站解释不同的字节;补全端点向无权访问调用者建议生产环境。)

## 合同管道

> **【中文解读】**把每次工具调用看作五道门:发现(读取确定性的分页工具列表)→ 准入(校验每个描述符并应用本地安全策略)→ 调用(校验参数、构建传输元数据)→ 执行(运行处理器、正确分类失败)→ 消费(在交付模型前校验内容块和结构化输出)。关键归属:准入和消费客户两道归宿所有户端服务器无法强迫端信任自己的注解、方案或输出──

处理每个工具通话作为五个门:

1. **Discover.**阅读一个确定性,页面化的工具列表.
2. **Admit.**验证每个描述符并应用本地安全政策.
3. **Invoke.**验证参数和构建运输元数据.
4. **Execute.**运行操作器,并正确分类故障.
5. **Consume.**在使用模型之前验证内容块和结构化输出.

```figure
mcp-contract-pipeline
```

服务器不能强迫客户端相信其注释,方案或输出.

## 运行时间的边界是 JSON 计划的运行时间的边界

> **【中文解读】**在2026-07-28的MCP中,`inputSchema`和 `outputSchema`它们是JSON计划,`$schema`缺省时方言默认 2020-12──三个要点:(1) 无参工具也应声明 `{"type":"object","additionalProperties":false}`比裸体`{"type":"object"}`更严;(2) 服务器一旦发布输出方案,包括`isError: true`每个完整的结果都必须返回符合该方案的状态.`structuredContent`错误标志只分类执行结果,不豁免输出契约;

在MCP中`2026-07-28`现在`inputSchema`其他`outputSchema`使用JSON图案.`$schema`如果没有,默认方言是2020-12.

> 在MCP`2026-07-28`在中,`inputSchema`与`outputSchema`使用JSON方案.`$schema`缺失时默认方言是 2020-12。

输入方案必须是方案对象. 没有参数的工具仍然应该说它接受的内容:

```json
{
  "type": "object",
  "additionalProperties": false
}
```

这比`{ "type": "object" }`通过""来实现,

一旦服务器发布一个,每个完整的工具都会使用
结果承诺返回符合`structuredContent`含结果
随着`isError: true`错误标志分类执行结果;它没有
客户应该验证结果,
对于信任描述者.

> 输出方案是可选的.服务器发布后,每个完整的工具结果都承诺返回符合该方案.`structuredContent`包括`isError: true`结果――错误标志只分类执行结果,不免已发布的输出协议――客户端应验证结果,而不是信任描述符――

### 结构化内容可以是任意的 JSON 值

不要硬码`structuredContent`作为一个词典.

- 一个物体;
- 一个阵列;
- 一条弦;
- 一个号码;
- 一个布尔式;
- `null`现在,我们要去.

这个工具返回一个阵列:

```json
{
  "name": "tag_catalog",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "array",
    "items": {"type": "string"}
  }
}
```

结果是有效的:

```json
{
  "resultType": "complete",
  "content": [
    {
      "type": "text",
      "text": "[\"contracts\", \"mcp\", \"stateless\"]"
    }
  ],
  "structuredContent": ["contracts", "mcp", "stateless"],
  "isError": false
}
```

为了实现兼容性,结构化结果还应包含文本块中的串行 JSON.文本不是验证源. `structuredContent`是的.

> 为了兼容,结构化结果也应在文本块中携带序列化的JSON.`structuredContent`才是.

### 一个小的验证器仍然教导了边界.

课程使用了故意的JSON Schema子集,因为它留在Python标准库内.它检查了样本工具所使用的机制:

> 本课刻意使用一个JSON Schema 子集,以保持在Python 标准库之内.它校验示例工具使用到的机制:对象/阵列/字符串/整数/数量/布尔式/零 类型"",要求 属性"",`additionalProperties: false`、数组项目、enum 取值、字符串最小长度──它不是完整的生产校验器的替代品可重复的课程要点是"校验发生在哪里":描述器 在发现之后、参数在执行之前、结构化结果在消费之前──

- 对象,数组,字符串,整数,数,布尔式和零类型;
- 要求的特性;
- `additionalProperties: false`其他
- 阵列项;
- 值值;
- 弦长度最低.

这不是替代一个完整的生产验证器.可重复使用的课程是验证发生的地方:在描述器的发现后,在执行论证之前,在结构化结果的消费之前.

## 内容块的成本不同.

> **【中文解读】** `content`数组可以混合五种内容块:文本和模型可读的摘要,当作不可信的输出对待) 图像) 选择原则:大件或独立变化的东西链接一次往返的载荷;必须与结果的原子同行的小证据才内嵌.

其他`content`列可以结合多种内容类型.

| Type | Use it for | Main boundary |
|------|------------|---------------|
| `text` | Human and model-readable summaries | Treat text as untrusted output |
| `image` | Visual evidence encoded as base64 | Validate media type and size |
| `audio` | Spoken or recorded output encoded as base64 | Validate media type and duration limits |
| `resource_link` | A URI the client may fetch later | Reauthorize the later resource read |
| `resource` | Data embedded directly in the result | Enforce payload and content limits now |

资源链接不是证明资源在 `resources/list`客户端仍然在遵循URI时应用其资源政策.

> 资源链接不证明该资源出现`resources/list`里;它只是本次工具调用回归的一个引用.

嵌入式资源避免了再一次回路,但增加了当前响应规模. 使用链接用于大型或独立变化的文物. 使用嵌入式资源用于小证据,必须随结果进行原子旅行.

> 嵌入资源省掉一次回来,但会增加当前响应体积.

我们学会了什么?`evidence_bundle`客户端在接受结果之前验证每个区块.

## `x-mcp-header`现在,我们在线上开户.`x-mcp-header`是由元数据

> **【中文解读】** `inputSchema`里属性可以声明`x-mcp-header`客户端在流式HTTP上将该参数视图为`Mcp-Param-{name}`头──目的:让负载均衡、网关或策略引擎不解析 JSON 体就能路由;它不是放凭证的地方──规范约束(全部失败关闭):头名非空且符合HTTP字段名称 语法、大小写不敏感地唯一、属性类型只能是字符串/整数/ boolean(禁止号码)`inputSchema.properties`它们的属性,`oneOf`分支 项目`$ref`引到的定义、输出方案 中一律拒绝) 整数必须在 JavaScript 安全整数范围内.`password`现在,我们要去.`secret`现在,我们要去.`token`现在,我们要去.`api_key`现在,我们要去.`authorization`等名字的描述符 直接拒绝──审计记录头名,不记录值──

房子里面的房产`inputSchema`声明`x-mcp-header`通过流式HTTP,客户端将该参数反映在`Mcp-Param-{name}`现在,我们要去.

```json
{
  "region": {
    "type": "string",
    "x-mcp-header": "Region"
  }
}
```

随着`region: "eu-west"`运输可能会发射:

```http
Mcp-Param-Region: eu-west
```

标注存在于一个负载平衡器,门户或政策引擎可以在没有解析JSON体内进行路由.

协议限制了注释:

- 标题名称是无空的,并遵循HTTP字段名称代码语法;
- 标题名称是不论情况如何,均为独一无二的;
- 属性类型是字符串,整数或布尔式;
- `number`禁止使用;
- 标注仅出现在直接成员的`inputSchema.properties`其他
- 整数值保持在`-9007199254740991`通过`9007199254740991`现在,我们要去.

位置规则是语法和失败关闭. 走整个图案树,
您的验证器不仅了解了这些特性.
嵌套物体下面的注释`properties`其他`oneOf`部门`items`其他
定义`$ref`解决一个引用的方法是
没有将引用的节点转化为直接的顶级属性.

> 位置规则是语法性的且失败关闭――要穿越整个图案树,而不仅仅是你的校验器恰好了解的部分属性――嵌套对象的`properties`,我知道.`oneOf`,我知道.`items`经历`$ref`到达的定义以及任何输出方案的注释都必须拒绝解析引用并不会将引用节点变成直接的顶层属性.

这一课增加了部署政策:拒绝反映如`password`现在`secret`现在`token`现在`api_key`其他`authorization`服务器作者不应该反映敏感参数. 客户端可以把这些建议变成一个严格的录取规则.

检查标题名称,而不是其值.`Mcp-Param-Region`在保持`eu-west`审计活动中.

### 在构建HTTP头之前编码值

参数值只能作为平文传输,只能是不空字符串
可见的ASCII字符`!`通过`~`没有任何相似的
其他一切都用了这个形式:

> 只有当一个参数值是`!`到了`~`的可见ASCII 字符组成的非空字符串、且不像编码哨兵时,才能以明文传输; 其余一切(Unicode、空串、空格、制表符、控制字符、CR/LF、首尾空白、以及以`=?base64?`开头的值) 都编码为`=?base64?{Base64UTF8}?=`对于原始的UTF-8字节做标准基础64,编码前不剪、不归结、不替换――对"长得像哨兵"的值重新编码一次,正是接收方能够恢复字面原文而不是当作传输语法解码的关键――布尔染为小写.`true`现在,我们要去.`false`整数按十进制染且必须落在 JavaScript 安全整数范围内,范围外的值直接拒绝而不是让中间人四舍五进.

```text
=?base64?{Base64UTF8}?=
```

`Base64UTF8`标准的Base64是 UTF-8字节的标准.
编码 Unicode,空字符串,空间,
标签,控制字符,CR或LF,前线或后线白色空间,任何
开始的值`=?base64?`编码一个看起来像哨兵的值是
接收器可以恢复文字原始文本,而不是解码
作为交通语法.

布尔语是小字母.`true`或`false`在基础10中呈现的整数和
值必须在 JavaScript 安全整数范围内留下.
它们被中介拒绝而不是圆.

### 服务器检查镜像副本

在流式HTTP界限上,
服务器必须:

> 在流式HTTP边界上,服务器必须:不区分头号大小写地找到已识别的`Mcp-Param-*`名字;存在时解码精确的基础64 哨兵形式;把解码文本与 JSON体中应参数进行精确比较;在分发之前拒绝缺失、重复、意外、形或不匹配的已识别头──拒绝方式是 HTTP`400`加 JSON-RPC 错误码`-32020`审计记录中只包含已识别的头号和拒绝类别,不包含体值,也不包含编码形式.

1. 发现被认可`Mcp-Param-*`名称,不考虑标题名称情况;
2. 现有时,将精确的base64哨兵形式解码;
3. 完全将解码的文本与相应的JSON体参数进行比较;
4. 拒绝丢失,复制,意想不到,错形或不匹配的东西
   在发送前识别标题.

拒绝是HTTP`400`使用JSON-RPC错误代码`-32020`没有任何一个
审计记录中,该表格的编码标题形式也不属于审计记录.
仅承认标题名称和拒绝类别.

`code/main.py`直接模拟这个边界.[Lesson 09](../../09-mcp-transports/)
涵盖了更广泛的 Streamable HTTP 验证顺序,包括方法和
协议版本平衡.

## 页面标签是不透明的

> **【中文解读】**页面大小和游标格式由服务器定,客户端只有一个决定`nextCursor`是否为`None`,最经典的错误是用Python.`if not result.get("nextCursor")`):空字符串是合法游标,真值判断会提前翻完――正确写法只判`is None`△客户端必须解码、递增、与旧游标比排序或推断页码游标可能被签名、绑定目录版本或映射到私有状态,这是服务器实现细节──无效游标返回 JSON-RPC 无效参数,错误码`-32602`,我知道.

服务器选择页面大小和线程格式.客户端得到一个决定:

```python
if result.get("nextCursor") is None:
    break
cursor = result["nextCursor"]
```

不要写这句话:

```python
if not result.get("nextCursor"):
    break
```

没有字符串是有效的线索.

> 没有什么可言,但它是个合法游标.

客户端不得解码一个线索,增加它,与之前的线索进行订单,或推断页面号码.服务器可以签署一个线索,将其绑定到目录版本,或将其映射到私有状态.这是服务器的实现细节.

样本服务器故意返回`""`客户端必须在第二次请求中发送这个值.

```text
<first request with no cursor>
<second request with cursor "">
```

无效的缓冲器生成 JSON-RPC无效参数,代码 `-32602`现在,我们要去.

## 完成是授权的表面.

> **【中文解读】** `completion/complete`为快速参数和资源模板参数提供补充建议. 它对交互式表单很有用,但可能泄露普通列表.`development`和 `staging`只有操作员才能看到`production`◎原则:对补充请求套件的使用与引用提示/资源相似的授权边界.

`completion/complete`提供快速参数和资源模板参数的建议. 它对于交互式表格是有用的,但它可以泄露普通列表方法保护的名称.

完成请求中,引用和完成的论点:

```json
{
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "deployment_review"
    },
    "argument": {
      "name": "environment",
      "value": "st"
    }
  }
}
```

结果返回最多100个值,并且可以报告`total`另外`hasMore`现在,我们要去.

应用引用提示或资源使用的相同授权界限.`development`其他`staging`只有一个运营商才能接收`production`现在,我们要去.

生产完成还需要:

- 输入验证;
- 电话通讯过;
- 要求在客户中撤销;
- 在服务器中限制速度;
- 限制结果数量;
- 没有暴露敏感的建议值的日志.

完成是协助,而不是发现的绕行.

## 两个错误层.

> **【中文解读】**协议错误与工具执行错误必须分开.MCP 请求无法正确分发时使用JSON-RPC错误(未知工具名称、请求形状形、缺少请求元数据、游标无效);调用已到达工具、工具报告可操作的失败时,使用`isError: true`模型往往可以修复工具执行错误,但无法修复违反自身输出方案的服务器. 如果工具声明输出方案,可操作的失败也必须建模在该方案中.`route_report`失败回复请求的区域加`accepted: false`随着人类可读的错误文本和`isError: true`,我知道.

保持协议错误与工具执行错误分开.

使用JSON-RPC错误,当MCP请求无法正确发送时:

- 工具名称未知;
- 要求形状不良;
- 缺失请求元数据;
- 无效的标记器.

使用完整的工具结果`isError: true`要求到达工具时,工具报告可执行的故障:

- 报告来源不可使用;
- 日期不在支持范围之外;
- 商业规则拒绝请求的操作.

模型通常可以修复工具执行错误.它们不能修复违反其自己的输出方案的服务器.

如果工具声明出口方案,模型可以操作的故障在
图案,样本`route_report`失败返回其请求区域
`accepted: false`通过使用的文件,`isError: true`现在,我们要去.

## 建立它,实现它.

> **【中文解读】** `code/main.py`用Python 标准库同时实现边界两侧.服务器侧:逐请求MCP 元数据校验、带工具与完成能力`server/discover`确定性`tools/list`分页、四个工具描述器 (其中一个必须被拒绝) 数组结构化输出 全部五种内容块类型,解码已识别参数头,并在不匹配时返回HTTP`400`其他类型`-32020`链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接链接`x-mcp-header`位置校验和敏感字段策略、精确的明文可见ASCII或base64 UTF-8编码、能跟随空字符串的不透明游标循环、参数与结果校验、内容块校验、只包含标题不含值的审计事件──那个意图不安全的描述器是教学数据:证明被拒绝的工具不妨碍其他合法工具加载──

`code/main.py`通过Python标准库构建边界的两侧.

服务器实现:

- 根据要求验证MCP元数据;
- `server/discover`具有工具和完成能力;
- 确定性`tools/list`页面化;
- 四个工具描述符,其中一个必须被拒绝;
- 阵列结构输出;
- 每个当前工具内容块类型;
- 通过 HTTP 流式等值门来解码已识别的参数标题和
  返回 HTTP `400`加上JSON-RPC`-32020`没有匹配的情况;
- 授权和限额完成.

客户执行:

- 描述符的录取;
- 树`x-mcp-header`定位验证和敏感领域政策;
- 精确可见ASCII或base64 UTF-8值编码;
- 无透明的针循环,遵循一个空串;
- 论证和结果验证;
- 内容区块验证;
- 标题审计事件包含名称,但不是值.

无人为人所知的描述符是教学数据. 它证明一个被拒绝的工具不会阻止有效的工具加载.

## 让它变得更好.

根据数据库根:

```bash
cd phases/13-tools-and-protocols/28-mcp-tool-contracts-and-content/code
python3 main.py
python3 -m unittest discover tests -v
```

演示版允许的工具,拒绝的描述符,
要求,结构化数组内容,内容区块类型,镜头标题
名称,无论是需要编码的值,HTTP等级状态,以及
调用器过完成值.

## 互动实验室

> **【中文解读】**十步实验的核心不是背后的JSON形状,而是亲眼看每门在"拥有它的边界"上失败:把`tag_catalog.outputSchema.type`改成`object`看客户端拒绝返回数组;让首页 `nextCursor`保持`""`看游标记;给字符串属性加`x-mcp-header: "Authorization"`看准入拒绝; 用 Unicode、换行、首尾空格、字面`=?base64?SGVsbG8=?=`试编码回环;把注解搬进`oneOf`现在,我们要去.`items`现在,我们要去.`$ref`看全树遍历;改掉或删掉已识别的头看 HTTP 边界返回 `400`其他`-32020`,我知道.

开放`code/main.py`查找`TOOLS`现在,我们要去.

1. 改变`tag_catalog.outputSchema.type`其他`array`为了`object`现在,我们要去.
2. 运行演示,客户端应该拒绝返回的阵列.
3. 恢复方案.
4. 保持第一页的.`nextCursor`作为`""`然后返回最后一页
   `nextCursor: None`没有遗漏这个领域.
5. 运行测试,并比较导向器的痕迹.
6. 加入`x-mcp-header: "Authorization"`它们是指一个字符串的属性.
7. 确认描述符的录取在调用之前拒绝.
8. 试试吧`region`包含 Unicode,新线,周围空间的值,以及
   字面上文本`=?base64?SGVsbG8=?=`解码发射的每个标题,并证明
   基本值仍然是正确的.
9. 移动注释到`oneOf`现在`items`其他`$ref`确认
   每个描述符都被拒绝,即使该分支从未被演示程序使用.
10. 删除已识别的标题或更改其解码值.确认HTTP
    边界返回状态`400`和JSON-RPC代码`-32020`现在,我们要去.

目的不是记住一个JSON形状,而是观察每个门在它所有的边界失败.

## 实验室 进步实验

扩大合同实验室`search_evidence`工具.

> 给契约实验扩展一个`search_evidence`工具──九条要求:(1) 输入方案 接受`query`,我知道.`limit`并且一个安全的`region`路由字段;(2) 输出方案是含`uri`,我知道.`title`,我知道.`score`参数拒绝未知属性;`limit`由应用校验设界;(6) 无权访问某个URI调用者永远无法通过补充或工具输出看到它;(7) 测试覆盖不合规分数、非法头注解和两页列表;(8) 头值测试覆盖可见的ASCII、Unicode、控制字符、空白、哨兵样文本和JavaScript安全整数两个边界;(9) HTTP 固定大小写不敏感地接受头号,但缺失或不匹配时返回`400`其他`-32020`,我知道.

要求:

1. 它的输入方案接受`query`现在`limit`并且有一个安全柜`region`路由场
2. 它的输出方案是具有 的对象数组.`uri`现在`title`其他`score`现在,我们要去.
3. 结果包括每个项目兼容性文本和资源链接.
4. 论证拒绝了未知的属性.
5. `limit`申请验证的限制.
6. 没有访问一个URI的调用者从来没有看到完成或工具输出的URI.
7. 测试包括不符合分数,无效标题注释,以及两页列表.
8. 标题值测试涵盖可见的ASCII,Unicode,控制字符,
   它们都具有 JavaScript 安全的整数界限.
9.  HTTP 装置接受不敏感的标题名称,但拒绝缺失
   或与地位相匹配的认可值不一致`400`及代码`-32020`现在,我们要去.

## 运送的艺术品产品

`outputs/skill-mcp-contract-reviewer.md`提供工具描述符,样本结果,页面化行为和完成政策.它返回录取决定,结果验证计划,标题政策和具体失败测试.

> `outputs/skill-mcp-contract-reviewer.md`给它一个工具描述器,样本结果,分页行为和补充策略,它会返回进入决定,结果校验计划,头条策略和具体的失败测试.

## 检查一下.

> **【中文解读】**验收清单要逐条过:`tools/list`重复调用顺序稳定;`nextCursor`为`""`时客户端会发第二次请求;敏感头描述器被排除而其他工具可用;数组过数组方案、对象不过;错误结果不能省略或违反已发布的输出方案;五种内容块全部通过校验;审计事件只命名没有值;明文保持明文、其余值经base64 UTF-8 精确往返;安全整数范围之外的整数被拒绝;藏在`oneOf`现在,我们要去.`items`子的象`$ref`输出方案的注释在准入期被拒绝;大小写不敏感的已识别的头号只有在解码值与体的精确匹配时才通过,否则`400`其他`-32020`分析师的补充永远不回来`production`工具失败使用`isError: true`形协议调用JSON-RPC `error`,我知道.

如果这些说法是真的,课程就会完整:

- `tools/list`在重复通话时返回相同的逻辑顺序.
- 客户在`nextCursor`是`""`现在,我们要去.
- 其他工具仍可用,而不安全的敏感标题描述器被排除在外.
- 一个阵列通过其阵列输出方案.
- 它们是对象的.
- 错误结果不能忽略或违反已发布的输出方案.
- 文字,图像,音频,资源链接和嵌入式资源块验证.
- 标题审计事件包含名称,没有值.
- 简单可见的ASCII仍然是简单的; 统一码,控制,填充,空,
  通过精确的base64 UTF-8编码,看起来像哨兵的值往返.
- 拒绝除JavaScript安全范围之外的镜像整数.
- 下列说明`oneOf`现在`items`嵌物体`$ref`定义或
  在入学期间,输出方案被拒绝.
- 只有解码值时,可通过无情案例的认可标题名称
  完全匹配体;缺失或不匹配的副本产生HTTP `400`
  及JSON-RPC`-32020`现在,我们要去.
- 分析师的完成永远不会回来`production`现在,我们要去.
- 工具故障使用`isError: true`错误的协议调用使用JSON-RPC`error`现在,我们要去.

## 产品失败模式

> 下表左列是失败、中列是你看到的现象、右列是正确的响应──最容易踩的三行:空游标标作为假值(最后几页消失)、敏感值被镜像(秘密 出现在代理/WAF/trace 里)、头体不一致(网关路由到A而源站执行B) ⋅

| Failure | What the learner sees | Correct response |
|---------|-----------------------|------------------|
| Client assumes object output | Valid arrays fail or are silently wrapped | Validate against the published schema without object-only types |
| Empty cursor treated as false | Final pages disappear | Continue whenever `nextCursor` is present and non-null |
| Sensitive value mirrored | Secret appears in proxy, WAF, or trace data | Reject the descriptor and keep secrets in protected request data |
| Raw Unicode or whitespace mirrored | Gateway and origin disagree or the value is normalized | Use exact base64 UTF-8 sentinel encoding and compare after decoding |
| Annotation hidden in a schema branch | A client misses routing metadata during admission | Traverse the entire schema tree and allow only direct top-level properties |
| Large integer mirrored | JavaScript intermediary rounds the routing value | Reject values outside the JavaScript safe integer range |
| Header and body disagree | Gateway routes one target while the origin executes another | Reject before dispatch with HTTP `400` and JSON-RPC `-32020` |
| Output schema ignored | Downstream code consumes corrupt structure | Validate before model or application use |
| Resource link trusted automatically | Caller follows an unauthorized URI | Reauthorize every resource read |
| Completion shares global suggestions | Hidden tenant names leak | Filter by caller, reference, and authorization |
| Tool annotations treated as policy | Destructive operation bypasses confirmation | Enforce authorization and approval outside annotations |
| One malformed tool breaks discovery | Entire server becomes unavailable | Reject the bad descriptor and admit valid tools independently |

## 毕业项目 接下来

阶段13的终点石需要一个可以将几个服务器的工具合并的门户.

> 阶段13 毕业项目需要一个能合并多台服务器工具的网关,本课程提供了其进入核心. 用它给四个毕业证书分类:确定和完整的分页发现,模型暴露之前的描述器,校验,校验的结构化输出加上有界限的内容块,保持授权边界的补充和路由元数据.`tools/call`关于宣称网关兼容要捕获描述符,分页痕迹,进入工具集,拒绝工具集和已经过的结果.

通过该文物来分类四件石头证据:

- 确定性和完整的页面化发现;
- 在模型暴露之前验证描述符;
- 验证的结构化输出加上有界限的内容块;
- 完成和路由以保留授权界限的元数据.

没有成功的网关兼容性`tools/call`记录描述符,页面追踪,被允许的工具集,被拒绝的工具集,以及一个验证结果.

## 关键词 关键词

| Term | Meaning |
|------|---------|
| `inputSchema` | JSON Schema object defining accepted tool arguments |
| `outputSchema` | Optional JSON Schema defining `structuredContent` |
| `structuredContent` | Any JSON value produced by a tool result |
| Content block | Typed text, image, audio, resource link, or embedded resource |
| `x-mcp-header` | Schema annotation that mirrors a primitive argument into Streamable HTTP metadata |
| Opaque cursor | Server-issued pagination token whose value the client does not interpret |
| Completion reference | Prompt name or resource URI/template whose argument is being completed |
| Admission | Client decision to expose or reject a discovered descriptor |

## 继续阅读 继续阅读

- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP Completion](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/completion)
- [MCP Pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination)
- [MCP Streamable HTTP Parameter Headers](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http#custom-headers-from-tool-parameters)
