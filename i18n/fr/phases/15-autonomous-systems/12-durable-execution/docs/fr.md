# Les agents de longue durée: exécution durable

> Les agents de production à long horizon ne sont pas utilisés `while True`. Chaque appel LLM devient une activité avec un point de contrôle, une nouvelle tentative et une répétition. L'intégration du SDK OpenAI Agents de Temporal est terminée en mars 2026. Claude Code Routines (Anthropic) exécute des invocations de code Claude programmées sans un processus local persistant. Les sessions font une pause sur l'entrée humaine, survivent aux déploiements et reprennent à partir du dernier point de contrôle sur la touche de Claude Code.`thread_id`. Derrière la nouvelle ergonomie se trouve un vieux modèle  orchestration des flux de travail  avec une nouvelle entrée: LLM appelle des activités non déterministes qui doivent être répétées déterministiquement lors de la récupération.

> **【中文解读】**Produit de l' agent`while True`Le programme de formation en technologie de l'information (LAM) est un programme de formation en technologie de l'information et de communication (LAM) qui a été créé en 2026 par le gouvernement de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État

> **【拓展：LLM 调用 = 活动的精确契合】**LLM 调用完美匹配活动特征:不确定性(温度 > 0) 昂贵(金钱和延迟) 、可能失败(速率限制、超时) 、有副作用(调用工具)  让每个 LLM 调用包装为活动即可获得指数退避重试、跨重启检查点和可重放调试追踪──这就是为什么 Temporal、LongGraph、Cloudflare Durable Objects、Claude Code Routines 全部收到相同 API 形态`thread_id`+ 后端存储 + 最近检查点恢复──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la situation actuelle de l'agent.
>  **【类比】**Exécution durable = "Agent de l'archive point"。 ordiner Agent = 玩游戏没存档(崩=重头);Durable = 每个 LLM 调用后自动存档(崩=读最近的档档)。关键技巧: mettre chaque LLM 调用包装为"活动",记录输入输出到日志,崩时重放日志而不是重新调用既省钱又避免副作用重复执行(如重复转账)。
> ️ **【易错点】**副作用工具(写数据库、调外部 API) 不存缺失键 → 恢复时重复执行可能导致业务错误(用户被扣两次款) ――修复: chaque effet secondaire调用必须带等键(如`idempotency-key: uuid`), puis le lien vers le haut.

## Le problème , l' introduction du problème

> **【中文解读】**持久执行确保代理 任务在故障后能恢复――传统代理在内存中运行,进程崩意味着从头开始――持久执行将状态保存到外部存储 (database、文件系统),任何时刻都可以从最近检查点恢复――Temporal和LangGraph sont les deux principaux cadres d'exécution de réalisation de la durée――

> **【拓展：durable execution】**持久执行对长时间运行的代理 至关重要――如果一个需要运行 2 小时的代理 在第90 分钟崩,没有持久执行就意味着重新开始――Temporal 通过事件追溯源实现持久工作流,LangGraph 通过检查点实现持久状态图――2026年最佳实践是每一个重要步骤后自动保存检查点――

Considérez un agent qui fonctionne pendant quatre heures, appelle trois outils, demande à l'utilisateur deux fois et fait quarante appels LLM. À mi-parcours, l'hôte qu'il exécute se redémarre.

> 考虑一个运行四小时的代理――它调用三个工具――提示用户两次――进行40次的LLM调用――中途,运行的主机重启――

- Qu'est-ce qui se passe ?

> - Qu'est-ce qui se passe ?

- Dans un naïf .`while True`La mise en œuvre de la procédure de réinitialisation est effectuée à partir de zéro. les trois appels à l'outil (avec des effets secondaires réels) sont réactivés.
  Le mot grec traduit par " dans le simple "`while True`循环中: tout perdu. 运行从头重启.
