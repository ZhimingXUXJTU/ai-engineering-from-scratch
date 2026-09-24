# تحليل المشاعر

> مهمة النمط النووي القنوني. معظم ما تحتاج إلى معرفته عن تصنيف النص الكلاسيكي يظهر هنا.
> أحدث مهمة في مجال النفط النووي الكلاسيكي، كل ما تحتاج إلى معرفته هنا

> **【中文解读】**判断文本的情感倾向──是NLP最经典的分类任务之一──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

"الطعام لم يكن جيداً" إيجابي أم سلبي؟

> "الطعام لم يكن رائعاً" أم "أو" ؟

يبدو الشعور بسيطًا. قال أحد المراجعين إنهم أحبوا أو لم يحبوا شيئًا ما. وضع علامة على الجملة. السبب في أن الأمر أصبح مهمة NLP القنوني هو أن كل حالة سهلة المظهر تخفي واحدة صعبة. ينقل الرفض المعنى. يعكس الساركازم ذلك. "ليس سيئاً على الإطلاق" إيجابيًا على الرغم من كلمتين ذات رمز سلبي. تحمل الإموجيز إشارة أكثر من النص المحيط.`tight`في مراجعة الموسيقى مقابل `tight`في مراجعة الأزياء).

> يبدو التحليل العاطفي بسيطا. يقول المعلقين إنه يحب أو لا يحب أي شيء. يصبح هذا مهمة NLP كلاسيكية، لأن كل حالة تبدو بسيطة خلفها كل حالة مخبأة في حالة صعبة.`tight`مع عصريات`tight`(‬)

إن المشاعر هي مختبر عمل لـ NLP الكلاسيكي. إذا فهمت لماذا كل خط أساسي ساذج لديه وضع فشل محدد، فهمت لماذا تم اختراع كل نموذج أغنى. هذا الدروس يبني خط أساسي بايز ساذج من الصفر، ويضيف رجعة لوجستية، ويعطى الأسماء للطغيان التي تجعل مشاعر الإنتاج مشكلة درجة الامتثال.

> تحليل العاطفة هو المختبر المنتج في النمط النووي الكلاسيكي. إذا كنت تفهم لماذا كل خط بسيط له نمط فاشل محدد، فأنت تفهم لماذا كل نمط أكثر غنى تم اختراعها.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

الشعور الكلاسيكي هو وصفة خطوتين

> تحليل العاطفة الكلاسيكية هو خطوة خطوتين

1. **Represent.**حول النص إلى متجه ميزة.
   **表示。**将文本转换为特征向量──BoW、TF-IDF 或 n-gram──
