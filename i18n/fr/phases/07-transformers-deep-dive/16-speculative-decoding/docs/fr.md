# Décodage spéculatif  Développe, vérification, répétition  Découverte  Développe 验证、重复

> Le décoding autorégressif est sériel. Chaque jeton attend le précédent. Le décoding spéculatif rompt la chaîne: un modèle bon marché rédige N jetons, le modèle cher vérifie tous N en un seul passe avant. Lorsque le projet est correct, vous payez un gros avant pour N générations.

> **【中文解读】**Utilisez un petit modèle rapide générateur de jetons de candidature, un grand modèle de test de masse.

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Un échantillonnage de 70B LLM d'un jeton prend ~ 30 ms sur un H100. Un modèle de projet 3B prend ~ 3 ms. Si nous laissons le projet 3B 5 jetons en avant, puis exécutez le 70B * une fois * pour vérifier tous les 5, le total est `5×3 + 30 = 45 ms`pour un maximum de 5 jetons acceptés  versus `5×30 = 150 ms`C'est le pitch complet du décoding spéculatif: échanger une petite quantité de mémoire de GPU supplémentaire (modèle de projet) pour une latence de décoding inférieure de 24x.

> Un modèle de projet de loi de 70B 采样一个代币 在H100上需要约30 ms──一个3B草案模型需要约3 ms──如果我们让3B提前生成5代币,然后运行70B *一次*验证所有5个,总时间为`5×3 + 30 = 45 ms`Le plus possible de 5 tokens acceptés et de génération directe`5×30 = 150 ms`                                                                                                                                                                                                                                                              

L'échantillonnage spéculatif, introduit par Leviathan et coll. (2023) et par Chen et coll. simultanément, garantit que la séquence de sortie est **identically distributed**Il n'y a pas de compromis de qualité, juste plus vite.

> Cette technique doit être maintenue en constante répartition.**完全相同**Il n'y a pas de perte de qualité.

Quatre familles de paires de vérificateurs de projet dominent l'inférence 2026:

> Les quatre types de projets-certificateurs devraient prendre la place dominante dans la proposition de 2026:

1. **Vanilla speculative (Leviathan 2023).**Modèle de projet séparé (p. ex. Llama 3 1B) + vérificateur (p. ex. Llama 3 70B).
   Le mot grec traduit par " le mot grec "**朴素推测（Leviathan 2023）。**独立的草案模型(如 Llama 3 1B) + 验证器(如 Llama 3 70B) ⋅
2. **Medusa (Cai 2024).**Plusieurs têtes de décoding sur la position de prédiction du vérificateur `t+1..t+k`Pas de modèle de projet séparé.
   Le mot grec traduit par " le mot grec "**Medusa（Cai 2024）。**Plusieurs décompteurs sur l'étiquette et position de prédiction`t+1..t+k`无需独立草案模型──
3. **EAGLE family (Li 2024, 2025).**Draft léger qui réutilise les états cachés du vérificateur; taux d'acceptation plus proche que la vanille; 34× typique.
   Le mot grec traduit par " le mot grec "**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案; acceptation rate par rapport au simple programme est plus élevé; accélération typique 3-4 fois:
4. **Lookahead decoding (Fu 2024).**Je ne suis pas un modèle de projet, je ne suis pas une spéculation, je suis un peu dépendant.
   Le mot grec traduit par " le mot grec "**前瞻解码（Fu 2024）。**Je suis un homme qui a une grande expérience de la vie.

Chaque pile d'inférence de production en 2026 envoie par défaut un décodeur spéculatif. vLLM, TensorRT-LLM, SGLang et llama.cpp prennent tous en charge au moins la vanille + EAGLE-2.

> Chaque production de 2026 est assurée par le système de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de production de la ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne de ligne

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B)快速生成 N 个候选代币,大模型(70B) une fois à l'avant pour la propagation验证所有 N 个──总时间从 N×30ms 降至 5×3+30=45ms,加速 2-4 倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**EAGLE(2024) Réutiliser l'état caché du grand modèle pour générer un projet, le taux d'acceptation est plus élevé que celui du petit modèle indépendant, l'accélération typique est de 3-4 fois.

## Le concept de base.

### L'algorithme de base

En raison d' un vérificateur `M_q`et un projet moins cher `M_p`- Le numéro de la liste:

> 给定验证器 `M_q`Et plus abordable`M_p`- Le numéro de la liste:

1. Je vous laisse .`x_1..x_k`être le préfixe déjà décodé.
   Le mot "je" est traduit par "je"`x_1..x_k`Pour le code de la première.
