# 显而易见的作用域和无状态诱导输入

> 根源在MCP 2026-07-28中已经过时,从来没有成为安全沙箱.将可见工具参数或资源URI进行范围,在服务器上授权,并在工具真正需要用户输入时使用MRTR.用户看到决定,模型看到手柄,任何服务器实例都可以处理重试.

> **【中文解读】**本课题在MCP 2026-07-28 版本发生了根本性的变化:Roots (根范围) 正式被废弃它从来不是安全沙箱;作用域信息必须显然出现在工具参数或资源URI,由服务器负责授权;诱导输入) 仍然存在,但当工具真的需要用户输入时,使用MRTR (多轮往返请求) 交付.用户可以看到决策,模型可以看到句柄,任何服务器实例都能处理重试.

> **【拓展：显式作用域→可审计的 MCP 安全模型】**转移作用域从隐藏传输会话状态转移到可见的请求参数,换来可检查可重放可审计可路由与REST无状态束相承:一切影响行为信息都在报文中.授权归服务器.路径包含检查防目录穿越;操作系统沙箱底,三层缺失不可不可缺少. 本课与第13期·11期无状态MRTR和第13期·15期MCP安全) 构成一个完整线索.

>  **【前置】**学习节前请先掌握:(1) 阶段13·07(MCP服务器) 工具调用与能力协商的基本形态;(2) 阶段13·11(无状态MRTR) `input_required`结果`requestState`回传、无会话重试机制,本课的发明 完全建立在它上;

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 11 (stateless MRTR) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 11（无状态 MRTR）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## 学习目标

- 替换过时的 Roots 用明确的工作空间参数,资源URI或服务器配置.
  中文翻译:用显式工作区参数、资源URI或服务器配置取代废弃的Roots──
- 允许,路径控制和操作系统砂盒的分别范围提示.
  中文翻译:把作用域提示与授权,路径包含检查,操作系统和区分开来.
- 交付方式`elicitation/create`通过MRTR`input_required`结果.
  中文翻译:通过MRTR `input_required`结果交付表单模式的`elicitation/create`,我知道.
- 广告在客户端要求能力中进行调试支持,拒绝不支持模式.
  中文翻译:在按请求的客户端能力中声明请求支持,并拒绝不支持的模式──
- 验证`accept`现在`decline`其他`cancel`它们的结果是明确的.
  中文翻译:把 `accept`,我知道.`decline`和 `cancel`现在,我们已经开始了.
- 绑定破坏性确认与认证的主体,原始参数,候选组,和过期.
  中文翻译:把破坏性确认绑定到已认证的主体、原始参数、候选集和过期时间──

## 两个看起来相似的问题似乎是相似的问题.

一个备注工具收到这样的请求:"删除旧的TPS报告".

> 一笔笔记工具收到这样的请求:"删除旧的TPS 报告――"

服务器必须回答两个不同的问题.

> 服务器必须回答两个不同的问题.

1. 哪个工作场所可能会受到这次行动的影响?
   中文翻译:这个操作可以触摸哪个工作区?
2. 用户指的是哪一个相匹配的三张音符?
   中文翻译:三条匹配的笔记里用户指的是哪条?

首先是范围和授权.第二个是互动的歧义. 混合它们导致危险的设计,例如将客户提供的文件作为证明,呼叫者可能会删除它内的所有内容.

> 首先是作用域和授权问题.第二是互动式消歧义.把它们混在一起会导致危险的设计.

> **【中文解读】**作用域(我能碰哪里) 与消歧义(用户指哪个) 是两个正交的问题──前者由服务器授权决定,后者需要用户输入──旧版MCP 用 Roots 表达前者、用反向发动 请表达后者;2026-07-28 把它们都转化为显式、无状态形式:作用域进参数,用户输入 MRTR 重试──

## 根源是一个迁移面.

