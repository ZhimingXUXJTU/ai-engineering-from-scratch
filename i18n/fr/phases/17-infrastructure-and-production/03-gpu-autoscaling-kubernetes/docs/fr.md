# GPU Autoscaling sur Kubernetes  Karpenter, KAI Scheduler, Scheduling Gang  Automote de l'expansion de Kubernetes  GPU régulateur

> Trois couches, pas une. Les nœuds de fournitures Karpenter sont dynamiques (moins d'une minute, 40% plus rapide que Cluster Autoscaler). KAI Scheduler gère la planification de gang, la prise de conscience de la topologie et les files d'attente hiérarchiques. Il empêche le piège d'allocation partielle 7 sur 8 où sept nœuds attendent et brûlent sur un GPU manquant. Autoscalers au niveau de l'application (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) à l'échelle des signaux spécifiques à l'inférence  profondeur de file d'attente, utilisation du cache KV  pas cycle de travail du processeur / DCGM. Le classique piège de l' HPA est que`DCGM_FI_DEV_GPU_UTIL`est une mesure du cycle de tâche: 100% pourrait être 10 demandes ou 100. vLLM alloue préalablement la mémoire cache KV, de sorte que la mémoire ne déclenche jamais la mise à l'échelle.`WhenEmptyOrUnderutilized`une politique qui met fin à l'exécution de GPU en milieu d'inférence.

> **【中文解读】**Ce chapitre présente les stratégies d'expansion automatique des ressources de la GPU.
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la situation actuelle de la société.
>  **【类比】**GPU 扩缩 = "餐厅运力调度"。Karpenter = 开新店(分钟级);KAI = 桌位组合(gang scheduling 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调座。HPA 陷:DCGM utilisation rate is占空比,100% 可能是10 个或100 个请求必须使用 Goodput(Phase 17·08) 替补。

## Objectifs d'apprentissage

- Décrire les trois couches d'auto-échelle (provisionnement des nœuds, planification des groupes, niveau d'application) et nommer l'outil utilisé à chaque couche.
  Le nom de chaque couche est utilisé pour les outils.
- Expliquez pourquoi .`DCGM_FI_DEV_GPU_UTIL`est le signal HPA incorrect pour vLLM et nomme deux remplacements (profondeur de file d'attente, utilisation de cache KV).
  Pourquoi ?`DCGM_FI_DEV_GPU_UTIL`Il y a deux alternatives à l'utilisation de l'HPA:
- Décrivez la planification des groupes et le mode d'échec de l'allocation partielle que KAI Scheduler empêche (7 GPU sur 8 inactifs).
  Le schedulaire de KAI prévient la distribution de la partie de la défaillance du système de gestion de la carte graphique (GPU)
- Nom de la politique de consolidation de Karpenter (`WhenEmptyOrUnderutilized`) qui met fin à l'exploitation des GPU et déclare l'alternative sûre de 2026.
  Le projet de développement de la GPU est en cours de développement.`WhenEmptyOrUnderutilized`),并说明2026年的安全替代方案──

## Le problème , l' introduction du problème

> **【中文解读】**La GPU s'expande automatiquement sur les Kubernetes avec trois niveaux de défaillance: 1) HPA utilise un signal erroné (à la place du taux de prise de GPU), entraîne une augmentation rapide; 2) Cluster Autoscaler: un point de distribution trop lent, une demande de longueur de temps; 3) plusieurs GPU distribués par une part de réflexion; 7) 7 pièges de 8), 7 GPUs à attendre le 8e.

> **【拓展：GPU 集群管理】**En 2026, Kubernetes est devenu la plateforme de planification standard de services de conseil en droit. NVIDIA DGX Cloud, Google GKE, AWS EKS fournissent des GPUs.

Votre équipe envoie un service de maîtrise de la loi sur Kubernetes.`DCGM_FI_DEV_GPU_UTIL`Les pints de service à 100% utilisation pendant les heures de travail. HPA ne s'élargit jamais  il pense déjà que vous êtes plein. Vous ajoutez une réplique manuellement; TTFT tombe. HPA ne s'élargit toujours pas. Le signal vous ment.

> Votre équipe a déployé un service de Master à Kubernetes.`DCGM_FI_DEV_GPU_UTIL`作为信号设置了HPA──服务在业务时段保持在100%利用率──HPA 从不扩容它认为你已经满满了──你手动添加一副本;TTFT 下降──HPA 仍然不扩容──信号在欺骗你──

Vous utilisez le Cluster Autoscaler pour les nœuds. Une requête de jeton 1M arrive à 2 heures du matin; le cluster passe 3 minutes à fournir un nœud, et les temps de demande sont terminés.

> D'autre part, vous utilisez Cluster Autoscaler 管理节点──凌晨2点来一个M token 的提示;集群花3分钟供给节点,请求超时──

Vous déployez un modèle 70B qui nécessite 8 GPU sur 2 nœuds. Le cluster dispose de 7 GPU gratuits et 1 réparti sur 3 nœuds. Cluster Autoscaler fournit un nœud pour le 1 GPU manquant.

> Encore une fois, vous déployez un modèle 70B de 8 GPU qui nécessite 2 nœuds. Le groupe dispose de 7 GPUs vides, 1 dispersé sur 3 nœuds.

Trois couches, trois modes d'échec différents. L'autoscalage conscient de la GPU en 2026 n'est pas "allumé à HPA". Il compose le provisionnement de nœuds, la planification de gangs et l'autoscalage des signaux d'application.

> Trois niveaux, trois modes de défaillance différents. La GPU de 2026 ne se développe pas automatiquement en " ouvrant HPA " .

## Le concept de base.

### Couche 1  fourniture de nœuds (Karpenter)

> **【中文解读】**Le premier niveau est la fourniture de nœuds. Le pôde de contrôle et de régulation du carpentre, en 45 à 60 secondes, est nécessaire pour créer un nœud GPU, en moyenne 40% de plus que le Cluster Autoscaler traditionnel.`WhenEmptyOrUnderutilized`合并策略它会终止运行推理的GPU节点转移到更便宜的实例类型,导致请求失败和模型重新加载(5-20 分钟中断)。GPU池应使用 `WhenEmpty`+ `consolidateAfter: 1h`La stratégie de sécurité.

Karpenter surveille les pods et les nœuds de provision en attente en 45 à 60 secondes (Cluster Autoscaler prend généralement 90 à 120 secondes pour les nœuds GPU).`NodePool`restriction  si votre module a besoin de 8 H100 et que le cluster n'a pas de nœud correspondant, Karpenter fournit un directement au lieu d'échelonner un groupe existant.

> Carpenter  surveillance et régulation du Pod, en environ 45-60 secondes pour fournir des points de commande  Cluster Autoscaler pour les points de GPU  nécessite généralement 90-120 secondes `NodePool`约束动态选择实例类型 Si votre Pod 需要8 H100 且集群没有匹配节点,Karpenter 直接供应一个,而不是扩展现有组──

**The consolidation trap**: Le défaut de Karpenter `consolidationPolicy: WhenEmptyOrUnderutilized`Il met fin à un nœud de GPU en cours d'exécution pour migrer les pods vers une instance de taille plus économique. Pour les charges de travail d'inférence qui signifient évacuer les demandes en cours d'exécution et reloader un modèle 70B sur le nouveau nœud.

> **合并陷阱**Carpenter est un homme de bien.`consolidationPolicy: WhenEmptyOrUnderutilized`Pour la GPU, la batterie est dangereuse. Elle met fin à la GPU en cours de fonctionnement, et le Pod est transféré à un exemple plus économique. Pour la charge de travail de calcul, cela signifie que la demande est déchargée et rechargée sur le nouveau module.

Configuration sécurisée pour les pools GPU:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Laissez Karpenter consolider des nœuds vraiment vides après une heure mais ne jamais expulser un emploi en cours.

> 让卡珀特在一小时后合并真正空的节点,但永不驱逐运行中的任务──

### Couche 2  planification des gangs (KAI Scheduler)

> **【中文解读】**Le deuxième niveau est la coordination de la régulation. Le schedulaire KAI résoudre les trois problèmes par défaut: 1) la régulation de gang  totalement inégalée, 8-GPU                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

