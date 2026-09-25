# La confidentialité différentielle pour les LLM 差分隐私 LLM

> Le DP-SGD reste la norme  les mises à jour de gradients injectées par bruit offrent des garanties formelles (epsilon, delta). Les coûts généraux en matière de calcul, de mémoire et d'utilité sont importants; la configuration DP fine-tuning (LoRA + DP-SGD) à paramètres efficaces est la configuration commune de 2025 (ACM 2025). Deux corps de preuves en tension: l'inférence de l'adhésion canarienne (Duan et coll., 2024) rapporte un succès limité contre les modèles linguistiques; l'extraction de données de formation (Carlini et coll., 2021; Nasr et coll., 2025) récupère une mémorisation verbale substantielle. Résolution (arXiv:2503.06808, mars 2025): l'écart est dans ce qui est mesuré  canaries insérées par rapport aux données "plus extractibles". Les nouvelles conceptions canaries permettent des MIA basées sur des pertes sans modèles d'ombre et donnent le premier audit non trivial de DP d'un LLM formé sur des données réelles avec des garanties réalistes de DP. Les alternatives: PMixED (arXiv:2403.15638)  prédiction privée au moment de l'inférence par le biais d'un mélange d'experts sur les distributions de jetons suivants; génération de données synthétiques DP (Google Research 2024). Attaque émergente: Inversion différentielle de la vie privée via le retour de la MLL  fuite de la confiance.

> **【中文解读】**Ce chapitre présente la différence entre la confidentialité du LLM et la protection de la confidentialité des données des utilisateurs dans les méthodes mathématiques de formation et de réflexion.

> **【拓展：MIA vs 训练数据提取 → 衡量差距】**Les deux éléments de preuve de la période 2024-2025 sont formés Zhang力: Kim丝雀 MIA(Duan 等人 2024) Report on success of language models limited; train数据提取(Carlini 2021, Nasr 等人 2025) Récupérer une grande quantité de mémoire par mot.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les étudiants, il est nécessaire de préparer un programme de formation de formation en ligne.
>  **【类比】**DP = " données cachées "──DP-SGD dans le niveau d'injection de bruit, un seul échantillon n'affecte pas l'ensemble de l'entraînement→ la démonstration mathématique formalisée ne peut pas être tirée du modèle contre proposer un certain nombre de données dans l'entraînement collectif──代价:计算/内存/效用都明显下降──LoRA+DP-SGD est 2025 实用配置(((
> 🤔 困境: MIA 攻击失败 vs 训练数据提取成功差别在测什么(插入 vs 最易提取) ・・・2025.3 新金雀设计首次对真数据 LLM做非凡 DP 审计──

## Objectifs d'apprentissage

- Définir la confidentialité différentielle (epsilon, delta) et indiquer la recette DP-SGD.
- Expliquez la tension de 2024 à 2025: l'IA canarienne et l'extraction de données de formation donnent des images différentes.
- Décrivez le PMixED et pourquoi la prédiction privée de l'inférence-temps est une alternative à la formation en DP.
- Décrivez l'inversion différentielle de la confidentialité via l'attaque de rétroaction de la LLM.

> 定义 (epsilon, delta) -差分隐私并说明 DP-SGD 方法──解释 2024-2025 年张力:金丝雀 MIA vs 训练数据提取给出不同图景──描述 PMixED 及为什么推理时私有预测是 DP 训练的替代──描述通过LLM 反的差分隐私逆转攻击──

## Le problème .

Les LLM mémorisent. Carlini et coll. 2021 ont montré que les modèles de langage de production reproduisent le texte de formation littérale à la demande. DP est la défense formelle: entraîne de sorte que la sortie soit probablement insensible à un seul exemple de formation. Les preuves 2024-2025 montrent que DP-SGD est nécessaire mais que les valeurs ε déployées peuvent ne pas correspondre au modèle de menace.

> LLM 会记忆──Carlini 等人 2021 années de démonstration de production de langage modèle 可按需复现逐字训练文本──DP est une défense formalisée: entraînement rend le sort insensitif à tout seul modèle de formation──2024-2025 années de preuve montre DP-SGD est nécessaire mais la valeur ε possible de déploiement ne correspond pas au modèle de menace──

## Le concept.

> **【中文解读】**(epsilon, delta) -差分隐私定义:随机算法 M 是 (epsilon, delta) -DP 的, si pour n'importe quel deux phases de différence entre un exemple de données et tout événement S:P(M(D) dans S) <= e^epsilon * P(M(D') dans S) + delta。

