# Escalada: Treinamento Distribuído, FSDP, DeepSpeed.

> O seu modelo 124M treinado em uma GPU. Agora tente 7 bilhões de parâmetros. O modelo não cabe na memória. Os dados levam semanas em uma única máquina. O treinamento distribuído não é opcional em escala. É o único caminho para a frente.

> **【中文解读】**1.24 bilhão de modelos são treinados em uma única GPU. Mas 70 bilhões de modelos de parâmetros não estão disponíveis, e os dados de treinamento de uma única máquina precisam de várias semanas.

> **【拓展：DeepSeek-V3的2048卡训练】**DeepSeek-V3 utiliza 2048 张 H800 GPU train, adota DualPipe 流水线并行 + MoE 专家并行── compreender treinamento distribuído é a base para entender como um grande modelo de vanguarda é treinado fora──

> - Não .**【前置】**学本节前请先掌握:Fase 10·04(Pre-Training Mini GPT)单 GPU 训练基础;PyTorch DDP 概念;多 GPU 通信(NCCL、AllReduce)。本节是Fase 10·19(DualPipe)和Fase 10·20(DeepSeek-V3 Walkthrough) 的前置──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 04 (Pre-Training a Mini GPT)
**Time:** ~120 minutes

> - Não .**【类比】**Distribuição de treinamento = 多人合作搬大箱子──**数据并行**(DP) = 4 个体各搬一个相同的小箱子(同模型不同数据,结果 AllReduce 平均) ⋅**张量并行**(TP) = 4 pessoas juntos carregam um grande caixão de quatro cantos (TTP)**流水线并行**(PP) = 4 个人流水线,第 1 人搬一层传给第二 人(模型按层切分)**FSDP**= DP + 把模型切片分到各卡,用时再聚合 (省显存) ―― produção cenário geral 3 组合 (用3D paralelismo) 』

> ️ **【易错点】**3 crateras de treino:**batch size 设错**单卡 bs=8,4 卡应该 bs=32(4×8)而非 bs=8; usar o tamanho de lote efetivo 计算 lr―(2) **AllReduce 瓶颈**卡间通信比 GPU 计算慢 10 倍,bs 太小会让 GPU等通信;bs 至少 32+才划算──(3) **没设 seed** Cada cará de início diferente, resultados irrepetíveis;`torch.manual_seed(42) + torch.cuda.manual_seed_all(42)`- Não.

## Objetivos de aprendizagem

- Explique os três tipos de paralelismo (dados, tensor, pipeline) e quando cada um é necessário com base no modelo e no tamanho do cluster
  解释三种并行类型(数据并行、张量并行、流水线并行) e suas aplicações
- Implementar treinamento paralelo de dados usando PyTorch DDP com sincronização de gradientes em várias GPUs
  Utilize PyTorch DDP  realçar vários dados GPU                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
- Calcular o orçamento de memória para um determinado tamanho do modelo (pesos + estados de otimização + gradientes + ativações) para determinar o hardware mínimo
  计算给定模型大小的显存预算(权重 + 优化器状态 + 梯度 + 激活值), determinar a mínima demanda de hardware
- Configurar os estágios FSDP ou DeepSpeed ZeRO para fragmentar os estados do modelo em GPUs e modelos de ajuste que excedam a memória de um único GPU
  Configurar o FSDP ou a fase de ZeRO DeepSpeed para um estado de modelo fragmentado, para que o modelo ultra-singular possa ser treinado

> **【中文解读】**Este curso focaliza-se no núcleo do treinamento LLM: evidência de armazenamento.

## O problema é o problema da introdução

Um modelo de parâmetro 7B em FP16 precisa de 14 GB apenas para os pesos. O Adam Optimizer armazena duas cópias adicionais de cada parâmetro (estimativas do primeiro e segundo momento). Isso é mais 28 GB. Os gradientes durante a propagação de volta adicionam 14 GB mais. Você está em 56 GB antes de uma única ativação ser armazenada.

