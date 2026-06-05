# Speaker Recognition & Verification | 说话人识别与验证

> ASR asks "what did they say?" Speaker recognition asks "who said it?" The math looks the same — embeddings plus cosine — but every production decision hinges on a single EER number.

> **【中文解读】** ASR 问"说了什么"，说话人识别问"谁说的"。数学看起来一样——嵌入向量+余弦相似度——但每个生产决策都取决于一个 EER（等错误率）数值。EER 越低，系统越可靠。

> **【拓展：声纹识别应用】** 声纹识别用于银行电话认证、智能音箱用户识别、安防监控。声纹（voiceprint）就像语音的指纹，是生物特征识别的重要分支。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

A user says a passphrase. You want to know: is this the person they claim to be (*verification*, 1:1), or is it the first person in your enrollment bank (*identification*, 1:N)? Or neither — is this an unknown speaker (*open-set*)?

> 用户说出一个口令。你想知道：这是他们声称的那个人吗（*验证*，1:1），还是你注册库中的第一个人（*识别*，1:N）？或者都不是——这是一个未知说话人（*开放集*）？

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Pre-2018: GMM-UBM + i-vectors. Reasonable EER but fragile to channel shift (phone vs laptop) and emotion. 2018–2022: x-vectors (TDNN backbone trained with angular margin). 2022+: ECAPA-TDNN and WavLM-large embeddings. By 2026 the field is dominated by three models and one metric.

> 2018 年前：GMM-UBM + i-vectors。EER 合理但对信道偏移（电话 vs 笔记本）和情绪敏感。2018-2022：x-vectors（用角度间隔训练的 TDNN 骨干）。2022+：ECAPA-TDNN 和 WavLM-large 嵌入。到 2026 年，该领域由三个模型和一个指标主导。

The metric is **EER** — Equal Error Rate. Set your decision threshold so False Accept Rate = False Reject Rate. The crossover is EER. Used in every paper, every leaderboard, every procurement call.

> 这个指标是 **EER**——等错误率。设置决策阈值使假接受率 = 假拒绝率。交叉点就是 EER。用于每篇论文、每个排行榜、每个采购评审。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.** Enrollment: record 5–30 seconds of the target speaker; compute a fixed-dimension embedding (192-d for ECAPA-TDNN, 256-d for WavLM-large). Verification: get the test utterance embedding; compute cosine similarity; compare to a threshold.

> **流水线。** 注册：录制目标说话人 5-30 秒语音；计算固定维度嵌入（ECAPA-TDNN 为 192 维，WavLM-large 为 256 维）。验证：获取测试语音嵌入；计算余弦相似度；与阈值比较。

**ECAPA-TDNN (2020, still dominant 2026).** Emphasized Channel Attention, Propagation and Aggregation - Time-Delay Neural Network. 1D conv blocks with squeeze-excitation, multi-head attention pooling, followed by a linear layer to 192-d. Trained on VoxCeleb 1+2 (2,700 speakers, 1.1M utterances) with Additive Angular Margin loss (AAM-softmax).

> **ECAPA-TDNN（2020，2026 年仍占主导）。** 强调通道注意力、传播和聚合的时延神经网络。1D 卷积块 + squeeze-excitation + 多头注意力池化，接线性层输出 192 维。在 VoxCeleb 1+2（2,700 说话人，110 万条语音）上用加性角度间隔损失（AAM-softmax）训练。

**WavLM-SV (2022+).** Fine-tune a pretrained WavLM-large SSL backbone with AAM loss. Higher quality but slower — 300+ MB vs 15 MB.

> **WavLM-SV（2022+）。** 用 AAM 损失微调预训练的 WavLM-large SSL 骨干。质量更高但更慢——300+ MB vs 15 MB。

**x-vector (baseline).** TDNN + statistics pooling. Classic; still useful on CPU / edge.

> **x-vector（基线）。** TDNN + 统计池化。经典方案；仍在 CPU/边缘设备上有用。

**AAM-softmax.** Standard softmax with added margin `m` in the angular space: `cos(θ + m)` for the correct class. Forces inter-class angular separation. Typical `m=0.2`, scale `s=30`.

> **AAM-softmax。** 在角度空间中添加间隔 `m` 的标准 softmax：正确类用 `cos(θ + m)`。强制类间角度分离。典型值 `m=0.2`，缩放 `s=30`。

### Scoring

> ### 评分

- **Cosine** between enrollment and test embeddings. Threshold-based decision.
  **余弦**相似度，在注册嵌入和测试嵌入之间计算。基于阈值的决策。
- **PLDA (Probabilistic LDA).** Project embeddings into a latent space where same-speaker vs different-speaker has a closed-form likelihood ratio. Added on top of cosine for +10–20% EER reduction. Standard pre-2020; now used only in closed-set setups.
  **PLDA（概率 LDA）。** 将嵌入投影到潜在空间，其中同说话人 vs 不同说话人有闭式似然比。在余弦基础上可降低 10-20% EER。2020 年前的标准；现在仅用于封闭集场景。
