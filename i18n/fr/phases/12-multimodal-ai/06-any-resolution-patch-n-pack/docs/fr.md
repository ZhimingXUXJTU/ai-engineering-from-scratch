# La vision de toute résolution: patch-n'-pack et NaFlex 

> Les images réelles ne sont pas 224x224 carrés. Un reçu est 9:16, un graphique est 16:9, une analyse médicale peut être 4096x4096, une capture d'écran mobile est 9:19.5. La réponse VLM pré-2024  redimensionner tout à un carré fixe  a jeté le signal qui rend OCR, compréhension de documents et analyse de scène haute résolution fonctionnant. NaViT (Google, 2023) a montré que vous pouviez emballer des correctifs à résolution variable dans un seul lot de transformateur avec un masque de bloc-diagonale. Le M-RoPE (2024) de Qwen2-VL a complètement abandonné les tables de position absolue. L'AnyRes de LLaVA-NeXT a plaqué des images haute résolution dans une base + sous-images. La variante NaFlex de SigLIP 2 (2025) est maintenant l'encodeur par défaut pour les VLM ouverts qui veulent un seul point de contrôle pour servir chaque ratio d'aspect. Cette leçon met en œuvre le patch-n'-pack de bout en bout.

> **【中文解读】**L'image du monde réel n'est pas une image carrée de 224x224  Réception est de 9:16, la figure est de 16:9, l'image médicale est possible 4096x4096 ⋅2024 Année précédente VLM 统一将图像缩缩放为固定正方形, ce qui va perdre la compréhension OCR、文档和高分辨率场景解析的关键信息──本课讲解如何让变压器以原始分辨率处理任意宽高比的图像──

> **【拓展：金融文档场景的分辨率挑战】**Dans le monde financier, la largeur des documents de rapports, émissions de billets, contrats et autres diffèrent de milliers de fois. La réduction de la forme carrée fixe entraîne une diminution de la précision des textes.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言:** Python（标准库，补丁打包器 + 块对角掩码）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置知识:** Phase 12 · 01（ViT补丁）、Phase 12 · 05（LLaVA）
**Time:** ~120 minutes  | **时间:** ~120 分钟

>  **【前置】**Je vous invite à maîtriser la phase 12 de la partie 1 du programme.
>  **【类比】**La plupart des boîtes sont en forme de boîtes, un camion est en forme de boîtes.
> ️ **【易错点】**实现 NaViT 时忘记块对角掩码 → 三张图的补丁 会相互做注意,模型训练完全失败──修复: il faut construire (N,N) 的注意矩阵, uniquement dans chaque diagramme du patch 索引对应的块内允许注意,块外为 -inf──

## Objectifs d'apprentissage

- Emballez des patchs d'un lot d'images à résolution variable dans une séquence et construisez le masque d'attention à diagonale de bloc.
  > Envelopper les correctifs d'une image à résolution différente en une séquence, construire un bloc à angle de l'attention masquer.
- Choisissez entre AnyRes (LLaVA-NeXT), NaFlex (SigLIP 2) et M-RoPE (Qwen2-VL) pour une tâche donnée.
  > Selon les tâches à effectuer, vous pouvez choisir AnyRes 切片 (LLaVA-NeXT) 、NaFlex (SigLIP 2) ou M-RoPE (Qwen2-VL) ⋅
- Comptez les budgets de jetons pour le RCR, les graphiques et la photographie sans redimensionner.
  > 计算无缩缩的情况下 OCR 图表和摄影的代币 预算
- Nombre des trois modes d'échec de la taille carrée: texte écrasé, contenu coupé, jetons gaspillés sur le rembourrage.
  > 列举正方形缩放的三种失败模式:文字压缩,内容裁剪,padding 浪费,

## Le problème , le contexte .

Les transformateurs s'attendent à une séquence. Un lot est une pile de séquences de la même longueur. Si vos images sont 224x224, vous obtenez 196 jetons de patch à chaque fois, le rembourrage n'est pas nécessaire, le travail est fait. Train sur 224, inférer sur 224, ne jamais penser à la résolution à nouveau.

> Transformer 期望固定长度序列──一批就是一堆等长序列──如果图像都是224x224,每次都产生196补丁代币,无需填充,问题解决──训练和推理都用224,永远不用考虑分辨率──

Les documents sont portraits (8,5x11 pouces, 2:3-ish). Les captures d'écran des graphiques sont paysages (16:9). Les reçus sont hauts et fins (1:3). Les navires d'imagerie médicale à 2048x2048 ou plus. Les captures d'écran des appareils mobiles sont 1170x2532 (0,46:1).

