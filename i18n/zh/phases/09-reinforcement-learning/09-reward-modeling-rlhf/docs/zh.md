# 奖励模拟与RLHF

> 人类不能写一个奖励函数"好助手响应",但他们可以比较两个响应,选择更好的. 适应一个奖励模型,然后 RL语言模型对比它. 基督徒 2017. 指示GPT 2022. 食谱使GPT-3变成ChatGPT. 2026年它主要被DPO 取代,但心理模型仍然存在.

> **【中文解读】**人类无法为"好的助手回复"写奖励函数,但可以比较两个回复选更好.

> **【拓展：RLHF 是大模型对齐的关键】**基于人类反的强化学习) 是ChatGPT成功的核心技术──三步流程:(1) 监督微调 SFT;(2) 训练奖励模型 RM;(3) 用PPO 优化LM──DPO 简化第2-3步,但本质相同──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

你训练了一个语言模型,以下一个代币预测目标.它写着语法英语.它也说谎,乱,拒绝拒绝.你不能通过更多的预训来解决这个问题.

> 你在下一个标志上预测目标上训练了语言模型――它写出语法正确的英语――但它也会撒谎,跑题、拒绝不拒绝――你不能通过更多预训来修复网络文本是问题,不是解决办法――

您想要一个*scalar reward*,上面写着"A的反应比对 X的反应更好".写出奖励函数是不可能的."Helpfulness"不是一个封闭形式的表达式.但人类可以比较两个输出并标记一个偏好.

> 你想要一个*标志奖励*,表示"对于指令 X,回复 A 比 B 更好"――手写这个奖励函数是不可能的――"有用性"不是标志上式的关闭表达式――但人类可以比较两个输出和标志偏好――这可以低成本的大规模收集――

根据RLHF (Christiano et al. 2017; Ouyang et al. 2022) 将偏好转换为奖励模型,然后通过PPO来优化LM对付该奖励.在三个步骤中:SFT → RM → PPO.这是ChatGPT,Claude,Gemini和其他所有符合LLM在 20232025的配方.

> 通过PPO对LM进行优化. 三步:SFT → RM → PPO. 这就是推出ChatGPT、Claude、Gemini 和 2023-2025年每个对齐LLM的配方.

2026年,PPO步骤主要被DPO (Phase 10 · 08) 取代,因为它更便宜,几乎对对对齐调整效果很好.但*奖励模型*仍然是每个Best-of-N样本,每个RL-from-verifiable-rewards管道的基础,以及使用过程奖励模型的每个推理模型的基础.了解RLHF,你将理解整个对齐堆.

> 2026年,PPO 步骤大多被DPO 替代,因为更便宜且对齐效果几乎相同.但*奖励模型*仍然是最好的采样机,可验证奖励RL管道和过程奖励模型的基础.

> **【中文解读】**RLHF 三阶段流程:(1) SFT在人类示范数据上监督微调基础模型;(2) RM使用人类偏好对训练布拉德利-特里 奖励模型;(3) PPO使用奖励模型的信号优化语言模型,同时加上 KL 惩罚防止偏离SFT 太远.

> **【拓展：DPO 与 RLHF 的对比】**直接偏好优化) 将RLHF的RM+PPO 两步合并为一步直接从偏好对训练策略,无需显式训练奖励模型.数学上等于在布拉德利-特里模型下优化策略.

## 概念的核心概念

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**开始从预训练的基础模型. 精细调理人类写的目标行为示范 (遵循指示的反应,有用的答案等). 结果:一个模型 `π_SFT`虽然它是对良好的行为有偏见的,但仍然具有无限的行动空间.

> **阶段 1：监督微调（SFT）。**结果:一个*偏向良好行为*但仍然存在无限的动作空间的模型`π_SFT`,我知道.

**Stage 2: Reward Model training.**

- 收集对答案`(y_+, y_-)`为了得到提示`x`标记为"y_+ 优先于y_-."
- 培养一个奖励模式`R_φ(x, y)`给更高的分数`y_+`现在,我们要去.
- 损失:**Bradley-Terry pairwise logistic**其他:

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  由于BT是标准的,它是现代RLHF中的主导选择.

