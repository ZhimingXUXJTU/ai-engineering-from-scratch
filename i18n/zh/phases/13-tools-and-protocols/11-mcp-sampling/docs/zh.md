# 标签: 移民和无国籍MRTR

> 通过MCP 2026-07-28将新设计的样本取消,并删除服务器到客户端请求道.如果现有工作流仍然需要客户端的模型,服务器将返回一个 `input_required`结果是,客户端将原始请求重新尝试,使用模型输出.

> **【中文解读】**由于新设计中已放弃了采样,并移除了"服务器向客户端发送请求"的通道.`input_required`结果,客户端带着模型输出重试原始请求――推理循环因此变得显然、有界、且在协议层无状态――本课教你两条路:新服务器直连模型提供商;存量 样本 工作流迁至MRTR(多轮回复请求)

> **【拓展：Sampling→MRTR 的方向反转】**旧版样本是协议中的唯一的"反向通道":服务器在处理请求时反过来调用客户端的LLM这正是它被移除的原因,反向通道让服务器逻辑依赖连接存活、难以无状态部署――MRTR 将"反向调用"改写成"结果 + 重试":服务器将要做的事装进`inputRequests`返回,客户端得到模型输出后使用新ID 重新发起相同的方法──方向反转与课时09的传输层无状态化、课时10的`subscriptions/listen`是同一个建筑演进.

>  **【前置】**学习节前请先掌握:(1) 阶段13·07(MCP服务器) 工具/调用的分发与校验;(2) 阶段13·10(资源和提示)`_meta`留关键,`server/discover`,我知道.`resultType`判别符;(3) HMAC / 认证加密的基本概念`requestState`系统的完整性保护需要使用;`sampling/createMessage`求你,请把那套"反向请求"心智模型换成"结果+重试"――

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources and prompts) | **前置知识:** Phase 13 · 07（MCP 服务器）、Phase 13 · 10（资源与提示）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## 学习目标

- 解释为什么MCP 2026-07-28中采样已过时,并选择新服务器的直接模型集成默认.
  中文翻译:解释 采样在 MCP 2026-07-28 中被废弃的原因,并为新服务器选择直连模型集成的默认路径.
- 实现兼容性工作流程`sampling/createMessage`通过多次回路请求 (MRTR).
  中文翻译:实现通过多轮往返请求(MRTR)承载 `sampling/createMessage`兼容工作流.
- 将协议修改和客户端功能放入每个请求中`_meta`它们是什么?
  中文翻译:把协议修订版和客户端能力放进每个请求的`_meta`象征
- 返回`resultType: "input_required"`通过新的JSON-RPCID重新尝试原始方法.
  中文翻译:返回 `resultType: "input_required"`没有使用全新的JSON-RPCID 重试原始方法.
- 保护完整性`requestState`并且将其绑定到本,方法,论点和过期.
  中文翻译:对 `requestState`完成完整性保护,并将其绑定到主体,方法,参数和过期时间.
- 附带模型辅助循环,具有能力检查,批准,响应验证和圆的限制.
  中文翻译:用能力检查,审批,应对校验和轮数上限给模型辅助循环设界.

## 协议之前的决定

> **【中文解读】**首先做构建决策,再谈协议.`summarize_repo`这种工具包含两类工作:确定性工作 (列文件,阅读允许的文件,校验路径,拼装内容) 和模型工作 (挑选代表性文件,综合摘要) 两条合法架构: 1) 新服务器直连模型提供商,服务器自持模型选择,凭证,预算,重试和可观测性,对MCP客户端只返回一个普通的`tools/call`结果;(2) 存量样本工作流迁移到MRTR兼容路径,仅当"使用客户端的模型和凭证"是真实产品需求时才选择它,并且要记录移动计划──

工具如`summarize_repo`需要两种工作:

1. 确定性工作:列表文件,阅读允许文件,验证路径和组装内容.
  中文翻译:确定性工作:列出文件、读取允许的文件、校验路径、拼装内容──
2. 模型工作:选择代表文件并合成总结.
  中文翻译:模型工作:选择代表性文件并综合出摘要。

