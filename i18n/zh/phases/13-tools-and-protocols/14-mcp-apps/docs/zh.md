# 无国有协议上的MCP应用程序

> 互动结果仍然是MCP工具和资源交换. 2026-07-28的核心使交换自主,而应用程序扩展增加了沙盒浏览器表面.

> **【中文解读】**一个交互式结果仍然是一个MCP工具与资源交换――2026-07-28 核心协议让这个交换自包含(每个请求自带版本与能力,无会话),应用程序扩展在其上叠加沙盒化的浏览器表面――注意本课已完全改版:不再围绕SEP-1724/ext-app SDK,而是围绕`io.modelcontextprotocol/ui`扩展`server/discover`发现以及"UI 声明在工具定义上调用前元数据") 的新契约.

> **【拓展：MCP Apps→Agent 的应用平台】**应用程序是从"文本工具调用"向"应用平台"的关键步骤,类似微信小程序之于微信:写一次`ui://`资源,所有兼容宿主都能染──2026-07-28 重设计后,它与无状态核心严格分层核心管发现/工具/资源,应用程序 扩展管 UI 声明与iframe 桥接,浏览器沙箱管最终边界──

>  **【前置】**学习节前请先掌握: 1) 阶段13·07(MCP服务器) 与13·10(资源)`ui://`是资源的方案,应用程序 声明依赖`tools/list`和 `resources/read`上;(2) 2026-07-28 无状态核心(13·11 MRTR、13·12发出同源) 每个请求携带`_meta`能力,没有`initialize`基于这些信息的重度依赖于它们.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 10（resources）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## 学习目标

- 通过MCP应用程序进行广告`server/discover`根据要求扩展功能.
  中文翻译:通过 `server/discover`和按要求扩展能力声明MCP应用程序
- 声明一个`ui://`在调用工具之前,在工具上使用资源.
  中文翻译:在工具被调用之前就把`ui://`资源声明在工具定义上.
- 返回完整的工具和资源结果,在2026-07-28无状态电线上.
  中文翻译: 在 2026-07-28 无状态线格式上返回完整的工具与资源结果──
- 分开应用程序`ui/initialize`移除MCP核心握手的桥梁消息.
  中文翻译:把应用的`ui/initialize`桥接消息与已移动的MCP核心分手
- 申请原产权验证,沙盒,CSP和最小特权权权.
  中文翻译:应用源校验、沙箱、CSP 和最小权限──

## 问题 问题引入

> **【中文解读】**文本结果只能"描述"时间线,不能给用户一个能过、能检查、能操作的时间线──MCP应用程序使用可扩展解决现象问题:工具定义指向`ui://`资源,主机可以在工具运行前抓取并审查该资源,在沙箱里染,并通过JSON-RPC 桥接中介所有应用动作.前提是别把应用程序包装在旧连接生命周期2026-07-28 核心没有会话.

文本结果可以描述一个时间线. 它不能给用户一个时间线,他们可以过,检查或采取行动.

> 文本结果可以描述一个时间线. 它不能给用户一个能过,能检查,能操作的时间线.

工具定义指出一个 工具的定义是`ui://`工具运行之前,主机可以获取和审查该资源,将其呈现成一个沙盒的iframe,并通过JSON-RPC桥接所有应用程序操作.

> 应用程序使用可选扩展解决现有问题.`ui://`资源──主机可以在工具运行前抓取并审查该资源──在沙箱iframe中染它──并通过JSON-RPC 桥接中介所有应用动作──

2026-07-28 年,核心协议发生了变化.

> 核心协议在2026-07-28 变化了. 不要把App包入旧连接生命周期:

- 没有核心`initialize`要求或`notifications/initialized`通知
  中文翻译:没有核心`initialize`请问,也没有`notifications/initialized`通知.
- 没有.`Mcp-Session-Id`标题
  中文翻译:没有`Mcp-Session-Id`头子
- 每个请求都包含协议版本和客户端功能.`params._meta`现在,我们要去.
  中文翻译:每个请求都在`params._meta`中携带协议版本和客户端能力.
- 服务器实现`server/discover`客户可以检查版本,核心功能和扩展.
  中文翻译:服务器实现 `server/discover`让客户端能够检查版本,核心能力和扩展.
- 每个成功的结果都有一个`resultType`歧视者.
  中文翻译:每个成功都会有结果`resultType`判别符.
