# Le contrôle de la sécurité et de la sécurité

> Le texte seul est un signal de contrôle maladroit. ControlNet vous permet de cloner un modèle de diffusion prétrainé et de le diriger avec une carte de profondeur, un squelette de pose, un graffiti ou une image de bord. LoRA vous permet de affiner un modèle de paramètre 2B en entraînant 10 millions de paramètres. Ensemble, ils ont transformé Stable Diffusion d'un jouet en pipeline d'image 2026 qui est expédié à chaque agence.

> **【中文解读】**純文本控制太粗──ControlNet utilise une image de profondeur, une structure de pose, un graffiti ou un graphisme de bord pour contrôler la production; LoRA ne fait que former 1000 millions de paramètres pour modéliser 20 milliards de paramètres── les deux combinés permettent une diffusion stable des jouets en images de flux de l'image utilisées par chaque entreprise de conception en 2026──

> **【拓展：LoRA 是大模型时代的微调标准】**LoRA (Low Range Adaptation) est utilisé non seulement dans la production d'images, mais aussi largement dans la gestion de la personnalisation de l'IA (LLMA-LoRA) et il est nécessaire de former 0,1% des paramètres pour pouvoir s'adapter à de nouvelles tâches et à de nouveaux styles, ce qui réduit considérablement les coûts de personnalisation de l'IA.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## Le problème , l' introduction du problème

Une demande comme "une femme en robe rouge promenant un chien dans une rue animée" ne donne pas à la mannequin d'informations sur *où* se trouve le chien, *quelle pose* la femme est dans, ou *la perspective* de la rue.

>  Comme "une femme en rouge est un chien sur une rue occupée" cette suggestion ne dit pas au modèle où il se trouve, quelle est la position de la femme, comment elle se présente.

La formation d'un nouveau modèle conditionnel à partir de zéro pour chaque signal (position, profondeur, ruse, segmentation) est prohibitive. Vous voulez garder la colonne vertébrale SDXL de 2,6B paramètre gelée, attacher un petit réseau latéraux qui lit le conditionnement, et le faire pousser les caractéristiques intermédiaires de la colonne vertébrale.

