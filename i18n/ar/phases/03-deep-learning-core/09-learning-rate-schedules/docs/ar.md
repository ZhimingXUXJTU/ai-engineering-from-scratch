# جدولات معدل التعلم والحرارة

> معدل التعلم هو المعيار الأكثر أهمية ليس الهندسة المعمارية ليس حجم مجموعة البيانات ليس وظيفة التفعيل معدل التعلم إذا لم تتنغم شيئا آخر، تنغم هذا

> **【中文解读】**معدل التعلم هو العيار الفائق الأهم  ليس البنية، ليس كمية البيانات، هو معدل التعلم  علامة 3 استخدام القيمة القصوى lr=3e-4 + 2000 步升温 + التدهور الكويسيني  GPT-3 استخدام lr=6e-4 + التدفئة‬‬ فهم معدل التعلم هو المفتاح لتدريب أي نموذج‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.06 (Optimizers), Lesson 03.08 (Weight Initialization)
**Time:** ~90 minutes

## أهداف التعلم

- تنفيذ جدولات ثابتة، تدريجية التدهور، التخفيف الكوسيني، التدفئة + الكوسيني، وتدريب معدل التعلم في دورة واحدة من الصفر
- إظهار أساليب الفشل الثلاثة لانتخاب معدل التعلم: الانحراف (على الدرجة العالية جدا) ، والتوقف (أقل جدا) ، والتذبذب (لا تدهور)
- شرح لماذا الحرارة ضرورية للمحسنين على أساس آدم وكيف أنها تستقر التدريب المبكر
- مقارنة سرعة التقارب بين كل المواعيد الخمسة في نفس المهمة واختيار المواعيد المناسبة لميزانية تدريب معينة

> **【中文解读】**هذا الفصل لتحقيق خمسة أنواع من معدل التعلم:恒定、阶梯衰减、余弦退火、warmup+余弦、1cycle 策略。

## المشكلة المشكلة المشكلة

حدد معدل التعلم إلى 0.1. التدريب يختلف -- الخسارة تقفز إلى لا نهاية لها في 3 خطوات. حدد إلى 0.0001. التدريب التزحلق -- بعد 100 عصر، النموذج بالكاد انتقل من العشوائية. حدد إلى 0.01. التدريب يعمل لمدة 50 عصر، ثم الخسارة تتذبذب حول الحد الأدنى الذي لا يمكن أن يصل إليه أبدا لأن الخطوات كبيرة جدا.

> سيتم تعيين معدل التعلم 0.1── التدريب انتشار  الخسارة في 3 مراحل قفز إلى لا نهاية لها── التدريب 0.0001── التدريب بطيء التزحلق 100  عصر  بعد ذلك، نموذج تقريباً لا يتحرك من حالة عشوائية── التدريب 0.01── التدريب قبل 50  عصر فعال، ثم الخسارة في التزاوج القريب من القيمة الحد الأدنى التي لا يمكن تحقيقها أبدًا، لأن التدريب كبير جدا ً──

معدل التعلم المثالي ليس ثابتًا. يتغير أثناء التدريب. في البداية ، تريد خطوات كبيرة لتغطية الأرض بسرعة. في وقت متأخر من التدريب ، تريد خطوات صغيرة لتستقر في الحد الأدنى الحاد. الفرق بين نموذج دقيق بنسبة 90% ونموذج دقيق بنسبة 95% هو غالبًا مجرد الجدول الزمني.

> لا يوجد أي معدل أفضل للتعلم. يتغير في عملية التدريب. في البداية، تريد التقدم الكبير بسرعة كبيرة. في مرحلة التدريب، تريد التقدم الصغير الاستقرار إلى حد أدنى من القيمة.

كل نموذج رئيسي نشرته في السنوات الثلاث الماضية يستخدم جدول معدل التعلم. استخدم Llama 3 ذروة lr = 3e-4 مع 2000 خطوة حرارة وتدهور كوسين إلى 3e-5. استخدم GPT-3 lr = 6e-4 مع حرارة أكثر من 375 مليون رمز. هذه ليست خيارات تعسفية. إنها نتيجة لمتساحات فرعية فائقة المدى التي تكلف ملايين الدولارات.

