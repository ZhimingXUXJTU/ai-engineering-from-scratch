# Swarm Optimization for LLMs (PSO, ACO) | 优化 群体 PSO ACO LLM

> Bio-inspired optimization is making an LLM comeback. **LMPSO** (arXiv:2504.09247) uses PSO where each particle's velocity is a prompt and the LLM generates the next candidate; works well on structured-sequence outputs (math expressions, programs). **Model Swarms** (arXiv:2410.11163) treats each LLM expert as a PSO particle on a model-weight manifold and reports **13.3% average gain** over 12 baselines on 9 datasets with just 200 instances. **SwarmPrompt** (ICAART 2025) hybridizes PSO + Grey Wolf for prompt optimization. **AMRO-S** (arXiv:2603.12933) is ACO-inspired pheromone specialists for multi-agent LLM routing — **4.7x speedup**, interpretable routing evidence, quality-gated asynchronous update that decouples inference from learning. This lesson implements PSO on prompt parameter space and ACO on agent routing, measures why these classical algorithms fit the LLM era, and when they do not.

> **【中文解读】** 本节介绍了群体优化算法——PSO（粒子群）和 ACO（蚁群）等生物启发优化在多 Agent 中的应用。

> **【拓展：swarm optimization pso aco→具体应用】** 群体优化算法在多 Agent 中的应用：(1) 粒子群优化（PSO）——Agent 根据自身最优位置和全局最优位置调整搜索方向；(2) 蚁群优化（ACO）——Agent 通过信息素标记好的路径，后来者倾向于跟随强信息素路径。这些算法适合大规模搜索空间中的优化问题，如 Agent 任务分配和路径规划。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

You have a prompt that scores 62% on your task eval. You want to improve it. The naive move is gradient-free manual tweaking, which scales badly. Reinforcement learning needs reward signals and enough rollouts to train. Backprop through prompts is not really possible — the prompt is a discrete string, not a differentiable parameter.

> 你有一个在任务评估中得分 62% 的提示。你想改进它。朴素的方法是无梯度手动调整，扩展性差。强化学习需要奖励信号和足够的训练轮次。通过提示反向传播并不真正可能——提示是离散字符串，不是可微分参数。

Classical bio-inspired optimization — PSO for continuous search spaces, ACO for path selection — was designed exactly for this regime: gradient-free, population-based, cheap per evaluation. Pair them with LLMs for the gradient-free search step, and you get a surprisingly practical optimizer.

> 经典的生物启发优化——PSO 用于连续搜索空间，ACO 用于路径选择——正是为这种场景设计的：无梯度、基于种群、每次评估成本低。将它们与 LLM 配对进行无梯度搜索步骤，你得到一个惊人实用的优化器。

The same patterns apply to agent *routing* in multi-agent systems. An ACO-style pheromone trail records which agent worked best on which task-type, lets the router exploit the trail, and decays pheromones so routes can be rediscovered.

> 同样的模式适用于多 Agent 系统中的 Agent *路由*。ACO 风格的信息素轨迹记录哪个 Agent 在哪种任务类型上表现最好，让路由器利用轨迹，并衰减信息素以便重新发现路径。

## Concept | 核心概念

### PSO refresher (Kennedy & Eberhart 1995)

Particle Swarm Optimization: population of particles in a continuous search space. Each particle has position `x_i` and velocity `v_i`. Each iteration:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

Where `p_best` is particle's own best, `g_best` is swarm's best, `w, c1, c2` are inertia + cognitive + social weights, `r1, r2` are random factors.

### PSO on LLM outputs — LMPSO

arXiv:2504.09247 adapts PSO for LLM-generated structured outputs (math expressions, programs). Each particle is a candidate output. Velocity is a *prompt* that describes how to modify the current output toward the personal/global best. The LLM generates the new output from the velocity prompt. The "inertia" of the velocity is a prompt like "make small incremental changes."

This works well when:
- The output is structured (parseable, evaluable).
  中文翻译：输出是结构化的（可解析、可评估）。
- Fitness is automatic (test runs, arithmetic evaluation).
  中文翻译：适应度是自动的（测试运行、算术评估）。
- Population is small (~10-30 particles) so total LLM calls stay manageable.
  中文翻译：种群小（约 10-30 个粒子），总 LLM 调用可控。

It does not work well when fitness needs human review — the per-iteration cost becomes prohibitive.

> 当适应度需要人工审查时效果不好——每次迭代成本过高。

### Model Swarms

arXiv:2410.11163 takes PSO off the output layer and into the *model* layer. Each "particle" is an expert LLM (parameters). The swarm moves the parameters toward the collective best via a gradient-free update. Reported: 13.3% average gain over 12 baselines on 9 datasets, with just 200 instances per iteration.

The key insight is that LLM expert models are already nearby in a shared parameter manifold (adapter weights, LoRA deltas). PSO on this low-dimensional subspace is cheap and effective.

### ACO refresher (Dorigo 1992)

Ant Colony Optimization: ants traverse a graph; each path has a pheromone trail. Ant move probabilities weight by pheromone strength. Ants that complete the task deposit pheromone proportional to solution quality. Pheromone decays over time.

### AMRO-S — ACO for agent routing

arXiv:2603.12933 uses ACO for multi-agent routing. Each task-type is a "destination"; each agent is a possible route. Pheromones strengthen routes that produce good outputs. Key contributions:

- **Interpretable routing evidence.** Pheromone strength is a human-readable signal.
  中文翻译：**可解释的路由证据。** 信息素强度是人类可读的信号。
- **Quality-gated asynchronous update.** Pheromones update only after quality checks pass, decoupling inference from learning.
  中文翻译：**质量门控异步更新。** 信息素只在质量检查通过后更新，将推理与学习解耦。
