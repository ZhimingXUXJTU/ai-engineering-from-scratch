# ReWOO y Plan-y-Ejecutar: Desacoplado Planificación .

> ReAct intercalara el pensamiento y la acción en un flujo. ReWOO los separa: un plan grande por delante, luego ejecutar. 5 veces menos tokens, +4% de precisión en HotpotQA, y se puede destilar el planificador en un modelo 7B. Plan-and-Ejecutar lo generalizó; Plan-and-Act lo escalaron a la navegación web.

> **【中文解读】**ReAct en un flujo de cambios de pensamiento y acción. ReWOO los separará: primero una vez elaborar un plan completo, luego ejecutar.

> **【拓展：ReWOO → 现代 Agent 架构】**Entre los cinco modelos de trabajo de la Antropic "Building Effective Agents", el modelo de planificación-execución es uno de los principales.

> ¿ Qué es esto ?**【前置】**精通本节前请先掌握:Fase 14·01(Agent Loop / ReAct 循环)You must understand ReAct's "pensar-actuar-observar" exchange mode, porque ReWOO es para entender el token de ReAct de segunda vez de crecimiento problema; así como el concepto de gráfico básico (((DAG、拓排序), no está familiarizado con DAG 会卡在" depender de resolución" ese paso.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Explica por qué la división Planner / Worker / Solver de ReWOO ahorra tokens y mejora la robustez sobre el bucle intercaído de ReAct.
  Traducción: explica por qué el planificador/estado/busquero de ReWOO se separa de un token de ahorro de energía y no es más fuerte que el ciclo de cambio de ReAct.
- Implementar un plan DAG, un ejecutor de orden de dependencia y un solver que compone las salidas de trabajador  todos stdlib.
  En inglés, la palabra "plán de ejecución" se refiere a la forma en que se realiza el programa.
- Decidir cuándo una tarea debe ejecutarse como plan-then-execute vs. ReAct intercalados, utilizando el marco de 2026 "cinco patrones de flujo de trabajo" (Antropic).
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Reconocer cuándo se necesitan los datos de los planes sintéticos de Plan-and-Act para tareas web o móviles de largo horizonte.
  China: Identificar cuándo se necesita un plan y un plan de acción para procesar una tarea móvil.

## El problema es la introducción del problema

El ciclo de observación de pensamiento-acción-observación intercalados de ReAct es simple y flexible, pero cada llamada de herramienta tiene que llevar el contexto previo completo  incluyendo cada pensamiento anterior. El uso de tokens crece cuadráticamente con la profundidad. Peor: cuando una herramienta falla en medio del ciclo, el modelo tiene que derivar de nuevo todo el plan de la observación de errores.

> El ciclo de pensamiento-acción-observación de ReAct es simple y flexible, pero cada vez que se utiliza un instrumento, se necesita llevar un plan completo de la fase anterior, incluyendo cada uno de los anteriores.

ReWOO (Xu et al., arXiv:2305.18323, mayo 2023) notó esto y hizo una apuesta: planear todo de antemano, buscar evidencia en paralelo, componer la respuesta al final. Una llamada de LLM a planificar, N herramienta pide evidencia (puede ser paralelo), una llamada de LLM a resolver. El comercio es menos flexible (el plan es estático) para una mayor eficiencia de tokens y modos de fracaso más claros.

> ¿ Qué es esto ?**【类比】**ReWOO 像装修房子前先出施工图: diseñador una vez en una sola vez dibujar todos los procesos (规划器) 工人按图并行施工互不打扰 (工作器) 验收时把所有工序结果拼拼拼到一起结算 (求解器) ⋅ React 则像边施工边设计,每个工人都可以翻阅前面所有工人的笔记动手,所以 10 步后笔记就堆成山──

> ReWOO(Xu 等人,arXiv:2305.18323,2023 年 5 月) notó esto y propuso un esquema: primero planificar toda la tarea,并行获证,最后组合答案―― una vez LLM 调用规划、N 次工具调用获证 (可并行) 、 una vez LLM 调用求解──代价是灵活性降低(计划是静态的), pero en cambio viene mejor token 效率和更清晰的失败模式――

## El concepto central.

### Los tres papeles

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Planner produce un DAG. Cada nodo nombra una herramienta, sus argumentos y de qué nodos anteriores depende (referencias como `#E1`¿ Qué ?`#E2`Los trabajadores ejecutan los nodos en orden topológico.

> 规划器 generar un DAG. Cada nodo especifica una herramienta, sus parámetros y los precedentes de la dependencia.`#E1`¿Qué es esto?`#E2`等引用) ・工作器按拓顺序执行节点──求解器将所有内容拼拼在一起──

### ¿Por qué 5 veces menos tokens?

ReAct crece la longitud del momento linealmente con el recuento de pasos. En el paso 10, el momento contiene pensamiento 1 más acción 1 más observación 1 más pensamiento 2 más acción 2 más observación 2, etc. Cada paso intermedio también incluye redundantemente el momento original.

