# محفزات

> التراجع التدريجي يخبرك في أي اتجاه تتحرك لا يخبرك بأي مسافة أو سرعة

> **【中文解读】**梯度下降告诉你方向,但不说步幅和速度──SGD 像指南针只知道方向──亚当 像带实时路况的GPS根据历史信息调整策略──本章从零实现 SGD → 动力 →亚当 →亚当W,理解每一步优化直觉──

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.05 (Loss Functions)
**Time:** ~75 minutes

## أهداف التعلم

- تنفيذ SGD، SGD مع الزخم، آدم، وأدمW المتحفسين من الصفر في بيثون
- شرح كيف تعويض تصحيح التحيز آدم للتقديرات الصفر المبدئية لحظات في مراحل التدريب المبكرة
- إظهار لماذا AdamW تنتج التعميم أفضل من آدم مع تنظيم L2 في نفس المهمة
- حدد المحفزات المناسبة والمعايير المضطربة الافتراضية للمتحولات والسي إن إن، والإضفاءات النطاقية، والتحسينات الدقيقة

## المشكلة المشكلة المشكلة

لقد حاسبت المرافق. تعرف أن الوزن # 4,721 يجب أن تنخفض 0.003 لتقليل الخسارة. ولكن 0.003 في أي وحدات؟ مقياساً بماذا؟ و يجب أن تحرك نفس الكمية على الخطوة 1 كما على الخطوة 1000؟

> أنت حاسبت التدابير. هل تعلم أن الوزن يجب أن يقلل 0.003 لتقليل الخسارة. ولكن 0.003 هي ما هي الوحدة؟

تنخفض نسبة التعلم الفانيليا نفس معدل التعلم لكل معايير في كل خطوة: w = w - lr * نسبة التدفق. هذا يخلق ثلاثة مشاكل تجعل تدريب شبكات العصبية مؤلمة في الممارسة.

> انخفاض الدرجة الأولية في كل خطوة على كل عنصر تطبيق نفس معدل التعلم: w = w - lr * تراجيعها.

أولاً، التذبذب. لا يُظهر المشهد المُضايق بشكل شائع كوعة سلسة إنه أكثر مثل وادي طويل و ضيق يُحدد التراجع عبر الوادي (الجهة الرطبة) وليس على طوله (الجهة الرطبة). إنخفاض التدريجي يقلع ذهاباً وإياباً عبر الأبعاد الضيقة بينما يتقدم تقدماً صغيراً على طول الأبعاد المفيدة. لقد رأيتم هذا: الخسارة تنخفض بسرعة بعد مرتفعات، ليس لأن النموذج يتقارب ولكن لأنه يتذبذب.

> أولاً، التزاوج. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

ثانياً، إن معدل واحد للتعلم لجميع المعلمات خاطئ. بعض الأوزان تحتاج إلى تحديثات كبيرة (إنها في مرحلة مبكرة، غير مناسبة). آخرون بحاجة إلى تحديثات صغيرة (إنها قريبة من قيمتها المثلى). معدل التعلم الذي يعمل للقاعدة يدمر الأخيرة، وعكس ذلك.

> ثانيا، جميع العناصر المشتركة معدل التعلم هو خطأ. بعض الجهود تحتاج إلى تحديث كبير.

ثالثاً، نقاط القعد. في الأبعاد العالية، فإنّ المشهد المضاد لديه مناطق مسطحة واسعة حيث يكون التنحيل قريبًا من الصفر. الجدول المضاد المضاد المزدوج يزحف عبر هذه المناطق بسرعة التنحيل، والتي هي في الواقع صفر. يبدو أن النموذج عالق.

> في الارتفاع، يوجد على سطح المياه المزدوجة قطعة كبيرة من المنطقة السطحية، والتي يصل التدريج إلى الصفر.

(آدم) يحل كلّ الثلاثة يحافظ على متوسطين متجاريين لكل مبرمج - المتوسط (الحركة، يتعامل مع التذبذب) و المتوسط المربع (المعدل التكيفي، يتعامل مع المقاييس المختلفة). يجمع مع تصحيح التحيز للخطوات القليلة الأولى، فإنه يعطيك تحسين واحد يعمل على 80% من المشاكل مع المعلمات المفرطة الافتراضية. هذا الدروس يبنيها من الصفر حتى تفهم بالضبط متى ولماذا يفشل في الـ 20% الآخرين

