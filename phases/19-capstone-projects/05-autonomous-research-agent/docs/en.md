# Capstone 05 — Autonomous Research Agent (AI-Scientist Class) | 结业 研究 美国

> Sakana's AI-Scientist-v2 published full papers. Agent Laboratory ran the experiments. Allen AI shared traces. The 2026 shape is plan-execute-verify tree search over experiments, budgeted cost, sandboxed code execution, a vision-feedback LaTeX writer, and an automated NeurIPS-style reviewer ensemble. The capstone is to build one, run it end to end within $30 per paper, and survive the sandbox-escape red team that Sakana documented.

> **【中文解读】** 本节是综合项目——构建自主研究 Agent，从文献检索到报告生成的完整流程。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent + sandbox), LaTeX (output) | **语言:** Python（Agent + 沙箱）, LaTeX（输出）
**Prerequisites:** Phase 2 (ML), Phase 3 (deep learning), Phase 7 (transformers), Phase 10 (LLMs from scratch), Phase 14 (agents), Phase 15 (autonomous), Phase 16 (multi-agent), Phase 18 (safety)

> 🔗 **【前置】** 顶点项目 05 = 综合几乎所有 Phase（2/3/7/10/14/15/16/18）。自主研究 Agent = Phase 15·05 的实战版。
> 💡 **【类比】** 自主研究 Agent = "AI 研究生"。参考 Sakana AI-Scientist-v2 / Allen AI / Agent Laboratory。架构：plan-execute-verify 树搜索 + 预算约束 + 沙箱代码执行 + 视觉反馈 LaTeX 写作 + 自动 NeurIPS 评审 ensemble。挑战：每篇论文 <$30 + 抵御沙箱逃逸红队（Sakana 已记录）。| **前置知识:** Phase 2（ML）, Phase 3（深度学习）, Phase 7（Transformer）, Phase 10（从头构建 LLM）, Phase 14（Agent）, Phase 15（自主系统）, Phase 16（多 Agent）, Phase 18（安全）
**Phases exercised:** P0 · P2 · P3 · P7 · P10 · P14 · P15 · P16 · P18 | **涉及阶段:** P0 · P2 · P3 · P7 · P10 · P14 · P15 · P16 · P18
**Time:** 40 hours | **时间:** 40 小时

## Problem | 问题引入

> **【中文解读】** 本节描述自主研究 Agent 的技术前沿。2026 年 Sakana AI 的 AI-Scientist-v2 在 Nature 发表了 AI 生成的论文，通过学术同行评审。核心不是模型魔法，而是"规划-执行-验证"循环在有界预算下搜索实验树。难点在于循环设计、预算控制和安全性——Sakana 团队记录了沙箱逃逸失败案例，你的 Agent 必须通过同样的红队测试。

> **【拓展：AI-Scientist 系列】** Sakana AI 的 AI-Scientist-v1（2024）首次展示了端到端自动科研流程，v2 进一步引入 AB-MCTS 风格的树搜索。ShinkaEvolve（ICLR 2026）扩展到进化式假设生成。AMD 的 Agent Laboratory 提供可复现的实验追踪。成本方面，v2 单篇论文控制在 $15-30，核心是每步预算估计和硬性终止。评审采用 5 个 LLM 评委的 NeurIPS 风格评分（新颖性/严谨性/清晰度/可复现性/影响力）。

Autonomous research agents crossed a threshold in 2026. Sakana AI's AI-Scientist-v2 was published in Nature with generated papers that cleared workshop peer review. ShinkaEvolve (ICLR 2026) extended the line to evolving hypotheses. AMD's Agent Laboratory shipped reproducible traces. The agents are not magic — they are a plan-execute-verify loop running over a tree of candidate experiments, with cost caps, seed-bound sandboxes, and automated review. The craft is in the loop, the budget, and the safety story.

> 自主研究 Agent 在 2026 年跨越了一个门槛。Sakana AI 的 AI-Scientist-v2 在 Nature 上发表了通过研讨会同行评审的生成论文。ShinkaEvolve（ICLR 2026）将这一方向扩展到进化假设。AMD 的 Agent Laboratory 发布了可复现的追踪。这些 Agent 不是魔法——它们是在候选实验树上运行的规划-执行-验证循环，有成本上限、绑定种子的沙箱和自动化评审。工艺在于循环、预算和安全叙事。

