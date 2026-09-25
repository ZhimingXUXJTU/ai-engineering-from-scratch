# Les échanges entre les agents  LangGraph vs CrewAI vs AutoGen vs Agno  Agent  Framework vs LangGraph vs CrewAI vs AutoGen vs Agno
# Comptes d'affaires sur le cadre des agents  Graphique, rôle et orchestration des acteurs

> Chaque framework vend la même démo (un agent de recherche crée un rapport) et cache le même bug (un schéma d'état lutte avec la couche d'orchestration). Choisissez le framework dont les abstractions correspondent à la forme de votre problème; tout le reste est de la colle que vous écrivez deux fois.

> **【中文解读】**Chaque cadre montre le même démo, chaque cadre cache le même bug, chaque cadre choisit un cadre abstrait qui correspond à votre problème, le reste est le code à écrire deux fois.

> **【拓展：框架选择→Agent工程实践】**LangGraph  adapté à la nécessité de contrôles précis de flux de travail en état; CrewAI  adapté à plusieurs rôles; AutoGen  adapté à plusieurs agents de conversation; sélection de cadre est la principale cause du succès du projet  Agent.

>  **【前置】**Le programme est basé sur la méthode de formation de base de la formation de base de l'équipe de formation de formation de formation de formation.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Vous avez une tâche qui nécessite plus d'un appel de LLM. Peut-être est-ce un flux de travail de recherche (plan, recherche, résumé, citation). Peut-être est-ce un pipeline de code-révision (parse diff, critique, patch, validation). Peut-être est-ce un assistant multi-tours qui livre des vols, écrit des e-mails, et des rapports de dépenses. Vous choisissez un cadre.

> Vous avez besoin de plusieurs fois de la M.L.L. 调用任务──也许是研究工作流(规划、搜索、总结、引用)──也许是代码审查流水线(解析 diff、批评、修补、验证)──你选择一个框架──

Trois jours plus tard, vous découvrez la fuite d'abstractions du cadre. CrewAI vous donne des rôles mais vous combat quand le "chercheur" doit remettre un plan structuré à l'"écrivain". AutoGen vous donne un chat entre agents mais n'a pas d'état de première classe donc votre point de contrôle est un picot d'un journal de conversation. LangGraph vous donne un graphique de l'état mais vous oblige à nommer chaque transition avant de savoir ce que fera l'agent. Agno vous donne une abstraction à un seul agent qui crie quand vous essayez de diffuser à trois travailleurs concurrents.

> Trois jours plus tard, vous découvrez une fuite d'abstraction du cadre. L'équipe vous donne un rôle, mais quand le " chercheur " a besoin de fournir un plan structurel à l'écrivain, il y a des problèmes. AutoGen vous donne un agent, mais pas un statut civil.

La solution n'est pas de " choisir le meilleur cadre. " Il est de correspondre l'abstraction de base du cadre à la forme de votre problème.

> La méthode de réparation n'est pas de " choisir le meilleur cadre " mais de faire correspondre l'abstraction centrale du cadre à la forme de votre problème.


> **【中文解读】**Agent 框架选型的三个维度:(1) 任务复杂度简单 RAG 用LlamaIndex,复杂 Agent 用LangGraph;(2) 团队经验新手用LangChain 模板,专家用原生API;(3) 生产要求需要LangSmith 集成选LangChain 生态──

>  **【类比】**选 Agent 框架像选交通工具短途买菜用自行车(stdlib + function calling),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ⋅

> ️ **【易错点】**框架选错的 3 个常见原因:**跟风最热门**AutoGen 火就上 AutoGen, résultat de découverte des tâches sont simplement un seul agent + un outil, un surcroît d'ingénierie;**被 demo 误导**Demo du "Résident+Écrivain" de CrewAI semble très cool, mais la tâche réelle dans le rôle est floue, le rôle du CrewAI est abstrait et retracé; faites d'abord une correspondance de l'abstrait de PoC 验证抽象──(3) **低估迁移成本** Commencer à utiliser Agno 简单, ultérieurement à ajouter Agent 时发现Agno不支持,重写到 LangGraph 花两周;选框架时看 6 个月后的需求──


