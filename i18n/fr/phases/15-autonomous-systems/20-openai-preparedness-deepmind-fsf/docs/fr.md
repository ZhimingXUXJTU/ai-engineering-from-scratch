# Le cadre de préparation d' OpenAI et le cadre de sécurité de la frontière de l' esprit profond

> OpenAI Preparedness Framework v2 (avril 2025) introduit les catégories de recherche  Autonomie à longue portée, sandbagging, réplique autonome et adaptation, soustraction des garanties  distinctes des catégories suivantes. Les catégories suivantes déclenchent des rapports sur les capacités ainsi que des rapports sur les garanties examinés par le groupe consultatif sur la sécurité. La FSF v3 de DeepMind (septembre 2025, avec des niveaux de capacité de suivi ajoutés le 17 avril 2026) replie l'autonomie dans les domaines de R&D et de cyber-médias (niveau d'autonomie de R&D de ML 1 = automatiser complètement le pipeline de R&D de l'IA à un coût compétitif par rapport aux outils humains + AI). La FSF v3 aborde explicitement l'alignement trompeur par la surveillance automatisée des abus de raisonnement par instrument. La note honnête: Les catégories de recherche dans PF v2 (y compris l'autonomie à longue portée) ne déclenchent pas automatiquement des atténuations; le langage de politique est "potentiel". DeepMind lui-même dit que la surveillance automatisée "ne restera pas suffisante à long terme" si le raisonnement instrumental se renforce.

> **【中文解读】**Ce chapitre présente les cadres de sécurité de l'IA à l'avant-garde de chaque laboratoire, la préparation à l'IA ouverte et la préparation à l'IA en profondeur.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Les résultats de la recherche ont été obtenus en raison de la présence de la plupart des chercheurs en laboratoire.
>  **【类比】**Les trois grandes entreprises de l'aviation ont été chargées de la gestion de la sécurité de l'aviation.
> 🤔 **【困惑】**Q: Pourquoi les RSP sont-ils volontaires ? Parce qu'il n'y a pas de loi obligatoire.

## Le problème , l' introduction du problème

La leçon 19 lit de près la politique d'échelle d'Anthropic. Cette leçon complète l'image en lisant OpenAI et DeepMind. Les trois documents sont des objets de cousin traitant de la même question  quand un laboratoire frontalier devrait-il faire une pause ou passer une porte sur un modèle  et ils convergent sur un petit ensemble de catégories et divergent dans des endroits spécifiques qui comptent.

> Le cours a été suivi en détail par la politique d'expansion de l'Anthropic. Ce cours a été suivi en détail par la politique d'OpenAI et de DeepMind pour compléter le tableau. Ces trois documents sont des pièces de même source, répondant à la même question:

La convergence: les trois étiquettes autonomie à longue portée comme une classe de capacités digne de suivi. Tous les trois reconnaissent que le comportement trompeur est une catégorie de risque spécifique. Les trois ont un organe d'examen interne. La divergence: OpenAI divise les catégories en "Tracked" (atténuation obligatoire) et "Research" (pas de déclencheur automatique). DeepMind divise l'autonomie en deux domaines plutôt que de la nommer séparément. Les noms du laboratoire sont Tracked vs Research, ou Critical vs Moderate, ou Tier-1 vs Tier-2; la conséquence opérationnelle de la cuve dans laquelle une capacité vit est différente entre les laboratoires.

> 收点: 三者都将长程自主标记为值得跟踪的能力类别──三者都承认欺骗行为──对齐伪装、沙包) 是特定风险类别──三者都有内部审查机构──分歧点:OpenAI将分为"Tracked"(强制缓解) 和"Research"(无自动触发)──DeepMind将自主性折叠成两个领域而非单独命名──实验室名称

La même capacité peut être "atténuation obligatoire" chez Anthropic, "monitorée mais non déclenchée" chez OpenAI, et "traquée dans un domaine spécifique" chez DeepMind.

> La même capacité en anthropologie est la "atténuation forcée", en OpenAI est la "monitricalisation mais non touchée", en DeepMind est la "trace dans un domaine spécifique".

## Le concept de base.

### Le cadre de préparation d'OpenAI v2 (avril 2025)

La structure:

> 结构:

- **Tracked Categories**Les rapports de mesures de sécurité (quels sont les mesures d'atténuation en place) sont examinés par le groupe consultatif en matière de sécurité avant le déploiement.
  Le mot grec traduit par " le mot grec "**Tracked Categories（跟踪类别）**Le rapport de sécurité a été publié en décembre 2009 par le groupe consultatif de sécurité.
- **Research Categories**Le projet de recherche a été lancé en décembre 1995 pour la mise en œuvre de la stratégie de recherche et de l'analyse des données de l'industrie de l'énergie et de l'énergie.
  Le mot grec traduit par " le mot grec "**Research Categories（研究类别）**Le laboratoire suit mais n'a pas encore promis de déterminer la capacité de modélisation de la réduction.

Le cadre clé dans v2: Les catégories de recherche ne déclenchent pas automatiquement des atténuations. Le langage de politique est les atténuations " potentielles ". C'est le delta spécifique à surveiller: l'emplacement d'une catégorie dans Tracked vs Research est la charnière entre " fermé " et " observé ".

> Le cadre clé de v2: Catégories de recherche Non automatiquement inciter à la résilience. Le langage politique est le " potentiel " de la résilience.

### Framework de sécurité de la frontière DeepMind v3 (septembre 2025; niveaux de capacité de suivi ajoutés le 17 avril 2026)

La structure:

> 结构:

- **Critical Capability Levels (CCLs)**: seuils de capacité dans cinq domaines: Cyber, Bio, R&D ML, CBRN, Autonomie (divisés en R&D ML et Cyber).
  Le mot grec traduit par " le mot grec "**Critical Capability Levels（CCL，关键能力等级）**Le développement de l'apprentissage de l'équipement et de la technologie (R&D)
- **Tracked Capability Levels**Exemple concret: ML R&D autonomie niveau 1 = automatiser pleinement le pipeline de R&D de l'IA à un coût compétitif par rapport aux outils humains + IA.
  Le mot grec traduit par " le mot grec "**Tracked Capability Levels（跟踪能力等级）**:2026  4 月 追加额外粒度──具体例: machine learning R&D autonomes 1 = 以与人类+AI 工具竞争的成本完全自动化AI 研发管道──
- **Deceptive alignment monitoring**: engagement explicite à la surveillance automatisée des abus de raisonnement par des instruments.
  Le mot grec traduit par " le mot grec "**欺骗对齐监控**: une volonté claire de contrôler l'automatisation de l'utilisation abusive des outils.

L'autonomie de l'encadrement diffère de celle d'OpenAI. DeepMind ne garde pas "Autonomy" comme un domaine de premier niveau; il est plié dans les domaines où l'autonomie causerait des dommages (ML R&D et Cyber). L'argument est que l'autonomie sans domaine est une capacité sans risque; le contre-argument est que l'autonomie entre domaines est un méta-risque que le cadre devrait nommer.

> Le concept de l'autonomie est un concept qui est en train de se développer. Il est également possible de décrire la capacité de l'autonomie dans un domaine différent de celui de l'OpenAI.

### Ce sur quoi les trois convergent

- Groupe consultatif en matière de sécurité interne (nommé Anthropic SAG, OpenAI SAG, comité interne DeepMind).
  Le groupe de travail de l'organisation de sécurité interne est un groupe de travail spécialisé dans la sécurité interne.
- mention explicite de l'alignement trompeur / de l'alignement simulé comme une classe de risque.
  Le mot " fraude " est traduit par " fraude ".
- Les documents permanents sur une cadence déclarée (Anthropic: Route-plan de sécurité frontalière, rapport de risque; OpenAI: rapports sur les capacités et les garanties; DeepMind: cycle de mise à jour du FSF).
  Le programme de formation de l'Agence de formation en matière de formation professionnelle (Agence de formation en sciences et sciences) a été lancé en juin dernier par le ministère de la santé et de l'environnement.
- Reconnaissance que les défenses de surveillance seulement ont un plafond. "La surveillance automatisée ne restera pas suffisante à long terme", explique DeepMind.
  Le profondeur de la pensée affirme que " l'automatisation de la surveillance ne durera pas assez longtemps ".

### Où ils divergent

- **Anthropic**: l'engagement de pause supprimé dans v3.0; le seuil de R&D-4 est le porte suivant nommé.
  Le mot grec traduit par " le mot grec "**Anthropic**:v3.0 移除暂停承诺;AI R&D-4 值是命名的下一个门控──
- **OpenAI**: Traqué vs recherche divisé; les catégories de recherche (y compris l'autonomie à longue portée) ne se feront pas automatiquement passer.
  Le mot grec traduit par " le mot grec "**OpenAI**:Tracked vs Research 分割;Categories de recherche(incluant le long de la route autonome)
- **DeepMind**: autonomie repliée sur d'autres domaines; les niveaux de capacité suivis ajoutent de la granularité en avril 2026.
  Le mot grec traduit par " le mot grec "**DeepMind**: autonomie de la pente vers d'autres domaines; Trace des niveaux de capacité en 2026

### Le sablebaging: une capacité spécifique qui complique les trois

Le sandbagging (un modèle qui a des performances stratégiques inférieures aux évaluations) est dans les catégories de recherche d'OpenAI. Le RSP v3.0 d'Anthropic le traite via le vide d'évaluation-context (leçon 1). DeepMind le traite via une surveillance trompeuse de l'alignement dans FSF v3.

> Sandbagging (模型在评估中战略性表现不佳) dans les catégories de recherche d'OpenAI 中──Anthropic RSP v3.0 通过评估上下文差距(第 1 课)处理──DeepMind 通过 FSF v3 的欺骗对齐监控处理──

Si un modèle de sable de sable sur les évaluations, les seuils de capacité de chaque cadre sont sous-estimés. Le cadre fonctionne seulement si la mesure fonctionne. C'est pourquoi la mesure externe (leçon 21, METR) et l'évaluation adversitaire sont nécessaires en plus de l'auto-évaluation en laboratoire.

> Si le modèle est évalué en interne, la capacité de chaque cadre est sous-estimée. Le cadre est seulement valable lorsque la mesure est effectuée. C'est pourquoi, en plus de l'évaluation en laboratoire, la mesure externe est nécessaire.

### La compétence en matière de lecture des politiques

- Localiser: chaque fonctionnalité qui vous intéresse doit être disponible dans la police.
  Le mot grec traduit par " le mot grec "**定位**Les politiques ne couvrent pas les politiques.
- Classifier: est-ce suivi (qui déclenche l'atténuation) ou la recherche (qui suit mais ne déclenche pas)?
  Le mot grec traduit par " le mot grec "**分类**: est suivi (ou recherché) (ou suivi mais non suivi)?
- Cadence: la politique est-elle mise à jour sur un calendrier déclaré ou seulement après des événements spécifiques?
  Le mot grec traduit par " le mot grec "**节奏**Le programme de mise à jour de la politique est-il seulement mis en place après un événement spécifique ?
- L'indépendance: est-elle obligatoire ou facultative ? partenaires anthropologiques avec Apollo et l'Institut américain de sécurité de l'IA; OpenAI avec METR; DeepMind avec SAG interne principalement.
  Le mot grec traduit par " le mot grec "**独立性**L'analyse externe est-elle obligatoire ou optionnelle ?Anthropic avec Apollo et l'Institut de sécurité de l'IA des États-Unis;OpenAI avec METR  coopération;DeepMind principal avec SAG interne;;

## Utilisez-le avec le cadre de réalisation
```figure
a5-tracked-vs-research
```

## Utilisez-le

`code/main.py`Il est également possible de trouver des solutions de gestion de la situation en fonction de la capacité de l'entreprise à utiliser des outils de gestion de la situation en fonction de la capacité de l'entreprise à prendre des décisions.

> `code/main.py`• réaliser des différences de performance dans les petites décisions, outils de détermination de la capacité à l'autonomie, à la fraude, à l'automatisation de la recherche, à la mise en place de réseaux, etc.), à la production de trois politiques, à la fois pour la classification de ces capacités et pour les atténuations qu'elles peuvent provoquer.

## Envoyez-le . Produit .

`outputs/skill-cross-policy-diff.md`produit une comparaison entre les politiques pour une capacité spécifique, en utilisant les trois cadres comme référence.

> `outputs/skill-cross-policy-diff.md`Pour déterminer la capacité de génération de politiques, utiliser trois cadres comme référence.

## Les exercices

1. On court .`code/main.py`. Confirmer que la sortie de l'outil diff correspond aux politiques pour au moins deux fonctionnalités que vous pouvez vérifier par rapport aux documents source.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmation des différences d'outils de sortie correspondant à au moins deux capacités de vérification des documents de source disponibles.

2. Lisez le Cadre de préparation OpenAI v2 en entier. Identifiez chaque catégorie de recherche. Pour chaque catégorie, écrivez une phrase sur la raison pour laquelle elle est dans la recherche plutôt que dans le suivi.
   Pour chaque article, une phrase explique pourquoi il est en recherche et non suivi.

3. Lisez la version complète de DeepMind FSF v3, ainsi que la mise à jour des niveaux de capacité de suivi d'avril 2026. Identifiez les critères d'évaluation spécifiques de l'autonomie de niveau 1 de R&D de ML. Comment le mesurerez-vous à l'extérieur?
   Le niveau de capacité de suivi de l'apprentissage de l'éducation à l'automatisation est un niveau de mesure spécifique de l'apprentissage à l'automatisation.

4. Le sandbagging est dans les catégories de recherche d'OpenAI. Concevoir une évaluation qui obligerait un modèle de sandbagging à révéler sa capacité réelle.
   Le modèle de la recherche de l'OpenAI est un outil de recherche qui permet de déterminer la capacité de l'entreprise à jouer à des jeux de hasard.

5. Comparez les trois politiques sur une capacité spécifique (votre choix). Nommez la classification de la politique que vous trouvez la plus rigoureuse et la moins rigoureuse.
   Traduction anglaise: comparer trois politiques dans une catégorie spécifique.

## Les termes clés

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Encore une lecture

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/)- L'annonce de v2.
  Le nom de la ville est le nom de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville.
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) document complet.
  Le texte de la lettre est écrit en français
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Annonce de FSF v3.
  La rédaction de la lettre de la FFS
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) Ajout des niveaux de capacité suivis.
  Le niveau de capacité de suivi
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) exemple d'un rapport de risque au format FSF.
  Exemple de rapport de la FSE
