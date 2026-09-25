# Atenção Nativa de Esparcimento (Depseek NSA)

> Com 64k tokens, a atenção consome 70-80% da latência de decodificação. Todos os laboratórios abertos têm um plano para consertá-lo. A NSA do DeepSeek (melhor documento ACL 2025) é aquela que ficou preso: três ramos paralelas de atenção  tokens com grãos grosseiros comprimidos, tokens com grãos finos retidos seletivamente, e janelas deslizantes para contexto local  combinadas através de um portão aprendido. É alinhado com hardware (friendly-kernel), nativamente treinável (funciona em pré-treino, não ligado à inferência), e em 64k decodificações ele funciona mais rápido do que FlashAttention enquanto combina ou supera a qualidade de atenção total. Esta lição constrói os três ramos de ponta a ponta e mostra por que a esparsia é diferenciável de ponta a ponta.

> **【中文解读】**64K token 时注意力消耗 70-80%解码延迟──DeepSeek NSA(ACL 2025 最佳论文) Usar três条并行注意力分支解决: comprimir token gruas粒度、选择保留细粒度 token、滑窗局部上下文,通过可学习门控组合──硬件友好、可预训、比FlashAttention更快──

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K token) é a capacidade central do grande modelo de 2025-2026 anos;; NSA、MHA、GQA são um esquema de redução da complexidade de cálculo de atenção;; A inovação da DeepSeek é de raridade de extremo a extremo, pode ser usada diretamente na fase de treinamento preliminar;;

