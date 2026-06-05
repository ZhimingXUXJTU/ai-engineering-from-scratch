# Sim-to-Real Transfer | 仿真到现实迁移

> A policy trained in a simulator that fails on hardware is a policy that memorized the simulator. Domain randomization, domain adaptation, and system identification are the three tools to make learned controllers cross the reality gap.

> **【中文解读】** 在仿真器中训练的策略如果无法在真实硬件上工作，说明它"过拟合"了仿真器。域随机化、域自适应和系统辨识是让 RL 策略跨越"现实鸿沟"的三大工具。

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance)
**Time:** ~45 minutes

## The Problem | 问题引入

Training a real robot is slow, dangerous, and expensive. A biped takes millions of training episodes to learn to walk; a real biped that falls over even once breaks hardware. Simulation gives you unlimited resets, deterministic reproducibility, parallel environments, and no physical damage.

> 训练真实机器人很慢、危险且昂贵。一个双足机器人需要数百万训练回合才能学会行走；真实双足机器人即使摔倒一次也可能损坏硬件。仿真给你无限重置、确定性可复现、并行环境和零物理损伤。

But simulators are wrong. Bearings have more friction than MuJoCo models. Cameras have lens distortion the simulator does not include. Motors have delays, backlash, and saturation that 99% of sim models skip. Wind, dust, and variable lighting sabotage a policy trained on sterile rendering. The **reality gap** — systematic difference between sim distribution and real distribution — is the central problem of deployed RL for robotics.

> 但仿真器是错的。轴承比 MuJoCo 模型有更多摩擦。相机有仿真器不包括的镜头畸变。电机有延迟、间隙和饱和，99% 的仿真模型跳过了这些。风、灰尘和可变光照破坏了在无菌渲染上训练的策略。**现实鸿沟**——仿真分布和真实分布之间的系统性差异——是部署机器人 RL 的核心问题。

You need a policy that is *robust to sim-to-real distribution shift*. Three historical approaches: randomize the simulator (domain randomization), adapt the policy with a little real data (domain adaptation / fine-tuning), or identify the real system's parameters and match them (system identification). In 2026 the dominant recipe combines all three with massive parallel simulation (Isaac Sim, Isaac Lab, Mujoco MJX on GPU).

> 你需要一个对仿真到真实分布偏移*鲁棒*的策略。三种历史方法：随机化仿真器（域随机化）、用少量真实数据适应策略（域自适应/微调），或识别真实系统参数并匹配（系统辨识）。2026 年的主流方案是三者结合加大规模 GPU 并行仿真。

> **【中文解读】** "现实鸿沟"是机器人 RL 的核心问题。三大解决方案：(1) 域随机化——在训练时随机化仿真参数让策略更鲁棒；(2) 域自适应——用少量真实数据微调；(3) 系统辨识——测量真实参数修正仿真器。2026 年的主流方案是三者结合+大规模 GPU 并行仿真。

> **【拓展：域随机化→大模型泛化】** 域随机化的思想在 LLM 训练中也有对应：数据增强（同义改写、噪声注入）就是"随机化训练分布"以提高泛化能力。RLHF 中的 KL 惩罚防止策略偏离太远，类似于防止"过拟合仿真器"。

## The Concept | 核心概念

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).** Tobin et al. 2017, Peng et al. 2018. During training, randomize every sim parameter that might differ on the real robot: masses, friction coefficients, motor PD gains, sensor noise, camera position, lighting, textures, contact models. The policy learns a conditional distribution over "which sim it is in today" and generalizes across the full span. If the real robot falls within the training envelope, the policy works.

> **域随机化（DR）。** 训练期间，随机化每个可能与真实机器人不同的仿真参数：质量、摩擦系数、电机 PD 增益、传感器噪声、相机位置、光照、纹理、接触模型。策略学习一个"今天在哪个仿真中"的条件分布并在全范围内泛化。

- **Upside:** no real data needed. One recipe, many robots.
  **优点：** 不需要真实数据。一个方案，多种机器人。
- **Downside:** over-randomized training produces a "universal" but overly cautious policy. Too much noise ≈ too much regularization.
  **缺点：** 过度随机化训练产生"通用"但过于保守的策略。太多噪声≈太多正则化。

**System Identification (SI).** Fit the simulator's parameters to real-world data before training. If you can measure arm-joint friction on the real robot, plug that into the sim. Then train a policy that expects those values. Needs access to the real system but reduces the reality gap directly.

> **系统辨识（SI）。** 训练前将仿真器参数拟合到真实世界数据。需要接触真实系统但直接缩小现实鸿沟。

**Domain Adaptation.** Train in sim, fine-tune with a small amount of real data. Two flavors:

> **域自适应。** 在仿真中训练，用少量真实数据微调。两种变体：

