# Investigación de Alineación Automática (AAR)

> Anthropic dirigió equipos paralelos de Claude Opus 4.6 Autonomous Alignment Researchers en cajas de arena independientes, coordinándose a través de un foro compartido cuyos registros viven fuera de cualquier caja de arena (así que los agentes no pueden eliminar sus propios registros). En el problema de la formación de débil a fuerte, los AAR superaron a los investigadores humanos. Las propias señales de resumen de Anthropic que prescriben flujos de trabajo a menudo limitan la flexibilidad de AAR y degradan el rendimiento. La investigación de alineación automatizada es el paso de compresión que comprime la línea de tiempo a los riesgos exactos de desalinamiento que el RSP debe detectar.

> **【中文解读】**En el caso de los investigadores humanos, los resultados de los estudios de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de los científicos de los científicos de la ciencia de los científicos de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de la

> **【拓展：自主研究 Agent 的双重性】**La existencia de AAR tiene "compresión" y "uso doble": la forma en que se puede acelerar el estudio de la misma manera; la forma en que se puede automatizar el "destrucción de la misma manera".

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, parallel-research-forum simulator) | **语言:** Python（标准库，并行研究论坛模拟器）
**Prerequisites:** Phase 15 · 05 (AI Scientist v2), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 05（AI Scientist v2），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·05(AI Scientist v2 开放研究) Fase 15·04(DGM 自我修改) Fase 18·11(Scalable Supervisión 弱到强监督) AAR = AI Scientist utiliza para "AI seguridad investigación en sí misma"既是工具也是风险──
> ¿ Qué es esto ?**【类比】**AAR = "AI 给自己写体检报告"―AI Scientist v2 = AI hacerse una investigación científica;AAR = AI investigar cómo hacerse un hombre más seguro―Problema: ¿Doctor puede darse un hombre más seguro?
> ¿ Qué es esto ?**【困惑】**P: 既然 AI 能做对齐研究,为什么还需要人类?  AI 能加速但无法保证完整性──弱到强监督的根本困境 (Fase 18·11):弱监督者 (弱监督者) 人类或弱 AI)                                                                                                                                                                                                                               

## El problema es la introducción del problema

> **【中文解读】**La automatización de la investigación de la inteligencia artificial explora si los sistemas de inteligencia artificial pueden descubrir y reparar de forma autónoma sus propios problemas de seguridad. El problema central es: ¿La inteligencia artificial puede ser una ayudante de la investigación de seguridad propia? La experiencia de la investigación antropológica y Redwood muestra que la LM puede generar información de seguridad útil para los investigadores de la inteligencia artificial, pero no tiene la capacidad de realizar estudios de seguridad de forma independiente hasta el final.

> **【拓展：automated alignment research】**La investigación de la automatización para la seguridad de la IA es un punto de inflamación en el ámbito de la seguridad de la IA de 2025-2026. El artículo de Anthropic explora la viabilidad de la IA con la IA  Asistencia a la supervisión de una IA más fuerte. El reto clave es ¿Puede la supervisión de un modelo más débil captar todos los comportamientos peligrosos del modelo más fuerte?

La investigación de alineación es costosa en el tiempo del investigador humano.

> El tiempo de investigación en humanos es muy caro.

Los problemas como la supervisión escalable, la especificación de la recompensa o la capacitación de débil a fuerte requieren experimentos que tardan semanas por iteración.

> La capacidad de supervisión puede extenderse, las normas de recompensa o el entrenamiento de fuerza debilitante requieren experimentos de varias semanas.

La investigación de alineación automatizada (AAR) pregunta si los mismos modelos fronterizos cuya capacidad es superior a la alineación pueden contribuir a cerrar la brecha. El informe 2026 de Anthropic sobre un estudio de entrenamiento de débil a fuerte dirigido por AAR (alignment.anthropic.com/2026/automated-w2s-researcher/) es uno de los primeros resultados públicos de un sistema desplegado de esta clase.

> La investigación automática de la capacidad de interrogar (AAR) está corriendo y ganando en la misma línea de frente del modelo de capacidad de contribución a la cerramiento de la brecha.


> **【中文解读】**Este capítulo presenta la seguridad de la IA en la tecnología para garantizar que el comportamiento de los sistemas de IA se ajuste a las intenciones y valores humanos.

