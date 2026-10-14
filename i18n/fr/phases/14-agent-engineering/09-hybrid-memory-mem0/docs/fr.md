# La mémoire hybride: vecteur + graphe + KV (Mem0) 混合记忆:向量+图+KV(Mem0)
# Mémoire hybride: vecteur + graphe + KV

> La mémoire hybride exploite trois magasins en parallèle  vecteur pour la similitude sémantique, KV pour la recherche rapide de faits, graphique pour le raisonnement entité-relation  avec une couche de notation qui les fusionne lors de la récupération.

> **【中文解读】**Mem0 va considérer la mémoire comme trois lignes de stockage  volumes utilisés pour la synonymie  KV utilisés pour la recherche rapide de faits 图 utilisés pour la théorie des relations physiques  un niveau de notation en recherche  fusion  trois  Ceci est le standard de production de la mémoire externe de 2026 

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Expliquez pourquoi un seul stock (vecteur seulement, graphe seulement, KV seulement) est insuffisant pour la mémoire de l'agent.
  Expliquer pourquoi un seul stockage (solo) ne suffit pas à fournir un agent de souvenir.
- Nommez les trois magasins parallèles de Mem0 et ce que chacun optimisera pour.
  Le texte de la loi est le texte de la loi.
- Décrivez le score de fusion de Mem0  pertinence, importance, récente  et pourquoi il s'agit d'une somme pondérée et non d'une hiérarchie.
  Le mémoire est un outil de référence pour la création de la société.
- Implémenter une mémoire de trois étages de jouets dans stdlib avec un `add()`qui écrit à tous les trois et à un`search()`qui fusionne les résultats.
  Le jeu est un jeu de mots.`add()`写入所有三个储存,`search()`Le résultat de la fusion

## Le problème , l' introduction du problème

Un magasin est faux pour l'une des trois classes de requêtes:

> Un seul stockage à trois types de requêtes est erroné:

- **Semantic similarity**"Qu'est-ce que nous avons discuté de la dérive d'agent la semaine dernière?" Vector gagne, KV et la défaite graphique.
  Le mot grec traduit par " le mot grec "**语义相似性**"Nous avons discuté la semaine dernière de quoi l'agent s'est déplacé ?"
- **Fact lookup** "Quel est le numéro de téléphone de l'utilisateur?" KV gagne; vecteur est gaspillé, graphe est exagéré.
  Le mot grec traduit par " le mot grec "**事实查找**" Quel est le numéro de téléphone de l'utilisateur ? " KV 胜出;向量浪费,图过度──
- **Relationship reasoning** "quels clients partagent la même entité de facturation?" Le graphique gagne; vecteur et KV ne peuvent répondre.
  Le mot grec traduit par " le mot grec "**关系推理**" Quels clients partagent le même compte-rendu ? " 图胜出;向量和 KV 无法回答──

Les agents de production émettent les trois en une seule session. Une mémoire d'une seule boutique est toujours mauvaise pour deux d'entre eux.`add`- Je suis là.`search`la surface avec une fonction de notation qui les fusionne.

>  **【类比】**Les trois types de référencement de la bibliothèque de Mem0: le modèle de la bibliothèque de l'écriture de l'écriture de l'écriture de l'écriture de Mem0: le modèle de la bibliothèque de l'écriture de Mem0: le modèle de la bibliothèque de l'écriture de Mem0: le modèle de la bibliothèque de l'écriture de Mem0: le modèle de la bibliothèque de Mem0: le modèle de la bibliothèque de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de Mem0: le modèle de la bibliothèque de Mem0: le modèle de Mem0: le modèle de la méthode: le modèle de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de la méthode de

> Le producteur de production a envoyé toutes les trois requêtes en une seule réunion.`add`- Je suis là.`search`接口后面,并使用评分函数融合它们──

> **【中文解读】**Le système de mémoire à court terme est un système de mémoire à court terme. Il est basé sur la mémoire à court terme.

> **【拓展：Mem0 是目前最流行的 Agent 记忆解决方案之一】**Mem0 (2024-2025) est actuellement l'un des solutions de mémoire les plus populaires,GitHub 25k+ étoiles. Sa structure de trois niveaux: mémoire à court terme (en anglais seulement) ✓ mémoire à long terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme (en anglais seulement) ✓ mémoire à court terme ✓ mémoire à court terme ✓ mémoire à court terme ✓ mémoire à court terme ✓ mémoire à court terme ✓ mémoire à court terme ✓

