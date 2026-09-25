# Récipes VLM à poids ouvert: ce qui compte vraiment

> La littérature VLM de poids ouvert 2024-2026 est une forêt de tables d'ablation. Le MM1 d'Apple a testé 13 combinaisons d'encodeur d'image, de connecteur et de mélange de données. Les légendes humaines détaillées de l'IA Allen Molmo ont prouvé que la distillation GPT-4V était plus efficace. Cambrian-1 a effectué plus de 20 comparaisons d'encodeurs. Idefics2 a officiellement formalisé l'espace de conception à cinq axes. Les VLM prismatiques ont comparé 27 recettes de formation sur un critère de référence contrôlé. De tout ce bruit, un petit ensemble de résultats est valable sur tous les papiers: l'encodeur d'image compte plus que l'architecture du connecteur, le mélange de données compte plus que les deux, et les légendes humaines détaillées battent les données synthétiques distillées. Cette leçon lit ces tables pour que vous n'ayez pas à le faire.

> **【中文解读】**Le projet de loi de 2024-2026 sur les VLM est plein d'expériences de consommation. Il s'agit d'un projet de loi de 2024-2026 qui consiste à élaborer des techniques de gestion de contenu et de gestion de contenu, en particulier des systèmes de gestion de contenu et de gestion de contenu.

> **【拓展：VLM 工程的实践指南】**Les conclusions de ce cours guident directement la pratique de l'ingénierie VLM. Lorsque vous découvrez que les performances de VLM ne sont pas à la hauteur de la norme, vous devez suivre les priorités suivantes: 1) le nombre de jetons visuels est-il suffisant ? 2) le choix du codeur est-il suffisant ? 2) le nombre de données est-il suffisant ? 3) le nombre de données est-il suffisant ? 4) l'architecture de connecteurs est-elle suffisant ?

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Je vous invite à maîtriser la phase 12 du projet.
>  **【类比】**开源 VLM 五轴选择 = "买车选配置"──编码器 = 发动机(性能差 5-7 分);连接器 = 中控台界面(几乎不影响驾驶);LLM = 车身大小;数据 = 油品(差油再好的发动机也跑不快);分辨率 = 轮胎(决定能跑什么地形)──纠结界面(连接器) 是新手陷,老司机优先看发动机和油。

## Objectifs d'apprentissage

- Nommez l'espace de conception VLM à cinq axes: encodeur d'image, connecteur, LLM, mélange de données, calendrier de résolution.
- Lisez une table d'ablation MM1 / Idefics2 / Cambrian-1 et prédisez quel bouton déplace un point de référence donné.
- Choisissez une recette (encodeur, connecteur, données, résolution) pour un nouveau VLM étant donné un budget de calcul et un mélange de tâches.
- Expliquez pourquoi les légendes détaillées sur l'homme ont battu la distillation GPT-4V au même nombre de symboles.

## Le problème , le contexte .

Il existe des centaines de VLM à poids ouvert. La plupart du temps, l'écart entre "bon" et "state-of-the-art" n'est pas l'architecture. Il s'agit de données, de calendrier de résolution et de choix d'encodeur.

La vague 2023 (LLaVA-1.5, InstructBLIP, MiniGPT-4) a été réalisée sur un coup de sous-titres + LLaVA-Instruct-150k.

La vague 2024 (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) a effectué des ablations exhaustives.

> **【中文解读】**Dans plusieurs centaines de VLM open source, la différence entre "bon" et "meilleur" n'est pas principalement l'architecture, mais les données, la résolution de régulation et le choix du codeur.

## Le concept de base.

### L'espace de conception à cinq axes

Idefics2 (Laurençon et coll., 2024) a nommé les axes:

1. L'encodeur d'image / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Les encodeurs diffèrent en taille de patch, résolution et objectif de prétrainage / 编码器在补丁大小、分辨率和预训目标上各不相同.
2. Connecteur / 连接器. MLP (2-4 couches), Q-Former (32 requêtes + cross-attn), Percepteur Resampler (64 requêtes), C-Abstractor (convolution + bilinéaire pooling) / MLP(2-4 couches)、Q-Former(32 enquête+交叉注意力)、Percepteur 重采样器(64 enquête)、C-Abstractor(卷积+双线性池化).
3. Le modèle de langue / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5.
4. Les données de formation / 训练数据. couples de sous-titres (CC3M, LAION), interligés (OBELICS, MMC4), instruction (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Résolution de l'équipe de formation de la formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation en formation en formation de formation en formation de formation de formation en formation en formation de formation de formation de formation de formation de formation de formation en formation de formation de formation de formation de formation de formation de formation en.

Chaque VLM de production fait un choix sur chaque axe. La plupart des variations dans les scores MMMU sont expliquées par les axes 1, 4 et 5  et non par le connecteur que vous avez choisi.

> **【中文解读】**Chaque VLM est sélectionné sur cinq axes. La plupart des différences de la partition MMMU sont due à l'axe1 (codeur) ⋅ axes4 (données) et axes5 (résolution) expliquer plutôt que le connecteur que vous avez choisi.

### Axe 1: encodeur > connecteur

MM1 Section 3.2 a montré: le changement de CLIP ViT-L/14 à SigLIP SO400m/14 a ajouté 3 points MMMU. le changement du connecteur de MLP à Perceiver Resampler a ajouté moins de 1 point.

Le "Cambrian Vision Encoders Match-Up" de Cambrian-1 (Tong et coll., 2024) a utilisé plus de 20 encoders sur un benchmark axé sur la vision (CV-Bench). Le haut du classement est un mélange de DINOv2 et SigLIP; CLIP est au milieu du pack; ImageBind et ViT-MAE sont plus bas. L'écart entre CLIP ViT-L et DINOv2 ViT-g/14 est de ~ 5 à 7 points sur CV-Bench.

Le codeur par défaut 2026 pour les VLM ouverts est SigLIP 2 SO400m/14 pour les fonctionnalités sémantiques + denses, parfois concatené avec les fonctionnalités DINOv2 ViT-g/14 (l'agrégateur de vision spatiale de Cambrian le fait).

> **【中文解读】**Le codeur par défaut de VLM est SigLIP 2 SO400m/14, parfois avec DINOv2 ViT-g/14 拼接((Cambrian's "spatial visual aggregator" est ce que fait)

> ️ **【易错点】**Les nouveaux utilisateurs sont souvent pris dans le piège de la "réforme des systèmes de connexion" qui, selon Q-Former, est plus beau que cela.

### Axe 2: la conception du connecteur est un lavage.

MM1, Idefics2, Prismatic et MM-Interleaved ont tous conclu la même chose: à un nombre fixe de jetons visuels, l'architecture du connecteur compte à peine.

Ce qui compte, c'est le nombre de jetons. Plus de jetons visuels = plus de calcul LLM = meilleure performance jusqu'à un point, puis des rendements diminuant. 64 jetons par image est trop peu pour OCR. 576-1024 jetons est le point de départ pour la plupart des VLM ouverts. 2048+ aide uniquement pour les documents et les graphiques.

Q-Former vs MLP est une question de coût, pas une question de qualité: Q-Former limite les jetons à 32-64 indépendamment de la résolution de l'image; MLP émet tous les jetons de patch. Pour les entrées haute résolution, Q-Former économise le contexte LLM; pour les basses résolutions, la différence est le bruit.

> **【中文解读】**En termes de nombre de jetons visuels fixes, l'architecture du connecteur n'affecte presque pas les performances. La différence entre les 2 niveaux de MLP et les 32 requêtes de Q-Former est de 1 min. En effet, la taille des jetons est très faible. 546-1024 est le meilleur.

### Axe 3: La taille de la licence fixe le plafond

Le double du LLM de 7B à 13B ajoute de manière fiable 2 à 4 points sur MMMU sur chaque document VLM. À 70B, vous saturerez la plupart des points de référence.

C'est pourquoi Qwen2.5VL-72B et Claude Opus 4.7 écrasent MMMU-Pro et ScreenSpot-Pro: le cerveau du langage est énorme. Un VLM 7B ne peut pas remplacer un VLM 70B grâce à une conception intelligente de connecteur.

> **【中文解读】**Le nombre de personnes qui ont été interrogées par le logiciel est de plus en plus élevé. Il est possible de calculer les données de l'analyse de l'analyse de l'analyse de données.

### Axe 4: données  détails des légendes humaines surpassent la distillation DATA:

Molmo + PixMo (Deitke et coll., 2024) est le résultat 2024 que tout le monde devrait lire. Allen AI a demandé aux annotateurs humains de décrire les images en 1-3 minutes de passages de parole à texte denses, ce qui a donné 712K d'images sous-titrées denses. Aucune distillation GPT-4V nulle part dans les données de formation.

Molmo-72B bat Llama-3.2-90B-Vision sur 11 des 11 critères de référence. Le delta n'est pas une architecture  c'est la qualité des légendes. Les légendes détaillées contenant 5-10 fois plus d'informations par image que les légendes courtes et restent basées sur des faits où la distillation GPT-4V hallucine.

ShareGPT4V (Chen et coll., 2023) et Cauldron (Idefics2) ont suivi le même manuel avec des sous-titres humains + GPT-4V mixtes.

> **【中文解读】**Le fond de Molmo: faire en sorte que les marqueurs humains utilisent des images de description intensive de 1-3 minutes, obtiennent des images de marque de qualité supérieure à 712K, complètement sans utiliser GPT-4V 蒸── Molmo-72B sur le 11/11 基准 a battu Llama-3.2-90B-Vision── la différence n'est pas une structure qui décrit la qualité── détail de l'image de description de l'information est de 5-10 fois plus rapide que la description du réseau, et il est vrai, pas comme GPT-4V   données "récipient" du fantasme──

> **【拓展：数据质量的投资回报】**Cette découverte est une révélation importante pour le VLM dans le domaine vertical de la construction: elle coûte beaucoup de temps à la planification de l'architecture, mais elle ne sert pas à investir des ressources pour obtenir des données de haute qualité dans le domaine. Dans le cadre financier, les résultats sont beaucoup plus efficaces que ceux obtenus par GPT-4V, en utilisant des formules de signalisation, des émissions et des images de contrat.

### Axe 5: résolution et son horaire, résolution et régulation.

Les ablations d'Idefics2: 384 -> 448 ajoute 1-2 points. 448 -> 980 avec la fraction d'image (AnyRes) ajoute encore 3-5 sur les benchmarks OCR. Plateaux de formation à haute résolution à une précision moyenne; rampe de résolution (début 224, fin 448 ou natif) trains plus rapide et finit plus haut.

Cambrian-1 a effectué un trade-off résolution vs. tokens: au calcul fixe, vous pouvez avoir plus de tokens à résolution inférieure ou moins de tokens à résolution plus élevée.

La recette de production 2026: train étape 1 à 384 fixes, étape 2 avec résolution dynamique jusqu'à 1280 pour les tâches lourdes en matière de RCO.

> **【中文解读】**La résolution augmente de 384 à 448 à 1-2,448 à 980 avec la résolution de 3 à 5 dans le cadre OCR.

### La comparaison prismatique contrôlée prismatique contrôle par rapport à l' expérience

Prismatic VLMs (Karamcheti et coll., 2024) est le document qui a contrôlé tous les axes.

- Le nombre de jetons visuels par image explique environ 60% de la variance.
- Le choix du codeur explique ~ 20%.
- L'architecture de connecteur explique ~5%.
- Tout le reste (mix de données, planificateur, LR) le reste ~15%.

C'est une décomposition grossière, mais c'est la réponse la plus claire à "ce que je devrais ablation d'abord" dans la littérature.

> **【中文解读】**Les VLM prismatiques sont les expériences de contrôle les plus propres  les mêmes 13B LLM  les mêmes instructions  les mêmes évaluations, chaque fois seulement un seul axe  Conclusion:

### Un choix pour 2026

Compte tenu des preuves, la recette par défaut de VLM ouvert pour un nouveau projet en 2026:

- Encoder / 编码器: SigLIP 2 SO400m/14 à résolution native avec NaFlex, concaténée avec DINOv2 ViT-g/14 pour des caractéristiques denses si vous avez besoin de segmentation / grounding / 如需分割/定位则拼接 DINOv2.
- Connecteur / 连接器: 2 couches MLP sur les jetons de patch.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B pour le coût / 成本优先选7B, 70B pour la qualité / 质量优先选70B, sélectionné par latence cible / 按延迟目标选择.
- Données / données: PixMo + ShareGPT4V + Cauldron, complété par des données d'instructions spécifiques à la tâche / 补充任务特定指令数据.
- Résolution / résolution: dynamique (min 256, max 1280 pixels par côté long) / 动态(minimum256, max 1280像素每长边).
- Étapes de l'affichage: 1ère étape (projecteur seulement / 仅投影器), 2ème étape, mise en forme complète / 全参数微调, 3ème étape, mise en forme spécifique à la tâche / 任务特定微调.

Chacune de ces défauts remonte à une ablation mesurée dans les documents cités à la fin de cette leçon.

> **【中文解读】**Les résultats de chaque sélection par défaut remontent au résultat de l'expérience de désintégration dans le document cité dans le présent article.

## Utilisez-le en pratique
```figure
l5-vlm-recipe-knobs
```

## Utilisez-le

`code/main.py`est un analyseur de table d'ablation et un sélecteur de recettes. Il encode les tables d'ablation MM1 et Idefics2 (condensé) et vous permet de demander:

- "Compte tenu du budget X et de la tâche Y, quelle recette gagne?"
- "Si je change SigLIP pour CLIP sur un 7B Llama, quel est le delta MMMU attendu?"
- "Quel axe dois-je abler d'abord pour une réponse de confiance de 80%?"

La sortie est une liste de recettes classées avec des delta de référence attendues et une recommandation "ablate first".

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-vlm-recipe-picker.md`. Compte tenu d'un mix de tâches cibles, d'un budget de calcul et d'un objectif de latence, il émet une recette complète (encodeur, connecteur, LLM, mix de données, calendrier de résolution) avec des citations à l'ablation qui justifie chaque choix.

> **【中文解读】**Le projet de VLM est un projet de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de l'équipement de construction de construction de l'équipement de construction de construction de l'équipement de construction de construction de l'équipement de construction de construction de l'équipement.

## Les exercices

1. Pour un LLM 2B fixe à 50 millions d'images, quel codeur gagne ?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1 constate que la concaténation DINOv2 + SigLIP dépasse les résultats des critères de référence centrés sur la vision mais n'ajoute aucun signal sur MMMU.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. Votre cible est un agent d'interface utilisateur mobile sur un 2B LLM. Choisissez un encodeur, un connecteur, une résolution et un mélange de données.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo produit des modèles 4B et 72B. Le 4B est compétitif avec les VLM fermés 7B; le 72B bat Llama-3.2-90B-Vision sur les critères de référence 11/11.
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. Conçuez un tableau d'ablation pour isoler la qualité du mélange de données de la qualité du codeur sur un VLM 7B. Combien de sessions d'entraînement minimum?
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## Encore une lecture

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611)Je suis un homme qui a des problèmes avec la technologie.
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Facteurs clés de la construction de VLM
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146)Je suis un homme qui a des problèmes avec les gens.
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860)Je suis un homme qui a des problèmes avec le codeur Cambrian-1
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)Je suis un homme qui a des problèmes de santé.
