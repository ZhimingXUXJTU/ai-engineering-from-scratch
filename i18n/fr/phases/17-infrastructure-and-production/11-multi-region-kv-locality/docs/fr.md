# MLL multi-régions Servir et KV cache Localisation  多区域 局部性 服务 MLL KV

> L'équilibrage de la charge en round-robin est activement nocif pour l'inférence de la MLL en cache. Une demande qui ne débarque pas sur le nœud contenant son préfixe paie le coût de remplissage complet  environ 800 ms à P50 sur une longue demande par rapport à ~80 ms avec un cache hit. En 2026, le modèle de production est un routeur conscient du cache (vLLM Router in Rust, llm-d router) qui consomme des événements de cache KV et des routes sur le préfixe-hash match. Des recherches récentes (GORGO) font de la latence réseau interrégionale un terme explicite dans l'objectif de routage. Les offres commerciales d'"inférence transregionale" (inférence transregionale Bedrock, passerelles multi-cluster GKE) traitent l'inférence comme opaque  elles gèrent la disponibilité, pas le TTFT. JPMorgan et la Mayo Clinic ont fait une défaillance de l'East-1 en novembre 2024 à 22 minutes. La réalité de la DR: 32% des échecs de la DR LLM sont dus à ce que les équipes aient sauvegardé des poids mais ont oublié des fichiers de jeton ou des configurations de quantification.

> **【中文解读】**Ce chapitre présente les stratégies d'optimisation du cache de KV de la MLL 时的多区域 KV 局部性跨区域部署


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)

>  **【前置】**Pour les autres, il est nécessaire de mettre en place un système de gestion de la zone de détection de données.
>  **【类比】**L'équipe de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Expliquez pourquoi les ruptures de balance de charge en rouleau ont mis en cache l'inférence et quantifiez la sanction TTFT.
  Le système de gestion de la charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de charge de
- Diagramme d'un routeur conscient du cache: entrées (événements de cache KV), algorithme (partie de préfixe-hash), coupe-coupe (utilisation de GPU).
  Le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
- Nombre du pilote d'échec de DR de 32% pour les LLM (fichiers de jetonnisation manquants / configurations de quantification) et indiquez une liste de contrôle de DR de trois fichiers.
  Le texte de la loi est écrit en français et en français.
- Distinguer les offres commerciales trans-régionales (Bedrock CRI, GKE Multi-Cluster Gateway) de l'itinérance KV.
  Le système de communication de la communication est basé sur la communication de données.

## Le problème , l' introduction du problème

> **【中文解读】**Les trois problèmes principaux du service de LLM sont les suivants: 1) l'équilibre de charge de la demande par le caché KV a perturbé la localisation, entraînant une baisse du taux de caché de 70% à 8%; 2) le défaut de la DR DR de 32% est dû au fait que l'équipe a enregistré un poids de file ou une configuration quantifiée, mais a oublié la configuration des fractions de mot de passe; 3) le Réservation des données par le RGPD exige que les données des utilisateurs ne puissent pas quitter l'UE, le routeur en cache ne peut pas répondre à la demande des utilisateurs de Paris par le chemin de l'Est des États-Unis-1:

> **【拓展：多区域推理的产业实践】**Les meilleures pratiques de la mise en œuvre de la MLL dans de nombreuses régions de 2026 comprennent: 1) Chaque région 独立的缓存-aware router(vLLM Router / llm-d router), évitez le KV 转移的跨区域高延迟(US-EU RTT 约75ms,US-APAC 约220ms);(2) GORGO Research will网络延迟作为路由目标的显式项联合优化 prefill_time + network_latency;(3) Bedrock cross-region inference 和 GKE Multi-Cluster Gateway 处理可用性, but you don't process TTFT you still need to apply layer layer cache-aware router;;

