# Makine Öğrenimi İstatistikleri

> İstatistikler, modelinizin gerçekten işe yaradığını veya sadece şanslı olduğunu nasıl anlamanızı sağlar.
> 统计学告诉你模型是真的有效还是只是运气好――

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Öğrenme hedefleri

- Hesaplama tanımlayıcı istatistikleri, Pearson/Spearman ilişkisi ve kovariansa matrislerini sıfırdan hesaplayın
  ZERO hesaplama anlatımlı statistik √ Pearson/Spearman  √ Related系数和协方差矩阵

- Hipotez testlerini (t testi, chi kare) yapın ve p değerlerini ve güven aralıklarını doğru şekilde yorumlayın
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- Değişiklik varsayımları olmadan herhangi bir metrik için güven aralıkları oluşturmak için bootstrap yeniden örneklemesini kullanın
  Bootstrap kullanın Ağırlıklı bir şekilde herhangi bir gösterge için yapılandırın

- Etkinlik boyut ölçümlerini kullanarak istatistiksel önemi pratik önemi ile ayırt etmek
  İşe yararlılık ölçüsü, istatistik belirginlik ve gerçek belirginlik arasındaki fark

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性这些是ML 实验评估的基础──

## Sorunlar. Sorunlar.

> **【中文解读】**Model A 准确率 0.87, Model B 准确率 0.89,你部署了B──三周后线上效果反而变差了因为 0.02 差是噪音不是真实升升──统计学回答:差是否显著?置信区间多宽?样本量不够?没有统计学ML 实验 =盲摸象──

## Konsepten bir şey.

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**:推/搜索模型上线前必须做,统计显著(p<0.05) henüz yayınlanmadı;(2) **Bootstrap 置信区间**:Hesablı veriler dağıtımı kullanmakla, herhangi bir göstergeyi oluşturmakla;**效应量**:p  değeri size sadece " fark yok " diyerek, etkisi size " fark çok büyük " diyerek,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     **多重比较校正**En iyi 20 超参数 seçti, "多碰运气" olarak kabul edilmelidir.

Bu sürekli oluyor. Kağızlama sıralamaları. Tekrarlanamayan makaleler. Birkaç yüz numuneye dayanarak kazananları ilan eden A/B testleri.

> Bu tür olaylar sıklıkla gerçekleşir. Çatışmalar  sıralamalar  büyük şarjlar  geri dönüşü olmayan makaleler  birkaç yüz örnek üzerine kurulmuştur. Kazananın A/B testlerini ilan etmesi                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

İstatistik size sinyalleri gürültüden ayırt etme araçlarını verir. Farkın ne zaman gerçek olduğunu, ne kadar güvenli olmanız gerektiğini ve bir sonuca güvenmeden önce ne kadar veriye ihtiyacınız olduğunu söyler. Her ML boru hattı, her model karşılaştırması, her deney istatistiklere ihtiyaç duyar.

> 统计学 size sinyal ve gürültü ayırt etme aracı sağladı. Farkların ne zaman gerçek olduğunu, ne kadar güvenli olmanız gerektiğini ve bir sonuca inanmak için ne kadar veriye ihtiyacınız olduğunu söyler. Her bir ML borusu, her bir model karşılaştırması, her deney istatistik gerektirir.

## Konsepten bir şey.

### Açıklayıcı İstatistikler: Verilerinize Özet Toplamak

Bir şeyi modellemeden önce verilerin nasıl göründüğünü bilmelisin.

> Herhangi bir model oluşturmadan önce, verilerin nasıl olduğunu bilmeniz gerekir.

**Measures of central tendency**"Orta nerede?" diye cevap ver.

> **集中趋势度量**"Orta nerede?" diye cevap ver.

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

Ortalama dengeler. Ortalama yarı yol işaretidir. Ayrıldıklarında dağılım çarpık olur. Gelir dağılımlarının ortalama >> ortalaması vardır (milyardecilerden sağ çarpıklık). Eğitim sırasında kayıp dağılımlarının çoğu zaman ortalama << ortalaması vardır (sadece örneklerden sol çarpıklık).

