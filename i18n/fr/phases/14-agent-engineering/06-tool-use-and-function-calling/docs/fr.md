# Utilisation des outils et des fonctions Appels  outils utilisation et fonction调用

> Toolformer (Schick et coll., 2023) a commencé à s'auto-surveiller en annotant les outils. Berkeley Function Calling Leaderboard V4 (Patil et coll., 2025) définit la barre 2026: 40% agent, 30% multi-tour, 10% en direct, 10% non-vivant, 10% hallucination.

> **【中文解读】**Le leaderboard de la fonction de Berkeley V4 définit les critères d'évaluation pour l'année 2026: 40% de l'intelligence, 30% de la chaîne, 10% du temps réel, 10% du temps non réel, 10% de la chaîne de réflexion.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 13 · 01 (Function Calling Deep Dive) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Expliquez le signal d'entraînement auto-surveillé de Toolformer: gardez les annotations de l'outil seulement lorsque l'exécution réduit la perte de jeton suivant.
  Traduction anglaise: Expliquer Le seul outil de formation de l'ancien:
- Nommez les cinq catégories d'évaluation de la BFCL V4 et les mesures que chaque catégorie prend.
  Le contenu de chaque mesure est fourni par BFCL V4.
- Implémenter un registre d'outils stdlib avec validation de schéma, coercition d'arguments et sandboxing d'exécution.
  Traduction anglaise: avec la bibliothèque standard pour réaliser avec le modèle de validation, les paramètres de transformation obligatoire et de l'exécution de la boîte de l'outil de référence.
- Découvrez les trois problèmes ouverts de 2026: la chaîne d'outils à long horizon, la prise de décision dynamique et la mémoire.
  Traduction anglaise: diagnostic trois 2026 ans ouverture problème:长链工具编排、动态决策和记忆──

## Le problème , l' introduction du problème

L'utilisation des outils précoces a posé la question: le modèle peut-il prédire une appel de fonction correcte? l'utilisation des outils moderne demande: peut-il le modèle de chaîne d'outils sur 40 étapes, avec mémoire, avec observabilité partielle, avec récupération des défaillances des outils, sans halluciner des outils qui n'existent pas?

> Le problème de l'utilisation des outils précoces est: le modèle peut-il prédire correctement la fonction de référencement ? Le problème de l'utilisation des outils modernes est: le modèle peut-il référencement des outils en 40 étapes en chaîne, avoir des mémoires, traiter des parties observables, récupérer des outils en panne et ne pas avoir l'impression d'exister ?

Les modèles peuvent apprendre à appeler des outils avec une autorégulation.BFCL V4 définit l'objectif d'évaluation de 2026 .L'écart entre eux est celui des agents de production spatiale dans lesquels vivent.

> Le modèle peut être utilisé à travers l'auto-surveillance. Le BFCL V4 définit l'objectif d'évaluation de 2026: la différence entre les deux est le espace de survie de l'agent de production.

> **【中文解读】**Le problème de l'utilisation des outils précoces est: le modèle peut-il prédire correctement la modification des fonctions ? Le problème de l'utilisation des outils modernes est: le modèle peut-il récupérer des outils en défaillance et ne pas se rendre compte qu'ils n'existent pas ?

> **【拓展：BFCL V4 评估体系的演进】**Le classement des fonctions de Berkeley V4 est un critère d'évaluation de la réalité de 2026[6]. V3 introduit une évaluation basée sur l'état de l'application de recherche (API) état réel plutôt que pas correspondant à AST), V4 ajoute une catégorie de recherche Web  mémorisation et sensibilité au format[6].

>  **【前置】**Façon 13·01 (Fonction appelant Deep Dive) 本节假设你已经能写 JSON Schema并理解人类的`input_schema`Les résultats de l' OpenAI`function.parameters`区别;Phase 14·01(Agent Loop)  outil de régularisation se produit dans le cycle de l'agent, quittez le cycle de régularisation

## Le concept de base.

### Le groupe de travail de l'équipe de formation (Schick et coll., NeurIPS 2023)

Idée: laissez le modèle annoter son propre corpus de pré-entraînement avec des appels API candidats. Pour chaque candidat, exécutez-le. Gardez la annotation seulement si l'inclusion du résultat de l'outil réduit les pertes sur le jeton suivant.

> 核心思想: faire en sorte que le modèle utilise son propre pré-entraînement de la marque de texte API 调调.

Les outils couverts: calculateur, système d'évaluation de qualité, moteurs de recherche, traducteur, calendrier.