- `R_φ`转变器的背骨相同;单个线性层输出奖励.

> **阶段 2：奖励模型训练。**收集人类标志的偏好对`(y_+, y_-)`训练奖励模型给`y_+`更多的损失是布拉德利-特里的逻辑回归.`R_φ`通常从SFT模型初始化,加一个标量输出头.

**Stage 3: PPO against the RM with KL penalty.**

- 启动可培训的政策`π_θ`其他`π_SFT`保持一个结的 * 参考 *`π_ref = π_SFT`现在,我们要去.
- 答复结束时的奖励`y`其他:

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  克莱特的罚款阻止了`π_θ`由于自主而偏离`π_SFT`它是一个*规范性*的地区,而不是一个难以信任的地区.`β`通常`0.01`- 没有什么.`0.05`现在,我们要去.
- 运行PPO (课程 08) 通过此奖励.优势在代币水平轨迹上计算,但RM仅得分了全部响应.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**从`π_SFT`奖励 = RM 分数 - β × KL 到参考策略――KL 惩罚防止策略漂移太远――

**Why the KL?**没有它,PPO会很高兴找到奖励黑客策略. 人民币只在在分销完成中训练.`π_θ`机器在RLHF中最重要的单个.

> **为什么需要 KL？**没有它,PPO会找到奖励黑客策略RM只在分布式数据上训练――分布式的回复可能比任何人类编写的都高――KL 让`π_θ`保持在RM训练的流形附近──这是RLHF中最重要的旋转──

**2026 status:**

- **DPO**(拉法伊洛夫 2023):闭式代数崩 2+3阶段成为一个监督损失对偏好数据.没有RM,没有PPO.对计算的部分的对齐基准的质量相同.
- **GRPO**(DeepSeek 20242025):PPO以组相关基线而不是批评者,奖励来自*验证者* (代码运行 /数学答案匹配) 而不是人类训练的RM. 主导于推理模型.
- **Process reward models (PRMs):**评分部分解决方案 (每个推理步骤),用于RLHF和GRPO变体中的推理.
- **Constitutional AI / RLAIF:**通过一个合并的法定律师来生成偏好,而不是人类.

> **2026 年状态：**根据"法规"的规定,在"法规"中,将有"法规"的规定,在"法规"中,将有"法规"的规定,在"法规"中,将有"法规"的规定.

## 建立它,实现它.
```figure
reward-model
```

## 建立它

通过使用微小的合成"提示"和"反应"作为字符串.RM是线性得分符号表现.没有真正的LLM 管道的 *形状*是重要的,而不是规模.`code/main.py`现在,我们要去.

> 本课使用合成的小型"提示"和"回复"字符串.RM是基于词袋表示的线性评分器.

### 步骤1:合成优先数据

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

在真正的RLHF中,这些标签被人类标签所取代.`(prompt, preferred_response, rejected_response)`是相同的.

