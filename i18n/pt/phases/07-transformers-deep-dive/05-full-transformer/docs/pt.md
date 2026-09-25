# O Transformador Completo  Encoder + Decodificador
# 完整 Transformer  编码器 + 解码器

> A atenção é a estrela. Tudo o resto, resíduos, normalização, alimentação, atenção cruzada, é o andaime que permite que você a apile profundamente.

> O foco é o principal. O resto é o que você pode fazer para que ele possa ser mais profundo.

> **【中文解读】**Colocar a auto-atenção, a multi-cabeça, a FFN, o residual, a camada norma, em um transformador completo.

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Uma camada de atenção única é um extractor de características, não um modelo. Um matmul por camada não é capacidade suficiente para a linguagem. Você precisa de profundidade  e rupturas de profundidade sem a canalização certa.

>                                                                                                                                                                                                                                                               

O documento Vaswani de 2017 contou com seis decisões de design que transformaram uma camada de atenção em um bloco empilhável. Cada transformador desde  encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5)  herda o mesmo esqueleto. Em 2026 os blocos foram refinados (RMSNorm, SwiGLU, pre-norma, RoPE), mas o esqueleto é idêntico.

> Em 2017, Vaswani 论文打包了六个设计决策,将一个注意层变成堆叠的块──此后每个变压器纯编码器(BERT) 纯解码器(GPT) 编码器-解码器(T5) 都继承了相同的骨架──2026年,这些块已经优化了(RMSNorm、SwiGLU、前归化、RoPE),但骨架完全相同──

Esta lição é o esqueleto. As seguintes lições especializam-no  06 para codificadores, 07 para decodificadores, 08 para codificador-decodificador.

> Esta aula é um esquema. A próxima aula é especializada em ele.

> **【中文解读】**单个注意层只是一个特征提取器,不是完整模型――2017论文将六个设计决策包包装成可堆积的块:嵌入+位置编码、自注意力、FFN、残差连接、层归化、交叉注意力――todos os seguintes Transformer 变体BERT、GPT、T5都继承了相同的骨架――

## O conceito central.

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### As seis peças.

1. **Embedding + positional signal.**Tokens → vectores. posição injetada através de RoPE (moderno) ou sinusoidal (clássico).
   **嵌入 + 位置信号。**Token → 向量── através de RoPE(现代)

2. **Self-attention.**Cada posição atende a cada outra, mascarada em decodificadores.
   **自注意力。**Cada posição segue todas as outras posições.

3. **Feed-forward network (FFN).**MLP de duas camadas em termos de posição: `W_2 · activation(W_1 · x)`- Proporção de expansão 4x por padrão.
   **前馈网络 (FFN)。**位置级两层 MLP:`W_2 · activation(W_1 · x)`◊默认扩展比 4×──

4. **Residual connection.** `x + sublayer(x)`Sem isto, os gradientes desaparecem depois de 6 camadas.
   **残差连接。** `x + sublayer(x)`Não há nada, a escala desapareceu depois de seis.

5. **Layer normalization.** `LayerNorm`ou `RMSNorm`Estabiliza o fluxo residual.
   **层归一化。** `LayerNorm`Ou `RMSNorm`(现代) 』稳定残差流 』

6. **Cross-attention (decoder only).**As consultas vêm do decodificador, chaves e valores da saída do encodificador.
   **交叉注意力（仅解码器）。**Queria do decodificador, chave e valor do codificador de saída.

### Bloco de codificação (usado por BERT, T5 codificador)
Observe um fluxo de vetor através de um bloco: a atenção mistura-se entre as posições, o residual leva-o para a frente, o FFN transforma-o, e a norma mantém o fluxo estável.

```figure
transformer-block
```

### Bloco de codificação (utilizado pelo codificador BERT, T5)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

O codificador é bidirecional, não há mascaragem, todas as posições veem todas as posições.

> O codificador é bi-direcionado. Não há esconderijos.

### Bloco de decodificador (usado por GPT, T5 decodificador)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

O decodificador tem três subcamadas por bloco. O centro  atenção cruzada  é o único lugar onde as informações fluem de um codificador para um decodificador. Em uma arquitetura pura de apenas decodificador (GPT), a atenção cruzada é omitida e você apenas tem a auto-atenção mascarada + FFN.

