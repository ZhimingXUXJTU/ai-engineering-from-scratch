# 世界模型与视频传播

> 预测场景的下一秒钟的视频模型是世界模拟器, 条件下预测行动,你就有了学习的游戏引擎.

> **【中文解读】**能够预测场景接下来的几秒钟的视频模型就是一个世界模拟器.将预测条件化为动作,就得到了一个学习的游戏引擎.

> **【拓展：世界模型的前沿】** (OpenAI) 和Genie (DeepMind) 是世界模型的代表.

**Type:** Learn + Build | **类型:** 学习 + 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 10 (Diffusion), Phase 4 Lesson 12 (Video Understanding), Phase 4 Lesson 23 (DiT + Rectified Flow) | **前置知识:** Phase 4 Lesson 10（扩散模型），Phase 4 Lesson 12（视频理解），Phase 4 Lesson 23（DiT + 整流流）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 解释纯视频生成模型 (Sora 2) 和动作条件的世界模型 (Genie 3, DreamerV3) 的区别
- 描述视频的DIT:空间时间补丁,3D位置编码,跨 (T,H,W) 代币的联合关注
- 追踪世界模型如何连接到机器人:VLM计划 →视频模型模拟 →反向动态发射行动
- 选择Sora 2,Genie 3,跑道GWM-1世界,Wan-Video和HunyuanVideo之间的特定使用情况 (创意视频,交互式模拟,自动驾驶合成)

> **【中文解读】**学习目标列出了课程完成后应掌握的核心能力.建议在开始学习前先浏览目标,学习完后对照检查是否已实现.


## 问题 问题引入

视频生成和世界建模将在2026年融合. 一个能够生成一个连贯的视频分钟的模型, 从某种意义上讲, 已经学会了世界如何移动:物体永久性,重力,因果性,风格. 如果您将这些预测条件定为行动 (左步,打开门), 视频模型将成为一个可学习的模拟器,