## Le concept de base.

> **【中文解读】**L'agent  cadre de sélection est un projet de poids: LongChain 生态最完整但复杂度高,LlamaIndex 专注RAG,CrewAI 适合多 Agent 协作,LangGraph 适合状态机控制流,直接使用API最灵活但要自己写更多代码──

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph);(2) 团队经验(新手用 LangChain 模板,专家用原生API);(3) 生产要求(LangSmith 集成选 LangChain 生态)。2025年趋势是框架轻量化──


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

Quatre cadres dominent le paysage de 2026 et leurs abstractions fondamentales ne sont pas les mêmes.

> Quatre cadres ont dominé la structure de l'année 2026: leurs abstractions fondamentales sont différentes.

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### Ce que signifie réellement "abstraction"

L'abstraction de base d'un cadre est ce que vous dessinez sur le tableau blanc lorsque vous lancez l'architecture.

> Le cadre est le centre de l'abstraction de ce que vous avez peint sur une planche blanche lorsque vous vendez une architecture.

- **LangGraph**→ vous dessinez un graphique. Les nœuds sont des étapes, les bords sont des transitions, et l'objet d'état à chaque point est tapé.
  Vous dessinez un tableau. Le point est un pas, le côté est un changement.
- **CrewAI**→ vous dessinez un tableau d'org. Chaque rôle a une description de poste et un gestionnaire route les tâches.
  Vous dessinez une organisation. Chaque rôle a une description de responsabilité, un gestionnaire distribue des tâches.
- **AutoGen**Deux agents se font un message, un troisième se joint si vous avez besoin d'un modérateur.
  Tu as dessiné un Slack 私信. Deux agents.
- **Agno**→ vous dessinez une seule boîte avec des outils suspendus dessus. Placez des boîtes côte à côte pour une équipe. Le modèle mental est "agent avec des batteries inclus".
  Vous dessinez un cadre suspendu à l'outil.

### La question de l'État

L'État est le point où la plupart des choix de cadre se décomposent dans la production.

> L'état est le lieu où la plupart des cadres de choix sont en production.

- **LangGraph.**État de type (`TypedDict`Les modèles de calcul de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de
  **LangGraph。**类型化状态`TypedDict`Ou Pydantic 模型) 、每字段 reducer、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见Phase 11 · 16──)
- **CrewAI.**Les flux d' état sont des chaînes entre les tâches via le `context`Le champ ou structuré par`output_pydantic`Aucun magasin durable par équipage, vous devez vous enfuir si l'équipage doit survivre à un redémarrage.
  **CrewAI。**状态作为字符串在任务间通过 `context`字段流动, ou par le biais `output_pydantic`结构化── open box non durable par équipage  stockage; si l'équipage  doit survivre  re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re re
- **AutoGen.**L' état est l' historique de chat et toute définition utilisateur `context`. Les transcriptions de conversation persistent; l'état de flux de travail arbitraire ne le fait pas à moins que vous écriviez des adaptateurs.
  **AutoGen。** état est l' histoire du chat et de toute définition utilisateur `context` enregistrement de dialogue; état de flux de travail arbitrary non-permanent, sauf écrit adaptateur
- **Agno.**Les pilotes de stockage intégrés (SQLite, Postgres, Mongo, Redis, DynamoDB) sont attachés à un `Agent`par le biais `storage=` Les sessions de conversation et les souvenirs des utilisateurs persistent automatiquement.
  **Agno。**Le système de gestion de données est basé sur le système de gestion de données.`storage=`- Je suis là.`Agent`Le record de l'utilisateur est automatiquement conservé.

