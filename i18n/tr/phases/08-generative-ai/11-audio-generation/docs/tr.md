# Ses jenerasyonu 音频生成

> Ses, 16-48 kHz'de 1 boyutlu bir sinyaldir. Beş saniyelik bir klip 80-240k örneklerdir. Hiçbir transformatör bu sıraya doğrudan katılmaz. 2026'da her üretim ses modeli için çözüm aynıdır: bir sinir kodeksi (Encodec, SoundStream, DAC) sesini ayrı jetonlara 50-75 Hz'de sıkıştırır ve bir transformatör veya difüzyon modeli jetonları üretir.

> **【中文解读】**音频是16-48kHz'in 1D 信号,5秒就是8-24万采样点──没有变压器能直接处理如此长的序列──2026年所有音频生成模型的解决方案相同: 神经编码器(EnCodec等) 压缩为50-75Hz的离散代币,然后使用变压器 生成──

> **【拓展：MusicGen 与 AudioCraft】**Meta'nın MusicGen 和 AudioCraft kullanımı EnCodec + Transformer 架构生成音乐和音效──音频代码化 音频生成 alanındaki önemli yeniliktir──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 6 · 02 (Audio Features / 音频特征), Phase 6 · 04 (ASR), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## Sorunlar. Sorunlar.

Üç ses oluşturma görevi:

> Üç sesli üretim görevleri:

1. **Text-to-speech.**Metin verildiğinde konuşma üretin. Temiz konuşma dar bantlıdır ve güçlü fonetik yapısına sahiptir.
   **语音合成。**给定文本生成语音──已有良好的解决──
2. **Music generation.**Bir sürpriz (metin, melodi, akord ilerleme, tür) verildiğinde, müzik üretin. Çok daha geniş dağıtım. MusicGen (Meta), Stable Audio 2.5, Suno v4, Udio, Riffusion.
   **音乐生成。**给定提示(文本、旋律、和弦、流派)生成音乐──分布更广──
3. **Audio effects / sound design.**Bir istekle çevre sesini veya Foley'i üretin.
   **音效/声音设计。**给定提示生成环境音或拟音──

Üçü de aynı altyapıda çalışır: sinir ses kodek + token-AR veya difüzyon jeneratörü.

> Üçü aynı altyapıda çalışmaktadır: Neureus Audio Çözme Aracı + Token Özgürlük veya Genişleme Yükleyici.

> **【中文解读】**音频生成的三大任务语音合成(TTS)、音乐生成、音效生成都基于相同的基础架构:神经音频编解码器(如EnCodec) 音频压缩为离散代币,然后变体或扩散模型在代币序列上生成──

> **【拓展：ElevenLabs 与语音克隆技术】**ElevenLabs 2026'daki en popüler AI 语音平台ıdır. Sadece birkaç saniye süren bir referans sesleri, konuşmacıların sesini kullanıp, sonra da klon'un sesini herhangi bir metni oluşturmak için kullanır. Alt seviyede bir teknoloji olan Nörodelator ve koşul dil modeli.

## Konsepten bir şey.

![Audio generation: codec tokens + transformer or diffusion](../assets/audio-generation.svg)

### Nöral ses kodekleri

Encodec (Meta, 2022), SoundStream (Google, 2021), Descript Audio Codec (DAC, 2023). Bir konvulsyonal kodlayıcı dalga şeklini bir zaman aşaması vektörüne sıkıştırır; kalan vektör kvantizasyonu (RVQ) her vektörü K kod kitabı indekslerinin bir kaskadasına dönüştürür. Dekoder onu tersine çevirir. 24 kHz ses 2 kbps'de 8 RVQ kod kitabı kullanarak 75 Hz = 600 jeton / saniye.

```
waveform (16000 samples/sec)
    └─ encoder conv ─┐
                     ├─ RVQ layer 1 → indices at 75 Hz
                     ├─ RVQ layer 2 → indices at 75 Hz
                     ├─ ...
                     └─ RVQ layer 8
```

### İki jeneratif paradigma üstte

