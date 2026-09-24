# Vue en temps réel  Déploiement de bord  Vue en temps réel  Déploiement à la frontière

> L'inférence de bord est la discipline consistant à faire fonctionner un modèle de 90 degrés de précision à 30 fps sur un appareil avec 2 Go de RAM.

> **【中文解读】**Le détail de la mise en place de la méthode de calcul est un équilibre: permettre à 90% de la précision de fonctionner à 30 fps sur un appareil de 2 Go de stockage interne.

> **【拓展：边缘 AI 的应用】**Le réseau mobile, YOLO-nano, EfficientNet est un modèle de classe légère courante.

**Type:** Learn + Build | **类型:** 学习 + 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 04 (Image Classification), Phase 10 Lesson 11 (Quantization) | **前置知识:** Phase 4 Lesson 04（图像分类），Phase 10 Lesson 11（量化）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Mesurer la latence d'inférence, la mémoire maximale et le débit pour tout modèle PyTorch, et lire les FLOPs / paramètres / compromis de latence
- Quantiser un modèle de vision à l'INT8 en utilisant la quantification post-entraînement de PyTorch et vérifier la perte de précision < 1%
- Exporter à ONNX et compiler avec ONNX Runtime ou TensorRT; nommer les trois défaillances d'exportation les plus courantes et leurs corrections
- Expliquer quand choisir MobileNetV3, EfficientNet-Lite, ConvNeXt-Tiny ou MobileViT pour une restriction de bord

> **【中文解读】**Les objectifs de l'apprentissage sont énumérés dans la liste des compétences fondamentales que l'on devrait acquérir après avoir terminé la classe.


## Le problème , l' introduction du problème

Un modèle de vision en temps d'entraînement est un monstre à point flottant. 100M de paramètres, 10 GFLOPs par passe avant, 2 GB de VRAM. Aucun de ces éléments ne convient à un téléphone, à une unité d'info-entretenement d'une voiture, à une caméra industrielle ou à un drone.

> Le modèle visuel de l'entraînement est un modèle de déploiement de monstres.1.000 millions de paramètres. Il est diffusé à 10 GFLOPs par seconde.

Trois boutons font la plupart du travail: le choix du modèle (une architecture plus petite avec la même recette), la quantification (INT8 au lieu de FP32) et le temps d'exécution des inferences (ONNX Runtime, TensorRT, Core ML, TFLite).

> Les trois cycles ont fait la majeure partie du travail: modèle sélectionné (int8 substitution FP32) et la différence entre les produits livrés sur les modules de caméra de 30 dollars et les produits qui fonctionnent sur les stations de travail.