>  **【前置】**Il faut d'abord comprendre:Phase 14·07(MemGPT) et Phase 14·08(Letta Blocks)Mem0 est leur "répertoire de stockage post-end upgradé"── il faut aussi comprendre les différences entre les trois types de bases de données:

## Le concept de base.

### Trois magasins en parallèle

Mem0 (arXiv:2504.19413, avril 2025) sur `add(text, user_id, metadata)`- Le numéro de la liste:

> Mem0(arXiv:2504.19413,2025 年 4 月) 在 `add(text, user_id, metadata)`上:

1. Extraire des faits candidats du texte (étape axée sur le LLM).
   Le texte de la loi est en français.
2. Écrivez chaque fait dans le vecteur de stockage (embedding) pour la recherche sémantique.
   Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français
3. Écrivez chaque fait dans le magasin KV sur lequel vous avez mis la touche (user_id, fact_type, entité) pour la recherche O(1).
   Le texte de la première partie de la lettre est écrit dans le texte suivant:
4. Écrivez chaque fait dans le graph store (Mem0g) comme des bords taillés pour les requêtes de relation.
   Le texte est écrit dans le livre de la Bible.

Je suis en train de`search(query, user_id)`- Le numéro de la liste:

> Dans le`search(query, user_id)`上:

1. Le magasin vectoriel retourne le top-k en intégrant cosine.
   Le résultat de l'analyse est le résultat de l'analyse de la valeur de l'échantillon.
2. Le magasin KV renvoie des hits directs sur la requête dérivée (user_id, type, entité).
   Le KV 存储返回基于查询推导的 (user_id, type, entité) 键的直接命中──
3. Le graph store renvoie le sous-graphe accessible par les entités de requête.
   Le stockage est de retour de l'objet de la requête.
4. Une couche de scores fusionne les trois.
   Le groupe de travail est composé de trois personnes.

### Scoring de fusion

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

- **Relevance** cosine vectoriel, correspondance exacte KV, poids de la trajectoire du graphique.
  Le mot grec traduit par " le mot grec "**相关性**                                                                                                                                                                                                                                                              
- **Importance** étiqueté au moment de la rédaction ou appris (certains faits comptent plus: noms, identifiants, politiques).
  Le mot grec traduit par " le mot grec "**重要性**写入时标记或学习得到某些事实更重要:姓名、ID、策略)
- **Recency** déclin exponentiel au fil du temps depuis la dernière rédaction ou lecture.
  Le mot grec traduit par " le mot grec "**时效性** depuis la dernière inscription ou lecture l'indice de temps décliné

Les poids sont ajustés par produit.`w_recency`pour les agents de chat; plus élevé `w_importance`pour les agents de conformité; supérieur `w_relevance`pour les agents de récupération.

> ️ **【易错点】**Les données de référence sont les données de référence de la page d'accueil.**后果**: dans le cadre de la réglementation, les faits politiques importants (comme "le utilisateur est un utilisateur limité") ont été repris par le nouveau "hier chat du temps"`w_recency`La vieille importance du temps est trop élevée.**一行修复**Il est également possible de faire des recherches réelles sur les produits de base.

> 权重按产品调优──聊天 Agent 使用更高的 `w_recency`; Conformément à la loi`w_importance`; Inspection agent 使用更高的 `w_relevance`Il y a une autre.

### Mem0g et raisonnement temporel

Mem0g ajoute un détecteur de conflit. Lorsqu'un nouveau fait contredit un bord existant, le bord existant est marqué comme non valide mais non supprimé.

> Mem0g a ajouté un détecteur de conflits. Lorsque les nouveaux faits sont contredisés avec les frontières existantes, les frontières existantes sont marquées comme inefficaces mais non supprimées.

C'est le comportement de conformité que généralise le modèle d'invalidation de Letta.

> C'est le comportement de la Letta 失效模式泛化的合规级.

### Numéros de référence

Les rapports du document Mem0 (2025):

> Rapport de l'équipe de la Commission

- **LoCoMo**(mémoire de longue durée de conversation): 91,6
- **LongMemEval**(mémoire épisodique à long horizon): 93,4
- **BEAM 1M**(indice de référence de mémoire de jeton M): 64,1

Les lignes de base de comparaison (LLM en plein contexte 128k, magasin vectoriel plat, KV plat) perdent toutes 10 points. Les critères de référence ne justifient pas le choix  la forme opérationnelle  mais les chiffres montrent que la conception de fusion n'est pas une erreur d'arrondissement.

