# Quantisation de la production  AWQ, GPTQ, GGUF K-quants, FP8, MXFP4/NVFP4 量化 生产

> Le format de quantification n'est pas un choix universel  il est une fonction du matériel, du moteur de service et de la charge de travail. GGUF Q4_K_M ou Q5_K_M possède la CPU et le bord, livrés par llama.cpp et Ollama. GPTQ gagne dans le vLLM quand vous avez besoin de plusieurs LORA sur la même base. AWQ avec les noyaux Marlin-AWQ fournit ~741 tok/s sur un modèle de classe 7B avec le meilleur Pass@1 à INT4  la production par défaut de 2026 pour le centre de données. Le 8e trimestre reste le terrain du milieu sur Hopper, Ada et Blackwell  presque sans pertes et largement soutenu. NVFP4 et MXFP4 (microscalage Blackwell) sont agressifs et nécessitent une validation par bloc. Deux équipes de pièges: le jeu de données d'étalonnage doit correspondre au domaine de déploiement, et le cache KV est séparé de la quantification du poids  la leçon AWQ "mon modèle est 4 Go maintenant" oublie le cache KV de 10 à 30 Go aux tailles de lot de production.

> **【中文解读】**Ce chapitre présente l'application de la technologie de quantification de l'environnement de production à la déploiement Int8/Int4/FP8 dans la réduction des coûts de production.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

>  **【前置】**Je vous invite à maîtriser la phase 10·13 (en anglais)  la phase 17·04 (en anglais)  la phase 17·04 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais)  la phase 17 (en anglais) ) 
>  **【类比】**量化格式 = "压缩行李"。GGUF Q4_K_M = 适合火车/edge(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) "Mon modèle est seulement de 4GB" 忘了KV cache(production batch 下 10-30GB)。
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objectifs d'apprentissage

- Nombre des six formats de quantification de production et de leurs points doux en 2026.
  Le modèle de production de six niveaux de production et son meilleur usage en 2026
- Choisissez un format donné du matériel (CPU vs GPU, Hopper vs Blackwell), du moteur (vLLM, TRT-LLM, llama.cpp) et de la charge de travail (chat de routine, raisonnement, multi-LoRA).
  Selon le texte de la traduction chinoise, le mot de passe est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage" et "coupage" est "coupage"
- Compute la mémoire de poids enregistrée et le cache KV laissé intact pour un format choisi.
  Le calcul de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne de l'épargne
- Nommez le piège de l'ensemble de données d'étalonnage qui dégrade les modèles quantifiés sur le trafic de domaine.
  Traduction anglaise: dire que cela a conduit à la dégradation du modèle quantique dans le domaine de la circulation.

## Le problème , l' introduction du problème

> **【中文解读】**Quantification réduit la mémoire et HBM 带宽消耗 正是最需要的阶段 解码. FP16 模型重量为140GB,INT4 量化后仅35GB,可在一张H100上运行(80GB HBM) 但量化不是免费激进的量化降低质量 (特别是推理密集型任务),不同格式需要不同引擎,不同硬件支持不同精度──2026年有六种生产级量化格式,必须根据你的技术来选择──

> **【拓展：量化技术演进】**La technologie de quantification a connu trois générations: 1) la quantification moyenne (INT8/INT4)  simple mais de grande précision; 2) la perception (AWQ/GPTQ)  protection du poids important,INT4 下质量接近 BF16; 3) la quantification (FP8/NVFP4)  accélération des matériaux, la portée des activités s'améliore.

La quantification réduit la mémoire et la bande passante HBM, ce qui est exactement ce dont le décodeur a besoin. Un modèle FP16 70B est de 140 Go de poids. Quantifier les poids à INT4 (AWQ ou GPTQ) et le modèle est de 35 Go s'adapte à un H100 avec place pour le cache KV, ce qui importe car à 128 séquences concurrentes avec 2K contexte, le cache KV seul est de 20-30 Go.

> La réduction quantitative de la mémoire et de la consommation de bande passante HBM est le plus nécessaire pour le décodeur. Le poids du modèle 70B de la FP16 est de 140 Go. Le poids du modèle sera réduit à INT4 (AWQ ou GPTQ) Le modèle suivant ne peut être utilisé que sur un H100, il y a aussi de la place pour le KV, ce qui est important dans les 128 et 2K.