- **Real2Sim2Real:** learn a residual simulator `f(s, a, z) - f_sim(s, a)` using real rollouts, train in the corrected sim. Closes the gap without much real data.
  **Real2Sim2Real：** 用真实 rollout 学习残差仿真器，在修正后的仿真中训练。
- **Observation adaptation:** train a policy that maps real obs → sim-like obs via a learned feature extractor (e.g., GAN pixel-to-pixel). The controller stays in sim.
  **观测自适应：** 训练将真实观测映射为仿真式观测的策略。

**Privileged learning / teacher-student.** Miki et al. 2022 (ANYmal quadruped). Train a *teacher* in simulation that has access to privileged information (ground truth friction, terrain height, IMU drift). Distill a *student* that only sees real-sensor observations. The student learns to infer privileged features from history, robust across physical parameters.

> **特权学习/教师-学生。** 在仿真中训练有权访问特权信息的*教师*。蒸馏一个只看到真实传感器观测的*学生*。学生从历史推断特权特征。

**Massively parallel simulation.** 2024–2026. Isaac Lab, Mujoco MJX, Brax all run thousands of parallel robots on a single GPU. PPO with 4,096 parallel humanoids collects years of experience in hours. The "reality gap" shrinks as training distribution widens; DR becomes almost free when each of those 4,096 envs has different randomized parameters.

> **大规模并行仿真。** 2024-2026 年。Isaac Lab、Mujoco MJX、Brax 在单个 GPU 上运行数千个并行机器人。PPO 配合 4,096 个并行人形机器人在数小时内收集数年经验。当训练分布变宽时，"现实鸿沟"缩小。

**The real-world 2026 recipe (quadruped walking example):**

1. Massively parallel sim with domain-randomized gravity, friction, motor gains, payload.
2. Teacher policy trained with privileged info (terrain map, body velocity ground truth).
3. Student policy distilled from teacher using only proprioception (leg joint encoders).
4. Optional observation adaptation via autoencoder on real IMU.
5. Deploy. Zero-shot on 10+ environments. If it fails, do minutes of real-world fine-tuning with safety-constrained PPO.

> **真实世界 2026 年方案（四足行走示例）：** 大规模并行仿真 + 域随机化 → 教师策略（特权信息）→ 学生策略蒸馏（仅本体感受）→ 可选观测自适应 → 部署。零样本迁移到 10+ 环境。如果失败，做几分钟安全约束 PPO 真实世界微调。

## Build It | 动手实现

This lesson's code is a tiny demonstration of domain randomization on a GridWorld with *noisy* transitions. We train a policy that experiences randomized slip probabilities in "sim" and evaluate on "real" with a slip level it never saw during training. The shape maps directly to MuJoCo-to-hardware transfer.

> 本课的代码是在带*噪声*转移的 GridWorld 上域随机化的小型演示。我们训练一个在"仿真"中体验随机滑移概率的策略，并在训练中从未见过的滑移水平上评估"真实"。这个结构直接映射到 MuJoCo 到硬件的迁移。

