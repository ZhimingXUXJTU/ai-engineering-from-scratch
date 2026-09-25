# Le décodeur spéculatif et l' Eagle 3

> La leçon 16 a prouvé les mathématiques: la règle de rejet du Léviathan préserve exactement la distribution du vérificateur. Cette leçon est la vue de la formation en pile du décoding spéculatif de production de 2026. EAGLE-3 a transformé le modèle de projet d'une approximation bon marché en un réseau minuscule spécialement conçu et formé sur les états cachés du vérificateur, puis a ajouté une boucle de test de formation qui aligne ses distributions de train et d'inférence. Résultat: 3x à 6,5x accélération de bout en bout, taux acceptés par jeton supérieur à 0,9 sur le chat, aucun compromis de distribution. Chaque pile d'inférence de production en 2026 le renvoie par défaut.

> **【中文解读】**投机解码: Utilisez un petit modèle pour deviner 3-5 tokens, le grand modèle doit seulement être validé.

> **【拓展：投机解码→生产推理】**En 2026, tous les cadres de calculs principaux (vLLM, TensorRT-LLM) sont intégrés dans le projet de résolution.

>  **【前置】**學本節前 請先掌握:Phase 07·16(Décoding mathématique de la spéculation;Phase 10·12(Optimisation des inférences);Transformer 隐藏状态概念──本节是生产部署投机解码的工程视角──

>  **【类比】**投机解码 = 老板让实习生先起草邮件。实习生(draft model)秒写5 段草稿,老板(大模型) 校对一次一次──校对一段比从头写一段快得多──校对时如果某段错了,从那段开始重写──EAGLE-3's key:实习生看过老板以前写的邮件隐藏思考(隐藏状态),起草更像老板风格,接受率90%+──

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 16 (speculative decoding math), Phase 10 · 12 (inference optimization)
**Time:** ~75 minutes

## Objectifs d'apprentissage

- Décrire le théorème de Léviathan en une phrase et prouver que la boucle spéculative produit des échantillons distribués de manière identique au vérificateur.
  Utilisation d'une phrase de la théorie Leviathan, démontrant que le modèle généré par le cycle de projection est le même que le testateur
- Suivez la progression de deux ans du décoding des spécifications de vanille (Leviathan 2023) à l'Eagle, à l'Eagle-2 et à l'Eagle-3 et nommez la limite exacte à chaque étape.
  Réaliser de la simple mise en place de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'évolution de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement de l'événement
- Calculer l' accélération attendue du taux d' acceptation `α`et le ratio coûts entre projet et vérificateur `c`, et choisir la longueur optimale du projet `N`pour chaque régime.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               `α`Et le coût de l'essai`c`计算预期加速, choisir la longueur du projet pour chaque situation `N`
- Implémenter la boucle spéculative complète à partir de zéro: rédiger, vérifier, rejeter-échantillon du résiduel, retourner le cache KV à la rejet, émettre le jeton bonus à la pleine acceptation.
  De la réalisation de la totalité du cycle de lancement: décrets, vérifications, refus de la prise de données, refus de la rentrée de la mise en œuvre, stockage, acceptation, émission de jetons de récompense

## Le problème , l' introduction du problème

Le décodeur autorégressif sur un modèle 70B fonctionne à environ 35 jetons par seconde sur un H100. Le GPU n'est pas presque saturé. La bande passante de la mémoire est le plafond: chaque jeton charge 70B de poids de HBM, fait une étape d'arithmétique et produit une flotte.

> Le code de résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de la résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de résolution de

Le décodage spéculatif transforme cela en un problème de débit que vous pouvez réellement résoudre.`N`des jetons dans `N`Le vérificateur fonctionne une fois sur le préfixe plus tous`N`Les projets de répartition de la position du vérificateur`i`Si l'on est d'accord avec le projet (dans un sens statistique, nous allons être précis), on accepte; sinon, on rejette et on prend l'échantillon d'une correction de la distribution résiduelle.`N+1`accepté des jetons au lieu d'un.

> 投机解码 traduit cela en un problème de débit que vous pouvez réellement résoudre. Un modèle de projet bon marché proposant N 个标签. Le testateur s'occupe de N 个标签.

Le théorème qui compte est Leviathan, Kalman, Matias (ICML 2023): la distribution de sortie est identique à ce que l'échantillonnage du vérificateur aurait produit directement. Pas approximativement. Identiquement. C'est la raison entière pour laquelle le décoding spéculatif est acceptable dans la production  il s'agit d'une optimisation pure de la latence sans compromis de qualité.

> 关键定理来自Leviathan、Kalman、Matias(ICML 2023): la distribution de sortie est la même que celle qui est directement issue de l'échantillon d'éprouverteur.

Ce que la phase 7 · Leçon 16 vous a donné était la mathématiques. Ce que cette leçon vous donne est la pile de formation. Un bon projet vaut 2 fois plus d'accélération qu'un projet bon marché. EAGLE, EAGLE-2 et EAGLE-3 (Li et al., 20242025) ont transformé "projet = version plus petite du même modèle" en une discipline d'ingénierie précise.

## Le concept de base.

> **【中文解读】**投机解码(Décoding spéculatif) avec un petit modèle rapide deviner plusieurs jetons, reutiliser un grand modèle并行验证 jetons acceptés 直接保留,被拒绝从拒绝点重新生成──EAGLE 系列方法在特征层而不是 token层进行投机,接受率更高──

> **【拓展：投机解码的加速效果】**标准投机解码可实现2-3x 推理加速无损输出质量──EAGLE-2 和 Medusa 等方法通过多头并行预测达到3-4x 加速──关键技术指标是接受率(接受率)小模型与大模型的分布越近,接受率越高,加速效果越好──


### L'invariable: prélèvement d'échantillons de rejet du léviathan

Je vous laisse .`p(t)`être la distribution du projet pour le symbole suivant donné un préfixe, et `q(t)`Prenez un échantillon de jeton.`d ~ p`- Acceptez avec probabilité .`min(1, q(d) / p(d))`. Lorsqu'il est rejeté, échantillon de la distribution résiduelle `(q - p)_+ / ||(q - p)_+||_1`Les échantillons obtenus sont répartis selon `q`C' est vrai , peu importe la gravité .`p`C'est  pire c'est, plus vous rejetez souvent, mais la sortie reste exacte.

La pile `N`de ces appels de retour en retour en utilisant un vérificateur de transfert de transfert `prefix + d_1 + ... + d_N`Le vérificateur retourne `q_1, q_2, ..., q_{N+1}`En même temps, marchez de gauche à droite, sur le premier rejet à la position`j`, échantillon de `residual(q_j, p_j)`Après acceptation, prenez un jeton bonus.`q_{N+1}`- Je suis désolé .

### Ce qui détermine la vitesse

Je vous laisse .`α`Le taux d'acceptation attendu par jeton émis.`c = cost(draft) / cost(verifier)`Le nombre attendu de jetons acceptés par vérificateur à terme est:

```
E[accepted] = (1 - α^(N+1)) / (1 - α)
```

Le temps total de paroi attendu par jeton accepté est `(N * c + 1) / E[accepted]`- Réduire au minimum .`N`et vous obtenez le bon point.`α = 0.8, c = 0.05`: optimale `N`est d'environ 57, la vitesse est de 3,2x. Pour `α = 0.95, c = 0.02`: optimale `N`est d'environ 8×10, l'accélération pousse 5x.

Le seul levier le plus important est`α`- Je pars de`α = 0.6`(projet de vanille) à `α = 0.9`(AIGLE-3) à un niveau fixe `N = 5`Cela vous fait passer de 2,2 jetons acceptés attendus par vérificateur à 4.1.

### La progression de deux ans

**Vanilla speculative (Leviathan, 2023).**Le modèle de projet est un LLM plus petit de la même famille, formé indépendamment.`α ≈ 0.6`- On peut accélérer à 2 fois.

**EAGLE-1 (Li et al., 2024).**Draft est un transformateur minuscule  généralement d'une ou deux couches  qui prend l'état caché de la dernière couche du vérificateur comme entrée et prédit directement le prochain jeton.`α`s'élève à 0,70,8.

**EAGLE-2 (Li et al., 2024).**Ajout d'un arbre de projet dynamique: au lieu de proposer une seule séquence de `N`Les élèves peuvent choisir de choisir un petit arbre de candidats, de scorer chacun avec le vérificateur dans un passage en avant (attention des arbres) et de suivre le chemin de la plus grande probabilité.`α`par token accepté, il monte au-dessus de 0,85.

**EAGLE-3 (Li et al., 2025, NeurIPS).**Deux changements de plus. Tout d'abord, supprimez complètement la perte de prédiction de fonctionnalités  EAGLE-1/2 a entraîné le projet à correspondre aux états cachés du vérificateur, ce qui limite la quantité de données qui aide. Eagle-3 est directement sur la prédiction des jetons. Deuxièmement, test de temps de formation (TTT): lors de la formation de projet, remettre en avant les prédictions précédentes du projet en tant qu'inputs sur plusieurs étapes, de la même manière qu'il fonctionne à l'inférence. Cela aligne les distributions du train et des essais et arrête l'accumulation d'erreurs. Accélération mesurée: jusqu'à 6,5 fois sur le chat, amélioration de 38% du débit au lot 64 dans SGLang sur H100.

### Retour en arrière du cache KV

La vérification étend le cache KV du vérificateur de `N`Si le rejet se produit à la position`j`, le cache contient la position passée `j-1`Deux implémentations courantes: écrire à un tampon de grattage et s'engager sur acceptation (vLLM, TensorRT-LLM), ou garder un cache KV physique plus une longueur logique et truncate sur rejet.

Pour la recherche d'arbre EAGLE-2, le vérificateur exécute l'attention avec un masque non causale qui respecte la topologie des arbres.

### Projet d'architecture en 2026

| Strategy | Draft type | `α` | Speedup | Training cost |
|----------|-----------|-----|---------|---------------|
| Vanilla | Separate small LLM | 0.55-0.70 | 1.8-2.3× | None (reuse existing small model) |
| Medusa | Extra LM heads on verifier | 0.65-0.75 | 2-3× | ~1B SFT tokens |
| EAGLE-1 | 1-layer transformer on hidden states | 0.70-0.80 | 2.5-3× | ~60B tokens |
| EAGLE-2 | EAGLE-1 + dynamic draft tree | 0.80-0.88 | 3-4× | ~60B tokens |
| EAGLE-3 | Multi-layer feature fusion + TTT | 0.88-0.92 | 3.5-6.5× | ~60-200B tokens |
| Lookahead | No draft (Jacobi iteration) | N/A | 1.3-1.6× | None |

En 2026 production: vLLM et SGLang par défaut à EAGLE-3 quand disponible, EAGLE-2 autrement. TensorRT-LLM a le chemin Medusa le plus rapide pour les modèles publics Meta et NVIDIA. llama.cpp expédite le projet de vanille pour les déploiements de CPU.


> **【拓展：EAGLE 的创新点】**EAGLE utilise les caractéristiques de plusieurs niveaux précédents pour prédire les caractéristiques futures, puis les caractéristiques de déchiffrer les symboles. Le taux d'acceptation des méthodes traditionnelles s'élève à environ 60% à environ 80%, pour atteindre un accélération de 3 à 4 fois.


## Construisez-le et mettez-le en œuvre.
```figure
l5-spec-decode-eagle
```

## Faites-le

Regardez !`code/main.py`. Il s'agit de la boucle spéculative complète de Leviathan avec toutes les pièces: projet de N, passage parallèle du vérificateur, rejet par position, échantillonnage résiduel, jeton bonus, retour en arrière de KV et vérification empirique que la distribution de sortie correspond à l'échantillonnage direct de `q`- Je suis désolé .

### Étape 1: la règle de rejet

```python
def accept(q_prob, p_prob, u):
    if p_prob <= 0:
        return True
    return u < min(1.0, q_prob / p_prob)
```

### Étape 2: répartition résiduelle

```python
def residual(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    if s == 0:
        return list(q)
    return [r / s for r in raw]
```

### Étape 3: une étape spéculative complète

Le `spec_step`projets de fonction `N`des jetons de `p`, puis les vérifie tous en un parallèle `q`Pour chaque jeton élaboré, il applique la règle de rejet, et sur le premier rejet il prélève la correction du résidu.`q_{N+1}`- Je suis désolé .

### Étape 4: comptabilisation du KV

Le simulateur suit une logique .`kv_length`En ce qui concerne l'acceptation de l'accord de`k`Les projets `kv_length += k`- Sur un rejet à la position`j`, le cache est déjà écrit passé `j`, mais la longueur logique est fixée à `prefix_length + j + 1` un après le jeton de correction.

### Étape 5: le contrôle du Léviathan

Exécutez 50 000 étapes spéculatives. Comptez la répartition empirique des jetons acceptés. Comparer à 50 000 échantillons directs de`q`La statistique du carré de chi devrait être bien inférieure à la valeur critique.

### Étape 6: accélération par rapport à α

- La qualité du projet est perturbée .`p`loin de `q`à différentes amplitudes.`α`, puis tracer les jetons attendus par appel de vérificateur en fonction de `α`et `N`Le code imprime un tableau montrant comment la qualité des projets de classe EAGLE-3 (`α ≈ 0.9`) débloque 45 jetons par appel de vérificateur.

## Utilisez-le avec le cadre de réalisation

Niveau de production `vllm serve`avec EAGLE-3:

```bash
vllm serve meta-llama/Llama-3.3-70B-Instruct \
  --speculative-config '{
    "model": "yuhuili/EAGLE3-LLaMA3.3-Instruct-70B",
    "num_speculative_tokens": 5,
    "method": "eagle3"
  }'
```

SGLang avec EAGLE-3 au lot 64 sur H100: environ 1,38 fois plus de débit que le décoding en vanille du lot 64, selon le papier EAGLE-3.

Quand trouver le décodeur spéculatif:

- Toute charge de travail interactive de chat où la latence p50 compte plus que le débit maximum.
- Génération de code et sortie structurée (JSON, SQL). `α`est supérieure à 0,9 parce que la distribution cible est très prévisible.
- La génération de longs épisodes (milliers de jetons) et l'amortissement continue de payer.

Quand ne pas:

- Les modèles très petits (< 3B) Le projet n'est pas beaucoup moins cher que le vérificateur.
- Les petits déploiements de CPU de série 1... la mémoire du modèle de projet ne vaut peut-être pas la peine.
- Prise d'échantillons créatifs à très haute température où `α`Il s'effondre.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-eagle3-tuner.md`. Compte tenu de la charge de travail d'inférence (modèle, taille de lot, latence cible, profil de tâche), il recommande une stratégie de décoding spéculatif et des paramètres de réglage (famille de projets, `N`, profondeur des arbres, commutation à température).

> 本课产 出 `outputs/skill-eagle3-tuner.md` donner une idée de la tâche de charge (model 批次大小 目标延迟 任务配置), elle propose de tirer le meilleur parti des stratégies et des modifications de la tâche de travail (草稿族 ),`N`La température est en train de changer.

## Les exercices

1. On court .`code/main.py`- Confirmer les statistiques de la distribution de Leviathan en chiffres de chi-quadrés qui restent inférieurs à la valeur critique de 95% sur 50 000 échantillons.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer que la proportion de carburants de la distribution de Léviathan est inférieure à 95% de la valeur critique sur 50 000 échantillons.

2. - Le balayage .`N`de 1 à 10 avec `α`maintenu à 0,9 et `c`Le temps de chargement de la paroi est de 0,04 par token.`N`Il faut expliquer la forme de la courbe.
   Le premier est le premier.`N`De 1 à 10,`α` garder 0,9,`c`保持 0.04── dessiner chaque sélection de jetons d'attente numéros et chaque jeton 实际挂钟时间──找到最小化挂钟时间的 `N`❖ Expliquer la forme du volet

3. Modifier le code pour simuler la recherche d'arbre EAGLE-2: à chaque étape, le projet propose un arbre de forme `[2, 2, 2]`Le vérificateur est effectué une fois et le chemin accepté avec la plus grande probabilité gagne.`α`par feuille et par jetons totaux par appel de vérificateur.
   Le projet de loi est présenté en ligne par le gouvernement.`[2, 2, 2]`形状的树(8 条候选路径) ▽验证器运行一次,最高概率的接受路径胜出──计算每叶 ▽`α`L'équipe de recherche de la société de l'information et de l'information a été créée en décembre 2009.

4. Implémenter un simulateur de retour KV en lots pour deux séquences concurrentes. La séquence A a accepté tous les projets; la séquence B rejette à la position 2.`kv_length`Il est mis à jour par séquence et aucun travail n'est gaspillé.
   Suivant: réalisation de deux séries de séries de séries KV 回滚模拟器── séries A 所有草稿被接受; séries B 在位置 2 被拒绝──展示正确的`kv_length`按序列更新且无浪费──

5. Lisez la section 4 (Teste de temps de formation) du document EAGLE-3. Expliquez en deux phrases pourquoi la formation naïve au projet sans TTT souffre de biais d'exposition et pourquoi l'alimentation du projet par ses propres prédictions pendant la formation le corrige.
   Le texte de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'é

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Leviathan rule | "min(1, q over p)" | Bernoulli accept/reject with probability `min(1, q(d)/p(d))`, preserves the verifier distribution exactly when you sample from the residual on rejection | Leviathan 规则，精确保持验证器分布的接受/拒绝规则 |
| Residual distribution | "(q minus p) plus, normalized" | `(q - p)_+` clamped at zero and renormalized — the correct distribution to sample from on rejection | 残差分布，拒绝时从中采样的正确分布 |
| Acceptance rate α | "how often the draft is right" | Expected per-token Bernoulli-success probability under the rejection rule; governs all speedup math | 接受率，草稿每 token 的期望成功概率 |
| EAGLE-1 | "hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden state (Li et al., 2024) | EAGLE-1，基于验证器隐藏状态的小型草稿 |
| EAGLE-2 | "dynamic draft tree" | EAGLE-1 plus a tree of candidate continuations scored with tree attention in one verifier pass | EAGLE-2，动态草稿树+树注意力 |
| EAGLE-3 | "training-time test" | Drops the feature-prediction loss, trains on direct token prediction with the draft fed its own outputs during training | EAGLE-3，训练时让草稿自回归生成以匹配推理分布 |
| Training-time test (TTT) | "exposure bias fix" | Run the draft autoregressively during training so train and test input distributions match — the direct analog of scheduled sampling | 训练时测试，解决曝光偏差 |
| KV rollback | "undo rejected drafts" | Bookkeeping that resets the verifier's KV cache to the accepted-prefix length after a rejection | KV 回滚，拒绝后重置 KV 缓存到已接受前缀长度 |
| Bonus token | "the free one" | When all `N` drafts accept, sample one extra from `q_{N+1}` at no additional verifier cost | 奖励 token，全部接受时免费多生成一个 |
| Tree attention | "verify many candidates at once" | Attention with a non-causal mask that respects the topology of a draft tree; computes `q_i` for every node in the tree in one forward pass | 树注意力，一次前向传播验证多个候选 |

## Encore une lecture

- [Leviathan, Kalman, Matias — Fast Inference from Transformers via Speculative Decoding (arXiv:2211.17192, ICML 2023)](https://arxiv.org/abs/2211.17192) le document fondamental et le théorème de l'équivalence
- [Chen et al. — Accelerating Large Language Model Decoding with Speculative Sampling (arXiv:2302.01318)](https://arxiv.org/abs/2302.01318) introduction indépendante concomitante avec une preuve claire
- [Li et al. — EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) EAGLE-1, projet à condition d'état caché
- [Li et al. — EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) recherche dynamique des arbres
- [Li et al. — EAGLE-3: Scaling up Inference Acceleration via Training-Time Test (arXiv:2503.01840, NeurIPS 2025)](https://arxiv.org/abs/2503.01840) la défaillance de la production de 2026
- [Cai et al. — Medusa: Multiple Decoding Heads (arXiv:2401.10774)](https://arxiv.org/abs/2401.10774) approche alternative sans projet
- [vLLM Speculative Decoding documentation](https://docs.vllm.ai/en/latest/features/spec_decode.html) référence canonique de production avec toutes les stratégies câblées
