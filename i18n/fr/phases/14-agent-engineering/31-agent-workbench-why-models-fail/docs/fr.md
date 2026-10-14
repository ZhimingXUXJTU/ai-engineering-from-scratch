# Pourquoi les modèles capables échouent toujours ?

> Un modèle capable ne suffit pas. Les agents fiables ont besoin d'un tableau de travail: instructions, état, portée, rétroaction, vérification, examen et remise en main.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 26 (Failure Modes) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

>  **【前置】**Je suis en train de faire une série de tests de détection de la fonction de la fonction de la fonction de la fonction de la fonction de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de la fonction de détection de détection de la fonction de détection de détection de la fonction de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection de détection.

>  **【类比】**Le chef de cuisine a également fait une erreur en utilisant un mauvais aliment. La phase 14·31-42 détaille ces 7 étapes de travail.

## Objectifs d'apprentissage

- Capacité de modèle séparée de la fiabilité de l'exécution.
- Nommez les sept surfaces de bureau qui décident si un agent expédie.
- Comparez une course en temps réel à une course guidée par un bureau de travail sur une petite tâche de repo.
- Produire un rapport de mode d'échec qui trace chaque surface manquée au symptôme qu'elle a causé.

## Le problème , l' introduction du problème

Vous laissez tomber un modèle frontalier dans un référentiel réel et demandez-lui d'ajouter une validation d'entrée. Il ouvre quatre fichiers, écrit un code plausible, déclare le succès et s'arrête. Vous exécutez les tests. Deux échouent. Un troisième fichier est touché qui n'a rien à voir avec la validation. Il n'y a pas de dossier de ce que l'agent a supposé, ce qu'il a essayé en premier, ou ce qu'il reste à faire.

> Vous mettez un modèle avant-gardiste dans un réel code stockage, laissez-le ajouter des certificats d'entrée. Il ouvre quatre fichiers, écrive un code qui semble raisonnable, déclare le succès, puis arrête. Vous exécutez un test. Deux échecs.

Le modèle n'avait pas tort à propos de Python, il avait tort à propos du travail, il n'avait aucune idée de ce qui comptait comme fait, où il était autorisé à écrire, quels tests étaient autorisés, ou comment la prochaine session devait se dérouler.

> Le modèle en Python n'a pas d'erreur. Il est en train de travailler. Il ne sait pas ce qu'il faut faire. Il ne sait pas dans quelles conditions il faut écrire.


> **【中文解读】**Analyse des causes de défaillance dans un vrai stockage: 1) l'instruction de suivre la défaillance  ignorer la contrainte ou la capacité de créer non-existence; 2) la consommation de la fenêtre supérieure à la fenêtre entraîne la perte d'informations clés; 3) l'accumulation d'erreurs  petites erreurs dans la mise en œuvre à plusieurs étapes; 4) le manque de mémoire du projet  ignorer la configuration et la structure de la base de code.

Ce n'est pas un modèle, c'est un bureau, la surface autour de l'agent manque des pièces qui transforment une génération à un seul coup en ingénierie fiable et réutilisable.

> Ceci n'est pas un bug du modèle. C'est un bug de travail.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

## Le concept de base.

Un bureau de travail est l'environnement de fonctionnement qui enveloppe le modèle pendant une tâche.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

| Surface | What it carries | Failure when missing |
|---------|-----------------|----------------------|
| Instructions | Startup rules, forbidden actions, definition of done | Agent guesses what shipping means |
| State | Current task, touched files, blockers, next action | Each session restarts from zero |
| Scope | Allowed files, forbidden files, acceptance criteria | Edits leak into unrelated code |
| Feedback | Real command output captured into the loop | Agent declares success on a 400 |
| Verification | Tests, lint, smoke run, scope check | "Looks good" reaches main |
| Review | A second pass with a different role | Builder marks own homework |
| Handoff | What changed, why, what is left | Next session re-discovers everything |


