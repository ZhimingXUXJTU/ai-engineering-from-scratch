# Pourquoi multi-agent ?

> Un agent frappe un mur, le mouvement intelligent n'est pas un agent plus grand, c'est plus d'agents.

> **【中文解读】**Ce chapitre présente les raisons pour lesquelles il faut plus d'agents, les problèmes de confusion et de confusion de rôles, ainsi que la façon dont les agents peuvent résoudre ces problèmes en collaborant avec d'autres.

> **【拓展：why multi agent→具体应用】** Un agent unique est confronté à trois bouteilles lors du traitement de tâches complexes: 1) le message est déversé dans une fenêtre, l'information est submergée; 2) le désordre de rôles  Un agent joue plusieurs rôles qui provoquent des conflits de propos; 3) la chaîne d'exécution  des outils de référencement  ne peut être réparé                                                                                                                                                                                                                 

>  **【前置】**Les réponses à la question suivante sont: "Quand utiliser plusieurs agents" simple réponse: "Un seul agent + un seul instrument ne suffit pas à temps"".Expérience anthropique: tâche nécessite > 50 outils de réemploi"", ou > 1 rôle" (tel que chercheur + écrivain)

>  **【类比】**单 Agent vs 多 Agent = 全能管家 vs 专业团队──全能管家──单 Agent) peut tout faire mais chaque chose n'est pas précis: suédois faire la cuisine、 suédois faire la cuisine、 suédois faire la cuisine、 soirée faire la cuisine, chaque chose est un demi-jambon.

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Identifier le plafond de l'agent unique (survol de contexte, expertise mixte, goulets d'étranglement séquentiels) et expliquer quand la division en plusieurs agents est la bonne décision
  Le nom de l'agent unique est le plus souvent défini dans le langage de l'agent unique.
- Comparer les modèles d'orchestration (pipeline, ventilateur parallèle, superviseur, hiérarchique) et sélectionner le bon pour une structure de tâche donnée
  Le modèle de mise en place de la structure de tâches est le modèle de mise en place de la structure de tâches.
- Conception d'un système multi-agents avec des limites de rôle claires, un état partagé et un contrat de communication
  Traduction anglaise: dessiner un système multi-agent avec un rôle précis, un cadre de communication et un état de partage
- Analyse des compromis entre la complexité multi-agent (la latence, le coût, la difficulté de débogage) et la simplicité d'un agent unique
  Traduction anglaise: analyse multiple Agent  complexité 延迟、成本、调试难度) et un seul Agent 简单性

## Le problème , l' introduction du problème

Vous avez construit un seul agent dans la phase 14. Il fonctionne. Il peut lire des fichiers, exécuter des commandes, appeler des API et raisonner sur les résultats. Ensuite, vous le pointez vers une base de code réelle: 200 fichiers, trois langues, des tests qui dépendent de l'infrastructure, et une exigence de rechercher des API externes avant d'écrire du code.

> Vous construisez un seul agent à la phase 14. Il fonctionne bien, peut lire des fichiers, exécuter des commandes, utiliser l'API et faire des recherches sur les résultats. Ensuite, vous le dirigez vers une vraie base de codes: 200 fichiers, trois langues, tests de dépendance à l'infrastructure, ainsi que des exigences de réécriture de code en API externe.

Le fossé entre les agents de démonstration et les agents de production est le fossé entre "un fichier, une langue, un outil" et "plusieurs fichiers, beaucoup de langues, beaucoup d'outils avec des dépendances".

> 演示 Agent et production Agent est la différence entre "un document, une langue, un outil" et "un grand nombre de documents, de nombreuses langues, de nombreux outils dépendants".

L'agent se noie. Non pas parce que le LLM est stupide, mais parce que la tâche dépasse ce qu'un boucle d'agent peut gérer. La fenêtre contextuelle se remplit de contenu de fichier. L'agent oublie ce qu'il a lu 40 appels d'outils. Il essaie d'être chercheur, un codeur et un critique à la fois, et fait les trois mal.

