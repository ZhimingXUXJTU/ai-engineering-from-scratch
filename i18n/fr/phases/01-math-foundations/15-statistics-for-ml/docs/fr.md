# Statistiques pour l'apprentissage automatique

> Les statistiques sont la façon de savoir si votre modèle fonctionne vraiment ou si vous avez eu de la chance.
> La statistique vous dit si le modèle est vraiment efficace ou simplement bon.

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objectifs d'apprentissage

- Comptez les statistiques descriptives, la corrélation Pearson/Spearman et les matrices de covariance à partir de zéro
  De la 0 à la 0 calcul descriptif statistique  Pearson/Spearman  Related Factors and Coefficients

- Effectuer des tests d'hypothèse (t-test, chi-quadré) et interpréter correctement les valeurs p et les intervalles de confiance
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- Utiliser le reéchantillonnage de la bande de démarrage pour construire des intervalles de confiance pour toute mesure sans hypothèses de distribution
  Utilisation Bootstrap 重采样为任意标标构建置信区间, sans besoin de distribution

- Distinguer la signification statistique de la signification pratique en utilisant des mesures de taille des effets
  Utilisation de la signification statistique et de la signification réelle

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性这些是ML 实验评估的基础――

## Le problème , l' introduction du problème

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署了B──三周后线上效果反而变差因为 0.02 差异是噪音不是真实升级──统计学答案:差异是显著吗置信区间多宽?样本量不够?没有统计学ML 实验 = 盲摸象──

