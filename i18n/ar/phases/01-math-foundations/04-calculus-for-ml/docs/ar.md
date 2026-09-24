# الحسابات للتعلم الآلي

> المشتقات تخبرك في أي طريق هو الهبوط هذا كل ما تحتاج الشبكة العصبية إلى تعلمه

> 导数告诉你哪边是下坡方向                                                                                                                                                                                                                                                         

**Type:** Learn | **类型:** 学习
**Language:**" بايثون "**语言:**بايثون
**Prerequisites:** Phase 1, Lessons 01-03 | **前置知识:** Phase 1, Lessons 01-03
**Time:** ~60 minutes | **时间:** ~60 分钟

## أهداف التعلم

- محاسبة المشتقات العددية والتحليلية للعملات المشتركة للطاقة المعدنية (x^2, sigmoid, cross-entropy)
  计算常见 ML 函数(x^2、sigmoid、交叉) من عدد القيم والحسابات والتحليلات
- تنفيذ انخفاض التدرج من الصفر لتقليل وظيفة الخسارة في 1D و 2D
  من صفر تحقيق التدريج إلى أسفل، في 1D و 2D الحد الأدنى من خسارة وظيفة
- استنباط تراجع النموذج الخطوي وتدريبها عن طريق تحديثات الوزن اليدوية
  推导线性回归模型的梯度,并通过手动权重更新进行训练
- شرح المصفوفة الهسسيّة، مقربات سلسلة تايلور، وربطها بأساليب التحسين
   شرح هيسيان 矩阵、تايلور درجة عدد التقريب والارتباط مع طريقة التحسين

> **【中文解读】**
> 导数告诉你"往哪个方向走可以让差差变小"―― هناك ملايين من العناصر في شبكة العصبية، كل عنصر هو "دوار" واحد، 微积分告诉你每旋转应往哪个方向调――梯度下降就是沿着导数反方向步步走到最小值――

> **【拓展：微积分与神经网络】**
> - **梯度下降**: الجهاز الأساسي للتدريب على شبكات العصبية  على طول التدابير المتضاربة
> - **SGD/Adam**: كانت تغيرات تراجعة انخفاض، ودم اضاف إلى الحركة والتكيف معدل التعلم.
> - **学习率**梯度下降的步长──太大则跳过最小值,太小则收太慢──

## المشكلة المشكلة المشكلة

> **【中文解读】**شبكة العصبية لديها مليون وزن (((دوار)) ، التدريب هو العثور على كل دورة يجب أن تتحول إلى أي اتجاه.

## المفهوم الأساسي

> **【拓展：偏导数就是"只动一个旋钮看效果"]**وظيفة فقدان شبكة العصبية L(w1، w2، ..., wn) 有百万个变量──偏导数 ∂L/∂w_i 告诉你"只改变w_i 权重,损失变化多少"──梯度就是把所有偏导数组合成一个向量,指向"最的上坡方向",所以沿负梯度走就是最快的下坡路──

### ما هو المشتق؟

المشتقات تقيس معدل التغيير. بالنسبة لـ y = f(x) ، فإن المشتقات f'(x) تخبرك: إذا قمت بتشغيل x بمقدار صغير، كم يغير؟

> 导数衡量变化率──对于函数 y = f(x),导数 f'(x) 告诉你: إذا x 微小变化,y 变化多少?

من الناحية الجيموترية، المشتق هي ميل الخط المتعلق في نقطة.

> على الجوهر، العدد الموجّه هو التوجه من نقطة قطع خط.

**f(x) = x^2:**

| x | f(x) | f'(x) (slope) |
|---|------|---------------|
| 0 | 0    | 0 (flat, at the bottom) |
| 1 | 1    | 2 |
| 2 | 4    | 4 (tangent line slope at this point) |
| 3 | 9    | 6 |

عند x=2، فإن الميل هو 4 إذا حركت x قليلا إلى اليمين، يزيد من حوالي 4 مرات هذا المبلغ. عند x=0، الميل هو 0. أنت في أسفل الصحن.

> في x=2 处,斜率为 4── إذا كنت ستحرك x إلى اليمين بقطعة واحدة,y تقريبا زيادة 4 مرات من هذه الحركة── في x=0 处,斜率为 0你正处"碗底"──

التعريف الرسمي:

```
f'(x) = lim   f(x + h) - f(x)
        h->0  -----------------
                     h
```

في الرمز، تخطي الحد وتستخدم فقط h صغير جدا. هذا هو المشتق الرقمي.

> في كود، قفز فوق الحد الأقصى، مباشرة باستخدام h صغير جدا لتقريبها.

### المشتقات الجزئية: متغير واحد في كل مرة

المواد الحقيقية لديها العديد من المدخلات. فقدان الشبكة العصبية يعتمد على آلاف الوزن. المشتق جزئي يحتفظ جميع المتغيرات ثابتة باستثناء واحدة، ثم يأخذ المشتق فيما يتعلق بذلك واحد.

> المهام الحقيقية لديها العديد من الإدخالات. وظيفة فقدان الشبكة العصبية تعتمد على آلاف الوزن. الحفاظ على الاختلافات الأخرى غير متغيرة، فقط على متغير واحد.

```
f(x, y) = x^2 + 3xy + y^2

df/dx = 2x + 3y     (treat y as a constant)
df/dy = 3x + 2y     (treat x as a constant)
```

