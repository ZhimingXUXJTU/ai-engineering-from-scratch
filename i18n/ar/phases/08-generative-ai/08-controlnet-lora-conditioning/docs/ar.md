# (كنتول نت) ، (لورا) والترتيبات

> يسمح لك ControlNet بتنسيق نموذج التوزيع المسبق للتدريب وتوجيهه باستخدام خريطة عمق أو هيكل عظمي أو خدش أو صورة حافة. يسمح لك LoRA بتحسين نموذج معايير 2B من خلال تدريب 10 ملايين ملامح. معا حولوا Diffusion Stable من لعبة إلى خط أنابيب الصور 2026 الذي يتم شحنه في كل وكالة.

> **【中文解读】**純文本控制太粗──ControlNet باستخدام العميقة الصورة 姿态骨架、涂 أو الحافة الصورة تحديد التحكم توليد؛ LoRA فقط تدريب 1000 مليون عنصر على التضليل من 20 مليار عنصر نموذج── كلتا الاثنين يجمعان لجعلها مستقر الانتشار من اللعبة إلى تصبح 2026 كل شركة تصميم في استخدام الصورة تدفق المياه..

> **【拓展：LoRA 是大模型时代的微调标准】**لا يقتصر استخدامها في إنتاج الصور على استخدامها على نطاق واسع في مجال التطبيقات التنفيذية (LLM) ، مثل LLaMA-LoRA.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## المشكلة المشكلة المشكلة

إن إشارة مثل "مرأة في ثوب أحمر تمشي كلباً في شارع مزدحم" لا تعطي النموذج معلومات عن * أين * الكلب ، * ما هي وضعية * المرأة ، أو * منظور * من الشارع. يحدد النص حوالي 10% مما تحتاج إليه لتضمين صورة. الباقي بصري ولا يمكن وصفه بكلمات بكفاءة.

> مثل "مرأة مرتدية الحمراء على شارع مزدحم" لا تخبر النموذج الكلب في * أين * ، المرأة هي * ما الموقف * ، * وجهة نظر * من الشارع كيف.

تعليماً نموذج مشروط جديد من الصفر لكل إشارة (موقف، عمق، حكمة، قسم) أمر محظور. تريد أن تبقي العمود الفقري SDXL 2.6B-param مقفوفة، وربط شبكة جانبية صغيرة تقرأ التشريع، وتجعلها تدفع الميزات المتوسطة للعمود الفقري. وهذا هو ControlNet.

> للشكل الواحد (مظهر، عمق، حافة، تقسيم) من الصف التدريب الجديد النموذج الظروف تكلفة عالية جدا.

كما تريد تعليم النموذج مفاهيم جديدة (وجهك، منتجك، أسلوبك) دون إعادة تدريب النموذج الكامل. تريد دلتا أصغر بنسبة 100 مرة. هذا هو مكيّفات LoRA  منخفضة الدرجة التي تتواصل مع أوزان الاهتمام القائمة.

> أنت أيضاً تريد تعليم النموذج الجديد ((وجهك، منتجاتك، أسلوبك)) دون إعادة تدريب النموذج بأكمله.

ControlNet + LoRA + text = مجموعة أدوات الممارس 2026. معظم خطوط أنابيب الصورة الإنتاجية تضم 2-5 LoRAs ، 1-3 ControlNets ، ومعدل IP فوق قاعدة SDXL / SD3 / Flux.

> ControlNet + LoRA + text = 2026 سنة الممارس المعدات. معظم الإنتاج الصور تدفق على SDXL / SD3/Flux على أساس فوق 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter。

## المفهوم الأساسي

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### (تشارون)

خذ SD متدربة مسبقاً. * قم بتسجيلها* من نصف تشفير U-Net. قم بتجميد الأصلي. قم بتسجيله لتقبل مدخل إضافي للتشغيل (الحواف والعمق والوضع). قم بتوصيل الكلون إلى نصف تشفير الأصلي مع * صفر-convolution* تخطي الاتصالات (1 × 1 convs المبدئية إلى الصفر  تبدأ كإغلاق، تعلم دلتا).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

0-conv init يعني أن ControlNet يبدأ على شكل هوية  لا ضرر حتى قبل التدريب. القطار على 1M (السرعة، الحالة، الصورة) يضاعف إلى ثلاثة أضعاف مع فقدان الانتشار القياسي.

تم إرسال ControlNets للطريقة الواحدة كنموذج جانبي صغير (~ 360M لـ SDXL، ~ 70M لـ SD 1.5).

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### (هو وزملاء)

لأي طبقة خطية`W ∈ R^{d×d}`في النموذج، التجمد `W`و أضف ديلتا منخفضة الدرجة:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

