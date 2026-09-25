# Encodificação de posição  Sinusoidal, RoPE, ALiBi
# Posição  正弦、RoPE、ALiBi

> A atenção é invariavel em permutação. "O gato sentou no tapete" e "mat o gato sat no tapete" produzem a mesma saída sem sinal posicional. Três algoritmos o corrigem  cada um com uma aposta diferente sobre o que significa "posição".

> Atenção é a linha de mudança. O gato sentou-se no tapete e o gato sentou-se no tapete.

> **【中文解读】**Transformador 没有位置信息,需要手动注入──RoPE é método de uso de Llama, ALiBi 支持外推到更长序列──

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A atenção do produto de ponto é cega à ordem.`softmax(Q K^T / √d) V`É calculado a partir de semelhanças em pares.`X`Nada dentro da atenção se importa com a posição.

> 缩放点积注意力是顺序无关的──注意力矩阵 `softmax(Q K^T / √d) V`Por causa da comparação calculada e por causa da perturbação.`X`A linha, a saída, a saída são perturbadas da mesma forma.

Não é um erro num modelo de saco de palavras. Para linguagem, código, áudio, vídeo  qualquer coisa onde a ordem carrega significado  é fatal.

> No modelo de palavras, não é um bug, mas para linguagem, código, áudio, vídeo, qualquer ordem de coisas que possam ter significado é fatal.

A solução é injetar posição nos embeddings de alguma forma.

> O método de reparação é de alguma forma inserir a posição em um embutidos.

1. **Absolute sinusoidal**(Vaswani 2017). Adicionar `sin/cos`Simples, livres de aprendizagem, extrapolam mal além dos comprimentos treinados.
   **绝对正弦编码**(Vaswani 2017)。将位置的 `sin/cos`Adição a embutidos. Simples. Não precisa de aprendizagem.

2. **RoPE — Rotary Position Embeddings**(Su 2021). Rotar os vetores Q e K por um ângulo proporcional à posição. Encode * posição relativa * diretamente no produto de pontos. Dominant em 2026.
   **RoPE — 旋转位置嵌入**(Su 2021) ・ em relação à posição em relação ao ângulo de rotação Q 和 K 向量── diretamente em relação à posição──2026

3. **ALiBi — Attention with Linear Biases**(Presião 2022). Salte integrados inteiramente; adicione uma penalidade linear por cabeça às pontuações de atenção com base na distância. Excelente extrapolação de comprimento.
   **ALiBi — 带线性偏置的注意力**(Presião 2022):  total saltar embutidos; adicionar a punição de cada cabeça em função da distância para a atenção.

A partir de 2026, praticamente todos os modelos abertos de fronteira usam RoPE: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi.

> 截至2026年, básicamente cada modelo de origem aberta da linha de frente utiliza RoPE:Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。

> **【中文解读】**O sistema de codificação de três posições representa três épocas: 1) o código de cordas de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha de linha

## O conceito central.

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### Absoluto sinusoidal.

Pre-computação de uma matriz fixa `PE`de forma`(max_len, d_model)`- Não .

> 预计算一个固定矩阵 `PE`, forma `(max_len, d_model)`- Não .

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

Então ...`X' = X + PE[:N]`Cada dimensão é um sinusoide em uma frequência diferente.`max_len`O modelo não tinha conhecimento do que acontece na posição 2048 quando só viu posições 02047.

> Então, em atenção.`X' = X + PE[:N]`◊ cada dimensão é de diferentes frequências de os cordos.`max_len`Outrofacto: o modelo só viu a posição 0-2047 , nada diz que ele vai estar na posição 2048 

### RoPE - Roteamento de posição embutida

Rotar os vetores Q e K (não incorporados). Para um par de dimensões `(2i, 2i+1)`- Não .

> 旋转 Q 和 K 向量( não embutidos) ⋅对一对维度 `(2i, 2i+1)`- Não .

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Aplicar a mesma rotação às teclas com posição `pos_k`O produto de pontos`q'_m · k'_n`torna-se uma função de `(m - n)`- Só a mim.**the attention score depends only on the relative distance**- É um truque bonito.

> Para a posição de aplicação`pos_k`Da mesma rotação.`q'_m · k'_n`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `(m - n)`Definição:**注意力分数只取决于相对距离**Mesmo que a rotação seja baseada em uma posição absoluta...

