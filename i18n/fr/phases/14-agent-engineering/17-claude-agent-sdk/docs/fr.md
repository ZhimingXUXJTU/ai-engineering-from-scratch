# Les subagents et les magasins de séances
# Le harnais comme bibliothèque  Subagents et magasin de séances

> Un harnais que vous pouvez importer: outils intégrés, sous-éléments pour l'isolement de contexte, crochets, propagation des traces W3C, persistance de session. Le SDK Claude Agent est l'exemple de référence  la forme de bibliothèque du harnais Claude Code  et Claude Managed Agents est l'alternative hébergée pour le travail asynchrone à long terme.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Expliquez la différence entre le SDK client anthropic (API brute) et le SDK agent Claude (forme de harnais).
- Décrire les sous-éléments  parallélisation et isolement de contexte  et quand les atteindre.
- Nommer la surface de stockage de session du SDK Python (`append`- Je suis là .`load`- Je suis là .`list_sessions`- Je suis là .`delete`- Je suis là .`list_subkeys`) et le rôle de `--session-mirror`- Je suis désolé .
- Implémenter un harnais stdlib avec des outils intégrés, un débarquement sous-débarquement avec un contexte isolé, des crochets de cycle de vie et un magasin de session.

## Le problème , l' introduction du problème

Une API LLM brute vous donne un tour de retour. Un agent de production a besoin d'exécution des outils, des serveurs MCP, des crochets de cycle de vie, de reproduction sous-jacente, de persistance de session, de propagation des traces. Claude Agent SDK expédie cette forme en tant que bibliothèque  le même harnais que Claude Code utilise, exposé pour les agents personnalisés.

> Le programme de formation en formation professionnelle (API) peut seulement vous donner une fois de retour et de retour de l'utilisation.


> **【中文解读】**Claude Agent SDK est un système d'exploitation de l'agent 官方的 Agent 开发框架──核心特性:(1) 内置工具(文件读写、代码执行等);(2) 子 Agent 支持Agent 可以生成子 Agent 处理子任务;(3) 生命周期子 在 Agent 执行的关键节点插入自定义逻辑──SDK 深度集成 Claude's Extended Thinking 能力──

> **{【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】}**Le SDK Claude Agent est un outil de développement central de l'économie Claude de 2026[6]. Par rapport au SDK OpenAI Agents, il met davantage l'accent sur l'intégration profonde des capacités uniques de Claude, telles que la pensée étendue, l'utilisation de l'ordinateur. Le mode de sous-agent du SDK permet à l'agent de diviser des tâches complexes en sous- tâches, chacune des sous- tâches étant traitée par un sous-agent spécial, similaire à la division des tâches dans un organisme[6].

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) etPhase 14·10(Skill Libraries) Claude Agent SDK a intégré la compétence 系统作为子 Agent的标准模式──如果没有使用Claude Code CLI,强烈建议先使用几天本SDK就是Claude Code的库形式,理解CLI's behavior pattern对学习SDK事半功倍──

## Le concept de base.

### SDK client contre SDK agent

- **Client SDK (`anthropic`).**Tu possèdes la boucle, les outils, l'état.
- **Agent SDK (`claude-agent-sdk`).**Exécution intégrée, connexions MCP, crochets, reproduction sous-jacente, magasin de session, boucle de code Claude comme bibliothèque.

> **Client SDK（`anthropic`）。**Premières pages de l'API.
> **Agent SDK（`claude-agent-sdk`）。**Le code de l'équipe de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion

### Des outils intégrés

Le SDK expédie plus de 10 outils hors boîte: lecture/écriture de fichiers, shell, grep, glob, web fetch, etc. Les outils personnalisés s'enregistrent via l'interface standard outil-schéma.

> SDK 开箱提供 10+ 工具:文件读写、shell、grep、glob、网页抓取等──自定义工具通过标准工具-schema 接口注册──

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Les sous-gants

Deux objectifs documentés par Anthropic:

> L'anthropique a enregistré deux utilisations:

1. **Parallelization.**Exécuter des travaux indépendants simultanément. " Trouver le fichier de test pour chacun de ces 20 modules " est une tâche parallèle de 20 subagents.
2. **Context isolation.**Les subagents utilisent leur propre fenêtre de contexte; seuls les résultats reviennent à l'orchestre.

