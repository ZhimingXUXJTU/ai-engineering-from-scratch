# AutoGen v0.4: Modèle d'acteur et cadre d'agent
# Le modèle d'acteur pour les agents  Messages asynchronisés et temps d'exécution typiés

> Les agents en tant qu'acteurs: échange de messages asynchrone, gestionnaires d'événements, isolation des défauts, concurrences naturelles. AutoGen v0.4 (Microsoft Research, Jan 2025) a redessiné l'orchestration des agents autour de ce modèle; le framework est maintenant en mode maintenance, avec Microsoft Agent Framework (preview publique Oct 2025) comme successeur de production.

> **【中文解读】**AutoGen v0.4 (Microsoft Research Institute, janvier 2025) autour de Actor 模型 redessinée Agent 编排──异步消息交换、事件驱动 Agent、故障隔离、天然并发── ce cadre est actuellement en cours de maintenance, Microsoft Agent Framework (en anglais) est devenu le successeur──

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Décrire le modèle d'acteur: agents en tant qu'acteurs, messages en tant que seul IPC, isolement de défaillance par acteur.
  Le rôle de l'acteur est d'une manière générale le rôle de l'acteur.
- Nommer les trois couches API d'AutoGen v0.4  Core, AgentChat, Extensions  et ce que chacun est pour.
  Le code de l'AutoGen v0.4 est basé sur trois API:
- Expliquez pourquoi la déconnexion de la transmission des messages de la manutention donne une isolation des défauts et une simultanée naturelle.
  Traduction chinoise: expliquer pourquoi la transmission de messages avec la compréhension peut entraîner une rupture et une échec naturels.
- Implémenter un acteur stdlib runtime en Python et portez un flux de révision de code à deux agents sur lui.
  Le code d'examen du code est porté à son niveau.

## Le problème , l' introduction du problème

La plupart des cadres d'agents sont synchrones: un agent produit, un agent consomme, dans une pile d'appels. Les défaillances écrasent la pile. La concurrence est activée. La distribution nécessite une réécriture.

> La plupart des agents sont synonymes: un agent produit, un agent consomme, une personne utilise, une personne utilise, une personne utilise, une personne utilise, une personne utilise, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée ou une personne utilisée, une personne utilisée, une personne utilisée, une personne utilisée ou une personne utilisée, une personne utilisée, une personne utilisée ou une personne utilisée, une personne utilisée ou une autre.

Autogénération v0.4: le modèle acteur. Chaque agent est un acteur avec une boîte de réception privée. Les messages sont la seule interaction. Le temps d'exécution découple la livraison de la manipulation. Les défaillances isolent à un acteur. La concurrence est native. La distribution est juste un transport différent.

> Autogénération v0.4 Réponse:Acteur 模型── chaque agent est un acteur avec une boîte de réception privée── nouvelle est le seul moyen de communication── opérationnel sera livré avec une compréhension── échec isolé à un acteur──并发是原生── distribuée est simplement un moyen de transmission différent──

> **【中文解读】**AutoGen v0.4  adoption Acteur  modèle chaque agent est un acteur indépendant, par le biais de la transmission de messages communication. Ceci est différent du modèle graphique de LangGraph ou du modèle de rôle de CrewAI.

> **【拓展：AutoGen 的演进】**AutoGen développé par Microsoft Research Institute, v0.4 (2025) est une nouvelle construction majeure. De la version 0.3 du modèle de dialogue à l'Actor Model, l'inspiration vient du modèle de développement d'Erlang/Akka.

>  **【前置】**Il faut d'abord comprendre:Phase 14·01(Agent Loop) et Phase 14·12 ((Anthropic Workflow Patterns) 本节是这些模式在"并发场景"下延伸──还需要"Actor 模型"的基本概念如果不知道Erlang/Akka是什么,先去补一节分布式系统课──本节硬核在"异步消息传递"而不是"LLM 调用"──

## Le concept de base.

### Actors

Un acteur a:

> Un acteur a:

