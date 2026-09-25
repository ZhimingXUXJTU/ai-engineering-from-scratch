# Ses Aktivitesini tespit ve dönüşüm  Silero, Cobra ve Flush Trick 语音活动检测与轮次切换

> Her ses ajansı iki karar üzerine yaşar veya ölür: kullanıcı şimdi konuşuyor mu, ve onlar bitti mi? VAD ilkine cevap verir. Dönüş algısı (VAD + sessizlik-sükûp + semantik uç noktası modeli) ikincine cevap verir. Yanlış yapın ve asistanınız ya kullanıcıları keser ya da asla susmaz.

> **【中文解读】**Her bir ses yardımcısının başarısı iki yargıdan asılıdır: user is currently in talking? user says completed? VAD(语音活动检测) cevap ilk,轮次检测(VAD+静音持续+语义终点模型) cevap ikinci.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

Sesli bir ajanın her 20 ms'lık bir bölümde yaptığı üç farklı karar:

> Ses yardımcısı her 20 ms ses bloklarında üç farklı yargı yapmalıdır:

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


1. **Is this frame speech?**- Biner, çerçeve başına.
   Çinçe Çevirim:  语音? VAD──二分类,逐判断──
2. **Has the user started a new utterance?** başlangıç algısı.
   Çinçe Çevirimi: user started a new发言吗?
3. **Has the user finished?** son yönlendirme (turn-end).
   Çinçe Çevirimi: user says完了?

Naif cevap (enerji eşiği) herhangi bir gürültüde başarısız olur  trafik, klavyeler, kalabalık böbürleri. 2026 cevabı: Silero VAD (açık, derin öğrenilen) + bir dönüş algılama modeli (semantik son işaretleme) + VAD kalibrli bir sessizlik sarhoşluğu.

> 朴素的答案(能量值) 任何噪音环境下都会失败交通声、键盘声、人群杂声──2026 yılının cevabı: Silero VAD(开源、深度学习) + 轮次检测模型(语义端点检测) + VAD 校准的静音持续等待──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### Üç katlı VAD kaskasası

> Üç sınıf VAD 级联架构

**Tier 1: energy gate.**En ucuz, -40 dBFS'de RMS eşiği, açık sessizlik filtreleri ama eşiğinden yüksek herhangi bir gürültü ateş eder.

> **第一层：能量门控。**En ucuz yöntem: RMS  değerini -40 dBFS olarak ayarlayabilir.

**Tier 2: Silero VAD**1M parametreleri. 6000+ dilde eğitilmiş. Tek bir CPU düğümünde 30 ms parçası başına ~ 1 ms'de çalışır. % 5 FPR'de % 87,7 TPR. Açık kaynak öntanımlı.

> **第二层：Silero VAD**(MIT  izin) ∼100.000 parametre ∼ 6000+ 种语言上训练──在单 CPU 线程上每30 ms块约1 ms 推理时间──5% FPR 下 TPR ∼87.7%──开源方案的默认选择──

**Tier 3: semantic turn detector.**LiveKit'in dönüş algılama modeli (2024-2026) veya kendi küçük sınıflandırıcınız. "Söz ortasında durmak" ile "dedikten sonra konuşmayı" ayırır.

> **第三层：语义轮次检测器。**LiveKit'in sıralama denetim modeli ((2024-2026) veya kendi kendini tanımlayan küçük sınıflar, "sözler arasında duraklama" ve "söyleme tamamlandı" olarak ayrılır.

### Ana parametreler ve öntanımlı özellikleri

> 关键参数 ve onun özelleştirilmiş değeri

