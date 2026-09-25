# DualPipe Parallélisme 双向流水线并行

> DeepSeek-V3 a été formé sur 2048 GPU H800 avec des experts de MoE dispersés sur les nœuds. L'expert en communication tout-à-tout coûte 1 heure de communication pour chaque heure de calcul. Les GPU étaient en activité la moitié du temps. DualPipe (DeepSeek, décembre 2024) est un pipeline bidirectionnel qui superpose le calcul avant et arrière avec les communications tout-à-tout qu'ils déclenchent. La chute des bulles, la hausse du débit et la conservation de deux exemplaires de modèle-paramètre (le "dual" qui donne le nom) sont bon marché une fois que Expert Parallelism répand déjà des experts dans les rangs de toute façon. Cette leçon est une expérience de type Learn de ce que fait vraiment DualPipe et pourquoi le raffinement DualPipeV du Sea AI Lab réduit le coût du paramètre 2x au détriment d'une bulle légèrement plus serrée.

> **【中文解读】**DeepSeek-V3 en 2048 张 H800 上训练,MoE 专家分布在节点间――跨节点-all-to-all 通信让 GPU 一半时间在等待――DualPipe est une ligne de flux de l'eau à deux voies, va faire face à l'ensemble du calcul 通信重叠, réduire la foudre、 augmenter la débit¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

> **【拓展：DualPipe→大规模训练】**DualPipe est la clé de l'entraînement à haute efficacité de DeepSeek-V3: il va superposer les coûts de communication de MoE avec le calcul avant/arrière, ce qui permettra à l'efficacité de l'entraînement sur 2048 cartes de se rapprocher de l'expansion linéaire.

>  **【前置】**學本節前请先掌握:Phase 10·05(Scaling Distributed);MoE(Mix of Experts) concept;流水线并行(Pipeline Parallelism)基础;all-to-all 通信模式。本节是Phase 10·20(DeepSeek-V3 Walkthrough) 的并行策略详解。

**Type:** Learn
**Languages:** Python (stdlib, schedule simulator)
**Prerequisites:** Phase 10 · 05 (distributed training, FSDP, DeepSpeed), Phase 10 · 14 (open-model architectures and MoE)
**Time:** ~60 minutes

## Objectifs d'apprentissage

- Nombre des quatre composants d'une pièce DualPipe vers l'avant et vers l'arrière et pourquoi chacun a sa propre fenêtre de chevauchement.
  Expliquer les quatre composants du bloc du double piquet avant-contre-versant et les causes de leur superposition
- Expliquez le problème de la bulle de pipeline à grande échelle et ce que signifie " sans bulle " dans la pratique par rapport au marketing.
  Expliquer le problème des bulles de débit à grande échelle, ainsi que la différence entre la pratique du "bubble de débit" et la pratique du marketing
- Suivez manuellement un calendrier DualPipe pour 8 rangs PP et 16 micro-parties et confirmez que les courants avant et arrière remplissent les espaces vacants de l'autre.
  Trace manuel 8 étapes PP et 16 petits lots de doubles tuyaux, confirmant la direction droite et l'inverse de la circulation remplir les espaces vides de l'autre
- Expliquez le compromis que fait DualPipeV (Sea AI Lab, 2025): la réplication de paramètre 2x est supprimée au prix d'une bulle légèrement plus grande lorsque Expert Parallelism est inactif.
  Il s'agit d'un projet de recherche qui a été réalisé par le projet de recherche de l'Institut de recherche et développement de l'IA de la mer.

## Le problème , l' introduction du problème

La formation d'un modèle MoE 671B sur des GPU H800 de 2k se retrouve dans trois goulots d'étranglement:

1. **Memory pressure.**Chaque GPU contient une tranche du modèle.
2. **Pipeline bubbles.**Le parallélisme traditionnel des pipelines (GPipe, 1F1B) laisse les GPU en marche pendant qu'elles attendent l'entrée ou le gradient de leur étape.
3. **Cross-node all-to-all.**Le MoE avec le parallélisme expert disperse les experts à travers les nœuds. Chaque passe avant déclenche un tout-à-tout pour envoyer des jetons à leurs experts, et un autre pour combiner.

