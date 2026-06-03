"""
蒙特卡洛方法 (Monte Carlo Methods) — 从完整回合中学习

核心概念：不需要环境模型，只需运行策略、收集完整回合、对回报取平均
即可估计值函数。分首次访问 MC 和每次访问 MC 两种。

AI 对应：PPO/RLHF 训练中采样多个回答计算平均奖励；DeepSeek-R1 的 GRPO
使用组内采样均值作为基线——都是 MC 思想的直接应用。

本模块实现：
  - 首次访问 MC 策略评估
  - ε-贪心 MC 控制（在线策略）
"""

import random
from collections import defaultdict


GRID = 4
TERMINAL = (3, 3)  # 终止状态（右下角）
ACTIONS = ("up", "down", "left", "right")
DELTAS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def reset():
    """重置环境到起始状态 (0,0)"""
    return (0, 0)


def step(state, action):
    """执行一步：移动并返回 (新状态, 奖励, 是否终止)"""
    if state == TERMINAL:
        return state, 0.0, True  # 终止状态
    dr, dc = DELTAS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)  # 碰壁停留
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL  # 每步 -1 奖励


def states():
    """返回所有网格状态"""
    return [(r, c) for r in range(GRID) for c in range(GRID)]


def rollout(policy, rng, max_steps=200):
    """执行一个完整回合，返回轨迹 (s, a, r) 列表"""
    trajectory = []
    state = reset()
    for _ in range(max_steps):
        action = policy(state, rng)  # 按策略选动作
        state_next, reward, done = step(state, action)
        trajectory.append((state, action, reward))
        state = state_next
        if done:
            break
    return trajectory


def returns_from(trajectory, gamma):
    """从轨迹计算折扣回报：反向遍历 G_t = r_{t+1} + γ G_{t+1}"""
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):  # 反向遍历
        G = r + gamma * G  # 折扣回报递推
        returns.append(G)
    returns.reverse()
    return returns


def uniform_policy(_state, rng):
    """均匀随机策略：等概率选择每个动作"""
    return rng.choice(ACTIONS)


def mc_policy_evaluation(policy, episodes, gamma=0.99, rng=None):
    """首次访问 MC 策略评估：对每个状态取首次访问的回报均值"""
    rng = rng or random.Random(0)
    V = defaultdict(float)  # 状态值估计
    counts = defaultdict(int)  # 访问计数
    for _ in range(episodes):
        trajectory = rollout(policy, rng)
        returns = returns_from(trajectory, gamma)
        seen = set()  # 本回合已访问的状态
        for (s, _, _), G in zip(trajectory, returns):
            if s in seen:
                continue  # 跳过重复访问（首次访问 MC）
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]  # 增量均值更新
    return V, counts


def mc_control(episodes, gamma=0.99, epsilon=0.1, rng=None):
    """ε-贪心 MC 控制：在线策略学习最优 Q 和策略"""
    rng = rng or random.Random(0)
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})  # Q(s,a) 表
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(state, local_rng):
        """ε-贪心策略：以 ε 概率随机，否则选 Q 最大的动作"""
        if local_rng.random() < epsilon:
            return local_rng.choice(ACTIONS)
        return max(Q[state], key=Q[state].get)

    returns_log = []
    for ep in range(episodes):
        trajectory = rollout(policy, rng)
        returns = returns_from(trajectory, gamma)
        seen = set()  # 首次访问 (s,a) 对
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]  # 增量更新 Q
        if returns:
            returns_log.append(returns[0])  # 记录起始状态的回报
    greedy = {s: max(Q[s], key=Q[s].get) for s in Q}  # 提取贪心策略
    return Q, greedy, returns_log


def print_V(V, title):
    print(f"  {title}")
    for r in range(GRID):
        row = " ".join(f"{V[(r, c)]:7.2f}" for c in range(GRID))
        print("   " + row)


def print_policy(policy, title):
    arrows = {"up": "^", "down": "v", "left": "<", "right": ">"}
    print(f"  {title}")
    for r in range(GRID):
        row = " ".join(
            arrows[policy[(r, c)]] if (r, c) in policy and (r, c) != TERMINAL else ("." if (r, c) == TERMINAL else "?")
            for c in range(GRID)
        )
        print("   " + row)


def main():
    """运行 MC 评估和 MC 控制，对比 DP 基准"""
    rng = random.Random(1)
    V, counts = mc_policy_evaluation(uniform_policy, episodes=20000, gamma=0.99, rng=rng)
    print(f"=== first-visit MC, uniform-random policy, 20000 episodes, gamma=0.99 ===")
    print_V(V, "V^pi(s)")
    print()
    print(f"V(0,0) MC estimate     = {V[(0,0)]:.2f}")
    print(f"V(0,0) DP  reference   = -39.41   (from lesson 02 of this phase)")
    print(f"visit counts at (0,0)  = {counts[(0,0)]}")
    print()

    rng2 = random.Random(1)
    _Q, greedy, log = mc_control(episodes=30000, gamma=0.99, epsilon=0.1, rng=rng2)
    print("=== epsilon-greedy MC control, 30000 episodes ===")
    print_policy(greedy, "greedy policy recovered")
    print()
    tail = log[-5000:]
    if tail:
        mean_tail = sum(tail) / len(tail)
        print(f"mean return over last 5000 episodes = {mean_tail:.2f}")
        print("(optimal return on this 4x4 GridWorld = -6.0)")


if __name__ == "__main__":
    main()
