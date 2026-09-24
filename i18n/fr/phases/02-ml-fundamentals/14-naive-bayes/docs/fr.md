# Bayes naïf
# 朴素贝叶斯


> L'hypothèse naïve est fausse, et elle fonctionne quand même.

> L'hypothèse de "pure" est fausse, mais elle est toujours utilisable.

**Type:** Build | **类型：** 构建
**Language:**Je suis un Python .**语言：**Python
**Prerequisites:** Phase 2, Lessons 01-07 (classification, Bayes' theorem) | **前置知识：** Phase 2 第 1-7 课（分类、贝叶斯定理）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## Objectifs d'apprentissage

- Implémenter des Bayes naïfs multinomiels à partir de zéro avec le lissage Laplace pour la classification du texte
  De zéro à zéro avec Laplace plates de multiples formes simples utilisées dans les classes de texte
- Expliquez pourquoi l'hypothèse naïve d'indépendance est mathématiquement erronée mais produit des classements de classe corrects dans la pratique.
  Expliquer pourquoi la simple hypothèse d'indépendance est mathématiquement erronée mais produit une classification de catégories correcte dans la pratique
- Comparez les variantes de Bayes naïves multinomial, bernoulli et gaussienne et sélectionnez la bonne pour un type de fonctionnalité donné
  Comparer les variantes polyvalentes, Bernoulli et Highly Simple Bayes, pour déterminer le type de variante choisie correctement
- Évaluer les naïfs Bayes contre la régression logistique sur les données rares de haute dimension et expliquer le compromis de biais-variance au travail
  Dans les données de haute qualité, évaluer la simplicité de la base et le retour logique, expliquer le poids des différences


> **【中文解读】**
> Le concept de l'indépendance est très simple, mais il est très simple de le faire.

> **【拓展：朴素贝叶斯在垃圾邮件过滤和情感分析中的应用】**
> Les premiers filtres de spam comme SpamAssassin utilisent beaucoup de simple Bayes, car il a des centaines de milliers de mots, mais il est très peu utilisé dans les scènes de formation.

## Le problème , l' introduction du problème

Vous devez classer le texte. Les e-mails en spam ou non-spam. Les avis des clients en positifs ou négatifs. Les billets de support en catégories. Vous avez des milliers de fonctionnalités (une par mot) et des données de formation limitées.

> Vous devez diviser le texte en catégories. Les messages sont divisés en messages ordinaires ou non ordinaires. Les commentaires des clients sont divisés en catégories positives ou négatives.

La plupart des classifiateurs s'étouffent ici. La régression logistique a besoin de suffisamment d'échantillons pour estimer des milliers de poids de manière fiable. Les arbres de décision se divisent sur un mot à la fois et s'adaptent de manière sauvage. KNN en 10 000 dimensions est sans sens car chaque point est également éloigné de tous les autres points.

> La plupart des classificateurs ici sont en train de vivre. La rentrée logique nécessite une estimation fiable de milliers de poids.

Bayes naïf s'occupe de ça. Il fait une hypothèse mathématiquement erronée (que chaque fonctionnalité est indépendante de toutes les autres fonctionnalités données dans la classe), et il surpasse toujours les modèles "smarts" sur la classification des textes, en particulier avec de petits ensembles de formation. Il traîne en une seule fois les données. Il est à l'échelle de millions de caractéristiques. Il produit des estimations de probabilité (bien que souvent mal calibrées en raison de l'hypothèse d'indépendance).

> Il a fait une hypothèse mathématiquement erronée, mais il est toujours meilleur que le modèle "plus intelligent" dans les classes de texte, en particulier dans les petits groupes d'entraînement. Il ne faut qu'une fois passer par les données pour pouvoir s'entraîner. Il s'étend à des millions de caractéristiques. Il génère des estimations de probabilité.

Comprendre pourquoi une supposition erronée conduit à de bonnes prédictions vous apprend quelque chose de fondamental sur l'apprentissage automatique: le meilleur modèle n'est pas le plus correct, c'est celui qui a le meilleur compromis de variance de biais pour vos données.

> Comprendre pourquoi les hypothèses erronées peuvent générer de bonnes prédictions vous enseigne certaines choses fondamentales de votre apprentissage automatique: le meilleur modèle n'est pas le modèle le plus exact, mais le meilleur modèle pour mesurer les différences de données.

> **【中文解读】**
> La "pure" de Bayes consiste à supposer que toutes les caractéristiques sont indépendantes les unes des autres dans une catégorie donnée. Ce qui est presque inexistant dans la réalité (comme "gratuit" et "avantage" dans les e-mails de déchets). Mais pourquoi peut-il être utilisé ? Parce que les catégories ne nécessitent que la classification correcte des probabilités des catégories, pas besoin de la valeur de probabilité précise.

## Le concept de base.

### Théorème de Bayes (révision rapide)

Le théorème de Bayes renverse les probabilités conditionnelles:

> 贝叶斯定理翻转条件概率:

```
P(class | features) = P(features | class) * P(class) / P(features)
```

Nous voulons`P(class | features)`-- la probabilité qu'un document appartient à une classe compte tenu des mots qui y sont.
- `P(features | class)`-- la probabilité de voir ces mots dans des documents de cette classe
  `P(features | class)`- Dans ce genre de documents, voir ces mots semblent
- `P(class)`-- la probabilité antérieure de la classe (combien de spam est commun en général?)
  `P(class)`-- 类别的先验概率(垃圾邮件通常有多常见?)
- `P(features)`- les preuves, les mêmes pour toutes les classes, afin que nous puissions l'ignorer lors de la comparaison
  `P(features)`-- 证据, à tous les types identiques, peut être ignoré lors de la comparaison

La classe avec le plus haut .`P(class | features)`Il gagne.

> `P(class | features)`La meilleure classe à gagner.

### La supposition naïve de l'indépendance

L' informatique `P(features | class)`Il faut calculer la probabilité commune de toutes les caractéristiques ensemble. avec un vocabulaire de 10 000 mots, vous devriez estimer une distribution sur 2^10 000 combinaisons possibles.

> 精确计算 `P(features | class)`Pour une liste de 10 000 mots, vous devez estimer la distribution de 2 à 10 000 variétés possibles.

L'hypothèse naïve: chaque caractéristique est conditionnellement indépendante compte tenu de la classe.

> 朴素假设:给定类别下每个特征条件独立――

```
P(w1, w2, ..., wn | class) = P(w1 | class) * P(w2 | class) * ... * P(wn | class)
```

Au lieu d'une distribution commune impossible, vous estimez n distributions simples par fonction.

> Vous n'avez pas besoin d'estimer une distribution commune impossible, mais d'estimer n'importe quelle simple distribution par caractéristique.

Cette hypothèse est évidemment fausse. Les mots "machine" et "apprentissage" ne sont indépendants dans aucun document. Mais le classifiant n'a pas besoin d'estimations de probabilité correctes. Il a besoin de classements corrects - quelle classe a la plus grande probabilité. L'hypothèse d'indépendance introduit des erreurs systématiques, mais ces erreurs affectent toutes les classes de manière similaire, de sorte que le classement reste correct.

> Cette hypothèse est évidemment erronée. La "machine" et le "apprentissage" ne sont pas indépendants dans aucun document. Mais les classifications ne nécessitent pas d'estimation de probabilité correcte.

### Pourquoi il fonctionne encore

Trois raisons:

> Trois raisons:

1. **Ranking over calibration.**La classification ne nécessite que la classe la plus haut classée pour être correcte. Même si P(spam) = 0,99999 lorsque la vraie probabilité est de 0,7, le classifiant choisit toujours correctement le spam. Nous n'avons pas besoin de probabilités correctes. Nous avons besoin du gagnant correct.
   **排名优于校准。**Même si le P(spam) = 0,99999 alors que la vraie probabilité est de 0,7, le classifiant reste toujours correct pour choisir le spam.

2. **High bias, low variance.**L'hypothèse d'indépendance est un précédent fort. Elle restreint fortement le modèle, ce qui empêche le surpassage. Avec des données de formation limitées, un modèle légèrement erroné mais stable bat un modèle théoriquement correct mais extrêmement instable.
   **高偏差、低方差。**L'hypothèse d'indépendance est une forte préoccupation. Elle est un modèle très limité, empêchant de trop se comporter.

3. **Feature redundancy cancels out.**Les caractéristiques corrélatives fournissent des preuves redondantes. Le classifiant compte ces preuves à double, mais il les compte à double pour la classe correcte aussi. Si "machine" et "apprentissage" apparaissent toujours ensemble, les deux fournissent des preuves pour la classe "tech". NB les compte deux fois, mais il les compte deux fois pour la classe correcte.
   **特征冗余相互抵消。**相关特征提供冗余证据――分类重复计数 这些证据,但正确类别的证据也被重复计数――如果"机器"和"学习"总是出现一次,两者都为"技术"类提供证据――简单贝叶斯数两次,但为正确类别的证据两次――

Une quatrième raison pratique: Naïf Bayes est extrêmement rapide. La formation est un seul passage à travers les fréquences de comptage des données. La prédiction est une multiplication de matrice. Vous pouvez vous entraîner sur un million de documents en quelques secondes. Cette vitesse signifie que vous pouvez iterer plus rapidement, essayer plus de fonctionnalités et exécuter plus d'expériences que avec des modèles plus lents.

> La quatrième raison réelle: Simple Bayes est très rapide. L'entraînement est une fréquence de calcul de données simple. La prédiction est une multiplication de matrices. Vous pouvez entraîner un million de documents en quelques secondes. Cette vitesse signifie que vous pouvez essayer plus de caractéristiques, faire plus d'expériences que d'utiliser des modèles plus lents.

### Les mathématiques étape par étape

Prenons un exemple concret: supposons que nous ayons deux classes: spam et non-spam. Notre vocabulaire a trois mots: "gratuit", "argent", "réunion".

Données de formation:
- Les e-mails de spam mentionnent "gratuit" 80 fois, "argent" 60 fois, "réunion" 10 fois (150 mots au total)
- Les e-mails non-spam mentionnent "gratuit" 5 fois, "argent" 10 fois, "réunion" 100 fois (115 mots au total)
- 40% des e-mails sont des spams, 60% ne sont pas des spams

Avec le lissage Laplace (alpha=1):

```
P(free | spam)    = (80 + 1) / (150 + 3) = 81/153 = 0.529
P(money | spam)   = (60 + 1) / (150 + 3) = 61/153 = 0.399
P(meeting | spam) = (10 + 1) / (150 + 3) = 11/153 = 0.072

P(free | not-spam)    = (5 + 1) / (115 + 3) = 6/118 = 0.051
P(money | not-spam)   = (10 + 1) / (115 + 3) = 11/118 = 0.093
P(meeting | not-spam) = (100 + 1) / (115 + 3) = 101/118 = 0.856
```

Le nouveau courriel contient: "gratuit" (2 fois), "argent" (1 fois), "réunion" (0 fois).

```
log P(spam | email) = log(0.4) + 2*log(0.529) + 1*log(0.399) + 0*log(0.072)
                    = -0.916 + 2*(-0.637) + (-0.919) + 0
                    = -3.109

log P(not-spam | email) = log(0.6) + 2*log(0.051) + 1*log(0.093) + 0*log(0.856)
                        = -0.511 + 2*(-2.976) + (-2.375) + 0
                        = -8.838
```

Le mot "gratuit" apparaissant deux fois est une preuve forte du spam. Notez que "réunion" ne apparaissant pas contribue à zéro à les deux log sumes (0 * log(P)) - dans le NB multivarié, les mots absents n'ont aucun effet. C'est Bernoulli NB qui modélise explicitement l'absence de mots.

### Trois variantes

Bayes naïf est disponible en trois saveurs.`P(feature | class)`- C'est différent.

> Il y a trois variantes.`P(feature | class)`Il y a une autre façon de construire.

#### Bayes naïf à plusieurs noms

Modèles de chaque fonctionnalité comme un compte. Il est préférable pour les données de texte où les caractéristiques sont des fréquences de mots ou des valeurs TF-IDF.

> Pour chaque caractéristique, le plus approprié est le texte de la valeur de la fréquence ou du TF-IDF.

```
P(word_i | class) = (count of word_i in class + alpha) / (total words in class + alpha * vocab_size)
```

Le `alpha`est le lissage Laplace (expliqué ci-dessous).

> `alpha`Il est le premier à avoir été créé par le Père Noël.

#### Bayes naïf gaussien

Modèle de chaque fonctionnalité comme une distribution normale.

> Mettre chaque caractéristique en forme de répartition normale.

```
P(x_i | class) = (1 / sqrt(2 * pi * var)) * exp(-(x_i - mean)^2 / (2 * var))
```

Chaque classe a sa propre moyenne et sa propre variance par fonctionnalité. Cela fonctionne bien lorsque les fonctionnalités suivent réellement une courbe de cloche au sein de chaque classe.

> Chaque catégorie a sa propre valeur moyenne et sa différence avec chaque caractéristique.

#### Bernoulli naïf Bayes

Modèles de chaque fonctionnalité comme binaire (présent ou absent).

> Pour chaque caractéristique, mettre en valeur deuxièmes (apparente ou non)

```
P(word_i | class) = (docs in class containing word_i + alpha) / (total docs in class + 2 * alpha)
```

Contrairement à Multinomial, Bernoulli pénalise explicitement l'absence d'un mot. Si "libre" apparaît généralement dans le spam mais est absent de cet e-mail, Bernoulli le compte comme preuve contre le spam.

> Contrairement à de nombreux autres, Bernard définit le terme punition comme étant absent. Si "libre" apparaît généralement dans le spam mais que ce mail ne soit pas disponible, Bernard considère cela comme une preuve de l'opposition au spam.

### Quand utiliser chaque variante

| Variant | Feature Type | Best For | Example |
|---------|-------------|----------|---------|
| Multinomial | Counts or frequencies | Text classification, bag-of-words | Email spam, topic classification |
| Gaussian | Continuous values | Tabular data with normal-ish features | Iris classification, sensor data |
| Bernoulli | Binary (0/1) | Short text, binary feature vectors | SMS spam, presence/absence features |

| 变体 | 特征类型 | 最适合 | 示例 |
|------|---------|--------|------|
| Multinomial | 计数或频率 | 文本分类、词袋 | 邮件垃圾过滤、主题分类 |
| Gaussian | 连续值 | 近正态的表格数据 | 鸢尾花分类、传感器数据 |
| Bernoulli | 二值（0/1） | 短文本、二值特征向量 | 短信垃圾过滤、出现/缺失特征 |

### Légimentation de la place

Que se passe-t-il lorsqu'un mot apparaît dans les données d'essai mais n'apparaît jamais dans les données de formation pour une classe particulière?

> Si un mot apparaît dans les données de test, mais ne apparaît jamais dans les données d'entraînement d'une catégorie, que se passe-t-il ?

Sans lissage:`P(word | class) = 0/N = 0`Un zéro multiplié par l' ensemble produit fait`P(class | features) = 0`Un seul mot invisible détruit toute la prédiction, peu importe combien d'autres preuves l'appuient.

> Il n'y a pas de décomposition:`P(word | class) = 0/N = 0`◊ Un zéro multiplicateur à l'ensemble du multiplicateur`P(class | features) = 0`Quoi qu'il en soit, les autres preuves ne sont pas suffisantes pour que la parole qu'on n'a pas vue détruise la prédiction.

Le lissage de la laplace ajoute un petit nombre `alpha`(généralement 1) pour chaque nombre de caractéristiques:

> La place est plate à chaque caractéristique et à chaque petit chiffre.`alpha`(habituellement pour 1):

```
P(word_i | class) = (count(word_i, class) + alpha) / (total_words_in_class + alpha * vocab_size)
```

Avec alpha = 1, chaque mot obtient au moins une probabilité minuscule. Le mot "discombobulate" apparaissant dans un e-mail de test ne tue plus la probabilité de spam. Le smoothing a une interprétation bayésienne: il est équivalent à placer un Dirichlet uniforme avant les distributions de mots.

> alpha=1 时, chaque mot obtient au moins une très petite probabilité――"discombobulate" apparaît dans test mail ne plus détruire la probabilité du spam──平滑有贝叶斯解释:等价于在词分布上放一个均 Dirichlet先验──

L'alpha supérieur signifie un raffinement plus fort (distributions plus uniformes).

> L'alpha plus élevé signifie plus fort de la distribution moyenne (en anglais: +) ⋅ plus proche de la distribution moyenne (en anglais: +) ⋅ plus bas signifie plus fidèle au modèle et à la données (en anglais: +).

L'effet de l' alpha:

> L'influence de l'alpha:

| Alpha | Effect | When to use |
|-------|--------|-------------|
| 0.001 | Almost no smoothing, trust the data | Very large training set, no unseen features expected |
| 0.1 | Light smoothing | Large training set |
| 1.0 | Standard Laplace smoothing | Default starting point |
| 10.0 | Heavy smoothing, flattens distributions | Very small training set, many unseen features expected |

| Alpha | 效果 | 使用场景 |
|-------|------|---------|
| 0.001 | 几乎不平滑，相信数据 | 非常大的训练集，预期不会有未见特征 |
| 0.1 | 轻度平滑 | 大训练集 |
| 1.0 | 标准 Laplace 平滑 | 默认起点 |
| 10.0 | 重度平滑，拉平分布 | 非常小的训练集，预期有很多未见特征 |

### Compteur log-espace

Multiplication de centaines de probabilités (chacune inférieure à 1) provoque un sous-flux de point flottant. Le produit devient zéro dans le point flottant même si la valeur réelle est un nombre positif très petit.

> Mettre des centaines de probabilités (à chaque fois inférieure à 1) entraînera une augmentation des points de basse décharge.

La solution: travailler dans l'espace log. Au lieu de multiplier les probabilités, ajoutez leurs logarithmes:

> 解决方案: dans le calcul de l'espace numérique, la probabilité est multipliée par le nombre de facteurs:

```
log P(class | x1, x2, ..., xn) = log P(class) + sum_i log P(xi | class)
```

Cela transforme la prédiction en un produit de point:

> Cette prédiction est devenue un point de départ.

```
log_scores = X @ log_feature_probs.T + log_class_priors
prediction = argmax(log_scores)
```

La multiplication de matrice. C'est pourquoi la prédiction de Bayes naïve est si rapide -- c'est la même opération qu'un modèle linéaire à couche unique.

> C'est la raison pour laquelle la prédiction de Bayes est si rapide.

### Bayes naïf contre la régression logistique

Les deux sont des classifiants linéaires pour le texte.

> Les deux sont des classifiants de texte. La différence réside dans l'objet qu'ils construisent.

| Aspect | Naive Bayes | Logistic Regression |
|--------|------------|-------------------|
| Type | Generative (models P(X\|Y)) | Discriminative (models P(Y\|X)) |
| Training | Count frequencies | Optimize loss function |
| Small data | Better (strong prior helps) | Worse (not enough to estimate weights) |
| Large data | Worse (wrong assumption hurts) | Better (flexible boundary) |
| Features | Assumes independence | Handles correlations |
| Speed | Single pass, very fast | Iterative optimization |
| Calibration | Poor probabilities | Better probabilities |

| 方面 | 朴素贝叶斯 | 逻辑回归 |
|------|----------|---------|
| 类型 | 生成式（建模 P(X\|Y)） | 判别式（建模 P(Y\|X)） |
| 训练 | 统计频率 | 优化损失函数 |
| 小数据 | 更好（强先验有帮助） | 更差（数据不足以估计权重） |
| 大数据 | 更差（错误假设有害） | 更好（灵活边界） |
| 特征 | 假设独立 | 能处理相关性 |
| 速度 | 单次遍历，极快 | 迭代优化 |
| 校准 | 概率校准差 | 概率校准更好 |

Règle générale: commencez par Naive Bayes. Si vous avez assez de données et des plateaux NB, passez à la régression logistique.

> 经验法则: First use simple贝叶斯──如果数据足够且NB 性能停滞,换逻辑回归──

### L'équipement de transport

```mermaid
flowchart LR
    A[Raw Text] --> B[Tokenize]
    B --> C[Build Vocabulary]
    C --> D[Count Word Frequencies]
    D --> E[Apply Smoothing]
    E --> F[Compute Log Probabilities]
    F --> G[Predict: argmax P class given words]

    style A fill:#f9f,stroke:#333
    style G fill:#9f9,stroke:#333
```

En pratique, nous travaillons dans l'espace log pour éviter le sous-flux des points flottants. Au lieu de multiplier de nombreuses petites probabilités, nous ajoutons leurs logarithmes:

```
log P(class | features) = log P(class) + sum_i log P(feature_i | class)
```

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**
> De la réalisation de la plupart des langages simples (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriodiode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la plupart des langages (pluriode) à la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de

> **【拓展：朴素贝叶斯在现代 NLP 中的角色演变】**
> Bien que le Transformer 模型 (BERT、GPT) dépasse considérablement la simple Bayès dans la tâche de la PNL, la simple Bayès a encore son utilité: réel temps de spammail (très) 毫秒级延迟) 、大规模文本预分类 (extrêmement faible) 、 comme référence 快速验证特征工程效果── dans le diagnostic médical, la haute probabilité de sortie est expliquée et largement utilisée  Les médecins doivent savoir "qu'il y a beaucoup de savoir", plutôt que de sortir dans la boîte noire.
```figure
naive-bayes
```

## Faites-le

Le code dans `code/naive_bayes.py`Il implémentera à la fois MultinomialNB et GaussianNB à partir de zéro.

### Nombre de noms

La mise en œuvre à partir de zéro:

1. **fit(X, y)**Pour chaque classe, comptez la fréquence de chaque fonctionnalité. Ajoutez le lissage Laplace. Comptez les probabilités de journaux. Réservez les prérogatives de classe (journaux de fréquences de classe).

2. **predict_log_proba(X)**Pour chaque échantillon, calculer le log P(class) + la somme du log P(feature_i==class) pour toutes les classes.

3. **predict(X)**: Retournez la classe avec la plus grande probabilité de log.

```python
class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        classes = np.unique(y)
        n_classes = len(classes)
        n_features = X.shape[1]

        self.classes_ = classes
        self.class_log_prior_ = np.zeros(n_classes)
        self.feature_log_prob_ = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.class_log_prior_[i] = np.log(X_c.shape[0] / X.shape[0])
            counts = X_c.sum(axis=0) + self.alpha
            self.feature_log_prob_[i] = np.log(counts / counts.sum())

        return self
```

La prédiction est juste une multiplication de matrice plus un biais.

### Gaussie NB

Pour les caractéristiques continues, on estime la moyenne et la variance par classe par caractéristique:

```python
class GaussianNB:
    def __init__(self):
        pass

    def fit(self, X, y):
        classes = np.unique(y)
        self.classes_ = classes
        self.means_ = np.zeros((len(classes), X.shape[1]))
        self.vars_ = np.zeros((len(classes), X.shape[1]))
        self.priors_ = np.zeros(len(classes))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.means_[i] = X_c.mean(axis=0)
            self.vars_[i] = X_c.var(axis=0) + 1e-9
            self.priors_[i] = X_c.shape[0] / X.shape[0]

        return self
```

La prédiction utilise le PDF gaussien par fonctionnalité, multiplié par fonctionnalité (ajouté dans l'espace de journaux).

### Démo: Classification du texte

Le code génère des données de sacs de mots synthétiques simulant deux classes (articles technologiques contre articles sportifs). Chaque classe a une distribution de fréquence de mots différente.

Les données synthétiques fonctionnent comme ceci: nous créons 200 "words" (columnes de fonctionnalités). Les mots 0-39 ont une fréquence élevée dans les articles techniques et faible dans le sport. Les mots 80-119 ont une fréquence élevée dans le sport et faible dans le domaine technique. Les mots 40-79 sont de fréquence moyenne dans les deux. Cela crée un scénario réaliste où certains mots sont des indicateurs de classe forts et d'autres sont du bruit.

### Démo: fonctionnalités continues

Le code génère des données Iris-like (3 classes, 4 caractéristiques, clusters gaussiens). GaussianNB classifie en utilisant la moyenne et la variance par classe. Chaque classe a un centre différent (vecteur moyen) et une diffusion différente (variance), imitant les données du monde réel où les mesures diffèrent systématiquement entre les catégories.

Le code démontre également:
- **Smoothing comparison:**Formation de MultinomialNB avec différentes valeurs alpha pour montrer l'effet de la force de lissage sur la précision.
- **Training size experiment:**Comment la précision de NB s'améliore à mesure que les données de formation passent de 20 à 1600 échantillons. NB atteint une précision décente même avec très peu d'échantillons - c'est son principal avantage.
- **Confusion matrix:**La précision par classe, le rappel et le score de F1 pour montrer où NB fait des erreurs.

### Vite de prédiction

La prédiction naïve de Bayes est une multiplication de matrice. Pour n échantillons avec d caractéristiques et k classes:
- MultinomialNB: une matrice multipliée (n x d) @ (d x k) = O(n * d * k)
- GaussianNB: n * k Évaluations PDF gaussiennes, chacune sur d caractéristiques = O(n * d * k)

Les deux sont linéaires dans toutes les dimensions. Comparer ceci à KNN (qui nécessite le calcul de la distance à tous les points de formation) ou SVM avec le noyau RBF (qui nécessite l'évaluation du noyau contre tous les vecteurs de support). NB est plus rapide par ordre de magnitude au moment de la prédiction.

## Utilisez-le avec le cadre de réalisation

Avec sklearn, les deux variantes sont unlinées:

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
print(f"GaussianNB accuracy: {gnb.score(X_test, y_test):.3f}")

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_counts, y_train)
print(f"MultinomialNB accuracy: {mnb.score(X_test_counts, y_test):.3f}")
```

Pour la classification du texte avec sklearn:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB(alpha=1.0)),
])

text_clf.fit(train_texts, train_labels)
accuracy = text_clf.score(test_texts, test_labels)
```

Le code dans `naive_bayes.py`Comparer les mises en œuvre à partir de zéro avec les données de sklearn sur les mêmes données pour vérifier leur exactitude.

### TF-IDF avec Naive Bayes

Les nombres de mots bruts donnent à chaque mot le même poids par occurrence. Mais les mots communs comme "le" et "est" apparaissent fréquemment dans chaque classe - ils ne contiennent aucune information. TF-IDF (Term Frequency - Inverse Document Frequency) diminue le poids des mots communs et augmente le poids des mots rares et discriminatoires.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB(alpha=0.1)),
])
```

Les valeurs TF-IDF sont non négatives, elles fonctionnent donc avec MultinomialNB. La combinaison de TF-IDF + MultinomialNB est l'une des lignes de base les plus fortes pour la classification du texte.

### BernoulliNB pour texte court

Pour le texte court (tweets, SMS, messages de chat), BernoulliNB peut surpasser MultinomialNB. Les textes courts ont un faible nombre de mots, de sorte que les informations de fréquence sur lesquelles MultinomialNB s'appuie sont bruyantes.

```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

