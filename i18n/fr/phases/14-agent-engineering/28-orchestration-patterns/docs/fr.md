# Modèles d'orchestration: superviseur, groupe, hiérarchique.

> Quatre modèles d'orchestration se reproduisent dans les cadres 2026: supervisor-worker, swarm / peer-to-peer, hiérarchique, débat.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**學本節前 請先掌握:Phase 14·01 Agent Loop)  Single Agent 基础;Phase 14·12 Workflow Patterns) Anthropic's 5 种工作流模式;Phase 14·25 Multi-Agent Debate) 多 Agent 协作基础。**重要原则**: d'abord avec un seul agent + un seul flux de travail, pas assez de temps pour recommencer à travailler avec un autre agent

## Objectifs d'apprentissage

- Nombrez les quatre modèles d'orchestration récurrents et le moment où chacun s'adapte.
- Décrivez la recommandation LangChain 2026: supervision basée sur des appels outils contre des bibliothèques de superviseurs.
- Expliquez la règle de "construire le bon système" d'Anthropic et comment elle empêche le choix de la topologie.
- Mettre en œuvre les quatre en stdlib contre un LLM écrit commun.

## Le problème , l' introduction du problème

Les équipes cherchent "multi-agent" avant de l'avoir besoin. Quatre modèles se reproduisent dans les cadres; une fois que vous pouvez les nommer, vous pouvez choisir le bon  ou sauter la topologie entièrement.

> L'équipe utilise " plusieurs agents " quand ce n'est pas nécessaire. Quatre modèles apparaissent à plusieurs reprises dans le cadre; une fois que vous pouvez les nommer, vous pouvez choisir le bon ou le saut complet.


> **【中文解读】**Le modèle de répartition et de coordination des tâches dans le système d'agents multiples est défini en quatre modes: 1) l'ordre des tâches entre les agents; 2) la mise en œuvre de plusieurs agents et le traitement de différentes tâches; 3) le niveau de gestion de l'agent; 4) la mise en œuvre d'une coopération égale entre les agents.

>  **【类比】**4 种编排模式 = 4 种公司组织:**Supervisor-Worker**= 老板分活给员工 (la plupart des employés sont des employés de la société);**Swarm/P2P**= 同事相互协作(适合讨论类任务,AutoGen GroupChat);(3) **Hierarchical**= 多层老板(CEO→总监→员工,超复杂任务);(4) **Debate**= 委员会投票 (→ Liste des tâches de contrôle des élections)

> ️ **【易错点】**编排选错的 3 个坑:**简单任务用多 Agent**Un seul agent + 5 工具能解决 80% 需求,过早使用监督反而增加复杂度;Anthropic 明确建议"先简单再拓"──(2) **Supervisor 成瓶颈** toutes les tâches sont passées par le superviseur 转发,单点延迟 + 单点失败;让工人间直接通信(仅必要时报监督员)**没设 worker 超时**l'ouvrier lent 卡住整个流程; chaque ouvrier 调用 doit fixer un délai,超时返回降级结果──

> **{【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】}**L'agent 编排是2026年生产 Agent 系统的核心挑战――Anthropic's模式分类(Prompt Chaining、Routing、Parallélisation、Orchestrator-Workers) est devenu un standard――En application réelle, la plupart des systèmes combinent plusieurs types de modes, tels que les demandes de mode par le système client, réutilisant des modèles de couches séparées pour les distribuer à un agent spécialisé――LangGraph's state diagram est un outil de réorganisation des flux principaux――
## Le concept de base.

### Travailleur-surveillant

- Un programme de gestion de la gestion des risques est envoyé à des agents spécialisés.
- Il décide: retourner à lui-même, remettre à un spécialiste, mettre fin.
- Les spécialistes ne parlent pas entre eux; tout le routage passe par le superviseur.

Cadres: LangGraph `create_supervisor`, les ouvriers de l'orchestre anthropologique, le processus hiérarchique de l'équipage.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

**2026 LangChain recommendation:**faire la surveillance par des appels directs aux outils plutôt que `create_supervisor`- vous décidez exactement ce que chaque spécialiste voit.

> **2026 年 LangChain 建议：**通过直接工具调用而不是 `create_supervisor`Pour réaliser le contrôle, vous pouvez déterminer exactement ce que chaque spécialiste voit.

### Les groupes de personnes

- Les agents se détachent directement sur une surface d'outils partagée.
- Pas de routeur central.
- Réduction de la latence par rapport à celle du superviseur (moins de sauts).
- Plus difficile à raisonner sur (pas de point de contrôle unique).

Cadres: topologie de swarm LangGraph, délivrance SDK OpenAI Agents (lorsque tous les agents peuvent délivrer à tous les autres).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### La hiérarchie

- Superviseurs gérant sous-superviseurs gérant les travailleurs.
- Implémenté en tant que sous-graphes encastrés dans LangGraph; équipages encastrés dans CrewAI.
- Équelles à des populations d'agents de grande taille au coût de la complexité opérationnelle.

Lorsque vous en avez besoin: lorsque le budget contextuel d'un seul superviseur ne peut contenir des descriptions de tous les spécialistes.

