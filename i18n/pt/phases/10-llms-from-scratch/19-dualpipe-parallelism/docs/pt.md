# DualPipe Paralelo 双向流水线并行

> O DeepSeek-V3 foi treinado em 2.048 GPUs H800 com especialistas em MoE espalhados por nós. O perito de comunicação trans-nodo custa uma hora de comunicação por cada hora de computação. As GPUs estavam inactivas metade do tempo. DualPipe (DeepSeek, Dec 2024) é um pipeline bidirecional que se sobrepõe computação para frente e para trás com as comunicações todos-a-todos que eles desencadeiam. A queda de bolhas, o aumento de rendimento e a manutenção de duas cópias de parâmetro do modelo (o "dual" que dá o nome) é barata uma vez que o Expert Parallelism já está espalhando especialistas entre as fileiras de qualquer maneira. Esta lição é um passo-a-passo do tipo Aprenda sobre o que a DualPipe realmente faz e por que o refinamento da Sea AI Lab em DualPipeV reduz o custo dos parâmetros 2x às custas de uma bolha marginalmente mais apertada.

> **【中文解读】**DeepSeek-V3 em 2048 张 H800 上训练,MoE 专家分布在节点间――跨节点-to-all 通信让 GPU 一半时间在等待――DualPipe é uma linha de fluxo de água em dois sentidos, que irá avançar/reversar com o sistema de comunicação em todos os sentidos, reduzir a burbuça, aumentar a transmissão――

> **【拓展：DualPipe→大规模训练】**DualPipe é a chave para o treinamento de alta eficiência do DeepSeek-V3: ele irá superponer a comunicação do MoE com o cálculo de frente/versão, tornando a eficiência do treinamento em 2048 caras quase linearmente expandida.

> - Não .**【前置】**学本节前请先掌握:Fase 10·05(Escalação Distribuída);MoE(Mixura de Especialistas) Conceptos;流水线并行(Pipeline Parallelism) Basis;Todo-a-Todo 通信模式。本节是Fase 10·20(DeepSeek-V3 Walkthrough) 的并行策略详解。

**Type:** Learn
**Languages:** Python (stdlib, schedule simulator)
**Prerequisites:** Phase 10 · 05 (distributed training, FSDP, DeepSpeed), Phase 10 · 14 (open-model architectures and MoE)
**Time:** ~60 minutes

## Objetivos de aprendizagem

- Nomear os quatro componentes de um pedaço DualPipe para frente e para trás e por que cada um tem sua própria janela de sobreposição.
  Explicar quatro componentes de blocos de DualPipe para frente e para trás e suas respectivas janelas de sobreposição
- Explique o problema da bolha de pipeline em escala e o que significa "sem bolhas" na prática versus no marketing.
   Explicar a grande quantidade de fluxos de água e a diferença entre a prática de "não-bububu" e a prática de marketing
- Rastrear um cronograma DualPipe à mão para 8 fileiras de PP e 16 micro-batches e confirmar os fluxos para frente e para trás preencher os espaços ociosos um do outro.
  Manuais rastreamento de 8 fases de PP e 16 pequenos lotes de DualPipe 调度, confirmar direção e reverso do fluxo preencher os espaços em branco uns dos outros
- Explique a compensação que o DualPipeV (Sea AI Lab, 2025) faz: deixa cair a replicação de parâmetros 2x ao custo de uma bolha ligeiramente maior quando o Expert Parallelism está inativo.
  Explicar o DualPipeV(Sea AI Lab, 2025)

## O problema é o problema da introdução

Treinar um modelo 671B MoE em GPUs H800 2k entra em três gargalos de engarrafamento:

1. **Memory pressure.**Cada GPU tem uma fatia do modelo. A memória de ativação em sequência 8k em 61 camadas em 128 cabeças é enorme.
2. **Pipeline bubbles.**O paralelismo tradicional de pipeline (GPipe, 1F1B) deixa as GPUs inativas enquanto esperam a entrada ou gradiente de seu estágio. Em 8 estágios, cerca de 12% do tempo da GPU pode ser bolha mesmo com a programação 1F1B.
3. **Cross-node all-to-all.**O MoE com paralelismo especialista espalha especialistas por todos os nós. Cada passagem avançada desencadeia um todo-a-todo para enviar tokens para seus especialistas e outro para combinar. Em GPUs de 2k isso facilmente se torna uma relação computação-comm 1:1.