Mais la quantification n'est pas gratuite. La quantification agressive dégrade la qualité, en particulier sur les tâches lourdes de raisonnement. Différents formats fonctionnent avec différents moteurs. Différents matériels prennent en charge différentes précisions nativement. Le format du zoo 2026 est réel et vous ne pouvez pas copier le choix de quelqu'un d'autre.

> Mais la quantification n'est pas gratuite. La quantification de l'énergie réduit la qualité, en particulier en raison de tâches de type intensif.

## Le concept de base.

### Les six formats

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### GGUF  le CPU/edge par défaut

> **【拓展：GGUF 在边缘推理中的地位】**Le GGUF est le format par défaut de llama.cpp 和 Ollama, qui occupe une place dominante dans la logique CPU/边缘. Q4_K_M 和 Q5_K_M est la production par défaut à 4-5 bits pour atteindre la qualité de BF16.

GGUF est un format de fichier, pas un schéma de quantification en soi. Il regroupe les variantes quantiques K (Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0) dans un conteneur. Q4_K_M et Q5_K_M sont les défauts de production  près de la qualité BF16 à 4-5 bits. Le meilleur choix pour le serveur CPU ou Edge car llama.cpp est de loin le moteur d'inférence CPU le plus rapide.

> GGUF est un format de fichier, en soi pas un schéma quantifié. Il va être K-quant 变体打包在一个容器中. Q4_K_M 和 Q5_K_M est la production par défaut de 4-5 bits.

Penalty de débit dans vLLM: ~93 tok/s sur 7B  le format n'est pas optimisé pour les noyaux de GPU. Utilisez GGUF lorsque la cible de déploiement est CPU/edge.

> Le modèle n'est pas destiné à l'optimisation du GPU. Le seul objectif de la déploiement est d'utiliser le GPU/GGUF en utilisant le GPU/GGB.

### GPTQ  multi-LRA dans le vLLM

GPTQ est un algorithme de quantification post-entraînement avec un passage d'étalonnage.

> GPTQ est un type d'algorithme de quantification de formation avec la programmation.

Le succès unique: GPTQ-Int4 prend en charge les adaptateurs LoRA dans vLLM. Si vous utilisez un modèle de base plus 10 à 50 variantes finement ajustées (chacune en tant que LoRA), GPTQ est votre chemin. NVFP4 ne prend pas en charge encore LoRA dès le début de 2026.

> 独特优势:GPTQ-Int4 在 vLLM 中支持LoRA 适配器──如果你在服务一个基础模型加10-50个微调变体(每个作为LoRA),GPTQ est votre chemin──截至2026年初NVFP4 尚不支持LoRA──

### AWQ  le GPU par défaut du centre de données

> **【中文解读】**AWQ(Activation-conscious Weight Quantization) est une sélection par défaut du GPU du centre de données de 2026 ans 推理的默认选择──它保护量化过程中约1% 最显著的权重,配合Marlin-AWQ内核实现 10.9x 加速── sur le modèle 7B atteint ~741 tok/s, est le plus élevé du format INT4 dans le Pass@1 形式──除非需要多 LoRA(选择GPTQ) ou Blackwell FP4(选择 NVFP4),否则应应新 GPU 推理项目默认使用 AWQ──

La quantification de poids consciente de l'activation protège les poids les plus remarquables de 1% pendant la quantification. Noyaux Marlin-AWQ: 10.9x de vitesse par rapport à naïf. ~ 741 tok/s sur 7B, meilleur Pass@1 parmi les formats INT4.

> 激活感知权重量化──保护量化过程中约1% 最显著的权重──Marlin-AWQ 内核:比朴素方法快 10.9 倍──7B 模型约 741 tok/s,INT4 格式中 Pass@1 最高──

Choisissez AWQ pour le nouveau service de GPU à moins que vous n'ayez besoin de multi-LoRA (GPTQ) ou d'un Blackwell FP4 agressif (NVFP4).

