# WMDP et évaluation de la capacité à double utilisation  évaluer  double utilisation WMDP

> Li et coll., "Le benchmark WMDP: Mesurer et réduire l'utilisation malveillante avec le désapprentissage" (ICML 2024, arXiv:2403.03218). 4 157 questions à choix multiples sur la biosécurité (1 520), la cybersécurité (2 225) et la chimie (412). Les questions sont posées dans la "zone jaune"  à proximité permettant la connaissance, filtrées par l'examen par plusieurs experts et la conformité juridique ITAR/EAR. Deux objectifs: évaluation par procuration de la capacité à double usage et référence de non-apprentissage (la méthode RMU complémentaire réduit les performances du WMDP tout en préservant la capacité générale). 2024-2025 récit de terrain: les premières évaluations OpenAI/Anthropic 2024 ont rapporté une " légère amélioration " de la recherche sur Internet; en avril 2025, le Cadre de préparation OpenAI v2 a déclaré que les modèles étaient " sur le point d'aider significativement les novices à créer des menaces biologiques connues ".

> **【中文解读】**Ce chapitre présente les deux utilisations de l'évaluation de la capacité de l'IA dans les domaines de la biologie, de la chimie, de la sécurité réseau, etc. 4,157 questions de choix couvrant la sécurité biologique (1,520) ̊ et de la sécurité réseau (2,225) ̊ et de la chimie ̊) 412), dans les opérations de "zéro région" qui permettent de connaître des processus nocifs mais non directement synthétiques, mais qui permettent de maintenir la capacité de l'IA dans le cadre de la mise en œuvre de la méthode de gestion de l'IA.

> **【拓展：2024-2025 提升叙述 → 从"轻微"到"关键"】**Trois étapes de la description: le modèle de rapport d'évaluation précoce de l'année 2024 " légère amélioration " ne présente que de petits avantages pour les nouveaux utilisateurs; le modèle de rapport de l'année 2025 " ouvrir l'OpenAI PF v2 " va bientôt faire une percée significative pour aider les nouveaux utilisateurs à créer des menaces biologiques connues; les essais d'acquisition d'armes biologiques anthropiques de l'année 2025 " ont été multipliés par 2,53, ne suffisant pas à éliminer l'ASL-3: 18 mois de " légère " évolution pour " potentiellement promouvoir " la réalisation de l'essai.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, WMDP-shaped uplift evaluation harness) | **语言:** Python（标准库，WMDP 形式提升评估框架）
**Prerequisites:** Phase 18 · 16 (red-team tooling), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 16 (红队工具), Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les résultats de la recherche ont été obtenus en 1er janvier 2015.
>  **【类比】**Le programme de recherche sur l'IA (en anglais seulement) est basé sur la recherche sur l'IA (en anglais seulement) et l'analyse de l'IA (en anglais seulement) est basé sur l'IA (en anglais seulement).

## Objectifs d'apprentissage

- Décrivez les trois domaines de WMDP, le nombre de questions et le critère de filtrage "zone jaune".

> Décrire les trois domaines du WMDP, le nombre de questions et les normes de la "région jaune".

- Expliquez à l'UER et pourquoi le WMDP est à la fois une évaluation et un critère de référence pour le désapprentissage.

> Expliquer la RMU et pourquoi le WMDP est à la fois évalué et oublié.

- Décrivez le récit de l'élévation de 2024-2025: "légère élévation" -> "sur le point" -> "insufficient pour exclure ASL-3".

> 描述 2024-2025 年提升叙述:"轻微提升" -> "即将突破" -> "不足以排除ASL-3"──

- Distinguer la capacité relative des débutants de la capacité absolue des experts.

> 区分新手对提升和专家绝对能力──

## Le problème .

La capacité à double usage est le problème de mesure dans le cadre de la sécurité frontalière de chaque laboratoire (leçon 18). La question est: le modèle X améliore-t-il la capacité d'un débutant à causer des dommages massifs en bio, en chimie ou en cyber ? La mesure directe (demander au modèle de produire réellement des dommages) est illégale et contraire à l'éthique. La mesure par procuration a besoin d'un indice de référence que le modèle ne peut refuser (pour produire des chiffres honnêtes de capacité), mais dont les questions ne sont pas elles-mêmes des publications nuisibles.

> La capacité à double usage est une question de mesure dans le cadre de sécurité de chaque laboratoire. La question est de savoir si le modèle X a en substance développé la capacité de nouveaux utilisateurs à causer des dommages massifs dans le domaine de la biologie, de la chimie ou du réseau. La mesure directe est illégale et immorale. La mesure par procuration nécessite un modèle qui ne peut pas refuser les bases, mais le problème lui-même n'est pas une publication nocive.

## Le concept.

> **【中文解读】**"Yellow Zone" design: nécessite un processus dangereux qui permet de connaître mais pas de synthétiser directement la composition. Chaque question est examinée par des experts dans plusieurs domaines, conformément aux règles de contrôle des exportations de l'ITAR/EAR.

