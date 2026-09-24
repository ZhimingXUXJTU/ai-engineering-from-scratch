# حقيبة الكلمات، TF-IDF، و تمثيل النص

> أقرأ أولاً، فكر في ذلك لاحقاً، فـ"تـف-إيدف" لا تزال تفوق على التكليد في المهام المحددة جيداً في عام 2026.
> في مهمة محددة، فإن الاتحاد الدولي للطاقة الذرية (TF-IDF) حتى عام 2026 سيظل ينجح في التثبيت.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词──这是最基础的文本表示方法──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## أهداف التعلم

- بناء حقيبة الكلمات و تمثيلات TF-IDF من الصفر
  من零构建词袋模型和 TF-IDF 表示
- فهم المتجهات النادرة، وتردد المصطلحات، وتردد المستندات العكسية
  فهم نادرة التردد ∙ كلمة频和逆文档频率
- استخدام CountVectorizer و TfidfVectorizer من scikit-learn في الإنتاج
  في الإنتاج استخدام سكيت-تعلم من CountVectorizer و TfidfVectorizer
- معرفة متى يفوز TF-IDF على التوابل وعندما يفشل
  تعرفون (تف-إيدف) ، كيف نجحت في ذلك، كيف فشلت؟

## المشكلة المشكلة المشكلة

النموذج يحتاج الأرقام لديك سلسلة

> 模型需要数字──你手上的是字符串──

كل خط أنابيب NLP يجب أن يجيب على نفس السؤال. كيف نغير تدفق الطول المتغير من الرموز إلى متجه حجم ثابت يمكن أن يستهلك المصنف. وكانت أول إجابة الحقل هبطت على الأكثر غباء التي تعمل. عد الكلمات. صنع متجه.

> يجب على كل خط من خطوط النفط الوطنية الإلكترونية الإجابة على نفس السؤال: كيف سيتم تحويل التوجينات إلى حجم ثابت من الحجم الكبير، حتى يتمكن المجموعات من استهلاكها.

هذا المتجه قد حمل أكثر من النموذج النووي الإنتاجية من أي نموذج إضافة. مرشحات البريد الإلكتروني، تصنيفات الموضوعات، اكتشاف شذوذ السجلات، تصنيف البحث (قبل BM25) ، الموجة الأولى من تحليل المشاعر، العقد الأول من المعايير الأكاديمية لـ NLP. 2026 الممارسين لا يزالون يصلون إليه أولاً في مهام التصنيف الضيقة. إنه سريع ويمكن تفسيره، وغالبًا ما لا يمكن التمييز بينه وبين نموذج تضمين معايير 400 م على المهام التي يكون فيها وجود الكلمات هو ما يهم.

> هذا الطراز يحمل إنتاج NLP  تطبيق أكثر من أي نموذج مدمج هو: 垃圾邮件 器 器 日志 异常检查 搜索排序 BM25 出现之前) 首波情感分析 学术 NLP 基准测试第一十年 2026 الممارسين في المهمات المحدودة                                                                                                                                                                                                                    

هذه الدروس تبني كيس الكلمات، ثم TF-IDF، من الصفر. ثم تظهر scikit-تعلم القيام بنفس الشيء في ثلاث خطوط. ثم أسماء وضع الفشل الذي يجعلك تصل إلى التوابل.

> هذا الدروس من الصفر بناء كلمات كيس النموذج، ثم بناء TF-IDF، ثم عرض كيفية التعلم باستخدام ثلاثة صفوف من الكود القيام بنفس الشيء، وأخيرا أن يلاحظ جعلك لا بد أن تختار في وضع النقص النموذج.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**Bag of Words (BoW)**يرمي النظام. لكل وثيقة، عد عدد مرات ظهور كل كلمة في المفردات. طول المتجه هو حجم المفردات. الموقف `i`هو عدد الكلمات`i`. . .

