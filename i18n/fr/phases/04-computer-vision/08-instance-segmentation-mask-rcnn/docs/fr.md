# Segmentation d'instance Masque R-CNN

> Ajouter une branche de masque à un détecteur R-CNN plus rapide et vous avez une segmentation d'instance.

> **【中文解读】**Le problème est que les différentes zones candidates de taille RoIA alignent les caractéristiques de la zone de taille fixe, et maintiennent l'exactitude de l'espace. La différence entre la division des exemples et la division des termes est que les exemples peuvent être divisés par des individus différents de la même catégorie (comme chaque personne dans la photo).

> **【拓展：实例分割的应用】**Masque R-CNN  широко utilisé pour la conduite autonome 区分不同车辆和行人) 机器人抓取 识别单个物体轮) 视频编辑 精确图)  RoIAlign 技术后来也被用于视觉变换器的适配器中──

**Type:** Build + Learn | **类型:** 动手 + 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (YOLO), Phase 4 Lesson 07 (U-Net) | **前置知识:** Phase 4 Lesson 06（YOLO），Phase 4 Lesson 07（U-Net）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Tracer l'architecture de fin à fin de la masque R-CNN: colonne vertébrale, FPN, RPN, RoIAlign, tête de boîte, tête de masque
- Implementer RoIAlign à partir de zéro et expliquer pourquoi RoIPool n'est plus utilisé
- Utilisez la visibilité de la torche `maskrcnn_resnet50_fpn_v2`modèle prétrainé pour les masques d'instance de qualité de production et lire correctement son format de sortie
- R-CNN à régler sur un petit ensemble de données personnalisé en remplaçant la boîte et les têtes de masque et en gardant le dos gelé

> **【中文解读】**Les objectifs de l'apprentissage sont énumérés dans la liste des compétences fondamentales que l'on devrait acquérir après avoir terminé la classe.


## Le problème , l' introduction du problème

La segmentation sémantique vous donne un masque par classe. La segmentation par instances vous donne un masque par objet, même lorsque deux objets partagent une classe. Le comptage des individus, le suivi des cadres et la mesure des choses (la boîte de délimitation de chaque brique dans un mur, chaque cellule dans une image au microscope) nécessitent tous une segmentation par instances.

> 语义分割给你每一类一个掩码――实例分割给你每一个物体一个掩码, même si deux objets appartiennent à la même catégorie――数个体、跨跟踪和测量东西―― chaque bloc dans le mur的边界框、显微镜图像中每细胞) 需要实例分割――

Mask R-CNN (He et al., 2017) a résolu cette question en reformulant la segmentation d'instance en tant que détection plus-un masque. La conception était si propre que pendant les cinq années suivantes, presque tous les documents de segmentation d'instance étaient une variante de Mask R-CNN, et la mise en œuvre de la torchvision est toujours la norme par défaut de production pour les petits et moyens ensembles de données.

> Le masque R-CNN est en cours de révision en 2017 en utilisant la division d'exemples pour résoudre ce problème.

Le problème difficile de l'ingénierie est le prélèvement d'échantillons: comment extraire une région de fonctionnalités de taille fixe d'une boîte de proposition dont les coins ne sont pas alignés sur les limites des pixels?

> Le problème de l'ingénierie est le suivant: comment pouvez-vous couper une zone de caractéristiques de taille fixe dans un cadre de candidature qui ne correspond pas à la limite du tableau ?

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


### L'architecture

```mermaid
flowchart LR
    IMG["Input"] --> BB["ResNet<br/>backbone"]
    BB --> FPN["Feature<br/>Pyramid Network"]
    FPN --> RPN["Region<br/>Proposal<br/>Network"]
    FPN --> RA["RoIAlign"]
    RPN -->|"top-K proposals"| RA
    RA --> BH["Box head<br/>(class + refine)"]
    RA --> MH["Mask head<br/>(14x14 conv)"]
    BH --> NMS["NMS"]
    MH --> NMS
    NMS --> OUT["boxes +<br/>classes + masks"]

    style BB fill:#dbeafe,stroke:#2563eb
    style FPN fill:#fef3c7,stroke:#d97706
    style RPN fill:#fecaca,stroke:#dc2626
    style OUT fill:#dcfce7,stroke:#16a34a
```

Cinq pièces à comprendre:

1. **Backbone** ResNet-50 ou ResNet-101 formé sur ImageNet. Produit une hiérarchie de cartes de fonctionnalités aux étapes 4, 8, 16, 32.
   Le résnet 50 ou le résnet 101 sont formés en ImageNet.
2. **FPN (Feature Pyramid Network)** connexions latérales supérieures et inférieures qui donnent à chaque niveau C des canaux riches en fonctionnalités sémantiques.
   Traduction chinoise: depuis le haut et le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas, vers le bas.
3. **RPN (Region Proposal Network)** une petite tête de convection qui, à chaque position d'ancrage, prédit "y a-t-il un objet ici?" et "comment affiner la boîte ?" Produit ~ 1000 propositions par image.
   Un petit volume de volumes, en chaque point de position prédiction " y a-t-il ici des objets ? " et " comment modifier le bord de bord ? "
4. **RoIAlign** échantillonnage d'un patch de taille fixe (par exemple 7x7) provenant de n'importe quelle boîte sur n'importe quel niveau FPN.
   Le modèle est un modèle de la taille fixe de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille.
5. **Heads** tête de boîte à deux couches qui raffinent la boîte et choisit une classe, plus une petite tête de boîte qui donne une sortie `28x28`masque binaire pour chaque proposition.
   Deux couches de boîtes sont utilisées pour modifier les limites du boîtier et choisir les catégories, en plus d'un petit rouleau pour chaque zone de sortie.`28x28`Le deuxième est le couvert.

### Pourquoi RoIAlign et non RoIPool

Le R-CNN Fast a utilisé RoIPool, qui divise une boîte de proposition en une grille, prend la fonctionnalité maximale dans chaque cellule et arrondit toutes les coordonnées en nombres entiers.

> Le premier Fast R-CNN utilisait un RoIPool, il divisait le cadre de candidature en un réseau, en prenant la valeur de la plus grande caractéristique de chaque segment, et en faisait un nombre entier de tous les cadres. Ce cadres permettait à l'image de caractéristiques et de cadres d'entrée de figure d'avoir une influence très petite sur l'image de 224x224, mais quand le cadres de cadres de 32 c'était catastrophique.

```
RoIPool:
  box (34.7, 51.3, 98.2, 142.9)
  round -> (34, 51, 98, 142)
  split grid -> round each cell boundary
  misalignment accumulates at every step

RoIAlign:
  box (34.7, 51.3, 98.2, 142.9)
  sample at exact float coordinates using bilinear interpolation
  no rounding anywhere
```

RoIAlign relève le masque AP de 3 à 4 points sur COCO gratuitement.

> Roialign en COCO 上免费提升掩码 AP 3-4 个点──每个关心定位精度检测器现在都使用它YOLOv7 seg、RT-DETR、Mask2Former 无一例外──

### Le RPN en un seul paragraphe

À chaque position d'une carte de caractéristiques, placez des boîtes d'ancrage K de différentes tailles et formes. Prédire un score d'objets pour chaque ancre et un décalage de régression pour transformer l'ancre en une boîte plus adaptée. Gardez les 1000 boîtes de dessus par score, appliquez NMS à l'UIO 0.7, et remettez les survivants aux têtes. Le RPN est formé avec sa propre mini-perte  la même structure que la perte YOLO de la leçon 6, seulement avec deux classes (objet / aucun objet).

> Pour chaque boîte prévoir un débit objectif et un déviation de retour, le boîte sera transformé en boîte de bord plus adaptée. Pour conserver le score maximum d'environ 1000 boîtes, dans l'application NMS de l'IoU 0.7, le survivant sera remis à la suite du chapitre. RPN utilisera sa propre structure de petite perte de fonction pour entraîner la perte de YOLO de la 6e classe, il n'y a que deux catégories d'objets (non objets) (environ 200).

### La tête du masque

Pour chaque proposition (après RoIAlign), la tête de masque est une minuscule FCN: quatre conv 3x3, une deconv 2x, une conv finale 1x1 qui produit `num_classes`les canaux de sortie à `28x28`La résolution. Seul le canal correspondant à la classe prévue est conservé; les autres sont ignorés.

> Pour chaque région candidate, le titre de la base est un FCN minuscule: quatre volumes 3x3 ∙ un 2x contrevolumes ∙ un 1x1 final ∙`28x28`Résolution sur génération `num_classes`个输出通道―― seulement conservé avec la prédiction des classes à l'égard des passages; le reste des passages sont ignorés―― ce qui va cacher la prédiction et la classification des solutions──

