# بناء خط أنابيب الرؤية الكاملة  Capstone  بناء كامل 视觉流水线  毕业项目

> نظام رؤية الإنتاج هو سلسلة من النماذج والقواعد التي تم اختراقه بعقود البيانات.

> **【中文解读】**النظام البصري للقيام بالإنتاج هو سلسلة من النماذج والقواعد المتصلة من خلال اتفاقيات البيانات.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lessons 01-15 | **前置知识:** Phase 4 Lessons 01-15
**Time:** ~120 minutes | **时间:** ~120 分钟

## أهداف التعلم

- تصميم خط أنابيب رؤية الإنتاج التي تكتشف الأشياء وتصنفها وتصدر JSON مهيكلة  مع كل مسار فشل يتم التعامل معه
- توصيل جهاز كشف (Mask R-CNN أو YOLO) ، وصف (ConvNeXt-Tiny) ، وعقد البيانات (Pydantic) إلى خدمة واحدة
- قم بتحديد خط الأنابيب من نهاية إلى نهاية وتحديد العنق الزجاجة الأولى (عادةً معالجة مسبقة، ثم الكاشف)
- إرسال خدمة FastAPI الحد الأدنى التي تقبل تحميل الصور وتشغيل خط الأنابيب وتعطي الكشفات مع التصنيفات

> **【中文解读】**يُدعى أهداف التعلم المفردة التي يجب أن تتحكم فيها بعد الانتهاء من الدورة.


## المشكلة المشكلة المشكلة

نموذج الرؤية الفردية مفيدة؛ منتجات الرؤية هي سلسلة منها. مراجعة رف التجزئة هي كاشف مزيد من تصنيف المنتج مزيد من خط أنابيب OCR السعر. القيادة الذاتية هي كاشف 2D مزيد من كاشف 3D مزيد من قطعة مزيد من متابعة مزيد من خطط.

> 单个视觉模型有用; 视觉产品是它们的链条;;零售货架审计是检测器加产品分类器加价 OCR 流水线;;自动驾驶是2D检测器加3D检测器加分器加跟踪器加规划器;;医疗预是分器加区域分类器加临床 UI;;

إن توصيل هذه السلاسل هو الجزء الذي يفصل نموذج ML عن منتج. كل واجهة بين النماذج هي مكان جديد للخطأ. كل تحويل منسجم، كل قياس، كل تحويل حجم القناع هو مرشح لفشل صامت. خط أنابيب قوي بقدر ضعف واجهته.

> 连接这些链条是将ML原型与产品区分开放的部分―― كل واجهة بين النموذج هي نقطة جديدة للخطأ―― كل محرك تغيير٬ كل إعادة التأثير٬ كل تخفيض المظلة هي المرشحين الفاشل الصمت٬ قوته تعتمد على أضعف واجهة――

هذه الحجر النهائي يضع الحد الأدنى من خط الأنابيب القابلة للتطبيق: الكشف + التصنيف + الخروج المهيكلي + طبقة الخدمة. كل شيء آخر في الفتحات في المرحلة 4 في هذا العظم: تبادل Mask R-CNN لYOLOv8, إضافة رأس OCR, إضافة فرع التقسيم, إضافة متابعة. الهندسة المعمارية مستقرة؛ قطع قابلة للتشبيك.

> هذا المشروع التخرج يحتوي على الحد الأدنى من التدفقات المياهية: الاختبار + التقسيم + الخروج المهيكلي + مستوى الخدمة.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


### خط الأنابيب

```mermaid
flowchart LR
    REQ["HTTP request<br/>+ image bytes"] --> LOAD["Decode<br/>+ preprocess"]
    LOAD --> DET["Detector<br/>(YOLO / Mask R-CNN)"]
    DET --> CROP["Crop + resize<br/>each detection"]
    CROP --> CLS["Classifier<br/>(ConvNeXt-Tiny)"]
    CLS --> AGG["Aggregate<br/>detections + classes"]
    AGG --> SCHEMA["Pydantic<br/>validation"]
    SCHEMA --> RESP["JSON response"]

    REQ -.->|error| RESP

    style DET fill:#fef3c7,stroke:#d97706
    style CLS fill:#dbeafe,stroke:#2563eb
    style SCHEMA fill:#dcfce7,stroke:#16a34a
```

سبعة مراحل. المرحلتين النموذجية مكلفة؛ الخمسة الأخرى هي حيث يعيش الحشرات.

