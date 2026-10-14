# Les critères: SWE-bench, GAIA, agentBench

> Trois critères de référence évaluation des agents d'ancrage en 2026. SWE-bench teste le patchage de code. GAIA teste l'utilisation des outils généralistes. AgentBench teste le raisonnement multi-environnement. Connaître leur composition, leur histoire de contamination et ce qu'ils ne mesurent pas.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Nommez le harnais d'essai du banc SWE (FAIL_TO_PASS) et expliquez pourquoi il est exempt des tests unitaires.
- Expliquez pourquoi SWE-bench Verified (OpenAI, 500 tâches) existe et ce qu'il supprime.
- Décrivez la conception de GAIA: simple pour les humains, difficile pour l'IA; trois niveaux de difficulté.
- Nommez les huit environnements d'AgentBench et son principal bloqueur pour les LLM open source.
- Résumez la constatation de contamination du banc SWE+ et ses implications.

## Le problème , l' introduction du problème

Les classements vous indiquent quel modèle gagne sur un critère de référence.

> Le classement vous dit quel modèle gagne sur un certain niveau.

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

- Si le point de référence est contaminé (résolutions dans les données de formation, fuite de test).
- Si le benchmark mesure ce qui vous intéresse (code vs navigation vs généraliste).
- Si l'évaluateur est robuste (conformité AST, vérification de l'état, examen humain).


> **【中文解读】**SWE-bench et GAIA sont les deux plus importants de l'année 2026 Agent 能力基准。SWE-bench 评估 Agent 修复真实GitHub issue 能力软件工程)。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题能力──通用推理──两者共同定义了 Agent 能力边界──

> **{【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】}**Le SWE-bench (Princeton, 2023) contient 2 294 vrais problèmes GitHub, Agents 必须在真实代码库中定位 bug、编写修复并通过测试──2026年 SOTA  72% 解决率(OpenAI's Codex)──GAIA (Meta, 2023)  466 问题需要 web 搜索、文件处理、代码执行等工具──人类平均 92%,最佳 Agent 约70%──
Connaître les trois indicateurs d'ancrage et leurs modes d'échec avant de citer un nombre.

> Avant de citer les données, il faut d'abord comprendre ces trois tests de base et leur mode de défaillance.

>  **【前置】**建议先过:Phase 14·06(Utilisation des outils)  comprendre comment l'agent utilise les outils 是看懂 GAIA's prémisse; ainsi que les "méthodoses d'évaluation de la machine learning" fondamentales  précision/reprise、contamination DATA污染)  test set leakage── si vous citez un modèle de référence mais ne savez pas ce qu'est la contamination,本节必须学──

## Le concept de base.

### SWE-bench (Jimenez et coll., ICLR 2024 orale)

- 2 294 problèmes réels de GitHub provenant de 12 repositories Python populaires.
- L'agent obtient: la base de code à la préfix commit + description du problème en langage naturel.
- L'agent produit un patch.
- Évaluateur: appliquer le correctif, exécuter la suite de tests du repo. Le correctif doit faire revenir les tests FAIL_TO_PASS (anciennement échecs, maintenant réussissant) sans casser les tests PASS_TO_PASS.

SWE-agent (Yang et coll., 2024) a atteint 12,5% à la sortie en mettant l'accent sur les interfaces agent-ordinateur (commandes de l'éditeur de fichiers, syntaxe de recherche que le modèle comprend).

>  **【类比】**SWE-bench 像考"开卷实操": donner à l'agent une vraie code library(开卷) 、 un problème 描述(考题) 、一套现有单元测试(评分标准) ✿**关键设计**:测试用 FAIL_TO_PASS(修复前失败、修复后通过) + PASS_TO_PASS(c'est pas possible de détruire une fonction déjà existante), du certain "rectifier A 破了 B" de faux passage。

