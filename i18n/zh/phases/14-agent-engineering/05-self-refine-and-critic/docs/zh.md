# 自我精炼和批判:反复的输出改进

> 自理修 (Madaan et al., 2023) 在一个循环中使用一个LLM在三个角色中生成,反,完善.平均收益:7项任务上+20绝对.CRITIC (Gou et al., 2023) 通过通过外部工具路由验证来加固反步骤.2026年,这种模式将在每个框架中作为"评估者优化器" (Anthropic) 或一个防护轨道循环 (OpenAI Agents SDK).

> **【中文解读】**通过外部工具进行验证步骤的强化. 搜索,代码解释器,计算器) 通过2026年成为每个框架的标志.

> **【拓展：CRITIC → Claude Code 的自我修复】**克劳德代码在编写代码后会自动运行测试证这是Critic模式的生产实现.

>  **【前置】**必须先过:阶段14·01(代理循环) 和阶段14·03(反思) ・自我清洗是反思的"单次任务内"版本(反思跨多次试验,自我清洗在一次生成内代) ・不理解反思存到记忆的"反思存到记忆"机制,会混自我清洗的"反不持久化"特征──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 状态自我清理的三个提示 (生成,反,精炼) 并解释为什么历史对精炼提示很重要.
  中文翻译:陈述自精的三个提示 (生成、反、精炼) 并解释为什么精炼提示的历史记录很重要.
- 解释Critic的关键见解:在没有外部依据的情况下,LLC在自我验证上是不可靠的.
  中文翻译:解释Critic的关键洞察:没有外部定,LLM 在自我验证上不可靠.
- 实现一个具有历史和可选的外部验证器的 stdlib 自定义循环.
  中文翻译:用标准库实现带历史记录和可选的外部验证器的自我清理循环.
- 绘制这个模式到安特罗皮克的"评估者优化器"工作流程和OpenAI代理SDK的输出防护窗口.
  中文翻译:将此模式映射到人类的"评估器优化器"工作流和OpenAI代理SDK的输出护──

## 问题 问题引入

代码可能有一个语法错误. 总结可能太长. 也许一个计划错过了一个边缘案例. 你想要的是: 代码批评自己的输出,然后修复它.

> 代理产生了一个几乎正确的答案――也许一行代码有语法错误――也许摘要太长了――也许一个计划遗漏了边缘情况――你想要的是:代理评价自己的输出,然后修复它――

简单的方法是通过单个模型,没有训练数据,没有RL来实现这一目标.但有一个问题:LLM在硬实实上自我验证方面很不好.

> 简单的自我验证能力很差. 临界界指出修复方案通过外部工具 (搜索码解释器,计算器,测试运行器) 通过验证步骤.

它们将在2026年实现反复改进的默认标准:生成,验证 (在可能的情况下,外部),完善,停止验证器通过时.

> 这两篇论文共同定义了2026年代改进的默认模式:生成、验证(尽可能外部验证)、精炼、验证通过则停止──

> **【中文解读】**自我清理的核心思想:一个模型扮演生成者,批评者,精炼者三重角色.但在硬实上,自我验证不可靠.

## 概念的核心概念

### 个人清理 (Madaan等, NeurIPS 2023)

一个法师,三个角色:

> 一个法学士,三个角色:

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

关键细节:`refine`报纸中指出:历史下降,质量急剧下降.

>  **【类比】**简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简单简**关键**必须把历史稿和批次一起给模型,否则模型会"忘记上轮指出的问题",陷入循环.

> ️ **【易错点】**常见 bug:只把"上一轮输出"给精炼,没有反.**后果**后输出重新引入反 指出的问题,陷入"指出问题→改→再指出→再改"的死亡循环──**一行修复**其他:`refine_prompt = task + output_0 + critique_0 + output_1 + critique_1 + ... + output_n`历史必须全量传入.

> 关键细节:`refine`能看到完整的历史 所有前面的输出和批评因此不会重复错误.论文对此进行消融实验:删除历史记录后质量急剧下降.

标题:平均在7项任务 (数学,代码,缩写,对话) 中实现+20的绝对改善,包括GPT-4.没有培训,没有外部工具,单一模型.

