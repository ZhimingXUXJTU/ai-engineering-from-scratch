# Pre-treinamento de um Mini GPT (124M Parâmetros) 预训迷你 GPT(1,24 亿参数)

> O GPT-2 Small tem 124 milhões de parâmetros. São 12 camadas de transformador, 12 cabeças de atenção e embutidos 768-dimensional. Você pode treiná-lo de zero em uma única GPU em poucas horas. A maioria das pessoas nunca faz isso. Eles usam pontos de verificação pré-treinados. Mas se você não treinar um sozinho, você não entende realmente o que está acontecendo dentro do modelo em que está construindo produtos.

> **【中文解读】**GPT-2 Small tem 1,24 bilhão de parâmetros: 12 camadas Transformer  12 个注意力头、 768 维嵌入── single GPU 几小时即可从头训――理解预训是理解大模型的第一步──

> **【拓展：大模型三阶段】**O modelo de treinamento é o primeiro passo, o GPT-2 é o primeiro tipo de GPT.

> - Não .**【前置】**學本節前 請先掌握:(1) Fase 10·01-03(分词器、数据管线) 理解代币 ID 序列如何输入模型;(2) Transformer 架构(Fase 05) 自我注意、LayerNorm、FFN;(3) numpy 矩阵运算、反向传播手算(Fase 03 微积分与链式法则);(4) 交叉损失函数的梯度推导──本课**用 numpy 实现**Não dependa mais do PyTorch Autograd, para poder escrever sozinho.`backward()`- Não.

**Type:** Build
**Languages:** Python (with numpy)
**Prerequisites:** Phase 10, Lessons 01-03 (Tokenizers, Building a Tokenizer, Data Pipelines)
**Time:** ~120 minutes

## Objetivos de aprendizagem

- Implementar a arquitetura completa do GPT-2 (124M parâmetros) a partir do zero: embeddings de tokens, embeddings posicionais, blocos de transformadores e cabeçalho de modelo de linguagem
  Desde zero implementar completa GPT-2 架构(124M 参数):token 嵌入、位置嵌入、Transformer 块和语言模型头
- Treinar um modelo GPT em um corpus de texto usando previsão de tokens próximos com perda de entropia cruzada
  Use下一代币 预测和交叉损失在文本语料上训练 GPT 模型
- Implementar a geração de texto autoregressiva com amostragem de temperatura e filtragem top-k/top-p
  实现带温度采样和 top-k/top-p 过的自归文本生成
- Monitorar as curvas de perda de formação e validar que o modelo aprenda padrões de linguagem coerentes
   Monitoring training loss curve, verificação modelo aprendizado de modo de linguagem

> **【中文解读】**Este curso usa um numpy puro desde zero para implementar GPT-2 Small(124M 参数) ⋅ Você vai ver como 1.24 bilhões de parâmetros passam por um ciclo de treinamento de transferência de peso para prever o próximo token ⋅ Isto não é PyTorch 黑盒 Cada rectangular multiplicado é visível ⋅

## O problema é o problema da introdução

Você sabe o que é um transformador, já leu os diagramas, pode recitar "atentação é tudo o que você precisa" e desenhar caixas rotuladas "Atentação de várias cabeças" em um quadro branco.

> Você sabe o que é um transformador. Você já viu o gráfico. Você pode recitar "Atentão é tudo que você precisa" e desenhar um quadro com um sinal de "Atentão Multi-Capa".

Nada disso significa que entenda o que acontece quando um modelo gera texto.

> Isso não significa que você entenda o que aconteceu quando o modelo gerou o texto.

Existem 124.438.272 parâmetros no GPT-2 Small (com ligação de peso). Cada um deles foi definido executando um ciclo de treinamento: passagem avançada, perda de cálculo, passagem para trás, pesos de atualização. Doze blocos de transformador. Doze cabeças de atenção por quarteirão. Um espaço de inserção em 768 dimensões. Um vocabulário de 50.257 tokens. Toda vez que o modelo gera um token, todos os 124 milhões de parâmetros participam de uma única cadeia de multiplicação de matriz que toma uma sequência de IDs de token e produz uma distribuição de probabilidade sobre o próximo token.

> GPT-2 Small tem 124.438.272 个参数 (incluindo peso compartido) ⋅ cada parâmetro é definido através de um ciclo de treinamento: 转向传播、计算损失、反向传播、更新权重── 12 blocos de transformador, cada bloco 12 个注意力头,768 维嵌入空间,50,257 词表── por cada geração de token, todos os 1.24 bilhões de parâmetros participam de uma linha de quadrado de矩阵, transformando o token ID 序列 em um próximo token 概率分布──

Se nunca construíram isto, estão a trabalhar com uma caixa negra. Podem usar a API. Podem ajustar. Mas quando algo vai mal - quando o modelo alucina, quando se repete, quando se recusa a seguir instruções - não têm modelo mental para "porquê".

> Se você nunca construiu esse modelo pessoalmente, você está usando uma caixa negra. Você pode ajustar a API, pode modificar. Mas quando o modelo se torna ilusório, repete-se ou se recusa a seguir instruções, você não sabe por quê.

Esta lição construiu GPT-2 Small a partir do zero. Não em PyTorch. Em numpy. Cada multiplicação de matriz é visível. Cada gradiente é calculado pelo seu código. Você verá exatamente como 124 milhões de números conspiram para prever a próxima palavra.

