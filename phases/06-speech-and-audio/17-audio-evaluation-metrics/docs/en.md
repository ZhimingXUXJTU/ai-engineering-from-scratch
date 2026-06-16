# Audio Evaluation — WER, MOS, UTMOS, MMAU, FAD, and the Open Leaderboards | 音频评估指标

> You cannot ship what you cannot measure. This lesson names the 2026 metrics for every audio task: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), audio-language (MMAU, LongAudioBench), music (FAD, CLAP), and speaker (EER). Plus the leaderboards where you compare.

> **【中文解读】** 无法度量就无法交付。本课列出 2026 年所有音频任务的评估指标：ASR 用 WER（词错率）、TTS 用 MOS（平均意见分）、音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER。还有对比排行榜。

> **【拓展：WER 是语音识别的黄金指标】** WER（Word Error Rate，词错率）= (替换+删除+插入) / 总词数。Whisper Large v3 在英文上达到 ~5% WER，接近人类水平。中文用 CER（字错率）。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## The Problem | 问题引入

Every audio task has multiple metrics, each measuring a different axis. Using the wrong metric is how you ship a model that looks great on your dashboard and terribly in production. The 2026 canonical list:

> 每个音频任务都有多种指标，每种指标衡量不同的维度。使用错误的指标就是如何上线一个在仪表盘上看起来很棒但在生产中表现糟糕的模型。2026 年的标准列表：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


| Task | Primary | Secondary |
|------|---------|-----------|
| ASR | WER | CER · RTFx · first-token latency |
| TTS | MOS / UTMOS | SECS · WER-on-ASR-round-trip · CER · TTFA |
| Voice cloning | SECS (ECAPA cosine) | MOS · CER |
| Speaker verification | EER | minDCF · FAR / FRR at operating point |
| Diarization | DER | JER · speaker confusion |
| Audio classification | top-1 · mAP | macro F1 · per-class recall |
| Music generation | FAD | CLAP · listening panel MOS |
| Audio language model | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| Streaming S2S | latency P50/P95 | WER · MOS |

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## The Concept | 核心概念

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### ASR metrics

> ASR 评估指标

**WER (Word Error Rate).** `(S + D + I) / N`. Lowercase, strip punctuation, normalize numbers before scoring. Use `jiwer` or OpenAI's `whisper_normalizer`. &lt; 5% = human-parity read speech.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`。评分前需转小写、去除标点、标准化数字。使用 `jiwer` 或 OpenAI 的 `whisper_normalizer`。低于 5% = 朗读语音的人类水平。

**CER (Character Error Rate).** Same formula, character-level. Used for tone languages (Mandarin, Cantonese) where word segmentation is ambiguous.

> **CER（字错率）。** 相同公式，字符级别。用于声调语言（普通话、粤语），因为词 segmentation 不明确。

**RTFx (inverse real-time factor).** Audio seconds processed per wall-clock second. Higher is better. Parakeet-TDT hits 3380×. Whisper-large-v3 is ~30×.

> **RTFx（逆实时因子）。** 每实际秒处理的音频秒数。越高越好。Parakeet-TDT 达到 3380×。Whisper-large-v3 约 30×。

**First-token latency.** Wall-clock from audio input to first transcript token. Critical for streaming. Deepgram Nova-3: ~150 ms.

> **首 token 延迟。** 从音频输入到第一个转录 token 的实际时间。对流式处理至关重要。Deepgram Nova-3：约 150 ms。

### TTS metrics

> TTS 评估指标

**MOS (Mean Opinion Score).** 1-5 human rating. Gold standard but slow. Collect 20+ listeners per sample, 100+ samples per model.

> **MOS（平均意见分）。** 1-5 分人工评分。黄金标准但速度慢。每个样本收集 20+ 听者，每个模型 100+ 样本。

**UTMOS (2022-2026).** Learned MOS predictor. Correlates ~0.9 with human MOS on standard benchmarks. F5-TTS: UTMOS 3.95; ground truth: 4.08.

> **UTMOS（2022-2026）。** 学习型 MOS 预测器。在标准基准上与人类 MOS 相关性约 0.9。F5-TTS：UTMOS 3.95；真实值：4.08。

