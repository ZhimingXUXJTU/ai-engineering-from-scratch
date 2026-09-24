# Une attention à plusieurs têtes
# Une attention particulière

> Un chef d'attention apprend une relation à la fois, huit têtes apprennent huit têtes sont libres, prenez-en plus.

> Une attention première à apprendre une relation.

> **【中文解读】**Les différents types de relations sont également concernés: la structure du langage, la structure du langage, la position, etc.

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Une seule tête d'attention à soi compute une matrice d'attention. Cette matrice capture un type de relation  généralement celle qui minimise la perte sur quoi que ce soit le signal d'entraînement. Si vos données ont un accord sujet-verbe, une co-référence, un discours à longue portée et un chunking syntaxique tous enracinés ensemble, une seule tête les épluche dans une seule distribution de max douce et perd la moitié du signal.

> 单个自注意头计算一个注意矩阵――这个矩阵捕获一种关系通常是最小化训练信号损失的那种种――如果你的数据中的主题一致、共指消解、长程语篇和句法分块纠在一起,单个头会模糊它们成单软max 分布,丢失半信号――

La correction du papier Vaswani 2017: exécuter plusieurs fonctions d'attention en parallèle, chacune avec ses propres projections Q, K, V, et concatener les sorties. Chaque tête fonctionne dans un sous-espace de dimension plus petit `d_model / n_heads`Les paramètres totaux restent les mêmes.

> Révision du thèse Vaswani 2017:并行运行多个注意力函数, chacun a sa propre Q、K、V 投影, puis le拼接输出──每个头在维度为`d_model / n_heads`Les résultats de l'étude ont été obtenus en 1er janvier.

L'attention multi-tête est la norme par défaut de chaque transformateur dans les navires de 2026. Le seul argument est sur * combien de têtes* et si les touches et les valeurs partagent des projections (attention groupée, attention multi-quéret, attention latente multi-tête).

> L'unique débat est sur le nombre de titres et la valeur de la projection partagée (à savoir si le groupe de recherche a un nombre de titres et si le groupe de recherche a un nombre de titres).

> **【中文解读】**Le concept de l'attention est le suivant: avec plusieurs concentrations de l'attention indépendantes, chaque tête apprend différentes relations dans un espace différent, l'option finale est mélangée.

## Le concept de base.

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**Prenez .`X`de forme `(N, d_model)`- Projet à Q, K, V de forme`(N, d_model)`- Ressoufflez-vous .`(N, n_heads, d_head)`où `d_head = d_model / n_heads`- Transposer à`(n_heads, N, d_head)`- Je suis désolé .

> **拆分。**取形为 `(N, d_model)``X`◊ projetés à différentes formes`(N, d_model)`Il y a aussi des réactions négatives.`(N, n_heads, d_head)`, parmi lesquels `d_head = d_model / n_heads`                                                                                                                                                                                                                                                              `(n_heads, N, d_head)`Il y a une autre.

**Attend in parallel.**Exécutez des produits à l'échelle de points à l'intérieur de chaque tête.`(N, d_head)`Les têtes fonctionnent sur différents sous-espaces de l'embedding et ne parlent jamais pendant le calcul de l'attention lui-même.

> **并行计算注意力。**Dans chaque tête, le fonctionnement se réduit en points de concentration.`(N, d_head)`: Les opérations sur différents espaces de l'établissement, ne communiquent pas entre eux pendant le calcul de l'attention.

**Concatenate and project.**Les têtes de pile retournent à `(N, d_model)`et multiplier par une matrice de sortie apprise `W_o`de forme `(d_model, d_model)`- Je suis là .`W_o`C'est là que les têtes se mélangent.

> **拼接并投影。**La tête sera rassemblée en`(N, d_model)`et multiplié par la matrice de sortie de l'apprentissage`W_o`, forme pour`(d_model, d_model)`Il y a une autre.`W_o`C'est un lieu où on peut se mélanger.

