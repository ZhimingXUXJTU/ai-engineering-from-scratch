# 音频评估指标 — WER、MOS、UTMOS、MMAU、FAD 与开放排行榜

> 无法度量就无法交付。本课列出 2026 年所有音频任务的评估指标：ASR 用 WER（词错率）、TTS 用 MOS（平均意见分）、音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER。还有对比排行榜。

> **【中文解读】** 无法度量就无法交付。本课列出 2026 年所有音频任务的评估指标：ASR 用 WER（词错率）、TTS 用 MOS（平均意见分）、音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER。还有对比排行榜。

> **【拓展：WER 是语音识别的黄金指标】** WER（Word Error Rate，词错率）= (替换+删除+插入) / 总词数。Whisper Large v3 在英文上达到 ~5% WER，接近人类水平。中文用 CER（字错率）。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**时长：** 约 60 分钟

## 问题引入

每个音频任务有多个指标，每个衡量不同维度。使用错误的指标就是你发布一个在仪表盘上看起来很好但在生产中很糟糕的模型的方式。2026 年的标准列表：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

| 任务 | 主要指标 | 次要指标 |
|------|----------|----------|
| ASR | WER | CER · RTFx · 首 token 延迟 |
| TTS | MOS / UTMOS | SECS · ASR 往返 WER · CER · TTFA |
| 语音克隆 | SECS（ECAPA 余弦） | MOS · CER |
| 说话人验证 | EER | minDCF · 工作点 FAR / FRR |
| 说话人日志 | DER | JER · 说话人混淆 |
| 音频分类 | top-1 · mAP | 宏观 F1 · 每类召回率 |
| 音乐生成 | FAD | CLAP · 听力面板 MOS |
| 音频语言模型 | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| 流式 S2S | 延迟 P50/P95 | WER · MOS |

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

## 核心概念

![音频评估矩阵 — 指标 vs 任务 vs 2026 排行榜](../assets/eval-landscape.svg)

### ASR 指标

**WER（词错率，Word Error Rate）。** `(S + D + I) / N`。评分前小写、去标点、数字归一化。使用 `jiwer` 或 OpenAI 的 `whisper_normalizer`。< 5% = 朗读语音的人类水平。

**CER（字符错误率，Character Error Rate）。** 相同公式，字符级。用于声调语言（普通话、粤语），因为词分割有歧义。

**RTFx（逆实时因子）。** 每墙钟秒处理的音频秒数。越高越好。Parakeet-TDT 达到 3380x。Whisper-large-v3 约 30x。

**首 token 延迟。** 从音频输入到首个转录 token 的墙钟时间。对流式关键。Deepgram Nova-3：约 150 ms。

### TTS 指标

**MOS（平均意见分，Mean Opinion Score）。** 1-5 人类评分。黄金标准但慢。每样本 20+ 听众，每模型 100+ 样本。

**UTMOS（2022-2026）。** 学习的 MOS 预测器。在标准基准上与人类 MOS 相关约 0.9。F5-TTS：UTMOS 3.95；真实语音：4.08。

**SECS（说话人编码器余弦相似度）。** 用于语音克隆。参考和克隆输出之间的 ECAPA 嵌入余弦。> 0.75 = 可识别的克隆。

**ASR 往返 WER。** 将 Whisper 运行在 TTS 输出上，计算与输入文本的 WER。捕获可懂度退化。2026 SOTA：< 2% CER。

**TTFA（首个音频时间）。** 墙钟延迟。Kokoro-82M：约 100 ms；F5-TTS：约 1 秒。

### 语音克隆专用

**SECS + MOS + CER** 作为三元组。高 SECS 但低 MOS 意味着音色正确但不自然；反过来意味着自然声音但说话人不对。

### 说话人验证

**EER（等错误率）。** 错误接受率等于错误拒绝率时的阈值。VoxCeleb1-O 上的 ECAPA：0.87%。

**minDCF（最小检测代价）。** 在选定工作点（通常 FAR=0.01）的加权代价。比 EER 更贴近生产。

### 说话人日志

**DER（日志错误率）。** `(FA + Miss + Confusion) / total_speaker_time`。漏检语音 + 误报语音 + 说话人混淆，各占比例。AMI 会议：DER 约 10-20% 是现实的。pyannote 3.1 + Precision-2 商业：在录制良好的音频上 < 10% DER。

**JER（Jaccard 错误率）。** DER 的替代，对短段偏差更鲁棒。

### 音频分类

多标签：**mAP（平均精度均值）** 跨所有类别。AudioSet：BEATs-iter3 为 0.548 mAP。

多类别互斥：**top-1、top-5 准确率**。Speech Commands v2：99.0% top-1（Audio-MAE）。

不平衡：**宏观 F1** + **每类召回率**。按类报告——汇总准确率隐藏了哪些类别失败。

### 音乐生成

**FAD（Frechet 音频距离）。** 使用 VGGish 嵌入的真实 vs 生成音频分布之间的距离。MusicCaps 上 MusicGen-small：4.5。MusicLM：4.0。越低越好。

**CLAP 分数。** 使用 CLAP 嵌入的文本-音频对齐分数。> 0.3 = 合理对齐。

