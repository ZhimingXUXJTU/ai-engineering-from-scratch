# Spektrogramlar, Mel Skala ve Ses Özellikleri

> Neural ağlar çiğ dalga biçimlerini iyi tüketmezler. Spektrogramları tüketirler. Mel spektrogramlarını daha iyi tüketirler. 2026'da her ASR, TTS ve ses sınıflandırıcısı bu tek önceden işleme seçeneğiyle yaşar veya ölür.

> **【中文解读】**Neural net işleminin orijinal dalga şekli etkisi iyi değil, ama işlem frekansı grafik etkisi iyi, işlem Mel 频谱 grafik etkisi daha iyi. 2026 yılında tüm ASR、TTS 和音频分类器 başarısı bu bir önceden işlem seçeneğine bağlıdır.

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**Mel 频谱图将音频转换为 2D 图像(时间×频率), CNN/ViT 处理──Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

10 saniyelik 16 kHz klip al. 160.000 dalga.`[-1, 1]`"Köpek havlaması" ya da " kedi kelimesi" etiketleriyle neredeyse tamamen ilişkili olmayan. Çiğ dalga şekli bilgiyi içerir, ancak bir biçimde model kolayca çıkaramaz. 100 ms arası konuşulan iki aynı fonem tamamen farklı çiğ örneklere sahiptir.

> 10 saniyeli 16 kHz ses frekansı... 160.000 个浮点数,全在`[-1, 1]`范围内, neredeyse " köpek çağır" veya " kelime kedi " etiketleriyle tamamen ilgisi yoktur.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Bir spektrogram bunu düzeltir. İnsan algısının onu görmezden geldiği zamansal ayrıntıları çökür (mikrosekundu jitter) ve algının katıldığı yapı (frequency enerjik olan, ~ 1025 ms'lik zaman pencereleri boyunca) korur.

> 频谱图 bu sorunu çözdü. İnsan algısının göz ardı ettiği zaman ayrıntılarını sıkıştırdı, algılama kaygılarının yapısını korudu.

Mel spektrogramları daha da ileriye doğru ilerler. İnsanlar yüksek sesleri logaritmik olarak algılar: 100 Hz vs. 200 Hz 1000 Hz vs. 2000 Hz ile "eşit mesafe" sesleri. Mel ölçeği frekans eksisini eşleşecek şekilde çarpıtır. Mel ölçeği spektrogramı 2010-2026 yılları arasında konuşma ML'de en önemli özelliktir.

> Mel 频谱图进一步── İnsanların yüksek sesle ilgili algılamaları sayısal olarak: 100 Hz ile 200 Hz 听起来和 1000 Hz ile 2000 Hz "as far away"──Mel ölçeği frekans ekseni çarpıklıkları ile uyumlu olarak bu algılamalara göre gerçekleşecek──Mel 频谱图 2010-2026 yılları arasında ses makinesi öğreniminde en önemli tek özelliktir──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**Dalga şeklini üst üste döşen çerçevelere kes (tipik: 25 ms penceresi, 10 ms hop = 400 örnek / 16 kHz'de 160 örnek). Her çerçeveyi bir pencere işleviyle çarpın (Hann varsayılan; Hamming biraz farklı bir değişim).`(n_frames, n_freq_bins)`Bu senin spektrogramın.

> **STFT（短时傅里叶变换）。**Genel olarak 25 ms fendi, 10 ms 步长 = 16 kHz 下 400 采样点 / 160 采样点) ⋅ her 乘以窗函数 (默认 Hann;Hamming 略有不同) ⋅对每做 FFT。将幅谱堆叠成`(n_frames, n_freq_bins)`Bu senin frekans çizgisinin bir parçası.

**Log-magnitude.**Çömlek büyüklükleri 5-6 büyüklük sırası arasında değişir.`log(|X| + 1e-6)`veya `20 * log10(|X|)`Her üretim borusunda çiğ büyüklük değil, log büyüklüğü kullanılır.

> **对数幅度。**İlk boyut 5-6 sayısal seviyeye kadar.`log(|X| + 1e-6)`Ya da`20 * log10(|X|)`Sıkıştırma dinamik aralığı. Her üretim akımı, orijinal değil, sayısal boyut üzerinde kullanılır.

**Mel scale.**Sıklık`f`Hz haritelerinde mel `m`- ...`m = 2595 * log10(1 + f / 700)`. Haritalama yaklaşık olarak 1 kHz'nin altında lineer ve yukarıda yaklaşık olarak logaritmiktir.

> **Mel 尺度。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `f`(Hz)映射到 mel `m`公式为`m = 2595 * log10(1 + f / 700)`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                           

**Mel filterbank.**Mel ölçeğinde eşit derecede uzanan üçgenli filtrelerin bir kümesi. Her filtreler, bitişik FFT kutularının ağırlıklı toplamıdır. STFT büyüklüğünü filtrebank matrisine çarpırsak, bir matmul'de mel spektrogramını verir.

> **Mel 滤波器组。**Bir grup mel ölçeğinde sıralanmış üçgen 波器── her 波器 ise, komşu FFT binin artışı ve ⋅ olacak STFT genişliği 波器组矩阵 ile çarpılır.

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`- Whisper'in girişleri, Parakeet'in girişleri, Seamless M4T'nin girişleri, evrensel 2026 ses ön uçları.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`❖ Hıskançlık ❖ Paraket ❖ Hıskançlık M4T ❖ 2026 yıl genel kullanımlı ses ses sesleri ❖

**MFCCs.**Log-mel spektrogramını alın, DCT (Tipe II) uygulayın, ilk 13 katılamı tutun. Özellikleri dekorele eder ve daha da sıkıştırır. Çöm log-mellerde CNN'ler / Transformers yakalandığı 2015 yılına kadar baskın özellik. Hâlâ hoparlör tanıma (x vektörleri, ECAPA) için kullanılır.

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II),保留前 13 个系数──除特征间相关性并进一步压缩──2015 yılından önce baskın özellik, ardından CNN/Transformer 在原始 log-mel 上追上── halen konuşma için kullanılır 的人识别(x-vectors、ECAPA)。