之前的MCP修改允许客户端广告Roots并通知服务器当清单发生变化时.Roots是信息指导.它们没有限制服务器进程可以读到什么,没有授权调用者,也不创建操作系统沙箱.

> 更早的MCP修改版允许客户端声明 根并不在列表变化时通知服务器──根是信息性指导──它们不约束服务器进程能读什么、不授权调用者、也不构成操作系统沙箱──

欧盟2026-07-28年计划已被废除`roots/list`其他`notifications/roots/list_changed`对于新设计,最好选择以下明确的替代品之一:

> 关于新设计的MCP 2026-07-28废弃`roots/list`和 `notifications/roots/list_changed`△优先选择以下明显替代方案:

- `workspaceUri`或`directory`工具参数,当范围因调用而异.
  中文翻译:作用域随调用变化时,用 `workspaceUri`或`directory`工具参数――
- 运行已经针对资源时的资源URI.
  中文翻译:操作本质上针对某个资源时,使用资源URI.
- 服务器配置,当一个部署拥有一个固定工作空间时.
  中文翻译:一个部署只拥有一个固定工作区时,使用服务器配置.
- 进程沙箱或关闭的文件系统,当代码技术上不能逃脱时.
  中文翻译:当代码必须在技术上无法跨界时,使用进程沙箱或受限文件系统.

如果目前的2026-07-28的整合仍需要`roots/list`在截止窗口期间,服务器将其嵌入MRTR `inputRequests`它们不能发送现场反转请求. 这是一种迁移适配器,而新的处理器应该接受明确的范围.

> 如果现有的2026-07-28 集成在废弃窗口中仍然需要`roots/list`服务器要将它嵌入MRTR中`inputRequests`中──它必须发送活跃的反向请求──那就是迁移适配器;新的处理器应接受显式作用域──

隐藏的运输会议范围更难检查,重播,审核和路线.

> 模型可以看到并重复一个显式句柄──隐藏的传输会话作用域更难检查、重放、审计和路由──

>  **【类比】**根像客人进门口头说"我只去客厅"主人听了但不锁门;显式作用域像每张出入证上都印着房间号,门禁系统(服务器授权) 逐间验票――前者只是"提示",后者才是"凭证"――旧版本把提示当边界使用;新版本要求把边界写成见的参数,再由服务器真正执行授权检查――

### 三个层的规则

显而易见的URI仍然没有授权自己.

> 显式URI 本身仍不能自我授权.

1. **Authorization:**证实的校长是否可以使用这个工作空间?
   翻译: 中文**授权：**这位已认证主体是否被允许使用这个工作区?
2. **Containment:**标准化目标URI是否保持在授权工作空间边界内?
   翻译: 中文**包含检查：**归结后的目标URI是否仍在授权工作区边界内?
3. **Sandbox:**操作系统能阻止一个受损的服务器逃离吗?
   翻译: 中文**沙箱：**操作系统还能阻止一个被攻击的服务器吗?

运行式服务器保留授权工作空间URI的允许列表,正常化百分比编码的路径,检查实际的路径组件边界,并在删除前立即重新检查封存.

> 可运行的服务器维护已授权工作区URI的白名单,归化百分号编码的路径,检查真实的路径组件边界,并在删除前一刻重新检查包含关系――

简单的字符串前检查是错误的:

> 简单的前字符串检查是错的:

```text
allowed:   file:///work/notes
attacker:  file:///work/notes-evil/secret.md
traversal: file:///work/notes/%2e%2e/private.md
```

两个敌对的路径都以误导性字符串开始.首先将路径组件正常化,然后比较.一个生产文件系统服务器也必须防范符号链接竞赛和平台特定的路径语义.

> 两种恶意路径都是以误导性的字符串开头.

