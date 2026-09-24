# GAN conditionnel et Pix2Pix

> La première grande déblocage de 2014-2017 était de contrôler ce qu'une GAN fait. Attachez une étiquette, ou une image, ou une phrase. Pix2Pix a fait la version d'image et il bat toujours tous les modèles génériques texte-à-image sur les tâches étroites image-à-image.

> **【中文解读】**La première grande percée de 2014-2017 est de contrôler GAN.

> **【拓展：Pix2Pix 的应用】**Pix2Pix a créé le modèle "image to image translation": dessin→ photos、白天→ nuit、线稿→彩色图── ce modèle a été adopté par ControlNet.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

Un GAN inconditionnel échantillonne des visages arbitraires. Utilisés pour une démonstration, inutiles dans la production. Vous voulez: *mappage d'une esquisse à une photo*, *mappage d'une carte à une photo aérienne*, *mappage d'une scène de jour à la nuit*, *colorer une image à l'échelle de gris*. Dans toutes ces images, vous obtenez une image d'entrée`x`et doit sortir `y`Il y a beaucoup de choses plausibles.`y`- le`x`Une défaite adversaire ne le fait pas, car "il semble réel" est fort.

> 无条件 GAN 采样任意人脸──适合演示,不适合生产──你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜*、*给灰度图上色*──在所有这些场景中,给定输入图像`x`, doit produire des relations significatives à la résolution`y`Tout le monde.`x`Il y a beaucoup de raisons .`y` Les erreurs de la moyenne les réduiront en un groupe de morceaux, et la résistance ne perdra pas, car "il semble vrai" est rentable

Le GAN conditionnel (Mirza & Osindero, 2014) ajoute une condition `c`comme une entrée pour les deux `G`et `D`Pix2Pix (Isola et coll., 2017) a spécialisé ceci: condition est une image d'entrée complète, générateur est un U-Net, discriminateur est un classifiateur * patch-based* (PatchGAN), et perte est adversarial + L1. Cette recette surpasse les modèles de texte à image de zéro sur des domaines image à image étroits même en 2026 car elle est formée sur * données en paires *  vous avez exactement le signal dont vous avez besoin.

> 条件 GAN(2014) dans `G`et `D`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `c` Pix2Pix(2017) a spécialisé ce: condition est une image intégrale d'entrée, le générateur est U-Net, le déterminateur est PatchGAN, perte = opposition + L1♦. Ce programme est encore meilleur que le modèle de l'image de tête de l'exercice de 2026 dans les tâches de traduction d'images de domaine restreint, car il est en train de faire des signaux nécessaires à l'exercice de l'exercice de la formation.

