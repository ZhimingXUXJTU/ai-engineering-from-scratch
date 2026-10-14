# Bibliothèques de compétences et apprentissage tout au long de la vie (Voyager)

> Voyager (Wang et al., TMLR 2024) traite le code exécutable comme une compétence. Les compétences sont nommées, récupérables, comptables et affinées par les commentaires environnementaux.

> **【中文解读】**Voyager va pouvoir exécuter des codes en tant que compétences. Les compétences sont nommées, récupérables, assemblées et passées par l'environnement contre l'élimination.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Nommez les trois composants de Voyager  programme d'études automatique, bibliothèque de compétences, incitation itérative  et le rôle de chacun.
  Les trois composants du Voyager sont: cours automatiques, compétences, suggestions et rôles.
- Expliquez pourquoi Voyager fait le code de l'espace d'action, pas les commandes primitives.
  Expliquer pourquoi Voyager va mettre en place un code plutôt qu'une commande originale.
- Implémenter une bibliothèque de compétences stdlib avec enregistrement, récupération, composition et raffinement basé sur l'échec.
  Traduction anglaise: avec la bibliothèque standard pour réaliser avec l'enregistrement, le contrôle, la mise en œuvre et le défaut de la bibliothèque des compétences de l'éducation et de la formation.
- Mettez le modèle de Voyager sur les compétences du SDK de l'agent Claude 2026 et l'écosystème du kit de compétences.
  Le modèle Voyager se déroulera jusqu'en 2026 avec les compétences et les compétences de Claude Agent SDK.

## Le problème , l' introduction du problème

Les agents qui reconstruisent chaque capacité à partir de zéro à chaque séance font trois choses mal:

> Chaque réunion commence par un agent capable de reconstruire tout. Il va faire trois erreurs:

1. **Waste tokens.**Chaque tâche réitère le même raisonnement.
   Le mot grec traduit par " le mot grec "**浪费 token。**Chaque mission est de nouveau à l'origine de la même proposition.
2. **Lose progress.**Une correction apprise en session A ne passe pas à la session B.
   Le mot grec traduit par " le mot grec "**丢失进展。**En cours de formation, les corrections ne seront pas transférées à la formation B.
3. **Fail on long-horizon composition.**Les tâches complexes nécessitent des hiérarchies de capacités; les instructions à un seul coup ne peuvent pas les exprimer.
   Le mot grec traduit par " le mot grec "**在长程组合上失败。**Les tâches complexes nécessitent des niveaux de capacité; les simples suggestions ne peuvent pas les exprimer.

> **【中文解读】**技能库(Skill Libraries) Originaire de Voyager (Wang et coll., 2023)  Un agent qui explore et apprend de lui-même dans Minecraft。 L'innovation centrale de Voyager est la découverte et le stockage automatiques de compétences: l'agent trouve une séquence d'opération efficace lors de l'exécution d'une tâche, en le codifiant en fonction de compétences réutilisables dans la base de compétences。

Voyager répond: traiter chaque capacité réutilisable comme un morceau de code nommé stocké dans une bibliothèque, récupérable par similitude, compostable avec d'autres compétences, et affiné par feedback d'exécution.

> Voyager's réponse: considérer chaque capacité réutilisable comme un bloc de code nommé stocké dans la base de données, par la recherche de similitude, par la combinaison avec d'autres compétences, et par la mise en œuvre de l'analyse de l'analyse.

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用】**Les cours et les compétences du codex sont des variantes de cette idée qui vont permettre à un mode d'exploitation efficace de se transformer en compétences réutilisables. Voyager utilise 160 compétences de découverte automatique dans Minecraft pour effectuer les tâches qui nécessitent des joueurs humains quelques heures pour les réaliser.

>  **【前置】**需要先掌握:Phase 14·05(Self-Refine/CRITIC) Voyager's "代提示机制"本质是 Self-Refine + 环境反;Phase 14·07(MemGPT) 技能库的检索机制类似于档案记忆的语义搜索──还需要理解"代码即行动"的概念,区别于"文本即行动"──

## Le concept de base.

### Trois composants

Voyager (arXiv:2305.16291) structure un agent autour de:

> Voyager ((arXiv:2305.16291) autour des trois composants suivants:

1. **Automatic curriculum.**Un proposant motivé par la curiosité choisit la prochaine tâche en fonction de l'état actuel de l'agent et de son environnement.
   Le mot grec traduit par " le mot grec "**自动课程。**Bien-aimé propulseur de suggestion selon l'agent actuel compétences et l'état de l'environnement choisir la prochaine tâche.
2. **Skill library.**Chaque compétence est un code exécutable. De nouvelles compétences sont ajoutées lorsque une tâche réussit.
   Le mot grec traduit par " le mot grec "**技能库。**Chaque compétence est exécutable. Une nouvelle compétence est ajoutée à la réussite de la tâche.
3. **Iterative prompting mechanism.**En cas d'échec, l'agent reçoit des erreurs d'exécution, des commentaires sur l'environnement et des sorties d'auto-vérification, puis affiner la compétence.
   Le mot grec traduit par " le mot grec "**迭代提示机制。**失败时,Agent 接收执行错误、环境反和自我验证输出, puis élève les compétences。

L'évaluation de Minecraft (Wang et coll., 2024): 3,3 fois plus d'articles uniques, 8,5 fois plus rapides outils en pierre, 6,4 fois plus rapides outils en fer, 2,3 fois plus long travers de carte par rapport aux lignes de base.

> Minecraft 评估(Wang 等人,2024):3.3 倍更多独特物品、8.5 倍更快石制工具、6.4 倍更快铁制工具、2.3 倍更长地图遍历对比基线──数字是Minecraft 特定的,但模式可迁移──

### Espace d'action = code

La plupart des agents émettent des commandes primitives.

> La plupart des agents émettent des commandes originales.

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

Composé de sous-compétences, stocké sur la description et l'intégration, récupéré comme un programme, pas une requête.

> En tant que processus, il est préférable de les décrire et de les intégrer dans le stockage de clés.

C'est la compétence du SDK 2026 Claude Agent: une pièce de code nommée et récupérable plus des instructions que l'agent charge à la demande.

> C'est le 2026 Claude Agent SDK: un code nommé, récupérable, plus un code d'agent chargé en fonction des besoins.

>  **【类比】**技能库像程序员's "code fragment library" ou snippets de l'IDE: vous n'avez pas besoin de chaque fois de réécrire Python`read_file`函数,调用已有的就行;; Voyager's insight is to let Agent also do it"invented" a une fois"挖铁矿" code, stockée dans la bibliothèque, suivante encore à fouiller dans le chemin de fer sur le contrôle direct调用;;**关键**: compétences est**代码**Il n'y a pas de**提示词**代码可以被环境执行、获得明确反,提示词不行──

### Récupération des compétences

Une nouvelle tâche: faire une hache à diamant.

> Il est un agent de la production de diamants.

1. Intégre la description de la tâche.
   Le nom de l'équipe de formation est le nom de l'équipe de formation.
2. Demande à la bibliothèque des compétences pour des compétences similaires.
   Le plus souvent, les compétences sont les mêmes.
3. Retour `craftIronPickaxe`- Je suis là .`mineDiamond`- Je suis là .`placeCraftingTable`et ainsi de suite.
   Le mot " le " signifie " le " le " .`craftIronPickaxe`- Je suis là.`mineDiamond`- Je suis là.`placeCraftingTable`Ça va.
4. Compose la nouvelle compétence à partir de primitives récupérées + nouvelle logique.
   Le texte original est traduit en français par "from the original language" et "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language" en français par "from the original language").

Il s'agit de la mise en œuvre des ressources MCP (phase 13) et des compétences SDK d'agent: récupération sur une surface de connaissances/code, axée sur la tâche actuelle.

> C'est le MCP 资源(Phase 13) et les compétences SDK d'Agent 实现的模式:在知识/代码表面上检索,限于当前任务──

### Réfinition itérative

La boucle de rétroaction du Voyager:

> Le cycle de Voyager:

1. L'agent écrit une compétence.
   Le nom de l'agent est traduit en français par " agent " ou " agent ".
2. La compétence est contre l'environnement.
   Le langage est le langage de la langue.
3. Un des trois signaux revient:`success`- Je suis là .`error`(avec des traces de pile), `self-verification failure`- Je suis désolé .
   Le mot "réponse" est traduit par "réponse":`success`- Je suis là.`error`Je suis en train de vous suivre.`self-verification failure`Il y a une autre.
4. L'agent réécrit l'habileté en utilisant le signal comme contexte.
   Le rédacteur en chef utilise le langage de l'agent comme un moyen de réécrire.
