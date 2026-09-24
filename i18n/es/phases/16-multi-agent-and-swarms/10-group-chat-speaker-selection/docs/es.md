# Grupo de chat y la selección de los oradores  grupo de charlas  seleccionar 发言人

> La orquestación de conversación compartida pone a N agentes en una conversación; una función selectora (LLM, round-robin o custom) elige quién habla después. Este es el arquetipo de conversación emergente multi-agente  los agentes no saben su papel en un gráfico estático, simplemente reaccionan a la piscina compartida. AutoGen GroupChat y AG2 GroupChat son las implementaciones de referencia: la semántica de GroupChat de AutoGen v0.2 se conservó en el tenedor AG2; AutoGen v0.4 lo reescribió como un modelo de actor impulsado por eventos. Microsoft puso AutoGen en modo de mantenimiento en febrero de 2026 y lo fusionó con el Kernel Semántico en Microsoft Agent Framework (RC febrero de 2026). El primitivo de GroupChat sobrevive tanto en AG2 como en Microsoft Agent Framework  apréndelo una vez, usalo en todas partes.

> **【中文解读】**Este episodio presenta el grupo de hablantes seleccionando más agentes para decidir quién habla, cuándo habla y cómo habla.

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多 Agent 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略:(1) 轮流制按固定顺序发言;(2) 相关性制最相关的 Agent 发言;(3) 仲裁制一个专门协调员决定谁发言──AutoGen's GroupChat 使用 LLM 作为仲裁者──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04(原语模型) 、AutoGen 基础──群聊 = N 个 Agent 共享一个对话池,发言人选择决定谁说话──
> ¿ Qué es esto ?**【类比】**群聊发言人选择 = "presidente de la conferencia"──轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = 主持人指定──AutoGen GroupChat utiliza LLM cuando es el presidente高成本但灵活──2026 Nota:AutoGen 已被微软合并并到微软代理框架,AG2是社区 fork,都保留了 GroupChat 原语──

## # El problema # # El problema #

Los gráficos estáticos (LangGraph) son excelentes cuando se conoce el flujo de trabajo. Las conversaciones reales no son estáticas: a veces el codificador pregunta al revisor, a veces al investigador, a veces al escritor. El codificación dura de cada posible entrega produce una explosión de borde.

> 静态图(LangGraph) en el trabajo flujo conocido cuando es bueno.  El verdadero diálogo no es estático.

El problema de la explosión de bordes es real: un sistema de 5 agentes con todas las posibles entregas tiene 25 bordes dirigidos. Agregue un sexto agente y tiene 36. El enfoque gráfico no se escala a conversaciones emergentes; necesita una piscina.

> 边爆炸问题是真实的:带所有可能交接的 5 Agent 系统有25条有向边――加上第六个 Agent 就有36条――图方法不能扩展到涌现的对话;你需要池――

Eso es exactamente lo que hace AutoGen GroupChat.

> Esto es lo que AutoGen GroupChat hace.

## Concepto de la esencia de la concepción

### La forma

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Cada agente ve cada mensaje y en cada turno se invoca una función de selector para elegir quién habla después.

> Cada agente ve cada mensaje. Cada turno utiliza la función selector para seleccionar al siguiente orador.

La piscina de transparencia completa es tanto la fortaleza como la debilidad de GroupChat. Fuerza: cualquier agente puede reaccionar a cualquier cosa que alguien diga. Debilidad: después de 20 vueltas, el contexto de cada agente es enorme, caro y diluido. Mitigations: proyecto de visualizaciones de alcance por agente (lección 15) o terminar temprano.

> 完全透明池既是Grouppchat的优点也是弱点. 优点: cualquier agente puede responder a cualquier cosa que diga cualquiera. 弱点:20 Runs después, cada agente de arriba abajo: enorme, caro y raro.

### Los tres sabores selectores

**Round-robin.**Ciclo fijo. Determinista. Escala linealmente en N pero ignora el contexto  un codificador obtiene el turno incluso cuando el tema es revisión legal.