> L'agent s'est effondré. Non pas parce que le LLM est stupide, mais parce que les tâches dépassent le champ de traitement d'un seul agent.

C'est le plafond à agent unique, on le frappe chaque fois qu'une tâche exige:

> C'est un seul agent à la limite. Chaque fois que la mission nécessite les conditions suivantes, vous rencontrerez:

Le plafond est structurel, pas algorithmique. Un meilleur LLM retarde le plafond mais ne le supprime pas. Une fenêtre de contexte de 1M-token se remplit aussi sûrement qu'une 200k  il faut juste plus de fichiers.

> La limite supérieure est structurelle, pas algorithmique. Une meilleure LLM est retardée mais ne la déplace pas.

- **More context than fits in one window**- lire 50 fichiers passe 200 000 jetons
  Le mot grec traduit par " le mot grec "**超出一个窗口容量的上下文** 读取 50 文件会超过200k de jetons
- **Different expertise at different stages**- la recherche nécessite une incitation différente de la génération de code
  Le mot grec traduit par " le mot grec "**不同阶段需要不同的专业知识** Les besoins de recherche et la génération de code sont différents
- **Work that can happen in parallel**- Pourquoi lire trois fichiers en séquence quand on peut les lire simultanément ?
  Le mot grec traduit par " le mot grec "**可以并行执行的工作**Si on peut lire trois documents en même temps, pourquoi les lire en ordre ?

## Le concept de base.

### Le plafond à agent unique

Un seul agent est une boucle, une fenêtre contextuelle, une requête système.

> Un seul agent est un cycle, une fenêtre de texte, un système de suggestions.

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

Le système unique est la cause principale. Il doit donner des instructions pour la recherche, le codage, l'examen et les tests simultanément. Chaque instruction dilue les autres. L'agent finit par " ok " à tout, excellent à rien.

> 单系统提示是根本原因――它必须同时提供指令用于研究,编码,审核和测试――每条指令稀释其他――Agent 最终在所有事上"还行",在任何事上都不优秀――

Trois choses se brisent:

> Trois problèmes vont entraîner une chute:

1. **Context saturation**Au tour 30, l'agent a consommé 150 000 jetons de contenu de fichiers, de commandes et de raisonnement préalable.
   Le mot grec traduit par " le mot grec "**上下文饱和** 工具結果不断堆积──到第30轮时,Agent 已消耗150k tokens 文件内容、命令输出和前推理──第5轮关键细节丢失──

2. **Role confusion**- un prompt système qui dit "vous êtes un chercheur, un codeur, un réviseur et un testeur" produit un agent qui fait la moitié de la recherche, la moitié des codes, et ne termine jamais la révision.
   Le mot grec traduit par " le mot grec "**角色混乱** Un système d'expérience qui écrit "tu es chercheur, programmeur, réviseur et testeur" génère un agent à moitié-étude, à moitié-codeur, toujours incomplet d'examen.

3. **Sequential bottleneck**- l'agent lit le dossier A, puis le dossier B, puis le dossier C. Trois appels en série, trois exécutions en série.
   Le mot grec traduit par " le mot grec "**串行瓶颈** Agent 读取文件 A, puis文件 B, puis文件 C──三次串行 LLM 调用──三次串行工具执行──没有并行性──

L'agent unique est un généraliste qui est demandé à être spécialiste à chaque étape.

> Un agent unique est un agent qui est obligé de devenir un expert à chaque étape.

### La solution à plusieurs agents

Donnez à chaque agent un travail, une fenêtre contextuelle et une requête système adaptée à ce travail:

> 拆分工作── donner à chaque agent une tâche、 une fenêtre de texte ci-dessus et un système de suggestion pour cette tâche:

Il s'agit d'une " séparation des préoccupations " appliquée aux agents de LLM. Le prompt de chaque agent est plus court et plus concentré. La fenêtre contextuelle de chaque agent ne contient que ce dont il a besoin. Chaque agent peut être testé et amélioré indépendamment. L'orchestre gère la composition.

> Il est appliqué à l'agent de LLM pour "concentrer les points de séparation". Chaque agent a des conseils plus courts et plus focalisés.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Chaque agent a:
- Une requête de système centrée ("Vous êtes un réviseur de code. Votre seul travail est de trouver des bugs. ")
  Le code est un code reviewer. Votre seule tâche est de trouver des bugs.
- Sa propre fenêtre de contexte (non polluée par le travail d'autres agents)
  Le travail de l'agent est contaminé par le même agent.
- Un contrat de sortie/entrée clair (recevoir des notes de recherche, code de sortie)
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la

L'agent orchestrateur ne doit comprendre que la tâche de haut niveau et comment déléguer. Il n'a pas besoin de savoir comment faire chaque sous-tâche. Chaque agent spécialisé ne doit connaître que son propre travail étroit.

> 编排 Agent Il suffit de comprendre les tâches de haut niveau et comment les déléguer. Il ne suffit pas de savoir comment accomplir chaque tâche.

### Des systèmes réels qui le font

**Claude Code subagents**- quand Claude Code engendre un subagent avec `Task`Le parent garde son contexte propre, l'enfant travaille avec concentration et renvoie un résumé.

> **Claude Code 子 Agent** 当 Claude Code 使用 `Task`Lorsqu'un agent est créé, il crée un agent de son propre domaine.

Le modèle est viral parce qu'il se compose: un subagent peut engendrer ses propres subagents.

> Ce mode de propagation virale est courant dans les trois niveaux de tâches de code complexe; au-delà de cette profondeur, le test devient douloureux.

**Devin**- un agent de planification, un agent de programmation et un agent de navigateur. le planificateur découpera le travail en étapes. le codeur écrit le code. le navigateur recherche la documentation. chacune a un contexte distinct.

> **Devin** 运行一个规划代理一个编码代理 和一个浏览器代理――规划器将工作分解成步骤――编码器编写代码――浏览器研究文档――每个都有独立的上下文――

L'architecture de Devin est le modèle de superviseur de manuel: un planificateur qui possède le plan mondial, plusieurs travailleurs spécialisés qui exécutent des tranches.

> L'architecture de Devin est le modèle du superviseur du style du livre: un planificateur qui a un plan global, plusieurs épisodes exécutés, un spécialiste du travail.

**Multi-agent coding teams (SWE-bench)**- les systèmes de performance supérieure sur le banc SWE utilisent un chercheur qui lit la base de code, un planificateur qui conçoit la correction et un codeur qui la met en œuvre.

> **多 Agent 编码团队 (SWE-bench)** SWE-bench sur le meilleur système de performance à l'aide d'un chercheur de la bibliothèque de code de lecture, un planificateur de programme de révision de conception et un éditeur de révision de mise en œuvre.

Le tableau de leader du banc SWE 2026 est dominé par des systèmes multi-agents. Le modèle: un chercheur avec un large contexte pour la compréhension de la base de code, un planificateur avec un prompt axé sur la conception de corrections, un codeur avec des exigences de typage strictes pour la mise en œuvre. Chaque rôle obtient le prompt dont il a besoin.

> 2026 SWE-bench  répertoire par plusieurs agents  système dominé 模式:带大上下文的研究员用于代码库理解、带焦提示的规划器用于修复设计、带严格类型要求的编码器用于实现──每个角色都获得了它需要的提示──

**ChatGPT Deep Research**- génère plusieurs agents de recherche en parallèle, chacun explorant un angle différent, puis synthétise les résultats.

> **ChatGPT Deep Research** et de générer plusieurs agents de recherche, chaque explorer différents angles, puis de compiler les résultats.

### Le spectre

Le multi-agent n'est pas binaire, c'est un spectre:

> Il n'y a pas de double agent.

Le cadre du spectre est important car la plupart des systèmes de production ne sont pas à l'un des extrêmes. Claude Code utilise des subagents (un niveau de profondeur). Devin utilise une petite équipe.

> Le cadre de spectre est important, car la plupart des systèmes de production ne sont pas en phase avec le système de production.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**- Une boucle, une commande.

> **单 Agent** Un cycle, une suggestion  Adapté à une simple tâche 

**Subagents**- un parent donne naissance à des enfants pour des sous-tâches ciblées. le parent maintient le plan. les enfants rapportent. c'est ce que fait Claude Code.

> **子 Agent** Père Agent pour se concentrer sur les sous-tâches générées  Père Agent 维护计划 子 Agent 汇报结果  Voilà la pratique de Claude Code

**Pipeline**- les agents fonctionnent en séquence. la sortie de l'agent A devient l'entrée de l'agent B. Bon pour les flux de travail stagnées: recherche -> code -> examen -> test.

> **流水线** Agent 顺序运行──Agent A's输出成为 Agent B's输入──适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试──

**Team**- les agents fonctionnent en parallèle avec un bus de messagerie partagé. chacun a un rôle. un orchestrateur coordonne. bon quand différentes compétences sont nécessaires simultanément.

> **团队** Agent 通過共享消息总线并行运行──每个人都有角色──编排器协调──适应需要同时使用不同技能的场景──

**Swarm**- beaucoup d'agents identiques ou presque identiques avec un état partagé. pas d'orchestre fixe. les agents prennent le travail à la file d'attente. bon pour des tâches parallèles à haut débit.

> **群体**  许多相同或近似相同的代理 共享状态――没有固定的编排器――Agent de l'ordre de travail――适合高吞吐量并行任务――

### Les quatre modèles multi-agents

#### Modèle 1: Pipeline

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Chaque agent transforme les données et les transmet, simple à raisonner, mais l'échec d'une étape bloque le reste.

> Chaque agent transfère des données et les transmet à l'autre.

Utilisez quand: chaque étape a une entrée/sortie claire et les étapes sont naturellement séquentielles.

> Utilisation de la situation: chaque étape a une explication de l'entrée/sortie et une explication de l'ordre naturel de l'exécution.

#### Modèle 2: Fan-out / Fan-in

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Partager le travail entre des agents parallèles, puis fusionner les résultats.

> Le travail sera distribué à l'agent qui suit la même ligne, puis le résultat sera combiné.

Utilisez lorsque: la tâche se divise nettement en morceaux indépendants (par exemple, recherchez 5 sources différentes, résumons 10 documents). Évitez lorsque: les sous-tâches dépendent les unes des autres ou la fusion nécessite un raisonnement profond.

> Utilisation de la situation: les tâches peuvent être clairement divisées en parties indépendantes, comme par exemple 5 个不同来源,总结, 10 份文档.

#### Modèle 3: Orchestreur-travailleur

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

Un orchestrateur intelligent décide de ce qu'il doit faire, délègue les résultats aux travailleurs et synthétise les résultats.

> L'éditeur intelligent décide de ce qu'il fait, l'envoie à l'éditeur, et comporte des résultats.

Utiliser quand: la tâche est suffisamment complexe pour que décider quoi faire soit lui-même un problème difficile.

> Utilisation de la situation: les tâches sont assez complexes, décider quoi faire en soi est un problème difficile.

#### Modèle 4: Les pairs

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

Aucun orchestrateur central, les agents communiquent entre eux, les décisions émergent de l'interaction, plus difficile à déboguer, mais à échelle de nombreux agents.

> 没有中央编排器──Agent 之间点对点通信──决策从交互中涌现──更难调试,但可以扩展到许多Agent──

Utilisez lorsque: de nombreux agents homogènes effectuent des travaux similaires (grappage, classification) à l'échelle.

> Utilisation de la technique: beaucoup de agents de même qualité à grande échelle faire des travaux similaires

### Quand ne pas utiliser de multi-agent

Le débogage passe de "lire une conversation" à "tracer les messages à travers cinq agents".

> Les messages entre les agents sont un problème potentiel. La modification de la " lecture d'un dialogue " est devenue " tracer les messages entre les cinq agents ".

**Stay single-agent when:**
- La tâche s'inscrit dans une fenêtre contextuelle (moins de 100k tokens de données de travail)
  Le nombre de données de travail ne dépasse pas 100 000 jetons)