> Dans le 2k H800 GPU, le modèle MoE 671B se retrouve avec trois boîtes complexes:

1. **内存压力。**Chaque GPU possède un morceau de modèle. La longueur de séquence de 8K, 61 couches, 128 têtes, est énorme.
   Le nombre de capteurs de la GPU est énorme.
2. **流水线气泡。**传统流水线并行(GPipe、1F1B) Laissez la GPU attendre son entrée ou la température de sa phase 时空──8 个阶段, même en utilisant la régulation 1F1B, environ 12% du temps de la GPU 可能是气泡──
   Traditionnellement, le temps de la GPU est de la température de la GPU.
3. **跨节点全互联。**Le MoE distribuera les experts à différents niveaux. Chaque fois que le premier et le dernier sont diffusés, le premier est distribué à un expert.
   MoE 专家并行每次前向传播触发两次全互联通信, en 2k GPU 时计算通信比接近 1:1──

Chacune d'entre elles a des solutions distinctes: la mise en garde des gradients pour la mémoire, la bulle zéro (Sea AI Lab, 2023) pour les bullettes de pipeline, les noyaux de communication experts parallèles pour tout le monde. Ce que fait DualPipe, c'est les faire jouer ensemble. Le calendrier superpose le calcul et la communication dans une seule pièce avant-arrière, injecte des micro-parties des deux extrémités du pipeline simultanément et utilise le calendrier résultant pour cacher tout à l'intérieur des fenêtres de calcul.

Résultat rapporté: presque élimination des bulles de pipeline, plus de 95% d'utilisation de GPU dans la course d'entraînement de 14.8T de DeepSeek-V3.

## Le concept de base.

> **【中文解读】**DualPipe est un algorithme de fusion de flux de l'eau à deux voies proposé par DeepSeek-V3, en utilisant des calculs de superposition entre le flux de l'eau à l'avant et l'arrière pour maximiser le taux d'utilisation de la GPU.

> **【拓展：DualPipe 与 DeepSeek-V3 的效率】**DeepSeek-V3 est un des principaux modèles de formation de DeepSeek-V3 à partir de 560 millions de dollars.


### Récupération du parallélisme des pipelines

Partager un modèle à couche N entre les appareils P. Dispositif `i`Il tient des couches `i * N/P .. (i+1) * N/P - 1`. Un micro-batch s'écoule vers l'avant à travers les dispositifs 0 à P-1, puis vers l'arrière de P-1 à 0. Chaque appareil ne peut démarrer sa phase vers l'avant que lorsque le dispositif précédent envoie sa sortie et ne peut démarrer vers l'arrière que lorsque le dispositif en aval envoie le gradient en amont.

GPipe (Huang et coll., 2019) planifie un micro-batch à la fois, ce qui gaspille la plupart du temps de la GPU. Le point 1F1B (Narayanan et coll., 2021) interpose les passes avant et arrière pour plusieurs micro-parties. La bulle zéro (Qi et al., 2023) divise le passage vers l'arrière en deux parties  vers l'arrière pour l'entrée (B) et vers l'arrière pour les poids (W)  et les planifie pour remplir la bulle. Après la bulle Zéro, le pipeline est presque serré.

DualPipe est la prochaine étape. Il ajoute deux idées en plus:

### Idée 1: décomposition en morceaux

Chaque pièce avant est divisée en quatre composants:

- **Attention.**Projections Q/K/V, attention, projection de sortie.
- **All-to-all dispatch.**La communication entre les nœuds qui envoie des jetons à leurs experts.
- **MLP.**Le calcul de l'expert du ministère de l'Économie.
- **All-to-all combine.**La communication entre les nœuds qui ramène des résultats d'experts.

Une pièce arrière ajoute des versions de gradient de chacune d'elles. DualPipe les planifie de sorte que l'envoi tout-à-tout se produit en parallèle avec le calcul de l'attention de la pièce suivante, et la combinaison tout-à-tout se produit en parallèle avec le calcul MLP de la pièce suivante.

### Idée 2: planification bidirectionnelle

La plupart des programmes de pipelines injecter des micro-parts à partir de l'étape 0 et couler vers l'étape P-1. DualPipe injecte des micro-parts à partir des deux extrémités.