- 流式HTTP每请求使用一个POST.现代GET和 DELETE输入点返回405.
  中文翻译:可流动的HTTP 每个请求用一个 POST──现代 GET 与 DELETE 入口返回 405──

应用程序桥仍然有一个叫做`ui/initialize`它属于iframe后消息方言. 它不会重建核心MCP会议.

> 应用程序 桥接仍然有一个名为`ui/initialize`的方法──它属于iframe 信息 方言──它不会重建核心MCP 会话──

>  **【类比】**像"AI助手版微信小程序",2026版又把它搬进"去中心化货架":以前每个主机都有一个挂件API(Claude文物、GPT自定义HTML),应用程序作者需要个个适应;现在一个.`ui://`资源+ 一份扩展声明,任何实现的`io.modelcontextprotocol/ui`作为一个自助餐机,每个请求都需要自带身份和能力,而不是办理会员卡.

## 概念的核心概念

> **【中文解读】**本节走完整个契约链:双协议分层 → 发现(`server/discover`)→ 工具定义上声明 UI(调用前元数据)→ 工具调用只返回数据 → `resources/read`提供可执行内容 → 按可执行内容缓存 → 线格式歧义先行拒绝 → 沙箱是边界而非信任判决 → 桥接有自己的生命周期 → 宿主上下文与能力撤销 → 降级是契约的一部分──

### 两个协议,一个功能

保持层次的明确性:

> 让各层保持显式:

1.  MCP核心携带`server/discover`现在`tools/list`现在`tools/call`现在`resources/list`其他`resources/read`现在,我们要去.
   中文翻译:MCP 核心承载 `server/discover`,我知道.`tools/list`,我知道.`tools/call`,我知道.`resources/list`和 `resources/read`,我知道.
2. 扩展MCP Apps声明UI并定义iframe到主机桥梁.
   中文翻译:MCP Apps 扩展声明 UI 并定义iframe 到主人的桥梁──
3. 浏览器的沙箱规则限制了用户界面可以达到的内容.
   中文翻译:浏览器沙箱规则限制用户界面的范围.

扩展标识符是`io.modelcontextprotocol/ui`客户端在每个请求中发送功能对象内部的扩展支持:

> 扩展标识符是`io.modelcontextprotocol/ui`△两端都选择加入.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/ui": {}
        }
      },
      "io.modelcontextprotocol/clientInfo": {
        "name": "timeline-host",
        "version": "1.0.0"
      }
    }
  }
}
```

`clientInfo`报告的数据是自主报告的数据,而不是授权身份.

> 建议包含`clientInfo`为了诊断,它是自报数据,不是授权身份.

### 在转换之前发现

服务器的发现结果宣传了扩展:

> 服务器的发现结果声明该扩展:

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {},
    "resources": {},
    "extensions": {
      "io.modelcontextprotocol/ui": {}
    }
  },
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "timeline-app-server",
      "version": "2.0.0"
    }
  }
}
```

服务器必须支持发现. 客户端不被迫在每一项行动之前调用发现,因为每个行动都具有自己的能力.

> 服务器必须支持发现.客户端不必在每个动作前都调用发现,因为每个动作都带有能力.

### 声明工具定义中的UI

> **【中文解读】**这就是新版和旧版的最大契约差异:UI 不再依赖于工具调用结果.`_meta.ui`上,而是提前声明在`tools/list`的工具定义里`_meta.ui.resourceUri`换来三个好处:主机可以预装,缓存,并要求显示结果之前做安全审查.

现代应用程序合同将UI与工具绑定在`tools/list`其他:

> 现代应用程序 契约在`tools/list`中把 UI 绑定到工具上:

```json
{
  "name": "notes_timeline",
  "description": "Render a timeline of notes.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "_meta": {
    "ui": {
      "resourceUri": "ui://notes/timeline.html"
    }
  }
}
```

预定的数据是预先调用的元数据. 服务器可以预先加载,缓存和检查HTML,然后结果要求显示. 旧的平板元数据键可能会被兼容代码接受,但新服务器应该发射嵌套的元数据.`_meta.ui.resourceUri`形式.

> 预装,缓存和对HTML进行安全审查. 较旧的平元数据键可能会被兼容代码接受,但新服务器应发出嵌套.`_meta.ui.resourceUri`形式:

`tools/list`包含确定性排序,`ttlMs`其他`cacheScope`使用`private`可见的工具因用户或代币而异.

> `tools/list`在当前核心中,可缓存的.`ttlMs`和 `cacheScope`△随着用户或令牌变化而可见工具使用`private`,我知道.

### 返回数据,然后让主机绑定视图

工具调用返回普通内容加上结构化数据:

> 工具调用返回普通内容加结构化数据:

```json
{
  "resultType": "complete",
  "content": [
    {"type": "text", "text": "Timeline ready."}
  ],
  "structuredContent": {
    "notes": [
      {"id": "note-1", "title": "Discover", "created": "2026-07-28"}
    ]
  },
  "isError": false
}
```

机器主机已经知道该工具属于哪个视图. 避免发明新的内容块,只是为了重复URI.

> 宿主已经知道该工具属于哪个视图了. 不要为了重复URI而发明新的内容块.

### 作为资源使用应用程序

服务器的广告`resources`为了实现这一目标,`resources/list`运行.其确定性列表入口包括可行URI,稳定名称,描述和MIME类型.列表结果包括`resultType`服务器身份元数据,`ttlMs`其他`cacheScope`像确定性工具列表一样.

> 服务器在发现中声明`resources`为了实现强制性`resources/list`操作――其确定性列表条目包含规范URI、稳定名称、描述和MIME类型――列表结果包含`resultType`、服务器身份元数据、`ttlMs`和 `cacheScope`符合确定性工具列表

主人派了`resources/read`在流式HTTP上,请求有:

> 宿主发送 `resources/read`在流式HTTP上,请求形如:

```text
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: resources/read
Mcp-Name: ui://notes/timeline.html
```

标题值和JSON-RPC体必须匹配.不匹配是协议错误`-32020`现在,我们要去.

> 头部值与JSON-RPC 主体必须匹配――不匹配即协议错误`-32020`,我知道.

结果包含HTML资源和缓存提示:

> 结果包含HTML资源和缓存提示:

```json
{
  "resultType": "complete",
  "contents": [
    {
      "uri": "ui://notes/timeline.html",
      "mimeType": "text/html;profile=mcp-app",
      "text": "<!doctype html>...",
      "_meta": {
        "ui": {
          "csp": {
            "connectDomains": [],
            "resourceDomains": [],
            "frameDomains": [],
            "baseUriDomains": []
          },
          "permissions": {}
        }
      }
    }
  ],
  "ttlMs": 60000,
  "cacheScope": "public"
}
```

### 缓存用户界面资源作为可执行内容

应用程序资源不能与普通散文交换.其缓存输入可以执行桥码,染工具数据,并请求主机调整的操作.按法式键键键键.`ui://`服务器身份和版本,资源内容消化,以及授权文本`cacheScope`永远不要在主题中重复使用私有应用资源,因为HTML或其政策元数据可能会不同,即使URI是相同的.

> 应用程序资源不能与普通文本混为一谈. 它的缓存条目可以执行桥接代码,染工具数据,请求主体中介的动作.`ui://`已准备的服务器身份和版本,资源内容摘要,以及`cacheScope`为了私人时代授权下文作为缓存键.绝对不要跨主体复制私有应用资源.

无效的输入`ttlMs`工具的使用期限过去了.`_meta.ui.resourceUri`修改链接,服务器版本或被允许的描述符针变化,或一个被确认的资源更改订阅命名为URI.在重新安装之前重新检查和重新应用CSP和权限审查.一个过时的iframe不能仅仅因为新资源版本尚未加载而保留更广泛的权限.

> 当条目的`ttlMs`过期、工具的`_meta.ui.resourceUri`绑定变化、服务器版本或已准备描述符点变化、或已确认的资源变化订阅点名该 URI 时,使条目失效──重新挂载前重新抓取并重复做CSP与权限审查──旧iframe 不能仅仅是因为新资源版本尚未加载就保留更宽的权限──

### 在功能政策之前拒绝线索模糊性

验证有故意的顺序.首先验证JSON-RPC形状,并需要字符串协议元数据以及对象客户端能力地图.然后将路由头条与机体进行比较.只有那么才能决定是否支持匹配的协议版本.这个顺序阻止代理和服务器解释不同的请求.

