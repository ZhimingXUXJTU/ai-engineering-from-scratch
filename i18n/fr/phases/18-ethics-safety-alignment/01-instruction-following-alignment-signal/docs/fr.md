# Suivre les instructions comme signal d'alignement

> Chaque critique ultérieure de RLHF s'oppose à ce pipeline. Avant d'étudier comment la pression d'optimisation déforme un proxy, vous devez voir le proxy. InstructGPT (Ouyang et coll., 2022) a défini l'architecture de référence: réglage supervisé sur les paires d'instructions-réponse, un modèle de récompense formé sur les classements de préférence par paires et PPO contre le modèle de récompense avec une pénalité KL à la politique SFT. Un GPT Instruct 1.3B a été préféré à un GPT 175B-3. Ce résultat unique est la raison pour laquelle chaque laboratoire frontalier en 2026 envoie toujours un pipeline post-entraînement en forme de RLHF.

> **【中文解读】**InstructGPT(Ouyang 等人, 2022) définit une structure de référence pour les humains: 1) superviser les modifications de la SFT) dans les entraînements de commande-réponse; 2) le modèle de récompense est formé sur la séquence des préférences; 3) le modèle de récompense de la PPO, avec la protection du KL 惩罚.

> **【拓展：RLHF → 现代 AI 对齐】**RLHF (RHF) est une technique clé du succès de ChatGPT.

>  **【前置】**學本節前 請先掌握:Phase 10·06(SFT 監督微调)、Phase 10·07(RLHF)、Phase 10·08(DPO) 理解三段对齐管线的技术细节──本节是Phase 18 的开篇,从工程视角审视对齐后续 29节都基于此基础──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy three-stage pipeline) | **语言:** Python（标准库，玩具三阶段管线）
**Prerequisites:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO) | **前置知识:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objectifs d'apprentissage

- Nombre des trois étapes du pipeline InstructGPT et la perte utilisée dans chacune d'elles.
  Le texte de la loi est écrit en français.
- Expliquez pourquoi un modèle ajusté aux instructions 1.3B a dépassé le modèle brut 175B GPT-3 sur l'évaluation des préférences humaines.
  Le modèle 1.3B a été défait par le GPT-3 original.
- Expliquez à quoi la sanction KL de l'étape 3 protège et pourquoi la suppression de celle-ci entraîne un comportement de recherche de mode.
  Le troisième étape de la KL 惩罚 protéger est ce que, ainsi que pourquoi le déplacement de celui-ci entraînera le mode 崩行为.
- Décrivez l'impôt d'alignement et l'atténuation du PPO-ptx appliquée à l'égard de Ouyang et coll.
  Le PPO-ptx 缓解方法, utilisé par Ouyang et d'autres personnes, est un moyen de réduire les taxes.

## Le problème , l' introduction du problème

Les modèles de langage prétraînés complètent le texte. Ils ne répondent pas aux questions. Demandez à GPT-3 "écrire une fonction Python qui renverse une liste" et vous obtenez souvent une autre demande, car la plupart de la distribution de formation est un texte Web qui se poursuit avec plus de texte Web. Le modèle fait son travail  le travail est faux.

> 预训语言模型补充全文,而不是回答问题――让GPT-3 "écrire une fonction Python 函数反转列表", vous obtiendrez souvent un autre conseil, car la plupart des réponses de la formation continuent à générer plus de contenu en ligne du texte en ligne―― le modèle est en train de terminer son travail 只是这个工作是错的──

Le proxy utilisé par chaque laboratoire sérieux pour corriger cela est la préférence humaine. Deux compléments vont à un évaluateur; le évaluateur choisit le meilleur; un modèle de récompense apprend le évaluateur. Puis une boucle RL déplace la politique vers les résultats du modèle de récompense score élevé. C'est la thèse complète de InstructGPT en trois phrases. Le reste du papier est l'ingénierie.

> Chaque laboratoire strict utilisé pour corriger ce problème est l'intermédiaire des préférences humaines. Deux compléments donnent aux évaluateurs; les évaluateurs choisissent mieux; les évaluateurs apprennent à évaluer le modèle de récompense.

## Le concept de base.

### Étape 1: réglage fin supervisé (SFT)

Rassembler des paires de réponses rapides où la réponse est ce qu'un humain bien intentionné écrirait. Ouyang et al. ont utilisé des demandes 13k de labélistes et de l'API OpenAI.

> 收集提示-响应, dont la réponse est un contenu écrit par un étiquetteur de bonne volonté. Ouyang et d'autres ont utilisé les 13k 提示 từ từ từ từ từ ký ký ký ký và OpenAI API.

Ce que la SFT vous donne: le modèle répond maintenant aux questions au lieu de les poursuivre. Ce qu'il ne vous donne pas: tout signal sur la réponse que le rater préfère lorsque plusieurs sont plausibles.

