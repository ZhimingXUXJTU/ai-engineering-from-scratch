# LangGraph  Máquinas Estatales para Agentes  LangGraph:Estado de Agentes
# Máquinas del Estado agente  Gráficos, nodos, puestos de control

> Un bucle ReAct escrito a mano es un `while True`El mismo bucle escrito como un gráfico explícito es algo que se puede hacer en punto de control, interrumpir, ramificar y viajar en el tiempo.

> **【中文解读】**El ciclo de la escritura de ReAct es uno.`while True` React cycle es un ciclo de tiempo que se puede revisar en un gráfico LangGraph  React cycle es un ciclo de tiempo que se puede revisar en un gráfico  React cycle es un ciclo de tiempo que se puede revisar en un gráfico  React cycle es un ciclo de tiempo que se puede revisar en un gráfico LangGraph  React cycle es un ciclo de tiempo que se puede revisar en un gráfico  React cycle es un ciclo de tiempo que se puede revisar en un gráfico  React cycle cycle cycle cycle                                                                                                                                                                                                                                                                                                                                                                                    

> **【拓展：LangGraph→Agent工程】**LangGraph es el marco de organización de agentes más maduro en la actualidad, el cual ejecutará el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, el estado de los agentes, etc.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:(1) Fase 11·09(Funación llamada);(2) Fase 14·01(Agencia de ciclo)  comprensión ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph`¿Qué es esto?`langchain-core`¿Qué es eso?

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Se envía un agente de llamada de función. Funciona durante tres vueltas, luego algo sale mal: el modelo prueba una herramienta que devuelve 500, el usuario cambia de opinión en medio de la tarea, o el agente decide reembolsar un pedido sin una firma humana.`while True:`no se puede pausar, no se puede volver a doblar, y no se puede ramificar en "qué pasa si el modelo hubiera escogido la otra herramienta". En el momento en que envías esto después de una demostración, el agente se convierte en una caja negra que o funcionó o no.

> Usted publicó una función para usar el agente. Trabajó tres vueltas, y luego surgió un problema: el modelo intentó devolver una herramienta de 500, el usuario cambió de idea en medio, o el agente decidió devolver la moneda sin firmas artificiales.`while True:`循环没有子──你不能暂停它、倒回它、或分支到"Si el modelo elige otro instrumento, ¿cómo será"── Una vez que publicas algo así en la demo, el agente se convierte en una caja negra──

El siguiente paso es obvio una vez que lo veas. El agente ya es una máquina de estado  sistema de respuesta más el historial de mensajes más llamadas de herramienta pendientes más la siguiente acción. Haga que la máquina del estado sea explícita: nodos para "el modelo piensa", "una herramienta funciona", "un humano aprueba", y bordes para las transiciones condicionales entre ellas. Una vez que el gráfico es explícito, el arnés obtiene cuatro cosas de forma gratuita: control (salvar estado entre pasos), interrupciones (pausa para un humano), transmisión (tokens de flujo y eventos intermedios) y viaje en el tiempo (reincorporarse a un estado anterior y probar una rama diferente).

> Una vez que lo ves, el siguiente paso es evidente. El agente es un estado de trabajo. El sistema de información, la información y el proceso de información.

LangGraph es la biblioteca que envía esta abstracción. No es un marco de agente en el sentido de LangChain ("aquí hay un AgentExecutor, buena suerte"). Es un tiempo de ejecución de gráfico con estado de primera clase, persistencia de primera clase y interrupciones de primera clase. El bucle de agente es algo que dibujas, no algo que escribes a mano.
La aplicación de referencia de esta abstracción es LangGraph. No es un marco de agente en el sentido de LangChain ("aquí hay un AgentExecutor, buena suerte"). Es un tiempo de ejecución de gráfico con estado de primera clase, persistencia de primera clase y interrupciones de primera clase. El bucle de agente es algo que dibujas, no algo que escribes a mano.

> LangGraph es una biblioteca de este tipo de abstracción. No es un marco de agente en el sentido de LangChain. Es un marco de trabajo con un estado de ciudadanía igual, una perpetuación de la ciudadanía igual y una interrupción de la ciudadanía igual.


> **【中文解读】**La ventaja central de LangGraph es el apoyo a un flujo de control complejo: ciclo  Agente                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

> ¿ Qué es esto ?**【类比】**El tiempo de viaje de regreso a un determinado punto de prueba es diferente de la sección de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de trabajo de la página de la página de trabajo de la página de la página de trabajo de la página de trabajo de la página de la página de trabajo de la página de la página de trabajo de la página de trabajo de la página de la página de trabajo de la página de la página de la página de trabajo de la página de la página de trabajo de la página de la página de la página de trabajo de la página de la página de la página de la página de trabajo de la página de la página de la página de trabajo de la página de la página de la página de la página de la página de la página de trabajo de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de trabajo de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página

> ️ **【易错点】**LangGraph's 3 个坑: ((1) **状态 schema 太松散**¿Qué es esto?`dict`Cuando estado 没类型约束,运行时关键 拼错发现不了;用 `TypedDict`O Modelo Pidantico  definición del Estado。(2) **条件边写得太复杂** una borda 函数里 si/otro 嵌套 5 层,调试地狱; desmantelar en varios simples bordes 函数, cada uno regresa a un solo节点名──(3) **checkpoint 用 SQLite 不持久化** Reinicio del servicio perdido; producción con Postgres o Redis hacer checkpointer


## El concepto central.

> **【中文解读】**LangGraph 将 LLM Agent 建模为状态机(State Machine): define el estado de la máquina (como la investigación, la generación, la verificación) y el cambio de la máquina (como la producción, la producción, la verificación)

> **【拓展：LangGraph 与 Agent 编排】**LangGraph es el marco de organización de la organización de LangChain, apoyado por el equipo de LangGraph.


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

¿ Qué es esto ?`StateGraph`tiene tres cosas.

> `StateGraph`Hay tres cosas.

1. **State.**Un dictado tipado (modelo TypedDict o Pydantic) que fluye a través del gráfico. Cada nodo recibe el estado completo y devuelve una actualización parcial, que LangGraph fusiona utilizando un *reducer* por campo `operator.add`para las listas que deben acumularse, sobrescribir por defecto.
   **状态。**流过图的类型化字典── cada uno de los puntos recibe el estado completo y vuelve a la parte actualizada──
2. **Nodes.**Funciones de Python `state -> partial_state`Cada uno es un paso discreto: "llamar al modelo", "ejecutar herramientas", "resumir".
   **节点。**Python  funciones `state -> partial_state` Cada uno es un paso separado
3. **Edges.**Transiciones entre nodos. los bordes estáticos van a un lugar. los bordes condicionales toman una función de enrutador`state -> next_node_name`Así que el gráfico puede ramificar en la salida del modelo.
   **边。**节点之间的转换──静态边去一个地方──条件边接受路由函数以在模型输出上分支──

Compila la gráfica. Compila se une a la topología, se une un checkpointer (opcional pero esencial para la producción), y devuelve un ejecutable.`thread_id`Cada paso de la ejecución es un punto de control con teclado .`(thread_id, checkpoint_id)`¿ Qué ?

> Usted编译图──编译绑定拓、附加检查点器并返回可运行对象──你使用初始状态和 `thread_id`调用它――执行的每一步都会持久化一个检查点――

### Las cuatro superpotencias

**Checkpointing.**Cada transición de nodo escribe el nuevo estado a una tienda (en memoria para pruebas, Postgres/Redis/SQLite para prod).`thread_id`El gráfico se repite donde se detuvo.

> **检查点。**Cada nodo se transfiere a un nuevo estado de escritura en el almacén.`thread_id`Re-reutilizar el dibujo para recuperarlo.

**Interrupts.**Marque un nodo con `interrupt_before=["human_review"]`La API responde al usuario con "esperando aprobación". Una solicitud posterior a la misma `thread_id`con`Command(resume=...)`reanudará la ejecución.

> **中断。**¿ Qué ?`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`Los estados deltas como ocurren.`mode="messages"`transmite los tokens de LLM dentro de los nodos del modelo. `mode="values"`Es el momento de elegir qué aparecer en la interfaz de usuario.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`devuelve el registro completo del puesto de control.`checkpoint_id`¿ Qué ?`graph.invoke`Y se forja desde ese punto. Es ideal para el depuración ("¿qué pasa si el modelo hubiera escogido la herramienta B en su lugar?") y para las pruebas de regresión que reproducen rastros de producción.

