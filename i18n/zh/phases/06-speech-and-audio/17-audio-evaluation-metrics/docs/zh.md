# 音频评价指标: 音频评价指标:

> 您不能运送您无法测量的东西.本课程列出了每个音频任务的2026个指标:ASR (WER, CER,RTFx),TTS (MOS,UTMOS,SECS,WER-on-ASR-round-trip),音频语言 (MMAU,LongAudioBench),音乐 (FAD,CLAP),音箱 (EER).

> **【中文解读】**无法量度就无法交付――本课列出2026年所有音频任务的评估指标:ASR 用WER(词错率)、TTS 用MOS(平均意见分)、音频语言模型用MMAU、音乐用FAD、说话人识别用EER──还有对比排行榜――

> **【拓展：WER 是语音识别的黄金指标】**词错率 (Word Error Rate,词错率) = (替换+删除+插入) / 总词数――语大v3 在英文上达到~5% WER,接近人类水平――中文用 CER(字错率) ――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## 问题 问题引入

每个音频任务都有多个指标,每个指标都测量不同的轴.使用错误的指标是如何运送一个模型,看起来很好在仪表板上,而且生产非常糟糕.2026年经典列表:

> 每个音频任务都有多种指标,每个指标衡量不同的维度.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


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

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


## 概念的核心概念

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### 标准标准

> 评估指标

**WER (Word Error Rate).** `(S + D + I) / N`低文字,脱离分区,在得分之前正常化数字.`jiwer`或是OpenAI的`whisper_normalizer`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`评分前需转小写、除标点、标准化数字──使用 `jiwer`或开放AI 的`whisper_normalizer`△低于5% = 朗读语音的人类水平.

**CER (Character Error Rate).**语音语言 (曼德林,堪敦语) 使用的语音语言,语音分类不明确.

> **CER（字错率）。**相同公式,字符级别──用于声调语言(普通话、语),因为词分类不明确──

**RTFx (inverse real-time factor).**音频秒钟是每秒钟的处理. 较高更好. 子-TDT 达到3380×. 声-大-v3 达到30×.

> **RTFx（逆实时因子）。**每实际秒处理的音频秒数――越高越好――鱼-TDT 达到3380×――语-大v3约30×――

**First-token latency.**视频传输到转录代币的墙钟.

> **首 token 延迟。**从音频输入到第一个转录代币的实际时间――对流式处理至关重要――Deepgram Nova-3:约150 ms――

### 标准标准

> 评价指标

**MOS (Mean Opinion Score).**测量量1-5人,金标准,但速度慢. 每个样本收藏20多名听者,每个模型收藏100多个样本.

> **MOS（平均意见分）。**黄金标准但速度慢. 每个样本收集20+听者,每一个模型100+样本.

**UTMOS (2022-2026).**已学习的MOS预测器.与标准基准的人类MOS相对应.F5-TTS:UTMOS3.95;基础真相:4.08.

> **UTMOS（2022-2026）。**学习型MOS 预测器──在标准基准上与人类MOS 相关性约0.9──F5-TTS:UTMOS 3.95;真实值:4.08──

**SECS (Speaker Encoder Cosine Similarity).**对于语音克隆.ECAPA 嵌入引用和克隆输出之间的共数. &gt; 0.75 =可识别的克隆.

> **SECS（说话人编码器余弦相似度）。**用于语音克隆──参考音频和克隆输出之间的ECAPA 嵌入余弦相似度──大于0.75 =可识别的克隆──

**WER-on-ASR-round-trip.**运行Whisper在TTS输出上,计算WER与输入文本.捕获可理解性回归. 2026 SOTA: &lt;2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**对TTS 输出运行 微笑,计算对输入文本的 WER──捕获可理解度退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**长时间: 长时间: 短时间: 短时间: 短时间:

> **TTFA（首个音频时间）。**实际延迟──科科罗-82M:约100ms;F5-TTS:约1秒──

### 语音克隆特定

> 语音克隆专用标签

**SECS + MOS + CER**克隆中高SECS但低MOS的意思是对音调,但不自然;相反的意思是自然的声音,但错误的扬声器.

> **SECS + MOS + CER**作为三重指标──克隆分高SECS但低MOS意味着音色正确但不自然;反之则意味着声音自然但说话人不对──

### 扬声器验证

> 说话人验证指标

**EER (Equal Error Rate).**假接受率等于假拒绝率的门值.

> **EER（等错误率）。**错误接受率等于错误拒绝率的值.

**minDCF (min Detection Cost).**在选择的运营点中,重量成本 (通常是FAR=0.01).

> **minDCF（最小检测代价）。**在选定工作点 (通常是FAR=0.01) 的加权代价.

### 腹化

> 说话人日志指标

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`错失语音+假报警语音+扬声器混,每一个是小部分. AMI会议:DER ~10-20%是现实的. pyannote 3.1 +精确-2广告: &lt;10%DER在记录良好音频.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◎ 漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──钢琴注 3.1 +精确-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**替代DER,强到短段偏见.

