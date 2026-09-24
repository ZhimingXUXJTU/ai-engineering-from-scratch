# Heritage of FIPA-ACL and Speech Acts | FIPA-ACL 与言语行为的遗产

> Before MCP, before A2A, there was FIPA-ACL. In 2000 the IEEE Foundation for Intelligent Physical Agents ratified an agent communication language with twenty performatives, two content languages, and a set of interaction protocols — contract net, subscribe/notify, request-when. It faded from industry because the ontology overhead was too heavy for the web, but the LLM revival of multi-agent systems is quietly reimplementing the same ideas without the formal semantics: JSON contracts stand in for performatives, natural language stands in for ontologies. This lesson reads FIPA-ACL seriously so you can see which 2026 protocol decisions are reinvention, which are novelty, and where the current wave is going to rediscover problems the 2000s already solved.

> **【中文解读】** 本课讲 FIPA-ACL 遗产——多 Agent 系统通信协议的历史标准与现代演进。2000 年定型的二十个施事行为（performatives）、内容语言和交互协议，正是 2026 年 MCP/A2A/ACP 们正在重新发明的东西：JSON 契约替代施事行为，自然语言替代本体。读懂这段历史，你才能分辨新协议里哪些是再发明、哪些是真创新。

> **【拓展：FIPA ACL 遗产→具体应用】** FIPA ACL（Foundation for Intelligent Physical Agents Agent Communication Language）是 1990-2000 年代多 Agent 系统的通信标准。虽然 FIPA 组织已于 2013 年解散，但其核心思想（标准化的通信原语如 INFORM、REQUEST、PROPOSE）仍然影响着现代多 Agent 协议。2026 年的 A2A 协议可以看作 FIPA ACL 的 LLM 时代重生。

> 🔗 **【前置】** 学本课前请先掌握：Phase 16·01（为什么需要多 Agent）、Phase 13（MCP/工具协议）。本课是历史课——理解 FIPA ACL 才能看懂 2026 协议（MCP/A2A/ACP）是重新发明还是真创新。

> 💡 **【类比】** FIPA-ACL = "AI 界的拉丁语"。2000 年的标准，2026 年的协议（MCP/A2A）大量继承其思想。区别：FIPA 用形式化本体（重）、现代协议用 JSON+自然语言（轻）。学历史的价值：避免重蹈覆辙——FIPA 因为"本体太重"而死，现代协议要保持轻量。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Problem | 问题引入

> **【中文解读】** 2026 年的 Agent 协议看似百花齐放，实则大多在重走一条二十年前的决策树：言语行为理论（话语即行动）→ KQML 线协议 → FIPA-ACL 标准化 → 因本体太重而被 Web 技术栈淘汰。本节给出判断框架：看新协议时，先问它对应 FIPA 决策树上的哪个节点。

The 2026 agent-protocol landscape is busy: MCP for tools, A2A for agents, ACP for enterprise audit, ANP for decentralized trust, NLIP for natural-language content, plus CA-MCP and two dozen research proposals. Each spec announces itself as foundational.

> 2026 年的 Agent 协议领域很热闹：MCP 用于工具、A2A 用于 Agent、ACP 用于企业审计、ANP 用于去中心化信任、NLIP 用于自然语言内容，还有 CA-MCP 和二十多个研究提案。每个规范都宣称自己是基础性的。

The honest read is that most of them are rediscovering a very specific twenty-year-old decision tree. Speech-act theory from Austin (1962) and Searle (1969) gave us "utterances are actions." KQML (1993) turned that into a wire protocol. FIPA-ACL (ratified 2000) produced the reference standardization: twenty performatives, content languages SL0/SL1, interaction protocols for contract-net and subscribe-notify. JADE and JACK were the Java reference platforms. The effort faded around 2010 because the ontology overhead was too heavy and the web was winning.

