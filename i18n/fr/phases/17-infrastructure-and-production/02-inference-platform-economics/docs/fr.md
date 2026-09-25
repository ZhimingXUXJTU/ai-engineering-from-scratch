# Économie de plateforme d'inférence  Feux d'artifice, ensemble, basétain, modal, réplique, à n'importe quel échelle 推理 经济学

> Le marché des inférences 2026 n'est plus une location de temps de GPU. Il se diviser en silicium personnalisé (Groq, Cerebras, SambaNova), plateformes GPU (Baseten, Together, Fireworks, Modal) et marchés API-first (Replicate, DeepInfra).$1/hr per GPU on May 1, 2026, and $La valorisation 4B sur 10T+ tokens par jour indique le modèle de travail axé sur le volume.$300M Series E at $La règle de positionnement compétitif est simple: les feux d'artifice optimisent la latence, ensemble optimisent la largeur du catalogue, baseten optimisent le polissage d'entreprise, modal optimisent Python-native DX, répétition optimisent la portée multimodal, Anyscale optimises distribué Python. Cette leçon vous donne une matrice que vous pouvez remettre à un fondateur.

> **【中文解读】**Ce chapitre présente la structure des coûts de la plateforme de calcul économique LLM  La structure des coûts de calcul des services  Modèles de prix et analyse économique 
**Type:** Learn
**Languages:** Python (stdlib, toy per-call economics comparator)
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy per-call economics comparator) | **语言:** Python（标准库，每次调用经济性比较器）
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 01（托管 LLM 平台）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**Je suis en train de faire une étude sur la façon dont les gens peuvent utiliser les ressources humaines pour leur permettre de mieux comprendre la situation.
>  **【类比】**推理平台 = "AI 云服务商"──三类:(1) 定制芯片(Groq/Cerebras/SambaNova) = 专用 CPU;(2) GPU 平台(Baseten/Together/Fireworks/Modal)= 通用云;(3) API 市场(Replicate/DeepInfra)= 应用商店──选型口:Fireworks 低延迟、Together 模型多Baseten 企业级、Modal多原生、Replicate模态广、Anyscale 分布式 Python──

## Objectifs d'apprentissage

- Nombre des trois segments de marché (silicon personnalisé, plateformes GPU, API-first) et carte de chaque fournisseur à un segment.
  Le premier est le premier, qui est le premier, qui est le premier, qui est le premier.
- Expliquez pourquoi le modèle de tarification de l'API "par jeton" se concentre sur la courbe de coût du moteur de service et non sur celle du matériel.
  Expliquer pourquoi l'API 定价模型 est comprimée en la courbe de coûts du moteur de service plutôt que dans le coût du matériel.
- Calculer le coût effectif par demande auprès d'au moins trois fournisseurs et expliquer quand le coût par minute (Baseten, Modal) dépasse le coût par jeton.
  Le nombre de demandes de fournisseurs est de 0,5% en moyenne.
- Identifier quelle plateforme est la bonne par défaut pour une charge de travail donnée (serveur sans éclat, haute capacité constante, variantes finement ajustées, multimodal).
  Le mot "serveur" est un mot qui signifie "serveur".

## Le problème , l' introduction du problème

Vous avez évalué les plateformes hypercalculaires gérées. Vous avez décidé que vous aviez besoin d'un fournisseur plus étroit et plus rapide  Feuilletons pour la latence, Ensemble pour la largeur, Baseten pour un modèle personnalisé finement ajusté. Maintenant vous avez six choix réels et les pages de prix ne sont pas alignées. Feuilletons montre $/M tokens; Baseten shows $/minute; Modal montre $/second; Replicate shows $On ne peut pas les comparer face à face sans modéliser la charge de travail.

> Vous avez évalué le cloud de gestion, après avoir décidé que vous avez besoin d'un fournisseur plus spécialisé, plus rapide, des feux d'artifice, de la recherche de retard, ensemble, de la recherche de la largeur, du bassin, de la recherche de modèles de modélisation.$/M tokens；Baseten 显示 $/分钟; Modal 显示 $/秒；Replicate 显示 $/ pré测──不建模工作负载就无法直接比较──