- Vous n'avez pas besoin de différentes instructions système pour les différentes étapes
  Le système de communication est un système de communication.
- L' exécution séquentielle est assez rapide
  Suivant: Le temps de l'exécution suffit
- La tâche est assez simple pour qu'en la divisant, on ajoute plus de coûts généraux que de valeur.
  Traduction anglaise: tâche assez simple, décomposition augmentée des dépenses dépassant sa valeur

**The complexity cost:**
- Chaque limite d'agent est une étape de compression perdue: le contexte complet de l'agent A est résumé dans un message pour l'agent B
  Chaque agent 边界都是有损压缩步骤: Le message complet de l'agent A est résumé pour envoyer le message de l'agent B
- La logique de coordination (qui fait quoi, quand, dans quel ordre) est sa propre source de bugs
  Le code de la ligne de référence est le code de la ligne de référence.
- L'augmentation de la latence: N agents signifie N séries LLM appels minimum, plus si elles ont besoin de parler en avant et en arrière
  Le nom de l'agent signifie au moins N fois que vous faites une demande de licence.
- Le coût est multiplié par un: chaque agent brûle des jetons indépendamment
  Nom de fichier: "Cost倍增:每个 Agent 独立消耗 token"

Règle générale: si une tâche prend moins de 20 appels d'outils et s'adapte à 100 000 jetons, gardez-la à un seul agent.

