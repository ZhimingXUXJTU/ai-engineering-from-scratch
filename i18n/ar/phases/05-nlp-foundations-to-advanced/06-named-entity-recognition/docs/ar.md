# اسم الكيان التعرف 命名实体识别 (NER)

> سحب الأسماء خارج. يبدو سهلا حتى تتعامل مع حدود غامضة، كيانات مستجمعة، وجرم النطاقات.
> ضع اسمها خارجها. تبدو بسيطة حتى تواجه الحدود المظلمة.

> **【中文解读】**من المقالة تعريف اسم الشخص، اسم الأرض، اسم المنظمة، وغيرها من الكيانات.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

"أبل دعمت جوجل بسبب صفقة بحثها عن iPhone في الولايات المتحدة". خمسة كيانات: Apple (ORG) ، Google (ORG) ، iPhone (PRODUCT) ، صفقة بحث (ربما) ، US (GPE). نظام NER جيد يستخرج جميعها مع أنواع صحيحة. واحد سيء يفتقد iPhone، يخلط Apple الفاكهة مع Apple الشركة، ويعطي علامة "US" كشخص.

> "أبل دعمت جوجل على صفقة بحثها عن iPhone في الولايات المتحدة". 五个实体:Apple(ORG) 、Google(ORG) 、iPhone(PRODUCT) 、بحث صفقة(可能) 、US(GPE) ✿.

إن إير هو الحصان المكلف تحت كل خط إستخراج مهيكلي. تحليل سير سير العمل، مسح سجل الامتثال، تحليل السجلات الطبية، فهم استفسارات البحث، تأسيس استجابات الـ "تشات بوت"، استخراج العقود القانونية. لا يمكنك أبداً رؤيتها تماماً، أنت دائماً تعتمد عليها.

> إن إر هو محرك عمل لكل عملية هيكلية لاستخراج التدفقات المائية. لا يمكنك أن ترى أي شيء عنها، ولكنك دائما تعتمد عليها.

هذه الدروس تمر المسار الكلاسيكي (قاعدة القواعد، HMM، CRF) إلى المسار الحديث (BiLSTM-CRF، ثم المحولات). كل خطوة تحل قيودا محددة من تلك التي قبلها. النمط هو الدروس.

