# 进化编码代理

> 结合一个边界编码模型,一个进化循环和一个可机器检查的评估器. 让循环足够长. 它发现了4x4复杂矩阵乘法程序,使用48个 skalar乘法,这是在56年来第一次改善Strassen. 它还发现了谷歌范围内的Borg计划测量, 建筑是故意无聊的. 获胜来自评审员的严谨性.

> **【中文解读】**通过将前沿编码模型与进化循环和机器可检查的评估器配对,让循环运行足够久. 它发现使用48次标量乘法的4×4复矩阵乘法过程56年来首次超越Strasen. 它还发现了一个谷歌全局博格调度启动式,在生产中恢复了约0.7%的集群计算.

> **【拓展：进化算法 + LLM 的化学反应】**进化算法 (?? 变异+选择+交叉) 已经有几十年的历史,但传统随机变异在大型程序几乎总是产生语法错误.LLM作为"智能变异算法"改变了这一点:它可以提出编译通过的语义上的合理修改.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段15·01(长程代理) 阶段15·02(STaR自我改进) 进化算法基础(变异/交叉/选择) ・AlphaEvolve = LLM 作为智能变异算子的进化算法。
>  **【类比】**艾尔法Evolve = "AI 实验室里的博士生群体"――传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群AI 博士生,每个人都提出有意义的修改("试试把循环展开两倍"),评估器跑实验打分,高分修改进入下一代种群――LLM 解决"如何提出合理变异",评估器解决"如何辨别伪装"结真相 56年首次突破Strassen 矩阵乘法――
>  **【困惑】**问:为什么AlphaEvolve 能超越人类专家? 因为它运行数百万次变化,每次使用真实基准验证.

## 问题 问题引入

语言模型可以编写代码.进化算法可以搜索代码.这两种语言都已经被单独尝试了几十年;两种都达到限度.

> 大语言模型可以编写代码,进化算法可以在代码空间上搜索.

士师范大学的上限是论:模型写出可靠的代码,但它不做它所说的.进化上限是搜索成本:语法上的随机突变很少产生可编译的程序,更不用说更好的程序.

> 士课程的天花板是虚构的:模型写出看似合理但实际行为不符的代码.

专业知识研究 (LLC) 提出了针对性的编辑程序数据库;一个自动评估器评分每个变体;高分变体成为未来代人的父母.专业知识研究处理了可信代码编写的昂贵步骤;评估员捕获了论.循环持续数小时到几周.

> 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏平台 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏 博电子游戏

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) 将进化算法应用于代码优化. 它维护了一个程序种群,通过变异,交叉和选择代优化.

结果报告:48级乘法4x4复杂矩阵乘法 (斯特拉森1969年限为49),谷歌生产中的博格计划论,FlashAttention内核增速32.5%,双子座训练吞吐量改进.

> 报告结果:48次标量乘法4x4 复矩阵乘法(Strassen 1969年的边界是49),Google 生产中的Borg调度启动式,32.5%的闪光注意力内核加速,双胞胎 训练吞吐量改进──

建筑是因为评估器是机器检查的,它不在评估器没有的地方工作.

> 这种不对称性是本课程的核心:架构之所以有效,是因为评估器是机器可检查的;评估器不可信的领域,循环就失效了.

## 概念的核心概念

### 循环

1. 开始从种子计划开始`P_0`这正确,但不太理想.
   简单的,但优秀的种子程序.`P_0`开始.
2. 保持变种程序的数据库,每个程序由评价者评分.
   中文翻译:维护一个变体程序数据库,每个变体由评估器打分.
3. 从数据库中取出一个或多个父母的样本 (MAP精英类型或岛屿类型).
   中文翻译:从数据库中采样一个或多个父本(MAP精英风格或岛屿模型) ⋅
4. 要求士 (许多候选人是双子闪光,硬的双子Pro) 制造父母的修改版本.
   中文翻译:提示 LLM(多数候选人用双子闪光,难题用双子Pro)生成父本的修改变体──
