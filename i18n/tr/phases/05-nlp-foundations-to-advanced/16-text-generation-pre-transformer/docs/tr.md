# Transformers'a Önceki Metin Genresimi  N-gram Dil Modelleri  Transformer  önceki metin generasyonu  N-gram 语言模型

> Bir kelime şaşırtıcı ise model kötüdür. Kafası karışıklık bir sayıyı şaşırtır.
> Eğer bir kelime şaşırtıcı ise, model çok kötüdür.

> **【中文解读】**N-gram 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Transformatörlerden, RNN'lerden, kelimeler yerleştirilmeden önce, bir dil modeli, önceki kelimenin ne kadar sıklıkla takip ettiğini sayarak bir sonraki kelimeyi tahmin ediyordu `n-1`"Kedi" → "Yata" 47 kez, "Kedi" → "sapan" 12 kez, "Kedi" → "doğaz" 0 kez sayın.

> 之前,之前 RNN 之前,之前词嵌入之前,语言模型通过统计前 `n-1`个词后面跟着当前词的频率来预测下一个词──统计 " kedi " → " otur " 出现 47 次, " kedi " → " atladı " 出现 12 次, " kedi " → " buzdolap " 出现 0 次──归结得到概率分布──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Bu n-gram dil modeli. 1980'den 2015'e kadar her konuşma tanıtıcısı, her harf kontrolcüsü ve her cümle tabanlı makine çevirisi sistemini çalıştı.

> İşte n-gram 言語模型── 1980'den 2015'e kadar, her ses tanımlayıcıında, her yazım kontrolcüsünde ve her kısa sözlere dayalı bir makinelerle çevrimiçi sistemde çalıştı.

İlginç olan sorun, görünmeyen n-gramlar hakkında ne yapılmasıdır. Çiğ sayım tabanlı bir model, görmediği herhangi bir şeye sıfır olasılık belirler, bu da felaketlidir, çünkü cümleler uzun ve neredeyse her uzun cümle en az bir görünmeyen sırayı içerir.

> İlginç bir soru şu: Görülmemiş n-gramları nasıl ele alacağız. İlk sayısal tabanlı modellerin görülmemiş herhangi bir şeye dağılımı sıfır olasılıktır. Bu felaketli bir durumdur, çünkü cümleler uzun, neredeyse her uzun cümle en az bir görülmemiş sırayı içerir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### Önceden tahmin oyunu

Bu makineler var olmadan önce bir deney dil modelinin ne olduğunu tanımladı. İngilizce cümlenin bir sonraki harfini kaplayın. Bir kişiyi doğru bir tahmin yapana kadar tahmin etmesini isteyin. Tahmin sayısını yazın. Birkaç yüz harfi tekrarlayın.

Tahmin sayıları önemsiz değildir. Bunlar metnin kaybı olmayan bir yeniden kodlamasıdır: sayım sırasını ikinci, aynı tahminciye teslim edin ve her harfi yeniden yapılandırabilirler, çünkü her pozisyonda hangi tahminlerin önce geldiğini tam olarak biliyorlar. Daha az sembolle yeniden kodlayabileceğiniz bir mesaj, her sembol için daha az bilgi taşır, bu nedenle tahmin sayım istatistikleri İngilizce entropiye bir tavan koydu.

Shannon 1951'de bunu yaptı ve bu alanı hala yönetiyen bir sayı aldı. 27 sembollü bir alfabenin (26 harf artı boşluk) taşıyabileceği bir sayı.`log2(27) ≈ 4.75`Bu nedenle, bir modelin öğrenmesi gereken yapı, herhangi bir model öğrenmeden önce ölçülmüştür.

O zamandan beri her dil modeli bu oyunun mekanik bir oyuncusu ve bu dersdeki her değerlendirme numarası da oyunun puanladığı sayı:

- **Cross-entropy loss**Bir LM'yi eğitmek, tahmin oyununda puanını azaltacak.
- **Perplexity**- Evet .`2^bits`(veya `e^nats`): modelin tahmininden sonra hala karşı karşıya olduğu dalgalama faktörü. 27 sembolden fazla teker teker tahmin etmek 27 karmaşıklığa sahiptir; bir harf başına 1 bit oynatıcının karmaşıklığı vardır 2.
- **Context length is the player's memory.**Bir trigram modeli iki hafıza jetonu ile oynar. Bir transformatör aynı oyunu 100K jetonu ile oynar. Kurallar asla değişmez. Oyuncu daha iyi olur.

