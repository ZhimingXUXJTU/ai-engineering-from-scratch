# نقطة التفتيش التدريجية وتحديد التشغيل

> يحتفظ Backprop بكل تنشيط متوسط. عند معايير 70B و 128K سياق الذي هو 3 TB من التنشيط لكل رتبة. التفتيش التجارة FLOPs للذاكرة: إعادة الحساب بدلا من حفظ. السؤال هو أي قطاعات أن تسقط، والجواب ليس "جميعهم".

> **【中文解读】**في المقابل، يجب أن يتم حفظ جميع النشاطات الوسطى. 70B 参数 + 128K 上下文 = 每卡 3TB 激活.

> **【拓展：梯度检查点→大模型训练】**梯度检查点是训练大模型的标配技术──PyTorch's torch.utils.checkpoint、DeepSpeed's activation checkpointing 都是实现这一思想──在128K 上下文训练中,选择性检查点可以节省60%+的显存──

>  **【前置】**学本节前请先掌握:Phase 10·04(Pre-Training GPT);反向传播算法;GPU 显存层次(SRAM vs HBM)。本节是训练超大模型 + 长上下文时的关键技术。
>  **【类比】**梯度检查点 = 出差只带必要文件──反向传播── 工作完成后回顾所有材料;不检查点 = 把出差路上所有的材料都背着(占满行李箱);全检查点 = 只带护照,需要时重新打印(重算成本高);选择性检查点──只扔可重算的(如草稿),保留难重建的(如合同) 平衡存储和速度显著──

**Type:** Build
**Languages:** Python (with numpy, optional torch)
**Prerequisites:** Phase 10 Lesson 04 (Pre-Training Mini-GPT), Phase 10 Lesson 05 (Scaling & Distributed)
**Time:** ~70 minutes

## المشكلة المشكلة المشكلة

تخزين تدريب المحول، لكل طبقة، المدخلات لكل عملية يتم التمييز فيها للخلف: مدخلات الاهتمام، وتقنيات Q/K/V، ومخرجات softmax، مدخلات FFN، ومخرجات القاعدة، والتيار المتبقية. بالنسبة للطبقة ذات الحجم الخفي `d`، طول التسلسل`L`، اللحظة`B`، هذا على ترتيب`12 * B * L * d`تعبث في كل طبقة

>  تدريب المحول ، كل طبقة تحتاج إلى تخزين في الاتجاه المنعكس للتنشر من كل تدخلات قابلة للتشغيل: توجهة إدخال  Q/K/V 投影、softmax 输出、FFN 输入、归化输出和残差流──`d`、序列长度 `L`、 الكمية `B`من الطبقة، وهذا تقريبا هو كل طبقة`12 * B * L * d`个浮点数──

لأجل`d=8192, L=8192, B=1`هذا هو 800 MB / طبقة في BF16. نموذج 64 طبقة هو 51 GB من التفعيلات  وهذا قبل أن تضاعف بحجم microbatch، قبل أن تضيف الاهتمام-softmax المتوسطات (`L^2`(في الرأس) ، وقبل أن تقوم بتحليل النسخة الجزئية المتوازية مع التنسور.

> لـ`d=8192, L=8192, B=1`,BF16 下每层800 MB──64 层模型的激活值为51 GB`L^2`), لا يعد هناك جزء من المجموعة المشتركة

الفاتورة ذات الجانبين: أوزان BF16 بالإضافة إلى حالة المحفز قد تناسب في 80GB ، ولكن التفعيلات تدفعك إلى ما بعد. التحقق من التحقق من التحقق (والمعروف باسم إعادة حساب التفعيل) هو الإصلاح القياسي. إسقاط معظم التفعيلات ؛ إعادة التحقق من التحقق من التحقق من التحقق منها. التكلفة: FLOPs إضافية. الفائدة: انخفاض الذاكرة بنسبة قطاعات نقاط التحقق إلى مجموع الطبقات.

> 双面账单:BF16 权重加优化器状态可能放入80GB,但激活值让你超出──梯度检查点(又称激活重计算) هو نظام إصلاحي قياسي── تخلى عن معظم القيمة النشطة؛ في فترة الانتشار المضاد؛ إعادة القيام بالعمل الاولى للتوزيع لتحسينها──代价: إضافية FLOPs──收益:显存按检查段段数与总层数比例下降──

