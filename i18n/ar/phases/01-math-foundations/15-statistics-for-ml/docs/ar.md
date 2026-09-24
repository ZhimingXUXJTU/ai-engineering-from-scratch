# إحصاءات للتعلم الآلي                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> الإحصاءات هي كيف تعرف ما إذا كان نموذجك يعمل فعلاً أو كان محظوظاً
> الإحصاءات تخبرك أن النموذج فعال حقاً أم فقط جيد

**Type:** Build | **类型:** 动手
**Language:**" بايثون "**语言:**بايثون
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## أهداف التعلم

- إحصاءات تصريفيّة الحساب، وتصريحات ارتباط بييرسون/سبيرمان، ومصفوفات التغيرات من الصفر
  من صفر حساب تصريحية احصاءات  بيرسون / سبيرمان  Related系数和协方差矩阵

- إجراء اختبارات فرضية (اختبار t، chi- مربع) وتفسير قيم p ومناطق الثقة بشكل صحيح
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- استخدام bootstrap resampling لبناء فترات الثقة لأي متريكا دون افتراضات توزيعية
  استخدام Bootstrap 重采样为任意标标构建置信区间,无需分布假设

- تمييز الأهمية الإحصائية عن الأهمية العملية باستخدام قياسات حجم التأثير
  استخدام النتائج الحد الأدبي والواقعية

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性这些是ML 实验评估的基础──

## المشكلة المشكلة المشكلة

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署 B──三周后线上效果反而变化因为 0.02 差异是噪音不是真的提升──统计学答案:差异是否显著?置信区间多宽?样本量不够?没有统计学ML 实验 = 盲人摸象──

## المفهوم الأساسي

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**:推/搜索模型上线前必须做,统计显著(p<0.05) تا تا نشر;(2) **Bootstrap 置信区间**: لا تحتاج إلى فرضية توزيع البيانات ، باستخدام الاختبار الزمني لبناء أي مؤشر من منطقة الإعتقاد ؛**效应量**:p 值 فقط يخبرك"لست هناك فرق"، 效应量 يخبرك"الفرق كبير" 统计显著 ≠ 实际有用;**多重比较校正**: تدوّن 20 超参数取最好的, يجب أن تكون القانون "多碰运气"

هذا يحدث باستمرار. تغييرات في قائمة الرتبة. أوراق لا تتكاثر. اختبارات A / B التي تعلن الفائزين بناء على بضع مئات من العينات. السبب الجذري هو دائما نفسها: شخص ما تخطي الإحصاءات.

> هذا يحدث في كثير من الأحيان. تكرار الدرجة. لا يمكن إعادة التأثير. بناء على مئات العينات من النماذج التي أعلنت عن الفائز في اختبار A / B.

الإحصاءات تعطيك الأدوات لتمييز الإشارة عن الضوضاء. إنها تخبرك متى يكون الفرق حقيقيًا، ومدى الثقة التي يجب أن تكون بها، ومقدار البيانات التي تحتاجها قبل أن تثق في نتيجة. كل خط أنابيب ML، كل مقارنة نموذج، كل تجربة تحتاج إلى إحصاءات. بدونها، كنت تخمين.

> تقدم الإحصاء لك أداة للتمييز بين الإشارات والضوضاء. يخبرك متى يكون الفرق حقيقيًا، وكيف يجب أن تكون واثقًا، وكيف تحتاج إلى كمية البيانات لتثق في نتيجة. كل أنبوب ML، كل نموذج مقارنة، كل تجربة تحتاج إلى إحصاء.

## المفهوم الأساسي

### الإحصاءات التفصيلية: تلخيص بياناتك

قبل أن تقوم بتصميم أي شيء، تحتاج إلى معرفة كيف تبدو البيانات الخاصة بك. الإحصاءات التوضيحية تضغط مجموعة البيانات إلى عددين يحتوي على شكلها.

> قبل بناء أي نموذج، تحتاج إلى معرفة نمط البيانات.