> 试验有意图的顺序――先试验JSON-RPC 形状,要求字符串协议元数据和对象型客户端能力映射――再比较路由头和主体――最后才判断是否支持了匹配的协议版本――这个顺序防止代理和服务器对各自的不同请求进行解释――

| Condition | HTTP | JSON-RPC error |
|-----------|------|----------------|
| Header and body version, method, or name disagree | 400 | `-32020` |
| Header and body agree on an unsupported version | 400 | `-32022`, with `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}` |
| `resources/read` lacks the Apps extension capability | 400 | `-32021`, with `data.requiredCapabilities.extensions.io.modelcontextprotocol/ui` |
| Method is unknown | 404 | `-32601` |

> 表格对照(zh 版):头部与主体的版本/方法/名称不一致HTTP 400,错误 `-32020`双方一致但版本不受支持;`-32022`没有任何`data`精确为`{"supported":["2026-07-28"],"requested":"<actual>"}`其他`resources/read`缺少应用 扩展能力400,`-32021`没有任何`data.requiredCapabilities.extensions.io.modelcontextprotocol/ui`方法未知404`-32601`,我知道.

没有JSON-RPC通知`id`服务器从来没有发出一个JSON-RPC响应.一个被接受的HTTP通知返回202的空格.一个错误可以改变HTTP状态,但它仍然不能为通知创建一个JSON-RPC错误体.

> 没有通知`id`因此服务器永远不会为它发出JSON-RPC响应. 被接受的HTTP通知返回202与空主体.

### 沙盒是边界,不是信任判决

> **【中文解读】**沙箱解决"能不能碰到",不解决"该不该相信"――主管控制 iframe:App 不能直接读主管 Cookie、本地存储或页面 DOM,一切特权操作必须过桥──默认值:CSP 域名列表全空再按需加(`connectDomains`管 fetch/XHR/WebSocket,`resourceDomains`管脚本样式图片字体);能打包就打包;没有可见功能就不要申请摄像头/麦克风/定位;postMessage 钉死精确对端源;工具参数、结果、资源文本、桥接消息全部当不可信输入;用户同意留在宿主iframe 不能批准自己的重大操作──切记:放行的域名仍是外泄通道,`connectDomains: ["https://api.example.com"]`这意味着应用程序中的任何脚本都能将获取的数据发送到那里.

应用程序不能直接读取主机的cookies,本地存储器或页面DOM.所有权限的工作必须跨越桥梁.

> 宿主控制 iframe──App 不能直接读取宿主 Cookie──本地存储或页面 DOM──所有特权工作必须通过桥接──

使用以下默认:

> 使用这些默认值:

- 让所有CSP域名列表空,然后只添加应用程序需要的原始. 使用 `connectDomains`对于搜索,XHR和WebSocket;使用`resourceDomains`对于脚本,风格,图像和字体.
  中文翻译:让所有CSP域名列表保持空,然后只添加应用程序需要的源――搜索、XHR 和 WebSocket 用`connectDomains`脚本,样式,图片和字体使用`resourceDomains`,我知道.
- 实际情况下,将代码和数据捆绑起来.
  中文翻译:可行时把代码和数据打包内置.
- 要求任何相机,麦克风或位置许可,除非可见的功能需要它.
  中文翻译:除非有可见功能需要,否则不申请摄像头、麦克风或定位权限.
- 子`postMessage`对于其他任何起源,
  中文翻译:把 `postMessage`坚定在精确的对端源,拒绝来自任何其他源的事件.
- 处理工具参数,工具结果,资源文本和桥梁消息作为不可信的输入.
  中文翻译:把工具参数、工具结果、资源文本和桥接消息都当作不可信输入──
- 保持用户同意在主机中. iframe不能批准其自己的后果行动.
  中文翻译:把用户同意留在宿主.

别复制一个固定的`sandbox`根据应用程序的原始模型和其自己的隔离设计,主机必须选择旗.

> 不要把教程固定在`sandbox`属性复制到每个主机中.主机必须基于应用程序的源模型和自己的隔离设计来选择标志.

允许的域仍然是透路径.`connectDomains: ["https://api.example.com"]`意思是,任何执行应用程序中的脚本都可以将允许的数据发送到那里. 确切的原产地匹配可以防止目的地混,但它并不能决定有效载荷是否适合. 默认保持连接访问空,避免将载体代币放置在iframe中,在实际情况下通过主机进行代理狭窄操作,限制响应和请求大小,并审计用户的行为导致了每个输出请求. 治疗`resourceDomains`单独与`connectDomains`;允许加载字体或脚本不应允许任意加载数据.

