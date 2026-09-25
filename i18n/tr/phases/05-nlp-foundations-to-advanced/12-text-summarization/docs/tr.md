# Metin Özetleri

> Ekstraktif sistemler size belgenin ne dediğini söyler. Abstraktif sistemler yazarın ne demek istediğini söyler. Farklı görevler, farklı tuzaqlar.
> 抽取式系统告诉你文档说了什么――生成式系统告诉你作者意思―― farklı görevler, farklı kapanlar――

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Sorunlar. Sorunlar.

2000 kelimelik bir haber makalesi sizin feed'inize yer alır. 120 kelimeyi ele alabilirsiniz. Ya makaleden en önemli üç cümleyi (ekstrakt) seçebilir veya içeriği kendi kelimelerinizle (abstrakt) yeniden yazabilirsiniz. Her ikisi de özetleme olarak adlandırılır.
> Bir haber makalesinin 2000 kelimesi sizin bilgi akışınızda ortaya çıkıyor. Onu genel olarak ifade etmek için 120 kelime gerekmektedir. Ya da kendi sözcüklerinizle yazmayı yeniden başlatabilirsiniz.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


Ekstraktif özetleme sıralama sorunu.`k`. Çıkış her zaman dilbilimsel çünkü sözcük olarak kaldırılır.
> 抽取式摘要是一个排序问题──给每个句子打分,返回排名 `k`Yapılan sonuçlar, genel olarak sözcük hukukuyla uyumludur, çünkü bu, bir yazılı olarak alınan sonuçlardır.

Abstraktif özetleme bir nesil sorunudır. Bir transformatör giriş üzerine koşullanmış yeni bir metin üretir. Çıktı akıcı ve sıkıştırıcı ancak kaynağa ait olmayan gerçekleri halüsinasyonlayabilir. Risk güvenli bir yapımdır.
> Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çzzüm: Çzüm: Çzüm: Çzzzzzzüm: Çzzüm: Çzzzzzzüm: Çzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

Bu ders her ikisini de güçlendirir. Her birinin başarısızlık moduna sahip.
> Bu ders, iki yapı ve kendi başarısızlık modelini oluşturur.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


## Konsepten bir şey.

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**Makaleyi bir grafik olarak ele alın, burada düğümler cümle, kenarlar da benzerliklerdir.**TextRank**(Mihalcea ve Tarau, 2004).
> **抽取式（Extractive）。**Yazıyı görme şekli, nokta cümle, kenar benzerliktir.**TextRank**(Mihalcea ve Tarau, 2004)。

**Abstractive.**Doküman-sözet çiftlerinde bir transformatör kodlayıcı-dekodör (BART, T5, Pegasus) ince ayarlayın. Sonuçta, model belgeyi okuyor ve çapraz dikkat yoluyla toplamadan token-token oluşturur. Pegasus özellikle çok ince ayarlama yapmadan toplamayı mükemmel kılan bir boşluk cümle öncesi eğitim hedefini kullanır.
> **生成式（Abstractive）。**Bu nedenle, bir dizi farklılıkları olan bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin ve bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi, bir dizi metin, bir dizi metin, bir dizi, bir dizi metin, bir bir bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin, bir metin

 ile değerlendirme**ROUGE**ROUGE-1 ve ROUGE-2 puanları tekerlek ve büyükerlek üstlenir. ROUGE-L puanları en uzun ortak ardıcıllık. Daha yüksek daha iyidir ancak 40 ROUGE-L "iyi" ve 50 "istifadedir". Her makale üçü de rapor eder.`rouge-score`Paket.
> Kullanım**ROUGE**(Hatırlatma odaklı inceleme Gisting Değerlendirme için) 评估──ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠──ROUGE-L 评分最长公共子序列──越高越好,但40 ROUGE-L 是"好",50 是"出色"──每篇论文都报告全部三个──使用`rouge-score`- Evet.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.


## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
summarize-collapse
```

## Yapın

### Adım 1: TextRank (kısaltma)
> 两件事值得注意──相似度函数, orijinal TextRank'ın değişikliği olan sayısal birleştirme sözcüğü kullanır──TF-IDF 向量的余弦相似度也行──阻尼因子 0.85 和代次数是PageRank'ın öntanımlı değeri──

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

İki şey isimlendirme değeridir. Benzerlik fonksiyonu orijinal TextRank variansı olan log-normalize word overlap kullanır. TF-IDF vektörlerinin kozine de çalışır. Damping faktörü 0.85 ve tekrar sayısı, PageRank'in öntanımlı özellikleri.
> BART-large-CNN, CNN/DailyMail 语料上微调──开箱即便产生新闻风格摘要──, diğer alanlar için, Pegasus 检查点或在目标数据上微调──,

### Adım 2: BART ile soyutlama
> 始终使用词干提取──没有它, "running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

BART-large-CNN, CNN/DailyMail korpusuna ince ayarlanmıştır. Kutudan haber tarzında özetler üretir. Diğer alanlar (bilimsel makaleler, diyalog, hukuki), ilgili Pegasus kontrol noktasını veya hedef verilerinizi ince ayarlayın.
> ROUGE, 20 yıl boyunca ana kısaltma göstergesidir, ancak 2026 yılında sadece buna dayanmak yeterli değil.

### Adım 3: ROUGE değerlendirme
> - **BERTScore**(上下文嵌入相似度) 2023 yılında ilgi alanı kazanmak için, şimdi çoğu özet makale ROUGE ile bir rapor oluşturmaktadır.
- **BARTScore**Önemlendirme: BART'ın önceden hazırlanması ile özetin değerlendirilmesi için belirlenmiş kaynaklar belirlenmiştir.
- **MoverScore**(上下文嵌入上的推土机距离) 2025 yılı özet基准 içinde zirveye ulaşır, çünkü REDGE'den daha iyi bir dil anlamı toplama yapmaktadır.
- **FactCC**和**基于 QA 的事实性检查**2021-2023 yılları çok sık görülen, şimdi genellikle **G-Eval**(GPT-4 提示链, 链式思考推理评分连贯性、一致性、流性和相关性)
- **G-Eval**Ve benzer LLM  değerlendirme yöntemleri, değerlendirme standartları iyi tasarlanmışken insan yargılamaları ile yaklaşık % 80 aynıdır.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

Sensiz "cırmak" ve "cırmak" farklı kelimeler olarak sayılır ve ROUGE az sayılır.
> 生产建议: 报告 ROUGE-L 用于遗留比较,BERTScore 用于语义重叠,G-Eval 用于连贯性和事实性──针对 50-100 个人类标签摘要校准──

### ROUGE'den öte (2026 özet değerlendirme)
> Çözümlü özetlerin kolayca hayal oluşması riskleri çok daha düşüktür, çünkü çıkışlar kaynaktan kelimelerle harcanır, ancak kaynak cümleler aşağıdaki metinlerden ayrılırsa bile, bunlar hala yanlış yönlendirilebilir. Bu, üretim sistemlerinin düzenle ilgili içeriğe göre hala tercih edilen çekim yöntemlerinin en büyük nedenidir.

ROUGE yirmi yıldır baskın bir toplama metrikidir ve 2026 yılında kendi başına yeterli değildir. NLG makalelerinin büyük ölçekli bir meta-analisisinde şunlar gösterildi:
> 需要命名的幻觉类型:

- **BERTScore**(konekstüel yerleştirme benzerliği) 2023 yılına kadar yer aldı ve şimdi çoğu özet makalesinde ROUGE ile birlikte rapor edildi.
- **BARTScore**değerlendirmeyi bir nesil olarak değerlendirir: özetin kaynağı verildiğinde önceden eğitilmiş bir BART'in onu ne kadar olasılıkla tahsis ettiği ile değerlendirilmelidir.
- **MoverScore**(Earth Mover's Distance over contextual embeddings) 2025'te top noktaya ulaştı çünkü ROUGE'den daha iyi semantik üst üsteliklemeyi yakalar.
- **FactCC**ve **QA-based faithfulness**2021-2023 yılları arasında yaygın olanlar, şimdi sıklıkla **G-Eval**(GPT-4 uyarı zinciri, tutarlılık, akıcılık, düşünce zinciri akıllanmasına ilişkin uygunluk puanları).
- **G-Eval**ve benzer LLM-hakimi yaklaşımları, rubrikaların iyi tasarlandığı zaman insan yargısına eşittir.
> - **实体替换。**源说 "John Smith"―摘要说 "John Brown"―
- **数字漂移。**源说 "25,000"―摘要说"25 milyon"―
- **极性翻转。**源说 "sırayı reddetti"―摘要说 "sırayı kabul etti"―
- **事实编造。**CEO'nun onaylandığını söyledi.

Üretim önerisi: geçmiş bir karşılaştırma için ROUGE-L raporunu, semantik üst üstelik BERTScore raporunu, tutarlılık ve gerçeklik için G-Eval raporunu. 50-100 insan etiketiyle özetlere göre kalibrel.
> Etkili değerlendirme yöntemleri:

### Dördüncü adım: Gerçeklik sorunu
> - **FactCC。**Kaynak cümle ve özet cümlelerinin  içerikli ilişkisine eğitimli iki sınıfı 
- **基于 QA 的事实性检查。**K.A. 模型質問源内有答题──如果摘要支持不同的答案,标记──
- **实体级 F1。**Kaynak ve özette bulunan isimlendirilmiş varlıklar ile karşılaştırılmak için, özette bulunan varlıklar şüphelilerdir.

Abstraktif özetler halüsinasyona eğilimlidir. Ekstraktif özetler, kaynaktan sözde çıkarıldığı için çok daha düşük bir halüsinasyon riski taşır, ancak kaynak cümlelerinin bağlamsızlaştırıldığında, eskiye kalmışsa veya sıra dışı alıntı yapıldığında yanıltıcı hale gelebilirler. Bu, üretim sistemlerinin halen uyumlulık ile bitişik içerik için ekstraktif yöntemleri tercih etmesinin tek büyük nedeni.
> ⇒ Gerçeklik için önemli olan kullanıcıya yönelik içerik için ⇒ haber, sağlık, kanun, finans), çekim daha güvenli bir öntanımlı seçimdir.

Halüsinasyon türleri:

- **Entity swap.**Kaynak "John Smith" diyor. Kısacası "John Brown".
- **Number drift.**Kaynak "25.000" diyor. Özet "25 milyon".
- **Polarity flip.**Kaynak "sırayı reddetti" diyor.
- **Fact invention.**Kaynak CEO'dan bahsetmiyor.

Değerlendirme bu işe yaklaşımları:

- **FactCC.**Kaynak cümle ile özet cümlesi arasındaki bağlantıya bağlı olarak eğitilmiş ikili bir sınıflandırıcı.
- **QA-based factuality.**Kaynağında cevapları olan bir soru sor.
- **Entity-level F1.**Kaynak ve özetle ilgili isimleri karşılaştırın.

Gerçeklik önemli olan (haberler, tıbbi, yasal, finansal) kullanıcıya yönelik her şey için, ekstraksif daha güvenli bir özelliktir.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:
> 2026 yıl teknik:

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> Şekil kullanma önerisi
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


Uzun bağlamlı LLM'ler, hesaplama bir kısıtlama olmadığı 2026'da genellikle uzmanlaşmış modellerden üstün gelir.
> 2026 yılında, kalkulü sınırlama değildir, uzun süre aşağıda LLM genellikle özel modelden çok daha fazladır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-summary-picker.md`- ...
> 保存为 `outputs/skill-summary-picker.md`- ...

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## Egzersizler.

