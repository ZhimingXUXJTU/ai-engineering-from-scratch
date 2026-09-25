# L'équipe rouge: PAIR et attaques automatisées

> Chao, Robey, Dobriban, Hassani, Pappas, Wong (NeurIPS 2023, arXiv:2310.08419). PAIR  Rapid Automatic Iterative Refinement  est le jailbreak automatique de boîte noire canonique. Un LLM attaquant avec un système de red-team prompt propose à plusieurs reprises des jailbreaks pour un LLM cible, en accumulant des tentatives et des réponses dans son propre historique de chat comme rétroaction dans le contexte. PAIR réussit généralement dans les 20 requêtes, des ordres de magnitude plus efficaces que GCG (la recherche de gradients au niveau des jetons de Zou et coll.), et sans avoir besoin d'accès à la boîte blanche. PAIR est maintenant une ligne de base standard dans JailbreakBench (arXiv:2404.01318) et HarmBench, aux côtés de GCG, AutoDAN, TAP et Persuasive Adversarial Prompt.

> **【中文解读】**Ce chapitre présente une méthode d'évaluation de la sécurité du système de contrôle des équipes rouges, utilisant des attaques automatisées pour détecter les lacunes de l'IA 系统.

> **【拓展：PAIR → GCG → 攻击家族谱系】**GCG(Zou 等人 2023) dans le cadre de la recherche de la formation, il faut une boîte blanche pour accéder à la formation, produire des liens indétectables.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, mock PAIR loop against a toy target) | **语言:** Python（标准库，针对玩具目标的模拟 PAIR 循环）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 14 (Agent 工程)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Pour les étudiants, il est nécessaire de se préparer à la phase 18 de la formation.
>  **【类比】**PAIR = "AI autoauto-cherche de la faille"――手工红队 = 人写越狱(慢);PAIR = 攻击 LLM 看目标 LLM 反应,代改进(通常 20 查询内成功,比 GCG 快几个数级)―JailbreakBench/HarmBench 标准基线。

## Objectifs d'apprentissage

- Décrire l'algorithme PAIR: prompt du système d'attaque, raffinement itératif, rétroaction dans le contexte.

> 描述 PAIR 算法: attaquant系统提示、代改进、上下文反──

- Expliquez pourquoi PAIR est strictement plus efficace que GCG lorsque la cible est la boîte noire.

> Expliquez pourquoi PAIR dans le but est plus strict que GCG.

- Nombre de quatre autres lignes de base d'attaque automatisée (GCG, AutoDAN, TAP, PAP) et indiquez une caractéristique distinctive de chacune.

> 列出其他四种自动化攻击基线 (GCG, AutoDAN,TAP,PAP)及各自的区分特征──

- Décrivez les protocoles d'évaluation JailbreakBench et HarmBench et ce que signifie " taux de réussite des attaques " sous chacun d'eux.

> description de l'accord d'évaluation de JailbreakBench et HarmBench ainsi que de leur " taux de réussite des attaques ":

## Le problème .

Le red-teaming était une activité manuelle. Un petit nombre de testeurs experts ont construit des instructions adversitaires et suivi celles qui fonctionnaient. Cela n'est pas à l'échelle: le taux de réussite des attaques a besoin d'un échantillon statistique, et la cible est une cible mobile avec chaque version du modèle. PAIR opère le red-teaming comme un problème d'optimisation avec une cible de boîte noire.

> Le test des équipes rouges est un mouvement manuel. Une minorité de testateurs spécialisés construisent des suggestions et suivent les éléments qui sont efficaces.

## Le concept.

> **【中文解读】**PAIR 算法流程:输入目标 LLM T、评判 LLM J、攻击者 LLM A、目标字符串 G、预算 K(ordinairement 20 查询) 循环 k=1..K:A 根据目标和历史(提示,响应) contre émission de nouvelles suggestions p_k; soumettre p_k 到 T 获得响应 r_k; J 评分; si le nombre de particules dépasse值则停止; sinon se ajoute à l'histoire continue。NeurIPS 2023 结果: contre GPT-3.5-turbo 和 Llama-2-7B-chat 攻击成功率 >50%, le nombre moyen de réussite des requêtes dans la gamme 10-20 范围──

### Algorithme de paiement

Les entrées:
- Cible LLM T (le modèle que nous attaquons).
- Le juge LLM J (se marque si une réponse est une jailbreak).
- Attacker LLM A (l'optimisateur de l'équipe rouge).
- C'est une ligne de but G: "répondez avec [instruction nuisible]."
- Budget K (généralement 20 requêtes).

> 输入: objectif LLM T(我们攻击的模型) 评判 LLM J(评分响应是否越狱) 攻击者 LLM A(红队优化器) 目标字符串 G("用[有害指令]响应") 预算 K(通常 20 查询) ⋅

