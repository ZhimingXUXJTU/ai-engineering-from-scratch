# Mecanismo de atenção A descoberta

> O decodificador deixa de olhar para um resumo comprimido e começa a olhar para toda a fonte.
> O descifrador não mais olha para o resumo, começa a olhar para a fonte inteira.

> **【中文解读】**O mecanismo de atenção faz com que o modelo se concentre em partes relacionadas da entrada.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A lição 09 terminou com uma falha medida. Um codificador-decodificador GRU treinado em uma tarefa de cópia de brinquedo vai de 89% de precisão na comprimento 5 para quase acaso na comprimento 80. A razão é estrutural, não um erro de treinamento: cada bit de informação coletada pelo codificador tem que caber em um estado oculto de tamanho fixo, e o decodificador nunca vê nada mais.

> Seção 09                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

Bahdanau, Cho e Bengio publicaram uma correção de três linhas em 2014. Em vez de dar ao decodificador apenas o estado final do encodificador, mantenha cada estado do encodificador. Em cada passo do decodificador, calcule uma média ponderada dos estados do encodificador onde os pesos dizem "quanto o decodificador precisa olhar para a posição do encodificador `i`Essa média ponderada é o contexto, e muda cada passo do decodificador.

> Bahdanau、Cho 和 Bengio em 2014 publicou uma terceira revisão. Não apenas dá ao decodificador o estado final do codificador, mas mantém cada estado do codificador. Em cada passo do decodificador, calcula o aumento de peso do estado do codificador.`i`"Este aumento de potência é acima e abaixo, ele muda em cada passo do decodificador.

É essa a ideia. Os transformadores ampliaram-na. A auto-atenção aplicou-a a uma única sequência. A atenção multi-head correu em paralelo. Mas a versão de 2014 já quebrou o gargalo de engarrafamento, e uma vez que você tem, o pivô para transformadores é engenharia, não conceitual.

> É assim que a ideia é: o transformador o ampliou. A própria atenção vai aplicá-lo a uma única sequência.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

Em cada passo de decodificação `t`- Não .

> Em cada passo de código`t`- Não .

1. Use o estado oculto do decodificador anterior `s_{t-1}`como um **query**- Não .
2. Ponha-o contra cada estado de codificação oculto .`h_1, ..., h_T`Um escalar por posição do codificador.
3. Softmax as pontuações para obter pesos de atenção `α_{t,1}, ..., α_{t,T}`que a soma é de 1.
4. Vêctor de contexto `c_t = Σ α_{t,i} * h_i`- Media ponderada dos estados do codificador.
5. O decodificador leva `c_t`mais o token de saída anterior, produz o próximo token.
   1. Use anterior um descifrador estado oculto `s_{t-1}` Como**查询（Query）**- Não.
   2. O que é que é o código?`h_1, ..., h_T`打分── cada codificador de posição é um símbolo──
   3. Para fazer o fraco máximo , obter o peso da atenção .`α_{t,1}, ..., α_{t,T}`, som&gt; é 1
   4. 上下文向量 `c_t = Σ α_{t,i} * h_i`◊ aumento de peso média do estado do codificador
   5. - Não .`c_t`Adicionando o primeiro token de saída, produzir o próximo token.

A média ponderada é o ponto. Quando o decodificador precisa traduzir "Je" para "I", ele pesa o estado do codificador sobre "Je" alto e os outros baixos. Quando ele precisa de "não", ele pesa "pas" alto. O vetor de contexto remodela cada passo.

> Quando o sistema de codificação precisa de "Je" 翻译为"I" 时,它对"Je"上的编码器状态权重高,其他低──当需要"not" 时,它对"pas"权重高──上下文向量在每步重塑──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Formas (a coisa que morde a todos) 形状

É aqui que toda implementação de atenção vai mal a primeira vez.

> É o primeiro lugar em que cada atenção é feita.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Não .

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Não.

- `s_{t-1}`tem forma`(d_s,)`- Não .`h_i`tem forma`(d_h,)`- Não .
- `W_a`tem forma`(d_attn, d_s)`- Não .`U_a`tem forma`(d_attn, d_h)`- Não .
- A sua soma dentro do tanh tem forma .`(d_attn,)`- Não .
- `v_α`tem forma`(d_attn,)`O produto interno com`v_α`- Ele desmorona para um escalar.**This is what `v_α` does.**Não é mágica, é a projeção que transforma um vetor de atenção-dim em uma pontuação escalar.
  - `s_{t-1}`形状为 `(d_s,)`- Não .`h_i`形状为 `(d_h,)`- Não.
  - `W_a`形状为 `(d_attn, d_s)`- Não.`U_a`形状为 `(d_attn, d_h)`- Não.
  - Tanh 内部的和形为 `(d_attn,)`- Não.
  - `v_α`形状为 `(d_attn,)` Com`v_α`O seu volume é reduzido para o volume.**这就是 `v_α` 的作用。**Não é magia. É a projeção da dimensão de tensão para a quantidade de pontos.