> هذا الدروس من الطرق الكلاسيكية (((بناء على القواعد、HMM、CRF) إلى الطرق الحديثة ((BiLSTM-CRF ، ثم Transformer)  كل خطوة حلت حدود محددة للخطوة السابقة‬ هذا النموذج نفسه هو محتوى هذا القسم‬

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**BIO tagging**(أو BILOU) يُحول استخراج الكيان إلى مشكلة في وضع علامات التسلسل.`B-TYPE`(بدء الشركة)`I-TYPE`(كيان داخلي) ، أو`O`(خارج أي كيان)

> **BIO 标注**(أو بيلو) سوف يتم استئصال الكيانات إلى سلسلة علامات المشكلة.`B-TYPE`(实体开始)`I-TYPE`(في الواقع) أو`O`(ليس في أي جسم)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

سلسلة الكيانات متعددة الرموز: `New B-GPE`،`York I-GPE`،`City I-GPE`نموذج يفهم البيولوجي يمكن استخراج المدى التعسفي.

> 多 token 实体链接:`New B-GPE`.`York I-GPE`.`City I-GPE` فهم نموذج البيولوجي يمكن أن تستخدم أي طول

تقدم الهندسة المعمارية:

> 架构演进:

- **Rule-based.**البحث عن المعلومات المُعلنة، دقة عالية على الكيانات المعروفة، صفر تغطية على الكيانات الجديدة.
  **基于规则。**正则 + 地名词典查找──对已知实体精确率高,对新实体零覆盖──
- **HMM.**نموذج ماركوف المخفي احتمال الإصدار من علامة معينة، احتمال انتقال من علامة إلى علامة، تشفير فيتربي، تدريب على البيانات الملصقة.
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**الحقل العشوائي المشروط. مثل HMM ولكن تمييزي، حتى يمكنك خلط ميزات تعسفية (شكل الكلمات، الرموز، الكلمات المجاورة). لا يزال حصان العمل الإنتاج الكلاسيكي في عام 2026 للتنفيذات منخفضة الموارد.
  **CRF。**条件随机场──类似于 HMM ولكن判别式، لذلك يمكن اختلاط أي خصائص 词形、大小写、相邻词)── حتى عام 2026 لا يزال القوة المنتجة الكلاسيكية لتنفيذ الموارد المنخفضة──
- **BiLSTM-CRF.**الميزات العصبية بدلاً من صنعها يدوياً. LSTM تقرأ الجملة في كلا الاتجاهين، وطبقة CRF في الأعلى تفرض تسلسلات علامات متسقة.
  **BiLSTM-CRF。**العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية المختلفة: العلامات العلمية
- **Transformer-based.**تحديد المعلومات مع رأس تصنيف الرمز، أفضل دقة، أفضل حساب
  **基于 Transformer。**استخدم رمز 分类头微调BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
ner-bio-tagging
```

## بناءها

### الخطوة الأولى: مساعدي التسمية البيولوجية

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### الخطوة الثانية: الميزات المصنوعة يدوياً

بالنسبة لـ NER الكلاسيكية (غير العصبية) ، هي الميزات اللعبة. المفيدة:

> بالنسبة للطبيعية غير العصبية، خصائص هي المفتاح.

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`العائدات`xXxxxx`. .`word_shape("USA-2024")`العائدات`XXX-dddd`أنماط الرأسمالية هي إشارة عالية للاسمين المناسبين

> `word_shape("iPhone")`عودتي`xXxxxx`.`word_shape("USA-2024")`عودتي`XXX-dddd`◊ نمط الكتابة على المميزات هي علامات عالية

### الخطوة الثالثة: قاعدة بسيطة على القواعد + القاموس

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

المجلات الإنتاجية لديها ملايين الإدخالات المقطوعة من ويكيبيديا و DBpedia.`Apple`(الشركة مقابل الفاكهة) فظيع. لهذا السبب فاز النماذج الإحصائية.

> 生产地名词典有数百万条目,从维基百科 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`مقابل 水果`apple`(بسيطة جداً، هذا هو السبب في أن النتائج الإحصائية نجحت)

### الخطوة الرابعة: خطوة CRF (رسم، ليس إضافة كاملة)

الـ CRF الكامل من الصفر في 50 سطر لا يُنير بدون أساس نظرية الاحتمال.`sklearn-crfsuite`بدلاً من ذلك:

>  بدون أساس احتمالية  لا يُعرف كيفية تحقيق الميزانية الكاملة من الصفر إلى 50 صف `sklearn-crfsuite`:

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`و`c2`التنظيمات L1 و L2. `all_possible_transitions=True`يسمح للنموذج تعلم تسلسلات غير قانونية (مثل: `I-ORG`بعد`O`) غير محتمل، وهذا هو كيف أن CRF يفرض التماسك البيولوجي دون كتابة القيود.

> `c1`和 `c2`نعم L1 و L2`all_possible_transitions=True`让模型学习非法序列 (على سبيل المثال)`O`بعد ظهور`I-ORG`) غير محتمل، هذا هو طريقة CRF في حالة عدم كتابة حزم إضافية للوثوميات البيولوجية.

### الخطوة 5: ما يضيفه BiLSTM-CRF

يتم تعلم الميزات. المدخلات: إدخال الرمز (GloVe أو fastText). يقرأ LSTM من اليسار إلى اليمين و من اليمين إلى اليسار. تتجاوز الحالات الخفية المختلفة طبقة إنتاج CRF. لا يزال CRF يفرض استناداً لتتبع التسمية؛ ويستبدل LSTM الميزات المصنوعة يدوياً بالمتعلمات.

> تعريف تحول إلى تعلم الحصول على. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

لطبقة CRF، استخدم `torchcrf.CRF`المكاسب على CRF المصنوعة يدويا يمكن قياسها ولكن أقل مما تتوقع إلا إذا كان لديك عشرات الآلاف من الجمل المسموحة.

> CRF 层使用 `torchcrf.CRF`(بيب تثبيت مصباح الوقود)  مقارنة مع اليدوية ارتفاع CRF يمكن قياسه، ولكن مقارنة مع توقعاتك الصغيرة، إلا إذا كان لديك عدة آلاف من العلامات

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

إن spaCy تسافر في مستوى الإنتاج من نوع NER خارج الصندوق.

> المجال المفتوح يقدم على درجة الإنتاج NER.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

ملاحظة`iPhone`المعلقة`ORG`بدلاً من`PRODUCT` نموذج spaCy الصغير لديه تغطية ضعيفة للكيانات المنتجة.`en_core_web_lg`(تغيرات)`en_core_web_trf`) يفضل ذلك

