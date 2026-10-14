# L'agent de l'observation: Langfuse, Phoenix, Opik

> Trois plates-formes d'observabilité d'agents open source dominent 2026. Langfuse (MIT)  6M+ installations/mois, suivi + gestion rapide + évaluations + répétition de session. Arize Phoenix (Elastic 2.0)  évaluations approfondies spécifiques à l'agent, pertinence RAG, automatisation OpenInference. Comet Opik (Apache 2.0)  optimisation automatique des rappel, garde-corps, détection des hallucinations par juge LLM.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 23 (OTel GenAI) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Nombre des trois principales plateformes d'observabilité des agents open source et leurs licences.
- Distinguer ce que chacun est le plus fort à: Langfuse (sessions mgmt + instantanées), Phoenix (RAG + auto-instrumentation), Opik (optimisation + garde-corps).
- Expliquez pourquoi 89% des organisations déclarent avoir l'observabilité des agents en place d'ici 2026.
- Mettre en œuvre un pipeline de trace à tableau de bord avec évaluation par le juge de la LLM.

## Le problème , l' introduction du problème

OTel GenAI (Léction 23) vous donne le schéma. Vous avez toujours besoin de la plateforme qui ingère les étendues, exécute les évaluations, stocke les versions rapides et surface les régressions.

> OTel GenAI (III) vous a donné un schéma. Vous avez toujours besoin d'une plateforme pour recevoir la durée de fonctionnement, l'évaluation, la mise en cache et la réémission.

>  **【前置】**Je vous invite à maîtriser la phase 14 de l'OTEL GenAI Conventions.`invoke_agent`La phase 14·05 (Self-Refine/CRITIC)  Comprendre le mode de jugement de la LLM est un mode de jugement critique, sinon vous jugerez comme étant "un autre LLM à utiliser" plutôt que "une vérification des faits fondée sur des preuves externes".


> **【中文解读】**Une plateforme de surveillance est fournie à l'agent de l'exécution du processus de surveillance de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécution de l'exécuteur.

## Le concept de base.

### Langfuse (MIT)

>  **【类比】**Les trois types de systèmes d'information hospitaliers sont divisés:**Langfuse**est un ensemble de HIS hospitalisés, en particulier dans les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé et les établissements de santé, les établissements de santé et les établissements de santé et les établissements de santé et les établissements de santé et de santé, les établissements de santé et les établissements de santé et les établissements de santé et de santé publique, les établissements de santé publique, les établissements de santé publique, les établissements de santé et les établissements de santé publique, les établissements de santé et de santé publique, en établissements de santé publique, en établissements de santé publique, en établissements de santé publique, établissements de santé publique et de santé publique, en établissements de santé publique, établissements de santé publique et de santé publique, en établissements de santé publique, établissements de santé publique, établissements de santé et de santé publique, établissements de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé publique, établissement de santé**Phoenix**Il est un centre d'examen spécialisé dans la recherche de qualité, la recherche de comportement, la recherche de traces et le clustering de données qui vous indiquent que le comportement de l'agent et le comportement de l'agent ne sont pas similaires, mais que vous ayez modifié le conseil.**Opik**C'est un système de gestion des essais cliniques. Il peut être utilisé pour la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre.

- 6M+ SDK installés par mois, 19k+ étoiles GitHub.
- Caractéristiques: suivi, gestion rapide avec version + terrain de jeu, évaluations (LLM-as-judge, commentaires des utilisateurs, personnalisés), répétitions de session.
- Juin 2025: précédemment des modules commerciaux (LLM-as-a-judge, files d'attente d'annotation, expériences rapides, Playground) open-source sous MIT.
- Le plus fort pour: observabilité de bout en bout avec une boucle de gestion rapide serrée.

### Arize Phoenix (licence élastique 2.0)

- Évaluation plus approfondie spécifique à l'agent: clustering des traces, détection d'anomalies, pertinence de la récupération pour le RAG.
- Autonome instrumentation OpenInference natif.
- Partage avec Arize AX géré pour la production.
- Aucune version rapide  positionnée comme un outil de dérive/régrésion comportementale aux côtés de plates-formes plus larges.
- Le plus fort pour: la pertinence des RAG, la dérive comportementale, la détection des anomalies.

### Comète Opik (Apache 2.0)

- Optimisation rapide automatisée par des expériences A/B.
- Rideaux de protection (rédaction des informations sur les données, contraintes de travail).
- Détection d'hallucinations par le juge LLM.
- Benchmark de la mesure de Comet: les journaux Opik + évaluations en 23.44s vs Langfuse 327.15s (~14x gap)  prennent les benchmarks du fournisseur comme directionnels.
- Le plus fort pour: boucle d'optimisation, expérimentation automatisée, application de la garde-corps.

### Données de l'industrie

Par Maxim (2026 analyse de terrain): 89% des organisations ont une observabilité des agents; les problèmes de qualité sont la principale barrière de production (32% des répondants les citent).

> Les outils de surveillance et de révision des indicateurs de fonctionnement sont fournis par l'agent 可观测性平台提供运行时追踪、指标监控和调试工具──Langfuse、Arize Phoenix、Braintrust est l'agent principal可观测性工具── en 2026

### Je choisis une

| Need | Pick |
|------|------|
| All-in-one with prompt management | Langfuse |
| Deep RAG evaluation + drift | Phoenix |
| Automated optimization + guardrails | Opik |
| Open licensing, no ELv2 | Langfuse (MIT) or Opik (Apache 2.0) |
| Datadog / New Relic integration | Any — they all export OTel |

### Où ce modèle va mal

> 🤔 **【困惑】**Q: 89% des organisations disent avoir un agent observable, mais pourquoi l'accident est-il encore là? A: La plupart des équipes ne font que " connecter OTel → tracer dans Langfuse " cette étape, c'est comme installer une caméra de surveillance mais personne ne la regarde.

