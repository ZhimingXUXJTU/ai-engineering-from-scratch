# Voice Anti-Spoofing & Audio Watermarking — ASVspoof 5, AudioSeal, WaveVerify | 语音防伪与音频水印

> Voice cloning shipped faster than defenses. 2026 production voice systems need two things: a detector (AASIST, RawNet2) that classifies real vs fake speech, and a watermark (AudioSeal) that survives compression and editing. Ship both or do not ship voice cloning.

> **【中文解读】** 语音克隆技术跑在了防御前面。2026 年的生产级语音系统需要两样东西：检测器（AASIST、RawNet2）区分真假语音，水印（AudioSeal）在压缩和编辑后仍能存活。不做这两项就不要上线语音克隆功能。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

Three related defenses:

> 三种相关防御手段：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


1. **Anti-spoofing / deepfake detection.** Given an audio clip, is it synthetic or real? ASVspoof benchmarks (ASVspoof 2019 → 2021 → 5) are the gold standard.
   中文翻译：**反欺骗/深度伪造检测。** 给定一段音频，判断它是合成的还是真实的？ASVspoof 基准测试（ASVspoof 2019 → 2021 → 5）是黄金标准。
2. **Audio watermarking.** Embed an imperceptible signal in generated audio that a detector can extract later. AudioSeal (Meta) and WavMark are the open options.
   中文翻译：**音频水印。** 在生成的音频中嵌入不可感知的信号，检测器之后可以提取。AudioSeal（Meta）和 WavMark 是开源选项。
3. **Authenticated provenance.** Cryptographic signing of audio files + metadata. C2PA / Content Authenticity Initiative.
   中文翻译：**认证来源。** 音频文件 + 元数据的加密签名。C2PA / 内容真实性倡议。

Detection handles adversaries who don't cooperate. Watermarking handles compliance — AI-generated audio should be identifiable as such. Both are required in 2026.

> 检测应对不配合的攻击者。水印应对合规性——AI 生成的音频应可被识别。2026 年两者都是必需的。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5 — the 2024-2025 benchmark

> ASVspoof 5 — 2024-2025 年基准测试

Biggest change from prior editions:

> 与之前版本相比的最大变化：

- **Crowdsourced data** (not studio clean) — realistic conditions.
  中文翻译：**众包数据**（非录音棚纯净数据）——真实条件。
- **~2000 speakers** (vs ~100 before).
  中文翻译：**约 2000 名说话人**（之前约 100 名）。
- **32 attack algorithms.** TTS + voice conversion + adversarial perturbation.
  中文翻译：**32 种攻击算法。** TTS + 语音转换 + 对抗性扰动。
- **Two tracks.** Countermeasure (CM) standalone detection; Spoofing-robust ASV (SASV) for biometric systems.
  中文翻译：**两个赛道。** 反制措施（CM）独立检测；生物识别系统的抗欺骗 ASV（SASV）。

State-of-the-art on ASVspoof 5: ~7.23% EER. On the older ASVspoof 2019 LA: 0.42% EER. Real-world deployment: expect 5-10% EER on in-the-wild clips.

> ASVspoof 5 上的 SOTA：约 7.23% EER。在较旧的 ASVspoof 2019 LA 上：0.42% EER。实际部署：预期在野外音频上 EER 为 5-10%。

### AASIST and RawNet2 — detection model families

> AASIST 和 RawNet2 — 检测模型家族

**AASIST** (2021, updated through 2026). Graph-attention on spectral features. Current SOTA on ASVspoof 5 countermeasure task.

> **AASIST**（2021 年，持续更新至 2026 年）。基于频谱特征的图注意力机制。ASVspoof 5 反制措施任务的当前 SOTA。

**RawNet2.** Convolutional front-end over raw waveform + TDNN backbone. Simpler baseline; still competitive with fine-tuning.

> **RawNet2。** 原始波形上的卷积前端 + TDNN 骨干网络。更简单的基线；微调后仍有竞争力。