> ️ **【易错点】**场景:用`uri.startswith(workspace)`做包含检查 / 后果:`file:///work/notes-evil/secret.md`车和车`file:///work/notes/%2e%2e/private.md`通过检查,造成越界读写 / 修复:先`unquote`归一化,再拆成路径组件逐段比较边界,删除前再查一次;真实文件系统实现还要防符号链接竞争(TOCTOU 窗口) 』

## 发货仍然存在,但交货改变了.

> **【中文解读】**这就是这本课的最大变化点:`elicitation/create`服务器在调用中发出反向 JSON-RPC 请,需要一个活跃会话;2026-07-28的服务器直接返回`resultType: "input_required"`结果,把表单请求装进`inputRequests`客户端染表单,收集答案后带来`inputResponses`用全新的身份证 重试 `tools/call`两次调用之间没有协议会话 状态由签名 `requestState`携带.

调用是当前客户端功能,用于收集用户输入`tools/call`现在`prompts/get`其他`resources/read`方法名称仍然存在`elicitation/create`电线流的方向发生了变化.

> 发动是在`tools/call`,我知道.`prompts/get`或`resources/read`期间收集用户输入现行客户端特性──方法名仍是`elicitation/create`变是线上流转的方向.

服务器不会发送反转JSON-RPC请求.`InputRequiredResult`其他:

> 服务器不发送反向 JSON-RPC 请求――它返回一个`InputRequiredResult`其他:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "delete_choice": {
        "method": "elicitation/create",
        "params": {
          "mode": "form",
          "message": "Choose one matching note and confirm deletion.",
          "requestedSchema": {
            "type": "object",
            "properties": {
              "note_id": {
                "type": "string",
                "enum": ["note-3", "note-7", "note-14"]
              },
              "confirm": {"type": "boolean"}
            },
            "required": ["note_id", "confirm"]
          }
        }
      }
    },
    "requestState": "integrity-protected-delete-state"
  }
}
```

客户端将表格转换.用户可以接受,明确拒绝或拒绝.`tools/call`具有新身份证:

> 客户端使用全新的ID重试原始的`tools/call`其他:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "notes_delete",
    "arguments": {
      "workspaceUri": "file:///Users/alice/Documents/Notes",
      "title": "TPS report"
    },
    "inputResponses": {
      "delete_choice": {
        "action": "accept",
        "content": {"note_id": "note-14", "confirm": true}
      }
    },
    "requestState": "integrity-protected-delete-state",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {"form": {}}
      }
    }
  }
}
```

两个调用之间没有协议会议.服务器验证了回声状态,验证了对预期方案的响应,检查选定的笔记是否在签署的候选组中,重新授权工作空间,重新检查包含,然后删除.

> 两次调用之间没有协议会话――服务器验证回传的状态――按预期方案――校验响应――检查所选笔记确实在签名的候选人集里――重新授权工作区――重新检查包含关系,然后才删除――

## 能力谈判是根据要求进行的能力

支持表格模式调用的客户端声明:

> 支持单单模式调教的客户端声明:

```json
{
  "io.modelcontextprotocol/clientCapabilities": {
    "elicitation": {"form": {}}
  }
}
```

没有任何动力,`"elicitation": {}`其他类型的支持,但仅仅是形式的支持.`"elicitation": {"form": {}}`支持表格模式. 仅使用URL的声明,`"elicitation": {"url": {}}`服务器不得嵌入一个没有当前请求功能的模式,即使在一个早期请求中广告它.

> 空的诱惑能力`"elicitation": {}`兼容性仍然等于仅支持单一表现.`"elicitation": {"form": {}}"`同样支持单个模式.`"elicitation": {"url": {}}"`则不支持──服务器必须嵌入当前请求能力中不存在的模式,即使更早的请求声明过它──

每个请求都包含`io.modelcontextprotocol/protocolVersion`输出一个缺失或非字符串版本`-32602`没有支持的字符串返回`-32022`确切的`supported`其他`requested`缺失或仅使用URL的请求支持返回`-32021`随着`data.requiredCapabilities`设置为`{"elicitation":{"form":{}}}`现在,我们要去.

