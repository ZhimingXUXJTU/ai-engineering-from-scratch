# Agents multimodels et utilisation informatique (Capstone) 

> Le produit frontier 2026 est un agent multimodal qui lit des captures d'écran, clique sur des boutons, navigue sur les interfaces Web, remplit des formulaires et complète des flux de travail de bout en bout. SeeClick et CogAgent (2024) ont prouvé que la première étape de l'interface graphique était la mise en terre. Ferret-UI a ajouté mobile. ChartAgent a introduit l'utilisation d'outils visuels pour les graphiques. VisualWebArena et AgentVista (2026) sont les points de référence de la poursuite frontalière  et même Gemini 3 Pro et Claude Opus 4.7 score ~30% sur les tâches difficiles d'AgentVista. Cette pierre angulaire regroupe tous les fils de la phase 12: la perception (VLM haute résolution), le raisonnement (LLM avec utilisation d'outils), la mise à terre (sortie de coordonnées), la mémoire à long horizon et l'évaluation.

> **【中文解读】**Le premier produit de 2026 est capable de lire des clichés, des clichés, des pages de navigation, des formulaires, des modèles de travail à terme. SeeClick et CogAgent prouvent que la GUI est disponible, que la Ferret-UI est étendue au mobile, que le ChartAgent introduit des outils visuels. Mais dans les tâches difficiles d'AgentVista, même les Gemini 3 Pro et Claude Opus 4.7 ne passent que 30% de la réussite.

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

>  **【前置】**學本節前請先掌握:Phase 12 全部(VLM 演进) 、Phase 14·01-10(Agent 循环、工具调用) 、Phase 14·30+(工作台系列 Agent 实践) ⋅本节是Phase 12 的毕业课所有多模态 + Agent 技术整合成一个能操作电脑的产品──
>  **【类比】**À partir de la première étape, le programme de formation est mis en œuvre pour la réalisation de la mission de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de la formation de l'équipe de formation de formation de la formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation.
> ️ **【易错点】**让 Agent 直接执行动作不设人工审核 = 灾难(可能误转账、错删除) 修复:所有"破坏性动作" (→ All actions) 👇点击提交、确认、删除按) 必须人类审核或干运行 模式。

## Objectifs d'apprentissage

- Conception d'un boucle d'agent multimodal: percevoir → raison → action → observer → répétition.
  设计多模态 Agent 循环:感知 → 推理 → 行动 → 观察 → 重复。
- Construisez un schéma de sortie de mise à terre de l'interface graphique (coordonnées de clic, texte de type, défilement, glisser) que le VLM peut émettre sous forme de JSON.
  构建 GUI 定位输出模式(点击坐标、输入文字、滚动、拖),VLM 以 JSON 格式输出──
- Comparer les agents à capture d'écran seulement avec les agents à arbres d'accessibilité avec les agents hybrides.
  Comparé à l'agent pur de coupe, l'agent sans obstacle et l'agent mixte
- Configurez une évaluation de référence multimodale sur une petite tranche de VisualWebArena.
  En vue de la mise en place d'une nouvelle stratégie de développement de l'entreprise, les entreprises doivent être en mesure de faire des efforts pour améliorer la qualité de leur service.

## Le problème est défini .

> **【中文解读】**Pour le cas échéant, l'agent doit extraire une page du navigateur, extraire une image + URL + objectif générateur, extraire un mouvement structuré, cliquer sur le bouton de réception, faire un déplacement sur le navigateur, observer un nouveau statut, faire un cycle jusqu'à la fin de la tâche.

Un flux de travail sur le site de réservation: " Trouvez-moi un vol pour Tokyo pour le 15 avril, siège d'allée sous 800 $, réservez-le. "

> Un ordinateur de travail: "Aide-moi à trouver le 15 avril, vol à Tokyo, par la route, 800 $ 以下, pré-commande !"

Un agent multimodal doit:

> À l'aide de l'agent:

1. Prenez une capture d'écran du navigateur.
   Le texte de la lettre de la première lettre est écrit en français.
2. Parser la capture d'écran + URL + objectif dans un plan.
   Le mot de passe est "plan de création".
3. Émettez une action structurée: cliquez (à x,y), tapez "Tokyo" (à l'élément E), faites défiler vers le bas, sélectionnez (bouton radio).
   Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
4. Appliquez l'action au navigateur.
   En français, traduit par " faire un geste "
5. Observez l' état nouveau (prochain capture d' écran).
   Le texte est en français.
6. Répétez jusqu'à ce que la tâche soit terminée.
   Le récit de la première partie de la série est écrit en français.

Chaque étape est un appel VLM multimodal. La sortie VLM doit être JSON parseable. Les erreurs se composent à travers les étapes, donc la récupération est importante.

> Chaque étape est une fois un multiple mode VLM 调用──VLM 输出 必须是可解析的 JSON──错误在步骤间累积,因此恢复机制至关重要──

## Le concept de base.

> **【中文解读】**L'Agence de l'utilisation informatique permet à l'IA d'opérer directement l'interface informatique: c'est une application finale de l'AI qui peut non seulement comprendre l'image, mais aussi exécuter des tâches dans l'interface graphique.

> **【拓展：Computer Use 的前沿**L'utilisation de l'ordinateur de l'Anthropic 让 Claude 直接操作桌面应用,完成网页浏览、表单填写等任务──OpenAI Operator 使用类似方法──关键技术挑战:精确定位──准确点击按)、状态跟踪──理解界面变化──错误恢复──操作失败后重试──


### L'interface graphique à terre  le primitif  l'interface graphique 定位 基础原语

La mise à terre de l'interface graphique est: donné un capture d'écran et une instruction de langage naturel, sortez la coordonnée (x, y) pour cliquer (ou autre action).

> GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作)

> **【中文解读】**GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作) ――SeeClick est le premier grand ouverture de résultats,CogAgent 增加了1120x1120高分辨率编码,Ferret-UI 聚焦移动端 UI──输出格式通常是JSON,`element_desc`字段帮助恢复当坐标在截图间漂移时,语义提示让系统重新定位──

SeeClick (arXiv:2401.10935) est le premier résultat ouvert à l'échelle: affiner un VLM sur des données GUI synthétiques + réelles, les coordonnées de sortie en tant que jetons de texte ordinaires.

> SeeClick est le premier grand ouverture de résultats: dans synthèse+ vraies données GUI sur micro-modulation VLM, à partir de texte pur jeton 输出坐标──有效──.

CogAgent (arXiv:2312.08914) a ajouté 1120x1120 de haute résolution de codage pour les interfaces utilisateurs denses. Score: ~84% sur la navigation Web.

> CogAgent pour l'interface utilisateur plus étroite ajouté 1120x1120 code de haute résolution.

Ferret-UI (arXiv:2404.05719) se concentre sur les interfaces mobiles, s'intègre avec les données d'accessibilité iOS.

> Ferret-UI 聚焦移动端 UI, intégré iOS 无障碍数据──

Le format de sortie est généralement JSON:

> 输出格式 est généralement JSON:

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

Le `element_desc`aide à la récupération: si les coordonnées dérivent entre les captures d'écran, l'indice sémantique permet au système de replanter.

> `element_desc`帮助恢复: si le sit-geon se déplace dans le schéma, le système peut être réaffecté.

### Des plans d'action.

Un schéma d'action typique comporte 6 à 10 types d'action:

> Le modèle d'action typique comprend 6 à 10 types d'action:

> **【中文解读】**Le modèle de mouvement typique comprend 6 à 10 types de mouvement: cliquez sur le bouton de touche, type, type, défilement, défilement, tirage, sélection, sélection, défilement, navigation, attente, réalisation, réalisation.

