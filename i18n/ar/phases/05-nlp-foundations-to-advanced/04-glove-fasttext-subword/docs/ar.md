# GloVe، FastText، و مضخات الكلمات الفرعية

> قام Word2Vec بتدريب إضافة واحدة لكل كلمة. قام GloVe بتحليل المصفوفة المشتركة. قام FastText بتدريب الأجزاء. وصل BPE إلى المحولات.
> Word2Vec 为每个词训练一个嵌入──GloVe 分解共现矩阵──FastText 嵌入词的组成部分──BPE 桥接到变压器──

> **【中文解读】**استفادة العالم من جميع المواقع المشتركة، الفوركس الفوري 处理子词解决 OOV 问题。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

كلمة2فيك تركت سؤالين مفتوحين

> كلمة2Vec  left left left دو مسألة مفتوحة:

أولاً ، كان هناك خط متوازي من البحوث الذي يعدل معامل التواصل المباشر (LSA ، HAL) بدلاً من إجراء تحديثات المخططات عبر الإنترنت. هل كان نهج Word2Vec المتكرر أفضل أساساً ، أم أن الفرق كان عبارة عن عبارة عن طريقة التعامل مع الطرقين تعتبر مهمة؟ **GloVe**أجاب: تعديل المصفوفات مع خسرة مختارة بعناية تطابق أو تفوق Word2Vec، وتكلفة أقل للتدريب.

> أولاً، هناك طريق بحثي متوازي، يُفكّر مباشرة المُتواجدات المُحددة (LSA、HAL) ، بدلاً من القيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام بالقيام**GloVe**回答了:配合精心选择的损失函数矩阵分解匹配或超过 Word2Vec,且训练成本较低

ثانياً، لم يكن لدى أي منهج قصة لأقوال لم يسبق له رؤيتها.`Zoomer-approved`،`dogecoin`، أي اسم مناسب تم اختراع الأسبوع الماضي، كل شكل مُلتف من جذور نادرة**FastText**وصلح هذا من خلال إدراج حرف n-جرام: كلمة هو مجموع أجزائها، بما في ذلك المورفيمات، حتى الكلمات خارج المفردات الحصول على متجه معقول.

> ثانياً، هناك طريقتان لا توجد حلول لهذه الكلمات التي لم نرها من قبل.`Zoomer-approved`.`dogecoin`、上周刚造的任何专名词、稀有词根的每变形形式──**FastText**من خلال إدخال الحروف n-gram ، قمنا بإصلاح هذه المشكلة: كلمة هي كل جزء منها ، بما في ذلك الكلمة ، لذلك حتى الكلمات خارج الكلمة يمكن الحصول على حجم معقول.

ثالثا، بمجرد وصول المحولين، تغيرت السؤال مرة أخرى. قاموس مستوى الكلمات يحتوي على حوالي مليون إدخال؛ اللغة الحقيقية أكثر انفتاحا من ذلك. **Byte-pair encoding (BPE)**و حل أقاربها هذا عن طريق تعلم المفردات من الوحدات الفرعية المتكررة التي تغطي كل شيء. كل رمز الحديث لكل ماجستير في العلوم الحديثة هو رمز الفرعية.

> ثالثا، عندما جاء المحول، تغيرت المشكلة مرة أخرى.**字节对编码（Byte-Pair Encoding, BPE）** وتغيراتها من خلال تعلم تغطي كل شيء                                                                                                                                                                                                                                                         

هذا الدروس يذهب على كل ثلاثة، ثم يشرح ما يجب الوصول إلى متى.

