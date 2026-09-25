# Parallèle / Charme / Architectures réseau

> Contrairement à la direction: aucun décideur central. Les agents lisent un bus d'événements partagés, reprennent le travail de manière asynchrone, rédigent les résultats. LangGraph prend explicitement en charge "Swarm Architecture" pour les environnements décentralisés et dynamiques. Matrix (arXiv:2511.21686) représente à la fois le contrôle et le flux de données en tant que messages sérialisés passés à travers des files d'attente distribuées pour éliminer le gouffre-bouteille de l'orchestre. Le compromis est explicite: déterminisme et traçabilité pour l'évolutivité. Swarm s'adapte aux tâches avec de nombreux sous-problèmes indépendants; il ne s'adapte pas aux tâches qui nécessitent un seul plan cohérent.

> **【中文解读】**Ce chapitre présente le modèle d'organisation du réseau de groupes de partage de l'agent par le biais d'un état de partage et de partage de travail.

> **【拓展：parallel swarm networks→具体应用】**Le réseau de groupes de travail permet de faire une grande quantité d'agents avec des tâches de traitement, puis de regrouper les résultats. Les résultats sont adaptés aux tâches de gestion de plusieurs documents.


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Les élèves doivent être informés de la situation de la population.
>  **【类比】**Swarm vs Supervisor = "decentralisation" vs "niveau-niveau"──Supervisor = 公司(CEO 调度);Swarm = 开源社区(每人看问题 板自己领取)──Swarm 适合独立子任务(多文件编辑、多源查询),不适合需要单一计划的任务──5-10 个代理是最优太多会聚聚时打架──

## ♪ Problème ♪ Introduction du problème ♪

Le superviseur est le seul à faire le choix, et chaque décision sur qui fait quoi passe par un seul agent.

> Le surveillant peut s'étendre à plusieurs machines de travail. Il devient lui-même un bouteilleur: chaque décision sur qui fait quoi passe par un agent.

Le superviseur est lui-même un appel de LLM. Chez des centaines de travailleurs, le superviseur fait des centaines d'appels de LLM juste pour envoyer. Chaque appel est de secondes; le débit de dépêche domine. Swarm retire le superviseur entièrement.

> Le surveillant lui-même est un MLL. Il n'y a que des centaines de machines à travailler où il ne peut effectuer que des centaines de MLL.

Les architectures de masse inversent la conception. Au lieu d'un planificateur central qui envoie le travail, les travailleurs choisissent le travail d'une file d'attente partagée. La "coordination" est intégrée à la sémantique du bus d'événement.

> L'architecture de groupe a été modifiée en conception. Il n'y a pas de planificateur central pour déployer des travaux, mais un outil pour obtenir des travaux de la cohorte commune.

L'inversion architecturale est significative: le goulot d'étranglement passe de "le LLM qui décide de ce qu'il faut faire" à "le courtier de messages qui fonctionne".

> L'équipe de formation de l'entreprise a été créée pour la première fois en 1999 et a été créée en 1999 par le groupe de travail de l'entreprise de formation professionnelle.

## Concept Le concept central

### La forme

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

Aucun orchestrateur. Chaque travailleur répète: tirer une tâche, procéder, écrire le résultat (et optionnellement faire des suivi).

> 没有编排器.每个工作器重复:拉取任务、处理、写入结果.

Le manque d'un décideur central est la caractéristique définitive. Les travailleurs n'attendent pas les instructions; ils s'organisent eux-mêmes autour de la file d'attente. C'est le modèle d'acteur appliqué aux LLM.

> 缺乏中央决策者是定义特征──工作器不等待指令; elles sont entourées de file d'attente elles-mêmes organisées──

### Quand l' essaim se passe

- **Many independent tasks.**Les tâches ne dépendent pas les unes des autres.
  Le mot grec traduit par " le mot grec "**许多独立任务。**Les tâches ne dépendent pas les unes des autres.
- **Variable-duration work.**Si certaines tâches prennent 100ms et d'autres 10s, un essaim équilibre automatiquement la charge  les travailleurs rapides tirent les prochains emplois.
  Le mot grec traduit par " le mot grec "**可变持续时间的工作。**Si certaines tâches nécessitent 100 ms et d'autres 10s, le groupe se charge automatiquement.
