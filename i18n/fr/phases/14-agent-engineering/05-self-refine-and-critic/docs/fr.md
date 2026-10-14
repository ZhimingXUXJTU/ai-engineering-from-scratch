# Autorefinition et critique: amélioration iterative de la sortie .

> Self-Refine (Madaan et coll., 2023) utilise un LLM dans trois rôles  générer, rétroaction, affiner  dans une boucle. Gain moyen: +20 absolu sur 7 tâches. CRITIC (Gou et coll., 2023) durcit l'étape de rétroaction en routant la vérification via des outils externes. En 2026, ce modèle se déploie dans chaque cadre comme un "évaluateur-optimisateur" (Anthropic) ou une boucle de garde (OpenAI Agents SDK).

> **【中文解读】**L'auto-réfinition 让一个LLM 扮演三个角色:生成、反、精炼,循环改进──7 个任务平均提升 20 个百分点──CRITIC 将验证步骤通过外部工具(搜索、代码解释器、计算器) être renforcée──2026 ans, il est devenu l'élément d'un cadre.

> **【拓展：CRITIC → Claude Code 的自我修复】**Claude Code dans la rédaction du code se comporte automatiquement après test test test 证 c'est la réalisation de la production du mode CRITIC

>  **【前置】**必須先過:Phase 14·01(Agent Loop) et Phase 14·03(Réflexion)。Self-Réfinition est la version de Réflexion de la "单次任务内" ̇Réflexion 跨多次试验,Self-Réfinition en une seule génération内代)。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Les trois instructions de l'État Self-Refine (générer, rétroaction, affiner) et expliquer pourquoi l'histoire est importante pour le prompt de raffinage.
  Je suis en train de vous expliquer pourquoi le récit historique de l'élimination de la peau est important.
- Expliquez l'idée critique de CRITIC: les LLM ne sont pas fiables pour l'auto-vérification sans fondement externe.
  Le mot "expert" est traduit par "expert".
- Implémenter une boucle stdlib Self-Refine avec l'historique et un vérificateur externe optionnel.
  Traduction anglaise: avec la bibliothèque de normes pour réaliser le cycle de l'auto-réfinition avec les enregistrements historiques et les vérificateurs externes choisis.
- Mettez ce schéma dans le flux de travail "évaluateur-optimisateur" d'Anthropic et les barreaux de sortie du SDK OpenAI Agents.
  Le modèle est projeté dans les flux de travail et les résultats de OpenAI Agents SDK.

## Le problème , l' introduction du problème

Un agent produit une réponse presque correcte. Peut-être qu'une ligne de code a une erreur de syntaxe. Peut-être qu'un résumé est trop long. Peut-être qu'un plan manque un cas d'extrémité. Ce que vous voulez, c'est: l'agent critique sa propre sortie, puis la corrige.

> L'agent  a produit une réponse presque exacte ⋅ peut-être une ligne de code avec une faille de langage ⋅ peut-être le résumé est trop long ⋅ peut-être un plan a laissé tomber la situation de bord ⋅ vous voulez: l'agent  critique sa propre sortie, puis la répare ⋅

Autorefinement montre que cela fonctionne avec un seul modèle, pas de données de formation, pas de RL. Mais il y a un problème: les LLM sont mauvais à l'auto-vérification sur des faits concrets.

> L'auto-réfinition a prouvé que cela fonctionne avec un seul modèle, sans besoin de formation, sans besoin de RL. Mais il y a un problème: la capacité de vérification de soi de l'LLM sur la réalité dure est très faible.

Ensemble, ces deux documents définissent la norme par défaut de 2026 pour l'amélioration itérative: générer, vérifier (externellement lorsque cela est possible), affiner, arrêter lorsque le vérificateur passe.

> Ces deux articles définissent ensemble le modèle de mise à niveau de la génération 2026: génération, expérience, expérience extérieure, expérience, élaboration, expérience, etc.