> Este curso é feito de zero construção GPT-2 Small── não é necessário PyTorch── com numpy── cada matrição multiplicada é visível── cada gradiente é calculado pelo seu código── você verá 1.24 bilhões de números como eles colaboram.

> Este curso é feito de zero construção GPT-2 Small── não é necessário PyTorch── com numpy── cada matrição multiplicada é visível── cada gradiente é calculado pelo seu código── você verá 1.24 bilhões de números como eles colaboram.

## O conceito central.

### A Arquitetura GPT

Aqui está o gráfico completo de cálculo de tokens IDs para probabilidades de tokens próximos:

> Aqui está o gráfico completo da probabilidade do token ID para o token seguinte:

1. Identificadores de tokens entram. Forma: (batch_size, seq_len).
2. Identificação de identificação de um vector de 768 dimensões.
3. Cada posição (0, 1, 2, ...) faz um mapa de um vetor de 768 dimensões.
4. Adicionar embeddings de tokens + posições de embebimento.
5. Passe por 12 blocos de transformadores.
6. Normalização da camada final.
7. Projeção linear para tamanho do vocabulário.
8. Softmax para obter probabilidades.

Não há convulsões, não há recorrência, apenas embalagens, atenção, redes de feedforward e normas de camadas empilhadas 12 vezes.

> É o modelo inteiro. Não há envolvimento. Não há ciclo. Apenas inserção.

> - Não .**【类比】**GPT 像一台"流水线打字机": papel带送进代币 ID → 印章 1(tōken embebedding)盖出 768 维向量 → 印章 2(position embebedding) 叠加位置 → 12 道工人(Transformer block) Layerwise Modify this向量 → 末端喷墨头(LM head) 喷概率 on 50257个候选词 → 选择最高概率的词输出 → 把新词同时再送回纸带开头,循环──一切秘都在那12道工人如何"修改"量量而自我注意力就是工人只用12眼眼注意力) 的看序列里其他代币能力──

```mermaid
graph TD
    A["Token IDs\n(batch, seq_len)"] --> B["Token Embeddings\n(batch, seq_len, 768)"]
    A --> C["Position Embeddings\n(batch, seq_len, 768)"]
    B --> D["Add"]
    C --> D
    D --> E["Transformer Block 1"]
    E --> F["Transformer Block 2"]
    F --> G["..."]
    G --> H["Transformer Block 12"]
    H --> I["Layer Norm"]
    I --> J["Linear Head\n(768 -> 50257)"]
    J --> K["Softmax\nNext-token probabilities"]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#0f3460,color:#fff
    style C fill:#1a1a2e,stroke:#0f3460,color:#fff
    style D fill:#1a1a2e,stroke:#16213e,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
    style H fill:#1a1a2e,stroke:#e94560,color:#fff
    style I fill:#1a1a2e,stroke:#16213e,color:#fff
    style J fill:#1a1a2e,stroke:#0f3460,color:#fff
    style K fill:#1a1a2e,stroke:#51cf66,color:#fff
```

### O bloco de transformador

Cada um dos 12 blocos segue o mesmo padrão. Arquitetura pré-norma (GPT-2 usa pré-norma, não pós-norma como o transformador original):

> Cada um dos 12 blocos segue o mesmo modelo.

1. LayerNorm
2. Atenção à própria vida
3. Conexão residual (agrega entrada de volta)
4. LayerNorm
5. Rede de transferência de dados (MLP)
6. Conexão residual (agrega entrada de volta)

As conexões residuais são críticas. Sem elas, os gradientes desaparecem quando atingem o bloco 1 durante a propagação de volta. Com eles, os gradientes podem fluir diretamente da perda para qualquer camada através do caminho "salto". É por isso que você pode apilar 12, 32 ou até mesmo 96 blocos (GPT-4 é rumorado para usar 120).

> A diferença de ligação é fundamental. Sem elas, a gradiência em contra-direção se espalha até o primeiro bloco, quando desaparece.

> **【中文解读】**GPT 架构的核心是变体器块的堆积──每个块包含:LayerNorm → 多头自注意力 →残差连接 → LayerNorm → 前网络(MLP)→残差连接──GPT-2 使用 pre-norm(先归归化再注意力),而非原始变体块的后-norm──残差连接是关键没有它,梯度在12层反向传播后会消失,无法训练深层网络──

> **【拓展：GPT 系列的架构演进】**GPT-2 Pequeno(124M, 12 Layer 768 维)→ GPT-2 Médio(355M, 24 Layer 1024 维)→ GPT-2 Grande(774M, 36 Layer 1280 维)→ GPT-2 XL(1.5B,48 Layer 1600 维)→ GPT-3(175B, 96 Layer 12288 维)─Arquitetura básica é a mesma, apenas as camadas e dimensões estão em constante expansão―Os parâmetros específicos do GPT-4 não estão abertos, mas a sugestão usou cerca de 120 camadas e MoE(especialistas mistos) Arquitetura―

### Atenção: Mecanismo central

A auto-atenção permite que cada token olhe para cada token anterior e decida quanto atender a cada um.

> Desde que o seu atenção para cada token  ver cada token anterior,并 decidir quanto atenção para cada token  dar.

