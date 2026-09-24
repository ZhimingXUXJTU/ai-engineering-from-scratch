# Estadísticas para el aprendizaje automático

> Las estadísticas son la manera de saber si tu modelo realmente funciona o simplemente tuvo suerte.
> La estadística te dice si el modelo es realmente efectivo o simplemente bueno.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizaje

- Computa estadísticas descriptivas, correlación Pearson/Spearman y matrices de covarianza desde cero
  Desde el cálculo de la descripción de estadística, Pearson/Spearman  Related Faeces y Cuadros de Diferencia

- Realizar pruebas de hipótesis (t-test, chi-cuadrado) e interpretar correctamente los valores de p e intervalos de confianza
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- Utilice el re-muestreo de bootstrap para construir intervalos de confianza para cualquier métrica sin suposiciones de distribución
  Utiliza Bootstrap 重采样为任意标标构建置信区间, no necesita hipótesis de distribución

- Distinguir la importancia estadística de la importancia práctica mediante medidas de tamaño de efecto
  Utilización de la diferencia entre la importancia estadística y la importancia real

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性 这些是ML 实验评估的基础──

## El problema es la introducción del problema

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署了B──三周后线上效果反而变化了因为 0.02 de las diferencias es ruido no es real aumento──统计学答案: ¿Es el diferencial notable?

## El concepto central.

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**: 推/搜索模型上线前必须做,统计显著(p<0.05) sólo se publicó;(2) **Bootstrap 置信区间**: no se utiliza la distribución de datos, se utiliza el modelo de construcción de cualquier indicación de la confianza;**效应量**:p 值 only tells you"¿hay ninguna diferencia",effect量 tells you"¿hay mucha diferencia"Statistics significant ≠ 实际有用;**多重比较校正**El mejor de los 20 superparámetros, debe ser "do碰运气" o "do碰运气".

Esto sucede constantemente. Cambios en el ranking de la tabla de clasificación. Papeles que no se reproducen. Pruebas A/B que declaran ganadores basándose en unos cientos de muestras. La causa es siempre la misma: alguien saltó las estadísticas.

> Esto ocurre con frecuencia. La mayoría de las veces se complica. El problema es que se ha saltado la estadística.

Las estadísticas te dan las herramientas para distinguir la señal del ruido. Te dice cuándo es real una diferencia, cuán seguro debes estar, y cuántos datos necesitas antes de confiar en un resultado. Cada tubería de ML, cada comparación de modelos, cada experimento necesita estadísticas.

> La estadística te proporciona una herramienta para distinguir entre señales y ruidos. Te dice cuándo es real la diferencia, cuánto confianza debes tener, y cuántos datos necesitas para creer en un resultado. Cada tubo de ML, cada modelo de comparación, cada experimento requiere estadística.

## El concepto central.

### Estadísticas descriptivas: resumiendo sus datos

Antes de modelar algo, necesitas saber cómo se ven los datos. Las estadísticas descriptivas comprimen un conjunto de datos en unos pocos números que capturan su forma.

> Antes de construir cualquier modelo, necesitas entender el modelo de los datos. La estadística descriptiva comprimirá el conjunto de datos en varios números que puedan capturar su forma.

**Measures of central tendency**Respuesta: "¿Dónde está el centro?"

> **集中趋势度量**¿En el medio de dónde?"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

La media es el punto de equilibrio. La media es la marca de mitad. Cuando divergen, su distribución es sesgada. Las distribuciones de ingresos tienen media >> media (desde la derecha de los multimillonarios). Las distribuciones de pérdidas durante el entrenamiento a menudo tienen media << media (desde la izquierda de las muestras fáciles).

> 平均值是平衡点──中位数是中标── cuando se desvían, tu distribución es desviada──收入分布的平均值远大于中位数(亿万富翁造成的右偏)── entrenamiento Distribución de pérdidas durante el entrenamiento Normalmente el promedio de pérdidas es muy pequeño que el mediano数(简单样本造成的左偏)──

**Measures of spread**Respuesta: "¿Qué tan disperso está el dato?"

> **离散程度度量**¿Hay datos que se dispersen?"

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

**Percentiles**El 25o percentil (Q1) significa que el 25% de los valores caen por debajo de este punto. El 50o percentil es la media. El 75o percentil es Q3.

> **百分位数**Se dividirá el dato de la clasificación posterior en 100 等份──第25百分位数(Q1) significa que el valor del 25% es inferior a este punto──第50百分位数就是中位数──第75百分位数是Q3──

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

