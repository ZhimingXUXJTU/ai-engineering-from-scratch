# Attention à la recherche de la NSA.

> Avec les 64k, l'attention consomme 70 à 80% de la latence de décode. Chaque laboratoire de modèle ouvert a un plan pour le réparer. La NSA de DeepSeek (ACL 2025 best paper) est celle qui a collé: trois branches d'attention parallèles  jetons à grains grossiers compressés, jetons à grains fins retenus sélectivement, et fenêtres coulissantes pour le contexte local  combinées à travers une passerelle apprise. Il est aligné sur le matériel (friendly au noyau), entraîneur natif (fonctionne dans la pré-entraînement, pas en boulon à l'inférence), et sur 64k décodeur il fonctionne plus rapidement que FlashAttention tout en correspondant ou battant la qualité de l'attention totale. Cette leçon construit les trois branches de bout en bout et montre pourquoi la rareté est différenciable de bout en bout.

> **【中文解读】**64K token 时注意力消耗 70-80% de解码延迟──DeepSeek NSA(ACL 2025 最佳论文) avec trois articles et suivi attention分支解决: compresser grosseur de jeton、 choisir de conserver petit grain jeton、滑窗局部上下文, via可学习门控组合──硬件友好、可预训、比FlashAttention更快──

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K token) est la capacité centrale du grand modèle 2025-2026 years;;NSA、MHA、GQA sont des solutions de réduction de la complexité de calcul de l'attention;;L'innovation de DeepSeek est en rareureté est de bout en bout de détail, peut être utilisé directement dans la phase de préparation de formation;;

>  **【前置】**Les élèves doivent être informés de la mise en œuvre de la méthode de formation.
>  **【类比】**NSA = 看长文档的三种策略同时进行:**压缩分支**= 看目录摘要(粗粒度);(2) **选择分支**= 重点看自己感兴趣的章节 (à voir dans le film)**滑动窗口**= moment de la page précédente 5 pages 仔细看(局部上下文) ――门控(gate) = décider de quelle stratégie chaque position doit utiliser, apprendre automatiquement le meilleur ensemble。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Objectifs d'apprentissage

- Décrivez les trois services d'attention de la NSA et ce que chacun capture.
  Expliquer les trois branches de l'Agence nationale de sécurité et les informations qu'elle a capturées
- Expliquez pourquoi la NSA est "trainable de manière naturelle" alors que les méthodes précédentes de l'attention rare étaient uniquement d'inférence.
  Expliquer pourquoi la NSA est "pratiquement entraîneuse", alors que les méthodes d'attention rare précédentes ne peuvent être utilisées que pour la logique.
- Compute les économies d'attention de l'analyse de l'attention de la NSA par rapport à l'attention complète dans le contexte 64k en fonction de la taille du bloc de compression et du top-k de sélection.
  计算在 64K 上下文中 NSA相对全注意的计算节省量(作为压缩块大小和选择 top-k 的函数)
- Implémenter la combinaison de trois branches dans stdlib Python sur une courte séquence synthétique et vérifier le comportement des poids de fermeture.
  Utilisez Python en utilisant des séquences de synthèse courte pour réaliser un ensemble de trois branches, vérifier le contrôle du poids

## Le problème , l' introduction du problème

Attention totale à la longueur de séquence N coûte `O(N^2)`le temps et `O(N)`La mise en cache KV par couche. À 64k tokens, les numéros de bande passante de calcul et de mémoire sont catastrophiques. Estimation théorique mesurée du papier de la NSA: l'attention représente 70-80% de la latence totale de décode à 64k. Tout en aval  TTFT, tokens/sec, coût par million de tokens  est dominé par le coût de l'attention.

> 序列长度 N  的全注意力成本为 `O(N^2)`时间和每层 `O(N)`Le nombre de jetons de 64 k est désastreux. Les estimations de la théorie de la mesure de l'essai de la NSA: 70 à 80% du total du délai de résolution de la mise en cache.