> 每个请求都带着`io.modelcontextprotocol/protocolVersion`△缺失或非字符串的版本返回`-32602`△不支持的字符串返回`-32022`并附精确的`supported`与`requested`数据――缺失或仅仅 URL 的发明 支持返回 `-32021`没有任何`data.requiredCapabilities`设为`{"elicitation":{"form":{}}}`,我知道.

没有JSON-RPC的封面`id`通过JSON-RPC,将数据处理到一个消息中,并将数据处理到一个消息中.`202 Accepted`没有尸体.

> 没有JSON-RPC`id`封封是通知.处理它,但没有发出JSON-RPC成功或错误响应. 在流式HTTP上,接受的通知没有响应体的收到.`202 Accepted`,我知道.

`clientInfo`必须在诊断中包含,但它是自主报告的,不能识别用户的授权.

> `clientInfo`应包含用于诊断,但它是自报数据,不能作为授权的用户身份.

服务器实现`server/discover`利率`supportedVersions`其他国家`ttlMs`其他`cacheScope`随着`resultType: "complete"`由于它宣传工具,它也实施强制性`tools/list`结果返回了确定性`notes_delete`描述符,一个有效的对象`inputSchema`服务器身份元数据,以及公共缓存提示.

> 服务器实现`server/discover`返回`supportedVersions`能力`ttlMs`和 `cacheScope`没有任何`resultType`为`"complete"`在现代设计中,它不声明根源.`tools/list`△该结果返回确定性`notes_delete`描述符,合法的对象`inputSchema`、服务器身份元数据和公开缓存提示──

>  **【困惑】**问: 客户端上一次请求明确声明过支持表单发出,服务器这次为什么还需要再检查一次? A: 因为2026-07-28 没有会话每个请求都是独立宇宙,能力声明只对当前请求有效.`_meta`,我知道.

## 形式模式 单个模式

> **【中文解读】**标签模式使用限制的平 JSON 方案 描述"用户要填什么":根是对象,属性只能是平的原始字段或枚举数组.定位是"小可用的确认对话框",不是通用单机引擎消歧义,破坏性确认,非敏感偏好收集是其主场.密码,API 密钥,支付凭证绝对不能走单:这些秘密会通过MCP 客户端,可能落入日志或模型上下文.

形式模式使用用于可用对话的限制JSON方案.根是一个对象,其属性是平原原始字段或支持的enum阵列.深嵌的对象和一般用途的文档方案不属于确认对话.

> 表单模式用于可用对话框设计的限制 JSON 方案.根是对象,属性是平的原始字段或支持的枚举数组.深层嵌套对象和通用文档方案不属于确认对话框.

使用表格模式:

> 表单模式适用于:

- 选择几个候选人中的一个;
  中文翻译:从多个候选中选择一个;
- 确认破坏性操作;
  中文翻译:确认一个破坏性操作;
- 收集非敏感偏好;
  中文翻译:收集非敏感偏好;
- 收集少量的值,用户而不是模型必须决定.
  中文翻译:收集少量必须由用户决定的价值.

对于密码,API密钥,访问代币或支付凭证,不要使用表格模式.这些秘密将通过MCP客户端传递,可能会进入日志或模型文本.

> 不要使用单个模式收集密码,API 密钥,访问令牌或支付证券. 这些秘密将通过MCP 客户端,可能进入日志或模型上下文.

服务器再次验证返回的内容.客户端形式验证改善了UX,但不会产生信任.

> 服务器需要再次检验回复内容――客户端表单检验改善UX,但不产生信任――

## 网站地图模式

转载方式将安全的网址发送到带外交互:

> 模式发送一个安全的网址,用于外交互联:

```json
{
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "message": "Connect the report service to continue.",
    "url": "https://mcp.example.com/connect/report-service"
  }
}
```

客户端在开放之前显示完整的目的地,并获得同意.它不得先查询URL.

