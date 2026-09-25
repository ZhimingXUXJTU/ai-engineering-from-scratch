# Eagle-3 Décodage spéculatif en production

> Le décoding spéculatif associe un modèle rapide à celui cible. Le projet propose des jetons K; l'objectif est vérifié en un seul forward; les jetons acceptés sont gratuits. En 2026, EAGLE-3 est la variante de la classe de production  il entraîne un chef de projet sur les états cachés du modèle cible plutôt que sur les jetons bruts, poussant le taux d'acceptation alpha dans la bande de 0,6-0,8 sur le chat général. La bonne question n'est pas "combien rapide est le projet" mais "qu'est-ce que l'alpha sur mon trafic?" Si l'alpha tombe en dessous de ~0.55, le décoding spéculatif est négatif net à haute simultanéité parce que chaque projet rejeté coûte un deuxième passe cible. Cette leçon vous apprend à mesurer l'alpha d'abord et à tourner le drapeau en second.

> **【中文解读】**Ce chapitre présente la technique de la prédiction de la réflexion avec un petit modèle.
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

>  **【前置】**Je suis en train de faire une étude sur la façon dont les données sont utilisées pour la production de produits de base.
>  **【类比】**EAGLE-3 = "Translator 打草稿"──草稿模型(draft) Rapid guess K 个代币,目标模型一次验证──猜对=免费,猜错=多一次验证开销──EAGLE-3 创新:用目标模型隐藏状态训练草案(而非原始代币), acceptation rate α 提到 0.6-0.8──生产关键问题:α 在你的流量上多少?<0.55 时反而拖慢(拒绝的草案 浪费算力)必须先测α 再开旗──
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Nombre des trois générations de décoding spéculatif et expliquer ce que l'Eagle-3 change de l'Eagle-2 et d'un modèle classique de projet.
  Traduction anglaise: 说出推测解码的三代,并解释 EAGLE-3 相比Eagle-2 和经典草案 模型改变了什么──
- Définir le taux d'acceptation alpha, calculer l'accélération attendue à partir d'alpha et K (longueur du projet), et identifier l'alpha de rupture équilibrée pour votre concurrence cible.
  Traduction anglaise: définir taux d'acceptation alpha, de alpha 和 K(dépôt 长度) calculer le taux d'accélération prévisible,并确定目标并发下亏平衡 alpha──
- Expliquez pourquoi le décoding spéculatif est opt-in (pas par défaut) dans vLLM 2026 et pourquoi l'activer sans mesurer alpha est un modèle anti-production.
  Le système de calcul de la production de l'alpha est un système de calcul de l'alpha.
- Écrivez un plan de mesure: quel est le point de référence, quelle est la distribution de la demande, quel point de concurrence, quelle est la mesure à utiliser.
  Le programme de mesure est écrit en français: quel est le point de mise en œuvre du programme de mesure ?

## Le problème , l' introduction du problème

> **【中文解读】**La phase de déchiffrement de la hypothèse est celle de la capacité de stockage à large bande passante de chaque déchiffrement d'un jeton. Il faut lire environ 140 Go/s de poids, GPU calculer presque le vide. La phase de déchiffrement de la hypothèse est celle de générer des jetons candidats K avec un petit modèle bon marché, puis de faire en sorte que le modèle cible soit validé par tous les K une fois de plus. Le taux d'acceptation alpha est le seul indicateur important de déchiffrement de la hypothèse de déchiffrement de K à un niveau inférieur à 0,55 à un niveau élevé.

> **【拓展：推测解码的产业应用】**Google prévoit en 2025 de déployer des codes de déploiement dans les analyses de l'IA, en termes de qualité, sans perte de qualité.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补充全(延迟敏感)场景──但需要注意:高并发(256+)

Le décodeur est lié à la mémoire. Sur un H100 exécutant Llama 3.3 70B FP8, chaque jeton décodé lit ~ 140 Go / s de poids et émet un jeton. Le calcul de la GPU est presque inactif pendant le décode.