现在你有两个有效的架构.

> 你现在有两个法律架构.

### 新服务器:直接与模型提供商集成

服务器拥有模型选择,凭证,预算,重试和可观测性.它返回一个普通 `tools/call`结果对MCP客户.

> 服务器自主选择,凭证,预算,重试和可观测性.`tools/call`结果.

当服务器已经是一个托管服务或预测模型行为比使用托管模型更重要时,选择此.

> 当服务器已经成为托管服务,或者当预期的模型行为比"主机模型"更重要时,选择这个路径.

### 现有样本工作流程:将其迁移到MRTR

针对2026-07-28的服务器不能发送直播`sampling/createMessage`要求返回客户.`InputRequiredResult`现在,我们要去.

> 面向2026-07-28的服务器无法向客户端发送活的`sampling/createMessage`请,它被改为把这个请求嵌入一个.`InputRequiredResult`,我知道.

选择这种兼容性路径只有在使用客户端模型时,并且凭证是真正的产品要求.记录一个删除计划,因为新的实现不应该采用过时的样本.

> 只有当"使用客户端的模型和凭证"是真正的产品需求时才选择了这种兼容路径――记录一个移动计划,因为新实现不应采用已废弃的样本――

## 无国籍合同

> **【中文解读】**2026年7月的协议没有`initialize`交换没有`notifications/initialized`没有`Mcp-Session-Id`原本活在手里信息现在随着每个请求传输.服务器在每个请求上验修订版:版本缺失或非字符串 → `-32602`没有支持的字符串 → `-32022`缺少样本测试能力 → `-32021`带`data.requiredCapabilities`无`id`封封是通知:可处理但未发出成功或错误响应,可流动的HTTP适应器对接受的通知返回无主体的`202`每一个成功的现代结果都带有分辨符:`complete`完成`input_required`(客户端须履行嵌入请求并重试),扩展可定义更多(任务 扩展在课13加`"task"`

2026年7月份的协议没有`initialize`交换,没有`notifications/initialized`没有.`Mcp-Session-Id`每个请求都包含了以前在握手中生活的信息:

> 2026年7月的协议没有`initialize`交换没有`notifications/initialized`没有也没有`Mcp-Session-Id`,每一个请求都携带原本活在手中的信息:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

服务器验证每一个请求的修改. 缺失或无字符串版本是无效的参数,`-32602`没有支持的字符串返回`-32022`具有准确的数据`{"supported":["2026-07-28"],"requested":"<client version>"}`缺失的样本能力返回`-32021`随着`data.requiredCapabilities`设置为`{"sampling":{}}`现在,我们要去.

> 服务器在每个请求上验修订版──缺失或非字符串的版本是无效参数`-32602`△不支持的字符串返回`-32022`并带有精确的数据`{"supported":["2026-07-28"],"requested":"<client version>"}`△缺失 样本检测能力返回`-32021`没有任何`data.requiredCapabilities`设为`{"sampling":{}}`,我知道.

没有JSON-RPC的封面`id`接收器可能会处理它,但它不会发出成功响应或错误响应.`202 Accepted`没有接受通知的机构.

> 不带JSON-RPC `id`收件者可以处理它,但既未发出成功响应也未发出错误响应.`202 Accepted`,我知道.

服务器还实现了`server/discover`准确的`supportedVersions`关键,能力,`ttlMs`其他`cacheScope`为了让客户端能够在调用工具之前学习和缓存服务器合同.`tools`服务器也执行强制性`tools/list`它是决定性的.`summarize_repo`描述符包含一个有效的对象`inputSchema`现在`resultType: "complete"`服务器身份元数据,以及公共缓存提示.

> 服务器还实现`server/discover`带精确的`supportedVersions`关键,能力,`ttlMs`和 `cacheScope`让客户端在调用工具之前学习并缓存服务器协议.`tools`服务器还需要实现强制性`tools/list`△其确定性`summarize_repo`描述符包含合法的对象`inputSchema`,我知道.`resultType: "complete"`、服务器身份元数据和公共缓存提示──

每一个成功的现代结果都有一个差异:

- `resultType: "complete"`代表行动结束.
  翻译: 中文`resultType: "complete"`表示操作已完成.
- `resultType: "input_required"`客户必须满足嵌入式请求,并再次尝试.
  翻译: 中文`resultType: "input_required"`表示客户端必须执行嵌入请求并重试.
- 扩展可能定义其他结果类型. 任务扩展添加 `"task"`在第13课.
  中文翻译:扩展可以定义更多结果类型――任务 扩展在 第13课中加入 `"task"`,我知道.

## 一轮MRT,一个轮MTR

> **【中文解读】**服务器在处理请求时无法调回客户端,于是回来`input_required`结果:`inputRequests`是服务器命名的映射,装嵌的 `sampling/createMessage`求你;`requestState`客户端验证自己支持样本采样,应用审批和模型策略,获得模型响应后,使用不同的JSON-RPC id 发送新请求:重复原始方法和参数,加上本轮的`inputResponses`(按 `inputRequests`关键组织) 字节回显`requestState`重试不是协议会话的延续,是新的独立请求.`tools/call`,我知道.`prompts/get`,我知道.`resources/read`上面.

>  **【类比】**像政府大厅的"一次性告知单"――旧样本 像"工作人员直接替你打电话问上级"(服务器反向调用客户端) 上级下班(连接断开) 事情就办不完――MRTR 改成:工作人员给你一张告知单(`inputRequests`现在你必须去盖章的材料清单) 和一张回执(`requestState`证明你已经排队到这个步骤),你去把章盖好(客户端模型补全),再取一个新号(新JSON-RPC id) 再来续办.

服务器无法在处理请求时调用客户端.

> 服务器在处理请求时无法调用客户端.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "pick_files": {
        "method": "sampling/createMessage",
        "params": {
          "messages": [
            {
              "role": "user",
              "content": {
                "type": "text",
                "text": "Choose three representative files and return a JSON array."
              }
            }
          ],
          "systemPrompt": "Return only the requested value.",
          "modelPreferences": {
            "costPriority": 0.8,
            "intelligencePriority": 0.2
          },
          "maxTokens": 400
        }
      }
    },
    "requestState": "opaque-integrity-protected-value"
  }
}
```

客户端验证它支持采样,应用其批准和模型政策,并获得模型响应.然后它发送一个新的请求,使用不同的JSON-RPC id:

> 客户端验证自己支持样本,应用其审批和模型策略,并获得模型响应.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "inputResponses": {
      "pick_files": {
        "role": "assistant",
        "content": {
          "type": "text",
          "text": "[\"README.md\", \"server.py\", \"docs/intro.md\"]"
        },
        "model": "host-model",
        "stopReason": "endTurn"
      }
    },
    "requestState": "opaque-integrity-protected-value",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}}
    }
  }
}
```

