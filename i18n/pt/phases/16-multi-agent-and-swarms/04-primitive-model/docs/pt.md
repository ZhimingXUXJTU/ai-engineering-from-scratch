# O Modelo Primitivo Multi-Agente.

> Quatro primitivas, nada mais  o agente, a transferência, o estado compartilhado, o orquestador  abrangem um espaço de design quadridimensional, e as principais estruturas multi-agentes que serão enviadas em 2026 (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework) são pontos nele. Esta lição construiu-os a partir de zero, executa um sistema de brinquedos em todos os quatro, e depois mapeia cada quadro principal nos mesmos eixos para que você possa ler qualquer nova versão em um parágrafo.

> **【中文解读】**Esta secção apresenta o modelo original 多 代理 系统 基本构建单元和交互原语.

> **【拓展：primitive model→具体应用】**多 Agent 系统的最小原语模型定义了 Agent 之间基本交互模式:(1) 消息传递Agent 通过发送消息通信;(2) 共享状态Agent 通过阅读写共享存储协调;(3) 事件通知Agent 订阅感兴趣的事件──AutoGen 用消息传递,LangGraph 用共享状态,黑板系统用事件通知──Most actual systems mix use multiple原语──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本节前 請先掌握:Fase 14 ((Agenta 工程) 、Fase 16·01 ((多 Agent 动机) 。本节是Fase 16 的核心4个原语(agent/handoff/shared-state/orchestrator) define所有框架的设计空间。
> - Não .**【类比】**4 原语 = "音乐四件套":agente(乐手)、handoff(独奏接力)、shared state(总谱)、orchestrator(指挥)。AutoGen 偏消息传递、LangGraph 偏共享状态、CrewAI 偏角色分工 são todas estas 4 原语的不同组合──学会原语后看任何新框架都能 1 段话读懂──

## Problema Introdução

A cada seis meses, um novo framework multi-agente é lançado. AutoGen em 2023. CrewAI em 2024. LangGraph e OpenAI Swarm em 2024. Google ADK em abril de 2025.

> Cada seis meses, haverá uma nova estrutura de multi-agente lançada. O AutoGen de 2023; o CrewAI de 2024; o LangGraph de 2024; e o OpenAI Swarm de 2024; o Google ADK de 4 de abril de 2025; o Microsoft Agent Framework RC de 2 de janeiro de 2026; cada jornal afirma ser um "abstrato verdadeiro".

O churn é real, mas os primitivos subjacentes não estão mudando. O que parece ser inovação é muitas vezes rebranding: os mesmos quatro botões (agente, transferência, estado compartilhado, orquestador) com diferentes padrões e sintaxe. Uma vez que você vê os primitivos, o marketing cai.

>  mudança é real, mas o idioma original de base não mudou.  parece que algo novo é frequentemente re-brandingado: os mesmos quatro círculos (agente, comunicação, condição de partilha, editor) têm diferentes valores e linguagem. Quando você vê o idioma original, a comercialização desaparece.

Se você tentar aprender um por um você vai ficar sem recursos. As APIs parecem diferentes. Os documentos discordam sobre o que é um "agente". Uma estrutura chama sua memória compartilhada de um "blackboard", outro chama-lo de um "pool de mensagens", um terceiro chama-lo de um "StateGraph". Você começa a suspeitar que o campo está apenas a girar.

> Se você tentar um um em um lugar para aprender, você vai se cansar de todo. Apí parece diferente.

Não é. Por baixo do marketing, os quatro primitivos são estáveis. Aprenda-os uma vez, leia cada novo quadro em um parágrafo.

> O fato não é assim. Em termos de marketing, quatro idiomas originais são estabilizados.

## Conceptos básicos

### Os quatro primitivos

1. **Agent** um prompt do sistema mais uma lista de ferramentas. Estatal; cada execução começa com o seu prompt do sistema e o histórico de mensagens atual.
   Tradução:**Agent** Uma ordem de dados de um sistema adicionada a uma lista de ferramentas.
2. **Handoff** uma transferência estruturada de controle de um agente para outro. Mecanicamente, uma chamada de ferramenta que retorna um novo agente ou uma borda de gráfico que segue uma condição.
   Tradução:**交接** Transferência de controle estrutural de um Agente para outro Agente.
3. **Shared state** qualquer estrutura de dados que mais de um agente possa ler (às vezes escrever). Pool de mensagens, quadro negro, armazenamento de valores de chave, memória vetorial.
   Tradução:**共享状态** Multiple Agentes pode ler qualquer estrutura de dados (sometimes write in) 
4. **Orchestrator** quem decide quem fala a seguir. Opções: um gráfico explícito (determinista), um selector de oradores LLM (suave), a chamada de entrega do último orador (OpenAI Swarm), ou um cronógrafo sobre uma fila (arquitetura de enxames).
   Tradução:**编排器** decidir quem vem a seguir a um discurso de papel.

Cada framework escolhe as definições padrão para cada eixo; o resto é a sintaxe de superfície.

> É o espaço de design inteiro. Cada quadro tem um valor de seleção de cada eixo.

A implicação: não há uma estrutura multi-agente "melhor". Há apenas "melhor para as preferências de eixo da sua tarefa". Uma estrutura que orquestra a orquestração para pipelines deterministas (LangGraph) é errada para conversas emergentes (use AutoGen). Conheça seus eixos, então escolha.

> 含义: não há "melhor" multi-agente 框架── apenas "melhor adequado para o seu objetivo eixo preferencial" framework── na determinação de fluxo de água na linha de fixação de um quadro de organização (Langgraph)

### Como cada quadro 2026 mapeia para ele

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

> O quadro do agente contacta o estado do compartilhamento do editor
> Não é o que eu quero dizer.
> O que é que eu faço?`Agent(instructions, tools)`O instrumento de volta para o agente de conversas.
> O AutoGen v0.4 / AG2`ConversableAgent`O grupo Chat é um selecionador de palavras, um selecionador de mensagens, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras, um selecionador de palavras.
> ♪ A tripulação está pronta ♪`Agent(role, goal, backstory)`- Não .`Process.Sequential / Hierarchical`Mudanças de trabalho em linha de saída, gestão de LLM ou em ordem estática.
> # LangGraph # Função de Nótulos # Diagrama + Condições`StateGraph`- A segurança.
> O Microsoft Agent Framework , o agente + Modelo de edição , padrão específico , padrão específico ,
> O Google ADK é um agente + cartão A2A

As diferenças superficiais parecem enormes, por baixo, os mesmos quatro botões.

> A diferença de superfície parece grande.

### Por que isto importa

Uma vez que você vê os primitivos, a comparação de framework se torna uma lista de verificação curta:

> Uma vez que você viu o idioma original, framework comparator se transforma em uma lista de verificação breve:

- O orquestrador confía no LLM para encaminhar (Swarm) ou encaminha o envio em código (LangGraph)?
  Tradução do inglês: 编排器是信任 LLM 来路由(Swarm)
- O estado compartilhado é histórico completo (GroupChat) ou projetado (Redutor de Estatograma)?
  Chinese: 共享状态是完整历史 (共享状态是完整历史) (Groupschat) ou投影 (投影) (Estado gráfico 归约器)?
- Os agentes podem modificar as instruções uns dos outros (gerente de CrewAI) ou apenas dar a mão (Swarm)?
  O agente pode mudar as suas dicas ou apenas se comunicar?

Estas três perguntas respondem a 80% de quais frameworks se encaixam num determinado problema.

> Estas três questões responderam a 80% do qual quadro se adapta a uma determinada questão.

Quando um novo quadro for lançado em 2027, faça as três perguntas. Se as suas respostas coincidem com um quadro que já usa, evite a migração. Se diferem em um eixo que você se importa, avalia. A maioria dos novos quadros é reembalar, não inovação.

> Quando o novo quadro de 2027 for lançado, as três questões sobre a sua execução são: se a resposta for adequada ao quadro que você já usa, salte para a migração.

### A visão sem Estado

Todos os primitivos, exceto o estado compartilhado, são estatais. Agente é uma função de (prompt, ferramentas).**The only stateful thing in the system is shared state.**É onde vivem todos os bugs interessantes: envenenamento da memória (Lessão 15), ordenação de mensagens, versão, contenção de escrita.

> Além do estado de partilha, cada idioma original é inestatável.**系统中唯一有状态的东西是共享状态。**É o que acontece com todos os bugs interessantes.

Esta visão impulsiona a estratégia de depuração: quando um sistema multi-agente se comporta mal, olhe primeiro para o estado compartilhado. O conjunto de mensagens está envenenado? As gravações estão ordenadas corretamente? O esquema está sendo respeitado? Agentes sem estado raramente causam bugs sutis; o estado compartilhado as causa constantemente.

> Essa percepção é impulsionada por uma estratégia de regulação: quando muitos agentes comportam-se de forma anormal, primeiro veja o estado de partilha.

Os quadros que escondem o estado compartilhado (Swarm) empurram o problema para o chamador.

> 藏共享状态的框架(Swarm) vai levar o problema para o usuário;;集中化它的框架(Langgraph 检查点、AutoGen 池) faz com que seja verificável, mas vai transferir os custos de coordenação para o estado de partilha para realizar o

### Anatomia de um único primitivo

#### Agente .

```
Agent = (system_prompt, tools, model, optional_name)
```

Não há memória, não há estado, dois agentes com o mesmo sistema de comando e ferramentas são intercambiáveis, tudo que parece ser um estado de agente é em estado compartilhado ou o protocolo de transferência.

> 没有记忆――没有状态――具有相同系统提示和工具的两个代理是可互换的――看起来就像每个代理状态的一切实际上都在共享状态或交互协议中――

Isto é contra-intuitivo, mas poderoso: agentes apátridas são triviais paralelarizáveis, reiniciáveis e trocáveis.

> É contra-intuitivo, mas forte: agente sem estado pode ser facilmente combinado, reinicializado e substituído. Você pode iniciar 100 cópias do mesmo agente, e seu comportamento é completamente o mesmo.

#### Transmissão

```
Handoff = (from_agent, to_agent, reason, payload)
```

São três as implementações que dominam:

> Três tipos de realização:

- **Function return** a ferramenta retorna o próximo agente. Este é o padrão OpenAI Swarm. Os agentes carregam roteamento em seus esquemas de ferramentas.
  Tradução:**函数返回** 工具返回下一个 Agent── é o modelo do OpenAI Swarm── Agente em seu modelo de ferramentas transportando-se através da sua rotação──
- **Graph edge** LangGraph. As bordas são declarativas. O LLM produz um valor; uma condição seleciona o próximo nó.
  Tradução:**图边** LangGraph──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection** AutoGen GroupChat. Uma função selector (às vezes uma chamada de LLM) lê o grupo e escolhe quem fala a seguir.
  Tradução:**发言者选择** AutoGen GroupChat。 seleccionador função( sometimes itself is LLM 调用)

#### Estado comum

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

Em geral, são mais frequentes: artefatos estruturados (exportações de tarefas CrewAI), conteúdo tipado (redutores de LangGraph), memória externa (MCP, vector DB).

> Pelo menos uma lista de notícias.

A forma do estado compartilhado determina quais tipos de coordenação são possíveis. Uma lista de mensagens plana torna a transmissão fácil, mas o filtro específico de papel difícil. Um esquema tipado torna o filtro trivial, mas requer design antecipado. Não há almoço gratuito.

> O formato do estado de comunhão determina o que é coordenação possível.

Duas topologias: **full pool**(cada agente vê todas as mensagens) e **projected**(agentes vejam uma visão de escala de papéis). Pools completos são simples e escalão mal. Pools projetados escala mas requerem um projeto de esquema antecipado.

> 两种拓:**完整池**(cada agente 看到每条消息) e**投影**(Agente vê o âmbito de roteiro) ⋅ total de uma piscina simples mas extensível diferença ⋅ projeção de uma piscina pode ser expandida mas precisa de um modelo de fase anterior de design ⋅

#### Orquestra

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Quatro sabores:

> Quatro tipos:

- **Static** o gráfico é fixado no tempo de construção (Deterministic LangGraph, CrewAI Sequential).
  Tradução:**静态** 图在构建时固定(Langgraph 确定性、CrewAI Sequential)
- **LLM-selected** um Mestrado em Direito Legítimo lê o grupo e escolhe o próximo orador (AutoGen, CrewAI Hierarquial).
  Tradução:**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI Hierarquial)
- **Handoff-driven** o agente atual decide chamando uma ferramenta de transferência (Swarm).
  Tradução:**交接驱动** 当前 Agente 通过调用交接工具决定(Caraço) ⋅
- **Queue-driven** trabalhadores tiram de uma fila compartilhada; nenhum alto-falante seguinte explícito (arquiteturas de enxames, Matrix).
  Tradução:**队列驱动** 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作器 工作

### Que alterações ocorrem entre os quadros

Uma vez que os primitivos são fixos, as decisões de design restantes são:

> Uma vez que o idioma original está fixado, o restante de decisão de design é:

- **Memory strategy** ponto de controlo efêmero versus duradouro (ponte de controlo LangGraph).
  Tradução:**内存策略** 临时 vs 持久检查点 (ponte de controlo de longgraph)
- **Safety boundary** que pode aprovar uma transferência (humano no circuito).
  Tradução:**安全边界** 谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)  谁可以批准交接 ( 谁可以批准交接)   谁可以批准交接) 
