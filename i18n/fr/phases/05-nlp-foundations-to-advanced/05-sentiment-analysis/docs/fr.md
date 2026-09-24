# Analyse des sentiments

> La plupart de ce que vous devez savoir sur la classification classique du texte apparaît ici.
> La plupart des choses que vous devez savoir sont ici.

> **【中文解读】**Le jugement des émotions du texte est l'une des tâches classiques de la PNL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

"La nourriture n'était pas bonne". Positive ou négative?

> "La nourriture n'était pas bonne".

Le sentiment semble simple. Un critique a dit qu'il aimait ou n'aimait pas quelque chose. Étiquettez la phrase. La raison pour laquelle elle est devenue la tâche canonique de la PNL est que chaque cas facile à regarder cache un cas difficile. La négation renverse le sens. Le sarcasme le renverse. " Pas du tout mauvais " est positif malgré deux mots codés négatifs.`tight`dans la revue musicale versus `tight`dans la revue de la mode).

> L'analyse émotionnelle semble simple. Les commentateurs ont dit qu'il y a du plaisir ou du désintérêt. Elle est devenue une tâche classique de la PNL, car chaque cas semble simple, derrière chaque cas, est caché un cas difficile.`tight`Avec le temps dans les commentaires`tight`)。

Si vous comprenez pourquoi chaque ligne de base naïve a un mode d'échec spécifique, vous comprenez pourquoi chaque modèle riche a été inventé. Cette leçon construit une ligne de base naïve Bayes à partir de zéro, ajoute la régression logistique et nomme les pièges qui font du sentiment de production un problème de conformité.

> L'analyse émotionnelle est le laboratoire classique de la PNL. Si vous comprenez pourquoi chaque ligne simple a un modèle de défaillance spécifique, vous comprenez pourquoi chaque modèle plus riche a été inventé.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

Le sentiment classique est une recette en deux étapes.

> L'analyse émotionnelle classique est un schéma en deux étapes.

1. **Represent.**Transformer le texte en vecteur de fonctionnalités.
   **表示。**Pour les autres, il est nécessaire de modifier le texte en utilisant le texte de la page d'accueil.
2. **Classify.**Adaptation d'un modèle linéaire (Naive Bayes, régression logistique, SVM) sur des exemples étiquetés.
   **分类。**Dans le cadre de la mise en œuvre de la loi sur les droits de l'homme, le projet de loi sur les droits de l'homme est adopté par le Conseil de la Justice.

Bayes est le modèle le plus stupide qui fonctionne.`P(word | positive)`et `P(word | negative)`En effet, les résultats sont étonnamment forts: avec des caractéristiques de texte rares et des données modérées, le classifiateur se soucie de savoir de quel côté chaque mot se penche plutôt que de combien.

> Le modèle de la simplicité de Béries est le plus simple mais le plus efficace.`P(word | positive)`et `P(word | negative)`◊ Le raisonnement va augmenter la probabilité. Le principe d'indépendance de "pure" est ridicule, mais les résultats sont étonnants.

La régression logistique corrige l'hypothèse d'indépendance. Elle apprend un poids par caractéristique, y compris des poids négatifs. `not good`Bayes naïf ne peut pas faire cela pour des bigrammes qu'il n'a jamais étiquetés.

