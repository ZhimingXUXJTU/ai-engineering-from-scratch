# SRE pour l'IA  Réaction à l'incident multi-agents, manuels de conduite, détection prédictive 

> L'AI SRE utilise des LLM basés sur des données d'infrastructure (logs, runbooks, topologie de services) via RAG pour automatiser les phases d'enquête, de documentation et de coordination. Le modèle d'architecture de 2026 est l'orchestration multi-agents  agents spécialisés (logs, métriques, livres de conduite) coordonnés par un superviseur; l'IA propose des hypothèses et des requêtes, les humains approuvent les appels de jugement. Datadog Bits AI et Azure SRE Agent expédient cela comme des produits gérés. Les runbooks évoluent: NeuBird Hawkeye utilise l'évaluation adversitaire (deux modèles analysent le même incident; accord = confiance, désaccord = incertitude); la mémoire opérationnelle persiste en fonction des changements d'équipe. L'automédication reste prudente: l'IA suggère, les humains approuvent. L'action entièrement autonome est étroite (capsule de redémarrage, déploiement spécifique de rampe) avec des barreaux serrés  toute personne vendant "set it and forget it" est survendue. Frontière émergente: prédiction d'incidents. Une recherche du MIT rapporte qu'un LLM formé sur les journaux historiques + les temps de GPU + les schémas d'erreur API a prédit 89% des pannes de service 10 à 15 minutes plus tôt. Projection: 95% des LLM d'entreprises auront un décalage automatisé d'ici fin 2026.

> **【中文解读】**Ce chapitre présente les méthodes d'ingénierie de la station de fiabilité de l'IA dans la pratique de l'IA.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy multi-agent incident triage simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)

>  **【前置】**Les résultats de la recherche ont été obtenus en 1er janvier 2015 et ont été publiés en 1er janvier 2015.
>  **【类比】**AI SRE = "AI 急诊医生"。多 Agent 编排:日志 Agent+指标 Agent+runbook Agent 协调;AI 提假设+查日志,人类批准判断。Datadog Bits AI、Azure SRE Agent 是托管产品。NeuBird Hawkeye 用对抗评估(两模型同分析事件,一致=高置信)。自动修复保持谨慎:AI 建议+人批准。前沿:预故障预测(MIT 用历史日志+GPU 温度+API 错误提模式预测 89% 故障 10-15 分钟)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Diagramme de l'architecture multi-agent AI SRE: superviseur + agents spécialisés (logs, métriques, runbooks) + passerelle d'approbation humaine.
  Le nom de l'agent de l'entreprise est le nom de l'agent de l'entreprise.
- Expliquez pourquoi la remise en état automatique est étroite (capsule de redémarrage, déploiement réversible) plutôt que large (service de réarchitecture).
  Expliquer pourquoi l'automatisation est de petite portée (à la place de grande portée)
- Nommez le modèle d'évaluation de l'adversité (NeuBird Hawkeye): deux modèles sont d'accord = confiance; désaccord = escalade.
  Le modèle de l'observation de l'homme est le modèle de l'observation de l'homme.
- Citons le résultat de détection précoce du MIT de 89% et la contrainte opérationnelle: les prédictions sans action sont juste des tableaux de bord.
  Le projet de loi de l'État de l'Afrique du Sud est en cours de mise en œuvre.

## Le problème , l' introduction du problème

> **【中文解读】**L'intelligence artificielle (AI SRE) a été créée en 1926 et a été mise en service par le groupe de travail de l'AI SRE.

> **【拓展：AI SRE 产品市场】**Les résultats de l'étude de l'étude de l'Agence de surveillance des données (ACE) ont été obtenus en 2026 par l'Agence de surveillance des données (ACE) et l'Agence de surveillance des données (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (ACE) (A) (ACE) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A) (A)

Un ingénieur en appel est appelé à 3 heures du matin "Total taux d'erreur dans la caisse". Ils vérifient Datadog, Loki, trois livrets d'exécution, le journal de déploiement. 30 minutes plus tard, ils réalisent que la cause principale est un OOM vLLM d'un KV cache spike. Ils redémarrent la capsule; l'erreur est nettoyée.

En 2026, les 20 premières minutes de cette enquête sont automatisées. Le regroupement des journaux par service, en corrélation avec les déploiements récents, en correspondance avec les runbooks  sont tous RAG + utilisation des outils. Un agent supervisé peut faire un triage de première passe et présenter une hypothèse avant que l'homme ouvre Datadog.

La réparation entièrement autonome est un problème différent. Retourner la capsule: sécurisé. Échanger la GPU pool: sécurisé si la politique le permet. Rédécorer le service: absolument pas. La discipline trace la ligne étroite.

## Le concept de base.

### Architecture multi-agent

> **【中文解读】**架构:Supervisor 将事件分分为查询,分派给专业化 Agent 日志 Agent 搜索日志、指标 Agent 查询 PromQL、Runbook Agent 检索文档) Supervisor 综合,向人类呈现假设 + 证据──人类批准或重定向──安全自动修复范围:重启 Pod、回滚特定部署、在预批准范围内扩展池──不安全范围:更改服务拓、更改资源限制、部署新代码、更改 IAM──

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

Le superviseur découple l'incident en sous-queries. Les agents spécialisés ont accès aux outils (recherche de journaux, PromQL, récupération de documents). Le superviseur synthétise, présente une hypothèse + des preuves à l'homme. L'homme approuve ou redirige.

### Département de traitement automatique

