# ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

> 只有一个小的自我改善循环, 模型会产生一个思想链, 保持那些答案的正确答案, 这就是STAR. 通过V-STaR添加验证器,因此推断时间选择更好. 静静的STAR推出了合理性到每一个标志. 这三种都能. 循环保存了任何偶然的快捷方式,

> **【中文解读】**最小的自我改进循环隐藏在推理过程中:模型生成思维链,保留正确答案的推理过程,在这些数据上微调――这就是STaR──V-STaR 添加验证器改善推理时选择──静静的STaR将推理下沉至每个代币──三者都是有效的,但都不是魔法循环保留偶然得到正确答案的任何捷径──

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**斯塔尔系列是"自我博"训练的核心思路模型用自己的推理输出训练自己──OpenAI o1/o3 系列模型背后的强化学习训练就采用了类似的思路:生成多个推理路径,选择正确的,使用它们来改进模型──这是实现AI自我改进关键技术──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段13·01-03(CoT思维链) 阶段11·08(SFT 监督微调) 阶段15·01(长程代理框架) ・STaR是"自蒸 + 推理增强"的最小闭环──
>  **【类比】**学生自批评"――普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对的推理保留并自我再练一遍(自我生成训练数据) ――问题是:有时推理过程是错误的但答案巧合对对对对对对对,STaR会强化这种"对对"推理V-STaR加一个法官验证器) 掉错误推理.
> ️ **【易错点】**修复:使用过程奖励 (PRM,Phase 13·03) 替代结果奖励,每一步推理都打分;或使用V-STaR加验证器检查推理质量。

## 问题 问题 问题 问题 问题 问题 问题

让一个模型学习理性,最简单的方式是收集人类写的理性痕迹.

> 模型推理的直接方法是收集人类书写的推理轨迹.

问:如果模型写出自己的理性,并根据已知答案评分它们呢?

> 史塔尔 (StaR) 提出:如果模型自己编写推理过程并与已知答案对照评分会如何?循环是:


> **【中文解读】**通过代式自我训练提升LLM推理能力.核心思想:让模型产生推理轨迹,过高质量轨迹,使用这些轨迹微调模型,循环代.这是OpenAI o1/o3 系列和人类扩展思想的技术基础.

1. 试试一个推理跟答案.
2. 如果最后的答案是正确的,
3. 细节调整了保存的痕迹.
4. 复制.

虽然GSM8K和CommonsenseQA都没有新的人类注释,但循环有内置偏见:任何产生正确答案的逻辑都保留,无论逻辑本身是否是正确的.V-STaR (Hosseini等人,2024) 与学术验证器补丁;Quiet-STaR (Zelikman等人,2024) 将这个想法概括为特定的内部逻辑.

> 它有效. 在没有新人类标志的情况下,GSM8K 和 CommonsenseQA都有提升. 但循环有一个内置偏差:任何产生正确答案的推理过程都保留,无论推理本身是否合理.

## 概念的核心概念

### 启动了什么工作

开始从一个有点弱的推理能力的基础模型. 在每个训练问题上,取一个推理加答案. 如果答案匹配标签,保持 (问题,推理,答案) 三倍. 细节调整模型在保持的集. 重复.

> 从一个较弱推理能力的基础模型开始. 在每个训练问题上,采用一个推理过程加答案. 如果答案与标签匹配,保留问题.

模型如果永远无法解决问题,循环就无法学习.**rationalization**对于模型失败的问题,注入正确的答案作为提示,然后重新提示模型产生导致它的合理性.

> 如果模型永远不能正确回答一个问题,循环就无法从中学习.**合理化**对于模型失败的问题,将正确答案作为提示注入,重新提示模型产生向该答案的推理过程.

结果在原始论文 (Zelikman等人, 2022):GPT-J基模型通过重复STaR轮流从5.8%提高到10.7%通过合理化约5个百分点绝对.在 CommonsenseQA上,STaR训练的GPT-J 6B达到72.5%,与精细调整的GPT-3 175B (~73%) 相比.

> 原始论文的结果:GPT-J基础模型通过合理化重复STaR轮次,在 GSM8K上升从5.8%升至10.7%约5个百分点的绝对升级.在 CommonsenseQA上,STaR训练的GPT-J 6B达到72.5%,可与微调的GPT-3 175B (约73%),相比后者是手工标签推理训练大约30倍的模型.

### 通过DPO训练验证员

霍塞尼等人 (2024) 观察到这些也是数据:每对 (rationale, "这是正确的") 都可以训练验证器.他们使用直接偏好优化对正确和不正确的解决方案构建排名器.在推断时,取样N理性,选择验证器的最佳选择.

> 通过"这是否正确"的分析,可以训练验证器. 他们使用直接偏好优化 (DPO) 在正确和错误的解决方案上构建排名器. 在构建推理时,采样N 个推理并选择验证器排名最高的.

报告的特拉值:在GSM8K和MATH上,比以前的自我改进基线上+4至+17个百分点,大部分收益来自使用验证器进行推断时间选择而不是进行额外的发电机细节调整.

> 报告的提升:在GSM8K和 MATH上比之前的自我改进基线提升 +4 到 +17个百分点,大部分提升来自推理时选择验证器而不是额外的生成器微调.

### 静态STAR:每代币的内部理性

泽利克曼等人问:如果模型在每个代币位置上学习生成一个短的内部理性,而不仅仅是问题和答案之间呢?静静的STaR训练模型在每个预测代币之前发出隐藏的"想法",然后通过学习的权重将意识预测与基线预测混合.

