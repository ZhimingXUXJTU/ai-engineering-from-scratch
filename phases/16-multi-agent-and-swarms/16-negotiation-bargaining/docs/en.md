# Negotiation and Bargaining | 协商 讨价还价

> Agents negotiate resources, prices, task allocations, and terms. The 2026 benchmark set is clear: NegotiationArena (arXiv:2402.05863) shows LLMs can improve payoffs ~20% via persona manipulation ("desperation"); "Measuring Bargaining Abilities" (arXiv:2402.15813) shows buyer is harder than seller and scale does not help — their **OG-Narrator** (deterministic offer generator + LLM narrator) pushed deal rate from 26.67% to 88.88%; the Large-Scale Autonomous Negotiation Competition (arXiv:2503.06416) ran ~180k negotiations and found that **chain-of-thought-concealing** agents win by hiding reasoning from counterparts; Bhattacharya et al. 2025 on Harvard Negotiation Project metrics ranked Llama-3 most-effective, Claude-3 aggressive, GPT-4 fairest. This lesson implements Contract Net Protocol (the FIPA ancestor, Lesson 02), wires an LLM-style buyer/seller, runs an OG-Narrator-style decomposition, and measures how deal rate changes with each structural choice.

> **【中文解读】** 本节介绍了协商和讨价还价——多 Agent 在资源分配和任务分配中的协商策略。

> **【拓展：negotiation bargaining→具体应用】** 协商和讨价还价是多 Agent 资源分配的核心机制。三种协商策略：(1) 合作型——Agent 追求整体利益最大化；(2) 竞争型——Agent 追求自身利益最大化；(3) 混合型——兼顾个体和整体。在 Agent 经济中，协商通常通过结构化的提议-响应协议实现，类似于合同网协议（Contract Net Protocol）。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Two agents need to agree on a price. Left to themselves with pure language prompts, 2024-2026 LLMs close deals at surprisingly low rates (~27% on tightly-parameterized bargains in arXiv:2402.15813). Scale does not fix it: GPT-4 is not structurally better at bargaining than GPT-3.5; it is better at the *language* of bargaining.

> 两个 Agent 需要就价格达成一致。在纯语言提示下，2024-2026 年的 LLM 成交率惊人地低（在 arXiv:2402.15813 的紧密参数化议价中约 27%）。规模化并不能解决：GPT-4 在议价结构上并不比 GPT-3.5 好；它只是在议价的*语言*上更好。

The root issue is that LLMs conflate two jobs — deciding the offer and narrating the offer. OG-Narrator separated these: a deterministic offer generator computes numeric moves; the LLM only narrates. Deal rate jumps to ~89%.

> 根本问题是 LLM 混淆了两个任务——决定报价和叙述报价。OG-Narrator 将两者分离：确定性报价生成器计算数字变动；LLM 只负责叙述。成交率跃升至约 89%。

This mirrors a classical multi-agent finding: decoupling the mechanism from the communication layer wins. Contract Net Protocol (FIPA, 1996; Smith, 1980) is the reference task-market mechanism. Plug an LLM into the narration slot and you get a modern LLM-powered task market.

> 这反映了一个经典的多 Agent 发现：将机制与通信层解耦是制胜之道。合同网协议（FIPA，1996；Smith，1980）是参考的任务市场机制。将 LLM 插入叙述槽位，你就得到了一个现代 LLM 驱动的任务市场。

## Concept | 核心概念

### Contract Net, in one paragraph

Smith's 1980 Contract Net Protocol: a **manager** broadcasts a **call for proposals (cfp)**; **bidders** respond with **propose** messages containing their offers; the manager picks a winner and sends **accept-proposal** to the winner and **reject-proposal** to the losers. The winner performs the work. Optional message: **refuse** (bidder declines to propose). FIPA codified this as `fipa-contract-net` interaction protocol.

> Smith 1980 年的合同网协议：**管理者**广播**提案请求（cfp）**；**投标人**回复包含其报价的**提案**消息；管理者选择获胜者并向获胜者发送**接受提案**，向落选者发送**拒绝提案**。获胜者执行工作。可选消息：**拒绝**（投标人拒绝提案）。FIPA 将其编码为 `fipa-contract-net` 交互协议。

### Why OG-Narrator wins

"Measuring Bargaining Abilities of Language Models" (arXiv:2402.15813) observed that:

> "衡量语言模型的议价能力"（arXiv:2402.15813）观察到：

