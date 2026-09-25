# Flamingo et Gated Cross-Attention pour quelques VLMs tirés

> Le Flamingo de DeepMind (2022) a fait deux choses avant quiconque. Il a montré qu'un seul modèle pouvait traiter des séquences d'images, de vidéos et de texte interdites arbitrairement. Et il a montré que les VLM pouvaient apprendre dans le contexte  donner quelques instants avec trois paires d'exemples (image, sous-titre) et le modèle sous-titre une nouvelle image sans aucune étape de gradient. Le mécanisme: couches de l'attention croisée fermées, insérées entre les couches existantes du LLM gelé, avec une porte de tanh apprise qui commence à zéro afin que la capacité de texte du LLM soit préservée lors de l'initialisation. Cette leçon traverse le ressampleur Percepteur de Flamingo et l'architecture de l'attention croisée fermée, l'ancêtre des entrées interlevées de Gémeaux et des jetons visuels d'Idefics2.

> **【中文解读】**Flamingo  Première mise en œuvre de la conception de l'écriture  Introduction et mise en œuvre de la conception de l'écriture   Introduction et mise en œuvre de la conception de l'écriture  Introduction et mise en œuvre de la conception de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre de l'écriture  Introduction et mise en œuvre  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introduction  Introd

> **【拓展：Flamingo→Gemini交织输入】**Le modèle de traitement des images de Flamingo est le modèle original des jetons visuels de Gémeaux et Idefics2, qui a été le premier modèle de la pratique littéraire.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Le projet de formation est un projet de formation de formation en ligne, qui a été créé par le projet de formation de formation en ligne et qui a été créé par le projet de formation en ligne.
>  **【类比】**Flamingo = "Entrée en ligne de chaque étage du LLM" (en anglais: Flamingo) = "Entrée en ligne de chaque étage du LLM" (en anglais: Flamingo) = "Entrée en ligne de chaque étage du LLM" (en anglais: Flamingo);

## Objectifs d'apprentissage

- Expliquez comment l'attention croisée fermée préserve la capacité de texte d'un LLM gelé à l'initialisation via tanh(gate) = 0.
  En français, le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et le nombre de personnes qui ont suivi le programme est de 0,0 et de 0,0 et de 0,0 et de 0,0 en moyenne, respectivement, de 0,6 et de 0,6 et de 0,6%.
- Passez par un ressampleur Percepteur: N patchs d'image → K fixé "latent" requêtes via l'attention croisée.
  Le modèle de percepteur: N 个图像 patch → 通过交叉注意力产生 K 个固定"潜在"查询──
- Décrivez comment Flamingo traite les séquences d'images-texte interligées avec un masquage causal qui respecte le placement de l'image.
  Le langage de la langue française est le langage de la langue française.
