# 评价 FID,Clip评分,人类偏好 评价指标 FID,Clip评分与人类偏好

> 每个生成模型排名表都引用了人类偏好领域的FID,CLIP分数和胜利率.每个数字都有一个确定研究人员可以玩的失败模式.如果你不知道失败模式,你无法从游戏运行中辨别真正的改善.

> **【中文解读】**每个生成模型排行榜都引用了FID (Fréchet Inception Distance) ‧CLIP 评分和人类偏好胜率──每一个指标都有可刷的漏洞──不了解这些漏洞,就无法区分真正的改进和刷榜──

> **【拓展：FID 的局限性】**根据FID测量图像生成与真实图像分布距离,但它可以优化 (如选择性生成高分样本) 人类偏好评估 (如Chatbot Arena模式) 较可靠但更昂贵的替代方案.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

生成模型是根据*样本质量*和*条件性依附性来判断的. 无论是没有封闭形式的测量.你的模型必须呈现10,000个图像;有什么东西必须赋予它们数字;你必须相信模型家庭中的数字,在分辨率中,在建筑中.

> 生成模型以*样本质量*和*条件遵循度*评判──两者都没有闭式度量──你的模型必须染10万张图像;必须有东西给它们打分──三个指标经历了2014-2026年的考试:

- **FID (Fréchet Inception Distance).**在Inception网络的功能空间中,两个分布之间的距离 实和生成的距离.较低更好.
  **FID。**真实和生成分布在 网络特征空间中的距离――越低越好――
- **CLIP score.**生成图像的Clip图像嵌入与提示的Clip文本嵌入之间的相似性.较高更好.测量提示遵守.
  **CLIP Score。**生成图像与文本提示的Clip 嵌入余弦相似度──越高越好──
- **Human preference.**让人类 (或GPT-4类型的模型) 选择更好的模型, 总结为Elo分数.
  **人类偏好。**两个模型对对对对,人类或GPT-4级模型选择更好,聚合为Elo 分数.

你还会看到:IS (初始分数,大多退休),KID,CMMD,ImageReward,PickScore,HPSv2,MJHQ-30k. 每个都对前一个失败进行了纠正.

> 你还会看到:IS(已基本退役) ‧KID、CMMD、ImageReward、PickScore、HPSv2等──每个人都修复了前一个的某种缺陷──

> **【中文解读】**生成模型评估的三大指标: 1) FID在初始化网络特征空间中衡量生成分布与真实分布的距离,越低越好; 2) CLIP Score生成图像与文本提示的语义匹配,越高越好; 3) 人类偏好两个模型比选择更好,聚合为 Elo 分数――每个指标都有已知漏洞,组合使用更可靠.

> **【拓展：生成模型评估的"刷榜"问题】**通过选择性生成高分样本"",调整"创建模型的特征层"",或过适合参考分布".CLIP Score 也有偏差.CLIP模型对某些概念更敏感.

## 概念的核心概念

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

###  样品质量

果和其他产品

> 其他们 () 们 (们)

1. 提取Inception-v3功能 (2048-D) 对于N真实图像和N生成的图像.
   为 N 张真实图像和 N 张生成图像提取 开始-v3 特征(2048 维) ⋅
2. 按一个高斯人对每个池:计算平均值`μ_r, μ_g`及共变性`Σ_r, Σ_g`现在,我们要去.
   对每池拟高斯:计算平均值`μ_r, μ_g`和协同差异`Σ_r, Σ_g`,我知道.
3. 子`||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`现在,我们要去.
   子`||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`,我知道.

解释:特征空间中的两个多变量高素之间的弗雷切距离.

> 解读:特征空间中两个多元高斯分布之间的频率距离──越低 = 分布越相似──

失效模式:

> 失败模式:

- **Biased on small N.**平均FID为特征分布小N低估了共差,给出虚假低FID.总是使用N ≥ 10,000.
  小 N 偏差:FID 是特征分布上的平均方差,小 N 会低估协同方差,给出虚假的低 FID──必需使用N ≥ 10,000──
