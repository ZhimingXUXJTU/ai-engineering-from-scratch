# GloVe, FastText ve Alt Sözcük Eklentileri

> Word2Vec, her kelime için bir yerleştirme eğitimi aldı. GloVe, eşleşme matrisini faktörleştirdi. FastText parçaları yerleştirdi. BPE transformatörlere köprü yaptı.
> Word2Vec için her kelime bir yerleşim için eğitilmiştir.

> **【中文解读】**GloVe'yi kullanmak, FastText 处理子词解决 OOV 问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Word2Vec iki açık soru bıraktı.

> Word2Vec'in iki açık sorunu kaldı.

İlk olarak, online atlama grafikleri güncelleştirmek yerine, doğrudan (LSA, HAL) eşleşme matrisini faktörleştiren paralel bir araştırma hattı vardı. Word2Vec'in tekrarlayıcı yaklaşımı temelde daha iyi miydi, yoksa iki yöntemin nasıl işlediğinin farkı bir eser miydi?**GloVe**Bu nedenle, bu soruların cevapları: dikkatle seçilen bir kayıp ile matris faktörleşmesi Word2Vec'e eşleşir veya yenir ve eğitime daha az maliyet verir.

> Birinci olarak, Word2Vec'in 代法'sı doğuştan daha iyi mi yoksa sadece iki yöntemin hesaplama yönteminin insan sonucu olarak mı?**GloVe**回答: 配合精心选择的损失函数的矩阵分解匹配或超过 Word2Vec,且训练成本较低──

İkincisi, hiçbir yöntemin hiç görmediği kelimeler için bir hikayesi yoktu.`Zoomer-approved`- Evet .`dogecoin`, geçen hafta ortaya çıkan her isim, nadir bir kökenin her eğilen şekli.**FastText**Bu, karakter n-gramları yerleştirerek çözüldü: bir kelime, morfeme dahil olmak üzere parçalarının toplamıdır, bu yüzden kelime birikmesinden dışındaki kelimeler bile mantıklı bir vektör elde eder.

> İkinci olarak, hiç görülmemiş kelimelere karşı iki yöntem çözümsüz.`Zoomer-approved`- Evet.`dogecoin`、上周刚造的任何专名词、稀有词根的每变形形式──**FastText**通过嵌入字符n-gram 修复了这个问题:一个词是其各部分之和,包括语素,因此即使在词表外的词也能获得合理的向量──

Üçüncü olarak, dönüştürücüler geldiğinde, soru tekrar değişti. Söz düzeyinde kelime havuzları yaklaşık bir milyon giriş kaplıyor; gerçek dil bundan daha açık. **Byte-pair encoding (BPE)**Bu, her modern LLM için bir modern tokenizerin bir alt sözcük tokenizer olduğunu gösteriyor.

> Üçüncü, Transformer geldiğinde, sorun tekrar değişti.**字节对编码（Byte-Pair Encoding, BPE）**及其变体通过学习覆盖一切的高频子词单元词表解决了这个问题──每个现代 LLM 的每个现代分词器都是子词分词器──

Bu ders üçü de ele alır, sonra hangisine ne zaman ulaşmamız gerektiğini açıklar.

> Bu ders, bu üçü birer birer açıklar, sonra hangisini ne zaman kullanmalı, hangisini ne zaman kullanmalı, açıklar.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**GloVe (Global Vectors).**Söz-kelimenin eşleşme matrisi oluştur .`X`nerede`X[i][j]`Ne kadar sık sözcük`j`kelimenin bağlamında ortaya çıkar `i`- Tren vektörleri böyle`v_i · v_j + b_i + b_j ≈ log(X[i][j])`- Ağırlık kaybı, o kadar sık çiftler hakim değil.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, içinden `X[i][j]`Evet , evet .`j` 出现在词 `i`Ünce aşağıdaki sıklık.`v_i · v_j + b_i + b_j ≈ log(X[i][j])`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊    ◊ ◊ ◊  ◊              ◊   ◊ ◊                                                     

**FastText.**Bir kelime, karakterinin n-gramlarının toplamı ve kelimenin kendisi.`where``<wh, whe, her, ere, re>, <where>`. Sözcük vektörü, bu bileşen vektörlerinin toplamıdır.`whereupon`) bilinen n-gramlardan oluşur.

> **FastText。**Bir kelimenin öz harfi n-gram 之和加上词本身──`where`变成 `<wh, whe, her, ere, re>, <where>`△词向量是这些组件向量和──像 Word2Vec 一样训练──好处:未见过的词(`whereupon`) Bilinen n-gram 组合而成

**BPE (Byte-Pair Encoding).**Bireysel bayt (veya karakter) sözcükleri ile başlayın. Korpus'taki her yanlışı çift sayın. En sık gelen çiftleri yeni bir simgeye birleştirin.`k`Sonuç: sözlük bir sözlük`k + 256`Sık dizi (`ing`- Evet .`tion`- Evet .`the`) tek bir simge ve nadir kelimeler tanıdık parçalara ayrılır.

