# Groupe de chat et sélection de conférenciers  groupe de discussion  sélection  émetteur

> L'orchestration de la conversation partagée met N agents dans une conversation; une fonction sélectrice (LLM, round-robin ou personnalisé) choisit qui parle ensuite. C'est l'archétype de la conversation multi-agents émergente  les agents ne connaissent pas leur rôle dans un graphique statique, ils réagissent simplement au pool partagé. AutoGen GroupChat et AG2 GroupChat sont les mises en œuvre de référence: la sémantique de GroupChat d'AutoGen v0.2 a été préservée dans la fourchette AG2; AutoGen v0.4 l'a réécrite comme un modèle d'acteur axé sur les événements. Microsoft a mis AutoGen en mode maintenance en février 2026 et l'a fusionné avec le Kernel sémantique dans le Microsoft Agent Framework (RC février 2026). Le GroupeChat primitif survit dans AG2 et Microsoft Agent Framework  apprendre une fois, l'utiliser partout.

> **【中文解读】**Cette partie présente le groupe de discussion sur le choix de l'agent et la détermination du mécanisme de l'échange.

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多代理 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略:(1) 轮流制按固定顺序发言;(2) 相关性制最相关的代理发言;(3) 仲裁制一个专门协调员决定谁发言──AutoGen's GroupChat Utilise LLM 作为仲裁员──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**學本节前Please first master:Phase 16·04(原语模型) 、AutoGen 基础──群聊 = N 个 Agent 共享一个对话池,发言人选择决定谁说话──
>  **【类比】**群聊发言人选择 = "président de réunion"──轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = 主持人指定──AutoGen GroupChat utilisant LLM lorsque le président 高成本但灵活──2026

## ♪ Problème ♪ Introduction du problème ♪

Les graphiques statiques (LangGraph) sont excellents lorsque le flux de travail est connu. Les vraies conversations ne sont pas statiques: parfois le codeur demande au critique, parfois au chercheur, parfois à l'écrivain. Le codage dur de chaque dépôt possible produit une explosion de bord. Vous voulez * agents réagissant à un pool partagé*, avec une fonction décidant qui parle ensuite.

> 静态图(Langgraph) dans le flux de travail connu lorsqu'il est bon. ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽     ▽     ▽ ▽    ▽                                                                       

Le problème de l'explosion de bord est réel: un système de 5 agents avec toutes les dépositions possibles a 25 bordes dirigées. Ajoutez un sixième agent et vous avez 36.

> Le problème de l'explosion est réel: avec tous les 5 agents possibles de communication, le système a 25 articles, il y a des pages à côté.

C'est exactement ce que fait AutoGen GroupChat.

> C'est exactement ce que fait le Groupe Chat AutoGen.

## Concept Le concept central

### La forme

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Chaque agent voit chaque message, une fonction de sélection est invoquée à chaque tour pour choisir qui parle ensuite.

> Chaque agent voit chaque message. Chaque tour utilise une fonction de sélectionneur pour sélectionner le prochain intervenant.

La capacité de transparence complète est à la fois la force et la faiblesse de GroupChat. La force: tout agent peut réagir à tout ce que quelqu'un dit. La faiblesse: après 20 tours, le contexte de chaque agent est énorme, coûteux et dilué.

> L'avantage est que tout agent peut répondre à tout ce que quelqu'un dit. L'avantage est que 20 tours après chaque agent, chaque agent a un niveau élevé de coût et de rareté.

### Les trois saveurs sélectionnantes

**Round-robin.**Cycle fixe. déterministe. Équelle linéairement en N mais ignore le contexte  un codeur obtient le tour même lorsque le sujet est une revue juridique.

> **轮询。**固定循环──确定性── selon la N 线性扩展但忽略上下文 Même si le sujet est un examen juridique, le codeur peut également obtenir le droit d'expression──

**LLM-selected.**Un appel à un LLM qui lit le pool récent et renvoie le meilleur intervenant suivant. Context-conscient mais lent: à chaque tour ajoute un appel à un LLM. Autogénération par défaut.

> **LLM 选择。**调用 LLM 读取近期池并返回最佳下文发言人──上下文感知但慢: chaque tour augmente une fois LLM 调用──AutoGen 的默认选择──

**Custom.**Une fonction Python avec la logique que vous voulez. Typique: LLM sélectionné avec des règles de retour (par exemple, "donner toujours le vérificateur le tour après le codeur").

> **自定义。**Une fonction Python, utilisant toute logique que vous voulez.

