# Modèles de diffusion  DDPM à partir de zéro  Modèle de diffusion  DDPM à partir de zéro

> Ho, Jain, Abbeel (2020) a donné au champ une recette qu'il ne pouvait pas arrêter. Destruire les données avec du bruit sur mille petits pas. Formez un filet neuronal pour prédire le bruit. Inversez le processus à l'inférence. Aujourd'hui, chaque image, vidéo, 3D et modèle musical traditionnel fonctionne sur cette boucle, éventuellement avec des astuces de correspondance de flux ou de cohérence en haut.

> **【中文解读】**Le processus central du DDPM: avec 1000 étapes pour donner des données à la suppression du bruit, entraîner un réseau de prédiction du bruit, proposer des techniques de suppression du bruit.

> **【拓展：扩散模型是当前 AI 生成的核心】**La diffusion stable, DALL-E 3, Midjourney, Sora sont basées sur le modèle de diffusion, la DDPM prouve qu'un simple objectif de désinfection du bruit peut produire une capacité de production étonnante.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

Tu veux un échantillon pour `p_data(x)`Les GAN jouent un jeu de minimax qui diverge souvent. Les VAE produisent des échantillons flou à partir d'un décodeur gaussien. Ce que vous voulez vraiment, c'est un objectif d'entraînement qui est (a) une seule perte stable (pas de point de selle, pas de minimax), (b) une limite inférieure sur `log p(x)`(pour que vous ayez des probabilités), et (c) des échantillons correspondant à la qualité de la SOTA.

> Tu veux ?`p_data(x)`Le plus souvent, les échanges sont en cours, mais les échanges sont en cours.`log p(x)`Le niveau de qualité est de 0,5% à 0,5% en moyenne.

Sohl-Dickstein et coll. (2015) ont eu une réponse théorique: définir une chaîne Markov `q(x_t | x_{t-1})`qui ajoute progressivement le bruit gaussien, et entraîne une chaîne inverse`p_θ(x_{t-1} | x_t)`Ho, Jain, Abbeel (2020) ont montré que la perte pouvait être simplifiée à une ligne  prédire le bruit  et nettoyé les mathématiques. En 2020 c'était une curiosité. En 2021 il a produit des échantillons de pointe. En 2022 il est devenu Stable Diffusion. En 2026 il est le substrat.

> Sohl-Dickstein (2015) a donné la réponse théorique: définir progressivement la chaîne de marque de bruit accru, entraîner contre la chaîne de bruit. Ho 等人 (2020) va simplifier la perte en une ligne de bruit prédictif.

> **【中文解读】**Le processus de démarrage de la DDPM est de: 1) le processus de pré-démarrage progressif de la pré-réaction du bruit jusqu'à ce que les données deviennent du bruit pur; 2) l'entraînement de l'apprentissage d'un pré-réaction du réseau à chaque étape de l'ajout du bruit; 3) le processus de réaction progressive de la pré-réaction du bruit pur, de la récupération de données réelles.

> **【拓展：从 DDPM 到实用扩散模型】**DDPM Originaire Essays dans l'opération de l'espace de la taille, la vitesse lentement, la vitesse à laquelle elle doit être utilisée.

## Le concept de base.

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**Ajoutez le bruit gaussien `T`La forme fermée  la raison pour laquelle la mathématique est traitable  est que la mesure cumulée est également gaussienne:

> **前向过程 `q`。**Dans le`T`Les phases suivantes sont également les suivantes:

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

où `α̅_t = ∏_{s=1..t} (1 - β_s)`pour un calendrier de `β_t`- Je vous en prie .`β_t`de 1e-4 à 0,02 linéairement sur T=1000 étapes et `x_T`est approximativement `N(0, I)`- Je suis désolé .

> Parmi eux `α̅_t = ∏_{s=1..t} (1 - β_s)`Il y a des gens qui sont là.`β_t`De 1e-4 à 0,02 线性排列 T=1000 步,`x_T`Je suis là.`N(0, I)`Il y a une autre.

**Reverse process `p_θ`.**Apprenez à utiliser un réseau neuronal .`ε_θ(x_t, t)`qui prédit le bruit qui a été ajouté.`x_t`, désigne par:

> **反向过程 `p_θ`。**Apprendre à utiliser un réseau neurologique`ε_θ(x_t, t)`预测添加的噪音──给定 `x_t`, de façon bruyante pour:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

où `σ_t`est soit `sqrt(β_t)`L'expression est laide mais c'est juste l'algèbre`x_{t-1}`vu le retrait `q(x_{t-1} | x_t, x_0)`et en remplacement `x_0`avec son estimation prévue pour le bruit.

