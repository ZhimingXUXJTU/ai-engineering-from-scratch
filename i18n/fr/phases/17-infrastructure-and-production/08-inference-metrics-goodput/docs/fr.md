# Les métriques d'inférence  TTFT, TPOT, ITL, Goodput, P99   recommander l'indicateur Goodput

> Quatre mesures déterminent si un déploiement d'inférence fonctionne. TTFT est pré-remplir plus que la file d'attente plus le réseau. TPOT (équivalemment ITL) est le coût de décode lié à la mémoire par jeton. La latence de bout en bout est TTFT plus TPOT fois longueur de sortie. Le débit est des jetons par seconde agrégés dans toute la flotte. Mais ce qui compte pour le produit, c'est le goodput  la fraction des demandes qui ont répondu à chaque SLO simultanément. Un débit élevé à un débit faible signifie que vous traitez des jetons qui n'atteignent jamais les utilisateurs à temps. Numéros de référence pour Llama-3.1-8B-Instruire sur le TRT-LLM en 2026: moyenne TTFT 162 ms, moyenne TPOT 7,33 ms, moyenne E2E 1,093 ms. Toujours signaler P50, P90, P99  jamais juste méchant. Et attention au piège de mesure: GenAI-Perf exclut le TTFT du calcul ITL, LLMPerf l'inclut; deux outils ne sont pas d'accord sur le TPOT pour la même course.

> **【中文解读】**Ce chapitre présente les indicateurs de qualité et le système de indicateurs clés de qualité des services.
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

>  **【前置】**Je suis en train de faire une étude sur la façon dont les données sont utilisées pour la formation.
>  **【类比】**推理指标 = "餐厅 KPI"。TTFT = 顾客坐到第一道菜上桌(prefill+queue+network);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅每小时出餐总数;Goodput = 满足所有SLO's request proportion(关键!)。陷:高吞吐低 Goodput = 制作了很多菜但客人不按值时吃到──必须报价P50/P90/P99 不能只报价均──GenAI-Perf 和 LLMPerf对 TPOT口径不同相同运行结果会冲突──
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Définir avec précision le TTFT, le TPOT, l'ITL, l'E2E, le débit et le goodput et nommer le composant que chaque mesure.
  Le texte de la lettre de référence est le texte de la lettre de référence.
- Expliquez pourquoi la moyenne est la statistique erronée pour le service de LLM et comment lire P50/P90/P99.
  Expliquer pourquoi la moyenne est une statistique erronée de l'application du droit de licence, ainsi que comment lire P50/P90/P99。
- Construire une limite multi-SLO (par exemple TTFT < 500 ms ET TPOT < 15 ms ET E2E < 2 s) et calculer le goodput en fonction de celle-ci.
  Le nombre de performances de la production est de 500ms et de 15ms.
- Nombre de deux outils de référence qui ne sont pas d'accord sur le TPOT pour la même période et expliquez pourquoi.
  Le TPOT a été testé en deux parties dans le même cours et a produit des résultats différents.

## Le problème , l' introduction du problème

> **【中文解读】**推理服务有多个延迟轴,每个轴以不同方式失败──Préfill est calculé limité,随提示长度增长;Decode est内存限制,随批量 增长;排队延迟是运维问题;网络是物理距离问题──needs different indicator to measure each dimension, needs percent, also needs a comprehensive indicator to say"user has got the desired experience" this is Goodput──

> **【拓展：LLM 推理指标体系】**Le système d'indicateurs complets de la mise en œuvre du programme de formation en ligne de 2026 comprend: 1) TTFT (premier jeton) 延迟 (premier jeton)  utilisateur感知到的第一次响应时间; 2) TPOT/ITL (premier jeton) 延迟 (inter-jeton) 流式输出平滑度; 3) E2E (exécutif) 端到端延迟 (exécutif) 总时间) 从请求到完成 (exécutif) 通过 (exécutif) 集群效率指标; 5) Goodput (exécutif) 同时满足所有 SLA (exécutif) 请求比例.

" Notre débit est de 15 000 jetons par seconde. " Alors quoi ? Si 40% des demandes ont dépassé 2 secondes de bout en bout, les utilisateurs ont abandonné la session.

> " Notre puissance est de 15 000 tokens par seconde. " Si 40% des demandes de fin de compte dépassent 2 secondes, l'utilisateur abandonne la conversation.