> هذه الدروس تُفسر هذه الثلاثة، ثم تُفسّر متى تستخدم أيّها.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**GloVe (Global Vectors).**بناء المصفوفة المشتركة الكلمة الكلمة`X`أين`X[i][j]`كم مرة كلمة `j`يظهر في سياق كلمة `i`. متجهات القطار مثل هذه`v_i · v_j + b_i + b_j ≈ log(X[i][j])`الوزن الخسارة كثيراً لا تهيمن على الأزواج

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`، من بينهم`X[i][j]`نعم كلمة`j` 出现在词 `i`                                                                                                                                                                                                                                                              `v_i · v_j + b_i + b_j ≈ log(X[i][j])`                                                                                                                                                                                                                                                              

**FastText.**كلمة هي مجموع حرفها n-جرام زائد الكلمة نفسها. `where`يصبح`<wh, whe, her, ere, re>, <where>`. المتجه الكلام هو مجموع المتجهات المكونة. تدريب ك Word2Vec.`whereupon`) تتكون من ن-جرام معروفة.

> **FastText。**كلمة هي حرفها n-gram 之和加上词本身──`where`变成 `<wh, whe, her, ere, re>, <where>`△ 词向量是这些组件的向量和──像 Word2Vec 一样训练──好处:未见过的词(`whereupon`) من المعروف n-غرام 组合而成

**BPE (Byte-Pair Encoding).**ابدأ بمفردة من البايتات الفردية (أو الأحرف). احتسب كل زوج مجاور في الجسم. دمج الزوج الأكثر شيوعا في رمز جديد. كرر ل `k`التكرار. النتيجة: مجموعة من المفردات`k + 256`الوهم حيث تتواصل التسلسلات المتكررة (`ing`،`tion`،`the`(ج) هي رموز منفردة و الكلمات النادرة يتم تحديدها إلى قطع مألوفة. كل جملة تعتبر رموز إلى شيء ما.

> **BPE（字节对编码）。**من مجرد حرف (或字符) تعدد الكلمات البداية.`k`ثانياً`k + 256`个标志的词表,其中高频序列(`ing`.`tion`.`the`) هو رمز واحد، يتم تفكيك الكلمات النادرة إلى قطع مألوفة.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
n5-subword-merge
```

## بناءها

### GloVe: تصنيف ماتريكس المواجهة

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

اثنين من قطع التحرك التي تستحق الإسم`f(x) = (x/x_max)^alpha`الوزن المنخفضة أزواج متكررة جدا (مثل `(the, and)`) حتى لا يهيمنون على الخسارة.`W`(في المركز) و `W_tilde`الجداول. جمع كل منهما هو خدعة نشرت التي تميل إلى أن تتفوق باستخدام واحدة فقط.

> 两个 مهمة مهمة`f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`(التي لا تُحكم في خسارتها)`W`(وسط كلمة) و `W_tilde`(上下文词)表之和──对两者求和是一个 مهارة منشورة ، عادة ما يكون من الأفضل استخدام واحد منها فقط──

### FastText: إضافة مدروسة للكلمات الفرعية

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

يتم تمثيل كل كلمة بمجموعة من n-جرام (عادة 3 إلى 6 أحرف). يتمثل كلمة تضمين في مجموع تضميناتها n-جرام. للتدريب على تخطي الجرام، قم بتضمين هذا حيث استخدم Word2Vec متجه واحد.

> كل كلمة من n-gram 集合 (عادة 3 إلى 6 حروف) تعبر عن كلمة嵌入 هي n-gram 嵌入之和。 بالنسبة لتدريب skip-gram 插入 Word2Vec باستخدام موقع واحد للقطر。

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

بالنسبة لكلمة غير مرئية، لا تزال تحصل على متجه طالما بعض من ن-جرامها معروفة. `whereupon`الأسهم`<wh`،`her`،`ere`و`<where`مع`where`، لذا فإنّهما يصلان بالقرب من بعضهما البعض

> بالنسبة للكلمات غير المرئية، طالما أن جزءها من ن-جرام هو معروف، يمكنك لا يزال الحصول على محور.`whereupon`مع`where`共享 `<wh`.`her`.`ere`和 `<where`لذا، كلاهما يقع في مكان قريب

