# Konuşmacı Tanım ve Doğrulama İnsan Tanımı ve Doğrulama

> ASR "Ne dediler?" sorusunu sorar. Konuşmacı tanıma "Kim söyledi?" sorusunu sorar. Matematik aynı  gömülmeler artı cosine  gibi görünüyor.

> **【中文解读】**ASR ̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆̆

> **【拓展：声纹识别应用】**声纹识别用于银行电话认证、智能音箱用户识别、安防监控──声纹(声纹) 语音 parmak izi gibi, biyolojik özelliklerin tanımlanmasının önemli bir parçasıdır──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

Bir kullanıcı bir şifre ifade eder. Bilmek istiyorsunuz: bu kişi olduğunu iddia eden kişi mi (* doğrulama*, 1:1), yoksa kayıt bankasınızdaki ilk kişi mi (* kimlik*, 1:N)?

> User bir sözcük çıkardı. ❓ You wondered: Is this the person they claim to be? ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

2018'den önce: GMM-UBM + i vektörleri. Makul EER ancak kanal değişimi (telefon vs dizüstü bilgisayar) ve duygu için kırılgan. 20182022: x vektörleri (tDNN omurgası açılı kenar ile eğitilmiştir). 2022+: ECAPA-TDNN ve WavLM- büyük gömülmeler. 2026 yılına kadar alan üç model ve bir metrik tarafından egemenlik kazanmıştır.

> 2018 yıl ön:GMM-UBM + i-vektorlar。EER 合理但对信道偏移(电话 vs 笔记本) 和情绪敏感。2018-2022:x-vektorlar◆用角度间隔训练的 TDNN 骨干)。2022+:ECAPA-TDNN 和 WavLM-large 嵌入──到2026年,该领域由三个模型和一个指标主导────

Metrik bu.**EER** Eşit hata oranı. Karar sınırını ayarlayın, böylece yanlış kabul oranı = yanlış reddetme oranı.

> Bu işaretçi**EER**等错误率──设定决策值使假接受率 =假拒绝率──交叉点就是 EER──用于每篇论文、每排行榜、每采购评审──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**Kayıt: hedef hoparlörün 530 saniye kayıt; sabit boyutlu bir yerleştirme hesaplayın (192-d ECAPA-TDNN için, 256-d WavLM- büyük için).

> **流水线。**注册:录制目标说话人 5-30秒语音;计算固定维度嵌入(ECAPA-TDNN 为 192 维,WavLM-large 为 256 维) 验证:获取测试语音嵌入;计算余弦相似度;与值比较──

**ECAPA-TDNN (2020, still dominant 2026).**Kanal Dikkat, Yayın ve Toplantı - Zaman Gecikmesi Nöral Ağ. 1D konvu blokları sıkıştırma-eğilim, çok başlı dikkat birleştirme, ardından 192-d'ye kadar bir çizgi katman. VoxCeleb 1+2 (2,700 hoparlör, 1.1M ifadeler) ile Eklemel Angular Margin kaybı (AAM-yumuşak maksimum) ile eğitilmiştir.

> **ECAPA-TDNN（2020，2026 年仍占主导）。**Çeviri dikkat, yayım ve birleşim zamanı sinir ağı.1.D 卷积块 + sıkıştırma-eğilim + 多头注意池化,接线性层输出192 维──

**WavLM-SV (2022+).**AAM kaybı ile önceden eğitilmiş WavLM büyük bir SSL omurgasını ince ayarlayın. Daha yüksek kalitede ama daha yavaş  300+ MB vs 15 MB.

> **WavLM-SV（2022+）。**AAM 损失微调预训的 WavLM-large SSL 骨干──质量更高但更慢300+ MB vs. 15 MB──

**x-vector (baseline).**TDNN + istatistikleri birleştirme. Klasik; hala CPU / kenarında yararlı.

> **x-vector（基线）。**TDNN + 统计池化── klasik program; hala CPU/ kenar cihazlarda kullanılabilir──

**AAM-softmax.**Eklenmiş marj ile standart softmax `m`Kolaylık:`cos(θ + m)`Bu, normal bir şekilde, sınıflar arası açısal ayrım güçleri.`m=0.2`, ölçekli`s=30`- Evet .

> **AAM-softmax。**Çevre açısından bir bölge ekle.`m`                                                                                                                                                                                                                                                              `cos(θ + m)`❖ zorunluluk sınıfları arasındaki açı ayrımı── tipik değer `m=0.2`,缩放 `s=30`- Evet.