text_clf = Pipeline([
    ("vectorizer", CountVectorizer(binary=True)),
    ("classifier", BernoulliNB(alpha=1.0)),
])
```

Le `binary=True`flag dans CountVectorizer convertit tous les nombres en 0/1. Sans lui, BernoulliNB fonctionne toujours mais voit des nombres pour lesquels il n'a pas été conçu.

### Calibration NB Probabilités

Les probabilités de NB sont mal calibrées. Lorsque NB dit P(spam) = 0,95, la vraie probabilité pourrait être de 0,7. Si vous avez besoin d'estimations de probabilité fiables (par exemple, pour définir un seuil ou combiner avec d'autres modèles), utilisez le CalibratedClassifierCV de sklearn:

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_nb = CalibratedClassifierCV(MultinomialNB(), cv=5, method="sigmoid")
calibrated_nb.fit(X_train, y_train)
proba = calibrated_nb.predict_proba(X_test)
```

Cela correspond à une régression logistique en plus des scores bruts de NB en utilisant la validation croisée.

### Les gotches communes

1. **Negative feature values.**MultinomialNB nécessite des caractéristiques non négatives. Si vous avez des valeurs négatives (comme TF-IDF avec certains paramètres ou caractéristiques standardisées), utilisez GaussianNB à la place, ou changez les caractéristiques pour être positives.

