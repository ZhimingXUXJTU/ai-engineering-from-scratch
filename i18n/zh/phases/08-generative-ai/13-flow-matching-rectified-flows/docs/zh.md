# 流量匹配和修改流量

> 扩散模型采用20-50个样本采集步骤,因为它们从噪音到数据的曲线路径.流量匹配 (Lipman等人, 2023) 和正流量 (Liu等人, 2022) 训练直路径.直路径意味着更少的步骤意味着更快的推断.稳定扩散3,流量1.1,音频Craft 2都转向流量匹配在2024年.

> **【中文解读】**扩散模型需要20-50步采样,因为走的是曲路径──流量匹配和修改流量训练直线路径更直的路径意味着更少的步数和更快的推理──SD3、FLUX.1、AudioCraft 2都在2024年转换到流量匹配──

> **【拓展：Flow Matching 是 2024-2026 的趋势】**流量匹配正取代传统的扩散调度成为新一代生成模型的标准. 它在数学上更优雅,实验上更高效.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

起的过程是从 起的步骤到步行.`N(0, I)`现在我们要回来数据分布.DDIM将其分解成20-50个确定性步骤.你想要少的步骤理想情况下是一个.阻者是,解决反向过程的ODE是硬的;路径是曲线的.

> 转向过程是从`N(0, I)`回到数据分布的1000步随机游走.DDIM将其缩小到20-50步.

如果您可以训练模型,使噪音到数据的路径是*直线*,`t=1`为了`t=0`流量匹配直接构建这个:定义直线插射从`x_1 ∼ N(0, I)`为了`x_0 ∼ data`引进一个向量场`v_θ(x, t)`为了匹配其时间衍生值,在推断中集成.

> 如果能训练模型使噪音到数据的路径是*直线*,`t=1`到了`t=0`足够了. 流量匹配 直接构建这个:定义`x_1 ∼ N(0, I)`到了`x_0 ∼ data`炼向量场`v_θ(x, t)`匹配时间导数――

修改流程 (Liu 2022) 进一步:通过重新流程程序反复直线路径,从而产生逐步接近线性ODE. 经过两次重新流程反复,一个2步样本器与50步DDPM质量相匹配.

> 通过回流 过程 代拉直路径──两次回流 代后,2步采样器匹配 50步 DDPM质量──

> **【中文解读】**流量匹配的核心思想:DDPM的噪音到数据路径是曲的,需要20-50步采样.如果能训练直线路径,一步就能从噪音到数据.

> **【拓展：FLUX.1 的 Flow Matching 实现】**黑森林实验室的FLUX.1(由稳定分散原作者创建) 使用流量匹配 替代传统扩散调度,配合MMDiT(多模态DT) 架构,在图像质量和生成速度上都显著优于SDXL──FLUX.1-schnell 版本只需4步采样即可生成高质量图像,验证了流量匹配的实际优势──

## 概念的核心概念

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### 直接流动

定义:

> 定义:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

在哪里`x_0 ~ data`其他`x_1 ~ N(0, I)`沿着直线的时间衍生值是恒定的:

> 其中`x_0 ~ data`没有任何`x_1 ~ N(0, I)`△沿着直线的时间导数是常数:

```
dx_t / dt = x_1 - x_0
```

定义一个神经向量场`v_θ(x_t, t)`并且将其训练成与此衍生品相匹配:

> 定义神经向量场`v_θ(x_t, t)`训练它匹配这个导数:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

这是**conditional flow matching**培训是无模拟的:你永远不会打开ODE.`(x_0, x_1, t)`后退.

> 这就是**条件 Flow Matching**损失(Lipman 2023) ◎训练是无模拟的:你永远不需要展开ODE──只需要采样`(x_0, x_1, t)`没有做回归即可.

### 样本采样

在推断时,将学习的向量场 *倒退* 集成在时间中:

> 推理时,将学到的向量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

开始`x_1 ~ N(0, I)`到,到.`t=0`现在,我们要去.

> 从`x_1 ~ N(0, I)`开始,用艾勒步进降到`t=0`,我知道.