> 覆盖的工具:计算器、QA 系统、搜索引擎、翻译器、日历──自监督信号纯粹关于工具是否有助预测文本不需要人工标签──

Les modèles plus petits sont touchés par les annotations des outils; les modèles plus grands gagnent. C'est pourquoi les modèles frontaliers 2026 ont une forte utilisation des outils, tandis que la plupart des modèles 7B nécessitent une mise en forme explicite de l'utilisation des outils pour être fiables.

> 规模效应: tool use on the big model surgissent. 小模型反而被工具标注损害; 大模型则受益. 如此为什么2026年前沿模型内置强大工具使用能力,而大多数7B模型需要显式工具使用微调才能可靠──

> **【中文解读】**L'idée centrale de Toolformer est de faire en sorte que le modèle utilise son propre API de marquage de texte pré-entraînement. Pour chaque candidat, il l'exécute. Seuls les résultats contenant des outils peuvent réduire la perte d'un prochain jeton peuvent conserver le marquage.

### Le tableau de classement des fonctions de Berkeley V4 (Patil et coll., ICML 2025)

BFCL est l'évaluation de facto de 2026 .

> Le BFCL est un critère d'évaluation de la réalité de l'année 2026[6].

- **Agentic (40%)** trajectories de l'agent complet: mémoire, multiples tours, décisions dynamiques.
  Le mot grec traduit par " le mot grec "**智能体 (40%)** Complete Agent 轨迹: souvenir, tournée, décision en cours de route
- **Multi-Turn (30%)** des conversations interactives avec des chaînes d'outils.
  Le mot grec traduit par " le mot grec "**多轮 (30%)**带工具链的交互式对话──
- **Live (10%)** réelles demandes d'information envoyées par l'utilisateur (distribution plus difficile).
  Le mot grec traduit par " le mot grec "**实时 (10%)** réellement présenté par l'utilisateur (en anglais)
- **Non-Live (10%)** cas d'essai synthétiques.
  Le mot grec traduit par " le mot grec "**非实时 (10%)**合成测试用例──
- **Hallucination (10%)** détecter quand aucun outil ne doit être appelé.
  Le mot grec traduit par " le mot grec "**幻觉 (10%)**检测何时不应调用工具──

V3 introduit une évaluation basée sur l'état: après une séquence d'outils, vérifiez l'état réel de l'API (par exemple: "le fichier a-t-il été créé?") plutôt que de correspondre à l'AST des appels de l'outil. V4 a ajouté des catégories de recherche Web, de mémoire et de sensibilité au format.

> V3 introduit une évaluation basée sur l'état: après l'exécution de la séquence d'outils, vérifiez l'état réel de l'API (par exemple: " le fichier a-t-il été créé ? ") plutôt que l'utilisation de l'outil de recherche AST。 V4 ajoute la recherche Web、 mémoire et la sensibilité au format.

Résultats de la recherche: l'appel à la fonction à tour unique est presque résolu. Les défaillances se concentrent dans la mémoire (le transport de contexte à travers les tours), la prise de décision dynamique (le choix d'outils basé sur des résultats antérieurs), les chaînes à long horizon (départ après plus de 20 étapes) et la détection des hallucinations (rejet de passer un appel quand aucun outil ne convient).

> Réalisation de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de la phase de révision de révision de révision de la phase de révision de révision de révision de la phase de révision de révision de révision de la phase de révision de révision de révision de révision de la phase de révision de révision de révision de révision de la phase de révision de révision de révision de révision de la phase de révision de révision de révision de révision de révision de la phase de révision de révision de révision de révision de la phase de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de la phase de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de

### Schéma d' outil

Chaque fournisseur a un schéma. Ils diffèrent dans les détails mais partagent la même forme:

> Chaque fournisseur a son propre modèle.

```
name: string
description: string (what it does, when to use it)
input_schema: JSON Schema (properties, required, types, enums)
```

Utilisation anthropologique `input_schema`Directement.`function.parameters`Les deux acceptent le schéma JSON. Les descriptions sont portables  le modèle les lit pour choisir l'outil correct. Les descriptions d'outils malveillants sont la première cause de défaillances de choix de mauvais outils.

>  **【类比】**工具描述就像给实习生写的"使用说明书"―― un modèle qui n'a jamais vu ton outil, il n'y a que la description dont il peut compter― si tu écris`name: get_user, description: "gets user"`Le modèle ne sait pas si c'est par ID ou par boîte de réception.**好描述包含三要素**: faire quoi + 何時用 + 输入输出语义──