- **Cost accounting** Orçamentos de tokens por agente.
  Tradução:**成本核算** Orçamento de cada agente.
- **Observability** rastrear transferências, estado persistente para repetição.
  Tradução:**可观测性** Seguir o contacto  Perdurar o estado para que seja devolvido

Todos implementáveis em cima dos primitivos. Nenhum deles é novo primitivos.

> Tudo pode ser realizado em cima do original. Não há nenhum novo original.

Quando um framework anuncia um recurso "novo" (humano-in-the-loop, retry, orçamento de token), verifique se ele realmente introduz um novo primitivo ou apenas compõe os quatro.

> Quando o framework divulga "novas" funções (quando as pessoas circulam, tentam, tentam, orçam), verifique se realmente introduziu novas linguagens ou apenas as combina.

## Construí-lo e realizei-o.
```figure
a5-primitive-radar
```

## Construí-lo

`code/main.py`Não há um LLM real. Cada agente é uma política scriptada, então o foco permanece na estrutura de coordenação.

> `code/main.py`Usando cerca de 150 páginas de Python  implementou quatro linguagens originais  Não há um LLM real  Cada Agente é uma estratégia de scripting, para manter o foco na estrutura de coordenação 

Exportação do ficheiro:

> 文件导出:

- `Agent` uma classe de dados de nome, sistema de instruções, ferramentas, função de política.
  Tradução:`Agent` 名称、系统提示、工具、策略函数的数据类──
