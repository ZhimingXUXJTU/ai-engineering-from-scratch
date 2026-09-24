# Supervisor / Orquesta-trabajero patrón .

> Un agente principal planea y delega; los trabajadores especializados ejecutan en contextos paralelos y informan. Este es el patrón detrás del sistema de investigación de Anthropic (Claude Opus 4 como plomo, Sonnet 4 como subagentes), medido en +90.2% sobre el Opus 4 de un solo agente en evaluaciones internas de investigación. El post de ingeniería de Anthropic informa que el 80% de la variación en BrowseComp se explica por el uso de tokens solo  multi-agente gana en gran medida porque cada subagente obtiene una nueva ventana de contexto. Esta lección construye el patrón de supervisor desde los primitivos y cubre las lecciones de ingeniería de 2026 de las implementaciones de producción.

> **【中文解读】**Un agente ejecutivo 规划并委派任务;专业化工作器在并行上下文中执行并汇报──这是人类研究系统背后的模式(Claude Opus 4.6 主管,Sonnet 4.5 子 Agent), en la evaluación interna de la investigación sobre el único agente Opus 4.6 提升 90.2%──核心洞察:多 Agent 胜出主要因为每个子 Agent 获得独立的下文窗口80% de la diferencia de navegación 仅由代币使用量解释──

> **【拓展：Supervisor 模式 → Claude DevFleet】**Claude Code de múltiples agentes  Equipo de clasificación Claude DevFleet es el supervisor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04(4 个原语) Fase 14·01(Agente 循环) Supervisor 模式 = 多 Agent 中最常用的一种一个主管 + 多个工作器──
> ¿ Qué es esto ?**【类比】**Supervisor 模式 = "Proyecto gerente + 工程师团队"──主管(Opus) descomponer tareas+审查,工作器(Soneto) 各干一摊──Antropic 数据:BrowseComp 80% 方差由代币 使用解释多 代理 赢是因为每个子 代理有独立上下文窗口(fresh context),不是协调本身魔法──

## # El problema # # El problema #

La investigación es la tarea prototipada que fallan los sistemas de agente único. Se pregunta "¿qué cambió en los sistemas de agentes múltiples entre 2023 y 2026?" Un agente único lee cinco artículos secuencialmente, llena la mitad de su contexto con su texto, y luego tiene que razonar sobre todos ellos juntos. Olvida el primer documento cuando llega al quinto. No puede paralelalizar.

> Estudiar es un trabajo típico de un solo agente  sistema fallido. Usted pregunta "¿Qué ha cambiado el sistema de varios agentes entre 2023 y 2026?" Un solo agente  ordenan lectura de cinco artículos, con su texto llenado la mitad de la siguiente, y luego debe reflexionar sobre ellos juntos.

El fallo de un solo agente es estructural, no se puede solucionar con mejores instrucciones. No importa cuán buena sea la instrucción del sistema, la ventana de contexto se llena. La información necesaria para la síntesis (los hallazgos clave de los cinco documentos) físicamente no encaja junto con el texto bruto de los documentos.

> 单代理 失败是结构性的,无法用更好的提示修复──无论系统提示多好,上下文窗口都会填满──综合需要信息(所有五篇论文的关键发现) Físicamente imposible de comparar con el artículo original文本并存──

El patrón de supervisor corrige esto: un agente principal planifica la búsqueda, delega cada subcuestión a un trabajador y la sintetiza. Cada trabajador obtiene su propia ventana de 200k-token para una pregunta estrecha. El líder nunca ve los papeles en bruto  sólo los resúmenes de los trabajadores.

> 监督者模式修复了这个问题: un director 规划搜索,将每个子问题委派给一个工作器,然后综合―― cada trabajo器获得了自己的200k代币 窗口用于一个狭窄的问题――主持者永远不看原始论文只看工作器摘要――

El flujo de información es el diseño: los datos en bruto permanecen en contextos de trabajadores; solo los hallazgos comprimidos llegan al plomo. El contexto del plomo está dedicado a la síntesis, no a la carga de datos. Esta es la victoria arquitectónica  separación del trabajo pesado en datos del trabajo pesado en síntesis.

> 信息流是设计: los datos originales permanecen en la máquina de trabajo en el contexto; sólo los hallazgos comprimidos llegan al director.

El sistema de investigación de producción de Anthropic informa +90.2% sobre evaluaciones internas de investigación frente a un solo Opus 4.

> El informe de investigación de producción de Anthropic en la evaluación interna de un solo Opus 4 aumentó +90.2%―.

