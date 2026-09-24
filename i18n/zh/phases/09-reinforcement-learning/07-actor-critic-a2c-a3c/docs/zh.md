# 演员评论家 演员评论家 演员评论家

> 强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强加强`V̂(s)`现在,我们可以看到一个值,从 A2C 运行它同步,A3C 运行它在线程.这两个是每个现代深度RL方法的心理模型.

> **【中文解读】**强大差距,但差距大幅下降. 这就是演员-批评PPO、SAC等所有现代深度RL方法的架构原型.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

尼拉反弹力有效,但它的变化是可怕的.`G_t`通过数量增加,我们可以在节目之间摆动10倍.`∇ log π`平均化产生了梯度估计器,需要数千个集,

> 强迫力有效,但差距很糟糕.`G_t`在回合间可能波动10倍.`∇ log π`平均而言,产生的梯度估计器需要数千次进行移动策略,以更少的DQN更新才能达到相同的效果.

如果减去基线,则将其从原始返回中取出.`b(s_t)`任何状态函数,包括学习值 预期保持不变,变异下降.最好的可处理的基线是`V̂(s_t)`现在数量乘以`∇ log π`是*优势*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报.`b(s_t)`任何状态函数,包括学习的值期望不变但方差降低.`V̂(s_t)`现在乘以`∇ log π`量就是优势

作为一个高于平均水平的收益,一个低于平均水平的收益是好的. 作为一个熟练的批评者,反复强化是*演员批评者*.批评者给演员一个低变量教师.这是2015年后的每一个深度政策方法 (A2C,A3C,PPO,SAC,IMPALA).

> 动作好如果产生高于平均回报;差如果低于――带学习批评的 REINFORCE 就是 *演员-批评*――批评给演员一个低方差的教师――这是2015年后每个深度策略方法(A2C、A3C、PPO、SAC、IMPALA) 』

## 概念的核心概念

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训,经过培训.
  **Actor** `π_θ(a | s)`策略:采样以行动:采用策略梯度训练:
- **Critic** `V_φ(s)`预计来自国家的回报.`(V_φ(s) - target)²`现在,我们要去.
  **Critic** `V_φ(s)`预期回报: 预期回报从状态中发出的估计.`(V_φ(s) - target)²`,我知道.

**The advantage.**两种标准表格:

> **优势函数。**两种标准形式:

- 果公司的优势`A_t = G_t - V_φ(s_t)`无偏见,更高的差异性.
  没有偏差,方差较高.
- 果的优势`A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`偏见性 (使用)`V_φ`),更低的变量.`δ_t`现在,我们要去.
  优势:* 有偏差(使用 `V_φ`),方差远低──也称为 *TD残差* `δ_t`,我知道.

**n-step advantage.**两者之间进行间接:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`纯粹的TD.`n = ∞`许多应用程序使用`n = 5`对于阿塔利,`n = 2048`对于 MuJoCo的PPO.

> **n 步优势。**在两者之间插值.`n = 1`只是一个特种.`n = ∞`是MC. 大多数实现了Atari.`n = 5`,我在上使用了PPO`n = 2048`,我知道.

**Generalized Advantage Estimation (GAE).**舒尔曼等人 (2016) 提出了对所有 n 步骤优势的指数权重平均值:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

随着`λ ∈ [0, 1]`现在,我们要去.`λ = 0`是TD (低差异,高偏差). `λ = 1`是MC (高差异性,无偏见性).`λ = 0.95`是2026年默认调调,直到偏差/变量拨号是你想要的.

> **【中文解读】**通过指数加权平均所有 n 步优势,在偏差和方差之间找到最优势平衡──lambda=0是纯 TD(低方差高偏差),lambda=1是纯 MC(高方差无偏差),lambda=0.95是 2026年默认值──GAE是 PPO的核心组件──

> **【拓展：GAE 在 RLHF 中的应用】**在LLM场景中",状态"是已生成的代币序列",动作"是下一个代币",奖励"来自奖励模型──GAE让PPO能在长文本生成中稳定训练,平衡即时奖励和长期回报──

**A2C: synchronous advantage actor-critic.**收集`T`跨越的步骤`N`通过平行环境计算每个步骤的优势 更新演员和评论家的组合. 重复. 简单,更可扩展的A3C兄弟.

> **A2C：同步优势 Actor-Critic。**在`N`个并行环境中收集`T`步──计算每步优势──在合并批次上更新 演员和评论家──重复──A3C的更简单,更可扩展的兄弟──

**A3C: asynchronous advantage actor-critic.**其他研究人员`N`工作者线程,每个操作一个环境.每个操作员在自己的推广上本地计算梯度,然后异步地将其应用到共享参数服务器上. 没有重复缓冲器需要. 工作者通过运行不同的轨迹来解关联. A3C证明你可以在规模上训练CPU. 在2026年,基于GPU的A2C (批量并行环境) 主导,因为GPU想要大批量.

> **A3C：异步优势 Actor-Critic。**其他 (2016) 开始`N`个工作线程,每个运行一个环境――每个工作线程在本地计算梯度,然后逐步应用到共享参数服务器――不需要回放缓冲区工作线程通过运行不同轨迹来相关――2026年,基于GPU的A2C占主导地位,因为GPU需要大量的.

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

政策渐进损失,价值回归,值奖金.`c_v ~ 0.5`现在`c_e ~ 0.01`它们是神圣的起点.

> **组合损失。**三项:策略 梯度损失 值回归 奖励`c_v ~ 0.5`,我知道.`c_e ~ 0.01`是典型的起始值.

> **【中文解读】**演员-批评组合损失 = 策略梯度损失 + 值函数归归 + 正则化――这些三项分别对应:让好的动作概率更大,让批评者更准确,防止策略过早缩小为确定性策略――

> **【拓展：GAE→PPO→RLHF】**广义优势估计 (GAE) 是PPO的核心组件,而PPO是ChatGPT RLHF训练的标准算法.

## 建立它,实现它.
```figure
actor-critic
```

## 建立它

### 步骤1:一个批评者

线性评论家`V_φ(s) = w · features(s)`更新与MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

在图表环境中,评论家在几百集中融合.在阿塔利上,用共享的CNN库 +值头取代线性评论家.

> 线性评论家`V_φ(s) = w · features(s)`在Atari上,换为共享CNN 主干+值头.

### 步骤2:n-步骤优势

考虑到长度的推广`T`起的决赛`V(s_T)`其他:

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`对于这些问题,我们必须要做出一些决定.`advantages`它们是什么乘法`∇ log π`现在,我们要去.