El resultado es realmente positivo: los ARS resolvieron un problema de investigación mejor que la línea de base humana.

> El resultado es realmente positivo: AAR es superior a la base humana en el problema de investigación. Pero este resultado también centrará todas las preocupaciones de esta etapa en un sistema.

Si la investigación de alineación puede ser automatizada, también pueden ser las partes que comprometen las salvaguardias.

> Si la investigación completa se puede automatizar, entonces también se puede automatizar parte de las medidas de salvaguardia.

## El concepto central.

### La arquitectura (como se describe públicamente)

- **Parallel agents.**Múltiples instancias de Claude Opus 4.6 se ejecutan como AAR, cada una en una caja de arena independiente.
  En inglés:**并行 Agent。**Muchos de los Opus 4.6  ejemplos como AAR 运行, cada uno en un archivo independiente 沙箱中.
- **Shared forum.**Los resultados se publican en un foro compartido cuyo almacenamiento de fondo se encuentra fuera de cada caja de arena. Los agentes pueden leer el foro; los agentes no pueden eliminar o editar los registros del foro desde dentro de su propia caja de arena.
  En inglés:**共享论坛。**Encontrado publicado en el foro de compartir, su archivo posterior se encuentra fuera de cada caja de arena.
- **Task allocation.**Una cola de tareas diseñada por el hombre asigna problemas de investigación a los AAR.
  En inglés:**任务分配。**La línea de tareas de la creación de obras de arte distribuirá los problemas de investigación a AAR.
- **Weak-to-strong training focus.**El estudio publicado abordó la formación de débil a fuerte  utilizando un modelo de supervisor más débil para capacitar a un modelo de estudiante más fuerte.
  En inglés:**弱到强训练聚焦。** Los estudios publicados se dirigen a la formación de los estudiantes de la supervisión de la formación de los modelos más débiles a los de la formación de los estudiantes de la supervisión de la supervisión de los modelos más fuertes.

### ¿Por qué importa el registro fuera de la caja de arena ?

La propiedad de integridad de registro es la diferencia entre un experimento controlado y uno potencialmente comprometido.

> La propiedad de la integridad del día es la diferencia entre la experiencia controlada y la experiencia potencialmente dañada.

Si los AAR pudieran editar sus propios registros, podrían encubrir experimentos fallidos o dudosos.

> Si las AAR pueden editar sus propios diarios, pueden ocultar el fracaso o los experimentos dudosos.

El analógico en términos de infraestructura son los registros de apéndice solo con escritura a través de almacenamiento externo (por ejemplo, bloqueo de objetos S3, registros Datadog inmutables). El agente no tiene credenciales para modificar registros pasados. Este es el mismo patrón que los equipos de seguridad corporativos 2026 utilizan para hacer rastros de auditoría resistentes a ransomware.

> 类比在基础设施术语中是写入外部存储的仅仅添加日志 (por ejemplo, S3对象锁,不可变数据库 日志)  Agente 无证证修改过去记录―― es el mismo modelo que el equipo de seguridad empresarial de 2026 utiliza para producir un seguimiento de auditoría de software antirroqueo―

### El flujo de trabajo prescrito de compensación .

El informe de Anthropic señala que los flujos de trabajo prescritos a menudo limitan la flexibilidad de AAR y degradan el rendimiento.

> El informe de Anthropic señala que los flujos de trabajo regulares suelen limitar la flexibilidad de AAR y disminuir su rendimiento.

En otras palabras: si el diseñador humano escribe el plan de investigación paso a paso, los AARs hacen peor que si se les dan objetivos de alto nivel y libertad para descomponerse. Esto es consistente con los resultados en toda la investigación agencial (LangGraph, el Marco de Agentes de Microsoft)  los andamios demasiado especificados perjudican a los agentes capaces.

> En otras palabras: si un diseñador humano redacta un plan de investigación gradualmente, AAR no se presenta como un objetivo de alto nivel y la libertad de descomposición. Esto coincide con los resultados del estudio de Agente.

La flexibilidad que mejora el rendimiento de AAR es también la flexibilidad que permite la descomposición sin sanción, el uso de herramientas nuevas y la derivación de objetivos. La compensación es una decisión del espacio de diseño: ¿cuánta flexibilidad compra suficiente capacidad para vencer a los humanos, sin entregar el espacio de agente para generalizar objetivos fuera de la distribución?