Pour que ça marche, appareil `i`doit contenir LA couche de tuyau précoce `i`Et la couche de la dernière pipeline.`P - 1 - i`. C'est la partie "dual" de DualPipe: chaque appareil conserve deux copies des couches de modèle dont il a besoin pour servir (une pour chaque direction). À l'échelle de DeepSeek-V3, c'est un coût de réplication de paramètre de 2x. Il est abordable parce que Expert Parallelism répand déjà les experts MoE si minces que la réplication des couches non-experts deux fois est de petites pommes de terre.

Le courant d'avance dans une direction et le courant de retour dans l'autre se chevauchent exactement là où les bulles se trouvent dans un calendrier à une seule direction.

### Un calendrier suivi à la main

Considérez P = 4 rangées, 8 micro-parties, divisées 4 avant / 4 arrière. Le temps se déplace de gauche à droite; les rangées sont des rangées d'appareils.

```
           Time →
rank 0:  F1 F2 F3 F4  F5R F6R F7R F8R  B1 B2 B3 B4  ...
rank 1:     F1 F2 F3  F4/F5R F6R F7R   B1 B2 ...
rank 2:        F1 F2  F3/F5R F4/F6R    B1 ...
rank 3:           F1  F2/F5R F3/F6R    ...
```

Lire la notation "F4/F5R": le rang 1 est en avance sur le micro-batch 4 (aller de gauche à droite dans le pipeline) ET en avant du micro-batch 5 (aller de droite à gauche) dans le même intervalle de temps.

Dans la phase moyenne stable du calendrier, chaque rang se superpose à l'avant de la direction X et à l'arrière de la direction Y. Le calcul est occupé. Les envois tout-à-tout pour le passage en avant se cachent à l'intérieur du calcul en arrière. Tout-à-tout combine se cacher à l'intérieur du calcul en avant. Les bulles sont pressées.

### Comptabilité des bulles

Bulle de pipeline standard 1F1B (temps gaspillé par rang):

```
bubble_1F1B = (P - 1) * forward_chunk_time
```

Le raffinement de la bulle zéro la réduit mais pas à zéro. DualPipe, dans la phase stable, a une bulle zéro si le nombre de micro-batches est divisible par 2 fois la profondeur du pipeline.

En termes marketing: " sans bulles ". En termes techniques: les bulles ne se développent pas avec le nombre de micro-parts. L'analyse de suivi du Sea AI Lab (DualPipeV / Cut-in-half) montre la bulle zéro complète seulement lorsque le parallélisme expert n'est pas le goulot d'étranglement; avec le tout-à-tout dirigé par EP, un certain compromis de planification est toujours présent.

### DualPipeV  le raffinement

Sea AI Lab (2025) a observé que la réplication du paramètre 2x est gaspillée lorsque la superposition de la communication EP n'est pas le point. Leur calendrier DualPipeV plie l'injection bidirectionnelle dans un calendrier "V-forme" qui fonctionne sur une seule copie de paramètre. La bulle est légèrement plus grande que celle de DualPipe, mais les économies de mémoire sont considérables. DeepSeek a adopté DualPipeV dans leur mise en œuvre DualPipe open source en mode EP-off.

Le compromis:

| Feature | DualPipe | DualPipeV | 1F1B | Zero Bubble |
|---------|---------|-----------|------|------------|
| Param copies per device | 2 | 1 | 1 | 1 |
| Bubble vs micro-batches | constant | small growth | grows | grows |
| Compute-comm overlap | full | partial | minimal | partial |
| Use when | EP-heavy MoE | dense or EP-light | baseline | any pipeline |

### Ce que cela signifie pour une course de jetons 14,8T

La pré-entraînement de DeepSeek-V3 a consommé 14,8 T de jetons sur 2048 GPU H800 en environ 2,8 millions d'heures de GPU. Avec 1F1B naïf, ils auraient perdu 12-15% de ce pour les bulles de pipeline  340-420K GPU-heures, assez pour former un modèle complet 70B. DualPipe a récupéré la plupart de ça. La quantification directe de la contribution est difficile sans les journaux internes, mais l'affirmation dans l'article est que l'utilisation moyenne de la GPU est supérieure à 95% sur l'ensemble de la formation.