**SECS (Speaker Encoder Cosine Similarity).** For voice cloning. ECAPA embedding cosine between reference and cloned output. &gt; 0.75 = recognizable clone.

> **SECS（说话人编码器余弦相似度）。** 用于语音克隆。参考音频和克隆输出之间的 ECAPA 嵌入余弦相似度。大于 0.75 = 可识别的克隆。

**WER-on-ASR-round-trip.** Run Whisper over TTS output, compute WER against the input text. Catches intelligibility regressions. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。** 对 TTS 输出运行 Whisper，计算相对输入文本的 WER。捕获可懂度退化。2026 SOTA：CER 低于 2%。

**TTFA (time-to-first-audio).** Wall-clock latency. Kokoro-82M: ~100 ms; F5-TTS: ~1 s.

> **TTFA（首个音频时间）。** 实际延迟。Kokoro-82M：约 100 ms；F5-TTS：约 1 s。

### Voice-cloning-specific

> 语音克隆专用指标

**SECS + MOS + CER** as a triple. Cloning that scores high SECS but low MOS means timbre-right-but-unnatural; the opposite means natural voice but wrong speaker.

> **SECS + MOS + CER** 作为三重指标。克隆得分高 SECS 但低 MOS 意味着音色正确但不自然；反之则意味着声音自然但说话人不对。

### Speaker verification

> 说话人验证指标

**EER (Equal Error Rate).** The threshold where False Accept Rate equals False Reject Rate. ECAPA on VoxCeleb1-O: 0.87%.

> **EER（等错误率）。** 错误接受率等于错误拒绝率的阈值。ECAPA 在 VoxCeleb1-O 上：0.87%。

**minDCF (min Detection Cost).** Weighted cost at a chosen operating point (often FAR=0.01). More production-relevant than EER.

> **minDCF（最小检测代价）。** 在选定工作点（通常 FAR=0.01）的加权代价。比 EER 更贴近生产需求。

### Diarization

