# Paralelas / Enxames / Arquiteturas em Rede

> Contraste com o supervisor: não há decisores centrais. Os agentes lêem um ônibus de eventos compartilhados, começam o trabalho de forma assíncrona, e escrevem os resultados. LangGraph suporta explícitamente "Arquitetura de Enxurro" para ambientes descentralizados e dinâmicos. Matrix (arXiv:2511.21686) representa tanto o controle quanto o fluxo de dados como mensagens serializadas passadas por filas distribuídas para eliminar o gargalho de engarrafamento do orquestador. A compensação é explícita: determinismo e rastreabilidade para escalabilidade. O conjunto de tarefas combina com muitos subproblemas independentes; não se encaixa em tarefas que necessitam de um único plano coerente.

> **【中文解读】**Esta secção apresenta o modelo de organização de um grande número de agentes através de um estado compartilhado e de um trabalho conjunto.

> **【拓展：parallel swarm networks→具体应用】**Elaboração de redes de grupos para fazer grandes quantidades de agentes, assim como tarefas de processamento, e então agregação de resultados.


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 16·04-05 ((原语+Supervisor) ⋅本節是Supervisor's反面无中心协调器的群体网络⋅
> - Não .**【类比】**Swarm vs Supervisor = "decentralização" vs "nível de nível"──Supervisor = empresa(CEO 调度);Swarm = 开源社区(每人看问题 板自己领取)──Swarm 适合独立子任务(多文件编辑、多源查询),不适合需要单一计划的任务──5-10 个代理是最优太多会聚聚时打架──

## Problema Introdução

O supervisor passa a ser um número limitado de trabalhadores. E se forem centenas? O próprio supervisor torna-se o gargalo de engarrafamento: cada decisão sobre quem faz o que canaliza através de um agente. Um passo lento do plano impede todo o sistema.

> O supervisor pode se expandir para várias máquinas. Os supervisores se tornam em cada um dos blocos: cada um dos seus decisões sobre quem faz o que é feito passa por um agente.

O supervisor é em si uma chamada de LLM. Em centenas de trabalhadores, o supervisor faz centenas de chamadas de LLM apenas para enviar. Cada chamada é de segundos; a carga de envio domina. Swarm remove o supervisor inteiramente.

> O supervisor em si é o LLM 调用. Em centenas de máquinas de trabalho, o supervisor apenas muda para realizar centenas de LLM 调用.

Arquiteturas de enxames inverter o design. Em vez de um planejador central despachando o trabalho, os trabalhadores escolhem o trabalho de uma fila compartilhada. A "coordenação" é cozida na semântica do ônibus de eventos.

> 群体架构翻转了设计―― não é um planejador central que divide o trabalho, mas um trabalho que é obtido pela coordenação de uma linha de trabalho compartilhada―― não há um organizador; o sistema se expande até que a linha de trabalho se torne um copo──

A inversão arquitetônica é significativa: o gargalo de engarrafamento passa de "o LLM que decide o que fazer" para "o corretor de mensagens que funciona".

> Arquitetura reversa transformação significativa: os grupos de agentes que usam os processos de transferência de um LLM para um outro são quase sempre ganhosos.

## Conceptos básicos

### A forma

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

Não há orquestra. Cada trabalhador repete: puxar uma tarefa, processar, escrever o resultado (e opcionalmente fazer a sequência).

> 没有编排器.每个工作器重复:拉取任务、处理、写入结果.

A falta de um decisor central é a característica definidora. Os trabalhadores não esperam instruções; eles se auto-organizam em torno da fila. Este é o modelo de atores aplicado aos LLM.

> 缺乏中央决策者是定义特征──工作器不等待指令;它们围绕着队列自组织──这是应用于 LLM actor 模型每个工作器是响应消息的独立 actor──

### Quando o enxame se encaixa

- **Many independent tasks.**Descarregamento, transformação, classificação.
  Tradução:**许多独立任务。**抓取、转换、分类── missões entre si não dependem umas das outras.
- **Variable-duration work.**Se algumas tarefas demoram 100ms e outras 10s, um enxame balança carga automaticamente  trabalhadores rápidos puxar os próximos trabalhos.
  Tradução:**可变持续时间的工作。**Se algumas tarefas exigem 100ms e outras 10s, o grupo irá automaticamente equilibrar a carga.
- **Throughput over determinism.**Tu queres o tempo total de conclusão, não a ordem rigorosa.
  Tradução:**吞吐量优先于确定性。**Tu preocupas-te com o tempo de conclusão, não com a ordem rigorosa.

### Quando o enxame falha

- **Ordered workflows.**Se o passo 3 precisar da saída do passo 2, um enxame corre o risco de disparar o passo 3 antes do passo 2 ser feito.
  Tradução:**有序工作流。**Se o passo 3 precisar de saída do passo 2, o grupo tem passo 3 em passo 2  antes de terminar o risco de iniciar o processo.
- **Global-plan tasks.**As questões de pesquisa complexas beneficiam de um planejador.
  Tradução:**全局计划任务。**Problema de estudo complexo beneficiado dos planejadores                                                                                                                                                                                                                                                       
- **Debugging.**Sem registro central e trabalho assíncrono, a reprodução de um bug é cara.
  Tradução:**调试。**没有中央日志和异步工作, o custo de recuperar bugs é muito alto.

### Matrix (arXiv:2511.21686)

Matrix é o documento de 2025 que leva o enxame à sua conclusão natural: tanto o fluxo de controle quanto o fluxo de dados são mensagens serializadas em fileiras distribuídas. Não há coordenador central. Tolerança de falha vem da durabilidade da mensagem. Escalabilidade é o problema do corretor de mensagens, não do sistema.

> Matrix é um artigo sobre o que o grupo em 2025 vai fazer para a conclusão natural: o fluxo de controle e o fluxo de dados são informações de sequenciação em linhas distribuídas. Não há coordenação central.

Ao tornar o corretor (Kafka, Redis Streams, NATS) o garfo de escala, a Matrix evita completamente o garfo de escala da LLM como orquestrador.

> 通過使代理 ((Kafka、Redis Streams、NATS) tornar-se um "botelão de expansão", Matrix 完全避开 LLM 作为编排器的瓶──如果代理可以,系统可以扩展到数千代理; LLM é puramente um "工作器", nunca um "协调器".

Contribuição: um modelo de programação em que a coordenação entre vários agentes é "a que assunto de mensagem este agente se inscreve?" em vez de "qual agente o supervisor escolhe a seguir?" Isso faz com que o sistema pareça uma malha de evento pub/sub.

> Contribuição: um modelo de programação, multi-agente coordena é "este agente  suscrição que assunto de notícias?" em vez de "supervisor próximo escolher qual agente?" que faz o sistema parecer um lançamento / suscrição evento netgromad.

### Arquitetura de Swarm de LangGraph
### Enxames em quadros gráficos

Os documentos de LangGraph 2025 descrevem explicitamente "Arquitetura de Enxurro" como um dos padrões multi-agentes: os agentes são nós, mas as bordas formam um gráfico direcionado com ciclos e qualquer nó pode ser ativado a partir do pool.

> LangGraph 2025 文档明确将"群体架构"描述为多代理模式之一:Agenta é um ponto, mas ao longo da formação de um círculo, qualquer ponto pode ser ativado na piscina.

A contribuição de LangGraph: o mesmo modelo mental baseado em gráficos agora suporta a dinâmica do enxame. nós que se ativaram com base em condições em vez de bordas fixas.

> Contribuições de LangGraph: o mesmo modelo mental baseado em gráficos agora suporta a dinâmica do grupo.

### Modo de falha: fome e manchas quentes

Se todos os trabalhadores fizerem a tarefa mais rápida disponível, as tarefas de longa duração nunca serão escolhidas até que sejam as únicas que restam.

> Se todos os dispositivos de trabalho tiverem as tarefas mais rápidas, as tarefas de longo prazo nunca serão selecionadas até que se tornem as únicas que sobrarem.

A fome é o modo de falha da assinatura do enxame. Sem envelhecimento explícito (a prioridade aumenta com o tempo de espera) ou trabalhadores especializados de tarefas longas, uma tarefa de 10 segundos espera para sempre atrás de um fluxo de tarefas de 100 ms. Enxames de produção devem engenharia em torno disso.

> 饥饿是群体的标志性失败模式――没有明显老化 (没有明显老化) 没有优先级随着等待时间增加) 没有专业化长任务工作器,10秒任务永远在100ms 任务流后等待――生产群必须围绕这个工程设计――

Mitigações:
- Coisas de prioridade com envelhecimento explícito (aumentar a prioridade com o tempo de espera).
  Tradução do inglês para o inglês: 带显式老化优先队列 (带显式老化优先队列)
- Especialização dos trabalhadores: alguns trabalhadores só assumem tarefas "longas".
  Tradução em inglês:工作器专业化:一些工作器只接受长任务──
- Pressão de retorno: limite o número de tarefas rápidas que entram na fila.
  Tradução do inglês: Backstroke: Limit how many fast tasks enters the lineup.

### O link de roteamento baseado em conteúdo

Os pares de conjuntos são naturalmente com roteamento baseado em conteúdo (Lessão 22). Em vez de uma fila genérica, tem uma fila por tipo de mensagem.

> O grupo e o caminho baseado em conteúdo não são uma linha geral, mas um tipo de linha para cada tipo de mensagem.

O roteamento baseado em conteúdo mais enxame fornece a rede de eventos pub/sub: um substrato onde qualquer agente pode publicar qualquer tipo de mensagem e apenas os agentes interessados recebem. Esta é a base do Matrix, CA-MCP e a maioria dos sistemas multi-agente de produção de 2026.

> Baseado em conteúdo, o grupo de routes adiciona-se para você publicar/subscrever eventos: um agente pode publicar qualquer tipo de mensagem e apenas o agente interessado recebe a sua base. Esta é a base do sistema Matrix, CA-MCP e a maioria dos sistemas de produção de agentes múltiplos em 2026:

## Construí-lo e realizei-o.
```figure
sw-work-stealing
```

## Construí-lo

`code/main.py`Implementa um enxame de 4 fios de trabalhadores puxando de um compartilhado `queue.Queue`As tarefas têm durações variáveis (alguns rápidos, outros lentos).

> `code/main.py`Realizou 4 ̇ de partilha ̇`queue.Queue`拉取工作线程──任务有可变持续时间一些快,一些慢)── apresentação

