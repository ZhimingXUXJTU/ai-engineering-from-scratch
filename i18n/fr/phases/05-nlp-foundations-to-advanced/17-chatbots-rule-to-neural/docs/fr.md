# Chatbots  Règles basées sur les neurones à des agents de LLM  聊天机器人  规则到神经网络到LLM Agent

> ELIZA répond avec des correspondances de motifs. DialogFlow carte des intentions. GPT répond à partir de poids. Claude exécute des outils et vérifie. Chaque ère a résolu le pire échec de l'autre.
> ELIZA Utilise le modèle de correspondance et de réaction.

> **【中文解读】**De l'ELIZA à la Seq2Seq à l'agent GPT.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Un utilisateur dit "Je veux changer mon vol". Le système doit comprendre ce qu'il veut, quelles informations manquent, comment l'obtenir et comment terminer l'action.

> L'utilisateur dit "je veux changer de vol ?" Le système doit comprendre ce qu'il veut, ce qu'il manque d'information, comment obtenir, comment terminer l'opération.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

La conversation est difficile pour un système ML. L'entrée est ouverte. La sortie doit être cohérente sur plusieurs tours. Le système peut avoir besoin d'agir sur le monde (changement de vol, charge d'une carte). Chaque mauvaise étape est visible à l'utilisateur.

> Pour les systèmes ML, il est difficile de parler. L'entrée est ouverte. La sortie doit être maintenue en plusieurs rounds. Le système peut avoir besoin d'une action contre le monde.

Les architectures de chatbot ont fait le tour de quatre paradigmes, chacun introduit parce que le précédent a échoué trop visiblement. Cette leçon les accompagne dans l'ordre.

> L'architecture de l'ordinateur a connu quatre types de façons, chacune étant due à l'échec du premier type, qui est trop évident pour être introduit.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

### Le demi-siècle écrit, 1950-2001

Le premier paradigme n'a pas duré cinq ans. Il a duré cinquante. Savoir son arc compte parce que chaque système en lui est la même machine  correspond à l'entrée, émet une réponse en conserve, met à jour un petit état  et cinquante ans d'ajout de règles à cette machine n'ont jamais produit le cas général. Ce plafond est pourquoi les paradigmes de deux à quatre existent.

**1950.**Turing échappe à la question de savoir si les machines peuvent penser en proposant un substitut opérationnel: si un interrogateur ne peut pas distinguer la machine d'une personne par télétype, la question philosophique est discutable.

**1956.**Le nom de l'atelier d'été à Dartmouth est "intelligence artificielle" sur la supposition que chaque caractéristique de l'intelligence "peut en principe être décrite si précisément qu'une machine peut être fabriquée pour la simuler".

**1966.**ELIZA envoie le truc de réflexion que vous construisez dans l'étape 1: les règles de décomposition tirent des fragments de l'entrée, les règles de réassemblage les font écho en tant que questions.

**1972.**PARRY, construit à Stanford pour modéliser la paranoïa, ajoute la pièce dont ELIZA manquait: l'état intérieur. Les variables numériques pour la peur, la colère et la méfiance se mettent à jour à chaque tournant et à chaque porte où le script est lancé ensuite, de sorte que les entrées identiques produisent des réponses différentes selon la conversation jusqu'à présent. Dans un test de transcription aveugle, les psychiatres ont distingué PARRY des patients humains au hasard. C'est l'ancêtre direct du conditionnement de personnalité  un système de prompt mis en œuvre en trois floats. La même année, les deux robots se sont pointés vers l'autre sur ARPANET: un script de thérapeute interviewé par une machine d'état paranoïaque, la première conversation bot-to-bot sur un réseau.

**1995.**ALICE étalonne la recette ELIZA avec AIML, un dialecte XML pour les paires de modèles-templates. Environ 40 000 catégories écrites à la main, trois prix Loebner. Il a prouvé la loi d'étalon des systèmes basés sur des règles: plus de règles achètent la couverture, jamais la généralité. Chaque règle est une responsabilité que quelqu'un doit maintenir.

**2001.**SmarterChild met la recette devant 30 millions d'utilisateurs de messagerie instantanée et ajoute des recherches en arrière-plan  météo, actions, horaires de cinéma  enregistrés dans des modèles.

Cinquante ans, un seul mécanisme, une règle croissante compte. Le paradigme a pris fin non pas parce que quelqu'un l'a refusé mais parce que le coût de maintenance des machines d'état écrites à la main augmente linéairement avec la couverture tandis que les attentes des utilisateurs augmentent avec ce qu'ils ont vu la semaine dernière.

```figure
chatbot-lineage
```

**Rule-based (ELIZA, AIML, DialogFlow).**Les modèles écrits à la main correspondent à l'entrée de l'utilisateur et produisent des réponses. Les classifiants d'intention se dirigent vers des flux prédéfinis. Les machines de remplissage de machines à sous recueillent les informations requises. Fonctionne brillant dans le cadre étroit pour lequel elles ont été conçues. Échoue immédiatement en dehors de celui-ci.

> **基于规则（ELIZA、AIML、DialogFlow）。**Les utilisateurs ont été informés de la mise en œuvre de la méthode de réception et de la réception des données.

**Retrieval-based.**Un système de type FAQ. Encodez chaque paire de (expression, réponse). En temps d'exécution, encodez le message de l'utilisateur et récupérez la réponse stockée la plus proche. Pensez à la caractéristique classique "articles similaires" de Zendesk.

> **基于检索。**Le code de l'utilisateur est utilisé pour la réception de messages et de messages.

**Neural (seq2seq).**Le décodeur-encodeur est formé sur les journaux de conversation. Génère des réponses à partir de zéro. Fluent mais sujet à des sorties génériques ("je ne sais pas") et à des dérives factuelles.

> **神经（seq2seq）。**Le codeur-décodeur de formation en cours dans le journal de dialogue. De la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à la génération à

**LLM agents.**Un modèle de langage enveloppé dans une boucle qui planifie, appelle des outils et vérifie les résultats. Pas un chatbot avec une longue demande. Un boucle d'agent: planifier → appeler outil → observer le résultat → décider de la prochaine étape.

> **LLM Agent。**包装在循环中的语言模型,规划,调用工具并验证结果──不是带长提示的聊天机器人──一个代理 循环:规划 → 调用工具 → 观察结果 →决定下一步──检索优先定(RAG) empêcher le phénomène──工具调用让它实际做事──这就是2026年架构──

Les quatre paradigmes ne sont pas des remplacements séquentiels. Un chatbot de production 2026 traverse les quatre: une procédure basée sur des règles pour l'authentification et les actions destructives, une récupération pour les FAQ, une génération neurale pour la phrasé naturelle, un agent LLM pour les requêtes ouvertes ambiguës.

> Ce type de modèle ne remplace pas l'ordre. En 2026, les robots de production de chat sont utilisés par quatre voies: les règles de référence pour l'identification et l'opération destructive, les recherches pour les FAQ, les générations neuronales pour les phrases naturelles, les agents de l'LLM pour les recherches ouvertes à la confusion.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

### Étape 1: correspondance des modèles basés sur des règles

```python
import re


class RulePattern:
    def __init__(self, pattern, response_template):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.template = response_template


PATTERNS = [
    RulePattern(r"my name is (\w+)", "Nice to meet you, {0}."),
    RulePattern(r"i (need|want) (.+)", "Why do you {0} {1}?"),
    RulePattern(r"i feel (.+)", "Why do you feel {0}?"),
    RulePattern(r"(.*)", "Tell me more about that."),
]


def rule_based_respond(user_input):
    for pattern in PATTERNS:
        m = pattern.regex.match(user_input.strip())
        if m:
            return pattern.template.format(*m.groups())
    return "I don't understand."
```

ELIZA en 20 lignes. La ruse de réflexion ("Je me sens triste" → "Pourquoi vous vous sentez triste") est la démo de psychothérapeute canonique de Weizenbaum 1966.

> 20 行 ELIZA──反射技巧("Je me sens triste" → "Pourquoi vous vous sentez triste") est une démonstration du thérapeute psychiatrique classique de Weizenbaum en 1966.

### Étape 2: Résumé de la demande (FAQ)

Ce morceau illustratif exige`pip install sentence-transformers`Le volant.`code/main.py`pour cette leçon utilise une similitude de Jaccard stdlib à la place, donc la leçon fonctionne sans dépendances externes.

> Cet exemple de code est nécessaire.`pip install sentence-transformers`(会拉取火) │ 本课的可运行 `code/main.py`Utilisation de la bibliothèque standard Jaccard similairement au lieu, de tels cours ne nécessitent aucune dépendance extérieure.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


FAQ = [
    ("how do i reset my password", "Go to Settings > Security > Reset Password."),
    ("how do i cancel my order", "Go to Orders, find the order, click Cancel."),
    ("what is your return policy", "30-day returns on unused items, original packaging."),
]


encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_questions = [q for q, _ in FAQ]
faq_embeddings = encoder.encode(faq_questions, normalize_embeddings=True)


def faq_respond(user_input, threshold=0.5):
    q_emb = encoder.encode([user_input], normalize_embeddings=True)[0]
    sims = faq_embeddings @ q_emb
    best = int(np.argmax(sims))
    if sims[best] < threshold:
        return None
    return FAQ[best][1]
```

Le refus basé sur le seuil est le choix de conception clé.`None`et laisser le système s'escalader.

> Réjection basée sur value  est un choix de conception clé. `None`让系统升级处理──

### Étape 3: génération neuronale (ligne de base)

Utilisez un petit encodeur-décodeur ajusté aux instructions (FLAN-T5) ou un modèle de conversation ajusté. Production-inutile par lui-même en 2026 (contradiction, dérive hors sujet, absurdité factuelle), mais naviguent à l'intérieur des systèmes hybrides pour la phrasé naturelle. Les modèles de décodeur à style dialogPT ont besoin de séparateurs de tour explicites et de manœuvres EOS pour produire des réponses cohérentes; un pipeline de texte2text FLAN-T5 fonctionne à l'extérieur de la boîte pour un exemple d'enseignement.

> Utilisation de petits ordres micro-modificateur-décodeur(FLAN-T5) ou de modèles de dialogue micro-modifiés.

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### Étape 4: boucle d'agent de LLM

La forme de production de 2026:

> Forme de production de l'année 2026:

```python
def agent_loop(user_message, tools, llm, max_steps=5):
    history = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = llm(history, tools=tools)
        tool_call = response.get("tool_call")
        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments")
            if not isinstance(tool_name, str) or tool_name not in tools:
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": str(tool_name), "content": f"error: unknown tool {tool_name!r}"})
                continue
            if not isinstance(args, dict):
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": tool_name, "content": f"error: arguments must be a dict, got {type(args).__name__}"})
                continue
            fn = tools[tool_name]
            result = fn(**args)
            history.append({"role": "assistant", "tool_call": tool_call})
            history.append({"role": "tool", "name": tool_name, "content": result})
        else:
            return response["content"]
    return "I could not complete the task in the step budget."
```

Les outils sont des fonctions appelées que le LLM peut invoquer. La boucle se termine lorsque le LLM renvoie une réponse finale au lieu d'un appel à l'outil. Le budget des étapes empêche des boucles infinies sur des tâches ambiguës.

> Les trois points essentiels. Les outils sont des fonctions de MLL pouvant être utilisées.

La production réelle ajoute: la première mise à terre de récupération (injection de documents pertinents avant chaque appel de LLM), les barreaux (réjection d'actions destructives sans confirmation), l'observabilité (enregistrement de chaque étape) et les évaluations (vérification automatique du comportement des agents en fonction des spécifications).

> 实际生产还需要:检索优先定(每次 LLM 调用前注入相关文档) 护(未经确认拒绝破坏性操作) 可观测性(记录每步) 和评估(自动检查代理 行为保持规范) 

### Étape 5: routage hybride

```python
def hybrid_chat(user_input):
    if is_destructive_action(user_input):
        return structured_flow(user_input)

    faq_answer = faq_respond(user_input, threshold=0.6)
    if faq_answer:
        return faq_answer

    return agent_loop(user_input, tools, llm)


def is_destructive_action(text):
    danger_words = ["delete", "cancel", "charge", "refund", "transfer"]
    return any(w in text.lower() for w in danger_words)
```

Le modèle: des règles déterministes pour tout ce qui est destructeur, la récupération pour les FAQ en conserve, les agents de LLM pour tout le reste.

> 模式: pour toute opération destructive, pour toute question fréquente, pour toute autre utilisation d'agent LLM.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

Il est important de noter que les méthodes de routage sont généralement utilisées pour les besoins de la production.

> Dans la production, il n'y a pas de structure unique capable de traiter chaque requête.

## Les modes d'échec qui sont encore en production vont encore entrer dans le mode de défaillance de la production.

- **Confident fabrication.**L'agent de la LLM affirme avoir effectué une action qu'il n'a pas effectuée.
  **自信捏造。**L'agent de LLM affirme avoir terminé une opération non terminée.
- **Prompt injection.**L'utilisateur insère du texte qui supprime le système de demande. LLM01 classé dans le Top 10 de l'OWASP pour les applications LLM 2025. Deux saveurs: injection directe (collection dans le chat) et injection indirecte (clandestin dans les documents, les e-mails ou les sorties d'outils que l'agent lit).
  **提示注入。**Utilisateur pour insérer le système de conseils dans le texte.

  Les taux d'attaques varient selon les scénarios. Les taux de réussite mesurés varient entre 0,5-8,5% sur les modèles frontaliers dans les critères de référence généraux d'utilisation des outils et de codage. Les configurations spécifiques à haut risque (attaques adaptatives contre les agents de codage de l'IA, orchestration vulnérable) ont atteint ~84%. Les CVE de production incluent EchoLeak (CVE-2025-32711, CVSS 9.3)  une faille d'exfiltration de données en clics zéro dans Microsoft 365 Copilot déclenchée par un courriel contrôlé par l'attaquant.
  Le taux de réussite des attaques est différent selon les scénarios. Dans l'utilisation des outils généraux et le code de base, le taux de réussite des modèles de la première ligne est d'environ 0,5-8,5%.

  Atténuations: traiter les entrées utilisateur comme non fiables tout au long de la boucle; désinfecter avant les appels à l'outil; isoler les sorties de l'outil de la demande principale; utiliser le modèle Plan-Verifier-Exécuter (PVE) où l'agent planifie d'abord, puis vérifie chaque action contre ce plan avant l'exécution (ce qui empêche les résultats de l'outil d'injecter de nouvelles actions non planifiées); exiger la confirmation de l'utilisateur pour des actions destructives; appliquer le moins de privilèges aux champs d'outil.
  缓解措施: dans l'ensemble du cycle, l'utilisateur sera considéré comme incroyable; tool调用前消毒;将工具输出与主提示隔离; utiliser la planification-验证-执行 (PVE) modèle, l'agent pré- planification, puis pour chaque opération selon le plan de vérification après la réexécution (qui empêche le résultat de l'outil d'injecter de nouvelles opérations non planifiées); pour les exigences de l'utilisateur de la destruction des opérations; pour la portée de l'application des outils, le droit minimum.

  Aucune quantité d'ingénierie rapide n'élimine complètement ce risque.
  Il est impossible de supprimer complètement ce risque.
- **Scope creep.**L'agent se retire de la tâche parce qu'un appel à l'outil a rendu des informations tangentielles liées.
  **范围蔓延。**L'agent parce que les outils sont utilisés pour retourner les informations et les problèmes liés indirectement.
- **Infinite loops.**L'agent appelle toujours le même outil, l'atténuation: budget, dédoublement des appels, juge de la loi sur "on fait des progrès".
  **无限循环。**L'agent continue à utiliser les mêmes outils.
- **Context window exhaustion.**Les longues conversations poussent les premiers tours hors contexte.
  **上下文窗口耗尽。**长对话将最早轮次推出上下文──缓解: résumé de vieilles routines── selon la similitude de recherche relatives aux routines historiques──或使用长上下文模型──

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-chatbot-architect.md`- Le numéro de la liste:

> 保存为 `outputs/skill-chatbot-architect.md`- Le numéro de la liste:

```markdown
---
name: chatbot-architect
description: Design a chatbot stack for a given use case.
version: 1.0.0
phase: 5
lesson: 17
tags: [nlp, agents, chatbot]
---

Given a product context (user need, compliance constraints, available tools, data volume), output:

1. Architecture. Rule-based, retrieval, neural, LLM agent, or hybrid (specify which paths go where).
2. LLM choice if applicable. Name the model family (Claude, GPT-4, Llama-3.1, Mixtral). Match to tool-use quality and cost.
3. Grounding strategy. RAG sources, retrieval method (see lesson 14), tool contracts.
4. Evaluation plan. Task success rate, tool-call correctness, off-task rate, hallucination rate on held-out dialogs.

Refuse to recommend a pure-LLM agent for any destructive action (payments, account deletion, data modification) without a structured confirmation flow. Refuse to skip the prompt-injection audit if the agent has write access to anything.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Implémenter la réponse basée sur les règles ci-dessus avec 10 modèles pour un bot de commande de café. Cas de bord de test: double commande, modifications, annulation, intention non claire.
   **简单。**Pour les cafés, les machines et les machines peuvent répondre à ces questions en suivant les règles énoncées ci-dessus, 10 modes, et les conditions de test: répéter les commandes, modifier, supprimer, éliminer.
2. **Medium.**Construisez une FAQ hybride + LLM fallback. 50 entrées de FAQ en conserve pour un produit SaaS, LLM fallback avec récupération sur le site des documents. Mesurez le taux de refus et la précision sur 100 questions de support réelles.
   **中等。**构建混合FAQ + LLM 回退──50 个 SaaS 产品的固定FAQ 条目,LLM 回退带文档站检索──100 个真实支持问题上测量拒绝率和准确率──
3. **Hard.**Implémenter la boucle d'agent ci-dessus avec trois outils (recherche, lecture-utilisateur-données, envoyer-email). Exécuter une évaluation avec 50 scénarios de test, y compris des tentatives d'injection rapide. Rapporte le taux de hors-task, taux de défaillance de tâche, et tout succès d'injection.
   **困难。**Utilisation de trois outils (recherche, lecture, données utilisateur, envoi de courrier) pour réaliser le cycle d'agent ci-dessus.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) le papier original basé sur les règles du chatbot. / 原始基于规则的聊天机器人论文──
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) Le dernier article de Google sur le chatbot neural, juste avant que les agents de la LLM ne prennent le relais.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) le papier qui a nommé le modèle de boucle d'agent. / 命名 Agent 循环模式的论文。
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) 2024 production orientation qui est toujours valable en 2026. / 2024 年生产指南,2026 年仍然有效。
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) le papier d'injection rapide. / 提示注入论文。
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) le classement qui a fait de l'injection rapide la principale préoccupation de sécurité. / 使提示注入成为首要安全关注的排名──
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Défense pratique de la couche d'orchestration, y compris les flux de planification- vérification- exécution et de confirmation de l'utilisateur.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) le CVE canonique de clics zéro de l'exfiltration de données à partir d'une injection directe directe. cas de référence pour expliquer pourquoi les agents d'accès à l'écriture ont besoin de défense en temps d'exécution. / 间接提示注入的典型零点击数据泄露 CVE──写入权限 Agent 需要运行时防御的参考案例──
| Intent | What the user wants | Categorical label (book_flight, reset_password). Routed to a handler. |
| Slot | A piece of info | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. |
| RAG | Retrieval plus generation | Retrieve relevant docs, then ground the LLM's response. |
| Tool call | Function invocation | LLM emits a structured call with name + args. Runtime executes, returns result. |
| Agent loop | Plan, act, verify | Controller that runs LLM calls interleaved with tool calls until task complete. |
| Prompt injection | User attacks prompt | Malicious input that tries to override the system prompt. |

## Pour en savoir plus

- [Turing (1950). Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238) le document qui a fait de la conversation le point de référence du domaine.
- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) le papier original basé sur des règles.
- [Colby, Weber, Hilf (1971). Artificial Paranoia](https://doi.org/10.1016/0004-3702(71)90002-6)  L'architecture parallèle à l'affection de PARRY, le premier chatbot à l'état.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239)Le dernier article sur le chatbot neuronal de Google, juste avant que les agents de la LLM ne prennent le relais.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)Le papier qui a nommé le modèle de boucle d'agent.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) L'orientation de production de 2024 qui est toujours valable en 2026.
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) le papier d'injection rapide.
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) le classement qui a fait de l'injection rapide la principale préoccupation de sécurité.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Des défenses pratiques de la couche d'orchestration, y compris les flux de planification- vérification- exécution et de confirmation par l'utilisateur.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) le CVE canonique d'exfiltration de données par clic zéro à partir d'injection directe directe.