> **时间旅行。**返回完整的检查点日志──传进任何前所未的 `checkpoint_id`, tú desde ese punto de división.

### Los reducidores son el punto

Cada campo de estado tiene un reducidor. La mayoría de los valores predeterminados están bien  un nuevo valor sobreescribe el viejo. Pero las listas de mensajes necesitan `operator.add`Los bordes paralelos fusionan sus actualizaciones a través del reducidor. Si dos nodos actualizan ambos`messages`y te olvidaste de la`Annotated[list, add_messages]`El reducidor es la única cosa sutil en la biblioteca; hazlo bien y el resto compone.

> Cada estado tiene un reducidor.`operator.add`Para que la nueva información se añada y no se sustituya. El reducidor es lo único delicado de esta biblioteca.

### El gráfico ReAct en cuatro nodos

Un agente ReAct de producción es de cuatro nodos y dos bordes:

> Un agente de reacción de producción es cuatro puntos y dos bordes:

1. `agent` llama al LLM con el historial de mensajes actual.
2. `tools` ejecuta cualquier llamada de herramienta en el último mensaje de asistente, añade los resultados de la herramienta como mensajes de herramienta.
3. Un borde condicional de `agent`que rutas a `tools`si el último mensaje tiene herramientas_llamadas, de otro modo `END`¿ Qué ?
4. Un borde estático de `tools`De vuelta a`agent`¿ Qué ?

