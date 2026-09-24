# معلومات الاستعراض والبحث

> BM25 دقيقة ولكن هشة، فهي تلقي شبكة واسعة لكن تفوت الكلمات الرئيسية، الهجينة هي الاختيار الافتراضي لعام 2026. كل شيء آخر يُصنّف.
> BM25 精确但脆弱──密检索撒大网但漏掉关键词──混合检索是2026年默认选择──其余都是调参──

> **【中文解读】**من الكلمات الرئيسية المتناسبة إلى استكشاف الطاقة.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## المشكلة المشكلة المشكلة

يكتب المستخدم "ما يحدث إذا كذب شخص ما للحصول على المال" ويوقع العثور على القانون الذي يغطي ذلك بالفعل: "القسم 420 IPC". يفتقد بحث الكلمات الرئيسية إلى ذلك بالكامل (لا يوجد مفردة مشتركة). يفتقد بحث معنوي إذا لم يتم تدريب التوابع على النص القانوني. يجب على البحث الحقيقي التعامل مع كليهما.
> المستخدم يدخل "ما يحدث إذا كان شخص يكذب للحصول على المال" وليس يتوقع العثور على تغطية فعلية لهذا المحتوى: "المرسوم 420 IPC"── مطلوبة الكلمات الرئيسية بحث تماما لا يصل إليه (((لا توجد تعريفات تعريفية)── إذا كان التثبيت لا يتم تدريبها على النصوص القانونية، فإن البحث في لغات أيضا سوف يخطئ من خلالها── البحث الحقيقي يجب معالجتها في نفس الوقت──

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.


إن IR هو خط الأنابيب تحت كل نظام RAG، كل شريط بحث، كل موقع وثائق البحث المضطرب. الهندسة المعمارية 2026 التي تعمل في الإنتاج ليست طريقة واحدة. إنها سلسلة من الطرق التكميلية، كل واحدة من الصادرة على فشل من قبل.
> إنّه نظام كلّ RAG، كلّ بحث، كلّ محطة وثائق، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ مُوجّد، كلّ، كلّ مُوجّد، كلّ مُد، كلّ مُوجّد، كلّ مُد، كلّ مُوجّد، كلّ، كلّ مُدّ، كلّ مُدّ، وكلّّ مُمُمُمُمُمُمُمُمُمُ مُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُُ

هذه الدروس تبني كل قطعة وأسماء تفشل كل صيد
> ويشير كل جزء من هذا الدروس إلى ما فشل في كل منهما.

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


## المفهوم الأساسي

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

أربعة طبقات اختر تلك التي تحتاجها
> أربع طوابق.

1. **Sparse retrieval (BM25).**سريع، دقيق في المقابلة الدقيقة، رهيب في التعريفات، إدراج مؤشر معاكس، تحت 10ms لكل استفسار على ملايين الوثائق، يحصل لك إشارات القانون، رموز المنتج، رسائل الخطأ، الكيانات المسمى الحق.
2. **Dense retrieval.**تشكيل استفسار وثائق إلى متجهات. بحث القريب القريب. تسجل المقاطع والتشابهات النطاقية. تفتقد مطابقات كلمات رئيسية دقيقة تختلف عن حرف واحد. 50-200ms لكل استفسار مع FAISS أو متجهات DB.
3. **Fusion.**دمج القوائم المتصنفة من النادرة والكثيفة. الاندماج المتبادل للرتبة (RRF) هو الافتراض السهل لأنه يتجاهل النتائج الخام (التي تعيش في مقياسات مختلفة) ويستخدم فقط مواقف الرتب. الاندماج الموزن هو خيار عندما تعرف إشارة واحدة تهيمن على مجالك.
4. **Cross-encoder rerank.**خذ العلوي 30 من الاندماج. تشغيل مُشفّر متقاطع (سؤال + وثيقة معاً، تسجيل كل زوج). حافظ على العلوي 5. المُشفّر المتقاطع أبطأ لكل زوج من المُشفّر الثنائي ولكن أكثر دقة بكثير. يمكنك إيقاف التكلفة عن طريق تشغيله فقط على العلوي 30.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万文档上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**سوف تتمكن من استخدام المعلومات والمواد المختلفة في البحث عن المعلومات والمواد المختلفة.
3. **融合。**合并稀疏和密的排列列表──倒数排列融合(RRF) هو خيار افتراضي بسيط ، لأنه يتجاهل النسبة الأصلية (((يوجد في مقياس مختلف) فقط باستخدام الموقع الترتيبى── عندما تعرف أن إشارة ما في مجالك تسيطر ، فإن إضافة الهيئة هي خيار──
4. **交叉编码器重排序。**من تركيب وسط أخذ أفضل 30 ∙: عمل صبور المعدات ∙: استفسار + 文档一起,对每对打分) ∙: الحفاظ على أفضل 5 ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: عمل صبور المعدات ∙: صبور المعدات ∙: صبور المعدات ∙: صبور المعدات ∙ صبور المعدات ∙ صبورة ∙ صبورة ∙ صبور المعدات : صبور : صبور : صبور : صبور : صبور : صبور: صبور: صبور: ص: ص: ص: ص: ص: ص:: ص:: ص:::: ص:::::

الاسترداد الثلاثي (BM25 + كثافة + متعلمة-المتفرقة مثل SPLADE) يتفوق على المتفرقة في مقاييس 2026 ولكن يحتاج إلى البنية التحتية لمؤشرات المتفرقة المتعلمة. بالنسبة لمعظم الفرق ، فإن إعادة ترتيب المتفرقة بالإضافة إلى المترجمات المتقاطعة هي نقطة الراحة.
> 三路检索(BM25 + 密 + 学习稀疏如 SPLADE) في عام 2026 كيساريا أفضل من اثنين من الطرق، ولكن تحتاج إلى تعلم البنية التحتية للتسجيلات الثقيلة.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.


## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

```figure
gx-hybrid-retrieval
```

## بناءها

### الخطوة الأولى: BM25 من الصفر
> اثنين من العناصر التي يجب أن تعرفها`k1=1.5`控制词频和;更高 يعني كلمة重复的权重更大──`b=0.75`控制长度归结;0 忽略文档长度,1 完全归结;;默认值是罗伯茨森 原始论文中的推值,很少需要调整;;

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

هناك مُعايير تستحق المعرفة`k1=1.5`يسيطر على الاكتفاء في تردد المدى؛ أعلى يعني المزيد من الوزن على تكرار المدى. `b=0.75`يسيطر على التطبيع على الطول؛ 0 يتجاهل طول الوثيقة، 1 يطبيع بشكل كامل. التوصيات الافتراضية هي توصيات روبرتسون من الورقة الأصلية ونادرا ما تحتاج إلى ضبط.
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2`هو 384 维,快速, على معظم English检索足够强.`paraphrase-multilingual-MiniLM-L12-v2` أعلى معدل الاصلاح`bge-large-en-v1.5`أو`e5-large-v2`.

### الخطوة الثانية: استرداد كثيف مع جهاز تشفير ثنائي
> `k=60`常数来自原始RRF 论文──更高的 `k`لتساوي مساهمة التفاوت في التصنيف ؛ أقل `k`60 هو القيمة ال默认 التي تم نشرها، لا تحتاج إلى تعديل.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2 تعاديل التوابل حتى النقطة المنتج يساوي كوسين. `all-MiniLM-L6-v2`هو 384 عمق، سريع، وقوي بما فيه الكفاية لمعظم الاستخدامات الإنجليزية.`paraphrase-multilingual-MiniLM-L12-v2`.للمحاسبة الدقيقة القصوى`bge-large-en-v1.5`أو`e5-large-v2`. . .
> 三阶段组合──BM25 找到词汇匹配──密找到语义匹配──RRF 合并两个排名而不需要分数校准──交叉编码器使用查询文档对重新对 top-30 打分,捕获双编码器遗漏的细粒度相关性──保留 top-5──

### الخطوة الثالثة: الاندماج المتبادل
> ‬ ‫المعنى
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

- نعم`k=60`المستمر يأتي من ورقة RRF الأصلية. أعلى `k`يُسطح مساهمة الفروق في الرتب ؛ أقل `k`60 هي النشرة الافتراضية المنشورة ونادرا ما تحتاج إلى ضبط.
> خاصة على RAG، معدات الاختبار**Recall@k**هو الأرقام الأهم.. إذا لم يتم التركيز على الوصول إلى المقطع الصحيح، فلن يستطيع القارئ الإجابة..

### الخطوة الرابعة: البحث الهجري + إعادة التصنيف
> 调试技巧:对于失败的查询,对比稀疏和密排名──如果一个找到正确文档而另一个没有,你有词汇不匹配(修复:添加缺失的一半) 或语义歧义(修复:更好的嵌入或重排序器)──

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

ثلاثة مراحل مؤلفة. BM25 يجد مطابقات لغوية. يجد مطابقات سمانية كثيفة. RRF يدمج التصنيفات الثنائية دون الحاجة إلى تصفية النتيجة. يقوم جهاز التشفير عبر التشفير بإعادة تسجيل أفضل 30 باستخدام أزواج الوثائق الاستفسارية معاً، مما يلتقط أهمية حبة دقيقة لم يتم إغلاق جهاز التشفير الثنائي. حافظ على الـ 5 الأولى.

### الخطوة 5: التقييم

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

وبالتحديد لـ RAG**Recall@k**من الجهاز الاحتياطي هو الأهم رقم. القارئ الخاص بك لا يمكن أن تجيب إذا كان المقطع الصحيح ليس في مجموعة استرداد.

نصيحة إزالة الأخطاء: بالنسبة للطلبات الفاشلة، فلتختلف في التصنيف النادر والكثيف. إذا وجد أحد الوثائق الصحيحة والآخر لا، لديك عدم مطابقة المفردات (تصحيح: إضافة النصف المفقود) أو غموضة معنوية (تصحيح: إدخال أفضل أو إعادة ترتيب).


> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.


"مجموعة 2026"
> 2026 年技术:

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> ‬ ‫القياس التكنولوجي‬ ‬
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

أياً كان ما تختارينه، ميزانية للتقييم. استرداد الموازين قبل استرجاع دقة RAG من نهاية إلى نهاية. القارئ لا يستطيع إصلاح ما غاب عن الاسترداد.
> مهما اختار، يجب أن يقوم بالقيام بتقييم الميزانية.

### الدروس التي اكتسبت بجد من 2026 الإنتاج RAG
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**团队花几周交换 LLM 和调优提示,而检索每三次查询就安静地回归错误的上下文──先修复分块──
- **分块策略比分块大小更重要。**固定大小分割会破坏表格、代码和嵌套标题──句子感知是默认选择;语义或基于LLM 分块在技术文档和产品手册有回报──
- **父文档模式。**检索小的"子"块以获得精度── عندما تظهر العديد من الكتل في نفس القسم، تغيير داخل الكتل لإبقاء على نطاق الزمنية.
- **k_rerank=3 通常最优。**كل زيادة من كتلة تزيد من هذا العدد سوف تزيد من الرمز التكوين وتولد تأخير دون تحسين جودة الإجابة.
- **HyDE / 查询扩展。**من استفسار إنتاج إجابة افتراضية، وضعتها، والبحث.
- **上下文预算控制在 8K token 以下。**في هذا الحد الأساسي يعني إعادة ترتيبات القيمة
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题率 关控在用户看到之前阻止回归──
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**، خاصة استفسارات مختلطة و لغوية.

- **80% of RAG failures trace to ingestion and chunking, not the model.**الفريق يقضي أسابيع في تبادل الـ "إل إل إم" وتحسين الإشارات بينما يسترد البحث بشكل هادئ السياق الخطأ في كل استفسار ثالث
- **Chunking strategy matters more than chunk size.**تقسيمات الحجم الثابتة تكسر الجداول والرموز والرؤوس المضمنة. إن إدراك الجملة هو الافتراض الافتراضي؛ والجزء المستند إلى التعريف أو القانون الدولي يُكافئ عن الوثائق التقنية واليدويات المنتجة.
- **Parent-doc pattern.**استرداد قطع صغيرة "الطفل" للحصول على دقة. عندما يظهر العديد من الأطفال من نفس القسم الوالد، قم بتبادل الكتل الوالدية للحفاظ على السياق. هذا يرفع جودة الإجابة باستمرار دون إعادة التدريب.
- **k_rerank=3 is usually optimal.**كل جزء إضافي من الماضي يضيف تكلفة رمزية وتخفيف توليد دون رفع جودة الإجابة. إذا كان k=8 لا يزال أفضل من k=3 بالنسبة لك، فإن المرتبة المُجددة غير فعالة.
- **HyDE / query expansion.**توليد إجابة افتراضية من السؤال، تضمين ذلك، استرداد. سيلوي الفجوة بين الأسئلة القصيرة والوثائق الطويلة. مفتوحة رفع الدقة دون تدريب.
- **Context budget under 8K tokens.**ضربات متسقة عند هذا الحد يعني أن عتبة إعادة المرتبة متخففة جداً
- **Version everything.**الإشارات، قواعد التجزئة، نموذج التضمين، إعادة التصنيف. أي تجرف يخسر صامتة جودة الإجابة. بوابات المعلوماتية على الوفاء، دقة السياق، ومعدل السؤال غير المطلوب قبل أن يراه المستخدمون.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**على مقارنات 2026، وخاصةً بالنسبة للمسائل التي تربط الأسماء المناسبة مع التعريفات. إرسالها عندما تدعم البنية التحتية مؤشرات SPLADE.
> وفقاً لقياسات الصناعة لعام 2026، فإن تصميم الاختبار الصحيح يقلل من 70-90% من الظلال. معظم أداءات RAG تتم من تحسين الاختبار الأفضل، وليس من تحسينات النموذج.

يقلل تصميم الاسترداد المناسب من الهلوسات بنسبة 70-90٪ وفقاً لقياسات الصناعة عام 2026. تأتي معظم مكاسب أداء RAG من أفضل الاسترداد ، وليس من ضبط النموذج.

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


## أرسلها .

إبقوا`outputs/skill-retrieval-picker.md`:
> 保存为 `outputs/skill-retrieval-picker.md`:

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


## تمارين التدريب

1. **Easy.**تنفيذ`hybrid_search`في مجموعة من 500 وثيقة اختبار 20 استفسار مقارنة التذكير في 5 بين BM25 فقط، كثافة فقط، وهيبريد
2. **Medium.**إضافة حساب MRR. لكل استفسار اختبار مع وثيقة صحيحة معروفة، العثور على رتبة الوثيقة الصحيحة في BM25، والرتبات الكثيفة، والهجرية. إبلاغ MRR لكل.
3. **Hard.**قم بتحسين مبرمجة كثيفة على نطاقك باستخدام MultipleNegativesRankingLoss (متحولات الحكم). قم ببناء مجموعة تدريبية من 500 زوج من أزواج الملفات. قم بمقارنة استدعاءات قبل وبعد التحسين.
> 1. **简单。**على 500  الملفات المفردة على تحقيق أعلاه `hybrid_search`△测试 20 个查询──比较 BM25 فقط、 كثافة فقط 和混合的回忆@5──
2. **中等。**إضافة MRR  حسابها. لجميع استفسارات الاختبار التي تمت معرفتها بالوثائق الصحيحة، العثور على المستند الصحيح في المرتبة BM25 密和混合.
3. **困难。**استخدام المتعدد السلبي (RankingLoss) ((Sentence Transformers) في مجالك من 500 استفسار وثائق على مجموعات التدريبات على البناء

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> ♪ المفاهيم ♪ ♪ الناس يقولونها ♪
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) العلاج النهائي بـ BM25.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR، المُشفّر الثنائي القنوني.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)-المتعلمة-المتفردة التي تغلق الفجوة مع كثافة.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)ورق RRF
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) استرداد التفاعل المتأخر.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) دبي آر، كلاسيكي
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)                                                                                                                                                                                                                                                              
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文。
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索。