> Em 2k H800 GPU 上训练 671B MoE 模型会遇到三个复合瓶:

1. **内存压力。**Cada GPU possui um pedaço de modelo. O número de sequências de 61 camadas e 128 cabeças é enorme.
   Tradução do inglês para tradução do inglês:                                                                                                                                                                                                                                                         
2. **流水线气泡。**传统流水线并行(GPipe、1F1B) Deixe a GPU esperar por sua fase de entrada ou gradiente时空──8 个阶段, mesmo usando 1F1B 调度, cerca de 12% do tempo da GPU 可能是气泡──
   Tradução do inglês para o inglês: Traditional streamwaterline并行让GPU在等待时空──8个阶段时,约12% de GPU 时间是气泡──
3. **跨节点全互联。**带专家并行 MoE 将专家分散到各节点──每次前向传播触发一次全互联将代币分发到专家,另一次将结果合并──2k GPU 时,这很容易变成 1:1的计算通信比──
   MoE 专家并行每次前向传播触发两次全互联通信, em 2k GPU 时计算通信比接近 1:1──

Cada uma delas tem soluções separadas: ponto de verificação de gradiente para memória, Zero Bubble (Sea AI Lab, 2023) para bolhas de pipeline, kernels de comunicação paralelas para todos. O que o DualPipe faz é fazê-los tocar juntos. O cronograma sobrepõe computação e comunicação dentro de um único pedaço para frente e para trás, injeta micro-partidas de ambas as extremidades do tubo simultaneamente e usa o cronograma resultante para esconder tudo dentro das janelas de computação.

Resultado relatado: quase eliminação de bolhas de pipeline, mais de 95% de utilização de GPU no treinamento de tokens de DeepSeek-V3 de 14,8T.

## O conceito central.

> **【中文解读】**DualPipe é um algoritmo de dupla direção de fluxo de água proposto pelo DeepSeek-V3, através de uma calculação de sobreposição entre a direção anterior e a direção reversa para maximizar a taxa de utilização da GPU. Comparado com a tradicional linha de fluxo de água única, DualPipe reduziu significativamente a flue de água.

> **【拓展：DualPipe 与 DeepSeek-V3 的效率】**DeepSeek-V3 em 2048 张 H800 GPUs, usando DualPipe + MoE 专家并行 + FSDP。DualPipe vai fluir em linha de gás de borbulha para cerca de 5% (cerca de 20%), é uma das principais técnicas de DeepSeek-V3 para treinar um modelo de topo de classe, com cerca de 560 milhões de dólares.


### Refrescar o paralelismo dos oleodutos

Dividir um modelo de camada N em dispositivos P. Dispositivo `i`mantém camadas `i * N/P .. (i+1) * N/P - 1`. Um micro-batch flui para a frente através dos dispositivos 0 a P-1, e depois para trás a partir de P-1 a 0. Cada dispositivo só pode iniciar a sua fase para a frente quando o dispositivo anterior envia a sua saída e só pode começar para trás quando o dispositivo a jusante envia o gradiente ascendente.

O GPipe (Huang et al., 2019) agenda um micro-batch por vez, o que desperdiça a maior parte do tempo da GPU. O 1F1B (Narayanan et al., 2021) interliga passes para frente e para trás para vários micro-partidos. A Bubble Zero (Qi et al., 2023) divide a passagem para trás em duas partes  para trás-para-entrada (B) e para trás-para-pesos (W)  e agenda-os para preencher a bolha. Depois da bolha Zero, o oleoduto está quase apertado.

O DualPipe é o próximo passo.

### Ideia 1: decomposição em pedaços

Cada peça à frente é dividida em quatro componentes:

- **Attention.**Projeções Q/K/V, atenção, projeção de saída.
- **All-to-all dispatch.**Comunicação transnacional que envia sinais aos seus especialistas.
- **MLP.**O cálculo do especialista do Ministério da Educação.
- **All-to-all combine.**Comunicação transnacional que traz resultados de especialistas de volta.

