# VLLM Servings Internal: PagedAttention, Continuous Batching, Chunked Prefill.
# Servidores internos do motor  PagedAttenção, Batch contínuo, Preenchimento em pedaços

> A capacidade moderna do motor de serviço baseia-se em três defeitos compostos, não num único truque. PagedAttention está sempre ligado. A batch contínua injeta novos pedidos no lote ativo entre iterações de decodificação. As fatias de preenchimento em pedaços são longas, para que os tokens de decodificação nunca morram de fome. Ligue os três e um Llama 3.3 70B FP8 em um H100 SXM5 empurra 2.200-2.400 tok/s em 128 torque simultâneo  cerca de 25% acima do próprio padrão do vLLM e 3-4x um ciclo PyTorch ingênuo. Esta lição lê o programação e o núcleo de atenção de vLLM  o motor de referência para todas as três técnicas  em um nível que você pode diagramar, e termina com um batch contínuo de brinquedo em `code/main.py`que os horários preenchem e decodificam como o VLLM faz.

> **【中文解读】**VLLM em 2026 dominação baseado em três compostos optimização:PagedAttention(分页注意力)始终开启;连续批处理在解码代间注入新请求;分块预填片长提示以防止解码 Token 饥饿。三者全开时,Llama 3.3 70B FP8 在单卡 H100 上以 128 并发达2,200-2,400 tok/s比朴素 PyTorch 循环快 3-4 倍──

> **【拓展：vLLM → LLM 推理服务标准】**VLLM é o mais popular open source LLM 推理服务引擎 em 2026 PagedAttention 借借操作系统的虚拟内存分页思想管理 KV Cache,将碎片率控制在4% 以下──连续批处理允许在解码步骤间动态加入新请求,大幅提高GPU利用率── é uma técnica essencial do MLM no âmbito do desenvolvimento ambiental.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**O que é o "Fase 11·12" do "Fase 12" do "Fase 11" do "Fase 12" do "Fase 11" do "Fase 12" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 11" do "Fase 12" do "Fase 11" do "Fase 12" do "Fase 12" do "Fase 11" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12" do "Fase 12 "Fase 12" do "Fase 12" do "Fase 12 "Fase 12" do "Fase 12" do "Fase 12 "Fase 12 " do "Fase 12" do "Fase 12 " do "Fase 12" do "Fase 12 " do "Fase 12 " do "Fase 12" do "Fase 12 " do " do "Fase 12 " do "Fase 12 " do "Fase 12 " do " do "Fase 12 " do "Fase 12 " do " do " do " do "Fase 12 " do "Fase 12 " do " do "Fase 12 " do "Fase 12 " do " do "Fase 12 " do " do " do " do "Fase 12 " do " do " do " do " do "F
> - Não .**【类比】**VLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache(像操作系统虚拟内存分页,碎片率 < 4%);Continuous Batching = 动态拼单(新请求随时插入运行批);Chunked Prefill = 切长快速(长输入切片避免阻塞解码)。Llama 3.3 70B FP8 em H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 ⋅倍

## Objetivos de aprendizagem

- Explique PagedAttention como um alocador de cache de KV: blocos, tabelas de blocos e por que a fragmentação permanece abaixo de 4% na carga de produção.
  Tradução do inglês para "PageedAttention" (em inglês)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
- Diagrama de batches contínuos no nível de iteração: como as sequências acabadas deixam o lote e as novas se juntam sem drenar.
  Tradução do inglês em chinês: 代级别绘制连续批处理:已完成的序列如何离开批次,新序列如何加入而无需清空──
- Descreva preenchimento em pedaços numa frase e nomear qual métrica de latência protege (indicação: é cauda TTFT, não significa transferência).
  O que é que o TTFT é?
- Nomear o 2026 vLLM v0.18.0 gotcha que morde equipes possibilitando toda otimização de uma só vez.
  Chinese:                                                                                                                                                                                                                                                              

## O problema é o problema da introdução

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批处理将所有请求填充到最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV Cache 碎片率从60-80% 降至4% 以下) 连续批处理(在解码代间动态加入新请求) 分块预填充(将长提示切片以防止解码饥饿) 

