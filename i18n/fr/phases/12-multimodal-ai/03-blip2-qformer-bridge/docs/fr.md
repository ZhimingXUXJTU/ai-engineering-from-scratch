# De CLIP à BLIP-2  Q-Former comme pont de modalité  de CLIP à BLIP-2: Q-Former 模态桥接

> CLIP aligne l'image et le texte, mais ne peut générer de légendes, répondre à des questions ou tenir une conversation. BLIP-2 (Salesforce, 2023) a résolu cela avec un petit pont entraînable: 32 vecteurs de requête apprenables assistent sur les caractéristiques d'un ViT gelé via l'attention croisée, puis s'insèrent directement dans le flux d'entrée d'un LLM gelé. 188 millions de paramètres de pont ont relié un LLM 11B à un ViT-g/14. Chaque VLM basé sur un adaptateur jusqu'en 2026  MiniGPT-4, InstructBLIP, les cousins de LLaVA  est un descendant. Cette leçon lit l'architecture du Q-Former, explique son entraînement en deux étapes et construit une version de jouet qui alimente des jetons visuels dans un décodeur de texte gelé.

> **【中文解读】**CLIP ne peut que s'adapter au texte mais ne peut pas être généré. BLIP-2 utilise 32 volumes de requêtes à apprendre par le biais de la communication de l'attention.

> **【拓展：Q-Former→多模态架构演进】**Q-Former est le fondateur du modèle "结视觉编码器+结LLM+轻量桥接", MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Je vous invite à maîtriser la phase 12 de la formation.
>  **【类比】**Q-Ex = "journaliste interview"──32 个记者(question) Stand ViT 出来的 256 补丁 前面,每个人都提问自己的问题,听完回答后写下 32 条新闻摘要──这32 条摘要就是给LLM的"新闻简报",LLM 不用看完整 256 张原始图片──

## Objectifs d'apprentissage

- Expliquez pourquoi un goulet d'étranglement entraînable entre un encodeur de vision gelé et un LLM gelé est supérieur à l'ajustement fin de bout en coût et stabilité.
  Traduction chinoise: expliquer pourquoi le coût et la stabilité de l'écriture de l'écriture vidéo et de l'écriture de l'écriture de l'écriture sont meilleurs que les modèles de l'écriture de l'écriture.
- Implémenter un bloc d'attention croisée où un ensemble fixe de requêtes apprenantes répond aux caractéristiques externes de l'image.
  En français, une requête est une requête qui peut être étudiée en particulier pour une image extérieure.
- Passez par la préparation en deux étapes de BLIP-2: représentation (ITC + ITM + ITG) puis générative (perte de LM avec décodeur gelé).
  Le programme de formation est basé sur le programme de formation de formation de formation professionnelle.
- Comparez Q-Former au plus simple projecteur MLP utilisé dans LLaVA et discutez quand chaque choix gagne.
  Le plus simple est que les projecteurs de MLP sont des projecteurs de Q-Former et de LLaVA.

## Le problème , l' introduction du problème

Vous avez un ViT gelé qui produit 256 jetons de patch de dim 1408 par image. Vous avez un LLM gelé 7B qui attend des emblèmes de jetons de dim 4096. Le pont évident  une couche linéaire de 1408 à 4096  fonctionne, mais l'alimentation de tous les 256 jetons de patch dans le contexte du LLM coûte 256 jetons supplémentaires par image.

> Vous avez une connexion ViT, chaque image génère 256 dimensions pour 1408 patch tokens. Vous avez une connexion 7B LLM, vous attendez à 4096 dimensions pour 4096 des jetons.

La question BLIP-2: pouvez-vous compresser la représentation d'image de 256 jetons en beaucoup moins de jetons (disons 32) tout en préservant suffisamment d'informations pour que le LLM puisse sous-titrer, répondre aux questions et raisonner sur l'image? Et pouvez-vous entraîner ce pont sans toucher les os froids, en gardant le coût de la formation aux seules paramètres du pont?

> Question de BLIP-2: Pouvez-vous compresser 256 images de jetons pour les représenter à moins de 32 jetons, tout en conservant suffisamment d'informations pour permettre à LLM de décrire des images, de répondre aux questions et de faire des raisonnements?

La réponse: un Q-Former. 32 vecteurs "query" apprenables qui se croisent aux jetons de patch du ViT, produisant un résumé visuel de 32 jetons que le LLM consomme. 188M de paramètres au total.

> La réponse est: Q-Former──32 个可学习的"查询"量通过交叉注意关注 ViT's patch token,产生LLM 消费的32 token 视觉摘要──总共188M 参数──在接触LLM 之前使用比较、匹配和生成目标进行训练──

## Le concept de base.