El 80% es el resultado principal: la elección de modelos, la ingeniería de las instrucciones y la elaboración de herramientas juntos explican solo el 20% de la variación. Si desea un mejor rendimiento de un agente de investigación, gasta más tokens (más subgentes, contextos más grandes) antes de ajustar las instrucciones.

> El 80% de este número es un tema de descubrimiento: el modelo de selección, la sugerencia de ingeniería y el aumento de herramientas sólo explica el 20% de la diferencia. Si quieres un mejor estudio de la actuación de un agente, gasta más tokens antes de la sugerencia de ajuste.

## Concepto de la esencia de la concepción

### El patrón

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

El plomo nunca lee las materias primas. Los trabajadores nunca ven el trabajo del otro hasta que el plomo se sintetiza. Cada flecha es una entrega con un artefacto estrecho.

> El director nunca lee el material original. El equipo nunca ve el trabajo del otro hasta que el director compleja. Cada arco es un conjunto de elementos estrechos.

Este aislamiento de la información es la elección principal del diseño. La ventana de contexto del plomo se centra en la planificación y la síntesis  nunca contaminada por 200k tokens de resultados de búsqueda crudos.

> Este tipo de aislamiento de información es el diseño central de la selección.

### Por qué gana

Tres mecanismos:

> Tres mecanismos:

1. **Fresh context per subagent.**Un trabajador que explora "FIPA-ACL herencia" no lleva los 40k tokens que el plomo gastó planificación.
   En inglés:**每个子 Agent 的清新上下文。**探索"FIPA-ACL 遗产"的工作器不携带主导人用于规划的40k token──它获得一个用于一个问题的200k窗口──
2. **Specialization via prompt.**El consejo del líder es "descompone y sintetize", no "investigue". El consejo de cada trabajador es estrecho: "Encuentra lo que ha cambiado en X". Los consejos enfocados producen resultados enfocados.
   En inglés:**通过提示专业化。**La sugerencia del director principal es "descomposición y composición", en lugar de "investigación"― la sugerencia de cada máquina de trabajo es estrecha:" averiguar qué ha cambiado X―" la sugerencia de enfoque para generar una salida de enfoque―.
3. **Parallelism.**Los trabajadores funcionan simultáneamente.`max(worker_times) + plan + synthesis`No , no .`sum(worker_times)`¿ Qué ?
   En inglés:**并行性。**工作器并发运行──挂钟时间大约是 `max(worker_times) + plan + synthesis`, en lugar de`sum(worker_times)`¿Qué es eso?

### Lecciones de ingeniería (antrópica 2025)

El post Anthropic enumera varias lecciones de producción que aún son relevantes para 2026:

> Anthropic's artículos enumeran algunas de las siguientes que todavía se aplican a la experiencia de producción en 2026:

- **Scale effort to query complexity.**Las consultas simples: un agente, 3-10 llamadas de herramientas. Las consultas complejas: 10+ agentes. El líder debe estimar esto, no el que llama.
  En inglés:**按查询复杂度缩放工作量。**简单查询: un agente, 3-10 veces herramienta调用──复杂查询:10+ 个代理──主持人必须估计这一点,而不是调用者──
- **Broad then narrow.**Descompón primero en subcuestiones amplias, luego despole más trabajadores por subcuestión si la respuesta justifica profundidad.
  En inglés:**先宽后窄。**Se desglosan en problemas de menor tamaño, si la respuesta requiere profundidad, se genera más trabajo para cada problema de menor tamaño.
- **Rainbow deployments.**Los agentes son duraderos y de estado. El verde azul tradicional no funciona. Anthropic utiliza arco iris: el lanzamiento gradual de nuevas versiones mientras las viejas se agotan.
  En inglés:**彩虹部署。**El agente es un agente de largo tiempo en funcionamiento y en estado de funcionamiento.
- **Token usage dominates.**Multi-agent es ~ 15x los tokens de un agente único. Sólo ejecutarlo cuando el valor de la tarea justifica el costo.
  En inglés:**Token 使用量占主导。**Más agente es aproximadamente 15 veces más agente solo. Sólo en el valor de la misión prueba el costo razonable para ejecutarlo.

### El giro nativo del gráfico

LangGraph originalmente envió un `langgraph-supervisor`biblioteca con un alto nivel `create_supervisor`En el año 2025 LangChain cambió la recomendación a implementar el patrón de supervisor a través de llamadas a herramientas directamente, porque las llamadas a herramientas dan más control sobre lo que el supervisor ve* (ingeniería de contexto).