En ML, te importan los percentiles para la latencia de inferencia, las distribuciones de confianza de predicción y la comprensión de las distribuciones de errores. Un modelo con un error promedio bajo pero un error P99 terrible podría ser inútil para aplicaciones críticas a la seguridad.

> En ML, se trata de un modelo de teorías de retraso, de la predicción de la confianza en la distribución y el error de distribución de porcentajes. Un modelo de error promedio es bajo pero P99  errores muy pobres, para aplicaciones clave de seguridad puede ser inútil.

**Sample vs population statistics.**Cuando se calcula la varianza de una muestra, divide por (n-1) en lugar de n. Esta es la corrección de Bessel. Compensará el hecho de que su media de muestra no es la media de población verdadera.

> **样本统计 vs 总体统计。**Desde el cálculo de la diferencia de muestras, el cálculo de la diferencia de muestras (n-1) no es n. Es la corrección de Bessel.

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

En la práctica: si n es grande (miles de muestras), la diferencia es insignificante.

> 实践中: si n 很大(数千个样本), la diferencia puede ser ignorada.

### Correlación: Cómo se mueven las variables juntas  Relación: cómo cambian las variables juntas

La correlación mide la fuerza y la dirección de una relación lineal entre dos variables.

>  Relación mide la intensidad y la dirección de la relación lineal entre dos variables

**Pearson correlation coefficient**medidas de asociación lineal:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson asume que la relación es lineal y ambas variables están distribuidas aproximadamente normalmente. Es sensible a los valores extremos.

> Pearson  hipótesis de la relación es lineal, y dos variables se adecúan en gran medida a la distribución de estado normal.

**Spearman rank correlation**medidas de asociación monótona:

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

**The golden rule:**La correlación no implica la causalidad. Las ventas de helados y las muertes por ahogamiento están correlacionadas porque ambas aumentan en verano. La precisión de su modelo y el número de parámetros están correlacionados, pero añadir parámetros no mejora automáticamente la precisión (ver: sobreajuste).

> **黄金法则：**相关不意味因果──冰淋销量和溺水死亡是相关的,因为 ambas aumentan en verano──你的模型精度和参数数数量是相关的, pero aumentar los参数 no mejora automáticamente la precisión.

### Matriz de covarianza .

La covarianza entre dos variables mide cómo varían juntas:

> La diferencia de equilibrio entre dos variables mide cómo cambian juntos:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

Para d características, la matriz de covarianza C es una matriz de d x d donde C[i][j] = Cov(feature_i, feature_j). Las entradas diagonales C[i][i] son las variaciones de cada característica.

> 对于d 个特征,协方差矩阵 C es una d x d矩阵, en la cual C[i][j] = Cov(feature_i, feature_j) ――对角线元素 C[i][i] 是每个特征的方差──

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

**Connection to PCA.**PCA propiocomponen la matriz de covarianza. Los propios vectores son los componentes principales (direcciones de la varianza máxima). Los valores propios le dicen cuánto variación capta cada componente. Esto es exactamente lo que la lección 10 cubrió, pero ahora ve por qué la matriz de covarianza es lo correcto para descomponer: codifica todas las relaciones lineales en pares en sus datos.

> **与 PCA 的联系。**PCA hace rasgos de descomposición de la matriz de diferencia de la combinación. La característica de la medida de la diferencia es el componente principal. El valor de la característica le dice a cada componente cuántos diferencia de la combinación de las diferencias de la combinación. Este es el contenido de la 10a clase, pero ahora entiende por qué la matriz de descomposición de la combinación es un objeto de descomposición correcto: codifica todas las relaciones lineares en los datos.

**Connection to correlation.**La matriz de correlación es la matriz de covarianza de variables estandarizadas (cada una dividida por su desviación estándar). La correlación normaliza la covarianza por lo que todos los valores caen en [-1, 1].

> **与相关性的联系。**相关矩阵是标准化变量 (), cuya cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuota de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta de cuenta

### Prueba de hipótesis.

Las pruebas de hipótesis son un marco para tomar decisiones bajo incertidumbre.

>  Supongamos que la prueba es un marco de toma de decisiones bajo incertidumbre―, empiezas con una propuesta, recopiles datos y luego juzgas si los datos coinciden con la propuesta―.

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**Es la probabilidad de ver datos tan extremos como lo que observó, suponiendo que H0 es verdad. NO es la probabilidad de que H0 sea verdad.

