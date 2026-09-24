# StyleGAN  StyleGAN  风格生成对抗网络

> La plupart des générateurs se déplacent .`z`StyleGAN le partage: première carte`z`à un intermédiaire `w`, puis * injecter *`w`Ce changement unique a démêlé l'espace latent et fait des visages photoréalistes un problème résolu pendant sept ans consécutifs.

> **【中文解读】**StyleGAN va concevoir des variables z avant de les cartographier dans l'espace intermédiaire w, puis, à travers AdaIN, à chaque niveau de résolution, injecter w, réaliser un contrôle indépendant sur la production d'images à différents niveaux de graisse (graisse/graisse) ⋅ ce changement a ouvert l'espace caché, rendant la production de faces réelles un problème résolu depuis sept ans.

> **【拓展：StyleGAN 的应用】**StyleGAN  largement utilisé pour la création de personnages (thispersondoesnotexist.com) 、虚拟人物创建、艺术创作──其 技术

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## Le problème , l' introduction du problème

Une carte DCGAN `z`Le problème:`z`Il contrôle tout  pose, éclairage, identité, arrière-plan  entrelacés.`z`Vous ne pouvez pas demander au modèle "la même personne, une pose différente" parce que la représentation ne fait pas de facteur de cette façon.

> DCGAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`映射为图像── le problème est:`z`Il y a aussi le contrôle de tout.`z`Vous ne pouvez pas exiger un modèle "le même homme, une posture différente", parce que le message ne se décompose pas de cette façon.

Karras et coll. (2019, NVIDIA) proposé: arrêter l'alimentation `z`- Envoyez une constante.`4×4×512`Apprenez à utiliser un MLP à 8 couches qui cartographient`z ∈ Z → w ∈ W`- Injecter`w`à chaque résolution via * normalisation d'instance adaptative* (AdaIN): normaliser chaque carte de caractéristiques conv, puis élargir et déplacer par des projections affine de `w`. Ajouter le bruit par couche pour les détails stochastiques (pores de peau, fils de cheveux).

> Karras 等人(2019,NVIDIA) a présenté: arrêter将 `z`Envoyez directement dans le volume.`4×4×512`张量作为网络输入──学习一个8层 MLP将 `z ∈ Z → w ∈ W`◊ par * autoadaptation exemple de régulation * * AdaIN) en chaque résolution`w`◊ Ajouter chaque couche de bruit pour chaque section ◊毛孔、发丝)

Le résultat: `W`Il a des axes orthogonaux pour "style de haut niveau" (position, identité) vs "style fine" (éclairage, couleur). Vous pouvez échanger des styles entre deux images en utilisant l'image A `w`pour les niveaux de résolution basse et les images B `w`Cette édition déverrouillée, la stylisation interdomaine et toute la ligne de recherche "StyleGAN-inversion".

> 结果:`W`空间对"高级风格" (gestition, identité) et "精细风格" (光照,颜色)`w`Avec une couche à basse résolution, image B.`w`Il est utilisé à des niveaux de haute résolution pour échanger des styles.

> **【中文解读】**La première étape de la mise en place de StyleGAN est la mise en place de la technique de mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en place de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre

> **【拓展：StyleGAN 3 的平移等变性】**StyleGAN 2 produit des images avec un "tattoo adhesion" problème  caractéristiques  tels que le titre) va "adhérer" à une position de la image spécifique et non à la surface de l'objet.  StyleGAN 3  2021  La compréhension de ce problème est déterminée par le biais de signaux continuels, de sorte que les résultats de production sont égaux à la rotation et à la rotation .

## Le concept de base.

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, une MLP de 8 couches.`Z = N(0, I)^512`- Je suis là .`W`Il apprend une forme adaptée aux données.

> **映射网络。** `f: Z → W`, 8 étages de MLP`W`Il n'est pas obligé de prendre une forme adaptée à ses besoins.

**Synthesis network.**Commence par une constante apprise .`4×4×512`. Chaque bloc de résolution: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`- Les résolutions doubles: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**De l'apprentissage à la fréquence`4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声──分辨率翻倍:4 到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