> 逻辑归修复了独立性假设──it est utilisé pour chaque caractéristique de l'apprentissage d'un pouvoir, y compris le pouvoir négatif──`not good` comme caractéristique du second groupe pour obtenir un poids négatif

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
sentiment-logits
```

## Faites-le

### Étape 1: un véritable mini-ensemble de données

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

Le travail réel utilise des dizaines de milliers d'exemples (IMDb, SST-2, polarité Yelp).

> Il y a aussi des milliers de modèles de mathématiques qui sont identiques.

### Étape 2: Naïve Bayes multinomial à partir de zéro

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

Le smoothing additif (alpha=1.0) est le smoothing Laplace. Sans lui, un mot invisible dans une classe a une probabilité de zéro et le log explose. `alpha=0.01`est commun dans la pratique. `alpha=1.0`est le défaut d'enseignement.

> 加法平滑(alpha=1.0) est un langage qui est un langage qui ne se trouve pas dans la catégorie.`alpha=0.01`Je le vois souvent.`alpha=1.0`Il est la valeur de l'enseignement.

### Étape 3: régression logistique à partir de zéro

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

La régularisation de l'L2 est importante ici. Les caractéristiques du texte sont rares; sans L2 le modèle mémorise des exemples de formation.`0.01`et à la musique.

> L2 est très important dans ce domaine. Les caractéristiques du texte sont rares; aucun modèle L2 ne se souviendra de l'exemple de formation.`0.01`- Je suis en train de faire des modifications.

### Étape 4: négation de la manutention (mode défaillance)

Considérez "pas bon" et "pas mal".`{not, good}`et `{not, bad}`Il apprend de qui il est le plus présent.`not_good`et `not_bad`Il est donc nécessaire de les apprendre comme caractéristiques distinctes.

> Je pense que c'est pas bon et pas mal.`{not, good}`et `{not, bad}`En fonction de l'entraînement qui apparaît plus à apprendre.`not_good`et `not_bad`作为不同特征学习──, cela est généralement suffisant──.

Un remède plus brut qui fonctionne quand on n' a pas de bigrammes:**negation scoping**. Préfixe des jetons suivant un mot de négation avec `NOT_`jusqu'à la prochaine ponctuation.

> Une réparation plus grossière mais efficace en l'absence de deux composés:**否定范围标记**                                                                                                                                                                                                                                                              `NOT_`Avant, jusqu'à la dernière étiquette.

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

- Je suis désolé .`good`et `NOT_good`Les trois lignes de pré-traitement, de précision mesurable, sautent sur les benchmarks de sentiment.

> Je suis là.`good`et `NOT_good`Les différents types de traitement sont différents. Les classificateurs peuvent leur donner un poids inverse.

### Étape 5: les mesures d'évaluation qui comptent

La précision seule est trompeuse si les classes sont déséquilibrées. Les vrais sentiments corporels sont généralement de 70-80% positifs ou de 70-80% négatifs; un classificateur à majorité constante obtient une précision de 80% et est sans valeur.

> Si les catégories sont déséquilibrées, le taux de précision ne peut être qu'équivoque. Les expressions de réalisme sont généralement positives de 70 à 80% ou négatives de 70 à 80%.

- **Per-class precision and recall.**Une paire par classe, et une moyenne macro pour obtenir un seul nombre qui respecte l'équilibre de classe.
  **每类精确率和召回率。**Chaque classe est un par. Les grandes moyennes obtiennent un nombre unique de l'équilibre de classe.
- **Macro-F1 (primary metric for imbalanced data).**La moyenne des scores par classe, avec le même poids.
  **Macro-F1（不平衡数据的主要指标）。**La valeur moyenne des fractions F1 est égale au poids.
- **Weighted-F1 (alternative).**Rapporte avec la macro-F1 lorsque le déséquilibre lui-même a une signification commerciale.
  **Weighted-F1（替代方案）。**En effet, les données de l'analyse de la situation actuelle sont généralement des données de référence.
- **Confusion matrix.**Il faut toujours vérifier avant de faire confiance à une métrique scalaire, elle révèle quel couple de classes le modèle confond.
  **混淆矩阵。**Le premier chiffre est le nombre de catégories de données de référence.
- **Per-class error samples.**Tirez 5 erreurs de prédiction par classe. Lisez-les. Rien ne remplace la lecture des erreurs réelles.
  **每类错误样本。**Chaque catégorie tire 5 erreurs de prédiction.

Pour les données gravement déséquilibrées (> rapport 95-5), le rapport **AUROC**et **AUPRC**Au lieu de l'exactitude, l'AUPRC est plus sensible à la classe minoritaire, ce qui est ce qui vous intéresse habituellement (spam, fraude, sentiment rare).

> 对于严重不平衡的数据 ((> 95-5 比例), rapport **AUROC**et **AUPRC**Le taux de précaution est le plus élevé de la population.

**Common bug to avoid.**En rapportant micro-F1 au lieu de macro-F1 sur des données déséquilibrées, on obtient un nombre qui semble élevé parce qu'il est dominé par la classe majoritaire.

> **常见错误。**Dans les données déséquilibrées, le rapport micro-F1 plutôt que macro-F1 donnerait un chiffre qui semble très élevé, car il est dominé par la majorité des classes.

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

Scikit-learn le fait en six lignes, correctement.

> Je suis un peu en train de faire des choses.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Trois choses à remarquer.`stop_words=None`Il ne peut pas se permettre de négationner.`ngram_range=(1, 2)`ajoute des bigrammes donc `not_good`devient une caractéristique. `sublinear_tf=True`Ces trois indicateurs représentent la différence entre une base de 75% et une base de 85% sur SST-2.

> Il y a trois choses à noter.`stop_words=None`Il faut le laisser.`ngram_range=(1, 2)`添加二元组使 `not_good`Il est devenu un trait.`sublinear_tf=True`抑制重复词── Ces trois signes sont la différence entre la ligne de base de la TSS-2 de 75% et la ligne de base de 85%.

### Quand trouver un transformateur

- Les modèles classiques échouent ici.
  Le modèle classique ici va rater.
- Des critiques longues où le sentiment change au milieu du document.
  情感在文档中转变的长评论──
- "La caméra était super mais la batterie était terrible". Vous devez attribuer le sentiment aux aspects.
  "La caméra était super mais la batterie était terrible".
- Les langues non anglaises et à faible consommation de ressources.
  Non anglais, faible ressources linguistiques, plusieurs langues BERT pour vous fournir gratuitement des échantillons de base de ligne.

Si vous avez besoin de l'un des éléments ci-dessus, passez à la phase 7 (merde profonde des transformateurs).

> Si vous avez besoin de plus de tout, sautez à la phase 7 (Transformer Deep Into) ⋅ sinon, dans le TF-IDF 加二元组加否定处理上的朴素贝叶斯或逻辑回归就是你2026年生产基线――

### Le piège de la reproductibilité (encore une fois)

La réapprentissage des modèles de sentiment est routinière. La réévaluation de ces modèles n'est pas. Les chiffres de précision rapportés dans les documents utilisent des fractions spécifiques, des pré-traitement spécifiques, des jetons spécifiques. Si vous comparez votre nouveau modèle à une ligne de base sans utiliser le même pipeline, vous obtiendrez des delta trompeurs.

> Le nouveau modèle émotionnel est une opération ordinaire. La réévaluation n'est pas un rapport de la précision du rapport. Le rapport utilise des chiffres spécifiques à la division de données, à la pré-traitement spécifique, à la fraction de mots. Si vous n'utilisez pas la même ligne de flux pour comparer le nouveau modèle à la ligne de base, vous obtiendrez une différence d'erreur.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-sentiment-baseline.md`- Le numéro de la liste:

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Les exercices

