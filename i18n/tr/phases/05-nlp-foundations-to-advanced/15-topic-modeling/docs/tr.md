# Konu Modelleme  LDA ve BERTopic  Tema Yapım  LDA ve BERTopic

> LDA: belgeler konuların karışımı, konuların kelimeler üzerinde dağılımıdır. BERTopic: belge grupları yerleşim alanında, gruplar konulardır. Aynı amaç, farklı parçalanmalar.
> LDA:文档是主题的混合,主题是词的分布──BERTopic:文档在嵌入空间中的聚类,聚类就是主题──相同的目标,不同分解──

> **【中文解读】**LDA'nın, BERTopic'in, BERT'in 嵌入式ı kullanımı ile öykü bulma modeli.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## Sorunlar. Sorunlar.

10,000 müşteri destek bileti, 50.000 haber makalesi veya 200.000 tweetiniz var. Toplumu okumadan ne hakkında olduğunu bilmeniz gerekir. Kategori etiketleri yoktur. Kaç kategori olduğunu bile bilmiyorsunuz.
> Bu koleksiyonun konularını okumadan öğrenmek zorundasın. Tanımlanmış sınıflar yok. Ne kadar sınıf var bilmiyor bile.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


Konu modeli, denetim olmadan cevaplar. Bir corpus verin, bir dizi tutarlı konuyu geri alın ve her belge için bu konuların dağıtımı.
> Tema yapılandırma, bu soruya sorgulamadan cevap vermek için bir dil kütlesini oluşturmak, bir grup devamlı temalara geri dönmek ve bu temalar üzerinde yayımlanan her belgeyi oluşturmak için bir dil kütlesini oluşturmak.

LDA (2003) her belgeyi gizli konuların bir karışımı ve her konuyu kelimelerin bir dağılım olarak ele alıyor. İndirim Bayesian'dır. Hala karışık üyelik konu görevleri ve açıklanabilir kelime seviyesindeki olasılık dağılımları gerektiği üretiminde gönderir.
> 两个算法族占主地位――LDA(2003) her makaleyi potansiyel konuların karışımı olarak görecek, her konu sözcüklerin dağılımını görecek――推断是贝叶斯的――它仍然需要你混合成员主题的分配和可解释的词级概率分布的生产中发布――

BERTopic (2020) belgeleri BERT ile kodlar, UMAP ile boyutluluğu azaltır, HDBSCAN ile kümeler oluşturur ve sınıf tabanlı TF-IDF üzerinden konu kelimelerini çıkarır. Kısa metin, sosyal medya ve kelimelerin üst üste geçmesinden daha fazla anlamlı benzerlik önemi olan her şeyi kazanır. Bir belge tek bir konu alır, bu da uzun biçimli içerik için bir sınırlama.
> BERTopic(2020) bir konuyu oluşturmak için bir makale oluşturmak için bir makale oluşturmak için bir kısıtlama oluşturur.

Bu ders hem içgüdü hem de belirli bir kitap için hangisini seçmek için isimler oluşturur.
> Bu ders, iki tarafın da içten bir anlayış oluşturması ve seçilmesi gereken bir konu belirtilmesidir.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


## Konsepten bir şey.

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**Her konu kelimelerin üzerine bir dağılımdır. Her belge bir konu karışımıdır. Bir belgedeki bir kelimeyi oluşturmak için, belge karışımından bir konu örneğini, sonra bu konu dağılımından bir kelimeyi örnekleyin. İndirim bunu tersine çevirir: gözlemlenen kelimeleri vererek, her belge başına konu dağılımını ve her konu başına kelime dağılımını çıkarın.
> **LDA 生成故事。**Her konu sözcük dağılımıdır. Her makale konu karışımıdır. Bir kelime bir makale içinde ortaya çıkarmalı, bir kelimeyi dosyanın karışımından alınmalı, sonra da bu konu dağılımından alınmalı.

