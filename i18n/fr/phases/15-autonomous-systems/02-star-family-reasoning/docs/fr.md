# STAR, V-STAR, Quiet-STAR  Rasonation autodidacte  STAR Série de méthodes de préconisation de soi

> La plus petite boucle d'auto-amélioration possible se trouve à l'intérieur de la logique. Un modèle génère une chaîne de pensées, garde celles qui arrivent à des réponses correctes, et les maîtrise. C'est le STAR. V-STaR ajoute un vérificateur donc la sélection des délais d'inférence est meilleure. Quiet-STaR pousse la raison à chaque marque. Les trois fonctionnent. Aucun d'entre eux n'est magique. La boucle préserve tout raccourci qui arrive pour atteindre la bonne réponse.

> **【中文解读】**Le plus petit cycle d'amélioration de soi caché dans le processus de réflexion: le modèle génère des chaînes de réflexion, conserve le processus de réflexion de la réponse correcte, modifie ces données. C'est STaR.

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**La série STaR est le cœur de l'entraînement de "auto-exploration"  modèle de l'entraînement avec son propre raisonnement à l'extérieur de l'entraînement de soi-même。OpenAI o1/o3 系列 模型背后的强化学习训练就采用类似思路:生成多个推理路径,选择正确的,使用它们来改进模型──这是实现AI自我改进闭环的关键技术──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Il est également possible de faire une analyse de la situation de l'équipe de formation de la formation professionnelle.
>  **【类比】**STaR = "élève auto-dépôt"──普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对对的推理保留并自我再练一遍(自我生成训练数据)──problème est: parfois le processus de推理是错误的但答案巧合对对对对对对对对对对对,STaR 会强化这种"蒙对"推理V-STaR加一个法官验证器) 掉错推理──
> ️ **【易错点】**STaR  entraînement 时只看"答案是否正确"会强化"捷径推理"(错误过程但正确结果) ――修复:用过程奖励(PRM,Phase 13·03)

## Le problème , le problème , l' introduction , l' introduction

La façon la plus simple d'enseigner à un modèle à raisonner est de recueillir des traces de raisonnement écrites par l'homme.

> La méthode directe de la réflexion du modèle est de recueillir les traces de réflexion de l'écriture humaine.

STaR (Self-Teught Reasoner, Zelikman et al., 2022) demande: que se passe-t-il si le modèle écrit ses propres raisonnements et les classe par rapport aux réponses connues ?

> STaR(auto-enseignement de la réflexion, Zelikman  et autres, 2022) propose: si le modèle lui-même écrivait le processus de réflexion et s'engageait avec la réponse connue à la réflexion ?


> **【中文解读】**Star 家族推理技术 (STAR、Quiet-STaR、ReST、ReST-EM) est une technique de formation à la base de la série OpenAI o1/o3 et de l'Anthropic Extended Thinking.

1. Prenez une trace de raisonnement plus une réponse.
2. Si la réponse finale est correcte, conservez la trace.
3. - Une bonne réglage des traces.
4. Je répète.

Il fonctionne. GSM8K et CommonsenseQA ont tous deux amélioré sans nouvelle annotation humaine. Mais la boucle a un biais intégré: toute raison qui a produit la bonne réponse est conservée, indépendamment du fait que le raisonnement lui-même était solide. V-STaR (Hosseini et coll., 2024) le corrige avec un vérificateur appris; Quiet-STaR (Zelikman et coll., 2024) généralise l'idée à per-token rationnels internes.

> Il est valable. GSM8K et CommonsenseQA ont augmenté sans marque de nouvelle personne. Mais le cycle a un décalage interne: tout processus de raisonnement qui produit une réponse correcte est conservé, peu importe si la raisonnement est raisonnable en soi.

## Le concept de base.

### STaR: démarrage sur ce qui a fonctionné

Commencez par un modèle de base avec une faible capacité de raisonnement. Pour chaque problème de formation, prenez un échantillon de raisonnement plus une réponse. Si la réponse correspond à l'étiquette, gardez le triple (problème, raisonnement, réponse).

> On commence par un modèle de base avec une capacité de raisonnement plus faible. Pour chaque question de formation, on prend un processus de raisonnement en plus de réponse. Si la réponse correspond à l'étiquette, on conserve le problème.

