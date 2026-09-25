# Décomposé / Décodage décomposé  NVIDIA Dynamo et llm-d  分离式 预填充 解码 LLM

> Le pré-remplissage est lié à l'informatique; le décode est lié à la mémoire. Exécuter les deux sur le même GPU gaspille une ressource. La désagrégation les divise en pools séparés et transfère le cache KV entre eux sur NIXL (RDMA/InfiniBand ou TCP fallback). NVIDIA Dynamo (GTC 2025 annonce, 1.0 GA) est situé au-dessus de vLLM/SGLang/TRT-LLM  son Planner Profiler + SLA Planner pré-remplissage automatique-match:décode pour répondre aux SLO. NVIDIA publie des gains de débit dans ce stade  developer.nvidia.com (2025-06) montre une amélioration de ~6x pour DeepSeek-R1 MoE sur GB200 NVL72 + Dynamo dans le régime de latence moyenne, et la page de produit Dynamo (developer.nvidia.com, non datée) annonce jusqu'à 50x de débit MoE sur GB300 NVL72 + Dynamo vs Hopper. Le chiffre "30x" est un agrégat communautaire sur les rapports Blackwell + Dynamo + DeepSeek-R1 à pile complète; nous n'avons pas trouvé de source primaire indiquant exactement 30x, alors traitez-le comme une revendication directionnelle. llm-d (Red Hat + AWS) est Kubernetes natif: pré-remplir / décoder / routeur comme services indépendants avec HPA par rôle. llm-d 0.5 ajoute un déchargement KV hiérarchique, un routage LoRA conscient du cache, un réseau UCCL, une échelle à zéro. Économie: le déploiement interne de plusieurs informations sur les clients suggère des économies de 3040% sur $2M-class inference spend (i.e., $600-800 K/an) lors du passage d'une portion en collage à une portion décomposée avec Dynamo à un SLA constant;$2M→$Le chiffre 600-800K est un composite interne, pas une seule étude de cas publiée  l'utiliser comme un ordre de grandeur ancre, pas une citation de référence.

> **【中文解读】**Ce chapitre présente la séparation du préchargement/décompression des éléments de la phase de préchargement et du décode des éléments de la phase de séparation en différents éléments.
**Type:** Learn
**Languages:** Python (stdlib, toy disaggregated-vs-colocated simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 08 (Inference Metrics)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy disaggregated-vs-colocated simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 08 (Inference Metrics) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 08 (Inference Metrics)

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 17 de la mise en cache.
>  **【类比】**Le même GPU 跑两者 = 厨师又做又菜端菜,浪费某种资源──Dynamo/llm-d 把两者分池,KV cache 通过NIXL(RDMA) 传输──NVIDIA发布:DeepSeek-R1 在 GB200+Dynamo 提速 ~6 倍;GB300+Dynamo MoE 吞吐最高50 倍──$2M 推理账单可省 30-40%（即 $600-800K/an)。短请求(<512 jeton) 不值得──
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objectifs d'apprentissage

- Expliquez pourquoi les précharges et les décodés ont des allocations GPU optimales différentes et quantifiez les déchets sous colocation.
  Expliquer pourquoi le préchargement et le code ont des GPU différentes, et la distribution et la quantification des ressources de la position.
- Diagramme de l'architecture décomposée: pré-remplissage, décodeur, transfert de KV via NIXL, routeur.
  Le code de la carte est le code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
- Nombre de conditions dans lesquelles la désagrégation ne porte pas ses fruits (indications courtes, sorties courtes).
  Le texte de la déclaration de l'État de l'Union européenne est en cours de révision.
- Distinguer NVIDIA Dynamo (stack-above) de llm-d (Kubernetes-native) et correspondre chacun à un contexte opérationnel.
  Le premier est le premier, qui est le premier, qui est le premier, qui est le premier.

## Le problème , l' introduction du problème

> **【中文解读】**Le problème central du préchargement/décompression de la GPU est que le préchargement est calculé limité, le décode est limité à la mémoire, les deux fonctionnent sur le même GPU et perdent une ressource.

> **【拓展：分离式推理的经济学】**Économie de la décentralisation: données globales internes montrent que le passage du service de décentralisation à Dynamo permet de réaliser des économies de 30 à 40% en tenant compte du même P99  retard SLA$2M 年支出可节省 $600-800K/year) ――Baseten  rapport Dynamo KV routage 带2x 更快 TTFT 和 61% 更高吞吐──关键条件:提示 >512 tokens + 输出 >200 tokens 时才值得分离短提示的 KV 传输开销超过收益──