L'inference a plusieurs axes de latence et chacun échoue différemment. Le pré-remplissage est calculé et mesure avec une longueur rapide. Le décode est lié à la mémoire et mesure avec la taille du lot. Le retard de file d'attente est un problème opérationnel. Le réseau est un problème de distance physique. Vous avez besoin de métriques distinctes pour chacune, et vous avez besoin de percentiles, et vous avez besoin d'un seul composite qui dit " l'utilisateur a obtenu ce qu'il attendait "

> 推理有多延迟轴,每个轴以不同方式失败──预填充是计算有限的,随提示长度增长──解码是内存有限的,随批次大小增长──排列延迟是运维问题──网络是物理距离问题──你需要每个维度不同的指标,需要百分数,还需要一个综合指标说"用户是否获得预期的体验"这是Goodput──

## Le concept de base.

### TTFT  temps pour le premier jeton

> **【中文解读】**TTFT = queue_time + network_request + prefill_time。Prefill en longueur de temps 32K prompt en Llama 3.3 70B FP8 H100 上 nécessite environ 800ms de pure préfill。排队时间是调度器的行为,网络请求包括 TLS的线缆时间──TTFT是用户在流式返回任何内容之前感知到的延迟──

`TTFT = queue_time + network_request + prefill_time`

Le préfil est le plus important lorsque les instructions sont longues. Sur Llama-3.3-70B FP8 sur H100, une requête de 32k prend environ 800 ms de préfil pur. Le temps de file d'attente est le comportement du planificateur sous chargement. La demande de réseau est le temps de fil, y compris TLS.

> Llama-3.3-70B FP8 sur H100,32K 提示需要约800ms的纯预充――排队时间是调度器的行为――网络请求是包括TLS的线缆时间――TTFT是用户在任何内容流式返回前感知到的延迟――

### TPOT / ITL  latence entre les jetons

> **【中文解读】**TPOT(temps par jeton de sortie) = ITL(la latence inter-token) = latence de décode par jeton。公式:TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下,TPOT 均值约 7ms;无分块预填充时,在长预填 邻居序列期间 TPOT 可升至 50ms。永远监控 P99而非均值。

Beaucoup de noms pour une quantité.`TPOT`(temps par jeton de sortie), `ITL`(la latence entre les jetons), `decode latency per token` tout de même. C'est le temps entre les jetons diffusés consécutifs après le premier.

> Une quantité de noms.`TPOT`(à chaque sortie de jeton 时间)`ITL`(inter-token 延迟)`每 token 解码延迟`都是同一个──它是第一个标志 之后连续流式标志 间时间──

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

Sur la même pile Llama-3.3-70B H100 avec pré-remplissage en morceaux, le TPOT est d'environ 7 ms. Sans pré-remplissage en morceaux, pendant un long pré-remplissage sur une séquence voisine, le TPOT peut atteindre 50 ms. Regardez P99, pas de moyenne.

> En même temps, le TPOT peut atteindre 50 ms, en particulier en P99, et non en moyenne.

### La latence E2E

`E2E = TTFT + TPOT * output_tokens + network_response`

Pour les sorties longues (> 500 jetons), E2E est dominé par le TPOT. Pour les sorties courtes avec des demandes longues, E2E est dominé par le TTFT.

> Pour le long terme, E2E par TTFT, E2E par TTFT, E2E par rapport au long terme.

### Résultats

`throughput = total_output_tokens / elapsed_time`

La métrique agrégée vous indique l'efficacité de la flotte, pas la santé des demandes individuelles.

> 聚合指标──告诉你集群效率──不告诉你单个请求的健康状况──

### La métrique dont vous vous souciez vraiment

> **【中文解读】**Le bon rendement est le seul indicateur global vraiment important. Le SLO est un nombre de contraintes. Une seule demande est de satisfaire simultanément le TTFT <= a、TPOT <= b、E2E <= c 才算"好"── haute throughput à 60% Le bon rendement est un échec; faible throughput à 99% Le bon rendement 才是目标── 2026 ans MLPerf Inference v6.0 et AI Plateformes fournisseurs de SLA interne 追踪 sont tous basés sur le bon rendement comme indicateur central.

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

Le SLO est une restriction multi-constraint. Une demande est "bonne" seulement si chaque contrainte est respectée. Goodput est la part.

> SLO est de beaucoup de contraintes. Seulement lorsque toutes les contraintes sont satisfaites, la demande est "bonne".

En 2026, le goodput est la métrique utilisée dans les soumissions MLPerf Inference v6.0 et dans le suivi interne de SLA chez les fournisseurs de plateformes d'IA.

> 2026 年,Goodput is MLPerf Inference v6.0 提交和AI 平台提供商内部 SLA 追踪使用的指标──

