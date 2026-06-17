# The Direct Preference Optimization Family | 优化家族 直接偏好

> Rafailov et al. (2023) showed RLHF's optimum has a closed form in terms of the preference data, so you can skip the explicit reward model and optimize the policy directly. That insight spawned a family — IPO, KTO, SimPO, ORPO, BPO — each fixing a failure mode of DPO. In 2026, direct alignment algorithms ship more frontier post-training runs than PPO. But the over-optimization curve from Lesson 2 still applies: DAAs do not escape Goodhart, they just move where it bites.

> **【中文解读】** 本节介绍了直接偏好优化（DPO）家族——绕过奖励模型直接从偏好数据训练的 RLHF 替代方案。Rafailov 等人（2023）证明 RLHF 最优解有关于偏好数据的闭式表达，因此可以跳过显式奖励模型。这个洞察催生了一个家族——IPO、KTO、SimPO、ORPO、BPO——每个都在修复 DPO 的某个失败模式。

> **【拓展：DPO 家族 → 现代 AI 训练】** 2026 年，直接对齐算法（DAA）比 PPO 在更多前沿后训练中部署。但 Lesson 2 的过度优化曲线仍然适用——DPO 并未逃脱古德哈特定律，只是改变了它攻击的表面。从"奖励模型过度优化"变成"参考策略比率过度优化"。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

> 🔗 **【前置】** 学本节前请先掌握：Phase 18·01-02（InstructGPT+古德哈特）、Phase 10·08（DPO 基础）。DPO 家族 = 绕过显式奖励模型直接从偏好数据训练。
> 💡 **【类比】** DPO = "去掉裁判的比赛"。RLHF = 训练裁判（奖励模型）+ 训练选手优化裁判评分；DPO = 直接用比赛结果（偏好对）训练选手。家族变体 IPO/KTO/SimPO/ORPO/BPO 都在修 DPO 不同缺陷。2026 DAA（直接对齐算法）比 PPO 部署更多。但古德哈特定律不变——只是从"奖励模型过度优化"挪到"参考策略比率过度优化"。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Derive the DPO closed form from the RLHF-with-KL optimum.
  中文翻译：从带 KL 的 RLHF 最优解推导 DPO 闭式解。
- State the failure mode each of IPO, KTO, SimPO, ORPO, BPO fixes in DPO.
  中文翻译：说明 IPO、KTO、SimPO、ORPO、BPO 分别修复了 DPO 的哪个失败模式。
- Distinguish "implicit reward gap" from "preference strength" and explain why IPO's identity mapping matters.
  中文翻译：区分"隐式奖励差距"和"偏好强度"，解释为什么 IPO 的恒等映射很重要。
- Explain why Rafailov et al. (NeurIPS 2024) prove DAAs over-optimize despite having no explicit RM.
  中文翻译：解释为什么 Rafailov 等人（NeurIPS 2024）证明 DAA 尽管没有显式 RM 仍然会过度优化。

## The Problem | 问题引入

The RLHF objective (Lesson 1):

> RLHF 目标（Lesson 1）：

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

has a known optimum:

> 有已知最优解：

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

So the reward is implicitly defined by the ratio of the optimal policy to the reference:

> 因此奖励由最优策略与参考策略的比率隐式定义：

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Substitute this into the Bradley-Terry preference likelihood and the partition function `Z(x)` cancels because it depends only on `x`. What remains is a loss in the policy parameters alone — no reward model needed. That is DPO.

> 将此代入 Bradley-Terry 偏好似然，配分函数 `Z(x)` 因只依赖 `x` 而抵消。剩下的是纯策略参数的损失函数——无需奖励模型。这就是 DPO。

The wrinkle: the derivation assumes the optimum is reachable, the preference data is in-distribution, and the reference policy is the true mode anchor. None of these hold exactly. Every family member fixes a different violated assumption.

> 问题在于：推导假设最优可达、偏好数据分布内、参考策略是真正锚点。这些假设在实践中都不完全成立。每个家族成员修复不同的违反假设。

## The Concept | 核心概念