### Step 1: parameterized sim

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip` is a parameter the simulator exposes. In real robotics it could be friction, mass, motor gain — anything that shifts between sim and real.

> `slip` 是仿真器暴露的参数。在真实机器人中它可能是摩擦、质量、电机增益——任何在仿真和真实之间变化的量。

### Step 2: train with DR

At the start of each episode, sample `slip ~ Uniform[0.0, 0.4]`. Train PPO / Q-learning / anything. Do this for many episodes.

> 每个回合开始时，采样 `slip ~ Uniform[0.0, 0.4]`。训练 PPO/Q-learning/任何算法。

### Step 3: evaluate zero-shot on "real" slips

Evaluate on `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`. The first four are within training support; `0.5` and `0.7` are outside. A DR-trained policy should stay near-optimal inside support and degrade gracefully outside. A fixed-slip-trained policy will be brittle outside its training slip.

> 在 `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}` 上评估。前四个在训练支撑内；`0.5` 和 `0.7` 在外。DR 训练的策略应在支撑内保持近最优，在外优雅退化。固定滑移训练的策略在其训练滑移外会很脆弱。

### Step 4: compare to narrow training

Train a second policy with `slip = 0.0` only. Evaluate on the same `slip` sweep. You should see a catastrophic drop as soon as real slip > 0.

> 用 `slip = 0.0` 训练第二个策略。在相同的滑移范围上评估。当真实滑移 > 0 时应看到灾难性下降。

## Pitfalls

- **Too much randomization.** Train on `slip ∈ [0, 0.9]` and your policy is so risk-averse it never tries the optimal path. Match the *expected* real-world distribution, not "anything could happen."
  **过度随机化。** 在 `slip ∈ [0, 0.9]` 上训练，策略过于规避风险而不尝试最优路径。匹配*期望的*真实世界分布。
- **Too little randomization.** Train on a thin slice and the policy can't generalize at all. Use adaptive curriculum (Automatic Domain Randomization) that widens the distribution as the policy improves.
  **过少随机化。** 在薄切片上训练，策略完全无法泛化。使用自适应课程（ADR），随策略改进加宽分布。
- **Misidentified parameter space.** Randomize the wrong thing (camera hue when the real gap is motor delay) and DR does not help. Profile the real robot first.
  **错误识别参数空间。** 随机化错误的东西，DR 无效。先分析真实机器人。
- **Privileged info leakage.** A teacher that uses global state for actions, not just observations, can produce a student that cannot catch up. Ensure the teacher's policy is realizable by the student given observation history.
  **特权信息泄漏。** 使用全局状态做动作的教师可能产生无法追赶的学生。
- **Sim-to-sim transfer failure.** If your policy is not robust to a harder sim variant, it will not be robust to the real world either. Always test on a held-out sim variant before deploying.
  **仿真到仿真迁移失败。** 如果策略对更难的仿真变体不鲁棒，对真实世界也不会鲁棒。部署前始终在保留仿真变体上测试。
- **No real-world safety envelope.** A policy that works in sim and "works in real" without a low-level safety shield can still break hardware. Add rate limits, torque limits, joint limits in a non-learned controller.
  **无真实世界安全包络。** 没有低级安全屏蔽的策略仍可能损坏硬件。在非学习控制器中添加速率限制、扭矩限制、关节限制。

## Use It | 用框架实现

The 2026 sim-to-real stack:

> 2026 年仿真到真实技术栈：

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

For control at all scales, the workflow is consistent: fit the sim as best you can, randomize what you can't fit, train enormous policies, distill, deploy with a safety shield.

> 对所有规模的控制，工作流一致：尽可能拟合仿真，随机化无法拟合的部分，训练巨大策略，蒸馏，部署时加安全屏蔽。

## Ship It | 产出物

Save as `outputs/skill-sim2real-planner.md`:

```markdown
---
name: sim2real-planner
description: Plan a sim-to-real transfer pipeline for a given robot + task, covering DR, SI, and safety.
version: 1.0.0
phase: 9
lesson: 11
tags: [rl, sim2real, robotics, domain-randomization]
---

Given a robot platform, a task, and access to real hardware time, output:

1. Reality gap inventory. Suspected sources ranked by expected impact (contact, sensing, actuation delay, vision).
2. DR parameters. Exact list, ranges, distribution. Justify each range against real measurements.
3. SI steps. Which parameters to measure; measurement method.
4. Teacher/student split. What privileged info the teacher uses; what obs the student uses.
5. Safety envelope. Low-level limits, emergency stops, backup controller.

Refuse to deploy without (a) a zero-shot sim-variant test, (b) a safety shield, (c) a rollback plan. Flag any DR range wider than 3× measured real variability as likely over-randomized.
```

## Exercises | 练习题

1. **Easy.** Train a Q-learning agent on the fixed-slip GridWorld (slip=0.0). Evaluate on slip ∈ {0.0, 0.1, 0.3, 0.5}. Plot return vs slip.
2. **Medium.** Train a DR Q-learning agent sampling `slip ~ Uniform[0, 0.3]`. Evaluate the same sweep. How much does DR buy at slip=0.5 (out-of-distribution)?
3. **Hard.** Implement a curriculum: start with slip=0.0, widen the DR range every time the policy hits 90% of optimal. Measure total environment steps to reach slip=0.3 zero-shot vs. a fixed DR baseline.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Reality gap | "Sim-to-real difference" / 现实鸿沟 | Distribution shift between training and deployment physics/sensing. |
| Domain randomization (DR) | "Train across random sims" / 域随机化 | Randomize sim parameters during training so policy generalizes. |
| System identification (SI) | "Measure real and fit sim" / 系统辨识 | Estimate real physical parameters; set sim to match. |
| Domain adaptation | "Fine-tune on real data" / 域自适应 | Small real-world fine-tune after sim training; may adapt obs or dynamics. |
| Privileged info | "Ground truth for teacher" / 特权信息 | Information only the sim has; student must infer it from obs history. |
| Teacher/student | "Distill privileged -> observable" / 教师-学生蒸馏 | Teacher trained with shortcuts; student learns to mimic without them. |
| ADR | "Automatic Domain Randomization" / 自动域随机化 | Curriculum that widens DR ranges as the policy improves. |
| Real2Sim | "Close the gap with real data" / 现实到仿真 | Learn a residual to make the sim mimic real rollouts. |

## Further Reading | 延伸阅读

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) — the original DR paper (vision for robotics).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) — DR for dynamics, quadruped locomotion.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) — Dactyl, ADR at scale.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822) — teacher-student for ANYmal.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470) — the massively parallel sim that drives 2025–2026 deployments.
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113) — ADR curriculum method.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf) — the Dyna framing (use a model for planning + rollouts) that underpins modern sim-to-real pipelines.
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303) — taxonomy of sim-to-real methods with benchmark results.