- Avec une exécution durable: la course se poursuit depuis le point de contrôle le plus récent. Les activités déjà terminées ne sont pas réexécutées; leurs résultats sont reproduits à partir du journal durable. L'utilisateur n'approuve pas de nouveau les choses qu'il a déjà approuvées. Les appels LLM déjà effectués ne sont pas ré-facturés.
  Le résultat de l'activité n'est pas réétablie; le résultat de l'activité n'est pas réétablie.

C'est le même schéma que les moteurs de flux de travail ont mis en place depuis une décennie (Temporal, Cadence, Cherami d'Uber). Ce qui est nouveau, c'est que les appels LLM sont maintenant une sorte d'activité  non déterministe, coûteuse, avec des effets secondaires  et ils s'intègrent parfaitement à ce schéma.

> C'est le même modèle que le travail de la décennie. Il est nouveau que le MLL est maintenant un type d'activité.

> **【中文解读】**持久化执行解决长程 经纪人的可靠性问题:四小时运行中主机重启时,朴素循环丢失一切(工具重新执行、用户重新审批、LLM 重新计费),而持久化执行从最近检查点恢复,已完成的活动从持久日志重放而不是重执行── Temporal OpenAI Agents SDK 集成于 2026 年 3 月 GA──核心洞察:LLM调用是一种动作不确定性、昂贵、有副作用活动,完美适应工作流引擎的模式──

Le thème principal de la leçon est: la fiabilité à long horizon décline (le METR observe une " dégradation de 35 minutes "  le taux de réussite diminue à peu près quadratiquement avec l'horizon).

> Le thème de la formation est: "Réduction de la fiabilité à long terme" (METR)  Rate de réussite et de décalage de temps (Rate of Success and Time Line approximately square against ratio down) 

## Le concept de base.

### Activités, flux de travail, et de répétition 活动 工作流和重放

- **Workflow**Le code d'orchestration déterministe définit la séquence des activités, les branches, les attentes.
  Le mot grec traduit par " le mot grec "**工作流**Il faut une certaine détermination pour pouvoir refaire le journal des événements sans qu'il y ait de différences inattendues.
- **Activity**L'activité est enregistrée avec ses entrées et (une fois terminée) ses sorties.
  Le mot grec traduit par " le mot grec "**活动**: non-certainty、可能失败的工作单元──LLM 调用、工具调用、文件写、HTTP 请求── chaque activité enregistrera son entrée et sa finition (完成时)
- **Event log**Chaque activité démarre, complète, échoue, réessaye et chaque décision de workflow est enregistrée.
  Le mot grec traduit par " le mot grec "**事件日志**Chaque activité commence, se termine, échoue, est réessayée et chaque décision est enregistrée.
- **Replay**: lors de la récupération, le code du flux de travail est réexécuté dès le début; chaque activité déjà terminée renvoie son résultat enregistré sans réexécuter. Seules les activités qui n'avaient pas été terminées sont réellement exécutées.
  Le mot grec traduit par " le mot grec "**重放**: en récupérant, le code de travail est redéparté; chaque activité accomplie retourne à son enregistrement sans être réécrite.

C'est la même forme que React qui rend une DOM virtuelle ou Git qui reconstruit un arbre de travail à partir de commits.

> Ceci est similaire à React  contre la ré-routine DOM virtuelle ou Git de la forme du bâtiment de ré-routine du commissaire                                                                                                                                                                                                                                              

### Pourquoi les appels de LLM correspondent au modèle ?

Les appels à la LLM sont:

> Le programme de formation est:

- Non déterministe (température > 0; même la température 0 dérive entre les versions du modèle).
  La température > 0; même la température 0 跨模型版本漂移)
- On peut en dire autant de la durée de vie.
  Le mot "argent" est traduit par "argent".
- Les défaillances potentielles (limits de taux, délais).
  Le nombre de personnes qui ont été arrêtées est de 6,7%.
- Effets secondaires (si elles invoquent des outils).
  Il y a des effets secondaires.

