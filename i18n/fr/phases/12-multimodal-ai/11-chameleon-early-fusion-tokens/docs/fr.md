# Chameleon et les jetons de fusion précoce - Modèles multimodels uniquement

> Chaque VLM que nous avons vu jusqu'à présent garde des images et du texte séparés. Les jetons visuels proviennent d'un encodeur de vision, circulent dans un projecteur, puis rencontrent le texte à l'intérieur du LLM. Le vocabulaire de vision et de texte ne se chevauchent jamais. Le chameau (Meta, mai 2024) a demandé: et si c'était le cas ? Formez un VQ-VAE qui transforme une image en une séquence de jetons distincts à partir d'un vocabulaire partagé. Chaque document multimodal est maintenant une séquence  de jetons de texte et de jetons d'image interlevées, une seule perte autorégressive. Effets secondaires: le modèle peut générer des sorties de modalité mixte  des jetons de texte et d'image alternés dans un seul appel d'inférence. Cette leçon lit la thèse de la fusion précoce et construit une version de jouet de bout en bout.

> **【中文解读】**Chameleon (Meta, 2024: 5 mai 2014) propose une méthode de multiple mode: avec VQ-VAE, l'image sera transformée en jeton dispersé, avec le jeton texte, partagé avec un même tableau de mots, avec un seul entraînement de perte de retour.

> **【拓展：早期融合 vs 后期融合】**之前所有 VLM(LLaVA、BLIP-2、Qwen-VL)都保持图像和文本分离──Chameleon's "early fusion" signifie que les images et le texte sont traités depuis le début dans le même espace, le modèle peut naturellement se substituer à la sortie du texte et de l'image── c'est le point de départ de la famille de modèle (Emu3、Show-o、Janus-Pro)

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Le changement de la phase de transformation est le changement de la phase de transformation de la phase de transformation.
>  **【类比】**Chameleon = " monde ";;LLaVA = 翻译机;;Vision编码器把图片翻译成 LLM 能懂的语言);Chameleon = 世界语;;图片和文本都用同一种人造语言,模型不用翻译);;

## Objectifs d'apprentissage

- Expliquez pourquoi un vocabulaire partagé + une seule perte modifie ce que le modèle peut faire.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力──
- Décrivez comment un VQ-VAE symbolise une image en une séquence discrète compatible avec l'objectif de la prochaine marque d'un transformateur.
  >  Description VQ-VAE  comment mettre en place une image分词为与变压器 下一代令子 目标兼容的分散序列──
- Nommez les astuces de stabilité de formation de Chameleon: QK-Norm, placement de démission, commandement de LayerNorm.
  > 列举 Chameleon's training稳定性技巧:QK-Norm、Dropout 位置、LayerNorm 顺序。
- Comparez l'approche Q-Former de Chameleon versus BLIP-2 et décris quand chacune est le bon choix.
  > Comparer le schéma Q-Former du Chameleon à celui du BLIP-2, décrivez les scénarios qui correspondent à chacun.

## Le problème , le contexte .

Les VLM basés sur l'adaptateur (LLaVA, BLIP-2, Qwen-VL) traitent le texte et l'image comme deux choses différentes.`embed(text_token)`Une image passe à travers `visual_encoder(image) → projector → ... pseudo_tokens`Le modèle a deux voies d'entrée qui se fondent en partie.

> Le texte et l'image sont divisés en deux types.`embed(text_token)`- Il est en train de passer .`visual_encoder(image) → projector → ... pseudo_tokens`◊ Modèle a deux voies d'entrée en milieu de la combinaison ◊

Trois conséquences:

> Trois résultats:

1. Le LLM ne peut consommer que des images, pas les émettre.
   L'image est seulement consommée, elle ne peut pas être produite.
2. Les documents de modalité mixte (paragraphes et images alternés, comme dans un article) sont gênants  vous analysez soit l'entrée multimodal en dehors du modèle, soit les générations de chaîne.
   Le modèle est un modèle de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de
3. Les jetons visuels et les jetons texte vivent dans différentes régions de l'espace caché, créant des problèmes d'alignement subtils.
   Le symbole de la vision et le symbole du texte se trouvent dans différentes régions de l'espace caché, ce qui pose de petits problèmes de coordination.

