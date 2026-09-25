# Mitigação de início frio para LLM sem servidor .

> Uma imagem de modelo de 20 GB leva 5-10 minutos (7B) a 20+ minutos (70B) para passar de frio para servir. Num mundo sem servidores, isso não é um aquecimento, é uma interrupção. As mitigações operam em cinco camadas: imagens pré-seed nodes (Bottlerocket na AWS, arco de duplo volume), streaming de modelo (NVIDIA Run:ai Model Streamer, nativo no vLLM), instantâneos de memória da GPU (punto de verificação Modal, até 10 vezes mais rápido reinicialização), pools quentes (`min_workers=1`O Modal publica 2-4s de início frio como um piso; Baseten 5-10s padrão, subsegundo com pré-aquecimento. Esta lição ensina a medir, orçar e empilhar as cinco camadas.

> **【中文解读】**Esta secção apresenta estratégias de primeira resposta de atraso de Mestrado em Direito e Direito em Relações Internacionais.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

> - Não .**【前置】**O curso de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem
> - Não .**【类比】**• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Enumere as cinco camadas de mitigação do arranque a frio e nomeie uma ferramenta ou padrão em cada camada.
  Chinese: 列举冷启动缓解的五层策略,并说出每层一个工具或模式──
- Calcule o tempo total de arranque a frio como a soma de (provimento de nó) + (pesos de descarga) + (pesos de carga no HBM) + (motor init) para um modelo 70B.
  O que significa que o motor está em funcionamento?
- Explique por que a migração ao vivo transfere tokens de entrada (KB) e não cache KV (GB) e qual é a penalidade (recomputamento).
  Tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês
- Nomear a compensação de polas de aquecimento (pagar por GPU em inatividade ou aceitar coda de arranque a frio) e o limiar de SLA em que `min_workers > 0`torna-se obrigatório.
  Tradução do inglês para inglês:                                                                                                                                                                                                                                                           `min_workers > 0`变为强制性的 SLA 值──

## O problema é o problema da introdução

> **【中文解读】**O problema de início frio do LLM sem servidor: 70B 模型从零到服务需要 3-8 分钟(节点供应 45-60s + 容器拉取 120-300s +权重载 45-120s + 引擎初始化 10-30s), SLA de SLA.

> **【拓展：Serverless LLM 平台对比】**2026 anos Servidorless LLM 平台的冷启动表现:Modal 凭借 GPU 快照技术实现 2-4s冷启动(业界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不包含模型加载);GCP Cloud Run + GPU 较新,冷启动约15-30s──对于TTFT P99 < 60s 的 70B+ 模型,热池是强制性的没有任何冷启动优化能在60s内完成全流程──

O seu endpoint do LLM sem servidor sobe para zero durante a noite, às 8 da manhã, o tráfego aumenta.

> Seu sem servidor LLM 端点在夜间缩容到零.

1. Karpenter fornece um nó GPU: 45-60s.
   Carpentero 供给 GPU 节点:45-60 秒──
2. O recipiente tira uma imagem de 30 GB com pesos: 120-300s.
   Chinese: 容器拉取 30GB de contê-
3. O motor carrega pesos em HBM: 45-120s dependendo do tamanho do modelo e da velocidade de armazenamento.
   O motor vai carregar até HBM:45-120 segundos, dependendo do tamanho do modelo e da velocidade de armazenamento.
4. VLLM ou TRT-LLM inicializa gráficos CUDA, pool de cache KV, tokenizer: 10-30s.
   中文翻译:vLLM 或 TRT-LLM 初始化 CUDA graph、KV 缓存池、分词器:10-30 秒──

Total: 220-510s (cerca de 3-8 minutos) antes de um token voltar.`min_workers=1`Se o seu serviço tem 5 produtos cada com uma réplica quente, isso é 5 × 24 × 30 = 3.600 horas de GPU / mês, quer um único usuário tenha ou não chamado.

> 总计:220-510 秒(约 3-8 分钟)才能返回一个代币――你的SLA是2秒――你部署热池(`min_workers=1`O problema parece desaparecer, mas agora você está 24/7 para um GPU em branco. Se o seu serviço tiver 5 produtos em cada uma, é que 5 × 24 × 30 = 3.600 GPU-horas/mês, independentemente de ser útil para o usuário.

A mitigação do início frio é como manter a economia sem servidor enquanto se aproxima a latência do sempre-on.

> A redução do custo de funcionamento é a redução do custo de manutenção de um serviço sem servidor.

## O conceito central.

### Layer 1  imagens de nós pré-sementados (Bottlerocket)

> **【中文解读】**Primeiro nível  Pre-播种节点镜像──AWS Bottlerocket 双卷架构将操作系统与数据分离──将容器镜像(含模型权重) 预到数据卷快照中,在 `EC2NodeClass`O novo ponto foi iniciado em NVMe local, eliminando os passos de captura de imagem, poupando 2-4 minutos para grandes modelos.

Na AWS, a arquitetura de dois volumes do Bottlerocket separa o sistema operacional dos dados.`EC2NodeClass`. Novos nós de arranque com pesos já em local NVMe  passos 2 e parte de 3 desaparecem. Funciona com Karpenter nativo. Economia típica: 2-4 minutos por arranque a frio para modelos grandes.

> Na AWS, a estrutura de dois volumes do Bottlerocket irá separar o sistema operacional dos dados.`EC2NodeClass`中引用快照 ID──新节点启动时权重已在本地 NVMe 上步骤 2 和部分步骤 3 消除──原生与卡珀特尔 配合──典型节省:大型模型每次冷启动 2-4 分钟──

Equivalente no GCP: imagens personalizadas de VM com camadas de contêiner pré-cozadas. No Azure: instantâneos de disco gerenciados com o mesmo padrão.

> GCP 等价方案:预容器层的自定义 VM 镜像──Azure:托管磁盘快照加相同模式──

### Layer 2  streaming modelo (Run:ai Model Streamer)

> **【中文解读】**Segundo nível Modelo fluido de carga. NVIDIA Run:ai Model Streamer não precisa de todo o arquivo de carga.

Em vez de carregar o arquivo completo antes de responder ao primeiro pedido, transmita pesos para a memória GPU camada por camada e comece o processamento assim que o primeiro bloco de transformador estiver residente. O NVIDIA Run:ai Model Streamer é originário em vLLM 2026. Funciona com S3, GCS e NVMe local. Cortar o tempo de carga de peso em cerca de metade para modelos grandes por sobreposição de I / O com configuração de computação.

> Não precisa em resposta ao primeiro pedido pré-carregando o arquivo completo, mas em vez de carregando o peso por camadas para a memória do GPU, e em primeiro transformador blococarregamento termina imediatamente após começar a processar.

### Layer 3  Snapshots de memória GPU (Modal)

> **【中文解读】**O modelo em primeiro carregamento foi colocado em estado de GPU (peso, peso, gráfico CUDA, KV Cache) e foi reiniciado em 10x. Este é o método mais próximo para "reiniciar o GPU" em 2 segundos.

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减半权重加载时间) + (3) GPU 快照(消除重重加载) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM) ――全叠加将 70B 模型从 328s冷启降到约15s22x 改善──选择哪几层取决于SLA 严格程度和预算──

