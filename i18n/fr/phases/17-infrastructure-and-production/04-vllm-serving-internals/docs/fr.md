# VLLM Servir interne: PagedAttention, Batching continu, pré-remplissage par morceaux
# Servir les moteurs internes  PagedAttention, batchage continu, préchargement en morceaux

> Le débit moderne du moteur de service repose sur trois défauts de composition, pas sur un seul truc. PagedAttention est toujours activée. Le batchage continu injecte de nouvelles demandes dans le batch actif entre les itérations de décode. Des tranches de pré-remplissage en morceaux font des longues instructions, donc les jetons de décode ne meurent jamais de faim. Allumez les trois et un Llama 3.3 70B FP8 sur un H100 SXM5 pousse 2 200 à 2 400 tok/s à 128 simultanément  environ 25% au-dessus de la vLLM et 3-4x une boucle PyTorch naïve. Cette leçon lit le programmeur et le noyau d'attention de vLLM  le moteur de référence pour les trois techniques  à un niveau que vous pouvez diagrammer, et se termine par un batcher continu de jouets en `code/main.py`que les horaires se remplissent et décodent de la même manière que VLLM.

> **【中文解读】**vLLM en 2026 domination est basée sur trois complexes optimisation:PagedAttention(分页注意力)始终开启;连续批处理在解码代间注入新请求;分块预填片长提示以防止解码代币饥饿──三者全开时,Llama 3.3 70B FP8 在单卡H100上以 128并发达2,200-2,400 tok/s比朴素PyTorch 循环快 3-4倍──

> **【拓展：vLLM → LLM 推理服务标准】**Le système d'exploitation de l'application de la technologie de gestion de l'environnement est un système de gestion de l'environnement de l'entreprise.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Le projet de loi de 2026 est un projet de loi de 2026 qui vise à améliorer la qualité de la vie des personnes.
>  **【类比】**vLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache(像操作系统虚拟内存分页,碎片率 < 4%);Continuous Batching = 动态拼单(新请求随时插入运行批);Chunked Prefill = 切长快速(长输入切片避免阻塞解码)。Llama 3.3 70B FP8 sur H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 ⋅倍

## Objectifs d'apprentissage

- Expliquez PagedAttention comme un allocateur de cache KV: blocs, tables de blocs, et pourquoi la fragmentation reste inférieure à 4% à la charge de production.
  Le taux de débit reste à 4% en fonction de la charge de production.
- Diagramme de la séquence continue au niveau de l'itération: comment les séquences terminées quittent le lot et les nouvelles se joignent sans se vider.
  Dans le cadre de la formation de la formation, le personnel de formation doit être informé de la manière dont les travaux sont effectués.
- Décrire le pré-remplissage en morceaux dans une phrase et nommer la métrique de latence qu'elle protège (indice: c'est la queue TTFT, pas le débit moyen).
  Le texte de la traduction chinoise est le suivant:
- Nommez le 2026 vLLM v0.18.0 gotcha qui mord les équipes permettant chaque optimisation à la fois.
  Le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la

## Le problème , l' introduction du problème

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批处理将所有请求填充到最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV Cache 碎片率从60-80% 降至4% 以下) 连续批处理(在解码代间动态加入新请求) 分块预填充(将长提示切片以防止解码饥饿) △

Une boucle de service PyTorch naïve exécute une demande à la fois: jetonner, pré-remplir, décoder jusqu'à EOS, retourner. Pour un utilisateur, cela fonctionne. À cent, c'est une file d'attente de patients. La correction évidente  par lots statiques  passe chaque demande à la plus longue demande dans la fenêtre, passe chaque décode à la plus longue sortie attendue et arrête l'ensemble du lot sur la séquence la plus lente. Vous payez pour des rembourrages que vous n'utilisez jamais, et les demandes rapides attendent les plus lentes.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填充、解码直到EOS、返回。 un utilisateur c'est un utilisateur qui attend patiemment une seule fois.

VLLM résout trois problèmes à la fois. PagedAttention empêche la fragmentation du cache KV de consommer 60-80% de la mémoire de la GPU de la manière de l'allocation contigue classique. Le batchage continu permet aux demandes de rejoindre et de laisser le lot entre chaque itération de décode, de sorte que le lot est toujours plein de travail réel. Un pré-remplissage en morceaux casse un token 32k en 512 tokens qui interviennent avec le décode, donc un long prompt ne gelera pas chaque token de décode sur le GPU.

