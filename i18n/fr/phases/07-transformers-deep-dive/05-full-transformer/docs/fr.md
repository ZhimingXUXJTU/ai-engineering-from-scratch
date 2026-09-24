# Le transformateur complet  Encoder + Décoder
# 完整 Transformer  编码器 + 解码器

> L'attention est l'étoile. Tout le reste, résidus, normalisation, flux, attention croisée, est l'échafaudage qui vous permet de l'empiler profondément.

> Attention est le principal. Tout le reste reste de la connexion, de l'intégration, du réseau, de la traversée.

> **【中文解读】**Pour que l'attention soit mise en œuvre, il faut se concentrer sur la façon dont l'attention est mise en œuvre.

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Une seule couche d'attention est un extracteur de caractéristiques, pas un modèle. Un matmul par couche n'est pas suffisant pour la capacité de langue. Vous avez besoin de profondeur  et de profondeurs de ruptures sans la bonne plomberie.

>  Un seul niveau d'attention est un extracteur de caractéristiques, pas un modèle.

Le papier Vaswani 2017 a compilé six décisions de conception qui ont transformé une couche d'attention en un bloc empilable. Chaque transformateur depuis  encodeur-seul (BERT), décodeur-seul (GPT), encodeur-decodeur (T5)  hérite du même squelette.

> En 2017, Vaswani a publié un article portant sur six décisions de conception, qui vont transformer une couche d'attention en blocs comptables.

Cette leçon est le squelette. Les leçons suivantes le spécialisent  06 pour les encoders, 07 pour les décoders, 08 pour l'encodeur-décodeur.

> Ce cours est un schéma. Ce cours est consacré à la programmation.

> **【中文解读】**Le seul niveau d'attention est un extracteur de caractéristiques, pas un modèle complet. L'article de 2017 compose six blocs de conception décisionnelles: intégration + code de position, auto-attention, FFN, connexion de décalage, recouvrement de niveau, concentration de passage.

## Le concept de base.

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### Les six pièces.

1. **Embedding + positional signal.**Tokens → vecteurs. Position injectée par RoPE (moderne) ou sinusoïdale (classique).
   **嵌入 + 位置信号。**Le signe → 向量──通过 RoPE(现代)

2. **Self-attention.**Chaque position est à l'aise avec l'autre.
   **自注意力。**Chaque position est suivie par toutes les autres positions.

3. **Feed-forward network (FFN).**PAM à deux couches en fonction de la position: `W_2 · activation(W_1 · x)`- Le ratio d'expansion est 4x par défaut.
   **前馈网络 (FFN)。**位置级两层 MLP:`W_2 · activation(W_1 · x)`◊默认扩展比 4×♦

4. **Residual connection.** `x + sublayer(x)`Sans cela, les gradients disparaissent après environ 6 couches.
   **残差连接。** `x + sublayer(x)`Il n'y a pas de niveau, le niveau disparaît après environ 6 niveaux.

5. **Layer normalization.** `LayerNorm`ou `RMSNorm`(moderne) stabilise le flux résiduel.
   **层归一化。** `LayerNorm`Ou `RMSNorm`(现代) ∼稳定残差流──

6. **Cross-attention (decoder only).**Les requêtes proviennent du décodeur, des clés et des valeurs de la sortie du codeur.
   **交叉注意力（仅解码器）。**查询来自解码器,键和值来自编码器输出.

### Bloc de cryptage (utilisé par BERT, T5 encodeur)
Observez le flux d'un vecteur à travers un bloc: l'attention se mélange entre les positions, le résidu le transporte vers l'avant, le FFN le transforme et la norme maintient le flux stable.

```figure
transformer-block
```

### Bloc d'encodeur (utilisé par BERT, encodeur T5)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

Le codeur est bidirectionnel, pas de masquage, toutes les positions voient toutes les positions.

> Le codeur est à deux voies. Il n'y a pas de couverture.

### Bloc de décodeur (utilisé par GPT, T5 décodeur)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

Le décodeur a trois sous-couches par bloc. Le centre  attention croisée  est le seul endroit où les informations circulent du décodeur au décodeur. Dans une architecture pure de décodeur uniquement (GPT), l'attention croisée est omise et vous avez simplement masqué l'attention personnelle + FFN.

> Le seul endroit où l'information passe du codeur au codeur est le centre. Dans la pure architecture du codeur, l'attention du codeur est omise.

### Pré-norme contre post-norme . Pré-régulier contre ré-régulier .

Papel original: `x + sublayer(LN(x))`contre`LN(x + sublayer(x))`. Après la normalisation, il est plus difficile de s'entraîner profondément sans un réchauffement minutieux.`LN`* avant * sous-couche) est la version par défaut 2026: Llama, Qwen, GPT-3+, Mistral l'utilisent tous.

