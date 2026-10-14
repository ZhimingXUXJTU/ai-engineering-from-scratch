# OpenTelemetry GenAI Conventions sémantiques

> Le génAI SIG d'OpenTelemetry (lancé en avril 2024) définit le schéma standard de télémétrie d'agent. Les noms de domaine, les attributs et les règles de capture de contenu convergent entre les fournisseurs, de sorte que les traces d'agent signifient la même chose dans Datadog, Grafana, Jaeger et Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Nommer les catégories de génération d'intervalle: modèle/client, agent, outil.
- Distinguer`invoke_agent`Les écarts de client versus internes et lorsque chacun s'applique.
- Liste des attributs de GenAI de premier niveau: nom du fournisseur, modèle de demande, identifiant de la source de données.
- Expliquer le contrat de capture de contenu: opt-in, `OTEL_SEMCONV_STABILITY_OPT_IN`, recommandation de référence externe.

## Le problème , l' introduction du problème

> **【中文解读】**Chaque fournisseur a inventé son propre espace de travail, le groupe de travail a finalement besoin de construire un instrument de travail indépendant pour chaque cadre.

Chaque fournisseur invente ses propres noms de champs. Les équipes d'opérations finissent par construire des tableaux de bord par cadre.

> Chaque fournisseur a développé son propre espace de travail. Le transport a finalement besoin de construire un tableau de bord indépendant pour chaque cadre.

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

>  **【前置】**學本節前 請先掌握:Phase 14·01(Agent Loop) 你需要先有 Agent 才能给它埋点;Phase 14·13(LangGraph) 理解状态图,因为跨度的父子层级就是图遍历的镜像──如果完全没有接触过OpenTelemetry(不知道什么是跨度、痕迹、语境传播),先看OTel 官方 Python 快速进入本节只讲 GenAI 专属约定,不重讲 OT基础 ⋅

## Le concept de base.

### Catégories de champs

>  **【类比】**Les trois catégories de l'OTel GenAI sont les suivantes:**Model span**Il est le plus bas niveau, enregistré "trait combien de sang"", avec quel instrument"", résultats combien" à la correspondance des symboles numéros, noms de modèles,, retard);**Agent span**Le processus complet de la maladie, du numéro de liaison au numéro de départ, comprend plusieurs expériences;**Tool span**Il y a aussi des projets de contrôle.`parent_span_id`链回父记录这样 Datadog 里你能展开看: l'ensemble de l'agent 调用 → 5 fois tool调用 → Chaque fois tool调用里 2 fois LLM 调用。

1. **Model / client spans.**Couvrir les appels LLM bruts. émis par les SDK du fournisseur (Anthropic, OpenAI, Bedrock) et les adaptateurs de modèles de cadre.
2. **Agent spans.** `create_agent`(lorsque l'agent est construit) et `invoke_agent`(lorsqu'il fonctionne).
3. **Tool spans.**Un par invocation d'outil; connecté à l'espace d'agent par relation parent-enfant.

### Nom de l'agent

- Nom de l'espagnol: `invoke_agent {gen_ai.agent.name}`si nommé; retour à `invoke_agent`- Je suis désolé .
- Une espèce de spande:
  - **CLIENT** pour les services d'agents à distance (API OpenAI Assistants, Agents Bedrock).
  - **INTERNAL** pour les cadres d'agents en cours de processus (LangChain, CrewAI, local ReAct).

### Attributs clés

- `gen_ai.provider.name` `anthropic`- Je suis là .`openai`- Je suis là .`aws.bedrock`- Je suis là .`google.vertex`- Je suis désolé .
- `gen_ai.request.model` le modèle d'identification.
- `gen_ai.response.model` le modèle résolu (peut différer de la demande en raison du routage).
- `gen_ai.agent.name` Identifiant de l'agent.
- `gen_ai.operation.name` `chat`- Je suis là .`completion`- Je suis là .`invoke_agent`- Je suis là .`tool_call`- Je suis désolé .
- `gen_ai.data_source.id` pour les RAG: quel corpus ou magasin a été consulté.

Des conventions spécifiques à la technologie existent pour Anthropic, Azure AI Inference, AWS Bedrock, OpenAI.

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

### Capture de contenu

> ️ **【易错点】**场景: développeur 图省事在`invoke_agent`L'application est une application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'utilisateur.`gen_ai.input.message_id=row42`), l'original落到带带 ACL'objet de stockage S3 里,运维要查时通过 ID 跳转授权访问──这就是本节反复强调的"external-reference recommendation"──

La règle par défaut: les instruments ne DEVENT PAS capturer les entrées/sorties par défaut.

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

Le modèle de production recommandé: stocker le contenu à l'extérieur (S3, votre magasin de journaux), enregistrer les références sur les intervalles (identifiants de pointeur, pas de prose).

>                                                                                                                                                                                                                                                               

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

### Stabilité

La plupart des conventions sont expérimentales à partir de mars 2026.

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