### Pourquoi la méchanceté est la mauvaise statistique

> **【中文解读】**LLM 延迟分布是右偏的──一个包含长预填 邻居的解码批可能发发发 500 个 TPOT ~7ms的代币 和 20 个 TPOT ~60ms的代币──平均值 TPOT 是 9ms,但P99 TPOT 是 65ms──用户经常遇到P99这是他们离开的原因──永远报告三元组(P50,P90,P99),对于用户体验,P99是需要优化的目标──

Les distributions de latence LLM sont à droite. Un lot de décode avec un voisin de pré-remplissage peut expédier 500 jetons avec TPOT ~ 7 ms et 20 jetons avec TPOT ~ 60 ms. Le TPOT moyen est de 9 ms. P99 TPOT est de 65 ms. Les utilisateurs frappent régulièrement le P99  c'est pourquoi ils partent.

> LLM 延迟分布是右偏的──一个包含长预填充邻居的解码批次可以发发发 500 个 TPOT 约7ms的代币和 20 个 TPOT 约60ms的代币──平均值 TPOT 是 9ms──P99 TPOT 是 65ms──用户经常遇到 P99这是他们离开的原因──

Rapporte toujours le triple (P50, P90, P99). Pour l'expérience utilisateur, P99 est celui que vous optimisez.

> Pour les utilisateurs, P99 est votre besoin d'optimisation.

### Numéros de référence  Llama-3.1-8B-Instruction sur le TRT-LLM, 2026

- TTFT moyen: 162 ms
  Nom de fichier: TTFT: 162ms
- TPOT moyen: 7,33 ms
  Nom de fichier:
- moyenne E2E: 1 093 ms
  Nom de fichier: E2E: 1,093ms
- P99 TPOT: varie de 10 à 25 ms selon la configuration de préchargement en morceaux.
  Le temps de chargement est de 10 à 25 ms.

Ce sont les points de référence NVIDIA publiés. Ils changent avec la taille du modèle (70B montrerait 3-5x), le matériel (H100 vs B200 ~ 3x), et la charge.

> Ces données sont publiées par NVIDIA. Elles sont disponibles avec un modèle de taille de 70B.

### Le piège de mesure

> **【中文解读】**Les deux outils de test de base les plus courants de l'année 2026 sur TPOT donnent des résultats différents: NVIDIA GenAI-Perf va exclure le TTFT de l'ITL  calcul en ligne, du token 2 开始, LLMPerf contient le TTFT, du token 1 开始) ⋅ la même requête, du TTFT 500ms、100 输出 token、700ms décode, du GenAI-Perf 报告 ITL=7.07ms, du LLMPerf 报告 ITL=12.00ms.., toujours expliquer quel outil utiliser, définir définitivement.

> **【拓展：LLM 基准测试工具生态】**L'équipe de recherche de l'équipe de recherche de l'Université de Toronto (États-Unis) a été créée pour la première fois en 2026 par le projet de recherche de recherche de l'Université de Toronto (États-Unis) et a été créée par le projet de recherche de recherche de l'Université de Toronto (États-Unis) pour la première fois en 2026 par le projet de recherche de recherche de l'Université de Toronto (États-Unis).

Deux des outils de référence les plus utilisés pour 2026 ne sont pas d'accord sur le TPOT pour la même période:

- **NVIDIA GenAI-Perf**: exclut le TTFT du calcul de l'ITL. L'ITL commence par le jeton 2.
  Le mot grec traduit par " le mot grec "**NVIDIA GenAI-Perf**: de l'ITL 计算中排除 TTFT──ITL de la deuxième étiquette 开始──
- **LLMPerf**: inclut le TTFT. ITL commence par le jeton 1.
  Le mot grec traduit par " le mot grec "**LLMPerf**: contenant TTFT──ITL depuis le 1er token 开始──

Pour une demande avec TTFT 500 ms et 100 jetons de sortie en 700 ms de décode total, GenAI-Perf rapporte `ITL = 700/99 = 7.07 ms`, rapporte LLMPerf `ITL = 1200/100 = 12.00 ms`Le choix de l'outil change le numéro.

> Pour une TTFT 500ms 100  sortie de jeton 700ms  total résolution de la demande, GenAI-Perf  rapport `ITL = 700/99 = 7.07ms`,LLMPerf  rapport `ITL = 1200/100 = 12.00ms`◊ outils de sélection pour changer le nombre.

Indiquez toujours quel outil, publiez toujours la définition.

> 始终说明使用哪个工具──始终发布定义──

### Construire un SLO