> Le thème de la rédaction`x + sublayer(LN(x))`contre`LN(x + sublayer(x))`◊ Après la reprise en 2019 ou encore  pas de pré-réalisation ◊ très difficile à entraîner ◊ avant la reprise ◊`LN`Dans le même temps, il est également possible de trouver des solutions de gestion de la situation.

### Le bloc modernisé de 2026

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm réduit la moyenne de centre de LayerNorm (une soustraction inférieure), ce qui permet de réduire les calculs et est empiriquement au moins aussi stable.`Swish(W1 x) ⊙ W3 x`) dépasse systématiquement le RELU/GELU FFN de ~0,5 points par rapport aux documents Llama, PaLM et Qwen.

> RMSNorm a éliminé la centralisation moyenne de LayerNorm (moins de 1 fois de réduction), économisé la quantité de calcul, et l'expérience a été au moins stable.`Swish(W1 x) ⊙ W3 x`Il est également possible de trouver des informations sur les différents types de données.

> **【中文解读】**Le bloc de transformateur moderne de 2026 avec l'édition originale de 2017: LayerNorm→RMSNorm, ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA。 Chaque amélioration est progressive, mais la mise en œuvre a considérablement amélioré la stabilité et la qualité du modèle de formation。

> **【拓展：为什么 Decoder-only 成为主流】**Bien que l'architecture de codeur-décodeur ait des avantages naturels sur des tâches telles que la traduction, le modèle de décodeur uniquement (GPT、Llama) est plus efficace sur l'expansion et la généralisation. Il peut utiliser la même structure pour traiter la compréhension et la génération de tâches, entraîner l'objectif de l'unité (en anglais seulement) et l'expansion a été testée par Chinchilla 定律证── c'est la raison pour laquelle presque tous les modèles de 2024-2026 ont été choisis en avant.

### Le nombre de paramètres.

Pour un bloc avec `d_model = d`et l'expansion du FFN `r`- Le numéro de la liste:

> Pour une`d_model = d`且 FFN 扩展比为 `r`Les blocs:

- MHA: `4 · d²`(Projections Q, K, V, O)
  Le MHA:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`- Je suis là.`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`- Je suis là.`3rd²`
- Normes: négligeables
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**Les paramètres du transformateur se concentrent principalement sur l'attention à la projection ((4d^2) et FFN(environ 8d^2 pour SwiGLU) (中。Llama 3 8B Chaque couche environ 1,5B 参数,32 couches communes environ 7B + emplacement et sortie tête。 Comprendre la distribution des paramètres aide à optimiser:MoE 替换FFN 可以增加总参数而不增加活跃计算;量化(如GPTQ、AWQ)

## Construisez-le et mettez-le en œuvre.

### Étape 1: Les blocs de construction étape 1: Construire un module

En utilisant le minuscule`Matrix`classe de la leçon 03 (copié dans ce dossier pour l'indépendance):

> Utilisation de la classe`Matrix`类(a été rédigé à ce dossier pour rester indépendant):

- `layer_norm(x, eps=1e-5)` Soustraire la moyenne, diviser par std.
  `layer_norm(x, eps=1e-5)`  减去平均值,除以标准差──
- `rms_norm(x, eps=1e-6)` Divise par RMS. Aucune soustraction moyenne.
  `rms_norm(x, eps=1e-6)` À l'exception du RMS.
- `gelu(x)`et `silu(x) * W3 x`Je suis désolé.
  `gelu(x)`et `silu(x) * W3 x`Je suis désolé.
- `ffn_swiglu(x, W1, W2, W3)`- Je suis désolé .
- `encoder_block(x, params)`et `decoder_block(x, enc_out, params)`- Je suis désolé .

### Étape 2: brancher un encodeur à 2 couches et un décodeur à 2 couches.

Passez l'enregistrement du codeur à chaque décodeur, ajoutez un LN final avant la projection de sortie.

> 堆叠它们──将编码器输出传入每个解码器交叉注意力──在输出投影前添加最终 LN──

```python
def encode(tokens, params):
    x = embed(tokens, params.emb) + sinusoidal(len(tokens), params.d)
    for block in params.encoder_blocks:
        x = encoder_block(x, block)
    return x

def decode(target_tokens, encoder_out, params):
    x = embed(target_tokens, params.emb) + sinusoidal(len(target_tokens), params.d)
    for block in params.decoder_blocks:
        x = decoder_block(x, encoder_out, block)
    return x