Votre service fonctionne dans US-East-1, US-West-2 et eu-West-1. Vous mettez un ALB devant avec round-robin. Le taux de préfixe cache de la production diminue à 8%. TTFT P50 triplé. Vos journaux vLLM montrent que chaque demande est payante le coût de remplissage complet.

> Vous êtes en face de la demande de livraison de la production de la première tranche de la production de la première tranche de la production de la première tranche de la production de la première tranche de la production de la première tranche de la tranche de la production de la première tranche de la tranche de la production de la première tranche de la tranche de la production de la tranche de la production de la première tranche de la tranche de la production de la tranche de la production de la tranche de la tranche de la production de la première tranche de la tranche de la production de la tranche de la tranche de la production de la tranche de la tranche de la production de la tranche de la tranche de la tranche de la tranche de la production de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de la tranche de tranche de la tranche de tranche de la tranche de tranche de la tranche de tranche de tranche de la tranche de la tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tranche de tran

Le round-robin est optimal pour les services sans état. L'inference LLM est stateful par conception  le cache KV encode tout ce que le modèle a vu.

> 轮询负载均衡对无状态服务优优――LLM 推理自然是有状态的KV 缓存编码了模型看到的所有内容――盲路由就是路由到错误的缓存――

Vous avez sauvegardé les poids du modèle vers la région S3. Une panne régionale survient; vous tentez de faire une panne; la réplique refuse de démarrer. Vous avez oublié que tokenizer.json, la configuration de quantification et la configuration de mise à l'échelle RoPE étaient dans un seau séparé que vous n'avez pas synchronisé.

> 另一方面, votre équipe a un plan de récupération de catastrophe. Vous allez mettre le modèle en charge à travers la région de sauvegarde jusqu'à S3.

Le service de LLM multi-régions est un problème de cache, un problème de routage et un problème d'hygiène DR  pas un problème d'équilibre de charge.

> Le service de la gestion des risques et des risques est un problème de réparation des risques et des risques.

## Le concept de base.

### Routage en connaissance de cache

> **【中文解读】**Le système de gestion de la mise en cache est un système de gestion de données qui permet de contrôler les données de la mise en cache.

La requête arrive avec un prompt. Le routeur hashes le préfixe (disons, les 512 premiers jetons); il demande à chaque réplique " avez-vous ce préfixe mis en cache ? " Les répliques publient des événements de cache KV sur un pub / sous-canal alors qu'elles allouent et évacuent des blocs. Le routeur choisit la réplique avec le match, passe à un coupe-coupe basé sur GPU util si personne ne le fait.

> S'il vous plaît, prenez des suggestions pour arriver. Le routeur pour le précédent (comme précédent 512 jetons) fait un hash; il demande à chaque copie " Avez-vous ce précédent cache ? "

**vLLM Router**(Rust, 2026 production-stack): souscrit à `kv.cache.block_added`événements, maintient un index de réplication de préfixe hash →, routes avec O(1) recherche. passe à la plus faible profondeur de file d'attente quand aucune correspondance.

> **vLLM Router**(Rust,2026 production-stack): 订阅 `kv.cache.block_added`事件,维护前哈希 → 副本索引,O(1) 查找路由──无匹配时回归最小队列深度──

**llm-d router**: le même schéma, Kubernetes natif. Publie des événements via l'API ControlPlane.

> **llm-d router**Il est également utilisé dans les applications de navigation.

**SGLang RadixAttention**(Phase 17 · 06) est l'équivalent intra-replica.

> **SGLang RadixAttention**(Phase 17 · 06) est l'équivalent de la valeur de l'article.

### Numéros

> **【拓展：KV Cache 路由的性能数据】**Différence de performances du KV de plusieurs régions: 2K-token 提示在 Llama 3.3 70B FP8 H100 上,cache hit(同副本、前常驻) TTFT ~80ms;cache miss(cold prefill) TTFT ~800ms10x 差距。 si le routeur de deux versions atteint un taux de pré-calébration moyen de 60 à 80% de la capacité de l'unité de deux versions, il peut être approximatif en N 副本容量下单副本性能──区域间 RTT est également un facteur clé: us-east-1  us-west-2 ~65ms、 us-east-1  eu-west-1 ~75ms、 us-east-1   southeast-1 ~220ms 跨-régional route 价值 只有在远程网上延迟才有时代──

