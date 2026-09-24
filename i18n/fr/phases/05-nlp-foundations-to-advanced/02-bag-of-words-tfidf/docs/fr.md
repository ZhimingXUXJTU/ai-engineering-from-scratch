# Bag de mots, TF-IDF, et représentation du texte .

> Le TF-IDF va encore mieux que les embeddings sur des tâches bien définies en 2026.
> Avant de compter, après de réfléchir, sur des missions définies, le FDI-F jusqu'en 2026 sera encore en mesure de gagner.

> **【中文解读】**Le terme "jeu de l'information" est utilisé pour désigner les mots de l'article.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Construire des représentations de sacs de mots et de TF-IDF à partir de zéro
  From零构建词袋模型和 TF-IDF Indiquer
- Comprendre les vecteurs rares, la fréquence des termes et la fréquence inverse des documents
  Comprendre la fréquence de la fréquence et de la fréquence des échanges
- Utilisation du compte-vectorificateur et du tfidfvectorizer de scikit-learn dans la production
  Dans la production, utilisez le compte-vectorificateur et le tfidfvectorizer
- Savoir quand TF-IDF gagne sur les emblèmes et quand il échoue
  Je sais que TF-IDF, comment a-t-il gagné, comment a-t-il échoué.

## Le problème , l' introduction du problème

Le modèle a besoin de numéros.

> Le modèle a besoin de chiffres.

Chaque pipeline de PNL doit répondre à la même question. Comment transformer un flux de jetons de longueur variable en un vecteur de taille fixe que le classifiateur peut consommer. La première réponse sur laquelle le champ a atterri était la plus stupide qui fonctionne. Comptez les mots. Faites un vecteur.

> Chaque ligne de flux de NLP doit répondre à la même question: comment va-t-on changer le nombre de jetons en un volume de taille fixe, pour permettre à la classification de consommer ? La première réponse donnée dans ce domaine est la méthode la plus utilisée.

Ce vecteur a produit plus de PNL de production que tout autre modèle d'intégration. Filtres de spam, classifiateurs de sujets, détection d'anomalies de journaux, classement de recherche (avant BM25), première vague d'analyse des sentiments, première décennie de benchmarks de PNL académiques. En 2026, les praticiens atteignent toujours la première place sur des tâches de classification étroites. Il est rapide, interprétable et souvent indistinguible d'un modèle d'intégration de paramètres de 400 M dans des tâches où la présence de mots est ce qui compte.

> Cette production de NLP à volumes répartis est plus importante que toute autre application de modèles intégrés. Les filtres de spam, les filtres de thèmes, les archives, les tests de recherche, les recherches, les analyses émotionnelles et les tests de base de NLP académiques sont utilisés dans la première décennie de la première vague de tests.

Cette leçon construit un sac de mots, puis TF-IDF, à partir de zéro, puis montre scikit-apprendre faire la même chose en trois lignes, puis nomme le mode d'échec qui vous fait atteindre pour les emblèmes.

> Ce cours commence par un modèle de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**Bag of Words (BoW)**Pour chaque document, comptez combien de fois chaque mot de vocabulaire apparaît.`i`est le nombre de mots `i`- Je suis désolé .

> **词袋模型（Bag of Words, BoW）**抛弃顺序──对每文档,统计每词表词出现的次数──向量长度是词表大小──位置 `i`C' est le mot`i`Le nombre de personnes.

**TF-IDF**Un mot qui apparaît dans chaque document est non informatif, donc réduisez-le. Un mot rare dans le corpus mais fréquent dans un seul document est un signal, donc redoublez-le.

> **TF-IDF**Pour BoW, le poids de la parole apparaît dans chaque document sans quantité d'information, donc en diminuant le poids.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

Où ?`TF`est la fréquence des termes dans le document, `df`est la fréquence du document (combien de documents contiennent le mot), `N`Les documents sont totaux.`log`Il garde le poids limité pour les mots omniprésents.

> Parmi eux `TF`C'est le cas de la première fois.`df`Il y a beaucoup de documents contenant ce mot.`N`C'est le nombre total des archives.`log`Il faut que le pouvoir de la parole soit maintenu.

Propriété clé: les deux produisent des vecteurs rares avec des axes interprétables. Vous pouvez regarder les poids d'un classifiateur formé et lire quels mots poussent un document vers chaque classe. Vous ne pouvez pas le faire avec une intégration BERT 768-dimensionnelle.