> 七阶段── دو مرحلة نموذجية مكلفة؛ والباقي خمسة مرحلة هي حفرة الحشرات 藏身之处──

### عقود البيانات مع Pydantic

كل حدود نموذج تصبح كائنًا مكتوبًا، وهذا يحول الفشل الصامت إلى الفشل الصاخب.

> كل نموذج حافة يصبح كائن من نوعها.

```
Detection(
    box: tuple[float, float, float, float],   # (x1, y1, x2, y2), absolute pixels
    score: float,                              # [0, 1]
    class_id: int,                             # from detector's label map
    mask: Optional[list[list[int]]],           # RLE-encoded if present
)

PipelineResult(
    image_id: str,
    detections: list[Detection],
    classifications: list[Classification],
    inference_ms: float,
)
```

عندما يعيد جهاز الكشف الصناديق في`(cx, cy, w, h)`بدلاً من`(x1, y1, x2, y2)`، تفشل تصحيح (بيدانتيك) في الحدود وتكتشف فوراً بدلاً من تحديد المحاصيل التي تعود بهدوء إلى مناطق فارغة

> عندما تستمر الاختبار`(cx, cy, w, h)`و لا`(x1, y1, x2, y2)`عندما يختصر الصفوف، فإن التحقق من Pydantic يفشل في الحدود، يمكنك أن تجد المشكلة على الفور، بدلا من التجربة للقطعة عندما تجد أنها ستعود بسكون إلى المنطقة الفارغة.

### حيث يذهب التأخير

ثلاثة حقائق موجودة في كل خط أنبوب الرؤية تقريبا:

> تقريبا كل مشاهدة تتكون من ثلاثة حقائق:

1. **Preprocessing is often the biggest single block.**فك الفاتورة JPEG، تحويل المساحات اللونية، إعادة الحجم  هذه مربوطة مع المعالجة المركزية وسهلة للنسيان.
   中文翻译:**预处理通常是最大的单一开销。**解码 JPEG 转换色空间 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放 缩放
2. **The detector dominates GPU time.**70-90٪ من وقت GPU في الكشف الأمامية.
   中文翻译:**检测器占据 GPU 时间的主导。**70-90% من الوقت المخصص لـ GPU في الاختبار
3. **Postprocessing (NMS, RLE encode/decode) is cheap on GPU, expensive on CPU.**دائماً أظهري مع الهدف الفعلي
   中文翻译:**后处理（NMS、RLE 编解码）在 GPU 上便宜，在 CPU 上昂贵。**دائماً في الهدف الفعلي التحليل

معرفة التوزيع هو ما يجعل التحسين قائمة أولويات.

> معرفة حالة التوزيع لتصبح تحسيناً في قائمة الأولويات

### أساليب الفشل

- **Empty detections**عُد قائمة فارغة، لا تتعطل.
  中文翻译:**空检测结果** عودة إلى قائمة空, لا تنهار ‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬
- **Out-of-bounds boxes** التمسك بحجم الصورة قبل الحصاد.
  中文翻译:**越界框**قطع قبل الحد من حجم الصورة
- **Tiny crops** تخطي التصنيف للصناديق الصغيرة من أدنى مدخل للمصنف.
  中文翻译:**微小裁剪** قفز فوق الصفوف الأدنى للدخول
- **Corrupt upload** 400 رد مع رمز خطأ محدد، وليس 500.
  中文翻译:**损坏的上传** أعود مع خطأ محدد 400 رد فعل، وليس 500 ‬
- **Model load failure** فشل في بدء الخدمة، وليس عند الطلب الأول.
  中文翻译:**模型加载失败**فاشل في بداية الخدمة وليس في أول طلب

خط إنتاج يدير كل هذه دون كتابة عادي `try/except`كل فشل يحصل على رمز معين ورد

> إنتاج درجة تدفق المياه التعامل مع كل حالة لا حاجة لإخفاء النوع العام الفاشل`try/except`كل فشل له اسم و رد

### التجميع

خدمة الإنتاج تخدم العديد من العملاء. الكشف عن المجموعات والتصنيفات عبر الطلبات تضاعف التنفيذ. التنازل: تأخر إضافي من انتظار المجموعة لملء. الإعداد النموذجي: جمع الطلبات لمدة تصل إلى 20ms ، المجموعة معا ، المعالجة ، توزيع الاستجابات. `torchserve`و`triton`القيام بذلك بشكل طبيعي؛ الخدمات الصغيرة مع الحمل المتوقع يرتدي ميكرو-باتشير الخاص بها.