> Le tableau de bord est à droite et à gauche. Le tableau de bord est à gauche.

Trois options pré-2024 et pourquoi chacune échoue:

> Trois options et les causes de leur défaite avant 2024:

1. La taille est réduite à un carré fixe (224x224 ou 336x336). Le squish déforme le texte et les visages.
   > 缩放为固定正方形(224x224或336x336)。缩缩会扭曲文字和人脸。下采样会破坏图表标签和OCR 内容──LLaVA-1.5 之前的标准做法──
2. On jette la plupart de l'image, et choisir l'emplacement de la culture est son propre problème de vision.
   > 剪裁为固定宽高比──会丢弃大部分图像,而选择剪裁位置本身就是一个视觉问题──
3. Le pad sur le côté le plus long. Réglectionne la distorsion mais gaspille plus de 50% des jetons sur le rembourrage pour les images de portrait. Coût d'attention quadratique sur tous ces jetons de pad.
   > 填充到最长边──修复扭曲但对屏图像浪费50%+的代币 在填充上──所有填充代币的注意成本是二次的──

> **【中文解读】**Transformer 期望固定长度的序列──真世界图像宽高比不同,2024年前有三种做法:(1) 缩缩为正方形文字变形、OCR 内容丢失;(2) 剪裁丢弃大量内容;(3) 填充屏幕图像浪费 50%+的代币 在填充上,注意计算成本第二次增长──

La réponse 2024-2025: laissez le transformateur manger des patchs à la résolution native de l'image, et de trouver comment emballer un lot hétérogène dans une séquence sans gaspiller de calcul.

> Réponse de 2024-2025: Laissez le transformateur "déterminer" directement avec le correctif de résolution initiale, puis réfléchissez à la façon de le faire en un seul ensemble sans gaspiller de calcul.

## Le concept de base.

### NaViT et le patch-n'-pack

NaViT (Dehghani et coll., 2023) a été le document qui a montré que cela fonctionne à grande échelle.

> NaViT ((Dehghani 等人,2023) a prouvé cette façon de penser à grande échelle.

1. Pour chaque image du lot, calculer sa grille de patch native à une taille de patch choisie (disons 14).
   > Pour chaque image de la série, pour spécifier les correctifs en taille (environ 14) calculer les correctifs en série.
2. Appliquer les patchs de chaque image dans sa propre séquence de longueur variable.
   > Pour chaque image, les suppléments sont placés dans leur séquence de longueur variable.
3. Concaténez tous les patchs d'images en une longue séquence pour le lot.
   > Résoudre toutes les images en une longue séquence en tant que lots.
4. Construisez un masque d'attention à diagonale de bloc afin que les patchs de l'image A ne se trouvent que dans l'image A.
   > Construire un bloc pour masquer l'attention sur les angles, afin que les corrections de l'image A ne soient effectuées que dans l'image A.
5. Les informations relatives à la position par patch (enregistrements RoPE ou position fractionnelle) doivent être portées.
   > Pour chaque supplément, portez des informations de position (ROPE 2D ou position intégrée).

Un lot de trois images à 336x336 (576 jetons), 224x224 (256 jetons) et 448x336 (768 jetons) devient une séquence de 1600 jetons avec un masque de bloc-diagon 1600x1600. Pas de rembourrage. Pas de calcul gaspillé. Le transformateur gère des ratios d'aspect arbitraires.

> Les lots sont transformés en un ensemble de 1600 tokens, avec 1600x1600 blocs contre un coin.

NaViT a également introduit la chute fractionnelle de patch pendant l'entraînement  la chute de 50% des patches au hasard dans le lot  qui régularise et accélère l'entraînement. SigLIP 2 a hérité de cela.

> La NaViT a également introduit des correctifs de formation en temps partiel abandonnés dans les lots à 50% abandonnés à 50%.

> **【中文解读】**Le cœur de NaViT: trois张不同分辨率的图像(576 + 256 + 768 = 1600 个代币) est enveloppé dans une séquence, avec des blocs pour cacher les angles afin de prévenir le repassage de l'image.

### Je suis en train de faire une petite histoire.

L'AnyRes de LLaVA-NeXT est l'alternative pragmatique.

1. Choisissez une mise en page de la grille d'un ensemble prédéfini  (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), etc.  qui correspond le mieux au rapport d'aspect de l'image.
2. Tire l'image complète dans la grille; chaque carreaux devient une récolte de 336x336.
3. Produire également une miniature: toute l'image est redimensionnée à 336x336 comme un jeton de contexte mondial.
4. Chaque carreaux est encodé par le codeur gelé 336. Concaténez les jetons de carreaux + jetons miniatures.

Pour une image 672x672 à la grille 2x2 plus une miniature: 4 * 576 + 576 = 2880 jetons visuels.

AnyRes est la voie de choix lorsque votre encodeur est gelé et ne prend en charge qu'une seule résolution. Il exploite le nombre de jetons pour les grandes images (une image de 1344x1344 à la grille 4x4 est de 9216 + 576 ≈ 9800 jetons, qui remplit la plupart d'un contexte LLM 8k).