> 诚实的看法是，它们中的大多数正在重新发现一个非常具体的二十年前的决策树。Austin（1962）和 Searle（1969）的言语行为理论告诉我们"话语即行动"。KQML（1993）将其转化为线协议。FIPA-ACL（2000 年批准）产生了参考标准化：二十个施事行为、内容语言 SL0/SL1、用于合同网和订阅-通知的交互协议。JADE 和 JACK 是 Java 参考平台。这项努力在 2010 年左右消退，因为本体开销太重，Web 正在获胜。

When you look at MCP's `tools/call`, A2A's task lifecycle, or CA-MCP's shared context store, you are looking at a softer, JSON-native rehash of FIPA decisions. Knowing the heritage tells you two things: which new "innovations" are actually reinventions, and which old failure modes the new specs will rediscover.

> 当你审视 MCP 的 `tools/call`、A2A 的任务生命周期或 CA-MCP 的共享上下文存储时，你看到的是 FIPA 决策的更柔和、JSON 原生的重述。了解这一遗产告诉你两件事：哪些新"创新"实际上是再发明，以及新规范将重新发现哪些旧失败模式。

## Concept | 核心概念

> **【中文解读】** 本节把谱系讲全：言语行为理论（Austin/Searle）→ KQML（1993）→ FIPA-ACL（2000，二十个施事行为 + SL0/SL1 内容语言 + 交互协议）→ JADE/JACK 平台 → 衰落 → LLM 时代以 JSON 语法复活。核心洞察：Agent 通信的语法小而稳定，只有表示方式在变。

### Speech acts, in one paragraph

> **【中文解读】** 一段话讲清理论根基：有些句子不是在描述世界，而是在改变世界（"我承诺""我请求"）。Searle 把它们分成五类；KQML 把这个哲学概念变成了软件可执行的线协议；FIPA-ACL 收尾标准化。所有现代 Agent 协议都是这条链条的后代。

Austin noticed that some sentences do not describe the world — they change it. "I promise." "I request." "I declare." He called these performative utterances. Searle formalized five categories: assertive, directive, commissive, expressive, declarative. KQML (Finin et al., 1993) made this operational for software agents: a message is a performative (the action) plus content (what the action is about). FIPA-ACL cleaned up KQML's gaps and standardized around twenty performatives.

> Austin 注意到有些句子并不描述世界——它们改变世界。"我承诺。""我请求。""我宣布。"他称这些为施事话语。Searle 将其形式化为五个类别：断言类、指令类、承诺类、表达类、宣告类。KQML（Finin 等，1993）将此操作化为软件 Agent 的概念：消息是一个施事行为（动作）加上内容（动作关于什么）。FIPA-ACL 填补了 KQML 的空白并标准化了约二十个施事行为。

### The twenty FIPA performatives (partial list)

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

The full list is in `fipa00037.pdf` (FIPA ACL Message Structure). The point is not to memorize it — the point is that every one of these corresponds to a primitive an LLM protocol eventually re-adds.

> 完整列表在 `fipa00037.pdf`（FIPA ACL 消息结构）中。重点不在于记忆——而在于每一个都对应着一个 LLM 协议最终会重新添加的原语。

### Canonical FIPA-ACL message

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

Seven fields carry the protocol envelope; one field (`content`) carries the payload. The rest of the fields are exactly what you reinvent every time you bolt retries, threading, and ontology onto a JSON protocol.

> 七个字段承载协议信封；一个字段（`content`）承载有效载荷。其余字段正是你每次将重试、线程和本体加到 JSON 协议上时重新发明的。

### The two legacy platforms

**JADE** (Java Agent DEvelopment framework, 1999–2020s) was the most-used FIPA-compliant runtime. Agents extended a base class, exchanged ACL messages, ran inside containers, and coordinated using "behaviors." The interaction-protocol library shipped with contract-net, subscribe-notify, request-when, and propose-accept.

