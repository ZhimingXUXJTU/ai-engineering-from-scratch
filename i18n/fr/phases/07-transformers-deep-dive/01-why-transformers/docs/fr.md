# Pourquoi les transformateurs  Les problèmes avec les RNN
# Pourquoi est-ce que le problème du Transformer  RNN

> Les RNN traitent les jetons un à la fois. Les transformateurs traitent tous les jetons à la fois. Ce pari architectural unique a changé chaque courbe d'échelle dans l'apprentissage en profondeur après 2017.

> RNN 个别处理代币――Transformer 一次性处理所有代币―― Cette structure a changé chaque section de l'apprentissage en profondeur après 2017.

> **【中文解读】**RNN a trois problèmes mortels: incapacité de parcourir, disparition de la longueur de chemin, boîte de longueur fixe. Le transformateur a utilisé son attention pour résoudre ces trois problèmes et a ouvert une nouvelle ère de l'apprentissage profond.

**Type:** Learn | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objectifs d'apprentissage

- Comprendre les trois faiblesses fatales des réseaux neuronaux récurrents (RNN)
  Il y a trois points faibles de la RNN.
- Expliquez pourquoi la profondeur de série, et non le nombre d'opérations, détermine le temps d'entraînement de la GPU
  解释为什么串行深度 (而不是操作数) a déterminé le temps de formation de la GPU
- Comparer la complexité RNN vs Transformer sur les tâches de modélisation de séquences
  Comparer RNN à Transformer dans la complexité des tâches de construction de séquences
- Identifier les scénarios dans lesquels les RNN ou les modèles spatiaux d'état peuvent encore être préférés
  识别 RNN ou état du modèle spatial encore mieux scène
- Reconnaître le changement de biais inductif de l'attention locale à l'attention mondiale
  ̇ connaissance de la transition de l'attention à la concentration de l'attention à la concentration de l'attention à la concentration totale

## Le problème , l' introduction du problème

Avant 2017, chaque modèle de séquence de pointe sur la planète  langue, traduction, parole  était un réseau neuronal récurrent. Les LSTM et GRU ont obtenu des benchmarks de traduction équivalents à ImageNet pendant une demi-décennie. Ils étaient le seul outil que quelqu'un avait.

> Jusqu'en 2017, chaque modèle de séquence le plus avancé de la planète  langue、 traduction、语音 était un réseau de neurones circulaires. LSM et GRU étaient considérés comme étant le seul outil de tous les humains.

Le calcul séquentiel ne permettait pas de paralléliser l'axe temporel.`t+1`Il faut le secret de l' état de la marque .`t`Une séquence de 1.024 jetons signifiait 1.024 étapes sérielles sur un GPU qui peut effectuer 1.000.000 opérations de points flottants par cycle.

> Ils ont trois faiblesses mortelles.`t+1` besoin de la marque `t`La séquence d'un token de 1,024 signifie que la GPU peut exécuter 1,000,000 fois de calcul de points de sortie par cycle pour exécuter 1,024 étapes de séquence. Sur des matériels conçus pour la simulation, le temps d'entraînement augmente avec la longueur de la séquence.

> **【中文解读】**Le premier point faible mortel: la séquence de calcul. Le RNN doit traiter chaque jeton de manière ordonnée, ne pouvant pas utiliser complètement la capacité de calcul de la GPU.

Les gradients disparus signifiaient que les informations 50 jetons de retour étaient déjà compressées à travers 50 non-linéaires. Les unités récurrentes par voie de fer (LSTM, GRU) ont atténué la dépression mais ne l'ont jamais éliminée.

> Le degré de disparition signifie que 50 tokens  précédents ont été comprimés par 50 unités de cycle contrôlées  LSM  GRU) ont atténué cette pression  mais n'ont jamais éliminé  Long程依赖  " Le livre que j'ai lu l'été dernier sur un avion de Kyoto était... "  souvent échoué ⋅

> **【中文解读】**Le deuxième point faible mortel: la disparition du degré. Après 50 niveaux de changements non liés, l'information est presque complètement perdue.

Les états cachés de largeur fixe signifiaient que l'encodeur comprimait toute la séquence source dans un seul vecteur avant que le décodeur ne voie quoi que ce soit.

