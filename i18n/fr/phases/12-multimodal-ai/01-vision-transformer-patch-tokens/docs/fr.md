# Transformateurs de vision et le primitif de patch-token

> Avant tout multimodal, une image doit devenir une séquence de jetons qu'un transformateur peut manger. Le papier ViT 2020 a répondu à cela avec des patchs de 16x16 pixels, une projection linéaire et une intégration de position. Cinq ans plus tard, chaque modèle frontalier 2026 (Claude Opus 4.7 à 2576px natif, Gemini 3.1 Pro, Qwen3.5-Omni) commence toujours de cette façon  l'encodeur a changé de ViT à DINOv2 à SigLIP 2, des jetons de registre ont été ajoutés, le schéma positionnel est devenu 2D-RoPE, mais le primitif a été maintenu. Cette leçon lit le pipeline de patch-token de bout en bout et le construit en stdlib Python afin que le reste de la phase 12 ait un modèle mental concret pour les "tokens visuels".

> **【中文解读】**Avant d'entrer dans le multi-modèle, l'image doit d'abord devenir la séquence de symboles de transformateur capable de traitement.

> **【拓展：ViT Patch→多模态基础】**Le patch-Token est la base de tous les modèles de langage visuel, qu'il s'agisse d'un éditeur visuel CLIP, d'une image de LLaVA ou d'un modèle de compréhension de documents, tout commence par le patch.

>  **【前置】**Pour les utilisateurs de la technologie, il est nécessaire de se préparer à la mise en œuvre de la technologie de transformation.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objectifs d'apprentissage

- Convertir une image HxWx3 en une séquence de jetons de correction avec un codage positionnel correct.
  Le code de fichier est le code de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier de fichier.
- Comptez la longueur de la séquence, le nombre de paramètres et les FLOP pour un ViT donné (taille de patch, résolution, faible cache, profondeur).
  Le nombre de patches de la série de vitesse de longueur, de paramètres et de flops.
- Nombre des trois améliorations qui ont permis de passer la recherche de ViT de 2020 à la production de 2026: pré-entraînement auto-supervisé (DINO / MAE), jetons de registre et emballage à résolution native.
  Le nombre de personnes concernées est de 1,0 à 1,0%, et le nombre de personnes concernées est de 2,0 à 1,0 à 2,0 à 2,0 à 2,0 à 2,0 à 3,0 à 2,0 à 3,0 à 3,0 à 3,0 à 3,0 à 3,0 à 3,0 à 3,0 à 3,0 à 3,0 à 5,0 à 5,0 à 5,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à + en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne en moyenne
- Choisissez entre le pooling CLS, le pooling moyen et l'enregistrement de jetons pour une tâche en aval.
  Pour les activités de base, le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la

## Le problème , l' introduction du problème

Les transformateurs fonctionnent sur des séquences de vecteurs. Le texte est déjà une séquence (byte ou jetons). Une image est une grille 2D de pixels avec trois canaux de couleur  pas une séquence. Si vous aplanissez chaque pixel, une image RGB 224x224 devient 150,528 jetons, et l'attention personnelle à cette longueur est un non-starter (quadratique en longueur de séquence).

> Le transformateur est utilisé pour la séquence de volumes. Le texte lui-même est la séquence de volumes. Mais l'image est une image de trois couleurs qui a une traversée de 2D. Si vous équipez chaque image, une image RGB de 224x224 devient un symbole de 150.528, alors que la concentration sur cette longueur est impossible.

Les approches pré-2020 ont boulonné un extracteur de fonctionnalités de CNN sur le devant: ResNet produit une carte de fonctionnalités 7x7 de vecteurs 2048-dimension, alimente ces 49 jetons à un transformateur. Cela fonctionne mais hérite des biais de la CNN (équivalence de traduction, champs réceptifs locaux) et perd l'appétit du transformateur pour l'échelle.

> Avant 2020, la méthode était à l'avant-garde d'un extracteur de caractéristiques de CNN: ResNet produisait un diagramme de caractéristiques de 2048 dimensions de 7x7, qui donnerait ces 49 jetons à Transformer.

