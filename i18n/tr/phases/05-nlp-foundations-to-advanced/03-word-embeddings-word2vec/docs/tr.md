# Word Embeddings  Word2Vec sıfırdan  Word2Vec sıfırdan gerçekleştirmek

> Bir kelime, bir şirket olarak kalır ve bu fikir üzerinde derin bir ağ oluşturur ve geometri düşer.
> Bir kelime, içinde bulunan şirketten kaynaklanır. Bu düşünce üzerinde derin bir ağ oluşturulur.

> **【中文解读】**Word2Vec Sözcükleri 密向量空间, 密向量空间中接近〜, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 密向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量空间, 向量, 向量空间, 向量空间, 向量, 向量, 向量, 向量, 向量空间, 向量, 向量, 向量, 向量, 向量量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 向量, 

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

TF-IDF biliyor .`dog`ve `puppy`Bu, farklı kelimelerdir.`dog`Bu konuda genel bir inceleme yapamazsınız.`puppy`Bu konuyu eşya ifadelerle yazabilirsiniz, ama bu nadir terimlerde, domain jargonunda ve tahmin edemediğiniz her dilde başarısız olur.

> TF-IDF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `dog`和 `puppy`Farklı kelimeler var. Onların anlamı neredeyse aynı.`dog`Üst eğitim sınıflandırma makinesi hakkında genişleme imkanı yok.`puppy`Bu, çok nadir bir terimdir ve her dilde başarısız olacağını tahmin edemediğin bir şekilde başarısız olur.

Bir temsilcilik istiyorsun .`dog`ve `puppy`Uzayda birbirine yakın bir yere yerleşmek.`king - man + woman`Yakın bir yerde`queen`- Bir modelin eğitim aldığı yer .`dog`Bir sinyal aktarıyor `puppy`- Ücretsiz.

> Bir ifade istiyorsun,让 `dog`和 `puppy`Yörede yakın ol.`king - man + woman`- Ben de öyleyim .`queen`Yakınlıkta.`dog`Üncelik modelleri ücretsiz`puppy`- Bir kaç sinyal gönder.

Word2Vec bize bu alanı verdi. İki katlı sinir ağı, trilyonlarca token eğitim çalışması, 2013 yılında yayınlandı. Mimarlık neredeyse utanç verici bir şekilde basit. Sonuçlar bir on yıl boyunca NLP'yi yeniden şekillendirdi.

> Word2Vec bize bu tür bir alanı sağladı. İki katlı sinir ağları, Milliard Token'lar için eğitim yürütülüyor, 2013 yılında yayınlandı.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**Distributional hypothesis**Birinci, 1957: "Bir kelimeyi, onun tutduğu arkadaşlıktan anlayacaksın".

> **分布假设（Distributional Hypothesis）**(Birinci, 1957):"Bir kelimenin içinde bir şirketin içinde onu tanıyacaksın". Eğer iki kelime benzer bir şekilde ortaya çıkarsa, muhtemelen benzer şeyler anlamına gelecektir.

Word2Vec iki çeşitlikte gelir. Her ikisi de bu fikri kullanıyor.

> Word2Vec'in iki farklı yönü var.

- **Skip-gram.**Merkezi kelime verildiğinde, çevresindeki kelimeleri tahmin et.`cat -> (the, sat, on)`Pencere boyutu 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, penceresi büyüklüğü 2
- **CBOW (continuous bag of words).**Etrafta sözcükler varken, merkezi tahmin et.`(the, sat, on) -> cat`- Evet .
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词──`(the, sat, on) -> cat`- Evet.

Skip-gram daha yavaş eğitimlenir ama nadir kelimeleri daha iyi ele alır.

> Skip-gram                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

Ağ, doğrusallık olmayan bir gizli katman vardır. Giriş sözlük üzerinde bir sıcak vektördür. Çıktı sözlük üzerinde bir yumuşak maksimum. Eğitimden sonra, çıkış katmanı atarsınız. Gizli katman ağırlıkları yerleşimlerdir.

> 网络 has an un带 nonlinear activation function's hidden layer──输入 is one-hot 向量──输出 is softmax on wordtable── eğitimden sonra, output layeri terk ettin── hidden layer'ın ağırlığı is embed──

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

Yaptığımız şey: 100 bin kelimeyi aşan softmax çok pahalı.**negative sampling**Bu nedenle, bu konektör kelimeyi bir ikili sınıflandırma görevine dönüştürmek için bir ikili sınıflandırma görevi oluşturmak için kullanılır. "Bu bağlam kelime bu merkez kelime yakınında, evet veya hayır olarak ortaya çıktı mı?" tahmin et.