> 过去三年发表的每个主要模型都使用学习率调度──Llama 3 使用峰值 lr=3e-4,2000 步升和余弦衰减到3e-5──GPT-3 使用 lr=6e-4,warmup 覆盖3.75 مليار رمز──这些不是随意的选择──它们是花费数百万美元进行大量超参数搜索的结果──

يجب أن تفهم الجدول الزمني لأن الخطط الافتراضية لن تعمل لمشكلةك. عندما تقوم بتحسين نموذج متدرب مسبقًا، فإن الجدول الزمني الصحيح مختلف عن التدريب من الصفر. عندما تزيد حجم الحزمة، يجب أن يتغير فترة التدفئة. عندما تنتهي التدريب عند الخطوة 10,000، تحتاج إلى معرفة ما إذا كان ذلك مشكلة في الجدول الزمني أو شيء آخر.

> تحتاج إلى فهم خطة التنظيم، لأن القيمة الافتراضية لا تطبق على مشاكلك. عندما تقوم بتنظيم نموذج التدريب المسبق، فإن التنظيم الصحيح مختلف عن التدريب المباشر. عندما تزيد الكمية في الحجم، تحتاج إلى تغيير الفترة التدفئة.

> **【中文解读】**معدل التعلم مرتفع جدا → تعليمه ينفصل(الخسارة إلى لا يزال) ؛ منخفض جدا → تعليمه بطيء جدا؛ مناسبة ولكن لا يقلل → تذبذب بالقرب من القيمة الحد الأدنى. كل نموذج رئيسي لديه خطة تحديث معدل التعلم، وهذه الخطوات هي من خلال البحث عن العناصر الفائقة على مستوى مليون دولار.

> **【拓展：大模型的学习率配置】**علامة 3 405B: ذروة lr=3e-4, تساقط التدفئة = 2000 步, تساقط الكويسين حتى 3e-5, 训练 1.8T رمز。GPT-3 175B: ذروة lr=6e-4, تساقط التدفئة =375M رمز。BERT-base: ذروة lr=1e-4, تساقط=10K 步, تساقط خطي。规律:模型越大,学习率通常越小;预训练比微调的学习率高 10-100 倍。

## المفهوم الأساسي

### معدل التعلم المستمر

أسهل طريقة، إختار رقمًا واستخدمه في كل خطوة

> أسهل طريقة... إختار رقم، كل خطوة تستخدمها

```
lr(t) = lr_0
```

نادراً ما يكون مثاليًا. إما أنه مرتفع جدًا في نهاية التدريب (التذبذب حول الحد الأدنى) أو منخفض جدًا في البداية (حساب مضيعة على خطوات صغيرة). يعمل بشكل جيد للنماذج الصغيرة وإعداد التحليلات. خيار رهيب لأي شيء يتدرب لأكثر من ساعة.