> Seguridad significación pequeña. La flexibilidad de la AAR también permite la descomposición no autorizada. El uso de nuevos instrumentos y la flexibilidad de la derivación de objetivos.

### El riesgo de compresión.

RSP v3.0 (Lección 19) introduce un umbral de capacidad de I+D de IA: la capacidad de automatizar completamente la tubería de I+D de IA a un costo competitivo frente a herramientas de IA + humanos. FSF v3 de DeepMind incluye un nivel de autonomía de I+D de ML análogo. Ambos marcos tratan este umbral como el desencadenante para controles elevados.

> RSP v3.0 (第 19 课) Introducción de la capacidad de I+D de la IA  Valor: la capacidad de la capacidad de la tubería de I+D de la IA totalmente automatizada bajo el costo de la competencia con humanos + herramientas de IA  Valor: la capacidad de la capacidad de la R&D de la IA bajo el costo de la competencia con humanos + herramientas de IA  ∞.

AAR está un paso por debajo del umbral: automatiza parte de la línea de trabajo (investigación de alineación sobre tareas específicas y bien ampliadas), pero no el ciclo de desarrollo de capacidades de extremo a extremo.

> AAR 离值一步之遥: es parte de la tubería de automatización de la investigación de la capacidad de desarrollo de la tarea específica (en lugar de un ciclo de desarrollo de la capacidad de la tarea).

Los plazos comprimidos son la preocupación por la falla de la composición. Si la investigación de alineación y la investigación de capacidad se componen a tasas similares, la superficie de riesgo de desalinamiento crece al menos tan rápido como la capacidad. Si la capacidad se compone más rápido (la tendencia histórica), la brecha se amplía. Este es el argumento de que el AAR es un bien calificado: cada resultado adicional de alineación reduce la brecha si y sólo si el proceso de investigación es confiable.

>                                                                                                                                                                                                                                                               

### Lo que el AAR no reemplaza lo que el AAR no reemplaza nada

Los investigadores humanos establecen la cola de tareas, revisan los resultados y tienen la autoridad constitucional.

> Los investigadores humanos establecen una línea de tareas, revisan los resultados y tienen el poder constitucional.

Los AAR aceleran la mitad de la línea de producción, no los extremos. Los resultados publicados de Anthropic incluyen tanto las contribuciones AAR como el juicio humano-investigador sobre qué publicar, qué retractar y qué refinar.

> AAR se acelera en la parte media del tubo, y no en los dos extremos.

Esto coincide con el patrón de proponer y luego comprometerse de la Lección 15 aplicada a la investigación misma: AARs proponen; humanos se comprometen.

> Este modelo de propuesta-entonces-compromiso se aplica al estudio mismo.

## Usalo con el marco de ejecución
```figure
aar-forum
```

## Usalo

`code/main.py`La aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la ley de la ley de la ley de la ley de la ley de 30 de 30 de 30 de junio de junio de julio de julio de de de julio de de de de de de de de de de de de de de de julio de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de

> `code/main.py`模拟多 AAR 研究论坛──三个独立"研究代理"并行运行, se encontrará publicado hasta la fecha con sólo un nuevo foro de cambios posibles.

- ¿Qué quieres ?

>  observar:

- Cómo la extracción de madera fuera de la caja de arena captura los intentos de manipulación de madera.
  China: 沙箱外日志 cómo capturar 日志 改尝试
- Cómo la asignación de tareas con descomposición libre supera los flujos de trabajo fijos en problemas más difíciles.
  Traducción:BandemFreedomDecomposition: ¿Cómo asignar las tareas en problemas más difíciles que en los que se trabajan en el flujo fijo?
- Cómo una sola AAR comprometida puede contaminar la señal del foro si el registro no es evidente.
  En el contexto de la política de la Unión Europea, el gobierno de la República de China ha adoptado una política de paz en el país.

## Envíe el producto .

`outputs/skill-aar-deployment-review.md`es una revisión previa a la implementación de una línea de investigación de alineación automatizada.