> 經驗法: Si une tâche ne nécessite que 20 fois de réparation des outils, et est adaptée à 100 000 jetons, il faut garder un seul agent.

## Construisez-le et mettez-le en œuvre.
```figure
swarm-messages
```

## Faites-le

### Étape 1: L'agent célibataire surchargé

Il a un énorme système de commande et une fenêtre contextuelle contenant des recherches, du code et des critiques:

> C'est un seul agent qui essaie de tout faire. Il a une énorme offre de système et une fenêtre de recherche, de code et de révision.

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Problèmes avec cette approche:
- La fenêtre contextuelle grandit à chaque étape.
  La fenêtre de la première phase de la croissance à chaque étape de la révision, elle contient des notes et des codes de recherche ainsi que des suggestions antérieures.
- Le système est générique, il ne peut pas être réglé pour chaque étape.
  Le système de suggestion est universel.
- Rien ne fonctionne en parallèle.
  Il est également connu pour sa production de produits chimiques.

La boucle à agent unique oblige le LLM à passer de contexte à autre entre des tâches cognitives très différentes (recherche vs codage vs révision) à chaque tour.

> 单代理 循环迫使 LLM 单代理 循环迫使 LLM 单代理 循环迫使 LLM 单代理 循环迫使 LLM 单代理 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环迫使 LLM 循环 循环冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲冲

### Étape 2: Agents spécialisés

Chaque agent a un travail:

> Maintenant, décomposez-le. Chaque agent obtient une mission:

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Chaque spécialiste a une mise en œuvre centrée, et chacun obtient une fenêtre contextuelle propre avec seulement les informations dont il a besoin.

> Chaque spécialiste a une idée de concentration. Chacun obtient une fenêtre de texte en haut et en bas propre, contenant uniquement les entrées nécessaires.