يتم البراغة، وتكلفة التفتيش نحو 33% أكثر من التفتيشات المقدمة في كل خطوة. يتم بشكل جيد  التفتيشات المنتخبة لكل "اختيار ذكي" من كورثيكانتي وآخرين.  يمكنك حفظ 5x الذاكرة لأقل من 5% من التفتيشات المقدمة. ومع FP8 matmuls، FSDP offload، وخبير متوازي MoE هذا يهم حقا: لا يمكنك تحمل ولا الذاكرة أو الحسابات المهدرة.

## المفهوم الأساسي

> **【中文解读】**梯度检查点(Gradient Checkpointing) باستخدام حساب تبادل الاحتفاظ: قبل التنقل لا يحفظ قيمة النشاط الوسطى، في مقابل التنقل احتاج إلى إعادة الحساب للإنشاط.

> **【拓展：梯度检查点在训练中的关键作用】**نقطة فحص التدريجية هي تقنية تعريف نموذج كبير للتدريب. بالنسبة للاما 3 70B، لا توجد نقطة فحص عندما يحتاج كل عينة إلى حوالي 16GB  قيمة تشغيل واضحة، ثم انخفض بعد الافتتاح إلى حوالي 5GB.


### ما يحتاجه المتخلفون في الواقع

`output = layer(input)`- يريدون الخلف`grad_input`و`grad_params`لتحسّبها يحتاج:

- `input`(للتحساب`grad_params = input.T @ grad_output`للطبقات الخطية)
- بعض مشتقات التفعيل المتوسطة (مشتقات ReLU/GELU/softmax تعتمد على قيمة التفعيل)

المخطط الأمامي يحتفظ به تلقائياً في الرسم البياني للشكل الذاتي`tensor.retain_grad()`وكل عملية تحتاج إلى إدخالها تحتفظ بمراجعة

### البراغبة في التفتيش الكامل

تقسيم الشبكة إلى `N`خلال المشاريع، تخزين فقط * المدخل * لكل قطاع. عندما يحتاج الخلفية إلى المتوسطات، إعادة تشغيل مرور القطاع إلى الأمام لتحقيقها، ثم التمييز.

مثال: محول 32 طبقة مقسم إلى 32 قطعة من طبقة واحدة لكل منها.

- الذاكرة: 32 مدخل طبقة (صغيرة) مقابل 32 * (حجم تفعيل لكل طبقة) (كبير).
- الحساب الإضافي: 1 إضافي للأمام لكل قطعة، أي ~33% أكثر من مجموع FLOPs للأمام (بما أن الخلف هو 2x للأمام، تصبح الخطوة الكاملة 1 + 1 + 2 = 4 وحدات بدلا من 1 + 2 = 3).

هذه وصفة " تشين " وآخرون في عام 2016: نقطة تفتيش واحدة لكل`sqrt(L)`طبقات لتوازن الذاكرة والحساب. بالنسبة ل=64, هذا هو 8 نقاط تفتيش.

### نقطة التفتيش الانتخابية (كورتهيكانتي 2022)

لا تكلف جميع التفعيلات بنفس القدر.`B*L*L*heads`و ينمو * مربعًا * مع طول التسلسل.`B*L*4d`و ينمو خطياً. بالنسبة لترتيبات طويلة، يهيمن على "البالغة الناعمة".

يحتفظ التفتيش الانتقائي بتشغيلات التخزين الرخيصة (التنبؤات السطحية والبقايا) ويعد فقط تلك المكلفة (الاهتمام). تدفع أدنى فلوب ليعيد الحساب ولكن توفر ذاكرة O(L^2).

تطبق ميغاترون كور هذا كإعادة حساب التفعيل "المتخذي". يستخدم في معظم تدريبات الحدود 2024+.

### إفراج

بديل لإعادة الحساب: تشغيل جهاز لـ RAM CPU بين الأمام والخلف. يتطلب عرض النطاق PCIe؛ مفيد عندما يتجاوز عرض النطاق العاطف تكلفة إعادة المادة. استراتيجيات مختلطة شائعة: نقطة تفتيش بعض الطبقات، وتفريغ آخرين.

FSDP2 يُرسل إزالة الحمولة كخيار من الدرجة الأولى. الإزالة تُضيء عندما تكون GPU عالقة في الذاكرة ولكن تحويل CPU-GPU لديه مساحة رأسية.

### نموذج التكلفة

كل خطوة تُفشل مع مراقبة سرية كلّ مرة`k`طبقات خارج `L`:

```
flops_fwd_normal = L * f_layer
flops_bwd_normal = 2 * L * f_layer
flops_total_normal = 3 * L * f_layer

flops_fwd_ckpt = L * f_layer
flops_recompute = L * f_layer  # one extra forward per layer in the segment
flops_bwd_ckpt = 2 * L * f_layer
flops_total_ckpt = 4 * L * f_layer
overhead = 4 / 3 - 1 = 0.33 = 33%
```