> انتباه`iPhone`تم تسميتها`ORG`و لا`PRODUCT` نموذج spaCy الصغير على تغطية جسم المنتج ضعيفها.`en_core_web_lg`(更好──Transformer 模型(`en_core_web_trf`أفضل

"مُحَضّن" لـ "NER" القائم على "BERT":

> "القبض على الوجه" على أساس "BERT"

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`يدمج رموز B-X، I-X متواصلة في فترة. بدونها، تحصل على علامات على مستوى رموز وتضطر إلى دمج نفسك.

> `aggregation_strategy="simple"`ستقوم بـ B-X 、 I-X التوترات 合并 لـ عبرة. بدونها، تحصل على علامة   درجة التوترات، تحتاج إلى نفسها 合并.

### الـ "NER" القائم على الـ "LLM" (خيار 2026)

إن برنامج LLM NER الصفري والقليل الآن تنافس مع نماذج دقيقة في العديد من المجالات، وأفضل بشكل كبير عندما تكون البيانات المسموحة نادرة.

> 零样本和少样本 LLM NER الآن تنافسية مع النموذج المتنقل في العديد من المجالات، والمزايا أكبر في وقت النقص في البيانات العلامة التجارية.

- **Zero-shot prompting.**أعط ماجستير في التدريس قائمة من أنواع الكيانات ومثالية النظام. اطلب من إنتاج JSON. يعمل خارج الصندوق؛ الدقة معتدلة على المجالات الجديدة.
  **零样本提示。**عطاء LLM قائمة ونموذج نموذجية من نوع الفردية  تطلب JSON 输出  استخدام مفتوح؛ متوسط معدل الصلة في المجالات الجديدة 
- **ZeroTuneBio-style prompting.**قم بتحلل المهمة إلى استخراج المرشح → التفسير → الحكم → التحقق من جديد. تحفيز خطوة متعددة المراحل (ليس في وقت واحد) دقة بشكل كبير على NER الطبية الحيوية. يعمل نفس النمط للسيطرة القانونية والمالية والعلمية.
  **ZeroTuneBio 风格提示。**将任务分解为候选抽取 → 含义解释 → 判断 → 复查──多阶段提示(而不是 فوري) في الطب البيولوجي NER ارتفاع كبير في معدلات الادقة.
- **Dynamic prompting with RAG.**استعادة أكثر الأمثلة مسموحة مماثلة من مجموعة صغيرة من البذور الملحوظة لكل دعوة استنتاج؛ بناء عرض القليل من الألقاب على الفور. في معايير 2026، هذا يرفع GPT-4 الطبية الحيوية NER F1 بنسبة 11-12٪ على الاستجابة ثابتة.
  **动态 RAG 提示。**كل مرة من التفكير التدريب من عدد قليل من العلامات النباتية التركيز على الاختبار أكثر نموذج العلامات مماثلة؛ متحرك بناء أقل من نموذج النقاط. في اختبار 2026 عام، مما جعل GPT-4 生物医学 NER F1 ارتفاع 11-12٪ عن النقاط الحالي.
- **Per-entity-type decomposition.**بالنسبة للوثائق الطويلة، فإن مكالمة واحدة التي تستخرج جميع أنواع الكيانات في وقت واحد تفقد التذكر مع نمو الطول. قم بتشغيل مرور استخراج واحد لكل نوع الكيان. تكلفة استنتاج أعلى، دقة أعلى بشكل كبير. هذا النمط القياسي للملاحظات السريرية والعقود القانونية.
  **按实体类型分解。**بالنسبة إلى الملفات البارزة، فإن الاستخدام الواحد لجمع جميع أنواع الكائنات، مع زيادة المدة، سوف يزيد من معدل فقدان الاستخدامات.

توصية الإنتاج اعتبارا من عام 2026: ابدأ بموجب خطة أساسية لمدرسة التدريب قبل جمع بيانات التدريب. غالبًا ما تكون الفورمولا 1 جيدة بما فيه الكفاية بحيث لا تحتاج إلى ضبطها.

> 2026 سنة تجارية: قبل جمع بيانات التدريب، أولا استخدام LLM 零样本基线开始―― عادة ف1 يكفي، أنت أبدا لا تحتاج إلى التغييرات الصغيرة――

### حيث لا يزال النظام الكلاسيكي النووي يفوز

حتى مع الـ LLM المتاحة، نيل كلاسيكية عندما:

> حتى لو كان هناك ماجستير في العلوم المتاحة، النجاح في الحالات التالية:

- ميزانية التأخير أقل من 50ms
  الميزانية المتأخرة أقل من 50 ملي ثانية
- لديك الآلاف من الأمثلة المسموحة وتحتاج إلى 98٪ + F1.
  لديك آلاف العلامات و تحتاج إلى 98٪ + F1
- المجال لديه أونتولوجيا مستقرة حيث CRF أو BiLSTM المدربة مسبقا ينقل بشكل جيد.
  المجال لديه مستقر في البداية، قبل التدريب CRF أو BiLSTM 迁移良好──
- القيود التنظيمية تتطلب نموذجًا محليًا غير مولد.
  监管约束要求本地部署的非生成式模型──

### حيث انهار

- **Domain shift.**(نير) المدرب في العقود القانونية أسوأ من (جابريتر)
  **领域偏移。**في CoNLL 上訓練的NER 处理法律合同同时比地名词典还差──在你的领域上微调──
- **Nested entities.**"بنك أوف أمريكا برج" هو في نفس الوقت ORG و FASILITY. لا يمكن أن تمثل BIO القياسية التداخلات المتداخلة. تحتاج إلى NER المجمعة (نموذجات متعددة المرور أو القائمة على التداول).
  **嵌套实体。**"بنك أمريكا برج" 同时是 ORG 和 FASILITY──标准BIO 无法表示重叠跨度──你需要嵌套 NER(多遍或基于跨度的模型)──
- **Long entities.**"شركة التأمين على الودائع الاتحادية في الولايات المتحدة". نماذج مستوى الرمز أحيانا تقسيم هذا. استخدام `aggregation_strategy`أو بعد العملية
  **长实体。**"شركة التأمين على الودائع الاتحادية للولايات المتحدة"..`aggregation_strategy`أو بعد معالجة
- **Sparse types.**علامات NER الطبية مثل DRUG_BRAND، ADVERSE_EVENT، DOSE. النماذج العامة لا فكرة لها. Scispacy و BioBERT هي نقاط البداية هناك.
  **稀疏类型。**医疗 NER 标签如Drug_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知──Scispacy 和 BioBERT هي نقطة الوصول هناك──

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/skill-ner-picker.md`:

> 保存为 `outputs/skill-ner-picker.md`:

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**تنفيذ`bio_to_spans`(العكس من `spans_to_bio`) والتحقق من استنتاجية الرحلة الروتينية على 10 جمل.
   **简单。** تحقيق `bio_to_spans`(`spans_to_bio`(أو) و (أو) على 10 عبارات
2. **Medium.**تدريب مركز التدريبات المركزية للشركات المختلفة أعلاه على مجموعة بيانات NER الإنجليزية CoNLL-2003.`seqeval`النتيجة النموذجية: ~ 84 F1.
   **中等。**في CoNLL-2003 英文 NER 数据集上训练上述 sklearn-crfsuite CRF──使用 `seqeval`報告 لكل فئة F1── النتيجة النموذجية:~84 F1──
3. **Hard.**-حسناً`distilbert-base-cased`على مجموعة بيانات NER محددة للمجال (طبية أو قانونية أو مالية). مقارنة مع نموذج spaCy الصغير.
   **困难。**في مجال محدد من النظم النظرية`distilbert-base-cased`◊ مقارنة مع الفضاء ◊ سجل إفشال البيانات ◊

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360)ورقة BiLSTM-CRF. القنوني. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) يقدم نمط تصنيف الرمز الذي أصبح معيارًا. /  introduced into becoming standard token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) إشارة عملية لكل سمة على `Doc.ents`و`Span`. / `Doc.ents`和 `Span`المعلومات المستخدمة في كل صفة
- [seqeval](https://github.com/chakki-works/seqeval)المكتبة المقاييس الصحيحة استخدمه دائماً