TTFT P50 sur une demande de jeton 2K, Llama 3.3 70B FP8, H100:
- Accès de cache (même réplique, préfixe résident): ~80 ms.
- Faute de cache (pré-remplissage à froid): ~ 800 ms.

Si votre routeur atteint 60 à 80% du cache de préfixe sur les réplices, vous approximerez la performance de la seule réplica à la capacité de N-réplique.

> 2K-token 提示在 Llama 3.3 70B FP8 H100 上的 TTFT P50:缓存命中(同副本,前常驻) environ 80ms;缓存未命中(冷预填充) environ 800ms──10倍差距──

### La zone transversale a une nouvelle contrainte  latence réseau

RTT interrégionale:
- US-Est-1  US-Ouest-2: ~65 ms.
- États-Unis-Est-1  Eu-Ouest-1: ~75 ms.
- États-Unis-est-1  ap-sud-est-1: ~ 220 ms.

Si le routage prend une demande d'us-est-1 vers un préfixe chaud en ap-sud-est-1, le pré-remplissage enregistré (800 → 80 ms) est éclipsé de 440 ms aller-retour.`prefill_time + network_latency`La réponse est souvent de continuer à router régionalement sauf sur des préfixes massifs de plusieurs MB où le préfilement domine.

> 区域间 RTT: us-est-1  us-west-2 约 65ms; us-est-1  eu-west-1 约 75ms; us-est-1  ap-sud-est-1 约 220ms。`prefill_time + network_latency`La réponse est généralement de maintenir la régionalisation du chemin, sauf si le préchargement est dominant sur un grand nombre de MB.

### Les "inférences transregionales" commerciales ne sont pas utiles ici.

L'inference transregionale AWS Bedrock enroute automatiquement les demandes vers d'autres régions pendant la pression de capacité. Elle optimise la disponibilité, pas le TTFT, et traite l'inference comme opaque.

> AWS Bedrock 跨区域推理在容量压力下自动将请求路由到其他区域――它优化可用性而不是 TTFT,将推理视为不透明――GKE Multi-Cluster Gateway 也是如此服务级故障转移,不感知 KV 缓存――

Vous avez toujours besoin d'un routeur de mise en cache de la couche de l'application même lorsque vous utilisez ces. Ils gèrent le cas " us-east-1 est en feu ".

> Même avec ces produits, vous avez encore besoin d'appliquer des caméras de traitement de la situation "US-East-1 Coming on Fire"

### L'hygiène DR  le problème des dossiers manquants de 32%

> **【中文解读】**DR 卫生的三文件最低清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置(vllm_config.yaml等);(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件)

> **【拓展：LLM 灾难恢复最佳实践】**La principale pratique de l'LLM DR de 2026 est la suivante: 1) la modélisation de produits de manière complète et non seulement un document de poids, mais aussi un tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板; 2) la réplique transregionale de S3 dans le modèle stockage, pour assurer que toutes les régions aient une copie complète; 3) l'automatisation de DR 测试 avec l'ingénierie du chaos; 4) la vérification régulière des échecs 流程; 4) le RTO 目标 entreprises de niveau LLM  services exigent généralement RTO < 30 minutes.

Statistique 2026 largement citée: 32% des échecs de la DR LLM se produisent parce que les équipes ont sauvegardé des poids mais ont oublié:

- `tokenizer.json`ou `tokenizer.model`
- Configuration de la quantification (`quantize_config.json`, échelles AWQ, points zéro GPTQ)
- Configurations spécifiques au modèle (mesure RoPE, masques d'attention, modèles de chat)
- Configuration du moteur (`vllm_config.yaml`, défauts de prélèvement d'échantillons, manifestes de l'adaptateur LoRA)

> Les statistiques de 2026 sont très répandues: 32% des LLM ont échoué parce que les équipes ont enregistré des réserves de poids mais ont oublié:

La fixation est un manifeste DR minimum de trois fichiers:

1. Tous les fichiers sous le modèle HF repo (poids + configurations + tokenizer).
2. Configuration de service spécifique au moteur.
3. Manifeste de déploiement (K8s YAML, fichier Docker, verrouillage de dépendance).

> 修复方案是三文件最低 DR 清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置;(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅

Le drill de JPMorgan US-East-1 a atteint 22 minutes de récupération en novembre 2024 seulement parce que le manuel de jeu a été répété.

> En outre: chaque trimestre de la course DR 演练──JPMorgan 2024  11 月 us-east-1 演练 atteint 22 minutes de récupération, c'est parce que le pré-projet a été suivi 排练──

### La résidence des données est orthogonale

Si votre routeur de cache-conscient envoie une demande parisienne à us-east-1 pour une correspondance de préfixe, vous avez violé le RGPD indépendamment du gain TTFT. Partagez les routeurs par limite de résidence avant d'optimiser le cache.

> Si votre routeur de détection de cache est envoyé à l'Est des États-Unis pour effectuer une correspondance préliminaire, quel que soit le bénéfice du TTFT, vous avez déjà violé le RGPD.

### Les chiffres que vous devriez vous rappeler

- L'écart entre le cache et le TTFT: ~ 10x (80 ms contre 800 ms sur 2K prompt).
- RTT interrégional États-Unis-UE: ~75 ms.
- Failure de DR: 32% manquent les configurations de jeton/quant.
- JPMorgan us-east-1 échec de l'offre Nov 2024: 22 minutes (30 minutes SLA).

## Utilisez-le avec le cadre de réalisation
```figure
cache-aware-router
```

## Utilisez-le

`code/main.py`Simulation de trois stratégies de routage (route-robin, cache-conscient régional, cache-conscient global) sur une charge de travail multi-régions.

> `code/main.py`Dans le cadre de la mise en œuvre de la stratégie de gestion des ressources humaines, le rapport de gestion des ressources humaines (TTFT P50/P99 et frais transrégionaux) est présenté en ligne.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-multi-region-router.md`- compte tenu des régions, des contraintes de résidence et de l'ALS, il conçoit un plan d'itinéraire.

> 本课产 出 `outputs/skill-multi-region-router.md` la région déterminée, la résidence et le SLA, le design route scheme

## Les exercices

1. On court .`code/main.py`À quelle longueur rapide le routage interrégional dépasse le routage local, compte tenu du RTT de 75 ms ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ Un RTT de 75 ms, dans quel sens le longueur des routes transversales est-il supérieur à celui des routes locales ?
2. Votre taux de cache de frappe diminue de 70% à 12%.
   Le taux de réussite de votre casse-tête est passé de 70% à 12%.
3. Conceptez un manifeste DR pour un modèle quantifié AWQ 70B servi dans vLLM avec 5 adaptateurs LoRA.
   Pour le vLLM, il y a 5 LORA 适配器 70B AWQ 量化模型设计 DR 清单──列出每个文件和配置──
4.    Le projet de loi de la Commission européenne sur les investissements dans les secteurs de la finance et de la technologie (CFP) a été adopté par le Conseil européen de la finance et de la technologie (CFP) en décembre 2014.
   Le système de gestion des ressources humaines est un système de gestion des ressources humaines.
5. Une demande d'origine parisienne correspond à un préfixe dans l'Est-Est.
   Une requête de source parisienne dans l'est des États-Unis1 匹配到前──你路由它吗?写出策略──

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Encore une lecture

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) réutilisation de la cache KV trans-régionale avec une durée de latence réseau.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) documentation de défaillance de disponibilité.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) source de routeur conscient du cache.
