# اكتشاف الأشياء  YOLO من الصفر ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬

> الكشف هو التصنيف بالإضافة إلى الرجوع، يتم تشغيله في كل موقع في خريطة الميزات، ثم يتم تنظيفه مع القمع غير القصوى.

> **【中文解读】**目标检测 = 分类 + 回归,运行 في كل موقع من الرسم البياني, ثم باستخدام غير عالية القيمة منعقدة(NMS) التطهير重复检测框――YOLO(You Only Look Once) الفكرة الأساسية هي: سوف تحويل مشكلة الاختبار إلى مشكلة التنبؤ المكثف, مرة واحدة إلى الأمام للتنشر في نفس الوقت التنبؤ جميع الفئات والمواقع المستهدفة。

> **【拓展：YOLO 在自动驾驶中的应用】**يولو هو أهم أليفات تحليل الهدف في الوقت الحقيقي في القيادة الذاتية، قادرة على تحليل الأشخاص والسيارات والعلامات المرورية، وما إلى ذلك.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 03 (CNNs), Phase 4 Lesson 04 (Image Classification), Phase 4 Lesson 05 (Transfer Learning) | **前置知识:** Phase 4 Lesson 03（CNN），Phase 4 Lesson 04（图像分类），Phase 4 Lesson 05（迁移学习）
**Time:** ~75 minutes | **时间:** ~75 分钟

## أهداف التعلم

- شرح تصميم الشبكة والمركز الذي يحول الكشف إلى مشكلة تنبؤ كثيفة ووضح ما يعنيه كل رقم في الجهاز التنفيذي
- الحسابات التقاطع بين الصناديق وتنفيذ القضاء غير القصوى من الصفر
- بناء رأس بسيط على رأس العمود الفقري المُدرب مسبقاً، بما في ذلك التصنيف، والشيء، والخسائر في التراجع
- اقرأ صف متري للكشف (precision@0.5, recall, mAP@0.5, mAP@0.5:0.95) واختيار الزر الذي يجب أن تدور فيه التالية

> **【中文解读】**يُدعى أهداف التعلم المفردة التي يجب أن تتحكم فيها بعد الانتهاء من الدورة.


## المشكلة المشكلة المشكلة

تقول التصنيف "هذه الصورة هي كلب". يقول الكشف "هناك كلب في البيكسلات (112, 40, 280, 210) ، وهناك قطة في (400, 180, 560, 310) ، ولا شيء آخر في الإطار. " أن واحد تغيير هيكلي  التنبؤ وعدد متغير من الصناديق الملصقة بدلا من ملصق واحد لكل صورة  هو ما يعتمد على كل نظام مستقل، كل منتج مراقبة، كل تصميم المستندات، وكل خط رؤية المصنع.

>  分类说"هذا الصورة هو كلب"──检测说"في الصورة (112, 40, 280, 210) يوجد كلب واحد، في (400, 180, 560, 310) يوجد قطة واحدة، في الصورة لا يوجد شيء آخر──"هذا التغيير الهيكلي التنبؤ بأعداد المتغيرة من مربع علامات التأشير بدلاً من كل صورة على علامة هي كل نظام قيادة ذاتي٬ كل منتج مراقبة٬ كل نسخة تصميمات محللة وكل خط المنتجات المشهورة المصنعة يعتمد عليها──

> **【中文解读】** 分类说" هذا الصورة هو كلب"检测说"狗在 (112,40,280,210),猫在 (400,180,560,310) "...... هذا التغيير الهيكلي من التنبؤ إلى التنبؤ إلى عدد غير مؤكد من مربع المشاريع  هو السيارات الذاتية  امن مراقبة  تصنيف الملفات 面分析和工厂质检的核心能力

الكشف هو أيضاً المكان الذي تظهر فيه كل التداول الهندسي في الرؤية في نفس الوقت. تريد صناديق دقيقة (رأس التراجع) ، تريد الطبقة المناسبة لكل صناديق (رأس التصنيف) ، تريد أن يعرف النموذج عندما لا يوجد شيء للكشف عنه (درجة الكائن) ، وتريد تنبؤًا واحدًا بالضبط لكل كائن حقيقي (قمع غير أقصى). إضافة إلى أن خط الأنابيب إما يضيع الأشياء أو يبلغ عن صناديق الهلوسة أو يتوقع نفس الشيء خمسة عشر مرة في مواقع مختلفة قليلاً

