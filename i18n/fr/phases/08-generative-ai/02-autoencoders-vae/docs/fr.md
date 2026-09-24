# Auto-encoders et variations Auto-encoders (VAE) ➡ Autencoders et modifiés Autencoders

> Un simple autoencodeur comprime puis reconstruit. Il mémore. Il ne génère pas. Ajoutez une astuce  forcez le code à regarder Gaussian  et vous obtenez un échantillonneur. Cette astuce unique, la réparamétrisation de `z = mu + sigma * epsilon`C'est pourquoi chaque modèle d'image de diffusion latente et de correspondance de flux que vous utilisez en 2026 a un VAE à l'entrée.

> **【中文解读】**Ordinary auto-coding comprimé reconstruction, juste mémoire, ne peut pas générer.`z = mu + sigma * epsilon`La capacité de traverser le processus est la clé de l'entraînement.

> **【拓展：VAE 是 Stable Diffusion 的基石】**En 2026, tous les modèles de diffusion potentielles seront mis en œuvre dans le cadre de la diffusion stable.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

Comprimez un chiffre MNIST de 784 pixels à un code à 16 chiffres, puis reconstruisez. Un autoencodeur simple fera une reconstruction MSE mais l'espace code est un gâchis. Choisissez un point aléatoire dans l'espace code, décodez-le, et vous obtenez du bruit. Il n'a pas de échantillonneur. C'est un modèle de compression habillé.

> Pour réduire le nombre de MNIST à 784 像素, il faut réduire le nombre de 16 chiffres. Le code est reconstitué.

Ce que vous voulez vraiment, c'est: (a) l'espace de code est une distribution propre et lisse que vous pouvez échantillonner à partir d'un Gaussian isotrope`N(0, I)`Le codeur et le décodeur comprennent toujours bien. Trois objectifs, une architecture, une perte.

> Ce que vous voulez vraiment, c'est: a) le code spatial est propre, lisse, réalisable, distribué comme dans les différents pays.`N(0, I)`• b) Le code est toujours bien comprimé, un modèle est perdu, un modèle est perdu.

Le VAE 2013 de Kingma résout cette question en formant le codeur à produire une *distribution* `q(z|x) = N(μ(x), σ(x)²)`, tirant cette distribution vers le prior`N(0, I)`par une pénalité KL, puis le prélèvement `z`de `q(z|x)`Avant de décoder, au moment de l'inférence, laissez tomber le codeur, échantillon `z ~ N(0, I)`La pénalité KL est ce qui oblige l'espace de code à être structuré.

> Kingma 2013 année VAE 通过训练编码器输出*分布* `q(z|x) = N(μ(x), σ(x)²)`Pour résoudre ce problème, la punition sera distribuée à travers la KL.`N(0, I)`Puis de là .`q(z|x)`Dans le même ordre d'idées`z`Je me suis débarrassé de mon ordinateur.`N(0, I)`采样 `z`,解码──KL 惩罚正是使编码空间结构化的关键──

En 2026, les VAE sont rarement livrés indépendamment  ils ont été dépassés par la diffusion pour la qualité d'image brute  mais ils sont le codeur de choix pour chaque modèle de diffusion latente (SD 1/2/XL/3, Flux, AudioCraft).

> En 2026, très peu de VAE  Very few Independent Deployment  ont été étendues par des modèles sur la qualité d'image originale au-delà  mais c'est le premier éditeur de choix de tous les modèles potentiels de diffusion SD 1/2/XL/3、Flux、AudioCraft]].

> **【中文解读】**Le concept de base de la VAE: faire en sorte que le codeur soit distribué et non pointé.`z = mu + sigma * epsilon`L'utilisation de la norme est relativement simple. L'utilisation de la norme est relativement simple.

> **【拓展：beta-VAE 与解耦表示学习】**beta-VAE(2017) par réglage de la régulation de la régulation des paramètres de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation de la régulation

