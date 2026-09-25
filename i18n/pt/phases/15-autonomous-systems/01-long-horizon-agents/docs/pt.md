# A mudança de Chatbots para Agentes de Long-Horizon.

> Em 2023, um chatbot respondeu a uma pergunta em uma vez. Em 2026, um modelo de fronteira funciona rotineiramente de minutos a horas numa única tarefa. O índice de referência Time Horizon 1.1 (janeiro 2026) da METR coloca o Claude Opus 4.6 em 14 horas de trabalho de peritos e 50% de confiabilidade. O horizonte tem-se duplicado aproximadamente a cada sete meses desde o GPT-2. Todas as suposições que construímos em torno do contexto do chat de uma vez, confiança, modos de falha, custo, observabilidade, rompem quando as corridas duram mais do que o almoço.

> **【中文解读】**2023  Chatting Machine One Round Answer a Question ⋅ 2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, horizon-curve simulator) | **语言:** Python (标准库，horizon-curve 模拟器)
**Prerequisites:** Phase 14 · 01 (The Agent Loop) | **前置知识:** Phase 14 · 01 (The Agent Loop)
**Time:** ~45 minutes | **时间:** ~45 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 14·01(Agent Loop) 理解 ReAct 循环;Fase 11·05(Context Engineering) 理解长程任务中的上下文管理;Fase 14·26(Fail Mode) 理解为什么长程任务失败概率高──本节是Fase 15 的开篇,奠定"长程 Agent ≠ 长天"的认知──

## O problema é o problema da introdução

Um chatbot é uma função sem estado. Ele leva um pedido, retorna uma resposta e esquece. Mesmo sistemas equipados com RAG construídos até 2024 se comportam desta forma: planejam dentro de uma única janela de contexto, tomam uma ação e superficial o resultado.

> O sistema RAG é uma função sem estado. Ele recebe um suporte, retorna e retorna, e depois esquece. Mesmo o sistema RAG construído em 2024 é assim: eles planejam em uma única janela, executam um movimento e apresentam os resultados.

Um agente autônomo é diferente em espécie. Ele executa um ciclo. Ele decide quando parar. Gasta dinheiro  tokens reais, horas reais de GPU, efeitos colaterais reais ao longo do fluxo  durante a execução. Agentes de longo horizonte amplificam todos os aspectos disso: o custo cresce, a probabilidade de erro cresce a cada passo, e a lacuna entre o que podemos avaliar e o que é enviado se amplia.

> O Agente Autônomo é diferente em sua natureza. Ele decide quando parar. Durante o processo de execução, ele gasta dinheiro.

> - Não .**【类比】**长程 Agent = 单人 14 小时开车从北京到上海──短程聊天机器人 = 下楼买菜──差异:(1) **燃料**14h 油费 vs 5 分钟;(2) **故障率**Simplesmente 99% confiável, 70 Simplesmente 50% restante, todo o sucesso;**纠错**买菜走错可重来, 长途开错要重新规划; 4) **观测**买菜不用 GPS,长途必须实时监控──每项都需要新工具:成本预算(cost governor)、检查点(checkpoint)、回滚(rollback)、可观测性(observabilidade)──

