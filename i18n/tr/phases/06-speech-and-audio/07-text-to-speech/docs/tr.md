# Metin-Söz (TTS)  Tacotron'dan F5'e ve Kokoro'ya 语音合成  Tacotron'dan F5'e ve Kokoro'ya

> ASR konuşmayı metine çevirir; TTS metini konuşmaya çevirir. 2026 yığın üç parçadan oluşur: metin → jetonlar, jetonlar → mel, mel → dalga şekli. Her bölümde bir dizüstü bilgisayarına uyan bir varsayılan model vardır.

> **【中文解读】**ASR 把语音变文字,TTS 把文字变语音──2026 yılının TTS 技术分三步:文本→token→Mel 频谱→波形── her adımda bir tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane

> **【拓展：TTS 的应用】**TTS, bir sesli kitap, bir sesli yolculuk, bir sahte yardımcıdır.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

Bir ipiniz var: "Sevgililer, bana öğleden sonra saat 6'da bitkileri sulamayı hatırlatın". Doğal bir sesli, doğru bir prosodiye sahip olan, doğru vokal ile "bitkileri" telaffuz eden ve canlı bir ses asistanı için bir CPU'da 300 ms'den az süren 3 saniyelik bir ses klipi gerekiyor. Ayrıca ses değiştirmeniz, kod değiştirilmiş girişleri ("6'da hatırlat beni, daijoubu?") ile çalışmanız ve isimlerle utanmamanız gerekir.

> "Size lazım bir bölüm 3 saniyelik ses ses, dinle doğayı, 律正确(停顿、重音), "bitkiler"in元音发音正确,并且在CPU上不到300 ms 就能运行以用于实时语音助手──你还需要切换声音、处理混合语言输入("size lazım, daijoubu?"),且不能在人名上出错──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Modern TTS boru hattları şöyle görünüyor:

> 现代 TTS 流水线如下:

1. **Text frontend.**Metni (tarihler, numaralar, e-postalar) normalleştirin, fonemlere veya alt sözcük işaretlerine dönüştürün, prosody özelliklerini tahmin edin.
   **文本前端。**归一化文本(日期、数字、邮箱),转换为音素或子词符号,预测律特征。
2. **Acoustic model.**Metin → mel spektrogram. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。**文本 → Mel 频谱图──Tacotron 2(2017)、FastSpeech 2(2020)、VITS(2021)、F5-TTS(2024)、Kokoro(2024)。
3. **Vocoder.**Mel → dalga şekli. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), 2024+'te sinir kodek vokodörleri.
   **声码器。**Mel → 波形──WaveNet(2016)、WaveRNN、HiFi-GAN(2020)、BigVGAN(2022)、2024+ 的神经编解码声码器──

2026'da akustik + vokodör uçtan uçta yayılma ve akış eşleşme modelleri ile parçalanır.

> 2026 yılında, sonuna sonuna kadar yayılma ve akış uyumlu modellerin ortaya çıkmasıyla birlikte, sesik model + ses kodlayıcılarının sınırı bulanık hale geldi.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**Seq2seq: char-embedding → BiLSTM encoder → location-sensitive attention → autoregressive LSTM decoder mel frame'leri yayar.

> **Tacotron 2（2017）。**Seq2seq:字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定──仍被引用为基线──

**FastSpeech 2 (2020).**Bir sonlama, Tacotron'dan 10 kat daha hızlı. Biraz doğallik kaybeder (monoton uyum) ama her yere gemi.

> **FastSpeech 2（2020）。**Bu nedenle, bu durumun bir sonraki döneminde, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre sonra, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir sürece, bir süre, bir sürece, bir sürece, bir sürece, bir sürece, bir sürecececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece

**VITS (2021).**Birlikte kodlayıcı + akış tabanlı süresi + HiFi-GAN vokodörü sonu sonu sonu olarak varyasyonsal sonuçlandırma ile birlikte trenler. Yüksek kalite, tek model. Dominant açık kaynak TTS 20222024. Variantlar: YourTTS (büyük hoparlör sıfır çekim), XTTS v2 (2024, Coqui).

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型。2022-2024年主导开源 TTS。变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)。

**F5-TTS (2024).**Doğal prosodi, sıfır çekim ses klonlaması, 5 saniye referans sesle. 2026 açık kaynaklı TTS sıralama tablolarının en üst kısmı. 335M param.

> **F5-TTS（2024）。**基于流匹配的扩散 Transformer──自然律,5 秒参考音频零样本声音克隆──2026年开源 TTS 排行榜榜榜首──3.35 亿参数──

**Kokoro (2024).**Küçük (82M), CPU-işletilebilir, gerçek zamanlı kullanım için sınıfındaki en iyi İngilizce TTS.

> **Kokoro（2024）。**Küçük tip(8200.000 parametre), CPU'da çalıştırılabilir, aynı sınıf en iyi gerçek zaman İngilizce TTS──封闭词表仅限英文,Apache-2.0 许可──

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**ElevenLabs v2.5 duygu etiketleri ("[Fısıltılı]", "[kahkaha]") ve karakter sesleri 2026'da sesli kitap üretimine hakim olur.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业 SOTA──ElevenLabs v2.5 的情感标签("[buzlayarak]"、"[gülüyor]")和角色声音主导 2026年有声书制作──

### Vocoder evrimi

> ### Sesle çal

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

2026 yılına kadar çoğu "TTS" modeli metinden dalga şekline son derece uzaktır; mel spektrogram bir iç temsilidir.

> 2026 yılına kadar, çoğu "TTS" modeli metinden dalga şeklinde bir son modeline kadar; Mel 频谱图 is internal representation.

### Değerlendirme

> ### 评估

- **MOS (Mean Opinion Score).**1-5 ölçeği, kalabalık kaynaklı.
  **MOS（平均意见分）。**1-5 分量表,众包──仍然是黄金标准;速度痛苦地慢──
- **CMOS (Comparative MOS).**A-vs-B tercihleri, her not için daha sıkı güven aralıkları.
  **CMOS（比较 MOS）。**A-vs-B  偏好──每个标注的置信区间更狭──
- **UTMOS, DNSMOS.**Referanssız sinirsel MOS tahmincileri, sıralama çizelgeleri için kullanılır.
  **UTMOS、DNSMOS。**无参考神经 MOS 预测器──用于排行榜──
- **CER (Character Error Rate) via ASR.**TTS çıkışını Whisper üzerinden çalıştır, giriş metnini CER ile hesapla.
  **CER（字符错误率）通过 ASR。**TTS'i fısıldayarak çıkarmak, giriş yazısını hesaplamak,
- **SECS (Speaker Embedding Cosine Similarity).**Ses klonlama kalitesi.
  **SECS（说话人嵌入余弦相似度）。**声克隆质量──

LibriTTS test temizlemesi için 2026 numarası:

> 2026 yılı LibriTTS test-clean 上的数字:

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.




## Yapın.
```figure
sp-tts-stack
```

## Yapın

### Adım 1: fonemize giriş

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Phonemler evrensel bir köprüdür.

> 音素是通用桥梁──避免将原始文本输入到VITS 级别以下的任何模型──

### Adım 2: Kokoro (2026 CPU varsayılan) çalıştır

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

Oplandık, tek dosya, 82M param.

> İletişim, tek bir dosya 82 milyon parametre

### Adım 3: Ses klonlaması ile F5-TTS çalıştır

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

5 saniyelik referans klipi + transkripti geçin; F5 prosodi ve timbre klonları.

> 传入 5 秒参考音频 + 其转录文本;F5 克隆律和音色──

### Adım 4: HiFi-GAN vokodörü sıfırdan

