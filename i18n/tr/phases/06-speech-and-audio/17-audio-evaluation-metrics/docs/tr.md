# Ses Değerlendirme  WER, MOS, UTMOS, MMAU, FAD ve Açık Lider Tabloları

> Ölçemeyeceğiniz şeyi gönderemezsiniz. Bu ders her ses görevi için 2026 metrikleri belirler: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), ses dili (MMAU, LongAudioBench), müzik (FAD, CLAP) ve hoparlör (EER).

> **【中文解读】**无法量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER(词错率) ✓ TTS 用 MOS(平均意见分) ✓音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Köz Hata Sınıfı,词错率) = (替换+删除+插入) / 总词数──Whisper Büyük v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## Sorunlar. Sorunlar.

Her ses görevinin farklı bir ekseni ölçen birden fazla metrik vardır. Yanlış metrik kullanmak, arabasında harika görünen ve üründe korkunç bir model göndermek demektir. 2026 Kanonik listesi:

> Her ses görevinde farklı boyutları ölçen çeşitli göstergelere sahiptir. Yanlış kullanımı göstergeleri, bir cihaz üzerinde harika görünen ama üretim sırasında kötü performans gösteren bir modelin nasıl kullanıldığını gösterir.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


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

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


## Konsepten bir şey.

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### ASR ölçümleri

> ASR 评估指标

**WER (Word Error Rate).** `(S + D + I) / N`Küçük harflerle, çizim çizimleriyle, puan almadan önce sayıları normalleştir.`jiwer`veya OpenAI'nin `whisper_normalizer`. &lt;% 5 = insan eşitliği konuşma okuyucu.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`Ya da OpenAI'nın`whisper_normalizer`❖ % 5'ten az = 朗读语音的人类水平──

**CER (Character Error Rate).**Aynı formül, karakter seviyesinde. Sözcük bölünmesi belirsiz olan ses dillerinde (Mandarin, Kanton) kullanılır.

> **CER（字错率）。**Aynı formül,字符级别──用于声调语言(普通话、语),因为词分割 不明──

**RTFx (inverse real-time factor).**Ses saniyeleri, duvar saati saniyesine göre işlenir. Daha yüksek daha iyidir. Parakeet-TDT 3380×'ye ulaşır.

> **RTFx（逆实时因子）。**Her gerçek saniyede işlenir.

**First-token latency.**Ses girişinden ilk transkript tokenine kadar duvar saati.

> **首 token 延迟。**Sonraki videolar: 04.00'da, 04.00'da, 04.00'da, 04.00'da, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 04.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00 ve 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00'de, 06.00

### TTS ölçütleri

> TTS 评估指标

**MOS (Mean Opinion Score).**1-5 insan derecesi. Altın standart ama yavaş.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢──每个样本收集20+听者,每个模型100+样本──

**UTMOS (2022-2026).**Öğrenilmiş MOS tahmincisi. ~ 0.9 ile insan MOS'u standart referans değerlerinde ilişkilendiriyor. F5-TTS: UTMOS 3.95; temel gerçeklik: 4.08.

> **UTMOS（2022-2026）。**Önemli bir bilgi kaynağı olan MOS 预测器.

**SECS (Speaker Encoder Cosine Similarity).**Ses klonlaması için. ECAPA referans ve klon edilmiş çıkış arasında cosine yerleştirme. &gt; 0.75 = tanınabilir klon.

> **SECS（说话人编码器余弦相似度）。**Kullanılan sesler arasında ECAPA 嵌入余弦相似度──大于0.75 = 可识别的克隆──

**WER-on-ASR-round-trip.**TTS çıkışında Whisper çalıştırın, girilen metne karşı WER hesaplayın. Anlaşılabilirlik gerilemeleri yakalar. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**TTS için 输出运行 Whisper,计算对输入文本的 WER──捕获可理解退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**Kokoro-82M: ~100 ms; F5-TTS: ~ 1 saniye.

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: yaklaşık 100 ms; F5-TTS: yaklaşık 1 saniye──

### Ses klonlaması için özel

> 语音克隆专用标志

**SECS + MOS + CER**Yüksek SECS, düşük MOS puanı veren klonlama, tam anlamıyla doğru ama doğal olmayan bir timbre anlamına gelir.

> **SECS + MOS + CER**作为三重指标──克隆分高SECS但低MOS anlamı: 音色正确但不自然;反之则 anlamı: 音色自然但说话人不对──

### Konuşmacı doğrulama

> Konuşmak için bir kişilik göstergesi

**EER (Equal Error Rate).**Yalancı kabul oranının yanlış reddedilme oranının eşit olduğu eşiği.

