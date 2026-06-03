"""
动态规划 (Dynamic Programming) — 策略迭代与值迭代

核心概念：已知 MDP 模型（转移概率 + 奖励函数），通过 Bellman 方程的不动点迭代
精确求解最优值函数 V* 和最优策略 π*。

AI 对应：DP 是所有 RL 算法的"金标准"。AlphaZero 的 MCTS、ChatGPT 的 RLHF
训练循环，本质上都是 Bellman 备份思想的不同变体。

本模块实现：
  - 策略迭代 (Policy Iteration)：交替执行策略评估和策略改进
  - 值迭代 (Value Iteration)：一步到位的 Bellman 最优性备份
"""

GRID = 4
TERMINAL = (3, 3)
ACTIONS = ("up", "down", "left", "right")  # 四个动作：上、下、左、右
DELTAS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
SLIP = 0.1  # 随机滑动概率：10% 的概率滑向垂直方向


def states():
    """返回所有网格状态"""
    return [(r, c) for r in range(GRID) for c in range(GRID)]


def apply_move(state, direction):
    """执行移动动作，碰到边界则留在原地"""
    dr, dc = DELTAS[direction]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)  # 限制在网格范围内
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc)


def perpendiculars(action):
    """返回垂直方向（用于模拟滑动）"""
    if action in ("up", "down"):
        return ("left", "right")
    return ("up", "down")


def transitions(state, action):
    """MDP 转移模型：返回 (下一状态, 奖励, 概率) 的列表"""
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]  # 终止状态：停留，奖励0
    outcomes = []
    p_intended = 1.0 - SLIP  # 90% 概率按预期方向移动
    outcomes.append((apply_move(state, action), -1.0, p_intended))
    for perp in perpendiculars(action):
        outcomes.append((apply_move(state, perp), -1.0, SLIP / 2.0))  # 每个垂直方向 5%
    return outcomes


def q_value(state, action, V, gamma):
    """计算 Q(s,a) = Σ P(s',r|s,a) * [r + γ V(s')]"""
    return sum(p * (r + gamma * V[s_next]) for s_next, r, p in transitions(state, action))


def policy_evaluation(policy, gamma=0.99, tol=1e-6, max_iter=5000):
    """策略评估：反复迭代 Bellman 方程直到 V 收敛"""
    V = {s: 0.0 for s in states()}  # 初始化值函数为 0
    for _ in range(max_iter):
        delta = 0.0
        for state in states():
            if state == TERMINAL:
                continue
            dist = policy(state)
            v = sum(pi_a * q_value(state, action, V, gamma) for action, pi_a in dist.items())
            delta = max(delta, abs(v - V[state]))  # sup-范数收敛判断
            V[state] = v
        if delta < tol:
            return V
    return V


def greedy_from_V(V, gamma=0.99):
    """策略改进：对每个状态取 Q 值最大的动作"""
    policy = {}
    for state in states():
        if state == TERMINAL:
            policy[state] = "up"
            continue
        best = max(ACTIONS, key=lambda a: q_value(state, a, V, gamma))
        policy[state] = best
    return policy


def policy_iteration(gamma=0.99, tol=1e-6):
    """策略迭代：评估→改进→评估，循环直到策略不变"""
    policy = {s: "up" for s in states()}  # 初始策略：全部向上
    sweeps = 0
    for it in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma=gamma, tol=tol)  # 评估当前策略
        sweeps += 1
        new_policy = greedy_from_V(V, gamma)  # 贪心改进
        if new_policy == policy:  # 策略稳定 → 找到最优
            return V, policy, it + 1
        policy = new_policy
    return V, policy, 100


def value_iteration(gamma=0.99, tol=1e-6, max_iter=5000):
    """值迭代：直接取 max，一步完成评估+改进"""
    V = {s: 0.0 for s in states()}
    for it in range(max_iter):
        delta = 0.0
        for state in states():
            if state == TERMINAL:
                continue
            v = max(q_value(state, action, V, gamma) for action in ACTIONS)  # Bellman 最优性方程
            delta = max(delta, abs(v - V[state]))
            V[state] = v
        if delta < tol:
            return V, greedy_from_V(V, gamma), it + 1  # 收敛后提取贪心策略
    return V, greedy_from_V(V, gamma), max_iter


def print_V(V, title):
    print(f"  {title}")
    for r in range(GRID):
        row = " ".join(f"{V[(r, c)]:7.2f}" for c in range(GRID))
        print("   " + row)


def print_policy(policy, title):
    arrows = {"up": "^", "down": "v", "left": "<", "right": ">"}
    print(f"  {title}")
    for r in range(GRID):
        row = " ".join(arrows[policy[(r, c)]] if (r, c) != TERMINAL else "." for c in range(GRID))
        print("   " + row)


def main():
    """运行值迭代和策略迭代，比较两者的收敛结果"""
    print("=== 4x4 stochastic GridWorld (slip=0.1), value iteration ===")
    V_vi, pi_vi, n_vi = value_iteration(gamma=0.99)
    print_V(V_vi, f"V* (converged in {n_vi} sweeps)")
    print()
    print_policy(pi_vi, "optimal policy")

    print()
    print("=== Same MDP, policy iteration ===")
    V_pi, pi_pi, n_pi = policy_iteration(gamma=0.99)
    print_V(V_pi, f"V* (converged in {n_pi} outer iters)")
    print()
    print_policy(pi_pi, "optimal policy")

    print()
    V_match = max(abs(V_vi[s] - V_pi[s]) for s in states())
    print(f"sup-norm |V_vi - V_pi| = {V_match:.2e}  (should be ~0)")
    print(f"policies identical?     {pi_vi == pi_pi}")


if __name__ == "__main__":
    main()