> خدمات الإنتاج في نفس الوقت خدمة العديد من العملاء. التداولات: التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، التسجيلات، والسجيلات، والسجيلات، والسجيلات، والسجيلات،ات،ات.`torchserve`和 `triton`أساسية دعم؛ تحميل قابل للتنبؤ الخدمة الصغيرة يمكن أن تحقق ذاتيا معالجة الجمعية الصغيرة.

> **【拓展：工业部署中的视觉系统】**في التوزيع الصناعي الواقعي، تحتاج النموذج المرئي إلى النظر في التفكير في التأجيل، والنموذج الكبير، والجهاز الحدودي الملائمة وغيرها من المشاكل.

> **【拓展：数据标注与质量】** تأثير المهام المرئية يعتمد على جودة البيانات المعلنة.‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

> **【拓展：合成数据与数据增强】**عندما تكون البيانات الحقيقية غير كافية، فإن البيانات المكوّنة (مثل Blender  Unity 染) و زيادة البيانات (مثل قاعدة الملفات) هي استراتيجيات فعالة اثنين.




## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

```figure
v4-vision-pipeline
```

## بناءها

### الخطوة الأولى: عقود البيانات

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

class Detection(BaseModel):
    box: Tuple[float, float, float, float]
    score: float = Field(ge=0, le=1)
    class_id: int = Field(ge=0)
    mask_rle: Optional[str] = None


class Classification(BaseModel):
    detection_index: int
    class_id: int
    class_name: str
    score: float = Field(ge=0, le=1)


class PipelineResult(BaseModel):
    image_id: str
    detections: List[Detection]
    classifications: List[Classification]
    inference_ms: float
```

خمس ثوانٍ من الرمز يُوفّر ساعة من التحليل على أي خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط خط

> كود خمس ثواني يمكنه انقاذ أي تدفقات صارمة على خط المياه

### الخطوة الثانية: فئة خط أنابيب أدنى

```python
import time
import numpy as np
import torch
from PIL import Image

class VisionPipeline:
    def __init__(self, detector, classifier, class_names,
                 device="cpu", min_crop=32):
        self.detector = detector.to(device).eval()
        self.classifier = classifier.to(device).eval()
        self.class_names = class_names
        self.device = device
        self.min_crop = min_crop

    def preprocess(self, image):
        """
        image: PIL.Image or np.ndarray (H, W, 3) uint8
        returns: CHW float tensor on device
        """
        if isinstance(image, Image.Image):
            image = np.asarray(image.convert("RGB"))
        tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        return tensor.to(self.device)

    @torch.no_grad()
    def detect(self, image_tensor):
        return self.detector([image_tensor])[0]

    @torch.no_grad()
    def classify(self, crops):
        if len(crops) == 0:
            return []
        batch = torch.stack(crops).to(self.device)
        logits = self.classifier(batch)
        probs = logits.softmax(-1)
        scores, cls = probs.max(-1)
        return list(zip(cls.tolist(), scores.tolist()))

    def run(self, image, image_id="anonymous"):
        t0 = time.perf_counter()
        tensor = self.preprocess(image)
        det = self.detect(tensor)

        crops = []
        detections = []
        valid_indices = []
        for i, (box, score, cls) in enumerate(zip(det["boxes"], det["scores"], det["labels"])):
            x1, y1, x2, y2 = [max(0, int(b)) for b in box.tolist()]
            x2 = min(x2, tensor.shape[-1])
            y2 = min(y2, tensor.shape[-2])
            detections.append(Detection(
                box=(x1, y1, x2, y2),
                score=float(score),
                class_id=int(cls),
            ))
            if (x2 - x1) < self.min_crop or (y2 - y1) < self.min_crop:
                continue
            crop = tensor[:, y1:y2, x1:x2]
            crop = torch.nn.functional.interpolate(
                crop.unsqueeze(0),
                size=(224, 224),
                mode="bilinear",
                align_corners=False,
            )[0]
            crops.append(crop)
            valid_indices.append(i)

        class_preds = self.classify(crops)

        classifications = []
        for valid_idx, (cls_id, cls_score) in zip(valid_indices, class_preds):
            classifications.append(Classification(
                detection_index=valid_idx,
                class_id=int(cls_id),
                class_name=self.class_names[cls_id],
                score=float(cls_score),
            ))

        return PipelineResult(
            image_id=image_id,
            detections=detections,
            classifications=classifications,
            inference_ms=(time.perf_counter() - t0) * 1000,
        )