> LangGraph originalmente publicó una con un alto nivel .`create_supervisor` ayudante `langgraph-supervisor`库──2025年 兰格链将建议改为通过工具调用直接实现监督者模式,因为工具调用对*监督者看什么*(上下文工程) proporcionar más control.

El cambio refleja una visión de 2025-2026: la ingeniería de contexto importa más que la ingeniería de orquestación. Lo que el supervisor ve determina lo que puede planificar.

> Este cambio refleja la visión de 2025-2026: el proyecto de la subdivisión es más importante que el de la clasificación. El supervisor ve lo que decide lo que puede planificar.

### Los modos de falla

- **Lead hallucinates the plan.**Si el plomo genera subcuestiones que no descomponen la verdadera pregunta, los trabajadores hacen investigaciones precisas sobre el objetivo equivocado.
  En inglés:**主导者幻觉计划。**Si el problema generado por el director no resuelve el problema real, el trabajo se hace con precisión en el objetivo equivocado.
- **Workers over-explore.**Sin límites explícitos de alcance, los trabajadores se desplazan más allá de su subcuestión asignada y contaminan el paso de síntesis.
  En inglés:**工作器过度探索。** sin límites de alcance definidos, el trabajo se desplazará más allá de su distribución y contaminará los pasos integrales
- **Synthesis conflicts.**Dos trabajadores devuelven hechos contradictorios. El líder debe volver a preguntar (agrega una ronda) o notar el desacuerdo explícitamente.
  En inglés:**综合冲突。**两个工作器回复矛盾的事实──主导者必须重新询问(增加一轮) 或明确记录分歧──静默选择一方是最糟糕的失败:用户永远不知道发生分歧──

### Cuando el supervisor está equivocado

- **Sequential tasks.**Si el paso 2 necesita literalmente la salida del paso 1, el paralelismo no compra nada.
  En inglés:**顺序任务。**Si el paso 2 确实需要步骤 1 的输出,并行性没有帮助──使用流水线(CrewAI Sequential、LangGraph 线性图)──
- **Simple queries.**El agente único los maneja más rápido y más barato.
  En inglés:**简单查询。**单代理更快更便宜地处理它们―― antes de la producción de la máquina de trabajo, utilizar el control de "concentrado de la cantidad de trabajo" del director―
- **Strict determinism.**El supervisor utiliza delegación seleccionada por el LLM. Los gráficos estáticos son mejores cuando la auditoría / reproducción es más importante que la adaptabilidad.
  En inglés:**严格确定性。**监督者使用 LLM 选择的委派──当审计/回放比适应性更重要时,静态图更好──

## Construye y realiza.
```figure
supervisor-hierarchy
```

## Construye el mismo

`code/main.py`Implementa un supervisor de tres trabajadores paralelos utilizando `threading`. El plomo descomponen una consulta en subcuestiones, los trabajadores se ejecutan simultáneamente en cada subcuestión y el plomo se sintetiza.

> `code/main.py`Uso `threading` Realizar un supervisor de tres equipos de trabajo  El supervisor de trabajo se dividirá en preguntas, el equipo de trabajo se ejecutará en cada uno de los equipos de trabajo  El supervisor de trabajo se ejecutará en cada uno de los equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se dividirá en tres equipos de trabajo  El supervisor de trabajo se desarrollará en dos equipos de trabajo  El supervisor de trabajo se desarrollará en un equipo de trabajo  El supervisor de trabajo se desarrollará en un equipo de trabajo  El supervisor de trabajo se desarrolla en un equipo de trabajo se desarrolla para obtener y se desarrolla en un proyecto de trabajo 

La estructura clave:

> 关键结构:

- `Lead.plan(query)`Se divide una consulta en 3 subpreguntas.
  En inglés:`Lead.plan(query)`Se dividirá la consulta en tres preguntas.
- `Worker.run(sub_q)`devuelve un resumen falso (podría ser cualquier agente que utilice herramientas en la producción).
  En inglés:`Worker.run(sub_q)`返回一个假摘要 (en producción puede ser el agente de cualquier herramienta de uso)
- `Lead.run(query)`despide a los trabajadores en hilos, juntas y sintetizas.
  En inglés:`Lead.run(query)`En línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea, en línea,

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La salida muestra el plan, los rastros de trabajadores paralelos con sellos de tiempo de inicio/finales y la síntesis final.

> 输出显示计划、带有开始/结束时间的并行工作器跟踪和最终综合―― puedes ver el tiempo de ejecución de los tres equipos de trabajo en unos 0,35 segundos, en lugar de 0,9 segundos―

## Usalo con el marco de ejecución

