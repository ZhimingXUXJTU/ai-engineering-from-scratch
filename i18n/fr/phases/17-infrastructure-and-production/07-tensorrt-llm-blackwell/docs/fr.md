# Le TENSORRT-LLM sur Blackwell avec FP8 et NVFP4
# Compilation d'inferences spécialisées en matériel  FP8 et NVFP4 sur Blackwell

> La compilation d'inférence spécialisée dans le matériel commercialise la portabilité pour le débit, et TensorRT-LLM  NVIDIA-uniquement, réglée pour Blackwell  est l'exemple le plus clair du commerce qui porte ses fruits. Sur GB200 NVL72 avec l'orchestration Dynamo, SemiAnalysis InferenceX a mesuré $0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0,09/M sur H100 + vLLM  un écart économique de 7 fois. La pile est composée de trois régimes à point flottant: FP8 reste critique pour les noyaux de cache et d'attention KV car il a la gamme dynamique dont ils ont besoin; NVFP4 (4 bits de microscalage) gère les poids et les activations; prédiction multi-token (MTP) et pré-remplissage / décode décomposé ajouter un autre 2-3x en haut. Le support du modèle Day-0 charge directement les poids FP4 sans conversion post-entraînement. Le but pour les équipes d'ingénierie 2026: TRT-LLM est open source mais spécifique à NVIDIA  CUDA- et Blackwell- spécialisée  donc l'adoption de la portativité pour le débit. Faites le calcul de votre mélange de modèles et de matériel avant de vous engager.

> **【中文解读】**Ce chapitre présente les logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logici
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

>  **【前置】**Je vous invite à maîtriser la phase 17·04(vLLM)、Phase 10·13(quantité de base)。TensorRT-LLM est NVIDIA 专属优化, le GPU Blackwell
>  **【类比】**TensorRT-LLM = "NVIDIA 专属跑车"―GB200 NVL72 上 SemiAnalysis 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7 倍 经济性差距──三套浮点叠加:FP8(KV cache+attention 动态范围) + NVFP4(4-bit 权重激活) + MTP/解 pré-remplir-décoder 再加 2-3 倍──代价:闭源 NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合算账──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Expliquez pourquoi FP8 reste essentiel pour le cache et l'attention KV même lorsque les poids sont dans NVFP4.
  Expliquer pourquoi même dans NVFP4, la FP8 est encore essentielle pour le KV 缓存和注意力.
- Comptez l'empreinte HBM d'un modèle frontalier sous BF16, FP8 et NVFP4 et raisonnez sur l'origine des économies.
  Le modèle de calcul avant-coût est basé sur le BF16、FP8 et NVFP4
- Nommer les fonctionnalités spécifiques à Blackwell exploitées par TRT-LLM (jour-0 FP4, MTP, service décomposé, primitifs tout-à-tout).
  Le programme de formation de la société est basé sur la technologie de l'information et de l'information.
- Décidez quand le verrou NVIDIA de TRT-LLM vaut le 7x de l'écart de coût par rapport à VLLM sur Hopper.
  Le NVIDIA de TRT-LLM est 7 fois plus important que Hopper.

## Le problème , l' introduction du problème

> **【中文解读】**La réponse dépend de quatre niveaux de superposition sélection: hardware代际(Hopper H100/H200 vs Blackwell B200/GB200) ✓ Écence(BF16 → FP8 → NVFP4) ✓ Motrice de suggestion(vLLM vs SGLang vs TRT-LLM) et编排(朴素 vs 分离式 vs Dynamo) ✓$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $Le prix de cette différence est NVIDIA Lockdown.

> **【拓展：NVIDIA Blackwell 架构】**Blackwell (B200/GB200) est une architecture de GPU lancée par NVIDIA en 2024-2025 par rapport à Hopper (H100) dans le cadre de la LLM. Elle a 11 à 15 fois la capacité de production de chaque GPU.

La frontière de l'économie d'inférence en 2026 est "combien de jetons par dollar". La réponse dépend de quatre choix empilés: génération de matériel (Hopper H100/H200 vs Blackwell B200/GB200), précision (BF16 → FP8 → NVFP4), moteur de service (vLLM vs SGLang vs TRT-LLM), et orchestration (plain vs disaggregé vs Dynamo).

> La réponse dépend de quatre options: hardware代际(Hopper vs Blackwell)、精度(BF16 → FP8 → NVFP4)、推理引擎(vLLM vs SGLang vs TRT-LLM)