You learn the loop by implementing one against a seed idea in a narrow domain (for example, attention-sparsity ablations on a 100M-parameter transformer). The value is not in discovering something new on the first run. The value is in the infrastructure: the tree-search, the experiment sandbox, the writer-reviewer loop, the red-team report. The Sakana team documented sandbox-escape failures; your agent must pass the same red team.

> 你通过在狭窄领域的种子想法（例如，在 1 亿参数 Transformer 上的注意力稀疏性消融实验）上实现一个循环来学习。价值不在于第一次运行就发现新东西。价值在于基础设施：树搜索、实验沙箱、写作者-评审者循环、红队报告。Sakana 团队记录了沙箱逃逸失败；你的 Agent 必须通过同样的红队测试。

## Concept | 核心概念

> **【中文解读】** 自主研究 Agent 的核心是最佳优先树搜索。节点是实验规格（假设+配置+代码+预期结果），扩展步骤生成小改动的子节点（换优化器/调批次大小/消融组件）。每个子节点在带硬资源限制的沙箱中运行，结果反馈到评分函数（新颖性 x 质量 x 剩余预算）。论文写作是视觉反馈的：生成 LaTeX → 编译 → 渲染 PDF → 喂给 Opus 4.7 视觉模式评审布局和图表。安全方面，每个实验在无网络出口、固定种子的 E2B 沙箱中运行。

> **【拓展：自动化论文评审】** 评审集成使用 5 个不同 LLM（Opus 4.7、GPT-5.4、Gemini 3 Pro、DeepSeek R1、Qwen3-Max），加权聚合打分，模拟 NeurIPS 评审流程。均值低于 4.0/5 则退回修改，最多 3 轮重写。视觉反馈循环是关键创新——编译 PDF 后将渲染结果喂给 VLM 检查图表清晰度、声明-证据对齐和版面布局，这一步骤将论文质量提升约 15-20%。

The agent is a best-first tree search. Nodes are experiment specifications: (hypothesis, config, code, expected outcome). An expand step proposes children with small edits (swap optimizer, shift batch size, ablate a component). Each child runs in a fresh sandbox with a hard resource cap. Results feed back into a scoring function that ranks nodes by (novelty x quality x remaining budget). The tree grows until budget is exhausted, then the best branch is written up.

> Agent 是一个最佳优先树搜索。节点是实验规格：（假设、配置、代码、预期结果）。扩展步骤提出带有小编辑的子节点（交换优化器、调整批次大小、消融组件）。每个子节点在带有硬资源上限的新沙箱中运行。结果反馈到评分函数，按（新颖性 x 质量 x 剩余预算）对节点排序。树一直生长直到预算耗尽，然后最佳分支被写出来。

The writer is multimodal. It generates a LaTeX draft, compiles it, renders figures, and feeds the rendered PDF back into Claude Opus 4.7's vision mode for critique on layout, figure legibility, and claim-evidence alignment. A reviewer ensemble of five LLM judges emits NeurIPS-style scores (novelty, rigor, clarity, reproducibility, impact); if the average drops below threshold, the paper returns to the writer with critique.

> 写作者是多模态的。它生成 LaTeX 草稿、编译、渲染图表，并将渲染的 PDF 反馈给 Claude Opus 4.7 的视觉模式进行布局、图表清晰度和声明-证据对齐的批评。五个 LLM 评委的评审集成发布 NeurIPS 风格的分数（新颖性、严谨性、清晰度、可复现性、影响力）；如果平均分低于阈值，论文返回给写作者附带批评。

Safety is load-bearing. Every experiment runs in an E2B or Daytona sandbox with no network egress, bounded wall-clock, and pinned resource limits. The agent's code-generation step passes through a policy layer that blocks syscalls that escape the sandbox. The red-team report reproduces the Sakana-documented attack surface (fork bombs, filesystem escapes, LLM-written network calls).

> 安全是承重的。每个实验在无网络出口、有限挂钟时间和固定资源限制的 E2B 或 Daytona 沙箱中运行。Agent 的代码生成步骤通过一个策略层，阻止逃逸沙箱的系统调用。红队报告复现 Sakana 记录的攻击面（fork 炸弹、文件系统逃逸、LLM 编写的网络调用）。

## Architecture | 架构