> Le projet de développement de la nouvelle GPU 推理项目选择 AWQ, excepté si vous avez besoin de plus de LoRA(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

### PQ8  le milieu fiable

> **【拓展：FP8 量化的生产应用】**FP8(8-bit 浮点) est l'épreuve de la qualité de 2026 année. FP8 est la moitié de l'INT4, mais le risque de qualité est très faible.

Le point flottant de 8 bits. Presque sans perte. Largement pris en charge. Les cœurs de tension Hopper accélèrent FP8 de manière native. Blackwell hérite. FP8 est le défaut sûr de 2026 lorsque la qualité n'est pas négociable (réasonnement, médical, génération de code). L'économie de mémoire est la moitié de l'INT4 mais le risque de qualité est beaucoup plus faible.

> Le taux de débit de la production de la production de codes est de 0,8%, ce qui signifie que la production de codes de production est de 0,8%.

### MXFP4 / NVFP4  Blackwell agressif

Microscale FP4. Chaque bloc de poids a son propre facteur d'échelle. Aggressif mais accéléré par le matériel sur les cœurs de tensors Blackwell.

> 微缩放 FP4── chaque bloc de poids a son propre facteur de réduction── activation mais Blackwell Tensor Cores 硬件加速── comparativement à FP8 Phase 17 · 07

Les cavernes:
- Aucun soutien à la LRA pour l'instant (début 2026).
  Le gouvernement de la République de Chine a décidé de mettre fin à la guerre de Sécession.
- Une baisse de la qualité visible sur les charges de travail lourdes.
  Le nombre de personnes qui ont été affectées par la maladie a diminué de moitié.
- Valider sur votre ensemble d'évaluation par modèle.
  Chaque modèle est évalué en collection de tests.

### Le piège d'étalonnage

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 需要校准数据集来决定保护哪些权力──通用C4/WikiText 数据集在领域模型(代码、医疗、法律) 上会导致错误决策HumanEval Pass@1 可能下降几百分点──修复方法是用于领域内数据校准,通常几百个样本就够了,发货前在评估集上验证──

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎无影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH benchmark);(4) 长上下文理解INT4 在 128K+ context 上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用FP8 或BF16,通用聊天可用INT4──

AWQ et GPTQ nécessitent un ensemble de données d'étalonnage  généralement C4 ou WikiText. Pour les modèles de domaine (code, médical, juridique), l'étalonnage sur le texte Web générique permet à l'algorithme de prendre de mauvaises décisions sur les poids à protéger. Pass@1 sur HumanEval peut perdre plusieurs points.

> AWQ et GPTQ 需要校准数据集通常是C4或WikiText──对于领域模型(代码、医疗、法律),在通用网络文本上校准会让算法错误决策保护哪些权重──HumanEval Pass@1可能下降几百分点──

La solution: calibrer sur les données du domaine. Des centaines d'échantillons de domaine sont généralement suffisants.

> 修复方法: Utilisation de données dans le domaine de la classification.

### Le piège de cache KV

> **【中文解读】**KV Cache 陷:AWQ va réduire le poids de poids à 4 bits, mais KV Cache est indépendant, maintenir en FP16/FP8。70B AWQ 模型的完整内存预算是:权重35GB + KV Cache(128 并发 × 2K context) 20GB + 激活5GB = 总计60GB。朴素地认为"我的模型量化会到4GB 已忘记另外30-50GB──必须整体预算HBM。

AWQ réduit les poids à 4 bits. Le cache KV est séparé et reste à FP16/FP8. Pour un modèle 70B avec AWQ:

- Poids: ~ 35 Go (INT4 à partir de 140 Go).
  Le poids de l'incarnation est d'environ 35 Go.
- Cache KV à 128 contextes simultané × 2k: ~ 20 Go.
  Le KV 缓存: environ 20 Go.
- Activations: ~ 5 Go.
  Environ 5 Go.
- Total: ~60 Go  s'adapte au H100 80 Go.
  Environ 60 Go pour H100 80 Go.

Naïvement, "J'ai quantifié mon modèle à 4 Go" oublie les autres 30 à 50 Go.

> Je pense simplement que "mon modèle a été mesuré à 4 Go" et j'ai oublié les 30 à 50 Go.

Separément, la quantification cache KV (FP8 KV ou INT8 KV) est un choix différent avec ses propres compromis  elle affecte directement la précision de l'attention et n'est pas une victoire libre.

