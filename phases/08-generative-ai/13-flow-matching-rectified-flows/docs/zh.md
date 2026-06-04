# 流匹配与整流流

> 扩散模型需要 20-50 步采样，因为它们从噪声到数据走的是弯曲路径。流匹配 (Flow Matching, Lipman et al., 2023) 和整流流 (Rectified Flow, Liu et al., 2022) 训练了直线路径。更直的路径意味着更少的步数，意味着更快的推理。Stable Diffusion 3、Flux.1 和 AudioCraft 2 都在 2024 年切换到了流匹配。

> **【中文解读】** 扩散模型需要 20-50 步采样因为走的是弯曲路径。Flow Matching 和 Rectified Flow 训练直线路径——更直的路径意味着更少的步数和更快的推理。SD3、FLUX.1、AudioCraft 2 都在 2024 年切换到了 Flow Matching。

> **【拓展：Flow Matching 是 2024-2026 的趋势】** Flow Matching 正在取代传统扩散调度成为新一代生成模型的标准。它数学上更优雅，实验上更高效。SD3 和 FLUX 的质量提升很大程度上归功于这个改进。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 06（DDPM）、阶段 1 · 微积分
**预计时间：** ~45 分钟

## 问题引入

DDPM 的反向过程是从 `N(0, I)` 回到数据分布的 1000 步随机游走。DDIM 将其压缩为 20-50 步确定性过程。你想要更少的步数——理想情况下一步。阻碍在于求解反向过程的 ODE 是刚性的；路径是弯曲的。

如果你能训练模型使噪声到数据的路径是一条*直线*，从 `t=1` 到 `t=0` 的单次 Euler 步就能工作。流匹配直接构建了这一点：定义从 `x_1 ∼ N(0, I)` 到 `x_0 ∼ data` 的直线插值，训练向量场 `v_θ(x, t)` 匹配其时间导数，推理时积分。

整流流 (Rectified Flow, Liu 2022) 更进一步：通过 reflow 过程迭代拉直路径，产生逐步接近线性的 ODE。经过两次 reflow 迭代后，2 步采样器可以匹敌 50 步 DDPM 的质量。

> **【中文解读】** Flow Matching 的核心思想：DDPM 的噪声到数据路径是弯曲的，需要 20-50 步采样。如果能训练直线路径，一步就能从噪声到数据。Flow Matching 定义 x_1（噪声）到 x_0（数据）的直线插值，训练向量场 v_theta(x,t) 匹配时间导数。Rectified Flow 进一步通过 reflow 迭代拉直路径，2 步采样即可匹配 50 步 DDPM 的质量。

> **【拓展：FLUX.1 的 Flow Matching 实现】** Black Forest Labs 的 FLUX.1（由 Stable Diffusion 原作者创建）使用 Flow Matching 替代传统扩散调度，配合 MMDiT（多模态 DiT）架构，在图像质量和生成速度上都显著优于 SDXL。FLUX.1-schnell 版本仅需 4 步采样即可生成高质量图像，验证了 Flow Matching 的实际优势。

## 核心概念

![流匹配：噪声与数据之间的直线插值](../assets/flow-matching.svg)

### 直线流

定义：

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

其中 `x_0 ~ data` 且 `x_1 ~ N(0, I)`。沿这条直线的时间导数是常数：

```
dx_t / dt = x_1 - x_0
```

定义一个神经向量场 `v_θ(x_t, t)` 并训练它匹配这个导数：

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

这就是**条件流匹配**损失（Lipman 2023）。训练是免模拟的：你从不展开 ODE。只需采样 `(x_0, x_1, t)` 并回归。

### 采样

推理时，将学习到的向量场*反向*积分：

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

从 `x_1 ~ N(0, I)` 开始，Euler 步降到 `t=0`。

### 整流流 (Rectified Flow, Liu 2022)

直线流有效，但学到的路径*并非真正笔直*——它们弯曲是因为许多 `x_0` 可以映射到同一个 `x_1`。整流流的 reflow 步骤：

1. 用随机配对训练流模型 v_1。
2. 通过从 `x_1` 积分 v_1 到其落点 `x_0` 来采样 N 对 `(x_1, x_0)`。
3. 在这些配对样本上训练 v_2。因为配对现在是"ODE 匹配"的，它们之间的直线插值真正更平坦。
4. 重复。

实际上 2 次 reflow 迭代就能接近线性，实现 2-4 步推理。SDXL-Turbo、SD3-Turbo、LCM 都是从流匹配蒸馏的模型。

### 为什么这在 2024 年为图像赢得了胜利

三个原因：

1. **免模拟训练**——训练期间不需要 ODE 展开，实现起来微不足道。
2. **更好的损失几何**——直线路径有一致的信噪比，而 DDPM 的 ε 损失在调度边缘信噪比差。
3. **更快的推理**——SDXL-Turbo 质量下 4-8 步；使用一致性蒸馏可 1 步。

## 流匹配 vs DDPM——精确联系

使用高斯条件路径的流匹配就是具有*特定噪声调度*的扩散。选择 `x_t = α(t) x_0 + σ(t) x_1` 调度，流匹配恢复 Stratonovich 重构的扩散，其中 `v = α'·x_0 - σ'·x_1`。对于高斯路径，两者在代数上等价。

