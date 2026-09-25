# Modèles de langage vidéo: Tokens temporels et de fondation.

> La vidéo n'est pas une pile de photos. Un clip de 5 secondes a un ordre causal, des verbes d'action et un calendrier d'événement qu'un modèle d'image ne peut pas représenter. Video-LLaMA (Zhang et coll., juin 2023) a expédié le premier open video-LLM avec fondation audiovisuelle. VideoChat et Video-LLaVA ont étalé le modèle. En 2025, le TMRoPE de Qwen2.5-VL a fermé le fossé avec les modèles de propriété frontalière. Chaque système a résolu les jetons temporels différemment  Q-former par clip, concat-pool par frame, TMRoPE par jeton. Cette leçon lit les modèles, construit un échantillonneur de cadre uniforme contre dynamique et évalue les tâches de mise à terre temporelle.

> **【中文解读】**视频不是一堆照片的堆积──5 secondes de courte vidéo contient l'ordre de conséquences、动作动词和事件时间信息, c'est l'image modèle incapable de représenter──De la vidéo-LLaMA(2023) à Qwen2.5-VL(2025), le cœur de la vidéo VLM est dans la position du temps TMRoPE 让模型能看到"4.2 secondes"而不是"第15 "──

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

>  **【前置】**Le programme est basé sur la mise en œuvre de la stratégie de développement de la technologie de l'information et de l'information (FAS) et est basé sur la mise en œuvre de la stratégie de développement de l'information et de la communication.
>  **【类比】**视频 VLM 处理时间维度 = "看足球比赛回放"──均采样 = 每 10 秒截一(错过进球瞬间);事件驱动采样 = 进球时密集采样+其他时间稀疏(捕捉关键时刻);动态 FPS = 根据画面变化自动调度──TMRoPE 让模型能理解"4.2 秒发生进球"而不是"第15 ", c'est la clé de la compréhension de la vidéo de la catégorie produit──

## Objectifs d'apprentissage

- Expliquez pourquoi le codage positionnel temporel modifie les performances de la vidéo VLM indépendamment du codageur de vision.
  Traduction anglaise: expliquer pourquoi le temps de position de code est indépendant du codeur de vision qui influence le VLM.
- Comparer l'échantillonnage uniforme, dynamique-FPS et événement-driven de cadres sur les jetons-par seconde par rapport à la précision de mise à terre.
  Le taux de débit de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur est est est est est est est est est est est de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la
- Décrivez les conceptions Q-ex-per-clip (Video-LLaMA) vs. pooled-per-frame (Video-LLaVA) vs. M-RoPE-per-token (Qwen2.5-VL).
  Le film est un film de cinéma réalisé par le cinéaste américain John H.
- Nombre des quatre critères de référence pour la vidéo: VideoMME, TempCompass, EgoSchema, Video-MMMU.
  Le projet de loi de la loi de l'Union européenne sur les droits de l'homme est une loi de l'Union européenne sur les droits de l'homme.

## Le problème , l' introduction du problème

Une vidéo de 1 minute à 30 FPS est de 1800 images. À 196 jetons visuels par image (ViT-B à 224), c'est 352k jetons  plus gros que tout contexte LLM de l'ère 2024.

> 1 minute 30 FPS de vidéo avec 1800 ── en 196 视频代币 (ViT-B en 224 分辨率下) calculé, le total de 352k de jetons  dépasse la longueur de n'importe quel LLM de 2024 ──

> **【中文解读】**1 min 30FPS de vidéo a 1800 , 196  jetons visuels, un total de 352k de jetons loin de 2024 LLM de la fenêtre ci-dessus.

Il existe trois stratégies de réduction:

> 3 stratégies de compression:

1. Les cadres de sous-échantillons (1-8 FPS selon le contenu).
   Le contenu est de 1 à 8 FPS.
2. Rassembler les jetons de patch de chaque cadre de manière agressive (3x3 ou 4x4 bilinéaires).
   Pour chaque patch, il faut effectuer une activation de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en.
3. Comprimez par un Q-former qui prend un clip de 16 cadres et sort 64 jetons.
   Le film est sorti en version originale en version originale.

