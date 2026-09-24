# 语音识别 CTC、RNN-T与注意力机制

> 语音识别是每个时间步骤上的音频分类,由一个知道英语和沉默的序列模型粘在一起.CTC,RNN-T和注意力是这三个方法.

> **【中文解读】**语音识别是每时间步骤做音频分类,再使用序列模型 (知道语言和静音规律) 将它们粘在一起.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学)、会议记录(飞书/钉钉实时字幕)、视频字幕自动生成的核心──语是2026年开源的ASR标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

你有一个10秒16kHz的剪辑.你想要一个字符串:"点燃厨房灯".挑战是结构性的:音频框架不会与字符一致. "好吧"字可能需要200ms或1200ms.沉默点击发言.有些音符比其他更长.输出代码的数量未知事先.

> 你有一个段 10 秒 16 kHz 的音频──你想要一个字符串:"点燃厨房灯"──挑战是结构性的:音频与字符不是一对应的──单词"好吧"可能占据 200 ms或 1200 ms──静音打断话语──有些音素比其它更长──输出代币的数量事先不知道──

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

现在,我们有三种方法来解决这个问题:

> 三种方案解决这个问题:

1. **CTC (Connectionist Temporal Classification).**发射每个框架的代币概率,包括一个特殊的 *空白*. 解码时的崩重复和空白. 非自动降低,快速. 用于 wav2vec 2.0, MMS.
   **CTC（连接时序分类）。**逐发射代币概率,包括特殊的 *空*──解码时折重复和空白──非自归,快速──wav2vec 2.0、MMS 使用──
2. **RNN-T (Recurrent Neural Network Transducer).**联合网络预测下一个代码器框架和之前的代码. 流式. 谷歌的设备ASR,NVIDIA Parakeet使用.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google端侧ASR、NVIDIAParakeet 使用──
3. **Attention encoder-decoder.**编码器将音频压缩到隐藏状态,解码器交叉处理以自动降低生成代币.
   **注意力编码器-解码器。**编码器将频频缩为隐藏状态,解码器通过交叉注意力自归地生成代币――语、无M4T 使用――

2026年,在 LibriSpeech 测试清洁度上,SOTA WER 是1.4% (Parakeet-TDT-1.1B,NVIDIA) 和1.58%.

> 鱼-TDT-1.1B,NVIDIA) 和1.8%的声-大v3-turbo) 差异很小;部署差异很大──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**让编码器输出`T`框架水平分布`V+1`标记 (V字符号 + 空格).`y`长度`U < T`任何的架配线都会崩到`y`输出:每的 argmax,崩重复,删除空白.