**Measures of central tendency**أجيب "أين الوسط؟"

> **集中趋势度量**أجاب " وسط وسط أين؟"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

متوسط هو نقطة التوازن. متوسط هو علامة نصف الطريق. عندما تختلف، يتم تحويل التوزيع الخاص بك. توزيع الدخل لديه متوسط >> المتوسط (التوجه اليميني من المليارديرين). توزيع الخسائر أثناء التدريب غالبا ما يكون متوسط << المتوسط (التوجه اليسرى من عينات سهلة).

> 平均值是平衡点──中位数是中间标志──当它们偏离时,你的分布是偏斜的──收入分布的平均值远大于中位数(亿万富翁造成的右偏)──训练期间损失分布的平均值通常远小于中位数(简单样本造成的左偏)──

**Measures of spread**الإجابة على "كم توزيع البيانات؟"

> **离散程度度量**أجاب "هل هناك بيانات ربما تنتشر؟"

```
Variance:   average squared deviation from the mean
            sigma^2 = (1/n) * sum((x_i - mu)^2)

Standard deviation:  square root of variance
                     sigma = sqrt(sigma^2)
                     Same units as the data, so more interpretable.

Range:      max - min
            Sensitive to outliers. Almost never useful alone.

IQR:        Q3 - Q1 (interquartile range)
            The range of the middle 50% of the data.
            Robust to outliers. Used for box plots and outlier detection.
```

**Percentiles**تقسيم البيانات المرتبة إلى 100 جزء متساو. المئة 25 (Q1) تعني أن 25% من القيم تقع تحت هذه النقطة. المئة 50 هي المتوسط. المئة 75 هي Q3.

> **百分位数**سوف تقسيم البيانات بعد الترتيب إلى 100 等份──第 25 百分位数(Q1) يعني قيمة 25% أقل من هذه النقطة──第 50 百分位数就是中位数──第 75 百分位数是 Q3──

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

في ML، تهتم بالرسومات للتخفيف من الإستنتاج، وتوزيعات الثقة التنبؤية، وتوزيعات الخطأ الفهمية. قد يكون نموذجًا ذو متوسط ضئيل ولكن خطأ P99 رهيب غير مفيد للتطبيقات الحرجة للسلامة.

> في ML، أنت مهتم في التفكير في تأخير التوقعات والتنبؤ في النسبة المئوية لتوزيع الخطيئات والتوزيعات التوقعات. النموذج المتوسط للخطيئات منخفضة ولكن P99 الخطيئات هي خيبة جدا، بالنسبة للتطبيقات الرئيسية للأمن قد تكون غير مفيدة.

**Sample vs population statistics.**عند حساب التباين من عينة، قم بتقسيم (n-1) بدلاً من (n-1). هذا تصحيح بيسل. فإنه يعوض عن حقيقة أن متوسط عينتك ليس متوسط السكان الحقيقي. مع n في المسمي، فإنك تقليل التباين الحقيقي بشكل منهجي. مع (n-1) ، التقدير غير متحيز.

> **样本统计 vs 总体统计。**من نموذج حساب الفوارق، فاضل با (n-1) وليس n― هذا هو البيسيل المثالي (بيسيل تصحيح)― يعوض حقيقة أن متوسط القيمة النموذجية ليست الحقيقية مجموعي متوسط القيمة―分母用 n 会系统性地低估真实方差──用 (n-1), التقدير غير محايض‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

في الممارسة العملية: إذا كان n كبيرًا (ألف عينات) ، فإن الفرق ضئيل. إذا كان n صغيرًا (عشرات العينات) ، فهو مهم.

> في الممارسة: إذا كان عدد النماذج ضخمًا (ألف) ، فيمكن تجاهل التباين.

### العلاقة: كيف تتحرك المتغيرات معا 相关性: كيف تتغير المتغيرات معا

القياسات التناسلية تقيس قوة واتجاه العلاقة الخطية بين متغيرين.

> 相关性 قياس قوة والاتجاه للعلاقة بين المتغيرين

