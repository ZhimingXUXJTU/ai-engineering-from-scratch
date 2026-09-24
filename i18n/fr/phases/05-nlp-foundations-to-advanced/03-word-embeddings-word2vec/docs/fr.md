# Word Embeddings  Word2Vec de zéro  Word2Vec de zéro

> Un mot est la compagnie qu'il garde.
> Un mot dépend de la société qu'il maintient.

> **【中文解读】**Word2Vec Place le mot mappé à l'espace spatial, similaire au mot dans l'espace spatial proche.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Le TF-IDF sait `dog`et `puppy`Il ne sait pas qu'ils signifient presque la même chose.`dog`ne peut pas généraliser à une revue sur `puppy`Vous pouvez le faire en lisant des synonymes, mais cela échoue dans les termes rares, le jargon de domaine et toutes les langues que vous ne vous êtes pas attendues.

> TF-IDF  知道 `dog`et `puppy`Il ne sait pas ce que cela signifie.`dog`Le classement des hauts formateurs ne peut pas être généralisé en termes de`puppy`Vous pouvez compenser par la liste des synonymes, mais cela échouera dans les termes rares et dans les langues que vous ne vous attendez pas à.

Vous voulez une représentation où`dog`et `puppy`- Ils sont proches de l'espace.`king - man + woman`Terres proches`queen`- Un modèle qui a été formé à la`dog`Transfère un signal à `puppy`- Je le fais gratuitement.

> Tu veux un mot, fais.`dog`et `puppy`Dans l'espace, près de toi.`king - man + woman`Je suis tombé`queen`Je suis là.`dog`Modèle de formation gratuit vers`puppy`- Je vais vous envoyer des signaux.

Word2Vec nous a donné cet espace. Un réseau neural à deux couches, des milliards de tokens de formation, publié en 2013. L'architecture est presque embarrassantement simple. Les résultats ont remodelé la PNL pendant une décennie.

> Word2Vec nous a donné un espace pareil. Le réseau neural à deux niveaux, des milliards de tokens de formation en cours de fonctionnement, publié en 2013.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**Distributional hypothesis**(Première, 1957): " Vous reconnaîtrez un mot par la compagnie qu'il garde. " Si deux mots apparaissent dans des contextes similaires, ils signifient probablement des choses similaires.

> **分布假设（Distributional Hypothesis）**(First, 1957): "Tu le reconnaîtras par une entreprise qui tient un mot. " Si deux mots apparaissent similaires dans la citation ci-dessus, ils peuvent signifier des choses similaires.

Word2Vec est disponible en deux versions, les deux exploitant cette idée.

> Word2Vec a deux variantes, nous avons utilisé cette idée.

- **Skip-gram.**Donnez un mot central, prédisez les mots environnants. `cat -> (the, sat, on)`avec la taille de la fenêtre 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, la fenêtre est grande pour 2
- **CBOW (continuous bag of words).**Compte tenu des mots environnants, prédire le centre.`(the, sat, on) -> cat`- Je suis désolé .
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词──`(the, sat, on) -> cat`Il y a une autre.

Le ski-gramme est plus lent à apprendre, mais il gère mieux les mots rares.

> Le ski-gramme est devenu un choix par défaut.

Le réseau a une couche cachée sans non-linéarité. L'entrée est un vecteur un-chaud sur le vocabulaire. La sortie est un softmax sur le vocabulaire. Après l'entraînement, vous jetez la couche de sortie. Les poids de couche cachée sont les emblèmes.

> 网络有一个不带非线性激活函数的隐藏层――输入是单词表上的一个热向量――输出是单词表上的软max――训练后,你丢弃输出层――隐藏层的权重就是嵌入――

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

Le truc: le softmax de plus de 100 000 mots est trop cher.**negative sampling**Prévoir si ce mot contextuel apparaît près de ce mot central, oui ou non. Prenez une poignée de mots négatifs (non co-occurrents) par paire de formation au lieu de calculer le softmax sur l'ensemble du vocabulaire.

