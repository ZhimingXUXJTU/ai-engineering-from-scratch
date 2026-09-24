# Probabilité et répartition

> La probabilité est le langage utilisé par l'IA pour exprimer l'incertitude.
> La probabilité est une expression de l'incertitude de l'IA.

**Type:** Learn | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Implémenter des PMF et des PDF à partir de zéro pour les distributions Bernoulli, catégorique, Poisson, uniforme et normale
- Compute la valeur attendue, la variance et utilise le théorème de la limite centrale pour expliquer pourquoi les Gaussiens dominent
- Construire les fonctions softmax et log-softmax avec le truc de stabilité numérique (soustraire max logit)
- Calculer la perte d'entropie croisée des logits et la connecter à la probabilité négative de log

> **【中文解读】**
> 概率 est une IA qui exprime des langues incertaines. 概率 est une sorte de modèle de langue qui génère des images de la distribution apprise à celle de l'apprentissage. 概率 est une expression de la langue de l'incertitude. 概率 est une sorte de modèle de langue qui génère des images de la distribution apprenée à celle de l'apprentissage. 概率 est une sorte de modèle de modèle de la distribution de la probabilité.

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: Transformer la sortie du réseau neuronal en distribution de probabilité est la dernière étape de tous les modèles de classe.
> - **交叉熵损失**: la fonction standard de perte de tâche, égale à négative par nombre de similitudes.
> - **高斯分布**Le centre est très limité pour comprendre pourquoi le gazon est si courant dans la nature et l'IA.

## Le problème , l' introduction du problème

