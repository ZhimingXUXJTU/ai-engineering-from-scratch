# Codification de position  Sinusoïdale, RoPE, ALiBi
# La position est la même.

> L'attention est invariable en permution. "Le chat s'est assis sur le tapis" et "mat le chat sur le sat" produisent la même sortie sans signal de position. Trois algorithmes le fixent  chacun avec un pari différent sur ce que signifie "position".

> Attention est la répartition des variables. Le chat est assis sur le tapis et le chat est assis sur le tapis.

> **【中文解读】**Transformer 没有位置信息,需要手动注入──RoPE est un procédé utilisé par les transformateurs, ALiBi 支持外推到更长序列──

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

L'attention par produit de point est aveugle à l'ordre.`softmax(Q K^T / √d) V`est calculé à partir de similitudes par paires.`X`La position de l'attention ne compte pas pour l'intérieur.

> L'attention est sans ordre.`softmax(Q K^T / √d) V`Il y a une différence entre les deux.`X`La ligne, la ligne de sortie sont perturbées de la même manière.

Ce n'est pas un bug dans un modèle de sacs de mots. Pour le langage, le code, l'audio, la vidéo  tout ce qui a un sens dans l'ordre  c'est fatal.

> Dans le modèle de mot-bag, ce n'est pas un bug. Mais pour les choses qui ont un sens dans le langage, le code, l'audio, le vidéo, c'est mortel.

La solution est d'injecter la position dans les embeddings.

> La méthode de réparation est d'une certaine manière de placer l'emballage.

1. **Absolute sinusoidal**(Vaswani 2017). Ajouter `sin/cos`Il est simple, sans apprentissage, et il est peu extrapolé au-delà des longues longues.
   **绝对正弦编码**(Vaswani 2017) `sin/cos`Il est également possible de faire des tests de formation en plus de la durée de formation.

2. **RoPE — Rotary Position Embeddings**(Su 2021). Rotate les vecteurs Q et K par un angle proportionnel à la position. Encode la position *relative* directement dans le produit de point. Dominant en 2026.
   **RoPE — 旋转位置嵌入**(Su 2021) ・ selon l'angle de rotation Q 和 K 向量── directement dans le point de calcul

3. **ALiBi — Attention with Linear Biases**(Prés 2022). Sautez entièrement les emblèmes; ajoutez une pénalité linéaire par tête aux scores d'attention en fonction de la distance. Excellente extrapolation de longueur.
   **ALiBi — 带线性偏置的注意力**(Près 2022) ◊ complètement sur-écrou; ajouter la punition de chaque tête en fonction de la distance vers l'attention ⋅

En 2026, pratiquement tous les modèles frontaliers ouverts utilisent le RoPE: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi.

> Jusqu'en 2026, essentiellement chaque modèle de première ligne est utilisé par les modèles de RoPE: Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。

> **【中文解读】**Le système de codage des positions est un système de codage des positions de l'attention qui est en train de se dérouler.

## Le concept de base.

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### - C'est une forme sinusoïdale absolue.

Précompte une matrice fixe `PE`de forme `(max_len, d_model)`- Le numéro de la liste:

> 预计算一个固定矩阵 `PE`, forme pour`(max_len, d_model)`- Le numéro de la liste:

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

Alors ...`X' = X + PE[:N]`Chaque dimension est un sinus à une fréquence différente.`max_len`: rien n'a dit au modèle ce qui se passe à la position 2048 quand il ne voyait que les positions 02047.

> Alors, attention !`X' = X + PE[:N]`◊ chaque dimension est une série de fréquences différentes.`max_len`out of effect: le modèle n'a vu que la position 0-2047, rien ne lui dit ce qui va se passer à la position 2048

### RoPE tourne en position

Rotation des vecteurs Q et K (pas intégrés). Pour une paire de dimensions `(2i, 2i+1)`- Le numéro de la liste:

> 旋转 Q 和 K 向量( pas emplacé) ⋅对一对维度 `(2i, 2i+1)`- Le numéro de la liste:

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Appliquer la même rotation aux touches avec position `pos_k`Le produit de la dot`q'_m · k'_n`devient une fonction de `(m - n)`Je suis seul.**the attention score depends only on the relative distance**Même si la rotation était bloquée.

> Pour la position de l'application`pos_k`Le même tour.`q'_m · k'_n` devenir seulement `(m - n)`La fonction est:**注意力分数只取决于相对距离**Même si le tour est basé sur une position absolue...

> **【中文解读】**Les points de Q·K dépendent uniquement de la distance relative (m-n) ⋅ ce qui signifie que le modèle naturologique a une relation de position relative ⋅ ajustement de base ⋅ les paramètres peuvent également être réalisés à long terme.

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**Llama 3 通过 YaRN((Encore une autre méthode de RoPE extensionN) va passer de 8K 扩展到128K. Le processus central consiste à régler la fréquence de base du RoPE, de sorte que la haute fréquence de la taille reste à la résolution initiale, et la faible fréquence reste à la valeur de l'entrée. Cette stratégie de " traitement de la taille " maintient à la fois la perception de la position précise à courte distance, et développe la capacité de diffusion à longue distance.

Extension de l' ROPE: `base`Llama 3 est étendu de 8K à 128K de cette façon.

> 扩展 RoPE:`base`Il est possible de réduire le nombre de tests de la Llama 3 à 8K, de la Llama 3 à 128K.

### Attention à la déviation linéaire.

Laissez tomber le truc de l'intégration.

> 跳过嵌入技巧──直接偏置注意力分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

Où ?`m_h`est une pente spécifique à la tête (par exemple `1 / 2^(8·h/H)`Les jetons plus proches sont renforcés; les jetons plus éloignés sont pénalisés. Aucun coût de temps d'entraînement.

> Parmi eux `m_h`est spécifique à la cote de l'inclinaison de la tête`1 / 2^(8·h/H)`Les épreuves montrent une longueur supérieure à la longueur de la corde d'un étalon, correspondant à la longueur de son étalon d'entraînement original.

### Que choisir en 2026

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

Le RoPE a gagné parce qu'il attire l'attention sans changer l'architecture, encode la position relative et ses`base`l'hyperparamètre donne un bouton propre pour l'ajustement fin de long contexte.

> RoPE 胜出 est parce qu'il n'a pas besoin de changer l'architecture, il peut insérer l'attention, le code par rapport à la position, et il`base`Les superparamètres à long terme donnent une régulation claire du tour.

> **【中文解读】**Le choix du code de position 2026 est très clair: le nouveau projet est par défaut RoPE. Il ne change pas d'architecture, le code par rapport à la position, et en passant par la base, les paramètres fournissent une voie claire de longueur de la ligne de basse.

> **【拓展：位置编码对长上下文 RAG 的影响】**Dans le système RAG, le code de position affecte directement la capacité de traitement de fichiers longs. RoPE + YaRN permet à Llama 3 de traiter les fichiers de 128K, ce qui signifie qu'il peut traiter à la fois environ 300 pages de fichiers.
```figure
rope-explorer
```

## Faites-le

## Construisez-le et mettez-le en œuvre.

### Étape 1: Codage sinusoïdale

Regardez !`code/main.py`Un calcul à quatre lignes:

> 参见 `code/main.py`∼4 行计算:

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i]     = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

Ajoutez cela à la matrice d'intégration avant la première couche d'attention.

> Avant le premier niveau d'attention, il sera ajouté à la matrice de l'implémentation.

### Étape 2: RoPE appliqué à Q, K. Étape 2: RoPE appliqué à Q 、K

Le RoPE fonctionne sur place sur Q et K. Pour chaque paire de décolores:

> ROPE pour Q et K opérations de terre de base:

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i]     = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

Crucial: appliquer la même fonction à Q à la position `m`et K à la position `n`Leur produit dot prend un`cos((m-n)·θ_i)`L'attention apprend gratuitement la position relative.