- **Throughput over determinism.**Vous vous souciez du temps de réalisation total, pas de la commande stricte.
  Le mot grec traduit par " le mot grec "**吞吐量优先于确定性。**Tu as une grande préoccupation pour le temps de la réalisation, pas pour le classement strict.

### Quand l' essaim échoue

- **Ordered workflows.**Si l'étape 3 a besoin de la sortie de l'étape 2, un essaim risque de tirer l'étape 3 avant l'étape 2.
  Le mot grec traduit par " le mot grec "**有序工作流。**Si l'étape 3 nécessite la sortie de l'étape 2, le groupe a l'étape 3 avant l'étape 2 de la réalisation.
- **Global-plan tasks.**Les questions de recherche complexes bénéficient d'un planificateur.
  Le mot grec traduit par " le mot grec "**全局计划任务。**Les problèmes de recherche complexes sont bénéfiques pour les planificateurs.
- **Debugging.**Sans journal central et sans travail asynchrone, reproduire un bug est coûteux.
  Le mot grec traduit par " le mot grec "**调试。**没有中央日志和异步工作, le prix du bug de rétablissement est très élevé.

### Les données de l'équipe de gestion des données doivent être fournies à l'utilisateur.

Matrix est le document de 2025 qui conduit l'éventail à sa conclusion naturelle: le flux de contrôle et le flux de données sont des messages sérialisés sur des files d'attente distribuées. Aucun coordinateur central. La tolérance aux erreurs provient de la durabilité du message. L'évolutivité est le problème du courtier de messages, pas du système.

> Matrix est un thème qui conduit les groupes à la conclusion naturelle de 2025: les flux de contrôle et les flux de données sont des informations séquencées sur des coordonnées distribuées. Il n'y a pas de coordonnateur central.

En faisant du courtier (Kafka, Redis Streams, NATS) le goulot d'étranglement d'échelle, Matrix contourne entièrement le goulot d'étranglement de la LLM en tant qu'orchestre.

> 通过使代理(Kafka、Redis Streams、NATS) devenir un boîtier d'expansion, Matrix 完全避开 LLM 作为编排器的瓶──如果代理可以,系统可以扩展到数千代理;LLM est un pur travail, jamais un coordonnateur──

Contribution: un modèle de programmation où la coordination multi-agents est " quel sujet de message cet agent s'abonne-t-il à ? " plutôt que " quel agent le superviseur choisit-il ensuite ? " Cela fait ressembler le système à un réseau pub/sub événement.

> 贡献: un modèle de programmation, plusieurs agents 协调 est " ce agent 订阅什么消息主题? " plutôt que " le surveillant suivant choisit quel agent ? " qui fait ressembler le système à un réseau de publication/abonnement.

### L'architecture de la masse de LangGraph
### Les graphes sont en masse

Les documents de LangGraph 2025 décrivent explicitement "Architecture de la nuée" comme l'un des modèles multi-agents: les agents sont des nœuds, mais les bords forment un graphique dirigé avec des cycles et tout nœud peut être activé à partir du bassin.

> LangGraph 2025 文档明确将"群体架构" être décrite comme étant plusieurs agents 模式之一:Agent est un point, mais le côté est formé d'un cercle avec un plan, tout point peut être activé dans le réservoir.

La contribution de LangGraph: le même modèle mental basé sur des graphiques soutient maintenant la dynamique des essaims. Les nœuds qui s'activent en fonction de conditions plutôt que de bords fixes. Cela fait le pont entre le graphique statique et les mondes de la masse pure.

> Contributions de LangGraph: le même modèle mental basé sur la graphie soutient maintenant les mouvements du groupe.

### Mode d'échec: famine et hotspotting

Si tous les travailleurs effectuent la tâche la plus rapide disponible, les tâches de longue durée ne sont jamais choisies tant qu'elles ne sont pas les seules à faire.

> Si tous les outils de travail sont les plus rapides, les tâches de longue durée ne seront jamais choisies jusqu'à ce qu'elles deviennent les seules à rester.

La famine est le mode de défaillance de l'envahisseur. Sans vieillissement explicite (la priorité augmente avec le temps d'attente) ou des travailleurs spécialisés à longues tâches, une tâche de 10 secondes attend pour toujours derrière un flux de tâches de 100 ms. Les essaims de production doivent concevoir autour de cela.