où `y_scale`et `y_bias`proviennent de projections affine de `w`Normalement par carte de fonctionnalités, puis re-style. "Style" ici est la statistique de premier et deuxième ordre de la carte de fonctionnalités.

> Parmi eux `y_scale`et `y_bias`Je suis venu .`w`Le modèle de la projection est un modèle de la mise en œuvre de la conception de la structure de l'image.

**Per-layer noise.**Le bruit gaussien à canal unique est ajouté à chaque carte de fonctionnalités, mesuré par un facteur par canal appris.

> **每层噪声。**Le bruit de la seule voie est ajouté à chaque graphie caractéristique, en réduisant le facteur de passage par voie par voie appréciable.

**Truncation trick.**À l'inférence, échantillon `z`, calcul`w = mapping(z)`Alors ...`w' = ŵ + ψ·(w - ŵ)`où `ŵ`est la moyenne `w`sur de nombreux échantillons. `ψ < 1`La qualité est la plus importante de toutes les démo de StyleGAN.`ψ ≈ 0.7`- Je suis désolé .

> **截断技巧。**Il est temps de le faire.`w' = ŵ + ψ·(w - ŵ)`, parmi lesquels `ŵ`Oui `w`Dans plusieurs échantillons, la valeur moyenne est:`ψ < 1`À la fin de la série, les modèles de styleGAN ont été utilisés.`ψ ≈ 0.7`Il y a une autre.

## StyleGAN 1 → 2 → 3  StyleGAN  version développée

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

En 2026, StyleGAN3 reste la norme par défaut pour (a) le photoréalisme de domaine étroit à haute FPS, (b) l'adaptation de domaine à quelques coups (train sur un nouveau ensemble de données avec 100 images, cartographie de congé), (c) l'édition basée sur l'inversion (trouver les `w`qui reconstruit une photo réelle, puis édite cette photo `w`Pour le domaine ouvert text-to-image, ce n'est pas l'outil  diffusion est.

> Le styleGAN3 est toujours une option préconisée pour les scénarios suivants: a) un haut niveau de photos de champs étroits, b) un petit nombre de zones adaptées, c) un éditeur de champs ouverts n'est pas son outil, et le modèle de diffusion n'est pas le même.

## Construisez-le et mettez-le en œuvre.
```figure
gx-stylegan-mapping
```

## Faites-le

`code/main.py`Il implémentera un jouet "style-GAN lite" en 1-D: une MLP de cartographie, une fonction de synthèse qui prend un vecteur constant appris et le module avec `w`- des préjugés de l'échelle et du bruit par couche.`w`par correspondance ou par battements concatenant`z`dans l'entrée du générateur.

> `code/main.py`Dans la 1D, une "StyleGAN lite" est réalisée: MLP de cartographie, fonction synthétique et bruit de chaque couche.`w`Avec le directeur`z`拼接到输入相比效果相当或更好──

### Étape 1: réseau de cartographie

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Étape 2: normalisation de l'instance adaptative

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

L'échelle et le biais des cartes de fonctionnalités proviennent de `w`par projection linéaire.

>                                                                                                                                                                                                                                                               `w`Le projet de la ligne

### Étape 3: bruit par couche

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma par canal est appréciable.

> Chaque chemin de sigma est à apprendre.

## Les pièges sont des pièges.

- **Droplet artifacts.**StyleGAN 1 a produit une goutte de flou dans les cartes fonctionnalités parce que AdaIN a réduit à zéro la moyenne.
  **液滴伪影。**StyleGAN 1 因 AdaIN 归零均值产生液滴──StyleGAN 2 的权重解调通过缩放卷积权重修复──
- **Texture sticking.**Les textures StyleGAN 1 et 2 suivaient les coordonnées de pixel, pas les coordonnées d'objet (visibles lors de l'interpolation).
  **纹理粘附。**La structure de StyleGAN 1/2 suit le schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma du schéma.
- **Mode coverage.**La découpe`ψ < 0.7`est propre mais des échantillons d' un cône étroit; utilisation `ψ = 1.0`Si vous avez besoin de diversité.
  **模式覆盖。**- Je suis en train de le faire .`ψ < 0.7`Il semble propre mais à partir de la taille étroite; nécessite une grande variété de temps d'utilisation.`ψ = 1.0`Il y a une autre.
