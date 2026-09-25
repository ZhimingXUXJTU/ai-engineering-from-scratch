# GPU Autoescala em Kubernetes  Karpenter, KAI Scheduler, Gang Scheduling                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> Três camadas, não uma. Os pontos de provisão de Karpenter são dinâmicos (menos de um minuto, 40% mais rápido que o Cluster Autoscaler). O KAI Scheduler lida com a programação de gangues, a consciência de topologia e as filas hierárquicas. Previve a armadilha de alocação parcial de 7 de 8 onde sete nós esperam e queimam em uma GPU faltante. Os autoscalers de nível de aplicação (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) escalam em sinais específicos de inferência  profundidade de fila, utilização do cache KV  não ciclo de trabalho da CPU / DCGM. A armadilha clássica da HPA é que`DCGM_FI_DEV_GPU_UTIL`é uma medição do ciclo de trabalho: 100% pode ser 10 solicitações ou 100. vLLM pré-aloca a memória cache KV, para que a memória nunca inicie a escalação. Esta lição ensina você a compor as três camadas e evitar o default Karpenter `WhenEmptyOrUnderutilized`A política que termina a execução de trabalhos de GPU no meio da inferência.

> **【中文解读】**Este capítulo apresenta a estratégia de expansão automática de recursos de GPU em Kubernetes.
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

> - Não .**【前置】**学本节前请先掌握:Fase 17·02(平台经济学)、Fase 17·04(vLLM)、Kubernetes 基础。三层扩缩:Karpenter(节点层) + KAI Scheduler(Pod 层 gang scheduling) + 应用层(队列深度/KV利用率)。
> - Não .**【类比】**GPU 扩缩 = "餐厅运力调度"──Karpenter = 开新店(分钟级);KAI = 桌位组合(gang scheduling 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调座。HPA 陷:DCGM utilization rate is occupancy ratio,100% 可能是10 个或100 个请求必须使用 Goodput(Phase 17·08)

## Objetivos de aprendizagem

- Diagrama as três camadas de autoescalação (provisão de nós, agendamento de banda, nível de aplicação) e nome a ferramenta utilizada em cada camada.
  Chinese Language Translation: Drawing three layers automatically enlargement layer (três níveis de desenho)
- Explique por que .`DCGM_FI_DEV_GPU_UTIL`é o sinal HPA errado para vLLM e nomear duas substituições (profundeza da fila, utilização do cache KV).
  Tradução do português: explique porquê`DCGM_FI_DEV_GPU_UTIL`É o sinal de HPA errôneo do VLLM, e diz que existem duas alternativas:
- Descreva a programação de banda e o modo de falha de alocação parcial que o KAI Scheduler impede (7 das 8 GPUs inactivas).
  Chinese: 调度和 KAI Scheduler 防止的部分分配故障模式 (GPU 8 个中 7 个空)
- Nomear a política de consolidação da Karpenter (`WhenEmptyOrUnderutilized`) que encerra a execução de trabalhos de GPU e estabelece a alternativa segura para 2026.
  Chinese:                                                                                                                                                                                                                                                              `WhenEmptyOrUnderutilized`),并说明2026年的安全替代方案──

## O problema é o problema da introdução

> **【中文解读】**GPU auto-expansão em Kubernetes há três níveis de falhas de modo: 1) HPA usar erro de sinal (GPU 占用率而非队列深度), que leva a esse expansão não se expandir; 2) Cluster Autoscaler 节点 supplying too slow,长提示请求超时; 3) Multi GPU distribuição de raciocínio por parte distribuição; 7) 7-of-8 trap), 7 GPUs 空转等第 8 个.

> **【拓展：GPU 集群管理】**Em 2026 Kubernetes tornou-se uma plataforma de organização padrão de serviços de LLM 推理服务──NVIDIA DGX Cloud、Google GKE、AWS EKS 都提供 GPU 节点池管理──关键挑战在 GPU 是昂贵且稀缺资源──H100 约$3-4/h), ampliação de decisões deve ser preciso 过度供应浪费成本,供应不足影响SLA──Karpenter + KAI Scheduler 组合是目前最成熟的 GPU 调度方案──

