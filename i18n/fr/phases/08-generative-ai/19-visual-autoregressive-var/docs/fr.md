# Modélisation autorégressive visuelle (VAR): Prédiction à l'échelle suivante

> Les modèles de diffusion échantillonnent de manière itérative dans le temps (désignant les étapes). Les échantillons VAR échantillonnent de manière itérative dans l'échelle  il prédit un jeton 1x1, puis 2x2, puis 4x4, jusqu'à la résolution finale, chaque échelle conditionnant sur la précédente.

> **【中文解读】**扩散模型在时间维度上代采样 (代采样), VAR在尺度维度上代先预测 1x1 token,再2x2,再4x4,直到目标分辨率──2024年论文证明 VAR 展现了GPT 风格的规模法,在相同计算预算下超越DiT──

> **【拓展：VAR 是生成模型的新范式】**VAR va se retourner à l'idée de passer de "next one token" à "next one scale", ouvrant une nouvelle direction à la production d'images.

**Type:** Build / 构建型
**Languages:** Python (with PyTorch)
**Prerequisites:** Phase 7 Lesson 03 (Multi-Head Attention / 多头注意力), Phase 8 Lesson 06 (DDPM)
**Time:** ~90 minutes

## Le problème , l' introduction du problème

La génération autorégressive domine la modélisation du langage parce qu'elle évolue de manière prévisible: plus de calcul, plus de paramètres, moins de perplexité, de meilleures sorties. La génération d'images a eu deux tentatives principales de RA avant 2024: PixelRNN/PixelCNN (pixel-par-pixel) et DALL-E 1 / Parti / MuseGAN (token-par-token sur les codes VQ-VAE).

> La production d'images pré-images de 2024 a été principalement réalisée par l'entreprise de production de images de 2024 et de 2024 et est principalement réalisée par la société de production de images de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2024 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 2040 et de 20 de notre année.

Les pixels et les jetons sont disposés dans une grille 2D, mais le modèle AR doit les visiter dans un ordre raster 1D. Un pixel de coin précoce n'a aucune idée de ce que l'image devient finalement.

> Les deux sont confrontés à des problèmes de séquence de génération. Les images et les symboles sont classés dans le réseau 2D, mais les modèles AR doivent être visités en séquence de lumière 1D. Les premiers angles ne savent pas ce que l'image finira par devenir.

VAR résout le problème de l'ordre de génération en modifiant ce qui est généré. Au lieu de prédire les jetons d'image un par un dans l'espace, VAR prédit une image entière à des résolutions croissantes. Étape 1: prédire un jeton 1x1 (l'image globale " résumé "). Étape 2: prédire une grille de jetons 2x2 (caractéries plus grossières). Étape 3: prédire une grille 4x4. Étape K: prédire la grille finale (H/8) x ((W/8)).

> VAR 通过改变生成对象来修复生成顺序问题──不再逐空间预测图像代币, VAR 以增分辨率预测整个图像──步骤 1:预测 1x1代币(全局摘要)──步骤 2:预测 2x2代币 网格──步骤 K:预测最终网格──

Chaque échelle suit toutes les échelles précédentes (causalement dans l'ordre de l'échelle) et parallèle dans sa propre échelle.

> Chaque mesure prend en compte toutes les mesures précédentes (en conséquence de la "souverture de la mesure"), et s'écoule dans sa propre mesure.

> **【中文解读】**L'innovation centrale de VAR(Visual Autoregressive): la génération d'images se déclenche dans un ordre de retour de "image par image/token" à "mesure par mesure"― prédiction de résumé général de 1x1, de 2x2 à gros caractères, de 4x4 à petits détails, jusqu'à la résolution de l'objectif― génération intégrée de chaque dimension, éliminant les "problèmes de génération de séquences" de l'image AR traditionnelle―2024

> **【拓展：VAR 与扩散模型的对比】**Le VAR est le modèle de répartition le plus potentiel après l'image générateur de nouvelles formes. Les avantages: 1) une loi de mise à l'échelle claire comme GPT; 2) un processus de production structurée, plus conforme à la perception humaine; 3) un budget de calcul dépassant le même DiT.

## Le concept de base.

### Le marqueur à échelle multiple VQ-VAE

> ### VQ-VAE Tokenizer à plusieurs dimensions

Le VAR a besoin d' une**multi-scale discrete tokenizer**Pour une image x, elle produit une séquence de grilles de jetons de résolution progressivement plus élevée:

> VAR  besoin d'un**多尺度离散 tokenizer**Pour une image x, il produit une série de symboles de résolution accrue:

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