**Token-autoregressive.**Flat RVQ tokensini bir diziye çevirin, sadece bir dekodörle dönüştürücü çalıştırın. MusicGen, K kod defteri akışlarını akış karşılığı ile paralel olarak yaymak için "Gecikmiş paralel" kullanır. VALL-E, bir metin anketinden + 3 saniyelik ses örneğinden konuşma tokensini oluşturur.

**Latent diffusion.**Codec tokenlerini sürekli laten olarak paketleyin veya kategorik difüzyonla modelleyin. Stable Audio 2.5 sürekli ses latenlerinde akış eşleşmesini kullanır. AudioLDM 2 metin-mel-audio difüzyonunu kullanır.

2024-2026 e kadarki trend: akış eşleşimi müzik için kazanıyor (hızlı sonuç, temiz örnekler), token-AR ise doğal olarak nedensel olduğu ve iyi akışladığı için konuşmada hala hakimdir.

## Üretim manzarası

| System | Task | Backbone | Latency |
|--------|------|----------|---------|
| ElevenLabs V3 | TTS | Token-AR + neural vocoder | ~300ms first token |
| OpenAI GPT-4o audio | Full-duplex speech | End-to-end multimodal AR | ~200ms |
| NaturalSpeech 3 | TTS | Latent flow matching | Non-streaming |
| Stable Audio 2.5 | Music / SFX | DiT + flow matching on audio latents | ~10s for 1-minute clip |
| Suno v4 | Full songs | Undisclosed; token-AR suspected | ~30s per song |
| Udio v1.5 | Full songs | Undisclosed | ~30s per song |
| MusicGen 3.3B | Music | Token-AR on Encodec 32kHz | Real-time |
| AudioCraft 2 | Music + SFX | Flow matching | ~5s for 5s clip |
| Riffusion v2 | Music | Spectrogram diffusion | ~10s |

## Yapın.
```figure
score-matching
```

## Yapın

`code/main.py`temel fikri simüle eder: sentetik "audio token" dizilerinde küçük bir sonraki token transformatörü eğitmek iki farklı "stil"den üretilen (A stil için düşük ve yüksek tokenleri, B stil için monoton rampları)

### Adım 1: sentetik ses jetonları

```python
def make_tokens(style, length, vocab_size, rng):
    if style == 0:  # "speech-like": alternating
        return [i % vocab_size for i in range(length)]
    # "music-like": ramp
    return [(i * 3) % vocab_size for i in range(length)]
```

### Adım 2: Küçük bir işaret tahmincisi çalıştır

Bir büyük grafik biçiminde bir tahminci, biçimle koşullanmış.

### Adım 3: Şartlı olarak örnek

Styles token ve bir başlangıç token'ı verildiğinde, tahmin edilen dağıtımdan bir sonraki token'ı örnekleyin. 20-40 token için devam edin.

## Tuzaklar.

- **Codec quality caps output quality.**Eğer kodek sesleri sadakatle temsil edemiyorsa, hiçbir jeneratör kalitesi yardımcı olmaz.
- **RVQ error accumulation.**Her RVQ katmanı önceki katmanın kalıntılarını modellemektedir. Katman 1'deki hatalar çoğalabilir.
- **Musical structure.**30 saniyelik jeton 75 Hz'de 20k+ jetonlardır. Transformatörler için zor. MusicGen kaydırıcı pencere + hızlı devam kullanır; Stable Audio daha kısa klipler + çaprazlama kullanır.
- **Artifacts at boundaries.**Yaratılan klipler arasındaki çarpışma dikkatli bir örtüşme gerektirir.
- **Clean-data appetite.**Müzik jeneratörlerinin on binlerce saat lisanslı müzik ihtiyacı vardır. Suno / Udio RIAA davası (2024) bunu yüzeye çıkardı.
- **Voice cloning ethics.**3 saniyelik bir örnek ve bir metin sorusu, VALL-E / XTTS / ElevenLabs'ın bir ses klonlaması için yeterlidir. Her üretim modeli kötüye kullanımı tespit etmek + seçme listesine ihtiyaç duyar.

## Çerçeveyi kullanın.