> **【中文解读】**Analyse des causes de défaillance dans un vrai stockage: 1) l'instruction de suivre la défaillance  ignorer la contrainte ou la capacité de créer non-existence; 2) la consommation de la fenêtre supérieure à la fenêtre entraîne la perte d'informations clés; 3) l'accumulation d'erreurs  petites erreurs dans la mise en œuvre à plusieurs étapes; 4) le manque de mémoire du projet  ignorer la configuration et la structure de la base de code.

Le tableau de travail est indépendant du modèle. Vous pouvez échanger le modèle et garder les surfaces. Vous ne pouvez pas échanger les surfaces et garder la fiabilité.

> 工作台独立于模型── tu peux remplacer le modèle et garder la surface── tu ne peux pas remplacer la surface et garder la fiabilité──

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

```mermaid
flowchart LR
  Task[Task] --> Scope[Scope Contract]
  Scope --> State[Repo Memory]
  State --> Agent[Agent Loop]
  Agent --> Feedback[Runtime Feedback]
  Feedback --> Verify[Verification Gate]
  Verify --> Review[Reviewer]
  Review --> Handoff[Handoff]
  Handoff --> State
```

La boucle se ferme sur le fichier d'état, pas sur l'historique du chat. Le chat est volatil.

> Le cycle est fermé sur les fichiers d'état, et non sur l'histoire du chat.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Tableau de travail contre l'ingénierie rapide

Le prompte indique au modèle ce que vous voulez à ce tour. Un bureau de travail indique au modèle comment faire le travail à travers les tours et à travers les sessions. La plupart des cas d'échec des agents sont des défaillances du bureau portant des vêtements de prompte-ingénierie.

> 提示告诉模型这个轮你想要什么――工作台告诉模型如何跨轮次和跨会话做工作―― La plupart des agents 失败故事都是穿着提示工程外衣工作台失败――

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Tableau de travail par rapport au cadre

Un framework vous donne un temps d'exécution (LangGraph, AutoGen, Agents SDK). Un bureau de travail donne à l'agent un endroit pour travailler à l'intérieur de ce temps d'exécution. Vous avez besoin des deux. Cette mini-track est à peu près la seconde.

> 框架 gives you a running time ({{langgraph}}, AutoGen、Agents SDK) ⋅工作台 give Agent en ce running time ⋅ tous les deux ont besoin ⋅ cet article est sur le deuxième ⋅

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Réflexion à partir de primitifs, pas de taxonomies de fournisseurs

Il y a beaucoup à écrire sur "l'ingénierie des harnais" en ce moment. Addy Osmani, OpenAI, Anthropic, LangChain, Martin Fowler, MongoDB, HumanLayer, Code d'augmentation, Thoughtworks, la liste des laboratoires de marche incroyable, et un rythme constant de la batterie de médium et Hacker News pièces sont tous en train de le porter. Ils ne sont pas d'accord sur la limite de ce qu'est un harnais, de ce qu'il est dans la portée et du vocabulaire à utiliser. Nous n'avons pas besoin de choisir un parti. Les sept surfaces sont une couche UX; sous chaque bureau de travail se trouve le même ensemble de systèmes distribués primitifs qui tiennent un backend fiable.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

Une course à l'agent est un calcul qui traverse le temps, les processus et les machines. Pour rendre cela fiable, vous avez besoin des mêmes primitives que tout système de production.

> 暂时删除 标签 代理 标签 一个代理 运行是跨越时间、进程和机器的计算 为了使其可靠, vous avez besoin du même langage original que tout système de production 

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