> **【中文解读】**AnyRes  est adapté à un codeur qui est bloqué et ne prend en charge que la situation d'une seule résolution. Le prix est un nombre de jetons de grande image augmenté.

### M-RoPE (Qwen2-VL)  M-RoPE

Qwen2-VL a introduit l'intégration de position rotative multimodal. Au lieu des positions fractionnelles de NaViT ou de la carreaux et miniatures d'AnyRes, chaque patch porte une position 3D (temporale, hauteur, largeur).

M-RoPE envoie une résolution dynamique native sans recyclage. À l'inférence, vous nourrissez une image HxW, le patch embedder produit des jetons H/14 x W/14, chaque jeton obtient sa position (t=0, r=row, c=col), le RoPE fait tourner l'attention avec les bonnes fréquences, fait. Qwen2.5-VL et Qwen3-VL continuent ainsi.

Contrairement à AnyRes, M-RoPE est O(H x W / P^2) jetons à résolution native  pas de charge de carrelage multiplicative. Contrairement à NaViT, il attend toujours une seule image par avance.

> **【中文解读】**M-RoPE pour chaque supplément donne trois dimensions de position (temps, hauteur, largeur), utilise le code de position rotative pour traiter n'importe quel H、W 和 temps de longueur.

### Je suis un homme de la famille de NaFlex.

NaFlex est le mode native-flex du point de contrôle SigLIP 2. Un seul modèle sert plusieurs longueurs de séquences (256, 729, 1024 jetons) à l'inférence.

Pour une tâche sémantique (classification, récupération), 256 jetons. Pour OCR ou compréhension de graphique, 1024 jetons. Pas de recyclage.

> **【中文解读】**Le point de vente central de NaFlex est un point de contrôle, recommandé lors de la sélection de jetons 预算──语义任务使用256 jetons, OCR或图表理解使用1024 jetons,无需重训练──这非常适合构建成本敏感的多模态服务按需分配的 jetons 预算──

### Le masque d'emballage

Le masque de bloc-diagonale est le point où la plupart des implémentations trébuchent.`N_total`couverture d'images `i=0..B-1`avec des longueurs `n_i`, le masque `M`de forme `(N_total, N_total)`est 1 si les deux indices tombent dans le même bloc d'image, sinon 0. Vous pouvez le construire à partir d'une liste de longueur cumulée:

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

C' est une ligne dans PyTorch avec `torch.block_diag`La trajectoire de longueur variable de FlashAttention (`cu_seqlens`) saute entièrement le masque et se présente en séquences en utilisant directement le tensor de longueur cumulée  ~ 10 fois plus rapidement qu'un masque dense pour les lots typiques.

> **【中文解读】**块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角掩码 块对角角掩码 块对角角角`cu_seqlens`) se concentrer directement sur la longueur accumulée, sauter à travers le masque, la vitesse est d'environ 10 fois.

### Les billets de jeton

Choisissez votre stratégie par tâche:

- OCR / documents: 1024-4096 jetons. SigLIP 2 NaFlex à 1024, ou AnyRes 3x3 + miniature.
- Charts et UI: 729-1024 jetons à 384-448 natifs. résolution dynamique Qwen2.5VL avec cap de pixels max.
- Les photos naturelles: 256-576 jetons sont bons. Le LLM en aval voit assez. Paier pour les jetons où la densité de contenu est élevée.
- Vidéo: 64-128 jetons par image après le regroupement spatial, 2-8 FPS. Leçon 12.17 couvre ceci.

La règle de production 2026: choisir un capot max-pixels par tâche, encoder à la proportion d'aspect native jusqu'à ce capot, emballer le lot, et sauter le rembourrage.`min_pixels`et `max_pixels`Pour ce bouton.