> 允许域名仍然是一个外泄通道.`connectDomains: ["https://api.example.com"]`意思是应用程序中执行的任何脚本都能把获准的数据发送到那里――精确源匹配防止目标混,但不判断载荷是否应该当――默认保持连接 访问为空,避免让载体放入iframe,可行时让狭窄操作运行主机代理,限制响应和请求大小,并审计每个站请求由哪个用户动作触发.`resourceDomains`与`connectDomains`必须分开待遇;加载字体或脚本的权限不应授予任意数据传传传.

> ️ **【易错点】**场景:图省事给CSP 开`connectDomains: ["*"]`没有什么.`postMessage`的目标原始 写成`"*"`后果:App内任何脚本都能向任意地址外传数据、接收任意源的恶意消息精确源匹配只防"发错地方",不防"发的东西本身不应发" / 修复:域名列表默认全空、按需加白;`targetOrigin`与`event.origin`校验钉死精确对端;加载权(资源域名) 与上传权(连接域名) 分离;敏感操作走主代理并审计。

### 应用程序桥梁有自己的生命周期

> **【中文解读】**桥接是帖子 上的JSON-RPC 方言,拥有自己的小生命周期:View 发 `ui/initialize`带`appInfo`和 `appCapabilities`)→ 宿主回归能力与宿主上下文 → 视频 才发 `ui/notifications/initialized`现在,主机才开始看看消息.`notifications/initialized`已被移除,应用程序的`ui/notifications/initialized`仍然存在. 这个本地握手只建立"一个iframe与一个宿主"之间的桥,不协商MCP 协议版本、不创建服务器状态、不造传输会话;桥梁产生的核心请求是全新的自包含请求(新JSON-RPC id + 完整请求元数据) ⋅

应用程序桥是一个JSON-RPC方言`postMessage`它可以交换`ui/initialize`其他`ui/*`通过该系统,可通过 技术技术来实现`tools/call`现在,我们要去.

> 应用程序 桥接是`postMessage`上面的JSON-RPC 方言──它可以交换`ui/initialize`和 `ui/*`通知,并可以代理类似核心方法`tools/call`

视图发送`ui/initialize`随着`appInfo`其他`appCapabilities`接待器返回其功能和接待器语境.`ui/notifications/initialized`服务主必须等到此应用程序通知,然后向视图发送消息.

> 查看 发送带`appInfo`和 `appCapabilities`对象`ui/initialize`◎ 主人回归自己的能力与主人上下文──只有在那次响应之后, 查看才发送`ui/notifications/initialized`◎ 宿主必须等到此条 通知后才能向 发消息.

通过本地握手,一个iframe和一个主机框架之间建立了一个桥梁.它不会谈判MCP协议版本,创建服务器状态,或创建运输会话. 注意确切的预写:核心`notifications/initialized`应用程序被删除`ui/notifications/initialized`通过桥接工具调用生成的核心请求是一个新的自主请求,具有新的JSON-RPCID和完整的请求元数据.

> 那个本地握手在"一个iframe和一个主"之间建立桥梁.`notifications/initialized`已被移除,而应用程序的`ui/notifications/initialized`仍在.桥接工具调用生成的核心请求是一个全新的自包含请求,带着新的JSON-RPC id和完整的请求元数据.

### 主机背景,行动和撤销

服务主持人仍然是启动桥接后的权威.一个视频只能通过主机广告的功能请求工具操作,导航,剪辑板使用或其他特权效应.主机验证了输入的请求,当前用户,目标和参数,应用了批准政策,并可能拒绝它.按点击和有效的桥接消息表达了意图;没有一个权威.

> 桥梁初始化后,主持人仍然权威. 查看只能通过主持人声明的能力请求工具动作,导航,剪贴板或其他特权效果. 主持人校验类型化请求,当前用户,目标和参数,应用审批策略,并可以拒绝.

处理主题,大小和可访问性作为一个变化的主机环境而不是一次性染输入:

> 作为一个变化的主机,而不是一次性输入:

- 应用主机提供的颜色和类型符号,然后当主题或对比偏好发生变化时,
  中文翻译:应用主机提供的颜色与排版令牌,并对主题或比率偏好变化作出反应.