A sua equipa envia um serviço de LLM em Kubernetes.`DCGM_FI_DEV_GPU_UTIL`O HPA nunca aumenta a escala, já pensa que você está cheio, adiciona uma réplica manualmente, o TTFT cai, o HPA ainda não escala, o sinal está mentindo.

> A tua equipa em Kubernetes está a fazer um serviço de LLM.`DCGM_FI_DEV_GPU_UTIL`Como sinal de que o HPA foi definido. Serviço no período de negócios mantém-se em 100% de utilização.

Separadamente, você usa o Cluster Autoscaler para nós. Um sinal de 1M chega às 2 da manhã; o cluster passa 3 minutos provisionando um nó, e os tempos de solicitação.

> Por outro lado, você usa Cluster Autoscaler 管理节点──凌晨2点来一个M token 的提示;集群花3分钟供给节点,请求超时──

Separadamente, você implementa um modelo 70B que requer 8 GPUs em 2 nós. O cluster tem 7 GPUs livres e 1 espalhado por 3 nós. Cluster Autoscaler fornece um nó para o 1 GPU faltante. Sete nós esperam 4 minutos a queimar dinheiro enquanto Kubernetes recebe a última GPU.

> Em outro lado, você implementou um modelo 70B de 8 GPUs que precisa de 2 nodos. O grupo tem 7 GPUs em branco, 1 em 3 nodos. O Cluster Autoscaler, por falta de 1 GPU, fornece um node.

Três camadas, três modos de falha diferentes. Autoescalação consciente da GPU em 2026 não é "ativar HPA". É compor provisionamento de nós, agendamento de banda e autoescalação de sinais de aplicação.

> Três níveis, três diferentes padrões de falhas. A GPU de 2026 percebe que o aumento automático não é "abrir HPA".

## O conceito central.

### Layer 1  provisionamento de nós (Karpenter)

> **【中文解读】**O primeiro estágio é de fornecimento de pontos. O Carpenter controla e regula o Pod, em 45-60 segundos, a partir da necessidade de criar um GPU em pontos, em comparação com o tradicional Cluster Autoscaler 快约40%.`WhenEmptyOrUnderutilized`合并策略它将终止运行推理的GPU节点转移到更便宜的实例类型,导致请求失败和模型重新加载(5-20 分钟中断)。GPU池应使用 `WhenEmpty`+ `consolidateAfter: 1h`A estratégia de segurança.

Karpenter observa os pods pendentes e os nós de provisão em ~ 45-60 segundos (Cluster Autoscaler normalmente leva 90-120 segundos para os nós GPU).`NodePool`restrição  se o seu módulo precisa de 8 H100s e o cluster não tem um nó correspondente, Karpenter provê um diretamente em vez de escalar um grupo existente.

> Karpenter  monitorar e ajustar o pod, em cerca de 45-60 segundos para fornecer o ponto de interligação`NodePool`约束动态选择实例类型 Se o seu Pod 需要 8 个 H100 且集群没有匹配节点,Karpenter 直接供应一个,而不是扩展现有组──

**The consolidation trap**O default do Karpenter.`consolidationPolicy: WhenEmptyOrUnderutilized`É perigoso para os pools de GPU. Ele terminará um nó de GPU em execução para migrar pods para uma instância de tamanho certo mais barata. Para cargas de trabalho de inferência que significam despejar solicitações em execução e recarregar um modelo 70B no novo nó. Perda é minutos de capacidade mais falhas de solicitação.

> **合并陷阱**Carpenter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `consolidationPolicy: WhenEmptyOrUnderutilized`Para a GPU 池 é muito perigoso. O terminal de GPU 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节 节

Configuração segura para pools de GPU:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Deixa o Karpenter consolidar nós verdadeiramente vazios depois de uma hora, mas nunca despejar um emprego em execução.

