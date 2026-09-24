# Le mécanisme d'attention La percée Le mécanisme d'attention La rupture centrale du transformateur

> Le décodeur arrête de cligner des yeux sur un résumé comprimé et commence à regarder l'ensemble de la source.
> Le décodeur cesse de regarder le résumé, commence à regarder vers l'ensemble de la source.

> **【中文解读】**Le mécanisme de concentration fait que le modèle se concentre sur les parties connexes de l'entrée.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

La leçon 09 se termine par une défaillance mesurée. Un encodeur-décodeur GRU entraîné sur une tâche de copie de jouet passe de 89% de précision à longueur 5 à près de chance à longueur 80. La raison est structurelle, pas un bug d'entraînement: chaque bit d'information recueilli par l'encodeur doit s'intégrer dans un état caché de taille fixe, et le décodeur ne voit jamais autre chose.

> Le GRU codeur-décifleur entraîné à la tâche de copie de jouets à la longueur de 5 heures 89% de précision, à la longueur de 80 heures de proximité avec le temps. La raison est structurelle, pas un bug d'entraînement: chaque élément de l'information collectée par le codeur doit être placé dans un état caché de taille fixe, le décodeur ne regarde rien d'autre.

Bahdanau, Cho et Bengio ont publié une correction en trois lignes en 2014. Au lieu de donner au décodeur seulement l'état final de l'encodeur, gardez chaque état de l'encodeur. À chaque étape du décodeur, calculez une moyenne pondérée des états de l'encodeur où les poids disent "combien le décodeur a besoin de regarder la position de l'encodeur `i`Cette moyenne pondérée est le contexte, et elle change chaque étape du décodeur.

> Bahdanau、Cho 和 Bengio a publié en 2014 une troisième revue. Il ne donne pas seulement à l'éditeur l'état du codeur final, mais il conserve l'état de chaque codeur.`i`" Cette augmentation de la moyenne est sur la base, elle change à chaque étape du décodeur.

C'est l'idée. Les transformateurs l'ont étendue. L'attention personnelle l'a appliquée à une seule séquence. L'attention multi-têtes l'a couru en parallèle. Mais la version 2014 a déjà brisé le gouffre, et une fois que vous l'avez, le pivot des transformateurs est l'ingénierie, pas conceptuelle.

> C'est tout l'idée. Le Transformer l'a étendue. L'attention s'est appliquée à un seul processus.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

À chaque étape du décodeur `t`- Le numéro de la liste:

> Dans chaque étape de la rédaction `t`- Le numéro de la liste:

1. Utilisez l' état caché du décodeur précédent `s_{t-1}`comme une **query**- Je suis désolé .
2. Réservez-le à chaque état caché du codeur .`h_1, ..., h_T`Un scalaire par position d'encodeur.
3. Softenmax les scores pour obtenir des poids d' attention `α_{t,1}, ..., α_{t,T}`Cette somme est de 1.
4. Vecteur de contexte `c_t = Σ α_{t,i} * h_i`- moyenne pondérée des états de l'encodeur.
5. Le décodeur prend `c_t`plus le jeton de sortie précédent, produit le jeton suivant.
   1. Utilisation précédente Un décodeur caché état `s_{t-1}` comme**查询（Query）**Il y a une autre.
   2. Le mettre dans un état caché avec chaque codeur.`h_1, ..., h_T`Chaque éditeur a une taille.
   3. Pour le fractionnement à la plus grande douceur , on obtient un poids d' attention .`α_{t,1}, ..., α_{t,T}`, en tout et pour 1
   4.  上下文向量 `c_t = Σ α_{t,i} * h_i`◊ augmentation du pouvoir moyen de l'état du codeur
   5. - Je suis un homme !`c_t`Avec le premier jeton de sortie, générer le deuxième jeton.

La moyenne pondérée est le point. Lorsque le décodeur doit traduire "Je" en "I", il pèse l'état de l'encodeur sur "Je" élevé et les autres bas. Quand il a besoin de "non", il pèse "pas" élevé. Le vecteur de contexte remodèle chaque étape.

> Le temps de rédaction est un temps de rédaction de la note de rédaction.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Les formes (ce qui mord tout le monde)