> Comparer avec le baseline de l'épreuve de base: la mise en œuvre de la conception de la base de données n'est pas une erreur.

### Taxonomie de portée

Mem0 partage la mémoire par champ:

> Mem0 按范围拆分记忆:

- **User memory** persiste pendant les séances, enfoncée `user_id`- Je suis désolé .
  Le mot grec traduit par " le mot grec "**用户记忆**跨会话持久化, à savoir:`user_id`Pour la clé.
- **Session memory** persiste dans un seul fil.
  Le mot grec traduit par " le mot grec "**会话记忆** dans une ligne de perpétuation.
- **Agent memory** État d'instance par agent.
  Le mot grec traduit par " le mot grec "**Agent 记忆** chaque agent 实例状态──

Chaque écriture choisit un champ. La récupération peut effectuer des requêtes sur des champs avec des poids par champ. Le mélange des champs sans réfléchir est la façon dont vous obtenez "l'assistant a dit à Alice sur le projet de Bob" incidents.

> 🤔 **【困惑】**Q: Mem0 trois types de stockage doivent être déployés, le coût pour les petits équipes est trop élevé, ne peut-on pas seulement utiliser la base de stockage ?**纯聊天机器人**Utilisation de la capacité + KV pour la complexité de moins de 90%);**多用户企业 Agent**Il faut utiliser le dossier, sinon il y aura un accident du genre "Alice voit les données de Bob".

> Chaque fois que vous écrivez, choisissez une gamme. Les recherches peuvent être effectuées à travers la gamme.

### Où ce modèle va mal

- **Embedding drift.**Les résultats vectoriels qui apparaissent bien sur les 100 premières requêtes se dégradent à mesure que le corpus grandit.
  Le mot grec traduit par " le mot grec "**嵌入漂移。**Il est également possible de modifier le contenu de la requête en utilisant la méthode de recherche de l'analyse de données.
- **KV schema creep.** `(user_id, type, entity)`Il semble simple jusqu' à ce que chaque équipe ajoute le sien.`type`- vérifier le type de jeu trimestriellement.
  Le mot grec traduit par " le mot grec "**KV 模式蔓延。** `(user_id, type, entity)`Il semble simple, jusqu'à ce que chaque équipe ajoute son propre.`type`◊ Type de vérification de chaque trimestre
- **Graph explosion.**Un extracteur bruyant ajoute 50 bords par message.`add`- Je ne sais pas.
  Le mot grec traduit par " le mot grec "**图爆炸。**Un extracteur de messages à chaque message ajouter 50 pages de limite par jour`add`调用图写入数; 丢弃低置信度边缘──

## Construisez-le en main
```figure
ae-memory-fusion
```

## Faites-le

`code/main.py`met en œuvre le modèle à trois étages dans stdlib:

> `code/main.py`Utilisation de la base de données standard réalisé trois modes de stockage:

- `VectorStore` similitude naïve de superposition des symboles en tant que substituteur intégré.
  Le mot grec traduit par " le mot grec "`VectorStore`Une simple jeton 重叠相似性替代嵌入──
- `KVStore` dicté sur la touche `(user_id, fact_type, entity)`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`KVStore`以 `(user_id, fact_type, entity)`Pour les livres.
- `GraphStore` bordes typées (objet, relation, objet, valide).
  Le mot grec traduit par " le mot grec "`GraphStore`类型化边主语、关系、宾语、有效)
- `Mem0` façade de haut niveau avec `add()`- Je suis là .`search()`, le score de fusion, et la récupération consciente de la portée.
  Le mot grec traduit par " le mot grec "`Mem0`- Je suis en train de faire une petite fête.`add()`- Je suis là.`search()`、 fusion de l'évaluation et de la portée de l'analyse de la perception
- Une trace de travail sur une conversation multi-utilisateur, multi-session.
  Le mot "conversation" est traduit par "conversation".

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La sortie montre trois voies de rappel distinctes plus le top-k fusionné.`main()`et regarder le changement de classement.

> 输出显示三条独立的召回路径加上融合的顶-k---在 `main()`Le groupe de travail de la société de l'information a été créé en 2008 par le groupe de travail de l'entreprise de l'information.

## Utilisez-le avec le cadre de réalisation

- **Mem0 (Apache 2.0)** prêt à la production. Auto-hébergement avec Postgres + Qdrant + Neo4j, ou utiliser le cloud géré.
  Le mot grec traduit par " le mot grec "**Mem0 (Apache 2.0)**生产就绪──用 Postgres + Qdrant + Neo4j 自托管,或使用托管云──
