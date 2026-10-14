# Les portes de vérification sont contrôlées.

> L'agent ne peut pas marquer son propre travail comme fait. Une passerelle de vérification lit le contrat de portée, le journal de rétroaction, le rapport de règles et le diff, et répond à une seule question: cette tâche est-elle réellement terminée?

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 33 (Rules), Phase 14 · 36 (Scope), Phase 14 · 37 (Feedback) | **前置知识:** 见原文
**Time:** ~55 minutes | **时间:** 见原文

>  **【前置】**Je suis en train de faire une étude sur la façon dont les gens peuvent apprendre à comprendre la réalité de la réalité.
>  **【类比】**La vérification de la porte = 出厂质检,Agent 自己说"我做完了"不算数gate 独立检查"测试是否通过、scope 是否守住、规则是否满足、diff 是否合理"──门控失败,任务不算完成──这是阶段14·39(Reviewer Agent) 简化版gate 是脚本,reviewer 是 LLM──

## Objectifs d'apprentissage

- Définir une passerelle de vérification comme une fonction déterministe sur les artefacts de bureau.
- Combinez le rapport de règles, le rapport de portée, les dossiers de rétroaction et la différence en un seul verdict.
- Émettez un `verification_report.json`L'agent de l'examen et l'informateur peuvent lire.
- Refuser de faire avancer une tâche sur toute défaillance de gravité de bloc, sans exception.

## Le problème , l' introduction du problème

Les agents déclarent trop facilement le succès.

> L'agent est très facile à déclarer un succès.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

- " Ça a l'air bien. " Le modèle a lu sa propre différence et a décidé qu'elle était correcte.
- "Les tests ont passé". Il a dit en toute confiance.
- "Acceptation satisfaite". Les critères d'acceptation sont interprétés assez lourdement pour signifier "tout ce qui ressemble à ce qui a été fait".


> **【中文解读】**验证门在 Agent 执行的关键节点插入自动检查──常见验证门:(1) 编译检查代码修改后必须通过编译;(2) 测试检查提交前必须通过相关测试;(3) Lint 检查代码必须符合风格规范;(4) 安全检查必须引入已知漏洞──验证门防止错积――

La solution de la table de travail est une seule passerelle de vérification qui lit les objets que l'agent a déjà produits et fait l'appel. La passerelle est déterministe. La passerelle est en contrôle de version. La passerelle est câblée dans CI. L'agent ne peut pas la corrompre.

> 工作台的修复是一个单一的验证门控,读取 代理 已产生的工件并做出判断──门控是确定性的──门控在版本控制中──门控连接CI── 代理 无法它──

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

## Le concept de base.

```mermaid
flowchart TD
  Diff[Diff] --> Gate[verify_agent.py]
  Scope[scope_report.json] --> Gate
  Rules[rule_report.json] --> Gate
  Feedback[feedback_record.jsonl] --> Gate
  Gate --> Verdict[verification_report.json]
  Verdict --> Pass{passed?}
  Pass -- yes --> Review[Reviewer Agent]
  Pass -- no --> Refuse[refuse done + surface to human]
```


> **【中文解读】**验证门在 Agent 执行的关键节点插入自动检查──常见验证门:(1) 编译检查代码修改后必须通过编译;(2) 测试检查提交前必须通过相关测试;(3) Lint 检查代码必须符合风格规范;(4) 安全检查必须引入已知漏洞──验证门防止错积――

### Ce que vérifie la porte

| Check | Source artifact | Severity |
|-------|-----------------|----------|
| All acceptance commands ran | `feedback_record.jsonl` | block |
| All acceptance commands exited zero | `feedback_record.jsonl` | block |
| Scope check has no forbidden writes | `scope_report.json` | block |
| Scope check has no off-scope writes | `scope_report.json` | block or warn |
| All block-severity rules pass | `rule_report.json` | block |
| No `null` exit codes in feedback | `feedback_record.jsonl` | block |
| Touched files match `scope.allowed_files` | both | warn |

Une .`warn`la conclusion annotera le verdict; a `block`trouver des obstacles `passed: true`- Je suis désolé .

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

### Déterministique, non probabiliste

La porte doit produire le même verdict pour le même artefact mis à jour à chaque fois. Aucun juge LLM. Les juges LLM appartiennent au côté de l'examen (phase 14 · 39) où l'objectif est une évaluation qualitative, pas le statut.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

### Un rapport, un chemin

La porte en émet une .`verification_report.json`par tâche, écrit sous `outputs/verification/<task_id>.json`La CI consomme le même chemin, plusieurs portes avec des chemins différents forge la source de la vérité.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

### Renier sans exception

Les résultats de la gravité des blocs ne peuvent être annulés par l'agent.`override_reason`et une `overridden_by`L'annulation est un changement signé, pas une décision de l'agent.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

## Construisez-le et mettez-le en œuvre.
```figure
wb-gate-sequence
```

## Faites-le

`code/main.py`les implémentations:

- Un chargement pour chaque produit, tous enduits localement pour que la leçon soit autonome.
- Une .`verify(task_id, artifacts) -> VerdictReport`fonction pure.
- Une imprimante qui affiche les résultats par vérification et le résultat final.
- Une démo avec trois scénarios de tâches: passer clair, creep scope, absence d'acceptation.

- Je vais le faire.

```
python3 code/main.py
```

Résultat: trois rapports de verdict, chacun enregistré à côté du script.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

## Modèles de production dans la nature

Quatre modèles élèvent la porte d'un "autre travail de laine" à "le bord décisif".

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