5. Va jusqu'à ce que tu réussisses ou que tu réussisses.
   En français, cycle jusqu'à succès ou à la plus grande rotation.

Il s'agit de l'auto-réfinition (leçon 05) appliquée à la génération de code avec une vérification fondée sur l'environnement.

> ️ **【易错点】**Pour les compétences défaites, il faut les mettre directement dans le tableau des compétences.**后果**: l'ancienne version de l'original du travail a été perdue, la prochaine recherche est la nouvelle version avec un bug.**一行修复**: compétences库用版本化 key (en anglais seulement)`craft_pickaxe_v3`),失败时新增版本,不覆盖旧版本; seulement auto-vérification 通过才标记为`latest`Il y a une autre.

> C'est l'auto-réfinition (article 5) appliquée à la génération de codes de l'environnement (en tant que code de l'épreuve).

### Programme et exploration

Le module du programme de Voyager propose des tâches telles que " construire un abri près du lac " en fonction de ce que l'agent a et ce qu'il n'a pas encore fait.

> 🤔 **【困惑】**Q: Voyager a une " compétence " en JavaScript code "  Pourquoi pas Python ?  est Minecraft Mineflayer API  limité ?**代码作为动作空间必须可执行** langue n'est pas important, c'est important que "ne puisse être directement exécuté et retourné à succès/faillite signal"  dans le navigateur Agent 里可能是Playwright TS 代码, dans la base de données Agent 里可能是 SQL──

> Modules de cours du Voyager basés sur le contenu existant et non terminé de l'agent proposer des tâches, telles que " construire un refuge au bord du lac "  le proposateur utilise l'état de l'environnement + liste de compétences pour choisir un peu plus haut que la capacité actuelle  le meilleur point d'exploration 

Pour les agents de production, cela se traduit par un opérateur "ce qui manque": étant donné la bibliothèque de compétences actuelle et un domaine, quelles compétences ne sont pas encore couvertes?

> Pour l'agent de production, cela se traduit par un opérateur " manque de quoi ": dans un domaine et un ensemble de compétences actuels, quelles compétences n'ont pas encore été couvertes ?

### Où ce modèle va mal

- **Skill library rot.**La même compétence est ajoutée 10 fois avec des descriptions légèrement différentes.
  Le mot grec traduit par " le mot grec "**技能库腐化。**La même compétence utilise une description légèrement différente ajouter 10 fois.
- **Composed-skill drift.**Les compétences des parents dépendent d'un enfant qui a été affiné.
  Le mot grec traduit par " le mot grec "**组合技能漂移。**Les compétences des enfants qui dépendent des compétences des pères sont affinées.
- **Retrieval quality.**La récupération vectorielle sur les descriptions de compétences se dégrade à mesure que la bibliothèque dépasse quelques centaines.`category=tooling`").
  Le mot grec traduit par " le mot grec "**检索质量。**Les données de référence sont disponibles sur les sites de recherche et de recherche.`category=tooling`"De la compétence")

## Construisez-le en main
```figure
voyager-skills
```

## Faites-le

`code/main.py`met en œuvre une bibliothèque de compétences stdlib:

> `code/main.py`Utilisation de la base de compétences:

- `Skill` nom, description, code (en tant que chaîne), version, étiquettes, dépendances.
  Le mot grec traduit par " le mot grec "`Skill`名称、描述、代码(字符串) 、版本、标签、依赖──
- `SkillLibrary` enregistrer, rechercher (coupe de jetons), composer (type topologique de dép) et affiner (boîte de version à la mise à jour).
  Le mot grec traduit par " le mot grec "`SkillLibrary`注册、搜索(token 重叠)、组合(依赖的拓排序) 和精炼(更新时版本递增)
- Un agent scripté qui enregistre trois compétences primitives, compose une quatrième, frappe un échec et raffinera.
  En français, il est écrit: "Enregistrer trois compétences originales, assembler une quatrième, rencontrer un échec et éliminer un écrivain agent"".

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre les écrits de la bibliothèque, la récupération, la composition, une exécution ratée et un raffinement v2 de la boucle de Voyager de bout en bout.

> 轨迹显示库写入,检索,组合,一次失败执行和 v2 精炼 End to end cycle du voyageur

## Utilisez-le avec le cadre de réalisation