复试不是协议会议的延续,而是重复原始方法和参数的新请求,只添加当前轮的参数.`inputResponses`声的声音`requestState`字节对字节.

> 重试不是协议会话的延续. 它是一个新的请求:重复原始方法和参数,只添加当前轮次.`inputResponses`并逐字节回显`requestState`,我知道.

只有在 `tools/call`现在`prompts/get`其他`resources/read`服务器不得返回`input_required`没有相关的方法.

>  MRTR 只允许使用`tools/call`,我知道.`prompts/get`和 `resources/read`△服务器必须从无关方法返回`input_required`,我知道.

## 更多轮状态

> **【中文解读】**多轮工作流 (先挑文件,再总结) 中,服务器把阶段和经验中部数据放进下一个`requestState`◎ 作为攻击者可控待遇:只签名一个裸体阶段名不够.`clientInfo`)、发起方法、原始参数的摘要、短过期时间、当前阶段和已经验的中值──不需要密密性使用HMAC;客户端无法读该状态就用认证加密──坏签名、过期、主体变化、参数变化都使用`-32602`拒绝. 客户端不得不解析或修改.`requestState`只有一个职责,

这一课需要两个模式:

1. `pick_files`返回一个JSON阵列.
  翻译: 中文`pick_files`返回一个JSON 数组.