A comparação em três vias é o valor educacional: as mesmas tarefas, os mesmos trabalhadores, apenas a estratégia de envio muda. Sequencial = lento. Fixa = desperdiçosa. Enxame = óptimo. Os números do relógio de parede fazem o caso empiricamente.

> O sistema de ensino é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino que é um sistema de ensino.

- **Sequential baseline:**Um trabalhador processa todas as tarefas em série.
  Tradução:**顺序基线：**Uma máquina de trabalho está a processar todas as tarefas.
- **Fixed assignment:**Cada tarefa pré-assignada a um trabalhador específico (estilo de supervisor).
  Tradução:**固定分配：**Cada tarefa é previamente atribuída a um determinado trabalho.
- **Swarm:**Os trabalhadores se retiram de uma fila compartilhada.
  Tradução:**群体：**工作器 de comunhão de equipa

As balanças de massa carregam-se automaticamente; a atribuição fixa deixa os trabalhadores rápidos ociosos quando a tarefa atribuída é lenta.

> 群体自动平衡负载; fixa distribuição em atribuição de tarefas lenta tempo fazer rápido

A distribuição "inequilibrada, mas ideal" é a assinatura do enxame. Um trabalhador que termina sua tarefa em 50 ms tira mais três enquanto um trabalhador em uma tarefa de 2 segundos ainda está em sua primeira. O total do relógio de parede é limitado pela tarefa única mais lenta, não a soma.

