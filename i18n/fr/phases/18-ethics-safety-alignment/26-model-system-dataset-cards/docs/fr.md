# Modèle, système et cartes de données

> Trois formats de documentation structurent la transparence de l'IA. Les cartes modèle (Mitchell et coll. 2019)  Étiquettes nutritionnelles pour les modèles: données de formation, analyses quantitatives désagrégées, considérations éthiques, avertissements; seulement 0,3% des cartes modèles Hugging Face documentent des considérations éthiques (Oreamuno et coll. 2023). Fiches de données pour les ensembles de données (Gebru et coll. 2018, CACM)  motivation, composition, processus de collecte, étiquetage, distribution, entretien; analogie électronique-fichier de données. Les cartes de données (Pushkarna et coll., Google 2022)  détails modulaires en couches (téléscopiques, périscopiques, microscopiques) en tant qu'objets de limite pour divers lecteurs. Les développements de 2024 à 2025: génération automatisée via des LLM (CardGen, Liu et coll. En ce qui concerne les données relatives aux données de téléchargement, le rapport de référence de la Commission a été établi en vue de la réalisation de la nouvelle version de la carte de modèle (Liang et coll. Les certificats vérifiables (Laminator, Duddu et coll. Les États membres ont également adopté des mesures de répartition des données sur les données relatives aux données de l'Union européenne. Le 1er juillet 2025); les cartes réglementaires UE/ISO émergentes. Les cartes système (Sidhpurwala 2024; transparence au niveau du système méta; "Bluprints of Trust" arXiv:2509.20394)  documentation complète du système d'IA couvrant les capacités de sécurité, la protection par injection rapide, la détection des données d'exfiltration, l'alignement avec les valeurs humaines.

> **【中文解读】**Ce chapitre présente les modèles/systèmes/dataset cardésAI 系统透明度的标准化文档──三种文档格式各有不同的透明度范围:Model Cards(Mitchell 等人 2019)模型的营养标签;Data Sheets for Datasets(Gebru 等人 2018)数据集的电子规格书;System Cards端到端AI 系统文档──

> **【拓展：采用率 → 0.3% 问题】**Oreamuno et autres 2023  Audit Hugging Face 模型卡 发现只有0.3% 记录伦理考量。Liang 等人 2024 发现详细模型卡与高达29%的下载增加相关采用压力现在是市场驱动的,不仅是合规驱动的──自动化生成(CardGen, Liu 等人 2024) 和可验证证明(Laminator, Duddu 等人 2024) 解决长期采用问题──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, model-card + datasheet + system-card generator) | **语言:** Python（标准库，模型卡 + 数据表 + 系统卡生成器）
**Prerequisites:** Phase 18 · 18 (safety frameworks), Phase 18 · 24 (regulatory) | **前置知识:** Phase 18 · 18 (安全框架), Phase 18 · 24 (监管)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**學本節前Please first master:Phase 18·18+24──三种透明度文档:模型卡 + 数据集卡 + 系统卡──
>  **【类比】**透明卡 = "protocol de produits de l'IA"―Model Cards = 营养标签(训练数据/分析/伦理);Data sheets = 电子元件规格书(数据集动机/组成/收集);System Cards = 整机蓝图(端到端系统)―问题:
> 🤔 详细卡 → 下载量 29%(HF 2024 数据)  Transparency has commercial value──2024-2025 ⇒ Nouvelle tendance:LLM Automatic Generating卡(CardGen)、可验证证明(Laminator)、可持续性报告(碳/水)。

## Objectifs d'apprentissage

- Décrivez la carte modèle Mitchell et coll. 2019 et la fiche de données Gebru et coll. 2018.
- Décrire la couche télescopique/périscopique/microscopique des cartes de données.
- Décrivez les cartes système et leur couverture de bout en bout.
- Définir trois développements de 2024 à 2025 (génération automatisée, attestations vérifiables, rapports sur la durabilité).

> 描述Michell 等人 2019 的原始模型卡和Gebru 等人 2018 的数据表──描述Data Cards 的望远镜/潜望镜/显微镜分层──描述系统卡 及其端到端覆盖──说明三个 2024-2025 年发展──

## Le problème .

Les cadres réglementaires (leçon 24) et les politiques de sécurité de laboratoire (leçon 18) exigent toutes deux de la documentation. Les formats de documentation ont évolué de modèles spécifiques (carte modèle) à des ensembles de données spécifiques (fiches de données) à des systèmes spécifiques (carte système). Chacun aborde une portée différente de transparence.

> Le cadre de surveillance et la politique de sécurité des laboratoires exigent des documents. Le format du document va de la modélisation spécifique à la collecte de données spécifique à la mise en œuvre du système spécifique.

## Le concept.

> **【中文解读】**Les cartes de modèle 九大板块:模型详情、预期用途、因素 (relatives population or environmental factors) 、指标、评估数据、训练数据、定量分析 (按因素分解) 、伦理考量、注意事项和建议――Data Cards(Google 2022) 三层缩放:望远镜级(非专家高层摘要) 、潜望镜级(ML 从业者中层概览) 、微镜级(审计员显详特征级文档) ⋅

### Les cartes modèle (Mitchell et coll. 2019)

Les sections:
- Des détails du modèle.
- Utilisation prévue.
- Facteurs (facteurs démographiques ou environnementaux pertinents à évaluer).
- Les métriques.
- Les données d'évaluation.
- Données de formation.
- Analyse quantitative (décomposée par facteur).
- Des considérations éthiques.
- Des cavernes et des recommandations.

Problème d'adoption: Oreamuno et collègues ont constaté en 2023 que 0,3% des documents concernant les considérations éthiques étaient des cartes modèle Hugging Face.

### Les fiches de données pour les ensembles de données (Gebru et coll. 2018)

Analogie électronique-fichier de données.
- Motivation (pourquoi le jeu de données a été créé).
- Composition (ce qui est dedans).
- Processus de collecte (comment il a été assemblé).
- Étiquetage (le cas échéant).
- Utilisations (intentionnées, interdites, risques).
- La distribution.
- - Je suis en service.

Publié dans CACM 2021. La feuille de données est la documentation en amont; la carte modèle dépend de l'exactitude de la feuille de données.

### Carte de données (Pushkarna et coll., Google 2022)

Détail en couches modulaires.
- **Telescopic.**Résumé de haut niveau pour les non-experts.
- **Periscopic.**Un aperçu de niveau moyen pour les praticiens de l'IM.
- **Microscopic.**Documentation détaillée au niveau des caractéristiques pour les auditeurs.

Cadrage des objets frontaliers: différents lecteurs extraient des informations différentes du même document.

> **【拓展：System Cards → 部署层透明度】**La couverture des cartes système de fin à fin 系统 系统 comprenant le modèle+ sécurité+ déploiement sur la suite. Le type de bloc: sécurité capacité、 suggestion de protection、 données externe de dépistage、 déclaration de valeurs humaines de la même façon 事件响应。"Bluprints of Trust" ((arXiv:2509.20394) 系统卡 形式化为模型卡的部署层补充──EU AI Act GPAI 代码实践透明度章节要求模型卡作为合规工件──

### Carte de système

Scope: système d'IA de bout en bout comprenant le modèle + stack de sécurité + contexte de déploiement.
- Les capacités de sécurité.
- Protection contre les injections rapides.
- Détection des données par exfiltration.
- L'alignement avec les valeurs humaines déclarées.
- Réaction à l'incident.

Sidhpurwala 2024 et le travail de transparence au niveau du système Meta. " Blueprints of Trust " (arXiv:2509.20394) formalite la carte système comme complément à la couche de déploiement des cartes modèle.

> **【中文解读】**2024-2025 Développement:CardGen(Liu 等人 2024) Grâce à la LLM Automatic Generating Model Card, rapport de plus en plus d'objectivité que de nombreuses cartes artificielles;Laminator(Duddu 等人 2024) grâce à la signature TEE/crypto réaliser la preuve de validation permettant au modèle de transporter une déclaration de validation et non pas seulement une déclaration; Sustainable characteristics 段(Jouneaux 等人

### Les événements de 2024 à 2025

- **CardGen (Liu et al. 2024).**Génération automatique de cartes modèle via LLM; rapporte une objectivité plus élevée que de nombreuses cartes d'auteur humain sur les champs standardisés Mitchell 2019.
- **Download correlation (Liang et al. 2024).**Les cartes de modèle détaillées corrélatives à des taux de téléchargement jusqu'à 29% plus élevés sur la pression d'adoption de HF  sont désormais orientées par le marché, et non seulement par la conformité.
- **Laminator (Duddu et al. 2024).**Les attestations vérifiables par voie de TEE matérielle / signatures cryptographiques  permettent au modèle de carte de porter une preuve de réclamation, pas seulement une réclamation.
- **Sustainability (Jouneaux et al. July 2025).**Ajout de carbone, d'eau et d'empreinte énergétique; normes ISO émergentes.
- **Regulatory cards.**La loi sur l'IA de l'UE (leçon 24) Le chapitre du code de pratique du GPAI sur la transparence exige que les cartes modèle soient un élément de conformité.

### Là où cela s'inscrit dans la phase 18

Les leçons 24-25 sont les couches réglementaire et CVE. La leçon 26 est la couche de documentation. La leçon 27 est la gouvernance des données de formation, qui est la feuille de données en amont. La leçon 28 est l'écosystème de recherche qui produit des évaluations référencées dans les cartes.

> Les leçons 24-25 sont la surveillance et la CVE. Les leçons 26 sont les documents. Les leçons 27 sont la formation en gestion des données. Les leçons 28 sont la production de cartes de référence pour évaluer le système de recherche.

> **【拓展：可验证证明 → Laminator】**Laminator (Duddu et autres) utilise des signatures TEE / 加密硬件 pour réaliser des preuves de validation permettant aux modèles de transporter des déclarations de preuve et non seulement des déclarations. Par exemple, un module de carte peut transporter des " Y% de précision dans le ensemble de données X ", un vérificateur peut vérifier la preuve sans avoir besoin de recourir à une évaluation. Ceci est particulièrement important pour la réglementation de la loi sur l'IA de l'UE, leçon 24.

## Utilisez-le.
```figure
an-card-scopes
```

## Utilisez-le

`code/main.py`Il est possible de vérifier le format et de comparer les trois champs.

> `code/main.py`Pour la mise en place de jouets, les modèles de cartes, de tableaux de données et de systèmes sont les plus petits. Chacun suit la structure du chapitre standard.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-card-audit.md`- En cas de carte modèle, de feuille de données ou de carte système, elle vérifie la couverture des sections, la désagrégation numérique et la présence d'attestations vérifiables.

> 本课产 出 `outputs/skill-card-audit.md` une carte de modèle, une carte de données ou une carte de système, une section d'audit, une décomposition numérique et une preuve de validité.

## Les exercices

1. On court .`code/main.py`- Inspecter les cartes générées. Identifier les sections faibles (pour les titulaires de places uniquement) et préciser les éléments de preuve qui les renforceront.

2. Élargir la carte modèle avec une analyse quantitative désagrégée sur deux groupes démographiques (leçon 20).

3. Lire Oreamuno et coll. 2023 sur le taux d'adoption de 0,3%. Proposer un changement structurel à la spécification du modèle de carte qui augmenterait l'adoption des considérations éthiques.

4. Laminator (Duddu et coll. 2024) utilise des TEE pour les attestations vérifiables.

5. Écrivez une carte système (carte système, pas carte modèle) pour un projet passé ou un déploiement hypothétique.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Model Card | "the Mitchell card" | Mitchell et al. 2019 standard documentation for ML models |
| Datasheet | "the Gebru datasheet" | Gebru et al. 2018 standard documentation for datasets |
| Data Card | "the Pushkarna card" | Google 2022 modular layered data documentation |
| System Card | "the deployment card" | End-to-end AI system documentation including safety stack |
| Boundary object | "different readers, one doc" | Data Cards framing: same document serves diverse audiences |
| Verifiable attestation | "the Laminator attestation" | Cryptographic or TEE proof attached to a documentation claim |
| Sustainability field | "carbon / water footprint" | Emerging 2025 addition for environmental accounting |

## Encore une lecture

- [Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993, FAT* 2019)](https://arxiv.org/abs/1810.03993) la carte modèle canonique
- [Gebru et al. — Datasheets for Datasets (CACM 2021, arXiv:1803.09010)](https://arxiv.org/abs/1803.09010) papier de feuille de données
- [Pushkarna et al. — Data Cards (Google 2022)](https://arxiv.org/abs/2204.01075) documentation de données en couches
- [Sidhpurwala et al. — Blueprints of Trust (arXiv:2509.20394)](https://arxiv.org/abs/2509.20394) Formalisation de la carte système