- **Inception-dependent.**开始-v3 在 ImageNet 上进行了训练.远离 ImageNet 的域名 (面孔,艺术,文本图像) 产生无意义的 FID. 使用域名特定的特征提取器.
  根据Inception:Inception-v3 在ImageNet上训练――远离ImageNet的领域 ([[人脸]],艺术、文字图像]]) 将产生无意义的FID――使用领域的特定特征提取器――
- **Gaming.**过度适应初始前,没有改善视觉质量.
  刷分:对Inception先验过拟合能提供低的FID,但视觉质量没有提升.

### 快速遵守 快速遵守

对于生成的图像+提示:

> 对于生成图像+提示:

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

平均30万张生成的图像是模型之间相比的尺度图像.

> 对于30k张生成图像的平均求 → 一个可在模型中比较的标量.

失效模式:

> 失败模式:

- **CLIP's own blind spots.**CLIP 具有较弱的构成推理 ("蓝球上的红立方体"经常失败).模型可以在 CLIP 评分上排名良好,而不会真正遵循复杂的提示.
  蓝球体上的红色立方体经常失败) ――模型可以在CLIP Score上排名靠前,但实际上并没有真正遵循复杂提示――
- **Short prompt bias.**短短的提示在自然界中比较符合Clip图像,而较长的提示在机械上比较低的Clip分数.
  短快速 偏差:短快速 在野外有更多的CLIP图像匹配.
- **Prompt gaming.**包含"高质量,4k,杰作"在提示中,
  快速刷分:在快速中加入"高质量,4K,杰作" 能升高Clip Score而不改善图文绑定──

 CMMD (Jayasumana等,2024) 修复了一些问题:使用CLIP功能而不是Inception,而不是Fréchet的最大平均差异.

> 山等2024年修改了其中一些问题:使用CLIP特征而不是Inception,使用MMD (最大平均值差异)而不是Fréchet 距离.

### 人类偏好 土地真实

选择一个提示池.使用模型A和模型B生成.向人类 (或强大的LLM法官) 展示对. 总结获利成Elo或布拉德利-特里分数. 基准:

> 选择一批提示――用模型A 和模型B 生成――把成对结果展示给人类 (或强 LLM 评判) ――把胜场聚合为Elo 或布拉德利-特里 分数――基准:

- **PartiPrompts (Google)**共有1600个不同的提示,12个类别.
  **PartiPrompts（Google）**其他类型: 类型:
- **HPSv2**据了解,在此之前,
  **HPSv2**据悉,在此之前,
- **ImageReward**根据MIT许可,
  **ImageReward**现在,我在做什么?
- **PickScore**培训者: 选择一个选择的2.6M.
  **PickScore**现在,我们在车上做了很多好事.
- **Chatbot-Arena-style image arenas**其他https://imagearena.ai/其他.
  **Chatbot-Arena 风格的图像竞技场**其他:https://imagearena.ai/其他

失效模式:

> 失败模式:

- **Judge variance.**专家的偏好不同,使用两者.
  评判者差异:非专家和专家有不同的偏好.
- **Prompt distribution.**桃选的提示有利于一个家庭.
  快速分布:精心挑选的快速会偏向某一家.
- **LLM-judge reward hacking.**,但错误的输出会欺骗GPT-4法官.
  通过"好看但错"的输出欺骗.

## 组合使用

生产评估报告应包括:

> 一份生产级评估报告应包括:

1. 根据实质分布 (样品质) 的测试,对10-30k样品进行了FID.
   在10-30k样本上相对留出真实分布的FID(样本质量)
2. 同样样样本的CIP分数/CMMD与其提示 (附属性).
   相同样本相对各自提示的CIP Score/CMMD (CCIP Score/CMMD) 遵循度)
3. 失明场合的胜利率与前型号 (总体偏好).
   与前一个模型在盲评竞技场中的胜率 (整体偏好)
4. 失败模式分析:50个随机抽取的输出,标记为已知的问题 (手解剖学,文本染,一致的对象数量).
   失败模式分析:随机采样50个输出,标记已知问题

任何单一的指标都是谎言.

> 任何单一指标都是谎言.

## 建立它,实现它.
```figure
gx-fid-distributions
```

## 建立它

