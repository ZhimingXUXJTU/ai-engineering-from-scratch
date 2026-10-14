# Les blocs de mémoire et le calcul du temps de sommeil (Letta)
# Les blocs de mémoire et le calcul du temps de sommeil

> Les blocs de mémoire fonctionnels discrets que le modèle peut modifier directement, et un agent de sommeil qui consolide la mémoire de manière asynchrone pendant que l'agent principal est inactif.

> **【中文解读】**Le développement de MemGPT en 2024 devient Letta. En 2026, deux idées sont ajoutées: le modèle peut être directement édité de blocs de mémoire de fonctionnalités dispersées, ainsi que l'agent de sommeil du mémoire associé à l'agent principal.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Nombre des trois niveaux de mémoire utilisés par Letta (core, rappel, archivage) et le rôle de chacun.
  Le mot "récollection" est utilisé pour désigner les trois niveaux de mémoire utilisés par Letta.
- Expliquez le modèle de blocage de mémoire: bloc humain, bloc de personnalité et bloc définis par l'utilisateur comme objets de première classe.
  Le modèle de bloc de mémoire est le bloc humain, le bloc de la personne et l'utilisateur se définissent eux-mêmes comme un objet de type.
- Décrivez ce qu'est le calcul du temps de sommeil, pourquoi il est hors de la voie critique et pourquoi il peut exécuter un modèle plus fort que l'agent principal.
  Traduction chinoise: description de l'Huyleep calcul est quoi, pourquoi il est en dehors de la voie clé, pourquoi il peut fonctionner avec un modèle plus fort que l'agent principal.
- Implémenter une boucle scriptée à deux agents où un agent principal sert les réponses et un agent de sommeil consolide les blocs entre les tours.
  En français, l'agent principal fournit une réponse, l'agent pendant son sommeil, le cycle de l'action.

## Le problème , l' introduction du problème

MemGPT (leçon 07) a résolu le flux de contrôle de la mémoire virtuelle.

> MemGPT (septième cours) a résolu trois problèmes de production:

1. **Latency.**Chaque opération de mémoire est sur le chemin critique. si l'agent doit tailler, résumer ou réconcilier pendant que l'utilisateur attend, la latence de la queue explose.
   Le mot grec traduit par " le mot grec "**延迟。**Chaque opération de mémoire est sur un chemin clé. Si l'agent doit modifier un résumé ou un coordonné pendant l'attente de l'utilisateur, le bout du temps sera retardé.
2. **Memory rot.**Les écrits s'accumulent, les faits contradictoires restent, la récupération se noie dans le contenu obsolète.
   Le mot grec traduit par " le mot grec "**记忆腐化。**写入积累―― contradiction facts保留――检索被过时内容淹没――
3. **Structure loss.**Un magasin d'archives plat ne peut pas exprimer "le bloc humain est toujours dans le prompt; le bloc Persona est toujours dans le prompt; le bloc Tasks swaps par session".
   Le mot grec traduit par " le mot grec "**结构丢失。**平的归档存储不能表达"Human 块始终在提示中;Persona 块始终在提示中;Task 块按会话交换――"

Letta (letta.com) est le nom de la plateforme le projet MemGPT original adopté en 2024  le modèle du papier garde le nom MemGPT  et la réécriture 2026 Letta V1 est une étape ultérieure, séparée.

> Letta (en anglais: Letta) est une réécriture de 2026 par le groupe Letta.com.

> **【中文解读】**Le calcul du temps de sommeil est une méthode de mémorisation de la mémoire. Il est utilisé pour contrôler la proportion de toutes les informations dans la fenêtre de la mémoire.

> **【拓展：Letta 的演进】**Letta (ancienne MemGPT) introduit dans les développements de 2024-2025 deux concepts clés du calcul du bloc de mémoire et du bloc de sommeil. Le bloc de mémoire sera divisé en deux sections fixes, évitant la confusion des informations.