> 平均值 = 均衡点──中位数 = 中间标志── 偏离时,你的分布是偏斜的── 收入分布的平均值远大于中位数── 亿万富翁造成的右偏 (右偏)── antrenman sırasında kayıp dağılımının ortalaması genellikle orta değerden çok küçüktür.

**Measures of spread**"Veriler ne kadar dağılmış?" cevabını ver.

> **离散程度度量**"Bilgi çok mu yayılmış?" diye cevap verdi.

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

**Percentiles**Toplam verileri 100 eşit bölüme bölün. 25. yüzdesi (Q1) değerlerin %25'inin bu noktadan aşağı düştüğünü gösterir. 50. yüzdesi ortalama. 75. yüzdesi Q3.

> **百分位数**Bu sıradan sonra veriler 100 ve aynı bölümlere ayrılır. 25. %位数 (Q1) %25 değerinin bu noktada daha düşük olduğunu gösterir. 50. %位数 (Q3) ise orta sayıdır.

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

ML'de, sonuç geçiciliği, tahmin güven dağılımları ve hata dağılımlarını anlama için yüzdeliller önemsediğiniz. Düşük ortalama hata ama korkunç P99 hatası olan bir model güvenlik kritik uygulamalarda işe yaramaz olabilir.

> ML'de, ileri sürülme, tahmin ve güven dağılımının yüzde yüzü ve hata dağılımının yüzde yüzü üzerinde yoğunlaşırsınız. Ortalama hata düşük ancak P99  hata çok kötü bir model, güvenlik anahtarı uygulamaları için kullanışsız olabilir.

**Sample vs population statistics.**Bir örnekten varyansa hesaplarken, n yerine (n-1) bölün. Bu Bessel'in düzeltmesidir. Bu örnek ortalamanın gerçek popülasyon ortalaması olmamasını telafi eder. N isimlendiriciyle, gerçek varyansa sistematik olarak küçümseniyor. (n-1) ile, tahmin tarafsızdır.

> **样本统计 vs 总体统计。**Örnek hesaplama oranı farkında, n değil, n olarak ayrılır. Bu Bessel'in düzeltmesidir.

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

Pratikte: n büyükse (binlerce örnek), fark önemsizdir. n küçükse (bir düzine örnek), önemli.

> 实践中: n 很大了 (n 很大了) 千个样本),差异可以忽略── n 很小了 (n 很小了) 几十个样本),差异很重要──

### Bağlantı: Değişkenlerin Birlikte Nasıl Hareket Edildiği

Korrelasyon, iki değişken arasındaki bir çizgiden ilişkinin gücünü ve yönünü ölçer.

> 相关性 iki değişken arasındaki 线性关系ın gücünü ve yönünü ölçmek.

**Pearson correlation coefficient**Düzsel ilişki önlemleri:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson, ilişkinin doğrusal olduğunu ve her iki değişkenin de normal olarak dağıtıldığını varsayıyor.

> Pearson                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

**Spearman rank correlation**Monoton ilişki önlemleri:

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

**The golden rule:**İsteğe bağlılık nedenlik anlamına gelmez. Dondurma satışları ve boğulma ölümleri, yaz aylarında artış nedeniyle ilişkili. Modelin doğruluğu ve parametrelerin sayısı ilişkilidir, ancak parametrelerin eklenmesi otomatik olarak doğruluğu artırmaz (bakınız: aşırı uyum).

> **黄金法则：**相关不意味因果──冰淋销量和溺水死亡都相关,因为它们都在夏季增加──你的模型精度和参数数数量是相关的,但增加参数并不自动提高精度(参见:过拟合) 

### Covariance Matrix.

İki değişken arasındaki kovarians, birlikte nasıl değiştiklerini ölçer:

> İki değişken arasındaki farklar, birlikte nasıl değiştiklerini ölçer:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

D özellikleri için, kovariansa matrisi C, C[i][j] = Cov(feature_i, feature_j) olduğu bir d x d matrisidir.

> 对于 d 个特征,协方差矩阵 C 是一个 d x d矩阵,其中 C[i][j] = Cov(feature_i, feature_j) ――对角线元素 C[i][i] 是每个特征的方差──

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

