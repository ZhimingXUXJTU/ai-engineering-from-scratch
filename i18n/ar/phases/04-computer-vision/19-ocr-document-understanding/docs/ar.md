# فهم المستندات والمواد المستندية والمواد المستندية والمواد المستندية

> OCR هو خط أنابيب ثلاث مراحل  اكتشاف صناديق النص، وتعرف على الأحرف، ثم وضعها. كل نظام OCR الحديثة إعادة ترتيب هذه المراحل أو دمجها.

> **【中文解读】**OCR(تعرف الكتب الضوئية) is three stages流水线:检测文本框 → 识别字符 → 布局分析。 نظام OCR الحديث سوف يعيد ترتيب هذه المراحل أو يجمعها──文档理解不仅识别文字,还理解表格、图表、版面结构──

> **【拓展：文档理解的金融应用】**تمتلك فهم OCR والوثائق تطبيقات واسعة في مجال المالية: التعرف على التمويل المصرفي ، إصدار الصناديق التلقائي ، مراجعة عقود ذكية ، تحليل التقارير المالية.

**Type:** Learn + Use | **类型:** 学习 + 应用
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (Detection), Phase 7 Lesson 02 (Self-Attention) | **前置知识:** Phase 4 Lesson 06（目标检测），Phase 7 Lesson 02（自注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## أهداف التعلم

- تتبع خط الأنابيب الكلاسيكية لـ OCR (اكتشاف -> التعرف -> التخطيط) والبدائل الحديثة من النهاية إلى النهاية (دونوت ، Qwen-VL-OCR)
- تنفيذ خسارة CTC (التصنيف الزمني للاتصال) لتدريب OCR المتسلسل إلى المتسلسل
- استخدام PaddleOCR أو EasyOCR لتحليل وثائق الإنتاج دون تدريب
- تمييز OCR، تحليل التخطيط، وفهم الوثائق  واختيار الأداة المناسبة لكل مهمة

> **【中文解读】**يُدعى أهداف التعلم المفردة التي يجب أن تتحكم فيها بعد الانتهاء من الدورة.


## المشكلة المشكلة المشكلة

الصور المملئة بالنص موجودة في كل مكان: الإيصالات والفواتير والهوية والكتب المسحرة والنماذج واللواح البيضاء والرسومات والصور الشاشية. استخرج البيانات المهيكلة منها ليس فقط الحروف، ولكن "هذه هي المبلغ الإجمالي" هي واحدة من أعلى القيمة مشكلة الرؤية التطبيقية.

> الصور المملوءة بالأحرف لا توجد: رسومات، إصدارات، شهادات الهوية، مسح كتب، شكل، لوحات، علامات، قطع.

المجال ينقسم إلى ثلاث طبقات من المهارات:

> يُقسم هذا المجال إلى ثلاثة مستويات مهارة:

1. **OCR proper**تحويل البيكسلات إلى نص
2. **Layout parsing**: إنتاج المجموعة OCR إلى مناطق (اللقب، الجسم، الجدول، العنوان).
3. **Document understanding**: استخراج الحقول المهيكلة ("فواتير_جميع = 42.50 دولار") من التخطيط.

كل طبقة لديها نهج كلاسيكي ومحاصر، والفرق بين "أريد نص من صورة" و "أريد المبلغ الإجمالي من هذا الإيصالات" أكبر مما تدرك معظم الفرق.

> كل طبقة لديها طريقة كلاسيكية ومحديثة، والفرق بين "أريد الحصول على الكتب من الصورة" و"أحتاج إلى إجمالي المبلغ من هذا الإيرادات" أكبر من معظم الفريق أدرك.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


### خط الأنابيب الكلاسيكي