> O sistema de código aberto tem três sub-camadas. O sistema de código aberto é o único sistema de código aberto que possui três subcamadas.

### Pre-norma vs pós-norma .

Papel original: `x + sublayer(LN(x))`- Não .`LN(x + sublayer(x))`O que é mais difícil de treinar profundamente sem um aquecimento cuidadoso.`LN`* antes de * subcamada) é o padrão 2026: Llama, Qwen, GPT-3+, Mistral todos usam.

> Origem:`x + sublayer(LN(x))`- Não .`LN(x + sublayer(x))`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊`LN`Na sub-camada, há um novo modelo de "Llama", que será usado em 2026 por todos os usuários.

### O bloco modernizado de 2026

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

O RMSNorm diminui a centriação média do LayerNorm (uma subtracção menor), o que economiza a computação e é empíricamente pelo menos tão estável.`Swish(W1 x) ⊙ W3 x`) supera consistentemente o FFN ReLU/GELU em ~0,5 pontos na publicação Llama, PaLM e Qwen.

> RMSNorm eliminou a centralização média da LayerNorm (má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-má-`Swish(W1 x) ⊙ W3 x`) em Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约0.5 个困惑度点──

> **【中文解读】**2026 现代 Transformer 块与 2017 原版相比:LayerNorm→RMSNorm,ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA。 Cada melhoramento é gradual, mas a combinação melhorou significativamente a estabilidade do treinamento e a qualidade do modelo。

> **【拓展：为什么 Decoder-only 成为主流】**Embora a estrutura de codificador-descóderos tenha vantagens naturais em tarefas como tradução, mas o modelo de apenas Decoder (GPT、Llama) é mais vencedor em expansão e generalidade. Pode ser usado para processar e gerar tarefas, treinando objetivos, e a expansão já foi verificada pela Lei Chinchilla. Esta é a razão pela qual quase todos os modelos anteriores de 2024-2026 são exclusivos.

### Contagem de parâmetros.

Por um quarteirão com `d_model = d`e expansão do FFN `r`- Não .

> Para um .`d_model = d`且 FFN 扩展比为 `r`O bloco:

- MHA: `4 · d²`(Projeções Q, K, V, O)
  MHA:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`- Não .`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`- Não .`3rd²`
- Normas: insignificantes
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**Os parâmetros do transformador são principalmente concentrados em concentração de atenção ([[4d^2) e FFN]] ([[8d^2]] para SwiGLU) ([[中]]) Llama 3 8B Cada camada é de aproximadamente 1,5B 参数, 32 camadas 共约 7B加上嵌入层和输出头―― compreender a distribuição de parâmetros ajuda a optimizar:MoE 替换FFN pode aumentar o total de parâmetros sem aumentar o cálculo ativo; quantização(como GPTQ、AWQ) principal compressão FFN 权重――

## Construí-lo e realizei-o.

### Passo 1: Os blocos de construção. Passo 1: Construir um módulo.

Usando o pequeno`Matrix`classe da lição 03 (copiada para este arquivo para independência):

> Utilize 第 03 课中的微型 `Matrix`类(ha sido copiado até este documento para manter independente):

- `layer_norm(x, eps=1e-5)`Subtrair a média, dividir por std.
  `layer_norm(x, eps=1e-5)`  减去平均值,除以标准差──
- `rms_norm(x, eps=1e-6)` Divida por RMS. Sem subtracção média.
  `rms_norm(x, eps=1e-6)` Excepto RMS── não reduzido valor médio──
- `gelu(x)`E ...`silu(x) * W3 x`- Não.
  `gelu(x)`和 `silu(x) * W3 x`(SwiGLU)
- `ffn_swiglu(x, W1, W2, W3)`- Não .
- `encoder_block(x, params)`E ...`decoder_block(x, enc_out, params)`- Não .

### Passo 2: Conectar um codificador de 2 camadas e um decodificador de 2 camadas. Passo 2: Conectar um codificador de 2 camadas e um decodificador de 2 camadas.

Aponte-os, passe a saída do codificador em cada atenção transversal do decodificador, adicione um LN final antes da projeção de saída.

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

### Passo 3: Avançar em um exemplo de brinquedo . Passo 3: em um exemplo de brinquedo

Passe uma fonte de 6 tokens e um alvo de 5 tokens. Verifique a forma de saída é `(5, vocab)`Esta lição é sobre arquitetura, não sobre perda.

> 输入 6 个代币的源和 5 个代币的目标──验证输出形状是 `(5, vocab)`Não se preocupem com a construção, não se preocupam com a perda.

### Passo 4: Swap em RMSNorm + SwiGLU 步骤 4: substituir por RMSNorm + SwiGLU

Substitua LayerNorm e ReLU-FFN por RMSNorm e SwiGLU. Confirme que as formas ainda coincidem. Esta é a modernização de 2026 com uma substituição de função.

> Usar RMSNorm 和 SwiGLU 替换 LayerNorm 和 ReLU-FFN── confirmação de forma ainda se corresponde── é através de uma única função substituída realizando 2026 现代化──

## Use-o com o framework implementado.

As implementações de referência PyTorch/TF: `nn.TransformerEncoderLayer`- Não .`nn.TransformerDecoderLayer`Mas a maioria dos códigos de produção 2026 faz o seu próprio bloco porque:

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer`- Não.`nn.TransformerDecoderLayer`Mas a maioria dos códigos de produção de 2026 anos se autoconstruem, pois:

- A atenção flash é chamada para dentro da atenção, não através de`nn.MultiheadAttention`- Não .
  Flash Atenção em atenção interna, não através `nn.MultiheadAttention`- Não.
- GQA / MLA não estão na referência stdlib.
  GQA / MLA Não está em referência à norma.
- RoPE, RMSNorm, SwiGLU não são as configurações padrão do PyTorch.
  RoPE、RMSNorm、SwiGLU não é o valor padrão do PyTorch。

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**三种架构的选择:Encoder-only(BERT)适合分类和嵌入;Decoder-only(GPT/Llama)适合生成和通用任务;Encoder-Decoder(T5/BART)适合有明确的"源序列"的结构化转换任务──2026年的主流选择是Decoder-only,因为它的扩展性最好,训练最简洁──

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU(Swish-Gated Linear Unit) através do mecanismo de controle de portas fazer a expressão da FFN mais forte.

## Envia-o . Produto .

Veja .`outputs/skill-transformer-block-reviewer.md`. A competência revisa a implementação de um novo bloco de transformador contra as anomalias de 2026 e indica as peças faltantes (pre-norma, RoPE, RMSNorm, GQA, FFN ratio de expansão).

> 参见 `outputs/skill-transformer-block-reviewer.md` Esta habilidade, de acordo com a configuração de 2026 em conformidade, revisar o novo bloco de transformador 实现,并标记缺失部分──

## Exercícios.

1. **Easy / 简单。**Conte os parâmetros no seu bloco de codificação em `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Valida através da implementação do bloco e usando `sum(p.numel() for p in block.parameters())`- Não .
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`- Não.

2. **Medium / 中等。**Passe de pós-norma para pré-norma. Iniciar ambos e medir a norma de ativação após 12 camadas empilhadas em entrada aleatória.
   De posterior regeneração de mudança para anterior regeneração. Iniciação e medição de 12 camadas de acumulação em cada entrada.

3. **Hard / 困难。**Implementar um codificador-decodificador de 4 camadas em uma tarefa de cópia de brinquedo (cópia `x`A taxa de perda de RMSNorm + SwiGLU + RoPE  diminui?
   Em jogo de cópia tarefa`x`O que é o RMSNorm + SwiGLU + RoPE?

## Termos-chave .

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

## Mais leitura 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) especificação original do bloco.
  Vaswani 等人(2017)  原始块规范。

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) por que a pré-norma bate profundamente a pós-norma.
  Xiong 等人(2020)  Por que o pre-reunificação em profundidade entre vencer após a reunificação.

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202)O papel SwiGLU.
  Shazeer(2020)  SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) bloco canônico 2026 apenas para decodificadores.
  Abraçando o rosto .`modeling_llama.py` 2026                                                                                                                                                                                                                                                             