- 让查看报告所需的尺寸,但让主机盖并应用iframe尺寸,以便内容不能逃离布局或创建欺骗性叠加.
  中文翻译:让视图 报告期望尺寸,但由主机封顶并应用iframe尺寸,使内容无法逃离布局或制造欺骗性覆盖层.
- 保存键盘顺序,可见的焦点,可访问的名称,屏幕阅读器状态,足够的对比,放大,以及iframe内部的运动减少行为.
  中文翻译:在iframe内保留键盘顺序"",可见焦点"",无障碍名称"",屏幕阅读器状态"",足够对比度"",缩放和减少动效行为"",
- 重新测试主机控制器和查看控制器之间的重点转移,在改变尺寸和重新呈现后.
  中文翻译:在缩放和重染后重新测试主控件与视图控件之间的焦点转移──

应用程序开放期间,功能可被撤销,因为用户改变帐户,政策改变,服务器被隔离,或主机缩小同意.`ui/initialize`在撤销时,拒绝待定的特权调用,停止不再符合政策的网络活动,清除敏感的转载状态,并在用户界面资源本身不再被允许时重新安装或返回文本.

> 能力可在应用程序开放期间被撤销 用户切换账号 策略变化 服务器被隔离 宿主收缩同意 动时检查能力与授权,不仅仅在`ui/initialize`期间──撤销时:拒绝待处理特权调用、停止不再符合策略的网络活动、清除已感染的敏感状态,并在 UI 资源本身不再被访问时重新上传或返回文本──视图必须把拒绝作为正常的结果处理,而不是再试图让主让步为止──

### 倒退是合同的一部分

应用程序知情的服务器仍然可以为不广告UI扩展的主机服务:

> 感知应用程序的服务器仍然能服务未声明 UI 扩展的主机:

- 返回相同的工具`_meta.ui`在`tools/list`现在,我们要去.
  中文翻译:在`tools/list`中返回不带 `_meta.ui`它们是同样的工具.
- 保存一个有用的文本结果`tools/call`现在,我们要去.
  中文翻译:为 `tools/call`保持有用的文本结果.
- 拒绝`resources/read`对于缺失能力错误的UI.
  中文翻译:对 UI 的`resources/read`以缺少能力错误拒绝
- 决策工具是否完成时,永远不要假设一个iframe存在.
  中文翻译:判断工具是否完成时,永远不要假设iframe存在.

```figure
t3-ui-sandbox
```

## 动手构建

`code/main.py`通过Skype,它可以通过Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Skype,Syyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`server/discover`列出工具和资源,执行工具,并提供一个独立的HTML资源.

> `code/main.py`构建一个不使用SDK的小型进程内协议模型――它可以通过`server/discover`声明应用程序列表工具与资源执行工具并提供自含的HTML资源.

该模型已经接受了分析的体体和路由标题. 它不是完整的HTTP适配器,也不解析`Content-Type`或`Accept`. 使用第09课程来完成需要的完整的流通 HTTP 适配器`Content-Type: application/json`其他`Accept`含有两者中的值`application/json`其他`text/event-stream`现在,我们要去.

> 该模型接收已解析的主体和路由头. 它不是完整的HTTP适配器,也没有解析.`Content-Type`或`Accept`◎完整的流式HTTP适配器 ◎要求 ◎`Content-Type: application/json`且`Accept`值同时包含`application/json`与`text/event-stream`)见第09课.

运行它:

> 运行:

```bash
cd phases/13-tools-and-protocols/14-mcp-apps
python3 code/main.py
python3 -m unittest discover code/tests -v
```

检查输出中的四个东西:

> 在输出中检查四件事:

1. 每次电话都是独立的.
   中文翻译:每个调用都是独立的.
2. 每个要求都有`_meta`能否实现.
   中文翻译:每个请求都有`_meta`能力──
3. `resources/list`在任何资源阅读之前返回稳定描述符.
   翻译: 中文`resources/list`在任何资源读取之前返回稳定描述符.
4. 每个结果都有`resultType`服务器身份元数据.
   中文翻译:每个结果都有`resultType`和服务器身份元数据――
5. 没有出现核心会议标识符.
   中文翻译:不出现任何核心会话标识符.

## 运行证

