# علامات البوست والتحليل المزمنة

> كانت الحجم غير موضع الطراز لفترة، ثم كل خط أنابيب ماجستير في العلوم الحكمة يحتاج إلى التحقق من الاستخراج المهيكلي،
> 语法 كان يوماً غير منتشرة. بعد ذلك كل LLM 流水线都需要验证结构化抽取, it again came back.

> **【中文解读】**给每一个词标注词性,分析句子的语法结构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

الدروس الأولى وعدت بأن الـ "ليميتازيشن" تحتاج إلى علامة جزء من الكلام`running`هو فعل، لا يمكن لمهاتيزر أن يقلله إلى`run`بدون معرفة`better`هو صفت، لا يمكن أن تقلل إلى `good`. . .

> 第01 课承诺过词形回原需要词性标注――不知道 `running`نعم, نعم, نعم, نعم`run`لا أعرف`better`هو صيغة كلمة، لا يمكن أن تستعيد`good`.

هذا الوعد يخفي حقلًا فرعيًا كاملًا. تعيين جزء من الكلام للفئات الجهامية. تحليل النصية يعيد بنية الجملة: أي كلمة تعدل أي كلمة ، أي فعل يحكم أي حجج. قضى النمط النووي الكلاسيكي عشرين عامًا على تحسين كل منهما. ثم انهيار التعلم العميق في مهمة تصنيف رمزية فوق محول مقدم تدريب ، ومتواصل مجتمع البحث.

> ذلك الالتزام خلف يخفي في مجال كامل من التوزيعات. وتقسيمات الكلمات. وتقسيمات الكلمات. وتقسيمات الكلمات. وتحليلات الكلمات. تعيد تشكيلات الكلمات.

لا مجتمع التطبيق. لا يزال كل خط أنابيب استخراج مهيكلي يستخدم أشجار POS ومدرجة الاعتماد تحت الغطاء. يتم التحقق من JSON التي تم إنشاؤها من خلال LLM ضد القيود النحوية. تقوم أنظمة الإجابة على الأسئلة بتفكيك الأسئلة باستخدام أجزاء تعتمد. يقوم مقدمو جودة الترجمة الآلية بتحقق من التوجه لأجزاء الأجزاء.

> 应用界没有──每一个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

هذا الدروس يقدم لك علامات التجديد، خطوط الأساس، ونقطة حيث تتوقف عن تنفيذها من الصفر وتدعو spaCy.

> 值得了解──本课介绍标签集、基线以及你停止从零实现转而调用空间的节点──

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**POS tagging**يضع علامات على كل رمز مع فئة صفرية.**Penn Treebank (PTB)**التجست هي الإنجليزية الافتراضية. 36 علامة مع الاختلافات يجد القارئ العادي مزعج: `NN`اسم واحد، `NNS`اسم متعدد`NNP`اسم خاص واحد`VBD`فعل الماضي،`VBZ`الفعل الشخص الثالث المتفرد الحاضر، وهلم جرا.**Universal Dependencies (UD)**التجست أكثر قاسية (17 علامة) ومتعددة اللغات؛ وأصبحت الافتراض الافتراضي للعمل عبر اللغات.

> **词性标注（POS Tagging）**لكل رمز 标注语法类别。**Penn Treebank (PTB)**标签集是英语的默认选择──36标签,带有一般读者觉得过于细致的区别:`NN`单数名词、`NNS`复数名词`NNP`专名词单数、`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**标签集更粗(17 个标签) و غير مرتبطة باللغة؛ أصبحت اختيارًا متضمنًا للعمل عبر اللغات.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**يُنتج شجرة.

> **句法分析（Syntactic Parsing）**تُنتج شجرة.

- **Constituency parsing.**تعبيرات اسمية، تعبيرات فعل، تعبيرات تعبيرات تعويضية تعيش داخل بعضها البعض. الناتج هي شجرة من الفئات غير النهائية (NP، VP، PP) مع الكلمات كوراق.
  **成分分析（Constituency Parsing）。**اسم اسم اسم قصير، اسم اسم اسم قصير، اسم اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم قصير، اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم اسم
- **Dependency parsing.**كل كلمة لديها كلمة رأس واحدة تعتمد عليها ، وتتسم بالعلاقة الجهامية. الناتج هي شجرة حيث كل حافة هي (الرأس ، والاعتماد ، والعلاقة) ثلاثية.
  **依存分析（Dependency Parsing）。**كل كلمة لديها مركز لها، علامة على علاقة.

فاز تحليل الاعتماد في 2010s لأنه يجميع بشكل نظيف عبر اللغات، وخاصة تلك التي من ترتيب الكلمات الحرة.

> تحليل الاعتماد في 2010 تمت انتصاره ، لأنه عبر اللغات泛化更干净 ، وخاصة لبرنامج الحرية.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
pos-tagger
```

```figure
dependency-arcs
```

## بناءها