> SFT  vous donne: le modèle répond maintenant aux questions plutôt que de continuer à les compléter. SFT ne vous donne pas: lorsque plusieurs réponses sont raisonnables, le réviseur préfère tout signal de la réponse.

> **【中文解读】**SFT 阶段使模型从"补全文"转向"回答问题",但无法提供关于多个合理答案中哪个更好的信号──RM 阶段使用布拉德利-特里 成对偏好损失 L_RM = -log sigmoid(r(x,y_w) - r(x,y_l)) 在标注者排列的补对上训奖励模型──RM est généralement basé sur le SFT 模型初始化并替换 LM 头为标量头,6B 就足以指导 175B 模型──

### Étape 2: modèle de récompense (RM)

Pour chaque prompt, prenez l'échantillon des compléments K du modèle SFT. Un étiqueteur les classe.`y_w`était préféré à `y_l`- Le numéro de la liste:

> Pour chaque suggestion, de la SFT 模型采样 K 个补全;; les étiquetteurs pour les ranger;; entraînement un modèle de récompense pour toute suggestion-réponse à la fraction, de sorte que pour `y_w`- Je suis là .`y_l`Le groupe de travail

```
L_RM = -log sigmoid(r(x, y_w) - r(x, y_l))
```

C'est la perte de préférence par paire Bradley-Terry. Le RM est généralement initialement défini à partir du modèle SFT avec la tête LM remplacée par une tête escalare.

> C'est Bradley-Terry qui est devenu un défaut de préférence.

Les modèles de récompense sont petits: 6B suffisait pour le 175B InstructGPT. Ils sont également fragiles  section 5 du document concerne principalement les comportements de piratage de la récompense qui se sont produits à petite échelle.

> Le modèle de récompense est très petit: 6B suffit pour guider 175B de l'InstructionGPT.

> **【拓展：PPO 阶段 → RLHF 的核心工程】**La fonction cible de la phase PPO 阶段 J(pi) = E[r(x,y) - beta * KL(pi de pi_SFT) maximiser la récompense tout en gardant la stratégie proche de SFT。 KL系数 beta est la plus importante RLHF 超参数太低导致奖励黑客,太高则 SFT 上无改进。

### Étape 3: PPO avec une pénalité KL

Définir l'objectif:

```
J(pi) = E_{x~D, y~pi(.|x)} [ r(x, y) ] - beta * KL(pi(.|x) || pi_SFT(.|x))
```

Le terme KL est conservé.`pi`Sans elle, l'optimisateur trouve des exemples contradictoires  des chaînes qui marquent bien sous le RM parce que le RM ne les a jamais vus, pas parce que les humains les préfèrent réellement.

> Utilisez le PPO maximisation.`pi`Sans elle, l'optimisateur trouvera des liens de caractères contre les échantillons dans RM, parce que RM n'a jamais vu ces derniers, et non pas les véritables préférences humaines.

Le coefficient KL `beta`trop bas: piratage de la récompense trop élevé: aucune amélioration par rapport à la SFT.

> Le nombre de K.L.`beta`Il est important de noter que la RLHF 超参数──太低:奖励黑客──太高:相比 SFT 没有改进──

> **【中文解读】**Pour le paiement du tarif: le RLHF 后模型在人类偏好上更好但在标准基准(SQuAD, HellaSwag, DROP) 上退步。Ouyang 等人称之为"对齐税"并使用PPO-ptx 修复将预训梯度混入RL 目标,使模型不忘从未获奖的下游任务──PPO-ptx 成为标准Anthropic、DeepMind和Meta 都使用某种变体──

### Taxe d'alignement

Après la RLHF, le modèle est préféré par les humains mais régresse sur les critères de référence standard (SQuAD, HellaSwag, DROP). Ouyang et al. appellent cela la taxe d'alignement et le fixent avec PPO-ptx: mélangez les gradients pré-entraînement dans l'objectif de RL afin que le modèle n'oublie pas comment effectuer des tâches en aval pour lesquelles il n'a jamais été récompensé.

> Après la RLHF, le modèle est meilleur sur les préférences humaines mais sur les critères de base (Squad, HellaSwag, DROP) (en anglais: Standard KPI, SQUAD, HellaSwag, DROP) (en anglais: Standard KPI, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, SQUAD, S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S. S

```
J_ptx(pi) = J(pi) + gamma * E_{x~D_pretrain} [ log pi(x) ]
```

Le PPO-ptx est devenu standard. Anthropic, DeepMind et Meta utilisent tous une variante.

> Le PPO-ptx  devenir un standard──Anthropique、DeepMind 和 Meta 都使用某种变体──

> **【拓展：1.3B vs 175B → 对齐独立于能力】**1.3B InstructGPT sur les préférences des émetteurs de marque environ 70% du temps sur 175B GPT-3。 la différence dans le flux de production caché sur les suggestions de test est plus grande。 deux points importants: 1) le niveau de conformité est différent de celui de la capacité175B a plus de capacité, 1.3B a plus de niveau de conformité, les préférences des émetteurs de marque sont plus élevées; 2) la capacité sous-limité par le modèle de base est définie vous ne pouvez pas RLHF Un modèle de base lui permet de savoir des faits qu'il n'a jamais vus.

