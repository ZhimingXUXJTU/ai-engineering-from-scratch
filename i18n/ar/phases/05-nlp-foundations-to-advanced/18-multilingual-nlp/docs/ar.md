# اللغة متعددة اللغات

> نموذج واحد، أكثر من 100 لغة، صفر بيانات تدريبية بالنسبة لمعظمهم. الانتقال عبر اللغات هو المعجزة العملية للعام 2020.
> نموذج، 100+ لغة، معظم اللغات صفر تدريبات البيانات.

> **【中文解读】**多语言BERT、XLM-R 等模型处理多种语言──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

اللغة الإنجليزية لديها مليارات الأمثلة الملصقة. اللغة الأردية لديها الآلاف. اللغة الماثيلية لديها تقريباً أي واحدة. أي نظام عملي لإن إل بي الذي يخدم جمهور عالمي يجب أن يعمل على ذيل طويل من اللغات حيث لا توجد بيانات تدريب محددة للمهام.

> هناك مليارات نموذج التعليمات الإنجليزية. هناك آلاف اللغات الأوربية.

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.

نموذجات متعددة اللغات تحل هذا الأمر عن طريق تدريب نموذج واحد على العديد من اللغات في وقت واحد. تمثيل المشترك يسمح لنموذج نقل المهارات المتعلمة في لغات ذات الموارد العالية إلى لغات ذات الموارد المنخفضة. تحسين النموذج على تحليل المشاعر الإنجليزية، و ينتج توقعات المشاعر الجيدة بشكل مفاجئ على الأردو خارج الصندوق. هذا هو نقل عبر اللغات بدون إطلاق، وقد أعاد تشكيل كيفية نقل النفط النووي إلى العالم.

> نموذج متعدد اللغات من خلال تدريب نموذج واحد على العديد من اللغات في نفس الوقت لحل هذه المشكلة. تمثل التشارك في جعل نموذج نقل مهارات اللغة المكتسبة من الموارد العالية إلى اللغة المنخفضة. في تحليل العاطفة الإنجليزية، يمكن أن يكون نموذجًا جيدًا بشكل مدهشًا في اللغة الأوردية.

هذه الدروس تعبر عن التنازلات والنماذج القنونيّة والقرار الوحيد الذي يُحاول أن يُساعد الفرق الجديدة في العمل متعدّدة اللغات: اختيار لغة مصدر للتنقل.

> هذا الدروس يسمى الاختيار المتحركات لغة المبدأ

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**تستخدم النماذج متعددة اللغات رمز SentencePiece أو WordPiece المدرب على النص من جميع اللغات المستهدفة. يتم مشاركة المفردات: تمثل وحدة الكلمات الفرعية نفس المورفيم عبر اللغات ذات الصلة. `anti-`في الإنجليزية والإيطالية يحصلون على نفس الرمز.

> **共享词表。**تعتبر هذه اللغات من أشكال تعريفية، حيث يتم استخدامها في جميع اللغات المستهدفة.`anti-`الحصول على نفس الشعار

**Shared representation.**يتعلم محول مدرب مسبقًا على نمذجة اللغة المخفية عبر العديد من اللغات أن الجمل المماثلة في اللغات المختلفة تنتج حالات مخفية مماثلة. يظهر mBERT و XLM-R و NLLB هذا جميعًا. تضمينات "قطة" في اللغة الإنجليزية تشكل مجموعة بالقرب من "التحدث" بالفرنسية و "gato" باللغة الإسبانية ، وكذلك تضمينات الجملة الكاملة.

> **共享表示。**في العديد من اللغات لغة مخفية بناء التدريبات المسبقة على Transformer تعلم إلى مختلف اللغات 中语义相似ة الجملة تظهر حالة مخفية مماثلة.

**Zero-shot transfer.**قم بتحسين النموذج على البيانات المسموحة باللغة الواحدة (عادة الإنجليزية). عند الاستنتاج، قم بتشغيله على أي لغة أخرى يدعمها النموذج. لا حاجة إلى علامات اللغة المستهدفة. النتائج قوية بالنسبة للغات ذات صلة بالتصميم والضعيفة بالنسبة للغات البعيدة.

> **零样本迁移。**في لغة واحدة (معظمها الإنجليزية) ، يتم تعديل النموذج على بيانات العلامات.

**Few-shot fine-tuning.**إضافة 100-500 مثال معلّم في اللغة المستهدفة. يرتفع الدقة إلى 95-98% من الخط الأساسي الإنجليزي في مهام التصنيف. هذا هو الرافعة الوحيدة الأكثر فعالية من حيث التكلفة في اللغة متعددة اللغات.

> **少样本微调。**إضافة 100-500 نموذج من العلامات في اللغة المستهدفة. ارتفع معدل الصلة على المهام التنظيمية إلى 95-98% من القاعدة الإنجليزية.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## النماذج

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