### L'API de l'agent conversiblement

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`Quand un agent termine un tour, le gestionnaire appelle le sélecteur, qui renvoie le prochain agent.

> `GroupChatManager`持有选择器──当代理 完成一轮时,管理者调用选择器,返回下一个代理──循环继续直到终止条件──

La fonction sélecteur est le cœur de GroupChat. Échangez-le, changez le style d'orchestration. sélecteur de rouleau rond = déterministe. sélecteur LLM = adaptif. sélecteur personnalisé = quelles que soient les règles que vous codifiez. Les mêmes primitives, différentes orchestrations.

> La fonction de sélectionneur est au cœur du Groupe Chat. Elle est modifiée, modifie le format de sélectionnement.

### Résolution

Trois modèles communs:

> 3 modes habituels:

- **Max rounds.**Une boucle dure sur les virages totaux.
  Le mot grec traduit par " le mot grec "**最大轮数。**总轮数的硬上限──
- **"TERMINATE" token.**Les agents peuvent envoyer un message de sentinelle; le gestionnaire s'arrête quand il apparaît.
  Le mot grec traduit par " le mot grec "**"TERMINATE" 标记。**L'agent peut envoyer des messages de poste; le gestionnaire s'arrête à son arrivée.
- **Goal-reached check.**Un vérificateur léger passe à chaque tour et arrête la conversation.
  Le mot grec traduit par " le mot grec "**目标达成检查。**Légère qualité de l'épreuve de chaque tour de fonctionnement et de l'achèvement de l'arrêt de la discussion.

### La division AutoGen -> AG2 et la fusion du Microsoft Agent Framework
### Lignée: forcs et fusions

Au début de 2025, Microsoft a commencé une réécriture majeure d'AutoGen (v0.4) autour d'un modèle d'acteur axé sur les événements.

> Au début de 2025, Microsoft a commencé à faire une réécriture majeure de l'AutoGen (v0.4) autour de l'acteur moteur des événements.

La fourchette était nécessaire car la version 0.4 a rompu la compatibilité arrière de manière fondamentale.`GroupChat`- Je suis là .`ConversableAgent`, et `GroupChatManager`L'API est stable, tandis que la version 0.4 introduit de nouvelles primitives basées sur des événements.

> Le split est nécessaire, car la version 0.4 a essentiellement détruit la compatibilité vers l'arrière.`GroupChat`- Je suis là.`ConversableAgent`et `GroupChatManager`L'API est stable, tandis que la version 0.4 introduit de nouveaux événements.

En février 2026, Microsoft a annoncé que AutoGen passerait au mode maintenance, avec le modèle d'acteur axé sur les événements fusionnant dans **Microsoft Agent Framework**Le concept de GroupChat survit dans les deux pistes; les détails de mise en œuvre diffèrent. AG2 est le code préféré en amont pour le code compatible v0.2.

> En février 2026, Microsoft annonce que AutoGen entre dans le mode de maintenance, acteur de l'événement**Microsoft Agent Framework**Le groupe Chat est un concept de communication en deux voies.

Le cours: API surface survit les cadres. Code écrit contre l'API GroupChat d'AutoGen v0.2 en 2024 fonctionne toujours inchangé via AG2 en 2026. Cadres churn; les primitifs (partagé pool + sélecteur) ne le font pas. parier sur les primitifs.

> Apprendre à utiliser les données de l'API en ligne et à les utiliser pour les autres utilisateurs.

### Quand le groupe chat est adapté

- **Emergent conversations.**Vous ne voulez pas pré-cabeler chaque haut-parleur possible.
  Le mot grec traduit par " le mot grec "**涌现对话。**Tu ne veux pas de connexion préalable à chaque possible de l'autre éditeur.
- **Role-mixing tasks.**Le codeur demande au chercheur, le chercheur demande à l'archiviste, l'archiviste demande au codeur de retour.
  Le mot grec traduit par " le mot grec "**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器──流程不是DAG──
- **Exploratory problem-solving.**Pensez à la réunion de la tempête, pas à la ligne d'assemblage.
  Le mot grec traduit par " le mot grec "**探索性问题解决。**Je pense à la "séance de la tempête" plutôt qu'à la "classe de la ligne de décoration".

### Quand il échoue

- **Strict determinism.**Le sélecteur de la licence peut être incohérent, le même prompt, des coups différents, des intervenants différents.
  Le mot grec traduit par " le mot grec "**严格确定性。**LLM 选择器可能不一致──相同提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**Les agents se déposent à qui parle le plus en confiance.
  Le mot grec traduit par " le mot grec "**谄媚级联。**L'agent se soumet à l'orateur le plus confiant.
- **Context bloat.**Chaque agent lit chaque message; après 10 tours, le contexte est énorme.
  Le mot grec traduit par " le mot grec "**上下文膨胀。**Chaque agent 读取每条消息;10 轮后上下文巨大──使用投影(L'enseignement 15) 来限定视图──
- **Hot speakers.**Un agent domine la conversation parce que le sélecteur favorise ses spécialités.
  Le mot grec traduit par " le mot grec "**热发言者。**Un agent principal dirige le dialogue, parce que le sélecteur est orienté vers son expertise.

### Chat de groupe contre superviseur

Les mêmes primitifs, différents par défaut:

> Pour les autres, la valeur de la valeur de l'image est:

- Un agent planifie et d'autres exécutent.
  Le choix de l'agent est le choix de l'agent.
- Chat de groupe: tous les agents sont des pairs; le sélecteur est une fonction sur le pool partagé.
  Tout agent est le même; le sélecteur est la fonction de la pile de partage.

Les deux utilisent les quatre primitives de la leçon 04. Les discussions de groupe par défaut à l'orchestration sélectionnée par le LLM et à l'état partagé complet.

> Les deux utilisent les quatre langues originales de la leçon 04 群聊默认使用LLM 选择的编排和全池共享状态──

Le choix entre le superviseur et le chat de groupe concerne principalement *qui détient le plan*. Superviseur: un agent possède le plan et les délégués.

> Le choix entre le surveillant et le groupe de discussion est principalement celui qui a un plan. Le surveillant: un agent qui a un plan et le commande.

## Construisez-le et mettez-le en œuvre.
```figure
swarm-speaker
```

## Faites-le

`code/main.py`Il est possible de mettre en œuvre un groupechat à partir de zéro dans stdlib.`TERMINATE`Je vous en prie.

> `code/main.py`Il s'agit d'un programme de formation de formation professionnelle qui consiste à fournir des informations et des conseils à des personnes qui souhaitent être éligibles à un programme de formation professionnelle.`TERMINATE`Le signe de la fin.

La démo imprime la transcription de la conversation plus la trace de décision du sélecteur pour les deux variantes.

> 演示 imprimé enregistrement de dialogue ainsi que suivi des choix des deux variables.

## Utilisez-le avec le cadre de réalisation

`outputs/skill-groupchat-selector.md`configure un sélecteur GroupChat pour une tâche donnée  round-robin vs LLM-selected vs custom, et quelles entrées sélecteur (messages récents, spécialités d'agent, compteurs de tour) utiliser.

> `outputs/skill-groupchat-selector.md`Pour déterminer la tâche de configuration GroupeChat  sélectionneur 轮询 vs LLM 选择 vs 自定义, ainsi que l'utilisation de quoi sélectionneur输入(最近消息、Agent 专长、轮次计数)

## Envoyez-le . Produit .

Liste de contrôle:

> 检查清单:

- **Max rounds cap.**Toujours. 10 à 20 pour les tâches typiques.
  Le mot grec traduit par " le mot grec "**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**Tournées de piste par agent; alerte lorsque le déséquilibre dépasse un seuil.
  Le mot grec traduit par " le mot grec "**发言者平衡指标。**Suivre chaque tour de l'agent; quand l'équilibre dépasse la valeur de l'agence de renseignements.
- **Termination token.** `TERMINATE`ou un agent de vérification dédié.
  Le mot grec traduit par " le mot grec "**终止标记。** `TERMINATE`Ou un agent spécialisé en vérification.
- **Projection or scoped memory.**Après ~ 10 messages, envisagez de donner à chaque agent seulement une vue à portée de main pour éviter le gonflement de contexte.
  Le mot grec traduit par " le mot grec "**投影或范围内存。**Après environ 10 nouvelles, il faut considérer que chaque agent ne possède qu'une seule vue pour éviter une inflation de la situation.
- **Selector logging.**Pour les variantes sélectionnées par LLM, enregistrer à la fois l'entrée du sélecteur et son choix.
  Le mot grec traduit par " le mot grec "**选择器日志。**Pour les LLM, l'entrée et la sélection des sélectionneurs sont impossibles.

## Les exercices

1. On court .`code/main.py`Comparer la conversation sous round-robin vs LLM-selectionné.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Comparer les enquêtes et les choix de l'LLM  Dialogue ◊ Dans chaque mode, quel agent est le principal ?
2. Ajoutez une règle de "maximum parle par agent" dans le sélecteur.
   Le code de la rédaction de la lettre de référence est le plus large de tous les articles de référence.
3. Mettre en œuvre une fin d'essai atteinte: arrêter lorsque l'examen est "approuvé".
   Le référendum est un accord de coopération entre les États membres.
4. Lisez les documents stables AutoGen sur GroupChat. Identifiez le sélecteur par défaut utilisé par `GroupChatManager`- Je suis désolé .
   Le groupe de discussion est un groupe de discussion.`GroupChatManager`Utilisation de l'équipe de sélection
5. Lisez le repo AG2 et comparez son v0.2 GroupChat à la version axée sur les événements v0.4.
   Le groupe de discussion a été créé en 2004 pour la première fois en collaboration avec le groupe de discussion de l'année dernière.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Encore une lecture

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) la mise en œuvre de référence
  Le texte de l'article est en anglais.
- [AG2 repo](https://github.com/ag2ai/ag2) communauté AutoGen v0.2 continuation
  Le code de conduite est le code de conduite.
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) le successeur fusionné, RC février 2026
  Le rédacteur en chef de Microsoft Agent Framework 文档  合并后后的继任者,2026 年 2 月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) le successeur fusionné, RC février 2026
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) Récris détails du modèle d'acteur axé sur l'événement
  Le modèle de l'auto génération v0.4  édition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
