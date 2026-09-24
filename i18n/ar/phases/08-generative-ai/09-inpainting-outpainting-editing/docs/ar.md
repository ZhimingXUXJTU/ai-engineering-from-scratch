# التلوين والتمزيق والتحرير الصور 图像修复、扩展与编辑

> النص إلى الصورة يجعل أشياء جديدة. التلوين يصلح الأشياء القديمة. في الإنتاج، 70٪ من عمل الصورة القابل للتصوير هو التحرير  تبادل الخلفية، إزالة شعار، تمديد اللوحة، إعادة تشكيل يد. التلوين هو حيث يكتسب التوزيع الاحتفاظ بها.

> **【中文解读】**文本生成图像创造新东西,图像修复(涂料) تعديل ما هو موجود.

> **【拓展：Photoshop 生成式填充】**Adobe Photoshop's generative fill) هو على أساس التكنولوجيا التلوينية.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 8 · 08 (ControlNet & LoRA)
**Time:** ~75 minutes

## المشكلة المشكلة المشكلة

يقوم العميل بإرسال صورة منتجية مثالية مع علامة تشتت في الخلفية. تريد مسح علامة وتترك كل شيء آخر متطابقة بالبيكسل. لا يمكنك تشغيل النص إلى الصورة من الصفر  النتيجة ستكون لون مختلفة، وإضاءة مختلفة، زاوية منتج مختلفة. تريد إعادة إنتاج * فقط * المنطقة المخدّمة، وتريد إعادة إنتاج احترام السياق المحيط.

> 客户发来一张完美的产品照片,背景有分散注意的标志――你想抹去标志并保持其他图像完全一致――你不能从头发运行文生图结果会有不同的颜色,光照和产品角度――你想只重生*被遮蔽区域*,并让重生内容尊重周围上下文――

هذا هو التلوين

> هذا هو التلوين

- **Inpainting.**إعادة التوليد داخل قناع، والبقاء خارج البيكسلات.
  **图像修复。**في الظل إعادة إنتاج، الحفاظ على الصورة الخارجية.
- **Outpainting.**إعادة التوليد خارج القناع (أو خارج اللوحة) ، والبقاء داخل.
  **图像扩展。**في الغطاء خارج إعادة إنتاج، الحفاظ على الداخل.
- **Image editing.**إعادة إنتاج الصورة بأكملها ولكن الحفاظ على الوفاء التفسيلي أو الهيكلي للمصدر الأصلي (SDEdit، InstructPix2Pix).
  **图像编辑。**إعادة إنتاج الصورة بأكملها ولكن الحفاظ على التوافقات الهيكلية

كل خط أنابيب التنشر في عام 2026 يُرسل وضعًا للتلوين. فلوكس.1-ملي، إنبيت التنشر المستقر، SDXL-Inpaint، DALL-E 3 Edit. يعملون على نفس المبدأ.

> 2026 سنة كل انتشار تدفق مياه لديه طلاء 模式──Flux.1-Fill、SD-Inpaint、SDXL-Inpaint、DALL-E 3 Edit──原理相同──

> **【中文解读】**إنماط (تصوير الصور) هو أكثر حاجة إلى تحرير الصور شيوعاً في بيئة الإنتاج. التحدي الأساسي: إعادة إنتاج المنطقة المغطاة فقط، مع الحفاظ على التوافق مع ما تحيط بها.

> **【拓展：Photoshop 生成式填充与商业 Inpainting】**Adobe Photoshop هي تطبيق تاريخي للتكنولوجيا التلوينية. يجمع بين نموذج التوسع وتكنولوجيا التجمع الحدودي، مما يسمح للمستخدمين من خلال تعليمات اللغة الطبيعية نقل / استبدال أي محتوى في الصور.

## المفهوم الأساسي

![Inpainting: mask-aware denoising with context-preserving reinjection](../assets/inpainting.svg)

### النهج البديل (ولماذا هو خاطئ)

> ### طريقة بسيطة و لماذا لا تفعل ذلك

إستخدم الصورة من النص إلى الصورة مع قناع، في كل خطوة من مراحل أخذ العينات، قم بتبديل المنطقة غير المقنعة للضوضاء الخفية بالصورة النظيفة المتوسعة للأمام، إنها تعمل بشكل سيء، الأثاث الحدودية تنزف لأن النموذج لا يملك معلومات عن ما هو في المنطقة المقنعة.