O Modal toma um ponto de verificação do estado da GPU (pesos, gráficos CUDA, região cache KV) após a primeira carga. Reinicializações subsequentes deserializam diretamente em HBM  10 vezes mais rápido do que reinicializando. Esta é a coisa mais próxima de "iniciar uma GPU quente em 2 segundos".

> Modal em primeira carga após o estado da GPU ⋅权重、CUDA graph、KV 缓存区域) fazer checkpoint──后续重启直接反序列化到HBM比重启动快10倍──这是2秒启动热 GPU"最接近的技术──代价:快照与 GPU 拓绑定,如果卡珀特搬迁到不同 SKU 需要重制快照──

### Layer 4  Piscinas quentes (min_workers=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026 ano Serverless LLM Plataforma de início a frio desempenho:Modal em GPU 快照技术实现 2-4s(业界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常10-30s(不含模型加载);原始 70B 模型冷启动 3-8 分钟。Modal 快照技术是关键差它将 GPU 状态(权重 + CUDA graph + KV Cache 区域)序列化,重启直反序列化到HBM,重启动快 10x。代价是快照与 GPU 拓绑定,迁移到不同 SKU 需要重制快照──

A redução mais simples: manter sempre uma réplica pronta. O custo é a taxa horária de uma GPU 24x7.$0.85-$1,50/hora para evitar um início frio de 30s) e gentil para os grandes (pagar $ 4 / hora para evitar um início frio de 5 minutos). O limiar SLA onde piscinas quentes se tornam obrigatórias: tipicamente TTFT P99 < 60s em um modelo 70B +.

