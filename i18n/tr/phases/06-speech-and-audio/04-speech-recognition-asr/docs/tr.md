# Konuşma Tanıma (ASR)  CTC, RNN-T, Dikkat  语音识别  CTC、RNN-T  关注机

> Konuşma tanıma, her zaman adımında ses sınıflandırmasıdır, İngilizce ve sessizlik bilinen bir dizi modeli ile yapıştırılır. CTC, RNN-T ve dikkat bunu yapmanın üç yolu.

> **【中文解读】**语音识别, her zaman sesli bir dizi biçiminde kullanılır.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学) 会议记录(飞书/钉钉实时字幕) 视频字幕自动生成的核心──Whisper is 2026 yılının açık kaynağı ASR 标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

10 saniyelik 16 kHz klipiniz var. Bir ip istersiniz: "mutfak lambalarını açın". Çabası yapısal: ses çerçeveleri karakterlerle birbiriyle uyumlu değildir. "OK" kelimesi 200 ms veya 1200 ms alabilir. Sessizlik ifadeni noktalar. Bazı fonemler diğerlerinden uzun. Çıktılık belirtilerin sayısı önceden bilinmemektedir.

> Siz bir bölüm 10 saniye 16 kHz 音频──你想要一个字符串:"turna light kitchen"──挑战是结构性的:音频与字符不是一对应的──单词"okay"可能占用200 ms或1200 ms──静音打断语语语──有些音素比其它更长──输出代币的数量事先不知道──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Üç formülasyon bu durumu çözer:

> Üç farklı çözüm yolu:

1. **CTC (Connectionist Temporal Classification).**Özel bir * boş* dahil bir çerçeve için belirtiler olasılığını gönderin. Decode zamanı çöküş tekrarları ve boşlukları.
   **CTC（连接时序分类）。**逐发射代币 概率,包括特殊的 *blank*──解码时折叠重复和空白──非自归归,快速──wav2vec 2.0、MMS 使用──
2. **RNN-T (Recurrent Neural Network Transducer).**Ortak ağ, verilen bir sonraki token'ı kodlayıcı çerçevesine ve önceki token'lara önceden tahmin eder. Akışlanabilir.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google 端侧 ASR、NVIDIA Parakeet 使用──
3. **Attention encoder-decoder.**Kodlayıcı sesleri gizli durumlara sıkıştırır, dekoderler otomatik olarak jetonlar oluşturmak için çapraz olarak çalışır.
   **注意力编码器-解码器。**编码器将音频压缩为隐藏状态,解码器通过交叉注意力自归归地生成代币──Whisper、SeamlessM4T 使用──

2026 yılında LibriSpeech test temizliği SOTA WER'nin %1.4 (Parakeet-TDT-1.1B, NVIDIA) ve %1.58% (Whisper-Large-v3-turbo) oranı.

> 2026 yıl,LibriSpeech test-clean 上的SOTA WER为1.4% (Parakeet-TDT-1.1B,NVIDIA) y 1.58% (Whisper-Large-v3-turbo)

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**Kodlayıcı çıkış yapsın `T`Çerçeve seviyesindeki dağılımlar `V+1`işaretler (V karakterler + boş). Hedef dizilisi için `y`uzunlukta `U < T`, herhangi bir çerçeve düzeni çöküyor `y`CTC kaybı tüm bu ayarların toplamı.

> **CTC 直觉。**让编码器输出 `T`个级分布,每个分布覆盖 `V+1`个标志(V 个字符 + blank) ⋅对于长度为 `U < T`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `y`, her bir çarpma sonrası `y`Bu nedenle, bu durumun bir sonraki sonucu olarak, bir diğerinin de bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğerinin sonucu olarak, bir diğer bir diğerinin de diğerine görevi olarak, bir diğerinin sonucu olarak, bir diğer bir diğerine görevi olarak, bir diğer bir diğerine görevi olarak, bir diğerine görevi olarak, bir diğerine görevi olarak, bir diğerine görevi olarak, diğerine görevi olarak, diğerine, diğerine görevi olarak, diğerine görevi olarak, diğerine görevi olarak, diğerine de, diğerine de, diğerine, diğerine de, diğerine, diğerine de, diğerine, diğerine de, diğerine, diğerine, diğerine de de de de, diğerine, diğerine, de, diğerine, de de de de de de de, de, diğerine, de, de de de de de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de, de de de, de, de de de de, de, de de, de de, de de de de de, de de de de de de, de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de

