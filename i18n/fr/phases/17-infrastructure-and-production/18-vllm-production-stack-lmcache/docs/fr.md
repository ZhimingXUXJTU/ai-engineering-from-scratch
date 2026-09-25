# VLLM Production Stack avec LMCache KV Déchargement .
# Production Servant Stack  Déchargement KV et routage en cache

> Une production qui sert le routeur, les moteurs et l'observabilité des fils de pile dans un déploiement Kubernetes et traite le cache KV comme une ressource qui peut quitter le GPU. Le déchargement KV extrait le cache KV de la mémoire de la GPU et le réutilise sur les requêtes et les moteurs (DRAM du processeur, puis disque/Ceph). La production-stack de vLLM est le déploiement de référence; LMCache est la couche de déchargement. Le connecteur de déchargement vLLM 0.11.0 KV (janvier 2026) rend ce connecteur asynchrone et branchable via l'API du connecteur (v0.9.0+). Le chemin de déchargement est généralement caché du chemin de la demande, bien que les manquements de cache et les promotions puissent ajouter une latence de bout en bout. LMCache est précieux même sans préfixes partagés  lorsque un GPU se débarrasse des fentes KV, les demandes préemptives peuvent être restaurées à partir du processeur au lieu de recomputer le préchargement. Des benchmarks publiés sur 16x H100 (80 GB HBM) sur 4 a3-highgpu-4g: lorsque le cache KV dépasse le HBM, la décharge de CPU native et le LMCache améliorent considérablement le débit; à faible empreinte KV, toutes les configurations correspondent à la ligne de base avec de petites charges générales.

> **【中文解读】**Ce chapitre présente le vLLM  Recommandation service  PagedAttention 连续批处理和分块预填三大核心优化──
**Type:** Learn
**Languages:** Python (stdlib, toy KV-spill simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang/RadixAttention)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy KV-spill simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention)

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 17 de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre
>  **【类比】**LMCache = "GPU 内存搬家"──KV cache 装不下 HBM → 溢出到 CPU DRAM 再到磁盘──GPU 满时预先 请求可从 CPU 恢复(无需重算预填)──异步、对用户透明──即使无共享前也值──16x H100 référence:KV 超HBM 时大幅升吞;低KV 占用时开销很小──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Diagramme des couches de production de la pile vLLM: routeur, moteurs, déchargement KV, observabilité.
  Le modèle de production de VLLM est le modèle de production de VLLM.
- Expliquez l'API du connecteur de déchargement KV (v0.9.0+) et comment le chemin asynchrone 0.11.0 cache la latence de déchargement.
  Le code de déchargement de connecteurs KV est un code de déchargement de connecteurs KV.
- Quantifier quand le LMCache aide le CPU-DRAM (KV > HBM) par rapport aux coûts généraux (KV suffisamment petit pour s'adapter au HBM).
  Le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
- Choisissez entre le déchargement de CPU vLLM natif et le connecteur LMCache compte tenu des contraintes de déploiement.
  Traduction anglaise: given determin deploy约束, dans le langage original vLLM CPU 卸载和 LMCache 连接器之间选择──

## Le problème , l' introduction du problème

> **【中文解读】**vLLM 推理服务在高并发时 GPU HBM 占满,发生抢占事件请求被逐出、重新排队、同一个2K-token提示一分钟内被重新填充四次。GPU 计算花在冗余预填上,Goodput 远低于原始吞吐──添加更多GPU 是线性成本,但CPU DRAM 很便一个插座有512GB+,延迟虽然比HBM 差几个数级,但对于"临时热"的KV Cache 足够──

> **【拓展：vLLM Production Stack 架构】**La série de production de VLLM est le programme de mise en œuvre de Kubernetes proposé en 2026: 1) le routeur est en cache-connaissance (Phase 17·11), consommer des KV; 2) les moteurs sont utilisés par les travailleurs de VLLM, par GPU ou par TP/PP; 3) le KV Cache est déchargé (LMCache) ou par connecteur de vie; 4) le système de mise en cache (Prometheus + Grafana + OTel) est utilisé pour la mise en cache (Prometheus + Grafana + OTel) et 5) le système de contrôle (Control face à service) est mis en place.

Votre service vLLM affiche les GPU à 100% HBM avec des événements de préemption chaque fois que la concurrence monte. Les demandes sont expulsées, réquisitions et vous remplissez à nouveau la même requête de jeton 2K quatre fois en une minute. Le calcul de la GPU est dépensé sur des pré-remplissages redondants; le rendement est bien inférieur au rendement brut.

