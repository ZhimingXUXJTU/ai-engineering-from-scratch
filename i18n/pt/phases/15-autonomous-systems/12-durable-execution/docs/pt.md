# Agentes de longa duração: Execução duradoura

> Produtos de longo horizonte não são utilizados `while True`. Cada chamada de LLM se torna uma atividade com checkpoint, retry e replay. A integração do OpenAI Agents SDK do Temporal foi GA Março 2026. Claude Code Routines (Anthropic) executa invocações programadas de Claude Code sem um processo local persistente. As sessões pausam na entrada humana, sobrevivem às implantações e retomam a partir do último checkpoint teclado por`thread_id`. Por trás da nova ergonomia se encontra um antigo padrão  orquestração de fluxos de trabalho  com uma nova entrada: LLM chama-se a atividades não deterministas que devem ser reproduzidas deterministicamente na recuperação.

> **【中文解读】**Produção de produtos`while True`O programa de desenvolvimento de um programa de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendiz

> **【拓展：LLM 调用 = 活动的精确契合】**LLM 调用完美匹配活动特征:不确定性(temperatura > 0) 昂贵(金钱和延迟) 、可能失败(速率限制、超时) 、有副作用(调用工具)  让每个 LLM 调用包装为活动即可获得指数退避重试、跨重启检查点和可重放调试追踪──这就是为什么 Temporal、LangGraph、Cloudflare Durable Objects、Claude Code Routines 全部收到相同 API 形态`thread_id`+ 后端存储 + 最近检查点恢复──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O processo de execução duradoura é o processo de execução de um agente.
> - Não .**【类比】**Execução Durável = "Agent's archi archi archive point"―Ordinary Agent = 玩游戏没存档(崩=重头);Durable = Cada LLM 调用后自动存档(崩=读最近的存档)―Key tips:把每个 LLM 调用包装为"活动",记录输入输出到日志,崩时重放日志而不是重新调用既省钱又避免副作用重复执行(如重复转账)―
> ️ **【易错点】**副作用工具(写数据库、调外部 API) 不存缺失关键 → 恢复时重复执行可能导致业务错误(user被扣两次款) ――修复: cada side side side调用必须带等键(如`idempotency-key: uuid`), 后端按键去重──

## O problema é o problema da introdução

> **【中文解读】**持久执行确保 Agent 任务在故障后能恢复――传统 Agent 在内存中运行, process collapse 意义从头开始――持久执行将状态保存到外部存储 (database、文件系统), qualquer momento pode ser recuperado―Temporal 和 LangGraph são duas estruturas principais de execução permanente.

> **【拓展：durable execution】**持久执行对长时间运行的代理 至关重要――如果一个需要运行 2 小时的代理在第90 分钟崩,没有持久执行就意味着重新开始――Temporal 通过事件追溯源实现持久工作流,LangGraph 通过检查点实现持久状态图――2026 最佳实践是每一个重要步骤后自动保存检查点――

Considere um agente que funciona por quatro horas, chama três ferramentas, pede ao usuário duas vezes e faz quarenta chamadas de LLM.

> Consider a running of four hours Agent. Ele utiliza três ferramentas.

O que é que se passa?

> O que é que se passa?

- Em um ingênuo .`while True`loop: tudo está perdido. A execução reinicia do zero. As três chamadas de ferramenta (com efeitos colaterais reais) são executadas novamente. O usuário é solicitado novamente para coisas que já aprovaram. Quarenta chamadas LLM são re-facturadas.
  Tradução do português:`while True`循环中:一切丢失──运行从头开始重新.
- Com execução durável: a execução retoma-se a partir do ponto de controle mais recente. As atividades já concluídas não são re-executadas; seus resultados são reproduzidos a partir do registro durável. O usuário não reaprova coisas que já aprovou. As chamadas de LLM já feitas não são re-facturadas.
  Chinese:有持久执行时:运行从最近检查点恢复──已完成活动不重新执行;其结果从持久日志重放──用户不重新批准已批准的事──已做 LLM 调用不重新计费──

Este é o mesmo padrão que os motores de fluxo de trabalho têm enviado há uma década (Temporal, Cadence, Cherami do Uber). O que é novo é que as chamadas de LLM são agora uma espécie de atividade  não determinista, cara, com efeitos colaterais  e se encaixam neste padrão limpo.

> É o mesmo modelo que a máquina de trabalho de 10 anos (Temporal, Cadence, Uber's Cherami) ⋅ novo é o LLM 调用现在是一种活动不确定性昂贵有副作用它们干净地契合于这个模式

> **【中文解读】**持久化执行解决长程 经纪人的可靠性问题:四小时运行中主机重启时,朴素循环丢失一切(工具重新执行、用户重新审批、LLM 重新计费),而持久化执行从最近检查点恢复,已完成的活动从持久日志重放而不是重新执行──Temporal OpenAI Agents SDK 集成于 2026 年 3 月 GA──核心洞察:LLM调用是一种不确定性、昂贵、有副作用活动,完美适应工作流引擎的模式──

O tema da lição: a fiabilidade de longo horizonte declina (METR observa uma "degradação de 35 minutos"  taxa de sucesso cai aproximadamente quadraticamente com o horizonte).

> O METR observou "35 minutos de declínio" taxa de sucesso e linha de tempo aproximadamente ao quadrado contra o menor)  A execução duradoura permite uma operação mais longa do que o apoio de arquivos de confiabilidade, é um novo método de design correta quando a segurança falha, o design errado quando a segurança falha.