**Luong (multiplicative) score.**Três variantes:

> **Luong（乘性）分数。**Três variações:

- `dot`- Não .`e_{t,i} = s_t^T * h_i`- Requer .`d_s == d_h`- Não, não, não, não.
  `dot`- Não .`e_{t,i} = s_t^T * h_i` Requisitos`d_s == d_h`Se o codificador for bi-direcionado, então salta.
- `general`- Não .`e_{t,i} = s_t^T * W * h_i`com`W`forma`(d_s, d_h)`Remove a restrição de igual dim.
  `general`- Não .`e_{t,i} = s_t^T * W * h_i`- Não .`W`形状为 `(d_s, d_h)`❖ Movimento e manutenção
- `concat`A forma Bahdanau é essencialmente a mais rara, já que as duas primeiras são mais baratas.
  `concat`A forma Bahdanau é muito mais barato.

**One Bahdanau / Luong gotcha worth naming.**Bahdanau utiliza `s_{t-1}`(o estado do decodificador * antes de * gerar a palavra atual). Luong usa `s_t`(o estado *após *). misturando-os produz gradientes sutilmente errados que são extremamente difíceis de depurar.

> **一个值得注意的 Bahdanau / Luong 陷阱。**Bahdanau 使用 `s_{t-1}`(生成当前词*之前*的解码器状态) ―Long 使用 `s_t`(em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em inglês) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão) (em alemão))

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
attention-heatmap
```

## Construí-lo

### Passo 1: atenção aditiva (Bahdanau)

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

Verifique as suas formas contra a mesa acima.`encoder_states`tem forma`(T_enc, d_h)`- Não .`projected_enc`tem forma`(T_enc, d_attn)`- Não .`projected_dec`tem forma`(d_attn,)`e transmissões. `combined`tem forma`(T_enc, d_attn)`- Não .`scores`tem forma`(T_enc,)`- Não .`weights`tem forma`(T_enc,)`- Não .`context`tem forma`(d_h,)`- Envia-o.

> Controle o seu estado de forma.`encoder_states`形状为 `(T_enc, d_h)`- Não.`projected_enc`形状为 `(T_enc, d_attn)`- Não.`projected_dec`形状为 `(d_attn,)`Não se transmite.`combined`形状为 `(T_enc, d_attn)`- Não.`scores`形状为 `(T_enc,)`- Não.`weights`形状为 `(T_enc,)`- Não.`context`形状为 `(d_h,)`Já está.

### Passo 2: Luong dot e geral

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

É por isso que o papel de Luong chegou, com a mesma precisão na maioria das tarefas, muito menos código.

> Cada três linhas. É o significado do artigo Luong. Na maioria das tarefas, a mesma precisão, o código é muito menor.

### Passo 3: exemplo numérico trabalhado

Dado três estados de codificação (aproximadamente "cat", "sat", "mat") e um estado de decodificação que alinha mais com o primeiro, a distribuição de atenção se concentra na posição 0.

> 给定三个编码器状态 ((大致是"cat"、"sat"、"mat") e um com o primeiro mais em linha com o estado do decodificador, concentração de atenção distribuída em posição 0。

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

A primeira linha ganha, depois move o estado do decodificador mais perto do terceiro estado do encodificador e observe a mudança de pesos.

> Primeiro, ele vai mudar o seu estado de código para o terceiro, e então ele vai mudar de peso.

### Passo 4: por que esta é a ponte para transformadores

Traduza a linguagem acima para Q/K/V:

> 将上的语言翻译为:

- **Query**= estado do decodificador `s_{t-1}`
  **查询（Query）**= estado do computador`s_{t-1}`
- **Key**= estados de codificação (o que nós pontuação em relação)
  **键（Key）**= 编码器状态 (temos usado para fazer distinções)
- **Value**= estados de codificação (o que pesamos e somamos)
  **值（Value）**= 编码器状态(我们用来加权和的对象)

Na atenção clássica, as chaves e os valores são a mesma coisa. A auto-atenção as separa: você pode consultar uma sequência contra si mesma, com diferentes projeções aprendidas para K e V. A atenção multi-cabeça executa-a em paralelo com diferentes projeções aprendidas. Os transformadores empilham o estágio inteiro muitas vezes e soltam RNNs.

> Na atenção clássica, o valor e o valor são a mesma coisa. A atenção própria irá separá-los: você pode usar diferentes estudos para pesquisar uma sequência como K e V.

A matemática é a mesma, as formas são as mesmas, o salto pedagógico da atenção Bahdanau para a atenção escalada de produto de ponto é principalmente notação.

> A matemática é a mesma. A forma é a mesma. O salto do ensino do Bahdanau atenção para o ponto de concentração e concentração de atenção é principalmente um símbolo.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

PyTorch e TensorFlow enviam a atenção diretamente.

> PyTorch e TensorFlow  directamente prestar atenção

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

É uma camada de atenção do transformador. Batalha de consulta de 5 posições, bateria de chave/valor de 10 posições, 128-dim cada, 8 cabeças.`output`É a nova consulta aumentada de contexto. `weights`é a matriz de alinhamento 5x10 que você pode visualizar.

> É um transformador. Atenção.`output`É novo, mais forte.`weights`É uma matriz de 5x10, você pode visualizá-la.

### Quando a atenção clássica ainda é importante

- A versão de cabeça única, de camada única, baseada no RNN torna cada conceito visível.
  Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching: Teaching:
- tarefas de sequência no dispositivo em que os transformadores não se encaixam.
  Transformador 放不下设备端序列任务。
- Qualquer artigo de 2014 a 2017 vai ser mal lido sem saber a convenção de Bahdanau.
  Qualquer artigo de 2014-2017 não sabe Bahdanau's约定你会误读它──
- Análise de alinhamento de grãos finos em MT. Pesos de atenção em bruto são uma ferramenta de interpretação mesmo em modelos de transformadores, e lê-los requer saber o que são.
  A pequena parte da análise em tradução automática é um instrumento explicativo, mas o que é preciso saber é o que é.

### A armadilha da atenção-peso-como-explicação

Os pesos de atenção parecem interpretáveis. São pesos que somam a um em todas as posições; você pode traçar-os; alto significa "olhado para isso".

> O peso da atenção parece explicável. Eles são pesados em várias posições e são de um; você pode desenhá-los; alto significa "olhou isto".

Eles não são tão interpretáveis quanto parecem. Jain e Wallace (2019) mostraram que as distribuições de atenção podem ser permutadas e substituídas por alternativas arbitrárias sem mudar as previsões de modelos para algumas tarefas. Nunca relatar pesos de atenção como evidência de raciocínio sem uma ablação ou verificação contrafactual.

> Eles não parecem tão explicáveis. Jane e Wallace (2019) mostram que a distribuição da atenção pode ser substituída e substituída por qualquer substituição, sem alterar a previsão do modelo de certas tarefas. Nunca deve ser usado como evidência de hipótese em casos sem análise de consumo ou contratação de fatos.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-attention-shapes.md`- Não .

