# احتمالات وتوزيعات  احتمالات وتوزيع

> المحتملة هي اللغة التي تستخدمها الذكاء الاصطناعي للتعبير عن عدم اليقين.
> احتمال هو تعبير عن الذكاء الاصطناعي غير المؤكد.

**Type:** Learn | **类型:** 学习
**Language:**" بايثون "**语言:**بايثون
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## أهداف التعلم

- تنفيذ PMFs و PDFs من الصفر لبرنولي، الفئوية، البوزون، الموحدة، والتوزيعات العادية
- احسب القيمة المتوقعة والتشابه واستخدم نظرية الحد المركزي لشرح سبب سيطرة الغوسيان
- قم ببناء وظائف softmax و log-softmax باستخدام خدعة الاستقرار الرقمي (استبعاد max logit)
- الحساب الخسارة المتقاطعة من الـ "لوجيت" وربطها مع احتمالات الـ "لوج" السلبية

> **【中文解读】**
> 概率 هي AI تعبير لغة غير مؤكدة.                                                                                                                                                                                                                                                        

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: تحويل الناتج النبوي للخروج إلى توزيع احتمالية، هو الخطوة الأخيرة لجميع النماذج النمطية.
> - **交叉熵损失**: فاعل خسرة المعيار من المهام، يساوي سلبية على عدد مثل
> - **高斯分布**: فهم مركزي محدود يفسر لماذا توزيع الكوكس في الطبيعة والذكاء الاصطناعي هو أمر شائع جدا.

## المشكلة المشكلة المشكلة

> **【中文解读】** 分类器输出 `[0.03, 0.91, 0.06]`(91% احتمالية هو القط) ، نموذج لغوي من بين 50.000 كلمة مرشحة، نموذج التوسع من خلال التوزيع المتعلمة تمثل الصور هذه هي النظرية الاحتمالية في العمل.

## المفهوم الأساسي

> **【拓展：概率分布是 AI 生成模型的基础】**النموذج النموذجي (VAE、GAN、 انتشار النموذج) هو جوهر التوزيع الاحتمالي: تعلم إلى توزيع البيانات p(x) ، ثم من خلال الاختبار إنتاج بيانات جديدة.

كل تنبؤ يقوم به نموذج هو توزيع الاحتمالات. تقوم كل وظيفة الخسارة بقياس مدى المسافة التي يخطط لها التوزيع من الوضع الحقيقي. تقوم كل خطوة تدريبية بتعديل المعلمات لجعل توزيع واحد يبدو أكثر مماثلاً لآخر. بدون احتمال، لا يمكنك قراءة ورقة ML واحدة، أو إزالة عيب نموذج واحد، أو فهم سبب خسارة التدريب الخاصة بك هو NaN.

> كل توقع من النموذج هو توزيع احتمالية. كل وظيفة الخسارة تقيس الفرق بين توزيع التنبؤ والتوزيع الحقيقي. كل خطوة تدريبية في تعديل العناصر التي تجعل توزيع واحد أقرب إلى آخر.

## المفهوم الأساسي

### الأحداث ومناطق العينات والاحتمالات

مساحة العينة S هي مجموعة من جميع النتائج المحتملة. حدث هو مجموعة فرعية من مساحة العينة. احتمالية تقوم بتخطيط الأحداث إلى أرقام تتراوح بين 0 و 1.

> 样本空间 S هو مجموع جميع النتائج المحتملة. الأحداث هي الجماعة الفرعية من 样本空间. احتمالية أن يتم تصوير الأحداث إلى رقم بين 0 إلى 1.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

ثلاثة محور تعريف جميع احتمالات:
1. P(A) >= 0 لأي حدث A
2. P(S) = 1 (شيئ يحدث دائما)
3. P(A أو B) = P(A) + P(B) عندما لا يمكن أن تحدث A و B كلاهما

> 概率论由三条公理定义:
> 1. 对于任意事件 A,P(A) >= 0
> 2. (بالتأكيد هناك نوع من النتائج)
> 3. عندما A 和 B 不能同时发生时,P(A أو B) = P(A) + P(B)

كل شيء آخر (نظرية بايز، التوقعات، التوزيعات) يتبع من هذه القواعد الثلاثة.

> كل شيء آخر (باييس) يخرج من هذه القواعد

### احتمالية مشروطة واستقلالية