> **【中文解读】**Le concept central de l'auto-réfibrillation: un modèle qui joue le rôle de générateur, critiqueur, éliteur, trois rôles. Mais le programme de révision de l'auto-réfibrillation en réalité difficile est de faire l'objet d'une réévaluation par des outils externes.

## Le concept de base.

### Autorefinition (Madaan et coll., NeurIPS 2023)

Un LLM, trois rôles:

> Un LLM, trois rôles:

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

Détail clé:`refine`Le document ablè ce point: l'historique de la chute et la qualité de la chute sont nettement.

>  **【类比】**Autodéfinition 像写论文的"自改稿"流程:第一稿(genérer)→ 通读找问题(feedback)→ 按问题改第二稿(refiné, mais à regarder dans le premier稿和批注改, sinon il va重复同样错)→ 再找问题→再改──**关键**Chaque fois que l'on finit, il faut mettre ensemble les traits et les lots, sinon le modèle "oubliera le problème de la ronde supérieure" et tombera dans le cycle.

> ️ **【易错点】**常见 bug: "On ne fait que donner une sortie à la fin, pas de rétroaction"".**后果**:refine 后的输出重新引入反见指出的问题,陷入"指出问题→改→再指出→再改"的死循环──**一行修复**- Le numéro de la liste:`refine_prompt = task + output_0 + critique_0 + output_1 + critique_1 + ... + output_n`L'histoire doit être entièrement transmise.

> Je suis en train de faire une petite histoire.`refine`能看到完整历史所有前来的输出和批评因此不会重复错误──论文对此进行消融实验:删除历史记录后质量急剧下降──

Titre: +20 amélioration absolue moyenne sur 7 tâches (mathématiques, code, acronyme, dialogue) y compris GPT-4.

> 核心数据: sur 7 tâches (mathematics, code, abréviation, dialogue) une moyenne absolue de 20 points de percentile est augmentée, y compris GPT-4―.

### CRIQUE (Gou et coll., arXiv:2305.11738, v4 février 2024)