> : 100.000 words make softmax 代价太高──Word2Vec 使用**负采样（Negative Sampling）**Bu yüzden, bu konudaki bir dizi sözcüklerin birbiriyle birlikte olması için, bu sözcüklerin birbiriyle birlikte olması gerekmektedir.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
word-vector-arithmetic
```

## Yapın

### Adım 1: bir korpustan eğitim çiftleri

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

Bir penceredeki her (merkezi, bağlam) çift olumlu bir eğitim örneğidir.

> 窗口中的每个(中心词,上下文词)对都是一个正正训练样本──

### Adım 2: Masalar yerleştirme

İki matris.`W`Ortadaki kelimenin yerleştirme masası (sağlam). `W'`Bu, bağlamlı kelime tablosudur (sık sık atılır, bazen ortalama olarak `W`)

> İki tane.`W`Evet, bu da bir şey.`W'`Evet, bu da bir şey.`W`取平均) ⋅

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

Küçük rastgele başlangıç. 10k ve dim 100 kelime boyutu gerçekçi; öğretim için, 50 kelime x 16 dim jeometri görmek için yeterlidir.

> Küçük zamanlı başlangıç. Sözcük sayısı 10.000'dir. 100'ün boyutu gerçek.

### Adım 3: negatif örnekleme hedefi

Her olumlu çift için `(center, context)`, örnek`k`Sözcükten geleneksel kelimeler negatif olarak kullanın.`W[center] · W'[context]`Pozitifler için yüksek, negatifler için düşük.

> Her doğru örnek için .`(center, context)`, sözcük gösteriminden `k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`高,负例の低。

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

Sihirli formül: pozitif çift üzerinde lojistik kaybı (sigmoid yakınında 1) ek olarak negatif çiftlerde lojistik kaybı (sigmoid yakınında) . Gradientler her iki tabloya akıyor. Tam türev orijinal kağıtta; eğer yapışmak istiyorsanız kalem ve kağıt ile bir kez geçin.

> 神奇的公式:正例对上逻辑损失(希望 sigmoid 接近 1)加上负例对上逻辑损失(希望 sigmoid 接近 0) ・・・梯度流向两个表──完整推导见原始论文; eğer bunu derinlemesine anlamak istiyorsan, kâğıt kağıdı ile tekrar tekrar geçelim──

### Dördüncü adım: Oyuncak korpusunda eğitim

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

Büyük bir korpus üzerinde yeterince zaman geçtikten sonra, bağlamları paylaşan kelimelerin merkezi benzerliklere sahiptir. Oyuncak korpusunda, etkisini hafifçe görürsünüz.

> Büyük dilde yeterince kez konuştuktan sonra, paylaşımdaki aşağıdaki kelimelerin benzer merkezi kelimeler yer aldı. Oyuncak dilde etkisi zayıfladı.

### 5. Adım: Analogya hilesi

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

