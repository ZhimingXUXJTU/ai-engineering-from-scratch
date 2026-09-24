# 语音克隆与语音转换

> 语音克隆读取你的文字在别人的声音中.语音转换将你的声音重写成别人的声音,同时保留了你所说的.

> **【中文解读】**语音克隆用别人的声音朗读你的文字;语音转换把你的声音变成别人的但保留内容――两者核心都是同一个分解:将说话人身份与内容分离――

> **【拓展：语音克隆的伦理与法律】**语音克隆技术引发严重的伦理和法律问题深度伪造语音欺诈、名人声音未经授权使用──2025-2026年多起诉案(如华纳音乐5亿美元和解案) 推动了音频水印和防伪技术的发展──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

2026年,一个5秒音频剪辑足以使用消费者GPU制作高质量的任何人的声音克隆.ElevenLabs,F5-TTS,OpenVoice v2,VoiceBox都提供零射击或少数射击克隆.该技术是一种祝福 (可访问性TTS,翻译,辅助声音) 和武器 (诈骗呼叫,政治深假,IP盗窃).

> 2026年,一段5秒音频就足以使用消费级GPU高质量克隆任何人的声音――ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox都提供零样本或少样本克隆――这项技术既是福音(无障碍TTS、配音、辅助声音),也是武器(诈骗电话、政治深度伪造、知识产权盗窃)―

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

两个紧密相关的任务:

> 两个密切相关任务:

- **Voice cloning (TTS-side):**文字+5秒的参考语音 →在这个语音中的音频.
  **声音克隆（TTS 侧）：**文本 + 5 秒参考声音 → 该声音的音频──
- **Voice conversion (speech-side):**源音频 (人 A 说 X) +人 B 的参考声音 → B 说 X 的音频.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

两者都将波形 (内容,扬声器,声) 纳入一个形式,并将来自一个来源的内容重新组合到另一个来源的扬声器.

> 两者都将波形分解为内容、说话人、律) 并从一个来源取内容与另一个来源的说话人重新组合.

现在你在2026年将面临的关键限制:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**你的管道必须发出无声水印,拒绝非同意的克隆.

> 现在,我们需要一个新的解决方案.**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的**你的流水线必须发出不可听闻的水印并拒绝未经同意的克隆.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**传递一个5秒钟的剪辑到一个已经在数千个扬声器上训练的模型.扬声器编码器将剪辑映射到一个嵌入式扬声器;TTS解码器在嵌入式加上文本上设置条件.

> **零样本克隆。**将5秒音频传给了数千个说话人训练过的模型.

已使用:F5-TTS (2024),YourTTS (2022),XTTS v2 (2024),OpenVoice v2 (2024).

> 您的TTS (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (您的TTS) (TTS)

**Few-shot fine-tuning.**记录目标声音的5-30分钟.LoRA-细调一个基本模型一个小时.质量从"好"跳到"不可分辨".科基和ElevenLabs都支持这种模式;社区使用它与F5-TTS.

> **少样本微调。**录制目标声音 5-30 分钟.洛拉 微调基础模型一小时.质量从"还行"跳到"无法区分"――Coqui 和 ElevenLabs 都支持这种模式.社区使用F5-TTS实现――

**Voice conversion (VC).**两个家庭:

> **语音转换（VC）。**两个家族:

- **Recognition-synthesis.**运行ASR类似模型以提取内容表示 (例如软音响后面,PPG),然后再合成目标扬声器嵌入. 强有力的语言和口音. KNN-VC (2023),Diff-HierVC (2023).
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG),然后使用目标说话人嵌入重新合成──对语言和口音鲁棒──KNN-VC(2023)、Diff-HierVC(2023) 使用──
- **Disentanglement.**训练一个自动编码器,在瓶中隐藏空间中分开内容,扬声器和声器.在推理时内嵌的音箱交换.质量较低但更快.由 AutoVC (2019) 应用,VITS-VC变体.
  **解耦。**训练自编码器在瓶处的潜在空间中分离内容、话语人和律──推理时交换话语的人嵌入──质量较低但更快──AutoVC(2019)、VITS-VC 变体使用──推理时交换话语的人嵌入──质量较低但更快──自编码器在瓶处的潜在空间中分离内容、话语人和律──推理时交换话语人嵌入──

**Neural codec-based cloning (2024+).**视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视频视

> **基于神经编解码器的克隆（2024+）。**音频视频将视频视为 SoundStream/EnCodec的离散代币,在编解码代币上训练大型自归或流匹配模型──短提示上质量可与ElevenLabs相当──

### 伦理问题,不是一个子

> ### 伦理问题,不是可选项

**Watermarking.**珀斯 (珀斯) 和SilentCipher (2024) 嵌入了~16-32位ID无形地在音频中. 存活了重新编码,流媒体和常见编辑. 准备生产的开源.