1. **Easy.**Ajouter `apply_negation`comme étape de pré-traitement dans le pipeline scikit-learn et mesurer le delta de la F1 sur un petit ensemble de données de sentiment.
   **简单。**Il va`apply_negation` comme étape de pré-traitement ajoutée à la petite apprentissage 流水线, dans un petit ensemble de données émotionnelles, mesure F1 变化
2. **Medium.**Implémentation de la régression logistique pondérée par classe (passage `class_weight="balanced"`Mesurer l'effet sur un déséquilibre synthétique de classe 90-10.
   **中等。**实现类别加权逻辑回归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅ dans la synthèse de 90 à 10 类别不平衡上测量效果
3. **Hard.**Construisez un détecteur de sarcasme en formant un deuxième classifiateur sur les résidus du modèle de sentiment. Documentez votre configuration expérimentale. Avertissez le lecteur lorsque votre précision est inférieure à la chance (le niveau de chance sur le sarcasme de 2 classes est de ~ 50% et la plupart des premières tentatives y atterrissent).
   **困难。**Dans le modèle émotionnel, entraînez un deuxième classifiant pour construire un testeur de pierres. Récisez votre expérience.

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les termes clés

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Encore une lecture

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) l'enquête fondamentale. Longue, mais les quatre premières sections couvrent tout le classique.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) le papier qui montrait Bigrams + Naïve Bayes est difficile à battre sur le texte court. / 证明二元组 + 朴素贝叶斯在短文上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) référence à `CountVectorizer`- Je suis là .`TfidfVectorizer`, et chaque bouton que vous régler.`CountVectorizer`- Je suis là.`TfidfVectorizer`及你将调参的每个参数的参考──