> آدم  حل كل ثلاثة مشاكل. انه يحافظ على كل عنصر اثنين من التشغيل متوسط القيمة  متوسط القيمة درجة ((حركة، معالجة التزاوج) و متوسط درجة ((سرعة التكيف، معالجة مختلفة الحجم)  جنبا إلى جنب مع التحديثات الاختلافية من الخطوات السابقة، فإنه يوفر تحسين واحد، تطبق تحت الاختلافات الاختيارية فوق العنصر 80٪.

> **【中文解读】**المشكلة الأولى في مجال التعلم: التزاوج (التزاوج) ، وتعدد التعلم (التعلم) ، لا يناسب جميع العناصر (التعلم) ، لا يمكن عبور المنطقة المُسطحة (التدفق) ، وتعدد قريب من الصفر (التزاوج) ، والتي تُحلل في نفس الوقت.

## المفهوم الأساسي

### التراجع التدريجي السطوالي (SGD) 随机梯度下降

أسهل محفز، احسب التراجع على مجموعة صغيرة وخطوة في الاتجاه المعاكس

> أسهل أدوات تحسينات:

```
w = w - lr * gradient    # 最简单的参数更新公式
```

"الستوكاستيك" يعني أنك تستخدم مجموعة فرعية عشوائية (ميني-بارت) من البيانات لتقدير التدفق، بدلا من مجموعة البيانات الكاملة. هذا الضجيج مفيد في الواقع -- يساعد على التخلص من الحد الأدنى المحلي الحاد. ولكن الضجيج يسبب أيضا التذبذب.

> "توقيت" يعني أنك تستخدم مجموعة صغيرة من البيانات لتقييم التدرج ، وليس مجموعة البيانات بأكملها. هذا الضجيج مفيد في الواقع. يساعد على الهروب من الحد الأدنى من القيمة المحلية للقمة. ولكن الضجيج يؤدي أيضًا إلى التذبذب.

معدل التعلم هو الزر الوحيد. مرتفع جداً: تختلف الخسائر. منخفض جداً: يستغرق التدريب إلى الأبد. يعتمد القيمة المثلى على الهندسة المعمارية والبيانات وحجم الحزمة والمرحلة الحالية للتدريب. بالنسبة لـ SGD الفانيليا على الشبكات الحديثة، تتراوح القيم النموذجية من 0.01 إلى 0.1. ولكن حتى في غضون جولة تدريب واحدة، يتغير معدل التعلم المثالي.

> تعتمد نسبة التعلم على المرحلة الحالية من التدريب. بالنسبة للدراسة الجوية الأصلية على شبكة الويب الحديثة، فإن المرحلة النموذجية تتراوح بين 0.01 إلى 0.1 . ولكن حتى في عملية التدريب الفردي، يتغير نسبة التعلم المثالي أيضًا.

### -تيرة -حركة

تشبيه التدفقات المستخدمة بشكل مفرط ولكنها دقيقة، بدلاً من الدخول عبر التدفق وحده، تحافظ على سرعة تتراكم عبر التدفقات.

> تم استخدام المثابة على المرجع فوق المعدل ولكن هذا صحيح جدا.

```
m_t = beta * m_{t-1} + gradient    # 速度 = 衰减 × 历史速度 + 当前梯度
w = w - lr * m_t                    # 沿速度方向更新
```

يتحكم التاريخ في التاريخ (عادة 0.9) ، مع التاريخ التاريخي = 0.9 ، فإن الزخم هو متوسط آخر 10 تراجعات (1 / (1 - 0.9) = 10).

> في حالة البيتا (بيتا) ، فإن الحد الأوسط هو 10 درجات قريباً.

لماذا هذا يصلح التذبذب: تراكم التدرج الذي يشير في نفس الاتجاه. تتباطأ التدرج التي تغير الاتجاه. في ذلك الوادي الضيق، يتحول المكون "العكس" كل خطوة ويصبح ضباب. يبقى المكون "على طول" متسقًا ويصبح مضخمًا. النتيجة تسريع سلس في الاتجاه المفيد.

> لماذا يمكن أن يعاد التذبذب: يُشير إلى تراجعات تتراكم في نفس الاتجاه.

الأرقام الحقيقية: قد يستغرق SGD وحده على مشهد الخسائر السيئة 10,000 خطوة. SGD مع الزخم (بيتا = 0.9) عادة ما يستغرق 3,000-5,000 خطوة على نفس المشكلة. السرعة ليست هامشية.

> 具体数字: في ظل الظروف المتباينة، قد يتطلب SGD وحيد 10,000 قدم. 带动量(beta=0.9) SGD في نفس المشكلة عادة ما تتطلب 3,000-5,000 قدم.

> **【拓展：SGD + Momentum 的 resurgence】**على الرغم من أن آدم هو اختيار متضمن، ولكن مقال عام 2023 يظهر SGD+مومنتوم في مهمة محددة لا تزال لديها ميزات.

### "إنه لن يصل إلى الجذر"

أول طريقة لعدد التعلم التكيفي لكل مبرمير عملت فعلاً. اقترحها هينتون في محاضرة في كورسيرا (لم يتم نشرها رسمياً قط).

> أول طريقة فعالة حقاً لتحديد معدل التعلم.

```
s_t = beta * s_{t-1} + (1 - beta) * gradient^2
w = w - lr * gradient / (sqrt(s_t) + epsilon)
```

تتبع s_t المتوسط الجاري للمرافق المربعة. يتم تقسيم المعايير ذات المرافق الكبيرة باستمرار بأعداد كبيرة (متوسط التعلم الفعلي الأصغر). يتم تقسيم المعايير ذات المرافق الصغيرة بأعداد صغيرة (متوسط التعلم الفعلي الأكبر).

> s_t  تتبع متوسط عمليات درجة التربيعية.

هذا يحل مشكلة "متوسط واحد للتعلم لجميع المعلمات". الوزن الذي يحصل بالفعل على تحديثات كبيرة هو على الأرجح قريب من هدفه -- يبطئ. الوزن الذي يحصل على تحديثات صغيرة قد يكون دون تدريب -- تسريع.

> هذا يحل مشكلة "جميع العناصر تتشارك في معدل واحد للتعلم"― واحد قد حصل على وزن كبير من التحديث قد يقترب من الهدف بطءاً  واحد فقط قد يحصل على وزن صغير من التحديث قد يفتقر إلى التدريب تسرع

يمنع إيبسيلون (عادة 1e-8) من الانقسام بالصفر عندما لم يتم تحديث أحد المعلمات.

> إيبسيلون ((عادة 1e-8) منع العنصر غير تم تحديثها عند إزالة إلى صفر.

### آدم: الزخم + RMSProp ٠ آدم:动量 + تطابق الذاتي معدل التعلم

آدم يجمع بين هذين الفكرين، وهو يحافظ على متوسطين متحركين متكيفين لكل مبرمج:

> آدم 结合了两种思想──它为每个参数维护两个指数移动平均值:

```
m_t = beta1 * m_{t-1} + (1 - beta1) * gradient        (first moment: mean)        # 一阶矩：梯度均值
v_t = beta2 * v_{t-1} + (1 - beta2) * gradient^2       (second moment: variance)   # 二阶矩：梯度方差
```

**Bias correction**هو التفاصيل الرئيسية التي تفوت معظم التفسيرات. في الخطوة 1، m_1 = (1 - بيتا1) * تراجيع. مع بيتا1 = 0.9, هذا هو 0.1 * تراجيع -- عشرة مرات صغيرة جدا. المتوسط المتحرك لم يُحترم بعد. تعويض تعديل التحيز:

> **偏差修正**هو معظم تفسير قفز من التفاصيل الرئيسية.

```
m_hat = m_t / (1 - beta1^t)
v_hat = v_t / (1 - beta2^t)
```

في الخطوة 1 مع beta1 = 0.9: m_hat = m_1 / (1 - 0.9) = m_1 / 0.1 = التنحدر الفعلي. في الخطوة 100: (1 - 0.9^100) هو حوالي 1.0, لذلك تختفي التصحيح. التصحيح التحيزية مهمة بالنسبة لأول ~ 10 خطوات وغير ذات صلة بعد ~ 50.

> 第 1 步 beta1 = 0.9 时:m_hat = m_1 / (1 - 0.9) = m_1 / 0.1 = 实际梯度──第 100 步:(1 - 0.9^100) 大约等于 1.0,修正消失──偏差修正对前 ~10 步重要,~50 步后无关紧要──

التحديث:

> 更新公式:

```
w = w - lr * m_hat / (sqrt(v_hat) + epsilon)
```

أديام الافتراضات: lr = 0.001، beta1 = 0.9، beta2 = 0.999, epsilon = 1e-8. هذه الافتراضات تعمل على 80% من المشاكل. عندما لا يفعلون ذلك، تغيير lr أولا. ثم بيتا2.

> آدم 默认值:lr = 0.001,beta1 = 0.9,beta2 = 0.999,epsilon = 1e-8。 هذه القيم الم默认 تطبق على 80% من المشاكل──不适用时,先调 lr,再调 beta2──几乎从不需要改beta1或epsilon──

> **【拓展：Adam 的局限性】**على الرغم من أن آدم هو المعدل الأكثر استخداماً، إلا أنه ليس كاملًا: 1) في بعض المشاكل الملتوية لا تكون مثل SGD ؛ 2) أن آدم كان عامًا في بعض الأحيان يختلف عن SGD ؛ 3) أن آدم كان يتمتع بتكلفة كبيرة من SGD ، وذلك لأن معدل التعلم المتكيف يمكن أن يؤدي إلى زيادة التكيف ؛ 3) أن آدم كان يتحمل إمدادات إمدادات إمدادات إمدادات إمدادات إمدادات إمدادات إمدادات إمدادات إمدادات إدنية.

