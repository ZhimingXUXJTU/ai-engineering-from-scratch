# GloVe, FastText et les emplacements de sous-parts

> Word2Vec a formé un intégration par mot. GloVe a factorisé la matrice de co-occurrence. FastText a intégré les pièces. BPE a relié aux transformateurs.
> Word2Vec pour chaque mot entraîne un emplacement. GloVe 分解共现矩阵.

> **【中文解读】**GloVe utilise la totalité du courant,FastText 处理子词解决 OOV 问题。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Word2Vec a laissé deux questions ouvertes.

> Word2Vec a laissé deux questions ouvertes:

Premièrement, il y avait une ligne parallèle de recherche qui facturait directement la matrice de co-occurrence (LSA, HAL) plutôt que de faire des mises à jour en ligne de skip-grammes.**GloVe**Il a répondu que: la factualisation de matrice avec une perte bien choisie correspond ou bat Word2Vec, et coûte moins cher à former.

> Premièrement, il existe un chemin de recherche en ligne, directement décomposant la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la**GloVe**回答了: la matrice de la fonction de perte de sélection de couplage de l'émotion est décomposée correspondant ou supérieure à Word2Vec, et le coût de formation est inférieur.

Deuxièmement, aucune méthode n'avait une histoire pour les mots qu'elle n'avait jamais vus. `Zoomer-approved`- Je suis là .`dogecoin`, tout nom propre inventé la semaine dernière, chaque forme inflexion d'une racine rare.**FastText**Il a fixé cela en intégrant des caractères n-grammes: un mot est la somme de ses parties, y compris les morphèmes, donc même les mots hors vocabulaire obtiennent un vecteur sensible.

> Deuxièmement, deux méthodes ne peuvent pas résoudre les problèmes de mots jamais vus.`Zoomer-approved`- Je suis là.`dogecoin`、上周刚造的任何专名词、稀有词根的每变形形式──**FastText**通过嵌入字符n-gram 修复了这个问题: un mot est de ses différentes parties, y compris le langage, de sorte que même les mots extérieurs à la forme du langage peuvent également obtenir une fréquence raisonnable.

Troisièmement, une fois les transformateurs arrivés, la question a changé à nouveau. Les vocabulaires au niveau des mots se limitent à environ un million d'entrées; le langage réel est plus ouvert que cela. **Byte-pair encoding (BPE)**Et ses parents ont résolu cela en apprenant un vocabulaire de fréquents unités de sous-parts qui couvre tout.

> Troisième, lorsque le Transformateur arrive, le problème se transforme à nouveau.**字节对编码（Byte-Pair Encoding, BPE）** et ses variants                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

Cette leçon traverse les trois, puis explique lequel pour quand.

> Il faut expliquer ces trois choses, puis expliquer quand et où.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**GloVe (Global Vectors).**Construire la matrice de co-occurrence mot-mot `X`où `X[i][j]`est la fréquence de la parole `j`apparaît dans le contexte du mot `i`- Les vecteurs de train tels que`v_i · v_j + b_i + b_j ≈ log(X[i][j])`- Le poids est perdu si souvent que les couples ne dominent pas.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, parmi lesquels `X[i][j]`C' est le mot`j`Apprendre le mot`i`Réponse: Le nombre de personnes qui ont été formées à l'école`v_i · v_j + b_i + b_j ≈ log(X[i][j])`◊ Le droit à la perte de plus en plus de pouvoir est souvent négligé.

**FastText.**Un mot est la somme de ses caractères n-grammes plus le mot lui-même. `where`devient `<wh, whe, her, ere, re>, <where>`Le vecteur de mot est la somme de ces vecteurs composants.`whereupon`) sont composés de n-grammes connus.

> **FastText。**Un mot est son caractère n-gramme 之和加上词本身──`where`变成 `<wh, whe, her, ere, re>, <where>`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △  △ △ △ △ △ △    △ △                                                                                                                `whereupon`) à partir de n-grammes connus

