# Modèles génératifs  Taxonomie et histoire  生成模型 

> Chaque modèle d'image, modèle de texte, modèle vidéo et modèle 3D s'adapte à l'un des cinq seins. Choisissez le mauvais seau et vous allez vous battre les mathématiques pendant des semaines. Choisissez le bon et les douze dernières années de progrès du domaine s'accumulent en votre tête.

> **【中文解读】**Toutes les images, textes, vidéos et modèles de production 3D peuvent être classés en cinq catégories: VAE、GAN、 modèle de diffusion、 modèle de flux et modèle de retour personnel―; les catégories de choix vous aideront à comprendre les mathématiques et les résultats des 12 dernières années seront clairement accumulés dans votre esprit.

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,Stable Diffusion 的编码器;(2) GAN生成对抗网络,StyleGAN的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow Matching,SD3/FLUX的新方向;(5) 自归GPT 模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## Le problème , l' introduction du problème

Un modèle génératif ne fait qu'un seul travail: des échantillons de formation donnés tirés d'une distribution inconnue `p_data(x)`Les visages, les phrases, les fichiers MIDI, les structures de protéines, tout le même problème si vous clignez des yeux.

> Le modèle de formation ne fait qu'une chose: il est déterminé par une distribution inconnue.`p_data(x)`Les résultats de l'exercice sont les mêmes que ceux de la formation, les résultats sont les mêmes que ceux de la formation.

Le problème c' est que ...`p_data`Les échantillons sont situés sur un mince polyvalent à l'intérieur de cet espace, et vous n'avez peut-être que 10 millions d'exemples.

> Le problème est`p_data`Il existe dans un espace de plusieurs millions de dimensions (une image RGB de 512 x 512 environ 78,60.000 dimensions), le modèle ne prend qu'une forme mince dans cet espace, et vous ne pouvez avoir que 1000 000 de modèles. La densité de la violence est désespérée.

Cinq familles ont survécu au cours des douze dernières années.

> Au cours des 12 dernières années, cinq familles modèles ont survécues. Pour comprendre ce que chaque famille a fait, il faut savoir pourquoi elle a gagné certaines tâches et s'est effondrée dans d'autres.

> **【中文解读】**Le défi réside dans les données rares de l'espace de haute dimension. Les cinq grandes familles de modèles ont des modes de compromis différents: auto-retour/flux modèles directement construits mais limités à la structure; VAE/expansion modèles optimisés densité sous-définition; GAN  saut densité directement générer des modèles;;

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**La tendance la plus importante de 2024-2026 est le passage du modèle de diffusion (DDPM) vers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching) à travers le flux de correspondance (Flow Matching)).

## Le concept de base.

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**Écrivez`log p(x)`Les modèles autorégressifs (PixelCNN, WaveNet, GPT) factorisent`p(x) = ∏ p(x_i | x_<i)`- normalisation des flux (RNVP, Glow)`p(x)`Les résultats de l'analyse de la base sont les suivants: la probabilité exacte, la perte de formation nette, la déduction autorégressive, la séquence (lente pour les longues séquences), les flux nécessitent des architectures invertibles (architecturellement restrictives).

