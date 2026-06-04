# 语音识别 — CTC、RNN-T 与注意力机制

> 语音识别是在每个时间步做音频分类，再用序列模型（知道语言和静音规律）把它们粘合起来。三种方法：CTC（Connectionist Temporal Classification，连接时序分类）、RNN-T（Recurrent Neural Network Transducer，递归神经网络转换器）、注意力机制。Whisper 使用注意力机制。

> **【中文解读】** 语音识别是在每个时间步做音频分类，再用序列模型（知道语言和静音规律）把它们粘合起来。三种方法：CTC（连接时序分类）、RNN-T（递归神经网络转换器）、注意力机制。Whisper 使用注意力机制。

> **【拓展：ASR 的应用】** 语音识别是语音助手（Siri、小爱同学）、会议记录（飞书/钉钉实时字幕）、视频字幕自动生成的核心。Whisper 是 2026 年的开源 ASR 标杆。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**时长：** 约 45 分钟

## 问题引入

你有一段 10 秒的 16 kHz 音频片段。你想要一个字符串："turn on the kitchen lights"。挑战是结构性的：音频帧与字符不是一一对应的。单词"okay"可能需要 200 ms 或 1200 ms。静音分割话语。某些音素比其他的长。输出 token 数量不可预知。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

三种公式化方法解决这个问题：

1. **CTC（连接时序分类）。** 逐帧发射 token 概率（包括特殊的 *blank*）。解码时折叠重复和 blank。非自回归，快速。wav2vec 2.0、MMS 使用。
2. **RNN-T（递归神经网络转换器）。** 联合网络根据编码器帧和之前的 token 预测下一个 token。可流式。Google 端上 ASR、NVIDIA Parakeet 使用。
3. **注意力编码器-解码器。** 编码器将音频压缩为隐藏状态，解码器通过交叉注意力自回归地生成 token。Whisper、SeamlessM4T 使用。

2026 年，LibriSpeech test-clean 上的 SOTA WER 为 1.4%（Parakeet-TDT-1.1B，NVIDIA）和 1.58%（Whisper-Large-v3-turbo）。差异微小；部署差异巨大。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![三种 ASR 公式：CTC、RNN-T、注意力编码器-解码器](../assets/asr-formulations.svg)

**CTC 直觉。** 让编码器输出 `T` 个帧级分布，每个在 `V+1` 个 token 上（V 个字符 + blank）。对于长度 `U < T` 的目标字符串 `y`，任何折叠后等于 `y` 的帧对齐都计数。CTC 损失对所有这类对齐求和。推理：逐帧 argmax，折叠重复，移除 blank。

优势：非自回归、可流式、零前瞻。缺点：*条件独立假设*——每帧预测与其他帧独立，因此没有内部语言模型。通过 beam search 或浅层融合使用外部 LM 修复。

**RNN-T 直觉。** 添加一个 *预测器* 网络来嵌入 token 历史，以及一个 *合并器* 将预测器状态与编码器帧组合成 `V+1` 上的联合分布（`+1` 是空/不发射）。显式建模 CTC 忽略的条件依赖。可流式，因为每步只依赖过去的帧和过去的 token。

优势：可流式 + 内部 LM。缺点：训练更复杂、更耗内存（3D 损失格）；RNN-T 损失内核本身就是一整个库类别。

**注意力编码器-解码器。** 编码器（6-32 层 Transformer）处理对数 Mel 帧。解码器（6-32 层 Transformer）交叉注意力编码器输出以自回归生成 token。没有对齐约束——注意力可以看音频中的任何位置。除非限制注意力（分块 Whisper-Streaming，2024），否则不可流式。

优势：离线 ASR 最高质量，使用标准 seq2seq 工具易于训练。缺点：自回归延迟与输出长度成正比；不经过工程改造无法流式。

### WER：那个数字

**词错率（WER, Word Error Rate）** = `(S + D + I) / N`，其中 S=替换，D=删除，I=插入，N=参考词数。匹配词级别的 Levenshtein 编辑距离。越低越好。WER 超过 20% 通常不可用；低于 5% 在朗读语音上达到人类水平。2026 年标准基准上的数字：

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

以上都是编码器-解码器或 RNN-T 架构。纯 CTC 系统（wav2vec 2.0）在 test-clean 上约 1.8-2.1%。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：贪心 CTC 解码

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: 逐帧概率向量列表
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

两条规则：折叠连续重复，丢弃 blank。示例：`a a _ _ a b b _ c` -> `a a b c`。

### 步骤 2：Beam-search CTC

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

生产环境使用带 LM 融合的前缀树 beam search；这是概念骨架。

### 步骤 3：WER

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### 步骤 4：用 Whisper 推理

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

2026 年最强通用 ASR 的一行调用。在 24 GB GPU 上约 20 倍实时速度运行。

### 步骤 5：用 Parakeet 或 wav2vec 2.0 流式推理

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

流式 ASR 需要分块编码器注意力和状态传递；使用支持它的库（NeMo 用于 Parakeet，带 `chunk_length_s` 的 `transformers` 流水线）。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 选择 |
|------|------|
| 英语，离线，最高质量 | Whisper-large-v3-turbo |
| 多语言，鲁棒 | SeamlessM4T v2 |
| 流式，低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘，移动端，<500 ms 延迟 | Whisper-Tiny 量化版或 Moonshine（2024） |
| 长音频 | Whisper + 基于 VAD 的分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |

## 2026 年仍在出现的陷阱

- **没有 VAD。** 在静音上运行 Whisper 会产生幻觉（"Thanks for watching!"）。务必用 VAD 做门控。
- **字符 vs 词 vs 子词 WER。** 报告归一化后（小写、去除标点）的词级 WER。
- **语言识别漂移。** Whisper 的自动 LID 将嘈杂片段错误路由到日语或威尔士语；已知语言时强制 `language="en"`。
- **长片段未分块。** Whisper 有 30 秒窗口。超过此长度使用 `chunk_length_s=30, stride=5`。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-asr-picker.md`。为给定的部署目标选择模型、解码策略、分块方案和 LM 融合方式。

## 练习题

1. **简单。** 运行 `code/main.py`。它贪心解码手工制作的 CTC 输出并计算与参考的 WER。
2. **中等。** 正确实现步骤 2 的前缀树 beam search（处理 blank 合并规则）。在 10 个合成样本上与贪心解码比较。
3. **困难。** 用 `whisper-large-v3-turbo` 在 [LibriSpeech test-clean](https://www.openslr.org/12) 上运行。计算前 100 条话语的 WER。与公布数字比较。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| CTC | blank-token 损失 | 对所有帧到 token 对齐的边际化；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编码器-解码器 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的那个数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空的那个 | CTC 中的特殊 token，表示"此帧不发射"。 |
| LM 融合 | 外部语言模型 | 在 beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) —— CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711) —— RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) —— 2022 年标志性论文；v3-turbo 扩展于 2024 年。
- [NVIDIA NeMo — Parakeet-TDT 卡片](https://huggingface.co/nvidia/parakeet-tdt-1.1b) —— 2026 年开放 ASR 排行榜领先者。
- [Hugging Face — 开放 ASR 排行榜](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) —— 25+ 模型的实时基准。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
