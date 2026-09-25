# Estatísticas para aprendizado de máquina

> A estatística é como se sabe se o seu modelo funciona ou só teve sorte.
> A estatística diz-te se o modelo é realmente eficaz ou apenas bom.

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizagem

- Computa estatísticas descrittivas, correlação Pearson/Spearman e matrizes de covariância a partir do zero
  Desde zero cálculo descrito statistiquom  Pearson/Spearman  Related系数和协方差矩阵

- Realizar testes de hipótese (t-test, chi-quadrado) e interpretar corretamente os valores de p e os intervalos de confiança
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- Use bootstrap resampling para construir intervalos de confiança para qualquer métrica sem suposições distributivas
  Utilize Bootstrap 重采样为任意标标构建置信区间,无需分布假设

- Distinguir significância estatística da significância prática utilizando medidas de tamanho do efeito
  Utilização de quantidade de efeitos Diferença entre significância estatística e significância real

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性这些是ML 实验评估的基础──

## O problema é o problema da introdução

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署了B──三周后线上效果反而变差了因为 0.02 差是噪音不是真实升升──统计学答案:差是否显著?置信区间多宽?样本量不够?没有统计学ML 实验 = 盲摸象──

## O conceito central.

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**O que é que é necessário fazer?**Bootstrap 置信区间**Não é necessário uma distribuição de dados, mas um modelo de construção de qualquer indicado de um setor de dados.**效应量**:p 值只告诉你"有没有差异",efffect量告诉你"差异有多多大"统计显著 ≠ 实际有用;**多重比较校正**O que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor é que o que é melhor.

Isto acontece constantemente. O ranking de um cartão de vendas é alterado. Papéis que não se reproduzem. Testes A/B que declaram vencedores com base em algumas centenas de amostras. A causa é sempre a mesma: alguém saiu das estatísticas.

> O que acontece com frequência é que há um grande problema na classificação, que não pode ser repetido, com base em centenas de amostras de testes A/B anunciados como vencedores, e a razão fundamental é sempre a mesma: alguém está a saltar a estatística.

A estatística dá-lhe as ferramentas para distinguir sinal do ruído. Ela diz-lhe quando uma diferença é real, quão confiante você deve ser e quantos dados você precisa antes de confiar em um resultado.

> A estatística fornece-lhe uma ferramenta para distinguir sinais e ruídos. Ela diz-lhe quando as diferenças são reais, quanto confiança você deve ter, e quanto dados você precisa para acreditar em um resultado.

## O conceito central.

### Estatísticas descritivas: Resumindo seus dados

Antes de modelar qualquer coisa, é preciso saber como são os dados.

> Antes de criar qualquer modelo, você precisa entender a forma de dados.

**Measures of central tendency**Resposta: "Onde está o meio?"

> **集中趋势度量**Responder "em meio a onde?"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

A média é o ponto de equilíbrio. A média é a marca de meio caminho. Quando divergem, sua distribuição é distorcida. As distribuições de renda têm média >> mediana (distribuição direita dos bilionários). As distribuições de perdas durante o treinamento muitas vezes têm média << mediana (distribuição esquerda de amostras fáceis).

> 平均值是平衡点──中位数是中标── quando eles se desviam, sua distribuição é inclinada──收入分布的平均值远大于中位数(亿万富翁造成的右偏)── treino distribuição de perdas durante a formação geralmente é menor do que中位数(简单样本造成的左偏)──

**Measures of spread**Resposta: "Quão disperso está o dados?"

> **离散程度度量**Responder: "Datos estão disponíveis?"

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

**Percentiles**Divida os dados classificados em 100 partes iguais. O 25o percentil (Q1) significa que 25% dos valores caem abaixo deste ponto. O 50o percentil é a média. O 75o percentil é Q3.

> **百分位数**A classificação de dados posterior dividirá em 100 e assim por diante.

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

Em ML, você se importa com percentil para latência de inferência, distribuições de confiança de previsão e distribuições de erro de compreensão. Um modelo com erro médio baixo, mas erro P99 terrível pode ser inútil para aplicações críticas à segurança.

> No ML, você se preocupa com a teoria do atraso, a previsão da confiança e a porcentagem de distribuição de erros. Um modelo com um erro médio baixo, mas P99 muito ruim, pode ser inútil para aplicações de segurança.