## O conceito central.

### Atividades, fluxos de trabalho e repetição

- **Workflow**O código de orquestração determinista define a sequência de atividades, os ramos, as expectativas.
  Tradução:**工作流**O processo de determinação é um processo de determinação, que é necessário para que o processo de determinação seja reorganizado e não seja causado uma diferença inesperada.
- **Activity**A atividade é registrada com suas entradas e (uma vez concluída) suas saídas.
  Tradução:**活动**O processo de execução é realizado através de um processo de execução de um processo de execução.
- **Event log**Todas as atividades iniciadas, concluídas, falhas, retestadas e todas as decisões do fluxo de trabalho são gravadas.
  Tradução:**事件日志**O processo de criação de um novo sistema de gestão de dados é realizado em cada um dos Estados-Membros.
- **Replay**A recuperação é realizada através de um processo de recuperação: ao recuperar, o código do fluxo de trabalho é executado novamente desde o início; cada atividade já concluída retorna o resultado registrado sem re-executar.
  Tradução:**重放**Quando o processo de recuperação é executado, cada atividade concluída retorna ao seu resultado registrado sem ser reexercida.

Esta é a mesma forma que React re-renderizando contra um DOM virtual, ou Git reconstruindo uma árvore de trabalho a partir de commits.

> Esta é a mesma forma que React  em relação a DOM virtual ou Git  em relação à forma do arco de trabalho de reconstrução do submetido                                                                                                                                                                                                                                              

### Porque é que as chamadas de LLM se encaixam no padrão ?

As chamadas de LLM são:

> LLM 调用是:

- Não determinista (temperatura > 0; até mesmo temperatura 0 varia entre as versões do modelo).
  中文翻译:非确定性(temperatura > 0; até mesmo temperatura 0 跨模型版本漂移) 』
- Precioso (dinheiro e latencia).
  O que é que você tem a ver com o seu dinheiro?
- Potencialmente falha (limites de taxas, temporadas).
  Tradução do inglês:可能失败 (速率限制)
- Efeitos colaterais (se invocarem ferramentas).
  Tradução do inglês:

Esta é exatamente a atividade perfil. Envolvendo cada chamada LLM como uma atividade dá-lhe uma nova tentativa com backkoff exponencial, checkpointing através de restarts, e um rastro replayable para depuração.

> É o arquivo de atividades. Cada LLM irá utilizar a embalagem para atividades.

### Pontos de controlo indicados por `thread_id`- Não .`thread_id`Porquê?

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects e Claude Code Routines convergem na mesma forma de API: um `thread_id`(ou equivalente) identifica a sessão; cada transição de estado persiste para um backend (postgreSQL padrão, SQLite para dev, Redis para cache); resume lê o último ponto de verificação.

> LangGraph、Microsoft Agent Framework、Cloudflare Durable Objects 和 Claude Code Routines foram recebidos até o mesmo formato de API:`thread_id`(ou similar) Identificação de dados; cada estado transformado em um postgreSQL; dev com SQLite; restore read最新检查点──

A escolha do backend importa:

> 后端选择重要:

- **PostgreSQL**A LangGraph é padrão.
  Tradução:**PostgreSQL**O que é que é que é o que é que é?
- **SQLite**: apenas local-dev; perde dados em todos os hosts.
  Tradução:**SQLite**: apenas em desenvolvimento; transversais de dados.
- **Redis**: rápido, mas efêmero, a menos que seja configurado AOF/snapshot.
  Tradução:**Redis**:快但临时, excepto para a configuração AOF/快照。
- **Cloudflare Durable Objects**: distribuído de forma transparente; escopo por uma chave única; sobrevive durante horas a semanas.
  Tradução:**Cloudflare Durable Objects**: transparente distribuído; em único tipo de gama; sobrevivido número de horas a semanas.

### Introdução humana como um estado de primeira classe.

Proporcionar-depois-comprometer (Lessão 15) requer um estado duradouro de "espera em humanos". O fluxo de trabalho faz pausas, a fila externa mantém a solicitação pendente e a aprovação retoma exatamente a partir desse ponto. Sem durabilidade, este é o melhor esforço; com ele, uma aprovação durante a noite chega e o fluxo de trabalho retoma na manhã.

> Propõe-se então-comprometer (§ 15 课) necessita de manter o estado de "esperar humanos" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

### A degradação de 35 minutos diminuiu 35 minutos.

A METR observou que cada classe de agentes medida demonstra decadência de fiabilidade além de ~ 35 minutos de operação contínua.

> METR  Observação de cada medida  Classe de Agente em cerca de 35 minutos de funcionamento continuado mostrou uma diminuição da confiabilidade 