```mermaid
flowchart LR
    IMG["Image"] --> DET["Text detection<br/>(DB, EAST, CRAFT)"]
    DET --> BOX["Word/line<br/>bounding boxes"]
    BOX --> CROP["Crop each region"]
    CROP --> REC["Recognition<br/>(CRNN + CTC)"]
    REC --> TXT["Text strings"]
    TXT --> LAY["Layout<br/>ordering"]
    LAY --> OUT["Reading-order text"]

    style DET fill:#dbeafe,stroke:#2563eb
    style REC fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

- **Text detection**ينتج أرباعي خط أو كلمة.
  中文翻译:**文本检测**生成 كل خط أو كل كلمة مربع مربع
- **Recognition**يصل كل منطقة إلى ارتفاع ثابت، ويقوم بإدارة جهاز CNN + BiLSTM + CTC لإنتاج تسلسل شخصية.
  中文翻译:**识别**تقطع كل منطقة إلى ارتفاع ثابت، وتشغيل CNN + BiLSTM + CTC 生成字符序列
- **Layout**يعيد بناء ترتيب القراءة (من الأعلى إلى الأسفل، من اليسار إلى اليمين بالنسبة إلى اللاتينية؛ مختلفة بالنسبة إلى العربية واليابانية).
  中文翻译:**布局**重建阅读顺序(拉丁文从上到下、从左到右;阿拉伯文和日文不同)

### المعلومات المتاحة في الفقرة الواحدة

إن التعرف على OCR ينتج تسلسلًا متغيرًا من خريطة ميزة ذات طول ثابت. يسمح لك CTC (Graves et al., 2006) بتدريب هذا دون توازن مستوى الأحرف. يقوم النموذج بإخراج توزيع على (الكلمات + الفراغ) في كل خطوة زمنية. تخسر CTC على هامش جميع التوصلات التي تقل إلى النص المستهدف بعد دمج التكرارات وإزالة الفراغات.

> OCR 识别从固定长度的特征图生成可变长度序列──CTC(Graves 等,2006)让你无需字符级对齐就能训练──模型在每时间步输出(词表 +空白) على التوزيع؛CTC 损失对所有合并重复和移除空白后归约为目标文本对齐方式进行边缘化──

```
raw output: "h h h _ _ e e l l _ l l o _ _"
after merge repeats and remove blanks: "hello"
```

ويعتبر CTC هو السبب في عمل CRNN في عام 2015 وما زال يدرّب معظم نماذج OCR الإنتاجية في عام 2026.

> إن سي تي سي هي سبب عمل CRNN في عام 2015 وما زال يتدرب في عام 2026 معظم إنتاج نماذج OCR ‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

### النماذج الحديثة من نهاية إلى نهاية

- **Donut**(كيم وزملاء، 2022)  مرموز ViT + مرموز نص؛ يقرأ صورة ويصدر JSON مباشرة. لا يوجد كشف نص، لا يوجد وحدات التخطيط.
  中文翻译:**Donut**(Kim 等,2022) ViT 编码器 + 文本解码器;读取图像直接输出 JSON──无需文本检测器或布局模块──
- **TrOCR** جهاز تشخيص المتحول ViT + لـ OCR على مستوى الخط.
  中文翻译:**TrOCR**ViT + محول 解码器، للمستخدمين في أوقار الصف
- **Qwen-VL-OCR / InternVL** نماذج كاملة للغة الرؤية مُعدّلة لمهام OCR؛ أفضل دقة في عام 2026 على الوثائق المعقدة.
  中文翻译:**Qwen-VL-OCR / InternVL**                                                                                                                                                                                                                                                              
- **PaddleOCR** خط أنابيب DB + CRNN الكلاسيكي في حزمة إنتاج ناضجة؛ لا يزال حزمة العمل مفتوحة المصدر.
  中文翻译:**PaddleOCR** الكلاسيكي DB + CRNN 流水线; لا يزال مفتوحاً

تحتاج النماذج من نهاية إلى نهاية إلى المزيد من البيانات والحسابات ولكن تجنب تراكم الأخطاء في خطوط الأنابيب متعددة المراحل.

> النموذج من النهاية إلى النهاية يحتاج إلى المزيد من البيانات والحسابات ، ولكن قفز من خلال العديد من المراحل التدفقات التدريبية.

### تحليل التخطيط

بالنسبة للوثائق المهيكلة، قم بتشغيل كاشف التخطيط (LayoutLMv3 ، DocLayNet) الذي يضع علامة على كل منطقة: عنوان ، الفقرة ، الرسم ، الجدول ، ملاحظة أسفل. يصبح ترتيب القراءة بعد ذلك "تكرر عبر المناطق في ترتيب التخطيط ، المزدوج".

> 对于结构化文档,运行布局检测器(LayoutLMv3、DocLayNet) تسمية كل منطقة: عنوان 段落、图、表、脚注。阅读顺序变成"按布局顺序遍历区域,拼接"──

في الاستمارات، استخدم **Key-Value extraction**النماذج (دونوت للوثائق الغنية بالبصر، LayoutLMv3 للتسحينات العادية).

> 对于表单,使用**键值提取**模型(视觉丰富文档用唐nut,普通扫描用 LayoutLMv3) ――它们收录图像 + 检测到的文本 + 位置,预测结构化的键值对──

### مقاييس التقييم

- **Character Error Rate (CER)** مسافة ليفينشتاين / طول مرجع. أقل أفضل. هدف الإنتاج: < 2% على المسحات النظيفة.
  中文翻译:**字符错误率（CER）** 编辑距离 / 参考文本长度──越低越好──生产目标:清晰扫描上 < 2%──
- **Word Error Rate (WER)** نفس الشيء على مستوى الكلمات.
  中文翻译:**词错误率（WER）**词级的同样标志──
- **F1 on structured fields** للمهمات ذات القيمة الرئيسية؛ تدابير ما إذا كان `{invoice_total: 42.50}`يبدو صحيحاً
  中文翻译:**结构化字段 F1**مؤشر مهمة القيمة الرئيسية؛ قياس `{invoice_total: 42.50}`نعم نعم حقاً
- **Edit distance on JSON** لتحليل الوثائق من نهاية إلى نهاية. أدخلت ورقة دونوت مسافة تعديل شجرة معايرة.
  中文翻译:**JSON 编辑距离**端到端文档解析的指标;Donut 论文引入归一化树编辑距离──

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

> **【拓展：工业部署中的视觉系统】**في التوزيع الصناعي الواقعي، تحتاج النموذج المرئي إلى النظر في التفكير في التأجيل، والنموذج الكبير، والجهاز الحدودي الملائمة وغيرها من المشاكل.

> **【拓展：数据标注与质量】** تأثير المهام المرئية يعتمد على جودة البيانات المعلنة.‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬




## بناء ذلك تحرك لتحقيق
```figure
cv3-ctc-collapse
```

## بناءها

### الخطوة الأولى: فقدان CTC + مفكّر طموح

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank=0):
    """
    log_probs:      (T, N, C) log-softmax over vocab including blank at index 0
    targets:        (N, S) int targets (no blanks)
    input_lengths:  (N,) per-sample time steps used
    target_lengths: (N,) per-sample target length
    """
    return F.ctc_loss(log_probs, targets, input_lengths, target_lengths,
                      blank=blank, reduction="mean", zero_infinity=True)


def greedy_ctc_decode(log_probs, blank=0):
    """
    log_probs: (T, N, C) log-softmax
    returns: list of index sequences (blanks removed, repeats merged)
    """
    preds = log_probs.argmax(dim=-1).transpose(0, 1).cpu().tolist()
    out = []
    for seq in preds:
        decoded = []
        prev = None
        for idx in seq:
            if idx != prev and idx != blank:
                decoded.append(idx)
            prev = idx
        out.append(decoded)
    return out
```