L'ajout de plus de GPU coûte linéairement. L'ajout de plus de HBM n'est pas possible. Mais le DRAM de CPU est bon marché  une prise a 512 GB + à des ordres de latence de magnitude pires que HBM mais bien pour le cache KV "temporairement chaud".

LMCache extrait le cache KV dans le DRAM du processeur afin que les demandes préemptées se récupèrent rapidement, et les préfixes répétés à travers les moteurs partagent le cache sans que chaque moteur soit rechargé.

## Le concept de base.

### vLLM série de production

`github.com/vllm-project/production-stack`est le déploiement Kubernetes de référence:

- **Router** cache-conscient (phase 17 · 11). Consomme des événements KV.
- **Engines** travailleurs vLLM. Un par GPU ou par groupe TP/PP.
- **KV cache offload** Déploiement de LMCache ou connecteur natif.
- **Observability**- Prometheus, les tableaux de bord Grafana, les traces OTel.
- **Control plane** Découverte de services, configuration, mises à jour en cours.

Envoyé en tant qu'opérateur Helm chart +.

### L'API du connecteur de déchargement KV (v0.9.0+)

vLLM 0.9.0 a introduit une API Connector pour les backends cache KV branchables. Votre moteur décharge les blocs sur le connecteur; le connecteur les stocke (RAM, disque, stockage d'objets, LMCache).

vLLM 0.11.0 (janvier 2026) ajoute un chemin de déchargement asynchrone  déchargement peut se produire en arrière-plan afin que le moteur ne le bloque pas dans le cas courant. La latence et le débit de bout en bout dépendent toujours de la forme de la charge de travail, du taux de débit de cache KV et de la pression du système; les notes de vLLM indiquent que le débit de noyau personnalisé peut dégrader le débit à faibles taux de débit et que la planification asynchrone a connu des problèmes d'interaction avec le décoding spéculatif.

### Déchargement du processeur natif par rapport à LMCache

> **【中文解读】**两种KV Cache 卸载方案对比:(1) 原生 vLLM CPU 卸载引擎本地,存储KV 块到主机 RAM,实现快速,零网络跳转,但不跨引擎共享;(2) LMCache 连接器集群级,存储块到共享LMCache 服务器(CPU DRAM + Ceph/S3 压层), n'importe quel moteur est accessible.

**Native vLLM CPU offload**: localisé par le moteur. stocke des blocs KV dans la RAM hôte. rapide à mettre en œuvre, zéro saut réseau. Ne croise pas les moteurs.

**LMCache connector**Les blocs sont accessibles à n'importe quel moteur. 16x H100 de référence publiés.

Choisissez natif lorsqu'un seul moteur a une pression HBM. Choisissez LMCache lorsque plusieurs moteurs partagent des préfixes (RAG avec des instructions système communes, multi-locataire avec des modèles partagés).

### Comportement de référence

> **【拓展：LMCache 基准测试数据】**LMCache sur 16x H100(80GB HBM) à travers 4 个 a3-highgpu-4g 基准测试表现:(1) 低KV 足迹(短提示、低并发) 所有配置匹配基线,LMCache 增加~3-5% 开销;(2) 中等足迹LMCache 开始在前复用方面提供帮助;(3) KV 超过HBM原生CPU 卸载和LMCache 显著改善吞吐,LMCache 由于引擎共享收益更大.

Le test H100 16x (HBM de 80 Go) réparti sur 4 a3-highgpu-4g:

- Faible empreinte KV (réponse courte, faible concurrence): toutes les configurations correspondent à la ligne de base, LMCache ajoute ~ 3-5% de frais généraux.
- Modérée empreinte: LMCache commence à aider à réutiliser les préfixes dans les moteurs.
- KV dépasse HBM: déchargement de CPU natif et LMCache améliorent tous deux le débit de manière substantielle; LMCache plus grand gain en raison du partage entre moteurs.

### Lorsque la LMCache est décisive

> **【中文解读】**LMCache dans les scénarios suivants est décisif: 1) 多租户服务系统提示跨租户共享; 2) RAG文档块跨查询重复; 3) 微调变体(LoRA) KV 复用减少冗余工作; 4) 抢占密集型工作负载从CPU 恢复比重新预填 更便宜;;不应启动场景:HBM 压力小(只有开销没有收益) 短上下文(<1K tokens,传输时间 > 重新预填) 单租户单单无复用可捕获提示)

> **【拓展：KV Cache 卸载的集成】**Phase 17·17 Déconnexion service + LMCache: transfert de KV de pré-remplissage à décode de la pile si elle n'est pas immédiatement utilisée, peut être enregistrée dans LMCache; ultérieurement la requête de LMCache 拉取而不是重新 prefill。Phase 17·11 du routeur conscient du cache peut être roulé vers le local ou LMCache avec le même moteur.