> **【拓展：GPU 调度器生态】**Le scheduler de GPU de 2026 comprend le scheduler de KAI ((orig Karp, support gang + topologie + file d'attente) 、UniKorn ((Apache 项目, support queue et抢占) 、 ainsi que le scheduler par défaut kube-scheduler + 设备插件。KAI Scheduler est le seul scheduler de scheduling de gang original, déjà utilisé par Ray 和 vLLM production-stack 集集团── pour le besoin de GPU distribué en plusieurs scénarios de suggestion(70B+ 模型),KAI est un choix indispensable──

KAI Scheduler (projet "Karp" renommé ensuite) gère ce que le kube-scheduler par défaut ne fait pas:

**Gang scheduling**Un module d'inférence distribuée nécessitant 8 GPU ou les 8 démarrent ensemble ou aucun ne le fait. Sans cela, vous obtenez le piège de l'allocation partielle: 7 des 8 pods démarrent, attendent indéfiniment, brûlent de l'argent.

**Topology awareness** savoir quels GPU partagent NVLink, qui sont sur le même rack, qui ont InfiniBand entre eux. Placez les pods en conséquence.

**Hierarchical queues** Plusieurs équipes se disputent pour le même pool de GPU avec priorité et quota.

KAI est déployé à côté de kube-scheduler comme un scheduler secondaire; vous annoterez les charges de travail pour l'utiliser.

> KAI 作为二级调度器和 kube-scheduler 一起部署;你通过注解让工作负载使用它──Ray 和 vLLM production-stack 都已集成──

### Couche 3  Signes au niveau de l'application

> **【中文解读】**Le troisième niveau est l'application des signaux.`DCGM_FI_DEV_GPU_UTIL`Le taux de débit de la GPU (cycle de tâche) est de 100%, ce qui signifie peut-être 10 demandes ou 100 demandes, car la GPU est occupée.

> **【拓展：推理感知自动扩缩】**NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler est un élargissement spécialisé en 2026 pour le design de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels

**The HPA trap**Le numéro de la liste:`DCGM_FI_DEV_GPU_UTIL`est une métrique du cycle de tâche  il mesure si le GPU faisait du travail à chaque intervalle d'échantillonnage. 100% utilisation pourrait signifier 10 demandes concurrentes ou 100; le GPU était occupé de toute façon.

Pire encore, les moteurs vLLM et similaires préalloquent la mémoire cache KV (jusqu'à `--gpu-memory-utilization`L'utilisation de la mémoire reste proche de 90% même à une seule demande.

**2026 replacement signals**- Le numéro de la liste:

- Profondeur de file d'attente (nombre de demandes attendues pour le remplissage préalable).
  En français, la requête est complète.
- Utilisation de cache KV (quelle fraction de blocs est allouée aux séquences actives).
  Le taux d'utilisation de la réserve de données est le taux de stockage de données de la réserve de données.
- Le signal de votre SLA est TTFT P99 par réplique.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Goodput (demandes de remplacement de tous les SLO par seconde).
  Le nombre de requêtes de SLO satisfaites par seconde est de 7 à 7 fois plus élevé.

NVIDIA Dynamo Planner et llm-d Workload Variant Autoscaler consomment ces signaux et réplices d'échelle. Ils remplacent entièrement HPA pour le service LLM.

> NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本──它们完全取代了LLM 服务中的HPA──

### Quand utiliser quoi

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】**L'optimisation des coûts de GPU en groupe pour 2026 est la suivante: 1) L'exemple de GPU Spot de Spot InstanceAWS/GCP/Azure peut être économisé à 60 à 70%, mais nécessite un arrêt de traitement(Carpenter + 热池缓解); 2) L'expansion automatique du Carpenter en période de non-haut sommet réduit automatiquement la taille du point de débit, à 50% de la consommation d'épargne; 3) Le GPU commun partage à travers le MIG (Multi-Instance GPU) va diviser le H100 en plusieurs exemples, adaptés à un petit modèle de GPU; 4) L'hybridation du GPU FP8/INT4 réduit la quantité de stockage, permettant plus de déploiement; 5) Le déploiement séparé prefill/decode divisé en différents types de GPU, à 30 à 40% de la production de données.

