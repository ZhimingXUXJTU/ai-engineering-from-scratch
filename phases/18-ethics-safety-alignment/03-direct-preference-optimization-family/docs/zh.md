# 直接偏好优化家族

> Rafailov 等人（2023）表明 RLHF 的最优解有关于偏好数据的闭式表达，因此你可以跳过显式奖励模型直接优化策略。这个洞察催生了一个家族——IPO、KTO、SimPO、ORPO、BPO——每个都在修复 DPO 的某个失败模式。2026 年，直接对齐算法比 PPO 在更多前沿后训练中部署。但 Lesson 2 的过度优化曲线仍然适用——DPO 家族并未逃脱古德哈特定律，只是改变了它攻击的表面。

> **【中文解读】** 本节介绍了直接偏好优化（DPO）家族——绕过奖励模型直接从偏好数据训练的 RLHF 替代方案。Rafailov 等人（2023）证明 RLHF 最优解有关于偏好数据的闭式表达，因此可以跳过显式奖励模型。这个洞察催生了一个家族——IPO、KTO、SimPO、ORPO、BPO——每个都在修复 DPO 的某个失败模式。

> **【拓展：DPO 家族 → 现代 AI 训练】** 2026 年，直接对齐算法（DAA）比 PPO 在更多前沿后训练中部署。但 Lesson 2 的过度优化曲线仍然适用——DPO 并未逃脱古德哈特定律，只是改变了它攻击的表面。从"奖励模型过度优化"变成"参考策略比率过度优化"。

**类型：** 学习
**语言：** Python（标准库，六种偏好损失比较器）
**前置条件：** Phase 18 · 01（InstructGPT）、Phase 18 · 02（奖励黑客）、Phase 10 · 08（DPO 基础）
**时间：** 约 75 分钟

## 学习目标

- 从带 KL 的 RLHF 最优解推导 DPO 闭式解。
- 说明 IPO、KTO、SimPO、ORPO、BPO 各自修复 DPO 的什么失败模式。
- 区分"隐式奖励差距"和"偏好强度"，解释为什么 IPO 的恒等映射很重要。
- 解释为什么 Rafailov 等人（NeurIPS 2024）证明 DPO 家族即使没有显式 RM 也会过度优化。

## 问题引入

RLHF 目标（Lesson 1）：

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

有已知最优解：

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

所以奖励由最优策略与参考策略的比率隐式定义：

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

将其代入 Bradley-Terry 偏好似然，配分函数 `Z(x)` 因只依赖 x 而抵消。剩下的是纯策略参数的损失——无需奖励模型。这就是 DPO。

问题在于：推导假设最优解可达、偏好数据在分布内、参考策略是真正的模式锚点。这些假设在实践中都不完全成立。每个家族成员修复不同的被违反的假设。

## 核心概念

> **【中文解读】** DPO 的推导：RLHF 目标有已知最优解 pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x,y)/beta)。将奖励表示为最优策略与参考策略比率的对数，代入 Bradley-Terry 偏好似然，配分函数 Z(x) 因只依赖 x 而抵消——剩下的是纯策略参数的损失函数，无需奖励模型。但推导假设最优可达、偏好数据分布内、参考策略是真正锚点——这些假设在实践中都不完全成立。

### DPO（Rafailov 等人, 2023）

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

可能出错的地方：

- 隐式奖励差距 `beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)` 无界。微小的偏好可能产生任意大的差距。
- 损失驱动选择和拒绝的对数概率朝相反方向移动。只要拒绝下降更快，它可以压低选择的绝对对数概率。这就是退化选择响应现象。
- 分布外偏好（罕见的 rare 对 vs rare 对）产生任意隐式奖励。

> **【拓展：IPO → DPO 的边界控制】** IPO（Identity Preference Optimization）用恒等映射替换 log-sigmoid，偏好差距被 1/(2*beta) 封顶。这解决了 DPO 的核心问题：微小偏好差异可能产生任意大的隐式奖励差距。在偏好强度变化很大的数据集上，IPO 比 DPO 更稳定。

### IPO（Azar 等人, 2024）

恒等偏好优化用恒等映射替换 log-sigmoid。损失变成有界目标上的平方误差：

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

边际被 `1/(2 beta)` 限制。偏好强度和隐式奖励差距成比例。不会爆炸。

> **【拓展：KTO → 无配对数据训练】** KTO（Kahneman-Tversky Optimization）的关键创新是完全放弃配对结构，只需要单个标记为"理想"或"不理想"的输出。这大大扩展了可用训练数据的范围——二进制反馈信号（点赞/踩）比成对偏好排序更容易获取。KTO 利用前景理论的损失厌恶原理，对"不理想"输出给予更大惩罚。

### KTO（Ethayarajh 等人, 2024）

Kahneman-Tversky 优化完全放弃配对结构。给定单个标记输出和二进制"理想"或"不理想"信号，它映射到前景理论效用：

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

对收益和损失使用不同权重（损失厌恶）。好处：你可以使用非配对数据，这要丰富得多。

> **【中文解读】** SimPO 移除了参考策略，用长度归一化的对数似然替代，加上边际 gamma 稳定训练。这直接解决了 DPO 的长度偏见失败模式——更长的 y_w 构造性地产生更大的对数概率差距。ORPO 更激进：将偏好项加到标准 SFT 的 NLL 损失上，单阶段从基础模型训练到对齐模型。BPO 则识别了"退化选择响应"问题——DPO 保留 y_w > y_l 排序但 y_w 的绝对对数概率可以下降。

