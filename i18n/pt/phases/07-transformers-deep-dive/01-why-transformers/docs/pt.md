# Por que os transformadores  Os problemas com RNNs
# Por que é que o problema do Transformer  RNN

> As RNNs processam tokens uma a uma. Os transformadores processam todos os tokens de uma só vez. Essa única aposta arquitetônica mudou cada curva de escalagem no deep learning após 2017.

> RNN 个别处理 token──Transformer 一次性处理所有 token── Esta estrutura 注 改变了 2017 后深度学习中的每条扩展曲线──

> **【中文解读】**RNN tem três problemas fatais: não consegue colaborar, a longitude desaparece, a longitude fixa é uma grande quantidade de problemas.

**Type:** Learn | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizagem

- Compreender as três fraquezas fatais das redes neurais recorrentes (RNN)
  Compreender os três pontos fracos do ciclo
- Explicar por que a profundidade serial, e não o número de operações, determina o tempo de treinamento da GPU
   Explicar por que seria a profundidade (e não o número de operações) que determinou o tempo de treinamento da GPU
- Compare RNN vs Transformer complexidade em tarefas de modelagem de sequência
  Comparar RNN com Transformer na complexidade de tarefas de construção de sequências
- Identificar cenários em que ainda se possam preferir RNNs ou modelos do espaço-estado
  识别 RNN 或状态空间模型仍然更优场景
- Reconhecer a mudança de viés indutivo da localidade para a atenção global
  認識局部性から全局注意力归纳偏好への移行 認識局部性から全局注意力への归纳偏好への移行 認識

## O problema é o problema da introdução

Antes de 2017, cada modelo de sequência de última geração no planeta  língua, tradução, fala  era uma rede neural recorrente. LSTMs e GRUs ganharam benchmarks de tradução equivalentes à ImageNet por meio década. Eles eram a única ferramenta que alguém tinha.

> Até 2017, cada modelo de sequência mais avançado do mundo  linguação, tradução, voz  são redes circulantes de neurônios. LsTM e GRU são chamados de cinco anos em comparação com o teste de tradução de nível ImageNet.

Os cálculos sequenciais significavam que não se podia paralelalizar ao longo do eixo do tempo:`t+1`Precisa do estado oculto do token .`t`Uma sequência de 1.024 tokens significava 1.024 passos em série em uma GPU que pode fazer 1.000.000 de operações de pontos flutuantes por ciclo.

> Eles têm três pontos fracos fatais.`t+1`需要来自代币 `t`O estado oculto. Uma sequência de 1.024 tokens significa que a GPU de 1.000.000 vezes de operação de floating point pode ser executada em cada ciclo, para executar 1.024 passos em cadeia. Em hardware projetado para paralelismo, o tempo de treinamento aumenta com o longo e linear do ciclo.

> **【中文解读】**Primeiro ponto fraco fatal: 串行计算──RNN 必须顺序处理每个代币,完全无法利用GPU 的并行计算能力──训练时间与序列长度线性增长,这在GPU 时代是巨大的浪费──

Os gradientes desaparecidos significaram que a informação 50 tokens atrás já estava comprimida através de 50 não-lineares. Unidades recorrentes de gate (LSTM, GRU) suavizaram a esmagamento, mas nunca o eliminaram. Dependências de longo alcance  "o livro que li no verão passado em um avião para Quioto foi..."  rotineiramente falhou.

> 梯度消失 significa 50 tokens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> **【中文解读】**Segundo ponto fraco fatal: desaparecimento do nível. Após 50 camadas de mudanças não-lineares, a informação está quase completamente perdida.

Os estados ocultos de largura fixa significavam que o codificador apertou toda a sequência de fonte em um único vetor antes que o decodificador visse qualquer coisa. Não importa se a fonte é de 5 tokens ou 500; o gargalo de engarrafamento é a mesma forma.

> O estado oculto de largura fixa significa que o codificador antes de ver qualquer conteúdo no decodificador, comprimirá toda a sequência de origem em um veículo.