> **【中文解读】**BLIP-2  Introduction Q-Former 结视觉编码器和结 LLM 之间的轻量桥接层。Q-Former Utilisation d'un ensemble de jetons de requête pouvant être appris  从视觉编码器提取与文本最相关的视觉特征, réduit considérablement le nombre de séances d'entraînement  仅训练 Q-Former), a réalisé un haut rendement de la visualisation-langue par z齐──

> **【拓展：BLIP-2 的高效训练】**BLIP-2 peut être terminé en 12 heures sur un seul A100, avec seulement Q-Former 参数), par rapport à la méthode précédente, 10 à 100 fois. La conception de Q-Former a influencé les modèles suivants de LLaVA、InternVL et autres.


> **【拓展：Q-Former 的影响】**L'idée de conception de Q-Former est largement utilisée. Elle permet de former des modèles multiples en utilisant des GPU de consommation.


### Questions à apprendre

Le truc principal du Q-Former: au lieu de laisser les jetons de texte du LLM s'occuper des correctifs d'image, introduisez un nouvel ensemble de 32 vecteurs de requête apprenables `Q`Les requêtes sont des paramètres du modèle  elles sont apprises lors de la formation et les mêmes 32 requêtes sont utilisées pour chaque image.

> Q-Former's core technique: ne pas laisser le texte de la LLM jeton  se concentrer sur le patch d'image, mais introduire un nouveau groupe de 32                                                                                                                                                                                                                                           `Q`, les faire * attention à la patch d'image. La requête est le paramètre du modèle à apprendre pendant l'entraînement, et chaque image utilise les mêmes 32 requêtes.

> ️ **【易错点】**Pour "32 requêtes sont 32 张不同图片的查询"错!32 查询是固定的,对所有图片都一样.
> 🤔 **【困惑】**Q: 32 个查询 如何知道每个该看什么?A: 训练时三个损失(ITC/ITM/ITG) 会反向传播梯度告诉每个查询 该专精什么;;

Après l'attention croisée, chaque requête contient un résumé comprimé de l'image  "décrire l'objet principal", "décrire l'arrière-plan", "comptez les objets", etc. Les requêtes ne se spécialisent pas littéralement dans les étiquettes sémantiques; elles apprennent ce que le codage fait en aval les pertes de baisse.

> Après la mise en œuvre de la mise en œuvre de la communication, chaque requête contient un résumé de l'image "description des principaux objets""", description du contexte""", nombre d'objets calculés" etc. La requête ne se concentre pas littéralement sur les étiquettes de signification; elles apprennent à réduire les pertes de l'écriture.

### Architecture

Le Q-Former est un petit transformateur (12 couches, ~ 100M params) avec deux voies:

> Q-Former est un petit transformateur (environ 100M de dimensions)

1. Voie de requête: 32 vecteurs de requête circulent à travers l'auto-attention (entre eux), puis l'attention croisée sur les jetons de patch du ViT gelé, puis FFN.
   En français, le mot "coup d'attention" est traduit par "coup d'attention" (en français: "coup d'attention").
2. Voie de texte: un encodeur de texte semblable à BERT partage l'auto-attention et les poids FFN avec le chemin de requête.
   Le codeur de texte de la BERT et le codeur de requête du cours de recherche de la langue française sont les mêmes.

Les requêtes et le texte interagissent par l'intermédiaire de l'auto-attention partagée, ce qui signifie que les requêtes peuvent conditionner le texte pour les tâches qui en ont besoin (ITM, ITG).

>                                                                                                                                                                                                                                                               

### Formation en deux étapes

BLIP-2 prétraine en deux étapes:

> BLIP-2 分两阶段预训练:

Étapes 1: apprentissage représentatif (pas de LLM). Trois pertes:
- CTI (contraste image-text): contraste CLIP entre les jetons de requête regroupés et les jetons CLS texte.
  Le code de la carte de crédit est un code de crédit qui est utilisé pour les transactions de transactions.
- ITM (image-text matching): classifiateur binaire  est cette paire image-text un match?
  Le modèle de l'image est un modèle de l'image de l'image.