> 当敏感信息必须直接进入服务器控制的Web流程时,如第三方授权) 使用它.客户端展示完整的目标地址,并开放前征得同意.

`accept`响应是用户同意打开URL.它不证明外部流程完成.在重试时,服务器检查了自己的状态,然后完成或返回另一个状态.`input_required`结果.

> `accept`响应表示用户同意打开这个URL. 它不证明外部流程已完成. 重试时,服务器检查自己的状态,要么完成操作,要么返回另一个.`input_required`结果.

URL发动不是MCP客户端和MCP服务器之间的授权的替代品.它是MCP服务器需要代表用户进行外部互动的原因.服务器必须将浏览器用户绑定到启动MCP操作的相同认证主题.

> URL征集不是MCP客户端与MCP服务器之间授权的替代品. 它用于MCP服务器代表用户执行的外部交互.

## 响应分支

处理行动作为产品决定,而不是伪称:

> 作为产品决策而不是同义词:

| Action | Meaning | Safe server behavior |
|--------|---------|----------------------|
| `accept` | User submitted the interaction | Validate content and continue |
| `decline` | User explicitly refused | Return a complete, non-error refusal outcome |
| `cancel` | User dismissed or could not finish | Stop safely and allow a later retry |

> **【中文解读】**表格对照(zh 版):`accept`= 用户提交交互先校验内容再继续;`decline`= 用户明确拒绝返回完整的非错误拒绝结果;`cancel`关闭或未能完成安全停止,允许稍后再试.

永远不要把缺失内容解释为同意.

> 永远不要把缺失内容解释为同意.永远不要把衰退变成重复弹窗的循环.

## 保护破坏性MRTR状态

候选人列表不能只存在一个提示或未签署的 Base64值. 客户端控制了它回发的一切.

> 候选人列表不能仅仅活在提示词或未签名的Base64值里.

课程签署了包含:

> 本课程对包含以下内容的状态负载签名:

- 证实的资本;
  中文翻译:已认证主体;
- 产品来源方法;
  中文翻译:发起方法;
- 消化`workspaceUri`其他`title`其他
  翻译: 中文`workspaceUri`和 `title`的摘要;
- 在表格中显示的允许的注册表;
  中文翻译:表单中展示的允许笔记 id 集合;
- 运营阶段;
  中文翻译:操作阶段;
- 短期期.
  中文翻译:较短的过期时间――

在突变之前,服务器还检查了现场记录. 这捕获了删除比赛和表格显示后移动到工作空间之外的目标.

> 在变更之前,服务器还会检查活跃的笔记记录.

对于一次性金融或不可逆转的行动,仅HMAC不能阻止在到期期间重复有效状态. 存储和消耗一个nonce,在每一个处理器实例共享的重播商店. 课程注入了一个有限的,TTL切割的存储器,并保持其原子声称,同时执行内存删除. 生产数据库应将非实质性索赔和突变结合到一个交易或相当的条件性写字边界.

> 对于一次性金融操作或不可逆操作,仅靠HMAC无法阻止有效状态在过期内被重置.在所有处理器实例共享的重置储存中,恰好存储并消耗一次不存在. 本课程注入一个有界限的储存,按TL清理的储存,并在执行内存删除期间持有其原子声明.

要求不合格的反应或 否则`cancel`没有发生突变,并且可以在到期之前恢复状态.`decline`课程是终极的,所以课程消耗了无数的内容,而不会删除任何内容.

> 在声明中 之前的交互――形式错误的响应或`cancel`不执行变更,状态在过期前保持可重试――显然`decline`由于这种情况,本课在不删除任何东西的情况下消耗不了.

> ️ **【易错点】**场景:只做HMAC 签名、不做一次性不做 / 后果:攻击者(或重复的客户端重试) 在过期窗口内原样重放相同份`requestState`其他`inputResponses`修复:签名只解决"状态未被改",不解决"状态只使用一次";把"声明不变+执行变更"放进同一原子边界(事务或条件写),并让所有实例共享同一个重放存储.