> `returns`是一个批评者.`advantages`是乘以`∇ log π`量量

### 步骤3: 综合更新

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

政策上,每次发布一次, 演员和评论家的学习率分开.

> 在线策略,每次更新一个推出,演员和评论员 使用不同学习率.

### 步骤4:并行 (A3C与A2C)

- **A3C:**转动起来`N`它们是个""的,它们是""的,它们是""的,它们是""的,它们是""的.
- **A2C:**跑步`N`集观察到一个过程中的实例`[N, obs_dim]`批量前进,批量后退,高GPU使用率,确定性,更容易推理.

我们的玩具代码是单线的,以便更清晰; 重写成批量A2C是三行的无线.

> 我们的玩具代码是单线的,以保持清晰度; 重写为批量A2C只需要三行编译.

## 陷

- **Critic bias before actor gradient.**如果评论家是随机的,它的基线是非信息性的,你正在训练纯粹的噪音. 在启动政策梯度之前,加热评论家几百步,或者使用缓慢的演员学习率.
  **Actor 梯度之前的 Critic 偏差。**如果评论是随机的,其基线没有信息量,你在纯噪音上训练――在开启策略梯度前前预热评论 几百步――
- **Advantage normalization.**实现每批次平均零/单位/STd的优势.
  **优势归一化。**每批次优势将归纳为零平均值/单位标准差距――几乎零成本下大幅稳定训练――
- **Shared trunk.**通过使用共享功能提取器,在影像输入中使用演员和评论家. 分开头.共享功能在两种输入中自由行.
  **共享主干。**图像输入时使用共享特征提取器. 分开头.共享特征同时从两个损失中获益.
- **On-policy contract.**更多的数据,你的梯度偏差 (重要样本纠正是PPO添加的).
  **在线策略约束。**据悉,A2C 恰好使用数据进行一次更新.
- **Entropy collapse.**没有`c_e > 0`几百次更新后,政策就会变得近乎决定性,
  **熵坍缩。**没有`c_e > 0`策略在几百次更新后变得近乎确定性并停止探索.
- **Reward scale.**优势大小取决于奖励规模. 规范奖励 (例如,运行-std 分类) 对于不同任务的一致梯度大小.
  **奖励尺度。**优势量级取决于奖励量级.

## 用它实现框架

它们是后来的建筑物,

> A2C/A3C 在2026年很少是最终选择,但它们是后来所有方法精确的架构:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

如果在2026年的一篇论文中看到"优势",

> 如果在2026年论文中看到"优势",就想到演员评论家.

## 运送它.

保存如`outputs/skill-actor-critic-trainer.md`其他:

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## 练习题

1. **Easy.**训练演员-批评者具有 MC优势 (`G_t - V(s_t)`根据第06课程的实验效率与REINFORCE与运行平均基线进行比较.
2. **Medium.**转向 TD残余优势 (`r + γ V(s') - V(s)`优势分组的差异量量.
3. **Hard.**执行GAE () 扫描`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`图案最终回报与样本效率. 这个任务的偏差/变异点是什么?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## 继续阅读 继续阅读

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783)A3C,原始的异步演员评论论文.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) 
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf)基础;与第9章关于函数近似的结合,当批评者是神经网络.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561)可扩展的分布式演员批评,可通过V-trace的政策外纠正.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/)生产A2C/PPO的实施值得阅读.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms)对两次度的演员-批评分解的基本融合结果.
