# استراتيجيات التجزئة لـ RAG

> يؤثر تشكيل التقطيع على جودة الاسترداد بقدر ما يؤثر على اختيار نموذج التضمين (Vectara NAACL 2025). الحصول على التقطيع الخطأ ولا توفر لك أي كمية من إعادة التصنيف.
> التنظيم على نوعية البحث هو أكبر من اختيار النموذج المضمن.

> **【中文解读】**في نظام RAG، كيفية تخصيص الملفات إلى قطاعات تؤثر مباشرة على نتائج البحث.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## المشكلة المشكلة المشكلة

لا يعد الإصلاح "شراء نموذج إضافة أفضل". الإصلاح هو التقطيع بشكل صحيح. أظهرت ورقة NAACL 2025 التي أصدرها Vectara أن استراتيجية التقطيع تشرح الكثير من التباين في جودة الاسترداد مثل اختيار إضافة.

> 修复方法不是 "买个更好的嵌入模型"──修复方法是正确分块──论文 NAACL 2025 文章 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文献 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文 文

> **【中文解读】**والسؤال الذي يطرحه هذا القسم هو: كيفية فهم وتطبيق هذه التقنية بشكل صحيح في التشغيل العملي.

في فبراير 2026 أظهرت النتائج المفاجئة: التجزئة الباهظة في الحجم الثابت مع قطع 100 رمز و 20 رمز تتداخل تفوق معظم استراتيجيات التجزئة " الذكية " على RAG العامة. يساعد التجزئة النطاقية على النص السردي. يساعد التجزئة على مستوى الجمل على محتوى على طراز FAQ. لا يوجد فوز عالمي.

> 2026 سنة 2 أشهر اختبار基准 أظهر نتائج مذهلة: بسيطة ثابتة大小分块(100 رمز زائد 20 رمز 重叠) في عام RAG فوق هزمت معظم " الذكاء " استراتيجيات 分块。

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض النظريات الأساسية والفكرة الأساسية.

**Fixed-size chunking.**تقسيم النص إلى كتلة N-token مع التداخل الاختياري. بسيط، سريع، فعال بشكل مفاجئ. الافتراضي في معظم أنظمة RAG الإنتاج.

> **固定大小分块。**تقسيم النص إلى N علامة كتلة، يمكن الاختيار فوقها.

**Sentence-level chunking.**تقسيم على حدود الجملة. كل جزء = جملة واحدة أو أكثر. جيد لمواجهة الأسئلة والرد قصير.

> **句子级分块。**في الحدود الحدودية للقواعد. كل قطعة = واحد أو أكثر من القواعد.

**Semantic chunking.**تضمين الجمل، مجموعة الجمل المتتالية مع تضمين مماثل في قطع. أفضل على النص السردي، أبطأ في الحساب.

> **语义分块。**嵌入句子,将嵌在相似连续句子分组为块──在叙述性文本上更好,计算更慢──

**Recursive character chunking.**تقسيمها بالفقرة ثم بالجملة ثم بالشخصية

> **递归字符分块。**按段落分割,然后按句子,然后按字符──长链的默认──好的通用启发式──

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمت التحول من "كل مهمة تدريب نموذج" إلى "نموذج واحد لحل جميع المهام" في مجال NLP.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الأنظمة الأكثر شيوعا في التطبيقات التجارية للذكاء الاصطناعي.

> **【拓展：NLP 的多语言挑战】**يوجد في العالم أكثر من 7000 لغة، ولكن دراسات اللغة النووية تركز بشكل رئيسي على اللغة الإنجليزية واللغة القليلة.
```figure
n5-chunk-cuts
```

## بناءها

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية المركزية.

### الخطوة الأولى: التجزئة ذات الحجم الثابت مع التداخل

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### الخطوة الثانية: التجزئة التفاصلية

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**هذا القسم يظهر كيفية استخدام الإطار الناضج للتطبيق السريع لهذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارة أساسية لمهندسين النظام البيولوجي.

## استخدمها في إطار التنفيذ

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج على المنتجات المتاحة.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## أرسلها .

إبقوا`outputs/skill-chunking-picker.md`:

> 保存为 `outputs/skill-chunking-picker.md`:

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## تمارين التدريب

1. **Easy.**تنفيذ التجزئة ذات الحجم الثابت مع التداخل. قياس جودة الاستخدام. / **简单。**实现固定大小分块──测量检索质量──
2. **Medium.**مقارنة الثابتة مقابل المقطع التفاصيل على مجموعة بيانات السردية. / **中等。**في بيانات التفاصيل مقارنة ثابتة بمقارنة مع الكتب
3. **Hard.**بناء خط أنابيب تحديد المكونات المثلى الذي يتكيف مع حجم المكونات لكل نوع من الوثائق. / **困难。**构建按文档类型自适应块大小的优分块流水线──

## شروط الرئيسية

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## المزيد من القراءة

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) مقياس التجزئة. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) تطبيقات شحوم. / 分块实现。