### الخطوة الأولى: نقطة أساسية للشخصيات الأكثر شيوعاً

أهم علامة POS التي تعمل، لكل كلمة، توقع علامة كانت لديها في التدريب

> أحدث علامات التسجيل المستخدمة في التدريبات.

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

على الجسم البراون، هذا الخط الأساسي يصل إلى دقة 85٪. ليس جيدا، ولكن الأرضية التي لا ينبغي أن تسقط أي نموذج خطير.

> في المجموعة البنية، هذا القيادة يصل إلى نسبة دقة حوالي 85%.

### الخطوة الثانية: علامة HMM الكبيرة

نموذج احتمال المشترك للانتظام:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

الجداول الثانية: احتمالات الانتقال (التسمية مع التسمية السابقة) ، احتمالات الانبعاث (التسمية مع الكلمة). تقدير كل من العد مع تسطيح لابلاس. فك مع Viterbi (برمجة ديناميكية على شبكة التسمية).

> 两个表:转移概率(给定前一个标签的标签概率),发射概率(给定标签的词概率) ・・・ كلتاؤما من الحسابات باستخدام 拉普拉斯平滑估算── باستخدام Viterbi 解码(在标签格上的动态规划) ・・・

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

البيغرام HMM على براون يصل إلى دقة ~ 93٪. قفزة من 85% إلى 93% هي معظم احتمالات الانتقال  يتعلم النموذج `DET NOUN`هو شائع و`NOUN DET`نادرة

> في المجموعة الثانية من المواد اللغة البراونية HMM  يصل إلى 93% من معدلات الدقة  من 85% إلى 93% من القفز`DET NOUN`هو عادة`NOUN DET`هو نادر جداً

### الخطوة الثالثة: لماذا يضرب المشاركون الحديثون هذا

احتمالات الانتقال + الانبعاثات محلية.`saw`هو اسم في "لقد اشتريت ورقة" ولكن فعل في "شاهدت الفيلم". CRF مع ميزات تعسفية (التضاف، شكل الكلمة، كلمة قبل وبعد، كلمة نفسها) يصل ~97٪. BiLSTM-CRF أو المحول يصل ~98% +.

> 转移 + 发射概率是局部的──它们无法捕获`saw`في "شريعتُ ورقةً" بينها اسم كلمة لكن في "شاهدتُ الفيلم" بينها كلمة متحركة.

يحدد السقف على هذه المهمة من خلال خلاف الملاحظين. الملاحظون البشريين يوافقون على حوالي 97% من الوقت على بن تريبانك. النماذج التي تجاوزت 98% على الأرجح تتجاوز معدات الاختبار.

> تم التوصل إلى اتفاق في حوالي 97% من الوقت من قبل المؤشرين في بن تريبانك.

### الخطوة الرابعة: رسم تحليل الاعتماد

التبعية الكاملة تحليل من الصفر خارج نطاق؛ التعامل الكانوني دروس الكتاب هو في جورافسكي ومارتن. العائلات الكلاسيكية للاعتراف:

> من التحقق من التحليل التأمين الكامل خارج نطاق؛ التعليمات الكلاسيكية التعاملة انظر Jurafsky و مارتن.

- **Transition-based**تعمل المصفحات (مستعدة للقوس ، ومعايير القوس) مثل المصفحات المقللة للدورة: فهي تقرأ الرموز ، وتحويلها إلى كومة ، وتطبق إجراءات تقلل تخلق القوس. يتم تشفير الشموع بسرعة. التنفيذ الكلاسيكي هو MaltParser. النسخة العصبية الحديثة: المصفح القائم على انتقال تشين ومانينغ.
  **基于转移的**解析器(arc-eager、arc-standard) مثل تحرك إلى الداخل 解析器一样工作:读入代币,移进到上,应用创建弧的归约动作──贪解码很快──经典实现是MaltParser──现代神经版本:Chen 和 Manning 的基于转移的解析器──
- **Graph-based**يُسجلُ الجزر (الخوارزميةِ الآيزنرِ، Dozat-Manning biaffine) كل حافةٍ محتملةٍ تعتمد على الرأس ويحددُ الأشجارِ التي تُمتدُ أقصى مدىً. أبطأُ ولكن أكثر دقةً.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) على كل ممكنة رأس-اعتماد 边打分,选择最大生成树──更慢但更准确──

بالنسبة لمعظم العمل المطبق، اتصل بـ spaCy:

>  بالنسبة لمعظم التطبيقات،

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

اقرأ`dep`عمود من أسفل إلى أعلى و هيكل الجملة النحوية ينزلق.