> 关键特性: les deux génèrent des rares tendances d'axe explicable. Vous pouvez consulter le poids d'un bon classifiant, lire quels mots le document sera déployé dans chaque catégorie. Vous ne pouvez pas utiliser un BERT de 768 dimensions pour le faire.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
bow-tfidf
```

## Faites-le

### Étape 1: construire le vocabulaire

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Entrée: liste des documents Tokenized (tout Tokenizer au niveau des mots le fera; le `code/main.py`Dans cette leçon, une variante en minuscules simplifiée est utilisée.`{word: index}`L'ordre d'insertion stable signifie que l'index de mots 0 est le premier mot vu dans le premier document.

> 输入:token 化的文档列表(任何词级分词器都可以;本课的 `code/main.py`Utilisation simplifiée ignorer les changements de texte`{word: index}`字典──稳定的插入顺序 字符索引 0 est le premier mot vu dans le premier document──惯例各不相同;skikit-learn 字母排序──

### Étape 2: sac de mots

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

Les lignes sont des documents, les colonnes sont des indices de vocabulaire.`[i][j]`est "combien de fois le mot `j`apparaît dans le document `i`. " Doc 1 a été`cat`Deux fois parce qu'il l'a fait.`ran`Zéro fois parce que ce n'est pas le cas.

> 行是文档──列是词表索引──条目 `[i][j]`C' est un mot`j`Dans les archives`i`Il y a eu plusieurs fois.`cat`Parce qu'il est apparu deux fois.`ran`Parce qu'il n'est pas apparu.

### Étape 3: fréquence des termes et fréquence des documents

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

Deux astuces qui méritent d'être nommées.`(n+1)/(d+1)`éviter `log(x/0)`- Le trail .`+1`Il est également possible de faire en sorte qu'un mot dans chaque document ait toujours IDF 1 (et non 0), ce qui correspond à l'interface par défaut de scikit-learn.`log(N/df)`Les deux fonctionnent, la version lisse est plus conviviale.

> Deux techniques de l'élimination des éclats`(n+1)/(d+1)`viter `log(x/0)`尾部 de `+1`¢ s'assurer que les mots de chaque document apparaissent toujours en 1 ¢ au lieu de 0 ¢), conformément à la valeur par défaut de l'apprentissage de scikit¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬`log(N/df)`两种都有效;平滑版本更友好

### Étape 4: TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

Trois documents, cinq mots vocabulaires (`the`- Je suis là .`cat`- Je suis là .`sat`- Je suis là .`dog`- Je suis là .`ran``the`apparaît dans les trois, donc son IDF est faible. `dog`Les vecteurs sont rares (la plupart des entrées sont petites) et les mots discriminatifs apparaissent.

> Il y a trois mots, cinq expressions.`the`- Je suis là.`cat`- Je suis là.`sat`- Je suis là.`dog`- Je suis là.`ran`)。`the`Dans tous les trois archives, il est apparu, donc son IDF est très faible.`dog`Il est également connu pour avoir été utilisé dans les archives de l'armée israélienne.

### Étape 5: normaliser les rangées L2

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

Sans normalisation, un document plus long obtient un vecteur plus grand et domine les scores de similitude. La normalisation L2 met chaque document sur l'hypersphère unitaire.

>  sans regroupement, les documents plus longs obtiendront un volume plus grand et domineront la similarité de la note. L2  regroupement placeront chaque document sur unité supersoule.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

Scikit-Learn envoie la version de production.

> Sikit-learn a fourni une version de production.

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`fait la tokenization, le vocabulaire et le BoW en un seul appel. `TfidfVectorizer`Les deux matrices sont rares. pour 100 000 documents, la version dense ne s'inscrit pas dans la mémoire; reste rare jusqu'à ce que le classifiateur demande dense.

> `CountVectorizer`En une fois调用中完成分词、构建词表和 BoW。`TfidfVectorizer`增加 IDF 加权和 L2 归结化──都回归稀疏矩阵──对10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏──

Des boutons qui changent tout:

>  modifiant tout                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### Lorsque le TF-IDF gagne toujours (à partir de 2026)

- La détection du spam, l'étiquetage des sujets, le démarrage des anomalies du journal.
  垃圾邮件检测、主题标注、日志异常标注──existence ou non du mot est essentiel; signification de la différence est peu importante──