Así es todo. Obtienes el bucle completo de ReAct (Pensamiento → Acción → Observación → Pensamiento → ...) con puntos de control, interrupciones y transmisión, en aproximadamente 40 líneas de código.

> Así es. Usted obtiene un ciclo completo de ReAct.

### StateGraph vs Enviar (fanout)

`Send(node_name, state)`El agente decide consultar tres extractores a la vez.`Send`La función de la función de reducción de los niveles de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de los grupos de trabajo de trabajo de trabajo de los grupos de trabajo de trabajo de trabajo de trabajo de los grupos de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo

> `Send(node_name, state)`让一个节点分派并行子图── cada uno `Send`生成目标节点的并行执行; su salida a través del reducidor de estado 合并──

### Subgrafos

Un gráfico compilado puede ser un nodo en otro gráfico. El gráfico externo ve un solo nodo; el gráfico interno tiene su propio estado y sus propios puntos de control. Así es como los equipos construyen agentes supervisores de trabajadores: el gráfico supervisor rúa la intención del usuario a un subgrafo de trabajadores por dominio.

>  Compilada después del cuadro puede ser un nodo en otro cuadro. El cuadro exterior puede ver un solo nodo; el cuadro interno tiene su propio estado y punto de control.

## Construye y realiza.
```figure
l5-state-graph-ledger
```

## Construye el mismo

### Paso 1: estado y nodos

> Paso 1: estado y punto

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

`add_messages`Es el reducidor que hace que la lista de mensajes se acumula en lugar de sobrescribir.

> `add_messages`Es un reducidor de la acumulación de la lista de noticias y no de la cobertura. Olvídate de que es el bug LangGraph más común.

### Paso 2: ejecutar con un hilo

> Paso 2: con el camino de la operación.

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Cada actualización es un dictado .`{node_name: state_delta}`Su frontend puede transmitir esto a la interfaz de usuario para que los usuarios vean "el agente está pensando... llamando a search_web... obtuvo el resultado... respondiendo".

> Cada actualización es`{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"agente 思考中... 调用 search_web... 得到结果... 回答中"──

### Paso 3: añadir una interrupción humana en el circuito

Marque un nodo para que la ejecución se detenga antes de ejecutarse.

> Paso 3: Añadir personas a la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de la organización de la organización de la organización de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de

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

El estado, el punto de control y el hilo persisten durante la interrupción.

> 状态、检查点和线程在中断期间全部持久化──除了执行期间, nada está en memoria──

### Paso 4: Viaje en el tiempo para el depuración

> Paso 4:调试用时间旅行──

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Pasando .`None`Cuando la entrada se repite desde el punto de control dado, pasar un valor lo añade como una actualización al estado de ese punto de control antes de reanudar. Así es como se reproduce un agente mal ejecutado sin volver a ejecutar toda la conversación.

> 传入 `None`作为输入从给定的检查点重放;传输值则在恢复前将其作为更新添加到该检查点的状态――这就是如何在不重新运行整个对话的情况下复现一个错误的代理运行――

### Paso 5: cambiar el punto de control para la producción

> Paso 5: producción de un medio ambiente en sustitución de un inspector.

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis y Postgres están enviados.`MemorySaver`Todo lo que persiste en los reinicios necesita una tienda real.

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`Para probar todo lo que necesita reiniciar, todo lo que necesita un verdadero almacenamiento.

## La habilidad

> Construyes agentes como gráficos, no como`while True`- ¿Qué es eso?
> Usted ha construido un agente para él, y no para él.`while True`循环:

Antes de llegar a LangGraph, haz un diseño de 60 segundos:

> Antes de usar LangGraph, hacer un diseño de 60 segundos:

1. **Name the nodes.**Cada decisión discreta o acción secundaria es un nodo. "El agente piensa, " "la herramienta se ejecuta, " "el revisor aprueba, " " "los flujos de respuesta". Si no puedes enumerarlos, la tarea aún no está en forma de agente.
   **命名节点。**Cada decisión de separación o acción secundaria es un punto.
