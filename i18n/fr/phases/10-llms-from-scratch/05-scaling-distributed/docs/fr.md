# Échantillonnage: Formation distribuée, FSDP, DeepSpeed

> Votre modèle 124M a été formé sur un GPU. Maintenant essayez 7 milliards de paramètres. Le modèle ne s'adapte pas à la mémoire. Les données prennent des semaines sur une seule machine.

> **【中文解读】**1,24 milliard de modèles sont formés sur un seul GPU. Mais 70 milliards de modèles par paramètres ne sont pas disponibles, et un seul train de données nécessite plusieurs semaines.

> **【拓展：DeepSeek-V3的2048卡训练】**DeepSeek-V3 utilise 2048 张 H800 GPU entraînement, adoption DualPipe 流水线并行 + MoE 专家并行;; compréhension de la formation distribuée est la base de la compréhension de la façon dont le modèle de grande taille est entraîné.

>  **【前置】**Je suis en train de faire une première séance de formation en ligne avec le groupe de travail de la formation.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 04 (Pre-Training a Mini GPT)
**Time:** ~120 minutes

>  **【类比】**Le travail de plusieurs personnes pour déplacer une grande boîte.**数据并行**(DP) = 4 personnes déplacent chacun un même petit boîtier avec différents modèles, résultats AllReduce average)**张量并行**(TP) = 4 personnes portent ensemble un gros coffret de quatre côtés de la même couche de 4 carrés)**流水线并行**(PP) = 4 个人流水线,第 1 人搬一层传给第二 人(模型按层切分)**FSDP**= DP + 把模型切片分到各卡,用时再聚聚合 (省显存) ⋅ production场景一般 3种组合用 (三维对行) ⋅

> ️ **【易错点】**3 cratères de formation:**batch size 设错**单卡 bs=8,4 卡应该 bs=32(4×8)而非 bs=8; utiliser la taille effective du lot 计算 lr―(2) **AllReduce 瓶颈**卡间通信比GPU 计算慢10倍,bs 太小会让GPU等通信;bs 至少32+才划算──(3) **没设 seed** chaque démarrage est différent, les résultats sont irréalisables;`torch.manual_seed(42) + torch.cuda.manual_seed_all(42)`Il y a une autre.

## Objectifs d'apprentissage

- Expliquer les trois types de parallélisme (données, tensor, pipeline) et quand chacun est nécessaire en fonction du modèle et de la taille du cluster
  解释三种并行类型(数据并行、张量并行、流水线并行) et sa scène d'utilisation
- Implémenter une formation parallèle des données à l'aide de PyTorch DDP avec synchronisation des gradients sur plusieurs GPU
  Utilisation PyTorch DDP  réaliser plusieurs GPU données并行训练和梯度同步
- Calculer le budget de mémoire pour une taille de modèle donnée (poids + états d'optimisation + gradients + activations) pour déterminer le minimum de matériel
  计算给定模型大小的显存预算(权重 + 优化器状态 + 梯度 + 激活值), déterminer le besoin minimum de matériel
- Configurer les étapes FSDP ou DeepSpeed ZeRO pour fragmenter les états du modèle sur les GPU et les modèles de compatibilité qui dépassent la mémoire GPU unique
  Configurer le FSDP ou la phase de ZeRO à la phase de la phase de la phase de la phase de la phase de la phase de la phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de phase de

> **【中文解读】**Le programme de formation de l'LLM est basé sur la méthode de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation

## Le problème , l' introduction du problème

Un modèle de paramètre 7B dans FP16 a besoin de 14 Go juste pour les poids. Adam optimisateur stocke deux copies supplémentaires de chaque paramètre (estimation du premier et du deuxième moment). C'est un autre 28 Go. Gradients pendant la propagation arrière ajouter 14 Go de plus. Vous êtes à 56 Go avant qu'une seule activation est stockée.

> Le modèle de paramètres 7B est en FP16 en bas de l'échelle de charge et nécessite 14 Go. Adam  Optimisateur pour chaque paramètre de stockage extra deux copies de stockage (estimation du premier et du second étage), nécessite également 28 Go.

Une NVIDIA A100 a 80 Go de mémoire.

> NVIDIA A100 avec 80 Go de stockage.

56 Go sur 80 Go consommé. Cela laisse 24 Go pour les activations - les valeurs intermédiaires calculées pendant le passage vers l'avant qui doivent être maintenues en vie pour la propagation vers l'arrière. Pour une séquence de 2048 jetons avec un modèle 4096 dimensions, les activations d'une seule couche utilisent environ 64 Go. Avec 32 couches, vous avez besoin de 2 Go par échantillon. Une taille de lot de 8 nécessite 16 Go. Vous avez 24 Go. Une taille de lot de 12 explose.

> Le reste de 24 Go est utilisé pour la valeur active  avant de se propager dans le calcul de la valeur moyenne, doit être conservé pour la propagation inverse  Pour les séquences de jetons 2048 et les modèles 4096 维, la valeur active de couche unique est d'environ 64 MB── 32 niveaux nécessitent un échantillon de 2 GB── la taille de la série 8 需要 16 GB── vous avez 24 GB── la taille de la série 12                                                                                                                                                                                                          

Maintenant essayez les paramètres 70B. Poids seuls: 140 Go en FP16. Ne pas monter sur un GPU. Vous avez besoin d'au moins 2 A100 (2 x 80 Go = 160 Go) juste pour tenir les poids. Ajoutez des états d'optimisation et des gradients et vous avez besoin de beaucoup plus: 3+ GPU minimum, et réaliste 8-16 selon la stratégie de fragmentation.

> 现在试试 70B 参数――仅权重:FP16 下 140GB──放不进一张GPU──至少需要2张A100(2 x 80GB = 160GB)才能放下权重──加上优化器状态和梯度,需要更多:最少3+张GPU,实际需要8-16张,取决于分片策略──

Llama 3 405B a été entraîné sur 16 384 GPU NVIDIA H100.$100 million in compute. DeepSeek V3 trained a comparable model for roughly $5,6 millions en étant intelligents sur l'architecture (Mixure d'experts signifie seulement une fraction des paramètres activés par jeton) et l'efficacité de la formation.