Dosovitskiy et al. (2020) a posé la question simple: et si nous ignorons la CNN ? Divisez l'image en patchs de taille fixe (disons 16x16 pixels), projettez chaque patch de manière linéaire dans un vecteur, ajoutez une intégration positionnelle et alimentez la séquence à un transformateur de vanille. À l'époque, c'était une vision hérétique sans convolutions. Avec suffisamment de données (JFT-300M, puis LAION) il a battu ResNet sur ImageNet et a continué à s'améliorer.

> Dosovitskiy et autres) pose une question directe: si nous sautons la CNN, cette image se divise en un patch de taille fixe (par exemple 16x16 pixels), projette chaque patch en un vecteur, ajoute le code de position, puis donne la séquence à la transformateur standard.

En 2026, la base de la première vitesse est la ViT. La tour de vision de chaque VLM à poids ouvert est un descendant (DINOv2, SigLIP 2, CLIP, EVA, InternViT). La question n'est plus " devrions-nous utiliser des patches ? " mais " quelle taille de patch, quelle résolution, quel objectif de pré-entraînement, quel codage positional ".

> En 2026, le ViT original est devenu la base incontestable de chaque VLM de la construction de la ligne de vision de son VLM.

## Le concept de base.

> **【中文解读】**Le Transformer de vision (ViT) va diviser l'image en un patch fixe de taille grande (comme 16x16 像素), chaque patch 展平后通过线性投影变成一个代币, puis, comme le Transformer en PNL, un même traitement.

> **【拓展：ViT 的影响】**Dosovitskiy et d'autres proposent en 2020 un transformateur de vitesse de test sur les images de la classe peut dépasser CNN. ViT-L/14 sur l'imageNet atteint un taux de précision de 88,5% de haut de 1%. ViT est la base du codeur visuel de plusieurs modèles de CLIP, GPT-4V, Gemini, etc.


> **【拓展：ViT 对 CNN 的优势】**L'ensemble de ViT est nettement meilleur que le sens local de CNN. Après avoir suivi des entraînements préliminaires sur ImageNet-21k, il a été utilisé dans plusieurs missions de navigation au-delà de EfficientNet et ResNet.


### Les patches en tant que jetons

En raison d' une image `x`de forme `(H, W, 3)`et une taille de patch `P`, vous taillez l' image dans une grille de `(H/P) x (W/P)`Les patchs ne se chevauchent pas.`P x P x 3`Cube de pixels. Appliquer chaque cube à un`3 P^2`Vecteur. Appliquer une projection linéaire partagée `W_E`de forme `(3 P^2, D)`pour cartographier chaque patch dans la dimension cachée du modèle `D`- Je suis désolé .

> 给定形为 `(H, W, 3)`                      `x`Et le patch est grand.`P`, va l' image être coupée pour `(H/P) x (W/P)`个不重叠的补丁 网格── chaque patch est un `P x P x 3`Le tableau de chaque carré est égal à celui de chaque carré.`3 P^2`维向量── appliqué à la forme`(3 P^2, D)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `W_E`, chaque patch sera mappé à la dimension cachée du modèle`D`Il y a une autre.

Pour la configuration canonique ViT-B/16:
- Résolution 224, taille de patch 16 → grille 14x14 → 196 jetons de patch.
  Le code de la page de référence est le code de la page de référence.
- Chaque plaque est `16 x 16 x 3 = 768`Les valeurs de pixels, projetées à `D = 768`- Je suis désolé .
  Chaque patch contient`16 x 16 x 3 = 768`个像素值, projetée à `D = 768`Il y a une autre.
- Ajoutez un apprenant `[CLS]`longueur de la séquence → symbole 197.
  En français, traduit par " ajouter un apprendre "`[CLS]`- Je suis en train de faire une petite histoire.

La projection de patch est mathématiquement identique à une convolutions 2D avec la taille du noyau `P`- Je suis en train de faire un pas .`P`, et `D`C'est ainsi que le code de production le met en œuvre  `nn.Conv2d(3, D, kernel_size=P, stride=P)`. Le cadre de la projection linéaire est conceptuel; le cadre du noyau est efficace.

