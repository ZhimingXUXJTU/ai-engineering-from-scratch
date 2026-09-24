# FIPA-ACL 与言语行为的遗产

> 在 MCP 之前，在 A2A 之前，有 FIPA-ACL。2000 年，IEEE 智能物理代理基金会（Foundation for Intelligent Physical Agents）批准了一种 Agent 通信语言，包含二十个施事行为（performatives）、两种内容语言和一组交互协议——合同网（contract net）、订阅/通知（subscribe/notify）、条件请求（request-when）。它从行业中消失是因为本体（ontology）开销对 Web 来说太重，但 LLM 复兴的多 Agent 系统正在悄悄重新实现相同的思想，只是没有形式语义：JSON 契约替代了施事行为，自然语言替代了本体。本课认真阅读 FIPA-ACL，让你看清 2026 年的哪些协议决策是重新发明，哪些是创新，以及当前浪潮将在哪里重新发现 2000 年代已经解决的问题。

> **【中文解读】** 本课讲 FIPA-ACL 遗产——多 Agent 系统通信协议的历史标准与现代演进。2000 年定型的二十个施事行为、内容语言和交互协议，正是 2026 年 MCP/A2A/ACP 们正在重新发明的东西：JSON 契约替代施事行为，自然语言替代本体。读懂这段历史，你才能分辨新协议里哪些是再发明、哪些是真创新。

> **【拓展：FIPA ACL 遗产→具体应用】** FIPA ACL（Foundation for Intelligent Physical Agents Agent Communication Language）是 1990-2000 年代多 Agent 系统的通信标准。虽然 FIPA 组织已于 2013 年解散，但其核心思想（标准化的通信原语如 INFORM、REQUEST、PROPOSE）仍然影响着现代多 Agent 协议。2026 年的 A2A 协议可以看作 FIPA ACL 的 LLM 时代重生。

> 🔗 **【前置】** 学本课前请先掌握：Phase 16·01（为什么需要多 Agent）、Phase 13（MCP/工具协议）。本课是历史课——理解 FIPA ACL 才能看懂 2026 协议（MCP/A2A/ACP）是重新发明还是真创新。

> 💡 **【类比】** FIPA-ACL = "AI 界的拉丁语"。2000 年的标准，2026 年的协议（MCP/A2A）大量继承其思想。区别：FIPA 用形式化本体（重）、现代协议用 JSON+自然语言（轻）。学历史的价值：避免重蹈覆辙——FIPA 因为"本体太重"而死，现代协议要保持轻量。

**类型：** 学习
**语言：** Python（标准库）
**前置条件：** Phase 16 · 01（为什么需要多 Agent）
**预计用时：** 约 60 分钟

## 问题引入

> **【中文解读】** 2026 年的 Agent 协议看似百花齐放，实则大多在重走一条二十年前的决策树：言语行为理论（话语即行动）→ KQML 线协议 → FIPA-ACL 标准化 → 因本体太重而被 Web 技术栈淘汰。本节给出判断框架：看新协议时，先问它对应 FIPA 决策树上的哪个节点。

2026 年的 Agent 协议领域热闹非凡：MCP 用于工具，A2A 用于 Agent，ACP 用于企业审计，ANP 用于去中心化信任，NLIP 用于自然语言内容，加上 CA-MCP 和二十多个研究提案。每个规范都宣布自己是基础性的。

诚实的看法是，它们中的大多数正在重新发现一个非常特定的二十年前的决策树。Austin（1962）和 Searle（1969）的言语行为理论告诉我们"话语即行动"。KQML（1993）将其转化为线协议。FIPA-ACL（2000 年批准）产生了参考标准化：二十个施事行为、SL0/SL1 内容语言、合同网和订阅-通知的交互协议。JADE 和 JACK 是 Java 参考平台。这项努力在 2010 年左右消退，因为本体开销太重，Web 正在获胜。

当你看 MCP 的 `tools/call`、A2A 的任务生命周期或 CA-MCP 的共享上下文存储时，你看到的是 FIPA 决策的更柔软、JSON 原生的重述。了解遗产告诉你两件事：哪些新"创新"实际上是重新发明，以及新规范将重新发现哪些旧失败模式。

## 核心概念

> **【中文解读】** 本节把谱系讲全：言语行为理论（Austin/Searle）→ KQML（1993）→ FIPA-ACL（2000，二十个施事行为 + SL0/SL1 内容语言 + 交互协议）→ JADE/JACK 平台 → 衰落 → LLM 时代以 JSON 语法复活。核心洞察：Agent 通信的语法小而稳定，只有表示方式在变。

### 言语行为，一段话说明