**NeXt-TDNN + SSL features.** 2025 variant: ECAPA-style + WavLM features + focal loss. Achieves the 0.42% EER on ASVspoof 2019 LA.

> **NeXt-TDNN + SSL 特征。** 2025 年变体：ECAPA 风格 + WavLM 特征 + focal loss。在 ASVspoof 2019 LA 上达到 0.42% EER。

### AudioSeal — the 2024 watermark default

> AudioSeal — 2024 年的水印默认方案

Meta's **AudioSeal** (Jan 2024, v0.2 Dec 2024). Key design:

> Meta 的 **AudioSeal**（2024 年 1 月，v0.2 于 2024 年 12 月）。核心设计：

- **Localized.** Detects the watermark per-frame at 16 kHz sample resolution (1/16000 s).
  中文翻译：**局部化。** 以 16 kHz 采样分辨率逐帧检测水印（1/16000 秒）。
- **Generator + detector jointly trained.** Generator learns to embed inaudible signal; detector learns to find it through augmentations.
  中文翻译：**生成器 + 检测器联合训练。** 生成器学习嵌入不可听信号；检测器学习通过增强找到它。
- **Robust.** Survives MP3 / AAC compression, EQ, speed-shift ±10%, noise mix +10 dB SNR.
  中文翻译：**鲁棒。** 能经受 MP3/AAC 压缩、均衡、±10% 变速、+10 dB SNR 噪声混合。
- **Fast.** Detector runs at 485× realtime; 1000× faster than WavMark.
  中文翻译：**快速。** 检测器以 485 倍实时速度运行；比 WavMark 快 1000 倍。
- **Capacity.** 16-bit payload (can encode model ID, generation timestamp, user ID) embeddable in each utterance.
  中文翻译：**容量。** 16 位载荷（可编码模型 ID、生成时间戳、用户 ID）可嵌入每段语音。

### WavMark

The pre-AudioSeal open baseline. Invertible neural network, 32 bits/sec. Problems:

> AudioSeal 之前的开源基线。可逆神经网络，32 位/秒。问题：

- Synchronization brute-force is slow.
  中文翻译：同步暴力破解很慢。
- Can be removed by Gaussian noise or MP3 compression.
  中文翻译：可被高斯噪声或 MP3 压缩去除。
- Not real-time friendly.
  中文翻译：不适合实时场景。

### WaveVerify (July 2025)

Addresses AudioSeal's weaknesses — specifically temporal manipulations (reversal, speed). Uses FiLM-based generator + Mixture-of-Experts detector. Competitive with AudioSeal on standard attacks; handles temporal edits.

> WaveVerify（2025 年 7 月）。解决 AudioSeal 的弱点——特别是时间操作（反转、变速）。使用基于 FiLM 的生成器 + MoE 检测器。在标准攻击上与 AudioSeal 相当；能处理时间编辑。

### The gap adversaries exploit

From AudioMarkBench: "under pitch shift, all watermarks show Bit Recovery Accuracy below 0.6, indicating near-complete removal." **Pitch-shift is the universal attack.** No 2026 watermark is fully robust to aggressive pitch modification. This is why you need detection (AASIST) alongside watermarking.

> 攻击者利用的漏洞。来自 AudioMarkBench："在音高偏移下，所有水印的位恢复准确率低于 0.6，表明几乎完全被去除。"**音高偏移是通用攻击。** 没有任何 2026 年的水印能完全抵御激进的音高修改。这就是为什么你需要检测（AASIST）与水印配合使用。

### C2PA / Content Authenticity Initiative

Not an ML technique — a manifest format. Audio files carry cryptographically signed metadata about creation tool, author, date. Audobox / Seamless use it. Good for provenance; does nothing if a bad actor re-encodes and strips metadata.

> C2PA / 内容真实性倡议。不是机器学习技术——是一种清单格式。音频文件携带关于创建工具、作者、日期的加密签名元数据。Audobox / Seamless 使用它。有利于溯源；但如果恶意行为者重新编码并剥离元数据则无效。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。




## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: a simple spectral-feature detector (toy)

> 步骤 1：简单的频谱特征检测器（玩具版）

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

Synthetic speech often has unusually flat high-frequency energy. Production detectors use AASIST, not this. But the intuition holds.

> 合成语音通常具有异常平坦的高频能量。生产级检测器使用 AASIST，而不是这个。但直觉是正确的。

### Step 2: AudioSeal embed + detect

> 步骤 2：AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Step 3: evaluation — EER

> 步骤 3：评估 — EER（等错误率）

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Step 4: the production integration

> 步骤 4：生产级集成

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Every generation ships: (1) watermark, (2) signed manifest, (3) retention-policy-compliant audit log.

> 每次生成的输出都包含：（1）水印，（2）签名清单，（3）符合保留策略的审计日志。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning | AudioSeal embed on every output (non-negotiable) |
| Biometric voice unlock | AASIST + ECAPA ensemble; liveness challenge |
| Call-center fraud detection | AASIST on 20% sample of incoming calls |
| Podcast authenticity | C2PA signing on upload, AudioSeal if AI-generated |
| Research / training detectors | ASVspoof 5 train/dev/eval sets |



## Pitfalls

> 常见陷阱

- **Watermark without detector ever running.** Pointless. Ship the detector in your CI.
  中文翻译：**嵌入水印但从未运行检测器。** 毫无意义。把检测器集成到 CI 中。
- **Detection without calibration.** AASIST trained on ASVspoof LA overfits; real-world accuracy drops. Calibrate on your domain.
  中文翻译：**检测未校准。** 在 ASVspoof LA 上训练的 AASIST 会过拟合；实际准确率下降。在你的领域数据上校准。
- **Pitch-shift gap.** Aggressive pitch shift removes most watermarks. Have a detection fallback.
  中文翻译：**音高偏移漏洞。** 激进的音高偏移能去除大多数水印。准备检测作为后备。
- **Metadata strip-and-rehost.** C2PA is trivially bypassable by re-encoding. Always add cryptographic + perceptual (watermark) defense together.
  中文翻译：**元数据剥离重新托管。** C2PA 通过重新编码即可轻易绕过。始终同时使用加密 + 感知（水印）防御。
- **Liveness as detection.** Ask user to say a random phrase. Prevents replay attacks but not real-time cloning.
  中文翻译：**活体检测作为检测手段。** 让用户说一个随机短语。能防止重放攻击但不能防止实时克隆。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-spoof-defender.md`. Pick detection model, watermark, provenance manifest, and operational playbook for a voice-gen deployment.

> 保存为 `outputs/skill-spoof-defender.md`。为一个语音生成部署选择检测模型、水印、来源清单和运营手册。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Toy detector + toy watermark embed/detect on synthetic audio.
   中文翻译：**简单。** 运行 `code/main.py`。在合成音频上测试玩具检测器 + 玩具水印嵌入/检测。
2. **Medium.** Install `audioseal`, embed a 16-bit payload in a TTS output, re-decode. Corrupt the audio with noise and measure Bit Recovery Accuracy.
   中文翻译：**中等。** 安装 `audioseal`，在 TTS 输出中嵌入 16 位载荷，重新解码。用噪声损坏音频并测量位恢复准确率。
3. **Hard.** Fine-tune a RawNet2 or AASIST on ASVspoof 2019 LA. Measure EER. Test on a held-out set of F5-TTS-generated clips — see how OOD detection degrades.
   中文翻译：**困难。** 在 ASVspoof 2019 LA 上微调 RawNet2 或 AASIST。测量 EER。在留出的 F5-TTS 生成音频集上测试——观察 OOD 检测的退化程度。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) — the current benchmark.
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) — the watermark default.
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150) — MoE detector for temporal attacks.
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) — the SOTA detection backbone.
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) — robustness evaluation.
- [C2PA specification](https://c2pa.org/specifications/specifications/) — provenance manifest format.

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

