# 构建一个MCP服务器:无状态Python和TypeScript

> 现代MCP服务器不记得握手. 它验证了每一个请求的元数据,运行一个处理器,并返回一个输入结果.

> **【中文解读】**现代MCP 服务器不记得任何手掌. 它对每个请求进行校验的数据执行一个处理器 返回一个类型化结果. 本课程使用纯标准库把一个笔记服务器写两次 (Python 和 TypeScript),核心是四件事:`params._meta`、必选的`server/discover`、确定性排序可缓存列表以及统一的列表`resultType`结果包装.

> **【拓展：MCP 服务器→Claude 生态开发】**MCP 服务器是Claude 生态的标准工具接口形态:Claude Desktop、Cursor、VS Code等主机都通过studio或HTTP 启动你的服务器并调用其工具──旧教程以初始化握手开场;2026-07-28 之后无状态内核反而更简单没有连接状态要维护,任何副本都能处理任何请求──理解本课的 stdlib 实现后,迁移到官方SDK 只是换语法──

>  **【前置】**学本节前请先掌握:(1) 第13阶段 · 06(MCP 基础) 无状态请求模型`params._meta`其他地方`server/discover`,我知道.`resultType`现在,我们要去.`ttlMs`现在,我们要去.`cacheScope`语语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文: 语文

**Type:** Build | **类型:** 构建
**Languages:** Python, TypeScript | **语言:** Python, TypeScript
**Prerequisites:** Phase 13, Lesson 06 | **前置知识:** Phase 13, Lesson 06
**Time:** ~85 minutes | **时间:** ~85 分钟

## 学习目标

- 执行强制性`server/discover`对于MCP`2026-07-28`现在,我们要去.
  中文翻译:为 MCP `2026-07-28`实现必选的`server/discover`,我知道.
- 在每一个请求中验证协议版本和客户端功能.
  中文翻译:在每个请求上校验协议版本和客户端能力.
- 通过确定性列表排序,将工具,资源和提示展示.
  中文翻译:以确定性列表排序曝光工具、资源和提示──
- 返回`resultType`服务器身份,以及对正确结果的缓存提示.
  中文翻译:在正确的结果上回归`resultType`、服务器身份和缓存提示──
- 在Python和TypeScript中使用新线程有限的工作室使用相同的无国籍合同.
  中文翻译:用Python和TypeScript在换行分隔的工作室上提供同一个无状态契约――

## 问题 问题引入

> **【中文解读】**旧式服务器把第一个请求的功能存存下来复用,好写但运运维:同一进程先后服务多个客户端、远程请求落到不同员工时,过期的能力声明将跨授权边界泄漏行为──2026-07-28 用"每个请求自定义"解决协议层问题;你的应用仍然可以保留笔记、任务等持久状态,唯一的禁令是影响后续请求解码的隐藏协议状态──

服务器在第一次消息后存储客户端功能是容易构建的和难以操作的.同样的过程可能为序列客户端服务.远程请求可能会降落于不同的工作者.一个陈旧的功能声明可以泄露行为跨权限界限.

> 一个在第一条消息后存储客户端能力的服务器容易写,但运行难.

股`2026-07-28`您的应用程序仍然可以保存持久的笔记,工作或明确状态处理.它无法保留的是隐藏的协议状态,改变了后来的请求如何解码.

> 股`2026-07-28`通过让每个请求自定义来解决这个问题的协议部分. 你的应用程序仍然可以保留持久的笔记,任务或显然状态句柄. 它不能保留将改变后续请求解码方式的隐藏协议状态.

通过此课程,我们将两次构建一个笔记服务器.Python 和TypeScript版本仅使用其标准库用于协议核心.

> 本课程将一个笔记本服务器构建两次. 字符号版本和TypeScript版本的协议核心仅使用各自的标准库.

## 概念的核心概念

### 现代发送循环

> **【中文解读】**现代分发循环九步:读一行 JSON-RPC → 解析信封 → 通知不响应 → 校验本请求的参数._meta → 按方法路由 → 用结果Type 和 serverInfo 包装成功 → 写一行响应 → 忘记请求级元数据――studio 三条铁律不变:stdout只写 JSON-RPC(诊断走 stderr) 换行分隔并逐条冲动、stdin EOF 即不是退出――进程生命周期只是传输层生命周期,MCP 会话――