> **【中文解读】** 一段话讲清理论根基：有些句子不是在描述世界，而是在改变世界（"我承诺""我请求"）。Searle 把它们分成五类；KQML 把这个哲学概念变成了软件可执行的线协议；FIPA-ACL 收尾标准化。所有现代 Agent 协议都是这条链条的后代。

Austin 注意到有些句子不是描述世界——它们改变世界。"我承诺。""我请求。""我宣布。"他称之为施事话语（performative utterances）。Searle 将其形式化为五个类别：断言类（assertive）、指令类（directive）、承诺类（commissive）、表达类（expressive）、声明类（declarative）。KQML（Finin 等人，1993）将此操作化为软件 Agent：消息是一个施事行为（动作）加上内容（动作关于什么）。FIPA-ACL 清理了 KQML 的缺陷，并标准化了大约二十个施事行为。

### 二十个 FIPA 施事行为（部分列表）

| 施事行为 | 意图 |
|---|---|
| `inform` | "我告诉你 P 为真" |
| `request` | "我请求你做 X" |
| `query-if` | "P 为真吗？" |
| `query-ref` | "X 的值是什么？" |
| `propose` | "我提议我们做 X" |
| `accept-proposal` | "我接受该提案" |
| `reject-proposal` | "我拒绝该提案" |
| `agree` | "我同意做 X" |
| `refuse` | "我拒绝做 X" |
| `confirm` | "我确认 P 为真" |
| `disconfirm` | "我否认 P" |
| `not-understood` | "你的消息无法解析" |
| `cfp` | "关于 X 征求提案" |
| `subscribe` | "当 X 变化时通知我" |
| `cancel` | "取消正在进行的 X" |
| `failure` | "我尝试了 X 但失败了" |

完整列表在 `fipa00037.pdf`（FIPA ACL 消息结构）中。重点不是记住它——重点是每一个都对应一个 LLM 协议最终会重新添加的原语。

### 规范的 FIPA-ACL 消息

> **【中文解读】** 标准信封只有七个信封字段加一个 `content` 载荷字段。`conversation-id` 和 `reply-with` 是请求-响应关联原语——现代异步系统不断重新发明的东西；没有它们就无法线程化多轮交换。

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

七个字段承载协议信封；一个字段（`content`）承载负载。其余字段正是你每次在 JSON 协议上添加重试、线程化和本体时重新发明的东西。

### 两个遗留平台

**JADE**（Java Agent DEvelopment framework，1999–2020 年代）是最常用的 FIPA 兼容运行时。Agent 继承基类，交换 ACL 消息，在容器内运行，并使用"行为"进行协调。交互协议库附带合同网、订阅-通知、条件请求和提议-接受。

**JACK**（Agent Oriented Software，商业产品）强调在 FIPA 消息之上的 BDI（信念-愿望-意图）推理。更正式，采用较少。

一旦 Web 技术栈吞噬了多 Agent 用例，两者都衰落了。MCP 和 A2A 是 2026 年的运行时"容器"。

### FIPA 为何衰落

- **本体开销。** FIPA 需要共享本体来解析 `content`。就本体达成一致是一个长达数年的标准化过程。Web 直接使用了 HTTP + JSON。
- **没人使用的形式语义。** SL（语义语言）给出了严格的真值条件，但大多数生产系统使用自由格式内容并忽略了形式主义。
- **工具锁定。** JADE 只有 Java 版本；JACK 是商业的。多语言团队绕过了两者。
- **互联网赢得了技术栈。** REST，然后是 JSON-RPC，然后是 gRPC 替代了 ACL 的传输。

### LLM 复兴是 FIPA 轻量版

> **【中文解读】** 把 FIPA `request` 和 MCP `tools/call` 并排放：同一个信封（谁、对谁、意图、负载、关联 id），不同的语法。Liu 等 2025 综述明确给出谱系映射：MCP=工具使用言语行为，A2A=Agent 对等言语行为，ACP=审计轨迹言语行为，ANP=去中心化身份扩展。新规范都是 JSON 语法、更松语义的 ACL 后代。

比较 FIPA 的 `request` 与 MCP 的 `tools/call`：

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

相同的信封，不同的语法。两者都承载：谁、对谁、意图、负载、关联 ID。两者之间没有革命——它们是相同设计上的不同权衡。

Liu 等人 2025 年的调查（"Agent 互操作性协议调查：MCP、ACP、A2A、ANP"，arXiv:2505.02279）明确说明了这种谱系：MCP 对应工具使用言语行为，A2A 对应 Agent 对等言语行为，ACP 对应审计轨迹言语行为，ANP 对应去中心化身份扩展。新规范是具有 JSON 语法和更松散语义的 ACL 后代。

### 权衡，明确说明

