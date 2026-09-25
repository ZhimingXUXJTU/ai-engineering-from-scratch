# Ses Temelleri  Dalga şekilleri, örnekleme, Fourier dönüştürücüsü  音频基础  波形、采样与里叶变化

> Dalga şekilleri çiğ sinyalidır. Spektrogramlar temsilidir. Mel özellikleri ML dostu formudur. Her modern ASR ve TTS boru hattı bu merdivenin üzerinde yürür ve ilk adım örnekleme ve Fourier'i anlamak.

> **【中文解读】**波形是原始信号,频谱图是表示形式,Mel特征是机器学习的友好的形式──每个现代语音识别(ASR) 和语音合成(TTS) 系统都沿着这个阶梯上:波形 → 频谱图 → Mel特征──第一阶段就是理解采样和里叶变换──

> **【拓展：音频 AI 的基础】**采样率 (örneğin 16kHz) belirleyebilir en yüksek frekansını belirler. 里叶变化将时域信号分解为频域成分.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

Bir mikrofon bir basınç ve zaman sinyali üretir. sinir ağınız tenzorlar tüketir. Onların arasında bir dizi konvansiyon bulunur ve bu konvansiyonlar ihlal edildiğinde sessiz böcekler üretir: model iyi çalışır ama WER iki katlanır, ya da TTS bir hisseder veya ses klonlama sistemi hoparlör yerine mikrofonı ezberler.

> 麦克风产生一个压力-时间信号―― 麦克风产生一个压力-时间信号―― 麦克风产生一个压力-时间信号―― 麦克风产生一个压力-时间信号―― 麦克风产生一个隐性 bug:模型训练正常但WER 翻倍,或 TTS 输出声,或语音克隆系统记住麦克风而不是说话人――

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Konuşma sistemlerinde her hata üç sorudan birine döner:

> 语音系统deki her hata aşağıdaki üç sorunun birinden kaynaklanır:

1. Veriler hangi örnek oranında kaydedildi ve model ne bekliyor?
   Verilerin kayıt çekim oranı ne kadar, model beklenen çekim oranı ne kadar?
2. Sinyal adı gizli mi?
   - Bir karışıklık var mı?
3. Çiğ örnekler üzerinde mi çalışıyorsunuz yoksa frekans temsilleri üzerinde mi?
   Çözümün ne kadar sık olduğunu mu öğrendin?

Bunları doğru yaparsanız, 6. aşamada kalanlar kontrol edilebilir.

> Bu üç sorunun üstesinden gelmek için, 6. aşamada kalanlar kolayca anlaşılabilir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**Bir boyutlu bir sünger arşivinde `[-1.0, 1.0]`. Örnek numarasına göre indeksi. Sekünteler için örneğin oranına bölün: `t = n / sr`16 kHz'de 10 saniyelik bir klip 160.000 dalga ile bir dizi.

> **波形（Waveform）。**Bir değer alıyorum.`[-1.0, 1.0]`间一维浮点数组──以采样编为索引──以秒数转换,除以采样率:`t = n / sr`❖ ❖ 10 saniyelik 16 kHz 音频= 160.000 个浮点数数组──

**Sampling rate (sr).**2026'da ortak oranlar:

> **采样率（sr）。**Her saniye için örnek noktası sayısı: 2026 yılın sürekli örneklemesi oranı:

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.**`sr`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `sr/2`- Ne ?`sr/2`Sınır * Nyquist frekansıdır. Nyquist'in üzerindeki enerji * aliased *  aşağı frekanslara katlanır  ve sinyali bozar.

> **奈奎斯特-香农定理。**采样率 `sr`En yüksek seviyeye kadar ifade edebilirsiniz.`sr/2`Çevreyi sıklıkla kullanmak.`sr/2`边界就是奈奎斯特的能量会被被混叠折叠到更低的频率从而破坏信号──降采前务必先进行低通波──

**Bit depth.**16 bit PCM (salıkonulan int16, aralığı ±32.767) evrensel değişim biçimidir.`soundfile`int16 okuyun ama float32 dizilerini açığa çıkarın `[-1, 1]`- Evet .