Chaque trade-off est différent. le sous-échantillonnage perd les détails temporels. le pooling perd les détails spatiaux. le Q-former perd un peu les deux mais économise des jetons.

> Chaque poids est différent. Chaque poids est différent. Chaque poids est différent. Chaque poids est différent.

Le codeur de position temporelle est l'autre axe: comment le modèle sait-il que le cadre 5 est venu avant le cadre 6 ? Les options incluent le simple RoPE temporel 1D (Video-LLaMA), les emblèmes temporels apprises (Video-LLaVA) et le TMRoPE (Qwen2.5-VL, 3D complet).

> 时间位置编码是另一个维度:模型怎么知道第5 在第6 之前?选项包括简单的1D 时间 RoPE(Video-LLaMA)、可学习时间嵌入(Video-LLaVA) 和TMRoPE(Qwen2.5-VL,完整3D)。

## Le concept de base.

> **【中文解读】**Le temps de référence est le temps de référence de la description de la langue dans le cadre de la vidéo.

> **【拓展：时序定位的应用场景】**La technique est largement utilisée dans les domaines de la recherche vidéo, de la compilation automatique, de l'analyse de la situation, de la sécurité et de la surveillance.


### Vidéo-LLaMA: Q-former par clip + branche audio

Le vidéo-LLMA (2023) est le premier vidéo-LLM ouvert.

> Vidéo-LLaMA(2023) est la première vidéo ouverte de la LLL.