> **【中文解读】**条件 GAN's core improvement: donne à un générateur et à un générateur de données tous les conditions d'entrée c⋅Pix2Pix's condition est une image d'entrée complète, générateur U-Net (Retaint Space Details), générateur de données avec PatchGAN (Retaint Space Details), générateur de données avec un graphique local (L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L1 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L L2 L2 L L L2 L2 L L L L L2 L L L L L L2 L2 L L L L2 L L L L L L L L L L L L L2 L L L L L L L L L L L L L2 L L L L L L L L L L L L2 L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**La conception de "génération des conditions d'image" de Pix2Pix est adoptée par ControlNet (en 2023) et développée. ControlNet va intégrer les conditions de contrôle dans le modèle de diffusion stable de pré-entraînement, permettant une génération contrôlée plus générale.

## Le concept de base.

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`Dans Pix2Pix,`z`est dérapagé à l'intérieur de G (aucun bruit d'entrée  Isola trouvé le bruit explicite a été ignoré).

> **条件生成器 G。** `G(x, z) → y`Dans Pix2Pix,`z`Il y a une absence de bruit de sortie de l'intérieur.

**Conditional D.** `D(x, y) → [0, 1]`. L'entrée est la paire (condition, sortie).`y`est compatible avec `x`, pas seulement si `y`Ça a l'air réel.

> **条件判别器 D。** `D(x, y) → [0, 1]`◊输入是*配对*(条件,输出)`y`      `x`Un coup, pas seulement`y`Si oui ou non, ça semble réel.

**U-Net generator.**Encoder-décoeur avec des connexions de saut à travers le goulet d'étranglement. Critical pour les tâches où l'entrée et la sortie partagent une structure de bas niveau (marges, silhouette). Sans les sauts, les détails à haute fréquence disparaissent.

> **U-Net 生成器。**带有跳跃连接的编码器-解码器── Pour les tâches de la structure de bas niveau de partage des sorties et des entrées, les tâches sont essentielles.

**PatchGAN discriminator.**Au lieu de produire un seul score réel/faux, D produit un `N×N`La moyenne est de 70×70 pixels. C'est une hypothèse de champ aléatoire de Markov: le réalisme est local.

> **PatchGAN 判别器。**D 输出 `N×N`网格而不是单一真/假分数, chaque unité juge environ 70×70 像素的感受野──这是马尔可夫随机场假设:真实感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

Le terme L1 stabilise l'entraînement et pousse G vers la cible connue. L1 donne des bords plus tranchants que L2 (médians, pas moyens). `λ = 100`était le Pix2Pix par défaut.

> L1 项稳定训练并推动 G 趋向已知目标──L1比L2 产生更利的边缘(中位数对平均值)──`λ = 100`C'est la valeur par défaut de Pix2Pix.

## CycleGAN quand vous n'avez pas de paires

Pix2Pix a besoin d' être couplé `(x, y)`Les données. CycleGAN (Zhu et coll., 2017) réduit cette exigence au prix d'une perte supplémentaire: la perte de la cohérence du cycle.`G: X → Y`et `F: Y → X`- Les entraîner ainsi .`F(G(x)) ≈ x`et `G(F(y)) ≈ y`Cela vous permet de traduire des chevaux en zèbres, en été en hiver, sans exemples parallèles.

> Pix2Pix 需要配对 `(x, y)`Les données de CycleGAN (en 2017) ont abandonné cette exigence, le prix étant une perte supplémentaire de cohérence de cycle.`G: X → Y`et `F: Y → X`, entraînement `F(G(x)) ≈ x`et `G(F(y)) ≈ y`Il vous permet de faire des échantillons sans avoir besoin de coupe pour que le cheval devienne un cheval de course, l'été un hiver.

En 2026, l'image-à-image non couplée est principalement réalisée via diffusion (ControlNet, IP-Adapter) plutôt que CycleGAN, mais l'idée de cohérence de cycle survit dans presque tous les documents d'adaptation de domaine non couplés.

> En 2026, la conception de l'image non coupée est terminée principalement par un modèle de diffusion (ControlNet、IP-Adapter) et non CycleGAN, mais l'idée de l'accord de cycle est presque présente dans tous les articles de l'adaptation de domaine non coupé.

## Construisez-le et mettez-le en œuvre.
```figure
gx-patchgan
```

## Faites-le

`code/main.py`Il met en œuvre une petite GAN conditionnelle sur les données 1D.`c`est une étiquette de classe (0 ou 1). La tâche: produire un échantillon à partir de la distribution conditionnelle pour la classe donnée.

> `code/main.py`Dans un dimension de données, réaliser une condition de type GAN.`c`C'est un type de modèle généré par une distribution de conditions.

### Étape 1: ajouter la condition aux entrées G et D

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

Le codage à un seul coup est le moyen le plus simple.

> Le code unique est le moyen le plus simple.

### Étape 2: train conditionné

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

Le générateur doit correspondre à la réelle distribution *pour la condition donnée*, et non à la marginale.

> Les appareils doivent correspondre à une répartition réelle dans des conditions déterminées, et non à une répartition marginelle.

### Étape 3: vérifier la sortie par classe

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## Les pièges sont des pièges.

- **Condition ignored.**G apprend à se marginaliser, D ne pénalise jamais parce que le signal de condition est faible.
  **条件被忽略。**G apprendre à se marginaliser, D de ne pas punir parce que les conditions sont faibles.
- **L1 weight too low.**G dérive vers des sorties réelles arbitraires, pas fidèles.
  **L1 权重太低。**G 偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**G produit des résultats flou parce que L1 est toujours une norme de L_p.
  **L1 权重太高。**G 产生模糊输出── entraînement stable après progressivement diminuer──
- **Ground-truth leakage in D.**Concaténate `(x, y)`comme entrée D, pas seulement `y`Sans ce D, on ne peut pas vérifier la cohérence.
  **D 中的真值泄漏。**Il va`(x, y)`拼接为 D 的输入,而非仅仅 `y`Il y a une autre.
- **Mode collapse per class.**Chaque classe peut s'effondrer indépendamment.
  **每类模式坍塌。**Chaque catégorie peut être indépendante.

## Utilisez-le avec le cadre de réalisation

2026 état des tâches image à image:

> 2026 année image à image mission de l'état:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix reste l'outil idéal lorsque (a) vous avez des milliers d'exemples en couple, (b) la tâche est étroite et répétable, et (c) vous avez besoin d'une inférence rapide.

> Pix2Pix est toujours correct dans les situations suivantes: a) il y a des milliers de modèles de parcours, b) les tâches sont étroites et récurrentes, c) il faut une rapidité de réflexion.

## Envoyez-le . Produit .

- Ça va .`outputs/skill-img2img-chooser.md`. Les compétences prennent une description de tâche, la disponibilité des données (parées contre non parées, échantillons N) et le budget de latence/qualité, puis les sorties: approche (Pix2Pix, CycleGAN, variante ControlNet, SDXL + IP-Adapter), exigences de données de formation, coût d'inférence et protocole d'évaluation (LPIPS, FID, spécifique à la tâche).

> 保存 `outputs/skill-img2img-chooser.md` Des compétences  Réception des tâches  Définition des tâches                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

## Les exercices

1. **Easy / 简单.**Modifier `code/main.py`Confirmer G maps toujours le bruit de chaque classe au bon mode.
   修改 `code/main.py`添加第三类. 确认 G 仍将每个类的噪音映射到正确模式.
2. **Medium / 中等.**Remplacez L1 par une perte de style perceptif dans le réglage 1-D (par exemple, un petit D gelé agissant comme extracteur de caractéristiques).
   Dans la configuration 1D, la perte de sensation est remplacée par L1.
3. **Hard / 困难.**Dessinez un CycleGAN dans le réglage 1D: deux distributions, deux générateurs, perte de cycle. Montrez qu'il apprend à cartographier entre eux sans données en couple.
   Dans le cadre de la mise en 1D, le CycleGAN: Deux distributions, deux générateurs, péril de cycle prouve qu'il n'est pas nécessaire de faire des analyses de données pour pouvoir apprendre à cartographier.

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Note de production: Pix2Pix comme une ligne de base liée à la latence

Lorsque vous avez associé des données et une tâche étroite (boutons → rendu, carte sémantique → photo, jour → nuit), l'inférence à un seul coup de Pix2Pix bat la diffusion d'un ordre de grandeur sur la latence.

> Lorsque vous avez des tâches de données et de domaine restreint, la seule hypothèse de Pix2Pix est de diffuser rapidement un modèle de diffusion au niveau quantitatif.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix gagne sur le débit en lots statiques (toute demande est la même FLOPs). Diffusion gagne sur la qualité et la généralisation. Le jeu moderne est souvent d'envoyer un modèle distillé de style Pix2Pix pour la tâche étroite et une rétroaction de diffusion pour les entrées de queue.

> Pix2Pix est généralement utilisé pour la déploiement de tâches de domaine restreint.

## Encore une lecture

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) le papier cGAN.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)- Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291)- Le coup de foudre.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) la projection D.