> VLLM une fois résoudre trois problèmes. Attention payée: empêcher KV de stocker des morceaux de données comme la distribution continue classique de 60 à 80% du GPU. Continuation de traitement de la demande entre chaque génération de code.

La production par défaut de 2026 est activée, vous devez comprendre ce que chacun fait parce que les modes d'échec sont tous sur le planificateur, pas le modèle.

> La production par défaut de 2026 est ouverte à trois. Vous devez savoir ce que chacun doit faire, car le mode défaut est sur le régulateur, et non sur le modèle.

## Le concept de base.

### PagedAttention en tant que système de mémoire virtuel

> **【中文解读】**PagedAttention 借借鉴操作系统虚拟内存分页思想管理 KV Cache。 Traditionellement, la répartition continue est faite pour chaque séquence pré-distribution maximale de longueur(comme 8192 jetons), mais la demande moyenne ne prend que 1500 jetons, dépense 82% de HBM。PagedAttention va diviser le Cache KV en un bloc de taille fixe(fait 16 jetons), chaque séquence a un bloc de carte de cartographie position logique à l'ID du bloc physique, selon la répartition nécessaire, le taux de fragments inférieur à 4%。 c'est le seul distributeur de vLLM, par le biais de`--gpu-memory-utilization`(默认 0.9) contrôler KV Cache HBM utilisable

> **【拓展：KV Cache 内存管理演进】**KV Cache 内存管理 a connu trois générations de développement: 1) 连续预分配简单但浪费60-80%内存; 2) PagedAttention(vLLM 2023) 分页管理,碎片率 <4%, devenir un standard de l'industrie; 3) RadixAttention(SGLang 2024)                                                                                                                                                                                                                         

Un cache KV est `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`Pour Llama 3.3 70B à 8192 jetons, c'est environ 1,25 Go par séquence dans BF16. Si vous réservez 8192 slots à l'avance pour chaque demande mais que la demande moyenne ne utilise que 1500 jetons, vous gaspillez environ 82% du HBM que vous avez réservé.

> Chaque séquence de KV est en stockage`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element` Llama 3.3 70B en 8192 jetons 时, BF16 下每序列约 1.25 GB── Si vous pré-réservez 8192 槽位 pour chaque requête, mais que la demande moyenne ne consomme que 1500 jetons, vous avez gaspillé environ 82% 预留的HBM── classique de traitement de lot a supporté ce gaspillage──

PagedAttention emprunte l'idée de la mémoire virtuelle du système d'exploitation. Le cache KV n'est pas contigu à chaque séquence. Il est alloué en blocs de taille fixe (par défaut 16 jetons). Chaque séquence a une table de blocs qui cartographient ses positions logiques de jetons aux identifiants de blocs physiques. Lorsqu'une séquence dépasse ses blocs alloués, un autre bloc est ajouté. Quand elle est terminée, ses blocs retournent dans le pool.

> PagedAttention  emprunt à l'opérationnement système de l'inventaire virtuel de l'idée──KV 缓存 n'est pas de chaque séquence continuée── elle est fixée à un bloc de taille fixe(défaut 16 jetons) distribuée── chaque séquence a un bloc de table, le jeton logique 位置 est mappé à l'ID du bloc physique── lorsque la séquence croît au-delà du bloc distribué, ajoutez un nouveau bloc── après termination, le bloc retourne dans la pile──

La fragmentation diminue de 60-80% (classique) à moins de 4% (Attention page). Vous ne pouvez pas activer PagedAttention avec un drapeau  c'est le seul allocateur vLLM navires. Le bouton est `--gpu-memory-utilization`(par défaut 0.9), qui indique à vLLM combien de HBM doit réserver pour les blocs KV après le chargement des poids et des activations.

> Le taux de débit est passé de 60-80% à 4% en bas.`--gpu-memory-utilization`(默认 0.9), dites à VLLM dans le chargement du poids et activation après pour KV bloc pré-retraite combien HBM.

### Partage continu au niveau de l'itération