> **位深度。**16 位 PCM(有符号 int16,范围 ±32,767) is通用交换格式──音乐用 24 位,内部 DSP用 32 位浮点──`soundfile`İnternal okuyucuyu bekle ama geri dön.`[-1, 1]`范围的浮动32 数组──

**Fourier Transform.**Herhangi bir sınırlı sinyal, farklı frekanslarda sinusoidlerin toplamıdır.`N`örnekler, `N`karmaşık katı  bir frekans bin başına. `bin k`frekans haritaları `k · sr / N`Hz. Büyüklük bu frekansta genişliktir, açı faz.

> **傅里叶变换。**任何有限信号都可分成不同频的正弦波之和──离散里叶变换 (DFT) 对 `N`个采样点计算 `N`个复数系数 个频率 bin 个个 个`bin k`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `k · sr / N`Hz── genişlik bu frekansın genişliği, açı ise bir fazittir──

**FFT.**Hızlı Fourier Değişimi: bir `O(N log N)`DFT algoritması, `N`Her ses kütüphanesi kapının altında FFT kullanır. 16 kHz'de 1024 örnek FFT, 15.6 Hz çözünürlükte 08 kHz'den oluşan 512 kullanılabilir frekans kutuları verir.

> **FFT。**快速里叶变换:当 `N`2'nin,DFT'nin`O(N log N)`算法。 her ses kütlesinin alt katı FFT。16 kHz  下 1024 采样点的 FFT 产生 512 个可用频率 bin,覆盖 08 kHz,分辨率为 15.6 Hz。

**Framing + window.**Bir klipi FFT yapmıyoruz. Tekrar üst üste *frames* (genellikle 25 ms 10 ms hop) olarak keseriz, kenar kesintisizlikleri ortadan kaldırmak için her çerçeveyi bir pencere işlevi (Hann, Hamming) ile çarpırız, sonra her çerçeveyi FFT yapıyoruz. Bu kısa süreli Fourier dönüşümü (STFT).

> **分帧 + 加窗。**Biz tüm ses bölümünü FFT yapmamıyoruz. Bunun yerine, genellikle 25 ms, 10 ms, her seferinde bir pencere işlevi ile FFT yapıyoruz.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
mel-scale
```

## Yapın

### Adım 1: bir klip oku ve dalga şeklini çiz

`code/main.py`Sadece stdlib kullanıyor `wave`Bu modül, demo bağımlılığından kurtulmak için kullanılacak.`soundfile`veya `torchaudio.load`(İkisi de geri dönüyor `(waveform, sr)`Tüpler:

> `code/main.py`仅使用标准库的 `wave`模块以保持演示无依赖.`soundfile`Ya da`torchaudio.load`(两者都回归)`(waveform, sr)`元组):

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Adım 2: Birinci ilkelerden sinüs dalgasını sentez edin

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

440 Hz sinüs (koncert A) 16 kHz'de 1 saniye için 16,000 float.`wave.open(..., "wb")`16 bit PCM kodlamasını kullanıyor.

> 16 kHz 采样率下 440 Hz 正弦波(标准音 A)持续 1 秒是 16,000 个浮点数──使用 `wave.open(..., "wb")`E 16 位 PCM 编码写入──

### Adım 3: DFT'yi el ile hesaplayın

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N²)` için cezalandırılır `N=256`Doğruyu doğrulayan gerçek ses için işe yaramaz.`numpy.fft.rfft`veya `torch.fft.rfft`- Evet .

> `O(N²)`复杂度 对 `N=256`验证正确性还行,对真实音频没有用──实际代码调用 `numpy.fft.rfft`Ya da`torch.fft.rfft`- Evet.

### Dördüncü adım: baskın frekansı bulun

Büyüklük zirvesi endeksi `k_star`frekans haritaları `k_star * sr / N`440 Hz sinüsünde çalıştırmak bin ' de bir zirve gönderir .`440 * N / sr`- Evet .

> 幅度峰值索引 `k_star`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `k_star * sr / N`△ 440 Hz için 正弦波运行`440 * N / sr`处返回峰值──

### Adım 5: isim değiştirmeyi göster

