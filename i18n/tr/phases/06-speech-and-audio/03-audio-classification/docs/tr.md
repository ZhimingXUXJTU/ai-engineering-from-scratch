# Ses sınıflandırması  MFCC'den MFCC'ye K-NN'den AST ve BEAT'e  音频分类  MFCC'den + KNN'e AST ve BEAT'e 

> "Köpek kışkırtması vs siren"den "bu hangi dil"e kadar her şey ses sınıflandırmasıdır. Özellikleri erimiş. Arsitektir her on yılda hareket eder. Değerlendirme AUC, F1 ve sınıf başına hatırlanmaya kalır.

> **【中文解读】**"Çoğu Çağırmak Ya da Ses Ses Sesleri"den "Bu Ne Dil"e kadar, tüm sesler                                                                                                                                                                                                                                                  

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

10 saniyelik bir klip alırsınız. Bilmek istiyorsunuz: "Ne?" Şehir ses (siren, egzersiz, köpek), konuşma komutu (evet/hayır/durma), dil kimliği (en/es/ar), konuşmacı duygu (gürültülü/ayrı taraflı), veya çevresel ses (özel) Bunlar * ses sınıflandırması* ve 2026 yılında temel mimarlık olgunlaşmıştır: log-mel → CNN veya Transformer → softmax.

> Siz bir bölüm 10 saniye ses sesini elde ettiniz. Bu nedir? " diye merak ediyorsunuz.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Ana zorluk ağ değil. Veriler. Ses verilerinin vahşi sınıf dengesizliği, güçlü etki alanı değişimi (temiz vs gürültülü) ve etiket gürültüsü vardır (kim "şehirli gürültü" vs. "restaurant gürültüsü" karar verdi). Sorunun %80'i CNN'i Transformer ile değiştirmek değil, kurasyon, büyütme ve değerlendirme.

> 核心难点不在网络,而在数据──音频数据集有严重类别不平衡、强领域偏移(干净 vs 杂) 和标签噪音(() ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊) ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ 

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**Her klip için düz MFCC'ler, etiketlenmiş bir banka ile cosine benzerliği hesaplamak, üst K'nin çoğunluk oyunu geri vermek. Temiz, küçük veri kümeleri (Speech Commands, ESC-50) üzerinde şaşırtıcı derecede güçlü.

> **MFCC 上的 k-NN（1990 年代基线）。**Bu, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ve bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir dizi metin ile bir araya gelerek, bir araya gelerek, bir dizi metin ile bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelişe, bir araya gelerek, bir araya gelerek, bir araya gelerek, bir araya gelişe, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir, bir araya gele, bir araya gele, bir araya gele, bir araya gele, bir, bir, bir araya gele, bir, bir araya gele, bir, bir, bir araya, bir araya gele, bir araya, bir araya gele, bir, bir, bir araya gele, bir, bir araya gele, bir, bir, bir araya gele, bir, bir

**2D CNN on log-mels (2015-2019).**- Yapabilirsin .`(T, n_mels)`ResNet-18 veya VGG tarzı uygulayın. Küresel ortalama zaman ekseni birleştirir. Sınıflar üzerinde yumuşaklık. 2026 kaggle yarışlarının çoğu için hâlâ temel çizgi.

> **log-mel 上的 2D CNN（2015-2019）。**- Ben de .`(T, n_mels)`ResNet-18 veya VGG biçimi ile, zaman aksidesinde tüm ortamın ortalama değerini oluşturmak için, sınıflara yumuşaklıklılık göstermek için, 2026 yılının çoğu kaggle yarışında hala temel çizgi olarak kullanılır.

**Audio Spectrogram Transformer, AST (2021-2024).**Log-mel'i (örneğin 16×16 patch) yapıştırın, pozisyon yerleştirmelerini ekleyin, bir ViT'ye girin.

> **音频频谱图 Transformer，AST（2021-2024）。**将 log-mel 分块(16×16 块 gibi),添加位置嵌入,送入 ViT。AudioSet 上监督学习的 SOTA(mAP 0.485)。

**BEATs and WavLM-base (2024-2026).**Kendi kendine denetimli ön eğitim milyonlarca saat. İhtiyacınız olan denetimli verilerin %1-10'u ile görevinizi inceleme. 2026 yılında bu konuşma dışı ses için varsayılan başlangıç noktasıdır. BEATs-iter3 hesaplama kullanırken AudioSet'te AST'yi 1-2 mAP'ye yener.

> **BEATs 和 WavLM-base（2024-2026）。**Bu, sesli sesler için standart başlangıç noktasıdır. Beats-iter3 AudioSet'te AST'den yüksek 1-2 mAP'den daha yüksek, hesaplama oranı ise sadece 1/4'dir.