> **【中文解读】**A vantagem da RoPE: embora o ângulo de rotação baseie-se na posição absoluta, mas o ponto de Q·K depende apenas da distância relativa (m-n) ―― isto significa que o modelo natural geologicamente tem relação de posição relativa―, o parâmetro base também pode ser realizado em longo sentido.

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**Llama 3 通過 YaRN(E outro método de extensão do RoPEN) irá aumentar a partir de 8K 擴展到 128K──核心思路是調節 RoPE 基頻率,使高频度保持原始分辨率,低频度進行插值── essa estratégia de "分维度處理" mantém a percepção da posição precisa de curta distância, além de expandir a capacidade de externalização de longa distância──

Extensão do RoPE: `base`O Llama 3 foi ampliado de 8K para 128K de tal forma.

> 扩展 RoPE:`base`Pode ser reduzido (NTK-consciente, YaRN, LongRoPE) em caso de não re-treinamento, para fora de suporte para mais longo.

### Alibi, com a atenção de desvio linear.

Esqueça o truque de inserção.

> 跳过嵌入技巧──直接偏置注意力分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

Onde ?`m_h`é uma inclinação específica da cabeça (por exemplo `1 / 2^(8·h/H)`O documento mostra que a extrapolação de comprimento supera o sinusoidal e corresponde ao RoPE em seu comprimento treinado original.

> Entre eles `m_h`É especificamente a inclinação do rosto.`1 / 2^(8·h/H)`O texto mostra que a extensão de extratos excede o código de cordas, em sua extensão de treinamento original, correspondendo à RoPE.

### O que escolher em 2026

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

O RoPE ganhou porque chama a atenção sem alterar a arquitetura, codifica a posição relativa e a sua`base`O hiperparâmetro dá um botão limpo para ajuste fino de longo contexto.

> RoPE 胜出 é porque não precisa mudar a estrutura, é inserir atenção, codificar em relação à posição, e o seu `base`O superparâmetro para longo tempo fornece uma configuração clara do giro.

> **【中文解读】**A seleção de código de localização de 2026 é muito clara: novo projeto é padrão RoPE. Não altera a estrutura, o código em relação à posição.

> **【拓展：位置编码对长上下文 RAG 的影响】**No RAG, o código de localização afeta diretamente a capacidade de processamento de arquivos. RoPE + YaRN permite que o Llama 3 possa processar o código de 128K, o que significa que pode processar de forma simultânea cerca de 300 páginas de arquivos. A escolha do programa de localização determina se o sistema RAG precisa de estratégias de blocos complexos.
```figure
rope-explorer
```

## Construí-lo

## Construí-lo e realizei-o.

### Passo 1: codificação sinusoidal. Passo 1: codificação de cordas.

Veja .`code/main.py`Um cálculo de 4 linhas:

> 参见 `code/main.py`△4 行计算:

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

Adicione isto à matriz de incorporação antes da primeira camada de atenção.

> Antes da primeira camada de atenção, será adicionado à matriça embutida.

### Passo 2: RoPE aplicado a Q, K. Passo 2: RoPE  aplicado a Q 、K

O RoPE opera no local em Q e K. Para cada par de dimmers:

> RoPE para Q 和 K operações de origem:

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

Crucial: aplicar a mesma função a Q na posição `m`E K na posição `n`O produto deles pega um .`cos((m-n)·θ_i)`A atenção aprende a posição relativa de graça.

> 关键: em posição `m`De Q e posição`n`de K  aplicam a mesma função.`cos((m-n)·θ_i)`Porque... atenção... aprendi a aprender a relação...

> **【中文解读】**O núcleo de realização do RoPE: fazer uma rotação em relação à posição de cada um dos Q e K (2i, 2i+1) e a posição de cada um dos K em relação à posição de K, por isso os pontos de Q_m · K_n aparecem em cosmos, em que a natureza codifica a distância em relação à posição de K.

### Passo 3: Alíbi inclinações e preconceitos

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

Adicionar`bias[h]`- O que é ?`(seq_len, seq_len)`Matriz de pontuação de atenção da cabeça `h`, depois softmax.

> - Não .`bias[h]`Adição ao cabeçalho`h`de `(seq_len, seq_len)`Atenção à massa, então suavemax.

### Passo 4: Verificar propriedade relativa de distância do RoPE. Passo 4: Verificar propriedade relativa de distância do RoPE.

Escolha dois vetores aleatórios .`a, b`- Vira por .`(pos_a, pos_b)`- Então , por ...`(pos_a + k, pos_b + k)`. Ambos os produtos de pontos devem corresponder no erro de ponto flutuante. Essa propriedade é o ponto inteiro de RoPE  é invariante ao deslocamento absoluto, só a diferença relativa é importante.

> 选择两个随机向量 `a, b`- Não.`(pos_a, pos_b)`- Então, então, use.`(pos_a + k, pos_b + k)`旋转── dois pontos de acumulação em torno do erro de ponto devem se combinar. Esta característica é o significado total do RoPE.

> **【拓展：位置编码的历史演进】**De Vaswani(2017) para o código de cordas de direção absoluta, até GPT-2/3 para inserção em posição de aprendizagem, novamente para RoPE(2021) e ALiBi(2022), o código de direção passou por uma mudança de padrão de "localização absoluta" para "localização relativa".

## Use-o com o framework implementado.

PyTorch 2.5+ embarca serviços de RoPE em `torch.nn.functional`A maioria dos códigos de produção usa`flash_attn`ou `xformers`onde o RoPE é aplicado dentro do núcleo de atenção.

> PyTorch 2.5+ em`torch.nn.functional`中内置了 RoPE 工具── maioria dos produtos utilizam código `flash_attn`Ou `xformers`, dos quais a RoPE é aplicada no interior da atenção intèrna.

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**Redescálculos`base`- Não .`base * (scale_factor)^(d/(d-2))`quando se estende de 4K a 16K+.
  **NTK-aware 插值。**Quando de 4K  expandido para 16K + 时,将 `base`重新缩放为 `base * (scale_factor)^(d/(d-2))`- Não.
- **YaRN.**Interpolação mais inteligente que preserva a entropia da atenção em contextos longos.
  **YaRN。**Mais inteligência, manter a atenção sobre o texto abaixo.
- **LongRoPE.**O método 2024 da Microsoft que usa a pesquisa evolutiva para escolher fatores de escala por dimensão.
  **LongRoPE。**Microsoft 2024 anos de método, usando evolução de pesquisa selecionar por dimensão diminuir o fator.
- **Position interpolation + fine-tuning.**Apenas reduzir as posições pelo fator de extensão e ajustar para tokens de 15B. Surpreendentemente eficaz.
  **位置插值 + 微调。**Apenas é preciso, por expansão, um factor de redução de posição e uma pequena mudança de 1-5B.

## Envia-o . Produto .

Veja .`outputs/skill-positional-encoding-picker.md`. A habilidade escolhe uma estratégia de codificação para um novo modelo, dada a extensão do contexto-alvo, as necessidades de extrapolação e o orçamento de formação.

> 参见 `outputs/skill-positional-encoding-picker.md` Esta habilidade é utilizada para escolher estratégias de codificação de novos modelos, tendo como objetivo a duração da sua produção, a necessidade de desenvolvimento e o orçamento de treinamento.

## Exercícios.

1. **Easy / 简单。**Traçar o sinusoidal `PE`Matrix como mapa de calor para `max_len=512, d=128`Confirmar o padrão "as tiras ficam mais largas à medida que o índice de dimensões cresce".
   Vai estar bem.`PE`矩阵绘制为 `max_len=512, d=128`O modelo de "aumentar a linha de linha de larga escala"

2. **Medium / 中等。**Implementar a escalação do RoPE com NTK. Treinar um pequeno LM em sequências de comprimento 256, depois testar no comprimento 1024 com e sem escalação. Medir a perplexidade.
   实现 NTK-consciente RoPE 缩放── treinar um LM de pequeno tipo em sequência de 256 de longitude, então testar a longitude 1024── em caso de contagem e não de contagem──

3. **Hard / 困难。**Implementar ALiBi e RoPE no mesmo módulo de atenção. Treinar um transformador de 4 camadas em uma tarefa de cópia com sequências de comprimento 512. Extrapolar para 2048 no momento do teste. Comparar degradação.
   Em um mesmo módulo de atenção, a realização de ALiBi e RoPE. Em uma série de longitudes 512 de tarefas de replicação, a formação de um transformador de 4 níveis.

## Termos-chave .

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

## Mais leitura 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762)- Sinusoidal original.
  Vaswani 等人(2017)  原始正弦编码──

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)Papel RoPE.
  Su 等人(2021)  RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409)- Alibi.
  Press, Smith, Lewis... (em 2021)

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) Estado de ponta de escalagem RoPE.
  Peng 等人(2023)  Última evolução do RoPE 缩放──

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595) O artigo de longo contexto Llama 2 do Meta.
  Chen 等人(2023)  Meta's Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) o método Microsoft utilizado pelo Phi-3-Long.
  Ding 等人(2024)  Microsoft's method, foi usado Phi-3-Long.

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) Implementações de cada sistema de escalagem de RoPE em nível de produção.
  EmbracingFace Transformers  Propriedade RoPE 缩放方案的生产级实现──