> "Não uniforme mas ideal" distribuição é o grupo características. 50ms  para completar tarefas em 2 segundos tarefas de trabalho ainda leva três tarefas mais ao tempo da primeira tarefa.

A saída mostra o número de tarefas por trabalhador (a distribuição do enxame é desigual mas ótima) e os tempos do relógio de parede.

> 输出显示每个工作器的任务计数(grupos distribuídos não uniformes, mas melhores)

## Use-o com o framework implementado.

`outputs/skill-swarm-fit.md`Avalia se uma tarefa deve utilizar swarm vs supervisor. Input: independência da tarefa, variação de duração, requisitos de encomenda, necessidades de depuração.

> `outputs/skill-swarm-fit.md`评估任务应使用群体还是监督者――输入: independência de tarefas、持续时间差、排序要求、可调试性需求――

## Envia-o . Produto .

Lista de verificação:

> 检查清单:

- **Priority queue with aging.**Prevenção da fome de longas tarefas.
  Tradução:**带老化的优先队列。**防止长任务饥饿── Não é preciso.
- **Worker idempotency.**A tarefa pode ser realizada mais de uma vez se um trabalhador acidentar no meio da corrida.
  Tradução:**工作器幂等性。**Se o trabalho se desmoronar, as tarefas podem ser retiradas várias vezes.
