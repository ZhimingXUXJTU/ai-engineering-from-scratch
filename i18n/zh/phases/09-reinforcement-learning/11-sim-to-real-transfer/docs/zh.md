# 仿真到现实移动

> 训练在模拟器中失败的硬件是记住模拟器的政策.域名随机化,域名适应和系统识别是让学到的控制器跨越现实差距的三个工具.

> **【中文解读】**如果不能在真实硬件上工作,说明它"过适合"真实器.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance) | **前置知识:** Phase 9 · 08 (PPO), Phase 2 · 10 (偏差/方差)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

训练一个真正的机器人是慢,危险,昂贵的.双脚需要数百万次训练才能学会走路;一个真正的双脚即使一旦打破硬件,也会摔倒.模拟给你无限的重置,确定性可复制性,并行环境,没有物理损害.

> 训练真实的机器人很慢,危险又昂贵. 一个双脚机器人需要数百万训练回合才能学会走走;真实的双脚机器人即使摔倒一次也可能损坏硬件.

模拟器是错误的.轴承比MuJoCo模型更有摩擦.相机有镜头扭曲.模拟器不包括.电机有延误,反响和和99%的Sim模型跳过.风,尘埃和变量照明破坏了训练在无菌的染的政策.**reality gap**系统性区别在真实分布和Sim分布之间是机器人部署RL的核心问题.

> 但是仿真机是错误的.轴承比MuJoCo模型有更多的摩擦.相机有仿真机不包括镜头变.电机有延迟,间隙和和,99%的仿真模型跳过这些.风,灰尘和可变光照破坏了无菌染染上训练的策略.**现实鸿沟**仿真分布与真实分布之间的系统性差异是部署机器人RL的核心问题.

需要一个可靠的政策, 历史方法:随机化模拟器 (域名随机化),使用一些实际数据 (域名适应/细调) 调整政策,或识别实际系统的参数并匹配它们 (系统识别). 2026年,主导的配方将所有三种配方都结合到大型并行模拟 (GPU上的Isaac Sim,Isaac Lab,Mujoco MJX).

> 你需要一个对仿真到真实的分布偏移的策略――三种历史方法:随机化仿真器 (随机化) 、使用少量真实数据适应策略 (随机化),或识别真实系统参数并匹配 (系统识别) ──2026年的主流方案是三者结合加大GPU并行仿真――

> **【中文解读】**"现实沟通"是机器人RL的核心问题. 三大解决方案: 1) 域随机化在训练中随机化仿真参数让策略更好; 2) 域自适应使用少量真实数据微调; 3) 系统识别测量真实参数修改仿真机.

> **【拓展：域随机化→大模型泛化】**域随机化思想在LLM培训中也有对应:数据增强 (同义改写、噪声注入) 是"随机化培训分布"以提高泛化能力.

## 概念的核心概念

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).**其他类型 2017年,潘等 美国 在训练期间,随机定制每一个可能在实际机器人上不同的模拟参数:质量,摩擦系数,电动PD增长,传感器噪音,摄像头位置,照明,纹理,接触模型. 政策学习了"今天的情况"的条件分布,并将其在整个范围进行概括. 如果真正的机器人属于训练包,

> **域随机化（DR）。**训练期间,随机化每一个可能与真机器不同的仿真参数:质量,摩擦系数,电机PD 增益,传感器噪声,相机位置,光照,纹理,接触模型.

- **Upside:**没有真正的数据,只需要一个食谱,很多机器人.
  **优点：**没有必要的真实数据.
- **Downside:**过度随机化培训产生了"普遍"但过于谨慎的政策.
  **缺点：**过度随机化训练产生了"通用"但过于保守的策略.

**System Identification (SI).**训练前将模拟器的参数与现实数据调整.如果你能测量实机器人的臂关节摩擦,将其插入在模拟器中.然后训练一个预期这些值的政策.需要访问实系统,但直接减少现实差距.

> **系统辨识（SI）。**训练前将模拟器参数适合真实世界数据――需要接触真实系统但直接缩小现实沟――

**Domain Adaptation.**训练在模拟,微调用少量真实数据.

> **域自适应。**在仿真中训练,使用少量真实数据微调.

- **Real2Sim2Real:**学习一个残余模拟器`f(s, a, z) - f_sim(s, a)`通过使用真实推广,在修改的模拟中训练. 没有太多真实数据就关闭了差距.
  **Real2Sim2Real：**用真实推广学习残差模仿器,在修改后的模仿中训练.
- **Observation adaptation:**通过学习的特征提取器 (例如GAN像素到像素) 绘制真实obs →sim类似的obs的策略.控制器保持在sim.
  **观测自适应：**训练将真实观测映射为仿真观测的策略.

**Privileged learning / teacher-student.**学生们可以从历史中推断特权特征,在物理参数中强. 学生们可以从历史中推断特权特征,在物理参数中强. 学生们可以从历史中推断特权特征.

> **特权学习/教师-学生。**在仿真中训练有权访问特权信息的*教师*──蒸一个只看到真实的传感器观测的*学生*──学生从历史推断特权特征──

**Massively parallel simulation.**20242026年.艾萨克实验室,Mujoco MJX,Brax都在一个GPU上运行数千个并行机器人.PPO拥有4,096个并行人形,在几个小时内收集了多年的经验.随着训练分布的扩大,"现实差距"缩小;当这些4,096个 envs中的每个具有不同的随机参数时,DR几乎变得自由.

> **大规模并行仿真。**2024-2026年──伊萨克实验室、穆乔科MJX、Brax 在单个GPU上运行数千个并行机器──PPO配合4,096个并行人形机器人在几小时内收集了多年的经验──当训练分布变宽时",现实沟"缩小──

