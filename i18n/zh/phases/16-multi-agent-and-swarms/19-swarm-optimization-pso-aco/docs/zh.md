# 优化 群体PSO ACO LLM

> 生物灵感优化正在使LLM复苏.**LMPSO**(arXiv:2504.09247) 使用PSO,每个粒子的速度是提示,LLM生成下一个候选人;在结构序列输出 (数学表达式,程序) 上工作良好. **Model Swarms**(arXiv:2410.11163) 对待每一位LLM专家作为模型重量多元件的PSO粒子,并报告**13.3% average gain**只有200个实例的9个数据集上超过12个基线. **SwarmPrompt**为了快速优化,将PSO+灰狼混合.**AMRO-S**                                  **4.7x speedup**通过"PROPT PARAMETER SPACE"和"ACO"在代理路由中,测量这些经典算法为什么适合LLM时代,以及何时不适合.

> **【中文解读】**本节介绍了生物启动多代理中优化算法 (PSO) 和ACO (ACO) 等生物的应用.

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO)  根据自身最佳位置和全局最佳位置调整搜索方向;(2) 群体优化(ACO)  代理通过信息素标记的好路径,后者倾向于遵循强信息素路径.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

>  **【前置】**学本节前请先掌握:阶段16·09(Swarm 网络) 、阶段16·14(BFT) 、经典优化算法(PSO/ACO/GA) ⋅本节把生物启发算法应用到LLM时代快速 优化、模型路由──
>  **【类比】**马+PSO/ACO = "群找最佳快速"──PSO = 每个代理是粒子,速度=快速,向全局最优移动;ACO = 代理在快速 空间留下信息素,后者跟随强信息素──LMPSO 适合结构化输出(数学表达式、代码);模型群把每个LLM 专家作为粒子,比12个基线平均高13.3%;AMRO-S使用ACO 做代理 路由,4.7倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

您有一个提示,在任务评估中得分62%.您想改进它. 简单的举动是无梯度的手动调整,这很糟糕.强化学习需要奖励信号和足够的推广来训练. 通过提示推进实际上是不可能的.提示是一个单独的字符串,而不是一个可分化参数.

> 你有一个在任务评估中获得62%的提示――你想改进它――简单的方法是无梯度的手动调整,扩展性差距――强化学习需要奖励信号和足够的训练轮次――通过提示反向传播并不真正可能

经典生物启发优化  PSO 连续搜索空间,ACO 选路是专门为这个制度设计的:无梯度,基于人口,每项评估便宜.对其进行无梯度搜索步骤的LLM结合,你得到了一个令人惊的实用优化器.

> 经典的生物启发优化PSO 用于连续搜索空间,ACO 用于选择路径正是为这种场景设计的:无梯度,基于种群,每次评估成本低.

类似的模式适用于多代理系统中的代理 *路由 * .ACO式的子记录了哪个代理在哪个任务类型上最好工作,让路由器利用该线路,并分解子,以便重新发现路线.

> 同样的模式适用于多代理系统中的代理 *路由*──ACO 风格的信息素轨迹记录哪个代理在哪种任务类型上表现最好,让路由器利用轨迹,并减少信息素以重新发现路径──

## 概念的核心概念

### 公共卫生组织的更新 (肯尼迪和埃伯哈特 1995)

粒子群优化:在连续搜索空间中的粒子群.每个粒子都有位置.`x_i`速度`v_i`每次代:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

在哪里?`p_best`粒子本身的最佳.`g_best`是群众最好的,`w, c1, c2`它们是惯性+认知+社会权重,`r1, r2`它们是随机因素.

### 关于法定管理局的产品的PSO  LMPSO

根据""的定义,每颗粒子都是一个候选输出.速度是描述如何修改当前输出,以实现个人/全球最佳.LLM从速度提示生成新的输出.速度的"惰性"是"做小增进变化"这样的提示.

如果:
- 输出结构化 (可解析,可评估).
  中文翻译:输出是结构化的(可解析、可评估)
- 健身是自动的 (测试运行,算术评估).
  中文翻译:适应度是自动的测试运行、算术评估)
- 人口小 (~10-30颗粒),因此总计LLM调用仍然可管理.
  中文翻译:种群小(约10-30个粒子),总 LLM 调用可控。

身体健康需要人体检查时,它不起作用.

> 适应需要人工审查时效果不好 代价过高

### 模型群

随着一个数据集的更新,每一个"粒子"都会通过一个无梯度更新将参数移动到集体最佳水平.报告:在9个数据集上平均增加13.3%的12个基线,每次代仅为200次.

基本的见解是,在一个共享参数多元组 (适配器重量,LORA 分) 中,LLC专家模型已经接近.

### 更新ACO (多里戈 1992)

殖民地优化:穿过图表;每个路径都有子痕迹.子按子强度移动概率重量.完成任务的子按溶液质量比例存储子.子随时间而衰退.

###  AMRO-S  ACO 代理路由

根据ACO的数据,每一个任务类型都是"目的地",每一个代理都是可能的路线.

- **Interpretable routing evidence.**子强度是人类可以读取的信号.
  翻译: 中文**可解释的路由证据。**信息素强度是人类可读的信号.
- **Quality-gated asynchronous update.**异体仅在质量检查通过后更新, 脱离结论与学习.
  翻译: 中文**质量门控异步更新。**信息素只在质量检查通过更新后,将与学习解.
- **4.7x speedup**关于多代理路由基准.
  中文翻译:在多 代理路由基准上**4.7 倍加速**,我知道.