اختيار حسب حالة الاستخدام. التصنيف يعمل بشكل جيد مع XLM-R-base باعتبارها الافتراض المعقول. مهام الجيل تتطلب mT5 أو NLLB اعتمادا على الترجمة مقابل الجيل المفتوح. أزواج عمل في نمط LLM مع Aya-23 أو Claude باستخدام استئناف متعدد اللغات صريح.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译vs开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## قرار اللغة المصدر (2026 بحث) ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ 2026 بحث)

معظم الفرق تُخَلِّف اللغة الإنجليزية كمصدر للتحديث. أظهرت الأبحاث الأخيرة (2026) أن هذا غالباً ما يكون خاطئاً.

> أكثرية المجموعات المعتمدة على اللغة الإنجليزية كصدر صغير. أحدث دراسة (2026) أظهرت أن هذا عادة ما يكون خطأ.

يتنبأ التشابه اللغوي بجودة النقل بشكل أفضل من حجم الجسم الخام. بالنسبة للأهداف السلافية، غالبًا ما يتغلب الألمانية أو الروسية على الإنجليزية. بالنسبة للأهداف الهندية، غالبًا ما تتغلب الهندية على الإنجليزية.**qWALS**مقياس التشابه (2026, على أساس ميزات اطلس العالمي لهياكل اللغة) يقدر هذا. **LANGRANK**(لين وآخرون، ACL 2019) هي طريقة منفصلة سابقة تصنف لغات المصدر المرشح من مزيج من التشابه اللغوي، وحجم الجسم، والترابط الوراثي.

> 语言相似性比原始语料大小更好地预测迁移质量──对于斯拉夫语目标,德语或俄语通常胜英语──对于印度语目标,印地语通常胜英语──**qWALS**مثل القدر الجنسية (٢٢٦) قد قام بتقييم هذا النقطة**LANGRANK**(Lin 等,ACL 2019) من اللغة التشابهية, واللغة الكبيرة والتربية

قاعدة عملية: إذا كانت لغتك المستهدفة لها قريبة من نوعها من ذوي الموارد العالية، حاول تحسين ذلك أولاً، ثم مقارنة مع اللغة الإنجليزية.

