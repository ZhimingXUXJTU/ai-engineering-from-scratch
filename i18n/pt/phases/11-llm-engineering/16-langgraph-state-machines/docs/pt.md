# LangGraph  Máquinas Estaduais para Agentes  LangGraph:Estado do Agente
# Máquinas do Estado Agente  Gráficos, Nodos, Pontos de Controle

> Um ciclo ReAct escrito à mão é um `while True`O mesmo ciclo escrito como um gráfico explícito é algo que você pode fazer ponto de controle, interromper, ramificar e viajar no tempo.

> **【中文解读】**O ciclo de reação é um.`while True` ReAct cycle é um ciclo de imagem que pode ser examinado em ponto de conservação, interrupção, separação, tempo de viagem.

> **【拓展：LangGraph→Agent工程】**LangGraph é o quadro de organização de agentes mais maduro, que irá executar o seu estado de trabalho, apoiando o seu trabalho e o seu estado de permanência.

> - Não .**【前置】**学本节前请先掌握:(1) Fase 11·09(Função chamada);(2) Fase 14·01(Agenta Loop) 理解 ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph`- Não.`langchain-core`- Não.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Enviamos um agente que chama a função. Funciona por três voltas, e depois algo vai mal: o modelo tenta uma ferramenta que retorna 500, o usuário muda de ideias no meio da tarefa, ou o agente decide reembolsar uma encomenda sem uma assinatura humana.`while True:`O loop não tem ganchos. Não pode pausar, não pode voltar a girar, e não pode se ramificar para "e se o modelo tivesse escolhido a outra ferramenta". No momento em que você envia isso para além de uma demonstração, o agente se torna uma caixa negra que ou funcionou ou não.

> Você lançou uma função para usar o Agente. Funcionou três vezes, e então surgiu um problema: o modelo tentou uma ferramenta de 500 dólares, o usuário mudou de ideias, ou o Agente decidiu retirar o dinheiro sem assinatura artificial.`while True:`O ciclo não tem nenhum efeito. Você não pode suspender-o, voltar-se para ele, ou se for dividido em "Como vai ser se o modelo escolher outro instrumento"?

O próximo passo é óbvio quando o ver. O agente já é um sistema de máquina de estado  prompt mais histórico de mensagem mais pendentes ferramentas chamadas mais a próxima ação. Faça a máquina do estado explícita: nós para "o modelo pensa", "uma ferramenta funciona", "um ser humano aprova", e bordas para as transições condicionais entre elas. Uma vez que o gráfico é explícito, o arnes recebe quatro coisas gratuitamente: checkpointing (salvar estado entre passos), interrupções (pausa para um humano), streaming (tokens de fluxo e eventos intermediários) e viagem no tempo (revoltar para um estado anterior e tentar um ramo diferente).

> Uma vez que você viu, o próximo passo é evidente. O agente é um estado de máquina. O sistema de informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação, a informação e a informação, etc.

LangGraph é a biblioteca que envia essa abstracção. Não é um quadro de agente no sentido de LangChain ("aqui há um AgentExecutor, boa sorte"). É um tempo de execução de gráfico com estado de primeira classe, persistência de primeira classe e interrupções de primeira classe. O loop de agente é algo que você desenha, não algo que você escreve à mão.
A implementação de referência desta abstracção é LangGraph. Não é um quadro de agente no sentido de LangChain ("aqui há um AgentExecutor, boa sorte"). É um tempo de execução de gráfico com estado de primeira classe, persistência de primeira classe e interrupções de primeira classe. O loop de agente é algo que você desenha, não algo que você escreve à mão.

> O LangGraph é uma biblioteca de tal abstração. Não é um quadro de agente no sentido de LangChain. É uma estrutura de estado civil igual, de perpetuidade civil igual e de interrupção civil igual.


> **【中文解读】**O LangGraph tem o principal benefício de apoiar o fluxo de controle complexo: ciclo (Agent 遇到错误时重试) 条件分支 (O agente 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (O agente 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到错误时重试) 条件分支 (Agent 遇到任务类型选择不同工具) 条件分支) 条件分支 (Agent 选择不同任务 根据任务类型 工具) 的人工审批批批批批批批批批批批批批批率 率 率 率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率率

> - Não .**【类比】**O plano de trabalho é de um modo que pode ser usado para a criação de um plano de trabalho. O plano de trabalho é de um modo que pode ser usado para a criação de um plano de trabalho.

> ️ **【易错点】**LangGraph's 3 个坑: ((1) **状态 schema 太松散**- Não .`dict`Quando o estado não tem tipo de restrição, o código de execução não está disponível.`TypedDict`Ou Modelo Pidantico  definição de Estado。(2) **条件边写得太复杂** uma borda 函数里 if/other 嵌套 5 层,调试地狱; desmantelar em vários simples bordas 函数, cada volta single一节点名──(3) **checkpoint 用 SQLite 不持久化** Reiniciar o serviço perdido; produzir postgres ou redis fazer checkpointer


## O conceito central.

> **【中文解读】**LangGraph vai LLM Agente 建模为状态机(State Machine): define state节点 (como a procura, a produção, a verificação) e a transformação (como a condição)

> **【拓展：LangGraph 与 Agent 编排】**LangGraph é um programa de programação de agências lançado pela LangChain  equipa, apoiado por:多 Agent 协作、人工介入 (Human-in-the-loop) 、持久化状态、时间旅行调试――与 CrewAI (Agen de papel) e AutoGen (Agen de vários agentes)


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

A.`StateGraph`Tem três coisas.

> `StateGraph`Há três coisas.

1. **State.**Um ditado tipado (TypedDict ou modelo Pydantic) que flui através do gráfico. Cada nó recebe o estado completo e retorna uma atualização parcial, que LangGraph combina usando um *redutor* por campo `operator.add`Para as listas que devem acumular-se, substituir-se por padrão.
   **状态。**流过图的类型化字典── cada ponto recebe o estado completo e retorna a parte actualizada──
2. **Nodes.**Funções Python `state -> partial_state`Cada um é um passo discreto: "cham o modelo", "exercem ferramentas", "resumem".
   **节点。**Python 函数 `state -> partial_state`Cada um é um passo de separação.
3. **Edges.**Transições entre nós. bordas estáticas vão para um lugar. bordas condicionais tomam uma função de roteador`state -> next_node_name`Então o gráfico pode se ramificar na saída do modelo.
   **边。**节点之间的转换──静态边去一个地方──条件边接受路由函数以在模型输出上分支──

Compile liga a topologia, anexa um checkpointer (opcional, mas essencial para a produção), e retorna um executável.`thread_id`Cada etapa da execução é um ponto de controlo com teclado .`(thread_id, checkpoint_id)`- Não .

> Você escreveu um texto. Você escreveu um texto.`thread_id`调用它──执行的每一步都会持久化一个检查点──

### As quatro superpotências

**Checkpointing.**Cada transição de nó escreve o novo estado para um armazém (em memória para testes, Postgres/Redis/SQLite para prod). Resume chamando o gráfico novamente com o mesmo `thread_id`O gráfico retoma onde parou.

> **检查点。**Cada ponto de transferência será o novo estado de escrita em armazém.`thread_id`Re-reutilizar o quadro para recuperar.

**Interrupts.**Marque um nó com `interrupt_before=["human_review"]`A sua API responde ao usuário com "esperando aprovação". Uma solicitação posterior para o mesmo `thread_id`com`Command(resume=...)`retoma a execução.

> **中断。**- Não .`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`O estado da Delta, quando acontece.`mode="messages"`Transmite os tokens do LLM dentro dos nós do modelo. `mode="values"`E você escolhe o que aparecer na interface.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI 中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`Retorna o registro completo do posto de controlo.`checkpoint_id`- Não .`graph.invoke`Ótimo para depurar ("e se o modelo tivesse escolhido a ferramenta B em vez disso?") e para testes de regressão que reproduzem traços de produção.

