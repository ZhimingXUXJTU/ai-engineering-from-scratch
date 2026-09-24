# Flow Matching & Rectified Flow 流匹配与整流

> Les modèles de diffusion prennent 20 à 50 étapes de prélèvement d'échantillons parce qu'ils suivent un chemin incurvé du bruit aux données.

> **【中文解读】**Le modèle de diffusion nécessite 20 à 50 étapes de la conception car il s'agit de la combinaison de flux et de flux rectifié.

> **【拓展：Flow Matching 是 2024-2026 的趋势】**Le flux de correspondance est en train de remplacer la régulation de diffusion traditionnelle en tant que norme du modèle de production de nouvelle génération.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Le processus inverse du DDPM est une marche stochastique de 1000 pas de `N(0, I)`Le blocage est que le processus inverse est rigide, le chemin est incurvé.

> Le processus de réaction du DDPM est de`N(0, I)`Retour à 1000 étapes de la distribution des données avec le temps. Le DIM est réduit à 20 à 50 étapes.

Si vous pouviez former le modèle de telle sorte que le chemin du bruit vers les données était une * ligne droite*, un seul pas d'Euler de `t=1`à `t=0`Le flux de correspondance construit ceci directement: définir une interpolation en ligne droite à partir de`x_1 ∼ N(0, I)`à `x_0 ∼ data`, entraîne un champ vectoriel `v_θ(x, t)`pour correspondre à sa dérivée temporelle, intégrer à l'inférence.

> Si le modèle d'entraînement permet de faire du bruit à la datation, le chemin est *direct*, étape Euler de `t=1`À la`t=0`Pour le dépôt de la résolution, il faut faire une comparaison directe.`x_1 ∼ N(0, I)`À la`x_0 ∼ data`Le train de l'équipe`v_θ(x, t)`匹配时间导数──

Le flux rectifié (Liu 2022) va plus loin: redresser de manière itérative les chemins avec une procédure de reflux qui produit un ODE progressivement plus proche de la ligne. Après deux itérations de reflux, un échantillonneur en 2 étapes correspond à la qualité DDPM en 50 étapes.

> Réglementation du flux (en 2022): plus loin: par le reflux 过程 代拉直路径──两次 reflux 代后,2 步采器匹配 50 步 DDPM质量──

> **【中文解读】**Le flux de données est un flux de données de 20 à 50 étapes. Si vous pouvez entraîner un flux de données, vous pouvez passer de la fréquence de bruit à la fréquence de données.

> **【拓展：FLUX.1 的 Flow Matching 实现】**FLUX.1 des Black Forest Labs est une architecture de diffusion de flux qui est nettement supérieure à celle de la SDXL. La version FLUX.1 est en seulement 4 étapes de production d'images de haute qualité.

## Le concept de base.

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Des lignes droites

Définir:

> 定义:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

où `x_0 ~ data`et `x_1 ~ N(0, I)`La dérivée temporelle le long de cette ligne droite est constante:

> Parmi eux `x_0 ~ data`- Je suis désolé .`x_1 ~ N(0, I)` Le nombre de temps de la ligne droite est le nombre constant:

```
dx_t / dt = x_1 - x_0
```

Définir un champ vectoriel neuronal `v_θ(x_t, t)`et l'entraîner à correspondre à cette dérivé:

> 定义神经向量场 `v_θ(x_t, t)`, entraînement il correspond à ce guide:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

C' est le **conditional flow matching**L'apprentissage est sans simulation: vous ne déployez jamais l'ODE.`(x_0, x_1, t)`et le régression.

> C'est comme ça.**条件 Flow Matching**L'entraînement est sans simulation.`(x_0, x_1, t)`Il ne fait pas de retour.

### Prenez des échantillons.

Pour l'inférence, intégrez le champ vectoriel appris * à l'arrière* dans le temps:

> 推理时,将学到的量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Commencez par `x_1 ~ N(0, I)`, Euler-passer vers le bas à `t=0`- Je suis désolé .

> De `x_1 ~ N(0, I)`- Ça va aller.`t=0`Il y a une autre.

### Le flux de l'eau est corrigé (Liu 2022)

Les voies de la ligne droite fonctionnent, mais les voies apprises ne sont pas en fait droites. Elles se courbent parce que beaucoup de voies sont droites.`x_0`s peut être cartographié à la même `x_1`. étape de reflux du flux rectifié:

> Le flux direct, bien que efficace, mais le chemin de l'apprentissage en fait* n'est pas vraiment direct*`x_0`Ça peut être diffusé sur le même.`x_1`,路径会曲──Reflow de reflux de reflux 步骤:

1. Modèle de débit de train v_1 avec des couplages aléatoires.
   Utilisez le modèle de l'entraînement Flow v_1──