- `click`Les points suivants:
  Le mot grec traduit par " le mot grec "`click`:点击 (x, y)
- `type`: (texte, x?, y?)
  Le mot grec traduit par " le mot grec "`type`:输入文本,可选位置──
- `scroll`: (direction, montant)
  Le mot grec traduit par " le mot grec "`scroll`Il est très important de savoir comment faire.
- `drag`Les produits de la production de produits de haute qualité
  Le mot grec traduit par " le mot grec "`drag`: de (x0, y0) 拖到 (x1, y1)
- `select`: (option_index)
  Le mot grec traduit par " le mot grec "`select`: sélectionner les éléments de sélection
- `hover`Les points suivants:
  Le mot grec traduit par " le mot grec "`hover`: suspen (x, y)
- `navigate`- Je suis désolé.
  Le mot grec traduit par " le mot grec "`navigate`Pour le navigateur:
- `wait`Les résultats de l'enquête
  Le mot grec traduit par " le mot grec "`wait`Attends quelques secondes.
- `done`: (succès, explication)
  Le mot grec traduit par " le mot grec "`done`Pour le moment, je suis en train de faire une petite histoire.

L'agent émet une action par étape. L'enveloppe du navigateur exécute et renvoie l'état nouveau.

> Agent chaque étape de la sortie d'un mouvement.

### - Je ne peux pas le faire.

> **【中文解读】**两种输入模式: pure截图模式最通用但精度较低;无障碍树(DOM/iOS 无障碍信息) plus fiable mais seulement disponible dans les données structurées; mixed mode simultanément utilisé,树用于原子动作定位,截图用于语义理解;;生产 Agent 尽可能使用混合模式;;

Deux modes d'entrée:

> 两种输入模式:

- Capture d'écran seulement: image complète, aucune information structurelle.
  Le texte est en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français,
- Arbre d'accessibilité: informations structurées sur l'accessibilité DOM / iOS. Beaucoup plus fiable pour la mise à terre; fonctionne lorsque l'arbre est disponible.
  Le site Web de l'entreprise est un site Web de services de téléphonie mobile.
- Hybride: les deux, avec l'arbre comme fondateur fiable pour les actions atomiques et la capture d'écran pour le contexte sémantique.
  Le mot "réaction" est utilisé pour désigner le type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type de type

Les agents de production utilisent des hybrides lorsque cela est possible. L'automatisation du navigateur (Sélénium + accessibilité) a toujours l'arbre; les applications de bureau le font parfois.

> Produit d'un produit à l'aide de l'agent de production 尽可能使用混合模式;;

### Je ne sais pas si tu peux m'aider.

Un flux de travail de 20 étapes génère 20 captures d'écran. Le contexte du VLM se remplit rapidement.

> 20 步工作流产生 20 张截图──VLM 上下文快快填满──三种压缩策略:

> **【中文解读】**20 步工作流产生 20 张截图,VLM 上下文很快填满──三种缩写策略:摘要链(每5 步总结一次,丢弃旧截图)、跳(保留首尾和每第3 张)、工具记录日志(只保留文本日志不看旧截图)──Claude's computer use API 使用日志模式,更简单可靠──

- Chaîne de résumé: après chaque 5 étapes, résumer ce qui s'est passé, laisser tomber les anciens captures d'écran.
  Chaque 5 étapes résument ce qui s'est passé, en abandonnant l'ancien cliché.
- Skip-frame: conservez la première, la dernière et chaque troisième capture d'écran.
  Le texte est en français: "Retention de la première, dernière et troisième partie".
- Log enregistré par l'outil: exécuter des actions, garder un journal texte de ce qui a été fait; ne regardez pas à nouveau les anciens captures d'écran.
  Le texte de la première partie est écrit en français.

L'API de Claude utilise le modèle du journal, plus simple et plus fiable.

> L'ordinateur de Claude utilise une API.

### Utilisation d' outils visuels Utilisation d' outils visuels