### 整流流, 整流流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流, 整流,

直线流程是有效的,但学习的路径是不直接的,因为很多`x_0`现在,我们可以将它们映射到同一位置.`x_1`调整流的反流步骤:

> 虽然有效,但学习的路径实际上*不是真正的直线*因为许多`x_0`可以映射到同一个`x_1`路径会曲──修正流的反流步骤:

1. 列车流量模型v_1随机对接.
   用随机配对训练流动模型 v_1──
2. 样本N对`(x_1, x_0)`通过将v_1从`x_1`在它着陆之前`x_0`现在,我们要去.
   通过将 v_1 从 `x_1`积分到落点`x_0`采样 对`(x_1, x_0)`,我知道.
3. 由于对现在是"ODE-匹配",所以它们之间的直线插件是真正平坦的.
   在这些配对样本上训练 v_2──因为配对现在是"ODE 匹配",它们之间的直线插值确实更平坦──
4. 复制.
   复制

在实践中,两次反流代将你带到近线性,使得2-4步推断.SDXL-Turbo,SD3-Turbo,LCM都是蒸的流量匹配模型.

> 实践中,两次反流 代就能使路径接近线性,从而支持2~4步推理──SDXL-Turbo、SD3-Turbo、LCM 都基于流量匹配的模型──

### 为什么这在2024年赢得了图像的胜利?

原因有三个:

> 三个原因:

1. **Simulation-free training**培训期间没有ODE,实施是无关紧要的.
   **无需仿真的训练**训练时无需展开ODE,实现非常简单.
2. **Better loss geometry**直路线具有一致的信号到噪音,而DDPM ε-loss在时间表边缘具有不良的SNR.
   **更优的损失几何**直线路径信噪比一致,而DDPM的 ε-损失在调度边缘的SNR 较差.
3. **Faster inference** SDXL-Turbo质量4-8步;一致性蒸1步.
   **更快的推理**4-8 步即可达到SDXL-Turbo质量;配合一致性蒸可一步生成

## 流量匹配与DDPM 确切的连接

流量与高斯定条件路径相匹配是散 *具有特定的噪音时间表*.`x_t = α(t) x_0 + σ(t) x_1`时间表和流量匹配恢复了斯特拉托尼维奇修改的扩散`v = α'·x_0 - σ'·x_1`两者对高斯路径的代数式等价.

> 使用高斯条件路径的流量匹配实际上是*具有特定噪音调度*的扩散模型──选取`x_t = α(t) x_0 + σ(t) x_1`调度后,流量匹配还原为以斯特拉顿维奇形式重写的扩散,其中`v = α'·x_0 - σ'·x_1`△对于高斯路径,两者在代数上等价.

流量匹配增加了什么:目标的清晰度 (平坦的速度),更清洁的损失,以及使用非高斯人插件进行实验的许可.

> 流量匹配的真正贡献是:目标的*清晰度*(一个普通的速度向量) 、更干净的损失,以及尝试非高插值的自由──

## 建立它,实现它.
```figure
normalizing-flow
```

## 建立它

`code/main.py`实现1D流量匹配在两个模式的高斯混合物上.`v_θ(x, t)`在推断时,将1,2,4和20个艾勒步骤整合起来,并比较样品质量.

> `code/main.py`在双峰高斯混合分布实现1D流量匹配.`v_θ(x, t)`是一个微型MLP,使用直线目标训练.

### 步骤1: 训练失败

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 训练损失:采样噪音`x1`和时间`t`构建插值`x_t`目标为`x1 - x0`做平方回归.

### 步骤2:多步推理

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> 多步推理:从高斯噪音发出,按步长反向积分──步数越多结果越精确,但延迟越高──

### 步骤3:比较步数.

预计4步样本已经与20步质量相匹配,

> 已配合20步质量,对延迟是重大改进.

## 陷常见的陷

- **Time parameterization.**流量匹配用途`t ∈ [0, 1]`随着`t=0`在数据上,`t=1`声. 声.`t ∈ [0, T]`随着`t=0`在数据上,`t=T`报纸总是错误的.
  时间参数化:流量匹配 用`t ∈ [0, 1]`没有任何`t=0`在数据端,`t=1`在噪音端;DDPM使用`t ∈ [0, T]`论文经常搞错.