- **Claude Agent SDK skills**(Anthropic)  la référence 2026: chaque compétence a une description, un code et des instructions; chargée à la demande pendant une session d'agent.
  Le mot grec traduit par " le mot grec "**Claude Agent SDK skills**(Anthropic) 2026 Year Reference: chaque compétence a une description ̊ code et instruction; en Agent 会话中按需加载──
- **skillkit**(npm: skillkit)  Gestion des compétences entre agents pour plus de 32 agents de codage d'IA.
  Le mot grec traduit par " le mot grec "**skillkit**(npm: skillkit) 32+ AI 编码 Agent 跨 Agent 技能管理。
- **Custom skill libraries** Spécifique pour le domaine (compétences SQL pour les agents de données, compétences Terraform pour les infra-agents).
  Le mot grec traduit par " le mot grec "**自定义技能库** domaine spécifique DATA Agent  SQL skills、 Infrastructure Agent  Terraform skills)
- **OpenAI Agents SDK `tools`** à la fin inférieure; chaque outil est une compétence légère.
  Le mot grec traduit par " le mot grec "**OpenAI Agents SDK `tools`**低端; chaque outil est une compétence de niveau léger.

## Envoyez-le . Produit .

`outputs/skill-skill-library.md`génère une bibliothèque de compétences en forme de Voyager avec enregistrement, récupération, versionnement et raffinement câblé pour tout temps d'exécution cible.

> `outputs/skill-skill-library.md`Le programme de recherche et d'élaboration de l'équipe de recherche de l'avion Voyager est un outil de recherche et d'élaboration de compétences, adapté à tout objectif de mise en œuvre.

## Les exercices

1. Ajouter un détecteur de cycle de dépendance à `compose()`Que se passe-t-il quand la compétence A dépend de B qui dépend de A ?
   Dans le texte original,`compose()`En plus de dépendance à l'épreuve de cycle.
2. Implémenter la version de la mise en place de compétences.`crafting@1`, un raffinement à `crafting@2`ne doit pas mettre à niveau le parent en silence.
   Traduction anglaise: réalisation selon les compétences`crafting@1`时,`crafting@2`Le perfectionnement ne peut pas faire de progrès dans la pratique.
3. Remplacez la récupération par superposition de jetons par des intégrations de transformateurs de phrases (ou une impl BM25 stdlib). Mesurer la récupération@5 sur une bibliothèque de jouets de 50 compétences.
   Le code de la langue française est le code de la langue française.
4. Ajouter un agent "curriculum": compte tenu de la bibliothèque actuelle et de la description du domaine, proposer 5 compétences manquantes.
   En français, le terme " cours " est défini comme étant " cours " et " cours " en français.
5. Lisez les documents de compétences de Claude Agent SDK d'Anthropic, portez la bibliothèque de jouets au schéma de compétences du SDK.
   Le jeu de jouets est porté à la capacité de développement de jouets.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Skill | "Reusable capability" / "可复用能力" | Named chunk of code + description, retrievable by similarity / 命名的代码块 + 描述，可按相似性检索 |
| Skill library | "Agent memory of how-to" / "Agent 的操作记忆" | Persistent store of skills, searchable and composable / 技能的持久化存储，可搜索可组合 |
| Curriculum | "Task proposer" / "任务提议器" | Bottom-up goal generator driven by current capability gap / 由当前能力差距驱动的自底向上目标生成器 |
| Composition | "Skill DAG" / "技能 DAG" | Skills invoking skills; topologically sorted on execution / 技能调用技能；执行时拓扑排序 |
| Iterative refinement | "Self-correcting loop" / "自我纠错循环" | Env feedback + errors + self-verification fold back into the next version / 环境反馈+错误+自我验证反馈到下一版本 |
| Action-space-as-code | "Programmatic actions" / "编程式动作" | Emit functions, not primitive commands, for temporally extended behavior / 发出函数而非原始命令，用于时间扩展行为 |
| Dedup on write | "Skill collapse" / "技能合并" | Near-duplicate descriptions collapse to one canonical skill / 近似重复描述合并为一个规范技能 |

## Encore une lecture

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) le papier de la bibliothèque de compétences original
  Voyageur, le début de la carrière.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) les compétences en tant que productivisation de 2026
  Le programme de développement de l'entreprise est basé sur la technologie de l'industrie.
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) compétences et subagents en pratique
  En anglais, le code de la langue est le code de la langue de l'anglais.
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) la boucle de raffinement sous le Voyager
  Le cycle d'élimination de l'auto-réfibrillation