> **EER（等错误率）。**误接受率等于误拒率的值──ECAPA 在 VoxCeleb1-O 上:0.87%──

**minDCF (min Detection Cost).**Seçilen bir işletme noktasında ağırlıklı maliyet (genellikle FAR=0,01).

> **minDCF（最小检测代价）。**Bu nedenle, bu durumun daha da yaygın olduğu bir durumdur.

### Diaryizasyon

> Konuşmak için

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Kaybolan konuşma + yanlış alarm konuşması + hoparlör-kafası, her biri bir bölüm olarak. AMI toplantıları: DER ~ 10-20% gerçekçi. pyannote 3.1 + Precision-2 reklam: &lt;10% DER iyi kaydedilen ses.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──pianonote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**DER'e alternatif, kısa segmentli kısıtlama için sağlam.

> **JER（Jaccard 错误率）。**DER'in alternatif programı, kısa bölümlerde daha fazla farkı vardır.

### Ses sınıflandırması

> 音频分类标志

Çok etiketli: **mAP (mean Average Precision)**Tüm sınıflar için.

> Çok fazla etiket:**mAP（平均精度均值）**, cover all categories──AudioSet:BEATs-iter3 为 0.548 mAP──

Çok sınıflı özel: **top-1, top-5 accuracy**Konuşma Komutları v2: 99.0% top-1 (Audio-MAE).

> Birbirine çok farklı.**top-1、top-5 准确率**❖ Konuşma Komutları v2:99.0% top-1

Denge eksikliği: **macro F1**+ **per-class recall**.Sınıf başına rapor  Toplam doğruluk hangi sınıfların başarısız olduğunu gizler.

> Düzsel olmayan veriler:**macro F1**+ **每类召回率**❖ Klas raporlarına göre hangi sınıfların başarısız olduğunu örtbas edecek ❖

### Müzik jenerasyonu

> 音乐生成指标

**FAD (Fréchet Audio Distance).**VGGish içeren gerçek vs. üretilen ses dağıtımları arasındaki mesafe. MusicGen MusicCaps üzerinde küçük: 4.5. MusicLM: 4.0. Daha düşük daha iyi.

> **FAD（Fréchet 音频距离）。**Gerçek ve üretim ses frekansı arasındaki mesafe 嵌入分布间距──MusicGen-small 在 MusicCaps 上:4.5──MusicLM:4.0──越低越好──

**CLAP Score.**CLAP gömülmelerini kullanarak metin-audio uyum puanı. &gt; 0.3 = makul uyum.

> **CLAP 分数。**CLAP kullan 嵌入式文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**TTS Arena'da Suno v5 ELO 1293 (insan tercihlerinden)

> **听音评审团 MOS。**Suno v5 TTS Arena'da 1293'e yükseldi.

### Sesli dil referansları

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10 bin sesli-QA çift.

> **MMAU（大规模多音频理解）。**10.000 sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesliğine sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesliğine sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesliğine

**MMAU-Pro.**1800 sert öğe, dört kategori: konuşma / ses / müzik / çok sesli. Rastgele şans 25% dört yönlü. Gemini 2.5 Pro genel olarak ~ 60%; çok sesli tüm modellerde ~ 22% .

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%──

**LongAudioBench.**Semantik sorularla birlikte birkaç dakikalık klipler.

> **LongAudioBench。**Belki de saatler boyunca sesli konuşmalar yaparak.

**AudioCaps / Clotho.**SPICE, CIDER, FENSE ölçümleri.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### Konuşma-söz akışı

> 流式语音到语音标志

**Latency P50 / P95 / P99.**Kullanıcının konuşma sonundan ilk sesli tepkiye kadar duvar saati.

> **延迟 P50 / P95 / P99。**Kullanıcı ses bitmesi ile ilk duyulabilir tepki gerçek zamanına kadar.

**WER / MOS**Çıktı.

>  输出上 **WER / MOS**- Evet.

**Barge-in responsiveness.**Kullanıcı kesintiden asistan sessizliğe kadar.

> **打断响应时间。**Kullanıcı kesintisi ile yardımcı sesli sesli zamanından. Hedef 150 ms'ten aşağıdır.

### 2026 liderlik tabloları

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.




## Yapın.
```figure
sp-wer-align
```

## Yapın

### Adım 1: Normalleşme ile WER

> 步骤 1: standartlaştırılmış WER ile

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

### Adım 2: TTS geri dönüş WER

> 步骤 2: TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Adım 3: Ses klonlaması için SECS

> 步骤 3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Adım 4: Müzik jenerasyonu için FAD