> **时间旅行。**返回完整的检查点日志──传进任何前所未的 `checkpoint_id`, você é do ponto de divisão.

### Os reductores são o ponto

Cada campo de estado tem um redutor. A maioria das definições são boas  um novo valor sobrepõe o antigo. Mas as listas de mensagens precisam `operator.add`As bordas paralelas combinam suas atualizações através do redutor. Se dois nós atualizar ambos`messages`E esqueceste-te do .`Annotated[list, add_messages]`O reductor é a única coisa sutil na biblioteca; faça o certo e o resto compõe.

> Cada estado tem um redutor.`operator.add`Para que novas notícias adicionem e não substituam. O Redutor é a única coisa delicada neste arquivo.

### O gráfico ReAct em quatro nós

Um agente ReAct de produção é constituído por quatro nós e duas bordas:

> Um agente ReAct de classe de produção é quatro pontos e duas bordas:

1. `agent` chama o Mestrado em Direito com o histórico de mensagem atual. Retorna a mensagem assistente (que pode conter tool_calls).
2. `tools` executa qualquer tool_call na última mensagem assistente, anexa os resultados da ferramenta como mensagens de ferramenta.
3. Uma borda condicional de `agent`que liga-se a `tools`se a última mensagem tem tool_calls, de outra forma `END`- Não .
4. Uma borda estática de `tools`De volta para `agent`- Não .

