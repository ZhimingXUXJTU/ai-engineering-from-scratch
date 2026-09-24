# إنتاج النص قبل المحولات  نموذجات اللغة N-gram   منتج  السابقة النص

> إذا كانت الكلمة مفاجئة، فإن النموذج سيء، والحيرة تجعل المفاجأة رقم، والسلم يبقيه محدود.
> إذا كان كلمة مدهشة، النموذج لا يُحسن.

> **【中文解读】**N-gram 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

قبل المحولات، قبل RNNs، قبل التوابل الكلمة، تمت توقعات نموذج اللغة الكلمة التالية عن طريق احتساب عدد المرات التي تلتها السابقة `n-1`عد "الكات" → "جلوس" 47 مرة، "الكات" → "قفز" 12 مرة، "الكات" → "الثلاجة" 0 مرة. عادي للحصول على توزيع الاحتمالات.

> في ترانسفورمتر  قبل، في RNN  قبل، في كلمة في داخل قبل، لغوي نموذج من خلال统计前 `n-1`个词后面跟着当前词的频率来预测下一个词――统计 " القط " → "الجلوس " 出现 47 次, " القط " → "قفز " 出现 12 次, " القط " → " المبرد " 出现 0 次。归结得到概率分布──

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.

هذا نموذج لغة n-gram. لقد عمل كل متعرف على الكلام، كل فحص الأحرف، وكل نظام ترجمة الآلة القائم على العبارات من عام 1980 إلى عام 2015.

> هذا هو نموذج اللغة n-gram. من عام 1980 إلى عام 2015، كان يعمل في كل جهاز تعريف الصوت، كل جهاز تحليل النصوص، وكل نظام ترجمة آلية على أساس القصص.

المشكلة المثيرة للاهتمام هي ما يجب القيام به حول n-غرامات غير مرئية. النموذج الخام القائم على العد يخصص احتمال صفر لأي شيء لم يراه ، وهو كارثي لأن الجمل طويلة وكل جملة طويلة تقريبًا تحتوي على تسلسل غير مرئي على الأقل. خمسين عامًا من البحث المُسطح قد حَل ذلك. تسطيح كنيسر-ني هو النتيجة ، وتورث التعلم العميق الحديث تقاليدها التجريبية.

> السؤال المثير للاهتمام هو: كيفية التعامل مع غير المرئي n-gram. النموذج المستند إلى الحساب الأصلي لتوزيع صفر احتمالية على أي شيء غير المرئي، وهذا أمر كارثي، لأن العبارات طويلة، تقريبا كل عبارة طويلة تحتوي على على على حد الأقل سلسلة غير المرئية.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### لعبة التنبؤ

قبل وجود أي من هذه الآلات، كان هناك تجربة تحدد ما هو نموذج اللغة. تغطي الحرف التالي من الجملة الإنجليزية. اطلب من شخص ما أن يحدد ذلك، تخمين واحد في كل مرة، حتى يحصلون عليه بشكل صحيح. اكتب عدد الخمين. كرر لعدة مئات من الحروف.

حسابات الاحتمالات ليست أمراً بسيطاً. إنها إعادة تشفير النص دون خسائر: سلم سلسلة الاحتمالات إلى شخص آخر، متطابق ويمكن أن يعيد بناء كل حرف، لأنه في كل موقف يعرف بالضبط أي تخمينات تأتي أولاً. رسالة يمكنك إعادة تشفيرها في عدد أقل من الرموز تحمل معلومات أقل لكل رمز، لذلك تضع إحصاءات حسابات الاحتمالات سقفًا على إنجليزية.

شانون) قام بإجراء هذا في عام 1951) و حصل على رقم لا يزال يحكم الحقل.`log2(27) ≈ 4.75`بيتات لكل حرف. المُخمنون البشريون مع 100 حرف من السياق وصلوا بين 0.6 و1.3 بيتات لكل حرف. اللغة الإنجليزية هي حوالي ثلاثة أرباع التحركات القسرية. تم قياس الهيكل الذي يجب أن يتعلمه النموذج قبل أن يتمكن أي نموذج من تعلمه.

كل نموذج لغوي منذ ذلك الحين هو لاعب ميكانيكي لهذه اللعبة، وكل رقم تقييم في هذه الدروس هو اللعبة التي تم تسجيلها:

- **Cross-entropy loss**هو متوسط عدد البيتات التي يحتاجها النموذج لكل رمز. تدريب LM هو حرفيا تقليل درجة له في لعبة التخمين.
- **Perplexity**هو`2^bits`(أو `e^nats`): عامل التفرق الذي لا يزال يواجه النموذج بعد تخميناته. تخمين موحد على 27 رمزا هو الارتباك 27؛ لاعب 1 بت لكل حرف لديه الارتباك 2.
- **Context length is the player's memory.**نموذج التريغرام يلعب مع رموز الذاكرة اثنين. محول يلعب نفس اللعبة مع رموز 100K. القواعد لم تتغير أبدا. أصبح اللاعب أفضل.