| Primitive | What it is | What it carries for an agent |
|-----------|------------|------------------------------|
| Function | Typed handler. Pure where possible. Owns its inputs and outputs. | A tool call, a rule check, a verification step, a model invocation |
| Worker | Long-lived process that owns one or more functions and a lifecycle | The builder, the reviewer, the verifier, an MCP server |
| Trigger | Event source that invokes a function | Agent loop tick, HTTP request, queue message, cron, file change, hook |
| Runtime | The boundary that decides what runs where, with what timeouts and resources | Claude Code's process, LangGraph's runtime, a worker container |
| HTTP / RPC | The wire between caller and worker | Tool-call protocol, MCP request, model API |
| Queue | Durable buffer between trigger and worker; back-pressure, retry, idempotency | The task board, the feedback log, the review inbox |
| Session persistence | State that survives crashes, restarts, model swaps | `agent_state.json`, checkpoints, KV stores, the repo itself |
| Authorization policy | Who can call what function with which scope | Allowed/forbidden files, approval boundaries, MCP capability lists |

Maintenant, cartographier les sept surfaces de bureau sur ces primitifs.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- **Instructions** les métadonnées de politique + fonction.`AGENTS.md`) est une politique attachée au démarrage de la période d'exécution.
- **State** Persistance de session. Un stockage à clé lit le temps d'exécution à chaque étape. Fichier, KV ou DB; la sémantique de persistance importe, le backend de stockage ne le fait pas.
- **Scope** politique d'autorisation par tâche. Les globes autorisés/interdits sont un ACL. Les approbations requises sont un réseau d'autorisation.
- **Feedback**Chaque appel est un enregistrement, durable, jouable.
- **Verification** une fonction. déterministe sur les entrées. déclenchée lors de la clôture de la tâche. Échec fermé.
- **Review** un travailleur séparé ayant autorité de lecture uniquement sur les objets de construction et autorité de rédaction uniquement sur les rapports d'examen.
- **Handoff** un enregistrement durable émis par un déclencheur de fin de session.

La boucle d'agent elle-même est un travailleur qui consomme des événements (message utilisateur, résultat outil, timing), appelle des fonctions (le modèle, puis les outils que le modèle choisit), écrit des enregistrements (état, rétroaction) et émet des déclencheurs (vérification, révision, remise en main).

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Des motifs en circulation, traduits en primitifs

Chaque modèle de harnais populaire se réduit à huit primitifs.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

| Vendor or community pattern | What it actually is |
|------------------------------|--------------------|
| Ralph Loop (Claude Code, Codex, agentic_harness book) — re-inject original intent into a fresh context window when the agent tries to stop early | A trigger that re-enqueues a task with a clean context; session persistence carries the goal forward |
| Plan / Execute / Verify (PEV) | Three workers, one per role, communicating via state and a queue between phases |
| Harness-compute separation (OpenAI Agents SDK, April 2026) — split control plane from execution plane | Restating control-plane / data-plane. Predates the agent label by decades |
| Open Agent Passport (OAP, March 2026) — sign and audit every tool call against a declarative policy before execution | An authorization policy enforced by a pre-action worker, with a signed audit queue |
| Guides and Sensors (Birgitta Böckeler / Thoughtworks) — feedforward rules + feedback observability | Authorization policy + verification functions + observability traces |
| Progressive compaction, 5-stage (Claude Code reverse engineering, April 2026) | A state-management worker that runs cron-like over session persistence to keep it within a budget |
| Hooks / middleware (LangChain, Claude Code) — intercept model and tool calls | Triggers + functions wrapped around the runtime's invocation path |
| Skills as Markdown with progressive disclosure (Anthropic, Flue) | A function registry where the function metadata is loaded into context just-in-time |
| Sandbox agents (Codex, Sandcastle, Vercel Sandbox) | The compute plane: a runtime with isolated filesystem, network, and lifecycle |
| MCP servers | Workers exposing functions over a stable RPC, with capability lists as authorization |

Chaque entrée dans ce tableau est la communauté d'agents qui arrive à un primitif qui avait déjà un nom dans les systèmes distribués et lui donne un nouveau. Étiquettes utiles pour le marketing; pas utile comme vocabulaire d'ingénierie.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Ce que disent les reçus