2. **Zero variance features.**Le GaussianNB est divisé par variance. Si une fonction a une variance zéro pour une classe (toutes les valeurs sont identiques), le calcul de probabilité est cassé. Le code ajoute un petit terme de lissage (1e-9) à toutes les variances pour éviter cela.

3. **Class imbalance.**Si 99% des e-mails ne sont pas spam, le P (non-spam) = 0,99 est si fort qu'il dépasse les preuves de probabilité. Vous pouvez définir manuellement les priorités de classe ou utiliser le paramètre class_prior dans sklearn.

4. **Feature scaling.**Le multinomialNB n'a pas besoin d'échelle (il fonctionne sur les calculs). Le GaussianNB n'a pas besoin d'échelle non plus (il estime les statistiques par caractéristique).

## Envoyez-le . Produit .

Cette leçon donne:
- `outputs/skill-naive-bayes-chooser.md`-- une compétence de décision pour choisir la bonne variante NB
- `code/naive_bayes.py`-- MultinomialNB et GaussianNB à partir de zéro, avec une comparaison sklearn

### Quand Bayes échoue

NB échoue lorsque l'hypothèse d'indépendance provoque des classements incorrects (et non seulement des probabilités incorrectes).

1. **Strong feature interactions.**Si la classe dépend de la combinaison de deux caractéristiques mais pas l'une ou l'autre seule (patterns XOR-like), NB la manquera complètement.