> L'état caché de la largeur fixe signifie que le codeur va compresser l'ensemble de la séquence source en un seul volume avant que le codeur ne voie tout le contenu.

> **【中文解读】**Troisième point faible: la largeur fixe du boîtier. Le codeur doit compresser l'ensemble de la séquence source à une longueur fixe du volume.

L'article de 2017 "Attention est tout ce dont vous avez besoin" a proposé quelque chose de radical: supprimer complètement la récurrence. Laissez chaque position attirer chaque autre position en parallèle.

> L'article de 2017 intitulé "Attention Is All You Need" propose un programme dynamique: abandonner complètement le cycle.

Le résultat domine toutes les modalités d'ici 2026. Langue (GPT-5, Claude 4, Llama 4), vision (ViT, DINOv2, SAM 3), audio (Whisper), biologie (AlphaFold 3), robotique (RT-2).

> À l'horizon 2026, ses résultats ont dominé chaque mode de langage: GPT-5, Claude 4 Llama 4.

## Le concept de base.

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**Un RNN compute `h_t = f(h_{t-1}, x_t)`Chaque étape dépend de la précédente.`h_5`avant `h_4`Sur les GPU modernes avec plus de 10 000 cœurs parallèles, cela gaspille 99% du silicium sur une longue séquence.

> **循环即瓶颈。**RNN 计算 `h_t = f(h_{t-1}, x_t)`Chaque étape dépend de l'étape précédente.`h_4`之前计算 `h_5` Avec plus de 10 000 GPU modernes et un cœur de production, cela a coûté 99% de la capacité de calcul des puces.

> **【中文解读】**Le cycle est la nature de la bouteille: chaque étape du calcul dépend du résultat de l'étape précédente. La GPU est capable de milliers d'opérations de synchronisation, tandis que la RNN est capable de ne l'utiliser que pour une petite partie de l'algorithme de la GPU. Le transformateur, en se concentrant sur le traitement de la séquence, réduit la profondeur de la synchronisation de la GPU à O (N) à O (O) [1].

**Attention as a broadcast.**Les calculs de l' attention personnelle `output_i = sum_j(a_ij * v_j)`Pour chaque paire `(i, j)`Tout le matrix d'attention N×N remplit un matmul en lots.

> **注意力即广播。**Autosouciance en même temps pour chaque couple`(i, j)`计算 `output_i = sum_j(a_ij * v_j)`◊ Toute la N×N attention force matricule est remplie en une seule masse matricule multiplication ◊ pas de étapes interdépendantes ◊ GPU 喜欢它

**The speedup is not a constant.**C' est la différence entre `O(N)`profondeur de série et `O(1)`En pratique, les transformateurs s'entraînent 510x plus vite par époque sur le matériel correspondant à N=512, et l'écart s'élargit avec la longueur de la séquence jusqu'à ce que vous atteignez le`O(N²)`paroi mémoire de l'attention (qui Flash Attention a plus tard réparé  voir leçon 12).

> **加速不是常数。**C' est ça .`O(N)`串行深度与 `O(1)`En pratique, en N = 512 sur le matériel de correspondance, le transformateur à chaque époque de la formation est rapide de 5 à 10 fois, et l'écart augmente avec la longueur de la séquence jusqu'à ce que vous rencontrez l'attention.`O(N²)`Une fois la mise en place, il est possible de la modifier.

**What transformers cost.**Les échelles de mémoire d' attention sont:`O(N²)`Pour le contexte 2K, bien. Pour le contexte 128K, vous avez besoin de fenêtres coulissantes, extrapolation RoPE, carreaux d'attention flash, ou variantes d'attention linéaire.`O(N)`Les transformateurs échangent le temps contre la mémoire et gagnent ensuite le temps par le parallélisme.

> **Transformer 的代价。**Attention à la mémoire`O(N²)`Pour les 2K, pas de problème. Pour les 128K, vous devez glisser la fenêtre.`O(N)`Transformer avec l'époque de l'époque, puis gagner le temps.