`F.ctc_loss`يستخدم تنفيذ CuDNN الفعال عندما يكون متاحًا. إن المفكّر البشع أبسط من البحث عن الشعاع وعادة ما يكون ضمن 1% من إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إطار إ

> `F.ctc_loss`في الوقت المتاح استخدام كيو دي إن إن عالية الفعالية لتحقيقها.

### الخطوة الثانية: جهاز التعرف على CRNN الصغير

الحد الأدنى من CNN + BiLSTM لخط OCR.

> يستخدم لتحقيق أقل قدر من التسجيلات (أوكر) من خلال (سي إن إن + بي إل إس)

```python
class TinyCRNN(nn.Module):
    def __init__(self, vocab_size=40, hidden=128, feat=32):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, feat, 3, 1, 1), nn.BatchNorm2d(feat), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(feat, feat * 2, 3, 1, 1), nn.BatchNorm2d(feat * 2), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(feat * 2, feat * 4, 3, 1, 1), nn.BatchNorm2d(feat * 4), nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),
            nn.Conv2d(feat * 4, feat * 4, 3, 1, 1), nn.BatchNorm2d(feat * 4), nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),
        )
        self.rnn = nn.LSTM(feat * 4, hidden, bidirectional=True, batch_first=True)
        self.head = nn.Linear(hidden * 2, vocab_size)

    def forward(self, x):
        # x: (N, 1, H, W)
        f = self.cnn(x)                # (N, C, H', W')
        f = f.mean(dim=2).transpose(1, 2)  # (N, W', C)
        h, _ = self.rnn(f)
        return F.log_softmax(self.head(h).transpose(0, 1), dim=-1)  # (W', N, vocab)
```