C'est là que chaque mise en œuvre de l'attention va mal la première fois.

> C'est là que chaque attention est mise pour la première fois.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Je suis désolé .

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`Il y a une autre.

- `s_{t-1}`a une forme`(d_s,)`- Je suis là .`h_i`a une forme`(d_h,)`- Je suis désolé .
- `W_a`a une forme`(d_attn, d_s)`- Je suis là .`U_a`a une forme`(d_attn, d_h)`- Je suis désolé .
- Leur somme à l'intérieur du tanh a une forme .`(d_attn,)`- Je suis désolé .
- `v_α`a une forme`(d_attn,)`- Le produit intérieur avec`v_α`Il s'effondre à un escalier.**This is what `v_α` does.**Ce n'est pas de la magie, c'est la projection qui transforme un vecteur attentif en un score scalaire.
  - `s_{t-1}`形状为 `(d_s,)`- Je suis désolé .`h_i`形状为 `(d_h,)`Il y a une autre.
  - `W_a`形状为 `(d_attn, d_s)`Il y a une autre.`U_a`形状为 `(d_attn, d_h)`Il y a une autre.
  - et forme de la`(d_attn,)`Il y a une autre.
  - `v_α`形状为 `(d_attn,)` avec`v_α`Le nombre de personnes qui ont été arrêtées est de plus en plus élevé.**这就是 `v_α` 的作用。**Ce n'est pas magique. C'est une projection de la dimension d'attention et du moment de projection.

**Luong (multiplicative) score.**Trois variantes:

> **Luong（乘性）分数。**Trois changements:

- `dot`Le numéro de la liste:`e_{t,i} = s_t^T * h_i`- Il faut .`d_s == d_h`- Passer si votre encodeur est bidirectionnel.
  `dot`- Le numéro de la liste:`e_{t,i} = s_t^T * h_i` les exigences`d_s == d_h`Si le codeur est à double sens, il saute.
- `general`Le numéro de la liste:`e_{t,i} = s_t^T * W * h_i`avec `W`forme `(d_s, d_h)`- Il supprime la contrainte de l'égalité de la teinte.
  `general`- Le numéro de la liste:`e_{t,i} = s_t^T * W * h_i`- Je suis désolé .`W`形状为 `(d_s, d_h)`❖ Le déplacement et la mise en place
- `concat`Le format Bahdanau est essentiellement le même.
  `concat`La forme Bahdanau est en fait plus abordable, elle est très peu utilisée.

**One Bahdanau / Luong gotcha worth naming.**Bahdanau utilise `s_{t-1}`(l'état du décodeur * avant * de générer le mot courant).`s_t`Le mélange produit des gradients subtilement erronés qui sont extrêmement difficiles à débogager.

> **一个值得注意的 Bahdanau / Luong 陷阱。**Bahdanau 使用 `s_{t-1}`(生成当前词*之前*的解码器状态) ―Long 使用 `s_t`(après le * état) ◊ Les conflits se produisent à un degré de délicatesse et de délicatesse.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
attention-heatmap
```

## Faites-le

### Étape 1: attention additive (Bahdanau)

```python
import numpy as np


def additive_attention(decoder_state, encoder_states, W_a, U_a, v_a):
    projected_dec = W_a @ decoder_state
    projected_enc = encoder_states @ U_a.T
    combined = np.tanh(projected_enc + projected_dec)
    scores = combined @ v_a
    weights = softmax(scores)
    context = weights @ encoder_states
    return context, weights


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / e.sum()
```

Vérifiez vos formes contre la table ci-dessus. `encoder_states`a une forme`(T_enc, d_h)`- Je suis là .`projected_enc`a une forme`(T_enc, d_attn)`- Je suis là .`projected_dec`a une forme`(d_attn,)`et les émissions. `combined`a une forme`(T_enc, d_attn)`- Je suis là .`scores`a une forme`(T_enc,)`- Je suis là .`weights`a une forme`(T_enc,)`- Je suis là .`context`a une forme`(d_h,)`- Envoyez-le.

