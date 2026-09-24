# 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中的强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习 游戏中强化学习

> 1992年:TD-Gammon在纯TD后游中击败了人类冠军. 2016年:AlphaGo击败了Lee Sedol. 2017年:AlphaZero从零开始主导了象棋,肖吉和GO. 2024年:DeepSeek-R1证明了相同的配方,GRP取代了PPO,基于推理.游戏是推动这一阶段的每一个突破的基准.

> **【中文解读】**游戏是RL突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025) ――DeepSeek-R1 证明了 AlphaZero的"自我博+搜索+策略改进"循环可以直接用于大模型的数学推理代币就是动作,验证器就是"赢/输"信号――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## 问题 问题引入

游戏拥有RL想要的一切. 清洁的奖励 (胜负). 无限的集 (自动游戏重置). 完美的模拟 (游戏 *是*模拟器). 微小或连续的行动空间. 多代理结构,强迫对手的强度.

> 游戏拥有RL所需的一切──清晰的奖励──无限回合──自我博重置──完美仿真──游戏*就是*仿真器──离散或小型连续动作空间──迫使对抗鲁棒性的多智能体结构──

游戏是每个主要的RL突破都被测试的方法. 果 (背, 1992). 根据"中国"的规定, 其他类型: 果产品 开放AI五 (第2号) 星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星际星 泽罗 (学习模型,2019) 子 (矩阵乘法,2022年) 根据"国际数据"的规定, 最新的证明,游戏RL技术在文本上工作.

> 游戏是每个RL重大突破的试验场. 游戏是每一个RL重大突破的试验场. 游戏是TD-Gammon ((西洋双陆棋,1992) 游戏是Atari-DQN(2013年) 游戏是AlphaGo(2016) 游戏是AlphaZero 游戏是2017年 (AlphaZero) 游戏是OpenAI Five (AlphaStar) 游戏是星际争 II,2019) 游戏是MuZero 学习模型,2019) 游戏是AlphaTensor 矩阵乘法,2022年 (AlphaDev) 排序算法,2023年 (DeepSeek-R1 数学推,2025年) 游戏是最新的证明:RL 技术可以用于文本.

这块顶石通过一个统一镜头来测试了三个具有里程碑意义的建筑:**self-play + search + policy improvement**每个都将前一个概括起来;特别是GRPO是AlphaZero的配方,用于LLM推理,作为行动的代币和数学验证作为胜利信号.

> 这个总结通过单一统一视角**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO──每个都是前一个推广;GRPO 特别是将 AlphaZero 的配方应用于 LLM 推理,代码是动作,数学验证是获胜信号──

## 概念的核心概念

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**银等. 根据已知规则的游戏 (象棋,肖吉,戈):

- 政策价值网络:一个塔`f_θ(s) → (p, v)`现在,我们要去.`p`法律行动的先驱.`v`游戏的预期结果.
- 果树搜索 (MCTS):每次移动,扩展一个可能的延续的树. 使用 `(p, v)`按 UCB (PUCT) 选择节点: `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`现在,我们要去.
- 玩自己游戏:玩代理对代理.`t`士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,士,`π_t`成为政策培训目标.
- 损失:`L = (v - z)² - π · log p + c · ||θ||²`现在,我们要去.`z`是游戏结果 (+1 / 0 / -1).

没有人知道,没有手工修复,只有一个食谱, 掌握了几万个自动游戏的棋牌,肖吉和戈.

> 零人类知识――零手工启发式―― 一种配方在数百万个自我博后掌握国际象棋,棋牌和围棋――

**MuZero (2019).**施里特维泽等. 取消了规则的要求.

- 学习一个置动态模型`(h, g, f)`其他:
  - `h(s)`编码观察到隐形状态.
  - `g(s_latent, a)`预测下一个潜伏状态 + 奖励.
  - `f(s_latent)`预测政策前值.
-  MCTS在"学习的隐藏空间"中运行.
- 运行在棋牌,棋牌,肖吉和阿塔利,一个算法,没有规则知识.

> 在围棋,国际象棋,棋牌和阿塔利上都有效一个算法,无需规则知识

> **【中文解读】**通过学习隐藏空间动力学模型消除了这一限制. 这一"自我博+搜索+策略改进"循环直接启动了DeepSeek-R1的推理训练用可验证奖励替代游戏胜负信号.

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**通过测试,测试是否通过测试) 是"胜负信号"――GRPO 替代PPO,组内采样替代自我博――这证实了游戏AI的方法论可以转移到大模型推理训练――

**Stochastic MuZero (2022).**增加了动力和机会节点; 扩展到后游类游戏.

> **随机 MuZero (2022)。**添加随机动力学和机会节点;扩展到双陆棋类游戏.

**Muesli, Gumbel MuZero (2022-2024).**样品效率和确定性搜索的提高.

> **Muesli、Gumbel MuZero (2022-2024)。**样本效率和确定性搜索的改进.

**GRPO (2024-2025).**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

- "游戏":回答数学/编码/推理问题. "Win" =验证器 (测试案例通过,数值答案匹配) 返回1.
- 政策:法师. 行动:代币. 状态:快速+反应-迄今.
- 没有批评者 (PPO式V_φ).`G`根据政策的完成,每一个收费的收费.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`作为REINFORCE类型更新的信号.
- 根据"海上海域"的规定,海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域海域.
- 完全损失:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

没有奖励模型,没有批评者,没有MCTS. 组相关基线取代了所有三个. 在计算的部分情况下,在推理基准上匹配或超过PPO-RLHF质量.

> **GRPO (2024-2025)。**探-R1 配方──同样的 AlphaZero 形状循环,应用于语言模型推理:不需要奖励模型、批判或MCTS──组相对基线替代了三者──在推理基准上匹配或超越PPO-RLHF质量,计算量仅为一小部分──

> **【中文解读】**GRPO 是DeepSeek-R1的核心创新:不需要批评网络 (省一半内存),使用组内平均值和标准差构建优势.对每个问题采样 G 个回答,正确回答的优势为正确的概率),错误的负面的概率降低的概率.

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**深度寻找R1的四阶段训练流程:冷启动SFT → 推理导向GRPO → 拒绝采样+SFT → 全谱GRPO──R1-Zero(纯GRPO 无SFT) 证明了LLM可以从零学会推理,但输出可读性差量──蒸实验表明:使用强 RL教师的推理轨迹做SFT,比小模型从头做 RL效果更好──

**The R1 recipe in full.**根据该报告,该报告的内容包括:

> **R1 完整配方。**探R1是论文中的两个模型:

- **R1-Zero.**从DeepSeek-V3基模型开始.没有SFT.直接使用两个奖励组件应用GRPO: *准确性奖励* (基于规则的是否对最终答案进行了正确的解析,/代码是否通过单元测试) 和 *格式奖励* (完成是否包裹了其思想链在`<think>…</think>`通过数千个步骤,平均响应长度从100到10,000个代币,数学基准分数升到接近o1预览水平.该模型从零开始学习推理.缺点:它的思想链往往是不可读的,语言混合,缺乏风格抛光.
- **R1.**通过四阶段管道来解决R1-Zero的可读性问题:
  1. **Cold-start SFT.**收集几千个长时间的CoT示范, 进行清洁格式化, 监督, 调整它们的基模型. 这就给出了可读的起点.
  2. **Reasoning-oriented GRPO.**应用GRPPO,加上准确性+格式奖励以及*语言一致性*奖励,以防止代码交换.
  3. **Rejection sampling + SFT round 2.**从RL检查点采样600K的推理轨迹,只保留具有正确的最终答案和可读的CoT的轨迹,并将其结合到200K的非推理SFT例子 (写作,质量检查,自我认知).再次调整基础.
  4. **Full-spectrum GRPO.**另一个RL轮,涵盖了推理 (基于规则的奖励) 和一般的调整 (基于有用性/无害性偏好的奖励).

结果与AIME和 MATH-500的o1相匹配,并且足够小,可以蒸.同样的论文还通过SFT'ing对R1的推理痕迹进行释放六种蒸密集模型 (Qwen-1.5B到Llama-70B).学生没有RL.强大的RL教师的蒸始终从零开始击败RL.

> 结果在AIME 和 MATH-500 上匹配 o1,且足够小可以蒸──蒸强 RL 师的推理轨迹始终优于学生规模的从头 RL──

**Why GRPO instead of PPO for reasoning.**根据DeepSeekMath论文 (Feb 2024) 的三个原因: (1) 没有值网络训练,将记忆减半; (2) 组基线自然处理了推理任务产生的稀少轨迹结尾奖励; (3) 每次调整使得不同难度的问题中的优势相对而易见,这是PPO的单独批评者无法做到的.

> **为什么推理用 GRPO 而非 PPO。**三个原因: 1) 无需训练值网络,内存减半; 2) 组基线自然处理推理任务产生的稀疏回合末奖励; 3) 每个提示归结使优势在难度差异巨大的问题间可比较――

**Search-free vs search-based.**游戏分类:

> **Search-free vs search-based.**

- *长视野的完美信息游戏* (Go,棋牌):仍然基于搜索.
- *LLM推理*:目前还没有 MCTS; GRPO在完整的推广,最好的推理计算.过程奖励模型 (PRM) 暗示了阶段级搜索被添加回来.

## 建立它,实现它.
```figure
f3-selfplay-ladder
```

## 建立它

编码在`code/main.py`实现**GRPO in miniature**一个具有多组样品的强盗.算法与LLM相同;只有政策和环境更简单.它教导了*损失*和*团体相对优势*,即2025年的创新.

> `code/main.py`中代码实现**微型 GRPO**一个具有多组样本的博机. 算法与LLM上相同;只是策略和环境更简单.

### 步骤1:一个小的验证器环境

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

在真正的GRPO中,验证器执行单位测试或检查数学等式.

> 真实GRPO 中验证器运行单元测试或检查数学等式──

### 步骤2:政策:每提示的软max超过K答案代币

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

相当于一个即时的LLM的最终层输出.

> 士学位的最后一层出口.

### 阶段3:集团采样和集团相对优势

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

根据"基线"的定义,该组的平均值是"基线"的平均值,而正常化则使用"基层" (group std).

> 组相对优势是2024年深度搜索的技巧.

### 步骤4:与REINFORCE基线 (无价值) 进行比较

它们的设置和计算相同, 它们的复核能力也相同.

> 类似设置,相同计算量,纯强加力.

### 步骤5:观察和KL

根据"RLHF"的诊断, 平均KL是指标,政策透,奖励过时间.

> 与RLHF相似的诊断:平均KL到参考策略,策略,奖励随着时间的变化.

## 陷

- **Reward hacking via verifier gaming.**经验者可能会发现实验者是错误的或可利用的.
  **通过验证器博弈的奖励黑客。**由于这些问题,我们必须要做出一些决定.
- **Group size too small.**基因基因变异是`1/√G`在下面`G = 4`优势信号是噪音的;标准选择是`G = 8`为了`64`现在,我们要去.
  **组大小太小。**组基线的方差与`1/√G`现在,我还在做.`G = 4`下面有噪音的优势信号;标准选择是`G = 8`到了`64`,我知道.
- **Length bias.**通过代币计数正常化,或使用序列级日志检查,或缩小到最大长度.
  **长度偏差。**不同长度的LLM 完成有不同的对数概率.
- **Pure self-play cycles.**球运动的总数可以被各种对手游泳池减轻 (联盟比赛,10课).
  **纯自我博弈循环。**通过多样化对手池缓解.
- **Search-policy mismatch.**如果政策网太小,不能代表搜索的分布,训练站.
  **搜索-策略不匹配。**训练策略模仿搜索输出. 如果策略网络太小不能表示搜索分布,训练停滞.
- **Compute floor.**子/阿尔法零需要大量的计算.一个单个的除通常需要数百个GPU-小时.小型演示程序 (例如,AlphaZero在连接四) 为学习而存在.
  **计算下限。**需要大量计算. 单次消耗通常需要数百个GPU 小时.
- **Verifier coverage.**通过一个错误解决方案的单元测试,加强了错误. 设计验证器,
  **验证器覆盖。**通过有 bug 解决方案的单元测试将强化 bug 设计能够捕获边缘情况的验证器

## 用它实现框架

游戏-RL2026年景观,按领域:

> 根据领域:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

食谱* 自动玩,搜索增强改进,政策蒸 跨越文字,像素和物理控制.

> 这种方法*自我博"",搜索增强改进"",策略蒸蒸跨文本"",像素和物理控制"",GRPO是最新的例子;更多即将到来──

## 运送它.

保存如`outputs/skill-game-rl-designer.md`其他:

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## 练习题

1. **Easy.**执行 GRPO 强盗在`code/main.py`训练用2个提示 ×4个答案代币.  konverge 在<1000个更新中`G=8`现在,我们要去.
2. **Medium.**入PPO (剪切) 和尼拉 REINFORCE. 比较样品效率和奖励差异与GRPO在同一名强盗.
3. **Hard.**扩展到长度-2的"推理链":代理发出两个代币,验证者奖励对.测量GRPO如何处理两个步骤的序列中信用分配. (提示:计算组优势每 *完整序列*,扩散到两个代币位置).

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## 继续阅读 继续阅读

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)现在,我们要去.
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)现在,我们要去.
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)现在,我们要去.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)现在,我们要去.
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300)引入GRPO和组相关基准的论文.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)全四阶段R1配方加上R1-零的除.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400)CFR+深度学习规模.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)报纸是这一切的起始.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer)用于使用定制奖励功能的GRPO生产参考.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math)多个尺度上对R1配方的开放复制.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf)R1在LLM规模上设置的自动游戏,搜索和"设计奖励"的教科书框架.