>  **【前置】**必須先通過Fase 14·07 (MemGPT) 本節是它的直接延續──如果您不理解 MemGPT's"主上下文 vs 外部上下文"二层模型,那么 Letta's三层(core/recall/archival) 扩展会把你搞──

## Le concept de base.

### Trois niveaux

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

Le cœur est le cœur MemGPT. rappelez-vous est le tampon de conversation avec sa queue évacuée. archivage est le magasin externe. la fraction nettoie la surcharge à deux niveaux de MemGPT.

> Le cœur est le cœur du MemGPT. Le souvenir est le dialogue缓冲区带驱逐尾部. L'archivage est le stockage externe.

### Blocs de mémoire

Un bloc est une section taillée, persistante et éditable du niveau principal.

> Le bloc est la classification de la couche centrale, la persévérance, la rédaction des zones.

- **Human block** faits sur l'utilisateur (nom, rôle, préférences, objectifs).
  Le mot grec traduit par " le mot grec "**Human 块** À propos des faits concernant l'utilisateur (姓名,角色,偏好,目标)
- **Persona block** l'identité, le ton, les contraintes de l'agent.
  Le mot grec traduit par " le mot grec "**Persona 块**Agent du concept de soi (身份、语气、约束)

Letta généralise à des blocs définis par l'utilisateur: a `Task`bloc pour l'objectif actuel, un `Project`bloc pour les faits de base de code, un `Safety`Chaque bloc a une limite de débit.`id`- Je suis là .`label`- Je suis là .`value`- Je suis là .`limit`(capitulatif de caractères), `description`(pour que le modèle sache quand le modifier).

> Letta 泛化为任意用户定义块:用于当前目标的 `Task`块、用于代码库事实 `Project`Pour les blocs de rouleaux`Safety`Chaque pièce a un`id`- Je suis là.`label`- Je suis là.`value`- Je suis là.`limit`(symbole sur limite)`description`(Laissez le modèle savoir comment l'éditer)

Les blocs sont éditables via la surface de l'outil:

> 块通过工具接口可编辑:

- `block_append(label, text)`
  Le mot grec traduit par " le mot grec "`block_append(label, text)`向块追加文本──
- `block_replace(label, old, new)`
  Le mot grec traduit par " le mot grec "`block_replace(label, old, new)`替换块中的文本──
- `block_read(label)`
  Le mot grec traduit par " le mot grec "`block_read(label)`读取块内容──
- `block_summarize(label)` condenser un bloc qui est proche de sa limite.
  Le mot grec traduit par " le mot grec "`block_summarize(label)` Compression proche de la limite supérieure de blocs

### Compteur du sommeil

L'ajout Letta 2025: exécuter un deuxième agent en arrière-plan, hors du chemin critique.`learned_context`En effet, les données de l'archivage sont des données de base, et elles sont partagées en blocs partagés, et les archives sont consolidées ou invalidées.

> 2025 Letta: dans le second agent, non sur un chemin clé.`learned_context`写入共享块,并合并或使归档记录失效──

Propriétés qui tombent:

> 随之产生的特性:

- **No latency cost.**Les réponses primaires ne doivent pas attendre des opérations de mémoire.
  Le mot grec traduit par " le mot grec "**无延迟成本。**Il ne faut pas attendre l'opération de mémoire.
- **Stronger model allowed.**L'agent de sommeil peut être un modèle plus cher et plus lent car il n'est pas limité par la latence.
  Le mot grec traduit par " le mot grec "**允许更强的模型。**L'agent de sommeil peut être un modèle plus cher, plus lent, car il n'est pas retardé.
- **Natural consolidation window.**Déduire, résumer, annuler les faits contradictoires lorsque l'utilisateur n'attend pas.
  Le mot grec traduit par " le mot grec "**天然的合并窗口。**Dans le cas d'un utilisateur qui n'attend pas, il faut réessayer le résumé et faire échouer les contradictions.

La forme correspond à la façon dont les humains travaillent: vous faites la tâche, vous dormez dessus, la mémoire à long terme se calme du jour au lendemain.

>  **【类比】**Compteur de temps de sommeil 像夜晚的清洁工:白天你(主代理) occupé à répondre aux clients, aux bureaux(主上下文)堆满今天的会议记录、文件、咖啡杯;晚晚清洁工(睡眠时间代理) 进来擦桌子、归档文件、把"明天要跟进的事"贴到便利贴上(写入人/任务块) ・・・第二天你上班,看整洁待机面和清晰的办公清单──**关键**Le nettoyage peut être lent, cher, car le client n'est pas attendu.

> Cette forme correspond à la façon de travailler humaine: tu fais des tâches, tu dors, tu fais des souvenirs de longue durée pendant la nuit.

### Letta V1 et le raisonnement natif
### Résumé du sujet

Letta V1 (`letta_v1_agent`, 2026) déprécie `send_message`/ battements de cœur et en ligne `Thought:`Les réponses API (OpenAI) et les messages API avec la pensée étendue (Anthropic) émettent le raisonnement sur un canal séparé, passé à travers des tours (crypté entre les fournisseurs en production).

> Letta V1`letta_v1_agent`,2026) a été abandonné.`send_message`/ cœur et intérieur `Thought:`Les messages sont des messages qui sont ouverts à des utilisateurs de logiciels de référence et qui sont utilisés pour les messages de référence.

