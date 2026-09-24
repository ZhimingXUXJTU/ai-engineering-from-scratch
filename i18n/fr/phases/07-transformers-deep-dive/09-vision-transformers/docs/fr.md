# Les transformateurs de vision (ViT)

> Une image est une grille de patchs, une phrase est une grille de jetons, le même transformateur les mange tous les deux.

> **【中文解读】**ViT Placez l'image coupée en patch 当作 टोकन 序列处理──理解 ViT =理解Transformer Non limité à la NLP──CLIP、DALL-E、Sora 都基于Transformer──

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Avant 2020, la vision par ordinateur signifiait des convulsions. Chaque SOTA sur ImageNet, COCO et les benchmarks de détection utilisaient une colonne vertébrale de CNN.

> Avant 2020, le computer vision signifiait "volume": ImageNet, COCO et chaque SOTA sur le fondement de l'analyse utilisait le réseau de base de la CNN.

Dosovitskiy et coll. (2020)  " Une image vaut 16x16 mots "  a montré que vous pouvez laisser tomber les convolutions entièrement. Couper une image en patches de taille fixe, projeter linéairement chaque patch dans une intégration, alimenter la séquence à un encodeur transformateur de vanille. À une échelle suffisante (ImageNet-21k pré-entraînement ou plus grande), ViT correspond ou bat les modèles basés sur ResNet.

> Dosovitskiy 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送进标准变压器编码器──在足够大的下规模(ImageNet-21k 预训或更大),ViT可以匹配或超越基于ResNet的模型──

ViT a été le début d'un modèle plus large en 2026: une architecture, de nombreuses modalités. Whisper symbolise l'audio. ViT symbolise les images. Tokens d'action pour la robotique. Tokens de pixels pour la vidéo. Le transformateur ne se soucie pas  alimente une séquence et il apprend.

> ViT est le point de départ d'une tendance plus large de 2026: une architecture, plusieurs modèles, etc.

En 2026, ViT et ses descendants (DeiT, Swin, DINOv2, ViT-22B, SAM 3) possèdent la plupart de la vision. Les CNN gagnent toujours sur les appareils de bord et les tâches sensibles à la latence. Tout le reste a un ViT quelque part dans la pile.

> En 2026, le ViT et ses successeurs (DeiT, Swin, DINOv2, ViT-22B, SAM3) occupent la majeure partie du domaine visuel.

> **【中文解读】**L'image peut être coupée comme un texte en séquence "token" ⋅ 224x224                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

## Le concept de base.

![Image → patches → tokens → transformer](../assets/vit.svg)

### Étape 1  patch

Partagez un`H × W × C`image dans une `N × (P·P·C)`séquence de patchs plats. configuration typique: `224 × 224`image, `16 × 16`Les correctifs → 196 correctifs de 768 valeurs chacun.

> Il va`H × W × C`图像分为 `N × (P·P·C)`序列──typique de la mise en place:`224 × 224`- Une image.`16 × 16`Le patch → 196 个 768 值的补丁──

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

Les patches plus petites = plus de jetons, meilleure résolution, coût d'attention quadratique.

> Le patch, plus petit, plus petit, plus gros, moins cher, plus gros.

### Étape 2  intégration linéaire

Une seule matrice apprise projette chaque plateau plat à `d_model`. Équivalent à une convolutions de taille du noyau `P`et de faire des pas.`P`En PyTorch , c' est littéralement`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` une mise en œuvre en deux lignes.

> Une matrice d'apprentissage sera chaque patch plat`d_model`◊ égal prix à la grandeur nucléaire`P`、步长为 `P`Je suis en train de me faire une idée.`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现──

> **【拓展：Swin Transformer 的层级设计】**標準 ViT 使用固定 patch 大小和全局注意力,计算量 O(N^2)。Swin Transformer 引入层次结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野。这使计算复杂变为O(N), tout en préservant la capacité de sélectionner des caractéristiques de niveau。Swin est encore supérieur aux normes ViT。

### Étape 3  préparation `[CLS]`- les symboles, ajouter des emplacements positionnels

- Préparez un apprenant`[CLS]`Son dernier état caché est la représentation d'image utilisée pour la classification.
  En français, traduire en français:`[CLS]`token── son état caché final est utilisé pour la représentation d'images de catégorie──
- Ajouter des embellissements positionnels apprenables (originaux ViT) ou sinusoïdal 2D (variantes ultérieures).
  Le texte est en français et en français.
- En 2024+ RoPE étendu à 2D pour la position, parfois sans intégrations explicites.
  Après 2024, RoPE s'est étendu à la 2D, parfois sans avoir besoin d'une intégration apparente.

### Étape 4  encodeur de transformateur standard

L' épaisseur de blocs de `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`- Identique au BERT. Aucune couche spécifique à la vision.