### BPE: تعلّم لغة الكلمات الفرعية

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

التكرار الأول يدمج الزوج المجاور الأكثر شيوعا. بعد التكرار الكافي،`low`،`est`،`tion`(ج) تصبح رموز واحدة والكلمات النادرة تتحطم بشكل واضح.

> أول مرة تمت المشاركة في المرحلة الأولى من العصر`low`.`est`.`tion`(تحول إلى رمز واحد، نادر الكلمات تصبح صافيًا تمزيقها).

يتعلم مؤشر GPT / BERT / T5 الحقيقي 30k-100k الاندماج. النتيجة: يتم توكيين أي نص إلى تسلسل طويل محدود من الهويات المعروفة ، لا OOV أبدا.

> GPT / BERT / T5 分词器学习 3،000 إلى 10،000 مرة 合并── نتيجة: أي نص يتم分词为已知 ID 的有界长度序列,永远不会有 OOV──

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

في الممارسة، نادراً ما تدرب أي من هذه بنفسك.

> في الممارسة، أنت تقريبا لا تدرب نفسك على هذه.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

للتعلامات الفرعية على النمط BPE في عصر المحول:

> 对于 Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

- نعم`Ġ`يرمز المرفق إلى حدود الكلمات (اتفاقية GPT-2). كل رمز حديث هو متغير BPE ، WordPiece (BERT) ، أو SentencePiece (T5 ، LLaMA).

> `Ġ`السابق 标记词边界(GPT-2 的约定) ・・・ كل عصري分词器都是 BPE 变体、WordPiece(BERT) أو SentencePiece(T5、LLaMA) ・・・

### متى لا تختار أي

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/skill-embeddings-picker.md`:

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

## تمارين التدريب

1. **Easy.**أركض`char_ngrams("playing")`و`char_ngrams("played")`.حسب التداخل جاكارد من مجموعتين n-جرام. يجب أن ترى قطع مشتركة كبيرة (`pla`،`lay`،`play`() ، ولهذا السبب يتم نقل FastText بشكل جيد بين المتغيرات المورفولوجية.
   **简单。**运行 `char_ngrams("playing")`和 `char_ngrams("played")`△ حساب اثنين من ن-جرام 集合的Jaccard 重叠度──你应该看到大量共享片段(`pla`.`lay`.`play`), هذا هو السبب في نقل الصيغة السريعة في التغيرات بين المنتقلات الجيدة.
2. **Medium.**التمديد`learn_bpe`لتتبع نمو المفردات. رسم الرموز لكل حرف كعمل من عدد الاندماج. يجب أن ترى ضغط سريع في البداية، كما يختص تقريبا 2-3 رموز لكل رموز.
   **中等。**扩展 `learn_bpe`以跟踪词表增长──绘制每个语料字符的符号 数作为合并次数的函数──你应该看到开始时快速压缩,在约2-3字符/符号 附近渐近──
3. **Hard.**قم بتدريب الـ 1K-BPE على أعمال شكسبير الكاملة، قارن رمزية الكلمات الشائعة مقابل الكلمات النادرة، قم بتقييم متوسط الـ Tokens لكل كلمة قبل وبعد ذلك، اكتب ما فاجأك.
   **困难。**في سبايبيا كاملة تمارس 1000 مرة المجموعة BPE── مقارنة الكلمات العادية مع الكلمات النادرة المخصصة نتائج الكلمات分词── قياس قبل بعد متوسط كل كلمة رمزة ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ 

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## شروط الرئيسية

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## المزيد من القراءة

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf)ورقة GloVe، سبعة صفحات، لا تزال أفضل مشتق من الخسارة.
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) FastText. / FastText 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) الورقة التي قدمت BPE إلى النمط النووي الحديث. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) كيف تختلف BPE، WordPiece، و SentencePiece في الواقع في الممارسة العملية. / BPE、WordPiece 和 SentencePiece 在实践中的区别──