```

### Étape 3: Avance sur un exemple de jouet.

Passez une source de 6 jetons et une cible de 5 jetons.`(5, vocab)`Cette leçon est sur l'architecture, pas sur la perte.

> 输入 6 个标签的来源和 5 个标签的目标──验证输出形状是 `(5, vocab)`◊ ne pas s'intéresser à l'architecture, ne pas s'intéresser à la perte.

### Étape 4: Swap dans RMSNorm + SwiGLU

Remplacez LayerNorm et ReLU-FFN par RMSNorm et SwiGLU. Confirmez que les formes correspondent toujours.

> Utilisation de la norme RMSNorm et de la norme SwiGLU  remplacement de la coucheNorm et de la norme ReLU-FFN── confirmation de forme encore correspondant── c'est à travers une fonction de remplacement réalisée en 2026 année de modernisation──

## Utilisez-le avec le cadre de réalisation

Les mises en œuvre de référence PyTorch/TF: `nn.TransformerEncoderLayer`- Je suis là .`nn.TransformerDecoderLayer`Mais la plupart des codes de production 2026 ont leur propre bloc car:

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer`- Je suis là.`nn.TransformerDecoderLayer` Mais la plupart des codes de production de 2026 sont auto-construits, car:

- L'attention flash est appelée à l'intérieur de l'attention, pas par l'intermédiaire de `nn.MultiheadAttention`- Je suis désolé .
  Attention flash dans l'attention interne, pas de passage `nn.MultiheadAttention`Il y a une autre.
- Les GQA/MLA ne sont pas dans la référence stdlib.
  GQA / MLA 不在标准库参考中──
- RoPE, RMSNorm, SwiGLU ne sont pas les défauts PyTorch.
  RoPE、RMSNorm、SwiGLU n'est pas la valeur par défaut de PyTorch.

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**三种架构的选择:Encoder-only(BERT)适合分类和嵌入;Decoder-only(GPT/Llama)适合生成和通用任务;Encoder-Decoder(T5/BART)适合有明确的"源序列"结构化转换任务──2026年的主流选择是Decoder-only,因为它的扩展性最好、训练最简洁──

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU (Swish-Gated Linear Unit) par le biais d'un mécanisme de contrôle de porte permet à FFN de mieux exprimer ses capacités. Llama, PaLM, Qwen, etc. Les expériences de modèle indiquent que SwiGLU est inférieur à ReLU/GELU en termes de confusion linguistique.

## Envoyez-le . Produit .

Regardez !`outputs/skill-transformer-block-reviewer.md`. La compétence examine une nouvelle mise en œuvre de bloc de transformateur contre les défauts de 2026 et détecte les pièces manquantes (pre-norme, RoPE, RMSNorm, GQA, FFN ratio d'expansion).

> 参见 `outputs/skill-transformer-block-reviewer.md` Cette compétence, en fonction du paramètre par défaut de 2026 d'examen de nouveaux blocs de transformateurs, est réalisée et a été marquée par la défaillance de la partie.

## Les exercices

1. **Easy / 简单。**Comptez les paramètres dans votre encoder_block à `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Valider en mettant en œuvre le bloc et en utilisant `sum(p.numel() for p in block.parameters())`- Je suis désolé .
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`La preuve

2. **Medium / 中等。**Passez de post-norme à pré-norme. Initializer les deux et mesurer la norme d'activation après 12 couches empilées sur entrée aléatoire.
   De la transition de la post-régulier à la pré-régulier. Les deux premiers sont mesurés par 12 couches de charge sur les paramètres d'activation de l'entrée au hasard.

3. **Hard / 困难。**Implémenter un encodeur-décodeur à 4 couches sur une tâche de copie de jouet (copie `x`Retour à la ligne de départ.
   Dans les tâches de reproduction de jouets`x`) sur la réalisation de 4 niveaux de codeur-décodeur.

## Les termes clés

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Block / 块 | "One transformer layer" / "一个 Transformer 层" | Stack of norm + attention + norm + FFN, wrapped in residual connections. 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| Residual / 残差连接 | "Skip connection" / "跳跃连接" | `x + f(x)` output; enables gradient flow through deep stacks. `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| Pre-norm / 前归一化 | "Normalize before, not after" / "先归一化，不是后归一化" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "LayerNorm without the mean" / "没有均值的 LayerNorm" | Divide by RMS; one less op, same empirical stability. 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "The FFN everyone switched to" / "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. 在 LM 困惑度上击败 ReLU/GELU。 |
| Cross-attention / 交叉注意力 | "How the decoder sees the encoder" / "解码器如何看到编码器" | MHA with Q from decoder, K/V from encoder outputs. MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN expansion / FFN 扩展比 | "How wide the middle MLP is" / "中间 MLP 有多宽" | Ratio of hidden-size to d_model, usually 4 or 2.6 (SwiGLU). 隐藏大小与 d_model 的比率，通常为 4 或 2.6（SwiGLU）。 |
| Bias-free / 无偏置 | "Drop the +b terms" / "去掉 +b 项" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## Encore une lecture

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) spécifications originales du bloc.
  Vaswani 等人(2017)  原始块规范──

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745)Pourquoi la pré-norme bat profondément la post-norme.
  Xiong 等人(2020)  Pourquoi la pré-réunion au milieu de la victoire après la réunion ?

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) le papier SwiGLU.
  Shazeer(2020)  SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) bloc canonique 2026 décoteur seulement.
  Des câlins .`modeling_llama.py` 2026                                                                                                                                                                                                                                                             