## Le concept de base.

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`- Je suis là .`x̂ = decoder(z)`, perte = `||x - x̂||²`- L'espace de code est non structuré.

> **自编码器。** `z = encoder(x)`- Je suis désolé .`x̂ = decoder(z)`, perte = `||x - x̂||²`◊编码空间无结构──

**VAE encoder.**Les sorties sont de deux vecteurs: `μ(x)`et `log σ²(x)`- Ils définissent ...`q(z|x) = N(μ, diag(σ²))`- Je suis désolé .

> **VAE 编码器。**输出 deux émetteurs:`μ(x)`et `log σ²(x)`Ils ont défini.`q(z|x) = N(μ, diag(σ²))`Il y a une autre.

**Reparameterization trick.**Prise d' échantillons à partir de `q(z|x)`L'échantillon est réécrit comme `z = μ + σ·ε`où `ε ~ N(0, I)`- Maintenant .`z`est une fonction déterministe de `(μ, σ)`+ un bruit non paramétrique  des gradients circulent `μ`et `σ`- Je suis désolé .

> **重参数化技巧。**De `q(z|x)`采样不可微──将采样重写为 `z = μ + σ·ε`, parmi lesquels `ε ~ N(0, I)`Je suis là.`z`Oui `(μ, σ)`La fonction de détermination plus le bruit non paramétrique`μ`et `σ`Réaction à la propagation.

**Loss.**Les preuves de la base de la base (ELBO), deux termes:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

La reconstruction est en train de pousser `x̂`vers le`x`- KL pousse .`q(z|x)`Les données de base de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l

> Rétablissement de la perte de puissance`x̂`趋近 `x` L'action`q(z|x)`Le modèle de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de la formation de l'équipe de formation de l'équipe de la formation de formation de la région de l'équipe de formation de l'équipe de la région de formation de formation de l'équipe de formation de la région de formation de l'équipe de formation de la région de la région de la région de la région de la région de la région de l'équipe de formation de formation de la région de la région de la région de la région de la région de la région de la région de la région de la région de la région de la région de la région de développement de la région de la région de développement de développement de la région

**Sampling.**À l' inférence: tirage au sort `z ~ N(0, I)`Un passage en avant, pas d'échantillonnage itératif comme la diffusion.

> **采样。**推理时: depuis `N(0, I)`- Je ne sais pas.`z`, envoyé dans le codeur avant de se propager.

> **【中文解读】**Les deux composantes de la perte d'ELBO sont différentes: la perte de reconstruction assure la qualité du code, la dispersion de KL assure la régularité du potentiel de l'espace. La conception ne nécessite pas complètement de codeur directement à partir de N(0,I) 采样 z 送进解码器──VAE 生成速度快(单次前向传播), mais la qualité de l'image est généralement plus floue que celle du modèle de diffusion, car elle est optimisée par ELBO 下界而非精确似──

> **【拓展：Stable Diffusion 中的 VAE】**La diffusion stable utilise la pré-entraînement de l'AEV qui réduira la compression de l'image à 64x64 de l'espace potentiel. Le processus de diffusion se déroule dans l'espace potentiel, réduisant considérablement la quantité de calcul.

## Construisez-le et mettez-le en œuvre.
```figure
vae-latent-grid
```

## Faites-le

`code/main.py`Il est utilisé pour la mise en œuvre d'un petit VAE sans numpy ou torche. L'entrée est des données synthétiques 8 dimensions tirées d'un mélange gaussien à 2 composants en 8D. L'encodeur et le décodeur sont des MLP à couche cachée unique.

> `code/main.py`L'entrée est une simple mise en œuvre de la méthode de production de données de 8 dimensions, qui ne dépend pas de la numérisation ou de la torche.

### Étape 1: encodeur vers l'avant

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`Au lieu de `σ`Ainsi, la sortie du réseau est libre (softplus de σ est un piège  gradients meurent à σ ≈ 0).

> Utilisation `log σ²`Il n'y a pas de`σ`Il est possible que la sortie du réseau soit sans restriction (l'écart de la ligne de sortie est un frein dans la ligne de sortie de la ligne de sortie).

### Étape 2: réparamétrifier et décoder

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Étape 3: l'ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

Il est vrai que les deux distributions sont gaussiennes, mais ne sont pas intégrées numériquement.

> 精确的闭式 KL,因为两个分布都是高斯的──不要数值积分──2026年还有人发布蒙特卡洛 KL 估计代码无端慢了3倍──

### Étape 4: générer

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

C'est le modèle génératif.

> C'est le mode de génération.

## Les pièges sont des pièges.

- **Posterior collapse.**Les lecteurs à terme KL `q(z|x) → N(0, I)`si agressivement que `z`ne contient aucune information sur `x`. Réparation: β-annulation (début β=0, rampe à 1), bits libres, ou sauter le KL sur les dimensions inactives.
  **后验坍塌。**KL est si fort que le monde va être`q(z|x)`- Je suis en train de le faire .`N(0, I)`, à cause de`z`Je ne sais pas`x`Les données sont à l'origine de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré
- **Blurry samples.**La probabilité du décodeur gaussien implique la reconstruction de l'ESM, qui est Bayes-optimale pour L2 (la moyenne)  la moyenne d'un ensemble de chiffres plausibles est un chiffre flou. Fix: décodeur discrète (VQ-VAE, NVAE), ou utiliser le VAE uniquement comme un encodeur et diffusion en pile sur les latents (c'est ce que fait Stable Diffusion).
  **模糊样本。**高斯解码器似然意味着 MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE), ou simplement utiliser VAE comme un codeur, sur une échelle de modèle de diffusion potentielle──