Cette leçon met en place la discipline de mesure en premier lieu (on ne peut pas optimiser ce qu'on ne peut pas mesurer), puis marche sur les trois boutons.

> Ce cours commence par établir la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure de la mesure.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


### Les trois budgets

```mermaid
flowchart LR
    M["Model"] --> LAT["Latency<br/>ms per image"]
    M --> MEM["Memory<br/>peak MB"]
    M --> PWR["Power<br/>mJ per inference"]

    LAT --> SHIP["Ship / no-ship<br/>decision"]
    MEM --> SHIP
    PWR --> SHIP

    style LAT fill:#fecaca,stroke:#dc2626
    style MEM fill:#fef3c7,stroke:#d97706
    style PWR fill:#dbeafe,stroke:#2563eb
```

- **Latency**La moyenne de seulement p50 cache le comportement de la queue qui compte pour les systèmes en temps réel.
  Le mot grec traduit par " le mot grec "**延迟**Le nombre de points de vue de la valeur moyenne est supérieur à la valeur moyenne de la valeur moyenne.
- **Peak memory**Le nombre de détecteurs de données est le maximum que le dispositif peut voir, pas la moyenne en état d'arrêt.
  Le mot grec traduit par " le mot grec "**峰值内存**La valeur maximale de l'appareil est la valeur moyenne stable.
- **Power / energy**Le nombre de périphériques de traitement de la CPU/GPU est souvent calculé par temps d'utilisation.
  Le mot grec traduit par " le mot grec "**功耗/能量**Le nombre de millifocus par seconde sur les appareils de distribution électrique est généralement le taux d'utilisation du processeur / GPU × temps à approximation.

Une table de (modèle, latence, mémoire, précision) est ce à partir duquel une décision de bord est prise.

> Le tableau de la mise en œuvre de la mise en œuvre de la décision est basé sur un modèle (模型, 延迟, 内存, 精度).

### Discipline de mesure

Trois règles que chaque profil de bord doit suivre:

> Chaque analyse de performance de bord doit être suivie de trois règles:

1. **Warm up**Le modèle avec 5 à 10 dépassages avant la mesure.
   Le mot grec traduit par " le mot grec "**预热** mesure préuse 5-10 fois virtuelle pré-directionnelle pré-chauffement modèle。 cold缓存和 JIT 编译会产生不代表性的初始数据。
2. **Synchronise**Charges de travail de GPU avec `torch.cuda.synchronize()`Sans cela, vous mesurez le déploiement du noyau, pas l'exécution du noyau.
   Le mot grec traduit par " le mot grec "**同步** dans le compte-temps`torch.cuda.synchronize()`Dans ce cas, vous mesurez la régulation de la CPU, pas l'exécution de celle-ci.
3. **Fix input sizes**La latence sur 224x224 n'est pas la latence sur 512x512.
   Le mot grec traduit par " le mot grec "**固定输入尺寸** utilisation de la résolution de production── 224x224                                                                                                                                                                                                                                                       

### Les FLOPs en tant que délégué

Les FLOPs (opérations de points flottants par inférence) sont un proxy bon marché, indépendant des appareils pour la latence. Utilisé pour la comparaison d'architecture, trompeur comme une horloge murale absolue. Un modèle avec 10% de plus de FLOPs peut être 2 fois plus rapide en pratique car il utilise des options conviviales avec le matériel (des convs en profondeur compilent bien, les grands convs 7x7 ne le font pas).

> Les FLOPs (en anglais: FLOPs) sont un indicateur de retard de fonctionnement peu coûteux, sans aucun lien avec les appareils. Ils sont utilisés dans la comparaison des structures, mais ils sont très mal conçus.

Règle: utiliser les FLOP pour la recherche d'architecture, utiliser la latence sur l'appareil pour les décisions de déploiement.

> Le principe: faire des recherches d'architecture à l'aide de FLOP, prendre des décisions de déploiement avec un retard sur l'appareil.

### Quantification dans un paragraphe

Remplacez les poids et les activations de FP32 par INT8. La taille du modèle diminue de 4 fois, la bande passante de la mémoire diminue de 4 fois, le calcul diminue de 2 à 4 fois sur le matériel qui a des noyaux INT8 (tous les SoC mobiles modernes, tous les GPU NVIDIA avec des cores tensors).

> Le modèle de taille réduit de 4 fois, la bande passante de mémoire réduit de 4 fois, le volume de calcul sur le matériel interne de l'INT8 réduit de 2 à 4 fois.

Les types:

> 类型:

- **Dynamic** poids quantique à INT8, activations calculées en FP.
  Le mot grec traduit par " le mot grec "**动态** Pesourage de puissance pour INT8, valeur activée en FP 计算──简单,加速有限──
- **Static (post-training)** Poids quantique + activation de calibration sur un petit ensemble de calibration.
  Le mot grec traduit par " le mot grec "**静态（训练后）**量化权重 + 在小校准集上校准激活范围──比动态快得多──
- **Quantisation-aware training (QAT)** simuler la quantification pendant la formation afin que le modèle apprenne autour de lui.
  Le mot grec traduit par " le mot grec "**量化感知训练（QAT）** formation en mode de mesure, faire adaptation  précision optimale, besoin de marquer les données 

Pour la vision, la quantification statique post-entraînement donne 95% des avantages avec 5% de l'effort.

> Pour les tâches visuelles, l'utilisation de QAT est inacceptable lorsque le PTQ perd son équivoque.

### Élagage et distillation

- **Pruning** supprimer des poids non importants (à partir de la taille) ou des canaux (structurés).
  Le mot grec traduit par " le mot grec "**剪枝** Le déplacement de poids non important (en fonction de la longueur) ou du passage (en fonction de la structure)  est bon pour le modèle de paramétrage; il n'est pas grand pour les structures déjà très étroites.
- **Distillation** former un petit élève à imiter les logites d'un grand professeur.
  Le mot grec traduit par " le mot grec "**蒸馏** training小模型 (en français: training小模型)  student) 模仿大模型 (en français: grande modèle)  teacher (en français: maître)  logits  训练小模型 (en français: formation) 学生) 模仿大模型 (en français: grande modèle)  师)  师)  师的逻辑──通常能恢复缩小模型损失的大部分精度──生产级边缘模型的标准做法──