واحد واحد لتحويل المسار: تسجيلات اللعبة لكل حرف في بيت (`log2`), بينما الصيغة n-غرام أدناه تسجل لكل كلمة رمز في ناتس (سجل طبيعي)  ومنذ الارتباك `e^H`في الأرقام المتساوية`2^H`في البيت، فإن المشاهدين هما نفس القياس في وحدات مختلفة.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- إصلاح`n`(عادة 3 للاستعمال الثلاثي، 4 للاستعمال الثلاثي)

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})` ثابتة`n`(ثلاثة أجزاء عادةً تكون 3، أربعة أجزاء تكون 4)

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**أي ن-جرام لا يظهر في التدريب يحصل على احتمال صفر. وجدت دراسة عام 2007 على برون كوربوس أن حتى نموذج 4 جرام كان لديه 30٪ من 4 جرام غير مرئية في التدريب. لا يمكنك تقييم على أي نص حقيقي دون تسطيع.

> **零计数问题。**تم الحصول على احتمالات صفر من أي مجموعة من المواد التي لم تظهر في أي تدريب. اكتشفت دراسة عام 2007 على قاعدة البيانات البراونية أن حتى نموذج مجموعة أربعة فئة لديه 30% من المجموعات الأربعة التي لم تظهر في أي تدريب.

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**إضافة واحد لكل عدّة بسيط، فظيع في الأحداث النادرة
   **拉普拉斯（加一）。**إضافة 1 إلى كل عدد بسيط، ولكن في الحوادث النادرة، النتيجة هي ضعيفة
2. **Good-Turing.**أعيد توزيع كتلة الاحتمالات من الأحداث ذات التردد العالي إلى غير المرئية بناءً على تردد التردد
   **Good-Turing。**基于频率的频率,将概率质量从高频事件重新分配到未见事件──
3. **Interpolation.**الجمع بين n-gram، (n-1)-gram، وما إلى ذلك، التقديرات مع الوزن المتناسب.
   **插值。**تستخدم تعديل الوزن
4. **Backoff.**إذا كان عدد n-gram 0، انخفض إلى (n-1) -gram. كاتز بيكوف يطبق هذا.
   **回退。**إذا n-gram 计数为零، 回退到 (n-1) -gram──Katz 回退将归归一化──
5. **Absolute discounting.**خفض خصم ثابت `D`من كل العدد، إعادة توزيع إلى الغيب.
   **绝对折扣。**من جميع الحسابات تخفيض خصم ثابت`D`, إعادة توزيعها على الأحداث غير المرئية
6. **Kneser-Ney.**تخفيض مطلق بالإضافة إلى خيار ذكي لنموذج النظام الأدنى: استخدام * احتمال الاستمرار* (كم من السياقات تظهر كلمة) بدلاً من التردد الخام.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择: استخدام*续接概率*(一个词出现多少上下文中) بدلاً من المعدل الأصلي‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

إنّ رؤية (كنيسر-نيي) عميقة. "سان فرانسيسكو" هي لغة كبيرة شائعة. يظهر اللوحة الواحدة "فرانسيسكو" في الغالب بعد "سان". تخفيضات متساوية مطلقة تعطي "فرانسيسكو" احتمالية واحدة عالية (لأن العدد مرتفع). يلاحظ كنيسر-ني أن "فرانسيسكو" يظهر في سياق واحد فقط ويقلل من احتمال استمرارها وفقًا لذلك. النتيجة: الكلام الكبير الذي ينتهي بـ "فرانسيسكو" يحصل على احتمال المناسب منخفض.

> إنّ "سان فرانسيسكو" هو مجموعة ثنائية شائعة. يظهر "سان" في المجموعة الرئيسية. يظهر "سان" في المجموعة الثانية. يظهر "سان فرانسيسكو" في المجموعة الثانية. يظهر "سان فرانسيسكو" في المجموعة الثانية.

**Evaluation: perplexity.**معدل احتمالات السجل السلبي المتوسط لكل كلمة على مجموعة اختبار مستمرة. أقل هو أفضل. معدل الارتباك من 100 يعني أن النموذج مشوش كما سيكون اختيار متساوية بين 100 كلمة.

> **评估：困惑度。**留出测试集上每字平均负对数似然指数──越低越好──困惑度 100 يعني درجة الغموض في النموذج تساوي متوسط الاختيار بين 100 كلمة──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
ngram-backoff
```

## بناءها

### الخطوة الأولى: حسابات الأربعية

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

المدخل هو قائمة من الجمل المرموزة. الخروج هو عدد n-جرام والحسابات السياقية. `<s>`و`</s>`هذه حدود الجملة

> 输入是分词后的句子列表──输出是n-gram 计数和上下文计数──`<s>`和 `</s>`"إنها الحدود"

### الخطوة الثانية: تسطيح اللابلاست

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

إضافة 1 لكل عدّة، يُسطح لكن يُفرض الكثير من الكتلة على الأحداث غير المرئية، ويحطّم الأحداث النادرة المعروفة أيضاً.

> 给每一个计数加1――平滑但过度分配质量给未见事件,也伤害已知罕见事件──

### الخطوة الثالثة: كنيسر-ني (بيغرام، متقاطع)

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