**Pearson correlation coefficient**تدابير الربط الخطي:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

يفترض بيرسون أن العلاقة خطية وكلا المتغيرات موزعة بشكل طبيعي تقريبًا. هو حساسًا للمخالفات. نقطة متطرفة واحدة يمكن أن تسحب r من 0.1 إلى 0.9.

> بيرسون افتراض العلاقة هي خطية، ويتمثل المتغيرات بشكل كبير في التوزيع العادي.

**Spearman rank correlation**تدابير الربط المتوحد:

> **Spearman 秩相关**衡量单调关联:

```
1. Replace each value with its rank (1, 2, 3, ...)
2. Compute Pearson correlation on the ranks

Spearman catches any monotonic relationship, not just linear.
If y = x^3, Pearson gives r < 1 but Spearman gives rho = 1.
```

**When to use each:**

> **何时使用哪个：**

```
Pearson:    Both variables are continuous and roughly normal.
            You care about the linear relationship specifically.
            No extreme outliers.

Spearman:   Ordinal data (rankings, ratings).
            Data is not normally distributed.
            You suspect a monotonic but not linear relationship.
            Outliers are present.
```

**The golden rule:**التواصل لا يعني وجود سبب. مبيعات الآيس كريم وفيات الغرق مرتبطة لأن كلا الزيادة في الصيف. دقة نموذجك وعدد المعلمات مرتبطة، ولكن إضافة المعلمات لا تحسن دقة تلقائيًا (انظر: الإفراط في التكيف).

> **黄金法则：**相关不意味因果──冰冰销量和溺水死亡是相关的,因为它们都在夏季增加──你的模型精度和参数数数量是相关的,但增加参数并不自动提高精度(参见:过拟合) 

### ماتريكس التباين

يقدر التباين بين متغيرين كيف يتباين معاً:

> التكافؤ بين المتغيرين يقيّم كيف يتغيران معاً:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

بالنسبة لميزات d، فإن المصفوفة C هي المصفوفة d x d حيث C[i][j] = Cov(feature_i، feature_j). الإدخالات المقطعية C[i][i] هي المتغيرات لكل ميزة.

> بالنسبة ل d 个特征، فإن الموجة المشتركة C هي واحدة من d x d 矩阵، من بينها C[i][j] = Cov(feature_i، feature_j)。对角线元素 C[i][i] 是每个特征的方差──

```
C = | Var(x1)      Cov(x1,x2)  Cov(x1,x3) |
    | Cov(x2,x1)  Var(x2)      Cov(x2,x3) |
    | Cov(x3,x1)  Cov(x3,x2)  Var(x3)     |

Properties:
  - Symmetric: C[i][j] = C[j][i]
  - Positive semi-definite: all eigenvalues >= 0
  - Diagonal = variances
  - Off-diagonal = covariances
```

**Connection to PCA.**يجمع PCA نفسه المصفوفة التباينية. المتجهات الخاصة هي المكونات الرئيسية (اتجاهات أقصى اختلاف). القيم الخاصة تخبرك كم التباينية التي يتقاطعها كل مكون. هذا بالضبط ما تغطيه الدروس 10 ، ولكن الآن ترى لماذا هو المصفوفة التباينية هو الشيء الصحيح للتفكك: فهو يرمز جميع العلاقات الخطية المتزاوجة في بياناتك.

> **与 PCA 的联系。**يُخبرك قيمة الصفحة أن كل عنصر قد اكتسب عدد الاختلافات الواسعة. هذا هو بالضبط ما سبق أن تمتد به في الدورة العاشرة، ولكن الآن فهمت لماذا هي الموجة الواسعة صحيحة في الاختلافات: إنها ترميز جميع العلاقات السريعة في البيانات.

**Connection to correlation.**المصفوفة التواصل هي المصفوفة التواصلية المتغيرات المعيارية (كل منها مقسمة عن طريق انحرافها القياسي). التواصل يطبق التواصلية بحيث تسقط جميع القيم في [-1, 1].