**Connection to PCA.**PCA özendependiance matrisiyi oluşturur. Özvektorlar ana bileşenlerdir (maksimum değişkenlik yönleri). Öz değerleri size her bileşenin ne kadar değişkenlik yakaladığını söyler. Bu tam olarak Ders 10'un kapsadığı şeydir, ancak şimdi neden kovariansa matrisi parçalanmak için doğru olduğunu görüyorsunuz: verilerinizde tüm çift yönlü doğrusal ilişkileri kodlar.

> **与 PCA 的联系。**PCA, bir koordinat farklılık matçının özellik ayrımı yapmaktadır. Özellik vektörü ana bileşendir. Özellik değeri size her bileşenin kaç yön ayrımı aldığını söyler. Bu, 10. dersdeki konudur. Ama şimdi neden koordinat farklılık matçının doğru bir parçalanma objesi olduğunu anlıyorsunuz.

**Connection to correlation.**Korrelasyon matrisi, standart değişkenlerin (her biri standart sapmalarıyla bölünmüş) kovarians matrisidir. Korrelasyon kovariansı normalleştirir, böylece tüm değerler [-1, 1]'e düşer.

> **与相关性的联系。**相关矩阵是标准化变量 (), 相关矩阵将协方差归结,使所有值落在 [-1, 1]。

### - İpotis Testleri.

Hipotez testi belirsizlik altında kararlar vermenin bir çerçevesidir. Bir iddiayla başlar, veriler toplar ve verilerin iddia ile tutarlı olup olmadığını belirler.

> 假设检查在不确定性下做决策的框架中──你从一个主张开始,收集数据,然后判断数据是否与主张一致──

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**H0'nun doğru olduğunu varsayarak, gözlemlediğiniz kadar aşırı bir veri görme olasılığıdır. H0'nun doğru olduğu olasılığı değildir.

> **p 值**H0 için gerçek bir ihtimal değildir. Bu, istatistikte en yaygın yanlış anlamalardır.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**Bir parametrenin makul değerler aralığını belirtin:

> **置信区间**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

Güven aralığının genişliği size doğruluk hakkında bilgi verir. Geniş aralıklar yüksek belirsizlik anlamına gelir. Dar aralıklar tahmininizin doğru olduğunu (ama verileriniz tarafsızsa mutlaka doğru değil) anlamına gelir.

> 置信区间的宽度告诉你精度──宽区间意味着高不确定性──狭区间意味着你的估计是精确的(但如果数据有偏见,不一定准确) 

### T-test.

T testi ortalamaları karşılaştırır.

> t 检测比较平均值──有几种变量──

**One-sample t-test:**nüfusun ortalaması bir hipotez değerinden farklı mı?

> **单样本 t 检验：** Genel ortalama değer, varsayılan değerden farklı mıdır?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**İki grup farklı mıdır?

> **两样本 t 检验（独立）：**İki grup arasındaki ortalama değer farklı mı?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**ölçümler çift olarak yapıldığında (aynı veriler üzerinde değerlendirilmiş aynı model):

> **配对 t 检验：**Ölçüm aynı verilerde aynı modelle karşılaştırıldığında:

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

ML'de çiftleştirilmiş t testi yaygın: her iki modeli aynı 10 çapraz onay katlamasında çalıştırır ve puanlarını çiftleştirerek karşılaştırırsınız.

> ML'de t 检验配对 çok yaygındır: Aynı 10 交叉验证折 üzerinde iki model çalıştırır, sonra bunların sayılarını karşılaştırır.

### Çikrelik Test.

Chi kare testi, gözlemlenen frekansların beklenen frekanslarla uyumlu olup olmadığını kontrol eder.

> 卡方检查检查观测频率是否匹配期望频率──适用于分类数据──

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

### ML Modelleri için A/B Testing

ML'deki A/B testleri web A/B testleri ile aynı değildir.

> ML'deki A/B 测试 ile A/B 测试 farklıdır.

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

### İstatistik Önemlik vs. Pratik Önemlik .