> Llama 3 405B a été utilisé pour la formation de 16 384 张 NVIDIA H100 GPU, le coût de calcul estimé à environ 1 milliard de dollars.

Cette leçon couvre les quatre stratégies qui permettent de former à grande échelle: le parallélisme des données, le parallélisme tensor, le parallélisme des pipelines et le parallélisme des données complètement fragmentées. Vous simulerez chacune d'elles en Python pur pour comprendre la mécanique avant de toucher un cadre de formation distribué.

> Cette formation couvre quatre stratégies possibles pour un entraînement à grande échelle: données et flux, flux et flux de données. Vous allez comprendre le mécanisme de chaque entraînement en utilisant Python purement et simplement, avant de commencer à utiliser un cadre de formation distribué.

## Le concept de base.

### Pourquoi la distribution est nécessaire

Voici les mathématiques de la mémoire pour les modèles réels.

> Voici les calculs mathématiques de l'expression du modèle réel. Chaque chiffre est calculé, pas une estimation.

| Model | Params | Weights (FP16) | Adam States | Gradients (FP16) | Total (no activations) |
|-------|--------|----------------|-------------|------------------|----------------------|
| GPT-2 Small | 124M | 248 MB | 992 MB | 248 MB | 1.5 GB |
| Llama 3 8B | 8B | 16 GB | 64 GB | 16 GB | 96 GB |
| Llama 3 70B | 70B | 140 GB | 560 GB | 140 GB | 840 GB |
| Llama 3 405B | 405B | 810 GB | 3,240 GB | 810 GB | 4,860 GB |

La colonne "Adam States" est le tueur. Adam stocke une moyenne en cours d'exécution (m) et une variance en cours d'exécution (v) pour chaque paramètre, à la fois dans FP32. Pour un modèle 70B, c'est 70B x 4 octets x 2 = 560 Go. L'optimisateur seul a besoin de sept A100.

> "Adam 状态"列是致命的──Adam pour chaque paramètre de stockage une moyenne de fonctionnement(m) et une différence de fonctionnement(v), sont FP32── Pour le modèle 70B, c'est-à-dire 70B x 4 字节 x 2 = 560GB──on a besoin de sept décodeurs A100──

Un seul H100 a 80 Go. Llama 3 405B a besoin d'au moins 61 H100 pour maintenir les poids, l'optimisateur et les gradients. Ajoutez des activations et le nombre augmente encore. Meta a utilisé 16 384 GPU non parce qu'ils voulaient - parce qu'ils devaient.

> 单张H100 有80GB──Llama 3 405B 至少需要61张H100 才能放置权重、优化器和梯度──加上激活值数字更大──Meta 使用16384张GPU 不是因为他们想而因为他们必须──

> **【中文解读】**显存预算是LLM 训练的第一道关卡──以Llama 3 70B为例:FP16 权重140GB + Adam 优化器状态560GB +梯度140GB = 840GB(不含激活值)──单张H100 只有80GB,至少需要11张GPU才能放下这些状态──Llama 3 405B 的总需求高达4,860GB──Adam 优化器是显存杀手它为每个参数存储两个FP32 的动量估计节量m和v),参数 x 8 字 x 2──

> **【拓展：Llama 3 的 16384 GPU 训练】**Llama 3 405B a été formé sur 16 384 张 H100 GPU, avec des lignes de données 3D et de lignes de données + 张量并行 + 流水线并行) ⋅ un coût total d'entraînement estimé à environ 1 milliard de dollars.

### Parallélisme des données

La stratégie distribuée la plus simple. Copiez l'ensemble du modèle en N GPU. Divisez chaque lot d'entraînement en N parties égales. Chaque GPU effectue un passage vers l'avant et vers l'arrière sur son fragment de données. Après le passage vers l'arrière, faites la moyenne des gradients sur tous les GPU. Chaque GPU met à jour sa copie des poids avec les mêmes gradients moyens, en gardant toutes les copies en synchronisation.

> Le plus simple est de répartir le modèle entier en N 张 GPU. Chaque entraînement se décompose en N 等份. Chaque GPU se décompose en deux parties.

**The good:**L'échelle de débit linéaire. N GPUs traiter N fois plus de données par étape. La communication est limitée à la moyenne de gradient, qui se chevauchent avec le calcul.

> **优点：**吞吐量线性扩展──N 张 GPU Chaque étape de traitement N 倍的数据──通信仅限于梯度平均,可与计算重叠──

**The bad:**Chaque GPU contient une copie complète du modèle, des états d'optimisation et des gradients. Pour un modèle 70B, chaque GPU a besoin de 840 Go. Le parallélisme des données ne réduit rien à la mémoire par GPU.

> **缺点：**Chaque GPU possède un modèle, une copie complète de l'état et de la température de l'optimisateur. Pour le modèle 70B, chaque GPU a besoin de 840 Go.

**The math:**La taille de lot efficace = par_gpu_batch_size x N. Pour N=64 GPU avec par-GPU lot de 16, le lot efficace est de 1.024. Llama 3 a utilisé une taille de lot efficace de 16 millions de jetons par étape.

> **数学：**Pour N = 64 张 GPU, par GPU 批量 16,有效批量为 1,024 拉玛 3 使用每步16000000代币的有效批量──

```mermaid
graph TD
    subgraph DataParallel["Data Parallelism (N=4 GPUs)"]
        B["Full Batch\n(1024 samples)"] --> S["Split"]
        S --> G1["GPU 1\nFull Model Copy\n256 samples"]
        S --> G2["GPU 2\nFull Model Copy\n256 samples"]
        S --> G3["GPU 3\nFull Model Copy\n256 samples"]
        S --> G4["GPU 4\nFull Model Copy\n256 samples"]
        G1 --> AR["AllReduce\nAverage Gradients"]
        G2 --> AR
        G3 --> AR
        G4 --> AR
        AR --> U["Update\n(identical on all GPUs)"]
    end

    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style G1 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G3 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G4 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style AR fill:#1a1a2e,stroke:#51cf66,color:#fff
    style U fill:#1a1a2e,stroke:#51cf66,color:#fff
```