Chameleon rejette cette hypothèse: les images ne sont que des séquences de jetons distincts d'un vocabulaire partagé.

> Chameleon a rejeté cette hypothèse: l'image est simplement un ensemble de jetons de partage.

## Le concept de base.

> **【中文解读】**Chameleon (Meta) adopte une stratégie de fusion précoce: images et textes sont dispersés en un seul séquence de symboles, avec le même Transformer 处理── images via VQGAN 编码为离散代币,与文本代币 在同一词表中──

> **【拓展：早期融合 vs 晚期融合】**早期融合 (Chameleon) va être un mode multiple unifié à la même marque 空间, théoriquement plus beau mais le coût de formation est élevé.


### VQ-VAE en tant que marqueur d'image

Le tokenizer est un autoencodeur variatif quantifié par vecteur.

> 分词器 est un métro quantifié de variation de codeur.

- Encoder: CNN + ViT qui cartographient l'image à une carte spatiale, disons 32x32 caractéristiques de dim 256.
  Le format de l'image est le même que celui de la carte de l'image.
- Codebook: un vocabulaire appris de vecteurs K (Chameleon utilise 8192), également dim 256.
  Le nombre de mots utilisés par le Chameleon est de 256 .
- Quantification: pour chaque fonctionnalité spatiale, recherchez l'entrée de codebook la plus proche par distance L2. Remplacez la fonctionnalité continue par l'indice entier.
  Pour chaque caractéristique spatiale, utilisez L2 距离查找最近码本条目── pour remplacer les caractéristiques en entier.
- C'est CNN qui ramène les fonctionnalités quantifiées à des pixels.
  CNN va quantifier les caractéristiques de la reconstruction en images.

Formation: Perte de reconstruction de l'AEV + perte d'engagement + perte de codebook.

> 訓練:VAE 重建损失 + 承诺损失 + 码本损失──码本索引构成图像的离散字母表──

Pour le Chameleon: une image devient 32*32 = 1024 jetons tirés d'un vocabulaire de 8192. Concaténé avec des jetons de texte (du vocabulaire BPE du LLM, disons 32000).

> Pour le Chameleon: un image est transformé en 32*32 = 1024 个标签, de 8192 词汇表, de 32000 拼接, de 32000 拼接, de BPE 词汇表, de LLM 拼接, de 40192 转变器 看到一序列,一个损失──

### Le vocabulaire partagé

Le vocabulaire de Chameleon combine des jetons de texte, des jetons d'image et des séparateurs de modalité. Chaque jeton a un seul ID. La couche d'intégration d'entrée cartonne chaque ID vers un vecteur caché D-dim. Les cartes de projection de sortie sont cachées aux logits de vocabulaire. Softmax choisit le jeton suivant, quelle que soit la modalité.

> Le tableau de mots de Chameleon est composé de symboles de texte, de symboles d'images et de symboles de séparation. Pour chaque symbole, il y a un seul ID. Pour chaque symbole, il y a un seul ID. Pour chaque symbole, il y a un seul ID. Pour chaque symbole, il y a un seul ID. Pour chaque symbole, il y a un seul ID. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un seul symbole. Pour chaque symbole, il y a un symbole. Pour chaque symbole, il y a un symbole. Pour chaque symbole.

Les séparateurs sont importants: `<image>`et `</image>`Les balises sont en parenthèses de la séquence de jetons d'image. au moment de la génération, si le modèle émet `<image>`Le logiciel en aval sait que les 1024 prochains jetons sont des indices VQ à envoyer au décodeur pour la rendu des pixels.

> Il est important de se séparer .`<image>`et `</image>`标签包裹图像代币 序列──生成时,如果模型输出 `<image>`Le logiciel sait que les 1024 prochains jetons sont des index VQ, il faut les envoyer au décodeur pour les rendre intelligents.

### Génération de mobilité mixte

L'inference est la prédiction du prochain jeton dans le vocabulaire partagé.

> 推理是共享词汇表中的下一代币 预测。例提示:"画一只猫并描述它──"Chameleon 输出:

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

Le modèle choisit l'ordre de manière autonome  il peut produire une image puis un texte, un texte puis une image, ou interdire.

> Le modèle peut choisir son propre ordre, il peut choisir l'image, le texte, le texte, le texte ou le texte.