**Resolution trade.**Daha büyük FFT = daha iyi frekans çözünürlüğü ancak daha kötü zaman çözünürlüğü. 25 ms / 10 ms ses-ML standartıdır; müzik için 50 ms / 12.5 ms; geçici algılama için 5 ms / 2 ms (baton vurguları, plosivler).

> **分辨率权衡。**Daha büyük FFT = daha iyi frekans çözünürlüğü ama daha kötü zaman çözünürlüğü──25 ms / 10 ms ise ses frekansının öntanımlı değeri;50 ms / 12.5 ms müzik için;5 ms / 2 ms anlık bir denetim için;]]

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
spectrogram-window
```

## Yapın

### Adım 1: Dalga şeklini çerçeve

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

10 saniyelik 16 kHz klip ile `frame_len=400, hop=160`998 çerçeve verir.

> Bir bölüm 10 秒 16 kHz 的音频,使用 `frame_len=400, hop=160`998'e ulaştım.

### Adım 2: Hann penceresi

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

FFT'den önce element olarak çarpın. sıfır olmayan uç noktalarda kısaltma nedeniyle kaynaklanan spektral sızıntıları ortadan kaldırır.

> FFT'den önce elementlerin birbiriyle çarpılması, non-zero-point kesintiye yol açan frekans sızdırmalarının ortadan kaldırılması.

### Adım 3: STFT büyüklüğü

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Üretim kullanımları `torch.stft`veya `librosa.stft`Bu döngü pedagojiktir; kısa klipler üzerinde çalışır.`code/main.py`- Evet .

> 生产环境使用 `torch.stft`Ya da`librosa.stft`(FFT ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞`code/main.py`Çekilme ve çekecek.

### Dördüncü adım: mel filterbank

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 mels 08 kHz ile`n_fft=400`bir `(80, 201)`Matrix.`(n_frames, 201)`Transpose ile STFT büyüklüğü elde etmek için `(n_frames, 80)`Mel spektrogramı.

> 80'i kapsamlı.`n_fft=400`- Al .`(80, 201)`- Ben de öyleyim.`(n_frames, 201)`STFT 幅ü çarpı  dönüştürülmüş`(n_frames, 80)`- Evet.

### Adım 5: log-mel

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Ortak alternatifler: `librosa.power_to_db`(referans normallaştırılmış dB),`10 * log10(power + eps)`. Whisper daha fazla katılımcı bir klip kullanır + rutinleri normalleştirir (Whisper's `log_mel_spectrogram`)

> 常见替代方案:`librosa.power_to_db`(Debliklere değinmek için)`10 * log10(power + eps)`❖ Şapışkın daha karmaşık kesim + 归一化流程`log_mel_spectrogram`)。

### Adım 6: MFCC'ler

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Bu, MFCC matrisinizdir. İlk katı genellikle düşürülür (toplam enerjiyi kodlar).

> Her log-mel için DCT uygulamak için, 13 系数 korun. İşte MFCC 矩阵ınız.




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Başparmak kuralı: **if you are not working on music, start with 80 log-mels.**Kanıt yükü herhangi bir sapıklık üzerindedir.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**Her türlü ayrımın mantıklılığını kanıtlamak gerekir.



## 2026'da hala yolculuk eden tuzaklar

> 2026 yılı hâlâ suçlu bir tuzağa düşüyor.

- **Mel count mismatch.**80 mels ile eğitim, 128 mels ile sonuç, sessiz başarısızlık, her iki ucunda da özellik şeklini kaydet.
  **Mel 数量不匹配。**訓練用80m,推理用128m. 静默失败──在两端记录特征形状──
- **Sample-rate mismatch upstream.**22.05 kHz'de hesaplanan Mels 16 kHz'den farklı görünüyor.
  **上游采样率不匹配。**22.05 kHz  hesaplama mels ile 16 kHz                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
- **dB vs log.**Whisper, dB-mel değil log-mel bekliyor.
  **dB 与 log。**HF 流水线会自动检测;Your自定义代码不会──
- **Normalization drift.**Eğitim sırasında bir çıkış normallaştırması, sonuçlama sırasında küresel normallaştırma.
  **归一化漂移。**訓練時逐句归化,推理時全局归化── bu üretim hataları 翻倍化.
- **Leakage from padding.**Bir klifin sonunu sıfırla doldurmak, arka çerçevelerde düz bir spektrum oluşturur.
  **填充泄漏。**Sonraki bölümde                                                                                                                                                                                                                                                             

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-feature-extractor.md`. Yetenek belirli bir model hedefi için özellik türü, mel sayısı, çerçeve/sıkış ve normallaşımı seçer.