> **【中文解读】** 权衡要明说：FIPA 给形式语义（可证明）、规范施事行为目录（不用重争论）、带正确性保证的交互协议模式；现代规范给 JSON 原生负载、自然语言内容、Web 传输、能力发现。交换的就是"更松散的意图语义换更容易的实现"。

**FIPA 给你的而现代规范丢弃的：**

- 形式语义——你可以证明 `inform` 意味着发送者相信该内容。
- 规范的施事行为目录——你不必重新争论"我们应该有 `cancel` 吗？"。
- 数十年的交互协议模式——合同网、订阅-通知、提议-接受——具有已知的正确性属性。

**现代规范给你的而 FIPA 没有的：**

- 与每个现代工具兼容的 JSON 原生负载。
- LLM 可以无需手工编码本体即可解释的自然语言内容。
- Web 技术栈传输（HTTP、SSE、WebSocket）。
- 通过实时 MCP `server/discover` 和 A2A Agent Card 进行能力发现。

更松散的意图语义换取更容易的实现。这就是确切的权衡。

### 值得移植的交互协议

> **【中文解读】** FIPA 约 15 个交互协议里，三个值得搬进 LLM 多 Agent 系统：合同网（任务市场模式，对应 Phase 16·16 协商）、订阅/通知（每个事件总线）、请求-当（持久工作流引擎的延迟任务，对应 Phase 16·22）。它们都能干净映射到现代消息队列、HTTP + 轮询或 SSE 流。

FIPA 提供了约 15 个交互协议。三个值得延续到 LLM 多 Agent 系统中：

1. **合同网协议 (CNP)。** 管理者发出 `cfp`（征求提案）；竞标者以 `propose` 响应；管理者接受/拒绝。这是规范的任务市场模式（Phase 16 · 16 协商）。
2. **订阅/通知。** 订阅者发送 `subscribe`；发布者在主题变化时发送 `inform`。这就是 2026 年的每个事件总线。
3. **条件请求。** "当条件 Y 成立时做 X。"带前置条件的延迟动作。2026 年的类似物是持久工作流引擎中的延迟任务（Phase 16 · 22 生产扩展）。

每个都可以干净地映射到现代消息队列、HTTP + 轮询或 SSE 流。

### 丢弃本体时什么会出问题

> **【中文解读】** 丢掉本体的代价是语义漂移：两个 Agent 对同一个词（"customer"）有微妙不同的概念，接收方按错误理解行动，而 schema 验证器抓不住。FIPA 的本体要求会在解析时就拒绝这类消息。缓解三件套：`content` 上加 JSON Schema、类型化工件（A2A）、信封里显式施事行为。

没有共享本体，Agent 从自然语言内容推断含义。记录在案的 2026 年失败模式是**语义漂移**（semantic drift）：两个 Agent 使用相同的词（`"customer"`）表示微妙不同的概念，接收方的 Agent 基于错误的解释行动，没有模式验证器捕获它。FIPA 的本体要求会在解析时就拒绝该消息。

不走完整本体的缓解措施：

- `content` 上的 JSON Schema——在线路层面拒绝结构性错误。
- 类型化产物（A2A）——拒绝错误的模态。
- 信封中的显式施事行为——即使内容是自然语言，也使意图明确。

### 2026 年规范，映射到言语行为遗产

| 现代规范 | FIPA 类似物 | 保留的 | 丢弃的 |
|---|---|---|---|
| MCP `tools/call` | `request` | 显式意图、关联 ID | 形式语义、本体 |
| MCP `resources/read` | `query-ref` | 显式意图、关联 ID | 形式语义 |
| A2A 任务生命周期 | 合同网 + 条件请求 | 异步生命周期、状态转换 | 形式完整性保证 |
| A2A 流式事件 | 订阅/通知 | 异步推送 | 类型化谓词订阅 |
| CA-MCP 共享上下文 | 黑板（Hayes-Roth 1985） | 多写入器共享内存 | 逻辑一致性模型 |
| NLIP | 自然语言内容 | LLM 原生 | 模式 |

从上到下阅读表格，模式是：保留结构性原语，丢弃形式主义，让 LLM 填补歧义。

> **【中文解读】** 一句话总结全表：2026 规范保留的是结构性原语（显式意图、关联 id、异步生命周期），丢弃的是形式主义（形式语义、本体、逻辑一致性），用 LLM 的解释能力填补歧义。这是"廉价互操作换证明能力"的明确交换。

```figure
sw-contract-net
```

## 动手实现

> **【中文解读】** 示例代码是一个纯标准库的 FIPA-ACL 翻译器：把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来，并跑一个"一个管理者 + 三个投标者"的玩具合同网协商。输出并排展示同一消息的 2026 JSON 形态和 FIPA-ACL 形态——同一些协议原语在往返中存活，只有语法不同。