> Deixe Karpenter em um momento de paz, mas não vai deslocar a missão.

### Layer 2  agendamento de gangs (KAI Scheduler)

> **【中文解读】**Segundo nível é coordenação de调度. KAI Scheduler  resolver três problemas padrão que o cronista não pode lidar com: 1) Gang Scheduling全有全无调度, 8-GPU 推理要么全部启动要么全部等待; 2) 拓感知根据 NVLink/InfiniBand/机架拓放置 Pod; 3) 分层队列多团队竞争同一GPU 池时按优先级和配额管理;; Isso é muito importante para o paralelismo tensor, pois a quantidade de dados do modelo de MoE do DeepSeek-V3 etc. deve estar dentro do mesmo domínio NVLink.

> **【拓展：GPU 调度器生态】**O programação de GPU 调度器 de 2026 inclui o KAI Scheduler ((orig Karp, suportando gang + topologia + fila) 、UniKorn ((Apache 项目, suportando filas e arranjos) 、 bem como o programação padrão de kube-scheduler + 设备插件。KAI Scheduler é o único programa de programação de gangs originalmente suportado, já foi integrado pela Ray 和 vLLM production-stack 集集──

O KAI Scheduler (projeto "Karp" então renomeado) lida com o que o kube-scheduler padrão não faz:

**Gang scheduling**Uma cápsula de inferência distribuída que requer 8 GPUs ou todas as 8 começam juntas ou nenhuma. sem isso, você tem a armadilha de alocação parcial: 7 de 8 cápsulas começam, esperam indefinidamente, queimam dinheiro.

**Topology awareness** saber quais GPUs compartilham NVLink, que estão na mesma plataforma, que têm InfiniBand entre eles. Colocar pods de acordo. Uma carga de trabalho tensor-parallel DeepSeek-V3 67B deve permanecer em um domínio NVLink; KAI Scheduler respeita isso.

**Hierarchical queues** várias equipes competem pelo mesmo pool de GPU com prioridade e quota.

O KAI é implementado ao lado do kube-scheduler como um cronograma secundário; você anota cargas de trabalho para usá-lo.

> KAI 作为二级调度器和 kube-scheduler 一起部署;你通过注解让工作负载使用它──Ray 和 vLLM produção-stack 都已集成──

### Capela 3  sinais de nível de aplicação

> **【中文解读】**O terceiro estágio é o nível de aplicação.`DCGM_FI_DEV_GPU_UTIL`É a taxa de ocupação da GPU (cíclo de função) indicador 100% pode significar 10 个请求或 100 个请求, pois a GPU está ocupada.

> **【拓展：推理感知自动扩缩】**O NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler é um amplificador de 2026 especializado em LLM 推理设计. Eles consomem diretamente indicadores internos do motor de raciocínio.

**The HPA trap**- Não .`DCGM_FI_DEV_GPU_UTIL`é uma métrica de ciclo de trabalho  que mede se a GPU estava fazendo trabalho em cada intervalo de amostragem. Utilização 100% poderia significar 10 solicitações simultâneas ou 100; a GPU estava ocupada de qualquer maneira. Escalagem no ciclo de trabalho está a escalando cegamente.

Pior ainda, os motores vLLM e similares pré-alocam a memória cache KV (até `--gpu-memory-utilization`O uso de memória permanece próximo de 90% mesmo com uma única solicitação.

**2026 replacement signals**- Não .

- Profundidade da fila (número de pedidos em espera de preenchimento).
  Tradução do inglês:                                                                                                                                                                                                                                                            
- Utilização do cache KV (qual é a fração de blocos atribuída às sequências ativas).
  Chinese:KV 缓存利用率 (KV 缓存利用率)
- Por replica P99 TTFT (o seu sinal SLA).
  Tradução do inglês:
- O resultado final é o resultado final do processo de verificação.
  Tradução do inglês:Goodput (s)

O Planeador Dynamo da NVIDIA e o Variante de Carga de Trabalho de llm-d Autoscaler consomem esses sinais e réplicas de escala.

> NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本──它们完全取代了LLM 服务中的HPA──

### Quando utilizar o que

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】**Os principais estratégias para o ano de 2026 incluem: 1) Spot InstanceAWS/GCP/Azure's GPU Spot instance conta 60-70%, mas precisa de processamento interrompidoCarpenter + 热池缓解);(2) Auto expansionCarpenter em períodos não-alto-pico Automatic shrinkage节点池,50% 成本节省;(3) GPU 共享通过MIG(Multi-Instance GPU) 将H100 切割为多个实例,适合小模型推;(4) 混合 GPUFP8/INT4 量化减少内存需求,允许更多并发;(5) 分离式部署prefill/decode 分离到不同本类别 ,30-40% 成本节省;;

### Preenchimento/decodificação desagregado complica tudo

> **【中文解读】**A fase 17·17) aumentou ainda mais a complexidade de expansão: o preenchimento de Pod de acordo com a profundidade da linha de expansão, o desquadro de Pod de acordo com o KV Cache pressão de expansão. Não pode ser usado em dois HPAs.

> **【拓展：Kubernetes GPU 生态】**2026 ano Kubernetes GPU  gestão  componentes chave incluem: NVIDIA GPU Operador(auto instalação de drivers/CUDA/container toolkit) 、NVIDIA Device Plugin(GPU  recursos de descoberta e distribuição) 、MIG(Multi-Instança GPU, vai ser um A100/H100 切分为多个实例) 时间分片(GPU 共享) ;;结合Karpenter + KAI Scheduler + Dynamo Planner, pode ser implementado a partir de um ponto dado para Pod 调度到副本扩缩的完整 GPU 自動扩缩链──

Se executar pré-reempimento/decodificação desagregada (Fase 17 · 17), terá duas classes de cápsulas com diferentes desencadeadores de escala: escala de cápsulas de pré-reempimento na profundidade da fila, escala de cápsulas de decodificação na pressão do cache KV. llm-d expõe-as como separadas `Services`Não tente colocar um único HPA em frente a ambos.

> Se você estiver operando separadamente pré-reempenho/descodificação(Fase 17 · 17), você tem dois Pods com diferentes expansões de catapultadores:`Services`Cada personagem tem o seu próprio HPA. Não tente colocar um HPA em frente dos dois.

### O início frio também importa aqui .

A mitigação do início a frio (fase 17 · 10) é quando o tempo de provisionamento do nó torna-se visível ao usuário.`min_workers=1`) para os caminhos críticos para o SLO, ou utilizar o ponto de controlo de estilo Modal na camada de aplicação.