Boucle, pour k en 1..K:
1. A est incité par l'objectif G et l'historique des paires (prompte, réponse) jusqu'à présent.
2. Un émet une nouvelle demande de p_k.
3. Envoyer p_k à T; recevoir une réponse r_k.
4. J marque (p_k, r_k) sur le but.
5. Si le score >= seuil, arrêtez  jailbreak trouvé.
6. Sinon, ajoutez (p_k, r_k) à l'historique de A; continuez.

> 循环 k=1..K:1. A 被提示目标 G 和历史(提示,响应) 对──2. A 发发新提示 p_k──3. 提交 p_k 到 T;接收响应 r_k──4. J 评分(p_k, r_k) ・・・5.

Résultat empirique (NeurIPS 2023): > 50% taux de réussite des attaques contre GPT-3.5-turbo, Llama-2-7B-chat; requêtes moyennes à succès dans la plage 10 à 20.

> 实证结果(NeurIPS 2023): pour GPT-3.5-turbo、Llama-2-7B-chat  taux de réussite d'attaque > 50%; nombre moyen de requêtes de réussite dans la gamme 10-20 ⋅

### Pourquoi PAIR est efficace

GCG (Zou et coll. 2023) recherche les suffixes de jetons adversitaires par gradient; il nécessite un accès à un modèle de boîte blanche et produit des suffixes illisibles. PAIR est une boîte noire et produit des attaques en langage naturel qui se transférent entre les modèles.

> GCG 通过梯度搜索对抗性令牌后;需要白盒访问且产生不可读后──PAIR est une boîte noire, produisant un modèle de migration de l'attaque du langage naturel──PAIR's 上下文反让攻击者从每次拒绝中学习; GCG 没有等价机制──

### Attaques automatisées connexes

- **GCG (Zou et al. 2023, arXiv:2307.15043).**La recherche de suffixes adversitaires au niveau des jetons.

> **GCG（Zou 等人 2023）。**Il est également possible de trouver des informations sur les différents types de données.

- **AutoDAN (Liu et al. 2023).**La recherche évolutionniste des instincts, guidée par un objectif hiérarchique.

> **AutoDAN（Liu 等人 2023）。**进化搜索提示, par le niveau de recherche

- **TAP (Mehrotra et al. 2024).**Arbre d'attaques avec taille  branches multiples déploiements de style PAIR.

> **TAP（Mehrotra 等人 2024）。**Les attaques de la branche ont été lancées.

- **PAP (Zeng et al. 2024).**Les instructions adverse persuasives  encodent les techniques de persuasion humaine comme des modèles de persuasion.

> **PAP（Zeng 等人 2024）。**L'homme doit être convaincu de la capacité de l'homme à se convaincre de la réalité.

> **【拓展：ASR 指标 → 评估陷阱】** taux de réussite des attaques ASR) doit être rapporté dans un budget de requête fixe 90% ASR dans 200 requêtes et 85% ASR dans 20 requêtes sont incomparables Justice de qualité est également le moteur du rapport ASRGPT-4-turbo Justice et Llama Guard Justice contre la même attaque peut donner des scores différents En comparaison, les attaques doivent être adaptées au budget et à la détermination des évaluations 

### JailbreakBench et HarmBench

Les deux (2024) standardisent l'évaluation:

> 两者(2024) est une évaluation standardisée:

- JailbreakBench (arXiv:2404.01318). 100 comportements nuisibles dans 10 catégories de politiques OpenAI. Taux de réussite des attaques (ASR) comme la métrique principale.

> Le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 et le nombre de cas de violation de la loi est de 10 à 10 ans.

- HarmBench (Mazeika et coll. 2024). 510 comportements dans 7 catégories, avec des tests de dommages sémantiques et fonctionnels. Compares 18 attaques contre 33 modèles.

> HarmBench:510 个行为,横跨 7 个类别,包含语义和功能性危害测试──比较 18 种攻击对33 模型──

Les attaques comparées nécessitent des budgets correspondants; une RSA de 90% à 200 requêtes n'est pas comparable à une RSA de 85% à 20.

> Les RSA sont généralement reportées sous le budget de la demande fixe. Les attaques comparées doivent être correspondues au budget.

> **【中文解读】**2026 année de déploiement signification: chaque avant-bord de laboratoire est actuellement en cours de publication avant de lancer un modèle de production de PAIR et TAP.

### Pourquoi il importe pour les déploiements de 2026

Chaque laboratoire frontalier effectue désormais des tests de PAIR et de TAP contre des modèles de production avant leur sortie.

> Chaque laboratoire de première ligne est actuellement en cours de publication pour le modèle de production de PAIR et TAP.

