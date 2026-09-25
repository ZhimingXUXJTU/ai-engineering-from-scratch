# Jamba  Transformateur SSM hybride  Jamba  Transformateur SSM mixte

> Les modèles spatiaux d'État (SSM) et les transformateurs veulent des choses différentes. Les transformateurs achètent la qualité à un coût quadratique. Les SSM achètent l'inférence linéaire et la mémoire constante par une récurrence mais un retard qualité. Jamba (mars 2024) et Jamba 1.5 (août 2024) d'AI21 les mettent dans le même modèle: 1 couche transformateur pour chaque 7 couches Mamba, MoE sur chaque autre bloc, et une fenêtre contextuelle de 256k qui s'adapte à un seul GPU de 80 Go. Mamba-3 (ICLR 2026) resserre le côté SSM avec des espaces d'état de valeur complexe et des projections MIMO. Cette leçon explique pourquoi la recette hybride a survécu à trois ans d'évolution alors que les tentatives de long-context pur-SSM et pur-Transformer n'en ont pas.

> **【中文解读】**Transformateur avec une seconde complexité de l'attention pour changer de qualité, SSM avec une logique de temps et des calculs de temps conventionnels, mais avec un faible taux de conversion de la qualité.

> **【拓展：SSM+Transformer→未来架构】**La mise en œuvre de la méthode de transformation de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de la structure de base de base de la structure de base de base de la structure de base de base de la structure de base de base de la structure de base de base de la structure de base de base de la structure de base de base de la structure de base de base de base de la structure de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base

>  **【前置】**Les transformateurs sont les éléments de la structure de l'équipement et de la structure de l'équipement.
>  **【类比】**Jamba = " long-course mémorisation "──Transformer = 短期回忆(精确但贵,每件事都需要注意力);Mamba = 长期回忆(粗略但便宜,用状态缩历史)──1:7 比例 = 偶尔做精确回忆,大多数时候用快速缩记忆──两者结合在 256K 上下文 下下既精确又便宜──

**Type:** Learn
**Languages:** Python (stdlib, layer-mix calculator)
**Prerequisites:** Phase 10 · 14 (open-model architectures), Phase 10 · 17 (native sparse attention)
**Time:** ~60 minutes

## Objectifs d'apprentissage

- Expliquez les trois primitives dans un bloc Jamba  couches transformateur, couches Mamba, MoE  et la recette 1:7: même interlacer.
  解释 Jamba 块中的三个基元Transformer 层、Mamba 层、MoE及 1:7:
- Expliquer à quel point la récurrence d'un SSM ressemble à un niveau élevé et pourquoi elle permet l'inférence de mémoire constante.
  Expliquer comment est la récursion de la MSS sur le plan macro, et pourquoi elle peut réaliser des hypothèses de résistance constante
- Computez l'empreinte cache KV d'un modèle Jamba à 256k de contexte et comparez à ce dont un modèle transformateur pur aurait besoin.
  计算 Jamba 模型在 256K 上下文中的 KV 缓存占用,并与纯变压器 模型对比