> Le code est limité en mémoire. En H100, chaque code est utilisé pour le Llama 3.3 70B FP8.

Le décoding spéculatif exploite le fossé. Générez des jetons candidats K avec un modèle de projet bon marché, puis demandez au modèle cible de vérifier tous les K dans un seul passe à l'avant. Chaque jeton vérifié est effectivement gratuit (amortisé dans un lot de K à l'avant que la cible aurait dû faire de toute façon).

> 推测解码利用这个差距――Utiliser un projet bon marché 模型 générer K 个候选标签, puis faire que le modèle objectif vérifie tous les K 个在一次前向传播中―― chaque token passé par la vérification 实际上是免费的(分摊到目标模型应该做的 K 批前向中)。

L'approche classique du modèle de projet utilise un modèle plus petit de la même famille (Llama 3.2 1B rédaction pour Llama 3.3 70B). Il fonctionne mais le taux d'acceptation est médiocre  la distribution du modèle plus petite diverge de l'objectif. L'Eagle, puis l'Eagle-2, puis l'Eagle-3 entraînent une tête de projet légère directement sur les états internes du modèle cible, de sorte que la distribution du projet suit la cible beaucoup plus de près. C'est pourquoi Alpha passe de 0,4 avec le modèle de projet à 0,6-0,8 avec EAGLE-3.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为 Llama 3.3 70B做草案)──它可行但接受率平更小模型的分布偏离目标──EAGLE、EAGLE-2、EAGLE-3 直接在目标模型内部状态上训练轻量草案头,所以草案的分布更接近目标──这就是为什么alpha从草案 模型的0.4 升至EAGLE-3 的0.6-0.8──

Le capture: EAGLE-3 est accepté dans le vLLM 2026. `speculative_config`Les équipes qui le déploient sans mesurer l'alpha sur leur trafic réel voient souvent la latence de la queue s'aggraver, pas s'améliorer.

> 关键点:EAGLE-3 dans le vLLM 2026 année est opt-in de la.`speculative_config`Il faut une définition évidente. Il n'y a pas de marque, il n'y a pas d'accélération.

## Le concept de base.

### Ce que le décoding spéculatif achète réellement