> 4 adım: FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Adım 5: Konuşmacıların doğrulanması için EER (Disim 6)

> 5 adım: 话人验证的 EER(第 6 课与相同的代码)

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

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

Her dağıtımın her model güncelleme sırasında çalışacak sabit bir değerlendirme harnesine eşleştirilmesini sağlayın.

> Her bir dağıtım, her bir model güncelleştirilmesinde çalışmaya devam eden, belirli bir değerlendirme aracıyla birlikte yapılır.

1. **Normalize before scoring.**Küçük harf, nokta çizgisi, sayı genişle.
   Çeviri:**评分前标准化。**转小写、去标点、数字展开―― rapor standartlaştırma kuralları―
2. **Report distributions, not averages.**P50/P95/P99 gecikme için. Sınıf başına geri çağırma sınıflandırma için. MMAU için kategori başına.
   Çeviri:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**Üretim verileriniz farklı olsa bile, Open ASR / TTS Arena / MMAU'da raporlar, inceleyicilerin elma ile elma arasında bir kıyaslama yapmasına izin verir.
   Çeviri:**运行一个权威公共基准。**Üretim verileriniz farklı olsa bile, Open ASR / TTS Arena / MMAU'da raporlar, değerlendirmeciler için adil bir karşılaştırma yapmalarını sağlayabilir.



## Tuzaklar

> 常见陷

- **UTMOS extrapolation.**VCTK tarzı temiz konuşma konusunda eğitilmiş; gürültülü / klonlanmış / duygusal sesleri kötü puanlar.
  Çeviri:**UTMOS 外推问题。**VCTK 风格的纯净语音上训练;对杂/克隆/情感语音评分效果差──
- **MOS panel bias.**20 Amazon Mechanical Turk çalışanı ≠ 20 hedef kullanıcı.
  Çeviri:**MOS 评审团偏差。**20 Amazon Mechanical Turk 工作者不等于 20 目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**Modeller arasında aynı referans dağılımına karşılaştırın.
  Çeviri:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**Toplam %5 REM'de, aksanlı konuşmalarda %30 REM'i gizleyebilir.
  Çeviri:**汇总 WER。**整体 5% WER                                                                                                                                                                                                                                                            
- **Public benchmark saturation.**Çoğu sınır modeli standart standart standartlarda tavanın yakınında. Trafikinizi yansıtan bir ev içi bir tutunma seti yapın.
  Çeviri:**公共基准饱和。**Çoğu önde gelen model standart taban üzerinde bir kenara yaklaştı.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-audio-evaluator.md`. Her ses modelinin yayını için ölçümleri, referansları ve raporlama biçimini seçin.

> 保存为 `outputs/skill-audio-evaluator.md`◊ herhangi bir sesli model için seçme göstergesi, temel ve rapor biçimi yayınlamak

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Oyuncak girişleri üzerinde WER / CER / EER / SECS / FAD-ish / MMAU-ish hesaplayın.
   Çeviri:**简单。**运行  İşlem`code/main.py` Oyuncuların sayısı: WER / CER / EER / SECS / FAD / MMAU
2. **Medium.**TTS dönüş WER harnesini yapın. Kokoro veya F5-TTS çıkışınızı Whisper üzerinden çalıştırın. WER'i 50'den fazla ipucu hesaplayın. Bayrak ipucuları WER &gt; % 10 ile.
   Çeviri:**中等。**构建 TTS 回环 WER 评估工具──用 Whisper 处理你的Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10% 的提示──
3. **Hard.**Ders 10 LALM seçeneğini MMAU-Pro konuşma + çoklu ses alt kümeleri üzerinde değerlendirin (her biri 50 madde).
   Çeviri:**困难。**MMAU-Pro'nun ses + 多音频子集上 (50 bölümden) değerlendirmek için, sınıfların doğrulaması oranını rapor etmek ve yayınlama verileri karşılaştırmak.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

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

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [jiwer](https://github.com/jitsi/jiwer) Normalleşme araçları ile WER/CER kütüphanesi.
  带标准化工具的 WER/CER库
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) MOS tahmincisi öğrendi.
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) Müzik-gen standardı.
  Fréchet Audio Distance(Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)2026 canlı sıralamaları.
  Açık ASR 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) İnsan oyları TTS lider listesinde.
  TTS Arena İnsanların Oylamaları TTS 排行榜──
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) LALM akıl yürütme lider tablosu.
  MMAU-Pro 基准LALM 推理排行榜──
- [HEAR benchmark](https://hearbenchmark.com/) sesli SSL referansları.
  İşitmek 基准音频 SSL 评估基准──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