- **LangGraph.**État de type (`TypedDict`Les modèles de calcul de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de
- **CrewAI.**Les flux d' état sont des chaînes entre les tâches via le `context`Le champ ou structuré par`output_pydantic`Aucun magasin durable par équipage, vous devez vous enfuir si l'équipage doit survivre à un redémarrage.
- **AutoGen.**L' état est l' historique de chat et toute définition utilisateur `context`. Les transcriptions de conversation persistent; l'état de flux de travail arbitraire ne le fait pas à moins que vous écriviez des adaptateurs.
- **Agno.**Les pilotes de stockage intégrés (SQLite, Postgres, Mongo, Redis, DynamoDB) sont attachés à un `Agent`par le biais `storage=` Les sessions de conversation et les souvenirs des utilisateurs persistent automatiquement.

### La question de la branche

Tous les agents non triviaux sont des branches.

> Chaque agent extraordinaire a une branche.

- **LangGraph** vous décidez, via des bords conditionnels. Le routage est une fonction Python avec des branches nommées. Les branches sont de première classe dans le graphique compilé; le point de contrôle enregistre la branche qui a été prise.
  **LangGraph**你决定,通过条件边──路由是带命名分支的Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI** le gestionnaire décide en mode hiérarchique; en mode séquentiel, vous décidez au moment de la construction. Le routage est implicite dans la liste de tâches; il n'y a pas de "si" de première classe en dehors de la demande du gestionnaire.
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定──路由隐含在任务列表中;经理提示外无一等公民"if"──
- **AutoGen**Les agents décident par chat.`GroupChatManager`sélectionne le prochain haut-parleur; vous pouvez écrire à la main un `speaker_selection_method`Mais le défaut est basé sur le LLM.
  **AutoGen**Agent 通過聊天決定──分支從誰下一個說話中涌现──`GroupChatManager`选下一个发言人;可手写 `speaker_selection_method`Mais il est vrai que le droit d'auteur est une loi.
- **Agno** l'agent décide par quel outil appeler ensuite. les équipes ont un mode coordinateur/router/collaborateur; le développement est responsable de brancher au-delà de cela.
  **Agno**Agent 通过下一个调用哪个工具决定──团队有协调员/路由器/合作者模式;

- **LangGraph** vous décidez, via des bords conditionnels. Le routage est une fonction Python avec des branches nommées. Les branches sont de première classe dans le graphique compilé; le point de contrôle enregistre la branche qui a été prise.
- **CrewAI** le gestionnaire décide en mode hiérarchique; en mode séquentiel, vous décidez au moment de la construction. Le routage est implicite dans la liste de tâches; il n'y a pas de "si" de première classe en dehors de la demande du gestionnaire.
- **AutoGen**Les agents décident par chat.`GroupChatManager`sélectionne le prochain haut-parleur; vous pouvez écrire à la main un `speaker_selection_method`Mais le défaut est basé sur le LLM.
- **Agno** l'agent décide par quel outil appeler ensuite. les équipes ont un mode coordinateur/router/collaborateur; le développement est responsable de brancher au-delà de cela.

### La question de l'observabilité

> Problèmes de réflexion

- **LangGraph** OpenTelemetry via LangSmith ou tout exportateur OTel. Chaque transition de nœud est une durée de traçabilité; les points de contrôle sont doubles en tant que traces jouables. LangSmith est l'option de première partie; Langfuse/Phoenix possède également des adaptateurs.
  **LangGraph**À travers LangSmith ou tout autre 导出器 de OTel 导出器的 OpenTelemetry──每个节点转换是一个跟踪跨度;检查点兼作重放追踪──LangSmith est la première option;Langfuse/Phoenix 也有适配器──
- **CrewAI** OpenTelemetry de première classe depuis fin 2025; intégrations avec Langfuse, Phoenix, Opik, AgentOps.
  **CrewAI**2025 年末起一等公民OpenTelemetry; 集成 Langfuse、Phoenix、Opik、AgentOps。
- **AutoGen** L'intégration de OpenTelemetry via `autogen-core`Les connecteurs sont des connecteurs, la granularité de traçage est par message agent, pas par nœud.
  **AutoGen**- Je suis là.`autogen-core`Les données de suivi sont données par l'agent, pas par le point de contact.
- **Agno** intégré `monitoring=True`flag plus les exportateurs OpenTelemetry; intégration étroite avec Langfuse pour les traces de session.
  **Agno**内置 `monitoring=True`标志加 OpenTelemetry 导出器;与 Langfuse 紧密集成会话追踪──

### Coût et latence

Les quatre cadres ajoutent des frais généraux par appel (logie du cadre, validation, sérialisation). ordre approximatif d'augmentation des frais généraux: Agno ≈ LangGraph < CrewAI ≈ AutoGen. La différence est dominée par le montant supplémentaire de la mise en route du cadre.`GroupChatManager`LangGraph ne dépense que des jetons là où vous écrivez.`llm.invoke`Le chemin d'Agno est mince.

> Les quatre cadres augmentent chaque fois que les cours sont utilisés.

Lorsque le coût par course est important, préférer le routage explicite (LangGraph edges, AutoGen `speaker_selection_method`) sur le parcours sélectionné par le LLM.

> Lorsque le coût de fonctionnement est important, la priorité est d'utiliser des routes explicites plutôt que des routes LLM.

### Interopérabilité

> 互操作性

- **LangGraph** **LangChain**outils, récupérateurs, LLM. Adapteur MCP de première classe (outils importés en tant que serveurs MCP).
  **LangGraph** **LangChain**工具、检索器、LLM──一等公民 MCP 适配器(工具作为 MCP 服务器导入)
- **CrewAI** les outils hérités de `BaseTool`Les outils LangChain, LlamaIndex et MCP s'adaptent tous à l'équipage.`allow_delegation=True`- Je suis désolé .
  **CrewAI** 工具继承自 `BaseTool`;LongChain 工具、LlamaIndex 工具、MCP 工具都适配进来──Crew-to-crew 委派通过 `allow_delegation=True`Il y a une autre.
- **AutoGen**- Je suis là.`FunctionTool`Il est possible de mettre en place un adaptateur MCP disponible, un couplage serré avec l'écosystème AG2 pour les modèles agent-agent.
  **AutoGen**- Je suis là.`FunctionTool`Package de tout Python pouvant être utilisé; MCP 适配器可用──
- **Agno**- Je suis là.`@tool`décorateur ou sous-classe BaseTool; adaptateur MCP; les outils peuvent être partagés entre les agents et les équipes.
  **Agno**- Je suis là.`@tool`装饰器或BaseTool 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## La compétence

> Vous pouvez expliquer, en une phrase, pourquoi un cadre donné est bon pour un problème d'agent donné.
> Tu peux utiliser une phrase pour expliquer pourquoi un cadre s'adapte à un problème d'agent.

Liste de contrôle préconstruite:

> 构建前检查清单:

1. **Draw the shape.**Est-ce un graphique (état typé, transitions nommées)? un jeu de rôle (les spécialistes abandonnent le travail)? un chat (les agents parlent jusqu'à ce qu'ils aient fini)? un agent unique avec des outils?
   **画出形状。**C'est un dessin, un rôle, une conversation ou un agent avec des outils ?
2. **Decide who branches.**Le développement décide de la branche → LangGraph. Le gestionnaire décide de l'agent → CrewAI hiérarchique.
   **决定谁分支。**开发者决定 → LangGraph──经理 Agent decis → CrewAI──聊天涌现 → AutoGen──工具调用决定 → Agno──
3. **Check the state budget.**Si oui, LangGraph est la fonction par défaut; les sessions Agno couvrent l'état de la conversation.
   **检查状态预算。**Vous avez besoin de récupérer du point de contrôle ?
4. **Check the cost budget.**Le routage sélectionné par LLM coûte des jetons supplémentaires par tour.
   **检查成本预算。**Les actions de la Commission sont les suivantes:
5. **Budget the framework overhead.**Chaque cadre est une autre dépendance. Si la tâche est deux appels LLM et un outil, écrivez 30 lignes de Python simple; aucun cadre est moins cher que aucun cadre.
   **预算框架开销。**Chaque cadre est une autre dépendance. Si la tâche est seulement deux fois LLM 调用一个工具, écrire 30 行纯Python.

Ne cherchez pas un cadre avant de pouvoir dessiner le graphique, le graphique d'org, le chat ou la boîte d'agents.

> Avant de pouvoir dessiner, organiser, parler ou créer un cadre d'agent, ne pas tendre la main sur le cadre. Ne choisissez pas quelque chose qui vous oblige à combattre pour son modèle d'état.

## La matrice de décision

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## Les exercices
```figure
l5-framework-fit
```

## Exercices

1. **Easy.**Prenez la même tâche  "rechercher le siège social d'Anthropic, écrivez un bref de 200 mots, citer des sources"  et mettez-le en œuvre dans LangGraph (quatre nœuds: planifier, rechercher, écrire, citer) et dans CrewAI (trois rôles: chercheur, écrivain, éditeur). Rapporte le coût des jetons par exécution et lignes de code.
   Utilisez la même mission dans LangGraph et CrewAI, pour rendre compte du nombre de tokens, de composants et de codes de chaque opération.
2. **Medium.**Construire la même tâche dans AutoGen (chercheur  chat écrivain, éditeur rejoint via `GroupChat`) et Agno (un seul agent avec `search_tools`et `write_tools`Les quatre mises en œuvre sont classées selon: a) le coût par course, b) la capacité de reprendre après un accident, c) la capacité d'injecter une approbation humaine avant la phase de rédaction.
   Dans AutoGen et Agno, réaliser la même tâche, selon le coût, la capacité de récupération, la capacité d'approbation artificielle, la capacité d'injection.