5. 编译,运行和评估在持久的评估器上的变体.
   中文翻译:编译、运行并保留评估器上评估变体──
6. 按其分数和特征向量键入数据库.
   中文翻译:以分数和特征向量为关键插入数据库.
7. 复制.
   中文翻译:重复──

首先,LLM需要更多的数据库,加上评估者签名,加上简短的任务描述.模型的工作是提出一个有针对性的变化,可能会改善得分.第二,数据库结构化 (MAP精英网格,基于岛屿) 因此循环探索多样性,而不仅仅是当前领导者.

> 两个细节很重要. 第一,提示LLM 时不仅给父程序通常是数据库中排名最高的几个变体,加上评估器签名和简短任务描述.模型的工作是建议可能提高分数的针对性变化.

### 评价器是什么不妥协的?

们都在一个快速,决定性和难以玩的领域中获胜:

> 果的成功全部来自评估器快速,确定性和难以理解的领域:

- **Matrix multiplication algorithm**测试单位测试,乘以矩阵并检查等式的比特相同.
  翻译: 中文**矩阵乘法算法**乘以矩阵并位检查等等的单元测试.
- **Borg scheduling heuristic**产品级模拟器,可重复历史集群负载,并测量浪费计算.
  翻译: 中文**Borg 调度启发式**一个生产级模拟器,重放历史集群负载并测量浪费的计算.
- **FlashAttention kernel**实用硬件的墙钟基准.
  翻译: 中文**FlashAttention 内核**正确性测试加上真实硬件上的墙钟基准.
- **Gemini training throughput**测量每步的GPU秒.
  翻译: 中文**Gemini 训练吞吐量**测量每步的GPU秒数量.

在每个情况下,评估员发现了其他类型的LLM错误:假设的正确性要求,硬件上消失的性能要求和边缘故障.

> 在每种情况下,评估器捕获了否则将占主导地位的LLM错误类:虚假的正确声明,在硬件上消失的性能声明和边缘情况失败.

### 奖励改是这个论点的另一面

进化对评估器所测量的任何东西都进行了优化.如果评估器不完美,循环会发现不完美.在未经验证的域中,循环会对表面特征进行优化,而不是预期的行为.

> 进化优化评估器测量任何东西. 如果评估器不完美,循环会发现不完美的处境. 在未经验证的领域中,循环会优化表面特征而不是预期行为.

根据 DeepMind 的论文, AlphaEvolve 的成功只转移到评估者严格度符合搜索的野心的领域.

> 深度思维在论文中明确指出:AlphaEvolve的成功只能转移到评估器严谨性和搜索野心相匹配的领域.

具体的2025-2026年奖励黑客在代码搜索循环中:

> 奖励改的具体例子:

- 优化目标,以"完成时间"为回报,
  中文翻译:奖励"完成时间"的优化目标会奖励提交空解决方案。
- 基准分数是奖励正确性在测试中奖励的记忆测试和过度匹配.
  中文翻译:奖励测试正确的基准分数会奖励记忆测试和过拟合――
- 代码质量代理将删除评论和重写变量名称,
  中文翻译:"代码质量"代理会奖励删除注释和重写变量名,而没有语义变化──

对于"阿尔法发达"的解决方案:将一个经过审批的评估员发送到法师从未见过,在评估时产生的输入.

> 通过"深思熟虑"建议对任何提议的部署进行严格审查.

### 为什么LLM+搜索比单独使用胜得单独

专业知识学士可以产生可编译,语义上可行的修改.在2000行Python文件上的随机突变GA几乎总是产生语法错误.专业知识学士还集中在可行的邻居 (改变一个函数,而不是随机字节) 上搜索,这大大减少了浪费的评估者调用.

> 在2000 行Python文件上的随机变异GA几乎总是产生语法错误.LLM还将集中在合理的邻域 (转换一个函数而不是随机字节),这大大减少了浪费的评估器调用.