Chaque z_k utilise le même codebook (taille typique 4096-16384). La tokenization à chaque échelle n'est pas indépendante  elle est formée de sorte que la somme des résidus à chaque échelle reconstruit f:

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

C' est une**residual VQ**L'échelle k capture ce que les échelles 1..k-1 ont manqué.

> C'est une**残差 VQ**变体──尺度 k 捕获尺度 1..k-1 遗漏的内容──解码器将所有尺度嵌入并产生图像──

Le tokenizer VQ à grande échelle est entraîné une fois (comme VQGAN) puis congelé.

> Multi-dimension VQ Tokenizer  entraînement une fois (comme VQGAN) puis结── Tout le travail de production est effectué par le modèle de retour de la haute couche.

### Prédition à l'échelle suivante

> ### Prévision de la taille

Le modèle génératif est un transformateur qui voit les jetons de toutes les échelles précédentes et prédit les jetons à l'échelle suivante.

> 生成模型 est un transformateur, voir tous les symboles de la précédente dimension et prédire le symbole de la prochaine dimension.

Structure de séquence d'entrée:
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

Les emplacements de position codent à la fois l'indice d'échelle et la position spatiale dans l'échelle. L'attention est causelle dans l'ordre d'échelle: le jeton à l'échelle k, position (i, j) peut attirer tous les jetons à l'échelle 1..k et les jetons à l'échelle k eux-mêmes qui viennent plus tôt dans l'ordre intra-échelle utilisé (VAR utilise l'attention positionnelle fixe sans causalité intra-échelle  toutes les positions dans une échelle sont prédites en parallèle).

Perte de formation: à chaque échelle k, prédire les jetons z_k donnés à tous les jetons de l'échelle précédente. Perte d'entropie croisée sur les codes VQ discrets. La même structure que GPT sauf la "sequence" est maintenant structurée à l'échelle.

### Génération

Pour la conclusion:
```
generate z_1 = sample from p(z_1)                    # 1 token
generate z_2 = sample from p(z_2 | z_1)              # 4 tokens in parallel
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 tokens in parallel
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

Pour une échelle K = 10, la génération est de 10 passes transformateurs avant. Chaque pass produit son échelle entière en parallèle  pas d'autorégression par jeton dans une échelle. Pour une image 256x256, cela représente environ 10 passes par rapport à 28-50 de DiT.

> Pour K = 10 dimensions, la génération est 10 transformateurs avant de se propager.

### Pourquoi la prochaine édition gagne la prochaine édition

> ### Pourquoi la taille de la marque est supérieure à la taille de la marque ?

Trois victoires structurelles:

> Trois avantages structurels:

1. **Coarse-to-fine aligns with natural image statistics.**La perception visuelle humaine et les ensembles de données d'images présentent à la fois des régularités dépendantes de l'échelle: la structure à basse fréquence est stable et prévisible; les détails à haute fréquence sont conditionnés par le contenu à basse fréquence.
   **从粗到细与自然图像统计一致。**低频结构稳定可预测;高频细节依赖低频内容──
2. **Parallel generation within scale.**Contrairement au GPT-style token AR, VAR produit tous les tokens à l'échelle en une seule étape.
   **尺度内并行生成。**Contrairement aux symboles AR, VAR produit un seul pas de toute la taille de tous les symboles.
3. **No generation order bias.**Les jetons à l'échelle k voient tous l'échelle k-1; il n'y a pas de biais "de gauche" ou "de dessus" qui oblige les jetons précoces à s'engager avant que le contexte tardif ne soit disponible.
   **无生成顺序偏差。**Voir la note de la taille K-1.

### Loi de l'échelle

> ### Loi de l' écaillage / 缩放定律

Tian et al. Il a démontré que le VAR suit une courbe d'échelle de la loi de pouvoir pour la FID sur ImageNet  tout comme le GPT le fait pour la perplexité. Le doublage des paramètres ou du calcul réduit de manière fiable l'erreur de moitié. C'était le premier modèle générateur d'images à exprimer ce type de comportement d'échelle aussi nettement que les modèles de langage. Le résultat est que les prédictions à l'échelle VAR deviennent prévisibles à partir de calcul, et non des conjectures empiriques par architecture.

> Tian 等人 prouve que VAR sur ImageNet suit une courbe d'agrégation selon la loi  comme GPT à la confusion .

### La relation avec la diffusion

> ### Relation avec le modèle de diffusion

La VAR et la diffusion partagent la même histoire de compression de données: les deux décomposent le problème de génération en une séquence de sous-problèmes plus faciles.

> VAR et diffusion partagent les mêmes données de compression histoire: tout va générer des problèmes se décomposer en un ensemble de questions plus simples.

- Diffusion: ajoutez progressivement du bruit, apprenez à annuler une étape.
  扩散: progressivement augmenter le bruit, apprendre à retirer progressivement.
- VAR: ajoutez progressivement la résolution, apprenez à prédire la prochaine échelle.
  VAR: progressivement augmenter la résolution, apprendre à prévoir la mesure de la résolution.

Les deux génèrent des distributions conditionnelles traitables. En empirie, le VAR est plus rapide à l'inférence (moins de passes, toutes parallèles dans une échelle) et correspond ou bat le DiT sur l'ImageNet classé.

> Les deux sont des conditions de traitement de la distribution de la question.

## Construisez-le et mettez-le en œuvre.
```figure
gx-var-next-scale
```

## Faites-le

Dans `code/main.py`vous allez:
1. Faites une petite .**multi-scale VQ tokenizer**sur des données "image" synthétiques (2 anneaux gaussiens en D).
2. - Le train a**VAR-style transformer**pour prédire les jetons à l'échelle suivante.
3. Prenez l'échantillon en appelant le transformateur 4 fois (4 échelles) et décodant.
4. Vérifiez que la formation organisée à l'échelle rend la génération parallèle à l'échelle.

Il s'agit d'une mise en œuvre de jouets. Le but est de voir le masque d'attention structuré à l'échelle et la génération parallèle à l'échelle fonctionner réellement.

> Il s'agit d'un jouet de réalisation. L'important est de voir la structure de la mesure et la concentration de l'attention sur la mesure et la production de vrais travaux.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-var-tokenizer-designer.md` une compétence pour concevoir un tokenizer à plusieurs échelles: nombre d'échelles, ratios d'échelle, taille de codebook, partage résiduel, architecture de décodeur.

> 本课产生 `outputs/skill-var-tokenizer-designer.md` Design multi-dimension Tokenizer compétences: nombre de mesures, proportion de mesures, taille de taille, décalage de partage, structure de code.

## Les exercices

1. **Scale count ablation.**Traînez VAR avec des échelles 4, 6, 8, 10. Mesurez la qualité de la reconstruction par rapport au nombre de passes autorégressives. Plus de échelles = plus de résidus fins = meilleure qualité mais plus de passes.

2. **Codebook size.**Les codes de train avec des codes de taille 512, 4096, 16384 offrent une meilleure reconstruction mais une prédiction plus difficile.

3. **Parallel-within-scale check.**Pour un VAR formé, mesurez explicitement le modèle d'attention. Dans l'échelle k, le modèle prend-il en charge des positions à l'échelle transversale mais pas à l'échelle interne?

4. **VAR vs DiT scaling.**Pour la même tâche de classe ImageNet, entraînez VAR et DiT à des budgets paramétriques correspondants (par exemple, 33M, 130M, 458M).

5. **Text conditioning.**Extension de VAR pour prendre une intégration de texte (CLIP pooled) comme entrée de conditionnement supplémentaire via adaLN. C'est la recette HART.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| VAR | "Visual AutoRegressive" | Image generation by next-scale prediction over a pyramid of VQ token grids |
| Next-scale prediction | "Predict coarser, then finer" | The model predicts tokens at increasing resolution scales, conditioning on all previous scales |
| Multi-scale VQ tokenizer | "Residual VQ" | VQ-VAE that produces K token grids of increasing resolution, with decoder summing all scales |
| Scale k | "Pyramid level k" | One of K resolution levels, from 1x1 at k=1 up to (H/p)x(W/p) at k=K |
| Parallel-within-scale | "One forward per scale" | All tokens at scale k are predicted in one transformer pass, not autoregressively |
| Causal-across-scales | "Scale-ordered attention" | Token at scale k can attend to all of scales 1..k but not scales k+1..K |
| Residual VQ | "Additive tokenization" | Each scale's tokens encode the residual left by lower scales; decoder sums all scale embeddings |
| VAR scaling law | "Image GPT scaling" | FID follows a predictable power law in compute, like language models' perplexity |
| HART | "Hybrid VAR + text" | Text-conditional VAR variant combining MaskGIT-style iterative decoding with VAR's scale structure |
| Scale position embedding | "(scale, row, col) triple" | Positional encoding carries both the scale index and spatial coordinates within the scale |

## Encore une lecture

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) le document VAR, référence canonique
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) DiT, la ligne de base de comparaison de diffusion
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) VQGAN, le tokenizer de la famille VAR
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) VQ-VAE, fondement de la symbolisation discrète d'images
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) VAR en termes de texte
