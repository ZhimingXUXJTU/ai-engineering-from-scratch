# Les délivrances et les routines  Orchestration sans État 编排 交接 例程 状态

> Swarm d'OpenAI (octobre 2024) a distillé l'orchestration multi-agent à deux primitives: **routines**(instructions + outils comme un prompt système) et **handoffs**(un outil qui renvoie un autre agent). Aucune machine d'État, aucune branche DSL  les itinéraires LLM en appelant le bon outil de remise. Le SDK OpenAI Agents (mars 2025) est le successeur de la production. L'équipe de la série est la référence conceptuelle la plus pure. Le modèle est viral parce que la surface de l'API est à peu près "agent = prompt + outils; remise = agent de retour de fonction. " Limite: sans état, donc la mémoire est le problème de l'appelant.

> **【中文解读】**Ce chapitre présente les processus et procédures de communication et de contrôle des tâches de transmission entre les agents.

> **【拓展：handoffs and routines→具体应用】**交接(Handoffs) est le concept central de OpenAI Agents SDKAgent A va transférer le contrôle à l'Agent B。 Key Design Decision:(1) 上下文传递B 收到多少 A 的历史?(2) 恢复机制B 完成后控制权回到 A 还是交给C?(3) 超时处理B 如果卡住怎么办?


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les autres, il est nécessaire de se préparer à la préparation de la première phase de la phase de formation.
>  **【类比】**Handoff = "客服转接"──用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm 的天才之处:handoff 就是一个普通工具调用(回复代理),LLM 自动路由──无状态机、无 DSL,几百行代码搞定──OpenAI Agents SDK 是生产版本──

## ♪ Problème ♪ Introduction du problème ♪

Chaque framework multi-agents veut que vous appreniez son DSL: les nœuds et les bords de LangGraph, les équipes et les tâches CrewAI, AutoGen GroupChat et les gestionnaires.

> Chaque cadre d'agents veut vous faire apprendre le DSL:Notes et bords de la Langgraph,l'équipe et les tâches de l'équipe d'AutoGen, le GroupeChat et le gestionnaire.

Le verrouillage DSL est la taxe de cadre multi-agents. Chaque DSL a ses propres concepts, ses propres outils de débogage, sa propre communauté. Une fois que vous vous engagez, la migration est coûteuse.

> DSL 锁定是多代理 框架税──每个 DSL a son propre concept、 son propre outil de révision、 sa propre communauté── once you commit,迁移昂贵──Swarm 的注: complètement sauter sur DSL, utiliser les outils existants du modèle调用──

L'équipe de communication est la machine d'État implicite dans les instructions du système des agents.

> Swarm 推向相反的方向: utiliser les capacités de référencement des outils existants du modèle.

La compréhension est profonde: vous n'avez pas besoin d'une DSL d'orchestration parce que les LLM sont déjà des orchestrateurs. Chaque appel de LLM décide de ce qu'il faut faire ensuite en fonction du contexte.

> 洞察深:你不需要编排 DSL,因为LLM 已经是编排器──每次LLM 调用根据上下文决定下一步做什么──交接只是将该决策暴露为模型可调用工具──

## Concept Le concept central

### Deux primitifs

**Routine.**Un système de commande qui définit le rôle d'un agent et les outils disponibles. Pensez à cela comme un ensemble de instructions à portée de main: "vous êtes un agent de triage; si l'utilisateur demande des remboursements, remettez-les à l'agent de remboursement".

> **例程。**定义 Agent 角色和可用工具的系统提示──把它想象成一组范围化的指令:"tu es un agent de diagnostic; si un utilisateur demande un remboursement, se connectez à un agent de remboursement──"

**Handoff.**Un outil que l'agent peut appeler qui renvoie un nouvel objet d'agent.

> **交接。**L'agent peut être utilisé pour le retour d'un nouvel agent à un objet.

C'est l'abstraction dans son ensemble.

> C'est tout le résumé.

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

L'interrogatoire du système de l'agent de triage lui permet de choisir la bonne remise en fonction du message de l'utilisateur.

> Le système de l'agent de diagnostic le fait fonctionner selon les informations de l'utilisateur choisir correctement le contact.

Il s'agit d'un mouvement élégant: réutiliser l'infrastructure existante de l'appel à l'outil du modèle pour l'orchestration. Pas de nouveau DSL, pas d'éditeur de graphiques, pas de machine d'état. Le modèle sait déjà comment choisir le bon outil; les remises sont juste des outils qui retournent les agents.

> C'est une initiative de beauté: réutiliser les outils existants du modèle pour le montage de l'infrastructure. Pas de nouveaux DSL, pas de rédacteurs de graphiques, pas de machines d'état. Le modèle sait déjà comment choisir le bon outil.

### Pourquoi il est viral

- **Small API.**Deux concepts à apprendre.
  Le mot grec traduit par " le mot grec "**小型 API。**Il faut apprendre deux concepts.
- **Uses what the model already does.**L'appel à l'outil est déjà de qualité de production entre les fournisseurs.
  Le mot grec traduit par " le mot grec "**使用模型已有的能力。**Les outils de production sont déjà utilisés par les fournisseurs.