> **与相关性的联系。**الموجات المرتبطة هي المعدلات المعتمدة (كل منها من خلال المعدلات المعتمدة) الموجات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات المرتبطة بالمعادلات [-1, 1]

### اختبار الفرضية

اختبار الفرضية هو إطار لاتخاذ القرارات في ظل عدم اليقين. تبدأ بطلب، وتجمع البيانات، وتحديد ما إذا كانت البيانات متوافقة مع المطالبة.

> افتراض أن الاختبار هو إطار لاتخاذ القرارات تحت عدم اليقين.

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**هو احتمال رؤية البيانات متطرفة كما لاحظته، افتراض H0 صحيحة. انها ليست احتمال H0 صحيحة. هذا هو واحد من أكثر سوء الفهم الشائعة في الإحصاءات.

> **p 值**هو في H0 لفرض حقيقية، لاحظ احتمالات البيانات التي تتم ملاحظتها على نفس الطرف أو أكثر من ذلك.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**إعطاء مجموعة من القيم المثيرة للصدق للفاروم:

> **置信区间**عطاء مجموعة من العناصر ذات القيمة المعقولة:

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

عرض فترة الثقة يخبرك عن الدقة. فترات واسعة تعني عدم اليقين العالي. فترات ضيقة تعني تقديرك دقيق (ولكن ليس بالضرورة دقيقًا، إذا كانت بياناتك متحيزة).

> 置信区间的宽度告诉你精度──宽区间意味着高不确定性──狭区间意味着你的估计是精确的(但如果数据有偏见,不一定准确) 

### اختبار التقييم

اختبار "ت" يقارن معدل، هناك العديد من الذوق

> معدل التقييمات:

**One-sample t-test:**هل متوسط السكان مختلف عن القيمة المفترضة؟

> **单样本 t 检验：**هل يختلف متوسط القيمة الإجمالية عن القيمة المفترضة؟

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**هل المجموعتين تعنيان مختلفان؟

> **两样本 t 检验（独立）：**هل يختلف متوسط المجموعتين؟

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**عندما تكون القياسات مقترحة (المثل الذي يتم تقييمه على نفس تقسيم البيانات):

> **配对 t 检验：**عندما يتم قياس النموذج نفسه على نفس البيانات:

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

في ML، اختبار t المزدوج شائع: تقوم بتشغيل كلا النماذج على نفس 10 طوابق التحقق المتقاطع وتقارن درجاتها بشكل مزدوج.

> في ML، تعادل التحقق هو أمر شائع: تقوم بالعمل على نموذجين على نفس 10 ثقب التحقق، ثم تقارن بينهما.

### اختبار " تشي " مربع " اختبار " كاردون

اختبار "شي-سكواد" يختبر ما إذا كانت الترددات الملاحظة تتطابق مع الترددات المتوقعة. مفيدة للبيانات الفئوية.

> 卡方检查检查 观测频率是否匹配期望频率──适用分类数据──

```
chi^2 = sum((observed - expected)^2 / expected)

Example: does a language model's output distribution match the
training distribution across categories?

Category    Observed   Expected
Positive       120        100
Negative        80        100
chi^2 = (120-100)^2/100 + (80-100)^2/100 = 4 + 4 = 8

With 1 degree of freedom, chi^2 = 8 gives p < 0.005.
The difference is significant.
```

### اختبار A/B لنماذج ML   اختبار A/B لنماذج ML  اختبار

لا يعد اختبار A/B في ML هو نفسه من اختبار A/B على شبكة الإنترنت.

> المواد المختلفة من المواد المختلفة من المواد المختلفة من المختلفة.

```
1. Same test set:    Both models must be evaluated on identical data.
                     Different test sets make comparison meaningless.

2. Multiple metrics: Accuracy alone is not enough. You need precision,
                     recall, F1, latency, and fairness metrics.

3. Variance:         Use cross-validation or bootstrap to estimate
                     the variance of each metric, not just point estimates.

4. Data leakage:     If the test set was used during model selection,
                     your comparison is biased. Hold out a final test set.
```

