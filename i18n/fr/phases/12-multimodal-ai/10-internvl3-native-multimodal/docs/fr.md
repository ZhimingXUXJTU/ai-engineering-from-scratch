# InternVL3: Pré-entraînement multimodaux natif

> Chaque VLM ouvert avant InternVL3 suivait la même recette en trois étapes: prendre un texte LLM formé sur des milliards de jetons de texte, boulon sur un codeur de vision, puis affiner les coutures. Ce système fonctionne mais a une dette d'alignement  le texte LLM a dépensé tout son budget pré-entraînement sur le texte pur et ne comprend pas nativement les jetons visuels. Lorsque vous ajoutez la vision post-hoc, le LLM doit réapprendre à relier l'entrée visuelle à son raisonnement textuel sans oublier le texte. InternVL3 (Zhu et coll., avril 2025) rejette l'approche post-hoc: une course pré-entraînement, un texte et un multimodal interlevé à partir de l'étape 1. Le résultat correspond à Gemini 2.5 Pro sur MMMU-Pro à 78B params ouverts. Cette leçon explique le cas de la pré-entraînement natif et ce qui change lorsque vous le faites.

> **【中文解读】**L'innovation centrale de InternVL3: rejet du programme de rechange de "Pré-trainage de texte LLM Recoupement de texte vidéo éditeur", modifié à partir de la première étape pour le texte et le multi-modèles de données de la formation de tissus de données.

> **【拓展：原生预训练 vs 后装的成本权衡】**La formation initiale a éliminé la dette totale, mais le coût est bien supérieur à la formation initiale. Elle nécessite des millions de GPU en temps réel, et renonce à la flexibilité de la formation initiale. Pour la plupart des projets, la formation initiale est encore plus économique.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**Le programme de formation est basé sur la formation de la formation professionnelle et la formation professionnelle.
>  **【类比】**后装 VLM(LLaVA) = "成年后学外语"已经掌握母语(文本),再艰难学第二语言(视觉) ・・・原生 VLM(InternVL3) = "双语家庭长大"两种语言同时学,没有翻译损耗──后装方案便宜但有口音(对齐债务),原生方案昂贵但流利──
> 🤔 **【困惑】**Q: 既然 l'entraînement de base est si bon, pourquoi LLaVA  est-il toujours en vogue?  成本!

## Objectifs d'apprentissage

- Expliquez pourquoi la formation post-hoc VLM accumule une dette d'alignement, en citant les trois symptômes mesurables (oubli catastrophique, dérive de réponse, inconséquence visuelle-texte).
- Décrivez le mélange de corpus de pré-entraînement natif de InternVL3 et pourquoi le rapport du texte : interlevé: sous-titre importe.
- Comparer V2PE (codation de position visuelle variable) à M-RoPE de Qwen2-VL.
- Nommer le routeur de résolution visuelle (ViR) et les optimisations de déploiement de langage de vision découplé (DvD).

## Le problème , le contexte .

La formation post-hoc VLM est la formation par défaut. LLaVA, BLIP-2, Qwen-VL, Idefics  prennent tous un LLM déjà prétrainé (Llama, Vicuna, Qwen, Mistral) et ajoutent la vision.

1. LLM gelé + vision gelée encodeur + projecteur entraîneur, entraîné sur des paires de sous-titres pour aligner les emblèmes.
2. Défrichez le LLM, entraînez-vous sur les données d'instruction.
3. Optionnel pour les tâches spécifiques.

Trois symptômes de la dette de l'alignement apparaissent:

- L'oubli catastrophique / 灾难性遗忘. Le VLM post-hoc oublie les compétences en texte seulement. Les scores GSM8K baissent de 5 à 10 points. Les scores Hellaswag baissent. Les agents pur-textes régressent.
- Réponse drift / 回答漂移. Les petites phrases de la même question visuelle obtiennent des réponses différentes. Le codeur de vision se connecte au LLM avec des liaisons plus faibles que les jetons du LLM lui-même.
- L'image peut être décrite correctement et ensuite répondre à une question contradictoire à sa propre description. Les jetons visuels ne participent pas aux contrôles de cohérence internes du LLM de la même manière que le texte.