> قاعدة عملية: إذا كان لغتك المستهدفة قريبة من لغة ذات مصادر عالية، حاول أولاً التقييم على تلك اللغة، ثم مقارنة مع اللغة الإنجليزية.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
n5-crosslingual-bridge
```

## بناءها

### الخطوة الأولى: تصنيف متعدد اللغات

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

نموذج واحد، ثلاث لغات، نفس API. XLM-R تدرب على NLI نقل البيانات جيدا إلى التصنيف عن طريق خدعة التمسك.

> نموذج، ثلاث لغات، نفس API.

### الخطوة الثانية: مساحة إدراج متعددة اللغات

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

الترجمات تقع بالقرب من مساحة الإدخال. جملة إنجليزية مختلفة تقع أبعد. هذا ما يجعل الاستخدام عبر اللغات، والجمع، والشبه يعمل.

> 翻译在嵌入空间中距离很近. 不同英语句子距离更远. 翻译在嵌入空间中距离很近.

### الخطوة الثالثة: استراتيجية ضبط دقيقة

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

بالنسبة لـ 100-500 مثال لغة هدف، `num_train_epochs=5`و`learning_rate=2e-5`وتسبب معدل التعلم العالي في انهيار التوافق متعدد اللغات وتحصل على نموذج إنجليزي فقط.

> 对于100-500 个目标语言样本,`num_train_epochs=5`和 `learning_rate=2e-5`يمنح القيمة الراهنة. ارتفاع معدل التعلم يؤدي إلى انهيار اللغات المتعددة.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## تقييم يعمل فعلاً

- **Per-language accuracy on held-out sets.**ليس مجتمعاً، المجمّع يخفي الذيل الطويل
  **每种语言在留出集上的准确率。**لا تتجمع. تتجمع.
- **Benchmark against monolingual baseline.**بالنسبة للغات التي لديها بيانات كافية، نموذج واحد اللغات المدرب من الصفر أحيانا يفوق المتعدد اللغات. اختبار.
  **与单语基线比较。**بالنسبة للغات ذات بيانات كافية، فإن نموذج اللغة الواحدة من التدريبات في بعض الأحيان يفوز على نموذج اللغة المتعددة.
- **Entity-level tests.**الكيانات المسمى في اللغة المستهدفة. غالبا ما تكون النماذج متعددة اللغات لديها علامات ضعيفة للكتب البعيدة عن اللاتينية.
  **实体级测试。**目標語言中的命名实体──多语言模型对远离拉丁文的书写分词通常较弱──
- **Cross-lingual consistency.**نفس المعنى في لغتين يجب أن ينتج نفس التنبؤ. قياس الفجوة.
  **跨语言一致性。**两种语言相同含义应产生相同预测――测量差距――

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

## استخدمها في إطار التنفيذ

"مجموعة 2026"

> 2026 سنة التقنية:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

دائماً ميزانية للتحسين في لغة الهدف إذا كان الأداء مهماً. الصفر هو نقطة البداية وليس الإجابة النهائية.

> إذا كان الأداء مهمًا ، فهي دائماً ميزانية الحد الأدنى للغة المستهدفة.

### ضريبة التكنولوجيا

النماذج متعددة اللغات تشارك رمزًا واحدًا في جميع لغاتها. يتم تدريب هذه المفردات على مجموعة تهيمن عليها الإنجليزية والفرنسية والإسبانية والصينية والألمانية. بالنسبة لأي لغة خارج مجموعة المهيمنة، يتم تركيب ثلاثة ضرائب بصمت:

> تعتبر هذه اللغة تعليماً على المواد المستندة إلى اللغة الإنجليزية والفرنسية والإسبانية والصينية والألمانية.

- **Fertility tax.**يُعد نص لغة ذات موارد منخفضة رموزًا أكثر بكثير لكل كلمة من الإنجليزية. يمكن أن تحتاج جملة هندية إلى 3-5 مرات رموز جملة إنجليزية معادلة.
  **繁殖税。**低资源语言文本 每个词分词成比英语多很多的代币―― 一个印地语句子可能需要等价英语句子的3-5倍的代币――
- **Variant recovery tax.**كل خطأ في النص، والفراز الدياكريتي، أو عدم مطابقة تطبيق يونيكود، أو اختلاف الحالة يصبح تسلسلًا غير مرتبطًا بدءًا باردًا في مساحة التضمين.
  **变体恢复税。**كل خطأ في النص، تغيرات الصوت، تغيرات اليونيكود، تغيرات في التنسيق أو التنسيق في التنسيق في الفضاء البارد،
- **Capacity spillover tax.**الضرائب 1 و 2 تستهلك مواقف السياق، عمق الطبقة، وأبعاد التضمين. ما تبقى للبرأى الفعلي هو أصغر بشكل منهجي.
  **容量溢出税。**税 1 和 2 消耗 على الموقع التالي 层深度和嵌入维度── ترك إلى التفكير الفعلي النظامية 系统性地更小──

العرض العملي: نموذجك يتدرب عادة على الهندي، ويعتبر منحنى الخسارة صحيحا، ويعتبر تعقيد التقييم معقول، ونتائج الإنتاج خاطئة بشكل ظريف. **You cannot data-scale your way out of a broken tokenizer.**

> العلامات الحقيقية: النموذج يتدرب بشكل طبيعي على الهندية، ويكون التوترات محطمة بشكل صحيح، ويتم تقييم الارتباكات بشكل معقول، ولكن الإنتاج ينتج بشكلٍ خفيف.**你无法通过数据扩展来修复损坏的分词器。**

التخفيف: اختيار رمز مع تغطية جيدة لغتك المستهدفة؛ التحقق من خصوبة رمزية على النص المستهدف المحتفظ به؛ استخدام مستوى البايتات للخلفية للخطوط طويلة حقا.

> 缓解措施:选择对目标语言覆盖良好的分词器; 在留出的目标文本上验证分词繁殖率;对真正长尾书写使用字节级回退──

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/skill-multilingual-picker.md`:

> 保存为 `outputs/skill-multilingual-picker.md`:

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**قم بتشغيل خط الأنابيب التصنيفية الصفرة على 10 جمل لكل لغة عبر اللغة الإنجليزية والفرنسية والهندية والعربية.
   **简单。**في الإنجليزية والفرنسية والهندية والعربية، يتم تشغيل صفر نموذج من فئة التدفقات، في كل لغة 10 جملات.
2. **Medium.**استخدام`paraphrase-multilingual-MiniLM-L12-v2`لبناء جهاز استرداد متعدد اللغات على مجموعة صغيرة من اللغات المختلطة. استفسار باللغة الإنجليزية، استرداد المستندات في أي لغة. قياس recall@5.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量 recall@5──
3. **Hard.**مقارنة المصدر الإنجليزي ومصدر الهندي للتحسين لمهمة تصنيف الهندي. تقرير ما المصدر الذي ينتج دقة أفضل الهندي. هذا هو أطروحة LANGRANK في الصغر.
   **困难。**مقارنة المصادر الإنجليزية والهندية للتحليل على أثر المهام التقسيمية بالهندية.

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116)ورقة XLM-R. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) تحليل نقل اللغات المتعددة. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) ماجستير دراسات العلوم متعددة اللغات في كوهير.
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / qWALS / LANGRANK 源语言论文。
