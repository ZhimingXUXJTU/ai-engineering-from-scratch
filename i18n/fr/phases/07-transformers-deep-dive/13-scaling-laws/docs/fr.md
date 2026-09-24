# Les lois de l'échelle

> Le papier de Kaplan 2020 disait: plus grand modèle, moins de perte. Le papier de Hoffmann 2022 disait: vous étiez sous-entraînés.

> **【中文解读】**La loi de Chinchilla révèle les relations optimales entre les modèles de taille, de données, de calcul.

**Type:** Study | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Lorsque vous avez des C FLOP de formation en calcul et que vous voulez le meilleur modèle, vous êtes confronté à deux boutons:

> Lorsque vous avez l'entraînement pour calculer la quantité et le meilleur modèle, vous vous retrouvez face à deux rotations:

1. **How many parameters (N)?**Un modèle plus grand, une capacité plus élevée.
   Le mot grec traduit par " le mot grec "**多少参数（N）？**Le modèle est plus grand, la capacité est plus élevée.
2. **How many training tokens (D)?**Plus de données, une meilleure utilisation des capacités.
   Le mot grec traduit par " le mot grec "**多少训练 token（D）？**Les données sont plus nombreuses, la capacité d'utilisation est plus bonne.

Les PLOP sont approximativement `6 × N × D`Vous pouvez pousser N vers le haut et D vers le bas, ou D vers le haut et N vers le bas.

> Les FLOP sont approximatifs`6 × N × D`Vous pouvez augmenter N 减小 D, ou augmenter D 减小 N... lequel est mieux?

Avant 2022, la réponse était "pousse N fort". GPT-3 (2020) était 175B paramètres formés sur ~ 300B jetons. Un ratio d'environ 1,7 jetons par paramètre.

> Avant 2022, la réponse est "推大 N"──GPT-3(2020) il y a 175B 参数, dans environ 300B de jetons en haut de l'entraînement── la proportion est d'environ 1,7 参数 par jetons──Kaplan 缩放定律支持这一观点──

Hoffmann et coll. (2022), qui a formé une petite famille de modèles appelés Chinchilla, a trouvé quelque chose de différent: le rapport optimal est plus proche de **20 tokens per parameter**Le GPT-3 était 10 fois moins entraîné. Chinchilla (70B params, 1.4T tokens) a battu le GPT-3 (175B, 300B tokens) sur chaque référence à 2,5 fois moins de coût d'inférence.

> Hoffmann 等人(2022) entraîne un petit groupe nommé modèle de Chinchilla, trouvant différents résultats: le meilleur rapport approximatif**每个参数 20 个 token** GPT-3 低估训练了10倍──Chinchilla(70B 参数,1.4T token) a battu GPT-3 sur chaque base de test(175B,300B token), le coût de la formation est estimé à seulement 2,5% de la dernière.

Llama 3 8B a été formé sur 15 billions de jetons, un ratio de 1 875 jetons par paramètre. 94 fois plus que le Chinchilla-optimal. Les coûts d'inférence comptent plus que les coûts de formation pour les modèles qui seront utilisés à l'échelle, donc une formation excessive (passer Chinchilla) pour une empreinte déployable plus petite est la norme par défaut de 2026.

> En 2026, il s'agit du monde de Chinchilla, mais il y a un tournant important. Llama 3 8B utilise 15 milliards de tokens pour entraîner, proportionnellement pour chaque paramètre de 1,875 tokens.

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D(参数 × token 数) ;;Kaplan(2020) tend à augmenter N, mais Chinchilla(2022) prouve le meilleur pourcentage d'environ 20 tokens/paramètres。2026 années de pratique plus loin:Llama 3 8B utilise 1,875 tokens/paramètres entraînement远超 Chinchilla 最优, car le coût de la théorique est plus important que le coût de la formation, le surcoût de la formation de petits modèles et le faible coût de déploiement est devenu une norme de l'industrie。