**The procedure:**

> **操作步骤：**

```
1. Define your metric and significance level (alpha = 0.05)
2. Run both models on the same k-fold cross-validation splits
3. Collect paired scores: [(a1, b1), (a2, b2), ..., (ak, bk)]
4. Compute differences: d_i = b_i - a_i
5. Run a paired t-test on the differences
6. Check: is the mean difference significantly different from 0?
7. Compute a confidence interval for the mean difference
8. Compute effect size (Cohen's d) to judge practical significance
```

### الإحصائيات ذات أهمية مقابل الأهمية العملية

النتيجة يمكن أن تكون ذات أهمية إحصائية ولكن لا معنى لها عملياً. مع وجود بيانات كافية، يصبح الفارق البسيط مهماً إحصائيًا.

> نتيجة يمكن أن تكون ملحوظة إحصائيًا ولكن لا معنى لها في الواقع. عندما يكون هناك الكثير من البيانات، حتى الاختلافات الصغيرة ستصبح ملحوظة إحصائيًا.

```
Example:
  Model A accuracy: 0.9234
  Model B accuracy: 0.9237
  n = 1,000,000 test samples
  p-value = 0.001

Statistically significant? Yes.
Practically significant? A 0.03% improvement is not worth the
engineering cost of deploying a new model.
```

**Effect size**يحدد مقدار الفرق، بغض النظر عن حجم العينة:

> **效应量**الفرق الكمي كبير، لا علاقة له بمقدار العينات:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

دائماً أبلغ كل من قيمة p وحجم التأثير. قيمة p تخبرك إذا كان الفرق حقيقي. حجم التأثير يخبرك إذا كان يهم.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真──效应量告诉你差异是否有意义──

### مشكلة مقارنة متعددة مشكلة مقارنة متعددة

عندما تختبر العديد من الفرضيات، بعضها سيكون "مهم" بالصدفة. إذا اختبرت 20 شيء عند ألفا = 0.05, تتوقع 1 إيجابية كاذبة حتى عندما لا شيء حقيقي.

> عندما تقوم بتحقق العديد من الفرضيات، بعضها يحدث بشكل "مبين".

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**تقسيم ألفا على عدد الاختبارات

> **Bonferroni 校正：**سوف أضع ألفاً في عدد المراحل

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

في ML، هذا يهم عندما تقارن نموذج عبر مقاييس متعددة، واختبار العديد من تكوينات المعلمات العالية، أو تقييم على مجموعة بيانات متعددة.

> في مجال ML، عندما تقارن النماذج على العديد من المؤشرات، وتختبر العديد من التكوينات الفائقة المعايير أو تقييمها على مجموعة بيانات متعددة، هذا أمر مهم.

### أساليب التشغيل

يقدر Bootstrapping توزيع العينات من إحصاءات عن طريق إعادة أخذ العينات من البيانات الخاصة بك مع استبدال. لا توجد افتراضات حول التوزيع الأساسي مطلوبة.

> التنفيذ من خلال إعادة إرسال البيانات إلى التقديرات التنفيذية للحصصات. لا حاجة إلى أي افتراضات على التوزيع الأساسي.

**The algorithm:**

> **算法：**

```
1. You have n data points
2. Draw n samples WITH replacement (some points appear multiple times,
   some not at all)
3. Compute your statistic on this bootstrap sample
4. Repeat B times (typically B = 1000 to 10000)
5. The distribution of bootstrap statistics approximates the
   sampling distribution
```

**Bootstrap confidence interval (percentile method):**

> **Bootstrap 置信区间（百分位数法）：**

```
Sort the B bootstrap statistics
95% CI = [2.5th percentile, 97.5th percentile]
```

**Why bootstrap matters for ML:**

> **Bootstrap 对 ML 为什么重要：**

