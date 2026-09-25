# Critères d'équité  Groupe, individuel, contrefactuel  Contrar faits  juste 准则

> Trois familles ont créé la littérature de l'équité. L'équité des groupes: parité démographique, cotisations égalées, équité d'utilisation conditionnelle d'une certaine précision  taux égaux entre les groupes protégés en moyenne. L'équité individuelle (Dwork et al. 2012): des individus similaires reçoivent des décisions similaires; condition de Lipschitz sur la carte de décision. L'équité contrefactuelle (Kusner et coll. 2017): une décision est juste pour un individu si elle est inchangée lorsque des attributs sensibles sont modifiés de manière contrefactuelle. Résultat théorique 2024 (NeurIPS 2024): il existe un compromis inhérent entre CF et précision; une méthode modèle-agnostique convertit un prédicteur optimal mais injuste en un prédicteur CF avec perte de précision limitée. Contrastes de rétractation (arXiv:2401.13935, janvier 2024): un nouveau paradigme qui évite d'exiger des interventions sur les attributs légalement protégés. Réconciliation philosophique (ICLR Blogposts 2024): avec des graphiques de causes, satisfaire certaines mesures d'équité de groupe implique une équité contrefactuelle.

> **【中文解读】**Ce chapitre présente les principes d'équité  équité collective  équité collective  équité collective et équité collective  équité collective  équité collective  équité collective et équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité collective  équité  équité collective  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité  équité

> **【拓展：不可能定理 → 公平性冲突】**Chouldechova / Kleinberg-Mullainathan-Raghavan (en 2017): impossible de théorie: le droit à l'égalité des peuples, la prééquivabilité moyenne et les conditions d'utilisation du taux de précision moyenne ne peuvent être satisfaites simultanément sous le taux de base d'inégalité.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Je vous invite à maîtriser la phase 18·20 (façon 2)
>  **【类比】**公平 = "AI de la justice " (→ Les résultats de l'étude de l'emploi et de la recherche de l'emploi)
> 🤔 NeurIPS 2024:CF-vers-exactitude Il y a un poids interne, mais il existe un moyen de transfert de perte de bord.

## Objectifs d'apprentissage

- Indiquez les trois critères d'équité de groupe (parité démographique, cote égalisée, égale précision d'utilisation conditionnelle) et un résultat impossible.

> Il y a trois groupes de normes équitables:

- Décrire l'équité individuelle à l'aide de la formule de Dwork et coll. 2012 de Lipschitz.

> 描述通过 Dwork 等人 2012年 Lipschitz 公式定义的个体公平──

- Décrivez l'équité contrefactuelle et sa dépendance au graphe causale.

> 描述反事实公平及其因果图依赖──

- Expliquez les contrefaçons de rétractation et pourquoi elles évitent le problème de l'intervention sur les attributs protégés.

> Expliquer les faits et les raisons pour lesquelles ils évitent d'intervenir sur les propriétés protégées.

## Le problème .

La leçon 20 traitait de la mesure des biais. La leçon 21 traitait de la définition de la norme d'équité à laquelle la mesure devrait servir. Les trois familles donnent des normes structurellement différentes  un modèle peut être équitable en groupe et injuste en individu, équitable en contrefaçon et injuste en groupe. Choisir une norme est une décision politique; aucune norme n'est universellement optimale.

> La leçon 20 est sur les préjugés de mesure. La leçon 21 est sur la définition des normes équitables de mesure et de service.

## Le concept.

> **【中文解读】**群体公平三大标准: population平权P(Y=1 oùA=a) = P(Y=1 oùA=a'),各组接受率相等;均等化赔率P(Y=1 oùY*=y,A=a) = P(Y=1 oùY*=y,A=a'),各组真阳性率和假阳性率相等;条件使用准准率均等P P Y*=yY=y,A=a) = P各组Y(*=yY=y,A=a'),

### L'équité de groupe

- **Demographic parity.**P\Y=1\A=a=P\Y=1\A=a') pour tous les groupes.
- **Equalized odds.**P (Y=1), Y=y, A=a = P (Y=1), Y=y, A=a) = TPR et FPR égaux dans les groupes.
- **Conditional use accuracy equality.**P * Y = y , Y = y, A = a) = P * Y * y , Y = y, A = a') est la même valeur prédictive entre les groupes.

> Les taux d'acceptation de chaque groupe sont égaux; les taux de compensation de chaque groupe sont égaux; les taux de positivité et de faux positivité de chaque groupe sont égaux; les conditions d'utilisation sont égales; les taux de prédiction de chaque groupe sont égaux.

L'impossibilité (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): ces trois critères ne peuvent pas être satisfaits simultanément sous des taux de base inégaux.

> Il n'est pas possible de déterminer: les trois ne peuvent pas être satisfaits simultanément en fonction du taux d'inégalité.

### L'équité individuelle

Une carte de décision f est individuellement équitable par rapport à une métrique de similitude spécifique à la tâche d si f(x) - f(x') <= L * d(x, x') pour une constante de Lipschitz L. Des individus similaires prennent des décisions similaires.

> Dwork 等人 2012── décision mappage f Si un nombre de Lipschitz 常数 L 满足 f  x) - f  x') est <= L * d  x, x'), alors la mesure de similitude d'une tâche spécifique est équitable── similaire.

Il faut définir d. Question politique, pas statistique.

> Il faut définir le problème de la politique, pas de la statistique.

> **【拓展：反事实公平 → 因果图依赖】**Kusner 等人(2017) de l'antifactueux équité: dans le modèle de l'inconvénient, si la décision ne change pas après que l'attribut sensible de l'individu contre le fait change, alors la décision est équitable pour cet individu.

