# Evaluation — FID, CLIP Score, Human Preference | 评估指标 — FID、CLIP Score 与人类偏好

> Every generative model leaderboard cites FID, CLIP score, and a win rate from a human-preference arena. Each number has a failure mode a determined researcher can game. If you do not know the failure modes, you cannot tell a real improvement from a gaming run.

> **【中文解读】** 每个生成模型排行榜都引用 FID（Fréchet Inception Distance）、CLIP Score 和人类偏好胜率。每个指标都有可以被刷的漏洞。不了解这些漏洞，就无法区分真正的改进和刷榜。

> **【拓展：FID 的局限性】** FID 衡量生成图像与真实图像的分布距离，但它可以被优化（如选择性地生成高分样本）。人类偏好评估（如 Chatbot Arena 模式）是更可靠但更昂贵的替代方案。

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

A generative model is judged on *sample quality* and *conditioning adherence*. Neither has a closed-form measure. Your model has to render 10,000 images; something has to assign them numbers; you have to trust the numbers across model families, across resolutions, across architectures. Three metrics survived the 2014-2026 gauntlet:

> 生成模型以*样本质量*和*条件遵循度*评判。两者都没有闭式度量。你的模型必须渲染 10000 张图像；必须有东西给它们打分。三个指标经历了 2014-2026 的考验：

- **FID (Fréchet Inception Distance).** A distance between two distributions — real and generated — in an Inception network's feature space. Lower is better.
  **FID。** 真实和生成分布在 Inception 网络特征空间中的距离。越低越好。
- **CLIP score.** Cosine similarity between a generated image's CLIP-image embedding and a prompt's CLIP-text embedding. Higher is better. Measures prompt adherence.
  **CLIP Score。** 生成图像与文本 prompt 的 CLIP 嵌入余弦相似度。越高越好。
- **Human preference.** Pit two models head-to-head on the same prompt, have humans (or a GPT-4-class model) pick the better one, aggregate to an Elo score.
  **人类偏好。** 两个模型头对头对比，人类或 GPT-4 级模型选择更好的，聚合为 Elo 分数。

You will also see: IS (inception score, largely retired), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Each corrects for one failure of the previous.

> 你还会看到：IS（已基本退役）、KID、CMMD、ImageReward、PickScore、HPSv2 等。每个都修正了前一个的某种缺陷。

> **【中文解读】** 生成模型评估的三大指标：(1) FID——在 Inception 网络特征空间中衡量生成分布与真实分布的距离，越低越好；(2) CLIP Score——生成图像与文本 prompt 的语义匹配度，越高越好；(3) 人类偏好——两个模型对比选择更好的，聚合为 Elo 分数。每个指标都有已知漏洞，组合使用更可靠。

> **【拓展：生成模型评估的"刷榜"问题】** FID 可以被优化——通过选择性地生成高分样本、调整 Inception 模型的特征层、或过拟合到参考分布。CLIP Score 也有偏差——CLIP 模型对某些概念更敏感。人类偏好评估（如 Artificial Analysis 的 Arena）是最可靠但最昂贵的方法。2026 年的趋势是使用 GPT-4 级别模型作为"自动评判员"来近似人类偏好。

## The Concept | 核心概念

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### FID — sample quality | FID — 样本质量

Heusel et al. (2017). Steps:

> Heusel 等人（2017）。步骤：

1. Extract Inception-v3 features (2048-D) for N real images and N generated.
   为 N 张真实图像和 N 张生成图像提取 Inception-v3 特征（2048 维）。
2. Fit a Gaussian to each pool: compute mean `μ_r, μ_g` and covariance `Σ_r, Σ_g`.
   对每个池拟合高斯：计算均值 `μ_r, μ_g` 和协方差 `Σ_r, Σ_g`。
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`.
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`。

Interpretation: Fréchet distance between two multivariate Gaussians in feature space. Lower = more similar distributions.

> 解读：特征空间中两个多元高斯分布之间的 Fréchet 距离。越低 = 分布越相似。

Failure modes:

> 失败模式：

- **Biased on small N.** FID is mean-squared over the feature distribution — small N under-estimates covariance, gives falsely low FID. Always use N ≥ 10,000.
  小 N 偏差：FID 是特征分布上的均方误差，小 N 会低估协方差，给出虚假的低 FID。务必使用 N ≥ 10,000。
- **Inception-dependent.** Inception-v3 was trained on ImageNet. Domains far from ImageNet (faces, art, text images) produce meaningless FID. Use a domain-specific feature extractor.
  依赖 Inception：Inception-v3 在 ImageNet 上训练。远离 ImageNet 的领域（人脸、艺术、文字图像）会产生无意义的 FID。使用领域特定的特征提取器。