La faiblesse de l'auto-réfinition: l'étape de rétroaction est un LLM en soi. Pour les affirmations factuelles, cela est peu fiable (une hallucination semble souvent convaincante pour le modèle qui l'a produite).`feedback(task, output)`avec `verify(task, output, tools)`où `tools`comprend:

> La faiblesse de l'auto-réfiguraison: les contre-étapes sont des LLM qui donnent leur propre avis.`verify(task, output, tools)`替代 `feedback(task, output)`, parmi lesquels `tools`Les éléments suivants:

- Un moteur de recherche pour des affirmations factuelles.
  Le mot de passe est utilisé pour la recherche de déclarations de faits.
- Un interprète de code pour la correction du code.
  Pour les explicateurs de code.
- Une calculatrice pour l'arithmétique.
  Pour le calcul de l'arithmétique.
- Les vérificateurs spécifiques à un domaine (essais unitaires, vérificateurs de type, linters).
  Le code de contrôle est un code de contrôle.

Le vérificateur produit une critique structurée basée sur les résultats des outils.

> Les tests sont effectués en fonction des résultats de l'analyse structurée.

Titre: CRITIC dépasse Auto-Réfinition sur les tâches factuelles parce que la critique est basée.

> 🤔 **【困惑】**Q: 既然 CRITIC préfère l'auto-réfinition 强, pourquoi ne pas utiliser CRIQUE ? A: Parce que le CRITIC dépend des outils externes ((recherche, code interprète, unité de test) ⋅创意写作、邮件色**事实类用 CRITIC，创造类用 Self-Refine**Il y a une autre.

> 核心数据:CRITIC sur les tâches factuelles dépassant l'auto-réfinition, car la critique est basée sur la

### Condition d'arrêt

Deux formes communes:

> 两种常见形式:

1. **Verifier passes.**Les tests externes donnent le résultat. préférentiel lorsque cela est possible (essais d'unité, vérificateur de type, affirmation de barrière).
   Le mot grec traduit par " le mot grec "**验证器通过。**Le test est effectué en fonction de la taille de l'appareil.
2. **No feedback issued.**Le modèle dit "la sortie est bonne". Cheap mais peu fiable; coupler avec un capot d'iteration maximale.
   Le mot grec traduit par " le mot grec "**无反馈发出。**模型说"输出没问题"──更便宜但不可靠;配合最大代次数上限──

2026 par défaut: les combiner. " Arrêtez si le vérificateur passe OR modèle dit bien ET itérations >= 2 OR itérations >= max_iterations. "

> 2026 "Si l'équipe de test est passée, ou le modèle dit pas de problème et le nombre de fois >= 2, ou le nombre de fois >= maximal, alors cesse !"

### Évaluateur-optimisateur (Anthropic, 2024)

Le post de décembre 2024 d'Anthropic l'appelle l'un des cinq modèles de flux de travail.

> L'article de l'Anthropic 2024 du 12 décembre sera nommé comme l'un des cinq modes de travail.

- Évaluateur: note la production et produit une critique.
  Le groupe de travail est composé de deux groupes de travail.
- Optimisateur: révise la sortie en raison de la critique.
  Le référencement est le plus souvent utilisé dans les langues anglaises.

La conception de l'analyse est un processus de révision de la structure de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de la analyse de la recherche.

> 循环直到评估器通过──这是Anthropic 框架下自精/CRITIC──Anthropic 添加的关键工程细节:评估器和优化器提示应该有实质性差异,以免模型只是皮图章──

### Garde-roue de sortie OpenAI Agents SDK

Un protecteur est un validateur qui fonctionne sur la sortie finale d'un agent.`OutputGuardrailTripwireTriggered`Les gardages peuvent appeler des outils (au style CRITIC) ou être des fonctions pures (au style Auto-Réfinition).

> Le SDK OpenAI Agents va utiliser ce modèle comme "输出护" fournir.`OutputGuardrailTripwireTriggered`),输出被拒绝,Agent peut être réessayer.

### 2026 pièges

- **Rubber-stamp loops.**Le même modèle de génération et de critique avec le même style de prompt converge sur "il me semble bien". Utilisez des instructions structurellement différentes, ou un modèle moins cher pour critiquer.
  Le mot grec traduit par " le mot grec "**橡皮图章循环。**Le même modèle utilise le même style de proposition pour générer et critiquer les résultats jusqu'à "sembler pas mal" ⋅ utiliser des suggestions structurelles différentes, ou utiliser des modèles plus petits et moins chers ⋅ critiquer.
- **Over-refinement.**Chaque passe de raffinage ajoute de la latence et des jetons.
  Le mot grec traduit par " le mot grec "**过度精炼。**Chaque élaboration augmente le retard et le jeton.
- **CRITIC on trivial tasks.**Si il n'y a pas de vérificateur externe, CRITIC dégénère en Auto-Réfinition; ne payez pas la latence pour un vérificateur de stub.
  Le mot grec traduit par " le mot grec "**在简单任务上使用 CRITIC。**Si vous n'avez pas de vérificateur externe, le CRITIC est dédié à l'auto-réfinition; ne payez pas de retard pour le vérificateur.

## Construisez-le et mettez-le en œuvre.
```figure
self-refine
```

## Faites-le

`code/main.py`Il implique Auto-Réfinition et CRITIC sur une tâche de jouet: produire une courte liste de balles donnée à un sujet. Le vérificateur vérifie le format (3 balles, chacune inférieure à 60 chars).

> `code/main.py`Dans une tâche de jouet, réaliser l'auto-réfinition et la critique: donner un sujet déterminé générer une liste courte.

Components:

> 组件:

- `generate`- Producteur du scénario.
  Le mot grec traduit par " le mot grec "`generate`脚本生成器──
- `feedback` Autoscritie au style de la maîtrise de la loi.
  Le mot grec traduit par " le mot grec "`feedback`LLM 风格自我批评──
- `verify_external` vérificateur fondé de style CRITIC.
  Le mot grec traduit par " le mot grec "`verify_external`CRITIC 风格 定验器──
- `refine` réécrit l'expérience de sortie donnée.
  Le mot grec traduit par " le mot grec "`refine` Selon l'histoire
- Condition d'arrêt  passe de vérificateur ou max 4 itérations.
  Le test est effectué à l'aide d'un test de dépistage.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

Comparer les tests Auto-réfinition versus CRITIC. CRITIC capture une erreur factuelle Auto-réfinition manquée parce que le vérificateur externe a mis à terre l'auto-critique ne le fait pas.

> Comparer l'auto-réfiguraison et la critique 运行──CRITIC  Capture l'auto-réfiguraison 遗漏 fact error, parce que les vérificateurs externes possèdent une base définitive de l'auto-réfiguration 

## Utilisez-le avec le cadre de réalisation

L'optimisateur d'évaluation d'Anthropic est ce modèle dans le langage convivial à Claude. Les barreaux de sortie du OpenAI Agents SDK sont en forme de CRITIC (les barreaux peuvent appeler des outils). LangGraph envoie un nœud de réflexion qui se lit comme Self-Refine. L'utilisation de l'ordinateur Gemini 2.5 de Google ajoute un évaluateur de sécurité à chaque étape qui est une variante CRITIC: chaque action est vérifiée avant de se commit.

> L'analyseur-optimisateur de l'anthropique est utilisé par Claude Friendly Language. Le modèle de production de l'OpenAI Agents SDK est un outil de forme critique.

## Envoyez-le . Produit .

`outputs/skill-refine-loop.md`Configure une boucle d'évaluation-optimisateur en fonction de la forme de la tâche, de la disponibilité du vérificateur et du budget d'itération. Émet des requêtes pour le générateur, l'évaluateur/ vérificateur et l'optimisateur, ainsi qu'une politique d'arrêt.

> `outputs/skill-refine-loop.md`En fonction de la forme de la tâche, la disponibilité du testateur et le cycle de l'évaluation des budgets de la configuration du testateur-optimisateur, les conseils de l'appareil de formation, de l'évaluation du testateur/testateur et de l'optimisateur ainsi que les stratégies de mise en place de l'appareil.

## Les exercices

1. Exécutez le jouet avec max_iterations=1.
   Le texte est en français.
2. Le système de vérification externe doit être remplacé par un vérificateur bruyant (faux positifs aléatoires de 30%).
   Le cycle de test est un processus qui se poursuit jusqu'à la fin de l'année 2026.
3. Implémenter une variante "critique génératrice sur différents modèles": génère des modèles de grande taille, critique de modèles de petite taille.
   Le modèle est-il meilleur que le modèle ?
4. Lisez la section 3 de CRITIC (arXiv:2305.11738 v4). Nommez les trois catégories d'outils de vérification et donnez un exemple pour chacune.
   Le texte de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième de la deuxième partie de la deuxième partie de la deuxième de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième de la deuxième partie de la deuxième partie de la deuxième de la deuxième partie de la deuxième partie de la deuxième de la deuxième partie de la deuxième de la deuxième partie de la deuxième de la partie de la deuxième de la partie de la deuxième de la partie de la deuxième de la partie de la partie de la deuxième de la partie de la deuxième de la partie de la deuxième de la partie de la partie de la deuxième de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de
5. La carte OpenAI Agents SDK `output_guardrails`Qu'est-ce qui ne va pas avec le SDK, et qu'est-ce qui va bien ?
   Le code de défense de l' organisation`output_guardrails`Le rôle du testateur de la critique.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## Encore une lecture

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) le papier canonique
  Le récit de la rédaction de la Bible est le récit de la rédaction de la Bible.
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) vérification fondée sur des outils
  Le mot "critique" est traduit par "critique".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) modèle de flux de travail évaluateur-optimisateur
  Traduction anglaise:Anthropique 关于构建有效代理的指导评估器-优化器工作流模式──
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) barreaux de sortie en tant que vérificateurs en forme de CRITIC
  Le code de défense de l'information est un code de défense de l'information.
