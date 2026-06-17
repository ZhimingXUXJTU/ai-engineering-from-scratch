# Agent Economies, Token Incentives, Reputation | 经济

> Long-horizon autonomous agents (METR's 1-hour to 8-hour work-curve) need economic agency. The emerging **5-layer stack** is: **DePIN** (physical compute) → **Identity** (W3C DIDs + reputation capital) → **Cognition** (RAG + MCP) → **Settlement** (account abstraction) → **Governance** (Agentic DAOs). Production agent-incentive networks include **Bittensor** (TAO subnets reward task-specific models), **Fetch.ai / ASI Alliance** (ASI-1 Mini LLM + FET token), and **Gonka** (transformer-based PoW that reallocates compute to productive AI tasks). Academic work: AAMAS 2025's decentralized LaMAS uses **Shapley-value credit attribution** to fairly reward contributing agents; Google Research "Mechanism design for large language models" proposes **token auctions** with second-price payment under monotone aggregation. This lesson builds a minimal agent marketplace, applies Shapley-value credit attribution to a multi-agent pipeline, and runs a second-price token auction so the game-theory machinery lands concretely.

> **【中文解读】** 本节介绍了 Agent 经济——多 Agent 系统中的资源交易、定价和市场机制。

> **【拓展：agent economies→具体应用】** Agent 经济探讨多 Agent 系统中的资源分配和激励机制。核心概念：(1) 代币经济——Agent 使用代币支付服务；(2) 声誉系统——Agent 的服务质量影响其被选择概率；(3) 拍卖机制——资源通过竞价分配。OpenAI 的 x402 支付协议和 MCP 的 scope 模型是 Agent 经济的初步实现。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 16 (Negotiation and Bargaining), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 16（协商与讨价还价），Phase 16 · 09（并行群体网络）

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·16（协商）、Phase 16·09（Swarm）、机制设计基础（Shapley 值、拍卖理论）。Agent 经济 = 多 Agent 系统的市场层。
> 💡 **【类比】** Agent 经济 = "AI 自由市场"。5 层栈：DePIN（算力）+ 身份（DID+声誉）+ 认知（RAG+MCP）+ 结算（账户抽象）+ 治理（Agentic DAO）。Bittensor 子网奖励专门模型，Fetch.ai 用 ASI-1 Mini + FET token，Gonka 用 transformer PoW 把算力导向生产任务。学术：Shapley 值给多 Agent 公平分润、二价 token 拍卖防操纵。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Multi-agent systems get complicated when agents produce value jointly but need to be rewarded individually. Classical mechanisms — equal split, last-contributor-takes-all — are unfair or gameable. Coalition-based rewarding via Shapley values is fair by construction but expensive to compute. The 2025-2026 literature pushes useful approximations: Shapley sampling, monotone aggregation auctions, and on-chain reputation that accrues from confirmed contributions.

> 多 Agent 系统在 Agent 共同产生价值但需要单独奖励时变得复杂。经典机制——平分、最后贡献者全拿——不公平或可被操纵。基于联盟的 Shapley 值奖励在构造上是公平的但计算昂贵。2025-2026 年文献推动了有用的近似：Shapley 采样、单调聚合拍卖和从确认贡献中积累的链上声誉。

Beyond credit attribution, the field has turned to actual economic agents: Bittensor TAO rewards mining compute to fine-tune subnet-specific models, Fetch.ai/ASI rewards ASI-1 Mini LLM usage with FET tokens, Gonka reallocates transformer proof-of-work toward productive AI tasks. Agents that transact autonomously exist today; the question is how to align incentives.

> 超越信用归因，该领域转向了真正的经济 Agent：Bittensor TAO 奖励挖掘计算来微调子网特定模型，Fetch.ai/ASI 用 FET token 奖励 ASI-1 Mini LLM 使用，Gonka 将 transformer 工作量证明重新分配给生产性 AI 任务。自主交易的 Agent 今天已经存在；问题是如何对齐激励。

This lesson treats agent economies as a specific problem family — credit attribution, mechanism design, and reputation — and builds each with the minimal math so the ideas stick.

> 本课将 Agent 经济视为一个特定问题族——信用归因、机制设计和声誉——并用最少的数学构建每一个，使概念真正理解。

## Concept | 核心概念

### The 5-layer agent-economy stack

1. **DePIN (physical compute).** Decentralized infrastructure that rents GPU, storage, bandwidth. Bittensor subnets, Render Network, Akash. Not agent-specific; agents use it.
   中文翻译：**DePIN（物理计算）。** 租赁 GPU、存储、带宽的去中心化基础设施。Bittensor 子网、Render Network、Akash。非 Agent 专用；Agent 使用它。
2. **Identity.** W3C Decentralized Identifiers (DIDs) give each agent a durable ID independent of any platform. Reputation accrues to the DID. The Agent Network Protocol (ANP) uses DID as the discovery layer.
   中文翻译：**身份。** W3C 去中心化标识符（DID）给每个 Agent 一个独立于平台的持久 ID。声誉积累到 DID。Agent 网络协议（ANP）使用 DID 作为发现层。
3. **Cognition.** The agent's reasoning loop: LLM + RAG + MCP. This is what the other phases build.
   中文翻译：**认知。** Agent 的推理循环：LLM + RAG + MCP。这是其他阶段构建的。
4. **Settlement.** Account abstraction (ERC-4337) lets agents pay gas from their own balances without holding ETH. Agents can pay for services, each other, or compute.
   中文翻译：**结算。** 账户抽象（ERC-4337）让 Agent 从自己的余额支付 gas 而无需持有 ETH。Agent 可以支付服务、互相支付或支付计算。
5. **Governance.** Agentic DAOs: governance structures where humans *and* agents vote on protocol changes, with voting power tied to reputation.
   中文翻译：**治理。** Agent DAO：人类*和* Agent 对协议变更投票的治理结构，投票权与声誉绑定。

Not every production system uses all five. Bittensor uses 1, 2, partially 3, partially 4, none of 5. OpenAI agents use none except 3. The stack is a reference map, not a requirement.

### Bittensor, Fetch.ai, Gonka — what runs

**Bittensor (TAO).** Subnets are specialized tasks (language modeling, image generation, forecasting). Miners submit model outputs. Validators rank them; stake-weighted scoring distributes the TAO rewards. Each subnet has its own evaluation. The economic lesson: pay for task-specific output quality, not compute used.

**Fetch.ai / ASI Alliance.** ASI-1 Mini LLM runs on Fetch.ai's network; users pay FET tokens for inference. The agents-as-peers narrative is stronger here: an agent on Fetch can call another for a task and pay in FET.

**Gonka.** Transformer proof-of-work: the "work" is forward passes of a transformer. Miners earn by running inference tasks that have known correct outputs (from training data). Resource-productive PoW instead of hash-based PoW.

All three are production-grade as of April 2026. Payoff distribution differs. Bittensor rewards quality relative to subnet validators; Fetch rewards utility measured by paying users; Gonka rewards verifiable inference work.

### Shapley-value credit attribution

Three agents collaborate on a task. The output scores 0.8. Who contributed what?

Shapley value: the unique credit allocation satisfying four axioms (efficiency, symmetry, linearity, null). For agent `i`:

```
shapley(i) = (1/N!) * sum over all orderings O of (v(S_i_O ∪ {i}) - v(S_i_O))
```

where `S_i_O` is the set of agents before `i` in ordering `O`. In practice: enumerate all permutations, record marginal contribution of each agent in each permutation, average.

For N=3 agents, there are 6 permutations. For N=10, 3.6M — so in practice you sample orderings rather than enumerate.

### Second-price auction for aggregation

Google Research ("Mechanism design for large language models") proposes second-price token auctions for aggregating LLM outputs. Setup: N agents each propose a completion; each has a private value for being selected. The auctioneer picks the highest-value proposal and pays the *second-highest* value. Under monotone aggregation (value depends on which proposal is chosen, not how many were bid), this is truthful — agents bid their true value.

Why this matters for LLM systems: you can outsource completion tasks to multiple agents with different pricing; the auction picks the best + pays fairly, and agents have no incentive to misreport.

### Reputation capital

A DID-bound reputation score accumulates from confirmed contributions. A simple update rule:

```
rep(i, t+1) = alpha * rep(i, t) + (1 - alpha) * contribution_quality(i, t)
```

With decay factor `alpha` close to 1. Reputation:

- Is cheap to read for routing decisions ("send hard tasks to high-rep agents").
- Is expensive to forge (accumulates over time, bound to DID).
- Can be slashed: contributions that fail verification subtract.

### AAMAS 2025 decentralized LaMAS

The LaMAS proposal (AAMAS 2025) combines: DID identity, Shapley-value credit attribution, and a simple auction mechanism. The key claim: decentralizing the credit attribution step makes the system auditable and immune to single-point manipulation.

### Where the economics falls apart

- **Price oracle manipulation.** If the credit function can be gamed, agents will game it. Every mechanism needs an adversarial test.
- **Sybil attacks.** One operator spins up N fake agents to inflate their own contribution. DIDs slow but do not stop this; reputation cost-to-forge is the mitigation.
- **Verification cost.** Credit attribution is only as fair as the verifier. If verification is cheap (small LLM), it can be gamed; if expensive (human panel), the system does not scale.
- **Regulatory overhang.** Agent economies intersect with financial regulation. Bittensor, Fetch, and Gonka all operate in legal gray areas in some jurisdictions as of 2026.

### When agent economies make sense

- **Open networks with heterogeneous operators.** No single team controls all agents.
- **Verifiable outputs.** Without verification, credit attribution is a guess.
- **Long-horizon workflows.** One-shot tasks do not benefit from reputation accumulation.
- **Tokenized payments are legally viable** in your jurisdiction.

In closed corporate systems, economics gives way to simpler allocation (managers assign work, metrics are internal). The economics literature applies mostly to open networks.

## Build It | 动手构建

`code/main.py` implements:

- `shapley(value_fn, agents)` — exact Shapley computation by enumeration for small N.
- `second_price_auction(bids)` — truthful mechanism; winner pays second-highest.
- `Reputation` — DID-bound reputation with exponential decay and slashing.
- Demo 1: three agents collaborate, exact Shapley attributes credit.
- Demo 2: five agents bid for a task slot; second-price auction picks winner + payment.
- Demo 3: 100 rounds of task assignment to agents with heterogeneous rep; rep-weighted routing beats random.

Run:

```
python3 code/main.py
```

Expected output: Shapley values for each agent; auction result showing truthful-bid equilibrium; rep-weighted routing showing 10-20% quality gain over random after warmup.

## Use It | 使用方法

`outputs/skill-economy-designer.md` designs a minimal agent economy: choice of identity layer, credit attribution mechanism, payment mechanism, reputation rule.

## Ship It | 部署上线

Running an agent economy in 2026:

- **Start with reputation, not tokens.** Reputation is cheap to implement and valuable alone; tokens add legal and economic complexity.
  中文翻译：**从声誉开始，不是 token。** 声誉实现廉价且单独就有价值；token 增加法律和经济复杂性。
- **Verify before you reward.** Never distribute credit without an independent verification step. Self-reported quality accrues sybil games.
  中文翻译：**先验证再奖励。** 没有独立验证步骤永远不要分配信用。自报质量会积累女巫博弈。
- **Shapley-sample, not Shapley-exact.** Sample 100-1000 orderings; exact enumeration does not scale.
  中文翻译：**Shapley 采样，而非 Shapley 精确。** 采样 100-1000 个排序；精确枚举不可扩展。
- **Cap decay factor and floor reputation.** Unbounded decay wipes legitimate contributors; too-slow decay rewards stale high-rep agents.
  中文翻译：**限制衰减因子和最低声誉。** 无界衰减抹去合法贡献者；太慢的衰减奖励过时的高声誉 Agent。
- **Audit mechanisms adversarially.** Run red-team scenarios before opening the network. Every mechanism has a game theory; you want to find the holes, not the attackers.
  中文翻译：**对抗性审计机制。** 开放网络前运行红队场景。每个机制都有博弈论；你想找到漏洞，而非攻击者。

## Exercises | 练习题

1. Run `code/main.py`. Confirm Shapley values sum to total value (efficiency axiom). Change the value function; do Shapley allocations change in the expected direction?
2. Implement Shapley *sampling* (Monte Carlo over K orderings). How does K affect approximation accuracy? Compare to exact for N=4.
3. Implement a coalition-forming step before the auction: agents can merge into teams and bid as a unit. Which coalitions form? Is the outcome Pareto-better than individual bidding?
4. Read the Google Research mechanism-design post. Identify one assumption that, if violated, breaks truthfulness. What does that failure mode look like in an LLM setting?
5. Read the AAMAS 2025 decentralized LaMAS paper. Implement their Shapley step over 10 agents on a synthetic task. How long does exact computation take? How close does sampling get with 100 draws?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| DePIN / 去中心化物理基础设施 | "Decentralized physical infrastructure" / "去中心化物理基础设施" | Token-incentivized compute/storage/bandwidth. Bittensor, Akash, Render. / Token 激励的计算/存储/带宽。Bittensor、Akash、Render。 |
| DID / 去中心化标识符 | "Decentralized identifier" / "去中心化标识符" | W3C spec for portable IDs. Agent reputation binds to DID, not to a platform. / W3C 便携 ID 规范。Agent 声誉绑定到 DID，而非平台。 |
| ERC-4337 / 账户抽象 | "Account abstraction" / "账户抽象" | Contract accounts that can sponsor gas, enabling agent payments. / 可以赞助 gas 的合约账户，使 Agent 支付成为可能。 |
| Shapley value / Shapley 值 | "Fair credit attribution" / "公平信用归因" | Unique allocation satisfying efficiency, symmetry, linearity, null. / 满足效率、对称、线性、零贡献者的唯一分配。 |
| Second-price auction / 二价拍卖 | "Vickrey auction" / "Vickrey 拍卖" | Truthful mechanism: winner pays second-highest bid. Monotone aggregation compatible. / 诚实机制：获胜者支付第二高出价。兼容单调聚合。 |
| Reputation capital / 声誉资本 | "Accumulated quality score" / "累积质量分数" | DID-bound score from confirmed contributions; decays over time. / DID 绑定的来自确认贡献的分数；随时间衰减。 |
| Agentic DAO / Agent DAO | "Agents + humans govern" / "Agent + 人类治理" | DAO with agent voters as first-class, voting power tied to reputation. / Agent 投票者作为一等公民的 DAO，投票权与声誉绑定。 |
| TAO / FET / GPU credits / Token 面额 | "Token denominations" / "Token 面额" | Bittensor TAO, Fetch.ai FET, various DePIN tokens. / Bittensor TAO、Fetch.ai FET、各种 DePIN token。 |

## Further Reading | 延伸阅读

- [The Agent Economy](https://arxiv.org/abs/2602.14219) — 2026 survey of the 5-layer agent-economy stack
- [Google Research — Mechanism design for large language models](https://research.google/blog/mechanism-design-for-large-language-models/) — token auctions with monotone aggregation
- [AAMAS 2025 — decentralized LaMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2896.pdf) — Shapley-value credit attribution
- [Bittensor TAO documentation](https://docs.bittensor.com/) — subnet structure and reward distribution
- [Fetch.ai / ASI Alliance](https://fetch.ai/) — ASI-1 Mini LLM and FET token
- [W3C Decentralized Identifiers (DIDs) spec](https://www.w3.org/TR/did-core/) — identity foundation