- Un État privé (ne jamais touché directement de l'extérieur).
  Le gouvernement est un État privé.
- Une boîte de réception (ligne de message).
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Un gestionnaire:`receive(message) -> effects`où les effets peuvent être "répondez", "envoyez à un autre acteur", "spam un nouvel acteur", "actualiser l'état", "arrêter soi-même".
  Le traitement:`receive(message) -> effects`, l'effet peut être "répéter""",envoyer à d'autres acteurs"",créer un nouvel acteur"",actualiser l'état""",arrêter soi-même"

Deux acteurs ne peuvent pas partager leur mémoire, ils ne peuvent envoyer que des messages.

>  **【类比】**Actor 模型像办公室里互相见的同事: chacun a son propre lieu de travail (privé état) et sa propre boîte de réception (facile de réception)  You want to let your colleague help, can't go directly over his place (facile de réception), only can send mail (facile de réception), only can send mail (facile de réception)  You want to let your colleague help (facile de réception)  You want to let your colleague help (facile de réception)  You want to let your colleague help (facile de réception)  You want to let your colleague help (facile de réception)  You want to let your colleague help (facile de réception)  You want to let your colleague help (facile de réception)  You want to get your colleague help (facile de réception)  You want to get your colleague help (facile de réception)  You want to send another person (faillessly)  You want to send another person (faillessly)  You want to send another person (faillessly)  You want to send another person (faillessly)  You want to send another person (failled)  You want to another person (failled)  You want to another person (failled)  You want to be so so that he can'd to be so so so so so so so so so so so so so so that he can be so that he can be so that he can be so that he can be so that he can be so that he can be so that he can be so that he can be so so that he can be so that he can be so that he can be so so that he can be so so that he can be so that he can be so so that he can be so that he can be so that he can be so so that he can be so that he can be so that he can be so that he can be so so that he can be so that he can be so that he can be so that he can be so so that he can be so that he can be so that he can be so that he can be so that he can be so that he can be**关键**Une maladie de collègue ne touche pas les autres.

> Les deux acteurs ne peuvent pas partager leur histoire.

### Trois couches d'API dans AutoGen v0.4
### Trois couches d'API

AutoGen v0.4 divise sa surface en trois:

1. **Core.**Cadre d'acteurs de bas niveau. `AgentRuntime`- Je suis là .`Agent`- Je suis là .`Message`- Je suis là .`Topic`Échange de messages asynchronisés, basé sur des événements.
   Le mot grec traduit par " le mot grec "**Core。**Le cadre de l'acteur de base`AgentRuntime`- Je suis là.`Agent`- Je suis là.`Message`- Je suis là.`Topic`                                                                                                                                                                                                                                                              
2. **AgentChat.**API de haut niveau axée sur les tâches (renversement de ConversableAgent de v0.2). `AssistantAgent`- Je suis là .`UserProxyAgent`- Je suis là .`RoundRobinGroupChat`- Je suis là .`SelectorGroupChat`- Je suis désolé .
   Le mot grec traduit par " le mot grec "**AgentChat。**任务驱动的高级 API(替代 v0.2 的可转换Agent)`AssistantAgent`- Je suis là.`UserProxyAgent`- Je suis là.`RoundRobinGroupChat`- Je suis là.`SelectorGroupChat`Il y a une autre.
3. **Extensions.**Intégrations  OpenAI, Anthropic, Azure, outils, mémoire.
   Le mot grec traduit par " le mot grec "**Extensions。**Il est également un des principaux acteurs de la technologie.

### Pourquoi la déconnexion est importante

Dans le modèle v0.2, appel `agent_a.chat(agent_b)`Il bloque synchronement agent_a jusqu'à ce que l'agent_b revienne.`send(agent_b, msg)`Il met le message dans la boîte de réception de l'agent_b et le retour.

> Dans la version 0.2, il est utilisé.`agent_a.chat(agent_b)`Dans la version 0.4, le système de contrôle de l'action est de retour.`send(agent_b, msg)`La réponse est fournie par le courrier officiel.

- **Fault isolation.**L'agent B s'écrase pas l'agent A  le temps d'exécution capture l'échec dans le gestionnaire de B et décide de quoi faire (enregistrement, réessayer, lettre morte).
  Le mot grec traduit par " le mot grec "**故障隔离。**L'agent B ne s'effondre pas entraînant l'agent A s'effondrer dans le traitement de B et décider de quoi faire.
- **Natural concurrency.**Beaucoup de messages en vol à la fois; les acteurs traitent leur boîte de réception en même temps.
  Le mot grec traduit par " le mot grec "**天然并发。**Les messages sont transmis en même temps; l'acteur ne les traite pas.
- **Distribution-ready.**La boîte de réception + transport est la même abstraction que si l'acteur est en cours de traitement ou sur un autre hôte.
  Le mot grec traduit par " le mot grec "**分布式就绪。**Le récepteur + le transfert est le même abstrait, que l'acteur soit dans le processus ou sur l'autre machine.

> ️ **【易错点】**Avec l'acteur, mais j'ai oublié que le message doit être séquencé.**后果**Le processus de production est distribué à plusieurs occasions et se déroule en fonction de l'objet.**一行修复**Toutes les informations doivent être définies avec un schéma pydantic/dataclass/JSON, interdit de transmettre des lambda, des fichiers, des connexions à la base de données, etc.

### Topologies

- **RoundRobinGroupChat.**Les agents se tournent en rotation fixe.
  Le mot grec traduit par " le mot grec "**RoundRobinGroupChat。**Agents à la suite de la rotation fixe.
- **SelectorGroupChat.**Un agent sélecteur choisit qui va suivre en fonction du contexte de la conversation.
  Le mot grec traduit par " le mot grec "**SelectorGroupChat。**选择器 Agent 根据对话上下文选择下一个发言人──
- **Magentic-One.**Une équipe multi-agents de référence pour la navigation sur le Web, l'exécution du code, la gestion de fichiers.
  Le mot grec traduit par " le mot grec "**Magentic-One。**Utilisé pour la navigation en ligne, l'exécution du code, le traitement des fichiers, la référence à l'agent  équipe   sur la base de l'agent Chat  construction 

### Observabilité

Le support OpenTelemetry est intégré. Chaque message émet une durée; les appels à l'outil sont portés `gen_ai.*`Les caractéristiques de l'OTel GenAI sont les mêmes que celles des conventions sémantiques OTel GenAI de 2026 (leçon 23).

> OpenTelemetry 支持内置──每条消息发发出一个跨度;工具调用携带 `gen_ai.*`属性, conforme à la loi de 2026 语义约定 (第 23 课) ⋅

### Statut: mode de maintenance

Début 2026: AutoGen v0.7.x est stable pour la recherche et le prototypage. Microsoft a déplacé le développement actif vers le Microsoft Agent Framework, le successeur de production (preview publique 1 octobre 2025; 1.0 GA a été ciblé pour la fin du 1er trimestre 2026).

```figure
actor-mailbox
```

> 🤔 **【困惑】**Q: AutoGen est entré dans le mode de maintenance, je dois encore apprendre ?**别在生产上选 AutoGen** raisons: 1) Microsoft a déménagé vers Microsoft Agent Framework (MAF), AutoGen n'a plus de nouvelles caractéristiques; 2) Actor 模型 itself is个**经久不衰的分布式设计思想**(de l'article Hewitt de 1973, comparable à un LLM de 50 ans), comprendre qu'il est utile de vous évaluer MAF, Erlang, Akka, Ray, et d'utiliser AutoGen comme " matériel ", MAF ou LangGraph comme " outil de production "