É isso. Você obtém o ciclo completo ReAct (Pensamento → Ação → Observação → Pensamento → ...) com ponto de verificação, interrupções e streaming, em aproximadamente 40 linhas de código.

> É assim. Você tem um ciclo completo de ReAct.

### StateGraph vs Enviar (fanout)

`Send(node_name, state)`O agente decide consultar três retrievers ao mesmo tempo.`Send`O LangGraph é um sistema de análise de dados que permite a execução paralela do nó-alvo; suas saídas se fundem através do redutor de estado.

> `Send(node_name, state)`Deixa-me fazer um ponto de partilha e fazer um plano.`Send`生成目標节点的并行执行; suas saídas passam pelo reduzidor de estado 合并──

### Subgrafos

Um gráfico compilado pode ser um nó em outro gráfico. O gráfico externo vê um único nó; o gráfico interno tem seu próprio estado e seus próprios pontos de controle. É assim que as equipes construem agentes de supervisor-trabalhador: o gráfico supervisor encaminha a intenção do usuário para um subgrafo de trabalhador por domínio.

> O quadro posterior pode ser um ponto de outro quadro. O quadro exterior pode ver um único ponto; o quadro interno tem seu próprio estado e ponto de verificação.

## Construí-lo e realizei-o.
```figure
l5-state-graph-ledger
```

## Construí-lo

### Passo 1: estado e nós