**The real-world 2026 recipe (quadruped walking example):**

1. 具有域式随机引力,摩擦,动力增长,有效载荷.
2. 教师政策训练有素的信息 (地图,身体速度地图).
3. 学生政策仅使用自体感 (腿关节编码器) 来从教师中炼.
4. 通过真实IMU的自动编码器进行可选的观察适应.
5. 如果它失败,用安全限制的PPO进行几分钟的现实世界细节调整.

> **真实世界 2026 年方案（四足行走示例）：**大规模并行仿真 + 域随机化 → 教师策略(特权信息)→ 学生策略蒸(仅本体感受)→ 可选观测自适应 → 部署。零样本迁移到10+ 环境。如果失败,做几分钟安全约束 PPO 真实世界微调。

## 建立它,实现它.
```figure
f3-reality-gap
```

## 建立它

本课程的代码是 GridWorld上随机域定位的小示范,具有 *噪音*的过渡.我们训练了一个政策,在"sim"中体验到随机滑梯概率,并以"真实"评估,使用训练中从未见过的滑梯水平.形状直接映射到MuJoCo到硬件转移.

> 本课程的代码是带*噪音*转移的 GridWorld 上域随机化的小演示. 我们训练了一个在"仿真"中体验随机滑移概率的策略,并在训练中从未见过的滑移水平上评估"真实"――这个结构直接映射到MuJoCo到硬件的迁移.

### 步骤1:参数化Sim

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip`在真实机器人中,它可能是摩擦,质量,运动增长 任何在真实和真实之间转移的东西.

> `slip`在真实机器中,它可能是摩擦,质量,电机增长

### 步骤2:与DR一起训练

在每一集的开始,`slip ~ Uniform[0.0, 0.4]`训练PPO/Q学习/任何东西.

> 每次回合开始时,采样`slip ~ Uniform[0.0, 0.4]`△培训PPO/Q-学习/任何算法──

### 步骤3:评估"真实"的分片中零射击

评估`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`首先,四个项目包括培训支持.`0.5`其他`0.7`对于外围的运动, DR训练的运动应该保持在内部的支持中接近最佳水平,在外面却会显著降低.

> 在`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`上评.前四个在训练支内;`0.5`和 `0.7`在外面,DR 训练策略应保持在支内最接近优势,在外面优雅退化.

### 步骤4:与狭窄的训练相比

培养第二个政策`slip = 0.0`只有在同一方面进行评估`slip`实际滑动时就会出现灾难性的下降.

> 用`slip = 0.0`训练第二个策略――在相同的滑移范围上评估――当真实的滑移 > 0 时应看到灾难性下降――

## 陷

- **Too much randomization.**列车上线`slip ∈ [0, 0.9]`您的政策是如此的不愿意冒险,它从来没有尝试最佳的路径.
  **过度随机化。**在`slip ∈ [0, 0.9]`炼,策略过于规范,不尝试最佳路径――匹配*期望的*真实世界分布――
- **Too little randomization.**训练在一个薄片,政策根本不能通用. 使用适应课程 (自动域名随机化),随着政策的改善,扩大分布.
  **过少随机化。**在薄片上训练,策略完全无法泛化.
- **Misidentified parameter space.**随机定位错误的东西 (当真实差距是运动延迟时,摄像头的色调)
  **错误识别参数空间。**随机化错误的东西,DR无效.
- **Privileged info leakage.**通过使用全球状态来进行行动,而不是仅仅进行观察, 教授可以产生无法追赶的学生.
  **特权信息泄漏。**使用全局状态做动的教师可能产生无法追赶的学生.
- **Sim-to-sim transfer failure.**如果您的政策不适合更难的模拟变体,它也不适合现实世界.
  **仿真到仿真迁移失败。**如果策略对更难的仿真变体不好,对真实世界也不好.
- **No real-world safety envelope.**没有低级安全屏蔽的"真实工作"的政策仍然可以打破硬件. 在未学习的控制器中添加速度限制,扭矩限制,关节限制.
  **无真实世界安全包络。**没有低级安全屏蔽策略仍然可能损坏硬件――在非学习控制器中增加加速率限制、扭矩限制、关节限制――

## 用它实现框架

现在,我们要做什么?

> 2026年仿真到真实技术:

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

为了在所有尺度上控制,工作流程是一致的:尽可能适应模拟器,随机定制无法适应的,

> 为了控制所有规模,工作流一致:尽可能适合仿真,随机化无法适合部分,训练巨大的策略,蒸,部署时加安全屏蔽.

## 运送它.

保存如`outputs/skill-sim2real-planner.md`其他:

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

## 练习题

1. **Easy.**训练一个Q学习代理在固定滑动格里德世界 (滑动=0.0). 评估在滑动 ∈ {0.0, 0.1, 0.3, 0.5}.
2. **Medium.**训练一个DRQ学习代理样本`slip ~ Uniform[0, 0.3]`根据"分销"的价格,DR在0.5分时购买多少钱?
3. **Hard.**实施课程:从滑=0.0开始,每当政策达到90%的最佳时,扩大DR范围. 测量环境的总步骤,以达到滑=0.3的零射与固定DR基线.

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907)原始的DR论文 (机器人技术的视觉).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) 动力,四次机动的DR.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) 达克泰尔,ADR在尺度上.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822)为 ANYmal 的教师-学生.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470)引发2025~2026次部署的巨大平行模拟器.
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113)ADR课程方法.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf)Dyna框架 (用于规划+推广模型),支持现代的真实模拟管道.
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303)与基准结果的真实模拟方法分类.
