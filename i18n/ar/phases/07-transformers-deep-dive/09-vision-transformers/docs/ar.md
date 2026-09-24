# تحويلات الرؤية (ViT) 视觉 Transformer (ViT)

> الصورة هي شبكة من المزيفات، الجملة هي شبكة من الرموز. نفس المحول يأكل كليهما.

> **【中文解读】**فيت وضع الصورة قطع معطلة 当作 توكن 序列处理──理解 فيت = فهم منصور غير محدودة إلى NLP──CLIP、DALL-E、Sora 都基于 منصور──

**Type:** Hands-on | **类型:** 动手
**Language:**" بايثون "**语言:**بايثون
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

قبل عام 2020، كان رؤية الكمبيوتر تعني تحولات. كل SOTA على ImageNet، COCO، ومعايير الكشف استخدمت قاعدة قاعدة قاعدة CNN. كان المحولات لغة.

> قبل عام 2020، كان تصميم الكمبيوتر يعني حجمها.

دوسويتسكي وزملاء (2020)  "الصورة تساوي 16 × 16 كلمة"  أظهر أنه يمكنك إسقاط التحولات بالكامل. قم بتقطيع صورة إلى ملصقات ذات حجم ثابت ، وبرمج كل ملصق خطياً في إضافة ، ومدفئة التسلسل إلى مُرسل مُحول فانيلياً. على نطاق كاف (مُقبل التدريب على ImageNet-21k أو أكبر) ، يطابق ViT أو يفوق النماذج القائمة على ResNet.

> دوسويتسكي 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送进标准变压器编码器──在足够大的下尺寸(ImageNet-21k 预训练或更大),ViT 可以匹配或超越基于ResNet的模型──

كانت ViT بداية نمط أوسع في عام 2026: بنية واحدة، العديد من الطرق. يُشير إلى الصوت. ViT يُشير إلى الصور. توكنات العمل للروبوتات. توكنات البيكسل للفيديو. لا يهتم المحول  يُغذيه تسلسلًا ويعلم.

> فيديو تينز هي نقطة انطلاق من اتجاهات أكثر نطاقا عام 2026: نوع من البنية، العديد من الأشكال.

بحلول عام 2026، يمتلك ViT وذريته (DeiT، Swin، DINOv2، ViT-22B، SAM 3) معظم الرؤية. لا تزال قنوات CNN تفوز على الأجهزة الحافة والمهام الحساسة بالخمول. كل شيء آخر لديه ViT في مكان ما في كومة.