Pire encore, le modèle d'affaires derrière chaque page de tarification est différent. Les feux d'artifice fonctionnent avec leur propre moteur personnalisé (FireAttention) sur les GPU partagées; le taux par jeton reflète leur courbe d'utilisation. Baseten vous donne des GPU Truss + dédiés; par minute reflète l'exclusivité. Modal est vrai Python sans serveur  par seconde de facturation avec sous-seconde démarrage froid. La même sortie (une réponse LLM), trois fonctions de coûts différentes.

> Pire encore, chaque page de fixation est différente. Fireworks est un moteur de développement autonome partagé de la GPU. FireAttention; par jeton  tarifs reflètent sa courbe d'utilisation. Baseten  fournir Truss +  GPU spécialisé; par minute reflètent la monopole.

Cette leçon modèle les six et vous dit quand chacun gagne.

> Je vais vous dire à quel moment vous avez gagné.

> **【中文解读】**Le problème central du marché de la plateforme de calcul est la fixation des prix. Il faut voir le prix de l'appareil.

> **【拓展：LLM 推理成本构成】**Le coût de la formation de LLM est principalement dû au GPU.$2-3/hr）、电力（约 $Le taux de rentabilité des plateformes de recommandation est généralement de 20 à 40% (a16z 2025  Infrastructure report)  L'optimisation des coûts de recommandation est essentielle pour améliorer le taux d'utilisation des GPU et le lot de la mise en service continue de la grande série de VLLM.

## Le concept de base.

> **【中文解读】**推理平台市场分为三大细分:(1) 自研芯片(Groq LPU、Cerebras WSE、SambaNova RDU) 以 5-10x 解码速度取胜但单价更高;(2) GPU 平台(Baseten、Together、Fireworks、Modal) 运行NVIDIA GPU, 介于原始 GPU 租和超级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级级

> **【拓展：自研推理芯片竞赛】**LPU de Groq (Language Processing Unit) est une unité de traitement de langage capable de réaliser 300+ tokens/s sur Llama 70B, est un moteur de 10x de GPU 推理的 CS-3 晶圆级引擎可达 2000+ tokens/s. Mais l'inconvénient de ces puces est une faible flexibilité  seulement capable de fonctionner sur des modèles spécifiques.

### Les trois segments

**Custom silicon**Groq (LPU), Cerebras (WSE), SambaNova (RDU). Généralement, le décodeur est 5 à 10 fois plus rapide qu'un cluster basé sur GPU sur le même modèle. Le prix par jeton plus élevé (Groq était de ~ 0,99 $ / M sur Llama-70B fin 2025) mais imbattable pour les cas d'utilisation sensibles à la latence. Groq est le choix de production pour les agents vocaux et la traduction en temps réel.

> **自研芯片** Groq(LPU)、Cerebras(WSE)、SambaNova(RDU)。 habituellement par rapport au modèle de GPU 集群解码速度快 5-10 倍──按代币 价格更高(Groq 2025 年末在 Llama-70B 上约 $0.99/M), mais pour le cas sensible au retard il n'y a pas de rivalisateurs──Groq est un représentant de la production et une option de traduction en temps réel──

**GPU platforms** Baseten, Together, Fireworks, Modal, Anyscale. Exécuté sur NVIDIA (H100, H200, B200 en 2026) ou parfois AMD. La couche économique entre " location de GPU brut " (RunPod, Lambda) et " service géré hypercalérisé " (Bedrock).

> **GPU 平台** Baseten、Together、Fireworks、Modal、Anyscale。运行在 NVIDIA(2026 ans H100、H200、B200) ou有时是 AMD 上。"l'ancien GPU 租"(RunPod、Lambda) et "云托管服务" (Bedrock) entre l'économie层。

**API-first marketplaces** Répliquer, DeepInfra, OpenRouter, Fal. Catalogue large, pay-per-prediction ou pay-per-seconde, mettre l'accent sur le temps à la première appel.

> **API 优先市场** Répliquer 、Infra-profondeur 、OpenRouter 、Fal。 Catégorie large, selon la prédiction ou selon la seconde de paiement, soulignant la première fois la rapidité de mise en service ∼

### Feu d'artifice  plateforme GPU optimisée pour la latence

