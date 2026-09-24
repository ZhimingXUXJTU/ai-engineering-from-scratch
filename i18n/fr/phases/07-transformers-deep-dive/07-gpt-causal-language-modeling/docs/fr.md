# GPT  Modélisation du langage de cause  GPT  因果语言模型

> Le masque triangulaire est la ligne de code la plus importante de l'IA moderne.

> **【中文解读】**GPT est un transformateur décodeur uniquement, avec un effet massif ({{sfn}}) pour empêcher de voir le futur.

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Un modèle de langage répond à une question: étant donné la première `t-1`Les jetons, quelle est la répartition de probabilité sur les jetons `t`Trainer sur ce signal  prédiction de jeton suivant  et vous obtenez un modèle qui peut générer du texte arbitraire un jeton à la fois.

> 语言模型回答一个问题:给定前 `t-1`- Je suis un symbole.`t`Dans ce signal dans le suivant 预测 sur l'entraînement, vous pouvez obtenir un modèle de texte qui peut être généré par le token

Pour l'entraîner de bout en bout sur une séquence entière en parallèle, vous devez que la prédiction de chaque position ne dépend que des positions précédentes.

> Pour s'entraîner sur toute la séquence, vous avez besoin de prévoir chaque position en fonction de la position précédente.

Le masque causale fait ceci.`-inf`Les valeurs ajoutées aux points d'attention avant softmax. Après softmax, ces positions deviennent 0. Chaque position peut se concentrer uniquement sur elle-même et les positions précédentes. Et parce que vous l'appliquez une fois à toute la séquence, vous obtenez N parallèles de prochaine jetons prédictions dans un passage en avant.

> Il est un top-triangle.`-inf`值), plus softmax 之前的注意分数上──softmax 后, ces positions changent à 0──每位置只能关注自身及之前的位置──因为对整个序列只适用一次,所以一次前向传播就能得到N个并行的下一个代币 预测──

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  ils sont tous des transformateurs causaux décodeurs uniquement avec la même boucle de base.
GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2025), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  ce sont tous des transformateurs causaux décodeurs uniquement avec la même boucle de base. Ce qui les sépare, ce sont la qualité des données, l'échelle et les raffinements architecturaux, et la post-formation (SFT, RLHF, DPO, et leurs successeurs).

> GPT-1(2018)、GPT-2(2019)、GPT-3(2020)、GPT-4(2023)、GPT-5(2024)、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi

> **【中文解读】**Le masque de conséquences est la ligne de code la plus importante de l'IA moderne. Une première ligne de code est la "matrice de trois côtés" (inf 值), ajoutée au nombre de points d'attention, et le softmax est remplacé par un point de position de 0 pour chaque position.

## Le concept de base.

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### Le masque

Compte tenu d' une séquence de longueur `N`, construire une`N × N`matrice:

> 给定长度为 `N`De la séquence, construire une.`N × N`La réaction:

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Ajouter `M`à la note d'attention avant softmax. `exp(-inf) = 0`Chaque rangée de la matrice d'attention est une répartition de probabilité sur les positions précédentes seulement.

> Il va`M`Ajout à la concentration initiale de l'attention avant le softmax.`exp(-inf) = 0`, donc le poids de la position masquée est de zéro. Chaque ligne de la matrice d'attention est simplement une répartition de probabilité sur la position précédente.

Coût de mise en œuvre: 1 `torch.tril()`Le temps de calcul: nanosecondes, impact sur le terrain, tout.

> 实现成本: 一行 `torch.tril()`调用──计算时间:纳秒级── sur l'ensemble du domaine:
### D'où vient le triangle

Le masque est généralement présenté comme un patch boulonné sur l'attention.

**Stage 1 — prefix average.**Le résumé de la suite de causes la plus stupide: position`i`devient la moyenne des positions `0…i`En tant que boucle, c'est`out[i] = X[:i+1].mean(0)`Le même calcul est une matrice multipliée. Prenez une matrice triangulaire inférieure de un, divisez chaque rangée par son nombre, multipliez:

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

