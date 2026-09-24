# Word Embeddings  Word2Vec من الصفر  Word2Vec من التحقق

> كلمة هي الشركة التي تبقيها، قم بتدريب شبكة سطحية على تلك الفكرة و الهندسة تسقط.
> تعتمد كلمة على الشركة التي تحافظ عليها.

> **【中文解读】**Word2Vec وضع كلمة تخطيط إلى 密向量空间، مماثلة كلمة في 量空间接近── هي أساس النمط النووي الحديث.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

يعرف (تف-إيدف)`dog`و`puppy`إنها كلمات مختلفة. لا يعرف أنها تعني نفس الشيء تقريبا.`dog`لا يمكن أن تجميع إلى مراجعة حول `puppy`يمكنك أن تكتب على هذا عن طريق إدراج المختلفات، ولكن هذا يفشل في المصطلحات النادرة، الجارغون المجال، وكل لغة لم تتوقعها.

> TF-IDF  知道 `dog`和 `puppy`إنها مختلفة عن الكلمات التي لا تعرفها تقريباً نفسها`dog`لا يمكن أن يتم توحيد التدريبات`puppy`يمكنك أن تعالج ذلك من خلال قائمة معاني الكلمات، ولكن هذا في لغات نادرة، والخطوط التي لم تتوقعها في كل لغة سوف تفشل.

تريد تمثيلاً حيث`dog`و`puppy`الأرض قريبة من بعضها البعض في الفضاء`king - man + woman`أرض قريبة`queen`حيث تم تدريب عارضة`dog`يُنقل بعض الإشارات إلى`puppy`مجاناً

> أنت تريد طريقة للتعبير،让 `dog`和 `puppy`في الفضاء القريب.`king - man + woman`-أقف في`queen`قربها`dog`نموذج التدريب المجان`puppy`传递 بعض الإشارات

Word2Vec أعطتنا هذا الفضاء. شبكة عصبية طبقتين، تم تشغيل تريليون رمز، نشرت في عام 2013. الهندسة المعمارية بسيطة بشكل محرج تقريبا. النتائج أعادت تشكيل NLP لمدة عقد.

> Word2Vec  أعطى لنا هذا الفضاء ∙ دو لاير نيورال شبكة، تمرينات تمر بـ مليون توكن، 2013 نشر ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙   ∙ ∙ ∙    ∙ ∙    ∙ ∙      ∙     ∙                                                                                                                                                                                            

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**Distributional hypothesis**(الأول، 1957): "تعرف كلمة من خلال الشركة التي تحافظ عليها". إذا ظهرت كلمتان في سياقين متشابهين، فمن المحتمل أن تعني أشياء متشابهة.

> **分布假设（Distributional Hypothesis）**(أول، 1957):"ستعرفها من خلال كلمة واحدة تحتفظ بها. "إذا ظهرت كلمتان متشابهة في النص الأدنى، فربما تعني أشياء متشابهة.

Word2Vec يأتي في طعمين، كلاهما يستغل هذه الفكرة.

> كلمة2Vec لديها نوعان من التغيرات، كلنا استخدمنا هذه الفكرة

- **Skip-gram.**مع كلمة مركزية، توقع الكلمات المحيطة.`cat -> (the, sat, on)`مع حجم النافذة 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, النافذة كبيرة لـ 2
- **CBOW (continuous bag of words).**بالنظر إلى الكلمات المحيطة، توقع المركز.`(the, sat, on) -> cat`. . .
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词――`(the, sat, on) -> cat`.

إنّ لغة "سكيپ-جرام" بطيئة في التدريب، ولكنها تتعامل مع الكلمات النادرة بشكل أفضل.

> تمارس المخططات بشكل أبطأ ولكن أفضل معالجتها بشكل أفضل. أصبح اختيارًا متضمنًا.

الشبكة لديها طبقة واحدة مخفية بدون عدم وجود خطية. المدخل هو متجه واحد حار على المفردات. الخروج هو softmax على المفردات. بعد التدريب، يمكنك إلقاء الطبقة الخروج. الوزن الطبقة الخفية هي التوابع.

> 网络有一个不带非线性激活函数的隐藏层――输入是单词表上的热向量――输出是单词表上的软max――训练后,你丢弃输出层――隐藏层的权重就是嵌入――

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

الخدعة: "البالغة المكثفة من 100 ألف كلمة" مكلفة للغاية.**negative sampling**تحويلها إلى مهمة تصنيف ثنائية. توقع "هل ظهرت هذه الكلمة السياقية بالقرب من هذه الكلمة المركزية ، نعم أو لا". قم بعمل عينة من الكلمات السلبية (غير المتواصلة) لكل زوج تدريب بدلاً من حساب softmax على كل المفردات.

