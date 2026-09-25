# SGLang et RadixAttention pour les charges de travail lourdes préfixes
# Préfixe-cache de service  RadixAttention et réutilisation KV

> Traitez le cache KV comme une ressource réutilisable de première classe stockée dans un arbre radix et modifiez le calendrier avec lui: au lieu de FCFS (first-come, first-served) comme des horaires vLLM, un planificateur conscient du cache priorise les demandes avec des préfixes partagés plus longs  efficacement un traversage de radix de profondeur pour que les branches chaudes restent résidentes dans HBM. SGLang est le moteur qui a construit en fonction de cette idée. Sur Llama 3.1 8B avec des requêtes 1K similaires à ShareGPT, SGLang atteint ~ 16.200 tok/s à ~ 12.500 de vLLM, un avantage de ~ 29%. Sur les charges de travail RAG lourdes avec préfixe, l'avantage atteint 6,4x. Sur les charges de travail en forme de clonage vocale, le taux de clics a été supprimé de 86%. Déployé sur plus de 400 000 GPU en 2026 sur xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. Le problème est que le nombre 6.4x s'évapore lorsque le préfixe de commande est incohérent.

> **【中文解读】**Ce chapitre présente la SGLang et RadixAttention  par le biais de la prévention du partage de l'efficacité de la réflexion 
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

>  **【前置】**Je suis en train de faire une mise à jour de la série de télécommunications.
>  **【类比】**SGLang RadixAttention = " memoriere图书馆"。vLLM = 每次重新查目录;SGLang = 热门前(系统提示+RAG context)存 radix tree 复用。Llama 3.1 8B 在 ShareGPT 上比 vLLM 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在40万+ GPU(xAI、LinkedIn、Cursor)──关键:前必须稳定排序才有效──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Diagramme RadixAttention: comment les préfixes sont stockés dans un arbre radix et comment les blocs KV sont partagés entre des séquences enracinées dans la même branche.
  Le code de radix est un code de radix.
- Expliquez pourquoi le système de planification de cache est mal utilisé pour le trafic de préfixes.
  Expliquer pourquoi le flux de données de l'équipement de stockage est erroné.
- Calculer l'accélération attendue pour une charge de travail en fonction du taux de pré-cache et de la distribution de longueur rapide.
  Traduction anglaise: given determination 缓存命中率和快速 长度分布,计算工作负载的预期加速──
- Nommez la discipline de commande rapide qui rend le nombre 6.4x réel par rapport à un avantage perdu.
  Le récit de la révélation de la Bible est un récit de la révélation de la Bible.

## Le problème , l' introduction du problème

> **【中文解读】**Le service de démarche traditionnelle va rapidement répondre à chaque demande 视为不透明 Même 5000 RAGs Demande de partage du même 2000 Token 系统提示, vLLM également exécutera 5000 fois le pré-remplissage complet.

> **【拓展：前缀共享在 Agent 场景的价值】**L'agent 工作负载天然具有前共享特征:系统提示、工具方案、少数拍示例、对话历史跨请求重复──Cursor(AI 代码编辑器) en 2026 rapportant son agent 调用中系统提示 + 工具定义占快速的80%, 仅用户查询部分不同──使用SGLang的RadixAttention 后, ces partages 前只需计算一次,后续请求复用KV Cache,将推理成本降低60-80%──

Le service classique traite le prompt de chaque requête comme opaque. Même lorsque 5000 requêtes RAG commencent toutes avec le même prompt système de 2 000 jetons plus le même préambule de récupération, vLLM remplit ce préfixe de 2 000 jetons 5 000 fois.

> Le service classique va répondre à chaque demande de manière rapide. Même 5 000 RAG peuvent demander le même type de 2 000 jetons.

L'observation: les commandes dans les charges de travail agentique et RAG partagent presque toujours de longs préfixes. Les commandes système, les schémas d'outils, quelques exemples de prises de vue, les en-têtes de récupération, l'historique de conversation  toutes se répètent à travers les demandes. Si vous avez stocké le cache KV pour ce préfixe une fois et l'avez réutilisé, vous ne le remplissez pas à nouveau.

> 观察:Agent 和 RAG 工作负载中的提示 几乎总是共享长前──系统提示、工具方案、少数截图示例、检索头、对话历史都在请求间重复── si vous stockez une fois 缓存并复用前的 KV,就不需要再预填──