```text
read one JSON-RPC line
parse the envelope
if it is a notification, do not respond
validate params._meta for this request
route by method
wrap success with resultType and serverInfo
write one JSON-RPC response line
forget request-scoped metadata
```

工作室的三个规则仍然重要:

- 写JSON-RPC短信给STOUT,发送诊断给STODR.
  中文翻译:只向stdout 写JSON-RPC消息──诊断信息发发到stderr──
- 通过新线来界定消息,然后将每个回复都填写在线.
  中文翻译:用换行符分隔消息并逐条冲冲响──
- 快速出发,当STDIN到达EOF.
  中文翻译:当我到达欧联时立即退出.

过程寿命是运输寿命,而不是现代的MCP会议.

> 过程生命周期只是传输层生命周期.

> ️ **【易错点】**场景:调试时用 `print()`往 stdout 打印变量 / 后果:stdout 混入非 JSON 文本,客户端解析信封失败断连;另一个常见坑是忘记`flush()`导致响应滞留缓冲区,客户端超时 / 修复:所有诊断输出走`sys.stderr`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`sys.stdout.write(json.dumps(...) + "\n")`后立即`flush()`,我知道.

### 申请验证

每个请求都必须包含:

> 每个请求必须包含:

```json
{
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "notes-client",
        "version": "1.0.0"
      }
    }
  }
}
```

需要使用前两种字段.`clientInfo`确认现有身份形状,但不要把它视为身份验证.

> 两个段落是必填的.`clientInfo`是建议项.校验"存在时的身份形状",但不要把它当作认证.

如果版本不支持,返回代码`-32022`随着`requested`其他`supported`错失的请求元数据是无效的参数,代码`-32602`永远不要填写之前的电话中缺失的字段.

> 如果版本不支持,返回错误码`-32022`附加`requested`与`supported`△缺失请求元数据属于无效参数,返回`-32602`绝对从上一次调用补充全缺失字段.

### 必须发现

现代服务器必须实现`server/discover`完整的发现结果包括支持的现代版本,功能,可选指令,缓存提示和结果中的服务器身份`_meta`其他:

> 现代服务器必须实现`server/discover`△完整的发现结果包括支持现代版本,能力,可选使用说明,缓存提示以及结果`_meta`中的服务器身份:

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {"listChanged": false},
    "resources": {"listChanged": false, "subscribe": false},
    "prompts": {"listChanged": false}
  },
  "ttlMs": 3600000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

发现无法解锁服务器.`tools/list`没有说发现,因为`tools/list`已包含相同的请求元数据.

> 发现不会"解锁"服务器.客户端可以不调用发现而直接调用.`tools/list`因为`tools/list`现在我们也需要同样的数据.

### 工具

> **【中文解读】**工具部分两条线:`tools/list`返回确定性排序的工具描述符(稳定排序改善响应缓存并保持模型上下文稳定),结果必带 `ttlMs`和 `cacheScope`其他`tools/call`返回内容块和 `isError`△错误有两层:协议信封或方法参数无效 → JSON-RPC错误;调用合法但工具本身失败 → `isError: true`◎ 这让模型能在上下文中读到失败原因并自我修复,而不是只收到一个连接层错误――注释(阅读Only/destructive/idempotent/openWorld) 仍然只是提示,宿主拿它做确认和展示,真正授权仍然需要服务器自己执行――

`tools/list`稳定排序改善响应缓存并保持模型文本稳定.结果还需要`ttlMs`其他`cacheScope`现在,我们要去.

> `tools/list`返回确定性排序工具描述符列表――稳定排序改善响应缓存并保持模型上下文稳定――该结果还必须带来`ttlMs`和 `cacheScope`,我知道.

`tools/call`返回内容块和`isError`使用JSON-RPC错误,当协议包裹或方法参数不有效时. 使用 `isError: true`当有效的工具调用运行,但工具本身失败时.

> `tools/call`返回内容块和 `isError`△协议信封或方法参数不有效时使用JSON-RPC错误;合法工具调用已执行,但工具本身失败时使用`isError: true`,我知道.

工具注释仍然是提示,而不是执行:

- `readOnlyHint`
  翻译: 中文`readOnlyHint`现在,我知道.
- `destructiveHint`
  翻译: 中文`destructiveHint`没有什么可做.
