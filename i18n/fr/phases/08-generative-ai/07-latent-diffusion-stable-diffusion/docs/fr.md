# Diffusion latente et diffusion stable.

> La diffusion de l'espace-pixel sur les images 512x512 est un crime de guerre informatique. Rombach et coll. (2022) ont remarqué que vous n'avez pas besoin de toutes les dimensions 786k pour générer une image  vous avez besoin de suffisamment pour capturer la structure sémantique, et un décodeur séparé pour le reste.

> **【中文解读】**Dans le 512x512 像素空间做扩散是计算灾难──Rombach 等人发现不需要全部 78.6万维度只需要捕获语义结构,剩余用解码器补充──

> **【拓展：Stable Diffusion 的革命】**La diffusion stable permettra de diffuser le processus de diffusion du lieu de la image au lieu de l'espace potentiel, réduisant la quantité de calcul de dizaines de fois, permettant la mise en œuvre de GPU de niveau de consommation. Après la publication de la source ouverte, le LoRA a provoqué un écosystème riche, le ControlNet, etc., favorisant la diffusion de l'AIGC.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

La diffusion de l' espace-pixel à 5122 signifie que le réseau U fonctionne sur des tensors de forme .`[B, 3, 512, 512]`Chaque étape d'échantillonnage est d'environ 100 GFLOPS pour un U-Net de 500M. 50 étapes sont 5 TFLOPS par image.

> 5122 像素空间扩散 signifie U-Net dans `[B, 3, 512, 512]`张量上运行──每采样步约100GFLOPS──50 步就是5 TFLOPS──在十亿图像上训练计算成本荒谬──

La plupart de ces FLOPs vont pousser des détails perceptiblement sans importance à travers le net  la texture à haute fréquence qu'un VAE perdant pourrait compresser. L'idée de Rombach: entraîner un VAE une fois (le * premier stade*), le geler, et exécuter la diffusion entièrement dans l'espace latent 64×64 à 4 canaux (le * deuxième stade*). Le même U-Net. 1/16 des pixels. ~ 64x moins de FLOPs pour une qualité comparable.

> La plupart des FLOPs sont utilisés pour faire avancer la perception sur des détails non importants.

C'est la recette de diffusion stable. SD 1.x / 2.x a utilisé un U-Net de 860M sur `64×64×4`Les données de l'U-Net sont en cours de révision.`128×128×4`Le flux de la technologie est basé sur le flux de la technologie de diffusion.

> C'est le modèle de diffusion stable. SD 1.x/2.x utilise 860M U-Net sur 64×64×4 , SDXL utilise 2.6B U-Net sur 128×128×4 , SD3 utilise DiT + Flow Matching .

> **【中文解读】**L'architecture centrale de la diffusion stable est de deux phases de conception: 1) la première phase VAE 编码器 va 512x512 图像压缩到64x64x4 潜在空间(16 倍压缩); 2) la deuxième phase 运行在潜在空间中运行扩散过程──U-Net sur 64x64 张量运行,计算量降低约64 倍── SD 1.x到 SD3 演变:U-Net → DiT(Diffusion Transformer), DDPM → Flow Matching──

> **【拓展：从 U-Net 到 DiT 的架构变迁】**SD 1.x/2.x Utilisation de l'U-Net  comme réseau de dés noise.SD3(2024) et FLUX 转向 DiT(Diffusion Transformer) Utilisation de la Transformer 替代 U-Net。DiT's advantage is in expansion ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ 

## Le concept de base.

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.**Le codeur `E(x) → z`, décodeur `D(z) → x`. Compression cible: 8 fois échantillon en bas dans chaque axe spatial + réglage des canaux de sorte que la taille totale latente soit ~1/16e du nombre de pixels. Perte = reconstruction (L1 + LPIPS perceptuelle) + KL (peut-être faible poids)`z`n'est pas forcé trop Gaussian, parce que nous n'avons pas besoin de prélèvement exact de `z`Les images décodées sont souvent nettes.

   **阶段 1 — VAE。**编码器 `E(x) → z`, décodeur `D(z) → x` L'objectif de la construction: 8 fois le volume de l'essence.

2. **Stage 2 — diffusion on `z`.**Traiter`z = E(x_real)`En effet, les données sont les données de l'entreprise.`z_t`- À l' inférence: échantillon `z_0`par diffusion, alors `x = D(z_0)`- Je suis désolé .

   **阶段 2 — 在 `z` 上扩散。**Il va`z = E(x_real)`视为数据──训练 U-Net(或 DiT) 去噪音──推理时:采样 `z_0`Alors ...`x = D(z_0)`Il y a une autre.

**Text conditioning.**Deux composants supplémentaires: un encodeur de texte gelé (CLIP-L pour SD 1.x, CLIP-L+OpenCLIP-G pour SD 2/XL, T5-XXL pour SD3 et Flux).`[Q = image features, K = V = text tokens]`Les jetons sont la seule façon dont le texte influence l'image.