- Service multi-locataires où les informations du système sont partagées entre les locataires.
- RAG où les pièces de document se répètent à travers les requêtes.
- Variantes finement ajustées (LoRA) sur la même base où la réutilisation du modèle de base KV réduit le travail redondant.
- Charges de travail lourdes: récupérer à partir de la CPU moins cher que de re-précharger.

### Lorsque N' activer pas

- Petite pression HBM  vous payez les frais généraux sans avantage.
- Contexts courts (tokens < 1K)  temps de transfert > ré-récharge.
- Charge de travail à un seul locataire à une seule demande  aucune réutilisation à capturer.

### Intégration avec une portion décomposée

Phase 17 · 17 serveurs désagrégés + composés LMCache: KV transfère de pré-remplissage pool à décodeur de terre pool dans LMCache si elle n'est pas utilisée; les requêtes ultérieures tirent de LMCache. Phase 17 · 11 routeur conscient de cache peut rouvrir vers le moteur dont le cache local ou LMCache partagé correspond à la cache.

### Les chiffres que vous devriez vous rappeler

- VLLM 0.9.0: API du connecteur expédié.
- vLLM 0.11.0 (janvier 2026): chemin de déchargement asynchrone; impact de latence de bout en bout dépend de la charge de travail, de la vitesse de KV et de la pression du système (pas une garantie absolue).
- 16x H100: LMCache aide lorsque l'empreinte de KV dépasse la HBM.
- Petite pression HBM: 3-5% de frais généraux sans avantage.

## Utilisez-le avec le cadre de réalisation
```figure
zero-sharding
```

## Utilisez-le

`code/main.py`Il est également possible de simuler une charge de travail lourde avec et sans LMCache.

> `code/main.py`Il est également possible de simuler une charge de travail lourde avec et sans LMCache.

> `code/main.py`Il est également possible de simuler une charge de travail lourde avec et sans LMCache.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-vllm-stack-decider.md`. Compte tenu de la forme de la charge de travail et du déploiement de vLLM, décide native vs LMCache vs aucun des deux.

> 本课产 出 `outputs/skill-vllm-stack-decider.md`. Compte tenu de la forme de la charge de travail et du déploiement de vLLM, décide native vs LMCache vs aucun des deux.

## Les exercices

1. On court .`code/main.py`À quelle utilisation de HBM commence LMCache à payer ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`LMCache commence à planifier à quel taux de BPM ?
2. Un locataire partage un système de jeton 6K sur 200 requêtes par heure.
   Une requête / heure en commun de 6K de jetons 系统提示――计算 LMCache 的预期节省――
3. Le serveur LMCache est un point unique d'échec.
   Le système de cache est un simple défaut.
4. Pour un KV 4K à 70B FP8 (500 MB), quel est le temps de lecture par rapport à la pré-remplissage ?
   Pour les 70B FP8 sur 4K jeton KV(500MB), l'écoute retard est combien?
5. Discutez si le chemin asynchrone vLLM 0.11.0 est "libre"  où se cache la tête supérieure?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Production-stack | "the reference deployment" | vLLM's Kubernetes Helm chart + operator |
| Connector API | "KV backend interface" | vLLM 0.9.0+ pluggable KV store interface |
| Native CPU offload | "engine-local spill" | Store KV in host RAM of same engine |
| LMCache | "cluster KV cache" | Cross-engine KV cache server on CPU DRAM + disk |
| 0.11.0 async | "non-blocking offload" | Offload hidden behind engine stream |
| Preemption | "evict to make room" | KV cache shuffle when HBM full |
| Prefix reuse | "same system prompt" | Multiple queries share beginning; cache hit |
| Ceph tier | "disk tier" | Durable storage below DRAM in the cache hierarchy |

## Encore une lecture

- [vLLM Blog — KV Offloading Connector (Jan 2026)](https://blog.vllm.ai/2026/01/08/kv-offloading-connector.html)
- [vLLM Production Stack GitHub](https://github.com/vllm-project/production-stack) Graphique du casque + opérateur.
- [LMCache for Enterprise-Scale LLM Inference (arXiv:2510.09665)](https://arxiv.org/html/2510.09665v2)
- [LMCache GitHub](https://github.com/LMCache/LMCache) Implementation du connecteur.
- [vLLM 0.11.0 release notes](https://github.com/vllm-project/vllm/releases) détails de la trajectoire asynchrone.
