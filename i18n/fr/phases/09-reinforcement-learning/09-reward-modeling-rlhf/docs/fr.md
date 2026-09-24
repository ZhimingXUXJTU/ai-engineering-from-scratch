# Récompense Modélisation & RLHF

> Les humains ne peuvent pas écrire une fonction de récompense pour " bonne réponse assistante ", mais ils peuvent comparer deux réponses et choisir la meilleure. Ajustez un modèle de récompense à ces comparaisons, puis RL le modèle de langue contre lui. Christiano 2017. InstructGPT 2022. La recette qui a transformé GPT-3 en ChatGPT. En 2026 il est principalement remplacé par DPO  mais le modèle mental reste.

> **【中文解读】**Les gens ne peuvent pas écrire une fonction de récompense pour un " bon assistant répéter ", mais ils peuvent comparer deux répéter et choisir mieux. Avec ces modèles de récompense de formation comparés, ils utilisent de nouveau le modèle de langue RL.

> **【拓展：RLHF 是大模型对齐的关键】**RLHF(basé sur l'humanité contre de la force de l'apprentissage) est le cœur de la technologie de succès ChatGPT.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Vous avez formé un modèle de langage sur l'objectif de prédiction du prochain jeton. Il écrit l'anglais grammatical. Il ment aussi, vagabondage et refuse de refuser. Vous ne pouvez pas résoudre cela avec plus de prétrainement.

> Vous avez entraîné le modèle de langage dans le prochain jeton 预测目标. Il écrit le langage correct en anglais. Mais il ment aussi.

Vous voulez une * récompense à l'échelle* qui dit " la réponse A est meilleure que la réponse B pour l'instruction X. " Écrire cette fonction de récompense à la main est impossible. " Aide " n'est pas une expression de forme fermée sur des jetons. Mais les humains peuvent comparer deux sorties et marquer une préférence.

> Vous voulez une * étiquette récompense*, indiquant " Pour l'ordre X, répéter A par rapport à B mieux "...... écrire cette fonction récompense est impossible.

RLHF (Christiano et coll. 2017; Ouyang et coll. 2022) convertit les préférences en un modèle de récompense, puis optimise le LM via PPO contre cette récompense. En trois étapes: SFT → RM → PPO. C'est la recette qui a expédié ChatGPT, Claude, Gemini et tous les autres alignés-LLM en 20232025.

> RLHF va se transformer en modèle de récompense, puis passer par PPO pour optimiser la LM.

En 2026, la phase PPO est principalement remplacée par la phase 10 · 08, car elle est moins chère et presque aussi bonne pour l'ajustement de l'alignement. Mais la pièce * modèle de récompense * est toujours à la base de chaque échantillonneur Best-of-N, chaque pipeline RL-from-verifiable-rewards, et chaque modèle de raisonnement utilisant un modèle de récompense de processus.

> En 2026, les PPO sont largement remplacés par les DPO, car ils sont moins chers et ont pratiquement les mêmes résultats. Mais le modèle de récompense reste le meilleur des échantillons.

> **【中文解读】**RLHF 三阶段流程:(1) SFT supervise les modèles de base de la démonstration humaine;(2) RM utilise les préférences humaines à l'entraînement Bradley-Terry 奖励模型;(3) PPO utilise le modèle de signal optimisation du langage de la démonstration de la démonstration de Bradley-Terry, tout en ajoutant KL 惩罚 empêcher le déviation de SFT 太远──

> **【拓展：DPO 与 RLHF 的对比】**DPO(Direct Preference Optimization) va mettre en place RM+PPO de RLHF 两步合并为一步 directement du modèle de préférence à la stratégie de formation, sans besoin de modèle de récompense de formation manifeste.

## Le concept de base.

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**Commencez par un modèle de base prétrainé. Définition sur des démonstrations écrites par l'homme du comportement cible (réactions à la suite d'instructions, réponses utiles, etc.).`π_SFT`qui est *biased vers le bon comportement* mais a toujours un espace d'action illimité.

> **阶段 1：监督微调（SFT）。**Le modèle de base de pré-entraînement commence à être modifié en termes de comportement objectif de l'écriture humaine.`π_SFT`Il y a une autre.

**Stage 2: Reward Model training.**

- Rassembler des paires de réponses `(y_+, y_-)`à des invites `x`, étiqueté par les humains comme "y_+ est préférable à y_-. "
- Formez un modèle de récompense `R_φ(x, y)`pour attribuer des scores plus élevés à `y_+`- Je suis désolé .
- Perte: le **Bradley-Terry pairwise logistic**- Le numéro de la liste:

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  Le prix de la récompense est le plus élevé de tous les prix de la récompense.

- `R_φ`Le modèle SFT est généralement initialement défini avec une tête scalaire en haut.