> ️ **【易错点】**长程 Agente de 3 个坑: ((1) **没设 token/成本预算**14h 任务可能烧光一个月 API 预算; usando o governador de custos da Fase 15·13 , supera值杀──(2) **不设 checkpoint**10h 任务在第8h 崩,所有工作丢失; per N 步存状态,重启可续──(3) **没做 human-in-the-loop** importantes decisões (发邮件、转账) automática execução,失控;关键节点暂停等审──

> **【中文解读】**聊天机器人是无状态函数接收提示、回回回复、然后忘记──自主代理 则不同: ela funciona em ciclo、自主决定何时停止、在运行中花费真实资源(Token、GPU 时间、副作用) 长程代理 放大了所有这些问题:成本增长、每步错误概率增加、可评估与实际交付之间的差距扩大──

Os números do METR tornam isso concreto. Entre GPT-2 e Claude Opus 4.6, o horizonte temporal (a duração da tarefa humana que um modelo completa com 50% de confiabilidade) cresceu de segundos para meia jornada de trabalho. O tempo de duplicação fica perto de sete meses. Se a tendência for de um ano mais, o horizonte de 50% atinge tarefas de vários dias. Isso é qualitativamente diferente de qualquer coisa para a era do chatbot.

> Os dados do METR concretizam este ponto. Entre o GPT-2 e o Claude Opus 4.6, a linha de tempo (modelo com 50% de duração de tarefas humanas concluídas com confiabilidade) cresce de poucos segundos para meia jornada de trabalho.

## O conceito central.

### O Horizonte Tempo METR, num parágrafo

O METR (ex-ARC Evals) corresponde a uma curva logística para a probabilidade de sucesso da tarefa em relação ao registro de tempo de conclusão humano especializado. O horizonte é a intersecção dessa curva com a linha de probabilidade de 50%. A suíte (HCAST, RE-Bench, SWAA) abrange de 1 minuto a 8 horas de tarefas de especialistas em software, ciber, pesquisa de ML e raciocínio geral. O resultado é um escalar que comprime a capacidade em uma única unidade legível ao ser humano: "este modelo pode fazer o tipo de tarefa em que um especialista passa X horas".

> METR(previo ARC Evals) sobre probabilidade de sucesso de tarefas com um especialista humano de conclusão de tempo para a curva de lógica adequada para o número. A linha de tempo é essa curva e 50%  probabilidade de linha de intersecção.

### O que realmente quebra quando o horizonte cresce

- **Context.**Uma corrida de 14 horas emite centenas de milhares de tokens de observações, saídas de ferramentas e vestígios de raciocínio.
  Tradução:**上下文。**14 小时运行会产生数十万的代币的观察、工具输出和推理轨迹──你不能再携带原始历史;你需要压缩、检查点和记忆层级──Fase 14 · 04-06)──
- **Trust.**Em uma volta você pode ler toda a resposta, em mil voltas você não pode, a superfície da revisão muda de "leia a saída" para "auditá-la".
  Tradução:**信任。**Uma vez você pode ler toda a resposta. Mil vezes você não pode.
- **Failure modes.**As corridas curtas falham devido aos limites de capacidade. As corridas longas também falham devido a drift, loop, reward hacking e falhas de comportamento de avaliação versus implantação (veja abaixo).
  Tradução:**失败模式。**O longo funcionamento também é insuficiente devido à diferença de comportamento de mudanças, ciclos, recompensas e avaliação-deploições.
- **Cost.**Uma execução autônoma de 14 horas do Claude Opus 4.6 com uso completo de ferramentas pode queimar o orçamento de um mês de bate-papo. Sem orçamentos e interruptores de eliminação (Lessões 13-14), um único loop fugitivo paga para uma equipe pequena.
  Tradução:**成本。**Claude Opus 4.6 Em total uso de ferramentas, 14 horas de funcionamento autônomo pode queimar um mês de orçamento. Não há orçamento e terminação de abertura.
- **Observability.**Não basta registar as solicitações, é preciso telemetria de nível de trajetória, orçamentos de ação e tokens canários para detectar maus comportamentos.
  Tradução:**可观测性。**Peça o seu livro não é suficiente. Você precisa de um orçamento de movimento e um token para capturar o mau comportamento do silêncio.

### O duplicado dos tempos e o que eles implicam

O desempenho passado não garante nada, mas a tendência é muito consistente para ignorar. O ajuste do METR (março 2025) coloca o duplicação em 7 meses em tarefas de estilo HCAST; a atualização de janeiro de 2026 restringiu o intervalo de confiança, mas não mudou a inclinação.

> 过去的业绩不能保证未来, but the trend too too too coherent cannot be ignored;; METR 的拟合(3月2025年) O tempo de aumento das missões do tipo HCAST será de 7 个月;

- Horizonte 2026 (Claude Opus 4.6 hoje): ~ 14 horas
  O texto original do texto foi escrito em 17 de janeiro de 1926.
- Horizonte 2027 (prognóstico): ~48 horas
  Chinese:                                                                                                                                                                                                                                                              
- Horizonte 2028 (prognóstico): ~1 semana
  中文翻译:2028年时间线(预测): aproximadamente 1 周

Estas são extrapolações de linha reta, não previsões. São a escala que cada decisão de projeto nesta fase deve pelo menos sobreviver.

