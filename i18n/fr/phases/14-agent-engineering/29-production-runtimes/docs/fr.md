# Temps d'exécution de la production: file d'attente, événement, chronologie

> Les agents de production fonctionnent sur six formes de temps d'exécution: requête-réponse, streaming, exécution durable, arrière-plan basé sur la file d'attente, événement-orienté et planifié. Choisissez la forme avant de choisir le cadre.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**學本節前 請先掌握:Phase 14·13(LangGraph) 状态图基础;Phase 17 ((Infrastructure & Production) 本节是其前置概念,深入生产部署看Phase 17 全部。

## Objectifs d'apprentissage

- Nombre des six formes de production et correspondent chacune à un modèle de cadre / produit.
- Expliquez pourquoi l'exécution durable (LangGraph) est importante pour les tâches à long terme.
- Décrivez le temps de fonctionnement de l'événement et le moment où Claude Managed Agents convient.
- Expliquer la déclaration de capacité d'observabilité à charge pour les agents à plusieurs étapes.

## Le problème , l' introduction du problème

Les agents de production échouent de manière à ce qu'un ordinateur portable Jupyter ne soit pas sur la surface: les délais de réseau à l'étape 37, l'utilisateur suspend une appel vocale au milieu, le travail cron meurt lors du redémarrage de la machine, le travailleur d'arrière-plan se débarrasse de la mémoire.

> Le mode de défaillance de l'agent de production est Jupyter  notebook impossible à démontrer: 37 étapes de réseau supertemps, l'utilisateur est suspendu au milieu de la conversation, la tâche fixe est déclenchée lorsque l'appareil redémarre, la mort, la pénurie de stockage de l'appareil.


> **【中文解读】**Environnement de production L'agent doit traiter le problème de développement de l'environnement non nécessaire lors de sa fonctionnement: état de pérennité, capacité d'erreur de récupération, étendue de niveau, limitation de vitesse, contrôle des coûts et observabilité.

>  **【类比】**6 种运行时 = 6 种交通工具:**request-response**= le plus simple;**streaming**=高铁(边走边看风景,token 流式);(3) **durable execution**=房车(sleeping awake to continue, point de contrôle LangGraph);(4) **queue-based**- Je suis en train de faire une petite histoire.**event-driven**= Plateforme de vente extérieure (accès à l'information, claude agents gérés);**scheduled**=钟(定时执行,cron) ―― tâche à accomplir

> ️ **【易错点】**3 cratères de la course:**长任务用 request-response**3 小时任务挂 HTTP Plégions,nginx 60s 超时切断; avec exécution durable(LangGraph) + 后台轮询──(2) **observability 当可选**上线后发现"不知道为失败"; depuis le premier jour de contact avec Langfuse/LangSmith, chaque outil a été utilisé pour suivre──(3) **没做 graceful shutdown** service reboot lors de l'exécution de la tâche directement mort; utilisez SIGTERM 子 pour enregistrer le point de contrôle, reboot après le point de contrôle 续跑。

> **{【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】}**2026 ans de production Agent 运行时的选择:(1) LangGraph CloudLangGraph's托管服务,内置状态检查点和重放;(2) Temporal通用工作流引擎,配合AI SDK可构建持久化 Agent;(3) Autogestion基于Redis/Kafka的消息队列 +自定义 Agent 循环──关键决策因素是是否需要持久化执行如果 Agent可能运行数小时甚至数天,Temporal或LangGraph是更安全的选择──
## Le concept de base.

### Réponse à la demande

- HTTP synchrone, l'utilisateur attend la finition.
- Uniquement viable pour des tâches courtes (< 30 ans).
- Les piles: Agno (Python + FastAPI), Mastra (TypeScript + Express/Hono/Fastify/Koa).
- Observabilité: journaux d'accès HTTP standard + spans OTel.

### Retour en continu

- SSE ou WebSocket pour la sortie progressive.
- LiveKit étend cela à WebRTC pour la voix/vidéo (leçon 22).
- Stacks: tout cadre avec support de streaming + une frontend qui gère SSE/WS.
- Observabilité: le timing par pièce, la latence du premier jeton, la latence de la queue.

### Exécution durable

- Le poste de contrôle de l'État après chaque étape, les CV automatiques en cas d'échec.
- Le modèle d'acteur AutoGen v0.4 isole les défaillances à un agent (leçon 14).
- Le différentiateur de base de LangGraph (leçon 13).
- Essentiel lorsque le nombre d'étapes est inconnu et que le coût de récupération est élevé.

### Basé sur la file d'attente / arrière-plan

- Le travail entre en file d'attente, les travailleurs se rassemblent, les résultats reviennent via des webhooks ou des pubs/subs.
- Essentiel pour les agents à long horizon (de dizaines à des centaines d'étapes par tâche, par annonce d'utilisation informatique d'Anthropic).
- Les piles: Céléri (Python), BullMQ (Node), SQS + Lambda (AWS), sur mesure.
- Observabilité: profondeur de file d'attente, répartition de la latence par emploi, taille du DLQ.

### Événements

- Les agents s'abonnent aux déclencheurs: nouveau courriel, relations publiques ouvertes, feu de cron.
- Claude Managed Agents couvre cela à l'extérieur de la boîte (leçon 17).
- Les flux d'IAC (leçon 15) structurent les flux de travail déterministes basés sur les événements.
- Observabilité: source de déclenchement, latence de l'événement au démarrage, latence de l'agent.

### Les programmes

- Des agents en forme de Cron qui fonctionnent périodiquement.
- Combinez avec une exécution durable pour que la course nocturne échoue à la prochaine fois.
- Stacks: Kubernetes CronJob + un cadre durable; hébergé (Render cron, Vercel cron).

### Modèles de déploiement 2026

- **CrewAI Flows**pour la production axée sur les événements.
- **Agno**FastAPI sans état pour les microservices Python.
- **Mastra**adaptateurs de serveur (Express, Hono, Fastify, Koa) pour intégration.
- **Pipecat Cloud / LiveKit Cloud**pour la voix gérée (leçon 22).
- **Claude Managed Agents**pour l'asynchronisation à long terme hébergée.

### La visibilité est porteur de charge

Sans OpenTelemetry GenAI (leçon 23) plus un Langfuse/Phoenix/Opik backend (leçon 24), vous ne pouvez pas débogager un agent multi-étape qui a échoué à l'étape 40. Ce n'est pas facultatif pour la production. C'est la différence entre "nous débogageons rapidement" et "nous reproduisons à partir de zéro avec plus de logging".

> 没有 OpenTelemetry GenAI span(第 23 课)加上 Langfuse/Phoenix/Opik 后端(第 24 课),you cannot调试在第 40 步失败的多步代理―― ceci n'est pas optionnel pour l'environnement de production―― c'est la différence entre "réchauffement rapide" et "réchauffement et ajoutation de plus de journaux"".

> Le déploiement, la diffusion et la fiabilité de l'agent sont principalement pris en compte par: gestion de l'état, erreur de récupération, limitation des flux, gestion des lignes et contrôle des coûts.

### Lorsque les temps de production ne sont pas satisfaisants

- **Wrong shape choice.**Choisir une requête-réponse pour une tâche de 5 minutes.
- **No DLQ.**Les travailleurs font la queue sans lettre morte.
- **Opaque background work.**Les défaillances sont invisibles jusqu'à ce que l'utilisateur les rapporte.
- **Skipping durable state.**Toute course > 30 secondes où vous ne pouvez pas vous permettre de redémarrer nécessite une exécution durable.

> **错误的形态选择。**Pour 5 minutes tâche de sélection de requête-réponse.
> **没有 DLQ。**La tâche est perdue.
> **不透明的后台工作。**后台 Agent 运行没有追踪导出――失败不可见直到用户报告――
> **跳过持久化状态。**Toute opération de plus de 30 secondes et incapable de se redémarrer nécessite une exécution permanente.

## Construisez-le et mettez-le en œuvre.
```figure
wb-runtime-shapes
```

## Faites-le

`code/main.py`est une démo multi-forme stdlib:

- Point final de demande-réponse (fonction simple).
- Gestionnaire de diffusion (générateur).
- Travailleur en file d'attente avec DLQ.
- Registre de déclenchement d'événement.
- Un planificateur en forme de Cron.

- Je vais le faire.

```bash
python3 code/main.py
```

Exécution: cinq traces montrant le comportement de chaque forme sur la même tâche. La même logique d'agent, différentes coquilles extérieures. L'exécution durable (la sixième forme) est intentionnellement couverte dans la leçon 13 avec la vérification LangGraph.

> 输出: 5 traces montrent chaque forme de comportement sur la même tâche.

> Le déploiement, la diffusion et la fiabilité de l'agent sont principalement pris en compte par: gestion de l'état, erreur de récupération, limitation des flux, gestion des lignes et contrôle des coûts.

## Utilisez-le avec le cadre de réalisation

- **Request-response**pour une expérience utilisateur de chat.
- **Streaming**pour les réponses progressives.
- **Durable**pour des tâches à long terme.
- **Queue**pour les lots / asynchronyme / longue durée.
- **Event**pour la réactivité de l'agent.
- **Cron**pour le ménage (consolidation de la mémoire, évaluations, rapports de coûts).

## Envoyez-le . Produit .

`outputs/skill-runtime-shape.md`choisit une forme de temps de fonctionnement pour une tâche et fixe les exigences d'observabilité.

> `outputs/skill-runtime-shape.md`Pour choisir une fonctionnement en mode et connexion observable exigences.

> Le déploiement, la diffusion et la fiabilité de l'agent sont principalement pris en compte par: gestion de l'état, erreur de récupération, limitation des flux, gestion des lignes et contrôle des coûts.

## Les exercices

1. Portes ta leçon 01 ReAct boucle à toutes les six formes de ta pile. Quelle forme correspond à quelle surface du produit?
  Le mot "exercer" est traduit par "exercer".
2. Ajouter un DLQ à la démo basée sur la file d'attente. Simuler 10% d'échec de travail; surface taille DLQ.
  Le mot "exercer" est traduit par "exercer".
3. Écrivez un agent d'évaluation à l'aide de cron qui fonctionne chaque nuit contre vos 20 principales traces de la journée.
  Le mot "exercer" est traduit par "exercer".
4. Implémenter le streaming avec la pression de contre: si le client est lent, pause l'agent. Comment cela interagit-il avec un budget de tour?
  Le mot "exercer" est traduit par "exercer".
5. Quand vous déménagerez-vous avec un agent à long horizon ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Request-response | "Synchronous" | User waits; short tasks only |  |
| Streaming | "SSE / WS" | Progressive output; better UX; latency observable per chunk |  |
| Durable execution | "Resume from failure" | Checkpointed state; restart at last step |  |
| Queue-based | "Background jobs" | Producer / worker pool / DLQ |  |
| Event-driven | "Trigger-based" | Agent reacts to external events |  |
| DLQ | "Dead-letter queue" | Parking lot for failed jobs |  |
| Claude Managed Agents | "Hosted harness" | Anthropic-hosted long-running async with caching + compaction |  |

## Encore une lecture

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Détails d'exécution durables
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Asynchronisation à long terme hébergée
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) "Des dizaines à des centaines de pas par tâche"
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Isolement des défauts du modèle acteur
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
