# 多 Agent 辩论

> Du et al. (ICML 2024, "Society of Minds") run N model instances that independently propose answers, then iteratively critique each other over R rounds to converge. Improves factuality, rule-following, reasoning. Sparse topology beats full mesh on token cost.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC)
**预计时间：** ~60 minutes

## 学习目标

- Explain the debate protocol: N proposers, R rounds, converge on a shared answer.
- Describe why debate improves factuality, rule-following, and reasoning.
- Explain sparse topology: not every debater needs to see every other.
- Implement a stdlib debate over a scripted LLM with full-mesh and sparse variants; measure token cost vs accuracy.

## 问题引入

> **【中文解读】** 多 Agent 辩论通过让多个 LLM 实例从不同角度讨论同一问题来提高推理质量。核心洞察：单个 LLM 可能自信地给出错误答案，但多个 LLM 辩论时，错误更容易被识别和纠正。这与人类专家小组讨论的原理相似。
> **【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】** 多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个 ChatGPT 实例辩论可以显著提高推理准确率。2026 年的实践表明，3-5 个 Agent 的辩论效果最好——太少缺乏多样性，太多导致协调成本过高。OpenAI 的 Council 模式和 Anthropic 的多模型验证都采用了这一思想。

## 核心概念

### Society of Minds (Du et al., ICML 2024)
- N model instances independently propose answers to the same question.
- Over R rounds, each model reads the others' proposals and critiques them.
- Models update their answers based on the critiques.
- After R rounds, return the convergent answer.
Original experiments used N=3, R=2 due to cost. Accuracy improves with more agents and more rounds on hard problems (MMLU, GSM8K, Chess Move Validity, biography generation).
Cross-model combinations beat single-model debates: ChatGPT + Bard together > either alone.
### Sparse topology
"Improving Multi-Agent Debate with Sparse Communication Topology" (arXiv:2406.11776, 2024-2025) showed full-mesh debate is not always optimal. Sparse topologies (star, ring, hub-and-spoke) can match accuracy at lower token cost. Each debater sees only a subset of peers.
Implications:
- Full mesh N=5, R=3 = 5 × 3 = 15 proposals, each reading 4 peers = 60 critique ops.
- Star N=5, R=3 (one hub + 4 spokes) = 15 proposals, spokes read only the hub = 12 critique ops.
### When debate helps
- **Factuality.** N independent proposals, cross-check reduces hallucination.
- **Rule-following.** Chess move validity — one model misses a rule, others catch it.
- **Open-ended reasoning.** Multiple framings narrow in on the right answer.
### When debate hurts
- **Latency-sensitive UX.** N × R serial rounds is latency you may not have.
- **Cost-sensitive scale.** N × R tokens per question.
- **Simple factual lookups.** One lookup is cheaper than five debates.
### 2026 practical instantiations
- **Anthropic orchestrator-workers** (Lesson 12) — one variant of debate with a synthesis step.
- **LangGraph supervisor** (Lesson 13) — central router + specialist agents can implement debate as a node.
- **OpenAI Agents SDK** (Lesson 16) — agents handoff back and forth for iterative critique.
- **Multi-agent evals** — pair debate + evaluator-optimizer for eval signal.
### Where this pattern goes wrong
- **Convergence collapse.** All agents converge on the first wrong answer. Mitigate with required disagreement rounds.
- **Hub failure.** In a star topology, a bad hub corrupts everyone. Rotate or use multiple hubs.
- **Prompt homogenization.** All agents use the same prompt; they produce the same answers. Use diverse prompts and/or models.

## 动手实现

`code/main.py` implements stdlib debate:
- `Debater` class (scripted LLM with per-debater opinion drift).
- `FullMeshDebate` and `SparseDebate` runners.
- Three questions: one factual, one rule-based, one reasoning.
- Metrics: convergent answer, rounds to convergence, total critique ops.
Run it:
```
python3 code/main.py
```
Output: per-protocol accuracy and cost; sparse matches full mesh on 2/3 questions at lower cost.

## 用框架实现

- **Anthropic orchestrator-workers** for simple 2-3-worker debates.
- **LangGraph** for stateful multi-round debate with checkpointing.
- **Custom** for research or specialized correctness guarantees.

## 产出物

`outputs/skill-debate.md` scaffolds a multi-agent debate with configurable topology, N, R, and a convergence rule.

## 练习题

1. Implement a "forced disagreement" rule: in round 1, every debater must produce a distinct proposal. Measure effect on convergence speed.
   *思考并实践此练习*
2. Add a confidence-weighted aggregation: debaters return (answer, confidence); aggregator weights by confidence. Does it help?
   *思考并实践此练习*
3. Swap one "agent" for a different scripted LLM with different opinions. Does heterogeneity improve accuracy?
   *思考并实践此练习*
4. Measure token cost for full mesh vs sparse on your 3 questions. Plot cost vs accuracy.
   *思考并实践此练习*
5. Read the Society of Minds paper. Port your toy to N=5, R=3. What breaks? What gets better?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Debate | "Multi-agent critique" |
| Full mesh | "Everyone reads everyone" |
| Sparse topology | "Limited peer view" |
| Hub-and-spoke | "Star topology" |
| Convergence | "Agreement" |
| Society of Minds | "Du et al. debate paper" |

## 延伸阅读