> **CTC 直觉。**让编码器输出`T`个级分布,每个分布覆盖`V+1`个标志 ((V 个字符 + 空白) ⋅对于长度为 `U < T`的目标字符串`y`任何折叠后等于`y`对于所有这些对齐求和的损失.

优点:非自行降低,可流动,视角零.缺点: *条件独立假设* 每个框架预测是独立的,因此没有内部语言模型.通过光束搜索或浅融合通过外部LM来解决.

> 优势:非自归、可流式处理、零前──缺点:*条件独立性假设*每预测彼此独立,因此没有内部语言模型──通过光束搜索或浅融合的外部LM 来修复──

**RNN-T intuition.**添加一个 *预测器* 网络,嵌入符号历史和一个 * 结合器* 结合预测器状态和编码器框架,成为一个共同分布`V+1`其他`+1`显然模型了CTC忽略的条件依赖性. 流动性,因为每个步骤只在过去的框架和过去的代币上.

> **RNN-T 直觉。**添加一个嵌入式代币 历史的 *预测器* 网络和一个将预测器 状态与编码器结合为 `V+1`联合分布的 *joiner*(`+1`是无效/不发射) ⋅显式建模 CTC 忽略的条件依赖――可流式处理,因为每一步只依赖过去的和过去的代币――

优点:可流动+内部LM. 缺点:训练更复杂,更需要记忆 (3D损失网格);RNN-T损失内核本身是一个整体库类别.

> 优势:可流式 + 内部LM──缺点:训练更复杂,更耗内存(3D损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**编码器 (6-32 个变压器层) 在日志邮件框架上. 编码器 (6-32 个变压器层) 交叉监督编码输出以自行降低代币. 没有对齐限制 注意力可以在音频中任何地方看. 除非你限制注意力外,无法流媒体 (碎片的声流, 2024).

> **注意力编码器-解码器。**编码器(6-32层变压器) 处理日志──解码器(6-32层变压器) 通过交叉注意力自归生成代币──无对齐约束注意力可以看到频频的任何位置──除非限制注意力──分块 微笑流,2024),否则不可流式处理──

优点:在线ASR上提供最高质量,使用标准seq2seq工具进行训练很容易.缺点:自动降低延迟与输出长度相比例;不能在没有工程的情况下流.

> 优势:离线ASR 质量最高,使用标准seq2seq 工具易于训练――缺点:自归延迟与输出长度成正比;不做工程优化无法流式处理――

### 单个号码

> ### 唯一指标

**Word Error Rate**`(S + D + I) / N`根据Levenstein的数据,在Levenstein的数据中,S=替代,D=删除,I=插入,N=引用词数.

> **词错误率**`(S + D + I) / N`对于应词级别的莱文施泰因编辑距离――越低越好――WER 超过20%通常不可用;低于5%对读音达到人类水平――2026年标准基准上的数字:

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

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


所有这些都是基于编码器-解码器或RNN-T的.纯CTC系统 (wav2vec 2.0) 在测试清洁时约为1.82.1%.

> 这些都是编码器-解码器或RNN-T 架构――纯CTC系统(wav2vec 2.0) 在测试清洁上约1.82.1%──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.
```figure
ctc-collapse
```

## 建立它

### 步骤1:贪的CTC解码

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

两条规则: 连续重复,放空.`a a _ _ a b b _ c`其他`a a b c`现在,我们要去.

> 两条规则:折叠连续重复,丢弃空白.`a a _ _ a b b _ c`其他`a a b c`,我知道.

### 步骤2:光束检查CTC

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

制作使用LM融合的先树束搜索;这是概念骨架.

> 生产环境使用带LM 融合的前树束搜索;这是概念骨架.

### 步骤3: WER

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

### 步骤4:推断与语

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

单线器为2026年最强的一般ASR. 运行在24GB的GPU上以20x实时.

> 2026年最强的通用ASR代码一行.

### 步骤5:使用Parakeet或 wav2vec 2.0 流媒体

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


流媒体ASR需要分片编码器注意和运输状态;使用支持它的库 (NeMo为Parakeet,`transformers`配合的管道`chunk_length_s`)

> 流式ASR 需要分块编码器注意力和转移状态;使用支持它的库`transformers`管道带`chunk_length_s`




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

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



## 陷在2026年仍存在

> 2026年仍在犯案陷中

- **No VAD.**语在沉默中产生幻觉 ("谢谢你观看!").
  **没有 VAD。**在静音上运行 语 会产生幻觉("谢谢你观看!")
- **Character vs word vs subword WER.**报告词级 WER *后*正常化 (小字母,切符符删除).
  **字符 vs 词 vs 子词 WER。**报告归归一化后 (小写、去标点) 的词级 WER。
- **Language ID drift.**声的自动LID误导噪音的视频到日本语或威尔士语;`language="en"`当你知道的时候.
  **语言识别漂移。**语的自动语言识别会把杂段误判为日语或威尔士语;已知语言时强制`language="en"`,我知道.
- **Long clips without chunking.**语有30秒的时间.`chunk_length_s=30, stride=5`任何更长时间.
  **长音频不分块。**微笑有30秒窗口.`chunk_length_s=30, stride=5`,我知道.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-asr-picker.md`选择模型,解码策略,分化和LM融合,

> 保存为`outputs/skill-asr-picker.md`◎为给定的部署目标选择模型、解码策略、分块和LM融合方案──

## 练习题

1. **Easy.**跑步`code/main.py`它贪地解读了手工制作的CTC输出,并将WER计算在参考中.
   **简单。**运行`code/main.py`△它对手工制作的CTC 输出进行贪解码并计算WER──
2. **Medium.**按照第2步的前树束搜索进行正确执行 (考虑空格合并规则).在10个合成数据集中,比较贪.
   **中等。**正确实现步骤 2 中的前树束搜索(考虑空白合并规则) ⋅在10个合成样本上与贪方法比较.
3. **Hard.**使用`whisper-large-v3-turbo`现在[LibriSpeech test-clean](https://www.openslr.org/12)计算第100次发言的WER.
   **困难。**在[LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`△计算前 100 条语音的 WER──与发表的数据比较──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)CTC文件.
  连接时序分类 CTC论文──
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711)RNN-T的报纸.
  通过RNN进行序列转换RNN-T论文──
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)2022年法典文件;2024年将扩展到v3轮机.
  拉德福德等 / OpenAI (2022). 语:大规模弱监督的鲁棒语音识别2022年经典论文;2024年 v3-turbo 扩展
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) 2026年开放ASR排名榜领导人.
  印度的新能源公司 (NVIDIA NeMoParakeet-TDT) 模型卡2026年开放ASR排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)25多个模型的现场基准.
  抱擁脸Open ASR 排行榜25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

