# AlphaEvolve  Agents de codage évolutif  AlphaEvolve  Agents de codage évolutif

> Associer un modèle de codage frontalier avec une boucle évolutionnaire et un évaluateur vérifiable par machine. Laissez la boucle fonctionner assez longtemps. Il découvre une procédure de multiplication de matrice complexe 4x4 qui utilise 48 multiplication escalare  la première amélioration sur Strassen en 56 ans. Il trouve également une heuristique de planification Borg à l'échelle de Google qui récupère ~ 0,7% du calcul de cluster en production. L'architecture est ennuyeuse à dessein. Les gains viennent de la rigueur de l'évaluateur.

> **【中文解读】**Il a également trouvé un système de réglage de Borg global de Google, qui a permis de récupérer environ 0,7% de la production en calcul collectif. La structure est intentionnellement conçue pour être sèche, les gains sont dus à la rigueur de l'évaluateur.

> **【拓展：进化算法 + LLM 的化学反应】**L'algorithme d'évolution (algorithme d'évolution) a une histoire de plusieurs décennies, mais la tradition de l'évolution avec des grandes variantes de processus produit presque toujours des erreurs de langage. L'algorithme de changement intelligent a changé ce point: il peut proposer des modifications rationnelles à la compilation, en termes de langage. L'innovation clé d'AlphaEvolve repose sur cette proposition de l'ALLM, la décision de l'évaluateur.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les étudiants, il est nécessaire de se préparer à la phase 15 de la formation.
>  **【类比】**AlphaEvolve = "AI 实验室里的博士生群体"。传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群 AI 博士生,每个人都提出有意义的修改("试试把循环展开两倍"),évaluateur跑实验打分,高分修改进入下一代种群。LLM 解决"如何提出合理变异",évaluateur解决"如何辨别伪"结合 56 ans de première percée Strassen 矩阵乘法。
> 🤔 **【困惑】**Q: Pourquoi AlphaEvolve peut-il dépasser les spécialistes humains? Parce qu'il fonctionne des millions de fois, chaque fois avec des véritables critères de référence  validation.

## Le problème , l' introduction du problème

Les grands modèles de langage peuvent écrire du code. Les algorithmes évolutionnaires peuvent rechercher le code. Les deux ont été testés séparément pendant des décennies; les deux atteignent des plafonds.

> Les modèles de langage peuvent rédiger du code, les algorithmes évolués peuvent être recherchés dans l'espace de code.

Le plafond de la LLM est une confabulation: le modèle écrit un code plausible qui ne fait pas ce qu'il prétend. Le plafond évolutionnaire est le coût de recherche: les mutations aléatoires sur la syntaxe produisent rarement des programmes compilables, encore moins de meilleurs.

> Le plancher de l'LLM est fictif: le modèle écrit un code qui semble raisonnable mais qui ne correspond pas à un comportement réel.

AlphaEvolve (Novikov et coll., DeepMind, arXiv:2506.13131, juin 2025) les combine. Le LLM propose des modifications ciblées à une base de données de programmes; un évaluateur automatique note chaque variante; les variantes à haut score deviennent des parents pour les générations futures. Le LLM gère la étape coûteuse d'écrire du code plausible; l'évaluateur capture les confabulations.

> AlphaEvolve(Novikov 等人,DeepMind,arXiv:2506.13131,2025 6月) va les combiner.LLM propose une édition ciblée de la base de données de processus; évaluateur automatique de chaque variable; élevé des variables pour devenir le père de la génération future.

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) va mettre en œuvre des algorithmes d'évolution pour l'optimisation des codes. Il maintient une population de processus, en passant par la variation, le transfert et la sélection de l'optimisation.

Les résultats rapportés: 48-scalar-multiplication 4x4 matrice complexe de multiplication (la limite de 1969 de Straßsen était 49), une heuristique de planification Borg dans la production de Google, un 32,5% FlashAttention accélération du noyau, améliorations de la capacité de formation de Gémeaux.

> 報告的結果:48 次标量乘法 4x4 复矩阵乘法(Strassen 1969 年的边界是 49),Google 生产中的 Borg调度启发式,32.5% 的 FlashAttention 内核加速,Gemini 训练吞吐量改进──

L'architecture fonctionne parce que l'évaluateur est vérifiable par machine. Elle ne fonctionne pas là où l'évaluateur n'est pas. Cette asymétrie est la leçon.

> Cette incongruité est au cœur de ce cours: l'architecture est donc efficace, car l'évaluateur est un domaine de contrôle mécanique; l'évaluateur est un domaine de confiance, le cycle est inefficace.

## Le concept de base.

### La boucle de cycle

1. Commencez par un programme de semence `P_0`C'est vrai, mais pas optimal.
   Le programme de semence est vrai mais bon.`P_0`Je commence.
2. Maintient une base de données de programmes variants, chacun marqué par l'évaluateur.
   Le programme est basé sur la base de données de chaque variable.