**Defense-in-depth, not single gate.**Chaque couche est déterministe, de sorte qu'une défaillance dans une couche est prise par la suivante. Le manuel de jeu de mars 2026 de microservices.io est explicite: le crochet pré-commit est non-passageable parce que, contrairement à une compétence côté modèle, il ne dépend pas de l'agent suivant les instructions.

**Defense by deterministic check, model-judge only for nuance.**L'appariement de la norme hybride 2026 d'Anthropic: récompenses vérifiables (tests d'unités, vérifications de schéma, codes de sortie) répondent " le code a-t-il résolu le problème ? "  Les rubriques du LLM répondent " le code est-il lisible, sécurisé, en style ? " La passerelle exécute la première classe; le réviseur (phase 14 · 39) exécute la seconde. Le mélange des deux effondre le signal.

**Signed override log, not Slack threads.**Chaque dépassement émet une ligne dans `outputs/verification/overrides.jsonl`avec: timestamp, code de recherche, raison, utilisateur signé, engagement HEAD actuel. Le temps d'exécution refuse toute annulation qui manque de signature; la piste d'audit est git-tracked. C'est la ligne entre une politique d'annulation et un théâtre d'annulation.

**Coverage floor as a first-class check.**Une .`coverage_report.json`Il est alimenté par un`coverage_floor`(par défaut 80%) vérification. La passerelle échoue si la couverture mesurée tombe en dessous du sol ou en dessous du sol de la fusion précédente de plus de 1 point de pourcentage.

**`--strict` mode promotes warns to blocks.**Pour les branches de libération, les relations publiques de blocage des navires ou le tri après incident, `--strict`Le drapeau est opt-in par branche, pas le défaut mondial, parce que strict-on-tout corrodant le flux quotidien.

## Utilisez-le avec le cadre de réalisation

Modèles de production:

- **CI step.**Une .`verify_agent`Le travail de l'agent s'enfuit contre les objets finaux.`passed: true`- Je suis désolé .
- **Pre-handoff hook.**L'agent appelle la porte avant de générer le document.
- **Manual triage.**Les opérateurs lisent le rapport quand un agent prétend réussir et un humain le soupçonne.

La porte est le bord décisif du flux de la table de travail.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

## Envoyez-le . Produit .

`outputs/skill-verification-gate.md`les câbles de la passerelle dans un projet spécifique: quelles commandes d'acceptation le nourrissent, quelles règles sont sévères, quelles écritures hors champ sont tolérées, comment le journal d'audit de suppression est stocké.

> 验证门(Verification Gates) est un point de contrôle de chaque étape de l'agent 工作流.

## Les exercices

1. Ajouter un `coverage_floor`vérification: la commande d'essai doit produire un rapport de couverture d'au moins 80%. Détermine quel artefact porte le sol.
  Le mot "exercer" est traduit par "exercer".
2. Soutenir un`--strict`mode qui favorise chaque `warn`à `block`- documenter les cas où le mode strict est le bon par défaut.
  Le mot "exercer" est traduit par "exercer".
3. Faites en sorte que la passerelle produise un résumé Markdown en plus de JSON. Défendre quels champs appartiennent au résumé.
  Le mot "exercer" est traduit par "exercer".
4. Ajouter un `time_since_last_human_touch`vérification: tout fichier modifié dans les 60 secondes suivant une pression de touche humaine est exempté de drapeaux hors champ d'application.
  Le mot "exercer" est traduit par "exercer".
5. Il faut utiliser un agent réel différent de votre produit.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Verification gate | "The check that stops things" | Deterministic function over workbench artifacts producing a pass/fail verdict |  |
| Block severity | "Hard fail" | A finding that prevents `passed: true` and requires a signed override |  |
| Override log | "Why we let it through" | Signed entries with reason and user id, audited by review |  |
| Acceptance command | "The proof" | A shell command whose zero exit is what `done` means |  |
| One report path | "Source of truth" | `outputs/verification/<task_id>.json`, consumed by CI and humans alike |  |

## Encore une lecture

- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI Agents SDK guardrails](https://platform.openai.com/docs/guides/agents-sdk/guardrails)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [microservices.io, GenAI dev platform: guardrails](https://microservices.io/post/architecture/2026/03/09/genai-development-platform-part-1-development-guardrails.html) défense en profondeur entre pré-engagement et CI
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [ICMD, The 2026 Playbook for Agentic AI Ops](https://icmd.app/article/the-2026-playbook-for-agentic-ai-ops-guardrails-costs-and-reliability-at-scale-1776661990431) échelle de porte d'approbation (projet → approbation → auto en dessous des seuils)
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Type-Checked Compliance: Deterministic Guardrails (arXiv 2604.01483)](https://arxiv.org/pdf/2604.01483) Lean 4 comme limite supérieure de la délimitation déterministe
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [logi-cmd/agent-guardrails — merge gate spec](https://github.com/logi-cmd/agent-guardrails) portée + portes de test de mutation
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Guardrails AI x MLflow](https://guardrailsai.com/blog/guardrails-mlflow) validateurs déterministes en tant que scoreurs d'IC
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Akira, Real-Time Guardrails for Agentic Systems](https://www.akira.ai/blog/real-time-guardrails-agentic-systems) Ports de pré/post-outil
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- Phase 14 · 27  Défense à injection rapide (parue de la porte)
- Phase 14 · 36  le contrat de portée que cette porte impose
- Phase 14 · 37  le journal de rétroaction ce portail marque
- La phase 14 · 39  l'agent d'examen le portail se déplace à
