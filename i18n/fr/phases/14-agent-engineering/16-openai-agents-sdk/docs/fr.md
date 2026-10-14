# Les dépôts, les gardes, le suivi.

> OpenAI Agents SDK est le framework multicommandé léger construit sur l'API Responses. cinq primitifs: Agent, Handoff, Guardrail, Session, Tracing.`transfer_to_<agent>`Les rails de garde sont activés par défaut.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Nombre des cinq primitifs du SDK OpenAI Agents.
- Expliquez les remises: pourquoi elles sont modélisées comme des outils, quelle forme de nom le modèle voit et comment le contexte se transmet.
- Distinguer les barreaux d'entrée, les barreaux de sortie et les barreaux d'outillage; expliquer `run_in_parallel`contre le mode de blocage.
- Implémenter un runtime stdlib avec des remises + barreaux + traçage de style span.

## Le problème , l' introduction du problème

Les agents qui ne peuvent pas déléguer de manière propre finissent par tout remplir dans un seul prompt. Les agents sans barreaux expédient des PII, des sorties violant les politiques ou des boucles pour toujours. Le SDK d'OpenAI codifie les trois primitives qui rendent le travail multi-agent traitable.

> 无法干净地委派任务的代理 最终将所有东西塞进一个提示词中. 无护的代理会泄露PII,输出违反政策内容或永远循环. OpenAI SDK rendra le travail de plusieurs agents gérable.


> **【中文解读】**OpenAI Agents SDK(original Swarm) est le cadre de développement officiel de l'agent OpenAI.

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}**Le SDK d'OpenAI Agents est le cadre d'agent de classe léger le plus populaire de 2025-2026[6]. Son mode de délivrance permettra à plusieurs agents de coopérer pour "réunir" un agent qui effectuera sa propre partie et qui transfère le contrôle à un autre[6].

>  **【前置】**Il faut d'abord connaître:Phase 14·01(Agent Loop) et Phase 14·06(Utilisation des outils) OpenAI Agents SDK sont ces concepts de produits en vrac.

## Le concept de base.

### Cinq primitifs

1. **Agent.**LLM + instructions + outils + remises.
2. **Handoff.**Délégué à un autre agent.`transfer_to_<agent_name>`- Je suis désolé .
3. **Guardrail.**Validation sur entrée (seulement le premier agent), sortie (seulement le dernier agent) ou invocation d'outil (par outil de fonction).
4. **Session.**L'historique de conversation automatique à travers les virages.
5. **Tracing.**Des couches intégrées pour les générations de LLM, des appels à l'outil, des remises, des barreaux.

### Les outils

Le modèle voit .`transfer_to_billing_agent`L'appel indique le temps de fonctionnement à:

> 模型 dans sa liste d'outils voir `transfer_to_billing_agent`调用 Il signifie fonctionnement lorsque besoin:

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

1. Copiez le contexte de la conversation (ou effondre via `nest_handoff_history`- le beta).
2. Initializer l'agent cible avec ses instructions.
3. Continuez la course avec l'agent cible.

C'est le modèle de supervision (leçon 13 / leçon 28) produit.

> C'est le modèle de la surveillance des produits après leur mise en œuvre.

>  **【类比】**En écoutant la description du patient, il dit: "Tu vas au centre cardiaque".`transfer_to_cardiology_agent` patients (en anglais seulement)**关键**Le contrôle est un simple transfert, l'agent original ne participe plus.

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

### Rennes de garde

Trois saveurs:

> Trois types:

- **Input guardrails.**Rejetez les demandes dangereuses ou hors de portée avant toute appel de LLM.
- **Output guardrails.**On peut détecter les fuites d'informations, les violations de la politique, les réponses malformées.
- **Tool guardrails.**Exécutez l'outil par fonction, validez les arguments, vérifiez les autorisations, exécutez l'audit.

Mode:

> 模式:

- **Parallel**(par défaut). le LLM Guardrail fonctionne à côté du LLM principal.
- **Blocking**(le secteur de l'énergie)`run_in_parallel=False`Le Master de la Garde routière passe en premier, si vous trébuchez, aucun jeton n'est gaspillé sur l'appel principal.

Les câbles triplé s' élèvent .`InputGuardrailTripwireTriggered`- Je suis là .`OutputGuardrailTripwireTriggered`- Je suis désolé .

> Le détecteur de coups de feu`InputGuardrailTripwireTriggered`- Je suis là .`OutputGuardrailTripwireTriggered`- Ça va.

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

### Traçage

Chaque génération de LLM, appel à l'outil, remise en main et garde-corps émet une durée. `OPENAI_AGENTS_DISABLE_TRACING=1`Il décide de ne pas le faire.`add_trace_processor(processor)`Les fans s'étendent à votre propre backend à côté de OpenAI.

> 默认开启──每次LLM 生成、工具调用、交接和护都发发出一个跨度──`OPENAI_AGENTS_DISABLE_TRACING=1`Je peux choisir de me retirer.`add_trace_processor(processor)`Il peut être envoyé à votre propre bout et à l'arrière de OpenAI.

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

### Les séances

`Session`stocke l'historique de conversation dans un backend (SQLite, Redis, personnalisé). `Runner.run(agent, input, session=session)`les charges automatiques et les appendages.

> `Session`Dans le cadre de la mise en œuvre de la politique de sécurité, le gouvernement a décidé de mettre en place une nouvelle politique de sécurité.`Runner.run(agent, input, session=session)`Automatisez et ajoutez.

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

### Où ce modèle va mal

> ️ **【易错点】**Départ de délivrance: l'agent A 移交给 B,B 又移交给 A,A 再移交给 B...**后果**Le projet est terminé.**一行修复**: dans le coureur 里加 hop counter`max_handoffs=5`), dépassant`HandoffBudgetExceeded`异常──OpenAI SDK 默认没有这个保护, il faut se mettre à jour──

- **Handoff drift.**L'agent A passe à l'agent B qui le remet à l'agent A. Ajoutez un compteur de saut.
- **Guardrail bypass.**Les barreaux d'outils ne tirent que sur les outils fonctionnels; les outils intégrés (lecteur de fichiers, récupération Web) ont besoin d'une politique distincte.
- **Over-tracing.**Contenu sensible en spans. Parler avec OTel GenAI règles de capture de contenu (leçon 23)  stockage externe, référence par ID.

> 🤔 **【困惑】**Q: Parallèle de garde-rail et blocage 模式怎么选? looks parallel 总是更快──A: 不一定──Parallèle est "main LLM 和 garde-rail LLM 同时跑"快但浪费代币(garde-rail 触发时时主 LLM 已经在跑,代币 已经花了)──Blocking est "先 guardrail,过了再主 LLM"慢但省钱──**选择规则**Si le taux de détérioration est faible, il est préférable de bloquer le taux de détérioration parallèle.

> **交接漂移。**L'agent A 交付 à l'agent B, l'agent B 交付 à l'agent A 添加跳数计器
> **护栏绕过。**工具护 只有在函数工具上触发;内置工具(文件读取器、网页抓取) nécessite une stratégie unique。
> **过度追踪。**La liste comporte des informations sensibles.

## Construisez-le et mettez-le en œuvre.
```figure
ae-agent-handoff
```

## Faites-le

`code/main.py`met en œuvre la forme SDK dans stdlib:

> `code/main.py`Utilisation de la norme pour réaliser le SDK:

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

- `Agent`- Je suis là .`FunctionTool`- Je suis là .`Handoff`(en tant qu'outil de fonction avec la sémantique de transfert).
- `Runner`avec des barreaux d'entrée/sortie/outil, un déploiement de dépêche et un compteur de saut.
- Un émetteur simple pour montrer la forme de la trace.
- Un agent de triage qui se livre à la facturation ou au support en fonction de la requête de l'utilisateur; les sorties de garde-garde sur une entrée.

- Je vais le faire.

```
python3 code/main.py
```

La trace montre deux remises réussie, un voyage sur la garde-ferre d'entrée, et un arbre d'espace reflétant ce que le SDK réel émet.

> Trace montre deux connexions réussis ∞ une fois d'entrée ∞ et une fois de détail ∞

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

## Utilisez-le avec le cadre de réalisation

- **OpenAI Agents SDK**pour les premiers produits OpenAI.
- **Claude Agent SDK**(Létion 17) pour les produits Claude-first.
- **LangGraph**(Létion 13) quand vous voulez un état explicite et un CV durable.
- **Custom**lorsque vous avez besoin d'un contrôle exact (voix, multi-fournisseurs, déploiements fédérés).

## Envoyez-le . Produit .

`outputs/skill-agents-sdk-scaffold.md`échafaudage d'une application SDK Agents avec un agent de triage, des remises, des barreaux d'entrée/sortie/outil, un magasin de session et un processeur de suivi.

> `outputs/skill-agents-sdk-scaffold.md`construire un SDK d'agents application, contenant un agent de suivi 交接、输入/输出/工具护、会话存储和追踪处理器──

> Les agents d'OpenAI 提供四种核心概念:Agents (en anglais seulement) 带指令和工具的LLM) ‧Handoffs (en anglais seulement) ‧Agent 间移交) ‧Guardrails (en anglais seulement) 输入/输出验证 (en anglais seulement) ‧Tracing (en anglais seulement) 运行追踪 (en anglais seulement) ‧Production (en anglais seulement) 开发框架 (en anglais seulement) ‧Agent 开发框架 (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails (en anglais seulement) ‧Gardrails) ‧Gardrails (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails de gestion (en anglais seulement) ‧Gardrails) ‧Gardrails de gestion (en anglais) ‧Grading)

## Les exercices

1. Ajouter un compteur de dépôt: rejet après N transfert.
  Le mot "exercer" est traduit par "exercer".
2. Mise en œuvre `nest_handoff_history`en option  coller les messages précédents en un seul résumé avant de les transférer.
  Le mot "exercer" est traduit par "exercer".
3. Écrivez une barrière de sortie bloquant. Comparer la latence sur les commandes qui le bousculeraient contre celles qui passent.
  Le mot "exercer" est traduit par "exercer".
4. Le fil`add_trace_processor`Quelle forme émet-il par intervalle ?
  Le mot "exercer" est traduit par "exercer".
5. Lisez les documents du SDK. Portez votre jouet stdlib à `openai-agents-python`- Vous avez mal modelé quoi ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## Encore une lecture

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) primitivité, remise en main, garde-corps, traçage
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) Cote-partie à la saveur de claude
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) quand se rendre à la demande
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) le SDK standard Agents couvre la carte à
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