La revendication de l'utilisation de ce modèle est maintenant très répandue, car c'est le seul argument honnête contre "attendre un modèle plus intelligent".

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- Terminal Bench 2.0  même modèle, changement de harnais a déplacé un agent de codage de l'extérieur des 30 premiers à la cinquième place (LangChain, * Anatomy of an Agent Harness*).
- Vercel  a supprimé 80% des outils de son agent; le taux de réussite est passé de 80% à 100% (MongoDB).
- Harvey  les agents juridiques ont plus que doublé la précision grâce à l'optimisation de l'harnais seul (MongoDB).
- 88% des projets d'agents d'IA d'entreprise ne parviennent pas à la production. Les défaillances se regroupent autour du temps d'exécution, et non du raisonnement (preprints.org, *Harness Engineering for Language Agents*, mars 2026).
- Une étude de référence de 2025 sur trois cadres open source populaires a rapporté ~50% de fin de tâche; WebAgent de long contexte s'est effondré de 40 à 50% à moins de 10% dans les conditions de long contexte, principalement à partir de boucles infinies et de perte de but (couvert largement au début des rédactions de 2026).

Le résultat n'est pas " le harnais gagne pour toujours. " Les modèles absorbent les astuces du harnais au fil du temps. Le résultat est que aujourd'hui, l'ingénierie porteuse est autour du modèle, pas à l'intérieur, et les primitifs qui transportent cette charge sont ceux dont chaque système de production a toujours eu besoin.

> La conclusion n'est pas "harness 永远赢"―― le modèle va vraiment absorber le harness 技巧―― la conclusion est aujourd'hui, le poids de l'ingénierie de charge est la partie entourant le modèle, et non l'intérieur du modèle, le poids original de cette charge est le nécessaire pour chaque système de production―

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

### Où les écrivains de fournisseurs s'arrêtent à court terme