```

كل واجهة يتم كتابتها. كل مسار فشل لديه قرار معين للتعامل معه.

> كل اتصال من نوعها. كل طريق فشل له قرارات معالجة واضحة.

### الخطوة الثالثة: قم بتشغيل جهاز كشف ومرسوم

```python
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2
from torchvision.models import convnext_tiny

# Use ImageNet-pretrained weights for a realistic pipeline without training
detector = maskrcnn_resnet50_fpn_v2(weights="DEFAULT")
classifier = convnext_tiny(weights="DEFAULT")
class_names = [f"imagenet_class_{i}" for i in range(1000)]

pipe = VisionPipeline(detector, classifier, class_names)

# Smoke test with a synthetic image
test_image = (np.random.rand(400, 600, 3) * 255).astype(np.uint8)
result = pipe.run(test_image, image_id="demo")
print(result.model_dump_json(indent=2)[:500])
```

### الخطوة الرابعة: خدمة FastAPI

```python
from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO

app = FastAPI()
pipe = None  # initialised on startup

@app.on_event("startup")
def load():
    global pipe
    detector = maskrcnn_resnet50_fpn_v2(weights="DEFAULT").eval()
    classifier = convnext_tiny(weights="DEFAULT").eval()
    pipe = VisionPipeline(detector, classifier, class_names=[f"c{i}" for i in range(1000)])

@app.post("/detect")
async def detect_endpoint(file: UploadFile):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="unsupported image type")
    data = await file.read()
    try:
        img = Image.open(BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="cannot decode image")
    result = pipe.run(img, image_id=file.filename or "upload")
    return result.model_dump()
```

اجري مع`uvicorn main:app --host 0.0.0.0 --port 8000`. اختبار مع`curl -F 'file=@dog.jpg' http://localhost:8000/detect`. . .

> استخدام`uvicorn main:app --host 0.0.0.0 --port 8000`运行。用 `curl -F 'file=@dog.jpg' http://localhost:8000/detect`测试。

### الخطوة 5: قم بتحديد خط الأنابيب

```python
import time

def benchmark(pipe, num_runs=20, image_size=(400, 600)):
    img = (np.random.rand(*image_size, 3) * 255).astype(np.uint8)
    pipe.run(img)  # warm up

    stages = {"preprocess": [], "detect": [], "classify": [], "total": []}
    for _ in range(num_runs):
        t0 = time.perf_counter()
        tensor = pipe.preprocess(img)
        t1 = time.perf_counter()
        det = pipe.detect(tensor)
        t2 = time.perf_counter()
        crops = []
        for box in det["boxes"]:
            x1, y1, x2, y2 = [max(0, int(b)) for b in box.tolist()]
            x2 = min(x2, tensor.shape[-1])
            y2 = min(y2, tensor.shape[-2])
            if (x2 - x1) >= pipe.min_crop and (y2 - y1) >= pipe.min_crop:
                crop = tensor[:, y1:y2, x1:x2]
                crop = torch.nn.functional.interpolate(
                    crop.unsqueeze(0), size=(224, 224), mode="bilinear", align_corners=False
                )[0]
                crops.append(crop)
        pipe.classify(crops)
        t3 = time.perf_counter()
        stages["preprocess"].append((t1 - t0) * 1000)
        stages["detect"].append((t2 - t1) * 1000)
        stages["classify"].append((t3 - t2) * 1000)
        stages["total"].append((t3 - t0) * 1000)

    for stage, times in stages.items():
        times.sort()
        print(f"{stage:12s}  p50={times[len(times)//2]:7.1f} ms  p95={times[int(len(times)*0.95)]:7.1f} ms")
```

الناتج النموذجي على المعالجة المركزية: التحليل قبل العملية ~ 3 ms ، الكشف عن 300-500 ms ، تصنيف 20-40 ms ، إجمالي 350-550 ms. على GPU ، الكشف هو 20-40 ms والتحليل + تصنيف يبدأ في الأهمية أكثر من الناحية النسبية.