> **轮询。**固定循环──确定性──按N 线性扩展但忽略上下文 Incluso si el tema es la revisión legal, el codificador también puede obtener el derecho de pronunciación──

**LLM-selected.**Una llamada a un LLM que lee el grupo reciente y devuelve el mejor próximo orador. Contexto consciente pero lento: cada turno añade una llamada de LLM. AutoGen es predeterminado.

> **LLM 选择。**调用 LLM 读取近期池并返回最佳下文发言人──上下文感知但慢: cada ronda aumenta una vez más LLM 调用──AutoGen 的默认选择──

**Custom.**Una función Python con cualquier lógica que desee. Típico: LLM-seleccionado con reglas de retroceso (por ejemplo, "siempre dar al verificador el turno después del codificador").

> **自定义。**Una función Python, usando cualquier lógica que desee.

### La API de Agente Conversable

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`Cuando un agente completa un turno, el gerente llama al selector, que devuelve al siguiente agente.

> `GroupChatManager`持有选择器──当代理 完成一轮时,管理者调用选择器,返回下一个代理──循环继续直到终止条件──

La función selector es el corazón de GroupChat. Cambiarlo, cambiar el estilo de orquestación. Selector de rotonda = determinista. Selector LLM = adaptativo. Selector personalizado = cualesquiera reglas codifiques.

> 选择器函数 选择器函数 选择器函数 选择器函数 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择器 选择 选择器 选择器 选择 选择 选择器 选择器 选择 选择 选择 选择 选择 选择 选择 选择 选择 器 选择 选择 选择 选择 器 选择 选择 选择  选择  选择   选择 选择   选择   选择     选择 选择     选择       选择                                                                                                                                                             

### Terminado

Tres patrones comunes:

> Tres tipos de modalidad:

- **Max rounds.**Tape fuerte en giros totales.
  En inglés:**最大轮数。**总轮数的硬上限──
- **"TERMINATE" token.**Los agentes pueden emitir un mensaje de sentinela; el gerente se detiene cuando aparece uno.
  En inglés:**"TERMINATE" 标记。**El agente puede enviar mensajes de la policía; el administrador puede detenerse cuando aparezca.
- **Goal-reached check.**Un verificador ligero corre cada turno y detiene la charla cuando lo haga.
  En inglés:**目标达成检查。**轻量级验证者每轮运行和完成时停止聊天──

### La división de AutoGen -> AG2 y la fusión de Microsoft Agent Framework
### Líneas de linaje: bifurcaciones y fusiones

A principios de 2025, Microsoft comenzó una reescritura importante de AutoGen (v0.4) en torno a un modelo de actores impulsado por eventos.

> A principios de 2025, Microsoft comenzó a realizar una reescritura importante en torno a AutoGen (v0.4) 社区将 AutoGen v0.2 语义分叉为 AG2, reservando las API que los primeros usuarios habían integrado 社区将 AutoGen v0.2 语义分叉为 AG2, reservando la API de los primeros usuarios 模型已经集集集的.

El tenedor fue necesario porque la versión 0.4 rompió la compatibilidad hacia atrás de manera fundamental.`GroupChat`¿ Qué ?`ConversableAgent`, y `GroupChatManager`La API es estable, mientras que la versión 0.4 introduce nuevas primitivas basadas en eventos. Ambas líneas se mantienen activamente a partir de 2026.

> La división es necesaria, ya que la versión 0.4 en aspectos básicos destruyó la compatibilidad hacia atrás.`GroupChat`¿Qué es esto?`ConversableAgent`Y `GroupChatManager`API 稳定, mientras que v0.4  introduce nuevos eventos driven原语──截至 2026年,两条线都积极维护──

En febrero de 2026, Microsoft anunció que AutoGen pasaría al modo de mantenimiento, con el modelo de actores impulsado por eventos fusionándose en **Microsoft Agent Framework**El concepto de GroupChat sobrevive en ambas pistas; los detalles de implementación difieren. AG2 es el código preferido en el ascensor para el código compatible con v0.2.

> 2026 年 2 月, Microsoft anunció AutoGen 进入维护模式,事件驱动 actor 模型合并到 **Microsoft Agent Framework**(R.C.,现已与语义核心合并) ――GroupChat 概念在两个轨道中存活;实现细节不同──AG2 是 v0.2 兼容代码的首选上游──

La lección: la superficie de la API dura más que los frameworks. El código escrito contra la API de GroupChat de AutoGen v0.2 en 2024 sigue funcionando sin cambios a través de AG2 en 2026.

> En el marco de la aplicación de la API, el código de código de la API para el grupo de chat se modificó en 2026 a través de AG2.

### Cuando GroupChat se ajusta

- **Emergent conversations.**No quieres pre-cable cada posible próximo altavoz.
  En inglés:**涌现对话。**Tú no quieres conectar con el próximo hablante de cada uno de nosotros.
- **Role-mixing tasks.**El codificador pregunta al investigador, el investigador pregunta al archivista, el archivista pregunta al codificador.
  En inglés:**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器──流程不是DAG──
- **Exploratory problem-solving.**Piensa en "reunión de tormenta cerebral", no en "línea de montaje".
  En inglés:**探索性问题解决。**想想"头脑风暴会议", en lugar de "装配线" (la línea de montaje)

### Cuando falla

- **Strict determinism.**El selector de LLM puede ser inconsistente, el mismo prompt, diferentes ejecuciones, diferentes oradores siguientes.
  En inglés:**严格确定性。**LLM 选择器可能不一致──相同提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**Los agentes se aplazan a quien hable con más confianza.
  En inglés:**谄媚级联。**El agente se somete a los más seguros de su palabra.
- **Context bloat.**Cada agente lee cada mensaje; después de 10 vueltas el contexto es enorme.
  En inglés:**上下文膨胀。**Cada agente lee cada artículo de la serie de fotos de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de
- **Hot speakers.**Un agente domina la conversación porque el selector favorece sus especialidades.
  En inglés:**热发言者。**Un agente, el principal, dirige el diálogo, ya que el selector se orienta hacia su especialidad.

### El chat de grupo vs supervisor

Las mismas primitivas, diferentes valores predeterminados:

> Como se dice en el texto original, diferente:

- Supervisor: un agente planea y otros ejecutan.
  El agente de selección es un agente de control.
- Chat de grupo: todos los agentes son pares; selector es una función sobre el pool compartido.
  El grupo de conversaciones: todos los agentes es el mismo; el selector es la función en el grupo de distribución.

Ambos usan las cuatro primitivas de la Lección 04.

> 两者都使用课04的四个原语──群聊默认使用LLM 选择的编排和全池共享状态──

El control de los planes de trabajo es un proceso de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo

> 监督者和群聊之间的选择主要是关于*谁持有计划*──监督者:一个代理 拥有计划并委派──群聊:计划是隐式的,从对话中涌现──前者更可控;后者更灵活──

## Construye y realiza.
```figure
swarm-speaker
```

## Construye el mismo

`code/main.py`La aplicación de un grupo de chat desde cero en stdlib. tres agentes (codificador, revisor, gerente), variantes rotundas y LLM seleccionadas, y una terminación en un`TERMINATE`- Sí, es un símbolo.

> `code/main.py`En el caso de los programas de formación, el programa de formación de los estudiantes de la universidad de la Universidad de Madrid, el programa de formación de los estudiantes de la universidad de la Universidad de Madrid, el programa de formación de los estudiantes de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de formación de la universidad de la universidad de la Universidad de Madrid, el programa de la Universidad de Madrid, el programa de la Universidad de Madrid, el programa de la Universidad de Madrid, el programa de la Universidad de Madrid, el programa de la Universidad de Madrid, el programa de la Universidad de la Universidad de Madrid, el programa de la Universidad de Madrid, el cual se desarrolla en el año pasado.`TERMINATE`标记上终止──

La demostración imprime la transcripción de la conversación más el rastro de decisión del selector para ambas variantes.

> 演示印打对话记录以及 两种变体的选择器决策追踪──

## Usalo con el marco de ejecución

`outputs/skill-groupchat-selector.md`Configura un selector de GroupChat para una tarea dada  round-robin vs LLM-select vs custom, y qué entradas selector (mensajes recientes, especialidades de agente, recuentos de turno) utilizar.

> `outputs/skill-groupchat-selector.md`Para determinar la asignación de tareas GrupoChat  seleccionador 轮询 vs LLM 选择 vs 自定义, así como usar qué seleccionador输入(最近消息、Agent 专长、轮次计数) ⋅

## Envíe el producto .

Lista de control:

> 检查清单:

- **Max rounds cap.**Siempre. 10-20 para tareas típicas.
  En inglés:**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**Las curvas de pista por agente; alerta cuando el desequilibrio exceda un umbral.
  En inglés:**发言者平衡指标。**Seguir las órdenes de cada agente, cuando el equilibrio exceda de la cantidad de tiempo que se le da.
- **Termination token.** `TERMINATE`o un agente verificador dedicado.
  En inglés:**终止标记。** `TERMINATE`O agente de verificación especializado.
- **Projection or scoped memory.**Después de ~ 10 mensajes, considere dar a cada agente solo una vista de alcance para evitar la hinchazón de contexto.
  En inglés:**投影或范围内存。**Después de 10 años, considere que cada agente sólo tiene un alcance de visión para evitar la inflación de la información.
- **Selector logging.**Para las variantes seleccionadas en el LLM, registre tanto la entrada del selector como su elección.
  En inglés:**选择器日志。**对于LLM 选择变体,记录选择器的输入和选择――否则调试不可能――

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Comparar la conversación entre el round-robin y el LLM. ¿Cuál agente domina en cada uno?
   Traducción:运行`code/main.py`◊ Comparar consultas y consultas con el LLM  seleccionar en diálogo ◊ En cada modelo, ¿qué agente ocupa la posición dominante?
2. Añadir una regla de "máximo habla por agente" en el selector. ¿Cómo afecta a la transcripción?
   En inglés, se puede añadir "cada agente mayor número de veces que pronuncia" en un selector.
3. Implementar una terminación alcanzada: detenerse cuando el revisor regrese "aprobado". ¿Con qué frecuencia se activa antes del límite redondo?
   Traducción: Cuando el revisor regresa a la "aprobación" se detiene. ¿Cuánto tiempo hace que se inicie el proceso?
4. Lea los documentos estables de AutoGen en GroupChat. Identifique el selector predeterminado utilizado por `GroupChatManager`¿ Qué ?
   En el lenguaje chino, el lenguaje de la lengua se traduce en inglés como "AutoGen".`GroupChatManager`Uso de la máquina de elegir por escrito.
5. Lea el repos AG2 y compare su v0.2 GroupChat con la versión impulsada por eventos v0.4. ¿Qué propiedades concretas (transmisión, tolerancia a fallos, composibilidad) añade v0.4?
   China 翻译:阅读 AG2 仓库并比较其 v0.2 GroupChat con v0.4 事件驱动版本──v0.4 添加了什么具体属性(吞吐量、容错、可组合性)?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Más Leer más Leer más

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) la aplicación de referencia
  中文翻译:AutoGen 群聊文档  参考实现
- [AG2 repo](https://github.com/ag2ai/ag2) comunidad AutoGen v0.2 continuación
  中文翻译:AG2 仓库  社区 AutoGen v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) el sucesor fusionado, RC febrero 2026
  中文翻译:Microsoft Agent Framework 文档  合并后的继任者,2026 年 2 月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) el sucesor fusionado, RC febrero 2026
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) Detalles de reescribir el modelo de actor impulsado por eventos
  中文翻译:AutoGen v0.4 发布说明  事件驱动 actor 模型重写详情
