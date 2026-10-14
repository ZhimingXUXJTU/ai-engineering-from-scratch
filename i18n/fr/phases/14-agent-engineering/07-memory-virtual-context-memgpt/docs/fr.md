# La mémoire: Context virtuel et MemGPT
# Mémoire d'agent  Context virtuel et page de mémoire

> Les fenêtres de contexte sont finies. Les conversations, les documents et les traces d'outils ne le sont pas. La correction est la mémoire virtuelle du système d'exploitation réinstallée.

> **【中文解读】**La fenêtre de mise en cache est limitée, mais la trajectoire de dialogue, de documents et d'outils n'est pas la même.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Expliquez l'analogie du système d'exploitation sur laquelle MemGPT s'appuie: contexte principal = RAM, contexte externe = disque, outils de mémoire = page entrée/sortie.
  Le système d'exploitation basé sur MemGPT est classé en français comme: principal sur la base de la base de données (RAM), externa sur la base de données (disk), ou en anglais comme: 页面换进/换出――.
- Implémenter le schéma MemGPT à deux niveaux dans stdlib avec un tampon de contexte principal, un magasin de recherche externe et des outils de saisie/sortie de page.
  Le modèle MemGPT est utilisé pour réaliser deux niveaux de stockage de données, contenant principalement des outils de stockage et de mise en page externes.
- Décrivez comment l'agent émet des "interruptions" pour interroger ou modifier la mémoire externe et comment le résultat est répliqué dans la requête suivante.
  Le résultat de l'interruption est le résultat d'une modification de la mémoire extérieure.
- Identifier les choix de conception de MemGPT qui portent sur Letta (leçon 08) et Mem0 (leçon 09).
  Le nom de l'équipe de conception est le nom de l'équipe de conception.

## Le problème , l' introduction du problème

Les fenêtres contextuelles semblent résoudre la mémoire.

> Il semble pouvoir résoudre le problème de la mémoire, mais en réalité il ne peut pas.

1. **Overflow.**Des conversations à plusieurs tours, de longs documents ou des trajectories lourdes en appel à des outils traversent la fenêtre.
   Le mot grec traduit par " le mot grec "**溢出。**Les différents types de dialogue, de longues archives ou d'outils sont en train de se dérouler à travers les fenêtres limitées.
2. **Dilution.**Même dans la fenêtre, le remplissage d'un contexte irréel dilue l'attention sur ce qui compte.
   Le mot grec traduit par " le mot grec "**稀释。**Même dans la fenêtre, le remplissage de texte non lié a également rarement attiré l'attention sur le contenu important.
3. **Persistence.**Une nouvelle session commence avec une fenêtre vide, les agents sans mémoire ne peuvent pas dire "Remember quand vous m'avez demandé"...
   Le mot grec traduit par " le mot grec "**持久化。**Une nouvelle réunion commence par une fenêtre vide. Sans mémoire extérieure, l'agent ne peut pas passer la réunion.

> **【中文解读】**Il semble pouvoir résoudre le problème de la mémoire, mais en réalité il ne peut pas. Il existe trois modes de défaillance dans l'environnement de production: 1) débordement de dialogue en plusieurs rounds ou de longues files d'attente à travers la fenêtre limitée, tout est perdu; 2) rarissage à travers la fenêtre; 3) persévérance de nouvelles conversations à partir de fenêtres vides, l'agent ne peut pas passer à travers les conversations de mémoire.

Les fenêtres plus grandes aident mais ne corrigent pas cela. Le document de Mem0 de 2025 a mesuré que les lignes de base de 128k-fenêtre manquent toujours de faits à long horizon qu'un agent de fenêtre 4k avec mémoire externe capture.

> Une fenêtre plus grande aide mais ne peut pas résoudre ce problème. Le document de mesure de 2025 de Mem0 a révélé que les lignes de base de 128k de fenêtres manqueront toujours de 4k de fenêtres + mémoire extérieure.