> 步骤 1: estado e ponto

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages`O redutor é o que faz com que a lista de mensagens se acumula em vez de ser substituída.

> `add_messages`É fazer com que a lista de notícias se acumula e não se cobre. Esqueça que é o bug LangGraph mais comum.

### Passo 2: executar com um fio

> 步骤 2: Usar o caminho de transporte.

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Cada atualização é um ditado .`{node_name: state_delta}`O frontend pode transmitir isto para a interface para que os usuários vejam "o agente está a pensar... a ligar para o search_web... obteve resultado... a responder".

> Cada novidade é.`{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"agente 思考中... 调用 search_web... 得到结果... 回答中"──

### Passo 3: adicionar uma interrupção humana no loop

Marque um nó para que a execução pare antes de ser executada.

> 步骤 3: Additional人机协作中断──标记节点使执行在运行前暂停──

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

O estado, o ponto de controlo e o fio persistem durante a interrupção.

> O estado, os pontos de verificação e os fios permanecem todos durante a interrupção, exceto durante a execução.

### Passo 4: viagem no tempo para depurar

> 步骤 4:调试用时间旅行──

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Passando .`None`como a entrada repete-se a partir do ponto de verificação dado; passar um valor acrescenta-o como uma atualização ao estado do ponto de verificação antes de retomar.

> 传入 `None`Como entrada de um determinado ponto de verificação, reinstalar; como entrada de um ponto de verificação, o valor de entrada é adicionado ao estado do ponto de verificação antes da recuperação.

### Passo 5: troca o ponto de controlo para a produção

> 步骤 5: produção ambiente substitução de inspector de pontos de

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis e Postgres estão enviados.`MemorySaver`Qualquer coisa que persista durante o reinicio quer uma loja real.

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`Para testar, qualquer coisa que precise de reinicialização precisa de armazenamento real.

## A habilidade

> Construem agentes como gráficos, não como`while True`- Os circuitos.
> Tu fizeste um agente para construir, e não para...`while True`Circulo.

Antes de chegar ao LangGraph, faça um desenho de 60 segundos:

> Antes de usar LangGraph, faça um design de 60 segundos:

1. **Name the nodes.**Cada decisão discreta ou ação de efeitos colaterais é um nó. "Agente pensa," "outil funciona," "revisor aprova," "resposta fluxos".
   **命名节点。**Cada decisão de separação ou movimento secundário é um ponto.
2. **Declare the state.**Tipo mínimo com um redutor para cada campo de lista. Não enche tudo em `messages`• campos específicos de tarefa (um trabalho)`plan`, a `budget`Contador, um `retrieved_docs`Lista) até ao nível superior.
   **声明状态。**O último tipo de ditado, cada lista de segmentos tem um redutor.
3. **Draw the edges.**Estático, a menos que o próximo passo dependa da saída do modelo.
   **画边。**A partir do próximo passo, depende do modelo de saída, ou então use o lado estático.
4. **Choose a checkpointer up front.** `MemorySaver`Para testes, Postgres/Redis/SQLite para qualquer outra coisa. Não enviar sem um  nenhum ponto de verificação significa nenhum currículo, nenhuma interrupção, nenhuma viagem no tempo.
   **提前选择检查点器。**测试用 `MemorySaver`, outros usados em Postgres/Redis/SQLite。
5. **Decide interrupts before tools run, not after.**As aprovações vão na borda para um nó de efeitos colaterais para que você possa cancelar antes de causar danos; a validação vai na borda para fora do modelo para que você possa rejeitar chamadas ruins a baixo custo.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`para a interfaz de utilização, `mode="messages"`para o streaming de nível de token dentro dos nós do modelo, `mode="values"`para instantâneos completos durante a avaliação.
   **默认使用流式输出。**

Recusar-se a enviar um agente LangGraph que não tem ponto de controlo. Recusar-se a enviar um que interrompa *após* o efeito colateral. Recusar-se a enviar um`messages`campo sem `add_messages`como seu reductor.

> Recusou a publicar não existem agentes LangGraph do ponto de inspecção. Recusou a publicar agentes interrompidos após efeitos secundários. Recusou a publicar não existem.`add_messages`Como redução de`messages`- Não.

## Exercícios.

1. **Easy.**Implementar o gráfico ReAct de quatro nós acima com uma ferramenta de calculadora e uma ferramenta de pesquisa na web. Verifique se `list(app.get_state_history(config))`Retorna ao menos quatro pontos de controlo para uma conversa de dois turnos.
   **简单。**实现上述四节点 ReAct 图,验证检查点历史记录──
2. **Medium.**Adicionar um`planner`nó que corre antes `agent`e escreve um estruturado `plan: list[str]`- Não, não.`agent`Marque os passos do plano como feito.`plan`Se o número de dados de verificação for alterado, o número de dados de verificação será alterado.
   **中等。**- Adicione um.`agent`之前运行的 `planner`节点,写入结构化计划到状态──
3. **Hard.**Construir um gráfico de supervisão que percorra entre três subgrafos (`researcher`- Não .`writer`- Não .`reviewer`) utilizando `Send`Cada subgrafo tem o seu próprio estado e ponto de controlo.`interrupt_before=["writer"]`Confirme que a viagem no tempo a partir de um ponto de controlo anterior re-corre apenas o ramo forcado.
   **困难。**Construir um supervisor, entre três`Send`- Não.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## Mais leitura 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) Referência canónica para StateGraph, reductores, checkpointers e interrupções.
  LangGraph 文档StateGraph、redutor、checkpoint器和中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) o modelo mental que esta lição usa, diretamente da fonte.
  LangGraph 概念: estado, redução, controle de pontos.
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) os detalhes das lojas Postgres/SQLite/Redis, espaços de nomes dos pontos de verificação e IDs de thread.
  LangGraph 持久化和检查点详情──
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)- Não .`interrupt_before`- Não .`interrupt_after`- Não .`Command(resume=...)`, e o padrão de edição-estado.
  LangGraph 人机协作interrupt 和 resume 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) o padrão que cada agente LangGraph implementa; leia para o raciocínio racional.
  Cada agente LangGraph realiza um modelo de ReAct.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) quais formas de gráfico (cadeia, roteador, orquestrador-trabalhador, avaliador-optimizador) preferir e quando.
  Antropic  Sobre a escolha de quais formas de desenho e quando usar o guia
- Fase 11 · 09 (Calling Function)  o primitivo de chamada de ferramenta é reutilizado por todos os nós do agente LangGraph.
  第 11 阶段 · 09(函数调用) 每个 LangGraph Agent 节点重用工具调用原语。
- Fase 11 · 14 (Modelo de Protocolo de Contexto)  Descoberta de ferramentas externas que se conectam a um LangGraph `ToolNode`através do adaptador MCP.
  第 11 阶段 · 14(MCP) 通过MCP 适配器插入 LangGraph `ToolNode`O instrumento externo é o descobrimento.
- Fase 11 · 17 (Compromissos de estrutura de agentes)  quando escolher LangGraph sobre CrewAI, AutoGen ou Agno.
  第 11 阶段 · 17(Agente 框架对比) 何时选择 LangGraph──