Anahtar LDA çıkışı:
> 关键 LDA 输出:

- `doc_topic`: matris`(n_docs, n_topics)`, her satır 1'e (dokümanın konu karışımı) kadar.
- `topic_word`: matris`(n_topics, vocab_size)`, her satır 1'e (topik kelimelerinin dağılımı) kadar.
> - `doc_topic`:矩阵 `(n_docs, n_topics)`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,
- `topic_word`:矩阵 `(n_topics, vocab_size)`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , 1 , , , , , 1 , 1 , , , ,

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Her belgeyi cümle dönüştürücü ile kodlayın (örneğin, `all-MiniLM-L6-v2`384 boyutlu vektörler.
2. UMAP ile boyutluluğu ~5 boyutlara düşürün. BERT yerleşimleri kümeler için çok yüksek bir kalınlıkta.
3. HDBSCAN ile gruplama. Sıklık tabanlı, değişken boyutlu gruplamalar ve "outlier" etiketini üretir.
4. Her küme için, en önemli kelimeleri çıkarmak için küme belgeleri üzerinde sınıf tabanlı TF-IDF hesaplayın.
> 1. 用句子 Transformer(如 `all-MiniLM-L6-v2`)编码每篇文档──384 维向量──
2. UMP'yi kullanarak, boyut çok yüksek.
3. HDBSCAN 聚类── yoğunluk üzerine, oluşur 变大小聚类和离群值标签──
4. Her bir sınıf için, sınıf dosyalarında sınıflara dayalı TF-IDF'yi hesaplamak için en üst sınıf kelimeleri çıkarmak için:

Çıktı, her belgeye bir konu (daha -1 dışarısı etiket) ve seçeneği olarak HDBSCAN'ın olasılık vektörü üzerinden yumuşak bir üyelik.
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地,通过 HDBSCAN 的概率向量获得软成员资格──

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.


## Yapın.
```figure
topic-drift
```

## Yapın

### Adım 1: Sikit-learn üzerinden LDA
> Dikkat: kaldırıldı durdurma sözcüğü, min_df 和 max_df 过罕见和无处不在的词, CountVectorizer kullanmak, TfidfVectorizer değil) çünkü LDA 期望原始计数。

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Not: Stopwords kaldırıldı, min_df ve max_df nadir ve her yerde bulunan terimleri filtreledi, CountVectorizer (TfidfVectorizer değil) çünkü LDA çiğ sayıları bekliyor.
> `Topic != -1`Bu nedenle, bu konuyla ilgili bir bilgiyi göndermek için, bir bilgiyi gönderin.`min_topic_size`控制 HDBSCAN'ın en küçük bir kümesi;BERTopic 库默认为 10──本例为课程规模显然设置为 15── 10,000'den fazla 文档语料, 50 veya 100─

### Adım 2: BERTopic (önem)
> 两种方法都输出主题词――问题是这些词是否连贯――

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