**Sample vs population statistics.**Quando você calcula a variância de uma amostra, divide por (n-1) em vez de n. Esta é a correção de Bessel. Ele compensa o fato de que a média da amostra não é a média da população verdadeira. Com n no denominador, você subestima sistematicamente a variância verdadeira. Com (n-1), a estimativa é imparcial.

> **样本统计 vs 总体统计。**A partir do cálculo de um sample, separando em (n-1) não n. É a correção de Bessel.

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

Na prática: se n é grande (milhares de amostras), a diferença é insignificante.

> 实践中: se n 很大(数千个样本), a diferença pode ser ignorada;; se n 很小(几十个样本), a diferença é importante。

### Correlação: Como as variáveis se movem juntas

A correlação mede a força e a direção de uma relação linear entre duas variáveis.

> Relatividade Messa a intensidade e direção da relação linear entre duas variáveis.

**Pearson correlation coefficient**Medidas de associação linear:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson assume que a relação é linear e ambas as variáveis são aproximadamente normalmente distribuídas. É sensível a valores fora do horizonte.

> Pearson  hipóteses de relação é linear, e duas variações são amplamente obedecidas à distribuição normal.

**Spearman rank correlation**Medidas de associação monótona:

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

**The golden rule:**A correlação não implica a causalidade. As vendas de gelados e as mortes por afogamento estão correlacionadas porque ambas aumentam no verão. A precisão do modelo e o número de parâmetros estão correlacionados, mas adicionar parâmetros não melhora automaticamente a precisão (ver: sobre-ajustamento).

> **黄金法则：**相关不意味因果──冰淋销量和溺水死亡是相关的,因为 ambas aumentam no verão──你的模型精度和参数数数量是相关的,但增加参数并没有自动提高精度(参见:过拟合) 

### Matriz de Covariância

A covariância entre duas variáveis mede a sua variação conjunta:

> A diferença de coesão entre duas variações mede como elas mudam juntas:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

Para d características, a matriz de covariância C é uma matriz d x d onde C[i][j] = Cov(feature_i, feature_j). As entradas diagonais C[i][i] são as variâncias de cada característica.

> 对于d 个特征,协方差矩阵 C é uma d x d矩阵, em que C[i][j] = Cov(feature_i, feature_j) ――对角线元素 C[i][i] 是每个特征的方差──

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

**Connection to PCA.**O PCA compõe a matriz de covariância. Os vetores próprios são os componentes principais (direções de variância máxima). Os valores próprios dizem-lhe quanta variância cada componente capta. Isto é exatamente o que a lição 10 cobriu, mas agora você vê por que a matriz de covariância é a coisa certa para se descompor: ele codifica todas as relações lineares em pares em seus dados.

> **与 PCA 的联系。**O PCA faz características de descomposição de uma matriz de diferenciação de coeficientes. O valor de caracteres diz-lhe quanto diferença de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficientes de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de coeficients de de de de de de de de de de de de deficients de de de de de deficients de de de de deficients de de de de de deficients de de de de deficients de de de de de deficients de de de de de de deficients de de de de de de de deficients de de de de de de de deficients de de de de de de de deficients de de de de de de de deficients de de de de de de de de de de deficients de de de de de de de de deficients de de de de de de de de de de deficients de de de de de de deficients de de de de de de de de de de de deficients de de de de de de de de de de de de de de de de de de de de de de de de

**Connection to correlation.**A matriz de correlação é a matriz de covariância de variáveis padronizadas (cada uma dividida por seu desvio padrão).

> **与相关性的联系。**Relacionamento é uma matriz de variação padronizada (incluindo os valores de variação padronizada) de cada uma, que excede os seus valores padronizados.

### Teste de hipóteses.

Testes de hipóteses são um quadro para tomar decisões sob incerteza. Começa com uma alegação, coleta dados e determina se os dados são consistentes com a alegação.

>  assumiu que a análise é um quadro de tomada de decisão sob incerteza.

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**É a probabilidade de ver dados tão extremos quanto o que você observou, supondo que H0 é verdade.

> **p 值**É observado que, sob a hipótese H0 é real, a probabilidade de dados observados é igual ou mais extrema. Não é H0 é probabilidade real. É o erro mais comum na estatística.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**indicar uma faixa de valores plausíveis para um parâmetro:

> **置信区间**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