### Où ce modèle va mal

> ️ **【易错点】**"静默漂移" est le bug le plus dangereux de Letta 部署: le agent du sommeil a modifié le personnage à l'arrière du jeu (par exemple, il a toujours utilisé le chinois pour le répéter), mais le principal agent ne sait pas.**后果**: l'utilisateur a découvert que l'agent a changé de comportement mais il ne trouve pas de raison parce que le journal de dialogue ne registre que les sorties de l'agent principal**一行修复**: chaque fois que vous dormez 写入后版本化块内容, et en suivant le commandement du principal agent 里注入"自上次以来块变化:..."的不同提示──

- **Block bloat.**Il n' y a pas de fin .`block_append`- Il faut mettre un résumé avant l'écriture qui dépasse le capot.
  Le mot grec traduit par " le mot grec "**块膨胀。**Il n' y a pas de limite .`block_append` Rapidement atteindre la limite supérieure                                                                                                                                                                                                                                                          
- **Silent drift.**L'agent du sommeil réécrit un bloc et l'agent principal ne le remarque jamais.
  Le mot grec traduit par " le mot grec "**静默漂移。**L'agent de sommeil réécrit des blocs mais l'agent principal ne s'est pas rendu compte.
- **Poisoned consolidation.**L'agent du sommeil traite le contenu accessible à l'attaquant dans le noyau.
  Le mot grec traduit par " le mot grec "**投毒合并。**L'agent de sommeil va traiter le contenu de l'attaquant dans le cœur.

> 🤔 **【困惑】**Q: L'agent du sommeil utilise un modèle plus fort et ne coûte pas plus cher ? Pourquoi est-ce que l'argent est économisé plutôt que brûlé ?**避开了关键路径的高价** L'agent principal  doit utiliser le streaming + haute priorité, le prix unique est de 2-3 fois le lot.

## Construisez-le en main
```figure
memory-blocks
```

## Faites-le

`code/main.py`les implémentations:

> `code/main.py`实现:

- `Block` id, étiquette, valeur, limite, description.
  Le mot grec traduit par " le mot grec "`Block`id、étiquette、value、limite、description。
- `BlockStore` CRUD + `near_limit(label)`- Je suis un assistant.
  Le mot grec traduit par " le mot grec "`BlockStore`CRUD + `near_limit(label)`- Le système de sécurité
