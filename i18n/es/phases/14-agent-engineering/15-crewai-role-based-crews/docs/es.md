# CrewAI: Equipos basados en el papel y flujos
# Equipos de agentes basados en el papel  Roles, tareas, procesos

> Cuatro primitivas: agente, tarea, tripulación, proceso. Dos formas de nivel superior: equipos (autónomo, colaboración basada en roles) y flujos (evento-driven, determinista). CrewAI es la implementación de referencia de 2026, y sus documentos son contundentes: "para cualquier aplicación lista para la producción, comience con un flujo".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 14 (Actor Model) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Nombre a los cuatro primitivos de CrewAI (Agencia, tarea, tripulación, proceso) y lo que cada uno posee.
- Distinguir el proceso de Consenso secuencial, jerárquico y planeado; elegir uno por carga de trabajo.
- Distinguir a los equipos (basados en roles autónomos) de los flujos (determinísticos basados en eventos) y explicar la recomendación de producción de los docentes.
- Herramientas de alambre con el `@tool`decoratora y`BaseTool`Subclase; razonamiento sobre las salidas estructuradas vs texto libre.
- Nombre de los cuatro tipos de memoria CrewAI y cuando cada uno paga.
- Implementar un equipo de tres agentes (investigador, escritor, editor) que produzca un resumen.
- Detecta los tres modos de falla de CrewAI: Inflación rápida, impuestos de gerente-LLM, entregas frágiles.

## El problema es la introducción del problema

Los equipos que adoptan marcos multi-agentes se encuentran en la misma pared. "La colaboración autónoma" suena bien en una demostración. Luego un cliente presenta un error y necesitas una reproducción determinista. O las finanzas preguntan cuánto cuesta un equipo enrutado por LLM por carrera. O en la llamada necesita saber qué agente se detuvo a las 3 am.

>  El equipo de un marco multiagente se encuentra en el mismo muro.  "Cooperación autónoma" en la presentación suena genial.  Luego el cliente propone un error, necesita una reinstalación de la certeza.  O el departamento financiero pregunta una vez a un equipo de la LLM  el funcionamiento de la ruta se necesita gastar mucho dinero.  O el personal de trabajo necesita saber qué agente se quedó en la mañana a las 3 horas de la mañana.

Los equipos de formación libre y de formación en LLM no responden a ninguna de estas preguntas, pero los DAG puros responden a todas pero pierden la forma exploratoria que necesita un agente de lluvia de ideas.

> El equipo de la LLM de forma libre no puede responder de forma clara a estas preguntas.


> **【中文解读】**La característica única de la tripulación es que la teoría de gestión de la organización se proyecta en el diseño del agente, de modo que los usuarios no técnicos también puedan definir el equipo.

> **{【拓展：CrewAI 是 2024-2025 年增长最快的 Agent 框架之一（GitHub 20k+ s...】}**CrewAI es uno de los frameworks de agentes de más rápido crecimiento de 2024-2025 años (GitHub 20k+ estrellas) ⋅ su punto de venta central es bajo código Agent 协作 通过 YAML 配置文件定义 Agent 角色和任务流──CrewAI 支持两种模式:Crew 预定义角色团队) 和 Flow 动态工作流 (Flow 动态工作流) ─企业用户 (尤其是非技术团队) 特别青其直观的角色定义方式──
La división de CrewAI es honesta sobre el comercio. equipos para el trabajo colaborativo, basado en el papel, exploratorio. flujos para la producción impulsada por eventos, propiedad de código, auditable. El mismo marco, dos formas, elegir por superficie.

> La división de la EIA se basa en este peso. El equipo utiliza el método de colaboración, el trabajo exploratorio basado en el papel. El flujo utiliza el movimiento de eventos, el control de códigos, el medio ambiente de producción auditable.

> ¿ Qué es esto ?**【前置】**必须先掌握:Fase 14·12 Antropic Workflow Patterns) CrewAI's Flow就是这些模式的实现,Crew is"自主版"工作流;以及Fase 14·14 Actor Model) Crew 内部的代理 协作本质上是消息传递──还需要理解Pydantic(结构化输出验证),因为任务的`output_pydantic`Es el acuerdo central.