Önceden eğitilmiş 300d Google Haber vektörlerinde:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`- Çünkü model, kraliyetten bahsettiğini biliyor.`(king - man)`"krallık" gibi bir şey yakalar ve ekler.`woman`Kraliyet kadınları bölgesinin yakınlarında yer alan topraklar.

> `king - man + woman = queen`- Ne olduğunu model bildiği için değil, ama boyutları için.`(king - man)`"Kralın evine" benzer bir şey yakaladık, onu da ekleyeceğiz.`woman`Ü落在王室女性区域附近──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Word2Vec'i sıfırdan yazmak öğretimdir.`gensim`- Evet .

> Word2Vec öğretim amacıyla yazılmıştır.`gensim`- Evet.

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

Gerçek iş için neredeyse hiç Word2Vec'i kendin eğitmiyorsun.

> 实际工作中,你几乎从不自训练 Word2Vec──你下载预训向量──

- **GloVe**Stanford'un ortak oluşu matrisi faktörleşme yaklaşımı. 50d, 100d, 200d, 300d kontrol noktaları. İyi genel kapsam. Ders 04 özellikle GloVe'yi kapsar.
  **GloVe** Stanford'un ortak mevcut matç parçalanma yöntemi──50 维、100 维、200 维、300 维'nin kontrol noktası──通用覆盖良好──第 04 课专讲解 GloVe──
- **fastText** Facebook'un n-gram karakterleri içeren Word2Vec uzantısı. Sözcüklük dışındaki kelimeleri alt kelimeleri oluşturarak ele alır. Ders 04.
  **fastText** Facebook'un Word2Vec  genişletilmiş, gömülü karakter n-gram── geçişi 组合子词处理词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d, 3M kelime sözlüğü, 2013 yılında yayınlandı.
  **Google News 预训练 Word2Vec** 300 维,300万词表,2013年发布──至今每天都有人下载──

### Word2Vec 2026'da hala kazanırken

- Uzaylı bir alan özel çekim, bir saatte bir dizüstü bilgisayarla tıbbi çekimler üzerinde çalışmak, özel vektörler almak, genel modeller çekimleri olmamak.
  轻量级领域的特定检查――笔记本上一小时在医学摘要上训练,获得通用模型无法捕获的专用向量――
- Analogik tarzlı özellik mühendisliği.`gender_vector = mean(man - woman pairs)`- Başka kelimelerden çıkarıp cinsiyet tarafsızlığı elde edelim.
  类比式特征工程──`gender_vector = mean(man - woman pairs)`❖ Diğer kelimelerden çıkarıp, ❖ gense orta ⋅ aksi elde etmek için ❖ hala eşitlik araştırmasında kullanılmaktadır
- 100d, PCA veya t-SNE üzerinden çizim yapıp aslında kümeler oluştuğunu görmek için yeterince küçüktür.
  Çözülebilir. 100 维足够小, PCA veya t-SNE yoluyla 绘图并实际见聚类形成──
- Herhangi bir yerde sonuçlar GPU olmadan cihazda çalıştırılmalıdır. Word2Vec arama tek satırlı bir çekimdir.
  任何需要在没有GPU的设备上运行推理的场景──Word2Vec 查找就是单行获取──

### Word2Vec'in başarısız olduğu yerler

- Polysemi duvarı.`bank`Bir vektörü var.`river bank`ve `financial bank`Paylaşın.`table`Bir sınıflandırıcı aşağı akıntıda duyuları vektörden ayırt edemez.

> Çok anlamlı kısıtlamalar.`bank`Sadece bir yönü var.`river bank`和 `financial bank`Paylaşıldı.`table`(電子表格 vs. 家具) paylaşmak.

Konekstel yerleşimler (ELMo, BERT, her transformatör o zamandan beri) çevredeki bağlamlara göre kelimenin her bir oluşumu için farklı bir vektör üreterek bunu çözdü. Bu, Word2Vec'ten BERT'e atlama: statikten bağlamlıya.

> Ünlü kısımlardaki yerleşimler (ELMo、BERT ve sonrası tüm Transformer) ile ilgili olarak, her kelimenin ortaya çıkması için farklı yönlü bir döngü oluşturmak için bu sorunu çözdüler.

Sözcük kaynağı dışında olan sorun diğer başarısızlık.`Zoomer-approved`Eğer bu bilgi eğitim verilerinde bulunmamışsa.

> 词表外(Out-of-Vocabulary) sorun başka bir başarısızlıktir.`Zoomer-approved`Bu konuda bir çok şey var. Bu konuda bir çok şey var.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-embedding-probe.md`- ...

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## Egzersizler.

1. **Easy.**Küçük bir kurpus üzerinde eğitim döngüsünü yürütün (20 kediler ve köpekler hakkında cümle).`nearest(vocab, W, W[vocab["cat"]])`Devamı`dog`Eğer yapmazsanız, dönemleri veya kelime birikimini artırın.
   **简单。**Bir küçük dilde çalışmak için bir eğitim döngüsü içinde.`nearest(vocab, W, W[vocab["cat"]])`返回'ın üst 3 içeren `dog`Eğer yapmazsa, daha fazla seslenme.
2. **Medium.**Sık sözcüklerin alt örneklerini ekleyin.`10^-5`Bu nedenle, bu değerlerin, sıklıkla orantılı olan olasılıklara göre, eğitim çiftlerinden düşürülmesi gerekir.
   **中等。**添加高频词子采样──频率高于 `10^-5`Sözlerin sıklıkla oranına göre doğru oranı, eğitimden ortalama atılmaya yönelik olarak görülür.
3. **Hard.**20 Haber Grupları korpusunda bir model çalıştırın.`he - she`ve `doctor - nurse`Bu, araştırmacıların kullandığı bir araştırma yöntemidir.
   **困难。**20 Haber Grubları 语料上训练模型――计算两个偏见轴:`he - she`和 `doctor - nurse`将职业词投投向两轴上  报告哪个职业有最大偏见差                                                                                                                                                                                                                                                  

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Anahtar Şartlar .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Daha fazla okumak

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) negatif örnekleme kağıdı. Kısa ve okuyabilir. / 负采样论文。短小易读。
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) gradientlerin en net türü, eğer orijinal kağıtın matematiği yoğun hissederse.
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) üretim eğitim ayarları gerçekten işe yarıyor. / 真正有效的生产训练设置──