O comprimento do intervalo de confiança diz-lhe sobre a precisão. intervalos largos significam alta incerteza. intervalos estreitos significam que a sua estimativa é precisa (mas não necessariamente precisa, se os seus dados são tendenciosos).

> 置信区间的宽度告诉你精度──宽区间 significa alta incerteza──窄区间 significa que sua estimativa é precisa, mas se os dados tiverem preconceito, não é necessariamente preciso.

### O teste de T.

O teste t compara os meios.

> T 检测比较平均值──有几种变异──

**One-sample t-test:**A média populacional é diferente de um valor hipotético?

> **单样本 t 检验：** O valor médio total é diferente do valor de hipóteses?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**São dois grupos significados diferentes?

> **两样本 t 检验（独立）：**O valor médio dos dois grupos é diferente?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**Quando as medições forem realizadas em pares (o mesmo modelo avaliado em partes de dados):

> **配对 t 检验：**Quando a medida é realizada em relação a um mesmo modelo em uma mesma divisão de dados:

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

No ML, o teste de t em par é comum: você executa ambos os modelos nas mesmas 10 dobras de validação cruzada e compara as suas pontuações em pares.

> No ML, é comum comparar t 检验: você executa dois modelos em 10 foldas de verificação de intervalo iguais, e depois compara o número de porções delas.

### Teste quadrado de Chi. Teste de Carbo.

O teste de chi-quadrado verifica se as frequências observadas correspondem às frequências esperadas.

> 卡方检查检查观测频率是否匹配期望频率── aplica-se a 分类数据──

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

### A/B Testing para modelos ML                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

A análise A/B em ML não é a mesma que a análise A/B na web. A comparação de modelos apresenta desafios específicos:

> A/B 测试与网页 A/B 测试不同──模型比较有特定挑战:

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

### Significação estatística vs. Significação prática.

Um resultado pode ser estatisticamente significativo, mas praticamente sem significado. Com dados suficientes, até mesmo uma diferença trivial se torna estatisticamente significativa.

> Um resultado pode ser estatisticamente significativo, mas na prática sem significado. Quando os dados são suficientes, mesmo pequenas diferenças também se tornam estatísticas significativas.

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

**Effect size**quantifica a grandeza da diferença, independentemente do tamanho da amostra:

> **效应量**Quantificação diferença é grande, não tem relação com a quantidade de amostras:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Sempre informe o p-valor e o tamanho do efeito. O p-valor diz-lhe se a diferença é real.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真实──效应量告诉你差异是否有意义──

### Problemas de comparação múltipla.

Quando você testa muitas hipóteses, algumas serão "significativas" por acaso. Se você testar 20 coisas em alfa = 0,05, você espera 1 falso positivo mesmo quando nada é real.

> Quando você verifica muitas hipóteses, algumas delas são "significativas"...... se você estiver no alfa = 0,05

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**Dividir o alfa pelo número de testes.

> **Bonferroni 校正：**A partir de agora, a lista de casos de exame será alterada.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

No ML, isso importa quando você compara um modelo em várias métricas, testa muitas configurações de hiperparâmetros ou avalia em múltiplos conjuntos de dados.

> No ML, quando você compara modelos em vários indicadores, testa várias configurações de superparâmetros ou avalia em vários conjuntos de dados, isso é importante.

### Metodos de arranque

O Bootstrapping estima a distribuição de amostragem de uma estatística re-amostragem de seus dados com substituição.

> Bootstrap  através de um levantamento de dados de pesquisa para estimar a distribuição de dados estatísticos  Não é necessário fazer qualquer hipótese sobre a distribuição de nível inferior 

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

Este é mais robusto do que o teste de t emparelhado porque não faz suposições distributivas.

> É mais estável que o comparativo de t, porque não faz hipóteses de distribuição.

### Parâmetro vs. Não Parâmetro Testes .

**Parametric tests**Assumir uma distribuição específica (geralmente normal):

> **参数检验**假设特定分布 (normalmente distribuição em estado normal):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**Não fazer suposições de distribuição:

> **非参数检验**Não fazer hipóteses de distribuição:

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

Em experimentos de ML, normalmente há pequenas n (5 ou 10 dobras de validação cruzada), por isso, os testes não paramétricos como o Wilcoxon-signature-rank são muitas vezes mais apropriados do que os testes t.