> **JER（Jaccard 错误率）。**对于短段偏差更为鲁棒.

### 音频分类

> 音频分类标志

多标签: **mAP (mean Average Precision)**音频组:BETs-iter3的 0.548mAP

> 多标签:**mAP（平均精度均值）**覆盖所有类别──音频组:BEATs-iter3 为 0.548mAP──

多类独家: **top-1, top-5 accuracy**语音指令v2: 99.0% 顶-1 (音频-MAE).

> 多类互斥:**top-1、top-5 准确率**◎语音命令 v2:99.0% 顶-1

失衡:**macro F1**其他**per-class recall**报告每类 总准确性隐藏了哪些类失败.

> 不平衡数据:**macro F1**其他**每类召回率**△按类别报告汇总准确率将掩盖哪些类别失败.

### 音乐产生的

> 音乐生成指标

**FAD (Fréchet Audio Distance).**视频集成直播器与生成音频之间的距离. MusicGen-small on MusicCaps:4.5. MusicLM:4.0.更低.

> **FAD（Fréchet 音频距离）。**音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐 音乐

**CLAP Score.**通过CLAP嵌入式的文字音频配列分数.

> **CLAP 分数。**使用CLAP 嵌入式文本音频对齐分数――大于0.3 = 合理对齐――

**Listening panel MOS.**对于消费者级音乐,Suno v5 ELO 1293在TTS Arena (来自人类对配的偏好).

> **听音评审团 MOS。**仍然是消费级音乐的最终评判标准.

### 音频语言基准指标

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**十万个音频QA对.

> **MMAU（大规模多音频理解）。**十万个频道.

**MMAU-Pro.**1,800个硬件,四类:语音/声音/音乐/多音频. 随机机会25%在四方向. 双子 2.5 专用总体约60%; 多音频约22%在所有车型上.

> **MMAU-Pro。**1,800个难题,四个类别:语音/声音/音乐/多音频──4 选1随机猜测 25%──Gemini 2.5 Pro整体约60%;所有模型在多音频上约22%.──

**LongAudioBench.**音频Flamingo下一个比双子 2.5Pro更好.

> **LongAudioBench。**听力 火 接下来 超过双子 2.5 专业.

**AudioCaps / Clotho.**标题标签:SPICE,CIDER,FENSE指标

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### 流通语音

> 流式语音到语音指标

**Latency P50 / P95 / P99.**截止用户语音到首次听到的响应.

> **延迟 P50 / P95 / P99。**从用户语音结束到首个可听响应的实际时间──莫希:200 ms;GPT-4o 实时:300 ms──

**WER / MOS**在输出.

> 输出上的**WER / MOS**,我知道.

**Barge-in responsiveness.**时间从用户中断到助理.目标&lt;150ms.

> **打断响应时间。**从用户打断到助手静音的时间――目标低于150ms――

### 2026 年的排名榜

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――




## 建立它,实现它.
```figure
sp-wer-align
```

## 建立它

### 步骤1:WER与正常化

> 步骤1:带标准化WER

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

### 步骤2:TTS回路 WER

> 步骤 2:TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### 步骤3:语音克隆的SECS

> 步骤3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### 步骤4:音乐生成的FAD