Python SDK ajoutés récemment: `list_subagents()`- Je suis là .`get_subagent_messages()`pour la lecture des transcriptions de subagents.

> Python SDK récemment ajouté:`list_subagents()`- Je suis là.`get_subagent_messages()`Pour lire le récit de la conversation de l'agent.

>  **【类比】**子 Agent 像大公司的"项目组":CEO 主代理) saisir l'ensemble du projet, mais chaque projet spécifique est exécuté par un groupe de projets spécialisé 子代理)**关键收益是上下文隔离**Si le "rechercheur" doit lire 100 articles sur les produits, le principal agent se fera lui-même et sera submergé; si le fils agent, fils agent, est submergé, le 100 articles sur les produits ne contaminent pas le point de vue du principal agent, il ne revient que sur les 3 conclusions de l'analyse des produits.

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Boutique de séances

Parité de protocole avec TypeScript:

> Avec TypeScript 版本 de l'accord pour les autres:

- `append(session_id, message)` ajouter un tour.
- `load(session_id)`- Retourner la conversation.
- `list_sessions()` énumérer.
- `delete(session_id)` avec des séances en cascade à subagent.
- `list_subkeys(session_id)` liste des clés sous-jacentes.

`--session-mirror`(Bandard CLI) reflète la transcription à un fichier externe alors qu'elle est diffusée, pour débogage.

> `--session-mirror`(CLI 标志) dans le flux de transmission, le dialogue sera enregistré dans des fichiers externes, pour être utilisé pour le contrôle.

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Les crochets

Les crochets de cycle de vie que vous pouvez enregistrer:

> Pour les enfants:

- `PreToolUse`- Je suis là .`PostToolUse` Appels de passerelle ou d'outil d'audit.
- `SessionStart`- Je suis là .`SessionEnd`- Il est en train de démolir.
- `UserPromptSubmit` agir sur les données d'entrée utilisateur avant que le modèle ne les voie.
- `PreCompact` fonctionner avant la compression du contexte.
- `Stop`- Le nettoyage à l'exit de l'agent.
- `Notification` Alertes de canal latéraux.

Les crochets sont la façon dont les flux de travail pro (références du programme de cours de la phase 14) et les systèmes similaires ajoutent un comportement transversale.

> 子是专业工作流 (Phase 14 课程参考) et similaires systèmes de comportement ajouté à travers le monde.

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Contextes de traces W3C

Les étendues OTel actives sur l'appelant se propagent dans le sous-processus CLI via les en-têtes de contexte de trace W3C. L'ensemble de la trace multi-processus apparaît comme une trace dans votre backend.

> 调用方上活跃的OTel span 通过W3C 追踪上下文头传播到CLI 子进程──整个多进程追踪在你的后端显示为一个追踪──

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Claude gérait les agents

L' alternative hébergée (tête bêta `managed-agents-2026-04-01`Le contrôle des transactions pour les infrastructures gérées.

> 托管替方案 beta 头 `managed-agents-2026-04-01`••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Où ce modèle va mal

> ️ **【易错点】**Les catastrophes les plus fréquentes: pour 100 petites tâches générant 100 agents.**后果**: chaque enfant Agent a son propre système prompt + 工具注册 + 上下文初始化,开销 30-60 秒/个,100 个就是 1 小时;并发又有限制(Anthropique chaque minute jeton 限制),最终任务跑一晚上。**一行修复**Le seul vrai besoin de tâches de " indépendance sur la fenêtre " est de créer un agent.

- **Subagent over-spawn.**On fait 100 sous-gants pour 100 petites tâches, le surcharge domine.
- **Hook creep.**Chaque équipe ajoute des crochets, des ballons de démarrage, et les revue tous les trimestres.
- **Session bloat.**Les séances s'accumulent, la taille augmente.`list_sessions`+ politique d'expiration.

> 🤔 **【困惑】**Q: Claude Agent SDK et directement avec Python SDK anthropic 写 agent loop 有什么本质区别?**内置工具开箱即用**(文件、shell、grep 等 10+ 工具, vous-même écrire au moins deux jours);(2) **Session 持久化协议**(incluant子 Agent 会话级联删除);**Hook 生命周期**Si votre agent 只是 simple questions à répondre, utiliser SDK anthropique suffit; si vous devez écrire Claude Code, alors ça est un agent de production, SDK 省你几周工程时间。

