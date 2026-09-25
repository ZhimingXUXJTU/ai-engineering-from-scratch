# Atenção de várias cabeças
# Multiplicação de atenção

> Uma cabeça de atenção aprende uma relação por vez, oito cabeças aprendem oito cabeças são livres, pegue mais delas.

> Uma atenção na primeira vez para aprender uma relação.

> **【中文解读】**O modelo de atenção múltipla concentra-se simultaneamente em diferentes tipos de relações: linguagem, linguagem, posição, etc.

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Uma única cabeça de auto-atenção calcula uma matriz de atenção. Essa matriz capta um tipo de relação  geralmente aquela que minimiza a perda em qualquer sinal de treinamento. Se os seus dados têm acordo sujeito-verbo, co-referência, discurso de longo alcance e fragmentos sintáticos todos emaranhados juntos, uma única cabeça os esmagia em uma única distribuição de max soft e perde metade do sinal.

> 单个自注意头计算一个注意矩阵―― essa矩阵捕获一种关系通常是最小化训练信号损失的一种―― Se os seus dados principais entre os mesmos são united,共指消解,长程语篇和句法分块纠在一起,单个头会模糊它们成单软max 分布,丢失半信号――

A correção do artigo Vaswani de 2017: executar várias funções de atenção em paralelo, cada uma com suas próprias projeções Q, K, V, e concatenar as saídas.`d_model / n_heads`Os parâmetros totais permanecem iguais.

> 2017 Vaswani 论文的修复方案:并行运行多个注意力函数, cada um tem seu próprio Q、K、V 投影, então拼接输出──每个头在维度为`d_model / n_heads`O número de componentes não muda, a capacidade de expressão aumenta.

A atenção multi-cabeça é o padrão de cada transformador em 2026 navios com. O único argumento é sobre * quantas cabeças * e se as chaves e valores compartilham projeções (Attenção de Queria Grupada, Attenção de Queria Multi, Attenção Latente de Multi-cabeça).

