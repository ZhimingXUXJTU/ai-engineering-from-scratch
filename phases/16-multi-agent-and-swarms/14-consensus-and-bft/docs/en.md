# Consensus and Byzantine Fault Tolerance for Agents | 共识 Agent

> Classical distributed-systems BFT meets stochastic LLMs. In 2025-2026 three research directions emerged: **CP-WBFT** (arXiv:2511.10400) weighs each vote by a confidence probe; **DecentLLMs** (arXiv:2507.14928) goes leaderless with parallel worker proposals and geometric-median aggregation; **WBFT** (arXiv:2505.05103) combines weighted voting with Hierarchical Structure Clustering to split Core and Edge nodes. The honest empirical result from "Can AI Agents Agree?" (arXiv:2603.01213) is that even scalar agreement is fragile today — a single deceptive agent can compromise a Mixture-of-Agents. BFT is necessary but not sufficient. This lesson builds a minimal BFT protocol, injects three agent-specific attacks (byzantine lie, sycophantic conformity, correlated-error monoculture), and measures how each consensus variant copes.

> **【中文解读】** 本节介绍了共识和拜占庭容错——多 Agent 在可能存在故障或恶意行为时如何达成一致。

> **【拓展：consensus and bft→具体应用】** 拜占庭容错（BFT）在多 Agent 系统中的应用：当部分 Agent 可能故障或被攻击时，如何确保系统整体正确？经典 BFT 算法（PBFT）需要 3f+1 个节点容忍 f 个故障节点。在 LLM Agent 上下文中，'故障'可以是幻觉、被注入或拒绝执行。实践中使用多数投票作为简化的 BFT。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

You have N LLM agents each producing an answer. They disagree. Majority vote picks the wrong one because two agents are correlated (same base model, same training data, same failure modes). A third agent happens to be wrong in a novel way — so the majority is a false majority.

> 你有 N 个 LLM Agent，每个都产生一个答案。它们不一致。多数投票选出了错误的答案，因为两个 Agent 是相关的（相同的基础模型、相同的训练数据、相同的失败模式）。第三个 Agent 恰好以一种新颖的方式出错——因此多数是虚假多数。

Now add a deceptive agent: it lies on purpose. Or a sycophantic agent: it agrees with whoever spoke last. In classical BFT, the assumption is that Byzantine nodes are a fraction `f < n/3` and behave arbitrarily. The 2026 reality is that LLM nodes are stochastic even when honest, correlated across models, and influenced by each other's outputs. You cannot treat them as independent Bernoulli voters.

> 现在加入一个欺骗性 Agent：它故意撒谎。或者一个谄媚性 Agent：它同意最后一个发言者的意见。在经典 BFT 中，假设拜占庭节点占比 `f < n/3` 并且行为任意。2026 年的现实是，LLM 节点即使诚实也是随机的，跨模型相关，并受彼此输出的影响。你不能将它们视为独立的伯努利投票者。

Classical BFT (PBFT, 1999) is not wrong — it is incomplete. It handles arbitrary bit-flipping. It does not handle "three honest agents share a hallucination because they share training data." This lesson builds from PBFT's foundation and layers on three 2025-2026 adaptations.

> 经典 BFT（PBFT，1999）并非错误——它是不完整的。它处理任意的位翻转。但它不处理"三个诚实 Agent 因为共享训练数据而产生相同的幻觉"。本课程从 PBFT 的基础出发，叠加三个 2025-2026 年的改进。

## Concept | 核心概念

### What classical BFT gives you

Practical Byzantine Fault Tolerance (Castro & Liskov, OSDI 1999) tolerates `f < n/3` Byzantine nodes. The protocol has three phases (pre-prepare, prepare, commit) and two primitives (signed messages, quorum certificates). Agreement on a single value among `n >= 3f + 1` honest-or-malicious nodes.

> 实用拜占庭容错（Castro & Liskov, OSDI 1999）容忍 `f < n/3` 个拜占庭节点。协议有三个阶段（预准备、准备、提交）和两个原语（签名消息、仲裁证书）。在 `n >= 3f + 1` 个诚实或恶意节点之间就单一值达成一致。

The guarantees are strong but assume:

> 这些保证很强，但假设：

1. **Independent faults.** Byzantines do not coordinate.
   中文翻译：**独立故障。** 拜占庭节点不协调。