RadixAttention fait exactement cela. Les jetons sont indexés dans un arbre radix; chaque nœud possède des blocs KV pour la séquence de jetons sur son chemin de la racine. Une nouvelle demande passe à travers l'arbre: tout nœud dont le jeton correspond réutilise les blocs KV de ce nœud. Le coût de remplissage devient proportionnel au suffixe "nouveau", pas le prompt complet.

> RadixAttention est en train de le faire. Tous les symboles de chaque nœud possèdent des blocs KV de la séquence des symboles de la racine à la route.

Le défi est de planifier. Si deux demandes partagent un préfixe de 2000 jetons et qu'un troisième partage seulement 200 jetons du même préfixe, vous voulez servir les deux demandes partagées ensemble afin que le long préfixe reste dans HBM. FCFS fait l'inverse  il sert celui qui est arrivé le premier, éventuellement évacuant la branche chaude avant que la prochaine demande de long préfixe ne frappe.

> Le défi est de réguler. Si deux demandes partagent 2 000 jetons, le troisième partage 200 jetons, vous souhaitez servir simultanément deux demandes partagées pour maintenir le long terme dans le HBM.

## Le concept de base.

### L'arbre radix en tant qu'indice de KV

> **【中文解读】**Radix tree (en anglais: Radix tree) est la structure de données centrale de SGLang. Chaque node possède un jeton de portée et de résolution de KV blocs. Une nouvelle demande est faite pour entrer dans le cadre du code.

Un arbre radix (compact trie) stocke des séquences de jetons. Chaque nœud possède une plage de jetons et les blocs KV calculés pour cette plage.

> Radix tree (紧前树) séquence de jetons de stockage 序列。 chaque point possède un jeton 范围和为该范围计算的 KV块──子节点扩展序列一个或多个 token──

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

Une nouvelle demande est envoyée avec le système prompt + "Context: <doc A>" + "Question: Carol". Le planificateur marche: système préfixe correspondant (124 blocs réutilisés), doc-A branche correspondant (31 blocs réutilisés), puis alloue de nouveaux blocs uniquement pour "Question: Carol" (4 blocs). Coût de remplissage: 4 blocs de nouveaux jetons. Sans l'arbre: 160 blocs. ~40x d'économies sur le remplissage préalable.

> Une nouvelle demande avec un système de suggestion + "Context: <doc A>" + "Question: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块), puis uniquement pour "Question: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### Calendrier en cache

> **【中文解读】**缓存感知调度: 1) la profondeur de la priorité de la priorité du service et de la requête de partage de la distribution de la distribution de l'ensemble des opérations actuelles, maintenir le point de chaleur de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de la distribution de

La réutilisation de Radix est inutile si le cache se détériore.

> Si le stockage continue à se dérouler, le redirectionnement de l'arbre de radix n'a aucun sens.

1. **Depth-first dispatch**Lorsque vous choisissez la prochaine requête de la file d'attente, préférer les requêtes enracinées dans la même branche que le jeu en cours d'exécution. Cela garde la branche chaude coincée.
   Le mot grec traduit par " le mot grec "**深度优先调度**◊ Lorsque vous choisissez la prochaine requête de la liste, choisissez la priorité avec la requête de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de la section de section de la section de section de la section de section de section de la section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de section de
2. **LRU at branch level, not block level**. Éliminer les branches entières (à partir des feuilles les plus courtes utilisées) plutôt que des blocs individuels, de sorte que la forme du cache correspond à la forme du radix.
   Le mot grec traduit par " le mot grec "**分支级 LRU** élimination de l'ensemble des branches (à partir des feuilles les moins utilisées), plutôt que de blocs, afin que la forme du cache correspond à la forme du radix ⋅

La FCFS viole les deux, une demande de partage de 2000 jetons est derrière une demande de partage de 50, puis la branche de 2000 jetons est expulsée pour admettre celle de 50 jetons.

> FCFS 违反两者──一共享2000代币的请求排在共享50代币的请求后面,然后2000代币分支被淘汰以接受50代币的请求──

### Numéros de référence que vous devriez mémoriser

- Llama 3.1 8B, H100, ShareGPT 1K: SGLang ~ 16.200 tok/s contre vLLM ~ 12.500 (~ 29% de bord).
  Le nombre de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de volumes de vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol vol
- RAG avec préfixe lourd (même système + même document, question variable): jusqu'à 6,4x sur SGLang.
  Le nombre de personnes concernées par la loi est de 6,4 à 6,4 fois.
- Charges de travail de clonage vocale: taux de succès de préfixe-cache de 86,4%.
  Le taux de chômage est de 86,4%