> 说话人日志指标

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Missed speech + false-alarm speech + speaker-confusion, each as a fraction. AMI meetings: DER ~10-20% is realistic. pyannote 3.1 + Precision-2 commercial: &lt;10% DER on well-recorded audio.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`。漏检语音 + 虚警语音 + 说话人混淆，各占比例。AMI 会议：DER 约 10-20% 是现实水平。pyannote 3.1 + Precision-2 商业版：在良好录音上 DER 低于 10%。

**JER (Jaccard Error Rate).** Alternative to DER, robust to short-segment bias.

> **JER（Jaccard 错误率）。** DER 的替代方案，对短段偏差更鲁棒。

### Audio classification

> 音频分类指标

Multi-label: **mAP (mean Average Precision)** over all classes. AudioSet: 0.548 mAP for BEATs-iter3.

> 多标签：**mAP（平均精度均值）**，覆盖所有类别。AudioSet：BEATs-iter3 为 0.548 mAP。

Multi-class exclusive: **top-1, top-5 accuracy**. Speech Commands v2: 99.0% top-1 (Audio-MAE).

> 多类互斥：**top-1、top-5 准确率**。Speech Commands v2：99.0% top-1（Audio-MAE）。

Imbalanced: **macro F1** + **per-class recall**. Report per-class — aggregate accuracy hides which classes fail.

> 不平衡数据：**macro F1** + **每类召回率**。按类别报告——汇总准确率会掩盖哪些类别失败。

### Music generation

> 音乐生成指标

**FAD (Fréchet Audio Distance).** Distance between VGGish-embedding distributions of real vs generated audio. MusicGen-small on MusicCaps: 4.5. MusicLM: 4.0. Lower better.

> **FAD（Fréchet 音频距离）。** 真实与生成音频的 VGGish 嵌入分布之间的距离。MusicGen-small 在 MusicCaps 上：4.5。MusicLM：4.0。越低越好。

**CLAP Score.** Text-audio alignment score using CLAP embeddings. &gt; 0.3 = reasonable alignment.

> **CLAP 分数。** 使用 CLAP 嵌入的文本-音频对齐分数。大于 0.3 = 合理的对齐。

**Listening panel MOS.** Still the final word for consumer-grade music. Suno v5 ELO 1293 on TTS Arena (from paired human preferences).

> **听音评审团 MOS。** 仍然是消费级音乐的最终评判标准。Suno v5 在 TTS Arena 上的 ELO 为 1293（来自配对人类偏好）。

### Audio-language benchmarks

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).** 10k audio-QA pairs.

> **MMAU（大规模多音频理解）。** 1 万个音频-QA 对。

**MMAU-Pro.** 1800 hard items, four categories: speech / sound / music / multi-audio. Random chance 25% on 4-way. Gemini 2.5 Pro overall ~60%; multi-audio ~22% across all models.

> **MMAU-Pro。** 1800 个难题，四个类别：语音/声音/音乐/多音频。4 选 1 随机猜测 25%。Gemini 2.5 Pro 整体约 60%；所有模型在多音频上约 22%。

**LongAudioBench.** Multi-minute clips with semantic queries. Audio Flamingo Next beats Gemini 2.5 Pro.

> **LongAudioBench。** 多分钟音频片段 + 语义查询。Audio Flamingo Next 超过 Gemini 2.5 Pro。

**AudioCaps / Clotho.** Captioning benchmarks. SPICE, CIDEr, FENSE metrics.

> **AudioCaps / Clotho。** 音频描述基准测试。SPICE、CIDEr、FENSE 指标。

### Streaming speech-to-speech

> 流式语音到语音指标

**Latency P50 / P95 / P99.** Wall-clock from end-of-user-speech to first audible response. Moshi: 200 ms; GPT-4o Realtime: 300 ms.

> **延迟 P50 / P95 / P99。** 从用户语音结束到首个可听响应的实际时间。Moshi：200 ms；GPT-4o Realtime：300 ms。

**WER / MOS** on the output.

> 输出上的 **WER / MOS**。

**Barge-in responsiveness.** Time from user interrupt to assistant mute. Target &lt; 150 ms.

> **打断响应时间。** 从用户打断到助手静音的时间。目标低于 150 ms。

### The 2026 leaderboards

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。




## Build It | 动手实现

### Step 1: WER with normalization

> 步骤 1：带标准化的 WER

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

### Step 2: TTS round-trip WER

> 步骤 2：TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Step 3: SECS for voice cloning

> 步骤 3：语音克隆的 SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Step 4: FAD for music generation

> 步骤 4：音乐生成的 FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Step 5: EER for speaker verification (same code as Lesson 6)

> 步骤 5：说话人验证的 EER（与第 6 课相同的代码）

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

## Use It | 用框架实现

Pair every deploy with a fixed eval harness that runs on every model update. Three cardinal rules:

> 每次部署都配一个固定的评估工具，在每次模型更新时运行。三条核心规则：

1. **Normalize before scoring.** Lowercase, punctuation-strip, number-expand. Report the normalization rule.
   中文翻译：**评分前标准化。** 转小写、去标点、数字展开。报告标准化规则。
2. **Report distributions, not averages.** P50/P95/P99 for latency. Per-class recall for classification. Per-category for MMAU.
   中文翻译：**报告分布而非均值。** 延迟用 P50/P95/P99。分类用每类召回率。MMAU 用每类别。
3. **Run one canonical public benchmark.** Even if your production data differs, reporting on Open ASR / TTS Arena / MMAU lets reviewers compare apples-to-apples.
   中文翻译：**运行一个权威公共基准。** 即使你的生产数据不同，在 Open ASR / TTS Arena / MMAU 上报告可以让评审者做公平对比。



## Pitfalls

> 常见陷阱

- **UTMOS extrapolation.** Trained on VCTK-style clean speech; scores noisy / cloned / emotional audio poorly.
  中文翻译：**UTMOS 外推问题。** 在 VCTK 风格的纯净语音上训练；对嘈杂/克隆/情感语音评分效果差。
- **MOS panel bias.** 20 Amazon Mechanical Turk workers ≠ 20 target users. Pay for a domain panel if stakes are high.
  中文翻译：**MOS 评审团偏差。** 20 个 Amazon Mechanical Turk 工作者不等于 20 个目标用户。如果风险高，花钱请领域专家评审团。
- **FAD depends on reference set.** Compare against the same reference distribution across models.
  中文翻译：**FAD 依赖参考集。** 跨模型比较时使用相同的参考分布。
- **Aggregate WER.** A 5% WER overall can hide 30% WER on accented speech. Report by demographic slice.
  中文翻译：**汇总 WER。** 整体 5% 的 WER 可能掩盖带口音语音 30% 的 WER。按人口统计分组报告。
- **Public benchmark saturation.** Most frontier models are near the ceiling on standard benchmarks. Build an in-house held-out set that reflects your traffic.
  中文翻译：**公共基准饱和。** 大多数前沿模型在标准基准上已接近天花板。构建反映你真实流量的内部留出集。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-audio-evaluator.md`. Pick metrics, benchmarks, and reporting format for any audio model release.