> **【拓展：Token 预算与成本优化】**Dans l'environnement de production, les jetons  budgétaire affectent directement l'API 成本和延迟── pour les tâches OCR 分配 1024+ jetons est nécessaire, mais naturellement les photos avec 256 jetons sont suffisantes── en fonction des tâches 动态调整分辨率 est la meilleure pratique de la déploiement de VLM en 2026──

> 🤔 **【困惑】**1) Réellement déployer le système OCR, min_pixels et max_pixels Le nombre de fixations ? 文档类 min=28*28*4、max=28*28*2560(Qwen2-VL 默认); 过高会爆显存,过低会丢失小字──2) Pourquoi ne pas utiliser directement 2k×2k? token,长文档一张图就吃掉整个LLM 上下文──3) NaFlex vs AnyRes 哪个更通用? NaFlex(SigLIP 2) 更现代,单一检查点 适应所有分辨率;AnyRes 是过渡方案──

## Utilisez-le en pratique
```figure
mm-patch-n-pack
```

## Utilisez-le

`code/main.py`Il implémentera le patch-n'-pack pour un lot hétérogène d'images avec des coordonnées de pixel entiers.

> `code/main.py`Utilisation intégrale de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de l'image.

- Prend une liste des tailles d'image (H, W).
  > 接收 (H, W) 图像尺寸列表
- Calcule la longueur de la séquence de patch de chaque image à la taille de patch 14.
  > 計算每张图像在补丁大小 14 下的序列长度──
- Les emballer en une séquence de longueur totale `sum(n_i)`- Je suis désolé .
  > 打包为总长度 `sum(n_i)`De la seule séquence.
- Construit le masque d'attention à diagonale de bloc (dense, pour clarté).
  > 构建块对角注意力掩码 (construction de blocs à couper le souffle)
- Comparer le coût de l'emballage par rapport à la taille carrée et à la tôle AnyRes.
  > Comparativement à l'emballage et à la réduction des écarts.
- Imprime un tableau de budget symbolique pour un lot mixte (receipt, graphique, capture d'écran, photo).
  > 打印混合批次(收据、图表、截图、照片) du symbole 预算表。

Les chiffres qui tombent sont la raison pour laquelle chaque VLM ouvert en 2026 utilise un patch-n'-pack.

> Le nombre de pages imprimées est le principal facteur de l'utilisation de patch-n'-pack par les VLM en 2026.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-resolution-budget-planner.md`. Compte tenu d'une charge de travail à rapport d'aspect mixte (OCR, graphiques, photos, images vidéo) et d'un budget total de jetons, il choisit la bonne stratégie (NaFlex, AnyRes, M-RoPE ou quadré fixe) et émet une configuration par demande.

> 本课产 出 `outputs/skill-resolution-budget-planner.md` Donner une combinaison de largeur et de hauteur de travail chargement (OCR, graphiques, photos, vidéos) et un total de jetons budget, il choisit la bonne stratégie (NaFlex, AnyRes, M-RoPE ou forme carrée fixe) et génère selon la configuration demandée.

> **【中文解读】**Le projet de loi sur la gestion des ressources humaines et de l'emploi (voir paragraphe 1) est un projet de loi sur les ressources humaines et les ressources humaines.

## Les exercices

1. Un reçu est 600x1500 (1:2.5). À la taille du patch 14, combien de jetons à résolution native? combien après la taille carrée à 336? Qui perd plus de précision OCR en pratique?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. Construisez le masque de bloc-diagonale pour un lot de quatre images de longueur 256, 576, 729, 1024.`256^2 + 576^2 + 729^2 + 1024^2`les entrées non zéroes.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. Pour une image 1792x896 au patch 14, comparez: (a) quadratiser à 336 puis encoder, (b) AnyRes 2x1 + miniature, (c) M-RoPE à native.
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Mettre en œuvre la chute de patch fractionnée: compte tenu d'une séquence emballée, déposez 50% des jetons de manière uniforme au hasard et mettez à jour le masque de bloc-diagonale en conséquence. Mesurer la variation de la rareté du masque.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Lisez la section 3.2 du document Qwen2-VL (arXiv:2409.12191). Décrivez en deux phrases ce qui est`min_pixels`et `max_pixels`le contrôle et pourquoi les deux limites comptent.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Encore une lecture

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304)Je suis un homme de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe.
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)Je suis un homme qui a des problèmes avec la machine.
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Facteurs clés de la construction de VLM
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786)Je suis un homme qui a une vieille fille.
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)Je suis en train de faire une petite histoire.
