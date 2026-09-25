# Les études de cas et l' état de l' art 2026

> Trois références de la classe de production à l'étude de bout en bout, chacune illustrant une tranche différente de l'ingénierie multi-agent. **Anthropic's Research system**(travailleur d'orchestre, jetons 15x, +90,2% sur les déploiements d'Opus 4 à agent unique) est le cas canonique de superviseur. **MetaGPT / ChatDev**(SOP-encodé spécialisation des rôles pour l'ingénierie logicielle; "déhallucination communicative" de ChatDev; extension MacNet à >1000 agents via DAGs, arXiv:2406.07155) est le cas canonique de décomposition des rôles. **OpenClaw / Moltbook**(originellement Clawdbot par Peter Steinberger, novembre 2025; renommé deux fois; 247k GitHub stars en mars 2026; agents locaux ReAct-loop; Moltbook comme un réseau social à but non lucratif avec ~2,3M comptes d'agents dans les jours suivant le lancement, acquis par Meta 2026-03-10) illustre ce qui se passe à l'échelle de la population: activité économique émergente, risques d'injection rapide, réglementation au niveau de l'État (la Chine a restreint OpenClaw sur les ordinateurs gouvernementaux, mars 2026).**Framework landscape April 2026:**LangGraph et CrewAI sont les principaux producteurs; AG2 est la suite de la communauté AutoGen; Microsoft AutoGen est en mode maintenance (fusé dans Microsoft Agent Framework, RC Feb 2026); OpenAI Agents SDK est le successeur de production Swarm; Google ADK (avril 2025) est le participant natif A2A. Chaque cadre majeur fournit maintenant un support MCP; la plupart fournissent un support A2A. Cette leçon lit chaque cas de bout en bout et distille les schémas communs afin que vous puissiez choisir la bonne référence pour votre prochain système de production.

> **【中文解读】**Ce chapitre présente l'analyse des cas de SOTA multi-agent de 2026  les meilleurs systèmes multi-agent 

> **【拓展：case studies 2026 sota→具体应用】**2026 ans SOTA 多 Agent 系统案例: 1) Claude Research 多 Agent de l'Anthropic  collaboration pour mener des recherches approfondies; 2) Code 多 Agent 协作编码 de l'OpenAI; 3) Microsoft AutoGen 团队 多 Agent 软件开发──共同趋势:专业化分工、层次化编排、MCP 工具使用和 A2A Agent 间通信的结合──


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**Le programme est en phase 16 收官课,整合 01-24 所有内容──三生产级案例:Anthropic Research (en anglais seulement) Supervisor 典范) MetaGPT/ChatDev (en anglais seulement) 角色分工典范) OpenClaw (en anglais seulement) Moltbook (en anglais seulement) 群体规模涌现典范) 
>  **【类比】**Trois cas = " trois types de sociétés multi-agents "―Réservation anthropique = 精小队 (en anglais: 精小队) 10 个 代理,深度研究);MetaGPT = 标准开发团队 (en anglais: 标准开发团队) 角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会 (en anglais: 百万 Agent 涌现经济、被政府监管)―2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen
**Time:** ~90 minutes | **时间:** ~90 分钟

## ♪ Problème ♪ Introduction du problème ♪

L'ingénierie multi-agents est une discipline jeune. Les références de production sont rares et couvrent chacune une partie différente de l'espace. Il est utile de les lire une à la fois; il est plus utile de les comparer en série. Cette leçon traite trois études de cas canoniques de 2026 comme une liste de lecture de bout en bout, pince les schémas communs et cartographies du paysage de cadre afin que vous puissiez faire des choix de cadre à partir de la connaissance, pas du marketing.

> L'ingénierie en agent est une discipline de formation très jeune. Les références de production sont très peu nombreuses, chaque partie de l'espace est couverte.

## Concept Le concept central

### Système de recherche anthropologique

Le cas des superviseurs de production. Claude Opus 4 planifie et synthétise; Claude Sonnet 4 recherche en parallèle.https://www.anthropic.com/engineering/multi-agent-research-system.

Résultats de mesure clés:

> 关键测量结果:

- **+90.2%**amélioration par rapport à l'Opus 4 sur les évaluations internes de la recherche par un seul agent.
  En français, le nombre de personnes concernées est de 5 à 6 ans.**+90.2%**Il y a une autre.
