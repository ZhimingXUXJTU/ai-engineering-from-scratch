# Traffic d'ombre, déploiement des Canaries et déploiement progressif pour LLM

> Les déploiements de LLM combinent les parties les plus difficiles du déploiement de logiciels: aucun test unitaire, modes de défaillance diffuse, signaux retardés. La séquence est (1) mode ombre  répétition de demandes de prod à un modèle candidat, journal, comparer avec zéro impact utilisateur; détecte des problèmes de distribution évidents mais n'est pas une garantie de qualité; (2) déploiement canarien  déplacement progressif du trafic 10% → 25% → 50% → 75% → 100% avec des portes à chaque étape; suivi des percentiles de latence, coût / demande, taux d'erreur / refus, distribution de longueur de sortie, taux de retour d'utilisateur; (3) test A / B pour différentes alternatives après la stabilité confirmée. Le non-déterminisme est irréductible  jusqu'à 15% de variation de précision sur les circuits avec des entrées identiques en raison de la non-associativité du GPU FP plus la variance de la taille du lot. Le coût est variable, pas constante  un modèle de 20% peut être 3 fois plus cher par appel. La vitesse de retour est décisive: si le retour nécessite un redéploiement, vous êtes trop lent. Politique de vie dans la configuration/drapeau; modèle de vie dans le registre avec les digests collés; retour = politique de retour + seuil de retour + pin ancien modèle en quelques secondes.

> **【中文解读】**Ce chapitre présente les stratégies de déploiement du Shadow/KinsheN/Graduation


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

>  **【前置】**Les résultats de la formation sont les suivants:
>  **【类比】**LLM 部署三步 = "飞机首飞流程"。 Shadow = 地面模拟(复制 prod 请求,零用户影响,对比但不切换);Canary = 真飞但逐步开载客(10%→25%→50%→50%→100%,每步有门禁);A/B = 商务航班对比(稳定测不同方案)。关键后:非确定性不可消除(GPU 浮点+batch 差异致 15% 准确率波动);成本是变量(好20%的模型可能贵重3倍);秒回滚速度决定性(旗级 切换不能重新部署)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Distinguer le mode ombre (comparaison à impact zéro), canarien (traffic en direct progressif) et A/B (comparaison confirmée par la stabilité).
  Le nombre de personnes qui ont été affectées par le changement de comportement est de 0,5% à 0,5% en moyenne.
- Enumérer cinq mesures canaries spécifiques au LLM (latérance, coût/demande, erreur/déni, distribution de la longueur de sortie, rétroaction des utilisateurs).
  Le nombre de personnes qui ont été licenciées en droit de conduire est de 5 000 personnes.
- Expliquez pourquoi le non-determinisme de la LLM (jusqu'à 15%) modifie ce que signifie "stable" dans un déploiement.
  Le terme "stabilisation" est utilisé dans les études de droit.
- Conceptez un chemin de retour qui prend des secondes (flip de politique) et non des heures (réploiement).
  Le projet de réinstallation est un projet de réinstallation de la structure de l'équipement.

## Le problème , l' introduction du problème

> **【中文解读】**La mise en œuvre de la MLL a combiné les parties les plus difficiles de la mise en œuvre du logiciel: aucun module de test, aucun modèle de défaillance, aucun signal de retard. La séquence correcte est: 1) le modèle de production sera copié à la demande de production jusqu'au modèle candidat, à la proportion de journaux, à l'impact de zéro utilisateur; 2) le système de mise en œuvre de la MLM a été mis en place à 10%→25%→50%→75%→100%; 3) le test A/B a un indicateur de contrôle de la stabilité après la confirmation de la mise en œuvre; 3) la vitesse de retour de la mise en œuvre de la MLM est déterminante.

> **【拓展：LLM 非确定性与部署】**L'incertitude de la LLM est incontournable la même entrée sur le même modèle peut produire des différences de précision allant jusqu'à 15% sur le même modèle cause:GPU FP non-collision √√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√

Vous expédez un nouveau modèle. Les évaluations hors ligne montrent une augmentation de 3% de précision. Vous le redistribuez dans la production. En 24 heures, le coût est en hausse de 40%, les pouces des utilisateurs sont en hausse de 8%, trois billets de clients rapportent " réponses étranges. " Vous retournez. Rédéployer prend 3 heures. Votre week-end est ruiné.

Chaque élément de cela était évitable. Le mode ombre aurait saisi le 40% de hausse des coûts avant que n'importe quel utilisateur ne le voie. Canary aurait arrêté à 10% lorsque les pouces vers le bas se déplaçaient. Le retour du drapeau politique aurait pris 30 secondes. La discipline est ce qui comble le fossé entre "les évaluations hors ligne semblent bonnes" et "les utilisateurs réels sont heureux".

## Le concept de base.

### Mode d'ombre

> **【中文解读】**影子模式候选模型接收与生产相同的请求,输出仅记录不回归用户――日志内容包括:输出内容(与生产不同) 代码数量(成本差异)、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒绝变化、硬错误――不能捕获:用户会感知到的质量差异影子是烟雾测试,不是质量测试――

Le candidat reçoit les mêmes demandes que la production; les sorties sont enregistrées, et non retournées aux utilisateurs.

- Contenu de la production (différence par rapport à la production).
- Compte des jetons (delta de coût).
- La latence.
- Le refus et l'erreur.

