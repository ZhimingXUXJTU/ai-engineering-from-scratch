# Neural Audio Codecs  EnCodec, SNAC, Mimi, DAC ve Semantic-Acoustic Split

> 2026 ses jenerasyonu neredeyse tüm jetonlardır. EnCodec, SNAC, Mimi ve DAC, sürekli dalga formlarını bir transformatör tarafından tahmin edilebilen ayrı sıralara dönüştürürler.

> **【中文解读】**2026 yılının ses üretimi neredeyse her şey simge üzerine kurulu. EnCodec、SNAC、Mimi、DAC, Transformer'in öngörülebilmesi için ayrı bir dizi olarak değişecek.

> **【拓展：音频 token 化】**Tıpkı metin gibi BPE tokenizer, metin bir tokene dönüşecek, ses ses sesleri bir EnCodec gibi bir kodlayıcı, ses ses seslerini bir tokene dönüştürecek. Bu da ses sesleri metin gibi büyük dil modeline göre işlenmeye yardımcı olacaktır.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 10 · 11 (Quantization), Phase 5 · 19 (Subword Tokenization) | **前置知识:** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## Sorunlar. Sorunlar.

Dil modelleri ayrı belirtiler üzerinde çalışır. Ses süreklidir. Konuşma / müzik için LLM tarzında bir model istiyorsanız  MusicGen, Moshi, Sesame CSM, VibeVoice, Orpheus  önce bir **neural audio codec**: sesleri küçük bir token kelime birikimine ayırt eden öğrenilmiş bir kodlayıcı ve dalga şeklini yeniden oluşturan eşleşen bir dekoder.

> 语言模型处理离散 token──音频是连续的── eğer siz de语音/音乐 için düşünüyorsanız LLM 风格的模型MusicGen、Moshi、Sesame CSM、VibeVoice、Orpheus你首先需要一个**神经音频编解码器**Bir öğrenme kodlayıcı, ses ses sesini küçük bir kelime göstergesi olarak ayırır.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

İki aile ortaya çıktı:

> İki aile ortaya çıktı:

1. **Reconstruction-first codecs** EnCodec, DAC. Algılama ses kalitesini optimize edin. Tokenler "akustik"  konuşmacı kimliği, timbre, arka plan gürültüsü dahil her şeyi yakalar.
   **重建优先编解码器**EnCodec、DAC──优化感知音频质量──Token is "声学学"它们捕获一切,包括说话人身份、音色、背景噪声──
2. **Semantic-first codecs** Mimi (Kyutai), SpeechTokenizer. İlk kod kitabı dil / fonetik içeriği kodlamaya zorlar (sık sık WavLM'den destilleyerek).
   **语义优先编解码器**Mimi(Kyutai)、SpeechTokenizer。强制第一个码本编码语言/语音内容(通常通过从波LM 蒸)。后续码本是声学细节。

2024-2026 yıllarındaki görüşler: **a pure reconstruction codec gives you blurry speech when you try to generate from text.**Kodek simgelerinin üzerine LLM, aynı kod defterinde hem dil yapısını hem de akustik yapısını öğrenmek zorunda.

> 2024-2026 yıllarındaki anlayış:**纯重建编解码器在从文本生成时给你模糊的语音。**编解码代币 上的LLM 必须同时学习语言结构和声学结构在同一码本中,这无法扩展──将它们分离语义码本0,声学码本1-N正是Moshi 和芝麻CSM başarısının anahtarı──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Four codec landscape: EnCodec, DAC, SNAC (multi-scale), Mimi (semantic+acoustic)](../assets/codec-comparison.svg)

### Temel numara: Geri kalan vektör kvantizasyonu (RVQ)

Bir büyük kod defteri yerine (iyi kalite için milyonlarca kod gerekecek) tüm modern ses kodekleri kullanır **RVQ**: küçük kod defterlerinin bir kaskasası. Birinci kod defterinde kodlayıcı çıkışı, ikincisi kalıntılı kalıntıları kuantleştirir.