> الناتج النموذجي على جهاز التشغيل المركزي: التحليل المسبق حوالي 3ms ٬ التحليل 300-500ms ٬ التشغيل 20-40ms ٬ إجمالي 350-550ms ٬ في جهاز التشغيل المركزي، التحليل المسبق حوالي 20-40ms، أصبح النسبة المقابلة بين التحليل المسبق والفئة أكثر أهمية٬

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.





> **【拓展：视觉模型的持续学习】**في بيئة الإنتاج، يتطلب نموذج الرؤية التكيف المستمر مع البيانات الجديدة.

## استخدمها في إطار التنفيذ

نماذج الإنتاج تتحرك إلى نفس الهيكل، بالإضافة إلى:

- **Model versioning** دائما تسجيل اسم النموذج وزيادة الهاشش في الإجابة.
- **Per-request trace IDs** سجل كل مرحلة توقيت لكل طلب حتى تتمكن من ربط الاستجابات البطيئة مع المراحل.
- **Fallback path** إذا انتهى وقت التصنيف، أعد الكشف دون تصنيف بدلاً من عدم إنجاز الطلب بأكمله.
- **Safety filters** فلترات NSFW / PII تعمل بعد التصنيف ، قبل أن يغادر الاستجابة الخدمة.
- **Batch endpoint** أ `/detect_batch`قبول قائمة عناوين URL للصور لعملية المعالجة الجماعية.

للخدمة الإنتاجية`torchserve`،`Triton Inference Server`و`BentoML`التعامل مع الإعدادات، الإصدارات، المقاييس، والتحقق من الصحة خارج الصندوق.`FastAPI`مباشرة هو جيد للنموذج الأول والمنتجات الصغيرة.

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.




## أرسلها .

هذا الدرس ينتج عن:

- `outputs/prompt-vision-service-shape-reviewer.md` طلب يراجع رمز خدمة الرؤية لانتهاكات شكل العقد / الاستجابة ويعطي الاسم للكذب الأول.
- `outputs/skill-pipeline-budget-planner.md` مهارة تعطي، بالنظر إلى التأخير المستهدف والعبث، ميزانية زمنية لكل مرحلة من خط الأنابيب وتحدد المرحلة التي ستفوت ميزانيتها أولاً.

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


## تمارين التدريب

1. **(Easy)**قم بتشغيل خط الأنابيب على 10 صور من أي مجموعة بيانات مفتوحة. قم بتقديم تقرير عن متوسط الوقت لكل مرحلة وتوزيع عدد الكشف لكل صورة.
2. **(Medium)**إضافة حقل خروج القناع إلى `Detection`وتقوم بتشفيرها على أنها RLE. التحقق من أن JSON يبقى أقل من 1MB حتى لو كانت صورة 10 كائنات.
3. **(Hard)**إضافة مجموعة صغيرة أمام المصنف: جمع المحاصيل لمدة تصل إلى 10 ميس، تصنيفها كلها في اتصال واحد لـ GPU، إرجاع النتائج لكل طلب. قياس زيادة التوصيل عند 5 طلبات متزايدة في الثانية والانخفاض المضاف.

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Pipeline | "The system" | An ordered chain of preprocessing, inference, and postprocessing steps with a typed interface between each pair |
| Data contract | "The schema" | Pydantic / dataclass definitions that every stage input and output conforms to; catches integration bugs at the boundary |
| Preprocessing | "Before the model" | Decoding, colour conversion, resizing, normalising; usually the biggest CPU time sink |
| Postprocessing | "After the model" | NMS, mask resize, threshold, RLE encode; cheap on GPU, expensive on CPU |
| Microbatcher | "Collect then forward" | Aggregator that waits a fixed window for multiple requests, runs a single batched forward pass |
| Trace ID | "Request id" | Per-request identifier logged at every stage so slow requests can be traced end-to-end |
| Failure code | "Named error" | Specific error code per failure class instead of generic 500; enables client retry logic |
| Health check | "Readiness probe" | Cheap endpoint that reports whether the service can answer; loadbalancers rely on this |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [Full Stack Deep Learning — Deploying Models](https://fullstackdeeplearning.com/course/2022/lecture-5-deployment/) الرؤية العامة للإنتاج
- [BentoML docs](https://docs.bentoml.com) إطار خدمة مع الإجراءات المشتركة، الإصدارات، والمقاييس
- [torchserve docs](https://pytorch.org/serve/)مكتبة "بيتورش" الرسمية
- [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server) خدمة عالية التدفق مع دعم المجموعات والعديد النماذج
