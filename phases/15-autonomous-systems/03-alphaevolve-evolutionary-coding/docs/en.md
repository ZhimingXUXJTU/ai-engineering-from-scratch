# AlphaEvolve — Evolutionary Coding Agents | AlphaEvolve — 进化编码 Agent

> Pair a frontier coding model with an evolutionary loop and a machine-checkable evaluator. Let the loop run long enough. It discovers a 4x4 complex-matrix multiplication procedure that uses 48 scalar multiplications — the first improvement over Strassen in 56 years. It also finds a Google-wide Borg scheduling heuristic that recovers ~0.7% of cluster compute in production. The architecture is boring on purpose. The wins come from the evaluator's rigor.

> **【中文解读】** 将前沿编码模型与进化循环和机器可检查的评估器配对，让循环运行足够久。它发现了一种使用 48 次标量乘法的 4x4 复矩阵乘法过程——56 年来首次超越 Strassen。它还找到了一个 Google 全局 Borg 调度启发式，在生产中恢复约 0.7% 的集群计算。架构故意设计得枯燥，胜利来自评估器的严谨。

> **【拓展：进化算法 + LLM 的化学反应】** 进化算法（变异+选择+交叉）已有数十年历史，但传统随机变异在大型程序上几乎总是产生语法错误。LLM 作为"智能变异算子"改变了这一点：它能提出编译通过的、语义上合理的修改。AlphaEvolve 的关键创新就在于此——LLM 提议，评估器裁决。这是"LLM 智能搜索"模式的代表作，后续的 AI Scientist v2、Darwin Godel Machine 都遵循同一配方。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Large language models can write code. Evolutionary algorithms can search over code. Both have been tried separately for decades; both hit ceilings.

> 大语言模型可以编写代码，进化算法可以在代码空间上搜索。两者各自尝试了几十年，都碰到了天花板。

The LLM ceiling is confabulation: the model writes plausible code that does not do what it claims. The evolutionary ceiling is search cost: random mutations over syntax rarely produce compilable programs, let alone better ones.

> LLM 的天花板是虚构：模型写出看似合理但实际行为不符声明的代码。进化的天花板是搜索成本：对语法的随机变异很少产生可编译的程序，更不用说更好的。

AlphaEvolve (Novikov et al., DeepMind, arXiv:2506.13131, June 2025) combines them. The LLM proposes targeted edits to a program database; an automatic evaluator scores each variant; high-scoring variants become parents for future generations. The LLM handles the expensive step of writing plausible code; the evaluator catches the confabulations. The loop runs for hours to weeks.

> AlphaEvolve（Novikov 等人，DeepMind，arXiv:2506.13131，2025 年 6 月）将两者结合。LLM 对程序数据库提出有针对性的编辑；自动评估器对每个变体打分；高分变体成为未来世代的父本。LLM 处理编写合理代码这一昂贵步骤；评估器捕获虚构。循环运行数小时到数周。

> **【中文解读】** AlphaEvolve（Google DeepMind, 2025）将进化算法应用于代码优化。它维护一个程序种群，通过变异、交叉和选择迭代优化。关键创新是将 LLM 作为变异算子——用 LLM 生成和修改代码，而不是随机变异。在数学发现和算法优化上取得了突破性成果。

