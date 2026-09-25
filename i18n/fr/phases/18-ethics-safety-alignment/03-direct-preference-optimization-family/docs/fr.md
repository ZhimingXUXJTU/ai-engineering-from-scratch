# La famille de l' optimisation des préférences directes

> Raphaïlov et al. (2023) a montré que l'optimisation de RLHF a une forme fermée en termes de données de préférence, de sorte que vous pouvez sauter le modèle de récompense explicite et optimiser la politique directement. Cette compréhension a donné naissance à une famille  IPO, KTO, SimPO, ORPO, BPO  chacun fixant un mode d'échec de DPO. En 2026, les algorithmes d'alignement direct envoient plus de courses post-entraînement frontalières que les PPO. Mais la courbe de suroptimisation de la leçon 2 s'applique toujours: les DAA ne fuient pas Goodhart, ils se déplacent simplement là où il mord.

> **【中文解读】**Le présent épisode présente le modèle de récompense dépassé directement par le modèle de RLHF de l'entraînement de données de préférence. Raphaëlov et d'autres personnes ont démontré que le RLHF de l'optimisation des données de préférence est lié à l'expression de données de préférence, de sorte que l'on peut sauter le modèle de récompense apparente.

> **【拓展：DPO 家族 → 现代 AI 训练】**En 2026, le DPO n'a pas échappé à la loi ancienne, mais a simplement changé la surface de son attaque. De "modèle de récompense sur-optimisé" à "ratio de référence sur-optimisé" ("Refrain Strategy Ratio sur-optimisation").

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

>  **【前置】**學本節前 請先掌握:Phase 18·01-02 InstructionGPT+古德哈特) Phase 10·08 DPO 基础) DPO 家族 = 绕过显式奖励模型直接从偏好数据训练──
>  **【类比】**DPO = " éliminer le match du juge "―RLHF = 训练裁判(奖励模型) + 训练选手优化裁判评分;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;偏好对) 训练选手;;家族变体 IPO/KTO/SimPO/ORPO/BPO 都在修 DPO 不同缺陷;;2026 DAA(直接对齐算法) 更多比 PPO 部署;;但古德特定规律不变只是从"奖励模型过优化"挪到"参考策略比率过度优化"―
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Dériver la forme fermée du DPO de l'optimisme RLHF-avec-KL.
  Le RLHF de KL est le plus connu de la région.
- Indiquez le mode d'échec de chacune des corrections d'IPO, KTO, SimPO, ORPO et BPO dans le DPO.
  Le premier est le premier, qui a été créé par le gouvernement de l'État.
- Distinguer "l'écart de récompense implicite" de "la force de préférence" et expliquer pourquoi la cartographie de l'identité de l'IPO est importante.
  La différence entre les prix et les prix est importante.
- Expliquez pourquoi Rafailov et coll. (NeurIPS 2024) prouvent que les DAA sont suroptimisés en dépit de leur absence de RM explicite.
  Le rapport de la RDA (RDA) confirme que la RDA est encore en surpoids.

## Le problème , l' introduction du problème

L'objectif du RLHF (leçon 1) est le suivant:

> RLHF 目标(L'enseignement 1):

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

a un optimum connu:

> Il y a le meilleur résultat:

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

Ainsi, la récompense est implicitement définie par le rapport entre la politique optimale et la référence:

> Le ratio des récompenses par les meilleures stratégies et les stratégies de référence est donc défini en termes suivants:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Remplacez cela par la probabilité de préférence Bradley-Terry et la fonction de partition .`Z(x)`annuler parce que cela dépend uniquement de `x`. Ce qui reste, c'est une perte dans les paramètres de politique seulement  pas besoin de modèle de récompense.

> Pour le remplacer par Bradley-Terry, la fonction de distribution`Z(x)`Parce que ça dépend.`x`La seule chose qui reste est la fonction de perte des paramètres de stratégie pure.

La dérive: la dérive suppose que l'optimal est atteignable, les données de préférence sont en distribution et la politique de référence est l'ancre de mode vrai. Aucun de ces éléments ne s'applique exactement. Chaque membre de la famille fixe une hypothèse différente violée.

> Le problème réside dans: la préférence des hypothèses optimales dans la distribution des données, la stratégie de référence est réelle.

## Le concept de base.

> **【中文解读】**La recommandation de l'OPE:RLF 目标有已知最优解 pi*((DH y y y yx) = (1(x)) * pi_ref(y y yx) * exp(r((x,y) /beta)  La récompense sera exprimée pour le plus grand nombre de stratégies optimales et de taux de référence stratégies, cédé à Bradley-Terry 偏像然, la fonction de répartition Z(x) Parce que dépend uniquement de x et qu'il reste une fonction de perte des paramètres stratégies, sans besoin de récompense modèle ~~ mais la recommandation de hypothèses optimales à atteindre, la distribution de données préférentielle  la référence stratégies est vraiment  point  Ces hypothèses ne sont pas complètement valides dans la pratique.

### DPO (Rafailov et coll., 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

Qu'est-ce qui peut aller mal ?

> Ça peut être un problème.

- L' écart de récompense implicite `beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`Une petite préférence peut créer un écart arbitrairement grand.
  Le prix de la récompense est un prix de la récompense.
- Les disques de perte choisissent et rejettent les log-probes dans des directions opposées. Il peut pousser le log-prob absolu choisi vers le bas tant que le rejet tombe plus rapidement.
  Le risque de déclin des nombres est inversé. Si le déclin des nombres est plus rapide, il peut être réduit.
- Les préférences hors distribution (pares rares contre pares rares) produisent des récompenses implicites arbitraires.
  Le premier est le premier.

> **【拓展：IPO → DPO 的边界控制】**IPO(Identity Preference Optimization) avec des cartes de log-sigmoïde, la différence de préférence est supprimée par 1/(2*beta) 封顶. Ceci résout le problème central du DPO: de petites différences de préférence peuvent générer une différence de récompense cachée volumineuse.

### Les actions d'investissement (Azar et coll., 2024)

L'optimisation des préférences d'identité remplace le log-sigmoid par une carte d'identité sur la probabilité de préférence.

> L'IPO utilise des égalistes pour remplacer le log-sigmoïde, la différence de préférence est supprimée par 1/(2 *beta) 封顶.

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

La marge est délimitée par `1/(2 beta)`- La force de préférence et l'écart entre les récompenses implicites sont proportionnels.

> La frontière est en train de se détériorer.`1/(2 beta)`La différence entre la force de préférence et la récompense cachée est correcte.

> **【拓展：KTO → 无配对数据训练】**L'innovation clé de l'optimisation de Kahneman-Tversky est d'abandonner complètement le couplage de la structure, en utilisant uniquement des signaux individuels pour les sorties "idéales" ou "immédials".

### Les mesures de sécurité sont prises en application de la directive 2009/65/UE.

L'optimisation Kahneman-Tversky réduit entièrement la structure parallèle.

> KTO  complètement abandonné le couplage de la structure ⋅ donné un seul signal de sortie et de signal "idéal" ou "non idéal", il est cartographié à l'effet théorique de la perspective:

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

Les données de l'entreprise sont utilisées pour les données de l'entreprise, mais elles sont utilisées pour les données de l'entreprise.

> Les avantages: vous pouvez utiliser des données non associées, ce qui est plus important que les données associées.

> **【中文解读】**SimPO remonte la stratégie de référence, en remplaçant par des comparaisons de longueur unifiées par des comparaisons de longueur, en ajoutant à la formation de stabilité gamma. Ceci résout directement le problème de la longueur de la DPO par défaut de modèle  plus long y_w constructionnairement produisant une plus grande différence de probabilité de longueur ⋅ ORPO ⋅ plus intensifié: ajouter des préférences à la norme SFT ⋅ NLL ⋅ sur la perte, un seul stade de la formation du modèle de base à la formation de la ZZ ⋅ BPO identifie le problème de " résolution de la sélection de déformation " DPO garde y_w > y_w ≠ but y_w ≠ des probabilités de longueur absolue peuvent diminuer.

### SimPO (Meng et coll., 2024)

L'optimisation des préférences simple aligne le signal d'entraînement avec la génération.

> SimPO va former les signaux et générer les mêmes.

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

avec une marge `gamma`La normalisation de la longueur élimine l'incitation à exploiter le mode d'échec du biais de longueur du DPO (plus long `y_w`donne un écart plus grand entre les logs et les probes par construction).

> Avec le temps`gamma`稳定训练―― Longitude regroupement a éliminé l'utilisation de DPO 长度偏见失败模式的激励`y_w`La différence de probabilité de la formation des nombres est plus grande.

### ORPO (Hong et coll., 2024)

L'optimisation des préférences par rapport aux cotes ajoute un terme de préférence à la probabilité de log négatif standard de la FFT:

> L'ORPO ajoutera les préférences à la norme SFT 负对数似然上:

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

Aucune politique de référence  le terme SFT est le régulateur. entraînement en une seule étape du modèle de base au modèle aligné. Aucun point de contrôle SFT séparé.

> 无参考策略SFT 项就是正则化器──单阶段从基础模型训练到对齐模型──无需单独的SFT 检查点──

### BPO (déclaration ICLR 2026, OpenReview id=b97EwMUWu7)

Identifie le problème des réponses dégradées choisies: le DPO conserve le classement `y_w > y_l`Mais le log-prob absolu de `y_w`Le BPO ajoute une correction à une seule ligne qui pénalise les mouvements descendants sur la réponse choisie.

> BPO 识别了"退化选择响应" problème:DPO 保持 `y_w > y_l`排序但 `y_w`Le taux de probabilité de l'absence de nombre peut être réduit.

> **【拓展：DAA 过度优化 → 通用防御】**Raphaïlov et d'autres ont été utilisés dans plusieurs collections de données et le budget de KL pour former le DPO, l'IPO, la SLiC et la stratégie. Les récompenses réelles et les courbes de KL sont les mêmes que celles de Gao et d'autres.

### Le résultat universel: les DAI continuent à suroptimiser

Rafailov et coll. "Leges d'échelle pour la suroptimisation des modèles de récompense dans les algorithmes d'alignement direct" (NeurIPS 2024) ont formé des politiques avec DPO, IPO, SLiC sur plusieurs ensembles de données sur les budgets KL. Les courbes doré-récompense-versus-KL ont la même forme Gao et coll. La requête implicite de récompense demande des échantillons hors de distribution pendant la formation; la normalisation KL ne stabilise pas cela.

> Raphaïlov et d'autres ont été formés sur plusieurs ensembles de données et le budget de KL sur la stratégie DPO、IPO、SLiC。 les récompenses réelles sont apparues avec la même forme de progression et de baisse que celle de KL ‖ Gao et d'autres.

Les DAA ne s'échapperont pas à Goodhart. Ils changent la surface où il mord de "modèle de récompense suroptimisé" à "ratio de politique de référence suroptimisé".

> La DAA n'a pas échappé à la loi ancienne. Elles vont simplement passer de l'optimisation excessive du modèle de récompense à l'optimisation excessive du taux de référence.

> **【中文解读】**Les méthodes de sélection de 2026 sont les suivantes: il y a une forte proportion de données préférentielles → DPO(保守 beta) ou SimPO(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

### Choisir parmi eux (2026)

- Si vous avez de grandes données de préférence partagées: DPO avec bêta conservateur, SimPO si le biais de longueur est évident.
  Le premier est le premier, qui est le premier, qui est le premier.
- Si vous avez des retours binaires non couplés: KTO.
  Il est également utilisé dans les services de communication.
- Si vous voulez un pipeline à étape unique d'un modèle de base: ORPO.
  Le mot "seulement" est traduit par "seulement" en français.
- Si vous voyez des sondes de journaux choisies dégradées dans les journaux du DPO: BPO.
  Le taux de croissance est de 4,5% en moyenne.
- Si les valeurs de préférence varient considérablement et que le DPO est saturant: IPO.
  Le débit de la production est de 0,5% en moyenne.

Chaque laboratoire utilise une batterie pour choisir le gagnant par tâche.

> Chaque laboratoire a été entièrement suivi par toutes les méthodes. Il n'y a aucune raison de penser que la meilleure méthode de logique mathématique et de sécurité est la même.

> **【拓展：DPO 家族实践 → 方法选择】**En 2026, chaque laboratoire avant-gardiste a été entièrement suivi par des méthodes différentes. Il n'y a aucune raison de penser que la meilleure méthode de logique et de sécurité mathématiques est la même.

## Utilisez-le avec le cadre de réalisation
```figure
dpo-margin
```

## Utilisez-le

`code/main.py`Comparer six pertes (DPO, IPO, KTO, SimPO, ORPO, BPO) sur un ensemble de données de préférence de jouets où la force de préférence réelle varie par paire. Chaque perte est optimisée contre le même échantillon de 500 paires avec une petite politique de softmax.

> `code/main.py`Dans le jeu de données de variation de la intensité de préférence, comparer six types de perte (DPO,IPO,KTO,SimPO,ORPO,BPO) ⋅ chaque type de perte dans le même 500 pour les échantillons avec des stratégies de softmax de petite taille ⋅ optimiser ⋅ tracer le taux de victoire final de chaque méthode ⋅ sélection de probabilité de déménagement et de répartition de récompenses cachées ⋅

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-preference-loss-selector.md`. Compte tenu des statistiques des ensembles de données (parées contre nonparées, variables contre force de préférence uniforme, distribution de longueur) et d'une cible (étape unique ou SFT-then-preference), recommander une perte de préférence et signaler le mode de défaillance contre lequel il protège.

> 本课产 出 `outputs/skill-preference-loss-selector.md` données données données statistiques (partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie partie

## Les exercices

1. On court .`code/main.py`. Rapporte la dernière baisse de l'enquête de logue choisie pour le DPO et le BPO.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Rapport de la décision finale du DPO et du BPO sur la probabilité de décroissance du nombre de personnes.

2. Modifiez les données de préférence afin que toutes les paires aient la même force.
   La modification des préférences de données rend toutes les formes de comparaison de la force et de la force.

3. Faites en moyenne 2 fois plus longues les réponses rejetées que celles choisies.
   En français, la valeur de réponse moyenne de la réponse moyenne est de 2 fois.

4. Rafailov et coll. (NeurIPS 2024) affirment que les DAA sont suroptimisées.
   Le projet de loi de la République de Russie (Nord-Estonie) prévoit une réduction de la répartition des taux de chômage en raison de la répartition des taux de chômage en Allemagne.

5. Lisez le résumé du document BPO (OpenReview b97EwMUWu7).`code/main.py`- Je suis désolé .
   Le texte de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la lettre de la première lettre de la première lettre de la lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première lettre de la première de la première lettre de la première de la première à la première à la lettre de la première de la première de la lettre de la première de la lettre de la première de la première de la première de la lettre de la première de la première de la lettre de la première de la première de la première de la lettre de la première de la première de la première de la lettre de la première de la première de la première de la lettre de la première de la première de la première de la première de la première de la première de la lettre de la première de la première de la première de la première de la première de la première de la première de la lettre de la première de la première de la première de la première de la première de la première de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de la semaine de`code/main.py`Confirmation de réalisation

## Les termes clés

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Encore une lecture

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  Le texte original de la déclaration de l'État de Russie
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) OPC
  Le texte de l'article est le suivant:
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  Le texte de l'article est le suivant:
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  Le texte de l'article est le suivant:
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  Le texte de la lettre de Hong Kong
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  Le comportement de BPO  garder l'optimisation
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  Le texte de la loi est en partie écrit en français.