Les prises: augmentation des coûts, régressions de longueur, changements évidents de refus, erreurs difficiles. N'attrape pas: les utilisateurs de delta de qualité perçoivent. L'ombre est un test de fumée, pas un test de qualité.

### Déploiement des Canaries

> **【拓展：LLM 金丝雀发布的五个门控指标】**Il est également possible de modifier le code de démarrage de la ligne de référence pour les données de référence de la ligne de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de la ligne de référence de référence de référence de référence de la ligne de référence de référence de référence de référence de la ligne de référence de référence de référence de référence de référence de la ligne de référence de référence de référence de référence de référence de référence de référence de la ligne de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de la ligne de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence de référence

Décalage progressif du trafic avec les portes. Progression typique: 1% → 10% → 25% → 50% → 75% → 100%.

1. **Latency percentiles** P50, P95, P99. violation: le canary a un P99 > 1,5 fois le niveau de référence.
2. **Cost per request** mixte $. Violation: > 20% au-dessus de la ligne de départ.
3. **Error / refusal rate**5xx plus des refus explicites.
4. **Output length distribution** moyenne + P99. Violation: déplacement de distribution.
5. **User-feedback rate**- Les dépôts de billets.

### Le non-déterminisme est la nouvelle variance

Les entrées identiques produisent des sorties non identiques.

- Non-associativité de la GPU FP (ordre de réduction du point flottant varie selon le lot).
- Variance de taille de lot (même indication dans un lot de 128 contre un lot de 16).
- Prise d'échantillons (température > 0).

Mesurée: jusqu'à 15% de variation de précision en fonction des ensembles d'évaluation identiques. "Stable" dans un déploiement signifie que les mesures sont dans la variance attendue, pas identique à la ligne de base.

### Le coût est variable

Un modèle de 20% peut être 3 fois plus cher par appel. Le coût/la demande est l'une des cinq portes.

### Le Rollback est l'arme.

- Flag de politique (système de flag de fonctionnalité): pourcentage de décalage en configuration; prend des secondes.
- Pinning du modèle (digestation du registre): le modèle en pin ne s'améliore pas automatiquement.
- Retour = renverser le drapeau + régler le digeste fixe à l'ancien.

Si votre pile doit être réaffectée, réparez-la avant de le faire.

### Les outils

> **【拓展：LLM 渐进式部署工具链】**Le programme de mise en œuvre de la licence de licence de licence de 2026 a été lancé en 2026 par le groupe de spécialistes de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de

**Argo Rollouts**- Je suis là .**Flagger** Contrôleurs de livraison progressifs Kubernetes. Intégrés à l'itinéraire pondéré Istio/Linkerd.

**Istio weighted routing** Partage du trafic au niveau du réseau de service.

**KServe / Seldon Core** modèle servant avec canary intégré.

**Feature flags**LaunchDarkly, Flagsmith, Désactiver.

### Cadence des métriques

Les portes canaries vérifient toutes les 5 à 15 minutes selon le volume de trafic. 1% du trafic avec 10 req / min donne 50 à 150 points de données par fenêtre  suffisamment pour la latence mais bruyant pour les commentaires des utilisateurs. 10% donne ~ 10 fois plus. Les progrès doivent faire une pause suffisamment longue pour accumuler suffisamment d'échantillons à chaque étape.

### L'étape A/B est facultative

Si le nouveau modèle est nettement différent (comportement différent, courbe de coût différente, ton différent), A/B test à 50% après le passage des canaries.

### Les chiffres que vous devriez vous rappeler

- Progression canarienne: 1% → 10% → 25% → 50% → 75% → 100%.
- Plafond de non-determinisme: jusqu'à 15% de variance de fonctionnement à fonctionnement sur les entrées identiques.
- Cinq indicateurs canariens: latence, coût, erreur/réjection, durée de sortie, rétroaction de l'utilisateur.
- Portée de coût: > 20% au-dessus de la ligne de référence est une violation.
- - Des secondes, pas des heures.

## Utilisez-le avec le cadre de réalisation
```figure
i4-canary-ramp
```

## Utilisez-le

`code/main.py`Simulation d'un déploiement canarien avec régressions injectables.

> `code/main.py`Simulation d'un déploiement canarien avec régressions injectables.

> `code/main.py`Simulation d'un déploiement canarien avec régressions injectables.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-rollout-runbook.md`. Compte tenu du modèle candidat, de la ligne de base et de la tolérance au risque, le plan de conception est shadow→canary→100%.

> 本课产 出 `outputs/skill-rollout-runbook.md`. Compte tenu du modèle candidat, de la ligne de base et de la tolérance au risque, le plan de conception est shadow→canary→100%.

## Les exercices

1. On court .`code/main.py`- Une régression des coûts de 25%.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ 25% de retour. ❖ Quel est le stade de sa capture ?
2. Votre nouveau modèle a un gain de précision de 3% hors ligne mais le coût/demande est de +18%.
   Le prix de vente de votre nouveau modèle est augmenté de 3% mais le coût/ demande est de +18%.
3. Conceptez un roulement qui prend moins de 60 secondes de bout en bout.
   Le projet est terminé en 60 secondes.
4. Le non-determinisme montre ±7% sur votre évaluation.
   Le système de contrôle de l'information est un système de contrôle de l'information.
5. Le mode ombre a une hausse de 40% avant le canary.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Encore une lecture

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