```
- Test set accuracy is a point estimate. Bootstrap gives you
  confidence intervals.
- You cannot assume metric distributions are normal (especially
  for AUC, F1, precision at k).
- Bootstrap works for ANY statistic: median, ratio of two means,
  difference in AUC between two models.
- No closed-form formula needed.
```

**Bootstrap for model comparison:**

> **Bootstrap 用于模型比较：**

```
1. You have predictions from Model A and Model B on the same test set
2. For each bootstrap iteration:
   a. Resample test indices with replacement
   b. Compute metric_A and metric_B on the resampled set
   c. Store diff = metric_B - metric_A
3. 95% CI for the difference:
   [2.5th percentile of diffs, 97.5th percentile of diffs]
4. If the CI does not contain 0, the difference is significant
```

هذا أكثر قوة من اختبار t المزدوج لأنه لا يقدم افتراضات توزيعية.

> هذا أكثر استقرارًا من معايير التحقق لأنه لا يفترض توزيعها.

### اختبارات المعلمات مقابل غير المعلمات

**Parametric tests**افترض توزيع محدد (عادة طبيعي):

> **参数检验**假设特定分布 (عادة تكون توزيعاً صائباً):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**لا يفترض التوزيع:

> **非参数检验**غير مقسمة:

```
Mann-Whitney U:     compares two groups (replaces independent t-test)
Wilcoxon signed-rank: compares paired data (replaces paired t-test)
Spearman rho:       correlation on ranks (replaces Pearson)
Kruskal-Wallis:     compares multiple groups (replaces ANOVA)
```

**When to use non-parametric:**

> **何时使用非参数检验：**

```
- Small sample size (n < 30) and data is clearly non-normal
- Ordinal data (ratings, rankings)
- Heavy outliers you cannot remove
- Skewed distributions
```

**When to use parametric:**

> **何时使用参数检验：**

```
- Large sample size (CLT makes the test statistic approximately normal)
- Data is roughly symmetric without extreme outliers
- More statistical power (better at detecting real differences)
```

في تجارب ML، عادة ما يكون لديك n صغيرة (5 أو 10 طوابق التحقق المتقاطع) ، لذلك الاختبارات غير المعلمية مثل Wilcoxon الموقع المرتبة غالبا ما تكون أكثر ملاءمة من الاختبارات t.