## Le concept de base.

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**: Recommandations / recherche modèle sur la ligne doit être fait, statistiques significatives ((p<0.05) ont été publiées;(2) **Bootstrap 置信区间**: pas besoin de la distribution de données, de la réception pour construire des indices de confiance;**效应量**:p 值 only tells you" have no difference",efffect quantity tells you" have a much difference"statistique significative ≠ 实际有用;**多重比较校正**Il y a 20 super-paramètres qui sont les meilleurs, il faut les modifier.

Les résultats de l'étude sont toujours les mêmes: des résultats négatifs, des tests A/B qui déclarent les gagnants sur la base de quelques centaines d'échantillons.

> Ce genre de choses se produisent souvent. Les problèmes de classement sont insurmontables. Les résultats des tests A/B sont généralement les mêmes:

Les statistiques vous donnent les outils pour distinguer le signal du bruit. Elles vous disent quand une différence est réelle, à quel point vous devez être sûr et à quelle quantité de données vous avez besoin avant de pouvoir faire confiance à un résultat. Chaque pipeline de ML, chaque comparaison de modèle, chaque expérience a besoin de statistiques. Sans cela, vous devinez.

> La statistique vous fournit un outil pour distinguer les signaux et le bruit. Elle vous dit quand les différences sont réelles, à quel point vous devriez avoir confiance, et combien de données vous avez besoin pour croire un résultat.

## Le concept de base.

### Statistique descriptive: résumer vos données

Avant de modéliser quoi que ce soit, vous devez savoir à quoi ressemblent vos données.

> Avant de créer un modèle, vous devez comprendre la forme des données.

**Measures of central tendency**Réponse: " Où est le milieu ? "

> **集中趋势度量**Répondre "entre où ?"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

La moyenne est le point d'équilibre. La médiane est la marque à mi-chemin. Quand elles divergent, votre répartition est faussée. Les répartitions de revenus ont la moyenne >> médiane (faussée droite des milliardaires). Les répartitions de pertes pendant la formation ont souvent la moyenne << médiane (faussée gauche des échantillons faciles).

> La moyenne est un point d'équilibre. La moyenne est un signe intermédiaire. Lorsque les écarts sont faits, votre répartition est tendue. La moyenne de la distribution des revenus est supérieure à la moyenne.

**Measures of spread**Répondre à "combien les données sont dispersées?"

> **离散程度度量**"Il y a peut-être des données?"

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

**Percentiles**Le 25e percentile (Q1) signifie que 25% des valeurs tombent en dessous de ce point. Le 50e percentile est la médiane. Le 75e percentile est Q3.

> **百分位数**Pour la classification, les données sont divisées en 100 et suivantes:

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

En ML, vous vous souciez des percentiles pour la latence d'inférence, les distributions de confiance de prédiction et la compréhension des distributions d'erreurs. Un modèle avec une erreur moyenne faible mais une erreur P99 terrible pourrait être inutile pour les applications critiques pour la sécurité.

> Dans le ML, vous vous occupez du raisonnement de retard, de la prédiction et de la confiance en la distribution et de la distribution des erreurs. Un modèle de moyenne d'erreur faible mais P99 d'erreur très faible, peut être inutile pour les applications de sécurité.

**Sample vs population statistics.**Lorsque vous comptez la variance d'un échantillon, divisez par (n-1) au lieu de n. C'est la correction de Bessel. Cela compense le fait que votre moyenne d'échantillon n'est pas la vraie moyenne de la population. Avec n dans le dénominateur, vous sous-estimez systématiquement la vraie variance. Avec (n-1), l'estimation est impartiale.

> **样本统计 vs 总体统计。**De l'échantillon calculé par différence de carré, en dehors de (n-1) et non par n. C'est la correction de Bessel. Il compense le fait que la valeur moyenne de l'échantillon n'est pas la valeur moyenne totale réelle.

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

En pratique: si n est grand (mille d'échantillons), la différence est négligeable; si n est petit (décennages d'échantillons), cela importe.

> En pratique, si n'y a pas de milliers d'échantillons, les différences peuvent être négligées.

### Corrélation: Comment les variables se déplacent ensemble

La corrélation mesure la force et la direction d'une relation linéaire entre deux variables.

>  Relativité mesure la force et la direction des relations entre deux variables 

**Pearson correlation coefficient**mesures d'association linéaire:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson suppose que la relation est linéaire et que les deux variables sont normalement distribuées.

> Pearson suppose que la relation est linéaire, et que deux variables sont largement soumises à la distribution normale.

**Spearman rank correlation**mesures d'association monotone:

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

**The golden rule:**La correlation ne signifie pas de causalité. Les ventes de crèmes glacées et les décès par noyade sont corrélées car les deux augmentent en été. La précision de votre modèle et le nombre de paramètres sont corrélés, mais l'ajout de paramètres n'améliore pas automatiquement la précision (voir: surmatch).

> **黄金法则：**相关不意味因果──冰冰销量和溺水死亡是相关的,因为它们都在夏季增加──你的模型精度和参数数数是相关的,但增加参数并非自动提高精度(见:过拟合) 

### Matrice de covariance

La covariance entre deux variables mesure leur variation ensemble:

> La différence de coefficients entre deux variables mesure leur évolution ensemble:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

Pour les caractéristiques d, la matrice de covariance C est une matrice d x d où C[i][j] = Cov(feature_i, feature_j). Les entrées diagonales C[i][i] sont les variantes de chaque caractéristique.

> Pour les caractéristiques de la c, la coefficience de différence C est une coefficience de différence de chaque caractéristique.

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

**Connection to PCA.**PCA proprecompose la matrice de covariance. Les propres vecteurs sont les composants principaux (directions de variance maximale). Les valeurs propres vous disent combien de variance chaque composant capture. C'est exactement ce que la leçon 10 couvre, mais maintenant vous voyez pourquoi la matrice de covariance est la bonne chose à décomposer: elle encode toutes les relations linéaires par paires dans vos données.

> **与 PCA 的联系。**La PCA fait des caractéristiques de décomposition de la matrice de différence de couverture. La caractéristique du flux est le composant principal. La valeur de la caractéristique vous dit combien de différences de couverture chaque composant a capturé. C'est exactement ce que j'ai dit dans la 10e classe, mais maintenant vous comprenez pourquoi la matrice de différence de couverture est un objet de décomposition correct: elle code toutes les relations de couverture dans les données.

**Connection to correlation.**La matrice de corrélation est la matrice de covariance des variables normalisées (chacune divisée par son écart standard). La corrélation normalise la covariance de sorte que toutes les valeurs tombent dans [-1, 1].

> **与相关性的联系。**La relation est une relation de variation standardisée, chaque relation est une relation de variation standardisée.

### Test d'hypothèse

Les tests d'hypothèse sont un cadre pour prendre des décisions en cas d'incertitude.

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

**The p-value**C'est la probabilité de voir des données aussi extrêmes que ce que vous avez observé, en supposant que H0 est vrai.

> **p 值**Il est vrai que dans l'hypothèse H0 , on observe la probabilité de données à l'extrémité ou à l'extrémité supérieure des données observées.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**donner une gamme de valeurs plausibles pour un paramètre:

> **置信区间** donner une gamme de valeurs raisonnables à un paramètre:

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

La largeur de l'intervalle de confiance vous indique la précision. Les intervalles larges signifient une grande incertitude.

> La largeur de la zone de confiance vous dit la précision. La largeur signifie une grande incertitude. La petite zone signifie que votre estimation est précise.

### Le t-test .

Le t-test compare les moyens.

> T 检测比较平均值──有几种变异──

**One-sample t-test:**La moyenne de la population diffère-t-elle d'une valeur hypothétique ?

> **单样本 t 检验：** La valeur moyenne totale est-elle différente de la valeur hypothétique ?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**deux groupes signifient-ils différemment?

> **两样本 t 检验（独立）：**La valeur moyenne des deux groupes est-elle différente?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**lorsque les mesures sont effectuées en paires (même modèle évalué sur les mêmes fractions de données):

> **配对 t 检验：**Lorsque la mesure est réalisée par le même modèle dans la même division de données:

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

Dans ML, le t-test parallèle est courant: vous exécutez les deux modèles sur les mêmes 10 plies de validation croisée et comparez leurs scores parallèlement.

> Dans le ML, il est courant de comparer les tests: vous effectuez deux modèles sur les mêmes 10 tests de croisement, puis vous comparez le nombre de fractions.

### Teste de carré en chi.

Le test en chi-quadré vérifie si les fréquences observées correspondent aux fréquences attendues.

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

### Test A/B pour les modèles ML   Test A/B de modèle ML 

Les tests A/B en ML ne sont pas les mêmes que les tests A/B en ligne.

> Les tests A/B du ML sont différents des tests A/B du ML.

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

### Signification statistique contre signification pratique

Un résultat peut être statistiquement significatif mais pratiquement sans signification.

> Un résultat peut être statistiquement significatif mais en réalité il n'a pas d'importance. Lorsque les données sont suffisamment nombreuses, même les différences mineures deviennent statistiquement significatives.

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

**Effect size**quantifie la taille de la différence, indépendamment de la taille de l'échantillon:

> **效应量** différence quantitative est grande, sans rapport avec la quantité d'échantillonnage:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Rapporte toujours la valeur de p et la taille de l'effet. La valeur de p vous indique si la différence est réelle.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真──效应量告诉你差异是否有意义──

### Problème de comparaison multiple Problème de comparaison multiple

Quand vous testez de nombreuses hypothèses, certaines seront "signifiantes" par hasard. Si vous testez 20 choses à alpha = 0,05, vous attendez 1 faux positif même quand rien n'est réel.

> Quand vous examinez de nombreuses hypothèses, certaines se produisent par hasard "signifiant"― Si vous testez 20 choses en alpha = 0,05 − même sans effet réel, vous attendez aussi à avoir 1 faux positif―

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**Divisez alpha par le nombre de tests.

> **Bonferroni 校正：**Il y aura des tests.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

En ML, cela compte quand vous comparez un modèle à travers plusieurs mesures, testez de nombreuses configurations d'hyperparamètres ou évaluez sur plusieurs ensembles de données.

> Dans le ML, lorsque vous comparez des modèles sur plusieurs indicateurs, testez plusieurs superparamètres ou évaluez plusieurs ensembles de données, c'est important.

### Les méthodes de démarrage

Bootstrapping estime la distribution d'échantillonnage d'une statistique en repensant vos données avec un remplacement.

> Bootstrap 通过有放回地重采采数据来估计统计量抽样分布──不需要对底层分布做任何假设──

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

C'est plus robuste que le t-test parallèle car il ne fait aucune hypothèse de distribution.

> Ceci est plus stable que le t-test, car il ne fait pas de supposition de distribution.

### Tests paramétriques contre non paramétriques

**Parametric tests**en supposant une distribution spécifique (généralement normale):

> **参数检验**假设特定分布 (habituellement une distribution en état normal):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**ne prennent pas de hypothèses de distribution:

> **非参数检验**Il n'y a pas de différence entre les deux.

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

Dans les expériences ML, vous avez généralement de petits n (5 ou 10 plies de validation croisée), de sorte que des tests non paramétriques comme Wilcoxon sign-rank sont souvent plus appropriés que les tests t.

> Dans les expériences ML, vous avez généralement de petits n(5 ou 10 交叉验证折), donc comme Wilcoxon 符号 秩, des tests non paramétriques comme celui-ci sont généralement plus appropriés que les tests t.

### Le théorème des limites centrales: implications pratiques

Le CLT indique que la distribution des moyens d'échantillonnage approche une distribution normale à mesure que n augmente, indépendamment de la distribution de la population sous-jacente.

> CLT dit que, avec la croissance, la distribution de la valeur moyenne de l'échantillon tend à se rapprocher de la distribution normale, quelle que soit la distribution globale de la couche inférieure.

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

### Erreurs statistiques courantes dans les documents ML 论文中常见的统计错误

1. **Testing on the training set.**Garantir un surmatch, toujours tenir des données que le modèle ne voit pas pendant la formation.

> 1. **在训练集上测试。**Gardez toujours des données inédites lors de l'entraînement du modèle.

2. **No confidence intervals.**En déclarant un seul numéro d'exactitude sans incertitude, les résultats ne peuvent être reproduits et non vérifiés.

> 2. **没有置信区间。** Rapporter un chiffre de précision unique sans mesure d'incertitude, rendant les résultats irréalisables et indéfectibles 

3. **Ignoring multiple comparisons.**Tester 50 configurations et signaler la meilleure sans correction gonfle les taux de faux positifs.

> 3. **忽略多重比较。**测试 50 配置并报告 一个不做校正,会膨胀假阳性率──

4. **Confusing statistical and practical significance.**Une valeur p de 0,001 sur une amélioration de précision de 0,01% n'est pas significative.

> 4. **混淆统计显著性和实际显著性。**0,01%  précision  amélioration de la valeur de p  0,001  sans signification 

5. **Using accuracy on imbalanced data.**99% d'exactitude sur un ensemble de données avec une classe négative de 99% signifie que le modèle n'a rien appris.

> 5. **在不平衡数据上使用精度。**Dans les données de 99% de catégories négatives, 99% d'exactitude signifie que le modèle n'a rien appris.

6. **Cherry-picking metrics.**Rapporte seulement les mesures où votre modèle gagne.

> 6. **挑选指标。**Rapporte seulement les indicateurs de réussite de ton modèle.

7. **Leaking information across train/test splits.**Normalement avant de se diviser, ou en utilisant des données futures pour prédire le passé.

> 7. **在训练/测试划分之间泄露信息。**Dans le passé, les données ont été analysées.

8. **Small test sets with no variance estimates.**L'évaluation sur 100 échantillons et la prétention d'une amélioration de 2% est du bruit, pas du signal.

> 8. **小测试集没有方差估计。**Dans une évaluation de 100 échantillons, on a affirmé que 2% de l'augmentation était du bruit, pas du signal.

9. **Assuming independence when data is not independent.**Des images médicales du même patient, plusieurs phrases du même document.

> 9. **数据不独立时假设独立。**Les images médicales du même patient, plusieurs phrases du même dossier, sont pertinentes.

10. **P-hacking.**Essayez différents tests, sous-ensembles ou critères d'exclusion jusqu'à ce que vous obteniez p < 0,05. Le résultat est un artefact de la recherche.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, jusqu'à ce que vous obteniez p < 0.05── résultat est une pseudo-image du processus de recherche──

## Construire le réaliser

Vous mettez en œuvre:

> Vous allez réaliser:

1. **Descriptive statistics from scratch**(média, médiane, mode, déviation standard, percentiles, RQI)
   **从零实现描述性统计**(value moyenne, nombre de personnes, différence de niveau, taux de participation, RQI)
2. **Correlation functions**(Pearson et Spearman, avec la matrice de covariance)
   **相关函数**(Pearson et Spearman, ainsi que la même réaction)
3. **Hypothesis tests**(test t-échantillon unique, test t-échantillon double, test chi-quadré)
   **假设检验**(Un seul échantillon t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(pour toute statistique, aucune hypothèse n'est nécessaire)
   **Bootstrap 置信区间**(volume de calcul, sans prétexte)
5. **A/B test simulator**(générer des données, tester, vérifier les erreurs de type I et de type II)
   **A/B 测试模拟器**(Generation de données, test, inspection de première et deuxième catégories d'erreurs)
6. **Statistical vs practical significance demo**(montrant que le grand n rend tout "signifiant")
   **统计 vs 实际显著性演示**(montrer grand n faire tout "signifiant")

Tout à partir de zéro, en utilisant seulement `math`et `random`Pas de numpy, pas de scipy.

> Toutes les réalisations, seulement utilisation `math`et `random`◊不使用 numpy、scipy。

## Les termes clés
```figure
f3-bootstrap-resample
```

## Les termes clés

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