- **Durable queue.**Use Kafka, Redis Streams ou uma fila de produção com base em banco de dados. `queue.Queue`É apenas na memória.
  Tradução:**持久队列。**O que é o "conjunto de dados" de "Kafka"",Redis Streams" ou "Database Supported"`queue.Queue`                                                                                                                                                                                                                                                              
- **Observability per task.**Cada tarefa tem um identificador de rastreamento; todos os trabalhadores registam o início/fim com ele.
  Tradução:**每个任务的可观测性。**Cada missão tem um ID de rastreamento; cada trabalho com ele registra começo/final.
- **Back-pressure.**Se a fila crescer mais rápido do que os trabalhadores a drenarem, retarda o produtor.
  Tradução:**背压。**Se a linha de produção crescer rapidamente em relação à velocidade de produção, diminui-se o número de produtores.

## Exercícios.

1. Corra .`code/main.py`Quanto mais rápido é o enjambre do que o sequencial na carga de trabalho de duração variável?
   Tradução: 运行`code/main.py`◊ O que é o número de grupos em carga de trabalho em tempo de duração variável?
2. Adicionar uma variante da fila de prioridade (utilização `queue.PriorityQueue`Acompanhe a prioridade por tarefa no campo "importância". Observe se as tarefas de baixa prioridade já passam por fome sob carga contínua.
   中文翻译:添加优先队列变体(使用 `queue.PriorityQueue`■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
3. Implementar um detector de pontos de calor: registar quando um trabalhador processa 3 vezes mais tarefas do que o trabalhador mais lento.
   Tradução do inglês para tradução do inglês: implementando o ponto de calor: quando qualquer máquina de trabalho processar mais de 3 vezes a velocidade de trabalho do que a mais lenta, isso indica que a distribuição de tempo de trabalho tem quais características?
4. Leia o resumo do artigo da Matrix (arXiv:2511.21686) e a Seção 3. Identifique um tradeoff específico que a Matrix aceita (ganho de escalabilidade) e um que ele desiste (traçabilidade, determinismo).
   Tradução do português: read Matrix 论文 ((arXiv:2511.21686) resumo e 3o 节──identificação Matrix 接受一个具体权衡(可扩展性收益) 和一个放弃的(可追溯性、确定性)──
5. Converte a demo do enxame para usar um `queue.Queue`As regras de roteamento são sensíveis quando as tarefas são heterogêneas.
   Tradução do inglês para tradução livre:将群体演示转换为使用 (task_type, payload) 元组的 `queue.Queue`, trabalho máquina apenas subscreve um tipo específico. Quando as tarefas são construídas, quais regras de routes são razoáveis?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Mais leitura 延伸阅读

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Apoio explícito do enxame
  Tradução do inglês:LangGraph 工作流和 Agent  群体架构  明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) Enxame completo de mensagens
  Tradução do idioma:MATRICS  多 AGENT 系统的去中心化框架  全消息传递群体
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) por que um sistema de produção específico escolheu explicitamente o supervisor em vez do enxame
  Chinese Translation:Antropic 工程  Por que o sistema de pesquisa escolhe o supervisor e não o grupo  Por que um sistema de produção específico claramente escolhe o supervisor e não o grupo
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) o ator de eventos-driven reescrever, mais perto do enjambre do que o GroupChat de v0.2
  AutoGen v0.4 actor 模型文档  事件驱动 actor 重写,比 v0.2 的 GroupChat 更接近群体