Comparer à des VLM adaptateurs où la génération est uniquement de texte.

> Avec l'adaptateur VLM (en anglais seulement)

### Stabilité de formation  QK-Norm, dérapagement, commandes LayerNorm

L'entraînement à la fusion précoce est instable à l'échelle.

> Le thème de l'éducation à la formation de la fusion précoce est un peu instable à grande échelle.

- QK-Norm. Appliquez LayerNorm à la requête et aux projections clés à l'intérieur de l'attention, avant le produit de point. empêche l'explosion de la magnitude logite à la profondeur. Utilisé par plusieurs grands modèles post-2024.
  La norme est utilisée dans les applications de la couche de l'attention et de la mise en œuvre de la norme, avant de se développer.
- Le décalage de la position. Le décalage après chaque ajout résiduel, pas seulement après l'attention et la MLP. Une régulation plus importante est nécessaire lorsque les gradients des jetons d'image peuvent dominer.
  Le décalage de la position. Il faut plus de normalisation lorsque le degré de la marque d'image peut dominer.
- LayerNorm ordonnage. Pré-LN sur la branche résiduelle (standard), plus un LN supplémentaire sur la connexion de saut du dernier bloc. Stabilise le débit de gradient de la couche finale.
  L'extension de la couche de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de l'étage de la ligne de la ligne de l'étage de la ligne de l'étage de la ligne de la ligne de l'étage de la ligne de la ligne de l'étage de la ligne de la ligne de la ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne

Sans ces astuces, l'entraînement du 34B-param Chameleon divergeait à plusieurs points de contrôle. Avec eux, il converge.

>  sans ces techniques, le chamelion de 340 milliards d'éléments  entraîne dans plusieurs points de contrôle  dispose d'elles, entraîne la collecte                                                                                                                                                                                                                                           

### Le plafond de reconstruction du jeton

Le VQ-VAE est une perte. Avec 8192 entrées de codebook et 1024 jetons par image 512x512, la reconstruction PSNR se situe entre 26 et 28 dB. Cela suffit pour une génération d'images reconnaissables mais est visiblement pire que la diffusion continue de l'espace (la diffusion stable 3 atteint 32+ dB).

> VQ-VAE est une image perdue. 8192 个码本条目和每张 512x512 图像 1024 个代币, reconstruit PSNR, limite supérieure d'environ 26-28 dB.

Le tokenizer est le goulot d'étranglement. Les meilleurs tokenizers (MAGVIT-v2, IBQ, SBER-MoVQGAN) soulevent le plafond. Emu3 (Létion 12.12) permet de générer une qualité SDXL par un seul tokenizer meilleur.

> Le groupe de travail de la société de développement a été créé en 2008 pour développer la technologie de développement de la technologie de l'information.

### Chameleon contre BLIP-2 / LLaVA

Chameleon (fusion précoce, vocabulaire partagé):
- Une perte, un décodeur.
  Un perdant, un décodeur.
- Génère une sortie de mode mixte.
  Le mot grec traduit par " production " est traduit par " production ".
- Le Tokenizer est le plafond de qualité.
  Le mot "parceau" est le mot "parceau".
- Coût: décodeur VQ-VAE par image générée sur le chemin d'inférence.
  Le système de calcul de la valeur de l'image est un système de calcul de la valeur de l'image.

BLIP-2 / LLaVA (fusion tardive, tours séparées):
- La vision est entrée, les messages sont envoyés.
  Le texte est en anglais.
- Reutilise le Master de droit prétrainé.
  Le traducteur de la langue française est le traducteur de la langue française.
- Pas de goulot d'étranglement pour comprendre.
  Le mot grec traduit par " compréhension " signifie " compréhension ".
- Passe unique en avant.
  Le mot "sans-souvenir" est traduit par "sans-souvenir".

Si vous avez besoin de génération d'images, famille Chameleon, si vous avez seulement besoin de compréhension, l'adaptateur VLM est plus simple et réutilise plus de calcul prétrainé.

> 按任务选择──如果需要图像生成,选择Chameleon 系列──如果只需要理解,适配器 VLM更简单且复用更多预训计算──

### Fuyu et AnyGPT

Fuyu (Adept, 2023) est une approche connexe: sauter le codeur de vision séparé entièrement, alimenter les patches d'image brutes à travers la projection d'entrée du LLM comme s'il s'agissait de jetons, pas de tokenizer.