```
seed idea + domain
      |
      v
  literature search (Semantic Scholar + OpenAlex + FAISS cache)
      |
      v
  LangGraph plan-execute-verify tree
      |
      v
  +--- expand node ----+      per-node sandbox
  |                    |      (E2B / Daytona)
  v                    v      resource caps
  child_1           child_k   no network egress
  |                    |      deterministic seeds
  v                    v
  run experiment       run experiment
  |                    |
  v                    v
  score nodes by (novelty, quality, budget)
      |
      v
  best branch -> LaTeX writer
      |
      v
  compile + vision critique (Opus 4.7 vision)
      |
      v
  reviewer ensemble (5 LLM judges, NeurIPS rubric)
      |
      v
  paper.pdf + review.md + trace.json
```

## Stack | 技术栈

- Orchestration: LangGraph with checkpointing and human-approval gates
  中文翻译：Orchestration: LangGraph with checkpointing and human-approval gates
- Tree search: custom best-first over experiment nodes (AB-MCTS-style from Sakana v2)
  中文翻译：Tree search: custom best-first over experiment nodes (AB-MCTS-style from Sakana v2)
- Sandbox: E2B per experiment, Docker-in-Docker fallback; resource caps via cgroups
  中文翻译：Sandbox: E2B per experiment, Docker-in-Docker fallback; resource caps via cgroups
- Literature: Semantic Scholar Graph API + OpenAlex + local FAISS cache of abstracts
  中文翻译：Literature: Semantic Scholar Graph API + OpenAlex + local FAISS cache of abstracts

> 中文翻译：Literature: Semantic Scholar Graph API + OpenAlex + local FAISS cache of abstracts（翻译）

- Writer: LaTeX template + Claude Opus 4.7 (vision mode) for figure critique and layout
  中文翻译：Writer: LaTeX template + Claude Opus 4.7 (vision mode) for figure critique and layout
- Reviewer: ensemble of 5 judges (Opus 4.7, GPT-5.4, Gemini 3 Pro, DeepSeek R1, Qwen3-Max) with weighted aggregation
  中文翻译：Reviewer: ensemble of 5 judges (Opus 4.7, GPT-5.4, Gemini 3 Pro, DeepSeek R1, Qwen3-Max) with weighted aggregation

> 中文翻译：Reviewer: ensemble of 5 judges (Opus 4.7, GPT-5.4, Gemini 3 Pro, DeepSeek R1, Qwen3-Max) with weighted aggregation（翻译）

- Experiment framework: PyTorch 2.5 for the physical experiments, W&B for logging
  中文翻译：Experiment framework: PyTorch 2.5 for the physical experiments, W&B for logging
- Observability: Langfuse for agent traces, $30 hard budget per paper
  中文翻译：Observability: Langfuse for agent traces, $30 hard budget per paper

## Build It | 动手构建

1. **Seed and domain scoping.** Take a seed idea (e.g., "investigate sparsity patterns in attention maps of sub-1B transformers"). Define the search space: models, datasets, compute budget.
   中文翻译：1. **Seed and domain scoping.** Take a seed idea (e.g., "investigate sparsity patterns in attention maps of sub-1B transformers"). Define the search space: models, datasets, compute budget.

2. **Literature pass.** Query Semantic Scholar + OpenAlex for 50 most-cited relevant papers; cache abstracts locally; generate a 1-page domain digest.
   中文翻译：2. **Literature pass.** Query Semantic Scholar + OpenAlex for 50 most-cited relevant papers; cache abstracts locally; generate a 1-page domain digest.

3. **Tree scaffolding.** Initialize the root with the seed hypothesis. Implement `expand(node) -> children` with small-edit proposals (one config change per child). Implement `score(node)` as a weighted novelty x quality x budget term.
   中文翻译：3. **Tree scaffolding.** Initialize the root with the seed hypothesis. Implement `expand(node) -> children` with small-edit proposals (one config change per child). Implement `score(node)` as a weighted novelty x quality x budget term.

4. **Sandbox wrapping.** Every experiment runs `docker run --network=none --memory=8g --cpus=2 --pids-limit=256 --read-only` (or the equivalent E2B policy). Seeds are written to the sandbox; outputs are mounted read-only back out.
   中文翻译：4. **Sandbox wrapping.** Every experiment runs `docker run --network=none --memory=8g --cpus=2 --pids-limit=256 --read-only` (or the equivalent E2B policy). Seeds are written to the sandbox; outputs are mounted read-only back out.