> **【中文解读】** DPO 的推导：RLHF 目标有已知最优解 pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x,y)/beta)。将奖励表示为最优策略与参考策略比率的对数，代入 Bradley-Terry 偏好似然，配分函数 Z(x) 因只依赖 x 而抵消——剩下的是纯策略参数的损失函数，无需奖励模型。但推导假设最优可达、偏好数据分布内、参考策略是真正锚点——这些假设在实践中都不完全成立。

### DPO (Rafailov et al., 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

What can go wrong:

> 可能出什么问题：

- The implicit reward gap `beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)` is unbounded. A tiny preference can produce an arbitrarily large gap.
  中文翻译：隐式奖励差距无界。微小偏好可以产生任意大的差距。
- The loss drives chosen and rejected log-probs in opposite directions. It can push the chosen absolute log-prob down as long as the rejected falls faster. This is the Degraded Chosen Response phenomenon.
  中文翻译：损失驱动选择和拒绝的对数概率朝相反方向。只要拒绝的下降更快，它可以将选择的绝对对数概率推低。这是"退化选择响应"现象。
- Out-of-distribution preferences (rare rare pair vs rare rare pair) produce arbitrary implicit rewards.
  中文翻译：分布外偏好产生任意隐式奖励。

> **【拓展：IPO → DPO 的边界控制】** IPO（Identity Preference Optimization）用恒等映射替换 log-sigmoid，偏好差距被 1/(2*beta) 封顶。这解决了 DPO 的核心问题：微小偏好差异可能产生任意大的隐式奖励差距。在偏好强度变化很大的数据集上，IPO 比 DPO 更稳定。

### IPO (Azar et al., 2024)

Identity Preference Optimization replaces the log-sigmoid with an identity mapping on the preference probability. The loss becomes a squared-error on a bounded target:

> IPO 用恒等映射替换 log-sigmoid，偏好差距被 1/(2*beta) 封顶。这解决了 DPO 的核心问题：微小偏好差异可能产生任意大的隐式奖励差距。

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

The margin is bounded by `1/(2 beta)`. Preference strength and implicit-reward gap are proportional. No blow-up.

> 边界被 `1/(2 beta)` 封顶。偏好强度和隐式奖励差距成正比。不会爆炸。

> **【拓展：KTO → 无配对数据训练】** KTO（Kahneman-Tversky Optimization）的关键创新是完全放弃配对结构，只需要单个标记为"理想"或"不理想"的输出。这大大扩展了可用训练数据的范围——二进制反馈信号（点赞/踩）比成对偏好排序更容易获取。KTO 利用前景理论的损失厌恶原理，对"不理想"输出给予更大惩罚。

### KTO (Ethayarajh et al., 2024)

Kahneman-Tversky Optimization drops pairwise structure entirely. Given a single labeled output and a binary "desirable" or "undesirable" signal, it maps to a prospect-theory utility:

> KTO 完全放弃配对结构。给定单个标记输出和二元"理想"或"不理想"信号，它映射到前景理论效用：

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

with different weights for gains and losses (loss aversion). Benefit: you can use unpaired data, which is far more plentiful.

> 对收益和损失使用不同权重（损失厌恶）。好处：你可以使用非配对数据，这远比配对数据丰富。

> **【中文解读】** SimPO 移除了参考策略，用长度归一化的对数似然替代，加上边际 gamma 稳定训练。这直接解决了 DPO 的长度偏见失败模式——更长的 y_w 构造性地产生更大的对数概率差距。ORPO 更激进：将偏好项加到标准 SFT 的 NLL 损失上，单阶段从基础模型训练到对齐模型。BPO 则识别了"退化选择响应"问题——DPO 保留 y_w > y_l 排序但 y_w 的绝对对数概率可以下降。

### SimPO (Meng et al., 2024)

Simple Preference Optimization aligns the training signal with generation. Remove the reference policy entirely and normalize log-likelihood by length:

> SimPO 将训练信号与生成对齐。完全移除参考策略，用长度归一化对数似然：

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