> **【中文解读】**后装 VLM's Three Forms of Balance Debt: 1) L'oubli catastrophique GSM8K 掉 5-10 分; 2) Répondre漂移 Différentes expressions du même problème visuel obtiennent différentes réponses; 3) Le modèle visuel-textuel inconsistent  décrit correctement l'image, mais donne des réponses contradictoires  Ces symptômes sont dus à la façon dont les jetons visuels diffèrent des jetons textuels et ont profondément contribué à l'examen interne de la cohérence de la LLM

## Le concept de base.

### Pré-entraînement multimodal natif

InternVL3 traîne à partir de zéro sur un corpus qui est natif multimodal à partir de l'étape 1.

- 40% de données uniquement textuelles (FineWeb, Proof-Pile-2, etc.) / 40% 纯文本数据
- 35% de données entre images et textes interligées (OBELICS, style MMC4) / 35% 交织图文数据
- 20% de données de sous-titres d'image parallèles / 20% 图文配对数据
- 5% de données vidéo-texte / 5% 视频文本数据

Les jetons de vision, les jetons de texte et les interactions intermodiales participent tous à la même perte dès la première étape du gradient.

La formation est une étape unique pour le modèle de base.

> **【中文解读】**InternVL3 De la première étape, il sera introduit dans la même fonction de perte, il n'y aura pas besoin de préparation, il n'y aura pas besoin de projecteur, il n'y aura pas besoin de récupération du désastre.

### V2PE (codation de position visuelle variable)

Qwen2-VL utilise M-RoPE avec allouement d'axe fixe. InternVL3 introduit V2PE: le codage de position varie selon le type de modalité (texte, image, vidéo) avec une mise à l'échelle appréciable.

- Les jetons de texte obtiennent une position 1D (index de texte).
- Les patchs d'image obtiennent une position 2D (ligne, colonne).
- Les images vidéo ont une position 3D (temps, rangée, col).

Les trois partagent la même base de fréquences RoPE, mais l'allocation de la lumière cachée par bande est un paramètre appris plutôt que une fraction fixe.

L'affirmation d'ablation de V2PE: 1 à 2 points sur les points de référence vidéo par rapport à M-RoPE au même calcul.

> **【中文解读】**La différence entre le V2PE et le M-RoPE: la dimension cachée est répartie entre les différents phases de fréquence par des paramètres apprenables et non par des divisions fixes. Le modèle peut mesurer automatiquement le temps et la fréquence de résolution de l'espace au cours du processus de préparation.

### Le routeur de résolution visuelle (ViR)

Optimisation du déploiement. Toutes les images ne nécessitent pas un codage à haute résolution. Une photo avec un objet à faible détail gaspille des jetons lorsqu'elle est cochée à 1280px natif. ViR est un petit classifiant qui prédit la résolution minimale nécessaire pour répondre à la question, avant de cocher.

Le routage a trois niveaux: faible résolution (256 jetons), moyen (576), élevé (2048+). Pour 60% des requêtes dans le trafic de production, faible ou moyen est suffisant.

> **【中文解读】**ViR est déployé optimisé: un petit classifiateur a la résolution minimale nécessaire à la requête de prédiction de codage.

> **【拓展：ViR 与金融场景】**Dans le traitement des documents financiers, la plupart des requêtes (comme "le montant total de cette émission est combien") nécessitent seulement une résolution basse, mais les tâches OCR (comme "Télécharger tous les projets") nécessitent une résolution élevée.

### Déploiement de la vision-langue déconnectée (DvD) 解视觉-语言部署

Lorsque vous servez un grand VLM, l'encodeur de vision fonctionne une fois par image mais le LLM fonctionne autorégressivement pour chaque jeton de sortie. Les deux composants ont des goulots d'étranglement différents (vision = bande passante de la mémoire GPU pour conv + attention; LLM = cache KV).

Pour un modèle d'encodeur 8B + 400M, le DvD doublera à peu près le débit par nœud par rapport au co-loqué.

> **【中文解读】**Le DVD va déployer le codeur vidéo et le LLM sur différents GPU, via des connexions de transmission en cours de route.

### La qualité de la phase unique contre la qualité de la phase multi

La première référence de l'InternVL3 est: à 78B params, correspondre à MMMU-Pro de Gemini 2.5 Pro. À 38B, correspondre à GPT-4o. À 8B, mener le leader des 8B ouverts. Tout sur une recette de pré-entraînement + instruction-tune d'une seule étape.