> Em experiências de ML, você geralmente tem um pequeno n ((5 ou 10 交叉验证折), então, como Wilcoxon 符号秩, os exames não-parametral como este geralmente são mais adequados do que os t 检验.

### Teorema do limite central: implicações práticas.

A CLT diz que a distribuição de amostras se aproxima de uma distribuição normal à medida que a n cresce, independentemente da distribuição populacional subjacente.

> A CLT diz que, com o crescimento, a distribuição do valor médio de amostra tende a se aproximar da distribuição normal, independentemente da distribuição geral do nível inferior.

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

### Erros estatísticos comuns em papéis ML 论文中常见的统计错误

1. **Testing on the training set.**Garantia de sobreajuste, sempre forneça dados que o modelo nunca vê durante o treinamento.

> 1. **在训练集上测试。**Garantizar que está preparado. Sempre reter dados nunca vistos durante o treinamento.

2. **No confidence intervals.**Relatar um único número de precisão sem incerteza torna os resultados irreprodutíveis e não verificáveis.

> 2. **没有置信区间。** Reporting single precision numbers without uncertainty measures, making the results irrefutable and unverifiable¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

3. **Ignoring multiple comparisons.**Testar 50 configurações e relatar a melhor sem correcção aumenta as taxas falsas positivas.

> 3. **忽略多重比较。**Test 50 配置并报告最好一个不做校正,会膨胀假阳性率──

4. **Confusing statistical and practical significance.**Um p-valor de 0,001 em uma melhora de precisão de 0,01% não é significativo.

> 4. **混淆统计显著性和实际显著性。**0.01% P  Valor de p                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

5. **Using accuracy on imbalanced data.**99% de precisão num conjunto de dados com 99% classe negativa significa que o modelo não aprendeu nada.

> 5. **在不平衡数据上使用精度。**Na 99% de dados negativos, 99% de precisão significa que o modelo não aprendeu nada.

6. **Cherry-picking metrics.**Só relatar as métricas em que o seu modelo ganha.

> 6. **挑选指标。**Apenas informe os indicadores de ganho do seu modelo.

7. **Leaking information across train/test splits.**Normalização antes de dividir, ou usando dados futuros para prever o passado.

> 7. **在训练/测试划分之间泄露信息。**Emprego de dados de futuro.

8. **Small test sets with no variance estimates.**A avaliação em 100 amostras e a afirmação de uma melhoria de 2% é ruído, não sinal.

> 8. **小测试集没有方差估计。**Em 100 amostras avaliadas, a afirmação de que o aumento de 2% é ruído, não sinal.

9. **Assuming independence when data is not independent.**Imagens médicas do mesmo paciente, várias frases do mesmo documento.

> 9. **数据不独立时假设独立。**Imagem médica do mesmo paciente, várias frases do mesmo arquivo, grupo de observações são relacionadas.

10. **P-hacking.**Tentar diferentes testes, subconjuntos ou critérios de exclusão até obter p < 0,05. O resultado é um artefato da pesquisa.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, até obter p < 0.05── resultado é a falsa imagem do processo de busca──

## Construir isso em movimento

Implementarão:

> Você vai realizar:

1. **Descriptive statistics from scratch**(média, média, modo, desvio padrão, percêntulos, RQI)
   **从零实现描述性统计**(valor médio, número de pessoas, diferença de padrão, percentagem de pessoas, RQI)
2. **Correlation functions**(Pearson e Spearman, com a matriz de covariância)
   **相关函数**(Pearson e Spearman, bem como a colaboração)
3. **Hypothesis tests**(teste de uma amostra, teste de duas amostras, teste de chi-quadrado)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(para qualquer estatística, não são necessárias suposições)
   **Bootstrap 置信区间**(quantificação arbitrária, não necessária)
5. **A/B test simulator**(Generar dados, testar, verificar os erros de tipo I e tipo II)
   **A/B 测试模拟器**(Generar dados, testar, verificar o primeiro e o segundo tipos de erros)
6. **Statistical vs practical significance demo**(mostrando que grande n faz tudo "significante")
   **统计 vs 实际显著性演示**(Mostra grande n fazer tudo "significativo")

Tudo do zero, usando apenas`math`E ...`random`Não há cretinos, nem cretinos.

> Tudo desde zero realizado, apenas para uso `math`和 `random`Não usam numpy,cipy.

## Termos-chave .
```figure
f3-bootstrap-resample
```

## Termos-chave

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