- Reproduire une structure de prompt multimodal de quelques coups (3 exemples de sous-titres d'image puis une image de requête).
  Le modèle de la structure de l'exemple de la page suivie d'une image de la requête.

## Le problème , l' introduction du problème

BLIP-2 alimente 32 jetons visuels dans la couche d'entrée d'un LLM gelé. Fonctionne pour une image par prompt. Mais que faire si vous voulez alimenter * beaucoup * d'images entrelacées avec du texte, comme dans " ici est l'image A, sous-titre; ici est l'image B, sous-titre; maintenant ici est l'image C, sous-titre " ? L'auto-attention du LLM devrait gérer les jetons d'image et les jetons de texte dans un seul flux, et la question de savoir quelles positions peuvent être occupées par quelles images devient agitée.

> BLIP-2 va mettre en place 32 jetons visuels 结 LLM de l'entrée de niveau. Il s'applique à chaque pointe d'une image. Mais si vous voulez entrer dans une image en relation avec le texte, par exemple "c'est une image A, décris-la; c'est une image B, décris-la; c'est une image C, décris-la"; L'auto-attention de LLM doit être traitée dans un seul flux de jetons d'image et de jetons de texte, quelles positions peuvent être prises pour les questions d'image devient difficile.

La réponse de Flamingo: ne modifiez pas du tout le flux d'entrée du LLM. Insérer des couches de croisement supplémentaires entre les blocs de LLM existants. Les jetons de texte circulent toujours à travers l'auto-attention de la LLM comme toujours. Entre quelques blocs de LLM, les jetons de texte interagissent également avec les caractéristiques de l'image via une nouvelle couche fermée. La porte (initialisée à zéro) signifie que à l'étape zéro les nouvelles couches sont sans opérations  le modèle se comporte exactement comme le LLM prétrainé. Au fur et à mesure que l'entraînement progresse, la porte s'ouvre et les informations visuelles commencent à circuler.

> Flamingo répond: totalement pas changer le flux d'entrée de LLM. Dans les blocs existants de LLM, il y a un niveau d'attention supplémentaire entre les blocs de LLM. Dans les blocs existants, il y a un niveau d'attention supplémentaire entre les blocs de LLM. Dans les blocs de LLM, il y a un niveau de contrôle supplémentaire entre les blocs de LLM.

La deuxième question Flamingo a répondu: comment gérer un nombre variable d'images (0, 1 ou plusieurs) par prompt? Un rééchantillon Perceiver  un petit module de réflexion croisée qui prend le nombre de patches que vous avez et produit un nombre fixe de jetons visifs latents. La couche d'attention croisée LLM voit la même forme indépendamment du nombre d'images dans le prompt.

> Flamingo répond à la deuxième question: comment traiter chaque pointe avec un nombre variable d'images ? 0、1 ou plusieurs张 ?

## Le concept de base.

> **【中文解读】**Flamingo (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo) (en anglais: Flamingo: Flamingo: Flamingo) (en anglais: Flamingo: Flamingo) (en) (en anglais: Flamingo: Flamingo: Flamingo: Flamingo) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (

> **【拓展：Flamingo 的高效适配】**Flamingo ️ seulement entraînement de 1% ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️


> **【拓展：门控机制的数学原理】**La mise en place de la valeur de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en en en en en œuvre de mise


### Le LLM congelé

Flamingo commence par un LLM de Chinchilla 70B gelé. Tous les poids 70B intacts.

> Le projet de loi de la loi de la Chine, Chinchilla 70B, est lancé pour mettre en place la loi de la loi de la Chine, qui prévoit des mesures de protection des droits de l'homme.

### Remplacement de l'échantillon de percepteur

Pour chaque image dans le prompt, le ViT produit N patch tokens. Le resampler Percepteur a K fixes latences apprenables (Flamingo utilise K=64).

> Pour chaque image de la pointer, ViT 产生 N 个补丁代币──Perceptor resampler has K 个固定的可学习潜在向量(Flamingo 使用 K=64)──Chaque resampler bloc a deux étapes:

> 🤔 **【困惑】**Q: Le prélèvement du prélèvement et BLIP-2 du Q-Former ont des différences ?A: 思想几乎一样(learnable query from patch 提取信息), mais Flamingo's Perceiver prélèvement ne fait que faire des caractéristiques de compréhension, ne participe pas à l'entraînement des pertes; Q-Former est un transformateur 结构且有ITC/ITM/ITG 三个损失──

1. Attention croisée: les K latences sont présentes sur les N patch tokens (Q des latences, K/V des patches).
   Le code de référence est le code de référence de la page de référence.
2. Autotentification + FFN dans les latences.
   L'attention de l'intérieur de l'énergie potentielle est plus forte que la concentration de l'énergie.

Après 6 blocs de repérage, la sortie est K = 64 jetons visuels de dim 1024, quel que soit le nombre de correctifs produits par le ViT. Une image 224x224 (196 patches) et une image 480x480 (900 patches) sortent tous deux en 64 jetons de repérage.

> Après avoir passé 6 blocs de repérage, le produit est K=64 个维度为 1024 视频代币, peu importe le nombre de patches produites par ViT.

Pour la vidéo, le resampler est appliqué temporairement: les patchs de chaque cadre produisent 64 latences, et un codage positionnel temporel permet au modèle de distinguer t=0 de t=N. La vidéo complète devient des jetons visuels T * 64.

> Pour le vidéo, échantillon  selon la taille de l'application: par patch  générer 64 潜在向量, temps position编码让模型区分 t=0 和 t=N──

### Attention croisée par voie ferrée

Entre chaque couche M du LLM gelé (Flamingo utilise M=4), insérer un nouveau bloc de l'attention croisée fermé:

> Dans le cadre de la formation de la M.L.M. entre les deux niveaux, il est possible de créer un nouveau bloc d'attention:

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`est un scalaire apprenable initialisé à zéro.
  Le mot grec traduit par " le mot grec "`alpha`C'est un échantillon à apprendre, initialement à zéro.
- `tanh(0) = 0`, donc à init la branche fermée contribue à zéro.
  Le mot grec traduit par " le mot grec "`tanh(0) = 0`, donc le temps de démarrage est de zéro.
- Comme `alpha`Si la valeur de l'attention croisée s'éloigne de zéro, elle augmente de façon fluide.
  Le mot " avec " signifie " avec " .`alpha`远离零,交叉注意力贡献平滑增长──
- La connexion résiduelle signifie que même une porte entièrement ouverte ne surécrit pas la représentation du texte du LLM; elle ajoute simplement des informations visuelles en haut.
  Le texte de la loi est ouvert et ne couvre pas le texte de la loi.

C'est le choix de conception le plus important dans Flamingo: le conditionnement visuel est additif, fermé et zéro à l'initialisation.

> C'est le choix le plus important de Flamingo: les conditions visuelles sont complémentaires, contrôlées, initiales à zéro.

> ️ **【易错点】**La formation de l'équipe de formation de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de l'équipe de formation de formation professionnelle de l'équipe de l'équipe de formation professionnelle de l'équipe de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de l'équipe de l'équipe de formation de formation de l'équipe de formation d'équipe de l'équipe de l'équipe de l'équipe de la direction de la direction de la direction de la direction de la direction
>  **【类比】**零初始化门控 = "new员工进入职模式"──新员工 (新员工) 视觉层) 第一周只观察、不说话(gate=0);熟悉业务后逐渐发言(gate 慢慢打开)──直接让新员工主导决策(gate≠0初始化)

### Attention croisée masquée pour les entrées interdites

Dans un prompt comme "<image A> caption A <image B> caption B <image C> ?", chaque jeton de texte ne doit voir que des images qui lui ont précédé dans la séquence.`t`ne prend en charge que les jetons de repérage d'image dont l'index d'image `i < i_t`où `i_t`est l' image la plus récente avant la position `t`"Voice seulement la dernière image précédente" ou "Voice toutes les images précédentes" sont tous deux des choix valides; Flamingo a choisi le premier.

> Dans le cadre de la "<image A> description A <image B> description B <image C> ?" , chaque symbole texte doit seulement voir la séquence située dans l'image précédente.`t`Les symboles de texte suivent seulement l'index d'image`i < i_t`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `i_t`est position `t`之前最近的图像──"Oncle regardez la dernière image" ou "Voir toutes les images précédentes" sont des sélections valides; Flamingo 选择前者──

### Apprendre en quelques coups dans le contexte

Une requête Flamingo ressemble à:

> Flamingo 提示 ressemble à ceci:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

Le modèle voit le schéma de finition et produit "oiseau" (ou ce que l'image3 montre). Aucune étape de gradient. La capacité d'apprentissage dans le contexte du LLM gelée traverse l'attention croisée fermée.

> Le modèle voir le modèle complet et le modèle de production de "oiseau" (ou image3) 显示的任何内容) 无需梯度步骤──结 LLM's 上下文学习能力通过门控交叉注意力传递

> 🤔 **【困惑】**Q: Pourquoi Flamingo peut apprendre dans le contexte alors que BLIP-2 ne peut pas?A: Flamingo en LLM chaque 4 niveaux injecté dans l'information visuelle,LLM  interne de l'apprentissage dans le contexte(en phase 11·05 apprendre过) est toujours en pleine tâche;BLIP-2 Place 32 jetons visuels 直接拼到即前面,LLM Placez-les comme jetons ordinaires 处理, mais l'objectif de l'entraînement n'est pas de quelques coups 模式, donc la capacité est faible.

### Données de formation

Flamingo a été formé sur trois ensembles de données:

> Flamingo dans trois ensembles de données

1. MultiModal MassiveWeb (M3W): 43 millions de pages Web avec des images et du texte interligés, reconstruisant l'ordre de lecture.
   Le site Web MassiveWeb (M3W) est en train de créer une nouvelle page Web contenant des images et des textes.
2. Pares image-texte (ALIGN + LTIP): 4,4B pares.
   Le nombre de personnes concernées est de 44 millions.
3. Parts vidéo-texte (VTP): 27 millions de courts clips vidéo.
   Le film est sorti en version originale en version originale.

OBELICS (2023) est une reproduction ouverte du corpus web interlevé, sur lequel Idefics, Idefics2 et la plupart des modèles "flamingo-like" ouverts s'entraînent.

> OBÉLICS (en 2023) est un modèle ouvert de la base de langages du réseau intertextuel, idétiques, idétiques2 et la plupart des modèles "classes flamingos" ouverts.

### OpenFlamingo et la lentille

OpenFlamingo (2023) est la reproduction ouverte. L'architecture est identique (reprimateur de percepteur + attention croisée fermée sur LLaMA congelé ou MPT).

> OpenFlamingo(2023) est ouvert à nouveau. La même structure.

Otter (2023) s'appuie sur OpenFlamingo avec l'ajustement des instructions sur MIMIC-IT (un ensemble de données d'instructions multimodal), montrant des fonctions d'attention croisée fermée pour les instructions suivantes également.

> Otter(2023) pour effectuer des instructions de micro-modification à l'aide de MIMIC-IT (OpenFlamingo) sur la base de l'application, démontrer que l'attention du contrôle de la transmission est également applicable à l'instruction de suivi.

### Les descendants

- Idefics / Idefics2 / Idefics3: La lignée de l'attention croisée fermée de Hugging Face, progressivement plus simple (Idefics2 a abandonné le resampler en faveur des jetons de patch directs avec pooling adaptatif).
  Le code de la page de référence est le code de la page de référence.
- Transition Flamingo-Chameleon: d'ici 2024, de nombreuses équipes ont déménagé vers la fusion précoce (Lésion 12.11); l'attention croisée fermée de style Flamingo reste en production où le gel de la colonne vertébrale est nécessaire.
  Traduction anglaise: Transition du flamingo au chaméléon: jusqu'en 2024, de nombreuses équipes se tournent vers la première fusion.
- L'entrée interlevé de Gémeaux: conceptuellement hérite de la flexibilité de format interlevé de Flamingo, bien que le mécanisme exact soit propriétaire.
  Le concept a hérité de la flexibilité du style de la chemise des Flamingos, bien que le mécanisme spécifique soit exclusif.

### Comparé à BLIP-2

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Choisissez BLIP-2 pour une image unique VQA sur un budget. Choisissez Flamingo/Idefics2 pour un raisonnement interligé, peu de coups ou multi-image.

> 预算有限的单图像 VQA 选 BLIP-2──交织、少样本或多图像推理选 Flamingo/Idefics2──

## Utilisez-le avec le cadre de réalisation
```figure
cross-attention-fusion
```

## Utilisez-le

`code/main.py`démontre:

> `code/main.py`Il a dit:

1. Un échantillon de réception sur 36 faux patch tokens avec 8 latences appréciables (attention croisée pure Python).
   Pour le modèle de 36 faux patch, utilisez 8 potentiels potentiels possibles.
2. Un pas de l' attention croisée fermée avec `alpha = 0`→ sortie égale à l'entrée (LLM inchangé), alors `alpha = 2.0`→ contribution visuelle mélangée.
   Le mot "défense" est traduit par "défense".`alpha = 0`→ 输出等于输入 (LLM 不变), puis `alpha = 2.0`→ 视觉贡献混入──
3. Un constructeur de masques interleavés qui produit le masque d'attention 2D pour une séquence "(image 1) (texte 1) (image 2) (texte 2)".
   Le système de construction de la structure de la structure est un système de construction de la structure de la structure.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-gated-bridge-diagnostic.md`. Compte tenu de la configuration d'un VLM ouvert (sampler Y/N, fréquence de fréquence croisée, schéma de passerelle), il identifie les éléments de lignée Flamingo et explique la stratégie de congélation. Utilisée pour déboguer les raisons pour lesquelles une mise en forme fine dégrade les performances du texte (réponse: la passerelle s'est largement trop rapidement élargie).

> 本课产 出 `outputs/skill-gated-bridge-diagnostic.md` Donner une définition de la configuration du VLM (voir la liste des paramètres de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de l'équipe de contrôle de contrôle de l'équipe de contrôle de l'équipe de contrôle de contrôle de l'équipe de contrôle de contrôle de l'équipe de contrôle de contrôle de l'équipe de contrôle de contrôle de l'équipe de contrôle de contrôle de contrôle de l'équipe de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de contrôle de

## Les exercices

1. Comptez le nombre de paramètres visuels du Flamingo-9B: 9B LLM + 1,4B couches de l'attention croisée fermées + 64M resampler. Quelle fraction des paramètres totaux est formée?
   Compteur de paramètres visuels de Flamingo-9B: 9B LLM + 14 milliards de points de contrôle

2. Implémenter le résidu clos `y = tanh(alpha) * cross + x`Dans PyTorch, montre expérimentalement que avec`alpha=0`- Je suis là .`y==x`Exactement à l'initi.
   Le système de contrôle des déchets`y = tanh(alpha) * cross + x` Précises de test`alpha=0`时 `y==x`Il est vrai.

3. Lisez la section 3.2 d'OpenFlamingo (arXiv:2308.01390) sur la façon dont ils gèrent plusieurs images dans un lot lorsque chaque prompt a un nombre d'images différent.
   Le projet de loi de l'Union européenne sur la protection des données (CEDEFOP) a été publié le 30 décembre 2015 par le gouvernement de l'Union européenne.

4. Pourquoi le masque d'attention croisée de Flamingo permet-il à un jeton texte de ne s'attacher qu'à * la plus récente* image précédente plutôt que à toutes les images précédentes ?
   Pourquoi Flamingo est-il en train de se concentrer sur les images précédentes plutôt que sur les images précédentes ?

5. Dans le contexte, quelques coups: construisez un prompt avec 4 exemples de "image → couleur de l'objet principal" pour une nouvelle variante Flamingo.
   Le modèle de construction comprend 4 " images " et les exemples de couleurs des principaux éléments.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Encore une lecture

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198) le papier original.
  Le texte original de la lettre de la première lettre est écrit en français.
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) reproduction ouverte.
  Le récit de la rédaction de la Bible
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) corps de toile entrelacée.
  Le texte de la Bible est écrit en français.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) l'architecture générale du percepteur.
  Le système de calcul de la structure de l'image est un système de calcul de la structure de l'image.
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726)Des descendants de Flamingo réglés par des instructions.
  Le flamingo est un flamingo.
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) modernisation de l'approche flamingo.
  Le flamingo est un moyen de lutte contre la corruption.
