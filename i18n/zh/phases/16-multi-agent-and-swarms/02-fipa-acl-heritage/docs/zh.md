# 菲帕-ACL和言论行为遗产

> 在MCP之前,A2A之前,有FIPA-ACL. 2000年,IEEE智能物理代理基金会批准了一种具有二十个执行语言,两个内容语言和一组互动协议的代理通信语言. 它从行业中消失了,因为对网络的ontology上层费用太重了,但多代理系统的LLM复兴正在地重新实现相同的想法, 这一课将FIPA-ACL认真读取,以便您可以看到2026年协议的决定是什么,是什么新奇,

> **【中文解读】**本课讲 FIPA-ACL 遗产多 代理 系统通信协议的历史标准与现代发展――2000年定型的二十个施事行为 (?? 行为) 内容语言和交互协议,正是2026年MCP/A2A/ACP正在重新发明的东西:JSON 契约替代施事行为,自然语言替代本体――了解这段历史,你才能辨别新协议中哪些是重新发明的,哪些是真正的创新――

> **【拓展：FIPA ACL 遗产→具体应用】**虽然FIPA组织已经在2013年解散,但其核心思想 (如INFORM、REQUEST、PROPOSE) 仍然影响现代多代理协议――2026年的A2A协议可以看作FIPA ACL的LLM时代重生.