> **JADE**（Java Agent 开发框架，1999-2020 年代）是最常用的 FIPA 兼容运行时。Agent 继承基类，交换 ACL 消息，在容器内运行，并使用"行为"进行协调。交互协议库附带合同网、订阅-通知、请求-当和提议-接受。

**JACK** (Agent Oriented Software, commercial) emphasized BDI (Belief-Desire-Intention) reasoning on top of FIPA messages. More formal, less adopted.

> **JACK**（Agent Oriented Software，商业产品）强调在 FIPA 消息之上进行 BDI（信念-愿望-意图）推理。更正式，采用较少。

Both declined once the web stack ate multi-agent use cases. MCP and A2A are the runtime "containers" of 2026.

> 一旦 Web 技术栈吞噬了多 Agent 用例，两者都衰落了。MCP 和 A2A 是 2026 年的运行时"容器"。

### Why FIPA faded

- **Ontology overhead.** FIPA required a shared ontology to parse `content`. Agreeing on ontologies is a years-long standards process. The web just used HTTP + JSON.
  中文翻译：**本体开销。** FIPA 需要共享本体来解析 `content`。就本体达成一致是一个长达数年的标准化过程。Web 只用了 HTTP + JSON。
- **Formal semantics nobody used.** SL (Semantic Language) gave rigorous truth conditions, but most production systems used free-form content and ignored the formalism.
  中文翻译：**没人用的形式语义。** SL（语义语言）提供了严格的真值条件，但大多数生产系统使用自由格式的内容并忽略了形式主义。
- **Tooling lock-in.** JADE was Java-only; JACK was commercial. Polyglot teams routed around both.
  中文翻译：**工具锁定。** JADE 仅支持 Java；JACK 是商业的。多语言团队绕过了两者。
- **The internet won the stack.** REST, then JSON-RPC, then gRPC replaced ACL's transport.
  中文翻译：**互联网赢得了技术栈。** REST、然后是 JSON-RPC、然后是 gRPC 取代了 ACL 的传输。

### The LLM revival is FIPA-lite

> **【中文解读】** 把 FIPA `request` 和 MCP `tools/call` 并排放：同一个信封（谁、对谁、意图、载荷、关联 id），不同的语法。Liu 等 2025 综述明确给出谱系映射：MCP=工具使用言语行为，A2A=Agent 对等言语行为，ACP=审计轨迹言语行为，ANP=去中心化身份扩展。新规范都是 JSON 语法、更松语义的 ACL 后代。

Compare a FIPA `request` to an MCP `tools/call`:

> 将 FIPA `request` 与 MCP `tools/call` 进行比较：

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

Same envelope, different syntax. Both carry: who, whom, intent, payload, correlation id. Neither is a revolution over the other — they are different trade-offs on the same design.

> 相同的信封，不同的语法。两者都携带：谁、对谁、意图、有效载荷、关联 ID。两者都不是对另一方的革命——它们是同一设计上的不同权衡。

The 2025 survey by Liu et al. ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) makes this lineage explicit: MCP corresponds to tool-use speech acts, A2A to agent-peer speech acts, ACP to audit-trail speech acts, ANP to decentralized-identity extensions. The new specs are ACL descendants with JSON syntax and looser semantics.

> Liu 等人 2025 年的综述（"Agent 互操作性协议综述：MCP, ACP, A2A, ANP"，arXiv:2505.02279）明确指出了这一谱系：MCP 对应工具使用言语行为，A2A 对应 Agent 对等言语行为，ACP 对应审计轨迹言语行为，ANP 对应去中心化身份扩展。新规范是 ACL 的后裔，使用 JSON 语法和更松散的语义。

### The trade-off, stated plainly

> **【中文解读】** 权衡要明说：FIPA 给形式语义（可证明）、规范施事行为目录（不用重争论）、带正确性保证的交互协议模式；现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现。交换的就是"更松散的意图语义换更容易的实现"。

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- Formal semantics — you can prove `inform` implies the sender believes the content.
  中文翻译：形式语义——你可以证明 `inform` 意味着发送者相信该内容。