> 核心数据:在7个任务中平均绝对提升了20个百分点,包括GPT-4──无需训练──无需外部工具──单一模型──

### 评论 (Gou等人, arXiv:2305.11738, v4 Feb 2024)

对于事实性说法来说,这不可靠 (一种幻觉往往看起来令人信服的模型).`feedback(task, output)`随着`verify(task, output, tools)`在哪里`tools`包括:

> 对于事实性声明而言,这并不可靠.`verify(task, output, tools)`替代`feedback(task, output)`在其中`tools`包括:

- 搜索引擎寻找事实性索赔.
  中文翻译:用于事实声明的搜索引擎.
- 代码解释器,以确保代码正确.
  中文翻译:用于代码正确性的代码解释器──
- 算数计算器.
  中文翻译:用于算术的计算器.
- 域特定验证器 (单位测试,类型检查器,接器).
  中文翻译:领域特定验证器 (单元测试器,类型检查器,代码检查器)

验证器根据工具结果进行结构化批评,然后对此进行条件.

> 验证器产生基于工具结果的结构化评价.

标题:Critic在事实任务上优于Self-Refine,因为批评是基于地面的.在没有外部验证器 (创意写作,格式化) 的任务上,Critic将其降低到Self-Refine.

>  **【困惑】**答:因为Critic依赖于外部工具 (搜索,代码解释器,单元测试) 创意写作,邮件 色 这类任务没有"对错答案"可言,强行接入外部工具反而引入噪音.**事实类用 CRITIC，创造类用 Self-Refine**,我知道.

> 核心数据:CRITIC 在事实性任务上超越自我清理,因为批评是有依据的. 在没有外部验证器的任务上,创意写作、格式化),CRITIC 退化为自我清理.

### 停车条件

两种常见的形状:

> 两种常见形式:

1. **Verifier passes.**外部测试结果成功. 当可用时最好 (单元测试,类型检查器,防护断).
   翻译: 中文**验证器通过。**外部测试回归成功──在可用时优先单元测试、类型检查器、护断言)──
2. **No feedback issued.**价格更便宜,但不可靠; 配合最大.
   翻译: 中文**无反馈发出。**模型说"输出没问题"――更便宜但不可靠;配合最大代次数上限――

2026默认:结合它们. "如果验证器通过OR模型说好,停止,并且反复 >= 2 OR反复 >= max_iterations".

>  默认做法:组合使用:"如果验证器通过,或模型说没有问题且代次数 >= 2,或代次数 >=最大代次数,则停止.

### 评价者-优化器 (人类学, 2024)

亚当普奇的2024年12月的帖子将这列为五个工作流程模式之一.

> 人类2024年12月的文章将被命名为五种工作流模式之一.

- 评价者:评分产品并产生批评.
  中文翻译:评估器:对输出评分并产生批评.
- 优化器:根据批评,修改输出.
  中文翻译:优化器:根据批评修改输出.

循环直到评估器通过.这是Anthropic的框架中的自我清理/CRITIC.Anthropic补充说:评估器和优化器提示应该很大程度上不同,所以模型不仅仅是印.

> 循环直到评估器通过.这是人类的框架下自我精炼/批判.

### 开放AI代理SDK输出防护护

防护护是一个验证器,在代理的最终输出上运行.如果防护护出行 (升高)`OutputGuardrailTripwireTriggered`防护轨道可以调用工具 (CRITIC式) 或是纯函数 (Self-Refine式).

> 作为"输出护"提供. 护是代理 最终输出上运行的验证器.`OutputGuardrailTripwireTriggered`),输出被拒绝,代理可以重试.

### 2026 年陷

- **Rubber-stamp loops.**采用结构上不同的提示,或者采用较小的廉价模型来批评.
  翻译: 中文**橡皮图章循环。**同一个模型使用相同提示风格进行生成和批评会收到"看起来不错"――使用不同的结构性提示,或使用更小更便宜的模型进行批评――
- **Over-refinement.**每次精炼通过都增加了延迟和代币.预算1到3通过;之后,升级到人体审查.
  翻译: 中文**过度精炼。**每次精炼增加延迟和代币――预算 1-3轮;然后升级为人工审查――
