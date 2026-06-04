# 评估指标 — FID、CLIP Score 与人类偏好

> 每个生成模型排行榜都引用 FID（Fréchet Inception Distance）、CLIP Score 和人类偏好竞技场的胜率。每个指标都有可以被研究者刷的漏洞。不了解这些漏洞，就无法区分真正的改进和刷榜。

> **【中文解读】** 每个生成模型排行榜都引用 FID（Fréchet Inception Distance）、CLIP Score 和人类偏好胜率。每个指标都有可以被刷的漏洞。不了解这些漏洞，就无法区分真正的改进和刷榜。

> **【拓展：FID 的局限性】** FID 衡量生成图像与真实图像的分布距离，但它可以被优化（如选择性地生成高分样本）。人类偏好评估（如 Chatbot Arena 模式）是更可靠但更昂贵的替代方案。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 8 · 01（分类）、阶段 2 · 04（评估指标）
**预计时间：** ~45 分钟

## 问题引入

生成模型以*样本质量*和*条件遵循度*来评判。两者都没有闭合形式的度量。你的模型需要生成 10,000 张图像；必须有东西给它们打分；你必须信任这些分数在模型家族、分辨率、架构之间是可比的。三个指标经受住了 2014-2026 年的考验：

- **FID (Fréchet Inception Distance)。** 真实分布和生成分布在 Inception 网络特征空间中的距离。越低越好。
- **CLIP Score。** 生成图像的 CLIP 图像嵌入与提示的 CLIP 文本嵌入之间的余弦相似度。越高越好。衡量提示遵循度。
- **人类偏好。** 让两个模型在相同提示上对决，由人类（或 GPT-4 级模型）选择更好的，聚合为 Elo 分数。

你还会看到：IS (Inception Score，基本已淘汰)、KID、CMMD、ImageReward、PickScore、HPSv2、MJHQ-30k。每个都修正了前一个的某个缺陷。

> **【中文解读】** 生成模型评估的三大指标：(1) FID——在 Inception 网络特征空间中衡量生成分布与真实分布的距离，越低越好；(2) CLIP Score——生成图像与文本 prompt 的语义匹配度，越高越好；(3) 人类偏好——两个模型对比选择更好的，聚合为 Elo 分数。每个指标都有已知漏洞，组合使用更可靠。

> **【拓展：生成模型评估的"刷榜"问题】** FID 可以被优化——通过选择性地生成高分样本、调整 Inception 模型的特征层、或过拟合到参考分布。CLIP Score 也有偏差——CLIP 模型对某些概念更敏感。人类偏好评估（如 Artificial Analysis 的 Arena）是最可靠但最昂贵的方法。2026 年的趋势是使用 GPT-4 级别模型作为"自动评判员"来近似人类偏好。

## 核心概念

![FID、CLIP 与偏好：三个维度，不同的失败模式](../assets/evaluation.svg)

### FID — 样本质量

Heusel et al.（2017）。步骤：