Si le modèle ne peut jamais résoudre un problème, la boucle ne peut pas apprendre à partir de lui.**rationalization**Pour les problèmes qui ne sont pas satisfaits, injectez la réponse correcte comme indice et réinvitez le modèle à produire une justification qui en débouche.

> Un tournant clé: si le modèle ne peut jamais répondre correctement à une question, le cycle ne peut pas apprendre de lui.**合理化**Pour les problèmes de défaillance du modèle, la réponse correcte est insérée comme une suggestion, la suggestion de nouveau produit un modèle qui se dirige vers cette réponse.

Résultat dans le document original (Zelikman et coll., 2022): un modèle de base GPT-J s'est amélioré sur GSM8K de 5,8% à 10,7% grâce à des tours répétés de STaR avec une rationalisation  environ 5 points de pourcentage absolus. Sur CommonsenseQA, le GPT-J 6B formé par STaR a atteint 72,5%, comparable à un GPT-3 175B (~73%)

> Le modèle de base de GPT-J est passé par une refonte rationalisée de la série STaR, passant de 5,8% à 10,7% sur GSM8K, à environ 5 pour cent de points de croissance absolue.

### V-STaR: former un vérificateur avec le DPO

Les STaR rejettent les rationales incorrectes. Hosseini et coll. (2024) ont observé que ce sont aussi des données: chaque paire de (rationale, "est-ce correct") peut former un vérificateur. Ils utilisent l'optimisation des préférences directes sur les solutions correctes et incorrectes pour construire un classement.

> STaR  abandonner les raisonnements incorrects🏼Hosseini 等人🏼2024) observe que ceux-ci sont également données: par contre🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻🏻

Delta déclaré: +4 à +17 points de pourcentage par rapport aux lignes de base précédentes d'auto-amélioration sur GSM8K et MATH, la plupart des gains provenant de l'utilisation du vérificateur pour la sélection du temps d'inférence plutôt que pour la mise au point fine supplémentaire du générateur.

> 报告的提升: en GSM8K 和 MATH, la plupart des améliorations sont dues à des tests de sélection de données, et non à des modifications supplémentaires de générateurs.

### Quiet-STaR: rationaux internes par jeton

Zelikman et coll. (2024) ont demandé: que se passe-t-il si le modèle apprend à générer une courte rationalisation interne à chaque position de jeton, pas seulement entre problème et réponse? Quiet-STaR entraîne un modèle à émettre une "pensée" cachée avant chaque jeton prédit, puis mélange la prédiction consciente de la pensée avec la prédiction de base via un poids appris.

> Zelikman et d'autres ont proposé: si le modèle s'établit à chaque position de chaque jeton pour générer une brève raison interne, et non seulement entre les questions et les réponses?

Résultat: Mistral 7B a obtenu des améliorations absolues de zéro coup sur GSM8K de 5,9% à 10,9% et CommonsenseQA de 36,3% à 47,2% sans ajustement spécifique à la tâche.

> Résultat: Le Mistral 7B dans le GSM8K a augmenté de 5,9% à 10,9%, dans le CommonsenseQA de 36,3% à 47,2%, sans avoir besoin de micro-régulation spécifique.

### Pourquoi les trois ont- ils un souci commun pour la sécurité ?

Les trois méthodes utilisent la réponse finale comme le signal de gradient. Une logique qui atteint la bonne réponse par un raisonnement erroné  exploitant un raccourci, devinant ou utilisant un schéma non généralisant  est renforcée positivement. Sur les problèmes de distribution, le raccourci fonctionne. Sur les problèmes de distribution, il se brise silencieusement.

> Trois méthodes utilisent la réponse finale comme signal de gradience. Le processus de raisonnement qui consiste à obtenir une réponse correcte par le biais de raisonnements défectueux est renforcé de manière positive.

Le vérificateur de V-STaR atténue en apprenant à classer les rationales, mais le vérificateur est formé sur le même ensemble d'étiquettes. Il peut apprendre à préférer le raisonnement incorrect bien formaté à l'incertitude honnête. La conception plus sûre consiste à combiner les données de style STaR avec (a) des modèles de récompense supervisés par le processus (récompenser les étapes intermédiaires, pas seulement les réponses) et (b) une évaluation OOD prolongée qui rompt des raccourcis simples.