2. `summary`返回最后的散文.
  翻译: 中文`summary`返回最终散文摘要

每次重试只包含了该轮回复.因此服务器将阶段和验证的中间数据放入下一个轮.`requestState`现在,我们要去.

> 每次重试只带着轮回应. 因此服务器将阶段和已经过的中部数据放入下一个阶段.`requestState`,我知道.

通过使用一个原始的相位名称,将状态绑定到:

> 作为攻击者可控的待遇. 仅仅签署一个裸体阶段名是不够的.

- 证实的资本,非自报 `clientInfo`其他
  中文翻译:已认证主体,而不是自报的`clientInfo`其他
- 产品来源方法;
  中文翻译:发起方法;
- 关于本案的论点的摘要;
  中文翻译:原始参数的摘要;
- 短期的期限;
  中文翻译:较短的过期时间;
- 现阶段和验证的中间值.
  中文翻译:当前阶段和已经验的中值.

使用HMAC,如果不需要保密.使用验证加密,如果客户端不能读取状态.拒绝错误的签名,过期值,改变主题或改变参数.`-32602`现在,我们要去.

> 客户端必须读取状态时使用认证加密.`-32602`拒绝了.

客户不得分析或修改`requestState`唯一的任务是重试时回声.

> 客户端必须解析或修改`requestState`,它唯一的工作是重试时, 显示出那个精确的字符串.

> ️ **【易错点】**场景:`requestState`只编码阶段名不做绑定校验,或客户端图省事解析/改它 / 后果:攻击者伪造状态跳到任意阶段、跨请求重放旧状态、换参数续跑别人开头工作流;改后服务器行为不可预期 / 修复:HMAC或认证加密 + 五重绑定(主体/方法/参数摘要/过期/阶段与中值),任何校验失败一律`-32602`客户端侧只做个字节回显.

## 模型偏好只是提示

> **【中文解读】** `costPriority`,我知道.`speedPriority`,我知道.`intelligencePriority`客户端可以忽略它们,因为模型策略归属于客户端所有.`includeContext`保持为`"none"`其他上下文模式增加泄漏风险,本身已被废弃;在请求中只传递最少明显上下文.

`costPriority`现在`speedPriority`其他`intelligencePriority`客户可能会忽略它们,因为客户拥有模型政策.

> `costPriority`,我知道.`speedPriority`,我知道.`intelligencePriority`客户端可以忽略它们,因为模型策略归于客户端所有.

保持`includeContext`在`"none"`如果您保留已旧的样本流量.其他语境模式增加泄漏风险,本身已过时.请通过请求中最小明确的语境.

> 如果你维护遗产样本流程,把`includeContext`保持为`"none"`其他上下文模式会增加泄漏风险,并且本身已被废弃.

## 安全变化量

> **【中文解读】**客户端是嵌入式 样本请求的信任边界――七条不变量:策略要求时向用户展示服务器想让模型做什么;给MRTR轮数设限;恶意服务器否则可制造模型花费循环;每个采样响应应用文件名,URL或工具输入前校验;限制每轮字节数和代币数;拒绝未在当前客户端能力声明中输入请求;模型输出不得参与授权决策;发行记录方法和输入请求键,但不记得敏感提示内容――`clientInfo`和 `serverInfo`确实是可证实的.

客户是嵌入式样本请求的信任界限.

> 客户端是嵌入式样本请求的信任边界――

- 显示用户在政策需要批准时服务器要求模型做什么.
  中文翻译:策略要求审批时,向用户展示服务器正在让模型做什么──
- 通过MRT,一个恶意服务器可以创建一个模型支出循环.
  中文翻译:给MRTR轮数设上限――否则恶意服务器可以制造模型花费循环――
- 在使用它作为文件名,URL或工具输入之前验证每个样本反应.
  中文翻译:每采样应在被使用文件名、URL或工具输入之前进行校验.
- 每轮的字节和代币限制.
  中文翻译:限制每轮的字节数和符号数.
