# CLIP et la formation de la langue de vision contrastée

> Le CLIP d'OpenAI (2021) a prouvé une idée suffisamment grande pour alimenter les cinq prochaines années: aligner un encodeur d'image et un encodeur de texte dans le même espace vectoriel en utilisant uniquement des paires bruyantes de sous-titres d'image Web et une perte de contraste. Zéro étiquette supervisée. 400 millions de paires. L'espace d'intégration résultant fait une classification à zéro coup, une récupération d'image-texte et se connecte à chaque VLM en 2026 comme sa tour de vision. SigLIP 2 (2025) a remplacé softmax par sigmoid et a été supprimé par CLIP à moindre coût. Cette leçon passe les maths de InfoNCE à la perte par paire sigmoid et construit l'étape d'entraînement en stdlib Python.

> **【中文解读】**CLIP utilise 400 millions de pages de données en ligne pour, par rapport à la perte de données, le code des images et du texte dans le même volume de l'espace.

> **【拓展：CLIP→多模态大模型】**Le tableau de CLIP est la base de l'étude par rapport à LLaVA, BLIP-2 et autres grands modèles.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Pour les étudiants, la phase 12 est la phase 1, la phase 11 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4, la phase 4 est la phase 4 est la phase 4, la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 et la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 est la phase 4 la phase 4 est la phase 3 est la phase 3 est la phase 3 est la phase 3 est la phase 3 est la phase 3 est la phase 3 est la phase 3
>  **【类比】**CLIP 訓練 = "中外文词典配对游戏"── donner 32k à la photo, la description), laisser le modèle de l'école de chaque image et sa propre description être portée à la même position de l'espace métrique, lancer la description des autres 31999 张图片. Après la formation, le modèle peut mettre "une photo d'un chat" et un vrai chat tiré ensemble même si le train n'a pas vu ce chat──

## Objectifs d'apprentissage

- Dériver la perte d'InfoNCE à partir d'informations mutuelles et mettre en œuvre une version vectoriée numériquement stable.
  Le texte de l'article est basé sur le texte de la loi de l'Union européenne.
- Expliquez pourquoi la perte par paire sigmoïde (SigLIP) s'élève à 32768+ sans les exigences de la charge générale de la douceur max.
  Le nombre de paquets de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de frais de