### La "zone jaune"

Les questions qui nécessitent une connaissance proche d'un processus nocif sans être une recette de synthèse directe. " Quel réactif catalyse l'étape 4 de [route publiée] ? " et non " comment faire [compound dangereux] ? " Chaque question examinée par plusieurs experts de domaine; filtrée pour la conformité ITAR/EAR aux contrôles d'exportation.

> Il faut approcher les processus nocifs pour obtenir des connaissances mais pas directement des formulations synthétiques.

Au total, 4 157 questions:
- Biosecurité: 1 520
- Sécurité informatique: 2 225
- Chimique: 412

>  total de 4 157  道题: sécurité biologique 1 520 网络安全 2 225 化学 412 ⋅

Les modèles répondent sans être invités à aider à quoi que ce soit; la capacité peut être mesurée sans provoquer un comportement nuisible.

> 选择题格式──模型在不被要求协助任何有害活动的情况下回答; capacité peut être mesurée dans le cas où aucun comportement nocif ne peut être provoqué──

> **【中文解读】**RMU: utilisation de LLaMa-2-7B, en réduisant le nombre de WMDP à près de la moyenne tout en maintenant MMLU et autres capacités générales basées sur quelques centaines de points.

### RMU  Réprésentation Fausse direction pour désapprentissage

La méthode de désapprentissage associée. Appliquée à LLaMa-2-7B, réduit les scores de WMDP à presque aléatoire tout en préservant MMLU et autres critères de référence de capacité générale dans quelques points de pourcentage. La méthode publiée est la ligne de base de désapprentissage pour chaque article de désapprentissage bio-chimique-cyberconcentré ultérieur.

> Le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la

### Le récit édifiant 2024-2025

Trois phases:

> Trois étapes:

1. **2024 "mild uplift."**Les premières évaluations d'OpenAI et d'Anthropic Preparedness/RSP ont rapporté de petits avantages par rapport à la recherche sur Internet pour les débutants qui tentent des tâches bio-adjacentes.

> **2024 年"轻微提升"。**Le modèle de rapport d'évaluation précoce n'a que quelques avantages pour les nouveaux utilisateurs.

2. **April 2025 "on the cusp."**Le Cadre de préparation d'OpenAI v2 a rapporté des modèles " sur le point d'aider significativement les novices à créer des menaces biologiques connues. " Pas une revendication de capacité  un avertissement que le seuil est proche.

> **2025 年 4 月"即将突破"。**OpenAI PF v2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

3. **Anthropic's 2025 bioweapon-acquisition trial.**Une étude contrôlée avec des participants débutants, mesurée de succès relatif dans les tâches de phase d'acquisition. augmentation de 2,53 fois rapportée. insuffisante pour exclure ASL-3 (leçon 18)  le seuil de la politique d'échelle responsable d'Anthropic de niveau 3 est atteint ou approché.

> **Anthropic 2025 年生物武器获取试验。**Pour les nouveaux participants à la recherche de mesure, le taux de réussite des tâches à la phase d'obtention du rapport a augmenté de 2,53 fois, ce qui ne suffit pas à exclure l'ASL-3:

> **【拓展：新手相对提升 vs 专家绝对能力 → 安全案例构建】**Les nouveaux connaissent très peu, même si l'information de modération est aussi très utile; les experts absolument compétents sont des experts de haute planche qui savent ce que cela demande et comment l'expliquer.

### Le débutant relatif contre l'expert absolu

Une distinction cruciale:

> 关键区分:

- **Novice-relative uplift.**Le modèle aide- t- il un non-expert? Multiplicatif. L'avantage relatif est élevé parce que les débutants savent peu; même des informations modestes peuvent aider.

> **新手相对提升。**Les modèles sont très utiles pour les non-experts.

- **Expert-absolute capability.**Le modèle produit combien d'informations avec le maximum d'efforts? Un expert peut extraire plus qu'un novice.

> **专家绝对能力。**Le modèle produit-il beaucoup d'informations dans le plus grand effort ?

Les cas de sécurité (leçon 18) visent à la fois: "le modèle ne peut pas donner à un débutant suffisamment de relance pour l'exécuter" et "un expert ne peut pas extraire des informations du modèle qui n'a pas déjà été publié".

> Les deux sont également visés par: "Le modèle ne peut pas donner aux nouveaux suffisamment de promotion pour exécuter"

### Le piège de mesure

Le WMDP est un proxy de capacité, pas une mesure de déploiement. Un modèle qui obtient un score élevé sur le WMDP peut ou non être exploitable par un débutant dans la pratique, selon:
- Résistance à l'évitement (combien il est difficile de retirer la capacité sans démarrer les filtres de sécurité)
- Connaissance tacite (capacité qui nécessite des compétences en laboratoire humide, pas des informations)
- Les obstacles à l'exécution (achats, équipements)

> Le WMDP est un agent de capacité, pas un déploiement de mesure.

