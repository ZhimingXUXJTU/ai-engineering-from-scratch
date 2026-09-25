# Réduction du démarrage à froid pour les LLM sans serveur

> Une image de modèle de 20 Go prend de 5 à 10 minutes (7 B) à plus de 20 minutes (70 B) pour passer du froid à la portion. Dans un monde sans serveurs, ce n'est pas un réchauffement, c'est une panne. Les atténuations fonctionnent à cinq niveaux: images de nœuds pré-sémentées (Bottlerocket sur AWS, arc à double volume), streaming de modèle (NVIDIA Run:ai Model Streamer, natif en vLLM), captures instantanées de mémoire GPU (points de contrôle modèles, redémarrage jusqu'à 10 fois plus rapide), piscines chaudes (`min_workers=1`Le module de téléchargement est un module de téléchargement de 2 à 4 fois par étage, basé sur un bassin de 5 à 10 secondes par défaut, sous-seconde avec pré-calé.

> **【中文解读】**Ce chapitre présente les stratégies de réaction à la retardée de la première fois en matière de gestion des coûts de gestion de l'entreprise.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**Je suis en train de faire une étude de la technologie de l'information et de la communication.
>  **【类比】**Le temps de chargement est de 20 minutes à 5 minutes. Le temps de chargement est de 20 minutes à 5 minutes.
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Nombrez les cinq couches d'atténuation du démarrage à froid et nommez un outil ou un motif à chaque couche.
  Traduction anglaise: L'écriture est une méthode de réaction de la réaction de la réaction.
- Comptez le temps total de démarrage à froid comme la somme de (provisionnement du nœud) + (poids de téléchargement) + (poids de chargement dans le HBM) + (initiation du moteur) pour un modèle 70B.
  Le temps de chargement total du modèle est de 70B = 节点供给 + 权重下载 + 权重加载到HBM + 引擎初始化――
- Expliquez pourquoi la migration en direct transfère des jetons d'entrée (KB) et non le cache KV (GB) et quelle est la sanction (recomputation).
  Le code de référence est le code de référence de la carte de crédit.
- Nommez le compromis de la piscine chaude (payer pour la GPU en marche ou accepter la queue de démarrage à froid) et le seuil de SLA à lequel `min_workers > 0`devient obligatoire.
  Le nombre de personnes qui ont été incarcérées dans le système de calcul est de 0,5% en moyenne.`min_workers > 0`变为强制性的 SLA 值──

## Le problème , l' introduction du problème

> **【中文解读】**Le problème de démarrage froid du point de départ du LLM sans serveur:70B 模型 de zéro à service nécessite 3-8 minutes 节点供应 45-60s + 容器拉取 120-300s + 权重载 45-120s + 引擎初始化 10-30s), SLA de loin sur 2s ⋅ solution est de conserver la batterie thermos ⋅min_workers=1), mais cela signifie 24/7 支付空 GPU 费用 5 produits ⋅ chaque conserver 1 个热副本, 3600 GPU-hours par mois 无论是否有用户调──

> **【拓展：Serverless LLM 平台对比】**2026 ans Serverless LLM Plateau de la performance de démarrage à froid:Modal 凭借 GPU 快照技术实现 2-4s 冷启动(业界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不包含模型加载);GCP Cloud Run + GPU 较新,冷启动约15-30s── Pour le modèle 70B+ de TTFT P99 < 60s, la thermal pool est obligatoire pas de démarrage à froid optimiser le processus complet dans les années 60──

Votre point final de votre LLM sans serveur passe à zéro au cours de la nuit.

> Vous avez besoin de votre aide pour obtenir un accès à la télévision.

1. Karpenter fournit un nœud GPU: 45-60s.
   Le carpenter fournit une GPU à la base de 45 à 60 secondes.
2. Le conteneur tire une image de 30 Go avec des poids: 120-300s.
   Container à 30 Go de contenu: 120 à 300 secondes.
3. Le moteur charge des poids dans le HBM: 45 à 120s selon la taille du modèle et la vitesse de stockage.
   Le chargement du moteur se fera à HBM:45-120 secondes, en fonction de la taille du modèle et de la vitesse de stockage.