> En outre, le KV 缓存量化 (FP8 KV ou INT8 KV) est un choix indépendant avec un poids différent qui affecte directement l'exactitude de l'attention, et non les bénéfices gratuits.

### AWQ INT4 est dangereux pour le raisonnement

La chaîne de pensée, les mathématiques, le code-gen avec un long contexte  ceux-ci souffrent visiblement de quantification agressive. AWQ INT4 perd ~ 3-5 points sur MATH. Pour les charges de travail lourdes, envoyez FP8 ou BF16; acceptez le coût de la mémoire.

> Pour une charge de travail intensive, utilisez FP8 ou BF16; acceptez le coût de stockage.

### Guide de sélection 2026

- Service de CPU/extrémité: GGUF Q4_K_M. Fin.
  Le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
- GPU serve, chat de routine, pas de LoRA.
  Le groupe de travail de la société civile a été créé en 1999 pour la création de l'entreprise de la société civile.
- GPU serve, multi-LoRA: GPTQ avec Marlin.
  Le texte de la lettre de la première lettre est écrit en français.
- Charge de travail de raisonnement: 8e RP.
  Le travail de la société civile est une activité de la société civile.
- Centre de données Blackwell, qualité validée: NVFP4 + FP8 KV.
  Le nombre de personnes concernées est de 0,9%.
- Ambigu: effectuer une évaluation de 1000 échantillons sur chaque format de candidat.
  Le nombre de candidats à l'élection présidentielle est de 1000.

## Utilisez-le avec le cadre de réalisation
```figure
gpu-memory-breakdown
```

## Utilisez-le

`code/main.py`Il compute l'empreinte mémoire (poids + KV + activations) et le débit relatif sur les six formats pour une gamme de tailles de modèles.

> `code/main.py`計算一系列模型大小在六种格式下内存占用(权重 + KV + 激活) et la capacité de débit relative。 démontrer que KV 缓存在在哪里占主导、权重压缩在哪里划算、FP8 在哪里是安全选择──

## Envoyez-le . Produit .

> **【拓展：量化选型决策树】**2026 année de sélection de format quantifié Tree de décision:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU 通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) Un certain → 在候选格式运行1000样本评估;;;;

Cette leçon produit `outputs/skill-quantization-picker.md`. Compte tenu du matériel, de la taille du modèle, du type de charge de travail et de la tolérance de qualité, choisit un format et produit un plan d'étalonnage/validation.

> 本课产 出 `outputs/skill-quantization-picker.md` la tolérance au travail et à la qualité, la sélection du format et la production de programmes de certification.

## Les exercices

1. On court .`code/main.py`Pour un modèle 70B à 128 en simultané avec 2k contexte, calculer le total HBM pour chaque format.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Pour le modèle 70B de 128 et 2K, calculer le total de chaque format HBM.
2. Si vous avez tort sur la tolérance de qualité, quel est le chemin de récupération ?
   Vous avez un modèle de 7B. Choisissez un modèle et expliquez pourquoi. Si vous jugez mal la tolérance à la qualité, quel est le chemin de la récupération ?
3. Comptez la taille du ensemble de données d'étalonnage nécessaire pour calibrer AWQ pour un modèle de domaine médical. Pourquoi plus de données ne sont pas toujours meilleures?
   Le modèle de calcul du domaine médical AWQ 校准所需的数据集大小──为什么更多数据不总是好?
4. Lisez le papier du noyau de Marlin-AWQ ou les notes de sortie. Expliquez en trois phrases pourquoi AWQ atteint 741 tok/s sur 7B alors que le GPTQ brut atteint ~712.
   Le nombre de points de conversion de la quantité nucléaire atteint 741 par seconde, tandis que le GPTQ original atteint 712 par seconde.
5. Quand est-il logique de combiner les poids AWQ avec le cache KV FP8 vs garder KV à BF16 ?
   Le nombre de réserves de stockage est de 16 KV.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## Encore une lecture

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/) des critères de référence comparatifs.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) Numéros de débit par format.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/) sélection format par format.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html) formats et drapeaux pris en charge.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) la formule AWQ originale.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323) la formule originale du GPTQ.