L'hypothèse de l'alignement-débit est mesurable: InternVL3-8B perd moins de points de référence texte (MMLU, GSM8K) que Qwen2.5-VL-7B par unité de gain de référence vision.

> **【中文解读】**InternVL3-8B Chaque année, on obtient un niveau de formation de base de la vue, une augmentation de la perte de la valeur de base de texte par rapport à Qwen2.5-VL-7B.

### Les résultats de l'enquête

InternVL3.5 (août 2025) évolue la recette. La même approche de pré-entraînement natif, plus de données, plus de paramètres.

InternVL-U (2026) ajoute une production d'image unifiée de génération  via les têtes MMDiT sur le dessus de la même colonne vertébrale.

> **【中文解读】**InternVL-U(2026) a intégré la capacité de génération d'images sur le même tronc (à travers MMDiT) à la recherche de la compréhension du style de transfusion + génération d'un modèle unifié.

### Les échanges de pré-entraînement natif

La pré-entraînement native n'est pas gratuite:

- Compute / 计算. La formation d'un nouveau VLM à partir de zéro coûte le même que la formation d'un texte LLM  millions d'heures GPU.
- Les données / données. Les corps d'image-texte interligés à l'échelle sont rares. OBELICS est de 141 millions de documents; MMC4 est de 571 millions. Le texte seul est livré à 15T jetons. La pénurie de données pré-entraînement multimodal est une contrainte difficile.
- La formation initiale renonce à la possibilité de passer un nouveau LLM plus tard. Après le hoc, vous pouvez échanger Llama-3.1 contre Llama-4 en ne recyclant que l'adaptateur.

Le pari de InternVL3 est que la dette d'alignement est pire que la perte de réutilisation. Les critères de référence confirment la revendication. Les coûts de production empêchent les laboratoires futurs de reproduire à bas prix.

> **【中文解读】**Les résultats de la formation de base sont plus intéressants que les résultats de la formation de base.

## Utilisez-le en pratique
```figure
l5-native-pretrain
```

## Utilisez-le

`code/main.py`est un mélangeur de formation et un simulateur de routeur ViR.

- Prend un corpus cible mix (% texte, % interleavé, % sous-titre, % vidéo) et calcule les étapes attendues par modalité.
- Simule le routage ViR sur un lot de requêtes (distribution: 50% de faible détail, 30% de moyen, 20% de haut détail) et rapporte le nombre moyen de jetons.
- Rapporte les estimations de débit de DVD données par l'encodeur par rapport aux FLOP LLM.
- Il imprime un suivi de la formation post-hoc et de la formation précoce des natifs en paramètres, calcul, données et symptômes attendus d'alignement-endettement.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-native-vs-posthoc-auditor.md`. En raison d'un plan de formation proposé pour le VLM, il vérifie si l'on doit se lancer en mode native ou post-hoc, identifie le risque d'alignement-endettement et recommande un corpus mix.

> **【中文解读】**Le programme de formation VLM est basé sur la formation de la formation professionnelle et de la formation professionnelle.

## Les exercices

1. Évaluer le delta de calcul entre InternVL3-8B (pré-train natif) et LLaVA-OneVision-7B (post-hoc).
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 rapporte 40% de texte / 35% de sous-titres / 20% de vidéo. Si votre tâche cible est vidéo-cheveuse, proposez un nouveau ratio et expliquez pourquoi le modèle de base a encore besoin de données de texte et de sous-titres substantielles.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. Lisez MM1.5 Section 4 sur l'oubli. Nommez le point de référence exact où l'entraînement post-hoc a montré la plus grande régression.
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. ViR envoie 60% du trafic à un codage à basse résolution. Quels types de requêtes est-il enroule (envoie à basse résolution lorsque la haute résolution est nécessaire)?
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. DvD divise la vision et le LLM en GPU séparées.
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Encore une lecture

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238)Je suis un homme de la première génération.
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)Je suis un homme qui a fait de la musique.
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265)Je suis un homme qui a une grande expérience.
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)Je suis un homme qui a une bonne idée de la situation.
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566) MM1.5 pour la quantification de la dette