### Là où cela s'inscrit dans la phase 18

La leçon 12 est la base de l'attaque automatisée. La leçon 13 (Many-Shot Jailbreaking) est une exploitation complémentaire de longueur. La leçon 14 (ASCII Art / Visual) est une attaque de codage. La leçon 15 (Indirect Prompt Injection) est la surface d'attaque de production de 2026. La leçon 16 couvre les homologues de l'outil de défense (Llama Guard, Garak, PyRIT).

> Leçon 12 est la base de l'attaque automatisée. Leçon 13 est la longueur d'utilisation de l'interaction. Leçon 14 est la programmation de l'attaque. Leçon 15 est la production d'attaques de 2026. Leçon 16 couvre les outils de défense.

> **【拓展：TAP 和 PAP → 攻击进化】**TAP(Mehrotra 等人 2024) a lancé et a coupé des branches pour étendre le PAIR ASR mais plus calcul──PAP(Zeng 等人 2024) va mettre en place une technologie de convaincre l'humanité en tant que modèle de suggestion── attaquer la famille de la recherche des cartes blanches du GCG à l'amélioration des cartes noires du PAIR, à la recherche des arbres du TAP et de l'architecture sociale du PAP── chaque génération est plus forte à différents niveaux d'attaque.

## Utilisez-le.
```figure
al-pair-loop
```

## Utilisez-le

`code/main.py`Le juge note la réponse. Vous regardez l'attaquant réussir dans ~5-15 itérations contre le filtre de mots clés et échouer contre un filtre sémantique.

> `code/main.py`Construire un cycle de paiement de jouets. L'objectif est de rejeter les suggestions " évidentes " nocives.  Les attaquants sont des éditeurs de règles de tentative de libération, de rôle-rôle et de codage.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-attack-audit.md`- compte tenu d'un rapport d'évaluation de l'équipe rouge, il vérifie: quelles attaques ont été menées (PAIR, GCG, TAP, AutoDAN, PAP), à quel budget chacune a été menée, avec quel juge, sur quel comportement nocif a été mis en place (JailbreakBench, HarmBench, interne).

> 本课产 出 `outputs/skill-attack-audit.md` donner un rapport d'évaluation, un audit: quelles attaques ont été menées, quel est le budget de chaque attaque, quelles évaluatrices ont été utilisées, quelles sont les actions nocives.

## Les exercices

1. On court .`code/main.py`- Mesurer les requêtes moyennes à succès pour les trois stratégies d'attaque intégrées. Expliquer quelle hypothèse de défense cible exploite chacune.

2. Mettre en œuvre une quatrième stratégie d'attaque (p. ex., traduction dans une autre langue, codage base64) Rapporte les nouvelles requêtes moyennes à succès contre le filtre de mots clés et le filtre sémantique cible.

3. Lisez Chao et coll. 2023 Figure 5 (comparaison PAIR vs GCG). Décrivez deux scénarios où le GCG est préféré malgré l'avantage d'efficacité de PAIR.

4. JailbreakBench rapporte ASR contre un ensemble d'objectifs fixes. Concevoir une métrique supplémentaire qui mesure la diversité d'attaque (variance des demandes de succès). Expliquer pourquoi la diversité est importante pour l'évaluation de la défense.

5. TAP (Mehrotra 2024) étend PAIR avec branchage + taille.`code/main.py`et décrire le coût computationnel par rapport au taux de réussite.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| PAIR | "automated jailbreak" | Prompt Automatic Iterative Refinement; attacker-LLM + judge-LLM loop |
| GCG | "gradient jailbreak" | White-box token-level gradient search for adversarial suffixes |
| Attack success rate (ASR) | "% jailbreaks at k queries" | Primary metric; must be reported with query budget and judge identity |
| Judge LLM | "the scorer" | LLM that grades whether a response satisfies the harmful goal |
| JailbreakBench | "the evaluation" | Standardized harmful-behaviour set with tagged categories |
| HarmBench | "the broader bench" | 510 behaviours, functional + semantic harm tests |
| TAP | "tree of attacks" | PAIR with branching + pruning; better ASR at higher compute |

## Encore une lecture

- [Chao et al. — Jailbreaking Black Box LLMs in Twenty Queries (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) Papers de l'entreprise, NeurIPS 2023
- [Zou et al. — Universal and Transferable Adversarial Attacks on Aligned LLMs (arXiv:2307.15043)](https://arxiv.org/abs/2307.15043) papier GCG
- [Chao et al. — JailbreakBench (arXiv:2404.01318)](https://arxiv.org/abs/2404.01318) évaluation standardisée
- [Mazeika et al. — HarmBench (ICML 2024)](https://arxiv.org/abs/2402.04249) évaluation plus large