### Le pré-remplissage/décodage décomplexe tout

> **【中文解读】**La phase 17·17 augmente encore la complexité de l'expansion: le pré-expansion de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de la chaîne de répartition de répartition de la chaîne de répartition de répartition de la chaîne de répartition de répartition de la chaîne de répartition de répartition de la chaîne de répartition de répartition de répartition de la chaîne de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition de répartition

> **【拓展：Kubernetes GPU 生态】**Les principaux composants de la gestion de la GPU Kubernetes de 2026 sont: NVIDIA GPU Operator (en anglais seulement)  NVIDIA Device Plugin (en anglais seulement)  NVIDIA Device Plugin (en anglais seulement)  NVIDIA Device Plugin (en anglais seulement)  MIG (en anglais seulement)  Multi-Instance GPU, qui sera divisé en plusieurs exemples)  GPU 共享 (en anglais seulement)  Link Karpenter + KAI Scheduler + Dynamo Planner, qui peut être réalisé à partir de l'élément donné à la Pod 调度 jusqu'à la gamme complète de GPU automatiquement agrandie 

Si vous exécutez des classes de pré-remplissage/décodage désagrégées (phase 17 · 17), vous avez deux classes de pods avec des déclencheurs d'échelle différents: échelle de pods de pré-remplissage sur la profondeur de la file d'attente, échelle de pods de décode sur la pression de cache KV. llm-d les expose séparément `Services`Ne tentez pas de mettre un seul HPA devant les deux.