- 拒绝未在当前客户端功能中声明的输入请求.
  中文翻译:拒绝未在当前客户端能力中声明的输入请求.
- 保持模型输出在授权决策中.
  中文翻译:模型输出不得参与授权决策.
- 记录原始方法和输入请求键,而不记录敏感的提示内容.
  中文翻译:记录发起方法和输入请求键,但不记录敏感提示内容──

`clientInfo`其他`serverInfo`任何一个数据都不能被认证身份.

> `clientInfo`和 `serverInfo`绝对不要把任何一个作为已认证的身份.

```figure
t3-sampling-flip
```

## 建立它,实现它.

> **【中文解读】**示例使用纯标准库运通完整两轮流:发现返回版本和缓存提示;工具发现返回确定性描述符;每次调用校验请求元数据;第一结果嵌入选文件的采样请求;第一次重试证模型结果并嵌入第二请求;HMAC 保护的`requestState`在独立请求之间带走阶段;最终结果`complete`△假宿主模型保证示例确定性 接真宿主时只换 `fake_host_model`服务器边状态机应保持确定 可测

`code/main.py`实现了完全的双轮流,没有第三方包:

- `server/discover`收益`supportedVersions`通过Cache,广告工具支持,并返回缓存提示.
  翻译: 中文`server/discover`返回`supportedVersions`、公告工具支持并返回缓存提示──
- `tools/list`返回一个确定性,可缓存的`summarize_repo`具有对象输入方案的描述符.
  翻译: 中文`tools/list`返回带对象输入方案的确定性可缓存`summarize_repo`描述符.
- `tools/call`根据请求验证了元数据.
  翻译: 中文`tools/call`校验逐请求元数据――
- 首先,结果是`sampling/createMessage`文件选择.
  中文翻译:第一个结果嵌入用于选文件的`sampling/createMessage`,我知道.
- 第一次重试验证实模型结果,并嵌入第二次请求.
  中文翻译:第一次重试验证模型结果并嵌入第二请求――
- 受到HMAC保护`requestState`独立请求之间的阶段.
  中文翻译:HMAC 保护的 `requestState`在独立请求之间带阶段.
- 最终结果使用`resultType: "complete"`现在,我们要去.
  中文翻译:最终结果使用 `resultType: "complete"`,我知道.

假的主机模型使得例子是确定性的.`fake_host_model`服务器边状态机应该保持确定性和可测试性.

> 假宿主模型让示例保持确定性.`fake_host_model`△服务器侧状态机应保持确定和可测试──

## 用它实现框架

根据数据库根:

```bash
cd phases/13-tools-and-protocols/11-mcp-sampling/code
python3 main.py
python3 -m unittest discover tests -v
```

预期的检查站:

- 发现返回一个完整的结果`ttlMs`其他`cacheScope`现在,我们要去.
  中文翻译:发现返回带`ttlMs`和 `cacheScope`完整的结果.
- 工具发现返回相同的分类描述符`resultType`服务器身份,缓存提示.
  中文翻译:工具发现返回相同排序的描述符,带 `resultType`、服务器身份和缓存提示──
- 缺失功能和不支持版本使用精确的`-32021`其他`-32022`错误数据.
  中文翻译:能力缺失和不支持的版本使用精确的 `-32021`和 `-32022`错误数据.
- 没有 id 的通知不会产生 JSON-RPC 响应.
  中文翻译:无 id 的通知不产生 JSON-RPC 响应.
- 要求身份证是`[1, 2, 3]`证明每次MRTR轮都是独立的.
  中文翻译:请求 id 是 `[1, 2, 3]`证明每个MRTR轮次相互独立.
- 首先的两个结果是`input_required`现在,我们要去.
  中文翻译:前两个结果是`input_required`,我知道.
- 最终结果是`complete`包含选定的文件以及总结.
  中文翻译:最终结果是`complete`包含选出的文件和摘要
- 试验中改变原始参数将失败于请求状态检查.
  中文翻译:重试时改变原始参数会未经请求状态检查──

## 运送它.

