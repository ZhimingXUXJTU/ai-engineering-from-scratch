# 政策级别 从零开始强化 策略梯度 从零开始实现强化

> 停止估值.直接参数化政策,计算预期回报的梯度,上升步骤.威廉姆斯 (1992) 在一个定理中写下.这就是为什么PPO,GRPO和每一个LLM RL循环都存在.

> **【中文解读】**计算期望回报的梯度和梯度上升――REINFORCE 定理告诉我们:`∇J(θ) = E[G · ∇log π_θ(a|s)]`,这是PPO、GRPO、以及所有大模型RL训练循环存在的原因.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

通过Q-学习和DQN来参数 *值*函数.`argmax Q`它们是对单独的操作和单独的状态来说很好的.`argmax`对于10维扭矩而言,`argmax`根据结构的决定性性.

> 通过 参数化*值*函数.`argmax Q`选择动作. 这对离散动作和离散状态没有问题.`argmax`需要随机策略时`argmax`没有什么可预测的.

政策梯度则为"政策"设定参数.`π_θ(a | s)`根据数据的数据,一个数据的分布在一个数据的分布中.`θ`走上山坡.`argmax`没有贝尔曼复发,只是梯度上升.`J(θ) = E_{π_θ}[G]`现在,我们要去.

> 策略梯度改为参数化策略`π_θ(a | s)`是一个输出动作分布神经网络.`θ`梯度──往上走──不需要`argmax`没有贝尔曼的需要.`J(θ) = E_{π_θ}[G]`升级上升.

强化定理 (威廉姆斯 1992) 告诉你,这个梯度是可计算的:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`运行一个集,计算返回,乘以`∇ log π_θ(a | s)`平均水平,梯度上升,完成.

> 威廉斯 1992年) 告诉我们这个梯度是可计算的:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`运行一个回合. 计算回报.`∇ log π_θ(a | s)`取平均――梯度上升――完成――

对于2026年每一个LLM-RL算法都是REINFORCE的完善.

> 2026年每一个LLM-RL 算法PPO、DPO、GRPO都是 REINFORCE 的精化.将掌握到肌肉记忆是本阶段剩余部分以及10期的前提.

> **【中文解读】**策略梯度的核心思想:直接优化策略参数 θ,让高回报的动作概率增加,低回报的动作概率减少.`∇log π`是"策略的方向指导数",乘以回报 G就是"沿着好的方向走".

> **【拓展：PPO→ChatGPT对齐】**通过使用PPO 算法,本质上就是 REINFORCE + 批评基线 + 信赖域剪剪.`loss = -advantage * log_prob`这一行代码,现在几乎所有2026年大模型RL训练脚本中都出现了.

## 概念的核心概念

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**任何政策`π_θ`参数为`θ`其他:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

在哪里`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`是从步骤的折扣回报`t`预期已经超过了完整的轨迹`τ`采集了`π_θ`现在,我们要去.

> **策略梯度定理。**任何事物`θ`参数化策略`π_θ`收益期望等于:收益折扣和乘以数量策略梯度的期望.`π_θ`采样完整轨迹上取.

**The proof is short.**区分`J(θ) = Σ_τ P(τ; θ) G(τ)`使用 `∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`原因是,我们在这个过程中,`log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`两个代数线给出了定理.

> **证明很短。**在期望下对`J(θ)`求导,使用数导技巧.`log P(τ; θ)`环境项目消失. 两行代数得到确定.

**Variance reduction tricks.**尼拉强化学品具有凶残的变化 回报很,`∇ log π`它们的产品非常杂.

> **方差降低技巧。**报道有很大的差异,`∇ log π`它们的噪音是更多的.

1. **Baseline subtraction.**取代`G_t`随着`G_t - b(s_t)`对于任何基线`b(s_t)`这不取决于`a_t`公正,因为`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`典型的选择:`b(s_t) = V̂(s_t)`经过评论家 →演员-评论家的学习 (课程07).
   **基线减法。**用`G_t - b(s_t)`替换`G_t`◎典型选择:`b(s_t) = V̂(s_t)`由评论家 学习 → 演员-评论家 (演员-评论家)
2. **Reward-to-go.**取代`Σ_t G_t · ∇ log π_θ(a_t | s_t)`随着`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`只有未来的回报对特定行动而言是重要的过去的回报贡献零平均噪音.
   **未来回报。**只有未来回报给定动作有意义的过去奖励贡献零平均值噪音.