### Les délais de fonctionnement des déductions

- **PyTorch eager** lent, pas pour déploiement.
  Le mot grec traduit par " le mot grec "**PyTorch eager**慢, pas utilisé pour la déploiement―
- **TorchScript** héritage. Supplémenté par `torch.compile`et l'exportation de ONNX.
  Le mot grec traduit par " le mot grec "**TorchScript**遗留方案──已被 `torch.compile`Et le nombre de personnes qui ont été arrêtées est de plus en plus élevé.
- **ONNX Runtime**Le CPU, CUDA, CoreML, TensorRT, OpenVINO ont tous des fournisseurs ONNX.
  Le mot grec traduit par " le mot grec "**ONNX Runtime**中性运行时──CPU、CUDA、CoreML、TensorRT、OpenVINO ont tous des fournisseurs ∞
- **TensorRT** Compileur de NVIDIA. La meilleure latence sur les GPU NVIDIA (station de travail et Jetson). Intégre avec ONNX Runtime ou standalone.
  Le mot grec traduit par " le mot grec "**TensorRT**NVIDIA 的编译器──在 NVIDIA GPU(工作站和 Jetson) 上延迟最低──
- **Core ML** Temps d'exécution d'Apple pour iOS/macOS.`.mlmodel`ou `.mlpackage`- Je suis désolé .
  Le mot grec traduit par " le mot grec "**Core ML**Apple iOS/macOS 运行时──需要 `.mlmodel`Ou `.mlpackage`Il y a une autre.
- **TFLite** Temps d'exécution de Google pour Android/ARM.`.tflite`- Je suis désolé .
  Le mot grec traduit par " le mot grec "**TFLite**Google Android/ARM 运行时──需要 `.tflite`Il y a une autre.
- **OpenVINO** Temps d'exécution de l'Intel pour le processeur/VPU.`.xml`+ `.bin`- Je suis désolé .
  Le mot grec traduit par " le mot grec "**OpenVINO**Intel's CPU/VPU 运行时──需要 `.xml`+ `.bin`Il y a une autre.

Dans la pratique: export PyTorch -> ONNX -> choisir le temps de fonctionnement de la cible.

> 实践中:导出 PyTorch -> ONNX -> 选择目标运行时。ONNX 是通用语言。

### Prise en charge de l'architecture de bord

| Budget | Model | Why |
|--------|-------|-----|
| < 3M params | MobileNetV3-Small | Compiles everywhere, good baseline |
| 3-10M | EfficientNet-Lite-B0 | Best accuracy per param on TFLite |
| 10-20M | ConvNeXt-Tiny | Best accuracy-per-param, CPU-friendly |
| 20-30M | MobileViT-S or EfficientViT | Transformer with ImageNet accuracy |
| 30-80M | Swin-V2-Tiny | If stack supports window attention |

Quantisez tous ces éléments à l'INT8 à moins d'avoir une raison spécifique de ne pas le faire.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：工业部署中的视觉系统】**Dans le cadre de la déploiement industriel réel, les modèles visuels doivent prendre en compte la réflexion sur la différence de taille des modèles, l'adaptation des appareils de bord, etc. TensorRT, ONNX Runtime, OpenVINO sont des outils d'accélération de réflexion courants. Les systèmes de conduite autonome (comme Tesla FSD) utilisent généralement plusieurs modèles visuels en temps réel sur les puces de véhicule.

> **【拓展：数据标注与质量】**L'efficacité des tâches visuelles dépend fortement de la qualité des données de marquage. Le Studio de marquage, CVAT, est l'outil de marquage principal. Dans le monde industriel, l'apprentissage actif peut réduire le coût de marquage.




## Construisez-le et mettez-le en œuvre.
```figure
cnn-param-count
```

## Faites-le

### Étape 1: Mesurer correctement la latence