> Büyük bir kod kullanmak yerine, tüm modern sesli kodlama cihazları kullanılıyor.**RVQ**Birinci kod kendiliğinden kodlayıcı çıkışı; ikinci kodsal gerideği; bu tür önerilerde bulunur.

Sonuçlama sırasında, dekodör yeniden yapılandırmak için seçilen tüm kodları çerçeve başına toplamlar.

> Bu durumda, çözücü her seçilen tüm kodları yeniden inşa edecek.

### 2026'da önemli olan dört kodek

**EnCodec (Meta, 2022).**Baseline. Gelgen şekli üzerinde kodlayıcı-dekoder, RVQ şişe boynuzu. 24 kHz, 32 kod defteri mümkün, varsayılan 4 kod defteri @ 1.5 kbps. Kullanım `1D conv + transformer + 1D conv`MusicGen tarafından kullanılıyor.

> **EnCodec（Meta，2022）。**基线──波形上的编码器-解码器,RVQ 瓶──24 kHz, en fazla 32 个码本,默认 4 个码本 @ 1.5 kbps──使用 `1D conv + transformer + 1D conv`架构──MusicGen 使用──

**DAC (Descript, 2023).**RVQ, L2 normallaştırılmış kod defterleri, dönemi etkinleştirme fonksiyonları, iyileştirilmiş kayıplar. Herhangi bir açık kodek için en yüksek yeniden yapılandırma sadakati  bazen 12 kod defterle orijinal konuşmadan ayırt edilemez. 44.1 kHz tam bant.

> **DAC（Descript，2023）。**L2 归化码本、周期性激活函数和改进损失的RVQ──开源编码器中重建保真度最高12个码本时有时与原始语音无法区分──44.1 kHz 全频带──

**SNAC (Hubert Siuzdak, 2024).**Çok ölçekli RVQ  kaba kod defterleri ince olanlardan daha düşük bir çerçeve hızında çalışır. Etkili bir şekilde ses hiyerarşik olarak modellendirir: ~ 12 Hz'de kaba bir "sketch" artı 50 Hz'de ayrıntı. Orpheus-3B tarafından kullanılır çünkü hiyerarşik yapısı LM tabanlı jenerasyona iyi haritası yapar.

> **SNAC（Hubert Siuzdak，2024）。**Çok boyutlu RVQ kaba kod kullanımı, küçük kod kullanımı oranından daha düşük  oranında çalışır.

**Mimi (Kyutai, 2024).**2026 oyun değiştiricisi. 12.5 Hz çerçeve hızı (çok düşük), 8 kod kitabı @ 4.4 kbps.**distilled from WavLM**WavLM'in konuşma içeriği özelliklerini tahmin etmek için eğitilmiştir. 1-7 kod kitabı akustik kalıntılardır. Bu bölünme Moshi (Daabi 15) ve Sesame CSM güçlendiriyor.

> **Mimi（Kyutai，2024）。**2026 yılının oyun kuralları değiştiricisi──12.5 Hz 率(极低),8 个码本 @ 4.4 kbps──码本 0 **从 WavLM 蒸馏** training to predict WavLM'in语音内容特征──码本 1-7 声学残差──这种分离驱动了Moshi(第15 课) 和芝麻CSM──

### Çerçeve oranları dil modelleme için önemli

Daha düşük çerçeve hızı = daha kısa dizi = daha hızlı LM.

> 率对语言建模很重要: 率越低 = 序列越短 = LM 越快──

| Codec | Frame rate | 1 s = N frames | Good for |
|-------|-----------|----------------|---------|
| EnCodec-24k | 75 Hz | 75 | music, general audio |
| DAC-44.1k | 86 Hz | 86 | high-fidelity music |
| SNAC-24k (coarse) | ~12 Hz | 12 | AR-LM efficient |
| Mimi | 12.5 Hz | 12.5 | streaming speech |

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适用场景 |
|---------|------|------------|---------|
| EnCodec-24k | 75 Hz | 75 | 音乐、通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗） | ~12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

12.5 Hz'de, 10 saniyelik bir ifadeler sadece 125 kodek çerçevesidir.

> 12.5 Hz                                                                                                                                                                                                                                                              

### Semantik vs. Akustik Token