## El concepto central.

### Cuatro primitivos

La superficie de la tripulación es pequeña, memorizad esto y el resto está configurado.

> La interfaz de la tripulación es muy pequeña.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

- **Agent.** `role + goal + backstory + tools + (optional) llm`La historia de fondo es cargadora. modela el tono, el juicio, cuando el agente se detiene. Las herramientas son funciones que el agente puede llamar (más abajo).

> ¿ Qué es esto ?**【类比】**El objetivo es KPI, la historia de fondo es la cultura empresarial del cerebro, "es un experto en IBM durante 20 años, con especial atención en la rigor"...**关键洞察**La historia de fondo no es un decorado, realmente afectará el estilo de juicio de LLM.
- **Task.** `description + expected_output + agent + (optional) context + (optional) output_pydantic`Una unidad de trabajo reutilizable.`expected_output`Es el contrato.`context`En el caso de las actividades de gestión de los datos, el número de datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de los datos de gestión de datos de la gestión de datos de la gestión de datos de datos de la gestión de datos de datos de la gestión de datos de datos de datos de la gestión de datos de datos de datos de datos de la gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de cuyo sitio web.`output_pydantic`fuerza una forma estructurada.
- **Crew.**Container, posee la lista de`agents`, la lista de `tasks`, el `process`, y opcionales `memory`¿ Qué es eso ?`verbose`¿ Qué es eso ?`manager_llm`configuración.
- **Process.**Estrategia de ejecución: secuencial, jerárquico, consenso (planificado).

Los agentes no se ven directamente, las tareas son de referencia, la tripulación secuencia las tareas, el proceso decide quién elige la siguiente tarea, ese es todo el modelo mental.

> Agente 间不直接见彼此──Task 引用 Agente──Equipo 排列任务顺序──Proceso que decide quién ejecuta la siguiente tarea──Toto es el modelo intelectual completo──