> بحلول عام 2026، سيارت الفي.إن. ومتابعتها بعدها ((ديت، سواين، دينوف2، فيت-22ب، سام 3) استحوذت على معظم مجال الرؤية.

> **【中文解读】**رؤية جوهرية في تي: يمكن قطع الصور مثل النص على أنها "مؤشرات" تسلسل. سيتم قطع 224x224 صورة إلى 14x14 个 16x16 ملصق، كل ملصق 展平后线性投影为嵌入向量,然后送入标准变压器编码器.

## المفهوم الأساسي

![Image → patches → tokens → transformer](../assets/vit.svg)

### الخطوة 1  إصلاح

تقسيم`H × W × C`الصورة إلى صورة`N × (P·P·C)`تسلسل اللقطات المسطحة.`224 × 224`الصورة`16 × 16`اللقطات → 196 اللقطات ذات 768 قيمة لكل منها.

> ستعمل`H × W × C`图像 分分为 `N × (P·P·C)`序列──典型设置:`224 × 224`الصور`16 × 16`اللصق → 196 个 768 值的 اللصق

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

حجم اللصوص هو الرافعة. اللصوص الصغيرة = المزيد من الرموز، وضوح أفضل، تكلفة الاهتمام التربيعي. اللصوص الكبيرة = أكثر صعوبة، أرخص.

> الملفات الكبيرة هي التحكم في المعايير. الملفات الصغيرة = أكثر رموز.

### الخطوة 2  إضافة خطية

المصفوفة المعلمة واحدة تعرض كل مسطح مسطح إلى`d_model`. يعادل صعوبة من حجم النواة`P`و خطوات`P`في (بيتورش) هذا حرفياً`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` تنفيذ خطين.

> واحد يتعلم من المصفوفة سوف كل ملصق مسطح`d_model`◊ يساوي السعر للطاقة النووية`P`、步长为 `P`في بيتورش وسط هو`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现──

> **【拓展：Swin Transformer 的层级设计】**标准 ViT باستخدام اللفة الثابتة 大小和全局注意力,计算量 O(N^2)。Swin Transformer 引入层级结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野──这使计算复杂变为O(N),同时保留层级特征提取的能力──Swin 在检测和分分任务仍然优于标准 ViT──

### الخطوة 3  إعداد `[CLS]`رمز، إضافة التوابل الموضعية

- إعداد شيء يمكن التعلم`[CLS]`الـ (Token) ، الحالة الخفية النهائية هي تمثيل الصورة المستخدمة للتصنيف
  ترجمة: في افتتاح إضافة واحد قابل للتعلم`[CLS]`رمزها: تعريف الصور المختلفة
- إضافة التوابل الموضعية القابلة للتعلم (في تي الأصلية) أو 2D السينوسويدية (المختلفات اللاحقة).
  中文翻译:添加可学习的位置嵌入 (ViT 原始版) أو الصناعة 2D 嵌入 (后续变体)
- في عام 2024+ تم تمديد RoPE إلى 2D للموقع، أحياناً دون تضمين صريح.
  بعد عام 2024، توسعت ROPE إلى 2D  موقع编码، وأحيانا لا تحتاج إلى إدخال واضح.

### الخطوة 4  مُرمّد مُحول قياسي

كومة من الكتل`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`. متطابقة مع برت . لا توجد طبقات محددة للرؤية . هذه هي الخطوط التعليمية للورقة

> 堆叠 L 个 `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT 完全相同──没有视觉特有的层──这是这篇论文的教学要点──

### الخطوة 5

للتصنيف: خذ `[CLS]`الحالة الخفية → خطية → softmax. بالنسبة لـ DINOv2 أو SAM، إرمي`[CLS]`، استخدموا إضافة المفاتيح مباشرة

>  分类:取 `[CLS]`                                                                                                                                                                                                                                                              `[CLS]`, مباشرة استخدام اللصقة 嵌入──

### الإختلافات التي كانت مهمة

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### لماذا استغرق الأمر وقتاً

تحتاج شركة ViT إلى * الكثير من البيانات لتطابق CNN لأنها لا تملك أي من التحيزات التحديدية لـ CNN (غير تغير الترجمة ، المحلية). بدون صور معينة > 100 مليون أو تدريبات سابقة ذاتية إشراف قوية ، لا تزال شركة CNN تفوز في الحسابات المتطابقة. حل DeiT هذا في عام 2021 باستخدام خدوش التقطير ؛ حل DINOv2 بشكل دائم في عام 2023 باستخدام الإشراف الذاتي.

> فييت 需要大量 من البيانات لتطابق أداء سي أن إن ، لأنه لا يحتوي على تفضيلات CNN للخصم ؛ ((平移不变性、局部性)  لا يوجد 1 مليار张以上 من الصور المعلنة أو التدريبات المسبقة للمراقبة الذاتية ، لا تزال سي ان ان نغلبه في نفس الحسابات.

> **【中文解读】**تحفيزات التأثير الضعيف في التأثير الفيوت هو سيف ذو ذو ذروة: تحتاج إلى المزيد من البيانات لتطابق أداء سي إن إن ، لأن سي إن إن تيمون لديها تحفيزات متواصلة ومحلية. ولكن عندما يكون حجم البيانات كبير بما فيه الكفاية ، فإن توسيع فييت يزيد عن سي إن إن.

> **【拓展：ViT 在多模态系统中的角色】**استخدام الفيديو التنفيذي لـ "Clip" 编码图像、Transformer 编码文本,通过对比学习对齐两个模态──DALL-E 和 Sora 使用 ViT理解图像/视频,再生成新内容──SAM(Segment Anything) استخدام الفيديو 作为主干网络实现通用图像分割──ViT 已成为多模态 AI 视觉基础模块──

## بناء ذلك تحرك لتحقيق
```figure
n5-patch-stream
```

## بناءها

انظر`code/main.py`. صبغات مستحقة + إضافة خطية + فحص الصحة العقلية. لا تدريب  ViT على أي نطاق واقعي يحتاج PyTorch و ساعات من وقت GPU.

> 参见 `code/main.py` إصلاح المقاييس المعتادة + إضافة إضافية + إختبار منطقية.

### الخطوة الأولى: صورة مزيفة

صورة RGB 24 × 24 كقائمة من صفوف `(R, G, B)`نستخدم 6×6 معطيات → 16 معطيات، 108-D وضع متجه لكل.

> صورة 24 × 24 RGB`(R, G, B)`تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات الصفحة السابقة: تعبيرات: تعبيرات الصفحة السابقة: تعبيرات: تعبيرات:

### الخطوة الثانية: إصلاح

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

ترتيب الرأس: الصف الرئيسي عبر الشبكة كل ViT يستخدم هذا الترتيب

> نور تسلسل: شبكة على حسب خط الأولى عبرها. كل مرة تستخدم هذا الترتيب.

### الخطوة الثالثة: إرسال خطي

ضرب كل مسطح مسطح بالشكل العشوائي`(patch_flat_size, d_model)`المصفوفة. التحقق من شكل الخروج هو `(N_patches + 1, d_model)`بعد الإعداد`[CLS]`. . .

> سوف كل ملصق يُضاعف إلى إختيار`(patch_flat_size, d_model)`矩阵──验证在添加 `[CLS]`后输出形状为 `(N_patches + 1, d_model)`.

### الخطوة الرابعة: إعداد المعايير لـ ViT الواقعي

طبع عدد المعايير لـ ViT-Base: 12 طبقة، 12 رأس، d = 768, معصمة = 16. مقارنة مع ResNet-50 (~ 25M). ViT-Base يصل إلى ~ 86M. ViT-Large ~ 307M. ViT-Huge ~ 632M.

> 打印 ViT-Base 的参数:12 层、12 头、d=768、patch=16──与ResNet-50(约25M)对比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## استخدمها في إطار التنفيذ

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**تجميد العمود الفقري، تدريب رأس صغير يعمل للتصنيف، الاستعراض، الكشف، الترجمة. نقاط التفتيش DINOv2 في Meta تتفوق على CLIP في كل مهمة رؤية غير نصية.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头──适用于分类,检查,检测,图像描述──DINOv2 检查点在每个非文本视觉任务上都优于CLIP──

**Patch-size picking.**تستخدم النماذج الصغيرة 16 × 16 (ViT-B/16). تستخدم التنبؤات الكثيفة (التقسيم) 8 × 8 أو 14 × 14 (SAM ، DINOv2). تستخدم النماذج الكبيرة جدا 14 × 14.

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) استخدام 8×8 أو 14×14(SAM、DINOv2)。 جداً كبير

## أرسلها .

انظر`outputs/skill-vit-configurator.md`. تتختر المهارة فاريان ViT وحجم الإصلاح لمهمة رؤية جديدة نظراً لقياس مجموعة البيانات والقرار وميزانية الحساب.

> 参见 `outputs/skill-vit-configurator.md` هذه المهارة  حسب مجموعة البيانات الكبيرة  القرار والكمبيوتر الحسابي، لمهام الرؤية الجديدة اختيار ViT 变体和补丁 

## تمارين التدريب

1. **Easy.**أركض`code/main.py`. تأكد من عدد المزقين يساوي`(H/P) * (W/P)`وبعملية المزج المسطح مساوية`P*P*C`. . .
   中文翻译:运行 `code/main.py` تصحيح الملفات`(H/P) * (W/P)`, 平 ملصق 维度等于 `P*P*C`.
2. **Medium.**تنفيذ إدخالات موقفية في الحلبة السينوسيدالية 2D  اثنين من رموز الحلبة السينوسيدالية المستقلة ل `row`و`col`كل ملصق، متسلسل. إعطائهم في جهاز PyTorch ViT الصغير وقارن الدقة مقابل التوابل الموضعية القابلة للتعلم على CIFAR-10.
   中文翻译:实现 2D 正弦位置嵌入每个补丁的 `row`和 `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**قم ببناء ViT (PyTorch) ثلاثية الطبقات ، وتدريب على 1000 صورة MNIST مع ملصقات 4 × 4. قياس دقة الاختبار. الآن أضف DINOv2 التدريب المسبق على نفس 1000 صورة (بسهولة: فقط تدريب المبرمج للتنبؤ بتضمين اللصوص من ملصقات مخفية). هل تتحسن الدقة؟
   中文翻译:构建 3层 ViT(PyTorch), باستخدام 4×4 ملصق في 1,000 张 MNIST 图像上训练。测量测试准确率──然后添加 DINOv2 预训练(简化版:训练编码器从掩码补丁 预测补丁 嵌入)──准确率是否提升?

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## المزيد من القراءة

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)ورقة "في تي".
  中文翻译:ViT 原始论文。
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877) إختيار
  中文翻译:ديت 论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)-تسلل
  中文翻译:ساوين ترانسفورمير 论文。
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) DINOv2
  中文翻译:DINOv2 论文。
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) إصلاح رمز التسجيل لـ DINOv2.
  中文翻译:DINOv2 的注册代码 修复论文。