with a margin `gamma` to stabilize. The length normalization removes the incentive to exploit DPO's length-bias failure mode (longer `y_w` gives a larger log-prob gap by construction).

> 加边际 `gamma` 稳定训练。长度归一化消除了利用 DPO 长度偏见失败模式的激励（更长的 `y_w` 构造性地产生更大的对数概率差距）。

### ORPO (Hong et al., 2024)

Odds-Ratio Preference Optimization adds a preference term to the standard SFT negative log-likelihood:

> ORPO 将偏好项加到标准 SFT 负对数似然上：

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

No reference policy — the SFT term is the regularizer. Train in a single stage from the base model to the aligned model. No separate SFT checkpoint.

> 无参考策略——SFT 项就是正则化器。单阶段从基础模型训练到对齐模型。无需单独的 SFT 检查点。

### BPO (ICLR 2026 submission, OpenReview id=b97EwMUWu7)

Identifies the Degraded Chosen Responses problem: DPO preserves the ranking `y_w > y_l` but the absolute log-prob of `y_w` can drop. BPO adds a single-line correction that penalizes downward moves on the chosen response. Reported +10.1% accuracy on Llama-3.1-8B-Instruct on math reasoning over DPO.

> BPO 识别了"退化选择响应"问题：DPO 保持 `y_w > y_l` 排序但 `y_w` 的绝对对数概率可以下降。BPO 添加单行修正，惩罚选择响应的向下移动。报告在 Llama-3.1-8B-Instruct 数学推理上比 DPO 提升 10.1% 准确率。

> **【拓展：DAA 过度优化 → 通用防御】** Rafailov 等人（NeurIPS 2024）在多个数据集和 KL 预算上训练 DPO、IPO、SLiC 策略。真实奖励与 KL 的曲线呈现出与 Gao 等人相同的先升后降形状。DAA 的隐式奖励在训练期间查询分布外样本，KL 正则化无法稳定这一点。通用修复——更好的数据、集成、早停——对 PPO 和 DPO 家族同样适用。

### The universal result: DAAs still over-optimize

Rafailov et al. "Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms" (NeurIPS 2024) trained policies with DPO, IPO, SLiC on multiple datasets across KL budgets. The gold-reward-vs-KL curves have the same Gao et al. peak-and-collapse shape. The implicit reward queries out-of-distribution samples during training; KL regularization does not stabilize this.

> Rafailov 等人在多个数据集和 KL 预算上训练 DPO、IPO、SLiC 策略。真实奖励与 KL 的曲线呈现出与 Gao 等人相同的先升后降形状。DAA 的隐式奖励在训练期间查询分布外样本，KL 正则化无法稳定这一点。

DAAs do not escape Goodhart. They change the surface where it bites from "reward model over-optimized" to "reference policy ratio over-optimized." The universal fix — better data, ensembles, early stopping — applies to both.

> DAA 并未逃脱古德哈特定律。它们只是将攻击表面从"奖励模型过度优化"变成"参考策略比率过度优化"。通用修复——更好的数据、集成、早停——对两者都适用。

> **【中文解读】** 2026 年的方法选择指南：有大量配对偏好数据 → DPO（保守 beta）或 SimPO（如有长度偏见）；有非配对二元反馈 → KTO；想要单阶段管线 → ORPO；DPO 日志显示选择概率下降 → BPO；偏好强度变化大且 DPO 饱和 → IPO。每个实验室在所有方法上跑完再按任务选优——数学推理和安全的最优方法可能不同。

### Choosing among them (2026)

- If you have large paired preference data: DPO with conservative beta, SimPO if length bias is evident.
  中文翻译：有大量配对偏好数据 → DPO（保守 beta），如有长度偏见用 SimPO。
- If you have unpaired binary feedback: KTO.
  中文翻译：有非配对二元反馈 → KTO。
- If you want a single-stage pipeline from a base model: ORPO.
  中文翻译：想要从基础模型的单阶段管线 → ORPO。
- If you see degraded chosen log-probs in DPO logs: BPO.
  中文翻译：DPO 日志中看到选择概率下降 → BPO。