> **水印。**和沉默Cipher (PertTh 和 SilentCipher) 已被重新编码,流传输和常见编辑.

**Consent gates.**必须将所有被克隆的输出与可验证的同意记录结合起来. "我,罗希特,在2026-04-22日,授权这个声音X目的.

> **同意门。**每个克隆输出必须配合可验证的同意记录.

**Detection.**美国ASIST,RawNet2和Wav2Vec2-AASIST作为探测器. ASVspoof 2025挑战发布了对ElevenLabs,VALL-E2和Bark输出的最先进探测器的0.82.3%的EER.

> **检测。**作为检测器发布――ASVspoof 2025 挑战赛发布了SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为0.8-2.3%──

### 统计数 (2026)

> 2026 年的数字

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


对于大多数听众来说,SECS > 0.70通常无法与目标区分.

> 对于大多数听众来说,SECS > 0.70通常与目标无法区分.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.
```figure
sp-voice-factorize
```

## 建立它

### 步骤1:与识别合成分解 (仅在 main.py 中进行代码演示)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

概念简单; 实施量为`tts_model`它们是"音器"的编码器.

> 概念上简单;实现量在`tts_model`和说话人编码器中.

### 步骤2:F5-TTS的零射击克隆

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

引用文本必须与音频完全匹配;不匹配打断了对齐.

> 转录必须与音频完全匹配;不匹配会破坏对齐.

### 步骤3:使用 KNN-VC 进行语音转换

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC运行WavLM以提取源和目标池的每个框架嵌入,然后将每个源框架替换成池中的最近邻居.非参数,使用一个分钟的目标语音.

> 运行KN-VC 波动 提取源和目标池的逐个嵌入,然后使用池中最近的邻居替换每个源──非参数化,一分钟目标语音即可工作──

### 步骤 4:嵌入一个水印

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

通过MP3重新编码和轻噪声可检测到的32位的有效载荷.

> 约32位载荷,MP3重编码和轻度噪音后仍可检测.

### 步骤5:同意门

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## 陷

> 常见陷

- **Misaligned reference transcript.**要求引用文本与引用音频精确一致,包括分分.
  **参考转录不对齐。**标准标准:F5-TTS等要求参考文献与参考频频完全匹配,包括标点.
- **Reverberant reference.**声声杀了克隆,记录干燥,近距离麦克风.
  **混响参考。**声声会毁掉克隆.
- **Emotional mismatch.**训练参考"欢乐"产生欢乐的克隆, 匹配参考情感与目标使用.
  **情感不匹配。**训练参考"欢快"会对所有内容产生欢快克隆――匹配参考情感与目标用途――
- **Language leakage.**克隆一个英语发音者,然后要求模型说法语,通常都带着口音;使用跨语言模型 (XTTS,VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍然带有口音;使用跨语言模型 (XTTS、VALL-E X) ⋅
- **No watermark.**从2026年8月起,在欧盟合法不可出货.
  **没有水印。**从2026年8月起,欧盟法律上不可发布.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-voice-cloner.md`设计一个具有同意门+水标+质量目标的克隆或转换管道.

> 保存为`outputs/skill-voice-cloner.md`◎设计带同意门 + 水印 + 质量目标的克隆或转换流水线──

## 练习题

1. **Easy.**跑步`code/main.py`通过计算两个"扬声器"之间的前后和后的代价,证明了扬声器嵌入式交换.
   **简单。**运行`code/main.py`通过计算交换前后两个"说话人"的余弦相似度来演示说话人嵌入交换.
2. **Medium.**通过OpenVoice v2来克隆自己的声音. 测量引用和克隆之间的SECS. 测量通过声的 CER.
   **中等。**用OpenVoice v2 克隆你自己的声音――测量参考与克隆之间的SECS――通过语测量 CER――
3. **Hard.**应用SilentCipher水标到20个克隆,运行它们通过128 kbps MP3编码+解码,检测有效载荷.报告位准确性.
   **困难。**对于20个克隆应用 SilentCipher 水印,通过 128 kbps MP3编码+解码,检测载荷――报告比特准确率――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885)开源SOTA零射击克隆.
  陈等 (2024).F5-TTS开源SOTA 零样本克隆.
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)其他[VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370)神经编码器TTS.
                                                                                                                                                                                                                                                                
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879)基于解脱的语音转换.
  等 (2019). 基于解的语音转换.
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975)基于检索的风险投资.
  基因检索的语音转换──
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) 已准备生产的32位音频水标.
  无声声水印 生产可用 32位音频水印
- [ASVspoof 2025 results](https://www.asvspoof.org/)检测器与合成器武器竞赛,更新于2026年.
  美国国家安全局2025年 结果检测器vs合成器军备竞赛,2026年更新──

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