- **Gaming.** Overfitting to the Inception prior gives low FID without visual quality improvement. Beat it with CMMD (below).
  刷分：对 Inception 先验过拟合能给出低 FID 但视觉质量没有提升。用下面的 CMMD 击败它。

### CLIP score — prompt adherence | CLIP Score — Prompt 遵循度

Radford et al. (2021). For a generated image + prompt:

> Radford 等人（2021）。对于生成图像 + prompt：

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

Average across 30k generated images → a scalar comparable between models.

> 对 30k 张生成图像求平均 → 一个可在模型间比较的标量。

Failure modes:

> 失败模式：

- **CLIP's own blind spots.** CLIP has weak compositional reasoning ("a red cube on a blue sphere" often fails). Models can rank well on CLIP score without really following complex prompts.
  CLIP 自身的盲点：CLIP 组合推理能力弱（"红色立方体在蓝色球体上"经常失败）。模型可以在 CLIP Score 上排名靠前但实际并未真正遵循复杂 prompt。
- **Short prompt bias.** Short prompts have more CLIP-image matches in the wild. Longer prompts have lower CLIP scores mechanically.
  短 prompt 偏差：短 prompt 在野外有更多 CLIP-image 匹配。长 prompt 在 CLIP Score 上机械性地更低。
- **Prompt gaming.** Including "high quality, 4k, masterpiece" in the prompt inflates CLIP score without improving image-text binding.
  Prompt 刷分：在 prompt 中加入 "high quality, 4k, masterpiece" 能抬高 CLIP Score 而不改善图文绑定。

CMMD (Jayasumana et al., 2024) fixes some of these: uses CLIP features instead of Inception, maximum-mean discrepancy instead of Fréchet. Better at detecting subtle quality differences.

> CMMD（Jayasumana 等人 2024）修正了其中一些问题：使用 CLIP 特征而非 Inception，使用 MMD（最大均值差异）而非 Fréchet 距离。更善于检测细微的质量差异。

### Human preference — the ground truth | 人类偏好 — 地面真值

Pick a pool of prompts. Generate with model A and model B. Show pairs to humans (or a strong LLM judge). Aggregate wins into an Elo or Bradley-Terry score. Benchmarks:

> 选一批 prompt。用模型 A 和模型 B 生成。把成对结果展示给人类（或强 LLM 评判）。把胜场聚合为 Elo 或 Bradley-Terry 分数。基准：

- **PartiPrompts (Google)**: 1,600 diverse prompts, 12 categories.
  **PartiPrompts（Google）**：1600 个多样化 prompt，12 个类别。
- **HPSv2**: 107k human annotations, widely used as automated proxy.
  **HPSv2**：10.7 万条人类标注，广泛用作自动代理。
- **ImageReward**: 137k prompt-image preference pairs, MIT-licensed.
  **ImageReward**：13.7 万对 prompt-图像偏好对，MIT 许可。
- **PickScore**: trained on Pick-a-Pic 2.6M preferences.
  **PickScore**：在 Pick-a-Pic 260 万条偏好上训练。
- **Chatbot-Arena-style image arenas**: https://imagearena.ai/ and others.
  **Chatbot-Arena 风格的图像竞技场**：https://imagearena.ai/ 等。

Failure modes:

> 失败模式：

- **Judge variance.** Non-experts have different preferences than experts. Use both.
  评判者方差：非专家和专家有不同偏好。两者都用。
- **Prompt distribution.** Cherry-picked prompts favor one family. Always document.
  Prompt 分布：精心挑选的 prompt 会偏向某一家族。务必记录。
- **LLM-judge reward hacking.** GPT-4-judge gets fooled by pretty-but-wrong outputs. Triangulate with human.
  LLM 评判被刷分：GPT-4 评判会被 "好看但错" 的输出欺骗。与人类三角验证。

## Use together | 组合使用

A production eval report should include:

> 一份生产级评估报告应包含：

1. FID on 10-30k samples against a held-out real distribution (sample quality).
   在 10-30k 样本上相对留出真实分布的 FID（样本质量）。
2. CLIP score / CMMD on the same samples vs their prompts (adherence).
   相同样本相对各自 prompt 的 CLIP Score / CMMD（遵循度）。
3. Win rate in a blinded arena vs the previous model (overall preference).
   与前一模型在盲评竞技场中的胜率（整体偏好）。
4. Failure mode analysis: 50 randomly sampled outputs, flagged for known issues (hand anatomy, text rendering, consistent object count).
   失败模式分析：随机采样 50 个输出，标记已知问题（手部解剖、文字渲染、对象计数一致性）。

Any single metric is a lie. Three corroborating metrics + qualitative review are a claim.

> 任何单一指标都是谎言。三个相互印证的指标 + 定性审查才算一个声明。

## Build It | 动手实现