2. **Draft**: utilisation `M_p`à proposer de manière autorégressive `d_{k+1}, d_{k+2}, ..., d_{k+N}`avec des probabilités de projet `p_1..p_N`- Je suis désolé .
   Le mot grec traduit par " le mot grec "**草案**: usage `M_p`Proposition de réintégration`d_{k+1}, d_{k+2}, ..., d_{k+N}`,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `p_1..p_N`Il y a une autre.
3. **Verify in parallel**: courir `M_q`Une fois de plus .`x_1..x_k, d_{k+1}, ..., d_{k+N}`, obtenir des probabilités de vérification `q_1..q_{N+1}`pour les positions `k+1..k+N+1`- Je suis désolé .
   Le mot grec traduit par " le mot grec "**并行验证**Pour le`x_1..x_k, d_{k+1}, ..., d_{k+N}`Une fois .`M_q`, obtenir une position`k+1..k+N+1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `q_1..q_{N+1}`Il y a une autre.
4. **Accept/reject each draft token left to right**: pour chacun `i`, accepter avec probabilité `min(1, q_i(d_i) / p_i(d_i))`- Je suis désolé .
   Le mot grec traduit par " le mot grec "**从左到右接受/拒绝每个草案 token**Pour chacun`i`, en général`min(1, q_i(d_i) / p_i(d_i))`- Je le sais.
5. Au premier rejet à la position `j`: échantillon `t_j`de la distribution "résiduelle" `(q_j - p_j)_+`Tous les projets après`j`sont jetés.
   En français, dans la langue française`j`首次被拒绝时: de la distribution des "résidu"`(q_j - p_j)_+`归一化后采样 `t_j`Il y a une autre.`j` après tout projet a été abandonné
6. En acceptant tout .`N`: échantillon d' un jeton supplémentaire `t_{N+1}`de `q_{N+1}`(le jeton bonus gratuit).
   Le nom de la ville est le nom de la ville.`N`个都被接受时: depuis `q_{N+1}`采样一个额外的标志 `t_{N+1}`(tone de récompense gratuit)

Le truc de distribution résiduelle est la compréhension mathématique qui maintient la sortie distribuée exactement comme si `M_q`J'avais pris des échantillons à partir de zéro.

> La technique de distribution des différences est de maintenir la distribution des sorties et des sorties.`M_q`Il y a des mathématiques qui sont exactement les mêmes.

### Ce qui détermine la vitesse

Je vous laisse .`α`= taux d'acceptation attendu par jeton projet.`c`= rapport coût entre projet et vérificateur.

> 设 `α`= Le taux d'acceptation anticipé de chaque jeton de projet.`c`= coût du projet et du test par étape:

- La génération naïve fait un appel de modèle par jeton.
  Le mot "grand modèle" est traduit par "grand modèle".
- La spéculative fait un appel de modèle par personne .`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`les jetons quand `α`C'est élevé.
  Le mot " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " est dé dé dé dé dé dé dé dé dé dé dé dé dé dé dé " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "`α`较高时,每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`个代币 调用一次大模型──

La règle typique est que `α = 0.75`et `N = 5`Le coût du projet est 5 fois moins cher.

> `α = 0.75`et `N = 5`Le temps de révision des projets est de 5 fois moins cher.

> **【中文解读】**Le résidu de la distribution résiduelle est un élément clé de la répartition cohérente. Le rejet de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition résiduelle est un élément clé de la répartition cohérente.

**α depends on:**

> **α 取决于：**

- La qualité de la rédaction approximative du vérificateur.
  Le projet de loi sur la quasi-souvenir des éprouvateurs
- Stratégie de décoding: projet avide contre vérificateur avide: élevé α. Prélèvement d'échantillons à température: plus difficile à faire correspondre; acceptation diminue.
  Le taux de réception est en baisse.
- Type de tâche: le code et la sortie structurée acceptent plus (prévisible); l'écriture créative sous forme libre accepte moins.
  Traduction anglaise: tâche type.

### Medusa  projets sans modèle de projet

Medusa remplace le modèle de projet par des têtes de sortie supplémentaires sur le vérificateur.`t`- Le numéro de la liste:

> Medusa utilise le test de l'extérieur de l'exportation de la conception de modèle de remplacement.`t`- Le numéro de la liste:

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Chaque tête produit ses propres logits. À l'inférence, vous prenez un échantillon de chaque tête pour obtenir une séquence de candidats, puis vérifiez avec un passage vers l'avant en utilisant un schéma d'attention à l'arbre qui considère toutes les continuations de candidats à la fois.