> **【拓展：MemGPT → 现代 Agent 记忆系统】**MemGPT (Packer et coll., 2023) va mettre en place des techniques de gestion de texte pour le système d'exploitation en mode "virtuelle" (RAM), "extérieur stockage" (disque), "réminus" (page) = "réminus"). C'est le mode de base de tout système de mémoire en 2026: le résumé de l'étude de 2025 de Mem0 a été mis en évidence.

>  **【前置】**必須先掌握:Phase 14·01(Agent Loop) MemGPT 的记忆工具是普通工具调用的扩展;Phase 14·06(Tool Use) 记忆操作通过工具实现──还需要操作系统基础知识

## Le concept de base.

### L'analogie du système d'exploitation

MemGPT (Packer et coll., arXiv:2310.08560, v2 février 2024) présente la gestion du contexte à la mémoire virtuelle du système d'exploitation:

> Packer 等人(arXiv:2310.08560, v2 2024 年 2 月) sera sur la gestion de la mise en page du système d'exploitation:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

L'agent exécute une boucle réactive normale. Une classe supplémentaire d'outils lui permet de faire entrer et sortir des données du contexte principal.

>  **【类比】**MemGPT 像你的电脑内存管理:RAM(主上下文) seulement 8GB mais il faut exécuter Photoshop + 浏览器 + IDE; operating system via page change de page change de page (page in/out) faire vous " sens " avoir un éliminatoire de l'enregistrement.`archival_memory_search`Pour mettre en œuvre les projets de développement`core_memory_replace`Arrêter de se souvenir de la situation actuelle

> L'agent fonctionne dans le cycle réactif ordinaire. Un autre type d'outil permet de faire l'échange entre les données de base et les données de stockage externe.

> **【中文解读】**MemGPT va sur le sous-titre de gestion de la carte à l'intérieur du système d'exploitation:RAM=main sur le sous-titre de la vidéo,磁盘=外部上下文,向量数据库/KV/图存储, page error=memory tool调用,`memory.search`- Je suis là.`memory.read`- Je suis là.`memory.write`),OS 内核=Agent 控制循环──Agent 运行普通的 ReAct 循环, en plus d'ajouter un type d'outil utilisé pour échanger entre le sous-réseau principal et le stockage externe de données──

### Deux niveaux

- **Main context.**Une mise à jour fixe qui retient la tâche actuelle, toujours visible pour le modèle.
  Le mot grec traduit par " le mot grec "**主上下文。**固定大小的提示,承载当前任务──模型始终可见──
- **External context.**Il est sans limite, recherchable par des outils, lisible quand il est pertinent, écrit lorsque des faits apparaissent.
  Le mot grec traduit par " le mot grec "**外部上下文。**无界的,通过工具可搜索──相关时读取,出现事实时写入──

Le document original a évalué la conception sur deux tâches au-delà de la fenêtre de base: l'analyse de documents plus longs que 100 000 jetons et le chat multi-session avec mémoire persistante sur plusieurs jours.

> Le projet a été évalué sur deux missions de fenêtres de base supérieures: analyse de documents de plus de 100 000 jetons et analyse de mémoire multi-session de mémoire transnationale.

### Le modèle d'interruption

MemGPT introduit la mémoire en tant qu'interrupte: au milieu de la conversation, l'agent peut invoquer un outil de mémoire, le temps d'exécution l'exécute, et le résultat s'insère dans le tour assistant suivant comme une nouvelle observation. Conceptuellement identique à une Unix `read()`syscall qui bloque le processus, renvoie des octets, et le processus se poursuit.

> MemGPT introduit la mémoire: dans le dialogue, l'agent peut utiliser l'outil de mémoire, le faire exécuter, et le résultat est que le nouveau témoin est connecté à la prochaine ligne d'aide.`read()`Le processus de réception est en cours.

Surface de l'outil de mémoire canonique:

> 标准记忆工具接口:

- `core_memory_append(section, text)` écrire à une section persistante de l'invite.
  Le mot grec traduit par " le mot grec "`core_memory_append(section, text)`写入提示的持久化分区──