- **No state-machine burden.**Vous ne décrivez pas le graphique; les instructions des agents décrivent à qui ils remettent.
  Le mot grec traduit par " le mot grec "**无状态机负担。**Vous ne décrivez pas le tableau; les conseils de l'agent décrivent ceux qui les ont transmis à qui.

### Le commerce des apatrides

Le cadre conserve une histoire de message pendant une course, mais il ne persiste rien. mémoire, continuité, tâches de longue durée  tout le problème de l'appelant.

> Le cadre de fonctionnement est un système de gestion de l'information, mais il ne peut rien maintenir.

La conception sans état est intentionnelle: elle rend le cadre trivialement redémarrable, évolutif horizontalement et débogable (chaque course est indépendante).

> 无状态设计是有意的: il rend le cadre facilement redémarrable, étendu et modifiable à chaque fois que fonctionne indépendamment.

En production (OpenAI Agents SDK, mars 2025) c'était l'une des principales choses qui a changé: le SDK ajoute la gestion de session intégrée, les barreaux de garde et le suivi tout en maintenant la remise à la main primitive.

> Dans le cadre de la production environnement, le SDK OpenAI Agents est un des principaux changements: le SDK a ajouté la gestion de session intégrée, la protection et le suivi, tout en conservant le lien avec le langage original.

### Lorsque les épaules/les manches s'adaptent

- **Triage patterns.**L'agent de première ligne envoie l'utilisateur à un spécialiste.
  Le mot grec traduit par " le mot grec "**分诊模式。**L'agent de première ligne va utiliser le réseau de l'utilisateur pour le spécialiste.
- **Skill-based handoffs.**"Si la tâche a besoin de code, appelez le codeur; si elle a besoin de recherche, appelez le chercheur".
  Le mot grec traduit par " le mot grec "**基于技能的交接。**"Si les tâches doivent être codées, utilisez le codeur; si vous avez besoin de rechercher, utilisez le chercheur"".
- **Short, bounded conversations.**Assistance à la clientèle, FAQ à billet, flux de travail simples.
  Le mot grec traduit par " le mot grec "**短、有界对话。**客户支持、FAQ到工单、简单工作流──

### Quand les éclats luttent

- **Long sessions with shared memory.**Les remises de mains ont réinitialisé l'état de conversation à l'historique de l'interrogatoire du nouvel agent.
  Le mot grec traduit par " le mot grec "**需要共享内存的长会话。**交接将对话状态重置为新代理的提示加历史――没有调用者管理的内存就没有跨代理的持久状态――
- **Parallel execution.**Le transfert est un à la fois  les commutateurs d'agent actif.
  Le mot grec traduit par " le mot grec "**并行执行。**交接是逐一的活动 交换――并行性需要调用者编排多个群众 运行――
- **Audit and replay.**Les courses sans statut sont difficiles à reproduire exactement; le choix de l'offre du LLM n'est pas déterministe.
  Le mot grec traduit par " le mot grec "**审计和回放。**无状态运行难以精确回放; La sélection de connexions de LLM n'est pas certaine.

### Le programme de développement durable OpenAI Agents (mars 2025)

Le successeur de la production ajoute:

> Il y a eu des réactions de violence.

- **Session state.**Un fil persistant à travers les courses.
  Le mot grec traduit par " le mot grec "**会话状态。**跨运行的持久线程──
- **Guardrails.**Les crochets de validation de l'entrée/sortie.
  Le mot grec traduit par " le mot grec "**防护栏。**输入/输出验证子──
- **Tracing.**Chaque appel et remise d'outils sont enregistrés.
  Le mot grec traduit par " le mot grec "**追踪。**Chaque utilisation et communication sont enregistrées.
- **Handoff filters.**Contrôlez le contexte transféré sur le transfert.
  Le mot grec traduit par " le mot grec "**交接过滤器。**控制交接时传输什么上下文──

Le primitif de la remise en main survit; l'ergonomie de la production s'y ajoute.

> 交接原语存活下来; produire un corps humain autour de lui

C'est la progression standard pour les abstractions virales: les navires primitifs simples en premier (Swarm), la production concerne la couche supérieure (Agents SDK).

> C'est le standard progression du virus: premier lancement de simples langues originales, production de concentrations sur son niveau supérieur, et le développement de l'économie de marché.

### Swarm vs GroupeChat

Les deux utilisent un routage basé sur le LLM, mais ils diffèrent en**who picks next**- Le numéro de la liste:

> Les deux utilisent des voies de LLM, mais dans**谁选择下一个**上不同:

- GroupeChat: un sélecteur (fonction ou LLM) choisit le prochain orateur de l'extérieur.
  Le groupe de discussion est le premier groupe de discussion.
- L'agent actuel choisit son successeur en appelant un outil de transfert.
  Le groupe de travail est un groupe de travail de formation.

Swarm est "l'agent décide ce qui vient ensuite"; GroupChat est "le gestionnaire décide ce qui vient ensuite".`GroupChatManager`- Je suis désolé .