> **【中文解读】**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[0.03, 0.91, 0.06]`(91% 概率是猫), modèle de langue parmi 50.000 candidats choisis, modèle de diffusion parmi les distributions apprises, générant des images 

## Le concept de base.

> **【拓展：概率分布是 AI 生成模型的基础】**Le cœur du modèle de développement (VAE, GAN, diffusion) est la distribution de probabilité: apprendre une distribution de données p (x), puis de la même manière générer de nouvelles données.

Chaque prédiction qu'un modèle fait est une distribution de probabilité. Chaque fonction de perte mesure à quelle distance la distribution prévue est de la vraie. Chaque étape de formation ajuste les paramètres pour que une distribution ressemble davantage à une autre. Sans probabilité, vous ne pouvez pas lire un seul document ML, déboguer un seul modèle ou comprendre pourquoi votre perte de formation est NaN.

> Chaque prédiction du modèle est une distribution de probabilité. Chaque fonction de perte mesure la différence entre la distribution de prédiction et la réelle distribution. Chaque étape de l'entraînement est en train de régler les paramètres pour rapprocher une distribution de l'autre.

## Le concept de base.

### Les événements, les espaces d'échantillonnage et la probabilité

L'espace échantillon S est l'ensemble de tous les résultats possibles. Un événement est un sous-ensemble de l'espace échantillon.

> 样本空间 S est le ensemble de tous les résultats possibles. 事件是样本空间的子集.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Trois axiomes définissent toute probabilité:
1. P(A) >= 0 pour tout événement A
2. P(S) = 1 (quelque chose se passe toujours)
3. P(A ou B) = P(A) + P(B) lorsque A et B ne peuvent pas se produire les deux

> 概率论由三条公理定义:
> 1. 对于任意事件 A,P(A) >= 0
> 2. P (S) = 1 (Il doit y avoir un résultat)
> 3. Quand A et B ne peuvent pas se produire simultanément, P(A ou B) = P(A) + P(B)

Tout le reste (théorème de Bayes, attentes, distributions) découle de ces trois règles.

> Tout ce qui est en train d'être fait est en train d'être fait par ces trois règles.

### Probabilité conditionnelle et indépendance

P ((A) est la probabilité de A étant donné que B est arrivé.

> P  A  B) est la probabilité qu'une évolution se produise dans des conditions où B  a déjà eu lieu.

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

Deux événements sont indépendants quand le fait de connaître l' un ne vous dit rien de l' autre:

> Deux événements indépendants signifient savoir que l'un ne vous dira rien de l'autre:

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

Les pièces de monnaie sont indépendantes, les cartes sans remplacement ne le sont pas.

> La mise en pièces est indépendante.

### Les fonctions de masse de probabilité par rapport aux fonctions de densité de probabilité

Les variables aléatoires discrètes ont une fonction de masse de probabilité (PMF). Chaque résultat a une probabilité spécifique que vous pouvez lire directement.

> 离散随机变量有概率质量函数 (PMF) ⋅ chaque résultat a une probabilité spécifique qui peut être directement lue ⋅

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

Les variables aléatoires continues ont une fonction de densité de probabilité (PDF). La densité à un seul point n'est pas une probabilité.

> 连续随机变量有概率密度函数 (PDF) ⋅ la densité d'un point unique n'est pas une probabilité, la probabilité provient de la densité de la fonction dans une zone spécifique.

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

Cette distinction est importante dans les ML. Les sorties de classification sont des PMF (choix discrètes).

> Cette différence est importante dans le ML.

### Distributions communes

**Bernoulli:**Un essai, deux résultats, des modèles de classification binaire.

> **伯努利分布：**Une expérience, deux résultats.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**Les modèles sont classés en plusieurs classes (sortie de softmax).

> **分类分布：**Une expérience, un résultat de la sorte.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**Il est utilisé pour initialiser au hasard.

> **均匀分布：**Les résultats sont généralement utilisés pour la démarrage.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**La courbe de cloche est paramétrisée par la moyenne (mu) et la variance (sigma^2).

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**Les modèles de taux d'événements sont les suivants:

> **泊松分布：**Cote des incidents rares dans les zones fixes.

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### La valeur attendue et la variation

La valeur attendue est le résultat moyen pondéré.

> L'espérance est un résultat moyen de la valeur ajoutée.

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Les mesures de variance sont réparties autour de la moyenne.

> La différence de mesure du degré de dispersion autour de la valeur moyenne.

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

Dans ML, la valeur attendue apparaît comme la fonction de perte (perte moyenne sur la distribution des données).

> Dans le ML, la valeur attendue est exprimée en fonction de perte de données (la perte moyenne de la distribution de données), le décalage indique la stabilité du modèle.

### Distributions communes et marginales

Une distribution commune P ((X, Y) décrit deux variables aléatoires ensemble.

> 联合分布 P(X, Y)   描述两个 variables qui se produisent simultanément.

Exemple de PMF commun (X = temps, Y = parapluie):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

La distribution marginale résume l'autre variable:

>  marginalisation par rapport à une autre variable

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

Les totaux de la rangée et de la colonne figurant dans le tableau ci-dessus sont les marges.

> Les échanges et les échanges sont les plus importants.

### Pourquoi la distribution normale est partout présente

Le théorème de la limite centrale: la somme (ou la moyenne) de nombreuses variables aléatoires indépendantes converge à une distribution normale, indépendamment de la distribution originale.

> Le nombre de variables indépendantes et les taux de réception à la distribution normale, quelle que soit la distribution initiale.

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

C'est pour ça que:
- Les erreurs de mesure sont approximativement normales (plusieurs petites sources indépendantes)
  Traduction anglaise: mesure d'erreur approximative (en anglais: measure error approximation correct)
- Les initialisations de poids dans les réseaux neuraux utilisent des distributions normales
  Traduction anglaise: Création de la distribution normale du pouvoir de la toile
- Le bruit de gradient dans le SGD est approximativement normal (summe de nombreux gradients d'échantillon)
  Le bruit de la température moyenne est proche du normal.
- La distribution normale est la distribution d'entropie maximale pour une moyenne et une variance données
  Traduction chinoise: répartition normale est la distribution la plus large de la valeur moyenne et de la différence de la distance.

### Probabilités de log

Les probabilités brute causent des problèmes numériques. Multiplier de nombreuses petites probabilités ensemble diminue rapidement à zéro.

> La probabilité initiale entraîne des problèmes de valeur numérique.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

Les probabilités de logs corrigent cela.

> Pour le nombre de probabilités, le problème est résolu.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Règles:
- log(a * b) = log(a) + log(b)
- Les probabilités de log sont toujours <= 0 (puisque 0 < P <= 1)
- Plus négatif = moins probable
- La perte de l'entropie croisée est la probabilité de log négatif de la classe correcte

> Règles:
> - log(a * b) = log(a) + log(b)
> - Pour le nombre de probabilités, le taux de probabilité est de 0 = 0 parce que 0 < P < = 1)
> - 越负 = 越不可能
> - Le risque de perte est le taux de négation de la classe correcte

### Softmax comme répartition de probabilité

Les réseaux neuronaux produisent des scores bruts (logits). Softmax les convertit en une distribution de probabilité valide.

> Le nombre de loges est de 0,9%.

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

Le truc de softmax: soustraire la logite max avant d'exposer pour éviter le débordement.

> Softmax 技巧: avant de réduire le maximum de logit, prévenir le débordement

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax combine softmax et log pour la stabilité numérique. PyTorch utilise cela en interne pour la perte d'entropie croisée.

> Log-softmax va utiliser le softmax et log 合并 pour maintenir la stabilité numérique.

### Prise d'échantillons

Prise d'échantillons: extraction de valeurs aléatoires à partir d'une distribution.
- Jetez des échantillons aléatoires qui ne sont pas des neurones
  Le déploiement décide de quelles sont les positions de la position de zéro
- Des échantillons d'augmentation des données transformations aléatoires
  Le changement de données
- Modèles de langage échantillonnent le prochain jeton de la distribution prévue
  Le modèle de langage de prédiction
- Modèles de diffusion échantillonnent le bruit et dénoncent progressivement
  Le modèle de diffusion du bruit et de la diffusion du bruit

L'échantillonnage à partir de distributions arbitraires nécessite des techniques telles que l'échantillonnage de transformation inverse, l'échantillonnage de rejet ou le truc de réparamétrisation (utilisé dans les VAE).

> De la distribution arbitraire dans le stockage nécessite une inversion de la variation dans le stockage, refus de stockage ou de la réparation techniques (VAE usage) etc.

## Construisez-le et mettez-le en œuvre.
```figure
gaussian-pdf
```

## Faites-le

### Étape 1: Les bases de probabilité

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

### Étape 2: PMF et PDF à partir de zéro

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

### Étape 3: Value et variance attendues

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

### Étape 4: Prise d'échantillons à partir de distributions

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

### Étape 5: Softmax et probabilités de log

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

### Étape 6: démonstration du théorème des limites centrales

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### Étape 7: Visualisation

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Des mises en œuvre complètes avec toutes les visualisations sont en `code/probability.py`- Je suis désolé .

> incluant la réalisation complète de tout ce qui est visible `code/probability.py`Il y a une autre.

## Utilisez-le avec le cadre de réalisation

Avec NumPy et SciPy, tout ce qui est en haut est un-liners:

> Utilisez NumPy et SciPy, toutes les fonctionnalités ci-dessus nécessitent une ligne de code:

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

Vous avez construit ça à partir de zéro, maintenant vous savez ce que font les appels de la bibliothèque.

> Tu as construit ces choses depuis le zéro. Maintenant tu sais ce que font les fonctions de la bibliothèque.

## Les exercices

1. Implémenter l'échantillonnage inverse de transformation pour la distribution exponentielle. Vérifiez en prélèvant des échantillons de 10 000 valeurs et en comparant l'histogramme au vrai PDF.

2. Construisez une table de répartition commune pour deux dés chargés, comptez les répartitions marginales et vérifiez si les dés sont indépendants.

3. Calculer la perte d' entropie croisée pour un classificateur de 5 classes qui produit des logits `[2.0, 0.5, -1.0, 3.0, 0.1]`Lorsque la classe correcte est l'indice 3. Puis vérifiez votre réponse avec PyTorch `nn.CrossEntropyLoss`- Je suis désolé .

4. Écrivez une fonction qui prend une liste de probabilités de log et renvoie la séquence la plus probable, la probabilité totale de log et la probabilité brute équivalente. Testez-la avec une phrase de 50 mots où chaque mot a une probabilité de 0,01.

## Les termes clés

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

## Encore une lecture

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- preuve visuelle de la raison pour laquelle les moyennes deviennent normales
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- une référence concise couvrant tout ici et plus encore
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- pourquoi la stabilité numérique est importante et comment y parvenir