> 语义 vs 声学 işaretleri

```
frame_t → [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **Semantic token (codebook 0 in Mimi).**Söylenenleri kodlar  fonemleri, kelimeler, içerik.
  **语义 token（Mimi 中的码本 0）。**编码说了什么音素、单词、内容──通过辅助预测损失从波LM 蒸──
- **Acoustic tokens (codebooks 1-7).**Kodlama timbre, hoparlör kimliği, prosody, arka plan gürültüsü, ince detaylar.
  **声学 token（码本 1-7）。**编码音色、说话人身份、律、背景噪音、精细细节──

Bir AR LM önce semantik simgeyi (metin üzerine koşullanmış) tahmin eder, sonra akustik simgeyi (semantik + hoparlör referansı üzerine koşullanmış) tahmin eder. Bu faktörleşme modern TTS'nin sıfır çekim klon seslerinin nedenini gösterir: semantik model içeriği ele alır; akustik model timbreyi ele alır.

> Öz归归 LM 先预测语义符号(以文本为条件),再预测语学符号(以语义 + 说话人参考为条件) ・・・这种分解正是现代 TTS 能够零样本克隆声音的原因:语义模型处理内容,声学模型处理音色。

### 2026 yeniden inşaat kalitesi (sekonda bitler, daha düşük bit hızı daha iyidir)

| Codec | Bitrate | PESQ | ViSQOL |
|-------|---------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

| 编解码器 | 比特率 | PESQ | ViSQOL |
|---------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

Opus gibi geleneksel kodekler hala algısal kalitede bit başına kazanıyor.**discrete tokens**(Opus üretmediği) ve **generative-model quality**(LM'nin bu tokenlerle ne yapabileceği).

> 傳統編解碼器 (Opus gibi) her bit algılama kalitesinde hâlâ üstünlük kazanıyor.**离散 token**(Opus 不产生)**生成模型质量**Bu işaretlerle ne yapabilirim?

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
rvq-codec-cascade
```

## Yapın

### Adım 1: EnCodec ile kodlayın

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

`n_codebooks=8`Her kod 0-1023 (10 bit)

> 6 kbps 下 `n_codebooks=8`❖ Her kod取值 0-1023(10 比特)

### Adım 2: Deşifreleme ve yeniden ölçüm

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### Adım 3: semantik-akustik bölünme (Mimi tarzı)

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

Semantik kod defteri 0 WavLM ile uyumludur. Bir metin-semantik transformatörü  doğrudan seslere gitmekten çok daha küçük bir kelime birikimi eğitmek için.

> 语义码本 0 与 WavLM 对齐──你可以训练一个文本→语义 Transformer词表比直接到音频小得多──然后一个独立的声学→波形解码器以说话人参考为条件──

### Adım 4: neden AR LM kodek simgelerinden çalışıyor

Mimi'nin 12.5 Hz × 8 kod defterinde 10 saniyelik bir konuşma klipi için:

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


1000 token, bir transformatör için önemsiz bir bağlamdır. 256M parametre transformatörü modern bir GPU'da milisaniyede 10 saniye konuşma üretebilir.

> 1000 tane Transformer için küçük bir token. 2.56 milyar parametrelik bir Transformer modern GPU'da birkaç saniyede 10 saniyelik bir ses üretir.




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

Harita sorunu → kodek:

| Task | Codec |
|------|-------|
| General music generation | EnCodec-24k |
| Highest-fidelity reconstruction | DAC-44.1k |
| AR LM over speech (TTS) | SNAC or Mimi |
| Streaming full-duplex speech | Mimi (12.5 Hz) |
| Sound-effect library with text | EnCodec + T5 condition |
| Fine-grained audio editing | DAC + inpainting |

| 任务 | 编解码器 |
|------|---------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 文本驱动的音效库 | EnCodec + T5 条件 |
| 细粒度音频编辑 | DAC + 内画 |

Başparmak kuralı: **if you're building a generative model, start with Mimi or SNAC. If you're building a compression pipeline, use Opus.**

> 经验法则:**如果你在构建生成模型，从 Mimi 或 SNAC 开始。如果在构建压缩流水线，使用 Opus。**