Sur Hopper avec VLLM, un MoE 120B fonctionne à ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$Une partie de cette lacune est matérielle (Blackwell est 11-15x par GPU LLM throughput vs Hopper). Une autre est la pile: poids FP4, projet MTP, pré-remplissage / décode décomposé, et NVLink 5 tout-à-tout pour la communication par experts MoE.

> Dans le Hopper + vLLM 上, 120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012便宜 7 倍──部分差距来自硬件(Blackwell vs Hopper 每 GPU LLM 吞吐 11-15 倍)──部分来自:FP4 权重、MTP draft、分离式预填充/解码和NVLink 5 all-to-all Utilised for MoE 专家通信──

Vous ne pouvez pas reproduire cela en dehors de la pile NVIDIA. C'est le compromis  portabilité pour l'économie. Comprendre quels choix de pile donnent quelle part de l'écart est le but de cette leçon.

> Vous ne pouvez pas le faire en dehors de NVIDIA. C'est le poids de la transposition.

## Le concept de base.

### Pourquoi FP8 est toujours le sol pour KV cache

> **【中文解读】**FP8 est la requête de précision minimale de KV Cache. La valeur de concentration de KV Cache est très large. La taille de KV est réduite à FP4 et entraîne une perte de précision catastrophique. NVFP4 ne peut être utilisé que pour le poids et l'activation.

Une erreur commune en 2026: en supposant que NVFP4 s'applique partout. Il ne l'est pas. Le cache KV a besoin de FP8 (8 bits floating point) car il stocke des clés d'attention et des valeurs qui couvrent une large gamme dynamique. Le quantifier KV à FP4 provoque une perte de précision catastrophique  la queue de la distribution diminue et les scores d'attention s'effondrent.

> Une erreur commune de 2026: supposer que NVFP4 s'applique à tous les endroits. Il n'est pas de la. KV 缓存需要FP8 (en anglais seulement), car il est stocké dans une large gamme de champs d'attention.

NVFP4 (2025-2026) s'applique aux poids et aux activations. Microscale: chaque bloc de poids a son propre facteur d'échelle afin que de petits blocs puissent couvrir différentes gammes dynamiques sans perte d'échelle par tenseur. Pour les activations, FP4 se maintient parce que les activations sont de petite gamme dans une couche.

> NVFP4 (en anglais: NVFP4 (en anglais: NVFP4 (en anglais: NVFP4 (en anglais: NVFP4)) est utilisé pour le poids et l'activation.

Le type de Blackwell:

- Poids: NVFP4 (4 bits à micro-échelle).
  Le texte de la lettre de la première lettre est écrit en français.
- Activations: NVFP4.
  Le mot "réflex" est le mot "réflex".
- Le cache KV: FP8.
  Le texte de la lettre de la première lettre est écrit en français.
- Accumulateur d'attention: FP32 (stabilité à hauteur de la température).
  Le récit de la première partie de la série est le suivant:

### Les primitives spécifiques à Blackwell utilisées par TRT-LLM

- **Day-0 FP4 weights**Les fournisseurs de modèles expédient directement les poids FP4; les charges TRT-LLM sans conversion post-entraînement.
  Le mot grec traduit par " le mot grec "**Day-0 FP4 权重**Le modèle fournisseur de téléchargement est directement publié par FP4 权重;TRT-LLM 无需训练后转换即可载──FP4 不需要 AWQ/GPTQ 步骤──
- **Multi-token prediction (MTP)**: la même idée que EAGLE (phase 17 · 05) mais intégrée dans la construction TRT-LLM.
  Le mot grec traduit par " le mot grec "**多 token 预测 (MTP)**La phase 17 est la même que celle de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation.
- **Disaggregated serving**: pré-remplissez et décodez sur des pools GPU distincts, KV cache transféré par NVLink ou InfiniBand.
  Le mot grec traduit par " le mot grec "**分离式服务**Le code est fourni par le système de téléchargement de téléphonie mobile.
- **All-to-all communication primitives**NVLink 5 réduit la latence de communication des experts MoE de 3x par rapport à Hopper.
  Le mot grec traduit par " le mot grec "**All-to-all 通信原语**Le taux de retard de communication de l'EER sera réduit de 3 fois.
- **NVFP4 + MXFP8 microscaling**: manipulation accélérée par le matériel de facteurs d'échelle sur les cœurs de tensor Blackwell.
  Le mot grec traduit par " le mot grec "**NVFP4 + MXFP8 微缩放**Le système de traitement des éléments de Blackwell Tensor Core

### Les chiffres que vous devriez mémoriser

- HGX B200 à 0,02 $ / M de jetons sur GPT-OSS-120B via TRT-LLM.
  Le code de débit de la valeur de la banque est le code de débit de la banque.
- GB200 NVL72 à 0,012/M $ par le biais de Dynamo (orchestration TRT-LLM).
  Le code de débit est basé sur le code de débit.
- H100 + vLLM ≈ 0,09 $ / M de jetons sur une charge de travail comparable.
  H100 + vLLM 在可比工作负载上约$0.09 /M des jetons。
- 2,8 fois plus de débit en trois mois de mises à jour du TRT-LLM (2026).
  Le taux de croissance de la production de gaz de carbone est de 2,8 fois supérieur à celui de la production de gaz de carbone.
- 11 à 15 fois le débit par GPU LLM, Blackwell vs Hopper.
  Le nombre de personnes qui ont été tuées par les autorités de l'État de New York est de 11 à 15 fois.
- MLPerf Inference v6.0 (avril 2026): Blackwell domine chaque tâche présentée.
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEP) est une initiative de la Commission européenne sur les droits de l'homme (CEP).

### Quel est le coût de la qualité du 4e PQ

> **【中文解读】**La norme de base de la norme NVFP4 est de prévoir que les modèles de calcul utilisent le poids FP8 + FP4 activé comme un freinage ou continuent à utiliser H200 complet FP8 . La règle est de prévoir que, avant de soumettre le poids NVFP4, il faut vérifier la qualité de la tâche dans son propre ensemble d'évaluation.

> **【拓展：量化精度 vs 推理成本权衡】**La sélection de la précision quantique est un poids de la qualité et du coût: 1) BF16 sans perte de qualité, mais la demande de stockage est grande; 2) FP8 presque sans perte, Hopper/Blackwell Accélération du matériel, recommandé pour la détection de tâches de type intensif; 3) INT4(AWQ/GPTQ) 4-bit Pétence, MATH 分数下降 3-5点, adapté à la discussion générale; 4) NVFP4 le plus actif, Blackwell 专用, doit être évalué dans l'objectif d'essai.