Para cada posição de token, calcular três vetores a partir da entrada:
- **Query (Q)**"O que estou à procura?"
  Tradução:**查询（Q）**"Eu estou a procurar o quê?"
- **Key (K)**"O que contém?"
  Tradução:**键（K）**"Eu contendo o quê?"
- **Value (V)**"Que informação tenho?"
  Tradução:**值（V）**"O que é que eu tenho consigo?"

```
Q = input @ W_q    (768 -> 768)
K = input @ W_k    (768 -> 768)
V = input @ W_v    (768 -> 768)

attention_scores = Q @ K^T / sqrt(d_k)
attention_scores = mask(attention_scores)   # causal mask: -inf for future positions
attention_weights = softmax(attention_scores)
output = attention_weights @ V
```

A máscara causal é o que torna o GPT autoregressivo. A posição 5 pode atender às posições 0-5 mas não 6, 7, 8, etc. Isso impede que o modelo "tropece" olhando para futuros tokens durante o treinamento.

> O efeito masquerado faz com que o GPT se torne um modelo de auto-regressão. A posição 5 pode ser observada na posição 0-5, mas não pode ser observada na posição 6、7、8 etc. Isto impede que o modelo em treino passe por um token futuro para "falta".

**Multi-head attention**O espaço 768-dimensional divide-o em 12 cabeças de 64 dimensões cada uma. Cada cabeça aprende um padrão de atenção diferente. Uma cabeça pode rastrear relações sintáticas (acordo entre sujeito e verbo). Outra pode rastrear semântica semelhança (sinônimos). Outra pode rastrear proximidade posicional (palavras próximas). As saídas de todas as 12 cabeças são concatenadas e projetadas de volta para 768 dimensões.

> **多头注意力**Para classificar o 768 维空间, divide-se em 12 维的头―― cada cabeça aprende diferentes modos de atenção―― um cabeçalho pode rastrear o seu significado de significado.

```mermaid
graph LR
    subgraph MultiHead["Multi-Head Attention (12 heads)"]
        direction TB
        I["Input (768)"] --> S1["Split into 12 heads"]
        S1 --> H1["Head 1\n(64 dims)"]
        S1 --> H2["Head 2\n(64 dims)"]
        S1 --> H3["..."]
        S1 --> H12["Head 12\n(64 dims)"]
        H1 --> C["Concat (768)"]
        H2 --> C
        H3 --> C
        H12 --> C
        C --> O["Output Projection\n(768 -> 768)"]
    end

    subgraph SingleHead["Each Head Computes"]
        direction TB
        Q["Q = X @ W_q"] --> A["scores = Q @ K^T / 8"]
        K["K = X @ W_k"] --> A
        A --> M["Apply causal mask"]
        M --> SM["Softmax"]
        SM --> MUL["weights @ V"]
        V["V = X @ W_v"] --> MUL
    end

    style I fill:#1a1a2e,stroke:#e94560,color:#fff
    style O fill:#1a1a2e,stroke:#e94560,color:#fff
    style Q fill:#1a1a2e,stroke:#0f3460,color:#fff
    style K fill:#1a1a2e,stroke:#0f3460,color:#fff
    style V fill:#1a1a2e,stroke:#0f3460,color:#fff
```

A divisão por sqrt(d_k) -- sqrt(64) = 8 -- é escalar. Sem ele, os produtos de pontos crescem para vetores de alta dimensão, empurrando softmax para regiões onde os gradientes são quase zero. Esta foi uma das principais ideias no artigo original "Attenção é tudo que você precisa".

> Além de em quadrado, = 64) = 8 é encolhido. Sem ele, o ponto de acumulação em alta dimensão em volume vai se tornar muito grande, vai levar softmax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### KV Cache: Por que a inferência é rápida

Durante o treinamento, você processa toda a seqüência de uma só vez. Durante a inferência, você gera um token de cada vez. Sem otimização, gerar token N requer recomputar atenção para todos os tokens anteriores N-1. Isso é O(N^2) por token gerado, ou O(N^3) total para uma sequência de comprimento N.

> 訓練時,你一次處理整列──推理時,你個個生成トークン──無優化詞,生成トークン N 需要为所有N-1 个前代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代