- **Inversion is lossy.**Inverter une photo réelle dans `W`Les résultats dérivent sur de nombreuses itérations.
  **反演有损。**Pour faire une photo réelle .`W`Généralement, en utilisant l'optimisation ou le codeur, le résultat se déplace à plusieurs reprises.

## Utilisez-le avec le cadre de réalisation

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

Pour les démos de qualité produit où la réponse est "photo du visage d'une personne", StyleGAN dépasse la diffusion sur le coût d'inférence (pass avant unique, <10ms sur un 4090) et la netteté pour la même barre de qualité.

> Pour les produits de la catégorie "personnes face photos", StyleGAN en raison du coût de diffusion, 4090 à <10 ms) et de la même qualité.

## Envoyez-le . Produit .

- Ça va .`outputs/skill-stylegan-inversion.md`. Les compétences prennent une photo réelle et les résultats: méthode d'inversion (e4e / ReStyle / HyperStyle), perte latente attendue, budget d'édition (combien de temps dans `W`Vous pouvez vous déplacer avant les objets), et une liste de bonnes directions d'édition connues (âge, expression, pose).

> 保存 `outputs/skill-stylegan-inversion.md`◊Skill Recevoir des photos réelles, faire des émissions de films, prévoir des pertes potentielles, éditer un budget et connaître des directions éditoriales―

## Les exercices

1. **Easy / 简单.**On court .`code/main.py`avec `adain_on=True`et `adain_on=False`Comparer la propagation des sorties pour un latent fixe versus un latent perturbé.
   Pour moi .`adain_on=True`et `adain_on=False`运行―― comparer la distribution des flux de change fixe et des flux de change perturbateur―
2. **Medium / 中等.**Implémentation de la régulation des mélanges: pour un lot de formation, calcul `w_a`- Je suis là .`w_b`, et s' appliquer `w_a`pour la première moitié de la synthèse et `w_b`Le décodeur apprend-il les styles démêlés ?
   实现混合正则化──解码器 Ĉu学到了解的风格?
3. **Hard / 困难.**Prenez un modèle de styleGAN3 FFHQ prétrainé (ffhq-1024.pkl).`w`Direction qui contrôle le "sourire" en formant un SVM sur des échantillons étiquetés; indiquer jusqu'où vous pouvez aller avant que les dérives d'identité.
   Utiliser le styleGAN3 FFHQ 模型, par le biais de SVM 找到控制"微笑"的`w`La direction

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Note de production: pourquoi StyleGAN est toujours expédié en 2026

StyleGAN3 sur un 4090 génère un visage de 10242 FFHQ en moins de 10 ms  `num_steps = 1`En termes de production, c'est la latence de sol pour tout générateur d'image. Un pipeline de décode SDXL + VAE de 50 étapes à la même résolution est d'environ 3 secondes.**300× gap**, et pour les produits de domaine étroit (services d'avatar, lignes de documents d'identification, génération de stock face) il gagne sur TCO.

> StyleGAN3 en 4090 en moins de 10ms`num_steps = 1`, sans VAE, sans interruption attention.**300 倍差距**, sur les produits de zones restreintes, les TCO sont gagnants.

Deux conséquences opérationnelles:

> 两个运营后果:

- **No scheduler, no batcher.**Le lot statique à l'occupation cible est optimal. Le lotage continu (essentiel pour les LLM et la diffusion) offre un bénéfice nul car chaque demande reçoit les mêmes FLOP.
  **无需调度器或批处理器。**La répartition des coûts de production et de production est un facteur important pour la gestion des coûts de production et de production.
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`Les échantillons de la couche de l'échantillon sont obtenus à partir d'un cône étroit de la plage du réseau de cartographie.`ψ`à la charge maximale, le lever pour les utilisateurs premium.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`De la carte réseau de la portée étroite. C'est le seul niveau de différence entre le niveau de service de contrôle.`ψ`, les utilisateurs supérieurs sont améliorés.

## Encore une lecture

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) inversion e4e.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273) StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) Récipitatif minimal moderne de GAN.