2. Pratique N paires `(x_1, x_0)`en intégrant v_1 à partir de `x_1`à son atterrissage `x_0`- Je suis désolé .
   通过将 v_1 从 `x_1`- Je suis en train de tomber.`x_0`采样 N à`(x_1, x_0)`Il y a une autre.
3. En train de v_2 sur ces exemples en couple. Parce que les paires sont maintenant "ODE-matched", l'interpolant en ligne droite entre eux est vraiment plus plat.
   Dans ces exemples de couplage, l'équilibre est "ODE" et la valeur de l'interaction entre eux est plus plate.
4. Je répète.
   Je vous en prie.

En pratique, 2 itérations de reflux vous amènent à une approche linéaire, permettant une inférence de 2 à 4 étapes. SDXL-Turbo, SD3-Turbo, LCM sont tous des modèles distillés à partir de flux.

> En pratique, 2 fois de reflux 代就能使路径接近线性,从而支持 2-4 步推理──SDXL-Turbo、SD3-Turbo、LCM sont basés sur le modèle de parallèle de flux 蒸出的模型──

### Pourquoi cette image a gagné en 2024 ? Pourquoi la génération d'images 2024 a-t-elle évolué vers le flux de correspondance ?

Trois raisons:

> Trois raisons:

1. **Simulation-free training** aucune ODE déroulant pendant la formation, trivial à mettre en œuvre.
   **无需仿真的训练** entraînement                                                                                                                                                                                                                                                             
2. **Better loss geometry** les voies droites ont une signal-au-bruit cohérente, alors que la DDPM ε-loss a une mauvaise SNR aux bords du calendrier.
   **更优的损失几何** 直线路径信噪比一致, tandis que l' ε-losse du DDPM est en moyenne supérieure à celle du SNR.
3. **Faster inference** 4 à 8 étapes à la qualité SDXL-Turbo; 1 étape avec distillation de consistance.
   **更快的推理**4-8 步即可达到 SDXL-Turbo 质量;

## Le flux correspondant versus DDPM  la connexion exacte  Le flux correspondant versus DDPM  精确联系

Le flux correspondant à un chemin conditionné de Gauss est la diffusion *avec un calendrier de bruit spécifique*.`x_t = α(t) x_0 + σ(t) x_1`Le calendrier et le flux correspondant récupèrent la diffusion réformée par Stratonovich avec `v = α'·x_0 - σ'·x_1`Les deux sont équivalents algébriques pour les chemins gaussiens.

> Utilisation de la méthode de coordonnée de flux de haute qualité est en fait un modèle de diffusion avec une régulation sonore spécifique.`x_t = α(t) x_0 + σ(t) x_1`调度后,Flow Matching encore en forme de réécriture de Stratonovich`v = α'·x_0 - σ'·x_1`Pour les voies de hauteur, les deux sont égaux en prix.

Ce que l'ajustement de flux a ajouté: la * clarté* de la cible (une vitesse simple), une perte plus nette et la licence d'expérimenter avec des interpolants non gaussiens.

> Le vrai apport de l'ajustement de flux est: la clarté de l'objectif, la perte de la vitesse normale, ainsi que la liberté de tenter de ne pas ajouter de valeur à hauteur.

## Construisez-le et mettez-le en œuvre.
```figure
normalizing-flow
```

## Faites-le

`code/main.py`Il met en œuvre une correspondance de flux 1D sur un mélange gaussien à deux modes.`v_θ(x, t)`En conclusion, intégrez les étapes 1, 2, 4 et 20 d'Euler et comparez la qualité de l'échantillon.

> `code/main.py`Dans la distribution mixte de deux sommets, réaliser un parallèle de flux en 1D.`v_θ(x, t)`C'est un MLP de type micro, utilisant une formation directe à l'objectif.

### Étape 1: Perte d'entraînement

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 训练损失: prise de bruit `x1`Et le temps`t`, valeur de construction`x_t`, objectif `x1 - x0`, faire le retour à la place.

### Étape 2: inférence multi-étape étape 2: plusieurs étapes de la réflexion

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> Il est possible de faire des calculs de la fréquence de fréquence des émissions de bruit à haute fréquence, selon le nombre de pas vers le point de vue de la fréquence de fréquence.

### Étape 3: Comparer le nombre de étapes.

Attendez-vous que le prélèvement de 4 étapes corresponde déjà à la qualité de 20 étapes  un gros problème pour la latence.

> 4 étapes de l'échantillonnage doivent être adaptées à 20 étapes de qualité.

## Les pièges sont des pièges.

- **Time parameterization.**Utilisation de l' échange de flux `t ∈ [0, 1]`avec `t=0`à la base de données, `t=1`à l'aide de la DDPM`t ∈ [0, T]`avec `t=0`à la base de données, `t=T`Les journaux se trompent constamment.
  时间参数化: flux correspondant utilisé `t ∈ [0, 1]`- Je suis désolé .`t=0`Dans les données,`t=1`Dans le bruit, DDPM utilise`t ∈ [0, T]`Les résultats sont les mêmes mais les dimensions différentes.