- Moteur FireAttention (custom); commercialisé avec une latence 4 fois inférieure à celle de vLLM sur des configurations équivalentes.
  Le mot d'ordre est "FireAttention" (FireAttention) et "FireAttention" (FireAttention) est "FireAttention" (FireAttention) (FireAttention) (FireAttention) " (FireAttention) et "FireAttention" (FireAttention) " (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) " (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention)) (FireAttention) (FireAttention) (FireAttention)) (FireAttention) (FireAttention) (FireAttention)) (FireAttention)) (FireAttention)) (FireAttention)) (FireAttention)) (FireAttention)) (FireAttention)) (FireAttention)) (Fire) (Fire) (FireAttention)) (Fire) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F))))))))))) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (
- Niveau de lot à ~50% de taux sans serveur pour les charges de travail non interactives.
  Traduction anglaise: pour les charges de travail non interactives, le niveau de la masse est d'environ 50% du taux de frais de serveur.
- Le modèle finement ajusté sert au même rythme que le modèle de base  un véritable différenciateur par rapport aux fournisseurs qui facturent une prime pour votre LORA.
  La différenciation entre les fournisseurs qui facturent des primes à la LORA et les fournisseurs qui facturent des primes à la LORA est un facteur réel.
- Mi-2026: augmentation du loyer sur demande de GPU de 1 $/heure à compter du 1er mai 2026.
  Le prix de location de la GPU est de 1 $ / heure.
- Signal financier: évaluation de 4 B$, 10T+ tokens par jour gérés.
  Nom de fichier: $4B 估值, traitement quotidien de 10T+ jetons.

### Ensemble  optimisé pour la largeur

- 200 modèles, y compris les versions open source, dans les jours suivant la publication en amont.
  Traduction anglaise: 200+ 模型, incluant la version ouverte de la première partie de la publication.
- 50 à 70% moins cher que Replicate sur des modèles LLM équivalents  le positionnement "AI Native Cloud" est volume et catalogue.
  Le modèle de l'équipe de recherche en droit est de 50 à 70% moins cher que le modèle de l'équipe de recherche en droit.
- Inference + ajustement fin + formation dans une API.
  Traduction anglaise: 推理 + 微调 + 训练在一个API 中。

### Baseten  optimisé pour les entreprises

- Cadre de confiance: emballage de modèle avec dépendances, secrets, config dans un seul manifeste.
  Traduction anglaise: Confidence 框架: modèle打包, contenant une dépendance 密钥、服务配置在一个清单中──
- La GPU va de T4 à B200, facturation par minute avec une réduction raisonnable du démarrage à froid.
  Le GPU varie de T4 à B200, selon le coût de l'heure, il y a un raisonnable soulagement de démarrage à froid.
- SOC 2 type II, prêt pour HIPAA.
  Le système de santé de l'État est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé qui est un système de santé.
- $5B valuation, January 2026 Series E ($300 millions de dollars de CapitalG, IVP, NVIDIA).
  Le mot grec traduit par " le mot grec "$5B 估值，2026 年 1 月 E 轮融资（来自 CapitalG、IVP、NVIDIA 的 $300 M)

### Modal  Python natif optimisé

- Infrastructure-as-code en Python pur. Décorer une fonction avec `@modal.function(gpu="A100")`et déployer avec un seul commandement.
  Traduction anglaise: pure Python's infrastructure est un code.`@modal.function(gpu="A100")`La fonction de décoration, une section de commandes
- Le temps de facturation par seconde: le temps de chargement commence par 2 à 4 secondes avec le préchauffement; < 1s pour les petits modèles.
  Le temps de chargement est de 2 à 4 secondes.
- $87M Series B at $1.1B évaluation (2025). Le score le plus fort de l'expérience des développeurs dans des enquêtes indépendantes.
  Le financement de la société$87M，估值 $1.1B(2025)。 indépendants enquête dans les développeurs expérience évaluation la plus élevée。

### Réplication  largeur multimodal

- La plateforme par défaut pour les modèles d'image, vidéo et audio.
  Traduction anglaise: selon la prédiction de payer.
- L'intégration des écosystèmes (Zapier, Vercel, plugins CMS).
  Le système de gestion de la gestion des ressources humaines est un système de gestion de ressources humaines.
- Moins compétitif sur les taux de LLM par jeton mais gagne sur la variété multimodal.
  L'économie de l'économie est un facteur de croissance économique.