> **【中文解读】**O terceiro ponto fraco fatal: o botelho de largura fixa. O programador deve comprimir toda a sequência de origem para um volume de comprimento fixo.

O artigo de 2017 "Attenção é tudo que você precisa" propôs algo radical: deixar cair a recorrência inteiramente. Deixe cada posição atender a todas as outras posições em paralelo. Treine em uma grande multiplicação de matriz em vez de 1.024 sequenciais.

> O artigo de 2017 "Attenção é tudo que você precisa" propôs um esquema impulsionado: abandonar completamente o ciclo.

O resultado domina todas as modalidades até 2026. Língua (GPT-5, Claude 4, Llama 4), visão (ViT, DINOv2, SAM 3), áudio (Whisper), biologia (AlphaFold 3), robótica (RT-2).

> Até 2026, seus resultados dominaram cada tipo de modél­ação.

## O conceito central.

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**Um RNN computa `h_t = f(h_{t-1}, x_t)`Cada passo depende do anterior.`h_5`Antes de`h_4`Em GPUs modernas com mais de 10.000 núcleos paralelos, isso desperdiça 99% do silício numa longa sequência.

> **循环即瓶颈。**RNN 计算 `h_t = f(h_{t-1}, x_t)`Cada passo depende do primeiro.`h_4`之前计算 `h_5`❖ Com mais de 10.000 GPUs modernos em linha central, isso desperdiçou 99% da capacidade de cálculo de chips.

> **【中文解读】**O ciclo é a essência da botelha: cada passo do tempo de cálculo depende dos resultados do passo anterior. O GPU é bom em milhares de operações em conjunto, enquanto a linha de RNN depende de que só possa ser usada para uma pequena parte do cálculo do GPU. O transformador, através do seu próprio esforço, irá processar a sequência de O(N) a profundidade da linha de O(1), liberando completamente a capacidade de execução da GPU.

**Attention as a broadcast.**Computações de auto-atenção .`output_i = sum_j(a_ij * v_j)`Para cada par .`(i, j)`A matriz de atenção N×N completa um matmul em lote.

> **注意力即广播。**Autotestão simultânea para cada um`(i, j)`计算 `output_i = sum_j(a_ij * v_j)`◊ Toda a N×N Attention矩阵在一次批量矩阵乘法中填满──没有步骤相互依赖──GPU 喜欢它──

**The speedup is not a constant.**É a diferença entre `O(N)`profundidade serial e `O(1)`Na prática, os transformadores treinam 510x mais rápido por época em hardware correspondente em N=512, e a lacuna se amplia com o comprimento da sequência até atingir o `O(N²)`parede de memória da atenção (que a Flash Attention mais tarde fixou  ver lição 12).

> **加速不是常数。**É isso.`O(N)`串行深度与 `O(1)`串行深度之间的区别──在实践中,在匹配硬件上 N=512 时,Transformer Cada época de treinamento velocidade rápida 5-10 vezes, e a diferença aumenta com a duração da série, até você encontrar a atenção `O(N²)`内存墙(Flash Attention 后来修复了它见第 12 课) ⋅

**What transformers cost.**Escalas de memória da atenção como `O(N²)`Para o contexto de 2K, bem. Para o contexto de 128K, você precisa de janelas deslizantes, extrapolação de RoPE, azulejos de atenção flash, ou variantes de atenção linear.`O(N)`transformadores trocam tempo por memória e depois ganham o tempo de volta através do paralelismo.

> **Transformer 的代价。**Atenção à memória`O(N²)`增长──对2K上下文,没问题──对128K上下文,你需要滑窗,RoPE外推,Flash Attention 分块计算或线性注意力变体──循环在时间和内存都是`O(N)`Transformador com memória muda de tempo, depois passa por um processo de ganhar de volta o tempo.

**The inductive bias shift.**Os transformadores assumem localidade e recência. Os transformadores não assumem nada. Cada par é um candidato à atenção. É por isso que os transformadores precisam de mais dados para treinar bem, mas escalar mais quando tiverem. Chinchilla (2022) formalizou isso: dado tokens suficientes, um transformador sempre bate um RNN de igual número de parâmetros.