- Exécuter la classification ImageNet à tirage nul en construisant des modèles de texte (`a photo of a {class}`) et de prendre argmax par rapport à la similitude cosine.
  Le texte est écrit en français.`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 ImageNet 分类。
- Nommez les quatre leviers que vous donne la pré-entraînement CLIP / SigLIP: taille de lot, température, modèle de demande, qualité des données.
  Le groupe de formation de formation de classe moyenne est composé de quatre groupes de formation de classe moyenne.

## Le problème , l' introduction du problème

La vision pré-CLIP était supervisée. Collectez des ensembles de données étiquetés (ImageNet: 1.2M images, 1000 classes), entraînez une CNN, expédez-la. Les étiquettes sont chères, les étiquettes sont biaisées à ce que les étiquetteurs peuvent se mettre d'accord sur, et les étiquettes ne sont pas transférées à de nouvelles tâches sans ajustement.

> Le système de surveillance de l'étiquette est un système de surveillance de l'étiquette. Il est également possible de déployer des étiquettes de marqueurs qui ne peuvent pas être transférés à de nouvelles tâches.

Le site Web de sous-titres d'images dispose gratuitement de plus d'un milliard de paires étiquetées librement. Une photo d'un retriever doré avec un texte alternatif " mon chien Max dans le parc " porte un signal de surveillance  le texte décrit l'image.

> Il y a plus d'un milliard de photos de chiens de chasse en ligne disponibles gratuitement. Une photo de chiens de chasse en argent avec un autre texte "Mon chien Max dans le parc" a apporté un signal de surveillance.

La réponse de CLIP: traiter les paires d'images-titres comme une tâche correspondante. Compte tenu d'un lot d'images N et de titres N, apprenez à correspondre chaque image à sa propre légende contre les distracteurs N-1. La supervision est " ces deux choses appartiennent ensemble; ces N-1 ne le font pas. " Aucune étiquette de classe. Aucune annotation humaine.

> Réponse de CLIP: donner un ensemble de N 张图像和 N 条描述, apprendre dans N-1 干扰项目将每图像匹配自己的描述――监督信号是" ces deux choses appartiennent ensemble; cette N-1 个不属于"―― pas de catégorie de marque, pas de marque artificielle, seulement de perte de comparaison――

L'espace d'embedding résultant fait plus que CLIP a été formé pour. ImageNet fonctionne à zéro tir parce que "une photo d'un chat" est intégrée à proximité d'images de chats qui n'ont jamais été explicitement étiquetés chats. C'est le pari qui a engendré chaque 2026 VLM.

> 得到的嵌入空间 dépassait l'objectif de formation de CLIP.  ImageNet 零样本分类有效, parce qu'"une photo d'un chat " est emballée jusqu'à ce qu'elle ne soit jamais clairement marquée pour une image de chat de chat.

## Le concept de base.

> **【中文解读】**CLIP(Contrastative Language-Image Pre-training) par le biais de l'apprentissage comparatif, les images et le texte seront cartographiés dans le même volume de espace: images correspondantes à la distance proche, non correspondantes à la distance. CLIP, après avoir été formé à 4 milliards de images, sans micro-modulation, est la base de la capacité de la division d'images à zéro.

> **【拓展：CLIP 的应用生态】**Le modèle de comparaison de CLIP a généré une grande application: DALL-E 2/3 avec CLIP pour la génération d'images, Diffusion stable avec OpenCLIP comme filtre de sécurité, LLaVA avec CLIP pour le codeur vidéo connexion LLM et compréhension d'images.


> **【拓展：CLIP 的 zero-shot 能力】**La capacité la plus étonnante de CLIP est de tirer zéro, la classe ne nécessite aucun données de formation des missions de sortie, il suffit de donner un nom de classe.


### Le double encodeur

CLIP a deux tours:

> Il y a deux tours.

- Encodeur d' image `f`: ViT ou ResNet, produit un vecteur D-dim par image.
  Le codeur de l'image`f`:VIT ou ResNet, chaque image en sort d'une D 维向量
- Encodeur de texte `g`: petit transformateur, produit un vecteur D-dim par sous-titre.
  Le rédacteur en chef`g`:Milleur transformateur, chaque article décrit la production d'un D 维向量

Les deux tours normalisent leurs sorties à la longueur d'unité.`cos(f(x), g(y)) = f(x)^T g(y)`puisque les deux sont la norme de l'unité.

> Les deux tours seront exportés en unité de longueur.`cos(f(x), g(y)) = f(x)^T g(y)`Parce que les deux sont unités de volume.

> ️ **【易错点】**忘归一化 (L2 normaliser) 关于计算相似度 → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必须`f = f / ||f||`Je ne sais pas .`cos`Il y a une autre.
> 🤔 **【困惑】**Q: Pourquoi utiliser l'équivalence des restes sans utiliser la distance d'O?A: Le restes ne regardent que dans la direction et ne regardent pas le modèle, à l'image "lumière différente mais le même contenu" est un peu différent; la distance d'O est dirigée par le modèle de la masse.

Pour un lot de paires N (image, sous-titre), construire la similitude矩阵 `S`de forme `(N, N)`- Le numéro de la liste:

> Pour un groupe de N 个 (图像, description)`(N, N)`La même chose.`S`- Le numéro de la liste:

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

où `tau`est une température apprise (CLIP s'initialise à 0,07; apprise dans l'espace log).

> Parmi eux `tau`C'est un paramètre de température appréciable (CLIP initiale est de 0,07; dans le temps de l'espace numérique)

### Perte de l'infoNCE

CLIP utilise une entropie croisée symétrique sur les lignes et les colonnes:

> CLIP pour les lignes et les lignes utilisées pour les lignes de transport:

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

Le softmax de la CE force chaque image à correspondre à sa légende plus que toutes les autres légendes du lot. Les " négatifs " sont tous les autres articles du lot.

> C'est le softmax de l'InfoNCE──CE  Forcez chaque image à correspondre à votre description plus que toutes les autres descriptions de la série ‒ "échantillon négatif" est l'ensemble des autres éléments de la série ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif" ‒ "échantillon négatif"

> ️ **【易错点】**L'équipe de formation de la formation de la formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation
>  **【类比】**InfoNCE 像"找卧底游戏":32k 张图片对应 32k 个描述, chaque image doit trouver son propre vrai partenaire dans un tas de descriptions.

### Température

`tau`La couche de la couche de la couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de couche de

> `tau`控制 softmax 的度──低 tau → 尖分布,具有难负例挖掘效果──高 tau → 平滑,所有样本都有贡献──CLIP 学习 log(1/tau),并剪剪以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替补──

### Pourquoi les sigmoïdes sont mieux étalés (SigLIP)

Softmax a besoin de la matrice de similitude entière en synchronisation. Dans la formation distribuée, vous devez rassembler tous les intégrations à chaque réplique, puis faire le softmax.

> Softmax  nécessite l'ensemble de la matrice de similitude avec le même rythme. Dans l'entraînement distribué, vous devez intégrer chaque partie dans chaque partie, puis faire softmax.

SigLIP remplace softmax par un sigmoïde à base d' éléments: pour chaque paire `(i, j)`, la perte est une classification binaire de "sont-ce la paire correspondante?" les étiquettes de classe positive sont la diagonale, tout le reste est négatif.

> SigLIP avec chaque élément sigmoïde  remplacement de la douce max: pour chaque`(i, j)`, la perte est à la " sont-elles correspondantes ? "

> 🤔 **【困惑】**Q: Pourquoi softmax  nécessite tout-assembler alors que sigmoid  不需要?A: softmax 的分母是" tous les N2 个配对的相似度之和 ", chaque GPU 必须看到全部; sigmoid 只看每个 (i,j) 配对独立判断是/否匹配,不依赖全局信息──多 GPU 训练时 sigmoid 损失可以本地计算后减少──
>  **【类比】**InfoNCE = "32k 選 1 選題", doit regarder le livre complet 張卷子才能做; SigLIP = "32k 个判断题 (((这对配对吗?) ", chaque réponse indépendante.

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`si `i == j`Chaque GPU calcule son bloc local et ses sommes. SigLIP 2 évolue à 32k-512k à moindre coût où CLIP aurait besoin d'une communication proportionnelle plus grande.