مع`r << d`. الدرجة 4-16 هي معيار للاهتمام، الدرجة 64-128 لخطوات دقيقة ثقيلة. عدد المعلمات الجديدة: `2 · d · r`بدلاً من`d²`. لـ (SDXL) الاهتمام مع`d=640`،`r=16`: 20k في كل جهاز تعديل بدلا من 410k  تخفيض 20x. عبر النموذج بأكمله: لورا عادة ما تكون 20-200MB مقابل 5GB القاعدة.

عند الاستنتاج يمكنك أن تقوم بتحقيق حجم المعدل`W' = W + α · B @ A`. .`α = 0.5-1.5`المواد المتعددة لـ LoRA تتراكم بشكل إضافي (مع الحذارة المعتادة بأنها تتفاعل بطريقة غير خطية).

### المعدل المعدل (Ye et al., 2023)

مُعدّل صغير يقبل الصورة كشروط (بجانب النص). يستخدم مُرمّد الصورة CLIP لإنتاج رموز الصورة، ويُحققها في الاهتمام المتقاطع جنباً إلى جنب مع رموز النص. ~ 20 ميب لكل نموذج أساسي. يسمح لك بـ "إنتاج صورة في أسلوب هذا المرجع" دون لورا.

## ماتريكس التجميع

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

شبكة التحكم فضائية، لورا معنوية، استخدم الاثنين

> ControlNet ≈ 空间控制──LoRA ≈ 语义控制──两者配合使用──

> **【中文解读】**الجهاز الأساسي لـ ControlNet: كلون SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态) ・・・零卷积(零卷积) 初始化确保训练开始时ControlNet 不影响原始模型。LoRA 在线性层上添加低排矩阵 B@A,只训练极少参数量(20-200MB vs 基础模型 5GB) ・・・

> **【拓展：ControlNet + LoRA 的组合控制】**في الإنتاج الواقعي،ControlNet(مراقبة الفضاء) وLoRA(风格/موضوع التحكم) عادةً يستخدمونها في مجموعة. على سبيل المثال:ControlNet 控制人物姿态,LoRA 注入特定艺术风格,文本提示 描述场景内容── هذه الجهازات الثلاثية للسيطرة هي التكوين المعيار لخدمات الصور التجارية AI 图像服务──IP-Adapter 则提供"مستخدمة الصور التحكم الصورة" الأبعاد الرابع──

## بناء ذلك تحرك لتحقيق
```figure
v4-controlnet-zero
```

## بناءها

`code/main.py`يحاكي الآليين في 1-D:

1. **LoRA.**طبقة خطية مسبقة`W`أجمدوه، تدربوا منخفضين`B @ A`مثل هذا`W + BA`يطابق طبقة خطية هدف.`r = 1`يكفي لتعلم تصحيح الدرجة 1 بشكل مثالي

2. **ControlNet-lite.**"قاعدة مقفزة" و "شبكة جانبية" تقرأ إشارة إضافية. يتم إغلاق خروج الشبكة الجانبية بواسطة مقياس قابل للتعلم تم تشريعه إلى الصفر (إصدارنا من الصفر-conv). قم بتشغيل ومراقبة البوابة.

### الخطوة الأولى: رياضيات لورا

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### الخطوة الثانية: شبكة جانبية صفر

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

في الخطوة 0 تكون الناتجية متطابقة مع القاعدة. تحديثات التدريب المبكر `gate`ببطء لا يوجد تدفق كارثي

> في المرحلة الثانية المخرج مع النموذج الأساسي تماما نفسها.`gate`更新缓慢没有灾难性偏移──

## الفخاخة

- **Over-scaling LoRAs.** `α = 2`أو`α = 3`هو عملية "جعلها أقوى" شائعة التي تنتج نتائج أكثر من اللازمة.`α ≤ 1.5`. . .
  **LoRA 过度缩放。** `α = 2`أو`α = 3`"تعزيز" الممارسة المعتادة، سوف تسبب زيادة في تصنيف/تلف المنتجات.`α ≤ 1.5`.
- **ControlNet weight conflict.**استخدام شبكة التحكم في الوزن 1.0 و شبكة التحكم في الغموض عند الوزن 1.0 عادة ما يتجاوز. مجموع الوزن ≈ 1.0 هو افتراض آمن.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 هي القيمة الاختيارية للسلامة
- **LoRA on the wrong base.**SDXL LoRA لا تعمل بصمت على SD 1.5 لأن أبعاد الاهتمام لا تتطابق.
  **LoRA 用错基础模型。**SDXL LoRA في SD 1.5 上会静默无效──