Bir öğretim metni için çok büyük ama şekli şöyle:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Eğitim: karşıtlık (kısık pencerelerde ayrımcılık) + mel spektrogramı yeniden yapılandırma kaybı + özellik eşleşme kaybı.`hifi-gan`repo veya nvidia-NeMo.

> 訓練:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`倉庫或 nvidia-NeMo'nın önceden eğitim kontrol noktası

### Adım 5: Tam boru hattı (pseudokod)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

2026 yılına kadar açık kaynak liderleri: **F5-TTS for quality, Kokoro for efficiency**Tarihçi olmadıkça Tacotron'a ulaşmayın.

> 2026 yıl açık kaynak liderleri:**F5-TTS 追求质量，Kokoro 追求效率**Tarihçi olmadıkça, Tacotron'u kullanma.



## Tuzaklar

> 常见陷

- **No text normalizer.**"Dr. Smith" "Doctor" veya "Drive" olarak mı okunuyor? "2026" "twenty twenty six" veya "two zero two six" olarak mı?
  **没有文本归一化器。**"Dr. Smith" 读成"Doctor"还是"Drive"?2026"读成"20266"还是"two zero two six"?在音素化之前归归一化──
- **OOV proper nouns.**"Ghumare" → "ghyu-mair"?
  **OOV 专有名词。**"Ghumare" → "ghyu-mair"?
- **Clipping.**Vocoder çıkışı nadiren klipler, ama mel ölçekleme yanlış sonucu ±1.0 aşarak olabilir.`np.clip(wav, -1, 1)`- Evet .
  **削波。**声码器输出很少削波,但推理时 Mel 缩放不匹配可能超出 ±1.0──始终使用 `np.clip(wav, -1, 1)`- Evet.
- **Sample-rate mismatch.**Kokoro 24 kHz çıkışı sağlar. Aşağıdaki boru hattınız 16 kHz → yeniden örneklenmesini bekler veya isimsizliğe sahip olur.
  **采样率不匹配。**Kokoro 输出 24 kHz;你的下游流水线期望 16 kHz → 重采样否则产生混叠──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-tts-designer.md`. Belirli bir ses, gecikme ve dil hedefi için TTS boru hattı tasarlayın.

> 保存为 `outputs/skill-tts-designer.md`◊ belirli ses için 、延迟和语言目标设计 TTS 流水线──

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Oyuncak sözcüklerinden fonem sözlüğü oluşturur, fonem başına sürenin tahminini yapar ve sahte bir "mel" programını basar.
   **简单。**运行  İşlem`code/main.py`❖ Oyuncak kelimelerinden yapısal sesli metin, her sesli metin süresini tahmin etmek,
2. **Medium.**Kokoro'yu yükle, sesle aynı cümleyi sentezle.`af_bella`ve `am_adam`- Ses sürelerini ve öznel kalitesi ile karşılaştırın.
   **中等。**Kokoro'yu kullan.`af_bella`和 `am_adam`声合成同一句话──比较音频时长和主观质量──
3. **Hard.**Kendinizi 5 saniyelik referans klipi kaydetin, F5-TTS'i kullanın klonlayın ve referans ve klon çıkışları arasında SECS raporlayın.
   **困难。**Kayıt bir bölüm 5 saniye kendiliğinden referans sesleri.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) sek2 sek'in başlangıç çizgisi.
  Shen 等 (2017). Tacotron 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) Sonundan sonuna akış tabanlı.
  Kim, Kong, Son (2021).
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) mevcut açık kaynaklı SOTA.
  Chen 等 (2024). F5-TTS当前开源SOTA。
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646)2026'da hala gemiye giden Vocoder.
  Kong, Kim, Bae (2020). HiFi-GAN2026 yıl hâlâ kullanımda ses kodlayıcıları.
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 CPU dostu İngiliz TTS.
  Kokoro-82M 在 HuggingFace 上2024 yıl CPU 友好的英文 TTS。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