4. VLLM ou TRT-LLM initiale les graphiques CUDA, KV cache pool, jeton: 10-30s.
   Le premier est le premier, le deuxième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième et le troisième.

Total: 220-510s (environ 3 à 8 minutes) avant le retour d'un jeton.`min_workers=1`Si votre service a 5 produits chacun avec une réplique chaude, c'est 5 × 24 × 30 = 3 600 GPU-heures / mois, qu'un seul utilisateur ait appelé ou non.

> 总计:220-510 秒(约 3-8 分钟)才能返回一个代币――你的SLA是2秒――你部署热池(`min_workers=1`) Le problème semble avoir disparu mais maintenant vous avez 24/7 pour un GPU 付费. Si votre service a 5 produits chacun d'une copie chaude, c'est 5 × 24 × 30 = 3.600 GPU-hours/month, peu importe si c'est utile à l'utilisateur.

L'atténuation du démarrage à froid est de garder l'économie sans serveur tout en approximant la latence du toujours-on.

> Le ralentissement du démarrage est le retard du service de démarrage en continuant à être économique sans serveur.

## Le concept de base.

### Couche 1  images de nœuds pré-semencés (Bottlerocket)

> **【中文解读】**Première étape  pré-production                                                                                                                                                                                                                                                          `EC2NodeClass`Le nouveau module a été lancé en NVMe en ligne, ce qui a permis de réduire les étapes de retrait de l'image, ce qui a permis de réduire les coûts de production de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image.

Sur AWS, l'architecture à double volume de Bottlerocket sépare le système d'exploitation des données.`EC2NodeClass`. Les nouveaux nœuds démarrent avec des poids déjà sur le NVMe local  étapes 2 et partie 3 disparaissent. Fonctionne avec Karpenter natively. Économies typiques: 2-4 minutes par démarrage à froid pour les grands modèles.

> Sur AWS, la structure en double volumes de Bottlerocket va séparer le système d'exploitation et les données.`EC2NodeClass`Le poids est déjà en activation à la fois dans le cadre de la mise en œuvre de la nouvelle ligne NVMe.

Équivalent sur GCP: images VM personnalisées avec des couches de conteneurs prépayées. sur Azure: instantanés de disque gérés avec le même motif.

> GCP 等价方案:预容器层的自定义 VM 镜像──Azure:托管磁盘快照加相同模式──

### Couche 2  Modèle de diffusion (Run:ai Modèle Streamer)

> **【中文解读】**Deuxième étape 模型流式加载──NVIDIA Run:ai Model Streamer non besoin等等 l'ensemble du fichier load complet才开始服务, mais va être chargé à niveau par processus de chargement dans le GPU, et le traitement commence après la fin du premier transformateur 块加载──2026年 vLLM 原生支持此功能──兼容 S3、GCS 和本地 NVMe──en passant par la superposition I/O 和计算设置, le temps de chargement des grands modèles peut être réduit de moitié──

Au lieu de charger le fichier complet avant de répondre à la première demande, le flux de poids dans la mémoire GPU couche par couche et commencer le traitement dès que le premier bloc transformateur est résident. Le NVIDIA Run:ai Model Streamer expédite natif dans vLLM 2026. Fonctionne avec S3, GCS et NVMe local. Réduit le temps de charge de poids d'environ la moitié pour les grands modèles en superposant I / O avec la configuration de calcul.

> Il n'est pas nécessaire de répondre à la première demande avant de charger le fichier complet, mais de charger le poids étape par étape dans le GPU et de commencer à le traiter immédiatement après la fin du premier transformateur.

### Couche 3  Snapshots de mémoire GPU (Modal)

> **【中文解读】**Le troisième niveau GPU 内存快照──Modal en première charge 后对 GPU 状态(权重、CUDA graph、KV Cache 区域) faire un point de contrôle, puis reboot directement contre séquence jusqu'à HBM比重启动快10x── c'est la technique la plus proche de "2 secondes de lancement thermo GPU"──代价是快照与 GPU 拓绑定

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减半权重加载时间) + (3) GPU 快照(消除重重加载) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM)。全叠加将 70B 模型从 328s冷启动降至约15s22x 改善。选择哪几层取决于SLA 严格程度和预算。