> **【拓展：过度训练策略的经济逻辑】**Llama 3 8B utilise 15T token  entraînement(Far sur Chinchilla maximal 160B token), le coût de la réflexion est considérablement réduit. C'est parce que la quantité de calcul de chaque token est en proportion avec le paramètre de la réflexion,8B paramètre du coût de la réflexion est seulement d'environ 1/9 de 70B modèle. Pour les modèles de grande taille déployés, comme API 服务), la réflexion coût économie est très supérieure au coût de la réflexion. Ceci explique pourquoi Phi-3-miniwen 3.8B) et Q2-1.5B etc. modèles sont trop entraînés.

## Le concept de base.

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### La loi Hoffmann

Dans le journal Chinchilla, la perte est suivante:

> Le texte de Chinchilla, perdus suit:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`= paramètres (non intégrés).
  Le mot grec traduit par " le mot grec "`N`= 参数量 (non intégré)
- `D`= jetons de formation.
  Le mot grec traduit par " le mot grec "`D`= 訓練符号 数──
- `α ≈ 0.34`- Je suis là .`β ≈ 0.28`(à peu près symétrique).
  Le mot grec traduit par " le mot grec "`α ≈ 0.34`- Je suis là.`β ≈ 0.28`Je suis en train de faire une petite fête.
- `E ≈ 1.69`, le plafond irréductible de perte.
  Le mot grec traduit par " le mot grec "`E ≈ 1.69`, une perte de valeur maximale.
- `A ≈ 406`- Je suis là .`B ≈ 411`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`A ≈ 406`- Je suis là.`B ≈ 411`Il y a une autre.

Deux termes sont négociés l'un contre l'autre à mesure que vous étaliez.`N`à calcul fixe (C = 6ND) et résoudre:

> 两项在扩展时相互制衡──在固定计算量 (C = 6ND) 下对 `N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Optimisé pour le calcul: 20 jetons par paramètre.

> 計算最优: chaque paramètre est de 20 tokens.

### Pourquoi trop de formation ?

Le Chinchilla-optimal réduit les pertes d'entraînement par entraînement FLOP. Mais vous payez le coût de l'entraînement une fois; l'inférence coûte pour toujours.

> La Chine maximale minimise les pertes de formation de chaque entraînement FLOP. Mais le coût de formation ne coûte qu'une seule fois; le coût de la formation est toujours constant.

Pour un chatbot qui sert un milliard de tokens par mois, l'inférence domine le coût total. L'approche de Llama: traîne plus petit, plus long. 8B à 15T tokens est profondément optimisé pour l'inférence:

> Pour les services mensuels de milliards de tokens, la méthode de formation est de mieux optimiser la profondeur de la formation.

- Il s'adapte aux GPU du consommateur.
  Le mot "GPU" est traduit par "GPU".
- La latence est une fraction de 70B Chinchilla-optimal.
  Le chinois traduit par "Just for 70B Chinchilla"
- La qualité est suffisamment proche pour la plupart des tâches.
  Pour la plupart des tâches, la qualité est assez proche.

Le document 2024 de DeepMind ("Over-training is the new optimal") formait cela. Pour les charges de travail dominées par les inférences, le ratio correct est plus proche de 100500 jetons par paramètre en fonction du volume de service.

> Le thème de DeepMind 2024 est "excès de formation est le meilleur nouveau") a formalisé ce point. Pour la charge de travail de la théorie, le ratio exact approche de chaque paramètre 100 à 500 tokens, dépend du volume de service.

### Émergence versus lissage

Prétendue: certaines capacités (arithmétique, raisonnement à plusieurs étapes, suivi de la chaîne de pensée) "émergent" soudainement à une certaine échelle.

> 声称: certaines capacités (算术、多步推理、思维链遵循) dans une certaine échelle "survenue" (en anglais seulement).

Schaeffer et coll. (2023) ont soutenu que c'est un artefact de mesure: les mesures émergentes utilisent des scores discontinues (correspondance exacte, précision au seuil) qui cachent une amélioration fluide des logits sous-jacents.

> Schaeffer 等人(2023) considère que c'est une mesure de faux-image:涌现指标使用不连续的评分(精确匹配、值准确率), caché des améliorations de la planification des logits de basse échelle。连续指标(交叉) montrer la planification de la ligne。

En 2026, le consensus est que les prévisions sur les pertes continues sont fiables. Les sauts de référence sont souvent des objets de plus haut niveau.

> Le consensus de 2026 est que la prévision des pertes continuelles est fiable.