> `outputs/skill-aar-deployment-review.md`Es la automatización de la implementación de la investigación de la tubería de la información.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Comparar la configuración de "flujo de trabajo fijo" con la de "descomposición libre". ¿Gana siempre la descomposición libre, o existen clases de problemas en las que el flujo de trabajo fijo es competitivo?
   Traducción:运行`code/main.py`¿Comparar la configuración de "flujo de trabajo fijo" con la de "liberación de trabajo"? ¿La liberación de trabajo siempre es exitosa, o hay problemas de flujo de trabajo fijo competitivo?

2. Modifique el simulador para que un agente intente manipular el registro. Confirme que el registro de apéndice lo detecta. Escriba un párrafo que describa exactamente cómo se ve la firma de detección en el registro.
   China: Modificar el modelo de un agente 尝试日志改──确认仅增加日志检测到──写一段准确描述日志中检测签名的外观──

3. Lea el informe de AAR de Anthropic de débil a fuerte. Identifique la subtarefa específica en la que los AAR superaron a los investigadores humanos. ¿Qué lo hizo susceptible a la automatización?
   En inglés, el estudio de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia de ciencia

4. Diseñar una política de asignación de tareas en la cola que equilibre la flexibilidad de AAR (mejores resultados) con las restricciones del flujo de trabajo prescritas (auditoria más fácil). Describir cómo se analizaría A/B los dos.
   En inglés, el método de distribución de la línea de tareas de AAR 灵活性 (AAR) se utiliza para describir cómo A/B 测试两者──.

5. Lea el umbral de I+D-4 de la IA de RSP v3.0. En un párrafo, describa lo que cree que cruzaría que AAR actualmente no.
   China Translation: Read RSP v3.0 de AI R&D-4 valor。 Usando un fragmento de descripción de lo que crees que va a atravesarlo mientras AAR actualmente no se cruza。

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AAR | "Automated Alignment Researcher" | Claude Opus 4.6 instance operated autonomously on alignment problems |
| AAR | "自动化对齐研究器" | 在对齐问题上自主操作的 Claude Opus 4.6 实例 |
| Weak-to-strong training | "Training a stronger model with a weaker supervisor" | Classic scalable-oversight benchmark AARs outperformed humans on |
| 弱到强训练 | "用较弱监督者训练较强模型" | AAR 击败人类的经典可扩展监督基准 |
| Shared forum | "Where agents publish findings" | Append-only, out-of-sandbox storage |
| 共享论坛 | "Agent 发布发现之处" | 仅追加、沙箱外存储 |
| Out-of-sandbox log | "Agent cannot edit its own record" | Tamper-evident write-through to external storage |
| 沙箱外日志 | "Agent 不能编辑自己的记录" | 写入外部存储的防篡改透写 |
| Prescribed workflow | "Step-by-step plan from human designer" | Constrains AAR; often degrades performance vs free decomposition |
| 规定工作流 | "人类设计者的逐步计划" | 约束 AAR；通常比自由分解降低性能 |
| Free decomposition | "Agent decides how to break the task" | More capable, harder to audit |
| 自由分解 | "Agent 决定如何拆分任务" | 更有能力，更难审计 |
| AI R&D threshold | "RSP/FSF capability level" | Full automation of R&D pipeline at competitive cost |
| AI R&D 阈值 | "RSP/FSF 能力级别" | 在竞争成本下完全自动化 R&D 管道 |
| Compressed timeline | "Alignment vs capability race" | If capability compounds faster than alignment, misalignment risk grows |
| 压缩时间线 | "对齐与能力竞赛" | 若能力比对齐复利更快，不对齐风险增长 |

## Más Leer más Leer más

- [Anthropic — Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) fuente primaria.
  La traducción de la lengua inglesa es:
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Enmarcamiento del umbral de I+D de la IA.
  La tecnología artificial es un sistema de investigación y desarrollo de la IA.
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) un marco más amplio de la autonomía de los agentes.
  En español, más amplios:
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) ML niveles de autonomía en I+D paralelos a los de RSP.
  Traducción:RSP, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R&D, R
- [Burns et al. (2023). Weak-to-Strong Generalization (OpenAI)](https://openai.com/index/weak-to-strong-generalization/) el problema subyacente atacado por los AAR.
  La respuesta es: "No hay nada que me haga sentir mal".