> **阶段 2：奖励模型训练。** Collecter les préférences des marques humaines `(y_+, y_-)`, entraînement de récompense modèle donner`y_+`La perte est Bradley-Terry et la logique est retournée.`R_φ`Généralement, à partir de SFT 模型 initiale, ajouter un échantillon de sortie.

**Stage 3: PPO against the RM with KL penalty.**

- Initialiser la politique de formation `π_θ`de `π_SFT`Gardez une référence gelée.`π_ref = π_SFT`- Je suis désolé .
- Récompense à la fin d' une réponse `y`- Le numéro de la liste:

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  La pénalité de KL empêche `π_θ`de dériver arbitrairement de `π_SFT` il s'agit d'un régulateur, pas d'une région de confiance difficile. `β`Généralement`0.01`- Je suis là.`0.05`- Je suis désolé .
- Exécutez PPO (Léction 08) avec cette récompense.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**De `π_SFT`Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats de la formation: Résultats: Résultats de la formation: Résultats: Résultats de la formation: Résultats: Résultats: Résultats: Résultats de la formation: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats: Résultats Résultats: Résultats: Résultats: Résultats Résultats: Résultats Résultats: Résultats Résultats: Résultats Résultats Résultats: Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résultats Résésésésultats R

**Why the KL?**Sans elle, le PPO trouvera heureusement des stratégies de piratage des récompenses  le RM n'a été formé que sur les réalisations en distribution.`π_θ`C'est le bouton le plus important de la RLHF.

> **为什么需要 KL？**Sans elle, le PPO trouverait des stratégies de récompense pour les clients.`π_θ`保持在 RM 训练的流形附近──这是 une des randonnées les plus importantes de la RLHF──

**2026 status:**

- **DPO**(Rafailov 2023): l'algèbre de forme fermée s'effondre en une seule perte supervisée sur les données de préférence. Aucun RM, aucun PPO. La même qualité sur les points de référence d'alignement pour une fraction du calcul.
- **GRPO**(DeepSeek 20242025): PPO avec une base de référence relative au groupe au lieu d'un critique, récompense d'un *verifier* (code run / maths answers matches) au lieu d'un RM formé par l'homme. Dominant pour les modèles de raisonnement. couvert dans la phase 9 · 12.
- **Process reward models (PRMs):**Les solutions partielles de score (chaque étape de raisonnement), utilisées dans les variantes RLHF et GRPO pour le raisonnement.
- **Constitutional AI / RLAIF:**Il est important de noter que les entreprises peuvent utiliser un LLM aligné pour générer des préférences au lieu d'utiliser des humains.

> **2026 年状态：**Le DPO va mettre en place une phase 2+3 de révision de la situation.

## Construisez-le et mettez-le en œuvre.
```figure
reward-model
```

## Faites-le

Cette leçon utilise de minuscules "interrogations" et "réactions" synthétiques représentées sous forme de chaînes. Le RM est un marqueur linéaire sur une représentation de sac de jetons.`code/main.py`- Je suis désolé .

> Le RM est un indicateur de la ligne de référence de la lettre de référence. Il n'y a pas de véritable LLM.

### Étape 1: données de préférence synthétiques

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

Dans la vraie RLHF, cette étiquette est remplacée par des étiquettes humaines.`(prompt, preferred_response, rejected_response)` est identique.

> RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)`Toute la même chose.

### Étape 2: Modèle de récompense Bradley-Terry

Score linéaire: `R(x, y) = w · bag(y)`- Trainer pour minimiser les pertes de logs par couples BT:

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

Après quelques centaines de mises à jour,`w`assigne des poids positifs aux bons mots et négatifs aux mauvais.

> Après quelques centaines de mises à jour,`w`给好词代币 分配正权重,坏词 分配负权重──

### Étape 3: Politique de PPO en plus de RM

Notre politique de jouets produit un seul jeton à partir d'un vocabulaire.`log π_θ(token | prompt)`, ajouter une pénalité KL à référence, et appliquer le coupé PPO substitué.

> Notre stratégie de jouets consiste à générer un seul jeton à partir d'un seul mot.`log π_θ(token | prompt)`Il a ajouté KL à la punition de la stratégie de référence, et appliqué la coupe de la PPO 代理.

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键: récompense = RM 分数 - β × KL(π_θ 1920 π_ref) ――β est le contrôle de la stratégie de déménagement

### Étape 4: surveiller le KL

La moyenne de la piste `KL(π_θ || π_ref)`chaque mise à jour.`~5-10`La politique a dérivé de `π_SFT` plus bas `β`C'est le diagnostic le plus élevé dans la vraie RLHF.

> Chaque mise à jour de suivi moyenne`KL(π_θ || π_ref)` Si plus `~5-10`, la stratégie est loin`π_SFT`可能 β 正在降低或奖励黑客正在开始── c'est le diagnostic le plus important dans la vraie RLHF──

### Étape 5: la recette de production avec RTR

Une fois que vous comprenez le pipeline de jouets, voici la même boucle qu'un véritable utilisateur de bibliothèque l'écrit.[TRL](https://huggingface.co/docs/trl)est la mise en œuvre de référence  `RewardTrainer`pour la phase 2 et `PPOTrainer`(avec un KL-to-reference intégré) pour la phase 3.

> Une fois que vous avez compris le flux de jouets, ici est la vraie façon de rédiger le même cycle.`RewardTrainer`, étape 3`PPOTrainer`Il y a une autre.

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

Trois choses que la bibliothèque fait pour vous.`adap_kl_ctrl=True`met en œuvre le calendrier adaptatif-β: si le KL observé dépasse `target_kl`Le modèle de référence est gelé par convention  vous ne devez pas partager accidentellement des paramètres avec `policy`La valeur de la tête de la police est la même que celle de la police (`AutoModelForCausalLMWithValueHead`Il est également possible de faire une mise en place de la TRL.`policy/kl`et `value/loss`séparément.

> Il y a trois choses que tu dois faire.`adap_kl_ctrl=True`实现自适应 β 调度: si KL 超越目标则 β 翻倍, si低于一半则 β 减半―― référence modèle selon le règlement 结―― valeurs et stratégies sont sur le même axis principal――

## Les pièges

- **Over-optimization / reward hacking.**Le RM est imparfait .`π_θ`Les symptômes: la récompense monte indéfiniment tandis que le score humain d'évaluation atteint des plateaux ou des chutes.`β`- l'élargissement des données de formation RM.
  **过度优化/奖励黑客。**RM 不完美;`π_θ`找到抗性补全分高但质量差──症状: la récompense continue à augmenter mais le nombre de résultats de l'évaluation humaine est en retard ou en baisse──修复:早停止、提高 β、扩展 RM 训练数据──
- **Length hacking.**Les RM formés sur des réponses utiles récompensent souvent implicitement la longueur.
  **长度黑客。**Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Rés
- **Too-small RM.**Une petite somme ne peut pas évaluer fidèlement les résultats de la police.
  **RM 太小。**RM au moins doit être aussi grand que la stratégie.
- **KL tuning.**La politique de détection de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur est est est est est est est est est de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur
  **KL 调优。**Le but de la stratégie est de s'adapter à la situation de l'autre.
- **Preference-data noise.**- 30% des étiquettes humaines sont bruyantes ou ambiguës.
  **偏好数据噪声。**Environ 30% des étiquettes humaines sont bruyantes ou floues.
- **Off-policy problems.**Les données de PPO sont légèrement hors politique après la première époque.
  **离策略问题。**Les données de la première ère de la PPO 后略离策略──像课08那样监控裁剪比例──

## Utilisez-le avec le cadre de réalisation

Le RLHF en 2026 est couché:

> Le RLHF de 2026 est divisé en:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

En 2026, les pipelines d'alignement de production sont DPO-first, PPO-only pour les étapes de RM-intensive ou critiques pour la sécurité.

> Le RLHF en 2022-2024 est une méthode fondamentale.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-rlhf-architect.md`- Le numéro de la liste:

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## Les exercices

1. **Easy.**Entrenez le modèle de récompense Bradley-Terry .`code/main.py`sur 500 paires de préférence synthétiques. Mesurer par paires la précision sur 100 paires de préférence.
2. **Medium.**Réglez la boucle de jouets PPO-RLHF avec `β ∈ {0.0, 0.1, 1.0}`Pour chaque score, le score RM par rapport au KL à la référence sur les mises à jour.
3. **Hard.**Mettre en œuvre le DPO (perte de probabilité de préférence de forme fermée) sur les mêmes données de préférence et comparer avec le pipeline RLHF-PPO en calcul utilisé et le score final RM obtenu.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## Encore une lecture

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)Le journal qui a lancé RLHF.
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) la recette derrière le ChatGPT.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) RLHF antérieur pour résumé.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) DPO; le défaut post-RLHF en 2026.
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) RLAIF et boucle d'autocritique.
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862)- Le papier HH.
- [Hugging Face TRL library](https://huggingface.co/docs/trl) production `RewardTrainer`et `PPOTrainer`- Lisez la source de l'entraîneur pour les détails de la KL adaptative et de la valeur de tête.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)par Lambert, Castricato, von Werra, Havrilla  la marche canonique du pipeline en trois étapes avec des diagrammes.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl) la bibliothèque; `examples/`Il a des scripts RLHF de bout en bout pour Llama, Mistral et Qwen.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) la vision de l'hypothèse de récompense; condition préalable essentielle pour penser au piratage de la récompense.