`outputs/skill-supervisor-designer.md`toma una consulta del usuario y produce un diseño de patrón supervisor: el prompt del sistema principal, los roles de los trabajadores, las reglas de descomposición de la subcuestión y la plantilla de síntesis.

> `outputs/skill-supervisor-designer.md`接收用户查询并生成监督者模式设计:主导系统提示、工作器角色、子问题分解规则和综合模板──在构建新的研究风格 系统之前使用──

## Envíe el producto .

Lista de verificación antes de desplegar un patrón de supervisión:

> 部署监督者模式之前的检查清单:

- **Model pairing.**El plomo en un modelo de razonamiento (clase Opus, `o3`Los trabajadores de un modelo más rápido y más barato (Sonnet, `o4-mini`¿Qué es lo que se hace?
  En inglés:**模型配对。**El autor utiliza el modelo de la teoría de la naturaleza.`o3`类) ・工作器使用更快、更便宜的模型(Sonet、`o4-mini`)。
- **Worker timeout.**Cualquier trabajador que exceda el 2x de la media de tiempo de ejecución es asesinado; el plomo o reaparece con un alcance más estrecho o procede sin él.
  En inglés:**工作器超时。** cualquier máquina de más de 2 veces el tiempo de funcionamiento se termina; el director o se reproduzca en un rango más estrecho, o no se continúa utilizando.
- **Token cap per worker.**El límite duro (por ejemplo, 10 veces la cantidad de datos de síntesis esperada) evita que un trabajador huye del presupuesto.
  En inglés:**每个工作器的 Token 上限。**硬限制 (por ejemplo, 10 veces de la entrada de trabajo integral anticipado) para evitar que el equipo de trabajo fuera controlado y se agotara el presupuesto.
- **Observability.**Trazar el plan del líder, las llamadas de herramientas de cada trabajador y la síntesis. Esta es la base para cualquier depuración post-hoc.
  En inglés:**可观测性。**Seguir el plan del director, la utilización y la integración de los instrumentos de cada equipo.
- **Rainbow rollout.**Los agentes de larga duración del estado necesitan una transición gradual de versión, no un intercambio caliente.
  En inglés:**彩虹推出。**Hay un estado de largo tiempo en el que el agente necesita una transición progresiva, no un cambio de calor.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`, luego modificar el plomo para generar 5 trabajadores en lugar de 3. Observe el efecto del reloj de la pared. ¿En qué número de trabajadores el gasto general de generar supera los ahorros paralelos en esta demostración?
   Traducción:运行`code/main.py`, y luego modificar el director para generar 5 en lugar de 3 máquinas. Observar el efecto del tiempo de la horario. En esta demostración, ¿cuánto tiempo alcanza el número de máquinas para generar más que el ahorro?
2. Implementar un tiempo de espera para los trabajadores: matar a cualquier trabajador que corra más de 0,5 segundos y hacer que el plomo sintetice los resultados restantes. ¿Qué observabilidad necesita para saber que un trabajador fue cortado?
   Traducción:                                                                                                                                                                                                                                                              
3. Si dos trabajadores devuelven respuestas contradictorias, el líder nota el desacuerdo en lugar de elegir uno. ¿Cómo detectas la contradicción sin llamar a un LLM?
   Traducción:En el conjunto de los dirigentes añadir conflictos de inspección pasos: si dos equipos devuelven la respuesta de la contradicción, el director registra分歧 en lugar de elegir uno de los dos. ¿Cómo puedes inspeccionar contradicciones en caso de no utilizar LLM?
4. Lea el artículo de ingeniería de sistemas de investigación de Anthropic.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
5. Comparar las de LangGraph `create_supervisor`¿Qué te da un mejor control sobre lo que ve el supervisor? ¿Por qué Anthropic pasa explícitamente sólo sub-respuestas y no contexto de trabajadores en síntesis?
   En inglés, traduce:`create_supervisor`¿Por qué Antropic 明确 sólo transmite la respuesta en lugar de la original en el trabajo?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Más Leer más Leer más

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) la referencia de producción para el patrón de supervisión
  Traducción:Antropico 工程  我们如何构建多 Agent 研究系统  监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) el supervisor de llamadas de herramientas es ahora el formulario recomendado
   工具调用监督者现在是推的形式  工具调用监督者现在是推的形式  工具调用监督者现在是推的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) el auxiliar heredado, todavía utilizado en la producción de 2026
  中文翻译:LangGraph 监督者参考  旧版助手, todavía en uso 2026年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Variante de supervisor basada en la transferencia
  China 翻译:OpenAI 手册  编排 Agente:例程和交接  基于交接的监督者变体