### Notlama

> ### 评分

- **Cosine**Başvurma ve sınav yerleşimleri arasında.
  **余弦**Benzerlik, kayıtlı yerleşim ve test yerleşim arasında hesaplanır.
- **PLDA (Probabilistic LDA).**Aynı hoparlör ile farklı hoparlör arasındaki olasılık oranının kapalı olduğu gizli bir alanın içine yerleştirilen proje. +1020% EER azaltımı için cosine üstüne eklenir. Standart 2020 öncesi; şimdi sadece kapalı set set setuplarda kullanılır.
  **PLDA（概率 LDA）。**Projection'u potansiyel alanlara yerleştirecek, bu alanlarda konuşmacı ile konuşmacı arasında bir kapalı benzerlik vardır.
- **Score normalization.** `S-norm`veya `AS-norm`Bu, her puanı sahte araç ve diğer araçlara karşı normalleştirir.
  **分数归一化。** `S-norm`Ya da`AS-norm`Bu nedenle, bu değerlerin değerlendirilmesi ve değerlendirilmesi için, bu değerlerin değerlendirilmesi ve değerlendirilmesi gerekmektedir.

### Bilmeniz gereken sayılar (2026)

> 2026 yılının bilmen gereken sayısı

| Model | VoxCeleb1-O EER | Params | Throughput (A100) |
|-------|-----------------|--------|-------------------|
| x-vector (classic) | 3.10% | 5 M | 400× RT |
| ECAPA-TDNN | 0.87% | 15 M | 200× RT |
| WavLM-SV large | 0.42% | 316 M | 20× RT |
| Pyannote 3.1 segmentation + embedding | 0.65% | 6 M | 100× RT |
| ReDimNet (2024) | 0.39% | 24 M | 100× RT |

| 模型 | VoxCeleb1-O EER | 参数量 | 吞吐量（A100） |
|------|-----------------|--------|----------------|
| x-vector（经典） | 3.10% | 500 万 | 400× 实时 |
| ECAPA-TDNN | 0.87% | 1500 万 | 200× 实时 |
| WavLM-SV large | 0.42% | 3.16 亿 | 20× 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 600 万 | 100× 实时 |
| ReDimNet（2024） | 0.39% | 2400 万 | 100× 实时 |

### Diaryizasyon

> ### Konuşmak için kim var?

"Kim ne zaman konuştu" bir çok hoparlör klipi. Pipeline: VAD → segment → her segment → cluster (aglomeratif veya spektral) → düz sınırlar yerleştirir. Modern yığın: `pyannote.audio`3.1, bir çağrı arkasında hoparlör segmentasyonu + yerleştirme + gruplama birleştirir. 2026 SOTA DER AMI'de ~ 15% (2022'de 23%'den düştü).

> Çoğu konuşma insan sesli metinlerde "Who is there?"`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为一个调用──2026 yılının AMI 上 SOTA DER 约15%(2022 yılının 23% 下降)──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
sp-eer-crossover
```

## Yapın

### Adım 1: MFCC istatistiklerinden oyuncak yerleştirme

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26-d
```

Sadece öğretmenlik için bir millik bir SOTA değil.`code/main.py`Bu, sentetik hoparlör verileri üzerinde bir kavram kanıtı olarak kullanır.

> 离 SOTA 差得远 yalnızca öğretim için kullanılır.`code/main.py`Bu, insan verisini bir kavram olarak tanımlamak için kullanılır.

### Adım 2: Kosinus benzerliği + eşiği

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Adım 3: Eşlik çiftlerinden EER

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 1.0, 0.0)  # (fa, fr, threshold)
    for t in thresholds:
        fr = sum(1 for s in same_scores if s < t) / len(same_scores)
        fa = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        if abs(fa - fr) < abs(best[0] - best[1]):
            best = (fa, fr, t)
    return (best[0] + best[1]) / 2, best[2]
```

Geri dönüşler (eer, threshold_at_eer).

> 返回 (eer, threshold_at_eer) ・・・两者都要报告──

