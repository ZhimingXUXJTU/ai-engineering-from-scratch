# Phase 9: 强化学习

> **12 节课 · ~13 小时 · 🟡进阶**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**Phase 1 的概率与分布，以及 Phase 2 第 01 课（机器学习分类体系）。

**第一课：**[MDP 状态、动作与奖励](01-mdps-states-actions-rewards/)

在仓库根目录运行以下命令：

```bash
python3 phases/09-reinforcement-learning/01-mdps-states-actions-rewards/code/main.py
```

保留命令、退出码、随机策略与贪心策略的回报、价值网格，以及一句话把策略质量与期望回报联系起来。

**下一步：**修改折扣因子，预测价值会如何变化，然后继续学习 [动态规划](02-dynamic-programming/)。

浏览[完整的 Phase 9 课程列表](../../README.md#phase-9)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 理解马尔可夫决策过程（MDP）的数学框架：状态、动作、奖励
- 掌握动态规划、蒙特卡洛、时序差分等经典强化学习方法
- 深入理解 DQN、策略梯度、Actor-Critic、PPO 等深度强化学习算法
- 了解奖励建模与 RLHF 在大模型对齐中的应用
- 学习多智能体强化学习和从仿真到现实的迁移方法

## 前置知识

- 深度学习基础（Phase 3：神经网络、PyTorch）
- 概率与统计基础（Phase 1：期望、方差、马尔可夫链）
- 优化基础（Phase 1：梯度下降）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | MDP 状态、动作与奖励 | Learn | Python | ~45min |
| 02 | 动态规划 | Build | Python | ~75min |
| 03 | 蒙特卡洛方法 | Build | Python | ~75min |
| 04 | 时序差分 — Q-Learning 与 SARSA | Build | Python | ~75min |
| 05 | 深度 Q 网络 (DQN) | Build | Python | ~75min |
| 06 | 策略梯度方法 — REINFORCE | Build | Python | ~75min |
| 07 | Actor-Critic — A2C 与 A3C | Build | Python | ~75min |
| 08 | 近端策略优化 (PPO) | Build | Python | ~75min |
| 09 | 奖励建模与 RLHF | Learn | Python | ~45min |
| 10 | 多智能体强化学习 | Learn | Python | ~45min |
| 11 | 从仿真到现实迁移 | Learn | Python | ~45min |
| 12 | 强化学习在游戏中的应用 | Build | Python | ~75min |

## 常见困惑

- **"强化学习和监督学习有什么区别？"** → 监督学习有标签，强化学习只有奖励信号（可能延迟）。智能体需要通过试错学习最优策略，而不是从正确答案中学习。
- **"为什么要学 PPO？"** → PPO 是 ChatGPT 训练中 RLHF 阶段使用的核心算法。理解 PPO 是理解大模型对齐的关键。
- **"强化学习一定要用环境模拟器吗？"** → 本阶段课程使用 OpenAI Gym 等轻量级环境，不需要复杂模拟器。游戏和机器人模拟器在后续课程中介绍。

## 开始学习

→ [第一课：MDP 状态、动作与奖励](01-mdps-states-actions-rewards/docs/zh.md)