Modal prend un point de contrôle de l'état de la GPU (poids, graphiques CUDA, région cache KV) après le premier chargement. Les redémarrages ultérieurs désérialisent directement dans HBM  10 fois plus rapidement que la réinitialisation. C'est la chose la plus proche de "démarrer un GPU chaud en 2 secondes".

> Modal en première charge après l'état de la GPU ⋅权重、CUDA graph、KV 缓存区域) faire un point de contrôle──后续重启直反序列化到HBM比重启动快10倍──这是2秒启动热 GPU"最接近的技术──代价:快照与 GPU 拓绑定,如果卡珀特搬迁到不同 SKU 需要重制快照──

### Couche 4  piscines chaudes (min_travailleurs=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026 ans Serverless LLM Plateforme de démarrage à froid performance:Modal utilisant GPU 快照技术实现 2-4s(业界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常 10-30s(不含模型加载);original 70B 模型冷启动 3-8 分钟。Modal 快照技术是关键差异它将 GPU 状态(权重 + CUDA graph + KV Cache 区域)序列化,重启直反序列化到HBM,重启动快速10x。代价是快照与 GPU 拓绑定,迁移到不同 SKU 需要重制快照──

La méthode la plus simple: gardez toujours une réplique prête. Le coût est le taux horaire d'un GPU 24x7.$0.85-$1,50/h pour éviter un démarrage à froid de 30s) et gentils à de grands (payer 4 $/h pour éviter un démarrage à froid de 5 minutes). Le seuil SLA où les piscines chaudes deviennent obligatoires: typiquement TTFT P99 < 60s sur un modèle 70B+.

> Le plus simple des remèdes: garder une copie toujours disponible. Le coût d'un GPU est de 24 heures sur 24.$0.85-$1,50/小时以避免30秒冷启动),大模型则相对友好(付 $4/小时以避免5分钟冷启动)。热池变为强制性SLA 值:

### Couche 5  Chargement à plusieurs niveaux (LLM sans serveur)

ServerlessLLM traite le stockage comme une hiérarchie: NVMe (rapide mais grand), DRAM (médium mais classé), HBM (petit mais instantané). Les poids sont pré-chargés sur DRAM; chargement à la demande dans HBM. Le papier rapporte une réduction de latence de 10-200 fois sur les charges froides par rapport à des naïfs disques à HBM. L'adoption de la production est précoce mais des intégrations avec vLLM existent.

> Le système de gestion de données sans serveur sera stocké en tant que niveau:NVMe(快但大)、DRAM(中等但分层)、HBM(小但即时)。权重预载到DRAM;按需加载到HBM。论文报告冷启动延迟降低 10-200 倍──生产采用尚早,但已存在与vLLM的集成──

### Couche 6  migration en direct (moteur bonus)

Lorsqu'un nœud devient indisponible (éviction de point, drain de nœud), le modèle traditionnel est de démarrer à froid une autre réplique et de drain de requête de file d'attente. La migration en direct déplace les jetons d'entrée (kilobytes) vers une destination qui a le modèle chargé et recompte le cache KV sur la destination. La recomputation est moins chère que le transfert de GB de cache KV sur le réseau. Applicable aux déploiements désagrégés.

> Lorsque le point est inutilisable alors que le point est inutilisable alors que le point est inutilisable alors que le mode traditionnel est de déclencher un autre code de requête.

### Le calcul de la piscine chaude

> **【中文解读】**热池数学: Pour le service de P99 TTFT SLA 为 2s, le problème n'est pas "热池 yes/no" mais "多少热副本、哪些路径需要"──高价值交互路径(实时聊天、语音 Agent)→ min_workers=1-2;后台批处理路径(夜间分类)→ échelle à zéro acceptable;高级层级 → 按租户专用热副本。简单算术:5 个产品各 1 热副本 = 5 × 24 × 30 = 3600 GPU-hours/月, indépendamment de l'utilité de la modification.

Pour un service avec P99 TTFT SLA de 2s, la question n'est pas "poisson chaud oui/non" mais "combien de réplicas chaudes, et quels chemins les obtiennent".