2. **Honest nodes are truly honest.** Correctness of honest outputs is a non-issue; the protocol only aligns disagreement.
   中文翻译：**诚实节点真正诚实。** 诚实输出的正确性不是问题；协议只处理分歧。
3. **The question has a ground-truth answer.** Consensus on a wrong fact is still consensus.
   中文翻译：**问题有标准答案。** 对错误事实的共识仍然是共识。

LLM agents violate all three. Two agents running the same base model share faults. An "honest" LLM still hallucinates. And on ambiguous questions, the "truth" is what the agents decide — there is no external oracle.

> LLM Agent 违反了所有三个假设。运行相同基础模型的两个 Agent 共享故障。"诚实的" LLM 仍然会产生幻觉。在模糊的问题上，"真相"由 Agent 决定——没有外部预言机。

### The three LLM-specific attacks

**Byzantine lie.** One agent outputs a deliberately wrong answer. Classical BFT handles this if `f < n/3`.

> **拜占庭撒谎。** 一个 Agent 输出故意错误的答案。如果 `f < n/3`，经典 BFT 可以处理。

**Sycophantic conformity.** One agent reads others' answers before voting and aligns with whoever spoke last. Not malicious, but correlates with the loudest voice. Classical BFT does not prevent this because the agent passes every signature check.

> **谄媚从众。** 一个 Agent 在投票前阅读其他 Agent 的答案，并与最后一个发言者保持一致。不是恶意的，但与最大的声音相关。经典 BFT 无法防止这种情况，因为该 Agent 通过了所有签名检查。

**Correlated-error monoculture.** Three agents share a base model. They hallucinate the same wrong answer. The majority is wrong. Classical BFT does not help because all three "honestly" agree.

> **相关错误单一文化。** 三个 Agent 共享一个基础模型。它们产生相同的错误幻觉。多数是错误的。经典 BFT 无济于事，因为三个 Agent 都"诚实地"达成一致。

### The 2025-2026 responses