> - Não .**【前置】**學本節前 請先掌握:Fase 10·16 ((差分注意力);FlashAttention 概念;softmax 门控機──本節是注意力优化进阶──
> - Não .**【类比】**NSA = 看长文档的三种策略同时进行:**压缩分支**= 看目录摘要(粗粒度);(2) **选择分支**= 重点看自己感兴趣的章节 (重点看自己感兴趣的章节) ((细粒度) ((3) **滑动窗口**= 当前页前后 5 页仔细看(局部上下文) ・门控(gate) = decidir qual é a melhor combinação de estratégias para cada posição,

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Objetivos de aprendizagem

- Diga os três serviços de atenção da NSA e o que cada um capta.
  Explicação das três ramificações da NSA e suas respectivas captações de informações
- Explique por que a NSA é "naturalmente treinável" onde os métodos anteriores de atenção escassa eram apenas inferência.
  Explica por que a NSA é "praticamente treinável", enquanto os métodos anteriores de atenção rara só podem ser usados para raciocínio.
- Calcule a economia de atenção computacional da NSA versus atenção total em contexto de 64k como função do tamanho do bloco de compressão e da seleção top-k.
  计算在 64K 上下文中 NSA相对全注意的计算节省量(como função de blocos de compressão de grandeza e seleção de top-k)
- Implementar a combinação de três ramos no stdlib Python em uma curta sequência sintética e verificar o comportamento dos pesos de gating.
  Usar Python em sequências de síntese curtas para implementar três componentes, verificando o controle de peso

## O problema é o problema da introdução

Atenção total no comprimento da sequência N custos `O(N^2)`tempo e`O(N)`O cache KV por camada. Em tokens 64k, os números de computação e largura de banda de memória são catastróficos. Estimação teórica medida do papel da NSA: a atenção representa 70-80% da latência total de decodificação em 64k. Tudo no downstream  TTFT, tokens / sec, custo por milhão de tokens  é dominado pelo custo da atenção.

> 序列长度 N                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `O(N^2)`时间和每层 `O(N)`KV 缓存── em tokens 64k 时,计算和显存带宽的数字是灾难性的──NSA 论文的测量理论估计:64k 时注意占据总解码延迟的70-80%──所有下游指标TTFT、tokens/sec、每百万 token 成本都由注意成本主导──

Pouca atenção é a resposta óbvia. As tentativas anteriores caem em dois baldes. A esparcidade de padrão fixo (janela deslizante, passo, bloco local) descarta informações e falha em tarefas de recall de longo alcance. A esparcidade de tempo de inferência (KV cache pruning, H2O, StreamingLLM) é aplicada a um modelo pré-treinado em atenção densa e recupera apenas uma fração do potencial aceleramento porque o modelo nunca foi solicitado a encaminhar informações através do padrão esparso.

> 稀疏注意力是显而易见的答案―― anteriores tentativas foram divididas em duas categorias――固定模式稀疏性 (modular fixo de rareficação) 滑窗,跨步,块局部) (desperdição de informações e falha na tarefa de memória de longo prazo――推理时稀疏性 (KV 缓存剪枝, H2O, StreamingLLM) é usado em modelos de treinamento em atenção intensiva, só pode recuperar uma pequena parte da potencial aceleração, pois o modelo nunca foi solicitado através de informações de módulos de rareficação.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 best paper, arXiv:2502.11089) faz ambas as coisas: um padrão de esparcidade que o modelo aprende durante o pré-treino, implementado como um algoritmo alinhado ao kernel que realmente fornece as economias de computação na inferência.

> O estudo foi realizado em um estudo de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pes

## O conceito central.

> **【中文解读】**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é que é o que é o que é que é o que é que é o que é que é o que é que é o que é que é o que é que é que é o que é que é o que é que é que é o que é que é que é que é que é o que é que é que é o que é que é que é que é que é que é que é.

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral's 32K 窗口) + 全局 token([CLS]) + 选择性关注。Google's Ring Attention 和 Block-Sparse Attention 将上下文扩展到百万代币──DeepSeek's NSA(Native Sparse Attention) 在训练时直接学习稀疏模式──


### Três ramos paralelas

Para cada consulta, a NSA corre a atenção três vezes, contra três visualizações diferentes do cache KV:

1. **Compressed branch.**Os tokens são agrupados em blocos de tamanho `l`Cada bloco é comprimido em um único token de resumo através de um pequeno MLP aprendido.

2. **Selected branch.**Usando pontuações de atenção do ramo comprimido, os blocos top-k mais relevantes para a consulta atual são identificados. Tokens de grãos finos (não comprimidos) desses blocos são lidos e a consulta atende a todos eles. Pense na atenção do ramo comprimido como o sinal de roteamento para a seleção.

3. **Sliding-window branch.**A consulta atende aos mais recentes `W`Tokens (tipicamente 512) para contexto local. Este ramo capta os padrões de curto alcance de estrutura pesada (sintaxa, coreferência local) que os outros dois podem perder.

As três saídas de ramificação são combinadas através de um portão de posição aprendido:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`Não é necessário somar a 1  podem pesar ramos de forma independente.

### Por que isso é "naturalmente treinável"

O passo de seleção (blocos de topo-k) é discreto. Operações discretas quebram fluxo de gradiente. O trabalho anterior de atenção escassa ou saltou o backprop através da seleção (treino limitante) ou usou relaxações contínuas que não deram escassez real na inferência.

A NSA evita isto: a atenção de ramo comprimido é uma atenção grosseira diferenciável sobre toda a sequência. A operação top-k apenas reutiliza as pontuações de atenção mais altas do ramo comprimido para escolher quais blocos de grãos finos carregar. Os gradientes fluem através das pontuações de ramo comprimido (que influenciam tanto a saída comprimida quanto a lógica de seleção), e a contribuição dos blocos selecionados para a saída final também é diferenciável. O não diferenciável`top_k`A operação é um no-op no gráfico computacional avançado.

É por isso que a NSA pode ser usada em pré-treino de ponta a ponta. O modelo aprende a encaminhar informações através dos três ramos em conjunto, produzindo um padrão escasso que, na inferência, realmente entrega a velocidade prometida.

### Núcleo alinhado com hardware

O kernel da NSA é projetado para hierarquias de memória GPU modernas. O kernel carrega consultas por grupos GQA (loop externo), traz os blocos de KV esparsos correspondentes por grupo (loop interno) e dirige a atenção para SRAM. Como cada grupo de consulta vê os mesmos blocos selecionados (a seleção é por grupo de consulta, não por cabeça de consulta), as cargas de KV são amortizadas em todo o grupo.

O artigo relata que os kernels de Triton executam 9 vezes mais rápido do que o FlashAttention em 64k decodificadores, com a taxa de aceleração crescendo com o comprimento da sequência.

### Orçamento de cálculo

Deixe-me .`N`ser o comprimento da sequência, `l`O tamanho do bloco de compressão, `k`o número de seleções de cima-k, `w`a janela deslizante, `b`O tamanho do bloco selecionado (normalmente é igual `l`)).

- Arco comprimido: `O(N/l)`Chaves por consulta, então `O(N * N / l)`- Total.
- Ramo selecionado: `O(k * b)`Chaves por consulta, então `O(N * k * b)`- Não .
- Arranho deslizante: `O(w)`Chaves por consulta, então `O(N * w)`- Não .

Total: `O(N * (N/l + k*b + w))`- Não .

Com o`N = 64k, l = 64, k = 16, b = 64, w = 512`: custo por consulta é `1000 + 1024 + 512 = 2536 keys`- Atenção total é ...`64000 keys`- 25 vezes a redução de cálculo.

Com o`N = 128k, l = 64, k = 16, b = 64, w = 512`: custo por consulta é `2000 + 1024 + 512 = 3536 keys`- Atenção total é ...`128000 keys`O benefício aumenta com o comprimento da sequência, que é o ponto principal.

### Como é que se compara

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) foi publicado simultaneamente e adota uma abordagem similar de três é melhor do que um, aplicando o princípio de MoE aos blocos de atenção. NSA e MoBA são as duas arquiteturas para saber para 2026 pré-treinamento de longo contexto.


> **【拓展：稀疏注意力在长上下文中的应用】**O número de dados de um computador de 128K em 1M é reduzido para um nível aceitável.


## Construí-lo e realizei-o.
```figure
sliding-window-attention
```

## Construí-lo

`code/main.py`Implementa os três ramos numa curta sequência sintética e mostra:

- A MLP de compressão (uma linha de base simples de média é usada para clareza pedagógica; a NSA real usa uma MLP aprendida).
- A selecção de blocos de cima-k, impulsionada por pontuações de ramos comprimidas.
- A atenção da janela deslizante na última.`w`- Os tokens.
- A combinação fechada.
- Uma impressão de contagem computacional comparada à atenção total.

### Passo 1: comprimir os tokens em blocos

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Passo 2: Atenção a ramificação comprimida

Execute a atenção de softmax da consulta contra as teclas comprimidas.

### Passo 3: Seleção do bloco superior

Escolha os índices do `k`Blocos comprimidos com maior pontuação. Carregue os tokens originais não comprimidos desses blocos e dê atenção a eles.

### Passo 4: Atenção à janela deslizante

Tome o último .`w`- E a atenção estática contra eles.

### Passo 5: porta + combinação

Uma pequena MLP na consulta produz três pesos de porta. A saída final é uma soma ponderada das três saídas de ramo.

### Passo 6: contagem computacional

Imprimir o número de teclas atendidas por consulta para cada ramo e o total.`N`Em uma sintética com 1024 tokens com`l = 32, k = 4, w = 128`A NSA vê .`32 + 128 + 128 = 288`As chaves por consulta versus 1024 para atenção total  3,5 vezes menos.

## Use-o com o framework implementado.

A NSA está a enviar no próprio DeepSeek de longo contexto de pré-treinamento pipeline.

- **DeepSeek internal**: pesos nativos e publicados utilizam a NSA ou o seu sucessor DSA (Deepseek Sparse Attention).
- **vLLM**: apoio experimental da NSA no desenvolvimento de pesos DeepSeek-V3.x.
- **SGLang**: Os índices de referência da NSA publicados; o caminho de produção segue o VLLM.
- **llama.cpp / CPU**: não suportado; o custo de decomposição do kernel não vale a pena na capacidade de CPU.

Quando contactar a NSA:

- Cursos de pré-formação ou de formação contínua destinados a contextos superiores a 64 000 e com um orçamento de cálculo sério.
- Inferência dos próprios pontos de controlo de longo contexto da DeepSeek.

Quando não:

- Não se pode modernizar a NSA sem treinamento.
- O custo superior de três ramos domina as poupanças.
- Chat interativo de batch 1. Benefícios de decodificação sensível à latência, mas apenas em contextos longos.

## Envia-o . Produto .

Esta lição produz`outputs/skill-nsa-integrator.md`. Dada uma especificação de execução pré-treinamento de longo contexto, produz um plano de integração NSA: tamanho de bloco de compressão, top-k, janela deslizante, largura de porta MLP, escolha do kernel e as avaliações específicas de longo contexto que justificariam a mudança de arquitetura.

> 本课产 出 `outputs/skill-nsa-integrator.md` Providenciar o desenvolvimento de um programa de integração da NSA: compressão de blocos de grande dimensão, de cima a fundo, de janelas de deslizamento, de controle de portas, de MLP, de largura, de seleção do núcleo, bem como de demonstração de que a estrutura é mais razoável.

## Exercícios.

1. Corra .`code/main.py`- Em um token sintético de 1024 .`(l, k, w)`Identificar o pré-conto que atinge o menor número de chaves por consulta, mantendo 95% de recall contra a atenção total em um teste de agulha-em-pacote de feno.
   Tradução do inglês:`code/main.py` Em três pré-estações`(l, k, w)`Não imprimir quantidade de cálculo. Encontrar em testes de estaca de feno para manter a atenção total em 95% de taxa de convocação ao mesmo tempo em que alcançar o mínimo de preconceito de cada consulta.

2. Substitua o compressor de média com um pequeno MLP aprendido (2 camadas, escondidas 32). Treine-o em uma tarefa sintética onde o sinal é a média de um bloco. Mese a diferença de perplexidade contra a linha de base do mean pool em dados mantidos.
   Tradução em inglês: using小型学习 MLP ((2 Layer, Hidden 32) substituir o compressor de um valor médio de um bloco de dados em um bloco de um valor médio de um bloco de dados.

3. Implementar o gate MLP. Ele toma a consulta como entrada e sai três escalares. Mostre que o gate se comporta sensatamente: ponderação quase uniforme em consultas aleatórias, peso pesado no ramo selecionado quando a consulta atinge um bloco de trás distante.
   Tradução do inglês para inglês: implementing door control MLP── é usado para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazer perguntas para fazerem perguntas para fazerem perguntas para fazerem para fazerem para fazer perguntas para fazer perguntas para fazerem para fazer perguntas.

4. Calcule o orçamento de memória do cache KV para um modelo 70B habilitado pela NSA em contexto de 128k. Cabeças KV são 8, cabeça dim 128, BF16. Compare com atenção plena e MLA (Fase 10 · 14 mostrou os números do MLA). Identifique o comprimento da sequência onde o cache KV de ramo fino da NSA é igual à atenção completa.
   O modelo 70B de NSA  iniciado em 128K  KV 缓存内存预算──KV 头 8 个,头维度 128,BF16──与全注意力和MLA比较──找到 NSA 细粒度分支 KV 缓存等于全注意序列长度──

5. Leia a Seção 4 do documento da NSA (arXiv:2502.11089) e explique em três frases por que as pontuações de atenção do ramo comprimido são reutilizadas para a seleção top-k em vez de calcular uma pontuação de roteamento separada.
   Tradução do idioma japonês: Lire o artigo 4o do NSA, usando três palavras para explicar por que o número de unidades de atenção em um grupo de compressores é usado para escolher o topo do grupo de recursos, e não para calcular o número de unidades de dados de um grupo de recursos.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## Mais leitura 延伸阅读

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089)O papel
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) os alvos da família de arquiteturas da NSA
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) Trabalho simultâneo, atenção ao estilo MoE sobre blocos
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) Origens de janelas deslizantes
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) A linha de base da escarsidade no tempo de inferência
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) a linha de base de atenção completa os núcleos NSA bater em 64k