Sonuç istatistiksel olarak önemli olabilir ama pratikte anlamsızdır. Yeterli veri ile, önemsiz bir fark bile istatistiksel olarak önemli olur.

> Bir sonuç istatistik olarak önemli olabilir ama aslında hiçbir anlam ifade etmez.

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

**Effect size**örnek boyutundan bağımsız olarak farkın ne kadar büyük olduğunu ölçer:

> **效应量**Közelik farkı çok büyüktür, örnekleme miktarıyla ilgisi yoktur:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Her zaman hem p-de etki boyutunu bildirin. p-değer farkın gerçek olup olmadığını söyler. efekt boyutu önemli olup olmadığını söyler.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真──效应量告诉你差异是否有意义──

### Çoklu karşılaştırma sorunu

Eğer bir çok hipotez denediğinizde, bazıları tesadüfen "önemli" olur. Eğer 20 şeyi alfa = 0.05'te test ederseniz, hiçbir şey gerçek olmasa bile 1 yanlış pozitif beklersiniz.

> Eğer bir alfa = 0.05'de 20 şeyi test edersen, gerçek bir etkisi olmasa bile, bir tane yanlış olumlu olduğunu da beklersin.

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**Alfa'yı test sayısına göre bölün.

> **Bonferroni 校正：**Alfa'yı kontrol sayısını çıkarmak için.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

ML'de, bir modelin birden fazla metrik arasında karşılaştırıldığında, birçok hiperparametre yapılandırmasını test ettiğinde veya birden fazla veri kümesi üzerinde değerlendirdiğinde bu önemlidir.

> ML'de, bir çok gösterge üzerinde model karşılaştırırken, bir çok süperparamantal konutlama veya bir çok veri kümesi üzerinde değerlendirirken, bu çok önemlidir.

### Bootstrap Metodları

Bootstrapping, verilerinizi değiştirerek bir istatistikin örnekleme dağılımını tahmin eder.

> Bootstrap'da, değerlendirme yapımının toplama ve toplama verilerini değerlendirmek için bir tane daha toplama yapılması gerekmez.

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

Bu, çiftleştirilmiş t testiden daha sağlam çünkü dağılımsal varsayımlar yapmaz.

> Bu t 检测 配对  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测  t 检测 检测  t 检测  t 检测 检测  t 检测 检测  t 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 检测 

### Parametrik vs. Parametrik olmayan Testler . Parametrik kontrol vs. Parametrik olmayan kontrol .

**Parametric tests**belirli bir dağılım (genellikle normal) varsayın:

> **参数检验**假设特定分布 (genellikle normal bir dağılımdır):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**dağıtım varsayımları yapmazlar:

> **非参数检验** 不做分布假设:

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

ML deneylerinde, tipik olarak küçük n (5 veya 10 çapraz onay katlaması) vardır, bu nedenle Wilcoxon'un imzalaması gibi parametrik olmayan testler genellikle t testlerinden daha uygun olur.