Um pedaço para trás adiciona versões de gradiente de cada um destes. DualPipe agendá-los de modo que o despacho de tudo para tudo ocorra em paralelo com o cálculo da atenção do pedaço seguinte, e o combinar tudo para tudo ocorre em paralelo com o cálculo MLP do pedaço seguinte.

### Ideia 2: programação bidireccional

A maioria dos cronogramas de oleodutos injeta micro-parches a partir do estágio 0 e fluem para o estágio P-1. DualPipe injeta micro-parches a partir de ambas as extremidades.

Para que isto funcione, dispositivo.`i`Deve manter ambas as camadas de tubo inicial `i`E a camada de tubo final.`P - 1 - i`. Essa é a parte "dual" da DualPipe: cada dispositivo mantém duas cópias das camadas de modelo que precisa servir (uma para cada direção). Na escala do DeepSeek-V3, este é um custo de replicação de parâmetros 2x. É acessível porque o Expert Parallelism já espalha os especialistas do MoE tão finos que replicar as camadas não-expertas duas vezes é uma pequena batata.

Crucialmente, o fluxo para frente em uma direção e o fluxo para trás na outra direção se sobrepõem exatamente onde as bolhas estariam num cronograma de uma direção.

### Um cronograma rastreado à mão

Considere P = 4 filetes, 8 micro-partidas, divididas 4 para frente / 4 para trás. O tempo se move de esquerda para direita; filetes são filetes de dispositivos.

```
           Time →
rank 0:  F1 F2 F3 F4  F5R F6R F7R F8R  B1 B2 B3 B4  ...
rank 1:     F1 F2 F3  F4/F5R F6R F7R   B1 B2 ...
rank 2:        F1 F2  F3/F5R F4/F6R    B1 ...
rank 3:           F1  F2/F5R F3/F6R    ...
```

Lendo a notação "F4/F5R": o rank 1 está a avançar para o micro-batch 4 ( indo de esquerda para direita no pipeline) E para a frente do micro-batch 5 ( indo de direita para esquerda) no mesmo intervalo de tempo.

Na posição 2 os fluxos cruzados se sobrepõem mais cedo, na posição 0 e P-1 eles se sobrepõem mais tarde. Na fase média estável do cronograma, cada posição corre para a frente de X-direção sobrepondo-se com para trás de Y-direção. O cálculo está ocupado.

### Contabilidade de bolhas

Bolha de condutores padrão 1F1B (tempo desperdiçado por categoria):

```
bubble_1F1B = (P - 1) * forward_chunk_time
```

O refinamento de bolhas zero leva-o para baixo, mas não para zero. DualPipe, na fase estável, tem bolha zero se a contagem de micro-batches for divisível por 2 vezes a profundidade do tubo. Fora da fase estável (calentamento e resfriamento), há alguma bolha, mas não cresce com o número de micro-batches  uma propriedade chave que o papel destaca.

Em termos de marketing: "sem bolhas". Em termos técnicos: bolhas não crescem com a contagem de micro-parcelas. A análise de acompanhamento do Sea AI Lab (DualPipeV / Cut-in-half) mostra a bolha zero completa somente quando o Expert Parallelism não é o gargalo de engarrafamento; com o EP-driven all-to-all, algum compromisso de agendamento está sempre presente.

### DualPipeV  o refinamento

Sea AI Lab (2025) observou que a replicação de parâmetros 2x é desperdiçosa quando a sobreposição de comunicações EP não é o ponto. O seu cronograma DualPipeV dobra a injecção bidirecional em um cronograma "de forma V" que funciona com uma única cópia de parâmetro. A bolha é um pouco maior que a DualPipe, mas a economia de memória é substancial. A DeepSeek adotou o DualPipeV em sua implementação de código aberto DualPipe como um modo de EP-off.

O compromisso:

| Feature | DualPipe | DualPipeV | 1F1B | Zero Bubble |
|---------|---------|-----------|------|------------|
| Param copies per device | 2 | 1 | 1 | 1 |
| Bubble vs micro-batches | constant | small growth | grows | grows |
| Compute-comm overlap | full | partial | minimal | partial |
| Use when | EP-heavy MoE | dense or EP-light | baseline | any pipeline |

### O que significa para uma corrida de tokens de 14,8T

