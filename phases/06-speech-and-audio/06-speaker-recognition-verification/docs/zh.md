# 说话人识别与验证

> ASR 问"说了什么"，说话人识别问"谁说的"。数学看起来一样——嵌入向量 + 余弦相似度——但每个生产决策都取决于一个 EER（Equal Error Rate，等错误率）数值。EER 越低，系统越可靠。

> **【中文解读】** ASR 问"说了什么"，说话人识别问"谁说的"。数学看起来一样——嵌入向量+余弦相似度——但每个生产决策都取决于一个 EER（等错误率）数值。EER 越低，系统越可靠。

> **【拓展：声纹识别应用】** 声纹识别用于银行电话认证、智能音箱用户识别、安防监控。声纹（voiceprint）就像语音的指纹，是生物特征识别的重要分支。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**时长：** 约 45 分钟

## 问题引入

用户说出一个口令。你想知道：这是他们声称的那个人吗（*验证*，1:1），还是你注册库中的第一个人（*识别*，1:N）？或者都不是——这是一个未知说话人（*开放集*）？

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

2018 年前：GMM-UBM + i-vector。合理的 EER 但对信道偏移（电话 vs 笔记本）和情绪脆弱。2018-2022：x-vector（带角度裕度的 TDNN 骨干训练）。2022+：ECAPA-TDNN 和 WavLM-large 嵌入。到 2026 年，该领域由三个模型和一个指标主导。

该指标是 **EER**——等错误率。将决策阈值设置为使错误接受率等于错误拒绝率。交叉点就是 EER。用于每篇论文、每个排行榜、每个采购电话。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![注册 + 验证流水线，使用嵌入 + 余弦 + EER](../assets/speaker-verification.svg)

**流水线。** 注册：录制目标说话人 5-30 秒；计算固定维度嵌入（ECAPA-TDNN 为 192 维，WavLM-large 为 256 维）。验证：获取测试话语的嵌入；计算余弦相似度；与阈值比较。

**ECAPA-TDNN（2020，2026 年仍占主导）。** 强调通道注意力、传播和聚合 - 时延神经网络（Emphasized Channel Attention, Propagation and Aggregation - Time-Delay Neural Network）。带 squeeze-excitation 的 1D 卷积块，多头注意力池化，接线性层到 192 维。在 VoxCeleb 1+2（2,700 个说话人，110 万条话语）上用加性角度裕度损失（AAM-softmax）训练。

**WavLM-SV（2022+）。** 用 AAM 损失微调预训练的 WavLM-large SSL 骨干。质量更高但更慢——300+ MB vs 15 MB。

**x-vector（基线）。** TDNN + 统计池化。经典；在 CPU / 边缘设备上仍有用。

**AAM-softmax。** 带裕度 `m` 的标准 softmax，加在角度空间：正确类别用 `cos(theta + m)`。强制类间角度分离。典型值 `m=0.2`，缩放 `s=30`。

### 评分

- **余弦相似度。** 注册和测试嵌入之间的余弦。基于阈值的决策。
- **PLDA（概率 LDA）。** 将嵌入投影到潜在空间，其中同说话人 vs 不同说话人有闭式似然比。在余弦之上增加 10-20% EER 降低。2020 年前的标准；现在只在封闭集设置中使用。
- **分数归一化。** `S-norm` 或 `AS-norm`：对冒充者均值和标准差的队列归一化每个分数。跨域评估必需。

### 你应该知道的数字（2026）

| 模型 | VoxCeleb1-O EER | 参数 | 吞吐量（A100） |
|------|-----------------|------|----------------|
| x-vector（经典） | 3.10% | 5M | 400x 实时 |
| ECAPA-TDNN | 0.87% | 15M | 200x 实时 |
| WavLM-SV large | 0.42% | 316M | 20x 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 6M | 100x 实时 |
| ReDimNet（2024） | 0.39% | 24M | 100x 实时 |

### 说话人日志（Diarization）

"谁在什么时候说话"用于多人片段。流水线：VAD -> 分段 -> 对每段嵌入 -> 聚类（层次聚类或谱聚类）-> 平滑边界。现代栈：`pyannote.audio` 3.1，将说话人分割 + 嵌入 + 聚类打包在一个调用中。2026 年 AMI 上的 SOTA DER 约 15%（从 2022 年的 23% 下降）。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：从 MFCC 统计量构造玩具嵌入

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26 维
```

离 SOTA 差得远——仅用于教学。`code/main.py` 在合成说话人数据上用它做概念验证。

### 步骤 2：余弦相似度 + 阈值

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### 步骤 3：从相似度对计算 EER

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

返回 (eer, eer 处的阈值)。两个值都要报告。

### 步骤 4：用 SpeechBrain 做生产级验证

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# 注册：平均 3-5 个干净样本的嵌入
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# 验证
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA 典型阈值；在你的数据上调优
```

### 步骤 5：用 pyannote 做说话人日志

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 防伪（重放 / 深度伪造检测） | AASIST 或 RawNet2 |
| 微型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |

## 陷阱

- **信道不匹配。** 在 VoxCeleb（网络视频）上训练的模型 != 电话音频。始终在目标信道上评估。
- **短话语。** 测试音频低于 3 秒时 EER 急剧下降。
- **有噪声的注册。** 一个有噪声的注册会毒化锚点。使用 3 个以上干净样本并取平均。
- **跨条件固定阈值。** 始终在目标领域的留出开发集上调优阈值。
- **未归一化的嵌入上的余弦。** 先做 L2 归一化；否则幅度会占主导。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-speaker-verifier.md`。选择模型、注册协议、阈值调优计划和欺诈防护措施。

## 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

1. **简单。** 运行 `code/main.py`。构建合成"说话人"（不同音调轮廓），注册，在 100 对试验列表上计算 EER。
2. **中等。** 在 30 条 VoxCeleb1 话语（5 个说话人 × 每人 6 条）上使用 SpeechBrain ECAPA。比较余弦 vs PLDA 的 EER。
3. **困难。** 用 `pyannote.audio` 构建完整的注册 -> 日志 -> 验证流水线。在 AMI 开发集上评估 DER。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| EER | 头条指标 | 错误接受 = 错误拒绝时的阈值。 |
| 验证（Verification） | 1:1 | "这是 Alice 吗？" |
| 识别（Identification） | 1:N | "谁在说话？" |
| 开放集（Open-set） | 可能未知 | 测试集可包含未注册的说话人。 |
| 注册（Enrollment） | 注册登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度裕度的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 日志错误率——漏检 + 误报 + 混淆。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) —— 经典的深度嵌入论文。
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) —— 2020-2026 年的主导架构。
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) —— 用于说话人验证和日志的 SSL 骨干。
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) —— 生产级日志 + 嵌入栈。
- [VoxCeleb 排行榜（2026 年更新）](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) —— 各模型当前 EER 排名。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
