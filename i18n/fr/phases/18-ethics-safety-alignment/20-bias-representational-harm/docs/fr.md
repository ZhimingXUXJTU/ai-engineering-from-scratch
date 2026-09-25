# Les préjugés et les préjudices représentatifs dans les LLM

> Il est également possible de faire appel à des services de communication et de communication de manière à ce que les données soient disponibles. Enquête fondatrice de 2024 distinguant les dommages représentatifs (stéréotypes, suppression) des dommages alloués (distribution inégale des ressources) et catégorisant les mesures d'évaluation en tant que métriques basées sur l'intégration, la probabilité ou le texte généré. 2024-2025 empirique: An et al. (PNAS Nexus, mars 2025) mesure le biais intersectionnel de genre x race sur GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B sur l'évaluation automatisée du CV pour 20 emplois de niveau d'entrée. WinoIdentity (COLM 2025, arXiv:2508.07111) introduit une évaluation de l'équité fondée sur l'incertitude pour les identités intersectionnelles. Yu & Ananiadou 2025 identifient les neurones de genre dans les couches de PLM; Ahsan & Wallace 2025 utilisent les SAE pour révéler les préjugés raciaux cliniques; Zhou et coll. 2024 (UniBias) manipule les têtes d'attention pour débiasing. Meta-critique (arXiv:2508.11067): La littérature de 10 ans se concentre de manière disproportionnée sur le biais binaire de genre.

> **【中文解读】**Cette section présente les préjugés et les préjugés représentatifs dans les systèmes d'IA. Les méthodes de préjugés provenant de l'IA sont les méthodes de contrôle et de réduction. Gallegos et autres.

> **【拓展：交叉偏见 → 真实世界影响】**Une 等人(PNAS Nexus, 2025 年 3 月) a mesuré GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B en 20 positions d'entrée en classe dans l'évaluation de l'auto-rédaction du sexe× préjugés raciaux。GPT-4o dans l'évaluation de l'évaluation du traitement des femmes noires par les femmes noires est plus grave que la discrimination des hommes noirs et des femmes blanches Un seul axe d'évaluation ne peut pas saisir cet effet。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les élèves doivent être informés de la situation et de la situation des enfants.
>  **【类比】**偏见 = "AI de l'ai de couleur"── provenant de données de formation(social history bias) + 训练目标──评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计)──2025 Un PNAS Nexus:GPT/Claude/Gemini/Llama 在简历评估上都有交叉性别×种族偏见──Yu 2025 dans le MLP 定位"性别神经元",Ahsan 2025 Uses SAE 揭露临床种族偏见──

## Objectifs d'apprentissage

- Définir les dommages représentatifs par rapport aux dommages alloués et donner un exemple de chacun dans un déploiement de MLL.

> ☐ définir les préjudices représentatifs et les préjudices distributifs, et en donner chacun un exemple dans le cadre de la déploiement du MLL.

- Nombre des trois catégories d'évaluation-métrie de Gallegos et coll. 2024 et décrivez une métrique de chacune.

> 列出 Gallegos 等人, trois indicateurs d'évaluation pour l'année 2024,并描述一个指标在每类中.

- Décrivez l'intersectionnalité et pourquoi la mesure de l'équité basée sur l'incertitude de WinoIdentity aborde les lacunes dans l'évaluation du biais à un seul axe.

>  description de la croisée et pourquoi la mesure équitable de l'incertitude basée sur la WinoIdentity a résolu la lacune de l'évaluation du biais monométrique

- Décrire deux approches mécanistes-interprétables du biais (néurones de genre, caractéristiques de l'ESA, manipulation de la tête d'attention).

> 描述两种偏见的机制可解释性方法 性别神经元、SAE特征、注意力头操作)

## Le problème .

Les leçons précédentes couvrent les dommages délibérés (détentions, complot) et la gouvernance de la sécurité.

