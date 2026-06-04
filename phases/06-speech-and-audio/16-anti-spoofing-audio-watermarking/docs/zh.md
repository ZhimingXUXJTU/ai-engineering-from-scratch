# 语音防伪与音频水印 — ASVspoof 5、AudioSeal、WaveVerify

> 语音克隆技术跑在了防御前面。2026 年的生产级语音系统需要两样东西：检测器（AASIST、RawNet2）区分真假语音，水印（AudioSeal）在压缩和编辑后仍能存活。不做这两项就不要上线语音克隆功能。

> **【中文解读】** 语音克隆技术跑在了防御前面。2026 年的生产级语音系统需要两样东西：检测器（AASIST、RawNet2）区分真假语音，水印（AudioSeal）在压缩和编辑后仍能存活。不做这两项就不要上线语音克隆功能。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**时长：** 约 75 分钟

## 问题引入

三种相关防御：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. **防伪 / 深度伪造检测。** 给定一段音频，它是合成的还是真实的？ASVspoof 基准（ASVspoof 2019 -> 2021 -> 5）是黄金标准。
2. **音频水印。** 在生成音频中嵌入不可感知的信号，检测器之后可以提取。AudioSeal（Meta）和 WavMark 是开源选择。
3. **认证来源。** 音频文件的加密签名 + 元数据。C2PA / 内容真实性倡议。

检测处理不合作的对手。水印处理合规——AI 生成的音频应可识别为 AI 生成。2026 年两者都是必需的。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![防伪 vs 水印 vs 来源 — 三层防御](../assets/spoofing-watermark.svg)

### ASVspoof 5 — 2024-2025 基准

与之前版本的最大变化：

- **众包数据**（非录音棚干净数据）——真实条件。
- **约 2000 个说话人**（之前约 100 个）。
- **32 种攻击算法。** TTS + 语音转换 + 对抗性扰动。
- **两个赛道。** 独立对策（CM）检测；欺骗鲁棒 ASV（SASV）用于生物识别系统。

ASVspoof 5 上的 SOTA：约 7.23% EER。在较旧的 ASVspoof 2019 LA 上：0.42% EER。实际部署：预期野外片段上 5-10% EER。

### AASIST 和 RawNet2 — 检测模型家族

**AASIST**（2021，更新至 2026）。频谱特征上的图注意力。ASVspoof 5 对策任务当前 SOTA。

**RawNet2。** 原始波形上的卷积前端 + TDNN 骨干。更简单的基线；微调后仍有竞争力。

**NeXt-TDNN + SSL 特征。** 2025 变体：ECAPA 风格 + WavLM 特征 + 焦点损失。在 ASVspoof 2019 LA 上达到 0.42% EER。

### AudioSeal — 2024 水印默认选择

Meta 的 **AudioSeal**（2024 年 1 月，v0.2 2024 年 12 月）。关键设计：

- **本地化。** 在 16 kHz 采样分辨率下逐帧检测水印（1/16000 秒）。
- **生成器 + 检测器联合训练。** 生成器学习嵌入不可听信号；检测器学习通过增强找到它。
- **鲁棒。** 抵抗 MP3 / AAC 压缩、均衡、速度偏移 +/-10%、噪声混合 +10 dB SNR。
- **快速。** 检测器以 485 倍实时运行；比 WavMark 快 1000 倍。
- **容量。** 16 位 payload（可编码模型 ID、生成时间戳、用户 ID）可嵌入每段话语。

### WavMark

AudioSeal 之前的开源基线。可逆神经网络，32 比特/秒。问题：

- 同步暴力破解很慢。
- 可被高斯噪声或 MP3 压缩移除。
- 非实时友好。

### WaveVerify（2025 年 7 月）

解决 AudioSeal 的弱点——特别是时间操作（反转、变速）。使用基于 FiLM 的生成器 + 混合专家检测器。在标准攻击上与 AudioSeal 竞争；处理时间编辑。

### 对手利用的差距

来自 AudioMarkBench："在音高偏移下，所有水印的比特恢复准确率低于 0.6，表明近乎完全移除。"**音高偏移是通用攻击。** 没有 2026 年的水印完全鲁棒于激进的音高修改。这就是为什么你需要检测（AASIST）配合水印。

### C2PA / 内容真实性倡议

不是 ML 技术——一种清单格式。音频文件携带关于创建工具、作者、日期的加密签名元数据。Audobox / Seamless 使用。有利于来源追溯；如果不良行为者重新编码并剥离元数据则无效。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：简单频谱特征检测器（玩具）

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

合成语音通常有异常平坦的高频能量。生产检测器使用 AASIST，不是这个。但直觉成立。

### 步骤 2：AudioSeal 嵌入 + 检测

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
# result: [0, 1] 中的浮点数 —— 水印存在概率
# decoded_payload: 16 位；与嵌入的 payload 匹配
```

### 步骤 3：评估 — EER

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

### 步骤 4：生产集成

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

每次生成交付：(1) 水印，(2) 签名清单，(3) 符合保留政策的审计日志。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

| 用例 | 防御 |
|------|------|
| 发布 TTS / 语音克隆 | 每个输出上嵌入 AudioSeal（不可协商） |
| 生物识别语音解锁 | AASIST + ECAPA 集成；活性挑战 |
| 呼叫中心欺诈检测 | 对 20% 进线通话样本运行 AASIST |
| 播客真实性 | 上传时 C2PA 签名，AI 生成的加 AudioSeal |
| 研究 / 训练检测器 | ASVspoof 5 训练/开发/评估集 |

## 陷阱

- **有水印但检测器从未运行。** 毫无意义。在 CI 中部署检测器。
- **未校准的检测。** AASIST 在 ASVspoof LA 上训练过拟合；真实世界准确率下降。在你的领域上校准。
- **音高偏移差距。** 激进音高偏移移除大多数水印。有检测回退。
- **元数据剥离再托管。** C2PA 通过重新编码可轻易绕过。始终同时添加加密 + 感知（水印）防御。
- **活性作为检测。** 要求用户说一个随机短语。防止重放攻击但不能防止实时克隆。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-spoof-defender.md`。为语音生成部署选择检测模型、水印、来源清单和运维手册。

## 练习题

1. **简单。** 运行 `code/main.py`。玩具检测器 + 玩具水印在合成音频上嵌入/检测。
2. **中等。** 安装 `audioseal`，在 TTS 输出中嵌入 16 位 payload，重新解码。用噪声破坏音频并测量比特恢复准确率。
3. **困难。** 在 ASVspoof 2019 LA 上微调 RawNet2 或 AASIST。测量 EER。在 F5-TTS 生成的留出片段上测试——观察 OOD 检测如何退化。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| ASVspoof | 那个基准 | 两年一次的挑战赛；2024 = ASVspoof 5。 |
| CM（对策） | 检测器 | 分类器：真实语音 vs 合成/转换。 |
| SASV | 说话人验证 + CM | 集成生物识别 + 欺骗检测。 |
| AudioSeal | Meta 水印 | 本地化，16 位 payload，比 WavMark 快 485 倍。 |
| 比特恢复准确率 | 水印存活率 | 攻击后恢复的 payload 比特比例。 |
| C2PA | 来源清单 | 关于创建/作者身份的加密元数据。 |
| AASIST | 检测器家族 | 基于图注意力的防伪 SOTA。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) —— 当前基准。
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) —— 水印默认选择。
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150) —— 用于时间攻击的 MoE 检测器。
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) —— SOTA 检测骨干。
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) —— 鲁棒性评估。
- [C2PA 规范](https://c2pa.org/specifications/specifications/) —— 来源清单格式。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