> **【中文解读】**连续批处理在每个解码步骤之间做出接受/释放决策──每个代:(1) 移除已完成(EOS或 max_tokens) 的序列;(2) 检查等队列,如果有空 KV块则接收新序列;(3) 执行前向传播一次对RUNNING列表中的所有序列──批次大小不定,不同输出位置的序列共享一次融合前向计算──2026年 vLLM V1 调度器的核心不变量是:调度器解码每个代运一次,而不是每一个请求运一次──

L'ancien " batchage dynamique " attendait une fenêtre (disons 10 ms) pour remplir un lot, puis exécutait le préfill + décode + décode + décode jusqu'à ce que chaque séquence soit terminée.

> 旧的"动态批处理" attends une fenêtre (environ 10ms) pour remplir des lots, puis fonctionne préfill + décode + décode + décode jusqu'à ce que chaque séquence soit terminée.

Le batchage continu fonctionne entre chaque étape de décode.`RUNNING`à chaque itération:

> 连续批处理在每个解码步骤之间操作―― sera appelé `RUNNING`列表──每次代:

1. Toute séquence dans `RUNNING`qui vient de frapper EOS ou max_tokens est supprimé.
   Le mot grec traduit par " le mot grec "`RUNNING`Toute séquence de jetons EOS ou max_tokens est supprimée.
2. Le planificateur regarde la file d'attente. S'il y a des blocs KV gratuits, il admettra de nouvelles séquences (pré-remplir ou reprendre).
   Si il y a un bloc KV, il accepte la nouvelle séquence (préchargement ou récupération)
3. Le passe avant passe sur tout ce qui est maintenant en .`RUNNING`, émettant un nouveau jeton par séquence.
   Le mot " propagation " est traduit par " propagation "`RUNNING`Chaque séquence émet un nouveau jeton.

Les séquences à différentes positions dans leur sortie partagent une fusion vers l'avant.`V1 scheduler`. L'invariable de clé: le planificateur fonctionne une fois par itération de décode, pas une fois par requête.

> 批次大小从不填充到固定数字――输出不同位置的序列共享一次融合前向传播――2026年 vLLM 中称为 `V1 scheduler`◊ Key Notes: chaque référencement fonctionne une fois, et non chaque requête fonctionne une fois.

### Le préchargement en morceaux protège la queue TTFT

> **【中文解读】**Le dépôt de blocs a résolu le problème de longueur de file d'attente. Un dépôt de 32K sur le modèle 70B nécessite environ 800 ms de pré-completude, tandis que tous les autres dépôts de blocs sont en attente. Le dépôt de blocs est effectué en un bloc de taille fixe.

> **【拓展：vLLM 生产部署最佳实践】**Les principales configurations du VLLM en 2026 comprennent:`--gpu-memory-utilization 0.9`预留 90% HBM 给 KV Cache;(2) `--max-model-len` selon la définition de la demande réelle et non la valeur maximale par défaut;(3) 分块预填充默认开启但与某些推测解码模式不兼容;(4) `--enable-prefix-caching`Dans le cadre de la RAG/Agent, il est possible de réduire considérablement la répétition du pré-remplissage;

Le préfill est lié au calcul. Une demande de 32k-token sur Llama 3.3 70B prend ~ 800 ms de préfill pur sur un H100. Pendant que le préfill fonctionne, décodez les jetons pour chaque autre séquence dans la séquence d'attente. Dans une boucle de service, la latence de premier jeton (TTFT) d'un long demande devient la latence inter-token (ITL) blip pour des dizaines d'autres utilisateurs.

> Le prélèvement est un type de calcul intensif. Llama 3.3 70B sur un jeton 32K de pointe sur un seul H100 sur une seule carte nécessite environ 800 ms de pure prélèvement. Le prélèvement de pointe sur toutes les autres séries de la série est en attente.

Le pré-remplissage par morceaux divise le pré-remplissage en morceaux de taille fixe (par défaut 512 jetons) et planifie chaque morceau en unité. Entre les morceaux, le planificateur peut avancer les séquences de décode par un jeton. Vous échangez un petit hit de latence de pré-remplissage absolu (quelques ms par morceau) pour un jitter de décode beaucoup plus faible. P99 ITL sous charge mixte tombe de ~ 50 ms à ~ 15 ms dans les benchmarks publiés.