> Pour le P99 TTFT SLA pour 2 secondes de service, le problème n'est pas "la thermal pool oui/non" mais "combien de thermal vice-présentant, quelles routes en ont besoin"

- Volets interactifs à haute valeur (chat en direct, agent de voix): `min_workers=1-2`- Je suis désolé .
  Le mot "réalité" est le mot "réalité".`min_workers=1-2`Il y a une autre.
- Parcours de départ de l'arrière-plan (classification nocturne): accepté à l'échelle de zéro, tolérable à partir de 5 à 10 minutes à froid.
  La réaction de la société à la réaction de l'État est de réduire la capacité de traitement de la production de produits chimiques.
- Niveau de prime: `min_workers`par locataire ayant une capacité dédiée.
  Traduction anglaise:`min_workers`专用容量──

### Mesurer avant d'optimiser

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重到HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

Anatomie à démarrage à froid pour un modèle 70B sur un noeud frais (illustratif):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Les chiffres que vous devriez vous rappeler

- Début à froid modal: 2 à 4 secondes (avec des captures instantanées GPU).
  Modal Coldstart: 2 à 4 secondes
- Baséten démarrage à froid par défaut: 5 à 10 secondes; sous-seconde avec préchauffage.
  Le bassin est un début de la journée.
- Début à froid de 70B: 3 à 8 minutes.
  Le récit de la première partie de la série est un récit de la première partie de la série.
- Retour de mode: 2 fois plus rapide.
  Le modèle de streaming: environ 2 fois le chargement accéléré.
- Chargement en niveaux sans serveurLLM: réduction de la latence de 10 à 200 fois (numéros de papier).
  Le nombre de données de serveurs sans serveur est de 10 à 200 fois plus élevé.

## Utilisez-le avec le cadre de réalisation
```figure
cold-start-pipeline
```

## Utilisez-le

`code/main.py`Les données relatives aux coûts de la piscine chaude et au taux de demande de compensation au-dessus duquel la piscine chaude se paie par elle-même.

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自付自足的亏平衡请求率――

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-cold-start-planner.md`- étant donné la SLA, la taille du modèle et la forme du trafic, choisir les mesures d'atténuation à mettre en place.

> 本课产 出 `outputs/skill-cold-start-planner.md` Donner une SLA  modèle de taille et de circulation, choisir les stratégies de réduction.

## Les exercices

1. On court .`code/main.py`- Calculer le taux de demande de compensation au-dessus duquel une copie chaude est moins chère que le paiement de la taxe de démarrage à froid par des baisses supplémentaires de demande à SLO.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` calculer les frais de paiement par le biais de l'OPS.
2. Vous déployez un modèle 13B avec P99 TTFT SLA de 3s. Choisissez la pile d'atténuation minimale (moins de couches) qui le réalise.
   Vous déployez un modèle 13B, P99 TTFT SLA 为 3 秒──选择实现它的最小缓解(最小层级)──
3. La pré-semission de la bouteille élimine la traction de l'image mais les poids sont toujours chargés de l'imprimé à la HBM.
   Le poids de l'image est toujours à partir du chargement rapide de l'image jusqu'à HBM.
4. Votre fournisseur sans serveur offre des instantanés GPU (Modal) et votre équipe refuse parce que "les instantanés fuissent des PII".
   Le fournisseur de services sans serveur fournit une GPU 快照(Modal), mais le groupe refuse à cause de la " rapid照 divulgation de PII "― Débat les deux parties 实际风险是什么,缓解方案是什么(临时快照、加密、命名空间隔离)?
5. Conceptez une politique de pool chaud à niveaux: combien de réplices chaudes pour les utilisateurs payants, les utilisateurs expérimentaux et les charges de travail de lot?
   Traduction anglaise: design à couche de chaleur stratégies: payer les utilisateurs, les utilisateurs expérimentaux et les opérations de traitement de la masse de charge de chaque pièce ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Encore une lecture

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) Les critères de référence et l'architecture des points de contrôle publiés par Modal.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) modèle d'imagerie du volume de données pré-sémenté.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) charge de poids de chevauchement avec configuration de calcul.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/) Le manuel de préchauffement.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) conception de chargement à plusieurs niveaux.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) migration en direct pour les déploiements décomposés.