En terminant chaque appel de LLM comme une activité, vous pouvez réessayer avec un backoff exponentiel, un point de contrôle à travers les redémarrages et une piste reproduisable pour débogage.

> C'est le dossier des activités. Chaque LLM va utiliser l'emballage pour l'activité pour vous donner un indice de réélimination des tentatives.

### Les points de contrôle identifiés par `thread_id`Je suis là.`thread_id`Pour le point de contrôle

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects et Claude Code Routines convergent toutes sur la même forme d'API: une `thread_id`(ou équivalent) identifie la session; chaque transition d'état persiste à un backend (postgreSQL par défaut, SQLite pour dev, Redis pour cache); résumé lit le dernier point de contrôle.

> LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects et Claude Code Routines ont reçu le même format d'API:`thread_id`(ou égal prix) identification de la langue; chaque état est transformé en postgreSQL, dédié à la langue de l'autre; récupéré Read Latest Checkpoint,

Le choix de l'arrière-plan est important:

> 后端选择重要:

- **PostgreSQL**: durable, consultable, survit aux déploiements.
  Le mot grec traduit par " le mot grec "**PostgreSQL**Le programme de recherche est en cours de réalisation.
- **SQLite**: local-dev seulement; perd des données sur les hôtes.
  Le mot grec traduit par " le mot grec "**SQLite**: seulement développé; transversale de l'organisation de la perte de données.
- **Redis**: rapide mais éphémère, sauf si l'AOF/snapshot est configuré.
  Le mot grec traduit par " le mot grec "**Redis**: rapidement mais temporairement, sauf si vous avez un projet de loi
- **Cloudflare Durable Objects**: distribué de manière transparente; scope par une clé unique; survit pendant des heures à des semaines.
  Le mot grec traduit par " le mot grec "**Cloudflare Durable Objects**: transparente distribuée; en unique key for range; survie nombre de heures à plusieurs semaines

### Les personnes qui entrent dans l'État sont des citoyens de première classe.

La proposition-et-commit (leçon 15) nécessite un état durable d'"attente humaine". Le flux de travail prend une pause, la file d'attente externe retient la demande en attente et l'approbation reprend à partir de ce point.