质量关键:没有它,快速但错误的代理会积聚,

> 质量门很重要:没有它,快速但错误的代理会积累信息素,系统锁定在不好的路径上.

### 什么时候使用PSO/ACO在 LLM

**Use PSO when:**
- 搜索空间是连续的或是连续参数的地图 (即时嵌入,LoRA权重,数值生成参数).
  中文翻译:搜索空间是连续的或映射到连续参数 (图片嵌入,LoRA权重,数值生成参数) ⋅
- 健身是便宜的,自动的.
  中文翻译:适应度评估廉价且自动.
- 人口可能很小 (10-30).
  中文翻译:种群可以很小 ((10-30) 』

**Use ACO when:**
- 你有路由或路径选择问题.
  中文翻译:你有路由或路径选择问题──
- 随着时间的推移,决策得到加强 (同样的任务类型会再次出现).
  中文翻译:决策随时间强化 (同样的任务类型会回来)
- 你需要解释的证据来决定路线.
  中文翻译:你需要路由决策的可解释证据.

**Do not use either when:**
- 健身需要人体审查 (每次代谢太昂贵).
  中文翻译:适应度需要人工审查 (每次代过贵)
- 搜索空间是单独的和结合式的,以一种方式,PSO不覆盖 (使用遗传算法而不是).
  中文翻译:搜索空间是离散组合的,PSO无法覆盖 (改用遗传算法)
- 实时决策需要严格的延迟 (PSO/ACO相对于单通度度相对慢相近).
  中文翻译:实时决策需要严格延迟(PSO/ACO 相对单次启发式收慢) ⋅

### 生物灵感的原因仍然是胜利

基于梯度的方法需要可分辨的信号.LLM输出和路由决策并不微乎其微的分辨性.伪梯度方法 (强化学习路由器,DPO式快速调节器) 有效,但需要昂贵的培训.

对于 PSO 和 ACO,只需要一个*评估器*函数.如果您可以评分一个候选输出或路由决定,您可以优化空间. 这使得适用性条格更低.

### 实际限制

- **Population budget.**对于LLM评价的~$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20,根据计划.
- **Exploration vs exploitation.**子衰变率和PSO惰性交换;过快衰变 →忘记解决方案;过慢 →坚持早期的本地优势.
- **Catastrophic drift.**两种算法可以在健身环境变化 (新数据分布) 时融合,然后分离.

## 动手构建
```figure
swarm-stigmergy
```

## 建立它

`code/main.py`执行:

- `LMPSO`PSO对数值提示参数 (温度,顶_k重量).每个粒子的"LLM生成"是模拟的脚本健身函数.运行算法30次并显示g_best融合.
- `AMRO_S` ACO 类型的路由. 3 个代理, 4 个任务类型, 子矩阵, 100 个路由任务. 打印 (task_type → 代理选择) 时间分布以显示轨迹形成.
- 比较:随机路由与同一任务流中的ACO路由. 测量质量和延迟.

运行:

```
python3 code/main.py
```

预期产量:
- 体育:g_best 身体健康从随机到近最佳的改善超过30次.
- AMRO-S:因任务类型而稳定于正确的代理;ACO路由在质量上随机超过30-40%,同时降低延迟 (减少重试).

## 用它使用方法

`outputs/skill-swarm-optimizer.md`帮助选择PSO,ACO,遗传算法和基于梯度的优化器来解决LLM/代理优化问题.

## 发射上线

- **Start small.**只有在缩曲线显示明显的增长的情况下,
  翻译: 中文**从小开始。**只有收曲线显示明显的增长,才扩大.
- **Log pheromones or g_best per iteration.**没有痕迹的调试群群优化器是痛苦的.
  翻译: 中文**每次迭代记录信息素或 g_best。**没有轨迹调试群体优化器很痛苦.
- **Quality-gate updates.**特别是在ACO路由方面:快速和错误的药物不能积累.
  翻译: 中文**质量门控更新。**特别是ACO路由:快速但错误的代理 不能积累信息素.
- **Reset decay on distribution shift.**当你的评估分布发生变化时,老化的子会变得陈旧;暂时重新设置或翻倍衰变率.
  翻译: 中文**分布偏移时重置衰减。**评估分布变化时,信息素老化过时;重置或临时加倍衰退率.
- **Cap the per-iteration cost.**发出每次发行成本的指标. 费用500美元/发行,并获得0.5%的收益,不能运输.
  翻译: 中文**限制每次迭代成本。**发出每代成本指标. 每代花费500美元,只增加0.5%的PSO不可发行.

## 练习题

1. 跑步`code/main.py`观察LMPSO的化. 不同人口规模 5, 10, 20, 50. 化时间在多少度?
2. 执行"灾难性漂移"实验:在30次回复后,改变健身功能.PSO如何快速适应?是否重置`p_best`帮助?
3. 添加质量门 AMRO-S:仅在评估分数>0.7 的运行时存储子.
4. 读LMPSO (arXiv:2504.09247). 绘制纸的"速度作为提示"回到你的数值速度.
5. 通过非同步的激素更新,实现脱的"推理快速路径". 这如何改变系统延迟在持续负载下?

## 关键词 关键词

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

## 继续阅读 继续阅读

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968)1995年公共卫生组织文件
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) 1992年ACO基金会
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247)结构化LLM产品的公共服务管理局
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163)模型重量子空间的PSO
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) 质量门的胺驱动路由