开始`server/discover`确认`io.modelcontextprotocol/ui`在服务器扩展地图中显示.`tools/list`首先,一个是用App功能,一次是没有App功能.

> 从`server/discover`开始确认`io.modelcontextprotocol/ui`出现在服务器扩展映射中――然后调用 `tools/list`两次,一次带应用程序能力一次不带.

阅读`ui://notes/timeline.html`查找HTML`hostOrigin`其他`event.origin`两条线是桥梁没有使用野生卡片目标的最小可见证据.

> 读取`ui://notes/timeline.html`在HTML中搜索`hostOrigin`和 `event.origin`守卫──这两行是"桥接不使用通配目标"的最小可见证据──

## 运送它.

这一课是很好的.`outputs/skill-mcp-apps-spec.md`通过它,在编写框架代码之前,可审查应用程序合同.它迫使作者指定当前的核心包裹,扩展谈判,倒退,UI资源,缓存政策,CSP,权限,桥梁方法和同意界限.

> 本课产出发 `outputs/skill-mcp-apps-spec.md`〔在编写框架代码之前使用它审查应用程序契约〕它强制制作者说清现行核心信封、扩展协商、降级、UI资源、缓存策略、CSP、权限、桥接方法和同意边界──

## 练习题

1. 改为空扩展地图. 确认`tools/list`保持工具,但删除 UI 绑定.
   中文翻译:把客户端能力改为空的扩展映射──确认 `tools/list`保存工具但移除UI 绑定.
2. 发送`Mcp-Name: ui://notes/other.html`通过一个读取时间线的器官.`-32020`现在,我们要去.
   中文翻译:发送 `Mcp-Name: ui://notes/other.html`现在,我已经知道了.`-32020`,我知道.
3. 改变资源为`cacheScope: private`描述使用者特定的条件,证明其合理.
   中文翻译:把资源改为`cacheScope: private`△描述支持这一点的用户特定条件.
4. 转换脚本到`https://static.example.com/app.js`添加这个来源到`resourceDomains`并且解释了新的供应链风险.
   中文翻译:把脚本移到`https://static.example.com/app.js` 加入`resourceDomains`并解释了新的供应链风险.
5. 添加一个`notes_open`按键通过主机. 保持用户批准在主机.
   中文翻译:添加 `notes_open`工具并让按点击经由主机路由.

## 关键词 快速查找表

| Term | Meaning |
|------|---------|
| MCP Apps | Optional extension for interactive HTML rendered by an MCP host |
| `io.modelcontextprotocol/ui` | Extension identifier advertised by both peers |
| `ui://` | Resource scheme for an App's UI template |
| `text/html;profile=mcp-app` | MIME type for MCP App HTML |
| `server/discover` | Current RPC for protocol and capability discovery |
| `resources/list` | Mandatory resource listing method when the server advertises resources |
| `resultType` | Required discriminator for modern successful results |
| `ui/initialize` | First Apps bridge request, separate from removed core initialization |
| `ui/notifications/initialized` | Apps View readiness notification sent after the host responds |
| CSP | Browser policy that restricts scripts, styles, images, and network origins |
| Text fallback | Tool behavior retained for a host without Apps support |

> **【中文解读】**术语速查(中英对照):MCP Apps=由MCP 宿主染交互式 HTML 的可选扩展;`io.modelcontextprotocol/ui`=两端声明的扩展标识符;`ui://`=应用程序UI 模板的资源方案;`text/html;profile=mcp-app`=MCP应用程序HTML的MIME类型;`server/discover`= 协议与能力发现现行PCR;`resources/list`=服务器声明资源后强制性的资源列表方法;`resultType`现代成功结果的必需分辨符;`ui/initialize`应用程序的第一个请求与已移动的核心初始化无关;`ui/notifications/initialized`浏览器策略: 文本倒退=为不支持应用程序的主持人保留文本降级.

## 继续阅读 继续阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
  中文翻译:2026-07-28 基础协议规范──
- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)
  中文翻译:MCP应用程序 扩展总览。
- [MCP Apps build guide](https://modelcontextprotocol.io/extensions/apps/build)
  中文翻译:MCP应用程序 构建指南。
- [Official extension support matrix](https://modelcontextprotocol.io/extensions/client-matrix)
  中文翻译:官方扩展支持矩阵 (中文翻译:官方扩展支持矩阵)
