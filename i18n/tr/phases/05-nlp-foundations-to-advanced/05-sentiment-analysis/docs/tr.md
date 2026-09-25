# Duygu analizi.

> Klasik metin sınıflandırması hakkında bilmeniz gerekenlerin çoğu burada gösterilmiştir.
> En klasik NLP görevleri. Bilmeniz gereken en büyük kısım burada.

> **【中文解读】**判断文的情感倾向──是NLP最经典的分类任务之一──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

"Yemek çok iyi değildi". İyi mi kötü mi?

> "Yemek çok iyi değildi". "Doğru mu, olumsuz mu?"

Duygular basit görünüyor. Bir eleştirmen bir şeyi beğendiğini veya beğenmediğini söyledi. cümleyi etiketleyin. Kanonik NLP görevi haline gelmesinin nedeni, her kolay görünen durumun zor birini saklamasıdır. İtiraz anlamını tersine çevirir. Sarkazm onu tersine çevirir. "Hiç fena değil" iki negatif kodlanmış kelime olmasına rağmen olumlu olur. Emojis çevresindeki metinden daha fazla sinyal taşır.`tight`Müzik incelemesi vs.`tight`moda incelemesinde).

> 情感分析听起来简单――评论员说喜欢或不喜欢什么――标记句子――它之所以成为经典 NLP 任务,是因为每个看似简单的案例背后都隐藏着一个困难的案例――否定翻转含义――刺反转含义――"Hiç fena değil"`tight`Zamanla birlikte`tight`)。

Sentiment klasik NLP için bir çalışma laboratuvarıdır. Eğer her naif temel çizginin neden belirli bir başarısızlık moduna sahip olduğunu anlarsanız, her zengin modelin neden icat edildiğini anlarsınız. Bu ders, naif Bayes temel çizgisini sıfırdan inşa eder, lojistik geri dönüşü ekler ve üretim duygusunu bir uyumluluk derecesi sorunu yapan tuzakları isimlendirir.

> 情感分析 klasik NLP'nin çalışma laboratuvarıdır. Eğer her basit temelinin neden belirli bir başarısızlık modeli olduğunu anlarsanız, her zengin modelin neden ortaya çıktığını anlarsınız. Bu ders, basit basit temellerden başlayarak mantıksal geri dönüşü ekler ve üretim duygusal analizini uyumlu bir sorunun tuzağına dönüştürdüğünü belirtir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

Klasik duygu iki adımlı bir tarif.

> Klasik duygu analizi iki adımlı bir çözümdür.

1. **Represent.**Metni bir özellik vektörüne dönüştürün.
   **表示。**Bu, bir diğer devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde bir devirde birde bir devirde bir devirde birde bir devirde bir devirde birde birde bir devirde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde birde bir
2. **Classify.**Etiketlenmiş örneklere bir çizgisi model (Naive Bayes, lojistik gerileme, SVM) uygulayın.
   **分类。**Etiket örneği üzerinde uygun 線性模型 (SVM) ⋅

Bayes'in en aptalca modelini kullanırken, her özellik etiketi göz önüne alındığında bağımsız olduğunu varsayalım.`P(word | positive)`ve `P(word | negative)`Bu nedenle, "sürekli" bağımsızlık varsayımı gülünç bir şekilde yanlış ve sonuçlar şaşırtıcı derecede güçlüdür.

> Basitçe Beyaz'ın en iyi ama kullanışlı modeli vardır.`P(word | positive)`和 `P(word | negative)`◊ Düşünce zamanında olasılık çarpıtıyor. "sadece" bağımsızlık hipotezi komik, ama sonuçlar şaşırtıcı yerlerde.

Logistik gerileme bağımsızlık varsayımını düzeltir. Negatif ağırlıklar dahil her özellik için bir ağırlık öğrenir. `not good`Bayes'in bence bunu hiç etiketlemediği bir büyüklük için yapamaz.