> Multi-headed attention é a configuração padrão de cada Transformer em 2026 e a única discussão é sobre * quantas* cabeças e se o valor e o valor são compartilhados em projetos ([[:o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_

> **【中文解读】**

## O conceito central.

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**- Toma .`X`de forma`(N, d_model)`Projeto para Q, K, V de cada forma`(N, d_model)`- Refazer para`(N, n_heads, d_head)`onde`d_head = d_model / n_heads`Transpor para`(n_heads, N, d_head)`- Não .

> **拆分。**取形为 `(N, d_model)`de `X`◊ Projeção até forma`(N, d_model)`O que é que é o que é?`(N, n_heads, d_head)`, entre os `d_head = d_model / n_heads`                                                                                                                                                                                                                                                              `(n_heads, N, d_head)`- Não.

**Attend in parallel.**Execute uma escala de atenção de ponto-produto dentro de cada cabeça.`(N, d_head)`As cabeças operam em diferentes subespaços da incorporação e nunca falam durante o próprio cálculo da atenção.

> **并行计算注意力。**Em cada cabeça, o funcionamento reduz o ponto de concentração de atenção.`(N, d_head)`头在嵌入的不同子空间上操作,在注意计算本身期间互不通信──

**Concatenate and project.**- A cabeça de pila volta para o`(N, d_model)`e multiplicar por uma matriz de saída aprendida `W_o`de forma`(d_model, d_model)`- Não .`W_o`É onde as cabeças se misturam.

> **拼接并投影。**Vai re-empenhar-se para`(N, d_model)`Não multiplicando a matriz de saída de aprendizagem`W_o`, forma `(d_model, d_model)`- Não.`W_o`É um lugar misturado.

**Why it works.**Cada cabeça pode se especializar sem competir com os outros para o orçamento representativo. Estudos de pesquisa de 20192024 mostram papéis distintos de cabeça: cabeças posicionais, cabeça que atende ao token anterior, cabeças de cópia, cabeças de entidade nomeada, cabeças de indução (que são a base da aprendizagem no contexto).

> **为什么有效。**Cada cabeça pode ser especializada sem competir com outros títulos para representar o orçamento. Pesquisas de pesquisa de 2019-2024 mostraram diferentes papéis de cabeça: posição de cabeça, atenção ao primeiro token de cabeça, duplicação de cabeça, nome de corpo, cabeçalho de registo, que é a base para a literatura de cima e baixo.

> **【中文解读】**三步走:Split(拆分到多个子空间)→ Participação(cada cabeça independente fazer atenção)→ Concat+Projeto(拼接并通过 W_o 混合)。

> **【拓展：GQA 在 Llama 3 中的实际应用】**Llama 3 70B utiliza 64 cabeças de consulta, mas apenas 8 cabeças de KV, o KV 缓存压缩了8倍――这在推理时节省大量显存,同时几乎不损失模型质量――GQA 已成为2024-2026年开源大模型的标配――DeepSeek-V2 的 MLA则进一步,将 KV 压缩到低排隐空间――

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA é o padrão moderno porque reduz a memória de cache KV por um fator de `N/G`MLA vai mais longe comprimindo K/V em um espaço latente, e depois projetando de volta no tempo de computação  custa FLOPs, economiza muito mais memória.

> GQA é uma opção moderna, porque reduzirá o KV 缓存内存 `N/G`倍, ao mesmo tempo, manter quase a qualidade completa. MLA 通過將 K/V 壓縮到隱藏空間更进一步,然后在計算時投影回來,省更多内存.

## Construí-lo e realizei-o.
```figure
multihead-split
```

## Construí-lo

### Passo 1: Divida as cabeças da atenção de cabeça única que já temos. Passo 1: Divida a atenção de cabeça única.

Leva o .`SelfAttention`A partir da lição 02 e envolver com um par de divisão/conca.`code/main.py`para uma implementação numpica; a lógica é:

> 取第 02 课的   取第 02 课的                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `SelfAttention`, Usando a separação /拼接对包装它──参见 `code/main.py`中的 numpy 实现; lóg辑如下:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

Um reformula e outro transponha, sem ciclo, é exatamente o que o PyTorch faz sob`nn.MultiheadAttention`- Não .

> Uma vez reformulado e uma vez transposto. Não há ciclo.`nn.MultiheadAttention`O que faz o nível inferior.

> **【中文解读】** `split_heads`和 `combine_heads`                                                                                                                                                                                                                                                              

### Passo 2: Execute escalado ponto-produto atenção por cabeça  passo 2: cada cabeça operação reduzir ponto acumulação atenção

Cada cabeça recebe sua própria fatia de Q, K, V. A atenção torna-se um matmul em lote:

> Cada cabeça obtém seu próprio Q、K、V 切片── atenção para se transformar em massa de matrizes multiplicadas:

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

Em hardware real .`Qh @ Kh.transpose(...)`É um .`bmm`A GPU vê um único batch de forma .`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Adicionar cabeças é livre.

> Em hardware real,`Qh @ Kh.transpose(...)`É uma vez.`bmm`O GPU vê que é forma`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`O aumento de volume é gratuito.

### Passo 3: Grupo-Query Variante de atenção . Passo 3:

Só as projeções de chave e valor mudam.`n_heads`grupos; K e V obtêm`n_kv_heads < n_heads`grupos e são repetidas para corresponderem:

>  Só a projecção de chave e valor é alterada.`n_heads`- E o que é que é ?`n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

Em inferência , isso economiza memória porque só`n_kv_heads`cópias vivem no cache KV, não `n_heads`Llama 3 70B usa 64 cabeças de consulta com 8 cabeças de KV  um encolher de cache 8x.

> Quando o pensamos, isso é economizado na memória, porque só...`n_kv_heads`份副本 existem em KV 缓存中, em vez de `n_heads`份──Llama 3 70B Utilize 64 查询头和 8 KV头8 倍缓存缩减──

> **【拓展：MQA/GQA 在推理中的内存节约】**KV 缓存大小与 KV 头号成正比──Llama 3 70B utiliza 64 查询头, mas apenas 8 KV 头, KV 缓存压缩了8倍──对于128K 上下文,这意味着节省数 GB 显存──这是大模型长上下文推理的关键优化GQA 几乎不损质量,但显著降低推理成本──

### Passo 4: Probe o que cada cabeça aprendeu. Passo 4: Explore o que cada cabeça aprendeu.

Exerça a MHA numa frase curta com 4 cabeças.`(N, N)`Você verá diferentes cabeças escolher diferentes estruturas mesmo com inicialização aleatória que é parcialmente sinal, parcialmente simetria de rotação nos subespaços.

> Em um breve período, usamos quatro cabeças para executar o MHA.`(N, N)`Atenção à rectangular. Você verá que, mesmo usando inicialização de azar, diferentes cabeças também escolherão diferentes estruturas.

## Use-o com o framework implementado.

Na PyTorch, a versão de uma linha:

> PyTorch 中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

GQA em relação ao PyTorch 2.5+:

> GQA(PyTorch 2.5+):

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**Regras práticas dos modelos de produção em 2026:

> **多少个头？**Lei de experiência do modelo de produção de 2026:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`Quase sempre cai em 64 ou 128. É a unidade de quanto uma cabeça pode "ver".`sqrt(d_head)`• se ultrapassar o 256, perderá o benefício de "muitos especialistas pequenos".

> `d_head` quase sempre 64 ou 128. É uma unidade de medida que pode "ver" o número de unidades.`sqrt(d_head)`冲突; mais de 256 时, você perdeu os benefícios de "many小专家"

## Envia-o . Produto .

Veja .`outputs/skill-mha-configurator.md`. A competência recomenda o número de cabeças, o número de cabeças kv e a estratégia de projecção para um novo transformador, dado o orçamento de parâmetros, o comprimento da sequência e o objetivo de implantação.

> 参见 `outputs/skill-mha-configurator.md` Esta habilidade é utilizada para o novo transformador                                                                                                                                                                                                                                                         

## Exercícios.

1. **Easy / 简单。**Tome o MHA de `code/main.py`e mudança .`n_heads`de 1 a 16 com `d_model=64`A perda de um modelo de uma camada pequena em uma tarefa de cópia sintética.
   取 `code/main.py`Em MHA, em`d_model=64`Em circunstâncias determinadas,`n_heads`De 1 para 16... em uma tarefa de duplicação sintética, desenhar uma perda de modelo de tipo único.

2. **Medium / 中等。**Implementar MQA (um cabeçalho KV compartilhado em todas as cabeçalhas de consulta). Medir a quantidade de parâmetros que caem em conta versus MHA completa.
   实现 MQA(一 KV 头在所有查询头间共享) ⋅ Messação em comparação com MHA completa ⋅ MQA em comparação com MHA

3. **Hard / 困难。**Implementar uma versão pequena de Atenção Latente Multi-Cé: comprimir K, V para um rank-`r`O que é que é que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?`r`A memória cache passa abaixo de 1/8 da MHA completa enquanto a qualidade permanece dentro de 1 bit da validação?
   实现迷你版的多头潜伏注意:将 K,V 压缩为秩 `r`O valor de cache em KV 缓存中存储隐向量, em atenção calcular o tempo de deslição.`r`O valor do cache inferior diminui para 1/8 do MHA completo, enquanto o qualidade permanece em 1 bit da confusão de verificação?

## Termos-chave .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Mais leitura 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) a especificação original de cabeça múltipla.
  Vaswani 等人(2017)  原始多头规范──

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) o documento da MQA.
  Shazeer(2019)  MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) como converter o MHA em GQA após o treino.
  Ainslie 等人(2023)  訓練後如何将 MHA 转换为 GQA──

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA e por que é melhor do que MHA/GQA na memória cache.
  DeepSeek-AI(2024)  MLA 及为何在缓存内存上击败 MHA/GQA──

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) olhar mecanicista para o que as cabeças realmente fazem.
  Olsson 等人 (→ 2022)  Análise do mecanismo das funções reais do teste.

> **【拓展：Induction Heads 与上下文学习】**O estudo antropológico descobriu que a capacidade de aprendizagem literária de transformadores (ou aprendizagem no contexto) é principalmente realizada por um tipo de atenção chamada "cabeça de indução".