- **No eval strategy.**Tracer sans évaluation est juste une extraction coûteuse.
- **Self-rolled LLM-judge without grounding.**Le modèle CRITIC (leçon 05) s'applique  les juges ont besoin d'outils externes pour la vérification des faits.
- **Prompt versions not tied to traces.**Quand le prod régresse, vous ne pouvez pas le couper à l'interrupteur qui l'a causé.

> **没有评估策略。**Aucune évaluation n'est faite, mais un journal coûteux.
> **自建的 LLM 评审器没有基础。**• la mise en œuvre d'un système de contrôle des données et de la gestion des données.
> **提示版本未与追踪关联。**Quand la production est revenue, vous ne pouvez pas vous positionner pour résoudre le problème.

## Construisez-le et mettez-le en œuvre.

> ️ **【易错点】**场景: le team a tracé OTel 接到Langfuse 后, a écrit un juré LLM 给每条 trace 打 1-5分, mais la rubrique n'a qu'une phrase "response très bien mal" → 后果:分数毫无意义, jugez Placez"礼貌但答错"打 5分"",正确但简短"打 2分,dashboard 上 95% 满意度但客户投诉暴 → 修复: rubrique 必须维维分(((factual correctness、scope adherence、tone), chaque dimension de l'exploitation est définie comme "scope adherence: l'agent a-il fait ou non les exigences de l'utilisateur"), et comportez 50-100 articles de marque d'exploitation à la base   准为何强调"Phoenix"Phoenix souligne que le juge a "confirmé" sur votre propre corpus de travail.
```figure
wb-trace-ingest
```

## Faites-le

`code/main.py`met en œuvre un collecteur de traces stdlib + évaluateur juge LLM:

> Les outils de surveillance et de révision des indicateurs de fonctionnement sont fournis par l'agent 可观测性平台提供运行时追踪、指标监控和调试工具──Langfuse、Arize Phoenix、Braintrust est l'agent principal可观测性工具── en 2026

- Ingérez des écoulements en forme de GenAI.
- Groupe par session, étiquette de défaillance des courses (voyage de garde, évaluations de faible confiance).
- Un juge de droit spécialisé qui note les réponses des agents sur une rubrique.
- Un résumé de tableau de bord: taux d'échec, principales raisons d'échec, répartition des scores d'évaluation.

- Je vais le faire.

```
python3 code/main.py
```

Résultats: scores d'évaluation par séance et catégorisation des défaillances correspondant à ce que Langfuse/Phoenix/Opik montrerait.

> 输出: pour chaque séance, le nombre d'évaluations et les défaites des classes, correspondant au contenu de Langfuse/Phoenix/Opik.

> Les outils de surveillance et de révision des indicateurs de fonctionnement sont fournis par l'agent 可观测性平台提供运行时追踪、指标监控和调试工具──Langfuse、Arize Phoenix、Braintrust est l'agent principal可观测性工具── en 2026

## Utilisez-le avec le cadre de réalisation

- **Langfuse**hébergé par eux-mêmes ou dans le cloud; transmis par voie électronique via OTel ou leur SDK.
- **Arize Phoenix**Autogestion; ouverture à l'instrument automatique.
- **Comet Opik**l'hébergement autonome ou dans le cloud; boucle d'optimisation automatisée.
- **Datadog LLM Observability**pour les équipes de opérations mixtes + ML qui gèrent déjà Datadog.

## Envoyez-le . Produit .

`outputs/skill-obs-platform-wiring.md`choisit une plateforme et envoie des traces + évaluations + des versions rapides dans un agent existant.

> `outputs/skill-obs-platform-wiring.md`选择一个平台,并将追踪 + 评估 + 提示版本 接入现有代理──

> Les outils de surveillance et de révision des indicateurs de fonctionnement sont fournis par l'agent 可观测性平台提供运行时追踪、指标监控和调试工具──Langfuse、Arize Phoenix、Braintrust est l'agent principal可观测性工具── en 2026

## Les exercices

1. Exporter une semaine de traces d'OTel vers le cloud Langfuse.
  Le mot "exercer" est traduit par "exercer".
2. Écrivez une rubrique de juge de LLM pour votre domaine (correction factuelle, ton, adhérence à la portée).
  Le mot "exercer" est traduit par "exercer".
3. Comparer la version rapide de Langfuse avec la cluster de traces de Phoenix.
  Le mot "exercer" est traduit par "exercer".
4. Lisez les documents de la garde d'Opik, envoyez une garde d'information à l'un de vos agents.
  Le mot "exercer" est traduit par "exercer".
5. Évaluez les trois sur votre corpus, ignorez les chiffres publiés par le vendeur, mesurez les vôtres.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Tracing | "Spans collector" | Ingest OTel / SDK spans; index by session |  |
| Prompt management | "Prompt CMS" | Versioned prompts tied to traces |  |
| LLM-as-judge | "Automated eval" | Separate LLM scores agent output against a rubric |  |
| Session replay | "Trace playback" | Step through past runs for debugging |  |
| RAG relevancy | "Retrieval quality" | Does the retrieved context match the query |  |
| Trace clustering | "Behavioral grouping" | Cluster similar runs for drift detection |  |
| Guardrail enforcement | "Policy at log time" | PII/toxicity/scope checks on logged content |  |

## Encore une lecture

- [Langfuse docs](https://langfuse.com/) Traçabilité, évaluation, mise en œuvre rapide
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Arize Phoenix docs](https://docs.arize.com/phoenix) Automatisation des instruments, dérive
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Comet Opik](https://www.comet.com/site/products/opik/) Optimisation + barreaux
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) le schéma consomment les trois
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