C'est là que tu n'as pas besoin d'être poli.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- LangChain * Anatomy of an Agent Harness* énumère onze composants  des instructions, des outils, des crochets, des boîtes à sable, de l'orchestration, de la mémoire, des compétences, des sous-composants et une " boucle stupide " de temps d'exécution.
- L'ingénierie de l'agent de harnais d'Addy Osmani a fait tomber le cadre.`Agent = Model + Harness`et le modèle de la ciseau, mais ne dit pas de quoi est construit un harnais.
- Anthropic et OpenAI vont plus profondément sur les surfaces mais restent à l'intérieur de leurs propres temps d'exécution. L'annonce de "séparation de harnais-computation" dans le SDK d'Avril 2026 Agents est la première pièce de fournisseur qui approuve explicitement la séparation contrôle-plan / données-plan. C'est une idée primitive, pas une nouvelle.
- Le livre agent_harness traite le harnais comme un objet de configuration (Jaymin West's *Agentic Engineering*, chapitre 6) et la ligne la plus forte est "le harnais est la principale limite de sécurité dans un système agent".
- Les fils de Hacker News continuent d'arriver au même endroit. Le fil d'avril 2026 *Le harnais d'agent appartient à l'extérieur de la boîte à sable* soutient que le harnais devrait être "plus comme un hyperviseur qui se trouve à l'extérieur de tout et autorise l'accès en fonction du contexte et de l'utilisateur".

Vous n'avez pas besoin de ne pas être d'accord avec l'une de ces pièces pour remarquer le vide. Ils écrivent des descriptions UX d'un système qui existe déjà. Nous écrivons le système. Lorsque le système est construit correctement, les sept surfaces tombent des primitives. Quand il est construit mal, aucune quantité de`AGENTS.md`polish répare la file d'attente manquante.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

Donc quand vous entendez "ingénierie de harnais" ailleurs, traduisez à des primitifs. Les instructions et les règles sont des politiques et des fonctions. Le plancher est le temps de course. Les barreaux sont l'autorisation + la vérification. Les crochets sont des déclencheurs. La mémoire est la persistance des séances. Le Ralph Loop est en attente. Les subagents sont des ouvriers. Les boîtes à sable sont des avions de calcul. Le vocabulaire change, mais pas l'ingénierie. Le tableau de travail est l'UX face à l'agent; le harnais, dans le sens qui survit au prochain reframe fournisseur, est des fonctions, des travailleurs, des déclencheurs, des temps d'exécution, des files d'attente, de la persistance et des politiques câblées correctement.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

## Construisez-le et mettez-le en œuvre.
```figure
wb-seven-surfaces
```

## Faites-le

`code/main.py`Le script compte les surfaces manquantes lors de l'exécution ratée et imprime un rapport de mode de défaillance.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

La tâche de repo est petite à propos: ajouter la validation de l'entrée à un gestionnaire de format FastAPI à un fichier et écrire un test de réussite.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- Je vais le faire.

```
python3 code/main.py
```

Résultats: un journal côte à côte des deux courses, un `failure_modes.json`résumant la course rapide et un verdict à une seule ligne pour la course de travail.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

L'agent est un petit bâton basé sur des règles; le point est les surfaces, pas le modèle.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

## Utilisez-le avec le cadre de réalisation

Trois surfaces de bureau de travail existent déjà dans la nature, même si personne ne les appelle comme ça:

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- **Claude Code, Codex, Cursor.** `AGENTS.md`et `CLAUDE.md`Les commandes de la ligne de démarrage sont la surface des instructions, les commandes de la ligne de démarrage sont la portée, les crochets sont la vérification.
- **LangGraph, OpenAI Agents SDK.**Les points de contrôle et les magasins de séances sont la surface de l'État.
- **CI on a real repo.**Les tests, les liens et la vérification du type sont la vérification. Le modèle de relations publiques est remis.

L'ingénierie de workbench est la discipline de rendre ces surfaces explicites et réutilisables, au lieu de laisser chaque équipe les redécouvrir.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

## Envoyez-le . Produit .

`outputs/skill-workbench-audit.md`est une compétence portable qui vérifie un référentiel existant pour les sept surfaces de bureau et les rapports qui manquent, qui sont partiels, et qui sont sains.

> `outputs/skill-workbench-audit.md`C'est une compétence transportable, qui contrôle les sept surfaces de travail de l'entrepôt existant, rapporte quelles sont les manquements, quelles sont les parties existantes, quelles sont les forces de santé.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

## Les exercices

1. Choisissez un repo où vous avez déjà un agent. Marquez les sept surfaces de 0 (disparu) à 2 (saine). Quelle est votre surface la plus faible?
  Le mot "exercer" est traduit par "exercer".
2. Extension `main.py`Donc la course rapide produit aussi une fausse affirmation de "succès".
  Le mot "exercer" est traduit par "exercer".
3. Ajoutez une huitième surface à votre produit, justifiez pourquoi il ne s'effondre pas dans l'une des sept.
  Le mot "exercer" est traduit par "exercer".
4. Refaire le script avec un autre agent qui hallucine une écriture de fichier supplémentaire.
  Le mot "exercer" est traduit par "exercer".
5. Mettez les cinq modes de défaillance récurrents de l'industrie de la phase 14 · 26 sur les sept surfaces.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Workbench | "The setup" | Engineered surfaces around the model that make work reliable |  |
| Surface | "A doc" or "a script" | A named, machine-readable input the agent reads or writes every turn |  |
| System of record | "The notes" | The file the agent treats as truth when chat history is gone |  |
| Definition of done | "Acceptance" | An objective, file-backed checklist the agent cannot fake |  |
| Workbench audit | "Repo readiness check" | A pass over the seven surfaces that flags missing pieces before work begins |  |

## Encore une lecture

Les concepts sont tous des éléments de la taxonomie partielle, et doivent être traduits en un concept primitif (fonction, travailleur, déclencheur, temps d'exécution, HTTP/RPC, file d'attente, persistance, politique) avant de décider de l'adopter.

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

Les cadres du fournisseur:

- [Addy Osmani, Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) `Agent = Model + Harness`et le motif de la cage; mince sur l'infrastructure
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LangChain, The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) onze composants: les instructions, les outils, les crochets, l'orchestration, les sablettes, la mémoire, les compétences, les sous-gents, le temps d'exécution; omet les files d'attente, le déploiement, l'authz
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI, Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) La vue de l'équipe Codex sur les surfaces autour de leur temps d'exécution
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI, Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) la boucle d'agent réduite à un `while`sur les appels à fonction
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) surfaces à long horizon dans un temps de fonctionnement spécifique
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) notes de conception appliquées
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LangChain Deep Agents harness capabilities](https://docs.langchain.com/oss/python/deepagents/harness) Surface de configuration de l'heure d'exécution
  Le mot "réfléchisseur" est traduit par "réfléchisseur".

Pièces de praticiens avec détails utilisables:

- [Martin Fowler / Birgitta Böckeler, Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) guides (feedforward) + capteurs (feedback); le cadre de la théorie de contrôle le plus propre
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [HumanLayer, Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) "ce n'est pas un problème de modèle, c'est un problème de configuration"
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [MongoDB, The Agent Harness: Why the LLM Is the Smallest Part of Your Agent System](https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system) reçus: Vercel 80% à 100%, Harvey 2x précision, Terminal Bench Top 30 à Top 5
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Augment Code, Harness Engineering for AI Coding Agents](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) La première traversée de la contrainte
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Sequoia podcast, Harrison Chase on Context Engineering Long-Horizon Agents](https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/) préoccupations concernant le temps de fonctionnement par rapport aux préoccupations relatives au modèle
  Le mot "réfléchisseur" est traduit par "réfléchisseur".

