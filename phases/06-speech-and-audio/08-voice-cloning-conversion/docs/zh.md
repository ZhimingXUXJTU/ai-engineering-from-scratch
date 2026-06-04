# 语音克隆与语音转换

> 语音克隆用别人的声音朗读你的文字；语音转换把你的声音变成别人的但保留内容。两者的核心都是同一个分解：将说话人身份与内容分离。

> **【中文解读】** 语音克隆用别人的声音朗读你的文字；语音转换把你的声音变成别人的但保留内容。两者的核心都是同一个分解：将说话人身份与内容分离。

> **【拓展：语音克隆的伦理与法律】** 语音克隆技术引发严重的伦理和法律问题——深度伪造语音诈骗、名人声音未经授权使用。2025-2026 年多起诉讼（如 Warner Music 5 亿美元和解案）推动了音频水印和防伪造技术的发展。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**时长：** 约 75 分钟

## 问题引入

2026 年，5 秒音频片段足以用消费级 GPU 高质量克隆任何人的声音。ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox 都提供零样本或少样本克隆。这项技术既是福音（无障碍 TTS、配音、辅助语音），也是武器（诈骗电话、政治深度伪造、知识产权盗窃）。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

两个密切相关的任务：

- **语音克隆（TTS 侧）：** 文本 + 5 秒参考声音 -> 该声音的音频。
- **语音转换（语音侧）：** 源音频（A 说的 X）+ B 的参考声音 -> B 说 X 的音频。

两者都将波形分解为（内容、说话人、韵律）并将一个源的内容与另一个源的说话人重新组合。

2026 年你现在必须遵守的关键约束：**水印和授权门在欧盟（AI 法案，2026 年 8 月可执行）和加利福尼亚州（AB 2905，2025 年生效）中是法律要求的。** 你的流水线必须发出不可听的水印并拒绝非授权克隆。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![语音克隆 vs 转换：分解、交换说话人、重组](../assets/voice-cloning.svg)

**零样本克隆。** 将 5 秒片段传给在数千说话人上训练过的模型。说话人编码器将片段映射到说话人嵌入；TTS 解码器根据该嵌入加文本条件生成。

使用者：F5-TTS（2024）、YourTTS（2022）、XTTS v2（2024）、OpenVoice v2（2024）。

**少样本微调。** 录制目标声音 5-30 分钟。LoRA 微调基础模型一小时。质量从"还行"跃升到"难以区分"。Coqui 和 ElevenLabs 都支持这种模式；社区在 F5-TTS 上使用。

**语音转换（VC）。** 两个家族：

- **识别-合成。** 运行类 ASR 模型提取内容表示（如软音素后验概率 PPG），然后用目标说话人嵌入重新合成。对语言和口音鲁棒。KNN-VC（2023）、Diff-HierVC（2023）使用。
- **解耦。** 训练一个自编码器，在瓶颈处的潜在空间中分离内容、说话人和韵律。推理时交换说话人嵌入。质量较低但更快。AutoVC（2019）、VITS-VC 变体使用。

**基于神经编解码器的克隆（2024+）。** VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox——将音频视为 SoundStream / EnCodec 的离散 token，训练一个大型自回归或流匹配模型在编解码器 token 上。短提示上的质量可与 ElevenLabs 媲美。

### 伦理部分，不是附加品

**水印。** PerTh 和 SilentCipher（2024）在音频中不可感知地嵌入约 16-32 位 ID。能抵抗重编码、流媒体和常见编辑。开源且生产就绪。

**授权门。** 必须为每个克隆输出配对一个可验证的授权记录。"我，某某，于 2026-04-22，授权将此声音用于 X 目的。"存储在防篡改日志中。

**检测。** AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器部署。ASVspoof 2025 挑战赛发布了针对 ElevenLabs、VALL-E 2 和 Bark 输出的 0.8-2.3% EER。

### 数字（2026）

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数 |
|------|----------|-------------------|---------------|------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

SECS > 0.70 对于大多数听众来说通常与目标无法区分。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：用识别-合成做分解（仅代码演示在 main.py 中）

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

概念上简单；实现的工作量在 `tts_model` 和说话人编码器中。

### 步骤 2：用 F5-TTS 做零样本克隆

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

参考转录必须完全匹配音频；不匹配会破坏对齐。

### 步骤 3：用 KNN-VC 做语音转换

```python
import torch
from knnvc import KNNVC  # 2023 模型, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC 运行 WavLM 提取源和目标池的逐帧嵌入，然后用最近邻替换每个源帧。非参数化，一分钟目标语音即可工作。

### 步骤 4：嵌入水印

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # 返回 payload 字节
```

约 32 位 payload，MP3 重编码和轻微噪声后仍可检测。

### 步骤 5：授权门

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（改写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |

## 陷阱

- **参考转录不对齐。** F5-TTS 等要求参考文本完全匹配参考音频，包括标点。
- **混响参考。** 回声会毁掉克隆。录制干声、近距离麦克风。
- **情感不匹配。** "欢快"的训练参考会产生欢快的所有克隆内容。匹配参考情感到目标用途。
- **语言泄漏。** 克隆英语说话人然后让模型说法语通常会带口音；使用跨语言模型（XTTS、VALL-E X）。
- **没有水印。** 从 2026 年 8 月起在欧盟法律上不可交付。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-voice-cloner.md`。设计带授权门 + 水印 + 质量目标的克隆或转换流水线。

## 练习题

1. **简单。** 运行 `code/main.py`。通过计算交换前后两个"说话人"的余弦来演示说话人嵌入交换。
2. **中等。** 使用 OpenVoice v2 克隆自己的声音。测量参考和克隆之间的 SECS。通过 Whisper 测量 CER。
3. **困难。** 对 20 个克隆应用 SilentCipher 水印，通过 128 kbps MP3 编码+解码运行，检测 payload。报告比特准确率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验概率，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用最近的目标池帧替换每个源帧。 |
| 神经编解码器 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入在音频中的比特，重编码后仍可检测。 |
| SECS | 克隆保真度 | 目标和克隆说话人嵌入之间的余弦。 |
| AASIST | 深度伪造检测器 | 防伪模型；检测合成语音。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) —— 开源 SOTA 零样本克隆。
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111) 和 [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) —— 神经编解码器 TTS。
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) —— 基于解耦的语音转换。
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) —— 基于检索的语音转换。
- [SilentCipher (2024) — 音频水印](https://github.com/sony/silentcipher) —— 生产就绪的 32 位音频水印。
- [ASVspoof 2025 结果](https://www.asvspoof.org/) —— 检测器 vs 合成器军备竞赛，2026 年更新。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