> ️ **【易错点】**Le modèle de retour de la confiance est le type de paramètre.`"5"`Retour à l' attente`int`Le schéma de la réforme**后果**: votre outil fonction `TypeError`L'ensemble de la boucle d'agents est interrompu.**一行修复**: dans les outils d'exécution`pydantic.BaseModel.parse_obj`Ou comme une expérience, une expérience échoue lorsque vous retournez à une erreur structurée, comme`{"error": "expected int, got str"}`Je vais essayer de le faire.

> Anthropologie 直接使用 `input_schema`✿OpenAI 使用 `function.parameters`◊ Tous deux acceptent le schéma JSON. La description est la base du modèle.

### Validation des arguments

Ne faites confiance à aucun appel d'outil.

> Ne vous fiez à aucun outil.

1. **Type coercion.**Le modèle peut retourner une chaîne "5" où le schéma dit int. Forcer si non ambigu; rejeter si non.
   Le mot grec traduit par " le mot grec "**类型强制转换。**模型可能返回字符串 "5" 但模式要求 int──如果无歧义则强制转换;否则拒绝──
2. **Enum validation.**Si le schéma dit:`status in {"open", "closed"}`et émissions de modèle `"in_progress"`, rejeter avec une erreur descriptive.
   Le mot grec traduit par " le mot grec "**枚举验证。**Si mode spécifié `status in {"open", "closed"}`La production et la production`"in_progress"`, avec une description de l'erreur de refus.
3. **Required fields.**champ requis manquant -> observation d'erreur immédiate de retour au modèle, pas un crash.
   Le mot grec traduit par " le mot grec "**必填字段。**缺少必填字段 -> 立即回归错误观察给模型, plutôt que de s'effondrer
4. **Format validation.**Les dates, les courriels, les adresses URL  valident avec des parseurs de béton, pas avec des regex.
   Le mot grec traduit par " le mot grec "**格式验证。**Il est utilisé pour l'expression de l'URL avec des analystes spécifiques, et non avec des expressions ordinaires.

Chaque défaillance de validation doit renvoyer une observation structurée afin que le modèle puisse réessayer avec la forme correcte.

> Chaque échec de test doit être retourné à l'observation structurée, afin que le modèle puisse être retesté avec le format correct.

### Appels parallèles à l'outil

Les fournisseurs modernes prennent en charge les appels parallèles d'outils en un seul tour d'assistant.

> 现代提供商支持在一个助手轮次中并行调用工具──循环:

1. Le modèle émet 3 appels d' outils avec des distincts `tool_use_id`S.
   Le modèle évolue avec 3 différences`tool_use_id`Les outils sont utilisés.
2. Le temps d'exécution les exécute (en parallèle si indépendant).
   Le texte est écrit en français.
3. Chaque résultat revient comme un `tool_result`bloc corrélateur par `tool_use_id`- Je suis désolé .
   Le mot " résultat " est traduit par " résultat ".`tool_result`Retour en arrière, par le biais`tool_use_id`Je suis en train de vous parler.

Règle d'ingénierie: traiter les identifiants de corrélation comme des charges, les échanger et vous obtenez un routage de mauvais outil à mauvais résultat.

> 🤔 **【困惑】**Q: 40% de BFCL V4 est agent, n'est-ce pas indiquer que le cycle unique n'est plus important ? A: Non. 40% agent est pour refléter la production réelle, mais le taux de précision de la rotation unique est toujours la base de la tâche agent.

> 工程规则:将关联 ID 视为核心承载──交换它们会导致错误的工具-结果路由──

### La boîte à sable

L'exécution de l'outil est la limite de la boîte à sable. Voir leçon 09 pour plus de détails.`run_shell(cmd)`est un drapeau rouge; spécifique `git_status()`C'est plus sûr.

> 工具执行是沙箱边界──详见第 9 课――简短版: chaque instrument doit être spécifié dans la gamme de lecture, dans la gamme de l'accès au réseau, dans la durée et dans la limite de la mémoire.`run_shell(cmd)`est le drapeau rouge; spécifique `git_status()`Plus sûr.

## Construisez-le en main
```figure
tool-routing
```

## Faites-le

`code/main.py`met en œuvre un registre des outils de forme de production:

> `code/main.py`实现 un registre de l'outil de production:

- Validateur de sous-ensemble JSON Schema (stdlib uniquement).
  Le système de test de JSON est un système de test de JSON.
- L'enregistrement de l'outil avec description, schéma d'entrée, délai et exécuteur.
  Avec le modèle de description, de saisie, de l'écriture et de l'exécution.
- La coercition des arguments et la validation enum.
  Le mot "paramètres" est traduit par "paramètres".
