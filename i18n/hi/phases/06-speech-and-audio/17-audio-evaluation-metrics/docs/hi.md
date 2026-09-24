# ऑडियो मूल्यांकन  WER, MOS, UTMOS, MMAU, FAD, और ओपन लीडरबोर्ड्स  音频评估指标

> आप जो नहीं माप सकते हैं उसे भेज नहीं सकते। इस पाठ में प्रत्येक ऑडियो कार्य के लिए 2026 मीट्रिक का नाम दिया गया हैः एएसआर (WER, सीईआर, आरटीएफएक्स), टीटीएस (एमओएस, यूटीएमओएस, एसईसीएस, WER-ऑन-एएसआर-राउंड-ट्रिप), ऑडियो-भाषा (एमएमएयू, लॉन्ग ऑडियोबेंच), संगीत (एफएडी, सीएलएपी), और स्पीकर (ईईआर) । साथ ही आप तुलना करने वाले रैंकिंगबोर्ड।

> **【中文解读】**无法量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER(词错率) ✓TTS 用 MOS(平均意见分) ✓音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Word Error Rate,词错率) = (替换+删除+插入) / 总词数──Whisper Large v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## समस्या  समस्या परिचय

प्रत्येक ऑडियो कार्य में कई मीट्रिक होते हैं, प्रत्येक एक अलग अक्ष को मापता है। गलत मीट्रिक का उपयोग करके आप एक मॉडल कैसे भेजते हैं जो आपके डैशबोर्ड पर बहुत अच्छा दिखता है और उत्पादन में भयानक है। 2026 की कैनोनिकल सूचीः

> प्रत्येक ऑडियो मिशन में कई मापदंड होते हैं, प्रत्येक मापदंड अलग-अलग आयामों को मापता है। गलत उपयोग के मापदंडों का उपयोग यह है कि कैसे एक मॉडल उपकरण पर अच्छा दिखता है लेकिन उत्पादन में खराब प्रदर्शन करता है।

> **【中文解读】**इस खंड में प्रश्न उठे हैं कि इस तकनीक को वास्तविक इंजीनियरिंग में सही ढंग से कैसे समझा जाए और लागू किया जाए।


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

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।


## अवधारणा का मूल अवधारणा

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### एएसआर मेट्रिक्स

> एएसआर  मूल्यांकन सूचक

