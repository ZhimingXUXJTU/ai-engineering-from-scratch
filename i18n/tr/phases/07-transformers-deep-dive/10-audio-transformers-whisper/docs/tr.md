# Ses Transformers  Fısıltı Yapılandırması 音频 Transformer  Fısıltı Yapılandırması

> Ses, zamanla frekansın bir görüntüdür.

> **【中文解读】**Transformer ile fısıldayın, Transformer ile yapın. Transformer ile nasıl bir simge oluşturacağınızı anlayın.

**Type:** Study | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Whisper'den önce (OpenAI, Radford et al. 2022), en gelişmiş otomatik konuşma tanıma (ASR) wav2vec 2.0 ve HuBERT  kendiliğinden denetim edilen özellik çıkarıcıları ve ince ayarlanmış bir baş anlamına geliyordu. Yüksek kalite, pahalı veri boru hattları, alan kırılganlığı. Çok dilli konuşma tanıma dil ailesi başına ayrı modeller gerektiriyordu.

> Whisper, Radford  et al., 2022) öncesinde, en gelişmiş otomatik dil tanımlama (ASR) wav2vec 2.0 ve HuBERT'in kendiliğinden denetim özellikleri ile yapılan bir inceleme makinesi kullanıldı.

Whisper üç bahis yaptı:

> Şapşır üç şey yaptı:

1. **Train on everything.**İnternetten 97 dilde 680.000 saat zayıf etiketli ses çıkartıldı temiz akademik bir kitap yok fonem etiketleri yok.
   Çeviri:**用一切数据训练。**İnternetten çekilen 680.000 saat, 97 dil kapsıyor.
2. **Multi-task single model.**Bir dekoder, birlikte transkripsiyon, çeviri, ses etkinliği algılama, dil kimliği ve görev işaretleri aracılığıyla zaman damgası konusunda eğitilmiştir.
   Çeviri:**单模型多任务。**Bir çözücü görev simgesi geçiyor 联合训练转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**Kodlayıcı log-mel spektrogramlarını tüketir. Dekoder metin belirtilerini otomatik olarak üretir. Vocoder, CTC, HMM yoktur.
   Çeviri:**标准编码器-解码器 Transformer。**编码器消费 log-mail 频谱图──解码器自归生成文本代币──无声码器,无CTC,无HMM──

Sonuç: Whisper large-v3 aksan, gürültü ve sıfır temiz etiketlenmiş verilere sahip diller arasında sağlamdır. 2026'da her açık kaynaklı ses asistanı ve çoğu ticari için öntanımlı konuşma ön ucudur.

> Sonuç:Susper large-v3 konuşma, gürültü ve sıfır işaretleme verisi dillerinde de çok güçlü bir özellik vardır. 2026 yılında her açık kaynaklı ses asistanının ve çoğu ticari ses asistanının ön kesimi olarak kullanılacaktır.

> **【中文解读】**Whisper'ın üç büyük yeniliği: 1) 680.000 saat zayıf işaretleme sesli eğitim, 97 种语言; 2) 单模型多任务(转录、翻译、语种识别、时间); 3) 标准编码器-解码器 Transformer 架。音频被转构为 log-mail 频谱图(类似图像),编码器处理频谱特征,解码器生成文本。

## Konsepten bir şey.

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Adım 1  Yeniden örnekleme + pencere

Ses 16 kHz. Klip/pad 30 saniye. Hesaplama log-mel spektrogramı: 80 mel bin, 10 ms adım → ~ 3.000 çerçeve × 80 özellik. Bu Whisper'in gördüğü "girinme görüntüsü".

> 音频采样率 16 kHz──剪剪/填充到30秒──计算日志-mail 频谱图:80 个梅尔频率 bin,10 ms 步长 → 约 3,000  × 80 特征──这是 Whisper 看到的"输入图像"──

### Adım 2  kıvrımlı gövde

Kerne 3 ve adım 2 ile iki Conv1D katmanı 3000 çerçeveyi 1.500'e düşürür.

> 两层 Conv1D(核大小 3,步长 2) 3.000  olarak 1500  olarak azaltılacak.

> **【拓展：Whisper 的多语言能力来源】**Whisper 97 种语言、68万小时音频上训练,多语言能力来自两个因素:(1) 超大规模的弱标注数据覆盖绝大多数语言;(2) 统一的BPE 词表是GPT-2 词表的超集,天然支持多语言──decoder prompt 中的语言代号(如`<|zh|>`) kontrol output language, aynı model gerçekleştirmek için transcript veya çeviri görevleri sağlar.

### Adım 3  kodlayıcı

Bir 24 katmanlı (büyük) 1500 zaman aşamasında bir transformer kodlayıcı. Sinusoidal pozisyon kodlaması, kendi kendine dikkat, GELU FFN. 1,500 × 1,280 gizli durum üretir.

> Bir 24 katlı  büyük 版本) Transformer 编码器处理 1,500 个时间步──正弦位置编码、自注意力、GELU FFN──产生 1,500 × 1,280 的隐藏状态──

