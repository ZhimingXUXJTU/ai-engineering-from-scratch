# Attention Variantes  Fenêtre coulissante, épargne, différentielle  Attention variable  Fenêtre glissant 稀疏 差分注意力

> Chaque jeton voit chaque jeton, et la mémoire paie le prix.

> **【中文解读】**La démarche de la réflexion est de réduire la complexité.

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Coûts de l' attention totale `O(N²)`mémoire et `O(N²)`Pour un Llama 3 70B de 128K, qui est 16 milliards d'entrées d'attention par couche, par 80 couches.`O(N²)`la mémoire d'activation mais ne change pas le coût arithmétique  chaque jeton continue de servir tous les autres jetons.

> L'attention totale est portée à la mémoire et au coût de calcul sur la longueur des séquences.`O(N²)`Pour 128K, c'est le Llama 3 70B, c'est 160 milliards d'attentions par couche, multiplié par 80 couches.`O(N²)`Le coût de chaque jeton est toujours le même.

Trois classes de variantes modifient la topologie de la matrice d'attention elle-même:

> Trois types de variables ont modifié la structure de la matrice d'attention elle-même:

1. **Sliding window attention (SWA).**Chaque jeton est à la fenêtre fixe des voisins, pas le préfixe complet.`O(N · W)`où `W`Je suis la fenêtre, Gemma 2/3, les premières couches du Mistral 7B, Phi-3-Long.
   Le mot grec traduit par " le mot grec "**滑动窗口注意力 (SWA)。**Chaque jeton se concentre uniquement sur le voisinage de la fenêtre fixe, et non sur l'ensemble de la surface.`O(N · W)`, parmi lesquels `W`Il est à la grandeur de la fenêtre.
2. **Sparse / block attention.**Seules les paires sélectionnées `(i, j)`Les autres sont obligés de ne pas peser.
   Le mot grec traduit par " le mot grec "**稀疏/块注意力。**只有选定的 `(i, j)`Pour être évalué, le reste est obligé de se faire passer pour un poids de zéro.
3. **Differential attention.**Compute deux cartes d'attention avec des projections Q/K distinctes, en soustraisant l'une de l'autre.
   Le mot grec traduit par " le mot grec "**差分注意力。**Avec un Q/K indépendant 投影计算两个注意力图,将一个从另一个减去――消除将权重汇聚到前几个代币的"注意力汇聚"现象――Microsoft's DIFF Transformer(2024)。

Un modèle frontalier de 2026 les mélange souvent: la plupart des couches sont SWA-1024, chaque cinquième est une attention globale complète, et une poignée sont des têtes différentielles qui nettoient la récupération.

> Ils peuvent coexister. Un modèle avant-coureur de 2026 est généralement utilisé en combinaison: la plupart des niveaux sont SWA-1024, chaque 5ème niveau est l'attention totale de l'ensemble du cours, une minorité est la différence de recherche de nettoyage.

> **【中文解读】**三种降低注意力复杂度的方法:(1) 滑窗口(SWA) 只关注局部邻域,O(N*W) 复杂度;(2) 稀疏/块注意力只计算选定的代币对;(3) 差分注意力两组 Q/K 注意力相减,消除"注意力汇聚"现象──2026年模型通常混合使用这些变体──

## Le concept de base.

### Attention à la fenêtre coulissante (SWA)

Chaque requête à position `i`ne prend part qu'à des postes dans `[i - W, i]`(SWA de cause à effet) ou `[i - W/2, i + W/2]`Les jetons à l' extérieur de la fenêtre se retrouvent`-inf`dans la matrice de score.

> La position`i`Chaque requête est soumise à un seul intérêt.`[i - W, i]`(因果 SWA) ou `[i - W/2, i + W/2]`Localisation dans la zone de référence:`-inf`Il y a une autre.

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

Pour `N = 8192`et `W = 1024`, la matrice de score a 1024 × 8192 rangées non zéro dans l'attente  une réduction de 8 ×.

> Pour le`N = 8192`et `W = 1024`Le nombre de références de référence est réduit de 8 fois par rapport à 1024 × 8192 ′ non-零行