- Deux agents avec scénario`PrimaryAgent`Il sert un tour, `SleepTimeAgent`se consolide entre les tours.
  Deux scénarios d'agent`PrimaryAgent`- Je vous en prie.`SleepTimeAgent`Dans la même période.
- Une trace qui montre une conversation en trois tours avec Block écrit, plus un passe-temps de sommeil qui résume un bloc et invalide un fait obsolète.
  Traduction anglaise: montrer trois rounds de dialogue avec des blocs d'écriture, plus des blocs de compréhension et faire défaillir le temps de la réalité de la traite de l'humour.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La transcription montre la fraction: les virages primaires sont rapides et produisent des écritures brutes; le passage du sommeil est compact et nettoie.

> Les enregistrements de transitions montrent que le travail principal: la production de la rédaction initiale; le traitement de la compression et du nettoyage de l'intervalle.

## Utilisez-le avec le cadre de réalisation

- **Letta**(letta.com) pour la mise en œuvre de référence.
  Le mot grec traduit par " le mot grec "**Letta**(letta.com) Pour réaliser.
- **Claude Agent SDK skills**En tant que connaissance en forme de bloc  une compétence est un bloc d'instructions nommé, versionné et récupérable que l'agent charge à la demande.
  Le mot grec traduit par " le mot grec "**Claude Agent SDK skills**comme bloc de connaissances compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence compétence 
- **Custom builds**Pour les équipes qui veulent contrôler le backend de stockage, utilisez le contrat Letta API pour pouvoir migrer plus tard.
  Le mot grec traduit par " le mot grec "**自定义构建** Adaptation à la volonté de contrôler le stockage de l'arrière-plan du groupe.

## Envoyez-le . Produit .

`outputs/skill-memory-blocks.md`génère un système de bloc en forme de Letta avec des crochets de sommeil pour tout temps d'exécution, y compris les règles de sécurité et le câblage de citation.

> `outputs/skill-memory-blocks.md`Pour toute opération, générer des blocs de Letta, avec des règles de sécurité et des liens de référence.

## Les exercices

1. Ajouter un `block_summarize`outil qui remplace la valeur de bloc par un résumé généré par modèle lorsque `near_limit`Quel seuil de déclenchement minimise à la fois les appels de résumé et le débordement de bloc ?
   Le mot " accroche " est traduit par " accroche "`block_summarize`工具, dans `near_limit`返回 true 时使用模型生成的摘要替换块值──哪个触发值最小化摘要调用和块溢出?
2. La déduction du temps de sommeil sur l'archivage: deux enregistrements dont le texte a une superposition symbolique de plus de 90% s'effondrent à un.
   En français, le "répertoire" est un terme qui signifie "répertoire" ou "répertoire" qui signifie "répertoire" ou "répertoire" qui signifie "répertoire" ou "répertoire".
3. Blocs de version. sur chaque enregistrement d'écriture la valeur ancienne et une différence.`block_history(label)`pour que les opérateurs puissent déboguer "pourquoi l'agent a oublié X".
   Traduction anglaise: éditionalisation de blocs.`block_history(label)`Pourquoi l'agent a-t-il oublié X ?
4. Traitez les agents de sommeil comme des écrivains peu fiables.
   Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français
5. Port l'exemple pour utiliser l'API Letta (`letta_v1_agent`Quels changements se produisent dans le schéma des blocs, et comment le raisonnement natif modifie-t-il la forme des traces?
   Le modèle de l'application Letta est utilisé pour le port de l'application Letta.`letta_v1_agent`• • Quels sont les changements dans le mode de vie ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## Encore une lecture

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) le modèle de bloc
  Le mot grec traduit par "l'écriture" est traduit par "l'écriture".
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute) consolidation asynchrone
  Le mot grec traduit par "l'écriture" est traduit par "l'écriture".
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent) Réécriture de raisonnement natif
  Letta 重建 Agent cycle blog原生推理重写──
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) l'origine
  Le texte de l'article est écrit en français.