> Propose-then-commit ((第 15 课) nécessite de persévérer dans l'état d'attente de l'homme.

### La dégradation de 35 minutes est déclinée.

METR a observé que chaque classe d'agent mesurée montre une détérioration de la fiabilité au-delà de ~35 minutes d'exploitation continue.

> METR  Observer chaque mesure de l'agent  catégorie dans environ 35 minutes de fonctionnement continu après tout montre une baisse de la fiabilité 

La durée de la tâche est doublée, ce qui réduit de quatre fois le taux d'échec. L'exécution durable ne résout pas cela; elle vous permet de courir plus longtemps que le profil de fiabilité ne le permet.

> Le mode de sécurité est de combiner la durabilité avec le point de contrôle du nouveau HITL nécessaire à la réentrée, avec le point de contrôle du budget de l'ensemble du calcul de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de l'horloge de lhorloge de lhorloge de l'horloge de lhorloge de l'horloge de lhorloge de lhorloge de lhorloge de lhorloge de l'horloge de lhorloge de l'horloge de l'horloge de lhorloge de l'horloge de l'horloge.

### Quand l'exécution durable est la mauvaise réponse, l'exécution durable n'est pas la réponse.

- Les courses sont plus courtes que quelques minutes sans intervention humaine.
  Le récit de la première édition de la série est en français.
- Récupération des informations uniquement lues.
  Le texte est en français.
- Les tâches dans lesquelles la correction nécessite une fin-à-fin dans une fenêtre de contexte (certaines tâches de raisonnement; certaines générations à coup unique).
  Traduction anglaise: correctité doit être effectuée dans une fenêtre de l'intérieur à l'extérieur de la fenêtre.

## Utilisez-le avec le cadre de réalisation
```figure
memory-consolidation
```

## Utilisez-le

`code/main.py`implémentera un moteur d'exécution durable minimal dans stdlib Python. Il prend en charge:

> `code/main.py`Utilisation de Python 实现最小持久执行引擎──它支持:

- `@activity`décorateur qui enregistre les entrées et sorties dans un journal d'événements JSON.
  Le mot grec traduit par " le mot grec "`@activity`Le décorateur va entrer l'enregistrement en sortant jusqu'au JSON 事件日志。
- Une fonction de flux de travail qui séquence les activités.
  Le référencement est le résultat de la rédaction de la page d'accueil.
- Une .`run_or_replay(workflow, event_log)`fonction qui reproduit les activités accomplies sans les réexécuter.
  Le mot grec traduit par " le mot grec "`run_or_replay(workflow, event_log)`函数重放已完成活动而不重新执行──

Le pilote simule un flux de travail de trois activités, s'écrase à mi-chemin et montre (a) une nouvelle tentative naïve de tout réexécuter par rapport à (b) une répétition exécutant uniquement l'activité manquante.

> 驱动器模拟三活动工作流,中途崩,展示 (a) 朴素重试重新执行一切 vs (b) 重放只运行缺失活动──

## Envoyez-le . Produit .

`outputs/skill-durable-execution-review.md`examine le déploiement d'un agent de longue date proposé pour une forme d'exécution durable correcte: activités, déterminisme, arrière-plan des points de contrôle, état d'entrée humaine et politique de HITL sur résumé.

> `outputs/skill-durable-execution-review.md`审查提议长时运行 署的正确持久执行形状: activité、确定性、检查点后端、人类输入状态和恢复时HITL 策略──

## Les exercices

1. On court .`code/main.py`. Observer la différence entre le nombre d'activités et d'exécutions entre la répétition naïve et la répétition.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ observer les différences de mise en œuvre des activités et de la mise en œuvre des activités ◊ modifier les échecs et démontrer les changements de la mise en œuvre des activités ◊

2. Convertir le moteur de jouet à utiliser `thread_id`Simuler deux sessions simultanées partageant le moteur et confirmer que leurs journaux d'événements ne collisionnent pas.
   Le moteur de jeu est transformé en utilisation manifeste.`thread_id`◊ 模拟共享引擎的两个发发会话并确认其事件日志不冲突──

3. Prenez une activité dans le moteur de jouets. Introduisez un non-determinisme (un timestamp de l'horloge murale à l'intérieur d'une décision de flux de travail). Démontre la divergence lors de la répétition. Expliquez comment les moteurs réels gèrent cela (enregistrement des effets secondaires, `Workflow.now()`Les API).
   En français, le mot "débat" est traduit par "débat" ou "débat".`Workflow.now()`L'approvisionnement en ressources

4. Lisez le message LangChain "Runtime behind production deep agents" en lisant chaque état dans lequel le temps de fonctionnement persiste et en nommant le mode d'échec couvert par chacun.
   Le langchhain a été créé pour la production de produits de haute qualité.

5. Conceptez une politique de checkpoint pour une tâche de codage autonome de 6 heures. Où vous déplacez le checkpoint?
   Pour 6 heures de travail autonome, vous avez besoin de nouvelles ressources.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Encore une lecture

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) budget, tournées et réécriture de la sémantique.
  Le budget, la reprise et le rétablissement
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Forme de demande d'information événement.
  Le récit de la demande est le suivant:
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) exigences concrètes en matière de temps de fonctionnement.
  Le mot "concrètement" est traduit par "concrètement".
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) forme d'activité pour les cours de maîtrise de droit.
  Le mot " activité " est utilisé dans le langage de la langue de langue étrangère.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) la référence de dégradation de 35 minutes.
  Je suis en train de faire une petite histoire.