> 饥饿是群体的标志性失败模式――没有明显老化(优先级随着等待时间增加) 或专业化长任务工作器,10秒任务永远在100ms 任务流后等待――生产群体必须围绕这个工程设计――

Les atténuations:
- Les files d'attente prioritaires avec vieillissement explicite (augmenter la priorité avec le temps d'attente).
  Le temps d'attente augmente la priorité de la vieillissement.
- Spécialisation des travailleurs: certains travailleurs ne prennent que des tâches "longues".
  Traduction anglaise: certains travailleurs acceptent seulement des tâches "长"
- Pressure de retour: limiter le nombre de tâches rapides entrant dans la file d'attente.
  Le nombre de tâches à effectuer dans la ligne de travail est limité.

### Le lien de routage basé sur le contenu

Les paires de groupes sont naturellement en route basée sur le contenu (leçon 22). Au lieu d'une file d'attente générique, il y a une file d'attente par type de message.

> Le groupe et le chemin basé sur le contenu (leçon 22) Le partage naturel ne constitue pas une ligne générale, mais un type de ligne pour chaque type de message.

Le routage basé sur le contenu plus swarm vous donne le réseau pub/sub-événement: un substrat où tout agent peut publier n'importe quel type de message, et que les agents intéressés le reçoivent.

> 基于内容的路由加群体给你发布/订阅事件网格: un agent peut publier n'importe quel type de message et seulement l'agent qui est intéressé 接收它的底层── c'est la base de la Matrix、CA-MCP 和大多数 2026 productions multi agent 系统──

## Construisez-le et mettez-le en œuvre.
```figure
sw-work-stealing
```

## Faites-le

`code/main.py`met en œuvre un essaim de 4 fils de travailleurs tirant d' un partagé `queue.Queue`Les tâches ont une durée variable (certaines rapides, d'autres lentes).