### إنخفاض الوزن صحيح

يضيف التنظيم L2 لامبا * w^2 إلى الخسارة. في SGD الفانيليا، هذا يعادل تدهور الوزن (إخراج لامبا * w من الوزن في كل خطوة). في آدم، هذا التكافؤ ينفذ.

> L2 إصلاحية ستعمل على اللامبدا * w^2 إضافة إلى الخسارة. في SGD الأصلية، هذا يساوي الوزن المقلد. في آدم، هذا يساوي الوزن المقلد.

نظرة لوششيلوف وهاتر: عندما تضيف L2 إلى الخسارة ثم يعالج آدم التدفق، معدل التعلم التكيفي يُقيس أيضاً مصطلح التدفق. العناصر ذات التباين الكبير يتحصل على تقييم أقل. العناصر ذات التباين الصغير تتحصل على المزيد. هذا ليس ما تريده - تريد تقييم متساو بغض النظر عن إحصاءات التدفق.

> رؤى لوششيلوف و هاتر: عندما تضيف L2 إلى الخسارة ثم آدم  معالجة التعدد، فإن معدل التعلم التكيفي أيضا يقلل من التعدد.

يصلح AdamW هذا الأمر عن طريق تطبيق التدهور الوزن مباشرة على الوزن، بعد تحديث آدم:

```
w = w - lr * m_hat / (sqrt(v_hat) + epsilon) - lr * lambda * w    # Adam 更新 + 解耦权重衰减
```

لا يتم قياس مصطلح التدهور في الوزن (lr * lambda * w) بواسطة عامل آدم التكيفي. كل معايير تحصل على نفس الانكماش النسبي.

يبدو هذا كجزء بسيط. ليس كذلك. يتقارب AdamW إلى حلول أفضل من إعادة تنظيم Adam + L2 في كل مهمة تقريبًا. إنه المحفز الافتراضي في PyTorch لتدريب المحولات، ونماذج التوزيع، ومعظم الهندسة المعمارية الحديثة. BERT، GPT، LLaMA، التوزيع المستقر - جميعها مدربة مع AdamW.

> **【中文解读】**إصلاحات أساسية في AdamW: حق الوزن ينخفض دون مرور آدم,作用直接 إلى العنصرات.

> **【拓展：LoRA 微调中的 AdamW】**مع LoRA 微调 LLM 时, عادة مع AdamW(lr=2e-5~1e-4, الوزن_decay=0.01)。LoRA فقط تدريب القليل على تقسيم المواصفات A و B,AdamW الوزن القلل يساعد على التحكم في حجم هذه العناصر الجديدة。