> A fase 17 · 10) é o ponto de fornecimento de tempo para tornar-se local percepível do usuário.`min_workers=1`), ou em aplicação em nível de uso Modal 风格的检查点──

### Números que você deve lembrar

- Provisão de nós de carpenter: ~ 45-60s vs Cluster Autoscaler ~ 90-120s (nodos GPU).
  Carpentário 节点供给: cerca de 45-60 秒 vs Cluster Autoscaler 约 90-120 秒(GPU 节点) 』
- O agendador KAI evita a queda de resíduos de alocação parcial  7 em 8.
  Tradução do inglês:KAI Scheduler 防止部分分配浪费7 of-8 陷。
- `DCGM_FI_DEV_GPU_UTIL`como sinal HPA: quebrado; utilizar profundidade de fila ou utilização de KV.
  Tradução:`DCGM_FI_DEV_GPU_UTIL`作为 HPA 信号:有缺陷; use队列深度或 KV利用率──
- Carpenter `WhenEmptyOrUnderutilized`O que é que é o problema?`WhenEmpty + consolidateAfter: 1h`Para inferir.
  Tradução:Carpenter`WhenEmptyOrUnderutilized`任务――推理使用 `WhenEmpty + consolidateAfter: 1h`- Não.

## Use-o com o framework implementado.

