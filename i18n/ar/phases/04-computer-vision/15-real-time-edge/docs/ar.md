# رؤية في الوقت الحقيقي  نشر الحافة  في الوقت الحقيقي                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

> استنتاج الحافة هو تخصص الحصول على نموذج 90 دقيقة ليتم تشغيله بسرعة 30 fps على جهاز لديه 2 جيجابايت من ذاكرة الوصول الذكي. يتم تداول كل نقطة مئوية من الدقة مقابل ملثنيات من التأخير.

> **【中文解读】**التفكير الحدودي هو فن توازن: جعل نموذج 90% ٪ دقة يعمل على 30fps على أجهزة 2GB فقط من الاحتفاظ بالخزنة الداخلية.

> **【拓展：边缘 AI 的应用】**边缘部署在智能手机 (?? 人脸解锁,拍照美化) 无人机 (?? 无人机) 实时目标检测) 工业物联网 (?? 缺陷检测) 及自动驾驶 (?? 车载推理) 中至关重要──MobileNet、YOLO-nano、EfficientNet 是常见的轻量级模型──

**Type:** Learn + Build | **类型:** 学习 + 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 04 (Image Classification), Phase 10 Lesson 11 (Quantization) | **前置知识:** Phase 4 Lesson 04（图像分类），Phase 10 Lesson 11（量化）
**Time:** ~75 minutes | **时间:** ~75 分钟

## أهداف التعلم

- قياس تأخير الإستنتاجات، الذكرى الذروة، والمدخل لأي نموذج PyTorch، وقراءة FLOPs / Params / تأخير التداول
- قم بتقييم نموذج الرؤية إلى INT8 باستخدام كمية PyTorch بعد التدريب وتحقق من فقدان الدقة < 1٪
- تصدير إلى ONNX وترتيب مع ONNX Runtime أو TensorRT؛ أسمائ ثلاثة أخطاء التصدير الأكثر شيوعا وتصحيحاتها
- شرح متى يجب اختيار MobileNetV3، EfficientNet-Lite، ConvNeXt-Tiny، أو MobileViT لقيود الحافة

> **【中文解读】**يُدعى أهداف التعلم المفردة التي يجب أن تتحكم فيها بعد الانتهاء من الدورة.


## المشكلة المشكلة المشكلة

نموذج رؤية في وقت التدريب هو وحش نقطة عائمة. 100 مليون ملاميتر، 10 GFLOPs لكل مرور إلى الأمام، 2 جيجابايت من VRAM. لا شيء من ذلك يناسب هاتف، وحدة إعلامية السعة في السيارة، وكاميرا صناعية، أو طائرة بدون طيار. شحن نظام رؤية يعني تكييف التنبؤات نفسها في ميزانية أقل من 100 مرة.

> النموذج البصري في التدريب هو عدد الوحوش البالغ عددها 1 مليار عنصر، في كل مرة يتنقل نحو 10 GFLOPs، 2 جيجابايت 显存.

تقوم ثلاث أزرار معظم العمل: اختيار النموذج (معمارة أصغر بنفس الوصفة) ، والكمية (INT8 بدلا من FP32) ، وزمنية تشغيل الاستنتاج (ONNX Runtime ، TensorRT ، Core ML ، TFLite). الحصول على الحق هو الفرق بين عرض تجريبي يعمل على محطة عمل ومنتج يتم شحن عليه على شكل كاميرا بقيمة 30 دولار.

> ثلاث ثورات عملت معظم العمل: نموذج اختيار (مجموعة صغيرة من نفس المخطط) 量化 (INT8 替代 FP32) و التقييم في الوقت الذي يعمل فيه (ONNX Runtime  TensorRT  Core ML  TFLite)  صحيح استخدامها في العروض التي تعمل على محطة العمل والفاصل بين المنتجات التي يتم تسليمها على وحدات كاميرا 30 美元 

