# Chaos Engineering pour le LLM Production

> L'ingénierie du chaos pour les LLM est sa propre discipline en 2026. Pré-requis avant la réalisation d'expériences en production: SLI/SLO définie, trace+metric+log observabilité, retour automatique, runbooks, en appel. L'architecture a quatre plans: contrôle (programateur d'expérience), cible (services, infra, stockage de données), sécurité (gardiens + interruption + filtres de trafic), observabilité (métres + traces + journaux), rétroaction (dans les ajustements SLO). Les barreaux de protection sont obligatoires: les alertes de taux de brûlure arrêtent les expériences si la brûlure quotidienne d'erreur-budget est prévue > 2 fois; fenêtres de suppression + correlation de trace-ID déduction de bruit d'alerte. Cadence: révision hebdomadaire des petits canaris + SLO; jour de jeu mensuel + post mortem; audit trimestriel de la résilience entre équipes + cartographie de la dépendance. Experiments spécifiques à la LLM: surcharge de mémoire, défaillances réseau, coupures de fournisseurs, messages malformés, tempêtes d'évacuation de cache KV. Les outils: Harness Chaos Engineering (récommandations dérivées du LLM, réduction du rayon d'explosion, intégration des outils MCP); LitmusChaos (CNCF); Chaos Mesh (CNCF Kubernetes-native).

> **【中文解读】**Ce chapitre présente la pratique du service de l'enseignement supérieur en matière de gestion de conflits.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

>  **【前置】**Il est également possible de faire une analyse de la situation de l'économie de marché et de la situation économique.
>  **【类比】**LLM 混沌工程 = " exercice de feu "。 pré-médice:SLI/SLO 定义好、可观测、自动回滚、runbook、on-call。四平面:控制(实验调度) + objectif(服务/数据/基础设施) + sécurité(守卫/中止/流量过) +可观测。必须护: error budget burn rate > 2x 时暂停实验──节奏:每周小卡纳里度+月度游戏日+季度跨团队审计──LLM 专属实验:内存过载、网络故障、供应商 机、坏快点、KV cache 驱逐风暴──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Nombre des cinq prérequis de l'ingénierie du chaos (SLI/SLO, observabilité, réouverture, runbooks, on-call) et explique pourquoi sauter n'importe quelle pratique est une violation de la pratique.
  Le récit de la première partie de la série est un récit de la première partie de la série.
- Décrire les quatre plans (contrôle, cible, sécurité, observabilité) et la boucle de rétroaction dans le SLO.
  Le tableau de bord de l'appareil SLO est composé de quatre plans (contrôle, objectif, sécurité, observabilité) et de quatre rouleaux.
- Enumérez cinq expériences spécifiques à la LLM (surchargement de mémoire, défaillance du réseau, panne du fournisseur, prompt malformé, tempête d'évacuation de KV).
  Le programme de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
- Choisissez un outil  Harness, LitmusChaos, Chaos Mesh  donné pile.
  Le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos,

## Le problème , l' introduction du problème

> **【中文解读】**LLM 混沌工程是2026年的独立学科──LLM 增加了新的故障模式:4K-token's toxication characteristics使分词器卡住12秒;上游提供商 429 触发网关重试,重试放大并发导致OOM;突发负载下 KV Cache 淘汰风暴引发重填级联,耗尽计算资源──这些都不会出现在单元测试中混沌工程工具用户才发现它们──

> **【拓展：LLM 混沌工程的五类实验】**2026 LLM 特定五类混沌实验:(1) 内存过载发送长上下文高并发请求引发 KV Cache 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断断推理网关与供应商的连接,观察故障是否在 SLA内生效;(3) 供应商中断模拟100% OpenAI 429,观察路由是否失败到人类;(4) 形提示注入器具死负载吗(分层嵌套 Unicode、 UTF-8码点),观察单个请求锁住员工淘汰;5) KV 淘汰巨大暴风和vLLM 块预算强制淘汰, L(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

Les stacks LLM ajoutent de nouveaux modes d'échec. Un prompt de jeton 4K avec un caractère toxique arrête le jeton pendant 12 secondes. Un fournisseur en amont 429s; vos entrées de retrait; vos OOMs de service sur la simultanée amplifiée à la répétition. Une tempête d'évacuation de cache KV sous charge de débordement provoque des cascades de remplissage qui saturent le calcul.

Aucun de ces tests n'apparaît dans les tests unitaires.

## Le concept de base.

### Préalabilités

> **【中文解读】**Le référencement de l'équipe de travail est un processus de réflexion qui se déroule dans le cadre de la production. Il s'agit d'un processus de réflexion qui se déroule dans le cadre de la production.

Ne provoquez pas de chaos dans la production sans:

1. **SLI/SLO** définir des indicateurs et des objectifs de niveau de service.
2. **Observability** Traces, métriques, journaux, câblées à des tableaux de bord.
3. **Automated rollback** Phase 17 · 20 - Réouverture du programme de politique de réforme.
4. **Runbooks** structurée, phase 17 · 23.
5. **On-call** quelqu'un pour répondre.

Le manque de tout moyen, le chaos devient un véritable incident.

### Quatre avions + rétroaction

**Control plane** programmeur d'expériences (flux de travail Litmus, programme Chaos Mesh, interface utilisateur Harness).

**Target plane** services, capsules, nœuds, équilibrateurs de charge, stockage de données.

**Safety plane** commutateur de compression, fenêtres de suppression, limites de rayon d'explosion, portes de budget d'erreur.

**Observability plane** des mesures normales + corrélation trace-ID pour distinguer les défaillances induites par le chaos des défaillances naturelles.

**Feedback loop** Les résultats se rapportent à l'ajustement du SLO, aux mises à jour des coordonnées, aux corrections de code.

### Les barreaux sont obligatoires

> **【拓展：混沌工程的安全护栏】**Les trois mesures de sécurité nécessaires de l'ingénierie du chaos: 1) le taux de combustion maximum pour les alarmes pendant les expériences si le dépense de budget d'erreur quotidienne dépasse les 2 fois de ce qui était prévu, interrompre automatiquement les expériences; 2) le silence dans le milieu explosif de l'expérience, éviter le bruit sur l'appel; 3) le trace-ID connecte toutes les expériences causées par l'erreur et porte des étiquettes, de sorte que l'appel peut être rechargé.