مع التفتيش الانتقائي تقوم بإعادة حساب فقط جوهر الاهتمام، وليس الطبقة بأكملها:

```
flops_recompute_selective = L * f_attention ~= L * f_layer * 0.15
overhead_selective = (3 + 0.15) / 3 - 1 = 0.05 = 5%
```

### نموذج توفير الذاكرة

حجم التفعيل لكل طبقة: `A`- لأجل`L`طبقات، ذاكرة تنشيط كاملة: `L * A`. . .

نقطة تفتيش كاملة (حجم القطاع 1): تخزين فقط `L * input_volume`(~`L * 1/10 A`لتحول عيار معياري)`9 * L * A * 1/10`. . .

نقطة تفتيش كلّ مرة`k`الطبقات: تخزين `L/k * A`بالإضافة`k-1`قيمة الطبقات داخل القطاع النشط.

في`k = sqrt(L)`تكلفة الذاكرة وإعادة الحساب كل من مقياس مع `sqrt(L)` التنازل الأمثل لطبقات التكلفة الموحدة.

### عندما لا تذهب إلى نقطة التفتيش

- الدراغ الداخلي من مرحلة خط الأنابيب بالفعل في الطيران، يجب أن ينتهيوا على أي حال.
- الطبقات الأولى والأخيرة إذا كانت تهيمن على حساب المرحلة ( نادرة في المحولات).
- أجزاء الاهتمام التي تستخدم بالفعل FlashAttention  Flash تقوم بالفعل بإعادة حساب softmax بسرعة، لذلك لا يضيف التفتيش الإضافي على مستوى الطبقة الكثير.

### نمط التنفيذ

1. **Function wrapper:**لف قطعة في `torch.utils.checkpoint.checkpoint(fn, input)`متجر بيتورش فقط`input`، يعيد حساب كل شيء آخر في الخلف

2. **Decorator-based:**تعيين الطبقات كمركز للتفتيش؛ يقوم المدرب في وقت التشغيل بتحديد القطاعات التي يتم لفها.

3. **Manual explicit recompute:**اكتبوا المخطط الخلفي بنفسك، واصطدقوا العادة`recompute_forward`الذي يكرر المقدمة مع المدخل المخزن.

كل ثلاثة يعطي نفس النتيجة الوظيفية. الملفوفات هي اللغة القياسية.

### التفاعل مع TP / PP / FP8

- **Tensor parallel:**يجب جمع مدخلات نقطة التفتيش أو إعادة توزيعها على إعادة الحساب؛ تحمل تكلفة الاتصالات.
- **Pipeline parallel:**النمط النموذجي هو تحديد نقطة التفتيش للأمام لكل مرحلة من خط الأنابيب حتى يمكن لشركات التشغيل الميكرو باكيرات التردد إعادة استخدام ذاكرة التفعيل.
- **FP8 recompute:**يجب أن تتطابق تاريخ amax المحدث أثناء إعادة الحساب مع التقدير الأصلي أو التدفقات في مقياس FP8.


> **【拓展：梯度检查点与 FSDP 的配合】**عادة ما تكون نقاط التفتيش التدريجي مع FSDP/ZeRO  مع استخدامها  FSDP  分片参数和优化器状态,                                                                                                                                                                                                                                                      


## بناء ذلك تحرك لتحقيق
```figure
activation-recompute
```

## بناءها

### الخطوة الأولى: نموذج لعبة مع قطاعات

```python
import numpy as np


def linear_forward(x, w, b):
    return x @ w + b


def relu(x):
    return np.maximum(x, 0)


def layer_forward(x, w1, b1, w2, b2):
    h = relu(linear_forward(x, w1, b1))
    return linear_forward(h, w2, b2)


def model_forward(x, params):
    activations = [x]
    h = x
    for w1, b1, w2, b2 in params:
        h = layer_forward(h, w1, b1, w2, b2)
        activations.append(h)
    return h, activations
```

### الخطوة الثانية: البراغيّة المتراجعة تحتاج إلى كلّ التفعيلات

```python
def model_backward(grad_output, activations, params):
    grads = [None] * len(params)
    g = grad_output
    for i in range(len(params) - 1, -1, -1):
        w1, b1, w2, b2 = params[i]
        x_in = activations[i]
        h_pre = linear_forward(x_in, w1, b1)
        h = relu(h_pre)
        gh = g @ w2.T
        gw2 = h.T @ g
        gb2 = g.sum(axis=0)
        g_pre = gh * (h_pre > 0)
        gx = g_pre @ w1.T
        gw1 = x_in.T @ g_pre
        gb1 = g_pre.sum(axis=0)
        grads[i] = (gw1, gb1, gw2, gb2)
        g = gx
    return g, grads
```

