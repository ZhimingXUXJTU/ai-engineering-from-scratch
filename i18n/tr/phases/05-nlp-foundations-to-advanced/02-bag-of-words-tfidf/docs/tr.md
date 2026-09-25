# Sözcükler Çanta, TF-IDF ve Metin Temsilcisi

> TF-IDF, 2026'da da iyi tanımlanmış görevlerde yerleşimleri yenmeye devam ediyor.
> Önceden hesaplama, sonra düşünme.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词――这是最基础的文本表示方法――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- Sözcük çantaları ve TF-IDF temsillerini sıfırdan oluşturun
  From零构建词袋模型和 TF-IDF gösterir
- Kısıtlı vektörleri, term frekansını ve ters belge frekansını anlamak
  Rar疏向量、词频和逆文档频率 anlaması
- Sikit-learn'ın CountVectorizer ve TfidfVectorizer'i üretiminde kullanın.
  Üretim sırasında kullanılır küçük öğrenme CountVectorizer & TfidfVectorizer
- TF-IDF'nin yerleşimleri ne zaman kazanıp ne zaman başarısız olduğunu bil
  TF-IDF'nin nasıl kazandığını, nasıl kaybettiğini biliyor.

## Sorunlar. Sorunlar.

Model numaralara ihtiyacı var.

> Model'in sayıları var.

Her NLP boru hattı aynı soruya cevap vermeli. Değişken uzunluklı bir token akışını bir sınıflandırıcı tarafından tüketilebilecek sabit boyutlu bir vektöre nasıl dönüştürebiliriz. Alanın ilk verdiği cevap işe yarayan en aptalca cevaptı. Sözleri sayın.

> Her NLP 流水线都都必须回答同样的问题: 流将变长的代币如何转变为固定大小的向量,使分类器能够消费――; bu alanda verilen ilk cevap en 但管用方法──数词频──做向量──;