> **【中文解读】**"Sufficience de mise en émergence" (survenue) a suscité une grande discussion en 2023 sur certaines capacités qui semblent apparaître soudainement à une échelle spécifique. Mais Schaeffer et d'autres ont prouvé que cela pourrait être une mesure de la mise en émergence de la mise en émergence de la capacité de mise en émergence.

> **【拓展：数据质量比数据量更重要】**En 2026, la nouvelle variante de la loi de réduction est la qualité des données. La série Phi de Microsoft prouve que les jetons "hautes qualités" sélectionnés peuvent augmenter efficacement la quantité de calcul de 2 fois ou plus. Llama 3 utilise l'optimisation du ratio de données et le renforcement des données synthétiques. L'architecture MoE permet de mieux comprendre la quantité totale de composants et la quantité de calcul active.

### La photo de 2026

Les lois de l'échelle fonctionnent toujours, mais:

> La loi est toujours valable, mais:

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】**En 2026, la réduction de la qualité des données est confrontée à un problème de mur de données. Les données de texte humain de haute qualité pourraient être consommées dans les prochaines années. Les données de synthèse sont une solution potentielle. La série Phi de Microsoft utilise GPT-4 pour entraîner les données de synthèse de la "qualité des textes" de la production.

L'optimisateur de Muon (Kimi Moonlight, 2024) a montré un gain de calcul efficace de ~ 2x par rapport à AdamW à des données correspondantes. Certaines séries de formation 2026 utilisent Muon par défaut.

> Muon 优化器 (Munion 优化器) Kim Moonlight,2024) a montré sur les mêmes données une augmentation de calcul valide d'environ 2 fois supérieure à celle d'AdamW

## Construisez-le et mettez-le en œuvre.
```figure
scaling-laws
```

## Faites-le

Regardez !`code/main.py`Nous mettons en œuvre l' équation de perte de Chinchilla et résolvons pour calcul-optimal`(N, D)`à chacun des différents budgets informatiques.

> 参见 `code/main.py` Nous avons réalisé l'équation de la perte de Chinchilla et avons cherché à résoudre le calcul optimal dans plusieurs budgets`(N, D)`Il y a une autre.

### Étape 1: Perte de la chinchilla

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

Le film`L`comme un contour sur `(N, D)`à fixé `C = 6ND`Trouvez le minimum.

> Il va`L` comme `(N, D)`                         `C = 6ND`❖ trouver la valeur minimale.

### Étape 2: frontière optimale en matière de calcul

Pour les budgets informatiques de `1e17`à `1e25`Les FLOPs, trouvez `(N, D)`qui réduisent au minimum les pertes, sous réserve de `6ND = C`- Vérifiez le rapport `D/N ≈ 20`- Je suis désolé .

> Pour le`1e17`À la`1e25`Les FLOP de calcul du budget, trouver pour minimiser les pertes `(N, D)`, la rédaction`6ND = C` Pourcentage de la vérification`D/N ≈ 20`Il y a une autre.

### Étape 3: coût de la surentraînement

Comptez la perte supplémentaire que vous payez pour former un modèle 10x plus petit (1/10 de N optimale, 10x D optimale).