`code/main.py`通过 FID,Clip-score和 Elo 聚合,我们将合成的"特征向量" (我们使用4D向量作为Inception特征的替代品) 实现.

> `code/main.py`在合成"特征向量"上实现FID、类CLIP Score 和 Elo 聚合(我们用4维向量代替Inception特征) ――你会看到:

- 在一个小N和一个大N 的偏差上进行FID计算.
  小N 和大N 上的FID 计算偏差──
- 作为特征池之间的共数相似性.
  作为一个相似的特征.
- 根据合成偏好流的 Elo更新规则.
  根据""的新规则,

### 步骤1:四行FID

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> 四行FID:分别对真实和生成特征计算平均值与协方差,再计算平均值差平方加协方差迹.

### 步骤2:CLIP风格余弦相似度

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> 点积除以两个向量范数乘积,加上子 防止除零.

### 排列三:排列三:排列三:排列三

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> 更新:基于期望胜率和实际结果调整分数,K=32是国际象棋标准.

## 陷常见的陷

- **FID at N=1000.**报告低NFID的论文是游戏.
  报告低 N FID 的论文在刷分.
- **Comparing FID across resolutions.**开始的299×299尺寸改变了功能分布.
  跨分辨率比较FID:Inception的299×299 缩放会改变特征分布――只在匹配分辨率下比较――
- **Reporting one seed.**试试三种种子,报告.
  报告一个种子:至少跑3种子.
- **CLIP score inflation via negative prompts.**检查视觉度.
  通过负向快速 抬高 CLIP 评分:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**如果两个模型在训练中看到一个基准提示, Elo 无意义. 使用延迟提示设置.
  快重叠导致的Elo偏差:如果两个模型训练时见过基准提示,Elo 无意义――使用留出的提示集──
- **Human eval paid-crowd skew.**果的MTurk注释者偏向年轻人/技术友好.
  人工评估付费众包偏差:繁殖、M土克标注者偏年轻 / 偏技术友好──混合招募的艺术/设计专家──

## 用它实现框架

2026年生产评估协议:

> 2026年生产级评估协议:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

报告中的四个支柱都是一份要求,任何一个都是一份营销.

> 任何单独的只是销售.

## 运送它.

保存`outputs/skill-eval-report.md`技能采用了新的模型检查点+基线,并输出了完整的评估计划:样本大小,指标,故障模式探测器,签署标准.

> 保存为`outputs/skill-eval-report.md`△该技能收到一个新的模型检查点+基线,输出完整评估计划:样本数,标志,失败模式探针,签字标准.

## 练习题

1. **Easy.**跑步`code/main.py`根据同一个合成分布的N=100与N=1000的FID比较.
2. **Medium.**根据合成CLIP类型的功能实现CMMD (见Jayasumana et al., 2024).对质量差异的敏感性与FID进行比较.
3. **Hard.**复制HPSv2设置:从Pick-a-Pic的子集中取1000个图像即时对,根据偏好调整一个基于 CLIP 的小分分数,并测量其与持久的集合一致性.

## 关键词 快速查找表

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

## 产品笔记:评估也是推理工作负载

运行FID在10k样本上意味着生成10k图像.对于一个单个L4上50步 SDXL基础在10242上,这就是11小时的单次请求推断.评估预算是真实的,框架是完全离线推理情况 (最大化吞吐量,忽略TTFT):

- **Batch hard, forget latency.**离线 eval = 静态批量,最大的尺寸适合内存. `pipe(...).images`随着`num_images_per_prompt=8`在80GB的H100上,墙上的钟表比单次请求速度快4至6倍.
- **Cache the real features.**实际参考集中的Inception (FID) 或CLIP (CLIP-score,CMMD) 功能提取运行 *once*,存储为`.npz`没有重新计算每一个评估.

对于CI/回归门:每次 PR (~30分钟) 的500个样本子小组中运行FID + CLIP分数;每晚运行FID + HPSv2 + Elo的全部10k.

## 继续阅读 继续阅读

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) 联邦调查局的文件.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603)   
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)  
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341)   
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) 图像奖励
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) 活动提示
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675)失败模式调查.