- **Letta** un noyau/reprise/archivage à trois niveaux; apportez vos propres arrière-plan vectoriels et graphiques.
  Le mot grec traduit par " le mot grec "**Letta** trois niveaux de noyau/reprise/archivage;
- **Zep** alternative commerciale avec KG temporel et extraction de faits.
  Le mot grec traduit par " le mot grec "**Zep**带时序知识图谱和事实提取的商业替代方案──
- **Custom builds** lorsque vous avez besoin d'un contrôle exact sur l'extracteur (conformité) ou les poids de fusion (agents vocaux où la récente domination).
  Le mot grec traduit par " le mot grec "**自定义构建** lorsque vous avez besoin de contrôler précisément le poids du son (en anglais) 

## Envoyez-le . Produit .

`outputs/skill-hybrid-memory.md`génère un échafaudage de mémoire à trois étages avec un scorer de fusion, une taxonomie de champ et une invalidation temporelle câblés.

> `outputs/skill-hybrid-memory.md`Il est également possible de modifier le système de calcul de la valeur de l'échantillon.

## Les exercices

1. Remplacez la similitude vectorielle de jouet par un modèle d'intégration réel (transformateurs de phrases, Ollama, intégrations OpenAI). Mesurer le rappel@10 sur une longue conversation synthétique.
   Le jeu est un jeu de société de jeu de société.
2. Ajoutez une requête temporelle: `search(query, as_of=timestamp)`- Retourner uniquement des dossiers valides à cette date ou avant.
   Le mot "quête" est traduit par "quête".`search(query, as_of=timestamp)`◊ Revenir seulement à ce temps ou à des enregistrements déjà valides ◊ Quel stockage a besoin de plus de travail ?
3. Implémenter un détecteur de conflit: si un fait entrant contredit un bord de graphique, invalidez l'ancien bord et enregistrez les deux.
   Le texte de l'article suivant est le plus ancien de tous les textes de la Bible.
4. Port le scorer de fusion pour inclure un `user_feedback`dimension (poignée en haut sur les enregistrements récupérés). Comment prévenir les jeux (l'agent ne renvoie que les enregistrements qu'il a déjà aimés)?
   Le groupe de travail est en train de se développer.`user_feedback`Comment empêcher le manipulation ?
5. Lire les documents du mémoire (`docs.mem0.ai`Prenez le jouet à la main .`mem0`Comparer la qualité de récupération sur les mêmes 20 requêtes de test.
   Le jeu est en train de se transformer en jeu.`mem0`客户端调用──比较相同 20 测试查询的检索质量──

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Hybrid memory | "Vector plus graph plus KV" / "向量加图加 KV" | Three stores written in parallel, fused on retrieval / 三个存储并行写入，检索时融合 |
| Fact extraction | "Memory ingestion" / "记忆摄取" | LLM step that breaks text into (entity, relation, fact) tuples / 将文本拆分为（实体、关系、事实）元组的 LLM 步骤 |
| Fusion scoring | "Relevance ranking" / "相关性排序" | Weighted sum of relevance, importance, recency / 相关性、重要性、时效性的加权和 |
| Scope | "Memory namespace" / "记忆命名空间" | user / session / agent — determines who sees what / 用户/会话/Agent——决定谁看到什么 |
| Mem0g | "Memory graph" / "记忆图" | Typed edges with temporal validity for relationship queries / 带时序有效性的类型化边，用于关系查询 |
| Temporal invalidation | "Soft delete" / "软删除" | Mark contradicted edges invalid; never delete / 标记矛盾边为无效；永不删除 |
| Embedding drift | "Retrieval rot" / "检索腐化" | Vector quality degrades as corpus grows; re-embed periodically / 向量质量随语料增长退化；定期重新嵌入 |

## Encore une lecture

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) le papier original
  Le texte original est écrit en français.
- [Mem0 docs](https://docs.mem0.ai/platform/overview) API de production, SDK, cloud géré
  Le texte de la loi est le texte de la loi.
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) le prédécesseur de contexte virtuel
  Le texte de la première partie de la série est le premier de la série.
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) la conception de trois niveaux
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la première de la lettre de la lettre de la première de la première de la lettre de la première de la lettre de la première de la première de la première de la première de la première de la lettre de la première de la première de la première de la première de la première de la première de la première de la première de la première de la première de la scène.