**Why it works.**Chaque tête peut se spécialiser sans rivaliser avec les autres pour le budget représentatif. Les études de sondage de 2019 à 2024 montrent des rôles distincts de tête: les têtes positionnelles, la tête qui assiste au jeton précédent, les têtes de copie, les têtes d'entité nommée, les têtes d'induction (qui sous-tendent l'apprentissage dans le contexte).

> **为什么有效。**Chaque titre peut être spécialisé sans rivaliser avec les autres titres pour représenter le budget. Une étude de recherche de 2019-2024 montre différents rôles de titre: position tête, attention à un titre précédent, réplique tête, nomme tête de corps, attribution tête.

> **【中文解读】**三步走:Split(拆分到多个子空间)→ Attend(每个头独立做注意力)→ Concat+Project(拼接并通过 W_o 混合)。关键洞察: chaque tête dans différents子空间 indépendante travail, non-chombrant pour représenter les ressources。 L'expérience montre que différents头确实学会了不同的"职责"。

> **【拓展：GQA 在 Llama 3 中的实际应用】**Llama 3 70B utilise 64 têtes de requête mais seulement 8 têtes de KV, le KV 缓存压缩8倍―― ceci permet d'économiser une grande quantité de stockage, tout en évitant presque de perdre la qualité du modèle―GQA est devenu l'échantillon du modèle ouvert de 2024-2026―DeepSeek-V2  MLA 

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA est la norme par défaut moderne car elle réduit la mémoire KV-cache d'un facteur de `N/G`MLA va plus loin en comprimant K/V dans un espace latent, puis en le projetant à l'heure de calcul  coûte FLOPs, économise beaucoup plus de mémoire.

> GQA est une option moderne, car elle réduira la KV 缓存内存 `N/G`En plus de cela, le MLA réduit le K/V à un espace caché plus loin, puis, en calculant, le projet revient à la charge de FLOP, économisant plus de stockage.

## Construisez-le et mettez-le en œuvre.
```figure
multihead-split
```

## Faites-le

### Étape 1: séparer les têtes de l'attention à tête unique que nous avons déjà. Étape 1: Débrancher l'attention de la tête unique existante.

Prenez le `SelfAttention`Leur résultat est le résultat de la leçon 02 et de l'envelopper avec une paire de fractionnement/concétation.`code/main.py`pour une mise en œuvre numpy; la logique est:

> 取第 02 课的 `SelfAttention`, avec le décomposé / le coupé pour l'emballage.`code/main.py`中的 numpy 实现;逻辑如下:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

Une remodèle et une transposition, pas de boucle, c'est exactement ce que fait PyTorch sous`nn.MultiheadAttention`- Je suis désolé .

> Une fois de remodeler et une fois de transposer. Pas de cycle.`nn.MultiheadAttention`Ce que fait le bas de la planche.

> **【中文解读】** `split_heads`et `combine_heads`                                                                                                                                                                                                                                                              

### Étape 2: Exécuter l'échelle de point-produit attention par tête

Chaque tête obtient sa propre tranche de Q, K, V. L'attention devient un matmul en lots:

> Chaque tête obtient son propre Q、K、V 切片── attention à devenir la masse de la matrice multiplicative:

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

Sur du matériel réel .`Qh @ Kh.transpose(...)`est un`bmm`La GPU voit une seule forme de matmul .`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`- Ajouter des têtes est gratuit.

> Sur le vrai matériel,`Qh @ Kh.transpose(...)`C' est une fois `bmm`◊GPU 看到的是形状为 `(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Le nombre de personnes qui ont été déplacées dans le secteur de l'électricité est de 0,5% en moyenne.

### Étape 3: Variante de l'attention de la requête groupée . Étape 3:

Seules les projections de clé et de valeur changent.`n_heads`les groupes; K et V obtiennent `n_kv_heads < n_heads`les groupes et sont répétés pour correspondre:

>  seulement la projection de la clé et de la valeur change.`n_heads`个组; K 和 V 有 `n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

En conséquence , cela permet d' économiser la mémoire , car seulement`n_kv_heads`Les copies sont en direct dans le cache KV, pas `n_heads`Llama 3 70B utilise 64 têtes de requête avec 8 têtes KV  un rétrécissement de cache 8x.

> En réfléchissant, ça économise la mémoire, parce que seulement`n_kv_heads`份副本 existent dans KV 缓存中, plutôt que `n_heads`份──Llama 3 70B Utilisation de 64 têtes de requête et 8 têtes de KV 8 倍 de réduction de la réserve ⋅

> **【拓展：MQA/GQA 在推理中的内存节约】**KV 缓存大小与 KV 头号成正比──Llama 3 70B utilise 64 查询头, mais seulement 8 KV 头, KV 缓存将压缩8倍──对 128K 上下文,这意味着节省数 GB 显存──这是大模型长上下文推理的关键优化GQA 几乎不损质量,但显著降低推理成本──

### Étape 4: Découvrez ce que chaque tête a appris

Exécutez MHA sur une phrase courte avec 4 têtes.`(N, N)`Vous verrez différentes têtes choisir différentes structures même avec l'initialisation aléatoire qui est en partie le signal, en partie la symétrie rotative dans les sous-espaces.

> Dans un court article, on utilise 4 pages pour faire fonctionner le MHA.`(N, N)`Attention à la réaction. Vous verrez même en utilisant l'initialisation au hasard, différents têtes choisiront également différentes structures.

## Utilisez-le avec le cadre de réalisation

Dans PyTorch, la version à une ligne:

> PyTorch 中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

GQA à partir de PyTorch 2.5+:

> GQA(PyTorch 2.5+):

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**Règles générales des modèles de production en 2026:

> **多少个头？**Loi sur l'expérience de production modèle 2026:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`Il est l'unité de la quantité qu'une tête peut "voir".`sqrt(d_head)`Si vous dépassez 256 points, vous perdez le bénéfice "beaucoup de petits spécialistes".

> `d_head`                                                                                                                                                                                                                                                              `sqrt(d_head)`冲突; plus de 256 时, vous avez perdu les avantages de "many小专家"

## Envoyez-le . Produit .

Regardez !`outputs/skill-mha-configurator.md`. La compétence recommande le nombre de têtes, le nombre de têtes kv et la stratégie de projection pour un nouveau transformateur, compte tenu du budget des paramètres, de la longueur des séquences et de l'objectif de déploiement.

> 参见 `outputs/skill-mha-configurator.md` Cette compétence est donnée à la nouvelle transformatrice  recommandation de numéros de titres  KV  et stratégie de projection, à la définition de paramètres budgétaires  longueur de séquence et objectifs de déploiement 

## Les exercices

1. **Easy / 简单。**Prenez le MHA de `code/main.py`et le changement `n_heads`de 1 à 16 avec `d_model=64`Une fois que vous avez terminé, vous pouvez faire une copie synthétique.
   取 `code/main.py`Le MHA, dans le`d_model=64`Dans des conditions déterminées,`n_heads`De 1 à 16 ⋅ Perte de modèle à couche de type micro sur une tâche de copie synthétique ⋅ Perte de modèle à couche de type micro ⋅ Plus de titres ⋅ Aide à atteindre la période de mise en œuvre ou nocifs ?

2. **Medium / 中等。**MQA (un seul KV partagé sur tous les têtes de requête). Mesurer combien de paramètres du compte de gouttes par rapport à MHA complet. Comptez combien la taille de la caisse KV se réduit à l'inférence pour N = 2048.
   实现 MQA(un KV 头在所有查询头间共享) ――测量与完整MHA相比参数下降多少──计算在N=2048的推理时 KV 缓存大小缩减多少──

3. **Hard / 困难。**Mettez en œuvre une version minuscule de l'attention latente multi-tête: comprimant K, V à un rang-`r`Laissez-le dans le cache KV, décomprimez-le à l'heure de l'attention.`r`la mémoire cache passe-t-elle en dessous de 1/8 de la MHA complète tandis que la qualité reste à l'intérieur de 1 bit de la validation ?
   实现迷你版的多头潜伏注意:将 K,V 压缩为秩 `r`En effet, les données de l'équipe de recherche sont en train de se dérouler en fonction de la valeur de l'équipe de recherche.`r`La valeur de la cache cache descend à 1/8 de la MHA complète, tout en maintenant la qualité en 1 bit de confusion de l'essai.

## Les termes clés

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Encore une lecture

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) la spécification originale de plusieurs têtes.
  Vaswani et d'autres personnes (en 2017)

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) le document MQA.
  Shazeer(2019)  MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) comment convertir l'AMM en GQA après la formation.
  Ainslie 等人(2023)  训练后如何将 MHA 转换为 GQA。

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA et pourquoi il bat MHA/GQA sur la mémoire cache.
  DeepSeek-AI (en 2024) MLA 及为何在缓存内存上击败 MHA/GQA

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) Regardez mécaniquement ce que font réellement les têtes.
  Il s'agit d'une analyse du mécanisme des fonctions réelles.

> **【拓展：Induction Heads 与上下文学习】**Les résultats de la recherche anthropologique ont révélé que la capacité d'apprentissage littéraire de Transformer (en cours de contexte) est principalement réalisée par un type de "tête d'induction" appelé attention tête.