### معدل التعلم: أهم المعيار المفرط

```mermaid
graph TD
    LR["Learning Rate"] --> TooHigh["Too high (lr > 0.01)"]
    LR --> JustRight["Just right"]
    LR --> TooLow["Too low (lr < 0.00001)"]

    TooHigh --> Diverge["Loss explodes<br/>NaN weights<br/>Training crashes"]
    JustRight --> Converge["Loss decreases steadily<br/>Reaches good minimum<br/>Generalizes well"]
    TooLow --> Stall["Loss decreases slowly<br/>Gets stuck in suboptimal minimum<br/>Wastes compute"]

    JustRight --> Schedule["Usually needs scheduling"]
    Schedule --> Warmup["Warmup: ramp from 0 to max<br/>First 1-10% of training"]
    Schedule --> Decay["Decay: reduce over time<br/>Cosine or linear"]
```

إذا قمت بتحديد معايير فائقة واحدة، تحبط معدل التعلم. تغيير 10x في معدل التعلم مهم أكثر من أي قرار معماري سوف تتخذ.

> إذا كنت تحويلي واحد فقط من العناصر العالية، تحويلي معدل التعلم ‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

- SGD: lr = 0.01 إلى 0.1
  SGD:lr = 0.01 إلى 0.1
- آدم/آدمW: lr = 1e-4 إلى 3e-4
  آدم/آدمW:lr = 1إيه-4 إلى 3إيه-4
- النماذج المُدربة مسبقاً للتحقيق: lr = 1e-5 إلى 5e-5
  微调预训练模型:lr = 1e-5 إلى 5e-5
- ارتفاع معدل التعلم: ريمب خطية خلال الخطوات الأولى 1-10%
  معدل التعلم الدافئ: في 1-10% الاولى

### تحسين مقارنة مع تحسينات

```mermaid
flowchart LR
    subgraph "Optimization Path"
        SGD_P["SGD<br/>Oscillates across valley<br/>Slow but finds flat minima"]
        Mom_P["SGD + Momentum<br/>Smoother path<br/>3x faster than SGD"]
        Adam_P["Adam<br/>Adapts per-parameter<br/>Fast convergence"]
        AdamW_P["AdamW<br/>Adam + proper decay<br/>Best generalization"]
    end
    SGD_P --> Mom_P --> Adam_P --> AdamW_P
```

### عندما يفوز كل محفز

```mermaid
flowchart TD
    Task["What are you training?"] --> Type{"Model type?"}

    Type -->|"Transformer / LLM"| AdamW["AdamW<br/>lr=1e-4, wd=0.01-0.1"]
    Type -->|"CNN / ResNet"| SGD_M["SGD + Momentum<br/>lr=0.1, momentum=0.9"]
    Type -->|"GAN"| Adam2["Adam<br/>lr=2e-4, beta1=0.5"]
    Type -->|"Fine-tuning"| AdamW2["AdamW<br/>lr=2e-5, wd=0.01"]
    Type -->|"Don't know yet"| Default["Start with AdamW<br/>lr=3e-4, wd=0.01"]
```

> **【拓展：深度学习中优化器的演进】**من 2012 AlexNet SGD+Momentum، إلى 2014 Adam طرح، مرة أخرى إلى 2017 AdamW ولد تطوير المنحفات جعل التدريب من" تحتاج إلى عدة أسابيع لتعديل" إلى" المتفردة العيار على القدرة على السير"。 تدريب Llama 3 405B باستخدام AdamW، قمة القيمة lr=3e-4, في 16384 بلاك H100 GPU التدريب على 30.8M GPU 小时──

## بناء ذلك تحرك لتحقيق

> **【中文解读】**أسفل من صفر تحقيق أربعة أشكال تحسينات:SGD → SGD+Momentum → آدم → آدمW── كل واحد على أساس السابقة إضافة آلية رئيسية── ملاحظة تحسين التمييز آدمW والانحدار من الوزن الادامW هي نقطة المعرفة في المقابلة العادية──
```figure
optimizer-trajectory
```