> الاختبار هو أيضاً المكان الذي يظهر فيه كل الاختبارات في المشاهدة. ستحتاج إلى مربع صحيح (صورة) ، ستحتاج إلى كل مربع من الصفوف صحيحة (صورة) ، ستحتاج إلى نموذج يعرف أين لا يوجد شيء لتحقيقه (صورة) ، ستحتاج إلى كل شيء حقيقي (صورة) ، ستحتاج إلى توقعات (صورة) ، لا تقلق (صورة) ، ستحتاج إلى أي شيء حقيقي (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى أي شيء آخر (صورة) ، ستحتاج إلى (صورة) ، أو ستحتاج إلى (صورة)

يولو (أنت فقط تنظر مرة واحدة، ريدمون وزملاء 2016) هو التصميم الذي جعل كل هذا الجري في الوقت الحقيقي عن طريق القيام بذلك مع مرور واحد إلى الأمام من شبكة مخزن، والقرارات الهيكلية نفسها لا تزال العمود الفقري للمكشفات الحديثة (YOLOv8، YOLOv9، YOLO-NAS، RT-DETR). تعلم الأساس و كل فاريان يصبح إعادة ترتيب من نفس الأجزاء.

> يولو ((أنت تبحث مرة واحدة فقط ، ريدمون وغيرها 2016) هو من خلال عملية تنسيق واحدة من خلال شبكة الانتشار لتوسيع جميع هذه الممارسات التي تعمل في الوقت الحقيقي ، والقرارات الهيكلية نفسها لا تزال هي الاختبار الحديث ((YOLOv8、YOLOv9、YOLO-NAS、RT-DETR)

> **【中文解读】**检测是视觉中所有工程权衡的交汇点:框要准确(回归头) 类别要正确(分类头) 要知道哪里没有物体(置信度) 、每个物体只检测一次(NMS) 。YOLO 用单次前向传播实现所有这些,同样设计思想延续到YOLOv8、RT-DETR 等现代检测器──

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


### الكشف كتنبؤ كثيف

مصنف يخرج أرقام C لكل صورة. جهاز كشف نمط YOLO يخرج`(S x S x (5 + C))`أرقام لكل صورة، حيث S هو حجم الشبكة الفضائية.

>  分类器每张图像输出 C 个数字──YOLO 风格的检测器每张图像输出 `(S x S x (5 + C))`个数字,其中 S 是空间网格大小──

```mermaid
flowchart LR
    IMG["Input 416x416 RGB"] --> BB["Backbone<br/>(ResNet, DarkNet, ...)"]
    BB --> FM["Feature map<br/>(C_feat, 13, 13)"]
    FM --> HEAD["Detection head<br/>(1x1 convs)"]
    HEAD --> OUT["Output tensor<br/>(13, 13, B * (5 + C))"]
    OUT --> DEC["Decode<br/>(grid + sigmoid + exp)"]
    DEC --> NMS["Non-max suppression"]
    NMS --> RESULT["Final boxes"]

    style IMG fill:#dbeafe,stroke:#2563eb
    style HEAD fill:#fef3c7,stroke:#d97706
    style NMS fill:#fecaca,stroke:#dc2626
    style RESULT fill:#dcfce7,stroke:#16a34a
```

كل واحد من`S * S`خلايا الشبكة تتوقع `B`الصناديق لكل صندوق:

> كل واحد`S * S`网格单元预测 `B`个框──对于每个框:

- 4 أرقام تصف الهندسة: `tx, ty, tw, th`. . .
  中文翻译:4 个数字描述几何形状:`tx, ty, tw, th`(مركز الانحراف والانخفاض)
- الرقم 1 هو نسبة الاكتتاب: "هل هناك شيء مركز في هذه الخلية؟"
  ترجمة: 1 个数字是目标性分数:"هل يوجد في مركز الوحدة أي شيء؟"
- أرقام "س" هي احتمالات الفئة
  中文翻译:C 个数字是类别概率──

إجمالي لكل خلية: `B * (5 + C)`. لـ VOC مع `S=13, B=2, C=20`، وهذا هو 50 رقم لكل خلية.

> كل وحدة مجموع:`B * (5 + C)` بالنسبة لـ VOC`S=13, B=2, C=20`, أي كل وحدة 50 رقم

### لماذا الشبكات والرسوم

التراجع البسيط يتنبأ`(x, y, w, h)`لجميع الأشياء كنسجمة مطلقة. هذا صعب على شبكة conv لأن ترجمة الصورة لا ينبغي أن ترجمة جميع التنبؤات بنفس الكمية  كل شيء مقوسة مساحيا. الجريدية تجيب على هذا عن طريق تعيين كل مربع الحقيقة الأرضية إلى الخلية الشبكة يقع مركزها في؛ فقط تلك الخلية هي المسؤولة عن هذا الموضوع.

> فقط العودة إلى كل شيء`(x, y, w, h)` كمحرك مطلق للتنبؤ. هذا أمر صعب بالنسبة لشبكة الكولومات، لأن الصورة المسبقة لا ينبغي أن تضع جميع التنبؤات على نفس الكمية كل جسم في الفضاء مستقل.

المرسومات تعالج مشكلة ثانية. لا يمكن لـ 3 × 3 conv أن يعود بسهولة مربع 500 بكسل على نطاق واسع من خلية ميزة حقل استقبلية 16 بكسل. بدلاً من ذلك، نحن نعرّف مسبقاً`B`يُتوقع النموذج أن يختار المرسوم الصحيح ويضعه بدلاً من التراجع من لا شيء.

> 框解决第二问题──3x3 卷积很难从16 像素感受野的特征单元回归到500 像素宽的框──因此我们为每个单元预定义 `B`个先验框形状(框),并预测 نسبتاً لكل 框的小偏移量──模型学习选择正确的框并微调,而不是从零回归──

```
Anchor box priors (example for 416x416 input):

  small:   (30,  60)
  medium:  (75,  170)
  large:   (200, 380)

At each grid cell, every anchor emits (tx, ty, tw, th, obj, c_1, ..., c_C).
```

غالبا ما تستخدم الكشفات الحديثة FPN مع مجموعات مقعد مختلفة لكل قرار مقعدات صغيرة على خرائط عالية الدقة ، مقعدات كبيرة على خرائط عالية الدقة العميقة منخفضة الدقة. نفس الفكرة ، المزيد من المقاييس.

> تستخدم المفتشات الحديثة عادةً FPN (معارض شبكة الكيميائي) ، على مختلف القرارات استخدام مجموعة مختلفة من الصور على القرارات المختلفة.

### توقعات فك التشفير

الخام`tx, ty, tw, th`ليست إحداثيات مربع، بل هي أهداف تراجع يجب تحويلها قبل التخطيط:

> أصلي`tx, ty, tw, th`ليست مربع مقعد؛ فهي تحتاج إلى تعديل في الرسمة السابقة

```
centre x  = (sigmoid(tx) + cell_x) * stride
centre y  = (sigmoid(ty) + cell_y) * stride
width     = anchor_w * exp(tw)
height    = anchor_h * exp(th)
```

`sigmoid`يحتفظ بالتعديلات المركزية داخل الخلية. `exp`يسمح للمقياس العريض بحرية من المرسوم دون تحويل إشارة. `stride`يُقَدِّم خطوات الشبكة إلى بيكسلات. هذه الخطوة في فك الشفرة هي نفسها في كل إصدار من YOLO منذ v2.

> `sigmoid`سيتم تحريك المركز في وحدات واحدة`exp`让宽度可以从框自由缩放而不需要符号翻转.`stride`سوف يتم تعديل الشبكة إلى صورة.

### (إي أو)

المقياس الشبيه العالمي للكشف بين مربعتين:

> 检测中2框之间的通用相似度度度:

```
IoU(A, B) = area(A intersect B) / area(A union B)
```

IoU = 1 يعني متطابقة؛ IoU = 0 يعني عدم التداخل. IoU بين التنبؤ والصندوق الحقيقي الأساسي هو ما يقرر ما إذا كان التنبؤ يعتبر إيجابيًا صحيحًا (عادة IoU > = 0.5). IoU بين التنبؤين هو ما يستخدمه NMS للتقليص.

> يُظهر IoU = 1 تماماً نفسها؛ IoU = 0 يُظهر تماماً غير متداخلة. يُقرر IoU أن يكون الوقوف على الحساب مثالاً حقيقياً. عادةً IoU >= 0.5)

### القمع غير القصوى

غالبًا ما تتوقع شبكة CONV تدرب على المرافق المجاورة صناديق تتداخل لنفس الكائن. تحتفظ NMS بالتنبؤ بأعلى ثقة وتحذف أي التنبؤات الأخرى مع IoU فوق عتبة.

> عادة ما تكون شبكة التجميع التي تمارس على الإطار المجاور تتوقع العديد من الإطارات المتداخلة من نفس الكائن.

```
NMS(boxes, scores, iou_threshold):
    sort boxes by score descending
    keep = []
    while boxes not empty:
        pick the top-scoring box, add to keep
        remove every box with IoU > iou_threshold to the picked box
    return keep
```

العدالة النموذجية: 0.45 للكشف عن الكائنات. الكشفات الأخيرة تحل محل NMS القياسية ب `soft-NMS`،`DIoU-NMS`أو تعلم القمع مباشرة (RT-DETR) ولكن الغرض الهيكلي هو نفسه.

> 典型值: هدف检测用 0.45──最近检测器用 `soft-NMS`.`DIoU-NMS`替代标准NMS,或直接学习抑制策略(RT-DETR) ، ولكن الهدف الهيكلي هو نفسه.

### الخسارة

خسارة YOLO هي ثلاثة خسائر مضافة مع الوزن:

> يوولو  خسارة هي ثلاثة وظائف خسارة + حق طلب و:

```
L = lambda_coord * L_box(pred, target, where obj=1)
  + lambda_obj   * L_obj(pred, 1,     where obj=1)
  + lambda_noobj * L_obj(pred, 0,     where obj=0)
  + lambda_cls   * L_cls(pred, target, where obj=1)
```

تساهم الخلايا التي تحتوي على كائن فقط في خسائر التراجعة والتصنيف. تساهم الخلايا التي لا تحتوي على كائن فقط في خسارة الكائن (تعليم النموذج على الصمت). `lambda_noobj`عادة ما تكون صغيرة (~ 0.5) لأن الغالبية العظمى من الخلايا فارغة وإلا سيهيمن على الخسارة الكلية.

>  فقط وحدات المواد المحتوية على إعادة الإصلاح والفئات من الخسائر هي المساهمة.`lambda_noobj`عادةً يكون ذلك صغيراً (حوالي 0.5 رصيد) ، لأن معظم الوحدات هي فارغة، وإلا ستؤدي إلى الإضرارات الكاملة.

وتستبدل التغيرات الحديثة خسارة صندوق MSE مقابل CIoU / DIoU (التي تحسن IoU مباشرة) ، واستخدام خسارة التركيز لعدم التوازن في الفئة، وتوازن العنصر مع خسارة التركيز الجودة. لا تتغير هيكل ثلاثة مكونات.

> 现代变体用 CIoU/DIoU(直接优化 IoU) بديل عن MSE 框损失, باستخدام فقدان التركيز 处理类别不平衡, باستخدام فقدان التركيز الجودة平衡目标性──三组件结构不变──

### مقاييس الكشف

الدقة لا تنتقل إلى الكشف أربعة أرقام تفعل:

> 准确率 غير مناسبة للتحقق.

- **Precision@IoU=0.5** من التنبؤات التي تم احتسابها إيجابية، كم عدد منها صحيحة فعلاً.
  中文翻译:**Precision@IoU=0.5**في التنبؤات التي تم اعتبارها صحيحة، هناك الكثير من الأشياء التي هي صحيحة حقا.
- **Recall@IoU=0.5**من الأشياء الحقيقية، كم وجدنا.
  中文翻译:**Recall@IoU=0.5**بين كل الأشياء الحقيقية، وجدنا الكثير
- **AP@0.5** مساحة منحنى الاستعادة الدقيقة عند عتبة الـ IoU 0.5، رقم واحد لكل فئة.
  中文翻译:**AP@0.5** IoU                                                                                                                                                                                                                                                             
- **mAP@0.5:0.95** متوسط AP فوق أعلى حدود IoU 0.5، 0.55, ..., 0.95.
  中文翻译:**mAP@0.5:0.95** AP في IoU قيمة 0.5、0.55、...、0.95 العليا متوسط القيمة──COCO 指标;最严格、信息量最大──

تقرير كل أربعة. الكشف الذي هو قوي على mAP@0.5 ولكن ضعيف على mAP@0.5:0.95 هو تحديد المواقع بشكل تقريبي ولكن ليس بقوة؛ إصلاح مع أفضل خسارة التراجعة الصندوق. الكشف مع دقة عالية ومنخفضة التذكر هو محافظ جدا؛ خفض عتبة الثقة أو زيادة وزن الكائنة.

> 報告全部四指标── واحد في mAP@0.5 上强但在 mAP@0.5:0.95 上弱的检测器定位粗略但不精确; باستخدام أفضل إطار للعودة إلى الخسارة لإصلاح── واحد عالية الدقة والقليل للعودة إلى الاحتفاظ بها; تخفيض الثقة值或增加目标性权重──

> **【拓展：工业部署中的视觉系统】**في التوزيع الصناعي الواقعي، تحتاج النموذج المرئي إلى النظر في التفكير في التأجيل، والنموذج الكبير، والجهاز الحدودي الملائمة وغيرها من المشاكل.

> **【拓展：数据标注与质量】** تأثير المهام المرئية يعتمد على جودة البيانات المعلنة.‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬



## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

```figure
object-detection-nms
```

## بناءها

### الخطوة الأولى:

فحص العمل في الدروس كلها يعمل على صفين من الصناديق في`(x1, y1, x2, y2)`التنسيق

> أدوات الأساسية لهذا الدراسة`(x1, y1, x2, y2)`格式的框──

```python
import numpy as np

def box_iou(boxes_a, boxes_b):
    ax1, ay1, ax2, ay2 = boxes_a[:, 0], boxes_a[:, 1], boxes_a[:, 2], boxes_a[:, 3]
    bx1, by1, bx2, by2 = boxes_b[:, 0], boxes_b[:, 1], boxes_b[:, 2], boxes_b[:, 3]

    inter_x1 = np.maximum(ax1[:, None], bx1[None, :])
    inter_y1 = np.maximum(ay1[:, None], by1[None, :])
    inter_x2 = np.minimum(ax2[:, None], bx2[None, :])
    inter_y2 = np.minimum(ay2[:, None], by2[None, :])

    inter_w = np.clip(inter_x2 - inter_x1, 0, None)
    inter_h = np.clip(inter_y2 - inter_y1, 0, None)
    inter = inter_w * inter_h

    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a[:, None] + area_b[None, :] - inter
    return inter / np.clip(union, 1e-8, None)
```

يعيد رقم`(N_a, N_b)`المصفوفة من أجهزة الـ IoU المتزدوجة. استخدمها ضد مربع واحد من الحقيقة الأرضية عن طريق جعل أحد المصفوفات تشكل`(1, 4)`. . .

> عودتي`(N_a, N_b)`                                                                                                                                                                                                                                                              `(1, 4)`形形即可对单个真实框使用──

### الخطوة الثانية: القمع غير القصوى

```python
def nms(boxes, scores, iou_threshold=0.45):
    order = np.argsort(-scores)
    keep = []
    while len(order) > 0:
        i = order[0]
        keep.append(i)
        if len(order) == 1:
            break
        rest = order[1:]
        ious = box_iou(boxes[[i]], boxes[rest])[0]
        order = rest[ious <= iou_threshold]
    return np.array(keep, dtype=np.int64)
```

تحديد النتيجة`O(N log N)`من النوع، ويتطابق سلوك `torchvision.ops.nms`على مدخلات متطابقة.

> 确定性的,排序复杂度 `O(N log N)`, في نفس الإدخال على`torchvision.ops.nms`تصرفات متوافقة

### الخطوة الثالثة: تشفير الصندوق وتفكير

تحويل بين نقاط البيكسل والـ `(tx, ty, tw, th)`أهداف أن الشبكة تتراجع فعلا.

```python
def encode(box_xyxy, cell_x, cell_y, stride, anchor_wh):
    x1, y1, x2, y2 = box_xyxy
    cx = 0.5 * (x1 + x2)
    cy = 0.5 * (y1 + y2)
    w = x2 - x1
    h = y2 - y1
    tx = cx / stride - cell_x
    ty = cy / stride - cell_y
    tw = np.log(w / anchor_wh[0] + 1e-8)
    th = np.log(h / anchor_wh[1] + 1e-8)
    return np.array([tx, ty, tw, th])


def decode(tx_ty_tw_th, cell_x, cell_y, stride, anchor_wh):
    tx, ty, tw, th = tx_ty_tw_th
    cx = (sigmoid(tx) + cell_x) * stride
    cy = (sigmoid(ty) + cell_y) * stride
    w = anchor_wh[0] * np.exp(tw)
    h = anchor_wh[1] * np.exp(th)
    return np.array([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
```

الاختبار: تشفير مربع ثم فك تشفير يجب أن تحصل على شيء قريب جدا من الأصلي (حتى العكس sigmoid ليس قابلا للتحويل بشكل كامل عندما `tx`ليس في النطاق بعد السجماوي).

### الخطوة الرابعة: رأس يولو الحد الأدنى

واحد 1x1 مخزن على خريطة الميزات، وإعادة تشكيل إلى `(B, S, S, num_anchors, 5 + C)`. . .

```python
import torch
import torch.nn as nn

class YOLOHead(nn.Module):
    def __init__(self, in_c, num_anchors, num_classes):
        super().__init__()
        self.num_anchors = num_anchors
        self.num_classes = num_classes
        self.conv = nn.Conv2d(in_c, num_anchors * (5 + num_classes), kernel_size=1)

    def forward(self, x):
        n, _, h, w = x.shape
        y = self.conv(x)
        y = y.view(n, self.num_anchors, 5 + self.num_classes, h, w)
        y = y.permute(0, 3, 4, 1, 2).contiguous()
        return y
```

شكل الخروج: `(N, H, W, num_anchors, 5 + C)`الأبعاد الأخيرة تستمر`[tx, ty, tw, th, obj, cls_0, ..., cls_{C-1}]`. . .

### الخطوة 5: تعيين الحقيقة الأساسية

لكل صندوق حقيقة أساسية، قرر أي`(cell, anchor)`هو المسؤول

```python
def assign_targets(boxes_xyxy, classes, anchors, stride, grid_size, num_classes):
    num_anchors = len(anchors)
    target = np.zeros((grid_size, grid_size, num_anchors, 5 + num_classes), dtype=np.float32)
    has_obj = np.zeros((grid_size, grid_size, num_anchors), dtype=bool)

    for box, cls in zip(boxes_xyxy, classes):
        x1, y1, x2, y2 = box
        cx, cy = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
        gx, gy = int(cx / stride), int(cy / stride)
        bw, bh = x2 - x1, y2 - y1

        ious = np.array([
            (min(bw, aw) * min(bh, ah)) / (bw * bh + aw * ah - min(bw, aw) * min(bh, ah))
            for aw, ah in anchors
        ])
        best = int(np.argmax(ious))
        aw, ah = anchors[best]

        target[gy, gx, best, 0] = cx / stride - gx
        target[gy, gx, best, 1] = cy / stride - gy
        target[gy, gx, best, 2] = np.log(bw / aw + 1e-8)
        target[gy, gx, best, 3] = np.log(bh / ah + 1e-8)
        target[gy, gx, best, 4] = 1.0
        target[gy, gx, best, 5 + cls] = 1.0
        has_obj[gy, gx, best] = True
    return target, has_obj
```

اختيار المرسوم هو "أفضل شكل IoU مع الحقيقة الأرضية"  وكيل رخيصة تتطابق مع مهمة YOLOv2/v3. v5 ولاحقا استخدام استراتيجيات أكثر تطورا (التطابق المرتبط بالمهمة، ديناميكي k) التي تحسين نفس الفكرة.

### الخطوة السادسة: الخسائر الثلاثة

```python
def yolo_loss(pred, target, has_obj, lambda_coord=5.0, lambda_obj=1.0, lambda_noobj=0.5, lambda_cls=1.0):
    has_obj_t = torch.from_numpy(has_obj).bool()
    target_t = torch.from_numpy(target).float()

    # box-regression loss: only on cells with objects
    box_pred = pred[..., :4][has_obj_t]
    box_true = target_t[..., :4][has_obj_t]
    loss_box = torch.nn.functional.mse_loss(box_pred, box_true, reduction="sum")

    # objectness loss
    obj_pred = pred[..., 4]
    obj_true = target_t[..., 4]
    loss_obj_pos = torch.nn.functional.binary_cross_entropy_with_logits(
        obj_pred[has_obj_t], obj_true[has_obj_t], reduction="sum")
    loss_obj_neg = torch.nn.functional.binary_cross_entropy_with_logits(
        obj_pred[~has_obj_t], obj_true[~has_obj_t], reduction="sum")

    # classification loss on cells with objects
    cls_pred = pred[..., 5:][has_obj_t]
    cls_true = target_t[..., 5:][has_obj_t]
    loss_cls = torch.nn.functional.binary_cross_entropy_with_logits(
        cls_pred, cls_true, reduction="sum")

    total = (lambda_coord * loss_box
             + lambda_obj * loss_obj_pos
             + lambda_noobj * loss_obj_neg
             + lambda_cls * loss_cls)
    return total, {"box": loss_box.item(), "obj_pos": loss_obj_pos.item(),
                   "obj_neg": loss_obj_neg.item(), "cls": loss_cls.item()}
```

خمسة مُعايير فائقة التي يُحرم بها كل دراسة "يوولو" أو تُسحفها`lambda_coord=5, lambda_noobj=0.5`يعكس ورقة YOLOv1 الأصلية ومازال يعمل كخفض معقول.

### الخطوة 7: خط أنابيب الإستدلال

فك خيارات الخروج الخام للأسفل، وتطبيق sigmoid/exp، وعتبة على الموضوعية، و NMS.

```python
def postprocess(pred_tensor, anchors, stride, img_size, conf_threshold=0.25, iou_threshold=0.45):
    pred = pred_tensor.detach().cpu().numpy()
    grid_h, grid_w = pred.shape[1], pred.shape[2]
    num_anchors = len(anchors)

    boxes, scores, classes = [], [], []
    for gy in range(grid_h):
        for gx in range(grid_w):
            for a in range(num_anchors):
                tx, ty, tw, th, obj, *cls = pred[0, gy, gx, a]
                score = sigmoid(obj) * sigmoid(np.array(cls)).max()
                if score < conf_threshold:
                    continue
                cls_idx = int(np.argmax(cls))
                cx = (sigmoid(tx) + gx) * stride
                cy = (sigmoid(ty) + gy) * stride
                w = anchors[a][0] * np.exp(tw)
                h = anchors[a][1] * np.exp(th)
                boxes.append([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])
                scores.append(float(score))
                classes.append(cls_idx)

    if not boxes:
        return np.zeros((0, 4)), np.zeros((0,)), np.zeros((0,), dtype=int)
    boxes = np.array(boxes)
    scores = np.array(scores)
    classes = np.array(classes)
    keep = nms(boxes, scores, iou_threshold)
    return boxes[keep], scores[keep], classes[keep]
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.


هذا هو المسار الكامل لتقييم: رأس -> فك -> عتبة -> NMS.




> **【拓展：视觉模型的持续学习】**في بيئة الإنتاج، يتطلب نموذج الرؤية التكيف المستمر مع البيانات الجديدة.

## استخدمها في إطار التنفيذ

`torchvision.models.detection`السفن الكشفية الإنتاجية ذات نفس الهيكل المفاهيمي. تحميل نموذج مدرب مسبقًا يستغرق ثلاثة خطوط.

```python
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2

model = fasterrcnn_resnet50_fpn_v2(weights="DEFAULT")
model.eval()
with torch.no_grad():
    predictions = model([torch.randn(3, 400, 600)])
print(predictions[0].keys())
print(f"boxes:  {predictions[0]['boxes'].shape}")
print(f"scores: {predictions[0]['scores'].shape}")
print(f"labels: {predictions[0]['labels'].shape}")
```

لخطوط استنتاج في الوقت الحقيقي،`ultralytics`(YOLOv8/v9) هو المعيار: `from ultralytics import YOLO; model = YOLO('yolov8n.pt'); model(img)`النموذج يتعامل مع فك التشفير و NMS داخليا ويعود نفسها `boxes / scores / labels`ثلاثية التي بنيتها فوق.

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.




## أرسلها .

هذا الدرس ينتج عن:

- `outputs/prompt-detection-metric-reader.md` إشارة تدور `precision, recall, AP, mAP@0.5:0.95`في صف واحد في التشخيص واحد خط و التجربة التالية الأكثر فائدة.
- `outputs/skill-anchor-designer.md` مهارة التي، نظرا لمجموعة بيانات من مربعات الحقيقة الأساسية، تعمل على k- المتوسط `(w, h)`ويعود مجموعات المرسومات لكل مستوى FPN بالإضافة إلى إحصاءات التغطية التي تحتاجها لتحديد عدد المرسومات المناسبة.

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


## تمارين التدريب

1. **(Easy | 简单)**تنفيذ`box_iou`و أنقلبها ضد`torchvision.ops.box_iou`على 1000 زوج مربع عشوائية. التحقق من أقصى الفرق المطلق هو أقل`1e-6`. . .
    تحقيق `box_iou`وذلك في حالة التحقق من الوصول إلى المراقبة في 1000 على إطار التوقيت، والتحقق من أكبر خطأ < 1e-6:

2. **(Medium | 中等)**الميناء`yolo_loss`إلى نسخة تستخدم `CIoU`فقدان الصندوق بدلا من MSE. أظهر على مجموعة بيانات صناعية 100 صورة أن CIoU يتقارب إلى أفضل mAP@0.5:0.95 النهائي من MSE في نفس عدد من الفترات.
   ستعمل`yolo_loss`改为使用CIoU 框损失(بدل MSE) ، في مجموعة بيانات مركبة يثبت CIoU 收到更高的map──

3. **(Hard | 困难)**تنفيذ استنتاج متعدد المقاييس: إرسال نفس الصورة في ثلاث قرارات من خلال النموذج، وتوحيد توقعات الصندوق، وتشغيل NMS واحد في النهاية. قياس رفع mAP مقابل استنتاج مقياس واحد على مجموعة متواصلة.
   实现多尺度推理: باستخدام ثلاث حلول تمييز الاختبار، 合并预测框后统一做 NMS، قياس مقارنة مع واحد مقياس خريطة 提升──

## شروط رئيسية

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Anchor | "Box prior" | A pre-defined box shape at each grid cell from which the network predicts deltas instead of absolute coordinates | 锚框：预定义的框形状，网络只预测相对于锚框的偏移量 |
| IoU | "Overlap" | Intersection-over-union of two boxes; the universal similarity measure in detection | IoU：交并比，检测中通用的相似度度量 |
| NMS | "Deduplicate" | Greedy algorithm that keeps highest-score predictions and removes overlapping ones above a threshold | NMS：非极大值抑制，去除重复检测框 |
| Objectness | "Is there something here" | Per-anchor, per-cell scalar predicting whether an object is centred in that cell | 置信度/目标性：预测该位置是否有物体 |
| Grid stride | "Downsample factor" | Pixels per grid cell; a 416-px input with a 13-grid head has stride 32 | 网格步长：每个网格单元对应的像素数 |
| mAP | "Mean average precision" | Average of the area under the precision-recall curve, averaged over classes and (for COCO) IoU thresholds | mAP：平均精度均值，检测的核心评估指标 |
| AP@0.5 | "PASCAL VOC AP" | Average precision with IoU threshold 0.5; the lenient version of the metric | AP@0.5：IoU 阈值 0.5 的平均精度（宽松版） |
| mAP@0.5:0.95 | "COCO AP" | Average over IoU thresholds 0.5..0.95 step 0.05; the strict version and current community standard | mAP@0.5:0.95：多个 IoU 阈值的平均（严格版，COCO 标准） |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [YOLOv1: You Only Look Once (Redmon et al., 2016)](https://arxiv.org/abs/1506.02640)ورقة الأساسية كل يوولو منذ ذلك الحين هو تحسين لهذا الهيكل
- [YOLOv3 (Redmon & Farhadi, 2018)](https://arxiv.org/abs/1804.02767) الورقة التي قدمت رؤوس متعددة النطاقات في طراز FPN؛ لا يزال أكثر الرسم البياني وضوحا
- [Ultralytics YOLOv8 docs](https://docs.ultralytics.com) المرجح الحالي للإنتاج؛ يغطي تنسيقات مجموعة البيانات، وتكثيفات، وصفات التدريب
- [The Illustrated Guide to Object Detection (Jonathan Hui)](https://jonathan-hui.medium.com/object-detection-series-24d03a12f904)أفضل جولة بسيطة باللغة الإنجليزية في حديقة الحيوان الكشف الكاملة؛ لا تقدر بثمن لفهم كيفية ارتباط DETR، RetinaNet، FCOS، وYOLO
