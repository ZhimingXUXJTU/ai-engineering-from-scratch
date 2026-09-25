# Le modèle primitif multi-agent.

> Quatre primitives, rien de plus  l'agent, la remise en main, l'état partagé, l'orchestrateur  couvrent un espace de conception quadri-dimensionnel, et les principaux cadres multi-agents expédiés en 2026 (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework) sont des points dans celui-ci. Cette leçon les construit à partir de zéro, exécute un système de jouets sur les quatre, puis repère chaque cadre majeur sur les mêmes axes afin que vous puissiez lire toute nouvelle version en un paragraphe.

> **【中文解读】**Ce chapitre présente les unités de construction les plus élémentaires du système de multiples agents et les interactions.

> **【拓展：primitive model→具体应用】**Le modèle de langage original minimal du système défini le mode de communication de base entre les agents: 1) le message de l'agent par l'envoi de messages; 2) l'état de l'agent par l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture; 3) l'état de l'agent par l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**學本節前Please first master:Phase 14 (Agent 工程) 、Phase 16·01 (多 Agent 动机) 。本节是Phase 16's core4 个原语 (agent/handoff/shared-state/orchestrator) 定义所有框架的设计空间──
>  **【类比】**4 原语 = "音乐四件套":agent(乐手)、handoff(独奏接力)、shared state(总谱)、orchestrator(指挥)。AutoGen 偏消息传递、LangGraph 偏共享状态、CrewAI 偏角色分工 sont toutes ces 4 compositions différentes de l'original.

## ♪ Problème ♪ Introduction du problème ♪

Chaque six mois, un nouveau framework multi-agents est lancé. AutoGen en 2023. CrewAI en 2024. LangGraph et OpenAI Swarm en 2024. Google ADK en avril 2025. Microsoft Agent Framework RC en février 2026. Chaque communiqué de presse affirme être "l'abstraction correcte".

> Chaque six mois, un nouveau cadre multi-agents sera publié. AutoGen de 2023 et CrewAI de 2024 seront publiés. LangGraph et OpenAI Swarm de 2024 seront publiés. Google ADK de 4 avril 2025 seront publiés.

Le churn est réel mais les primitives sous-jacentes ne changent pas. Ce qui ressemble à l'innovation est souvent le rebranding: les mêmes quatre boutons (agent, remise, état partagé, orchestrateur) avec des défauts et une syntaxe différentes. Une fois que vous voyez les primitives, le marketing tombe.

> 变化 est réelle mais le langage original de base n'a pas changé. ⇒ Looks like innovation is often rebranding: the same four-cycle:  (Agent, contact, état de partage, éditeur) with different default values and languagefacts. ⇒ Une fois que vous voyez le langage original, le marketing disparaît.

Si vous essayez de les apprendre un à la fois, vous allez vous épuiser. Les API sont différentes. Les docs ne sont pas d'accord sur ce qu'est un "agent". Un cadre appelle sa mémoire partagée un "tableau noir", un autre le nomme un "pools de messages", un troisième le nomme un "StateGraph". Vous commencez à soupçonner que le champ est juste en train de se bouger.

> Si vous essayez de les apprendre en un seul endroit, vous serez fatigué de vous. L'API semble différente.

Les quatre primitives sont stables, apprenez-les une fois, lisez chaque nouveau cadre en un paragraphe.

> En réalité, ce n'est pas le cas.

## Concept Le concept central

### Les quatre primitifs

1. **Agent** un prompt système plus une liste d'outils. Stateless; chaque exécution commence à partir de son prompt système et de l'historique de message actuel.
   Le mot grec traduit par " le mot grec "**Agent** Un système de suggestions ajoutées à une liste d'outils.
2. **Handoff** un transfert structuré de contrôle d'un agent à un autre. mécaniquement, un appel à l'outil qui renvoie un nouvel agent ou un bord de graphique qui suit une condition.
   Le mot grec traduit par " le mot grec "**交接** Transfert de contrôle structurel d'un agent à un autre agent.
