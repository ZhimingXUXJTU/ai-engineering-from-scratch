# Speech Recognition (ASR) — CTC, RNN-T, Attention | 语音识别 — CTC、RNN-T 与注意力机制

> Speech recognition is audio classification at every timestep, glued together by a sequence model that knows English and silence. CTC, RNN-T, and attention are the three ways to do it. Pick one and understand why.

> **【中文解读】** 语音识别是在每个时间步做音频分类，再用序列模型（知道语言和静音规律）把它们粘合起来。三种方法：CTC（连接时序分类）、RNN-T（递归神经网络转换器）、注意力机制。Whisper 使用注意力机制。

> **【拓展：ASR 的应用】** 语音识别是语音助手（Siri、小爱同学）、会议记录（飞书/钉钉实时字幕）、视频字幕自动生成的核心。Whisper 是 2026 年的开源 ASR 标杆。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

You have a 10-second 16 kHz clip. You want a string: "turn on the kitchen lights". The challenge is structural: audio frames do not align one-to-one with characters. The word "okay" might take 200 ms or 1200 ms. Silence punctuates the utterance. Some phonemes are longer than others. The number of output tokens is not known in advance.

> 你有一段 10 秒 16 kHz 的音频。你想要一个字符串："turn on the kitchen lights"。挑战是结构性的：音频帧与字符不是一一对应的。单词"okay"可能占 200 ms 或 1200 ms。静音打断话语。有些音素比其他的更长。输出 token 的数量事先不知道。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Three formulations solve this:

> 三种方案解决这个问题：

1. **CTC (Connectionist Temporal Classification).** Emit per-frame token probabilities including a special *blank*. Collapse repeats and blanks at decode time. Non-autoregressive, fast. Used by wav2vec 2.0, MMS.
   **CTC（连接时序分类）。** 逐帧发射 token 概率，包括特殊的 *blank*。解码时折叠重复和空白。非自回归，快速。wav2vec 2.0、MMS 使用。
2. **RNN-T (Recurrent Neural Network Transducer).** Joint network predicts next token given encoder frame and previous tokens. Streamable. Used by Google's on-device ASR, NVIDIA Parakeet.
   **RNN-T（递归神经网络转换器）。** 联合网络根据编码器帧和之前的 token 预测下一个 token。可流式处理。Google 端侧 ASR、NVIDIA Parakeet 使用。
3. **Attention encoder-decoder.** Encoder compresses audio to hidden states, decoder cross-attends to generate tokens autoregressively. Used by Whisper, SeamlessM4T.
   **注意力编码器-解码器。** 编码器将音频压缩为隐藏状态，解码器通过交叉注意力自回归地生成 token。Whisper、SeamlessM4T 使用。

In 2026, SOTA WER on LibriSpeech test-clean is 1.4% (Parakeet-TDT-1.1B, NVIDIA) and 1.58% (Whisper-Large-v3-turbo). The differences are tiny; the deployment differences are huge.

> 2026 年，LibriSpeech test-clean 上的 SOTA WER 为 1.4%（Parakeet-TDT-1.1B，NVIDIA）和 1.58%（Whisper-Large-v3-turbo）。差异很小；部署差异很大。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.** Let the encoder output `T` frame-level distributions over `V+1` tokens (V chars + blank). For a target string `y` of length `U < T`, any frame alignment that collapses to `y` counts. CTC loss sums over all such alignments. Inference: per-frame argmax, collapse repeats, remove blanks.

> **CTC 直觉。** 让编码器输出 `T` 个帧级分布，每个分布覆盖 `V+1` 个 token（V 个字符 + blank）。对于长度为 `U < T` 的目标字符串 `y`，任何折叠后等于 `y` 的帧对齐都算。CTC 损失对所有这样的对齐求和。推理：逐帧 argmax，折叠重复，移除空白。

Advantages: non-autoregressive, streamable, zero lookahead. Drawback: *conditional independence assumption* — each frame prediction is independent of the others, so there is no internal language model. Fix with an external LM via beam search or shallow fusion.

> 优势：非自回归、可流式处理、零前瞻。缺点：*条件独立性假设*——每帧预测彼此独立，因此没有内部语言模型。通过 beam search 或浅融合的外部 LM 来修复。

**RNN-T intuition.** Adds a *predictor* network that embeds the token history and a *joiner* that combines predictor state with encoder frame into a joint distribution over `V+1` (the `+1` is a null / no-emit). Explicitly models the conditional dependence CTC ignored. Streamable because each step conditions only on past frames and past tokens.

> **RNN-T 直觉。** 添加一个嵌入 token 历史的 *predictor* 网络和一个将 predictor 状态与编码器帧结合为 `V+1` 联合分布的 *joiner*（`+1` 是 null/不发射）。显式建模 CTC 忽略的条件依赖。可流式处理，因为每步仅依赖过去的帧和过去的 token。

Advantages: streamable + internal LM. Drawback: training is more complex and memory-hungry (3D loss lattice); RNN-T loss kernels are a whole library category on their own.

> 优势：可流式 + 内部 LM。缺点：训练更复杂、更耗内存（3D 损失格）；RNN-T 损失核本身就是一个完整的库类别。

**Attention encoder-decoder.** Encoder (6-32 transformer layers) over log-mel frames. Decoder (6-32 transformer layers) cross-attends to encoder outputs to generate tokens autoregressively. No alignment constraint — attention can look anywhere in the audio. Non-streamable unless you restrict attention (chunked Whisper-Streaming, 2024).