> من أسفل إلى أعلى`dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

كل مكتبة إنتاج NLP ترسل POS و إحصائيات الاعتماد كجزء من خط أنابيب قياسي.

> كل إنتاج من النفط النووية 库都把 POS 和依赖解析器作为标准流水线的一部分提供──

- **spaCy**(`en_core_web_sm`- لا ، لا`md`- لا ، لا`lg`- لا ، لا`trf`السرعة، الدقة، متكاملة مع التكنولوجيا + NER + التنظيم. `token.tag_`(بين) ، `token.pos_`(UD) ، `token.dep_`(علاقة الاعتماد)
  **spaCy**(`en_core_web_sm`- لا ، لا`md`- لا ، لا`lg`- لا ، لا`trf`)──快速、准确,与分词 + NER + 词形还原集成──`token.tag_`(بين)`token.pos_`(UD)`token.dep_`(تعتمد على علاقة)
- **Stanford NLP (stanza)**. خليفة ستانفورد لـ CoreNLP . أحدث التكنولوجيا على أكثر من 60 لغة
  **Stanford NLP (stanza)** استبدال ستانفورد كور ن ل ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب ب
- **trankit**-تعتمد على محول، دقة جيدة
  **trankit** على أساس المحول، جيد UD 准确率‬
- **NLTK**. .`pos_tag`قابلة للاستخدام، بطيئة، أكبر سناً، جيدة للتدريس
  **NLTK**.`pos_tag`❖可用、慢、较旧──适合教学──

### حيث لا يزال هذا مهمًا في عام 2026

- **Lemmatization.**الدروس رقم واحد تحتاج إلى POS لتعريفها بشكل صحيح دائماً
  **词形还原。**第01 课需要 POS 才能正确词形还原──始终如此──
- **Structured extraction from LLM outputs.**تأكيد أن الجملة المولدة تحترم القيود النحوية (مثل اتفاق الموضوع والفعل، والتحديلات المطلوبة).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束(如主谓一致、必要修饰语)
- **Aspect-based sentiment.**تحليلات الاعتماد تخبرك أي صفت تعدل أي اسم
  **基于方面的情感分析。**تحليل الاعتماد يخبرك أي اسم تعبير
- **Query understanding.**"الأفلام التي قام بها (ويس أندرسون) بتمثيل (بيل موراي) " تتحلل إلى قيود مهيكلة عبر التحليل.
  **查询理解。**"الأفلام التي قام بها ويس أندرسون بتمثيل بيل موراي"
- **Cross-lingual transfer.**علامات UD وعلاقات الاعتماد هي لغوية-مجهولة، مما يسمح بتحليل هيكلي صفر إطلاق من اللغات الجديدة.
  **跨语言迁移。**الدعاية العلامات والتبعية مع اللغة لا علاقة لها، دعم التحليل الهيكلي للنموذج التجاري للغات الجديدة.
- **Low-compute pipelines.**إذا لم تتمكن من شحن محول، فإن POS + تحليل الاعتماد + جاجتير يجعلك متفاجئاً بعيداً.
  **低算力流水线。**إذا لم تتمكن من نشر محول، فيمكنك أن تتحرك بعيداً

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/skill-grammar-pipeline.md`:

> 保存为 `outputs/skill-grammar-pipeline.md`:

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**باستخدام خط الأساس الأكثر تواترًا على مجموعة صغيرة من العلامات (على سبيل المثال ، مجموعة فرعية براون من NLTK) ، قياس دقة الجمل التي تم استمرارها. تحقق من نتيجة ~ 85٪.
   **简单。**في مصطلحات العلامات الصغيرة مثل NLTK (براون 子集) التي تستخدم بشكل متكرر على أساس العلامات، يتم قياس معدل الادقة على العبارات التي تركها.
2. **Medium.**قم بتدريب HMM الكبير أعلاه وتقرير الدقة / استدعاء لكل علامة.
   **中等。**訓練上述二元组 HMM 并报告每标签精确率/召回率──HMM أسهل اختلاط أي علامات؟
3. **Hard.**استخدم تحليل الاعتماد spaCy لاستخراج ثلاثة أجزاء من الموضوع - الفعل - الموضوع من عينة 1000 جملة. تقييم على 50 ثلاثية معلقة يدويا. وثيقة حيث يفشل استخراج (غالبا ما تكون السلبية والتنسيقات والموضيع المتفردة).
   **困难。**استخدام تحليل الاعتماد على spaCy من 1000 جملة نموذج تم الاستخدام من بين المجموعة الرئيسية بـ 50 علامة يدوية تم تقييمها على مجموعة الثلاثة نقاط.

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) المعالجة الكانونية لكتب الدراسة لـ POS والتحليل. / POS 和解析的经典教科书处理。
- [Universal Dependencies project](https://universaldependencies.org/) مجموعة علامات متعددة اللغات ومجموعة "شجرة المصرف" المستخدمة من قبل كل محلل متعدد اللغات. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) إشارة عملية لكل سمة تم عرضها على `Token`. / `Token`المعلومات المستخدمة لكل من هذه الصفات
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf)الورقة التي أحضرت المفصلات العصبية إلى السيطرة الرئيسية.