Pour les petites exécutions (moins de 1k GPU), DualPipe est surkill  les bulles de pipeline sont plus petites par rapport au coût total, et l'entraînement de modèle dense frappe rarement le goulet d'étranglement.

### Là où il est dans la pile

- Complémentaire à **FSDP**(Phase 10 · 05). FSDP réduit les paramètres du modèle à travers des rangs; DualPipe planifie le calcul à travers des rangs. Ils se combinent.
- Compatible avec **ZeRO-3**La comptabilité de la réplique à deux copies doit coopérer avec les gradients fragmentés de ZeRO.
- Il faut que tu le fasses .**custom all-to-all kernels**Les noyaux open source de DeepSeek sont la mise en œuvre de référence.


> **【拓展：流水线并行的工程细节】**DualPipe, en se déplaçant dans la même direction, va réduire le taux de bulles de 20% à 5% et cela aura un impact énorme sur les coûts de formation à grande échelle.


## Utilisez-le avec le cadre de réalisation
```figure
expert-capacity
```

## Utilisez-le

`code/main.py`C'est un simulateur de calendrier de pipeline.`(P, n_micro_batches, schedule)`Il est un outil d'enseignement  les chiffres correspondent aux affirmations qualitatives dans les documents, ils ne sont pas une affirmation sur la production mesurée accélération.

La valeur du simulateur: utilisez différents P et micro-batches et regardez comment la fraction de la bulle augmente pour 1F1B mais pas DualPipe.

Les considérations d'intégration pour une formation réelle:

- Choisissez une profondeur parallèle de pipeline qui se divise nettement en votre nombre de micro-parts.
- Assurez-vous que votre filet expert-parallèle prend en charge le tout-à-tout bidirectionnel.
- Attends-toi à brûler une semaine de débogage sur le calendrier lui-même la première fois.
- Moniteur de l'utilisation de la GPU par rang, pas seulement l'agrégat.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-dualpipe-planner.md`. Compte tenu de la spécification du cluster de formation (compte de GPU, topologie, interconnexion, forme de modèle), il recommande une stratégie de parallélisation des pipelines, l'algorithme de planification à utiliser et la fraction de bulle attendue à l'échelle cible.

> 本课产 出 `outputs/skill-dualpipe-planner.md` Donner une formation spécifique à la population de l'équipement de formation (GPU), elle propose des stratégies de gestion des flux de l'eau, des algorithmes de régulation et des bulles de production prévues pour la taille de l'objectif.

## Les exercices

1. On court .`code/main.py`sur`(P=8, micro_batches=16, schedule=dualpipe)`et `(P=8, micro_batches=16, schedule=1f1b)`Calculer la différence d'utilisation de la GPU et l'exprimer en GPU-heures récupérées par million de jetons de formation.
   Dans le texte original,`(P=8, micro_batches=16, schedule=dualpipe)`et `(P=8, micro_batches=16, schedule=1f1b)`上运行 `code/main.py`◊ calculer le taux d'utilisation de la GPU différence并表示 pour le million de jetons de formation

2. Dessinez le tableau de l' horaire pour `(P=4, micro_batches=8, schedule=dualpipe)`Marquez chaque fuseau horaire avec l'identifiant et la direction du micro lot. Identifiez le premier fuseau horaire où les bulles sont absentes.
   Le mot "c'est-à-dire " est traduit par "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire " est-à-dire "c'est-à-dire " est-à-dire " est-ce" est un mot "c'est-à-dire " est" est un mot " est " est " est "`(P=4, micro_batches=8, schedule=dualpipe)`La répartition des températures de chaque tronc de temps est marquée par la première tranche de temps où la boue disparaît.

3. Lisez la figure 5 du rapport technique DeepSeek-V3 (arXiv:2412.19437). Identifiez la fenêtre de chevauchement pour la dépêche tout-à-tout à l'intérieur d'une pièce du DualPipe vers l'avant. Expliquez comment le calendrier de calcul le cache.
   Le système de recherche de la technologie de DeepSeek-V3 est un système de recherche de données de la technologie de recherche de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de données de données de recherche de données de la technologie de DeepSeek-V3 qui est un système de recherche de recherche de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de.

4. Comptez le coût de la conduite de 2x du modèle à densité de 70B avec P=8 étapes de pipeline et un modèle MoE de 671B avec P=16 étapes de pipeline. Montrez pourquoi le coût de la conduite de la case MoE est proportionnellement plus petit (la plupart des paramètres sont des experts, fragmentés dans un grand groupe EP).
   Le calcul du double-pipe pour les modèles 70B 密集模型 ((P=8 流水线阶段) et 671B MoE 模型 ((P=16 阶段) de 2 fois le nombre de débouchés.

5. Comparer DualPipe à Chimera (un planificateur bidirectionnel concurrent à partir de 2021). Identifiez les deux propriétés spécifiques que DualPipe a ajoutées que Chimera n'avait pas, en utilisant la section 3.4 du papier comme référence.
   Le deuxième chapitre de l'édition 2021 de la compétition est consacré à la mise en place de la chimère.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Pipeline bubble | "Idle time per rank" | GPU cycles wasted because a pipeline stage is waiting for its input or gradient | 流水线气泡，GPU 等待输入或梯度时空转的周期 |
| 1F1B | "Default pipeline schedule" | One forward / one backward interleaved scheduling; the baseline DualPipe beats | 1F1B 调度，一前向一反向交替 |
| Zero Bubble | "Sea AI Lab 2023" | Splits backward into B (input gradient) and W (weight gradient); almost fully tightens the pipeline | 零气泡，将反向拆为输入梯度和权重梯度 |
| DualPipe | "DeepSeek-V3 schedule" | Bidirectional pipeline + compute-comm overlap; bubbles do not grow with micro-batch count | DualPipe，双向流水线+计算通信重叠 |
| DualPipeV | "Cut-in-half" | V-shape refinement that drops the 2x parameter replication at the cost of slightly larger bubbles | DualPipeV，取消 2x 参数复制，气泡略增 |
| Chunk | "Unit of pipeline work" | A forward or backward pass of one micro-batch through one pipeline stage | 块，一个微批次在一个流水线阶段的前向/反向 |
| All-to-all dispatch | "Send tokens to experts" | Cross-node comm that routes tokens to their assigned MoE experts | 全互联分派，将 token 路由到 MoE 专家 |
| All-to-all combine | "Bring expert outputs back" | Cross-node comm that gathers expert outputs after the MLP | 全互联组合，收集专家输出 |
| Expert Parallelism (EP) | "Experts across GPUs" | Shards MoE experts across ranks so different GPUs hold different experts | 专家并行，不同 GPU 持有不同 MoE 专家 |
| Pipeline Parallelism (PP) | "Layers across GPUs" | Shards model layers across ranks; the dimension DualPipe schedules | 流水线并行，模型层分布在不同 GPU |
| Bubble fraction | "Wasted GPU time" | (bubble_time / total_time); the fraction DualPipe drives toward zero | 气泡比例，DualPipe 将其压向零 |

## Encore une lecture

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437), Section 3.3.2 and Figure 5](https://arxiv.org/abs/2412.19437) la référence principale du DualPipe
- [DeepSeek — DualPipe GitHub repository](https://github.com/deepseek-ai/DualPipe) la mise en œuvre de référence open source, y compris le mode DualPipeV (Cut-in-half)
- [Qi et al. — Zero Bubble Pipeline Parallelism (arXiv:2401.10241, Sea AI Lab 2023)](https://arxiv.org/abs/2401.10241) le prédécesseur de la bulle Zéro
- [Sea AI Lab — DualPipe could be better without the Dual](https://sail.sea.com/blog/articles/63) l'analyse DualPipeV qui a informé le mode de déconnexion EP de DeepSeek
- [Narayanan et al. — PipeDream / 1F1B (arXiv:1806.03377, 2018-2021)](https://arxiv.org/abs/1806.03377) le calendrier 1F1B comparé à DualPipe
- [Huang et al. — GPipe (arXiv:1811.06965, 2018)](https://arxiv.org/abs/1811.06965) le problème du parallélisme du pipeline original