2. **Highly correlated features with opposing evidence.**Si la fonction A dit "spam" et la fonction B dit "non-spam", mais A et B sont parfaitement corrélés (ils sont toujours d'accord dans la réalité), NB verra des preuves contradictoires là où il n'y en a pas.

3. **Very large training sets.**Avec suffisamment de données, des modèles discriminatifs tels que la régression logistique apprennent la véritable limite de décision et dépassent NB. L'hypothèse d'indépendance qui a aidé avec de petites données retient maintenant le modèle.

En pratique, ces modes d'échec sont rares pour la classification du texte. Les caractéristiques du texte sont nombreuses, individuellement faibles, et les erreurs de l'hypothèse d'indépendance ont tendance à annuler. Pour les données de tableau avec peu de caractéristiques fortement corrélatives, considérez d'abord la régression logistique ou les modèles basés sur des arbres.

## Les exercices

1. **Smoothing experiment.**Prenez MultinomialNB sur les données de texte avec des valeurs alpha de 0,01, 0,1, 1,0, 10,0 et 100,0.
   1. **平滑实验。**Utilisez l'alpha  valeurs 0.01 、 0.1 、 1.0 、 10.0 、 100.0 dans le texte de données entraînement MultinomialNB ⋅ dessin de la précision de taux vs alpha ⋅ Performance peak Où est ? Pourquoi très élevé alpha ⋅

2. **Feature independence test.**Prenez un ensemble de données de texte réel. Choisissez deux mots qui sont évidemment corrélés ("machine" et "apprentissage"). Comptez P "class word1′′) * P "word2′′) et comparez avec P "word1 AND word2′′ class. Quelle est la erreur de l'hypothèse d'indépendance?
   2. **特征独立性测试。**取一个真文本数据集. 选择两个明显相关词 (如"机器"和"学习") 计算 P (word1 类) * P (word2 类) 并与 P (word1 AND word2 类) 比较. 独立性假设错多少?

