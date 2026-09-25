# L' API de test de charge pour LLM  Pourquoi K6 et Locust mentent 

> Les testeurs de charge traditionnels n'ont pas été conçus pour les réponses de streaming, les longueurs de sortie variables, les mesures au niveau des jetons ou la saturation de la GPU. Deux pièges mordent la plupart des équipes. Le piège GIL: La mesure au niveau des jetons de Locust exécute la jetonisation sous le Python GIL, qui rivalise avec la génération de requêtes sous une forte concurrence; le backlog de jetonisation gonfle ensuite la latence inter-token rapportée  votre client est le goulot d'étranglement, pas le serveur. Le piège de l'uniformité de la mise en ligne: les mises en ligne identiques dans une boucle testent un point sur la distribution des jetons; le trafic réel a une longueur variable et des correspondances de préfixes diverses. LLMPerf résout cette situation avec `--mean-input-tokens`+ `--stddev-input-tokens`. Mapping des outils en 2026: spécialisée dans le domaine de la maîtrise de la loi (GenAI-Perf, LLMPerf, LLM-Locust, guidellm) pour une précision au niveau des tokens; **k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)** diffusion en streaming, Kubernetes natifs distribués via TestRun/PrivateLoadZone CRDs, le meilleur pour les portes CI/CD; Vegeta for Go saturation à taux constant; Locust 2.43.3 uniquement avec extension LLM-Locust pour le streaming.

> **【中文解读】**Ce chapitre présente les méthodes de test de l'API LLM  charge test  évaluation de la fonction de service en haute charge 


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**Je suis en train de faire une analyse de la situation de l'appareil.
>  **【类比】**LLM 负载测试 = "测自动驾驶 vs 测传统车"──两个陷:(1) GIL 陷:Locust 在Python GIL 下做代币化,与请求生成抢锁→报告的代币 间延迟虚高(客户端是瓶不是服务端);(2) Prompt 一致性陷:循环同步即时只测分布一个点,真流量有多样化前匹配──LLMPerf 用`--mean-input-tokens+stddev`修复──2026 工具:GenAI-Perf/LLMPerf/LLM-Locust(LLM 专用) + k6 v2026.1(流式+K8s) + Vegeta(Go 常速率) + Locust(仅配 LLM-Locust 扩展)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objectifs d'apprentissage

- Expliquez les deux anti-patterns (trampille GIL, piège de rapidité d'uniformité) qui font que les testeurs de charge génériques mentent pour les API LLM.
  Le système de test de charge généralisée est un système de test de charge généralisé.
- Choisissez un outil à un usage donné: LLMPerf (exécution de référence), k6 + extension de streaming (portée CI), guidellm (synthétique à grande échelle), GenAI-Perf (référence NVIDIA).
  Le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos, le Chaos,
- Conceptez quatre modes de charge (stable, rampe, point, plongée) et nommez le mode de défaillance de chaque prise.
  Le modèle de charge est de quatre modes:
- Construire une distribution rapide réaliste en utilisant la moyenne + stddev des jetons d'entrée plutôt que la longueur fixe.
  Le nombre de points de référence est de 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 en moyenne moyenne moyenne à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 en moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne.

## Le problème , l' introduction du problème

> **【中文解读】**Les outils de test de charge traditionnels ne sont pas conçus pour le LLM  ils ne supportent pas le flux de réponse ̊ variable de sortie de longueur ̊ indicateur de niveau de jetons  et de GPU  et de taille ⋅ deux pièges communs: 1) GIL  piège  La mesure de la taille de jetons de Locust dans Python GIL  fonctionnement分词, 高并发时代 代码 队列膨胀,虚报 延迟 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅  ⋅ ⋅ ⋅    ⋅                                                                 