Bir birimden bir parça: oyun harf başına bitler (`log2`), aşağıdaki n-gram formüller ise nats (doğal log)  ve karmaşıklıktan sonra sözcük başına puan verir.`e^H`- Evet .`2^H`Bitlerdeki iki görüntü farklı birimlerde aynı ölçümdür.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- Düzelt .`n`(genellikle üç, dört gram için dört) Sayılardan hesaplayın:

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`❖ Düzeltme`n`(三元组 genellikle 3,四元组 için 4)

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**Eğitimde görülmeyen herhangi bir n-gram, olasılık sıfır elde eder. Brown corpus üzerinde 2007 yılında yapılan bir çalışmada, 4 gramlı bir model bile eğitimde görülmemiş 4 gramın %30'unu elde ettiğini bulmuştur.

> **零计数问题。**任何训练中未见的n-gram都获得零概率──2007 Brown 语料库的研究发现, hatta dört元组模型 bile eğitim sırasında未见的四元组留下的30%──没有平滑就无法在任何实文上评估──

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**Her sayıya bir ekle.
   **拉普拉斯（加一）。**Her sayıya bir ekle. Ama nadir olaylarda çok kötü bir etki yaratıyor.
2. **Good-Turing.**Daha yüksek frekanslı olaylardan görülmeyen olaylara olasılık kütlesini frekans frekanslarına göre yeniden tahsis et.
   **Good-Turing。**                                                                                                                                                                                                                                                              
3. **Interpolation.**N-gram, (n-1)-gram, vb. tahminleri ayarlanabilir ağırlıklar ile birleştirin.
   **插值。**N-gram  n-1) -gram  等估计──
4. **Backoff.**Eğer n-gram sıfır sayıyorsa, (n-1) -gram'a geri düşersiniz.
   **回退。**Eğer n-gram 计数为零, (n-1) -gramı için geri dönerse, Katz geri döner.
5. **Absolute discounting.**Sıkı bir indirim çıkar `D`Her sayıdan, görünmeyenlere dağıtmak.
   **绝对折扣。**Tüm hesaplardan sabit indirimleri çıkarmak`D`, görülmemiş olaylara yeniden dağıtıldı.
6. **Kneser-Ney.**Kesin indirim ve aşağı sıralama modeli için akıllı bir seçim: * devam olasılığı* (bir kelime kaç bağlamda görünür) kullanmak yerine çiğ frekans.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择:使用*续接概率*(一个词出现多少上下文中) 原始频率而不是原始频率──

Kneser-Ney'in anlayışı derin. "San Francisco" da sıradan bir büyüklük. "Francisco" unigramı çoğunlukla "San. " Naive mutlak indirim "Francisco" yüksek unigram olasılığı verir (çünkü sayım yüksek). Kneser-Ney, "Francisco"'nun yalnızca bir bağlamda ortaya çıktığını ve devam olasılığını buna göre azaltdığını belirtir. Sonuç: "Francisco" ile biten bir roman büyüklüğü uygun düşük olasılık elde eder.

> Kneser-Ney'in anlayışı çok derin. "San Francisco" bir sık görülen ikili gruptur. "Francisco" birliğinin başlıca göstergesi "San" 之后──朴素绝对折扣给"Francisco" 高一元组概率(因为计数高)──Kneser-Ney'in "Francisco" sadece bir üst aşağı yazıda ortaya çıktığını,相应地降低其续概率──结果:以"Francisco"结尾的新二元组获得适当的低概率──

**Evaluation: perplexity.**Bir test setinde bir kelime başına ortalama negatif log olasılığının göstergesi. Daha düşük daha iyidir. 100'in karmaşıklığı, modelin 100 kelime arasında eşit seçtiği kadar karışık olduğu anlamına gelir.

> **评估：困惑度。**留出测试集上每字平均负对数似然的指数──越低越好──困惑度 100 含意模型的困惑程度等于中 100 词中平均选择──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
ngram-backoff
```

## Yapın

### Adım 1: Trigram sayıları

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

Giriş, simge edilen cümlelerin bir listesi. Çıktı n-gram sayılar ve bağlam sayılardır. `<s>`ve `</s>`cümle sınırları.

> 输入是分词后的句列表──输出是 n-gram 计数和上下文计数──`<s>`和 `</s>`Bu bir sınır.

### Adım 2: Laplace düzeltme

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Her sayıya 1 ekleyin. Gözden geçirilmeyen olaylara kütle ayırır, nadir bilinen olaylara da zarar verir.