- `idempotentHint`
  翻译: 中文`idempotentHint`等提示
- `openWorldHint`
  翻译: 中文`openWorldHint`现在,我们要做什么?

服务器必须执行真正的授权.

> 服务器仍必须执行真正的授权.

### 资源

`resources/list`返回稳定URI描述符. `resources/read`输入内容. 两个都可在 `2026-07-28`两个都包括`ttlMs`其他`cacheScope`现在,我们要去.

> `resources/list`返回稳定URI 描述符──`resources/read`返回类型化内容──两者在`2026-07-28`它们是可存储的,因此它们包含`ttlMs`和 `cacheScope`,我知道.

使用`cacheScope: "private"`对于用户特定的注释数据. 分享缓存不能在授权环境中重复使用私人响应.

> 用户相关笔记数据`cacheScope: "private"`△共享缓存不得跨授权上下文复用一个私人响应──

现代变更交付不使用`resources/subscribe`一个客户打开了`subscriptions/listen`要求`resourceSubscriptions`课程10建立了流量.

> 现代的变更投递不再使用`resources/subscribe`‧ 客户端打开`subscriptions/listen`并请求`resourceSubscriptions`或列表变更类别――10课 构建那个流程――

### 提示

`prompts/list`它们是可隐藏的,也是确定性的.`prompts/get`转换提示结果是完整的,但它不是可缓存列表或读取结果之一,需要缓存提示.

> `prompts/list`可存储且确定性排序`prompts/get`用参数染命名提示──染出的提示结果是完整的,但它不属于必须带缓存提示类型的可缓存列表/读取结果──

### 每个成功的结果都会被打字

> **【中文解读】**所有成功结果走向一个包装函数:打上`resultType: "complete"`和 `_meta`列表,读取和发现这三类处理器 再补`ttlMs`与`cacheScope`△集中一处包装的意义是防止某个处理者 漏掉现代结果字段 漏一个字段,客户端就可能按照旧时代解读你的响应.

例子中每次成功都用一个包装:

```python
def complete(payload):
    return {
        "resultType": "complete",
        **payload,
        "_meta": {SERVER_INFO_KEY: SERVER_INFO},
    }
```

列表,阅读和发现处理人员添加`ttlMs`另外`cacheScope`集中包装可以防止一个处理器默默忽略现代结果场地.

> 列表,读取和发现处理器 添加`ttlMs`与`cacheScope`把包装集中起来,可以防止某个处理者错过现代结果.

### 没有服务器启动的请求

> **【中文解读】**现代服务器可以发出两类信息:与客户端请求相关的通知以及客户端开放的通知.`subscriptions/listen`流上的通知――它必须主动发起自己的JSON-RPC 请求――当处理器需要采样,发出或根输入时,它回来`input_required`结果,由客户端补充内嵌的输入请求后使用新请求 id 重试原方法这是"多轮往返请求" (多轮往返请求) 模式,课11 展开──

现代服务器可以发送与客户端请求相关的通知,或者在客户端开放的通知.`subscriptions/listen`它们不能发送自己的JSON-RPC请求.

> 现代服务器可以发送与客户端请求相关的通知,或在客户端开放.`subscriptions/listen`流上发送通知. 它必须发送自己的JSON-RPC 请求.

当处理器需要采样,引发或根输入时,它返回一个`input_required`结果. 客户端完成嵌入式输入请求,并用新的请求ID重新尝试原始方法. 第11课涵盖了多轮访问请求模式.

> 当处理器需要采样或调试或根输入时,它回来`input_required`结果──客户端补充了内嵌的输入请求,然后使用新的请求ID 重试原方法──第11课讲解那个多轮往返请求模式──

### 显而易见的遗产兼容性

双代服务器也可以实现`2025-11-25`它们在一个明显分离的遗产分支上握手.`_meta`收到时的现象和遗产行为`initialize`现在,我们要去.

> 双时代服务器可以把`2025-11-25`握手实现在一条清晰分离的旧版分支上.`_meta`字段时选择现代行为,收到 `initialize`时选择旧版行为――

不要放一个`2026-07-28`通过传统的握手路径来请求.`resultType`在本课程中,代码是故意现代化的,所以其变量保持可见.

> 不要让`2026-07-28`请走旧版握手路径. 不要把现代.`resultType`字段盖到旧版初始化结果上──本课代码刻意只做现代版,好让不变式保持可见──