- Les taux de production de SGLang: 50 à 99% selon la discipline rapide.
  Le taux de production de l'entreprise: 50 à 99%, dépend du délai de répartition.
- Déployé sur plus de 400 000 GPU en 2026.
  En Chine, la version version version suivante est disponible en version version version originale.

### La commande t'a pris .

> **【中文解读】**6.4x accélération dépendant de l'ordre des suggestions modèles de tableau.`[system, tools, context, history, question]`, parfois construire .`[system, context, tools, history, question]`,radix tree  cannot find shared  on a look at humans, on a look at radix tree are two different sequences 杆 of engineers  is:                                                                                                                                                                                                                                            

> **【拓展：SGLang 在生产中的采用】**SGLang a été déployé sur plus de 40 000 blocs de GPU en 2026, les utilisateurs comprennent xAI(Grok)、LinkedIn、Cursor、Oracle, ainsi que les services de gestion de GCP/Azure/AWS。 Le principal avantage de ces scénarios est l'agent et RAG 工作负载 Le taux de répétition des conseils et outils définis dans ces scénarios est extrêmement élevé。 L'équipe de SGLang est composée de membres de l'UC Berkeley LMSYS(fondateurs de Chatbot Arena, et coopère étroitement avec l'équipe de vLLM。 Les deux ne sont pas de compétition strictevLLM a également ajouté un préfixe de mise en cache 功能︎ en 2026

Le nombre 6.4x repose sur une commande cohérente de modèle de prompt. Si votre client construit des commandes comme `[system, tools, context, history, question]`dans certaines demandes et `[system, context, tools, history, question]`Ce qui ressemble à un préfixe commun à un humain sont deux séquences distinctes à l'arbre radix.

> 6.4x le nombre dépend de l'ordre de la demande de correspondance. Si votre clientèle est construite dans certaines requêtes.`[system, tools, context, history, question]`, entre autres requêtes`[system, context, tools, history, question]`Pour les humains, l'arbre est commun, pour les arbres de radix, il y a deux séquences différentes.

Le levier de l'ingénieur: votre modèle de prompt est une clé cache. Fixer l'ordre. Mettre tout ce qui est immuable (système, outils, schémas) en premier. Mettre le contexte de récupération ensuite. Mettre la question utilisateur en dernier. Ne pas interférer le contenu dynamique dans le préfixe.

> 工程师的杆:你的提示 模板是缓存键──固定顺序──将所有不可变内容(系统、工具、方案) 放最前──检索上下文放中间──用户问题放最后──不要在可缓存前中交错动态内容──

Cas réel de la recherche: déplacer le contenu dynamique hors du préfixe cacheable a pris un déploiement de 7% à 74% taux de succès de cache en une seule modification.

> Dans le cas réel de l'étude: le transfert de contenu dynamique vers un cache prévisible, le taux de cache prévisible de déploiement unique est passé de 7% à 74%[2].

### Où RadixAttention gagne et perd

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**SGLang et vLLM sont en phase de stockage de données: dans Llama 3.1 8B H100, SGLang atteint ~16,200 tok/s par rapport à vLLM ~12,500 tok/s  29% 优势; dans la phase de stockage de données RAG à usage répété à la gravité  6.4x; dans la phase de stockage de données de données de travail de l'ensemble de SGLang  86%  mais vLLM a également ajouté le caching préfixe et le caching de cache-conscient de l'itinéraire en 2026  Rust 实现)                                                                                                                                                                                      

Les gagnants:
- RAG (même préambule de récupération, question différente).
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- Agents (les mêmes schémas d'outils, les requêtes variées).
  Le même outil, différentes enquêtes)
- Chattez avec le système de longue durée.
  Le langage est le langage de la langue.
- Charges de travail vocales/visibles avec préambules répétées.
  Le texte de la première partie est le texte de la première partie.

Perte (retour à la capacité de débit au niveau vLLM):
- Génération à coup unique avec des instructions uniques (complétation du code, chat ouvert sans réponse du système).
  Le code complément complet, sans système de suggestion de discussion ouverte.
- Des instructions dynamiques où chaque demande interpose un contenu unique dans le préfixe.
  Chaque requête est une requête en temps réel.

### Pourquoi c'est un problème de planificateur, pas seulement un problème de noyau

Vous pouvez implémenter la réutilisation de KV comme un truc du noyau. L'idée de SGLang est que la réutilisation ne paie que si le planificateur garde le branch résident chaud. Une politique naïve de "réutilisation si disponible" va faire tourner le cache sous charge mixte. Le planificateur indexé par radix-arbre est ce qui transforme le truc du noyau en un avantage de production de 29%.