Une attention peu élevée est la réponse évidente. Les tentatives précédentes sont divisées en deux. La rareté des motifs fixes (fouette coulissante, à pas, à bloc) jette les informations et échoue dans les tâches de rappel à longue portée. La rareté du temps d'inférence (KV cache pruning, H2O, StreamingLLM) est appliquée à un modèle prétrainé sur l'attention dense et ne récupère qu'une fraction de la vitesse potentielle car le modèle n'a jamais été invité à parcourir l'information à travers le modèle rare.

> La rareté de l'attention est une réponse évidente. Les tentatives précédentes ont été divisées en deux catégories. Le modèle fixe rareté (rouge à travers les fenêtres, tronçons, blocs) a été abandonné et a échoué dans la tâche de mémoire à long terme.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 best paper, arXiv:2502.11089) fait les deux: un modèle de sparsité que le modèle apprend lors de la pré-entraînement, mis en œuvre comme un algorithme aligné sur le noyau qui fournit réellement les économies de calcul à l'inférence.

> Origines rarefaction attention(Yuan 等人,DeepSeek + PKU + UW,ACL 2025 最佳论文,arXiv:2502.11089) Deux aspects du même concept: un modèle de rarefaction apprenant dans le cadre de la formation préliminaire, réalisé pour le schéma de coordination nucléaire, en cours de réflexion et réellement livré à l'économie de calcul.

## Le concept de base.

> **【中文解读】**Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Rés

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral's 32K 窗口) + 全局 token([CLS]) + 选择性关注。Google's Ring Attention 和 Block-Sparse Attention 将上下文扩展到百万代币──DeepSeek's NSA(Native Sparse Attention) 在训练时直接学习稀疏模式──


### Trois branches parallèles

Pour chaque requête, la NSA écoute trois fois, contre trois vues différentes du cache KV:

1. **Compressed branch.**Les jetons sont regroupés en blocs de taille `l`Chaque bloc est comprimé en un seul jeton de résumé via un petit MLP appris.

2. **Selected branch.**En utilisant les scores d'attention de la branche comprimée, les blocs top-k les plus pertinents pour la requête actuelle sont identifiés. Les jetons à grains fins (non comprimés) de ces blocs sont lus et la requête s'occupe de tous. Pensez à l'attention de la branche comprimée comme le signal de routage pour la sélection.

3. **Sliding-window branch.**La requête répond aux dernières `W`Cette branche capture les modèles de courte portée lourds de structure (syntaxe, coreference locale) que les deux autres pourraient manquer.