### (ε, δ) - confidentialité différentielle

Un algorithme randomisé M est (ε, δ) -DP si pour deux ensembles de données différents dans un exemple et un événement S:
P(M(D) dans S) <= e^ε * P(M(D') dans S) + δ.

> 随机算法 M 是 (ε, δ) -DP 的, si pour n'importe quel exemple de données et événements S:P(M(D) dans S) <= e^ε * P(M(D') dans S) + δ。

Interprétation: la distribution de sortie est assez proche (paramétrisée par ε) pour que la contribution d'un seul individu ne puisse être déduite de manière fiable, sauf avec probabilité δ.

> Expliquer: la distribution de l'extérieur est assez proche (par é) et aucune contribution individuelle ne peut être concluée, sauf la probabilité δ──

### Département de la pêche

Abadi et coll. 2016. La recette standard:
1. Prenez un mini lot.
2. Compute les gradients par exemple.
3. Cliquez chaque gradient par exemple à un seuil C.
4. Sumer les gradients coupés et ajouter le bruit gaussien avec std σ * C.
5. Utilisez la somme bruyante pour mettre à jour les paramètres.

> DP-SGD standard method:1. 采样小批次──2. 计算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后梯度并添加高的噪音──5.

Le coût de la protection de la vie privée est suivi par un comptable (comptable de Moments, comptable de Rényi DP). Les valeurs ε rapportées dans la littérature LLM varient considérablement selon le modèle de menace, la sensibilité des données et la cible d'utilité; il n'y a pas de défaut universellement "sécurisé" ε. Les exemples publiés couvrent environ ε ≈ 110 dans certains paramètres de formation LLM, mais ce sont des exemples illustratifs  non recommandés. Le bas ε nécessite généralement plus de bruit et peut augmenter la perte d'utilité.

> Le coût de la vie privée par le compteur de suivi. Le rapport de la littérature équivaut à une valeur différente du modèle de menace.

### LOR + DP-SGD

Le DP-SGD complet d'un modèle frontalier est prohibitif. LoRA (Hu et coll. 2022) limite les mises à jour de gradient à un petit adaptateur, réduisant ainsi le stockage de gradient par exemple. LoRA + DP-SGD est la configuration commune de 2025.

> Total volume DP-SGD  entraînement préfrontal modèle coût trop élevé。LoRA  limite de la température mise à jour à des adaptateurs petits, réduire le stockage de la température par cas。LoRA + DP-SGD est la disposition habituelle de 2025。DP保证适用于适配器; le modèle de base reste fixe。

### La tension de 2024 à 2025

Deux lignes de preuve:

> 两条证据线:

- **Canary MIA (Duan et al. 2024).**Insérer des canaries uniques dans les données de formation, mesurer si un attaquant d'inference de membres peut les identifier. Rapports de succès limité sur les modèles de langage. Suggère que la MIA est difficile.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).**Précisez le modèle avec un préfixe; mesurez s'il récupère le texte littéral de la formation. Rapporte une mémorisation substantielle. Suggère que MIA est facile dans le sens pertinent.

> Le rapport MIA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

Résolution de mars 2025 (arXiv:2503.06808): les deux mesures différentes. MIA demande " est l'exemple e dans D ? " sur les canaries insérées. L'extraction demande " que puis-je récupérer de D ? " L'exemple " le plus extractible " est ce qui compte pour la vie privée; les canaries en rapportent moins parce qu'ils ne sont pas optimisés pour être extractibles.

> Résolution de mars 2025: Deux mesures différentes. La MIA pose la question "Exemple e est-il dans le D?", pose la question "Qu'est-ce que je peux récupérer de D?"

Les nouveaux designs canariens, les MIA basées sur des pertes sans modèles d'ombre, le premier audit non trivial de DP d'un LLM sur des données réelles avec des garanties réalistes de DP.

> MIA basée sur la perte du modèle sans ombre, pour la première fois, sur des données réelles, avec une DP réelle, assure une LLM, effectue un audit de DP inhabituel.

> **【拓展：PMixED → 推理时隐私】**PMixED(arXiv:2403.15638) fournit des prévisions privées lors de la prise de décision: dans le prochain jeton de distribution, les spécialistes voient une fraction des données de formation, se regroupent pour ajouter du bruit pour réaliser DP。 éviter complètement DP entraînement。DP 合成数据生成(Google Research 2024) utilisent LoRA 微调采样合成数据 DP-SGD, puis se classent dans les données de synthèse, puis se classent dans les deux différents modèles de menaces pour éviter le coût de l'efficacité de l'entraînement DP 完全量──