> **注意力编码器-解码器。** 编码器（6-32 层 transformer）处理 log-mel 帧。解码器（6-32 层 transformer）通过交叉注意力自回归生成 token。无对齐约束——注意力可以看向音频的任何位置。除非限制注意力（分块 Whisper-Streaming，2024），否则不可流式处理。

Advantages: highest quality on offline ASR, easy to train with standard seq2seq tooling. Drawback: autoregressive latency is proportional to output length; cannot stream without engineering.

> 优势：离线 ASR 质量最高，用标准 seq2seq 工具易于训练。缺点：自回归延迟与输出长度成正比；不做工程优化无法流式处理。

### WER: the one number

> ### WER：唯一的指标

**Word Error Rate** = `(S + D + I) / N`, where S=substitutions, D=deletions, I=insertions, N=reference word count. Matches Levenshtein edit distance at the word level. Lower is better. A WER above 20% is generally unusable; below 5% is human-parity for read speech. 2026 numbers on standard benchmarks:

> **词错误率** = `(S + D + I) / N`，其中 S=替换，D=删除，I=插入，N=参考词数。对应词级别的 Levenshtein 编辑距离。越低越好。WER 超过 20% 通常不可用；低于 5% 对朗读语音达到人类水平。2026 年标准基准上的数字：

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


All these are encoder-decoder or RNN-T based. Pure CTC systems (wav2vec 2.0) sit around 1.8–2.1% on test-clean.

> 这些都是编码器-解码器或 RNN-T 架构。纯 CTC 系统（wav2vec 2.0）在 test-clean 上约 1.8–2.1%。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

### Step 1: greedy CTC decode

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

Two rules: collapse consecutive repeats, drop blanks. Example: `a a _ _ a b b _ c` → `a a b c`.

> 两条规则：折叠连续重复，丢弃空白。示例：`a a _ _ a b b _ c` → `a a b c`。

### Step 2: beam-search CTC

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

Production uses prefix tree beam search with LM fusion; this is the conceptual skeleton.

> 生产环境使用带 LM 融合的前缀树 beam search；这是概念骨架。

### Step 3: WER

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

### Step 4: inference against Whisper

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

One-liner for the strongest general ASR in 2026. Runs on a 24 GB GPU at ~20× realtime.

> 2026 年最强通用 ASR 的一行代码。在 24 GB GPU 上以约 20 倍实时速度运行。

### Step 5: streaming with Parakeet or wav2vec 2.0

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Streaming ASR needs chunked encoder attention and carryover state; use a library that supports it (NeMo for Parakeet, `transformers` pipeline with `chunk_length_s`).

> 流式 ASR 需要分块编码器注意力和转移状态；使用支持它的库（NeMo 用于 Parakeet，`transformers` pipeline 带 `chunk_length_s`）。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## Pitfalls that still ship in 2026

> 2026 年仍然在犯的陷阱

- **No VAD.** Running Whisper on silence produces hallucinations ("Thanks for watching!"). Always gate with VAD.
  **没有 VAD。** 在静音上运行 Whisper 会产生幻觉（"Thanks for watching!"）。务必用 VAD 过滤。
- **Character vs word vs subword WER.** Report word-level WER *after* normalization (lowercase, punctuation stripped).
  **字符 vs 词 vs 子词 WER。** 报告归一化后（小写、去标点）的词级 WER。
- **Language ID drift.** Whisper's auto LID mis-routes noisy clips to Japanese or Welsh; force `language="en"` when you know.
  **语言识别漂移。** Whisper 的自动语言识别会把嘈杂片段误判为日语或威尔士语；已知语言时强制 `language="en"`。
- **Long clips without chunking.** Whisper has a 30-second window. Use `chunk_length_s=30, stride=5` for anything longer.
  **长音频不分块。** Whisper 有 30 秒窗口。对更长的音频使用 `chunk_length_s=30, stride=5`。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-asr-picker.md`. Pick model, decoding strategy, chunking, and LM fusion for a given deployment target.

> 保存为 `outputs/skill-asr-picker.md`。为给定的部署目标选择模型、解码策略、分块和 LM 融合方案。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It greedily decodes a hand-crafted CTC output and computes WER against a reference.
   **简单。** 运行 `code/main.py`。它对手工制作的 CTC 输出进行贪婪解码并计算 WER。
2. **Medium.** Implement the prefix-tree beam search in Step 2 properly (account for the blank merge rule). Compare with greedy on a 10-example synthetic dataset.
   **中等。** 正确实现步骤 2 中的前缀树 beam search（考虑 blank 合并规则）。在 10 个合成样本上与贪婪方法比较。
3. **Hard.** Use `whisper-large-v3-turbo` on [LibriSpeech test-clean](https://www.openslr.org/12). Compute WER on the first 100 utterances. Compare with published numbers.
   **困难。** 在 [LibriSpeech test-clean](https://www.openslr.org/12) 上使用 `whisper-large-v3-turbo`。计算前 100 条语音的 WER。与发表的数据比较。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) — the CTC paper.
  Graves 等 (2006). 连接时序分类——CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711) — the RNN-T paper.
  Graves (2012). 用 RNN 进行序列转换——RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) — the 2022 canonical paper; v3-turbo extension in 2024.
  Radford 等 / OpenAI (2022). Whisper：大规模弱监督的鲁棒语音识别——2022 年经典论文；2024 年 v3-turbo 扩展。
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) — 2026 Open ASR Leaderboard leader.
  NVIDIA NeMo——Parakeet-TDT 模型卡——2026 年 Open ASR 排行榜领先者。
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) — live benchmark across 25+ models.
  Hugging Face——Open ASR 排行榜——25+ 模型的实时基准测试。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