- A canonical catalog of performatives — you do not have to re-argue "should we have a `cancel`?".
  中文翻译：规范的施事行为目录——你不必重新争论"我们应该有 `cancel` 吗？"。
- Decades of interaction-protocol patterns — contract-net, subscribe-notify, propose-accept — with known correctness properties.
  中文翻译：数十年的交互协议模式——合同网、订阅-通知、提议-接受——具有已知的正确性属性。

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- JSON-native payloads compatible with every modern tool.
  中文翻译：与每个现代工具兼容的 JSON 原生有效载荷。
- Natural-language content that LLMs can interpret without a hand-coded ontology.
  中文翻译：LLM 可以在没有手工编码本体的情况下解释的自然语言内容。
- Web-stack transport (HTTP, SSE, WebSocket).
  中文翻译：Web 技术栈传输（HTTP、SSE、WebSocket）。
- Capability discovery via live MCP `server/discover` and A2A Agent Cards.
  中文翻译：通过实时 MCP `server/discover` 和 A2A Agent Card 进行能力发现。

Looser intent semantics for easier implementation. That is the exact trade.

> 更松散的意图语义以实现更容易的实现。这正是权衡所在。

### Interaction protocols worth porting

> **【中文解读】** FIPA 约 15 个交互协议里，三个值得搬进 LLM 多 Agent 系统：合同网（任务市场模式，对应 Phase 16·16 协商）、订阅/通知（每个事件总线）、请求-当（持久工作流引擎的延迟任务，对应 Phase 16·22）。它们都能干净映射到现代消息队列、HTTP + 轮询或 SSE 流。

FIPA shipped ~15 interaction protocols. Three are worth carrying forward into LLM multi-agent systems:

> FIPA 发布了约 15 个交互协议。其中三个值得延续到 LLM 多 Agent 系统中：

1. **Contract Net Protocol (CNP).** Manager issues `cfp` (call for proposals); bidders respond with `propose`; manager accepts/rejects. This is the canonical task-market pattern (Phase 16 · 16 Negotiation).
   中文翻译：**合同网协议 (CNP)。** 管理者发布 `cfp`（征求提案）；投标者用 `propose` 响应；管理者接受/拒绝。这是典型的任务市场模式（Phase 16 · 16 协商）。
2. **Subscribe/Notify.** Subscriber sends `subscribe`; publisher sends `inform` whenever the topic changes. This is every event-bus in 2026.
   中文翻译：**订阅/通知。** 订阅者发送 `subscribe`；发布者在主题变化时发送 `inform`。这是 2026 年的每个事件总线。
3. **Request-When.** "Do X when condition Y holds." Delayed-action with pre-conditions. The 2026 analog is deferred tasks in durable workflow engines (Phase 16 · 22 Production Scaling).
   中文翻译：**请求-当。** "当条件 Y 成立时执行 X。"带前置条件的延迟动作。2026 年的类似物是持久工作流引擎中的延迟任务（Phase 16 · 22 生产扩展）。

Each maps cleanly onto modern message queues, HTTP + polling, or SSE streaming.

> 每个都可以清晰地映射到现代消息队列、HTTP + 轮询或 SSE 流。

### What breaks when you drop the ontology

> **【中文解读】** 丢掉本体的代价是**语义漂移**：两个 Agent 对同一个词（"customer"）有微妙不同的概念，接收方按错误理解行动，而 schema 验证器抓不住。FIPA 的本体要求会在解析时就拒绝这类消息。缓解三件套：`content` 上加 JSON Schema、类型化工件（A2A）、信封里显式施事行为。

Without a shared ontology, agents infer meaning from natural-language content. The documented 2026 failure mode is **semantic drift**: two agents use the same word (`"customer"`) for subtly different concepts, the receiver's agent acts on the wrong interpretation, no schema validator catches it. FIPA's ontology requirement would have rejected the message at parse time.

