# Génération de texte avant les transformateurs  N-gramme Modèles de langage  Transformer  précédent génération de texte  N-gramme 语言模型

> Si un mot est surprenant, le modèle est mauvais. La perplexité fait une surprise. Le doucement le maintient fini.
> Si un mot est étonnant, le modèle est mauvais. La confusion transforme l'étonnement en numérique.

> **【中文解读】**N-gramme 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Avant les transformateurs, avant les RNN, avant les emblèmes de mots, un modèle de langage prédisait le mot suivant en comptant la fréquence avec laquelle il suivait le précédent `n-1`Les mots: "le chat" → "s'assoit" 47 fois, "le chat" → "s'est fait sauter" 12 fois, "le chat" → "réfrigérateur" 0 fois. Normalize pour obtenir une répartition de probabilité.

> Dans le cadre de la formation de la RNN, les modèles de langage sont utilisés pour la formation de la langue.`n-1`个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词后面 个词 个词后面 个词 个词 个词后面 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个词 个

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

C'est un modèle de langage n-gramme. Il a utilisé tous les reconnaisseurs de discours, tous les contrôleurs d'orthographe et tous les systèmes de traduction automatique basés sur des phrases de 1980 à 2015.

> C'est le modèle de langue n-gramme. De 1980 à 2015, il fonctionnait sur chaque reconnaisseur de voix, chaque vérificateur de copropriété et chaque système de traduction automatique basé sur le langage court.

Le problème intéressant est ce qu'il faut faire avec les n-grammes invisibles. Un modèle à base de compte brut attribue zéro probabilité à tout ce qu'il n'a pas vu, ce qui est catastrophique parce que les phrases sont longues et presque toutes les phrases longues contiennent au moins une séquence invisible. Cinquante ans de recherche de lissage fixé que.

> La question intéressante est: comment traiter les n-grammes invisibles. Le modèle primitif de calcul fondé sur la probabilité de distribution de zéro pour tout ce qui n'a pas été vu est catastrophique, car les phrases sont longues, presque toutes les phrases longues contiennent au moins une séquence invisibles.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### Le jeu de prédiction

Avant que cette machine n'existe, une expérience défini un modèle de langage. Couvrez la lettre suivante d'une phrase anglaise. Demandez à quelqu'un de deviner, une devinette à la fois, jusqu'à ce qu'il la fasse correctement. Écrivez le nombre de devinettes. Répétez pour quelques centaines de lettres.

Les chiffres de devinettes ne sont pas des trivialités. Ce sont un recodage sans perte du texte: remettre la séquence de calcul à un second devinetteur identique et ils peuvent reconstruire chaque lettre, parce qu'à chaque position ils savent exactement quelles devinettes viennent en premier. Un message que vous pouvez recoder en moins de symboles porte moins d'informations par symbole, donc les statistiques de recodage de devinettes placent un plafond sur l'entropie de l'anglais.

Shannon a fait cette étude en 1951 et a obtenu un nombre qui gouverne encore le champ. Un alphabet de 27 symboles (26 lettres plus espace) pouvait contenir`log2(27) ≈ 4.75`Les devins humains avec 100 lettres de contexte ont obtenu entre 0,6 et 1,3 bits par lettre. L'anglais est environ trois quarts des mouvements forcés. La structure qu'un modèle doit apprendre a été mesurée avant qu'un modèle puisse l'apprendre.

Chaque modèle de langue depuis est un joueur mécanique de ce jeu, et chaque numéro d'évaluation dans cette leçon est le jeu marqué:

- **Cross-entropy loss**L'entraînement d'un LM réduit littéralement son score au jeu de devinettes.
- **Perplexity**est `2^bits`(ou `e^nats`Le facteur de branchage qui reste devant le modèle après sa conjecture.
- **Context length is the player's memory.**Un modèle de trigramme joue avec deux jetons de mémoire. Un transformateur joue le même jeu avec 100K jetons. Les règles n'ont jamais changé; le joueur est devenu meilleur.

Un seul passage à la piste: les scores du jeu par lettre en bits (`log2`), tandis que les formules n-grammes ci-dessous donnent un score par mot en nats (log naturel)  et depuis la perplexité `e^H`en natts égaux `2^H`en bits, les deux vues sont la même mesure dans différentes unités.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- Réparer .`n`(généralement 3 pour les trigrammes, 4 pour les 4 grammes).

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`❖ Fixée `n`(三元组: 3, 4元组: 4)

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**Un rapport de 2007 sur le corpus de Brown a révélé que même un modèle de 4 grammes avait 30% de 4 grammes non vus dans l'entraînement.

> **零计数问题。**Les n-grammes non vus dans toute formation obtiennent une probabilité de zéro. Une étude de 2007 sur la bibliothèque de langage de Brown a révélé que même les modèles de quadrupléments ont 30% de la formation non vue dans les quatre groupes.

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**Ajouter un à chaque compte, simple, terrible pour des événements rares.
   **拉普拉斯（加一）。**Pour chaque compte, il y a un simple, mais il a un effet très faible sur les rares événements.
2. **Good-Turing.**Réaffectionner la masse de probabilité des événements à plus haute fréquence à ceux invisibles en fonction de la fréquence des fréquences.
   **Good-Turing。**̇ Basé sur la fréquence de fréquence, la qualité de la probabilité sera redistribuée de l'événement à haut fréquence à l'événement inattendu ̇
3. **Interpolation.**Combiner n-grammes, (n-1)-grammes, etc., estimations avec des poids réglables.
   **插值。**Il est possible de modifier le poids de la masse de l'échantillon.
4. **Backoff.**Si n-gramme a le nombre zéro, retourner à (n-1) gramme.
   **回退。**Si n-gramme 计数为零, retour à (n-1) grammes―Katz 回退将其归归化―
5. **Absolute discounting.**Soustraire une réduction fixe `D`de tous les nombres, redistribuer à l'invisible.
   **绝对折扣。**Déduction de tous les rabais fixes`D`, réaffecté à des événements inattendus.
6. **Kneser-Ney.**Discounting absolu plus un choix intelligent pour le modèle de l'ordre inférieur: utiliser *probabilité de continuation* (combien de contextes un mot apparaît dans) au lieu de fréquence brute.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择:使用*续接概率*(一个词出现多少上下文中) plutôt que la fréquence initiale。

Le concept de Kneser-Ney est profond. "San Francisco" est un gros mot commun. L'unigramme "Francisco" apparaît principalement après "San". Le rabat absolu naïf donne à "Francisco" une probabilité élevée d'unigramme (parce que le nombre est élevé). Kneser-Ney constate que "Francisco" apparaît dans un seul contexte et réduit en conséquence sa probabilité de continuation. Résultat: un bigram roman terminant par "Francisco" obtient la probabilité appropriée.

> Kneser-Ney a une profonde compréhension. "San Francisco" est un groupe de deux groupes communs. "Francisco" est principalement présent dans le groupe de deux groupes.

**Evaluation: perplexity.**Le facteur de probabilité négative moyenne par mot sur un ensemble de tests prolongés. Moins est mieux. Une perplexité de 100 signifie que le modèle est aussi confus qu'il choisirait uniformément parmi 100 mots.

> **评估：困惑度。**留出测试集上每字平均负对数似然的指数──越低越好──困惑度 100 signifie que le degré de confusion du modèle est équivalent à la moyenne de la sélection de 100 mots──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
ngram-backoff
```

## Faites-le

### Étape 1: compte des trigrammes

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

L'entrée est une liste de phrases jetonnées.`<s>`et `</s>`sont des limites de la phrase.

> 输入是分词后的句子列表──输出是 n-gramme 计数和上下文计数──`<s>`et `</s>`C'est le bord de la ligne.

### Étape 2: Légalisation de la place

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Ajouter 1 à chaque compte, mais en suralloquant la masse à des événements invisibles, blessant aussi des événements rares.

> ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 2 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 1 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2 ≈ 2

### Étape 3: Kneser-Ney (bigramme, interpolé)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Trois pièces en mouvement.`continuation_prob`Il est donc important de noter que les résultats de l'étude de la recherche ont été analysés dans des contextes différents.`lambda_prev`est la masse libérée par la réduction, utilisée pour pondérer le backoff.

> Il y a trois parties.`continuation_prob`捕获 "这个词出现在多少不同上下文中?"`lambda_prev`La probabilité finale est de la réduction principale pour la répartition des droits de retrait.

### Étape 4: générer du texte avec le prélèvement d'échantillons

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Pratiquer des échantillons proportionnels à la probabilité. Il donne toujours une sortie différente par semence. Pour une sortie similaire à celle de la recherche de faisceau, choisissez l'argmax à chaque étape (avidité) et ajoutez un petit bouton de randomité (température).

> Pour chaque étape de la recherche, chaque étape prend un argmax (à l'intérieur du cœur) et ajoute un petit tour de température (à l'extérieur du cœur).

### Étape 5: perplexité

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Pour le corpus Brown, un modèle KN de 4 grammes bien ajusté atteint une perplexité d'environ 140. un transformateur LM atteint 15-30 sur le même ensemble de test.

> Pour le groupe de langage Brown, une étroite confusion de quatre groupes de KN est de 140 à 30 fois supérieure à celle du même ensemble de tests.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

- **Classical NLP teaching.**L'exposition la plus claire au smoothing, MLE, et la perplexité que vous pouvez obtenir.
  **经典 NLP 教学。**Le plus clair de l'expérience de flattenage et de confusion que vous puissiez obtenir.
- **KenLM.**Bibliothèque de production n-gramme. Utilisé comme rescorer dans les systèmes de parole et de MT où la faible latence compte.
  **KenLM。**Classe de production n-gramme 库── Utilisation de réévaluateurs de voix et de matériel de calcul
- **On-device autocomplete.**Des modèles de trigramme sur le clavier.
  **设备端自动补全。**Le modèle de trois groupes de la carte est toujours en usage.
- **Baselines.**Si votre transformateur ne dépasse pas KN de manière large, quelque chose ne va pas.
  **基线。**Avant de déclarer votre modèle de langage neuronal, toujours calculer n-grammes de LM 困惑度── si votre Transformer  ne bat pas fortement KN, alors il y a un problème──

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-lm-baseline.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-lm-baseline.md`- Le numéro de la liste:

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Exercez un trigramme LM sur un corpus de Shakespeare de 1000 phrases. Générez 20 phrases. Elles seront plausibles localement mais incohérentes à l'échelle mondiale.
   **简单。**En train de trois groupes de langages, on peut utiliser 1000 phrases pour créer 20 phrases.
2. **Medium.**Vous devriez voir la perplexité de votre modèle KN sur une fraction de Shakespeare prolongée.
   **中等。**En attendant, vous devez voir que votre confort est réduit de 30 à 50%.
3. **Hard.**Construire un correcteur d'orthographe de trigramme: compte tenu d'un mot mal orthographié et de son contexte, générer des corrections et classer par probabilité de contexte dans le LM. Évaluer sur le corpus d'orthographe Birkbeck (public).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按 LM 下的上下文概率排序──在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) le traitement canonique des LM n-grammes et le lissage. / n-gramme 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) le papier qui a établi Kneser-Ney comme le meilleur n-gramme plus lisse. / 确定 Kneser-Ney 为最佳 n-gramme 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) le papier KN original. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) production rapide n-gramme LM, encore utilisé en 2026 pour les applications sensibles à la latence. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## Pour en savoir plus

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) l'expérience de jeu de devinettes qui définit la cible que chaque modèle de langage optimise encore.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) le traitement canonique des LM n-grammes et le lissage.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)Le papier qui a établi Kneser-Ney comme le meilleur n-gramme plus lisse.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) le papier KN original.
- [KenLM](https://kheafield.com/code/kenlm/) LM à production rapide n-gramme, encore utilisé en 2026 pour les applications sensibles à la latence.