ثلاثة أجزاء متحركة`continuation_prob`يحتوي على "كم من السياقات المختلفة التي تظهر فيها هذه الكلمة؟" (ابتكار كنيسر-نيي). `lambda_prev`هي الكتلة التي تم تحريرها من خلال الخصم، تستخدم لوزن الخلف. الاحتمال النهائي هو الحد الأساسي المخصوم بالإضافة إلى الحد المثقل المتابع.

> ثلاثة أشكال`continuation_prob`捕获 "هذا الكلمة تظهر في كثير من الأحيان على النص التالي؟"`lambda_prev`هو نوعية الإفراج عن خصم، للاستخدام في إضافة الخصم إلى العودة.

### الخطوة الرابعة: إنتاج النص مع أخذ العينات

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

أخذ العينات متناسبة مع الاحتمال. يعطي دائماً نتائج مختلفة لكل بذرة. لإنتاج شبيه بالشعاع البحثي، اختر argmax في كل خطوة (طموح) واضافة زر عشوائي صغير (درجة الحرارة).

> 根据概率比例采样. 种子总是给出不同的输出. 对于类似束搜索的输出,每步取 argmax. 贪心.并加一个小随机性旋. 温度.

### الخطوة 5: الارتباك

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

أقل هو أفضل. بالنسبة لـ Brown corpus، نموذج KN المنسق بشكل جيد من 4 غرامات يصل إلى معقدة حوالي 140. محول LM يصل إلى 15-30 على نفس مجموعة الاختبار. الفجوة حوالي 10x. هذا الفجوة هو السبب في أن الحقل انتقل.

> 越低越好── بالنسبة لمكتبة اللغة البراونية، فإن الفوارق التي تمتد بشكل جيد إلى أربعة أجزاء من KN 模型 مغرورة حوالي 140── تصل نموذج اللغة المتحول إلى 15-30 فى نفس المجموعة الاختبارية── الفرق حوالي 10 مرات── هذا الفرق هو السبب في تحول هذا المجال──

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

- **Classical NLP teaching.**أوضح تعرض للطفولة، و MLE، والتحيرات التي يمكنك الحصول عليها.
  **经典 NLP 教学。**أفضل تجربة واضحة يمكنك الحصول عليها
- **KenLM.**المكتبة الإنتاجية n-gram. تستخدم كمسجل في النظم الكلامية و MT حيث تقل التأخير.
  **KenLM。**生产级 n-gram 库──用作低延迟语音和MT 系统的重评分器──
- **On-device autocomplete.**نماذج التريغرام في لوحة المفاتيح
  **设备端自动补全。**键盘中的三元组模型── لا يزال في استخدام──
- **Baselines.**دائماً احسب معقدة LM n-جرام قبل إعلان LM عصبي الخاص بك جيدة. إذا لم تحولك يفوق KN بحافة واسعة، هناك شيء خاطئ.
  **基线。**قبل أن تعلن عن نموذج لغتك العصبية جيد، دائماً احسب n جرام من LM 困惑度── إذا كان Transformer  لا يضرب KN بشكل كبير، ثم هناك مشكلة──

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/prompt-lm-baseline.md`:

> 保存为 `outputs/prompt-lm-baseline.md`:

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

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**قم بتدريب ثلاثية الأبعاد على مجموعة شكسبير من 1000 جملة، وخلق 20 جملة ستكون معقولة محلياً ولكن غير متماسكة عالمياً. هذه هي التجربة القنونية.
   **简单。**تعليّم على 1000 جملة في لغة الشاطبية. تولّد 20 جملة.
2. **Medium.**قم بتنفيذ الارتباك لنموذج KN الخاص بك على شيكسبير المزدوج. مقارنة مع Laplace. يجب أن ترى KN أقل الارتباك بنسبة 30-50٪.
   **中等。**في تركيب شكسبيا تقسيم على نموذجك كي ننجح في الارتباك.
3. **Hard.**بناء مُصحّح حجة التراكم: مع إعطاء كلمة خاطئة وتحديدها، تولّد تصحيحات وتصنيف حسب احتمالية السياق تحت المُصطلح. تقييم على مجموعة التراكم البيركبك (عامة).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按LM 下的上下文概率排序──在伯克贝克 拼写语料库(公开) 上评估──

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) العلاج القنوني لـ n-gram LM والسلاسة. / n-gram 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) الورقة التي تسوية كنيسر-ني كأفضل n-جرام سلاسة. / 确定 كنيسر-ني 为最佳 n-جرام 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) ورقة KN الأصلية. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) إنتاج سريع n-gram LM، لا يزال يستخدم في 2026 للتطبيقات الحساسة بالخمول. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## المزيد من القراءة

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf)تجربة اللعبة التي تحدد الهدف كل نموذج لغة لا يزال يُحسن.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) العلاج القنوني لـ n-gram LM والسطح.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)الورقة التي تسوية كنيسر-ني كأفضل n-جرام سلاسة.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) ورق KN الأصلي
- [KenLM](https://kheafield.com/code/kenlm/) إنتاج سريع n-gram LM، لا يزال يستخدم في 2026 للتطبيقات الحساسة بالتكسّف.