### Le résultat

Un 1.3B InstructGPT (SFT + RM + PPO-ptx) est préféré par les étiquetteurs au GPT-3 de base 175B environ 70% du temps.

> 1.3B de l'instructionGPT(SFT + RM + PPO-ptx) dans environ 70% du temps est préféré par le marqueur à 175B de base GPT-3── la différence est plus grande sur les suggestions de test cachés du flux de production── de ce chiffre on peut lire deux choses:

1. L'alignement est un axe différent de la capacité. Le modèle 175B avait plus de capacité; le modèle 1.3B avait plus d'alignement; les étiquetteurs préféraient celui aligné.
   Le modèle 175B a plus de capacité; le modèle 1.3B a plus de capacité; le modèle préfère le modèle.
2. Le niveau de capacité est fixé par le modèle de base.
   Vous ne pouvez pas passer par RLHF 让基础模型知道它从未见过的事实──

> **【拓展：Phase 18 后续课程 → 每个都在攻击此管线】**Chaque critique de l'étape suivante est en partie attaquée par cette ligne de conduite: les actions de récompense des blacks (leçon 2) étape 2, DPO (leçon 3) étape 2 et 3, CAI (leçon 5) remplacer les marqueurs humains (leçon 4) les marqueurs sont biaisés (leçon 9) les stratégies de démonstration peuvent être complètement contournées (leçon 3) Si cette ligne de conduite n'est pas dans le cerveau, il est impossible de comprendre ces critiques.

### Pourquoi c'est le point de référence de la phase 18

Chaque critique dans les leçons ultérieures  récompense de piratage (leçon 2), DPO (leçon 3), sycophancy (leçon 4), CAI (leçon 5), agents endormis (leçon 7), alignement de fausse (leçon 9)  s'oppose à une partie de ce pipeline. Les attaques de piratage récompensent étape 2. Le DPO s'effondre dans les étapes 2 et 3. CAI remplace l'étiquetateur humain. La sycophancy montre que l'étiquetage est un signal biaisé. Les faux alignements montrent que la politique peut se diriger entièrement autour de l'étape 3. Vous ne pouvez suivre aucune de ces critiques sans d'abord avoir le pipeline dans votre tête.

> Chaque critique de la suite du cours  récompense 黑客(Létion 2)、DPO(Létion 3)、(Létion 4)、CAI(Létion 5)、潜伏 Agent(Létion 7)、对齐伪装(Létion 9) 都在攻击此管线的某个部分── récompense 黑客攻击第二阶段──DPO 合并第二和第三阶段──CAI 替代人类标记者──展示标记者是有偏见信号──对齐伪装展示策略可以完全绕过第三阶段──如果没有在脑中这个管线,就无法理解这些批评──

## Utilisez-le avec le cadre de réalisation
```figure
al-instruct-pipeline
```

## Utilisez-le

`code/main.py`simulation des trois étapes sur les données de préférence des jouets. La "politique" de base est une pièce biaisée sur les actions {A, B, C}. La phase 1 du SFT imite les actions de l'étiquetage sur 200 demandes. La deuxième étape correspond à un modèle de récompense Bradley-Terry de 500 classements par paires. La phase 3 consiste à simplifier la mise à jour de l'OPP avec une pénalité KL à l'égard de la politique de FFT. Vous pouvez regarder la hausse des récompenses, la divergence KL croître, et la dérive des politiques  et vous pouvez désactiver le terme KL pour voir le piratage de récompense apparaître dans 50 étapes de mise à jour.

> `code/main.py`La stratégie de base est la mise en œuvre de la stratégie de mise en valeur de la monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de monnaie de

À quoi regarder:

观察要点:

- Trajectorie de récompense avec `beta = 0.1`contre`beta = 0.0`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`beta = 0.1`contre`beta = 0.0`时的奖励轨迹──
- L'éducation et la formation sont des aspects essentiels de la formation.
  Le changement de la formation est le changement de la formation.