> 关键: à la position `m`de Q et position `n`Les K  appliquent la même fonction ⋅ leurs points de cumulation dans chaque séquence pour obtenir un `cos((m-n)·θ_i)`Parce que l'attention est libre de l'apprendre à la position relative.

> **【中文解读】**Le cœur de réalisation du RoPE: pour chaque dimension de Q et K (2i, 2i+1) faire la position relative à la rotation, le tournage, l'angle de rotation et la position en proportion, de sorte que le point de Q_m · K_n apparaît dans le cos(((m-n) *theta) 项, naturellement codifié par rapport à la distance.

### Étape 3: Albi inclinations et biais

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias  # add to attention scores before softmax
```

Ajouter `bias[h]`à la `(seq_len, seq_len)`Matrice de score d' attention de la tête `h`, puis softmax.

> Il va`bias[h]`À la tête`h``(seq_len, seq_len)`Attention à la quantité de réaction, puis à la douceur maximale.

### Étape 4: Vérifiez la propriété relative de distance de RoPE.

Choisissez deux vecteurs aléatoires `a, b`- Retourne par`(pos_a, pos_b)`- Alors , par`(pos_a + k, pos_b + k)`- Les deux produits de point doivent correspondre à l'erreur de point flottant. Cette propriété est l'ensemble du point de RoPE  il est invariant à l'opposition absolue, seule l'écart relatif compte.

> 选择两个随机向量 `a, b`Il est utilisé.`(pos_a, pos_b)`Puis utilisez-le.`(pos_a + k, pos_b + k)`旋转── deux points de la différence de point de décalage doivent correspondre. Cette propriété est la signification complète du RoPE.

> **【拓展：位置编码的历史演进】**De Vaswani (en 2017) à GPT-2/3 (en 2021) et ALiBi (en 2022) le mode de codage de position a connu un changement de mode de "position absolue" à "position relative". Le succès du RoPE réside dans le fait qu'il ne change pas l'architecture de l'attention, directement dans le Q/K 旋转, mais offre une voie claire d'expansion de la structure.

## Utilisez-le avec le cadre de réalisation

PyTorch 2.5+ expédie des équipements RoPE en `torch.nn.functional`La plupart des codes de production utilisent`flash_attn`ou `xformers`où le RoPE est appliqué à l'intérieur du noyau d'attention.

> PyTorch 2.5+`torch.nn.functional`中内置了 RoPE 工具── la plupart des codes de production utilisés `flash_attn`Ou `xformers`, dont le RoPE dans l'application interne de l'attention intérieure.

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**Réscale `base`à `base * (scale_factor)^(d/(d-2))`lorsque vous passez de 4K à 16K+.
  **NTK-aware 插值。**Quand il est passé de 4K à 16K+, il sera`base`Réinitialisation`base * (scale_factor)^(d/(d-2))`Il y a une autre.
- **YaRN.**Une interpolation plus intelligente qui préserve l'entropie de l'attention dans de longs contextes.
  **YaRN。**Plus intelligent, conserver l'attention sur le long et le bas.
- **LongRoPE.**La méthode 2024 de Microsoft qui utilise la recherche évolutionniste pour choisir des facteurs d'échelle par dimension.
  **LongRoPE。**Microsoft 2024 méthode, utilisant l'évolution de la recherche sélectionner chaque dimension réduite facteur.
- **Position interpolation + fine-tuning.**Réduisez vos positions par le facteur d'extension et réglez les jetons de 15B.
  **位置插值 + 微调。**Il suffit de se développer en fonction de la taille des positions et de la taille des symboles 1 à 5B.

## Envoyez-le . Produit .

Regardez !`outputs/skill-positional-encoding-picker.md`. La compétence choisit une stratégie de codage pour un nouveau modèle compte tenu de la longueur du contexte cible, des besoins d'extrapolation et du budget de formation.

> 参见 `outputs/skill-positional-encoding-picker.md` Cette compétence est utilisée pour choisir des stratégies de code de nouveaux modèles, en fixant des objectifs sur la longueur de la page suivante, les besoins et le budget de formation.

## Les exercices

1. **Easy / 简单。**Tracer le sinus.`PE`matrice comme carte thermique pour `max_len=512, d=128`Confirmer le modèle "les bandes s'élargissent à mesure que l'indice de dimension augmente".
   Je vais être en train de jouer.`PE`矩阵绘制为 `max_len=512, d=128`Le modèle de "grandissement de l'index à mesure que la taille change de largeur"

2. **Medium / 中等。**Mettre en œuvre une mise à l'échelle de RoPE à la connaissance du NTK. Exercer un petit LM sur des séquences de longueur 256, puis tester sur longueur 1024 avec et sans mise à l'échelle. Mesurer la perplexité.
   实现 NTK-conscient RoPE 缩放── entraîner un micro LM sur une séquence de longueur 256 et ensuite tester la longueur 1024── en cas d'encombrement et de non-encombrement──

3. **Hard / 困难。**Mettre en œuvre ALiBi et RoPE dans le même module d'attention. entraîner un transformateur à 4 couches sur une tâche de copie avec des séquences de longueur 512. Extrapoler à 2048 au moment de l'essai. Comparer la dégradation.
   Dans le même module d'attention, réaliser ALiBi et RoPE.

## Les termes clés

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Positional encoding / 位置编码 | "Tells attention about order" / "告诉注意力顺序" | Any signal added to embeddings or attention that encodes position. 添加到嵌入或注意力中编码位置的任何信号。 |
| Sinusoidal / 正弦编码 | "The original one" / "原始的那种" | `sin/cos` at geometric frequencies added to embeddings; doesn't extrapolate. 以几何频率加到嵌入上的 `sin/cos`；不能外推。 |
| RoPE | "Rotary embeddings" / "旋转嵌入" | Rotate Q, K by position-dependent angle; dot product encodes relative distance. 按位置相关角度旋转 Q、K；点积编码相对距离。 |
| ALiBi | "Linear bias trick" / "线性偏置技巧" | Add `-m·|i-j|` to attention scores; no embedding needed, great extrapolation. 向注意力分数添加 `-m·|i-j|`；无需嵌入，出色的外推。 |
| base | "RoPE's knob" / "RoPE 的旋钮" | The frequency scaler in RoPE; increase to extend context at inference. RoPE 中的频率缩放器；增大以在推理时扩展上下文。 |
| NTK-aware | "A RoPE scaling trick" / "RoPE 缩放技巧" | Rescale `base` so high-frequency dims aren't squeezed when context expands. 重新缩放 `base` 使高频维度在上下文扩展时不被挤压。 |
| YaRN | "The fancy one" / "高级的那种" | Per-dimension interpolation+extrapolation that preserves attention entropy. 保留注意力熵的每维度插值+外推。 |
| Extrapolation / 外推 | "Works beyond trained length" / "超过训练长度还能用" | Can the position scheme serve correct output past `max_len` seen in training? 位置方案能否在训练中见过的 `max_len` 之后提供正确的输出？ |

## Encore une lecture

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762) sinusoïdale originale.
  Vaswani et d'autres personnes

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) papier RoPE.
  Le projet de loi de la Commission sur les droits de l'homme (CEPC) est un projet de loi de la Commission sur les droits de l'homme.

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409)- Il est bien.
  La presse, Smith, Lewis, le 2021

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) l'état de l'art de l'échelle RoPE.
  Peng et d'autres personnes (ppg 2023)

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595) Llama 2 du Meta, un document dans un long contexte.
  Chen 等人(2023)  Meta's Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) la méthode Microsoft utilisée par Phi-3-Long.
  Ding 等人(2024)  Microsoft's method, été utilisé Phi-3-Long

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) Implémentations de chaque système de mise à l'échelle RoPE au niveau de la production.
  Les transformateurs de face embrasés  possèdent des systèmes de production de RoPE 缩放方案