> **归纳偏好的转变。**RNN 假设局部性和邻近性──Transformer não faz nenhuma hipótese Cada par é um candidato à atenção── é por isso que Transformer 需要更多数据来训练好, mas uma vez que tiver dados suficientes, será capaz de se expandir ainda mais──Chinchilla(2022) formalizou este ponto: dado token suficiente, Transformer 总是击败 RNN de parâmetros iguais──

> **【中文解读】**O transmissão de preferências de regeneração é a chave do sucesso do transformador. O RNN 隐式假设"近处的符号更重要", enquanto o Transformer não faz qualquer hipótese  entre quaisquer duas posições pode ser estabelecida uma ligação direta.

> **【拓展：Chinchilla 缩放定律】**O DeepMind's Chinchilla Essay (em 2022) demonstra que a proporção de modelos e de dados de treinamento deve aumentar. Isso explica por que os modelos Llama, GPT-4 e outros precisam de dados de treinamento de milhões de tokens.

## Construí-lo e realizei-o.
```figure
rnn-vs-parallel
```

## Construí-lo

Não há rede neural aqui Simula-se o gargalo do núcleo numéricamente para que você sinta a lacuna no seu laptop.

> Não há rede neural. Usamos um número de valores para fazer a diferença no computador.

> **【中文解读】**Esta seção é feita com um modelo numérico puro para que você perceba a diferença de desempenho entre a linha e a linha. O principal problema é que a profundidade da cadeia é N, enquanto a profundidade da linha é apenas O (x) ou O (x) N.

### Passo 1: Medir a profundidade serial.

Veja .`code/main.py`- Construímos duas funções. Uma codifica uma sequência como uma cadeia de adições (serial, como um RNN).

> 参见 `code/main.py`△ Nós construímos duas funções── uma seria seria codificada para a cadeia de adição(串行, similar RNN)── uma seria codificada para a并行归约(广播, similar attention力)── a mesma matemática, diferentes dependências图──

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

Nós cronometramos ambos em sequências até 100.000 elementos. A versão RNN é O(N) e um único pipeline de CPU. Mesmo em Python puro, a redução de estilo de atenção bate-o em comprimento ≥ 1.000 porque Python `sum()`é implementado em C e reitera sem custos superiores de intérprete por passo.

> Nós temos que fazer a contagem de uma sequência de até 100.000 elementos. A versão RNN é uma única CPU de O(N) 流水线. Mesmo em Python puro, o estilo de atenção 归约在长度 ≥ 1,000 时也能胜出, pois Python `sum()`É um processo de implementação, sem explicação.

### Passo 2: Conte Operações Teóricas . 步骤 2: calcular operações teóricas

Os dois algoritmos adicionam N. A diferença é * profundidade de dependência *: quantas operações devem acontecer sequencialmente antes que a próxima possa começar. RNN profundidade = N. profundidade de atenção = log(N) com uma redução de árvore, ou 1 com uma varredura paralela. profundidade, não op contagem, decide o tempo da GPU.

> 两种算法都做N 次加法――区别在* depending on depth*:在下一个操作开始之前,必须顺序执行多少操作――RNN深度 = N。注意力深度 = 用树形归约时为 log(N), 用并行扫描时为 1――决定 GPU 时间是深度,而不是操作数――

### Passo 3: Escalação empírica em sequências longas.