> `y_ij = 1`Si `i == j`Les données de chaque processeur sont indépendantes, sans besoin de collecte. Chaque GPU peut calculer son propre bloc et obtenir et obtenir. SigLIP 2 peut être étendu à un coût réduit à 32k-512k lots, tandis que CLIP nécessite une correspondance plus de communication.

### Classification à tir zéro

En fonction des noms de classes N, construire un modèle de texte pour chaque classe:

> 给定 N 个类名称, pour chaque catégorie

```
"a photo of a {class}"
```

Embed chaque modèle avec le codeur de texte. Embed votre image avec le codeur d'image. Argmax cosine similarité = classe prévue. Aucune formation sur les classes cibles.

> Utilisation du codeur de texte dans chaque modèle. Utilisation du codeur d'image dans l'image.

> ️ **【易错点】** directement `"cat"`作为提示 → 比 `"a photo of a cat"`差 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整句子,单词作为提示会让分布偏移──修复:始终使用模板 单词作为提示会让分布偏移──修复:始终使用模板`"a photo of a {class}"`Je suis en train de faire un peu mieux.
> 🤔 **【困惑】**Q: ImageNet 1000 类全算一遍文嵌入 不是很慢吗?A: 仅算一次然后缓存──1000 个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000 次余弦相似度(向量化矩阵乘)──