### Native à rayons

- Construit sur Ray; RayTurbo est le moteur d'inférence propriétaire d'Anyscale (compétient avec vLLM).
  Le projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet
- Le meilleur pour les charges de travail Python distribuées où l'étape d'inférence est un nœud dans un graphique plus grand.
  Le plus adapté à la conception des étapes est le plus grand de l'ensemble des étapes de Python.
- Gestion des clusters Ray; intégration étroite avec Ray AIR et Ray Serve.
  Le groupe de travail de Ray Ray est composé de:

### Par jeton par minute  lorsque chacun gagne

Le jeton a du sens lorsque la charge de travail est insensible à la latence et débordante  vous ne payez que pour ce que vous utilisez.

> Lorsque la charge de travail est sensible au retard et à l'élan, le coût du jeton est plus raisonnable.

Règlement grossier: pour les charges de travail supérieures à ~ 30% d'utilisation continue d'un GPU dédié, par minute (Baseten, Modal) commence à battre par jeton (Fireworks, Together).

> Pour les GPU spécialisées, le taux d'utilisation continue dépasse environ 30% de la charge de travail, selon le分钟 (basé·Modal) commence à être meilleur que le token (Fireworks Together)

> **【中文解读】**Le cœur de la sélection du modèle de prix est le taux d'utilisation. Le coût de la mise à jour est basé sur la taille du modèle, le coût de la mise à jour est basé sur la taille du modèle.

> **【拓展：推理经济学趋势】**Le coût de la formation de l'équipe de formation de niveau 4 de la GPT à partir de 2023 est en baisse d'environ 90%$30/M tokens 降到 2025 年的 $Les tendances sont les suivantes: modèle quantification (INT8/INT4) ‧ meilleur lot 调度、自研芯片竞争和开源推理引擎 (vLLM/SGLang) ‧ maturation.

### Le moteur sur mesure est le vrai fossé

Chaque plateforme au-dessus de vLLM et SGLang revendique un moteur personnalisé. FireAttention, RayTurbo, la pile d'inférence de Baseten.

> Chaque plateforme au-delà de VLLM et SGLang affirme avoir un moteur de développement autonome. FireAttention, RayTurbo, Baseten, .

### Les chiffres que vous devriez vous rappeler

- Location de GPU pour feux d'artifice: augmentation d'une heure de 1 $ à compter du 1er mai 2026.
  Le prix de la GPU de la mise à feu est de 1 $ / 1 heure.
- Précédent: 4 fois moins de latence que vLLM sur des configurations équivalentes.
  Le feu de forêt est un feu de forêt.
- Ensemble: 50-70% moins cher que Replicate sur LLM.
  En même temps, le nombre de personnes qui ont été vaccinées est de 50 à 70%.
- Valorisation du basétain: $5B (Series E, Jan 2026, $300M de tour).
  Le mot "baset" est traduit par "baset".$5B（E 轮，2026 年 1 月，$300 M de roues
- Valorisation des capitaux: 1,1 milliard de dollars (série B, 2025).
  Nom de fichier: "B"
- Les battements par minute par jeton au-dessus de ~ 30% d'utilisation soutenue.
  Le taux d'utilisation continue dépasse environ 30% 时分钟优于代币。

## Utilisez-le avec le cadre de réalisation
```figure
cost-per-token
```

## Utilisez-le

`code/main.py`Les résultats de cette étude ont été analysés en fonction des résultats obtenus par les six fournisseurs sur une charge de travail synthétique sur différents modèles de prix.$/day and effective $- M. Pour trouver le break-even entre par-token et par-minute.

> `code/main.py`Comparer les modèles de prix de six fournisseurs sur la charge de travail synthétique.$/天和等效 $/M tokens。运行它找到按代币 和按分钟的亏平衡点。