> Les cours précédents couvraient les préjugés intentionnels et la gestion de la sécurité. Les préjugés sont des préjugés non intentionnels.

## Le concept.

### Réprésentation par rapport à allouement

- **Representational harm.**Un LLM qui présente les infirmières comme exclusivement féminines produit des dommages représentatifs.
- **Allocational harm.**Un LLM qui donne systématiquement un score inférieur aux CV des candidats noirs produit des dommages alloués.

> **代表性伤害：**刻板印象、抹除、低性描绘──**分配性伤害：**Les deux modèles peuvent être "réprésentatifs sans préjugés" mais "distributifs avec préjugés".

Un modèle peut être "réprésentatif impartial" (produit des représentations diverses) tout en étant "partial par allouement" (fait des recommandations inégales).

> 评估需要同时测量两者──

> **【中文解读】**3 catégories d'indicateurs d'évaluation: insertation en base à la mise en valeur de la valeur de l'image et des caractéristiques, liée à la mesure des expressions et non au comportement, la probabilité de la mise en valeur de l'image et de la confirmation par rapport à la contre-indication de la valeur de la valeur, la prise de partialité des comportements, la mise en place de la mise en valeur de la valeur de la valeur de la valeur de la valeur de la valeur et de la valeur de la valeur de la valeur.

### Trois catégories d'évaluation-métrie (Gallegos et coll. 2024)

- **Embedding-based.**Tests de style WEAT sur les emblèmes pré-RLHF. Mesure les associations statistiques entre les termes d'identité et les termes d'attribut.
- **Probability-based.**La probabilité de vérification des stéréotypes par rapport à la violation des stéréotypes.
- **Generated-text-based.**Mesure des tâches en aval sur le texte généré: scoring de CV, rédaction de recommandations, dialogue.

> **嵌入基础：**WEAT 式测试,测量身份词和属性词的统计关联──**概率基础：**L'impression confirme contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre contre**生成文本基础：**La mesure des tâches, la plus élevée mais la plus difficile à réaliser.

### Intersectionnalité

L'évaluation du biais sur le " genre " manque du biais qui ne se produit que sur les paires (de genre, de race).

> Les préjugés sur le "gender" ont été négligés dans les préjugés sur le sexe et la race.

WinoIdentity (COLM 2025) introduit l'équité intersectionnelle basée sur l'incertitude. Il mesure si l'incertitude du modèle sur les résultats diffère entre les tuples d'identité intersectionnelle  pas seulement la prédiction du point. Cela capture les cas où le modèle est également erroné entre les groupes mais plus incertain pour certains, ce qui produit un comportement d'allocation en aval différent.

> WinoIdentity  Introduction à une évaluation équitable de la relation entre les deux parties fondée sur l'incertitude.

> **【拓展：机制可解释性 → 偏见干预新路径】**Le mécanisme explicatif du travail de 2024-2025 ouvre la voie à l'intervention préconisée du mécanisme: les neurones de genre (Yu & Ananiadou 2025)  certains neurones de MLP liés au comportement spécifique du sexe, dissiper ces neurones à un coût limité de capacité de réduire la différence de sexe; préconisations cliniques raciales SAE  Ahsan & Wallace 2025)  rarement les caractéristiques du codeur se décomposeront en dimensions explicatives; UniBias  Zhou  et autres 2024)  attention à l'opération de réaliser des échantillons à préconisations 

### Approches mécanisées

Les travaux d'interprétation de 2024 à 2025 ouvrent le voile à l'intervention mécaniste:

- **Gender neurons (Yu & Ananiadou 2025).**Les neurones spécifiques de la PML sont corrélés avec des comportements spécifiques au genre.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**Les caractéristiques de l'autoencodeur Sparse décomposent la représentation interne en dimensions interprétables; les caractéristiques liées à la race peuvent être identifiées et supprimées.
- **UniBias (Zhou et al. 2024).**La manipulation des têtes d'attention pour débiasing à tir zéro. Les têtes spécifiques amplifient la sensibilité de la classe d'identité; le zéro ou le ré-poids de ces têtes réduit le biais sans réglage fin.