Vous exécutez Llama 3.3 70B sur 8 H100. Sous une charge de travail mixte (longues demandes + courtes sorties), les GPU sont inactifs pendant le décode parce que la plupart du calcul a été dépensé sur le pré-remplissage. Sous une charge de travail différente (courts demandes + longues demandes), il se passe le contraire.

> **【中文解读】**
> Le préempiler est un type de calcul intensif, le traitement de l'ensemble du prompt, le décode est un type de calcul intensif, chaque jeton ne fait que faire peu de calcul. La même GPU fonctionne à deux, il y a toujours une sorte de ressources gaspillées.

L'impact budgétaire: 20 à 40% du temps de la GPU est gaspillé sur la mauvaise ressource. Vous achetez un calcul H100 pour exécuter le décodeur lié à la mémoire, ou achetez une bande passante H100 HBM pour exécuter le préchargement lié au calcul.

La désagrégation divise le pré-remplissage et le décodeur en pools séparés de taille pour chaque goulot d'étranglement.

## Le concept de base.

### Pourquoi les écarts de contrôle diffèrent

**Prefill** exécuter le transformateur sur le prompt d'entrée complet dans un avant. Les multiplications de matrice dominent; en fonction de l'informatique. H100 FP8 donne ~ 2000 TFLOPS de débit utile. L'efficacité du lot est bonne  un avant traite de nombreux jetons.

**Decode** générer un jeton à la fois, en lisant les poids complets à chaque itération. La mémoire-largeur de bande est limitée. HBM3 donne ~ 3 TB/s. L'efficacité du lot est bonne uniquement à haute simultanéité  les poids lus amortize à travers le lot.

Leur colocation: vous achetez des GPU optimisées pour les deux. H100 est bon pour les deux mais coûte le même en tous les cas. À l'échelle, vous voulez un bassin de pré-remplissage sur H100 / calcul-cheveux; décodeur bassin sur H200 / mémoire-cheveux, ou avec quantification agressive.

### L'architecture

```
            ┌──────────────┐
  Request → │    Router    │ ───────────────────────┐
            └──────┬───────┘                        │
                   │                                │
                   ▼ (prompt only)                  │
            ┌──────────────┐    KV cache    ┌───────▼──────┐
            │ Prefill pool │ ─── NIXL ────► │ Decode pool  │
            │  (compute)   │                │  (memory)    │
            └──────────────┘                └──────┬───────┘
                                                   │ tokens
                                                   ▼
                                                 Client
```

NIXL est le transport internode de NVIDIA. Utilise RDMA/InfiniBand quand il est disponible, TCP fallback autrement. La latence de transfert est réelle  typiquement 20-80 ms pour le cache KV d'un prompt 4K-token sur 70B FP8.

### Dynamo contre Illm-d

> **【中文解读】**两种分离式推理框架对比:(1) NVIDIA Dynamo位于 vLLM/SGLang/TRT-LLM 之上的编排器,Rust 核心 + Python 扩展,Planner Profiler 自动配置预填:decode 比如,在 GB200 NVL72 + DeepSeek-R1 MoE 上报告 6x 吞吐提升;(2) llm-d(Red Hat + AWS) Kubernetes 原生,prefill/decode/router 作为独立服务,per-role HPA,`packDomain: rack`确保同一机架内的高带宽 KV 传输──选 Dynamo 如果想要托管编排器,选 llm-d 如果承诺到 CNCF 生态──

**NVIDIA Dynamo**(annonce de la CGD 2025, 1.0 GA):
- Assise au-dessus de VLLM, SGLang, TRT-LLM en tant qu'orchestre.
- Le profilateur de planificateur mesure la charge de travail, le planificateur de SLA configure automatiquement les ratios de pré-remplissage: décode.
- Le noyau de rouille, l'extensibilité de Python.
- Gains de débit: NVIDIA rapporte 6x pour DeepSeek-R1 MoE sur GB200 NVL72 + Dynamo dans le régime de latence moyenne (developer.nvidia.com, 2025-06); les rapports communautaires de "jusqu'à 30x" sur les piles complètes Blackwell + Dynamo + DeepSeek-R1 manquent d'une seule source primaire et devraient être traités comme directionnels.
- GB300 NVL72 + Dynamo: jusqu'à 50 fois le débit MoE par rapport à Hopper par page de produit Dynamo (développer.nvidia.com, non daté).