- **β too large, too early.**Voir l'effondrement postérieur.
  **β 太大太早。**见后验塌──从 β≈0.01 开始并逐渐增加──
- **Latent dim too small.**Le 16D fonctionne pour le MNIST, le 256-D pour l'ImageNet 2562, le 2048-D pour l'ImageNet 10242.
  **潜在维度太小。**MNIST avec 16 dimensions,ImageNet 2562 avec 256 dimensions.

## Utilisez-le avec le cadre de réalisation

Le groupe VAE 2026:

> 2026 années 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

Un modèle de diffusion latente est un modèle de diffusion VAE avec un modèle de diffusion vivant entre un encodeur et un décodeur. Le modèle de diffusion fait la compression grossière, le modèle de diffusion fait le travail lourd.

> Le modèle de propagation potentielle est entre le codeur et le codeur, le modèle de propagation est intégré à la VAE.

## Envoyez-le . Produit .

- Ça va .`outputs/skill-vae-trainer.md`- Je suis désolé .

> 保存 `outputs/skill-vae-trainer.md`Il y a une autre.

Les compétences requises: profil de l'ensemble de données + cible latente-dim + utilisation en aval (reconstruction, échantillonnage ou entrée de diffusion latente) et les résultats: choix d'architecture (plain/β/VQ/RVQ), horaire β, latente dim, probabilité de décoder (Gaussian vs catégorique), et plan d'évaluation (recon MSE, KL par dim, distance Fréchet entre `q(z|x)`et `N(0, I)`)

> Les compétences Reception: données collectives 概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(plain/β/VQ/RVQ) 、β 调度、潜在维度、解码器似然(高斯 vs 类别) 和评估计划──

## Les exercices

1. **Easy / 简单.**Le changement`β`dans `code/main.py`à `0.01`- Je suis là .`0.1`- Je suis là .`1.0`- Je suis là .`5.0`Enregistrer la reconstruction finale de MSE et KL. Quel β est le meilleur pareto pour vos données synthétiques ?
   Dans le`code/main.py`Le directeur`β`改为 `0.01`- Je suis là.`0.1`- Je suis là.`1.0`- Je suis là.`5.0` enregistrer la reconstruction finale de MSE et KL.
2. **Medium / 中等.**Remplacez la probabilité du décodeur gaussien par une probabilité de Bernoulli (perte de croisée entropie).
   Le codeur de haute valeur est remplacé par le codeur de haute valeur.
3. **Hard / 困难.**Extension `code/main.py`en mini VQ-VAE: remplacez le continu `z`Comparer la reconstruction MSE et indiquer le nombre d'entrées utilisées (l'effondrement du codebook est réel).
   Il va`code/main.py`扩展为迷你 VQ-VAE: avec K=32 的码本最近邻近查找替换连续 `z`◊ Comparer la reconstruction de l'ESM et le rapport ont utilisé plusieurs articles ◊

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Note de production: le VAE est le chemin le plus chaud dans un serveur de diffusion

Dans un pipeline Stable Diffusion / Flux / SD3, le VAE est appelé deux fois par demande  une fois pour encoder (si vous faites img2img / inpainting) et une fois pour décoder.`128×128×16`Les latents sont de retour à `1024×1024×3`- Deux conséquences pratiques:

> Dans la diffusion stable / flux / SD3 流水线, VAE chaque fois que la requête est régulièrement utilisée, une fois que le code est utilisé, une fois que le code est activé, dans la résolution 10242, le codeur est généralement le plus grand élément de la réserve maximale de l'ensemble du flux.

- **Slice or tile the decode.** `diffusers`exposés `pipe.vae.enable_slicing()`et `pipe.vae.enable_tiling()`- Le Tiling négocie un petit artefact de couture pour`O(tile²)`mémoire au lieu de `O(H·W)`- Essentiel pour 10242+ sur les GPU de consommation.
  **切片或分块解码。** `diffusers` fournisseur `enable_slicing()`et `enable_tiling()`分块以轻微接伪影换取 `O(tile²)`Je suis là.
- **bf16 decoder, fp32 numerics for the final resize.**Le SD 1.x VAE a été libéré en fp32 et *produit silencieusement des NaNs* lorsqu'il est jeté à fp16 à 10242+.`madebyollin/sdxl-vae-fp16-fix` préférer toujours la variante fp16-fix ou utiliser bf16.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在 fp16 下 10242+ 会静默产生 NaN──始终使用 fp16-fix 变体或 bf16──

## Encore une lecture

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) le papier de l'AEV.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) β-VAE démêlé.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) l'image de pointe de l'AEV.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Diffusion stable; VAE en tant qu'encodeur.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec, la norme audio VAE.