> 保存为 `outputs/skill-audio-evaluator.md`。为任何音频模型发布选择指标、基准和报告格式。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Compute WER / CER / EER / SECS / FAD-ish / MMAU-ish on toy inputs.
   中文翻译：**简单。** 运行 `code/main.py`。在玩具输入上计算 WER / CER / EER / SECS / 类 FAD / 类 MMAU。
2. **Medium.** Build a TTS round-trip WER harness. Run your Kokoro or F5-TTS output through Whisper. Compute WER over 50 prompts. Flag prompts with WER &gt; 10%.
   中文翻译：**中等。** 构建 TTS 回环 WER 评估工具。用 Whisper 处理你的 Kokoro 或 F5-TTS 输出。在 50 个提示上计算 WER。标记 WER 大于 10% 的提示。
3. **Hard.** Score your Lesson 10 LALM choice on MMAU-Pro speech + multi-audio subsets (50 items each). Report per-category accuracy and compare with the published number.
   中文翻译：**困难。** 在 MMAU-Pro 的语音 + 多音频子集上（各 50 项）评估你第 10 课选择的 LALM。报告每类别准确率并与发表数据对比。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| WER | ASR score | `(S+D+I)/N` at word level after normalization. / 标准化后的词级 `(S+D+I)/N` |
| CER | Character WER | For tone languages or char-level systems. / 用于声调语言或字符级系统 |
| MOS | Human opinion | 1-5 rating; 20+ listeners × 100 samples. / 1-5 分评分；20+ 听者 × 100 样本 |
| UTMOS | ML MOS predictor | Learned model; correlates ~0.9 with human MOS. / 学习型模型；与人类 MOS 相关性约 0.9 |
| SECS | Voice-clone similarity | ECAPA cosine between reference and clone. / 参考与克隆之间的 ECAPA 余弦相似度 |
| EER | Speaker verif score | Threshold where FAR = FRR. / FAR = FRR 的阈值 |
| DER | Diarization score | (FA + Miss + Confusion) / total. / (虚警 + 漏检 + 混淆) / 总时间 |
| FAD | Music-gen quality | Fréchet distance on VGGish embeddings. / VGGish 嵌入上的 Fréchet 距离 |
| RTFx | Throughput | Audio seconds per wall-clock second. / 每实际秒处理的音频秒数 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [jiwer](https://github.com/jitsi/jiwer) — WER/CER library with normalization utilities.
  jiwer——带标准化工具的 WER/CER 库。
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) — learned MOS predictor.
  UTMOS（Saeki 等 2022）——学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) — the music-gen standard.
  Fréchet Audio Distance（Kilgour 等 2019）——音乐生成的标准指标。
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) — 2026 live rankings.
  Open ASR 排行榜——2026 实时排名。
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) — human-vote TTS leaderboard.
  TTS Arena——人类投票的 TTS 排行榜。
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) — LALM reasoning leaderboard.
  MMAU-Pro 基准——LALM 推理排行榜。
- [HEAR benchmark](https://hearbenchmark.com/) — audio SSL benchmarks.
  HEAR 基准——音频 SSL 评估基准。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