1. **Easy.**5 haber makalesinde TextRank çalıştırın. En üst 3 cümleyi referans özetle karşılaştırın. ROUGE-L ölçün. CNN/DailyMail tarzındaki makalelerde 30-45 ROUGE-L görmelisiniz.
2. **Medium.**Kuruluş düzeyinde gerçekliği uygula: Kaynak ve özetten isimlendirilmiş kuruluşları çıkarmak (spaCy), özette kaynak kuruluşlarının hesaplama geri çağırılması ve kaynak karşı özetleyici kuruluşların kesinliği. Yüksek hassasiyet ve düşük hatırlama güvenli ama kısa anlamına gelir; düşük hassasiyet halüsinasyonlu kuruluşlar anlamına gelir.
3. **Hard.**BART-large-CNN ile LLM (Claude veya GPT-4) ile CNN/DailyMail'in 50 makalesinde karşılaştırın. ROUGE-L raporunu, gerçekliği (enti F1) ve özet başına maliyetini rapor edin. Her birinin kazandığı belge.
> 1. **简单。**5 篇新闻文章上运行 TextRank──将 top-3 句子与参考摘要比较──测量 ROUGE-L──在 CNN/DailyMail 风格文章上你应该看到 30-45 ROUGE-L──
2. **中等。**實體級事實性: 源和摘要中提取命名实体 (spaCy), 摘要中的计算源实体召回率和摘要实体对源的精度率──高精度率低召回率意味着安全但简略;低精度意味着幻觉实体──
3. **困难。**50 篇 CNN/DailyMail 文章上比较 BART-big-CNN vs LLM(Claude veya GPT-4);; rapor ROUGE-L、事实性(按实体 F1) 和每个摘要的成本──记录各自的胜场景──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> # Sözcükler # İnsanlar her zaman söylerdi # Gerçek anlamı #
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) ekstraksiyon kanonik kağıdı.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)BART kağıdı.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777)Pegasus ve boş cümle hedefi.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) Kırmızı kağıt.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) gerçeklik manzarası kağıdı.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777)Pegasus ve ayrımcılık hedefleri
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文。
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) Faktörlük 