> **【拓展：LLM 负载测试的四种模式】**2026 ans LLM  charge testés de quatre modes: 1) 稳态(stable-état) 恒定 RPS 持续30-60分钟,捕获基线性能退化; 2) 渐增) ramp) 从0 线性增加到目标 RPS,捕获容量断点和预热异常; 3) 突发(spike) 突然 3-10x RPS 持续2分钟然后回落,测试自动扩张响应、队列和和和冷启动影响; 4) 时间(稳态持续4-8小时,捕获内存漏、连接池漂移和可观测性溢溢.

Vous avez testé votre LLM avec 500 utilisateurs simultanément, vous avez réussi, vous avez expédié, en production avec 200 utilisateurs réels, le service est tombé sur P99 TTFT explose, les GPUs sont bloqués.

Deux choses se sont produites. Premièrement, k6 a envoyé 500 requêtes identiques  votre collecte de requêtes et votre mise en cache de préfixes ont fait semblant que vous gériez 500 décodes concurrents lorsque vous en gériez un. Deuxièmement, k6 ne suit pas la latence inter-token sur les réponses de streaming comme l'œil l'expérient; il voit une connexion HTTP, pas 500 jetons arrivant à des intervalles variables.

Les tests de charge pour les LLM sont sa propre discipline.

## Le concept de base.

### Le piège du GIL (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】**Python GIL(全局解释器锁) sur le LLM 负载测试的影响:Locust 使用Python 运行客户端分词,在高并发时代代码化 队列排在请求生成后面――报告的间代码 延迟包含客户端代码化 积压你以为是服务器慢,其实是测试工具的瓶──解决方案:(1) LLM-Locust 扩展将代码化 移动到独立进程;(2) 使用编译语言工具k(Go) MPerf(Rust-backed tokenizers.rs)──

Locust utilise Python et exécute le côté client de la jetonnisation sous le GIL. En haute concurrence, les files d'attente du jetonnisateur derrière la génération de requêtes. La latence inter-token rapportée inclut le backlog de jetonnisation du côté client. Vous pensez que le serveur est lent; c'est le harnais de test.

Correction: L'extension LLM-Locust déplace la tokenization vers des processus distincts ou utilise un harnais de langue compilée (k6, LLMPerf en utilisant tokenizers.rs).

### Le piège de l'uniformité rapide

Tous les testeurs de charge connus vous permettent de configurer un seul prompt. Dans un test en boucle de 10 000 itérations, le même prompt envoie exactement à chaque fois. Le serveur voit le même préfixe à chaque fois que le préfixe cache touche à 100%, le débit est excellent.

Correction: échantillon obtenu à partir d'une distribution rapide.`--mean-input-tokens 500 --stddev-input-tokens 150` divers longs et divers contenus.

### Quatre modes de charge

1. **Steady-state** RPS constant pendant 30 à 60 minutes.
2. **Ramp** augmentation linéaire du RPS de 0 à la cible sur 15 minutes.
3. **Spike**3 à 10 fois le temps de rotation pour 2 minutes, puis de retour.
4. **Soak**- état d'arrêt pendant 4 à 8 heures.

### 2026 cartographie des outils

> **【中文解读】**L'équipe de recherche de l'équipe de recherche de l'Université de New York (États-Unis) a été créée pour la première fois en 2026 par le projet de recherche de recherche de l'Université de New York.

> **【拓展：CI/CD 中的 SLA Gate】**En utilisant la porte SLA de k6 dans le CI  Configuration: par PR 运行 30-50 次代,gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在值以下──违规则构建失败──使用真实提示分布(mean + stddev of input tokens)而非固定长度LLMPerf 使用`--mean-input-tokens 500 --stddev-input-tokens 150`Il y a aussi des conseils.

**LLMPerf**(Anyscale)  Python mais Tokenization supportée par Rust. Mean/stddev prompts.

**NVIDIA GenAI-Perf** référence de NVIDIA. Utilise le client Triton; couverture métrique complète. Notez que son ITL exclut le TTFT; LLMPerf l'inclut. Deux outils produisent différents TPOT pour le même serveur.

**LLM-Locust**L'extension Locust qui résout le piège GIL.

**guidellm** analyse comparative synthétique à grande échelle.

**k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)**- Le numéro de la liste:
- k6 lui-même (Go, compilé, sans GIL) a ajouté des métriques sensibles au streaming.
- k6 L'opérateur utilise des CRD TestRun / PrivateLoadZone pour les tests distribués natifs Kubernetes.
- Il est préférable pour les portes CI/CD et les tests SLA.

**Vegeta** Go, plus simple que k6. saturation HTTP à taux constant. Pas au courant de la loi mais bon pour les tests de passerelle / limite de taux.

**Locust 2.43.3 stock** a le piège GIL pour LLM. Seulement avec extension LLM-Locust.

### Porte SLA dans CI

Retour sur les relations publiques avec:

- 30 à 50 itérations chacune au RPS de référence.
- Porte: P50/P95 TTFT, 5xx < 5%, TPOT inférieur au seuil.
- Faites-moi une erreur.

### Distribution rapide réaliste

Construisez à partir d'échantillons de trafic réels (si vous en avez) ou de distributions publiées (par exemple, les invites ShareGPT pour le chat, HumanEval pour le code).

### Les chiffres que vous devriez vous rappeler

- k6 Opérateur 1.0 GA: septembre 2025.
- K6 v2026.1.0: métriques de diffusion de contenu.
- Exécution typique de la LLMPerf: 100 à 1000 demandes à la simultanéité X.
- Portes d'intervention typiques: 30 à 50 itérations par PR.
- Quatre modèles: stable, rampe, point, plonge.

## Utilisez-le avec le cadre de réalisation
```figure
load-pattern-waves
```

## Utilisez-le

`code/main.py`simuler un test de charge avec une distribution rapide réaliste, mesurer le TPOT efficace et démontrer le piège de la mise à jour uniforme.

> `code/main.py`simuler un test de charge avec une distribution rapide réaliste, mesurer le TPOT efficace et démontrer le piège de la mise à jour uniforme.

> `code/main.py`simuler un test de charge avec une distribution rapide réaliste, mesurer le TPOT efficace et démontrer le piège de la mise à jour uniforme.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-load-test-plan.md`- compte tenu de la charge de travail et de la SLA, choisit l'outil et conçoit les quatre modes de charge.

> 本课产 出 `outputs/skill-load-test-plan.md`- compte tenu de la charge de travail et de la SLA, choisit l'outil et conçoit les quatre modes de charge.

## Les exercices

1. On court .`code/main.py`. Comparer une distribution uniforme versus réaliste  où est l'écart ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Comparison moyenne par rapport réelle distribution P99 TTFT  différence est-il dans ?
2. Écrivez le script k6 pour une passerelle CI: TTFT P95 < 800 ms à 100 minutes de courant.
   Le code de la ligne de contrôle est de 100 km/h.
3. Votre test de plongée montre une augmentation de la mémoire de 50 Mo/h. Nommez trois causes et l'instrumentation à choisir entre elles.
   Le test de votre absorption montre une augmentation de 50 Mo par heure.
4. Test de pointe de 10 à 100 RPS. Quel est le temps de récupération prévu si la pile de production Karpenter + vLLM est en place (phase 17 · 03 + 18)?
   Le temps de récupération est de 45 secondes.
5. GenAI-Perf rapporte TPOT=6ms; LLMPerf rapporte TPOT=11ms sur le même serveur.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Encore une lecture

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