> Vous pouvez réaliser la KV réutilisation pour les techniques nucléaires. Les idées de SGLang sont que la réutilisation est seulement utile dans le régulateur pour maintenir la chaleur à la fois permanente et régulière.

### Interaction avec le VLLM

Les deux systèmes ne sont pas des concurrents stricts.`--enable-prefix-caching`Le vide a été fermé mais n'a pas complètement disparu  L'ensemble de la pile de SGLang est radix-first; vLLM l'a greffé. Pour les charges de travail dominées par la réutilisation de préfixes, SGLang reste la norme par défaut. Pour le serveur à usage général sans modèles de préfixes forts, vLLM reste égal ou meilleur.

> 两个系统不是严格竞争者──2026年 vLLM 添加了前缓存(`--enable-prefix-caching`Le système de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de l'équipement de routage de routage de l'équipement de routage de routage de l'équipement de routage de routage de l'équipement de routage de routage de l'équipement de routage de routage de routage de la ligne de routage de routage de la ligne de routage de routage de la ligne de routage de routage de routage de la ligne de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de routage de

## Utilisez-le avec le cadre de réalisation
```figure
roofline
```

## Utilisez-le

`code/main.py`Il implémentera un cache KV de jouet radix-tree plus un planificateur avec deux politiques: FCFS et cache-conscient. Il exécute la même charge de travail à travers les deux, rapporte le taux de cache préfixe et le delta de débit. Puis il exécute une charge de travail "scrambled ordering" pour montrer l'effondrement de 6,4x.

> `code/main.py`实现 un simulateur de radix tree KV 缓存加两个策略调度器:FCFS 和缓存感知──用两者运行相同工作负载,报告前缓存命中率和吞吐量差异──然后运行"乱序排序"工作负载显示 6.4x 崩──

## Envoyez-le . Produit .

> **【拓展：前缀缓存策略选择】**2026  Cache dispose de trois niveaux: 1) 应用级语义缓存(Phase 17·14) 在调用LLM 前用嵌入相似度匹配历史响应,命中率 10-70%;(2) 服务端前缓存(SGLang RadixAttention / vLLM préfixe caching) 复用KV Cache,10x 延迟降低;(3) 跨节点缓存路由(Phase 17·11) 通过缓存-awaren router 将请求路由由由到持有前的副本.

Cette leçon produit `outputs/skill-radix-scheduler-advisor.md`. Compte tenu de la description de la charge de travail (forme de modèle de demande, modèle de récupération, nombre de locataires concurrents), il produit une ordonnance de demande de demande et une recommandation de mise en œuvre de la SGLang.

> 本课产 出 `outputs/skill-radix-scheduler-advisor.md`◊ donner une description de charge de travail                                                                                                                                                                                                                                                           

## Les exercices

1. On court .`code/main.py`. Comparer FCFS et cache-conscient sur la même charge de travail.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Comparer les FCFS et les perceptions de stockage sur la même charge de travail.
2. Modifiez la charge de travail afin que les instructions se déplacent aléatoirement `[system, tools, context]`- Pourquoi le taux de coupe ?
   Modifier le travail de charge de faire prompt 随机排列 `[system, tools, context]`Qu'est-ce qui a changé dans le taux de mortalité ?
3. Calculer le coût de HBM de maintenir un système de prompt de 2000 jetons résident comme une branche radix sur Llama 3.1 8B. Comparez avec le coût d'un lot de 16 séquences sans réutilisation de préfixes.
   L'exemple de la méthode de calcul de la Llama 3.1 8B est la méthode de calcul de la Llama 3.1 8B.
4. Lisez le document SGLang RadixAttention. Expliquez en trois phrases pourquoi l'expulsion de l'ULR en forme d'arbre est supérieure à celle de bloc sous une charge lourde de préfixe.
   Le texte de la lettre de référence est le texte de la lettre de référence de la lettre de référence de la lettre de référence de la lettre de référence.
5. Un client rapporte seulement 8% de taux de cache. Nommez trois causes probables et le diagnostic que vous exécuterez pour chacune.
   Le taux de mortalité de l'enfant est de 8%.

## Les termes clés

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Encore une lecture

- [SGLang GitHub](https://github.com/sgl-project/sglang) source et documents.
- [SGLang documentation](https://sgl-project.github.io/) RadixAttention et détails de planification.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) la référence de conception.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) numéros de référence et raison de l'agrément.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) mise en œuvre de la même façon que la radix de vLLM, pour comparaison.