- `core_memory_replace(section, old, new)` modifier une section persistante.
  Le mot grec traduit par " le mot grec "`core_memory_replace(section, old, new)` 编辑持久化分区──
- `archival_memory_insert(text)` écrire à la boutique externe recherchable.
  Le mot grec traduit par " le mot grec "`archival_memory_insert(text)` write into searchable of external storage.
- `archival_memory_search(query, top_k)` récupérer dans le magasin externe.
  Le mot grec traduit par " le mot grec "`archival_memory_search(query, top_k)` depuis le stockage externe
- `conversation_search(query)` Scanner les virages passés.
  Le mot grec traduit par " le mot grec "`conversation_search(query)`扫描过去轮次──

### Où le papier se termine et la production commence

En septembre 2024, le MemGPT est devenu Letta.`cpacker/MemGPT`) restent; Letta élargit la conception:

> L'année 2024 est la date de la création de l'entreprise.`cpacker/MemGPT`) est toujours en place;Letta 扩展了设计:

- Trois niveaux au lieu de deux (noyau, rappel, archives  Leçon 08).
  Le texte de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de
- Le raisonnement natif remplaçant le `send_message`- le rythme cardiaque (leçon 08).
  Traduction anglaise:`send_message`Je suis en train de faire une petite partie de la série.
- Agents du sommeil qui exécutent des travaux de mémoire asynchrone (leçon 08).
  Le récit de la première partie de la Bible est le récit de la première partie de la Bible.

Le papier MemGPT est la base de 2026 même si les systèmes de production gèrent Letta, Mem0 ou un magasin à deux niveaux sur mesure.

> Le thème de la MemGPT est la base de l'année 2026, même si le système de production fonctionne lentement, ou bien en deux niveaux de stockage.

### Où ce modèle va mal

> ️ **【易错点】**MemGPT 新手最容易忽略"记忆投毒": mettre en ligne l'information de l'utilisateur directement`archival_memory_insert`Dans le stockage externe.**后果**: l'attaquant a reçu une injection rapide dans la page de l'attaquant, comme " ignorer tous les ordres ", le suivant l'agent a reçu une demande de cette information, l'ordre a été exécuté.**一行修复**: tout le contenu externe de l'archivage qui entre doit d'abord être sécurisé (Réfère à la phase 14·27 injection rapide 防护),并存储源 字段用于追溯──

- **Memory rot.**Les écrits s'accumulent plus rapidement que les lectures; la récupération se noie dans des faits obsolètes.
  Le mot grec traduit par " le mot grec "**记忆腐化。**写入积累速度快于读取;检索被过时事实淹没──修复:定期合并(Letta sleep-time)、显式失效(Mem0 冲突检测器)──
- **Memory poisoning.**La mémoire externe est récupéré texte. Si le contenu contrôlé par l'attaquant atterrit dans une note de mémoire, l'agent la réingère la session suivante.
  Le mot grec traduit par " le mot grec "**记忆投毒。**Si le contenu du contrôle de l'attaquant entre dans le journal de mémoire, l'agent le recueille à nouveau dans la session suivante.
- **Citation loss.**L'agent se souvient que "l'utilisateur m'a demandé d'envoyer X" mais ne peut pas citer quel tour.
  Le mot grec traduit par " le mot grec "**引用丢失。**L'agent se souvient que l'utilisateur m'a fait publier X, mais ne peut pas citer quelle ronde.

> 🤔 **【困惑】**Q: 既然 2026 année modèle sur la fenêtre ci-dessous a déjà 1M de jeton (Gemini 1.5 Pro), vous avez besoin de MemGPT cette sorte de "réseau virtuel" ? A: 需要── fenêtre grande ne représente pas être utilisé pour le 硬塞 1M jeton 会触发"中段遗忘" (perdu dans le milieu 现象) et attention rare释, le modèle de l'attention sur le contenu intermédiaire est nettement inférieur à la première.