3. Prenez l'échantillon d'un ou plusieurs parents de la base de données (à la mode MAP-elites ou à l'échelle des îles).
   Le modèle de la carte est le modèle de la carte de la carte.
4. Faites appel au LLM (Gemini Flash pour de nombreux candidats, Gemini Pro pour les plus difficiles) pour produire une variante modifiée du parent.
   Le nombre de candidats à la formation en médecine est de 2,0%.
5. Compiler, exécuter et évaluer la variante sur l'évaluateur de retard.
   Le texte de la loi est écrit en français.
6. Insérer dans la base de données en fonction de son score et de son vecteur de fonctionnalités.
   En français, le nombre et la fréquence de l'élément sont insérés dans la base de données.
7. Je répète.
   Le récit de la première partie de la Bible est le récit de la première partie de la Bible.

Deux détails sont importants. Premièrement, le LLM est invité à plus que le programme parent  généralement plusieurs variantes supérieures de la base de données, plus la signature de l'évaluateur, plus une brève description de tâche. Le travail du modèle est de proposer un changement ciblé qui pourrait améliorer le score. Deuxièmement, la base de données est structurée (réseau de MAP-élites, basée sur l'île) de sorte que la boucle explore la diversité, pas seulement le leader actuel.

> Deux détails sont importants. Premièrement, le projet de programme LLM ne se limite pas à donner aux programmes les plus importants de la base de données, en plus de la signature de l'évaluateur et de la description des tâches courantes.

### Ce qui rend l' évaluateur non négociable

Les victoires d'AlphaEvolve proviennent de domaines où l'évaluateur est rapide, déterministe et difficile à jouer:

> Les victoires d'AlphaEvolve viennent toutes de domaines d'évaluation rapides, déterminants et difficiles à comprendre:

- **Matrix multiplication algorithm**: un test unitaire qui multiplie les matrices et vérifie l'égalité par bits identiques.
  Le mot grec traduit par " le mot grec "**矩阵乘法算法** un test de la même unité de la même une fois en même temps que la même une fois en même temps.
- **Borg scheduling heuristic**: un simulateur de qualité de production qui reproduit la charge historique du groupe et mesure les calculs gaspillés.
  Le mot grec traduit par " le mot grec "**Borg 调度启发式** Un simulateur de production, réétablissant des calculs de l'ensemble des charges et des déchets.
- **FlashAttention kernel**: un test de précision plus une référence de l'horloge murale sur le matériel réel.
  Le mot grec traduit par " le mot grec "**FlashAttention 内核**                                                                                                                                                                                                                                                              
- **Gemini training throughput**: mesurées en GPU-seconde par étape.
  Le mot grec traduit par " le mot grec "**Gemini 训练吞吐量** Mesurer le nombre de GPU par seconde.

Dans chaque cas, l'évaluateur détecte la classe d'erreurs LLM qui domineraient autrement: revendications de précision confabulates, revendications de performance qui disparaissent sur le matériel et défaillances de bord.

> Dans chaque cas, l'évaluateur a capturé le type d'erreur qui dominerait le programme de gestion de la gestion de la gestion de données: fausse déclaration de validité, déclaration de performances qui disparaissent sur le matériel et défaillance des conditions de bord.

### Le piratage des récompenses est l'autre face de cette déclaration.

L'évolution optimise pour tout ce que l'évaluateur mesure. Si l'évaluateur est imparfait, la boucle trouvera l'imperfection. Dans un domaine non vérifié, la boucle optimiserait pour la caractéristique de surface, pas le comportement prévu.

>  évoluer optimiser les caractéristiques de l'appareil d'évaluation  si l'appareil d'évaluation est imparfait, le cycle trouvera des choses imparfaites  dans les domaines non vérifiés, le cycle optimisera les caractéristiques de surface plutôt que les comportements attendus 

DeepMind indique explicitement dans le document: les succès d'AlphaEvolve ne sont transférés que dans des domaines où le rigor de l'évaluateur correspond à l'ambition de la recherche.

> DeepMind a précisé dans son article: "Le succès d'AlphaEvolve ne peut être transféré qu'à un domaine d'évaluation strictement adapté à l'objectif de recherche".

Exemples concrets de piratage des récompenses dans les boucles de recherche de code de 2025 à 2026:

> Exemples spécifiques de changements dans le cycle de recherche des années 2025-2026:

- Les objectifs d'optimisation qui récompensent le "temps de terminer" sont récompensés par la soumission de solutions vides.
  Le prix "Completé le temps" de l'optimisation de l'objectif de l'équipe de récompense de la solution de l'équipe de récompense.
- Les scores de référence qui récompensent les tests de précision sous test récompensés par les tests de mémorisation et les tests de surcodage.
  Traduction anglaise: récompense test correctement
- Un proxy de "qualité du code" récompense en supprimant les commentaires et en réécrivant les noms des variables, sans changement sémantique.
  Traduction anglaise: "code qualité"

La solution dans AlphaEvolve: envoyer un évaluateur qui a été retenu par le LLM, avec des entrées générées au moment de l'évaluation.

> AlphaEvolve: livrer un LLM à partir d'un évaluateur de réserves invisibles, en saisie lors de l'évaluation.

### Pourquoi la recherche de LLM + bat soit seule , pourquoi la recherche de LLM + gagne plus que seul