3. **Bernoulli implementation.**Extension du code avec une classe BernoulliNB. Convertir les sacs de mots en binaire (présent/absent) et comparer la précision contre MultinomialNB sur les données de texte. Quand Bernoulli gagne-t-il?
   3. **伯努利实现。**扩展代码添加 BernoulliNB 类──将词袋转为二值(存在/不存在)并与多数字数NB 在文本数据上比较准确率──伯努利何时赢?

4. **NB vs Logistic Regression.**Prenez les deux en fonction des données de texte. Commencez par 100 échantillons de formation et augmentez à 10 000.
   4. **NB vs 逻辑回归。**En effet, les deux sont en train de se former sur les données de texte. De 100 échantillons de formation, ils ont commencé à augmenter jusqu'à 10 000.

5. **Spam filter.**Construire un classifiateur de spam complet: jetonner le texte brut du courrier électronique, créer un vocabulaire, créer des fonctionnalités de sacs de mots, former MultinomialNB, évaluer avec précision et rappeler (pas seulement l'exactitude - pourquoi?).
   5. **垃圾邮件过滤器。**构建完整的垃圾邮件分类器:分词原始邮件文本、构建词汇表、创建词袋特征、训练 MultinomialNB、使用精确率和召回率评估──

> **【中文解读】**
> 朴素贝叶斯的三种变体:(1) 多项式朴素贝叶斯(MultinomialNB) 适用于词频/TF-IDF特征文本分类;(2) 伯努利朴素贝叶斯(BernoulliNB) 适用于二值特征(词是否出现);(3) 高斯朴素贝叶斯(GaussianNB) 适用于连续特征,假设每类内特从正态分布而征服――Laplace 平滑加

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Naive Bayes | "Simple probabilistic classifier" | A classifier that applies Bayes' theorem with the assumption that features are conditionally independent given the class |
| Conditional independence | "Features don't affect each other" | P(A, B \| C) = P(A \| C) * P(B \| C) -- knowing B tells you nothing new about A once you know C |
| Laplace smoothing | "Add-one smoothing" | Adding a small count to every feature to prevent zero probabilities from dominating the prediction |
| Prior | "What you believed before seeing data" | P(class) -- the probability of each class before observing any features |
| Likelihood | "How well the data fits" | P(features \| class) -- the probability of observing these features if the class is known |
| Posterior | "What you believe after seeing data" | P(class \| features) -- the updated probability of the class after observing the features |
| Generative model | "Models how data is generated" | A model that learns P(X \| Y) and P(Y), then uses Bayes' theorem to get P(Y \| X) |
| Discriminative model | "Models the decision boundary" | A model that directly learns P(Y \| X) without modeling how X is generated |
| Log probability | "Avoid underflow" | Working with log P instead of P to prevent the product of many small numbers from becoming zero in floating point |

## Encore une lecture

- [scikit-learn Naive Bayes docs](https://scikit-learn.org/stable/modules/naive_bayes.html)-- les trois variantes avec des détails mathématiques
  [scikit-learn 朴素贝叶斯文档](https://scikit-learn.org/stable/modules/naive_bayes.html)- 3 types de variables et détails mathématiques
- [McCallum and Nigam, A Comparison of Event Models for Naive Bayes Text Classification (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)-- la comparaison classique de Multinomial vs Bernoulli pour le texte
  [McCallum and Nigam (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)- Comparison des classiques
- [Rennie et al., Tackling the Poor Assumptions of Naive Bayes Text Classifiers (2003)](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf)-- améliorations de la note pour le texte
  [Ng and Jordan (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)- provable NB dans peu de données
- [Ng and Jordan, On Discriminative vs. Generative Classifiers (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)-- prouve que la NB converge plus rapidement que la LR avec moins de données
