"""
演员-评论家 (Actor-Critic) — A2C 风格实现

核心概念：两个网络协同工作
  - Actor（演员）：策略网络 π_θ(a|s)，用策略梯度更新
  - Critic（评论家）：值网络 V_φ(s)，用 MSE 回归更新
  - 优势函数 A = G - V(s) 作为 Actor 的梯度信号

GAE (广义优势估计)：通过 λ 参数在 TD (λ=0, 低方差高偏差)
和 MC (λ=1, 高方差无偏差) 之间插值。λ=0.95 是 2026 年默认值。

AI 对应：GAE → PPO → ChatGPT RLHF 训练的核心组件。
理解 A2C + GAE，就理解了大模型对齐训练的基础架构。

本模块实现：手写线性 Actor + Critic + GAE 优势计算
"""

import math
import random


GRID = 4
TERMINAL = (3, 3)
ACTIONS = ("up", "down", "left", "right")
DELTAS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
N_ACTIONS = len(ACTIONS)
N_FEAT = GRID * GRID


def reset():
    return (0, 0)


def step(state, action_idx):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = DELTAS[ACTIONS[action_idx]]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL


def features(state):
    x = [0.0] * N_FEAT
    r, c = state
    x[r * GRID + c] = 1.0
    return x


def softmax(z):
    m = max(z)
    exps = [math.exp(zi - m) for zi in z]
    Z = sum(exps)
    return [e / Z for e in exps]


def logits(theta, x):
    return [sum(w * xi for w, xi in zip(theta[a], x)) for a in range(N_ACTIONS)]


def value(w, x):
    return sum(wj * xj for wj, xj in zip(w, x))


def sample(probs, rng):
    x = rng.random()
    cum = 0.0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return N_ACTIONS - 1


def init_theta(rng):
    return [[rng.gauss(0, 0.1) for _ in range(N_FEAT)] for _ in range(N_ACTIONS)]


def init_w(_rng):
    return [0.0] * N_FEAT


def rollout(theta, w, rng, max_steps=100):
    traj = []
    s = reset()
    for _ in range(max_steps):
        x = features(s)
        probs = softmax(logits(theta, x))
        a = sample(probs, rng)
        s_next, r, done = step(s, a)
        traj.append({"x": x, "a": a, "r": r, "probs": probs, "v": value(w, x), "done": done})
        if done:
            break
        s = s_next
    return traj


def gae_advantages(traj, gamma=0.99, lam=0.95):
    """计算 GAE (广义优势估计) 优势和回报目标

    GAE = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}，其中 δ_t = r_t + γ V(s_{t+1}) - V(s_t)
    λ=0 → 纯 TD（低方差高偏差），λ=1 → 纯 MC（高方差无偏差）
    """
    T = len(traj)
    advantages = [0.0] * T
    gae = 0.0
    for t in reversed(range(T)):  # 反向遍历
        next_v = 0.0 if traj[t]["done"] else (traj[t + 1]["v"] if t + 1 < T else 0.0)
        delta = traj[t]["r"] + gamma * next_v - traj[t]["v"]  # TD 残差 δ_t
        gae = delta + gamma * lam * gae  # GAE 递推
        advantages[t] = gae
    returns = [a + traj[t]["v"] for t, a in enumerate(advantages)]  # 回报 = 优势 + V(s)
    return advantages, returns


def normalize(xs):
    """标准化优势为零均值单位方差（大幅稳定训练）"""
    if len(xs) < 2:
        return xs
    m = sum(xs) / len(xs)
    var = sum((x - m) ** 2 for x in xs) / len(xs)
    sd = math.sqrt(var) + 1e-8
    return [(x - m) / sd for x in xs]


def actor_critic(episodes, lr_a=0.05, lr_v=0.1, gamma=0.99, lam=0.95, ent_coef=0.01, rng=None):
    """A2C 风格 Actor-Critic 训练：每回合更新 Actor 和 Critic"""
    rng = rng or random.Random(0)
    theta = init_theta(rng)  # Actor 参数
    w = init_w(rng)  # Critic 参数
    returns_log = []

    for ep in range(episodes):
        traj = rollout(theta, w, rng)  # 收集一个回合的轨迹
        advs, returns = gae_advantages(traj, gamma=gamma, lam=lam)  # 计算 GAE 优势
        advs_norm = normalize(advs)  # 标准化优势

        for t, node in enumerate(traj):
            # --- Critic 更新：MSE 回归 ---
            target = returns[t]
            err = target - value(w, node["x"])  # 值函数误差
            for j in range(N_FEAT):
                w[j] += lr_v * err * node["x"][j]  # 梯度下降

            # --- Actor 更新：策略梯度 + 熵正则化 ---
            adv = advs_norm[t]
            probs = node["probs"]
            for i in range(N_ACTIONS):
                grad_logpi = (1.0 if i == node["a"] else 0.0) - probs[i]  # ∇log π
                entropy_grad = -math.log(max(probs[i], 1e-12)) - 1.0  # 熵梯度
                for j in range(N_FEAT):
                    theta[i][j] += lr_a * (adv * grad_logpi + ent_coef * entropy_grad * probs[i]) * node["x"][j]

        if traj:
            mc_return = 0.0
            for r in reversed([n["r"] for n in traj]):
                mc_return = r + gamma * mc_return
            returns_log.append(mc_return)

    return theta, w, returns_log


def greedy_policy(theta):
    policy = {}
    for r in range(GRID):
        for c in range(GRID):
            if (r, c) == TERMINAL:
                continue
            z = logits(theta, features((r, c)))
            policy[(r, c)] = ACTIONS[max(range(N_ACTIONS), key=lambda i: z[i])]
    return policy


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


def block_mean(xs, block):
    return [sum(xs[i : i + block]) / block for i in range(0, len(xs) - block + 1, block)]


def main():
    episodes = 1500
    rng = random.Random(7)
    theta, w, log = actor_critic(episodes, lam=0.95, rng=rng)

    print(f"=== A2C-style actor-critic with GAE(lam=0.95) on 4x4 GridWorld ===")
    print()
    print(f"learning curve (mean return per 150 episodes):")
    for i, m in enumerate(block_mean(log, 150)):
        print(f"  block {i+1}: mean return = {m:6.2f}")

    print()
    print_policy(greedy_policy(theta), "greedy policy from actor")
    print()
    print("critic values V_phi(s):")
    for r in range(GRID):
        row = " ".join(f"{value(w, features((r, c))):7.2f}" for c in range(GRID))
        print("   " + row)

    print()
    print(f"final mean return (last 150 eps) = {sum(log[-150:]) / 150:.2f}  (optimal = -6.0)")


if __name__ == "__main__":
    main()
