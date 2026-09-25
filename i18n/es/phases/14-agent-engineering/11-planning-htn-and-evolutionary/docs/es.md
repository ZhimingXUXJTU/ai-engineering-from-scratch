# Planificación con HTN y búsqueda evolutiva .

> La planificación simbólica se ocupa de los casos en los que el plan es probada correcta. La búsqueda de código evolutivo se ocupa de los casos en los que la función de aptitud es verificable por máquina. ChatHTN (2025) y AlphaEvolve (2025) muestran lo que cada uno desbloquea cuando se empareja con un LLM.

> **【中文解读】**符号规划处理计划可证明正确的场景――进化代码搜索处理适应度函数可机器检查的场景――ChatHTN(2025) y AlphaEvolve(2025) han demostrado su capacidad de desbloqueo en el tiempo de la LLM 配合――

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 02 (ReWOO and Plan-and-Execute) | **前置知识:** Phase 14 · 02 (ReWOO 与计划-执行)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Explicar las redes jerárquicas de tareas: tareas, métodos, operadores, condiciones previas, efectos.
  En inglés, el nombre de la red de tareas es "Misión".
- Describa la búsqueda simbólica de circuito híbrido de ChatHTN con la descomposición de fallback de LLM.
  En inglés, el código de acceso de la red de acceso de chatHTN se puede utilizar para el uso de la red de acceso de chatHTN.
- Explica el ciclo evolutivo de AlphaEvolve y por qué solo funciona con un evaluador programático.
  Traducción:Explicar el ciclo evolutivo de AlphaEvolve y por qué solo es efectivo en el evaluador procedimental.
- Implemente un planificador de juguete HTN más una búsqueda evolutiva de juguete en Stdlib.
  Traducción:Use estándar de la biblioteca para implementar el juego de la lengua china.

## El problema es la introducción del problema

ReWOO (lección 02), Plan-and-Ejecute y ReAct cubren la mayoría de la planificación de agentes.

> ReWOO(第 2 课) 、Plan-and-Execute 和 ReAct 覆盖了大多数代理规划──两种它们不能很好覆盖情况:

1. **Plans with provable correctness.**El programa, la ruta de vuelo, los flujos de trabajo de cumplimiento  el plan debe ser sólido por construcción.
   En inglés:**可证明正确性的计划。**调度,航线规划,合规工作流计划必须在构建上是可靠的―― un fluido LLM 计划 de un paso ocasional de la ilusión es inaceptable――
2. **Optimizations with a machine-checkable fitness function.**La multiplicación de matrices, la planificación de heurísticas, los pasos del compilador  el objetivo no es "un plan correcto" sino "el mejor plan".
   En inglés:**有机器可检查适应度函数的优化。**矩阵乘法、调度启发式、编译器 pass 目标不是"un plan correcto" sino"el mejor plan"―

> **【中文解读】**El programa de planificación de agentes tiene dos tipos principales: red de tareas de nivel separado (HTN) y desarrollo de proyectos. El programa de planificación de proyectos de desarrollo de proyectos de proyectos de desarrollo (HTN) se divide en subtareas ejecutables, adaptadas al ámbito estructurado.

El plan de HTN y AlphaEvolve resuelven los dos problemas diferentes. Ambos usan LLM como amplificadores, no como reemplazos.

> HTN 规划和 AlphaEvolve 解决两个 diferentes problemas── ambas serán LLM con un amplificador y no un sustituto──

> **【拓展：2026 年 Agent 规划的前沿】**AlphaEvolve y Darwin-Godel Machine aplicarán algoritmos de desarrollo a la optimización de estrategias del propio agente no sólo en la planificación de tareas, sino en la planificación y optimización del proceso de planificación en sí mismo.

> ¿ Qué es esto ?**【前置】**必须先过阶段14·02 (ReWOO/Plan-and-Execute) HTN es su versión "rigorosamente formalizada"; así como el conocimiento básico clásico de la IA 规划知识 (status、前置条件、效果) ── Si no has escuchado los STRIPS o el PDDL, sugiere que primero añada dos episodios de "Clásico símbolo de la IA" instrucciones 本节的"可证明正确性" dependen de este conjunto de lenguajes formalizados────

## El concepto central.

### Las redes jerárquicas de tareas

Una HTN es:

> HTN es:

- **Tasks** Compuesto (para descomponerse) y primitivo (executable directamente).
  En inglés:**任务**复合(待分解)和原始(直接可执行)
- **Methods** formas de descomponer una tarea compuesta en subtareas, con condiciones previas.
  En inglés:**方法**将复合任务分解为子任务的方式,带前置条件──