O pré-treinamento do DeepSeek-V3 consumiu 14.8T de tokens em 2.048 GPUs H800 em aproximadamente 2,8 milhões de horas de GPU. Com 1F1B ingênuo, teriam perdido 12-15% disso para bolhas de tubo  340-420K GPU-hora, o suficiente para treinar um modelo completo de 70B. O DualPipe recuperou a maior parte disso. Quantificar diretamente a contribuição é difícil sem os registros internos, mas a afirmação no artigo é de mais de 95% de utilização de GPU em média em todo o treinamento.

Para corridas menores (menos de 1k GPUs), DualPipe é exagerado  bolhas de pipeline são menores em relação ao custo total, e o treinamento de modelo denso raramente atinge o gargalo de engarrafamento.

### Onde fica na pilha

- Complementar a **FSDP**(Fase 10 · 05). FSDP reduz os parâmetros do modelo em filas; DualPipe agenda o cálculo em filas.
- Compativel com **ZeRO-3**A contabilidade para a replicação de duas cópias precisa cooperar com os gradientes fragmentados do ZeRO.
- Requer**custom all-to-all kernels**Os kernels de código aberto do DeepSeek são a implementação de referência.


> **【拓展：流水线并行的工程细节】**DualPipe em uma mesma direcção, em troca de direção e direção, a taxa de bolhas de vapor irá diminuir de cerca de 20% para cerca de 5%.


## Use-o com o framework implementado.
```figure
expert-capacity
```

## Usá-lo

`code/main.py`É um simulador de cronograma de pipeline.`(P, n_micro_batches, schedule)`O sistema de produção de energia de alta velocidade é um sistema de ensino que permite a utilização de uma fase estável para cada um dos sistemas 1F1B, Zero Bubble, DualPipe e DualPipeV.

O valor do simulador: executá-lo com diferentes contagens de P e micro-batches e observe como a fração da bolha cresce para 1F1B, mas não para DualPipe.

Considerações de integração para uma formação real:

- Escolha uma profundidade paralela ao pipeline que se divide claramente em sua contagem de micro-batches.
- Certifique-se de que a sua malha paralela de especialistas suporta tudo-a-todo bidirecional.
- Espera que a primeira vez que o fizeres, queiras uma semana de tempo de depuração no próprio cronograma.
- Monitore a utilização da GPU por classificação, não apenas agregada.

## Envia-o . Produto .

Esta lição produz`outputs/skill-dualpipe-planner.md`. Tendo em conta a especificação do cluster de formação (contagem de GPU, topologia, interconexão, forma do modelo), recomenda uma estratégia de paralelismo de canais, o algoritmo de programação a utilizar e a fração de bolhas esperada na escala-alvo.

> 本课产 出 `outputs/skill-dualpipe-planner.md` Formas de formação e de formação (GPU), que recomendam estratégias de fluxo de água e de regulação de algoritmos e a proporção de bolhas de previsão na escala de objetivos.

## Exercícios.

1. Corra .`code/main.py`- Não .`(P=8, micro_batches=16, schedule=dualpipe)`E ...`(P=8, micro_batches=16, schedule=1f1b)`Calcule a diferença de utilização da GPU e expresse-a como horas de GPU recuperadas por milhão de tokens de treinamento.
   Tradução:`(P=8, micro_batches=16, schedule=dualpipe)`和 `(P=8, micro_batches=16, schedule=1f1b)`上运行 `code/main.py`◊ calcular GPU utilization rate diferença并表示为每百万训练代币回收的 GPU 小时数──

2. Esboçar a tabela de horário para `(P=4, micro_batches=8, schedule=dualpipe)`Marque cada espaço horário com a identificação e direcção do micro lote. Identifique o primeiro espaço horário onde as bolhas estão ausentes.
   Tradução do português:`(P=4, micro_batches=8, schedule=dualpipe)`O programa de regulação. Marca o primeiro tempo em que a bolha desaparece.

3. Leia a Figura 5 do relatório técnico do DeepSeek-V3 (arXiv:2412.19437). Identifique a janela de sobreposição para o despacho de todos para todos dentro de um pedaço de DualPipe para a frente. Explique como o cronograma de computação o esconde.
   Tradução do inglês:PDF, tradução do inglês: DeepSeek-V3 技术报告图 5――识别 DualPipe 前向块内所有调度的重叠窗口――解释计算调度如何隐藏它――