>                                                                                                                                                                                                                                                               

### Adım 3: Kneser-Ney (bigram, interpolasyon)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Üç hareketli parça.`continuation_prob`Bu kelime kaç farklı bağlamda ortaya çıkıyor? (Kneser-Ney yeniliği).`lambda_prev`Bu, indirimle serbest bırakılan kütle, geri çekimi ağırlaştırmak için kullanılır.

> Üç hareketli bölüm:`continuation_prob`捕获 "这个词出现在多少不同上下文中?"`lambda_prev`Bu, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, indirimli bir ödeme yapmanın en iyi yolu olan, geri dönüştürülün.

### Adım 4: Örnekleme ile metin oluşturmak

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Örnekleme olasılıkla orantılıdır. Her tohum için her zaman farklı bir çıkış verir. Balık arama benzeri çıkış için, her adımda argmax'i seçin (açık) ve küçük bir rastlantı düğmesi (temperatura) ekleyin.

> 概率 oranı 概率 oranı 概率 oranı 概率 oranı 概率 oranı 概率 oranı 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率

### Adım 5: Kafası karışık

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Daha düşük daha iyi. Brown corpus için, iyi ayarlanmış 4 gram KN modeli 140 civarında karmaşıklığa ulaşır.

> 越低越好── Brown 语料库 için, bir dikkatli调参の四元组 KN 模型困惑度約140──Transformer 言語模型在同一测试集上15-30──差距約10倍── bu fark bu alanın yönlendirmesinin nedeni budur──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

- **Classical NLP teaching.**En net şekilde düzeltme, MLE ve karışıklığa maruz kalmak.
  **经典 NLP 教学。**En net düzlem, MLE ve karışıklık deneyimini elde edebilirsin.
- **KenLM.**N-gram kütüphanesi. Düşük gecikme önemli olduğu konuşma ve MT sistemlerinde rescorer olarak kullanılır.
  **KenLM。**生产级 n-gram 库──用作低延迟语音和MT 系统的重评分器──
- **On-device autocomplete.**- Klavyelerde üçleme modeli var.
  **设备端自动补全。**Kişilik üzerinde üç grup model vardır.
- **Baselines.**Eğer transformatörünüz KN'yi geniş bir kenara geçmezse, bir sorun var.
  **基线。**Nevrolojik dil modelinizi açıklamadan önce, her zaman n gram LM 困惑度を計算します. Eğer Transformeriniz KN'yi büyük ölçüde yenmezse, sorun vardır.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-lm-baseline.md`- ...

> 保存为 `outputs/prompt-lm-baseline.md`- ...

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**1000 cümlelik Shakespeare'in bir corpusunda bir trigram LM'yi eğit. 20 cümle oluşturun. Yerel olarak makul ama küresel olarak tutarlı olmayacaklar. Bu kanonik demo.
   **简单。**1000 cümle Shakespeare'nin dil tercümesi üzerinde eğitim üç grup dil modeli oluşturur 20 cümle oluşturur.
2. **Medium.**KN modeliniz için karmaşıklığı uzun süren Shakespeare'in bir bölümü üzerinde uygulayın. Laplace ile karşılaştırın.
   **中等。**Kayıplıkların %30-50 oranında azalması görülmelidir.
3. **Hard.**Trigram yazma düzeltmeci oluşturun: yanlış yazılmış bir kelime ve bağlamı verildiğinde, LM'de bağlam olasılıkları doğrultusunda düzeltmeler oluşturun ve sıralayın. Birkbeck yazma corpusunda değerlendirin (özel).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按 LM 下的上下文概率排序──在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) n-gram LM'lerin kanonik tedavisi ve düzeltme. / n-gram 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)Kneser-Ney'i en iyi n-gram daha düzgün olarak belirleyen kağıt.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) orijinal KN kağıdı. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) hızlı üretim n-gram LM, 2026 yılında hala gecikme hassas uygulamalarda kullanılır. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## Daha Fazla Okumak

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) hedef tanımlayan tahmin oyunu deneyi her dil modeli hala optimize eder.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) n-gram LM'lerin kanonik tedavisi ve düzeltmesi.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)Kneser-Ney'i en iyi n-gram daha düzgün olan kağıdı.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) orijinal KN kağıdı.
- [KenLM](https://kheafield.com/code/kenlm/) hızlı üretim n-gram LM, 2026'da hala gecikme hassas uygulamalarda kullanılır.