> Début 2026: AutoGen v0.7.x dans le domaine de la recherche et du développement du modèle original. Microsoft est en train de se lancer dans le développement actif du Microsoft Agent Framework.

## Construisez-le en main

`code/main.py`met en œuvre un runtime d'acteur stdlib:

> `code/main.py`Utilisation des critères réalisés par Actor 运行时:

- `Message` chargement utile avec `sender`- Je suis là .`recipient`- Je suis là .`topic`- Je suis là .`body`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`Message`带 `sender`- Je suis là.`recipient`- Je suis là.`topic`- Je suis là.`body`Le type de charge
- `Actor` abstrait avec `receive(message, runtime)`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`Actor`带 `receive(message, runtime)`Le genre de l'abstraction.
- `Runtime` boucle d'événement avec une file d'attente partagée, livraison, isolement de défaillance.
  Le mot grec traduit par " le mot grec "`Runtime`带共享队列、投递、故障隔离的事件循环──
- Une démo de deux acteurs:`ReviewerAgent`code de révision, `ChecklistAgent`Ils échangent des messages jusqu'à un consensus.
  Deux acteurs:`ReviewerAgent`审查代码,`ChecklistAgent`运行检查清单; elles échangent des informations jusqu'à ce qu'une entente soit conclue.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre la livraison du message, un échec simulé chez un acteur qui ne s'écrase pas avec l'autre, et la convergence sur un verdict partagé.