- Répartition finale des actions par rapport à la préférence de l'étiquetage.
  Le référencement final de la distribution avec le préférencement des étiquetteurs.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-instructgpt-explainer.md`. Une description du pipeline RLHF ou un résumé papier indiquent quelle des trois étapes est modifiée, quelle perte est utilisée à chaque étape et si une pénalité KL ou un régulateur équivalent est présent.

> 本课产 出 `outputs/skill-instructgpt-explainer.md` Donner une description ou un résumé de l'article de la RLHF, il identifie les trois étapes qui ont été modifiées, quelles sont les pertes utilisées dans chaque étape, et s'il existe un système de correction ou d'équivalence KL.

## Les exercices

1. On court .`code/main.py`- Je suis prêt .`beta = 0.0`et de signaler la répartition de l'action après 200 étapes de PPO. Expliquez le comportement de recherche de mode en un paragraphe.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ la mise en place `beta = 0.0`Il a également rapporté la répartition des mouvements après la PPO de 200 étapes.

2. Modifiez le modèle de récompense pour avoir un biais de +0,5 pour l'action B (un bug de récompense simulé).`beta = 0.1`La sanction KL empêche-t-elle la politique d'exploiter le biais ?`beta`l'exploitation devient visible ?
   Le modèle de récompense modifié fait l'action B avec +0,5 偏置(模拟奖励 bug) 』用 `beta = 0.1`运行 PPO──KL 惩罚能否阻止策略利用偏置? 在什么?`beta`La valeur de l'utilisation est devenue visible ?

3. Lisez Ouyang et coll. (arXiv:2203.02155) Figure 1. Reproduire la courbe de préférence étiquetateur en exécutant PPO pour 1, 5, 20, 100 étapes et en mesurant la préférence par rapport au modèle SFT.
   Le modèle de la SFT est le modèle de la SFT.

4. La section 4.3 du journal rapporte qu'un GPT Instruct 1.3B dépasse 175B GPT-3 environ 70% du temps. Pourquoi le ratio serait-il plus élevé sur les instructions de production cachées que sur les instructions du label?
   Le rapport 1.3B InstructGPT a gagné environ 70% du temps 175B GPT-3... Pourquoi cette proportion de suggestions de production cachées est-elle plus élevée que celle des propres suggestions du marqueur ?

5. Remplacez la perte de PPO par DPO (phase 10 · 08) sur les mêmes données de préférence. Comparer la dérive finale de la politique (KL à SFT) et la récompense finale. Quelle méthode dérive plus loin à la récompense correspondante?
   La phase 10 · 08) est de remplacer la PPO 损失.

## Les termes clés

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| SFT | "instruction tuning" / "指令微调" | Stage 1: cross-entropy fine-tune on prompt-response pairs / 阶段 1：在提示-响应对上交叉熵微调 |
| Reward model | "the RM" / "奖励模型" | Scalar regressor over (prompt, response) trained with Bradley-Terry on pairwise labels / 用 Bradley-Terry 在成对标签上训练的标量回归器 |
| Bradley-Terry | "pairwise preference loss" / "成对偏好损失" | -log sigmoid(r_w - r_l); reduces pairwise ranking to binary classification / 将成对排序简化为二分类 |
| KL penalty | "the regularizer" / "正则化器" | `beta * KL(pi \|\| pi_SFT)` — keeps the RL policy near the SFT anchor / 保持 RL 策略接近 SFT 锚点 |
| PPO-ptx | "PPO with pretraining mix" / "带预训练混合的 PPO" | Adds a fraction of pre-training log-likelihood to the PPO objective to offset the alignment tax / 将部分预训练对数似然加入 PPO 目标以抵消对齐税 |
| Alignment tax | "the RLHF regression" / "RLHF 退步" | Post-RLHF drop on standard benchmarks that RLHF did not target / RLHF 后在未针对的标准基准上的性能下降 |
| Labeler preference | "the ground truth" / "地面真实" | Sample of human rankings; the RM is a statistical proxy for this, not for "human values" / 人类排序的样本；RM 是其统计代理，而非"人类价值观" |

## Encore une lecture

- [Ouyang et al. — Training language models to follow instructions with human feedback (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155) le papier InstructGPT, fondement de chaque pipeline RLHF qui a suivi
  Le projet de loi de construction de la RLHF est en cours de réalisation.
- [Stiennon et al. — Learning to summarize from human feedback (arXiv:2009.01325)](https://arxiv.org/abs/2009.01325) le prédécesseur du RLHF pour résumé
  Le récit de la première partie de la résumé
- [Christiano et al. — Deep reinforcement learning from human preferences (arXiv:1706.03741)](https://arxiv.org/abs/1706.03741) la formule de RL originale basée sur les préférences
  Traduction anglaise: Christiano et autres sur la base de RL préférentielle
- [Bai et al. — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)](https://arxiv.org/abs/2204.05862) L'extension de la HH de l'oléoduc InstructGPT par Anthropic
  Le langage de l'extension de la HH est en train de se développer.