- **4.7x speedup** on the multi-agent routing benchmark.
  中文翻译：在多 Agent 路由基准上**4.7 倍加速**。

The quality gate matters: without it, fast-but-wrong agents accrue pheromone, and the system locks in on bad routes.

> 质量门很重要：没有它，快速但错误的 Agent 会积累信息素，系统锁定在不好的路径上。

### When to use PSO / ACO for LLMs

**Use PSO when:**
- Search space is continuous or maps to continuous parameters (prompt embeddings, LoRA weights, numeric generation parameters).
  中文翻译：搜索空间是连续的或映射到连续参数（提示嵌入、LoRA 权重、数值生成参数）。
- Fitness is cheap and automatic.
  中文翻译：适应度评估廉价且自动。
- Population can be small (10-30).
  中文翻译：种群可以很小（10-30）。

**Use ACO when:**
- You have a routing or path-selection problem.
  中文翻译：你有路由或路径选择问题。
- Decisions reinforce over time (the same task types come back).
  中文翻译：决策随时间强化（相同任务类型会回来）。
- You need interpretable evidence for routing decisions.
  中文翻译：你需要路由决策的可解释证据。

**Do not use either when:**
- Fitness requires human review (too expensive per iteration).
  中文翻译：适应度需要人工审查（每次迭代太贵）。
- The search space is discrete and combinatorial in a way that PSO does not cover (use genetic algorithms instead).
  中文翻译：搜索空间是离散组合的，PSO 无法覆盖（改用遗传算法）。
- Real-time decisions need strict latency (PSO/ACO converge slowly relative to single-pass heuristics).
  中文翻译：实时决策需要严格延迟（PSO/ACO 相对单次启发式收敛慢）。

### Why bio-inspired still wins

Gradient-based methods need differentiable signals. LLM outputs and routing decisions are not trivially differentiable. Pseudo-gradient methods (reinforcement-learned routers, DPO-style prompt tuners) work but need expensive training.

PSO and ACO need only an *evaluator* function. If you can score a candidate output or a routing decision, you can optimize over the space. That makes the bar for applicability much lower.

### Practical limits

- **Population budget.** N particles × T iterations × per-eval cost. For LLM evals at ~$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20. Plan accordingly.
- **Exploration vs exploitation.** Pheromone decay rate and PSO inertia trade off; too fast decay → forget solutions; too slow → stuck on early local optima.
- **Catastrophic drift.** Both algorithms can converge and then diverge if fitness landscape shifts (new data distribution). Monitor best-fitness stability.

## Build It | 动手构建

`code/main.py` implements:

- `LMPSO` — PSO over numeric prompt parameters (temperature, top_k weights). Each particle's "LLM generation" is simulated as a scripted fitness function. Runs the algorithm for 30 iterations and shows g_best convergence.
- `AMRO_S` — ACO-style routing. 3 agents, 4 task types, pheromone matrix, 100 routed tasks. Prints (task_type → agent choices) distribution over time to show trail formation.
- Comparison: random routing vs ACO routing on the same task stream. Measures quality and latency.

Run:

```
python3 code/main.py
```

Expected output:
- LMPSO: g_best fitness improves from random to near-optimal over 30 iterations.
- AMRO-S: pheromone table stabilizes on the right agent per task-type; ACO routing beats random by ~30-40% on quality and also reduces latency (fewer retries).

## Use It | 使用方法

`outputs/skill-swarm-optimizer.md` helps choose between PSO, ACO, genetic algorithms, and gradient-based optimizers for LLM / agent optimization problems.

## Ship It | 部署上线

- **Start small.** 10-20 particles, 20-50 iterations. Scale up only if the convergence curve shows clear gain.
  中文翻译：**从小开始。** 10-20 个粒子，20-50 次迭代。只在收敛曲线显示明显增益时才扩大。
- **Log pheromones or g_best per iteration.** Debugging swarm optimizers without a trail is painful.
  中文翻译：**每次迭代记录信息素或 g_best。** 没有轨迹调试群体优化器很痛苦。
- **Quality-gate updates.** Especially for ACO routing: fast-and-wrong agents must not accrue pheromone.
  中文翻译：**质量门控更新。** 特别是 ACO 路由：快速但错误的 Agent 不能积累信息素。
- **Reset decay on distribution shift.** When your eval distribution changes, aged pheromones are stale; reset or double the decay rate temporarily.
  中文翻译：**分布偏移时重置衰减。** 当评估分布变化时，老化信息素过时；重置或临时加倍衰减率。
- **Cap the per-iteration cost.** Emit a cost-per-iteration metric. PSO that costs $500 / iteration and gains 0.5% is not shippable.
  中文翻译：**限制每次迭代成本。** 发出每次迭代成本指标。每次迭代花费 $500 且只增益 0.5% 的 PSO 不可发布。

## Exercises | 练习题

1. Run `code/main.py`. Observe LMPSO convergence. Vary population size 5, 10, 20, 50. At what size does time-to-converge saturate?
2. Implement a "catastrophic drift" experiment: after iteration 30, change the fitness function. How fast does PSO adapt? Does resetting `p_best` help?
3. Add a quality gate to AMRO-S: pheromone deposit only on runs with eval score > 0.7. How does this change convergence vs the un-gated version?
4. Read LMPSO (arXiv:2504.09247). Map the paper's "velocity as a prompt" back to your numeric velocity. What is lost in the simulation and what is preserved?
5. Read AMRO-S (arXiv:2603.12933). Implement the decoupled "inference fast-path" with asynchronous pheromone update. How does this change system latency under sustained load?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Further Reading | 延伸阅读

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) — the 1995 PSO paper
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) — 1992 ACO foundations
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) — PSO for structured LLM outputs
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) — PSO on model-weight subspace
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) — pheromone-driven routing with quality gate