Régime `i`de `A`est `[1/(i+1), …, 1/(i+1), 0, …, 0]`Les zéros au-dessus de la diagonale sont la causalité. Rien sur le futur n'a été masqué; le futur n'a jamais été dans la somme.

**Stage 2 — learned weights.**Une moyenne uniforme traite chaque jeton passé comme étant également pertinent.`S`. Maintenant, les lignes ne sont plus de la somme à un par construction, donc normaliser chaque ligne avec softmax au lieu de la division par le comptage. Softmax ne produit jamais un zéro exact, ce qui rompt la causalité  à moins que les scores futurs entrent comme `-inf`, parce que `exp(-inf) = 0`- Le numéro de la liste:

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

Le même triangle, la même matrice de rangée stochastique, le même matmul.`-inf`Le masque n'est pas une nouvelle machine, c'est une entrée zéro de l'étape 1, traduite dans le domaine d'entrée de softmax.

**Stage 3 — content-dependent weights.**Dans la phase 2, `S`La position 7 pèse toujours la position 3 de la même façon, peu importe ce que disent les jetons.`S = Q @ K.T / sqrt(d_k)`Le masque, le softmax, le matmul sont identiques.

Trois étapes, une invariante: une matrice de rangée-stochastique triangulaire inférieure multipliée par la séquence. moyenne uniforme, poids statiques apprises, poids dépendant du contenu. Le masque n'a jamais été ajouté à l'attention.

```figure
mask-derivation
```

### Formation parallèle, inférence en série

Formation: faire avancer l'ensemble `(N, d_model)`une fois la séquence, calculer N pertes d'entropie croisée (une par position), somme, backprop. Parallèlement le long de la séquence. C'est pourquoi les échelles de formation GPT  vous traitez 1M jetons dans un lot dans un seul GPU passer.

> 训练: à l'ensemble `(N, d_model)`序列做一次前向传播,计算 N 个交叉损失(每个位置一个),求和,反向传播──沿序列并行──这就是GPT 训练可扩展的原因一次GPU通行就能处理批量中的1M 个代币──

Inference: vous générez des jetons par jetons.`[t1, t2, t3]`Je suis là .`t4`- La nourriture .`[t1, t2, t3, t4]`Je suis là .`t5`- La nourriture .`[t1, t2, t3, t4, t5]`Je suis là .`t6`Le cache KV (leçon 12) sauve les états cachés de `t1…tn`Donc, vous ne les recomptez pas à chaque étape. Mais la profondeur sérielle à l'inférence = longueur de sortie. C'est la taxe autorégressive et pourquoi le décoding est le goulot d'étranglement de latence de chaque LLM.

> 推理: par symbole 生成──输入 `[t1, t2, t3]`Je suis là .`t4` Entrée`[t1, t2, t3, t4]`Je suis là .`t5` Entrée`[t1, t2, t3, t4, t5]`Je suis là .`t6` KV 缓存 (第 12 课) enregistré `t1…tn`Le coût de la reprise est également le résultat de chaque retard de la formation.

### La perte  changement par changement

Les jetons donnés `[t1, t2, t3, t4]`- Le numéro de la liste:

> - Je vous ai donné un signe .`[t1, t2, t3, t4]`- Le numéro de la liste:

- Enregistrement: `[t1, t2, t3]`
  En anglais, le mot "port" est traduit par "port":`[t1, t2, t3]`
- Objectifs: `[t2, t3, t4]`
  Le mot grec traduit par " objectif " signifie " objectif ".`[t2, t3, t4]`

Pour chaque poste .`i`, calcul`-log P(target_i | inputs[:i+1])`C'est la croisée de l'entropie de toute la séquence.

> Pour chaque position`i`, calcul `-log P(target_i | inputs[:i+1])`C'est le croisement de toute la série.