> 视频生成和世界建模在2026年融合了. 一个可以生成一分钟连贯视频的模型在某种意义上学会了世界如何运动:物体持久性,重力,因果关系,风格.如果你在预测上以动作条件 ((向左走、开门),视频模型就变成了一个可学习的模拟器,可以替代游戏引擎,驾驶模拟器或机器环境.

注是具体的. 基尼3从一个图像中生成可播放环境. 跑道GWM-1世界合成无限的可探索场景. 索拉2制作了长达几分钟的视频, 对于自动驾驶车辆训练数据,NVIDIA Cosmos-Drive,Wayve Gaia-2和Tesla DrivingWorld生成了现实驾驶视频. 机器人系统正在静地接管现实化.

> 利害关系是具体的. 基因3从单张图像生成可玩环境. 跑道GWM-1世界 合成无限可探索场景. 索拉 2 生成带同步音频和物理建模的分钟级视频.

这一课是第四阶段的"大图片"课程. 它将图像生成,视频理解和代理推理连接到主导研究正在发展的建筑模式中.

> 本课程是第四阶段的"全景"课程. 它将图像生成,视频理解和智能体推理连接到主导研究正在发展的架构模式.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


### 世界模型的三个家庭

```mermaid
flowchart LR
    subgraph GEN["Pure video generation"]
        G1["Text / image prompt"] --> G2["Video DiT"] --> G3["Video frames"]
    end
    subgraph ACTION["Action-conditioned world model"]
        A1["Past frames + action"] --> A2["Latent-action video DiT"] --> A3["Next frames"]
        A3 --> A1
    end
    subgraph RL["World models for RL (DreamerV3)"]
        R1["State + action"] --> R2["Latent transition model"] --> R3["Next latent + reward"]
        R3 --> R1
    end

    style GEN fill:#dbeafe,stroke:#2563eb
    style ACTION fill:#fef3c7,stroke:#d97706
    style RL fill:#dcfce7,stroke:#16a34a
```

- **Sora 2**没有动作接口,在部署中无法"引导".
  翻译: 中文**Sora 2**没有动作接口,你无法在生成过程中"操控"它.
- **Genie 3**现在**GWM-1 Worlds**现在**Mirage / Magica**互动式 你按键或移动相机,场景响应.
  翻译: 中文**Genie 3**,我知道.**GWM-1 Worlds**,我知道.**Mirage / Magica**动作条件化的世界模型. 从观察到的视频推断潜在动作,然后使用动作条件化未来预测.
- **DreamerV3**通过一个奖励信号训练,在隐藏的空间中预测. 视觉较少,更有用的样本效率的RL.
  翻译: 中文**DreamerV3**和经典RL世界模型家族在潜空间预测,带显式动作条件化,在奖励信号上训练――视觉性较弱;对样本高效RL更有用――

### 视频 设计

```
Video latent:          (C, T, H, W)
Patchify (spatial):    grid of P_h x P_w patches per frame
Patchify (temporal):   group P_t frames into a temporal patch
Resulting tokens:      (T / P_t) * (H / P_h) * (W / P_w) tokens
```

位置编码是3D:每 (t, h, w) 坐标的旋转或学习嵌入.注意力可以是:

- **Full joint**所有代币都会关注所有代币. O  N ^ 2 具有 N 代币.禁止长视频.
  翻译: 中文**全联合**所有代币 注意所有代币――O(N^2)――对长视频不可行――
- **Divided**交替时间注意 (时间间位置相同:`(H*W) * T^2`空间关注 (同一时间段,跨空间:`T * (H*W)^2`时光former和大多数视频节目.
  翻译: 中文**分离**交换时间注意力(同一个空间位置,跨时间) 和空间注意力(同一个时间步,跨空间) ――TimeSformer 和大多数视频 DiT 使用────
- **Window** (t, h, w) 中的本地窗户.
  翻译: 中文**窗口**(t,h,w) 中的局部窗口──视频Swin 使用──

每个2026年视频传播模型都使用了以下三个模式之一,加上AdaLN调节 (课3) 和修改流.

> 每个2026年的视频扩散模型都使用了这三个模式之一,加上AdaLN 条件化 (第23课) 和整流.

### 行动条件:隐藏行动模式

精灵学会了什么?**latent action**模型的解码器则在推断的隐藏行动而不是明确键盘键上进行条件.在推断时,用户可以指定隐藏行动 (或从新先前的样本中进行一个) 模型生成与该行动一致的下一个框架.

索拉完全跳过了操作界面.它的解码器预测了过去的空间时间代币的下一个空间时间代币.

### 物理可靠性

苏拉2的2026年发布明确宣告**physical plausibility**通过手动评级可靠性分数测量;模型明显改善了落下的物体,字符碰撞和故意失败 (错过跳跃) 情况.

合理性仍然是主导的失败模式.2024-2025年人们吃西瓜或喝杯的视频显示了模型缺乏持久的对象表示.2026年模型 (索拉2,跑道Gen-5,洪源视频) 减少但不消除这些.

### 自动驾驶世界车型

驾驶世界模型可以根据轨迹,界限框或导航地图生成现实道路场景.

- **Cosmos-Drive-Dreams**生成几分钟的驾驶视频用于RL训练.
- **Gaia-2** 轨迹条件的场景合成,用于政策评估.
- **DrivingWorld**模拟各种天气,日间时间,交通条件.
- **Vista**反应驾驶场景合成.

它们取代了昂贵的真实数据收集, 对于角落的案例, 晚上行人走路,冰的交叉路口,

> 它们取代了昂贵的真实世界数据收集,以处理边缘情况.

### 机器人堆:VLM+视频模型+反向动态

现在,我们正在研究一个新的机器人循环.

> 新兴的三组件机器人循环:

1. **VLM**分析目标 ("挑起红杯"),计划高层次的行动序列.
   翻译: 中文**VLM**解析目标:"拿起红色杯子"),规划高层动作序列──
2. **Video generation model**预测未来的观察 N 框架.
   翻译: 中文**视频生成模型**模拟执行每动作后样子预测 N 后观测──
3. **Inverse dynamics model**引擎指令将产生这些观察.
   翻译: 中文**逆动力学模型**提取产生这些观测的具体电机指令.

这取代了奖励形状和样本重的RL.世界模型是想象力;反动动态关闭了动作循环.精灵设想器是一个实例;许多研究小组正在融合这个结构.

> 这取代了奖励塑形和样本密集的RL. 世界模型负责想象;逆动力学关闭环到执行.

### 评估

- **Visual quality**FVD (Fréchet视频距离),用户研究.
  翻译: 中文**视觉质量**FVD(Fréchet 视频距离) 、用户研究。
- **Prompt alignment**每框的CLIPS分,VQA类型的评估.
  翻译: 中文**提示对齐**每CLIPScore、VQA 风格评估──
- **Physical plausibility**在基准组上进行手动评级 (索拉2内部基准,VBench).
  翻译: 中文**物理合理性**在基准套件上人工评分
- **Controllability**行动 →观察一致性;你能回到以前的状态吗?
  翻译: 中文**可控性**动作→观测一致性;能否回到前前的状态?

### 2026年样式景观

| Model | Use | Parameters | Output | License |
|-------|-----|------------|--------|---------|
| Sora 2 | text-to-video, audio | — | 1-min 1080p + audio | API only |
| Runway Gen-5 | text/image-to-video | — | 10s clips | API |
| Runway GWM-1 Worlds | interactive world | — | infinite 3D rollout | API |
| Genie 3 | interactive world from image | 11B+ | playable frames | research preview |
| Wan-Video 2.1 | open text-to-video | 14B | high-quality clips | non-commercial |
| HunyuanVideo | open text-to-video | 13B | 10s clips | permissive |
| Cosmos / Cosmos-Drive | autonomous driving sim | 7-14B | driving scenes | NVIDIA open |
| Magica / Mirage 2 | AI-native game engine | — | modifiable worlds | product |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：工业部署中的视觉系统】**在实际工业部署中,视觉模型需要考虑推迟模型大小的边缘设备适应等问题.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――标签工作室、CVAT是主流标签工具――在工业场景中,主动学习(主动学习) 可以减少标签成本:模型对不确定的样本请求人工标签,确定性的样本自动标签――




## 建立它,实现它.
```figure
v4-world-rollout
```

## 建立它

### 步骤1: 3D 贴合视频

```python
import torch
import torch.nn as nn


class VideoPatch3D(nn.Module):
    def __init__(self, in_channels=4, dim=64, patch_t=2, patch_h=2, patch_w=2):
        super().__init__()
        self.proj = nn.Conv3d(
            in_channels, dim,
            kernel_size=(patch_t, patch_h, patch_w),
            stride=(patch_t, patch_h, patch_w),
        )
        self.patch_t = patch_t
        self.patch_h = patch_h
        self.patch_w = patch_w

    def forward(self, x):
        # x: (N, C, T, H, W)
        x = self.proj(x)
        n, c, t, h, w = x.shape
        tokens = x.reshape(n, c, t * h * w).transpose(1, 2)
        return tokens, (t, h, w)
```

具有步骤等于内核的3D卷轴作为空间时间补丁器. `(T, H, W) -> (T/2, H/2, W/2)`电池的电池.

### 步骤2: 3D旋转位置编码

单独应用的旋转位置嵌入式 (RoPE) `t`现在`h`现在`w`轴:

```python
def rope_3d(tokens, t_dim, h_dim, w_dim, grid):
    """
    tokens: (N, T*H*W, D)
    grid: (T, H, W) sizes
    t_dim + h_dim + w_dim == D
    """
    T, H, W = grid
    n, seq, d = tokens.shape
    if t_dim + h_dim + w_dim != d:
        raise ValueError(f"t_dim+h_dim+w_dim ({t_dim}+{h_dim}+{w_dim}) must equal D={d}")
    assert seq == T * H * W
    t_idx = torch.arange(T, device=tokens.device).repeat_interleave(H * W)
    h_idx = torch.arange(H, device=tokens.device).repeat_interleave(W).repeat(T)
    w_idx = torch.arange(W, device=tokens.device).repeat(T * H)
    # Simplified: just scale channels by frequencies. Real RoPE rotates pairs.
    freqs_t = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(t_dim // 2, device=tokens.device) / (t_dim // 2))
    freqs_h = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(h_dim // 2, device=tokens.device) / (h_dim // 2))
    freqs_w = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(w_dim // 2, device=tokens.device) / (w_dim // 2))
    emb_t = torch.cat([torch.sin(t_idx[:, None] * freqs_t), torch.cos(t_idx[:, None] * freqs_t)], dim=-1)
    emb_h = torch.cat([torch.sin(h_idx[:, None] * freqs_h), torch.cos(h_idx[:, None] * freqs_h)], dim=-1)
    emb_w = torch.cat([torch.sin(w_idx[:, None] * freqs_w), torch.cos(w_idx[:, None] * freqs_w)], dim=-1)
    return tokens + torch.cat([emb_t, emb_h, emb_w], dim=-1)
```

简单的添加形式:真正的ROPE在频率上旋转对通道;位置信息相同.

### 步骤3: 分开注意力

```python
class DividedAttentionBlock(nn.Module):
    def __init__(self, dim=64, heads=2):
        super().__init__()
        self.time_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.space_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.ln1 = nn.LayerNorm(dim)
        self.ln2 = nn.LayerNorm(dim)
        self.ln3 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Linear(4 * dim, dim))

    def forward(self, x, grid):
        T, H, W = grid
        n, seq, d = x.shape
        # time attention: same (h, w), across t
        xt = x.view(n, T, H * W, d).permute(0, 2, 1, 3).reshape(n * H * W, T, d)
        a, _ = self.time_attn(self.ln1(xt), self.ln1(xt), self.ln1(xt), need_weights=False)
        xt = (xt + a).reshape(n, H * W, T, d).permute(0, 2, 1, 3).reshape(n, seq, d)
        # space attention: same t, across (h, w)
        xs = xt.view(n, T, H * W, d).reshape(n * T, H * W, d)
        a, _ = self.space_attn(self.ln2(xs), self.ln2(xs), self.ln2(xs), need_weights=False)
        xs = (xs + a).reshape(n, T, H * W, d).reshape(n, seq, d)
        xs = xs + self.mlp(self.ln3(xs))
        return xs
```

时间注意力在每个空间位置之间随时;空间注意力在每个框架之间随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随的随时随时随时随时随时随时随时随时随时随的随时随时随时随的随时随时随时随时随的随时随时随的随时随时随时随的随时随的随时随的随时随的随时随时随的随时随时随的随的随时随的随时随的随时随时随的随的随时随的随的随时随时随的随时随时随的随时随的随的随的随时随的随的随时随之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之之

### 步骤4:编写一个小视频

```python
class TinyVideoDiT(nn.Module):
    def __init__(self, in_channels=4, dim=64, depth=2, heads=2):
        super().__init__()
        self.patch = VideoPatch3D(in_channels=in_channels, dim=dim, patch_t=2, patch_h=2, patch_w=2)
        self.blocks = nn.ModuleList([DividedAttentionBlock(dim, heads) for _ in range(depth)])
        self.out = nn.Linear(dim, in_channels * 2 * 2 * 2)

    def forward(self, x):
        tokens, grid = self.patch(x)
        for blk in self.blocks:
            tokens = blk(tokens, grid)
        return self.out(tokens), grid
```

没有一个工作的视频生成器;一个结构性演示,

### 步骤5:检查形状

```python
vid = torch.randn(1, 4, 8, 16, 16)  # (N, C, T, H, W)
model = TinyVideoDiT()
out, grid = model(vid)
print(f"input  {tuple(vid.shape)}")
print(f"tokens grid {grid}")
print(f"output {tuple(out.shape)}")
```

期待`grid = (4, 8, 8)`其他`out = (1, 256, 32)`之后,头部将其投射到每代币的空间时间补丁, 准备好重新重新被放入视频中.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：视觉模型的持续学习】**在生产环境中,视觉模型需要不断适应新数据. 持续学习. 持续学习. 技术可以防止模型在适应新数据时忘记旧知识.

## 用它实现框架

2026年生产准入模式:

- **Sora 2 API**文字到视频,同步音频.
- **Runway Gen-5 / GWM-1**视频互动世界.
- **Wan-Video 2.1 / HunyuanVideo**开源自主主机.
- **Cosmos / Cosmos-Drive**驾驶模拟开放权重.
- **Genie 3**研究预览,请求访问.

为了构建一个互动的世界模型演示:从 Wan-Video开始,以提供质量,在隐形动作适配器上进行交互性.

对于机器人, 野生的堆:

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


1. 语言目标 -> VLM (Qwen3-VL) -> 高级计划.
2. 计划 -> 隐形行动视频模型 -> 想象中的部署.
3. 推出 -> 反动态模型 -> 低级操作.
4. 执行的操作 -> 观察返回步骤1.



## 运送它.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


这一课产生了:

- `outputs/prompt-video-model-picker.md`选择Sora 2 / 跑道 / 瓦恩 / 洪源视频 / 宇宙给任务,许可证和延迟.
- `outputs/skill-physical-plausibility-checks.md`定义自动检查 (物体永久性,重力,连续性) 在发送之前运行任何生成的视频的技能.

## 练习题

1. **(Easy)**计算5秒 360p视频的代币数量在补丁 t=2,补丁 h=8,补丁 w=8.
2. **(Medium)**换上方的分离注意力块,以获得一个完整的关联注意力块,并测量形状和参数数.解释为什么在真实视频模型中需要分离注意力.
3. **(Hard)**建立一个最小的隐形动作视频模型:采用 (frame_t, action_t, frame_{t+1}) 三倍的数据集 (任何简单的2D游戏),训练一个微小的视频DiT,以动作嵌入为条件,并显示不同的动作产生不同的下一个框架.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| World model | "Learned simulator" | A model that predicts future observations given state and action |
| Video DiT | "Spacetime transformer" | Diffusion transformer with 3D patchification and divided attention |
| Latent action | "Inferred control" | Discrete or continuous action latent inferred from frame pairs; used to condition next-frame generation |
| Divided attention | "Time then space" | Two attention operations per block — across time then across space — to keep O(N^2) manageable |
| Object permanence | "Things stay real" | Scene property that video models must learn; classic failure mode on food, glassware |
| FVD | "Fréchet Video Distance" | Video equivalent of FID; primary visual quality metric |
| Inverse dynamics model | "Observations to actions" | Given (state, next state), output the action that connects them; closes robotics loop |
| Cosmos-Drive | "NVIDIA driving sim" | Open-weights autonomous-driving world model for RL and evaluation |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Sora technical report (OpenAI)](https://openai.com/index/video-generation-models-as-world-simulators/)
- [Genie: Generative Interactive Environments (Bruce et al., 2024)](https://arxiv.org/abs/2402.15391)隐藏的行动世界模型
- [TimeSformer (Bertasius et al., 2021)](https://arxiv.org/abs/2102.05095) 视频转换器的重视
- [DreamerV3 (Hafner et al., 2023)](https://arxiv.org/abs/2301.04104)全球RL模型
- [Cosmos-Drive-Dreams (NVIDIA, 2025)](https://research.nvidia.com/labs/toronto-ai/cosmos-drive-dreams/)驾驶世界模式
- [Top 10 Video Generation Models 2026 (DataCamp)](https://www.datacamp.com/blog/top-video-generation-models)
- [From Video Generation to World Model — survey repo](https://github.com/ziqihuangg/Awesome-From-Video-Generation-to-World-Model/)