## بناءها

### الخطوة الأولى: SGD الفانيليا الخطوة الأولى: SGD الأصلية

> SGD الأصلي: العنصر مباشرة خفض معدل التعلم المتعدد 

```python
class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        for i in range(len(params)):
            params[i] -= self.lr * grads[i]
```

### الخطوة الثانية: SGD مع الزخم الخطوة الثانية:

> SGD+Momentum: تعريف التغيرات السريعة، تراكم التاريخية تدريجية.

```python
class SGDMomentum:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.velocities = None

    def step(self, params, grads):
        if self.velocities is None:
            self.velocities = [0.0] * len(params)
        for i in range(len(params)):
            self.velocities[i] = self.beta * self.velocities[i] + grads[i]
            params[i] -= self.lr * self.velocities[i]
```

### الخطوة الثالثة: آدم.

> آدم:维护一阶矩 m                                                                                                                                                                                                                                                           

```python
import math

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)

        self.t += 1

        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2

            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
```

### الخطوة الرابعة: أدمو

> آدم و.أ: على أساس آدم، تحليل انخفاض الوزن من الدرجة إلى الدرجة مباشرة إلى العنصر نفسه، دون أن يمر عبر تكميل m و v.

```python
class AdamW:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.weight_decay = weight_decay
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)

        self.t += 1

        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2

            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
            params[i] -= self.lr * self.weight_decay * params[i]
```

### الخطوة 5: مقارنة التدريب الخطوة 5: التدريب مقابل

قم بتدريب نفس الشبكة ذات الطبقتين على مجموعة بيانات الدورة من الدروس 05 مع جميع المحفزات الأربعة. مقارنة التقارب.

> باستخدام 5  ة درجة التدريب على مجموعة بيانات دائرية نفس شبكة ذات مستويين، مقابل أسرع من أربعة محركات تحسينات.

```python
import random

def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))

def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class OptimizerTestNetwork:
    def __init__(self, optimizer, hidden_size=8):
        random.seed(0)
        self.hidden_size = hidden_size
        self.optimizer = optimizer

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def get_params(self):
        params = []
        for row in self.w1:
            params.extend(row)
        params.extend(self.b1)
        params.extend(self.w2)
        params.append(self.b2)
        return params

    def set_params(self, params):
        idx = 0
        for i in range(self.hidden_size):
            for j in range(2):
                self.w1[i][j] = params[idx]
                idx += 1
        for i in range(self.hidden_size):
            self.b1[i] = params[idx]
            idx += 1
        for i in range(self.hidden_size):
            self.w2[i] = params[idx]
            idx += 1
        self.b2 = params[idx]

    def forward(self, x):
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def compute_grads(self, target):
        eps = 1e-15
        p = max(eps, min(1 - eps, self.out))
        d_loss = -(target / p) + (1 - target) / (1 - p)
        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        grads = [0.0] * (self.hidden_size * 2 + self.hidden_size + self.hidden_size + 1)
        idx = 0
        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            grads[idx] = d_h * self.x[0]
            grads[idx + 1] = d_h * self.x[1]
            idx += 2

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            grads[idx] = d_out * self.w2[i] * d_relu
            idx += 1

        for i in range(self.hidden_size):
            grads[idx] = d_out * self.h[i]
            idx += 1

        grads[idx] = d_out
        return grads

    def train(self, data, epochs=300):
        losses = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in data:
                pred = self.forward(x)
                grads = self.compute_grads(y)
                params = self.get_params()
                self.optimizer.step(params, grads)
                self.set_params(params)

                eps = 1e-15
                p = max(eps, min(1 - eps, pred))
                total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            avg_loss = total_loss / len(data)
            accuracy = correct / len(data) * 100
            losses.append((avg_loss, accuracy))
            if epoch % 75 == 0 or epoch == epochs - 1:
                print(f"    Epoch {epoch:3d}: loss={avg_loss:.4f}, accuracy={accuracy:.1f}%")
        return losses
```