2. **Classify.**تطبيق نموذج خطي (Naive Bayes، رجعة اللوجستية، SVM) على الأمثلة الملصقة.
   **分类。**في العلامة نموذج على مقارنة النموذج الخطية ((朴素贝叶斯、逻辑归归、SVM) 

البشعري (بايز) هو أغبى نموذج يعمل افترض كل ميزة مستقلة بالنظر إلى العلامة التجارية`P(word | positive)`و`P(word | negative)`في الاستنتاج، ضرب الاحتمالات. افتراض الاستقلال "الساذج" خاطئ بشكل مضحك ومع ذلك النتائج قوية بشكل مذهل. السبب: مع ميزات النص النادرة والبيانات المتوسطة، يهتم المصنف حول أي جانب كل كلمة تميل نحو أكثر من كم.

> الباييس بسيط هو النموذج الأكثر استخداماً ولكن المستخدمة. افتراض أن كل خصائص تعود إلى علامات معينة.`P(word | positive)`和 `P(word | negative)` التفكير في الوقت الذي سوف يضاعف احتمالات التفريق. افتراض استقلالية "بسيطة" خاطئ ومضحك، ولكن النتيجة مذهلة.

التراجع اللوجستي يصلح افتراض الاستقلال. يتعلم وزن لكل ميزة، بما في ذلك الوزن السلبي. `not good`وذلك لا يمكن لـ (بايز) البديل أن يفعل ذلك لـ (بايز) لم يسمّه أبداً

> العودة المنطقية تعيد افتراض استقلالية.`not good`                                                                                                                                                                                                                                                              

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
sentiment-logits
```

## بناءها

### الخطوة الأولى: مجموعة بيانات صغيرة حقيقية

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

صغيرة على وجه الخصوص. العمل الحقيقي يستخدم عشرات الآلاف من الأمثلة (IMDb، SST-2، قطبية Yelp). الرياضيات هي نفسها.

> فاعمل في الواقع على عدد قليل من النماذج.

### الخطوة الثانية: البديلة المتعددة من الصفر

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

التسهيل الإضافي (الألفا = 1.0) هو تسهيل لابلاس. بدونها، كلمة غير مرئية في فئة لديها احتمال صفر والسجل ينفجر. `alpha=0.01`هو شائع في الممارسة العملية. `alpha=1.0`هو الاختلالات التعليمية.

> 加法平滑(alpha=1.0) هو لا يزال لا يزال هناك، في فئة لا يزال هناك احتمالات للكلمات التي لم تظهر.`alpha=0.01`很常见──`alpha=1.0`تعليميّةٌ مُعتمدةٌ

### الخطوة الثالثة: تراجع اللوجستية من الصفر

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

يُعتبر التنظيم L2 مهمًا هنا. ميزات النص نادرة؛ بدون L2 يتذكر النموذج أمثلة التدريب. ابدأ من `0.01`و التنسيق

> L2 التنظيم هنا مهم جدا.`0.01`開始调参──

### الخطوة الرابعة: إبطال التعامل (وضع الفشل)

فكر في "غير جيد" و "ليس سيئا"`{not, good}`و`{not, bad}`ويتعلم من أي شخص ظهر أكثر في التدريب.`not_good`و`not_bad`ويتعلمها بصفة مميزة، وهذا عادة ما يكون كافياً.

> فكّر "ليس جيداً" و "ليس سيئاً"`{not, good}`和 `{not, bad}`, حسب أي من التدريبات التي تظهر المزيد لتعلم.`not_good`和 `not_bad`كالمختلفة من الخصائص التعلم.

إصلاحات أكثر صرامة تعمل عندما لا يكون لديك الكبيرة:**negation scoping**. إضافة رموز التوقيت بعد كلمة سلبية مع `NOT_`حتى النقاط التالية.

> إصلاح أكثر قاسية ولكن فعالة في غياب الجمع الثاني:**否定范围标记**في كلمة "الرفض"`NOT_`قبل، حتى التالي علامة علامة

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

الآن`good`و`NOT_good`المصفوف يمكن أن يوزنها على العكس. ثلاث خطوط من المعالجة المسبقة، دقة القياس قفزة على مقاييس الشعور.

> الآن`good`和 `NOT_good`تميزات مختلفة. يمكن أن يمنح الجهاز الوزن المقابل لهما.

### الخطوة 5: قياسات التقييم التي تهم

الدقة وحدها مضللة إذا كانت الفئات غير متوازنة. عادة ما تكون أعضاء المشاعر الحقيقية إيجابية بنسبة 70-80% أو سلبية بنسبة 70-80٪. يصبح تصنيف الأغلبية المستمرة دقة بنسبة 80% و غير قيمة.

> إذا كانت الفئة غير متوازنة، فإن معدلات التأكد فقط ستحدث خطأ. عادة ما تكون 70-80% من المواد العاطفية الحقيقية إيجابية أو 70-80% من السلبية. يمكن لأغلبية الفئات العادية الحصول على 80% من معدلات التأكد، ولكن لا قيمة لها.

- **Per-class precision and recall.**زوج واحد لكل فئة، ووسعهم الكلي للحصول على رقم واحد يحترم توازن الفئة.
  **每类精确率和召回率。**كل فئة واحدة على حد سواء.
- **Macro-F1 (primary metric for imbalanced data).**متوسط درجات الفئة الفئة، مع الوزن المتساوى. استخدم هذا بدلاً من الدقة عندما تكون الفصول غير متوازنة.
  **Macro-F1（不平衡数据的主要指标）。**متوسط قيمة الفئات الفئة F1 ، والوزن نفسه.
- **Weighted-F1 (alternative).**نفس ماكرو ولكن معدل من خلال تردد الفئة. تقرير إلى جانب ماكرو-F1 عندما يكون عدم التوازن نفسه له معنى عمل.
  **Weighted-F1（替代方案）。**مع المتوسط الكبير نفسه ولكن حسب الفئة المتكرر زيادة الوزن.
- **Confusion matrix.**العد الخام. دائما تحقق قبل الثقة أي مقياسية المتعددة؛ فإنه يكشف عن أي زوج من الفئات النموذج يخلط.
  **混淆矩阵。**الاختبار الأول في أي مؤشر كميات في الاعتقاد؛ فإنه يكشف عن ما هو النموذج المختلط مع أي فئات من المواد.
- **Per-class error samples.**سحب 5 توقعات خاطئة لكل فئة وقرأها لا شيء يحل محل القراءة الأخطاء الفعلية
  **每类错误样本。**كل فئة تستخرج 5 أخطاء توقعات.

بالنسبة للبيانات التي لا توازن لها بشكل كبير (نسبة 95-5) ، تقرير **AUROC**و**AUPRC**بدلاً من الدقة، فإن AUPRC أكثر حساسية تجاه الطبقة الأقلية، وهو ما يهمك عادة (البريد الإلكتروني والاحتيال والشعور النادر).

> 对于严重不平衡的数据 ((> 95-5 比例) ، تقرير **AUROC**和 **AUPRC**代替准确率──AUPRC أكثر حساسية للقسم الأقليمي، وهذا عادة ما يكون من شأنك

**Common bug to avoid.**الإبلاغ عن الفئة الصغيرة F1 بدلاً من الفئة الكبرى F1 على البيانات غير المتوازنة يعطي رقم يبدو عالياً لأنه يهيمن عليه فئة الأغلبية.

> **常见错误。**في بيانات غير متوازنة تقرير الف1 الصغيرة بدلا من الف1 الكبرى سوف تعطى رقم يبدو عاليا جدا، لأنه يسيطر على غالبية الفئات.

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

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

سيكيت-ليرن يفعل ذلك في ستة سطر، صحيح.

> تعلم القليل من الاختلافات

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

ثلاثة أشياء يجب ملاحظتها`stop_words=None`يحتفظ بالنساء`ngram_range=(1, 2)`يضيف الكلمات الكبيرة لذلك`not_good`يصبح ميزة`sublinear_tf=True`هذه العلامات الثلاثة هي الفرق بين خط أساسي دقيق بنسبة 75% و 85٪ دقيق في SST-2.

> ثلاثة أجزاء تستحق الاهتمام`stop_words=None`保留否定词──`ngram_range=(1, 2)`添加二元组使 `not_good`لتصبح مميزة`sublinear_tf=True`抑制重复词── هذه العلامات الثلاثة هي الفرق بين SST-2 على 75% 准确率基线 و 85% 准确率基线──

### متى يجب الوصول إلى محول

- اكتشاف السخرية النماذج الكلاسيكية تفشل هنا
  刺检测── 经典模型在这里会失败── 无例外──
- مراجعات طويلة حيث يغير المشاعر في منتصف الوثيقة
  情感在文档中转变的长评论──
- "الكاميرة كانت رائعة لكن البطارية كانت رهيبة" عليك أن تعطي المشاعر إلى الجوانب.
  على أساس تحليل العاطفة الجانبية. "كان الكاميرا رائعة ولكن البطارية كانت رهيبة".
- لغات غير الإنجليزية ذات موارد قليلة. BERT متعددة اللغات تعطيك خط أساسية صفر إطلاق مجانا.
  غير انجليزية 低资源语言多语言BERT 为你提供零样本基线

إذا كنت بحاجة إلى أي من المذكور أعلاه، فانتقل إلى المرحلة 7 (غوص العميقة للمتحولات). وإلا، فإن البغاء البايز أو التراجع اللوجستي على TF-IDF بالإضافة إلى البيغرامات بالإضافة إلى التعامل مع السلب هو خط أساسي لإنتاجك لعام 2026.

> إذا كنت بحاجة إلى أي شيء، قفز إلى المرحلة 7 ((المحول عميق)  وإلا، في TF-IDF 加二元组加否定处理

### فخ التكرار (مرة أخرى)

إعادة تدريب نماذج المشاعر هو روتين. إعادة تقييمها ليس كذلك. استخدام أرقام الدقة التي تم الإبلاغ عنها في الورق تقسيمات محددة، وتعالج مسبقا محددة، وتعلامات محددة. إذا قارنت نموذجك الجديد إلى خط أساسي دون استخدام خط الأنابيب المتطابق، فسوف تحصل على دلتا مضللة. دائما إعادة تشكيل خط الأساس على خط الأنابيب الخاص بك، وليس رقم الورق.

> 重新训练情感模型是常规操作――重新评估却不是―― 论文报告的准确率数字使用特定数据分分,特定预处理,特定分词器―― 如果你 لا تستخدم نفس التيار تماماً لتقارن النموذج الجديد مع التيار الأساسي، فسوف تحصل على اختلاف التوجهات الوهمية―― دائماً على التيار الأساسي الذي تم إنشاؤه على التيار الأساسي الخاص بك، وليس باستخدام الأرقام في المقالة――

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/prompt-sentiment-baseline.md`:

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

## تمارين التدريب

1. **Easy.**إضافة`apply_negation`كخطوة من قبل المعالجة في خط التعلم المتحكم في التعلم و قياس دلتا F1 على مجموعة بيانات الحساسية الصغيرة.
   **简单。**ستعمل`apply_negation`كخطوة إضافية للتدريب على التعلم القليل في مجال التدريب على العواطف، في مجموعة بيانات عاطفية صغيرة
2. **Medium.**تنفيذ تراجع اللوجستية الموزن حسب الفئة (موافقة `class_weight="balanced"`لتحقيق التوازن المختلف في فئة 90-10
   **中等。**实现类别加权逻辑回归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅ في المجموعة 90-10 类别不平衡上测量效果
3. **Hard.**قم ببناء كاشف السخرية عن طريق تدريب مصنف ثان على بقايا نموذج المشاعر. وثيقة إعدادك التجريبي. حذر القارئ عندما تكون دقةك أقل من فرصة (مستوى الاحتمال على السخرية من فئة 2 هو ~ 50% ، ومعظم المحاولات الأولى تهبط هناك).
   **困难。**في دراسة النموذج العاطفي على الفجوة تدرب جهاز فصيل ثاني لبناء جهاز اختبار الحالة. اكتب تحديدات تجربتك.

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## شروط الرئيسية

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## المزيد من القراءة

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) الاستطلاع الأساسي. طويل، ولكن الأقسام الأربعة الأولى تغطي كل شيء كلاسيكي.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) الورقة التي أظهرت البيغرام + البراهية بايز من الصعب أن تفوز على النص القصير. / 证明二元组 + 朴素贝叶斯在短文本上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) إشارة إلى `CountVectorizer`،`TfidfVectorizer`وكل زر ستقوم بتحسينه`CountVectorizer`.`TfidfVectorizer`及你将调参的每个参数的参考──
