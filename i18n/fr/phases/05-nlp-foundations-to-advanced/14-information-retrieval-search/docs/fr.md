# Récupération et recherche d' informations

> BM25 est précis mais fragile. Dense lance un large filet mais manque de mots clés. Hybrid est le modèle par défaut de 2026.
> BM25  précis mais fragile。密检索撒大网但漏掉关键词──混合检索是2026年默认选择──其余都是调参──

> **【中文解读】**Le référencement de l'information est l'application de l'analyse de l'information.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Le problème , l' introduction du problème

L'utilisateur tape "ce qui se passe si quelqu'un ment pour obtenir de l'argent" et s'attend à trouver le statut qui couvre réellement cela: " section 420 IPC. " Une recherche de mots clés la manque entièrement (pas de vocabulaire partagé). Une recherche sémantique la manque si les emblèmes n'ont pas été formés sur le texte juridique.
> Utilisateur entre "qu'est-ce qui se passe si quelqu'un ment pour obtenir de l'argent" et souhaite trouver une couverture réelle de ce contenu: " section 420 IPC "──

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


L'IR est le pipeline sous chaque système RAG, chaque barre de recherche, chaque recherche floue de site de documentation. L'architecture 2026 qui fonctionne dans la production n'est pas une seule méthode.
> L'IR est chaque système RAG, chaque recherche, chaque station de documents, chaque flux de données, et chaque station de documents est une chaîne de méthodes complémentaires, chaque capture est un échec de l'autre.

Cette leçon construit chaque pièce et nom qui échoue chaque capture.
> Ce cours a été construit en partie et a montré qu'ils avaient tous été défaits.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


## Le concept de base.

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Choisissez les quatre couches.
> Quatre étages. Choisissez ce dont vous avez besoin.

1. **Sparse retrieval (BM25).**Rapide, précis sur les correspondances exactes, terrible sur la sémantique. Remplissez un index inversé. Sub-10ms par requête sur des millions de documents. Vous obtenez des références de statut, codes de produit, messages d'erreur, entités nommées correctement.
2. **Dense retrieval.**Encodez la requête et les documents en vecteurs. recherche du voisin le plus proche. Capture des paraphrases et des similitudes sémantiques. Manque des correspondances exactes de mots clés qui diffèrent par un caractère. 50-200 ms par requête avec FAISS ou un vecteur DB.
3. **Fusion.**La fusion de rangs réciproque (RRF) est la solution par défaut parce qu'elle ignore les scores bruts (qui vivent dans différentes échelles) et n'utilise que les positions de rang.
4. **Cross-encoder rerank.**Prenez le top-30 de fusion. Exécutez un cross-encoder (query + document ensemble, en marquant chaque paire). Gardez le top-5.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万文档上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**Pour les données de référence, il est nécessaire de faire une analyse de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur.
3. **融合。**合并稀疏和密的排列列表──倒数排列融合(Reciprocal Rank Fusion, RRF) est une simple sélection par défaut, car elle ignore le nombre initial (existe à différentes échelles) et utilise uniquement la position de classement── lorsque vous savez qu'un signal domine dans votre domaine, la fusion de puissance est une sélection──
4. **交叉编码器重排序。**De la fusion à la première partie, on prend le top-30[6]. On utilise le top-30 pour le top-30 et on conserve le top-5[6].

La récupération à trois voies (BM25 + dense + learn-sparse comme SPLADE) dépasse les deux voies dans les indices de référence de 2026, mais nécessite une infrastructure pour les indices learn-sparse.
> 三路检索 (BM25 + 密 + 学习稀疏如 SPLADE) est un système de réparation de deux voies qui sera supérieur à celui de la base de données de 2026 mais qui nécessite l'apprentissage de l'infrastructure de l'indexation rare.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.


## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
gx-hybrid-retrieval
```

## Faites-le

### Étape 1: BM25 à partir de zéro
> Deux paramètres à connaître:`k1=1.5`控制词频和;更高 signifie plus haut du pouvoir de répétition.`b=0.75`控制长度归结;0 忽略文档长度,1 完全归结;; la valeur par défaut est la valeur recommandée dans le premier article de Robertson, très peu nécessitent d'ajustement;;

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Deux paramètres qui méritent d'être connus.`k1=1.5`Il est possible de contrôler la saturation par fréquence terminale; plus élevé signifie plus de poids sur la répétition terminale. `b=0.75`Les paramètres par défaut sont les recommandations de Robertson provenant du papier original et nécessitent rarement une mise en forme.
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2`Il est assez fort pour la plupart des recherches en anglais.`paraphrase-multilingual-MiniLM-L12-v2` taux de précision le plus élevé`bge-large-en-v1.5`Ou `e5-large-v2`Il y a une autre.

### Étape 2: récupération dense avec un bi-encodeur
> `k=60`Le nombre de références est de l'origine RRF 论文──更高的 `k`Pour les contributions des différences de classement, les taux de participation sont plus faibles.`k`60 est la valeur par défaut déjà publiée, très peu nécessitent de modification.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2 normaliser les intégrations de sorte que le produit de point est égal au cosine. `all-MiniLM-L6-v2`est 384 dimension, rapide et suffisamment fort pour la plupart des retouches en anglais.`paraphrase-multilingual-MiniLM-L12-v2`Pour une précision maximale,`bge-large-en-v1.5`ou `e5-large-v2`- Je suis désolé .
> 3 étapes de la formation. BM25 找到词汇匹配──密找到语义匹配──RRF 合并两个排名不需要分数校准──交叉编码器使用查询-文档对重新对 top-30 打分,捕获双编码器遗漏的细粒度相关性──保留 top-5──

### Étape 3: fusion de rang réciproque
> ♪ Le signe signifie ♪
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

Le `k=60`La constante provient du papier original RRF.`k`réduit la contribution des différences de rang;`k`60 est la version par défaut publiée et nécessite rarement une mise en forme.
> ), en particulier pour les RAG, les références**Recall@k**Si le passage correct n'est pas recherché, le lecteur ne peut pas répondre.

### Étape 4: recherche hybride + réaffectation
> 调试技巧: Pour une requête qui n'a pas été rendue, par rapport à rare疏和密排名──如果一个找到正确文档而另一个没有,你有词汇不匹配(修复:添加缺失的一半) 或语义歧义(修复:更好的嵌入或重排序器)──

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

BM25 trouve des correspondances léxicales. Dense trouve des correspondances sémantiques. RRF fusionne les deux classements sans avoir besoin d'une calibration de score. Cross-encoder récorde le top-30 en utilisant des paires de documents de requête ensemble, ce qui capture une pertinence fine graine du bi-encodeur manqué. Gardez le top-5.

### Étape 5: évaluation

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

Pour RAG spécifiquement, **Recall@k**Le lecteur ne peut pas répondre si le passage correct n'est pas dans l'ensemble récupéré.

Pour les requêtes qui ne sont pas correctes, différez les classements rares et denses. Si l'un trouve le bon document et l'autre non, vous avez un déséquilibre vocabulaire (fix: ajouter la moitié manquante) ou une ambiguïté sémantique (fix: meilleures emblèmes ou un réencadrement).


> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


La pile de 2026:
> 2026: année technique

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> La taille et la technologie.
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Quoi que vous choisissiez, budget pour l'évaluation. Rappel de référence avant de comparer la précision de fin à fin RAG. Un lecteur ne peut pas corriger ce que le récupérateur a manqué.
> Quoi que vous choisissiez, vous devez faire un budget pour évaluer le taux de réception de la recherche de base avant le taux de réception de la recherche de base.