3. **Shared state** toute structure de données que plus d'un agent peut lire (parfois écrire).
   Le mot grec traduit par " le mot grec "**共享状态** Plusieurs agents peuvent lire (à l'intérieur de la structure de données) 
4. **Orchestrator** qui décide qui parle ensuite. Options: un graphique explicite (déterministique), un sélecteur de haut-parleurs LLM (mous), l'appel de l'autre haut-parleur (OpenAI Swarm), ou un planificateur sur une file d'attente (architecture de swarm).
   Le mot grec traduit par " le mot grec "**编排器** décider qui est le prochain intervenant dans un échange de mots.

Chaque cadre choisit les paramètres par défaut pour chaque axe; le reste est la syntaxe de surface.

> C'est le design space entier. Chaque cadre est une valeur de choix de chaque axe.

Il n'existe pas de cadre multi-agents "meilleur". Il n'existe que "meilleur pour les préférences d'axe de votre tâche". Un cadre qui orchestre l'orchestration pour les pipelines déterministes (LangGraph) est mal adapté aux conversations émergentes (utiliser AutoGen).

> 含义: pas de "meilleur" multi-agent 框架──only"best suited to your task axis preferential" framework──en définition de flux de l'eau piégé sur le cadre de la rédaction (en anglais)

### Comment chaque cadre 2026 le trace

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

> Je suis un agent de la télévision.
> Je suis en train de vous dire que vous êtes en train de mourir.
> Je suis un homme qui a été tué par les agents.`Agent(instructions, tools)`Je reviens à l'agent.
> Je suis un homme qui a une bonne idée.`ConversableAgent`Je suis un homme qui a une bonne idée de ce que je veux dire.
> ♪ L' équipage est là. ♪`Agent(role, goal, backstory)`Je suis là.`Process.Sequential / Hierarchical`Je suis un homme qui a des problèmes avec la police.
> Je suis un homme qui a une vieille expérience.`StateGraph`Je suis un homme qui a une bonne idée.
> Je suis un agent de Microsoft. Je suis un agent de Microsoft.
> Je suis un agent de Google ADK + carte A2A

Les différences de surface sont énormes, sous les quatre boutons.

> La différence de surface est grande.

### Pourquoi cela importe ?

Une fois que vous voyez les primitifs, la comparaison du cadre devient une courte liste de contrôle:

> Une fois que vous avez vu le langage original, Framework comparator devient une liste de contrôle simple:

- Le chef d'orchestre fait-il confiance au LLM pour le routage (Swarm) ou le routage est-il en code (LangGraph)?
  Le code est également en cours de rédaction.
- Est-ce que l'état est partagé dans l'histoire complète (GroupChat) ou projeté (Reducteur de l'état-graphe)?
  Le groupe de discussion est-il en train de se développer ?
- Les agents peuvent-ils modifier les instructions de l'autre (gérant de l'équipement d'exploration) ou seulement les envoyer (swarm)?
  L'agent 能否修改彼此的提示?

Ces trois questions répondent à 80% du cadre qui correspond à un problème donné. Vous arrêtez de chercher le meilleur cadre multi-agents et commencez à concevoir pour l'axe qui vous intéresse vraiment.

> Ces trois questions répondent à 80% du cadre qui convient à un problème donné. Vous ne vous achetez plus le "meilleur cadre multi-agent", mais commencez à concevoir un axe qui vous intéresse vraiment.

Lorsque un nouveau cadre sera lancé en 2027, posez les trois questions. Si ses réponses correspondent à un cadre que vous utilisez déjà, sautez la migration. Si elles diffèrent sur un axe qui vous intéresse, évaluez. La plupart des nouveaux cadres sont de repackaging, pas d'innovation.

> Lorsque le nouveau cadre de 2027 sera publié, vous devrez répondre à ces trois questions. Si la réponse correspond au cadre que vous utilisez déjà, sautez vers le bas. Si elles ne sont pas sur l'axe que vous aimez, évaluez. La plupart des nouveaux cadres sont rechargés, pas innovants.

### Le discernement sans État

Tout élément primitif, à l'exception de l'état partagé, est sans état. L'agent est une fonction de (prompte, outils).**The only stateful thing in the system is shared state.**C'est là que vivent tous les bugs intéressants: empoisonnement de la mémoire (leçon 15), commande de messages, versionnement, contention de rédaction.

> À l'exception du mode de partage, chaque langue originale est sans état.**系统中唯一有状态的东西是共享状态。**C'est là que se trouve le bug intéressant: le contenu de l'écriture.

Cette compréhension conduit à une stratégie de débogage: lorsqu'un système multi-agents se comporte mal, regardez d'abord l'état partagé. Le pool de messages est-il empoisonné? Les messages sont-ils ordonnés correctement? Le schéma est-il respecté? Les agents apatrides causent rarement des bugs subtils; l'état partagé les provoque constamment.

> Cette idée est motivée par la stratégie de révision: Lorsque plusieurs agents comportent des systèmes de manière anormale, il faut d'abord vérifier l'état de partage.

Les cadres qui cachent l'état partagé (Swarm) poussent le problème vers l'appelant. Les cadres qui le centralisent (checkpoint LangGraph, pool AutoGen) le rendent inspectable mais déplacent le coût de coordination sur la mise en œuvre de l'état partagé.

> 藏藏共享状态的框架(Swarm) va faire passer le problème au utilisateur──集中化它的框架(Langgraph 检查点、AutoGen 池) rend son contrôle possible mais va transférer les coûts de coordination vers le partage de l'état de réalisation ⋅

### Anatomie d'une seule primitive

#### - Ça va ?

```
Agent = (system_prompt, tools, model, optional_name)
```

Deux agents avec le même système de commande et des outils sont interchangeables. Tout ce qui ressemble à l'état par agent est en fait dans l'état partagé ou le protocole de transfert.

> 没有记忆. 没有状态. 没有状态. 没有状态. 没有记忆. 没有状态. 没有状态. 没有记忆. 没有状态. 没有状态. 没有记忆. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态. 没有状态.

C'est contre-intuitif mais puissant: les agents apatrides sont parallèles, réinitialisables et échangeables. On peut faire 100 copies du même agent et ils se comportent tous de la même manière.

> C'est contre-intuitif mais fort: agent sans état peut facilement être assimilé, redémarré et remplacé. Vous pouvez démarrer 100 copies du même agent, leur comportement est complètement le même.

#### Retour

```
Handoff = (from_agent, to_agent, reason, payload)
```

Trois mises en œuvre dominent:

> 3 types de réalisations:

- **Function return** l'outil renvoie le prochain agent. Ceci est le modèle OpenAI Swarm. Les agents transportent le routage dans leurs schémas d'outils.
  Le mot grec traduit par " le mot grec "**函数返回** 工具返回下一个 Agent──这是OpenAI Swarm's模式──Agent dans son mode de l'outil································································································································································································································································································································································································································································································
- **Graph edge** LangGraph. Les bords sont déclaratifs. Le LLM produit une valeur; une condition sélectionne le nœud suivant.
  Le mot grec traduit par " le mot grec "**图边** LangGraph──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection** AutoGen GroupChat. Une fonction sélectrice (parfois elle-même appel LLM) lit le pool et choisit qui parle ensuite.
  Le mot grec traduit par " le mot grec "**发言者选择** AutoGen GroupChat。 sélectionneur fonction(

#### État partagé

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

Au moins une liste de messages. Plus souvent: des objets structurés (expériences de tâches CrewAI), un contexte typé (réducteurs de LangGraph), une mémoire externe (MCP, vecteur DB).

> Au moins une liste de messages.

La forme de l'état partagé détermine les types de coordination possibles. Une liste de messages plate rend la diffusion facile mais le filtrage spécifique au rôle difficile. Un schéma typé rend le filtrage trivial mais nécessite une conception anticipée. Il n'y a pas de déjeuner gratuit.

> La forme du statut commun détermine le type de coordination possible. La liste de messages simples rend la diffusion facile mais les rôles spécifiques sont difficiles.

Deux topologies: **full pool**(tous les agents voient chaque message) et **projected**Les pools complets sont simples et à faible échelle.

> 两种拓:**完整池**(Chaque agent voir chaque article de nouvelles) et**投影**(Agent voir le champ de rôle) ◊ la gamme complète est simple mais élargie ◊ la gamme de projections est élargie mais nécessite un modèle de conception à terme ◊

#### Orchestreur

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Quatre saveurs:

> Quatre styles:

- **Static** le graphique est fixé au moment de la construction (Deterministique LangGraph, Sequentiel CrewAI).
  Le mot grec traduit par " le mot grec "**静态** 图在构建时固定(Langgraph 确定性、CrewAI Sequential)
- **LLM-selected** un LLM lit le tableau et choisit le prochain conférencier (AutoGen, CrewAI Hiérarchique).
  Le mot grec traduit par " le mot grec "**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI Hiérarchique)
- **Handoff-driven** l'agent actuel décide en appelant un outil de remise (Swarm).
  Le mot grec traduit par " le mot grec "**交接驱动** Actuel agent 通过调用交接工具决定(Swarm)
- **Queue-driven** les travailleurs tirent de la file d'attente partagée; aucun haut-parleur suivant explicite (architectures de masse, Matrix).
  Le mot grec traduit par " le mot grec "**队列驱动** 工作器 from共享队列拉取;没有明确的下一个发言人(群体架构、马特里克斯)

### Quels changements entre cadres

Une fois les primitives fixées, les décisions de conception restantes sont:

> Une fois le langage original fixé, les décisions de conception restantes sont:

- **Memory strategy** contrôle éphémère par rapport à contrôle durable (contrôle LangGraph).
  Le mot grec traduit par " le mot grec "**内存策略** 临时 vs 持久检查点 (point de contrôle de la longographie)
- **Safety boundary** qui peut approuver une remise (humain-in-the-loop).
  Le mot grec traduit par " le mot grec "**安全边界** 谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接)   谁可以批准交接 ( 谁可以批准交接)    谁可以批准交接 ( 谁可以批准交接)                                                                                                                                                                        
- **Cost accounting** budgets de jetons par agent.
  Le mot grec traduit par " le mot grec "**成本核算** Le budget de chaque agent.
- **Observability** Tracer les remises, persister dans l'état pour la répétition.
  Le mot grec traduit par " le mot grec "**可观测性** Suivre la communication  maintenir l'état afin de le renvoyer 

Toutes sont mises en œuvre en plus des primitives.

> Tout peut être réalisé sur les langues originales.

Lorsqu'un framework annonce une fonctionnalité "nouvelle" (humain en boucle, retry, budget de jeton), vérifiez s'il introduit réellement une nouvelle primitive ou simplement les quatre. Presque toujours la dernière. Les quatre primitives sont stables; tout le reste est composition.

> Lorsque le cadre propage la fonction "nouvelle" (en revanche, en revanche, en revanche, en revanche, en revanche, en revanche, en revanche, en revanche, en revanche, il est nécessaire de vérifier si le cadre a réellement introduit les quatre langues originales ou si il les a simplement assemblées.

## Construisez-le et mettez-le en œuvre.
```figure
a5-primitive-radar
```

## Faites-le

`code/main.py`Il est utilisé pour la mise en œuvre des quatre primitives dans ~ 150 lignes de stdlib Python.

> `code/main.py`Avec environ 150 pages de bibliothèque standard Python, il a réalisé quatre langues originales. Il n'y a pas de véritable LLM. Chaque agent est une stratégie de scripting, ce qui permet de rester concentré sur la structure de coordination.

Les exportations de dossiers:

> 文件导出:

- `Agent` une classe de données de nom, de prompt système, d'outils, de fonction de politique.
  Le mot grec traduit par " le mot grec "`Agent` 名称、系统提示、工具、策略函数 的数据类──
- `Handoff` une fonction qui renvoie un nouvel agent.
  Le mot grec traduit par " le mot grec "`Handoff` 返回新 Agent's function──
- `SharedState` une base de messages sécurisée.
  Le mot grec traduit par " le mot grec "`SharedState` 线程安全的消息池──
- `Orchestrator` trois variantes: `StaticOrchestrator`- Je suis là .`HandoffOrchestrator`- Je suis là .`LLMSelectorOrchestrator`(simulé).
  Le mot grec traduit par " le mot grec "`Orchestrator` 三种变体:`StaticOrchestrator`- Je suis là.`HandoffOrchestrator`- Je suis là.`LLMSelectorOrchestrator`Je suis désolé.

La démo exécute le même pipeline de trois agents (recherche -> écrit -> examen) à travers les trois types d'orchestrateur et imprime le pool de messages à la fin. Vous pouvez voir que les sorties ne diffèrent que dans *qui choisit ensuite*; les agents et l'état partagé sont identiques sur les circuits.

> 演示通过所有三种编排器类型运行相同三 Agent 流水线(研究 -> 编写 -> 审阅), puis finalement imprimer消息池。 Vous pouvez voir le sort uniquement sur * qui choisit le suivant* sur différents;Agent 和共享状态在所有运行中是相同的。

- Je vais le faire.

```
python3 code/main.py
```

Les résultats attendus: trois circuits d'orchestrateur, un par modèle. Chacun imprime le groupe de messages final. La course guidée par la remise atteint moins d'agents si le chercheur décide de le faire tôt  c'est le compromis de routage LLM en miniature.

> 预期输出: trois fois le système d'édition, chaque mode une fois.  Chaque fois qu'il est imprimé, le système de gestion de l'information finale est terminé.

## Utilisez-le avec le cadre de réalisation

`outputs/skill-primitive-mapper.md`est une compétence qui lit toute base de code multi-agent ou document cadre et renvoie le cartographie quatre-primitive.

> `outputs/skill-primitive-mapper.md`C'est une compétence, lire n'importe quel document de code ou de cadre et revenir à quatre langues originales.

## Envoyez-le . Produit .

Avant d'adopter un nouveau cadre, écrivez la cartographie primitive pour elle. Si vous ne pouvez pas, les documents sont incomplets ou le cadre invente une cinquième primitive (rétrogradation  vérifier pour une saveur d'état partagé que vous n'avez pas vu).

> Avant d'adopter le nouveau cadre, écrivez le programme de programmation du langage original. Si vous ne le faites pas, indiquez que le document n'est pas complet ou que le cadre est en train d'émerger le 5ème cadre de programmation du langage original.

Enfoncer la cartographie dans votre document d'architecture. Quand un nouveau membre de l'équipe rejoint, envoyez-lui la cartographie avant les documents API. Lorsque les versions du framework changent, différez la cartographie, pas le changelog.

> La mise en page sera fixée dans le document d'architecture. Lorsque les membres du nouveau groupe rejoignent l'API, la mise en page sera envoyée avant la mise en page.

## Les exercices

1. On court .`code/main.py`Observez comment le choix de l'orchestre change les agents.
   Le nom de l'agent est utilisé dans le langage de l'agent.`code/main.py`三次──观察编排器选择如何改变哪些代理运行──
2. La mise en œuvre d'un quatrième type d'orchestre: un type de rangée où les agents pollent partagent l'état du travail.
   Suivant: L'article suivant: "L'équipe de contrôle de la sécurité de l'entreprise"
3. Prenez le LangGraph Quickstart et réécrivez-le comme les quatre primitives.
   Quel est l'abstrait du LangGraph qui est 1:1 映射, quel est le facilitateur d'emballage ?
4. Lisez le livre de cuisine OpenAI Swarm. Identifiez lequel des quatre primitifs que Swarm rend le plus ergonomique et lequel il pousse à l'appelant.
   Le Swarm utilise le plus de personnes qui sont en conformité avec l'ingénierie humaine, qui le propose au utilisateur.
5. Trouvez un cadre dans ce tableau qui cache l'état partagé entièrement. Expliquez ce qui se brise lorsque les agents doivent coordonner entre les remises sans relire l'histoire.
   Traduction chinoise: trouver un cadre de partage totalement caché dans le tableau.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Encore une lecture

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) l'articulation la plus claire de l'orchestration guidée par la main
  L'écriture est une référence à la langue française.
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) GroupChat + sélection de conférenciers est la référence pour l'orchestration sélectionnée par le LLM
  中文翻译:AutoGen 稳定文档  GroupChat + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Orchestration du bord du graphique et état partagé basé sur un réducteur
  L'écriture est une référence à la langue française.
- [CrewAI introduction](https://docs.crewai.com/en/introduction) agents de rôle-objectif-histoire de fond, processus séquentiels / hiérarchiques
  Le rôle de l'agent, le processus de séquence et de hiérarchie
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) la ligne AutoGen v0.2 en direct après que Microsoft ait mis v0.4 en maintenance
  Le système d'exploitation de la technologie de l'automobilisme est un système de gestion de la technologie de l'automobilisme.