> **【中文解读】**推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)`Pour K=5, alpha=0,7, l'accélération théorique est de 4,1x. Mais la production réelle ne dépasse généralement que 2 à 3x, car l'alpha atteint rarement 0,7 ou plus sur le flux réel, et l'essai de vente en grande quantité augmente en grande quantité.

Sans décode spécifique, le coût par jeton est un cible à l'avant.`1 + K * alpha`- Le rappel est ...`(1 + K * alpha) / (1 + epsilon)`où epsilon est le coût de la révision des projets. pour K=5, alpha=0,7:`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`Les chiffres du monde réel se regroupent autour de 2-3 fois parce que l'alpha est rarement aussi élevé sur le trafic de production et l'epsilon grandit à haute taille de lot.

> 没有推测解码时,每代币 成本是一个目标前向传播──有推测解码时,草案 长度 K 和接受率 alpha 下,每次目标前向的预期代币 数为 `1 + K * alpha`◊ Accélération par`(1 + K * alpha) / (1 + epsilon)`, dont l'epsilon est le projet + 验证开销── pour K=5, alpha=0.7:`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`◊ La concentration de données réelle est de 2-3 fois plus grande, car l'alpha est très faible dans le flux de production, et l'epsilon augmente en grande taille de lot.

### Pourquoi alpha est la seule métrique qui compte

Les jetons rejetés ne disparaissent pas  ils forcent une deuxième cible à la première jeton rejetée. Pour une charge de travail où l'alpha tombe à 0,4, vous payez des frais généraux de projet plus de vérification plus de ré-roll. À haute simultanéité (disons 256 simultanément), le lot de décode est déjà assez grand pour que l'écart entre "target seul" et "target avec vérifier" diminue. En dessous de l'alpha 0.55 sur la plupart des appareils de 2026, le décode des spécifications est négatif net.

> Les jetons rejetés ne disparaîtront pas et ils seront obligés de se propager à la première jeton rejetée pour un deuxième objectif. En alpha  en baisse à 0,4 de charge de travail, vous paierez le projet 开销 + 验证 + 重新生成.

Alpha varie selon la charge de travail. Sur le chat général de style ShareGPT, EAGLE-3 formé sur ShareGPT atteint 0,6-0,8. Sur le trafic spécifique au domaine (code, médical, juridique) le chef de projet formé sur les données générales tombe à 0,4-0,6.

> Alpha 因工作负载而异. Dans le langage général de ShareGPT 风格, avec EAGLE-3 de formation ShareGPT 达到 0.6-0.8 ⋅ sur un flux spécifique de domaine ⋅ code 、 médica, 法律) ⋅ sur le langage général de formation de données ⋅ sur un projet de tête ⋅ descendre à 0.4-0.6 ⋅ sur un projet de tête spécifique de domaine de formation ⋅ récupérer alpha par rapport à l'objectif de modulation, c'est une tâche de formation léger ⋅ rapide ⋅

### Des générations d'AIGLE à un coup d'œil

> **【中文解读】**推测解码经历了三代演进:(1) Modèle classique de projet de modèle(同一系列小模型,alpha 0.3-0.5) Simple mais faible taux d'acceptation;(2) EAGLE-1/2(en trainant le projet de tête sur l'état caché du modèle cible,alpha 0.5-0.7)Plus élevé taux d'acceptation;(3) EAGLE-3(en trainant sur l'état caché multiplacé,alpha 0.6-0.8)2025-2026 années de production.

> **【拓展：推测解码 vs 其他加速技术】**LLM 推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速, nécessite une tête de projet supplémentaire;(2) 量化(INT8/FP8) 推理加速 1.5-2x, avec légère perte de qualité;(3) 分块预填降低ITL尾但不直接提升吞吐;(4) 分分式预填/decode消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──

- **Classic draft model**: petit modèle de même famille. Alpha 0.3-0.5. Infrastructure simple  deux modèles chargés, projet de course K en avant par cible en avant.
  Le mot grec traduit par " le mot grec "**经典 draft 模型**:同系列的小模型──Alpha 0.3-0.5──基础设施简单加载两个模型,草案 每次目标前向运行 K 次前向──
- **EAGLE-1 (2024)**L'objectif est de maintenir la tête de projet unique en état caché (dernier niveau).
  Le mot grec traduit par " le mot grec "**EAGLE-1 (2024)**Le niveau de formation est de 0,5-0,6%.
- **EAGLE-2 (2025)**: longueur adaptative du projet et des projets basés sur des arbres (vérifiez plusieurs branches dans un seul passage cible). Alpha ~ 0,6-0,7.
  Le mot grec traduit par " le mot grec "**EAGLE-2 (2025)**Le projet de loi de la loi de l'Alpha (Alpha) est un projet de loi de la loi de l'Alpha (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (Alpha) (
- **EAGLE-3 (2025-2026)**: tête de projet entraînée sur plusieurs couches cibles (pas seulement la dernière), meilleure alignement. alpha ~ 0,6-0,8 sur le chat général.
  Le mot grec traduit par " le mot grec "**EAGLE-3 (2025-2026)**Le chef de projet de formation à plusieurs niveaux (pas seulement le dernier niveau) est mieux à l'aise.

### La recette de production de 2026

> **【中文解读】**• la mise en place d'un système de gestion de la production et de la production de produits de base et de production de produits de base;`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) Si alpha < 0.55,禁用推测解码或训练领域特定的草案头;(5) 在生产并发水平重新测试,确认 P99 ITL 没有恶化──