O KV Cache resolve isto. Depois de calcular K e V para cada token, armazená-los. Ao gerar token N + 1, você só precisa calcular Q para o novo token e procurar o caché K e V de todos os tokens anteriores. Isto reduz o custo por token de O(N) para O(1) para o cálculo K e V. O cálculo da pontuação de atenção ainda é O ((N) porque você atende todas as posições anteriores, mas evita multiplicidades redundantes de matriz na entrada.

> KV 缓存 resolveram o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá o problema. KV 缓存 resolverá. KV 缓存 resolverá. KV 缓存 resolverá. KV 缓存 resolverá. KV 缓存 resolverá. KV 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓 缓 缓存 缓 缓 缓存 缓 缓 缓 缓

Para GPT-2 com 12 camadas e 12 cabeças, o cache KV armazena 2 (K + V) x 12 camadas x 12 cabeças x 64 dims = 18.432 valores por token. Para uma sequência de 1024 tokens, que é cerca de 75 MB em FP32. Para Llama 3 405B com 128 camadas, o cache KV para uma única sequência pode exceder 10 GB. É por isso que a inferência de contexto longo é limitada à memória.

> 对于12层12头的GPT-2,KV 缓存每 token 存储 2(K + V) x 12层 x 12头 x 64维 = 18,432 个值。对于1024 token 的序列,在FP32中约为75MB──对于128层的Llama 3 405B,单序列的KV 缓存可超过10GB──这就是为什么长上下文推理是内存受限的──

### Preenchimento vs Decodificação: duas fases de inferência

Quando enviamos um pedido para um LLM, a inferência acontece em duas fases distintas.

> Quando você enviar um pedido para o LLM, a conclusão ocorre em duas fases diferentes.

**Prefill**processar todo o seu prompt em paralelo. Todos os tokens são conhecidos, para que o modelo possa calcular a atenção para todas as posições simultaneamente. Esta fase é computacional - a GPU está fazendo multiplicidades de matriz em total throughput. Para um prompt de 1000 tokens em um A100, prefill leva cerca de 20-50ms.

> **预填充（Prefill）**Elaboração de todo o prompt. Todos os tokens são conhecidos, então o modelo pode calcular simultaneamente a atenção de todas as posições. Esta fase é de um tipo de GPU com alta densidade de cálculo.

**Decode**gera tokens um a cada vez. Cada novo token depende de todos os tokens anteriores. Esta fase é limitada à memória - o gargalo de engarrafamento é a leitura dos pesos do modelo e do cache KV da memória da GPU, não da própria matemática da matriz. Os núcleos de computação da GPU ficam em grande parte inactivos à espera de leituras de memória. Para o GPT-2, cada passo de decodificação leva aproximadamente o mesmo tempo, independentemente do número de FLOPs que as matmulas exigem, porque a largura de banda de memória é a restrição.

> **解码（Decode）**个别生成代币――每个新代币依赖所有之前代币――这个阶段是访问存储密集型的瓶是从 GPU 内存读取模型权重和KV缓存,而不是矩阵运算本身――GPU的计算核心大部分时间在等待内存读取――对于GPT-2, cada fase de decodificação,时间大致相同,无论矩阵乘法需要多少FLOP,因为内存宽度是限制的――

Esta distinção é importante para os sistemas de produção. Preencha as escalas de tráfego com computação GPU (mais FLOPS = preenchaço mais rápido). Decode as escalas de tráfego com largura de banda de memória (memória mais rápida = decodificação mais rápida). É por isso que o H100 da NVIDIA se focou em melhorias na largura de banda de memória em relação ao A100 - ele acelera diretamente a geração de tokens.

> Esta diferença é importante para o sistema de produção. A H100 da NVIDIA se concentra na melhoria da capacidade de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenamento de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de armazenado de

```mermaid
graph LR
    subgraph Prefill["Phase 1: Prefill"]
        direction TB
        P1["Full prompt\n(all tokens known)"]
        P2["Parallel computation\n(compute-bound)"]
        P3["Builds KV Cache"]
        P1 --> P2 --> P3
    end

    subgraph Decode["Phase 2: Decode"]
        direction TB
        D1["Generate token N"]
        D2["Read KV Cache\n(memory-bound)"]
        D3["Append to KV Cache"]
        D4["Generate token N+1"]
        D1 --> D2 --> D3 --> D4
        D4 -.->|repeat| D1
    end

    Prefill --> Decode

    style P1 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style P2 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style P3 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style D1 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D2 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D3 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D4 fill:#1a1a2e,stroke:#e94560,color:#fff
```

### O ciclo de treinamento

O treinamento de um LLM é a previsão de tokens próximos. Dados tokens [0, 1, 2, ..., N-1], previsão de tokens [1, 2, 3, ..., N. A função de perda é entropia cruzada entre a distribuição de probabilidade prevista do modelo e o token seguinte real.

> 訓練 LLM 就是下一代币 预测──给定代币 [0, 1, 2, ..., N-1],预测代币 [1, 2, 3, ..., N]──损失函数是模型预测的概率分布与实际下一代币 之间交叉──

Um passo de formação:

> Um treino:

1. **Forward pass**Realizando o lote através dos 12 blocos, obtém logits (scores pré-softmax) para cada posição.
2. **Compute loss**: Entropia cruzada entre logits e tokens-alvo (a entrada mudada por uma posição).
3. **Backward pass**: Calcular gradientes para todos os parâmetros 124M utilizando a propagação de volta.
4. **Optimizer step**O GPT-2 usa o Adam para aquecer a taxa de aprendizagem e a decadência cosina.

O horário de aprendizagem é mais importante do que você poderia esperar. GPT-2 aquece de 0 para o pico de aprendizagem durante os primeiros 2.000 passos, depois decadem seguindo uma curva cosínea. Começando com uma alta taxa de aprendizagem faz com que o modelo diverja. Manter uma taxa constante de alta causa oscilação no treinamento posterior. O padrão de aquecimento-depois-decaimento é usado por todos os principais LLM.

> A taxa de aprendizagem é mais importante do que você imagina. GPT-2 em 2000 passos de 0 预热到峰值学习率, em seguida, em relação à curva de restringimento.

### GPT-2 Pequeno: Os números

| Component | Shape | Parameters |
|-----------|-------|------------|
| Token embeddings | (50257, 768) | 38,597,376 |
| Position embeddings | (1024, 768) | 786,432 |
| Per-block attention (W_q, W_k, W_v, W_out) | 4 x (768, 768) | 2,359,296 |
| Per-block FFN (up + down) | (768, 3072) + (3072, 768) | 4,718,592 |
| Per-block LayerNorms (2x) | 2 x 768 x 2 | 3,072 |
| Final LayerNorm | 768 x 2 | 1,536 |
| **Total per block** | | **7,080,960** |
| **Total (12 blocks)** | | **85,054,464 + 39,383,808 = 124,438,272** |

A projeção de saída (cabeça de logits) compartilha pesos com a matriz de incorporação de token. Isso é chamado de ligação de peso - reduz a contagem de parâmetros em 38M e melhora o desempenho porque obriga o modelo a usar o mesmo espaço de representação para entrada e saída.

> **【中文解读】**GPT-2 参数分布:token 嵌入层占 38.6M(50257 x 768),12 个变压器块各占 7.1M,最终 LayerNorm 只有 1.5K;;权重共享(权重绑定) 让输出投影层复用代币 嵌入矩阵,减少38M 参数的同时还提升性能因为输入和输出被强制使用相同表示空间──

## Construí-lo e realizei-o.

### Passo 1: Introdução de camada

Embedings de tokens mapeam cada um dos 50.257 tokens possíveis para um vetor de 768 dimensões. Embedings de posição adicionam informações sobre onde cada token fica na sequência. Os dois são somados.

> Token 嵌入将 50,257 个可能的 token 各映射到一个768 维向量――位置嵌入 嵌入 添加每个 token 在序列中位置的信息――两者相加――

```python
import numpy as np

class Embedding:
    def __init__(self, vocab_size, embed_dim, max_seq_len):
        self.token_embed = np.random.randn(vocab_size, embed_dim) * 0.02
        self.pos_embed = np.random.randn(max_seq_len, embed_dim) * 0.02

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        tok_emb = self.token_embed[token_ids]
        pos_emb = self.pos_embed[:seq_len]
        return tok_emb + pos_emb
```

O desvio padrão de 0,02 para inicialização vem do papel GPT-2. muito grande e os passes iniciais para a frente produzem valores extremos que desestabilizam o treinamento. muito pequeno e as saídas iniciais são quase idênticas para todas as entradas, tornando inúteis os sinais de gradiente iniciais.

> O nível de variação de padrões é de 0,02 ̊, que é o nível de variação de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padrões de padr

### Passo 2: Autoatenção com máscara causal

A máscara causal fixa posições futuras a infinito negativo antes do softmax, garantindo que cada posição só possa atender a si mesma e posições anteriores.

> Antes de fazer uma só atenção, mas em suavidade, antes de colocar uma posição negativa no futuro, assegure que cada posição só perceba a si mesma e a sua posição anterior.

```python
def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(0, -1, -2 if Q.ndim == 4 else 1) / np.sqrt(d_k)
    if mask is not None:
        scores = scores + mask
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights = weights / weights.sum(axis=-1, keepdims=True)
    return weights @ V
```

A implementação softmax subtrai o máximo antes de exponenciar. Sem isso, exp(large_number) supera em infinito. Este é um truque de estabilidade numérica que não altera a saída porque softmax(x - c) = softmax(x) para qualquer constante c.

> softmax 实现在取指数前减去最大值──没有这个,exp(large_number) 会溢出到无穷大──这是一个数值稳定性技巧,不改变输出,因为对任意常数 c,softmax(x - c) = softmax(x)──

### Passo 3: Atenção de várias cabeças

Divida a entrada 768-dimensional em 12 cabeças de 64 dimensões cada uma. Cada cabeça calcula a atenção de forma independente.

> Para fazer o cálculo, você deve dividir os 768 维输入 into 12 个 64 维的头――每个头独立计算注意力――拼接结果并投投回 768 维――

```python
class MultiHeadAttention:
    def __init__(self, embed_dim, num_heads):
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_out = np.random.randn(embed_dim, embed_dim) * 0.02

    def forward(self, x, mask=None):
        batch, seq_len, d = x.shape
        Q = (x @ self.W_q).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        K = (x @ self.W_k).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        V = (x @ self.W_v).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.head_dim)
        if mask is not None:
            scores = scores + mask
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights = weights / weights.sum(axis=-1, keepdims=True)
        attn_out = weights @ V

        attn_out = attn_out.transpose(0, 2, 1, 3).reshape(batch, seq_len, d)
        return attn_out @ self.W_out
```

A dança de remodelação-transposição-remodelação é a parte mais confusa da atenção multi-cabeça. Aqui está o que acontece: o tensor (batch, seq_len, 768) torna-se (batch, seq_len, 12, 64), então (batch, 12, seq_len, 64). Agora cada uma das 12 cabeças tem sua própria (seq_len, 64) matriz para dirigir a atenção. Depois da atenção, invertimos o processo: (batch, 12, seq_len, 64) torna-se (batch, seq_len, 12, 64) torna-se (batch, seq_len, 768).

> O processo é o mais confuso do que há de ser feito. O processo é como: ((batch, seq_len, 768) 张量变为 (batch, seq_len, 12, 64), depois (batch, 12, seq_len, 64) 现在 12个头各有自己的 (seq_len, 64) 矩阵来运行注意力――注意力后,我们反转过程: ((batch, 12, seq_len, 64) 变为 (batch, seq_len, 12, 64) 变为 (batch, seq_len, 768) 变为 (batch, seq_len, 12, 64) 变为 (batch, seq_len, 768) △

### Passo 4: Bloco de Transformador

Um bloco completo de transformador: LayerNorm, atenção multi-cabeça com resíduo, LayerNorm, feedforward com resíduo.

> Um transformador completo bloco:LayerNorm、带残差的多头注意力、LayerNorm、带残差的前网络──

```python
class LayerNorm:
    def __init__(self, dim, eps=1e-5):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps

    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta


class FeedForward:
    def __init__(self, embed_dim, ff_dim):
        self.W1 = np.random.randn(embed_dim, ff_dim) * 0.02
        self.b1 = np.zeros(ff_dim)
        self.W2 = np.random.randn(ff_dim, embed_dim) * 0.02
        self.b2 = np.zeros(embed_dim)

    def forward(self, x):
        h = x @ self.W1 + self.b1
        h = np.maximum(0, h)  # GELU approximation: ReLU for simplicity
        return h @ self.W2 + self.b2


class TransformerBlock:
    def __init__(self, embed_dim, num_heads, ff_dim):
        self.ln1 = LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads)
        self.ln2 = LayerNorm(embed_dim)
        self.ffn = FeedForward(embed_dim, ff_dim)

    def forward(self, x, mask=None):
        x = x + self.attn.forward(self.ln1.forward(x), mask)
        x = x + self.ffn.forward(self.ln2.forward(x))
        return x
```

A rede feedforward expande a entrada de 768 dimensões para 3.072 dimensões (4x), aplica uma não-linearidade, então projeta de volta para 768. Este padrão de expansão-contracção dá ao modelo uma representação interna "mais ampla" para trabalhar em cada posição. GPT-2 usa a ativação GELU, mas usamos ReLU aqui para simplicidade - a diferença é menor para entender a arquitetura.

> O modelo de expansão-reconstrução da rede é um modelo interno de "amplitude" que representa um trabalho em cada posição. GPT-2 usa a função GELU  ativação, mas aqui para simples uso de ReLU para a compreensão da estrutura é muito pequeno.

### Passo 5: Modelo GPT completo

Aponta 12 blocos de transformador. Adicione a camada de inserção na frente e a projeção de saída na parte de trás.

> 堆叠 12 变压器块──前面加嵌层,后面加输出投影──

```python
class MiniGPT:
    def __init__(self, vocab_size=50257, embed_dim=768, num_heads=12,
                 num_layers=12, max_seq_len=1024, ff_dim=3072):
        self.embedding = Embedding(vocab_size, embed_dim, max_seq_len)
        self.blocks = [
            TransformerBlock(embed_dim, num_heads, ff_dim)
            for _ in range(num_layers)
        ]
        self.ln_f = LayerNorm(embed_dim)
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)

        x = self.embedding.forward(token_ids)
        for block in self.blocks:
            x = block.forward(x, mask)
        x = self.ln_f.forward(x)

        logits = x @ self.embedding.token_embed.T
        return logits

    def count_parameters(self):
        total = 0
        total += self.embedding.token_embed.size
        total += self.embedding.pos_embed.size
        for block in self.blocks:
            total += block.attn.W_q.size + block.attn.W_k.size
            total += block.attn.W_v.size + block.attn.W_out.size
            total += block.ffn.W1.size + block.ffn.b1.size
            total += block.ffn.W2.size + block.ffn.b2.size
            total += block.ln1.gamma.size + block.ln1.beta.size
            total += block.ln2.gamma.size + block.ln2.beta.size
        total += self.ln_f.gamma.size + self.ln_f.beta.size
        return total
```

Observe a ligação de peso: `logits = x @ self.embedding.token_embed.T`A projeção de saída reutiliza a matriz de incorporação de tokens (transposto).

> Nota de participação:`logits = x @ self.embedding.token_embed.T` Output projeção de token de repetição 嵌入矩阵(转置) ・・・ Isso não é apenas uma técnica de economia de parâmetros── significa que o modelo usa o mesmo espaço de veículo para entender token (嵌入) e token de previsão (输出) ─

### Passo 6: Loop de treinamento

Para uma corrida de treinamento real em parâmetros 124M, você precisaria de uma GPU e PyTorch. Este loop de treinamento demonstra a mecânica em um pequeno modelo que funciona em pura numpy. Usamos um modelo pequeno (4 camadas, 4 cabeças, 128 dims) para torná-lo tratável.

> Para um verdadeiro treinamento de 124M, você precisa de GPU e PyTorch. Este ciclo de treinamento é feito em um pequeno modelo de funcionamento puro.

```python
def cross_entropy_loss(logits, targets):
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(-1, vocab_size)
    targets_flat = targets.reshape(-1)

    max_logits = logits_flat.max(axis=-1, keepdims=True)
    log_softmax = logits_flat - max_logits - np.log(
        np.exp(logits_flat - max_logits).sum(axis=-1, keepdims=True)
    )

    loss = -log_softmax[np.arange(len(targets_flat)), targets_flat].mean()
    return loss


def train_mini_gpt(text, vocab_size=256, embed_dim=128, num_heads=4,
                   num_layers=4, seq_len=64, num_steps=200, lr=3e-4):
    tokens = np.array(list(text.encode("utf-8")[:2048]))
    model = MiniGPT(
        vocab_size=vocab_size, embed_dim=embed_dim, num_heads=num_heads,
        num_layers=num_layers, max_seq_len=seq_len, ff_dim=embed_dim * 4
    )

    print(f"Model parameters: {model.count_parameters():,}")
    print(f"Training tokens: {len(tokens):,}")
    print(f"Config: {num_layers} layers, {num_heads} heads, {embed_dim} dims")
    print()

    for step in range(num_steps):
        start_idx = np.random.randint(0, max(1, len(tokens) - seq_len - 1))
        batch_tokens = tokens[start_idx:start_idx + seq_len + 1]

        input_ids = batch_tokens[:-1].reshape(1, -1)
        target_ids = batch_tokens[1:].reshape(1, -1)

        logits = model.forward(input_ids)
        loss = cross_entropy_loss(logits, target_ids)

        if step % 20 == 0:
            print(f"Step {step:4d} | Loss: {loss:.4f}")

    return model
```

A perda começa perto de ln(vocab_size) - para um vocabulário de nível de byte de 256 tokens, ou seja ln(256) = 5.55. Um modelo aleatório atribui probabilidade igual a cada token. À medida que o treinamento progride, a perda diminui porque o modelo aprende a prever padrões comuns: "th" após "t", espaço após um período, e assim por diante.

> 损失初始接近 ln(vocab_size) 对于 256 代币的字节级词表,即 ln(256) = 5.55。随机模型给每个代币 分配等概率──随着训练进行,损失下降,因为模型学会预测常见模式:"t" 后面是"th",句号后面是空格等──

Na produção, você usaria o optimizador Adam com acumulação de gradientes, aquecimento de taxa de aprendizagem e corte de gradientes. O loop de passagem para frente-perda-atendimento para trás é idêntico. O optimizador é mais sofisticado.

> Na produção, você usará o Adam  оптимизатор                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

### Passo 7: Geração de textos

A geração usa o modelo treinado para prever um token de cada vez. Cada previsão é amostrada a partir da distribuição de saída (ou tomada com ganância como o argmax).

> O modelo de um bom treinamento é um bom modelo de um bom modelo.

```python
def generate(model, prompt_tokens, max_new_tokens=100, temperature=0.8):
    tokens = list(prompt_tokens)
    seq_len = model.embedding.pos_embed.shape[0]

    for _ in range(max_new_tokens):
        context = np.array(tokens[-seq_len:]).reshape(1, -1)
        logits = model.forward(context)
        next_logits = logits[0, -1, :]

        next_logits = next_logits / temperature
        probs = np.exp(next_logits - next_logits.max())
        probs = probs / probs.sum()

        next_token = np.random.choice(len(probs), p=probs)
        tokens.append(next_token)

    return tokens
```

A temperatura controla a aleatoriedade. A temperatura 1.0 usa a distribuição bruta. A temperatura 0.5 agudiza-a (mais determinista - o modelo escolhe suas principais escolhas com mais frequência). A temperatura 1.5 aplania-a (mais aleatórias - tokens de baixa probabilidade têm uma maior chance). A temperatura 0.0 é codificação gananciosa (sempre escolha o token de maior probabilidade).

> 温度控制随机性──温度 1.0 使用原始分布──温度 0.5 使其更尖(更确定性模型更频繁地选择顶部候选)──温度 1.5 使其更平坦(更随机低概率代币 获得更大的机会)──温度 0.0 是贪心解码(始终选择最高概率代币)──

O `tokens[-seq_len:]`A janela é necessária porque o modelo tem um comprimento máximo de contexto (1024 para GPT-2). Uma vez que você excede isso, você deve soltar os tokens mais antigos. Esta é a "janela de contexto" que todos falam.

> `tokens[-seq_len:]`A janela é necessária, porque o modelo tem a maior down文長度 ((GPT-2 为 1024) ⋅ uma vez que ultrapassar, você deve abandonar o token mais antigo ⋅ é o que todos dizem sobre a janela.

## Use-o com o framework implementado.
```figure
sampling-decoder
```

## Usá-lo

### Formação e Demo de Geração

```python
corpus = """The transformer architecture has revolutionized natural language processing.
Attention mechanisms allow the model to focus on relevant parts of the input.
Self-attention computes relationships between all pairs of positions in a sequence.
Multi-head attention splits the representation into multiple subspaces.
Each attention head can learn different types of relationships.
The feedforward network provides nonlinear transformations at each position.
Residual connections enable gradient flow through deep networks.
Layer normalization stabilizes training by normalizing activations.
Position embeddings give the model information about token ordering.
The causal mask ensures autoregressive generation during training.
Pre-training on large text corpora teaches the model general language understanding.
Fine-tuning adapts the pre-trained model to specific downstream tasks."""

model = train_mini_gpt(corpus, num_steps=200)

prompt = list("The transformer".encode("utf-8"))
output_tokens = generate(model, prompt, max_new_tokens=100, temperature=0.8)
generated_text = bytes(output_tokens).decode("utf-8", errors="replace")
print(f"\nGenerated: {generated_text}")
```

Em um pequeno corpus com um modelo pequeno, o texto gerado será semicoerente na melhor das hipóteses. Aprenderá alguns padrões de nível de byte do texto de treinamento, mas não pode generalizar a forma como o GPT-2 faz com 40 GB de dados de treinamento e a arquitetura completa de parâmetros 124M. O ponto não é a qualidade da saída. O ponto é que você pode rastrear cada passo: inserção de busca, cálculo de atenção, transformação de feedforward, projeção logit, softmax e amostragem. Todas as operações são visíveis.

> Em pequenos materiais e pequenos modelos, o texto gerado é semi-consequente. Ele vai aprender de um texto de treinamento para um padrão de alguns caracteres, mas não pode ser generalizado como o GPT-2 em 40GB de dados de treinamento e uma estrutura de parâmetros 124M completa. A chave não é a qualidade de saída. A chave é que você possa acompanhar cada passo: inserção em busca de atenção, cálculo, mudança de lógica, projeção, max e amostra. Cada operação é visível.

## Envia-o . Produto .

Esta lição produz`outputs/prompt-gpt-architecture-analyzer.md`-- um prompt que analisa as opções de arquitetura em qualquer modelo de estilo GPT.

> 本课产 出 `outputs/prompt-gpt-architecture-analyzer.md` Uma análise arbitrária GPT 风格模型架构选择的提示──输入模型卡或技术报告, que irá descomplicar a distribuição de parâmetros、 atenção design e encolhimento de decisões──

## Exercícios.

1. Modifique o modelo para usar 24 camadas e 16 cabeças em vez de 12/12. Conte os parâmetros. Como duplicar a profundidade compara-se ao duplicar a largura (dimensão de incorporação)?

2. Implementar a função de ativação GELU (GELU(x) = x * 0.5 * (1 + erf(x / sqrt(2)))) e substituir o ReLU na rede de feedforward.

3. Adicione um cache KV à função de geração. Armazenar tensores K e V para cada camada após a primeira passagem para a frente, e reutilizar-os para tokens subsequentes. Medir a velocidade: gerar 200 tokens com e sem o cache e comparar o tempo do relógio de parede.

4. Implementar amostragem top-k (considere apenas os tokens de maior probabilidade k) e amostragem top-p (amostragem núcleo: considere o menor conjunto de tokens cuja probabilidade cumulativa exceda p). Compare a qualidade de saída a temperatura 0,8 com top-k=50 vs top-p=0,95.

5. Construir um traçado de curva de perda de treinamento. Treinar o modelo para 1000 passos e perda de gráfico vs passo. Identificar as três fases: descida inicial rápida (aprender bytes comuns), fase média mais lenta (aprender byte padrões), e planalto (overfitting no pequeno corpus). A forma desta curva é a mesma se você está treinando um modelo de 128 dimensões ou GPT-4.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Autoregressive | "It generates one word at a time" | Each output token is conditioned on all previous tokens -- the model predicts P(token_n \| token_0, ..., token_{n-1}) | 自回归，逐 token 生成，每个 token 依赖之前所有 token |
| Causal mask | "It can't see the future" | An upper-triangular matrix of -infinity values that prevents attention to future positions during training | 因果掩码，防止看到未来位置 |
| Multi-head attention | "Multiple attention patterns" | Splitting Q, K, V into parallel heads (e.g., 12 heads of 64 dims each for GPT-2) so each head can learn different relationship types | 多头注意力，并行学习不同关系类型 |
| KV Cache | "Caching for speed" | Storing computed Key and Value tensors from previous tokens to avoid redundant computation during autoregressive generation | KV 缓存，避免重复计算已生成 token 的 K/V |
| Prefill | "Processing the prompt" | The first inference phase where all prompt tokens are processed in parallel -- compute-bound on GPU FLOPS | 预填充阶段，并行处理 prompt，计算密集 |
| Decode | "Generating tokens" | The second inference phase where tokens are generated one at a time -- memory-bound on GPU bandwidth | 解码阶段，逐 token 生成，访存密集 |
| Weight tying | "Sharing embeddings" | Using the same matrix for input token embeddings and the output projection head -- saves 38M params in GPT-2 | 权重共享，输入输出共用嵌入矩阵 |
| Residual connection | "Skip connection" | Adding the input directly to the output of a sublayer (x + sublayer(x)) -- enables gradient flow in deep networks | 残差连接，使深层网络梯度流通 |
| Layer normalization | "Normalizing activations" | Normalizing across the feature dimension to mean 0 and variance 1, with learnable scale and bias parameters | 层归一化，特征维度归一化 |
| Cross-entropy loss | "How wrong the predictions are" | -log(probability assigned to the correct next token), averaged over all positions -- the standard LLM training objective | 交叉熵损失，LLM 训练的标准目标函数 |

## Mais leitura 延伸阅读

- [Radford et al., 2019 -- "Language Models are Unsupervised Multitask Learners" (GPT-2)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)-- o papel GPT-2 que introduziu a família de parâmetros 124M a 1.5B
- [Vaswani et al., 2017 -- "Attention Is All You Need"](https://arxiv.org/abs/1706.03762)- O papel transformador original com atenção escalada de produto ponto e atenção multi-cabeça
- [Llama 3 Technical Report](https://arxiv.org/abs/2407.21783)-- como Meta escalaram a arquitetura GPT para parâmetros 405B com GPUs 16K
- [Pope et al., 2022 -- "Efficiently Scaling Transformer Inference"](https://arxiv.org/abs/2211.05102)-- o papel que formalizou prefill vs decode e KV cache análise