> Le bloc de pré-remplissage sera pré-rempli en un bloc de taille fixe (en défaut 512 jetons), chaque bloc étant un unité de régulation.

### Les trois défauts interagissent

Les trois caractéristiques se prennent l'une l'autre. PagedAttention donne au planificateur une ressource KV à grains fins à négocier.`RUNNING`L'établissement de la liste  est une politique de planification supplémentaire, et non un système séparé.

> Les trois caractéristiques sont interdépendantes. L'attention payée pour le régulateur fournit des ressources de KV de petite taille pour le régulation.`RUNNING`La décision prise sur la liste est une autre stratégie de régulation, pas un système indépendant.

Vous n'avez pas besoin de connaître chaque drapeau, vous devez savoir ce que le planificateur optimise: un bon produit en fonction du budget du bloc KV, soumis à la découpe de pré-remplissage en morceaux.

> Vous n'avez pas besoin de savoir chaque marque. Vous avez besoin de savoir ce que le régulateur optimise.

### Le 2026 v0.18.0 vous a obtenu

> **【中文解读】**vLLM v0.18.0 中 ne peut pas être activé simultanément `--enable-chunked-prefill`Et le modèle de projet`--speculative-model`La seule exception est le N-gram GPU de régulateur V1 推测解码. Il est possible que l'équipe de l'optimisation de la mise en œuvre de tous les segments de démarrage soit confrontée à une erreur de fonctionnement lors de son démarrage, et non à une dégradation de la logique. Si le résultat du démarrage de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise en œuvre de mise

Dans vLLM v0.18.0 vous ne pouvez pas combiner `--enable-chunked-prefill`avec décoding spéculatif de modèle de projet (`--speculative-model`) L'exception documentée est le décoding spéculatif de GPU N-gramme dans le planificateur V1. Les équipes qui déploient chaque drapeau sans lire les notes de sortie ont une erreur de démarrage, pas une régression douce. Si votre gain spéculatif valait la peine de permettre le pré-remplissage en morceaux, revenez au choix  la bonne réponse en 2026 est souvent EAGLE-3 sans pré-remplissage en morceaux, pas un modèle de projet plus pré-remplissage en morceaux qui ne compile pas.

> Dans vLLM v0.18.0, vous ne pouvez pas l'activer simultanément `--enable-chunked-prefill`Et le modèle de projet`--speculative-model`)。 L'exception du dossier est le N-gram GPU du régulateur V1 推测解码。 non lu la publication de la description sur le démarrage de tous les logos de l'équipe rencontré une erreur lors de la mise en service et non une dégradation de la logique。 Si le démarrage du démarrage de la valeur de démarrage du démarrage est de pré-renouvellement, la réponse correcte à la révision de la sélection 2026 est généralement EAGLE-3 et non pas le modèle de projet。

### Les chiffres que vous devriez vous rappeler

- Llama 3.3 70B FP8, H100 SXM5, 128 simultanément, tous les trois en: 2 200-2 400 tok/s.
  Llama 3.3 70B FP8, H100 SXM5,128 并发,三个优化全开:2,200-2,400 tok/s
- Le même modèle, VLLM par défaut (pas de pré-remplissage en morceaux): ~ 1800 tok/s.
  Le code de la carte est le code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
- Le même modèle, PyTorch avant naïf boucle: ~600 tok/s.
  Le modèle de PyTorch est en train de se dérouler.
- Déchets de fragmentation de KV sous PagedAttention à charge de production: < 4%.
  Le taux de débit de KV en production est de 4% en moyenne.
- P99 ITL sous charge mixte: ~15 ms avec pré-remplissage en morceaux, ~50 ms sans.
  L'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe du groupe.