- **Threshold.**Silero bir olasılık çıkarır; konuşmayı &gt; 0.5 (devay) veya &gt; 0.3 (hissli) olarak sınıflandırın.
  Çeviri:**阈值。**Silero 输出概率值;以 > 0.5(默认) veya > 0.3(敏感模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**250 ms' dan kısa konuşmayı reddet  genellikle öksürük veya sandalye gürültüsü.
  Çeviri:**最小语音时长。**拒绝短于250 ms 的语音通常是咳或椅子噪音──
- **Silence hangover (end-pointing).**VAD 0'ya döndükten sonra, dönüşün sonunu ilan etmeden önce 500-800 ms bekleyin. Çok kısa → keskin kullanıcı. Çok uzun → yavaş hissettiriyor.
  Çeviri:**静音持续等待（端点检测）。**VAD 0'e kadar geri dönün, 500-800 ms bekleyin.
- **Pre-roll buffer.**VAD ateşlemeden önce 300-500 ms ses tutun. "Hey" kesilmesini önler.
  Çeviri:**预滚缓冲。**Bu yüzden, "VAD" kelimesinin kesilmesini önlemek için 300-500 ms 音频──防止""字被截断──

### Flush numarası (Kyutai 2025)

Akış STT modelleri ileriye bakma gecikmesine sahiptir (Kyutai STT-1B için 500 ms, STT-2.6B için 2.5 saniye).**send a flush signal to the STT**STT gerçek zamanlı olarak 4× işlem yapar, bu yüzden 500 ms tampon yaklaşık 125 ms'de biter.

> 流式 STT 模型有前视延迟(Kyutai STT-1B 为 500 ms,STT-2.6B 为 2.5 s)  Genellikle ses bitince bu kadar uzun süre beklemek gerekir.**向 STT 发送刷新信号**, zorunlu anında çıkış ve STT yaklaşık 4 倍 gerçek zamanlı işlem hızı, bu yüzden 500 ms 缓冲区在约125 ms内完成──

Son-son: 125 ms VAD + flush STT = konuşma gecikmesi.

> 端到端:125 ms VAD + 刷新 STT = 对话级延迟──

### 2026 VAD karşılaştırması

> 2026 yıl VAD karşılığı

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero, doğru varsayımdır. Cobra, uyumluluk / doğruluk yükseltmesidir. Sadece enerjiye sahip VAD'ın 2026 üretiminde yeri yoktur.

> Silero doğru bir standart seçimdir. Cobra, 2026 yılındaki üretim ortamında sadece enerjiye dayalı bir VAD'ın yer almadığı bir aşama seçeneği.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.

> **【拓展：语音隐私与安全】**语音数据 contains a lot of personal privacy information (Sözleşme 对话 内容) ◦深度伪造 (Depfake) 语音技术 (Sözleşme 信息) 语音 数据 语音 数据 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语





## Yapın.
```figure
sp-vad-cascade
```

## Yapın

### Adım 1: Enerji kapısı

> 1 adım: Enerji kontrolü

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Adım 2: Silero VAD Python

> 步骤 2: Python'da Silero VAD kullan

```python
from silero_vad import load_silero_vad, get_speech_timestamps

vad = load_silero_vad()
audio = torch.tensor(waveform_16k, dtype=torch.float32)
segments = get_speech_timestamps(
    audio, vad, sampling_rate=16000,
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=500,
    speech_pad_ms=300,
)
for s in segments:
    print(f"{s['start']/16000:.2f}s - {s['end']/16000:.2f}s")
```

### Adım 3: Son dönüm devleti makinesi

> 步骤 3: döngü:

```python
class TurnDetector:
    def __init__(self, silence_hangover_ms=500, min_speech_ms=250):
        self.state = "idle"
        self.speech_ms = 0
        self.silence_ms = 0
        self.silence_hangover_ms = silence_hangover_ms
        self.min_speech_ms = min_speech_ms

    def update(self, is_speech, chunk_ms=20):
        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            if self.state == "idle" and self.speech_ms >= self.min_speech_ms:
                self.state = "speaking"
                return "START"
        else:
            self.silence_ms += chunk_ms
            if self.state == "speaking" and self.silence_ms >= self.silence_hangover_ms:
                self.state = "idle"
                self.speech_ms = 0
                return "END"
        return None
```

### Dördüncü adım: Fırıltılı bir sünger kemiri

> 步骤 4:刷新技巧框架代码

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


STT (Kyutai, Deepgram, AssemblyAI) bunun çalışması için flush desteği olmalıdır.

> STT(Kyutai、Deepgram、AssemblyAI) Flush'i desteklemek zorundadır bu teknikleri etkinleştirmek için.




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Baskır kural: başka bir seçeneğiniz yoksa asla enerjiye bağlı VAD'leri göndermeyin.

> 経験法: Gerçekten başka seçenek yoksa, asla sadece enerjiye dayalı VAD'e gitme.



## Tuzaklar

> 常见陷

- **Fixed threshold.**Sessiz çalışır, gürültülü çalışırken başarısız olur.
  Çeviri:**固定阈值。**Bu, bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir
- **Too-short silence hangover.**Ajan cümle ortasında keser. 500-800 ms konuşma için en iyi noktayı.
  Çeviri:**静音持续等待过短。**助手在句中打断用户──500-800 ms is the best range of dialog语音──
- **Too-long hangover.**Hedef kullanıcıları ile A/B testi.
  Çeviri:**静音持续等待过长。**感觉迟──与目标用户进行A/B 测试──
- **No pre-roll buffer.**İlk 200-300 ms kullanıcı sesini kaybettim.
  Çeviri:**没有预滚缓冲。**Uzucu ses频的前 200-300 ms 丢失──始终保持滚动预滚缓冲──
- **Ignoring semantic endpointing.**"Hmm, bırak düşünme"... uzun süreli molalar içerir. Kullanıcılar düşüncelerinin ortasında kesilmekten nefret eder.
  Çeviri:**忽略语义端点检测。**",让我想想......" uzun bir duraklama içerir.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-vad-tuner.md`- Bir iş yükü için VAD modeli, eşiği, sarhoşluğu, ön rol ve dönüş algılama stratejisini seçin.

> 保存为 `outputs/skill-vad-tuner.md`◊ VAD 模型、值、静音持续等待、预滚缓冲和轮次检测策略──

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Konuşma + sessizlik + konuşma + öksürük dizisini simüle eder ve üç VAD seviyesini test eder.
   Çeviri:**简单。**运行  İşlem`code/main.py`∼ It模拟一段语音 + 静音 + 语音 + 咳的序列,并测试三层 VAD──
2. **Medium.**Kurulum`silero-vad`, 5 dakikalık bir kayıt işleme, hem ilk kelime klipleri hem de yanlış tetikleyicileri en aza indirmek için ayarlama eşiği.
   Çeviri:**中等。**- Yapımcılık`silero-vad`, İşleme bir bölüm 5 dakika kayıt,  değerini en aza indirmek için ayarlama  değerini en azlandırmak için 
3. **Hard.**Mini dönüş algılayıcısı oluşturun: Silero VAD + son 10 kelimenin gömülmelerinde 3 katmanlı MLP (cümle dönüştürücülerini kullanın). El etiketli bir dönüş sonu veriler kümesi üzerinde çalışın. Sadece Silero'yu %10 F1 ile yenebilirsiniz.
   Çeviri:**困难。** Küçük bir sıralama denetleyicisi inşa edin: Silero VAD +  10 个近词嵌入的 3 层 MLP ️句变化器 (MLP) ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Silero VAD](https://github.com/snakers4/silero-vad) İpucu açık VAD.
  Silero VAD  Open Source Reference VAD 
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) Ticari doğruluk lideri.
  Picovoice Cobra VAD 商业精度领先者
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt)- Sub-200 ms mühendislik hilesi.
  KyutaiUnmute + 刷新技巧亚 200 ms 的工程技巧──
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) üretimdeki semantik son gösterme.
  LiveKit 轮次检测 生产中的语义端点检测。
- [WebRTC VAD](https://webrtc.googlesource.com/src/) miras alınan temel çizgi.
  WebRTC VAD tradi基线──
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) Günlükleştirme derecesi segmentasyonu.
  pyannote bölünmesi说话人日志级别的分分──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