> Pour chaque signal (à partir du niveau de formation, les coûts du nouveau modèle de conditions sont trop élevés, vous voulez maintenir un SDXL de 2,6B, ajouter un petit réseau de côté à des conditions de lecture, c'est le ControlNet.

Vous voulez aussi enseigner au modèle de nouveaux concepts (votre visage, votre produit, votre style) sans refaire de formation au modèle complet. Vous voulez un delta 100 fois plus petit.

> Vous voulez aussi apprendre un nouveau concept de modèle (( votre visage, votre produit, votre style) sans recharger tout le modèle. Vous avez besoin de petit augmentation de 100 fois.

ControlNet + LoRA + texte = le kit d'outils du praticien de 2026. La plupart des pipelines d'images de production couvrent 2 à 5 LoRA, 1-3 ControlNets et un adaptateur IP sur une base SDXL / SD3 / Flux.

> ControlNet + LoRA + texte = boîte à outils des praticiens de 2026 ⋅ la plupart des images sont produites sur la base de l'SDXL/SD3/Flux ⋅ 2 à 5 ⋅ LoRA ⋅ 1-3 ⋅ ControlNet et un adaptateur IP ⋅

## Le concept de base.

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### Le contrôle des données (Zhang et coll., 2023)

Prenez une SD prétrainée. *Cloner* la moitié du codeur de l'U-Net. Congeler l'original. Entrer le clone à accepter une entrée de conditionnement supplémentaire (marges, profondeur, pose). Reconnecter le clone au décodeur de la moitié de l'original avec *zéro-convolution* sauter des connexions (1×1 convs initiales à zéro  commencer comme un no-op, apprendre un delta).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

Le train à 1M (prompte, condition, image) triple la perte de diffusion standard.

Les ControlNets de pérmodalité sont livrés sous forme de petits modèles secondaires (~360 M pour SDXL, ~70 M pour SD 1.5).

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### L'ACE (Hu et coll., 2021)

Pour toute couche linéaire `W ∈ R^{d×d}`dans le modèle, congélation `W`et ajouter un delta de faible rang:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

avec `r << d`.Le rang 4-16 est standard pour l'attention, le rang 64-128 pour les notes fines lourdes.`2 · d · r`Au lieu de `d²`. Pour l' attention de l' SDXL avec `d=640`- Je suis là .`r=16`: 20k par paramètre par adaptateur au lieu de 410k  une réduction de 20x.

Pour en tirer une conclusion , vous pouvez mesurer la LoRA:`W' = W + α · B @ A`- Je suis là .`α = 0.5-1.5`Les LRA multiples s'accumulent additionnellement (avec l'avertissement habituel qu'ils interagissent de manière non linéaire).

### Adapteur IP (Ye et coll., 2023)

Un petit adaptateur qui accepte une *image* comme conditionnement (à côté du texte). Utilise le codeur d'image CLIP pour produire des jetons d'image, les injecte dans l'attention croisée aux côtés des jetons de texte. ~ 20 Mo par modèle de base. Vous permet de "générer une image dans le style de cette référence" sans un LoRA.

## Matrice de composibilité

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

Le réseau de contrôle est spatial, le LoRA est sémantique.

> Le contrôle de l'espace.

> **【中文解读】**Le mécanisme central de ControlNet: Klon SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态)。零卷积(零卷积) initialization assurez le début du entraînement ControlNet ne affecte pas le modèle original。LoRA On lineary layer on add low ranking矩阵 B@A, only train extremely few parameters(20-200MB vs 基础模型 5GB)。

> **【拓展：ControlNet + LoRA 的组合控制】**En production réelle, le contrôle de l'espace et le contrôle de l'image sont généralement utilisés ensemble. Par exemple, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, le contrôle de l'image, et le contrôle de l'image.

## Construisez-le et mettez-le en œuvre.
```figure
v4-controlnet-zero
```

## Faites-le

`code/main.py`simulation des deux mécanismes sur le 1-D:

1. **LoRA.**Une couche linéaire prétrainée `W`- Fermez-le, entraînez un bas rang.`B @ A`comme ça .`W + BA`Il correspond à une couche linéaire cible.`r = 1`suffit pour apprendre une correction de rang 1 parfaitement.

2. **ControlNet-lite.**Un prédicteur de base gelée et un réseau côté qui lit un signal supplémentaire. La sortie du réseau côté est garée par un scalaire apprenable initialement à zéro (notre version de zéro-conv).

### Étape 1: mathématiques de la LORA

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Étape 2: réseau latérale à entrées zéro

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

À l'étape 0 la sortie est identique à la base.`gate`lentement sans dérive catastrophique.

> Dans la première étape, la production est la même que la base.`gate`更新缓慢 没有灾难性偏移──

## Les pièges sont des pièges.

- **Over-scaling LoRAs.** `α = 2`ou `α = 3`est un hack commun "faire le plus fort" qui produit des sorties trop stylisées / cassées.`α ≤ 1.5`- Je suis désolé .
  **LoRA 过度缩放。** `α = 2`Ou `α = 3`Il est courant de " renforcer " la pratique, de produire des sur-échanges/dégâts de production.`α ≤ 1.5`Il y a une autre.
- **ControlNet weight conflict.**L'utilisation d'un Pose ControlNet à un poids de 1,0 et d'un Depth ControlNet à un poids de 1,0 est généralement trop rapide.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 est la valeur par défaut de sécurité.
- **LoRA on the wrong base.**Les SDXL LoRA sont silencieusement non-op sur SD 1.5 parce que les dimensions d'attention ne correspondent pas.
  **LoRA 用错基础模型。**SDXL LoRA est en SD 1.5
- **Textual Inversion drift.**Les jetons entraînés sur un point de contrôle dérivent mal sur un autre.
  **Textual Inversion 漂移。**Dans un point de contrôle, le signe de formation est gravement déplacé dans un autre.
- **LoRA weight-merging and storage.**Vous pouvez cuire un LoRA dans les poids du modèle de base pour une inférence plus rapide (pas d'ajout de temps de course), mais vous perdez la capacité d'échelle `α`Gardez les deux versions.
  **LoRA 权重合并。**On peut accélérer la réflexion dans le modèle de base, mais perdre le temps de fonctionner.`α`De la capacité.

## Utilisez-le avec le cadre de réalisation

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## Envoyez-le . Produit .

- Ça va .`outputs/skill-sd-toolkit-composer.md`. La compétence prend une tâche (actifs d'entrée: prompt, image de référence facultative, pose facultative, profondeur facultative, scribber facultatif) et produit la pile d'outils, les poids et un protocole de semence reproductible.

## Les exercices

1. **Easy / 简单.**Dans `code/main.py`, varient le rang de la LoRA `r`À quel rang le LoRA correspond exactement à un delta cible de rang 2 ?
   Dans le`code/main.py`Le directeur général de la LRA`r`De 1 à 4... Où est le classement de l'ORL ?
2. **Medium / 中等.**Exercez deux LoRA séparés sur deux transformations cibles. Chargez-les ensemble et montrez leur interaction additive.
   En effet, les deux objectifs changent en fonction de la formation de la LRA.
3. **Hard / 困难.**Utilisez des diffuseurs pour empiler: SDXL-base + Canny-ControlNet (poids 0,8) + un style LoRA (α 0,8) + IP-adapter (poids 0,6). Mesurer le compromis FID-contre-prompte-adhérence à mesure que les poids de l'emplacement varient.
   Utilisation de diffuseurs 堆叠组合, mesure FID avec prompt 遵循的权衡──

## Les termes clés

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## Note de production: LoRA swaps, voies de contrôle réseau, service multi-locataires

Un vrai SaaS texte-à-image sert des centaines de LoRA et une douzaine de ControlNets sur le même point de contrôle de base. Le problème de service ressemble beaucoup à la multi-location LLM (la littérature de production couvre le cas LLM sous lotage continu et LoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.**La fusion`W' = W + α·B·A`dans la base donne ~ 3-5% plus rapide par étape d'inférence mais gèle `α`Les LRA sont maintenues chaudes dans le VRAM en tant que delta de rang-r; les diffuseurs sont exposés.`pipe.load_lora_weights()`+ `pipe.set_adapters([...], adapter_weights=[...])`Pour l'activation par demande, le coût de l'échange est le `2 · d · r · num_layers`Poids  à l'échelle de MB, sous-seconde.
- **ControlNet as a second attention lane.**Le codeur cloné fonctionne parallèlement à la base. Deux ControlNets de poids 1,0 chacun = deux passes supplémentaires à l'avant par étape, pas un pass fusionné. La taille du lot diminue quadratiquement. Budget pour ~ 1,5x coût de l'étape par ControlNet actif.
- **Quantized LoRAs too.**Si vous avez quantifié la base (voir leçon 07, Flux sur 8 Go), le delta LoRA quantifie également de manière propre à 8 bits ou 4 bits.

Flux-specific: Le portable de Niels Flux-on-8GB quantifie la base à 4 bits;`pipe.load_lora_weights("user/style-lora")`) sur cette base quantifiée à `weight_name="pytorch_lora_weights.safetensors"`C'est la recette que la plupart des agences SaaS expédient en 2026.

## Encore une lecture

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) ControlNet.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) LoRA (à l'origine pour les LLM; ports à diffusion).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) Adapteur IP.
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) une alternative plus légère au ControlNet.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242)- Le DreamBooth.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) tuyaux de référence.