> استخدام الظل للعمل المعيارية. في كل عملية استبدال المنطقة غير المظلمة.

### نموذج الطلاء المناسب

> ### 正确的 تلوين 模型

قم بتشغيل شبكة U-Net المعدلة التي تأخذ 9 قنوات مدخلة بدلا من 4:

```
input = concat([ noisy_latent (4ch), encoded_image (4ch), mask (1ch) ], dim=channel)
```

القنوات الإضافية هي نسخة من الصورة المصدرة التي يتم ترميزها VAE بالإضافة إلى قناع قناة واحدة. في وقت التدريب ، تقوم بتغطية مناطق الصورة بشكل عشوائي وتدريب النموذج على إشارة المنطقة المغطاة فقط بينما يتم إعطاء المنطقة غير المغطاة كإشارة تكييف نظيفة. عند الاستنتاج ، يمكن للنموذج "رؤية" ما يحيط المنطقة المغطاة ويؤتدي إلى استكمالات متماسكة.

يستخدم SD-Inpaint و SDXL-Inpaint و Flux-Fill كل هذه المدخلات التسعة قنوات (أو التناظرية).`StableDiffusionInpaintPipeline`،`FluxFillPipeline`. . .

> SD-Inpaint、SDXL-Inpaint、Flux-Fill 都使用这种 9通道(或类似)输入。

### SDEdit (Meng et al., 2022)  تحرير مجاني

> ### SDEdit  免费编辑

إضافة الضجيج إلى الصورة المصدرية حتى بعض الوسط `t`، ثم تشغيل السلسلة العكسية من`t`إلى 0 مع طلب جديد لا تدريب إعادة`t`يتداولون الصدقة من أجل الحرية الإبداعية

> إعطاء مصدر الصور ضجيج إلى مكان ما`t`ثم باستخدام الإرشادات الجديدة للصوت`t`                                                                                                                                                                                                                                                              

- `t/T = 0.3`→ متطابقة تقريباً مع المصدر، تغييرات نمطية صغيرة / 几乎与源相同,小风格变化
- `t/T = 0.6`→ تحريرات معتدلة، تحافظ على الهيكل الخام / 中等编辑,保留粗结构
- `t/T = 0.9`→ تم إنشاؤها من ضجيج قريب، الحفاظ على المصدر الحد الأدنى / 从近噪声生成,最小源保留

### InstructPix2Pix (بروكس وزملاء، 2023)

> ### InstructPix2Pix

تحسين نموذج التوزيع على`(input_image, instruction, output_image)`ثلاث مرات. عند الاستنتاج، تحديد حالة على كل من الصورة المدخلة وتعليمات النص ("جعلها تغروب الشمس"، "ضيف تنين"). مقياسين CFG: مقياس الصورة ومقياس النص.

> في`(输入图像, 指令, 输出图像)`ثلاث مجموعة على التوسع الصغرى النموذج.

### إعادة التلوين (Lugmayr et al., 2022)

> ### إعادة الطلاء

حافظ على نموذج انتشار قياسي غير مشروط. في كل خطوة عكسية، أعيد العينة  قفز مرة أخرى إلى حالة أكثر ضوضاء في بعض الأحيان وتجدد. تجنب الأثاث الحدودية. تستخدم عندما لا يكون لديك نموذج تدريب في الطلاء.

> 保持标准无条件扩散模型──在每反向步骤偶尔重采样跳回更噪的状态重新生成──避免边界伪影──

## بناء ذلك تحرك لتحقيق
```figure
inpaint-mask-reinject
```

## بناءها

`code/main.py`يطبق نظام طلاء لعبة 1-D على بيانات 5 أبعاد. نحن تدرب DDPM على بيانات خليط 5D حيث كل عينة 5 طائرات من واحدة من مجموعة. عند الاستنتاج، نحن "قناع" 2 من 5 أبعاد، حقن نسخة ضوضاء إلى الأمام من ثلاثة غير مقناع في كل خطوة، وتجدد فقط الأبعاد المقناع.

### الخطوة الأولى: بيانات DDPM 5-D