Filtrenin açık olması .`Topic != -1`BERTopic'in dışarısı kovalarını düşürür (HDDBSCAN belgeler toplayamadı). `min_topic_size`HDBSCAN'ın en az kümeler boyutunu kontrol eder; BERTopic'in kütüphane standartı 10. Bu örnek ders ölçeği için açıkça 15'e ayarlar. 10.000'den fazla belge için 50 veya 100'e yükseltin.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI (→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→`gensim.models.CoherenceModel`配 `coherence="c_v"`- Evet.
- **主题多样性。**Tüm konuların üst düzey kelimeler arasında tek kelime oranı──越高越好──
- **定性检查。**Her konuyu okuyun. Gerçek bir şey mi adlandırıyorlar? İnsan yargıları hala son savunma hattı mı?

### Adım 3: Değerlendirme

Her iki yöntem de konu kelimelerini çıkarır.

- **Topic coherence (c_v).**Slide-fenster bağlamlarında en üst kelime çiftlerinin NPMI'sini (normalleştirilmiş nokta yönünde karşılıklı bilgi) birleştirir, puanları konu vektörlerine toplar ve bu vektörleri cosine benzerliği yoluyla karşılaştırır. Daha yüksek daha iyidir. Kullanın `gensim.models.CoherenceModel`- Evet .`coherence="c_v"`- Evet .
- **Topic diversity.**Tüm konuların en önemli kelimelerindeki benzersiz kelimelerin bölümü.
- **Qualitative inspection.**Her konuyu ilk kelimelerle okuyun.


> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Hangisini seçmek için ne zaman

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

En büyük pratik düşünce, belge uzunluğudur. BERT yerleşimleri kısaltılır; LDA, herhangi bir uzunlukta çalışmayı sayır. Yerleşim modelinin bağlamından daha uzun belgelere, ya parça + toplam veya LDA kullanın.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


## Çerçeveyi kullanın.

2026'da:
> 2026 yıl teknik:

- **BERTopic.**Kısa metin ve semantik önemli olan her şey için öntanımlı.
- **`gensim.models.LdaModel`.**Klasik LDA üretimi, olgun, savaş testinde.
- **`sklearn.decomposition.LatentDirichletAllocation`.**Deney için kolay bir LDA.
- **NMF.**Negatif olmayan matris faktörleşmesi. LDA'ya hızlı alternatif, kısa metin üzerinde karşılaştırılabilir kalite.
- **Top2Vec.**BERTopic'e benzer bir tasarım. Daha küçük bir topluluk ama bazı referans değerlerinde iyi.
- **FASTopic.**Çok büyük korpuslarda BERTopic'ten daha yeni, daha hızlı.
- **LLM-based labeling.**Her türlü gruplama çalıştırın, sonra her gruptan bir modelin adını getirin.
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**生产级经典 LDA,成熟,久经验──
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单 LDA──
- **NMF。**LDA'nın hızlı bir şekilde değiştiği, kısaca kalıcılık oranı oranı olarak
- **Top2Vec。**BERTopic'in tasarımı gibi.
- **FASTopic。**Yenilemiş, 超大语料上比BERTopic 快──
- **基于 LLM 的标注。**Her bir sınıfı kullanın, sonra da her sınıfın adını verin.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-topic-picker.md`- ...
> 保存为 `outputs/skill-topic-picker.md`- ...

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## Egzersizler.

1. **Easy.**20 Newsgroup verisi üzerinde 5 konu ile LDA'yı uygulayın. Konu başına en iyi 10 kelimeyi basın. Her konuyu el ile etiketleyin. Algoritm gerçek kategorileri buldu mu?
2. **Medium.**BERTopic'i aynı 20 Haber Grubunun alt kümesine uygulayın. Bulunan konular, en önemli kelimeler ve kalite tutarlılığı LDA ile karşılaştırın. Gerçek kategorileri hangisi daha temiz bir şekilde yüze çıkarır?
3. **Hard.**LDA ve BERTopic için her iki bölüm için de c_v tutarlılığını hesaplayın. Her birini 5, 10, 20, 50 konu ile çalıştırın. Plan tutarlılığı vs. konu sayısı. Konu sayıları boyunca hangi yöntem daha istikrarlı olduğunu bildirin.
> 1. **简单。**20 Haber Grubunda 5 konu üzerinde bir LDA hazırlanmıştır.
2. **中等。**Aynı şekilde 20 Haber Grubları'nda da BERTopic'e uygun bir grup oluşturuldu.
3. **困难。**LDA ve BERTopic'in c_v 连贯度¬ı, 5、10、20、50 题 işlemi ile hesaplanır.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> # Sözcükler # İnsanlar her zaman söylerdi # Gerçek anlamı #
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)LDA gazetesi.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic gazetesi.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)- C_v ve arkadaşları tanıtan kağıt.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) üretim referansı.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