NVFP4 est agressif. Sur les charges de travail lourdes (chaîne de pensée, mathématiques, génération de code avec long contexte), les poids FP4 se dégradent visiblement. L'étalonnage par bloc atténue mais n'élimine pas. Les modèles de raisonnement des équipes utilisent souvent des poids FP8 + activations FP4 comme compromis, ou adhèrent à H200 avec FP8 tout au long.

> Le NVFP4 est activé. Dans la conception de la charge de travail intensive ([[pensées]], mathématiques]], la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de la conception de conception de la conception de conception de la conception de conception de la conception de la conception de la conception de la conception de conception de la conception de conception de la conception de conception de la conception de conception de la conception de conception de la conception de conception de conception de la conception de conception de la conception de conception de la conception de conception de la conception de conception

La règle: toujours valider la qualité de la tâche sur votre ensemble d'évaluation avant de s'engager dans des poids NVFP4.

> Règlement: avant de soumettre NVFP4 权重, toujours sur votre évaluation de l'ensemble de vérification de la qualité des tâches.

### Pourquoi c'est une décision de verrouillage NVIDIA

> **【中文解读】**TRT-LLM est un ensemble de C++ + CUDA + 闭源内核的组合―― un modèle nécessite un SKU GPU spécifique 编译―― ne prend pas en charge AMD、Intel ou ARM―― si votre stratégie d'infrastructure est multi fournisseurs, TRT-LLM  pour cette couche est une option non optionnelle vous pouvez toujours utiliser vLLM sur des matériels mixtes― mais si vous êtes uniquement NVIDIA, une différence économique de 7x vaut la peine de cette fermeture―

> **【拓展：NVIDIA vs AMD 推理生态】**En 2026, l'IA  Réflexion sur le marché des puces: NVIDIA  Avec CUDA 生态 et TRT-LLM  Prise en charge d'environ 80% de la part de la Résolution sur les centres de données. AMD MI300X est compétitif sur l'algorithme initial, mais le logiciel (ROCm + vLLM) est toujours à la recherche. Intel Gaudi 3 est une autre option mais son taux d'adoption est plus faible. Pour les entreprises qui dépensent plus de 100 millions de dollars en réflexion annuelle, le déménagement à Blackwell + TRT-LLM + Dynamo 7 fois plus loin dans la dépense pourrait économiser des milliards de dollars.

TRT-LLM est un noyau de source fermée. Les modèles doivent être compilés pour un SKU GPU spécifique. Pas de AMD, pas d'Intel, pas d'ARM. Si votre stratégie infrarouge est multi-vendeur, TRT-LLM est un non-starter pour le niveau TRT-LLM servi.