### Les leçons durement acquises de la production RAG 2026
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**L'équipe passe quelques semaines à échanger des LLM et des conseils, et le contrôle à chaque fois qu'elle reçoit une demande, elle retourne à l'erreur.
- **分块策略比分块大小更重要。**Les codes et les codes de mise en place sont définis comme étant des codes et des codes de mise en place.
- **父文档模式。**检索小的"子"块以获得精度──当同一节的多子块出现时,换进父块以保留下文──这持续提升答案质量而无需重新训练──
- **k_rerank=3 通常最优。**Chaque augmentation d'un bloc supérieur à ce nombre augmente le jeton, la durée et le retard de production ne augmentent pas la qualité de la réponse.
- **HyDE / 查询扩展。**De la recherche générer des hypothèses de réponse, en les intégrant, en les recherchant.
- **上下文预算控制在 8K token 以下。**Dans cette limite, la durée de vie signifie la réorganisation des valeurs.
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题率 关键控制在用户看到之前阻止回归──
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**En particulier, les requêtes de confusion et de signification sont publiées lorsque l'index SPLADE est soutenu par l'infrastructure.

- **80% of RAG failures trace to ingestion and chunking, not the model.**Les équipes passent des semaines à échanger des LLM et à régler les instructions, tandis que la récupération renvoie le mauvais contexte à chaque troisième requête.
- **Chunking strategy matters more than chunk size.**Les tableaux, les codes et les en-têtes sont divisés en deux.
- **Parent-doc pattern.**Retirer de petits morceaux " enfant " pour une précision. Lorsque plusieurs enfants de la même section parent apparaissent, échanger dans le bloc parent pour préserver le contexte. Cela améliore systématiquement la qualité des réponses sans recyclage.
- **k_rerank=3 is usually optimal.**Chaque pièce supplémentaire qui ajoute le coût des jetons et la latence de génération sans augmenter la qualité des réponses.
- **HyDE / query expansion.**Générer une réponse hypothétique à partir de la requête, intégrer, récupérer. Couper le fossé entre les questions courtes et les documents longs.
- **Context budget under 8K tokens.**Des coups constants à cette limite signifient que le seuil de ré-rangement est trop lâche.
- **Version everything.**Les instructions, les règles de déchiquetage, le modèle d'intégration, le réencadrement. Toute dérive brise silencieusement la qualité des réponses. Les portes de l'IC sur la fidélité, la précision du contexte et le taux de requête non répondue bloquent les régressions avant que les utilisateurs ne les voient.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**Envoyer lorsque l'infrastructure prend en charge les indices SPLADE.
> Selon les mesures de l'industrie de 2026, la conception correcte de la recherche réduit de 70-90% les apparences. La plupart des performances RAG augmentent par une meilleure recherche, plutôt que par des modèles modélisés.

Une conception correcte de récupération réduit les hallucinations de 70-90% selon les mesures de l'industrie de 2026.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-retrieval-picker.md`- Le numéro de la liste:
> 保存为 `outputs/skill-retrieval-picker.md`- Le numéro de la liste:

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──


## Les exercices

1. **Easy.**Mise en œuvre `hybrid_search`Comparer le rappel à 5 entre BM25 seulement, dense seulement et hybride.
2. **Medium.**Ajoutez le calcul MRR. Pour chaque requête de test avec un document correct connu, trouvez le rang du document correct dans les classements BM25, dense et hybride.
3. **Hard.**Téléchargez un codeur dense sur votre domaine en utilisant MultipleNegativesRankingLoss (Transformateurs de sentences). Construisez un ensemble de formation à partir de 500 paires de requêtes-document. Comparer le rappel avant et après la télétravail.
> 1. **简单。**Dans 500 documents de la langue réalisée ci-dessus`hybrid_search`△测试 20 个查询──比较 BM25 seulement、densité seulement 和混合的回忆@5──
2. **中等。**Pour chaque requête de test de documentation correcte connue, trouvez le document correcte dans la position BM25 密和混合排名.
3. **困难。**Utiliser des systèmes de classification de la phrase (MultipleNegativesRankingLoss) dans votre domaine.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> ♪ Les termes que les gens disent souvent ♪ ♪ Le sens réel ♪
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) le traitement définitif de BM25.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, le bi-encodeur canonique.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)Le retriever à sparsité apprise qui ferme l'écart avec dense.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) papier RRF.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) Retrait en interaction tardive.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, classique
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)                                                                                                                                                                                                                                                              
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文。
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