流匹配新增的是：目标的*清晰性*（一个简单的速度）、更干净的损失，以及实验非高斯插值的自由度。

## 动手实现

`code/main.py` 在双峰高斯混合上实现了 1 维流匹配。向量场 `v_θ(x, t)` 是一个用直线目标训练的微型 MLP。推理时，积分 1、2、4 和 20 步 Euler 步并比较样本质量。

### 步骤 1：训练损失

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # 反向传播 + 更新
```

### 步骤 2：多步推理

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

### 步骤 3：比较步数

预期 4 步采样器已经能匹敌 20 步的质量——这对延迟意义重大。

## 常见陷阱

- **时间参数化。** 流匹配使用 `t ∈ [0, 1]`，`t=0` 在数据端，`t=1` 在噪声端。DDPM 使用 `t ∈ [0, T]`，`t=0` 在数据端，`t=T` 在噪声端。方向相同，尺度不同。论文经常弄错。
- **调度选择。** 整流流的直线是"标准的"流匹配调度，但你可以使用余弦或 logit-normal t 采样（SD3 就这么做）以获得更好的尺度覆盖。
- **Reflow 成本。** 为 reflow 生成配对数据集需要对每个样本进行完整的推理传播。只有真正需要 1-2 步推理时才做 reflow。
- **无分类器引导仍然适用。** 只需在线性组合中将 ε 替换为 v：`v_cfg = (1+w) v_cond - w v_uncond`。

## 用框架实现

| 用例 | 2026 年技术栈 |
|----------|-----------|
| 文本生成图像，最佳质量 | 流匹配：SD3, Flux.1-dev |
| 文本生成图像，1-4 步 | 蒸馏流匹配：Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| 实时推理 | 从流匹配基础模型进行一致性蒸馏（LCM, PCM） |
| 音频生成 | 流匹配：Stable Audio 2.5, AudioCraft 2 |
| 视频生成 | 流匹配与扩散混合（Sora, Veo, Stable Video） |
| 科学 / 物理（粒子轨迹、分子） | 流匹配 + 等变向量场 |

当 2025-2026 年的论文说"比扩散更快"时，几乎总是流匹配 + 蒸馏。

## 产出物

保存 `outputs/skill-fm-tuner.md`。技能接收扩散式模型规格并转换为流匹配训练配置：调度选择、时间采样分布（均匀 / logit-normal）、优化器、reflow 计划、目标步数、评估协议。

## 练习题

1. **简单。** 运行 `code/main.py`，比较 1 步 vs 20 步的 MSE 与真实数据分布的差异。
2. **中等。** 从均匀 `t` 采样切换到 logit-normal（将采样集中在中间 t 值）。模型质量是否提升？
3. **困难。** 实现一次 reflow 迭代：通过积分第一个模型生成配对的 (x_0, x_1)，在配对上训练第二个模型，比较 1 步样本质量。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 流匹配 | "直线扩散" | 训练 `v_θ(x, t)` 沿插值路径匹配 `x_1 - x_0`。 |
| 整流流 | "Reflow" | 拉直学习到的流的迭代过程。 |
| 速度场 | "v_θ" | 模型的输出——移动 `x_t` 的方向。 |
| 直线插值 | "路径" | `x_t = (1-t)·x_0 + t·x_1`；目标导数平凡。 |
| Euler 采样器 | "一阶 ODE 求解器" | 最简单的积分器；路径直时效果良好。 |
| Logit-normal t | "SD3 采样" | 将 `t` 采样集中在梯度最强的中间值附近。 |
| 一致性蒸馏 | "1 步采样器" | 训练学生将任意 `x_t` 直接映射到 `x_0`。 |
| 带速度的 CFG | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`；同样的技巧，新的变量。 |

## 生产笔记：Flux.1-schnell 是流匹配最快的形态

流匹配的生产胜利是 Flux.1-schnell——一个蒸馏到 1-4 步推理的流匹配 DiT，同时保持 Flux-dev 级别的质量。Niels 的"在 8GB 机器上运行 Flux"笔记本是参考部署配方：T5 + CLIP 编码、量化 MMDiT 去噪（schnell 4 步 vs dev 50 步）、VAE 解码。成本核算：

| 变体 | 步数 | L4 上 1024² 延迟 | 总 FLOPs（相对） |
|---------|-------|------------------------|------------------------|
| Flux.1-dev（原始） | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08×（快 12 倍） |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2 步 | 2 | ~0.3 s | 0.03× |

生产规则：**流匹配基础 + 蒸馏 = 2026 年快速文本生成图像的默认选择。** 每个主要供应商都发布这个组合：SD3-Turbo（SD3 + 流 + 蒸馏）、Flux-schnell（Flux-dev + 整流流拉直）、CogView-4-Flash。纯扩散基础仅存在于遗留检查点。

## 延伸阅读

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) — 整流流。
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) — 流匹配。
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) — SD3，大规模整流流。
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) — 覆盖 FM + 扩散的通用框架。
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) — 扩散/流的 1 步蒸馏。
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042) — turbo 变体。
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) — 生产中的流匹配。