> 逻辑归修复了独立性假设──它为每个特征学习一个权重,包括负权重──`not good` As binary组 characteristics gain negative weight──Pole Bayes, hiç işaretlenmemiş binary组'lara karşı bu noktaya ulaşamadı.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
sentiment-logits
```

## Yapın

### Adım 1: Gerçek bir mini veri kümesi

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

Gerçek çalışmalarda on binlerce örnek kullanılır (IMDb, SST-2, Yelp polaritesi).

> Bu yüzden çok küçük bir çalışma yapıyorum.

### Adım 2: Multinomal Naive Bayes sıfırdan

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

Ekleyici düzeltme (alfa=1.0) Laplace düzeltmesidir. Bu olmadan, bir sınıfta görülmeyen bir kelime olasılık sıfırdır ve log patlar. `alpha=0.01`Bu, pratikte yaygın bir durumdur.`alpha=1.0`öğretim açısından yanlış.

> Gafa平滑(alfa=1.0) 拉普拉斯平滑──没有它,一个类别中未见的词概率为零,log会爆炸──实践中 `alpha=0.01`Çok sık görüyorum.`alpha=1.0`Öğrenme özelliği:

### Adım 3: Lojiistik geri dönüş sıfırdan

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

L2 düzenlenmesi burada önemlidir. Metin özellikleri nadirdir; L2 olmadan model eğitim örneklerini ezberler.`0.01`ve sesini dinle.

> L2 düzenlenmesi burada çok önemlidir. Metin özellikleri nadirdir; hiçbir L2 modeli antrenman örneğini hatırlayacaktır.`0.01`開始调参。

### Adım 4: Yükleme inkârı (kararlılık modu)

"Yok iyi" ve "kötü" düşünün.`{not, good}`ve `{not, bad}`Bir bigram sınıflandırıcısı görüyor.`not_good`ve `not_bad`Bu, genellikle yeterli olur.

> "İyi değil" ve "kötü değil" diye düşün.`{not, good}`和 `{not, bad}`Eğitimden hangisinin daha fazla öğrenmesi gerektiğine göre.`not_good`和 `not_bad`作为不同特征学习──通常就够了──

Bigramlar olmadığında işe yarayan bir çirkin ilaç:**negation scoping**. Negasyon kelimesinin ardından ön işaretler `NOT_`Bir sonraki noktalama kadar.

> Bir daha kaba ama iki binli bir grup olmadan geçerli bir düzeltme:**否定范围标记**                                                                                                                                                                                                                                                              `NOT_`Önceki, sonraki işaret noktası.

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

Şimdi .`good`ve `NOT_good`Bu, bir grup farklı özelliklere sahip olan bir grup sınıflandırıcı tarafından karşı tarafa ağırlıklandırılabilir.

> Şimdi .`good`和 `NOT_good`Bu özellikler farklı özelliklerdir. Sınıflama cihazları karşı tarafa ağırlık verebilir.

### Adım 5: Önemli değerlendirme ölçümleri

Düzgünlük, sınıfların dengesiz olması halinde yanıltıcıdır. Gerçek duygu korporası genellikle %70'den %80'e olumlu veya %70'e oranla negatifdir; sabit çoğunluk sınıflandırıcısı %80'e doğru olur ve değersizdir. Aşağıdaki her birini bildirin:

> Eğer sınıf dengesizse, sadece doğrulama oranı yanlış yönlendirilir. Gerçek duygusal ifade genellikle %70'den %80'e doğru veya %70'e negatifdir.

- **Per-class precision and recall.**Sınıf başına bir çift, sınıf dengesini koruyan tek bir sayı elde etmek için onları makro ortalama yapın.
  **每类精确率和召回率。**Her sınıf bir çift, büyük ortalama bir sınıf dengesi bir tek sayı elde eder.
- **Macro-F1 (primary metric for imbalanced data).**Sınıflar dengesiz olduğunda bu doğruluğu kullanmak yerine kullanın.
  **Macro-F1（不平衡数据的主要指标）。**F1 sınıfı bölümlerinin ortalama değeri, eşit ağırlık.
- **Weighted-F1 (alternative).**Makro gibi ama sınıf frekansı ile ağırlıklı.
  **Weighted-F1（替代方案）。**Büyük ortalama ile aynı ama sınıf frekansına göre artı­rın­cı­dan, kendi içinde dengesizlik iş anlamı bulunduk­da, Makro-F1 ile bir rapor­tan­
- **Confusion matrix.**Herhangi bir skalar metrikte güvenmeden önce her zaman kontrol edin; modelin hangi sınıf çiftini karıştırdığını ortaya çıkarır.
  **混淆矩阵。**İlk sayı: herhangi bir değer göstergesi önceden sürekli kontrol; modelin hangi sınıflara karıştığını ortaya çıkarır.
- **Per-class error samples.**Sınıf başına 5 yanlış tahmin çıkar ve oku.
  **每类错误样本。**Her sınıf 5 yanlış öngörüyü çekmektedir. Onları okuyor. Gerçek yanlışları okuyuyor.

Ağır dengesizlik (> 95-5 oranı) veriler için rapor **AUROC**ve **AUPRC**AUPRC, çoğunlukla önem verdiğiniz azınlık sınıfına karşı daha duyarlı (spam, dolandırıcılık, nadir duygu).

> 对于严重不平衡的数据(> 95-5 比例), rapor **AUROC**和 **AUPRC**Bu, genellikle sizin için önemliydi.

**Common bug to avoid.**Mikro-F1 yerine makro-F1 oranında dengesiz veriler raporlamak, çoğunluk sınıfının baskın olduğu için yüksek görünen bir rakam verir.

> **常见错误。**Mikro-F1 değil makro-F1 olarak dengesiz verilerden rapor ederken, çok yüksek görünen bir rakam verir çünkü çoğunluk tarafından yönlendirilir.

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Sikit-Learn altı satırda yapar, doğru.

> Sikit-learn 六行代码搞定,而且正确──

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Dikkat edilmesi gereken üç şey var.`stop_words=None`- Hayır.`ngram_range=(1, 2)`Bigramlar ekliyor.`not_good`Bir özellik haline gelir.`sublinear_tf=True`Bu üç işaret, SST-2'de %75 ve %85 doğruluklı bir başlangıç arasındaki farkı temsil eder.

> Üç dikkat edilmesi gereken yer...`stop_words=None`Bırakın beni terk et.`ngram_range=(1, 2)`添加二元组使 `not_good`成为特征――`sublinear_tf=True`抑制重复词── bu üç belirti, SST-2'nin %75 ve %85 doğruluk oranı arasındaki farkı oluşturur.

### Transformatörün ne zaman kullanılması gerekiyor?

- Klasik modeller burada başarısız oluyor.
  刺检测── klasik model burada başarısız olacaktır── hiçbir istisna yok──
- Uzun incelemeler, içgüdülerin değişmesi.
  情感在文档中转变的长评论──
- "Kamera harika ama pil berbat". Sadece transformörler veya yapılandırılmış çıkış modellerine ilişkin duyguları yönlendirmelisin.
  基于方面情感分析──"Kamera harika ama batarya korkunçtu".
- İngilizce olmayan, düşük kaynaklı diller. Çok dilli BERT size sıfır çekim temelini ücretsiz olarak verir.
  İngilizce değil, düşük kaynaklı diller.

Yukarıdaki herhangi birine ihtiyacınız varsa, 7. aşamaya geçin (transformatörler derin dalış). Aksi takdirde, Naive Bayes veya TF-IDF artı bigramlar artı inkar eleştirisi 2026 üretim başlangıç çizginizdir.

> Eğer herhangi bir şeye ihtiyacınız varsa, 7. aşamaya atlayın. Yoksa, TF-IDF'de basit bir işleme veya mantık geri dönüşü 2026 yılındaki üretim temelini oluşturur.

### Tekrarlanılabilirlik tuzağı (yeniden)

Duygu modellerini yeniden eğitmek rutin bir şey. Onları yeniden değerlendirmek değildir. Kağıtlarda bildirilen doğruluk rakamları belirli bölünmeler, belirli önceden işleme, belirli işaretleme kullanır. Yeni modelinizi aynı boru hattını kullanmadan bir temel çizgiyle karşılaştırırsanız yanıltıcı deltalar elde edeceksiniz. Kağıt numarası değil, boru hattınızdaki temel çizgiyi her zaman yenilenti yapın.

> 重新训练情感模型是常规操作――重新评估却不是――论文中报告的准确率数字使用特定数据分分、特定预处理、特定分词器―― Eğer yeni modelle基线 karşılaştırmak için tamamen aynı akış 线 kullanmazsanız, yanlış yönlendirme farkı elde edersiniz―― daima makaledeki sayıların yerine, akış 线inizde yeniden üretilen基线 üzerinde yeniden oluşturulur.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-sentiment-baseline.md`- ...

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Egzersizler.