7 kHz sinüsünün 10 kHz'de (Nyquist = 5 kHz) örneklenmesi. 7 kHz ton Nyquist'in üzerinde ve `10 − 7 = 3 kHz`FFT zirvesi 3 kHz'de görünür. Bu klasik isim göstergesidir ve bu nedenle her DAC/ADC gemisi tuğla duvarı düşük geçiş filtre ile gönderir.

> 采样 10 kHz 7 kHz 正弦波(奈奎斯特频率 = 5 kHz) ・7 kHz 音调高于奈奎斯特频率,会折叠到`10 − 7 = 3 kHz`FFT 峰 değeri 3 kHz 处  Bu klasik bir karışım gösterisi, ayrıca her DAC / ADC'nin 壁式低通波器                                                                                                                                                                                                                                           

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da gerçekten göndereceğiniz yığın:

> 2026 yılında siz gerçekten kullanacak teknikler:

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


Karar kuralları: **match sample rate before you match anything else**Whisper 16 kHz mono float32'yi bekliyor. 44.1 kHz stereoyu geçirin ve model bir böcek gibi görünen bir çöp alacaksınız.

> 决策规则:**在匹配其他任何东西之前先匹配采样率**❖ Şapış  期望 16 kHz 单声道浮遊32──传入 44.1 kHz 立体声, model böceği gibi görünüyorsun.

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;




## İndirin . Ürünler .

- Kaydet .`outputs/skill-audio-loader.md`Bu yetenek, ses girişinin aşağıdaki modelin beklentilerine uygun olup olmadığını ve doğru olmayan zamanlarda doğru şekilde örneklemenize yardımcı olur.

> 保存为 `outputs/skill-audio-loader.md`Bu beceri, sesli girişlerin aşağıdaki model beklentilerine uygun olup olmadığını ve uygun olmadığında doğru şekilde tekrar yapıldığını kontrol etmenize yardımcı olur.

## Egzersizler.

1. **Easy.**16 kHz'de 220 Hz + 440 Hz + 880 Hz'in 1 saniyelik bir karışımı sentezleyin. DFT çalıştırın. Beklenen kutularda üç zirveyi onaylayın.
   **简单。**合成 220 Hz + 440 Hz + 880 Hz'in 1 saniye karışık sinyal, 16 kHz 采样率──运行 DFT──确认在预期bin 位置有三个峰值──
2. **Medium.**Sesini 3 saniyelik WAV'da 48 kHz'de kaydet.`torchaudio.transforms.Resample`(anti-aliasing ile), sonra 16 kHz'e naif onarımı kullanarak (her üçüncü örnek).
   **中等。**Kayıt 1 bölüm 3 saniye 48 kHz 语音 WAV──使用 `torchaudio.transforms.Resample`(带抗混叠)降采样到16 kHz,然后用朴素抽取(每隔三个样本取一个)降采样到16 kHz──对两者做FFT──混叠现在出哪里?
3. **Hard.**STFT ' i sadece  kullanarak sıfırdan oluşturun`math`Ve DFT'den 3. Adımdan. Çerçeve boyutu 400, hop 160, Hann penceresi.`matplotlib.pyplot.imshow`Bu 2. Dersin spektrogramı.
   **困难。**Sadece kullanıyorum.`math`和步骤 3 的 DFT 从零构建 STFT──大小 400,步长 160,Hann 窗──用 `matplotlib.pyplot.imshow`Bu, 2. sınıfın frekans çizgisidir.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) örnekleme teoreminin arkasındaki kağıt.
  Shannon (1949) 带噪音条件下的通信采样定理背后的论文──
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) ücretsiz, kanonik DSP ders kitabı.
  Smith'in Bilim adamları ve Mühendisleri'nin Dijital Sinyal İşleme Rehberi
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) Kodla pratik bir yürüyüş.
  Kütüphaneler 文档音频入门带代码的实践教程──
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) Gerçek dünya sesinin neden temiz bir sinusoid olmadığını göstermek için bir referans.
  Heinrich Kuttruff 房间声学(第 6 版) 解释为什么真世界音频不是干净正弦波的参考书──
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/) frekans çubuğu algısı 10 dakika içinde temizlendi.
  Steve Eddins FFT 解读笔记10 分搞清频率 bin 的直觉──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