L'essai d'acquisition d'armes biologiques d'Anthropic en 2025 ajoute la couche d'élicitation des débutants en plus de la capacité de style WMDP: il mesure le succès réel de la tâche, pas la capacité de choix multiples.

> L'Anthropic 2025 BioWare acquisition test a ajouté un nouveau niveau de capacité à la WMDP: la réussite des tâches réelles au lieu de la capacité de choix multi-objectifs.

### Là où cela s'inscrit dans la phase 18

Les leçons 12-16 sont les outils d'attaque et de défense sur les sorties de modèle. La leçon 17 est la couche de capacité à double usage  la mesure que les cadres de sécurité frontaliers (leçon 18) évaluent. La leçon 30 ferme l'arc avec les preuves actuelles de 2026 cyber/bio/chimie/élévation nucléaire.

> Les leçons 12-16 sont des outils de défense et d'attaque du modèle. La leçon 17 est une mesure de la capacité à double usage du niveau de l'évaluation du cadre de sécurité de l'avant-garde.

> **【拓展：测量陷阱 → 能力代理非部署测量】**Le WMDP est un agent de capacité, pas une mesure de déploiement. Le modèle de WMDP est un modèle qui peut être utilisé par les nouveaux utilisateurs dans la pratique. Il dépend de la difficulté de l'obtention de résistance.

## Utilisez-le.
```figure
al-wmdp-yellow-zone
```

## Utilisez-le

`code/main.py`Un modèle de simulation est testé sur des questions encastrées dans des catégories; des scores par domaine sont rapportés. Une simple intervention de désapprentissage (réprésentation zéro-sauf spécifique au domaine) réduit les scores; vous pouvez mesurer le compromis par rapport à la capacité générale.

> `code/main.py` Construire un cadre d'évaluation de la forme WMDP 模拟模型在分类问题上测试; rapporter le score de chaque domaine  simple oubli de prévention et de réduction du score; vous pouvez mesurer le poids des capacités générales 

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-wmdp-eval.md`. Compte tenu d'une affirmation de capacité à double usage ("notre modèle n'aide pas significativement les armes biologiques"), il vérifie: quels critères de référence ont été exécutés, quel chemin de refus a été utilisé pour l'évaluation (completion brute par rapport aux objectifs politiques) et si les études d'élicitation novices complètent le résultat de choix multiples.

> 本课产 出 `outputs/skill-wmdp-eval.md` Déclaration de capacité à double usage, audit: quels critères ont été mis en œuvre, quelles méthodes ont été utilisées pour évaluer les refus, et comment les résultats de la recherche ont-ils été complétés?

## Les exercices

1. On court .`code/main.py`- Rapporter la précision par domaine avant et après la phase de désapprentissage du jouet.

2. Augmentez le WMDP avec un quatrième domaine (par exemple, radiologique). spécifiez deux types de questions illustratives dans la zone jaune. Expliquez pourquoi la rédaction de telles questions est plus difficile que l'ajout de questions en forme de MMLU.

3. Lisez la section 5 du WMDP 2024 (méthodologie RMU). Décrire une approche de désapprentissage plus simple (par exemple, supprimer les neurones top-k pour le contenu de domaine) et décrire son coût de capacité générale attendu.

4. L'essai d'acquisition d'armes biologiques d'Anthropic 2025 rapporte une hausse de 2,53 fois. Décrivez deux façons dont ce nombre pourrait être biaisé vers le haut (dimension d'échantillon novices, fidélité à la tâche) et deux vers le bas (plafond d'élicitation, clôture de sécurité du modèle).

5. Expliquer ce qu'un cas de sécurité pour l'ASL-3 exige en plus de passer le WMDP. Nommer au moins deux études complémentaires d'élicitation.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| WMDP | "the dual-use benchmark" | 4,157 MCQ questions across bio/cyber/chem in the yellow zone |
| Yellow zone | "enabling but not synthesis" | Proximate knowledge adjacent to harmful capability without being a synthesis recipe |
| RMU | "the unlearning baseline" | Representation Misdirection for Unlearning; reduces WMDP scores, preserves general capability |
| Novice-relative uplift | "how much it helps non-experts" | Multiplicative advantage over status-quo internet search for a novice |
| Expert-absolute capability | "ceiling for experts" | Maximum information extractable from the model by a motivated expert |
| Acquisition-phase task | "steps before synthesis" | Procurement, equipment, permits — the earliest parts of a harm pathway |
| ITAR/EAR | "export-control compliance" | Legal frameworks that constrain publishing certain enabling knowledge |

## Encore une lecture

- [Li et al. — The WMDP Benchmark (arXiv:2403.03218, ICML 2024)](https://arxiv.org/abs/2403.03218) le rapport de référence et le papier RMU
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) "sur le bord"
- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) Le seuil de bio de l'ASL-3 et les résultats des essais d'acquisition
- [DeepMind — Frontier Safety Framework v3.0 (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) LCC de bio-élévation