Le prompt du chercheur est optimisé pour la lecture et la résumé. Le prompt du codeur est optimisé pour écrire du code propre. Le prompt du réviseur est optimisé pour trouver des bugs. Aucun prompt unique n'essaie de faire les trois.

> Les conseils des chercheurs sur la lecture et l'optimisation du résumé. Les conseils des éditeurs sur la rédaction de code propre. Les conseils des rédacteurs sur la découverte de bugs.

### Étape 3: Coordonner les messages

Envoyez les spécialistes avec un message explicite:

> 通过显式消息传递将专家连接起来:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Chaque agent reçoit seulement les messages qui lui sont adressés, sans pollution de contexte, les 50 000 jetons de lecture de la documentation du chercheur n'entrent jamais dans le contexte du réviseur.

> Chaque agent ne reçoit que son propre message. Il n'y a pas de contamination de la page.

C'est le principal gain: l'isolement de l'information. La fenêtre contextuelle de chaque agent est dédiée à sa propre tâche. Le budget de 200 000 jetons d'un agent n'est pas gaspillé sur le travail de grattage des autres agents.

> C'est l'avantage central: l'isolement de l'information. Chaque fenêtre de l'agent se concentre sur sa propre tâche.

### Étape 4: Comparer

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

La version multi-agent utilise plus de jetons totaux (trois agents, trois appels LLM séparés), mais le contexte de chaque agent reste propre.

> Trois agents, trois LLM indépendants, mais chaque agent de la mise en page ci-dessus reste propre.

Le commerce est clair: dépenser plus de jetons, obtenir un meilleur rendement. Valorisez-le quand la tâche est difficile.

> Le poids est clair: dépenser plus de jetons, obtenir de meilleurs résultats.

## Utilisez-le avec le cadre de réalisation

Cette leçon fournit une information réutilisable pour décider quand se rendre multi-agent.`outputs/prompt-multi-agent-decision.md`- Je suis désolé .

> Le cours présente une suggestion réutilisable, pour décider quand utiliser plusieurs agents.`outputs/prompt-multi-agent-decision.md`Il y a une autre.

Le prompt pose quatre questions de diagnostic: 1) la tâche nécessite-t-elle plus de 100 000 tokens de contexte de travail? 2) elle a besoin de compétences différentes à différentes étapes? 3) il y a un travail parallèle? 4) la complexité vaut-elle la peine de payer les frais généraux?

> La proposition pose quatre questions de diagnostic: 1) la tâche nécessite-t-elle plus de 100 000 tokens de travail? 2) les différentes étapes nécessitent-elles des connaissances différentes? 3) y a-t-il des tâches qui peuvent être effectuées en même temps? 4) la complexité est-elle digne de vente?

## Les exercices

1. Ajouter un quatrième spécialiste: un agent " testeur " qui reçoit du code du codeur et examine les commentaires du réviseur, puis écrit des tests
   En français, le code de l'écrivain est rédigé par un agent, puis il est rédigé par un écrivain.
2. Modifier le pipeline afin que le réviseur puisse envoyer des commentaires au codeur pour une boucle de révision (max 2 tours)
   Traduction anglaise: modifier le flux de l'eau, permettant au lecteur de transférer le flux de l'eau vers le codeur pour effectuer le cycle de modification (maximum 2 rounds)
3. Convertir le pipeline séquentiel en un ventilateur: exécuter le chercheur et un agent "analyseur de besoins" en parallèle, puis fusionner leurs sorties avant de passer au codeur
   Le codeur est le codeur de l'équipe de recherche et de l'analyseur de besoins.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Encore une lecture

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- analyse des modèles multi-agents
  Le récit de la rédaction de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- Le cadre de conversation multi-agents de Microsoft
  AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- comment Claude Code délègue avec la tâche
  Le code Claude  How to use Task 委派
- [CrewAI documentation](https://docs.crewai.com/)- cadre multi-agents fondé sur les rôles
  Le rôle de l'agent est à l'origine de la création d'un ensemble de personnages.