المدخلات ذات الارتفاع الثابت (إن إن أقصى مستوى من الارتفاع إلى 1).

> 固定高度输入(CNN 将高度最大池化到 1)。宽度是CTC 的时间维度。

### الخطوة الثالثة: OCR الاصطناعي

توليد سلسلة من الأرقام السوداء إلى البيضاء لاختبار الدخان من النهاية إلى النهاية.

> 生成白底黑字符串,用于端到端冒烟测试──

```python
import numpy as np

def synthetic_line(text, height=32, char_width=16):
    W = char_width * len(text)
    img = np.ones((height, W), dtype=np.float32)
    for i, c in enumerate(text):
        x = i * char_width
        shade = 0.0 if c.isalnum() else 0.5
        img[6:height - 6, x + 2:x + char_width - 2] = shade
    return img


def build_batch(strings, vocab):
    H = 32
    W = 16 * max(len(s) for s in strings)
    imgs = np.ones((len(strings), 1, H, W), dtype=np.float32)
    target_lengths = []
    targets = []
    for i, s in enumerate(strings):
        imgs[i, 0, :, :16 * len(s)] = synthetic_line(s)
        ids = [vocab.index(c) for c in s]
        targets.extend(ids)
        target_lengths.append(len(ids))
    return torch.from_numpy(imgs), torch.tensor(targets), torch.tensor(target_lengths)


vocab = ["_"] + list("0123456789abcdefghijklmnopqrstuvwxyz")
imgs, targets, lengths = build_batch(["hello", "world"], vocab)
print(f"images: {imgs.shape}   targets: {targets.shape}   lengths: {lengths.tolist()}")
```

مجموعة بيانات OCR الحقيقية تضيف الخطوط والضوضاء والدورة والضباب واللون.

> حقيقة OCR بيانات تجمع زيادة الخطوط  الضوضاء  التدوير  المظلة واللون 

### الخطوة الرابعة: رسم التدريب