> **BPE（字节对编码）。**Tek kelime harfinden başlayan kelimelerden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfinden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir kelime harfden oluşan bir tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar tekrar`k`Bir sonraki 代── sonuç:`k + 256`个标志的词表,其中高频序列(`ing`- Evet.`tion`- Evet.`the`) tek bir işaret, nadir kelimeler tanıdık parçalara ayrılır.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
n5-subword-merge
```

## Yapın

### GloVe: eşleşme matrisini faktörleştir

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

İki hareketli parça isimlendirme değerinde.`f(x) = (x/x_max)^alpha`Çok sık çiftler (örneğin `(the, and)`) böylece kaybı etkilemez.`W`(merkezi) ve `W_tilde`(Kontext) tablolar. İkisini de toplamlamak, sadece bir tane kullanmakla daha iyi performans gösteren bir numara.

> 两个值得指出的关键点──加权函数 `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`Bu da bir diğer önemli konudur.`W`(中心词) 和 `W_tilde`(上下文词)表之和──对两者求和, genellikle sadece bir tanesini kullanmaktan daha iyi bir tekniktir.

### FastText: Alt kelime bilgili yerleşimler

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

Her kelime n-gram kümesi (genellikle 3 ila 6 karakter) ile temsil edilir. Söz gömülmesi n-gram gömülmelerinin toplamıdır.

> Her kelime n-gramından 集合 (önteminde 3 ila 6 karakter) gösterir.

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

Görülmeyen bir kelime için, n-gramlarının belli olduğu sürece vektör elde edilir.`whereupon`paylar `<wh`- Evet .`her`- Evet .`ere`ve`<where`- Evet .`where`Bu yüzden ikisi birbirine yakın yere düştü.

> ⇒ Görmediğiniz kelimeler için, n-gramın bir kısmı bilinmiş olduğu sürece, hala bir yönü elde edebilirsiniz.`whereupon`ile`where`共享 `<wh`- Evet.`her`- Evet.`ere`和 `<where`Bu yüzden ikisi de birbirine yakın bir yerde.

### BPE: öğrenilen sözcük sözcükleri

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

İlk iterasyon en yaygın bitişik çiftleri birleştirir.`low`- Evet .`est`- Evet .`tion`) tek bir simge haline gelir ve nadir kelimeler temiz bir şekilde kırılır.

> İlk defa 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合并 代合合合并 `low`- Evet.`est`- Evet.`tion`) tek bir simge haline gelir, r.v.

Gerçek GPT / BERT / T5 tokenizörleri 30k-100k birleşmeleri öğrenir. Sonuç: herhangi bir metin bilinen kimliklerin sınırlı uzunluklı bir dizisine tokenize edilir, hiçbir OOV yoktur.

> Gerçek GPT / BERT / T5 分词器学习 30.000 ila 100.000 kez 合并── sonuç: herhangi bir metin tarafından 分词 olarak bilinen ID'nin sınırlı boyutlı bir sırası olarak, asla OOV olmayacaktır──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Bu tür kontrol noktalarını çok nadiren kendiniz eğitirsiniz.

> Bu yüzden, pratikte, neredeyse kendinden hiç antrenman yapmıyorsun.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

Transformer çağında BPE tarzı alt sözcük tokenizasyonu için:

> 对于 Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

- Evet .`Ġ`Önceden sözcük sınırları (GPT-2 bir konvansiyon) işaretler. Her modern tokenizer bir BPE varianti, WordPiece (BERT) veya SentencePiece (T5, LLaMA) dir.

> `Ġ`Ön标记词边界(GPT-2 的约定) ・・・每个现代分词器都是 BPE 变体、WordPiece(BERT) 或 SentencePiece(T5、LLaMA) ・・・

### Hangisini seçmek için ne zaman

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-embeddings-picker.md`- ...

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## Egzersizler.

1. **Easy.**Çık .`char_ngrams("playing")`ve `char_ngrams("played")`İki n-gram kümesinin Jaccard örtüşmesini hesaplayın.`pla`- Evet .`lay`- Evet .`play`), bu nedenle FastText morfolojik variantlar arasında iyi bir şekilde aktarılır.
   **简单。**运行  İşlem`char_ngrams("playing")`和 `char_ngrams("played")`△ hesaplamak iki n-gram 集合のジャッカード 重叠度──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────`pla`- Evet.`lay`- Evet.`play`), bu yüzden FastText'in biçim değişimi arasında iyi bir göç yapmasının nedeni budur.
2. **Medium.**Uzaklaştırma`learn_bpe`Sözcük büyümesini izlemek için. Birleştirme sayısının fonksiyonu olarak her karakter başına simgeyi çiz. İlk başta hızlı bir sıkıştırma görmelisiniz, simptot olarak her simgeye yaklaşık 2-3 karakter.
   **中等。**扩展 `learn_bpe`E seguir kelimeler 增长── çizmek her sözcük karakterinin simgesi sayıları birleştirme sayılarının bir işlevi olarak── görmeniz gereken başlangıçta hızla sıkıştırılır, yaklaşık 2-3 字符/token 附近渐近──
3. **Hard.**Shakespeare'in bütün eserlerine 1k birleşim BPE eğit. Genel kelimelerin ortak isimlerle simgeleşmesini karşılaştır.
   **困难。**Shakespeare'de 1000 kez birleştirilen BPE'yi kullanarak, sık sık kullanılan kelimelerle nadir özel isimlerin birleştirilmesi için kullanılan BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'yi kullanarak, birleştirilen BPE'e karşılaştırın.

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Anahtar Şartlar .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Daha fazla okumak

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) GloVe kağıdı, yedi sayfa, hala kaybın en iyi türü. / GloVe 论文,七页,仍然是损失函数最好的推导──
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) FastText. / FastText 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) BPE'yi modern NLP'ye tanıtan makale. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) BPE, WordPiece ve SentencePiece'nin pratikte nasıl farklı olduğunu.