> Swarm est "l'agent décide le prochain pas";GroupChat est "l'administrateur décide le prochain pas"。L'action de la population est basée sur l'activité de l'agent;GroupChat est basé sur l'utilisation des outils de l'agent.`GroupChatManager`Dans le centre.

Implication pratique: Swarm est plus facile à débogager (suivre les appels d'outils de l'agent actif) mais plus difficile à restreindre (tout agent peut le remettre n'importe où). GroupChat est l'inverse: facile à restreindre (la fonction sélecteur est un endroit pour ajouter des règles), plus difficile à débogager (la logique du sélecteur peut être opaque).

> 实际影响:Swarm 更容易调试(跟踪活动 调用的工具) mais更难约束(Quelque agent peut être connecté n'importe où) ――GroupChat 相反:容易约束(

## Construisez-le et mettez-le en œuvre.
```figure
sw-handoff-routing
```

## Faites-le

`code/main.py`Il implémentera Swarm à partir de zéro: une classe de données d'agent, un mécanisme de remise (outil retourne agent) et une boucle de fonctionnement qui détecte les commutateurs d'agent.

> `code/main.py`De la tête à la réalisation de l'échantillon: le cycle de fonctionnement de l'agent (en anglais: agent, agent, agent, agent) et de l'agent (en anglais: agent, agent, agent)

Démo: un agent de triage effectue des itinéraires pour rembourser, vendre ou soutenir des spécialistes. Chaque spécialiste dispose de ses propres outils.

> 演示:分诊 路由到退款、销售或支持专家──每个专家都有自己的工具──运行循环打印每次交接──

Je vais courir .

```
python3 code/main.py
```

## Utilisez-le avec le cadre de réalisation

`outputs/skill-handoff-designer.md`Il est possible de déterminer les types d'interventions et les types de dépôt.

> `outputs/skill-handoff-designer.md`Pour déterminer les tâches de conception de liaison: quels agents existent, quels sont les liaisons à utiliser, quels sont les messages à transmettre.

## Envoyez-le . Produit .

Liste de contrôle:

> 检查清单:

- **Handoff logging.**Chaque remise écrit un événement avec un instant de l'agent à l'agent, un instant de contexte.
  Le mot grec traduit par " le mot grec "**交接日志。**Chaque contact est inscrit dans un événement de suivi, comprenant des agents à des agents.
- **Context transfer rules.**Décidez de ce qui se déplace sur le remise: l'historique complet (chère), les derniers N messages, ou un résumé.
  Le mot grec traduit par " le mot grec "**上下文传输规则。**Décider de communiquer le temps de transmission: complet historique
- **Guardrail on handoff.**Une remise à un spécialiste avec des permissions d'outil différentes doit être authentifiée  sinon l'injection rapide peut forcer des remises non désirées.
  Le mot grec traduit par " le mot grec "**交接防护栏。**Les experts qui ont des droits sur différents outils doivent être certifiés.
- **Loop detection.**Deux agents qui se détachent est un échec commun; détecter avec une simple vérification de sondage de dernière K.
  Le mot grec traduit par " le mot grec "**循环检测。**Les deux agents sont habituellement défaits; avec un simple test de contrôle de la dernière phase de la phase K.
- **Fallback agent.**Si une cible de remise n'existe pas, retournez à une défaillance sécurisée.
  Le mot grec traduit par " le mot grec "**后备 Agent。**Si le lien n'existe pas, retournez à la valeur par défaut de sécurité.

## Les exercices

1. On court .`code/main.py`Confirmez que l'agent actif du second tour est remboursé.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`,分诊到退款代理;; confirmer la deuxième série d'activités
2. Ajouter une règle de détection de boucle: si les deux mêmes agents ont donné 3 fois de suite, forcer une sortie.
   Règles de contrôle du cycle: si les deux mêmes agents continuent à se connecter 3 fois, ils sont obligés de se retirer.
3. Lisez les documents OpenAI Agents SDK sur les filtres de remise. Implémenter une version " résumer sur remise ": l'agent sortant comprime le contexte en un résumé de balle avant que l'agent entrant ne prenne le relais.
   Le code de gestion de l'information est le code de gestion de l'information.
4. Comparer la remise de Swarm à un sélecteur GroupChatManager.
   Le groupe de discussion est un groupe de discussion.
5. Lisez le livre de cuisine Swarm. Identifiez une décision de conception explicite Swarm prend que le SDK OpenAI Agents a changé ou conservé.
   Le code de conduite de l'entreprise est un code de conduite qui est utilisé pour la mise en œuvre de la stratégie de gestion de la sécurité.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Encore une lecture

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) l'articulation de référence
  Le code de la langue française est le code de la langue française.
- [OpenAI Swarm repo](https://github.com/openai/swarm) mise en œuvre originale, conservée comme référence conceptuelle
  Le projet de loi de l'État de l'Occident sur les droits de l'homme
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) successeur de production avec séances et suivi
  Le programme de développement de l'entreprise est basé sur le programme de développement de l'entreprise.
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) comment les subagents de code Claude utilisent un modèle de remise via `Task`
  En français, le code de Claude est le code de Claude.`Task`Utiliser un modèle similaire