> : pour 100 000 mots faire softmax 代价太高──Word2Vec 使用**负采样（Negative Sampling）**Pour chaque entraînement, il faut prendre en compte la quantité de cas négatifs (la quantité de cas négatifs) plutôt que la quantité de cas négatifs.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
word-vector-arithmetic
```

## Faites-le

### Étape 1: formation des paires à partir d'un corpus

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

Chaque paire (centre, contexte) dans une fenêtre est un exemple de formation positif.

> Chaque mot central dans la fenêtre est un modèle de formation.

### Étape 2: intégration des tables

Deux matrices.`W`est la table d'intégration du mot central (la que vous conservez). `W'`est la table des mots de contexte (souvent rejetée, parfois moyennée avec `W`)

> Deux réactions.`W`C'est le mot qui est resté.`W'`C'est le cas de la première phrase de la phrase.`W`取平均) ⋅

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

La taille du vocabulaire 10k et dim 100 est réaliste; pour l'enseignement, 50 vocabulaires x 16 dim suffisent pour voir la géométrie.

> La taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de

### Étape 3: objectif négatif de l'échantillonnage

Pour chaque paire positive `(center, context)`, échantillon `k`Les mots aléatoires du vocabulaire comme négatifs.`W[center] · W'[context]`est élevé pour les positifs et faible pour les négatifs.

> Pour chaque modèle`(center, context)`, du mot expression dans la phrase`k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`À la fin de la première année,

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

La formule magique: perte logistique sur la paire positive (je veux sigmoïde près de 1) plus perte logistique sur les paires négatives (je veux sigmoïde près de 0). Les gradients coulent vers les deux tables.

> 神奇的公式:正例对上逻辑损失(希望 sigmoid 接近 1)加上负例对上逻辑损失(希望 sigmoid 接近 0) ・・・梯度流向两个表──完整推导见原始论文; si vous voulez le faire comprendre plus profondément, utilisez le papier à l'oreille.

### Étape 4: entraînement sur un corps de jouet

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

Après suffisamment d'époques sur un grand corpus, les mots qui partagent des contextes ont des embrasements centraux similaires. Sur un corpus de jouets, vous voyez l'effet faiblement. Sur des milliards de jetons, vous le voyez de manière spectaculaire.

> Après avoir traversé suffisamment de séries sur le gros langage, les mots partagés sur le texte ci-dessous ont des termes similaires au centre de leur emplacement.

### Étape 5: le truc d' analogie

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