>  **【类比】**双时代服务器像机场的双通道边检:一条"电子护照自助通道" (现代:刷护照自描述通过),一条"人工柜台" (旧版:排队登记握手) 〔旅客走哪条由"出示什么证件"一次性判定(有`_meta`三件套 → 现代;发 `initialize`现代要求被拉到排队握手,或者旧版本结果被贴在电子通道的标签.

```figure
t3-dispatch-loop
```

## 用它实现框架

运行Python服务器的有限演示和测试:

> 运行 Python 服务器的有限演示和测试:

```bash
cd code
python3 main.py --demo
python3 -m unittest discover tests -v
```

使用TypeScript运行器运行TypeScript端口:

> 用TypeScript运行器运行TypeScript移植版:

```bash
npx tsx main.ts --demo
```

演示器发送了`server/discover`现在,我们可以看到一个版本错误,然后我们可以看到一个版本错误,然后我们可以看到一个版本错误.

> 演示发送`server/discover`逐个列出原语,调用工具,并显示一个不支持的版本错误.

## 运送它.

这一课是很好的.`outputs/skill-mcp-server-scaffolder.md`它提供了一个现代化的服务器计划,包括一个发现合同,每次请求验证,确定性可缓存列表和可选的孤立遗产适配器.

> 本课交付 `outputs/skill-mcp-server-scaffolder.md`△它产生了一个现代服务器规划:发现契约、逐请求校验、确定性的可缓存列表,以及可选的隔离旧版本适配器──

## 练习题

1. 删除一个请求的功能,证明服务器不重复使用前一个请求的声明.
   中文翻译:从某个请求中移动功能,证明服务器不会复用上一个请求的声明.

2. 扭转`TOOLS`现在`PROMPTS`确认所有列表结果保持稳定.
   中文翻译:反转 `TOOLS`,我知道.`PROMPTS`和笔记的插入顺序.

3. 添加一个破坏性的`notes_delete`执行器内进行授权检查.`destructiveHint`只是一个 UX 暗示.
   中文翻译:添加一个破坏性的`notes_delete`工具,并要求在执行器内部进行授权检查.`destructiveHint`只是为了使用提示.

4. 加入`resources/templates/list`随着`ttlMs`现在`cacheScope`它们是指"定性定制"的.
   中文翻译:添加带 `ttlMs`,我知道.`cacheScope`和确定性排序`resources/templates/list`,我知道.

5. 建立一个独立的传统适配器`2025-11-25`添加测试证明现代请求从来没有进入.
   中文翻译:为 `2025-11-25`构建一个独立的旧版本适配器――添加测试证明现代要求绝不会进入它――

## 关键词 快速查找表

| Term | Meaning |
|------|---------|
| Stateless server | Handles each request from its own metadata without protocol-session memory |
| `server/discover` | Mandatory modern method that advertises versions and capabilities |
| Complete result | Successful modern result with `resultType: "complete"` |
| Cacheable result | Discovery, list, or resource-read result with `ttlMs` and `cacheScope` |
| Deterministic list | Same logical registry produces the same item order |
| Server identity | Recommended `io.modelcontextprotocol/serverInfo` in result `_meta` |
| Tool error | Valid tool call that returns content with `isError: true` |
| Protocol error | Invalid JSON-RPC or MCP request returned through `error` |

> 术语中文对照:无状态服务器 (无状态服务器) 仅凭请求自元数据处理,无协议会话记忆;服务器发现 (必选现代方法,公示版本与能力);完整结果=完整结果 (完整结果) 带`resultType: "complete"`的成功现代结果;可缓存结果;发现/列表/资源读取结果,带 `ttlMs`与`cacheScope`);确定性列表=确定性列表(同逻辑注册表产出同顺序);服务器身份=服务器身份(结果 `_meta`中建议的服务器信息);工具错误=工具错误(合法调用返回内容且`isError: true`);协议错误=协议错误(非法JSON-RPC或MCP 请求,经 `error`返回) 』

## 继续阅读 继续阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)
  中文翻译:MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译:服务器/发现 方法规范
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  中文翻译:工具 原语规范
- [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  中文翻译:资源 原语规范
- [MCP Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  中文翻译:提示 原语规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  中文翻译:stdio 传输层规范