> Chaque tête sort ses propres logits. La recommandation est de prendre chaque échantillon dans la séquence de candidatures, puis d'utiliser le schéma d'attention pour une fois la propagation de la vérification, tout en considérant les candidatures.

Avantages: pas de deuxième modèle. inconvénients: ajoute des paramètres entraînables; nécessite une phase de réglage fin supervisée (~ 1B tokens); taux d'acceptation est un peu inférieur à la spéculative de vanille avec un bon projet.

> 优点:无需第二模型──缺点:增加可训练参数;需要监督微调阶段(约1B token); acceptation rate比好的草案模型的朴素推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**Le vLLM est le cadre de recherche de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de logiciels de

### L'AIGLE  meilleur dessin en réutilisant les états cachés

EAGLE-1/2/3 (Li et al., 20242025) fait du modèle de projet un minuscule transformateur (typiquement 1 couche) qui ingère les états cachés de la dernière couche du vérificateur.

> EAGLE-1/2/3 ((Li 等人,2024-2025)) va faire du modèle du projet un transformateur micro (généralement 1 niveau), l'état caché de la dernière couche de l'étiquette d'absorption.

EAGLE-3 (2025) a ajouté la recherche d'arbres sur les continuations candidates. vLLM et SGLang ont utilisé EAGLE-2/3 comme voie de spécification par défaut pour Llama 3/4 et Qwen 3.

> EAGLE-3(2025) a ajouté à la recherche des arbres pour les candidats à la présidence.

### La danse du cache KV

Feeds de vérification `N`Les jetons de projet dans le vérificateur en un seul passage.`N`Si certains projets sont rejetés, vous devez faire glisser le cache à la longueur du préfixe accepté.

> 验证在一次前向传播中将 `N`个草案 token 输入验证器── ceci va permettre à la KV 缓存扩展 `N`个条目── Si certains projets sont rejetés, vous devez les mettre en cache jusqu'à la durée de leur acceptation.

Les actions de production (vLLM) `--speculative-model`Je suis en train de faire une réflexion sur le sujet, et je suis en train de faire une réflexion sur le sujet.

> Produit réalisé`--speculative-model`、TensorRT-LLM's LookaheadDecoder) utilise le KV provisoire 缓冲区 pour traiter ce problème──pre-écrire, accepter lors de la soumission──conceptation sur pas difficile, mais réaliser sur la comparaison difficile──

## Construisez-le et mettez-le en œuvre.
```figure
draft-verify-tokens
```

## Faites-le

Regardez !`code/main.py`Nous mettons en œuvre l' algorithme de prélèvement de l' échantillonnage spéculatif de base (étape de rejet + distribution résiduelle) avec:

> 参见 `code/main.py`◊ Nous utilisons les composants suivants pour réaliser le système de calcul de base:

- Un " grand modèle " qui est un déterminisme-softmax sur une distribution codée à la main (donc nous pouvons vérifier l'acceptation mathématique analytique).
  Un " grand modèle " est une détermination de la distribution de code manuel à la plus grande échelle.
- Un "modèle de projet" qui est une perturbation du grand modèle.
  Le projet modèle est une version perturbée du modèle.
- Une boucle d'acceptation/déni qui produit la même distribution marginale que l'échantillonnage direct.
  Un cycle de acceptation/déni, produisant une distribution de la même ligne que le modèle direct.

### Étape 1: étape de rejet

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`est un nombre aléatoire uniforme. `q_prob`est la probabilité du vérificateur pour le jeton rédigé. `p_prob`Le théorème de Leviathan est que cette décision de Bernoulli, suivie d'un échantillonnage du résidu sur le rejet, préserve exactement la distribution du vérificateur.

> `u`C'est le nombre moyen.`q_prob`La probabilité de dépôt de jetons de projet est`p_prob`Le principe de Leviathan indique que cette décision de calcul, ainsi que le rejet des échantillons de résidu, peut assurer la distribution des détenteurs de certificats.

### Étape 2: répartition résiduelle

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Soustraire`p`de `q`En fonction des éléments, cliquez sur les valeurs négatives à zéro, renormez.

> Œuvres de l'homme`q`- Je ne sais pas .`p`, va être réduit à zéro, re-régulier à zéro.

### Étape 3: une étape spéculative

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Cinq acceptés → un bonus → six jetons produits dans un passe de vérification.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币──

### Étape 4: mesurer le taux d'acceptation

Exécutez 10 000 étapes spéculatives à différents niveaux de qualité du projet. Taux d'acceptation du plot par rapport à la divergence KL entre les distributions du projet et du vérificateur. Vous devriez voir une relation monotone propre.

> Dans le même temps, les résultats de la recherche ont été obtenus en termes de résultats de recherche et de résultats de recherche.

### Étape 5: vérifier l'équivalence de la distribution

En empirie, l'histogramme des jetons produit par la boucle spéculative doit correspondre à l'histogramme produit par le prélèvement d'échantillons directement depuis le vérificateur.

> √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √

## Utilisez-le avec le cadre de réalisation

Produit:

> La mise en œuvre de la politique de sécurité

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM a le chemin le plus rapide de Méduse à partir de la mi-2026. `faster-whisper`Enveloppe le décodeur spéculatif pour Whisper-large avec un petit morceau.

> Le RTLM possède le plus rapide chemin de la Méduse en 2026`faster-whisper`Pour le grand sourire, utilisez le petit modèle de projet.

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Génération de 15 jetons en séquence unique.
  Le nombre de symboles est de 1 à 5 générations.
- Prise d'échantillons à haute température (â gouttes).
  Le niveau de température est de 7 à 7 degrés.
- Déploiements limités par mémoire (modèle de projet ajoute VRAM).
  Le projet de loi est une loi qui a été adoptée par le gouvernement de l'État de Hongrie.

## Envoyez-le . Produit .

Regardez !`outputs/skill-spec-decode-picker.md`. La compétence choisit une stratégie de décoding spéculative (vanille / Medusa / Eagle / lookhead) et des paramètres de réglage (N, température de projet) pour une nouvelle charge de travail d'inférence.

> 参见 `outputs/skill-spec-decode-picker.md`◊ Ce savoir-faire pour un nouveau projet ◊ Le projet de loi

## Les exercices

1. **Easy.**On court .`code/main.py`. Confirmer que la distribution de jetons spéculatifs correspond à la distribution de l'échantillon direct du vérificateur sur 50 000 jetons dans un espace de p = 0,05 en chi-quare.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmation de 50 000 tokens, distribution des tokens de proposition par le testateur et échantillonnage direct distribué dans le test de carte p > 0,05 en correspondance
2. **Medium.**Accélération de l'intrigue (tokens par grand modèle à l' avance) en fonction de `N`pour `α = 0.5, 0.7, 0.85`- Identifier le meilleur`N`pour chaque α. (indice: jetons attendus par appel de vérification = `(1 - α^{N+1}) / (1 - α)`(dont le nom est
   Le dessin`α = 0.5, 0.7, 0.85`时加速比( par grande modèle de précédent numéros de jetons)`N`                                                                                                                                                                                                                                                              `N`◊                                                                                                                                                                                                                                                              `(1 - α^{N+1}) / (1 - α)`◊)
3. **Hard.**Mettez en œuvre une minuscule méduse: prenez la pierre angulaire GPT de la leçon 14, ajoutez 3 têtes LM supplémentaires qui prédisent les positions t+2, t+3, t+4.
   Le projet de formation de la méduse de la méduse de la méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méduse de méd
4. **Hard.**Retour à l'emploi: commencez par un préfixe KV de 10 jetons, alimentez 5 jetons de projet, simuliez un rejet à la position 3. Vérifiez que vos lectures de cache correspondent correctement au " préfixe + 2 premiers projets acceptés " à la prochaine itération.
   Le code de réception est le code de réception de la carte de réception.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Encore une lecture

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) l'algorithme de base et le théorème de l'équivalence.
  Le concept de la théorie de l'équation est le concept de l'équation.
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) introduction concomitante; preuve de rejet de Bernoulli.
  Le texte de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de l' du deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Papel de méduse; vérification de l'attention aux arbres.
  Le médoiseur est un homme qui a une grande expérience de la vie.
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) EAGLE-1; projet à condition d'état caché.
  Le projet de loi de l'État de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l'Etat de l
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) AGLE-2; profondeur dynamique des arbres.
  Le récit de la première partie de la série est le récit de l'époque.
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840)- Il est à l'Eagle-3.
  Le texte de l'article est le suivant:
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057)- Attention, approche sans projet.
  Le texte de la loi est en français.
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) référence canonique de production avec les quatre stratégies câblées.
  Le projet de loi de la loi de l'Union européenne sur les droits de l'homme est une loi de l'Union européenne sur les droits de l'homme.
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) le code de référence de l'EAGLE-1/2/3.
  Le code de réaction est le code de réaction.