- **80% of BrowseComp variance**expliqué par **token usage alone** Le multi-agent gagne en grande partie parce que chaque subagent obtient une nouvelle fenêtre de contexte.
  Le mot grec traduit par " le mot grec "**80% 的 BrowseComp 方差**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             **token 使用量**解释多 代理 胜出主要因为每个子 代理 获得新的上下文窗口──
- **15x tokens per query**contre un agent unique.
  Le mot "quête" est traduit par "question".**15 倍 token**contre un seul agent.
- **Rainbow deployment**Parce que les agents sont longs et états.
  Le mot grec traduit par " le mot grec "**彩虹部署**Parce que l'agent est en état de fonctionnement et de longue durée.

Les cours de conception codifiés:

> 编码化的 design training:

1. **Scale effort to query complexity.**Simple → 1 agent avec 3 à 10 appels d'outils. moyen → 3 agents. recherche complexe → 10+ subagents.
   Le mot grec traduit par " le mot grec "**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**Les subagents effectuent des recherches approfondies; le plomb est synthétisé; les subagents de suivi effectuent des recherches approfondies ciblées.
   Le mot grec traduit par " le mot grec "**先广后窄。**子 Agent faire une recherche étendue; principal agent 综合; suivants agent faire un détail
3. **Rainbow deploys.**Gardez les anciennes versions en vie jusqu'à ce que leurs agents en vol soient terminés.
   Le mot grec traduit par " le mot grec "**彩虹部署。**Restez actif jusqu'à ce que l'agent en cours de réalisation soit terminé.
4. **Verification is not optional.**Le système a été observé pour halluciner sans rôles explicites de vérificateur.
   Le mot grec traduit par " le mot grec "**验证不是可选的。**Le système est observé en l'absence de rôle de vérificateur explicite.

Il s'agit du cas de référence pour la topologie des travailleurs en charge (phase 16 · 05) à l'échelle de la production.

### MetaGPT / ChatDev

Le cas de décomposition du rôle de production SOP couvre arXiv:2308.00352 (MetaGPT) et arXiv:2307.07924 (ChatDev).