1. Modèle de port cible clair. Mesurer la TTFT de référence, le LTI, le débit à la simultanéité cible.
   Le premier est le modèle de base.
2. Activer le projet EAGLE-3 via vLLM `speculative_config`- Retournez le point de référence.
   Le mot " l' école " est traduit par " l' école "`speculative_config`Initiation du projet EAGLE-3 ∙ Réinitialisation du test de base ∙
3. Taux d' acceptation de journaux alpha. vLLM V1 rapporte ceci comme `spec_decode_metrics.accepted_tokens_per_request`Divisez par la longueur requise pour obtenir l'alpha.
   Le taux d'acceptation de l'alpha-vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request`Rapport: à l'exception du projet de demande, la longueur est obtenue alpha.
4. Si l'alpha < 0,55 est appliquée à la distribution du trafic de production, désactiver le décodeur des spécifications ou entraîner un projet EAGLE-3 spécifique au domaine.
   Si la distribution de la production est alpha < 0,55, il est impossible de faire des estimations de la capacité de production dans un domaine spécifique de l'équipe EAGLE-3.
5. Confirme que le P99 ITL n'a pas empiré.
   Le P99 ITL est sans défaut.

### Le piège de production: P99 queue

La moyenne ITL diminue avec le décode spécifique. P99 peut empirer si vous ne réglez pas. Les projets rejetés déclenchent une séquence de deux passes (draft + verifier-fail + ré-rollo).

> 平均 ITL 随推测解码下降──如果不调优,P99可能恶化──被拒绝的草案 触发两次传递序列(草案 + 验证失败 + 重新生成)──在满批次下, ces deux fois de传递串行化──关注 P99 ITL,而不是 P50──

### Lorsque l'Eagle-3 est déjà déployé

Google a déployé le décoding spéculatif dans AI Overviews en 2025 (même qualité, réponse plus rapide). vLLM V1 vaisseaux `speculative_config`comme l'interface documentée; le décoding spéculatif GPU N-gramme dans V1 est la variante compatible avec le pré-remplissage en morceaux. SGLang prend en charge EAGLE-3 comme le chemin de projet recommandé pour les charges de travail lourdes de préfixes.

> Google en 2025 va proposer le déploiement de code à l'IA.`speculative_config` comme interface documentée;V1 en N-gramme GPU  推测解码是与分块预填兼容的变体──SGLang 支持EAGLE-3 作为前密集工作负载的推草案路径──

### - Je ne peux pas faire de calcul.

Accélération attendue: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`- Je suis en train de régler .`S = 1`résolve pour alpha: `alpha_breakeven = verify_overhead / K`. Pour les charges de vérification typiques ~0,15 et K=5: `alpha_breakeven = 0.03`Mais c'est le mathématique de décode brut. À haute simultanéité, le coût de vérification augmente et le lot de décode amorte déjà les lectures de mémoire à travers les séquences, donc l'équilibre alpha_breakeven efficace monte à ~ 0,45-0,55 en pratique.