> 很少是最优的──要么对训练末期来说太高 ((在极小值附近振荡) ),要么对训练初步来说太低 ((微小步长浪费计算) ──适用小模型和调试──对于训练超过一小时的任务来说是糟糕的选择──

### خطوة التراجع

النهج القديم من عصر ريسنت: خفض معدل التعلم بمقدار عامل (عادةً 10x) في حقول ثابتة.

> في عصر معين، سوف يقلل معدل التعلم عن عامل واحد (عادة 10 مرات)

```
lr(t) = lr_0 * gamma^(floor(epoch / step_size))
```

حيث غاما = 0.1 و step_size = 30 يعني: lr ينخفض 10x كل 30 عصر.

> غاما = 0.1 且 step_size = 30 يعني: في كل 30 年代 學習率降低 10 倍──ResNet-50 استخدم هذا lr=0.1, في دور 30、60 و 90 تم تقليصها 10 倍──

المشكلة: نقاط التدهور المثلى تعتمد على مجموعة البيانات والهندسة المعمارية. الانتقال إلى مشكلة مختلفة و تحتاج إلى إعادة ضبط متى تنخفض. الانتقالات مفاجئة - يمكن أن يرتفع الخسارة عندما يتغير المعدل فجأة.

> 问题:最优衰减点取决于数据集和架构. 另一个问题就需要重新调整何时降低. 转度是突然的学习率突然改变时损失可能升.

### كوسين انيلينغ

التراجع السلس من معدل التعلم القصوى إلى الحد الأدنى، وذلك بعد منحنى الكوسين:

> من أكبر معدل التعلم إلى أقل معدل التعلم من التراجع السطحي، اتبع خطة الزيادة:

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * t / T))
```

حيث t هو الخطوة الحالية و T هو العدد الإجمالي للخطوات.

> من بينها t هو عدد الخطوات الحالية,T هو عدد الخطوات الإجمالية.

عند t=0، يكون مصطلح الكوسين 1، لذا lr = lr_max. عند t=T، يكون مصطلح الكوسين -1, لذا lr = lr_min. يكون التهالك لطيفا في البداية، ويتسارع في الوسط، ويصبح لطيفا مرة أخرى بالقرب من النهاية.

> t=0 时,余弦项为1,所以 lr = lr_max──t=T 时,余弦项为 -1,所以 lr = lr_min──衰减开始平缓,中间加速,末期又变平缓──

هذا هو الافتراض الافتراضي لمعظم عمليات التدريب الحديثة. لا توجد مفاصيل فائقة للتنسيق خارج lr_max و lr_min. شكل الكوزين يطابق الملاحظة التجريبية التي تحدث معظم التعلم في منتصف التدريب -- تريد أحجام خطوات معقولة خلال تلك الفترة الحرجة.

> هذا هو الاختيار المتبقي في معظم التدريبات الحديثة. باستثناء lr_max و lr_min، لا حاجة إلى تعديل الوصف العالي.

### لماذا تبدأ من الصغر ؟ لماذا تبدأ من معدل التعلم الصغير ؟

يحتفظ آدم وغيره من المحفسين التكيفيين بتقديرات تشغيلية لمتوسط التدرج والتباعد. في الخطوة 0 ، يتم تشغيل هذه التقديرات إلى الصفر. تستند التحديثات القليلة الأولى للتدرج إلى إحصاءات القمامة. إذا كان معدل التعلم كبير خلال هذه الفترة ، فإن النموذج يتخذ خطوات ضخمة ، غير موجهة بشكل سيء.

> أدم وآخرين من أجهزة تحسين التكيف على الذات تعزيز متوسط قيمة وفرق التشغيل. في الخطوة 0، تم إطلاق هذه التقديرات إلى صفر.

يصلح Warmup هذا. تبدأ مع معدل التعلم الصغير (غالباً ما lr_max / warmup_steps أو حتى صفر) وتسلق خطياً إلى lr_max على مدار الخطوات الأولى N. بحلول الوقت الذي تصل فيه إلى معدل التعلم الكامل ، فإن إحصاءات آدم قد استقرت.

> الحرارة صلح هذه المشكلة  بدء من معدل التعلم صغير جدا  عادةً يكون lr_max / حرارة_خطوات حتى صفر) ، ثم في المرحلة الأولى  ارتفاع إلى lr_max  عند بلوغ معدل التعلم الكامل، فإن إحصائيات آدم قد استقر 

```
lr(t) = lr_max * (t / warmup_steps)     for t < warmup_steps
```

التدفئة النموذجية: 1-5% من إجمالي مراحل التدريب. تدرب Llama 3 على حوالي 1.8 تريليون رمز وتدفأ على 2000 خطوة. GPT-3 حرارة أكثر من 375 مليون رمز.

> **【拓展：Warmup 的数学解释】**تعديل التفاوت في آدم (m_hat = m_t / (1-beta1^t)) في الأيام الأولى تعويضات لا يصل إلى 0.9 بـ مثال، في المرحلة الأولى من m_1 = 0.1* درجة، وذلك بفضل (1-0.9) = 0.1 الحصول على تقديرات التدريجية الصحيحة. ولكن في الأيام الأخيرة، تفرق التقديرات في التفاوت.

### التدفئة الخطية + التدهور الكوني  التدفئة الخطية +

الوضع الاصطناعي الحديث، يرتفع خطياً ثم يتحلل مع الكوسين:

```
if t < warmup_steps:
    lr(t) = lr_max * (t / warmup_steps)
