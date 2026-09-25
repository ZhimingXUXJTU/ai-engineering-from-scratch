# Show-o et Discrète-Diffusion Modèles Unifiés

> La transfusion mélange des représentations continues et discrètes. Show-o (Xie et coll., août 2024) va dans l'autre sens: les jetons texte utilisent la prédiction de jetons suivants de causalité, les jetons d'image utilisent la diffusion discrète masquée dans l'esprit de MaskGIT. Ils sont tous deux assis à l'intérieur d'un transformateur avec un masque d'attention hybride. Le résultat unifie VQA, texte à image, en peinture et génération de modalités mixtes sur une colonne vertébrale, un tokenizer par modalité, une formulation de perte (next-token étendu à la prédiction masquée). Cette leçon traverse le design Show-o  pourquoi la diffusion discrète masquée est un générateur d'images parallèle, en quelques étapes  et contraste avec Transfusion et Emu3.

> **【中文解读】**Show-o(2024年8月)走另一条路:文本代币 用因果下一代币 预测,图像代币 用掩码离散散散散散(MaskGIT风格) ・・・ les deux utilisent un transformateur, avec mixed attention掩码。 résultat est un point de contrôle 同时支持VQA、文本生成图像和图像修复──

> **【拓展：并行解码的速度优势】**Le Show-o produit des images qui nécessitent seulement environ 16 étapes, tandis que le Chameleon/Emu3 a besoin de 1024-4096 étapes, ce qui rend le Show-o le plus rapide dans le modèle de vie, mais la qualité de l'image est limitée à la reconstruction du jeton VQ.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Je suis en train de faire une analyse de la situation de la machine à sous. Je suis en train de faire une analyse de la situation de la machine à sous.
>  **【类比】**Show-o = "并行开锁"──Emu3 = 一把钥匙开 1024 把锁(自归单个代币);Show-o = 16 步内同时尝试所有锁(掩码扩散并行解码)──代价:图像质量略差(VQ 量化损失),但推理快得多──

## Objectifs d'apprentissage

- Expliquer la diffusion discrète masquée: le calendrier qui masque uniformément les jetons demande ensuite au transformateur de les récupérer.
  > Expliquer le cache: le token de cache est normal, puis laisser le Transformer reprendre sa régulation.
- Comparer le décoding d'image parallèle (Show-o, MaskGIT) au décoding d'image autorégressif (Chameleon, Emu3) en termes de vitesse et de qualité.
  > Comparer avec le modèle de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image.
- Nombre des trois tâches que Show-o gère dans un seul point de contrôle: T2I, VQA, peinture d'image.
  > 列举 Show-o dans un point de contrôle
- Choisissez un calendrier de masquage (cosine, linéaire, tronqué) et raisonnez de son effet sur la qualité de l'échantillon.
  > 选择掩码调度 (余弦、线性、截断) et analyser son impact sur la qualité de la séquence.

## Le problème , le contexte .

La formation à deux pertes de transfusion fonctionne mais a une dynamique plus délicate. La perte de diffusion continue vit à une échelle numérique différente de la perte NTP discrète.

> L'entraînement à la double perte de transfusion est possible mais le processus est plus complexe  perte de propagation continue et perte de NTP dispersée perte différente sur la échelle numérique .

La réponse de Show-o: gardez les deux modalités discrètes (comme Chameleon), mais générez des images en parallèle via une diffusion discrète masquée au lieu de séquentiellement.

> Réponse: maintenir deux modes sont dispersés, mais par le biais de masquer des formes de diffusion et de génération d'images, et non par ordre de génération.

## Le concept de base.

> **【中文解读】**Show-o 统一多模态理解和生成, utiliser le dispersé diffuser pour remplacer la tradition continual diffuser。 dispersé diffuser directement dans les opérations de niveau de jeton, va couvrir les prévisions  understanding tasks) et le dés noise 生成任务) uni uni dans le même cadre。

> **【拓展：离散扩散的统一优势】**离散扩散将文本生成和图像生成统一到同一个数学框架 () 掩码代币 预测), rendant le train de combinaison de plusieurs modèles plus simple.


### Diffusion discrète masquée (MaskGIT)

Le truc original de Chang et al. (2022) MaskGIT est élégant. Commencez par une image entièrement masquée (chaque jeton est le spécial `<MASK>`à chaque étape, prédire tous les jetons masqués en parallèle, puis garder les prédictions les plus confiantes et re-masquer le reste. Après ~ 8 à 16 itérations, tous les jetons sont remplis. Le calendrier du nombre de jetons à démasquer par étape est réglé  les calendriers cosines fonctionnent bien.

> Les techniques de masque sont très élégantes.`<MASK>`ID) ⋅ par étape et prévoit tous les jetons masqués, puis conserve le top-K 最有信心的预测并重新掩盖其余的── par environ 8-16 fois代, tous les jetons sont remplis── par étape et combien de jetons la régulation doit réguler 余弦调调度效果好──