> **子 Agent 过度生成。**Pour 100 tâches de production de 100 tâches d'agent, la production de produits, la vente et la gestion de produits, la transformation en traitement en vrac, la transformation en vrac.
> **钩子膨胀。**Chaque équipe ajoute des temps, le temps d'expansion est en cours.
> **会话膨胀。**L'utilisation de la langue est un processus de développement.`list_sessions`+ 过期策略──

## Construisez-le et mettez-le en œuvre.
```figure
ae-subagent-isolation
```

## Faites-le

`code/main.py`met en œuvre la forme SDK dans stdlib:

> `code/main.py`Utilisation de la norme pour réaliser le SDK:

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

- `Tool`- Je suis là .`ToolRegistry`avec intégré `read_file`- Je suis là .`write_file`- Je suis là .`list_dir`- Je suis désolé .
- `Subagent` contexte privé, courir isolé, résultats retournés.
- `SessionStore` ajouter, charger, liste, supprimer, list_subkey.
- `Hooks` `pre_tool_use`- Je suis là .`post_tool_use`- Je suis là .`session_start`- Je suis là .`session_end`- Je suis désolé .
- Une démo: l'agent principal génère 3 sous-générations en parallèle (chacune isolée), agrégate les résultats, persiste la session.

- Je vais le faire.

```
python3 code/main.py
```

La trace montre l'isolement de contexte subagent (la taille du contexte de l'orchestre reste limitée), l'exécution du crochet et la persistance de la session.

> 追踪显示子 代理的上下文隔离(编排者上下文大小保持有界) 子执行和会话持久化──

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

## Utilisez-le avec le cadre de réalisation

- **Claude Agent SDK**pour les produits Claude-first qui veulent la forme du harnais Claude Code.
- **Claude Managed Agents**pour les travaux d'asynchronisation à long terme hébergés.
- **OpenAI Agents SDK**(Létion 16) pour les contreparties OpenAI-premières.
- **LangGraph + custom tools**Si vous voulez la machine d'état en forme de graphe à la place.

## Envoyez-le . Produit .

`outputs/skill-claude-agent-scaffold.md`Échafaudage une application SDK Claude Agent avec sous-boîtes, crochets, magasin de session, MCP attaché serveur, et W3C trace propagation.

> `outputs/skill-claude-agent-scaffold.md`construire un SDK Claude Agent 应用, contenant un agent 子、会话存储、MCP 服务器连接和W3C 追踪传播──

> Claude Agent SDK est l'agent officiel de l'Anthropic 框架──核心概念:Agent(带系统提示和工具的LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

## Les exercices

1. Ajoutez un spawner de sous-gants qui regroupe 20 tâches en groupes de 5 sous-gants parallèles. Mesurez la taille du contexte de l'orchestre par rapport à une par tâche.
  Le mot "exercer" est traduit par "exercer".
2. La mise en œuvre d'une `PreToolUse`accroche que les limites de tarifs `write_file`Les appels (5 minutes par session).
  Le mot "exercer" est traduit par "exercer".
3. Le fil`list_subkeys`Comment est le nidage profond ?
  Le mot "exercer" est traduit par "exercer".
4. Mettez le jouet dans la vraie .`claude-agent-sdk`Quel est le changement de l'enregistrement des outils ?
  Le mot "exercer" est traduit par "exercer".
5. Quand passerais-tu de l'hébergement à l'administration ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent SDK | "Claude Code as a library" | Harness shape: tools, MCP, hooks, subagents, session store |  |
| Subagent | "Child agent" | Separate context, own budget; results bubble up |  |
| Session store | "Conversation DB" | Persist, load, list, delete turns with subagent cascade |  |
| Hook | "Lifecycle callback" | Pre/post tool, session, prompt submit, compact, stop |  |
| W3C trace context | "Cross-process trace" | Parent span propagates into CLI subprocess |  |
| Managed Agents | "Hosted harness" | Anthropic-hosted long-running async work |  |
| `--session-mirror` | "Transcript mirror" | Writes session turns to an external file as they stream |  |
| MCP server | "Tool surface" | External tool/resource source attached to the agent |  |

## Encore une lecture

- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) la forme bibliothécaire du code Claude
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) modèles de production
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) alternative hébergée
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) contrepartie
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