1. **Easy.**Ekle`apply_negation`Scikit-Learn borusunda bir önceden işleme adımı olarak ve küçük bir duygu verisi kümesi üzerinde F1 delta ölçülmesi.
   **简单。**- Ben de .`apply_negation` Küçük bir duygusal veri kümesi üzerinde F1  değişimleri ölçmek için 
2. **Medium.**Sınıf ağırlığıyla lojistik gerilemeyi uygulayın (geçer `class_weight="balanced"`90-10 sınıf dengesizliği üzerinde etkisini ölçün.
   **中等。**实现类别加权逻辑归归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅                                                                                                                                                                                                                                                        
3. **Hard.**Bir sarkasma algılayıcısı oluşturmak için, duygu modelinin kalıntıları üzerine ikinci bir sınıflandırıcıyı eğit. Deneysel ayarınızı belgeleyin.
   **困难。**Duygu modelinin gerideği üzerinde antrenman yaparak 刺 testerini oluşturmak için ikinci sınıflandırma makinesi oluşturun. Deneyim ayarlarını kaydet. 刺                                                                                                                                                                                                                                           

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Anahtar Şartlar .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Daha fazla okumak

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) temel araştırması. Uzun, ama ilk dört bölüm her şeyi kapsar.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) Bigrams + Naive Bayes'i gösteren makale kısa metin üzerinde yenilmek zor. / 证明二元组 + 朴素贝叶斯在短文上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) referans için `CountVectorizer`- Evet .`TfidfVectorizer`, ve her düğmeye ayarlayacaksın. / `CountVectorizer`- Evet.`TfidfVectorizer`及你将调参的每个参数的参考──
