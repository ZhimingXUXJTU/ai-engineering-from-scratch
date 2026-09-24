# GANs  Générateur contre discriminateur  GAN  Produire et déterminer

> Le truc de Goodfellow en 2014 était de sauter la densité entièrement. Deux réseaux. L'un fait des faux. L'autre les attrape. Ils se battent jusqu'à ce que les faux soient indistinguibles du vrai. Cela ne devrait pas fonctionner. Cela ne fonctionne souvent pas. Quand cela se produit, les échantillons sont toujours les plus acérés dans la littérature pour les domaines étroits.

> **【中文解读】**Les techniques de Goodfellow 2014 ont complètement surpassé les estimations de densité. Deux réseaux: un faux, un faux, se connaissent mutuellement jusqu'à ce que le faux échantillon soit indistinguible du vrai échantillon.

> **【拓展：GAN 的遗产】**StyleGAN (人脸生成) ‧CycleGAN (风格迁移) ‧Pix2Pix (图像翻译) ‧图像翻译) est une application classique de GAN. Bien que le modèle de diffusion de GAN soit devenu courant après 2022, l'idée de l'entraînement de la résistance de GAN est toujours utilisée pour améliorer la qualité des autres modèles.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

Les VAE produisent des échantillons flou parce que leur perte de décodeur MSE est Bayes-optimale pour l'image * moyenne *  et la moyenne de nombreux chiffres plausibles est un chiffre flou. Vous voulez une perte qui récompense * plausibilité*, pas la proximité pixel-wise à une cible. Il n'y a pas de forme fermée pour la plausibilité. Vous devez l'apprendre.

> La valeur moyenne de nombreux chiffres raisonnables est une valeur floue. Vous avez besoin d'une perte de réalisme, plutôt que de la proximité avec un objectif quelconque. La réalisme n'a pas de solution définitive, vous devez l'apprendre.

L'idée de Goodfellow: former un classifiateur `D(x)`Pour distinguer les images réelles des fausses.`G(z)`Pour faire la folie`D`- Le signal de perte pour`G`C' est quoi ?`D`Ce signal est mis à jour comme`G`Si les deux réseaux convergent,`G`a appris la distribution des données sans jamais écrire.`log p(x)`- Je suis désolé .

> L'idée du bon compagnon: entraîner un groupe de classe`D(x)`区分真假图像, entraînez un générateur `G(z)`Pour vous tromper .`D`Il y a une autre.`G`Le signal de perte est`D`On dirait que c'est vrai.`G`Les deux réseaux sont accueillis,`G`On apprend à distribuer les données sans avoir à écrire.`log p(x)`Il y a une autre.

C'est une formation à l'adversité.

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

En 2026, les GAN ne sont plus le générateur de SOTA (diffusion et flux de correspondance ont mangé cette couronne). Mais StyleGAN 2/3 reste les modèles de visage les plus acérés jamais expédiés, les discriminateurs GAN sont utilisés comme *persections perceptuelles* dans l'entraînement à la diffusion, et l'entraînement à l'adversité alimente les distillations rapides en 1 étape (SDXL-Turbo, SD3-Turbo, LCM) qui vous permettent d'expédition diffusion en temps réel.

> En 2026, GAN n'est plus le générateur le plus avancé de générateurs de diffusion et de flux de correspondance. Mais StyleGAN 2/3 est toujours le modèle de visage le plus rentable de l'histoire.

> **【中文解读】**Le concept central de la GAN est: non construire une densité, en utilisant l'apprentissage de la génération de l'image, générateur G(z) 尝试生成逼真图像,判别器 D(x) 尝试区分真假── les deux sont en évolution commune dans le minimum 博中── la perte de MSE de la VAE entraîne une confusion, car elle est optimisée par l'image moyenne, tandis que la récompense de la GAN pour la résistance à la perte de la "逼真度"──GAN produit une croissance rapide, mais l'apprentissage n'est pas stable──

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**Bien que GAN ne soit plus une méthode de production dominante, l'idée de l'apprentissage de l'anti-gestion dans le modèle de diffusion est mise à jour. Le modèle de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de l'anti-gestion de la qualité est plus efficace.

## Le concept de base.

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**Mape un vecteur de bruit `z ~ N(0, I)`à un échantillon `x̂`Un réseau en forme de décodeur (convecteur dense ou transposé).

> **生成器 `G(z)`。**Généralement, le bruit est élevé.`z ~ N(0, I)`映射为样本 `x̂`◊ Un réseau en forme de décodeur (full connection or transformation) ◊