Sur les vecteurs pré-entraînés de 300d Google News:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`Pas parce que le modèle sait ce qu'est la royauté.`(king - man)`capture quelque chose comme "royal", et l'ajouter à `woman`des terres près de la région royale féminine.

> `king - man + woman = queen`Ce n'est pas parce que le modèle sait ce qu'est la chambre, mais parce que le volume.`(king - man)`J'ai pris quelque chose qui ressemblait à la "Royal House", je vais l'ajouter.`woman`À proximité de la région des femmes de la salle des rois.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

L'écriture de Word2Vec à partir de zéro est un enseignement.`gensim`- Je suis désolé .

> De la création à la création Word2Vec est pour l'enseignement.`gensim`Il y a une autre.

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

Pour le vrai travail, vous ne faites presque jamais de Word2Vec vous-même.

> Œuvre réelle, vous ne vous entraînez pratiquement pas Word2Vec──

- **GloVe** L'approche de facteurisation de la matrice de co-occurrence de Stanford. 50d, 100d, 200d, 300d points de contrôle. Bonne couverture générale.
  **GloVe** Le système de décomposition de la matrice commune de Stanford  50 维、100 维、200 维、300 维的检查点──通用覆盖良好──第04 课专讲解 GloVe──
- **fastText** L'extension Word2Vec de Facebook qui intègre des caractères n-grammes.
  **fastText** Word2Vec 扩展,嵌入字符 n-gram──通过组合子词处理词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d, vocabulaire de 3M mots, publié en 2013. Toujours téléchargé quotidiennement.
  **Google News 预训练 Word2Vec** 300 维, 3 millions de mots表, 2013 année de publication.

### Quand Word2Vec gagnera encore en 2026

- Trainer sur des abstracts médicaux en une heure sur un ordinateur portable, obtenir des vecteurs spécialisés sans captures de modèle général.
  En plus de la formation de la résumé médical, il est possible de trouver un modèle général qui ne peut pas être capturé.
- L'ingénierie des caractéristiques de style analogue. `gender_vector = mean(man - woman pairs)`- Soustraire de l'autre mot pour obtenir un axe neutre sur le genre.
  类比式特征工程──`gender_vector = mean(man - woman pairs)`                                                                                                                                                                                                                                                              
- Interprétabilité. 100d est assez petit pour tracer via PCA ou t-SNE et voir en fait des amas de forme.
  可解释性──100 维足够小, peut être utilisé par PCA ou t-SNE 图并实际见聚类形成──
- N'importe où, les inférences doivent être exécutées sur un appareil sans GPU.
  任何需要在没有GPU的设备上运行推理的场景──Word2Vec 查找就是单行获取──

### Lorsque Word2Vec échoue

Le mur polysémique.`bank`a un vecteur. `river bank`et `financial bank`Partagez-le.`table`Un classifiateur en aval ne peut pas distinguer les sens du vecteur.

> Les barrières de la vie`bank`Il n'y a qu'un seul émetteur.`river bank`et `financial bank`Partagez-le.`table`(étiquette électronique vs. appareil) Partagez-le.

Les intégrations contextuelles (ELMo, BERT, chaque transformateur depuis) ont résolu cette question en produisant un vecteur différent pour chaque occurrence du mot en fonction du contexte environnant. C'est le saut de Word2Vec à BERT: de statique à contextuel.

> Le changement de courant de chaque mot est résolu en fonction de la forme de chaque mot qui l'entoure.

Le problème de l'échec du vocabulaire est l'autre.`Zoomer-approved`Si vous avez des informations sur les résultats de formation, vous pouvez les trouver dans les données de formation.

> Le problème est un autre défaut.`Zoomer-approved`Il n'y a pas de plan de préparation pour le projet.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-embedding-probe.md`- Le numéro de la liste:

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## Les exercices

1. **Easy.**Exécutez la boucle d'entraînement sur un petit corpus (20 phrases sur les chats et les chiens).`nearest(vocab, W, W[vocab["cat"]])`Retour `dog`Dans le cas contraire, augmentez les époques ou le vocabulaire.
   **简单。**Dans un petit langage, 20 phrases sur le chat et le chien`nearest(vocab, W, W[vocab["cat"]])`返回的前3中包含 `dog` Si non, augmenter le cycle ou la fréquence
2. **Medium.**Ajouter un sous-échantillonnage de mots fréquents.`10^-5`Les résultats de l'étude ont été analysés dans des groupes de formation avec une probabilité proportionnelle à leur fréquence.
   **中等。**添加高频词子采样──频率高于 `10^-5`Les résultats de l'étude ont été évalués en fonction de la fréquence et de la probabilité de la formation à la mise à l'abandon.
3. **Hard.**Exercer un modèle sur le corpus des 20 groupes de nouvelles.`he - she`et `doctor - nurse`- les mots de l'occupation de projet sur les deux axes. - Rapporte les occupations ayant le plus grand écart de biais.
   **困难。**Dans 20 groupes de nouvelles 语料上训练模型──计算两个偏见轴:`he - she`et `doctor - nurse`将职业词投投投向两个轴上.  Rapporter quelles professions ont le plus grand écart de préjugés.

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les termes clés

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Encore une lecture

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) le papier de prélèvement négatif.
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) la dérivation la plus claire des gradients, si les mathématiques du papier original se sentent denses. / 最清晰的梯度推导, si vous pensez que la mathématique du papier original est trop dense.
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) des réglages de formation de production qui fonctionnent réellement.