else:
    progress = (t - warmup_steps) / (total_steps - warmup_steps)
    lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * progress))
```

هذا ما يستخدمه لاما، GPT، PaLM، ومعظم المحولات الحديثة. الحرارة تمنع عدم الاستقرار المبكر. تدهور الكوسين يضع النموذج إلى الحد الأدنى.

> هذا هو Llama、GPT、PaLM 和大多数现代 Transformer 使用的方法──warmup 防止早期不稳定──余弦衰减使模型稳定到一个好的极小值──

### سياسة دورة واحدة

اكتشاف ليزلي سميث (2018): زيادة معدل التعلم من قيمة منخفضة إلى قيمة عالية في النصف الأول من التدريب، ثم زيادة ذلك مرة أخرى في النصف الثاني.

> اكتشاف ليزلي سميث (2018): في النصف الأول من التدريب سوف ترتفع معدلات التعلم من القيمة المنخفضة إلى القيمة العالية، والنصف الثاني سوف ينخفض مرة أخرى.

النظرية: ارتفاع معدل التعلم يعمل كتنظيم من خلال إضافة الضوضاء إلى مسار التحسين. يستكشف النموذج المزيد من المشهد الخساري خلال مرحلة الإرتفاع ، ويحصل على أحواض أفضل. ثم تتطور مرحلة الإرتفاع في أفضل الحوض الموجود.

> النظرية: ارتفاع معدل التعلم من خلال إعطاء مسارات تحسين إضافة الضوضاء يصل إلى تأثير تحسين الصوت.

```
Phase 1 (0 to T/2):    lr ramps from lr_max/25 to lr_max
Phase 2 (T/2 to T):    lr ramps from lr_max to lr_max/10000
```

1 دورة غالبا ما تتدرب أسرع من التدريب على الكوسين لحدد حساب ثابت.

> 1- دورة في الحساب الثابتة تحت الميزانية عادة أكثر سرعة من التدريب على عودة الحبل.

> **【拓展：微调时的学习率策略】**微调预训练模型(如BERT、Llama) 时,学习率通常比预训小 10-100 倍。LoRA 微调 Llama:lr=2e-5~1e-4,warmup=总步数的3%,cosine decay。关键技巧:对不同层使用不同学习率底层(接近输入) 用更小的 lr(因为通用特征已经学好),顶层(接近输出) 用更大的 lr因为需要适应新任务)。PyTorch 通过参数组实现──

### الموعد الأشكال 调度形状对比

```mermaid
graph LR
    subgraph "Constant"
        C1["lr"] --- C2["lr"] --- C3["lr"]
    end

    subgraph "Step Decay"
        S1["0.1"] --- S2["0.1"] --- S3["0.01"] --- S4["0.001"]
    end

    subgraph "Cosine Annealing"
        CS1["lr_max"] --> CS2["gradual"] --> CS3["steep"] --> CS4["lr_min"]
    end

    subgraph "Warmup + Cosine"
        WC1["0"] --> WC2["lr_max"] --> WC3["cosine"] --> WC4["lr_min"]
    end
```

### خريطة تدفق القرارات خريطة عملية القرارات

```mermaid
flowchart TD
    Start["Choosing a LR schedule"] --> Know{"Know total<br/>training steps?"}

    Know -->|"Yes"| Budget{"Compute budget?"}
    Know -->|"No"| Constant["Use constant LR<br/>with manual decay"]

    Budget -->|"Large (days/weeks)"| WarmCos["Warmup + Cosine Decay<br/>(Llama/GPT default)"]
    Budget -->|"Small (hours)"| OneCycle["1cycle Policy<br/>(fastest convergence)"]
    Budget -->|"Moderate"| Cosine["Cosine Annealing<br/>(safe default)"]

    WarmCos --> Warmup["Warmup = 1-5% of steps"]
    OneCycle --> FindLR["Find lr_max with LR range test"]
    Cosine --> MinLR["Set lr_min = lr_max / 10"]