> **1. 显式密度，可处理。**Il va`log p(x)`写成可以实际求值的求和──自归归模型(PixelCNN、WaveNet、GPT) va être unifié divisé en conditionnellement distribué multiplicité──标准化流(RealNVP、Glow) via simple distribution de la structure de changement de réaction`p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)

**2. Explicit density, approximate.**Lié`log p(x)`Les modèles de diffusion (DDPM, Ho 2020) entraînent un dénonciateur qui optimise implicitement un ELBO pondéré. La diffusion est la colonne vertébrale dominante de l'image, de la vidéo et de la 3D en 2026.

> **2. 显式密度，近似。**De l'autre côté`log p(x)`(ELBO)并优化该下界──VAE Utilisation de codeur-décodeur et de changement de la suite expérience──扩散模型训练去噪机,隐式优化加权 ELBO──扩散模型是 2026年图像、视频和3D 的主导骨干──

**3. Implicit density.**Sautez complètement la densité; apprenez un générateur `G(z)`qui produit des échantillons et un discriminateur `D(x)`Les GAN (Goodfellow 2014). Rapides à l'inférence (une passe avant) mais notoirement instables pendant l'entraînement. StyleGAN 1/2/3 reste l'état de l'art pour le photoréalisme de domaine fixe (visages, chambres à coucher) même en 2026.

> **3. 隐式密度。**Completement sauter sur l'estimation de la densité; apprendre un générateur `G(z)`产生样本,一个判别器 `D(x)`区分真假──GAN 推理快(单次前向传播), mais la formation est extrêmement instable──StyleGAN 1/2/3 est même en 2026 le modèle le plus avancé de la réalité du niveau de la photographie fixe──

**4. Score-based / continuous-time.**Apprenez le gradient de la densité de la tige `∇_x log p(x)`(le score) directement. Song & Ermon (2019) a montré que le parallèle de score généralise la diffusion à un SDE. Le parallèle de flux (Lipman 2023) est la chaleur 2024-2026: formation sans simulation, chemins plus droits, échantillonnage 4-10 fois plus rapide que le DDPM. Stable Diffusion 3, Flux, AudioCraft 2 utilisent tous le parallèle de flux.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度(分数函数) ――Song & Ermon (2019) 证明分数匹配将扩散推广到SDE──Flow Matching(2023) is 2024-2026热门:免模拟训练,更直的路径,比DDPM 快 4-10 倍──Stable Diffusion 3、Flux、AudioCraft 2 都使用Flow Matching──

> **【中文解读】**Le parallèle de flux et de coordonnées est une amélioration et une panne du modèle de diffusion. Le parallèle de flux a simplifié le processus d'entraînement sans avoir besoin de simuler le SDE, en apprenant directement le bruit à la transmission des données.

**5. Token-based autoregressive over discrete codes.**Comprimez les données à haute résolution avec un VQ-VAE ou un quantificateur résiduel dans une courte séquence de jetons discrets, puis utilisez un transformateur pour modéliser la séquence de jetons. Parti, MuseNet, AudioLM, VALL-E, le jetonnisateur de correctifs de Sora utilisent tous cela.

> **5. 基于离散 token 的自回归。**Utilisez VQ-VAE ou un restant quantificateur pour compresser les données en une courte séquence de jetons dispersés, puis utilisez Transformer 建模 token 序列──Parti、MuseNet、AudioLM、VALL-E、Sora.

## Une brève histoire.

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## Le tri des cinq questions.

Lorsque vous trouverez un nouveau modèle génératif, répondez à ces cinq questions avant de lire la section méthode.

> Lorsqu'un nouveau thème de génération de modèle est publié, vous devez répondre à ces cinq questions avant de commencer à lire la section méthode.

1. **What is being modeled?**Pixels, latences, jetons discrets, Gaussians 3D, mailles, formes d'onde ?
   **正在建模什么？**- Je suis en train de vous dire.
2. **Is the density explicit or implicit?**Ils l' écrivent ?`log p(x)`- Je suis désolé .
   **密度是显式还是隐式的？**Ils ont écrit ?`log p(x)`- Je suis désolé .
3. **Sampling: one-shot or iterative?**Iteratif signifie inférence plus lente; un coup signifie généralement adversarial ou distillé.
   **采样：单次还是迭代？**代 signifie penser plus lentement;单次 habituellement signifie contre ou蒸──
4. **Conditioning: unconditional, class, text, image, pose?**Cela détermine la perte et l'échafaudage architectural.
   **条件：无条件、类别、文本、图像、姿态？**Cela détermine les fonctions et les cadres de structure de perte.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**Chacun a connu des modes d'échec (voir leçon 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**Chacun a un modèle de défaillance déjà connu (voir le 14e cours).

Vous répondrez à ces cinq questions à chaque leçon de cette phase.

> Vous allez réécrire ces cinq questions dans chaque partie de cette phase.

> **【中文解读】**Ces cinq questions (construction d'objets, densité apparente/invisible, échantillonnage, type de conditions, indicateur d'évaluation) sont un cadre général pour analyser tout modèle généré. Répondre à ces cinq questions dans chaque section suivante peut vous aider à comprendre rapidement la contribution et la sélection technique du nouveau thème.

## Construisez-le et mettez-le en œuvre.
```figure
autoencoder-bottleneck
```

## Faites-le

Le code de cette leçon est une visualisation légère: adapter un mélange de Gaussins en 1D à partir d'échantillons à l'aide de trois approches de jouets (densité du noyau, histogramme discrète et générateur "GAN-ish" de l'échantillon le plus proche) afin que vous puissiez voir la différence entre la densité explicite et implicite sur un problème que vous pouvez imprimer sur un écran.

> Le code de cette classe est une visualisation à la lumière: utilisez trois méthodes simples: calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire, calcul de la densité nucléaire et de la densité nucléaire.

On court .`code/main.py`Il tire 2000 échantillons d'un mélange gaussien à deux modes, puis imprime:

> 运行  référencement`code/main.py`Il a extrait 2000 échantillons de la mixture de deux sommets et imprimé:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Remarquez: les deux premières vous permettent de demander "combien est probable ce point?" La troisième ne peut pas. C'est la distinction * explicite vs implicite* qui sera importante pour chaque future leçon.

> Remarque: les deux méthodes précédentes peuvent répondre à "Quelle est la probabilité de ce point ?" La troisième est impossible.

## Utilisez-le avec le cadre de réalisation

Quelle famille, pour quelle tâche, en 2026 ?

> En 2026, quelle famille va s'adapter à quelles missions ?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-model-chooser.md`- Je suis désolé .