Les trois sorties de branches sont combinées par un portail par position appris:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`Ils ne doivent pas être sumés à 1  ils peuvent peser les branches indépendamment.

### Pourquoi cela est "trainable de manière naturelle"

La sélection est discrète. Les opérations discrètes brisent le débit de gradient. Le travail d'attention rare précédent a soit sauté le backprop par la sélection (entraînement limitant) ou utilisé des relaxations continues qui ne donnent pas de réelle rareté à l'inférence.

La NSA échappe à cela: l'attention de branches compressées est une attention grossière différenciable sur l'ensemble de la séquence. L'opération top-k utilise simplement les scores d'attention supérieurs de la branche comprimée pour choisir les blocs à grains fins à charger. Les gradients circulent à travers les scores de branches compressées (qui influencent à la fois la sortie compressée ET la logique de sélection), et la contribution des blocs sélectionnés à la sortie finale est également différenciable. Le non-différenciable `top_k`L'opération est un no-op sur le graphique de calcul avant  il contrôle seulement quels blocs sont chargés de la mémoire.

C'est pourquoi la NSA peut être utilisée dans la pré-entraînement de bout en bout. Le modèle apprend à parcourir les informations à travers les trois branches conjointement, produisant un schéma rare qui, à l'inférence, fournit réellement la vitesse promise.

### Noyau aligné sur le matériel

Le noyau de la NSA est conçu pour les hiérarchies de mémoire GPU modernes. Le noyau charge les requêtes par groupes GQA (loculier externe), récupère les blocs KV rares correspondants par groupe (loculier interne) et exécute l'attention sur SRAM. Parce que chaque groupe de requête voit les mêmes blocs sélectionnés (la sélection est par groupe de requête, pas par tête de requête), les charges KV sont amorties à travers le groupe. L'intensité arithmétique reste élevée.

Le document rapporte que les noyaux Triton fonctionnent 9 fois plus vite que FlashAttention sur les décodes 64k, avec le rapport de vitesse croissant avec la longueur de la séquence.

### Le budget de calcul

Je vous laisse .`N`être la longueur de la séquence, `l`la taille du bloc de compression, `k`le nombre de sélections au sommet de la liste, `w`la fenêtre coulissante, `b`la taille du bloc sélectionné (habituellement égale `l`)

- Branche comprimée: `O(N/l)`les clés par requête, donc `O(N * N / l)`- Tout à fait.
- Branche sélectionnée: `O(k * b)`les clés par requête, donc `O(N * k * b)`- Je suis désolé .
- Branche coulissante: `O(w)`les clés par requête, donc `O(N * w)`- Je suis désolé .

Total: `O(N * (N/l + k*b + w))`- Je suis désolé .

Avec `N = 64k, l = 64, k = 16, b = 64, w = 512`: le coût par requête est `1000 + 1024 + 512 = 2536 keys`- Attention à tout .`64000 keys`- 25 fois moins de calcul.

Avec `N = 128k, l = 64, k = 16, b = 64, w = 512`: le coût par requête est `2000 + 1024 + 512 = 3536 keys`- Attention à tout .`128000 keys`Le bénéfice augmente avec la longueur de la séquence, ce qui est le point principal.

### Comment ça se compare

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) a été publié en même temps et adopte une approche similaire trois-est-meilleur-qu'un, en appliquant le principe MoE aux blocs d'attention. NSA et MoBA sont les deux architectures à connaître pour 2026 long-context pré-entraînement.


> **【拓展：稀疏注意力在长上下文中的应用】**La quantité de calcul de l'attention intensive O(n^2) permet de faire en sorte que la phase de pré-remplissage de 128K de la suite nécessite environ 30 secondes.


## Construisez-le et mettez-le en œuvre.
```figure
sliding-window-attention
```

## Faites-le

`code/main.py`met en œuvre les trois branches sur une courte séquence synthétique et montre:

- La LPM de compression (une base moyenne simple est utilisée pour la clarté pédagogique; la NSA réelle utilise une LPM apprise).
- La sélection des blocs de haut niveau est déterminée par les scores de branches compressées.
- La fenêtre coulissante est à l' attention de la dernière .`w`Les jetons.
- La combinaison fermée.
- Une impression de comptage comparée à l'attention totale.

### Étape 1: compresser les jetons en blocs

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Étape 2: attention des branches compressées

Exécutez la requête à l'attention de la clé compressée.

### Étape 3: sélection du bloc supérieur

Choisissez les indices de la`k`Les blocs comprimés les plus performants, chargez les jetons non comprimés originaux de ces blocs et faites attention à eux.

### Étape 4: Attention à la fenêtre coulissante

Prenez le dernier .`w`les jetons et les faire connaître.

### Étape 5: porte + combinaison

Une petite MLP sur la requête produit trois poids de porte.

### Étape 6: calcul du compte

Imprimez le nombre de touches attendues par requête pour chaque branche et le total.`N`Sur une synthèse de 1024 tokens avec`l = 32, k = 4, w = 128`La NSA le voit .`32 + 128 + 128 = 288`Les clés par requête par rapport à 1024 pour une attention totale  3,5 fois moins.

## Utilisez-le avec le cadre de réalisation

La NSA est en train de fournir le pipeline de formation préalable à DeepSeek.

- **DeepSeek internal**: des poids natifs, publiés utilisent la NSA ou son successeur DSA (Deepseek Sparse Attention).
- **vLLM**: une aide expérimentale de la NSA en cours de développement pour les poids DeepSeek-V3.x.
- **SGLang**: Les indices de référence de la NSA publiés; le chemin de production suit le VLLM.
- **llama.cpp / CPU**: non pris en charge; les frais généraux de décomposition du noyau ne valent pas la peine à la capacité de traitement du processeur.

Quand vous devez contacter la NSA:

- Exécution de formation préalable ou de formation continue ciblant un contexte de plus de 64 000 personnes et doté d'un budget de calcul sérieux.
- Les poids sont nés de la NSA.

Quand ne pas:

- Vous ne pouvez pas réhabiliter la NSA sans formation continue.
- Les dépenses de trois branches dominent les économies.
- Le chat interactif de lot 1 bénéficie de décoding sensible à la latence, mais seulement dans de longs contextes.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-nsa-integrator.md`. Compte tenu d'une spécification de long-context pré-entraînement, il produit un plan d'intégration NSA: taille de bloc de compression, haut-k, vitrine coulissante, largeur de porte MLP, choix du noyau, et les évaluations spécifiques long-context qui justifieraient le changement d'architecture.

