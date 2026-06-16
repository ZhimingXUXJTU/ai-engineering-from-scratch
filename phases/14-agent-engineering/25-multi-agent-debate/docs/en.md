# Multi-Agent Debate and Collaboration | 多 Agent 辩论

> Du et al. (ICML 2024, "Society of Minds") run N model instances that independently propose answers, then iteratively critique each other over R rounds to converge. Improves factuality, rule-following, reasoning. Sparse topology beats full mesh on token cost.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Explain the debate protocol: N proposers, R rounds, converge on a shared answer.
- Describe why debate improves factuality, rule-following, and reasoning.
- Explain sparse topology: not every debater needs to see every other.
- Implement a stdlib debate over a scripted LLM with full-mesh and sparse variants; measure token cost vs accuracy.

## The Problem | 问题引入

Self-Refine (Lesson 05) is one model critiquing itself — risks groupthink. CRITIC (Lesson 05) grounds critique in external tools — not always available. Debate introduces a third mode: multiple instances, cross-critique, convergence by disagreement.

> Self-Refine（第 5 课）是一个模型自我批评——存在群体思维的风险。CRITIC（第 5 课）将批评基于外部工具——并非总是可用。辩论引入了第三种模式：多个实例、交叉批评、通过分歧达成收敛。

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·05（Self-Refine / CRITIC）——辩论是 Self-Refine 的多实例扩展，不理解"一个模型自我批评为什么会陷入群体思维"就看不出辩论为什么要 N 个实例；Phase 14·12（Workflow Patterns）——理解 orchestrator-workers 和 supervisor 模式，本节的 hub-and-spoke 拓扑就是 supervisor 的具体实现。


> **【中文解读】** 多 Agent 辩论通过让多个 LLM 实例从不同角度讨论同一问题来提高推理质量。核心洞察：单个 LLM 可能自信地给出错误答案，但多个 LLM 辩论时，错误更容易被识别和纠正。这与人类专家小组讨论的原理相似。

> **{【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】}** 多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个 ChatGPT 实例辩论可以显著提高推理准确率。2026 年的实践表明，3-5 个 Agent 的辩论效果最好——太少缺乏多样性，太多导致协调成本过高。OpenAI 的 Council 模式和 Anthropic 的多模型验证都采用了这一思想。
## The Concept | 核心概念

### Society of Minds (Du et al., ICML 2024)

> 💡 **【类比】** 多 Agent 辩论像学术同行评审：你写论文（N=3 个独立作者各写一版）→ 投稿后 3 个审稿人读对方的版本写 review（R 轮交叉批评）→ 作者根据 review 修改 → 几轮后论文收敛。关键洞察：单个作者会自信地写错（Self-Refine 的群体思维），3 个独立作者互相挑错更容易揪出幻觉。但全连接（每人都读所有人）的评审成本是 O(N²)——所以会议用 "area chair + reviewers" 的星形拓扑（hub-and-spoke），审稿人只和 chair 沟通，成本降到 O(N)。

- N model instances independently propose answers to the same question.
- Over R rounds, each model reads the others' proposals and critiques them.
- Models update their answers based on the critiques.
- After R rounds, return the convergent answer.

Original experiments used N=3, R=2 due to cost. Accuracy improves with more agents and more rounds on hard problems (MMLU, GSM8K, Chess Move Validity, biography generation).

> 多 Agent 辩论通过让多个 Agent 对同一问题提出和论证不同观点来提高推理质量。这种方法在复杂推理任务上比单 Agent 表现更好。

Cross-model combinations beat single-model debates: ChatGPT + Bard together > either alone.

> 跨模型组合胜过单一模型辩论：ChatGPT + Bard 一起比单独任何一个都好。

> 多 Agent 辩论通过让多个 Agent 对同一问题提出和论证不同观点来提高推理质量。这种方法在复杂推理任务上比单 Agent 表现更好。

### Sparse topology

"Improving Multi-Agent Debate with Sparse Communication Topology" (arXiv:2406.11776, 2024-2025) showed full-mesh debate is not always optimal. Sparse topologies (star, ring, hub-and-spoke) can match accuracy at lower token cost. Each debater sees only a subset of peers.

> "Improving Multi-Agent Debate with Sparse Communication Topology"（arXiv:2406.11776, 2024-2025）表明全连接辩论并不总是最优的。稀疏拓扑（星形、环形、轮毂-辐条）可以在更低的 token 成本下匹配准确度。每个辩手只看到一部分同伴。

> 多 Agent 辩论通过让多个 Agent 对同一问题提出和论证不同观点来提高推理质量。这种方法在复杂推理任务上比单 Agent 表现更好。

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

