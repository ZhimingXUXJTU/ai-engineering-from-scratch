# Ses Klonlaması ve Ses Değişimi .

> Ses klonlaması, metnizi başka birinin sesinde okuyor. Ses dönüşümü, sesinizi başka birinin sesine yeniden yazarken söylediğiniz şeyi korur. İkisi de aynı parçalanmaya bağlıdır: konuşmacı kimliğini içeriğinden ayırır.

> **【中文解读】**语音克隆 başkalarının sesini kullanarak yazını okuyun;语音转换把你的声音变成别人的但保留内容──; bu iki şeyin merkezi aynı ayrıntıdır:

> **【拓展：语音克隆的伦理与法律】**语音克隆技术引发严重伦理和法律问题深度伪造语音诈骗、名人声音未经授权使用──2025-2026 yıllarca dava açılması( Warner Music gibi 5 milyar dolarlık anlaşma davaları)

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

2026 yılında, bir tüketici GPU ile herkesin sesinin yüksek kaliteli bir klonunu üretmek için 5 saniyelik bir ses klipi yeterlidir. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox hepsi sıfır çekim veya birkaç çekim klonlamasını gönderir. Teknoloji bir nimettir (erkinlik TTS, dublajlama, yardımcı sesler) ve bir silah (scam aramaları, siyasi derin sahtekarlıklar, IP hırsızlığı).

> 2026 yıl, bir 5 saniye 音频 on enough to use consumption grade GPU 高质量克隆任何人的声音──ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox 都提供零样本或少样本克隆── bu teknik hem İncil(无障碍 TTS、配音、辅助声音), hem de bir silah(cinsel sahtekarlık telefon、政治深度伪造、知识产权盗窃)──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

İki yakın bağlantılı görev:

> İki yakın ilişkili görev:

- **Voice cloning (TTS-side):**Metin + 5 saniye referans sesi → ses bu sesde.
  **声音克隆（TTS 侧）：**文本 + 5 秒参照音 → The sound's audio
- **Voice conversion (speech-side):**Kaynak ses ( kişi A'nın X'i söyleyerek) + kişi B'nin referans sesi → B'nin X'i söyleyerek ses.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

Her ikisi de dalga şeklini ( içeriği, hoparlör, prosodi) oluşturur ve bir kaynaktan hoparlörle diğerinden içeriği yeniden birleştirir.

> 两者都将波形分解为(内容、说话人、律) 并从一个来源取内容与另一来源的说话人重新组合──

2026 ' da şimdi gemiye gireceğiniz temel bir kısıtlama:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**- Boru hattınız sessiz bir su işaretini yaymalı ve konsensüs dışı klonları reddetmeli.

> 2026 yılında karşılaştığınız önemli bir şey var:**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的**Su akımının işitilmez bir iz bırakması ve onaylanmamış bir şekilde kabul edilmesini reddetmesi gerekir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**Binlerce hoparlör üzerinde eğitilmiş bir modele 5 saniyelik bir klip geçirin. Konuşmacı kodlayıcı klipini hoparlör yerleştirme kartı yapar; TTS dekodörü bu yerleştirme ek metinde koşullar oluşturur.

> **零样本克隆。**5 saniyelik sesli yayın, binlerce konuşmacı üzerinde eğitilmiş bir modelle aktarılacak.

F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024) tarafından kullanılır.

> İstifadeden kullanıcı:F5-TTS(2024)、YurTTS(2022)、XTTS v2(2024)、OpenVoice v2(2024)。

**Few-shot fine-tuning.**Bu nedenle, bu programın en iyi yönü, bir saatlik bir süre için bir temel modelin ayarlanmasıdır.

> **少样本微调。**录制目标声音 5-30 分钟──LoRA 微调基础模型一小时──质量从"还行"跳到"无法区分"──Coqui 和 ElevenLabs 都支持这种模式;社区用F5-TTS 实现──

**Voice conversion (VC).**İki aile:

> **语音转换（VC）。**İki aile:

- **Recognition-synthesis.**İçerik temsilini çıkarmak için ASR benzeri bir model çalıştırın (örneğin yumuşak fonem pozteriyeleri, PPG), sonra hedef hoparlör yerleştirme ile yeniden sentez edin. Dil ve aksan için sağlam. KNN-VC (2023), Diff-HierVC (2023) tarafından kullanılır.
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG), sonra hedef konuşma insanına yerleştirilmiş yeniden sentezleştirilmiştir.
- **Disentanglement.**İçerik, hoparlör ve prosodiyi şişek boynunda gizli bir alanda ayıran bir oto-kodlayıcı eğit. Sonucunda hoparlör yerleştirme. Daha düşük kalite ama daha hızlı. AutoVC (2019), VITS-VC çeşitleri tarafından kullanılır.
  **解耦。**訓練自编码器在瓶处的潜在空间中分离内容、言論者和律──推理时交换言論者嵌入──質量较低但更快──AutoVC(2019)、VITS-VC 变体使用──

**Neural codec-based cloning (2024+).**VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox  sesleri SoundStream / EnCodec'den ayrı bir token olarak değerlendirir, kodek tokenlerine karşı büyük bir autoregressive veya akış eşleşme modeli eğitir.

> **基于神经编解码器的克隆（2024+）。**VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox will音频视为 SoundStream/EnCodec'ın ayrıştırılmış simgesi,编解码 token 上训练大型自归归或流匹配模型──短提示上质量可与ElevenLabs相当──

### Etik kısım, bir şapka değil.

> ### 伦理问题,选项不是

**Watermarking.**PerTh (Perth) ve SilentCipher (2024) sesle ~16-32 bit bir ID'yi fark edilemez şekilde yerleştirir. Yeniden kodlama, akış ve ortak düzenlemeler hayatta kalır. Üretim hazır açık kaynak.

> **水印。**PerTh 和 SilentCipher(2024) ses yayında algılanamaz şekilde yerleştirilmiş yaklaşık 16-32 sit ID──能经受重新编码、流传输和常见编辑──生产可用开源方案──

**Consent gates.**Her klon edilmiş çıkışın doğrulanabilir bir onay kaydı ile eşleştirilmesi gerekir. "Ben, Rohit, 2026-04-22'de bu sesin X amaçlı yetkisi veriliyor".

> **同意门。**Her bir klon çıkışı bir onaylanmış onay kayıtına bağlı olmalıdır.

**Detection.**AASIST, RawNet2 ve Wav2Vec2-AASIST, detektör olarak gemiyi gönderdi. ASVspoof 2025 meydan okuma, ElevenLabs, VALL-E 2 ve Bark çıkışlarına karşı en son detektörler için 0.82.3% EER'leri yayınladı.

> **检测。**AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布──ASVspoof 2025 挑战赛 SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为0.8-2.3%──

### Sayılar (2026)

> 2026 yılının sayısı

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.


SECS > 0,70 çoğu dinleyiciler için hedeften genel olarak ayırt edilemez.

> SECS > 0.70 çoğunluk için genellikle hedef ile ayırt edilemez.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.
```figure
sp-voice-factorize
```

## Yapın

### Adım 1: Tanım-sentez ile parçalan (main.py'de sadece kodla gösterim)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Konseptik olarak basit; uygulama kütlesi `tts_model`Ve hoparlör kodlayıcı.

> 概念上简单; 实现量在`tts_model`Söyleyin, bu bir şey.

### Adım 2: F5-TTS ile sıfır atışlı klon

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

Referans transkripti sesle tam olarak eşleşmelidir; eşleşme uyumsuzluğu keser.

> 引用转录必须与音频完全匹配;不匹配将破坏对齐──

### Adım 3: KNN-VC ile ses dönüşümü

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC, kaynak ve hedef havuz için çerçeve içeriklerini çıkarmak için WavLM'i çalıştıracak, ardından her kaynak çerçeveyi havuzdaki en yakın komşusuyla değiştirir.