> Le fait qu'un acteur ait subi une défaillance ne conduira pas à un autre effondrement, ainsi qu'à la réception de décisions de partage.

## Utilisez-le avec le cadre de réalisation

- **AutoGen v0.4/v0.7**(maintenance)  stable pour la recherche, la prototypage, les modèles multi-agents.
  Le mot grec traduit par " le mot grec "**AutoGen v0.4/v0.7**(维护中) 研究、原型、多 Agent 模式稳定──
- **Microsoft Agent Framework**(preview publique)  le chemin à suivre; les mêmes idées de modèle d'acteur dans une API renouvelée.
  Le mot grec traduit par " le mot grec "**Microsoft Agent Framework**(public préview) 前进方向; dans le cadre de l'API mise à jour, le même acteur 模型理念――
- **Microsoft Agent Framework** le successeur de la production (preview publique Octobre 2025); les mêmes idées de modèle d'acteur dans une API mise à jour.
- **LangGraph swarm topology**(Léction 13)  Des modèles similaires par le biais de remises d'outils partagés.
  Le mot grec traduit par " le mot grec "**LangGraph 群体拓扑**(第 13 课)                                                                                                                                                                                                                                                            
- **Custom actor runtime** lorsque vous avez besoin d'un transport spécifique (NATS, RabbitMQ, gRPC).
  Le mot grec traduit par " le mot grec "**自定义 Actor 运行时** lorsque vous avez besoin de spécifier le transfert  NATS  RabbitMQ  gRPC) 时

## Envoyez-le . Produit .

`outputs/skill-actor-runtime.md`génère un temps de fonctionnement minimal des acteurs plus un modèle d'équipe (RoundRobin ou Selector) pour une tâche multi-agent donnée.

> `outputs/skill-actor-runtime.md`Pour déterminer plus d'agent  tâche de générer le plus petit acteur 运行时加团队模板(RoundRobin或 Selector) ⋅

## Les exercices

1. Ajoutez une file d'attente: quand un gestionnaire soulève, gardez le message défaillant pour inspection humaine.
   Suivant: Le traitement de l'information est effectué par un processeur de données.
2. Mise en œuvre `SelectorGroupChat`: un acteur sélecteur choisit qui traite le message suivant en fonction de l'état de conversation.
   Le récit de la prophétie`SelectorGroupChat`: choix de l'acteur selon le dialogue état
3. Ajouter le transport distribué: échanger la file d'attente en cours de processus pour un serveur JSON-over-HTTP afin que les acteurs puissent exécuter des processus distincts.
   Le serveur JSON-over-HTTP est remplacé par le serveur Actor, qui peut fonctionner dans un processus indépendant.
4. Transférez une durée d' OTel par message (ou un stand-in sans opération).`gen_ai.agent.name`- Je suis là .`gen_ai.operation.name`Pour la leçon 23.
   Pour chaque message connecté OTel span (ou non-op 替代)`gen_ai.agent.name`- Je suis là.`gen_ai.operation.name`Il y a une autre.
5. Lisez le post d'architecture d'AutoGen v0.4.`autogen_core`Qu'est-ce que vous avez omis qui compte dans la production ?
   Le jeu est porté à la réalité.`autogen_core`Qu'est-ce que tu as oublié de la production ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## Encore une lecture

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) le poste de redessin
  Le projet de loi de la société civile a été modifié en 2004 par le gouvernement de la République de Chine.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Alternative en forme de graphe
  Le langage de la carte est le langage de la carte.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) couvre AutoGen émet par défaut
  Le code de la téléphonie mobile est un code de la téléphonie mobile.