> **Validated against**CrewAI 0.86 (2026-05). Las versiones más recientes pueden renombrar o fusionar los tipos de proceso; compruebe el [CrewAI Processes docs](https://docs.crewai.com/concepts/processes)antes de depender de una forma específica.

### Secuenciales vs Jerárquicos vs Consenso

- **Sequential.**Las tareas se ejecutan en orden de declaración.`context`El costo más bajo, más predecible, se utiliza cuando se fija el pedido.
- **Hierarchical.**Un agente gerente (llamada separada de LLM) rutas entre los especialistas.`manager_llm`Configurar o un error predeterminado. El administrador selecciona la siguiente tarea cada ronda y puede rechazar o redirigir.
- **Consensus.**Los documentos reservan el nombre para un futuro proceso basado en el voto.

Hierarquical añade una llamada de LLM por ronda (el gerente) en la parte superior de cada llamada especializada. El costo de las fichas puede triplicar en una carrera de cinco pasos. Pague solo cuando necesite el enrutamiento.

> ️ **【易错点】**See CrewAI 文档示例都使用等级模式就跟随使用──**后果**Cuentas de trabajo:                                                                                                                                                                                                                                                             **一行修复**Se puede calcular el tiempo de ejecución de las tareas en el orden de trabajo.

> El modelo de nivel aumenta la cantidad de LLM en cada ronda de la sesión de los especialistas. En los cinco pasos de la sesión, el gasto de los tokens puede aumentar tres veces.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Los equipos contra los flujos

Este es el marco con el que los doctores lideran en 2026.

> Este es el marco más central del arquivo de 2026:

- **Crew.**La autonomía impulsada por el LLM. El marco elige la forma en el tiempo de ejecución. Es bueno para: investigación, lluvia de ideas, primeros proyectos, dondequiera que el camino sea parte de la respuesta. Es difícil de reproducir. Es difícil de probar. Es barato para el prototipo.
- **Flow.**Grafico basado en eventos que posees.`@start`marca la entrada. `@listen(topic)`Es un paso que dispara cuando otro paso emite ese tema. Cada paso es Python simple (puede llamar a un equipo internamente).

Las recomendaciones de producción de los doctores para 2026: comience con un flujo.`Crew.kickoff()`El flujo te da el rastro de auditoría, la tripulación te da la exploración.

> 文档 2026 年的生产建议:从流开始――当自主性值其成本时,将船员作为 作为`Crew.kickoff()`调用嵌入 Flow 步骤中. Flow 提供审计追踪,Crew 提供探索能力.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Integración de herramientas

Hay tres formas de darle a un agente una herramienta.

> Hay tres formas de dar a un agente un instrumento. Elige el más simple.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

1. **`@tool` decorator.**Las funciones puras se convierten en herramientas. La firma es el esquema; la cadena de documentos es la descripción que el LLM ve. Lo mejor para los ayudantes únicos.

   ```python
   from crewai.tools import tool

   @tool("Search the web")
   def search(query: str) -> str:
       """Return top results for the query."""
       return run_search(query)
   ```

2. **`BaseTool` subclass.**Herramienta basada en clases con esquema de args explícito, soporte de asíncrono, retries. Utilice cuando la herramienta tiene estado (un cliente, una caché) o necesita args estructurados.

   ```python
   from crewai.tools import BaseTool
   from pydantic import BaseModel

   class SearchArgs(BaseModel):
       query: str
       limit: int = 10

   class SearchTool(BaseTool):
       name = "web_search"
       description = "Search the web and return top results."
       args_schema = SearchArgs

       def _run(self, query: str, limit: int = 10) -> str:
           return self.client.search(query, limit=limit)
   ```

3. **Built-in toolkits.**CrewAI envía adaptadores de primera parte: `SerperDevTool`¿ Qué ?`FileReadTool`¿ Qué ?`DirectoryReadTool`¿ Qué ?`CodeInterpreterTool`¿ Qué ?`RagTool`¿ Qué ?`WebsiteSearchTool`- Un cable con una importación.

Las salidas estructuradas utilizan Pydantic.`output_pydantic=MyModel`La respuesta de la MLL contra el modelo y o bien obliga o retenta.`expected_output`las salidas de texto libre son buenas para los borradores; las salidas estructuradas son lo que los flujos aguas abajo pueden consumir.

>  Struktur化输出使用 Pydantic──在 任务 上传入 `output_pydantic=MyModel` El equipo de trabajo de acuerdo con el modelo de experiencia del LLM, no coincide con el cambio obligatorio o el retiro.`expected_output`字符串使用──自由文本输出适合草稿; estructurada输出才是下游流 可以消费的──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Cuchillos de memoria

CrewAI saca cuatro tipos de memoria de la caja.

> La tripulación ofrece cuatro tipos de recuerdos.

> **Validated against**CrewAI 0.86 (2026-05). Las últimas versiones tratan todo a través de un sistema unificado `Memory`El modelo conceptual de abajo sigue vigente, pero la superficie de la clase pública puede colapsar a una sola`Memory`punto de entrada en versiones más recientes; comprobar [CrewAI memory docs](https://docs.crewai.com/concepts/memory)para la API actual.

- **Short-term.**Puente de conversación en una sola carrera.
- **Long-term.**Persistido a través de ejecuciones. Almacenado en un vector DB (Chroma por defecto, intercambiable). Recuperado por similitud con la tarea actual.
- **Entity.**"El cliente X está en el plan empresarial" Es clave por entidad, no por similitud.
- **Contextual.**Recuperación en tiempo de montaje, extrae la memoria relevante en el momento en que el agente la necesita, no precargada.

Habilitar a la tripulación con `memory=True`El sistema de memoria de CrewAI es uno de los lugares donde CrewAI gana su mantenimiento frente a los marcos más delgados; LangGraph puro requiere que usted cable de cada uno de ellos usted mismo.

> En la tripulación arriba pasando `memory=True`O según el tipo de configuración para activar. Por tu configuración de embebidos  proveedor de apoyo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Cuando el CrewAI se ajuste
### Cuando los equipos basados en el papel se ajustan

- De tres a seis agentes con roles nombrados y un flujo de trabajo colaborativo.
- En el caso de los servicios de gestión de la empresa, el valor de la empresa es el valor de la empresa.
- En cualquier lugar el equipo es más feliz leyendo .`role + goal + backstory`que leer una definición de gráfico.

### Cuando no lo hacen

- Los DAG deterministas con orden estricto. Utilice LangGraph (lección 13). La forma del gráfico es la abstracción correcta; el marco de rol de CrewAI es la fricción.
- Los presupuestos de latencia subsegundos. Jerárquico añade viajes de ida y vuelta. Incluso Sequential serializa las instrucciones que incluyen historias de fondo y salidas anteriores.
- Los bucles de agente único. Salta el marco; un bucle de agente (lección 1) más un registro de herramientas es más corto.

La lección 17 (Tradeoffs de Marco de Agentes) expone esto en una matriz.

> Se trata de un proyecto de investigación que se desarrolla en el ámbito de la inteligencia artificial.

> ¿ Qué es esto ?**【困惑】**P: CrewAI 文档说"生产环境从流动开始", pero yo veo YouTube 教程全是 Crew 例子, ¿qué es realmente该信谁? A: 信文档。YouTube 教程偏向示范效果(Crew自主协作看起来更酷), pero el ambiente de producción es lo que se necesita**可重放、可审计、可监控** Estos sólo Flow 能给──建议路径: Use Crew 做原型验证思想 (((一两小时搞定),稳定后用Flow 重写为生产版本──Crew 不是不能用,而是不能直接上生产──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Forma de dependencia

Independiente de LangChain. Python 3.10 a 3.13. utiliza `uv`Cuenta de estrellas: mira[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)La integración de AWS Bedrock está documentada; los puntos de referencia de los proveedores informan de una velocidad sustancial frente a LangGraph en las cargas de trabajo de QA, pero la metodología (dataset, hardware, métrica de evaluación) no se publica, por lo que tratar los números de los proveedores de marco como direccionales.

> No depende de LangChain. Apoyo Python 3.10 a 3.13.`uv`包管理──AWS Bedrock 集成已有文件; proveedor基准测试报告称在QA 工作负载上有显著加速,但方法论(数据集、硬件、评估指标) no se ha abierto, por lo tanto, los datos del proveedor marco serán sólo para referencia──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

### Cuando este patrón va mal

- **Prompt-bloat from backstories.**Una historia de fondo de 2000 palabras por agente y un equipo de cinco agentes quema el presupuesto de contexto antes de la primera llamada de herramienta. Mantenga las historias de fondo de menos de 200 palabras.

> **背景故事导致的提示膨胀。**Cada historia de fondo de Agente 2000 palabras, además de cinco equipos de Agentes, se ha consumido en el presupuesto de la primera herramienta de la primera llamada.
- **Manager-LLM token tax.**El proceso jerárquico agrega una llamada de LLM del gerente antes de cada llamada especialista. En un equipo de cinco tareas que es seis llamadas de LLM en lugar de cinco, y la llamada del gerente lleva la lista completa de tareas más las salidas anteriores.

> **管理者 LLM 的 Token 税。**El modelo de nivel aumenta una vez antes de la convocatoria de expertos. El equipo de cinco tareas se convierte en seis veces de la convocatoria de LLM en lugar de cinco, y el modelo de gestión lleva una lista completa de tareas y su salida previa.
- **Brittle handoffs.**La tarea N's `expected_output`La tarea N+1 lo lee como `context`La LLM produjo cuatro, los agentes de la corriente baja, los ad-libs.`output_pydantic`En la tarea N, la tarea N+1 lee un objeto mecanografiado, no texto libre.

> **脆弱的交接。** misión N  `expected_output`Es un "gráfico" de tareas N+1 que se ejecutará como `context`读取并尝试解析三个部分──LLM 生成四个──下游 Agente 即兴发挥──用 `output_pydantic`修复任务 N,让任务 N+1 读取类型化对象而非自由文本。
- **Crew-as-prod.**El equipo de forma libre se envía a la producción sin envoltura de flujo. La variabilidad de salida es alta; la repetición es imposible; en la llamada no puede diferenciar una carrera mala contra una buena.

> **Crew 直接上生产。**没有包装成流就将自由形式 Crew 发布到生产环境――输出变异性高;无法重放;值班人员无法对抗好坏运行――使用流 包装――

## Construye y realiza.
```figure
ae-crew-vs-flow
```

## Construye el mismo

`code/main.py`Implementa versiones de STDlib de ambas formas más un equipo de tres agentes.

> `code/main.py`Utilizando el estándar, se han logrado dos formas y un equipo de tres agentes.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

Forma:

- `Agent`¿ Qué ?`Task`las clases de datos que coinciden con la superficie de la CrewAI.
- `SequentialCrew.kickoff(inputs)`ejecuta tareas en orden de declaraciones, trenzando las salidas como `context`¿ Qué ?
- `HierarchicalCrew.kickoff(topic)`Agrega un agente gerente que escoge al próximo especialista cada ronda, se detiene en "hecho".
- `Flow`con`@start`y `@listen(topic)`decoratores, un pequeño circuito de eventos, y un rastro.
- `tool(name)`Decorador que refleja el de CrewAI `@tool`¿Qué forma tiene?
- `Memory`con`short_term`¿ Qué ?`long_term`¿ Qué ?`entity`Las tiendas; la similitud burlada utiliza numpy.
- Las respuestas de LLM son cadenas codificadas con teclas de papel más prefijo de entrada.

Demo de concreto: investigador, escritor, equipo de redacción que produce un resumen sobre "ingeniería de agentes 2026".

> 具体演示:研究员、作者、编辑组成团队,生成一篇关于"agent engineering 2026"的简报──研究员获取(模拟的)来源──作者起草──编辑精炼──同一个团队通过流动 运行以展示确定性形态──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

- ¿Qué quieres decir ?

```bash
python3 code/main.py
```

Las cubiertas de rastro: secuencia de salida de la tripulación a través de los hilos `context`, equipo jerárquico con seleccionar el gerente (investigador, escritor, editor, luego "hecho"), flujo que se ejecuta los mismos tres pasos con temas explícitos (`researched`¿ Qué ?`drafted`¿ Qué ?`edited`), las llamadas a través de la herramienta`@tool`, y la memoria a largo plazo sobreviviendo a través de dos patadas.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

El rastro de la tripulación es fluido, el gerente podría en principio reordenar el rastro de flujo está fijo esa elección es la lección

> El seguimiento de la tripulación es fluido; el administrador puede reorganizarse en principio. El seguimiento de flujo es fijo.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

## Usalo con el marco de ejecución

- **CrewAI Flow**Incluso cuando el flujo es un paso que llama`Crew.kickoff()`El flujo da el límite de auditoría.
- **CrewAI Crew (Sequential)**para el trabajo colaborativo de ordenamiento claro, especialmente los primeros proyectos y los ciclos de revisión.
- **CrewAI Crew (Hierarchical)**cuando el enrutamiento depende de la salida y usted tiene cuatro o más especialistas.
- **LangGraph**(Lección 13) para máquinas de estado explícito, currículum duradero, ordenamiento estricto.
- **AutoGen v0.4**(Lección 14) para la concurrencia del modelo actor y el aislamiento de fallos.
- **OpenAI Agents SDK**(Ley 16) para los productos OpenAI-first con cargas y barandillas.
- **Claude Agent SDK**(Ley 17) para productos de primera clase con subagentes y tienda de sesiones.

## Envíe el producto .

`outputs/skill-crew-or-flow.md`Selecciona Crew vs Flow para una tarea y plantea la implementación mínima. Hard rechaza sobre temas de Crew-sin historia trasera, Flow-sin temas explícitos, Jerárquico con menos de tres especialistas.

> `outputs/skill-crew-or-flow.md`Para una tarea seleccionar el Equipo es también el flujo, y construir el mínimo de realización.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Proceso(execute策略)──

## Enlaces.

- **Backstory as flavor.**Se dan formas a las salidas, se prueban tres variantes por agente, la varianza es real, se escoge una y se congela.

> **把背景故事当装饰。**En realidad, ha formado la salida. Cada agente prueba tres variables; la diferencia es real.
- **Skipping `expected_output`.**Sin un contrato por tarea, las tareas posteriores se hacen cargo de lo que el LLM produjo.

> **跳过 `expected_output`。**没有每个任务的契约,下游任务会接收LLM 生成的任何内容──Crew 运行通过;审计失败──
- **Memory always-on.**El largo plazo escribe cada ejecución. El vector DB crece. La recuperación se hace ruidosa. El alcance escribe a tareas donde el hecho es persistente.

> **记忆始终开启。**长期记忆每次运行都写入──向量数据库不断增长──检索变杂──将写入范围限制在需要持久化事实的任务──
- **Manager prompt drift.**Si el enrutamiento se vuelve raro, deja en modo verbal y lee.

> **管理者提示漂移。**El consejo de los administradores de los modelos de nivel es oculto. Si el camino se vuelve extraño, usa el verbo 模式导出并阅读。
- **Tool side effects in Crews.**Un equipo puede llamar a una herramienta más veces de lo esperado.

> **Crew 中的工具副作用。**El equipo puede utilizar más herramientas de las que se esperaba.

## Los ejercicios.

1. Convierta a la tripulación de la secuencia a un flujo, cuenta los puntos de contacto donde baja la variabilidad, nota donde baja la legibilidad.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir memoria de entidad a la tripulación: los hechos sobre un cliente persisten a través de los arranques.
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Implemente un proceso jerárquico en el que el gerente se niega a dirigir al editor hasta que la salida del escritor tenga al menos tres párrafos.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. El cable a `BaseTool`Subclase para una búsqueda web (follando). Comparar la forma de rastreo con la `@tool`versión decorativa.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Añadir`output_pydantic=Brief`a la tarea de editor, donde `Brief`¿ Qué ?`title`¿ Qué ?`summary`¿ Qué ?`sections`. Hacer que la salida de la tarea de escritora JSON malformado una vez; verificar el comportamiento de CrewAI de nuevo en el rastreo.
  En inglés, "pensar y practicar" significa "pensar y practicar".
6. Lea la introducción de los documentos de CrewAI.`crewai`¿Qué garantías se saltaron de la versión de STDlib?
  En inglés, "pensar y practicar" significa "pensar y practicar".
7. ¿Qué rastros se perdieron en la versión de Stdlib?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "Persona" | Role + goal + backstory + tools |  |
| Task | "Unit of work" | Description + expected output + assignee + optional structured output |  |
| Crew | "Agent team" | Container for Agents + Tasks + Process |  |
| Process | "Execution strategy" | Sequential / Hierarchical / Consensus (planned) |  |
| Flow | "Deterministic workflow" | Event-driven, code-owned, testable |  |
| Backstory | "Persona prompt" | Tone and judgment shaper for the Agent |  |
| `@tool` | "Function tool" | Decorator that turns a function into a tool the Agent can call |  |
| `BaseTool` | "Class tool" | Class-based tool with args schema, retries, async support |  |
| Entity memory | "Per-entity facts" | Memory scoped to a customer / account / issue |  |
| Long-term memory | "Cross-run memory" | Vector-backed memory that survives between kickoffs |  |
| Contextual memory | "Just-in-time retrieval" | Memory pulled at the moment the Agent needs it |  |
| Manager LLM | "Router agent" | Extra LLM in Hierarchical process that picks the next task |  |
| `expected_output` | "Task contract" | String that tells the Agent (and audit) what shape to return |  |

## Más Leer más Leer más

- [CrewAI docs introduction](https://docs.crewai.com/en/introduction): conceptos y la vía de producción recomendada
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [CrewAI Flows guide](https://docs.crewai.com/en/concepts/flows): forma basada en eventos, `@start`¿ Qué ?`@listen`
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [CrewAI tools reference](https://docs.crewai.com/en/concepts/tools)¿ Qué es esto ?`@tool`¿ Qué ?`BaseTool`, herramientas incorporadas
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [CrewAI memory](https://docs.crewai.com/en/concepts/memory): a corto plazo, a largo plazo, entidad, contexto
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): cuando ayuda el multi-agente y cuando no
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): la alternativa de la máquina estatal
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