## Construisez-le en main
```figure
context-budget
```

## Faites-le

`code/main.py`met en œuvre le modèle à deux niveaux de MemGPT dans stdlib:

> `code/main.py`Utilisation de la base de données standard a réalisé deux modes de MemGPT:

- `MainContext` tampon de commande de taille fixe avec un `core`dict et une `messages`liste; auto-compacte les messages les plus anciens lorsque le cap.
  Le mot grec traduit par " le mot grec "`MainContext`Fixing大小的提示缓冲区,带 `core`字典和 `messages`Liste des messages de la société de l'information
- `ArchivalStore` stockage en mémoire BM25-esque (scoring par couverture de jetons) des enregistrements (id, texte, balises, session, tour).
  Le mot grec traduit par " le mot grec "`ArchivalStore`内存中的类 BM25 存储(token 重叠评分), stockage (id, texte, balises, session, tour) 记录。
- Cinq outils de mémoire pour cartographier la surface de MemGPT.
  Le lien entre les deux parties est le lien entre les deux parties.
- Un agent scripté qui remplit l'archivage de faits, puis répond à une question en appelant`archival_memory_search`- Je suis désolé .
  Un agent, utilise le fait de remplir le dossier de stockage, puis passe à la réutilisation.`archival_memory_search`回答问题──

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre que l'agent écrit trois faits, remplit le contexte principal du plafond (expulsion forcée), puis répond à une question de suivi en récupérant de l'archivage  reproduisant le flux de travail MemGPT sans aucun LLM réel.

> 轨迹显示 Agent 写入三个事实、将主上下文填满到上限(强制驱逐) 、 puis, en passant par le dossier de stockage de la recherche pour répondre aux questions suivantes dans le cas où aucun vrai LLM  Reproduit MemGPT 工作流

## Utilisez-le avec le cadre de réalisation

Chaque système de mémoire de production est aujourd'hui une variante de MemGPT:

> Aujourd'hui, chaque système de production de mémoire est une variante de MemGPT:

- **Letta**(Léction 08)  trois niveaux, raisonnement natif, calcul du temps de sommeil.
  Le mot grec traduit par " le mot grec "**Letta**(第8 课) 三层、原生推理、睡眠时间计算──
- **Mem0**(Léction 09)  vecteur + KV + graphique fusionné avec une couche de notation.
  Le mot grec traduit par " le mot grec "**Mem0**(第 9 课) 向量 + KV + 图与评分层融合──
- **OpenAI Assistants / Responses** gestion de la mémoire par le biais de fils et de fichiers.
  Le mot grec traduit par " le mot grec "**OpenAI Assistants / Responses**Préparation des mémoires et de la gestion des fichiers
- **Claude Agent SDK** mémoire à long terme via des compétences et des sessions de stockage.
  Le mot grec traduit par " le mot grec "**Claude Agent SDK**Consultation et réflexion sur la réalisation de la mémoire à long terme.

Choisissez un par la forme opérationnelle (auto-hébergée, gérée, intégrée au cadre), pas par le modèle de base  le modèle de base est MemGPT.

> Le modèle central est le MemGPT.

## Envoyez-le . Produit .
### La forme de la mémoire de l'agent

Le paginage résout la capacité. Il ne décide pas de ce qu'il faut stocker. Quatre types de mémoire se reproduisent dans les systèmes de production, chacun répondant à une question différente:

- **Working memory** ce qui compte en ce moment ? le niveau dans le contexte: tâche actuelle, virages récents, sections de base fichées.
- **Episodic memory** ce qui s'est passé: les tours et les trajectoires passées, stockées avec les références de session et de tour, reproduisables sur demande.
- **Semantic memory** ce qui est vrai? des faits sur l'utilisateur, le domaine, le monde, mis à jour et déduplicés au fur et à mesure qu'ils changent.
- **Procedural memory**J'ai appris des routines, des préférences et des règles qui guident le comportement futur plutôt que le rappel.