> A solução mais simples é manter um duplicado sempre pronto. O custo é de uma GPU.$0.85-$1,50/小时 para evitar 30 segundos de início frio), o grande modelo é relativamente amigável(付 $4/小时 para evitar 5 minutos de início frio)。 temperatura da bateria para o SLA 值: normalmente é 70B + 模型上 TTFT P99 < 60 秒──

### Layer 5  Carregamento em camadas (ServerlessLLM)

O ServerlessLLM trata o armazenamento como uma hierarquia: NVMe (rápido, mas grande), DRAM (médio, mas com camadas), HBM (minúsculo, mas instantâneo). Pesos são pré-carregados para DRAM; carga a pedido para HBM. O papel relata redução de latência de 10-200x em cargas frias em comparação com o navio disco para HBM. A adoção da produção é precoce, mas integrações com vLLM existem.

> O servidorlessLLM irá armazenar em nível:NVMe(quase mas grande)、DRAM(médio mas dividido)、HBM(小但即时)。权重预载到DRAM;按需加载到HBM。论文报告冷启动延迟降低 10-200倍──生产采用尚早,但已存在与vLLM的集成──

### Layer 6  Migração ao vivo (patrão de bônus)

Quando um nó fica indisponível (deslocamento de pontos, drenagem de nós), o padrão tradicional é iniciar a replica em frio e fazer uma fila de solicitações de drenagem. A migração ao vivo move os tokens de entrada (kilobytes) para um destino que tem o modelo carregado e recompõe o cache KV no destino. A recomputada é mais barata do que transferir GB de cache KV pela rede. Aplicável para implementações desagregadas.

> Quando o ponto é indisponível quando o ponto é interrompido, o modo tradicional é iniciar em frio outro lado do seu código. O modo tradicional é iniciar em frio outro lado do seu código. O modo tradicional é iniciar em frio um outro lado do seu código. O modo tradicional é iniciar em frio um outro lado do seu código.

### A matemática da piscina quente

> **【中文解读】**热池数学:对于P99 TTFT SLA 为 2s的服务,问题不是"热池是/no"而是"多少热副本、哪些路径需要"──高价值交互路径(实时聊天、语音 Agent)→ min_workers=1-2;后台批处理路径(夜间分类)→ escala-to-zero 可接受;高级层级 → 按租户专用热副本。简单算术:5 个产品各 1热副本 = 5 × 24 × 30 = 3600 GPU-hours/月,无论有用户调用是否──

Para um serviço com P99 TTFT SLA de 2s, a questão não é "poalha quente sim/não" mas "quantas réplicas quentes, e quais caminhos obtê-los".

>  Para o P99 TTFT SLA para 2 segundos de serviço, a questão não é "quanta água é necessária"

- Caminhos interativos de alto valor (chat ao vivo, agente de voz): `min_workers=1-2`- Não .
  Tradução do inglês: High value交互路径 (高价值交互路径)`min_workers=1-2`- Não.