Tous les transformateurs LM que vous avez entendus trainer sur cette perte.

> Chaque modèle de transformateur que vous avez entendu parler est en train de perdre ses capacités.

> **【拓展：Teacher Forcing 与暴露偏差】**GPT entraînement à l'aide de l'enseignant forçant chaque pas à entrer en réalité un premier jeton et non le modèle lui-même prédiction.

### Stratégies de décoding

Après l'entraînement, les choix d'échantillonnage comptent plus que les gens ne le pensent.

> Après la formation, le choix des stratégies d'échantillonnage est plus important que ce que les gens imaginent.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

En 2026, min-p + température 0,7 est une valeur par défaut raisonnable pour les modèles à poids ouvert.

> En 2026, la température min-p + 0,7 est la configuration rationnelle et standardisée du modèle open source.

> **【中文解读】**Le choix de la stratégie de décomposition affecte directement la production de qualité.

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**GPT-2(1.5B 参数)→ GPT-3(175B)→ GPT-4(en moyenne 1,8T MoE) dans le saut de la taille, les changements d'architecture sont très petits, mais les améliorations des méthodes de données et de formation sont énormes.

### Qu'est- ce qui a permis au " recette de la GPT " de fonctionner

1. **Decoder-only.**Pas de coefficient d'encodage, une attention par couche.
   Le mot grec traduit par " le mot grec "**解码器专用。**没有编码器开销──每层一次注意力 + FFN 通行──
2. **Scaling.**124M → 1.5B → 175B → trillions. Les lois de l'échelle de Chinchilla (leçon 13) vous disent comment dépenser l'informatique.
   Le mot grec traduit par " le mot grec "**规模扩展。**De 124M à 1,5B à 175B à nouveau à des millions de paramètres.
3. **In-context learning.**Il est apparu vers 6B13B. Le modèle peut suivre quelques exemples sans ajustement.
   Le mot grec traduit par " le mot grec "**上下文学习。**约在6B-13B 参数时涌现――模型无需微调就能遵循少样本示例――
4. **RLHF.**Une formation post-traînement sur les préférences humaines a transformé le texte brut prétrainé en assistants de chat.
   Le mot grec traduit par " le mot grec "**RLHF。**Le texte original de l'entraînement préalable sera traduit en aide au dialogue.
5. **Pre-norm + RoPE + SwiGLU.**Une formation stable à l'échelle.
   Le mot grec traduit par " le mot grec "**Pre-norm + RoPE + SwiGLU。**Une formation de stabilité à grande échelle.

L'architecture de base n'a pas beaucoup changé depuis GPT-2. Tout ce qui est intéressant s'est passé dans les données, l'échelle et la formation post-training.

> Depuis le GPT-2, la structure centrale n'a pas beaucoup changé. Tout ce qui est intéressant se passe dans les aspects de la taille et de la formation ultérieures.

> **【中文解读】**Elements de succès de GPT: Simplicité et étendue de l'architecture en décodeur seulement (de 124M à millions de paramètres)  capacité d'apprentissage littéraire (environ 6B)  RLHF 后训 (en anglais seulement) 将预训文转化为对话助手) 以及现代块设计 (en anglais seulement)  预规 + RoPE + SwiGLU) 

> **【拓展：自回归生成的推理瓶颈】**Le problème principal du GPT est que la formation et la mise en œuvre de la méthode de calcul doivent être effectuées par chaque élément de la série.

## Construisez-le et mettez-le en œuvre.
```figure
causal-mask
```

## Faites-le

### Étape 1: le masque de causalité

Regardez !`code/main.py`Une ligne unique:

> 参见 `code/main.py`Il y a une autre chose.

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Ajoutez-le aux notes d'attention avant le softmax.

> Pour le rendre plus doux, il faut le faire avec le temps.

### Étape 2: un modèle GPT à deux couches