Les mises en œuvre open source choisissent différents points d'attaque:

| Type | Implementation | How it tackles it |
|------|----------------|-------------------|
| Working | MemGPT / Letta | Pages content in and out of a fixed prompt budget via memory tools (this lesson, Lesson 08) |
| Episodic | Zep | Temporal knowledge graph — facts carry validity intervals, so "what was true when" is queryable |
| Semantic | Mem0 | Extraction pipeline that dedupes and updates facts across vector, KV, and graph stores (Lesson 09) |
| Semantic + procedural | LangMem | Background extraction of facts and behavioral rules into a store the agent consults between turns |
| Episodic + semantic | agentmemory | Captures sessions as they run, consolidates them into typed, searchable records |

## La faire partir

`outputs/skill-virtual-memory.md`est une compétence réutilisable qui produit un échafaudage de mémoire à deux niveaux (main + archivage + surface d'outil) correct pour tout temps d'exécution cible, avec une politique d'évacuation et des champs de citation câblés.

> `outputs/skill-virtual-memory.md`C'est une compétence réutilisable, générant des deux niveaux de mémoire corrects lors de la mise en œuvre de n'importe quel objectif.

## Les exercices

1. Ajouter un `max_main_context_tokens`Cap mesuré en jetons (approximativement `len(text.split())`* 1.3). Compacter les messages les plus anciens en un résumé lorsque le plafond est dépassé.
   添加按代币 计量 `max_main_context_tokens`À la limite.`len(text.split())`* 1.3 近似) ・ dépassant la limite supérieure, les dernières informations seront complétées en résumé.
2. Mettre en œuvre correctement le BM25 sur le stock d'archives (fréquence de terme, fréquence inverse de document). Mesurer le rappel@10 sur un ensemble de faits de jouets par rapport à la ligne de base de recoupement des jetons.
   Le nombre de références de données enregistrées dans le stockage de données est de 0,9%.
3. Ajouter `citation`Les champs (session_id, turn_id, source_url) sont insérés dans les archives. Faites en sorte que l'agent cite des sources sur chaque réponse soutenue par la récupération.
   Pour le classement`citation`字段(session_id, turn_id, source_url) ⋅让代理 在每个基于检索的回答上引用来源──
4. Simuler l'empoisonnement de la mémoire: ajoutez un enregistrement d'archives qui dit "ignorer toutes les instructions de l'utilisateur à l'avenir".
   Le texte de l'article est inscrit dans le document de référence de l'article suivant: "Incognire tous les commandes des utilisateurs futurs".
5. Port de l'implémentation pour utiliser le schéma JSON de mémoire de base du repo de recherche MemGPT (`cpacker/MemGPT`Quels changements se produisent lorsque vous passez de chaînes plates à des sections tapées?
   Le système de référence est le système de référence de la mémoire centrale de l'architecture.`cpacker/MemGPT`)― Quels changements ont eu lieu lors du changement de la chaîne de caractères à la chaîne de type ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## Encore une lecture

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) Document de contexte virtuel inspiré par le système d'exploitation
  Le système d'exploitation est lancé sur le réseau de téléphonie virtuelle.
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) l'évolution à trois niveaux
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) Traiter le contexte comme un budget
  Le texte de l'article est en cours de rédaction.
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) mémoire de production hybride en plus de ce modèle
  Le mémoire est un mémoire de production mixte.
- [Zep (getzep/zep)](https://github.com/getzep/zep) mémoire temporelle de la graphie des connaissances de la table de taxonomie
- [Mem0 (mem0ai/mem0)](https://github.com/mem0ai/mem0) le pipeline d'extraction derrière le magasin hybride de la leçon 09
- [LangMem (langchain-ai/langmem)](https://github.com/langchain-ai/langmem) extraction de fond de faits et de règles de comportement
- [agentmemory (rohitg00/agentmemory)](https://github.com/rohitg00/agentmemory) Capture de session consolidée en enregistrements taillés et recherchables