Bu vektör, herhangi bir yerleştirme modeliyle karşılaştırıldığında daha fazla üretim NLP taşıdı. Spam filtreleri, konu sınıflandırıcıları, kayıt anomali tespitleri, arama sıralaması (BM25'den önce), duygu analizinin ilk dalgası, akademik NLP referanslarının ilk on yılı. 2026 uygulayıcıları, dar sınıflandırma görevlerinde hala ilk olarak ulaşmaktadır. Sözcük varlığı önemli olan görevlerde 400M-parametrli bir gömleyici modelinden hızlı, yorumlanabilir ve sıklıkla ayırt edilemez.

> Bu vektör taşıyan üretim NLP  uygulaması herhangi bir yerleştirilmiş modelden daha fazladır. İspia posta filtreleri, konu sınıflandırma cihazları, 日志异常检查, arama sıralaması (BM25 ortaya çıkmadan önce) 首波情感分析,学术 NLP 基准测试的第一十年. 2026 yılında uzmanlar, dar sınıflandırma görevlerinde hala ilk olarak kullanırlar.

Bu ders, sıfırdan kelimelerden bir çanta oluşturur, sonra TF-IDF, sonra üç satırda aynı şeyi yapan bir scikit-learn gösterir. Sonra yerleşimlere ulaşmanızı sağlayan başarısızlık modunu adlandırır.

> Bu ders, sıfır yapılandırma sözcük modelinden, sonra TF-IDF yapılandırma ve daha sonra küçük bir öğrenme biçimini gösterir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**Bag of Words (BoW)**Her belge için, her kelime birikimi kelimesinin kaç kez ortaya çıktığını sayın.`i`kelimelerin sayımıdır.`i`- Evet .

> **词袋模型（Bag of Words, BoW）**抛弃顺序──对每文档,统计每词表词出现的次数──向量长度是词表大小──位置 `i`Evet , evet .`i`- Evet.

**TF-IDF**Bu, bir tek belgeye ait bir kelime, yani bir sinyal, yani bir kelime.

> **TF-IDF**BoW için ağırlık artışı. Her dosyada sözcüklerin sayısı çok azdır. Bu nedenle, ağırlığını azaltır.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

Nerede ?`TF`belgede terim sıklığıdır, `df`belgelerin sıklığı (sözü içeren kaç belge),`N`Bu, toplam belgeler.`log`Her yerde bulunan kelimelerin ağırlığını sınırlı tutar.

> İçlerinden `TF`Evet, bu çok güzel bir şey.`df`Bu kelimeyle ilgili bir makale var.`N`Bu da bir kayıt.`log`Sözlerin ağırlığını korumak için kullanılır.

Ana özellik: her ikisi de yorumlanabilir eksilerle nadir vektörler üretir. Eğitimli bir sınıflandırıcının ağırlıklarına bakabilir ve hangi kelimeleri her sınıfın yönüne doğru bir belgeyi itiyor okuyabilirsiniz. Bunu 768 boyutlu bir BERT gömleği ile yapamazsınız.

> 关键特性: Her ikisi de açıklanabilir bir etkisi olan nadir eğilimi oluşturuyor. İyi bir sınıflandırma makinesi ağırlığını görebilir, hangi kelimelerin her sınıf için dosya yönlendireceğini okuyabilirsiniz. Bunu 768 维'li BERT 嵌入 ile yapamazsınız.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
bow-tfidf
```

## Yapın

### Adım 1: Sözlük birikimi oluşturun

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Giriş: Tokenized belgeler listesini (her kelime seviyesindeki tokenizer yapacaktır; `code/main.py`Bu ders basitleştirilmiş küçük harflerle kullanılır.`{word: index}`Dict. Stabil ekleme sırası, sözcük indeksi 0'nın ilk belgede görülen ilk kelime olduğunu gösterir.

> 输入:token 化的文档列表(任何词级分词器都可以;本课的 `code/main.py`Uygulamayı basitleştirmek için kullanılır`{word: index}`字典──稳定的插入顺序 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符符符 字符符 字符索引 0 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 字符 序 字符 字符 字符 序 字符 字符 字符 字符 字符 字符 字符 字符 符 符 符 符 符 符 符 符 序 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符 符

### Adım 2: Sözler çanta

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

Satırlar belge, sütunlar sözlük indeksleri.`[i][j]`"Ne kadar defa sözcük"`j`Belgede görünmektedir `i`Dok. 1'nin yaptığı.`cat`- Doktor, iki kez oldu.`ran`- Hayır, çünkü sıfır.

> 行是文档──列是词表索引──条目 `[i][j]`Evet , evet .`j`Dosyalarda .`i`İçinde kaç kez ortaya çıktı?`cat`Çünkü gerçekten iki kez ortaya çıktı.`ran`Çünkü ortaya çıkmadı.

### Adım 3: Sözleşme sıklığı ve belge sıklığı

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

İki tane düzeltme numarasını anmaya değer.`(n+1)/(d+1)`kaçınılması `log(x/0)`- Arka tarafta .`+1`Bu, her belgedeki bir kelimeyi hâlâ IDF 1 (değil 0) olarak oluşturur ve scikit-learn'ın öntanımlı metniyle eşleşir.`log(N/df)`Her ikisi de çalışır, düzeltilmiş versiyon daha dostça.

> Dikkat edilmeye değer iki düzlem teknikleri:`(n+1)/(d+1)`避免 `log(x/0)`ᅳ尾部の`+1`                                                                                                                                                                                                                                                              `log(N/df)`两种都有效;平滑版本更友好

### 4. Adım: TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

Üç belge, beş kelime kelime (`the`- Evet .`cat`- Evet .`sat`- Evet .`dog`- Evet .`ran` ).`the`Üçünde de görülüyor, bu yüzden IDF'si düşük.`dog`Vectörler nadir (çoğu giriş küçüktür) ve ayrımcı kelimeler pop.

> Üç tane kayıt, beş tane ifade`the`- Evet.`cat`- Evet.`sat`- Evet.`dog`- Evet.`ran`)。`the`Tüm üç dosya arasında ortaya çıkmıştır, bu yüzden IDF'si çok düşük.`dog`Sadece bir dosyada ortaya çıkıyor, bu yüzden IDF  çok yüksek ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅  ⋅ ⋅                                                                                                                                                                                                                

### Adım 5: L2- sırayı normalleştir

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

Normalleşme olmadan, daha uzun bir belge daha büyük bir vektör alır ve benzerlik puanlarına hakim olur. L2 normalleşmesi her belgeyi birim hipersferine yerleştirir.

>                                                                                                                                                                                                                                                               

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Scikit-Learn üretim versiyonunu gönderir.

> Sikit-learn 提供了生产级版本──

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`Tek bir çağrıda işaretleme, kelime depolama ve BoW yapar. `TfidfVectorizer`Bu sayede, L2 normalleştirme ve IDF ağırlığı eklenir. Her ikisi de nadir matrisler gönderir. 100k belgeler için, yoğun versiyon hafıza girmez; sınıflandırıcı yoğun talep edene kadar nadir kalır.

> `CountVectorizer`Bir kez调用中完成分词、构建词表和 BoW。`TfidfVectorizer`增加了 IDF 加权和 L2 归结化──两者都回归稀疏矩阵──10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏──

Her şeyi değiştiren düğmeler:

> 改变一切的关键参数:

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### TF-IDF hala kazanırken (2026 itibariyle)

- Spam tespit, konu etiketleme, kayıt anomali işaretleme.
  垃垃邮检测、主题标注、日志异常标注──词的存在与否是关键;语义细微差不重要──
- Düşük veri rejimleri (yüzlerce etiketlenen örnek). TF-IDF artı lojistik geri dönüşü, eğitim öncesi maliyetlere sahip değildir.
  低数据场景(100标注样本) ――TF-IDF 加逻辑回归没有预训成本──
- TF-IDF artı bir çizgisi model mikrosekundada cevap verir.
  任何延迟敏感场景──TF-IDF 加线性模型的响应时间是微秒级──通过变压器 嵌入一个文档需要10-100毫秒──
- Bu sistemler tahminlerini açıklamalı, sınıflandırıcının katılıklarını incelemeli, en iyi kelimeler neden oluyor.
  需要解释预测结果的系统──检查分类器的系数──排名最高正权重词就是原因──

### TF-IDF'nin başarısız olması

Semantik körlük başarısızlığı.

> 语义盲点──考虑以下两个文档:

- "Film hiç de iyi değildi".
- "Film mükemmeldi".

Birincisi olumlu, birincisi olumlu, TF-IDF üst üstelik tam olarak aynı.`{the, movie, was}`Bir kelime kese sınıflandırıcısı bu kelimeyi ezberlemesi gerekir .`not`Yakınlıkta`good`Bunu yeterli veriyle öğrenebilir ama sözcük anlamlı bir model kadar zarif bir şekilde asla.

> Bir negatif değerlendirme, bir de kesin değerlendirme.`{the, movie, was}`                                                                                                                                                                                                                                                              `good`Yakınlık`not`Bu noktayı yeterince veriyle öğrenebilir ama asla bir dil anlayışı modeli gibi güzel olmayacaktır.

Diğer başarısızlık: Sözcük kaynağı dışındaki kelimeler sonucu. IMDb incelemelerinde eğitilmiş bir BoW modeli neyle uğraşacaklarını bilmiyor `Zoomer-approved`Bu, bir eğitim sırasında hiç ortaya çıkmamış bir token olarak görülür.

> 另一个失败:推理时的词表外(Out-of-Vocabulary, OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`Eğer bu token, bu sorunu çözmek için çalıştırılmamışsa,

### Hibrit: TF-IDF ağırlıklı yerleştirmeler

Ortalama veri sınıflandırması için 2026 pragmatik varsayım: sözcük yerleştirmelerine dikkat etmek için TF-IDF ağırlıklarını kullanın.

> 2026 yıl ortalama veriler sınıfı pratik öntanımlı program: TF-IDF 权重作为词嵌入的注意──

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

Bu, duygu, konu ve niyet sınıflandırması için kendi başına 50k etiketli örnekten daha düşük performans gösterir.

> Bu, TF-IDF'den nadir sözcükler üzerinde eğitim aldığınızda, yerleşimden anlamlı yetenekler elde ettiniz.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-vectorization-picker.md`- ...

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## Egzersizler.

1. **Easy.**Uygulama`cosine_similarity(doc_vec_a, doc_vec_b)`L2 normallaştırılmış TF-IDF çıkışında. Aynı belgelerin 1.0 puanı ve ayrılmış sözcüklük belgeleri ise 0.0 puanı verilir.
   **简单。**L2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `cosine_similarity(doc_vec_a, doc_vec_b)`▽验证 Aynı dosya skorı 1.0 ,词表完全不相交的文档 skorı 0.0──
2. **Medium.**Ekle`n-gram``bag_of_words`Parametre .`n`Üretir sayılar `n`- Gram, bunu test et.`n=2`- Evet .`["the", "cat", "sat"]`Büyük bir miktar hesaplar üretir.`["the cat", "cat sat"]`- Evet .
   **中等。**Çı`bag_of_words`添加 `n-gram`支持──参数 `n` oluşuyor`n`-gramın sayıları--- test`n=2`时  `["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`- Evet.
3. **Hard.**Yukarıda bulunan TF-IDF ağırlıklı gömülü hibridini GloVe 100d vektörleri kullanarak oluşturun (bir kez indir, önbelleğe). 20 Newsgroups veri kümesindeki sıradan TF-IDF ve sıradan ortalama birleştirilmiş gömülmelerle sınıflandırma doğruluğunu karşılaştırın.
   **困难。**GloVe 100 维向量 (GloVe 100 维向量) ]]> Üstteki TF-IDF + haklı yerleştirme karışımı programını oluşturmak.

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Anahtar Şartlar .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Daha fazla okumak

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) Kanonik API referansı, her düğmede notlar eklenir. / 权威 API 参考,以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) TF-IDF'i on yıl boyunca default yapan makale. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026'da eski yöntem ne zaman ve neden kazanırsa ele alın. / 2026 yıl eski yöntemle ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa ne zaman kazanırsa
