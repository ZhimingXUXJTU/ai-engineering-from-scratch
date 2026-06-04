# ControlNet、LoRA 与条件控制

> 纯文本控制太粗糙。ControlNet 让你克隆一个预训练的扩散模型，用深度图、姿态骨架、涂鸦或边缘图来引导它。LoRA 让你只训练 1000 万参数就能微调 20 亿参数的模型。两者结合让 Stable Diffusion 从玩具变成了 2026 年每个设计公司都在用的图像流水线。

> **【中文解读】** 纯文本控制太粗糙。ControlNet 用深度图、姿态骨架、涂鸦或边缘图精确控制生成；LoRA 只训练 1000 万参数就能微调 20 亿参数的模型。两者结合让 Stable Diffusion 从玩具变成了 2026 年每个设计公司都在用的图像流水线。

> **【拓展：LoRA 是大模型时代的微调标准】** LoRA（低秩适配）不仅在图像生成中使用，也被广泛用于 LLM 微调（如 LLaMA-LoRA）。只需训练 0.1% 的参数就能适配新任务/新风格，使 AI 定制化成本大幅降低。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 07（潜在扩散）、阶段 10（从零构建 LLM——LoRA 基础）
**预计时间：** ~75 分钟

## 问题引入

像"一位穿红裙的女士在繁忙的街道上遛狗"这样的提示给模型没有提供关于狗在*哪里*、女士是*什么姿态*或街道*什么视角*的信息。文本只能确定你需要指定一张图像的信息的约 10%。其余是视觉的，无法用文字高效描述。

为每个信号（姿态、深度、Canny 边缘、分割）从零训练一个新的条件模型代价太高。你想要保持 2.6B 参数的 SDXL 主干冻结，附加一个读取条件的小型侧网络，让它微调主干的中间特征。这就是 ControlNet。

你还想教模型新概念（你的脸、你的产品、你的风格），而不重新训练整个模型。你想要一个缩小 100 倍的增量。这就是 LoRA——插入现有注意力权重的低秩适配器。

ControlNet + LoRA + 文本 = 2026 年从业者的工具包。大多数生产图像流水线在 SDXL / SD3 / Flux 基础模型上叠加 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter。

## 核心概念