> ML deneylerinde, genellikle küçük n ((5 veya 10 交叉验证折) vardır, bu nedenle Wilcoxon 符号秩 gibi parametre dışı incelemeler genellikle t incelemelerinden daha uygundur.

### Merkez Sınır Teoremi: Pratik İlişkiler

CLT'nin belirttiği gibi, örneklerin dağılımı, n'in büyüdüğü sırada, temel popülasyon dağılımı ne olursa olsun normal bir dağılmaya yaklaşır.

> CLT, n  büyüme ile, örneğin ortalama değerinin dağılımı, alt kattaki genel dağılımın nasıl olduğuna bakılmaksızın, normal dağılmaya yaklaşır.

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

### ML makalelerinde yaygın istatistik hatalar .

1. **Testing on the training set.**Sürekli modelin eğitim sırasında görmediği verileri saklayın.

> 1. **在训练集上测试。**Bu yüzden, bu konuda bir şey yapmamalıyız.

2. **No confidence intervals.**Tek bir doğruluk numarasını belirsizlik olmadan bildirmek sonuçları tekrarlanamıyor ve doğrulanamıyor.

> 2. **没有置信区间。** Raporlama, kesinlik ölçüsünü belirsiz bir rakam ile yapılır ve sonuçları tekrarlanamaz hale getirir.

3. **Ignoring multiple comparisons.**50 yapılandırmayı test etmek ve en iyi olanı düzeltmeden rapor etmek yanlış pozitif oranları yükseltir.

> 3. **忽略多重比较。**Test 50 配置并报告 ⇒ En iyi bir düzeltme yapmadan, çarpıcı bir pozitiflik oranı olacaktır.

4. **Confusing statistical and practical significance.**0.001'lik bir p değeri, 0.01% doğruluk gelişimi için anlamlı değildir.

> 4. **混淆统计显著性和实际显著性。**0.01% 精度提升上 p 值 0.001 无意义──

5. **Using accuracy on imbalanced data.**99% negatif sınıflı bir veri kümesindeki %99 doğruluk, modelin hiçbir şey öğrenmediğini gösterir.

> 5. **在不平衡数据上使用精度。**99% 負のデータセットで 99% 精度, modelin hiçbir şey öğrenmediğini ifade eder.

6. **Cherry-picking metrics.**Sadece modelin kazandığı ölçümleri rapor edersin.

> 6. **挑选指标。**Sadece model kazanma göstergesini rapor et.

7. **Leaking information across train/test splits.**Bölmeden önce normalleştirmek veya geçmişi tahmin etmek için gelecekteki verileri kullanmak.

> 7. **在训练/测试划分之间泄露信息。**Bu, bir önceki birleştirme veya gelecek verileri ile birleştirilme anlamına gelir.

8. **Small test sets with no variance estimates.**100 numuneye değerlendirmek ve % 2 iyileşme iddiası yapmak, sinyal değil gürültüdür.

> 8. **小测试集没有方差估计。**100 örnek üzerinde değerlendirilmiş ve % 2'lik artışın sinyal değil gürültü olduğunu iddia etmiştir.

9. **Assuming independence when data is not independent.**Aynı hastadan gelen tıbbi görüntüler, aynı belgeye ait birden fazla cümle.

> 9. **数据不独立时假设独立。**Aynı hastanın tıbbi görüntüleri, aynı dosyanın birçok cümlesinden alınmıştır.

10. **P-hacking.**P < 0,05'e ulaşana kadar farklı testler, alt kümeler veya dışlama kriterlerini denemek.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, p < 0.05── sonuçları arama sürecinin sahte görüntüsüdür.

## Yapımcılık, gerçekleştirme.

Bu uygulamayı uygulayacaksınız:

> Siz bunu gerçekleştireceksiniz:

1. **Descriptive statistics from scratch**(ortalama, ortalama, mod, standart sapma, yüzdeler, IQR)
   **从零实现描述性统计**(mevcut değer, ortalama sayı, sayı, standart fark, yüzde sayı, IQR)
2. **Correlation functions**(Pearson ve Spearman, kovariansa matrisi ile)
   **相关函数**(Pearson ve Spearman, ve birlikte bir diğer rekordan)
3. **Hypothesis tests**(bir örnek t testi, iki örnek t testi, chi kare testi)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(herhangi bir istatistik için varsayım gerekmez)
   **Bootstrap 置信区间**(Önemli bir statü, gereksiz bir varsayım)
5. **A/B test simulator**(veriler oluşturmak, test etmek, I ve II tip hataları kontrol etmek)
   **A/B 测试模拟器**(data üretmek, test etmek, kontrol etmek birinci ve ikinci sınıf hatalar)
6. **Statistical vs practical significance demo**(büyük n'in her şeyi "önemli" kıldığını gösterir)
   **统计 vs 实际显著性演示**(Görünen her şey önemli)

Hepsi sıfırdan, sadece kullanılarak.`math`ve `random`- Ne şapşalık ne de şapşalık.

> 全部从零实现, sadece kullanmak `math`和 `random`❖不使用 numpy、scipy。

## Anahtar Şartlar .
```figure
f3-bootstrap-resample
```

## Anahtar Terimler

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