- **Operators** acciones primitivas con condiciones previas y efectos.
  En inglés:**操作符**带前置条件和效果的原始动作──
- **State** un conjunto de hechos.
  En inglés:**状态**一组事实──

Planificación: dada una tarea objetivo y un estado inicial, encontrar una descomposición en operadores primitivos cuyas condiciones previas se cumplen en secuencia.

> 规划: dado el objetivo de la tarea y el estado inicial, encontrar un esquema de descomposición en el operador original, su prepuesta de condiciones en orden satisfago.

El HTN es más antiguo que los LLM y sigue siendo la referencia para los planes probadamente correctos.

> El HTN es más antiguo que el LLM, y sigue siendo un referente de un plan correcto.

### El objetivo de la investigación es mejorar la calidad de la información y la calidad de la información.

ChatHTN (arXiv:2505.11814) interlea HTN simbólico con las consultas de LLM:

> ChatHTN(arXiv:2505.11814)交替进行符号 HTN 和 LLM 查询:

1. Trate de descomponer la tarea compuesta actual con métodos existentes.
   En inglés, "true" significa "true" o "construcción".
2. Si no se aplica ningún método, pregúntale al LLM: "cómo se descomponería `task`en el estado `s`¿Qué es eso?
   Si no hay un método adecuado, pregunta LLM:" en estado `s`¿Cómo se descompone?`task`¿Qué es eso?
3. Traducir la respuesta del LLM en subtareas candidatas.
   La ley de derecho de la mujer es una ley de derecho de la mujer.
4. Validación con respecto al esquema del operador; rechaza descomposiciones inválidas.
   En inglés, el método de prueba de control de un operador es el método de prueba de control de control de un operador.
5. Recurso.
   En el idioma chino, el idioma se traduce en chino.

El documento afirma que cada plan producido es probada como válido porque las sugerencias de LLM sólo entran como descomposiciones candidatas, nunca como ediciones directas de planes.