**The inductive bias shift.**Les transformateurs ne prennent rien en compte.  chaque paire est un candidat à l'attention. C'est pourquoi les transformateurs ont besoin de plus de données pour bien s'entraîner mais à évoluer une fois qu'ils l'ont. Chinchilla (2022) a formalisé ceci: donné suffisamment de jetons, un transformateur bat toujours un RNN d'un nombre de paramètres égal.

> **归纳偏好的转变。**RNN 假设局部性和邻近性──Transformer ne fait aucune hypothèse Chaque paire est un candidat à l'attention── voilà pourquoi Transformer 需要更多数据来训练好,但一旦拥有足够的数据就能扩展得更远──Chinchilla(2022) formalized this point:

> **【中文解读】**Le transfert de la préférence de régulation est la clé du succès du Transformateur. Le RNN est le plus important de tous les paramètres.

> **【拓展：Chinchilla 缩放定律】**Le thèse de Chinchilla de DeepMind (en 2022) prouve que les modèles de données et de données de formation devraient augmenter en proportion. Cela explique pourquoi les modèles de Llama, GPT-4 et autres ont besoin de millions de dollars de données de formation.

## Construisez-le et mettez-le en œuvre.
```figure
rnn-vs-parallel
```

## Faites-le

Aucun réseau neural ici  nous simulons le goulet d'étranglement du noyau numériquement afin que vous puissiez sentir l'écart sur votre ordinateur portable.

> Il n'y a pas de réseau neuronal. On utilise des nombres pour simuler le cœur du boîtier.

> **【中文解读】**Cette section utilise des modèles numériques pures pour vous faire sentir la différence de performance de la chaîne versus la chaîne. La clé est que la profondeur de la chaîne est N, tandis que la profondeur de la chaîne est seulement O(1) ou O(log N) ⋅.

### Étape 1: Mesurer la profondeur de série.

Regardez !`code/main.py`Nous construisons deux fonctions. Une encode une séquence comme une chaîne d'additions (série, comme un RNN). Une encode comme une réduction parallèle (diffusion, comme l'attention).

> 参见 `code/main.py`△ Nous construisons deux fonctions― une pour le code de la séquence pour la chaîne de complémentation △串行, similaire à RNN)― une pour le code de la séquence de complémentation △广播, similaire à attention)― la même mathématique, différentes dépendances △

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

Nous faisons le temps sur les deux séquences jusqu'à 100 000 éléments. La version RNN est O(N) et un seul pipeline de CPU. Même dans Python pur, la réduction de style d'attention la bat à la longueur ≥ 1000 parce que Python `sum()`est mis en œuvre en C et se répète sans frais d'interprétation par étape.

> Nous avons mis en œuvre des calculs sur des séquences de 100 000 éléments. La version RNN est une seule CPU de O(N) 流水线. Même dans le Python pur, l'attention-style 归约在长度 ≥ 1000 时也能胜出, car Python `sum()`Il est utilisé pour réaliser, sans explicateur de génération en génération.

### Étape 2: Compte les opérations théoriques .

Les deux algorithmes ajoutent N. La différence est * profondeur de dépendance*: combien d'opérations doivent se produire séquentiellement avant que la prochaine puisse commencer. RNN profondeur = N. profondeur d'attention = log(N) avec une réduction d'arbre, ou 1 avec un scan parallèle.

> 两种算法都做N 次加法――区别在*依赖深度*:在下一个操作开始之前,必须顺序执行多少操作――RNN深度 = N。注意力深度 = 用树形归约时为 log(N), 用并行扫描时为 1――决定 GPU 时间是深度,而不是操作数――

### Étape 3: Échantillonnage empirique sur les longues séquences

Nous imprimons un tableau de calendrier qui rend l'écart O(N) visible. Sur un ordinateur portable Mac 2026, les séquences sous 1000 éléments sont trop rapides pour mesurer. Les séquences de 100 000 montrent un scan linéaire propre. Étalons cela à un transformateur de 16.384 jetons avec un équivalent LSTM de 12 couches et vous voyez pourquoi l'entraînement de l'horloge murale était un blocage en 2016.

> Nous imprimons un tableau de temps visible de différence O(N) sur Mac  notebook 2026 , la séquence de moins de 1000 éléments est trop rapide et incommensurable.