`code/main.py` 实现了一个纯标准库的 FIPA-ACL 翻译器。它编码和解码规范的 ACL 信封，并展示每个 MCP / A2A 消息形状如何简化为相同的七个字段。演示：

- 将五个 MCP 风格和 A2A 风格的消息编码为 FIPA-ACL。
- 将 FIPA-ACL 解码回现代等效形式。
- 使用 `cfp`、`propose`、`accept-proposal`、`reject-proposal` 在一个管理者和三个竞标者之间运行一个玩具合同网协商。

运行：

```
python3 code/main.py
```

输出是一个并排追踪，显示每条现代消息的 2026 JSON 形式和 FIPA-ACL 形式，然后是合同网竞标的往返。相同的协议原语在往返中存活；只有语法不同。

## 用框架实现

`outputs/skill-fipa-mapper.md` 是一个技能，读取任何 Agent 协议规范并生成 FIPA-ACL 映射。在采用新协议之前使用它来回答："这是真正的新东西，还是带 JSON 语法的 `inform`？"

## 产出物

> **【中文解读】** 不要复活 FIPA-ACL，要带回它的检查清单：意图原语、关联 id、显式内容语言、一等公民的交互协议、语义漂移预案。任何新协议上生产前，先答完这五个问题。

不要把 FIPA-ACL 带回来。带回它的检查清单：

- 每条消息的意图原语（施事行为）是什么？
- 是否有用于请求-响应和取消的关联 ID？
- 是否有显式的内容语言（JSON-RPC、纯文本、结构化类型产物）？
- 交互协议是一等公民，还是你在从头重新实现合同网？
- 当两个 Agent 就内容含义发生分歧时会发生什么（语义漂移）？

在任何新协议投入生产之前，为它记录这五个问题。

## 练习题

1. 运行 `code/main.py`。观察往返编码。识别哪个 FIPA 施事行为对应 `tools/call`、`resources/read` 和 A2A 任务创建。
2. 用 `cancel` 施事行为扩展合同网演示，允许管理者在竞标中途撤回任务。`cancel` 解决了什么重试本身不能解决的失败案例？
3. 阅读 FIPA ACL 消息结构（http://www.fipa.org/specs/fipa00037/）第 4.1-4.3 节。选择本课未涉及的一个施事行为并描述其现代 JSON-RPC 类似物。
4. 阅读 Liu 等人，arXiv:2505.02279。对于 MCP、A2A、ACP、ANP 中的每一个，列出它们保留和丢弃的 FIPA 施事行为族。
5. 为你自己系统中的 `request` 施事行为的 `content` 字段设计一个最小的 JSON Schema。该模式给你什么纯自然语言不能给的，代价是什么？

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Speech act（言语行为） | "做某事的话语" | Austin/Searle：话语即行动。ACL 的理论基础。 |
| FIPA | "那个旧的 XML 东西" | IEEE 智能物理代理基金会。2000 年标准化了 ACL。 |
| ACL | "Agent 通信语言" | FIPA 的信封格式：施事行为 + 内容 + 元数据。 |
| Performative（施事行为） | "动词" | 消息的意图类别：`inform`、`request`、`propose`、`cfp` 等。 |
| KQML | "FIPA 的前身" | 知识查询和操作语言（1993）。更简单，更窄。 |
| Ontology（本体） | "共享词汇" | 内容语言讨论的概念的形式定义。 |
| SL0 / SL1 | "FIPA 内容语言" | 语义语言级别 0 和 1——形式内容语言族。 |
| Contract Net（合同网） | "任务市场" | 管理者发出 cfp；竞标者提议；管理者接受。规范的交互协议。 |
| Interaction protocol（交互协议） | "消息模式" | 具有已知正确性的施事行为序列：条件请求、订阅-通知等。 |

## 延伸阅读

- [Liu 等人 — Agent 互操作性协议调查：MCP、ACP、A2A、ANP](https://arxiv.org/html/2505.02279v1) — 将现代规范连接到 FIPA 遗产的经典 2025 调查
- [FIPA ACL 消息结构规范 (fipa00037)](http://www.fipa.org/specs/fipa00037/) — 批准的 2000 年信封格式
- [FIPA 通信行为库规范 (fipa00037)](http://www.fipa.org/specs/fipa00037/) — 完整的施事行为目录
- [MCP 规范 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) — `request`/`query-ref` 的当前无状态工具使用等效
- [A2A 规范](https://a2a-protocol.org/latest/specification/) — 合同网和订阅-通知的现代 Agent 对等效