2. **Declare the state.**Tipo mínimo Dict con un reducidor para cada campo de lista. No enchufes todo en `messages`• elevar los campos específicos de las tareas (un trabajo `plan`, una `budget`Contador, un `retrieved_docs`El Consejo de Ministros de la Unión Europea ha aprobado el proyecto de ley de la Unión Europea.
   **声明状态。**La última Dicta de Tipo, cada uno de los segmentos de la lista tiene un reducidor.
3. **Draw the edges.**Esta estática a menos que el siguiente paso dependa de la salida del modelo.
   **画边。**Además del siguiente paso depende del modelo de salida, o bien utiliza el lado en estado.
4. **Choose a checkpointer up front.** `MemorySaver`No se envíe sin uno  ningún punto de control significa ningún currículum, ninguna interrupción, ningún viaje en el tiempo.
   **提前选择检查点器。**测试用    pruebas de uso`MemorySaver`, otros usados en Postgres/Redis/SQLite。
5. **Decide interrupts before tools run, not after.**Las aprobaciones van en el borde a un nodo de efecto secundario para que puedas cancelar antes de dañar; la validación va en el borde fuera del modelo para que puedas rechazar malas llamadas a bajo costo.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`para la interfaz de usuario, `mode="messages"`para la transmisión a nivel de token dentro de los nodos del modelo, `mode="values"`para las instantáneas completas durante la evaluación.
   **默认使用流式输出。**

Rechazar el envío de un agente LangGraph que no tiene un punto de control. Rechazar el envío de uno que interrumpa *después* del efecto secundario. Rechazar el envío de un`messages`campo sin `add_messages`como su reducidor.

>  Rechazar la publicación de ningún agente LangGraph de un inspector  Rechazar la publicación de un agente interrumpido después de efectos secundarios  Rechazar la publicación de ningún agente  Rechazar la publicación de un agente LangGraph  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios  Rechazar la publicación de efectos secundarios  Rechazar la publicación de un agente de detección de efectos secundarios `add_messages` Como reducidor `messages`¿Qué es eso?

## Los ejercicios.

1. **Easy.**Implemente el gráfico de cuatro nodos ReAct de arriba con una herramienta de calculadora y una herramienta de búsqueda web.`list(app.get_state_history(config))`devuelve al menos cuatro puestos de control para una conversación de dos vueltas.
   **简单。**实现上述四节点 ReAct 图,验证检查点历史记录──
2. **Medium.**Añadir un`planner`nodo que se ejecuta antes `agent`y escribe un estructurado `plan: list[str]`En el estado.`agent`Marque los pasos del plan como se ha hecho.`plan`se pierde en un currículum de control (reducidor incorrecto).
   **中等。**Añade uno en`agent`之前运行的 `planner`节点,写入结构化计划到状态──
3. **Hard.**Construir un gráfico de supervisión que se ejecuta entre tres subgrafos (`researcher`¿ Qué ?`writer`¿ Qué ?`reviewer`) utilizando `Send`Cada subgrafo tiene su propio estado y punto de control.`interrupt_before=["writer"]`Confirmar que el viaje en el tiempo desde un punto de control anterior re-correce sólo la rama bifurcada.
   **困难。**Construir un supervisor 图, entre tres 图`Send`- ¿Qué pasa?

## Términos clave .

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

## Más Leer más Leer más

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) referencia canónica para StateGraph, reducidores, puntos de control y interrupciones.
  LangGraph 文档StateGraph、reducer、checkpoint and中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) el modelo mental que utiliza esta lección, directamente de la fuente.
  LangGraph 概念: estado  reducidor 检查点器
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) el detalle de las tiendas Postgres/SQLite/Redis, los espacios de nombres de los puntos de control e identificadores de hilos.
  LangGraph 持久化和检查点详情──
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)¿ Qué es esto ?`interrupt_before`¿ Qué ?`interrupt_after`¿ Qué ?`Command(resume=...)`, y el patrón de edición-estado.
  LangGraph 人机协作interrupt 和 resume 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) el patrón que cada agente de LangGraph implementa; lea para el razonamiento de la racionalidad de rastreo.
  Cada agente de LangGraph realiza un modelo de ReAct.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) qué formas de gráfico (cadena, enrutador, orquestrador-trabajadores, evaluador-optimizador) preferir y cuándo.
  Antropic  Sobre la selección de las formas y cuándo utilizar las direcciones 
- Fase 11 · 09 (Llamada de funciones)  la herramienta-llamada primitiva cada nodo agente LangGraph reutiliza.
  Sector 11 阶段 · 09(función调用)  cada agente de LangGraph 节点 herramienta de nuevo uso调用原语。
- Fase 11 · 14 (Modelo de Protocolo de Contexto)  Descubrimiento de herramientas externas que se enchufen en un LangGraph `ToolNode`a través del adaptador MCP.
  Se trata de un programa de trabajo de la Comisión para la gestión de la información y la información sobre la información.`ToolNode`De las herramientas externas de la búsqueda.
- Fase 11 · 17 (Compromiso de marco de agentes)  cuándo elegir LangGraph sobre CrewAI, AutoGen o Agno.
  Se trata de un proyecto de investigación que se desarrolla en el ámbito de la investigación y la investigación.