كل مشتق جزئي يجيب: إذا دفعت فقط هذا الوزن واحد، كيف يتغير الخسارة؟

> كل محور يرد: إذا قمت فقط بتحريك هذا الوزن، كم تغير الخسارة؟

### المتحدر: متجه لجميع المشتقات الجزئية

الجدار يجمع كل مشتق جزئي إلى متجه واحد. بالنسبة للعمل f ((x، y، z) ، الجدار هو:

> 梯度把所有偏导数 جمع في واحد向量── بالنسبة للعمل f ((x, y, z) ، 梯度为:

```
grad f = [ df/dx, df/dy, df/dz ]
```

يُحدّد التسلّل في اتجاه صعود أكثر خطورة، لتحقيق الحدّ الأدنى من وظيفة، اذهب في الاتجاه المعاكس.

> 梯度指向最上升方向──要最小化函数,就沿相反方向走──

**Contour plot of f(x,y) = x^2 + y^2:**

تشكل الوظيفة شكل وعاء مع دائرات مركزة كخطوط شكل. الحد الأدنى هو (0, 0).

> هذه الوظيفة تشكل شكلًا شكلًا كوعة ، وبالطبع تكون مع حلقة مركزية.

| Point | grad f | -grad f (descent direction) |
|-------|--------|----------------------------|
| (1, 1) | [2, 2] (points uphill, away from minimum) | [-2, -2] (points downhill, toward minimum) |
| (0, 0) | [0, 0] (flat, at the minimum) | [0, 0] |

> 梯度方向指向最上坡,负梯度方向指向最下坡 ((即朝向最小值) ⋅在最小值处梯度为零──

هذا هو انخفاض التراجع في صورة حساب التراجع، سلبه، اتخاذ خطوة.

> هذا هو الرسم البياني للدرجة المنخفضة.

### الارتباط مع التحسين

تدريب شبكة عصبية هو تحسين. لديك وظيفة الخسارة L ((w1، w2، ..., wn) التي تقيس مدى خطأ النموذج. تريد تقليل ذلك.

> 训练神经网络就是优化──损失函数 L(w1,w2, ..., wn) 衡模型有多"错",你要最小化它──

```
Gradient descent update rule:

  w_new = w_old - learning_rate * dL/dw

For every weight:
  1. Compute the partial derivative of loss with respect to that weight
  2. Subtract a small multiple of it from the weight
  3. Repeat
```

> 梯度下降规则: 新权重 = 旧权重 - 学习率 × 梯度──重复:1) حساب عدد التحركات لكل وزن؛2) خفض من الوزن من عدد ضخم من الوزن؛3) 代数百万次。

معدل التعلم يحدد حجم الخطوة، كبير جداً و أنت تتجاوز، صغير جداً و أنت تتجول.

> معدل التعلم التحكم على التقدم.

**Loss landscape (1D slice):**

تُشكّل وظيفة الخسارة L ((w) منحنى مع القمم والوعيّات مع تغير الوزن w.

> 损失函数 L(w) 随权重 w 变化形成带峰和谷的曲线──

| Feature | Description |
|---------|-------------|
| Global minimum | The lowest point on the entire curve -- the best solution |
| Local minimum | A valley that is lower than its neighbors but not the lowest overall |
| Slope | Gradient descent follows the slope downhill from any starting point |

> الحد الأدنى للمناطق المحلية هو أدنى نقطة في جميع أنحاء منحنى؛ الحد الأدنى للمناطق المحلية هو أقل من الجوار ولكن ليس أدنى من المناطق المحلية في وادي؛ وتراجع التسلسل من أي نقطة من المراكز على طول المرتفعات إلى أسفل.

يتبع التنحدر التدريجي التسلل الهبوطي. يمكن أن يعلق في الحد الأدنى المحلي، ولكن في المساحات العالية الأبعاد (ملايين الوزن) هذه نادرًا ما تكون مشكلة عملية.

> 梯度下降沿坡下行──可能陷入局部最小值, ولكن في高维空间中 (مليون درجة الوزن) ، هذا نادرًا ما يصبح مشكلة فعلية──

### المشتقات الرقمية مقابل التحليلية

هناك طريقتان لحساب مشتق

> هناك طريقتان في الحساب

التحليلي: تطبيق قواعد الحساب يدويا. بالنسبة f  x) = x^2, المشتق هي f  x) = 2x. بالضبط. سريع.

> 解析法:手动应用微积分规则──如 f(x) = x^2 的导数是 f'(x) = 2x──精确且快速──

عددي: تقريري باستخدام التعريف. حساب f ((x+h) و f ((x-h) لـ h صغير، ثم استخدام الفرق.

> عدد القيمة: مع تعریف تقاربها. حساب f  x + h) 和 f  x - h) ، مع فرق القيمة من خلال 2h.

```
Numerical (central difference):

f'(x) ~= f(x + h) - f(x - h)
          -----------------------
                  2h

h = 0.0001 works well in practice
```

المشتقات الرقمية بطيئة ولكن تعمل لأي وظيفة. المشتقات التحليلية سريعة ولكن تتطلب منك استنباط الصيغة. استخدام إطار الشبكات العصبية نهج ثالث: التمييز الآلي، الذي يحسب المشتقات الدقيقة ميكانيكيا. سترى ذلك في المرحلة 3.

> تعديلات الأرقام بطيئة ولكن تطبق على أي وظيفة. تحليل تعديلات السرعة ولكن يحتاج إلى التوجيه اليدوي.