5. **Plan-execute-verify loop.** `plan` proposes children. `execute` runs the sandbox, captures logs and metrics. `verify` runs unit checks on metrics (did the loss decrease? did the ablation isolate the effect?). Failed nodes get a failure reason stored on the tree.
   中文翻译：5. **Plan-execute-verify loop.** `plan` proposes children. `execute` runs the sandbox, captures logs and metrics. `verify` runs unit checks on metrics (did the loss decrease? did the ablation isolate the effect?). Failed nodes get a failure reason stored on the tree.

6. **Writer.** After budget, select the best branch. Render figures with matplotlib. Generate a LaTeX draft via Claude Opus 4.7 with the branch trace in context. Compile. Feed the compiled PDF back to Opus 4.7 vision for critique. Iterate.
   中文翻译：6. **Writer.** After budget, select the best branch. Render figures with matplotlib. Generate a LaTeX draft via Claude Opus 4.7 with the branch trace in context. Compile. Feed the compiled PDF back to Opus 4.7 vision for critique. Iterate.

7. **Reviewer ensemble.** Five judges score the draft on (novelty, rigor, clarity, reproducibility, impact) with NeurIPS-style rubrics. If mean < 4.0/5, return to writer with critique. Hard stop after 3 rewrites.
   中文翻译：7. **Reviewer ensemble.** Five judges score the draft on (novelty, rigor, clarity, reproducibility, impact) with NeurIPS-style rubrics. If mean < 4.0/5, return to writer with critique. Hard stop after 3 rewrites.

8. **Red team.** Build or integrate a set of adversarial tasks targeting the sandbox: fork bombs, network exfiltration attempts, filesystem escapes, LLM-written shell metacharacters. Confirm all are blocked. Write up findings.
   中文翻译：8. **Red team.** Build or integrate a set of adversarial tasks targeting the sandbox: fork bombs, network exfiltration attempts, filesystem escapes, LLM-written shell metacharacters. Confirm all are blocked. Write up findings.

9. **Reproducibility.** Every paper ships with its tree-search trace JSON, seeds, W&B run links, sandbox configs, and a README reproducing it end to end.
   中文翻译：9. **Reproducibility.** Every paper ships with its tree-search trace JSON, seeds, W&B run links, sandbox configs, and a README reproducing it end to end.

## Use It | 使用方法

```
$ ai-scientist run --seed "attention sparsity in sub-1B transformers" --budget 30
[lit]    50 papers, digest in 12s
[tree]   expanded 8 nodes, budget 12/30
[exec]   node #3 sparsity=top-8, loss=2.83 (best so far)
[exec]   node #6 sparsity=top-4, loss=3.12 (worse)
[exec]   ...
[tree]   chose branch rooted at node #3 (novelty 0.62, quality 0.81)
[write]  LaTeX draft v1 complete
[vision] critique: figure 2 legend too small, claim-evidence ok
[write]  draft v2 after 3 edits
[review] mean 4.2/5 (novelty 3.9, rigor 4.3, clarity 4.1, repro 4.5, impact 4.2)
[done]   paper.pdf + review.md + trace.json     $28.40 spent
```

## Ship It | 部署上线

`outputs/skill-ai-scientist.md` is the deliverable. Given a seed idea + a domain + a $30 budget, it runs the full pipeline and emits a reviewable paper plus a reproducibility bundle.

> `outputs/skill-ai-scientist.md` 是交付物。给定种子想法 + 领域 + $30 预算，它运行完整管道并输出可评审的论文加可复现包。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | Paper quality | Blind rubric review against published workshop papers |
| 25 | 论文质量 | 对已发布研讨会论文的盲审评分 |
| 20 | Experimental rigor | Baselines, seeds, ablations; every claim backed by a cell in the results table |
| 20 | 实验严谨性 | 基线、种子、消融；每个声明有结果表中的单元格支持 |
| 20 | Cost and compute discipline | $30/paper ceiling enforced, Langfuse-traced |
| 20 | 成本与计算纪律 | $30/论文上限强制执行，Langfuse 追踪 |
| 20 | Safety | Sandbox red team passes; network policy and kill-switch verified |
| 20 | 安全性 | 沙箱红队通过；网络策略和终止开关已验证 |
| 15 | Reproducibility | One-command rerun with identical seeds reproduces the paper |
| 15 | 可复现性 | 相同种子的一键重跑复现论文 |
| **100** | | |

## Exercises | 练习题