> 計算訓練一個 10倍小模型 ((最优 N 的 1/10,最优 D 的 10倍) 付出的额外损失──報告作为交换的推理 FLOP 节约(与 N 成正比)──

### Étape 4: comparer avec les modèles réels

Je sais .`(N, D)`Par exemple, les données de l'analyse de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur

> 输入 GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3(`(N, D)`Pour, comparer les pertes prévisionnelles et les pertes de rapport.

## Utilisez-le avec le cadre de réalisation

Vous ne pouvez pas former un modèle de frontière, mais les lois de l'échelle vous disent:

> Tu ne peux pas t'entraîner toi-même. Mais la loi de l'abréviation te dit:

1. **Whether your fine-tune has enough data.**Si vos données spécifiques à la tâche sont inférieures à 20 jetons par paramètre du modèle de base, attendez-vous à une saturation à un certain niveau de perte.
   Le mot grec traduit par " le mot grec "**你的微调是否有足够数据。**Si vos données spécifiques de tâche sont inférieures à 20 jetons par paramètre du modèle de base, l'attente sera de perdre une certaine limite.
2. **Whether to pick a bigger base model.**Si vous dépensez tout votre budget pour l'inférence, préférez un modèle plus petit et plus long.
   Le mot grec traduit par " le mot grec "**是否选择更大的基础模型。**Si vous dépensez tout le budget sur la réflexion, vous devez choisir un modèle plus petit, un modèle plus long.
3. **Where the returns diminish.**Au-delà de 1000 fois la meilleure des Chinchilla, les changements de perte de logs deviennent du bruit.
   Le mot grec traduit par " le mot grec "**收益递减在哪里。**Après avoir dépassé le maximum de 1000 fois, les pertes numériques sont transformées en bruit.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**Le Web a un nombre fini de jetons de haute qualité (~510 billions d'anglais après filtration). Le prétrain frontalier approche ce plafond.
  Le mot grec traduit par " le mot grec "**数据受限时代。**Le nombre de jetons de haute qualité sur le réseau est limité.
- **Compute-multiplier tricks.**Optimisateur de muons, MoE, meilleure curation de données  chaque déplace les constantes absolues, pas l'asymptote.
  Le mot grec traduit par " le mot grec "**计算倍增技巧。**Les données de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de l'équipe de recherche de recherche de l'équipe de l'équipe de recherche de la recherche de l'équipe de la recherche.
- **Scaling laws for RL.**Les premières preuves suggèrent la loi du pouvoir dans les échantillons de RL mais avec des exponents très différents de la pré-entraînement.
  Le mot grec traduit par " le mot grec "**RL 的缩放定律。**Open Question― Les premières preuves montrent que le modèle RL est lié à la loi, mais les indices et les préparatifs ne sont pas les mêmes―

## Envoyez-le . Produit .

Regardez !`outputs/skill-training-budget-estimator.md`- Les compétences sont choisies .`(N, D, hours, GPU)`pour une nouvelle formation, compte tenu du budget de calcul, des contraintes de déploiement et de la perte cible.

> 参见 `outputs/skill-training-budget-estimator.md` Cette compétence est mise en œuvre en fonction du budget de calcul, du déploiement des contraintes et des pertes de but, de la sélection des nouvelles formations et des opérations.`(N, D, hours, GPU)`Il y a une autre.

## Les exercices

1. **Easy.**On court .`code/main.py`Imprimez Chinchilla-optimal`(N, D)`pour les budgets informatiques `1e20`- Je suis là .`1e22`- Je suis là .`1e24`Comparer avec la vraie table de modèle.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Impression et calcul du budget`1e20`- Je suis là.`1e22`- Je suis là.`1e24`时的Chinchilla 最优 `(N, D)`                                                                                                                                                                                                                                                              
2. **Medium.**Implémenter la courbe de perte de fonction de calcul Hoffmann.`log10(C)`Identifier quand la loi prédit que nous aurons besoin de`>10^28`Les PLOP pour la prochaine réduction de 0,1 de l'entropie croisée.
   L'écriture de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de`log10(C)`◊ déterminer la loi prédiction`>10^28`Les FLOP 才能使交叉再降低 0.1──
3. **Hard.**Appliquez votre propre loi d'échelle sur 5 modèles minuscules (100 000 à 10 millions de params) formés sur le même ensemble de données.`α`et `E`- Vos exposants correspondent-ils à ceux publiés ?
   En français, traduire par " le même ensemble de données " et " le même ensemble de données " est un ensemble de 5 modèles (environ 100K à 10M) qui s'adaptent à leur propre modèle d'échantillonnage.`α`et `E`◊ Comment votre indice correspond à la valeur de publication ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## Encore une lecture

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) le premier document de droit de l'échelle; sous-trainé.
  Le texte de la loi est en français.
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)- Une Chinchilla.
  Le texte de la loi chinoise est le texte de la loi chinoise.
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) émergence en tant qu'artefact de mesure.
  Le thème de l'émergence de l'existence est:
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448)Pourquoi la surentraînement de Llama est la bonne chose pour sa charge de travail.
  Pourquoi l'excès de formation de Llama à son travail est correct ?
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) 2x multiplicateur de calcul.
  Le moon est un appareil de croissance, qui est un appareil de croissance.