> 真实RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)`完全相同的.

### 步骤2:布拉德利-特里奖励模型

线性分数:`R(x, y) = w · bag(y)`减轻BT双日记损失:

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

经过几百次更新,`w`给好词标记赋予正面权重,给坏词赋予负面权重.

> 几百次更新后,`w`给好词符号 分配正权重,坏词 分配负权重.

### 步骤3:除了人民币外,PPO类似的政策

我们的玩具政策从词汇中产生一个代币.`log π_θ(token | prompt)`加入KL-to-reference罚款,并使用切割的PPO替代品.

> 我们的玩具策略从一个词表中产生单个代币.`log π_θ(token | prompt)`为了帮助他们,他们需要在线观看.

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键:奖励 = RM 分数 - β × KL(π_θ的 π_ref) ――β 是控制策略漂移程度的关键超参数太大策略几乎不变,太小则奖励黑客开始──

### 步骤4:监控KL

轨道平均值`KL(π_θ || π_ref)`如果它过去,`~5-10`政策已经远离了`π_SFT`低`β`这就是真正的RLHF的顶级诊断.

> 每次更新跟踪平均`KL(π_θ || π_ref)`如果超过`~5-10`策略已远离`π_SFT`可能 β 正在降低或奖励黑客正在开始.

### 步骤5:使用TRL的生产配方

一旦你明白了玩具的管道, 这里就像一个真正的图书馆用户写的循环.[TRL](https://huggingface.co/docs/trl)是参考实施`RewardTrainer`对于第二阶段和`PPOTrainer`对于第三阶段,

> 一旦你明白玩具流水线,这里是真实库用户编写相同的循环方式.`RewardTrainer`阶段3 用`PPOTrainer`,我知道.

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

图书馆为你做了三件事.`adap_kl_ctrl=True`执行适应β时间表:如果观察到的KL超过`target_kl`参考模型是按照惯例结的, 您不能意外地与`policy`价值率与政策的基础 (`AutoModelForCausalLMWithValueHead`由于TRL的数据显示,`policy/kl`其他`value/loss`单独的.

> 库为你做三个事情.`adap_kl_ctrl=True`实现自适应的调度:如果KL超过目标则 β 翻倍,如果低于一半则 β 减半.

## 陷

- **Over-optimization / reward hacking.**子是不完美的.`π_θ`发现高分但不佳的对立性完成. 症状:奖励无限上升,而人类评价分水平高或下降. 修正:早点停止,提高 `β`增加了训练数据.
  **过度优化/奖励黑客。**没有完美的 RM;`π_θ`发现抗性补充全分高但质量差――症状:奖励持续升但人类评估分数停滞或下降――修复:早停,提高 β、扩大 RM 训练数据――
- **Length hacking.**训练在有用的反应上,RM通常隐含地奖励长度.政策学习填补响应.补救:长度正常化的奖励,或RLAIF与长度意识的RM.
  **长度黑客。**在有用回复上训练的RM常隐式奖励长度──策略学会填充回复──缓解:长度归结奖励或长度感知RM──
- **Too-small RM.**只有一个小的RM才能准确地评分出口.
  **RM 太小。**低估率至少要和策略一样大.
- **KL tuning.**太低 β →漂移和奖励黑客.太高 β →政策几乎没有改变.标准技巧是*适应性* β 针对每步的固定 KL.
  **KL 调优。**太低→漂移和奖励黑客──β 太高→策略几乎不变──标准技巧是*自适应* β 目标为固定 KL──
- **Preference-data noise.**通过训练RM使用协议过数据或使用BT温度进行校准.
  **偏好数据噪声。**约30%的人类标签有噪音或模糊.
- **Off-policy problems.**监测剪辑分数,如第08课.
  **离策略问题。**后略离策略――像第08课那样监控裁剪比例――

## 用它实现框架

2026年RLHF是层次的:

> 2026年,RLHF是分层的:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

在2026年,生产配线管道将用于RM密集型或安全关键的步骤,仅用于DPO.

> 根据"中国人民共和国"的规定,在2022-2024年,

## 运送它.

保存如`outputs/skill-rlhf-architect.md`其他:

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## 练习题

1. **Easy.**训练布拉德利-特里奖励模型`code/main.py`在500个合成优先对上,对100个被持久对上,测量对准.应超过90%.
2. **Medium.**使用玩具PPO-RLHF循环运行`β ∈ {0.0, 0.1, 1.0}`对于每一个,图片的RM分数与KL参考更新.
3. **Hard.**根据相同的偏好数据实施DPO (闭式形式偏好概率损失),并在计算中使用的RLHF-PPO管道和最终RM分数中进行比较.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## 继续阅读 继续阅读

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)是RLHF创始人.
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) ChatGPT背后的食谱.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325)之前的RLHF进行总结.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290)                           
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)                  
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862)HH纸.
- [Hugging Face TRL library](https://huggingface.co/docs/trl)生产`RewardTrainer`其他`PPOTrainer`阅读训练人员来源,了解适应性KL和值值.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)通过三阶段管道的可行通行图表.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl)图书馆;`examples/`对于Llama,Mistral和Qwen,它有了端到端的RLHF脚本.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf)奖励假设观点;对于考虑奖励黑客的基本前提.
