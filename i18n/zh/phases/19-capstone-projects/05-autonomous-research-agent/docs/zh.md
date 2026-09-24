# 卡普斯通05 自主研究代理 (人工智能科学家类)

> 萨卡纳的AI科学家-v2发表了完整的论文. 实验室经营了实验. 艾尔恩分享了痕迹. 2026 形状是计划执行验证实验的树搜索,预算成本,沙盒代码执行,视觉反的LateX编写器,以及一个自动 NeurIPS 风格的评论员组. 终点是建造一个,每张纸每期运行在30美元内,

> **【中文解读】**本节是综合项目构建自主研究代理,从文献检查到报告生成的完整流程.


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent + sandbox), LaTeX (output) | **语言:** Python（Agent + 沙箱）, LaTeX（输出）
**Prerequisites:** Phase 2 (ML), Phase 3 (deep learning), Phase 7 (transformers), Phase 10 (LLMs from scratch), Phase 14 (agents), Phase 15 (autonomous), Phase 16 (multi-agent), Phase 18 (safety)

>  **【前置】**顶点项目 05 = 综合几乎所有阶段(2/3/7/10/14/15/16/18);;自主研究代理 = 阶段15·05 的实战版。
>  **【类比】**自主研究代理 = "AI 研究生"。参考萨卡纳AI科学家-v2 / 艾伦AI / 代理实验室。架构:计划执行-验证 树搜索 + 预算约束 + 沙箱代码执行 + 视觉反 拉德克斯 写作 + 自动 NeurIPS 评审集团──挑战:每篇论文 <$30 + 抵御沙箱逃逸红队(萨卡纳 已记录) 。**前置知识:**阶段2 (ML),阶段3 (深度学习),阶段7 (Transformer),阶段10 (从头构建 LLM),阶段14 (Agent),阶段15 (自主系统),阶段16 (多 Agent),阶段18 (安全)
**Phases exercised:**它们是什么?**涉及阶段:**子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子
**Time:** 40 hours | **时间:** 40 小时

## 问题 问题引入

> **【中文解读】**本节描述自主研究代理的技术前沿――2026年萨卡纳AI的AI科学家-v2 在自然发表了AI 生成论文,通过学术同行评审.核心不是模型魔法,而是"规划执行验证"循环在有界预算下搜索实验树.难点在于循环设计,预算控制和安全性.萨卡纳团队记录了沙箱逃逸失败案例,你的代理必须通过同样的红队测试.

> **【拓展：AI-Scientist 系列】**萨卡纳AI的AI科学家-v1(2024) 首次展示了端到端自动科研流程,v2 进一步引入AB-MCTS风格的树搜索.ShinkaEvolve(ICLR 2026) 扩展到进化假设生成.AMD的代理实验室提供可复现实实验追踪.成本方面,v2 单篇论文控制在15-30美元,核心是每步预算估计和硬性终止.

自主研究机构在2026年超过了门. 萨卡纳AI的AI-Scientist-v2在自然杂志上发表了通过论文, 卡Evolve (ICLR 2026) 将这一线延伸到不断发展的假设. 美国麻醉剂实验室发送了可复制的痕迹. 代理人不是魔法,他们是一个计划执行验证循环, 运行在候选人实验的树上, 飞船是通报的,预算,安全故事.

> 自主研究代理在2026年跨越了一个门──Sakana AI的AI科学家-v2在自然上发表了通过研讨会同行评审的生成论文──ShinkaEvolve(ICLR 2026) 将扩展到进化假设──AMD的代理实验室发布可复制的追踪──这些代理不是魔法它们在候选实验树上运行的规划执行验证循环,有成本上限,绑定种子的沙箱和自动化评审──过程在循环,预算和安全叙述中.

通过在狭窄领域的种子想法中实现一个循环学习 (例如,在100M参数变压器上注意力-度的缩). 发现新东西不是最重要的. 价值在基础设施中:树木搜索,实验沙箱,作家-评论员循环,红团报告. 萨卡纳团队记录了逃离沙箱失败,你的代理必须通过同一个红色团队.

> 你通过在狭窄领域的种子想法 (例如,在1000亿参数变压器上注意力稀疏性消融实验) 实现一个循环来学习.

## 概念的核心概念

> **【中文解读】**自主研究代理的核心是最佳优先树搜索.节点是实验规格.设置+配置+代码+预期结果),扩展步骤生成小改动的子节点. 换优化器/调批次大小/消融组件. 每个子节点运行在带硬资源限制的沙箱中,结果反到评分函数. 新性 x质量 x 余额预算. 论文写作是视觉反的:生成 LaTeX → 编译 → 染色 PDF → 行 Opus 4.7 视觉模式评审局局和表安全.

> **【拓展：自动化论文评审】**评审集成使用5个不同的 LLM(Opus 4.7、GPT-5.4、Gemini 3 Pro、DeepSeek R1、Qwen3-Max),加权聚合打分,模拟NeurIPS 评审流程──平均值低于4.0/5则回回修改,最多3轮重写──视觉反循环是关键创新编译 PDF 后将染结果给VLM 检查图表清晰度、声明-证据对和版本布局,这一步将提高论文质量约15-20%──