```

### أرقام حقيقية من النماذج المنشورة

```mermaid
graph TD
    subgraph "Published LR Configs"
        L3["Llama 3 (405B)<br/>Peak: 3e-4<br/>Warmup: 2000 steps<br/>Schedule: Cosine to 3e-5"]
        G3["GPT-3 (175B)<br/>Peak: 6e-4<br/>Warmup: 375M tokens<br/>Schedule: Cosine to 0"]
        R50["ResNet-50<br/>Peak: 0.1<br/>Warmup: none<br/>Schedule: Step decay x0.1 at 30,60,90"]
        B["BERT (340M)<br/>Peak: 1e-4<br/>Warmup: 10K steps<br/>Schedule: Linear decay"]
    end
```

## بناء ذلك تحرك لتحقيق
```figure
lr-schedule
```

## بناءها

> **【中文解读】**أدناه من صفر تنفيذ خمس استراتيجيات التنظيم، ثم استخدام نفس الدائرة شبكة تدريب المجموعات البيانات مقابل النتائج.

### الخطوة الأولى: جدولة الوظائف الخطوة الأولى: تعديل الوظائف

كل وظيفة تأخذ الخطوة الحالية وتعيد معدل التعلم في تلك الخطوة.

> كل وظيفة تتلقى عدد الخطوات الحالية، وتعود إلى معدل تعلم هذه الخطوات.

```python
import math


def constant_schedule(step, lr=0.01, **kwargs):
    return lr


def step_decay_schedule(step, lr=0.1, step_size=100, gamma=0.1, **kwargs):
    return lr * (gamma ** (step // step_size))


def cosine_schedule(step, lr=0.01, total_steps=1000, lr_min=1e-5, **kwargs):
    if step >= total_steps:
        return lr_min
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * step / total_steps))


def warmup_cosine_schedule(step, lr=0.01, total_steps=1000, warmup_steps=100, lr_min=1e-5, **kwargs):
    if total_steps <= warmup_steps:
        return lr * (step / max(warmup_steps, 1))
    if step < warmup_steps:
        return lr * step / warmup_steps
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * progress))