评价者反过来会发现LLM的论.LLM会自信地声称函数"在限度中是O(n log n") 当它实际上是O ((n ^ 2);一个墙钟基准使问题解决.

> 评估器反过来捕获LLM的虚构――LLM会自信地声称一个函数"极限下是 O(n log n)",而实际上是 O(n2);墙钟基准让问题尘埃落定――

### 在这个领域,AlphaEvolve 已经进入了前沿技术的位置.

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

它们都是相同的配方的变化:生成器加值器,循环.

> 它们是相同的配方变体:生成器加评估器,循环.
```figure
alphaevolve-loop
```

## 用它

## 用它实现框架

`code/main.py`通过一个玩具符号回归问题实现了类似AlphaEvolve的最小循环.

> `code/main.py`在一个玩具符号回归问题上实现了类似AlphaEvolve的最小循环.

"LLM"是一个 stdlib 代理,它为计算目标函数的程序提出了小的语法突变. "评估者"的测量意味着在保留的测试点上出现的二次错误.

> "LLM"是一个标准库代理,对一个计算目标函数程序提出了小语法变异.

观察:

> 观察:

- 如何在几代人中得到最佳成绩.
  中文翻译:最佳分数如何在世代中提升──
- 如何让各种解决方案保持活力,使循环不到当地最低点.
  中文翻译:MAP精英网格如何保持多样化解存活,让循环不收到局部最小化.
- 如何将延续的测试 (仅进行训练的评估者) 移除使循环非常适合.
  中文翻译:移除保留测试 (移除保留测试) 如何让循环灾难性地过拟合――

## 运送它.

`outputs/skill-evaluator-rigor-audit.md`在一个新领域考虑一个AlphaEvolve样式的循环的前提是:你的评估员是否真的能发现你关心的失败?

> `outputs/skill-evaluator-rigor-audit.md`对于新领域的考虑,类似于AlphaEvolve循环的前提条件:你的评估器真的抓住了你关心的失败吗?

## 练习题

1. 跑步`code/main.py`除置评器 (旗)`--no-holdout`量化过度适应.
   中文翻译:运行 `code/main.py`◎记录最佳分数轨迹──禁用保留评估器`--no-holdout`) 再运行――量化过拟合――

2. 阅读MAP精英格格的AlphaEvolve论文第3节.为一个新的问题 (例如编译器优化通过) 设计一个特征向量描述符,使搜索保持多样性.
   中文翻译:阅读 AlphaEvolve论文第3节关于MAP精英网格――为新问题 (例如编译器优化遍次) 设计一个保持搜索多样性的特征向量描述符――

3. 读取论文的附录F,并用三句话解释为什么对这个问题的评估器特别容易得到正确,以及为什么大多数领域不像它.
   中文翻译:48次乘法的4x4 结果在56年后改进了斯特拉森的49次乘法边界――阅读论文附录 F,使用三句话解释为什么这个问题特别容易做,以及为什么大多数领域不是这样的――

4. 提出一个领域, AlphaEvolve 失败,确定评估者在哪里断裂,以及为什么.
   中文翻译:提议一个 AlphaEvolve 会失败的领域――精确指出评估器在哪里失败以及原因――

5. 对于您所熟悉的域名,请写出您将使用的评估器签名.包括 (a) 准确性条件, (b) 性能指标, (c) 持久的输入生成规则, (d) 至少一个反奖励黑客检查.
   中文翻译:对你了解的一个领域,写出你会使用的评估器签名――包括 (a) 正确性条件, (b) 性能指标, (c) 保留输入生成规则, (d) 至少一个反奖励改检查――

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131)完整的报纸.
  中文翻译:完整论文。
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) 供应商的报表,结果.
  中文翻译:厂商撰文及结果──
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results)发现算法,包括48-mul 4x4matmul.
  中文翻译:发现的算法仓库,包括48次乘法的4×4矩阵乘法.
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6)前任系统.
  中文翻译:前身系统FunSearch。
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0)将评估者自主化作为一个关键的研究方向.
  中文翻译:将评估器约束的自主性作为关键研究方向.