> KNN-VC 运行 WavLM 提取源和目标池的逐嵌入, sonra池中近邻的接替每个源──非参数化,一分钟目标语音即可工作──

### Dördüncü adım: Su işaretini yerleştir

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~ 32 bit yararlı yük, MP3 yeniden kodlaması ve hafif gürültüden sonra tespit edilebilir.

> Yaklaşık 32 位 yük, MP3 ağırlıklı kodlama ve hafif gürültü sonrası kontrol edilebilir.

### Adım 5: İzn verme kapısı

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Tuzaklar

> 常见陷

- **Misaligned reference transcript.**F5-TTS ve benzeri, referans metnini, noktalama dahil olmak üzere referans sesine tam olarak eşleştirmesini gerektirir.
  **参考转录不对齐。**F5-TTS等 referans metni ile referans ses ses sesleri tam uyumlu olmak üzere, işaret noktasını içerir.
- **Reverberant reference.**Echo klonu öldürür.
  **混响参考。**Bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir de sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir sesle bir bir sesle bir sesle bir bir sesle bir bir bir sesle bir bir sesle bir bir bir sesle bir bir bir bir sesle
- **Emotional mismatch.**Eğitim referansı "sevinçli" her şeyin sevinçli klonlarını üretir.
  **情感不匹配。**訓練参考"欢快" tüm içerikleri oluşturur 欢快克隆。 匹配参考情感与目标用途。
- **Language leakage.**İngilizce konuşan bir kişiyi klonlamak ve modelden Fransızca konuşmasını istemek genellikle aksanı taşır; diller arası modeller kullanın (XTTS, VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍将带有口音;跨语言模型的使用; XTS, VALL-E X) ⋅
- **No watermark.**2026 Ağustos'tan itibaren AB'de yasal olarak gönderilemez.
  **没有水印。**2026 yılının Ağustos ayından itibaren AB'de yasak olarak yayınlanamaz.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-voice-cloner.md`. İzin verme kapısı + su işaretleri + kalite hedefi ile klonlama veya dönüşüm boru hattı tasarlayın.

> 保存为 `outputs/skill-voice-cloner.md`◊ tasarımla onaylı门 + 水印 + 质量目标的克隆或转换流水线──

## Egzersizler.

1. **Easy.**Çık .`code/main.py`. Konuşmacı-içerilen değişimi iki "düşenç" arasındaki kosinus'u hesaplayarak gösterir.
   **简单。**运行  İşlem`code/main.py`❖ hesaplama işleminden sonra iki " konuşmacı " nin öyüdünün benzerliği konuşmacıyı birleştirme işlemine sunar.
2. **Medium.**OpenVoice v2'yi kullanarak kendi sesini klonlayın. Referans ve klon arasındaki SECS'i ölçün.
   **中等。**Bu yüzden, bu durumla ilgili bir görüşme yaparak, bu görüşme hakkında bir görüşme yaparak,
3. **Hard.**SilentCipher su işaretini 20 klona uygulayın, 128 kbps MP3 kodlama + çözümü ile çalıştırın, yararlı yükü tespit edin.
   **困难。**SilentCipher Su basımı için 20 个克隆应用,通过 128 kbps MP3编码+解码,检测载荷――报告比特准确率――

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) Açık kaynaklı SOTA sıfır çekim klonlaması.
  Chen 等 (2024). F5-TTS开源 SOTA 零样本克隆──
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)ve [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) Nöral kodek TTS.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2(2024)  神经编解码 TTS──
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) Çelişki tabanlı ses dönüşümü.
  Qian 等 (2019). AutoVC 基于解的语音转换──
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) Arama tabanlı VC.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC基于检索的语音转换──
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) 32 bitlik ses su işaretleri üretime hazır.
  SilentCipher(2024) 音频水印生产可用 32 位音频水印──
- [ASVspoof 2025 results](https://www.asvspoof.org/) Detektor vs. sentesizer silah yarışı, 2026'da güncellenmiştir.
  ASVspoof 2025 结果检测器 vs 合成器 silahlı birim yarışması,2026年更新。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