**KV cache shrinks with SWA.**Seulement la dernière .`W`Les jetons de K et V doivent être conservés par couche. Pour une configuration Gemma-3-ish (1024 fenêtre, contexte 128K), le cache KV tombe 128x.

> **KV 缓存随 SWA 缩小。**Chaque couche doit être conservée pour la dernière K et V.`W`个 token──对于类 Gemma-3 的配置(1024 窗口,128K 上下文),KV 缓存减少 128 倍──

**Quality cost.**Les transformateurs SWA seulement ont du mal à récupérer à longue portée. La solution: interdire les couches SWA avec des couches d'attention pleine. Gemma 3 utilise 5:1 SWA:global. Mistral 7B utilise une pile SWA causale où l'information "fluit vers l'avant" à travers des fenêtres superposées  chaque couche étend le champ réceptif efficace par `W`, et après `L`couches que le modèle peut assister `L × W`Les jetons sont de retour.

> **质量代价。**純 SWA Transformer 在长距离检索上表现不佳──修复方案:将 SWA 层与全注意层交换使用──Gemma 3 使用 5:1 的 SWA:全局比例──Mistral 7B 使用因果 SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`- Je suis désolé .`L`Le modèle de la couche est rétroactif.`L × W`Un signe.

### Attention à l' épargne / blocage

Choisissez une`N × N`Le modèle de sparsité à l'avance.

> 预先选择  référencement`N × N`Les trois formes classiques:

- **Local + strided (OpenAI sparse transformer).**Attends le dernier .`W`des jetons plus tous `stride`- Le symbole de la première fois.`O(N · sqrt(N))`- Je ne sais pas.
  Le mot grec traduit par " le mot grec "**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后 `W`个标志加上之前每隔 `stride`- Je suis un symbole.`O(N · sqrt(N))`La quantité de calcul permet de capturer simultanément des informations locales et longues distances.
- **Longformer / BigBird.**Fenêtre locale + petit ensemble de jetons globaux (p. ex. `[CLS]`) qui assurent la participation de tous et sont assurés par tous + liens aléatoires.
  Le mot grec traduit par " le mot grec "**Longformer / BigBird。**局部窗口 + 少量全局 token(如 `[CLS]`) avec tous les symboles 双向关注 + 随机稀疏连接―― l'expérience montre que la description se développe 2 fois sous la même qualité――
- **Native Sparse Attention (DeepSeek, 2025).**Apprenez quelles sont les blocs de `(Q, K)`Il faut passer les blocs zéro au niveau du noyau.
  Le mot grec traduit par " le mot grec "**原生稀疏注意力（DeepSeek，2025）。**Apprendre à faire`(Q, K)`块重要;在内核级别跳过零块──与 FlashAttention 兼容──

L'attention épargnée est une histoire d'ingénierie du noyau. Les mathématiques sont simples (masquer la matrice de score); le gain vient de ne jamais charger les entrées zéro dans SRAM. FlashAttention-3 et l'API 2026 FlexAttention rendent les modèles épargnées personnalisés de première classe dans PyTorch.

> 稀疏注意力 (RAR) est une histoire d'ingénierie nucléaire. La mathématique est très simple.

> **【拓展：滑动窗口的信息传递机制】**L'attention de la fenêtre de glissement semble seulement capter l'information locale, mais à travers plusieurs couches de compilation, l'information peut "percer" à une position plus éloignée. L'attention de la fenêtre de la fenêtre de l'échelle W, efficace pour le sens de l'image L×W, par exemple W=1024、 L=32 modèle efficace pour le sens de l'image 32K jeton. Mistral 7B a utilisé cette caractéristique en maintenant O(N*W)  calcul complexité en même temps de réaliser la longueur de la construction de l'image.

### L'attention différentielle (transformateur DIFF, 2024)

L'attention régulière a un problème de "sink attention": softmax force chaque rangée à s'ajouter à 1, de sorte que les jetons qui ne veulent pas prendre en charge quoi que ce soit en particulier dépôt le poids sur le premier jeton (ou les premiers).

> 標準注意力有"注意力汇聚" problème:softmax 强制每行总和为 1,所以不想关注任何特定内容的代币会重量倾倾倒到第一代币(或前几个) ;; ceci a volé la capacité de contenu qui devait être utilisé pour le vrai contenu。

L' attention différentielle résout cela en calculant **two**cartes d'attention et soustraction:

> 差分注意力通过计算**两个**Attention à ce que vous faites:

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

où `λ`est un écalier appris (typiquement 0,50,8). A1 capture des poids de contenu réels; A2 capture le lavabo.

> Parmi eux `λ`A1 捕获真实内容权重; A2 捕获汇聚──相减消除汇聚,将权重重新分配给相关代币──

Résultats rapportés (Microsoft 2024): 510% de perplexité moindre, 1,52x de plus de contexte efficace à la même longueur formée, récupération plus nette de l'aiguille dans le paquet de foin.

> 報告結果(Microsoft 2024):困惑度降低 5-10%,同训长度下有效上下文长度增加1.5-2倍,needle-in-haystack 检索更精确──

> **【中文解读】**差分注意力创新之处: 标准注意力因软max 归归化导致"注意力汇聚" (attention sink) 不相关的代币 放重重重集中在序列开头的代币 上。差分注意力计算两组注意力并相减,A1 捕获真内容权重,A2 捕获汇聚噪音,相减后消除汇聚现象──困惑度降低 5-10%──

> **【拓展：Gemma 3 的混合注意力策略】**Google Gemma 3 utilise 5:1 pour le ratio de la vitre de glissement et de l'attention globale à chaque 5 niveaux de l'attention locale.

### Comparaison variée

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Construisez-le et mettez-le en œuvre.
```figure
gqa-kv-sharing
```

## Faites-le

Regardez !`code/main.py`Nous mettons en œuvre un comparateur de masques causaux qui montre l'attention totale, SWA, locale + stridée et différentielle côte à côte sur une séquence de jouets.

> 参见 `code/main.py` Nous avons réalisé un comparateur de masquage des causes, qui montre l'attention totale, la SWA, le niveau local, les progrès et les différences dans la séquence des jouets

### Étape 1: masque causal complet (ligne de base)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Ligne de base de la leçon 07. Triangulaire inférieur; poids nul au-dessus de la diagonale.

> 第07 课的基线──下三角;对角线上权重为零──

### Étape 2: masque causal de la fenêtre coulissante

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

Un paramètre  `window`Pour ...`window >= n`Vous récupérez l'attention causale complète.`window = 1`Chaque jeton ne sert que lui-même.

> Un paramètre`window`Je suis là.`window >= n`时, récupérer pour l'attention de l'ensemble de l'effet.`window = 1`Chaque signe se préoccupe de lui-même.

### Étape 3: masque local + masque à poids faible à pas

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

Une fenêtre locale dense plus chaque fenêtre .`stride`Le champ réceptif se développe en étapes de journaux avec des couches supplémentaires.

> 密集局部窗加上从序列开头每隔`stride`个标语──感受野随着数层以对数步长的增长──

### Étape 4: attention différentielle

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

Deux passes d'attention, soustraire avec un coefficient de mélange appris. Dans le code, nous comparons la carte thermique attention-sink de unique versus différentiel et regarder l'évier s'effondrer.

> ∆2 attention calcul, en réduisant les facteurs mixtes apprises. Dans le code, nous comparons l'attention unique à l'attention différente, en observant l'élimination du phénomène de l'attention.

### Étape 5: Tailles de cache KV

Imprimez la taille du cache par couche à `N = 131072`Les variantes SWA et les variantes rares diminuent de 10 à 100 fois.

> 打印 `N = 131072`时每种变体每层缓存大小──SWA 和稀疏变体减少10-100倍──差分变体翻倍──要有意识地管理你的内存开销──

## Utilisez-le avec le cadre de réalisation

Modèles de production 2026:

> Modèle de production de 2026:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

FlexAttention dans PyTorch 2.5+ accepte une fonction de masque:

> PyTorch 2.5+ 中的 FlexAttention  acceptée de la fonction cache:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

Cela se compile à un noyau Triton personnalisé. Dans les 10% de la vitesse FlashAttention-3 pour les modèles communs, et la fonction de masque est un Python appelable.

> Ceci se traduit par Triton 内核. Pour le modèle habituel, la vitesse est à 10% de FlashAttention-3, et la fonction cache est un objet Python pouvant être modifié.

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** chaque couche jusqu'à ~ 16K de contexte, ou lorsque la qualité de récupération est primordiale.
  Le mot grec traduit par " le mot grec "**纯全注意力** Chaque couche est utilisée jusqu'à environ 16K sur la page ci-dessous, ou en cas de réception.
- **SWA + global mix** long context (> 32K), formation et inférence liées à la mémoire.
  Le mot grec traduit par " le mot grec "**SWA + 全局混合** 长上下文(>32K), formation et recommandation de prise en compte
- **Sparse block attention** noyau personnalisé, modèle personnalisé. réservé aux charges de travail spécialisées (retrait, audio).
  Le mot grec traduit par " le mot grec "**稀疏块注意力** 自定义内核,自定义模式──专用于特殊工作负载(检索、音频)──
- **Differential attention** toute charge de travail où la contamination par la prise d'attention fait mal (RAG à long contexte, aiguille dans un tas de foin).
  Le mot grec traduit par " le mot grec "**差分注意力** Attention 汇聚污染有害的任何工作负载(长上下文 RAG、nédlé dans le paquet de foin)

## Envoyez-le . Produit .

Regardez !`outputs/skill-attention-variant-picker.md`. La compétence choisit une topologie d'attention pour un nouveau modèle compte tenu de la longueur du contexte cible, des exigences de récupération et du profil de calcul de formation/inférence.

> 参见 `outputs/skill-attention-variant-picker.md` Cette compétence  en fonction de la longueur de l'objectif, de la demande et de la formation/de la mise en place de la méthode de calcul, pour le nouveau modèle de sélection de l'attention à la promotion 

## Les exercices

1. **Easy.**On court .`code/main.py`- Vérifiez la SWA à l' adresse `window=4`- Il n'y a pas de code de la ligne de débit.`window=n`reproduit l'attention causal complète de manière bit-identique.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` vérification `window=4`Le SWA va mettre en place tous les contenus de chaque dernière 4 jetons.`window=n`能逐位复现全因果注意力──
2. **Medium.**Implémentation de l' SWA de causalité avec `window=1024`En train de 1000 pas sur Tinyshakespeare, combien de valence perd la récession par rapport à l'attention totale ?
   En français traduit par " dans le programme de formation à la formation professionnelle "`window=1024`En effet, les résultats de la formation sont:
3. **Hard.**Implémenter un mélange de couches 5:1 de style Gemma-3 (5 SWA, 1 global) dans le modèle de capstone. Comparer la perte, la mémoire et la qualité de génération contre les lignes de base pur-SWA et pur-global à des paramètres correspondants.
   Le modèle de projet de formation a été réalisé dans le cadre de la mise en œuvre de la classe Gemma-3 à 5:1 de la combinaison de 5 niveaux SWA ∞ 1 de la totalité de la structure.
4. **Hard.**Mettre en œuvre une attention différentielle avec un apprenant `λ`Les résultats de la recherche sont les suivants:
   Le chinois traduit par " réaliser chaque tête avec une formation ".`λ`Les résultats de la recherche sont les suivants:

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Encore une lecture

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) le papier canonique de vitre coulissante + le papier de jeton global.
  Traduction anglaise: Longformer 论文, classique de la fenêtre de mouvement + 方案 全局代币
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062) local + mondial + aléatoire.
  Le texte de la première partie de la série est le suivant:
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) Le modèle local+réciproque d'OpenAI.
  Le référencement à l'écriture de la langue française est un langage de langue française.
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) le mélange 1:1 SWA:global.
  Le texte de la première partie est le texte de la première partie.
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) le mix 5:1 avec window=1024 qui est maintenant le manuel par défaut.
  Le rapport technique de Gemma 3 est de 5,1 混合, window = 1024, déjà devenu un enseignement.
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) papier transformateur DIFF.
  Le transformateur DIFF est un transformateur de transformateur.
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089) L'attention de l'apprentissage de la sparsité de DeepSeek-V3.2.
  Le thème de la recherche est "DeepSeek-V3.2".
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) Reference API pour le modèle de masque comme appel dans Utilisez-le.
  Le code de la société est le code de la société.