> **【拓展：GPT 训练中的优化器选择】**OpenAI 系列 GPT 全部使用 Adam 优化器(GPT-4 推测也使用 AdamW) 』 تدريب 时一常见技巧: على إضافة 层和输出 层使用不同的学习率──在 PyTorch 中通过参数组 实现:`optimizer = AdamW([{'params': base_params}, {'params': head_params, 'lr': lr*0.1}])`.

## استخدمها في إطار التنفيذ

> **【中文解读】**PyTorch 中的训练循环模式:zero_grad → forward → loss → backward → clip → step → schedule──这个顺序不能搞错──CNN 用SGD+Momentum(lr=0.1),Transformer 用AdamW(lr=1e-4)──

تعمل محفزات PyTorch على تعديل مجموعات المعلمات، وتقطيع التراجع، وتخطيط معدل التعلم:

```python
import torch
import torch.optim as optim

model = torch.nn.Sequential(
    torch.nn.Linear(784, 256),
    torch.nn.ReLU(),
    torch.nn.Linear(256, 10),
)

optimizer = optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

for epoch in range(100):
    optimizer.zero_grad()
    output = model(torch.randn(32, 784))
    loss = torch.nn.functional.cross_entropy(output, torch.randint(0, 10, (32,)))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    scheduler.step()
```

النمط هو دائما: zero_grad، forward، loss، backward، (clip) ، step، (schedule). حفظ هذا الترتيب. الحصول على خطأ (على سبيل المثال، الاتصال المخطط.step() قبل optimizer.step()) هو مصدر شائع للخطأ الخفيف.

بالنسبة لسي إن إن، لا يزال العديد من الممارسين يفضلون SGD + الزخم (lr=0.1 ، الزخم = 0.9 ، الوزن_انهيار = 1e-4) مع جدول خطوة أو كوسين. يجد SGD أدنى مستويات مسطحة ، والتي غالباً ما تجميع بشكل أفضل. بالنسبة للمتحولين والإل إل إم ، فإن AdamW مع التدفئة + تدهور كوسين هو الافتراض الشامل. لا تقاتل التوافق دون سبب مقيّر.

## أرسلها .

هذا الدرس ينتج عن:
- `outputs/prompt-optimizer-selector.md`-- تحرك قرار لتحديد المُحسن ومعدل التعلم المناسب لأي بنية

## تمارين التدريب