代理是最好的第一棵树搜索. 节点是实验规格: (假设,配置,代码,预期结果). 扩展步骤建议小编辑 (换换优化器,换批量大小,拆除组件). 每个孩子都在一个新鲜的沙箱里跑着, 结果将返回一个分数函数,该函数将节点排列为 (新品 x 质量 x 剩余预算). 树长得很长,直到预算耗尽,然后最好的枝子被写出来.

> 代理是最佳优先树搜索.节点是实验规格:(假设,配置,代码,预期结果) 扩展步骤提出带有小编辑的子节点.

写作者是多元化. 它生成了Latex草案,编译,呈现数字,并将呈现的PDF重新输入Claude Opus 4.7的视觉模式,用于对布局,图像可读性和索赔证据的批评. 五名LLM法官组成的评审团发出NeurIPS类型的分数 (新奇性,严格性,清晰性,可复制性,影响);如果平均值低于门,则论文将与批评回归作者.

> 写作者是多模态的. 它生成了 LaTeX 草稿、编译、染图,并将染的 PDF 反给克劳德奥普斯4.7的视觉模式进行布局、图表清晰度和声明证据的齐齐批评.

安全性是承载性的.每一次实验都在E2B或Daytona沙箱中运行,没有网络出口,有界限的墙钟和固定资源限制.代理的代码生成步骤通过一个政策层来阻止逃离沙箱的系统调用.红团报告复制了萨卡纳文档的攻击表面 (叉子炸弹,文件系统逃脱,LLM编写的网络调用).

> 安全是承担的――每个实验都在无网络出口、有限的挂钟时间和固定资源限制的E2B或Daytona沙箱中运行――代理代码生成步骤通过一个策略层,阻止逃逸沙箱的系统调用――红队报告复现 Sakana 记录的攻击面(叉子炸弹、文件系统逃逸、LLM 编写的网络调用) ――

## 建筑,建筑

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

##  技术

- 配乐:有检查点和人机批准门的LangGraph
  中文翻译:乐团: 带有检查点和人批准门的长图
- 树的搜索:自定义最佳首次对实验节点 (从Sakana v2中的AB-MCTS风格)
  中文翻译:树搜索:自定义最佳首次对实验节点 (从Sakana v2中的AB-MCTS风格)
- 沙箱:每次实验的E2B,Docker-in-Docker倒退;通过cgroups的资源限制
  中文翻译:沙盒:每次实验的E2B,Docker-in-Docker倒退;通过cgroups的资源限制
- 文学:语义学家图 API + OpenAlex + 摘要的当地 FAISS缓存
  中文翻译:文学:语义学家图 API + OpenAlex + 摘要的当地 FAISS缓存

> 中文翻译:文学:语义学家图 API + OpenAlex + 摘要的当地 FAISS缓存(翻译)

- 作者: LaTeX模板 + Claude Opus 4.7 (视觉模式) 图像评论和布局
  中文翻译:作者:拉特克斯模板 + 克劳德奥普斯 4.7 (视觉模式) 图像评论和布局
- 评审员:由5名评委组成 (Opus 4.7,GPT-5.4,Gemini 3 Pro,DeepSeek R1,Qwen3-Max)
  中文翻译:评审员:由5名评委组成 (Opus 4.7,GPT-5.4,Gemini 3 Pro,DeepSeek R1,Qwen3-Max)

> 中文翻译:评审员:由5名评委组成 (Opus 4.7,GPT-5.4,Gemini 3 Pro,DeepSeek R1,Qwen3-Max)

- 实验框架:PyTorch 2.5用于物理实验,W&B用于伐木
  中文翻译:实验框架:PyTorch 2.5用于物理实验,W&B用于伐木
- 观察性: 长用于探测代理,每张纸张30美元的预算
  中文翻译:可观察性: 经纪人痕迹的长,每张纸张30美元的硬预算

## 动手构建
```figure
ce-experiment-tree
```

## 建立它

1. **Seed and domain scoping.**设置一个种子想法 (例如"研究1B变压器的注意力地图中的稀疏性模式").定义搜索空间:模型,数据集,计算预算.
   中文翻译:1. **Seed and domain scoping.**设置一个种子想法 (例如"研究1B变压器的注意力地图中的稀疏性模式").定义搜索空间:模型,数据集,计算预算.

2. **Literature pass.**查询50篇最引用的相关论文;缓存摘要本地;生成1页域名摘要.
   翻译: 翻译:**Literature pass.**查询50篇最引用的相关论文;缓存摘要本地;生成1页域名摘要.

3. **Tree scaffolding.**首先将根源与种子假设进行初始化.`expand(node) -> children`通过小编辑建议 (每孩子每次进行一个配置更改).`score(node)`作为一个权重的新品 x质量 x预算期限.
   翻译: 翻译:**Tree scaffolding.**首先将根源与种子假设进行初始化.`expand(node) -> children`通过小编辑建议 (每孩子每次进行一个配置更改).`score(node)`作为一个权重的新品 x质量 x预算期限.