> **词袋模型（Bag of Words, BoW）**抛弃顺序──对每文档,统计每词表词出现次数──向量长度是词表大小──位置 `i`نعم كلمة`i`عدد

**TF-IDF**كلمة تظهر في كل وثيقة غير معلومية، لذلك قم بتخفيض حجمها. كلمة نادرة في جميع أنحاء الجسم ولكن متكررة في وثيقة واحدة هي إشارة، لذلك قم بتخفيض حجمها.

> **TF-IDF**على كل المستندات لا يوجد كلمات في كل المستندات كمية من المعلومات، لذلك تقلل من وزنها.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

أين`TF`هو تردد المصطلح في الوثيقة، `df`هو تردد الوثيقة (كم عدد الوثائق التي تحتوي على الكلمة) ،`N`هي الوثائق الكاملة.`log`يحتفظ بالوزن المحدد للكلمات المتاحة في كل مكان.

> من بينهم`TF`هو في الملفات`df`هو الملفات المتكررة (((`N`هو الملفات المجموعية`log`أن يحتفظ الوزن على الكلمات المتاحة

الخصائص الرئيسية: كل منهما ينتج متجهات نادرة مع محور يمكن تفسيرها. يمكنك النظر إلى أوزان المصنف المدرب وقراءة الكلمات التي تدفع الوثيقة نحو كل فئة. لا يمكنك القيام بذلك مع إدراج BERT 768 بعد.

> الخصائص الرئيسية: كل منهما ينتج حجم نادر من المحور الذي يمكن تفسيره. يمكنك أن ترى وزن المجموعة المهنية المهنية، وقراءة ما هي الكلمات التي ستقوم المستندات بتقديمها إلى كل فئة. لا يمكنك استخدام 768 维 BERT 嵌入 للقيام بذلك.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
bow-tfidf
```

## بناءها

### الخطوة الأولى: بناء المفردات

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

المدخل: قائمة بالوثائق المضمونة (أي مؤشر على مستوى الكلمة سوف يفعل ذلك ؛ `code/main.py`في هذا الدروس يستخدم متغير بسيط من الحروف الصغيرة).`{word: index}`إضافة ثابتة يعني كلمة مؤشر 0 هو أول كلمة ترى في الوثيقة الأولى. الاتفاقية تختلف؛ scikit-تعلم أنواع الأبجدية.

> 输入:token 化的文档列表(أي كلمة درجة分词器都可以;本课的 `code/main.py`استخدام التبسيط 忽略大小写变体) ⋅输出:`{word: index}`字典──稳定的插入顺序 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符索引 0 字符

### الخطوة الثانية: حقيبة الكلمات

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

الصفوف هي وثائق، العمودات هي مؤشرات المفردات.`[i][j]`هو "كم مرة كلمة `j`يظهر في الوثيقة`i`الدكتور 1 لديه`cat`مرتين لأنه فعل ذلك`ran`صفر مرات لأنه لم يفعل.

> 行是文档──列是词表索引──条目 `[i][j]`هو " كلمة `j`في الملفات`i`لقد ظهر في الملفات مرة واحدة`cat`لأنه ظهر مرتين`ran`لأنه لم يظهر

### الخطوة الثالثة: تردد المصطلحات وتردد الوثائق

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

خدعتين لتسهيل تستحق الإسم`(n+1)/(d+1)`تجنب`log(x/0)`- التابعة`+1`يضمن كلمة في كل وثيقة لا يزال IDF 1 (ليس 0) ، مما يطابق افتراض scikit-learn.`log(N/df)`كلاهما يعمل، النسخة المُسطحة أكثر صداقتاً

> .هناك طريقتان من المفاهيم`(n+1)/(d+1)`避免 `log(x/0)`۞ 尾部`+1` ضمان ظهور كلمة في كل وثيقة  IDF  لا يزال 1  بدلا من 0) ، وفقًا للقيمة الراسخة للتعلم.`log(N/df)`两种都有效;平滑版本更友好

### الخطوة الرابعة: TF-IDF

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

وثائق ثلاث، خمس كلمات في الكلمات (`the`،`cat`،`sat`،`dog`،`ran`)`the`يظهر في كل ثلاثة، لذلك جيش الدفاع الدولي منخفض.`dog`يظهر في واحد، لذلك الجيش الإسرائيلي مرتفع. المتجهات نادرة (معظم الإدخالات صغيرة) والكلمات التمييزية تظهر.

> ثلاث وثائق، خمسة كلمات`the`.`cat`.`sat`.`dog`.`ran`(‬)`the`في جميع المستندات الثلاثة ظهر، لذلك الجيش الإسرائيلي 很低`dog`فقط في الملفات الواحدة، لذلك الجيش الإسرائيلي 很高── حجمها نادر جدا.

### الخطوة 5: تعاديل الصفوف L2

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

بدون التطبيع، يحصل مستند أطول على متجه أكبر ويهيمن على درجات التشابه. يضع التطبيع L2 كل مستند على وحدات المضاربة. تشابه الكوزين بين الصفوف هو الآن مجرد نسبة نقطة.

>  بدون التوحيد، سيتم الحصول على مقياس أكبر ومحيط أكبر ومحيط أكبر من النقاط. L2  التوحيد يضع كل مستند على سطح الكرة فوق.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

سيكيت-تعلم السفينة الإصدار الإنتاجي.

> سيكيت-تعلم قدم نسخة درجة الإنتاج

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

`CountVectorizer`يستخدم الـ Tokenization و المفردات و BoW في مكالمة واحدة`TfidfVectorizer`يضيف وزن الجيش الإسرائيلي وتطبيع L2. كل منهما يعيد المصفوفات الضعيفة. بالنسبة إلى 100k وثائق، النسخة الكثيفة لا تناسب في الذاكرة؛ البقاء ضئيلة حتى يطلب المصنف الكثافة.

> `CountVectorizer`في المستخدمة الأولى، تمت إنجاز كلمة`TfidfVectorizer`增加 IDF 加权和 L2 归结化──都回归稀疏矩阵──对10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏──

القفز الذي يغير كل شيء:

> تغيير كل شيء

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### عندما لا يزال TF-IDF يفوز (من عام 2026)

- اكتشاف البريد الإلكتروني، وضع علامات على الموضوع، وضع علامات على شذوذ السجلات، وجود الكلمات هو ما يهم، لكن النونات الارضية لا.
  垃圾邮件检测、主题标签、日志异常标签──存在或不的词是关键;语义细微差异不重要──
- أنظمة بيانات منخفضة (مئات من الأمثلة المسموحة).
  低数据场景 ((مئات من العلامات النموذجية) ――TF-IDF 加逻辑回归没有预训成本──
- في أي مكان يهم التأخير، TF-IDF بالإضافة إلى نموذج خطي يستجيب في ثوانٍ صغيرة، إدخال وثيقة عبر محول يستغرق 10-100 ثانية.
  أي مشاهد حساسة للتأخير ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
- أنظمة يجب أن تفسر توقعاتها، فحص معايير المصنف، الكلمات الإيجابية العليا هي السبب.
  需要解释预测结果的系统──检查分类器的系数──排名最高正权重词就是原因──

### عندما تفشل نظام التأمين التجاري

الفشل في العمى التفسيري، فكر في هذه الوثائق:

> 语义盲点──考虑以下两个文档:

- "الفيلم لم يكن جيدا على الإطلاق".
- "كان الفيلم ممتازاً"

أحدهما هو مراجعة سلبية، والآخر إيجابية، التداخل بين الفئة التلفزيونية والفئة الدولية هو بالضبط`{the, movie, was}`. محترف تصنيف الكلمات يجب أن يتذكر هذه الكلمة`not`قريبة`good`يمكن أن تتعلم هذا على ما يكفي من البيانات، ولكن أبداً بجد مثل نموذج يفهم النص.

> واحد هو تقييم سلبي، والآخر هو تقييم مؤكد.`{the, movie, was}`يجب أن تتذكر`good` قريب `not`سوف تغير العلامة. يمكن أن تتعلم ذلك في بيانات كافية، ولكن لن تكون أبدا مثل نموذج فهم القانون اللغوي.

الفشل الآخر: كلمات خارج المفردات عند الاستنتاج. نموذج BoW المدرب على مراجعات IMDb لا يعرف ما الذي يجب فعله `Zoomer-approved`إذا لم تظهر هذه الرمزية في التدريب. تضمنت الكلمات الفرعية (المرحلة 04) تتعامل مع هذا. لا يمكن أن تقوم TF-IDF.

> 另一个失败:推理时的词表外(خارج المفردات، OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`إذا كان هذا الوهم لم يظهر في التدريب.

### الهجين: التوابل الموزعة TF-IDF

الاختيار العملي لعام 2026 لتصنيف البيانات المتوسطة: استخدام ثقيلات TF-IDF كاهتمام على تضمين الكلمات.

> 2026 سنة وسطى دراسة المعلومات: استخدام TF-IDF 权重作为词嵌入的注意力──

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

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

تحصل على القدرة التفاصلية من التوابع، وتأكيد الكلمات النادرة من TF-IDF. يقوم المصنف بتدريب على المتجه المجمع. هذا يتفوق بمفرده على الإحساس، الموضوع، والنية التصنيف تحت حوالي 50 ألف مثال معلّمة.

> تمكنك من الحصول على القدرة على التعبير من التثبيت ، من TF-IDF  الحصول على الكلمات النادرة التركيز.

## أرسلها .

إبقوا`outputs/prompt-vectorization-picker.md`:

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

## تمارين التدريب

1. **Easy.**تنفيذ`cosine_similarity(doc_vec_a, doc_vec_b)`على إصدار L2 المعتاد TF-IDF. التحقق من أن الوثائق المتطابقة تسجل 1.0 و الوثائق المفصلة المفصلة تعادل 0.0.
   **简单。**في L2  التوحيد TF-IDF  الناتج على تحقيق `cosine_similarity(doc_vec_a, doc_vec_b)` تجربة نفس المستندات النتيجة 1.0, كلمة表 تماما غير متناغمة
2. **Medium.**إضافة`n-gram`دعم `bag_of_words`. المعلم`n`يُنتجُ العدّاتِ أكثر `n`-جرام، اختبر ذلك`n=2`على`["the", "cat", "sat"]`يُنتجُ عدد الكبيرة`["the cat", "cat sat"]`. . .
   **中等。**لأجل`bag_of_words`إضافة`n-gram`支持──参数 `n` تكوين `n`-غرامات 计数──测试 `n=2`时 `["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`عدد
3. **Hard.**قم ببناء الهجين المضمن الموزن TF-IDF أعلاه باستخدام متجهات GloVe 100d (تنزيل مرة واحدة ، التخزين). مقارنة دقة التصنيف مع TF-IDF البسيطة والإضافة المتوسطة المجمعة البسيطة على مجموعة بيانات 20 Newsgroups. تقرير الذي يفوز أين.
   **困难。**استخدام GloVe 100 维向量(download一次并缓存) بناء المذكورة أعلاه TF-IDF 加权嵌入混合方案── في 20 مجموعة إعلامية على مقارنة التسوية، مقارنة مع نقية TF-IDF 和 نقية متوسط القيمة المجموعة嵌入── تقرير الذي في أي مكان يفوز

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## شروط الرئيسية

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## المزيد من القراءة

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) الإشارة القنونية لل API، بالإضافة إلى ملاحظات على كل زر. / 权威 API 参考،以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) الورقة التي جعلت TF-IDF الاختيار المخصص لعقد. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2)2026 - عندما تفوز الطريقة القديمة ولماذا. / 2026 - سنة على الطريقة القديمة
