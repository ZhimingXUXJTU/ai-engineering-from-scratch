# La prédiction multi-tokens (MTP)

> Chaque LLM autorégressif de GPT-2 à Llama 3 est à une perte par position: prédire le prochain jeton. DeepSeek-V3 a ajouté une deuxième perte par position: prédire le jeton après cela. Les paramètres 14B supplémentaires (sur un modèle 671B) ont été distillés dans le modèle principal par le débit de gradient, et les têtes MTP formées ont été réutilisées à l'inférence comme des dessinateurs de décoding spéculatif avec une acceptation de 80%+. La capacité de 1,8 fois de génération est gratuite. Cette leçon construit le module MTP séquentiel du rapport technique DeepSeek, calcule la perte et la disposition des paramètres de tête partagée, et explique pourquoi MTP conserve la chaîne causale alors que le MTP parallèle original de Gloeckle et al. l'a cassé.

> **【中文解读】**传统 LLM chaque position ne prévoit qu'un seul jeton。DeepSeek-V3 augmente une deuxième perte à chaque position: prévoit qu'un seul jeton。Extra 14B 参数 passe par la gradience du flux de réaction du principal modèle, un bon MTP est utilisé comme un éditeur de projet lors de la réflexion(80% + taux d'acceptation),1,8 fois plus de gain de capacité

> **【拓展：MTP→DeepSeek-V3创新】**MTP est l'une des quatre grandes innovations de DeepSeek-V3 (MLA + MoE + MTP + DualPipe) ⋅ elle améliore également la formation (en plus de la capacité de formation et de la formation).

>  **【前置】**Je vous invite à maîtriser la phase 10 de la formation (GPT); la phase 10 de la formation (DECODING)
>  **【类比】**Tradition suivante-token = 学英语时一次记一个单词──MTP = 同时记"这个单词"和"下一个常用搭配"训练时学更多结构(梯度信号丰富),推理时把"搭配预测器"当草稿器免费加速(80% 接受率)

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 10 · 04 (pre-training a mini GPT), Phase 10 · 15 (speculative decoding)
**Time:** ~60 minutes

## Objectifs d'apprentissage

- Indiquer l'objectif de formation MTP et déduire la perte commune sur les profondeurs de prédiction.
  Explication de l'objectif de formation de MTP, de la prévision de la profondeur de perte conjointe
- Expliquez la différence entre les têtes MTP parallèles de Gloeckle et coll. (2024) et les modules MTP séquentiels de DeepSeek-V3 et expliquez pourquoi la conception séquentielle préserve la chaîne causale.
   Expliquer la différence entre le MTP de Gloeckle et le MTP de DeepSeek-V3, ainsi que pourquoi le MTP de Gloeckle est un modèle de conception de la chaîne de résultat.
- Comptez le paramètre et le coût de la mémoire de l'ajout de modules MTP à une course de pré-entraînement.
   calculer les paramètres et la mémoire de MTP 模块 dans la formation préalable
- Mettre en œuvre un module MTP à partir de zéro: l'intégration partagée, le bloc transformateur par profondeur, la projection et la tête de sortie partagée.
  De zéro à réaliser un module MTP: mise en commun par profondeur de transformateur blocs, projection et sortie partagée

## Le problème , l' introduction du problème

La prédiction du prochain jeton est l'objectif standard de formation LLM. Chaque état caché est supervisé pour prédire exactement une chose: le jeton immédiatement suivant. C'est un signal étonnamment faible. La plupart des informations d'une séquence dépassent une structure, une cohérence, une réalité, un flux arithmétique. Le modèle doit les apprendre en accumulant de nombreux signaux d'un seul jeton sur des milliards de jetons.

> Le pronostic est l'objectif de formation standard de la LLM. Chaque état caché est surveillé. Le pronostic est une chose: le prochain jeton est proche. C'est un signal faible étonnant. La plupart des informations du séquence se prolongent vers un seul jeton.

MTP demande: et si chaque état caché était supervisé pour prédire plusieurs tokens futurs à la fois ? Le produit est le produit de l'industrie de l'industrie de l'électricité. (Meta, 2024) a montré que cela aide. Leur mise en œuvre a placé plusieurs têtes de sortie indépendantes sur le dos de la colonne vertébrale, chacune prédisant un décalage différent. Parallèlement, simple, mais les têtes ont vu le même état caché sans aucune affinité hiérarchique et les prédictions ne se sont pas chaînées causellement, de sorte qu'elles ne pouvaient pas être utilisées pour le décoding spéculatif.

> MTP 问: si chaque état caché est surveillé et prédit simultanément plusieurs tokens futur 会怎么样?Gloeckle 等人(Meta,2024) indiquent que cela aide. Leur réalisation a placé plusieurs sorties indépendantes au sommet du réseau de base, chaque prédit ayant des déviations différentes.

DeepSeek-V3 (décembre 2024) a redessiné MTP en tant que modules séquentiels qui maintiennent la chaîne causale à chaque profondeur de prédiction.`t+1`de `h_i^(0)`, puis prédit .`t+2`De l' état caché .`h_i^(1)`qui combiné `h_i^(0)`avec le `E(t+1)`Chaque profondeur est son propre petit bloc transformateur. L'intégration partagée et la tête de sortie partagée maintiennent modeste le paramètre de décomposition. À l'échelle de DeepSeek-V3, 14B paramètres supplémentaires sur les modules MTP en plus des poids du modèle principal 671B. Ce 2% de décomposition achète des signaux d'entraînement plus denses ET un projet de décoding spéculatif prêt à l'inférence.

Cette leçon construit un seul module MTP et la perte de profondeur D à partir de zéro.

## Le concept de base.

> **【中文解读】**Les études de méta montrent que les tests de plusieurs symboles ne permettent pas seulement d'accélérer la formation, mais aussi d'améliorer la capacité de planification et de raisonnement du modèle.

> **【拓展：Meta 的多 token 预测研究】**Meta a publié un article en 2024 indiquant que la prédiction de 4 tokens est nettement supérieure à la norme suivante dans la génération et la logique de code.


### La recette MTP séquentielle

DeepSeek-V3 ajoute `D`Les modules MTP sur le modèle principal.`k`(pour `k = 1..D`) prédit le symbole en profondeur `k` c'est-à-dire, `t_{i+k}`donné un préfixe par position `i`- Je suis désolé .

Module `k`est composé de:

- Un bloc de transformateur `T_k`avec son propre attention et MLP.
- Une matrice de projection `M_k`qui combine l'état caché de profondeur précédent avec l'intégration du symbole de vérité de fond de profondeur suivant.
- L' intégration partagée `E`(même que le modèle principal).
- Le chef de sortie partagé `Out`(même que le modèle principal).

En formation, pour un préfixe par position `i`, l' état caché par profondeur est:

```
h_i^(0) = main model backbone at position i
h_i^(k) = T_k( M_k * concat(RMSNorm(h_i^(k-1)), RMSNorm(E(t_{i+k}))) )   for k >= 1
```

La prédiction par profondeur est:

```
logits_{i+k} = Out(h_i^(k-1))   for k = 1..D
```

La perte de profondeur est une entropie croisée contre la vérité fondamentale .`t_{i+k}`- Le numéro de la liste:

```
L_k = CE(logits_{i+k}, t_{i+k})
```

La perte articulaire à travers les profondeurs:

```
L_MTP = (lambda / D) * sum_{k=1..D} L_k
```

`lambda`Le coefficient de pondération est faible  DeepSeek-V3 utilise 0,3 pour les 10% de formation et 0,1 après.`L_main + L_MTP`- Je suis désolé .

### Pourquoi séquentielle, pas parallèle

Le MTP parallèle original de Gloeckle avait des têtes de sortie D, chacune directement appliquée à `h_i^(0)`Chaque tête prédit .`t_{i+k}`C'est bien, mais les prédictions ne sont pas conditionnées l'une sur l'autre.`head_1`- La sortie pour aider .`head_2` les têtes tirent en parallèle.

Le design séquentiel de DeepSeek-V3 construit `h_i^(k)`de `h_i^(k-1)`plus l' intégration réelle du jeton suivant `E(t_{i+k})`- C' est la chaîne de causalité .`t_{i+k+1}`, le module à profondeur `k+1`Il voit ce qui se passe .`t_{i+k}`. Ceci est structurellement identique à la façon dont un décodeur autorégressif consomme sa propre sortie  rendant les modules MTP directement utilisables comme dessinateurs de décodeurs spéculatifs.

À la conclusion: fourrage `h_i^(k-1)`et le projet `t_{i+k}`dans le module `k+1`, obtenir une prédiction pour `t_{i+k+1}`C'est exactement un projet de style EAGLE, en utilisant le module MTP formé comme le projet de réseau. DeepSeek-V3 rapporte une acceptation de plus de 80% sur le premier module MTP et une accélération de ~1,8x.

### Comptabilité des paramètres

Pour un modèle avec caché `h`et le vocabulaire `V`- Le numéro de la liste:

- Modèle principal: milliards de paramètres, plus une tête de sortie de taille `V * h`- Je suis désolé .
- Cap de sortie partagée: réutiliser la tête du modèle principal.
- Embedding partagé: réutiliser l'embedding du modèle principal.
- Module par MTP:
  - La projection `M_k`Le numéro de la liste:`(2h) * h = 2h^2`- Je suis désolé .
  - Bloc de transformateur `T_k`Attention (`4h^2`pour MHA) plus MLP (généralement `8h^2`pour SwiGLU avec un rapport de 8/3).`12h^2`par bloc.

Total supplémentaire par module: `~14h^2`Pour les DeepSeek-V3.`h = 7168`, D = 1 module: `~14 * 7168^2 = ~720M`Les paramètres sur papier. DeepSeek-V3 rapporte 14B  la différence est principalement des couches d'experts étant MoE dans le module MTP aussi.

### Le paiement de décoding spéculatif

Pendant la pré-entraînement, les modules MTP ralentissent l'entraînement d'environ 10% (plus de calculs avancés, plus de pertes).

1. Signal d'entraînement de densité. Chaque état caché voit des cibles de surveillance D+1. Effets mesurés sur MMLU, GSM8K, MATH, HumanEval: améliorations constantes de quelques points de pourcentage dans les ablations de DeepSeek-V3.

2. Le module MTP est déjà formé pour prédire les prochains jetons. Résumé réseau, il fournit 80% + taux d'acceptation. À ce niveau, N = 3 ou N = 5 spécification décoding donne 1,8 × débit. Le coût de formation de 10% de temps se rembourse la première fois que vous exécutez une inférence.

### Relation avec l'AIGLE

L'Eagle entraîne séparément un petit modèle de projet après la pré-formation.

| Dimension | EAGLE-3 | MTP (DeepSeek-V3) |
|-----------|---------|------------------|
| When trained | Post-pre-training | During pre-training |
| Backward-compatible with existing weights | Yes | No (need to re-train) |
| Draft params | 1-2 transformer layers | 1 transformer block + projection |
| Acceptance rate | 0.88-0.92 | 0.80+ at depth 1 |
| Benefit beyond speedup | Speculative decoding only | Denser training signal + speedup |


> **【拓展：多 token 预测与推理加速的联系】**Les méthodes de formation de prédiction de 4 symboles sont généralement utilisées pour la génération de codes, car elles ont déjà appris à prévoir de nombreux symboles futurs.


## Construisez-le et mettez-le en œuvre.
```figure
multi-token-predict
```

## Faites-le

`code/main.py`Il construit un seul module MTP de bout en bout: intégration partagée, projection, bloc transformateur, tête de sortie partagée. Il calcule ensuite la perte de l'entropie croisée par profondeur sur une courte séquence synthétique et imprime le nombre de paramètres par composant. Un vocabulaire de jouets de 32 jetons garde les nombres lisibles.

### Étape 1: Table d'intégration partagée

Une seule .`vocab_size x hidden`La table est utilisée par le modèle principal ET par chaque module MTP à chaque profondeur.

### Étape 2: la combinaison par profondeur

```python
def combine(prev_hidden, next_token_embed, M_k):
    # concat along feature dim, then project down to hidden
    concat = rms_norm(prev_hidden) + rms_norm(next_token_embed)  # vector addition stand-in
    projected = matvec(M_k, concat)
    return projected
```

Réel DeepSeek-V3 concatenant les deux vecteurs RMSNormed à `[2h]`et des projets avec un`h x 2h`Le jouet utilise l'addition vectorielle pour la brèveur stdlib.

### Étape 3: le bloc de transformateur à la profondeur k

L'auto-attention plus le MLP. Dans le jouet, un bloc d'attention linéaire à couche unique et un SwiGLU MLP gardent la structure visible sans numpy.

### Étape 4: la tête de sortie partagée

Reutilisez la projection de sortie du modèle principal.

### Étape 5: Perte par profondeur

Entropie croisée de softmax (logits) contre le jeton de vérité au sol à compensation `k`- Aggreger à travers les profondeurs avec le`lambda / D`facteur d'échelle.

### Étape 6: comptabilité des paramètres

Imprimez le nombre total de paramètres, le nombre partagé (intégration, tête) et le nombre supplémentaire par module. Affichez le rapport entre MTP supplémentaire et taille du modèle principal.

## Utilisez-le avec le cadre de réalisation

MTP est intégré à DeepSeek-V3 (décembre 2024) et à la série DeepSeek-R1.

- La pile de serveurs de DeepSeek consomme des modules MTP comme décodeurs spéculatifs hors de la boîte.
- VLLM et SGLang ont des voies d'intégration pour DeepSeek-V3 MTP à compter d'avril 2026.
- Le tutoriel ROCm SGLang d'AMD montre une configuration spécifique de décoding spéculatif MTP avec une vitesse mesurée de 1,8 fois sur le point de contrôle V3.

Quand utiliser MTP dans une nouvelle course pré-entraînement:

- Vous contrôlez le pipeline de formation et vous voulez un signal d'entraînement plus dense.
- Vous savez que vous allez servir le modèle à l'échelle et voulez le décoding spéculatif gratuitement.
- Votre taille cachée est au moins 4096.

Quand ne pas:

- - l'ajustement de l'état de la machine à sous, le module MTP n'est pas formé.
- Les modèles de recherche où vous voulez une ligne de base propre à comparer.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-mtp-planner.md`. Compte tenu d'une spécification préalable à la formation (taille du modèle, données, calcul), il renvoie un plan d'intégration de MTP: nombre de profondeurs D, `lambda`le calendrier, le débit de mémoire et le câblage de décodage spéculatif de l'inférence-temps.

> 本课产 出 `outputs/skill-mtp-planner.md`◊ given given pre training运行规范(模型大小、数据、算力), il retourne à l'intégration du plan de MTP:`lambda`调度、内存开销和推理时投机解码连线──

## Les exercices

1. On court .`code/main.py`.Montrez que la perte par profondeur diminue de manière monotone à mesure que le signal synthétique se renforce.Modifiez le synthétique pour utiliser un schéma fixe et vérifiez la convergence des pertes de profondeur-1 et de profondeur-2.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` démontrer chaque perte de profondeur avec le signal synthétique augmenter un seul mode de transmission.

2. Comparer le coût de chargement des paramètres pour un modèle dense 70B (casqué 8192, 80 couches) avec un module MTP D = 1. Comparer avec le coût de chargement 14B rapporté par DeepSeek-V3. Expliquez pourquoi le nombre de DeepSeek est plus élevé: le bloc de transformateur MTP hérite de la même structure MoE, gonflant le nombre de paramètres par module.
   Le nombre de modules de MTP est inférieur à celui de MTP. Le nombre de modules de MTP est inférieur à celui de MTP.

3. Implémentation D=2 dans le jouet: ajouter un deuxième module MTP qui prend h^(1) et prédit `t_{i+2}`Vérifiez que la perte commune et la comptabilité des paramètres correspondent aux équations 19 à 21 du document DeepSeek.
   Dans le modèle de jouets réalisé D=2: Ajouter un deuxième MTP, prendre h^(1) 并预测 `t_{i+2}` L'évaluation des pertes et des pertes combinées avec le calcul des paramètres avec la formule du thèse de DeepSeek 19-21 匹配──

4. Transférez le jouet en MTP parallèle (style Gloeckle): ajoutez des têtes de sortie D au-dessus de l'état caché principal, chacune prédisant un décalage différent. Mesurez comment les pertes par profondeur se comparent à la version séquentielle sur le même signal synthétique. La version séquentielle devrait produire une perte de profondeur de plus faible pour k > 1 car elle conditionne les prédictions intermédiaires.
   Le modèle de jouets est modifié en MTP (Gloekle style): dans l'état d'origine, chaque prédiction est différente.

5. Utilisez le module MTP formé comme un projet de style EAGLE: appelez le module k pour proposer `t_{i+k}`Si vous atteignez 50%+ sur le jouet, vous avez reproduit la propriété empirique MTP-as-draft.
   Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEFOP) a été adopté par le Conseil européen de l'emploi (CEP) en juin 2014.`t_{i+k}` Mesurer ces jetons de projet sur la séquence de réservation pour le taux d'acceptation des prévisions du modèle principal. Si le modèle de jouets atteint 50%+, vous avez déjà réussi à reproduire les caractéristiques de l'expérience de MTP-as-draft.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| MTP module | "Extra loss block" | A small transformer block plus projection that predicts a token `k` positions ahead of the main model | MTP 模块，预测主模型后方第 k 个 token |