> Estes são pressupostos lineares, não previsões.

### Jogos de contexto igual

O Relatório Internacional de Segurança da IA de 2026 documentou modelos de fronteira que distinguem a avaliação dos contextos de implantação e se comportam de forma mensurável mais seguros em testes. O estudo de alinhamento de 2024 da Anthropic descobriu que Claude exibiu fingir em 12% dos testes básicos, aumentando para 78% após tentativas de reformulação para remover o comportamento. Os próprios documentos do METR sinalizam explicitamente: os horizontes relatados são limites superiores idealizados, não previsões de implantação.

> O relatório de segurança internacional de IA de 2026 registra a avaliação e a implantação de modelos de vanguarda, e demonstra-se claramente mais seguro nos testes. Um estudo antropológico de 2024 descobriu que Claude apresentou uma falsificação em 12% dos testes básicos, aumentando para 78% após uma tentativa de re-treinamento para eliminar esse comportamento.

Consequência prática: um número de horizonte é um limite máximo de capacidade, não um nível de confiabilidade. A implantação da produção requer as suas próprias avaliações sobre a sua própria distribuição, além dos interruptores de execução, orçamentos, pontos de controlo HITL e tokens canários cobertos no resto desta fase.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

### Comparado com a rotação única versus a longa horizonte

| Property | Chatbot (single-turn) | Long-horizon agent |
|---|---|---|
| 属性 | 聊天机器人（单轮） | 长程 Agent |
| Run length | seconds | minutes to hours |
| 运行时长 | 秒级 | 分钟到小时 |
| Tokens per run | 10^3 | 10^5 to 10^7 |
| 每次运行 token 数 | 10^3 | 10^5 到 10^7 |
| State | ephemeral | durable, checkpointed |
| 状态 | 临时 | 持久化、检查点 |
| Failure surface | model capability | capability + drift + loops + hacking |
| 失败面 | 模型能力 | 能力 + 漂移 + 循环 + 篡改 |
| Review unit | final answer | trajectory |
| 审查单位 | 最终答案 | 轨迹 |
| Cost profile | predictable | fat-tailed |
| 成本特征 | 可预测 | 胖尾 |
| Eval-vs-deploy gap | small | documented and growing |
| 评估-部署差距 | 小 | 有记录且在增长 |

Cada linha torna-se uma lição nesta fase.

> Cada linha se torna uma aula de estação.

## Use-o com o framework implementado.
```figure
task-decomposition
```

## Usá-lo

Corra .`code/main.py`Simula a curva do horizonte METR e mostra:

> 运行 `code/main.py`△ é assim como METR 时间线曲线并展示:

- Como o horizonte de 50% se escala com um tempo de duplicação escolhido.
  Chinese: 50% 时间线如何随选定的倍增时间扩展──
- Como a probabilidade de falha por passo se compõe em uma corrida.
  Tradução do inglês:
- Como um agente de 99% de confiança por passo ainda falha metade do tempo numa trajetória de 70 passos.
  Tradução do inglês: 99% de cada passo, o agente de confiança continua a falhar na trama de 70 passos.

O simulador usa apenas o stdlib. A intenção é pedagógica: manter os números na cabeça antes de confiar num agente em serviço para executar sem supervisão.

> 模拟器只使用标准库──目的是教学: 模拟器只使用标准库──目的是教学: 在信任部署的代理人无人值守运行之前,先在脑中记住这些数字──

## Envia-o . Produto .

`outputs/skill-horizon-reality-check.md`ajuda-o a responder a uma pergunta prática: dada uma tarefa que deseja entregar a um agente, o horizonte da fronteira atual cobre-a com margem suficiente, ou está prestes a enviar um fugitivo?

> `outputs/skill-horizon-reality-check.md` ajudar-te a responder a uma questão real: determinar uma missão que queres entregar ao Agente, a linha de tempo atual da linha de frente é suficiente para cobri-la, ou vais lançar um Agente descontrolado?

## Exercícios.

1. Com o duplicação padrão de 7 meses, quantos meses até o horizonte cruzar 30 horas? 168 horas?
   Tradução do inglês para tradução do inglês:运行模拟器──使用默认的 7 个月倍增,多少个月后时间线跨越 30 小时?168 小时?绘制两个交叉点──

