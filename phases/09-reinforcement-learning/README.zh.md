# Phase 9: 强化学习

> **12 节课 · ~13 小时 · 🟡进阶**

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
