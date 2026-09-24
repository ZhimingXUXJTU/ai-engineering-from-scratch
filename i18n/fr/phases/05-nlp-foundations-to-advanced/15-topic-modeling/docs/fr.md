# Sujet Modélisation  LDA et BERTopic  Sujet de construction  LDA et BERTopic

> LDA: les documents sont des mélanges de sujets, les sujets sont des distributions sur des mots. BERTopic: les documents sont un cluster dans un espace intégré, les clusters sont des sujets. Le même objectif, des décompositions différentes.
> LDA: le document est une combinaison de sujets, le sujet est une distribution de mots.

> **【中文解读】**LDA avec le modèle de probabilité de découverte de sujets, BERTopic avec BERT 嵌入──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## Le problème , l' introduction du problème

Vous avez 10 000 billets de soutien à la clientèle, 50 000 articles d'actualité ou 200 000 tweets. Vous devez savoir ce que la collection est sans le lire. Vous n'avez pas de catégories étiquetées. Vous ne savez même pas combien de catégories existent.
> Vous avez 10 000 张客户支持工单,50,000 篇新闻文章或200,000 条推文── vous devez comprendre le sujet de ce recueil sans avoir lu── vous n'avez pas de catégories marquées── vous ne savez même pas combien de catégories il existe──

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


La modélisation de thèmes répond à cela sans supervision. Donnez-lui un corpus, obtenez un petit ensemble de thèmes cohérents et, pour chaque document, une distribution sur ces thèmes.
> Réponse à cette question sans surveillance. Donnez-lui une bibliothèque de textes, retournez à un groupe de sujets réguliers, ainsi qu'à la répartition de chaque document sur ces sujets.

Deux familles algorithmiques dominent. LDA (2003) traite chaque document comme un mélange de sujets latents et chaque sujet comme une distribution sur des mots. L'inférence est bayésienne.
> 两个算法族占主导地位――LDA(2003) considérera chaque document comme une mixture de sujets potentiels, chaque sujet étant une distribution de mots―― la conclusion est celle de Béries―― il est toujours nécessaire de distribuer les sujets mixtes et de publier une distribution de probabilité de la distribution de la classe de mots explicables――

BERTopic (2020) encode les documents avec BERT, réduit la dimensionnalité avec UMAP, les clusters avec HDBSCAN et extrait les mots de thème via TF-IDF basé sur la classe. Il gagne sur le texte court, les médias sociaux et tout ce qui compte plus que la similitude sémantique que la chevauchée des mots. Un document obtient un sujet, ce qui est une limitation pour le contenu de forme longue.
> BERTopic (en anglais) est un document de référence de la société de l'information et de l'information (en anglais: BERTopic) qui est basé sur le langage de la langue de l'Union européenne (UE), qui est basé sur le langage de la langue de l'Union européenne (UE), et qui est basé sur le langage de la langue de l'Union européenne (UE).

Cette leçon construit l'intuition pour les deux et les noms à choisir pour un corps donné.
> Ce cours est destiné à créer un sens et à déterminer le thème à choisir.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


## Le concept de base.

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**Chaque sujet est une distribution sur des mots. Chaque document est un mélange de sujets. Pour générer un mot dans un document, prenez un échantillon d'un sujet du mélange du document, puis prenez un échantillon d'un mot de la distribution de ce sujet. L'inférence inverse ceci: étant donné les mots observés, inférez la distribution de sujet par document et la distribution de mots par sujet.
> **LDA 生成故事。**Chaque sujet est une distribution de mots. Chaque document est une combinaison de sujets. Il faut générer un mot dans le document, en le prenant à partir de la combinaison du document, puis en le prenant à partir de la distribution du sujet.

L'alimentation de base de l'AEL:
> 关键 LDA 输出:

- `doc_topic`: matrice `(n_docs, n_topics)`, chaque ligne s'élève à 1 (mixture de thèmes du document).
- `topic_word`: matrice `(n_topics, vocab_size)`, chaque ligne s'élève à 1 (distribution des mots du sujet).
> - `doc_topic`: Régime`(n_docs, n_topics)`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,
- `topic_word`: Régime`(n_topics, vocab_size)`, pour chaque ligne totale et pour 1 (()

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Encodez chaque document avec un transformateur de phrases (p. ex., `all-MiniLM-L6-v2`Les vecteurs de 384 dimensions.
2. Réduire la dimensionnalité avec UMAP à ~5 dimensions.
3. Cluster avec HDBSCAN. basé sur la densité, produit des clusters de taille variable et un label "outlier".
4. Pour chaque cluster, calculer TF-IDF basé sur la classe sur les documents du cluster pour extraire les mots les plus importants.
> 1. Uż句子 Transformer`all-MiniLM-L6-v2`Il est également possible de faire des recherches sur les différents types de données.
2. Utilisez UMAP 降维到大约5维度.
3. Utilisation de la méthode HDBSCAN 聚类── basée sur la densité, générer des changements de taille 聚类和离群值标签──
4. Pour chaque classe, le calcul sur la base des documents de classe TF-IDF est effectué pour élever les mots de haut niveau.

La sortie est un sujet par document (plus une étiquette de -1), optionnellement, une adhésion douce via le vecteur de probabilité de HDBSCAN.
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地,通过 HDBSCAN的概率向量获得软成员资格──

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.


## Construisez-le et mettez-le en œuvre.
```figure
topic-drift
```

## Faites-le

### Étape 1: LDA via scikit-learn
> Remarque: en dépit de l'utilisation de mots arrêtés, min_df 和 max_df 过罕见和无处不在的词, utilisez CountVectorizer (c'est-à-dire CountVectorizer)

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Remarque: les mots d'arrêt supprimés, min_df et max_df filtrent des termes rares et omniprésents, CountVectorizer (pas TfidfVectorizer) parce que LDA s'attend à des comptes bruts.
> `Topic != -1`Le groupe de données de BERTopic est abandonné.`min_topic_size`控制 HDBSCAN's minimum聚类大小;BERTopic 库默认为 10──本例为课程规模显然设为15──对于超过10,000 文档语料,增加到50或100──

### Étape 2: BERTopic (production)
> Les deux méthodes sont de sortie de la question de savoir si ces mots sont réunis.

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

Le filtre est allumé .`Topic != -1`dépose le bac à écarts de BERTopic (documents que HDBSCAN ne pouvait pas regrouper). `min_topic_size`Il est également possible de calculer la taille minimale du cluster HDBSCAN; la taille par défaut de la bibliothèque BERTopic est 10.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI(归一化点逐点互信息), va être le nombre de points regroupés en émetteurs de thème, par le biais de l'équivalence des émetteurs de l'équivalent.`gensim.models.CoherenceModel`配 `coherence="c_v"`Il y a une autre.
- **主题多样性。**Toutes les catégories de mots sont classées en termes de proportion de mots.
- **定性检查。**Les mots de chaque sujet sont-ils nommés une chose réelle ?

### Étape 3: évaluation

Les deux méthodes produisent des mots de thème.

- **Topic coherence (c_v).**Combine NPMI (informations mutuelles normales en sens ponctuel) des paires de mots de haut niveau sur des contextes de fenêtre coulissante, agrégant les scores en vecteurs de sujet et comparant ces vecteurs par similitude cosine.`gensim.models.CoherenceModel`avec `coherence="c_v"`- Je suis désolé .
- **Topic diversity.**Fraction de mots uniques sur les mots clés de tous les sujets.
- **Qualitative inspection.**Les mots clés de chaque sujet sont-ils réels?


> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Quand choisir lequel

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

La plus grande considération pratique est la longueur du document. Les emplacements BERT tronquent; LDA compte le travail sur n'importe quelle longueur. Pour les documents plus longs que le contexte du modèle d'embedding, soit chunk + aggregate ou utilisez LDA.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


## Utilisez-le avec le cadre de réalisation

La pile de 2026:
> 2026: année technique

- **BERTopic.**Par défaut pour le texte court et tout ce qui a de la signification.
- **`gensim.models.LdaModel`.**LDA classique pour la production, mature, testée en combat.
- **`sklearn.decomposition.LatentDirichletAllocation`.**LDA facile pour les expériences.
- **NMF.**Factorisation de matrice non négative, alternative rapide à LDA, qualité comparable sur texte court.
- **Top2Vec.**Conception similaire à BERTopic, communauté plus petite mais bonne sur certaines critères de référence.
- **FASTopic.**Plus récente, plus rapide que BERTopic sur de très gros corps.
- **LLM-based labeling.**Exécutez une clôture, puis demandez à un modèle de nommer chaque cluster.
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**Classe de production classique LDA, mature, longue expérience
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单 LDA──
- **NMF。**Non négatif de la répartition de la LDA, en équivalent à la qualité.
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新, dans un super gros langage 快──
- **基于 LLM 的标注。**- Je vais vous dire de ne pas le faire.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-topic-picker.md`- Le numéro de la liste:
> 保存为 `outputs/skill-topic-picker.md`- Le numéro de la liste:

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──


## Les exercices

1. **Easy.**LDA avec 5 sujets sur le jeu de données de 20 Newsgroups. Imprimez les 10 premiers mots par sujet. Étiquettez chaque sujet à la main. L'algorithme a-t-il trouvé les vraies catégories?
2. **Medium.**Réglez BERTopic sur le même sous-ensemble de 20 Newsgroups. Comparer le nombre de sujets trouvés, les mots clés et la cohérence qualitative par rapport à LDA.
3. **Hard.**Comptez la cohérence c_v pour LDA et BERTopic sur votre corpus. Exécutez chacun avec 5, 10, 20, 50 sujets.
> 1. **简单。**En 20 groupes de nouvelles, les données sont collectées avec 5 thèmes adaptés à l'ADL.
2. **中等。**En comparaison avec le nombre de sujets trouvés, les mots de haut niveau et la connectivité de la définition avec la LDA, quel est le plus clairement présenté la vraie catégorie ?
3. **困难。**Dans votre langage, calculer la continuité de l'ADL et du BERTopic.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> ♪ Les termes que les gens disent souvent ♪ ♪ Le sens réel ♪
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) le journal de l'Agence de l'emploi.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) le journal BERTopic.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)Le journal qui a introduit c_v et les amis.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) la référence de production.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