### À quoi ressemble le programmeur

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`C'est exactement cette boucle dans stdlib Python avec de faux nombres de jetons et de faux latences avant.

> `code/main.py`C'est la base de données pure de ce cycle Python 实现, en utilisant le faux nombre de jetons counting et faux avant vers le retard ⋅ run.

## Utilisez-le avec le cadre de réalisation
```figure
tensor-parallel
```

## Utilisez-le

`code/main.py`Simule un planificateur de style vLLM avec des fonctionnalités commutables.

> `code/main.py`模拟一个带有可换功能的 vLLM 风格调度器──运行

- `NAIVE`mode: une demande à la fois, aucune mise en lots.
  Le mot grec traduit par " le mot grec "`NAIVE`模式: une fois une demande, sans traitement de lots.
- `STATIC`mode: plaquette et attente, batchage classique.
  Le mot grec traduit par " le mot grec "`STATIC`模式: remplir et attendre, classique de traitement en lots.
- `CONTINUOUS`mode: admission et libération au niveau d'itération.
  Le mot grec traduit par " le mot grec "`CONTINUOUS`模式: 代级的接收和释放──
- `CONTINUOUS + CHUNKED`mode: pré-remplir les tranches interdites avec décode.
  Le mot grec traduit par " le mot grec "`CONTINUOUS + CHUNKED`模式: pré remplissage 片与解码交错──

La sortie montre le débit total (tokens par seconde virtuelle), la moyenne TTFT et P99 ITL.`CONTINUOUS + CHUNKED`la ligne doit être la principale dans le trafic mixte.

> 输出显示总吞吐量(每虚拟秒代币 数) 、TTFT 平均值和 P99 ITL。`CONTINUOUS + CHUNKED`L'activité de la société est de

## Envoyez-le . Produit .

> **【拓展：LLM 推理引擎对比】**Le système de gestion de la gestion des ressources humaines est basé sur la gestion des ressources humaines et les ressources humaines.

Cette leçon produit `outputs/skill-vllm-scheduler-reader.md`. Compte tenu de la configuration de service (dimension de lot, utilisation de la mémoire KV, taille de pré-remplissage par morceaux, configuration spéculative), il produit un diagnostic de planificateur qui indique lequel des trois défauts est le cou de bouteille et ce qu'il faut régler.

> 本课产 出 `outputs/skill-vllm-scheduler-reader.md`◊ donner un service de configuration (Bot次大小、KV 内存利用率、分块预填大小、推测配置), il génère un diagnostic de régulateur, en indiquant lequel des trois paramètres est le plus efficace et comment le réguler.

## Les exercices

1. On court .`code/main.py`- Comparer`STATIC`à `CONTINUOUS`En ce qui concerne les besoins de la production, la différence entre les besoins de production et les besoins de production est la différence entre les besoins de production et les besoins de production.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ dans la demande de travail mixte`STATIC`et `CONTINUOUS`◊ Quelle est la différence entre la précharge, la décompression ou le retard de la mise en service ?
2. Modifier le programmeur de jouets pour ajouter `--max-num-batched-tokens`. Quelle est la valeur correcte pour un H100 exécutant Llama 3.3 70B FP8 ? (indice: il s'agit d'une fonction de la taille des blocs KV et du nombre de blocs libres, pas de HBM brut.)
   Le référencement est le plus connu.`--max-num-batched-tokens` H100 运行 Llama 3.3 70B FP8 的正确值是多少?
3. Retournez les notes de sortie de vLLM v0.18.0. Quelles combinaisons de drapeaux sont mutuellement exclusives ?
   Le texte de la liste est le même que celui de la liste des autres.
4. Compute le gaspillage de fragmentation du cache KV pour une trace de 1000 requêtes avec une moyenne de 1500 jetons de sortie, std 600 jetons, sous (a) allouement contigu par requête à 8192 max, (b) PagedAttention avec 16 blocs de jetons.
   Le nombre moyen de fichiers de données est de 1 500 fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers fichiers de fichiers fichiers fichiers de fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichiers fichi
5. Expliquez dans un paragraphe pourquoi le préchargement en morceaux aide le P99 ITL mais pas le débit en isolement.
   Le P99 ITL est un système de calcul de la capacité de charge de l'énergie.

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Encore une lecture

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) source officielle sur la compatibilité des pré-remplissages en morceaux et des décodages spéculatifs.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026 libérer la cadence et le comportement spécifique à la version.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) l'écriture originale qui définit encore comment penser à l'allocateur.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) analyse de fragmentation et conception de calendrier.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) V1 détaillé planificateur de marche avec des graphiques de flammes.