> في تجربة ML ، عادة ما يكون لديك n ((5 أو 10) من التقاطع ، لذلك مثل Wilcoxon 符号 秩 مثل هذه التفتيشات غير العادلية عادة ما تكون أكثر ملائمة من التفتيشات.

### نظرية الحد المركزي: الآثار العملية

ويقول CLT أن توزيع العينات يقترب من توزيع طبيعي مع نمو n، بغض النظر عن توزيع السكان الأساسي.

> يقول CLT، مع نمو النموذج، تقسيم القيمة المتوسطة يتجه نحو التوزيع الصحي، بغض النظر عن كيفية توزيع الطبقة العامة.

```
If X_1, X_2, ..., X_n are iid with mean mu and variance sigma^2:

    X_bar ~ Normal(mu, sigma^2 / n)    as n -> infinity

Works for n >= 30 in most cases.
For highly skewed distributions, you might need n >= 100.
```

**Why this matters for ML:**

> **这对 ML 为什么重要：**

```
1. Justifies confidence intervals and t-tests on aggregated metrics
2. Explains why averaging over cross-validation folds gives stable
   estimates even when individual folds vary wildly
3. Mini-batch gradient descent works because the average gradient
   over a batch approximates the true gradient (CLT in action)
4. Ensemble methods: averaging predictions from many models gives
   more stable output than any single model
```

**What CLT does NOT do:**

> **CLT 不能做什么：**

```
- Does NOT make your data normal. It makes the MEAN of samples normal.
- Does NOT work for heavy-tailed distributions with infinite variance
  (Cauchy distribution).
- Does NOT apply to dependent data (time series without correction).
```

### أخطاء إحصائية شائعة في ورق ML 论文中常见的统计错误

1. **Testing on the training set.**تضمن التكيف الزائد، دائماً تمتلك بيانات لا يراها النموذج أثناء التدريب

> 1. **在训练集上测试。**ضمان أكثر ملاءمة. دائما الاحتفاظ بالبيانات التي لم نرها من قبل أثناء تدريب النموذج.

2. **No confidence intervals.**الإبلاغ عن رقم واحد من الدقة دون عدم اليقين يجعل النتائج غير قابلة للتكرار وغير قابلة للتحقق.

> 2. **没有置信区间。** تقرير رقم واحد من الدقة دون قياسات عدم اليقين، مما يجعل النتائج غير قابلة للتكرار وغير قابلة للتحقق.

3. **Ignoring multiple comparisons.**اختبار 50 تكوين وتقديم أفضل واحد دون تصحيح يضخم معدلات إيجابية كاذبة.

> 3. **忽略多重比较。**测试 50 配置并报告最好的一个不做校正,会膨胀假阳性率──

4. **Confusing statistical and practical significance.**قيمة p من 0.001 على تحسين دقة 0.01٪ ليست ذات معنى.

> 4. **混淆统计显著性和实际显著性。**0.01% 精度提升上 p 值 0.001 没有意义──

5. **Using accuracy on imbalanced data.**99٪ دقة على مجموعة بيانات مع 99٪ فئة سلبية يعني أن النموذج لم يتعلم شيئا. استخدم الدقة، التذكير، F1 أو AUC.

> 5. **在不平衡数据上使用精度。**في مجموعات بيانات من 99% من الفئات السلبية، فإن دقة 99% تعني أن النموذج لم يتعلم أي شيء.

6. **Cherry-picking metrics.**تقرير فقط المقاييس التي يفوز فيها نموذجك تقرير تقييم صادق جميع المقاييس ذات الصلة

> 6. **挑选指标。**فقط أبلغ عن مؤشرات النموذج الخاص بك.

7. **Leaking information across train/test splits.**التطبيع قبل الانقسام، أو استخدام البيانات المستقبلية للتنبؤ بالماضي.

> 7. **在训练/测试划分之间泄露信息。**في التقسيم السابق للعودة إلى التوحيد أو باستخدام بيانات التنبؤ بالمستقبل.

8. **Small test sets with no variance estimates.**التقييم على 100 عينة و المطالبة بتحسن 2% هو الضجيج، وليس الإشارة.

> 8. **小测试集没有方差估计。**في 100 عينة، أعلن تقييمها أن ارتفاع 2% هو الضجيج وليس الإشارة.

9. **Assuming independence when data is not independent.**صور طبية من نفس المريض، جمل عدة من نفس الوثيقة.

> 9. **数据不独立时假设独立。**الصور الطبية من نفس المريض، من نفس الملف، عدة جملة.

10. **P-hacking.**تجربة اختبارات مختلفة أو مجموعات فرعية أو معايير استبعاد حتى تحصل على p < 0.05. النتيجة هي أثرية للبحث.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, حتى تحصل على p < 0.05── نتيجة هي الظاهر المزيفة لعملية البحث.

## بناءه تحركه

ستنفذ:

> ستحقيق:

1. **Descriptive statistics from scratch**(متوسط، ووسط، وضع، انحراف قياسي، الفصائل، IQR)
   **从零实现描述性统计**(معدل القيمة، والوسط، والعدد، والمعيار، والفروق، والمعدل العادي)
2. **Correlation functions**(بيرسون وسبيرمان) مع المصفوفة المتجانسة)
   **相关函数**(بيرسون و سبيرمان)
3. **Hypothesis tests**(اختبار الـ T من عينة واحدة، اختبار الـ T من عينتين، اختبار الـ Chi-squared)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(لمعرفة أي إحصاءات، لا حاجة إلى افتراضات)
   **Bootstrap 置信区间**(حسابات إراديّة، لا حاجة إلى فرض)