**Whisper-encoder as a frozen backbone (2024).**Whisper'in kodlayıcısını alın, dekodörü bırakın, bir çizgi sınıflandırıcı ekleyin.

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器──在语言 ID 和简单事件分类上接近 SOTA,无需任何音频增强──"免费午餐"基线──

### Sınıf dengesizliği gerçek bir zorluk

> ### 类别不平衡才是真正的挑战

ESC-50: 50 sınıf, her biri 40 klip  dengeli, kolay. UrbanSound8K: 10 sınıf, denge dışı 10:1. AudioSet: 632 sınıf, 100.000:1 uzun kuyruğu. Çalışan teknikler:

> ESC-50:50 个类,每类 40 个片段平衡、简单。UrbanSound8K:10 个类,10:1 不平衡。AudioSet:632 个类,长尾比例 100,000:1──有效的技术:

- Eğitim sırasında dengeli örnekleme (değerlendirme sırasında değil).
  訓練時平衡采样 (Balanç zaman)
- Karıştırma: iki klip (ve etiketleri) büyütme olarak doğrusal olarak interpolasyon.
  Karıştırma: 線性插值两段音频 (→                                                                                                                                                                                                                                                        
- SpecAugment: rastgele zaman ve frekans bantlarını maske.
  SpecAugment: Şaplak Zaman ve Geçicilik ile.

### Değerlendirme

> ### 评估

- Çok sınıflı özel (Söz Komutları): üst-1 doğruluk, üst-5 doğruluk.
  Belki de konuşma komutları: üst-1 准确率、 üst-5 准确率。
- Çok sınıflı çok etiket (AudioSet, UrbanSound tarzı): ortalama doğruluk (mAP).
  Belki de çok fazla etiket(AudioSet、UrbanSound 类型): ortalama netlik ortalama değer(mAP)。
- Büyük ölçüde dengesiz: sınıf başına geri çağırma + makro F1.
  严重不平衡: 每类召回率 + 宏观 F1──

Bilmen gereken 2026 numarası:

> 2026 yılında bilmen gereken sayı:

| Benchmark | Baseline | SOTA 2026 | Source |
|-----------|----------|-----------|--------|
| ESC-50 | 82% (AST) | 97.0% (BEATs-iter3) | BEATs paper (2024) |
| AudioSet mAP | 0.485 (AST) | 0.548 (BEATs-iter3) | HEAR leaderboard 2026 |
| Speech Commands v2 | 98% (CNN) | 99.0% (Audio-MAE) | HEAR v2 results |

| 基准测试 | 基线 | 2026 SOTA | 来源 |
|----------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.

> **【拓展：语音隐私与安全】**语音数据 contains a lot of personal privacy information (Sözleşme 对话 内容) ◦深度伪造 (Depfake) 语音技术 (Sözleşme 信息) 语音 数据 语音 数据 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语





## Yapın.
```figure
mfcc-pipeline
```

## Yapın

### Adım 1: Featurization

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### Adım 2: Sıkı bir uzunluklı özet

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

Basit ama güçlü: ortalama + zaman aralığı 13 kovan MFCC için 26 boyutlu sabit bir yerleşim sağlar. Anında çalışır. ESC-50'de son zamanlarda 2017 yılında en son NN temel çizgileri yenir.

> 简单但有效:时间轴上平均值 + 方差为 13系数 MFCC 给出26维固定嵌入──运行瞬间── ESC-50 上直到2017年仍能击败当时的SOTA 神经网络基线──

### Adım 3: k-NN

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return dot / (na * nb)

def knn_classify(q, bank, labels, k=5):
    sims = sorted(range(len(bank)), key=lambda i: -cosine(q, bank[i]))[:k]
    votes = Counter(labels[i] for i in sims)
    return votes.most_common(1)[0][0]
```

### Dördüncü adım: Log-Mels'e CNN'e yükselt

PyTorch'te:

```python
import torch.nn as nn

class AudioCNN(nn.Module):
    def __init__(self, n_mels=80, n_classes=50):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(128, n_classes)

    def forward(self, x):  # x: (B, 1, T, n_mels)
        return self.head(self.body(x).flatten(1))
```

3M parametreleri. ESC-50'de tek bir RTX 4090 ile 10 dakika içinde trenler.

> 300.000 parametre── ESC-50 上 single张 RTX 4090 訓練 約 10 分鐘──精度率 80%+──

### Adım 5: 2026 Varsayılan  ince ayarlı BEAT

```python
from transformers import ASTFeatureExtractor, ASTForAudioClassification

ext = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained(
    "MIT/ast-finetuned-audioset-10-10-0.4593",
    num_labels=50,
    ignore_mismatched_sizes=True,
)

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


inputs = ext(audio, sampling_rate=16000, return_tensors="pt")
logits = model(**inputs).logits
```

BEAT için kullanın `microsoft/BEATs-base``beats`kütüphanesi; transformör API aynı şekildedir.

> 对于Beats,通过 `beats`Kullanım 库`microsoft/BEATs-base`;transformers API'nin biçimi aynıdır:




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Start with |
|-----------|-----------|
| Tiny dataset (<1000 clips) | k-NN on MFCC means (your baseline) + audio augmentation |
| Medium dataset (1K–100K) | BEATs or AST fine-tune |
| Large dataset (>100K) | Train from scratch or fine-tune Whisper-encoder |
| Real-time, edge | 40-MFCC CNN, quantized to int8 (KWS-style) |
| Multi-label (AudioSet) | BEATs-iter3 with BCE loss + mixup + SpecAugment |
| Language ID | MMS-LID, SpeechBrain VoxLingua107 baseline |

| 场景 | 起始方案 |
|------|----------|
| 小数据集（<1000 段） | MFCC 均值上的 k-NN（基线）+ 音频增强 |
| 中等数据集（1K–100K） | BEATs 或 AST 微调 |
| 大数据集（>100K） | 从零训练或微调 Whisper 编码器 |
| 实时、边缘设备 | 40-MFCC CNN，量化为 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


Karar kuralları: **start with a frozen backbone, not a fresh model**Beats'in kafasını ince ayarlamak, bir kaç hafta değil, saatler içinde %95 SOTA elde eder.

> 决策规则:**从冻结骨干开始，而不是从头训练模型**❖ Küçük düzenli BEAT'lerin sınıfı başları birkaç hafta yerine birkaç saat içinde SOTA'nın %95'ine ulaşabilir.



## İndirin . Ürünler .

- Kaydet .`outputs/skill-classifier-designer.md`. Verilen ses sınıflandırma görevi için mimari, artırmalar, sınıf dengesi stratejisi ve değerlendirme metriklerini seçin.

> 保存为 `outputs/skill-classifier-designer.md`◊ belirli bir ses sınıfı görev seçimi yapı, güçlendirme stratejisi, sınıf dengeleme stratejisi ve değerlendirme göstergesi için

## Egzersizler.

1. **Easy.**Çık .`code/main.py`.K-NN MFCC temel çizgisini 4 sınıf sentetik veri kümesi (farklı tonlarda saf tonlar) üzerine eğitir.
   **简单。**运行  İşlem`code/main.py`◊ Bu 4 类合成数据集 (不同音高的纯音) üzerinde eğitim k-NN MFCC 基线―― rapor混矩阵――
2. **Medium.**Değiştir `summarize`4 anlık birleştirme aynı sentetik veri kümesindeki ortalama + var'ı çarpıyor mu?
   **中等。**- Ben de .`summarize`替换为 [mean, var, skew, kurtosis]──四矩池化 is in the same synthesis dataset优于平均值+方差?
3. **Hard.**Kullanım`torchaudio`ESC-50 katında 2 boyutlu bir CNN eğitimi 1. 5 katlı çapraz doğrulama doğruluğunu bildirin. SpecAugment (zaman maskesi = 20, frekans maskesi = 10) ekleyin ve delta raporunu yapın.
   **困难。**Kullanım`torchaudio`, ESC-50 katman 1 上訓練 2D CNN。 rapor 5 折交叉验证准确率。添加 仕様Augment(时间掩码 = 20,频率掩码 = 10)并报告差值。

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| AudioSet | The ImageNet of audio | Google's 2M-clip, 632-class weakly-labeled YouTube dataset. |
| ESC-50 | Small classification benchmark | 50 classes × 40 clips of environmental sounds. |
| AST | Audio Spectrogram Transformer | ViT on log-mel patches; 2021 SOTA. |
| BEATs | Self-supervised audio | Microsoft model, iter3 leads AudioSet as of 2026. |
| Mixup | Pair augmentation | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`. |
| SpecAugment | Mask-based augmentation | Zero-out random time and frequency bands of the spectrogram. |
| mAP | Main multi-label metric | Mean average precision across classes and thresholds. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标注 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 个环境声音片段。 |
| AST | 音频频谱图 Transformer | log-mel 块上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`。 |
| SpecAugment | 掩码增强 | 将频谱图的随机时间和频率带置零。 |
| mAP | 主要多标签指标 | 各类别和阈值的平均精度均值。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) 2021 2024 tarihli kayıtlı mimarisi.
  Gong, Chung, Glass (2021). AST:音频频谱图 Transformer2021-2024 yılın kayıt yapısı。
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) 2024+'ün varsayımlılığı.
  Chen 等 (2022, 修订 2024). BEATs:声学 tokenizer 的音频预训练2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) baskın ses artışı.
  Park 等 (2019). SpecAugment主流音频增强方法──
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50)50 sınıflı bir referans değerinin devamı.
  Piczak (2015). ESC-50 数据集持续使用的50类基准──
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) 632 sınıfı YouTube taksonomisi; hala altın standart.
  Gemmeke 等 (2017). AudioSet632 类 YouTube 分类体系; hâlâ altın standart。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