> 本课产 出 `outputs/skill-nsa-integrator.md`◊ donner une définition de la norme de fonctionnement de la formation préalable, elle produit un plan d'intégration de la NSA: blocs de compréhension de taille, de haut en bas, de fenêtre de glissement, de fenêtre contrôlée, de PLM de largeur, de sélection de la base, ainsi que des évaluations de la structure de démonstration plus raisonnables.

## Les exercices

1. On court .`code/main.py`sur un synthétique à 1024 jetons.`(l, k, w)`Identifier le préconisateur qui obtient le nombre de clés le plus bas par requête tout en conservant un rappel de 95% contre toute l'attention lors d'un test à l'aiguille-en-paille de foin.
   Le code de la ligne de référence est le code de la ligne de référence.`code/main.py`◊ dans trois pré-sets de la sonde `(l, k, w)`Il est possible de calculer la quantité de l'appel à l'emploi et de l'emploi des données.

2. Remplacez le compresseur de la moyenne par un petit MLP appris (2 couches, caché 32).
   Traduction anglaise: avec un petit apprentissage MLP ((2 niveaux, caché 32) remplacement de la moyenne de la valeur de la pile comprimée.

3. MLP: la portée prend la requête comme entrée et en sort trois échelles. Montrez que la porte se comporte judicieusement: pondération quasi uniforme sur les requêtes aléatoires, poids lourd sur la branche sélectionnée lorsque la requête frappe un bloc à l'arrière.
   Le système de contrôle de la portée est basé sur trois critères:

4. Compute le budget de mémoire de cache KV pour un modèle 70B activé par la NSA à un contexte de 128k. Les têtes KV sont 8, la tête est faible 128, BF16. Comparer à l'attention pleine et à MLA (phase 10 · 14 a montré les numéros de MLA).
   Le modèle 70B de la NSA est activé en 128K. Le KV 缓存内存预算──KV 头 8 个,头维度 128,BF16──与全注意力和MLA比较──找到 NSA 细粒度分支 KV 缓存等于全注意序列长度──

5. Lisez la section 4 du document de la NSA (arXiv:2502.11089) et expliquez en trois phrases pourquoi les scores d'attention de la branche compressée sont réutilisés pour la sélection top-k plutôt que pour calculer un score de routage séparé.
   Le résumé de l'article 4 de l'étude de la NSA est une explication de trois phrases expliquant pourquoi le nombre de points d'attention de la branche de compréhension est répété pour le choix de haut-k plutôt que pour le calcul du nombre de points de cheminement séparé.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## Encore une lecture

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089) Le papier
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) la famille d'architectes cibles de la NSA
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) travail concomitant, attention au style MoE sur les blocs
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) Origines des fenêtres coulissantes
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) L'indice de base de la rareté du temps d'inférence
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) la ligne de base de l'attention totale des noyaux NSA bat à 64k