### Adım 4: SpeechBrain ile üretim

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Adım 5: Pyannote ile günlük yazın

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Pick |
|-----------|------|
| Closed-set 1:1 verification, edge | ECAPA-TDNN + cosine threshold |
| Open-set verification, cloud | WavLM-SV + AS-norm |
| Diarization (meetings, podcasts) | `pyannote/speaker-diarization-3.1` |
| Anti-spoofing (replay / deepfake detection) | AASIST or RawNet2 |
| Tiny embedded (KWS + enrollment) | Titanet-Small (NeMo) |

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘设备 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 反欺诈（回放/深度伪造检测） | AASIST 或 RawNet2 |
| 小型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |



## Tuzaklar

> 常见陷

- **Channel mismatch.**VoxCeleb (web video) üzerinde eğitimli model ≠ telefon çağrısı sesini.
  **信道不匹配。**VoxCeleb (WEB) üzerinde eğitim modelleri telefon sesleri ile eşit değildir.
- **Short utterances.**EER, test sesinin 3 saniyesinin altında keskin bir şekilde azalır.
  **短语音。**测试音频低于3秒时 EER 急剧恶化──
- **Enrollment with noise.**Bir gürültülü kayıt, demirciyi zehirliyor.
  **带噪注册。**Bir 杂的注册样本会毒化点──使用至少3 干净样本并取平均──
- **Fixed threshold across conditions.**Hedef alanından çıkmış bir dev seti için her zaman eşiği ayarlayın.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调值──
- **Cosine on non-normalized embeddings.**L2- önce normalleştirin; aksi takdirde büyüklük hakim olur.
  **未归一化嵌入上的余弦。**Önceden yapılması L2 归一化;否则模值会占主导──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-speaker-verifier.md`- Seçim modeli, kayıt protokolü, eşiğin ayarlama planı ve dolandırıcılık korumaları.

> 保存为 `outputs/skill-speaker-verifier.md` Seçim modeli, kayıt anlaşması, değerlendirme planı ve sahtekarlık önleme önlemleri

## Egzersizler.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


1. **Easy.**Çık .`code/main.py`- Sintez "konusucular" (farklı ses profilleri), 100 çift deneme listesine katılır, EER hesaplanır.
   **简单。**运行  İşlem`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖  ❖ ❖                  ❖                                                                              
2. **Medium.**30 VoxCeleb1 konuşmasında SpeechBrain ECAPA kullanın (5 hoparlör × 6 kişi).
   **中等。**Bu nedenle, bu programın başlıklı olarak, "Önemli bir konuşma" olarak adlandırılan bir konuşma yapımıdır.
3. **Hard.**Tam kayıt yapın → günlük yapın → verify pipeline with `pyannote.audio`- AMI dev kuruluşu üzerinde DER değerlendiriyoruz.
   **困难。**Kullan .`pyannote.audio`构建完整的注册 → 日志 → 验证流水线──在 AMI 开发集上评估 DER──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| EER | The headline metric | Threshold where False Accept = False Reject. |
| Verification | 1:1 | "Is this Alice?" |
| Identification | 1:N | "Who is speaking?" |
| Open-set | Unknown possible | Test set can contain unenrolled speakers. |
| Enrollment | Registering | Computing a speaker's reference embedding. |
| AAM-softmax | The loss | Softmax with additive angular margin; forces cluster separation. |
| PLDA | Classic scoring | Probabilistic LDA; likelihood-ratio scoring on top of embeddings. |
| DER | Diarization metric | Diarization Error Rate — miss + false alarm + confusion. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| EER | 头条指标 | 假接受率 = 假拒绝率时的阈值。 |
| 验证 | 1:1 | "这是 Alice 吗？" |
| 识别 | 1:N | "谁在说话？" |
| 开放集 | 可能有未知者 | 测试集可包含未注册的说话人。 |
| 注册 | 登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度间隔的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 说话人日志错误率——漏检 + 误检 + 混淆。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) klasik derin gömülü kağıt.
  Snyder 等 (2018). X-Vectors:说话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) 2020 2026 baskın mimarisi.
  Desplanques等 (2020). ECAPA-TDNN2020-2026 yılları
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) SV ve günlükleştirme için SSL omurgası.
  Chen 等 (2022). WavLM: Full 语音处理 大规模自监督预训SV 和日志的 SSL 骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) üretim günlükleşmesi + yerleştirme yığın.
  Bredin 等 (2023). pyannote.audio 3.1生产级日志 + 嵌入技术。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) Modeller arasında mevcut EER sıralamaları.
  VoxCeleb 排行榜(2026年更新) 各模型当前 EER 排名。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