> **【拓展：LLM SLO 设定参考】**2026 annulation de consommation de classe 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 jetons 输出)、Goodput >= 99%。Enterprise class SLO 收紧 TTFT(200-400ms) mais laisser E2E── mesure méthode: utiliser le vrai flux ou LLMPerf 合成流量(`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`), objectif 2x 峰值并发,运行 30-50 次代取百分位数──

Un SLO raisonnable pour un modèle de chat 70B en 2026:

- TTFT P99 <= 800 ms.
  Le premier jeton est le premier jeton.
- TPOT P99 <= 25 ms.
  Le code de débit est le code de débit.
- E2E P99 <= 3 s pour les sorties de < 300 jetons.
  Le code de débit est le code de débit.
- Objectif de rendement >= 99%.
  Le résultat est de 99%

Les SLO d'entreprise resserrent le TTFT (200-400 ms) et relâchent l'E2E. Le but est de les noter, de mesurer les trois et de suivre le goodput en un seul composite.

> 企业级 SLO 收紧 TTFT(200-400ms)并放宽 E2E──关键是要写下来、测量全部三、并将Goodput 作为单一综合指标追踪──

### Comment mesurer

- Exécuter un trafic réel ou synthétique réaliste (LLMPerf avec `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)
  Le mot "réalisme" est traduit par "réalisme".`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)。
- Objectif 2x concurrences maximales pour la course de référence.
  Le but de la mise en œuvre du test est de 2 fois la valeur du sommet.
- Exécutez 30 à 50 itérations, prenez des percentiles de l'échantillon combiné.
  Le nombre de personnes qui ont été arrêtées à l'égard de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation est de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation de l'organisation.
- Publier avec le nom de l'outil, la version de l'outil, le modèle, le matériel, la simultanéité, la distribution rapide.
  Le nom de l'outil, la version, le modèle, le matériel, le nombre et la distribution de l'information.

## Utilisez-le avec le cadre de réalisation
```figure
throughput-latency
```

## Utilisez-le

`code/main.py`Il est également possible de générer une distribution de latence synthétique, d'appliquer un SLO et de calculer le goodput.

> `code/main.py`Il est également montré la même trace de la différence entre la génération de l'AI-Perf et la génération de l'LLMPerf.

## Envoyez-le . Produit .

> **【拓展：SLO 设定与 Goodput 门控】**Le modèle de référence de 2026 est le 70B pour le modèle SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 jetons 输出)、Goodput 目标 >= 99%。 enterprise class SLO 收紧 TTFT(200-400ms) mais laisser E2E。

Cette leçon produit `outputs/skill-slo-goodput-gate.md`. Compte tenu de la charge de travail et de la SLO, il produit une recette de référence prête à l'IC/CD qui déploie les portes sur une bonne puissance plutôt que sur une capacité de débit.

> 本课产 出 `outputs/skill-slo-goodput-gate.md` Donnée charge de travail et SLO, elle génère un programme de test de base CI/CD, basé sur Goodput et non sur le débit en tant que contrôle de déploiement.

## Les exercices

1. On court .`code/main.py`Comment le goodput change-t-il lorsque vous serrez le P99 TPOT de 30 ms à 15 ms ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Génération avec une distribution de 1% de la pointe de la partie finale  Lorsque le P99 TPOT passe de 30ms  resserré à 15ms  Comment le Goodput change-t-il ?
2. Un vendeur cite "15.000 tok/s sur Llama 3.3 70B H100". Nommez trois questions à poser avant de lui faire confiance.
   Le prix de la vente est de 3,3 milliards de dollars.
3. Pourquoi le pré- remplissage en morceaux protège le P99 TPOT mais pas le TPOT ?
   Pourquoi le bloc de pré-remplissage de protection P99 TPOT mais pas de protection de valeur moyenne TPOT ?
4. Construire un SLO de consommation pour un assistant vocal (le premier jeton est entendu, pas lu). Quelle mesure est la plus visible par l'utilisateur?
   Pour les utilisateurs, quel est le plus visible ?
5. Lisez les documents LLMPerf README et GenAI-Perf. Identifiez trois autres mesures où les outils ne sont pas d'accord.
   Le texte de la loi est le texte de la loi de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Encore une lecture

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) définition canonique de TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) définitions alternatives et recette de mesure.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) mesure appliquée sur les déploiements réels.
- [LLMPerf](https://github.com/ray-project/llmperf) Résumé de référence de source ouverte basé sur Ray.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md) L'outil de référence de NVIDIA.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) l'indice de référence basé sur la qualité accepté par l'industrie.