> `code/main.py`4 projets de partage ont été réalisés.`queue.Queue`拉取工作线程──任务有可变持续时间((quelques rapides, quelques lent)──演示对比:

La comparaison à trois sens est la valeur éducative: les mêmes tâches, les mêmes travailleurs, seulement la stratégie de dépêche change. Sequentielle = lente. Fixée = gaspillante. Swarm = optimal. Les chiffres de l'horloge murale font empirieusement le cas.

> Les trois parties sont la valeur de l'éducation: la même tâche, le même appareil, seulement la modification de la stratégie.

- **Sequential baseline:**Un travailleur traite toutes les tâches en série.
  Le mot grec traduit par " le mot grec "**顺序基线：**Une machine à travailler pour traiter toutes les tâches.
- **Fixed assignment:**chaque tâche préalablement attribuée à un travailleur spécifique (type superviseur).
  Le mot grec traduit par " le mot grec "**固定分配：**Chaque tâche est préalablement attribuée à un appareil spécifique.
- **Swarm:**Les travailleurs sortent de la file d'attente.
  Le mot grec traduit par " le mot grec "**群体：**工作器 de la répartition des équipes

Les balances de masse se chargent automatiquement; les tâches fixes laissent les travailleurs rapides inactifs lorsque leur tâche est lente.

> 群体自动平衡负载; fixe répartition dans la tâche de répartition lent temps faire rapide

La distribution "inégale mais optimale" est la signature de la masse. Un travailleur qui termine sa tâche en 50 ms tire trois autres tandis qu'un travailleur sur une tâche de 2 secondes est toujours sur sa première.

> La répartition " non uniforme mais optimale " est caractéristique du groupe. 50 ms. Le travail effectué par le robot de 2 secondes est toujours en train de réaliser trois tâches supplémentaires lors de la première tâche.

Les résultats montrent le nombre de tâches par travailleur (les répartitions de masse sont inégales mais optimales) et les temps de l'horloge murale.

> 输出显示每个工作器的任务计数(群体分布不均但优优) 和挂钟时间──

## Utilisez-le avec le cadre de réalisation

`outputs/skill-swarm-fit.md`évaluera si une tâche doit utiliser swarm vs supervisor. Les entrées: indépendance de la tâche, variance de durée, exigences de commande, besoins de débogabilité.

> `outputs/skill-swarm-fit.md`评估任务应使用群体还是监督者──输入: tâche indépendance、持续时间差、排序要求、可调试性需求──

## Envoyez-le . Produit .

Liste de contrôle:

> 检查清单:

- **Priority queue with aging.**Éviter la famine à long terme.
  Le mot grec traduit par " le mot grec "**带老化的优先队列。**防止长任务 饥饿──
- **Worker idempotency.**Une tâche peut être effectuée plus d'une fois si un travailleur s'écrase au milieu de la course.
  Le mot grec traduit par " le mot grec "**工作器幂等性。**Si le travail s'effondre, les tâches peuvent être prises plusieurs fois.
- **Durable queue.**Utilisez Kafka, Redis Streams ou une file d'attente basée sur une base de données pour la production. `queue.Queue`est seulement en mémoire.
  Le mot grec traduit par " le mot grec "**持久队列。**L'utilisation de Kafka, Redis Streams ou de la base de données`queue.Queue`                                                                                                                                                                                                                                                              
- **Observability per task.**Chaque tâche a une identification de trace; chaque travailleur enregistre le début et la fin.
  Le mot grec traduit par " le mot grec "**每个任务的可观测性。**Chaque tâche a une identification de suivi; chaque travail utilise son enregistrement commence/finit.
- **Back-pressure.**Si la file d'attente croît plus vite que les travailleurs ne le drainent, ralentissez le producteur.
  Le mot grec traduit par " le mot grec "**背压。**Si la croissance des rangs est rapide à la vitesse de l'équipement, la production ralentit.

## Les exercices

1. On court .`code/main.py`Combien plus rapide est la charge de travail séquentielle sur la durée variable ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Combien de groupes sont plus nombreux que les autres sur la charge de travail en temps variable ?
2. Ajouter une variante de la file d'attente prioritaire (utilisation `queue.PriorityQueue`) Assigner la priorité par champ "importance" des tâches. Observer si les tâches à faible priorité sont jamais en train de mourir de faim sous charge continue.
   Le mot "coup" est le mot "coup" en français.`queue.PriorityQueue`)¬ en fonction de la tâche "importance" 字段分配优先级――观察低优先级任务是否 under continuous load Hunger――
3. Implémentation d'un détecteur de points chauds: enregistrer lorsque un travailleur traite 3 fois plus de tâches que le travailleur le plus lent.
   En français, traduit par " réaliser un détecteur de point de chaleur ": quand un appareil de travail traite plus de 3 fois la tâche de l'appareil le plus lent, cela indique que la répartition du temps de travail est caractéristique ?
4. Lisez l'abstrait du document Matrix (arXiv:2511.21686) et la section 3. Identifiez un compromis spécifique que la Matrix accepte (gains d'évolutivité) et celui qu'elle abandonne (traçabilité, déterminisme).
   Le texte de la première partie est le texte de la première partie de la première partie.
5. Convertir la démo swarm à utiliser un `queue.Queue`Les tâches sont généralement des tâches de type "tâche_type" ou "cargo utile" qui ne sont pas des tâches de type "tâche_type" ou "cargo utile" et qui ne sont pas des tâches de type "tâche_type" ou "cargo utile" qui sont des tâches de type "tâche_type" ou "cargo utile"), les travailleurs ne s'abonnent qu'à des types spécifiques.
   Le groupe de travail est composé de deux groupes de personnes.`queue.Queue`, les machines de travail ne peuvent être utilisées que pour un type spécifique.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Encore une lecture

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) soutien explicite de la bande
  L'équipe de travail et de travail de l'agent  群体架构  明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) Envahisseur complet de messages
  Le système de décentralisation de l'information
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) pourquoi un système de production spécifique a explicitement choisi le superviseur plutôt que le swarm
  Traduction anglaise:Anthropic Engineering  Pourquoi un système de recherche choisit un surveillant plutôt que un groupe  Pourquoi un système de production spécifique choisit clairement un surveillant plutôt que un groupe
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) l'acteur événement-driven réécrire, plus proche de la foule que le groupe de chat de v0.2
  Le groupe de discussion est un groupe de discussion qui se concentre sur les activités de communication.
