# 扩散模型 — 从零实现 DDPM

> Ho, Jain, Abbeel (2020) 给了领域一个无法放弃的配方。用一千个小步将数据用噪声摧毁。训练一个神经网络预测噪声。推理时反转这个过程。今天，每一个主流的图像、视频、3D 和音乐模型都运行在这个循环上，可能还叠加了流匹配或一致性技巧。

> **【中文解读】** DDPM 的核心流程：用一千步逐步给数据加噪声破坏数据，训练一个神经网络预测噪声，推理时反向去除噪声。2026 年所有主流图像/视频/3D/音乐模型都基于这个循环（可能加上 Flow Matching 或一致性技巧）。

> **【拓展：扩散模型是当前 AI 生成的核心】** Stable Diffusion、DALL-E 3、Midjourney、Sora 都基于扩散模型。DDPM 证明了一个简单的去噪目标可以产生惊人的生成能力。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 3 · 02（反向传播）、阶段 8 · 02（VAE）
**预计时间：** ~75 分钟

## 问题引入

你想要一个 `p_data(x)` 的采样器。GAN 进行极小极大博弈，经常发散。VAE 从高斯解码器产生模糊的样本。你真正想要的是一个训练目标，它 (a) 是一个单一稳定的损失（没有鞍点，没有极小极大）、(b) 是 `log p(x)` 的下界（所以你有似然）、(c) 样本质量匹敌 SOTA。

Sohl-Dickstein et al.（2015）给出了一个理论答案：定义一个马尔可夫链 `q(x_t | x_{t-1})` 逐步添加高斯噪声，训练一个反向链 `p_θ(x_{t-1} | x_t)` 进行去噪。Ho, Jain, Abbeel（2020）证明损失可以简化为一行——预测噪声——并整理了数学。2020 年这还是个新奇事物。2021 年它产生了最先进的样本。2022 年它变成了 Stable Diffusion。2026 年它是基础设施。

> **【中文解读】** DDPM 的三步流程：(1) 前向过程——逐步加高斯噪声直到数据变为纯噪声；(2) 训练——学习一个网络预测每一步添加的噪声；(3) 反向过程——从纯噪声开始逐步去噪，恢复出逼真数据。损失函数简化为"预测噪声"这一个目标——训练稳定，无需对抗博弈。

> **【拓展：从 DDPM 到实用扩散模型】** DDPM 原始论文在像素空间操作，速度慢（需要 1000 步去噪）。三个关键改进使其成为实用工具：(1) DDIM（2020）将采样步数从 1000 降到 20-50；(2) 潜在扩散（2021，Rombach）在 VAE 潜在空间中操作，大幅降低计算量；(3) CFG（Classifier-Free Guidance，2022）通过条件/无条件预测的差值提升生成质量。

## 核心概念

![DDPM：前向加噪，反向去噪](../assets/ddpm.svg)

**前向过程 `q`。** 在 `T` 个小步中添加高斯噪声。闭合形式——数学可处理的原因——是累积步也是高斯的：

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

其中 `α̅_t = ∏_{s=1..t} (1 - β_s)` 对应一个 `β_t` 调度。选择从 1e-4 到 0.02 的线性 `β_t`，T=1000 步，则 `x_T` 近似为 `N(0, I)`。

**反向过程 `p_θ`。** 学习一个神经网络 `ε_θ(x_t, t)` 预测添加的噪声。给定 `x_t`，通过以下方式去噪：

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

其中 `σ_t` 要么是 `sqrt(β_t)` 要么是学习到的方差。表达式看起来丑陋但只是代数——给定后验 `q(x_{t-1} | x_t, x_0)`，将 `x_0` 用噪声预测估计代入，解出 `x_{t-1}`。

**训练损失。**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

从数据中采样 `x_0`，随机选一个 `t`，采样 `ε ~ N(0, I)`，通过闭合形式一步计算含噪 `x_t`，回归噪声。一个损失，没有极小极大，没有 KL，没有重参数化技巧。

**采样。** 从 `x_T ~ N(0, I)` 开始。从 `t = T` 到 `1` 迭代反向步骤。完成。

## 为什么有效

三个直觉：

1. **去噪容易；生成困难。** 在 `t=T` 时，数据是纯噪声——网络需要解决一个平凡的问题。在 `t=0` 时，网络只需清理几个像素。在中间的 `t`，问题很难，但网络从每个噪声级别通过相同权重获得许多梯度。

2. **分数匹配的伪装。** Vincent（2011）证明了预测噪声等价于估计 `∇_x log q(x_t | x_0)`，即*分数*。反向 SDE 使用这个分数沿密度梯度上行——一个朝向高概率区域的引导随机游走。

3. **ELBO 退化为简单 MSE。** 完整的变分下界每个时间步都有一个 KL 项。在 DDPM 的参数化下，这些 KL 项简化为带特定系数的噪声预测 MSE；Ho 丢掉了系数（称之为"简单"损失），质量反而*提高了*。

## 动手实现

`code/main.py` 实现了一个 1 维 DDPM。数据是双峰混合。"网络"是一个微型 MLP，接收 `(x_t, t)` 并输出预测噪声。训练就是那一行损失。采样通过迭代反向链。

### 步骤 1：前向调度（闭合形式）

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### 步骤 2：一步采样 `x_t`

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### 步骤 3：一步训练

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### 步骤 4：反向采样

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

对于一个 40 个时间步和 24 单元 MLP 的 1 维问题，大约 200 个 epoch 就能学到双峰混合。

## 时间条件化