> 没有共享本体，Agent 从自然语言内容中推断含义。记录在案的 2026 年失败模式是**语义漂移**：两个 Agent 对同一个词（`"customer"`）有微妙不同的概念，接收方 Agent 基于错误的理解行动，没有模式验证器能捕获它。FIPA 的本体要求会在解析时拒绝该消息。

Mitigations without going full ontology:

> 不完全使用本体的缓解措施：

- JSON Schema on `content` — rejects structural errors at the wire.
  中文翻译：对 `content` 使用 JSON Schema——在传输层拒绝结构性错误。
- Typed artifacts (A2A) — rejects wrong modality.
  中文翻译：类型化工件（A2A）——拒绝错误的模态。
- Explicit performative in the envelope — makes intent unambiguous even when content is natural language.
  中文翻译：信封中显式的施事行为——即使内容是自然语言也使意图明确。

### The 2026 specs, mapped to speech-act heritage

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

Reading the table top to bottom, the pattern is: keep the structural primitive, drop the formalism, let LLMs paper over the ambiguity.

> 从上到下阅读表格，模式是：保留结构原语，丢弃形式主义，让 LLM 弥补模糊性。

> **【中文解读】** 一句话总结全表：2026 规范保留的是结构性原语（显式意图、关联 id、异步生命周期），丢弃的是形式主义（形式语义、本体、逻辑一致性），用 LLM 的解释能力填补歧义。这是"廉价互操作换证明能力"的明确交换。

```figure
sw-contract-net
```

## Build It | 动手实现

> **【中文解读】** 示例代码是一个纯标准库的 FIPA-ACL 翻译器：把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来，并跑一个"一个管理者 + 三个投标者"的玩具合同网协商。输出并排展示同一消息的 2026 JSON 形态和 FIPA-ACL 形态——同一些协议原语在往返中存活，只有语法不同。

`code/main.py` implements a pure-stdlib FIPA-ACL translator. It encodes and decodes the canonical ACL envelope and shows how every MCP / A2A message shape reduces to the same seven fields. The demo:

> `code/main.py` 实现了一个纯标准库的 FIPA-ACL 翻译器。它编解码标准 ACL 信封，并展示每个 MCP / A2A 消息形状如何简化为相同的七个字段。演示内容：

- Encodes five MCP-style and A2A-style messages as FIPA-ACL.
  中文翻译：将五个 MCP 风格和 A2A 风格的消息编码为 FIPA-ACL。
- Decodes FIPA-ACL back to the modern equivalent.
  中文翻译：将 FIPA-ACL 解码回现代等效形式。
- Runs a toy Contract Net negotiation between one manager and three bidders using `cfp`, `propose`, `accept-proposal`, `reject-proposal`.
  中文翻译：使用 `cfp`、`propose`、`accept-proposal`、`reject-proposal` 在一个管理者和三个投标者之间运行一个玩具合同网协商。

Run:

```
python3 code/main.py
```

The output is a side-by-side trace showing each modern message in both its 2026 JSON form and its FIPA-ACL form, then a round-trip of a contract-net bid. The same protocol primitives survive the round-trip; only the syntax differs.

> 输出是一个并排追踪，显示每条现代消息的 2026 JSON 形式和 FIPA-ACL 形式，然后是合同网投标的往返。相同的协议原语在往返中存活；只有语法不同。

## Use It | 用框架实现

`outputs/skill-fipa-mapper.md` is a skill that reads any agent-protocol spec and produces the FIPA-ACL mapping. Use it before adopting a new protocol to answer: "Is this genuinely new, or is it `inform` with JSON syntax?"

> `outputs/skill-fipa-mapper.md` 是一个技能，读取任何 Agent 协议规范并生成 FIPA-ACL 映射。在采用新协议之前使用它来回答："这是真正的新东西，还是带 JSON 语法的 `inform`？"