> **文本条件化。**结的文本编码器和交叉注意注入──每块 U-Net `[Q = 图像特征, K = V = 文本 token]`Faire une mise en garde: les symboles sont le seul moyen de modifier l'image.

**The loss function is identical to Lesson 06.**Le même DDPM / flux correspondant MSE sur le bruit. Vous changez simplement le domaine de données.

> **损失函数与第 06 课完全相同。**Je viens juste de changer de domaine de données.

## Des variantes d'architecture.

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

La tendance: remplacer U-Net par DiT (transformateur sur les patches latentes), élargir le codeur de texte (T5 dépasse CLIP pour une adhésion rapide), augmenter les canaux latents (4 → 16 donne plus de place aux détails).

> 趋势: utiliser DiT 替代 U-Net, étendre le texte编码器(T5 在 prompt 遵循上优于CLIP), augmenter les voies de communication possibles(4→16 给更多细节余量)

## Construisez-le et mettez-le en œuvre.
```figure
noise-schedule
```

## Faites-le

`code/main.py`Il met un jouet 1-D "VAE" (encodeur d'identité + décodeur, pour démonstration; un vrai VAE serait un réseau de convex) en haut du DDPM de la leçon 06 et ajoute un conditionnement de classe avec une orientation sans classifiant. Il montre que la même perte de diffusion fonctionne que vous exécutez sur des valeurs 1D brutes ou sur des valeurs codées  l'information clé.

> `code/main.py`Dans la 6e classe, un jouet 1D "VAE" est superposé sur le DDPM et un guide sans classe conditionnel est ajouté. Il montre une perte de propagation efficace à la fois sur la valeur initiale et sur la valeur de code.

### Étape 1: codeur/décodeur

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

Pour la pédagogie, cette carte linéaire suffit à montrer que la diffusion opère sur`z`sans se soucier de l'espace de données original.

> En effet, les élèves de la VAE ont une bonne formation.`z`Il ne s'agit pas de l'espace de données original.

### Étape 2: diffusion dans `z`- l'espace

Le même DDPM que la leçon 06.`z = E(x)`Après le prélèvement`z_0`, décodez avec `D(z_0)`- Je suis désolé .

> Les données vues sur le réseau sont les mêmes que celles du DDPM.`z = E(x)`- Je suis un homme.`z_0`后用 `D(z_0)`Je suis désolé.

### Étape 3: orientation sans classifiant

Pendant la formation, laissez tomber l'étiquette de classe 10% du temps (replacez-la par un jeton nul).`ε_cond`et `ε_uncond`, puis:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0`= aucune orientation (plénière diversité), `w = 3`= par défaut, `w = 7+`= saturée / trop tranchante.

> `w = 0`= 无引导(完全多样性),`w = 3`- Je suis un homme.`w = 7+`= 和/过度利。

### Étape 4: conditionnement du texte (concept, pas code)

Remplacez l'étiquette de classe par une sortie d'encodeur de texte gelé.

> Utilisation de l'étiquette de type U-Net:

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

C'est la seule différence substantielle entre un modèle de diffusion classé et une diffusion stable.

> C'est la seule différence substantielle entre le modèle de diffusion de classe et la diffusion stable.

## Les pièges sont des pièges.

- **VAE-scale mismatch.**SD 1.x VAEs ont une constante d'échelle (`scaling_factor ≈ 0.18215`L'oubli de cela fait que le train U-Net est en latences avec une variance très fausse.
  **VAE 尺度不匹配。**SD 1.x VAE  codifier après un nombre constant réduit ⋅ oublier que cela permettra à U-Net de s'entraîner sur le potentiel de l'espace de différence d'erreur ⋅
- **Text encoder silently wrong.**SD3 a besoin de T5-XXL avec >=128 jetons, et le retour à CLIP-seulement est perçu.`use_t5=True`ou des cratères de fidélité rapides.
  **文本编码器静默错误。**SD3 需要 T5-XXL 且 >=128 token──
- **Mixing latent spaces.**SDXL, SD3, Flux utilisent tous différents VAE. Un LoRA formé sur les latents SDXL ne fonctionnera pas sur SD3.
  **混合潜在空间。**SDXL、SD3、Flux avec différents VAE。SDXL de LoRA non peut être utilisé sur SD3
- **CFG too high.** `w > 10`Il est donc important de noter que les résultats obtenus par la Commission sont très variés.`w = 3-7`- Je suis désolé .
  **CFG 太高。** `w > 10`产生和、油的图像──
- **Negative prompts leaking.**Une requête négative vide devient le jeton nul; une requête négative remplie devient la `ε_uncond`Ce n'est pas la même chose, certains pipelines sont silencieusement défauts à la nullité.
  **负向 prompt 泄漏。**空负向 prompt 变为零代币; remplir de changements `ε_uncond`                                                                                                                                                                                                                                                              

## Utilisez-le avec le cadre de réalisation

Stacks de production en 2026:

> 2026: année de production

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## Envoyez-le . Produit .

- Ça va .`outputs/skill-sd-prompter.md`. Skill prend un prompt texte + style cible et les sorties: modèle + point de contrôle, échelle CFG, échantillon, prompt négatif, résolution, combo optionnel ControlNet/IP-Adapter, et une liste de contrôle de QA par étape.

> 保存 `outputs/skill-sd-prompter.md`◊Skill 接收文本提示+目标风格,输出模型+检查点、CFG、采样器、负向提示等──

## Les exercices

1. **Easy / 简单.**On court .`code/main.py`avec une direction `w ∈ {0, 1, 3, 7, 15}`- Enregistrer l'échantillon moyen par classe.`w`les moyens de classe divergent-ils au-delà des moyens de données réelles ?
   - Je veux le faire .`w ∈ {0, 1, 3, 7, 15}`- Je suis là.`w`La valeur moyenne de la catégorie par rapport à la valeur moyenne des données réelles ?
2. **Medium / 中等.**Le codeur linéaire du jouet est remplacé par un codeur/décodeur tanh-MLP avec une perte de reconstruction.
   Le codeur de jouets est-il remplacé par le codeur de jouets en ligne en tant que codeur/décodeur en tant que TANH-MLP ?
3. **Hard / 困难.**Installez une réelle inférence de diffusion stable avec des diffuseurs: charge `sdxl-base`, exécute 30 étapes Euler avec CFG = 7, le temps.`sdxl-turbo`Le même sujet, une qualité différente  décrit ce qui a changé et pourquoi.
   Utiliser des diffuseurs 搭建真实SD 推理, comparer SDXL-base 和 SDXL-Turbo

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| First stage | "The VAE" | Trained encoder/decoder pair; compresses 512² to 64². / 训练好的编码/解码器对；将 512² 压缩到 64²。 |
| Second stage | "The U-Net" | Diffusion model over the latent space. / 潜在空间上的扩散模型。 |
| CFG | "Guidance scale" / "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`; tunes conditioning strength. / 调节条件化强度。 |
| Null token | "Empty prompt embed" / "空 prompt 嵌入" | Unconditional embed used for `ε_uncond`. / 用于无条件预测的嵌入。 |
| Cross-attention | "How text gets in" / "文本如何进入" | Each U-Net block attends to text tokens as K and V. / 每个 U-Net 块对文本 token 做注意力。 |
| DiT | "Diffusion Transformer" | Replace U-Net with a transformer over latent patches; scales better. / 用 Transformer 替代 U-Net。 |
| MMDiT | "Multi-modal DiT" / "多模态 DiT" | SD3's architecture: text and image streams with joint attention. / SD3 架构：文本和图像流的联合注意力。 |
| VAE scaling factor | "Magic number" / "魔数" | Divides latents by ~5.4 so diffusion operates in unit-variance space. / 除以约 5.4 使扩散在单位方差空间操作。 |

## Note de production: exécuter Flux-12B sur un GPU de consommation de 8 Go

L'intégration de référence Flux est la recette canonique "J'ai un GPU de consommation, puis-je expédier ceci?"

> 参考流体集成是经典的"je ne peux déployer que des GPU de consommation ?"方案──三旋方案:

1. **Staggered loading.**Flux a trois réseaux qui n'ont jamais besoin de coexister dans VRAM: T5-XXL encodeur de texte (~ 10 Go en fp32), CLIP-L (petit), le 12B MMDiT, et le VAE. Encodez le prompt d'abord, * supprimez* les encodeurs, chargez le DiT, dénoncez, * supprimez* le DiT, chargez le VAE, décodez. Les GPU de 8 Go de consommation ne s'adaptent qu'à une étape à la fois.
   **交错加载。**Le flux a trois besoins en même temps de séjourner dans le réseau de VRAM.
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`Le codeur T5 et le DiT. Coupe la mémoire 8x, la baisse de qualité est imperceptible pour les textes à images par référence d'Aritra (lié dans le carnet).
   **4 位量化。**La T5 et la DiT sont quantifiées à 4 bits, la mémoire est réduite de 8 fois, la perte de qualité est minime.
3. **CPU offload.** `pipe.enable_model_cpu_offload()`Il échange automatiquement les modules entre le processeur et la GPU à mesure que chaque passage avance.
   **CPU 卸载。**Automatisez les modules de commutation entre le CPU et le GPU. Augmentez de 10 à 20% le retard, mais laissez le flux de courant fonctionner.

La comptabilité de la mémoire est: `10 GB T5 / 8 = 1.25 GB`quantifiés, `12 B params × 0.5 bytes = ~6 GB`En termes de stas00, c'est l'extrémité extrême de TP = 1 inférence  pas de parallélisme de modèle, quantification maximale. Pour la production, vous exécutez TP = 2 ou TP = 4 sur H100s; pour un seul ordinateur portable de développement, c'est la recette.

## Encore une lecture

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Diffusion stable.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748)- Je suis désolé.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) Famille Flux1.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) mise en œuvre de référence pour chaque point de contrôle ci-dessus.