- `Handoff` uma função que retorna um novo agente.
  Tradução:`Handoff` 返回新 Agent's function──
- `SharedState` um grupo de mensagens seguro de fios.
  Tradução:`SharedState`- Não, não.
- `Orchestrator` três variantes: `StaticOrchestrator`- Não .`HandoffOrchestrator`- Não .`LLMSelectorOrchestrator`(simulado).
  Tradução:`Orchestrator` 三种变体:`StaticOrchestrator`- Não.`HandoffOrchestrator`- Não.`LLMSelectorOrchestrator`Não, não.

A demonstração executa o mesmo pipeline de três agentes (pesquisa -> escrever -> revisão) através dos três tipos de orquestra e imprime o conjunto de mensagens no final. Você pode ver que as saídas diferem apenas em *quem escolhe o próximo*; os agentes e o estado compartilhado são idênticos em todas as corridas.

> 演示通过所有三种编排器类型运行相同三 Agent 流水线(研究 -> 编写 -> 审阅),并最后印消息池── você pode ver o output apenas em*谁选择下一个*上不同;Agent 和共享状态在所有运行中是相同的──

- É o que é ?

```
python3 code/main.py
```

A produção esperada: três corridas de orquestra, uma por padrão. Cada uma imprime o conjunto final de mensagens. A corrida dirigida por entrega chega a menos agentes se o pesquisador decidir que é feito cedo  que é o compromisso de envio de LLM em miniatura.