- Envoi parallèle d'outils avec identifiants de corrélation.
  Le mot de passe de la carte de crédit est le mot de passe de la carte de crédit.
- Observations d'erreur en tant que chaînes structurées.
  Le texte est écrit en français.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre un mini agent appelant trois outils à tour de rôle, avec un appel délibérément malformé qui est rejeté avec une erreur descriptive sur laquelle le modèle peut agir.

> 轨迹显示一个迷你代理在一轮次中调用三个工具, dont un de la façon intentionnelle de façon incorrecte de la façon de faire une mauvaise description de la façon de refuser, le modèle peut être selon cette action.

## Utilisez-le avec le cadre de réalisation

Chaque fournisseur a son propre schéma d'outils  Anthropic, OpenAI, Gemini, Bedrock. Utilisez une couche de traduction (OpenAI Agents SDK, Vercel AI SDK, adaptateur d'outils LangChain) si vous avez besoin de plusieurs fournisseurs.

> Chaque fournisseur a son propre modèle d'outils: Antropic, OpenAI, Gemini, Bedrock. Si vous avez besoin de plusieurs fournisseurs, utilisez le SDK, le Vercel, le LongChain outil adaptateur.

## Envoyez-le . Produit .

`outputs/skill-tool-registry.md`génère un catalogue d'outils, un schéma et un registre pour un domaine de tâche donné. Inclut des contrôles de qualité de la description (la description de chaque outil indique-t-elle au modèle quand l'utiliser?).

> `outputs/skill-tool-registry.md`Pour un domaine de tâches déterminées, générer des outils Catalogue, Modèle et registre.

## Les exercices

1. Ajouter un outil "no-op" qui permet au modèle de refuser explicitement d'utiliser tout autre outil. Mesurer sur un test d'hallucination similaire à BFCL.
   En français, le modèle est utilisé pour la mesure de la quantité de données.
2. Où la coercition commence-t-elle à cacher de vrais insectes ?
   Le nombre de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de la liste de caractères de caractères de la liste de caractères de caractères de la liste de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de caractères de
3. Ajouter un temps d'arrêt par outil et un disjoncteur (rejeter l'outil pendant 60 ans après 3 défaillances consécutives).
   En français, le temps de réinitialisation est de 30 à 60 secondes.
4. Lisez la description de BFCL V4. Choisissez une catégorie (par exemple "multi-turn") et exécutez 10 invites d'exemple par l'intermédiaire de votre agent.
   Le nombre de personnes qui ont été recrutées dans le cadre de l'enquête est de 10 000 personnes.
5. Portes le validateur de stdlib à Pydantic ou Zod.
   Le système de contrôle de la gamme est en cours de développement.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" / "工具使用" | Structured-output tool invocation with validated schema / 带验证模式的结构化输出工具调用 |
| Toolformer | "Self-supervised tool annotation" / "自监督工具标注" | Schick 2023 — keep tool calls whose results reduce next-token loss / Schick 2023——保留减少下一个 token 损失的工具调用 |
| BFCL | "Berkeley Function Calling Leaderboard" / "Berkeley 函数调用排行榜" | 2026 benchmark: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination / 2026 基准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉 |
| Tool schema | "Function signature for the model" / "模型的函数签名" | name, description, JSON Schema of arguments / 名称、描述、参数的 JSON Schema |
| tool_use_id | "Correlation ID" / "关联 ID" | Ties a tool call to its result; essential for parallel dispatch / 将工具调用与其结果关联；并行分派必需 |
| Hallucination detection | "Know when not to call" / "知道何时不调用" | V4 category: refuse to call when no tool fits / V4 类别：无合适工具时拒绝调用 |
| Argument coercion | "String-to-int repair" / "字符串到整数的修复" | Narrow fixes for predictable schema-mismatch; reject if ambiguous / 可预测模式不匹配的窄修复；如果歧义则拒绝 |
| Sandboxing | "Tool execution boundary" / "工具执行边界" | Per-tool read/write surface, network, timeout, memory cap / 每个工具的读写范围、网络、超时、内存上限 |

## Encore une lecture

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) annotation d'outils autosuvisés
  Le texte de la première partie de la série est le texte de la première partie de la série.
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html) référence d'évaluation 2026
  Le classement de la classe de Berkeley est basé sur la base de la liste de la classe de Berkeley.
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview) Schéma d'outil de production dans le SDK Claude Agent
  Le modèle de production de l'agent Claude SDK est un modèle de production de l'agent Claude.
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) type d'outil de fonction et Garderrails
  Le code de gestion de la fonctionnalité est le code de gestion de la fonctionnalité.