> **【拓展：GPU 自动扩缩成本模型】**O núcleo de otimização do custo do GPU auto-expansão é reduzir o tempo de transferência de espaço.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17.280── através de Karpenter 按需供应 + `WhenEmpty`合并策略 + 推理感知 HPA, pode ser automaticamente reduzido em tempos não-gápicos para 2 GPU, o custo mensal vai diminuir para cerca de US $ 8.640 (cerca de 50%) 
```figure
autoscaling
```

## Usá-lo

`code/main.py`Simula um autoescalador de três camadas em uma carga de trabalho de GPU quebrada. Compara HPA ingênuo (ciclo de serviço), HPA de profundidade de fila e escalação programada pela banda KAI. Relata solicitações não atendidas, minutos de GPU inativos e uma pontuação composta.

> `code/main.py`Em突发 GPU 工作负载上模拟三层自动扩缩机──比较简单 HPA(占用率) 队列深度 HPA 和 KAI 调度扩缩──报告未满足的请求数、空 GPU 分钟数和综合评分──

## Envia-o . Produto .

Esta lição produz`outputs/skill-gpu-autoscaler-plan.md`Considerando a topologia do cluster, a forma da carga de trabalho e o SLO, ele desenha um plano de autoescalação de três camadas.

> 本课产 出 `outputs/skill-gpu-autoscaler-plan.md` Formas de carga de trabalho e SLO, design de três níveis de expansion automática

## Exercícios.

1. Corra .`code/main.py`Sob uma carga de trabalho intensa, quantos pedidos o HPA naívo de ciclo de trabalho faz cair que a HPA de profundidade de fila captura?
   Tradução: 运行`code/main.py`◊ Em um período de tempo muito longo, a taxa de ocupação de HPA foi reduzida, e a diferença entre as duas categorias foi de que forma?
2. Desenhar um NodePool Karpenter para um cluster que serve Llama 3.3 70B FP8 no H100 SXM5. Especificar `capacity-type`- Não .`disruption.consolidationPolicy`- Não .`consolidateAfter`, e uma mancha que mantém as cargas de trabalho não GPU fora destes nós.
   中文翻译:为在 H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool──指定 `capacity-type`- Não.`disruption.consolidationPolicy`- Não.`consolidateAfter`和将非 GPU 工作负载隔离的污点──
3. A sua equipa diz que as implementações estão presas em espera porque "GPUs disponíveis, mas pod não agendar". Diagnose  é este Karpenter, kube-agendador, ou KAI agendador? Que métricas confirmam?
   Chinese Language Translation: Your Team Report Deployment卡在等待状态因为"GPU 可用但Pod 无法调度"──诊断是卡普特尔、库布-调度仪还是KAI调度仪? quais indicadores podemos confirmar?
4. Escolha um sinal para os módulos de preenchimento desagregados em autoescala e um sinal diferente para os módulos de decodificação.
   Chinese Translation: escolher um sinal para ampliar separado pré-reemplenho Pod, outro sinal para resolver Pod──为两者提供理由──
5. Calcule o custo do `WhenEmptyOrUnderutilized`Em um serviço de produção 24x7 que tenha uma média de 60 eventos de queda de solicitações por dia no P99 TTFT > 10s.
   Tradução: computador`WhenEmptyOrUnderutilized`合并陷在24x7 生产服务上的成本,该服务平均每天60次请求丢弃事件,P99 TTFT > 10秒──

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Mais leitura 延伸阅读

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) documentos de projeto e exemplos de configuração.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) semântica das políticas de consolidação e padrões de segurança da GPU.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) Dinamo Planner, sinais de escalagem.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) Padrão de integração de raios.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) Orientações específicas para a gestão de Kubernetes.
- [llm-d GitHub](https://github.com/llm-d/llm-d) Design de cargas de trabalho Variante Autoscaler.