1. Run the pipeline against three different seed ideas in the same domain. Compare which parts of the tree-search overlap. Identify duplicated wasted compute.
   中文翻译：在同一领域对三个不同种子想法运行管道。比较树搜索的重叠部分。识别重复的浪费计算。

2. Add a human-in-the-loop gate before experiment execution for nodes estimated above $5. Measure how much total cost drops.
   中文翻译：在预计超过 $5 的节点实验执行前添加人工审批门。测量总成本下降多少。

3. Swap the reviewer ensemble for a single judge. Measure the false-accept rate on a held-out set of known-bad papers.
   中文翻译：将评审集成换为单个评委。测量在已知差论文保留集上的误接受率。

4. Introduce a network-exfiltration red team test: agent writes code that tries to `curl` an external address. Confirm the `--network=none` policy blocks it. Log the attempt.
   中文翻译：引入网络渗透红队测试：Agent 编写尝试 `curl` 外部地址的代码。确认 `--network=none` 策略阻止它。记录尝试。

> 中文翻译：引入网络渗透红队测试：Agent 编写尝试 `curl` 外部地址的代码。确认 `--network=none` 策略阻止它。记录尝试。（翻译）


5. Compare your tree-search with a flat random baseline (same budget, no expansion strategy). Report the novelty x quality gain.
   中文翻译：将你的树搜索与平面随机基线比较（相同预算，无扩展策略）。报告新颖性 x 质量增益。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Tree search | "AB-MCTS-style expansion" | Best-first exploration over experiment nodes with a noveltyxqualityxbudget score |
| 树搜索 | "AB-MCTS 风格扩展" | 带新颖性x质量x预算分数的实验节点最佳优先探索 |
| Sandbox | "Experiment isolation" | Container with no network, bounded CPU/memory, pinned seeds, read-only inputs |
| 沙箱 | "实验隔离" | 无网络、有限 CPU/内存、固定种子、只读输入的容器 |
| Vision critique | "Render-then-read" | Compile the paper to PDF, feed the PDF back to a VLM for layout and claim-evidence critique |
| 视觉批评 | "渲染后阅读" | 将论文编译为 PDF，将 PDF 反馈给 VLM 进行布局和声明-证据批评 |
| Reviewer ensemble | "Automated peer review" | Multiple LLM judges scoring the paper with a NeurIPS rubric; weighted aggregate gates the pipeline |
| 评审集成 | "自动化同行评审" | 多个 LLM 评委用 NeurIPS 评分标准对论文打分；加权聚合控制管道 |
| Novelty score | "Is this new?" | Heuristic that penalizes proximity to the 50-paper literature cache |
| 新颖性分数 | "这是新的吗？" | 惩罚与 50 篇论文文献缓存接近度的启发式 |
| Cost ceiling | "$ budget" | Hard cap on total spend per paper; Langfuse counters + pre-run estimates |
| 成本上限 | "$ 预算" | 每篇论文总支出的硬性上限；Langfuse 计数器 + 预运行估算 |
| Red team | "Sandbox-escape audit" | Adversarial tasks that would escape the sandbox if the policy is wrong |
| 红队 | "沙箱逃逸审计" | 如果策略错误会逃逸沙箱的对抗任务 |

## Further Reading | 延伸阅读

- [Sakana AI-Scientist-v2 repository](https://github.com/SakanaAI/AI-Scientist-v2) — the reference production research agent
  中文翻译：参考生产研究 Agent
- [Sakana AI-Scientist-v1 paper (arXiv:2408.06292)](https://arxiv.org/abs/2408.06292) — the original methodology
  中文翻译：原始方法论
- [ShinkaEvolve (Sakana ICLR 2026)](https://sakana.ai) — evolutionary extension
  中文翻译：进化扩展
- [Agent Laboratory (AMD)](https://github.com/SamuelSchmidgall/AgentLaboratory) — multi-role research-lab framework
  中文翻译：多角色研究实验室框架
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — reference orchestration layer
  中文翻译：参考编排层
- [Semantic Scholar Graph API](https://api.semanticscholar.org/) — literature search
  中文翻译：文献搜索
- [E2B sandboxes](https://e2b.dev) — reference experiment isolation
  中文翻译：参考实验隔离
- [NeurIPS reviewer guidelines](https://neurips.cc/Conferences/2026/Reviewer-Guidelines) — the rubric the reviewer ensemble encodes
  中文翻译：评审集成编码的评分标准