- **Textual Inversion drift.**الوهم المدربة في نقطة تفتيش تتحرك بشكل سيء في نقطة أخرى.
  **Textual Inversion 漂移。**في نقطة فحص واحدة علامة تدريبية في آخر
- **LoRA weight-merging and storage.**يمكنك تطبيق لورا في أساس النموذج الوزن لتحديد أسرع (لا إضافة وقت التشغيل) ، ولكنك تفقد القدرة على التوسع`α`في وقت تشغيل، احتفظ بالنسختين
  **LoRA 权重合并。**يمكن أن تسرع التفكير في النموذج الأساسي، ولكن تفقد التشغيل في الوقت المناسب`α`قدرتها

## استخدمها في إطار التنفيذ

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## أرسلها .

إنقاذ`outputs/skill-sd-toolkit-composer.md`. تتولى المهارة مهمة (أصول المدخل: عجلة، صورة مرجعية اختيارية، وضع اختياري، عمق اختياري، مسرح اختياري) وتخرج كومة الأدوات، والأوزان، وبروتوكول البذور المتكملة.

## تمارين التدريب

1. **Easy / 简单.**في`code/main.py`، تغير رتبة لورا`r`من 1 إلى 4 في أي صف يطابق لورا بالضبط دلتا الهدف من صف 2؟
   في`code/main.py`中将 لورا 秩 `r`من 1 إلى 4.. في أي وقت يتناسب المعدل؟
2. **Medium / 中等.**قم بتدريب اثنين من الـ LoRA على اثنين من تحويلات الهدف قم بتحميلها معاً وظهر تفاعلهم الإضافي متى ينتهي التفاعل الخطية؟
   في غضون تغيير هدفين على التدريب على حدة LoRA.
3. **Hard / 困难.**استخدام الموزعات لتحديد: SDXL-base + Canny-ControlNet (وزن 0.8) + LoRA (α 0.8) + IP-Adapter (وزن 0.6).
   استخدام الموزعات 堆叠组合, قياس FID مع prompt 遵循的权衡──

## شروط الرئيسية

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## ملاحظة إنتاج: LoRA تبادلات، ControlNet طرق، خدمة متعددة المستأجرين  生产笔记: LoRA 热插拔、ControlNet 通道、多租户服务

يقدم SaaS الحقيقي من النص إلى الصورة مئات من LoRAs وعشرات ControlNets على نفس نقطة التفتيش القاعدة. تبدو مشكلة الخدمة على غرار LLM متعددة التأجير (غطي أدب الإنتاج حالة LLM تحت الإجراءات المستمرة والLoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.**الاندماج`W' = W + α·B·A`في القاعدة يعطي ~ 3-5% أسرع في خطوة استنتاج ولكن يتجمد `α`و القاعدة. الحفاظ على لورا ساخنة في VRAM كديلتا رتبة- r؛ الموزعات تعرض `pipe.load_lora_weights()`+ `pipe.set_adapters([...], adapter_weights=[...])`لتنشيط الطلب. تكلفة التبادل هي `2 · d · r · num_layers`الوزن  على مقياس MB، في الجزء الثاني.
- **ControlNet as a second attention lane.**يعمل المُخترف المُستنسخ بالتوازي مع القاعدة. اثنين من ControlNets وزنها 1.0 كل واحد = مرتين إضافيتين إلى الأمام في كل خطوة، وليس مراراً واحداً مدمجاً. تنخفض مساحة المجموعة من الحجم التربيعي. ميزانية ~ 1.5 × تكلفة الخطوة لكل ControlNet نشطة.
- **Quantized LoRAs too.**إذا قمت بتقييم القاعدة (انظر الدروس 07, التدفق على 8GB) ، فإن دلتا LoRA تقييمها أيضاً بشكل نظيف إلى 8 بتات أو 4 بتات. تسمح لك التحميل على شكل QLoRA بتجميع 5-10 LoRA على رأس قاعدة 4 بتات من التدفق دون تفجير الذاكرة.

تحديد التدفق: نيبوك نيلز التدفق على 8GB يقدر القاعدة إلى 4 بتات؛ وضع طراز LoRA (`pipe.load_lora_weights("user/style-lora")`) على هذه القاعدة الكمية في `weight_name="pytorch_lora_weights.safetensors"`هذا هو وصفة معظم وكالات SaaS تسافر في عام 2026.

## المزيد من القراءة

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) ControlNet
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) لورا (أولياً لـ LLM؛ الموانئ إلى التنشر).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) جهاز تعديل IP
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453)بديل أخف للسيطرة على شبكة التحكم
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242)"مكتب الأحلام"
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet)خطوط الأنابيب المرجعية