**BPE (Byte-Pair Encoding).**Commencez par un vocabulaire de caractères (ou octets) individuels. Comptez chaque paire adjacente dans le corpus. Fusez la paire la plus fréquente dans un nouveau jeton. Répétez pour `k`Les résultats: un vocabulaire de `k + 256`les jetons où des séquences fréquentes (`ing`- Je suis là .`tion`- Je suis là .`the`Les mots rares sont divisés en morceaux familiers.

> **BPE（字节对编码）。**Le nombre de mots dans le langage statistique est le plus fréquent.`k`Je suis en train de faire une autre chose.`k + 256`个标语的词表, parmi lesquelles高频序列(`ing`- Je suis là.`tion`- Je suis là.`the`) est un seul symbole, les rares mots sont divisés en fragments familiers.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
n5-subword-merge
```

## Faites-le

### GloVe: facteuriser la matrice de co-occurrence

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

Deux pièces en mouvement qui méritent d'être nommées.`f(x) = (x/x_max)^alpha`des poids inférieurs très fréquents par paires (comme `(the, and)`L'intégration finale est la somme de `W`(centre) et `W_tilde`(contextes) les tables. La somme des deux est une astuce publiée qui tend à surpasser en utilisant une seule.

> 两个 points à souligner `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`Il est donc possible de modifier le système de calcul de la charge de l'élément de charge.`W`(centre de mots)`W_tilde`(上下文词)表之和──对两者求和和 est une technique déjà publiée, généralement préférable à utiliser seulement l'une d'entre elles──

### FastText: intégrations sensibles aux sous-commentaires

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

Chaque mot est représenté par son ensemble de n-grammes (généralement 3 à 6 caractères).

> Chaque mot est inséré dans le n-gramme de l'entraînement, puis il est inséré dans Word2Vec en utilisant une position de chaque émetteur.

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

Pour un mot invisible, vous obtenez toujours un vecteur tant que certains de ses n-grammes sont connus. `whereupon`actions `<wh`- Je suis là .`her`- Je suis là .`ere`, et `<where`avec `where`, donc les deux atterrissent près l'un de l'autre.

> Pour les mots inconnus, tant que la partie n-gramme est connue, vous pouvez toujours obtenir un émetteur.`whereupon`Avec `where`Partage`<wh`- Je suis là.`her`- Je suis là.`ere`et `<where`Alors, les deux sont en position de proximité.

### BPE: vocabulaire de sous-parts appris

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

La première itération fusionne la paire adjacente la plus courante.`low`- Je suis là .`est`- Je suis là .`tion`) deviennent des jetons uniques et des mots rares se brisent nettement.

> La première fois que je me suis rencontré avec mon voisin, j'ai passé assez de temps après.`low`- Je suis là.`est`- Je suis là.`tion`) est transformé en un seul symbole, rares sont les mots qui se décomposent.

Les véritables jetonneurs GPT / BERT / T5 apprennent des fusions de 30k à 100k. Résultat: tout texte se jetonne dans une séquence de longueurs limitées d'ID connus, aucun OOV jamais.

> Réellement, GPT / BERT / T5 分词器学习 3 000 à 10 000 fois合并── Result: tout texte est classé en séquence de longueur de ligne connue, il n'y aura jamais d'OV──

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

En pratique, vous entraînez rarement vous-même.

> En pratique, tu ne t'entraînes presque pas à toi-même.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

Pour la tokénisation de sous-mot de style BPE à l'ère des transformateurs:

> Pour le Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

Le `Ġ`Le préfixe marque les limites des mots (une convention GPT-2).

> `Ġ`Il est également utilisé pour la définition de la phrase "B" (B) et "B" (B).

### Quand choisir lequel

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-embeddings-picker.md`- Le numéro de la liste:

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## Les exercices

1. **Easy.**On court .`char_ngrams("playing")`et `char_ngrams("played")`- calculer le chevauchement de Jaccard des deux ensembles de n-grammes.`pla`- Je suis là .`lay`- Je suis là .`play`), ce qui explique pourquoi FastText transforme largement les variantes morphologiques.
   **简单。**运行  référencement`char_ngrams("playing")`et `char_ngrams("played")`△ calculer deux n-grammes 集合的Jaccard 重叠度──you should see a lot de partage片段(`pla`- Je suis là.`lay`- Je suis là.`play`), c'est la raison pour laquelle FastText est bien déplacé entre les formes de changements.
2. **Medium.**Extension `learn_bpe`Vous devriez voir une compression rapide au début, en assimilant près de ~2-3 caractères par jeton.
   **中等。**扩展 `learn_bpe`Pour suivre le nombre de caractères, dessinez chaque symbole de chaque symbole.
3. **Hard.**Prenez une formation de 1k sur les œuvres complètes de Shakespeare. Comparer la symbolisation des mots communs contre les noms propres rares. Mesurer les jetons moyens par mot avant et après. Écrire ce qui vous a surpris.
   **困难。**En complément, le nombre de mots combinés par rapport aux mots communs est de 1000 fois supérieur à celui des mots communs.

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les termes clés

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Encore une lecture

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) le papier GloVe, sept pages, toujours la meilleure dérivation de la perte. / GloVe 论文,七页,仍然是损失函数最好的推导──
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) Rapide texte. / Rapide texte 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) le document qui introduit la BPE dans la PNL moderne. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) comment BPE, WordPiece et SentencePiece diffèrent réellement dans la pratique.
