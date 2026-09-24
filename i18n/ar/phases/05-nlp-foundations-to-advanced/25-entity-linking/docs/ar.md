# الكيانات ربط وتشويش

> وجدت "باريس". إن الكيان الذي يربط يقرر: باريس، فرنسا؟ باريس هيلتون؟ باريس، تكساس؟ باريس (الأمير الطرويجي) ؟ بدون ربط، يبقى جدول المعرفة غير واضح.
> نير 找到了 "باريس"──实体链接决定: باريس 法国? باريس 希尔顿? باريس 德克萨斯? باريس 特洛伊王子?

> **【中文解读】**لنشر NER 提取 إلى المادة الوحيدة في قاعدة المعرفة

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

يصل الارتباط الكيان (EL) إلى كل مذكرة إلى مدخل فريد في قاعدة المعرفة (ويكيديتا وويكيبيديا و GeoNames). خط الأنابيب المكون من خطوتين: إنتاج المرشحين (العثور على مطابقات محتملة) والتحليل (اختر الحق).

> 实体链接(EL) سوف تحدد كل指称解析为知识库(Wikidata、Wikipedia、GeoNames) من بين المواد الوحيدة.

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم وتطبيق هذه التقنية بشكل صحيح في المشاريع العملية.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض الأساس النظري والفكرة الأساسية.

**Candidate generation.**نظراً لـ "أورادانا"، أي إدخالات KB تتطابق؟ استخدم مطابقة السلاسل، وإعادة توجيه القرارات، وتقديرات شعبية. عادةً ما تستعيد أفضل 10 إلى 50 مرشحاً.

> **候选生成。**给定 "الاردن"، أي المعلومات المرتبطة؟ استخدام الخطوط المرتبطة 重定向解析和流行度先验──通常检索前 10-50 个候选──

**Disambiguation.**تصنيف المرشحين حسب شباهة السياق. دوي-مؤشر للسرعة، وترابط متعدد للدقة. السياق = النص المحيط + وصف الكيان من KB.

> **消歧。**按上下文相似度排名候选──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، NLP المجال شهد تحولات فانوسية

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الأنظمة الأكثر شيوعا في التطبيقات التجارية للذكاء الاصطناعي.

> **【拓展：NLP 的多语言挑战】**يوجد في العالم أكثر من 7000 لغة، ولكن دراسات اللغة النووية تركز بشكل رئيسي على اللغة الإنجليزية واللغة القليلة.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية المركزية.
```figure
gx-entity-linking
```

## بناءها

### الخطوة 1: بناء مؤشر مستعار من إعادة توجيهات ويكيبيديا

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

بيانات ويكيبيديا الاسم الأولي: ~ 18M (اسم الأولي، كيان) أزواج. تنزيل من Wikidata dumps. تخزين كإندكس معاكس.

### الخطوة الثانية: التشويش القائم على السياق

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】**هذا القسم يظهر كيفية استخدام الإطار الناضج للتطبيق السريع لهذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارة أساسية لمهندسين النظام البيولوجي.

## استخدمها في إطار التنفيذ

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج على المنتجات المتاحة.

- **OpenTapioca.**ال ال ال خفيف ال ال ال ال ال ل ويكيديتا. / OpenTapioca。 ويكيديتا 轻量 EL。
- **REL (Radboud Entity Linker).**أحدث ويكيبيديا EL. / REL。先进 ويكيبيديا EL。
- **GENRE.**الكيان السلطوي المتراجع يربط بواسطة فيسبوك. / GENRE。 فيسبوك 自回归实体链接。
- **LLM prompting.**اطلب من ماجستير الشهادة أن يكون واضحاً

## أرسلها .

إبقوا`outputs/skill-entity-linker.md`:

> 保存为 `outputs/skill-entity-linker.md`:

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## تمارين التدريب

1. **Easy.**بناء مولد مرشح على أساس ويكيبيديا. / **简单。**构建基于维基百科的候选生成器──
2. **Medium.**تنفيذ تشكيل ثنائي التشويش وتقييم على مجموعة اختبار. / **中等。**实现双编码器消歧──
3. **Hard.**مقارنة EL القائمة على LLM مقابل EL العصبي على مجموعة بيانات متعددة اللغات. / **困难。**في مجموعة بيانات متعددة اللغات مقارنة LLM EL بمقابل العقل EL.

## شروط الرئيسية

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## المزيد من القراءة

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自归实体链接──