> **【中文解读】**La plupart des entreprises ont été chargées de la production de produits de haute qualité par rapport aux six fournisseurs.$/day）和等效每百万 token 成本（$/M tokens), vous aider à trouver le point de croisement selon le jeton et selon le débit de la minute.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-inference-platform-picker.md`. Compte tenu du profil de charge de travail, de la SLA et du budget, choisit la plateforme d'inférence principale et nomme le deuxième.

> 本课产 出 `outputs/skill-inference-platform-picker.md` donner une définition de la charge de travail, des accords de travail et des budgets, choisir la principale plateforme de formation et nommer les options.

> **【拓展：推理平台选型决策树】**选型决策路径:(1) 是否需要 < 50ms TTFT? 是 → Groq/Cerebras;(2) 是否需要自托管/合规? 是 → Baseten/Modal;(3) 是否需要最大模型广度? 是 → Together/OpenRouter;(4) 是否需要多媒体模型? 是 → Replicate/Fal;(5) 默认 → Fireworks(延迟优化) or Together(成本优化)

## Les exercices

1. On court .`code/main.py`À quelle utilisation continue Baseten (par minute) bat Fireworks (par jeton) pour un modèle 70B sur un H100?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Baseten (en fonction de la minute) ◊ Dans quel état de fonctionnement le modèle 70B supérieur à celui des feux d'artifice (en fonction de la minute)?
2. Votre produit sert à la génération d'images plus le chat plus le dialogue par texte.
   Le produit fournit des images générées, des discussions et des textes.
3. Les feux d'artifice augmentent les prix d'un dollar par heure sur votre modèle principal. Modélisez l'impact des coûts mixtes si 40% de votre trafic passe à la catégorie de lot (50% de réduction).
   Le feu de forêt va être le principal modèle à 1$/heure. Si 40% du flux est transféré au niveau de la masse, il va être le plus rapide.
4. Un client réglementé a besoin de GPU dédiées SOC 2 Type II + HIPAA +. Quelles trois plateformes sont viables et laquelle gagne sur FinOps?
   Un client sous surveillance a besoin de SOC 2 Type II + HIPAA + GPU spécial.
5. Comparer le coût par 1000 prédictions pour Llama 3.1 70B sur Fireworks sans serveur, ensemble à la demande, Baseten dédié, et Replicate API.
   Comparer Llama 3.1 70B en Fireworks 无服务器、Together 按量、Baseten 专用和复制 API 上每1000次预测的成本──每天10次预测哪个最便宜?每天10,000次呢?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Custom silicon | "non-GPU chips" | Groq LPU, Cerebras WSE, SambaNova RDU — optimized for decode | 自研推理芯片——Groq LPU、Cerebras WSE 等 |
| FireAttention | "Fireworks engine" | Custom attention kernel; marketed at 4x lower latency than vLLM | Fireworks 自研注意力引擎，号称比 vLLM 快 4x |
| Truss | "Baseten's format" | Model packaging manifest; dependencies + secrets + serving config | Baseten 的模型打包格式，包含依赖、密钥、服务配置 |
| Per-token | "API pricing" | Charge by tokens consumed; pay for no idle | 按 token 计费——只付实际使用量 |
| Per-minute | "dedicated pricing" | Charge by wall-clock GPU time; wins at high utilization | 按分钟计费——高利用率时更划算 |
| Per-prediction | "Replicate pricing" | Charge per model invocation; common for image/video | 按预测次数计费——常见于图像/视频模型 |
| RayTurbo | "Anyscale engine" | Proprietary inference on Ray; competes with vLLM on Ray clusters | Anyscale 基于 Ray 的自研推理引擎 |
| Batch tier | "50% off" | Non-interactive queue at reduced rate; common on Fireworks, OpenAI | 批量推理队列——半价用于非交互任务 |
| Fine-tuned at base rate | "Fireworks LoRA" | Charge LoRA-served requests at base model's rate (differentiator) | 微调模型按基础模型费率计费 |

## Encore une lecture

- [Fireworks Pricing](https://fireworks.ai/pricing) Tarifs par jeton, niveau de lot, location de GPU.
- [Baseten Pricing](https://www.baseten.co/pricing/) taux par minute, capacité engagée, niveaux d'entreprise.
- [Modal Pricing](https://modal.com/pricing) vitesses de GPU par seconde et niveau libre.
- [Together AI Pricing](https://www.together.ai/pricing) Catalogue de modèle et tarifs par jeton.
- [Anyscale Pricing](https://www.anyscale.com/pricing) RayTurbo et géré Ray prix.
- [Northflank — Fireworks AI Alternatives](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference) évaluation comparative.
- [Infrabase — AI Inference API Providers 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) paysage des fournisseurs.
