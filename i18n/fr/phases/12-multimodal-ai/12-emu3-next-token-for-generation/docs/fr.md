# Emu3: Prédiction de la prochaine génération de fichiers et de vidéos

> L'Emu3 de BAAI (Wang et al., septembre 2024) est le résultat de 2024 qui aurait dû mettre fin au débat diffusion-contre-autorégression. Un transformateur unique de décodeur de style Llama, formé uniquement sur l'objectif de prédiction de jeton suivant, sur un vocabulaire unifié de texte + jetons d'image VQ + jetons vidéo VQ 3D, bat SDXL sur la génération d'images et LLaVA-1.6 sur la perception. Pas de perte de CLIP. Pas de calendrier de diffusion. Les conseils sans classifiateur sont utilisés pour déduire la qualité, mais l'objectif principal de la formation est la prédiction du prochain jeton avec l'obligation des enseignants. Publié dans Nature. Cette leçon explique pourquoi un meilleur tokenizer plus l'échelle est tout ce dont vous avez besoin et contraste avec les approches de diffusion.

> **【中文解读】**Emu3(BAAI,2024年9月) avec un seul jeton de retour en arrière 预测目标, dans l'entraînement de la formation de texte unifié + image + vidéo, sur la génération d'images, a battu SDXL, sur la compréhension visuelle, a battu LLaVA-1.6── sans CLIP 损失, pas de régulation de propagation, le but de l'entraînement de base est le jeton suivant 预测── publié sur Nature 上──

> **【拓展：自回归 vs 扩散的争论】**La contribution centrale de l'Emu3 est conceptuelle: si le signe suivant 预测能在图像生成上匹敌扩散模型, alors le modèle unifié (un perte, un os干, un modèle quelconque) est réalisable.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Je suis en train de faire une étude sur la façon dont les gens peuvent apprendre à utiliser les symboles de la vie.
>  **【类比】**扩散模型 vs Emu3 = "画油画" vs "拼乐高"。扩散 = 从噪音开始一步精修(连续去噪音),每步都重新画整张图;Emu3 = 一个标记 往下拼拼;;离散乐高块),按顺序拼出图片──乐高看粗,但块足够小+种类足多时也能拼出逼真画面,而且和文本生成同一套机制(都是下一个标语)。
> 🤔 **【困惑】**Q: 既然 Emu3 est si fort, pourquoi la diffusion stable est-elle toujours dominante ?  推理成本! diffusion modèle 50 étapes de bruit est capable de sortir, Emu3 auto-retour doit générer sur mille jetons 才能出图, lent 20 fois  生成质量 Emu3 接近 SDXL 但推理慢,所以生产仍然偏爱扩散── 推理成本!

## Objectifs d'apprentissage

- Expliquez pourquoi l'objectif de jeton suivant à perte unique d'Emu3 fonctionne malgré l'hypothèse de longue date selon laquelle la diffusion est nécessaire pour la qualité de l'image.
  > Expliquer pourquoi Emu3 单一损失的下一代币 目标在长期假设"图像生成必须扩散"的情况下, il est toujours valable.
- Décrivez le tokenizer vidéo 3D: à quoi ressemble un codebook VQ spatiotemporal, pourquoi les correctifs durent plus longtemps.
  > 描述 3D 视频分词器:时空 VQ 码本长什么样、为什么补丁 要跨时间维度──