> 保存为 `outputs/skill-model-chooser.md`Il y a une autre.

La compétence prend une description de tâche et des résultats: (1) quelle famille utiliser, (2) une liste classée de trois options ouvertes et trois hébergées, (3) le mode de défaillance probable que vous devriez surveiller, et (4) un budget de calcul/temps.

> Le savoir-faire  recevoir des tâches description,输出: 1) 应使用哪个家族, 2) 应使用哪个家族, 2) 应注意的可能失效模式, 4) 计算/时间预算.

## Les exercices

1. **Easy / 简单.**Pour chacun de ces cinq produits, identifiez la famille et la colonne vertébrale: image ChatGPT, Midjourney v7, Sora, Runway Gen-3, ElevenLabs.
   Pour ces cinq produits, identifier sa famille et ses origines: image ChatGPT, image Midjourney v7, Sora, Runway Gen-3, ElevenLabs,
2. **Medium / 中等.**Le journal que vous allez lire demain précise que le prélèvement d'échantillons est 100 fois plus rapide que la diffusion.
   Vous devez lire demain l'article qui affirme être plus rapide que le 100 fois plus rapide.
3. **Hard / 困难.**Prenez un domaine qui vous intéresse (par exemple structure des protéines, CAD, molécules, trajectoires). Répondre au triage de cinq questions pour le modèle SOTA actuel dans ce domaine et dessiner ce qu'un meilleur modèle changerait.
   选择一个你关心的领域 (如蛋白质结构,CAD,分子轨迹) ⋅ Pour ce domaine, le modèle actuel SOTA répond à cinq questions,并勾绘更好的模型会改变什么──

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Note de production: cinq familles, cinq formes d'inférence

Chaque famille affiche une courbe de coûts différente entre les inférences et les serveurs.

> Chaque famille doit répondre à différentes décompositions de serveur.

- **Autoregressive (bucket 1 and 5).**Le décode séquentiel domine la latence; le cache KV, le batchage continu et le décode spéculatif s'appliquent tous directement.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**Il n'y a pas de décode au sens de la LLM.`num_steps × step_cost`, et le `step_cost`Les boutons de production sont le nombre d'étapes (DDIM / DPM-Solver / distillation), la taille du lot et la précision (bf16 / fp8 / int4).
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**LLM 意义上没有解码──成本 = `num_steps × step_cost`, la production est un cycle de dimensionnement et de précision.
- **GAN (bucket 3).**Un pass avant, pas de calendrier, pas de cache KV, TTFT ≈ latence totale, c'est pourquoi StyleGAN gagne toujours sur l'UX de domaine étroit.
  **GAN（第 3 类）。**单次前向传播──没有调度,没有 KV 缓存──TTFT ≈ 总延迟──这就是StayGAN在狭域UX上仍然胜出的原因──

Lorsque vous voyez "plus rapide que la diffusion" dans un résumé papier, traduisez-le par "moins de pas × le même coût de la phase" ou "les mêmes étapes × le coût de la phase moins cher".

> Lorsque le résumé de l'article dit "quand la propagation est plus rapide", il est traduit par "moins de coûts de progression × de coûts de comparaison" ou "plus de coûts de progression × de coûts de progression moins chers".

## Encore une lecture

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) le papier GAN.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) le papier de l'AEV.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) le document du DDPM.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) diffusion en tant que SDE.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) le papier de correspondance de débit.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) Diffusion stable 3.