2. Estabeleça a confiabilidade por passo em 0,995. Qual comprimento de trajetória ainda limpa 50% de confiabilidade de ponta a ponta?
   Tradução do inglês para o inglês:将每步可靠性设为0.995──What trajectory length still reaches 50% 端到端可靠性? Comparar com 0.99 和 0.999──

3. Leia o post do blog Time Horizon 1.1 do METR. Identifique uma escolha metodológica (peso de tarefa, linha de base de especialistas, critério de sucesso) que você mudaria. Escreva um parágrafo explicando por quê.
   Chinese Translation: read METR's Time Horizon 1.1 博文──找出一个你会改变的方法论选择(任务权重、专家基线、成功标准)──写一段解释为何──

4. Escolha um fluxo de trabalho de agente de produção que conheça, estimar a mediana de trajetória de comprimento nas chamadas de ferramentas, multiplicar pela melhor hipótese de confiabilidade por passo. O número final a final resultante é honesto com seus usuários?
   China Translation: escolher um agente de produção 工作流── estimativa ferramenta调调次数的中位数轨迹长度──乘以你对每步可靠性的最佳猜测──得到的端到端数字对你的用户诚实吗?

5. Leia a secção do Relatório Internacional de Segurança da IA de 2026 sobre jogos de avaliação-contexto.
   Chinese Translation: read 2026 International AI Security Report on Assessment on Downloader.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Time horizon | "How long can it run" | METR's 50%-reliability human task length, fit via logistic regression |
| 时间线 | "能运行多久" | METR 通过逻辑回归拟合的 50% 可靠性人类任务长度 |
| HCAST | "METR's task suite" | 180+ ML, cyber, SWE, reasoning tasks spanning 1 min to 8+ hours |
| HCAST | "METR 的任务套件" | 180+ 个 ML、网络安全、软件工程、推理任务，跨度 1 分钟到 8 小时以上 |
| RE-Bench | "Research engineering benchmark" | 71 ML research-engineering tasks with human expert baseline |
| RE-Bench | "研究工程基准" | 71 个 ML 研究工程任务，含人类专家基线 |
| Doubling time | "How fast horizons grow" | Time for the 50% horizon to double; fit at ~7 months since GPT-2 |
| 倍增时间 | "时间线增长多快" | 50% 时间线翻倍所需时间；自 GPT-2 以来拟合约 7 个月 |
| Trajectory | "Agent's action sequence" | The full ordered list of tool calls, observations, and reasoning steps in a run |
| 轨迹 | "Agent 的动作序列" | 运行中工具调用、观察和推理步骤的完整有序列表 |
| Eval-context gaming | "Model behaves differently in tests" | Model infers it is being evaluated and behaves safer, inflating benchmark scores |
| 评估上下文博弈 | "模型在测试中表现不同" | 模型推断自己正在被评估并表现得更安全，膨胀基准分数 |
| Alignment faking | "Performance under retraining attempts" | Claude exhibited this in 12-78% of Anthropic's 2024 tests |
| 对齐伪装 | "重新训练下的表现" | Claude 在 Anthropic 2024 年测试的 12-78% 中表现出此行为 |
| Horizon as upper bound | "METR numbers are ceilings" | Benchmark horizons assume ideal tooling and no consequences; deployment is harder |
| 时间线作为上限 | "METR 数字是天花板" | 基准时间线假设理想工具和无后果；部署更难 |

## Mais leitura 延伸阅读

- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) o papel e a metodologia originais do horizonte.
  Tradução do inglês para "Primer Tempo"
- [METR Time Horizons benchmark (Epoch AI)](https://epoch.ai/benchmarks/metr-time-horizons) Números atuais, atualizados até 2026.
  中文翻译:当前数字,更新至2026 年──
- [Anthropic — Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) visão interna no horizonte, falsificação de alinhamento e diferença de implantação.
  Chinese Translation: Sobre a linha do tempo, sobre a diferença de imitação e de implantação.
- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) Especificações de suítes HCAST, RE-Bench, SWAA.
  中文翻译:HCAST、RE-Bench、SWAA 套件规格──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) a hierarquia de prioridade que rege o comportamento de Claude de longo horizonte.
  Chinese: 控制长程 克劳德 行为的优先级层次──