```python
def sample_data(rng):
    cluster = rng.choice([0, 1])
    center = [-1.0] * 5 if cluster == 0 else [1.0] * 5
    return [c + rng.gauss(0, 0.2) for c in center], cluster
```

### الخطوة الثانية: إعلان القطار على جميع الخمسة أجزاء

النتائج الشبكة تنبؤ الضوضاء 5-D لدخول الضوضاء 5-D.

### الخطوة الثالثة: عند الاستنتاج، العكس المعرف على القناع

```python
def inpaint_step(x_t, mask, clean_image, alpha_bars, t, rng):
    # replace unmasked dims with a freshly noised version of the clean source
    a_bar = alpha_bars[t]
    for i in range(len(x_t)):
        if not mask[i]:
            x_t[i] = math.sqrt(a_bar) * clean_image[i] + math.sqrt(1 - a_bar) * rng.gauss(0, 1)
    # ...then run the normal reverse step on x_t
```

هذا هو النهج البديل ويعمل على بيانات الألعاب 1-D. تصميم الصور الحقيقي يستخدم مدخل 9 قنوات لأن التماسك النسيج مهم أكثر.

### الخطوة الرابعة: التنفس

التلوين هو التلوين مع القناع معكسيا: تغطية القناع الجديد (غير موجود سابقا) ، وملء الباقي بالصيغة الأصلية. هدف التدريب المتماثل.

## الفخاخة

- **Seams.**يترك النهج البغيض حدود مرئية لأن معلومات التراجع لا تتدفق عبر القناع.
- **Mask leakage.**إذا كانت المنطقة غير المقنعة للوحة المضطربة منخفضة الجودة أو ضوضاء، فإنها تلوث الجيل داخل القناع.
- **CFG interacts with mask size.**ارتفاع CFG على قناع صغير = ملء ملقى. تقليل CFG للتحريرات الصغيرة.
- **SDEdit fidelity cliff.**من`t/T = 0.5`إلى`t/T = 0.6`يمكن أن تفقد هوية المُضطربة
- **Prompt mismatch.**يجب أن يصف المشارك الصورة بأكملها وليس فقط المحتوى الجديد. "قطة جالسة على كرسي" وليس "قطة".

## استخدمها في إطار التنفيذ

| Task / 任务 | Pipeline / 方案 |
|------|----------|
| Remove object, small mask / 移除物体 | SD-Inpaint or Flux-Fill, standard prompt |
| Replace sky / 替换天空 | SD-Inpaint + "blue sky at sunset" |
| Extend canvas / 扩展画布 | SDXL outpaint mode (8px feather) or Flux-Fill with outpaint mask |
| Regenerate hand / face / 重画手/脸 | SD-Inpaint with prompt re-describing the subject + ControlNet-Openpose |
| Change style of one region / 改变区域风格 | SDEdit at `t/T=0.5` on masked region |
| "Make it sunset" / "变成日落" | InstructPix2Pix or Flux-Kontext |
| Background replacement / 背景替换 | SAM mask → SD-Inpaint |
| Ultra-high-fidelity / 超高保真 | Flux-Fill or GPT-Image (hosted) for hardest cases |