> **p 值**Es en H0 por la hipótesis real, observar la probabilidad de los datos observados en el mismo extremo o más extremo de los datos observados.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**dar un rango de valores plausibles para un parámetro:

> **置信区间**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

El ancho del intervalo de confianza le dice acerca de la precisión. Los intervalos amplios significan una alta incertidumbre.

> La amplitud de la zona de confianza le dice la precisión. La amplitud significa alta incertidumbre. La estrecha significa que su estimación es precisa.

### El examen de la prueba.

La prueba comparó los medios. Hay varios sabores.

> T 检测比较平均值──有几种变量──

**One-sample t-test:**¿Es la media de población diferente de un valor hipotético?

> **单样本 t 检验：**¿Es el valor medio total diferente del valor de hipótesis?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**¿Son dos grupos diferentes?

> **两样本 t 检验（独立）：**¿Es diferente el valor medio de los dos grupos?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**cuando las mediciones se realicen en parejas (el mismo modelo evaluado en las mismas particiones de datos):

> **配对 t 检验：**Cuando la medida es realizada en la misma medida de los mismos modelos en la misma data divisor evaluar:

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

En ML, el t-test emparejado es común: ejecutas ambos modelos en los mismos 10 pliegues de validación cruzada y comparas sus puntajes en pareja.

> En ML, el uso de la prueba de cero es muy común: se ejecuta dos modelos en diez faltas de cero, y luego se compara el número de partes de ellos.

### Prueba de Chi-cuadrado. Prueba de la Carpa.

El test de chi-cuadrado comprueba si las frecuencias observadas coinciden con las frecuencias esperadas.

> 卡方检查检查 观测频率是否匹配期望频率──适用于分类数据──

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

### Pruebas A/B para modelos ML    тест A/B de modelos ML  

Las pruebas A/B en ML no son lo mismo que las pruebas A/B en la web.

> Los modelos comparados tienen desafíos específicos:

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

### Significación estadística vs. Significación práctica.

Un resultado puede ser estadísticamente significativo pero prácticamente sin sentido.

> Un resultado puede ser estadísticamente significativo pero en la práctica no tiene sentido. Cuando los datos son suficientes, incluso las diferencias insignificantes se vuelven estadísticamente significativas.

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

**Effect size**cuantifica la magnitud de la diferencia, independientemente del tamaño de la muestra:

> **效应量** Diferencias cuantitativas son grandes, sin relación con la cantidad de muestras:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Siempre informe tanto el valor p como el tamaño del efecto. El valor p le dice si la diferencia es real. El tamaño del efecto le dice si importa.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真实──效应量告诉你差异是否有意义──

### Problemas de comparación múltiple.

Cuando se prueban muchas hipótesis, algunas serán "significativas" por casualidad. Si se prueban 20 cosas en alfa = 0.05, se espera 1 falso positivo incluso cuando nada es real.

> Cuando usted examina muchas hipótesis, algunas se producen por casualidad "significativas"― Si usted examina 20 cosas en alfa = 0.05―, incluso sin efecto real, usted también espera tener 1 falso positivo―.

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**dividir el alfa por el número de pruebas.

> **Bonferroni 校正：**Se puede hacer un examen de alfa.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

En ML, esto importa cuando se compara un modelo a través de múltiples métricas, se prueban muchas configuraciones de hiperparámetros o se evalúa en múltiples conjuntos de datos.

> En ML, cuando se compara un modelo en varios indicadores, se evalúa en varios conjuntos de datos o se evalúa en varios superparámetros, esto es importante.

### Métodos de arranque

Bootstrapping estima la distribución de muestras de una estadística mediante el replanteamiento de los datos.

> Bootstrap                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

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

Esto es más robusto que la prueba de t emparejada porque no hace suposiciones de distribución.

> Esto es más estable que el uso de la prueba, porque no hace hipótesis de distribución.

### Parámetros contra no parámetros Tests.

**Parametric tests**asumir una distribución específica (generalmente normal):

> **参数检验**假设特定分布 (normalmente es una distribución de estado correcto):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**no hacer suposiciones de distribución:

> **非参数检验**No hace la distribución:

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

En los experimentos ML, por lo general se tienen pequeñas n (5 o 10 plegas de validación cruzada), por lo que las pruebas no parámétricas como Wilcoxon-signat-rank son a menudo más apropiadas que las pruebas t.

> En el experimento ML, normalmente tienes un pequeño n(5 o 10 交叉验证折), así que como Wilcoxon 符号秩, los controles sin parámetros suelen ser más adecuados que los de t.