### Parallélisme des tensors

Divisez les couches individuelles entre les GPU. Une seule multiplication de matrice est divisée entre les GPU, chaque partie de calcul du résultat.

> Une fois que la matrice multiplie est distribuée à plusieurs GPU, chaque partie de calcul en résulte.

Considérez une matrice de poids de forme (8192, 8192) dans une couche de flux. Avec un parallélisme tensor à quatre voies, chaque GPU contient une tranche (8192, 2048). Chaque GPU multiplie l'entrée par sa tranche, produisant un résultat partiel. Les résultats partiels sont combinés (via all-reduce ou all-gather) pour produire la sortie complète.

> 考虑前层中形状为 (8192, 8192) 的权重矩阵──使用4路张量并行,每张GPU 持有的分片 (8192, 2048) 的分片──每张GPU 将输入乘以其分片,产生部分结果──部分结果通过全归约或全收集组合为完整输出──

**The good:**Réduit la mémoire par GPU pour les poids du modèle. Un modèle 70B divisé en 8 GPU signifie que chaque GPU contient des poids d'environ 8,75B.

> **优点：** Reducer le poids du modèle par GPU 显存──70B 模型 分裂到8 张 GPU

**The bad:**Il nécessite une communication inter-GPU rapide après chaque couche. Le tout-réduire après chaque matmul ajoute une latence. Cela fonctionne bien avec NVLink (900 GB / s entre les GPU sur le même nœud) mais mal entre les nœuds connectés par InfiniBand (400 Gb / s, environ 50 GB / s).

> **缺点：**Chaque niveau nécessite une GPU rapide 间通信。 chaque fois que la fréquence multiplie, la fréquence de connexion augmente lentement。 ce qui est très efficace avec la GPU de l'élément NVLink 间 900 GB/s, mais avec la connexion InfiniBand ∞ 400 Gb/s, environ 50 GB/s.

**Real usage:**Megatron-LM a été le pionnier du parallélisme tensoriel. Llama 3 405B utilise un parallélisme tensoriel à 8 voies dans chaque nœud.

> **实际使用：**Megatron-LM a d'abord proposé une mise en œuvre de la quantité de chargement.

> **【中文解读】**张量并行(Tensor Parallelism) va décomposer une seule couche de la matrice en plusieurs GPUs. Par exemple, une (8192, 8192) de la matrice de poids est en 4 路并行下, chaque GPU n'a besoin que de la partie de stockage (8192, 2048). Mais le manque est que chaque couche a besoin de toute la communication, donc elle est presque limitée à la seule connexion NVLink 单节内(8 张 GPU) ⋅Llama 3 405B utilise 8 路张量并行.

> **【拓展：流水线并行的气泡问题】**Le modèle est distribué par couche sur différents GPUs, comme GPU1 1 à 8 couches, GPU2 9 à 16 couches. Mais il se produit une "bouffée" de GPU.

### Parallélisme du pipeline

Le GPU 1 exécute les couches 1-8. Le GPU 2 exécute les couches 9-16. Le GPU 3 exécute les couches 17-24. Le GPU 4 exécute les couches 25-32. Les données circulent dans le pipeline: le GPU 1 calcule ses couches et envoie des activations au GPU 2, qui calcule ses couches et envoie au GPU 3, et ainsi de suite.

> 按层拆分模型。GPU 1 跑 1-8层。GPU 2 跑 9-16层。GPU 3 跑 17-24层。GPU 4 跑 25-32层。Data流过流水线:GPU 1 计算其层并将激活值发送给 GPU 2,GPU 2 计算其层并发送给 GPU 3,以此类推──

**The good:**La communication minimale entre les GPU -- juste les activations aux limites de couches, qui sont petites par rapport aux gradients ou aux poids. Fonctionne sur les nœuds parce que les exigences en bande passante sont faibles.

> **优点：**La GPU 间通信最小 est la seule valeur activée de la limite de niveau, très petite par rapport au gradient ou au poids.

**The bad:**Les GPU 4 sont inactifs (ils ont déjà redirigé leur partie). Pendant le passage arrière, le schéma s'inverse. Avec une pipeline naïve, l'utilisation de la GPU est seulement 1/N pour les étapes de pipeline N.

> **缺点：**流水线气泡── lorsque la GPU 4 dans le calcul de la première propagation de la première partie de la série 1, la GPU 1、2、3 空(elles ont déjà terminé leur propre partie)──反向传播时模式相反──朴素流水线下, N 个阶段 GPU utilisation taux est seulement de 1/N──

**GPipe and PipeDream**Résoudre le problème de la bulle en divisant le lot en micro-parties. GPU 1 démarre sur micro-partie 2 dès qu'il termine de transmettre micro-partie 1. Ce comptage se chevauchera sur les étapes du pipeline. Avec M micro-parties et N étapes, la fraction de bulle tombe à (N-1) / M. Utilisez M = 16 micro-parties avec N = 4 étapes et la bulle est 3/16 = 18,75% temps de temps d'arrêt.

> **GPipe 和 PipeDream**通過將批次分為微批次來解決氣泡問題──GPU 1 一完成微批次 1 的前向传播就開始微批次 2──這在流水线阶段间重叠计算──M 个微批次和N 个阶段,氣泡比例降至 (N-1) /M──使用M=16 个微批次和N=4 个阶段,气泡为3/16 = 18.75% 空时间──

### FSDP: données parallèles entièrement fragmentées

FSDP combine l'évolutivité du parallélisme des données avec l'efficacité de la mémoire du sharding. Au lieu de chaque GPU contenant une copie complète du modèle, chaque GPU ne contient que 1/N des paramètres, des gradients et des états d'optimisation.