P ((A) هو احتمال A إعطاء أن B حدث.

> P ((A B) هو احتمال حدوث A بالمواقف التي حدثت بالفعل ب

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

حدثان مستقلان عندما تعرفان واحد لا يخبرونك شيئا عن الآخر

> الحوادث الثنائية مستقلة تعني معرفة أن واحدة منها لن تخبرك بأي معلومات عن الأخرى:

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

إن إلقاء العملات مستقلة، لا يمكن رسم البطاقات بدون استبدال

> لا تترك الـ"مـاركة" لا تترك الـ"مـاركة"

### وظائف الكتلة من احتمالية مقابل وظائف الكثافة من احتمالية

المتغيرات العشوائية المختلفة لديها وظيفة كتلة الاحتمال (PMF). لكل نتيجة احتمال محدد يمكنك قراءته مباشرة.

> 离散随机变量有概率质量函数 (PMF)                                                                                                                                                                                                                                                      

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

المتغيرات العشوائية المستمرة لديها وظيفة كثافة الاحتمال (PDF). الكثافة في نقطة واحدة ليست احتمالية. تأتي الاحتمال من دمج الكثافة على فترة.

> 连续随机变量有概率密度函数 (PDF) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅     ⋅                                                                                                                                                                                                          

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

هذا التمييز مهم في ML. إنخراجات التصنيف هي PMFs (الخيارات المتفصّلة). تستخدم الفضاءات الخفية في VAE ملفات PDF (متواصلة).

> هذا الاختلاف في ML مهم جدا.

### التوزيعات المشتركة

**Bernoulli:**تجربة واحدة، نتائج اثنتين، نماذج تصنيف ثنائي

> **伯努利分布：**تجربة، نتائج اثنتين.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**تجربة واحدة، نتائج k. النماذج تصنيف فئة متعددة (خروج غليظ).

> **分类分布：**تجربة، نوعا من النتائج.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**جميع النتائج محتملة بنفس القدر.

> **均匀分布：**جميع النتائج والاحتمالات تظهر.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**منحنى الزجاجة. يتم تحديدها بمعدل (mu) والانحراف (sigma^2).

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**يعد الحوادث النادرة في فترة محددة.

> **泊松分布：**عدد الحوادث النادرة في المنطقة الثابتة.

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### القيمة المتوقعة والتشابه

القيمة المتوقعة هي متوسط النتيجة الموزعة.

> 期望值是加权平均结果──

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

تدابير التباين منتشرة حول المتوسط

> الاختلاف يقيّم درجة الانفصال حول القيمة المتوسطة

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

في ML، تظهر القيمة المتوقعة كعمل الخسارة (الخسارة المتوسطة على توزيع البيانات). يخبرك التباين عن استقرار النموذج. التباين العالي في التراجع يعني تدريب ضجيج.

> في ML، فإن المتوقع أن يظهر على غرار خسارة الدالة ((الخسارة المتوسطة على توزيع البيانات) ، فإن الفوارق تخبرك عن استقرار النموذج.

### التوزيعات المشتركة والحاشية

توزيع مشترك P ((X، Y) يصف متغيرين عشوائيين معا.

> 联合分布 P(X,Y)  وصف حالة اثنين من التغيرات المتزامنة التي تحدث في نفس الوقت

مثال على PMF المشترك (X = الطقس، Y = مظلة):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

التوزيع الحدودي يجمع المتغير الآخر:

> 边缘分布通过对另一个变量求和得到:

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

مجموعات الصف والعمود في الجدول أعلاه هي الحدود.

> المجموعات والحسابات في الجدول العلوي هي التوزيع على الحافة.

### لماذا توزيع طبيعي يظهر في كل مكان

نظرية الحد المركزي: مجموع (أو متوسط) العديد من المتغيرات العشوائية المستقلة يتقارب إلى توزيع طبيعي، بغض النظر عن التوزيع الأصلي.

> معدل الحد الأقصى: العديد من التغيرات المستقلة والمتوسطية والمتميزة إلى التوزيع الصالح، بغض النظر عن التوزيع الأصلي هو ما هو.

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

هذا هو السبب:
- أخطاء القياس طبيعية تقريباً (كثير من المصادر الصغيرة المستقلة)
  中文翻译: قياس خطأ تقارب الصواب
- تُستخدم التشغيلات الأولى للوزن في الشبكات العصبية توزيعات طبيعية
  中文翻译:تأثير الوزن في شبكة النور باستخدام التوزيع الصحي
- ضجيج التدريج في SGD هو طبيعي تقريبًا (جمع العديد من التدريجيات العينة)
  中文翻译:SGD 中的梯度噪声近似正态(许多样本梯度的总和)
- التوزيع العادي هو أقصى توزيع للاندروبي لمتوسط معين و التباين
  ترجمة باللغة الصينية: تقسيم طبيعي هو تقسيم أقصى تحت متوسط القيمة والفرق

### احتمالات السجل

الاحتمالات الخامة تسبب مشاكل عددية. مضاعفة العديد من الاحتمالات الصغيرة معاً تسير بسرعة إلى الصفر.

> الإحتمالات الأولية تؤدي إلى مشكلة القيمة العددية.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

إعداد الاحتمالات تحل هذا

> على احتمالية العدد حل هذه المشكلة.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

القواعد:
- (log(a * b) = (log(a) + (log(b)
- احتمالات التسجيل هي دائما <= 0 (منذ 0 < P <= 1)
- أكثر سلبية = أقل احتمال
- الخسارة المتقاطعة للاندروبي هي احتمال السجل السلبي للدرجة الصحيحة

> 规则:
> - (log(a * b) = (log(a) + (log(b)
> - على احتمالية العدد总是 <= 0(لأن 0 < P <= 1)
> - 越负 = 越不可能
> - 交叉 خسارة هو الصواب من الصف السلبي مقابل احتمالات العدد

### Softmax كوزع احتمال

الشبكات العصبية تنتج النتائج الخامة (اللوجيتس). تحويلها Softmax إلى توزيع محتمل صالح.

> 神经网络输出原始分数(لوجيتس) ――Softmax سوف تحويلها إلى انتشار احتمال فعال

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

خدعة softmax: سحب الحد الأقصى قبل التعريض لمنع الإفراط.

> المهارات: قبل خفض النسبة القصوى من المعدل، لمنع التسرب.

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax يجمع بين softmax و log لتحقيق الاستقرار الرقمي. يستخدم PyTorch هذا داخلياً لخسارة الانتروبيا المتقاطعة.

> سيقوم Log-softmax بتحقيق softmax و log 合并 بخطوة للحفاظ على استقرار القيمة العددية.

### أخذ العينات

تعني أخذ العينات استنتاج قيم عشوائية من توزيع.
- أترك عينات عشوائية من الخلايا العصبية إلى الصفر
  中文翻译:تجريد 随机采样决定哪些神经元置零
- عينات زيادة البيانات تحويلات عشوائية
  中文翻译: بيانات زيادة الصورة تغير
- نموذج اللغة عينة الرمز التالي من التوزيع المتوقع
  中文翻译:语言模型从预测分布中采样下一个词
- نماذج التفريق تجميع الضوضاء وتحذيرها تدريجيا
  中文翻译: انتشار النموذج采样噪声并逐步去噪声

يتطلب أخذ العينات من التوزيعات التعسفية تقنيات مثل أخذ العينات من التحول العكسي، أو أخذ العينات من الرفض، أو خدعة إعادة التقييم (المستخدمة في VAEs).

> من التوزيع المتردد في الاختراع يحتاج إلى التغيير العكسي في الاختراع، أو رفض الاختراع أو تقنيات الاختراع الثقيل.

## بناء ذلك تحرك لتحقيق
```figure
gaussian-pdf
```

## بناءها

### الخطوة الأولى: أساسيات الاحتمال

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### الخطوة الثانية: PMF و PDF من الصفر

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### الخطوة الثالثة: القيمة المتوقعة والتشابه

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### الخطوة الرابعة: أخذ العينات من التوزيعات

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### الخطوة 5: Softmax و احتمالات السجل

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### الخطوة 6: إثبات نظرية الحد المركزي

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### الخطوة السابعة: التصور

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

التنفيذ الكامل مع جميع التصورات في `code/probability.py`. . .

> يحتوي على كل التطبيقات المُبصرة`code/probability.py`.

## استخدمها في إطار التنفيذ

مع NumPy و SciPy، كل شيء أعلاه هو خط واحد:

> استخدام NumPy و SciPy، جميع المهام فوق تحتاج فقط إلى صف من الكود:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

لقد بنيت هذه من الصفر، والآن تعرف ما الذي تفعله المكتبة

> لقد بنيت هذه من الصفر. الآن تعرف ما الذي تفعله وظيفة المكتبة.

## تمارين التدريب

1. قم بتنفيذ أخذ العينات من تحويل العكس للتوزيع المتعرض. تحقق من خلال أخذ العينات من 10،000 قيم ومقارنة الرسم البياني مع PDF الحقيقي.

2. قم ببناء جدول توزيع مشترك لـ 2 كرة من الكرة المثبتة، احسب التوزيعات الهامشية وتحقق من أن الكرة مستقلة.

3. احسب الخسارة المتقاطعة للاندروبي لـ 5 فئة تصنيف يخرج التسجيلات `[2.0, 0.5, -1.0, 3.0, 0.1]`عندما يكون الفئة الصحيحة هو المؤشر 3. ثم التحقق من إجابتك مع PyTorch `nn.CrossEntropyLoss`. . .

4. اكتب وظيفة تأخذ قائمة من احتمالات السجل وتعطي التسلسل الأكثر احتمالا، والاحتمالات السجلية الإجمالية، والاحتمالات الخام المكافئة. اختبره بعبارة من 50 كلمة حيث كل كلمة لديها احتمال 0.01.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## المزيد من القراءة

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- دليل بصري على سبب تصبح المتوسطات طبيعية
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- إشارة موجزة تغطي كل شيء هنا وأكثر
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- لماذا الاستقرار الرقمي مهم وكيفية تحقيقه