## Tuzaklar

- **Too many codebooks.**Kod defterlerini eklemek sadakatini doğrusal olarak arttırır ama LM dizisi uzunluğu da doğrusal olarak.
  **码本过多。**增加码本会线性提高保真度, fakat LM 序列长度也线性增长──停在8-12──
- **Frame-rate mismatch.**LM'yi 12.5 Hz'de eğitmek Mimi, sonra 50 Hz EnCodec'de ince ayarlama sessizce başarısız olur.
  **帧率不匹配。**12.5 Hz Mimi'ye LM'yi eğit, sonra 50 Hz EnCodec'e git.
- **Assuming all codebooks equal.**Mimi'de 0 kod kitabı içeriği taşır; kaybetmek anlayışını yok eder.
  **假设所有码本同等重要。**Mimi'de, kod kod 0  taşıyor; kayboluyor, anlaşılabilirliği bozacak.
- **Using reconstruction quality as the only metric.**Bir kodek büyük bir yeniden yapılandırmaya sahip olabilir ama semantik yapısı kötüse LM tabanlı nesil için işe yaramaz.
  **仅用重建质量作为唯一指标。**Bir kodlayıcı yeniden yapılandırma kalitesi iyi olabilir, ancak ifadeler farklı ise, LM tabanlı üretime hiç gerek yoktur.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-codec-picker.md`- Verilen bir generatif veya sıkıştırma görevi için bir kodek seçin.

> 保存为 `outputs/skill-codec-picker.md`❖ belirli bir üretim veya sıkıştırma görevi için seçmek ❖

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Oyuncak skalar + kalan kuantitörü uyguluyor ve kod defterlerini eklerken yeniden yapılandırma hatasını ölçüyor.
   **简单。**运行  İşlem`code/main.py` Bu bir oyuncak ölçüm + geride kalan ölçüm cihazı gerçekleştirdi, ölçüm kodın artışıyla yeniden inşaat hataları ile birlikte.
2. **Medium.**Kurulum`encodec`Ve 1, 4, 8, 32 kod defteriyi uzun süreli konuşma klipinde karşılaştırın.
   **中等。**- Yapımcılık`encodec`, 1⁄4, 8⁄32 个码本, PESQ veya MSE vs 比特率,
3. **Hard.**Mimi'yi yükle. Bir klip kodla. Kodu 0'yu rastgele tam sayılarla değiştirin; dekode edin. Sonra Kodu 7'yi benzer şekilde değiştirin.
   **困难。**Üzerinde bir parça ses sesli yayın var. Üzerinde bir parça sesli yayın var. Üzerinde bir parça sesli yayın var.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RVQ | Residual quantization | Cascade of small codebooks; each quantizes the previous residual. |
| Frame rate | Codec speed | How many token-frames per second. Lower = faster LM. |
| Semantic codebook | Codebook 0 (Mimi) | Codebook distilled from SSL features; encodes content. |
| Acoustic codebooks | Everything else | Timbre, prosody, noise, fine detail. |
| PESQ / ViSQOL | Perceptual quality | Objective metrics correlating with MOS. |
| EnCodec | Meta codec | The RVQ baseline; used by MusicGen. |
| Mimi | Kyutai codec | 12.5 Hz frame rate; semantic-acoustic split; powers Moshi. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其余所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Défossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) RVQ başlangıç çizgisi.
  Defossez 等 (2023). EnCodecRVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546)En yüksek sadakatle açık.
  Kumar 等 (2023). DAC最高保真开源编解码器──
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) Çok ölçekli RVQ.
  Siuzdak (2024). SNAC多尺度 RVQ──
- [Kyutai (2024). Mimi codec](https://kyutai.org/codec-explainer) semantik-akistik bölünme, WavLM destillasyonu.
  Kyutai (2024). Mimi 编解码器语义-声学分离,WavLM 蒸。
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) iki aşamalı semantik/akustik paradigma.
  Borsos 等 (2023). AudioLM两阶段语义/声学范式──
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) orijinal akışlanabilir RVQ kodek.
  Zenginlik ve diğerleri (2021).

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