`code/main.py` implements FID, CLIP-score-like, and Elo aggregation on synthetic "feature vectors" (we use 4-D vectors as stand-ins for Inception features). You see:

> `code/main.py` 在合成 "特征向量" 上实现 FID、类 CLIP Score 和 Elo 聚合（我们用 4 维向量代替 Inception 特征）。你会看到：

- FID computation on a small N and on a large N — the bias.
  小 N 和大 N 上的 FID 计算——偏差。
- "CLIP score" as cosine similarity between feature pools.
  作为特征池之间余弦相似度的 "CLIP Score"。
- Elo update rule from a synthetic preference stream.
  来自合成偏好流的 Elo 更新规则。

### Step 1: FID in four lines | 步骤 1：四行 FID

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> 四行 FID：分别对真实和生成特征计算均值与协方差，再算均值差平方加协方差迹。

### Step 2: CLIP-style cosine-similarity | 步骤 2：CLIP 风格余弦相似度

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度：点积除以两个向量范数乘积，加 epsilon 防止除零。

### Step 3: Elo aggregation | 步骤 3：Elo 聚合

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新：基于期望胜率和实际结果调整分数，K=32 是国际象棋标准。

## Pitfalls | 常见陷阱

- **FID at N=1000.** Heuristic is unreliable under N=10k. Papers reporting low-N FID are gaming.
  N=1000 时的 FID：在 N<10k 时不可靠。报告低 N FID 的论文在刷分。
- **Comparing FID across resolutions.** Inception's 299×299 resize changes the feature distribution. Compare at matched resolution only.
  跨分辨率比较 FID：Inception 的 299×299 缩放会改变特征分布。只在匹配分辨率下比较。
- **Reporting one seed.** Run 3 seeds minimum. Report std.
  只报告一个 seed：至少跑 3 个 seed。报告标准差。
- **CLIP score inflation via negative prompts.** Some pipelines boost CLIP by over-fitting the prompt. Check for visual saturation.
  通过负向 prompt 抬高 CLIP Score：有些流水线通过过拟合 prompt 抬高 CLIP。检查视觉饱和。
- **Elo bias from prompt overlap.** If both models saw a benchmark prompt during training, Elo is meaningless. Use held-out prompt sets.
  Prompt 重叠导致的 Elo 偏差：如果两个模型训练时见过基准 prompt，Elo 无意义。使用留出的 prompt 集。
- **Human eval paid-crowd skew.** Prolific, MTurk annotators skew younger / tech-friendly. Mix with recruited art/design experts.
  人工评估付费众包偏差：Prolific、MTurk 标注者偏年轻 / 偏技术友好。混合招募的艺术/设计专家。

## Use It | 用框架实现

Production eval protocol in 2026:

> 2026 年的生产级评估协议：

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

All four pillars in one report = claim. Any one alone = marketing.

> 四个支柱齐全才是一个声明。任何单独一个只是营销。

## Ship It | 产出物

Save `outputs/skill-eval-report.md`. Skill takes a new model checkpoint + baseline and outputs a full eval plan: sample sizes, metrics, failure-mode probes, sign-off criteria.

> 保存为 `outputs/skill-eval-report.md`。该技能接收一个新的模型 checkpoint + 基线，输出完整评估计划：样本数、指标、失败模式探针、签字标准。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Compare FID at N=100 vs N=1000 on the same synthetic distributions. Report bias magnitude.
2. **Medium.** Implement CMMD from synthetic CLIP-style features (see Jayasumana et al., 2024 for the formula). Compare sensitivity to quality differences vs FID.
3. **Hard.** Replicate the HPSv2 setup: take 1000 image-prompt pairs from a subset of Pick-a-Pic, fine-tune a small CLIP-based scorer on the preferences, and measure its agreement with a held-out set.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Production note: evaluation is an inference workload too | 生产笔记：评估也是推理工作负载

Running FID on 10k samples means generating 10k images. For a 50-step SDXL base at 1024² on a single L4, that is ~11 hours of single-request inference. Evaluation budgets are real, and the framing is exactly the offline-inference scenario (maximize throughput, ignore TTFT):

- **Batch hard, forget latency.** Offline eval = static batching at the largest size that fits in memory. `pipe(...).images` with `num_images_per_prompt=8` on an 80GB H100 runs 4-6× faster wall-clock than single-request.
- **Cache the real features.** The Inception (FID) or CLIP (CLIP-score, CMMD) feature extraction over the real reference set is run *once*, stored as a `.npz`. Do not recompute per eval.

For CI / regression gates: run FID + CLIP score on a 500-sample subset per PR (~30 min); run full 10k FID + HPSv2 + Elo nightly.

## Further Reading | 延伸阅读

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) — FID paper.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) — CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) — CLIP.
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) — HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) — ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) — PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) — failure-mode survey.