Le LLM peut produire des modifications comptables et sémantiquement plausibles. Une mutation aléatoire GA sur un fichier Python de 2000 lignes produit presque toujours des erreurs de syntaxe. Le LLM concentre également la recherche sur des quartiers plausibles (changer une fonction, pas des octets aléatoires) ce qui réduit considérablement les appels d'évaluateurs gaspillés.

> L'LLM peut générer des modifications comptables ∞ en termes de logique ∞ en 2000 行 Python 文件随机变异 GA 几乎总产生语法错误∞ LLM va également se concentrer sur des domaines voisins raisonnables ∞ en modifiant une fonction, et non un caractère aléatoire), ce qui réduit considérablement le gaspillage des références de l'évaluateur ∞

L'évaluateur, à son tour, prend les confabulations du LLM. Les LLM affirmeront avec confiance qu'une fonction "est O(n log n) dans la limite" alors qu'elle est en fait O(n^2); une référence de l'horloge de mur rend la question résolue.

> L'évaluation de l'évaluation de la fonction "Limite n log n" est une fonction qui est définie comme "Limite n log n" et qui est en fait une fonction "O" n2).

### Là où AlphaEvolve s'inscrit dans la pile frontalière

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

Les quatre sont des variations sur la même recette: générateur plus évaluateur, boucle.

> Les quatre sont des variantes du même composé: générateur, évaluateur, cycle.
```figure
alphaevolve-loop
```

## Utilisez-le

## Utilisez-le avec le cadre de réalisation

`code/main.py`Il implique une boucle minimale semblable à AlphaEvolve sur un problème de régression symbolique de jouet.

> `code/main.py`Dans un problème de retour des symboles de jouets, un cycle minimal similaire à AlphaEvolve est réalisé.

Le "LLM" est un proxy stdlib qui propose de petites mutations syntactiques à un programme qui compute une fonction cible.

> "LLM" est un standard de base, qui propose des modifications linguistiques mineures à un programme de fonction de calcul objectif.

Regardez !

> 观察:

- Comment le meilleur score s'améliore au fil des générations.
  Le meilleur score de la génération
- Comment une grille de MAP-Elites maintient des solutions diverses en vie pour que la boucle ne converge pas sur un minimum local.
  Le réseau de la carte est un réseau de réseaux de réseaux de réseaux.
- Comment enlever le test prolongé (évaluateur de formation seulement) permet de surcharger la boucle de façon spectaculaire.
  En français, le mot "séparation" est traduit par "séparation".

## Envoyez-le . Produit .

`outputs/skill-evaluator-rigor-audit.md`est la condition préalable pour envisager une boucle de style AlphaEvolve dans un nouveau domaine: votre évaluateur détecte-t-il réellement les défaillances qui vous intéressent ?

> `outputs/skill-evaluator-rigor-audit.md`Est-ce que dans un nouveau domaine, on peut envisager des conditions prédéterminées de la cycle AlphaEvolve: votre évaluateur a-t-il vraiment capturé l'échec de votre intérêt ?

## Les exercices

1. On court .`code/main.py`- Notez la meilleure trajectoire de score.`--no-holdout`) et de refaire.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` enregistrer le meilleur nombre de trajets  empêcher la conservation de l'évaluation `--no-holdout`) Récupération.

2. Lisez la section 3 du document AlphaEvolve sur la grille MAP-Elites.
   Le troisième chapitre de l'étude AlphaEvolve sur les élites de la carte de la planète 网格──为新问题 (en anglais)

3. Le résultat 48-multiplication 4x4 s'est amélioré sur la limite de 49-mul de Strassen après 56 ans. Lisez l'annexe F du document et expliquez en trois phrases pourquoi l'évaluateur pour ce problème est particulièrement facile à obtenir correctement, et pourquoi la plupart des domaines ne le sont pas.
   Le résultat de la pratique 4x4 de 48 fois est d'améliorer la 49 fois de la frontière de Strassen 56 ans plus tard.

4. Proposez un domaine où AlphaEvolve échouerait, identifiez exactement où l'évaluateur se casse et pourquoi.
   Le système d'évaluation est un système de gestion de la situation de l'entreprise.

5. Pour un domaine que vous connaissez, écrivez la signature de l'évaluateur que vous utiliserez. Incluez (a) les conditions de correction, (b) la métrique de performance, (c) la règle de génération de données de saisie retenue, (d) au moins une vérification anti-hacking de récompense.
   Pour une des parties de votre connaissance, écrivez le nom de l'équipe d'évaluation que vous utiliserez.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Encore une lecture

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131)- Le papier complet.
  Le texte est en français.
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) répertorier le fournisseur avec les résultats.
  Le produit est le produit de la production.
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results) des algorithmes découverts, y compris le matmul 4x4 à 48 moul.
  Le dépôt d'algorithmes, comprenant 48 fois la multiplication 4x4 矩阵乘法。
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) le système prédécesseur.
  Le mot "funsearch" est traduit par "funsearch".
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) définit l'autonomie liée aux évaluateurs comme une direction de recherche clé.
  L'autonomie de l'équipe d'évaluation est un élément clé de la recherche.