![ControlNet 克隆编码器；LoRA 添加低秩增量](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

取一个预训练的 SD。*克隆* U-Net 编码器的一半。冻结原始部分。训练克隆部分接受额外的条件输入（边缘、深度、姿态）。用*零卷积*跳跃连接（初始化为零的 1×1 卷积——初始为恒等操作，学习一个增量）将克隆部分连接回原始的解码器一半。

```
SD U-Net 解码器：   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

零卷积初始化意味着 ControlNet 初始为恒等——训练前也不会有害。在 100 万个（提示、条件、图像）三元组上用标准扩散损失训练。

每种模态的 ControlNet 作为小型侧模型发布（SDXL 约 360M，SD 1.5 约 70M）。推理时可以组合：

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### LoRA (Hu et al., 2021)

对于模型中的任意线性层 `W ∈ R^{d×d}`，冻结 `W` 并添加一个低秩增量：

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

其中 `r << d`。注意力层常用的秩为 4-16，重度微调为 64-128。新增参数数量：`2 · d · r` 而非 `d²`。对于 `d=640` 的 SDXL 注意力，`r=16`：每个适配器 20k 参数而非 410k——减少 20 倍。整个模型：LoRA 通常 20-200MB vs 基础模型 5GB。

推理时可以缩放 LoRA：`W' = W + α · B @ A`。`α = 0.5-1.5` 是正常范围。多个 LoRA 可以加性叠加（通常要注意它们以非线性方式交互）。

### IP-Adapter (Ye et al., 2023)

一个微型适配器，接受一张*图像*作为条件（与文本并行）。使用 CLIP 图像编码器生成图像 token，将它们与文本 token 一起注入交叉注意力。每个基础模型约 20MB。让你做到"以此参考图的风格生成图像"，无需 LoRA。

## 可组合性矩阵

| 工具 | 控制什么 | 大小 | 何时使用 |
|------|------------------|------|-------------|
| ControlNet | 空间结构（姿态、深度、边缘） | 70-360MB | 精确布局、构图 |
| LoRA | 风格、主体、概念 | 20-200MB | 个性化、风格 |
| IP-Adapter | 来自参考图像的风格或主体 | 20MB | 没有文字能描述那种外观 |
| Textual Inversion | 作为新 token 的单一概念 | 10KB | 遗留方法，大多被 LoRA 替代 |
| DreamBooth | 对主体的全面微调 | 2-5GB | 强身份感，高计算量 |
| T2I-Adapter | 更轻量的 ControlNet 替代 | 70MB | 边缘设备，推理预算有限 |

ControlNet ≈ 空间。LoRA ≈ 语义。两者都用。

> **【中文解读】** ControlNet 的核心机制：克隆 SD U-Net 编码器，冻结原始部分，训练克隆部分接受额外条件输入（边缘、深度、姿态）。零卷积（zero-convolution）初始化确保训练开始时 ControlNet 不影响原始模型。LoRA 在线性层上添加低秩矩阵 B@A，只训练极少量参数（20-200MB vs 基础模型 5GB）。

> **【拓展：ControlNet + LoRA 的组合控制】** 实际生产中，ControlNet（空间控制）和 LoRA（风格/主题控制）通常组合使用。例如：ControlNet 控制人物姿态，LoRA 注入特定艺术风格，文本 prompt 描述场景内容。这种三层控制机制是 2026 年商业 AI 图像服务的标准配置。IP-Adapter 则提供了"用图片控制图片"的第四维度。

## 动手实现

`code/main.py` 在 1 维上模拟了这两种机制：

1. **LoRA。** 一个预训练的线性层 `W`。冻结它。训练一个低秩 `B @ A` 使得 `W + BA` 匹配目标线性层。展示 `r = 1` 就足以完美学习一个秩为 1 的修正。

2. **ControlNet-lite。** 一个"冻结基础"预测器和一个读取额外信号的"侧网络"。侧网络的输出由一个初始化为零的可学习标量门控（我们的零卷积版本）。训练并观察门控逐渐增大。

### 步骤 1：LoRA 数学

```python
def lora(W, A, B, x, alpha=1.0):
    # W 被冻结；A, B 是可训练的低秩因子
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### 步骤 2：零初始化侧网络

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate 初始化为 0
h = base(x) + gated
```

在第 0 步，输出与基础模型完全相同。早期训练缓慢更新 `gate`——没有灾难性漂移。

## 常见陷阱

- **过度缩放 LoRA。** `α = 2` 或 `α = 3` 是常见的"让它更强"的技巧，会产生过度风格化/破损的输出。保持 `α ≤ 1.5`。
- **ControlNet 权重冲突。** 以权重 1.0 使用姿态 ControlNet 和权重 1.0 的深度 ControlNet 通常会过冲。权重总和 ≈ 1.0 是安全的默认值。
- **错误基础上的 LoRA。** SDXL LoRA 在 SD 1.5 上会静默无效，因为注意力维度不匹配。Diffusers 0.30+ 会警告。
- **Textual Inversion 漂移。** 在一个检查点上训练的 token 在另一个检查点上漂移严重。LoRA 更可移植。
- **LoRA 权重合并与存储。** 你可以将 LoRA 烘焙到基础模型权重中以获得更快的推理（无运行时加法），但你会失去运行时缩放 `α` 的能力。保留两个版本。

## 用框架实现

| 目标 | 2026 年流水线 |
|------|---------------|
| 复刻品牌的艺术风格 | 在约 30 张精选图像上以秩 32 训练的 LoRA |
| 将我的脸放入生成图像中 | DreamBooth 或 LoRA + IP-Adapter-FaceID |
| 特定姿态 + 提示 | ControlNet-Openpose + SDXL + 文本 |
| 深度感知构图 | ControlNet-Depth + SD3 |
| 参考图 + 提示 | IP-Adapter + 文本 |
| 精确布局 | ControlNet-Scribble 或 ControlNet-Canny |
| 背景替换 | ControlNet-Seg + Inpainting（第 09 课） |
| 快速 1 步风格 | LCM-LoRA on SDXL-Turbo |

## 产出物

保存 `outputs/skill-sd-toolkit-composer.md`。技能接收一个任务（输入资产：提示、可选参考图、可选姿态、可选深度图、可选涂鸦），输出工具栈、权重和可复现的种子协议。

## 练习题

1. **简单。** 在 `code/main.py` 中，将 LoRA 秩 `r` 从 1 变到 4。在什么秩下 LoRA 恰好匹配秩为 2 的目标增量？
2. **中等。** 在两个目标变换上分别训练两个 LoRA。同时加载它们并展示它们的加性交互。交互何时破坏线性？
3. **困难。** 使用 diffusers 堆叠：SDXL-base + Canny-ControlNet（权重 0.8）+ 风格 LoRA（α 0.8）+ IP-Adapter（权重 0.6）。测量随着栈权重变化的 FID-vs-提示遵循度权衡。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "空间控制" | 克隆编码器 + 零卷积跳跃连接；读取条件图像。 |
| 零卷积 | "初始为恒等" | 初始化为零的 1×1 卷积；ControlNet 初始为无操作。 |
| LoRA | "低秩适配器" | `W + B @ A`，`r << d`；比全量微调少 100 倍参数。 |
| 秩 r | "那个旋钮" | LoRA 压缩度；典型值 4-16，重度个性化 64+。 |
| α | "LoRA 强度" | LoRA 增量的运行时缩放。 |
| IP-Adapter | "参考图" | 通过 CLIP 图像 token 的小型图像条件适配器。 |
| DreamBooth | "全量主体微调" | 在约 30 张主体图像上训练整个模型。 |
| Textual Inversion | "新 token" | 只学习一个新的词嵌入；遗留方法，大多被替代。 |

## 生产笔记：LoRA 交换、ControlNet 通道、多租户服务

一个真实的文本生成图像 SaaS 在同一个基础检查点上服务数百个 LoRA 和十几个 ControlNet。服务问题很像 LLM 多租户（生产文献在连续批处理和 LoRAX / S-LoRA 下覆盖了 LLM 场景）：

- **热交换 LoRA，不要合并。** 将 `W' = W + α·B·A` 合并到基础模型中可加速每步推理约 3-5%，但冻结了 `α` 和基础模型。将 LoRA 作为秩为 r 的增量保持在 VRAM 中热加载；diffusers 提供了 `pipe.load_lora_weights()` + `pipe.set_adapters([...], adapter_weights=[...])` 用于按请求激活。交换成本是 `2 · d · r · num_layers` 个权重——MB 级别，亚秒级。
- **ControlNet 作为第二注意力通道。** 克隆的编码器与基础模型并行运行。两个权重为 1.0 的 ControlNet = 每步两次额外前向传播，而非一次合并的传播。批大小余量二次下降。预算每个活跃 ControlNet 约 1.5 倍步成本。
- **量化 LoRA 也是可以的。** 如果你量化了基础模型（见第 07 课，8GB 上的 Flux），LoRA 增量也可以干净地量化到 8-bit 或 4-bit。QLoRA 风格的加载让你可以在 4-bit Flux 基础上叠加 5-10 个 LoRA 而不爆内存。

Flux 特定：Niels 的 Flux-on-8GB 笔记将基础模型量化到 4-bit；在该量化基础上叠加风格 LoRA（`pipe.load_lora_weights("user/style-lora")`），使用 `weight_name="pytorch_lora_weights.safetensors"` 仍然有效。这是 2026 年大多数 SaaS 机构部署的配方。

## 延伸阅读

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) — ControlNet。
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) — LoRA（最初用于 LLM；移植到扩散）。
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) — IP-Adapter。
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) — ControlNet 的更轻替代。
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) — DreamBooth。
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) — 参考流水线。