> Si vous utilisez une fonction de séparation préchargement/déchargement (Phase 17 · 17), vous avez deux types de capteurs de déchargement différents:`Services`Chaque rôle a son propre HPA. Ne tentez pas de mettre un seul HPA devant les deux.

### Le début à froid est aussi important ici.

L'atténuation du démarrage à froid (phase 17 · 10) est le moment où le temps de mise en service des nœuds devient visible pour l'utilisateur.`min_workers=1`) pour les chemins critiques de la SLO, ou utiliser le point de contrôle modal à la couche d'application.

> La phase 17 · 10) est le temps de fourniture du point de départ de l'utilisateur à l'intérieur du centre de travail.`min_workers=1`), ou dans l'application de la mise en œuvre de la méthode de contrôle.

### Les chiffres que vous devriez vous rappeler

- Prévoyance de nœuds de carpenter: ~ 45-60s vs Cluster Autoscaler ~ 90-120s (nœuds GPU).
  Le carpenter est un appareil de mesure de la taille de l'appareil.
- Le schedulaire KAI empêche la prise de déchets partagés  7 sur 8.
  Le programmeur de KAI 防止部分分配浪费7 des 8 pièges。
- `DCGM_FI_DEV_GPU_UTIL`comme signal HPA: cassé; utilisez la profondeur de file d'attente ou l'utilisation de KV.
  Le mot grec traduit par " le mot grec "`DCGM_FI_DEV_GPU_UTIL`作为 HPA 信号:有缺陷; utiliser la profondeur de la ligne de bord ou le taux d'utilisation de la VK。