> La longitud de la propuesta de ReAct aumenta con el número de pasos lineares. Hasta el 10o paso, la propuesta contiene el pensamiento 1 + 行动 1 + 观察 1 + 思考 2 + 行动 2 + 观察 2, según este tipo de sugerencias. Cada paso intermedio contiene el espacio de la propuesta original.

ReWOO paga un planador de instrucciones (gran), N de trabajadores pequeños (cada uno sólo la llamada de herramienta, sin cadena), y un solver de instrucciones.

> ReWOO sólo necesita una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de resolución, una sola propuesta de resolución, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una sola propuesta de planificación, una propuesta de planificación, una propuesta de planificación, una propuesta de planificación, una propuesta de planificación, una propuesta de planificación y una propuesta de planificación, una propuesta de un proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de proyecto de

### Por qué es más robusto

Si el trabajador 3 falla en ReAct, el bucle tiene que razonar fuera del error en medio del flujo. En ReWOO, el trabajador 3 devuelve una cadena de error; el solucionador lo ve en contexto con el plan original y puede degradar con gracia. La localización del fallo es por nodo, no por paso.

> Si el trabajo 3 en ReAct falla, el ciclo debe ser pensado en medio del proceso desde el error en el proceso. En ReWOO, el trabajo 3 devuelve una cadena de error; el buscador puede ver que el error se baja en el siguiente texto del plan original.

### Destilación de planificadores

El segundo resultado del artículo: debido a que el planificador no ve observaciones, se puede ajustar un modelo 7B en las salidas del planificador de un maestro 175B. El modelo pequeño maneja la planificación; el modelo grande no es necesario en la inferencia. Esto es ahora estándar  muchos agentes de producción 2026 usan un planificador pequeño y un ejecutor grande o viceversa.

> El segundo resultado del trabajo: porque el planificador no ve los resultados observados, puedes modificar en el modelo de 175B el modelo de profesor y sacar un modelo de 7B.

> **【拓展：规划器蒸馏 → 成本优化】**Porque el planificador no necesita observaciones, se puede exportar el plan de los modelos de 175B docentes a los modelos de 7B. En el año 2026 el agente de producción utiliza generalemente la estructura mixta de "plan de modelos pequeños + gran modelo de ejecución" para optimizar el costo.

### Plan y ejecución (LangChain, 2023)
### Plan y ejecución (2023)

El post de agosto de 2023 del equipo de LangChain generalizó ReWOO en un nombre de patrón: Plan-and-Ejecute. El planificador de adelanto emite una lista de pasos, el ejecutor ejecuta cada paso, un replanificador opcional puede revisar después de observar los resultados. Esto es más cercano a ReAct que ReWOO (el replanificador trae las observaciones de nuevo a la planificación) pero conserva los ahorros de tokens.

> LangChain 团队 El artículo de agosto de 2023 generalizará ReWOO 泛化为一个模式名称:Plan-and-Execute.

### Plan y Acta (Erdogan et al., arXiv:2503.09572, ICML 2025)

Plan-and-Act escala el patrón a agentes web y móviles de largo horizonte. La contribución clave son los datos de planes sintéticos: un generador de trayectoria etiquetado produce datos de entrenamiento donde el plan es explícito. Se utiliza para ajustar a los modelos de planificador que siguen trabajando más allá de 3050 pasos en tareas similares a WebArena donde una sola trayectoria de ReAct pierde coherencia.

> Plan-and-Act extenderá este modelo a páginas web y agentes móviles de larga distancia. La contribución clave es la de un conjunto de datos de plan: un generador de rutas de marcado genera datos de entrenamiento, de los cuales el plan es evidente.

### ¿Cuándo elegir cuál

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

Guía de Anthropic de diciembre 2024: comience con lo más simple. Si la tarea es una llamada de herramienta más un resumen, no construya ReWOO. Si la tarea es una tarea de investigación de 40 pasos, no haga ReAct solo.

> ¿ Qué es esto ?**【困惑】**P: 既然 ReWOO 省5倍代币还准确,为什么不全部使用 ReWOO? A: 因为 ReWOO 的计划是"静态"的一发发就不再根据观察调整.

> Antropic 2024: desde el principio más simple. Si una tarea es un instrumento, no construya ReWOO. Si la tarea es una tarea de investigación de 40 pasos, no sólo utilice ReAct.

## Construye y realiza.

> ️ **【易错点】**实现 ReWOO 时新手最常踩的坑: olvidar el plan DAG hacer un análisis de círculo.`#E1`Depende de lo que sea .`#E2`Y ahora`#E2`Depende de lo que sea .`#E1`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,**后果**El ejecutor se encuentra en la cárcel.**一行修复**: To ordenar después de revisar el número de puntos de ordenar si es igual al número total de puntos, no igual en la balanza`CycleDetectedError`¿Qué es eso?
```figure
rewoo-plan
```

## Construye el mismo

`code/main.py`Implementa un juguete ReWOO:

> `code/main.py`实现 una juguete ReWOO:

- `Planner` una política guionada que emite un plan DAG desde una solicitud.
  En inglés:`Planner` de la estrategia de guión de la DAG de la propuesta de generación de planes.
- `Worker` Envía la llamada de herramienta de cada nodo a través del registro.
  En inglés:`Worker`                                                                                                                                                                                                                                                              