### SimPO（Meng 等人, 2024）

简单偏好优化将训练信号与生成对齐。完全移除参考策略，按长度归一化对数似然：

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

加上边际 `gamma` 稳定。长度归一化消除了利用 DPO 长度偏见失败模式的激励（更长的 `y_w` 按构造产生更大的对数概率差距）。

### ORPO（Hong 等人, 2024）

赔率比偏好优化将偏好项加到标准 SFT 负对数似然上：

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

无参考策略——SFT 项是正则化器。从基础模型到对齐模型单阶段训练。无需单独的 SFT 检查点。

### BPO（ICLR 2026 投稿, OpenReview id=b97EwMUWu7）

识别退化选择响应问题：DPO 保持排序 `y_w > y_l` 但 `y_w` 的绝对对数概率可能下降。BPO 添加一行修正，惩罚选择响应上的向下移动。报告在 Llama-3.1-8B-Instruct 数学推理上比 DPO 准确率高 +10.1%。

> **【拓展：DAA 过度优化 → 通用防御】** Rafailov 等人（NeurIPS 2024）在多个数据集和 KL 预算上训练 DPO、IPO、SLiC 策略。真实奖励与 KL 的曲线呈现出与 Gao 等人相同的先升后降形状。DAA 的隐式奖励在训练期间查询分布外样本，KL 正则化无法稳定这一点。通用修复——更好的数据、集成、早停——对 PPO 和 DPO 家族同样适用。

### 普适结果：DPO 家族仍然过度优化

Rafailov 等人 "Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms"（NeurIPS 2024）在多个数据集和 KL 预算上用 DPO、IPO、SLiC 训练策略。真实奖励 vs KL 曲线有与 Gao 等人相同的先升后降形状。隐式奖励在训练期间查询分布外样本；KL 正则化不能稳定这一点。

DPO 家族没有逃脱古德哈特。它们只是改变了攻击的表面，从"奖励模型过度优化"变为"参考策略比率过度优化"。通用修复——更好的数据、集成、早停——两者都适用。

> **【中文解读】** 2026 年的方法选择指南：有大量配对偏好数据 → DPO（保守 beta）或 SimPO（如有长度偏见）；有非配对二元反馈 → KTO；想要单阶段管线 → ORPO；DPO 日志显示选择概率下降 → BPO；偏好强度变化大且 DPO 饱和 → IPO。每个实验室在所有方法上跑完再按任务选优——数学推理和安全的最优方法可能不同。

### 选择哪个（2026 年）

- 如果有大量配对偏好数据：DPO 配保守 beta，如长度偏见明显则用 SimPO。
- 如果有非配对二元反馈：KTO。
- 如果想要从基础模型的单阶段管线：ORPO。
- 如果 DPO 日志中选择对数概率下降：BPO。
- 如果偏好强度变化大且 DPO 正在饱和：IPO。

每个实验室在全部五种方法上跑完测试电池后按任务选优。没有理由数学推理和安全的最优方法是同一个。

> **【拓展：DPO 家族实践 → 方法选择】** 2026 年每个前沿实验室在所有方法上跑完再按任务选优。没有理由认为数学推理和安全的最优方法是同一个。该 lesson 的 code/main.py 在偏好强度变化的玩具数据集上比较六种损失，绘制每种方法的最终胜率、选择概率漂移和隐式奖励分布。

## 用框架实现

`code/main.py` 在玩具偏好数据集上比较六种损失（DPO、IPO、KTO、SimPO、ORPO、BPO），其中真实偏好强度因对而异。每种损失在相同的 500 对样本上用小型 softmax 策略优化。绘制每种方法的最终胜率、选择对数概率漂移和隐式奖励分布。

## 产出物

本课产出 `outputs/skill-preference-loss-selector.md`。给定数据集统计（配对 vs 非配对、偏好强度变化 vs 均匀、长度分布）和目标（单阶段或 SFT 后偏好），推荐偏好损失并报告它防止的失败模式。

## 练习题

1. 运行 `code/main.py`。报告 DPO 和 BPO 的最终选择对数概率下降。BPO 应保持更高的选择绝对概率——验证这一点。

2. 修改偏好数据使所有对有相同强度。六种方法中哪个最鲁棒？哪个退化？解释 IPO 在此的优势。

3. 使拒绝响应平均比选择长 2 倍。不改其他东西，数值展示 DPO 的长度利用和 SimPO 的修复。

4. Rafailov 等人（NeurIPS 2024）声称 DPO 家族会过度优化。重现一个单点版本：绘制选择减拒绝的 KL 散度，观察大 beta 下 DPO 的过度优化。

5. 阅读 BPO 论文摘要（OpenReview b97EwMUWu7）。写下 BPO 对 DPO 添加的一行修正。对照 `code/main.py` 中的实现确认。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------|---------|
| DPO | "没有奖励模型的 RLHF" | 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| 隐式奖励 | "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))`——DPO 隐含的奖励 |
| IPO | "有界的 DPO" | 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "非配对 DPO" | 带损失厌恶的单标签前景理论效用 |
| SimPO | "无参考 DPO" | 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "单阶段 DPO" | NLL + 赔率比偏好项；从基础模型一次通过训练 |
| BPO | "选择保留 DPO" | DPO 加上对降低选择响应绝对对数概率的惩罚 |
| 退化选择 | "选择下降" | DPO 降低选择对数概率，只要拒绝下降更快 |
| DAA | "直接对齐算法" | 任何跳过显式 RM 的偏好损失方法 |

## 延伸阅读

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) — IPO
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