- If preference strengths vary widely and DPO is saturating: IPO.
  中文翻译：偏好强度变化大且 DPO 饱和 → IPO。

Every lab runs all five on a battery and picks the winner per task. There is no reason the optimum is the same for math reasoning and safety.

> 每个实验室在所有方法上跑完再按任务选优。没有理由认为数学推理和安全的最优方法是同一个。

> **【拓展：DPO 家族实践 → 方法选择】** 2026 年每个前沿实验室在所有方法上跑完再按任务选优。没有理由认为数学推理和安全的最优方法是同一个。该 lesson 的 code/main.py 在偏好强度变化的玩具数据集上比较六种损失，绘制每种方法的最终胜率、选择概率漂移和隐式奖励分布。

## Use It | 用框架实现

`code/main.py` compares six losses (DPO, IPO, KTO, SimPO, ORPO, BPO) on a toy preference dataset where the true preference strength varies by pair. Each loss is optimized against the same 500-pair sample with a small softmax policy. Plots final win rate, chosen-log-prob drift, and implicit-reward spread per method.

> `code/main.py` 在偏好强度变化的玩具数据集上比较六种损失（DPO、IPO、KTO、SimPO、ORPO、BPO）。每种损失在相同 500 对样本上用小型 softmax 策略优化。绘制每种方法的最终胜率、选择概率漂移和隐式奖励分布。

## Ship It | 产出物

This lesson produces `outputs/skill-preference-loss-selector.md`. Given dataset statistics (paired vs unpaired, variable vs uniform preference strength, length distribution) and a target (single-stage or SFT-then-preference), recommend a preference loss and report the failure mode it protects against.

> 本课产出 `outputs/skill-preference-loss-selector.md`。给定数据集统计（配对 vs 非配对、可变 vs 均匀偏好强度、长度分布）和目标（单阶段或 SFT-后-偏好），推荐偏好损失并报告它保护的失败模式。

## Exercises | 练习题

1. Run `code/main.py`. Report the final chosen-log-prob drop for DPO and BPO. BPO should retain higher chosen absolute probability — verify this.
   中文翻译：运行 `code/main.py`。报告 DPO 和 BPO 的最终选择对数概率下降。BPO 应保持更高的选择绝对概率——验证这一点。

2. Modify the preference data so that all pairs have equal strength. Which of the six methods is most robust? Which degrades? Explain IPO's advantage here.
   中文翻译：修改偏好数据使所有配对强度相等。六种方法中哪个最鲁棒？哪个退化？解释 IPO 的优势。

3. Make the rejected responses on average 2x longer than chosen. Without changing anything else, show DPO's length exploitation numerically and SimPO's fix.
   中文翻译：使拒绝响应平均比选择响应长 2 倍。不改其他东西，数值展示 DPO 的长度利用和 SimPO 的修复。

4. Rafailov et al. (NeurIPS 2024) claim DAAs over-optimize. Reproduce a single-point version: plot chosen-minus-rejected KL divergence and observe over-optimization in DPO at large beta.
   中文翻译：Rafailov 等人（NeurIPS 2024）声称 DAA 过度优化。复现单点版本：绘制选择减拒绝的 KL 散度，观察 DPO 在大 beta 时的过度优化。

5. Read the BPO paper abstract (OpenReview b97EwMUWu7). Write down the one-line correction BPO adds to DPO. Confirm against the implementation in `code/main.py`.
   中文翻译：阅读 BPO 论文摘要（OpenReview b97EwMUWu7）。写下 BPO 对 DPO 添加的单行修正。对照 `code/main.py` 中的实现确认。

## Key Terms | 关键术语

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Further Reading | 延伸阅读

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  中文翻译：Rafailov 等人——DPO 原始论文
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) — IPO
  中文翻译：Azar 等人——IPO 论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  中文翻译：Ethayarajh 等人——KTO 论文
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  中文翻译：Meng 等人——SimPO 论文
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  中文翻译：Hong 等人——ORPO 论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  中文翻译：BPO——行为保持优化
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  中文翻译：Rafailov 等人——DAA 过度优化缩放定律