```figure
t3-roots-boundary
```

## 动手构建

`code/main.py`证明了现代化的`notes_delete`工具:

> `code/main.py`演示一个现代的`notes_delete`工具:

- `tools/list`返回一个确定性,可缓存的描述符,包含所需的工作空间和标题方案.
  翻译: 中文`tools/list`返回带必需工作空间与标题方案的确定性,可缓存描述符.
- 范围是明确的`workspaceUri`关于一个问题.
  中文翻译:作用域是显式的`workspaceUri`参数.
- 服务器配置允许课程主任使用该工作空间.
  中文翻译:服务器配置为课程主体授权该工作区.
-  URI正常化拒绝预写混和编码的穿越.
  中文翻译:URI 归一化拒绝前混和编码穿越──
- 任何破坏性删除都需要形式模式的引发.
  中文翻译:每次破坏性删除都要求表单模式的诱导――
- 诱惑的过程是进入的.`resultType: "input_required"`现在,我们要去.
  中文翻译: 征求 装在 `resultType: "input_required"`里传输.
- 签署`requestState`结合了具体的候选人名单和原始参数.
  中文翻译:签名的 `requestState`绑定精确的候选人列表和原始参数.
- 注射的重播存储器在服务器实例中拒绝相同的接受或拒绝状态.
  中文翻译:注入的重放存储跨服务器实例拒绝与一个已接受或已拒绝的状态.
- 重新尝试使用新的请求ID,并返回`resultType: "complete"`现在,我们要去.
  中文翻译:重试使用全新请求 id 并返回 `resultType: "complete"`,我知道.

数据存储器存储在内存中,因此协议行为很容易检查.

> 在内存中存储数据,便于检查协议行为.

## 运行证

根据数据库根:

> 从仓库根目录:

```bash
cd phases/13-tools-and-protocols/12-mcp-roots-and-elicitation/code
python3 main.py
python3 -m unittest discover tests -v
```

预期的检查站:

> 预期检查点:

- 发现广告没有根的工具.
  中文翻译:发现结果声明工具而没有根.
- 工具发现返回`notes_delete`随着`resultType`服务器身份,缓存提示.
  中文翻译:工具发现返回带 `resultType`、服务器身份和缓存提示`notes_delete`,我知道.
- 申请身份`1`返回表格`inputRequests.delete_choice`现在,我们要去.
  中文翻译:请求 id `1`在`inputRequests.delete_choice`中返回表单.
- 申请身份`2`标签状态和删除完成.
  中文翻译:请求 id `2`回传签名状态并完成删除──
- 预सर्ग路径和加码的穿越路径都无法控制.
  中文翻译:前路径和编码穿越路径都未经含检查──
- 改名不能重新使用原始确认状态.
  中文翻译:改过的标题不能复用原始确认状态――
- 幅不变,则笔记没有变.
  中文翻译:衰退 之后笔记保持不变――
- 两个共享注释和重播状态的服务器对象不能执行一个确认.
  中文翻译:共享笔记与重放状态的两个服务器对象都不能执行相同的确认.
- 空格和明确的表格声明有效,而仅支持URL则返回准确的信息`-32021`形式要求.
  中文翻译:空声明和显式表单声明都能工作,而仅URL 支持返回精确的 `-32021`单单要求.
- 没有支持的版本故障使用了精确的`-32022`数据形状.
  中文翻译:不支持的版本失败使用精确的 `-32022`数据形状
- 没有 id 的通知不会产生 JSON-RPC 响应.
  中文翻译:无 id 的通知不产生 JSON-RPC 响应.

## 运送它.

`outputs/skill-elicitation-form-designer.md`设计了明确的范围,授权检查,MRTR表格,响应分支和状态绑定.它拒绝将废旧的根作为沙盒或通过表格模式收集秘密.