> Le mécanisme explicatif de 2024-2025 ouvre la voie à l'intervention préconisée du mécanisme: les neurones de genre sont désintégrés; ces neurones réduisent la différence de sexe à un coût limité; la préconisation clinique de la race SAE  identification et suppression des caractéristiques raciales; l'action de l'UniBias  attention à la réalisation de zéro échantillon de préconisations 

> **【中文解读】**Pour les personnes handicapées, les études ont montré que les préjugés de genre dans le domaine de l'éducation sont proportionnellement concentrés sur les préjugés de genre secondaire.

### La méta-critique

La revue de littérature de 10 ans (arXiv:2508.11067, 2025) constate que le domaine se concentre de manière disproportionnée sur le biais de genre binaire. D'autres axes  handicap, religion, statut de migration, identité multilingue  reçoivent beaucoup moins d'attention. La méta-critique soutient que l'attention étroite peut nuire aux groupes marginalisés par négligence: un modèle bien dévié sur le genre binaire peut être fortement biaisé sur les dimensions que personne n'a vérifiées.

> 10 ans de documentation recueille la découverte que ce domaine est déproportionné en se concentrant sur les préjugés de genre à deux niveaux.

### Là où cela s'inscrit dans la phase 18

Les leçons 20-21 couvrent le biais et l'équité formellement. La leçon 22 couvre la vie privée. La leçon 23 couvre l'eau marquée.

> Les leçons 20-21 officiellement couvrent les préjugés et l'équité. Les leçons 22 couvrent la vie privée. Les leçons 23 couvrent l'eau.

> **【拓展：交叉性 → WinoIdentity 基准】**WinoIdentity(COLM 2025, arXiv:2508.07111) introduit une évaluation équitable du modèle de mesure basée sur l'incertitude.

## Utilisez-le.
```figure
an-bias-two-harms
```

## Utilisez-le

`code/main.py`construit une sonde de biais basée sur l'intégration de jouets: mesurez la distance de style WEAT entre les termes d'identité et les termes d'attributs dans une simple intégration de co-occurrence. Vous pouvez injecter un biais et observer le feu métrique; appliquer une opération de débiasing simple et observer la récupération partielle.

> `code/main.py`Construit un jouet en jeu: mesure de la distance entre les mots et les mots de caractère en jeu.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-bias-eval.md`. En raison d'une carte modèle ou d'une allégation d'équité, elle contrôle l'évaluation dans les trois catégories métriques (embedding, probabilité, texte généré), la couverture de l'intersectionnalité et le mécanisme de toute intervention débiasing.

> 本课产 出 `outputs/skill-bias-eval.md` une déclaration de modélisation ou d'équité, une évaluation des trois catégories d'indicateurs d'audit, une couverture transversale et un mécanisme de prévention des préjugés.

## Les exercices

1. On court .`code/main.py`- Rapporter les scores de biais de style WEAT avant et après la débiasing étape.

2. Extension de la sonde avec un test intersectionnel: (genre, race) x (carrière, famille).

3. Lisez An et al. 2025 (PNAS Nexus). Identifiez les deux effets intersectionnels qu'ils rapportent que l'évaluation de genre à un seul axe manquerait.

4. Yu & Ananiadou 2025 identifier les neurones de genre. Dessinez une expérience de falsification qui distinguerait " ces neurones causent des préjugés de genre " de " ces neurones corréler avec les préjugés de genre ".

5. La méta-critique soutient que le domaine se concentre trop étroitement sur le sexe binaire.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Encore une lecture

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) enquête canonique
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) étude intersectionnelle à cinq modèles
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) nouveau point de référence
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) Débiasing à tir zéro