- Nombre des trois innovations Mamba-3 (discrétisation exponentielle-trapézoïdale, mise à jour de l'état à valeur complexe, MIMO) et le problème visé par chacune.
  Il s'agit d'une série de problèmes liés à la mise en place d'un système de gestion de la gestion des ressources humaines.

## Le problème , l' introduction du problème

L'attention est quadratique en longueur de séquence. Les modèles d'espace d'état sont linéaires. Cette différence est composée: à 256k jetons, une carte d'attention Transformer est de 65B entrées par tête; l'état récurrent d'un SSM est de taille fixe indépendamment de la longueur de la séquence.

> La différence est très importante après l'accumulation: 256 000 tokens, le diagramme de la transformation de la concentration de la chaîne contient 650 milliards d'articles par tête; l'état de cycle de la chaîne de calcul de la chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de calcul de chaîne de chaîne de calcul de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne de chaîne

Les modèles SSM purs (Mamba, Mamba-2) correspondent à la complexité des transformateurs à petite échelle, mais sont en retard sur les tâches de suivi de l'état et échouent dans certaines catégories de récupération dans le contexte.

> 純SSM 模型(Mamba、Mamba-2) à petite échelle correspondant Transformer 困惑度, mais en retard sur les tâches de suivi de l'état, dans certains cas, la recherche de classe est ratée.

La solution évidente: utiliser les deux. Mettez les couches de Transformer là où le rappel exact compte. Utilisez les couches SSM ailleurs. Ajustez le rapport. Jamba est le premier modèle de production à expédier cette recette hybride à l'échelle (52B au total, 12B actif, 256k contexte, GPU unique de 80 Go). Jamba 1.5 étend la famille à 398B au total / 94B actifs. Mamba-3 (ICLR 2026) est la meilleure base de base de SSM pure actuelle autour de laquelle les hybrides peuvent être reconstruits.

> 显而易见的修复:两者都用──在需要精确回忆的地方放 Transformer层──其他地方使用SSM层──调整比例──Jamba est le premier modèle de production de ce schéma mixte à grande échelle livré(52B 总参数,12B 活跃,256k 上下文,单张 80GB GPU)──Jamba 1.5 将家族扩展到398B 总参数 / 94B 活跃参数──Mamba-3ICLR 2026) est la meilleure pure SSM基线, l'architecture mixte peut être reconstruite autour de elle──

Cette leçon lit les trois articles et produit le modèle mental pour "choisir le bon rapport".

## Le concept de base.

> **【中文解读】**Jamba est un projet de l'AI21 Labs proposé par Mamba, un modèle spatial et étatique mixte de la structure SSM-Transformer, qui fournit une capacité de retrocédation précise à la structure et à la construction de la complexité de la structure.

> **【拓展：SSM 与 Transformer 的融合趋势】**La complexité de la réflexion de Mamba 等 SSM est O(1)(état fixe), tandis que Transformer est O(n)(KV-cache 随序列增长) ・・・Jamba 将两者结合:SSM 处理长程依赖(高效), attention processing needs精确回溯的任务(准确) ・・・ Cette structure mixte peut être la direction future de la réflexion de longue durée 下文 △


### Un SSM en une page

Un modèle spatial d' état traite une séquence `x_1, ..., x_N`par un état de taille fixe `h`- Le numéro de la liste:

```
h_t = A h_{t-1} + B x_t
y_t = C h_t
```

À chaque étape , l' état évolue par une dynamique linéaire .`A`, prend des informations `B x_t`, et émet des sorties `C h_t`- Je suis là .`A, B, C`Il est important de noter la propriété critique:`y_t`seulement besoin `h_{t-1}`et `x_t`Pas plus tôt .`x`La mémoire est constante, l'inférence est O (1) par jeton.

Le truc de la qualité de la modélisation est la structure de`A`. S4 (Gu 2021) a utilisé une matrice très structurée qui pouvait être évaluée efficacement en tant que longue convolutions pendant la formation.`A, B, C`Mamba-2 (2024) a encore simplifié la structure. Mamba-3 (2026) ajoute de nouveau la complexité dans des lieux spécifiques.

La propriété clé: pour un décodeur LLM, une couche SSM est un remplacement déroulant d'une couche attention, avec un état de taille fixe par couche au lieu d'un cache KV en croissance.

### Le bloc de Jamba

Un bloc de Jamba interpose des couches selon deux nombres:

- `l`Le rapport attention-Mamba.`l = 8`, soit 1 couche transformateur pour chaque 7 couches de Mamba (7 Mamba + 1 Attention = 8 couches par groupe).
- `e`: la fréquence MoE.`e = 2`, ce qui signifie que chaque autre couche s'applique à MoE.

La séquence de couches dans un bloc:

```
M  M  M  M  M  M  M  A    (7 Mamba + 1 Attention)
|  M  |  M  |  M  |  M    (where | marks MoE applied)
```