> 保存为 `outputs/prompt-attention-shapes.md`- Não .

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

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Implementação `softmax`Mascarar para que os tokens de enchimento no codificador tenham peso de atenção zero.
   **简单。** realização `softmax`掩码, fazer que o token de enchimento no codificador tenha o peso de atenção em zero.
2. **Medium.**Adicionar atenção multi-cabeça para o Luong `general`Forma.`d_h`em`n_heads`Grupos, atender por cabeça, concatenar, verificar se o caso de cabeça única coincide com a sua implementação anterior.
   **中等。**Por Luong`general`Forma-a-do-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-de-tão-tão-de-tão-de-tão-tão-de-tão-de-tão-tão-de-tão-de-tão-tão-de-tão-tão-de-tão-tão-de-tão-tão-tão-de-tão-tão-de-tão-tão-tão-de-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-tão-`d_h`- Não .`n_heads`组, cada um deles executar atenção,拼接, 验证单头情况与你之前实现匹配.
3. **Hard.**Treinar um codificador-decodificador GRU com Bahdanau atenção na tarefa de cópia de brinquedo da lição 09. A precisão da trama vs comprimento da sequência. Comparar com a linha de base de falta de atenção. Você deve ver a lacuna aumentar à medida que o comprimento cresce, confirmando atenção levanta o gargalo de engarrafamento.
   **困难。**Na 9a aula, treinar na tarefa de cópia de brinquedos com Bahdanau Atenção GRU 编码器-解码器──绘制准确率 vs.序列长度──与无注意力基线相比── Você deve ver a diferença crescendo e aumentando com a duração, confirmar que a atenção foi desligada──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)O jornal.
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) as três variantes de pontuação e sua comparação. / 三种分数变体及其比较──
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) a precaução de interpretação. / 可解释性警示──
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) caminhada de execução com PyTorch. / 带 PyTorch 的可运行演练──