> : لـ 100,000 كلمة做softmax 代价太高──Word2Vec استخدام**负采样（Negative Sampling）**تحويلها إلى قسم ثانوي من المهام. التنبؤ " هل هذا العبارة التالية تظهر في هذا المركز بالقرب من هذا المركز، هو أو لا"

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
word-vector-arithmetic
```

## بناءها

### الخطوة الأولى: أزواج التدريب من مجموعة

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

كل زوج (مركز، سياق) في نافذة هو مثال إيجابي للتدريب.

> كل كلمة مركز في النافذة، على النحو السفلي، على كل شيء نموذج تدريب حقيقي.

### الخطوة الثانية: إضافة الجداول

-ماثريتين`W`هو جدول إضافة الكلمة المركزية (الذي تحمله). `W'`هو جدول الكلمات السياقية (غالبا ما يتم التخلص منها، في بعض الأحيان يتم متوسطها مع `W`)

> -أثنان من المواصفات`W`هو مركز كلمة تمثيل表(أنت احتفظت تلك)`W'`هو على أسفل الكلمات表( عادة ما يتم التخلي عنها، أحيانا مع `W`取平均)

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

الحجم الكلامي 10k و dim 100 هو واقعي؛ للتدريس، 50 الكلامي x 16 dim يكفي لرؤية الهندسة.

>                                                                                                                                                                                                                                                               

### الخطوة الثالثة: هدف أخذ العينات السلبي

لكل زوج إيجابي`(center, context)`، عينة`k`تعليمي النموذج حتى النقطة المنتج`W[center] · W'[context]`هو مرتفع للإيجابيات و منخفض للإيجابيات

> لكل نموذج حقيقي`(center, context)`, من كلمة表中采样 `k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`高,负例的低──

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

الصيغة السحرية: الخسارة اللوجستية على الزوجة الإيجابية (تريد sigmoid بالقرب من 1) بالإضافة إلى الخسارة اللوجستية على الزوجات السلبية (تريد sigmoid بالقرب من 0). تدفق المعدلات إلى الجداولين. المشتق الكامل في الورق الأصلي؛ تمر عبرها مرة واحدة مع قلم ورق إذا كنت تريد أن يلتصق.

> 神奇的公式:正例对上逻辑损失(希望 sigmoid 接近 1)加上负例对上逻辑损失(希望 sigmoid 接近 0) ・・・梯度流向两个表──完整推导见原始论文; إذا كنت تريد جعلها تفهم عميقة، باستخدام ورق مدمرة مرة أخرى──

### الخطوة الرابعة: تدريب على جسم الألعاب

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

بعد فترات كافية على مجموعة كبيرة، الكلمات التي تشارك السياقات لها تركيبات مركزية مماثلة. على مجموعة لعبة، ترى التأثير ضعيفا. على مليارات الرموز، ترى ذلك بشكل كبير.

> بعد مرور دورات كافية على المواد الكبيرة، تمتلك الكلمات المشتركة على المواد التالية كلمات مركزية مشابهة.

### الخطوة 5: خدعة التشابه

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