Chaque bloc Jamba est de 8 couches. À 4 blocs de profondeur (32 couches au total), vous obtenez 28 Mamba et 4 couches Attention.

### Pourquoi le rapport 1:7

AI21 a exécuté des ablations: quel rapport attention-à-mamba donne la meilleure perplexité par paramètre ET rappel dans le contexte sur leurs évaluations de long contexte?

- Trop d'attention (1:1): la qualité augmente mais la mémoire et la vitesse se dégradent.
- Trop peu d'attention (1:15): la mémoire est excellente mais la récupération dans le contexte échoue.
- Le point de départ: 1:7 ou 1:8.

L'intuition: les couches Transformer gèrent le rappel exact et le suivi de l'état.

### Codification de position

Les couches de Mamba sont elles-mêmes conscientes de la position (via la récurrence). Les couches d'attention des hybrides originaux à base de Mamba n'ont pas utilisé RoPE  les couches SSM fournies informations de position. Jamba 1.5 ajoute RoPE aux couches d'attention pour une généralisation de contexte plus longue, un raffinement post-hoc basé sur l'évaluation empirique du contexte long.

### Le budget de la mémoire

Pour une forme Jamba-1 (32 couches: 28 Mamba + 4 Attention, 4096, 32 têtes d'attention cachées):

- Cache KV (seulement les couches d'attention): `2 * 4 * 32 * 128 * 256k * 2 = 8.4 GB`Les quatre couches d'attention contribuent.
- État du MSS: `28 * hidden * state_size`par préfixe de jeton, mais c'est une taille fixe par couche, pas en évolue avec la longueur de la séquence.`28 * 4096 * 16 * 2 = 3.7 MB`- Tout à fait.

Comparer à un transformateur pur à 32 couches, le même caché, plein MHA à 32 têtes: `2 * 32 * 32 * 128 * 256k * 2 = 128 GB`En effet, la plupart des modèles 2024 utilisent des modèles de base (environ 8 fois plus de KV) que les modèles de base (environ 8 fois plus de KV).`2 * 32 * 8 * 128 * 256k * 2 = 32 GB`), le hybride 1:7 de Jamba à 16 Go est encore deux fois plus petit.

C'est ce que signifie AI21 par "context 256k sur un seul GPU de 80 Go". Le cache KV d'un transformateur pur à MHA complet ne conviendrait pas; même une ligne de base GQA ne laisse aucune place aux poids et aux activations; Jamba le fait.

### Mamba-3: la ligne de base de la MSS pure en 2026

Mamba-3 (ICLR 2026, arXiv:2603.15569) présente trois innovations sur le côté pur du SSM:

1. **Exponential-trapezoidal discretization.**Remplace la discrétion de la méthode Euler dans Mamba-2 par une récurrence plus expressive.`x_t`- Je suis désolé .

2. **Complex-valued state update.**Les Mamba précédents ont réduit la matrice d'état de complexe (S4) à diagonale réelle (Mamba) à identité à l'échelle (Mamba-2). Mamba-3 ajoute de nouveau des valeurs complexes  équivalentes à une intégration rotative dépendante des données sur l'état. Cela restaure les capacités de suivi de l'état qui coûtent les simplifications précédentes à valeur réelle.

3. **Multi-input multi-output (MIMO) projections.**Au lieu de projections scalaires par fonction, utilisez des projections à valeur de matrice. Améliore la puissance de modélisation et l'utilisation du matériel de temps d'inférence sans augmenter la latence de décode.

À 1,5B, Mamba-3 améliore la précision moyenne en aval de 0,6 points par rapport au Gated DeltaNet; la variante MIMO ajoute 1,2 points de plus pour un gain total de 1,8 points.

Mamba-3 n'est pas encore livré dans un hybride de production à l'échelle  mais c'est le candidat évident pour le côté SSM du prochain modèle de la classe Jamba.

### Quand trouver un hybride

Les hybrides gagnent lorsque:

- Le contexte est assez long pour que le cache KV Transformer pur soit douloureux (64k+).
- Les tâches mélangent structure à courte portée (bon pour SSM) avec rappel à longue portée (necessité de transformateur).
- Vous voulez déployer sur des budgets de mémoire GPU uniques où le cache KV Transformer seul ne conviendrait pas.

Les hybrides perdent lorsque:

- Le contexte est court (moins de 16k).
- Les tâches nécessitent une attention partout-à-tout (réflexion profonde, référence croisée de plusieurs documents).
- Vous êtes en train d'évoluer vers des modèles frontaliers de plusieurs milliards de paramètres. Pure-Transformer + MLA + MoE (style DeepSeek-V3) remporte actuellement la course de capacité.

### Le paysage concurrentiel

| Model | Family | Scale | Unique claim |
|-------|--------|------|-------------|
| Mamba-2 | pure SSM | 3B | linear time, constant memory |
| Jamba | hybrid | 52B/12B | 256k on 80GB |
| Jamba 1.5 Large | hybrid | 398B/94B | enterprise-grade long-context |
| Mamba-3 | pure SSM | 1.5B (paper) | state-tracking restored |
| DeepSeek-V3 | pure Transformer + MoE | 671B/37B | frontier capability |

Le paysage 2026: le MoE transformateur pur domine la frontière, mais les hybrides possèdent la niche contextuelle de 256k plus.


> **【拓展：Mamba/SSM 的优势与局限】**Mamba 推理复杂度 O(1),远优于变压器的 O(n) ・・・ mais SSM est plus faible dans la tâche de retrocédation précisée.


## Utilisez-le avec le cadre de réalisation
```figure
swiglu-ffn
```

## Utilisez-le

`code/main.py`est une calculatrice de mémoire pour les architectures hybrides.

- Le cache KV dans le contexte cible.
- La mémoire de l'état SSM.
- La mémoire totale au contexte N pour une gamme de formes de modèle.

La calculatrice prend en charge:

- L'indice de base de la transformation pure (la cache KV augmente avec N).
- Hybride à style Jamba 1:7
- Le système de gestion des données (SSM) est pur (pas de cache KV du tout).

Les chiffres sont directement tirés des documents Jamba-1 et Jamba-1.5 pour les formes publiées et extrapolés pour les variantes hypothétiques.

Les considérations d'intégration pour un déploiement réel:

- La plupart des serveurs d'inférence de production (vLLM, SGLang) prennent en charge Jamba et Mamba.
- Dans le même VRAM, vous installez plus de séquences Jamba que de séquences Transformer.
- Mamba-3 en tant que modèle autonome n'est pas encore livré en production  recherche prévisualisation à 1.5B.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-hybrid-picker.md`. Compte tenu de la spécification de la charge de travail (profil de longueur de contexte, mix de tâches, budget de mémoire), il recommande de choisir entre un transformateur pur, un hybride de style Jamba et un SSM pur, en raison explicite des compromis entre la mémoire et la qualité.

> 本课产 出 `outputs/skill-hybrid-picker.md` la définition de la durée de la configuration, du composé des tâches, du budget de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la

## Les exercices

1. On court .`code/main.py`Pour calculer le cache KV à 256k context pour un transformateur pur à 32 couches (couches cachées 4096, 32 têtes) et pour un hybride Jamba-1 de la même forme.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`計算 32 層純變壓器 (                                                                                                                                                                                                                                                          

2. Modifier la calculatrice pour modéliser un hybride 1:3 (4 Mamba: 1 Attention) et un hybride 1:15 (14 Mamba: 1 Attention).
   Le calcul de la réserve de KV est calculé en fonction de la réserve de KV.

3. Lisez la section 3 du document Jamba (arXiv:2403.19887). Expliquez pourquoi AI21 utilise Mamba-1 plutôt que Mamba-2 malgré le fait que Mamba-2 soit plus rapide.
   Le texte de l'article suivant est le premier de la série de trois articles de l'étude.

4. Comparer le rapport actif à DeepSeek-V3 (37B/671B) et expliquer pourquoi l'architecture de Jamba pousse le rapport actif plus haut.
   Le nombre de moteurs de recherche de Jamba est de 1,75 B. Le nombre de moteurs de recherche de Jamba est de 1,67 B.

5. Lisez la section 3 du document Mamba-3 (arXiv:2603.15569). Expliquez en trois phrases pourquoi une mise à jour d'état à valeur complexe est équivalente à une intégration rotative dépendante des données.
   Le texte de Mamba-3 est en cours de rédaction et est en cours de rédaction.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| State space model (SSM) | "Recurrence with a fixed state" | A layer with a learned recurrence `h_t = A h_{t-1} + B x_t`; constant memory per token | 状态空间模型，固定状态的递归层 |
| Selective SSM | "Mamba's trick" | Data-dependent A, B, C parameters that give the model gating-like selectivity at linear time | 选择性 SSM，数据依赖的参数实现门控 |
| Attention-to-Mamba ratio | "How many attention layers" | In Jamba, `l = 8` means 1 attention layer per 7 Mamba layers | 注意力与 Mamba 层比例，Jamba 用 1:7 |
| Jamba block | "The 8-layer group" | One attention + seven Mamba + MoE on alternate positions | Jamba 块，1 层注意力 + 7 层 Mamba + MoE |
| SSM state | "The hidden buffer" | Fixed-size per-layer state that replaces the KV cache for Mamba layers | SSM 状态，替代 Mamba 层 KV 缓存的固定大小状态 |
| 256k context | "Jamba's flagship number" | The sequence length Jamba-1 fits on a single 80GB GPU; pure Transformer cannot at that size | 256K 上下文，Jamba-1 在单张 80GB GPU 上的最大序列长度 |
| Mamba-3 | "2026 pure SSM" | Current-best pure-SSM architecture with complex state + MIMO; the baseline hybrids rebuild around | Mamba-3，2026 年最优纯 SSM 架构 |
| MIMO | "Multi-input multi-output" | Mamba-3 innovation using matrix-valued projections instead of scalar per-feature | MIMO，矩阵值投影替代标量投影 |
| Exponential-trapezoidal discretization | "Mamba-3's recurrence" | More expressive recurrence that subsumes Mamba-2's Euler-method discretization | 指数梯形离散化，更高效的递归表达 |
| Hybrid architecture | "Mix attention and SSM" | Any model that interleaves Transformer and SSM layers; Jamba is the production archetype | 混合架构，交替使用 Transformer 和 SSM 层 |

## Encore une lecture

- [Lieber et al. — Jamba: A Hybrid Transformer-Mamba Language Model (arXiv:2403.19887)](https://arxiv.org/abs/2403.19887) le papier Jamba original, ablations de ratio, revendication de contexte 256k
- [AI21 — Jamba 1.5: Hybrid Transformer-Mamba at Scale (arXiv:2408.12570)](https://arxiv.org/abs/2408.12570) la famille de la mise à l'échelle, 398B/94B et 12B/52B publications
- [Gu, Dao — Mamba: Linear-Time Sequence Modeling with Selective State Spaces (arXiv:2312.00752)](https://arxiv.org/abs/2312.00752) le papier sélectif du MSS sur lequel Jamba s'appuie
- [Dao, Gu — Mamba-2 (arXiv:2405.21060)](https://arxiv.org/abs/2405.21060) le successeur simplifié de l'espace État structuré
- [Lahoti et al. — Mamba-3 (arXiv:2603.15569, ICLR 2026)](https://arxiv.org/abs/2603.15569) État à valeur complexe, MIMO, frontière 2026 pure-SSM
- [Gu et al. — Efficiently Modeling Long Sequences with Structured State Spaces (arXiv:2111.00396)](https://arxiv.org/abs/2111.00396) le document S4, point de départ de la généalogie SSM pour les LLM