Avantajlar: kendi kendine geri dönmeyen, akışlı, sıfır bakış açısı. Eksikliği: * koşullı bağımsızlık varsayımı*  her çerçeve öngörü diğerlerinden bağımsızdır, bu nedenle iç dil modeli yoktur.

> 优势:非自归、可流式处理、零前──缺点:*条件独立性假设*每预测彼此独立,因此没有内部语言模型──通过束搜索或浅融合的外部 LM 来修复──

**RNN-T intuition.**Token geçmişini yerleştiren *predictor* ağı ve *joiner* ' i ekler.`V+1`(Devayı)`+1`CTC'nin göz ardı ettiği koşullı bağımlılığı açıkça modeller. Her adım sadece geçmiş çerçeveler ve geçmiş jetonlar için koşullar nedeniyle akışlanabilir.

> **RNN-T 直觉。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `V+1`联合分布的 *joiner*(`+1`CTC 忽略的条件依赖──可流式处理,因为每步只依赖于过去和过去的代币──

Avantajlar: akışlı + iç LM. Eksikliği: eğitim daha karmaşık ve hafıza açtır (3D kaybı ağ); RNN-T kaybı çekirdekleri kendi başına bir kütüphane kategorisidir.

> 优势:可流式 + 内部 LM。缺点:训练更复杂、更耗内存(3D 损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**Log-mel çerçeveleri üzerinde kodlayıcı (6-32 transformatör katmanı). Dekoder (6-32 transformatör katmanı) otomatik olarak jetonlar üretmek için kodlama çıkışlarına çapraz hizmet verir. Düzeltme kısıtlaması  dikkat sesin herhangi bir yerinde bakabilir. Dikkatini kısıtlamadan akışılamaz (çıkılmış Şapışkış Akışı, 2024).

> **注意力编码器-解码器。**编码器(6-32 层变压器) 处理 log-mel ──解码器(6-32 层变压器) 通过交叉注意力自归归生成代币──无对齐约束注意力可以看向音频的任何位置──除非限制注意力(分块 语流,2024),否则不可流式处理──

Avantajlar: çevrimdışı ASR'de en yüksek kalitede, standart seq2seq araçlarıyla eğitilmek kolaydır. Eksikliği: autoregressive latency çıkış uzunluğuna orantılıdır; mühendislik olmadan akışa izin verilmez.

> 优势:离线 ASR 质量最高,标准 seq2seq 工具易训练──缺点:自归延迟与输出长度成正比;不做工程优化无法流式处理──

### WER: tek sayı

> ### WER: Tek gösterge

**Word Error Rate**= `(S + D + I) / N`, S=değiştirme, D=iptal, I=sıkıştırma, N=referans kelime sayısı. Levenshtein'in kelime seviyesindeki düzenleme mesafesine uyması. Daha düşük daha iyidir. 20%'den yüksek bir WER genellikle kullanılamaz; % 5'ten aşağıdaki insan-işleme konuşması için eşitliktir. 2026 standart referans değerleri:

> **词错误率**= `(S + D + I) / N`, içinde S=değiştirme, D=silimleme, I=插入, N=reference词数。对应词级的Levenstein 编辑距离──越低越好──WER 超过20%通常不可用; 5% 低于朗读语音达到人类水平──2026年标准基准上的数字:

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.


Tüm bunlar kodlayıcı-dekoder veya RNN-T tabanlıdır.

> Bunlar kodlayıcı- çözücü cihaz veya RNN-T 架构──纯 CTC 系统(wav2vec 2.0) test temizliği sırasında yukarı 1.82.1%──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.
```figure
ctc-collapse
```

## Yapın

### Adım 1: Açgözlü CTC çözümü

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

İki kural: çökme ardılı tekrarlar, boşluklar bırak.`a a _ _ a b b _ c`→ `a a b c`- Evet .

> 两条规则: 折叠连续重复,丢弃空白── örneği:`a a _ _ a b b _ c`→ `a a b c`- Evet.

### Adım 2: Çığlık araması CTC

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

Üretim LM füzyonu ile prefix ağaç ışın araması kullanır; bu kavramsal iskelet.

> 生产环境使用带 LM 融合的前树束搜索;这是概念骨架──

### Adım 3: WER

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### Dördüncü adım: Fısıltı ile sonuç

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

2026'da en güçlü genel ASR için tek satır. ~ 20× gerçek zamanlı bir 24 GB GPU'da çalışır.

> 2026 yılının en güçlü genel ASR kodunun bir satırı.

### Adım 5: Parakeet veya wav2vec 2.0 ile akış

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Akış ASR'nin parçalara ayrılmış kodlama dikkatini ve taşıma durumu gerektirir; destekleyen bir kütüphaneden kullanın (NeMo için Parakeet, `transformers` ile birlikte`chunk_length_s`)

> 流式 ASR 需要分块编码器注意力和转移状态;使用支持它的库`transformers`boru hattı 带 `chunk_length_s`)。




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## 2026'da hala yolculuk eden tuzaklar

> 2026 yılı hâlâ suçlu bir tuzağa düşüyor.

- **No VAD.**Sessizlikle Sısırmak, halüsinasyonlar yaratır ("Seyrettiğiniz için teşekkürler!").
  **没有 VAD。**"Sözüm için teşekkürler!"
- **Character vs word vs subword WER.**Söz düzeyinde WER *after* normalisasyonunu bildirin (en az yazılı, noktalama kaldırıldı).
  **字符 vs 词 vs 子词 WER。**報告归一化后 (小写、去标点) の词级 WER──
- **Language ID drift.**Whisper'in otomatik LID'si gürültülü klipleri Japonca veya Gallerce'ye yanlış yönlendirir; güç `language="en"`- Ne zaman bilsen.
  **语言识别漂移。**Şapışmanın otomatik dil tanıma sisteminin Japonya veya Uels dilinde yanlış yorumlanması; bilinen dilde zorunlu kullanılması`language="en"`- Evet.
- **Long clips without chunking.**Whisper'in 30 saniyelik bir penceresi var.`chunk_length_s=30, stride=5`Daha uzun süre.
  **长音频不分块。**Şapışın, 30 saniyelik bir pencerede.`chunk_length_s=30, stride=5`- Evet.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-asr-picker.md`- Belirli bir dağıtım hedefi için model seçin, kodlama stratejisi, parçalanma ve LM birleşimi.

> 保存为 `outputs/skill-asr-picker.md`❖ belirli bir dağıtım amacıyla model seçimi, çözme stratejisi, bölük ve LM 融合方案

## Egzersizler.

1. **Easy.**Çık .`code/main.py`- El yapımı bir CTC çıkışını açgözlülükle çözüyor ve WER'yi referans ile hesaplıyor.
   **简单。**运行  İşlem`code/main.py`◊ elle yapılmış CTC 输出 进行贪解码并计算 WER──
2. **Medium.**Adım 2'de önlük-taş ışın aramayı doğru şekilde uygulayın (boş birleştirme kuralını hesaplayın). 10 örnekteki sentetik veri kümesinde açgözlülükle karşılaştırın.
   **中等。**Doğrudan gerçekleştirmek 2 İçin ön ağaç ışın arama  考虑空白合并规则)  在 10 合成样本上与贪方法比较──
3. **Hard.**Kullanım`whisper-large-v3-turbo`- Evet .[LibriSpeech test-clean](https://www.openslr.org/12)İlk 100 konuşma ile WER hesaplayın.
   **困难。**- Evet .[LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`◊ hesaplama ◊ 100 条语音的 WER──与发表的数据比较──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) CTC kağıdı.
  Graves 等 (2006). 连接时序分类CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711)RNN-T kağıdı.
  Graves (2012). RNN  kullan  序列转换 RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) 2022 Kanonik Kağıdı; 2024'te v3-turbo uzantısı.
  Radford 等 / OpenAI (2022). Şapış: Büyük ölçek zayıf监督的鲁棒语音识别2022年经典论文;2024年 v3-turbo 扩展──
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) 2026 Açık ASR Leaderboard lideri.
  NVIDIA NeMoParakeet-TDT 模型卡2026 yıl Açık ASR 排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 25+ model üzerinde canlı bir referans.
  Öğütlü YüzAçık ASR 排行榜25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