**听力面板 MOS。** 仍是消费级音乐的最终裁判。TTS Arena 上 Suno v5 ELO 1293（来自配对人类偏好）。

### 音频语言基准

**MMAU（大规模多音频理解）。** 10k 音频-QA 对。

**MMAU-Pro。** 1800 个难题，四个类别：语音 / 声音 / 音乐 / 多音频。4 选项随机概率 25%。Gemini 2.5 Pro 总体约 60%；多音频所有模型约 22%。

**LongAudioBench。** 多分钟片段配语义查询。Audio Flamingo Next 超过 Gemini 2.5 Pro。

**AudioCaps / Clotho。** 标注基准。SPICE、CIDEr、FENSE 指标。

### 流式语音到语音

**延迟 P50 / P95 / P99。** 从用户语音结束到首个可听回复的墙钟时间。Moshi：200 ms；GPT-4o Realtime：300 ms。

输出上的 **WER / MOS**。

**打断响应性。** 从用户打断到助手静音的时间。目标 < 150 ms。

### 2026 排行榜

| 排行榜 | 赛道 | URL |
|--------|------|-----|
| 开放 ASR 排行榜（HF） | 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena（HF） | 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech | TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro | LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC | 说话人识别 | `voxsrc.github.io` |
| MMAU 音乐子集 | 音乐 LALM | （MMAU 内） |
| HEAR 基准 | 自监督音频 | `hearbenchmark.com` |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：带归一化的 WER

```python
from jiwer import wer, Compose, ToLowerCase, RemovePunctuation, Strip

transform = Compose([ToLowerCase(), RemovePunctuation(), Strip()])
score = wer(
    truth="Please turn on the lights.",
    hypothesis="please turn on the light",
    truth_transform=transform,
    hypothesis_transform=transform,
)
# ~0.17
```

### 步骤 2：TTS 往返 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### 步骤 3：语音克隆的 SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### 步骤 4：音乐生成的 FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### 步骤 5：说话人验证的 EER（与第 6 课相同代码）

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        frr = sum(1 for s in same_scores if s < t) / len(same_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

每次部署配一个固定的评估套件，在每个模型更新时运行。三条基本规则：

1. **评分前归一化。** 小写、去标点、数字展开。报告归一化规则。
2. **报告分布，不报告均值。** 延迟用 P50/P95/P99。分类用每类召回率。MMAU 用每类别。
3. **运行一个标准公开基准。** 即使你的生产数据不同，在开放 ASR / TTS Arena / MMAU 上报告让审阅者可以苹果比苹果。

## 陷阱

- **UTMOS 外推。** 在 VCTK 风格干净语音上训练；对嘈杂/克隆/情感音频评分差。
- **MOS 面板偏差。** 20 个 Amazon Mechanical Turbock 工作者 != 20 个目标用户。如果利害攸关，花钱请领域面板。
- **FAD 依赖参考集。** 跨模型使用相同参考分布比较。
- **汇总 WER。** 总体 5% WER 可能隐藏带口音语音上 30% 的 WER。按人口统计分片报告。
- **公开基准饱和。** 大多数前沿模型在标准基准上接近天花板。构建反映你流量的内部留出集。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-audio-evaluator.md`。为任何音频模型发布选择指标、基准和报告格式。

## 练习题

1. **简单。** 运行 `code/main.py`。在玩具输入上计算 WER / CER / EER / SECS / 类 FAD / 类 MMAU。
2. **中等。** 构建 TTS 往返 WER 套件。将你的 Kokoro 或 F5-TTS 输出通过 Whisper 运行。在 50 个提示上计算 WER。标记 WER > 10% 的提示。
3. **困难。** 在 MMAU-Pro 语音 + 多音频子集（各 50 项）上评测你的第 10 课 LALM 选择。报告每类别准确率并与公布数字比较。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| WER | ASR 分数 | 归一化后词级别的 `(S+D+I)/N`。 |
| CER | 字符 WER | 用于声调语言或字符级系统。 |
| MOS | 人类意见 | 1-5 评分；20+ 听众 × 100 样本。 |
| UTMOS | ML MOS 预测器 | 学习的模型；与人类 MOS 相关约 0.9。 |
| SECS | 语音克隆相似度 | 参考和克隆之间的 ECAPA 余弦。 |
| EER | 说话人验证分数 | FAR = FRR 时的阈值。 |
| DER | 日志分数 | (FA + Miss + Confusion) / total。 |
| FAD | 音乐生成质量 | VGGish 嵌入上的 Frechet 距离。 |
| RTFx | 吞吐量 | 每墙钟秒的音频秒数。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [jiwer](https://github.com/jitsi/jiwer) —— 带归一化工具的 WER/CER 库。
- [UTMOS（Saeki et al. 2022）](https://arxiv.org/abs/2204.02152) —— 学习的 MOS 预测器。
- [Frechet Audio Distance（Kilgour et al. 2019）](https://arxiv.org/abs/1812.08466) —— 音乐生成标准。
- [开放 ASR 排行榜](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) —— 2026 实时排名。
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) —— 人类投票 TTS 排行榜。
- [MMAU-Pro 基准](https://mmaubenchmark.github.io/) —— LALM 推理排行榜。
- [HEAR 基准](https://hearbenchmark.com/) —— 音频 SSL 基准。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