`outputs/skill-sampling-loop-designer.md`现在是迁移规划师.它首先决定是否应该取消样本以支持直接模型集成.如果需要兼容性,它会产生MRTR轮,状态绑定,能力门,预算,验证和取消计划.

> `outputs/skill-sampling-loop-designer.md`现在是一个迁移规划器. 它先决定是否应该移除样本化,改用直连模型集成. 如果需要兼容,它会产生MRTR轮次,状态绑定,能力门,预算,校验和移除计划.

## 练习题

1. 改变文件选择响应为无效的JSON. 确认服务器返回`-32602`而不是相信模型的输出.
   中文翻译:把文件选择响应改成非法JSON──确认服务器返回 `-32602`而不是信任模型输出.
2. 改变`audience`解释为什么封闭状态阻止了交叉请求的重复使用.
   中文翻译:在首次调用和重试之间变化`audience`解释为什么密封状态能阻跨请求复用
3. 加入第三轮,要求主机批评总结. 携带之前的总结进入签署状态,并将整个流量限制在三个轮.
   中文翻译:添加请主持评审摘要第三轮. 把早期的摘要放进签名状态,并将整个过程限制在三轮.
4. 通过用服务器所有模型适配器取代假的主机回调,删除样本.列出哪些批准,发票和可观察责任转移到服务器.
   中文翻译:用服务器自有的模型适配器替换假宿主调调以移除样本化――列出哪些审批,计费和可观测性职责转移到服务器――
5. 添加使用超过一秒的状态值的过期测试.
   中文翻译:用一个超过截止时间的状态值添加过期测试──

## 关键词 快速查找表

| Term | Meaning in 2026-07-28 | 中文术语 |
|------|------------------------|----------|
| Sampling | Deprecated feature that asks the client's model for a completion | 采样（已弃用） |
| MRTR | Stateless retry pattern for client input required during a request | 多轮往返请求 |
| `InputRequiredResult` | Result with `resultType: "input_required"` | 需输入结果 |
| `inputRequests` | Server-assigned map of embedded elicitation, sampling, or roots requests | 嵌入请求映射 |
| `inputResponses` | Current round's client results keyed like `inputRequests` | 本轮输入响应 |
| `requestState` | Opaque server state echoed exactly by the client and verified by the server | 请求状态（不透明） |
| `resultType` | Required discriminator for modern MCP results | 结果类型判别符 |
| Direct model integration | Recommended replacement for new servers that need model inference | 直连模型集成 |
| Capability gate | Rule that prevents sending an embedded request the client did not advertise | 能力门 |
| Loop budget | Maximum rounds, tokens, bytes, time, and spend allowed for the operation | 循环预算 |

## 遗留兼容性

> **【中文解读】**钉在2025-11-25的客户端仍然可以使用旧服务器启动在活连接上`sampling/createMessage`流程──把这种行为只放进了按版本隔离的适配器,绝不要把有话路径作为2026-07-28 服务器的架构──官方SDK可以为老对端翻译现代`input_required`处理器那片是兼容边界,不是添加新的依赖话语逻辑许可.

预定到2025-11-25的客户端可能仍然使用旧的服务器启动`sampling/createMessage`通过直播连接来传输. 仅在版本特定的适配器中保持这种行为. 不要让会议的路径成为2026-07-28服务器的架构.

> 钉在2025-11-25的客户端仍然可以在活连接上使用较旧的服务器发起`sampling/createMessage`流程――这种行为只保留在按版本隔离的适配器里――不要让有会话的路径成为2026-07-28 服务器的架构――

官方SDK可以翻译现代化`input_required`对于老年同龄人来说,这种闪是兼容性界限,而不是允许添加新的依赖于会议的逻辑.

> 官方SDK可以为较旧对端翻译现代 `input_required`处理器――那片是兼容边界,不是添加新的依赖话语逻辑许可.

## 继续阅读 继续阅读

- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译:MRTR模式的权威规范
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  中文翻译:2026-07-28 修订的完整变更清单
- [MCP Sampling deprecation](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)
  中文翻译:采样 废弃的SEP 提案原文
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  翻译: 中文`server/discover`发现契约规范