Imprimimos uma tabela de cronometragem que torna a lacuna O ((N) visível. Em um laptop Mac 2026, as sequências abaixo de 1.000 elementos são muito rápidas para medir. Sequências de 100.000 mostram uma varredura linear limpa. Escale isso para um transformador de 16.384 tokens com um equivalente LSTM de 12 camadas e você vê por que o treinamento de relógio de parede foi um bloqueador em 2016.

> Nós imprimimos um cronograma de tempo que faz O(N) diferença visível. Em 2026 Mac  notebook, a sequência de menos de 1.000 elementos é muito rápida e incomensurável.

## Use-o com o framework implementado.

Quando ainda escolher um RNN em 2026:

> 2026 年何时仍应选择 RNN:

> **【中文解读】**Embora o Transformer tenha vencido na maioria dos cenários, mas não foi capaz de fazer isso.

> **【拓展：Mamba 与状态空间模型】**Mamba(2023) através de um mecanismo de seleção de esborradura realizou a construção de sequências de complexidade O(N), ao mesmo tempo que suporta o treinamento de paralelos.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

Modelos de espaço-estado (SSM) como Mamba são essencialmente RNNs com parametrização estruturada que lhes dá o melhor de ambos: `O(N)`A maioria dos laboratórios de fronteira treina modelos híbridos de transformadores SSM+ (por exemplo, Jamba, Samba)  recorrência não está morta, é um componente.

> 状态空间模型 (SSM) como Mamba é, em sua essência, um RNN estruturado e parametrizado, e possui vantagens em ambos:`O(N)`扫描内存, através de seleção de扫描实现并行训练――它们恢复了变体器 90% 的质量,同时具有更好的长上下文扩展性――2026 绝大多数前沿实验室训练混合SSM+Transformer 模型(如Jamba、Samba) 循环没有灭亡,它是一个组件――

## Envia-o . Produto .

Veja .`outputs/skill-architecture-picker.md`A competência escolhe uma arquitetura para um novo problema de sequência dada a comprimento, o rendimento e as restrições orçamentais de treinamento.

> 参见 `outputs/skill-architecture-picker.md` Esta habilidade é utilizada para a nova sequência de problemas de seleção de arquitetura, dado o comprimento, a capacidade e o orçamento de treinamento.

> **【拓展：架构选择决策树】**No projeto real, a seleção de arquiteturas precisa considerar várias dimensões: a duração da sequência, a demora requerida, o orçamento de memória, a quantidade de dados treinados, a implantação de hardware. Para a maioria das tarefas de PNL, o Transformer de apenas Decoder é uma escolha padrão. Para a sequência de ultra-longo, considerar Mamba ou a estrutura misturada; para a implantação de bordas, RNN/SSM quantificados podem ser mais adequados.

## Exercícios.

1. **Easy / 简单。**- Toma .`rnn_style`de`code/main.py`E substituir o estado oculto escalar por um vector de comprimento-64 de estados ocultos.
   取 `code/main.py`Em meio`rnn_style`, será substituído pelo volume de estado oculto de longitud 64 pelo volume de estado oculto de longitud 64.

2. **Medium / 中等。**Implementar um prefixo paralelo-suma (Hillis-Steele scan) em Python puro. Verifique que produz a mesma saída numérica que uma varredura em série em comprimento 1024.
   Utilize pure Python  implementar并行前和(Hillis-Steele 扫描) 验证它在长度 1024 上产生与串行扫描相同数值输出──计算深度──

3. **Hard / 困难。**Portar a redução de estilo de atenção para PyTorch na GPU. Tempo tanto como você varrer o comprimento da sequência de 64 para 65.536.
   O processo de transmissão de uma torcida de 64 bits para 65 536 bits para os dois sistemas de tempo.

## Termos-chave .

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Mais leitura 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762)O artigo que matou a recorrência na PNL convencional.
  Vaswani 等人(2017)  终结了主流NLP 中循环的论文──

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)- onde nasceu a atenção, ligada a um RNN.
  Bahdanau, Cho, Bengio(2014) Atenção nasceu onde,

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) o papel original do LSTM, para o registro.
  Hochreiter, Schmidhuber(1997)  原始 LSTM 论文,留作记录。

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) Resposta recorrente moderna aos transformadores.
  Gu, Dao(2023)  Transformer's moderno ciclo alternativo

> **【拓展："Attention Is All You Need" 的历史影响】**Vaswani  et al. 2017's paper not only solved RNN's parallelisation problem, it also provoked a one-fashion revolution── from BERT(2018) to GPT-4(2023), from ViT(2020) to AlphaFold 2(2021),Transformer architecture has become a basic module of modern AI── provou que "fraqueza de preferência de logística + big data + bigpower" pode ultrapassar a precisão de design de áreas específicas arquitetura──