- **Schedule choice.**La ligne droite du flux rectifié est le calendrier de correspondance des flux, mais vous pouvez utiliser l'échantillonnage t-normal cosine ou logite (SD3 le fait) pour une meilleure couverture à l'échelle.
  调度选择: La ligne droite du flux rectifié est "standard" du flux de correspondance 调度, mais peut être utilisé avec cosine ou logique-normal de t 采样(SD3 就是这样做) pour obtenir une meilleure mesure de couverture。
- **Reflow cost.**Générer le jeu de données en couple pour le reflux est un passage d'inférence complet par échantillon.
  Reflux: générer un reflux  associer à un ensemble de données nécessite un seul échantillon pour une analyse complète .
- **Classifier-free guidance still applies.**Il suffit d' échanger ε contre v dans la combinaison linéaire: `v_cfg = (1+w) v_cond - w v_uncond`- Je suis désolé .
  Guidance libre de classifiateur  encore applicable: seulement nécessaire de mettre en ligne  换成 v:`v_cfg = (1+w) v_cond - w v_uncond`Il y a une autre.

## Utilisez-le avec le cadre de réalisation

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Chaque fois qu'un article dit "plus vite que la diffusion" en 2025-2026, c'est presque toujours le flux correspondant + la distillation.

> Quand l'article dit "Bí expandir más rápido" , presque toujours est le flux correspondant + 蒸──

## Envoyez-le . Produit .

- Ça va .`outputs/skill-fm-tuner.md`. Skill prend une spécification de modèle de diffusion et la convertit en une configuration de formation correspondant au flux: choix de calendrier, répartition des échantillons de temps (uniforme / logit-normal), optimisateur, plan de reflux, compte de étapes cibles, protocole d'évaluation.

> 保存为 `outputs/skill-fm-tuner.md` Cette compétence reçoit un modèle de modèle de diffusion, le transforme en flux de correspondance de formation de config:调度选择、时间采样分布(uniform / logit-normal) 、优化器、reflow 计划、目标步数、评估协议。

## Les exercices

1. **Easy.**On court .`code/main.py`et comparer la MSE de 1 étape contre 20 étapes contre la réelle distribution des données.
   **简单。**运行  référencement`code/main.py`, comparer les MSE de la répartition des données réelles par 1 et 20 étapes.
2. **Medium.**Passez de l' uniforme .`t`L'échantillonnage est-il en phase logit-normale (concentre l'échantillonnage au milieu de la phase t)?
   **中等。**Généralement`t`采样切换为 logit-normal (?? 集中在中间 t 附近采样)
3. **Hard.**Implémenter une itération de reflux: générer des paires (x_0, x_1) en intégrant le premier modèle, entraîner un deuxième modèle sur les paires et comparer la qualité de l'échantillon en 1 étape.
   **困难。**实现一次回流 代: en entraînant le deuxième modèle à la première échelle de production de couleurs (x_0, x_1), en entraînant le deuxième modèle à la première échelle de couleurs,并比较 1 步采样质量──

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Note de production: Flux.1-schnell est le flux correspondant à sa plus rapide

Le résultat de la production de flux matching est Flux.1-schnell  un flux-matched DiT distillé à 1-4 étapes d'inférence tout en maintenant la qualité de flux-dev-grade. Le bloc-notes de Niels "Run Flux sur une machine de 8 Go" est la recette de déploiement de référence: T5 + CLIP code, quantifié MMDiT dénoncer (en 4 étapes pour rapide vs 50 pour dev), VAE décode. La comptabilité des coûts:

> Le flux de production est le résultat de la production de Flux.1-schnell un évaporation à 1 à 4 étapes de la conception de la qualité de flux-dev  DiT。Niels' notebook "Flow matching on 8GB 机器运行Flux" est un référencement de la déploiement du programme:T5 + CLIP 编码、量化MMDiT 去噪音(schnell 4 步相比 dev 50 步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

La règle de production: **flow-matched base + distillation = the 2026 default for fast text-to-image.**Chaque grand fournisseur expédie cette combinaison: SD3-Turbo (SD3 + flux + distillation), Flux-schnell (Flux-dev + rectifié-flux), CogView-4-Flash.

> Règles de production:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**Chaque grand fabricant a proposé ce type de composition:SD3-Turbo(SD3 + flux + 蒸)、Flux-schnell(Flux-dev + flux rectifié 拉直)、CogView-4-Flash──纯扩散基座只为遗留检查点保留──

## Encore une lecture

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) débit rectifié.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) correspondance des flux.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, débit rectifié à l'échelle.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) cadre général qui couvre la diffusion FM+.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) Destilation en 1 étape de diffusion/flux.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042) Variante turbo.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) correspondance des flux dans la production.
