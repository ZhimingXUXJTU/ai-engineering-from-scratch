# O agente framework tradeoffs  LangGraph vs CrewAI vs AutoGen vs Agno  Agent framework vs LangGraph vs CrewAI vs AutoGen vs Agno
# Tradeoffs de Agente Framework  Gráfico, Papel e Orquestração de Atores

> Cada framework vende a mesma demonstração (o agente de pesquisa constrói um relatório) e esconde o mesmo bug (o esquema de estado luta com a camada de orquestração). Escolha o framework cujas abstrações correspondem à forma do seu problema; tudo o resto é cola que você escreve duas vezes.

> **【中文解读】**Cada framework mostra a mesma demonstração, todos escondem o mesmo bug, todos os esquemas de estado e conflitos de categorização.

> **【拓展：框架选择→Agent工程实践】**LangGraph  Adaptado para a necessidade de controle preciso do fluxo de trabalho de estado; CrewAI  Adaptado para a cooperação de vários papéis; AutoGen  Adaptado para o diálogo de vários agentes; Seleção de erro framework é a principal causa do fracasso do projeto de agente.

> - Não .**【前置】**O primeiro é o primeiro e último episódio da fase 11. (Langgraph, em comparação com os quatro principais frameworks) do Langgraph, CrewAI, AutoGen, Agno.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Você tem uma tarefa que precisa de mais de uma chamada de LLM. Talvez seja um fluxo de trabalho de pesquisa (planar, pesquisa, resumir, citar). Talvez seja um pipeline de revisão de código (parse diff, crítica, correção, validação). Talvez seja um assistente multi-turn que faz livros de voos, escreve e-mails e arquivam relatórios de despesas. Você escolhe uma estrutura.

> Você tem uma tarefa que precisa de várias vezes para o Mestrado em Mestrado em Administração (Mestrado em Administração) 调用任务――也许是研究工作流 (规划,搜索,总结,引用) ⋅也许是代码审查流水线 (解析,评价,修补,验证) ⋅ Você escolheu um quadro――

Três dias depois, descobrem a fuga de abstrações do quadro. A CrewAI dá-lhe papéis, mas luta contra você quando o "investigador" precisa entregar um plano estruturado ao "escritor". A AutoGen dá-lhe chat entre agentes, mas não tem estado de primeira classe, então o seu ponto de controle é um picão de um registro de conversa. O LangGraph dá-lhe um gráfico de estado, mas obriga-o a nomear cada transição antes de saber o que o agente vai fazer. O Agno dá-te uma abstração de um agente que grita quando tentas espalhar para três trabalhadores simultâneos.

> Três dias depois, você descobre que a estrutura de abstração vai vazando. A equipe de IA lhe dá um papel, mas quando o "investigador" precisa de um plano estruturado para entregar ao "escritor" surge um problema. A AutoGen lhe dá um agente, mas não tem um estado de cidadania igual. A LangGraph dá-lhe um estado de imagem, mas obriga-o a saber o que o agente vai fazer antes de nomear cada transformação.

A solução não é "pôr o melhor quadro". É combinar a abstração central do quadro com a forma do seu problema.

> O método de reparação não é "escolher o melhor quadro" mas sim fazer com que o abstracto central do quadro corresponda à forma do seu problema.


> **【中文解读】**Agente 框架选型的三个维度:(1) 任务复杂度简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph;(2) 团队经验新手用 LangChain 模板,专家用原生 API;(3) 生产要求需要 LangSmith 集成选 LangChain 生态──

> - Não .**【类比】**选 Agent 框架像选交通工具短途买菜用自行车(stdlib + function calling),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ⋅ Cada tipo de trabalho tem um cenário adequado, "quais é a melhor" é uma pergunta errada, "quais é a forma da pergunta que se encaixa com você" é apenas:

> ️ **【易错点】**框架选错的 3 个常见原因:(1) **跟风最热门**AutoGen 火就上 AutoGen, Resultado de descoberta das tarefas é apenas um único Agente + 工具,过度工程;**被 demo 误导**Demo do "Restaurante+ Escritor" do CrewAI parece muito legal, mas na realidade, os papéis na tarefa estão confusos, o papel do CrewAI é abstrato e atrasado; primeiro, o PoC é verificado.**低估迁移成本** Começar a usar Agno 简单,后期要增加 Agent 时发现 Agno 不支持,重写到 LangGraph 花两周;选框架时看 6 个月后的需求──


## O conceito central.

> **【中文解读】**O sistema de controle de dados é um sistema de controle de dados de dados de um sistema de dados de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de dados de um sistema de dados de um sistema de dados de dados de um sistema de dados de um sistema de dados de dados de um sistema de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de dados de dados de um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph);(2) 团队经验(新手用 LangChain 模板,专家用原生API);(3) 生产要求(LangSmith 集成选 LangChain 生态) ――2025 年的趋势是框架轻量化──


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

Quatro estruturas dominam a paisagem de 2026.

> Quatro quadros dominam a estrutura de 2026: os seus principais aspectos são diferentes.

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### O que significa "abstração"

A abstração central de uma estrutura é o que desenhamos no quadro quando apresentamos a arquitetura.

> O abstracto central do framework é o que você pinta em quadro branco quando você vende uma estrutura.

- **LangGraph**→ você desenha um gráfico. nós são passos, bordas são transições, e o objeto de estado em cada ponto é digitado.
  Você pinta uma imagem. O ponto é um passo, o lado é um transformador.
- **CrewAI**→ você desenha um organograma. Cada função tem uma descrição do trabalho e um gerente encaminha tarefas.
  Você desenha uma organização. Cada personagem tem uma descrição de responsabilidades, gerente distribui tarefas.
- **AutoGen**- você desenha um Slack DM. Dois agentes enviam mensagens um ao outro; um terceiro se junta se você precisa de um moderador.
  Você desenhou um Slack 私信──两个代理 互发消息──心智模型是聊天──
- **Agno**→ você desenha uma caixa única com ferramentas penduradas dela. Coloque caixas ao lado uma da outra para uma equipe. O modelo mental é "agente com baterias incluídas".
  Você desenha um quadro de ferramentas penduradas.

### A questão do Estado

O Estado é onde a maioria das escolhas de quadro se desmorona na produção.

> O estado é o lugar onde a maioria dos frameworks escolhe problemas em produção.

- **LangGraph.**Estado tipográfico (`TypedDict`O modelo Pydantic (ou modelo Pydantic), reductores por campo, ponto de verificação de primeira classe (SQLite/Postgres/Redis).
  **LangGraph。**类型化状态 (conhecimento)`TypedDict`Ou Pydantic 模型) 、每字段 reducer、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见Fase 11 · 16──)
- **CrewAI.**Os fluxos de estado como cadeias entre tarefas através do `context`campo, ou estruturado através de `output_pydantic`Não há uma loja durável por tripulação fora da caixa, você vai sair sozinho se a tripulação tiver que sobreviver a uma reinicialização.
  **CrewAI。** status como字符串在任务间通过 `context`字段流动, ou através `output_pydantic`strukturização── caixa aberta  armazenamento por tripulação  armazenamento; se a tripulação  tiver de sobreviver  reiniciar  
- **AutoGen.**Estado é o histórico de chat e qualquer usuário definido `context`As transcrições de conversação persistem; o estado de fluxo de trabalho arbitrário não, a menos que você escreva adaptadores.
  **AutoGen。** estado é chat histórico e qualquer usuário definido `context` Dialog record persistência; estado de fluxo de trabalho arbitrário não persistência, exceto se não escrever adaptador
- **Agno.**Drivers de armazenamento integrados (SQLite, Postgres, Mongo, Redis, DynamoDB) anexados a um `Agent`por via `storage=` sessões de conversação e memórias do usuário persistem automaticamente.
  **Agno。**Introdução ao sistema de armazenamento de dados (SQLite, Postgres, Mongo, Redis, DynamoDB)`storage=`- Não .`Agent`上对话会话和用户记忆自动持久化── não é um ponto de verificação completo; é um arquivo de conversação──