- Les régimes à faible données (des centaines d'exemples étiquetés) TF-IDF plus régression logistique ne nécessitent aucun coût de pré-entraînement.
  低数据场景(100 étiquettes de données) ――TF-IDF 加逻辑回归没有预训成本──
- La latence est importante partout. TF-IDF plus un modèle linéaire répond en microsecondes.
  Le temps de réponse du modèle de TF-IDF est de micro-seconde.
- Les systèmes qui doivent expliquer leurs prédictions, examiner les coefficients du classifiateur, les mots positifs sont la raison.
  需要解释预测结果的系统──检查分类器的系数──排名最高的正权重词就是原因──

### Lorsque le TF-IDF échoue

L'échec de la cécité sémantique.

> 语义盲点──考虑以下两个文档:

- "Le film n'était pas du tout bon".
- "Le film était excellent".

L'une est négative, l'autre est positive, leur superposition entre les deux est exactement la même.`{the, movie, was}`Un classifiateur de sacs de mots doit mémoriser ce mot .`not`près de`good`Il peut apprendre cela sur suffisamment de données, mais jamais aussi gracieusement qu'un modèle qui comprend la syntaxe.

> Une est une évaluation négative, une est une évaluation affirmative.`{the, movie, was}`Les mots doivent être retenus.`good` près de `not`Il peut apprendre cela avec suffisamment de données, mais ne sera jamais aussi beau qu'un modèle de compréhension de la grammaire.

L'autre échec: des mots hors vocabulaire à l'inférence.`Zoomer-approved`Les sous-verbes (leçon 04) gèrent cela. TF-IDF ne peut pas.

> 另一个失败:推理时的词表外(Out-of-vocabulary, OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`Si ce symbole n'est pas apparu dans la formation, il est possible de résoudre ce problème.

### Hybride: intégrations pondérées TF-IDF

Le principe par défaut pragmatique de 2026 pour la classification des données moyennes: utiliser les poids TF-IDF comme attention sur les emblèmes de mots.

> Le programme de mise en œuvre de la mise en œuvre de la TF-IDF en 2026:

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

Vous obtenez la capacité sémantique des emblèmes et l'accent sur les mots rares du TF-IDF. Le classifiateur se forme sur le vecteur regroupé. Cela dépasse soit par lui-même la classification des sentiments, des sujets et des intentions en dessous d'environ 50 000 exemples étiquetés.

> Vous avez acquis des capacités de synthèse grâce à l'intégration, à partir de TF-IDF  obtenir des rares mots soulignés ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙    ∙ ∙      ∙                                                                                                                                                                                                                                  

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-vectorization-picker.md`- Le numéro de la liste:

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## Les exercices

1. **Easy.**Mise en œuvre `cosine_similarity(doc_vec_a, doc_vec_b)`vérifier que les documents identiques obtiennent un score de 1,0 et les documents de vocabulaire disjoint un score de 0,0.
   **简单。**Dans le cadre de l'intégration de l' L2 TF-IDF `cosine_similarity(doc_vec_a, doc_vec_b)` Évaluation du même document avec un score de 1.0, le texte complet ininterrompue avec un score de 0.0♦
2. **Medium.**Ajouter `n-gram`soutien à `bag_of_words`Paramètre .`n`produit des comptes sur `n`- Je vais tester ça.`n=2`sur`["the", "cat", "sat"]`produit des nombres de bigrammes pour `["the cat", "cat sat"]`- Je suis désolé .
   **中等。**Pour`bag_of_words`添加 `n-gram`支持──参数 `n` générer `n`-grammes de chiffres.`n=2`时 `["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`Le nombre de personnes.
3. **Hard.**Construisez l'hybrid intégré pondéré TF-IDF ci-dessus en utilisant les vecteurs GloVe 100d (télécharger une fois, cache). Comparer la précision de classification avec les intégrations simples TF-IDF et simples en moyenne intégrées sur le jeu de données 20 Newsgroups. Rapporte qui gagne où.
   **困难。**Utilisation GloVe 100 维向量 (en anglais) ⋅construire le système de mise en cache TF-IDF et de mise en cache de l'information.

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les termes clés

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Encore une lecture

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) la référence canonique de l'API, plus les notes sur chaque bouton. / 权威 API 参考,以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) le document qui a fait du TF-IDF le défaut pour une décennie. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026 prendre quand l'ancienne méthode gagne et pourquoi. / 2026 年对旧方法何时胜出以及为什么的观点──