> Patch  projection en mathématiques égale à la taille nucléaire`P`、步长为 `P`、 les transports en commun`D`Le code de production est ainsi réalisé.`nn.Conv2d(3, D, kernel_size=P, stride=P)` "Lineuse projection" est conceptuelle; la réalisation du volume nucléaire est très efficace

### Embeddings positionnels

Les patchs n'ont pas d'ordre inhérent  le transformateur les voit comme un sac. Les premiers ViTs ont ajouté une intégration positionnelle 1D appréciable (un vecteur de 768 dimensions par position, 197 d'entre eux).

> Le patch  n'a pas d'ordre fixe Le transformateur les considère comme un ensemble sans ordre  Les premières ViT  ont ajouté un code de position 1D à apprendre  Pour chaque position une 768 dimension ,共 197 ) .

Les dos de vision modernes utilisent 2D-RoPE (M-RoPE de Qwen2-VL, par défaut de SigLIP 2) ou des positions 2D facteurisées. 2D-RoPE fait pivoter la requête et les vecteurs clés en fonction de l'indice du patch (ligne, colonne), de sorte que le modèle infère la position 2D relative à partir de l'angle de rotation.

> Le modèle peut donc être utilisé à partir d'un angle de rotation pour déduire la position 2D.

### Les jetons CLS, les sorties regroupées et les jetons de registre

Qu'est-ce que la représentation au niveau de l'image ?

> Qu'est-ce que le tableau ?

1. `[CLS]`Le symbole CLS est le symbole de l'image hérité de BERT. utilisé par le ViT original, CLIP.
   Le mot grec traduit par " le mot grec "`[CLS]`Le code de la carte est le code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
2. La moyenne des états cachés des jetons de patch utilisés par SigLIP, DINOv2, la plupart des VLM modernes.
   Le nombre de patches est de 2,0%, et la plupart des utilisateurs de patches sont de 4,0%.
3. Les jetons de registre. Darcet et coll. (2023) ont observé que les ViTs formés sans jeton de lavage explicite développent des correctifs "artifact" de haute norme qui détournent l'attention personnelle.
   En 2023, il est observé qu'aucun symbole de victoire n'a produit un nombre élevé de "photo-image" de patch, en ajoutant 4 à 16 symbole de registre pouvant être appris.

Le choix est important pour les tâches en aval. CLS est bon pour la classification. Pour les VLM qui alimentent des jetons de patch dans un LLM, vous sautez la mise en commun entièrement  chaque patch devient un jeton d'entrée LLM. Les registres sont jetés avant la remise (ils sont des échafaudages, pas du contenu).

> Pour les fichiers de patch qui seront introduits dans le VLM de l'LLM, chaque fichier sera intégré dans le fichier de l'LLM.

### Pré-entraînement: supervisé, contrastif, masqué, autodistilé

Le ViT 2020 a été prétrainé avec une classification supervisée sur le JFT-300M. Rapidement remplacé par:

> Les cours de formation de 2020 à la ViT en JFT-300M sont remplacés par:

- CLIP (2021): texte d'image contrasté sur 400 millions de paires.
  Le texte est en cours de rédaction et est en cours de rédaction.
- MAE (2021, He et al.): masquer 75% des patchs, reconstruire les pixels. Autoservisé, fonctionne sur des images pures.
  Le code de la photo de l'image est le code de la photo de l'image.
- DINO (2021) / DINOv2 (2023): auto-destilation avec élève-enseignant, sans étiquettes, sans sous-titres. Le 2023 DINOv2 ViT-g/14 est la colonne vertébrale purement visuelle la plus forte et la norme par défaut pour les cas d'utilisation "densité de caractéristiques".
  Le modèle DINOV2 ViT-g/14 de 2023 est le plus fort du réseau de la pure vision, et il est également "密集特征" de l'utilisation de l'impression de sélection.
- SigLIP / SigLIP 2 (2023, 2025): CLIP avec une perte sigmoïde et NaFlex pour le rapport d'aspect natif. La tour de vision dominante en 2026 est ouverte VLM (Qwen, Idefics2, LLaVA-OneVision).
  Le projet de construction de la ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de