> Pour vérifier votre forme,`encoder_states`形状为 `(T_enc, d_h)`Il y a une autre.`projected_enc`形状为 `(T_enc, d_attn)`Il y a une autre.`projected_dec`形状为 `(d_attn,)`Il est en train de se révéler.`combined`形状为 `(T_enc, d_attn)`Il y a une autre.`scores`形状为 `(T_enc,)`Il y a une autre.`weights`形状为 `(T_enc,)`Il y a une autre.`context`形状为 `(d_h,)`Je suis bien là.

### Étape 2: Luong point et général

```python
def dot_attention(decoder_state, encoder_states):
    scores = encoder_states @ decoder_state
    weights = softmax(scores)
    return weights @ encoder_states, weights


def general_attention(decoder_state, encoder_states, W):
    projected = W.T @ decoder_state
    scores = encoder_states @ projected
    weights = softmax(scores)
    return weights @ encoder_states, weights
```

C'est pour ça que le papier de Luong est arrivé, avec la même précision sur la plupart des tâches, beaucoup moins de code.

> Chaque trois lignes. C'est le sens de Luong. Dans la plupart des tâches, le code est beaucoup moins précis.

### Étape 3: exemple numérique travaillé

Compte tenu de trois états de décodeur (en gros "cat", "sat", "mat") et d'un état de décodeur qui s'aligne le plus avec le premier, la distribution de l'attention se concentre sur la position 0. Si l'état de décodeur se déplace pour s'aligner avec le dernier, l'attention passe à la position 2.