> Je suis en train de me faire une idée .`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT 完全相同──没有视觉特有的层──这是本文的教学要点──

### Étape 5 - tête

Pour la classification: prenez `[CLS]`L'état caché → linéaire → softmax. pour DINOv2 ou SAM, rejeter `[CLS]`, utilisez directement les inserts de patch.

>  分类: 取`[CLS]` Hide state → 线性层 → softmax── Pour DINOv2 ou SAM, abandonné `[CLS]`, directement utiliser le patch 嵌入──

### Les variantes qui comptent

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### Pourquoi ça a pris du temps ?

ViT a besoin de beaucoup de données pour correspondre aux CNN parce qu'il n'a aucun des biais inductifs de CNN (invariance de traduction, localité). Sans images étiquetées de > 100M ou une pré-entraînement auto-supervisée forte, les CNN gagnent toujours au calcul correspondant. DeiT a corrigé cela en 2021 avec des astuces de distillation; DINOv2 l'a corrigé de façon permanente en 2023 avec l'auto-supervision.

> ViT a besoin d'une quantité importante de données pour correspondre aux performances de CNN, car il n'a pas de préférence pour les attributions de CNN (placement immutable, localisation) ⋅ pas d'image de marque de plus de 1 milliard de pages ou de formation préliminaire de surveillance de CNN, la CNN est toujours en bonne et due forme en fonction du même volume de calcul.

> **【中文解读】**La faible préférence de la ViT est à double tranchant: il faut plus de données pour correspondre aux performances de CNN, car CNN a des préférences de régulation de la planète et de la localisation. Mais lorsque la quantité de données est assez grande, la propagation de ViT est bien supérieure à celle de CNN.

> **【拓展：ViT 在多模态系统中的角色】**CLIP utilise ViT 编码图像、Transformer 编码文本,通过对比学习对齐两个模态──DALL-E 和 Sora utilise ViT comprendre l'image/vidéo, se régénérer en nouveau contenu──SAM(Segment Anything) utilise ViT 作为主干网络实现通用图像分化──ViT 已成为多模态 AI's visual basis module──

## Construisez-le et mettez-le en œuvre.
```figure
n5-patch-stream
```

## Faites-le

Regardez !`code/main.py`- La mise en place de patch-stdlib + intégration linéaire + contrôle de santé mentale.

> 参见 `code/main.py`◊Pure standard library patch + 线性嵌入 + 合理性检查──无训练任何实际规模的VIT都需要PyTorch 和数小时的GPU 时间──

### Étape 1: image fausse

Une image RGB 24 × 24 en tant que liste de lignes de `(R, G, B)`Nous utilisons 6×6 patches → 16 patches, 108-d intégrant vecteur chacun.

> Une image RGB 24 × 24`(R, G, B)`元组的行列表形式表示──使用 6×6 patch → 16 个 patch,每个108 维嵌入向量──

### Étape 2: patch

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

L'ordre des races: rang principal sur la grille.

> L'ordre de la ligne: chaque vitesse utilise ce rangement.

### Étape 3: intégration linéaire

Multipliez chaque plaque par un nombre aléatoire `(patch_flat_size, d_model)`la matrice. Vérifiez que la forme de sortie est `(N_patches + 1, d_model)`après la préparation `[CLS]`- Je suis désolé .

> Pour chaque plaque, multipliez-la par un.`(patch_flat_size, d_model)`La réaction de l'équipe`[CLS]`后输出形状为 `(N_patches + 1, d_model)`Il y a une autre.

### Étape 4: comptez les paramètres pour un ViT réaliste

Imprimez le nombre de paramètres pour ViT-Base: 12 couches, 12 têtes, d = 768, patch = 16.

> 打印 ViT-Base 参数:12 层、12 头、d=768、patch=16──与ResNet-50(约25M)对比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## Utilisez-le avec le cadre de réalisation

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**La colonne vertébrale est gelée, la tête est entraînée, elle fonctionne pour la classification, la récupération, la détection, la sous-titration, les points de contrôle DINOv2 de Meta dépassent CLIP sur toutes les tâches de vision non textuelle.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络, entraînement un小头── s'applique à la classification, à la recherche, à la recherche, à la recherche, à la description de l'image── Meta's DINOv2  Checkpoint sur chaque tâche de visualisation non-littéraire est supérieur à CLIP──

**Patch-size picking.**Les modèles plus petits utilisent 16×16 (ViT-B/16). La prédiction dense (segmentation) utilise 8×8 ou 14×14 (SAM, DINOv2).

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) utiliser 8×8 或 14×14(SAM、DINOv2)。 très grand modèle utiliser 14×14。

## Envoyez-le . Produit .

Regardez !`outputs/skill-vit-configurator.md`. La compétence choisit une variante ViT et une taille de patch pour une nouvelle tâche de vision compte tenu de la taille, de la résolution et du budget de calcul du jeu de données.

> 参见 `outputs/skill-vit-configurator.md` Cette compétence  Selon le volume du jeu de données  la résolution et le budget de calcul, pour les nouvelles tâches visuelles, choisir ViT 变体和补丁 大小──

## Les exercices

1. **Easy.**On court .`code/main.py`- Vérifiez que le nombre de patchs est égal .`(H/P) * (W/P)`et la dimension de la plaque plate est égale `P*P*C`- Je suis désolé .
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` le patch de vérification`(H/P) * (W/P)`, 平 patch 维度等于 `P*P*C`Il y a une autre.
2. **Medium.**Implementer des embellissements positionnels sinusoïdes 2D  deux codes sinusoïdes indépendants pour `row`et `col`Envoyez-les dans un petit PyTorch ViT et comparez la précision par rapport aux emblèmes positionnels appréciables sur CIFAR-10.
   Le texte est en 2D.`row`et `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**Construisez un ViT (PyTorch) à 3 couches, entraînez sur 1000 images MNIST avec des correctifs 4×4. Mesurez la précision du test. Ajoutez maintenant DINOv2 pré-entraînement sur les mêmes 1000 images (simplifié: entraînez simplement le codeur pour prédire les emplacements de correctifs à partir de correctifs masqués).
   Le nombre de tests de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Encore une lecture

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)- Le papier de la ViT.
  Le texte original est en français.
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877)- Je ne sais pas.
  Le texte de la loi est le texte de la loi.
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)- Je suis en train de faire un tour.
  Le changement de couleur de la couleur est un changement de couleur.
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)- DINOv2.
  Le texte de la première partie est le suivant:
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) la fixation du code de registre pour DINOv2.
  Le code de registre de DINOv2 est modifié en français.