- **LangGraph.**Estado tipográfico (`TypedDict`O modelo Pydantic (ou modelo Pydantic), reductores por campo, ponto de verificação de primeira classe (SQLite/Postgres/Redis).
- **CrewAI.**Os fluxos de estado como cadeias entre tarefas através do `context`campo, ou estruturado através de `output_pydantic`Não há uma loja durável por tripulação fora da caixa, você vai sair sozinho se a tripulação tiver que sobreviver a uma reinicialização.
- **AutoGen.**Estado é o histórico de chat e qualquer usuário definido `context`As transcrições de conversação persistem; o estado de fluxo de trabalho arbitrário não, a menos que você escreva adaptadores.
- **Agno.**Drivers de armazenamento integrados (SQLite, Postgres, Mongo, Redis, DynamoDB) anexados a um `Agent`por via `storage=` sessões de conversação e memórias do usuário persistem automaticamente.

### A questão dos ramos

Todos os agentes não triviais são os que decidem as coisas.

> Cada agente extraordinário tem uma divisão... que decide a divisão é importante.

- **LangGraph** você decide, através de bordas condicionais. Routing é uma função Python com ramos nomeados. Ramos são de primeira classe no gráfico compilado; o checkpointer registra qual ramos foram tomados.
  **LangGraph**你决定,通过条件边──路由是带命名分支的 Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI** o gerente decide em modo hierárquico; em modo sequencial você decide no tempo de construção. O roteamento é implícito na lista de tarefas; não há "se" de primeira classe fora do prompt do gerente.
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定──路由隐含在任务列表中;经理提示外无一等公民"if"──
- **AutoGen**Os agentes decidem através do chat.`GroupChatManager`seleciona o próximo orador; pode escrever a mão um `speaker_selection_method`Mas o padrão é o LLM.
  **AutoGen**Agente 通過聊天決定──分支從誰下一個說話中涌现──`GroupChatManager`选下一个发言人;可手写 `speaker_selection_method`Mas reconhecido LLM 驱动:
- **Agno**O agente decide por que ferramenta ligar a seguir. As equipes têm um modo de coordenador/router/colaborador; a ramificação além disso é responsabilidade do desenvolvedor.
  **Agno**Agenta 通過下一個调用哪个工具决定── equipe tem coordenador/router/colaborador 模式; além disso, a分支由开发者负责──

- **LangGraph** você decide, através de bordas condicionais. Routing é uma função Python com ramos nomeados. Ramos são de primeira classe no gráfico compilado; o checkpointer registra qual ramos foram tomados.
- **CrewAI** o gerente decide em modo hierárquico; em modo sequencial você decide no tempo de construção. O roteamento é implícito na lista de tarefas; não há "se" de primeira classe fora do prompt do gerente.
- **AutoGen**Os agentes decidem através do chat.`GroupChatManager`seleciona o próximo orador; pode escrever a mão um `speaker_selection_method`Mas o padrão é o LLM.
- **Agno**O agente decide por que ferramenta ligar a seguir. As equipes têm um modo de coordenador/router/colaborador; a ramificação além disso é responsabilidade do desenvolvedor.

### A questão da observabilidade

> Problemas de observação

- **LangGraph** OpenTelemetry via LangSmith ou qualquer exportador OTel. Cada transição de nó é um período de rastreamento; pontos de controle duplicam como rastreamento repletável. LangSmith é a opção de primeira parte; Langfuse/Phoenix também tem adaptadores.
  **LangGraph** através de LangSmith ou qualquer outro 导出器的 OpenTelemetry──每个节点转换是一个追踪跨度;检查点兼作重放追踪──LangSmith é a primeira opção;Langfuse/Phoenix também tem um adaptador──
- **CrewAI** OpenTelemetry de primeira classe desde o final de 2025; integrações com Langfuse, Phoenix, Opik, AgentOps.
  **CrewAI**2025 年末起一等公民OpenTelemetry;集成 Langfuse、Fenix、Opik、AgentOps。
- **AutoGen** Integração da OpenTelemetry através de `autogen-core`O agente Ops e o opik têm conectores.
  **AutoGen** através `autogen-core`O sistema de rastreamento de dados é o sistema de rastreamento de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de
- **Agno** incorporado `monitoring=True`A Comissão propõe que a Comissão adopte um regulamento relativo à aplicação do artigo 107.o, n.o 1, do Regulamento (CE) n.o 1069/2009 do Parlamento Europeu e do Conselho.
  **Agno**内置 `monitoring=True`标志加 OpenTelemetry 导出器;与 Langfuse 紧密集成会话追踪──

### Custo e latência

Os quatro frameworks adicionam sobrecarga por chamada (lógica do framework, validação, serialização). Ordem aproximada de aumento de sobrecarga: Agno ≈ LangGraph < CrewAI ≈ AutoGen. A diferença é dominada pelo quanto extra LLM roteamento do framework faz. O gerente hierárquico do CrewAI gasta tokens para decidir quem vai a seguir; AutoGen `GroupChatManager`LangGraph só gasta tokens quando escrever.`llm.invoke`O caminho de Agno para um agente é fino.

> Quatro quadros aumentam a cada período de emprego.

Quando o custo por rodada é importante, prefira o roteamento explícito (LangGraph edges, AutoGen `speaker_selection_method`) sobre o itinerário selecionado pelo LLM.

> Quando o custo de cada operação é importante, a prioridade é a utilização de rotas de forma explícita e não de rotas de seleção de LLM.

### Interoperabilidade

> 互操作性

- **LangGraph**- Não .**LangChain**Ferramentas, retrievers, LLMs. Adaptador MCP de primeira classe (ferramentas importadas como servidores MCP).
  **LangGraph**- Não .**LangChain**工具、检索器、LLM──一等公民 MCP 适配器(工具作为 MCP 服务器导入)
- **CrewAI** ferramentas herdadas de `BaseTool`As ferramentas LangChain, LlamaIndex e MCP se adaptam a todos.`allow_delegation=True`- Não .
  **CrewAI** 工具继承自 `BaseTool`• LongChain 工具、LlamaIndex 工具、MCP 工具都适配进来──crew-to-crew 委派通过`allow_delegation=True`- Não.
- **AutoGen**→ `FunctionTool`O sistema de ligação é um sistema de ligação de ligação de um agente a outro.
  **AutoGen**→ `FunctionTool`Embalagem qualquer Python pode ser utilizado; MCP 适配器可用──与 AG2 生态紧密合用于 Agent 间模式──
- **Agno**→ `@tool`Decorador ou subclasse BaseTool; adaptador MCP; ferramentas podem ser compartilhadas entre agentes e equipes.
  **Agno**→ `@tool`装饰器或BaseTool 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## A habilidade

> Você pode explicar, em uma frase, por que uma determinada estrutura é adequada para um determinado problema de agente.
> Você pode explicar por que um quadro se adapta a um problema de um agente.

Lista de verificação pré-construída:

> 构建前检查清单:

1. **Draw the shape.**É um gráfico (estado tipado, transições nomeadas)? Um jogo de papel (especialistas entregar o trabalho)? Uma conversa (agentes falar até terminar)? Um único agente com ferramentas?
   **画出形状。**É um papel de papel, uma conversa ou um agente solitário?
2. **Decide who branches.**Desenvolvedor-decidido ramificação → LangGraph. Gerente-agente-decidido → CrewAI hierárquico. Chat-emergente → AutoGen. Ferramenta-chamada-decidido → Agno.
   **决定谁分支。**开发者决定 → LangGraph──经理 Agente decidi → CrewAI──聊天涌现 → AutoGen──工具调用决定 → Agno──
3. **Check the state budget.**Se você precisa de um currículo do ponto de verificação? viagem no tempo? interrupções humanas no meio da execução?
   **检查状态预算。**Precisas de recuperar do checkpoint?
4. **Check the cost budget.**O roteamento selecionado pela LLM custa tokens adicionais por turno.
   **检查成本预算。**O LLM 选择的路由每轮额外消耗代币 (Tocão de Consumo Extra Extra Extra) é uma forma de
5. **Budget the framework overhead.**Cada framework é outra dependência. Se a tarefa é duas chamadas de LLM e uma ferramenta, escreva 30 linhas de Python simples; nenhuma framework é mais barata do que nenhuma framework.
   **预算框架开销。**Cada framework é uma dependência diferente. Se a tarefa é apenas duas vezes LLM 调用一工具, escrever 30 行纯Python.

Recusar-se a procurar um quadro antes de poder desenhar o gráfico, o gráfico org, o chat ou a caixa de agentes.

> Antes de poderes desenhar um quadro, organizar um quadro, conversar ou um quadro de agente, não estendas a mão para um quadro. Não escolhas uma coisa que te obriga a lutar por seu modelo de estado.

## A Matriz de Decisão

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## Exercícios.
```figure
l5-framework-fit
```

## Exercícios

1. **Easy.**Faça a mesma tarefa  "investigar a sede da Anthropic, escrever um resumo de 200 palavras, citar fontes"  e implementá-lo em LangGraph (quatro nós: planejar, pesquisar, escrever, citar) e em CrewAI (três funções: pesquisador, escritor, editor).
   Utilizando a mesma tarefa em LangGraph e CrewAI, relatar o número de tokens, componentes e código executados por cada operação.
2. **Medium.**Construir a mesma tarefa em AutoGen (investigador  escritor chat, editor se une através `GroupChat`) e Agno (um único agente com `search_tools`E ...`write_tools`A classificação das quatro implementações é feita em função de: a) custo por execução, b) capacidade de retomada após um acidente, c) capacidade de injetar uma aprovação humana antes da fase de escrita.
   Em AutoGen e Agno, realização da mesma tarefa, por custo, capacidade de recuperação, aprovação artificial, capacidade de injeção de classificação.
