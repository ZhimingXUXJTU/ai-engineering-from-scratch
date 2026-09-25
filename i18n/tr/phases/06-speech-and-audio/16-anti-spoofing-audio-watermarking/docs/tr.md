# Ses Anti-Spoofing & Audio Watermarking  ASVspoof 5, AudioSeal, WaveVerify 语音防伪与音频水印

> Ses klonlaması savunmadan daha hızlı gönderildi. 2026 üretim ses sistemlerinin iki şeye ihtiyacı var: gerçek ve sahte konuşmayı sınıflandıran bir detektör (AASIST, RawNet2) ve sıkıştırmayı ve düzenlemeyi sağlayan bir su işaretisi (AudioSeal).

> **【中文解读】**语音克隆技术跑在防防前面──2026 Yılın üretim sınıfı ses sistemi iki şey gerektirir: tester (AASIST、RawNet2) 区分真假语音,水印 (AudioSeal) 压缩 ve düzenleme sonrasında hala canlı olabilir──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

Üç ilgili savunma:

> Üç çeşit savunma aracı:

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


1. **Anti-spoofing / deepfake detection.**Bir ses klipi verildiğinde, sentetik mi gerçek mi? ASVspoof referansları (ASVspoof 2019 → 2021 → 5) altın standarttır.
   Çeviri:**反欺骗/深度伪造检测。**给定一段音频,判断它是合成的还是真实的?ASVspoof 基准测试(ASVspoof 2019 → 2021 → 5)
2. **Audio watermarking.**Sonradan bir detektörün çıkarması için üretilen seslere algılanabilir bir sinyal yerleştirin.
   Çeviri:**音频水印。**Geliştirilen ses ses dalgalarında yerleştirilen algılanamayan sinyaller, test cihazı sonrasında çıkarabilir.
3. **Authenticated provenance.**Ses dosyalarının + metadataların şifreleme imzası. C2PA / İçerik Doğruluk Girişimi.
   Çeviri:**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

Ardından, bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin de kullanımı ile ilgili olarak, bir diğer sistemin de diğer sistemin de kullanımı ile ilgili olarak, bir diğer sistemin de bu sistemin de kullanımı ile ilgili olarak, bir diğer sistemin de diğer sistemin de diğer sistemin de kullanımı ile, bir diğer diğer sistemin de diğer sistemin de de diğer sistemin de de de diğer sistemlerin de kullanımı ile, diğer sistemlerin de dahil olmak üzere, bir diğer diğer diğerleri de diğerleri de, diğerleri de, diğerleri de de de diğerleri de dahil olmak üzere, diğer diğer diğerleri de diğerleri de, diğerleri de dahil olmak üzere, sistemlerin de, diğerleri de dahil olmak üzere, diğer diğer diğer diğer diğer diğer diğerleri de diğerleri de, diğerleri de dahil olmak üzere,

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026 yılın ikisinin de olması gerekir──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5  2024-2025 referans değerleri

> ASVspoof 5  2024-2025 yıl基准测试

Önceki baskılardaki en büyük değişiklik:

> Önceki sürümlere göre en büyük değişiklik:

- **Crowdsourced data**(stüdyodan temiz değil)  gerçekçi koşullar.
  Çeviri:**众包数据**(非录音棚纯净数据)