Livres, documents et mises en œuvre de référence:

- [Jaymin West, Agentic Engineering — Chapter 6: Harnesses](https://www.jayminwest.com/agentic-engineering-book/6-harnesses) traitement de la longueur du livre, traite l'arsenal comme la limite de sécurité principale
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [preprints.org, Harness Engineering for Language Agents (March 2026)](https://www.preprints.org/manuscript/202603.1756) Cadrage académique en tant que contrôle / agence / temps de fonctionnement
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [walkinglabs/awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering) Liste de lecture organisée en fonction du contexte, de l'évaluation, de l'observabilité, de l'orchestration
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) liste de sélection alternative (outils, évaluations, mémoire, MCP, autorisations)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [andrewgarst/agentic_harness](https://github.com/andrewgarst/agentic_harness) Implémentation de référence prête à la production avec la mémoire et la suite d'évaluation prises en charge par Redis
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) harnais d'agent ouvert avec agent personnel intégré
  Le mot "réfléchisseur" est traduit par "réfléchisseur".

Les thèmes de Hacker News valent la peine d'être lus pour les désaccords, pas pour le consensus:

> Les principales causes de l'échec du modèle d'analyse sont: instructions pour suivre l'échec, outils d'utilisation de l'erreur, perte de texte et rupture de la chaîne de réflexion.

- [HN: Effective harnesses for long-running agents](https://news.ycombinator.com/item?id=46081704)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [HN: Improving 15 LLMs at Coding in One Afternoon. Only the Harness Changed](https://news.ycombinator.com/item?id=46988596)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [HN: The agent harness belongs outside the sandbox](https://news.ycombinator.com/item?id=47990675) plaide pour l'autorisation en tant qu'avion séparé
  Le mot "réfléchisseur" est traduit par "réfléchisseur".

Les références croisées dans ce programme:

- Phase 14 · 23  Conventions OpenTelemetry GenAI: la couche d'observabilité que la littérature des capteurs pointe vers
- Phase 14 · 26  Catalogue des modes d'échec les sept surfaces sont conçues pour absorber
- Phase 14 · 27  Défense à injection rapide qui se situe à la base de la politique d'autorisation
- Phase 14 · 29  Temps d'exécution de la production (file, événement, cron): où les primitifs de cette leçon vivent en déploiement