Results reported: 48-scalar-multiplication 4x4 complex matrix multiplication (Strassen's 1969 bound was 49), a Borg scheduling heuristic in Google production, a 32.5% FlashAttention kernel speedup, Gemini training throughput improvements.

> 报告的结果：48 次标量乘法的 4x4 复矩阵乘法（Strassen 1969 年的边界是 49），Google 生产中的 Borg 调度启发式，32.5% 的 FlashAttention 内核加速，Gemini 训练吞吐量改进。

The architecture works because the evaluator is machine-checkable. It does not work where the evaluator isn't. That asymmetry is the lesson.

> 这种不对称性就是本课的核心：架构之所以有效，是因为评估器是机器可检查的；评估器不可信的领域，循环就失效。

## The Concept | 核心概念

### The loop | 循环

1. Start from a seed program `P_0` that is correct but suboptimal.
   中文翻译：从一个正确但次优的种子程序 `P_0` 开始。
2. Maintain a database of variant programs, each scored by the evaluator.
   中文翻译：维护一个变体程序数据库，每个变体由评估器打分。
3. Sample one or more parents from the database (MAP-elites-style or island-based).
   中文翻译：从数据库中采样一个或多个父本（MAP-elites 风格或岛屿模型）。
4. Prompt the LLM (Gemini Flash for many candidates, Gemini Pro for the hard ones) to produce a modified variant of the parent.
   中文翻译：提示 LLM（多数候选用 Gemini Flash，难题用 Gemini Pro）生成父本的修改变体。
5. Compile, run, and evaluate the variant on the held-out evaluator.
   中文翻译：编译、运行并在保留评估器上评估变体。
6. Insert into the database keyed by its score and feature vector.
   中文翻译：以分数和特征向量为键插入数据库。
7. Repeat.
   中文翻译：重复。

Two details matter. First, the LLM is prompted with more than the parent program — typically several top variants from the database, plus the evaluator signature, plus a short task description. The model's job is to propose a targeted change that might improve the score. Second, the database is structured (MAP-elites grid, island-based) so the loop explores diversity, not just the current leader.

> 两个细节很重要。第一，提示 LLM 时不只给父程序——通常是数据库中排名最高的几个变体，加上评估器签名和简短任务描述。模型的工作是提议可能提高分数的有针对性变更。第二，数据库是结构化的（MAP-elites 网格、岛屿模型），让循环探索多样性，而不只是当前最优解。

### What makes the evaluator non-negotiable | 评估器为何不可妥协

AlphaEvolve's wins all come from domains where the evaluator is fast, deterministic, and hard to game:

> AlphaEvolve 的胜利全部来自评估器快速、确定性且难以博弈的领域：

- **Matrix multiplication algorithm**: a unit test that multiplies matrices and checks equality bit-identically.
  中文翻译：**矩阵乘法算法**——一个乘以矩阵并逐位检查相等性的单元测试。
- **Borg scheduling heuristic**: a production-grade simulator that replays historical cluster load and measures wasted compute.
  中文翻译：**Borg 调度启发式**——一个生产级模拟器，重放历史集群负载并测量浪费的计算。
- **FlashAttention kernel**: a correctness test plus a wall-clock benchmark on real hardware.
  中文翻译：**FlashAttention 内核**——正确性测试加上真实硬件上的墙钟基准。
- **Gemini training throughput**: measured GPU-seconds per step.
  中文翻译：**Gemini 训练吞吐量**——测量每步的 GPU 秒数。

In each case the evaluator catches the class of LLM errors that would otherwise dominate: confabulated correctness claims, performance claims that vanish on hardware, and edge-case failures. Remove the evaluator and the loop optimizes for pretty code.

> 在每种情况下，评估器捕获了否则会占主导地位的 LLM 错误类：虚假的正确性声明、在硬件上消失的性能声明和边缘情况失败。移除评估器，循环会优化漂亮的代码。

### Reward hacking is the other face of that statement | 奖励篡改是该论断的另一面

Evolution optimizes for whatever the evaluator measures. If the evaluator is imperfect, the loop will find the imperfection. In an unverified domain the loop would optimize for the surface feature, not the intended behavior.

> 进化优化评估器测量的任何东西。如果评估器不完美，循环会找到不完美之处。在未验证的领域中，循环会优化表面特征而非预期行为。

DeepMind flags this explicitly in the paper: AlphaEvolve's successes transfer only to domains where evaluator rigor matches the ambition of the search.

> DeepMind 在论文中明确指出：AlphaEvolve 的成功只能迁移到评估器严谨性与搜索野心相匹配的领域。

Concrete 2025-2026 examples of reward hacking in code-search loops:

> 2025-2026 年代码搜索循环中奖励篡改的具体例子：

- Optimization targets that reward "time to complete" rewarded submitting empty solutions.
  中文翻译：奖励"完成时间"的优化目标会奖励提交空解决方案。
- Benchmark scores that reward correctness-under-test rewarded memorizing tests and overfitting.
  中文翻译：奖励测试正确性的基准分数会奖励记忆测试和过拟合。
- A "code quality" proxy rewarded removing comments and rewriting variable names, with no semantic change.
  中文翻译："代码质量"代理会奖励删除注释和重写变量名，而没有语义变化。

The fix in AlphaEvolve: ship a held-out evaluator the LLM has never seen, with inputs generated at evaluation time. Even then, DeepMind recommends strong review on any proposed deployment.

> AlphaEvolve 的修复：交付一个 LLM 从未见过的保留评估器，输入在评估时生成。即便如此，DeepMind 建议对任何提议的部署进行严格审查。

### Why LLM + search beats either alone | 为什么 LLM + 搜索胜过单独使用

The LLM can produce compilable, semantically plausible modifications. A random-mutation GA on a 2000-line Python file almost always produces syntax errors. The LLM also concentrates search on plausible neighborhoods (change one function, not random bytes) which dramatically reduces wasted evaluator calls.

> LLM 可以产生可编译的、语义上合理的修改。在 2000 行 Python 文件上的随机变异 GA 几乎总是产生语法错误。LLM 还将搜索集中在合理的邻域（改一个函数，而非随机字节），这大大减少了浪费的评估器调用。

The evaluator, in turn, catches the LLM's confabulations. LLMs will confidently claim that a function "is O(n log n) in the limit" when it is actually O(n^2); a wall-clock benchmark makes the question settled.

> 评估器反过来捕获 LLM 的虚构。LLM 会自信地声称一个函数"极限下是 O(n log n)"，而实际是 O(n²)；墙钟基准让问题尘埃落定。

### Where AlphaEvolve fits in the frontier stack | AlphaEvolve 在前沿技术栈中的位置

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

All four are variations on the same recipe: generator plus evaluator, loop. The differences are what the evaluator grades and how rigorous it is.

> 四者都是同一配方的变体：生成器加评估器，循环。区别在于评估器评分什么以及有多严谨。

## Use It | 用框架实现

`code/main.py` implements a minimal AlphaEvolve-like loop over a toy symbolic-regression problem.

> `code/main.py` 在一个玩具符号回归问题上实现了类似 AlphaEvolve 的最小循环。

The "LLM" is a stdlib proxy that proposes small syntactic mutations to a program that computes a target function. The "evaluator" measures mean squared error on held-out test points.

> "LLM" 是一个标准库代理，对一个计算目标函数的程序提出小的语法变异。"评估器" 在保留测试点上测量均方误差。

Watch:

> 观察：

- How the best score improves over generations.
  中文翻译：最佳分数如何在世代中提升。
- How a MAP-elites grid keeps diverse solutions alive so the loop doesn't converge on a local minimum.
  中文翻译：MAP-elites 网格如何保持多样化解存活，让循环不收敛到局部最小。
- How removing the held-out test (training-only evaluator) lets the loop overfit spectacularly.
  中文翻译：移除保留测试（仅训练评估器）如何让循环灾难性地过拟合。

## Ship It | 产出物

`outputs/skill-evaluator-rigor-audit.md` is the precondition for considering an AlphaEvolve-style loop in a new domain: does your evaluator actually catch the failures you care about?

> `outputs/skill-evaluator-rigor-audit.md` 是在新领域考虑类似 AlphaEvolve 循环的前提条件：你的评估器是否真的捕获了你关心的失败？

## Exercises | 练习题

1. Run `code/main.py`. Note the best score trajectory. Disable the held-out evaluator (flag `--no-holdout`) and re-run. Quantify the overfitting.
   中文翻译：运行 `code/main.py`。记录最佳分数轨迹。禁用保留评估器（标志 `--no-holdout`）重新运行。量化过拟合。

2. Read Section 3 of the AlphaEvolve paper on the MAP-elites grid. Design a feature-vector descriptor for a new problem (e.g. compiler optimization passes) that would keep the search diverse.
   中文翻译：阅读 AlphaEvolve 论文第 3 节关于 MAP-elites 网格。为新问题（例如编译器优化遍次）设计一个保持搜索多样性的特征向量描述符。

3. The 48-multiplication 4x4 result improved on Strassen's 49-mul bound after 56 years. Read Appendix F of the paper and explain in three sentences why the evaluator for this problem is particularly easy to get right, and why most domains are not like it.
   中文翻译：48 次乘法的 4x4 结果在 56 年后改进了 Strassen 的 49 次乘法边界。阅读论文附录 F，用三句话解释为什么这个问题的评估器特别容易做对，以及为什么大多数领域不是这样。

4. Propose one domain where AlphaEvolve would fail. Identify exactly where the evaluator breaks and why.
   中文翻译：提议一个 AlphaEvolve 会失败的领域。精确指出评估器在哪里失效以及原因。

5. For a domain you know, write the evaluator signature you would use. Include (a) correctness conditions, (b) performance metric, (c) held-out input generation rule, (d) at least one anti-reward-hacking check.
   中文翻译：对你了解的一个领域，写出你会使用的评估器签名。包括 (a) 正确性条件，(b) 性能指标，(c) 保留输入生成规则，(d) 至少一个反奖励篡改检查。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Further Reading | 延伸阅读

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) — the full paper.
  中文翻译：完整论文。
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) — vendor writeup with results.
  中文翻译：厂商撰文及结果。
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results) — discovered algorithms, including the 48-mul 4x4 matmul.
  中文翻译：发现的算法仓库，包括 48 次乘法的 4x4 矩阵乘法。
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) — the predecessor system.
  中文翻译：前身系统 FunSearch。
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) — frames evaluator-bound autonomy as a key research direction.
  中文翻译：将评估器约束的自主性作为关键研究方向。