4. Calcule o custo de 2x do parâmetro de DualPipe para um modelo denso de 70B com estágios de oleoduto P=8 e um modelo de MoE de 671B com estágios de oleoduto P=16. Mostre por que o custo de um caso de MoE é proporcionalmente menor (a maioria dos parâmetros são especialistas, divididos em um grande grupo de EP).
   O modelo de distribuição de energia é um dos principais componentes da economia do país.

5. Compare DualPipe com Chimera (um agendador bidirecional concorrente a partir de 2021). Identifique as duas propriedades específicas que DualPipe acrescentou que a Chimera não tinha, usando a Seção 3.4 do papel como referência.
   Chinese: 拼音:比较 双管与 Chimera (双管与 Chimera)  ([[2021年竞争双向调度器]])  ([[2021年]] 竞争双向调度器)  ([[2021年]] 竞争双向调度器)  ([[2021年]] 竞争双管双向调度器) ]] 识别 双管 添加的 Chimera 没有的两个特定属性,使用论文第3.4 节作为参考──

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Pipeline bubble | "Idle time per rank" | GPU cycles wasted because a pipeline stage is waiting for its input or gradient | 流水线气泡，GPU 等待输入或梯度时空转的周期 |
| 1F1B | "Default pipeline schedule" | One forward / one backward interleaved scheduling; the baseline DualPipe beats | 1F1B 调度，一前向一反向交替 |
| Zero Bubble | "Sea AI Lab 2023" | Splits backward into B (input gradient) and W (weight gradient); almost fully tightens the pipeline | 零气泡，将反向拆为输入梯度和权重梯度 |
| DualPipe | "DeepSeek-V3 schedule" | Bidirectional pipeline + compute-comm overlap; bubbles do not grow with micro-batch count | DualPipe，双向流水线+计算通信重叠 |
| DualPipeV | "Cut-in-half" | V-shape refinement that drops the 2x parameter replication at the cost of slightly larger bubbles | DualPipeV，取消 2x 参数复制，气泡略增 |
| Chunk | "Unit of pipeline work" | A forward or backward pass of one micro-batch through one pipeline stage | 块，一个微批次在一个流水线阶段的前向/反向 |
| All-to-all dispatch | "Send tokens to experts" | Cross-node comm that routes tokens to their assigned MoE experts | 全互联分派，将 token 路由到 MoE 专家 |
| All-to-all combine | "Bring expert outputs back" | Cross-node comm that gathers expert outputs after the MLP | 全互联组合，收集专家输出 |
| Expert Parallelism (EP) | "Experts across GPUs" | Shards MoE experts across ranks so different GPUs hold different experts | 专家并行，不同 GPU 持有不同 MoE 专家 |
| Pipeline Parallelism (PP) | "Layers across GPUs" | Shards model layers across ranks; the dimension DualPipe schedules | 流水线并行，模型层分布在不同 GPU |
| Bubble fraction | "Wasted GPU time" | (bubble_time / total_time); the fraction DualPipe drives toward zero | 气泡比例，DualPipe 将其压向零 |

## Mais leitura 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437), Section 3.3.2 and Figure 5](https://arxiv.org/abs/2412.19437) a referência principal de DualPipe
- [DeepSeek — DualPipe GitHub repository](https://github.com/deepseek-ai/DualPipe) a implementação de referência de código aberto, incluindo o modo DualPipeV (Cut-in-half)
- [Qi et al. — Zero Bubble Pipeline Parallelism (arXiv:2401.10241, Sea AI Lab 2023)](https://arxiv.org/abs/2401.10241) O antecessor da Bolha Zero
- [Sea AI Lab — DualPipe could be better without the Dual](https://sail.sea.com/blog/articles/63) a análise DualPipeV que informou o modo de desativação do EP da DeepSeek
- [Narayanan et al. — PipeDream / 1F1B (arXiv:1806.03377, 2018-2021)](https://arxiv.org/abs/1806.03377) o calendário 1F1B comparado com o DualPipe
- [Huang et al. — GPipe (arXiv:1811.06965, 2018)](https://arxiv.org/abs/1811.06965) o problema original de paralelismo de papel e bolha