```python
import time
import torch

def measure_latency(model, input_shape, device="cpu", warmup=10, iters=50):
    model = model.to(device).eval()
    x = torch.randn(input_shape, device=device)
    with torch.no_grad():
        for _ in range(warmup):
            model(x)
        if device == "cuda":
            torch.cuda.synchronize()
        times = []
        for _ in range(iters):
            if device == "cuda":
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            model(x)
            if device == "cuda":
                torch.cuda.synchronize()
            times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    return {
        "p50_ms": times[len(times) // 2],
        "p95_ms": times[int(len(times) * 0.95)],
        "p99_ms": times[int(len(times) * 0.99)],
        "mean_ms": sum(times) / len(times),
    }
```

Réchauffement, synchronisation, utilisation `time.perf_counter()`- Rapporte des percentiles, pas seulement des médiums.

> 预热、同步、使用 `time.perf_counter()`                                                                                                                                                                                                                                                              

### Étape 2: Counts de paramètres et de FLOP

```python
def parameter_count(model):
    return sum(p.numel() for p in model.parameters())

def flops_estimate(model, input_shape):
    """
    Rough FLOP count for a conv/linear-only model. For production use `fvcore` or `ptflops`.
    """
    total = 0
    def conv_hook(m, inp, out):
        nonlocal total
        c_out, c_in, kh, kw = m.weight.shape
        h, w = out.shape[-2:]
        total += 2 * c_in * c_out * kh * kw * h * w
    def linear_hook(m, inp, out):
        nonlocal total
        total += 2 * m.in_features * m.out_features
    hooks = []
    for m in model.modules():
        if isinstance(m, torch.nn.Conv2d):
            hooks.append(m.register_forward_hook(conv_hook))
        elif isinstance(m, torch.nn.Linear):
            hooks.append(m.register_forward_hook(linear_hook))
    model.eval()
    with torch.no_grad():
        model(torch.randn(input_shape))
    for h in hooks:
        h.remove()
    return total
```

Pour des projets réels `fvcore.nn.FlopCountAnalysis`ou `ptflops`; ils gèrent correctement chaque type de module.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `fvcore.nn.FlopCountAnalysis`Ou `ptflops`Ils peuvent correctement traiter chaque type de module.

### Étape 3: Quantification statique après l'entraînement

```python
def quantise_ptq(model, calibration_loader, backend="x86"):
    import torch.ao.quantization as tq
    model = model.eval().cpu()
    model.qconfig = tq.get_default_qconfig(backend)
    tq.prepare(model, inplace=True)
    with torch.no_grad():
        for x, _ in calibration_loader:
            model(x)
    tq.convert(model, inplace=True)
    return model
```

Trois étapes: configurer, préparer (insérer des observateurs), calibrer avec des données réelles, convertir (fuse + quantize).`Conv -> BN -> ReLU`- Je suis là.`ConvBnReLU`), qui `torch.ao.quantization.fuse_modules`Les poignées.

> 3 étapes: configuration, préparation, insertion dans l'observateur, utilisation de données réelles, conversion, fusion, quantification,`Conv -> BN -> ReLU`- Je suis là.`ConvBnReLU`),`torch.ao.quantization.fuse_modules`- Je vais le faire.

### Étape 4: Exporter à ONNX

```python
def export_onnx(model, sample_input, path="model.onnx"):
    model = model.eval()
    torch.onnx.export(
        model,
        sample_input,
        path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
        opset_version=17,
    )
    return path
```

`opset_version=17`est le défaut de sécurité en 2026. `dynamic_axes`vous permet d'exécuter le modèle ONNX avec une taille de lot arbitraire.

> `opset_version=17`C'est la sécurité de l'année 2026:`dynamic_axes`允许 ONNX 模型以任意批量大小运行──

### Étape 5: Indiquer et comparer les régimes

```python
import torch.nn as nn
from torchvision.models import mobilenet_v3_small

def compare_regimes():
    model = mobilenet_v3_small(weights=None, num_classes=10)
    params = parameter_count(model)
    flops = flops_estimate(model, (1, 3, 224, 224))
    lat_fp32 = measure_latency(model, (1, 3, 224, 224), device="cpu")
    print(f"FP32 MobileNetV3-Small: {params:,} params  {flops/1e9:.2f} GFLOPs  "
          f"p50={lat_fp32['p50_ms']:.2f}ms  p95={lat_fp32['p95_ms']:.2f}ms")
```