- LLMs often break the bargaining rules (offer at nonsensical prices, ignore the other side's ZOPA).
  中文翻译：LLM 经常违反议价规则（以无意义的价格报价，忽略对方的 ZOPA）。
- They anchor poorly (accept bad first offers; counter-offer at symbolic rather than strategic amounts).
  中文翻译：锚定效果差（接受糟糕的首轮报价；以象征性而非战略性的金额还价）。
- Scale alone does not fix these. Larger models make more-plausible language with similar strategic error.
  中文翻译：仅靠规模化不能解决这些问题。更大的模型产生更合理的语言但有类似的策略错误。

The OG-Narrator decomposition:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

The offer generator is a classical negotiation strategy: a Rubinstein bargaining model, a Zeuthen strategy, or a simple tit-for-tat over price. The LLM narrates. The message contains the deterministic price and the natural-language framing.

Deal rate jumps because:
- Prices stay in the bargaining zone.
- Anchors are strategic, not emotional.
- The LLM does what it is good at: writing.

> 成交率跃升因为：
> - 价格保持在议价区间内。
> - 锚点是战略性的，而非情绪化的。
> - LLM 做它擅长的事：写作。

### NegotiationArena findings

arXiv:2402.05863 provides the canonical benchmark. Headline findings:

> arXiv:2402.05863 提供了规范基准。主要发现：

- LLMs can improve payoffs ~20% by adopting personas ("I am desperate to sell this by Friday") — persona manipulation is a real tactic.
  中文翻译：LLM 可以通过采用人格来提高收益约 20%（"我急需在本周五前卖掉这个"）——人格操纵是一种真实策略。
- Fair/cooperative agents are exploited by adversarial ones; defense requires explicit counter-posturing.
  中文翻译：公平/合作的 Agent 被对抗性 Agent 利用；防御需要显式的反向姿态。
- Symmetric pair-ups converge to inequitable outcomes on about 40% of the benchmark scenarios.
  中文翻译：对称配对在约 40% 的基准场景上收敛到不公平的结果。

This is not "LLMs are bad negotiators." It is "LLMs negotiate too much like humans, including the exploitable parts."

> 这不是"LLM 是糟糕的谈判者"。而是"LLM 的谈判方式太像人类了，包括可被利用的部分"。

### Chain-of-thought concealment

The Large-Scale Autonomous Negotiation Competition (arXiv:2503.06416) ran ~180k negotiations across many LLM strategies. Winners concealed their reasoning from counterparts:

> 大规模自主协商竞赛（arXiv:2503.06416）在许多 LLM 策略上进行了约 18 万次协商。获胜者对对手隐藏了推理过程：

- If an agent prints "I will only go to $75; my reservation price is $70" into a publicly visible scratchpad, the opponent reads it.
  中文翻译：如果 Agent 将"我只出到 $75；我的保留价是 $70"打印到公开可见的草稿本上，对手会读取它。
- Winners compute strategy privately; the output channel contains only the offer and minimum required narration.
  中文翻译：获胜者私下计算策略；输出通道只包含报价和最低限度的叙述。

This is a 2026 echo of classical game theory (Aumann 1976 on rationality and information): revealing your private valuation costs payoff. LLMs do not intuit this and happily type their reservations in reasoning traces that become visible to the counterpart.

> 这是经典博弈论（Aumann 1976 关于理性和信息）在 2026 年的回响：透露私人估值会损失收益。LLM 不会直觉地意识到这一点，乐意在推理痕迹中输入保留价，这些痕迹对对手可见。

Engineering takeaway: separate private-scratchpad context from public-message context. Not optional.

> 工程要点：将私人草稿本上下文与公开消息上下文分离。这不是可选的。

### Bhattacharya et al. 2025 — model rankings

On Harvard Negotiation Project metrics (principled negotiation, BATNA respect, interest reciprocity):

> 在哈佛谈判项目指标上（原则性谈判、BATNA 尊重、利益互惠）：

- **Llama-3** was most-effective at striking bargains (deal rate + payoff).
  中文翻译：**Llama-3** 在达成交易方面最有效（成交率 + 收益）。
- **Claude-3** was the most-aggressive negotiator (high anchors, late concessions).
  中文翻译：**Claude-3** 是最具攻击性的谈判者（高锚点，晚让步）。
- **GPT-4** was the fairest (smallest variance in payoff across pairings).
  中文翻译：**GPT-4** 最公平（跨配对的收益方差最小）。

This is a 2025 snapshot. The point is not which model wins in April 2026 — it is that different base models have persistent negotiation styles. Heterogeneous ensembles (Lesson 15) include this as a diversity source.

> 这是 2025 年的快照。重点不是哪个模型在 2026 年 4 月获胜——而是不同基础模型有持久的谈判风格。异构集成（第 15 课）将此作为多样性来源。

### Task allocation via Contract Net + LLM

The modern re-use of Contract Net for LLM multi-agent:

> 合同网在现代 LLM 多 Agent 中的重用：

1. Manager agent decomposes a task into units.
   中文翻译：管理者 Agent 将任务分解为单元。
2. Broadcasts `cfp` with task description to worker agents.
   中文翻译：向工作者 Agent 广播带任务描述的 `cfp`。
3. Each worker returns an offer: `(price, eta, confidence)` where price could be tokens, compute units, or dollars.
   中文翻译：每个工作者返回一个报价：`(price, eta, confidence)`，其中 price 可以是 token、计算单元或美元。
4. Manager picks winners (single or multiple, depending on task) and awards.
   中文翻译：管理者选择获胜者（单个或多个，取决于任务）并授标。
5. Rejected workers are free to bid on other tasks.
   中文翻译：被拒绝的工作者可以竞标其他任务。

This scales well past 100 workers because coordination is broadcast-and-respond, not synchronous chat. Used in production: Microsoft Agent Framework's orchestration patterns, some LangGraph implementations.

> 这可以很好地扩展到 100 个以上的工作者，因为协调是广播-响应模式，而非同步聊天。已在生产中使用：微软 Agent 框架的编排模式，一些 LangGraph 实现。

### LLM-Stakeholders Interactive Negotiation

NeurIPS 2024 (https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) introduces multi-party scorable games with **secret scores** and **minimum-acceptance thresholds**. Each stakeholder has private utilities; the LLM must infer them from messages. This is the generalization of two-party bargaining to N-party coalition formation. Relevant for production task markets with heterogeneous worker capabilities.

> NeurIPS 2024 引入了具有**秘密分数**和**最低接受阈值**的多方可评分博弈。每个利益相关者有私人效用；LLM 必须从消息中推断。这是两方议价到 N 方联盟形成的推广。适用于具有异构工作者能力的生产任务市场。

### The narration-vs-mechanism rule

Across all 2024-2026 negotiation benchmarks, the consistent engineering rule is:

> Let the LLM narrate. Do not let the LLM compute the offer.

> 让 LLM 叙述。不要让 LLM 计算报价。

If the offer needs to be a number (price, ETA, quantity), generate it deterministically from the negotiation state and have the LLM produce the framing. If the offer needs to be a proposal structure (task decomposition, role assignment), let the LLM draft it, but validate it against a schema and constraint-check before sending.

> 如果报价需要是数字（价格、ETA、数量），从协商状态确定性地生成它，让 LLM 产生框架。如果报价需要是提案结构（任务分解、角色分配），让 LLM 起草它，但在发送前根据模式和约束检查验证。

## Build It | 动手构建

`code/main.py` implements:

- `ContractNetManager`, `ContractNetTask`, `Bid` — manager + bidders, broadcast cfp, collect proposals, award.
  中文翻译：`ContractNetManager`、`ContractNetTask`、`Bid` — 管理者 + 投标人，广播 cfp，收集提案，授标。
- `og_narrator_bargain(state, rng)` — OG-Narrator buyer: deterministic Zeuthen-style concession toward the midpoint.
  中文翻译：`og_narrator_bargain` — OG-Narrator 买方：确定性 Zeuthen 风格向中间点让步。
- `seller_response(state, rng)` — deterministic seller counter-offer policy (the structural ground truth for both styles).
  中文翻译：`seller_response` — 确定性卖方还价策略（两种风格的结构性基准）。
- `naive_llm_bargain(state, rng)` — simulates an all-LLM bargainer: picks prices with high variance, often outside the ZOPA.
  中文翻译：`naive_llm_bargain` — 模拟全 LLM 议价者：以高方差选价，经常超出 ZOPA。
- Measurement: deal rate over 1000 trials with fresh reservation prices sampled per trial.
  中文翻译：测量：1000 次试验的成交率，每次试验重新采样保留价。

Run:

```
python3 code/main.py
```

Expected output: naive-LLM deal rate ~65-75%; OG-Narrator deal rate ~85-95%; the 15-25 point gap is the structural advantage of decomposing offer-generation from narration. Plus a Contract Net task-market allocation example with three bidders and one task.

> 预期输出：朴素 LLM 成交率约 65-75%；OG-Narrator 成交率约 85-95%；15-25 个百分点的差距是将报价生成与叙述解耦的结构性优势。加上一个三个投标人和一个任务的合同网任务市场分配示例。

## Use It | 使用方法

`outputs/skill-bargainer-designer.md` designs a bargaining protocol: who generates offers (deterministic or LLM), who narrates, how private scratchpads separate from public messages, and how deal rate is monitored.

> `outputs/skill-bargainer-designer.md` 设计一个议价协议：谁生成报价（确定性或 LLM），谁叙述，私人草稿本如何与公开消息分离，以及如何监控成交率。

## Ship It | 部署上线

Production bargaining checklist:

- **Separate scratchpad.** Private state never reaches the counterpart's context. This is non-negotiable.
  中文翻译：**分离草稿本。** 私人状态永远不会到达对手的上下文。这是不可协商的。
- **Deterministic offer generation.** Prices, quantities, ETAs: compute, do not prompt.
  中文翻译：**确定性报价生成。** 价格、数量、ETA：计算，不要提示。
- **Validate all incoming offers** against a schema. Reject out-of-ZOPA offers at the protocol boundary.
  中文翻译：**验证所有传入报价**根据模式。在协议边界拒绝 ZOPA 外的报价。
- **Bound rounds.** 3-5 rounds maximum; escalate to mediator on deadlock.
  中文翻译：**限制轮次。** 最多 3-5 轮；死锁时升级到调解者。
- **Measure deal rate and payoff variance** continuously. A falling deal rate is a symptom — often a prompt drift or a counterpart-side attack.
  中文翻译：**持续测量成交率和收益方差。** 下降的成交率是症状——通常是提示漂移或对手方攻击。
- **Log all rejected proposals** with the deterministic rationale. For Contract Net managers, losing bidders need to understand why.
  中文翻译：**记录所有被拒绝的提案**及确定性理由。对于合同网管理者，落选投标人需要理解原因。

## Exercises | 练习题

1. Run `code/main.py`. Confirm OG-Narrator beats naive-LLM on deal rate. By how much?
   中文翻译：运行 `code/main.py`。确认 OG-Narrator 在成交率上优于朴素 LLM。优势多少？
2. Implement **persona-based payoff improvement** (arXiv:2402.05863) — the buyer adopts a "desperate to buy this week" persona in the narration only, offer generator unchanged. Does the deal rate or payoff change?
   中文翻译：实现**基于人格的收益改进**（arXiv:2402.05863）——买方仅在叙述中采用"本周急需购买"的人格，报价生成器不变。成交率或收益有变化吗？
3. Implement chain-of-thought **concealment**: maintain a private scratchpad string that is not passed to the counterpart. What happens if you accidentally leak it (simulate by swapping the channels)?
   中文翻译：实现思维链**隐藏**：维护一个不传递给对手的私人草稿本字符串。如果不小心泄露（通过交换通道模拟）会发生什么？
4. Extend Contract Net to N-bidder auction with reserve price. When bids all exceed reserve, how does the manager decide between lowest-price and highest-quality? Which award rule do you pick and why?
   中文翻译：将合同网扩展为带保留价的 N 投标人拍卖。当所有投标都超过保留价时，管理者如何在最低价格和最高质量之间选择？你选择哪个授标规则，为什么？
5. Read Bhattacharya et al. 2025 on Harvard Negotiation Project metrics. Implement two bargainers with different styles (aggressive vs fair). Measure payoff variance under symmetric and asymmetric pairings.
   中文翻译：阅读 Bhattacharya 等人 2025 年关于哈佛谈判项目指标的论文。实现两个不同风格的议价者（攻击性 vs 公平）。测量对称和非对称配对下的收益方差。

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Further Reading | 延伸阅读

- [NegotiationArena](https://arxiv.org/abs/2402.05863) — the benchmark; persona manipulation and exploitation findings
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) — OG-Narrator and the buyer-harder-than-seller result
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) — ~180k negotiations; chain-of-thought concealment wins
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) — multi-party scorable games with secret utilities
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) — the classical mechanism, IEEE Transactions on Computers