- **Burn-rate alert**: l'expérience de pause si le budget d'erreur quotidien dépasse le double prévu.
- **Suppression windows**: silence des alertes non expérimentales dans le rayon d'explosion pendant l'expérience.
- **Trace-ID correlation**: toutes les erreurs induites par l'expérience sont marquées de manière à pouvoir être déduites sur appel.

### Cinq expériences spécifiques à la LLM

1. **Memory overload** forcer une tempête de préemption de cache KV en envoyant des requêtes de long contexte avec une grande simultanéité.

2. **Network failure** coupure de connectivité entre la passerelle d'inférence et le fournisseur.

3. **Provider outage simulation** 100% 429 de OpenAI. Observez: le routage fait-il une défaillance vers Anthropic? (phase 17 · 16, 19)

4. **Malformed prompt** injecter une charge utile pour l'installation de jetons (par exemple, unicode profondément niché, un codepoint UTF-8 énorme).

5. **KV eviction storm** expulsion forcée par saturation du budget de bloc VLLM. Observez: le LMCache se rétablit-il ou le service se dégrade-t-il?

### Cadence

- **Weekly** petites expériences canaries en mise en scène, peut-être 5% de prod.
- **Monthly** jour de jeu prévu dans un scénario spécifique; présence entre équipes; post mortem.
- **Quarterly** Audit de la résilience entre équipes; mise à jour de la carte de la dépendance.

### Les outils

> **【拓展：混沌工程工具选择】**Le projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet

- **Harness Chaos Engineering** commercial; recommandations d'expériences dérivées de l'IA; réduction de l'échelle du rayon d'explosion; intégration des outils MCP.
- **LitmusChaos** Gradué du CNCF; basé sur le flux de travail Kubernetes.
- **Chaos Mesh** Sandbox CNCF; style CRD natif des Kubernètes.
- **Gremlin** commercial; large soutien.
- **AWS FIS**- Je suis là .**Azure Chaos Studio** Offres gérées dans le cloud.

### Commencez petit

Première expérience: décodez une copie sous un trafic constant, observez le redirigement et la récupération, si cela fonctionne et semble sûr, passez au chaos du réseau.

Première expérience spécifique à la LLM: injecter un fournisseur 429 pendant 5 minutes. Observez le retrait. La plupart des équipes découvrent que leur retrait n'a pas été entièrement testé.

### Les chiffres que vous devriez vous rappeler

- Quatre avions: contrôle, cible, sécurité, observabilité.
- Pause de taux de brûlure: 2 fois le budget quotidien prévu.
- Cadence: canary hebdomadaire, jour de jeu mensuel, audit trimestriel.
- Cinq expériences de LLM: mémoire, réseau, fournisseur, prompt malformé, KV tempête.

## Utilisez-le avec le cadre de réalisation
```figure
i4-chaos-guard
```

## Utilisez-le

`code/main.py`Il simule trois expériences de chaos avec des portes de sécurité, qui pourraient faire trébucher le taux de brûlure.

> `code/main.py`Il simule trois expériences de chaos avec des portes de sécurité, qui pourraient faire trébucher le taux de brûlure.

> `code/main.py`Il simule trois expériences de chaos avec des portes de sécurité, qui pourraient faire trébucher le taux de brûlure.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-chaos-plan.md`- Compte tenu de sa taille et de sa maturité, il choisit les trois premières expériences et l'outillage.

> 本课产 出 `outputs/skill-chaos-plan.md`- Compte tenu de sa taille et de sa maturité, il choisit les trois premières expériences et l'outillage.

## Les exercices

1. On court .`code/main.py`Quelle expérience défonce la porte de la vitesse de combustion et pourquoi ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Quelle expérience a provoqué le contrôle du taux de combustion ?
2. Conceptez les cinq premières expériences de chaos pour un service RAG basé sur vLLM. Incluez des critères de réussite.
   Pour la première fois, il y a eu des expériences de chaos.
3. Votre alerte a interrompu une expérience.
   Le taux de combustion de votre voiture a été suspendu. Comment déterminer le comportement de la source par rapport à l'attendu ?
4. Discutez si le chaos doit se produire dans la production ou seulement en scène.
   Le thèse Chaos Experiment devrait être en production ou seulement en pré-édition environnement de fonctionnement.
5. Nombre de trois modes de défaillance spécifiques à la MLL que le chaos du réseau générique ne peut reproduire.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Encore une lecture

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