> Fuyu(Adept,2023) est une méthode liée: complètement sauter au-delà de l'éditeur de visuel indépendant, va parfaire l'image originale par le biais de l'entrée de projet de LLM, comme si elles étaient des symboles, sans séparation de mots.

AnyGPT (Zhan et coll., 2024) étend le Chameleon à quatre modalités: texte, image, parole, musique. Le même truc VQ-VAE pour chacun, transformateur partagé.

> En 2024, le Chameleon s'étendra à quatre modèles: texte, images, voix, musique, etc.


> **【拓展：早期融合的训练挑战】**Le Chameleon de Meta utilise 8192 codex de VQGAN, qui a effectué des mesures précises entre la qualité de l'image et le texte (rFID de 5.0) et la compatibilité du texte.


## Utilisez-le en pratique
```figure
vq-codebook
```

## Utilisez-le

`code/main.py`construit un modèle de fusion précoce de bout en bout de jouet:

> `code/main.py`Construire un modèle de jeu de fin à fin:

- Un minuscule quantificateur de style VQ-VAE qui cartographient les correctifs 8x8 aux indices du codebook (K=16).
  Un petit quantificateur VQ-VAE, qui est équipé de patch 8x8
- Un vocabulaire partagé de (id du texte 0..31) + (id de l'image 32..47) + (separateurs 48, 49).
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Un décodeur autorégressif jouet (tableau de bigrammes) formé sur des légendes synthétiques + des séquences de jetons d'image.
  Une pièce à jouer à la mode est une pièce à jouer à la mode.
- Loup d'échantillonnage qui émet des jetons de texte + d'image alternés à une demande.
  Le texte est en train de changer en version originale.

Le code garde intentionnellement le transformateur en petits (bigrammes) afin que vous puissiez suivre le flux de signal de bout en bout.

> Le Transformer est très petit, pour que tu puisses suivre le signal.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-tokenizer-vs-adapter-picker.md`. Compte tenu d'une spécification de produit (comprendre seulement vs comprendre + générer, qualité d'image requise, budget de coûts), il choisit entre la famille Chameleon (fusion précoce) et la famille LLaVA (fusion tardive) et justifie avec des règles quantitatives.

> 本课产 出 `outputs/skill-tokenizer-vs-adapter-picker.md` Les produits sont conçus pour une utilisation de la technologie de l'information et de la communication.

## Les exercices

1. Chameleon utilise K=8192 entrées de codebook et 1024 jetons par image 512x512 . Estimer le rapport de compression par rapport à une image RGB 24 bits. Est-ce que c'est une perte ?
   Le nombre de pièces de rechange de l'image est de 512x512 images.

2. Une image 4K (3840x2160) à la même densité VQ-VAE produit combien de jetons d'image? un modèle de style chamélion peut-il générer une image 4K dans un appel d'inférence?
   Quels sont les symboles de l'image qui sont générés par le même modèle de caméléon ?

3. Implémenter QK-Norm en Python pur. Compte tenu d'une requête et d'une clé 64 dimensions, afficher le produit de point avant et après LayerNorm. Pourquoi le contrôle de la magnitude est important à la profondeur?
   Le code de la requête est utilisé pour la mise en œuvre de la norme QK-Norm.

4. Lisez la section 2.3 du Chameleon sur la stabilité de l'entraînement. Décrivez le mode de défaillance exact observé sur le papier à 34B sans QK-Norm.
   Le modèle de "Fan Number Explosion" est caractéristique de la "Fan Number Explosion".

5. Élargir le décodeur de jouet pour émettre une réponse de modalité mixte en cas de requête de texte uniquement. Mesurer la fréquence à laquelle le modèle choisit l'image-première par rapport au texte-première en cas de formation-distribution des données 60% texte-première / 40% image-première.
   En français, le modèle de mesure est le modèle de mesure de la fréquence de sélection des images par rapport aux données de formation.

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Encore une lecture

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  Le modèle de base de l'époque est le modèle de l'époque.
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  Le nom de la ville est le nom de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville.
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  Le roi de Babylone est un roi de Babylone.
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  En anglais, le terme "GPT" est traduit par "GPT".
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  Le programme de la vidéo est en cours de création.