3. **Hard.**Construire un script d' arbre de décision `pick_framework.py`qui prend une brève description du problème (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`Il est nécessaire de vérifier la validité de la recommandation dans six cas que vous avez conçus vous-même.
   构建决策树脚本, selon la description du problème

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Encore une lecture

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) StateGraph, points de contrôle, interruptions, voyage dans le temps.
  LangGraph 文档StateGraph、检查点、中断、时间旅行。
- [CrewAI documentation](https://docs.crewai.com/) équipages, flux, agents, tâches, processus.
  L'équipage, le flux, l'agent, le processus.
- [AutoGen documentation](https://microsoft.github.io/autogen/) ConversableAgent, GroupeChat, équipes, outils.
  AutoGen 文档ConversableAgent、GroupChat、équipes、outils。
- [Agno documentation](https://docs.agno.com/) Agent, équipe, flux de travail, stockage, mémoire.
  Agno 文档Agent、Équipe、Flow de travail、 stockage、mémoire。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) bibliothèque de modèles (chaîne de commande, routage, parallélisation, orchestrateur-travailleur, évaluateur-optimisateur)
  Le modèle de l'agent efficace est un modèle de l'agent efficace.
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) la boucle chaque cadre s'habille.
  Chaque cadre est dans l'emballage du cycle ReAct.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) Le papier de conception d'AutoGen.
  Autogénération de conception
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442) fondation de jeu de rôle sur laquelle les piles de personnages de style CrewAI s'appuient.
  CrewAI 风格角色堆所基于的角色扮演基础──
- La phase 11 · 16 (Langgraph)  le cadre par lequel cette leçon est comparée.
  Le cadre de base de cette formation est celui de la formation.
- Phase 11 · 19 (Réflexion)  un schéma qui correspond bien à LangGraph mais maladroitement à CrewAI.
  Un modèle clair dans LangGraph mais malhonnête dans CrewAI.
- Phase 11 · 22 (observabilité de la production)  comment utiliser l'instrument quel que soit le cadre que vous choisissez.
  Comment ajouter un cadre de votre choix ?