**llm-d**(Red Hat + AWS, natif de Kubernetes):
- Remplissez / décodez / routeur en tant que services Kubernetes indépendants.
- HPA par rôle avec des signaux de profondeur de file d'attente (préchargement) / utilisation KV (décodage).
- `topologyConstraint packDomain: rack`les paquets de pré-remplissage+décodage cliques sur le même rack pour le transfert de KV à haute bande passante.
- Ilm-d 0.5 (2026): déchargement hiérarchique de KV, routage LoRA conscient du cache, réseautage UCCL, échelle à zéro.

Utilisez Dynamo si vous voulez un orchestrateur géré par la pile, ou llm-d si vous voulez des primitifs natifs Kubernetes et engagés dans l'écosystème CNCF.

### Économie

Composite interne (pas une seule étude de cas publiée  ancrage d'ordre de grandeur):

- 2 millions de dollars par an sont dépensés pour les portions en collage.
- Passer à désagrégé avec Dynamo.
- Le même volume de demande, le même SLA de latence P99.
- Économies déclarées: $600K–$800 000 par an (30% à 40% de réduction).
- Pas de matériel nouveau.

Nous synthétisons ce chiffre à partir de plusieurs divulgations de clients plutôt qu'une seule étude de cas citable; le point de données publié le plus proche est le TTFT 2x plus rapide de Baseten / 61% de débit plus élevé avec le routage Dynamo KV (baseten.co, 2025-10), et la projection de VAST + CoreWeave de 60130% de jetons / $ de plus à 4060% KV taux de succès (vastdata.com, 2025-12). Les économies sont dues à la taille correcte de chaque piscine; les charges de travail lourdes à remplir en pré-emplacement (RAG avec préfixes 8K+) bénéficient davantage que les charges équilibrées.

### Lorsque ne pas être décomposé

> **【拓展：分离式推理的适用条件】**La différence entre les deux types de GPU est que le groupe n'a pas pu exploiter deux GPUs en fonction de leur rôle, mais il n'est pas simple. Il n'y a pas de réseau de RDMA TCP 输送税更重.

- Les impôts < 512 jetons et les sorties < 200 jetons: l'impôt sur les transferts domine les gains.
- Petit cluster (< 4 GPU): insuffisante diversité de piscine.
- L'équipe ne peut pas exploiter deux pools GPU avec une mise à l'échelle par rôle: Dynamo aide mais pas triviellement.
- Aucun tissu RDMA: la taxe de transfert TCP est plus lourde.

### Le routeur s'intègre à la phase 17 · 11

Les routeurs désagrégés sont conscients du cache KV (phase 17 · 11). Une demande atterrit sur le pool de décode contenant son préfixe  si aucune correspondance, il déplace préfill → décode.

### Le MoE sur Blackwell est où les chiffres réels sont

> **【中文解读】**Le modèle MoE (Modeux Mixte) est le plus grand bénéficiaire de la décomposition de Blackwell. Le routage d'experts MoE est calculé en phase pré-remplissage, le décodage en phase cache est en phase cache, de sorte que le décomposition est à double portée. Le service de modèle avant-coureur de 2026 est basé sur le MoE.

> **【拓展：分离式推理与缓存路由的协同】**Le routeur de la logique de déconnexion est KV-cache-conscient de la phase 17·11) ⋅ demande d'arriver au décodage 池时, si il y a déjà un cache, peut être directement copié sans avoir à passer par le pré-remplissage 池命中率 avec le déploiement de déconnexion ⋅ NIXL est le NVIDIA's node间传输层, en utilisant RDMA/InfiniBand (la plupart du temps disponible) ou TCP 回归──4K-prompt KV dans 70B FP8 ⋅ le délai de transmission est d'environ 20-80ms ⋅ c'est la raison de la mise en garde de la déconnexion ⋅

Le routage expert MoE est lourd en calcul sur le pré-remplissage mais lourd en mémoire sur le décodeur (caches experts), de sorte que la désagrégation est une double victoire. Le modèle frontalier de 2026 est le modèle dominant MoE (DeepSeek-V3, futures variantes GPT-5).

### Les chiffres que vous devriez vous rappeler

Les chiffres de référence dérivent  NVIDIA et la pile d'inférence publient des résultats mis à jour chaque trimestre.