3. **Hard.**Construir um script de árvore de decisão `pick_framework.py`que requer uma breve descrição do problema (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`O artigo 107.o, n.o 1, do Tratado CEE, estabelece que a Comissão deve proceder a uma avaliação dos riscos de risco e, em especial, a uma avaliação dos riscos de risco.
   构建决策树脚本,根据问题描述返回框架推──

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Mais leitura 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) StateGraph, pontos de controlo, interrupções, viagens no tempo.
  LangGraph 文档StateGraph、检查点、中断、时间旅行──
- [CrewAI documentation](https://docs.crewai.com/) Equipes, Fluxos, Agentes, Tarefas, Processos.
  CrewAI 文档 Crew、Flow、Agent、Task、Processo。
- [AutoGen documentation](https://microsoft.github.io/autogen/) Agente conversável, Chat de grupo, equipes, ferramentas.
  AutoGen 文档ConversableAgent、GroupChat、teams、tools。
- [Agno documentation](https://docs.agno.com/)Agente, equipa, fluxo de trabalho, armazenamento, memória.
  Agno 文档Agent、Team、Workflow、storage、memory。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) biblioteca de padrões (cadeia de instâncias, roteamento, paralelação, orquestra-trabalhadores, avaliador-optimizador) framework-agnostic.
  Antropic  Sobre a construção de um agente válido
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) o ciclo cada quadro se veste.
  Cada quadro está em embalagem de ReAct ciclo original de artigo.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) O papel de design da AutoGen.
  AutoGen's Design Essays:
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442)Base de jogo de papel que as pilhas de persona do estilo CrewAI se baseiam.
  A tripulação 风格角色堆所基于的角色扮演基础──
- Fase 11 · 16 (Langgraph)  o quadro que esta lição comparam.
  O que é o "Brasil"
- Fase 11 · 19 (Reflexão)  um padrão que mapeia limpo para LangGraph mas incómodo para CrewAI.
  Um modelo de mapeamento claro no LangGraph, mas mal-formado no CrewAI.
- Fase 11 · 22 (Observabilidade da produção)  como utilizar o instrumento, independentemente do quadro que escolher.
  Como é que você pode escolher qualquer estrutura para adicionar observação?