### L'équité contrefactuelle

Une décision est contrefactuellement juste pour l'individu i si, selon un modèle de causalité de la population, la décision est inchangée lorsque les attributs sensibles i sont contrefactuellement modifiés.

> Kusner et autres 2017: Dans le modèle de conséquences, si les décisions prises par un individu sont inchangées par des attributs sensibles au fait, elles sont équitable à l'égard de l'individu.

Il faut une DAG causale, la DAG est un choix de modélisation, l'équité contrefactuelle est justifiée seulement par la DAG.

> 需要因果 DAG──DAG 是建模选择──反事实公平的合理性取决于DAG的合理性──

### Le compromis CF-versus précision

NeurIPS 2024 théorique: il existe un compromis inhérent entre l'équité contrefactuelle et la précision prédictive. Une méthode modèle-agnostique peut convertir un prédicteur optimal mais injuste en un prédicteur CF, à un coût de précision limité. Le coût de précision dépend de l'ampleur du coefficient d'attribut sensible dans le prédicteur injuste optimal.

> NeurIPS 2024  Theoretical Result: Il existe un poids fixe entre l'antifactualité et la prédiction de la précision.

### Contrôts de rétractation

arXiv:2401.13935 (janvier 2024). Les contrefaçons traditionnelles nécessitent des interventions sur l'attribut sensible  "la décision changerait si cette personne avait été d'un sexe différent".

> La tradition anti-facts nécessite une intervention de nature sensible.

Les contrefactuels de rétractation font tourner le dos: au lieu d'intervenir sur l'attribut, demandez quelle combinaison des caractéristiques réelles de l'individu aurait produit le résultat contrefactuel.

> Le retour contre les faits n'est pas une attribut de pré-intervention, mais une question de savoir quelles composantes des caractéristiques réelles de l'individu produisent des résultats contre les faits.

> **【中文解读】**哲学调和((ICLR Blogposts 2024): après avoir trouvé des causes, satisfaire certaines mesures d'équité de groupe implique une contradiction de faits et de faits.

### Réconciliation philosophique

ICLR Blogposts 2024. Avec un graphique de causalité à portée de main, satisfaire certaines mesures d'équité de groupe implique une équité contrefactuelle.

> ICLR 2024: après la conception de la cause, satisfaire certains groupes de mesures équilibrées implique l'équité contre les faits.

Cela ne résout pas les théorèmes de l'impossibilité (les taux de base inégaux empêchent toujours l'équité simultanée des groupes).

> Il n'y a pas de solution impossible à la théorie, mais il est indiqué que la partie de l'opposition de surface entre le "groupe" et le "personne/fait contraire" est due à l'absence d'hypothèses causées par un modèle de facteur explicite.

### Là où cela s'inscrit dans la phase 18

La leçon 20 est la mesure du biais. La leçon 21 est la définition de l'équité. La leçon 22 est la vie privée (privé différentiel). La leçon 23 est la marquage d'eau.

> Leçon 20 est la mesure des préjugés. Leçon 21 est la définition équitable. Leçon 22 est la confidentialité. Leçon 23 est l'inconvénient.

> **【拓展：CF vs 准确性权衡 → 实际影响】**NeurIPS 2024  théorique résultat: il existe un poids fixe entre le contrefait public et la prédiction de la précision. Le modèle de l'inconnuisme peut convertir le prédicteur le plus optimal mais injuste en CF juste, mais la perte de précision dépend de la taille des facteurs d'attributs sensibles du prédicteur injuste. Cela signifie choisir des normes équitables avec des coûts réels.

## Utilisez-le.
```figure
an-fairness-trilemma
```

## Utilisez-le

`code/main.py`construit un ensemble de données de classification binaire de jouets avec un attribut sensible et des taux de base inégaux. Compute la parité démographique, les cotes égalées et l'équité de précision d'utilisation conditionnelle sur un classificateur simple. Observez les trois mesures qui ne sont pas d'accord. Appliquez une ré pondération pour la parité démographique et observez son coût sur les deux autres.

> `code/main.py` construire un ensemble de données de jouets à caractère sensible et à taux de base d'inégalité.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-fairness-criterion.md`. En raison d'une allégation ou d'une politique d'équité, il indique quel critère est réclamé, si le modèle peut satisfaire aux critères restants en vertu des taux de base inégalés réclamés et quel DAG de causalité dépend de la allégation.

> 本课产 出 `outputs/skill-fairness-criterion.md` Déclaration ou politique d'équité, déclaration de reconnaissance de la nature des critères, de la satisfaction des autres critères, et de la déclaration de la dépendance des causes

## Les exercices

1. On court .`code/main.py`- Rapporter les trois indicateurs de groupe sur les données par défaut.

2. Implémenter la métrique d'équité individuelle de Dwork et coll. 2012 en utilisant L2 sur les caractéristiques non sensibles.

3. Lisez Kusner et coll. 2017. Construisez un simple DAG causale à deux facteurs pour le score de CV et identifiez la condition d'équité contrefactuelle qu'il implique.

4. Le document relatif aux contrefacteurs de rétractation 2024 évite l'intervention sur les attributs protégés.

5. La réconciliation ICLR 2024 soutient que l'équité de groupe et contrefactuelle sont des facettes de la même structure.`code/main.py`et indiquer l'hypothèse causale qui les rendrait équivalents.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Encore une lecture

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) équité individuelle
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) équité contrefactuelle
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) impossibilité
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) un nouveau paradigme pour les interventions à attribut protégé