>  **【前置】**学本课前请先掌握:阶段16·01 ((为什么需要多个代理) ‧阶段13 ((MCP/工具协议) ‧本课是历史课了解FIPA ACL 才能看懂2026 协议(MCP/A2A/ACP) 是重新发明还是真创新──

>  **【类比】**国际人才联盟 (FIPA-ACL) = "AI界的拉丁语"――2000年的标准,2026年的协议(MCP/A2A) 大量继承其思想──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## 问题 问题引入

> **【中文解读】**2026年代理协议看似百花齐放,实则大多重走一条二十年前的决策树:言语行为理论 (话语即行动)→ KQML 线协议 → FIPA-ACL 标准化 → 因本体过重被网络技术淘汰. 本节给出判断框架:看新协议时,先问它应对FIPA决策树上的哪些节点.

2026年代理协议景观繁忙:工具的MCP,代理的A2A,企业审计的ACP,分散信任的ANP,自然语言内容的NLIP,加上CA-MCP和两十个研究提案.

> 2026年的代理协议领域非常热:MCP 用于工具,A2A 用于代理,ACP 用于企业审计,ANP 用于去中心化信任,NLIP 用于自然语言内容,还有CA-MCP 和二十多项研究建议.

诚实地说,他们中的大多数人正在重新发现一个20岁的决定树. 语音行为理论来自奥斯 (1962) 和塞尔 (1969) 给了我们"表达是行动". 国际合资联盟 (批准2000年) 制订了参考标准化:二十个执行语言,内容语言SL0/SL1,互动协议合同网和订阅通知. 杰德和杰克是Java的参考平台. 2010年左右,这项努力然消逝,因为对应性成本太大,

> 诚实的看法是,其中大多数正在重新发现一个非常具体的20年前的决策树――奥斯 (Austin)  (1962) 和塞尔 (Searle)  (1969) 的言语行为理论告诉我们"话语即行动"――KQML (KQML) 1993将其转化为线协议――FIPA-ACL (Ratified 2000 年) 产生了参考标准化:二十个施事行为――内容语言 SL0/SL1――用于合同网和订阅通知的交互协议――JADE 和 JACK 是Java 参考平台――这一努力在2010年左右消退,因为本体开销太重,Web正在取得胜利――

当你看看MCP时`tools/call`了解传统告诉你两件事:哪些新"创新"实际上是重发发,以及哪些旧失败模式新规将重新发现.

> 当你审视MCP的`tools/call`、A2A任务生命周期或CA-MCP的共享下文存储中,你看到的是FIPA决策的更柔和、JSON原始重述――了解这一遗产告诉你两件事:哪些新"创新"实际上是重新发明的,以及新规范将重新发现哪些旧失败模式――

## 概念的核心概念

> **【中文解读】**本节把谱系讲全:言语行为理论(奥斯/塞尔)→ KQML(1993)→ FIPA-ACL(2000,二十个施事行为 + SL0/SL1 内容语言 + 交互协议)→ JADE/JACK 平台 → 衰落 → LLM 时代以 JSON 语法复活──核心洞察:代理 通信的语法表示小而稳定,只有方式在变化──

### 演讲行为,在一段

> **【中文解读】**一段话讲清理论根基:有些句子不是描述世界,而是改变世界.

奥斯注意到,有些句子没有描述世界, "我承诺. " "我要求. " "我宣布. "他称这些表演演讲. 塞尔尔正式化了五种类别:断言性,指令性,委托性,表达性和声明性. 对于软件代理人来说,KQML (Finin等人,1993) 已经使这一点运行起来:一个信息是执行 (行动) 加上内容 (行动是什么). 国际标准化协会 (FIPA-ACL) 清理了KQML的缺陷,并标准化了大约20个表演.

> 奥斯注意到有些句子没有描述世界它们改变世界――"我承诺"",我请求"",我宣布――"他称这些为施事话语――"Searle将其形式化为五类:断言类"",命令类"",承诺类"",表达类"",宣告类――KQML(Finin等,1993) 将其转化为软件代理的概念:消息是一个施事行为(动作)加上内容(动作关于什么)

### 国际金融协会20个执行项 (部分列表)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

完整的列表在`fipa00037.pdf`问题不是记住它,问题是,每个这些都与一个原始的 LLM 协议最终重新添加.

> 完整列表在`fipa00037.pdf`专注不在于记忆,而是每个人都应对一个LLM协议最终会重新添加原语.

### 标准的FIPA-ACL信息

> **【中文解读】**标准信封只有七个信封字段加一个`content`载荷字段――`conversation-id`和 `reply-with`是请求响应 关联原语现代异步系统不断重新发明的东西;没有它们就无法线程化多轮交换.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

七个字段包含协议封面;一个字段 (`content`其他领域是你每次重新发明的,每次将重试,线程和ontology转载到JSON协议上.

> 七个字段承载协议信封;一个字段(`content`其他字段正是你每次重试的,线程和本体加到JSON协议上重新发明的.

### 两个传统平台

**JADE**(Java Agent DEvelopment framework, 19992020s) 是最常用的符合FIPA的运行时间.代理扩展了一个基类,交换ACL消息,运行在容器内,并通过"行为"协调.

> **JADE**(Java Agent 开发框架,1999-2020年年代) 是最常用的FIPA 兼容运行时.

**JACK**作为一个"非正式的,不太受欢迎的" (FIPA) 信息的基础上,BDI (信仰-愿望-意图) 的推理强调了.

> **JACK**投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者: 投资者:

两者都在网页堆吃了多代理使用案例后减少.MCP和A2A是2026年的运行时间"容器".

> 一旦网络技术吞了多个代理用户,两者都衰退了.

### 为什么FIPA淡

- **Ontology overhead.**国际金融协会要求进行共享的分析`content`网络只是使用HTTP+JSON.
  翻译: 中文**本体开销。**国际金融协会需要共享本体来解析`content` 基于本体达成一致是一个长达数年的标准化过程.
- **Formal semantics nobody used.**语义语言 (SL) 提供了严格的真相条件,但大多数生产系统使用了自由形式的内容,并忽略了形式主义.
  翻译: 中文**没人用的形式语义。**虽然SL (语义语言) 提供了严格的真价值条件,但大多数生产系统使用自由形式的内容并忽略了形式主义.
- **Tooling lock-in.**简单的说法是Java,简单的说法是JACK.
  翻译: 中文**工具锁定。**杰克是商业的.多语言团队已经绕过了两者.
- **The internet won the stack.**后来是JSON-RPC,然后是gRPC取代了ACL的运输.
  翻译: 中文**互联网赢得了技术栈。**后面是JSON-RPC,然后是gRPC取代了ACL的传输.

### 法律法师复兴是FIPA-lite

> **【中文解读】**将FIPA`request`和MCP`tools/call`并排放:同一个信封(谁、对谁、意图、载荷、关联 id),不同的语法──Liu 等 2025 综述明确给出谱系映射:MCP=工具使用语行为,A2A=代理对等语行为,ACP=审计轨迹言行为,ANP=去中心化身份扩展──新规范都是JSON语法、更松语义的ACL 后代──

比较一个FIPA`request`向一个MCP`tools/call`其他:

> 将FIPA `request`与MCP`tools/call`进行比较:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

两者都包含:谁,谁,意图,有效载荷,相关性ID. 两者都不是一个革命对另一个.

> 两者都携带着:谁,对谁,意图,有效载荷,关联ID.

等人在2025年进行的调查 ("MCP, ACP, A2A, ANP的调查"),使这一谱系明确:MCP与工具使用语音行为,A2A与代理同行语音行为,ACP与审计轨道语音行为,ANP与分散身份扩展等相关.新规格是ACL后代,具有JSON语法和较宽松的语义.

> 等人2025年综述("代理互操作性协议综述:MCP,ACP,A2A,ANP",arXiv:2505.02279) 明确指出这一谱系:MCP对应工具使用语音行为,A2A对应代理对等语音行为,ACP对应审计轨迹言语行为,ANP对应去中心化身份扩展──新规范是ACL的后裔,使用JSON语法和更松散的语义──

### 交易,明确表示

> **【中文解读】**权衡要明确说:FIPA 给形式语义(可证明) 规范施事行为目录(不需要重辩) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现――交换的就是"更松散的意图语义换更容易实现"――

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- 形式语义,你可以证明.`inform`意思是发送者相信内容.
  中文翻译:形式语义你可以证明`inform`意思是发送者相信这个内容.
- ,你不必再说"如果我们有"`cancel`没有什么可做.
  中文翻译:规范的施事行为目录你不必再争论"我们应该有`cancel`吗?"
- 几十年的互动协议模式 合同网,订阅-通知,提出-接受 已知正确性特性.
  中文翻译:几十年的交互协议模式合同网、订阅-通知、提议-接受具有已知的正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- 基于JSON的有效载荷,与所有现代工具兼容.
  中文翻译:与每个现代工具兼容的JSON 原生有效载荷──
- 法律法师可以在没有手编码的托学的情况下解释的自然语言内容.
  中文翻译:LLM可以在没有手工编码本体的情况下解释的自然语言内容.
- 网络堆运输 (HTTP,SSE,WebSocket).
  中文翻译:Web 技术传输(HTTP、SSE、WebSocket)
- 通过现场MCP发现能力`server/discover`,我还在.
  中文翻译:通过实时MCP `server/discover`和A2A代理卡 进行能力发现.

为了更轻松地实现,更宽松的意图语义.

> 为了实现更容易实现.

### 值得移植的交互协议

> **【中文解读】**根据国际金融协会 (FIPA) 约15个交互协议,三个值得搬进LLM多代理系统:合同网:任务市场模式,应对16期·16期 协商) 订阅/通知 (每个事件总线) 请求当(持久工作流引擎的延迟任务,应对16期·22期) 它们都能干净映射到现代消息队列,HTTP+轮询或SSE流――

国际金融协会发送了15个互动协议.三个值得将转载到LLM多代理系统:

> 国际法人管理局 (FIPA) 发布了约15个互动协议.其中三个值得延续到 LLM多代理系统中:

1. **Contract Net Protocol (CNP).**管理者问题`cfp`投标者回答:`propose`管理者接受/拒绝. 这就是常规的任务市场模式 (16 · 16 阶段的谈判).
   翻译: 中文**合同网协议 (CNP)。**管理者发布`cfp`投标者使用`propose`响应;管理者接受/拒绝.
2. **Subscribe/Notify.**订阅者发送`subscribe`出版商发送`inform`这就是2026年的每一个活动.
   翻译: 中文**订阅/通知。**订阅者发送`subscribe`发送 发行者在主题变化时发送`inform`这就是2026年每次事件的总线.
3. **Request-When.**"当条件 Y 维持时做X". 延迟操作与预先条件. 2026 模拟是耐用工作流动引擎中的延迟任务 (阶段 16 · 22 生产规模化).
   翻译: 中文**请求-当。**"当条件 Y 成立时执行 X──"带前置条件的延迟动作──2026年类似的东西是持久工作流引擎中的延迟任务──16期 · 22期 生产扩展)──

每个图片都清晰地将信息排队,HTTP+投票或SSE流量进行排列.

> 每个都可以清晰地映射到现代消息队列,HTTP+轮询或SSE流.

### 当你放弃了理学时,什么会破裂

> **【中文解读】**失去自己的价格是**语义漂移**两位代理对同一个词 (("客户") 有微妙不同的概念,接收者按误解行动,而方案验证器抓不住.`content`上加 JSON 方案,类型化工件,

没有共享的定学,代理从自然语言内容中推断意义.**semantic drift**:两个代理使用相同的词 (`"customer"`) 对微妙不同的概念,接收者的代理人根据错误的解释行动,没有方案验证器抓住它.FIPA的学要求将在解析时拒绝信息.

> 没有共享本体, 代理从自然语言内容中推断含义――记录在案的2026年失败模式是**语义漂移**两个代理对同一个词`"customer"`根据误解行动,没有模式验证器能够捕获它.FIPA的本质要求在解析时拒绝该消息.

减轻没有完全的定性:

> 不完全使用本体缓解措施:

-  JSON 方案`content`拒绝电线结构错误.
  中文翻译:对 `content`使用JSON Schema在传输层拒绝结构性错误.
- 类型的文物 (A2A) 拒绝了错误的模式.
  中文翻译:类型化工件(A2A) 拒绝错误的模态。
- 封面中的明确执行性使意图不含糊,即使内容是自然语言.
  中文翻译:信封中显式施事行为 即使内容是自然语言也使意图明确

### 2026年规格,与演讲行为遗产相匹配

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

阅读表表上至下,模式是:保持结构原始,放弃形式主义,让LLM在模糊性上写下.

> 从上到下阅读表格,模式是:保留原始语结构,放弃形式主义,让LLM弥补模糊性.

> **【中文解读】**一句话总结全表:2026 规范保留的是结构性原语 (显式意图,关联 id,异步生命周期),丢弃的是形式主义 (形式语义,本体,逻辑一致性),用 LLM的解释能力填补歧义.

```figure
sw-contract-net
```

## 建立它,实现它.

> **【中文解读】**示例代码是一个纯标准库的FIPA-ACL 翻译器:把五条MCP/A2A 风格消息编码为FIPA-ACL 再解码回来,并运行一个"一个管理者 + 三个投标者"的玩具合同网协商――输出并排展示相同消息的2026 JSON 形态和FIPA-ACL 形态和一些协议原语在往返中存活,只有语法不同――

`code/main.py`实现了纯stdlib的FIPA-ACL翻译器.它编码和解码了正规的ACL包裹,并显示了每个MCP/A2A消息形状如何缩小到相同的七个字段.演示:

> `code/main.py`实现一个纯标准库的FIPA-ACL翻译器――它编解标准ACL信封,并展示每个MCP/A2A消息形状如何简化为相同的七段――演示内容:

- 编码五个MCP式和A2A式消息为FIPA-ACL.
  中文翻译:将五个MCP风格和A2A风格的消息编码为FIPA-ACL。
- 解码FIPA-ACL回到现代相当.
  中文翻译:将FIPA-ACL 解码回现代等效形式──
- 运行一个玩具 合同 经理和三位投标者之间的网络谈判`cfp`现在`propose`现在`accept-proposal`现在`reject-proposal`现在,我们要去.
  中文翻译:使用 `cfp`,我知道.`propose`,我知道.`accept-proposal`,我知道.`reject-proposal`在一个管理者和三个投标者之间进行一个玩具合同网协商.

运行:

```
python3 code/main.py
```

输出是一个横边的痕迹,显示每一个现代消息,在2026 JSON形式和FIPA-ACL形式,然后是合同网投标的回路.同样的协议原始物存活回路;只有语法不同.

> 输出是一个并排追踪,显示每条现代消息的2026 JSON 形式和FIPA-ACL 形式,然后是合同网投标标的往返.

## 用它实现框架

`outputs/skill-fipa-mapper.md`通过FIFA-ACL地图,在采用新协议之前,使用它来回答:"这是真的新吗?`inform`通过JSON语法?"

> `outputs/skill-fipa-mapper.md`是一个技能,读取任何代理协议规范并生成FIPA-ACL映射. 在采用新协议之前使用它来回答:"这是真正的新东西,还是带着JSON语法.`inform`"我没有什么.

## 运送它.

> **【中文解读】**需要重新审核的内容,需要重新审核的内容.

让我们回来,让我们回来.

> 不要把FIPA-ACL带回来.

- 每个信息的原始意图是什么?
  中文翻译:每条消息的意图原语(施事行为) 是什么?
- 要求响应和取消的相关性ID有没有?
  中文翻译:有没有用于请求响应和取消的关联ID?
- 有没有明确的内容语言 (JSON-RPC,简体文本,结构化编写的文物)?
  中文翻译:有没有明显的内容语言?
- 互动协议是第一级的,还是你从零开始重新实施合同网?
  中文翻译:交互协议是一同公民,还是你正在重新实现合同网?
- 如果两个代理人在内容意义上不同意 (语义漂移) 怎么办?
  中文翻译:当两个代理对内容含义有分歧时会发生什么?

在你发送到生产之前,记录这些五个问题.

> 在任何新协议发布到生产环境之前,记录这些五个问题.

## 练习题

1. 跑步`code/main.py`观察回路编码. 确定 FIPA 性能符号对应哪个`tools/call`现在`resources/read`通过A2A创建任务.
   中文翻译:运行 `code/main.py`❖观察往返编码――识别哪些FIPA施事行为对应`tools/call`,我知道.`resources/read`和A2A 任务创建
2. 延长合同网演示`cancel`管理员可以在中期退出任务.`cancel`解决这些问题,你自己做了吗?
   中文翻译:用`cancel`施事行为扩展合同网演示,让管理者可以在投标中撤回任务.`cancel`解决了只靠重试无法解决的故障情况?
3. 阅读FIPA ACL信息结构 (http://www.fipa.org/specs/fipa00037/) 4.14.3 分. 选择本课程未涉及的执行式,并描述其现代的JSON-RPC模拟.
   中文翻译:阅读FIPA ACL 消息结构(http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代JSON-RPC类比──
4. 阅读Liu et al., arXiv:2505.02279. 对于每一个MCP,A2A,ACP,ANP,列出 FIPA执行家族,他们保持和下降.
   中文翻译:阅读 ?? 等,arXiv:2505.02279──对于MCP、A2A、ACP、ANP中的每一个,列出它们保留和丢弃的FIPA施事行为族──
5. 设计一个最小的JSON-Schema`content`一个字段`request`什么是纯自然语言没有的,而且成本是多少?
   中文翻译:为你自己系统中`request`施事行为`content`字段设计一个最小的JSON-Schema――这个模式给你提供了纯自然语言没有什么,价格是什么?

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## 继续阅读 继续阅读

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1)2025年可信调查,将现代规格与FIPA遗产联系起来
  中文翻译:Liu 等人代理 互操作性协议综述,连接现代规范与FIPA 遗产权威 2025 综述
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/)批准的2000年包裹格式
  中文翻译:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/)完整的表演目录
  中文翻译:FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)目前无国有工具使用等价`request`现在,我们要去.`query-ref`
  中文翻译:MCP 2026-07-28 规范`request`现在,我们要去.`query-ref`的当前无状态工具使用等效
- [A2A specification](https://a2a-protocol.org/latest/specification/)现代代理同等的合同网和订阅通知
  中文翻译:A2A 规范合同网和订阅通知的现代代理对等效