> Parmi eux `σ_t`Oui `sqrt(β_t)`Ou apprendre à faire différence. L'expression semble complexe mais c'est juste un nombre.`q(x_{t-1} | x_t, x_0)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `x_{t-1}`Il y a une autre.

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Pratique `x_0`à partir des données, choisissez un aléatoire `t`, échantillon `ε ~ N(0, I)`, calculer le bruit `x_t`Une perte, pas de minimax, pas de KL, pas de trucs de réparamétrisation.

> D'après les données`x_0`, à volonté`t`- Je suis un homme .`ε ~ N(0, I)`, par le biais de la fermeture d'une seule fois calcul contenant du bruit`x_t`, à la résistance au bruit, à la réaction.

**Sampling.**Commencez`x_T ~ N(0, I)`- Répétez l' étape inverse de `t = T`à `1`- C'est fait.

> **采样。**De `x_T ~ N(0, I)`开始, depuis `t = T`À la`1`代反向步骤──完成──

## Pourquoi ça marche ? Pourquoi ça marche ?

Trois intuitions:

> Je suis en train de vous dire:

1. **Denoising is easy; generating is hard.**À `t=T`Les données sont de bruit pur, le réseau doit résoudre un problème trivial.`t=0`Le réseau ne doit nettoyer que quelques pixels.`t`Le problème est difficile mais le filet a de nombreux gradients qui circulent à travers les mêmes poids à partir de chaque niveau de bruit.
   **去噪容易，生成难。**Dans le`t=T`时, données sont purement bruyantes 网络只需要解决简单的问题.`t=0`时, le réseau doit seulement nettoyer une petite quantité de images.

2. **Score matching in disguise.**Vincent (2011) a prouvé que prédire le bruit équivaut à estimer`∇_x log q(x_t | x_0)`Le SDE inverse utilise ce score pour monter le gradient de densité  une marche aléatoire guidée vers des régions à forte probabilité.
   **伪装的分数匹配。**预测 Le bruit est égal à la fonction de l'estimation`∇_x log q(x_t | x_0)`❖ L'utilisation de ce débit par rapport à la SDE à l'échelle de densité augmente ❖

3. **The ELBO reduces to simple MSE.**La limite inférieure variationnelle complète a un terme KL par étape temporelle. Avec la paramétrisation du DDPM, ces termes KL simplifient à MSE la prédiction du bruit avec des coefficients spécifiques; Ho a diminué les coefficients (appelant cela "perte simple") et la qualité *améliorée*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每个时间步骤都有 KL 项──何 抛弃系数后质量反而*提升*了──

## Construisez-le et mettez-le en œuvre.
```figure
diffusion-denoise
```

## Faites-le

`code/main.py`Le réseau est un petit MLP qui prend`(x_t, t)`Le train est la perte d'une ligne.

> `code/main.py`实现一维 DDPM──数据是双峰混合──"网络" est un micro type de MLP, recevoir `(x_t, t)`输出预测噪音──训练就是那一行损失──采样代反向链──

### Étape 1: calendrier anticipé (formule fermé)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### Étape 2: échantillon `x_t`en une seule prise

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Étape 3: une étape de formation

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### Étape 4: prélèvement inverse

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

Pour un problème 1D avec 40 étapes de temps et un MLP de 24 unités, il apprend le mélange des deux modes en ~200 époques.

> Pour les 40 étapes de temps et les 24 unités de MLP, environ 200 ronde de formation est possible en double-pièces mixtes.

## Le temps est conditionné .

Le réseau doit savoir quel temps il détecte.

> Le réseau doit savoir à quel moment il fait du bruit.

- **Sinusoidal embedding.**Comme le codage positionnel de Transformer.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`Passer par un MLP, diffuser sur le net.
  **正弦嵌入。**类似 Transformer 位置编码──
- **Film / group-norm conditioning.**L'intégration de projet à l'échelle/bias par canal (FiLM) à chaque bloc.
  **FiLM / 组归一化条件化。**Il sera placé dans une projection pour chaque canal de réduction/décalage.

Notre code jouet utilise le synusoïdal → concat.

> Nous avons créé un jeu avec un fichier.

## Les pièges sont des pièges.

- **Schedule matters a lot.**Linear `β`Le calendrier de calcul de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de cette valeur de cette valeur est de cette valeur est de cette valeur est de cette valeur est de cette valeur est de cette valeur est de cette valeur.
  **调度很重要。**线性 `β`Il est DDPM 默认但余弦调度在相同计算量下 FID 更好──
- **Timestep embedding is fragile.**Passer cru `t`comme un flot fonctionne pour le jouet 1-D mais ne fonctionne pas pour les images; utilisez toujours une intégration appropriée.
  **时间步嵌入脆弱。**     `t`Le nombre de points dans le jouet 1D est disponible mais l'image ne marche pas.
- **V-prediction vs ε-prediction.**Pour les régimes étroits (très petits ou très grands t), `ε`Il est très faible en signal-au-bruit.`v = α·ε - σ·x`) est plus stable; SDXL, SD3 et Flux l'utilisent.
  **V 预测 vs ε 预测。**Dans le temps, V est plus stable.