Améliorez deux blocs de décodeur (auto-attention masquée + FFN, aucune attention croisée). Ajoutez un embed token, un codage positional et un un déembedding (attaché à la matrice d'embedding token  un truc standard depuis GPT-2).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・ Ajouter des jetons 嵌入、位置编码和反嵌入(与 jetons 嵌入矩阵绑定GPT-2 以来标准技巧) ・・・

### Étape 3: Prédiction du prochain jeton, de bout en bout

Sur un vocabulaire de jouets à 20 jetons, produisez des logites à chaque position. Comptez la perte d'entropie croisée contre la cible de décalage par un. Pas de gradient  c'est un contrôle de santé mentale avant-pass.

> Sur le tableau de 20 symboles de jouets, chaque position génère des logits.

### Étape 4: prélèvement d'échantillons

Implémenter l'avidité, la température, le top-k, le top-p, le min-p. Exécuter chacun sur une demande fixe et comparer les sorties.

> 实现贪心、温度、top-k、top-p、min-p 采样──在固定提示上分别运行并比较输出──一个采样函数只需要10 行代码──

## Utilisez-le avec le cadre de réalisation

PyTorch, 2026 - Je suis un homme.

> PyTorch, 2026:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

Sous le capot,`generate()`Il effectue le passage vers l'avant, tire les logits de position finale, échantillonne le jeton suivant, l'apporte et le répète.

> Dans le fond,`generate()`运行前向传播,取出最后位置的logits,采样下一个代币,追加到序列中,重复──每个生产 LLM 推理(vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX) sont utilisés avec une grande optimisation pour réaliser le même cycle批量预填、连续批处理、KV 缓存分页、推测解码──

**GPT vs BERT, one line each:**Les prédictions du GPT `P(x_t | x_{<t})`- BERT prédit .`P(x_masked | x_unmasked)`La perte détermine si le modèle peut générer.

> **GPT 与 BERT 各一句话：**GPT 预测 `P(x_t | x_{<t})`│BERT 预测 │`P(x_masked | x_unmasked)` La fonction de perte détermine si le modèle peut être généré

## Envoyez-le . Produit .

Regardez !`outputs/skill-sampling-tuner.md`. La compétence choisit les paramètres d'échantillonnage pour une tâche de nouvelle génération et désigne les décodage déterministique requis.

> 参见 `outputs/skill-sampling-tuner.md` Cette compétence est nécessaire pour la sélection de paramètres de nouvelles tâches de génération, et marque le moment où la détermination est nécessaire.

## Les exercices

1. **Easy.**On court .`code/main.py`et vérifier que la matrice d'attention causale est triangulaire inférieure après softmax.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`, l'essai de la réaction de la réaction de l'attention dans le softmax 后是下三角的──抽查:
2. **Medium.**Comparez la perplexité de la poutre 4 contre la cupidité sur 10 courtes instructions. La poutre gagne-t-elle toujours ? (conseil: généralement pour la traduction, pas pour le chat ouvert).
   En français, la traduction est plus facile à trouver. En français, la traduction est plus facile à trouver.
3. **Hard.**Implémenter le décoding spéculatif: utiliser un modèle minuscule de 2 couches comme projet et un modèle de 6 couches comme vérificateur. Mesurer l'accélération de l'horloge murale sur 100 compléments de longueur 64.
   Le modèle de 6 niveaux est utilisé comme un modèle de projet. Il est utilisé pour la mesure de l'accélération réelle de 64 en 100 longitudes.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Encore une lecture

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) GPT-1.
  Le texte de la première partie est le texte de la première partie.
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) GPT-2.
  Le texte de la première partie est le texte de la première partie.
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) GPT-3 et apprentissage dans le contexte.
  Le texte est en français.
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) papier de décoding spécifique.
  Le thème de la rédaction de la Bible est:
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) code de référence canonique de la cause à la cause.
  Le mot "HuggingFace" est traduit par "HuggingFace Llama" en français.