> 预期 accélération比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`Il y a une autre.`S = 1`- Je suis désolé.`alpha_breakeven = verify_overhead / K` Typical verify_overhead 约0.15,K=5:`alpha_breakeven = 0.03`, mais c'est le début de la mathématique.

### Quand ne pas utiliser le décoding spéculatif

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 concurrent) 内存带宽差距大,收益明显。 在以下场景应避免:(1) 批量离线生成延迟不重要,使用平目标;(2) 短输出< 50 tokens) 草案 开销和验证成本主导;(3) 专业领域无领域训练的草案) alpha 太;(4) vLLM v0.18.0 + 草案-model + 零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零

> **【拓展：vLLM 推测解码配置】**vLLM V1 支持三种推测解码模式:(1) Développement modèle传统小模型作为草案,与零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零`speculative_config`Il faut une configuration évidente, VLLM ne démarre pas de code de démarrage.

- Génération hors ligne de série 1, où la latence n'a pas d'importance.
  Le nombre de décharges est de 1 à 1 en utilisant un modèle objectif ordinaire.
- Les résultats sont très courts (moins de 50 jetons).
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEPC) est une initiative de la Commission européenne sur les droits de l'homme (CEPC) et des droits de l'homme (CEPC).
- Des domaines spécialisés sans chef de projet.
  Le chef de projet de formation de la section spécialisée de la formation en français.
- vLLM v0.18.0 plus le décode des spécifications du modèle de projet plus `--enable-chunked-prefill`Cette combinaison ne se compile pas. L'exception documentée est le décode de spécifications de la GPU N-gramme dans V1.
  Le modèle de projet de projet de loi`--enable-chunked-prefill` Le composé est impossible à compiler  l'exception est la GPU N-gramme de V1 

## Utilisez-le avec le cadre de réalisation
```figure
mx-speculative-tree
```

## Utilisez-le

`code/main.py`Simulation d'une boucle de décode avec et sans décode spéculative sur une gamme de valeurs alpha et de longueurs de projet K. Il imprime l'alpha-partie, la vitesse mesurée et le comportement de la queue.

> `code/main.py`模拟有/无推测解码的解码循环, couvrant une série d'alpha 值和草案 长度 K―― il imprime 亏平衡 alpha、测量加速比和尾部行为――

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-eagle3-rollout.md`. Compte tenu d'un modèle cible, d'une description de la distribution du trafic et d'un objectif de simultanée, il produit un plan de déploiement EAGLE-3 en étapes  référence de base, permet la configuration, la mesure alpha, la porte sur alpha >= 0,55, voir P99 ITL.

> 本课产 出 `outputs/skill-eagle3-rollout.md` Donner un modèle de cible  Définition de la distribution et de la mise en œuvre de l'objectif, il génère des étapes EAGLE-3  lancement du plan 基准基线、 activation de la configuration  mesure alpha ̇ et alpha >= 0,55   作为门控、关注 P99 ITL。

## Les exercices

1. On court .`code/main.py`À K=5, quelle alpha vous faut pour une accélération de 2x ? Pour une accélération de 3x ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Qu'est-ce que le taux de débit de l'alpha ?
2. Imaginez que le trafic de production divise 70% le chat général, 30% le code. Le chat général atteint alpha 0.7 avec EAGLE-3 formé sur ShareGPT; le code atteint alpha 0.4.
   En français, le chiffre d'affaires de l'entreprise est de 0,7%, le chiffre d'affaires est de 0,7%.
3. Lisez le VLLM `speculative_config`Nommer les trois modes (modèle de projet, EAGLE, N-gramme) et lequel est compatible avec le pré-remplissage en morceaux.
   Le mot " l' école " est traduit par " l' école "`speculative_config`文档──说出三种模式(drafts model、EAGLE、N-gram)及哪个与分块预填兼容──
4. Vous voyez une baisse moyenne de l'ITL de 25% après avoir activé EAGLE-3 mais P99 ITL a augmenté de 15%.
   En anglais, le taux d'utilisation de l'ITL est de 25% mais le taux de P99 est de 15%[1].
5. Comptez le coût de mémoire de la tête de projet EAGLE-3 pour Llama 3.3 70B. Comment se compare-t-il à l'exécution de Llama 3.2 1B comme un projet classique?
   Llama 3.3 70B de EAGLE-3 projet tête 内存成本──与运行 Llama 3.2 1B 作为经典草案 相比怎么?

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Encore une lecture

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) source officielle sur `speculative_config`et la compatibilité avec le préchargement en morceaux dans V1.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) l'ensemble exact du champ.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) la formule originale de la tête de projet de l'Eagle.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) projets adaptatifs et arbres.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) système de MLL efficace avec décoding spéculatif.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) Liste de contrôle de déploiement de la production.