5. **A/B test simulator**(إنتاج البيانات، واختبار، التحقق من أخطاء النوع الأول والنوع الثاني)
   **A/B 测试模拟器**(إنتاج بيانات 测试 检查第一类和第二类错误)
6. **Statistical vs practical significance demo**(ويعرض أن n الكبير يجعل كل شيء "مهم")
   **统计 vs 实际显著性演示**(تظهر كل شيء"بصورة كبيرة")

كل شيء من الصفر، باستخدام فقط`math`و`random`لا شقق ولا شقق

> كل من التحقق، فقط الاستخدام`math`和 `random`◊不使用numpy、scipy‬

## شروط الرئيسية
```figure
f3-bootstrap-resample
```

## الشروط الرئيسية

| Term / 术语 | Definition / 定义 |
|---|---|
| Mean / 均值 | Sum of values divided by count. Sensitive to outliers. / 值的总和除以个数。对异常值敏感。 |
| Median / 中位数 | Middle value of sorted data. Robust to outliers. / 排序后数据的中间值。对异常值稳健。 |
| Standard deviation / 标准差 | Square root of variance. Measures spread in original units. / 方差的平方根。用原始单位衡量离散程度。 |
| Percentile / 百分位数 | Value below which a given percentage of data falls. / 给定百分比的数据低于此值。 |
| IQR / 四分位距 | Interquartile range. Q3 minus Q1. The spread of the middle 50%. / 四分位距。Q3 减 Q1。中间 50% 的展幅。 |
| Pearson correlation / Pearson 相关系数 | Measures linear association between two variables. Range [-1, 1]. / 衡量两个变量间的线性关联。范围 [-1, 1]。 |
| Spearman correlation / Spearman 相关系数 | Measures monotonic association using ranks. / 用排名衡量单调关联。 |
| Covariance matrix / 协方差矩阵 | Matrix of pairwise covariances between all features. / 所有特征间成对协方差的矩阵。 |
| Null hypothesis / 零假设 | Default assumption of no effect or no difference. / 无效应或无差异的默认假设。 |
| p-value / p 值 | Probability of data this extreme given the null hypothesis is true. / 在零假设为真的条件下观察到如此极端数据的概率。 |
| Confidence interval / 置信区间 | Range of plausible values for a parameter at a given confidence level. / 给定置信水平下参数的合理值范围。 |
| t-test / t 检验 | Tests whether means differ significantly. Uses the t-distribution. / 检验均值是否有显著差异。使用 t 分布。 |
| Chi-squared test / 卡方检验 | Tests whether observed frequencies differ from expected frequencies. / 检验观测频率是否与期望频率不同。 |
| Effect size / 效应量 | Magnitude of a difference, independent of sample size. Cohen's d is common. / 差异的大小，与样本量无关。常用 Cohen's d。 |
| Bonferroni correction / Bonferroni 校正 | Divides significance threshold by number of tests to control false positives. / 将显著性阈值除以检验次数以控制假阳性。 |
| Bootstrap / Bootstrap | Resampling with replacement to estimate sampling distributions. / 有放回重采样以估计抽样分布。 |
| Type I error / 第一类错误 | False positive. Rejecting H0 when it is true. / 假阳性。H0 为真时拒绝 H0。 |
| Type II error / 第二类错误 | False negative. Failing to reject H0 when it is false. / 假阴性。H0 为假时未能拒绝 H0。 |
| Statistical power / 统计功效 | Probability of correctly rejecting a false H0. Power = 1 minus Type II error rate. / 正确拒绝假 H0 的概率。功效 = 1 减第二类错误率。 |
| Central limit theorem / 中心极限定理 | Sample means converge to a normal distribution as sample size grows. / 样本均值随样本量增大趋近于正态分布。 |
| Parametric test / 参数检验 | Assumes a specific distribution for the data (usually normal). / 假设数据服从特定分布（通常是正态分布）。 |
| Non-parametric test / 非参数检验 | Makes no distributional assumptions. Works on ranks or signs. / 不做分布假设。基于排名或符号工作。 |