> **【中文解读】**L'agent peut alors exporter "région de coupe (100,200,300,400) puis utiliser OCR" comme outil de coupe.

L'agent de graphique (arXiv:2510.04514) introduit l'utilisation d'outils visuels pour la compréhension des graphiques: crop, zoom, OCR, appel de détection externe. L'agent peut exécuter "crop to region (100, 200, 300, 400) puis appeler OCR" comme appel d'outil. L'outil renvoie du texte; le VLM continue à raisonner.

> L'agent peut exporter "couper à la région (100, 200, 300, 400) puis utiliser l'OCR" comme outil de référencement.

Ce modèle généralise: l'interrogatoire de marque, l'annotation de région et les outils de détection externes correspondent tous au même schéma "expédier un appel d'outil, recevoir une réponse structurée".

> Ce modèle peut être promu: les indicateurs de collecte, les indicateurs régionaux et les instruments de test externes sont adaptés au même mode de "formation des outils de sortie, de réception et de réaction structurée".

### Les critères de référence de 2026

> **【拓展：多模态 Agent 基准全景】**ScreenSpot-Pro 测试 GUI 定位(open模型 ~85%,前沿 ~90%);VisualWebArena 测试端到端网页任务(open模型 ~20%,Gemini 3 Pro ~27%);AgentVista est le 2026 le dernier marché de l'emploi, couvrant 12 domaines de travail réels, le modèle de première ligne est de seulement 27 à 40%;WebArena/WebShop 已被前沿模型和──

- ScreenSpot Pro. L'interface graphique est basée sur environ 1 000 captures d'écran Web.
  Le code de la page est basé sur le code de la page d'accueil.
- VisualWebArena. tâches Web de bout en bout (boutique, forum, annonces classifiées). SOTA ouvert ~ 20%. Gemini 3 Pro ~ 27%.
  Le site Web est en train de devenir un site Web de télévision.
- AgentVista (arXiv:2602.23166). Le point de référence le plus difficile de 2026. Flux de travail réaliste sur 12 domaines. Modèles frontaliers score 27-40%; modèles ouverts 10-20%.
  Le modèle de travail de l'entreprise est le plus difficile de l'année 2026.
- WebArena / WebShop. Les critères de référence plus anciens; saturés par frontière.
  Le site WebArena / WebShop.

### Pourquoi c'est toujours difficile pourquoi c'est toujours difficile

> **【中文解读】**1) 细粒度视觉定位("点击小 X"在移动分辨率下经常失败);2) 长期规划(10 步后 Agent 偏离目标);3) 错误恢复(点击失败时检测和恢复缺乏训练数据);4) 跨页面上下文(跳转标签页面或长表单丢失状态) ――研究方向包括记忆架构、、式重规划多样式验证――

Les écarts de performance des agents:

> Agents de performance:

1. "Cliquez le petit X" échoue souvent à la résolution mobile.
   Le " petit X " est souvent défait en résolution mobile.
2. Après 10 actions, l'agent dérive de la cible.
   Le groupe de travail est un groupe de travail de longue durée.
3. Rétablissement d'erreur. Lorsqu'un clic échoue (tous bons), la détection + récupération est rarement une formation de données.
   En français, le mot "rétablissement" signifie "rétablissement" ou "rétablissement".
4. Le saut entre onglets ou longs formulaires perd son état.
   Le texte de la lettre de la première lettre est écrit en français.