> 预期输出: três vezes editador de operações, cada modelo uma vez.

## Use-o com o framework implementado.

`outputs/skill-primitive-mapper.md`é uma habilidade que lê qualquer base de código multi-agente ou documento framework e retorna o mapeamento primitivo de quatro.

> `outputs/skill-primitive-mapper.md`É uma habilidade, ler qualquer outro código de agente ou documento de framework e voltar para o quadrinato.

## Envia-o . Produto .

Antes de adotar um novo framework, escreva o mapeamento primitivo para ele. Se você não puder, os documentos são incompletos ou o framework está inventando um quinto primitivo (cheque raros  para um sabor de estado compartilhado que você não viu).

> Antes de adotar o novo framework, escreva o seu original. Se não estiveres a fazê-lo, explica que o arquivo não está completo ou que o framework está a desenvolver o terceiro original.

Quando um novo membro da equipe se juntar, envie-lhe o mapeamento antes dos documentos da API. Quando as versões do framework mudarem, difere o mapeamento, não o log de mudanças.

> Quando um membro da nova equipe se inscreve, é enviado um mapeamento antes do API. Quando a versão do framework muda, é comparado ao mapeamento, em vez de mudar de dia.

## Exercícios.

1. Corra .`code/main.py`Observe como a escolha do orquestrador muda os agentes que executam.
   Tradução do inglês:`code/main.py`Três vezes. Observar como o editor escolhe o agente que funciona.