A duplicação da duração da tarefa quase quadruplica a taxa de falha. A execução durável não corrige isso; permite que você execute mais tempo do que o perfil de confiabilidade suporta. O padrão seguro é combinar durabilidade com pontos de verificação que exigem HITL fresco na reentrada, e com interruptores de eliminação de orçamento (Lessão 13) que limitam o cálculo total independentemente do tempo do relógio de parede.

> O modelo de segurança é o de uma forma mais segura que se combina com a durabilidade e o de uma nova HITL que precisa de reentrada, com o de um ponto de verificação de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um orçamento de um ano.

### Quando a execução duradoura é a resposta errada, a execução duradoura não é a resposta.

- Corridas de menos de alguns minutos sem entrada humana.
  Tradução do inglês: 短于几分钟无人输入的运行──开销 > 收益──
- Recuperação de informações estritamente de leitura.
  Tradução do idioma: 严格只读信息检索。
- Funções em que a correcção exige end-to-end dentro de uma janela de contexto (algumas tarefas de raciocínio; algumas gerações de um só tiro).
  Tradução do inglês para o inglês: 正确性需要在一个上下文窗口内端到端的任务(某些推理任务;某些一次性生成)

## Use-o com o framework implementado.
```figure
memory-consolidation
```

## Usá-lo

`code/main.py`Implementa um motor de execução durável mínimo no stdlib Python.

> `code/main.py`Use padrão Python 实现最小持久执行引擎──它支持:

- `@activity`Decorador que registra entradas e saídas para um registro de eventos JSON.
  Tradução:`@activity`装饰器将输入输出记录到 JSON 事件日志──
- Uma função de fluxo de trabalho que sequencia as atividades.
  Tradução do inglês:将活动排序的工作流函数.
- A.`run_or_replay(workflow, event_log)`Função que reproduza as atividades concluídas sem re-executá-las.
  Tradução:`run_or_replay(workflow, event_log)`Função de re-exercício de atividade concluída e não re-exercício.

O motorista simula um fluxo de trabalho de três atividades, cai no meio, e mostra (a) uma nova tentativa ingênua re-executando tudo versus (b) uma repetição executando apenas a atividade faltante.

> 驱动器模拟三活动工作流,中途崩,展示 (a) 朴素重试重新执行一切 vs (b) 重放只运行缺失活动──

## Envia-o . Produto .

`outputs/skill-durable-execution-review.md`Revisar a implantação de agentes de longa duração proposta para a forma correta de execução duradoura: atividades, determinismo, backend de checkpoint, estado de entrada humana e política de HITL-on-resume.

> `outputs/skill-durable-execution-review.md`审查提议长时运行 署的正确持久执行形状: atividade, determinação, checkpoint后端, estado de entrada e recuperação humana  HITL estratégia

## Exercícios.

1. Corra .`code/main.py`Observe a diferença na contagem de execução de atividades entre a retentação ingênua e a repetição. Altere o ponto de queda e mostre a mudança na contagem de repetição em conformidade.
   Tradução: 运行`code/main.py`◊ observar simplesmente o teste e o teste de re-apertura de atividades de execução de contas diferença¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

2. Converte o motor de brinquedo para usar `thread_id`Simula duas sessões simultâneas compartilhando o motor e confirma que os registos de eventos não chocam.
   Tradução do inglês para inglês:`thread_id`❖ 模拟共享引擎的两个并发会话并确认其事件日志不冲突──

3. Tome uma atividade no motor de brinquedo. Introduza um não-determinismo (um timestamp de relógio de parede dentro de uma decisão de fluxo de trabalho). Demonstre a divergência na repetição. Explique como os motores reais lidam com isso (registro de efeitos colaterais, `Workflow.now()`- AIPs).
   Tradução do inglês em inglês:  中文翻译:在玩具引擎中取一个活动. Introdução à incerteza.`Workflow.now()`API) 

4. Leia o post "Runtime behind production deep agents" da LangChain, lista todos os estados em que o tempo de execução persiste e nome o modo de falha que cada um cobre.
   Chinese translation: read LangChain's "Runtime behind production deep agents"文章──列出运行时持久化的每个状态并命名各覆盖的失败模式──

5. Desenhar uma política de checkpoint para uma tarefa de codificação autônoma de 6 horas. Onde você checkpoint? Como é resumir-on-crash?
   Por exemplo, a primeira vez que o sistema de controle de dados foi criado, o sistema de controle de dados foi criado em uma nova plataforma de controle de dados.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Mais leitura 延伸阅读

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) orçamento, viradas e retomada da semântica.
  Tradução do inglês: budget、轮次和恢复语义。
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Forma de RequestInfoEvent.
  中文翻译:RequestInfoEvent 形态。
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) requisitos concretos de tempo de execução.
  Tradução do português: concret运行时要求。
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) Forma de actividade para chamadas de LLM.
  O termo "Linguagem de língua" é usado em língua portuguesa.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) a referência de degradação de 35 minutos.
  Tradução do inglês:
