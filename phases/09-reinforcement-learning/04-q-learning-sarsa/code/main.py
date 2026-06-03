"""
时序差分学习 (Temporal Difference) — Q-Learning 与 SARSA

核心概念：每一步都更新值函数，用 bootstrapping（自举）构造目标：
  TD 目标 = r + γ V(s')
Q-learning 用 max（离策略，学习最优 Q*），SARSA 用实际下一动作（在线策略，学习 Q^π）。

AI 对应：Q-learning 是 Atari DQN 的核心→开启了深度 RL 时代；
SARSA 的在线策略思想延伸到 PPO→ChatGPT RLHF 训练的核心算法。

本模块实现：
  - SARSA（在线策略 TD 控制）
  - Q-learning（离策略 TD 控制）
"""

import random
from collections import defaultdict


GRID = 4
TERMINAL = (3, 3)
ACTIONS = ("up", "down", "left", "right")
DELTAS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def reset():
    return (0, 0)


def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = DELTAS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL


def epsilon_greedy(Q, state, rng, epsilon):
    """ε-贪心动作选择：以 ε 概率随机探索，否则选 Q 最大的动作"""
    if rng.random() < epsilon:
        return rng.choice(ACTIONS)
    q = Q[state]
    return max(ACTIONS, key=lambda a: q[a])


def sarsa(episodes, alpha=0.1, gamma=0.99, epsilon=0.1, rng=None):
    """SARSA 算法（在线策略 TD 控制）：用实际下一动作 a' 构造目标"""
    rng = rng or random.Random(0)
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})  # Q 表初始化为 0
    returns = []
    for _ in range(episodes):
        s = reset()
        a = epsilon_greedy(Q, s, rng, epsilon)  # 选初始动作
        total = 0.0
        for _ in range(200):
            s_next, r, done = step(s, a)
            total += r
            if done:
                Q[s][a] += alpha * (r - Q[s][a])  # 终止时目标是 r
                break
            a_next = epsilon_greedy(Q, s_next, rng, epsilon)  # 用当前策略选下一动作
            target = r + gamma * Q[s_next][a_next]  # SARSA 目标：r + γ Q(s',a')
            Q[s][a] += alpha * (target - Q[s][a])  # TD 更新
            s, a = s_next, a_next
        returns.append(total)
    return Q, returns


def q_learning(episodes, alpha=0.1, gamma=0.99, epsilon=0.1, rng=None):
    """Q-learning 算法（离策略 TD 控制）：用 max Q(s',a') 构造目标"""
    rng = rng or random.Random(0)
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    returns = []
    for _ in range(episodes):
        s = reset()
        total = 0.0
        for _ in range(200):
            a = epsilon_greedy(Q, s, rng, epsilon)  # 行为策略（ε-贪心）
            s_next, r, done = step(s, a)
            total += r
            if done:
                Q[s][a] += alpha * (r - Q[s][a])
                break
            best_next = max(Q[s_next].values())  # 目标策略（贪心 max）
            target = r + gamma * best_next  # Q-learning 目标：r + γ max Q(s',·)
            Q[s][a] += alpha * (target - Q[s][a])  # TD 更新
            s = s_next
        returns.append(total)
    return Q, returns


def greedy_policy(Q):
    return {s: max(ACTIONS, key=lambda a: q[a]) for s, q in Q.items()}


def print_policy(policy, title):
    arrows = {"up": "^", "down": "v", "left": "<", "right": ">"}
    print(f"  {title}")
    for r in range(GRID):
        row = []
        for c in range(GRID):
            if (r, c) == TERMINAL:
                row.append(".")
            elif (r, c) in policy:
                row.append(arrows[policy[(r, c)]])
            else:
                row.append("?")
        print("   " + " ".join(row))


def block_means(xs, block):
    return [sum(xs[i : i + block]) / block for i in range(0, len(xs) - block + 1, block)]


def main():
    episodes = 3000
    rng = random.Random(42)
    Q_sarsa, ret_sarsa = sarsa(episodes, rng=rng)
    rng = random.Random(42)
    Q_ql, ret_ql = q_learning(episodes, rng=rng)

    print(f"=== 4x4 GridWorld, {episodes} episodes, alpha=0.1, eps=0.1, gamma=0.99 ===")
    print()
    print("learning curves (mean return per block of 500 episodes):")
    for i, (a, b) in enumerate(zip(block_means(ret_sarsa, 500), block_means(ret_ql, 500))):
        print(f"  block {i+1}: sarsa={a:7.2f}   q-learning={b:7.2f}")

    print()
    print_policy(greedy_policy(Q_sarsa), "SARSA greedy policy")
    print()
    print_policy(greedy_policy(Q_ql), "Q-learning greedy policy")

    print()
    print(f"final mean return (last 500 eps):  sarsa={sum(ret_sarsa[-500:])/500:.2f}   q-learning={sum(ret_ql[-500:])/500:.2f}")
    print("(optimal return on this 4x4 GridWorld = -6.0)")


if __name__ == "__main__":
    main()