- DeepSeek-R1 sur GB200 NVL72 + Dynamo: ~6x débit par rapport à la ligne de base dans le régime de latence moyenne (developer.nvidia.com, 2025-06); les revendications communautaires "jusqu'à 30x" sur les piles Blackwell + Dynamo complètes sont des agrégats directionnels sans source primaire unique.
- GB300 NVL72 + Dynamo: jusqu'à 50 fois le débit MoE par rapport à Hopper (développer.nvidia.com, non daté).
- Ancrage d'épargne (composite interne, pas une seule étude de cas): $600-800K/year off a $2 millions de dépenses annuelles à un taux constant de SLA.
- Le seuil de désagrégation: les commandes > 512 jetons + les sorties > 200 jetons.
- Transfert de KV par NIXL: 20 à 80 ms pour KV 4K-prompt sur 70B FP8.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**
> Le projet de développement de la société est un projet de développement de la société NVIDIA Dynamo. Il s'agit d'un projet de développement de la société NVIDIA Dynamo.

> **【拓展：分离式推理→下一代基础设施】**Le projet de répartition de la technologie de l'entreprise NVL72 de NVIDIA est une priorité de l'infrastructure de l'LLM de 2026: un modèle de répartition de la technologie NVL72 de NVIDIA est spécialisé dans le pré-remplissage/décodage de la conception de répartition de la technologie.
```figure
prefill-decode-split
```

## Utilisez-le

`code/main.py`Simulation de la portion coloquée par rapport à celle désagrégée.

> `code/main.py`Simulation de la portion coloquée par rapport à celle désagrégée.

> `code/main.py`Simulation de la portion coloquée par rapport à celle désagrégée.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-disaggregation-decider.md`- compte tenu de la charge de travail et du cluster, décide de découpler ou non.

> 本课产 出 `outputs/skill-disaggregation-decider.md`- compte tenu de la charge de travail et du cluster, décide de découpler ou non.

## Les exercices

1. On court .`code/main.py`À quelle longueur rapide la désagrégation va-t-elle surpasser la colocation ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Dans quelles conditions la déploiement de la division est-il supérieur à celui du service de la division ?
2. Conceptualiser le pool de pré-remplissage et le pool de décode pour un service RAG avec un préfixe P99 de longueur 8K, sortie 300.
   Pour la première fois, le système de gestion de la zone de production de gaz aérien a été mis en place pour les entreprises de production de gaz.
3. Dynamo vs llm-d: choisissez un magasin pur Kubernetes sans préférence pour le temps d'exécution Python.
   Synopsis: Pour les Kubernetes, pas de Python.
4. Comptez le coût de transfert de KV: 4K préchargement sur 70B FP8 = ~ 500 MB KV. À RDMA 100 GB/s, transfert = 5 ms. À TCP 10 GB/s = 50 ms. Qu'est-ce qui compte pour votre SLA?
   Le nombre de KV 转移成本: 70B FP8 上 4K 预填充 = environ 500MB KV──RDMA 100 GB/s 下传输 = 5ms──是否被解码延迟隐藏?
5. Comment la désagrégation se comporte-t-elle avec le MoE qui active différents experts par jeton ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Disaggregated serving | "split prefill/decode" | Separate GPU pools for each phase |
| NIXL | "NVIDIA transport" | Dynamo's inter-node KV transfer (RDMA/TCP) |
| NVIDIA Dynamo | "the orchestrator" | Stack-above coordinator for vLLM/SGLang/TRT-LLM |
| llm-d | "Kubernetes native" | Red Hat + AWS K8s disaggregated stack |
| Planner Profiler | "Dynamo auto-config" | Measures workload, configures pool ratios |
| SLA Planner | "Dynamo policy" | Auto-rate-matches prefill:decode to meet SLOs |
| `packDomain: rack` | "llm-d topology" | Pack prefill+decode on same rack for fast KV |
| UCCL | "unified collective" | llm-d 0.5 networking layer for scale-to-zero |
| MoE expert routing | "expert per token" | DeepSeek-V3 pattern; disaggregation helps |

## Encore une lecture

- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/)
- [TensorRT-LLM Disaggregated Serving blog](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog5_Disaggregated_Serving_in_TensorRT-LLM.html)
- [llm-d GitHub](https://github.com/llm-d/llm-d)
- [llm-d 0.5 release notes](https://github.com/llm-d/llm-d/releases)