- `Solver` Compuesto escrito que lee pruebas y produce una respuesta final.
  En inglés:`Solver`读取证据并生成最终答案的脚本组合器──
- Resolución de dependencia  referencias como `#E1`se sustituyen por resultados de trabajadores anteriores.
  En español: depender de la resolución`#E1`La referencia fue sustituida por anterior de trabajo.

La demostración responde a "Cuál es la población de la capital de Francia, redondeada a millones?" utilizando un plan de dos pasos: (1) buscar la capital, (2) buscar la población, y luego resolver.

> 演示回答"¿Cuánta población tiene la capital francesa, cuatro cuantos ingresan a millones?"

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra el plan completo primero, luego los resultados del trabajador, luego la composición del solver. Comparar el recuento de tokens (imprimiremos un recuento de caracteres aproximado) con una ejecución interleaved de estilo ReAct  ReWOO gana en este tipo de tarea estructurada.

> 轨迹 primero muestra el plan completo, luego es el resultado del trabajo, finalmente es el conjunto de los resultados.

## Usalo con el marco de ejecución

LangGraph envía Plan-and-Execute como receta (`create_react_agent`Para ReAct, gráficos personalizados para ejecutar el plan). Los flujos de CrewAI codifican el patrón directamente: se definen las tareas de antemano y el Flow DAG las ejecuta.

> LangGraph va a planificar y ejecutar  como complemento proporcionar`create_react_agent`Usado para ReAct, autodefinido para planificar-execución)  Los flujos de CrewAI  directamente codificados en este modelo:

## Envíe el producto .

`outputs/skill-rewoo-planner.md`genera un plan DAG de ReWOO a partir de una solicitud del usuario, dado un catálogo de herramientas. Valida el plan (acíclico, cada referencia resuelta, cada herramienta existe) antes de entregarlo a un ejecutor.

> `outputs/skill-rewoo-planner.md`根据用户请求和工具目录生成 ReWOO 计划 DAG──它在转交给执行器之前验证计划(无环、每个引用已解析、每个工具存在)──

## Los ejercicios.

1. Paralelamente ejecución de trabajadores para nodos de plan independientes. ¿Qué te compra en un DAG de 6 nodos con 2 grupos paralelos?
   China: ¿Qué beneficios tiene la combinación de 6 y 2 grupos de trabajo en el día de trabajo?
2. Añadir un nodo de replanificación que se dispara si algún trabajador devuelve un error. ¿Cuál es el menor cambio en ReWOO que lo hace Plan-and-Ejecute?
   China Translation: Añadir un punto de reorganización en el trabajo de regreso error en el tiempo de reorganización. ¿Cuál es el cambio mínimo en el plan y ejecución?
3. Reemplazar`Planner`con un modelo pequeño (clase 7B) y mantener `Solver`¿Cuál es el resultado de la división?
   En el caso de los modelos de la línea de trabajo, ¿qué tipo de modelo es el modelo de la línea de trabajo?
4. Leer la sección 4 del documento de ReWOO sobre la destilación de planificadores.
   En inglés, el proyecto de programación de la organización de proyectos de planificación de proyectos de planificación de proyectos de planificación de proyectos de proyectos de planificación de proyectos de proyectos de planificación de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos de proyectos
5. Portar el juguete a la forma de trayectoria de Plan-y-Act: plan es una secuencia, no un DAG. ¿Qué compensaciones cambian?
   La forma de trayectoria de Plan-y-Act: plan es de secuencia y no DAG. ¿Qué cambios ocurrieron?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| ReWOO | "Reasoning without observations" / "无观察推理" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt / 先规划，再并行获取证据，最后求解——规划提示中不包含观察 |
| Plan-and-Execute | "LangChain's plan-execute pattern" / "LangChain 的计划-执行模式" | ReWOO with an optional replanner node after execution / 带可选重新规划节点的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" / "扩展版计划-执行" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks / 使用合成计划训练数据的长程任务显式规划器/执行器分离 |
| Evidence reference | "#E1, #E2, ..." / "证据引用" | Plan-node placeholder substituted with prior worker output at dispatch time / 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" / "小规划器，大执行器" | Fine-tune a small model on planner traces from a large teacher / 用大模型的规划轨迹微调小模型 |
| Token efficiency | "Fewer round trips" / "更少往返" | 5x fewer tokens on HotpotQA vs ReAct in the paper / 论文中 HotpotQA 上比 ReAct 减少 5 倍 token |
| DAG executor | "Topological dispatcher" / "拓扑分派器" | Runs plan nodes in dependency order; parallel at each level / 按依赖顺序运行计划节点；每层可并行 |

## Más Leer más Leer más

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) el papel canónico
  En el libro de la revista ReWOO, el libro de la literatura clásica se publica en el periódico ReWOO.
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) planificador ejecutor a escala con planes sintéticos
  Plan y Acto  utilizando la versión ampliada de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión.
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) la receta marco
  El plan de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) Elige el patrón más simple que funcione
  En inglés, la mayoría de las personas que usan el método de selección de un agente eficaz pueden usar el método más simple.
