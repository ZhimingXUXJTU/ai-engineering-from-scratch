# Heritage of FIPA-ACL and Speech Acts | 遗产 FIPA 行动 ACL

> Before MCP, before A2A, there was FIPA-ACL. In 2000 the IEEE Foundation for Intelligent Physical Agents ratified an agent communication language with twenty performatives, two content languages, and a set of interaction protocols — contract net, subscribe/notify, request-when. It faded from industry because the ontology overhead was too heavy for the web, but the LLM revival of multi-agent systems is quietly reimplementing the same ideas without the formal semantics: JSON contracts stand in for performatives, natural language stands in for ontologies. This lesson reads FIPA-ACL seriously so you can see which 2026 protocol decisions are reinvention, which are novelty, and where the current wave is going to rediscover problems the 2000s already solved.

> **【中文解读】** 本节介绍了 FIPA ACL 遗产——多 Agent 系统通信协议的历史标准和现代演进。


**Type:** Learn
**Languages:** Python (stdlib)
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent)
**Time:** ~60 minutes

## Problem

The 2026 agent-protocol landscape is busy: MCP for tools, A2A for agents, ACP for enterprise audit, ANP for decentralized trust, NLIP for natural-language content, plus CA-MCP and two dozen research proposals. Each spec announces itself as foundational.

The honest read is that most of them are rediscovering a very specific twenty-year-old decision tree. Speech-act theory from Austin (1962) and Searle (1969) gave us "utterances are actions." KQML (1993) turned that into a wire protocol. FIPA-ACL (ratified 2000) produced the reference standardization: twenty performatives, content languages SL0/SL1, interaction protocols for contract-net and subscribe-notify. JADE and JACK were the Java reference platforms. The effort faded around 2010 because the ontology overhead was too heavy and the web was winning.

When you look at MCP's `tools/call`, A2A's task lifecycle, or CA-MCP's shared context store, you are looking at a softer, JSON-native rehash of FIPA decisions. Knowing the heritage tells you two things: which new "innovations" are actually reinventions, and which old failure modes the new specs will rediscover.

> **【中文解读】** 2026 年的 Agent 协议（MCP、A2A、ACP、ANP 等）大多是在重新发现 2000 年 FIPA-ACL 已经解决的设计决策。言语行为理论（Austin 1962、Searle 1969）提出"话语即行动"，KQML（1993）将其变为线协议，FIPA-ACL（2000）形成了参考标准。FIPA 在 2010 年左右衰落，因为本体论开销太重，而 Web 技术栈胜出。了解这段历史可以帮你分辨：哪些"创新"实际上是重新发明，哪些旧的失败模式新规范将重新遭遇。

## Concept

### Speech acts, in one paragraph

Austin noticed that some sentences do not describe the world — they change it. "I promise." "I request." "I declare." He called these performative utterances. Searle formalized five categories: assertive, directive, commissive, expressive, declarative. KQML (Finin et al., 1993) made this operational for software agents: a message is a performative (the action) plus content (what the action is about). FIPA-ACL cleaned up KQML's gaps and standardized around twenty performatives.

> **【中文解读】** 言语行为理论的核心洞察：有些句子不是在描述世界，而是在改变世界。"我承诺"、"我请求"、"我宣告"——这些都是施事话语。Searle 将其分为五类：断言式、指令式、承诺式、表达式、宣告式。KQML 将此概念操作化为软件 Agent 的消息格式：消息 = 施事行为 + 内容。FIPA-ACL 在此基础上标准化了约二十个施事行为。

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
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `cancel` | "Cancel the ongoing X" |
| `failure` | "I tried X and failed" |

The full list is in `fipa00037.pdf` (FIPA ACL Message Structure). The point is not to memorize it — the point is that every one of these corresponds to a primitive an LLM protocol eventually re-adds.

### Canonical FIPA-ACL message

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

### The two legacy platforms

**JADE** (Java Agent DEvelopment framework, 1999–2020s) was the most-used FIPA-compliant runtime. Agents extended a base class, exchanged ACL messages, ran inside containers, and coordinated using "behaviors." The interaction-protocol library shipped with contract-net, subscribe-notify, request-when, and propose-accept.

**JACK** (Agent Oriented Software, commercial) emphasized BDI (Belief-Desire-Intention) reasoning on top of FIPA messages. More formal, less adopted.