```python
model = TinyCRNN(vocab_size=len(vocab))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for step in range(200):
    strings = ["abc" + str(step % 10)] * 4 + ["xyz" + str((step + 1) % 10)] * 4
    imgs, targets, target_lens = build_batch(strings, vocab)
    log_probs = model(imgs)  # (W', 8, vocab)
    input_lens = torch.full((8,), log_probs.size(0), dtype=torch.long)
    loss = ctc_loss(log_probs, targets, input_lens, target_lens, blank=0)
    opt.zero_grad(); loss.backward(); opt.step()
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.


يجب أن تنخفض الخسارة من ~ 3 إلى ~ 0.2 على 200 خطوة على هذه البيانات الاصطناعية البسيطة.

> في هذه البيانات المكونة بسيطة، فإن خسائر 200 خطوة من حوالي 3 إلى حوالي 0.2




> **【拓展：视觉模型的持续学习】**في بيئة الإنتاج، يتطلب نموذج الرؤية التكيف المستمر مع البيانات الجديدة.

## استخدمها في إطار التنفيذ

ثلاثة طرق إنتاج:

- **PaddleOCR** بالغة، سريعة، متعددة اللغات. استخدام خط واحد: `paddleocr.PaddleOCR(lang="en").ocr(image_path)`. . .
- **EasyOCR** Python-أصلي، متعددة اللغات، PyTorch العمود الفقري.
- **Tesseract** الكلاسيكية؛ لا تزال مفيدة للمستندات القديمة المسحرة عندما تتعرض النماذج للصراع.

لتحليل الوثائق من النهاية إلى النهاية، استخدم Donut أو VLM:

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
```

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


بالنسبة للإيصالات والفواتير والأوراق ذات الهيكل المتكرر، قم بتحسين دونوت. بالنسبة للمستندات التعسفية أو OCR مع التفكير، فإن VLM مثل Qwen-VL-OCR هو الافتراض الحالي.



## أرسلها .

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──


هذا الدرس ينتج عن:

- `outputs/prompt-ocr-stack-picker.md` طلب يختار Tesseract / PaddleOCR / Donut / VLM-OCR نوع وثيقة معينة، اللغة، والهيكل.
- `outputs/skill-ctc-decoder.md` مهارة تكتب طموحة و البحث عن الشعاع CTC مبرمجة من الصفر، بما في ذلك التطبيع على الطول.

## تمارين التدريب

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


1. **(Easy)**تدريب TinyCRNN على سلسلة رقمية عشوائية 5 أرقام لمدة 500 خطوة. تقرير CER على مجموعة مدعومة.
2. **(Medium)**استبدل تشفير الشعاع ببحث الشعاع (beam_width=5). تقرير CER delta. على أي مدخلات يربح بحث الشعاع؟
3. **(Hard)**استخدم PaddleOCR على مجموعة من 20 إيصال، استخراج عناصر الخط، وحساب F1 ضد الحقيقة الأرضية المسموحة يدويا ل {item_name، سعر} أزواج.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| OCR | "Text from pixels" | Turning image regions into character sequences |
| CTC | "Alignment-free loss" | Loss that trains a sequence model without per-timestep labels; marginalises over alignments |
| CRNN | "Classic OCR model" | Conv feature extractor + BiLSTM + CTC; the 2015 baseline still used in production |
| Donut | "End-to-end OCR" | ViT encoder + text decoder; emits JSON directly from image |
| Layout parsing | "Find regions" | Detect and label Title/Table/Figure/Paragraph regions in a document |
| Reading order | "Text sequence" | Ordering of recognised regions into a sentence; trivial for Latin, non-trivial for mixed layouts |
| CER / WER | "Error rates" | Levenshtein distance / reference length at character or word granularity |
| VLM-OCR | "LLM that reads" | A vision-language model trained or prompted for OCR tasks; current SOTA on complex documents |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [CRNN (Shi et al., 2015)](https://arxiv.org/abs/1507.05717) بنية CNN+RNN+CTC الأصلية
- [CTC (Graves et al., 2006)](https://www.cs.toronto.edu/~graves/icml_2006.pdf) ورقة CTC الأصلية؛ مليئة بالكثير من الأفكار الخوارزمية
- [Donut (Kim et al., 2022)](https://arxiv.org/abs/2111.15664) محول لفهم الوثائق خالي من OCR
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) كومة OCR الإنتاج مفتوح المصدر