- Des clips de 16 images à 2 FPS (jusqu'à 8 secondes).
  Le texte est en français.
- Les fonctionnalités ViT par cadre -> Video Q-former qui intervient sur les 16 cadres -> 32 requêtes apprises -> LLM.
  Le premier est le premier, qui est le premier, qui est le premier.
- Branche audio parallèle: forme d'onde -> encodeur audio ImageBind -> Audio Q-former -> 32 requêtes -> LLM.
  Le lien est lié à l'image.

La force: raisonnement articulaire audiovisuel.

> 优势:音视频联合推理――劣势: fixe片段长度, incapable de faire un temps déterminé―

### VidéoChat et Vidéo-LLaVA

VideoChat a gardé l'idée de Video-LLaMA mais a abandonné l'audio et simplifié. Video-LLaVA (Lin et coll., 2023) a formé un seul encodeur visuel sur les images et les cadres vidéo ("alignement avant la projection"), donnant une représentation unifiée.

> Le vidéochat a conservé la pensée de la vidéo-LLaMA mais a supprimé le son et simplifié la diffusion.

Aucun ne peut traiter de longues vidéos.

> Les deux ne peuvent pas traiter le long de la vidéo.

### Qwen2,5-VL et TMRoPE

Qwen2.5-VL introduit TMRoPE  Embedding de position rotative temporelle-modalité. Chaque jeton de patch porte une position (t, h, w) où t est le timestamp réel (pas l'index du cadre).

> Qwen2.5-VL  introduit TMRoPE temps-模态旋转位置编码──每个补丁代币 携带 (t, h, w) 位置, dont t est le temps réel(非索引)──

Différences clés par rapport à l'intégration temporelle simple:

> Les différences clés avec Simple Time:

- Le modèle voit "à 4,2 secondes" et non "à 15".
  Le modèle vu est "4,2 secondes" et non "15e "。
- Chaque jeton visuel tourne indépendamment par son timestamp.
  Chaque vidéo est tournée indépendamment.
- Si vous prenez un échantillon à 2 FPS ici et 4 FPS là, TMRoPE gère l'espacement inégalitaire de manière native.
  Le même type de traitement est utilisé pour la gestion de la chaleur.

TMRoPE permet de " à quelle seconde le chat saute-t-il ? " Le modèle peut sortir " à 4,2 secondes. " Video-LLaMA ne pouvait dire que " tôt dans le clip. "

> TMRoPE 支持"Cat dans quelques secondes saute ?"

> **【中文解读】**TMRoPE est une innovation clé de Qwen2.5 VL: chaque jeton de vision porte (t, h, w) information de position, dont t est le temps réel et non l'indice. Cela signifie que le modèle voit ce qui est "4,2 secondes" plutôt que "15" et peut traiter naturellement les évolutions  rate   de temps intervalle  .

> **【拓展：TMRoPE 在金融视频分析中的应用】**La capacité de positionnement en temps absolu de TMRoPE est essentielle pour le scénario financier: lors de la vidéo de la réunion de publication de l'analyse financière, on peut déterminer avec précision le lieu de "le PDG a mentionné la croissance des revenus"; lors de la vidéo de surveillance des transactions, on peut marquer les points de temps d'événements étranges.

### Stratégies de prélèvement d'échantillons

Unique: l'échantillon N cadres uniformément sur la durée.

> 均采样: 在时长内均采样 N ──简单,但丢失运动峰值──

FPS dynamique: échantillon adapté en fonction de l'intensité du mouvement.

> 动态 FPS: selon la force du mouvement, l'adaptation à la sélection de la lumière.

Événement-driven: exécuter un détecteur léger, échantillonner plus où l'action se produit.

> 事件驱动:运行轻量级检测器, 在动作发生处密集采样──VideoAgent 使用──

Tasté + contexte: échantillon aux limites des prises de vue + quelques cadres adjacents. Utilisé pour le contenu cinématographique.

> 关键 + 上下文: dans l'objectif de bordure de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface de la surface.

> **【中文解读】**La meilleure pratique pour l'année 2026 est la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026 est la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure pratique pour l'année 2026: la meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure meilleure meilleure meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure pratique est la meilleure pratique pour l'année 2026: la meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure pratique est la meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure meilleure pour le plus la meilleure pour le plus la meilleure pour le plus la meilleure pour le plus pour le plus pour le plus la meilleure pour le plus la meilleure pour le plus la meilleure pour le plus la meilleure pour le plus la meilleure pour le plus soit la meilleure pour le plus soit la meilleure pour le plus soit la meilleure soit la meilleure soit la meilleure pour le soit la meilleure soit la meilleure soit la meilleure soit la meilleure soit la meilleure soit la meilleure soit la meilleure soit la

### Rassemblement par cadre

À 1 FPS et 576 jetons par image, un clip de 5 minutes est de 172.800 jetons. Faible avec le contexte 128k de Qwen2.5-VL-72B mais coûteux.

> 1 FPS ⋅ 576 jetons ⋅ 5 minutes ⋅ 1 minute ⋅ 172.800 jetons ⋅ Qwen2.5-VL-72B ⋅ 128k ⋅ 1

Le pool bilinéaire 3x3 se réduit à 64 jetons par cadre -> 19 200 jetons pendant 5 minutes.

> 3x3 双线性池化降至每 64 jetons → 5 分钟 19,200 jetons── la plupart des tâches sont sucrées──

Les actions de base sont plus agressives (6x6 -> 16 jetons par cadre) pour les flux de travail des agents où les détails spatiaux comptent moins.

> Pour les détails de l'espace, il est important de les utiliser.

### Les quatre critères de référence vidéo

- Vidéo-MME: compréhension vidéo complète, courte + moyenne + longue.
  VidéoMME:综合视频理解,短+中+长。
- TempCompass: raisonnement temporel finement nourri, questions "avant" / "après".
  TempCompass:细粒度时间推理, "之前" / "之后"问题──
- EgoSchema: vidéo à la première personne.
  Le groupe est composé de deux groupes:
- Vidéo-MMMU: questions vidéo multimodelles et multidisciplinaires.
  Le film est un film de la série de télévision américaine.

Une évaluation vidéo-VLM complète touche les quatre. Ils soulignent différents axes  TempCompass est tout sur la commande, EgoSchema est environ 3 + minutes de raisonnement, VideoMME couvre les durées.

> 完整的视频 VLM 评估需要覆盖全部四基准──它们测试不同维度TempCompass 关注时序,EgoSchema 关注 3分钟以上的推理,VideoMME 跨越不同时长──

### Format de sortie de mise au sol

Format de sortie pour la mise à terre temporelle:

> 时序定位的输出格式:

- "Le chat saute autour de la marque de 4 secondes". Facile à analyser mais imprecise.
  Le chat est en 4 secondes ou plus.
- JSON structuré: `{"event": "jump", "start": 4.1, "end": 4.3}`Le Qwen2.5VL est équipé de ce train.
  Le texte est écrit en français.`{"event": "jump", "start": 4.1, "end": 4.3}`◊ Qwen2.5VL  entraînement dans ce format。
- Basé sur des jetons: spécial `<time>4.1</time>`Les jetons sont interconnectés avec la réponse.
  Traduction anglaise:`<time>4.1</time>`Le code de la ligne de référence est le code de la ligne de référence.

Le format de sortie JSON de Qwen2.5VL partage directement.

> Le format de JSON de Qwen2.5-VL est directement résolu.

### 2026 les meilleures pratiques

Pour les VLM vidéo en 2026:

> 2026 années vidéo VLM:

- Encodeur: SigLIP 2 avec M-RoPE ou TMRoPE (Qwen2.5-VL).
  Le code de la ligne de référence est le code de la ligne de référence.
- Prise d'échantillons de cadres: FPS dynamique (1-4 en fonction du mouvement) avec capot maximal de cadres.
  Le nombre de personnes concernées est de 1 à 4 ans.
- Le poids par cadre: 3x3 bilinéaire.
  Le mot "c'est-à-dire " est traduit par "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par " est traduit par " est traduit par " est traduit par " en français).
- Sortie: JSON structuré avec champs de temps + événement.
  Le texte de l'article est écrit en français.
- Les critères de référence: Vidéo- PME + TempCompass pour les entreprises générales; EgoSchema pour les entreprises à long terme.
  Le programme de formation est basé sur le programme de formation de formation professionnelle.

## Utilisez-le avec le cadre de réalisation
```figure
video-temporal-patches
```

## Utilisez-le

`code/main.py`comprend:

> `code/main.py`包含:

- Des échantillonnages de cadres FPS uniformes et dynamiques.
  Le système de contrôle de la circulation est un système de contrôle de la circulation.
- Un évaluateur de la fondation temporelle de jouets: étant donné un événement de "vérité fondamentale" au moment T et une sortie de modèle, la précision est notée avec tolérance.
  Un jouet en temps réel et un modèle en sort dans la gamme de la capacité.
- Une comparaison entre les vidéos-LLaMA (16 images, Q-former), Vidéos-LLaVA (8 images, MLP), Qwen2.5-VL (FPS dynamique + TMRoPE).
  Le film est en cours de réalisation et est en cours de réalisation.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-video-vlm-frame-planner.md`. En fonction d'une tâche vidéo (monitoring, reconnaissance d'action, repérage temporel, résumé), il choisit l'échantillon de cadre, le facteur de mise en commun, le format de sortie et le niveau de précision attendu.

> 本课产 出 `outputs/skill-video-vlm-frame-planner.md` donner des tâches de surveillance, d'identification des mouvements, de désignation des séries, de résumé, de sélection des échantillons, des éléments de production, des formats et des niveaux de précision prévus.

## Les exercices

1. Pour une démonstration de cuisson de 3 minutes, choisissez un FPS uniforme contre dynamique. Justifiez avec un nombre de jetons.

2. TMRoPE ajoute ce qu'une simple table d'intégration temporelle ne peut pas faire spécifiquement ? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能?

3. Écrivez un schéma JSON pour le repérage temporel qu'un VLM peut apprendre à émettre. Inclure des cas d'erreur.

4. Lisez la section 3 de Video-LLaVA sur "L'alignement avant la projection". Pourquoi est-ce mieux que de former des encoders d'image et de vidéo séparés ?

5. Compte tenu du classement des entreprises vidéo-médias, quelle est la différence entre le modèle ouvert le plus élevé et le modèle propriétaire le plus élevé en 2026? Quelle est la différence entre le codage temporel et l'échelle de base de l'LLM?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Encore une lecture

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