- ITG (Génération de texte basée sur l'image): LM causel sur texte, conditionné sur les requêtes.
  Le code de la recherche est un code de la recherche obligatoire.

>  **【类比】**3 perte de travail:ITC = " regarder le texte " ([[gross grain]] à la main);ITM = " juger ce texte est-il vraiment écrit " ([[gross grain]] à la main);ITG = " regarder le texte à la main " ([[génération de capacité]])

Les trains Q-Former, le ViT est congelé, pas de LLM.

> 仅训练 Q-Former──ViT 结──不涉及 LLM──

Étape 2: apprentissage génératif. Attachez un LLM gelé (OPT-2.7B ou Flan-T5-XL, etc.). Projetez les 32 sorties de requête à la séquence d'embedding du LLM via une petite couche linéaire. Préparez-les à la requête de texte.

> Deuxième étape: générer des études. Lien à un LLM (OPT-2.7B ou Flan-T5-XL) et ainsi de suite.

Après la phase 2, la projection Q-Former + est l'adaptateur visuel complet. À l'inférence: image → ViT → Q-Former → projet linéaire → prépendu au texte → gelé LLM émet la sortie.

> Deuxième étape suivante, Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### Économie des paramètres

BLIP-2 avec ViT-g/14 (1.1B, congelé) + OPT-6.7B (6.7B, congelé) + Q-Former (188M, formé) = 8B total, 188M formé. Le Q-Former seul représente ~ 2,4% des paramètres de la pile complète.

> BLIP-2 Utilisation ViT-g/14(11 milliards,结) + OPT-6.7B(67 milliards,结) + Q-Former(1.88 milliards, entraînement) = 共 80 milliards, entraînement 1.88 milliards, Q-Former 仅占全参数约2.4%── entraînement coût reflète ce point:少量 A100 上数天 vs 端到端数周──

Qualité: BLIP-2 correspond ou bat Flamingo-80B sur VQA à tir zéro tout en étant 50 fois plus petit.

> La qualité:BLIP-2 en zéro échantillon VQA 上匹配或超越 Flamingo-80B, simultanément réduit de 50 fois.

### InstructBLIP et le Q-Former qui connaît les instructions

InstructBLIP (2023) étend le Q-Former avec une entrée supplémentaire: le texte d'instruction lui-même. Au moment de l'attention croisée, les requêtes ont maintenant accès à la fois aux patchs d'image et à l'instruction. Les requêtes peuvent se spécialiser par instruction ("comptez les voitures", "décrivez l'humeur") plutôt que d'apprendre un seul résumé fixe.

> En plus de la mise en place de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise

### MiniGPT-4 et l'approche à projecteur seulement

MiniGPT-4 a gardé le Q-Former mais a entraîné seulement la projection linéaire de sortie tout en congelant tout le reste. Cheap, mais le coût est de qualité  les requêtes étaient de BLIP-2, pas les vôtres. Bon pour l'itération rapide, pas la meilleure architecture.

> MiniGPT-4 conserve Q-Former, mais seulement entraînement, sortie de projection, résultat de tout le reste.

### Pourquoi LLaVA est devenu plus simple

LLaVA (2023, leçon 12.05) a remplacé le Q-Former par un MLP simple à 2 couches qui projette chaque jeton de patch ViT dans l'espace LLM  576 jetons par image pour une grille 24x24, tous alimentés au LLM. Pire compression mais laisse le LLM assister sur les patches brutes. À l'époque, cela était controversé; à la fin de 2023, il était dominant parce que les données d'instruction visuelle (LLaVA-Instruct-150k) prouvaient que le MLP pouvait être formé pour préserver suffisamment de signal. Le compromis: le contexte de LLaVA se remplit plus rapidement, mais il s'élargit naturellement à la multi-image et à la vidéo.

> LLaVA(2023, section 12.05 课) a remplacé Q-Former par un simple MLP de 2 niveaux, qui projettera chaque jeton de patch ViT dans l'espace LLM 24x24 网格下 chaque image 576 个 token, tout en donnant à LLM. Mais il est plus difficile de le faire.

> 🤔 **【困惑】**Q-Former: Compression 32 jetons 精心训练);长上下文 + 多图/视频 → LLaVA MLP: par jeton 信息量大但灵活) ⋅ 2026

En 2026, le champ est divisé: Q-Former survit là où le budget des jetons compte (vidéo longue, beaucoup d'images); le projecteur MLP domine là où la qualité brute par jeton est la priorité.

> D'ici 2026, le domaine de la distribution: Q-Former en token  budget important alors; MLP 投影器 en premier lieu en qualité de chaque token.

### Attention croisée: Flamingo, l'ancêtre

Flamingo (Lésion 12.04) précède BLIP-2 et utilise la même idée d'attention croisée mais à chaque couche LLM gelée, pas comme un seul pont. BLIP-2 a montré que vous pouvez compresser à la couche d'entrée uniquement et toujours travailler. Gemini et Idefics combinent les deux: jetons d'entrée interleavés plus une attention croisée fermée optionnelle pour quelques coups dans le contexte.

> Flamingo (第 12.04 课) a été développé plus tôt que BLIP-2, en utilisant la même idée de transfert d'attention mais dans chaque couche de LLM, et non un seul pont.

### Les descendants de 2026

- Q-Former: BLIP-2, InstructBLIP, MiniGPT-4 et la plupart des modèles vidéo-langue pour des raisons de budget de jeton.
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEAO) est une initiative de la Commission européenne sur les droits de l'homme (CEDEAO).
- Le modèle de réception: la variante Flamingo (leçon 12.04); la famille Idefics, Eagle, OmniMAE.
  Le modèle de percepteur:Flamingo's变体 (Flamingo's变体)