Le choix de la pré-entraînement détermine à quoi l'épine dorsale est adaptée: CLIP/SigLIP pour l'ajustement sémantique avec le texte, DINOv2 pour les caractéristiques visuelles denses, MAE comme point de départ pour la finition en aval.

> 预训练方式决定主干网络擅长什么:CLIP/SigLIP utilisé pour l'ajustement du langage du texte,DINOv2 utilisé pour les caractéristiques visuelles denses,MAE 作为下游微调的起点──

### Les lois de l'échelle

L'échelle ViT (Zhai et coll. 2022) a établi que la qualité d'une ViT obéit à des lois prévisibles en termes de taille du modèle, de taille des données et de calcul.

> ViT 缩放定律(Zhai 等人,2022) a établi la qualité de ViT suivant les règles prévisionnelles concernant le modèle de taille, la taille des données et le calcul de la quantité.

- Un modèle plus grand + plus de données → meilleure qualité.
  Le modèle est plus grand que le modèle de la qualité.
- La taille du patch est un levier sur la longueur de séquence par rapport à la fidélité. Le patch 14 (typique pour DINOv2/SigLIP SO400m) donne plus de jetons par image que le patch 16; mieux pour les tâches OCR et dense, pire pour la vitesse.
  Patch:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing:Pathing is a the firstly on the first pointed by the point that is more appropriate to the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point, but the point is more than the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the point of the
- La résolution est l'autre gros levier. passer de 224 à 384 à 512 aide presque toujours, au coût quadratique dans les FLOP.
  La résolution est un autre pilier important. De 224 à 384 et de 512 à 512 est presque toujours utile, mais les FLOP sont en double croissance.

ViT-g/14 (1B params, patch 14, résolution 224 → 256 jetons) et SigLIP SO400m/14 (400M params, patch 14) sont les deux encoders de cheval de travail pour les VLM ouverts de 2026.

> ViT-g/14(10 milliards de paramètres, patch 14, résolution 224 → 256 个代币) et SigLIP SO400m/14(4 milliards de paramètres, patch 14) sont les deux principaux codeurs de VLM ouverts en 2026:

### Le nombre de paramètres pour un ViT

Le calcul complet se fait en `code/main.py`Pour ViT-B/16 à 224:

> 完整计算见 `code/main.py`Pour ViT-B/16 en 224 résolution:

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Parquez chaque vitesse de ballon de cette façon avant de charger le point de contrôle.

> Avant le point de chargement, on peut utiliser cette méthode pour estimer chaque vitesse.

### Configuration de la production 2026

Le codeur le plus ouvert que les VLM ont utilisé en 2026 est SigLIP 2 SO400m/14 à résolution native (NaFlex).

> La plupart des éditeurs VLM en ligne de 2026 sont originaires de la résolution de la navigation de la NaFlex SigLIP 2 SO400m/14[6].

- Paramètres de 400 M.
  Le nombre de personnes concernées est de 4 milliards.
- Taille de patch 14, résolution par défaut 384 → 729 jetons de patch par image.
  Le patch est un symbole de patch.
- Pools moyen pour les tâches au niveau de l'image; tous les 729 patches coulent dans le MLL pour VQA.
  En français, les tâches de l'équipe de formation sont classées en images.
- 4 jetons de registre, jetés avant la remise de la LLM.
  Le code de l'établissement de retraite est le code de l'établissement de retraite.
- 2D-RoPE avec mise à l'échelle au niveau de l'image pour le rapport d'aspect natif.
  Le modèle de la couleur de l'image est en double.

Chaque décision de cette config remonte à un journal que vous pouvez lire.

> Chaque décision de la configuration peut être remise à l'article que vous pouvez lire.

## Utilisez-le avec le cadre de réalisation
```figure
image-patch-tokens
```

## Utilisez-le

`code/main.py`est un jeton de patch et une calculatrice géométrique. Il prend (image H, W, patch P, caché D, profondeur L) et rapporte:

> `code/main.py`Il est un jeton de patch 和几何计算器──它接收(图像 H, W, patch P, 隐藏维度 D, 深度 L)并报告:

- La forme de la grille et la longueur de la séquence après le patchage.
  Le lien est en lien avec le lien de la page de l'article.
- Sequence de jetons pour une image de jouet à 8x8 pixels synthétique (marcher à travers le chemin plat + projet).
  Le jeu est un jeu de mots.
- Le nombre de paramètres est divisé par insertion de patch, insertion de position, blocs de transformateur et tête.
  Suivant: le nombre de composants de transformateur et de tête décomposée
- Les FLOP par passe à l'avant à la résolution cible.
  Le texte de la lettre de référence est le texte de la lettre de référence.
- Un tableau de comparaison à travers ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384.
  Le nombre de personnes concernées est de 224 à 224 personnes.

Appliquez le nombre de paramètres aux numéros publiés, utilisez la taille et la résolution du patch pour connaître le coût du nombre de jetons.

> 运行它──将参数与发布数据对比──调整补丁大小和分辨率 感受代币数量成本──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-patch-geometry-reader.md`. Une configuration ViT (taille de patch, résolution, flou caché, profondeur) produit un nombre de jetons, un nombre de paramètres et une estimation VRAM avec des justifications.

> 本课产 出 `outputs/skill-patch-geometry-reader.md` Donner une configuration de ViT  patch  grandeur  résolution  dimension  profondeur), elle génère des jetons, des numéros, des paramètres et des estimations de stockage et de leur base  utiliser cette compétence chaque fois que vous choisissez un réseau de VLM                                                                                                                                                                                                                                                                                                                                                                                                                                                  

## Les exercices

1. Comptez la longueur de la séquence de patch-token pour Qwen2.5-VL à l'entrée 1280x720 native avec la taille du patch 14. Comment cela se compare-t-il à une représentation CLS seulement?
   Comment calculer Qwen2.5 VL en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en anglais en

2. Un cadre 1080p (1920x1080) au patch 14 produit combien de jetons? À 30 FPS sur une vidéo de 5 minutes, combien de jetons visuels au total? Quel coût vous économise le plus: pooling, échantillonnage de cadre ou fusion de jetons?
   Quel est le nombre de jetons produits dans le patch 14 ? À 30 FPS ? 5 minutes de vidéo, en total combien de jetons visuels ?

3. Implémenter le pooling moyen sur les jetons de patch dans Python pur. Vérifiez que le pool moyen sur 196 jetons d'une sortie DINOv2 correspond à ce que le modèle `forward`retourne lorsque vous demandez une intégration combinée.
   Le code de démarrage de la marque est utilisé pour la mise en œuvre de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de la marque de démarrage de démarrage de la marque de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de`forward`La réaction de l'équipe de réaction est de même nature.

4. Lisez la section 3 de " Les transformateurs de vision ont besoin de registres " (arXiv:2309.16588).
   Le récit de la vision transforme est un récit de la vision transforme.

5. Modifier `code/main.py`Pour soutenir le patch-n'-pack: une liste d'images de différentes résolutions étant fournie, produisez une seule séquence de package et le masque d'attention de bloc-diagonale.
   Le mot "réfléchisseur" est traduit par "réfléchisseur".`code/main.py`Pour le support du patch-n'-pack: donner un ensemble d'images à différentes résolutions, générer une séquence de coupe et un bloc pour le coin de l'écran.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Encore une lecture

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) ViT original.
  Le texte de l'article est en français.
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) MAE, pré-entraînement auto-supervisé.
  Le mot "défense" est traduit par "défense".
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) Autodistillation à grande échelle, sans étiquettes.
  Le mot "déjeuner" est traduit par "déjeuner".
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) enregistrement des jetons et analyse des artefacts.
  Le code de l'enregistrement et l'analyse de la pseudo-image.
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) la tour de vision par défaut de 2026.
  Le texte de la loi est en français.
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) les lois empiriques de l'échelle.
  En français, la langue officielle de la langue française est le français de la langue française.
