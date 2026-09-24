# النص المختصر 文本摘要

> الأنظمة الاستخراجية تخبرك بما قاله الوثيقة الأنظمة المجردة تخبرك بما كان المؤلف يقصده مهام مختلفة، مشاكل مختلفة
> النظام المنتج يخبرك بما قاله المستند. النظام المنتج يخبرك بما قاله المؤلف.

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## المشكلة المشكلة المشكلة

مقالة أخبار تضم 2000 كلمة تصل إلى تغذيتك. تحتاج إلى 120 كلمة التي تمسك بها. يمكنك إما اختيار الجمل الثلاث الأكثر أهمية من المقال (المستخلص) أو إعادة كتابة المحتوى بكلماتك (المجرد). كل منهما يسمى التجميع. إنها مشاكل مختلفة تماما.
> واحد 2000 كلمة من مقالات صحفية تظهر في مجرى المعلومات الخاصة بك. تحتاج إلى 120 كلمة لزيادة ذلك. يمكنك اختيار من بين مقالاتك ثلاثة أقصى جملة ((التقاط) ، أو إعادة كتابة المحتوى ((توليد) بمناسبة نفسك.

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.


الاختصار الاستخرجي هو مشكلة التصنيف`k`. إن الناتج هو دائماً صفرية لأنه يتم رفعها حرفياً. الخطر هو فقدان المحتوى الذي يتم توزيعه على جميع أنحاء المقال.
> 抽取式摘要是一个排序问题──给每个句子打分,返回排名 `k`المقالة المترتبة على النص المختلفة، والتي تعتبر من المفروض أن تكون المقالة المترتبة على النص المختلفة.

الموجات المختصرة هي مشكلة في التوليد. ينتج المحول نصًا جديدًا مشروطًا على المدخل. إن المخرجات متدفقة ومضغوطة ولكن قد تلهسون حقائق لم تكن في المصدر. الخطر هو التصميم الثقي.
> النتائج الناتجة هي مشكلة إنتاج. التحويلات تُنتج على أساس الإدخال وتنتج مقالات جديدة.

هذا الدرس يبني على كليهما، مع وضع الفشل لكل واحد يمتلك.
> هذا النوع من النماذج المختلفة.

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


## المفهوم الأساسي

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**تعامل المقال على أنه رسوم بيانية حيث العقدة هي الجمل والحوافز هي التشابهات. قم بتشغيل PageRank (أو شيء مماثل) على الرسم البياني لتحديد الجمل حسب مدى ارتباطها بكل شيء آخر. الجمل التي تحصل على أعلى درجات هي الملخص. التنفيذ القنوني هو **TextRank**(Mihalcea و Tarau، 2004).
> **抽取式（Extractive）。**إلى حد ما، فإن العدد هو العدد، والعدد هو العدد، والعدد هو التشابه.**TextRank**(ميهالسيّا و طاراو، 2004)

**Abstractive.**ضبط محول مبرمجة مبرمجة (BART ، T5 ، Pegasus) على أزواج المستندات الموجزة. عند الاستنتاج ، يقرأ النموذج المستند ويولد الموجزة الموجزة عبر الانتباه. يستخدم Pegasus بشكل خاص هدف التدريب المسبق لعبارة الفجوة مما يجعله ممتازًا في التجميع دون الكثير من التضبط المضيء.
> **生成式（Abstractive）。**في المقالة- المزودة على التداول الصغرى Transformer 编码器-解码器(BART、T5、Pegasus) ・・・ توصيل،模型读取文档并通过交叉注意力对代币 生成摘要。Pegasus 特别使用间隔句子预训目标,使它无需太多微调就擅长摘要。

التقييم مع **ROUGE**(تدقيق متجه إلى التذكر لتقييم النقاش). ROUGE-1 و ROUGE-2 نقاط التداخل بين واحد المخطط والبيجرام. ROUGE-L علامات أطول التالي الشائع. أعلى هو أفضل ولكن 40 ROUGE-L هو "جيد" و 50 هو "مستثنائي". كل ورقة تقرير كل ثلاثة. استخدم `rouge-score`الحزمة
> استخدام **ROUGE**(تأثيرات التفكير في التقييم) 评估──ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠──ROUGE-L 评分最长公共子序列──越高越好,但40 ROUGE-L 是"好",50 是"出色"──每篇论文都报告全部三个──使用`rouge-score`-كلا

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.


## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

```figure
summarize-collapse
```

## بناءها

### الخطوة الأولى: النص (المخرج)
> 两件事值得注意── استخدام وظيفة التشابه على تعدد التوحيد الكلمة التكلفة، وهو التغير الأصلي لـ TextRank──TF-IDF إلى المتوسط المتبقية التشابهية أيضا.

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

اثنين من الأشياء التي تستحق الإسم. تستخدم وظيفة التشابه تداخل الكلمات المعتادة في السجل ، وهو التنوع الأصلي من TextRank. يعمل كوسين متجهات TF-IDF أيضًا. عامل التخفيف 0.85 وعدد التكرار هي الافتراضات القابلة لصفحة.
> بارت-كبير-CNN على CNN/DailyMail 语料 على التغييرات.

### الخطوة الثانية: التجريد مع BART
> 始终使用词干提取──没有它,"running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

يتم ضبط BART-big-CNN على جهاز CNN / DailyMail. فإنه ينتج ملخصات في نمط الأخبار خارج الصندوق. بالنسبة للمناطق الأخرى (الأوراق العلمية، الحوار، القانونية) ، استخدم نقطة تفتيش Pegasus المقابلة أو ضبط بياناتك المستهدفة.
> لقد كان ROUGE مؤشرًا مُجردًا رئيسيًا لـ2010 عامًا ، ولكن في عام 2026 لم يعد هناك ما يكفي منه.

### الخطوة الثالثة: تقييم ROUGE
> - **BERTScore**(上下文嵌入相似度) في عام 2023 حصلت على اهتمام، الآن معظم المقالة المقتطفة مقالات مع ROUGE واحد التقارير.
- **BARTScore**سوف تقيم المخرج: من خلال التدريب المسبق BART  إعطاء المخرجات المحددة وقت تخصيص لامتثال المنتجات.
- **MoverScore**(على متن التطبيقات المضمنة) في 2025 يصل إلى القمة في المرحلة الزمنية المختلفة، لأنه أفضل من الزهرة في التقاط تعدد الكلمات.
- **FactCC**和**基于 QA 的事实性检查**في 2021-2023 سنة شائعة جدا، الآن عادة ما تكون **G-Eval**(نوع من GPT-4 提示链, باستخدام سلسلة التفكير في التقييمات连贯性,一致性,流性和相关性)
- **G-Eval**وطبيعة الحال، تقييم الجامعة الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعية الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة الجامعة

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

لا يُمكنك استخدام كلمة "جري" و "جري" ككلمات مختلفة و "روج" ككلمات أقل
> النتائج: تقرير ROUGE-L يستخدم للتقارن الوراثي، BERTScore يستخدم للتعبيرات، G-Eval يستخدم للتماسك والحقيقة.

### خارج ROUGE (2026 تقييم الموجب)
> من السهل أن تنتج المنتجات المنتجة تخيلات. مخاطر الخروج من المنتجات المنتجة هي أقل بكثير، لأن المنتجات هي المنتجة من المصدر بشكل متقدم، على الرغم من أن العبارات المنتجة يتم تحريرها عن النص الأساسي أو الزمن أو التسلسل المرتبط، فإنها لا تزال يمكن أن تكون خاطئة.

كانت ROUGE المقياس المهيمن لـ20 عامًا ، وهي غير كافية بمفردها في عام 2026 ، وقد أظهر تحليل كبير لملفات NLG:
> 需要命名的幻觉类型:

- **BERTScore**(مثل التضمين السياسي) اكتسب أرضاً حتى عام 2023 ويتم الإبلاغ عنه الآن إلى جانب ROUGE في معظم ورقات التجميع.
- **BARTScore**يعامل التقييم كإنتاج: قم بتقييم الموجة الموجة على مدى احتمالية تخصيصها من قبل المختصين بالبرنامج من قبل المختصين بمصدر.
- **MoverScore**(مسافة Earth Mover على التوابل السياقية) وصلت إلى المركز الأعلى في مقاييس التجميع في عام 2025 لأنه يحتوي على تداخل معنوي أفضل من ROUGE.
- **FactCC**و**QA-based faithfulness**كانت شائعة في الفترة من 2021 إلى 2023، والآن غالباً ما يتم استبدالها بـ **G-Eval**(سلسلة استشارات GPT-4 التي تسجل التماسك والاتساق والسريعة والسطح مع التفكير السلسلة).
- **G-Eval**وتتطابق نهجات القاضي في الجامعة مع الحكم البشري في 80% من الأحيان عندما يتم تصميم الروايات بشكل جيد.
> - **实体替换。**源说 "جون سميث"―摘要说 "جون براون"―
- **数字漂移。**源说 "25,000"―摘要说 "25 مليون"―
- **极性翻转。**源说 "رفضت العرض"―摘要说 "قبلت العرض"―
- **事实编造。**لم يذكر الرئيس التنفيذي 摘要说CEO 批准了

توصية الإنتاج: تقرير ROUGE-L للمقارنة القديمة، ورقم BERTScore للتداخل التدريجي، G-Eval للتماسك والحقائق. تحسّن ضد 50-100 ملخص بشري.
> طريقة تقييم فعالة:

### الخطوة الرابعة: مشكلة الواقعية
> - **FactCC。**في الحرف المصدر والحرف المقتطفة
- **基于 QA 的事实性检查。**إلى QA 模型 سؤال مصدر أسئلة في الإجابة.
- **实体级 F1。**مقارنة بين المصدر والكيان المسمّى في المقتطف.

الموجبات الجامعية هي عرضة للهلوسة. الموجبات الجامعية تحمل خطر الهلوسة أقل بكثير لأن المخرج يتم رفعها حرفيا من المصدر، على الرغم من أنها لا تزال يمكن أن تضلل إذا كانت الجملة المصدرية غير سياقية أو قديمة أو اقتباس خارج النظام. هذا هو السبب الوحيد الأكبر أنظمة الإنتاج لا تزال تفضل طرق الاستخراج للمحتوى المجاور للالتزام.
>  للمحتوى المستخدم المطلوب من الناحية الفعلية (إخباريات، طبيات، قانون، مالية) ، فإن الاستخراج أكثر أماناً من الاختيار المخصص.

أنواع الهلوسة للكشف عن:

- **Entity swap.**المصدر يقول "جون سميث" و المختصر يقول "جون براون".
- **Number drift.**المصدر يقول "25,000". الموجب يقول "25 مليون".
- **Polarity flip.**المصدر يقول "رفضت العرض" و المختصر يقول "قبل العرض"
- **Fact invention.**المصدر لا يذكر الرئيس التنفيذي، الموجز يقول أن الرئيس التنفيذي وافق

تقييمات النهج التي تعمل:

- **FactCC.**مصنف ثنائي مدرب على التواصل بين الجملة المصدرة والجملة الملخصة. يتوقع حقيقية / غير واقعية.
- **QA-based factuality.**اطلب من نموذج QA أسئلة تجيبها في المصدر. إذا كان الموجب يدعم إجابات مختلفة، علامة.
- **Entity-level F1.**مقارنة الكيانات المسموح بها في المصدر مقابل الموجة. الكيانات الموجودة فقط في الموجة المشتبه بها.

بالنسبة لأي شيء يواجه المستخدم حيث تُعتبر الحقيقة مهمة (اخبار، طبية، قانونية، مالية) ، فإن الاستخراج هو الاختيار الأكثر أماناً. يحتاج الامتصاص إلى فحص حقيقية في الحلقة.

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.


> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

"مجموعة 2026"
> 2026 年技术:

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> ‬ ‫استعمال المشهد‬ ‫‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


غالبا ما تغلب LLM ذات السياق الطويل على النماذج المتخصصة في عام 2026 عندما لا تكون الحساب قيوداً. التنازل هو التكلفة والتكاثر ؛ وتعطى النماذج المتخصصة نتائج أكثر استناداً.
> 2026 سنة في الحسابات ليست محدودة، فإن المهارات العليا العليا عادة ما تتجاوز المثاليات المخصصة.


## أرسلها .

إبقوا`outputs/skill-summary-picker.md`:
> 保存为 `outputs/skill-summary-picker.md`:

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## تمارين التدريب

1. **Easy.**قم بتشغيل مقالة النص على 5 مقالات أخبار. مقارنة العبارات الثلاثة الأولى لموجز مرجعي. قم بعد ROUGE-L. يجب أن ترى 30-45 ROUGE-L على مقالات على شكل CNN / DailyMail.
2. **Medium.**تنفيذ الواقعية على مستوى الكيان: استخراج الكيانات المسمى من المصدر والملخص (spaCy) ، استدعاء حسابي لكيانات المصدر في الملخص ودقة الكيانات المملحة مقابل المصدر. الدقة العالية والدقة المنخفضة تعني آمنة ولكن موجزة؛ الدقة المنخفضة تعني الكيانات الهلوسة.
3. **Hard.**مقارنة BART-Great-CNN مع LLM (Claude أو GPT-4) على 50 مقالة CNN / DailyMail. تقرير ROUGE-L، والوقائع (بحسب الكيان F1) والتكلفة لكل ملخص. وثيقة حيث يفوز كل واحد.
> 1. **简单。**في 5 篇新闻文章上运行 TextRank. 将 top-3 句子与参考摘要比较. 测量ROUGE-L.
2. **中等。**实现实体级事实性:从源和摘要中提取命名实体(spaCy),计算源实体在摘要中的召唤率和摘要实体对源的精确率──高精确率低召唤率意味着安全但简略;低精确率意味着幻觉实体──
3. **困难。**في 50 篇 CNN/DailyMail 文章上比较 BART-big-CNN مع LLM(Claude أو GPT-4) ―― تقرير ROUGE-L、事实性(بحسب الفوركس F1) وكل اقتباس 文章──记录各自的胜利场景──

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> ♪ المفاهيم ♪ ♪ الناس يقولونها ♪
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) الورقة الكنسية الاستخراجية
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)ورقة "بارت"
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) بيغاسوس والهدف من الجملة الفارغة.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)ورق حمراء
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661)ورقة المشهد الواقعية
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) بيغاسوس و间隔句子目标。
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文。
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) واقعية 整景论文