- Le projetor MLP: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  Le projet de loi de la loi de l'Union européenne sur les droits de l'homme est une loi de l'Union européenne sur les droits de l'homme.
- La salle d'attention: VILA, PaliGemma.
  Il est également connu pour sa grande popularité.

La question cruciale est de savoir si vous êtes limité par le budget des jetons ou par la qualité par jeton.

> Les quatre solutions sont efficaces. La question de la détermination est de savoir si votre limite est le token.

## Utilisez-le avec le cadre de réalisation
```figure
modality-projection
```

## Utilisez-le

`code/main.py`construit une attention croisée de style Q-Former:

> `code/main.py`Construire une bibliothèque standard Q-Former 风格的交叉注意力:

1. Simuler 256 jetons de patch d'image (dim 128).
   Le code de la page d'accueil est le code de la page d'accueil.
2. 32 requêtes instantanées à apprendre (dim 128).
   Le nombre de personnes interrogées est de 128.
3. Exécuter l'attention croisée produit-point-échelle (Q des requêtes, K/V des correctifs).
   Le problème est que le système de contrôle de la sécurité est un système de contrôle de sécurité.
4. Projet à la dimension LLM (512) via une couche linéaire.
   Le texte est en français: "L'écriture est une œuvre de la création".
5. Sortez les 32 jetons visuels prêts à être réalisés.
   Le code de la loi est le code de la loi.

Toutes les mathématiques en Python pur (boucles nichés sur des vecteurs). Jouet mais forme correcte. La matrice de poids d'attention est imprimée afin que vous puissiez voir quels patchs chaque requête est tirée de.

> Toutes les mathématiques fonctionnent avec Python purement. Vous pouvez voir chaque requête à partir de quelles patches.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-modality-bridge-picker.md`. Compte tenu de la configuration VLM cible (compte de jetons d'encodeur de vision, budget de contexte de LLM, contraintes de déploiement, objectif de qualité), il recommande le reéchantillon Q-Former vs MLP vs Perceiver avec une courte justification et une estimation du nombre de paramètres pour chaque pont.

> 本课产 出 `outputs/skill-modality-bridge-picker.md` donner un objectif VLM 配置(Vision编码器 token 数、LLM 上下文预算、部署约束、质量目标), il propose Q-Former vs MLP vs Perceiver resampler, avec un court argument et une estimation des paramètres de chaque couche de pont。

## Les exercices

1. Implémenter le bloc d'attention croisée dans PyTorch. Vérifiez que, avec 32 requêtes et 256 touches/valeurs, la matrice de poids d'attention est 32 x 256 et que chaque rangée s'élève à 1 après softmax.
   Le nombre de points de réponse est de 32 à 256 points, la fréquence de réponse est de 32 x 256, la ligne de réponse est de 1 à 1 point.

2. Dans BLIP-2 étape 1, le Q-Former effectue trois pertes simultanément: ITC, ITM, ITG. Écrivez la signature avant pour chacun en pseudo-code.
   En français, le code de code de référence est utilisé pour écrire chaque code de référence.

3. Comparer les nombres de paramètres: Q-Former (12 couches, 768 cachées) contre un projecteur MLP à 2 couches (1408 → 4096, deux couches).
   Comparer avec le nombre de participants: Q-Former (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-Former) (Q-For-L) (Q-For-For-L) (Q-For-L) (Q-L) (Q-For-L) (Q-For-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q-Q

4. Lisez la section 3.2 du document BLIP-2 (arXiv:2301.12597) sur la façon dont le Q-Former est initialisé.
   Le texte de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie

5. Pour une vidéo de 10 minutes à 1 FPS échantillonnée à 60 images, calculer le coût de jeton par image à (Q-Former → 32 jetons/image) vs (MLP projecteur → 576 jetons/image).
   Pour 10 minutes de vidéo à 1 FPS 采样为 60 ,计算每代币 成本:(Q-Former → 32 de la jeton/) vs.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Encore une lecture

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) le papier de base.
  Le texte de la première partie de la série est le texte de la première partie de la série.
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) le prédécesseur avec le trio ITC/ITM/ITG.
  Le premier est le premier, qui comprend la CSI/ITM/ITG 三联损失──.
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) "align avant fusible"  l'ancêtre conceptuel de la formation de phase 1.
  Le concept de formation de la première phase est le premier.
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500) Q-Former, qui connaît les instructions.
  Le Q-Former est un commandement.
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) approche à projecteur seulement.
  Le projet de loi de la loi de l'Union européenne sur les droits de l'homme
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) architecture générale pour l'attention croisée entre les questions apprenantes.
  Le système de formation est un système de formation de formation.
