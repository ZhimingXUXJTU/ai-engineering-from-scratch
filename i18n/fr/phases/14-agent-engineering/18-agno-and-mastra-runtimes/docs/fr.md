# Agno et Mastra: Les temps de production
# Temps de fonctionnement de l'agent de production  Installation rapide et flux de travail de type

> Un agent de production optimise le temps d'exécution de ce que les cadres de prototypage ignorent: le coût d'instantation, les surfaces de flux de travail typées et un backend prêt à être servi. L'association 2026: Agno (Python) vise l'instantation d'agent de microseconde et les backends FastAPI sans état. Mastra envoie des agents, des outils, des flux de travail, un routage de modèle unifié et un stockage composite sur le substrat SDK Vercel AI.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Identifiez les objectifs de performance d'Agnon et quand ils comptent.
- Nommer les trois primitifs de Mastra  Agents, Tools, Workflows  et les adaptateurs de serveurs pris en charge.
- Expliquez pourquoi un backend FastAPI sans état et scellé par session est la voie de production Agno recommandée.
- Choisissez Agno vs Mastra pour une pile donnée (Python-premier vs TypeScript-premier).

## Le problème , l' introduction du problème

LangGraph, AutoGen, CrewAI sont très lourds en matière de cadres. Les équipes qui veulent " juste la boucle d'agent, rapide, dans mon temps d'exécution " atteignent Agno (Python) ou Mastra (TypeScript).

> LangGraph、AutoGen、CrewAI sont des cadres pré-cheminés. Ils veulent " seulement si l'agent 循环, rapide, pendant mon fonctionnement " les équipes choisiront Agno (Python) ou Mastra (TypeScript).


> **【中文解读】**Agno 和 Mastra représente les deux types d'agents de 2026 运行时设计哲学。Agno(原 PhiData) poursuit极简 avec le plus petit nombre de codes construire Agent。Mastra(TypeScript) poursuit l'ensemble des fonctions fournir un agent complet 生命周期管理。

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}**Agno (GitHub 15k+ stars) 和 Mastra est un nouveau show en 2026 Agent 运行时的新秀。Agno's philosophie est de 'Agent 即函数' Chaque agent est une fonction différente avec un ensemble d'outils。Mastra 基于TypeScript,面向全开发者,提供完整的 Agent 生命周期管理(部署、监控、扩展)。

>  **【前置】**必須先掌握:Phase 14·01(Agent Loop) etPhase 14·13(LangGraph) 本节是这两者"轻量替代品"──如果不知道为什么要"轻量化"LangGraph,说明你还没在生产中遇到LangGraph的工程负担,建议先使用LangGraph 几周再回头看本节──

## Le concept de base.

### Agno

- Python, anciennement Phi-data.
- "Pas de graphiques, de chaînes ou de motifs compliqués  juste python pur".
- Objectifs de performance de leurs documents: ~ 2μs d'instantanation d'agent, ~ 3,75 KiB de mémoire par agent, ~ 23 fournisseurs de modèles.
- Chaque requête démarre un nouvel agent; l'état de session se trouve dans un DB.
- Multimodal natif (texte, image, audio, vidéo, fichier) et RAG agent.

Les objectifs de vitesse comptent quand vous avez des milliers d'agents de courte durée par seconde (chat fan-in, pipelines d'évaluation).

>  **【类比】**Agno 像摩托车、LangGraph 像SUV:摩托车启动快、轻便、能钻小(2μs 实例化、3.75 KiB 内存), adapté à la circulation courte et fréquente(1000 courts tâches par seconde);SUV 装得多、能跑长途、有空调导航(持久化、人回路、复杂图), mais démarrer、慢占地大──**关键洞察**Le choix de l'Agno n'est pas parce qu'il est " meilleur ", mais parce que votre scène est " haute fréquence "

> La vitesse de l'objectif est importante lorsque vous avez des milliers d'agents temporaires par seconde.

> Agno 和 Mastra sont deux types d'agents de petite taille 运行时──Agno 专注快速构建,Mastra 专注 TypeScript 生产部署──两者都提供最小化 Agent 抽象──

### Mastra

- TypeScript, construit sur le SDK Vercel AI.
- Trois primitifs:**Agents**- Je suis là .**Tools**(type de zone), **Workflows**- Je suis désolé .
- Modèle unifié routeur  3 300+ modèles sur 94 fournisseurs (mars 2026).
- Stockage composé: mémoire, flux de travail, observabilité à différents arrière-plans; ClickHouse recommandé pour l'observabilité à l'échelle.
- Apache 2.0 avec `ee/`les répertoires sous licence d'entreprise disponible sous source.
- Adapters serveurs pour Express, Hono, Fastify, Koa; intégration Next.js et Astro de première classe.
- Il envoie Mastra Studio (host local:4111) pour débogage.
- 22k+ GitHub étoiles, 300k+ téléchargements hebdomadaires npm à 1.0 (janvier 2026).

### Positionnement

Ils ne veulent pas être LangGraph.

> Les deux ne sont pas en train de tenter de devenir LangGraph. Leur compétition est:

> Agno 和 Mastra sont deux types d'agents de petite taille 运行时──Agno 专注快速构建,Mastra 专注 TypeScript 生产部署──两者都提供最小化 Agent 抽象──

- **Language fit.**Agno pour les équipes Python-premières; Mastra pour TypeScript-première.
- **Runtime ergonomics.**Agno = dépenses générales presque nulles; Mastra = intégré à l'écosystème Vercel.
- **Observability.**Les deux sont intégrés à Langfuse/Phoenix/Opik (leçon 24) mais Mastra Studio est une première partie.

### Quand choisir chacun