- **~2000 speakers**(Bundan önce 100'e karşı).
  Çeviri:**约 2000 名说话人**(Büyük 100 kişi)
- **32 attack algorithms.**TTS + ses dönüşümü + karşıtlık rahatsızlığı.
  Çeviri:**32 种攻击算法。**TTS + 语音转换 + 对抗性扰动──
- **Two tracks.**Karşı önlem (CM) bağımsız tespit; biyometrik sistemler için sahte-güçlü ASV (SASV).
  Çeviri:**两个赛道。**Çözüm: (CM) bağımsız inceleme; (SASV)

ABD'de 5'de en son teknoloji: ~ 7.23% EER. Eski ABD'de 2019 LA: 0.42% EER. Gerçek dünyadaki dağıtım: vahşi kliplerde 5-10% EER bekleyin.

> ASVspoof 5 上的 SOTA: yaklaşık 7.23% EER──在较旧 ASVspoof 2019 LA 上:0.42% EER──实际部署:预期在野外音频上 EER为 5-10%──

### AASIST ve RawNet2  tespit model aileleri

> AASIST 和 RawNet2  检测模型家族

**AASIST**(Yüzde 2021'de, 2026'a kadar güncelleştirilmiştir). Spektral özelliklere grafik-aramak.

> **AASIST**(Yeni yıl, 2026 yılına kadar devam eden güncelleme) ◊ Sıkıntılı kaynaktan kaynaklanan bir çizimleme makinesi ◊ ASVspoof 5 Anti-Message görevlerinin mevcut SOTA ◊

**RawNet2.**Çürüklü ön uç, çiğ dalga şekli + TDNN omurgası. Baseline daha basit; ince ayarlama ile rekabetçi.

> **RawNet2。**İlk dalga şeklinde devreler + TDNN 骨干网络── daha basit bir temel çizgi; küçük düzenler hala rekabet gücü vardır──

**NeXt-TDNN + SSL features.**2025 varianti: ECAPA tarzı + WavLM özellikleri + odak kaybı. ASVspoof 2019 LA'da % 0.42% EER'e ulaşır.

> **NeXt-TDNN + SSL 特征。**2025年变体:ECAPA 风格 + WavLM Özellikleri + odak kaybı──在 ASVspoof 2019 LA 上達 0.42% EER──

### AudioSeal  2024 su işaretinin varsayılan

> AudioSeal  2024 yılının su immi kararı

Meta'lar **AudioSeal**(Ocak 2024, v0.2 Aralık 2024) Ana tasarım:

> Meta **AudioSeal**(v0.2 于 2024 年 12 月) ⋅Közel tasarım:

- **Localized.**Su işaretini 16 kHz (1/16000 s) örnek çözünürlüğünde bir çerçeve başına algılar.
  Çeviri:**局部化。**采样分辨率逐检测水印 ((1/16000 秒) ⋅
- **Generator + detector jointly trained.**Generatör işitilmeyen sinyal eklemeyi öğrenir. Detektor da onu artırmalar yoluyla bulmayı öğrenir.
  Çeviri:**生成器 + 检测器联合训练。**Çözüm cihazı öğrenme, işitilmez sinyallere yerleştirilme; denetçi öğrenme, onu bulmayı güçlendirerek öğrenir.
- **Robust.**MP3 / AAC sıkıştırması, EQ, hız değişimi ± 10%, gürültü karışımı + 10 dB SNR hayatta.
  Çeviri:**鲁棒。**能经受 MP3/AAC 压缩、均衡、±10% 变速、+10 dB SNR 噪声混合──
- **Fast.**Detektor gerçek zamanlı 485x hızla çalışır. WavMark'tan 1000x daha hızlı.
  Çeviri:**快速。**检测器 485 倍实时速度运行; WavMark 快 1000 倍比
- **Capacity.**16 bitlik payload (model ID'yi kodlayabilir, jenerasyon zaman damgası, kullanıcı ID) her ifadede yerleştirilebilir.
  Çeviri:**容量。**16 位载荷(可编码模型 ID、生成时间、用户 ID)

### WavMark

AudioSeal'den önceki açık tabanlı, tersine çevirilebilir sinir ağı, 32 bit/sek.

> AudioSeal 之前的开源基线──可逆神经网络,32 位/秒──问题:

- Sinkronizeci güç yavaş.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Gaussian gürültüsü veya MP3 sıkıştırması ile çıkarılabilir.
  Çinçe Çevirimi: 可被高斯噪声或 MP3 压缩删除──
- Gerçek zamanlı dostluk değil.
  Çin Çeviri:不适合实时场景

### WaveVerify ( Temmuz 2025)

AudioSeal'in zayıflıklarını giderir  Özellikle zamansal manipülasyonlar (dönüştürme, hız). FiLM tabanlı jeneratör + Uzmanların Karıştırması detektörü kullanır. Standart saldırılar için AudioSeal ile rekabetçi; zamansal düzenlemeleri işliyor.

> WaveVerify(2025 yıl 7 月) ―― çöz AudioSeal'ın zayıf noktaları özellikle zaman operasyonları反转、变速) ―― FiLM'e dayalı bir jeneratör + MoE 检测器 kullanmak.

### Düşmanlar açığı kullanıyor

AudioMarkBench'ten: "Pitch shift altında, tüm su işaretleri Bit Recovery Düzgünlüğünü 0.6'dan aşağı gösterir. Bu neredeyse tamamlanmış kaldırımı gösterir". **Pitch-shift is the universal attack.**No 2026 su işaretleri agresif bir yükseklik değiştirmesine tamamen dayanıklıdır. Bu nedenle su işaretleri ile birlikte algılama (AASIST) gereklidir.

> 攻击者利用的漏洞── 来自 AudioMarkBench:"音高偏移下, tüm su izlerinin yeniden kurulması doğruluğu oranı 0.6'dan düşük, neredeyse tamamen silinmiş olduğunu göstermektedir".""**音高偏移是通用攻击。**任何2026年水印能完全抵御激进的音高修改──这就是为什么你需要检测(AASIST) 和水印配合使用──

### C2PA / İçerik Doğruluk Girişimi

Bu, bir yazılımcı tarafından oluşturulan metadataların bir parçasıdır. Bu metadataların bir kısmı, bir yazılımcı tarafından oluşturulan metadataların bir kısmıdır.

> C2PA / 内容真实性倡议──不是机器学习技术, bir çıkış biçimidir──音频文件携带关于创建工具、作者、日期的加密签名元数据──Audobox / Seamless 使用它──; ancak kötü niyetli eylemciler yeniden kodlanıp, ayrıntılı verileri çıkarsa, işe yaramaz──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.

> **【拓展：语音隐私与安全】**语音数据 contains a lot of personal privacy information (Sözleşme 对话 内容) ◦深度伪造 (Depfake) 语音技术 (Sözleşme 信息) 语音 数据 语音 数据 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语




## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
v4-audio-watermark
```

## Yapın

### Adım 1: basit bir spektral özellik detektörü (oyun)

> 步骤 1:简单的频谱特征检测器 (Yeni bir kez daha)

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

Sintez konuşma genellikle olağanüstü derecede düz yüksek frekanslı enerjiye sahiptir.

> 合成语音 genellikle anormal düzlükte yüksek frekanslı enerjiye sahiptir.

### Adım 2: AudioSeal gömül + tespit

> 步骤 2:AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Adım 3: değerlendirme  EER

> 步骤 3:  EER 等误率)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Dördüncü adım: Üretim entegrasyonu

> 4 adım: üretim sınıfı

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Her nesil gemi: (1) su işaretleri, (2) imzalanan manifesto, (3) tutma politikasına uygun denetim kayıtları.

> Her türlü üretim içermektedir: 1) su basımı, 2) imza liste, 3) koruma stratejisinin audit日志­ine uygun olarak.




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## Tuzaklar

> 常见陷

- **Watermark without detector ever running.**İletişim cihazını gönder.
  Çeviri:**嵌入水印但从未运行检测器。**无意义――把检测器集成到CI 中――
- **Detection without calibration.**AASIST, ABD'de gerçek dünya doğruluk oranında eksikliği yapan bir ekip.
  Çeviri:**检测未校准。**ABD'de eğitim alanında AASIST'in eğitimleri geçmiştir; gerçek doğruluk oranı düşüyor.
- **Pitch-shift gap.**Agresif bir atış noktası çoğu su işaretini ortadan kaldırır.
  Çeviri:**音高偏移漏洞。**激进的音高偏移能去除大多数水印──準備检测作为后备──
- **Metadata strip-and-rehost.**C2PA, yeniden kodlama yoluyla önemsiz olarak atlanabilir. Her zaman kriptografik + algılama (su işaretleri) savunmasını bir araya getirin.
  Çeviri:**元数据剥离重新托管。**C2PA 通過重新编码即可輕易绕過──始终同时使用加密 + 感知(水印) savunması──
- **Liveness as detection.**Kullanıcıya rastgele bir cümle söylemesini söyle. Tekrarlama saldırılarını önler ama gerçek zamanlı klonlama değil.
  Çeviri:**活体检测作为检测手段。**Kullanıcıya bir zamanlı kısa söz söyleyin. Yeniden saldırı önleyebilir ama gerçek zamanlı saldırı önleyemez.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-spoof-defender.md`Ses geninin dağıtımında tespit modeli, su işaretleri, kaynak manifesti ve operasyonel oyun kitabı seçin.

> 保存为 `outputs/skill-spoof-defender.md`◊ için bir语音生成部署选择检测模型、水印、来源清单和运营手册。

## Egzersizler.

1. **Easy.**Çık .`code/main.py`. Oyuncak detektörü + oyuncak su işaretleri sentetik ses üzerinde yerleştirilmiş/ tespit edilmiş.
   Çeviri:**简单。**运行  İşlem`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖
2. **Medium.**Kurulum`audioseal`TTS çıkışına 16 bitlik bir payload yerleştirir, yeniden kodlar.
   Çeviri:**中等。**- Yapımcılık`audioseal`, TTS 输出中嵌入 16 位载荷,重新解码──用噪音损坏音频并测量位恢复准确率──
3. **Hard.**ASVspoof 2019 LA'da RawNet2 veya AASIST'i ince ayarlayın. EER ölçün. F5-TTS üretilen kliplerin uzun süren bir setinde test yapın  OOD algılama nasıl bozulduğunu görün.
   Çeviri:**困难。**ABD'de 2019'da yapılan bir testte, RAVNet2 veya AASIST'in oranı ölçülüyor.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) mevcut referans değer.
  ABD'nin 5'ü...
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) Varsayılan su işaretleri.
  Defossez 等(2024). AudioSeal水印默认方案──
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150) Zamanlı saldırılar için MoE dedektörü.
  Chen 等(2025). WaveVerify  Time Attack'ın MoE 检测器
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) SOTA algılama omurgası.
  Jung 等(2022). AASISTSOTA 检测骨干。
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) Güçlülik değerlendirme.
  AudioMarkBench ((2024) 鲁棒性评估──
- [C2PA specification](https://c2pa.org/specifications/specifications/) Kaynak açıklaması biçimi.
  C2PA 规范来源清单格式──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