- Caminhos de batch de fundo (classificação noturna): escala a zero aceita, início a frio de 5 a 10 minutos tolerável.
  Tradução em inglês: 后台批处理路径 (后台批处理路径) 晚间分类: 接受缩容到零,5-10 分钟冷启动可容忍──
- Nível de prémio: `min_workers`por inquilino com capacidade específica.
  Tradução do inglês:`min_workers`专用容量──

### Messa antes de otimizar

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重到HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

Anatomia de arranque a frio para um modelo 70B num nó fresco (ilustre):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Números que você deve lembrar

- Começo a frio modal: 2-4 segundos (com instantâneos de GPU).
  Modal Coldstart: 2-4 segundos (Use GPU)
- Base de base de início a frio por defeito: 5 a 10 segundos; subsegundo com pré-aquecimento.
  Tradução do inglês: Baseten 默认冷启动:5-10 秒;预加热后亚秒级。
- Começo a frio de 70B: 3-8 minutos.
  Tradução do português: original 70B Cold start:3-8 分钟──
- Run:ai Modelo Streamer: ~ 2x aceleração de carga de peso.
  No entanto, o que não é um problema é que o usuário não pode fazer isso.
- Carregamento em camadas de ServerlessLLM: redução de 10-200x de latência (números de papel).
  O que é o problema?

## Use-o com o framework implementado.
```figure
cold-start-pipeline
```

## Usá-lo

`code/main.py`O relatório da Comissão sobre a aplicação do princípio da igualdade de oportunidades de trabalho e de emprego, que foi elaborado em 2002 e que foi publicado em 2002 e que foi publicado em 2002 e que foi publicado em 2002 e que foi publicado em 2002 e que foi publicado em 2002 e que foi publicado em 2002 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2006 e que foi publicado em 2007.

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自付自付的亏平衡请求率──

## Envia-o . Produto .

Esta lição produz`outputs/skill-cold-start-planner.md`- Tendo em conta o SLA, o tamanho do modelo e a forma do tráfego, escolhe quais as medidas de mitigação a empilhar.

> 本课产 出 `outputs/skill-cold-start-planner.md` Dedicar SLA  Modelo de grandeza e de fluxo de forma, escolher quais estratégias de alívio se superam.

## Exercícios.

1. Corra .`code/main.py`- Calcular a taxa de pedido de equilíbrio, acima da qual uma réplica quente é mais barata do que o pagamento do imposto de arranque a frio através de descontos adicionais de pedido no SLO.
   Tradução: 运行`code/main.py` calcular o montante do pagamento do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de início do pagamento em relação ao montante do imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de pagamento em relação ao imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto de imposto.
2. Você implanta um modelo 13B com P99 TTFT SLA de 3s. Escolha a pilha de mitigação mínima (menos camadas) que o atinja.
   中文翻译:你部署一个13B模型,P99 TTFT SLA 为 3 秒──选择实现它的最小缓解(最少层级)──
3. A pré-sementação de botelhas elimina a atração da imagem, mas os pesos ainda carregam da imagem para o HBM.
   O peso ainda precisa de ser carregado de forma rápida até o HBM.
4. O seu provedor sem servidor oferece instantâneos de GPU (Modal) e sua equipe recusa porque "snapshots vazam PII".
   Chinese:你的无服务器供应商提供 GPU 快照(Modal), mas a equipe recusou por causa da "快照泄露 PII"──辩论
5. Desenhe uma política de piscina quente em camadas: quantas réplicas quentes para usuários pagos, usuários de teste e cargas de trabalho em lote? Mostre a matemática.
   Chinese Translation: design separado estratégia: pagar usuário, usar usuário e processar trabalho em lote

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Mais leitura 延伸阅读

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) Os valores de referência e a arquitetura dos pontos de controlo publicados pela Modal.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) padrão de imagem de volume de dados pré-seeded.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) Pesos de sobreposição de carga com configuração de cálculo.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/) Manual de jogo de pré- aquecimento.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) Projeto de carga em camadas.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) migração ao vivo para as instalações desagregadas.