> SWE-agent ((Yang 等,2024) atteint 12,5% au moment de la publication, en mettant l'accent sur l'interface de l'agent-ordinateur ((文件编辑器命令、模型能理解的搜索语法) ]]

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

### Banque SWE vérifiée

OpenAI, août 2024. sous-ensemble de 500 tâches géré par l'homme. Élimine les problèmes ambiguës, les tests peu fiables et les tâches où la correction n'était pas claire.

> OpenAI, août 2024. ⋅ 500 tâches de planification artificielle ⋅ élimination de problèmes flou ⋅ test non fiable et réparation de tâches non précises ⋅ " Votre agent ⋅ peut-il livrer des correctifs réels ? "

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

### Contamination

- Plus de 94% des émissions de banque SWE précèdent la plupart des coupes de modèle.
- **SWE-bench+**Il a été constaté que 32,67% des correctifs réussis ont vu des solutions fuites dans le texte de l'émission (le modèle a vu la correction dans la description), et 31,08% étaient suspects en raison de la faible couverture des tests.
- Il est plus propre, mais pas sans contamination.

Implication pratique: un modèle qui obtient 50% de score sur le banc SWE peut obtenir 35% sur le banc SWE+. Rapporte toujours les deux si vous revendiquez des performances sur le banc SWE.

> ️ **【易错点】**引用 SWE-bench 分数时不提 Vérifie/SWE-bench+。**后果**Le problème est que les données de l'analyse de l'analyse de données sont très différentes.**一行修复**: tout citation SWE-bench numéros, doit être donné simultanément Verified 子集分数和 SWE-bench+(去污染版)分数,注明数据来源日期。

>  réel impact: un modèle dans le SWE-bench à 50% de score dans le SWE-bench+ 上可能只得到 35%──

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

### GAIA (Mialon et coll., novembre 2023)

- 466 questions; 300 ont été conservées pour le classement privé à huggingface.co/gaia-benchmark.
- Philosophie de conception: "conceptuellement simple pour les humains (92%) mais difficile pour l'IA (GPT-4 avec plugins: 15%)."
- Tests de raisonnement, de multi-modalité, de web, d'utilisation des outils.
- Trois niveaux de difficulté; le niveau 3 nécessite de longues chaînes d'outils sur les différentes modalités.

GAIA est ce que vous utilisez pour mesurer la "capacité généraliste". Ne la confond pas avec des critères de référence spécifiques au code.

> La GAIA est utilisée pour mesurer les bases de la "capacité générale".

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

### L'agent Bench (Liu et coll., ICLR 2024)

- 8 environnements à travers le code (Bash, DB, KG), les jeux (Alfworld, LTP), le web (WebShop, Mind2Web) et la génération ouverte.
- Multi-tours, environ 4K-13K de tours par partage.
- Résumé: Le raisonnement à long terme, la prise de décision et l'instruction suivantes sont les obstacles aux LLM OSS qui arrivent à la commercialisation.

### Ce que ces mesures ne mesurent pas

- Coût opérationnel réel (tokens, horloge murale).
- Comportement de sécurité dans des conditions adverses.
- Performance sur votre domaine (utilisez vos propres évaluations, leçon 30).
- Les défaillances de la queue (moyenne des points de référence; les opérateurs de production s'occupent des 1% les plus graves).

### Lorsque l'analyse comparative se trompe

- **Single-number fixation.**Le SWE-bench 50% vous indique moins que le coût P50/P75/P95 + distribution étape.
- **Contaminated claims.**Le fait de déclarer le benchmark SWE sans mentionner le benchmark Verified ou le benchmark SWE+ est trompeur.
- **Benchmark-as-development-target.**L'optimisation pour le point de référence diffère de l'utilité de la production.

> 🤔 **【困惑】**Q: SWE-bench Verified 上 70% + du modèle est sorti, est-ce que le logiciel d'ingénieur doit être au chômage ? A: 还早──三个原因:(1) Le problème du SWE-bench est un problème bien formé de "有明确测试用例、有清晰复现路径", 50% du problème en production n'est pas satisfait;(2) 70% signifie que pour chaque 3 tâches 1 失败, le coût de la réparation de l'environnement de production échoue est bien supérieur au bénéfice de la réparation réussie;(3)**生产代码库比 SWE-bench 的 12 个开源 Python 仓库复杂得多** private code 跨语言 几十年遗留代码──Le niveau de référence supérieur de 70% n'est pas égal à celui de l'environnement de production de 70%──

> **单一数字执念。**SWE-bench 50%  Dites votre information est inférieur à P50/P75/P95 成本 + 步骤分布──
> **污染声明。**报告 SWE-bench 时不提及 Verifié ou SWE-bench+ est une erreur de conduite.
> **基准作为开发目标。**Pour la base de l'optimisation, la production est détachée de l'utilité pratique.

## Construisez-le et mettez-le en œuvre.
```figure
ae-swebench-gate
```

## Faites-le

`code/main.py`met en place un harnais de jeu SWE-bench:

> `code/main.py` réaliser un outil de test de jouets similaire à SWE-bench:

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

- Les tâches de correction de bugs synthétiques (3 tâches).
- Un "agent" avec un script qui propose des correctifs.
- Un test qui vérifie FAIL_TO_PASS (bug maintenant corrigé) et PASS_TO_PASS (rien cassé).
- Un classificateur de difficulté de style GAIA basé sur la profondeur de la décomposition des questions.

- Je vais le faire.

```
python3 code/main.py
```

La sortie montre le taux de résolution par tâche + par difficulté et rend les règles de l'évaluateur concrètes.

> output montre le taux de résolution de chaque tâche et de chaque niveau de difficulté, et rend les règles de l'évaluateur concrétisées.

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

## Utilisez-le avec le cadre de réalisation

- **SWE-bench Verified**Pour les agents de code, rapportez toujours les scores vérifiés.
- **GAIA**Pour les agents généralistes, utilisez la division privée.
- **AgentBench**pour la comparaison multi-environnement.
- **Custom evals**(Létion 30) pour la forme réelle de votre produit.

## Envoyez-le . Produit .

`outputs/skill-benchmark-harness.md`construit un harnais de style SWE-bench pour toute paire de tâches de base de code avec une fermeture FAIL_TO_PASS / PASS_TO_PASS.

> `outputs/skill-benchmark-harness.md`Pour toute base de code, la tâche consiste à construire un outil de test de style SWE-bench, avec FAIL_TO_PASS / PASS_TO_PASS 门控──

> SWE-bench et GAIA sont les deux bases de base de la capacité de l'agent. SWE-bench évalue la capacité de réparation de code, GAIA évalue la capacité de raisonnement générale.

## Les exercices

1. Portez le harnais de jouet pour qu'il fonctionne sur un réel repo (en choisissez un de vos).
  Le mot "exercer" est traduit par "exercer".
2. Pour les 3 tâches, combien d'acteurs par résolution ?
  Le mot "exercer" est traduit par "exercer".
3. Lire le document SWE-bench+.Mettre en œuvre une vérification de fuite de solution (parallèlement du modèle du texte de la question par rapport au diff).
  Le mot "exercer" est traduit par "exercer".
4. Téléchargez une question de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de la recherche sur la recherche et de la recherche sur le suivi du public.
  Le mot "exercer" est traduit par "exercer".
5. Lisez l'analyse de l'agent Bench sur l'environnement, quel environnement reflète la surface de votre produit, à quoi ressemble le "SOTA" ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| SWE-bench | "Code agent benchmark" | 2,294 GitHub issues; patch must flip FAIL_TO_PASS tests |  |
| SWE-bench Verified | "Clean SWE-bench" | 500 human-curated tasks, OpenAI |  |
| FAIL_TO_PASS | "Fix gate" | Tests previously failing that must pass after the patch |  |
| PASS_TO_PASS | "No-regression gate" | Tests that were passing and must still pass |  |
| GAIA | "Generalist benchmark" | 466 human-easy / AI-hard multi-tool questions |  |
| AgentBench | "Multi-env benchmark" | 8 environments; long-horizon multi-turn |  |
| Contamination | "Training-set leak" | Benchmark tasks present in model training |  |
| SWE-bench+ | "Contamination audit" | 32.67% solution leakage found in successful SWE-bench patches |  |

## Encore une lecture

- [Jimenez et al., SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) l'indice de référence initial
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) le sous-ensemble sélectionné
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Mialon et al., GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) référence générale
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Liu et al., AgentBench (arXiv:2308.03688)](https://arxiv.org/abs/2308.03688) suite multi-environnement
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