> 🤔 **【困惑】** Q: 辩论到底什么时候值得用？N×R 的延迟和成本看起来很高。 A: 只用在"单模型错一次代价远高于辩论成本"的场景。判断公式：辩论成本 = N×R×单次推理成本；单模型错的期望损失 = 错误率 × 单次错误损失。当代码生成（一次 bug 进生产 = 几十万损失）、法律文书事实核查、医疗诊断这些场景，单模型哪怕 95% 准确率也值得用 N=3,R=2 辩论把准确率推到 99%。"今天天气怎么样""帮我总结邮件"这类一次错的损失就是用户重问一次的，千万别用辩论。

- **Convergence collapse.** All agents converge on the first wrong answer. Mitigate with required disagreement rounds.
- **Hub failure.** In a star topology, a bad hub corrupts everyone. Rotate or use multiple hubs.
- **Prompt homogenization.** All agents use the same prompt; they produce the same answers. Use diverse prompts and/or models.

> **收敛崩溃。** 所有 Agent 收敛到第一个错误答案。通过要求分歧轮次来缓解。
> **中心故障。** 在星形拓扑中，一个坏的中心会污染所有人。轮换或使用多个中心。
> **提示同质化。** 所有 Agent 使用相同的提示；产生相同的答案。使用多样化的提示和/或模型。

## Build It | 动手实现

> ⚠️ **【易错点】** 场景：开发者用同一个 prompt 起了 5 个 debater 实例期待"多样化观点" → 后果：5 个实例给出几乎一样的答案（甚至一样的错误），辩论沦为 N 倍成本的 Self-Refine，这叫 "prompt homogenization" → 修复：要么用不同模型（GPT-4o + Claude + Gemini，异构带来真分歧），要么给每个 debater 不同角色 prompt（"你是怀疑论者""你是乐观派""你是细节核查员"），要么至少随机化 temperature。论文里 ChatGPT + Bard 组合胜过单模型就是这个道理。

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

> 输出：每协议的准确度和成本；稀疏拓扑在 2/3 的问题上以更低成本匹配全连接。

> 多 Agent 辩论通过让多个 Agent 对同一问题提出和论证不同观点来提高推理质量。这种方法在复杂推理任务上比单 Agent 表现更好。

## Use It | 用框架实现

- **Anthropic orchestrator-workers** for simple 2-3-worker debates.
- **LangGraph** for stateful multi-round debate with checkpointing.
- **Custom** for research or specialized correctness guarantees.

## Ship It | 产出物

`outputs/skill-debate.md` scaffolds a multi-agent debate with configurable topology, N, R, and a convergence rule.

> `outputs/skill-debate.md` 搭建一个可配置拓扑、N、R 和收敛规则的多 Agent 辩论。

> 多 Agent 辩论通过让多个 Agent 对同一问题提出和论证不同观点来提高推理质量。这种方法在复杂推理任务上比单 Agent 表现更好。

## Exercises | 练习题

1. Implement a "forced disagreement" rule: in round 1, every debater must produce a distinct proposal. Measure effect on convergence speed.
  中文翻译：思考并实践此练习。
2. Add a confidence-weighted aggregation: debaters return (answer, confidence); aggregator weights by confidence. Does it help?
  中文翻译：思考并实践此练习。
3. Swap one "agent" for a different scripted LLM with different opinions. Does heterogeneity improve accuracy?
  中文翻译：思考并实践此练习。
4. Measure token cost for full mesh vs sparse on your 3 questions. Plot cost vs accuracy.
  中文翻译：思考并实践此练习。
5. Read the Society of Minds paper. Port your toy to N=5, R=3. What breaks? What gets better?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Debate | "Multi-agent critique" | N proposers, R rounds of cross-critique, converge |  |
| Full mesh | "Everyone reads everyone" | Every debater reads every peer each round |  |
| Sparse topology | "Limited peer view" | Debaters read only a subset of peers |  |
| Hub-and-spoke | "Star topology" | One central debater, N-1 spokes read only the hub |  |
| Convergence | "Agreement" | Debaters converge on a shared answer |  |
| Society of Minds | "Du et al. debate paper" | ICML 2024 multi-agent debate method |  |

## Further Reading | 延伸阅读

- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) — canonical multi-agent debate
  中文翻译：见原文。
- [Sparse Communication Topology (arXiv:2406.11776)](https://arxiv.org/abs/2406.11776) — sparse topology results
  中文翻译：见原文。
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — orchestrator-workers as a debate variant
  中文翻译：见原文。
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) — single-model self-critique counterpart
  中文翻译：见原文。