Um ciclo de serviço PyTorch ingênuo executa uma solicitação por vez: tokenize, prefill, decode até EOS, retornar. Em um usuário, isto funciona. A 100 é uma fila de pacientes. A solução óbvia  batching estático  pads cada solicitação para o prompt mais longo na janela, pads cada decodificação para a saída mais longa esperada, e impede o lote inteiro na sequência mais lenta. Pagas por tampas que nunca usas, e pedidos rápidos esperam para pedidos lentos.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填充、解码直到EOS、返回──一用户时时这行通──一百用户时,这就是一排耐心等待的人──显然修复静态批处理将每个请求填充到窗口中最长的提示,将每个解码填充到最长的预期输出,将每个解码填充到最长的预期输出,整个批次等待最慢的序列──你为未使用的填充单,快速请求等待缓慢请求──

O vLLM resolve três problemas de uma só vez. PagedAttention impede a fragmentação do cache KV de consumir 60-80% da memória da GPU da maneira que a alocação contígua clássica faz. Batching contínuo permite que os pedidos se juntem e deixem o lote entre cada iteração de decodificação, de modo que o lote está sempre cheio de trabalho real. O preenchimento em pedaços quebra um token de 32k em ~512 tokens que se interagem com a decodificação, de modo que um longo prompt não congela cada token de decodificação na GPU.

> VLLM uma vez resolveu três problemas. Atensão pagada bloqueia KV 缓存碎片像经典连续分配那样吞 60-80% de GPU 内存. Continuous批处理让请求在每个解码代之间加入和离开批次,所以批次总是充满真实工作. 分块预填将32K token的提示切成512 token的提示片段,与解码交换进行,所以长提示不会结 GPU 上的每个解码 token.

O padrão de produção 2026 está todos os três ligados. Você precisa entender o que cada um faz porque os modos de falha estão todos no agendador, não no modelo.

> A configuração padrão de produção de 2026 é de três tipos. Você precisa saber o que cada um faz, porque os padrões de falha estão no regulador, e não no modelo.

## O conceito central.

### PagedAttention como um sistema de memória virtual

> **【中文解读】**PagedAttention 借借鉴操作系统虚拟内存分页思想管理 KV Cache。 tradicional distribuição continuada para cada sequência pré-distribuição máxima longitud(como 8192 tokens), mas a solicitação média apenas com 1500 tokens, desperdiçar 82% de HBM。 PagedAttention divide KV Cache em blocos fixos de grande dimensão(默认 16 tokens), cada sequência tem um bloco de mapeamento lógica posição para blocos físicos ID, distribuição por necessidade, porcentagem de fragmentos inferior a 4%。 é o único distribuidor vLLM, através`--gpu-memory-utilization`(默认 0.9) control KV Cache disponível HBM

> **【拓展：KV Cache 内存管理演进】**KV Cache 内存管理 passou por três gerações de desenvolvimento: 1) 连续预分配简单但浪费60-80% 内存; 2) PagedAttention(vLLM 2023)分页管理,碎片率 <4%,成为行业标准; 3) RadixAttention(SGLang 2024)                                                                                                                                                                                                                          

Um cache KV é `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`Para Llama 3.3 70B em 8192 tokens, que é aproximadamente 1,25 GB por sequência em BF16. Se você reservar 8192 slots para cada solicitação, mas a solicitação média usa apenas 1500 tokens, você desperdiça cerca de 82% do HBM reservado.

> Cada sequência de KV 缓存大小为 `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element` Llama 3.3 70B em 8192 tokens 时, BF16 下每个序列约 1.25 GB── Se você tiver 8192 槽位预留留为每一个请求, mas uma solicitação média apenas com 1500  टोकens, você perderá cerca de 82% 预留的HBM──

PagedAttention empresta a ideia da memória virtual do sistema operacional. O cache KV não é contiguo por sequência. É alocado em blocos de tamanho fixo (tokens 16 por defeito). Cada sequência tem uma tabela de blocos que mapeia suas posições lógicas de token para IDs de blocos físicos. Quando uma sequência cresce além dos blocos alocados, mais um bloco é adicionado. Quando termina, seus blocos retornam ao pool.

> PagedAttention 借借借操作系统虚拟内存的思想──KV 缓存不是每个序列连续的──它以固定大小的块──默认16代币) 分配──每个序列有一个块表,将逻辑代币 位置映射到物理块 ID──当序列增长超过已分区时,添加一个新块──完成后,块返回池──