- Comparer Emu3 vs Stable Diffusion XL sur (computation de formation, coût d'inférence, plafond de qualité).
  > Comparer les émissions ému 3 à la diffusion stable XL en termes de différence de capacité d'entraînement, de coût et de qualité.
- Nommez les trois rôles que jouent le même modèle Emu3: Emu3-Gen (génération d'image), Emu3-Chat (perception), Emu3-Stage2 (génération vidéo).
  > 列举同一 Emu3 模型扮演的三种角色:Emu3-Gen(图像生成)、Emu3-Chat(感知)、Emu3-Stage2(视频生成)。

## Le problème , le contexte .

La sagesse conventionnelle jusqu'en 2024: la génération d'images a besoin de diffusion. L'argument: les jetons d'image discrets perdent trop d'informations pour reconstruire les détails, et le prélèvement autorégressif accumule des erreurs sur des milliers de jetons. Diffusion stable, DALL-E 3, Imagen, Midjourney utilisent toutes une forme de diffusion. Le Chameleon (Létion 12.11) a partiellement refusé cette proposition à petite échelle, mais n'a pas été de qualité comparable à celle de la SDXL.

> Le point de consensus de 2024: la génération d'images doit être générée. Le point de résultat est: le jeton d'image est dispersé.

Emu3 attaque l'argument face à face. L'affirmation: meilleur jeton visuel + assez d'échelle + perte de jeton suivante = génération d'image batant la diffusion dans le même modèle qui fait également la perception.

> Emu3 正面攻击这个论点──声称: Better视觉分词器 + 足够的规模 + 下一代币 损失 = Génération d'images qui se propagent au-delà du même modèle, tout en étant capable de faire sensation──

Deux ans plus tard, la famille de génération unifiée open source (Emu3, Show-o, Janus-Pro, Transfusion) est la voie par défaut pour la recherche; les modèles de frontière de production semblent utiliser une variante.

> Cette étude a été publiée avec un débat. Deux ans plus tard, elle est devenue un moyen de recherche standard.

## Le concept de base.

> **【中文解读】**EMU3 Utilisation pure auto-retour Next token  prédiction unifié multi-modèles compréhension et génération。 image est dispersée en token  séquence après, modèle comme prédiction texte comme prédiction Next visual token。

> **【拓展：自回归图像生成的挑战】**La méthode de pur auto-retour de l'EMU3 est encore en retard sur le modèle de diffusion en matière de génération d'images, car la longueur du jeton visuel dépend plus de la texture que de la texture.


### Le jeton ému3

L'ingrédient clé est le jeton visuel. Emu3 entraîne un jeton personnalisé de classe IBQ (Quantizer de couteau inverse, famille SBER-MoVQGAN) à 8x8 de réduction de résolution par jeton. Une image 512x512 devient 64x64 = 4096 jetons à la taille du codebook 32768.

> 关键成分是视觉分词器──Emu3 训练了自定义 IBQ 类分词器(逆瓶量化器,SBER-MoVQGAN 家族), chaque jeton 8x8 分辨率缩减──一张 512x512 图像变成64x64 = 4096 个 jeton,码本大小 32768──

Il est plus grand que les 1024 jetons de Chameleon par 512x512 à K=8192 mais moins cher par jeton (les recherches de codebook plus petites, codec plus simple).

> Ceci par rapport à Chameleon 512x512 图像 1024 个标志(K=8192) Plus grand, mais chaque token plus abordable(更小的码本查找、更简单的编解码器)  Indicateur clé: reconstruire PSNR à 30,5 dB, avec un répertoire de 32 dB de diffusion stable 竞争──

Pour la vidéo: un tokenizer VQ 3D encode un patch spatiotemporal (4x4x4 pixels) à un nombre entier. Un clip 4s à 8 FPS a 32 images; à 256x256 avec une réduction spatiale 4x et temporelle 4x, le nombre de jetons est (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32 768 jetons.

> Pour le vidéo: 3D VQ 分词器将时空补丁(4x4x4 像素) Codifier pour un nombre entier──4 秒片段在 8 FPS 下有 32 ;256x256 分辨率下 4x 空间和 4x 时间缩减,代码数字为 32768──

La qualité du tokenizer est le plafond.

> La qualité des mots est la limite. La contribution de l'ému3 réside dans le fait que nous avons entraîné un très bon mot.

### Formation à perte unique

Emu3 utilise un objectif: prévoir le prochain jeton sur un vocabulaire partagé entre des jetons de texte, des jetons d'image 2D et des jetons vidéo 3D. Les poids sont multipliés par des facteurs spécifiques à la modalité pendant la formation pour équilibrer la contribution, mais la fonction de perte est identique.

> Emu3 Utiliser un objectif: dans le tableau de référence des mots: prédiction, couvrant les symboles de texte, 2D, image et 3D, vidéo.

Le train est composé de:
- Genre d'image: `<text caption> <image> image_tokens </image>`
  Néo-latin: image génération
- Perception de l'image: `<image> image_tokens </image> <question> text_tokens`
  Le mot " image " est traduit par " image "
- Gen vidéo: `<text caption> <video> video_tokens </video>`
  Le film est sorti en français.
- Perception vidéo: analogue.
  Le film est aussi connu sous le nom de "Show Me".
- Seul texte: NTP standard.
  Le mot grec traduit par " prédestination " est traduit par " prédestination ".

Le modèle apprend à quel moment émettre des jetons d'image par rapport aux jetons de texte à partir de la distribution des données.`<image>`Je vous en prie.

> 模型从数据分布中学习何时输出图像代币与文本代币―― capacité de génération du modèle `<image>`标签后预测 Token d'image

### Guidance et température sans classifiant

La génération d'images autorégressives est beaucoup mieux avec la diffusion sans classifiateur (CFG) à l'inférence. Emu3 l'utilise: générer deux fois, une fois avec la légende complète, une fois avec une légende vide, mélanger les logits avec un poids de guidage (typique 3.0-7.0).

> L'utilisation de l'image de récupération est plus efficace. Elle est utilisée pour la production de données, la production de données et la production de données.

La température est importante: trop haute, les artefacts; trop bas, l'effondrement du mode.

> La température est importante: trop haute va avoir une image de l'image; trop bas va entraîner un effondrement du modèle.

### Trois rôles, un modèle

Les navires Emu3 sont constitués de trois API fonctionnellement distinctes mais d'un ensemble de poids sous-jacent:

> Emu3 以三个 fonctionnalités différentes API 发货, mais utiliser le même ensemble de poids:

- Génération d'images, texte d'entrée, jetons d'image de sortie.
  En anglais, le mot "Emu3" est traduit par "Emu3 Gen―图像生成―输入文本,输出图像代号―".
- Emu3-Chat. VQA et sous-titres. image d'entrée (tokens), texte de sortie.
  En anglais, le mot "conférence" est traduit par "conférence".
- Emu3-Stage2. génération vidéo et vidéo VQA. Entrée de texte ou vidéo, sortie de texte ou vidéo.
  Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française: Étude de la langue française

Pas de tête spécifique, juste des modèles de commande différents, le même point de contrôle.

> Il n'y a pas de tâche spécifique. Il y a juste un seul point de contrôle.

### Les points de référence

Dans le document Emu3 (septembre 2024):

> Il est également possible de faire une demande de règlement de la situation.

- Génération d'images: dépasse SDXL sur MJHQ-30K FID (5.4 vs 5.6), GenEval dans son ensemble (0.54 vs 0.55  égale statistique), et le composite de Deep-Eval sur par.
  Le groupe de travail de la société de l'information a été créé en 2004 pour la création de l'équipe de recherche de l'information.
- Perception d'image: dépasse le LLaVA-1.6 sur VQAv2 (75.1 contre 72.4) et correspond approximativement à MMMU.
  Le premier épisode de la série est un film de cinéma.
- Génération vidéo: qualité de vidéo de 4 secondes à FVD compétitive avec des modèles de l'ère Sora publiquement comparés.
  Le modèle de compétition de l'époque de Sora est équivalent à celui de l'époque de Sora.

Les chiffres ne gagnent pas toujours  Emu3 négocie un point ici pour un point là  mais l'affirmation "la prédiction du prochain jeton est tout ce dont vous avez besoin" est défendable dans toutes les modalités.

> Le nombre n'est pas toujours gagnant. Il est toujours possible de se tenir debout sur un point pour changer un autre.

### Coût de calcul

Emu3 a été formé sur ~300 milliards de jetons multimodals avec un modèle de paramètre 7B. Les heures de GPU sont à peu près comparables à la pré-entraînement Llama-2-7B (2k-4k GPU-années sur le silicium de classe A100).

> Emu3 est utilisé pour la formation de modèles paramétriques de 70 milliards de tokens. Le nombre de GPU est égal à celui de Llama-2-7B.

En inférence, Emu3 est plus lent que SDXL par image: 4096 jetons d'image à 30 tok/s est ~ 2 minutes par image 512x512 , contre 2-5 secondes pour SDXL. Le décoding spéculatif et l'optimisation de cache KV réduisent l'écart mais ne le ferment pas.

> 推理时,Emu3 张图像比SDXL 慢:4096 个图像代币 以 30 tok/s 生成,每张 512x512 图像约2分钟,而SDXL只需2-5秒――投机解码和KV 缓存优化缩小了差距但没有关闭它――自归图像生成计算密度;这是持续存在的权衡――

### Pourquoi cela importe ?

Si la prédiction de la prochaine jeton s'adapte à la diffusion sur la génération d'images, le chemin du modèle unifié (une perte, une colonne vertébrale, n'importe quelle modalité) est viable.

> Si le prochain jeton  prédiction peut s'étendre à une propagation correspondante sur la génération d'images, le chemin du modèle unifié                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

Show-o, Janus-Pro et InternVL-U s'appuient tous sur cette thèse ou la défient.

> Show-o、Janus-Pro 和 InternVL-U sont construits sur ce thème ou l'ont défié.


> **【拓展：EMU3 的统一训练策略】**La contribution centrale de l'UEM3 est de démontrer que la méthode de pur auto-réintégration peut être réalisée et produite en même temps.


## Utilisez-le en pratique
```figure
l5-emu3-next-token
```

## Utilisez-le

`code/main.py`construit deux jouets:

> `code/main.py`Il a construit deux composants de jouets:

- Un calculateur de compte de jetons VQ 2D vs 3D: donné (résolution, patch, clip_length, FPS), compte de jetons de calcul pour image vs vidéo.
  Le nombre de symboles de l'image et du vidéo est calculé en 2D et en 3D.
- Un échantillonneur autorégressif à jeton d'image avec une orientation sans classifiant à température.
  Le code de la température et de l'image de l'image

La mise en œuvre du CFG correspond à la recette de l'EMU3  mélangez des logits conditionnels et inconditionnels avec un poids de référence.

> Le CFG réalise le programme de correspondance Emu3 avec des logiques de gestion des conditions et des loges inconditionnelles.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-token-gen-cost-analyzer.md`. Compte tenu de la spécificité du produit de génération (image ou vidéo, résolution cible, niveau de qualité, budget de latence), il calcule le nombre de jetons, le coût d'inférence et choisit Emu3-famille par rapport à diffusion.

> 本课产 出 `outputs/skill-token-gen-cost-analyzer.md` Donnée spécification de produit (image ou vidéo  objectif de résolution  qualité et niveau  retard budgétaire), elle calcule le nombre de symboles  coûts de calcul et choisit entre la série Emu3 et le modèle de diffusion 

## Les exercices

1. Emu3 produit 4096 jetons par image 512x512 à une réduction de 8x8. Compute l'équivalent pour 1024x1024 et 2048x2048.
   En anglais, le nombre de symboles est de 512 à 512 .

2. Lisez la section 3.3 de l'Emu3 sur le jeton vidéo. Décrivez la forme du patch VQ 3D et pourquoi il est 4x4x4 et non 8x8x1.
   Le texte de la première partie de la série est le même que celui de la première partie de la série.

3. Le poids de la direction sans classifiant 5.0 contre 3.0: quel effet visuel ?`code/main.py`- Je suis désolé .
   Le modèle de l'image est le modèle de l'image.`code/main.py`Le milieu des mathématiques

4. Comptez les FLOP de formation pour les Emu3-7B à 300B et comparez-les à la Diffusion Stable 3.
   Comptez Emu3-7B en 300B jeton FLOPs de formation,并与稳定扩散3比较──哪个训练更贵?

5. L'Emu3 est supérieur à SDXL sur FID mais pas sur VQAv2 par rapport aux VLM spécialisés.
   En français, le système de gestion de la situation est un système de gestion de la situation de la situation de la population.

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Encore une lecture

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  Le signe de la prédiction est tout ce dont vous avez besoin.
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  En français, le mot " formation " est traduit par " formation ".
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  Le texte de l'article est le suivant:
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  Le mot de passe est le mot de passe de la langue française.
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  Le modèle de la vie est le modèle de la vie.