La formation est simple: échantillonnage d'un ratio de masquage uniformément à partir de [0, 1], appliquer sur les jetons VQ de l'image, entraîner le transformateur à récupérer les jetons masqués.

> 训练很简单: de [0, 1] 均采样掩码比例, appliqué à l'image du jeton VQ, 训练 Transformer 恢复被掩码的 jeton──就是BERT对文本做,扩展到图像生成──

### Show-o: un transformateur, masque hybride

Le show-o met MaskGIT à l'intérieur d'un transformateur de modèle de langage causale.

> Le modèle de la langue de la transformation est:

- Les jetons texte: causels (MLL standard).
  Le code de la loi est le code de la loi.
- Tokens d'image: bidirectionnels complets dans le bloc d'image (les tokens masqués peuvent donc voir tous les autres tokens d'image pendant la prédiction).
  Le symbole du masque peut être vu à l'avance.
- Text-to-image: le texte répond aux images précédentes, l'image répond au texte précédent.
  Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français

Les stages de formation alternent entre:
1. NTP standard sur les séquences de texte.
   NTP à la base de la norme.
2. T2I: texte → image avec des jetons d'image masqués, perte de prédiction de jetons masqués.
   Le code de la carte de crédit est un code de crédit qui est utilisé pour les transactions de transactions de transactions.
3. VQA: image → texte avec des jetons de texte masqués (en réalité seulement NTP).
   Le texte de la note de référence est le texte de la note de référence.

La perte unifiée est l' entropie croisée sur `<MASK>`les jetons, qui couvrent à la fois le NTP texte (seul le dernier jeton est "masqué") et la diffusion masquée d'image (un sous-ensemble aléatoire est masqué).

> La perte est`<MASK>`Le seul signe est le "masquerode" de) et l'image masquerode est diffusée (随机子集被掩码)

### Prise d'échantillons parallèles

Show-o génère une image en ~16 étapes au lieu de ~1000 (autorégressif par jeton) ou ~20 (diffusion). À chaque étape, prédisez tous les jetons masqués en parallèle; commettez le top-K confident; répétez.

> Show-o dans environ 16 étapes de génération d'image, plutôt que d'environ 1000 étapes de chaque jeton de retour) ou d'environ 20 étapes de propagation)