- **Score normalization.** `S-norm` or `AS-norm`: normalize each score against a cohort of imposter means and stds. Essential for cross-domain eval.
  **分数归一化。** `S-norm` 或 `AS-norm`：用冒充者群体的均值和标准差归一化每个分数。跨域评估必需。

### Numbers you should know (2026)

> 2026 年你应该知道的数字

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

### Diarization

> ### 说话人日志（谁在何时说话）

"Who spoke when" in a multi-speaker clip. Pipeline: VAD → segment → embed each segment → cluster (agglomerative or spectral) → smooth boundaries. Modern stack: `pyannote.audio` 3.1, which bundles speaker segmentation + embedding + clustering behind one call. 2026 SOTA DER on AMI is ~15% (down from 23% in 2022).

> 多说话人音频中"谁在何时说话"。流水线：VAD → 分段 → 对每段嵌入 → 聚类（层次聚类或谱聚类）→ 平滑边界。现代技术栈：`pyannote.audio` 3.1，将说话人分割 + 嵌入 + 聚类打包为一个调用。2026 年 AMI 上 SOTA DER 约 15%（从 2022 年的 23% 下降）。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: toy embedding from MFCC statistics

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

Not SOTA by a mile — for teaching only. `code/main.py` uses this as a proof-of-concept on synthetic speaker data.

> 离 SOTA 差得远——仅用于教学。`code/main.py` 将其作为合成说话人数据的概念验证。

### Step 2: cosine similarity + threshold

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Step 3: EER from similarity pairs

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

Returns (eer, threshold_at_eer). Report both.

> 返回 (eer, threshold_at_eer)。两者都要报告。

### Step 4: production with SpeechBrain

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Step 5: diarize with pyannote

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。





> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

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



## Pitfalls

> 常见陷阱

- **Channel mismatch.** Model trained on VoxCeleb (web video) ≠ phone-call audio. Always evaluate on target channel.
  **信道不匹配。** 在 VoxCeleb（网络视频）上训练的模型不等于电话音频。始终在目标信道上评估。
- **Short utterances.** EER degrades sharply below 3 seconds of test audio.
  **短语音。** 测试音频低于 3 秒时 EER 急剧恶化。
- **Enrollment with noise.** One noisy enrollment poisons the anchor. Use ≥3 clean samples and average.
  **带噪注册。** 一个嘈杂的注册样本会毒化锚点。使用至少 3 个干净样本并取平均。
- **Fixed threshold across conditions.** Always tune the threshold on a held-out dev set from the target domain.
  **跨条件固定阈值。** 始终在目标领域的留出开发集上调整阈值。
- **Cosine on non-normalized embeddings.** L2-normalize first; otherwise the magnitude dominates.
  **未归一化嵌入上的余弦。** 先做 L2 归一化；否则模值会占主导。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-speaker-verifier.md`. Pick model, enrollment protocol, threshold-tuning plan, and fraud safeguards.

> 保存为 `outputs/skill-speaker-verifier.md`。选择模型、注册协议、阈值调优计划和欺诈防护措施。

## Exercises | 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


1. **Easy.** Run `code/main.py`. Builds synthetic "speakers" (different tone profiles), enrolls, computes EER on a 100-pair trial list.
   **简单。** 运行 `code/main.py`。构建合成"说话人"（不同音调配置），注册，在 100 对试验列表上计算 EER。
2. **Medium.** Use SpeechBrain ECAPA on 30 VoxCeleb1 utterances (5 speakers × 6 each). Compute EER with cosine vs PLDA.
   **中等。** 在 30 条 VoxCeleb1 语音上使用 SpeechBrain ECAPA（5 个说话人 × 6 条）。用余弦和 PLDA 计算 EER。
3. **Hard.** Build the full enroll → diarize → verify pipeline with `pyannote.audio`. Evaluate DER on AMI dev set.
   **困难。** 用 `pyannote.audio` 构建完整的注册 → 日志 → 验证流水线。在 AMI 开发集上评估 DER。

## Key Terms | 术语速查表

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

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) — the classic deep-embedding paper.
  Snyder 等 (2018). X-Vectors：说话人识别的鲁棒 DNN 嵌入——经典的深度嵌入论文。
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) — dominant architecture 2020–2026.
  Desplanques 等 (2020). ECAPA-TDNN——2020-2026 年占主导的架构。
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) — SSL backbone for SV and diarization.
  Chen 等 (2022). WavLM：全栈语音处理的大规模自监督预训练——SV 和日志的 SSL 骨干。
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) — production diarization + embedding stack.
  Bredin 等 (2023). pyannote.audio 3.1——生产级日志 + 嵌入技术栈。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) — current EER standings across models.
  VoxCeleb 排行榜（2026 年更新）——各模型当前 EER 排名。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