- **CRITIC on trivial tasks.**如果没有外部验证器,Critic将退化为自行清理;不要为 stub验证器支付延迟.
  翻译: 中文**在简单任务上使用 CRITIC。**如果没有外部验证器,Critic 退化为自精;不要为验证器付出延迟代价.

## 建立它,实现它.
```figure
self-refine
```

## 建立它

`code/main.py`通过自定义和CRITIC在玩具任务中实现:制作一个特定主题的短弹名单.验证器检查格式 (3弹,每个小于60个).Critic添加一个外部的"事实验证器",惩罚已知的幻觉.

> `code/main.py`在一个玩具任务上实现自我清理和批判:给定主题生成短列表――验证器检查格式(3个要点,每个60字符以下) ・Critic 添加了已知幻觉的外部惩罚"事实验证器"――

组件:

> 组件:

- `generate`剧本制作人.
  翻译: 中文`generate`脚本生成器──
- `feedback` 法学士式的自我批评.
  翻译: 中文`feedback`LLM 风格自我批评.
- `verify_external` 基于基层的Critic类型验证器.
  翻译: 中文`verify_external`Critic 风格 定验器──
- `refine`重写输出给出历史.
  翻译: 中文`refine`根据历史重写输出
- 停止条件 验证器通过或最大4次代.
  中文翻译:停止条件 验证器通过或最多 4 次 代.

运行它:

> 运行:

```
python3 code/main.py
```

分析结果显示,自定义错误是因为外部验证器已经将自定义错误误误解读到.

> 比较自炼和批判运行――批判 捕获自炼遗漏的事实错误,因为外部验证器拥有没有自批的定依据――

## 用它实现框架

安特罗皮克的评估器优化器是这种模式的克劳德友好的语言.OpenAI Agents SDK的输出护是Critic形状的 (护可以调用工具).LangGraph发送一个反射节点,读起来像自定义.谷歌的Gemini 2.5计算机使用添加一个每步安全评估器,这是一个Critic变体:每一个操作都在提交之前被验证.

> 基于CLAUDE 友好语言表达的模式,OpenAI代理SDK的输出护是Critic形式的 (可调用工具).长图提供类似于自我清理的反思节点.Google的双子 2.5计算机使用添加了每步安全评估器,这是一个Critic变体:每个动作都在提交前经历过验证.

## 运送它.

`outputs/skill-refine-loop.md`设置评估器优化器循环,以任务形状,验证器可用性和代预算. 发出生成器,评估器/验证器和优化器的提示,加上停止政策.

> `outputs/skill-refine-loop.md`根据任务形状,验证器可用性和预算配置评估器-优化器循环,输出出生成器,评估器/验证器和优化器的提示以及停止策略.

## 练习题

1. 运行玩具的最大_率=1. 评论仍然有帮助吗?
   中文翻译:用 max_iterations=1运行――Critic 仍然有帮助吗?
2. 换一个噪音的外部验证器 (随机30%的假正值).循环是什么?这是大多数护堆的2026现实.
   中文翻译:将外部验证器替换为杂的版本.
3. 实施"不同模型的生成器批评"变体:大模型生成,小模型批评. 它是否超过相同的模型?
   中文翻译:实现"不同模型的生成-批评"变体:大模型生成,小模型批评――比同模型更好吗?
4. 阅读Critic Section 3 (arXiv:2305.11738 v4). 举个证实工具类别,并为每一个类别举一个例子.
   中文翻译:阅读Critic 第3节.
5. 图片OpenAI代理SDK的`output_guardrails`什么是 SDK 错误的,什么是正确的?
   中文翻译:将OpenAI代理 SDK 的 `output_guardrails`映射到Critic的验证器角色.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## 继续阅读 继续阅读

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651)法典论文
  中文翻译:自我精炼 经典论文自我精炼代改进。
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738)基于工具的验证
  中文翻译:Critic工具定验证──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)评估者-优化器工作流程模式
  中文翻译:人类学 关于构建有效代理的指导评估器-优化器工作流模式
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)作为Critic型验证器的输出护
  中文翻译:OpenAI代理 SDK 文档输出护作为Critic形式的验证器──
