# 发言人识别和验证

>  ASR问"他们说什么?"扬声器识别问"谁说?"数学看起来是相同的嵌体加上,但每个生产决定都依赖于一个EER号码.

> **【中文解读】** ASR 问"说了什么",说话人识别问"谁说的"――数学看起来像嵌向量+余弦相似度,但每个生产决策都取决于一个EER(等错误率) 数值.EER 越低,系统越可靠.

> **【拓展：声纹识别应用】**声纹识别用于银行电话认证、智能音箱用户识别、安全监控──声纹(声纹) 就像语音的指纹,是生物特征识别的重要分支──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

您想知道:这是他们声称自己 (*验证*, 1:1),还是您的注册银行 (*识别*, 1:N) 的第一个人?

> 用户发言令――你想知道:这是他们声称的那个人吗?

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

2018年前:GMM-UBM+i-向量.合理的EER但对道转移 (电话与笔记本电脑) 和情感很脆弱. 20182022:x向量 (TDNN脊柱训练有素的角差距). 2022+:ECAPA-TDNN和WavLM-大嵌入式.到2026年,该领域由三种模型和一个指标主导.

> 2018年前:GMM-UBM + i-矢量──EER 合理但对信仰偏移──电话 vs笔记本) 和情绪敏感──2018-2022:x-矢量──用角度间隔训练的TDNN骨干)──2022+:ECAPA-TDNN 和波浪-大 嵌入──到2026年,该领域由三个模型和一个指标主导────

测量量是**EER**  错误率. 设定你的决定门,所以错误接受率 =错误拒绝率. 交叉是EER. 在每篇论文,每篇排名表,每次采购调用中都使用.

> 这个标志是**EER**等误差率──设置决策值使假接受率 =假拒绝率──交叉点就是EER──用于每篇论文,每排行榜,每采购评审──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**录制:记录目标扬声器的530秒;计算固定维度嵌入 (192-d ECAPA-TDNN,256-d WavLM-大).验证:获取测试语音嵌入;计算共音相似性;与门进行比较.

> **流水线。**注册:录制目标说话人 5-30秒语音;计算固定维度嵌入(ECAPA-TDNN 为 192 维,WavLM-大为 256 维) △验证:获取测试语音嵌入;计算余弦相似度;与值比较──

**ECAPA-TDNN (2020, still dominant 2026).**强调频道关注,传播和聚合 - 时间延迟神经网络. 1D conv 块具有挤压激动,多头关注聚合,随后有一个直线层到192d.训练于 VoxCeleb 1+2 (2700扬声器,1.1M发言) 具有增量角利率损失 (AAM-软max).

> **ECAPA-TDNN（2020，2026 年仍占主导）。**强调通道注意力、传播和聚合的时延神经网络──1D卷积块+挤压刺激+多头注意力池化,接线性层输出192维──在VoxCeleb1+2(2,700 说话人,110万条语音) 上加性角度间隔损失(AAM-软max) 训练──

**WavLM-SV (2022+).**精细调节预训练的WavLM大SSL背骨,AAM损失.更高质量,但更慢的300+MBvs15MB.

> **WavLM-SV（2022+）。**用AAM 损失微调预训练的波浪LM-大SSL骨干――质量更高但更慢300+MBvs15MB――

**x-vector (baseline).**传统;仍然在CPU/边缘上有用.

> **x-vector（基线）。**传统方案;仍在CPU/边缘设备上有用.

**AAM-softmax.**标准软max 附加边缘`m`在角空间中: `cos(θ + m)`对于正确的类别. 类别间的角分离. 典型`m=0.2`规模`s=30`现在,我们要去.

> **AAM-softmax。**在空间中添加间隔`m`的标准软度:正确类用 `cos(θ + m)`△强制类间角分离――典型值`m=0.2`缩放`s=30`,我知道.

### 评分

> ### 评分

- **Cosine**根据值决定.
  **余弦**类似性,在注册嵌入和测试嵌入之间计算.
- **PLDA (Probabilistic LDA).**项目嵌入在一个隐藏空间中,相同扬声器与不同扬声器具有闭式形式概率比.增加在可西因上以减少+1020%的EER.标准前-2020;现在仅用于闭式设置.
  **PLDA（概率 LDA）。**投影将嵌入潜在空间,其中同话人与不同话人有闭式似然比比. 在余弦基础上可降低 10-20%的EER.
- **Score normalization.** `S-norm`或`AS-norm`对于跨领域评价来说,这是必不可少的.
  **分数归一化。** `S-norm`或`AS-norm`对于每分数的使用者群体的平均值和标准差异.

### 你应该知道的数字 (2026)

> 2026年你应该知道的数字

| Model | VoxCeleb1-O EER | Params | Throughput (A100) |
|-------|-----------------|--------|-------------------|
| x-vector (classic) | 3.10% | 5 M | 400× RT |
| ECAPA-TDNN | 0.87% | 15 M | 200× RT |
| WavLM-SV large | 0.42% | 316 M | 20× RT |
| Pyannote 3.1 segmentation + embedding | 0.65% | 6 M | 100× RT |
| ReDimNet (2024) | 0.39% | 24 M | 100× RT |

| 模型 | VoxCeleb1-O EER | 参数量 | 吞吐量（A100） |
|------|-----------------|--------|----------------|
| x-vector（经典） | 3.10% | 500 万 | 400× 实时 |
| ECAPA-TDNN | 0.87% | 1500 万 | 200× 实时 |
| WavLM-SV large | 0.42% | 3.16 亿 | 20× 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 600 万 | 100× 实时 |
| ReDimNet（2024） | 0.39% | 2400 万 | 100× 实时 |