| Task / 任务 | 2026 stack / 2026 技术栈 |
|------|------------|
| Commercial TTS / 商业语音合成 | ElevenLabs, OpenAI TTS, or Azure Neural |
| Voice cloning (consent-verified) / 语音克隆 | XTTS v2 (open) or ElevenLabs Pro |
| Background music, fast / 快速背景音乐 | Stable Audio 2.5 API, Suno, or Udio |
| Music with lyrics / 带歌词音乐 | Suno v4 or Udio v1.5 |
| Sound effects / Foley / 音效/拟音 | AudioCraft 2, ElevenLabs SFX, or Stable Audio Open |
| Real-time voice agent / 实时语音代理 | GPT-4o realtime or Gemini Live |
| Open-weights music research / 开源音乐研究 | MusicGen 3.3B, Stable Audio Open 1.0, AudioLDM 2 |
| Dubbing / translation / 配音/翻译 | HeyGen, ElevenLabs Dubbing |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-audio-brief.md`. Skill bir ses kısa ( görev, süresi, tarzı, ses, lisans) ve çıkışları alır: model + hosting, istekli biçim (genre etiketleri, stil tanımlayıcıları, yapısal işaretçiler), kodek + jeneratör + vokoder zinciri, tohum protokolü ve değerleme planı (TTS / kullanıcı A / B için MOS / CLAP puan / CER).

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Yaratılan dizilerin stil örneğine uygun olduğunu kontrol edin.
2. **Medium.**Gecikmiş paralel şifreleme ekleyin: 1 adımla karşılaştırılmalı olan 2 token akışını simüle edin. Ortak bir tahminci çalıştırın.
3. **Hard.**MusicGen-small'ı yerel olarak çalıştırmak için HuggingFace transformatörlerini kullanın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Codec | "Neural compression" | Encoder / decoder for audio; typical output is 50-75 Hz tokens. |
| RVQ | "Residual VQ" | Cascade of K quantizers; each models the residual of the previous. |
| Token | "One codec symbol" | Discrete index into a codebook; 1024 or 2048 typical. |
| Delayed parallel | "Offset codebooks" | Emit K token streams with staggered offsets to reduce sequence length. |
| Flow matching | "The 2024 win for audio" | Straighter-path alternative to diffusion; faster sampling. |
| Voice prompt | "3-second sample" | Speaker embedding or token prefix that steers the cloned voice. |
| Mel spectrogram | "The visual" | Log-magnitude perceptual spectrogram; used by many TTS systems. |
| Vocoder | "Mel to wave" | Neural component that converts mel spectrograms back to audio. |

## Üretim Notu: Ses sesleri akış sorunu.

Ses, kullanıcıların * üretildiği gibi * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

İki mimari sonuç:

- **Flow-matching audio models cannot stream trivially.**Stable Audio 2.5 ve AudioCraft 2 bir geçit içinde sabit bir klip uzunluğu gösterir. Akış için, klipin parçalanmasını ve üst üste geçiş sınırlarını  kaydırma penceresi yayımı  100-300 ms gecikme overhead vs. codec AR modeli ekleme.

Ürün "canlı ses sohbeti" veya "gerçek zamanlı müzik devamı" ise, codec AR yolu seçin. "Yükleyerek 30 saniyelik bir klip ver" ise, akış eşleşimi kalite ve toplam gecikme üzerinde kazanır.

## Daha fazla okumak

- [Défossez et al. (2022). Encodec: High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Kodek standartı.
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) ilk yaygın olarak kullanılan sinir ses kodek.
- [Kumar et al. (2023). High-Fidelity Audio Compression with Improved RVQGAN (DAC)](https://arxiv.org/abs/2306.06546)DAC.
- [Wang et al. (2023). Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (VALL-E)](https://arxiv.org/abs/2301.02111)- VALL-E.
- [Copet et al. (2023). Simple and Controllable Music Generation (MusicGen)](https://arxiv.org/abs/2306.05284) MusicGen.
- [Liu et al. (2023). AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining](https://arxiv.org/abs/2308.05734) AudioLDM 2.
- [Stability AI (2024). Stable Audio 2.5](https://stability.ai/news/introducing-stable-audio-2-5) 2025 akış eşleşmesi ile müziklere metin.