def one_cycle_schedule(step, lr=0.01, total_steps=1000, **kwargs):
    mid = max(total_steps // 2, 1)
    if step < mid:
        return (lr / 25) + (lr - lr / 25) * step / mid
    else:
        progress = (step - mid) / max(total_steps - mid, 1)
        return lr * (1 - progress) + (lr / 10000) * progress
```

### الخطوة الثانية: تظهر جميع الجدول الزمنية الخطوة الثانية: تظهر جميع التنظيمات

طبع خطة بناء على نص يظهر كيف يتطور كل جدول خلال التدريب.

> طباعة رسومات المقال، تظهر كل نوع من التغييرات في عملية التدريب

```python
def visualize_schedule(name, schedule_fn, total_steps=500, **kwargs):
    steps = list(range(0, total_steps, total_steps // 20))
    if total_steps - 1 not in steps:
        steps.append(total_steps - 1)

    lrs = [schedule_fn(s, total_steps=total_steps, **kwargs) for s in steps]
    max_lr = max(lrs) if max(lrs) > 0 else 1.0

    print(f"\n{name}:")
    for s, lr_val in zip(steps, lrs):
        bar_len = int(lr_val / max_lr * 40)
        bar = "#" * bar_len
        print(f"  Step {s:4d}: lr={lr_val:.6f} {bar}")
```

### الخطوة الثالثة: شبكة التدريب

شبكة بسيطة من طبقتين على مجموعة بيانات الدورة، نفس الدروس السابقة، ولكن الآن نحن نغير الجدول الزمني.

> في مجموعة بيانات دائرية، شبكة بسيطة ذات طبقتين، نفس المرحلة السابقة، ولكن الآن نحن نغير المخططات.

```python
import random


def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def relu(x):
    return max(0.0, x)


def relu_deriv(x):
    return 1.0 if x > 0 else 0.0


def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


def train_with_schedule(schedule_fn, schedule_name, data, epochs=300, base_lr=0.05, **kwargs):
    random.seed(0)
    hidden_size = 8
    total_steps = epochs * len(data)

    std = math.sqrt(2.0 / 2)
    w1 = [[random.gauss(0, std) for _ in range(2)] for _ in range(hidden_size)]
    b1 = [0.0] * hidden_size
    w2 = [random.gauss(0, std) for _ in range(hidden_size)]
    b2 = 0.0

    step = 0
    epoch_losses = []

    for epoch in range(epochs):
        total_loss = 0
        correct = 0

        for x, target in data:
            lr = schedule_fn(step, lr=base_lr, total_steps=total_steps, **kwargs)

            z1 = []
            h = []
            for i in range(hidden_size):
                z = w1[i][0] * x[0] + w1[i][1] * x[1] + b1[i]
                z1.append(z)
                h.append(relu(z))

            z2 = sum(w2[i] * h[i] for i in range(hidden_size)) + b2
            out = sigmoid(z2)

            error = out - target
            d_out = error * out * (1 - out)

            for i in range(hidden_size):
                d_h = d_out * w2[i] * relu_deriv(z1[i])
                w2[i] -= lr * d_out * h[i]
                for j in range(2):
                    w1[i][j] -= lr * d_h * x[j]
                b1[i] -= lr * d_h
            b2 -= lr * d_out

            total_loss += (out - target) ** 2
            if (out >= 0.5) == (target >= 0.5):
                correct += 1
            step += 1

        avg_loss = total_loss / len(data)
        accuracy = correct / len(data) * 100
        epoch_losses.append(avg_loss)

    return epoch_losses
```

### الخطوة الرابعة: مقارنة جميع الجدول الزمنية

قم بتدريب نفس الشبكة مع كل جدول و قم بتقارن الخسارة النهائية و سلوك التقارب.

> باستخدام كل تدريبات التنظيم على نفس الشبكة، مقارنة الخسائر النهائية والحصول على السلوك.

```python
def compare_schedules(data):
    configs = [
        ("Constant", constant_schedule, {}),
        ("Step Decay", step_decay_schedule, {"step_size": 15000, "gamma": 0.1}),
        ("Cosine", cosine_schedule, {"lr_min": 1e-5}),
        ("Warmup+Cosine", warmup_cosine_schedule, {"warmup_steps": 3000, "lr_min": 1e-5}),
        ("1cycle", one_cycle_schedule, {}),
    ]

    print(f"\n{'Schedule':<20} {'Start Loss':>12} {'Mid Loss':>12} {'End Loss':>12} {'Best Loss':>12}")
    print("-" * 70)

    for name, schedule_fn, extra_kwargs in configs:
        losses = train_with_schedule(schedule_fn, name, data, epochs=300, base_lr=0.05, **extra_kwargs)
        mid_idx = len(losses) // 2
        best = min(losses)
        print(f"{name:<20} {losses[0]:>12.6f} {losses[mid_idx]:>12.6f} {losses[-1]:>12.6f} {best:>12.6f}")
```

### الخطوة 5: LR مرتفعة جدا مقابل منخفضة جدا . الخطوة الخامسة: معدل التعلم مرتفعة جدا مقابل منخفض جدا

أظهر ثلاثة أوضاع الفشل: عالية جدا (التباين) ، منخفضة جدا (الزحف) ، والصواب.

> 展示三种失败模式: 太高(发散) 太低(爬行) 刚好。

```python
def lr_sensitivity(data):
    learning_rates = [1.0, 0.1, 0.01, 0.001, 0.0001]

    print("\nLR Sensitivity (constant schedule, 100 epochs):")
    print(f"  {'LR':>10} {'Start Loss':>12} {'End Loss':>12} {'Status':>15}")
    print("  " + "-" * 52)

    for lr in learning_rates:
        losses = train_with_schedule(constant_schedule, f"lr={lr}", data, epochs=100, base_lr=lr)
        start = losses[0]
        end = losses[-1]

        if end > start or math.isnan(end) or end > 1.0:
            status = "DIVERGED"
        elif end > start * 0.9:
            status = "BARELY MOVED"
        elif end < 0.15:
            status = "CONVERGED"
        else:
            status = "LEARNING"

        end_str = f"{end:.6f}" if not math.isnan(end) else "NaN"
        print(f"  {lr:>10.4f} {start:>12.6f} {end_str:>12} {status:>15}")
```

## استخدمها في إطار التنفيذ

> **【中文解读】**بيتورش  تقدم 15+ نوع من المعدات. الأكثر استخداما هو كوسينAnnealingLR 和 HuggingFace من get_cosine_schedule_with_warmup.

تقدم شركة PyTorch المخططات في `torch.optim.lr_scheduler`:

```python
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR, StepLR

model = nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 1))
optimizer = optim.Adam(model.parameters(), lr=3e-4)

scheduler = CosineAnnealingLR(optimizer, T_max=1000, eta_min=1e-5)

for step in range(1000):
    loss = train_step(model, optimizer)
    scheduler.step()
```

لتحسين التدفئة + التدفق، استخدم جهاز تخطيط لامپدا أو `get_cosine_schedule_with_warmup`من " HuggingFace "

> لتحسين الدوام، استخدام lambda 调度器 أو HuggingFace `get_cosine_schedule_with_warmup`:

```python
from transformers import get_cosine_schedule_with_warmup

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=2000,
    num_training_steps=100000,
)
```

وظيفة HuggingFace هي ما تستخدمه معظم نصوص التنسيق الدقيق للاما و GPT. عندما تكون في شك، استخدم التدفئة + كوسين مع التدفئة = 3-5% من إجمالي الخطوات. يعمل على كل شيء تقريبًا.

> وظيفة HuggingFace هي معظم Llama 和 GPT 微调脚本使用的──不确定时,使用暖化 +余弦,暖化为总步数的 3-5%──它几乎适用于所有场景──

## أرسلها .

هذا الدرس ينتج عن:
- `outputs/prompt-lr-schedule-advisor.md`-- طلب يوصي بتوقيت معدل التعلم المناسب وبرامج فائقة لترتيب التدريب الخاص بك

> 本课产出:`outputs/prompt-lr-schedule-advisor.md`- توصية صحيحة لتعلم معدل التنظيم والتحديد

## تمارين التدريب

1. تنفيذ التدهور المرتفع: lr(t) = lr_0 * غاما^t حيث غاما = 0.999. مقارنة مع التخفيف الكوسين على مجموعة البيانات الدائرة.

   1. 实现指数衰减:lr(t) = lr_0 * غاما^t, غاما = 0.999。在圆形数据集上和余弦退火对比──

2. تنفيذ اختبار نطاق معدل التعلم (ليسي سميث): تدريب لعدة مئات من الخطوات مع زيادة نمطية لـ LR من 1e-7 إلى 1. خسارة اللقطة مقابل LR.

   2. 实现学习率范围测试(Leslie Smith): تدريب بضعة مئات الخطوة، في نفس الوقت قم بزيادة LR من 1e-7 إعداد إلى 1── رسم الخسارة مقابل LR 曲线──最优最大 LR 是 الخسارة 开始上升前的值──

3. تدريب مع التدفئة + كوسين ولكن تغير طول التدفئة: 0٪، 1٪، 5٪، 10٪، 20٪ من إجمالي الخطوات. العثور على نقطة الحلوة حيث التدريب أكثر استقرارا.

   3. مع التدريب على التدفئة + التدريب على الصفوف ، ولكن التغيرات التدريب على التدفئة 长度:总步数的0%、1%、5%、10%、20%──找到训练最稳定的最佳点──

4. تنفيذ التمرد الكوسيني مع إعادة تشغيل دافئ (SGDR): إعادة تعيين معدل التعلم إلى lr_max كل خطوة T وتحلل مرة أخرى. مقارنة مع الكوسيني القياسي على دور تدريب أطول.

   4. 实现带热重启的余弦退火(SGDR): في كل خطوة تعيد تعديل معدل التعلم إلى lr_max 并再次衰减──在更长的训练上和标准余弦对比──

5. بناء "جراح جدول" الذي يراقب فقدان التدريب ويتحول تلقائيا من التدفئة إلى السينوم عندما يتحسن الخسارة، ويقلل من العدالة إذا كانت الخسارة مرتفعة لفترة طويلة جدا.

   5. 构建"调度医生": مراقبة تدريب الخسارة، الخسارة 稳定时自动从加热 转换到余弦,损失 停滞太久时降低 lr。

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Learning rate | "How fast the model learns" | The scalar that multiplies the gradient to determine the parameter update size |
| Schedule | "Change the LR over time" | A function that maps training step to learning rate, designed to optimize convergence |
| Warmup | "Start with a small LR" | Linearly ramping the LR from near-zero to the target value over the first N steps to stabilize optimizer statistics |
| Cosine annealing | "Smooth LR decay" | Decreasing the LR following a cosine curve from lr_max to lr_min over training |
| Step decay | "Drop LR at milestones" | Multiplying the LR by a factor (usually 0.1) at fixed epoch intervals |
| 1cycle policy | "Up then down" | Leslie Smith's method of ramping LR up then down in a single cycle for faster convergence |
| LR range test | "Find the best learning rate" | Training briefly while increasing LR to find the value where loss starts diverging |
| Cosine with warm restarts | "Reset and repeat" | Periodically resetting the LR to lr_max and decaying again (SGDR) |
| Eta min | "The floor for the LR" | The minimum learning rate that the schedule decays to |
| Peak learning rate | "The maximum LR" | The highest LR reached during training, typically after warmup |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| Learning rate / 学习率 | "模型学得多快" | 乘以梯度决定参数更新大小的标量 |
| Schedule / 调度 | "随时间变 LR" | 把训练步数映射到学习率的函数，旨在优化收敛 |
| Warmup / 预热 | "从小 LR 开始" | 在前 N 步把 LR 从近零线性升到目标值，稳定优化器统计 |
| Cosine annealing / 余弦退火 | "平滑 LR 衰减" | 训练中按余弦曲线从 lr_max 降到 lr_min |
| Step decay / 阶梯衰减 | "里程碑式降 LR" | 在固定 epoch 间隔把 LR 乘以一个因子（通常 0.1） |
| 1cycle policy / 1cycle 策略 | "先升后降" | Leslie Smith 的方法：单周期内先升 LR 后降，加速收敛 |
| LR range test / LR 范围测试 | "找最佳学习率" | 短训练中增加 LR，找到 loss 开始发散的点 |
| Cosine with warm restarts / 带热重启的余弦 | "重置并重复" | 周期性把 LR 重置为 lr_max 再次衰减（SGDR） |
| Eta min / 最小学习率 | "LR 的下限" | 调度衰减到的最小学习率 |
| Peak learning rate / 峰值学习率 | "最大 LR" | 训练期间达到的最高 LR，通常在 warmup 之后 |

## المزيد من القراءة

- لوششيلوف وهاتر، "SGDR: التنزل المستقيم مع إعادة البدء الحار" (2017) -- أدخل التنقل الكوسيني وإعادة البدء الحار
  لوششيلوف و هاتر،SGDR:带热重启的随机梯度下降(2017)引入余弦退火和热重启
- سميث، "التحول الخارق: تدريب سريع جدا للشبكات العصبية باستخدام معدلات التعلم الكبيرة" (2018) -- ورقة السياسة الدورة الأولى
  سميث,超收: استخدام الجامعة 习率快速训练神经网络(2018)1周期 策略论文
- توفرون وغيره، "لاما 2: أساس مفتوح ونماذج الدردشة المنسقة" (2023) -- توثيق جدول التدفئة + الجدول المستخدم على نطاق واسع
  توفرون 等人,لاما 2: مفتوحة الأساس و التغييرات التفاصيل النموذج(2023) سجلت استخدام واسع النطاق للتدفئة + 余弦调度
- Goyal et al., "دقيق، مجموعة صغيرة SGD: تدريب ImageNet في ساعة واحدة" (2017) -- قاعدة التوسع الخطوي والحرارة للتدريب على مجموعات كبيرة
  غويال 等人,精确大批量 SGD:1 小时训练 ImageNet(2017) 线性缩放规则和大批量训练的热升