- **Schedule choice.**修改流程的直线是"流量匹配时间表",但可以使用共数或逻辑正常t样本 (SD3这样做) 来获得更好的规模覆盖.
  调度选择:修改流的直线是"标准"的流量匹配调度,但可以使用共数或逻辑正常的 t采样 (SD3就是这样做的) 获得更好的尺度覆盖.
- **Reflow cost.**通过一个数据集,我们可以通过一个数据集,然后再进行一个数据集.
  转移 成本:生成转移 配对数据集需要每样本一次完整推理――只有真正需要1-2步推理才做转移――
- **Classifier-free guidance still applies.**只是在线性组合中换 ε为 v: `v_cfg = (1+w) v_cond - w v_uncond`现在,我们要去.
  仍然适用:只需把线性组合里 ε 换成 v:`v_cfg = (1+w) v_cond - w v_uncond`,我知道.

## 用它实现框架

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

任何一篇论文说2025-2026年"比扩散快"的时刻,

> 当论文说"比扩散更快"时,几乎总是流量匹配 + 蒸.

## 运送它.

保存`outputs/skill-fm-tuner.md`技能采用了扩散式模型规范,并将其转换为与流量匹配的训练配置:时间表选择,时间样本分配 (均/逻辑正常),优化器,回流计划,目标步骤计数,评估协议.

> 保存为`outputs/skill-fm-tuner.md`△该技能接收一个扩散模型规格,将其转换为流量匹配 训练配置:调度选择、时间采样分布(均/逻辑正常) 、优化器、反流 计划、目标步数、评估协议。

## 练习题

1. **Easy.**跑步`code/main.py`并且比较1步对20步的MSE对真实数据分布.
   **简单。**运行`code/main.py`实际数据分布的MSE与1步和20步相比.
2. **Medium.**换成制服`t`采样到logit-normal (集中采样在t中).模型质量有没有改善?
   **中等。**将平均`t`采样切换为逻辑正常的集中 t 附近采样) ――模型质量是否提升?
3. **Hard.**实现一个反流代:通过整合第一种模型生成对 (x_0, x_1) 组,对对进行第二种模型训练,并比较1步样品质量.
   **困难。**实现一次回流 代:通过对第一个模型积分生成配对 (x_0, x_1),在配对上训练第二个模型,并比较1步采样质量.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## 产品注释:Flux.1-schnell是流量匹配最快的形态

流量匹配的生产胜利是Flux.1-schnell 一个流量匹配的DT蒸到1-4推理步骤,同时保持Flux-dev级质量.尼尔的"Run Flux on an 8GB machine"笔记本书是参考部署配方:T5 + CLIP编码,量化MMDiT代号 (快速而不是 dev的50个步骤),VAE解码.成本计量:

> 流量匹配在生产中的胜利是Flux.1-schnell一个蒸到1-4步推理、保持Flux-dev 级质量的流量匹配的DiT。尼尔斯的"在8GB机器上运行Flux"笔记本是参考部署方案:T5 + CLIP 编码、量化MMDiT 去噪音(schnell 4步相对于 dev 50步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

生产规则:**flow-matched base + distillation = the 2026 default for fast text-to-image.**每个主要供应商都运送这种组合:SD3-Turbo (SD3 +流量 +蒸),Flux-schnell (Flux-dev +直流直线),CogView-4-Flash.纯的扩散基地仅适用于传统检查站.

> 生产规则:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**每个主要厂商都推出了这种组合:SD3-Turbo(SD3 +流量 +蒸) √流量-机(流量- +修改流量 拉直) √CogView-4-Flash──纯扩散基座仅为遗留检查点保留────

## 继续阅读 继续阅读

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003)正流量
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)流量匹配
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3,在尺度上调整流量.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797)涵盖FM+传播的一般框架.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) 1 步蒸/流.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042)轮机变体
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/)生产流量相匹配.