> O modelo de parametros 7B em FP16 abaixo apenas o peso requer 14GB. Adão  optimizador para cada parametros extra armazenamento de duas duplicadas ((1st and second phase estimation), também requer 28GB.

Um NVIDIA A100 tem 80 GB de memória.

> NVIDIA A100 tem 80 GB de armazenamento.

56 GB dos 80 GB consumidos. Isso deixa 24 GB para a ativação - os valores intermediários calculados durante a passagem avançada que devem ser mantidos vivos para a propagação para trás. Para uma sequência de 2048 tokens com um modelo 4096 dimensões, as ativações de uma única camada usam cerca de 64 MB. Com 32 camadas, você precisa de 2 GB por amostra. Um tamanho de lote de 8 requer 16 GB. Você tem 24 GB. Um tamanho de lote de 12 explode.

> O 80GB já consumiu 56GB. O restante de 24GB é usado para o valor de ativação  pré-direita de divulgação  calculado para o cálculo do valor médio, deve ser mantido para a distribuição de dados  para 2048 tokens 序列 e 4096 维模型, o valor de ativação de uma única camada é de cerca de 64MB.

Agora tente parâmetros 70B. Pesos sozinhos: 140 GB em FP16. Não cabe em uma GPU. Você precisa de pelo menos 2 A100s (2 x 80 GB = 160 GB) apenas para manter os pesos. Adicione estados e gradientes de otimização e você precisa de muito mais: 3+ GPUs mínimo, e realisticamente 8-16 dependendo da estratégia de fragmentação.

> Agora tente 70B 参数。 apenas peso:FP16 下 140GB。放不进一张 GPU── pelo menos 2张 A100(2 x 80GB = 160GB) para poder colocar o peso abaixo──加上优化器状态和梯度,需要更多: pelo menos 3+张 GPU,实际需要 8-16张,取决于分片策略──

O Llama 3 405B foi treinado em 16.384 GPUs NVIDIA H100.$100 million in compute. DeepSeek V3 trained a comparable model for roughly $5,6 milhões por ser inteligente sobre a arquitetura (Mixura de Especialistas significa apenas uma fração dos parâmetros ativados por token) e eficiência de formação.

> Llama 3 405B em 16,384 张 NVIDIA H100 GPU 上训练,计算成本估计约10亿美元──DeepSeek V3 通过巧妙的架构设计 ((MoE significa apenas parte do parâmetro ativado por cada vez)

Esta lição abrange as quatro estratégias que possibilitam o treinamento em larga escala: paralelo de dados, paralelo tensor, paralelo pipeline e paralelo de dados totalmente fragmentados. Você irá simular cada uma em Python puro para entender a mecânica antes de tocar em uma estrutura de treinamento distribuída.

> Esta capacitação abrange quatro estratégias de treinamento em grande escala: dados em conjunto, quantidade em conjunto, fluxo em conjunto e um conjunto completo de dados em pedaços. Você vai entender o mecanismo antes de entender o quadro de treinamento distribuído em contato com Python.

## O conceito central.

### Por que é necessário distribuir

Aqui está a matemática da memória para modelos reais.

> Aqui estão os cálculos matemáticos de cada número, não de uma estimativa.

| Model | Params | Weights (FP16) | Adam States | Gradients (FP16) | Total (no activations) |
|-------|--------|----------------|-------------|------------------|----------------------|
| GPT-2 Small | 124M | 248 MB | 992 MB | 248 MB | 1.5 GB |
| Llama 3 8B | 8B | 16 GB | 64 GB | 16 GB | 96 GB |
| Llama 3 70B | 70B | 140 GB | 560 GB | 140 GB | 840 GB |
| Llama 3 405B | 405B | 810 GB | 3,240 GB | 810 GB | 4,860 GB |

A coluna "Estados de Adam" é o assassino. Adam armazena uma média em execução (m) e uma variância em execução (v) para cada parâmetro, ambos em FP32. Para um modelo 70B, que é 70B x 4 bytes x 2 = 560GB. Otimizador sozinho precisa de sete A100s.

> "Adão  estado"列是致命的──Adam 为每个参数存储一个运行平均值(m) 和一个运行方差(v), são FP32──对于70B 模型,即70B x 4字节 x 2 = 560GB──只有优化器就需要七张A100──

Um único H100 tem 80 GB. Llama 3 405B precisa de pelo menos 61 H100s para manter os pesos, otimizador e gradientes. Adicionar ativações e o número cresce ainda mais. Meta usou 16.384 GPUs não porque queriam - porque tinham que.

> 单张H100 有80GB──Llama 3 405B 至少需要61张H100来放置权重、优化器和梯度──加上激活值数字更大──Meta Utilize 16,384张 GPU 不是因为他们想而是因为他们必须──

> **【中文解读】**显存预算是LLM 训练的第一道关卡──以 Llama 3 70B为例:FP16 权重140GB + Adam 优化器状态 560GB + 梯度 140GB = 840GB(没有激活值)──单张H100 只有80GB,至少需要11张GPU才能放下这些状态──Llama 3 405B 的总需求高达4,860GB──Adam 优化器是显存杀手它为每个参数存储两个 FP32 的动量估计节量m和 v),参数 x 8 字 x 2──

> **【拓展：Llama 3 的 16384 GPU 训练】**Llama 3 405B em 16,384 张 H100 GPUs, treinamento, usando 3D e 流行 (data并行 + 张量并行 + 流水线并行) ⋅ treinamento custo total estimado em cerca de 1 bilhão de dólares.

### Paralelismo dos dados

A estratégia mais simples distribuída. Copie todo o modelo para N GPUs. Divida cada lote de treinamento em N partes iguais. Cada GPU executa uma passagem para frente e para trás em seu fragmento de dados. Depois da passagem para trás, media os gradientes em todas as GPUs. Cada GPU atualiza sua cópia dos pesos com os mesmos gradientes médios, mantendo todas as cópias em sincronia.

> A estratégia mais simples de distribuição é: • Reproduzir todo o modelo em N 张 GPU• Dividir cada treinamento em N 等份• Dividir cada GPU em seus pedaços de dados para a execução de progressão e reversão de propagância• Depois de se propagarem de forma reversal, em todas as GPUs 间平均梯度• Usar a mesma média梯度 para atualizar suas cópias de peso, manter todas as cópias em sintonia•

**The good:**Escalada de passagem linear. N GPUs processam N vezes mais dados por passo. A comunicação é limitada à média de gradiente, que se sobrepõe com a computação.

> **优点：**吞吐量线性扩展──N 张 GPU Cada passo processar N 倍的数据──通信只限在梯度平均,可与计算重叠──

**The bad:**Cada GPU possui uma cópia completa do modelo, estados de otimização e gradientes. Para um modelo 70B, cada GPU precisa de 840 GB. O paralelismo de dados não reduz nada a memória por GPU.

> **缺点：**Cada GPU  possui um modelo  Otimizador está em estado e estágio  para o modelo 70B , cada GPU  precisa de 840GB  dados  não reduzem a cada GPU  aparência , mas reduzem o tempo de treinamento

**The math:**Tamanho de lote efetivo = por_gpu_batch_size x N. Para GPUs N=64 com lote por GPU de 16, o lote efetivo é 1.024. Llama 3 usou um tamanho de lote efetivo de 16 milhões de tokens por passo.

> **数学：**Para N = 64 张 GPU, por GPU 批量 16,有效批量为 1,024──Llama 3 使用每步 1600万代币的有效批量──

```mermaid
graph TD
    subgraph DataParallel["Data Parallelism (N=4 GPUs)"]
        B["Full Batch\n(1024 samples)"] --> S["Split"]
        S --> G1["GPU 1\nFull Model Copy\n256 samples"]
        S --> G2["GPU 2\nFull Model Copy\n256 samples"]
        S --> G3["GPU 3\nFull Model Copy\n256 samples"]
        S --> G4["GPU 4\nFull Model Copy\n256 samples"]
        G1 --> AR["AllReduce\nAverage Gradients"]
        G2 --> AR
        G3 --> AR
        G4 --> AR
        AR --> U["Update\n(identical on all GPUs)"]
    end

    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style G1 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G3 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G4 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style AR fill:#1a1a2e,stroke:#51cf66,color:#fff
    style U fill:#1a1a2e,stroke:#51cf66,color:#fff
```

### Paralelismo de tensão

Divida camadas individuais em GPUs. Uma única multiplicação de matriz é dividida entre GPUs, cada parte da computação do resultado.

> A partir de então, a massa de dados de cada câmara é dividida em várias GPUs.

Considere uma matriz de peso de forma (8192, 8192) em uma camada de feedforward. Com o paralelismo de tensor de quatro vias, cada GPU mantém um fragmento (8192, 2048). Cada GPU multiplica a entrada por seu fragmento, produzindo um resultado parcial. Os resultados parciais são combinados (via total redução ou total coleta) para produzir a saída completa.

> 考虑前层中形为 (8192, 8192) 的权重矩阵──使用 4 路张量并行,每张 GPU 持有的分片 (8192, 2048) 的分片──每张 GPU 将输入乘以其分片,产生部分结果──部分结果通过全归约或全收集组合为完整输出──

**The good:**Reduz a memória por GPU para pesos do modelo. Um modelo 70B dividido em 8 GPUs significa que cada GPU possui pesos de ~ 8,75B parâmetros.

> **优点：**Reduzir o peso do modelo para cada GPU 显存──70B 模型分成8张 GPU

**The bad:**Requer comunicação rápida entre GPUs após cada camada. O all-reduce após cada matmul adiciona latência. Isso funciona bem com NVLink (900 GB / s entre GPUs no mesmo nó) mas mal em todos os nós conectados por InfiniBand (400 Gb / s, cerca de 50 GB / s).

> **缺点：**Cada nível requer GPU 间通信── 间通信── 间接的速度增加延迟── 间接的速度增加延迟── 间接的速度增加延迟── 间接的速度增加延迟── 间接的速度增加了.

**Real usage:**Megatron-LM foi pioneiro no paralelismo tensor. Llama 3 405B usa o paralelismo tensor de 8 vias dentro de cada nó.

> **实际使用：**Megatron-LM  pioneira propôs 张量并行──Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 405B  Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 Llama 3 L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L

> **【中文解读】**张量并行 (tensor paralelismo) vai dividir uma única camada de matrizes em múltiplas GPUs. Por exemplo, uma (8192, 8192) de matrizes de peso em 4 路并行 (também apenas em 4 路并行) de cada GPU, mas a falha é que cada camada precisa de redexponência total (todos reduzidos) para comunicação, portanto, quase que apenas se limita a NVLink 连接的单节点内 (também em 8 张 GPU) ⋅ Llama 3 405B em 8 路张量并行 (também em 8 路张量并行).

> **【拓展：流水线并行的气泡问题】**流水线并行将模型按层分为不同 GPUs (como GPU1 跑 1-8层, GPU2 跑 9-16层) 但会产生"气泡"GPU 空等.

### Paralelismo de oleodutos

Divida o modelo por camadas. GPU 1 executa camadas 1-8. GPU 2 executa camadas 9-16. GPU 3 executa camadas 17-24. GPU 4 executa camadas 25-32. Dados fluem através do pipeline: GPU 1 calcula suas camadas e envia ativações para GPU 2, que calcula suas camadas e envia para GPU 3, e assim por diante.

> 按层拆分模型──GPU 1 跑 1-8层──GPU 2 跑 9-16层──GPU 3 跑 17-24层──GPU 4 跑 25-32层──数据流过流水线:GPU 1 计算其层并将激活值发送给 GPU 2,GPU 2 计算其层并发送给 GPU 3,以此类推──

**The good:**Minima comunicação entre GPUs - apenas as ativações em limites de camadas, que são pequenas em comparação com gradientes ou pesos. Funciona em todos os nós porque os requisitos de largura de banda são baixos.

> **优点：**O menor número de GPUs em comunicação é apenas o valor de ativação da linha de limite, muito pequeno em relação à escala ou peso.

**The bad:**Quando a GPU 4 está calculado o passagem para a frente em micro-batch 1, GPUs 1, 2 e 3 são inativos (eles já encaminharam sua porção). Durante o passagem para trás, o padrão se inverte. Com pipelining ingênuo, a utilização da GPU é apenas 1/N para N estágios de pipeline.

> **缺点：**流水线气泡── Quando a GPU 4 em calcular os avanços de 1 de micro-bots, a GPU 1、2、3 空(já terminaram sua própria parte)──反向传播时模式相反──朴素流水线下, N 个阶段 GPU utilization rate é apenas de 1/N──

**GPipe and PipeDream**Resolver o problema da bolha dividindo o lote em micro-batches. GPU 1 começa no micro-batch 2 assim que termina de encaminhar o micro-batch 1. Esta sobreposição da computação em todas as fases do pipeline. Com os micro-batches M e os estágios N, a fração da bolha cai para (N-1) / M. Use M=16 micro-batches com N=4 estágios e a bolha é 3/16 = 18,75% de tempo de inatividade.

> **GPipe 和 PipeDream**通過將批次分分成微批次來解決氣泡問題──GPU 1 一完成微批次 1 的前向传播就開始微批次 2──这在流水线阶段间重叠计算──M 个微批次和N 个阶段,气泡比例降至 (N-1) /M──使用M=16 个微批次和N=4 个阶段,气泡为3/16 = 18.75% 空时间──

### FSDP: Dados totalmente fragmentados paralelamente

O FSDP combina a escalabilidade do paralelismo de dados com a eficiência da memória do sharding. Em vez de cada GPU manter uma cópia completa do modelo, cada GPU mantém apenas 1/N dos parâmetros, gradientes e estados do optimizador.

> O FSDP combina a expansão e a eficiência de armazenamento de bits de parâmetros de dados. Cada GPU não possui uma cópia completa do modelo, mas apenas um parâmetro, gradiente e estado de optimizador de 1/N.

Antes de uma camada passar para a frente, o FSDP executa um **all-gather**Para recolher os parâmetros completos de todas as GPUs na memória de cada GPU. Depois da passagem para a frente, cada GPU descartará os parâmetros não locais. Durante a retrocidação, o conjunto será executado novamente para reconstruir os parâmetros para a computação de gradiente.**reduce-scatter**distribui fragmentos de gradientes para que cada GPU só armazene 1/N dos gradientes.

> Antes da propagação de uma camada, o FSDP executa a operação de coleta completa de todos os parâmetros da GPU até o aparelho de cada GPU. Depois da propagação de uma camada, cada GPU deixa de usar os parâmetros não locais.

**The math for a 70B model on 8 GPUs:**

| Component | Without FSDP | With FSDP |
|-----------|-------------|-----------|
| Weights (FP16) | 140 GB per GPU | 17.5 GB per GPU |
| Adam States (FP32) | 560 GB per GPU | 70 GB per GPU |
| Gradients (FP16) | 140 GB per GPU | 17.5 GB per GPU |
| **Total** | **840 GB per GPU** | **105 GB per GPU** |

Sem FSDP, você não pode colocar um modelo 70B em uma única GPU de 80GB. Com FSDP em 8 GPUs, cada GPU usa 105GB - espere, isso ainda não se encaixa. Você precisa de pelo menos 16 GPUs para ficar abaixo de 80GB por GPU, ou você combina FSDP com controle de ativação (recomputa ativações durante retrocesso em vez de armazená-las).

> 没有FSDP,70B 模型不能放入单张80GB GPU──使用FSDP在8张 GPU上,每张 GPU使用105GB等等,还是放不下──你需要至少16张 GPU 才能降至每卡80GB以下,或将FSDP与激活检查点结合(反向传播时重新计算激活值而不是存储它们) ⋅

O custo de comunicação é maior do que o paralelismo de dados de vainilha, devido ao todo-reunido antes de cada camada. Mas as economias de memória tornam possíveis corridas de treinamento anteriormente impossíveis.

> O custo de comunicação é maior do que o de uma data comum, pois cada nível requer uma coleta completa antes.

> **【中文解读】**FSDP( completa parcela de dados e parcela) é a combinação de dados e parcela de parcelação. Cada GPU só armazenou 1/N de parâmetros, gradientes e estado de optimizador.

> **【拓展：DeepSpeed ZeRO 的三个阶段】**ZeRO Fase 1 分片优化器状态(省 4x 显存),Fase 2 加上梯度分片(省 8x),Fase 3 加上参数分片(省 N 倍,N 为 GPU 数) ・FSDP 本质上是 ZeRO Fase 3 的 PyTorch 原生实现──Llama 3 405B 的 16,384 GPU 训练使用了FSDP + 张量并行 + 流水线并行的3D组合──

```mermaid
graph TD
    subgraph FSDP["FSDP: Fully Sharded Data Parallel (4 GPUs)"]
        direction TB
        S["Model: 4 layers, sharded"]

        subgraph GPU1["GPU 1"]
            G1S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU2["GPU 2"]
            G2S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU3["GPU 3"]
            G3S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end
        subgraph GPU4["GPU 4"]
            G4S["Shard: 1/4 params\n1/4 optimizer\n1/4 gradients"]
        end

        AG["All-Gather\n(reconstruct full params\nbefore each layer)"]
        FW["Forward Pass\n(full params temporarily)"]
        RS["Reduce-Scatter\n(distribute gradient shards\nafter backward)"]

        S --> GPU1
        S --> GPU2
        S --> GPU3
        S --> GPU4
        GPU1 --> AG
        GPU2 --> AG
        GPU3 --> AG
        GPU4 --> AG
        AG --> FW
        FW --> RS
    end

    style G1S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G3S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G4S fill:#1a1a2e,stroke:#0f3460,color:#fff
    style AG fill:#1a1a2e,stroke:#e94560,color:#fff
    style FW fill:#1a1a2e,stroke:#51cf66,color:#fff
    style RS fill:#1a1a2e,stroke:#e94560,color:#fff
```

### DeepSpeed ZeRO

O ZeRO (Zero Redundancy Optimizer) da DeepSpeed é conceitualmente idêntico ao FSDP, mas foi desenvolvido de forma independente pela Microsoft.

> O ZeRO de DeepSpeed é conceptualmente semelhante ao FSDP, mas desenvolvido pela Microsoft independentemente.

| Stage | Shards | Memory Savings | Communication |
|-------|--------|---------------|---------------|
| ZeRO-1 | Optimizer states only | ~4x reduction | Same as data parallel |
| ZeRO-2 | + Gradients | ~8x reduction | Slightly more |
| ZeRO-3 | + Parameters | ~Nx reduction (N GPUs) | All-gather per layer |

O ZeRO-3 é equivalente ao FSDP. O nome é diferente, o mecanismo é o mesmo. PyTorch adicionou o FSDP como uma implementação nativa depois que a DeepSpeed provou o conceito.

> ZeRO-3 é igual ao FSDP. Nome diferente, mecanismo igual.

A DeepSpeed também introduziu o ZeRO-Offload (estados de otimização de descarga para RAM da CPU, que é mais barato e maior) e o ZeRO-Infinity (carga para SSDs NVMe).

> A DeepSpeed também introduziu o ZeRO-Offload (o estado dotimizador será desligado para a memória do CPU, mais barato e maior) e o ZeRO-Infinity (desligado para o NVMe SSD) (o que permite a câmara de câmara de armazenamento ser mais lenta, mas liberta o GPU).

### Treinamento Misto de Precisão

O treinamento moderno utiliza vários formatos de pontos flutuantes simultaneamente:

> 现代训练同时使用多种浮点格式:

- **Forward pass**A memória é metade da memória da FP32.
- **Master weights**FP32 (32-bit). Mantido pelo optimizador para precisão numérica durante atualizações de peso.
- **Loss scaling**Multiplicar a perda por uma constante grande antes de passar para trás para evitar que os gradientes FP16 caam para zero. Dividir pela mesma constante antes do passo de otimização.

O BF16 (Brain Float 16) tem o mesmo intervalo de exponentes que o FP32 (8 bits de exponente), mas precisão reduzida (7 bits de mantissa vs. FP32's 23).

Os TPUs do Google usam BF16 nativo. A A100 e H100 da NVIDIA suportam tanto o FP16 quanto o BF16.

> **【中文解读】**混合精度训练是现代 LLM 训练的标准做法:前向传播用 BF16(16 位),优化器维护 FP32 主权重(32 位),损失缩放防止梯度下溢──BF16 混合精度与 FP32 有相同指数范围;;8 位),但精度降低(7 位尾数 vs 23 位),几乎不需要损失缩放──业界已从 FP16 全面显度转向 BF16──混合精度为7B 模型节省约28GB ⋅

> **【拓展：3D 并行与 MoE 的经济性】**Llama 3 405B Utilize 3D 并行:节点间数据并行 + 节点内 8 路张量并行 + 跨节点流水线并行。DeepSeek-V3 则使用 MoE(混合专家) Arquitetura reduzir custos Persequência de divulgação apenas ativar cerca de 37B 参数(总参数 671B), custo de treinamento apenas cerca de 560 milhões de dólares, é 1/18 de Llama 3

**Memory comparison for a 7B model:**

| Precision | Weights | Optimizer | Gradients | Total |
|-----------|---------|-----------|-----------|-------|
| FP32 everywhere | 28 GB | 56 GB | 28 GB | 112 GB |
| Mixed (BF16 + FP32 master) | 14 GB | 56 GB | 14 GB | 84 GB |

A precisão mista economiza 28 GB neste modelo. Os estados do optimizador permanecem em FP32 independentemente - é aqui que a maior parte da memória vai.

### Megatron-LM e paralelo 3D

A formação real em larga escala combina os três paralelismos:

- **Data parallelism**Em grupos de nós ( tamanho de lote de escala)
- **Tensor parallelism**dentro de um nó (camadas divididas em 8 GPUs)
- **Pipeline parallelism**através de nós (grupos de camadas divididos entre máquinas)

Llama 3 405B em 16.384 H100s:
- Paralelo tensor de 8 vias dentro de cada nó (8 GPUs por nó)
- Paralelamente de 16 vias de oleodutos em todos os nós (16 fases de oleodutos)
- Paralelamente de dados de 128 vias em toda a dimensão restante (16.384 / 8 / 16 = 128)

Esta decomposição 3D (8 x 16 x 128 = 16,384) é como você escala para milhares de GPUs. Cada GPU vê um fragmento de dados diferente (paralelo de dados), mantém uma fatia de cada camada (paralelo de tensor) e calcula um conjunto diferente de camadas (paralelo de pipeline).

> Esta forma de 3D de divisão ((8 x 16 x 128 = 16,384) é como você se expande para milhares de GPUs.

A DeepSeek V3 adotou uma abordagem diferente. A sua arquitetura Mix of Experts ativa apenas 37B de 671B parâmetros por token. Isso significa que cada GPU só precisa calcular (e armazenar ativações para) os parâmetros ativos. Eles treinaram em 2.048 H800 GPUs - menos de 1/8 da contagem de GPU da Meta - para$5.6M vs Meta's estimated $100 milhões.

> DeepSeek V3  adotou diferentes métodos. Suas arquiteturas especializadas misturadas para cada token apenas ativam 671B parâmetros 37B  Isso significa que cada GPU apenas precisa calcular                                                                                                                                                                                                                                      

```mermaid
graph TD
    subgraph ThreeD["3D Parallelism (Llama 3 405B)"]
        direction TB
        subgraph DP["Data Parallel (128-way)\nSplit batch across 128 groups"]
            subgraph PP["Pipeline Parallel (16-way)\nSplit layers across 16 stages"]
                subgraph TP["Tensor Parallel (8-way)\nSplit each layer across 8 GPUs"]
                    G1["GPU 1\nSlice of layers 1-N"]
                    G2["GPU 2\nSlice of layers 1-N"]
                    G8["GPU 8\nSlice of layers 1-N"]
                end
            end
        end
    end

    N1["Total: 8 x 16 x 128 = 16,384 GPUs"]

    style G1 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G2 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style G8 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style N1 fill:#1a1a2e,stroke:#e94560,color:#fff
```

## Construí-lo e realizei-o.
```figure
paged-kv-cache
```

## Construí-lo

### Passo 1: Simulação de paralelo de dados

Divida um lote em GPUs simuladas. Cada GPU calcula uma passagem para a frente em seu fragmento.

> A partir de agora, a CPU será dividida em GPUs em formato de imagem.

```python
import numpy as np

def simulate_data_parallelism(data, num_gpus, model_fn):
    batch_size = len(data)
    shard_size = batch_size // num_gpus
    remainder = batch_size % num_gpus

    gpu_losses = []
    gpu_gradients = []

    offset = 0
    for gpu_id in range(num_gpus):
        extra = 1 if gpu_id < remainder else 0
        shard = data[offset:offset + shard_size + extra]
        offset += shard_size + extra

        loss, grad = model_fn(shard)
        gpu_losses.append(loss)
        gpu_gradients.append(grad)

    avg_loss = np.mean(gpu_losses)
    avg_gradient = np.mean(gpu_gradients, axis=0)

    return avg_loss, avg_gradient
```

A operação total-redução (gradientes médios) é a única comunicação no paralelismo de dados. Na prática, isso usa a biblioteca NCCL nas GPUs NVIDIA, que implementa o ring all-reduce: cada GPU envia 1/N de seus gradientes para o seu vizinho, recebe 1/N do outro vizinho, e após N-1 passos cada GPU tem a média completa. Volume total de comunicação: 2 x gradiente_ tamanho x (N-1)/N, aproximando-se de 2x o tamanho do gradiente para grande N.

> A operação de integração total (NCCL) é a única comunicação na linha de dados. Na prática, esta utiliza a NCCL na GPU da NVIDIA, realizando a integração completa: cada GPU enviará 1/N da escala para o vizinho, recebendo 1/N de outro vizinho, N-1                                                                                                                                                                                                                                                                                                                                                                                                                                                      

### Passo 2: Simulação de paralelo de tensão

Divida uma matriz de peso entre GPUs. Cada GPU calcula uma multiplicação parcial de matriz. Combine os resultados.

> A partir de agora, o peso da matriz será dividido em várias GPUs.

```python
def simulate_tensor_parallelism(input_data, weight_matrix, num_gpus):
    d_in, d_out = weight_matrix.shape
    assert d_out % num_gpus == 0, f"d_out {d_out} not divisible by num_gpus {num_gpus}"
    shard_size = d_out // num_gpus

    partial_results = []
    for gpu_id in range(num_gpus):
        start = gpu_id * shard_size
        end = start + shard_size
        weight_shard = weight_matrix[:, start:end]

        partial = input_data @ weight_shard
        partial_results.append(partial)

    full_output = np.concatenate(partial_results, axis=-1)

    direct_output = input_data @ weight_matrix
    error = np.abs(full_output - direct_output).max()

    return full_output, error
```

O erro deve ser exatamente zero (ou epsilon de máquina). O paralelismo de tensão é matematicamente exato - produz o mesmo resultado que calcular o matmul completo em uma GPU. A divisão é ao longo da dimensão de saída, então cada GPU produz um pedaço diferente de colunas, e a concatenação reconstrui o resultado completo.

> 误差应恰好为零(或机器 epsilon) ――张量并行在数学上是精确的它产生与在一张GPU上计算完整矩阵乘法相同的结果──分拆沿输出维度进行,每个GPU 产生不同的列块,拼接重建完整结果──

Para camadas lineares paralelas de coluna (dividindo a dimensão de saída), você concatenar. Para linha paralela (dividindo a dimensão de entrada), você soma. Em um transformador FFN, o primeiro linear (expandir) usa coluna paralela e o segundo linear (contrato) usa linha paralela. Isso evita uma redução total entre as duas camadas.

> 对于列并行线性层(拆分输出维度),你拼接──对于行并行(拆分输入维度),你求和── 在变压器 FFN 中,第一个线性(扩展) 使用列并行,第二个线性(收缩) 使用行并行──这避免了两层之间的全归约──

### Passo 3: Simulação de paralelismo de oleodutos

Divide as camadas de um modelo em GPUs virtuais. Mostre o problema da bolha onde os estágios iniciais ficam inativos enquanto os estágios posteriores comemoram.

> A partir daí, o modelo será dividido em GPUs virtuais.

```python
def simulate_pipeline_parallelism(num_layers, num_stages, num_microbatches):
    layers_per_stage = num_layers // num_stages

    timeline = {}
    clock = 0

    for mb in range(num_microbatches):
        for stage in range(num_stages):
            start_time = max(
                timeline.get((stage, mb - 1, "fwd"), (0, 0))[1] if mb > 0 else 0,
                timeline.get((stage - 1, mb, "fwd"), (0, 0))[1] if stage > 0 else 0,
            )
            end_time = start_time + layers_per_stage
            timeline[(stage, mb, "fwd")] = (start_time, end_time)

    last_fwd_end = max(v[1] for v in timeline.values())

    for mb in range(num_microbatches - 1, -1, -1):
        for stage in range(num_stages - 1, -1, -1):
            deps = [last_fwd_end]
            if mb < num_microbatches - 1 and (stage, mb + 1, "bwd") in timeline:
                deps.append(timeline[(stage, mb + 1, "bwd")][1])
            if stage < num_stages - 1 and (stage + 1, mb, "bwd") in timeline:
                deps.append(timeline[(stage + 1, mb, "bwd")][1])
            start_time = max(deps)
            end_time = start_time + layers_per_stage
            timeline[(stage, mb, "bwd")] = (start_time, end_time)

    total_time = max(v[1] for v in timeline.values())
    compute_time = num_microbatches * num_stages * layers_per_stage * 2
    bubble_fraction = 1.0 - compute_time / (total_time * num_stages)

    return timeline, total_time, bubble_fraction
```

Com 4 fases e 1 micro-batch, a fração de bolhas é de 75% - três em cada quatro GPUs estão inativos a qualquer momento. Com 16 micro-batches, cai para cerca de 19%. O custo de eliminar bolhas é memória: você deve armazenar ativas para todos os micro-batches em voo simultaneamente.

> 4 fases e 1 micro-bots, a proporção de bolhas é de 75% Quartos de três GPUs  16 micro-bots                                                                                                                                                                                                                                               

### Passo 4: Calculador de memória

Calcular os requisitos de memória exatos para treinamento de qualquer tamanho de modelo.

> 計算訓練任意模型大小的精确显存需求──

```python
def memory_calculator(
    params_billions,
    precision_bytes=2,
    optimizer="adam",
    num_gpus=1,
    sharding="none",
    sequence_length=2048,
    batch_size_per_gpu=1,
    hidden_dim=None,
    num_layers=None,
):
    params = params_billions * 1e9

    weight_memory = params * precision_bytes

    if optimizer == "adam":
        optimizer_memory = params * 4 * 2
    elif optimizer == "sgd":
        optimizer_memory = params * 4
    else:
        optimizer_memory = 0

    gradient_memory = params * precision_bytes

    total_no_activation = weight_memory + optimizer_memory + gradient_memory

    if hidden_dim and num_layers:
        activation_per_layer = (
            sequence_length * batch_size_per_gpu * hidden_dim * precision_bytes * 4
        )
        activation_memory = activation_per_layer * num_layers
    else:
        activation_memory = params * precision_bytes * 0.5

    if sharding == "fsdp" or sharding == "zero3":
        weight_memory /= num_gpus
        optimizer_memory /= num_gpus
        gradient_memory /= num_gpus
    elif sharding == "zero2":
        optimizer_memory /= num_gpus
        gradient_memory /= num_gpus
    elif sharding == "zero1":
        optimizer_memory /= num_gpus

    per_gpu_total = weight_memory + optimizer_memory + gradient_memory + activation_memory

    return {
        "params_billions": params_billions,
        "weights_gb": weight_memory / 1e9,
        "optimizer_gb": optimizer_memory / 1e9,
        "gradients_gb": gradient_memory / 1e9,
        "activations_gb": activation_memory / 1e9,
        "per_gpu_total_gb": per_gpu_total / 1e9,
        "total_across_gpus_gb": per_gpu_total * num_gpus / 1e9,
        "fits_on_80gb": per_gpu_total / 1e9 <= 80,
        "num_gpus": num_gpus,
        "sharding": sharding,
    }
```

Esta calculadora responde à pergunta que cada engenheiro ML faz: "Quantas GPUs preciso?" Dê-lhe o tamanho do modelo e veja se cabe. Ajuste a estratégia de fragmentação até que o total por GPU cai abaixo de 80 GB.

> Este calculador responde a cada pergunta do engenheiro de ML: "Quantas GPUs preciso?"

### Passo 5: Simulação de Precissão Mista

Comparar o uso de memória entre FP32, FP16 e treinamento de precisão mista.

```python
def mixed_precision_comparison(params_billions):
    params = params_billions * 1e9

    fp32_weights = params * 4
    fp32_optimizer = params * 4 * 2
    fp32_gradients = params * 4
    fp32_total = fp32_weights + fp32_optimizer + fp32_gradients

    fp16_weights = params * 2
    fp16_master = params * 4
    fp16_optimizer = params * 4 * 2
    fp16_gradients = params * 2
    fp16_total = fp16_weights + fp16_master + fp16_optimizer + fp16_gradients

    mixed_weights = params * 2
    mixed_optimizer = params * 4 * 2
    mixed_gradients = params * 2
    mixed_total = mixed_weights + mixed_optimizer + mixed_gradients

    return {
        "fp32_total_gb": fp32_total / 1e9,
        "fp16_with_master_gb": fp16_total / 1e9,
        "mixed_bf16_gb": mixed_total / 1e9,
        "savings_vs_fp32": 1 - mixed_total / fp32_total,
    }
```

A maior surpresa para a maioria das pessoas: a precisão mista não reduz a metade da memória. Os estados do optimizador (m e v de Adam) permanecem em FP32 independentemente da precisão. Para um modelo 7B, o treinamento FP32 usa 112GB. A precisão mista usa 84GB. Isso é uma redução de 25% e não 50%.

> Para a maioria das pessoas, a maior incrível coisa é que a precisão misturada não reduzirá a metade a aparência.

## Use-o com o framework implementado.

### Executa todas as simulações

```python
def run_all_demos():
    print("=" * 70)
    print("DATA PARALLELISM SIMULATION")
    print("=" * 70)

    np.random.seed(42)
    data = np.random.randn(64, 32)
    weight = np.random.randn(32, 16)

    def model_fn(batch):
        output = batch @ weight
        loss = np.mean(output ** 2)
        grad = 2 * batch.T @ (batch @ weight) / len(batch)
        return loss, grad

    for n_gpus in [1, 2, 4, 8]:
        loss, grad = simulate_data_parallelism(data, n_gpus, model_fn)
        print(f"  {n_gpus} GPUs: loss={loss:.4f}, grad_norm={np.linalg.norm(grad):.4f}")

    print()
    print("=" * 70)
    print("TENSOR PARALLELISM SIMULATION")
    print("=" * 70)

    x = np.random.randn(4, 8192)
    W = np.random.randn(8192, 8192)

    for n_gpus in [1, 2, 4, 8]:
        output, error = simulate_tensor_parallelism(x, W, n_gpus)
        print(f"  {n_gpus} GPUs: output_shape={output.shape}, max_error={error:.2e}")

    print()
    print("=" * 70)
    print("PIPELINE PARALLELISM SIMULATION")
    print("=" * 70)

    for n_mb in [1, 4, 8, 16, 32]:
        _, total_t, bubble = simulate_pipeline_parallelism(32, 4, n_mb)
        print(f"  {n_mb:2d} micro-batches: total_time={total_t:4d}, bubble={bubble:.1%}")

    print()
    print("=" * 70)
    print("MEMORY CALCULATOR")
    print("=" * 70)

    configs = [
        (7, "none", 1),
        (7, "fsdp", 8),
        (70, "none", 1),
        (70, "fsdp", 8),
        (70, "fsdp", 16),
        (405, "fsdp", 64),
        (405, "fsdp", 128),
    ]

    print(f"  {'Model':>8} {'Sharding':>8} {'GPUs':>5} {'Per-GPU':>10} {'Fits 80GB':>10}")
    print("  " + "-" * 50)
    for params, shard, gpus in configs:
        result = memory_calculator(params, num_gpus=gpus, sharding=shard)
        fits = "Yes" if result["fits_on_80gb"] else "No"
        print(f"  {params:>6}B {shard:>8} {gpus:>5} {result['per_gpu_total_gb']:>8.1f}GB {fits:>10}")

    print()
    print("=" * 70)
    print("MIXED PRECISION COMPARISON")
    print("=" * 70)

    for params_b in [7, 13, 70, 405]:
        result = mixed_precision_comparison(params_b)
        print(f"  {params_b}B: FP32={result['fp32_total_gb']:.0f}GB, "
              f"Mixed BF16={result['mixed_bf16_gb']:.0f}GB, "
              f"Savings={result['savings_vs_fp32']:.0%}")
```

## Envia-o . Produto .

Esta lição produz`outputs/prompt-distributed-training-planner.md`-- um prompt que leva um tamanho de modelo e hardware disponível, e produz um plano de treinamento completo distribuído: estratégia de paralelismo, orçamento de memória, despesas gerais de comunicação e capacidade esperada.

## Exercícios.

1. Modifique a calculadora de memória para incluir o checkpointing de ativação. Com checkpointing, apenas armazenar ativações em cada camada K-th (típica K = 1, o que significa recomputar tudo). Mostre a troca de memória-computação: quanto memória o checkpointing salva e quanto ela retarda o treinamento (cerca de 33% mais computação para checkpointing completo)?

2. Extenda a simulação de paralelismo de pipeline para implementar o cronograma 1F1B (um para frente, um para trás) usado pelo PipeDream. Compare a fração de bolha com o cronograma ingênuo para 4 etapas e 8 micro-batches. O cronograma 1F1B deve ter uma memória de pico menor porque começa a passar para trás mais cedo.

3. Implemente um simulador de acumulação de gradientes. Em vez de reduzir todos após cada micro-parcela, acumule gradientes localmente para os passos K, e depois reduzir todos. Mostre como isso reduz a comunicação por K vezes, mas produz gradientes finais idênticos (e, portanto, treinamento idêntico).

4. Construir um estimador de custos. Dada a dimensão do modelo, o número de tokens alvo, o tipo de GPU (A100 em $2/hr, H100 at $A estratégia de paralelo estimou o custo total da formação em dólares.$100M, DeepSeek V3 cost ~$5,6M.

5. Adicione ZeRO-Offload à calculadora de memória. Suponha que a RAM da CPU seja de 512 GB por nó e NVMe seja de 2 TB. Mostre como o descarregar o optimizador para a CPU permite que um modelo 70B treine em 4 GPUs em vez de 16, ao custo de 30-50% de etapas de optimizador mais lentas.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Data parallelism | "Copy the model to every GPU" | Each GPU processes a different data shard; gradients are averaged via all-reduce after each step | 数据并行，每 GPU 处理不同数据分片，通过 all-reduce 平均梯度 |
| Tensor parallelism | "Split a layer across GPUs" | Partition weight matrices so each GPU computes part of the matmul; requires fast NVLink interconnect | 张量并行，拆分权重矩阵到多 GPU，需要 NVLink 互连 |
| Pipeline parallelism | "Split layers across GPUs" | Each GPU runs a different group of layers; data flows through the pipeline with micro-batches to reduce bubbles | 流水线并行，每 GPU 运行不同层组，用微批次减少气泡 |
| FSDP | "Shard everything" | Fully Sharded Data Parallel -- each GPU holds 1/N of weights, gradients, and optimizer states; all-gather before compute | 完全分片数据并行，每 GPU 持有 1/N 的参数/梯度/优化器状态 |
| ZeRO | "DeepSpeed's version of FSDP" | Zero Redundancy Optimizer with 3 stages: shard optimizer (Stage 1), + gradients (Stage 2), + parameters (Stage 3) | 零冗余优化器，三阶段分片：优化器→梯度→参数 |
| All-reduce | "Average across GPUs" | Collective operation where every GPU ends with the sum (or average) of all GPUs' inputs -- typically implemented as ring all-reduce | 全归约，所有 GPU 最终获得全局总和/均值 |
| All-gather | "Collect from all GPUs" | Collective operation where every GPU ends with the concatenation of all GPUs' data -- used in FSDP to reconstruct full parameters | 全收集，每 GPU 获得所有 GPU 数据的拼接 |
| Reduce-scatter | "Sum and distribute" | Collective operation that reduces (sums) data and scatters different chunks to different GPUs -- used in FSDP for gradient sharding | 归约散射，求和后分发不同块到不同 GPU |
| Mixed precision | "Train in half precision" | Use FP16/BF16 for forward/backward and FP32 for optimizer states -- saves ~25% memory, not 50%, because the optimizer dominates | 混合精度，前向/反向用 16 位，优化器用 32 位，省约 25% 显存 |
| Pipeline bubble | "Idle time in the pipeline" | Fraction of time GPUs sit idle waiting for data from the previous stage -- reduced by using more micro-batches | 流水线气泡，GPU 空闲等待前一阶段数据的比例 |

## Mais leitura 延伸阅读

- [Rajbhandari et al., 2020 -- "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"](https://arxiv.org/abs/1910.02054)- O DeepSpeed ZeRO paper que definiu as três etapas de fragmentação
- [Shoeybi et al., 2020 -- "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"](https://arxiv.org/abs/1909.08053)-- O paralelismo tensor da NVIDIA para transformadores
- [Narayanan et al., 2021 -- "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM"](https://arxiv.org/abs/2104.04473)-- Paralelo 3D combinando dados, tensor e pipeline
- [Zhao et al., 2023 -- "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel"](https://arxiv.org/abs/2304.11277)-- Implementação FSDP nativa da PyTorch
- [Llama 3 Technical Report](https://arxiv.org/abs/2407.21783)-- 16.384 GPU treinamento com detalhes de paralelismo 3D
- [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)-- como a arquitetura do MoE reduz o custo da formação em uma ordem de magnitude