网络需要知道它在去噪哪个时间步。两种标准选择：

- **正弦嵌入。** 类似 Transformer 位置编码。`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`。通过 MLP，广播到网络中。
- **FiLM / 组归一化条件化。** 将嵌入投影到逐通道的缩放/偏移 (FiLM) 在每个块中。

我们的玩具代码使用正弦 → 拼接。生产 U-Net 使用 FiLM。

## 常见陷阱

- **调度很关键。** 线性 `β` 是 DDPM 的默认值，但余弦调度（Nichol & Dhariwal，2021）在相同计算量下给出更好的 FID。如果质量停滞就切换调度。
- **时间步嵌入很脆弱。** 将原始 `t` 作为浮点数传入对玩具 1 维有效，但对图像会失败；始终使用适当的嵌入。
- **V 预测 vs ε 预测。** 对于极端情况（很小或很大的 t），`ε` 的信噪比很差。V 预测（`v = α·ε - σ·x`）更稳定；SDXL、SD3 和 Flux 使用它。
- **无分类器引导 (CFG)。** 推理时，计算条件和无条件的 `ε`，然后 `ε_cfg = (1 + w) · ε_cond - w · ε_uncond`，`w ≈ 3-7`。在第 08 课中详述。
- **1000 步太多了。** 生产使用 DDIM（20-50 步）、DPM-Solver（10-20 步）或蒸馏（1-4 步）。见第 13 课。

## 用框架实现

| 角色 | 2026 年的典型技术栈 |
|------|-----------------------|
| 图像像素空间扩散（小型、玩具） | DDPM + U-Net |
| 图像潜在扩散 | VAE 编码器 + U-Net 或 DiT（第 07 课） |
| 视频潜在扩散 | 时空 DiT（Sora, Veo, WAN） |
| 音频潜在扩散 | Encodec + 扩散 Transformer |
| 科学（分子、蛋白质、物理） | 等变扩散（EDM, RFdiffusion, AlphaFold3） |

扩散是通用生成主干。流匹配（第 13 课）是 2024-2026 年的竞争者，通常在相同质量下推理速度更快。

## 产出物

保存 `outputs/skill-diffusion-trainer.md`。技能接收数据集 + 计算预算，输出：调度（线性/余弦/S 形）、预测目标（ε/v/x）、步数、引导缩放、采样器族和评估协议。

## 练习题

1. **简单。** 在 `code/main.py` 中将 T 从 40 改为 10。样本质量（输出的可视化直方图）如何下降？在什么 T 下双峰结构坍塌？
2. **中等。** 从 ε 预测切换到 v 预测。重新推导反向步骤。比较最终样本质量。
3. **困难。** 添加无分类器引导。以类别标签 `c ∈ {0, 1}` 为条件，训练时 10% 的时间丢弃标签，采样时使用 `ε = (1+w)·ε_cond - w·ε_uncond`。测量 `w = 0, 1, 3, 7` 时的条件模式命中率。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 前向过程 | "加噪声" | 固定的马尔可夫链 `q(x_t \| x_{t-1})`，破坏数据。 |
| 反向过程 | "去噪" | 学习的链 `p_θ(x_{t-1} \| x_t)`，重建数据。 |
| β 调度 | "噪声阶梯" | 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | 累积乘积 `∏(1 - β)`；给出从 `x_0` 到 `x_t` 的闭合形式。 |
| 简单损失 | "噪声上的 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`；所有变分推导都退化为这个。 |
| ε 预测 | "预测噪声" | 输出是添加的噪声；标准 DDPM。 |
| V 预测 | "预测速度" | 输出是 `α·ε - σ·x`；跨 t 的更好条件化。 |
| DDPM | "那篇论文" | Ho et al. 2020；线性 β，1000 步，U-Net。 |
| DDIM | "确定性采样器" | 非马尔可夫采样器，20-50 步，相同的训练目标。 |
| 无分类器引导 | "CFG" | 混合条件和无条件噪声预测以放大条件化。 |

## 生产笔记：扩散推理是一个步数问题

DDPM 论文运行 T=1000 个反向步骤。生产中没有人这么做。每个实际的推理堆栈选择三种策略之一——每种都清晰地对应生产文献中"延迟来自哪里"的框架：

1. **更快的采样器，相同模型。** DDIM（20-50 步）、DPM-Solver++（10-20）、UniPC（8-16）。反向循环的直接替换；训练好的 `ε_θ` 权重不变。延迟降低 20-50 倍。
2. **蒸馏。** 训练一个学生以更少步数匹配教师：渐进蒸馏（2 → 1）、一致性模型（任意 → 1-4）、LCM、SDXL-Turbo、SD3-Turbo。延迟再降低 5-10 倍，需要重新训练。
3. **缓存和编译。** `torch.compile(unet, mode="reduce-overhead")`、TensorRT-LLM 的扩散后端、`xformers`/SDPA 注意力、bf16 权重。每步延迟降低约 2 倍。可与 (1) 和 (2) 叠加。

对于生产扩散服务器，预算对话与生产文献中描述的 LLM 相同：延迟是 `num_steps × step_cost + VAE_decode`，吞吐量是 `batch_size × (num_steps × step_cost)^-1`。TTFT 很小（一步）；TPOT 等价物是完整的响应时间，因为从用户角度来看图像生成是"一次性"的。

## 延伸阅读

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) — 扩散论文，领先于时代。
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — DDPM。
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) — DDIM，更少步数。
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672) — 余弦调度，学习方差。
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) — 分类器引导。
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) — CFG。
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) — 统一符号，最干净的配方。