على المتجهات المهنية المسبقة لـ 300d Google News:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`ليس لأن النموذج يعرف ما هو الملكية لأن المتجه`(king - man)`يحتجز شيئا مثل "ملكي" ، و إضافة ذلك إلى `woman`أراضي بالقرب من منطقة الملكيات

> `king - man + woman = queen`ليس لأن النموذج يعرف ما هو المكتب بل لأن النموذج يتحرك`(king - man)`لقد تم القبض على شيء يشبه "المنزل الملكي" ، وسوف يضيفه إلى`woman`على مقربة من منطقة النساء في غرفة الملكة

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

كتابة Word2Vec من الصفر هو التدريس.`gensim`. . .

> من صفر كتابة Word2Vec هو من أجل التدريس.`gensim`.

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

للعمل الحقيقي، لا تدربين Word2Vec بنفسك تقريباً. تنزيل متجهات متدربة مسبقاً.

> 工作中,你几乎从不自己训练 Word2Vec──你下载预训练向量──

- **GloVe** نهج ستانفورد للتعامل مع المصفوفات المشتركة. نقاط التفتيش 50d، 100d، 200d، 300d. تغطية عامة جيدة. الدروس 04 تغطي GloVe بشكل خاص.
  **GloVe**  斯坦福                                                                                                                                                                                                                                                            
- **fastText** Word2Vec التوسيع فيسبوك الذي يدمج حرف n-جرام. يتعامل مع الكلمات خارج المفردات عن طريق إعداد كلمات فرعية. الدروس 04.
  **fastText** Word2Vec  توسيع في فيسبوك، إدخال في حروف n-gram── من خلال مجموعة الكلمات المعاملة 词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d، 3M لغة الكلمات، نشرت 2013. لا يزال يتم تنزيلها يوميا.
  **Google News 预训练 Word2Vec** 300 维,3000000 كلمة表, 2013 سنة نشر.

### عندما Word2Vec لا يزال يفوز في 2026

- التدريب على الموجات الطبية في ساعة على جهاز كمبيوتر محمول، الحصول على المتجهات المتخصصة لا نموذج عام التقاط.
                                                                                                                                                                                                                                                                
- الهندسة المميزة في نمط التشابه`gender_vector = mean(man - woman pairs)`.استغرقها من كلمات أخرى للحصول على محور محايد بين الجنسين . ما زال يستخدم في أبحاث العدالة
  类比式特征工程──`gender_vector = mean(man - woman pairs)`                                                                                                                                                                                                                                                              
- التفسير. 100d صغير بما فيه الكفاية لتحديد عبر PCA أو t-SNE و في الواقع ترى تشكيل المجموعات.
  可解释性──100 维足够小, يمكن أن تتم من خلال PCA أو t-SNE 绘图并实际看到聚类形成──
- أي مكان يجب أن يبدأ الإستنتاج على الجهاز دون GPU.
  أي حاجة لتشغيل الموقع على جهاز بدون GPU.

### عندما يفشل Word2Vec

جدار البوليسميا`bank`لديه متجه واحد`river bank`و`financial bank`شاركها`table`(صفحة بيانات مقابل أثاث) يشاركها. مصنف أسفل نهر لا يمكن التمييز بين الحواس من المتجه.

> تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات تعبيرات`bank`فقط واحد`river bank`和 `financial bank`مشاركتها`table`(الكترونيات التجارية مقابل الأجهزة) مشاركةها.

حلّت التوابع السياقية (ELMo، BERT، كل محول منذ) هذا الأمر عن طريق إنتاج متجه مختلف لكل ظهور لل كلمة بناءً على السياق المحيط. وهذا هو القفز من Word2Vec إلى BERT: من ثابت إلى سياقي. المرحلة 7 تغطي نصف المحول.

> 上下文嵌入(ELMo、BERT و بعد ذلك جميع Transformer) من خلال الحدوث من مختلف قطاعات للظهور لكل كلمة على مدار الجوار على أسفل حل هذه المشكلة.

مشكلة خارج المفردات هي الفشل الآخر.`Zoomer-approved`إذا لم يكن في بيانات التدريب. لا يوجد عكس. fastText يصلح هذا مع تركيب الكلمات الفرعية (المدرس 04).

> 词表外(خارج الكلمات) المشكلة هي أخرى فشل.`Zoomer-approved`في بيانات التدريب، لم يسبق له أن رأيتها أبدا.

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/skill-embedding-probe.md`:

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

## تمارين التدريب

1. **Easy.**إدارة حلقة التدريب على مجموعة صغيرة (20 جملة عن القطط والكلاب) بعد 200 دورة، التحقق`nearest(vocab, W, W[vocab["cat"]])`العائدات`dog`في أعلى 3، وإلا، قم بتعزيز الفترات أو المفردات.
   **简单。**في حلقة تدريبية على لغة صغيرة ((20 جملة عن القط والكلاب)`nearest(vocab, W, W[vocab["cat"]])`أعلى ثلاثة من العودة`dog`إذا لم يكن هناك، زيادة الجولة أو الكلمات
2. **Medium.**إضافة عينة فرعية من الكلمات المتكررة. الكلمات ذات التردد أعلاه `10^-5`يتم إلقاءها من أزواج التدريب مع احتمال متناسب مع ترددها.
   **中等。**添加高频词子采样──频率高于 `10^-5`احتمالية تصبح كلمة على النحو المناسب من التدريب على النحو المرموق.
3. **Hard.**قم بتدريب نموذج على مجموعة الأخبار العشرين. احسب محورين للتحيز:`he - she`و`doctor - nurse`. مشروع كلمات المهنة على كلا المحاور. تقرير المهن التي لديها أكبر فجوة التحيز. هذا هو نوع من السؤال العدالة الباحثين يستخدمون.
   **困难。**في 20 مجموعة أخبار 语料上训练模型──计算两个偏见轴:`he - she`和 `doctor - nurse`将职业词投投投向两个轴上 报告哪些职业有最大偏见差距                                                                                                                                                                                                                                                  

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## شروط الرئيسية

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## المزيد من القراءة

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) ورقة العينات السلبية. قصيرة وقابلة للقراءة. / 负采样论文。短小易读。
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) أوضح مشتق من التدرج، إذا كانت الرياضيات في الورقة الأصلية تشعر كثافة. / 最清晰的梯度推导, إذا كنت تشعر أن الرياضيات
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) إعدادات تدريب الإنتاج التي تعمل فعلا. / 真正有效的生产训练设置──