SAM (Meta's Segment Anything، 2023) + diffusion inpaint هو خط أنابيب إزالة الخلفية 2026 . SAM 2 (2024) يعمل على الفيديو.

> SAM(Meta 的 Segment Anything) + 扩散 inpaint 是 2026 年的背景移除流水线──SAM 2(2024)支持视频──

## أرسلها .

إنقاذ`outputs/skill-editing-pipeline.md`. تتخذ مهارة صورة أصلية + وصف تحرير + قناع اختياري (أو طلب SAM) وتخرج: نهج توليد القناع ، النموذج الأساسي ، مقياس CFG (الصورة + النص) ، وضع SDEdit-t أو التلوين ، وقائمة التحقق من الجودة.

## تمارين التدريب

1. **Easy.**في`code/main.py`، يختلف جزء من الأبعاد المخفية من 0.2 إلى 0.8. في أي جزء تتساوى جودة الطلاء (البقية في المظاهرات المخفية) إلى توليد غير مشروط؟
2. **Medium.**قم بتنفيذ RePaint: في كل خطوة العاشرة للخلف، قفز إلى الوراء 5 خطوات (اضافة الضوضاء) وإعادة التعبير. قياس ما إذا كان يقلل من بقايا الحدود في حافة القناع.
3. **Hard.**استخدموا الموزعات المتحركة لتحديد الوجه للتقارن: SD 1.5 Inpaint + ControlNet-Openpose vs Flux.1-ملء على 20 مهمة إعادة إنتاج الوجه.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Inpainting | "Fill the hole" | Regenerate inside a mask; keep outside pixels. |
| Outpainting | "Extend the canvas" | Regenerate outside the canvas; keep inside. |
| 9-channel U-Net | "Proper inpainting model" | U-Net with `noisy \| encoded-source \| mask` as input. |
| SDEdit | "Img2img with noise level" | Noise to time `t`, denoise with new prompt. |
| InstructPix2Pix | "Text-only edits" | Fine-tuned diffusion on (image, instruction, output) triples. |
| RePaint | "No retraining" | Re-noise periodically during reverse to reduce seams. |
| SAM | "Segment Anything" | Mask generator by clicks or boxes; pairs with inpaint. |
| Flux-Kontext | "Edit with context" | Flux variant that accepts a reference image + instruction for edits. |

## ملاحظة الإنتاج: تحرير خطوط الأنابيب حساسة للتأخير

يُتوقع من المستخدمين الذين يُحَرِّرون الصورة رحلات ذهابًا وإيابًا لمدة أقل من 5 ثوانٍ. يبلغ SDXL-Inpaint في 10242 من 30 خطوة 3-4 ثانية على L4، بالإضافة إلى توليد قناع SAM (~ 200 ms) وترمية VAE / ترمية (~ 500 ms مجتمعة). في إطار الإنتاج، هذا مقيدًا لـ TTFT بدلاً من التوصيل مقيدًا  مجموعة 1، وتزايد التزامن المنخفض، وتقليل كل مرحلة:

- **SAM-H is the slow one.**SAM-H عند 10242 هو ~ 200 ms؛ SAM-ViT-B هو ~ 40 ms مع خسارة نوعية طفيفة. SAM 2 (فيديو) يضيف التكلفة العلوية؛ لا تستخدمها لتعديل الصورة الواحدة.
- **Skip the encode when possible.** `pipe.image_processor.preprocess(img)`إن كان لديك اللاتنتات من الجيل السابق (معتادة في واجهات البحث المتكررة) ، مرر بها مباشرة عبر `latents=...`لتفوت رمز VAE واحد
- **Mask dilation matters for throughput too.**قناع صغير يعني أن معظم مرور شبكة U-Net إلى الأمام يضيع (بكل حال يتم صبغ البكسلات غير المقنعة). `diffusers`"`StableDiffusionInpaintPipeline`يعمل على شبكة U-Net بالكامل بغض النظر؛ فقط تغيرات التسعة القنوات المثبتة بشكل صحيح تستغل الحوسبة المخفية.
- **Flux-Kontext is the 2025 answer.**تمرّة واحدة للأمام`(source_image, instruction)`لا يوجد قناع منفصل، لا يوجد مسح ضجيج SDEdit. على H100 فإنه يرسل تحرير في ~ 1.5 ثانية. درس الهندسة المعمارية: انهيار المراحل.

## المزيد من القراءة

- [Lugmayr et al. (2022). RePaint: Inpainting using Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2201.09865) التدريب الخالي من التدريب
- [Meng et al. (2022). SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073) إصابة
- [Brooks, Holynski, Efros (2023). InstructPix2Pix](https://arxiv.org/abs/2211.09800) تحرير نصوص نصية.
- [Kirillov et al. (2023). Segment Anything](https://arxiv.org/abs/2304.02643)SAM، مصدر القناع.
- [Ravi et al. (2024). SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) فيديو SAM.
- [Hertz et al. (2022). Prompt-to-Prompt Image Editing with Cross-Attention Control](https://arxiv.org/abs/2208.01626) تحرير مستوى الاهتمام
- [Black Forest Labs (2024). Flux.1-Fill and Flux.1-Kontext](https://blackforestlabs.ai/flux-1-tools/) 2024 أدوات