## Ship It | 产出物

> **【中文解读】** 不要复活 FIPA-ACL，要带回它的检查清单：意图原语、关联 id、显式内容语言、一等公民的交互协议、语义漂移预案。任何新协议上生产前，先答完这五个问题。

Do not bring FIPA-ACL back. Bring back its checklist:

> 不要把 FIPA-ACL 带回来。带回它的检查清单：

- What is the intent primitive (performative) of each message?
  中文翻译：每条消息的意图原语（施事行为）是什么？
- Is there a correlation id for request-response and cancellation?
  中文翻译：是否有用于请求-响应和取消的关联 ID？
- Is there an explicit content language (JSON-RPC, plain text, structured typed artifact)?
  中文翻译：是否有显式的内容语言（JSON-RPC、纯文本、结构化类型工件）？
- Are interaction protocols first-class, or are you re-implementing contract-net from scratch?
  中文翻译：交互协议是一等公民，还是你正在从头重新实现合同网？
- What happens when two agents disagree about content meaning (semantic drift)?
  中文翻译：当两个 Agent 对内容含义有分歧时会发生什么（语义漂移）？

Document these five questions for any new protocol before you ship it into production.

> 在将任何新协议发布到生产环境之前，记录这五个问题。

## Exercises | 练习题

1. Run `code/main.py`. Observe the round-trip encoding. Identify which FIPA performative corresponds to `tools/call`, `resources/read`, and A2A task creation.
   中文翻译：运行 `code/main.py`。观察往返编码。识别哪个 FIPA 施事行为对应 `tools/call`、`resources/read` 和 A2A 任务创建。
2. Extend the contract-net demo with a `cancel` performative that lets the manager withdraw the task mid-bid. What failure case does `cancel` solve that retries alone do not?
   中文翻译：用 `cancel` 施事行为扩展合同网演示，让管理者可以在投标中途撤回任务。`cancel` 解决了仅靠重试无法解决的什么故障情况？
3. Read FIPA ACL Message Structure (http://www.fipa.org/specs/fipa00037/) sections 4.1–4.3. Pick one performative not covered in this lesson and describe its modern JSON-RPC analog.
   中文翻译：阅读 FIPA ACL 消息结构（http://www.fipa.org/specs/fipa00037/）第 4.1-4.3 节。选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC 类比。
4. Read Liu et al., arXiv:2505.02279. For each of MCP, A2A, ACP, ANP, list the FIPA performative families they keep and drop.
   中文翻译：阅读 Liu 等人，arXiv:2505.02279。对于 MCP、A2A、ACP、ANP 中的每一个，列出它们保留和丢弃的 FIPA 施事行为族。
5. Design a minimal JSON-Schema for the `content` field of a `request` performative in your own system. What does that schema give you that pure natural-language does not, and what does it cost?
   中文翻译：为你自己系统中 `request` 施事行为的 `content` 字段设计一个最小的 JSON-Schema。该模式给你提供了纯自然语言没有的什么，代价是什么？

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) — the canonical 2025 survey connecting modern specs to FIPA heritage
  中文翻译：Liu 等人——Agent 互操作性协议综述，连接现代规范与 FIPA 遗产的权威 2025 综述
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) — the ratified 2000 envelope format
  中文翻译：FIPA ACL 消息结构规范——2000 年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) — the full performative catalog
  中文翻译：FIPA 通信行为库规范——完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) — the current stateless tool-use equivalent of `request`/`query-ref`
  中文翻译：MCP 2026-07-28 规范——`request`/`query-ref` 的当前无状态工具使用等效
- [A2A specification](https://a2a-protocol.org/latest/specification/) — the modern agent-peer equivalent of contract-net and subscribe-notify
  中文翻译：A2A 规范——合同网和订阅-通知的现代 Agent 对等效