4. **Sandbox wrapping.**每次实验都会运行.`docker run --network=none --memory=8g --cpus=2 --pids-limit=256 --read-only`种子被写入沙箱,输出只可读.
   翻译: 翻译:**Sandbox wrapping.**每次实验都会运行.`docker run --network=none --memory=8g --cpus=2 --pids-limit=256 --read-only`种子被写入沙箱,输出只可读.

5. **Plan-execute-verify loop.** `plan`让我知道.`execute`运行沙箱,捕获日志和指标. `verify`失败节点将存储在树上失败原因.
   翻译: 五.**Plan-execute-verify loop.** `plan`让我知道.`execute`运行沙箱,捕获日志和指标. `verify`失败节点将存储在树上失败原因.

6. **Writer.**预算后,选择最好的分支.用matplotlib生成数字.通过Claude Opus 4.7生成一个LateX草案,将分支的痕迹在文本中.编译.将编译的PDF返回Opus 4.7视觉进行评论.重复.
   翻译: 七个字**Writer.**预算后,选择最好的分支.用matplotlib生成数字.通过Claude Opus 4.7生成一个LateX草案,将分支的痕迹在文本中.编译.将编译的PDF返回Opus 4.7视觉进行评论.重复.

7. **Reviewer ensemble.**五名评委通过NeurIPS类型的标题评分草案 (新鲜性,严格性,清晰性,可复制性,影响性).如果平均值 <4.0/5,返回作者与批评. 3次重写后,硬停止.
   翻译:7.**Reviewer ensemble.**五名评委通过NeurIPS类型的标题评分草案 (新鲜性,严格性,清晰性,可复制性,影响性).如果平均值 <4.0/5,返回作者与批评. 3次重写后,硬停止.

8. **Red team.**构建或集成针对沙箱的反抗任务:叉子炸弹,网络泄密尝试,文件系统逃逸,LLM写的子元字符.确认所有被阻止.写出发现.
   翻译:8.**Red team.**构建或集成针对沙箱的反抗任务:叉子炸弹,网络泄密尝试,文件系统逃逸,LLM写的子元字符.确认所有被阻止.写出发现.

9. **Reproducibility.**每张纸都带着树木搜索的JSON,种子,W&B运行链接,沙盒配置,以及一个 README重复它.
   翻译:9.**Reproducibility.**每张纸都带着树木搜索的JSON,种子,W&B运行链接,沙盒配置,以及一个 README重复它.

## 用它使用方法

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

## 发射上线

`outputs/skill-ai-scientist.md`由于一个种子想法+一个域名+一个30美元的预算,它运行了整个管道,

> `outputs/skill-ai-scientist.md`提供种子想法+ 领域+30美元预算,它运行完整的管道并输出可审核的论文加可复现包.

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

## 练习题

1. 运行管道与同一领域的三个不同的种子想法进行比较. 树-搜索重叠的部分. 识别复制浪费计算.
   中文翻译:在同一领域对三个不同的种子的想法运行管道――比较树搜索的重叠部分――识别重复的浪费计算――

2. 在实验执行之前,为超过5美元的节点添加一个人-在循环的门.
   中文翻译:在预计超过5美元的节点实验执行前添加人工审批门.

3. 根据一系列已知坏报纸,测量假接受率.
   中文翻译:将评审集成换为单个评委――测量已知差论文保留集中的误会率――

4. 引入网络泄漏红团队测试: 代理编写试图`curl`确认一个外部地址.`--network=none`政策阻止了它.记录尝试.
   中文翻译:引入网络透红队测试:代理编写尝试`curl`确认  证据`--network=none`策略阻止它.

> 中文翻译:引入网络透红队测试:代理编写尝试`curl`确认  证据`--network=none`策略阻止它.记录尝试.


5. 根据您的树木搜索和一个平坦的随机基线 (相同的预算,没有扩张策略) 进行比较.
   中文翻译:将你的树搜索与平面随机基线比较(同样的预算,无扩张策略) 报告新性 x 质量增益

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Sakana AI-Scientist-v2 repository](https://github.com/SakanaAI/AI-Scientist-v2)参考生产研究机构
  中文翻译:参考生产研究代理
- [Sakana AI-Scientist-v1 paper (arXiv:2408.06292)](https://arxiv.org/abs/2408.06292)原始方法
  中文翻译:原始方法论
- [ShinkaEvolve (Sakana ICLR 2026)](https://sakana.ai)进化扩展
  中文翻译:进化扩展
- [Agent Laboratory (AMD)](https://github.com/SamuelSchmidgall/AgentLaboratory)多功能研究实验室框架
  中文翻译:多角色研究实验室框架
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)参考管弦层
  中文翻译:参考编排层
- [Semantic Scholar Graph API](https://api.semanticscholar.org/) 搜索文献
  中文翻译:文献搜索
- [E2B sandboxes](https://e2b.dev)参考实验隔离
  中文翻译:参考实验隔离
- [NeurIPS reviewer guidelines](https://neurips.cc/Conferences/2026/Reviewer-Guidelines)评审员组编码的条目
  中文翻译:评审集成编码的评分标准