- **Classifier-free guidance.**Pour l'inférence, calculer à la fois conditionnelle et inconditionnelle `ε`Alors ...`ε_cfg = (1 + w) · ε_cond - w · ε_uncond`avec `w ≈ 3-7`- C'est le sujet de la leçon 8.
  **无分类器引导。**推理时计算条件和无条件预测的差值──第 08 课详述──
- **1000 steps is a lot.**La production utilise du DDIM (20-50 étapes), du DPM-Solver (10-20 étapes) ou de la distillation (1-4 étapes). Voir leçon 12.
  **1000 步太多了。**Il est également possible de faire des tests de détection de la quantité de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de dé

## Utilisez-le avec le cadre de réalisation

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

La diffusion est la colonne vertébrale générative universelle. Le flux de correspondance (leçon 13) est le concurrent 2024-2026 qui gagne généralement sur la vitesse d'inférence pour la même qualité.

> 扩散是通用生成骨干;;Flow Matching (第 13 课) est un concurrent de 2024-2026, généralement plus rapide en fonction de la même qualité.

## Envoyez-le . Produit .

- Ça va .`outputs/skill-diffusion-trainer.md`. Les compétences prennent un ensemble de données + budget et des résultats de calcul: calendrier (linéaire/cosine/sigmoïde), objectif de prédiction (ε/v/x), nombre d'étapes, échelle de guidage, famille de prélèvements et protocole d'évaluation.

> 保存 `outputs/skill-diffusion-trainer.md` Skiller à recevoir des données + calculer le budget, à produire des données, à prévoir des objectifs, à suivre des mesures, à réduire les échantillons et à évaluer les accords.

## Les exercices

1. **Easy / 简单.**Changez le T de 40 à 10 en `code/main.py`- Comment la qualité de l'échantillon (histogramme visuel des sorties) se dégrade-t-elle ?
   Comment la structure de double sommet est-elle en train de s'effondrer ?
2. **Medium / 中等.**Passez de la prédiction à la prédiction, faites la dérive inverse, comparez la qualité de l'échantillon final.
   De ε 预测切换到v 预测。 redirigé contre direction étapes。
3. **Hard / 困难.**Ajouter des instructions sans classifiant. Condition sur une étiquette de classe `c ∈ {0, 1}`, en la déduisant 10% du temps pendant la formation et lors de l'utilisation de l'échantillonnage `ε = (1+w)·ε_cond - w·ε_uncond`. Mesurer le taux de touches en mode conditionnel à `w = 0, 1, 3, 7`- Je suis désolé .
   添加无分类器引导──测量 `w = 0, 1, 3, 7`Les conditions de vie sont différentes.

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Note de production: l'inférence de diffusion est un problème de nombre de étapes

Le papier DDPM exécute T=1000 étapes inverses. Personne ne le fait en production. Chaque pile d'inférence réelle choisit une des trois stratégies  et chaque carte détermine clairement le cadre de production de "d'où vient la latence":

> Le DDPM 论文 T=1000 Réversé étape.

1. **Faster sampler, same model.**DDIM (20-50 étapes), DPM-Solver++ (10-20), UniPC (8-16).`ε_θ`Les poids sont intacts, réduit la latence de 20 à 50 fois.
   **更快的采样器，相同模型。**DDIM、DPM-Solver++、UniPC──即插即用替换反向循环,降低延迟 20-50 倍──
2. **Distillation.**Formez un élève à correspondre à l'enseignant en moins d'étapes: Distillation progressive (2 → 1), Modèles de cohérence (arbitrary → 1-4), LCM, SDXL-Turbo, SD3-Turbo.
   **蒸馏。**訓練学生模型在更少步数匹配教师──再降延迟 5-10 倍,需要重训──
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`, les arrière-plans de diffusion de TensorRT-LLM,`xformers`Attention SDPA, poids bf16. Coupe de latence par étape ~ 2x.
   **缓存和编译。**La réaction de la société est de réduire la fréquence de la réaction de la société.

Pour un serveur de diffusion de production, la conversation budgétaire est la même que celle décrite dans la littérature de production pour les LLM: la latence est `num_steps × step_cost + VAE_decode`, le débit est `batch_size × (num_steps × step_cost)^-1`. Le TTFT est petit (une étape); l'équivalent TPOT est le temps de réponse complet car la génération d'images est " tout à la fois " du point de vue de l'utilisateur.

> L'économie de la production et de la production de produits de base`num_steps × step_cost + VAE_decode`◊TTFT 很小(一步);TPOT 等价物是完整响应时间──

## Encore une lecture

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) le papier de diffusion, en avance sur son temps.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502)- DDIM, moins de pas.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672)- Le calendrier cosine, la variance apprise.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) orientation du classifiateur.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) Notation unifiée, recette la plus propre.