Both declined once the web stack ate multi-agent use cases. MCP and A2A are the runtime "containers" of 2026.

> **【中文解读】** JADE（Java Agent DEvelopment framework）是最广泛使用的 FIPA 兼容运行时。Agent 通过基类扩展、ACL 消息交换、容器内协调来工作。JACK 在 FIPA 消息之上强调 BDI（信念-欲望-意图）推理。两者都随着 Web 技术栈的胜出而衰落。MCP 和 A2A 可以看作是 2026 年的"容器"。

### Why FIPA faded

- **Ontology overhead.** FIPA required a shared ontology to parse `content`. Agreeing on ontologies is a years-long standards process. The web just used HTTP + JSON.
- **Formal semantics nobody used.** SL (Semantic Language) gave rigorous truth conditions, but most production systems used free-form content and ignored the formalism.
- **Tooling lock-in.** JADE was Java-only; JACK was commercial. Polyglot teams routed around both.
- **The internet won the stack.** REST, then JSON-RPC, then gRPC replaced ACL's transport.

### The LLM revival is FIPA-lite

Compare a FIPA `request` to an MCP `tools/call`:

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

The 2025 survey by Liu et al. ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) makes this lineage explicit: MCP corresponds to tool-use speech acts, A2A to agent-peer speech acts, ACP to audit-trail speech acts, ANP to decentralized-identity extensions. The new specs are ACL descendants with JSON syntax and looser semantics.

> **【中文解读】** LLM 时代是多 Agent 协议实际上是 FIPA-lite：相同的信封（谁、对谁、意图、载荷、关联 ID），不同的语法（JSON 替代 S-expression）。MCP 的 `tools/call` 对应 FIPA 的 `request`，A2A 任务生命周期对应 contract-net + request-when。新规范是 ACL 后裔，用 JSON 语法和更宽松的语义。

### The trade-off, stated plainly

**What FIPA gave you and modern specs drop:**

- Formal semantics — you can prove `inform` implies the sender believes the content.
- A canonical catalog of performatives — you do not have to re-argue "should we have a `cancel`?".
- Decades of interaction-protocol patterns — contract-net, subscribe-notify, propose-accept — with known correctness properties.

**What modern specs give you and FIPA did not:**

- JSON-native payloads compatible with every modern tool.
- Natural-language content that LLMs can interpret without a hand-coded ontology.
- Web-stack transport (HTTP, SSE, WebSocket).
- Capability discovery via self-describing documents (MCP `listTools`, A2A Agent Card).

Looser intent semantics for easier implementation. That is the exact trade.

### Interaction protocols worth porting

FIPA shipped ~15 interaction protocols. Three are worth carrying forward into LLM multi-agent systems:

1. **Contract Net Protocol (CNP).** Manager issues `cfp` (call for proposals); bidders respond with `propose`; manager accepts/rejects. This is the canonical task-market pattern (Phase 16 · 16 Negotiation).
2. **Subscribe/Notify.** Subscriber sends `subscribe`; publisher sends `inform` whenever the topic changes. This is every event-bus in 2026.
3. **Request-When.** "Do X when condition Y holds." Delayed-action with pre-conditions. The 2026 analog is deferred tasks in durable workflow engines (Phase 16 · 22 Production Scaling).

Each maps cleanly onto modern message queues, HTTP + polling, or SSE streaming.

> **【中文解读】** FIPA 的三个值得移植的交互协议：1) **Contract Net Protocol（CNP）**——管理者发出招标，投标人提交提案，管理者接受/拒绝，这是任务市场的经典模式；2) **Subscribe/Notify**——订阅者注册关注，发布者在变化时通知，这是所有现代事件总线的原型；3) **Request-When**——"当条件 Y 满足时执行 X"，带前置条件的延迟动作，对应 2026 年持久化工作流引擎中的延迟任务。

### What breaks when you drop the ontology

Without a shared ontology, agents infer meaning from natural-language content. The documented 2026 failure mode is **semantic drift**: two agents use the same word (`"customer"`) for subtly different concepts, the receiver's agent acts on the wrong interpretation, no schema validator catches it. FIPA's ontology requirement would have rejected the message at parse time.

Mitigations without going full ontology:

- JSON Schema on `content` — rejects structural errors at the wire.
- Typed artifacts (A2A) — rejects wrong modality.
- Explicit performative in the envelope — makes intent unambiguous even when content is natural language.

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

> **【中文解读】** 放弃本体论的代价是**语义漂移**：两个 Agent 用同一个词（如"客户"）表示微妙不同的概念，接收方基于错误理解行动，而没有任何 schema 验证器能捕获。FIPA 的本体论要求会在解析时拒绝这种消息。现代缓解措施包括 JSON Schema 验证、类型化工件（A2A）和信封中显式的施事行为声明。

> **【拓展：FIPA 遗产 → 现代 Agent 协议设计】** 在设计新协议时，FIPA 的清单仍然有用：每条消息的意图原语是什么？是否有请求-响应和取消的关联 ID？是否有显式的内容语言？交互协议是否是一等公民？两个 Agent 对内容含义有分歧时怎么办？在发布到生产之前，用这五个问题检查你的协议。

## Build It | 动手构建

`code/main.py` implements a pure-stdlib FIPA-ACL translator. It encodes and decodes the canonical ACL envelope and shows how every MCP / A2A message shape reduces to the same seven fields. The demo:

- Encodes five MCP-style and A2A-style messages as FIPA-ACL.
- Decodes FIPA-ACL back to the modern equivalent.
- Runs a toy Contract Net negotiation between one manager and three bidders using `cfp`, `propose`, `accept-proposal`, `reject-proposal`.

Run:

```
python3 code/main.py
```

The output is a side-by-side trace showing each modern message in both its 2026 JSON form and its FIPA-ACL form, then a round-trip of a contract-net bid. The same protocol primitives survive the round-trip; only the syntax differs.

## Use It | 使用方法

`outputs/skill-fipa-mapper.md` is a skill that reads any agent-protocol spec and produces the FIPA-ACL mapping. Use it before adopting a new protocol to answer: "Is this genuinely new, or is it `inform` with JSON syntax?"

## Ship It | 部署上线

Do not bring FIPA-ACL back. Bring back its checklist:

- What is the intent primitive (performative) of each message?
- Is there a correlation id for request-response and cancellation?
- Is there an explicit content language (JSON-RPC, plain text, structured typed artifact)?
- Are interaction protocols first-class, or are you re-implementing contract-net from scratch?
- What happens when two agents disagree about content meaning (semantic drift)?

Document these five questions for any new protocol before you ship it into production.

## Exercises | 练习题

1. Run `code/main.py`. Observe the round-trip encoding. Identify which FIPA performative corresponds to `tools/call`, `resources/read`, and A2A task creation.
2. Extend the contract-net demo with a `cancel` performative that lets the manager withdraw the task mid-bid. What failure case does `cancel` solve that retries alone do not?
3. Read FIPA ACL Message Structure (http://www.fipa.org/specs/fipa00037/) sections 4.1–4.3. Pick one performative not covered in this lesson and describe its modern JSON-RPC analog.
4. Read Liu et al., arXiv:2505.02279. For each of MCP, A2A, ACP, ANP, list the FIPA performative families they keep and drop.
5. Design a minimal JSON-Schema for the `content` field of a `request` performative in your own system. What does that schema give you that pure natural-language does not, and what does it cost?

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为：话语即行动，ACL 的理论基础 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | 智能物理 Agent 基金会：2000 年标准化 ACL 的 IEEE 组织 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言：FIPA 的信封格式，包含施事行为+内容+元数据 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为：消息的意图类别，如通知、请求、提议、招标等 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | 知识查询与操作语言：FIPA 的前身（1993） |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体论：内容语言所讨论概念的形式化定义 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | 语义语言级别 0 和 1：FIPA 的形式化内容语言族 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网协议：管理者招标-投标人提案-管理者接受，经典交互协议 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议：具有已知正确性的施事行为序列 |

## Further Reading | 延伸阅读

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) — the canonical 2025 survey connecting modern specs to FIPA heritage
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) — the ratified 2000 envelope format
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) — the full performative catalog
- [MCP specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — the modern tool-use equivalent of `request`/`query-ref`
- [A2A specification](https://a2a-protocol.org/latest/specification/) — the modern agent-peer equivalent of contract-net and subscribe-notify