### الخطوة الثالثة: نقطة التفتيش - كل ذاكرة

```python
def model_forward_checkpointed(x, params, k=4):
    saved_inputs = [x]
    h = x
    for i, (w1, b1, w2, b2) in enumerate(params):
        h = layer_forward(h, w1, b1, w2, b2)
        if (i + 1) % k == 0:
            saved_inputs.append(h)
    return h, saved_inputs


def model_backward_checkpointed(grad_output, saved_inputs, params, k=4):
    grads = [None] * len(params)
    g = grad_output
    segments = [(j * k, min((j + 1) * k, len(params))) for j in range(len(saved_inputs))]
    for seg_idx in range(len(saved_inputs) - 1, -1, -1):
        start, end = segments[seg_idx]
        if start >= end:
            continue
        x_in = saved_inputs[seg_idx]
        _, seg_acts = model_forward(x_in, params[start:end])
        g, seg_grads = model_backward(g, seg_acts, params[start:end])
        for j, gr in enumerate(seg_grads):
            grads[start + j] = gr
    return g, grads
```

### الخطوة الرابعة: نموذج التكلفة

```python
def checkpoint_cost(n_layers, segment_size, flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }


def selective_checkpoint_cost(n_layers, attention_fraction=0.15,
                              flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * attention_fraction * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }
```

### الخطوة 5: مقياس الذاكرة

```python
def activation_memory_mb(n_layers, hidden=8192, seq=8192,
                        batch=1, bytes_per_value=2):
    per_layer = 12 * batch * seq * hidden * bytes_per_value
    return n_layers * per_layer / 1e6


def memory_after_checkpoint(n_layers, segment_size, hidden=8192,
                           seq=8192, batch=1, bytes_per_value=2):
    n_seg = max(1, n_layers // segment_size)
    saved = (n_seg + segment_size) * 1 * batch * seq * hidden * bytes_per_value
    return saved / 1e6
```

### الخطوة 6: حجم القطاع المثالي

```python
def optimal_segment(n_layers):
    return int(round(np.sqrt(n_layers)))
```

### الخطوة 7: قرار نقطة تفتيش انتقائية

```python
def should_recompute(layer_type, activation_bytes, recompute_flops_ratio):
    if layer_type == "attention" and activation_bytes > 100 * 1e6:
        return True
    if layer_type == "ffn" and activation_bytes > 500 * 1e6:
        return recompute_flops_ratio < 0.1
    return False
```

## استخدمها في إطار التنفيذ

- **torch.utils.checkpoint**: `from torch.utils.checkpoint import checkpoint`الملف القنوني في PyTorch. يلف وظيفة؛ يحتفظ فقط المدخلات، يعيد الحسابات إلى الوراء.
- **Megatron-Core activation recomputation**: دعم `selective`،`full`و`block`طرق التدريب: قياسية في تدريب الحدود 2024+
- **FSDP2 offload**: `module.to_empty(device="cpu")`مع`offload_policy`في FSDP2 تقطع التفعيلات إلى CPU بدلا من إعادة الحساب.
- **DeepSpeed ZeRO-Offload**: إزالة CPU للحالات ومفعولات المحفز، وتكملة التفتيش.

## أرسلها .

هذا الدرس يُنتج`outputs/prompt-activation-recompute-policy.md` طلب يأخذ إعداد النموذج الخاص بك (طبقات ، مخفية ، seq ، دفعة) والذاكرة المتوفرة لـ GPU ويعرض سياسة إعادة الحساب لكل طبقة (لا / انتقائية / كاملة / خارج الحمل).

> 本课产出 `outputs/prompt-activation-recompute-policy.md` تكوين نموذج مقبول                                                                                                                                                                                                                                                           

## تمارين التدريب

1. تحقق من صحة.`model_forward`+ `model_backward`(التفعيل الكامل) vs `model_forward_checkpointed`+ `model_backward_checkpointed`يجب أن تكون تراجعات المعلمات متطابقة مع دقة الآلة
   中文翻译:验证正确性──运行 `model_forward`+ `model_backward`(完整激活) مع `model_forward_checkpointed`+ `model_backward_checkpointed`(分段)  يجب أن يتوافق درجة المعايير مع دقة الآلة