> Le FSDP combine l'expansionnalité et l'efficacité de la mise en cache des parallèles de données. Chaque GPU ne possède pas une copie complète du modèle, mais seulement un paramètre, une gradience et un état d'optimisateur de 1/N.

Avant le passage vers l'avant d'une couche, le FSDP exécute un **all-gather**Pour collecter les paramètres complets de tous les GPU dans la mémoire de chaque GPU. Après le passage vers l'avant, chaque GPU rejette les paramètres non locaux. Pendant le retrait, le tout-ensemble se déroule à nouveau pour reconstruire les paramètres pour le calcul des gradients. Après le passage vers l'arrière, un **reduce-scatter**distribue des fragments de gradients de sorte que chaque GPU ne stocke que 1/N des gradients.

> Avant la propagation de la première couche, le FSDP a effectué l'ensemble des opérations de collecte, allant de la collecte des paramètres complets de tous les GPU à la mise en cache de chaque GPU. Après la propagation de la première, chaque GPU a abandonné les paramètres non natifs.

**The math for a 70B model on 8 GPUs:**

| Component | Without FSDP | With FSDP |
|-----------|-------------|-----------|
| Weights (FP16) | 140 GB per GPU | 17.5 GB per GPU |
| Adam States (FP32) | 560 GB per GPU | 70 GB per GPU |
| Gradients (FP16) | 140 GB per GPU | 17.5 GB per GPU |
| **Total** | **840 GB per GPU** | **105 GB per GPU** |

Sans FSDP, vous ne pouvez pas installer un modèle 70B sur un seul GPU de 80 Go. Avec FSDP sur 8 GPU, chaque GPU utilise 105 Go - attendez, cela ne convient toujours pas. Vous avez besoin d'au moins 16 GPU pour atteindre 80 Go par GPU, ou vous combinez FSDP avec le contrôle d'activation (recomptez les activations en arrière au lieu de les stocker).

> 没有FSDP,70B 模型不能放入单张80GB GPU──使用FSDP在8张 GPU上,每张 GPU使用105GB等等,还是放不下──你需要至少16张 GPU 才能降至每卡80GB以下,或将FSDP与激活检查点结合(反向传播时重新计算激活值而不是存储它们)──

Le coût de la communication est plus élevé que le parallélisme des données vanille en raison de la collecte avant chaque couche.

> Le coût de la communication est plus élevé que le coût de la mise en œuvre ordinaire des données, car chaque niveau nécessite une collecte complète avant la mise en œuvre.

> **【中文解读】**FSDP(partie de données complète et étroite) est une combinaison de données et de fractions de données. Chaque GPU ne stocke que les paramètres 1/N de la taille et de l'état de l'optimisateur.

> **【拓展：DeepSpeed ZeRO 的三个阶段】**La phase 1 de ZeRO est la phase 2 de la phase 3 de la phase 3 de ZeRO. La phase 3 de ZeRO est la phase 3 de la phase 3 de la phase 3 de la phase 3 de ZeRO.

```mermaid
graph TD
    subgraph FSDP["FSDP: Fully Sharded Data Parallel (4 GPUs)"]
        direction TB
        S["Model: 4 layers, sharded"]

        subgraph GPU1["GPU 1"]
            G1S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU2["GPU 2"]
            G2S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU3["GPU 3"]
            G3S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU4["GPU 4"]
            G4S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end

        AG["All-Gather\n(reconstruct full params\nbefore each layer)"]
        FW["Forward Pass\n(full params temporarily)"]
        RS["Reduce-Scatter\n(distribute gradient shards\nafter backward)"]

        S --> GPU1
        S --> GPU2
        S --> GPU3
        S --> GPU4
        GPU1 --> AG
        GPU2 --> AG
        GPU3 --> AG
        GPU4 --> AG
        AG --> FW
        FW --> RS
    end

    style G1S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G3S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G4S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style AG fill:#1a1a2e,stroke:#e94560,color:#fff
    style FW fill:#1a1a2e,stroke:#51cf66,color:#fff
    style RS fill:#1a1a2e,stroke:#e94560,color:#fff
```

### ZERO à haute vitesse

Le ZeRO (Zero Redundancy Optimizer) de DeepSpeed est conceptuellement identique à FSDP mais a été développé indépendamment par Microsoft.

> ZeRO de DeepSpeed est conceptuellement similaire à FSDP, mais développé indépendamment par Microsoft. Il définit trois phases, chaque phase étant plus active:

| Stage | Shards | Memory Savings | Communication |
|-------|--------|---------------|---------------|
| ZeRO-1 | Optimizer states only | ~4x reduction | Same as data parallel |
| ZeRO-2 | + Gradients | ~8x reduction | Slightly more |
| ZeRO-3 | + Parameters | ~Nx reduction (N GPUs) | All-gather per layer |

ZeRO-3 est équivalent à FSDP. Le nom est différent, le mécanisme est le même. PyTorch a ajouté FSDP comme une mise en œuvre native après que DeepSpeed ait prouvé le concept.

> ZeRO-3 est identique à FSDP. Le nom est différent, le mécanisme est le même.

DeepSpeed a également introduit ZeRO-Offload (états de décharge optimisateur à la RAM du processeur, qui est moins cher et plus grand) et ZeRO-Infinity (décharge à des SSD NVMe). Ces vitesses de calcul de la capacité de mémoire - les opérations déchargées sont plus lentes mais libèrent la mémoire de la GPU.

> DeepSpeed a également introduit ZeRO-Offload (en anglais seulement), qui permettra de décharger l'état de l'optimisateur sur la CPU, plus facile et plus grand) et ZeRO-Infinity (en anglais seulement) (en anglais seulement, qui permet de décharger sur le SSD NVMe).

### Formation à la précision mixte

La formation moderne utilise simultanément plusieurs formats de points flottants:

> 现代训练同时使用多种浮点格式:

- **Forward pass**Les matrices fonctionnent deux fois plus vite sur les cœurs tensoriels.
- **Master weights**: FP32 (32 bits). Maintenu par l'optimisateur pour une précision numérique lors des mises à jour de poids.
- **Loss scaling**: Multipliez la perte par une constante importante avant le passage en arrière pour empêcher les gradients FP16 de descendre à zéro. Divisez par la même constante avant l'étape d'optimisation.

Le BF16 (Brain Float 16) a la même gamme d'exponents que le FP32 (8 bits d'exponents) mais une précision réduite (7 bits de mantissa contre 23 de FP32). Il a rarement besoin d'une mise à l'échelle des pertes car il peut représenter la même gamme de valeurs.

Les TPU de Google utilisent BF16 natively. A100 et H100 de NVIDIA supportent à la fois FP16 et BF16.

> **【中文解读】**混合精度训练是现代 LLM 训练的标准做法:前向传播用 BF16(16位),优化器维护 FP32 主权重(32位),损失缩放防止梯度下溢──BF16 avec FP32 ont la même index de champs(8位), mais l'exactitude est réduite(7位尾数 vs 23位), presque pas besoin de perdre de la taille──业界已从 FP16 全面显度转向 BF16──混合精为7B 模型节省约28GB ⋅

> **【拓展：3D 并行与 MoE 的经济性】**Llama 3 405B utilise 3D et aligne:节点间数据并行 + 节点内 8 路张量并行 + 节点流水线并行。DeepSeek-V3 utilise MoE(混合专家) architecture réduit le coût par fois avant de se propager seulement activée environ 37B 参数(总参数 671B), le coût de formation est d'environ 560 millions USD, soit 1/18 de Llama 3

**Memory comparison for a 7B model:**

| Precision | Weights | Optimizer | Gradients | Total |
|-----------|---------|-----------|-----------|-------|
| FP32 everywhere | 28 GB | 56 GB | 28 GB | 112 GB |
| Mixed (BF16 + FP32 master) | 14 GB | 56 GB | 14 GB | 84 GB |

La précision mixte économise 28 Go sur ce modèle. L'optimisateur reste en FP32 indépendamment - c'est là que la plupart de la mémoire va.

### Megatron-LM et parallélisme 3D

Une véritable formation à grande échelle combine les trois parallèles:

- **Data parallelism**sur les groupes de nœuds (dimension de lot à l'échelle)
- **Tensor parallelism**dans un nœud (couches divisées sur 8 GPU)
- **Pipeline parallelism**à travers les nœuds (groupes de couches divisées entre les machines)

Llama 3 405B sur 16 384 H100:
- Parallélisme de tensor à 8 voies dans chaque nœud (8 GPU par nœud)
- Parallélisme de pipeline à 16 voies entre les nœuds (16 étapes de pipeline)
- Parallélisme des données de 128 voies sur la dimension restante (16.384 / 8 / 16 = 128)

Cette décomposition 3D (8 x 16 x 128 = 16,384) est la façon dont vous étalonnez à des milliers de GPU. Chaque GPU voit une tranche de données différente (parallèle de données), tient une tranche de chaque couche (parallèle de tenseur) et calcule un ensemble différent de couches (parallèle de pipeline).

> Cette sorte de 3D de décomposition ((8 x 16 x 128 = 16,384) est la façon dont vous pouvez vous étendre à des milliers de GPUs.

DeepSeek V3 a pris une approche différente. leur architecture Mixture of Experts active seulement 37B sur 671B par paramètre par jeton. Cela signifie que chaque GPU ne doit calculer (et stocker des activations) que pour les paramètres actifs. Ils ont été formés sur 2.048 GPU H800 - moins d'un/8 du nombre de GPU de Meta - pour$5.6M vs Meta's estimated $100 millions.

> DeepSeek V3  a adopté différentes méthodes  leurs architectures mixtes spécialisées pour chaque jeton  activent seulement 671B paramètres 37B . Cela signifie que chaque GPU  doit seulement calculer  et stockage  activation  paramètres   ils ont 2,048 张 H800 GPU  entraînés  pas jusqu'à 1/8 du nombre de Meta GPU  coût 560 millions USD vs Meta  estimation de 1 milliard USD 

```mermaid
graph TD
    subgraph ThreeD["3D Parallelism (Llama 3 405B)"]
        direction TB
        subgraph DP["Data Parallel (128-way)\nSplit batch across 128 groups"]
            subgraph PP["Pipeline Parallel (16-way)\nSplit layers across 16 stages"]
                subgraph TP["Tensor Parallel (8-way)\nSplit each layer across 8 GPUs"]
                    G1["GPU 1\nSlice of layers 1-N"]
                    G2["GPU 2\nSlice of layers 1-N"]
                    G8["GPU 8\nSlice of layers 1-N"]
                end
            end
        end
    end

    N1["Total: 8 x 16 x 128 = 16,384 GPUs"]

    style G1 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G8 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style N1 fill:#1a1a2e,stroke:#e94560,color:#fff
```

## Construisez-le et mettez-le en œuvre.
```figure
paged-kv-cache
```

## Faites-le

### Étape 1: Simuler le parallélisme des données

Partagez un lot entre des GPU simulées. Chaque GPU calcule un passage vers l'avant sur son fragment.

> Pour chaque GPU, le calcul de la partition est effectué en fonction de la "échelle" moyenne.

```python
import numpy as np

def simulate_data_parallelism(data, num_gpus, model_fn):
    batch_size = len(data)
    shard_size = batch_size // num_gpus
    remainder = batch_size % num_gpus

    gpu_losses = []
    gpu_gradients = []

    offset = 0
    for gpu_id in range(num_gpus):
        extra = 1 if gpu_id < remainder else 0
        shard = data[offset:offset + shard_size + extra]
        offset += shard_size + extra

        loss, grad = model_fn(shard)
        gpu_losses.append(loss)
        gpu_gradients.append(grad)

    avg_loss = np.mean(gpu_losses)
    avg_gradient = np.mean(gpu_gradients, axis=0)

    return avg_loss, avg_gradient
```

L'opération tout-réduire (gradients moyens) est la seule communication dans le parallélisme des données. En pratique, cela utilise la bibliothèque NCCL sur les GPU NVIDIA, qui implemente le ring all-reduce: chaque GPU envoie 1/N de ses gradients à son voisin, reçoit 1/N de l'autre voisin, et après N-1 étapes chaque GPU a la moyenne complète. Volume total de communication: 2 x gradient_size x (N-1)/N, approchant 2x la taille du gradient pour le grand N.

> En pratique, il utilise la NCCL de la GPU NVIDIA, réalisant une opération de régulation complète: chaque GPU enverra une échelle de 1/N à son voisin, recevant une échelle de 1/N, N-1  par étape, chaque GPU aura une moyenne complète de la valeur totale de la communication: 2 x                                                                                                                                                                                                                        

### Étape 2: Simuler le parallélisme de la tension

Partagez une matrice de poids entre les GPU. Chaque GPU calcule une multiplication partielle de matrice. Combinez les résultats.

> Pour chaque GPU, le poids du matériau est divisé en plusieurs GPUs.

```python
def simulate_tensor_parallelism(input_data, weight_matrix, num_gpus):
    d_in, d_out = weight_matrix.shape
    assert d_out % num_gpus == 0, f"d_out {d_out} not divisible by num_gpus {num_gpus}"
    shard_size = d_out // num_gpus

    partial_results = []
    for gpu_id in range(num_gpus):
        start = gpu_id * shard_size
        end = start + shard_size
        weight_shard = weight_matrix[:, start:end]

        partial = input_data @ weight_shard
        partial_results.append(partial)

    full_output = np.concatenate(partial_results, axis=-1)

    direct_output = input_data @ weight_matrix
    error = np.abs(full_output - direct_output).max()

    return full_output, error
```

L'erreur devrait être exactement zéro (ou epsilon machine). Le parallélisme de tension est mathématiquement exact - il produit le même résultat que le calcul de la matmul complète sur un GPU. La fraction est le long de la dimension de sortie, donc chaque GPU produit une pièce différente de colonnes, et la concaténation reconstruit le résultat complet.

> 误差 devrait être correctement formé par zero (epsilon) ⋅张量并行在数学上是精确的它产生与在一张GPU上计算完整矩阵乘法相同的结果──分拆沿输出维度进行,每张GPU 产生不同的列块,拼接重建完整结果──

Pour les couches linéaires parallèles de colonne (diviser la dimension de sortie), vous concateniez. Pour les couches linéaires parallèles de ligne (diviser la dimension d'entrée), vous sumez. Dans un transformateur FFN, la première ligne (expansion) utilise le parallèle de colonne et la deuxième ligne (contrat) utilise le parallèle de ligne. Cela évite une réduction totale entre les deux couches.

> Pour les lignes de transformer FFN, la première ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la seconde ligne de transformer FFN est élargie, la troisième est élargie, la troisième est élargie, la troisième est élargie, la troisième est élargie, la troisième est élargie.

### Étape 3: Simuler le parallélisme du pipeline

Divisez les couches d'un modèle sur des GPU virtuelles. Montrez le problème de la bulle où les premières étapes restent inactives tandis que les étapes ultérieures calculent.

> Le modèle est divisé en GPU virtuel. Il montre les problèmes de bulles de calcul de la phase initiale et de la phase finale.

```python
def simulate_pipeline_parallelism(num_layers, num_stages, num_microbatches):
    layers_per_stage = num_layers // num_stages

    timeline = {}
    clock = 0

    for mb in range(num_microbatches):
        for stage in range(num_stages):
            start_time = max(
                timeline.get((stage, mb - 1, "fwd"), (0, 0))[1] if mb > 0 else 0,
                timeline.get((stage - 1, mb, "fwd"), (0, 0))[1] if stage > 0 else 0,
            )
            end_time = start_time + layers_per_stage
            timeline[(stage, mb, "fwd")] = (start_time, end_time)

    last_fwd_end = max(v[1] for v in timeline.values())

    for mb in range(num_microbatches - 1, -1, -1):
        for stage in range(num_stages - 1, -1, -1):
            deps = [last_fwd_end]
            if mb < num_microbatches - 1 and (stage, mb + 1, "bwd") in timeline:
                deps.append(timeline[(stage, mb + 1, "bwd")][1])
            if stage < num_stages - 1 and (stage + 1, mb, "bwd") in timeline:
                deps.append(timeline[(stage + 1, mb, "bwd")][1])
            start_time = max(deps)
            end_time = start_time + layers_per_stage
            timeline[(stage, mb, "bwd")] = (start_time, end_time)

    total_time = max(v[1] for v in timeline.values())
    compute_time = num_microbatches * num_stages * layers_per_stage * 2
    bubble_fraction = 1.0 - compute_time / (total_time * num_stages)

    return timeline, total_time, bubble_fraction
```

Avec 4 étapes et 1 micro-batch, la fraction de la bulle est de 75% - trois GPU sur quatre sont inactifs à tout moment. Avec 16 micro-batches, elle diminue à environ 19%. Le coût d'éliminer les bulles est la mémoire: vous devez stocker les activations pour tous les micro-batches en vol simultanément.

> 4 étapes et 1 micro-partie, le pourcentage de boues est de 75% les quatre quarts des trois GPU  16 micro-partie est toujours vide🏼 16 micro-partie est réduite à environ 19%

### Étape 4: Calculateur mémoire

Calculer les besoins de mémoire exacts pour l'entraînement de n'importe quelle taille de modèle.

> 计算训练任意模型大小的精确显存需求──

```python
def memory_calculator(
    params_billions,
    precision_bytes=2,
    optimizer="adam",
    num_gpus=1,
    sharding="none",
    sequence_length=2048,
    batch_size_per_gpu=1,
    hidden_dim=None,
    num_layers=None,
):
    params = params_billions * 1e9

    weight_memory = params * precision_bytes

    if optimizer == "adam":
        optimizer_memory = params * 4 * 2
    elif optimizer == "sgd":
        optimizer_memory = params * 4
    else:
        optimizer_memory = 0

    gradient_memory = params * precision_bytes

    total_no_activation = weight_memory + optimizer_memory + gradient_memory

    if hidden_dim and num_layers:
        activation_per_layer = (
            sequence_length * batch_size_per_gpu * hidden_dim * precision_bytes * 4
        )
        activation_memory = activation_per_layer * num_layers
    else:
        activation_memory = params * precision_bytes * 0.5

    if sharding == "fsdp" or sharding == "zero3":
        weight_memory /= num_gpus
        optimizer_memory /= num_gpus
        gradient_memory /= num_gpus
    elif sharding == "zero2":
        optimizer_memory /= num_gpus
        gradient_memory /= num_gpus
    elif sharding == "zero1":
        optimizer_memory /= num_gpus

    per_gpu_total = weight_memory + optimizer_memory + gradient_memory + activation_memory

    return {
        "params_billions": params_billions,
        "weights_gb": weight_memory / 1e9,
        "optimizer_gb": optimizer_memory / 1e9,
        "gradients_gb": gradient_memory / 1e9,
        "activations_gb": activation_memory / 1e9,
        "per_gpu_total_gb": per_gpu_total / 1e9,
        "total_across_gpus_gb": per_gpu_total * num_gpus / 1e9,
        "fits_on_80gb": per_gpu_total / 1e9 <= 80,
        "num_gpus": num_gpus,
        "sharding": sharding,
    }
```

Cette calculatrice répond à la question que chaque ingénieur ML pose: " Combien de GPU ai-je besoin ? " Donnez-lui la taille du modèle et voyez s'il convient. Ajustez la stratégie de fragmentation jusqu'à ce que le total par GPU tombe en dessous de 80 Go.

> Ce calculateur répond à chaque question de l'ingénieur ML: "Combien de GPU ai-je besoin?"

### Étape 5: Simulation de précision mixte

Comparer l'utilisation de la mémoire entre FP32, FP16 et l'entraînement de précision mixte.

```python
def mixed_precision_comparison(params_billions):
    params = params_billions * 1e9

    fp32_weights = params * 4
    fp32_optimizer = params * 4 * 2
    fp32_gradients = params * 4
    fp32_total = fp32_weights + fp32_optimizer + fp32_gradients

    fp16_weights = params * 2
    fp16_master = params * 4
    fp16_optimizer = params * 4 * 2
    fp16_gradients = params * 2
    fp16_total = fp16_weights + fp16_master + fp16_optimizer + fp16_gradients

    mixed_weights = params * 2
    mixed_optimizer = params * 4 * 2
    mixed_gradients = params * 2
    mixed_total = mixed_weights + mixed_optimizer + mixed_gradients

    return {
        "fp32_total_gb": fp32_total / 1e9,
        "fp16_with_master_gb": fp16_total / 1e9,
        "mixed_bf16_gb": mixed_total / 1e9,
        "savings_vs_fp32": 1 - mixed_total / fp32_total,
    }
```

La plus grande surprise pour la plupart des gens: la précision mixte ne réduit pas la mémoire de moitié. Les états de l'optimisateur (m et v d'Adam) restent en FP32 indépendamment de la précision. Pour un modèle 7B, la formation FP32 utilise 112 GB. La précision mixte utilise 84 GB. Cela représente une réduction de 25% et non 50%.

> Pour la plupart des gens, la plus grande surprise: l'exactitude mixte ne diminuera pas de moitié l'économie de l'optimisateur.

## Utilisez-le avec le cadre de réalisation

### Exécutez toutes les simulations

```python
def run_all_demos():
    print("=" * 70)
    print("DATA PARALLELISM SIMULATION")
    print("=" * 70)

    np.random.seed(42)
    data = np.random.randn(64, 32)
    weight = np.random.randn(32, 16)

    def model_fn(batch):
        output = batch @ weight
        loss = np.mean(output ** 2)
        grad = 2 * batch.T @ (batch @ weight) / len(batch)
        return loss, grad

    for n_gpus in [1, 2, 4, 8]:
        loss, grad = simulate_data_parallelism(data, n_gpus, model_fn)
        print(f"  {n_gpus} GPUs: loss={loss:.4f}, grad_norm={np.linalg.norm(grad):.4f}")

    print()
    print("=" * 70)
    print("TENSOR PARALLELISM SIMULATION")
    print("=" * 70)

    x = np.random.randn(4, 8192)
    W = np.random.randn(8192, 8192)

    for n_gpus in [1, 2, 4, 8]:
        output, error = simulate_tensor_parallelism(x, W, n_gpus)
        print(f"  {n_gpus} GPUs: output_shape={output.shape}, max_error={error:.2e}")

    print()
    print("=" * 70)
    print("PIPELINE PARALLELISM SIMULATION")
    print("=" * 70)

    for n_mb in [1, 4, 8, 16, 32]:
        _, total_t, bubble = simulate_pipeline_parallelism(32, 4, n_mb)
        print(f"  {n_mb:2d} micro-batches: total_time={total_t:4d}, bubble={bubble:.1%}")

    print()
    print("=" * 70)
    print("MEMORY CALCULATOR")
    print("=" * 70)

    configs = [
        (7, "none", 1),
        (7, "fsdp", 8),
        (70, "none", 1),
        (70, "fsdp", 8),
        (70, "fsdp", 16),
        (405, "fsdp", 64),
        (405, "fsdp", 128),
    ]

    print(f"  {'Model':>8} {'Sharding':>8} {'GPUs':>5} {'Per-GPU':>10} {'Fits 80GB':>10}")
    print("  " + "-" * 50)
    for params, shard, gpus in configs:
        result = memory_calculator(params, num_gpus=gpus, sharding=shard)
        fits = "Yes" if result["fits_on_80gb"] else "No"
        print(f"  {params:>6}B {shard:>8} {gpus:>5} {result['per_gpu_total_gb']:>8.1f}GB {fits:>10}")

    print()
    print("=" * 70)
    print("MIXED PRECISION COMPARISON")
    print("=" * 70)

    for params_b in [7, 13, 70, 405]:
        result = mixed_precision_comparison(params_b)
        print(f"  {params_b}B: FP32={result['fp32_total_gb']:.0f}GB, "
              f"Mixed BF16={result['mixed_bf16_gb']:.0f}GB, "
              f"Savings={result['savings_vs_fp32']:.0%}")
```

## Envoyez-le . Produit .

Cette leçon produit `outputs/prompt-distributed-training-planner.md`-- une requête qui prend une taille de modèle et du matériel disponible, puis produit un plan de formation distribué complet: stratégie de parallélisme, budget de mémoire, frais de communication et débit attendu.

## Les exercices

1. Modifiez la calculatrice de mémoire pour inclure le contrôle de l'activation. Avec le contrôle, stockez uniquement les activations à chaque K-th couche (typique K = 1, ce qui signifie recomputer tout). Montrez l'offre mémoire-compute: combien de mémoire le contrôle économise, et combien ralentit-il l'entraînement (environ 33% de plus de calcul pour le contrôle complet)?

2. Élargir la simulation de parallélisme du pipeline pour mettre en œuvre le calendrier 1F1B (un vers l'avant, un vers l'arrière) utilisé par PipeDream. Comparer la fraction de la bulle avec le calendrier naïf pour 4 étapes et 8 micro-parties. Le calendrier 1F1B devrait avoir une mémoire de pic plus petite parce qu'il démarre vers l'arrière passe plus tôt.

3. Implémenter un simulateur d'accumulation de gradients. Au lieu de réduire tous les gradients après chaque micro-batch, accumuler localement les gradients pour les étapes K, puis réduire tous. Montrez comment cela réduit la communication par K fois mais produit les mêmes gradients finaux (et donc l'entraînement identique).

4. Élaborer un estimateur de coûts.$2/hr, H100 at $L'évaluation des coûts de formation en dollars est réalisée en fonction des coûts connus:$100M, DeepSeek V3 cost ~$5,6M.

5. Ajouter ZeRO-Offload à la calculatrice de mémoire. Supposons que la RAM de la CPU soit de 512 Go par nœud et que NVMe soit de 2 To. Montrez comment le déchargement de l'optimisateur sur le CPU permet à un modèle 70B de s'entraîner sur 4 GPU au lieu de 16, au coût de 30 à 50% de pas d'optimisateur plus lents.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Data parallelism | "Copy the model to every GPU" | Each GPU processes a different data shard; gradients are averaged via all-reduce after each step | 数据并行，每 GPU 处理不同数据分片，通过 all-reduce 平均梯度 |
| Tensor parallelism | "Split a layer across GPUs" | Partition weight matrices so each GPU computes part of the matmul; requires fast NVLink interconnect | 张量并行，拆分权重矩阵到多 GPU，需要 NVLink 互连 |
| Pipeline parallelism | "Split layers across GPUs" | Each GPU runs a different group of layers; data flows through the pipeline with micro-batches to reduce bubbles | 流水线并行，每 GPU 运行不同层组，用微批次减少气泡 |
| FSDP | "Shard everything" | Fully Sharded Data Parallel -- each GPU holds 1/N of weights, gradients, and optimizer states; all-gather before compute | 完全分片数据并行，每 GPU 持有 1/N 的参数/梯度/优化器状态 |
| ZeRO | "DeepSpeed's version of FSDP" | Zero Redundancy Optimizer with 3 stages: shard optimizer (Stage 1), + gradients (Stage 2), + parameters (Stage 3) | 零冗余优化器，三阶段分片：优化器→梯度→参数 |
| All-reduce | "Average across GPUs" | Collective operation where every GPU ends with the sum (or average) of all GPUs' inputs -- typically implemented as ring all-reduce | 全归约，所有 GPU 最终获得全局总和/均值 |
| All-gather | "Collect from all GPUs" | Collective operation where every GPU ends with the concatenation of all GPUs' data -- used in FSDP to reconstruct full parameters | 全收集，每 GPU 获得所有 GPU 数据的拼接 |
| Reduce-scatter | "Sum and distribute" | Collective operation that reduces (sums) data and scatters different chunks to different GPUs -- used in FSDP for gradient sharding | 归约散射，求和后分发不同块到不同 GPU |
| Mixed precision | "Train in half precision" | Use FP16/BF16 for forward/backward and FP32 for optimizer states -- saves ~25% memory, not 50%, because the optimizer dominates | 混合精度，前向/反向用 16 位，优化器用 32 位，省约 25% 显存 |
| Pipeline bubble | "Idle time in the pipeline" | Fraction of time GPUs sit idle waiting for data from the previous stage -- reduced by using more micro-batches | 流水线气泡，GPU 空闲等待前一阶段数据的比例 |

## Encore une lecture

- [Rajbhandari et al., 2020 -- "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"](https://arxiv.org/abs/1910.02054)-- le papier ZeRO DeepSpeed qui définit les trois étapes de déchiquetage
- [Shoeybi et al., 2020 -- "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"](https://arxiv.org/abs/1909.08053)-- Le parallélisme tensoriel de NVIDIA pour les transformateurs
- [Narayanan et al., 2021 -- "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM"](https://arxiv.org/abs/2104.04473)-- Parallélisme 3D combinant données, tensor et pipeline
- [Zhao et al., 2023 -- "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel"](https://arxiv.org/abs/2304.11277)-- La mise en œuvre FSDP native de PyTorch
- [Llama 3 Technical Report](https://arxiv.org/abs/2407.21783)-- 16.384 GPU entraînement avec des détails de parallélisme 3D
- [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)-- comment l'architecture du MoE réduit le coût de la formation d'un ordre de grandeur