> 步骤 4:音乐生成的FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### 步骤5:语音者验证的EER (与第6课相同的代码)

> 步骤5:说话人验证的EER(与第六课相同的代码)

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

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

通过每一个模型更新都运行的固定评估带来了每一个部署.

> 每次部署都配备一个固定的评估工具,在每次模型更新时运行.

1. **Normalize before scoring.**简字,点击条,数字扩大,报告规则.
   翻译: 中文**评分前标准化。**转小写、去标点、数字展开――报告标准化规则――
2. **Report distributions, not averages.**对于延迟,P50/P95/P99 类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类别回忆,类型回忆,类型回忆,类型回忆,类型回忆,类型回忆,类型等等.
   翻译: 中文**报告分布而非均值。**延迟使用P50/P95/P99──分类用每类召回率──MMAU 用每类──
3. **Run one canonical public benchmark.**即使您的生产数据不同, 报告在开放ASR/TTS Arena/MMAU让评论员比较果与果.
   翻译: 中文**运行一个权威公共基准。**即使你的生产数据不同, 在开放的ASR/TTS竞技场/MMAU上报可以让评审员做公平比较.



## 陷

> 常见陷

- **UTMOS extrapolation.**训练于VCTK风格的清洁演讲; 评分噪音/克隆/情感音频差.
  翻译: 中文**UTMOS 外推问题。**在VCTK风格的纯净语音上训练;对杂/克隆/情感语音评分效果差异.
- **MOS panel bias.**亚马逊机械土耳其员工的目标用户为20名.
  翻译: 中文**MOS 评审团偏差。**工作者不等于20个目标用户.
- **FAD depends on reference set.**较量模型中的参考分布相同.
  翻译: 中文**FAD 依赖参考集。**跨模型比较时使用相同的参考分布.
- **Aggregate WER.**总体上5%的WER可以隐藏30%的WER在强调的语音.
  翻译: 中文**汇总 WER。**总体5%的WER可能掩盖带口音语音30%的WER──根据人口统计分组报告──
- **Public benchmark saturation.**根据标准标准,大多数线路车型都接近天花板.
  翻译: 中文**公共基准饱和。**大多数前沿模型在标准基准上已经接近天花板――构建反映了你真正流量的内部留出集――

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-audio-evaluator.md`选择任何音频模型发布的指标,基准和报告格式.

> 保存为`outputs/skill-audio-evaluator.md`△任何音频模型发布选择标志,基准和报告格式.

## 练习题

1. **Easy.**跑步`code/main.py`计算玩具输入的 WER / CER / EER / SECS / FAD-ish / MMAU-ish.
   翻译: 中文**简单。**运行`code/main.py`△ 在玩具输入上计算WER / CER / EER / SECS / 类 FAD / 类 MMAU。
2. **Medium.**建立一个TTS回路WER带.通过Whisper运行你的Kokoro或F5-TTS输出.计算WER超过50个提示.旗提示WER&gt; 10%.
   翻译: 中文**中等。**构建TTS 回环 WER 评估工具──用Whisper 处理你的Kokoro或F5-TTS 输出──在50个提示上计算WER──标记WER大于10%的提示──
3. **Hard.**评分您的10课 LALM选择在MMAU-Pro语音+多音频子组 (每个组分为50个). 报告每类别的准确性,并与公布的数字进行比较.
   翻译: 中文**困难。**在 MMAU-Pro 的语音+多音频子集上 (各50项) 评估您第10课选择的 LALM──报告每类准确率并与发表数据相比──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [jiwer](https://github.com/jitsi/jiwer) WER/CER库,具有正常化工具.
  更多的标准化工具的WER/CER库
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152)学习了MOS预测器.
  学习型MOS预测器──
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466)音乐世代标准.
  音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)2026年现场排名.
  开放的ASR排行榜2026实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena)人投票的TTS排名榜.
  广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台 广播电视台
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) LALM推理排名榜
  基准LALM 推理排行榜
- [HEAR benchmark](https://hearbenchmark.com/)音频SSL基准.
  听力基准音频 SSL 评估基准

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

