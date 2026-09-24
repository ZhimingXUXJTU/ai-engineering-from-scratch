# موضوع النمذجة  LDA و BERTopic  موضوع الإنشاء  LDA و BERTopic

> LDA: المستندات هي مزيج من المواضيع، والمواضيع هي توزيع على الكلمات. BERTopic: مجموعة المستندات في مساحة التضمين، المجموعات هي المواضيع. نفس الهدف، تفكير مختلف.
> LDA:文档是主题的混合,主题是词的分布.BERTopic:文档在嵌入空间中的聚类,聚类就是主题.

> **【中文解读】**LDA باستخدام نموذج الاحتمالية العثور على الموضوع، BERTopic باستخدام BERT 嵌入──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## المشكلة المشكلة المشكلة

لديك 10 آلاف تذكرة دعم العملاء، 50 ألف مقالة أخبار، أو 200 ألف تغريدة. تحتاج إلى معرفة ما هو المجموعة دون قراءتها. ليس لديك علامات على الفئات. أنت لا تعرف حتى كم فئة موجودة.
> لديك 10 آلاف 张客户支持工单,50,000 篇新闻文章或200,000 条推文── تحتاج إلى معرفة موضوع المجموعة دون قراءة── لا توجد لديك فئة مرموقة── لا تعرف حتى كم فئة موجودة──

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.


وذلك بدون إشراف، أعطيه مجموعة صغيرة من المواضيع المتماسكة، و، لكل وثيقة، توزيع على تلك المواضيع.
> موضوع بناء الإجابة على هذا السؤال دون إشراف. أعطيه قاعدة من المواد، وعود إلى مجموعة من المواضيع المتصلة، فضلا عن توزيع كل وثيقة على هذه المواضيع.

تتهيمن عائلتان خوارزمية. يعامل LDA (2003) كل وثيقة كمزيج من المواضيع الخفية وكل موضوع كموزع على الكلمات. التوصل هو بايسي. لا يزال يُنتج في الإنتاج حيث تحتاج إلى تفويضات موضوعية مزيجة الأعضاء وتوزيعات احتمالية مستوى الكلمات يمكن تفسيرها.
> يُعتبر كل وثيقة مختلطة من المواضيع المحتملة، وتوزيع كل موضوع من المواضيع المحتملة.

برتوبيك (2020) يرمز الوثائق مع برت، ويقلل من الامتعداد مع UMAP، ويقوم بتجميعها مع HDBSCAN، ويستخرج كلمات الموضوع عن طريق TF-IDF القائمة على الفئة. فاز في النص القصير، وسائل التواصل الاجتماعي، وأي شيء حيث يشبه التشابه الدلالي أكثر من تداخل الكلمات. يحصل مستند واحد على موضوع واحد، وهو قيود للمحتوى الطويل.
> بروتوبيك (بالإنجليزية: BERTopic) 2020) باستخدام بروت 编码文档، باستخدام UMAP 降维، باستخدام HDBSCAN 聚类، من خلال نوع TF-IDF 提取主题词──它在短文本、社交媒体和语义相似性比词重叠更重要的内容上胜出──一篇文档获得一个主题,这对长篇内容是一个限制──

هذه الدروس تبني على الحدس لكل منهما والاسم الذي يجب أن تختاره للجسم المعين.
> هذا الدروس يُستخدم لإنشاء التفكير المباشر و يُشير إلى أن المواد التي يجب اختيارها هي التي يجب اختيارها.

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


## المفهوم الأساسي

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**كل موضوع هو توزيع على الكلمات. كل وثيقة هو مزيج من الموضوعات. لتوليد كلمة في وثيقة، عينة موضوع من مزيج الوثيقة، ثم عينة كلمة من توزيع هذا الموضوع. العكس الإستدلال: مع العطاء الكلمات الملاحظة، استدلال توزيع الموضوع لكل وثيقة وتوزيع الكلمات لكل موضوع. استدلال غيبز المنهار أو Bayes التغيرات يقوم بالحساب.
> **LDA 生成故事。**كل موضوع هو توزيع الكلمات. كل مستند هو مزيج من الموضوع. يجب أن تولد كلمة في المستند، من مختلطة المستندات أخذ موضوع واحد، ثم من توزيع هذا الموضوع أخذ كلمة واحدة.

إنتاج LDA الرئيسي:
> 关键 LDA 输出:

- `doc_topic`: المصفوفة `(n_docs, n_topics)`، كل سطر يصل إلى 1 (مزيج الموضوع في الوثيقة).
- `topic_word`: المصفوفة `(n_topics, vocab_size)`, كل سطر يصل إلى 1 (توزيع الكلمات للموضوع).
> - `doc_topic`:矩阵 `(n_docs, n_topics)`, في كل صفوف مجموعها: 1
- `topic_word`:矩阵 `(n_topics, vocab_size)`, في كل صفوف مجموعها = 1 ((→

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. ترميز كل وثيقة مع محول جملة (مثل: `all-MiniLM-L6-v2`) 384 متجهات
2. خفض الأبعاد مع UMAP إلى ~ 5 أبعاد. إضافة BERT عالية جداً من التسمم للتجميع.
3. مجموعة مع HDBSCAN. على أساس الكثافة، تنتج مجموعات ذات الحجم المتغير وملف "غير متوقع".
4. لكل مجموعة، قم بحساب TF-IDF القائم على الفئة عبر وثائق الكتلة لاستخراج الكلمات الرئيسية.
> 1. 用句子 محولات`all-MiniLM-L6-v2`)编码每篇文档──384 维向量──
2. استخدام UMAP 降维到大约5维度.BERT 嵌入对聚类来维度太高.
3. استخدام HDBSCAN 聚类── على أساس الدرجة الكثافة، تكوين التغيرات الكبيرة 聚类和 "离群值" 标签──
4. للكافة الفئات، في الملفات المرتبة في المجموعة الحساب على أساس الفئة TF-IDF لتحقيق كلمات الدرجة الأولى.

إنتاج هو موضوع واحد لكل وثيقة (بضافة علامة خارجية -1). اختياريًا ، عضوية ناعمة عبر متجه الاحتمالات في HDBSCAN.
> 输出是每篇文档一个主题(加上 -1 离群值标签) ⋅可选地,通过 HDBSCAN的概率向量获得软成员资格──

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.


## بناء ذلك تحرك لتحقيق
```figure
topic-drift
```

## بناءها

### الخطوة الأولى: LDA عبر scikit-learn
> انتباه: تحويل توقف استخدام الكلمات، min_df 和 max_df 过罕见和无处不在的词, استخدام CountVectorizer(ليس TfidfVectorizer) ، لأن LDA 期望原始计数。

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

ملاحظة: تم إزالة الكلمات المتوقفة، فلتر min_df و max_df مصطلحات نادرة ومنتشرة، CountVectorizer (ليس TfidfVectorizer) لأن LDA تتوقع العد الخام.
> `Topic != -1`المقالة: (موقع البيانات)`min_topic_size`控制 HDBSCAN 最小聚类大小;BERTopic 库默认为 10──本例为课程规模显然设为 15──对于超过10,000 文档语料,增加到50或100──

### الخطوة الثانية: BERTopic (إنتاج)
> 两种方法都输出主题词――问题是这些词是否连贯――

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

الفلتر على`Topic != -1`يُسقط خزنة BERTopic الخارقة (الوثائق التي لم تتمكن HDBSCAN من تجميعها). `min_topic_size`يسيطر على الحد الأدنى من حجم الكلاستر HDBSCAN؛ المكتبة الافتراضية BERTopic هو 10. هذا المثال يحددها إلى 15 صراحة لمدى الدروس. بالنسبة للمستندات أكثر من 10,000، زيادة إلى 50 أو 100.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的NPMI(归一化逐点互信息), سوف يتم جمع العدد المحدد للقطاع الموضوعي, من خلال الصفوف المتوازنة مقارنة هذه القطاعات。越高越好。 استخدام `gensim.models.CoherenceModel`配 `coherence="c_v"`.
- **主题多样性。**所有主题顶级词中唯一词的比例──越高越好主题不重叠)──
- **定性检查。**هل تمت إسمهم بشيء حقيقي؟

### الخطوة الثالثة: التقييم

كل منهجين يخرجون كلمات موضوعية. السؤال هو ما إذا كانت هذه الكلمات متطابقة.

- **Topic coherence (c_v).**يجمع بين NPMI (المعلومات المتبادلة المنظمة من الناحية النقطية) من أزواج الكلمات العليا على سياقات النافذة المنزلقة ، ويجمع النتائج إلى متجهات الموضوع ، ويقارن تلك المتجهات عبر شبكة الكوزين. أعلى هو أفضل. استخدام `gensim.models.CoherenceModel`مع`coherence="c_v"`. . .
- **Topic diversity.**جزء من الكلمات الفريدة بين كلمات الرئيسية لجميع الموضوعات. أعلى هو أفضل (المواضيع لا تتداخل).
- **Qualitative inspection.**اقرأ الكلمات الرئيسية لكل موضوع هل يسمون شيئا حقيقيا؟ الحكم البشري لا يزال خط الدفاع الأخير.


> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## متى لا تختار أي

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

أكبر اعتبار عملي هو طول الوثيقة. إضافة BERT تقصص؛ LDA تعتبر العمل على أي طول. بالنسبة للوثائق أطول من سياق نموذج الإضافة، إما قطعة + جمع أو استخدام LDA.

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.


## استخدمها في إطار التنفيذ

"مجموعة 2026"
> 2026 年技术:

- **BERTopic.**افتراضية للنص القصير وأي شيء يهم في التعريف
- **`gensim.models.LdaModel`.**طراز LDA كلاسيكي للإنتاج، ناضج، اختبر في المعركة.
- **`sklearn.decomposition.LatentDirichletAllocation`.**-إلى التجارب
- **NMF.**عاملة المصفوفات غير السلبية بديل سريع لـ LDA، جودة مقارنة على النص القصير.
- **Top2Vec.**تصميم مشابه لبرتوبيك. مجتمع أصغر ولكن جيد في بعض المعايير.
- **FASTopic.**أحدث وأسرع من برتوبيك على الكوربوس الكبيرة جدا.
- **LLM-based labeling.**إشغلي أي مجموعة، ثم اطلب من نموذج لإسم كل مجموعة.
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**生产级经典 LDA,成熟,久经验──
- **`sklearn.decomposition.LatentDirichletAllocation`。**تجربة مع بساطة LDA
- **NMF。**غير负矩阵分解──LDA's快速替代,短文上质量相当──
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新,在超大语料上比BERTopic 快──
- **基于 LLM 的标注。**أطلقوا أيّة فئة ثم أطلبوا من كل فئة أن تُسمى

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


## أرسلها .

إبقوا`outputs/skill-topic-picker.md`:
> 保存为 `outputs/skill-topic-picker.md`:

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


## تمارين التدريب

1. **Easy.**تطبيق LDA مع 5 مواضيع على مجموعة بيانات 20 مجموعة الأخبار. طبع أفضل 10 كلمات لكل موضوع. وضع علامة على كل موضوع يدويا. هل وجد الخوارزمية الفئات الحقيقية؟
2. **Medium.**تطبيق BERTopic على نفس مجموعة الفرعية 20 مجموعة أخبار. مقارنة عدد المواضيع المكتسبة، الكلمات الرئيسية، والاتساق النوعي ضد LDA. أي من الفئات الحقيقية تظهر بشكل أكثر نظافة؟
3. **Hard.**احسب التماسك c_v لكل من LDA و BERTopic على جسمك. قم بتشغيل كل من 5، 10، 20، 50 موضوعًا. تراكم التماسك مقابل عدد الموضوعات. أبلغ عن الطريقة الأكثر استقرارًا عبر عدد الموضوعات.
> 1. **简单。**في 20 مجموعة أخبار على مجموعة بيانات باستخدام 5 مواضيع مناسبة لـ LDA.
2. **中等。**في نفس 20 مجموعة الأخبار  مجموعة مناسبة بروتوبيك  مقارنة العثور على عدد المواضيع  كلمات الدرجة الأولى  ارتباطات الوضع مع LDA  أي من أكثر وضوحاً عرض الفئة الحقيقية؟
3. **困难。**في تعدد LDA و BERTopic على المواد الخاصة بك، فهي تُستخدم 5、10、20、50 موضوعًا، وتُستخدم 5、10、20、50 موضوعًا، وتُستخدم 5、10、20、50 موضوعًا، وتُستخدم 5、10、20،50 موضوعًا، وتُستخدم 5、10、20、50 موضوعًا، وتُستخدم 5、10、20、50 موضوعًا، وتُستخدم 5、10、20、20،20،20،20،20،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،30،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،3،4،4،4،4،4،4،4،4 و10،4،4،4،4،4،4،4،4،4،4،4،4،4،4،4 و5،4،4،4،4،4،4،4،4،4 و4،4،4،4،4

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> ♪ المفاهيم ♪ ♪ الناس يقولونها ♪
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)- ورقة الـ "إل دي اي"
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) ورقة BERTopic
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)-الورقة التي تقدمت (سي) وأصدقاء
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) المرجحات الإنتاجية. أمثلة ممتازة.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