**WER (Word Error Rate).** `(S + D + I) / N`. कम अक्षर, अंकन, अंकन से पहले संख्याओं को सामान्य करें.`jiwer`या OpenAI की `whisper_normalizer`. &lt;5% = मानव-समानता भाषण पढ़ना.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`या OpenAI की `whisper_normalizer` 5% से कम = 朗读语音的人类水平──

**CER (Character Error Rate).**एक ही सूत्र, वर्ण-स्तर। स्वर भाषाओं (मान्डारीन, कैंटोन) के लिए उपयोग किया जाता है जहां शब्द विभाजन अस्पष्ट है।

> **CER（字错率）。**समान सूत्र,字符级别──用于声调语言(普通话、语),因为词细分 不明──

**RTFx (inverse real-time factor).**ऑडियो सेकंड प्रति वॉल-क्लॉक सेकंड पर संसाधित. उच्च बेहतर है. पैराकीट-टीडीटी 3380x है. चुप्पी-बड़ी-v3 ~30x है.

> **RTFx（逆实时因子）。**प्रत्येक वास्तविक सेकंड का संसाधित करने का समय।

**First-token latency.**ऑडियो इनपुट से पहले ट्रांसक्रिप्ट टोकन तक दीवार घड़ी स्ट्रीमिंग के लिए महत्वपूर्ण है।

> **首 token 延迟。**से音频输入到第一转录符号的实际时间――流式处理至关重要――Deepgram Nova-3:约150 ms――

### टीटीएस माप

> टीटीएस  मूल्यांकन सूचक

**MOS (Mean Opinion Score).**1-5 मानव रेटिंग. स्वर्ण मानक लेकिन धीमा. प्रति नमूना 20+ श्रोताओं, प्रति मॉडल 100+ नमूने एकत्र.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢── प्रत्येक नमूना 20+ श्रोताओं, प्रत्येक मॉडल 100+ नमूने एकत्रित करते हैं──

**UTMOS (2022-2026).**सीखा MOS पूर्वानुमान. मानक बेंचमार्क पर मानव MOS के साथ ~0.9 के अनुरूप. F5-TTS: UTMOS 3.95; ग्राउंड सत्यः 4.08.

> **UTMOS（2022-2026）。**学习型 MOS 预测器──在标准基准上与人类 MOS 相关性约0.9──F5-TTS:UTMOS 3.95;真实值:4.08──

**SECS (Speaker Encoder Cosine Similarity).**आवाज क्लोनिंग के लिए. संदर्भ और क्लोन आउटपुट के बीच ECAPA कोसिन एम्बेडिंग. &gt; 0.75 = पहचान योग्य क्लोन.

> **SECS（说话人编码器余弦相似度）。**प्रयोग में प्रयोग किया जाता है语音克隆──参考音频和克隆输出之间的 ECAPA 嵌入余弦相似度──大于0.75 =可识别的克隆──

**WER-on-ASR-round-trip.**TTS आउटपुट पर Whisper चलाएं, इनपुट पाठ के साथ WER गणना करें. समझदारी की गिरावट पकड़ता है. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**TTS पर 输出运行 WER, गणना के सापेक्ष输入文本的 WER──捕获可理解度退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**वॉल क्लॉक लेटेन्स. कोकोरो-82एम: ~100 ms; F5-TTS: ~1 s.

> **TTFA（首个音频时间）。**实际延迟──कोकोरो-82M: लगभग 100 ms;F5-TTS: लगभग 1 सेकंड──

### आवाज क्लोनिंग-विशिष्ट

> 语音克隆专用标标志

**SECS + MOS + CER**एक उच्च एसईसीएस लेकिन कम एमओएस स्कोर का मतलब है कि टिमबर-राइट-लेकिन-अनैसर्गिक; विपरीत का मतलब है प्राकृतिक आवाज लेकिन गलत स्पीकर।

> **SECS + MOS + CER**作为三重指标──克隆分高SECS但低MOS का अर्थ है ध्वनि色正确但不自然;反之则 का अर्थ है ध्वनि自然但说话人不对──

### स्पीकर सत्यापन

> बोल बोलने वाले व्यक्ति सत्यापन संकेतक

**EER (Equal Error Rate).**वोक्ससेलेब1-ओ पर ECAPA: 0.87%.

> **EER（等错误率）。**错误接受率等于错误拒绝率的值──ECAPA 在 VoxCeleb1-O 上:0.87%──

**minDCF (min Detection Cost).**चयनित परिचालन बिंदु पर वजन की गई लागत (अक्सर FAR=0.01) जो EER की तुलना में उत्पादन से अधिक प्रासंगिक है।

> **minDCF（最小检测代价）。**EER से अधिक निकट उत्पादन की मांग में वृद्धि

### डायरीकरण

> 说话人日志指标

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. मिस स्पीच + फेक अलार्म स्पीच + स्पीकर-कन्फ्यूजन, प्रत्येक अंश के रूप में। एएमआई मीटिंग्सः डीईआर ~ 10-20% यथार्थवादी है। पियानोट 3.1 + प्रेसिजन-2 विज्ञापनः &lt;10% डीईआर अच्छी तरह से रिकॉर्ड किए गए ऑडियो पर।

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──pyannote 3.1 + सटीक-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**डीईआर के विकल्प, मजबूत से लघु खंड पूर्वाग्रह।

> **JER（Jaccard 错误率）。**DER के प्रतिस्थापन, लघु-अवस्था के लिए

### ऑडियो वर्गीकरण

> 音频分类指标

बहु-लेबलः **mAP (mean Average Precision)**सभी वर्गों पर। ऑडियोसेट: बीएटीएस-आईटीईआर3 के लिए 0.548 एमएपी।

> 多标签:**mAP（平均精度均值）**, कवर सभी वर्गों。ऑडियोसेट:BEATs-iter3 为 0.548 mAP。

बहु-वर्ग विशेष: **top-1, top-5 accuracy**. भाषण कमांड v2: 99.0% शीर्ष-1 (ऑडियो-MAE).

> दो प्रकार के परस्परः**top-1、top-5 准确率** भाषण कमांड v2:99.0% शीर्ष-1

असंतुलित: **macro F1**+ **per-class recall**. प्रति वर्ग रिपोर्ट  समग्र सटीकता छिपाता है कि कौन से वर्ग विफल होते हैं।

> असंतुलित डेटाः**macro F1**+ **每类召回率**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

### संगीत पीढ़ी

> 音乐生成指标

**FAD (Fréchet Audio Distance).**वास्तविक बनाम उत्पन्न ऑडियो के वीजीजीआईएसईएम एम्बेडेड वितरण के बीच दूरी। MusicGen-small on MusicCaps: 4.5. MusicLM: 4.0. कम बेहतर।

> **FAD（Fréchet 音频距离）。**वास्तविकता और उत्पादन ध्वनि के बीच की दूरी 嵌入分布间距──MusicGen-small 在 MusicCaps 上:4.5──MusicLM:4.0──越低越好──

**CLAP Score.**CLAP एम्बेडेड का उपयोग करके पाठ-ऑडियो संरेखण स्कोर। &gt; 0.3 = उचित संरेखण।

> **CLAP 分数。**CLAP 嵌入式文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**उपभोक्ता-ग्रेड संगीत के लिए अभी भी अंतिम शब्द। TTS एरेना पर Suno v5 ELO 1293 (मानव पसंद से जोड़ी) ।

> **听音评审团 MOS。**仍然是消费级音乐的最终评判标准──Suno v5  TTS Arena में ऊपरी ELO 为 1293

### ऑडियो भाषा बेंचमार्क

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10k ऑडियो-QA जोड़े.

> **MMAU（大规模多音频理解）。**10,000 से अधिक आवाजें

**MMAU-Pro.**1800 हार्ड आइटम, चार श्रेणियांः भाषण / ध्वनि / संगीत / मल्टी-ऑडियो। 4-वे पर 25% यादृच्छिक मौका। मिथुन 2.5 प्रो कुल ~ 60%; सभी मॉडल पर मल्टी-ऑडियो ~ 22%।

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%──

**LongAudioBench.**अर्थिक प्रश्नों के साथ मल्टी मिनट क्लिप। ऑडियो फ्लेमिंगो नेक्स्ट Gemini 2.5 प्रो से बेहतर है।

> **LongAudioBench。**शायद钟音频片段 + 语义查询──Audio Flamingo Next 超过双子 2.5 Pro──

**AudioCaps / Clotho.**संदर्भ मानकों का उपशीर्षक। SPICE, CIDER, FENSE मेट्रिक्स।

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### भाषण-भाषण स्ट्रीमिंग

> 流式语音到语音指标

**Latency P50 / P95 / P99.**उपयोगकर्ता के अंत-उपयोगकर्ता भाषण से पहली श्रव्य प्रतिक्रिया तक दीवार घड़ी।

> **延迟 P50 / P95 / P99。**उपयोगकर्ता आवाज समाप्त होने से पहले सुलभ प्रतिक्रिया के वास्तविक समय तक।

**WER / MOS**आउटपुट पर।

> आउटपुट पर **WER / MOS**

**Barge-in responsiveness.**उपयोगकर्ता के अंतराल से सहायक मूक तक समय। लक्ष्य &lt; 150 ms.

> **打断响应时间。**उपयोगकर्ता से उपयोगकर्ता के लिए समय का अंतराल से सहायक के लिए समय का अंतराल तक लक्ष्य 150 ms से कम है।

### 2026 के शीर्ष स्थान

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入大量工程优化解决这些长尾问题──实时性要求(<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**मेटा के एमएमएस मॉडल 1000 से अधिक भाषाओं के लिए समर्थन करते हैं।




## इसे बनाओ, इसे पूरा करो।
```figure
sp-wer-align
```

## इसे बनाओ

### चरण 1: सामान्यीकरण के साथ WER

> 步骤 1: मानक WER के साथ

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

### चरण 2: टीटीएस वापसी-यात्रा WER

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

### चरण 3: आवाज क्लोनिंग के लिए SECS

> 步骤 3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### चरण 4: संगीत पीढ़ी के लिए FAD

> 步骤 4: संगीत उत्पन्न की FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### चरण 5: स्पीकर सत्यापन के लिए ईईआर (लक्ष्य 6) के समान कोड

> 步骤 5: 话语人验证 के EER(第六课与相同的代码)

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

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।





> **【拓展：语音与情感计算】**语音 न केवल पाठ सूचना को प्रसारित करता है, बल्कि यह भी समृद्ध भावनात्मक संकेतों को भी ले जाता है। 语调、语速、音高变化)  भावनात्मक भाषा पहचान, भाषण भावना मान्यता, SER) का व्यापक रूप से ग्राहक गुणवत्ता जांच, मानसिक स्वास्थ्य निगरानी, बुद्धिमान शिक्षा आदि के क्षेत्र में उपयोग किया जाता है।

## इसे फ्रेमवर्क के साथ लागू करें

प्रत्येक तैनाती को एक निश्चित मूल्यांकन हर्नस के साथ जोड़ा जो प्रत्येक मॉडल अपडेट पर चलता है। तीन मुख्य नियमः

> प्रत्येक तैनाती में एक निश्चित मूल्यांकन उपकरण होता है, प्रत्येक मॉडल अपडेट के दौरान चल रहा है।

1. **Normalize before scoring.**लघु अक्षर, अंकन पट्टी, संख्या विस्तार। सामान्यीकरण नियम रिपोर्ट।
   中文翻译:**评分前标准化。**转小写、去标点、数字展开―― रिपोर्ट मानकीकरण नियम――
2. **Report distributions, not averages.**विलंबता के लिए P50/P95/P99। वर्गीकरण के लिए प्रति वर्ग याद। MMAU के लिए प्रति श्रेणी।
   中文翻译:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**यहां तक कि अगर आपके उत्पादन डेटा अलग-अलग हैं, तो ओपन एएसआर / टीटीएस एरेना / एमएमएयू पर रिपोर्टिंग करने से समीक्षकों को सेब-से-सेब की तुलना करने की अनुमति मिलती है।
   中文翻译:**运行一个权威公共基准。**यहां तक कि आपके उत्पादन डेटा में अंतर भी है, ओपन एएसआर / टीटीएस एरेना / एमएमएयू में रिपोर्ट करने से समीक्षक को उचित तुलना करने में मदद मिल सकती है।



## फंदे

> 常见陷

- **UTMOS extrapolation.**वीसीटीके शैली में स्वच्छ भाषण पर प्रशिक्षित; शोर / क्लोन / भावनात्मक ऑडियो खराब स्कोर करता है।
  中文翻译:**UTMOS 外推问题。**VCTK 风格 के शुद्ध语音 पर प्रशिक्षण;对杂/克隆/情感语音评分效果差──
- **MOS panel bias.**20 अमेज़ॅन मैकेनिकल टर्क कर्मचारी ≠ 20 लक्षित उपयोगकर्ता। यदि दांव उच्च हैं तो डोमेन पैनल के लिए भुगतान करें।
  中文翻译:**MOS 评审团偏差。**20 个亚马逊机械 Turk 工作者不等于 20 个目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**मॉडल के बीच समान संदर्भ वितरण के साथ तुलना करें।
  中文翻译:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**5% कुल मिलाकर, उच्चारण वाले भाषण पर 30% WER छिपा सकते हैं। जनसांख्यिकीय स्लाइस द्वारा रिपोर्ट करें।
  中文翻译:**汇总 WER。** कुल 5% की WER को कवर किया जा सकता है  30% की WER को कवर किया जा सकता है 
- **Public benchmark saturation.**अधिकांश सीमा मॉडल मानक बेंचमार्क पर छत के पास हैं। एक घर में रखा सेट बनाएं जो आपके ट्रैफ़िक को प्रतिबिंबित करता है।
  中文翻译:**公共基准饱和。**अधिकांश अग्रिम मॉडल मानक आधार पर तियनिबोर्ड के करीब आ चुके हैं।

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।


## इसे भेजें उत्पाद

`outputs/skill-audio-evaluator.md`किसी भी ऑडियो मॉडल रिलीज के लिए मेट्रिक्स, बेंचमार्क और रिपोर्टिंग प्रारूप चुनें।

> 保存为 `outputs/skill-audio-evaluator.md` किसी भी ध्वनि मॉडल के लिए चयन सूचकांक, आधार और रिपोर्ट प्रारूप जारी करना

## अभ्यास विषय

1. **Easy.**दौड़ें`code/main.py`खेल के इनपुट पर WER / CER / EER / SECS / FAD-ish / MMAU-ish की गणना करें।
   中文翻译:**简单。**运行 `code/main.py`在玩具输入上计算 WER / CER / EER / SECS / 类 FAD / 类 MMAU
2. **Medium.**एक TTS रिंगट्रिप WER हर्नर बनाएं. अपने Kokoro या F5-TTS आउटपुट को Whisper के माध्यम से चलाएं. 50 से अधिक संकेतों के साथ WER की गणना करें. 10% WER के साथ ध्वज संकेत।
   中文翻译:**中等。**构建 TTS 回环 WER 评估工具──用 Whisper 处理你的Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10%的提示──
3. **Hard.**एमएमएयू-प्रो भाषण + बहु-ऑडियो उपसमूहों (प्रत्येक 50 वस्तुओं) पर अपने पाठ 10 LALM विकल्प को स्कोर करें। प्रति श्रेणी सटीकता की रिपोर्ट करें और प्रकाशित संख्या के साथ तुलना करें।
   中文翻译:**困难。**MMAU-Pro के भाषा + 多音频子集上 (各 50 项) आपके 10 课选择的 LALM- का मूल्यांकन करें। प्रति वर्ग सटीकता दर तथा प्रकाशित डेटा के मुकाबले रिपोर्ट करें।

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## कीवर्ड्स  शब्द खोज तालिका

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

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।


## आगे पढ़ना 延伸閱讀

- [jiwer](https://github.com/jitsi/jiwer) सामान्यीकरण उपयोगिताओं के साथ WER/CER पुस्तकालय।
  WER/CER 库
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) सीखा MOS पूर्वानुमान।
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器──
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) संगीत-जन मानक।
  फ्रेचेट ऑडियो दूरी(किल्गुर 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 2026 लाइव रैंकिंग।
  ओपन एएसआर 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) मानव-मतों के साथ टीटीएस की रैंकिंग।
  TTS Arena人类投票的 TTS 排行榜──
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) LALM तर्क तालिका।
  एमएमएयू-प्रो 基准LALM 推理排行榜
- [HEAR benchmark](https://hearbenchmark.com/) ऑडियो एसएसएल बेंचमार्क।
  HEAR 基准音频 SSL 评估基准──

> **【中文解读】**延伸阅读 ने गहन शिक्षा के लिए उच्च गुणवत्ता वाले संसाधन प्रदान किए, जिसमें निबंध, शिक्षण और उपकरण शामिल हैं।