> 保存为 `outputs/skill-feature-extractor.md`◊ Bu beceri belirli bir modelin hedef seçimi için özellik türü, sayı, / adım, ve birleştirme biçimi için kullanılır.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`. Bir çırp sentez eder (frekans 200 → 4000 Hz) ve çerçeve başına argmax mel bin yazdırırır.
   **简单。**运行  İşlem`code/main.py`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △   △                                           
2. **Medium.**Tekrar çalıştır `n_mels`İçeride`{40, 80, 128}`ve `frame_len`İçeride`{200, 400, 800}`Zaman eksisinde keskin yükseklik bant genişliğini ölçün.
   **中等。**Kullan .`n_mels`Çı`{40, 80, 128}`和 `frame_len`Çı`{200, 400, 800}`重新运行──沿时间轴测量峰带宽── hangi kombinasyon sinyalleri en iyi şekilde ayırt eder?
3. **Hard.**Uygulama`power_to_db`ve AudioMNIST'te küçük bir CNN sınıflandırıcısının ASR doğruluğunu (a) çiğ log-mel, (b) dB-mel ile karşılaştırmak`ref=max`, (c) MFCC-13 + delta + delta-delta.
   **困难。** gerçekleştirmek `power_to_db`, on AudioMNIST 上用微型 CNN 分类器比较 (a) 原始 log-mel、(b)`ref=max`dB-mel  c) MFCC-13 + delta + delta-delta  准确率── rapor top-1 准确率──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420)- MFCC kağıdı.
  Davis、Mermelstein (1980) 单音节词识别的参数化表示比较MFCC 论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) orijinal mel ölçeği.
  Stevens, Volkmann, Newman (1937) 心理音高量级的尺度尺度 原始 mel 尺度
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) referans uygulanmasını okuyun.
  Açık AISipp 源码,log_mel_spectrogram阅读参考实现──
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) referans için `mfcc`- Evet .`melspectrogram`, ve hop / penceresi.
  kitaplık Özellikleri`mfcc`- Evet.`melspectrogram`和 hop/window 的参考──
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) Parakeet + Canary modelleri için üretim ölçeği boru hattı.
  NVIDIA NeMo音频预处理Parakeet + Canary 模型的生产级流水线──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