### المشتقات المستخدمة يدوياً للعمل البسيط

هذه هي المشتقات التي ستراها مرارا وتكرارا في ML.

> هذه هي العدد الذي ستراه في المادة الثنائية

```
Function        Derivative       Used in
--------        ----------       -------
f(x) = x^2     f'(x) = 2x      Loss functions (MSE)
f(x) = wx + b  f'(w) = x        Linear layer (gradient w.r.t. weight)
                f'(b) = 1        Linear layer (gradient w.r.t. bias)
                f'(x) = w        Linear layer (gradient w.r.t. input)
f(x) = e^x     f'(x) = e^x     Softmax, attention
f(x) = ln(x)   f'(x) = 1/x     Cross-entropy loss
f(x) = 1/(1+e^-x)  f'(x) = f(x)(1-f(x))   Sigmoid activation
```

بالنسبة f ((x) = x^2:

```
f(x) = x^2    f'(x) = 2x

  x    f(x)   f'(x)   meaning
  -2    4      -4      slope tilts left (decreasing)
  -1    1      -2      slope tilts left (decreasing)
   0    0       0      flat (minimum!)
   1    1       2      slope tilts right (increasing)
   2    4       4      slope tilts right (increasing)
```

> في x<0 时导数为负(函数递减),x=0 时导数为零(وصول إلى الحد الأدنى من القيمة),x>0 时导数为正(函数递增) ⋅

بالنسبة f(w) = wx + b مع x=3، b=1:

```
f(w) = 3w + 1    f'(w) = 3

The derivative with respect to w is just x.
If x is big, a small change in w causes a big change in output.
```

> وبالنسبة لـ w  التوجيه النتيجة هي x في الواقع. إذا كان x  كبير جدا، w التغيرات الصغيرة سوف يؤدي إلى تغييرات ضخمة في الناتج.

### قاعدة السلسلة

عندما تكون الوظائف مرتبة، قاعدة السلسلة تخبرك كيفية التمييز.

> عندما تكون الوظيفة مُختلطة، فإن قواعد الدرجة التالية تخبرك كيف تطلب الإرشاد.

```
If y = f(g(x)), then dy/dx = f'(g(x)) * g'(x)

Example: y = (3x + 1)^2
  outer: f(u) = u^2       f'(u) = 2u
  inner: g(x) = 3x + 1    g'(x) = 3
  dy/dx = 2(3x + 1) * 3 = 6(3x + 1)
```

شبكات العصبية هي سلسلة من الوظائف: المدخل -> خطي -> تفعيل -> خطي -> تفعيل -> خسارة. التنشر الخلفي هو قاعدة سلسلة تطبق مرارا من الخروج إلى المدخل. وهذا هو الخوارزمية بأكملها.

> النظام العصبي هو سلسلة وظيفية:输入 -> 线性 -> 激活 -> 线性 -> 激活 -> 损失──反向传播就是从输出到输入反复应用链式法则──这是整个算法──

### المصفوفة الهيسي

المرتفعات تخبرك بالمهد، والحسية تخبرك بالمنعطف

> التعدد يخبرك التوالي، الموجة هيسيان يخبرك التوالي

المادية الهسسي هي المصفوفة من المشتقات الجزئية من النظام الثاني. بالنسبة للعمل f ((x1، x2، ..., xn) ، فإن مدخل (i، j) من المادية الهسسي هو:

> هيسيان هي المجموعة المكونة من المكونات المكونة.

```
H[i][j] = d^2f / (dx_i * dx_j)
```

لـ 2 متغيرات f ((x، y):

```
H = | d^2f/dx^2    d^2f/dxdy |
    | d^2f/dydx    d^2f/dy^2 |
```

**What the Hessian tells you at a critical point (where gradient = 0):**

> هيسيان في نقطة الحد الأدنى (درجة = 0) أخبرك: هل هو الحد الأدنى من المحطة أو الحد الأقصى من المحطة أو الحد الأقصى من النقطة

| Hessian property | Meaning | Example surface |
|-----------------|---------|-----------------|
| Positive definite (all eigenvalues > 0) | Local minimum | Bowl pointing up |
| Negative definite (all eigenvalues < 0) | Local maximum | Bowl pointing down |
| Indefinite (mixed eigenvalues) | Saddle point | Horse saddle shape |

> 正定(所有特征值 > 0) = 局部最小值;负定(所有特征值 < 0) = 局部最大值;不定(特征值有正有负) = 点。

**Example:**f(x, y) = x^2 - y^2 (عمل السرير)

```
df/dx = 2x       df/dy = -2y
d^2f/dx^2 = 2    d^2f/dy^2 = -2    d^2f/dxdy = 0

H = | 2   0 |
    | 0  -2 |

Eigenvalues: 2 and -2 (one positive, one negative)
--> Saddle point at (0, 0)
```

مقارنة مع f ((x, y) = x^2 + y^2 (وعاء):

```
H = | 2  0 |
    | 0  2 |

Eigenvalues: 2 and 2 (both positive)
--> Local minimum at (0, 0)
```

**Why the Hessian matters in ML:**

> هيسيان في ML: نيوتن قانون استخدام هيسيان 修改梯度方向,使方向走小步、平坦方向走大步,从而比梯度下降更快收──

تستخدم طريقة نيوتن خطوات التحسين الأفضل من تراجع التراجع. بدلاً من اتباع التنحى فحسب، فإنها تأخذ بعين الاعتبار منحنى:

```
Newton's update:    w_new = w_old - H^(-1) * gradient
Gradient descent:   w_new = w_old - lr * gradient
```

> نيوتن 更新:w_new = w_old - H−1 × gradient── يستخدم المعدل المتحرك لتقليل التعدد──

طريقة نيوتن تتقارب أسرع لأن "إعادة تقييم" هيسيان التدفق -- الاتجاهات الرافية تحصل على خطوات أصغر، الاتجاهات المسطحة تحصل على خطوات أكبر.

> نيوتن لا يستقبل أسرع، لأن "إعادة التكبير" في هيسينية تدرج في اتجاه خطوة صغيرة، في اتجاه مسطح في اتجاه خطوة كبيرة.

المشكلة: لشبكة عصبية مع N المعلمات، هي Hessian N x N. نموذج مع 1 مليون المعلمات سوف تحتاج إلى 1 تريليون مدخل المصفوفة. وهذا هو السبب في أننا نستخدم التقارير.

> المشكلة تكمن في: شبكة N 个参数, Hessian هو N × N.

| Method | What it uses | Cost | Convergence |
|--------|-------------|------|-------------|
| Gradient descent | First derivatives only | O(N) per step | Slow (linear) |
| Newton's method | Full Hessian | O(N^3) per step | Fast (quadratic) |
| L-BFGS | Approximate Hessian from gradient history | O(N) per step | Medium (superlinear) |
| Adam | Per-parameter adaptive rates (diagonal Hessian approx) | O(N) per step | Medium |
| Natural gradient | Fisher information matrix (statistical Hessian) | O(N^2) per step | Fast |

> 不同优化器对比:梯度下降只用一阶导数(O(N),慢);نيوتن 法用完整赫西安(O(N3),快但太贵);L-BFGS用梯度历史近似赫西安;Adam用对角赫西安近似做每参数自适应;自然梯度用 Fisher 信息矩阵。

في الممارسة العملية، آدم هو المحسن الافتراضي للتعلم العميق. إنه يقترب من المعلومات من الدرجة الثانية بأسعار رخيصة عن طريق تتبع المتوسط الجاري وتباين التدرج لكل پیرامتر.

> في الواقع، آدم هو المحافظ الاختيارية للتعلم العميق.

### تقارب سلسلة تايلور

يمكن تقريب أي وظيفة سلاسة محليا عن طريق الكتلة:

> أي وظيفة مسطحة يمكن أن تكون مقاربة في محلية باستخدام العديد من الجوانب.

```
f(x + h) = f(x) + f'(x)*h + (1/2)*f''(x)*h^2 + (1/6)*f'''(x)*h^3 + ...
```

كلما تضيف المزيد من المصطلحات، كلما كانت التقريبات أفضل -- ولكن فقط بالقرب من النقطة x.

> 包含的项越多,近似越好但只有效在x 附近──一阶梯泰勒 = 梯度下降,二阶梯泰勒 = 牛顿法──

**Why Taylor series matter for ML:**

- **First-order Taylor = gradient descent.**عندما تستخدم f(x + h) ~ f(x) + f'(x) *h، فإنك تقوم بتقريب خطي. يقلل التنزل التدريجي هذا النموذج الخطي للاختيار h = -lr * f'(x.

- **Second-order Taylor = Newton's method.**باستخدام f(x + h) ~ f(x) + f'(x) *h + (1/2) *f'(x) *h^2 ، تحصل على نموذج مربع. تحد من ذلك يمنح h = -f'(x) / f'(x) -- خطوة نيوتن.

- **Loss function design.**إن MSE و entropy متسطّة، مما يعني أنّ توسعاتها Taylor تتصرف بشكل جيد. هذه ليست حادثة. الخسائر السلسة تجعل التكيفّيّة قابلة للتنبؤ.

> عدد تايلور في ML معنى: 1 مرحلة تايلور = 线性近似 = 梯度下降; 2 مرحلة تايلور = 2 مرتين近似 = نيوتن 法;MSE 和交叉 的平滑性不是巧合平滑损失让优化可预测──

```
Approximation order    What it captures    Optimization method
-------------------    -----------------   -------------------
0th order (constant)   Just the value      Random search
1st order (linear)     Slope               Gradient descent
2nd order (quadratic)  Curvature           Newton's method
Higher orders          Finer structure     Rarely used in ML
```

> مقارنة مع الحد الأدنى: 0 阶只用值(随机搜索); 1 阶用斜率(梯度下降); 2 阶用曲率(Newton 法);更高阶在ML很少使用──

المفهوم الرئيسي: كل التحسين القائم على التراجع هو حقا حول تقريب وظيفة الخسارة محليا وتحقيق الحد الأدنى من هذا التقريب.

> 关键洞见: جميع المحافظات المستندة إلى التعدد هي على طبيعتها في وظيفة الخسارة المقاربة المحلية، ثم تذهب إلى نقطة القليل المقاربة.

### الإجماليات في ML

المشتقات تخبرك بمعدلات التغيير. الكاملات تحسب التراكم -- المساحة تحت منحنى.

> 导数告诉你变化率,积分计算累积(曲线下面积)

في ML، نادراً ما تقوم بحساب التكاملات يدوياً، لكن المفهوم موجود في كل مكان:

> في المعلمين الاكتسابات القليلة، ولكن مفهوم الاكتسابات لا يوجد:

**Probability.**بالنسبة لمتغير عشوائي مستمر مع كثافة p ((x):
```
P(a < X < b) = integral from a to b of p(x) dx
```
المساحة تحت منحنى كثافة الاحتمال بين a و b هي احتمال الهبوط في هذا النطاق.

> **概率**: للقيام بتغيرات متواصلة، وظيفة الدرجة p(x) في [a، b] 区间积分就是落在此区间的概率──

**Expected value.**النتيجة المتوسطة الموزعة بالاحتمال:
```
E[f(X)] = integral of f(x) * p(x) dx
```
الخسارة المتوقعة على توزيع البيانات هي جزء لا يتجزأ. التدريب يقلل من التقريب التجريبي لهذا.

> **期望**:加权平均── المتوقع أن تخسر التوزيع على البيانات هو واحد积分، التدريب على تقليل تجربته تقريبا──

**KL divergence.**تقيس مدى اختلاف توزيعين:
```
KL(p || q) = integral of p(x) * log(p(x) / q(x)) dx
```
يستخدم في VAEs، نزيف المعرفة، والإستنتاج البايسي.

> **KL 散度**: قياس اختلافات توزيعيّتين.

**Normalization constants.**في استنتاج بايزي:
```
p(w | data) = p(data | w) * p(w) / integral of p(data | w) * p(w) dw
```
المعاد هو جزء متكامل على جميع قيم المعلمات المحتملة. غالبا ما يكون غير قابلة للتحدي، وهذا هو السبب في أننا نستخدم التقريبات مثل MCMC والإستنتاج المتغير.

> **归一化常数**: في فرضية بيليس، النسبة هي النسبة من جميع القيم المعادلة المحتملة، عادة لا يمكن تحديدها.

| Integral concept | Where it appears in ML |
|-----------------|----------------------|
| Area under curve | Probability from density functions |
| Expected value | Loss functions, risk minimization |
| KL divergence | VAEs, policy optimization, distillation |
| Normalization | Bayesian posteriors, softmax denominator |
| Marginal likelihood | Model comparison, evidence lower bound (ELBO) |

> 积分概念在 ML 中体现:曲线下面积(密度函数求概率) 期望(损失函数) 、KL 散度(VAE/蒸) 归结(贝叶斯后验/softmax 分母) 边际似然(模型比较/ELBO) ✿

### قاعدة سلسلة متعددة المتغيرات في الرسم البياني الحسابي

لا تنطبق قاعدة السلسلة على الوظائف المتعددة في خط. في شبكة عصبية، تتراوح المتغيرات وتدمج. إليك كيف تتدفق المشتقات من خلال مرور بسيط للأمام:

> قانون سلسلة الكميات متعددة التغيرات لا ينطبق فقط على وظيفة الكميات اللاسلكية. في شبكة العصبية، يتفرق التغيرات في شبكة التداول والتشبث.

```mermaid
graph LR
    x["x (input)"] -->|"*w"| z1["z1 = w*x"]
    z1 -->|"+b"| z2["z2 = w*x + b"]
    z2 -->|"sigmoid"| a["a = sigmoid(z2)"]
    a -->|"loss fn"| L["L = -(y*log(a) + (1-y)*log(1-a))"]
```

الممر الخلفي يحسب التراجع من يمين إلى يسار:

```mermaid
graph RL
    dL["dL/dL = 1"] -->|"dL/da"| da["dL/da = -y/a + (1-y)/(1-a)"]
    da -->|"da/dz2 = a(1-a)"| dz2["dL/dz2 = dL/da * a(1-a)"]
    dz2 -->|"dz2/dw = x"| dw["dL/dw = dL/dz2 * x"]
    dz2 -->|"dz2/db = 1"| db["dL/db = dL/dz2 * 1"]
```

كل سهم يضاعف بمشتقات محلية. تراجع لأي معادلة هو ناتج من جميع المشتقات المحلية على طول المسار من الخسارة إلى تلك المعادلة. عندما تتفرق المسارات وتدمج، يمكنك جمع المساهمات (قاعدة سلسلة متعددة المتغيرات).

> كل شريحة ضربة على الدرجة المحلية. درجة أي عنصر = ضربة جميع الدرجات المحلية على مسار الدرجة المحلية من الخسارة إلى مسار الدرجة المحلية. عند توزيع المسار والجمع، يجب أن تضيف كل مساهمة إلى الدرجة الحرة.

هذا كل التنشر الخلفي هو: قاعدة سلسلة تطبق بشكل منهجي من خلال الرسم البياني الحسابي، من الخروج إلى المدخلات.

> كل ما هو في التوزيع المتردد هو: في رسم الحساب من الخروج إلى الإدخال نظامية في قواعد التطبيقات.

### المصفوفة جاكوبية

عندما تقوم وظيفة بتخريط متجه إلى متجه (مثل طبقة شبكة عصبية) ، فإن مشتقها هو المصفوفة. يحتوي جيكوبيان على كل مشتق جزئي لكل خروج فيما يتعلق بكل مدخل.

> عندما تقوم الوظيفة بتخطي محورها إلى محورها مثل طبقة النظام العصبي ، فإن محورها هو محور جاكوبي 包含 كل إصدار على كل إدخال 

بالنسبة إلى f: R^n -> R^m، فإن J Jacobian هو ماتريكس m x n:

> بالنسبة لـ f: R^n → R^m، Jacobian J هو m × n 矩阵:

| | x1 | x2 | ... | xn |
|---|---|---|---|---|
| f1 | df1/dx1 | df1/dx2 | ... | df1/dxn |
| f2 | df2/dx1 | df2/dx2 | ... | df2/dxn |
| ... | ... | ... | ... | ... |
| fm | dfm/dx1 | dfm/dx2 | ... | dfm/dxn |

لن تقوم بحساب الجيكوبيانات يدوياً لشبكات العصبية. يديرها بيتورش. ولكن معرفة وجودها تساعدك على فهم الأشكال في الانتشار الخلفي: إذا كانت الطبقة تقوم بتخطيط R^n إلى R^m، فإن جيكوبيانها m x n. يتدفق التدفق الخلفي عبر نقل هذه المصفوفة.

> لن تُحسب شبكة الـ JacobianPyTorch العصبية تلقائياً. ولكن معرفة وجودها يمكن أن يساعدك على فهم الشكل المتردد في التنقل: إذا كان الطبقة يُخطي R^n إلى R^m، فإن Jacobian هو m×n، تدرج من خلال تحويله إلى التنقل المتردد.

### لماذا هذا مهم للشبكات العصبية

كل وزن في شبكة عصبية يحصل على تراجع. تراجع يخبرك كيفية ضبط هذا الوزن لتقليل الخسارة.

> كل وزن في شبكة العصبية لديه درجة، يخبرك كيفية تعديل هذا الوزن لتقليل الخسارة

```mermaid
graph LR
    subgraph Forward["Forward Pass"]
        I["input"] --> W1["W1"] --> R["relu"] --> W2["W2"] --> S["softmax"] --> L["loss"]
    end
```

```mermaid
graph RL
    subgraph Backward["Backward Pass"]
        dL["dL/dloss"] --> dW2["dL/dW2"] --> d2["..."] --> dW1["dL/dW1"]
    end
```

كل تحديث للوزن:
- `W1 = W1 - lr * dL/dW1`
- `W2 = W2 - lr * dL/dW2`

> كل وزن تحديث:W = W - lr × dL/dW──前向计算预测和损失,反向计算每个权重的梯度,每个权重沿梯度负方向走一小步──

المخطط الأمامي يحسب التنبؤ والخسارة، المخطط الخلفي يحسب تراجع الخسارة فيما يتعلق بكل وزن، ثم كل وزن يأخذ خطوة صغيرة أسفل التلال. كرر لملايين الخطوات. وهذا هو التعلم العميق.

> قبل نحو التنشر حساب التنبؤ والخسارة، والعكس نحو التنشر حساب كل وزن من التسلسلات، ثم كل وزن على طول التسلسلات الاتجاه السلبي يذهب إلى خطوة صغيرة.

## بناء ذلك تحرك لتحقيق
```figure
derivative-tangent
```

## بناءها

### الخطوة الأولى: المشتق العددي من الصفر

```python
def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def f(x):
    return x ** 2

for x in [-2, -1, 0, 1, 2]:
    numerical = numerical_derivative(f, x)
    analytical = 2 * x
    print(f"x={x:2d}  f'(x) numerical={numerical:.6f}  analytical={analytical:.1f}")
```

> استخدام مركز الفارق لتحقيق عدد القيم المحددة. h=1e-7 عادة ما يكون دقيقة جدا.

المشتق العددي يطابق المشتق التحليلي مع العديد من الأماكن العشرية.

> يثبت استناداة النظام المركزي للفرق في النظام المركزي على عدد من نقاط بعد عدد صغير.

### الخطوة الثانية: مشتقات جزئية ومحافظات

```python
def numerical_gradient(f, point, h=1e-7):
    gradient = []
    for i in range(len(point)):
        point_plus = list(point)
        point_minus = list(point)
        point_plus[i] += h
        point_minus[i] -= h
        partial = (f(point_plus) - f(point_minus)) / (2 * h)
        gradient.append(partial)
    return gradient

def f_multi(point):
    x, y = point
    return x**2 + 3*x*y + y**2

grad = numerical_gradient(f_multi, [1.0, 2.0])
print(f"Numerical gradient at (1,2): {[f'{g:.4f}' for g in grad]}")
print(f"Analytical gradient at (1,2): [2*1+3*2, 3*1+2*2] = [{2*1+3*2}, {3*1+2*2}]")
```

> عدد التعدد القيم: لـ لكل درجة مستقلة عن مركزها اختلاف التعدد المتجه إلى التوجه، مجموعة مركز التعدد المتجه إلى التوجه، تجربة f ((x,y) = x2+3xy+y2 在 (1,2) 处的梯度为 [8, 7]。

### الخطوة الثالثة: التراجع التدريجي للعثور على الحد الأدنى من f ((x) = x^2

```python
x = 5.0
lr = 0.1
for step in range(20):
    grad = 2 * x
    x = x - lr * grad
    print(f"step {step:2d}  x={x:8.4f}  f(x)={x**2:10.6f}")
```

بدءا من x=5، كل خطوة تتحرك أقرب إلى x=0 (الأقل).

> من x=5 خرجت, كل خطوة اقتربت من x=0 ((أقل قيمة)  معدل التعلم 0.1 让 x 逐步缩小到接近0。

### الخطوة الرابعة: انخفاض درجي على وظيفة 2D

```python
def f_2d(point):
    x, y = point
    return x**2 + y**2

point = [4.0, 3.0]
lr = 0.1
for step in range(30):
    grad = numerical_gradient(f_2d, point)
    point = [p - lr * g for p, g in zip(point, grad)]
    loss = f_2d(point)
    if step % 5 == 0 or step == 29:
        print(f"step {step:2d}  point=({point[0]:7.4f}, {point[1]:7.4f})  f={loss:.6f}")
```

> 2D 梯度下降: من (4, 3) 出发,每步更新点 -= lr × grad,逐步收到 (0, 0) 』

### الخطوة 5: مقارنة المشتقات العددية والتحليلية

```python
import math

test_functions = [
    ("x^2",      lambda x: x**2,          lambda x: 2*x),
    ("x^3",      lambda x: x**3,          lambda x: 3*x**2),
    ("sin(x)",   lambda x: math.sin(x),   lambda x: math.cos(x)),
    ("e^x",      lambda x: math.exp(x),   lambda x: math.exp(x)),
    ("1/x",      lambda x: 1/x,           lambda x: -1/x**2),
]

x = 2.0
print(f"{'Function':<12} {'Numerical':>12} {'Analytical':>12} {'Error':>12}")
print("-" * 50)
for name, f, df in test_functions:
    num = numerical_derivative(f, x)
    ana = df(x)
    err = abs(num - ana)
    print(f"{name:<12} {num:12.6f} {ana:12.6f} {err:12.2e}")
```

> مقابل 5 أشكال من المهام الشائعة في x=2 ة من محورات القيمة والحصول على القيمة: x2、x3、sin(x)、e^x、1/x。 الخلطات عادة في 1e-10 ة من الدرجة الكمية، صحيحة طريقة تحديد القيمة..

### الخطوة 6: حساب الهسسي عددا

```python
def hessian_2d(f, x, y, h=1e-5):
    fxx = (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h ** 2)
    fyy = (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h ** 2)
    fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h ** 2)
    return [[fxx, fxy], [fxy, fyy]]

def saddle(x, y):
    return x ** 2 - y ** 2

def bowl(x, y):
    return x ** 2 + y ** 2

H_saddle = hessian_2d(saddle, 0.0, 0.0)
H_bowl = hessian_2d(bowl, 0.0, 0.0)
print(f"Saddle Hessian: {H_saddle}")  # [[2, 0], [0, -2]] -- mixed signs
print(f"Bowl Hessian:   {H_bowl}")    # [[2, 0], [0, 2]]  -- both positive
```

> 数值计算 هيسيان 矩阵:fxx、fyy 是二阶偏导,fxy 是混合偏导,点函数 x2-y2 的 هيسيان 是 [[2,0],[0,-2]](一正一负=点),碗形 x2+y2 是 [[2,0],[0,2]](均正=最小值)。

يحتوي الحسسي لـ 2 و -2 (أشارة مختلطة تؤكد نقطة السرير). والقوطة لديها قيم خاصة 2 و 2 (كلتا إيجابية، تؤكد الحد الأدنى).

>  نقطة من وظيفة هيسيان خصصات قيمة هي 2 和 -2(一正一负, يعتقد点); وعاء شكل وظيفة هيسيان خصصات قيمة هي 2(均正, يعتقد أدنى قيمة)。

### الخطوة 7: تقريب تايلور في العمل

```python
import math

def taylor_approx(f, f_prime, f_double_prime, x0, h, order=2):
    result = f(x0)
    if order >= 1:
        result += f_prime(x0) * h
    if order >= 2:
        result += 0.5 * f_double_prime(x0) * h ** 2
    return result

x0 = 0.0
for h in [0.1, 0.5, 1.0, 2.0]:
    true_val = math.sin(h)
    t1 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=1)
    t2 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=2)
    print(f"h={h:.1f}  sin(h)={true_val:.4f}  order1={t1:.4f}  order2={t2:.4f}")
```

> تايلور 近似实战: في x0=0 处用一阶和二阶 Taylor 近似 sin(h) ・h=0.1 时近似精度极高,h=2 时偏差很大──这是梯度下降需要小学习率的数学根源──

قريب من x0=0, sin(x) ~ x (تايلور من الدرجة الأولى). التقريب ممتاز ل h صغير ولكن ينفصل ل h كبير. هذا هو السبب في أن تراجع التراجع يعمل بشكل أفضل مع معدلات التعلم الصغيرة - كل خطوة يفترض التقريب الخطي دقيق.

> في x0=0 附近,sin(x) ≈ x(一阶 Taylor) ・・・h 小时近似精确,h 大时偏离

### الخطوة الثامنة: لماذا هذا مهم لشبكة عصبية

```python
import random

random.seed(42)

w = random.gauss(0, 1)
b = random.gauss(0, 1)
lr = 0.01

xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [3.0, 5.0, 7.0, 9.0, 11.0]

for epoch in range(200):
    total_loss = 0
    dw = 0
    db = 0
    for x, y in zip(xs, ys):
        pred = w * x + b
        error = pred - y
        total_loss += error ** 2
        dw += 2 * error * x
        db += 2 * error
    dw /= len(xs)
    db /= len(xs)
    total_loss /= len(xs)
    w -= lr * dw
    b -= lr * db
    if epoch % 40 == 0 or epoch == 199:
        print(f"epoch {epoch:3d}  w={w:.4f}  b={b:.4f}  loss={total_loss:.6f}")

print(f"\nLearned: y = {w:.2f}x + {b:.2f}")
print(f"Actual:  y = 2x + 1")
```

> 完整的线性回归训练循环:从随机权重 w、b 出发,对每样本计算预测、误差、梯度 dw 和 db,然后更新参数──重复 200轮后,模型自动学到 y = 2x + 1──这是所有深度学习训练循环的原型──

كل حلقة تدريبية مبنية على التراجع تتبع هذا النمط: التنبؤ، فقدان الحساب، تراجع الحساب، وزن التحديث.

> تتبع كل دورة تدريبية مبنية على التعدد هذا النموذج: التنبؤ → تخسير الحساب → تعدد الحساب → تحديث الوزن.

## استخدمها في إطار التنفيذ

مع NumPy، نفس العمليات أسرع وأكثر وضوحا:

> استخدام NumPy 重写: نفس النظام أكثر بساطة وأسرع.

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3, 5, 7, 9, 11], dtype=float)

w, b = np.random.randn(), np.random.randn()
lr = 0.01

for epoch in range(200):
    pred = w * x + b
    error = pred - y
    loss = np.mean(error ** 2)
    dw = np.mean(2 * error * x)
    db = np.mean(2 * error)
    w -= lr * dw
    b -= lr * db

print(f"Learned: y = {w:.2f}x + {b:.2f}")
```

> NumPy إلى حجمية`np.mean`替代Python 循环求平均,更快更简洁──矢量化是数值计算的核心优化技巧──

لقد بنيت للتو انخفاض التراجعية من الصفر PyTorch تلقائي الحسابات التراجعية، ولكن حلقة التحديث هو نفسه.

> أنت فقط تحقق تراجعة هبوط من الصفر.`w -= lr * dw`هذا الأمر لن يتغير أبداً

## تمارين التدريب

1. تنفيذ`numerical_second_derivative(f, x)`استخدام `numerical_derivative`ثاني مشتق من x^3 عند x=2 هو 12.
    تحقيق `numerical_second_derivative(f, x)`,调用两次 `numerical_derivative` التحقق من x^3 في x=2 处的二阶导数为 12♦
2. استخدم نسبة تراجع التراجع لتحديد الحد الأدنى من f ((x, y) = (x - 3) ^ 2 + (y + 1) ^ 2. تبدأ من (0, 0). يجب أن تتحلى الإجابة إلى (3, -1).
   用梯度下降找 f(x, y) = (x - 3)2 + (y + 1)2 من الحد الأدنى من القيمة، من (0, 0) 出发,应收到 (3, -1)。
3. إضافة الزخم إلى حلقة هبوط التدرج: الحفاظ على متجه السرعة الذي يتراكم في التدرج السابق. مقارنة سرعة التقارب مع ودون الزخم على f ((x) = x^4 - 3x^2.
   给梯度下降循环加动量:维护一个累积过去梯度的速度向量──比较有无动量在 f(x) = x4 - 3x2 上的收速度──

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Derivative | "The slope" | The rate of change of a function at a point. Tells you how much the output changes per unit change in input. |
| Partial derivative | "Derivative of one variable" | The derivative with respect to one variable while all others are held constant. |
| Gradient | "Direction of steepest ascent" | A vector of all partial derivatives. Points in the direction that increases the function fastest. |
| Gradient descent | "Go downhill" | Subtract the gradient (times a learning rate) from the parameters to reduce the loss. The core of neural network training. |
| Learning rate | "Step size" | A scalar that controls how big each gradient descent step is. Too large: diverge. Too small: converge slowly. |
| Chain rule | "Multiply the derivatives" | The rule for differentiating composed functions: df/dx = df/dg * dg/dx. The mathematical basis of backpropagation. |
| Jacobian | "Matrix of derivatives" | When a function maps vectors to vectors, the Jacobian is the matrix of all partial derivatives of outputs with respect to inputs. |
| Numerical derivative | "Finite differences" | Approximating a derivative by evaluating the function at two nearby points and computing the slope between them. |
| Backpropagation | "Reverse-mode autodiff" | Computing gradients layer by layer from output to input using the chain rule. How neural networks learn. |
| Hessian | "Matrix of second derivatives" | The matrix of all second-order partial derivatives. Describes the curvature of a function. Positive definite Hessian at a critical point means local minimum. |
| Taylor series | "Polynomial approximation" | Approximating a function near a point using its derivatives: f(x+h) ~ f(x) + f'(x)h + (1/2)f''(x)h^2 + ... The basis for understanding why gradient descent and Newton's method work. |
| Integral | "Area under the curve" | The accumulation of a quantity over a range. In ML, integrals define probabilities, expected values, and KL divergence. |

> 术语速查:مشتق) 导数/斜率) ‧ مشتق جزئي ‧偏导数,固定其他变量) ‧Gradient ‧梯度, جميع المشتقات تتكون من ′′向,指向最上升方向) ‧ تراجع درجي ‧梯度下降,沿梯度负方向更新) ‧ متوسط التعلم ‧ تعلم 率,步长) ‧ قاعدة السلسلة ‧ ‧ قاعدة السلسلة, ‧ قاعدة الرياضيات ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ 

## المزيد من القراءة

- [3Blue1Brown: Essence of Calculus](https://www.3blue1brown.com/topics/calculus)- البصرية للشتات والتكاملات وقاعدة السلسلة
- [Stanford CS231n: Backpropagation](https://cs231n.github.io/optimization-2/)- كيف تتدفق التدرج عبر طبقات الشبكة العصبية