Directions de recherche: architectures de mémoire, replanification explicite, vérification multimodal (écran correspondant à la réussite de l'action).

> Les résultats de l'étude ont été obtenus en 1er janvier.

### Le projet de construction de la pierre angulaire.

> **【中文解读】**毕业项目任务: construire un ordinateur utilisant Agent, être capable de lire un pré-résumé du site Web, de créer un HTML+ de la page, de planifier plusieurs étapes de séquences, de faire des recherches, de produire des JSON de la correspondance et d'évaluer 10 tâches fixes.

La tâche principale: construire un agent d'utilisation informatique qui:

> 毕业项目任务: construire un ordinateur utilisant un agent, exigences:

1. Lisez le capture d'écran HTML + d'une page de simulation du site de réservation.
   Le texte de la page de l'éditeur est en français.
2. Planifie une séquence en plusieurs étapes: recherche → sélection → remplissage du formulaire → soumission.
   Le nom de l'équipe de formation est le nom de la société.
3. Émet des actions JSON correspondant au schéma d'action.
   Le modèle JSON 动作.
4. Évalué sur une tranche fixe de 10 tâches.
   En français, on peut lire:

La leçon fournit un code d'échafaudage facile à étendre dans un navigateur réel.

>  cours fournissent des codes de script, faciles à étendre à un vrai navigateur.

## Utilisez-le avec le cadre de réalisation
```figure
mm-agent-loop
```

## Utilisez-le

`code/main.py`est l'échafaudage en pierre de taille:

- Définition JSON du schéma d'action (10 actions).
  Le modèle de démarche de la société est le modèle de démarche de la société.
- Faux état de navigateur comme dicté.
  Le mot "c'est-à-dire " est traduit par "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "est-à-dire "est-à-dire" est traduit par "est-à-dire "est" est traduit par "est-à-dire "est" est traduit par " est traduit par "
- Le squelette de boucle d'agent: état de réception, émission d'action, application, boucle.
  Le cycle de l'agent: état de réception, de sortie, d'exécution, de cycle.
- Un mini-benchmark de 10 tâches (pages synthétiques) pour mesurer le taux de réussite de bout en bout.
  Le taux de réussite de la tâche est de 10%.
- Crochet de récupération d'erreur pour une action échouée.
  Le mot "rétablissement" est traduit par "rétablissement" en français.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-multimodal-agent-designer.md`. Compte tenu d'un produit d'utilisation informatique (domaine, ensemble d'action, cible d'évaluation), il conçoit la boucle complète de l'agent, la stratégie de mémoire, le mode de mise à terre et le score de référence attendu.

> 本课产 出 `outputs/skill-multimodal-agent-designer.md` déterminer les produits utilisés par les ordinateurs dans le domaine, les actions, les objectifs d'évaluation), concevoir un cycle complet d'agent, des stratégies de mémoire, des modes de positionnement et des prévisions de base.

## Les exercices

1. Élargir le schéma d' action avec un `screenshot_region`outil (crop + zoom). Quelles tâches sont utiles ?
   扩展动作模式, ajouter `screenshot_region`工具(裁剪+缩放) ◊ Quelles tâches seront bénéfiques ?

2. Lisez AgentVista (arXiv:2602.23166). Décrivez la catégorie de tâches la plus difficile et pourquoi les modèles frontaliers échouent toujours.
   阅读 AgentVista 论文── décrit les catégories de tâches les plus difficiles ainsi que les raisons pour lesquelles le modèle avant-coureur échoue encore──

3. Compression de la mémoire à long horizon: concevoir une chaîne de synthèse avec ≤4 captures d'écran maintenues en direct, n'importe quel numéro enregistré.
   长期记忆压缩: concevoir une chaîne de résumé, maintenir ≤4 张截图活跃, enregistrer jusqu'à jour.

4. Construire un crochet de récupération d'erreur: en cas d'échec de l'action (bouton non trouvé), que fait ensuite l'agent ?
   构建错误恢复子:当动作失败 (按未找到) 当,Agent Next step doing what?

5. Comparer Claude 4.7 à écran hybride + arbre d'accessibilité Qwen2.5 VL sur 10 tâches Web.
   Comparé à la performance de Claude 4.7 sur 10 missions en ligne par rapport au mode mixte Qwen2.5 VL, quelles missions ont été remportées par les différents types de missions ?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Encore une lecture

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