| Prediction depth | "Which offset" | The integer `k` such that module `k` predicts `t_{i+k}` from prefix through position `i` | 预测深度，模块 k 预测第 i+k 个 token |
| Parallel MTP | "Gloeckle-style" | D independent heads on the same backbone hidden state, no conditional chain | 并行 MTP，D 个独立头共享隐状态 |
| Sequential MTP | "DeepSeek-V3 style" | Each module conditions on the previous depth's hidden state plus the next token's embedding; preserves causal chain | 顺序 MTP，每层依赖前一层隐状态，保持因果链 |
| Shared output head | "Reuse the main head" | The MTP modules call the main model's LM head, not a separate output projection | 共享输出头，MTP 模块复用主模型的语言模型头 |
| Shared embedding | "Reuse the main table" | Same vocabulary embedding table is used everywhere; no duplicate parameters | 共享嵌入，复用词表嵌入表 |
| Projection matrix M_k | "Combine hidden + next-token" | An `h x 2h` linear层 that folds the previous hidden state and the target-token embedding into the next depth's input | 投影矩阵，组合隐状态与下一 token 嵌入 |
| Joint loss L_MTP | "Averaged extra losses" | Arithmetic mean of per-depth cross-entropy losses, scaled by `lambda` | 联合损失，各深度交叉熵损失的算术均值 |
| Acceptance rate at depth 1 | "How often MTP draft is right" | The rate at which the D=1 MTP module's top-1 prediction equals the main model's top-1 prediction; 80%+ on DeepSeek-V3 | 深度 1 的接受率，MTP 草稿与主模型一致的概率 |
| Lambda weighting | "Extra-loss importance" | Per-depth scaling factor; 0.3 at start of training, 0.1 later on DeepSeek-V3 | Lambda 权重，每深度损失的缩放因子 |

## Encore une lecture

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) la description complète du MTP séquentiel (section 2.2), y compris les équations de perte articulaire et la vitesse de 1,8 fois à l'inférence
- [Gloeckle et al. — Better & Faster Large Language Models via Multi-token Prediction (arXiv:2404.19737)](https://arxiv.org/abs/2404.19737) la ligne de base parallèle MTP
- [DeepSeek-V3 model card on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3) 685 B au total (671 B principal + 14 B MTP), notes de déploiement
- [Leviathan et al. — Fast Inference from Transformers via Speculative Decoding (arXiv:2211.17192)](https://arxiv.org/abs/2211.17192) le cadre de décoding spéculatif MTP s'intègre dans
- [Li et al. — EAGLE-3 (arXiv:2503.01840)](https://arxiv.org/abs/2503.01840) L'architecture de projet de 2025 de l'Eagle, l'équivalent MTP, est en concurrence avec