A fragmentação cai de 60-80% (clássico) para menos de 4% (Attenção Pagada).`--gpu-memory-utilization`(padrão 0.9), que indica à vLLM quanto HBM deve reservar para blocos KV após pesos de carga e ativas.

> 碎片率 de 60-80% (经典) reduziu-se a 4% abaixo (PageAtention)`--gpu-memory-utilization`(默认 0.9), diga à VLLM em carga de peso e ativar depois para KV blocos de reserva de quanto HBM.

### Batchamento contínuo no nível de iteração

> **【中文解读】**连续批处理在每个解码步骤之间做出接受/释放决策──每个代:(1) 移除已完成的序列;;((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

A velha "batchagem dinâmica" esperava uma janela (digamos 10 ms) para encher um lote, em seguida, executou prefill + decode + decode + decode + até que cada sequência terminasse.

> 旧的"动态批处理" espera uma janela (((tal como 10ms) para preencher os lotes, então executa prefill + decode + decode + decode até que cada sequência seja concluída;;

A batchagem contínua opera entre cada etapa de decodificação.`RUNNING`Em cada iteração:

> 连续批处理在每个解码步骤之间操作―― será chamado de conjunto de processos em execução `RUNNING`列表──每次代:

1. Qualquer sequência em `RUNNING`que apenas acerta EOS ou max_tokens é removido.
   Tradução:`RUNNING`Qualquer sequência de tokens de EOS ou max_tokens é removida.
2. O programador olha para a fila de espera. Se houver blocos KV livres, ele admite novas sequências (preencher ou retomar).
   Se houver um bloco de KV, ele recebe uma nova sequência (pre-reemplenha ou recuperação).
3. O passe para a frente corre em qualquer coisa que esteja agora dentro .`RUNNING`, emitindo um novo token por sequência.
   Tradução do português: 前向传播对`RUNNING`Todos os conteúdos estão em funcionamento, cada sequência é emitida um novo token.

O tamanho do lote nunca é empolhado para um número fixo. Sequências em diferentes posições em sua saída compartilham um fundido para a frente.`V1 scheduler`. A invariante chave: o programador é executado uma vez por iteração de decodificação, não uma vez por solicitação.

> 批次大小从不填充到固定数字――输出不同位置的序列共享一次融合前向传播――2026 vLLM 中称为 `V1 scheduler`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                               

### Preenchimento em pedaços protege a cauda TTFT

> **【中文解读】**O preenchimento de blocos resolveu o problema de "结" de outros sequências de decodificação. Um token de 32K requer cerca de 800ms de preenchimento em um modelo 70B, enquanto todos os outros sequências de token de decodificação estão esperando.

> **【拓展：vLLM 生产部署最佳实践】**A configuração da produção de produtos de base do VLLM para 2026 inclui:`--gpu-memory-utilization 0.9`预留 90% HBM 给 KV Cache;(2) `--max-model-len` De acordo com a configuração de necessidades reais e não o valor máximo padrão;(3) 分块预填充默认开启但与某些推测解码模式不兼容;(4) `--enable-prefix-caching`Em RAG/Agente 场景下可大幅减少重复预填;5) Prometheus 指标端点用于监控队列深度和 KV利用率──

O prefill é computacional. Um prompt de 32k-token no Llama 3.3 70B leva ~800 ms de prefill puro em um H100. Enquanto prefill executa, decodifica tokens para cada outra sequência na bateria de espera. Em um loop de serviço, a latença de primeiro token (TTFT) de um longo prompt se torna o blip de latença inter-token (ITL) para dezenas de outros usuários.

> O preenchimento é um tipo de cálculo intenso. O Llama 3.3 70B para um token de 32K requer cerca de 800ms de preenchimento em uma única H100. Quando o preenchimento é realizado, todos os outros tokens de decodificação da sequência estão esperando. No ciclo de serviço, o primeiro token de um longo token de atraso (TTFT) se transformou em uma dúzia de outros tokens de usuários.

O prefill fragmentado divide o prefill em pedaços de tamanho fixo (tokens padrão 512) e agenda cada pedaço como uma unidade. Entre pedaços o cronista pode avançar as sequências de decodificação em um token. Você troca um pequeno hit de latência de prefill absoluta (alguns ms por pedaço) por um jitter de tempo de decodificação muito menor. P99 ITL sob carga mista cai de ~ 50 ms para ~ 15 ms em benchmarks publicados.

> O módulo pode ser preenchido em blocos de tamanho fixo (conhecido como 512 tokens), cada bloco como um módulo de módulo.

### Os três padrões interagem

As três características assumem-se mutuamente. PagedAttention dá ao cronista um recurso KV de grãos finos para negociar contra. Batchings contínuos necessitam de esse recurso de grãos finos para que a admissão de uma nova sequência não força uma reorganização global. Preenchimento em pedaços é uma decisão que o cronista faz sobre o mesmo .`RUNNING`Lista  é mais uma política de agendamento, não um sistema separado.

> Três características interdependentes. A atenção pagada para o regulador fornece recursos de KV de pequena dimensão para a regulação.`RUNNING`A decisão feita na lista é outra estratégia de regulação, não um sistema independente.

Não é preciso conhecer todas as bandeiras, é preciso saber o que o programador otimiza: um bom rendimento sob o orçamento do bloco KV, sujeito a cortes de pré-enchimento em pedaços.

> Você não precisa saber cada sinal. Você precisa saber o que é o melhor.

### O 2026 v0.18.0 tem-te

> **【中文解读】**VLLM v0.18.0 中 não pode ser ativado simultaneamente `--enable-chunked-prefill`和 modelo de projeto 推测解码`--speculative-model`O único excepção é o N-gram GPU 推测解码 no V1 调度器. Não leia a nota de lançamento sobre a abertura de todos os sinais de otimização.

Em vLLM v0.18.0 não pode combinar `--enable-chunked-prefill`com decodificação especulativa de modelo de projecto (`--speculative-model`)). A exceção documentada é a descodificação especulativa da GPU de N-gram no cronógrafo V1. As equipes que deslizam todas as bandeiras sem ler as notas de lançamento recebem um erro no tempo de execução no início, não uma regressão suave. Se o seu ganho especulativo valeria a pena permitir preenchimento em pedaços, revisite a escolha  a resposta correta em 2026 é muitas vezes EAGLE-3 sem preenchimento em pedaços, não um modelo de projeto mais preenchimento em pedaços que não compila.

> Em vLLM v0.18.0, você não pode ativar simultaneamente `--enable-chunked-prefill`和 modelo de projeto 推测解码`--speculative-model`O sistema de análise de dados é um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

### Números que você deve lembrar

- Llama 3.3 70B FP8, H100 SXM5, 128 simultâneos, todos os três em: 2.200-2.400 tok/s.
  Llama 3.3 70B FP8, H100 SXM5,128 并发,三个优化全开:2,200-2,400 tok/s。
- O modelo é o mesmo, vLLM padrão (sem preenchimento em pedaços): ~1.800 tok/s.
  Não há nenhum bloco de preenchimento.
- O mesmo modelo, o ciclo PyTorch avançado ingênuo: ~600 tok/s.
  Tradução do inglês para inglês: 同模型,朴素 PyTorch 前向循环:約600 tok/s。
- Resíduos de fragmentação de KV no âmbito da PagedAttention na carga de produção: < 4%.
  中文翻译:PagedAttention 在生产负载下 KV 碎片浪费:<4%──
- P99 ITL sob carga mista: ~ 15 ms com preenchimento em pedaços, ~ 50 ms sem.
  Tradução do inglês: P99

### Como é que o cronograma

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`É exatamente esse ciclo no stdlib Python com contagens de tokens falsas e latência avançada falsa.

> `code/main.py`É a base de padrões pura do Python implementado neste ciclo, usando o contato de tokens falsos e o contato de tokens falsos.

## Use-o com o framework implementado.
```figure
tensor-parallel
```

## Usá-lo

`code/main.py`Simula um programação de estilo vLLM com recursos com alternância.

> `code/main.py`模拟一个带有可换功能的 vLLM 风格调度器──运行

- `NAIVE`modo: uma solicitação por vez, sem lotes.
  Tradução:`NAIVE`模式: uma vez, uma solicitação, não é processada em lote.
- `STATIC`modo: pad e espera, batchagem clássica.
  Tradução:`STATIC`模式: fill fill fill并等待, classical batch processing。
- `CONTINUOUS`Modo: admissão e liberação a nível de iteração.
  Tradução:`CONTINUOUS`Modelo: 代级的接收和释放──
- `CONTINUOUS + CHUNKED`modo: preencher as fatias entrelaçadas com decodificação.
  Tradução:`CONTINUOUS + CHUNKED`模式: pré-reemplenhação de pedaços de papel e desenho de papel.

A saída mostra o rendimento total (tokens por segundo virtual), média TTFT e P99 ITL.`CONTINUOUS + CHUNKED`A linha deve dominar o tráfego misto.

> 输出显示总吞吐量(每虚拟秒代币 数) 、TTFT 平均值和 P99 ITL。`CONTINUOUS + CHUNKED`O número de pessoas que se encontram em situação de risco é de aproximadamente 0,5% do total.

## Envia-o . Produto .

> **【拓展：LLM 推理引擎对比】**2026 ano LLM 推理引擎包括:vLLM(通用生产默认,PagedAttention+连续批处理) √SGLang(前共享优化,RadixAttention) √TensorRT-LLM(NVIDIA 专属,Blackwell 上吞吐最高) √Llama.cpp(CPU/边缘,GGUF 格式) √选择取取于硬件(CPU/GPU/Hopper/Blackwell) √工作负载(通用聊天/Agent/RAG) 和合规要求自(托管/云托管) √LLM √60% de produção de depósitos √2026 基于 AI 基础设施调查) √

Esta lição produz`outputs/skill-vllm-scheduler-reader.md`. Dada uma configuração de serviço ( tamanho de lote, utilização de memória KV, tamanho de preenchimento em pedaços, configuração especulativa), produz um diagnóstico de cronograma que indica quais dos três padrões são os gargalos de engarrafamento e quais a ajustar.

> 本课产 出 `outputs/skill-vllm-scheduler-reader.md` fornecer serviços de configuração (Bot次大小、KV 内存利用率、分块预填大小、推测配置), que gera o diagnóstico do regulador, indicando qual das três preferências é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o é.

## Exercícios.

1. Corra .`code/main.py`- Comparar .`STATIC`- Não .`CONTINUOUS`Em que se deve a diferença de rendimento entre a eficiência de preenchimento, a eficiência de decodificação ou a latência de cauda?
   Tradução: 运行`code/main.py`◊ em combinação de longos e curtos pedidos de trabalho`STATIC`和 `CONTINUOUS`◊ Diferença de transmissão de que é que a eficiência de preenchimento, a eficiência de decodificação ou o atraso final?
2. Modificar o cronograma de brinquedos para adicionar `--max-num-batched-tokens`Qual é o valor correto para um H100 com Llama 3.3 70B FP8? (Punta: é uma função do tamanho do bloco KV e do número de blocos livres, não de HBM bruto).
   Tradução do inglês: Modificar`--max-num-batched-tokens` H100 运行 Llama 3.3 70B FP8 正确值是多少?
3. Leia novamente as notas de lançamento do vLLM v0.18.0. Que combinações de bandeiras são mutuamente exclutivas?
   中文翻译:重新读 vLLM v0.18.0 发布说明──哪些标志组合互斥?列出它们──
4. Calcule o desperdício de fragmentação do cache KV para uma traça de 1.000 solicitações com 1500 tokens de saída médias, std 600 tokens, sob (a) alocação contígua por solicitação em 8192 max, (b) PagedAttention com blocos de 16 tokens.
   Chinese:计算 1,000 个请求的 KV 缓存碎片浪费(均值 1,500 输出代币,标准差 600),在 (a) 最大 8192 的连续每请求分配和 (b) 16 token 块的 PagedAttention 下。
5. Explique num parágrafo por que o preenchimento em pedaços ajuda o P99 ITL mas não a produção isolada.
   Tradução do inglês: using a fragmentation explains why分块预填充 helps P99 ITL, but not alone raise throughput.

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Mais leitura 延伸阅读

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) fonte oficial sobre compatibilidade com preenchimento em pedaços e decodificação especulativa.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026 liberação de cadência e comportamento específico de versão.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) o texto original que ainda define como pensar sobre o alocador.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) Análise de fragmentação e projeto de programação.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) A programação detalhada do V1 com gráficos de chama.