> `outputs/skill-elicitation-form-designer.md`设计显式作用域、授权检查、MRTR表单、响应分支和状态绑定――它拒绝把废弃的根当成盒子,也拒绝通过表单模式收集秘密――

## 练习题

1. 通过 SQLite 取代内存重播存储器. 使用一个交易来索赔非值并删除笔记,然后证明两个进程都不能承诺.
   中文翻译:把内存重置存储换成SQLite――用一个事务声明不删除笔记,然后证明两个进程都不能提交成功――
2. 加入`url`保持第三方的凭证远离`inputResponses`现在,我们要去.
   中文翻译:添加 `url`能力协商和一个带外设置流程.`inputResponses`,我知道.
3. 通过临时的SQLite数据库来取代内存记忆图.
   中文翻译:把内存笔记映射换成临时SQLite 数据库――在变更事务内部重新检查授权和包含关系――
4. 添加一个符号链接政策来实现真正的文件系统.解释为什么单独的URI词汇控制不能阻止符号链接逃逸.
   中文翻译:为真实文件系统实现添加符号链接策略──解释为什么仅靠URI词法包含检查不住符号链接逃逸──
5. 设计一个2025-11-25适配器,将现代MRTR处理器输出映射到传统的服务器启动的发动.将其与当前处理器隔离.
   中文翻译:设计一个 2025-11-25 适配器,把现代MRTR处理器输出映射为旧版服务器发起的发动.

## 关键词 快速查找表

| Term | Meaning in 2026-07-28 |
|------|------------------------|
| Roots | Deprecated informational workspace hints, not authorization or sandboxing |
| Explicit scope | Workspace, directory, or resource handle visible in request arguments |
| Containment | Normalized path-component check that keeps a target inside a boundary |
| Elicitation | Client feature for obtaining user input during an MCP operation |
| Form mode | In-band structured user input using a restricted flat schema |
| URL mode | Out-of-band interaction for sensitive or external workflows |
| MRTR | Stateless input-required result followed by a fresh retry |
| `requestState` | Opaque state echoed exactly and integrity-checked by the server |
| Decline | Explicit user refusal |
| Cancel | Dismissal or incomplete interaction without approval |

> **【中文解读】**术语速查(中英对照):Roots=已废弃的信息性工作区提示,不是授权也不是沙箱; Explicit scope=显式作用域,请求参数中可见的工作区/目录/资源柄句;Containment=包含检查,归结路径组件检查;Elicitation=诱导输入,MCP 操作期间获取用户输入的客户端特性;Form mode表=单模式; Mode=带外交互联URL;MRTR=无状态的输入_所需的结果加全新重试;requestState=样原传并由服务器进行完整检验的不透明状态;Decline=明确拒绝;Cancel=未完成关闭.

## 遗产兼容性

对于一个同龄人,被定制在2025-11-25`roots/list`现在`notifications/roots/list_changed`通过直播服务器启动`elicitation/create`标签适配器遗产. 勿允许一个遗产的根列表绕过服务器授权,并且不要将协议-会议假设带入现代处理器.

> 对于2025年11月25日的终端,`roots/list`,我知道.`notifications/roots/list_changed`和活跃的服务器发起`elicitation/create`可能仍然存在. 给适配器贴上旧标签. 不要让旧版本的根列表绕过服务器授权,也不要把协议会话的假设带入现代处理器.

## 继续阅读 继续阅读

- [MCP 2026-07-28 Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)
  中文翻译:2026-07-28 版 官方规范──
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译:MRTR(多轮往返请求)模式规范,`input_required`结果的权力定义――
- [MCP 2026-07-28 Roots deprecation](https://modelcontextprotocol.io/specification/2026-07-28/client/roots)
  中文翻译:根部 废弃说明
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  翻译: 中文`server/discover`发现机制规范