> ¿ Qué es esto ?**【类比】**ChatHTN 像严格的审计员 (严格的审计员) 符号层) + 创意实习生 (创意实习生) LLM (实习生提建议:"Me parece que este objetivo se puede desglosar así..."**结果**Todos los planes de adopción final han sido revisados, la fiabilidad está garantizada.

> 论文的核心主张: Cada plan que surja puede demostrarse ser fiable, ya que el LLM 建议只作为候选分化进入,从不作为直接计划编辑;;

Aprendizaje en línea de métodos (OpenReview `gwYEDY9j2x`, 2025 seguimiento) añade un alumno que generaliza las descomposiciones producidas por el LLM por regresión  recortando la frecuencia de consultas del LLM hasta el 75%.

> En línea métodos de aprendizaje (WEB se ha añadido a través de la regeneración de LLM  producir aprendizaje desglosado  LLM  frecuencia de consulta reducido hasta un 75% 

### AlphaEvolve (Novikov y otros, 2025)

AlphaEvolve (arXiv:2506.13131, DeepMind, junio 2025) es una bestia diferente: búsqueda de código evolutivo orquestada por un conjunto Gemini 2.0 Flash / Pro.

> AlphaEvolve ((arXiv:2506.13131, DeepMind,2025 年 6 月) es una existencia diferente: por Gemini 2.0 Flash/Pro 集群编排的进化代码搜索──

- ¿Qué es eso ?

>  ciclo:

1. Comience con un programa de semillas + un evaluador programático (retorna una puntuación de aptitud).
   Traducción: de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de los idiomas de la lengua de los idiomas de los idiomas de la lengua de los idiomas de los idiomas de la lengua de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de
2. El conjunto de LLM propone mutaciones.
   La ley de los derechos humanos se ha modificado en el contexto de la ley de derechos humanos.
3. Ejecutar las mutaciones a través del evaluador.
   Por ejemplo, el nombre de la empresa de evaluación de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad.
4. Mantenga lo mejor, mutar de nuevo.
   El mejor de los otros es el mejor de los otros.

Las ganancias publicadas:

>  resultados publicados:

- Primera mejora respecto a Strassen para la multiplicación de matrices complejas 4x4 en 56 años (48 multiplicaciones escalares).
  En el pasado, el sistema de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad
- El 0,7% recuperó la computación de Google a través de una heurística de programación Borg.
  China 計算資源: 调度启发式回收 0.7% de los recursos de Google 計算資源: 调度启发式回收
- El 32% de la atención flash se acelera en una carga de trabajo fronteriza.
  En la actualidad, el número de personas que se encuentran en la ciudad de Nueva York es de aproximadamente un 32%.

La difícil restricción: la función de aptitud debe ser controlada por máquina.

> ️ **【易错点】**Colocar AlphaEvolve en su conjunto de "creativo-escritura-optimización" para que el LLM utilice algoritmos de mejora de la escritura, con el LLM 评分作为健身.**后果**La función de aptitud en sí misma es LLM (随机+不稳定), la misma historia dice que el resultado puede ser de un 30% menos.**一行修复**En el caso de las tareas de programación de "Objective indicator" con AlphaEvolve, el rendimiento de código, la tasa de cobertura de pruebas y la eficiencia de la regulación, las tareas de creación se vuelven auto-refinadas/críticas.

> 硬约束: la función de la adaptación debe ser de máquina verificable.

### Cuándo utilizar cuál

| Problem class | Use | Why |
|---------------|-----|-----|
| 问题类别 | 使用 | 原因 |
| Scheduling with hard constraints | HTN + ChatHTN | Provable soundness / 可证明的可靠性 |
| Compiler optimization | AlphaEvolve | Machine-checkable fitness / 机器可检查的适应度 |
| Multi-step task execution | ReAct / ReWOO | LLM in the loop, no formal guarantees / LLM 在循环中，无形式化保证 |
| Code improvement with tests | AlphaEvolve | Tests are the evaluator / 测试即评估器 |
| Policy-bound automation | HTN | Preconditions encode policy / 前置条件编码策略 |

### Cuando este patrón va mal

- **HTN without operators.**Sin esquemas de precondisión/efecto, la afirmación de solidez se desmorona.
  En inglés:**没有操作符的 HTN。**无前置条件/效果模式,可靠性声明就崩了──ChatHTN's "LLM 建议分解" necesita un modelo para rechazar la inefficiencia.
- **AlphaEvolve without a real evaluator.**"Pregúntele al LLM si el código es mejor" no es una función de aptitud.
  En inglés:**没有真正评估器的 AlphaEvolve。**"Preguntar si el código de LLM es mejor" no es una función de adaptación.
- **Over-engineering.**La mayoría de las tareas de los agentes no necesitan ni una ni otra.
  En inglés:**过度工程。**La mayoría de los agentes no necesitan ningún otro.

> ¿ Qué es esto ?**【困惑】**P: ChatHTN 论文说"LLM 只有提建议不直接进计划"这跟LangChain Agent 调用工具不是一回事吗? A: 不一样.

## Construye con movimiento.
```figure
htn-tree-expand
```

## Construye el mismo

`code/main.py`Implementa dos juguetes:

> `code/main.py` Realizó dos juguetes:

- Un planificador de HTN de la serie con operadores, métodos, condiciones previas, efectos y una`LLMFallback`El LLM es un descomposición scripted para que el planificador se ejecute fuera de línea.
  Un programa de programación de tareas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de una serie de programas de desarrollo de proyectos de desarrollo de una serie de programas de desarrollo de proyectos de desarrollo de una serie de programas de desarrollo de proyectos de desarrollo de una serie de programas de desarrollo de proyectos de desarrollo de una serie de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de desarrollo de proyectos de desarrollo de proyectos de proyectos de desarrollo de proyectos de desarrollo de desarrollo de proyectos de desarrollo de desarrollo de desarrollo de proyectos de desarrollo de desarrollo de desarrollo de desarrollo de proyectos de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de proyectos de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo de desarrollo`LLMFallback`"LLM" es un desglosador de guiones, planificador de operaciones en línea
- Una búsqueda evolutiva de programas aritméticos: crecer expresiones cuya producción se minimiza `|f(x) - target|`El evaluador es determinista.
  Un estudio de la historia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia.`|f(x) - target|`En el ensayo de ensayos, la expresión mínima es la determinación.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra al planificador HTN descomponer una tarea compuesta (con una caída de LLM en el plano medio) y el bucle evolutivo convergiendo en una expresión objetivo.

> 轨迹显示 HTN 规划器分解复合任务(带中途 LLM 回退) y el ciclo de evolución recibiendo hasta la realización de los objetivos──

## Usalo con el marco de ejecución

- **HTN planners**¿ Qué es esto ?`pyhop`¿ Qué ?`SHOP3`, o construir su propio para la aplicación de políticas específicas de dominio.
  En inglés:**HTN 规划器** El`pyhop`¿Qué es esto?`SHOP3`, o para ejecutar estrategias específicas en el ámbito de su construcción.
- **ChatHTN** código de investigación; el patrón (símbolo + LLM fallback) se porta limpio a cualquier planificador de HTN.
  En inglés:**ChatHTN**研究代码;模式(符号 + LLM 回退)可干净地移植到任何HTN 规划器──
- **AlphaEvolve** Papel de DeepMind; el patrón (ensemble + evaluator) es reproducible. OpenEvolve y forks de código abierto similares están surgiendo.
  En inglés:**AlphaEvolve**DeepMind 论文;模式(集群 + 评估器)可复现──OpenEvolve 和类似开源分支正在涌现──
- **Agent frameworks** no se envíe todavía HTN de primera clase o AlphaEvolve.
  En inglés:**Agent 框架** Actualmente no hay una HTN o AlphaEvolve integrada.

## Envíe el producto .

`outputs/skill-hybrid-planner.md`genera un andamio de planificadores híbridos (HTN o evolutivo) con el rol de MLL explícitamente definido.

> `outputs/skill-hybrid-planner.md`El programa de trabajo de la Universidad de San Francisco (UFSA) se desarrolla en el ámbito de la educación y la educación.

## Los ejercicios.

1. Extensión del planificador de HTN con retroceso: cuando el postcondimiento del operador falla en el tiempo de ejecución, vuelva hacia atrás y pruebe el siguiente método.
   Cuando el operador se encuentra en condiciones de retrocesión en el tiempo de ejecución, regresar y intentar el siguiente método.
2. Añadir un caché del método LLM a ChatHTN: cuando el LLM descompone la tarea `T`en el patrón del estado `P`Reverifique la biblioteca de métodos primero en la próxima llamada.
   中文翻译:为 ChatHTN 添加 LLM 方法缓存:当 LLM 在状态模式 `P`Encuentro de las tareas`T`时,存储结果──下次调用时先重新检查方法库──
3. Cambiar el evaluador de búsqueda evolutiva a una suite de pruebas real. Desarrollar una función de clasificación que pasa 20 casos de prueba; reportar generaciones a convergencia.
   China:将进化搜索评估器替换为真实测试套件──进化一个通过 20 测试用例的排序函数;报告收代数──
4. Lea las notas de diseño de evaluadores de AlphaEvolve. Diseñe un evaluador para un dominio que le importe (optimización de consultas SQL, minimizado de la suite de pruebas, implementación YAML).
   En el contexto de la investigación, el equipo de evaluación de AlphaEvolve ha sido diseñado para el desarrollo de un sistema de evaluación de SQL.
5. Combina: utiliza HTN para descomponer una tarea compuesta en subtareas, luego utiliza búsqueda evolutiva en el operador primitivo de cada subtarea. ¿Dónde brilla, dónde se sobreingeniera?
   En inglés, el método de búsqueda de datos es el método de búsqueda de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| HTN | "Hierarchical planner" / "分层规划器" | Task decomposition with operators, preconditions, effects / 带操作符、前置条件、效果的任务分解 |
| Method | "Decomposition rule" / "分解规则" | Way to break a compound task into subtasks / 将复合任务分解为子任务的方式 |
| Operator | "Primitive action" / "原始动作" | Concrete step with precondition and effect / 带前置条件和效果的具体步骤 |
| ChatHTN | "LLM + HTN" / "LLM + HTN" | Symbolic planner asks LLM when no method matches / 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | "Evolutionary code search" / "进化代码搜索" | Ensemble LLMs mutate code; deterministic evaluator selects / LLM 集群变异代码；确定性评估器选择 |
| Fitness function | "Evaluator" / "评估器" | Deterministic, machine-checkable score over outputs / 输出上的确定性、机器可检查分数 |
| Online method learning | "Cached LLM decomposition" / "缓存的 LLM 分解" | Store + generalize LLM plans to cut query cost / 存储并泛化 LLM 计划以降低查询成本 |

## Más Leer más Leer más

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814) Planificador híbrido de LLM
  En inglés, el programa de programación de programas de programación de programas de programación de programas de programación de programas de programación de programas de programación de programas de programación de programas de programación de programas de programación de programación de programas de programación de programación de programas de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programa
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) búsqueda de código evolutivo con mutaciones de LLM
  El programa de investigación de la Universidad de California en San Diego, California, fue publicado en el periódico de la Universidad de San Diego en San Diego, California.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) cuándo alcanzar un planificador vs un simple bucle
  La guía antropológica sobre la construcción de un agente eficaz 何时使用规划器而非简单循环──