> Le testateur de V-STaR est un testateur qui apprend à classer les hypothèses, mais qui est entraîné sur le même ensemble d'étiquettes. Il peut apprendre à préférer le format de la hypothèse, mais pas le format de la hypothèse, mais l'incertitude non honnête.

### Comparaison

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### Là où cela se trouve dans la pile 2026

Le STAR est vieux. Mais le modèle réapparaît partout en 2025-2026. RL sur les problèmes mathématiques vérifiables (DeepSeek-R1, Kimi-k1.5, o1) est le signal de gradient de réponse conditionné de STaR, augmenté. Les modèles de récompense des processus (Lightman et coll., 2023; "Vérifions étape par étape" d'OpenAI) sont l'alternative supervisée par le processus. AlphaEvolve (leçon 3) est STaR pour le code, avec un évaluateur de programme au lieu d'une étiquette. Darwin Godel Machine (Légion 4) est STaR pour l'échafaudage agent lui-même.

> Le STaR est très ancien. Mais ce modèle est apparu en 2025-2026 à tout moment. RL (en mathématiques de recherche de profondeur) est la réponse à la question de la STaR.

Comprendre le STaR fait tous ces clics. C'est la boucle d'auto-amélioration minimale viable.

> Comprendre le STAR 让所有这些都说通── c'est le cycle de l'auto-amélioration le plus simple possible──

## Utilisez-le avec le cadre de réalisation
```figure
reflection-loop
```

## Utilisez-le

`code/main.py`Il utilise une boucle STaR simulée sur une tâche arithmétique de jouet.

- Comment la précision surpasse les tirs de lance-tampons.
  Le taux de démarrage est de 4,0%.
- Comment les raccourcis se glissent: le simulateur comprend une classe de logiciels "farouches" qui obtient la bonne réponse 40% du temps mais généralise mal.
  En français, le terme "réflexion" est utilisé pour désigner un type de "réflexion" qui est un type de "réflexion".
- Comment un vérificateur (style V-STaR) aide à l'inférence mais ne peut pas éliminer complètement les raccourcis introduits lors de la formation.
  Comment aider à la réflexion mais ne pas complètement modifier le chemin de l'introduction pendant l'entraînement.

## Envoyez-le . Produit .

`outputs/skill-star-loop-reviewer.md`vous aide à vérifier un projet de logiciel de raisonnement autodidacte avant de vous entraîner à le faire.

> `outputs/skill-star-loop-reviewer.md` vous aider à évaluer les recommandations de l'auto-enseignement avant l'entraînement 

## Les exercices

1. Exécutez le simulateur. Définissez la fréquence de raccourci à zéro, puis à 0,4. Quelle est la différence de précision finale entre les deux courses, même si les deux atteignent > 90% sur la distribution de l'entraînement?
   Quels sont les taux de différences de précision entre les deux opérations, même si les deux atteignent > 90% dans la distribution de formation ?

2. Ajoutez un test OOD prolongé au simulateur. Découvrez les problèmes d'une distribution différente et évaluez le modèle démarré sur les ensembles en distribution et OOD. Quantifiez l'écart.
   Le nombre de personnes qui ont été tuées est de plus de 500 personnes.

3. Lisez le papier Quiet-STaR (arXiv:2403.09629) Section 3. Expliquez le jeton "fin de la pensée" et la tête de poids de mélange en trois phrases chacune.
   Le mot "penser" est traduit par "penser" et "penser".

4. Comparer le filtre de conservation de la qualité de STaR à une alternative supervisée par le processus qui récompense chaque étape rationnelle de manière indépendante.
   Traduction anglaise: identifier les différences de coût et de qualité.

5. Conception d'une évaluation qui capturerait les rationales des raccourcis dans un modèle déployé.
   Il suffit de briser le plus simple chemin de renforcement du cycle de STaR.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Encore une lecture

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) le papier original.
  Le texte original est écrit en français.
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) ajoute un vérificateur DPO pour la sélection du temps d'inférence.
  Le document d'évaluation est utilisé pour la sélection.
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) rationales internes par jeton.
  Le mot "conception" est traduit par "conception".
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) modèles de récompense de processus, le signal de gradient alternatif.
  Le processus de récompense est un modèle de récompense.
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) RL sur les tâches vérifiables, STaR étendu à la formation frontalière.
  Le RL, le STAR est à l'avant-garde.