> **【拓展：AI SRE 自动修复的安全边界】**Les fournisseurs de sécurité de l'AI SRE auto-révision de bordures de sécurité répartissent: sécurité(région étroite)  redémarrage Pod、 rassemblement spécifique déploiement、 expansion de la pile en pré-ratification  activation de la fonction de pré-ratification flag。 non-sécurité(région étroite)  modification de la service   modification de la ressource limitation、 déploiement de nouveaux codes、 modification de la base de données。 tout fournisseur qui prétend être "déterminé après avoir oublié" s'engage à exagérer la sécurité  assemblage avec l'AI SRE mature et s'étend, mais les limites sont réelles  la meilleure pratique de l'année 2026 est:  recommandation  humanité  autorisation  ne permet que la mise en œuvre de la seule étendue étroite spécifique    comme le Pod 重启动) 

**Safe (narrow)**: redémarrer la capsule, revenir à la déploiement spécifique, faire évoluer le poids de l'échelle dans les limites pré-approuvées, activer le drapeau de fonctionnalité pré-approuvé.

**Not safe (broad)**: modifier la topologie des services, modifier les limites des ressources, déployer un nouveau code, modifier le système de gestion des données internes, modifier les bases de données.

Tout le monde qui vend "set it and forget it" est un surventeur.

### Évaluation adverse (NeuBird Hawkeye)

Deux modèles analysent indépendamment le même incident. Si ils sont d'accord sur la cause profonde, la confiance est élevée. Si ils ne sont pas d'accord, escalader à l'homme avec les deux hypothèses visibles.

### Mémoire opérationnelle

Le retour d'équipe est la destruction silencieuse des feuilles de connaissances tribales traditionnelles de SRE. AI SRE stocke des livres de conduite + des post-mortem dans un vecteur DB; les agents récupèrent sur chaque nouvel incident. Lorsque de nouveaux ingénieurs rejoignent, l'IA a une histoire complète.

### Prévision préalable à l'incident

MIT 2025 recherche: LLM formé sur les journaux historiques, les températures de GPU, les schémas d'erreur API prédit 89% des pannes 10 à 15 minutes avant qu'elles se produisent sur le set de test.

Vérifiez la réalité: les prédictions sans action sont des tableaux de bord. La question opérationnelle est "quand nous prédisposons, que faisons-nous?" drainage préventif? Pager? Auto-échelle? La réponse est spécifique à la politique.

### Produits en 2026

- **Datadog Bits AI** a géré le co-pilot de la SRE à l'intérieur de Datadog.
- **Azure SRE Agent**- Native de l'Azure.
- **NeuBird Hawkeye** évaluation adversitaire + mémoire opérationnelle.
- **PagerDuty AIOps** triage + déduplication.
- **Incident.io Autopilot** commandant d'incident + coordination.

### Les livres de conduite en tant que code

> **【拓展：AI SRE 实施路径】**1) d'abord mettre en œuvre un répertoire non structuré pour se transformer en un répertoire structuré de symptômes, de hypothèses, d'essais, d'actions; 2) réaliser une évaluation de la résistance à deux modèles indépendants analysant les mêmes événements; 3) établir une mémoire d'opération;

Les runbooks évoluent des pages Confluence à des versions de marquage avec des sections structurées (symptom, hypothèse, vérifier, agir).

### Les chiffres que vous devriez vous rappeler

- Détection précoce du MIT: 89% des pannes, 10 à 15 minutes de délai.
- Triation multi-agent: superviseur + (logs, métriques, manuels de conduite) + humain.
- Un ensemble de remède automatique sécurisé: redémarrer la capsule, réinstaller, étaler dans les limites.
- Évaluation adverse: deux modèles indépendants; accord = confiance.

## Utilisez-le avec le cadre de réalisation
```figure
i4-incident-agents
```

## Utilisez-le

`code/main.py`Simulation de triage multi-agent: l'agent de journal trouve une erreur, l'agent métrique trouve une pointe de CPU, l'agent de la carte de roulement correspond à un problème connu.

> `code/main.py`Simulation de triage multi-agent: l'agent de journal trouve une erreur, l'agent métrique trouve une pointe de CPU, l'agent de la carte de roulement correspond à un problème connu.

> `code/main.py`Simulation de triage multi-agent: l'agent de journal trouve une erreur, l'agent métrique trouve une pointe de CPU, l'agent de la carte de roulement correspond à un problème connu.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-ai-sre-plan.md`. Compte tenu du volume d'incidents, de la maturité de l'équipe, il conçoit un déploiement de l'IA SRE.

> 本课产 出 `outputs/skill-ai-sre-plan.md`. Compte tenu du volume d'incidents, de la maturité de l'équipe, il conçoit un déploiement de l'IA SRE.

## Les exercices

1. On court .`code/main.py`Et si les agents de log et de métrique ne sont pas d'accord ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Si le journal et l'indicateur ne sont pas d'accord, comment le directeur peut-il s'entendre ?
2. Définissez trois actions de réparation automatique "sûr" pour votre service.
   Pour chaque raison, il y a trois "sécurité" à utiliser.
3. Écrire un modèle de routeur structuré: sections, champs requis, commandes de vérification.
   Le texte de la loi est écrit en français.
4. Quelle est votre politique ?
   Le premier jour de la journée, le premier jour de la semaine, le premier jour de la semaine, le premier jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le deuxième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine, le troisième jour de la semaine de la semaine, le troisième jour de la semaine de la semaine, le troisième jour de la semaine de la semaine de la semaine, le troisième jour de la semaine de la semaine de la semaine de la semaine de la semaine, le deuxième jour de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine.
5. Débattez si une équipe de 3 personnes devrait adopter l'IA SRE en 2026 ou attendre.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## Encore une lecture

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