### Teorema de límite central: implicaciones prácticas.

El CLT dice que la distribución de la muestra se acerca a una distribución normal a medida que n crece, independientemente de la distribución de la población subyacente.

> CLT dice que, con el crecimiento, la distribución del valor medio de muestras se acerca a la distribución normal, independientemente de cómo se distribuya el conjunto de la base.

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

### Errores estadísticos comunes en los artículos ML 论文中常见的统计错误

1. **Testing on the training set.**Siempre mantenga datos que el modelo no ve durante el entrenamiento.

> 1. **在训练集上测试。**Garantizar que está preparado. Siempre guardando datos que nunca había visto durante el entrenamiento del modelo.

2. **No confidence intervals.**La información de un solo número de precisión sin incertidumbre hace que los resultados no sean reproducibles y no puedan ser verificados.

> 2. **没有置信区间。** Reportar un solo número de precisión sin una medida de incertidumbre, haciendo que los resultados sean irrefutables e indetectables¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

3. **Ignoring multiple comparisons.**Probar 50 configuraciones y reportar la mejor sin corrección inflama tasas falsas positivas.

> 3. **忽略多重比较。**测试 50 配置并报告最好一个不做校正,会膨胀假阳性率──

4. **Confusing statistical and practical significance.**Un valor p de 0,001 en una mejora de precisión del 0,01% no es significativo.

> 4. **混淆统计显著性和实际显著性。**0.01%  Precisión de aumento de p  Valor 0.001  No tiene sentido 

5. **Using accuracy on imbalanced data.**99% de precisión en un conjunto de datos con 99% de clase negativa significa que el modelo no aprendió nada.

> 5. **在不平衡数据上使用精度。**En el 99% de los datos negativos, el 99% de precisión significa que el modelo no ha aprendido nada.

6. **Cherry-picking metrics.**Sólo se informa la métrica donde gana el modelo.

> 6. **挑选指标。**Sólo informe los indicadores de ganancia de su modelo.

7. **Leaking information across train/test splits.**Normalizando antes de dividir, o usando datos futuros para predecir el pasado.

> 7. **在训练/测试划分之间泄露信息。**En la división anterior se hace la regeneración, o se utiliza el futuro de datos de la predicción pasada.

8. **Small test sets with no variance estimates.**La evaluación en 100 muestras y la afirmación de una mejora del 2% es ruido, no señal.

> 8. **小测试集没有方差估计。**En 100 muestras evaluadas, se afirmó que el aumento del 2% fue el ruido, no el señal.

9. **Assuming independence when data is not independent.**Imágenes médicas del mismo paciente, varias frases del mismo documento.

> 9. **数据不独立时假设独立。**La imagen médica del mismo paciente, varias frases del mismo archivo, y el grupo de observaciones están relacionados.

10. **P-hacking.**Probando diferentes pruebas, subconjuntos o criterios de exclusión hasta que obtengas p < 0,05. El resultado es un artefacto de la búsqueda.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, hasta obtener p < 0.05──结果是搜索过程的伪影──

## Construirlo se realiza de la mano

Implementará:

> Usted va a lograr:

1. **Descriptive statistics from scratch**(media, media, modo, desviación estándar, percentil, RIC)
   **从零实现描述性统计**(medio valor, medio número, número de personas, diferencia de nivel, porcentaje de personas, RSI)
2. **Correlation functions**(Pearson y Spearman, con la matriz de covarianza)
   **相关函数**(Pearson y Spearman, así como la matriz de la diferencia)
3. **Hypothesis tests**(t-test de una muestra, t-test de dos muestras, chi-squared test)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(para cualquier estadística, no se necesitan suposiciones)
   **Bootstrap 置信区间**(con un número de datos de datos de la empresa)
5. **A/B test simulator**(generar datos, probar, verificar si hay errores de tipo I y tipo II)
   **A/B 测试模拟器**(Generar datos, probar, revisar la primera y segunda clase de errores)
6. **Statistical vs practical significance demo**(mostrando que la gran n hace que todo sea "significativo")
   **统计 vs 实际显著性演示**(Mostra grande n 使一切都" significativo")

Todo desde cero, usando sólo`math`y `random`No hay numpy, no hay scipy.

> Todo desde el cero, sólo para usar.`math`Y `random`❖ 不使用 numpy、scipy。

## Términos clave .
```figure
f3-bootstrap-resample
```

## Términos clave

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