MetaGPT encode les SOP de l'ingénierie logicielle comme des instructions de rôle: Gérant de produit, architecte, chef de projet, ingénieur, ingénieur de QA.`Code = SOP(Team)`. Chaque rôle dispose d'un prompt étroit et spécialisé; les délivrances inter-rôles portent des objets structurés (documents de RPD, documents d'architecture, code).

Contribution de ChatDev: **communicative dehallucination**.Les agents demandent des détails avant de répondre  un agent de conception demande au programmeur quel langage est prévu avant de dessiner l'interface utilisateur, plutôt que de deviner.

MacNet (arXiv:2406.07155) étend ChatDev à **>1000 agents via DAGs**. Chaque nœud DAG est une spécialisation de rôle; les bords codent les contrats de transfert.

Les leçons de conception:

> 设计教训:

1. **Structure matters more than size.**Une équipe de 5 rôles est plus forte qu'un groupe de 50 agents non structurés.
   Le mot grec traduit par " le mot grec "**结构比规模更重要。**紧的 5 角色 SOP 团队胜过50 团队非结构化组的代理
2. **Handoff contracts in writing.**Les objets passés entre les rôles suivent un schéma.
   Le mot grec traduit par " le mot grec "**书面交接契约。**Le produit du rôle de la transmission suit le mode.
3. **Communicative dehallucination**est un modèle bon marché et porteur de charges.
   Le mot grec traduit par " le mot grec "**交际去幻觉**C'est un modèle bon marché.
4. **DAGs scale further than chat.**Quand le flux est reconnaissable, encodez-le.
   Le mot grec traduit par " le mot grec "**DAG 比聊天扩展更远。**Quand le processus est connu, c'est le code.

Il s'agit du cas de référence pour la spécialisation des rôles (phase 16 · 08) et la topologie structurée (phase 16 · 15).

### Écosystème OpenClaw / Moltbook

Le cas de la production à l'échelle de la population.

- **Nov 2025:**Les navires de Clawdbot (l'agent de codage local de Peter Steinberger)
- **Dec 2025 – Mar 2026:**renommé deux fois (Clawdbot → OpenClaw → continué sous OpenClaw).
- **Feb 2026:**Moltbook est lancé comme un réseau social uniquement pour les agents sur les mêmes primitifs; ~ 2,3 millions de comptes d'agents en quelques jours.
- **Mar 2026 (2026-03-10):**Meta acquiert Moltbook.
- **Mar 2026:**La Chine restreint OpenClaw sur les ordinateurs du gouvernement.
- **Mar 2026:**OpenClaw traverse 247 000 étoiles de GitHub.

Voici à quoi ressemble le multi-agent quand on met des millions d'agents sur un substrat partagé:

- **Emergent economic activity.**Les agents achètent, vendent et servent les uns les autres en utilisant des paiements par jeton.
- **Prompt-injection risks at population scale.**Un prompt malveillant dans un profil d'agent viral se propage à des milliers d'interactions d'agent à agent en quelques heures.
- **State-level regulatory response.**Dans les semaines qui suivent le lancement, la réglementation atteint l'écosystème.

Les leçons de conception tirées de ce cas sont en partie techniques, en partie de gouvernance:

1. **Multi-agent at population scale is a new regime.**Les meilleures pratiques individuelles (vérification, clarté de rôle) sont toujours applicables, mais ne sont pas suffisantes.
2. **Prompt injection is the new XSS.**Traiter les profils d'agents et les messages interagents comme des entrées non fiables par défaut.
3. **Regulation is faster than design cycles.**Planifiez-le.
4. **Open-source + viral scale compounds.**247 000 étoiles en 4 mois est inhabituel; conception pour déploiement-explosion-charge.

Regardez ![OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)Pour les bases techniques, les repositories Clawdbot / OpenClaw exposent la boucle locale ReAct; les messages publics de Moltbook révèlent l'architecture du graphique social en haut.

### Paysage cadre avril 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

Chaque cadre majeur est maintenant des navires .**MCP**soutien; la plupart des navires **A2A**La compatibilité du protocole n'est plus un facteur de différenciation.

### Les schémas communs dans les trois cas

1. **Orchestrator + workers**(superviseur explicite anthropic, PM-as-superviseur MetaGPT, agents individuels OpenClaw + effets réseau).
   Le mot grec traduit par " le mot grec "**编排者 + 工作者**(Anthropic 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立 Agent + 网络效应)
2. **Structured handoff contracts**(des descriptions de tâches sous-agents anthropiques, documents de PRD/architecture MetaGPT, objets OpenClaw A2A).
   Le mot grec traduit par " le mot grec "**结构化交接契约**(Agent anthropique 任务描述,MetaGPT PRD/架构文档,OpenClaw A2A 制品)
3. **Verification as first-class role**(Vérificateur d'Anthropic, ingénieur de QA de MetaGPT, validateurs en réseau d'OpenClaw).
   Le mot grec traduit par " le mot grec "**验证作为一等角色**(Anthropic 的验证器,MetaGPT 的 QA 工程师,OpenClaw 的网络内验证器)
4. **Scaling is topology + substrate, not just more agents**(déploiements d'arc-en-ciel, MacNet DAGs, sous-strates à l'échelle de la population).
   Le mot grec traduit par " le mot grec "**扩展是拓扑 + 基底，不仅是更多 Agent**(L'équipe de la police, MacNet DAG, groupe de taille)
5. **Cost is material and disclosed**(15x tokens, budget par rôle dans MetaGPT, prix par interaction dans Moltbook).
   Le mot grec traduit par " le mot grec "**成本是实质性的且已披露**Les prix de vente sont fixés à 15 fois, le budget de chaque rôle de la METAGPT, le prix de chaque interaction dans le Moltbook.
6. **Security posture is explicit**(L'anthropic sandboxing, les restrictions de rôle de MetaGPT, l'injection rapide d'OpenClaw comme surface d'attaque connue).
   Le mot grec traduit par " le mot grec "**安全态势是显式的**(Anthropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### Choisir une référence pour votre prochain projet

- **Production research / knowledge task → Anthropic Research.**Les subagents de nouveau contexte gagnent.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**Rôle + SOP + contrats de transfert.
- **Network-effect social product → OpenClaw / Moltbook.**Substrate + économie émergente.
- **Classic enterprise automation → CrewAI or LangGraph**(leader de production, durée de fonctionnement stable).

### Le résumé de l'état de l'art de 2026

Où se trouve le champ en avril 2026:

- **Frameworks are converging.**Le support MCP + A2A est des mises à table.
- **Evaluation is hardening.**Le SWE-bench Pro, le MARBLE, le STRATUS, est le test de réalité résistant à la contamination.
- **Production failure rates are measurable**Le domaine est sorti de l'ère de "l'apparence parfaite en démo".
- **Cost is the central engineering constraint.**Les prix des jetons par tâche, les prix des cloches murales par interaction, les coûts de déploiement de l'arc-en-ciel.
- **Regulation is a near-term input, not a background concern.**Les juridictions se déplacent plus vite que les cycles de déploiement individuels.

## Utilisez-le.
```figure
a5-orchestrator-scale
```

## Utilisez-le

`outputs/skill-case-study-mapper.md`est une compétence qui lit une conception de système multi-agents proposée et la trace à l'étude de cas la plus proche, en faisant apparaître les décisions de conception que l'étude de cas a déjà testées.

## Envoyez-le en ligne .

Règles de lancement pour la production multi-agent en 2026:

- **Start from a case study, not from scratch.**Choisissez le plus proche de la recherche anthropologique / MetaGPT / OpenClaw et adaptez-vous.
  Le mot grec traduit par " le mot grec "**从案例研究开始，不是从零开始。**选择最接近的人类研究 / MetaGPT / OpenClaw 并适配──
- **Adopt MCP + A2A.**La portabilité entre les cadres est précieuse; le support du protocole est gratuit.
  Le mot grec traduit par " le mot grec "**采用 MCP + A2A。**La portativité du cadre est précieuse; le support du protocole est gratuit.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**Il est contaminé.
  Le mot grec traduit par " le mot grec "**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**Vérifie 已被污染──
- **Pay the verification tax.**Un vérificateur indépendant coûte ~20-30% de votre budget de jeton et achète une précision mesurable.
  Le mot grec traduit par " le mot grec "**支付验证税。**Les tests indépendants coûtent environ 20-30% du budget des jetons, en échange de la validité de la mesure.
- **Rainbow deploy long-running agents.**Les courses d'agents à plusieurs heures deviennent une routine.
  Le mot grec traduit par " le mot grec "**彩虹部署长时间运行 Agent。**L'agent de l'agence est un habituel.
- **Read WMAC 2026 and the MAST follow-ups.**La discipline bouge rapidement.
  Le mot grec traduit par " le mot grec "**阅读 WMAC 2026 和 MAST 后续。**Cette discipline est en pleine croissance.

## Les exercices

1. Lisez le système de recherche anthropologique de bout en bout. Identifiez trois décisions de conception qui changeraient si vous remplaciez Opus 4 par un modèle plus petit (par exemple, Haiku 4).
2. Lisez les sections 3-4 du MetaGPT (arXiv:2308.00352). Encodez un SOP à partir de votre propre domaine (pas un logiciel) comme des instructions de rôle.
3. Lisez ChatDev (arXiv:2307.07924). Identifiez le mécanisme de "déhallucination communicative".
4. Lisez sur OpenClaw et Moltbook. Choisissez un mode d'échec spécifique qui est apparu à l'échelle de la population et qui ne apparaîtrait pas dans un système de 5 agents. Comment vous contre-engineeriez-vous ?
5. Choisissez votre projet multi-agent actuel. Lequel des trois études de cas est la référence la plus proche? Quelles décisions de conception de cette étude de cas n'avez-vous pas encore adoptées?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## Encore une lecture

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) la référence de production des travailleurs en charge
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) Décomposition du rôle du SOP
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) déhallucination communicative
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) Équelle basée sur le DAG
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) vue d'ensemble des écosystèmes
- [WMAC 2026](https://multiagents.org/2026/) Atelier du programme de pont 2026 de l'AAAI sur la coordination multi-agents
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) chef de la production
- [CrewAI docs](https://docs.crewai.com/en/introduction) cadre fondé sur les rôles