### Les alternatives à la formation en DP

- **PMixED (arXiv:2403.15638).**Prédiction privée au moment de l'inférence. mélange d'experts sur les distributions de jetons suivants; chaque expert voit une fragmentation de données de formation; aggregation ajoute du bruit pour DP. Évite complètement la formation DP.
- **DP synthetic data generation (Google Research 2024).**LoRA-fin-tune avec DP-SGD, échantillons de données synthétiques, entraînez un classificateur en aval sur les données synthétiques.

Les deux évitent le coût de l'utilité de la formation complète des DP au prix d'un modèle de menace différent.

> **【中文解读】**差分隐私逆转攻击(2025): utiliser le DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──防御:不暴露置信度,或在暴露前截断/量化──这是 (epsilon, delta) -DP 训练之外的额外要求──

### Réversion différentielle de la protection de la vie privée via le retour d'information du MLL

L'attaque de 2025 émerge. Utilisez les scores de confiance d'un modèle formé par DP comme un oracle pour identifier les individus. Même lorsque les sorties ne fuissent pas, les distributions de confiance peuvent.

> 2025: utilisation du modèle de formation DP  预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──

La défense: ne pas exposer les confidences, ou les truncer/quantifier avant l'exposition.

> 防御:不露置信度,或在露前截断/量化── ceci est une exigence supplémentaire en dehors de l'entraînement (ε, δ) -DP

### Là où cela s'inscrit dans la phase 18

Les leçons 20-21 sont les préjugés/l'équité. La leçon 22 est la vie privée. La leçon 23 est la provenance par marquage d'eau. La leçon 27 couvre la couche réglementaire de la provenance des données.

> Les leçons 20-21 sont préjugés/équité. Les leçons 22 sont intimité. Les leçons 23 sont de source de données. Les leçons 27 couvrent la surveillance des sources de données.

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】**L'utilisation de l'appareil est un facteur de référence pour la mise en place de l'appareil de stockage de données.

## Utilisez-le.
```figure
an-dp-clip-noise
```

## Utilisez-le

`code/main.py`Simulation du DP-SGD sur un ensemble de données de classification binaire de jouets. Vous pouvez analyser le multiplicateur de bruit σ et la norme de coupe C et suivre le budget (ε, δ) et le coût de précision. Une "attaque canarienne" insère un exemple de formation unique et mesure si un test de perte de journaux peut le détecter avant et après le DP.

> `code/main.py`Dans le jeu de jeu de catégorie 2, on peut analyser le nombre de bruits et les chiffres de coupe C, suivre (ε, δ) le budget et le coût de précision.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-dp-audit.md`. Compte tenu de la revendication de DP concernant le déploiement d'un modèle linguistique, elle vérifie: les valeurs (ε, δ), le comptable utilisé, le protocole d'évaluation des MIA et si des vecteurs d'exposition à la confiance ont été évalués.

> 本课产 出 `outputs/skill-dp-audit.md` Déclaration du DP sur la mise en œuvre du modèle de langage, audit: ((ε, δ) 值、l'utilisation de compteurs、MIA 评估协议以及 whether assessed the trust exposure volume。

## Les exercices

1. On court .`code/main.py`.Soufler σ dans {0,5, 1.0, 2.0} et signaler le compromis de précision (ε, δ).

2. Mettre en œuvre une insertion canarienne et un test de perte de journaux. Mesurer le taux de détection avant et après DP-SGD à σ = 1.0.

3. Lisez Nasr et coll. 2025 sur l'extraction de données de formation. Pourquoi le succès de l'extraction ne s'effondre pas sous la moyenne ε?

4. Conceptez un déploiement à l'aide de PMixED (arXiv:2403.15638) qui fonctionne entièrement au moment de l'inférence. Quel est le modèle de menace que PMixED aborde que DP-SGD ne fait pas?

5. Définir une contre-mesure qui limite la fuite du score de confiance et estime son coût de déploiement.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Encore une lecture

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) l'algorithme standard de formation en DP
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) le papier d'extraction canonique
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) IMM à succès limité
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) résolution de la tension
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) Prédiction privée de l'inférence-temps