2. Implementar um quarto tipo de orquestrador: um tipo de orquestra em que os agentes compartilham o estado do trabalho.
   Tradução do inglês para tradução do inglês: implementar quarta classe de editor: que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é?
3. Pegue o LangGraph quickstart e reescreva-o como os quatro primitivos. Qual dos mapas de abstracções de LangGraph 1:1 e quais são envoltórios de conveniência?
   Chinese:将 LangGraph 快速入门改写为四个原语――Qual é o resultado do LangGraph?
4. Leia o livro de cozinha OpenAI Swarm. Identifique qual dos quatro primitivos que o Swarm faz mais ergonômico e qual ele empurra para o chamador.
   中文翻译:阅读 OpenAI Swarm 手册──识别四个原语中 Swarm 使哪个最符合人体工程学,哪个推给调用者──
5. Encontre um quadro nesta tabela que esconda o estado compartilhado inteiramente e explique o que se rompe quando os agentes precisam coordenar entre as transferências sem ler novamente o histórico.
   Tradução do inglês para tradução do inglês para inglês: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage; translanguage: translanguage: translanguage: translanguage: translanguage: translanguage: translanguage; translanguage: translanguage: translanguage: translanguage; translanguage: translanguage: translanguage: translanguage: translanguage; translanguage translanguage: translanguage) translanguage transl

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Mais leitura 延伸阅读

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) a articulação mais clara da orquestração orientada por transferências
  Tradução do idioma: OpenAI 手册:编排 Agente  例例和交接 交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) GrupoChat + seleção de oradores é a referência para a orquestração selecionada pelo LLM
  中文翻译:AutoGen 稳定文档  GroupChat + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Orquestração de bordas gráficas e estado compartilhado baseado em redução
  Chinese:LangGraph 工作流和 Agent  图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction) agentes de papel-objetivo-conhecimento, processos sequenciais/hierárquicos
  中文翻译:CrewAI 介绍  角色-目标-背景故事 Agente,Sequenciais / Hierárquicos 流程
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) a linha de AutoGen v0.2 ao vivo depois que a Microsoft mudou v0.4 para manutenção
  O que é o que é o "AutoGen" (AutoGen)