### Adım 4  dekodör

24 katmanlı bir transformatör dekodörü. Bir kaç ses özel özel jetonlarla GPT-2'lerin bir süperset olan bir BPE sözlükten jetonlar üretir.

> Bir 24 katlı Transformer 解码器──自归地从 BPE 词表生成代币,该词表是GPT-2 词表的超集,外加几个音频专用特殊代币──

### Adım 5  görev işaretleri

Dekodör istekleri, modelin ne yapacağını söyleyen kontrol işaretleriyle başlar:

> Kontrol simgesi açmak için, model'e ne yapması gerektiğini söyle.

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

veya

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

Bu model bu konvensiyona göre eğitilmiştir. Görevleri önbellekle kontrol ediyorsunuz. 2026'da talimat ayarlama eşdeğeri, ama konuşmaya uygulanır.

> Bu, ses alanındaki bir düzeltme yöntemi.

> **【中文解读】**Whisper'in görev kontrol mekanizması çok iyi:`<|transcribe|>`Ya da`<|translate|>`) görev türünü belirlemek için. Bu, farklı ön belirtiler yoluyla aynı modelin dil alanında uygulanması için " talimatları düzenlemektir.

> **【拓展：Whisper 在语音助手中的应用】**Şapışmak 2026 yılında语音 AI'nin temel bileşeniyor. Gerçek zamanlı语音助手den video şablonı üretmeye, yeniden çok dil konuşma konferansının çevirmesine, Şapışmak 统一的语音前端提供了. Şapış-turbo (dört katlı çözücü) 8 kat daha az gecikecek.

### Adım 6  çıkış

Çığlık arama (genişlik 5) log-prob eşiği ile.`<|notimestamps|>`Token yok.

> 束搜索(宽度 5)加对数概率值──当没有 `<|notimestamps|>`Zamanı her 0.02 saniye boyunca bir kez tahmin ediyorum.

### Şapşırma boyutları

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

Büyük v3-turbo (2024) 32 katmanlı bir decoder'i <1 WER nokta geri dönüşü ile 4.8x daha hızlı decoder'e düşürüyor.

> Büyük v3-turbo(2024) çözücü 32 katından 4 katına düşecek. çözücü hızı 8 kat artar, WER 退化不到 1个百分点. Bu çözücü hızın kırılımı 2026 yılında Whisper-turbo 成为语音代理默认选择的原因──

> **【拓展：音频 Transformer 的统一趋势】**语音识别(Hisper)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向 Transformer 架构──核心思路相同:将音频转换为频谱图或离散符号 序列,然后使用标准 Transformer 处理──

### Şapşırmanın yapmadığı şeyler

- Günlükleme yok, bunun için bir çiftlik.
  Çinçe Çevirimiçi:没有说话人分离(谁在说话) ⋅需要搭配 ⋅
- Gerçek zamanlı akış yok  30 saniyelik pencerenin sabitlenmesi.`faster-whisper`- Evet .`WhisperX`) VAD + üst üste geçiş yoluyla akış açısını kapatmak.
  Çin Çeviri: 没有原生实时流式处理30秒窗口是固定的──现代封装器(`faster-whisper`- Evet.`WhisperX`) VAD + 重叠实现流式处理 арқылы:
- Dış parçalanmadan 30 saniye sonra uzun şekil bağlamı yoktur. İnsan konuşmasının transkripsiyon için nadiren uzun mesafeli bağlamın gerekliliği olduğu için pratikte iyi çalışır.
  Çinçe Çevirimi: hiç dış kısım blokları ise 30 saniyelik uzunluklı bir biçim üzerinde desteklenmiyor.

### 2026 manzarası

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Yapın.
```figure
n5-mel-decode
```

## Yapın

Bakın .`code/main.py`Biz Whisper'i eğitmiyoruz. log-mail spektrogram hattını + görev belirtileri uyarı formatörünü yapıyoruz.

> 参见 `code/main.py` Biz eğitim görmüyoruz Şapışmak  Biz log-mail yapılandırıyoruz  频谱图管道 + 任务符号 提示形式化器── bunlar üretimdeki pratik temasın bir parçasıdır──

### Adım 1: Ses sentezi

16 kHz'de 16 bin numune ile 440 Hz'de bir saniyelik sinüs dalgasını üretmek.

> Bir saniyelik 440 Hz normal dalga, 16 kHz ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼ 16.000 ∼

### Adım 2: Log-mel spektrogramı (sederletilmiş)

Tam mel spektrogramı FFT gerektirir.`librosa`- ...

> 完整的梅尔频谱图需要FFT──我们做一个简化分+逐能量版本,无需`librosa`Gösterme kanalları:

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

Çerçeve = 25 ms, hop = 10 ms. Whisper'in penceresine uyuyor.

>  = 25 ms,步长 = 10 ms── Whisper'ın penceresine uygun,   enerji öğretim gösterisi için kullanılır,

### Adım 3: 30 saniye

Whisper her zaman 30 saniyelik parçaları işliyor.

> Şapışmak 总是处理 30秒分块──将频谱图填充或剪) 3,000 ──

### Adım 4: Hemen simgeler oluştur

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

Bu görev kontrol yüzeyinin tamamı.

> Bu, tüm görevlerin kontrolü.

## Çerçeveyi kullanın.

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Daha hızlı, OpenAI ile uyumlu:

> Daha hızlı, OpenAI ile uyumlu olan bir çözüm:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- Bir model ile çok dilli ASR.
  Çinçe Çevirimi Çevirisi: Using a model do multi-lingual ASR。
- gürültülü, çeşitlilikli seslerin sağlam bir transkripsiyonu.
  Çinçe Çevirimi:                                                                                                                                                                                                                                                            
- Araştırma / prototip ASR  en hızlı başlangıç noktası.
  Çinçe Çevirimi:研究/原型 ASR最快的起点──

**When to pick something else:**

> **何时选择其他方案：**

- Ultra düşük gecikme oranında  Moonshine eşleşen kaliteli Whisper'i yener.
  Çinçe Çevirimi: 边缘设备上的超低延迟流式处理月光 在相同质量下比 ささやく 更快──
- Gerçek zamanlı sohbet AI'si <200 ms  özel akış ASR'ye ihtiyaç duyar.
  Çinçe Çevirimiçi: <200ms'ın gerçektir
- Konuşmacı günlükleştirme  Fısıltı bunu yapmaz; pyannote'de bir şırıltı.
  Çinçe Çevirim:                                                                                                                                                                                                                                                            

## İndirin . Ürünler .

Bakın .`outputs/skill-asr-configurator.md`. Yetenek bir ASR modeli, kodlama parametreleri ve yeni bir konuşma uygulaması için önceden işleme boru hattını seçer.

> 参见 `outputs/skill-asr-configurator.md`Bu beceriler yeni bir dil uygulaması seçmek için ASR modelleri, çözüme kavuşturma parametreleri ve önceden işleme kanalları.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`16 kHz'de 1 saniye sinyal için 10 ms hop'un 100 kadro olduğunu onaylayın. 30 saniye için: 3000 kadro.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 1 saniye sinyalini 16 kHz,10 ms 步长下约100 ──30 saniye:约3,000 ──
2. **Medium.**Tüm log-mel spektrogramını kullanarak oluşturun `numpy.fft`80 tane kutu eşleşmesini kontrol et .`librosa.feature.melspectrogram(n_mels=80)`Sayı hataları içinde.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`numpy.fft`构建完整的日志频谱图――验证 80 个 频率bin                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         `librosa.feature.melspectrogram(n_mels=80)`Hedef hataları aralığında uyumlu olarak.
3. **Hard.**Akış sonucu uygulamak: 2 saniyelik bir üst üstelik 10 saniyelik pencerelere parça ses, her parça üzerinde fısıldayarak çalıştırmak, transkriptleri birleştirmek. 5 dakikalık bir podcast örneğinde kelime hatası oranını vs. tek geçiş oranını ölçmek.
   Çinçe Çevirim: 实现流式推理:将音频分成10秒窗口(2秒重叠), her pencerede yürür Şapış,合并转录──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Daha fazla okumak

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Fısıltı kağıdı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [OpenAI Whisper repo](https://github.com/openai/whisper) Referans kodu + model ağırlıkları.`whisper/model.py`Conv1D kökünü + kodlayıcı + dekodörü yukarıdan aşağıya 400 satırda görmek için.
  中文翻译:OpenAI Whisper 代码仓库, yaklaşık 400 行代码展示 Conv1D stem + 编码器 + 解码器。
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) Adım 56'da açıklanan ışın araması + görev belirti mantığı burada; 500 satır, tamamen okunur.
  Çinçe Çevirim:束搜索 + 任务代币 逻辑的实现,500 行代码,完全可读──
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) öncü; bazı ayarlarda hala SOTA özellikleri.
  Çeviri:Whisper'ın önümüzdeki hali, bazı durumlarda hala SOTA özellikleri olarak görülüyor.
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) üretim ambalajı, referanstan 4x daha hızlı.
  Çinçe Çevirim:Hızlı-sısırt 生产封装器,比参考实现快4倍。
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 kenar dostu ASR, Fısıltı şeklinde ama daha küçük.
  Çin Çeviri, 2021 yıl yüz yüze kenarında ASR,类  sussur, mais更小──
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) mel spektrogram önceden işlemeci ve simge zaman damgası kullanımı dahil olmak üzere kanonik ince ayarlama tarifi.
  Çinçe Çevirim:HuggingFace Whisper 微调教程,包括梅尔频谱图预处理器和代币 时间处理。
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) ders mimarisi şemalarını yansıtan tam uygulamayı (kodlama, dekodlama, çapraz dikkat, jenerasyon).
  Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe, Çeviri:Türkçe