Les cartes Datadog v1.37+ génAI attribue nativement dans son schéma d'observabilité LLM. D'autres backends (Grafana, Honeycomb, Jaeger) prennent en charge les attributs bruts.

> 🤔 **【困惑】**Q: `invoke_agent`A: Look being调用 Agent est pas "autre processus/service" A: 看被调用 Agent est "另一个进程/服务" A: 看被调用 Agent est pas "另一个进程/服务" A: 看被调用 Agent est "另一个进程/服务" A: 看被调用 Agent est pas "另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用 Agent是不是另一个进程/服务" A: 看被调用 Agent是不是"另一个进程/服务" A: 看被调用的过程是不是"另一个进程, A: 如果你直接在 Python 进程中导入 Python 运行一个 ReAct,它是internal你自己的代码中的子调用. 如果你调用了 OpenAI助理的助理的帮助,那么你会调用 OpenAI助理的帮助的服务,那么是A: 链接的链接的链接与客户端的链接是链接的链接是链接的链接是链接的链接是链接的链接的链接是链接的, A:`rpc.system`- Je suis là.`rpc.service`), la facilité et la tradition de traçabilité des services

> Datadog v1.37+ 原生将 GenAI 属性映射到其LLM Observability schema──其他后端(Grafana、Honeycomb、Jaeger) support原始属性──

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

### Où ce modèle va mal

- **Capturing full prompts in spans.**Les informations personnelles, les secrets, les données des clients dans des traces que les opérations peuvent lire.
- **No `gen_ai.provider.name`.**Les tableaux de bord multi-fournisseurs se cassent lorsque l'attribution est manquante.
- **Spans without parent links.**Les outils orphelins s'étendent, ils propagent toujours le contexte.
- **Not setting stability opt-in.**Vos attributs peuvent être renommés lors de la mise à niveau.

> **在 span 中捕获完整提示。**运维可以读取的追踪包含PII、密钥、客户数据──externe stockage──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**Votre attribut pourrait être renommé à la fin de la mise à niveau.

## Construisez-le et mettez-le en œuvre.
```figure
ae-genai-span-tree
```

## Faites-le

`code/main.py`met en œuvre un émetteur stdlib d'épanouissement correspondant aux conventions de GenAI:

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

- `Span`avec le schéma d'attribut GenAI.
- `Tracer`avec `start_span`, des contextes enlisés.
- Un agent scripté qui émet:`create_agent`- Je suis là .`invoke_agent`(INTERNAL), par outil,`chat`les cours de droit.
- Un mode de capture de contenu qui stocke les invites à l'extérieur et enregistre les identifiants sur les intervalles.

- Je vais le faire.

```
python3 code/main.py
```

Sortie: un arbre de débit avec tous les attributs GenAI requis, et un "marché externe" montrant les références de contenu opt-in.

> 输出: un contenant de tout ce qui est nécessaire à la génération d'attributs 树, ainsi qu'un "extérieur stockage" de "extérieur stockage" de contenu.

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

## Utilisez-le avec le cadre de réalisation

- **Datadog LLM Observability**(v1.37+) des attributs de cartes natifs.
- **Langfuse / Phoenix / Opik**(Létion 24)  auto-instrument de l'écosystème.
- **Jaeger / Honeycomb / Grafana Tempo** traces OTel brutes; construire des tableaux de bord à partir des attributs GenAI.
- **Self-hosted** exécuter le Collecteur OTel avec un processeur GenAI.

## Envoyez-le . Produit .

`outputs/skill-otel-genai.md`Les fils OTel GenAI s'étendent sur un agent existant avec des défauts de capture de contenu et de stockage de référence externe.

> `outputs/skill-otel-genai.md`L'OTel GenAI est une gamme de données qui contient des données de référence et des données de référence externes.

> OpenTelemetry GenAI 语义约定 définit les critères de visibilité de LLM 和 Agent.`gen_ai.request.model`- Je suis là.`gen_ai.usage.input_tokens`- Je suis là.`gen_ai.agent.name`Ça va.

## Les exercices

1. Instruisez votre leçon 01 ReAct loop avec `invoke_agent`(INTERNAL) + spans par outil. Envoyez à une instance Jaeger.
  Le mot "exercer" est traduit par "exercer".
2. Ajouter la capture de contenu en mode "références seulement": les requêtes à SQLite, les attributs de durée ne comportent que des identifiants de rangée.
  Le mot "exercer" est traduit par "exercer".
3. Lisez la spécification pour `gen_ai.data_source.id`- Envoyez-le dans votre recherche de leçon 9.
  Le mot "exercer" est traduit par "exercer".
4. Réglage `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`et vérifier que vos attributs ne sont pas renommés par le collectionneur.
  Le mot "exercer" est traduit par "exercer".
5. Construire un tableau de bord: "quelles erreurs d'outil corrélataient avec quels modèles" à partir des attributs GenAI seulement.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## Encore une lecture

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) la spécification
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) Généraux par défaut
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Des espaces OTel intégrés
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) Propagation du contexte de trace W3C
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