**CP-WBFT** (arXiv:2511.10400) — Confidence-Probed Weighted BFT. Each voter attaches a confidence probe to its answer (a self-reported probability, or a separate calibration model's prediction). Vote weights scale with confidence. Reported +85.71% BFT improvement on complete graphs. Mitigation for: sycophantic conformity (conforming agents tend to have low confidence on their volunteered position).

> **CP-WBFT**（arXiv:2511.10400）——置信度探测加权 BFT。每个投票者为其答案附加一个置信度探测（自报概率，或单独校准模型的预测）。投票权重随置信度缩放。报告在完全图上有 +85.71% 的 BFT 改进。针对谄媚从众的缓解措施（从众 Agent 倾向于对自己自愿提出的立场置信度较低）。

**DecentLLMs** (arXiv:2507.14928) — Leaderless. Worker agents propose in parallel, evaluator agents score proposals, final answer is the geometric median of scored positions. Robust when `f < n/2`. Mitigation for: Byzantine lie and correlated errors (geometric median is robust to outliers and pulls toward the dense cluster, not the model-biased average).

> **DecentLLMs**（arXiv:2507.14928）——无领导者。工作 Agent 并行提出方案，评估 Agent 对方案评分，最终答案是评分位置的几何中位数。当 `f < n/2` 时稳健。针对拜占庭撒谎和相关错误的缓解措施（几何中位数对异常值稳健，趋向密集簇而非模型偏差的平均值）。

**WBFT** (arXiv:2505.05103) — Weighted BFT with Hierarchical Structure Clustering. Vote weights are assigned by response quality plus a trust score learned from history. Cluster agents into Core and Edge; Core agents must achieve consensus first, Edge agents follow. Mitigation for: scalability (Core consensus is small and fast) and partially for monoculture (Core can be chosen for diversity).

> **WBFT**（arXiv:2505.05103）——带层次结构聚类的加权 BFT。投票权重由响应质量加上从历史中学习的信任分数分配。将 Agent 聚类为核心和边缘；核心 Agent 必须先达成共识，边缘 Agent 跟随。针对可扩展性的缓解措施（核心共识小而快）和部分针对单一文化的缓解（核心可以选择多样性）。

### Empirical: "Can AI Agents Agree?" (arXiv:2603.01213)

The paper measures scalar agreement (LLM agents agreeing on a single numeric value) across multiple frontier models. The finding is uncomfortable:

> 该论文测量了多个前沿模型上的标量一致性（LLM Agent 就单一数值达成一致）。结果令人不安：

- Even with no adversaries, LLM agents disagree on scalar questions at rates above 30% on many benchmarks.
  中文翻译：即使没有对手，LLM Agent 在许多基准测试上对标量问题的不一致率超过 30%。
- A single agent that adopts a deceptive persona can pull the Mixture-of-Agents consensus 40+ percentage points off the honest baseline.
  中文翻译：采用欺骗人格的单个 Agent 可以将混合 Agent 共识偏离诚实基线 40 个百分点以上。
- Disagreement rates correlate with model diversity — heterogeneous ensembles disagree more than homogeneous ones (good: uncorrelated errors) but also drift more slowly (bad: longer time-to-agreement).
  中文翻译：不一致率与模型多样性相关——异构集成比同构集成不一致更多（好：不相关错误），但漂移更慢（坏：更长的一致达成时间）。

The takeaway: BFT gives you machinery to align outputs, but it does not tell you whether the aligned output is right. Combine with verification (Phase 16 · 08 role specialization), diversity (Phase 16 · 15 debate variants), and evaluator agents (Phase 16 · 24 benchmarks).

> 结论：BFT 提供了输出对齐的机制，但不告诉你对齐的输出是否正确。需要结合验证（Phase 16 · 08 角色专业化）、多样性（Phase 16 · 15 辩论变体）和评估 Agent（Phase 16 · 24 基准测试）。

### The core protocol, stripped down

A minimal BFT round for LLM agents:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

The semantic clustering step is the LLM-specific twist. Two answers "the study reports 4.2%" and "4.2% improvement" are the same cluster. A naive string-equality check would miss this. In production, use a cheap embedding model or explicit canonicalization.

> 语义聚类步骤是 LLM 特有的创新。两个答案"研究报告 4.2%"和"4.2% 的改进"是同一个簇。朴素的字符串相等检查会遗漏这一点。在生产中，使用廉价的嵌入模型或显式规范化。

### Threshold tuning

The `threshold` parameter decides when to accept and when to retry. Too low: you accept weak majorities. Too high: you never accept anything. Empirical range: 0.5-0.67 for `n=5-7` agents, higher for smaller `n`. Below a threshold, escalate to a human or to a different agent ensemble.

> `threshold` 参数决定何时接受、何时重试。太低：接受弱多数。太高：永远不接受任何东西。经验范围：`n=5-7` 个 Agent 时为 0.5-0.67，较小的 `n` 时更高。低于阈值时，升级给人类或不同的 Agent 集合。

### Where consensus does not help

- **Ambiguous questions.** If the question has no ground truth, consensus is an opinion. Call it that.
  中文翻译：**模糊问题。** 如果问题没有标准答案，共识就是意见。就叫它意见。
- **Compound questions.** "Write code and explain it" — two answers. Vote on each independently.
  中文翻译：**复合问题。** "编写代码并解释"——两个答案。分别独立投票。
- **Adversarial multi-round.** If agents can observe prior rounds and mimic (Du 2023 debate), they start agreeing with each other regardless of truth. Bound the rounds (2-3 typically).
  中文翻译：**对抗性多轮。** 如果 Agent 可以观察前几轮并模仿（Du 2023 辩论），它们会不管真相地互相同意。限制轮次（通常 2-3 轮）。

## Build It | 动手构建

`code/main.py` implements:

- `AgentVoter` — a scripted policy with (answer, confidence).
  中文翻译：`AgentVoter` — 带有（答案，置信度）的脚本策略。
- `MajorityVote` — classical plurality.
  中文翻译：`MajorityVote` — 经典多数投票。
- `CPWBFT` — confidence-weighted voting with semantic clustering.
  中文翻译：`CPWBFT` — 带语义聚类的置信度加权投票。
- `DecentLLMs` — geometric-median aggregation on scored proposals.
  中文翻译：`DecentLLMs` — 评分提案上的几何中位数聚合。
- `Scenario` — runs each aggregator under three attack patterns.
  中文翻译：`Scenario` — 在三种攻击模式下运行每个聚合器。

Attack patterns implemented:

> 实现的攻击模式：

1. `byzantine`: one agent lies with high confidence.
   中文翻译：`byzantine`：一个 Agent 以高置信度撒谎。
2. `sycophancy`: one agent copies the first answer it sees, with matching confidence.
   中文翻译：`sycophancy`：一个 Agent 复制它看到的第一个答案，置信度匹配。
3. `monoculture`: three agents share a wrong answer (correlated error) with moderate confidence.
   中文翻译：`monoculture`：三个 Agent 共享一个错误答案（相关错误），置信度中等。

Run:

```
python3 code/main.py
```

Expected output: a table of (attack, aggregator) -> final answer, with the correct answer highlighted. Plurality fails the monoculture case. CPWBFT's confidence weighting mitigates sycophancy. DecentLLMs' geometric-median pulls toward the honest cluster when monoculture is less than half the population.

> 预期输出：一张（攻击，聚合器）-> 最终答案的表格，正确答案高亮显示。多数投票在单一文化案例中失败。CPWBFT 的置信度加权缓解了谄媚。当单一文化不到一半时，DecentLLMs 的几何中位数趋向诚实簇。

## Use It | 使用方法

`outputs/skill-consensus-designer.md` designs a consensus protocol for a multi-agent ensemble: clustering method, weighting, threshold, and the escalation policy for sub-threshold rounds.

> `outputs/skill-consensus-designer.md` 为多 Agent 集合设计共识协议：聚类方法、权重、阈值，以及低于阈值轮次的升级策略。

## Ship It | 部署上线

Before shipping any consensus mechanism:

- **Attack-test with at least the three patterns** above. Your protocol should fail predictably, not silently.
  中文翻译：**至少用上述三种模式进行攻击测试。** 你的协议应该可预测地失败，而不是静默失败。
- **Log every minority cluster** with provenance. Minority clusters are your early-warning system for correlated errors.
  中文翻译：**记录每个少数派簇**及其来源。少数派簇是你相关错误的早期预警系统。
- **Enforce bounded rounds.** No "keep debating until agreement" — that rewards sycophancy.
  中文翻译：**强制限制轮次。** 不要"一直辩论直到同意"——那会奖励谄媚行为。
- **Separate agreement from correctness.** Consensus output goes to a verifier; verifier is independent of the ensemble.
  中文翻译：**分离一致性和正确性。** 共识输出交给验证器；验证器独立于集合。
- **Monitor the agreement rate.** A sharp rise means conformity bias; a sharp fall means model drift.
  中文翻译：**监控一致率。** 急剧上升意味着从众偏差；急剧下降意味着模型漂移。

## Exercises | 练习题

1. Run `code/main.py`. Confirm plurality fails the monoculture attack but CPWBFT partially mitigates it when the monoculture confidence is below 0.7.
   中文翻译：运行 `code/main.py`。确认多数投票在单一文化攻击中失败，但当单一文化置信度低于 0.7 时 CPWBFT 部分缓解了问题。
2. Add a fourth attack pattern: **silent abstention** — one agent refuses to answer ("I don't know"). How should each aggregator treat abstentions? Implement your choice.
   中文翻译：添加第四种攻击模式：**静默弃权** — 一个 Agent 拒绝回答（"我不知道"）。每个聚合器应该如何处理弃权？实现你的选择。
3. Swap the semantic clustering from string canonicalization to embedding-similarity (use any open-source embedding model). What happens to the sycophancy attack?
   中文翻译：将语义聚类从字符串规范化替换为嵌入相似度（使用任何开源嵌入模型）。谄媚攻击会发生什么？
4. Read CP-WBFT (arXiv:2511.10400). Implement the confidence-probe calibration step (a separate calibration model checks each agent's self-reported confidence). Measure the accuracy gain on the monoculture scenario.
   中文翻译：阅读 CP-WBFT（arXiv:2511.10400）。实现置信度探测校准步骤（单独的校准模型检查每个 Agent 的自报置信度）。测量在单一文化场景上的准确率增益。
5. Read "Can AI Agents Agree?" (arXiv:2603.01213). Reproduce a simplified scalar-agreement experiment: three agents, one scalar question, the deceptive-persona prompt. Does CPWBFT or DecentLLMs catch it?
   中文翻译：阅读"AI Agent 能达成一致吗？"（arXiv:2603.01213）。复现一个简化的标量一致性实验：三个 Agent，一个标量问题，欺骗人格提示。CPWBFT 或 DecentLLMs 能捕获吗？

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Further Reading | 延伸阅读

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) — the foundation
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) — vote weighting by confidence
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) — geometric-median aggregation
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) — Core/Edge split for bounded latency
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) — scalar-agreement fragility and deceptive-persona attack