1. قم بتنفيذ زخم نستروف، حيث تقوم بحساب التراجع في وضع "النظر" (w - lr * beta * v) بدلاً من الموقف الحالي. مقارنة التقارب مع زخم قياسي على مجموعة بيانات الدائرة.
   > **练习 1：**实现 Nesterov 动量 ((在"前"位置计算梯度),对标准动量的收速度──

2. تنفيذ جدول تعليمي للتدفئة: ريمب خطي من 0 إلى ماكس_لر خلال 10% من مراحل التدريب الأولى ، ثم تدهور الكوسين إلى 0. تدريب مع آدم + التدفئة مقابل آدم دون التدفئة. قياس عدد الفترات التي يستغرقها الوصول إلى دقة 90٪ على مجموعة بيانات الدائرة.
   > **练习 2：**تحقيق التدفئة + تدهور الكويسين تعديل معدل التعلم، مقارنة مع عدم التدفئة  تصل إلى 90%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

3. تتبع معدل التعلم الفعلي لكل معايير خلال تدريب آدم. المعدل الفعلي هو lr * m_hat / (sqrt(v_hat) + eps). رسم توزيع المعدلات الفعالة بعد 10، 50 و 200 خطوة. هل يتم تحديث جميع المعايير بنفس السرعة؟
   > **练习 3：** تتبع آدم  التدريبات معدل التعلم الفعال للعنصرات المختلفة، وملاحظة اختلافات في سرعة تحديث العنصرات المختلفة

4. قم بتنفيذ قطع التدرج (التقاط حسب المعيار العالمي). حدد معيار التدرج الأقصى إلى 1.0. قم بتدريب مع ودون قطع باستخدام معدل تعلم مرتفع (lr=0.01 بالنسبة لآدم). احسب عدد الركود التي تختلف (الخسارة تذهب إلى NaN) مع ودون قطع أكثر من 10 بذور عشوائية.
   > **练习 4：**تحقيق نسبة التدريبات المتوسطة في التعلم

5. مقارنة آدم مقابل آدم و على شبكة مع أوزان كبيرة. قم بتبني جميع الأوزان إلى قيم عشوائية في [-5, 5] (أكبر بكثير من الطبيعي). قم بتدريب 200 عصر مع وزن_انحدار = 0.1. رسم معايير الوزن L2 على التدريب لكل من المحفسينين. يجب أن يظهر آدم ووتان تقلص الوزن بشكل أسرع.
   > **练习 5：**في الوزن الأولية الكبيرة مقابل آدم و آدم و لاحظ اختلافات في الوزن الأولية

## شروط رئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Learning rate | "Step size" | The scalar multiplier on the gradient update; the single most impactful hyperparameter in training |
| SGD | "Basic gradient descent" | Stochastic gradient descent: update weights by subtracting lr * gradient, computed on a mini-batch |
| Momentum | "Rolling ball analogy" | Exponential moving average of past gradients; dampens oscillation and accelerates consistent directions |
| RMSProp | "Adaptive learning rate" | Divides each parameter's gradient by the running RMS of its recent gradients; equalizes learning rates |
| Adam | "The default optimizer" | Combines momentum (first moment) and RMSProp (second moment) with bias correction for the initial steps |
| AdamW | "Adam done right" | Adam with decoupled weight decay; applies regularization directly to weights rather than through the gradient |
| Bias correction | "Warmup for running averages" | Dividing by (1 - beta^t) to compensate for the zero-initialization of Adam's moment estimates |
| Weight decay | "Shrink the weights" | Subtracting a fraction of the weight value at each step; a regularizer that penalizes large weights |
| Learning rate schedule | "Changing lr over time" | A function that adjusts the learning rate during training; warmup + cosine decay is the modern default |
| Gradient clipping | "Capping the gradient norm" | Scaling down the gradient vector when its norm exceeds a threshold; prevents exploding gradient updates |

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 学习率 (Learning rate) | "步长" | 梯度更新的标量乘数；训练中影响最大的超参数 |
| SGD | "基础梯度下降" | 随机梯度下降：用小批量梯度更新 w -= lr * grad |
| 动量 (Momentum) | "滚球的类比" | 历史梯度的指数移动平均；抑制振荡、加速一致方向 |
| RMSProp | "自适应学习率" | 除以梯度平方的移动平均根；均衡各参数学习速度 |
| Adam | "默认优化器" | 动量 + RMSProp + 偏差修正的统一优化器 |
| AdamW | "正确的 Adam" | Adam + 解耦权重衰减；直接对参数施加正则化 |
| 偏差修正 (Bias correction) | "运行平均的热身" | 除以 (1-beta^t) 补偿 Adam 矩估计的零初始化偏差 |
| 权重衰减 (Weight decay) | "缩小权重" | 每步减去权重的一小部分；惩罚大权重的正则化手段 |
| 学习率调度 (LR schedule) | "随时间改变 lr" | 训练中调整学习率的函数；warmup + cosine decay 是现代标配 |
| 梯度裁剪 (Gradient clipping) | "限制梯度范数" | 梯度范数超限时缩小梯度；防止梯度爆炸 |

## المزيد من القراءة

- كينغما وبا، "آدام: طريقة للتحسين الاستوكاسطي" (2014) -- ورقة آدم الأصلية مع تحليل التقارب وتحليل التحسّل التحيزي
- لوششيلوف وهاتر، "تعديل التدهور في الوزن منفصل" (2017) -- أثبت أن تقييم L2 وتدهور الوزن ليسوا متساوين في آدم، واقترح أن آدم
- سميث، "تطورات التعلم الدوري للشبكات العصبية التدريبية" (2017) -- قدمت اختبار مجموعة LR والجدول الزمني الدوري الذي يزيل الحاجة إلى ضبط معدل التعلم الثابت
- رودر، "مراجعة عامة لخوارزميات تحسين التراجع التدريجي" (2016) -- أفضل مسح واحد لجميع أنواع المحفزات، مع مقارنات وضوحية والحسبان