2. حجم قطاع التنظيف`k`من 1 إلى `L`-أحصل على الركبة من المنحنى
   中文翻译:将段大小 `k`من 1 扫到 `L`◊ رسم FLOP 开销和内存──找到曲线的拐点──

3. تنفيذ التفتيشات الانتقائية: تخزين مدخلات وحدات الاهتمام ولكن ليس منتظمتها. قياس التفتيشات العليا للشكل العلوي مقابل التفتيشات الكاملة للطبقة لنموذج 32 طبقة عند seq=8192.
   中文翻译:实现选择性检查点: تخزين الاهتمام 模块输入但不存中间结果──测量 32层模型在 seq=8192 下与全层检查点的 FLOP 开销比较──

4. إضافة التحميل المنزول. حفظ مدخلات القطاعات إلى محاكاة "مضاد المركز المركزي" (قائمة منفصلة). قياس "بريدة النطاق PCIe" كالبايت/وقت وتحديد نقطة التوازن بين التحميل المنزول وإعادة الحساب.
   中文翻译:添加卸载──将段输入保存到模拟的"CPU 缓冲区"(单独的列表)──以字节/时间测量"PCIe 带宽"并找到卸载和重计算之间的平衡点──

5. قم بتقييم محول PyTorch الحقيقي مع و بدون`torch.utils.checkpoint`. قياس الذاكرة (بـ `torch.cuda.max_memory_allocated`) وقتاً للخطوات
   中文翻译:对真实 PyTorch محول 分别使用和不使用 `torch.utils.checkpoint`إجراء تجربة قياسية`torch.cuda.max_memory_allocated`و قدم طويل الوقت

## شروط الرئيسية

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Gradient checkpointing | "Save memory by redoing forward" | Store segment inputs only; recompute intermediates during backward to get gradient-support tensors | 梯度检查点，仅保存段输入，反向时重算中间值 |
| Activation recomputation | "Same as checkpointing" | The HPC-flavored name for the same technique | 激活重计算，梯度检查点的 HPC 叫法 |
| Segment size (k) | "How many layers per checkpoint" | Number of layers whose intermediates are dropped and rematerialized together | 段大小，每个检查点包含的层数 |
| Selective checkpointing | "Korthikanti's trick" | Recompute only expensive-to-store activations (attention softmax); keep cheap ones | 选择性检查点，只重算存储昂贵的激活 |
| Full checkpointing | "The naive version" | Recompute every layer's intermediates in every segment | 全量检查点，朴素版本重算所有中间值 |
| Block checkpointing | "Coarse-grained" | Checkpoint whole transformer blocks; largest granularity | 块级检查点，以 Transformer 块为粒度 |
| FLOP overhead | "The compute tax" | Extra FLOPs per step = (recompute FLOPs) / (fwd + bwd FLOPs); 33% naive, 5% selective | FLOP 开销，朴素版 33%，选择性版 5% |
| Activation offload | "Ship to CPU" | Move activations to CPU RAM across forward->backward; alternative to recompute | 激活卸载，将激活移到 CPU 内存 |
| sqrt-L rule | "The classical optimum" | For uniform-cost layers, optimal checkpoint spacing is sqrt(L) layers | sqrt-L 规则，均匀层代价的最优检查点间隔 |
| Attention-softmax volume | "The O(L^2) problem" | L^2 * heads * batch floats; dominates activation memory at long contexts | 注意力 softmax 体积，O(L^2) 的显存问题 |

## المزيد من القراءة

- [Chen et al., 2016 -- "Training Deep Nets with Sublinear Memory Cost"](https://arxiv.org/abs/1604.06174)-- الورقة الأصلية التي رسمية التفتيش التدريجي
- [Korthikanti et al., 2022 -- "Reducing Activation Recomputation in Large Transformer Models"](https://arxiv.org/abs/2205.05198)-- إعادة الحسابات المنتخبة للاستفادة وتحليل التكلفة الرسمي
- [Pudipeddi et al., 2020 -- "Training Large Neural Networks with Constant Memory using a New Execution Algorithm"](https://arxiv.org/abs/2002.05645)-- نهج بديل لذاكرة ثابتة عن طريق إعادة المادية في وضع العكس
- [Ren et al., 2021 -- "ZeRO-Offload: Democratizing Billion-Scale Model Training"](https://arxiv.org/abs/2101.06840)-- تحميل التشغيل على مقياس
- [PyTorch torch.utils.checkpoint docs](https://pytorch.org/docs/stable/checkpoint.html)-- API القياسية
- [Megatron-Core activation recomputation documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/features/memory_optimizations.html)-- أساليب اختيارية وملئة ومدينة