هذه الدروس تعيين الانضباط القياس أولا (لا يمكنك تحسين ما لا يمكنك قياسه) ، ثم يمشي على الأزرار الثلاثة. الهدف ليس تعلم كل حافة تشغيل الوقت ولكن لمعرفة ما هي الرافعات الموجودة وكيفية التحقق من كل واحد يفعل ما تعتقد.

> هذا الدرس أولاً يُنشئ قوانين القياس ((أنت لا تستطيع تحسين ما لا تستطيع قياسه) ، ثم يمر عبر ثلاث دورات. الغرض ليس التعلم عندما تعمل كل حافة، بل معرفة أي رصيدات و كيفية تحديد ما يفعله كل رصيد.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


### الميزانيات الثلاثة

```mermaid
flowchart LR
    M["Model"] --> LAT["Latency<br/>ms per image"]
    M --> MEM["Memory<br/>peak MB"]
    M --> PWR["Power<br/>mJ per inference"]

    LAT --> SHIP["Ship / no-ship<br/>decision"]
    MEM --> SHIP
    PWR --> SHIP

    style LAT fill:#fecaca,stroke:#dc2626
    style MEM fill:#fef3c7,stroke:#d97706
    style PWR fill:#dbeafe,stroke:#2563eb
```

- **Latency**: p50، p95، p99، متوسط p50 فقط يخفي سلوك الذيل الذي يهم للأنظمة في الوقت الحقيقي.
  中文翻译:**延迟**p50、p95、p99── فقط انظر p50  متوسط القيمة سوف تختفي عن النظام الحقيقي
- **Peak memory**: أقصى ما يراه الجهاز، وليس متوسط حالة ثابتة.
  中文翻译:**峰值内存**: أجهزة أصل أقصى قيمة، ليس متوسط مستقر.
- **Power / energy**: مليليوجول لكل استنتاج على جهاز يعمل بطارية. غالباً ما يتم استغلالها بواسطة وقت استخدام CPU/GPU *.
  中文翻译:**功耗/能量**: عدد المليوجوزات التي يتم تقديمها في كل مرة على جهاز إمدادات الكهرباء.

جدول (النموذج، التأخير، الذاكرة، الدقة) هو ما يتم اتخاذ قرار الحافة من. يتم قياس كل خلية على الجهاز المستهدف، وليس محطة العمل.

> تمت إعدادات (模型, 延迟, 内存, 精度) على أساس قرارات التنفيذ الحدودي.

### تأديب القياس

ثلاثة قواعد يجب أن تتبعها كل ملف حافة:

> يجب أن يتبع كل تحليل للأداء الحدودي ثلاثة قواعد:

1. **Warm up**النموذج مع 5-10 مرّات مخففة إلى الأمام قبل قياس. الكاشوف الباردة وتجميع JIT تنتج أرقام أولية غير ممثلة.
   中文翻译:**预热** قياس قبل استخدام 5-10 مرات افتراضية قبل الوساطة قبل الاحتفاظ والخزانة الجوية 编译会产生不代表性的初始数据──
2. **Synchronise**عبء عمل GPU مع `torch.cuda.synchronize()`قبل وبعد الكتلة المحددة بالتوقيت. بدون هذا تقيس إرسال النواة، وليس تنفيذ النواة.
   中文翻译:**同步** في المقاييس `torch.cuda.synchronize()`مع متواصلة GPU 工作负载──否则你测量是内核调度,而不是内核执行──
3. **Fix input sizes**التأخير على 224 × 224 ليس التأخير على 512 × 512.
   中文翻译:**固定输入尺寸** استخدام تصميم الإنتاج ∙ 224 × 224 ∙ التأخير العلوي ليس مساوياً لـ 512 × 512 ∙ التأخير العلوي

### الـ "FLOPs" كوكيل

FLOPs (عمليات نقطة عائمة حسب الاستنتاج) هو وكيل رخيصة ، مستقلة عن الجهاز للمقارنة مع الهندسة المعمارية ، مفيدة كمقارنة حائطية مطلقة. يمكن أن يكون نموذجًا لديه 10٪ من FLOPs أسرع مرتين في الممارسة لأنه يستخدم عمليات صديقة للأجهزة (التجمعات العميقة تقوم بتجميع جيد ، والتصالات الكبيرة 7x7 لا تفعل ذلك).

> FLOPs (((حسابات النقاط المتفوقة في كل محاكاة) هي مؤشر مؤخرة غير متعلقة بالأجهزة.

القاعدة: استخدام FLOPs للبحث عن الهندسة المعمارية، استخدام تأخر على الجهاز لقرارات التنفيذ.

> قانون: استخدام FLOPs لتحقيق البحث في البناء، استخدام التأخير على الجهاز لتنفيذ قرارات.

### الكمية في فقرة واحدة

استبدل وزنات FP32 وتفعيلاتها بـ INT8. انخفض حجم النموذج 4x، انخفض عرض النطاق النطاق 4x، انخفض الحساب 2-4x على الأجهزة التي لديها نواة INT8 (كل SoC المحمول الحديث، كل GPU NVIDIA مع أجزاء تنسور). فقدان الدقة في مهام الرؤية عادة 0.1-1 نقاط مئوية مع الكمية ثابتة بعد التدريب.

> لنقل FP32  الوزن والتحريك بدلاً من INT8。 نموذج الحجم قد انخفض 4 مرات، وتخفيض النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق النطاق الن

الأنواع:

> 类型:

- **Dynamic** الوزن الكم إلى INT8، تنشيطات محاسبة في FP. سهلة، تسريع صغيرة.
  中文翻译:**动态** الوزن المفيد لـ INT8، القيمة النشطة باستخدام FP 计算──简单,加速有限──
- **Static (post-training)** الوزن الكم + نطاق تنشيط التصفية على مجموعة تصويب صغيرة. أسرع بكثير من الديناميكية.
  中文翻译:**静态（训练后）**量化权重 + 在小校准集上校准激活范围──比动态快得多──
- **Quantisation-aware training (QAT)** محاكاة الكمية أثناء التدريب حتى يتعلم النموذج حولها.
  中文翻译:**量化感知训练（QAT）** تدريب  تمثيل  تطبيق 

بالنسبة للرؤية، فإن الكمية الدقيقة بعد التدريب توفر 95٪ من الفائدة مع 5٪ من الجهد. استخدم QAT فقط عندما يكون فقدان الدقة من PTQ غير مقبول.

> للحصول على 95% من المكاسب على المهام البصرية، مع محاولة 5٪ من تقييم الحالة بعد التدريب.

### الحصص والنزيف

- **Pruning** إزالة الأوزان غير المهمة (بناء على الكبيرة) أو القنوات (مهيكلة). يعمل بشكل جيد على النماذج المفرطة المعايير؛ أقل فائدة على الهندسة المعمارية المتكاملة بالفعل.
  中文翻译:**剪枝** الحذف غير مهم الوزن (بناء على الامتداد) أو الممر (بناء)  المهارات (بناء) 
- **Distillation** تدريب الطالب الصغير على تقليد منطقات المعلم الكبير. غالبًا ما يسترد معظم دقة المفقودة عن طريق تقليص النموذج. معيار لنماذج الحافة الإنتاجية.
  中文翻译:**蒸馏** تدريب نموذج صغير  الطلاب 模仿大模型  معلم  منطقات  عموما يمكن استعادة معظم دقة فقدان الموديل الصغير 

### توقيت التخلص

- **PyTorch eager** بطيئة، لا تستخدم للتنفيذ فقط
  中文翻译:**PyTorch eager**慢, ليس لتنفيذها.
- **TorchScript** إرث.`torch.compile`و صادرات ONNX
  中文翻译:**TorchScript**遗留方案──已被 `torch.compile`و ONNX 导出取代。
- **ONNX Runtime**الوقت المباشر المحايد، CPU، CUDA، CoreML، TensorRT، OpenVINO كل لديهم مزودي ONNX. ابدأ هنا.
  中文翻译:**ONNX Runtime**中性运行时──CPU、CUDA、CoreML、TensorRT、OpenVINO 都有ONNX 提供者──从这里开始──
- **TensorRT** محفز NVIDIA. أفضل تأخير على GPUs NVIDIA (محطة عمل وجيتسون). يدمج مع ONNX Runtime أو مستقل.
  中文翻译:**TensorRT**NVIDIA 的编译器──在NVIDIA GPU(工作站和Jetson) 上延迟最低──
- **Core ML** وقت تشغيل أبل لـ iOS/macOS. احتياجات `.mlmodel`أو`.mlpackage`. . .
  中文翻译:**Core ML**Apple's iOS/macOS 运行时──需要 `.mlmodel`أو`.mlpackage`.
- **TFLite** وقت تشغيل جوجل لـ Android/ARM. احتياجات `.tflite`. . .
  中文翻译:**TFLite**Google Android/ARM 运行时──需要 `.tflite`.
- **OpenVINO** وقت تشغيل إنتل لـ CPU/VPU. احتياجات `.xml`+ `.bin`. . .
  中文翻译:**OpenVINO**إنطيل CPU / VPU 运行时──需要 `.xml`+ `.bin`.

في الممارسة العملية: تصدير PyTorch -> ONNX -> اختيار وقت تشغيل الهدف. ONNX هي اللغة الفرنسية.

> 实践中:导出 PyTorch -> ONNX -> 选择目标运行时。ONNX 是通用语言。

### محركات تحديد المعماريات

| Budget | Model | Why |
|--------|-------|-----|
| < 3M params | MobileNetV3-Small | Compiles everywhere, good baseline |
| 3-10M | EfficientNet-Lite-B0 | Best accuracy per param on TFLite |
| 10-20M | ConvNeXt-Tiny | Best accuracy-per-param, CPU-friendly |
| 20-30M | MobileViT-S or EfficientViT | Transformer with ImageNet accuracy |
| 30-80M | Swin-V2-Tiny | If stack supports window attention |

قم بتحديد كل هذه إلى INT8 ما لم يكن لديك سبب محدد لعدم القيام بذلك.

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

> **【拓展：工业部署中的视觉系统】**في التوزيع الصناعي الواقعي، تحتاج النموذج المرئي إلى النظر في التفكير في التأجيل، والنموذج الكبير، والجهاز الحدودي الملائمة وغيرها من المشاكل.

> **【拓展：数据标注与质量】** تأثير المهام المرئية يعتمد على جودة البيانات المعلنة.‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬




## بناء ذلك تحرك لتحقيق
```figure
cnn-param-count
```

## بناءها

### الخطوة 1: قياس التأخير بشكل صحيح

```python
import time
import torch

def measure_latency(model, input_shape, device="cpu", warmup=10, iters=50):
    model = model.to(device).eval()
    x = torch.randn(input_shape, device=device)
    with torch.no_grad():
        for _ in range(warmup):
            model(x)
        if device == "cuda":
            torch.cuda.synchronize()
        times = []
        for _ in range(iters):
            if device == "cuda":
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            model(x)
            if device == "cuda":
                torch.cuda.synchronize()
            times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    return {
        "p50_ms": times[len(times) // 2],
        "p95_ms": times[int(len(times) * 0.95)],
        "p99_ms": times[int(len(times) * 0.99)],
        "mean_ms": sum(times) / len(times),
    }
```

إثارة، التزامن، الاستخدام`time.perf_counter()`-أبلغ عن النسب، وليس فقط السوء

> 预热、同步、使用 `time.perf_counter()`                                                                                                                                                                                                                                                              

### الخطوة الثانية: حسابات المعلمات و FLOP

```python
def parameter_count(model):
    return sum(p.numel() for p in model.parameters())

def flops_estimate(model, input_shape):
    """
    Rough FLOP count for a conv/linear-only model. For production use `fvcore` or `ptflops`.
    """
    total = 0
    def conv_hook(m, inp, out):
        nonlocal total
        c_out, c_in, kh, kw = m.weight.shape
        h, w = out.shape[-2:]
        total += 2 * c_in * c_out * kh * kw * h * w
    def linear_hook(m, inp, out):
        nonlocal total
        total += 2 * m.in_features * m.out_features
    hooks = []
    for m in model.modules():
        if isinstance(m, torch.nn.Conv2d):
            hooks.append(m.register_forward_hook(conv_hook))
        elif isinstance(m, torch.nn.Linear):
            hooks.append(m.register_forward_hook(linear_hook))
    model.eval()
    with torch.no_grad():
        model(torch.randn(input_shape))
    for h in hooks:
        h.remove()
    return total
```

للاستخدام في المشاريع الحقيقية`fvcore.nn.FlopCountAnalysis`أو`ptflops`؛ يتعاملون مع كل نوع من وحدات الدواء بشكل صحيح.

> حقا المشاريع الاستخدام`fvcore.nn.FlopCountAnalysis`أو`ptflops`؛ يمكنها معالجة كل نوع من الطرازات بشكل صحيح

### الخطوة الثالثة: الكمية الدقيقة بعد التدريب

```python
def quantise_ptq(model, calibration_loader, backend="x86"):
    import torch.ao.quantization as tq
    model = model.eval().cpu()
    model.qconfig = tq.get_default_qconfig(backend)
    tq.prepare(model, inplace=True)
    with torch.no_grad():
        for x, _ in calibration_loader:
            model(x)
    tq.convert(model, inplace=True)
    return model
```

ثلاث خطوات: تكوين، وإعداد (إدراج المراقبين) ، وتصفية مع البيانات الحقيقية، وتحويل (التضخم + الكمية).`Conv -> BN -> ReLU`-> `ConvBnReLU`) الذي`torch.ao.quantization.fuse_modules`اليدين

> ثلاث مراحل: تخصيص : إعداد : إدخال المراقب : استخدام المعلومات الحقيقية : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص : تخصيص :`Conv -> BN -> ReLU`-> `ConvBnReLU`(`torch.ao.quantization.fuse_modules`إصلاح هذه القضية

### الخطوة الرابعة: تصدير إلى ONNX

```python
def export_onnx(model, sample_input, path="model.onnx"):
    model = model.eval()
    torch.onnx.export(
        model,
        sample_input,
        path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
        opset_version=17,
    )
    return path
```

`opset_version=17`هو الاختلالات الآمنة في عام 2026`dynamic_axes`يسمح لك بتشغيل نموذج ONNX مع حجم اللحظة التعسفي.

> `opset_version=17`هو 2026 سنة الأمن المُعتمدة.`dynamic_axes`允许ONNX 模型以任意批量大小运行──

### الخطوة 5: قم بتحديد النظم ومقارنتها

```python
import torch.nn as nn
from torchvision.models import mobilenet_v3_small

def compare_regimes():
    model = mobilenet_v3_small(weights=None, num_classes=10)
    params = parameter_count(model)
    flops = flops_estimate(model, (1, 3, 224, 224))
    lat_fp32 = measure_latency(model, (1, 3, 224, 224), device="cpu")
    print(f"FP32 MobileNetV3-Small: {params:,} params  {flops/1e9:.2f} GFLOPs  "
          f"p50={lat_fp32['p50_ms']:.2f}ms  p95={lat_fp32['p95_ms']:.2f}ms")
```

إشغال نفس الوظيفة`resnet50`،`efficientnet_v2_s`و`convnext_tiny`ولديك جدول المقارنة الذي تحتاجه لقرار نشر.

> على`resnet50`.`efficientnet_v2_s`和 `convnext_tiny`运行 نفس الوظيفة، أنت حصلت على النسبة المطلوبة لتطبيق القرارات

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.





> **【拓展：视觉模型的持续学习】**في بيئة الإنتاج، يتطلب نموذج الرؤية التكيف المستمر مع البيانات الجديدة.

## استخدمها في إطار التنفيذ

تتقارب كومات الإنتاج على أحد ثلاثة مسارات:

- **Web / serverless**: PyTorch -> ONNX -> ONNX Runtime (مدونة CPU أو CUDA). أسهل، جيد بما فيه الكفاية بالنسبة لمعظم.
- **NVIDIA edge (Jetson, GPU server)**: PyTorch -> ONNX -> TensorRT. أفضل تأخير، أكبر جهد هندسي.
- **Mobile**: PyTorch -> ONNX -> Core ML (iOS) أو TFLite (Android).

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


للقياس`torch-tb-profiler`،`nvprof`- لا ، لا`nsys`و الأدوات على macOS تعطى تفكيكات طبقة بعد طبقة. `benchmark_app`(OpenVINO) و `trtexec`(تنسور آر تي) أعطوا أرقام CLI مستقلة.



## أرسلها .

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


هذا الدرس ينتج عن:

- `outputs/prompt-edge-deployment-planner.md` استشارة تحدد العمود الفقري، استراتيجية الكمية، وقتا تشغيل مع إعطاء جهاز الهدف و SLA التأخير.
- `outputs/skill-latency-profiler.md` مهارة تكتب نصًا كاملًا للتقييمات التأخيرية مع تسخين التزامنا والرسومات وتتبع الذاكرة.

## تمارين التدريب

1. **(Easy)**قياس p50 تأخير ل `resnet18`،`mobilenet_v3_small`،`efficientnet_v2_s`و`convnext_tiny`في 224 × 224 على CPU. إبلغ عن الجدول وتحديد أي الهندسة المعمارية لديها أفضل دقة في كل أجزاء.
2. **(Medium)**تطبيق الكميات الدقيقة بعد التدريب على `mobilenet_v3_small`. إبلاغ عن فقدان تأخر FP32 مقابل INT8 ودقة على مجموعة فرعية من CIFAR-10 أو ما شابه ذلك.
3. **(Hard)**الصادرات`convnext_tiny`إلى ONNX، إشغله`onnxruntime`مع`CPUExecutionProvider`و قم بتقارن التأخير مع خط أساس PyTorch الإهتمام. حدد الطبقة الأولى حيث ONNX Runtime أسرع و اشرح لماذا.

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Latency | "How fast" | Time from input to output; p50/p95/p99 percentiles, not mean |
| FLOPs | "Model size" | Floating-point ops per forward pass; rough proxy for compute cost |
| INT8 quantisation | "8-bit" | Replace FP32 weights/activations with 8-bit integers; ~4x smaller, 2-4x faster |
| PTQ | "Post-training quantisation" | Quantise a trained model without retraining; easy, usually enough |
| QAT | "Quantisation-aware training" | Simulate quantisation during training; best accuracy, requires labelled data |
| ONNX | "The neutral format" | Model exchange format supported by every mainstream inference runtime |
| TensorRT | "NVIDIA compiler" | Compiles ONNX into an optimised engine for NVIDIA GPUs |
| Distillation | "Teacher -> student" | Train a small model to mimic a big model's logits; recovers most lost accuracy |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [EfficientNet (Tan & Le, 2019)](https://arxiv.org/abs/1905.11946) التوسع المركب لهياكل معمارية فعالة
- [MobileNetV3 (Howard et al., 2019)](https://arxiv.org/abs/1905.02244) الهندسة المعمارية المتنقلة أولاً مع h-swish و squeeze-excite
- [A Practical Guide to TensorRT Optimization (NVIDIA)](https://developer.nvidia.com/blog/accelerating-model-inference-with-tensorrt-tips-and-best-practices-for-pytorch-users/) كيفية الحصول على أرقام التدفق في الورقة
- [ONNX Runtime docs](https://onnxruntime.ai/docs/) تعريف المعدلات، تحسين الرسم البياني، اختيار المقدمين