- **Agno**Python backend, beaucoup d'agents de courte durée, des exigences de perf, FastAPI magasin.
- **Mastra** TypeScript backend, Next.js / Vercel déploiement, routage unifié de modèle multi-provider, outils de type Zod.
- **LangGraph**(Létion 13)  lorsque l'état durable et le raisonnement graphique explicite comptent plus que la vitesse brute.
- **OpenAI / Claude Agent SDK** lorsque vous souhaitez une forme productive du fournisseur (leçons 1617).

### Où ce modèle va mal

> ️ **【易错点】**见Agnon "2μs 实例化"就无脑选Agnon**后果**Si votre scénario est " une seule demande de fonctionnement d'un agent de 10 minutes ", 2μs  l'exemplealisation a un impact sur le temps total de consommation de 0,0000003%  sélectionner le cadre aussi perdu la capacité de duration de LangGraph **一行修复**:Prémez votre travail chargé de "Agent  exemples de temps × 单次实例化开销 vs 总耗时", qui représente > 30% 才值得的性能选择 Agno, sinon continuez à utiliser LangGraph。

- **Perf-for-perf's-sake.**Je choisis Agno parce que "2μs" sonne bien quand la charge de travail est un appel lent par agent par demande.
- **Ecosystem lock-in.**L'intégration à la saveur Vercel de Mastra est un plus sur Vercel, un moins ailleurs.
- **Enterprise license confusion.**Le Mastra `ee/`Les annuaires sont disponibles sous source, pas Apache 2.0.

> 🤔 **【困惑】**Q: My team is Python 后端, encore veulent Mastra de "多模型路由" fonction, peut-il utiliser Agno 实现? A: 能, mais il faut écrire soi-même. Agno aussi a ~23 模型 fournisseur, mais Mastra de 3300 + 模型 94 fournisseur est basé sur la grande économie de Vercel AI SDK.

> **为性能而性能。**Parce que les 2μs semblent être bons pour Agno, et le travail est chargé pour chaque demande d'un agent lent.
> **生态系统锁定。**Le style vercel de Mastra est intégré à Vercel, il y a des avantages, il y a des défauts ailleurs.
> **企业许可困惑。**Le maître de la maison`ee/`Le code source est disponible, pas Apache 2.0. Si vous voulez le faire, lisez d'abord la licence.

## Construisez-le et mettez-le en œuvre.
```figure
wb-runtime-spawn
```

## Faites-le

Cette leçon est principalement comparative  aucun artefact de code unique ne rendrait justice à ces deux cadres. Voir `code/main.py`pour un jouet côte à côte: un flux minimal "exécuter un agent, diffuser la sortie, persister la session" mis en œuvre deux fois (une fois en forme d'Agnon, une fois en forme de Mastra).

> Cette classe est principalement comparative. Il n'y a pas de produit de code qui puisse exprimer simultanément les caractéristiques de deux cadres.`code/main.py`Le processus de mise en œuvre de l'agence est de deux fois: une fois Agno, une fois Mastra.

> Agno 和 Mastra sont deux types d'agents de petite taille 运行时──Agno 专注快速构建,Mastra 专注 TypeScript 生产部署──两者都提供最小化 Agent 抽象──

- Je vais le faire.

```
python3 code/main.py
```

Deux traces structurellement différentes mais fonctionnellement équivalentes.

> ∆ Les deux structures diffèrent mais fonctionnent de manière égale à la suite de la même valeur.

> Agno 和 Mastra sont deux types d'agents de petite taille 运行时──Agno 专注快速构建,Mastra 专注 TypeScript 生产部署──两者都提供最小化 Agent 抽象──

## Utilisez-le avec le cadre de réalisation

- **Agno** Python backend qui a besoin de vitesse et de forme FastAPI.
- **Mastra** TypeScript backend avec de nombreux fournisseurs et des primitifs de flux de travail.
- Les deux navires ont des crochets d'observation de première partie.

## Envoyez-le . Produit .

`outputs/skill-runtime-picker.md`choisit Agno, Mastra, LangGraph ou un SDK de fournisseur en fonction de la pile, du budget de latence et de la forme opérationnelle.

> `outputs/skill-runtime-picker.md`根据技术、延迟预算和运营形态选择 Agno、Mastra、LangGraph 或供应商 SDK──

> Agno 和 Mastra sont deux types d'agents de petite taille 运行时──Agno 专注快速构建,Mastra 专注 TypeScript 生产部署──两者都提供最小化 Agent 抽象──

## Les exercices

1. Lisez les documents d'Agno, portez la boucle de réaction de la stdlib à Agno.
  Le mot "exercer" est traduit par "exercer".
2. Lisez les documents de Mastra. Portez la même boucle à Mastra. Qu'est-ce qui a changé dans la typographie des outils (Zod vs rien)?
  Le mot "exercer" est traduit par "exercer".
3. Mesurer la latence de l'instantanation de l'agent sur votre pile.
  Le mot "exercer" est traduit par "exercer".
4. Conçuez une migration: si vous exécutez CrewAI en Python, qu'est-ce qui se passe si vous déménagez à Agno ?
  Le mot "exercer" est traduit par "exercer".
5. Lisez le livre de Mastra `ee/`Quelles restrictions affecteraient une fourchette open source ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## Encore une lecture

- [Agno Agent Framework docs](https://www.agno.com/agent-framework) objectifs de performance, intégration de FastAPI
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Mastra docs](https://mastra.ai/docs) primitifs, adaptateurs serveurs, routeur modèle
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) l'alternative à l'état-graphe
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Comet Opik](https://www.comet.com/site/products/opik/) comparaisons d'observabilité citées par les intégrations de Mastra
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