> Quelques minutes plus tard, le gouvernement a décidé de mettre en place un programme de formation pour les jeunes.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Débat

- Propositions parallèles + critique croisée itérative (leçon 25).
- Pas vraiment orchestration  plus de vérification  mais apparaît comme un choix de topologie dans les cadres.

### Les équipages autonomes et les flux déterministes

CrewAI forme deux modes de déploiement:

- **Flow**pour l'automatisation déterministe basée sur des événements (point de départ recommandé pour la production).
- **Crew**pour une collaboration autonome fondée sur les rôles.

Ceci est orthogonal aux quatre modèles ci-dessus mais correspond à la topologie: Flow est généralement supervisor ou hiérarchique; Crew est généralement supervisor avec un routeur LLM.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Les conseils de l'anthropique

" Le succès dans le domaine de la maîtrise de la loi ne consiste pas à construire le système le plus sophistiqué, mais à construire le système approprié pour vos besoins. "

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

Règlement de décision:

1. Un agent unique + des modèles de flux de travail (leçon 12)  commencent ici.
2. - le personnel de supervision  lorsque vous avez 2 à 4 spécialistes.
3. Swarm  quand la latence compte plus que la clarté du raisonnement.
4. Hiérarchique  seulement lorsque le budget de l'autorité de surveillance échoue.
5. Débat lorsque l'exactitude importe plus que le coût.

### Où ce modèle va mal

- **Topology-first thinking.**"Nous avons besoin de multi-agent" avant d'identifier le problème que le multi-agent résolve.
- **Bouncing handoffs in swarm.**A -> B -> A -> B. Utilisez des compteurs de sauterelles.
- **Fake hierarchy.**Trois couches parce que "entreprise"; deux équipes réelles.

> **拓扑优先思维。**Avant de déterminer ce qu'il faut faire, on dit: "Nous avons besoin de plus d'agents".
> **群体中弹跳交接。**A -> B -> A -> B。 Utilisation de la calculatrice de saut
> **虚假层级。**Parce que "l'entreprise" est en trois niveaux; en réalité, il n'y a que deux équipes.

## Construisez-le et mettez-le en œuvre.
```figure
orchestration-pattern
```

## Faites-le

`code/main.py`met en œuvre les quatre modèles dans stdlib contre un LLM écrit:

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- `Supervisor`- Le routeur central.
- `Swarm` Peer-to-peer avec des remises directes.
- `Hierarchical` les superviseurs des superviseurs.
- `Debate` propositions parallèles + critique.

Chaque modèle gère la même tâche à trois intentions (revers / bug / vente).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- Je vais le faire.

```
python3 code/main.py
```

Résultats: trace par modèle + nombre d'options. Supervisor est le plus propre; swarm est le plus court; hiérarchique est le plus profond; débat est le plus coûteux.

> 输出: chaque mode de suivi + 操作数──监督者最清晰;群体最短;层级最深;辩论最昂贵──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Utilisez-le avec le cadre de réalisation

- **LangGraph**pour les sous-graphes supervisants et hiérarchiques (subgraphes en nid).
- **OpenAI Agents SDK**pour les remises en tant qu'outils (en forme de superviseur).
- **CrewAI Flow**pour la détermination de la production.
- **Custom**Pour le débat ou quand vous voulez le contrôle exact.

## Envoyez-le . Produit .

`outputs/skill-orchestration-picker.md`choisit une topologie et la met en œuvre.

> `outputs/skill-orchestration-picker.md`选择一个拓并实现它──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Les exercices

1. Convertir un superviseur en essaim en enlevant le routeur.
  Le mot "exercer" est traduit par "exercer".
2. Ajoutez un compteur de saut au swarm: rejet après 3 remises.
  Le mot "exercer" est traduit par "exercer".
3. Construire un système hiérarchique à deux niveaux pour un domaine spécialisé de 12 spécialistes.
  Le mot "exercer" est traduit par "exercer".
4. Profiliser les quatre modèles sur une charge de travail en forme de production.
  Le mot "exercer" est traduit par "exercer".
5. Lisez le post " Construire des agents efficaces " de Anthropic.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Supervisor-worker | "Router + specialists" | Central LLM dispatches to specialists; they don't talk to each other |  |
| Swarm | "Peer-to-peer" | Direct handoffs via shared tools; no central router |  |
| Hierarchical | "Supervisors of supervisors" | Nested subgraphs for large populations |  |
| Debate | "Proposer + critique" | Parallel proposers, cross-critique (Lesson 25) |  |
| Tool-call-based supervision | "Supervisor without a library" | Implement supervisor as direct tool calls for context control |  |
| Crew | "Autonomous team" | CrewAI's role-based collaboration mode |  |
| Flow | "Deterministic workflow" | CrewAI's event-driven production mode |  |

## Encore une lecture

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) cinq modèles + agent vs flux de travail
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) superviseur, essaim, hiérarchique
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [CrewAI docs](https://docs.crewai.com/en/introduction) équipage contre flux
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) Modèle de débat
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