Exécutez la même fonction pour `resnet50`- Je suis là .`efficientnet_v2_s`, et `convnext_tiny`et vous avez la table de comparaison dont vous avez besoin pour une décision de déploiement.

> Pour le`resnet50`- Je suis là.`efficientnet_v2_s`et `convnext_tiny`运行相同函数, vous avez obtenu le rapport nécessaire à la décision de déploiement.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：视觉模型的持续学习】**Dans un environnement de production, le modèle visuel doit être en constante évolution pour s'adapter à de nouveaux données. La technologie de l'apprentissage continu permet d'éviter que le modèle s'adapte à de nouvelles données et oublie les anciens connaissances.

## Utilisez-le avec le cadre de réalisation

Les piles de production convergent sur l'une des trois voies suivantes:

- **Web / serverless**PyTorch -> ONNX -> ONNX Runtime (fournisseur de CPU ou CUDA).
- **NVIDIA edge (Jetson, GPU server)**La plus grande latence, le plus grand effort d'ingénierie.
- **Mobile**: PyTorch -> ONNX -> Core ML (iOS) ou TFLite (Android).

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


Pour la mesure, `torch-tb-profiler`- Je suis là .`nvprof`- Je suis là .`nsys`, et les instruments sur macOS donnent des pannes couche par couche. `benchmark_app`(OpenVINO) et `trtexec`(TensorRT) donner des numéros CLI indépendants.



## Envoyez-le . Produit .

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──


Cette leçon donne:

- `outputs/prompt-edge-deployment-planner.md` une requête qui choisit la colonne vertébrale, la stratégie de quantification et le temps d'exécution donné à l'appareil cible et à la latence SLA.
- `outputs/skill-latency-profiler.md` une compétence qui écrit un script complet de marquage de latence avec réchauffement, synchronisation, percentiles et suivi de la mémoire.

## Les exercices

1. **(Easy)**Mesurer la latence p50 pour `resnet18`- Je suis là .`mobilenet_v3_small`- Je suis là .`efficientnet_v2_s`, et `convnext_tiny`Rapportez la table et identifiez quelle architecture a la meilleure précision par ms.
2. **(Medium)**Appliquer une quantification statique post-entraînement à `mobilenet_v3_small`. Rapporte la perte de latence et de précision FP32 vs INT8 sur un sous-ensemble de CIFAR-10 ou similaire détenu.
3. **(Hard)**Export `convnext_tiny`À ONNX, passez-le par là.`onnxruntime`avec le `CPUExecutionProvider`, et comparer la latence à la ligne de base PyTorch enthousiaste. Identifier la première couche où ONNX Runtime est plus rapide et expliquer pourquoi.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Latency | "How fast" | Time from input to output; p50/p95/p99 percentiles, not mean |
| FLOPs | "Model size" | Floating-point ops per forward pass; rough proxy for compute cost |
| INT8 quantisation | "8-bit" | Replace FP32 weights/activations with 8-bit integers; ~4x smaller, 2-4x faster |
| PTQ | "Post-training quantisation" | Quantise a trained model without retraining; easy, usually enough |
| QAT | "Quantisation-aware training" | Simulate quantisation during training; best accuracy, requires labelled data |
| ONNX | "The neutral format" | Model exchange format supported by every mainstream inference runtime |
| TensorRT | "NVIDIA compiler" | Compiles ONNX into an optimised engine for NVIDIA GPUs |
| Distillation | "Teacher -> student" | Train a small model to mimic a big model's logits; recovers most lost accuracy |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [EfficientNet (Tan & Le, 2019)](https://arxiv.org/abs/1905.11946) Écalement composé pour des architectures efficaces
- [MobileNetV3 (Howard et al., 2019)](https://arxiv.org/abs/1905.02244) architecture mobile-first avec h-swish et squeeze-excite
- [A Practical Guide to TensorRT Optimization (NVIDIA)](https://developer.nvidia.com/blog/accelerating-model-inference-with-tensorrt-tips-and-best-practices-for-pytorch-users/) comment obtenir réellement les chiffres de débit dans le papier
- [ONNX Runtime docs](https://onnxruntime.ai/docs/) quantification, optimisation des graphiques, sélection des fournisseurs