> TRT-LLM est un ensemble de C++ + CUDA + 闭源内核的组合――模型需要为特定 GPU SKU 编译――不支持 AMD、Intel 或 ARM――如果你的基础设施策略是多供应商,TRT-LLM不可行你仍然可以在混合硬件上使用vLLM――如果你是NVIDIA-only,7x 差距值得这个锁──

### 2026 recette pratique

Pour une facture annuelle d'inférence de 100 millions de dollars, fonctionner sur Hopper + vLLM laisse 7 à 10 fois sur la table. Migrer les charges de travail dominantes en coûts vers Blackwell + TRT-LLM + Dynamo. Garder le niveau d'expérimentation sur H100 + vLLM pour la vitesse d'itération du modèle. Valider la qualité sur chaque modèle converti en NVFP4 avant la production.

> Pour les dépenses annuelles de 100 M$+, le fonctionnement de Hopper + vLLM signifie de 7 à 10 fois plus d'espace à économiser. Le coût de la charge de travail sera transféré à Blackwell + TRT-LLM + Dynamo.

### Le bonus de désagrégation

La portion désagrégée de TRT-LLM (pools de pré-remplissage et de décode séparés) est couverte en profondeur dans la phase 17 · 20. Sur Blackwell, les pile de multiplicateurs: poids FP4 × accélération MTP × placement désagrégé × routage conscient du cache.

> Le projet de loi de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de la Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Région de Régi

## Utilisez-le avec le cadre de réalisation

> **【拓展：Blackwell 迁移决策】**1) Les dépenses annuelles de calcul dépassent-elles les 5 millions de dollars ? est-ce que la migration mérite une évaluation ? 2) Est-ce que l'on peut accepter la NVIDIA ?
```figure
pipeline-parallel
```

## Utilisez-le

`code/main.py`Compute l'empreinte HBM, le décodage de débit (régime de mémoire liée) et les jetons $/M pour un modèle sur trois piles: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. Exécutez-le pour voir l'effet de composition et la part de l'écart que chaque changement contribue.

> `code/main.py`計算模型在三上 HBM 占用、解码吞吐量(内存受限) et $/M-tokens:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行它查看复合效应和每个变化贡献差距份额──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-trtllm-blackwell-advisor.md`. Compte tenu de la charge de travail, de la taille du modèle et du volume annuel des jetons, il décide si la pile Blackwell + TRT-LLM vaut le verrouillage NVIDIA.

> 本课产 出 `outputs/skill-trtllm-blackwell-advisor.md` Donnée la charge de travail  Modèle taille et volume de jetons annuels, il décide Blackwell + TRT-LLM  si vaut la peine de NVIDIA 锁定

## Les exercices

1. On court .`code/main.py`. Sur un MoE 120B avec des paramètres actifs de 30%, calculer le décodage limité de la mémoire-largeur de bande passante sur H100 BF16, H100 FP8 et B200 NVFP4/FP8.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Dans les 30% des paramètres actifs de 120B MoE, calculer H100 BF16、H100 FP8 et B200 NVFP4/FP8 de l'inventaire de la capacité de débit limitée de code ◊ le plus grand saut provient de qui ?
2. Un client dépense 2 millions de dollars par an sur H100 + vLLM. Quel est le nombre d'équivoques de GPU Blackwell qu'il doit acheter pour amorcer une migration vers TRT-LLM en 12 mois, compte tenu de l'écart économique de 7 fois ?
   Pour les clients H100 + vLLM 上, ils dépensent 2 millions de dollars par an.
3. Vous verrez une baisse de précision de 3 points sur MATH après la conversion de poids NVFP4. Nommez deux voies de récupération: une qualité-première (maintien des poids FP8) et une coût-première (calibrer avec les données dans le domaine).
   Le programme de rétablissement de la qualité de l'énergie et de la qualité de l'énergie est un programme de rétablissement de la qualité de l'énergie et de la qualité de l'énergie.
4. Lisez les résultats de l'inférence MLPerf v6.0.
   Le résultat de la mise en œuvre de la mise en œuvre de la mise en œuvre de la stratégie de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en.
5. Compute le HBM nécessaire pour un modèle 405B à des poids NVFP4 + FP8 KV cache à un contexte 128k.
   Le modèle de calcul 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下HBM 需求──.

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Encore une lecture

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) Avril 2026 résultats de la MLPerf.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) NVLink 5 tout-à-tout et MoE noyaux.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) documentation officielle du moteur.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) orchestration décomposée au-dessus de TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) la suite de référence qui publie les chiffres Blackwell.