> 泽利克曼等 (Zelikman et al.2024) 提出:如果模型学会在每个代币位置产生简短的内部推理,而不仅仅是在问题和答案之间?

结果:Mistral 7B在 GSM8K 上从5.9%提高到10.9%, CommonsenseQA 提高了36.3%到47.2%,没有具体任务的细节调整.该模型学会了"什么时候思考"硬代币得到更长的内部理性;简单代币几乎没有.

> 结果:在 GSM8K 上零样本中,Mistral 7B绝对从5.9%升至10.9%,在 CommonsenseQA上从36.3%升至47.2%,无需任务特定微调.

### 为什么三个人都担心安全

通过错误的推理来达到正确的答案,利用快捷方式,猜测或使用非通用模式,得到积极的加强.在分布式问题上,快捷方式工作.在分布式问题上,它默默地打破.

> 三种方法都用最终答案作为梯度信号.通过有缺陷的推理,达到正确答案的推理过程.

验证器通过学习对理性进行排名来缓解,但验证器受训在同一标签组上.它可以学习更喜欢格式良好的错误推理,而不是诚实的不确定性.更安全的设计是将STaR类型的数据结合 (a) 过程监督的奖励模型 (奖励中介步骤,而不仅仅是答案) 和 (b) 持续的OOD评估,破坏简单的快捷方式.

> 通过学习推理进行排名来缓解,但验证器是在相同标签集中训练的. 它可能会学会偏好形式的良好但错误推理而不是诚实的不确定性. 更安全的设计是将STaR风格的数据与 () 过程监督奖励模型 () 奖励中阶段,不仅仅是答案) 和 () 打破简单的捷径保留 OOD 评估相结合.

### 进行比较

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### 在2026年堆中,

塔尔已经老了. 但这种模式在2025年至2026年, 对于可验证的数学问题 (DeepSeek-R1,Kimi-k1.5,o1) 的RL是STaR的答案条件梯度信号,扩大. 过程奖励模型 (Lightman等人,2023年;OpenAI的"让我们一步一步验证") 是过程监督的替代方案. 编程程序评估器,而不是标签. 达尔文·戈德机器 (课4) 是特工架子本身的STaR.

> 太过老了.但这种模式在2025-2026年到处出现. 在可验证数学问题上的RL(DeepSeek-R1、Kimi-k1.5、o1) 是太过的答案条件梯度信号的放大版──过程奖励模型──Lightman等,2023;OpenAI的"逐步验证") 是过程监督的替代方案──AlphaEvolve(第3课) 是代码的太过,用程序评估器代替标签──达尔文·戈德尔机器──第4课) 是代理脚架本身的太过.

了解STaR使所有这些点击. 它是最小可行的自我改进循环.

> 了解STaR 让所有这些都说得通.

## 用它实现框架
```figure
reflection-loop
```

## 用它

`code/main.py`在玩具算术任务上运行模拟的STaR循环.

- 精度如何超越杆弹.
  中文翻译:准确率如何在启动轮次中升
- 模拟器包括一个"惰"的理性类, 40% 的时间得到了正确的答案,但很糟糕地概括.
  中文翻译:捷径如何潜入模拟器包含一个"惰"推理类,40%的时间得到正确答案,但泛化很差.
- 如何帮助推断,但不能完全剪除训练中引入的快捷方式.
  中文翻译:验证器 (V-STaR风格) 如何在推理时帮助但不能完全修剪训练期间引入的捷径──

## 运送它.

`outputs/skill-star-loop-reviewer.md`在训练之前,它可以帮助你审核一个提出的自学推理管道.

> `outputs/skill-star-loop-reviewer.md`帮助你在训练前审计提议的自我教学推理管道.

## 练习题

1. 运行模拟器. 设置快捷径频率为零,然后为0.4. 虽然两个运行之间的最终精度差异多大,但它们都在训练分布上达到90%以上?
   中文翻译:两次运行之间最终准确率分歧多少,即使两次在训练分布上都达到>90%?

2. 添加一个持续的OOD测试到模拟器中.从不同的分布中绘制问题,并评估在分发中和OOD组中启动的模型.量化差距.
   中文翻译:量化差距──

3. 阅读"静静的TAR"论文 (arXiv:2403.09629) 第3节.
   中文翻译:用三句话分别解释"思考结束"符号 和混合权重头――

4. 比较STaR的保持如果正确的过器与一个由过程监督的替代品,以独立奖励每个合理步骤. 确定标签成本差异和可行的质量差异.
   中文翻译:识别标标价差异和质量差异.

5. 设计一个评估,它会在部署的模型中捕获快捷方式理性. 它不必是完美的它必须打破一个STaR循环强化最简单的快捷方式.
   中文翻译:它只需要打破STaR循环的强化最简单的捷径.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## 继续阅读 继续阅读

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)原始的纸.
  中文翻译:原始论文。
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457)为推断时间选择添加了DPO验证器.
  中文翻译:添加DPO验证器用于推理时选择.
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629)每代币的内部理性.
  中文翻译:每符号内部推理。
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)过程奖励模型,替代梯度信号.
  中文翻译:过程奖励模型,替代梯度信号――
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948)                                                                                                                                                                                                                                                              
  中文翻译:可验证任务上的RL,STaR 扩展到前沿训练.