## Utilisez-le avec le cadre de réalisation

Quand encore choisir un RNN en 2026:

> 2026 年何时仍应选择 RNN:

> **【中文解读】** Bien que Transformer soit le plus souvent le plus populaire, il n'est pas toujours possible de le faire.

> **【拓展：Mamba 与状态空间模型】**Mamba(2023) a réalisé, par le biais d'un mécanisme de sélection de scan, des séquences de construction O(N) de complexité, tout en soutenant la formation de la même ligne.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

Les modèles de l'espace-état (SSM) comme Mamba sont essentiellement des RNN avec une paramétrisation structurée qui leur donne le meilleur des deux: `O(N)`Les tests de réparation de la mémoire de la machine à écrire, de la formation parallèle par le biais d'un scan sélectif. Ils récupèrent 90% de la qualité du transformateur avec une meilleure mise à l'échelle à long contexte.

> 状态空间模型 (SSM) comme Mamba est en fait un RNN structuré et paramétrique, et dispose des deux avantages:`O(N)`扫描内存, 通过选择性扫描实现并行训练―― elles ont retrouvé la qualité de Transformer 90% , tout en ayant une meilleure长上下文扩展性―― 2026 La plupart des expériences de l'année avant de l'expérimentation sont combinées SSM+Transformer 模型(comme Jamba、Samba)  cycle n'est pas éteint, c'est un composant――

## Envoyez-le . Produit .

Regardez !`outputs/skill-architecture-picker.md`. La compétence choisit une architecture pour un nouveau problème de séquence compte tenu de la longueur, du débit et des contraintes budgétaires de formation.

> 参见 `outputs/skill-architecture-picker.md` Cette compétence est destinée à la sélection de nouveaux séquences, à la définition de longueur, de débit et de budget de formation.

> **【拓展：架构选择决策树】**Dans le projet réel, la sélection d'architecture doit prendre en compte plusieurs dimensions: longueur de séquence, retard de mise en œuvre, budget de mémoire, formation de données, déploiement de matériel. Pour la plupart des tâches de PNL, le Transformer décodeur uniquement est la sélection par défaut. Pour la séquence super longue, considérer Mamba ou architecture mixte. Pour la déploiement à la frontière, la RNN/SSM quantifiée peut être plus adaptée.

## Les exercices

1. **Easy / 简单。**Prenez .`rnn_style`de `code/main.py`et remplacer l'état caché scalaire par un vecteur de longueur-64 d'états cachés.
   取 `code/main.py`Le centre`rnn_style`, le volume de l'état caché sera remplacé par le volume d'état caché de la longueur 64 .

2. **Medium / 中等。**Implémenter une somme parallèle de préfixe (scan Hillis-Steele) en Python pur. Vérifiez qu'il produit la même sortie numérique qu'un scan en série sur la longueur 1024.
   Utilisation pure Python pour réaliser et effectuer des analyses de la série.

3. **Hard / 困难。**Porté la réduction de l'attention à PyTorch sur GPU. temps à la fois que vous fouillez la longueur de la séquence de 64 à 65.536.
   La longueur du séquence est de 64 à 65 536 heures pour les deux.

## Les termes clés

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Encore une lecture

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) l'article qui a tué la récurrence dans la PNL traditionnelle.
  Vaswani et d'autres personnes (en 2017) ont mis fin à la principale série de travaux de la PNL.

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) où l'attention est née, boulonné sur un RNN.
  Bahdanau, Cho, Bengio(2014)  Attention où naît, ajouté à RNN 上。

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) le papier LSTM original, pour le compte rendu.
  Le projet de loi de l'Union européenne sur les droits de l'homme (LSTM) est un projet de loi de l'Union européenne sur les droits de l'homme.

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) Réponse récurrente moderne aux transformateurs.
  Gu, Dao(2023)  Le cycle moderne de transformateur

> **【拓展："Attention Is All You Need" 的历史影响】**Vaswani et d'autres ont non seulement résolu le problème de la fusion de RNN, mais ont également provoqué une révolution de la mode. De BERT(2018) à GPT-4(2023), de ViT(2020) à AlphaFold 2(2021), l'architecture transformatrice est devenue un module de base de l'IA moderne.