1. 提取 N 张真实图像和 N 张生成图像的 Inception-v3 特征（2048 维）。
2. 对每个池拟合高斯分布：计算均值 `μ_r, μ_g` 和协方差 `Σ_r, Σ_g`。
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`。

解释：特征空间中两个多元高斯之间的 Fréchet 距离。越低 = 分布越相似。

失败模式：
- **小 N 时的偏差。** FID 是特征分布上的均方误差——小 N 低估协方差，给出虚假的低 FID。始终使用 N ≥ 10,000。
- **依赖 Inception。** Inception-v3 在 ImageNet 上训练。远离 ImageNet 的领域（人脸、艺术、文本图像）产生无意义的 FID。使用领域特定的特征提取器。
- **刷榜。** 对 Inception 先验过拟合可以在不改善视觉质量的情况下获得低 FID。用 CMMD（见下文）击败。

### CLIP Score — 提示遵循度

Radford et al.（2021）。对于生成图像 + 提示：

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

在 30k 张生成图像上平均 → 一个可在模型间比较的标量。

失败模式：
- **CLIP 自身的盲点。** CLIP 的组合推理能力弱（"红色方块上的蓝色球体"经常失败）。模型可以在 CLIP Score 上排名很好但并未真正遵循复杂提示。
- **短提示偏差。** 短提示在自然中与 CLIP 图像匹配更多。长提示机械性地有更低的 CLIP Score。
- **提示刷榜。** 在提示中包含"高质量，4k，杰作"会在不改善图文绑定的情况下虚增 CLIP Score。

CMMD (Jayasumana et al., 2024) 修复了其中一些问题：使用 CLIP 特征而非 Inception，最大均值差异 (MMD) 而非 Fréchet 距离。检测微妙质量差异的能力更强。

### 人类偏好 — 真理标准

选取一组提示。用模型 A 和模型 B 生成。向人类（或强 LLM 评判）展示配对。将胜场聚合为 Elo 或 Bradley-Terry 分数。基准：

- **PartiPrompts (Google)**：1,600 个多样提示，12 个类别。
- **HPSv2**：107k 人类标注，广泛用作自动化代理。
- **ImageReward**：137k 提示-图像偏好对，MIT 许可。
- **PickScore**：在 Pick-a-Pic 260 万偏好上训练。
- **Chatbot-Arena 风格图像竞技场**：https://imagearena.ai/ 等。

失败模式：
- **评判者方差。** 非专家与专家有不同偏好。两者都用。
- **提示分布。** 精心挑选的提示有利于某个家族。始终记录。
- **LLM 评判奖励黑客。** GPT-4 评判被漂亮但错误的输出愚弄。与人类交叉验证。

## 组合使用

一份生产评估报告应包括：

1. 在 10-30k 样本上相对保留真实分布的 FID（样本质量）。
2. 相同样本相对其提示的 CLIP Score / CMMD（遵循度）。
3. 在盲测竞技场中相对前一代模型的胜率（总体偏好）。
4. 失败模式分析：50 个随机抽样的输出，标记已知问题（手部解剖、文字渲染、一致的物体计数）。

任何单一指标都是谎言。三个相互验证的指标 + 定性审查才是一项声明。

## 动手实现

`code/main.py` 在合成"特征向量"上实现了 FID、类 CLIP Score 和 Elo 聚合（我们使用 4 维向量作为 Inception 特征的替身）。你可以看到：

- 在小 N 和大 N 上的 FID 计算——偏差。
- "CLIP Score"作为特征池之间的余弦相似度。
- 从合成偏好流中的 Elo 更新规则。

### 步骤 1：四行 FID

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

### 步骤 2：CLIP 风格余弦相似度

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

### 步骤 3：Elo 聚合

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

## 常见陷阱

- **N=1000 时的 FID。** 启发式规则在 N < 10k 时不可靠。报告低 N FID 的论文在刷榜。
- **跨分辨率比较 FID。** Inception 的 299×299 缩放改变了特征分布。只在匹配分辨率下比较。
- **只报告一个种子。** 至少运行 3 个种子。报告标准差。
- **通过负面提示虚增 CLIP Score。** 某些流水线通过过度拟合提示来提升 CLIP Score。检查视觉饱和度。
- **Elo 的提示重叠偏差。** 如果两个模型在训练中都见过基准测试提示，Elo 就没有意义。使用保留的提示集。
- **人类评估付费众包偏差。** Prolific、MTurk 标注者偏向更年轻/技术友好。混入招募的艺术/设计专家。

## 用框架实现

2026 年生产评估协议：

| 支柱 | 最低要求 | 推荐 |
|--------|---------|-------------|
| 样本质量 | 10k vs 保留真实的 FID | + 5k 上的 CMMD + 每类别子集的 FID |
| 提示遵循度 | 30k 上的 CLIP Score | + HPSv2 + ImageReward + VQA 风格问答 |
| 偏好 | 200 个盲测配对 vs 基线 | + 2000 配对人类 + LLM 评判 + Chatbot Arena |
| 失败分析 | 50 个人工标记 | 500 个人工标记 + 自动化安全分类器 |

一份报告中包含全部四个支柱 = 声明。单独任何一个 = 营销。

## 产出物

保存 `outputs/skill-eval-report.md`。技能接收新模型检查点 + 基线，输出完整评估计划：样本量、指标、失败模式探查、签署标准。

## 练习题

1. **简单。** 运行 `code/main.py`。比较相同合成分布在 N=100 vs N=1000 时的 FID。报告偏差幅度。
2. **中等。** 从合成 CLIP 风格特征实现 CMMD（公式见 Jayasumana et al., 2024）。比较相对 FID 对质量差异的敏感度。
3. **困难。** 复制 HPSv2 设置：从 Pick-a-Pic 子集取 1000 个图像-提示对，在偏好上微调一个小型基于 CLIP 的评分器，测量其与保留集的一致性。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | 真实 vs 生成 Inception 特征高斯拟合的 Fréchet 距离。 |
| CLIP Score | "图文相似度" | CLIP 图像和文本嵌入之间的余弦相似度。 |
| CMMD | "FID 的替代" | CLIP 特征 MMD；偏差更小，无高斯假设。 |
| IS | "Inception Score" | Exp KL(p(y\|x) \|\| p(y))；在现代模型上相关性差，已淘汰。 |
| HPSv2 / ImageReward / PickScore | "学习的偏好代理" | 在人类偏好上训练的小型模型；用作自动评判。 |
| Elo | "棋类评分" | 配对胜场的 Bradley-Terry 聚合。 |
| PartiPrompts | "基准提示集" | Google 策划的跨 12 个类别的 1,600 个提示。 |
| FD-DINO | "自监督替代" | 使用 DINOv2 特征的 FD；对 ImageNet 外领域更好。 |

## 生产笔记：评估也是推理工作负载

在 10k 样本上运行 FID 意味着生成 10k 张图像。对于 50 步的 SDXL base 在 1024² 上使用单张 L4，这约 11 小时的单请求推理。评估预算是真实的，框架完全是离线推理场景（最大化吞吐量，忽略 TTFT）：

- **硬批处理，忘掉延迟。** 离线评估 = 以适配内存的最大大小的静态批处理。在 80GB H100 上 `pipe(...).images` 使用 `num_images_per_prompt=8` 比单请求快 4-6 倍实际耗时。
- **缓存真实特征。** 在真实参考集上的 Inception（FID）或 CLIP（CLIP Score, CMMD）特征提取只运行*一次*，存储为 `.npz`。不要每次评估都重新计算。

对于 CI / 回归门：每个 PR 运行 500 样本子集的 FID + CLIP Score（约 30 分钟）；每晚运行完整 10k FID + HPSv2 + Elo。

## 延伸阅读

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) — FID 论文。
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) — CMMD。
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) — CLIP。
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) — HPSv2。
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) — ImageReward。
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) — PartiPrompts。
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) — 失败模式综述。