> 给定三个编码器状态 ((大致是"cat"、"sat"、"mat") et un avec le premier le plus en phase avec le décodeur, attention est concentrée en position 0。

```python
H = np.array([
    [1.0, 0.0, 0.2],
    [0.5, 0.5, 0.1],
    [0.1, 0.9, 0.3],
])

s_close_to_cat = np.array([0.9, 0.1, 0.2])
ctx, w = dot_attention(s_close_to_cat, H)
print("weights:", w.round(3))
```

```
weights: [0.464 0.305 0.231]
```

La première ligne gagne, puis déplacer l'état du décodeur plus près de l'état du troisième encodeur et regarder le changement de poids.

> La première ligne est de se déplacer vers la troisième, observer le changement de puissance.

### Étape 4: pourquoi c'est le pont vers les transformateurs

Translatez la langue ci-dessus en Q/K/V:

> 将上的语言翻译为 Q/K/V:

- **Query**= état du décodeur `s_{t-1}`
  **查询（Query）**= 解码器 état `s_{t-1}`
- **Key**= états d'encodeur (ce que nous marquons contre)
  **键（Key）**= 编码器状态(我们用来打分的对象)
- **Value**= états d'encodeur (ce que nous pesons et somme)
  **值（Value）**= 编码器状态(我们用来加权和的对象)

Dans l'attention classique, les clés et les valeurs sont la même chose. L'attention personnelle les sépare: vous pouvez interroger une séquence contre elle-même, avec différentes projections apprises pour K et V. L'attention multi-tête le gère en parallèle avec différentes projections apprises. Les transformateurs empilent l'ensemble de la scène plusieurs fois et laissent tomber les RNN.

> Dans l'attention classique, la clé et la valeur sont la même chose. L'attention elle-même les séparera: vous pouvez utiliser différentes séquences de projection d'apprentissage pour rechercher une séquence elle-même en tant que K et V.

Les mathématiques sont les mêmes, les formes sont les mêmes, le saut pédagogique de l'attention Bahdanau à l'attention produit à l'échelle est principalement la notation.

> Le saut de l'enseignement de la concentration est principalement le symbole.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

PyTorch et TensorFlow envoient directement l'attention.

> PyTorch et TensorFlow fournissent directement une attention.

```python
import torch
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=128, num_heads=8, batch_first=True)
query = torch.randn(2, 5, 128)
key = torch.randn(2, 10, 128)
value = torch.randn(2, 10, 128)

output, weights = mha(query, key, value)
print(output.shape, weights.shape)
```

```
torch.Size([2, 5, 128]) torch.Size([2, 5, 10]
```

C'est une couche d'attention transformateur.`output`est la nouvelle requête augmentée par le contexte. `weights`est la matrice d'alignement 5x10 que vous pouvez visualiser.

> Ceci est un transformateur attention attention layer.`output`C'est une nouvelle mise en page.`weights`C'est une matrice de 5x10, vous pouvez la visualiser.

### Quand l'attention classique est encore importante

- La version à tête unique, à couche unique, basée sur le RNN rend chaque concept visible.
  Les concepts de RNN sont tous visibles.
- Les tâches de séquence sur l'appareil où les transformateurs ne s'adaptent pas.
  Transformer 放不下设备端序列任务。
- Tout article de 2014-2017, vous le lirez mal sans connaître la convention de Bahdanau.
  Toutes les publications de 2014-2017 ne comprennent pas Bahdanau.
- Analyse de l'alignement finement graineuse en MT. Les poids d'attention bruts sont un outil d'interprétation même sur les modèles transformateurs, et leur lecture exige de savoir ce qu'ils sont.
  La petite partie de la traduction en machine est une analyse.

### Le piège de l'attention-poids-comme-explication

Les poids de l'attention semblent interprétables. Ce sont des poids qui s'additionnent à un sur plusieurs positions; vous pouvez les tracer; haut signifie " regardé sur cela. " Les critiques les adorent.

> Attention le poids semble expliquable. Ils sont le poids de l'ensemble des positions et de l'ensemble de l'un; vous pouvez les dessiner; haute signifie "voir ceci" (voir ceci).

Ils ne sont pas aussi interprétables qu'ils semblent. Jain et Wallace (2019) ont montré que les distributions d'attention peuvent être permutées et remplacées par des alternatives arbitraires sans changer les prédictions de modèle pour certaines tâches.

> 它们 ne sont pas comme elles semblent être expliquées. Jane et Wallace (2019) ont montré que la distribution de l'attention peut être remplacée et remplacée par un remplacement arbitratif, sans modifier les prévisions de modèles de certaines tâches.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-attention-shapes.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-attention-shapes.md`- Le numéro de la liste:

```markdown
---
name: attention-shapes
description: Debug shape bugs in attention implementations.
phase: 5
lesson: 10
---

Given a broken attention implementation, you identify the shape mismatch. Output:

1. Which matrix has the wrong shape. Name the tensor.
2. What its shape should be, derived from (d_s, d_h, d_attn, T_enc, T_dec, batch_size).
3. One-line fix. Transpose, reshape, or project.
4. A test to catch regressions. Typically: assert `output.shape == (batch, T_dec, d_h)` and `weights.shape == (batch, T_dec, T_enc)` and `weights.sum(dim=-1) close to 1`.

Refuse to recommend fixes that silently broadcast. Broadcast-hiding bugs surface later as silent accuracy degradation, the worst kind of attention bug.

For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Mise en œuvre `softmax`masquer afin que les jetons de rembourrage dans l'encodeur obtiennent un poids d'attention zéro.
   **简单。** réaliser `softmax`掩码, faire le chargement du jeton dans le codeur attention le pouvoir de peser pour zéro.
2. **Medium.**Ajoutez une attention à la Luong `general`- La forme.`d_h`dans `n_heads`Vérifiez que le cas unique correspond à votre mise en œuvre antérieure.
   **中等。**Pour Luong`general`形式添加多头注意力──将 `d_h`Pour la partition`n_heads`组, chaque tête de travail attention,拼接,验证单头情况与你之前的实现匹配.
3. **Hard.**Prenez une formation GRU encodeur-décodeur avec Bahdanau attention sur la tâche de copie de jouet de la leçon 09. précision de la trace par rapport à la longueur de la séquence. Comparer avec la ligne de base de non-attention. Vous devriez voir l'écart s'élargir à mesure que la longueur augmente, confirmant attention soulève le goulet d'étranglement.
   **困难。**En cours de réplication de jouets de la 9e classe, entraînez-vous avec Bahdanau Attention GRU 编码器-解码器──绘制准确率 vs.序列长度──与无注意基线相比── vous devriez voir le décalage augmenter et se développer avec la longueur, confirmez que l'attention a été levée──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)Le journal.
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) les trois variantes de score et leur comparaison. / 三种分数变体及其比较──
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) la mise en garde contre l'interprétation. / 可解释性警示──
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) La marche en cours avec PyTorch. / 带 PyTorch 的可运行演练──