结合起来,你得到:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

是A2C (课07),PPO (课08的直接祖先) 的基线.

**Softmax policy parameterization.**对于单独行动,标准选择:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

在哪里`f_θ`任何神经网络都能输出每次操作的分数.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

投资者: 投资者: 投资者: 投资者: 投资者:

> **Softmax 策略参数化。**对于分散动作,梯度形式简洁:所采取的动作分数减去策略下的期望值.

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`现在,我们要去.`∇ log N(a; μ, σ)`只有9期07期的SAC需要.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`这就是9期07期的SAC所需的全部.

## 建立它,实现它.
```figure
policy-gradient-landscape
```

## 建立它

### 步骤1:软max政策网络

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

对于图表包装,使用线性政策 (每动作一个权重向量).对于Atari,切换在CNN中并保持软max头.

> 对于Atari,换入CNN并保留软max头──

### 步骤2:采样和记录概率

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### 步骤3: 随着记录探测器的捕获,部署

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### 步骤4: 更新 REINFORCE

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

梯度`∇ log π(a|s) = e_a - π(·|s)`(其中一个是`a`软max的核心是软max的政策梯度.

> 梯度`∇ log π(a|s) = e_a - π(·|s)`(`a`软max 策略梯度的核心.

### 步骤5:基线

运行的平均值`G`为了使4×4 GridWorld运行,需要500个集集集.`V̂(s)`你会得到演员评论.

> 最近回合中`G`运营平均值足以让4×4 GridWorld 工作;约500回合收──将基线升级为学习的`V̂(s)`得到了演员评论.

## 陷

- **Exploding gradients.**总是正常化.`G`为了`~N(0, 1)`在乘以之前,`∇ log π`现在,我们要去.
  **梯度爆炸。**回报可能很大.`∇ log π`之前始终将`G`归一化到`~N(0, 1)`,我知道.
- **Entropy collapse.**政策过早收缩到近定决策行动,停止探索,陷入困境.`β · H(π(·|s))`实现目标.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境――修复:向目标添加奖励`β · H(π(·|s))`,我知道.
- **High variance.**尼拉 REINFORCE需要数千个集. 标准解决方案是批评基线 (课时07),或TRPO/PPO的信任区域 (课时08).
  **高方差。**基本的基础线 (Critical 基线) 课07或TRPO/PPO的信赖域 (Lesson08) 是标准修复.
- **Sample inefficiency.**政策上意味着你在一次更新后都会丢弃每一个过渡.通过重要样本取样,在变化成本下,通过政策外的纠正将数据恢复 (PPO的比例是减小 IS重量).
  **样本效率低。**在线策略意味着每次更新后丢弃所有转移.
- **Non-stationary gradients.**百集前的梯度使用旧的`π`政策方法每次更新都是因为这个原因.
  **非平稳梯度。**百回合前的梯度使用旧的`π`在线策略方法因此每隔几个月推出更新一次.
- **Credit assignment.**没有奖励,过去的奖励会产生噪音.
  **信用分配。**没有未来回报,过去的奖励贡献噪音――始终使用未来回报――

## 用它实现框架

在2026年,REINFORCE很少直接运行,但其梯度公式在各处:

> 据报道,在2026年,

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

当你读的时候`loss = -advantage * log_prob`整个论文 (DPO,GRPO,RLOO) 是此一行之上的一些变化降低技巧.

> 当你在2026年的训练脚本中读到`loss = -advantage * log_prob`现在,我们在这个代码上都在减少差距的技巧.

## 运送它.

保存如`outputs/skill-policy-gradient-trainer.md`其他:

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## 练习题

1. **Easy.**运用4×4 GridWorld上 REINFORCE 进行直线软max 政策. 训练1000集没有基线. 绘制学习曲线;测量变异 (回报的STD).
2. **Medium.**加入运行平均基线. 再次训练. 比较样本效率和变异与尼拉运行.
3. **Hard.**添加一个体奖金`β · H(π)`扫描`β ∈ {0, 0.01, 0.1, 1.0}`关于这个任务的甜点点是什么?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## 继续阅读 继续阅读

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696)原始的 REINFORCE 文件.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html)现代政策渐变定理与函数近似.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) 教科书的演示.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html)使用 PyTorch 代码的明确教学说明.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) 变化减少和自然梯度视图,将REINFORCE与信托区域家族 (TRPO,PPO) 联系起来.