### 腹化

> ### 说话人日志 ((谁在何时说话)

管道:VAD → 段 → 嵌入每个段 → 集群 (聚合或光谱) → 滑的边界. 现代堆: `pyannote.audio`总体而言,在2026年,AMI的SOTA DER率为15% (从2022年的23%下降).

> 多说话人音频中"谁在何时说话"――流水线:VAD → 分段 → 对每段嵌入 →聚类`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为调用――2026年 AMI 上 SOTA DER 约15%(从2022年下降23%)

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
sp-eer-crossover
```

## 建立它

### 步骤1:从MFCC统计数据中嵌入玩具

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26-d
```

只有教学.`code/main.py`使用这种方法作为合成扬声器数据的概念证明.

> 离 SOTA 差得远仅用于教学.`code/main.py`作为合成语文人数据的概念验证.

### 步骤2: 数相似性+门

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### 步骤3:从相似性对的EER

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 1.0, 0.0)  # (fa, fr, threshold)
    for t in thresholds:
        fr = sum(1 for s in same_scores if s < t) / len(same_scores)
        fa = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        if abs(fa - fr) < abs(best[0] - best[1]):
            best = (fa, fr, t)
    return (best[0] + best[1]) / 2, best[2]
```

报表两者.

> 返回 (eer,门_at_eer) ──两者都要报告──

### 步骤4:使用SpeechBrain制作

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### 步骤5:用笔记记记本日记

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Situation | Pick |
|-----------|------|
| Closed-set 1:1 verification, edge | ECAPA-TDNN + cosine threshold |
| Open-set verification, cloud | WavLM-SV + AS-norm |
| Diarization (meetings, podcasts) | `pyannote/speaker-diarization-3.1` |
| Anti-spoofing (replay / deepfake detection) | AASIST or RawNet2 |
| Tiny embedded (KWS + enrollment) | Titanet-Small (NeMo) |

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘设备 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 反欺诈（回放/深度伪造检测） | AASIST 或 RawNet2 |
| 小型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |



## 陷

> 常见陷

- **Channel mismatch.**通过VoxCeleb (网络视频) 训练的模型 ≠电话呼叫音频.
  **信道不匹配。**在 VoxCeleb (网络视频) 上训练的模型不等于电话音频――总是在目标观念上评估――
- **Short utterances.**测试音频的EER明显降低到测试音频的3秒以下.
  **短语音。**测试音频低于3秒时EER急剧恶化.
- **Enrollment with noise.**声的接毒了.使用 ≥3 清洁样本和平均.
  **带噪注册。**一个杂的注册样本会毒化点.
- **Fixed threshold across conditions.**总是调整目标域的开发设置.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调整值.
- **Cosine on non-normalized embeddings.**首先将L2正常化;否则大小占主导地位.
  **未归一化嵌入上的余弦。**首先做L2归结;否则模值会占主导地位.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-speaker-verifier.md`选择模式,注册协议,值调整计划,以及欺诈保障措施.

> 保存为`outputs/skill-speaker-verifier.md`选择模型"",注册协议"",优化计划和欺诈防护措施"",

## 练习题

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


1. **Easy.**跑步`code/main.py`构建合成"扬声器" (不同音调配置),在100对试验列表中注册,计算EER.
   **简单。**运行`code/main.py`构建合成"说话人" (不同音调配置),注册,在100对试验列表上计算EER
2. **Medium.**使用SpeechBrain ECAPA在30个 VoxCeleb1语音中 (每个5个扬声器 × 6个).使用Cosine vs PLDA计算EER.
   **中等。**在 30 条 VoxCeleb1 语音上使用SpeechBrain ECAPA(5 个说话人 × 6 条) ――用余弦和 PLDA 计算 EER。
3. **Hard.**建立全报 →日记 → 验证管道`pyannote.audio`在 AMI 开发装置上评估DER.
   **困难。**用`pyannote.audio`构建完整的注册 → 日志 → 验证流水线――在 AMI 开发集上评估 DER――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| EER | The headline metric | Threshold where False Accept = False Reject. |
| Verification | 1:1 | "Is this Alice?" |
| Identification | 1:N | "Who is speaking?" |
| Open-set | Unknown possible | Test set can contain unenrolled speakers. |
| Enrollment | Registering | Computing a speaker's reference embedding. |
| AAM-softmax | The loss | Softmax with additive angular margin; forces cluster separation. |
| PLDA | Classic scoring | Probabilistic LDA; likelihood-ratio scoring on top of embeddings. |
| DER | Diarization metric | Diarization Error Rate — miss + false alarm + confusion. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| EER | 头条指标 | 假接受率 = 假拒绝率时的阈值。 |
| 验证 | 1:1 | "这是 Alice 吗？" |
| 识别 | 1:N | "谁在说话？" |
| 开放集 | 可能有未知者 | 测试集可包含未注册的说话人。 |
| 注册 | 登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度间隔的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 说话人日志错误率——漏检 + 误检 + 混淆。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf)经典的深入嵌入式纸.
  斯奈德等 (2018).X-矢量:说话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143)主导建筑 20202026
  欧洲经济联盟 (ECAPA-TDNN) 2020-2026年占主导的架构
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900)SV和日记化的SSL脊柱.
  陈等 (2022). 波L:全语音处理大规模自监督预训练SV 和日志的SSL骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio)生产日记化+嵌入堆.
                                                                                                                                                                                                                                                                
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/)各车型的EER现行排名.
  排行榜 (排行榜) 各模型当前 EER 排名──

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