Les modèles rapides sont importants. Le papier original de CLIP utilisait 80 modèles par classe (plain, artistique, photo, peinture, etc.) et comptait en moyenne les emblèmes. +3 points ImageNet. L'utilisation moderne choisit généralement un ou deux modèles.

> 提示模板很重要──CLIP Originiels theses utilisent 80 modèles par classe (普通、艺术、照片、绘画等) et sont en moyenne placés dans le réseau.

### Sondes linéaires et réglages fin

La mise à jour est une ligne de base. Une sonde linéaire (traîne une couche linéaire sur les fonctionnalités CLIP gelées pour vos classes cibles) bat la mise à jour zéro sur les tâches dans le domaine.

> 零样本是基线――线性探测(在结的 CLIP特征之上为目标类训练一线性层) sur des tâches dans le domaine dépassant 零样本――全量微调在域内超越线性探测,但可能损害零样本迁移――三种模式,三种权衡――

### SigLIP 2: NaFlex et caractéristiques denses

SigLIP 2 (2025) ajoute:

> Siglip 2(2025) Ajouté:

- NaFlex: un modèle unique gère des ratios d'aspect et des résolutions variables.
  NaFlex: un modèle de traitement à grande échelle et à grande résolution.
- Meilleures caractéristiques denses pour la segmentation et l'estimation de la profondeur, ciblant l'utilisation comme colonne vertébrale gelée dans les VLM.
  Le but est de créer un réseau de données de base en tant que réseau de données de base.
- Multilingue: formé à plus de 100 langues où le CLIP était uniquement anglais.
  Le CLIP est uniquement réservé à l'anglais.
- 1B paramétrage où CLIP a atteint le sommet à 400M.
  Le nombre de paramètres est de 10 milliards, tandis que le CLIP est de 4 milliards.

En 2026 VLMs ouverts, SigLIP 2 SO400m/14 est la tour de vision par défaut. CLIP reste la norme par défaut pour la récupération de texte d'image pure où la distribution de formation spécifique LAION-2B correspond à votre modèle de requête.

> Dans le VLM ouvert en 2026, SigLIP 2 SO400m/14 est toujours un choix par défaut dans les recherches de texte pur, en particulier lorsque la distribution de formation de LAION-2B correspond à votre modèle de recherche.

### Les produits de base sont les produits de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de

ALIGN (Google, 2021): la même idée que CLIP, 1,8B paire d'échelle, 90% bruyant. Évalué de la taille bruyante des données. OpenCLIP (LAION): reproduction ouverte de CLIP sur LAION-400M / 2B, échelles multiples, le point de contrôle aller à ouvrir. EVA-CLIP: initializes à partir de la modélisation d'images masquées; forte colonne vertébrale pour VLMs. BASIC: Google CLIP+ALIGN hybride. Toutes la même famille, différentes données et réglage.

> ALIGN(Google,2021): idée similaire à CLIP, 18 milliards à l'échelle, 90% de données sonores.

### Le plafond de tir zéro

Les modèles CLIP classent environ 76% de capture zéro ImageNet (CLIP-G, OpenCLIP-G). Au-delà nécessite soit des données beaucoup plus grandes (SigLIP 2 obtient 80% +) ou des changements d'architecture (têtes supervisées, plus de paramètres).

> Le niveau de CLIP est supérieur à celui de la classe de CLIP. Il est nécessaire de dépasser ce niveau pour obtenir des données plus grandes.

> 🤔 **【困惑】**1) Pourquoi le CLIP est-il à zéro-shot incapable de comprendre "que font les deux personnes dans le diagramme" comme GPT-4 ?

## Utilisez-le avec le cadre de réalisation
```figure
multimodal-fusion
```

## Utilisez-le

`code/main.py`les implémentations:

> `code/main.py`实现:

1. Un codeur à double encodeur de jouets (fonctionnalités d'image basées sur des hashtags, fonctions de graphiques de texte) afin que vous puissiez voir la forme InfoNCE sans numpy.
   Le codeur est basé sur les caractéristiques d'images de la page.
2. Perte de l'infoNCE dans le Python pur (stabilité numérique par log-sum-exp).
   Le code de base de l'information est un code de base de données qui est utilisé pour la mise en œuvre de la base de données.
3. Perte par paire sigmoïde pour comparaison.
   Le sigmoïde 成对损失用于对比.
4. Une routine de classification à tir zéro: calculer la similitude cosine contre un ensemble de textes, argmax pour la prédiction.
   Le calcul est un processus de calcul qui est le plus souvent utilisé pour calculer les différences entre les différences de résolution et les différences de résolution.

Les chiffres absolus sont des jouets, la forme correspond à ce qu'un véritable entraîneur CLIP émet.

> 运行它并观察损失曲线──绝对数值是玩具级的;但形状与真实CLIP 训练机的输出匹配──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-clip-zero-shot.md`. Compte tenu d'un ensemble d'images (via chemin) et d'une liste de classes cibles, il crée des invites de texte avec le modèle CLIP, intègre les deux côtés avec un point de contrôle indiqué (p. ex., `openai/clip-vit-large-patch14`La compétence refuse de faire des revendications sur les classes qui ne figurent pas dans la liste de réponse.

> 本课产 出 `outputs/skill-clip-zero-shot.md` donner un groupe d'images (à travers le chemin) et un groupe d'objectifs (à travers le chemin)`openai/clip-vit-large-patch14`) est inséré sur les deux côtés, et revient avec un nombre de similitudes de haut-1 / haut-5  prédiction。 cette compétence  refuse absolument de faire des jugements dans les catégories de la liste de suggestions 

## Les exercices

1. Implémenter InfoNCE pour un lot de 4 paires à la main. Construire la matrice de similitude 4x4, exécuter softmax, choisir la diagonale, calculer l'entropie croisée. Vérifiez votre Python mise en œuvre contre ce calcul à la main.
   Le modèle de l'InfoNCE, construit une matrice de similitude 4x4, fonctionne à la plus grande vitesse, utilise le calcul de l'angle.

2. SigLIP utilise un paramètre de biais `b`en plus de la température: `S'[i,j] = S[i,j]/tau + b`Quel rôle ?`b`Les résultats de la recherche ont été analysés dans le cadre de la recherche sur les résultats de la recherche.
   L'utilisation de paramètres de position partagée`b`- Le numéro de la liste:`S'[i,j] = S[i,j]/tau + b`◊ lorsque les lots sont nombreux à avoir des inégalités (en moyenne, les échantillons négatifs sont plus nombreux que les échantillons réels),`b`Il est donc possible de faire une demande de règlement.

3. Construisez un classifiateur de cats contre chiens.`a photo of a {class}`et `a picture of a {class}`- Mesurer la précision sur 100 images de test.
   Le mot "cat" est traduit par "cat" en français.`a photo of a {class}`et `a picture of a {class}`◊ Le taux de précision de mesure sur 100 张测试图像―― est l'intégration de modèles supérieure à celle d'un seul modèle?

4. Comptez le coût de communication de softmax InfoNCE vs sigmoid par paire pour une course à 512 GPU à 32k lots.
   Le nombre de données de l'information par rapport à l'information partagée par le système de signalisation est de 32 000 à 32 000 sous-tits.

5. Lisez le document OpenCLIP sur les lois d'échelle (arXiv:2212.07143, Cherti et al.).
   Le tableau de bord révèle les conclusions de l'expansion des données: quel est le rapport entre le taux de précision de l'imageNet et le taux de précision de l'échantillon de l'imageNet ?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Encore une lecture

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020) le document CLIP.
  Le texte de la loi est le texte de la loi.
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) SigLIP.
  Le texte de la lettre de la première lettre est écrit en français.
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) multilingue + NaFlex.
  Le mot grec traduit par " langue " est " langue " et " langue " est " langue " .
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) étaler avec des données web bruyantes.
  Le nombre de personnes concernées est de plus de 100 000 personnes.
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) Loi sur l'élargissement de l'OpenCLIP.
  Le code de la loi est un code de la loi.