**Discriminator `D(x)`.**Mape un échantillon à une probabilité (ou score) scalaire.

> **判别器 `D(x)`。**À propos de la réaction de la société de l'information

**Loss.**Deux mises à jour alternatives:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`- Entropie binaire croisée sur réel = 1, faux = 0.
- **Train `G`:** `loss_G = -log D(G(z))`C'est la forme non saturante utilisée par Goodfellow (original)`log(1 - D(G(z)))`saturé et tue les gradients lorsque `D`est confiant).

> **损失。**两个交替更新: entraînement D 用二元交叉(真实=1,伪造=0); entraînement G 用非和形式 `-log D(G(z))`(original formation dans D 自信时梯度 disparaître)

**Training loop.**Une étape de `D`, une étape de `G`Je répète.

> **训练循环。**Un pas D, un pas G, un pas en avant.

**Why it works.**Si vous`G`Il est parfait .`p_data`Alors ...`D`ne peut pas faire mieux que le hasard et les résultats sont 0,5 partout; `G`Il n'y a plus de gradient.

> **为什么有效。**Si `G`完美匹配 `p_data`, `D`Je ne peux pas mieux deviner que ça, j'ai une sortie de 0,5.`G`Il n'y a plus de degré.

**Why it breaks.**L'effondrement du mode (`G`trouve un mode `D`Je ne peux pas le classer et le mettre à mort pour toujours, le gradient disparaissant (`D`Il apprend trop vite et `log D`Les taux d'apprentissage, les tailles de lot, tout ce qui est nécessaire.

> **为什么会失败。**模式塌`G`找到 `D`Un modèle qui ne peut pas être classé et ne peut jamais être généré.`D`Je suis trop rapide pour ça.`log D`Le taux d'apprentissage est stable.

## Les variantes qui ont fait fonctionner les GAN sont devenues des variantes de succès de GAN.

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Construisez-le et mettez-le en œuvre.
```figure
gan-minimax
```

## Faites-le

`code/main.py`Le générateur et le discriminateur sont des MLP à couche cachée unique. Nous mettons en œuvre la boucle avant, arrière et minimax à la main. L'objectif est de voir les deux modes de défaillance clés (effondrement de mode + gradient de disparition) au fur et à mesure qu'ils se produisent.

> `code/main.py`En un niveau de données, l'entraînement d'un GAN de type micro:

### Étape 1: Perte non saturante

La perte de la vanille de Goodfellow .`log(1 - D(G(z)))`Le gradient de G est essentiellement zéro  G ne peut pas s'améliorer.`-log D(G(z))`Il est opposé à l'asymptote: il explose quand D est confiant, donnant à G un signal fort.

> Bon compagnon !`log(1 - D(G(z)))`Dans le D, la haute confiance sera de la catégorie de fausse classification de G à la fois tendance à 0, à cette époque la gradience de G est fondamentalement de zéro.`-log D(G(z))`Il y a un comportement de progression opposé: en D'auto-confiance, éclaircir G 强.

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Étape 2: une étape discriminatrice par étape génératrice

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

Des faux pour G, sinon les gradients sont obsolètes.

> Pour créer un nouveau faux échantillon, sinon la température est passée.

### Étape 3: surveillez l'effondrement du mode

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

Le symptôme canonique: l'un des deux modes réels cesse d'être généré. Le discriminateur cesse de le corriger parce qu'il n'est jamais vu comme faux.

> 典型症状: l'un des deux modes réels ne s'est plus produit.

## Les pièges sont des pièges.

- **Discriminator too strong.**Réduire le taux d'apprentissage de D de 2 à 5 fois, ou ajouter du bruit d'instance/couche. Si D atteint une précision de > 95%, G est mort.
  **判别器太强。**Si le taux d'apprentissage de D dépasse 95%, G mourra.
- **Generator memorizes a mode.**Ajouter du bruit aux entrées D, utiliser une couche de discrimination mini-batch ou passer à WGAN-GP.
  **生成器记住了一种模式。**给 D 输入添加噪音, utiliser un petit groupe de dispositifs de détermination, ou changer à WGAN-GP。
- **Batch norm leaking statistics.**Les statistiques sont mélangées par un vrai lot + un faux lot qui traverse la même couche BN.
  **批归一化泄漏统计量。**Les vrais lots et les faux lots sont mélangés par le même BN.
- **Inception-score gaming.**Les échantillons FID et IS sont bruyants à faible nombre d'échantillons.
  **Inception Score 作弊。**FID 和 IS dans un volume d'échantillons bas.
- **One-shot sampling is a lie for conditional tasks.**Vous avez encore besoin de balances CFG, de trucs de troncage et de re-échantillonnage pour obtenir des résultats utilisables.
  **条件任务中"单次采样"是个谎言。**Vous avez encore besoin de techniques de réduction et de retrait de CFG pour obtenir des sorties disponibles.

## Utilisez-le avec le cadre de réalisation

La pile de GAN 2026:

> 2026 années GAN 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

Les GAN sont nettes mais étroites. Une fois que votre domaine s'ouvre  photos, des textes arbitraires, des vidéos  passer à la diffusion.

> GAN 利但狭域──一旦领域开放照片、任意文本提示、视频就就转换到扩散模型──对抗技巧作为组件存活(感知损失、蒸),而不是独立生成器──

## Envoyez-le . Produit .

- Ça va .`outputs/skill-gan-debugger.md`. Skill prend une opération GAN défaillante (curves de perte, grille d'échantillon, taille de jeu de données) et produit une liste classée des causes probables, des corrections à une ligne et un protocole de répétition.

> 保存 `outputs/skill-gan-debugger.md`◊Skill Recevoir une GAN 运行 (损失曲线、样本网格、数据集大小),输出可能原因排列列表、一行修复和重跑方案──

## Les exercices

1. **Easy / 简单.**On court .`code/main.py`avec les paramètres de stock.`D_LR = 5 * G_LR`La perte de G s'effondre rapidement à une constante.
   Uzal默认设置运行 `code/main.py` puis mise en place `D_LR = 5 * G_LR`Les pertes de poids sont-elles constantes ?
2. **Medium / 中等.**Remplacez la perte de Goodfellow BCE par la perte de WGAN: `loss_D = E[D(fake)] - E[D(real)]`- Je suis là .`loss_G = -E[D(fake)]`, et de cliper les poids de D à `[-0.01, 0.01]`- L'entraînement est plus stable ?
   Pour remplacer les pertes de la BCE par les pertes du WGAN , coupez le poids de la D.`[-0.01, 0.01]`◊ entraînement plus stable?
3. **Hard / 困难.**Extension de l'exemple 1D à des données 2D (mixture de 8 Gaussians sur un anneau). Suivre combien des 8 modes le générateur capture aux étapes 1k, 5k, 10k. Implémenter la discrimination minibatch et re-mesure.
   Pour étendre l'exemple 1D à l'analyse 2D, le générateur de suivi a capturé des modèles en 1k,5k,10k à l'étape suivante.

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Note de production: une seule prise d'inconvénient est l'avantage durable de GAN

Les GAN ne gagnent plus sur la qualité des échantillons pour la génération de domaine ouvert, mais ils gagnent toujours sur le coût de l'inférence.

> GAN ne gagne plus sur la qualité des échantillons produits dans le domaine ouvert, mais sur le coût de la production, il gagne toujours.

- **No prefill, no decode stages.**Une seule .`G(z)`TTFT ≈ latence totale.
  **无 prefill，无 decode 阶段。**单次 `G(z)`Il est également possible de faire une déclaration de réception.
- **No KV-cache pressure.**La taille du lot est limitée par la mémoire d'activation, pas par le cache.
  **无 KV 缓存压力。**Le seul état est le poids. La taille du lot est limitée à l'activation du stockage et non au stockage.
- **Trivial continuous batching.**Comme chaque demande reçoit les mêmes FLOPs fixes, un lot statique à l'occupation cible du serveur est généralement optimal.
  **简单的连续批处理。**Chaque demande consomme les mêmes FLOP, la quantité statique est généralement la meilleure.

C'est pourquoi la distillation GAN (SDXL-Turbo, SD3-Turbo, ADD, LCM) est la technique dominante pour la transmission rapide de texte à image en 2026: elle effondre un pipeline de diffusion de 20 à 50 étapes en passages avant de 1 à 4 GAN tout en conservant la distribution d'une base de diffusion.

> C'est pourquoi le GAN 蒸(SDXL-Turbo、SD3-Turbo、LCM) est la principale technologie de 2026: elle se propage à 20 à 50 étapes en 1 à 4 fois le GAN 风格, tout en maintenant la distribution du modèle de diffusion.

## Encore une lecture

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) le papier original de la GAN.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434) la première architecture stable.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042) SDXL-Turbo.