Prenez le masque 28x28 à la taille de pixel originale de la proposition pour produire le masque binaire final.

> Prendre le modèle de la couverture de 28x28 à la taille de la image originale de la zone de candidature, générant la couverture de valeur secondaire finale.

### Les pertes

Mask R-CNN a quatre pertes ajoutées:

> Le masque R-CNN a quatre défauts supplémentaires:

```
L = L_rpn_cls + L_rpn_box + L_box_cls + L_box_reg + L_mask
```

- `L_rpn_cls`- Je suis là .`L_rpn_box` objet + régression des boîtes pour les propositions RPN.
  Le RPN 候选区的目标性和边界框归归损失.
- `L_box_cls` entropies croisées sur les classes (C+1) (y compris les arrière-plans) du classeur de la tête.
  Le premier est un type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type (C+1 (C+1).
- `L_box_reg` L1 lisse sur le raffinement de la boîte de la tête.
  Le texte est en français: L1 损失.
- `L_mask` entropies binaires croisées par pixel sur la sortie de masque 28x28.
  Le nombre de coups de feu de la ligne de détail est de 28x28

Chaque perte a son propre poids par défaut; la mise en œuvre de la torche les expose comme des arguments de constructeur.

> Chaque perte a son propre poids par défaut; la vision de la torche  réaliser les exposer à la construction des paramètres de fonction 

### Format de sortie

`torchvision.models.detection.maskrcnn_resnet50_fpn_v2`renvoie une liste de dicts, un par image:

```
{
    "boxes":  (N, 4) in (x1, y1, x2, y2) pixel coordinates,
    "labels": (N,) class IDs, 0 = background so indices are 1-based,
    "scores": (N,) confidence scores,
    "masks":  (N, 1, H, W) float masks in [0, 1] — threshold at 0.5 for binary,
}
```

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.


Le masque est déjà en pleine résolution, la tête de sortie 28x28 a été échantillonnée à l'intérieur.

> **【拓展：工业部署中的视觉系统】**Dans le cadre de la déploiement industriel réel, les modèles visuels doivent prendre en compte la réflexion sur la différence de taille des modèles, l'adaptation des appareils de bord, etc. TensorRT, ONNX Runtime, OpenVINO sont des outils d'accélération de réflexion courants. Les systèmes de conduite autonome (comme Tesla FSD) utilisent généralement plusieurs modèles visuels en temps réel sur les puces de véhicule.

> **【拓展：数据标注与质量】**L'efficacité des tâches visuelles dépend fortement de la qualité des données de marquage. Le Studio de marquage, CVAT, est l'outil de marquage principal. Dans le monde industriel, l'apprentissage actif peut réduire le coût de marquage.



## Construisez-le et mettez-le en œuvre.
```figure
cv3-roialign-sampling
```

## Faites-le

### Étape 1: aligner le système royaux à partir de zéro

C'est le seul composant de Mask R-CNN qui est plus simple à comprendre en code que en prose.

> C'est le seul composant de Mask R-CNN qui utilise le code plus facilement que le texte.

```python
import torch
import torch.nn.functional as F

def roi_align_single(feature, box, output_size=7, spatial_scale=1 / 16.0):
    """
    feature: (C, H, W) single-image feature map
    box: (x1, y1, x2, y2) in original image pixel coordinates
    output_size: side of the output grid (7 for box head, 14 for mask head)
    spatial_scale: reciprocal of the feature map stride
    """
    C, H, W = feature.shape
    x1, y1, x2, y2 = [c * spatial_scale - 0.5 for c in box]
    bin_w = (x2 - x1) / output_size
    bin_h = (y2 - y1) / output_size

    grid_y = torch.linspace(y1 + bin_h / 2, y2 - bin_h / 2, output_size)
    grid_x = torch.linspace(x1 + bin_w / 2, x2 - bin_w / 2, output_size)
    yy, xx = torch.meshgrid(grid_y, grid_x, indexing="ij")

    gx = 2 * (xx + 0.5) / W - 1
    gy = 2 * (yy + 0.5) / H - 1
    grid = torch.stack([gx, gy], dim=-1).unsqueeze(0)
    sampled = F.grid_sample(feature.unsqueeze(0), grid, mode="bilinear",
                            align_corners=False)
    return sampled.squeeze(0)
```

Chaque nombre est dans une position bilinéaire sans arrondissement, sans quantification, sans dégradation.

> Chaque valeur est située sur une position bilatérale.

### Étape 2: Comparer avec le RoIAlign de torchvision

```python
from torchvision.ops import roi_align

feature = torch.randn(1, 16, 50, 50)
boxes = torch.tensor([[0, 10, 20, 100, 90]], dtype=torch.float32)  # (batch_idx, x1, y1, x2, y2)

ours = roi_align_single(feature[0], boxes[0, 1:].tolist(), output_size=7, spatial_scale=1/4)
theirs = roi_align(feature, boxes, output_size=(7, 7), spatial_scale=1/4, sampling_ratio=1, aligned=True)[0]

print(f"shape ours:   {tuple(ours.shape)}")
print(f"shape theirs: {tuple(theirs.shape)}")
print(f"max|diff|:    {(ours - theirs).abs().max().item():.3e}")
```

Avec `sampling_ratio=1`et `aligned=True`, les deux correspondent à l' intérieur `1e-5`- Je suis désolé .

> - Je suis là .`sampling_ratio=1`且 `aligned=True`时, les différences entre les deux `1e-5`Dans le même temps.

### Étape 3: Charger un masque R-CNN prétrainé

```python
import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2, MaskRCNN_ResNet50_FPN_V2_Weights

model = maskrcnn_resnet50_fpn_v2(weights=MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
model.eval()
print(f"params: {sum(p.numel() for p in model.parameters()):,}")
print(f"classes (including background): {len(model.roi_heads.box_predictor.cls_score.out_features * [0])}")
```

Les paramètres 46M, 91 classes (COCO). La première classe (id 0) est l'arrière-plan; tout ce que le modèle détecte réellement commence à id 1.

> 46000000 paramètres,91 个类别(COCO)。第一个类别(id 0) 是背景;模型实际检测所有类别从 id 1 开始。

### Étape 4: Exécuter une inférence

```python
with torch.no_grad():
    x = torch.randn(3, 400, 600)
    predictions = model([x])
p = predictions[0]
print(f"boxes:  {tuple(p['boxes'].shape)}")
print(f"labels: {tuple(p['labels'].shape)}")
print(f"scores: {tuple(p['scores'].shape)}")
print(f"masks:  {tuple(p['masks'].shape)}")
```

Le tensor du masque est de forme .`(N, 1, H, W)`- Le seuil de 0,5 pour obtenir un masque binaire par objet:

> 掩码张量形为 `(N, 1, H, W)` Obtenir une valeur de 0,5 pour chaque objet:

```python
binary_masks = (p['masks'] > 0.5).squeeze(1)  # (N, H, W) boolean
```

### Étape 5: Échangez les têtes pour un compte de classe personnalisé

La recette commune de réglage fin: réutiliser la colonne vertébrale, FPN et RPN; remplacer les deux têtes de classification.

> 常见的微调方案: réutiliser le réseau de base de la structure, FPN et RPN; remplacer les deux têtes de la structure.

```python
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

def build_custom_maskrcnn(num_classes):
    model = maskrcnn_resnet50_fpn_v2(weights=MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)
    return model

custom = build_custom_maskrcnn(num_classes=5)
print(f"custom cls_score.out_features: {custom.roi_heads.box_predictor.cls_score.out_features}")
```

`num_classes`doit inclure la classe de fond, de sorte qu'un ensemble de données avec 4 classes d'objets utilise `num_classes=5`- Je suis désolé .

> `num_classes`Il doit contenir des catégories de contexte, de sorte qu'il existe 4 catégories d'objets utilisant des données.`num_classes=5`Il y a une autre.

### Étape 6: congeler ce qui n'a pas besoin d'être formé

Sur de petits ensembles de données, congeler la colonne vertébrale et le FPN.

> Dans les petits ensembles de données, il n'y a que les objectifs et les revenus de RPN et les deux principaux participants à l'étude.

```python
def freeze_backbone_and_fpn(model):
    # torchvision Mask R-CNN packs the FPN inside `model.backbone` (as
    # `model.backbone.fpn`), so iterating `model.backbone.parameters()` covers
    # both the ResNet feature layers and the FPN lateral/output convs.
    for p in model.backbone.parameters():
        p.requires_grad = False
    return model

custom = freeze_backbone_and_fpn(custom)
trainable = sum(p.numel() for p in custom.parameters() if p.requires_grad)
print(f"trainable after freeze: {trainable:,}")
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Sur les ensembles de données de 500 images, c'est la différence entre convergence et suradaptation.




> **【拓展：视觉模型的持续学习】**Dans un environnement de production, le modèle visuel doit être en constante évolution pour s'adapter à de nouveaux données. La technologie de l'apprentissage continu permet d'éviter que le modèle s'adapte à de nouvelles données et oublie les anciens connaissances.

## Utilisez-le avec le cadre de réalisation

La boucle d'entraînement complète pour Mask R-CNN dans torchvision est de 40 lignes et ne change pas significativement entre les tâches  swap datasets et go.

```python
def train_step(model, images, targets, optimizer):
    model.train()
    loss_dict = model(images, targets)
    losses = sum(loss for loss in loss_dict.values())
    optimizer.zero_grad()
    losses.backward()
    optimizer.step()
    return {k: v.item() for k, v in loss_dict.items()}
```

Le `targets`La liste doit contenir des dicts par image avec `boxes`- Je suis là .`labels`, et `masks`(comme `(num_instances, H, W)`Le modèle renvoie un dict de quatre pertes pendant l'entraînement et une liste de prédictions pendant l'évaluation, en fonction de la tactique `model.training`- Je suis désolé .

Le `pycocotools`l'évaluateur produit mAP@IoU=0.5:0.95 pour les boîtes et les masques; vous avez besoin des deux numéros pour savoir si la tête de boîte ou la tête de masque est le col de bouteille.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.




## Envoyez-le . Produit .

Cette leçon donne:

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──


- `outputs/prompt-instance-vs-semantic-router.md` une requête qui pose trois questions et choisit l'instance vs sémantique vs panoptique plus le modèle exact pour commencer.
- `outputs/skill-mask-rcnn-head-swapper.md` une compétence qui génère les 10 lignes de code pour échanger les têtes sur n'importe quel modèle de détection de torchvision, étant donné le nouveau `num_classes`- Je suis désolé .

## Les exercices

1. **(Easy)**Vérifiez votre alignement de royauté contre `torchvision.ops.roi_align`En plus de cela, il est possible de faire une analyse de la différence absolue maximale.
2. **(Medium)**- Je suis bien .`maskrcnn_resnet50_fpn_v2`sur un ensemble de données personnalisé de 50 images (deux classes: ballons, poissons, poussières, logos).
3. **(Hard)**Remplacez la tête de masque de Mask R-CNN par une tête qui prédit à 56x56 au lieu de 28x28. Mesurez mAP@IoU = 0,75 avant et après. Expliquez pourquoi le gain (ou l'absence de celui-ci) correspond à l'échange de précision limite / mémoire attendu.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Mask R-CNN | "Detection plus masks" | Faster R-CNN + a small FCN head that predicts a 28x28 mask per proposal per class |
| FPN | "Feature pyramid" | Top-down + lateral connections that give every stride level C channels of semantic-rich features |
| RPN | "Region proposer" | A small conv head that produces ~1000 object/no-object proposals per image |
| RoIAlign | "No-rounding crop" | Bilinearly samples a fixed-size feature grid from any float-coordinate box |
| RoIPool | "Pre-2017 crop" | Same purpose as RoIAlign but rounds box coordinates; obsolete |
| Mask AP | "Instance mAP" | Average precision computed with mask IoU instead of box IoU; the COCO instance segmentation metric |
| Binary mask head | "Per-class mask" | Predicts one binary mask per class for each proposal; only the predicted class's channel is kept |
| Background class | "Class 0" | The catch-all "no object" class; indices for real classes start at 1 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Mask R-CNN (He et al., 2017)](https://arxiv.org/abs/1703.06870) l'article; la section 3 sur le RoIAlign est la lecture critique
- [FPN: Feature Pyramid Networks (Lin et al., 2017)](https://arxiv.org/abs/1612.03144) le papier FPN; chaque détecteur moderne l'utilise
- [torchvision Mask R-CNN tutorial](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html) la référence pour la boucle d'ajustement fin
- [Detectron2 model zoo](https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md) Implémentations de production avec poids formés pour presque toutes les variantes de détection et de segmentation