Comparer:
- Chameleon / Emu3 (autorégressif sur les jetons): N_tokens passes en avant, généralement 1024-4096 par image.
  Le mot "Chameleon" est traduit par "Chameleon" (en anglais: Chameleon) et "Emu3") est traduit par "Chameleon" (en anglais: Emu3(逐符号自归):N_tokens 次前向传播,通常每张图像 1024-4096──
- Transfusion (diffusion continue): ~ 20 étapes, chaque étape est une transformer complète.
  Transfusion: environ 20 étapes, chaque étape une fois.
- Show-o (diffusion discrète masquée): ~16 étapes, chaque étape avec un transformateur complet.
  Le changement de format est le plus important dans la vie.

Le show-o est plus rapide que le chamélion sur des modèles à l'échelle similaire, correspond à peu près au nombre d'étapes de transfusion avec un coût par étape inférieur (logits vocabulaires discrets par rapport à la perte continue de MSE).

> Le nombre de étapes correspondant à la transfusion est plus rapide que celui du chameau, mais le coût par étape est plus faible.

### Les tâches effectuées à un seul point de contrôle

Show-o prend en charge quatre tâches à l'inférence, sélectionnées par format prompt:

> Show-o en proposant le soutien à quatre tâches, en suggérant le format de sélection:

- Génération de texte: sortie de texte autorégressif standard.
  Le texte est traduit en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " textes " et " textes " en français par " .
- VQA: image dans, message de sortie.
  Le texte est en anglais.
- T2I: texte dans, image hors via diffusion discrète masquée.
  Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français
- Peinture: image avec des jetons masqués, remplissez.
  Le code de la carte de crédit est le code de la carte de crédit.

La capacité d'inpeinture est gratuite grâce à la formation de prédiction masquée. Masquer une région de la grille de jetons VQ, alimenter le reste plus une requête de texte, prédire les jetons masqués.

> 图像修复能力从掩码预测训练中免费获得──掩码 VQ token 网格的一个区域,进入其余部分加上文本提示,预测被掩码的 token──

### Calendrier de masquage

Le calendrier du nombre de jetons à démasquer par étape forme la qualité.

> Chaque étape de la rédaction de la note de référence est la suivante:

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

À l'étape 0, tous les jetons masqués (ratio 1.0). à l'étape T, aucun masqué. Cosine concentre la masse sur des ratios de milieu de gamme où la prédiction est la plus informative.

> La quantité de chaînes est concentrée sur la quantité de chaînes de mesure, la quantité de chaînes de mesure est aussi disponible mais plus tôt.

### Le spectacle

Show-o2 (2025 suivi, arXiv 2506.15564) échelles Show-o: plus grande base de LLM, meilleur tokenizer, meilleur calendrier de masque.

### Là où se trouve Show-o

Dans la taxonomie de 2026:

> Dans les catégories de l'année 2026:

- Les jetons discrets + NTP: Chameleon, Emu3.
  Le mot de passe est "Chameleon"", ému3"", simple mais à la légère".
- Les jetons discrets + diffusion masquée: Show-o, MaskGIT, LlamaGen, Muse. Prise parallèle, encore perdue par le jetoniseur.
  Le mot "déjà" est traduit par "déjà" et "depuis" par "déjà".
- Transfusion continue + diffusion: transfusion, MMDiT, DiT. Formation de la plus haute qualité et plus complexe.
  Le plus grand nombre de personnes qui ont été vaccinées sont des personnes qui ont été vaccinées.
- Parallèle continu + flux dans un VLM: JanusFlow, InternVL-U. Nouveau.
  Le groupe de travail de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de l'équipe de l'équipe de l'équipe de formation de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de la région.

Choisir par tâche: Show-o lorsque vous voulez T2I + incarné + VQA dans un modèle ouvert avec une vitesse raisonnable; transfusion lorsque la qualité est primordiale et que vous pouvez vous permettre la plomberie à deux pertes.

> 按任务选择: nécessite un modèle ouvert en même temps T2I + 修复 + VQA 且速度合理时选 Show-o;质量至上且能承担双损失复杂性时选转血。


> **【拓展：Show-o 的离散扩散方法】**Le modèle de projection est un symbole de couverture. La partie de la couverture est une partie de la couverture.


## Utilisez-le en pratique
```figure
masked-diffusion-unmask
```

## Utilisez-le

`code/main.py`simulation de l'échantillonnage à démonstration:

> `code/main.py`模拟 Show-o 采样:

- Une grille de jouets de 16 jetons VQ.
  Un jeu de 16 VQ.
- Un faux "transformateur" qui prédit les logits en fonction d'un prompt et des jetons actuellement démasqués.
  Le code de la ligne de référence est le code de la ligne de référence.
- Prise d'échantillons masqués parallèles sur 8 étapes avec calendrier cossin.
  Le texte est en français:
- Imprime les états intermédiaires (évolution du modèle de masque) et les jetons finaux.
  Le mot de passe est le mot de passe de la langue française.

Faites-le, regardez le masque se dissoudre étape par étape.

> Il faut le faire, observer le cache-cache.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-unified-gen-model-picker.md`. Étant donné qu'un produit nécessite à la fois une compréhension (VQA, sous-titres) et une génération (T2I, peinture) avec une contrainte de poids ouvert, choisissez entre la famille Show-o, la famille Transfusion/MMDiT et la famille Emu3/Chamélion avec des compromis concrets.

> 本课产 出 `outputs/skill-unified-gen-model-picker.md`△ donner une définition nécessaire à la compréhension de la production et de la production de produits, en particulier les produits à charge ouverte, en fonction de la taille et du poids de la production.

## Les exercices

1. Des échantillons discrets de diffusion masqués en 16 étapes. Pourquoi pas 1? Qu'est-ce qui se brise si vous démasquez tout à l'étape 0?
   Pourquoi pas 1 étape ? Si tout le jeton est dissimulé à la première étape, comment cela se passerait ?

2. La peinture est gratuite avec diffusion masquée. proposez un cas d'utilisation du produit (réel ou hypothétique) où la peinture de Show-o dépasse un modèle spécialisé.
   Le modèle de réparation est gratuit.

3. Calendrier cosine vs calendrier linéaire: tracer le nombre de jetons non masqués par étape pour T=8.
   Le nombre de couches est plus équilibré.

4. Une image 512x512 Show-o est de 1024 jetons. À la voyelle K = 16384, le modèle émet 1024 * log2(16384) = 14.336 bits (~1.75 KiB) de données.
   Le modèle est un modèle de production de 1,75 KiB de données. Le modèle est un modèle de production de 768 KiB de images.

5. Comment le modèle d'image autorégressive classal de LlamaGen diffère-t-il de l'approche masquée de Show-o ?
   Quelle est la différence entre les conditions de classification de LlamaGen et la méthode de masquage de Show-o ?

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Encore une lecture

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Le thème de la série est "La vie est une chose".
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  Le film est sorti en version originale.
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  Le travail original de MaskGIT est un ouvrage de masque.
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  Le film est sorti en version originale.
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  Le mot "Muse" est traduit par "Muse".