- Carpenter `WhenEmptyOrUnderutilized`: met fin à l'exécution des tâches de GPU.`WhenEmpty + consolidateAfter: 1h`Pour des inférences.
  Le carpenter`WhenEmptyOrUnderutilized`: Termin止运行中的 GPU 任务──推理使用 `WhenEmpty + consolidateAfter: 1h`Il y a une autre.

## Utilisez-le avec le cadre de réalisation

> **【拓展：GPU 自动扩缩成本模型】**Le cœur de l'optimisation des coûts de l'expansion automatique de la GPU est la réduction du temps de transfert.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17,280 ⋅ par Karpenter 按需供应 + `WhenEmpty`合并策略 + 推理感知 HPA, pouvant être automatiquement réduit à 2 GPU pendant la période non-haute, le coût mensuel diminuera à environ 8 640 $ (environ 50%) .
```figure
autoscaling
```

## Utilisez-le

`code/main.py`Simulation d'une échelle automatique à trois couches sur une charge de travail de GPU éclatée. Compares HPA naïf (cycle de travail), HPA de profondeur de file d'attente et escalage programmé par KAI-gang. Rapporte les demandes non satisfaites, minutes de GPU inactives et un score composite.

> `code/main.py`En outre, le nombre de requêtes non satisfaites de la GPU est de plus de 0,5% en moyenne.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-gpu-autoscaler-plan.md`. Compte tenu de la topologie du cluster, de la forme de la charge de travail et de la SLO, il conçoit un plan d'auto-échelle de trois couches.

> 本课产 出 `outputs/skill-gpu-autoscaler-plan.md` la forme et la charge de travail, la conception de trois niveaux de schéma d'expansion automatique.

## Les exercices

1. On court .`code/main.py`Dans une charge de travail intense, combien de demandes de HPA naïfs du cycle de travail font tomber les captures de HPA en profondeur de file d'attente ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Dans le cadre de la charge de travail, le taux de participation simple de l'APH a été abandonné.
2. Conception d'un Carpenter NodePool pour un cluster desservant Llama 3.3 70B FP8 sur H100 SXM5.`capacity-type`- Je suis là .`disruption.consolidationPolicy`- Je suis là .`consolidateAfter`, et une tache qui empêche les charges de travail non GPU de ces nœuds.
   Pour le H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool──指定 `capacity-type`- Je suis là.`disruption.consolidationPolicy`- Je suis là.`consolidateAfter`和将非 GPU 工作负载隔离的污点──
3. Votre équipe rapporte que les déploiements sont bloqués dans l'attente parce que "GPUs disponibles mais la capsule ne planifie pas". Diagnose  est-ce Karpenter, kube-scheduler, ou KAI Scheduler?
   Le rapport de votre équipe est en attente car "GPU disponible mais Pod 无法调度"
4. Choisissez un signal pour les pods de remplissage pré-réparties à l'échelle automatique et un autre signal pour les pods de décode.
   Choisir un signal pour agrandir le Pod, un autre signal pour déchiffrer le Pod.
5. Calculer le coût de la `WhenEmptyOrUnderutilized`Trappe de consolidation sur un service de production 24x7 qui a en moyenne 60 événements de réduction des demandes par jour à P99 TTFT > 10s.
   Le mot grec traduit par " calcul "`WhenEmptyOrUnderutilized`Le coût du service de production 24x7 est en moyenne de 60 fois par jour, P99 TTFT > 10 secondes.

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Encore une lecture

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) documents de conception et exemples de configuration.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) la sémantique de la politique de consolidation et les défauts sécurisés par les GPU.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) Dynamo Planner étalant les signaux.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) Modèle d'intégration des rayons.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) orientation spécifique à Kubernetes gérée.
- [llm-d GitHub](https://github.com/llm-d/llm-d) Conception de la variante de charge de travail Autoscaler.
