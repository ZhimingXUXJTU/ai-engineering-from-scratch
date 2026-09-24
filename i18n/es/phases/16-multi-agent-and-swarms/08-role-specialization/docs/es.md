# Role Specialization  Planificador, crítico, ejecutor, verificador   especialización  crítico  programa 角色

> La descomposición multi-agente más común en 2026: un agente planea, ejecuta, critica o verifica. MetaGPT (arXiv:2308.00352) formaliza esto como SOP codificados en instrucciones de rol  Gerente de producto, arquitecto, gerente de proyecto, ingeniero, ingeniero de calificación  siguiente `Code = SOP(Team)`¿ Qué ? ChatDev (arXiv:2307.07924) en cadena diseñador, programador, revisor, probador a través de una "cadena de chat" con "deshallucinación comunicativa" (los agentes solicitan explícitamente detalles faltantes). El verificador es resistente a la carga: Cemri et al. (MAST, arXiv:2503.13657) muestran que cada falla multi-agente puede ser rastreada a la verificación faltante o rotura. PwC informó una ganancia de precisión de 7 veces (10% → 70%) a partir de los bucles de validación estructurados en CrewAI.

> **【中文解读】**Este capítulo presenta la especialización de los roles para cada agente, la distribución de un papel y especialidad definidos, la mejora de la eficiencia del equipo en su conjunto.

> **【拓展：role specialization→具体应用】**La especialización de roles es el concepto central de la CrewAI. Cada agente tiene un papel. El papel. Objetivo. y historia de fondo. La práctica muestra que la definición de un papel claro puede mejorar significativamente la eficiencia de la colaboración de varios agentes. Pero la especialización excesiva también tiene el riesgo de que la frontera de los roles sea demasiado estricta.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前Permanecer la fase 16·04-05 (原语+Supervisor) ⋅本节是 2026 最常见的多代理 分解模式:Planner + Critic + Executor + Verifier。
> ¿ Qué es esto ?**【类比】**角色专业化 = "电影制作团队"──Planner = 编剧(定方向)、Executor = 演员(执行)、Critic = 内审、Verifier = 质检员──MetaGPT、ChatDev、CrewAI 都用这种角色分解──Cemri 等人  MAST论文:所有多 Agent 失败都可追溯到"缺少或破损的验证人"验证是承重墙──PwC 案例:加验证人 让准确率从10% 到70% 7倍)──

## # El problema # # El problema #

Los sistemas multi-agentes genéricos producen una salida genérica. Tres codificadores en un chat de grupo escriben tres sabores del mismo código mediocre. Puedes agregar más agentes, agregar más rondas y aún así no cruzar el umbral de calidad.

> Los tres codificadores del grupo de conversaciones escriben tres tipos de códigos de la misma manera. Puedes añadir más agentes, más rutas, pero aún no puedes cruzar el código de calidad.

El problema no es la cantidad, sino la uniformidad. Tres agentes idénticos que reciben la misma tarea producen tres respuestas equivocadas similares. Comparten los mismos puntos ciegos porque comparten el mismo impulso y modelo. Agregar más de lo mismo no ayuda; necesitas agentes que sean diferentes en formas productivas.

>  el problema no es la cantidad sino la misma calidad.  Three the same Agent  given the same task will produce three similar error answers.  Ellos comparten el mismo punto ciego porque comparten la misma sugerencia y el mismo modelo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

La solución no es más agentes  son * diferentes * agentes. asignar funciones distintas. Dar a las herramientas críticas que el planificador no tiene. Dar al verificador una suite de prueba objetiva. Ahora el sistema tiene desacuerdo interno con la corrección basada en tierra, no sólo adivinar paralelo.

> El método de reparación no es más agente sino un agente* diferente. Distribuye diferentes roles.

El cambio clave: de "más agentes haciendo lo mismo" a "agentes diferentes haciendo cosas diferentes". El paralelismo sin especialización es sólo una adivinación costosa.

> 关键转变: de "más agentes hacen lo mismo" a "diferentes agentes hacen cosas diferentes"― no hay coincidencia especializada es sólo una conjetura costosa― la especialización crea un sistema que captura sus errores de incompetencia―

## Concepto de la esencia de la concepción

### Los cuatro papeles canónicos

**Planner.**Leer el objetivo, producir una lista de pasos o una especificación herramientas: recuperación de conocimientos, documentos. salida: plan estructurado.

> **规划者。**读取目标,产生步骤列表或规范──工具:知识检索、文档──输出: estructurada planificación──

**Executor.**Lea un plan paso a paso, produce el artefacto. herramientas: las herramientas de trabajo reales (compilador de código, shell, cliente API). salida: el artefacto.

> **执行者。**Cada vez que se le da un plan, se produce un proyecto.

**Critic.**Leer la salida del ejecutor contra la intención del planificador. herramientas: acceso solo para lectura al artefacto, análisis estático. salida: aceptar/rechazar con razones.

> **批评者。**根据规划者意图阅读执行人输出──工具:对工件的只读访问、静态分析──输出: aceptar/ rechazar及原因──

**Verifier.**Leer el artefacto y ejecutar una verificación determinista. herramientas: test runner, verificador de tipo, validador de esquema. salida: pasar / fallar con evidencia.

> **验证者。**读取工件并运行确定性检查──工具:测试运行器、类型检查器、模式验证器──输出:通过/失败及证据──

El crítico es subjetivo, opinado, a menudo basado en el LLM. El verificador es objetivo, determinista, a menudo basado en código.

> Los críticos son de tipo subjetivo, generalmente basados en el LLM, los verificadores son de tipo objetivo, generalmente basados en código, no son el mismo papel.

El sistema de análisis de los datos de los usuarios de los sistemas de control de código (Code Checks) tiene un resultado correcto pero feo. Necesitas ambos: crítico por gusto, verificador por corrección.

> Los sistemas de los que se componen son los más comunes: los sistemas de los que se componen los controles de código son los más comunes: los que se componen de los controles de código son los más comunes.

### El patrón de SOP de MetaGPT

MetaGPT (arXiv:2308.00352) codifica los SOP de ingeniería de software como instrucciones de rol:

> MetaGPT(arXiv:2308.00352)将软件工程 SOP 编码为角色提示:

El marco de "SOP" se toma prestado de las organizaciones humanas: los procedimientos operativos estándar convierten el trabajo ad hoc en un proceso repetible. MetaGPT aplica esto a los LLM  el SOP se convierte en un sistema de respuesta que limita al LLM a un papel específico con resultados específicos.

> El marco de "SOP" se toma de la organización humana: el proceso de operación estándar se transformará en un proceso recursivo.

- **Product Manager**escribe el PRD.
  En inglés:**产品经理**编写 PRD。
- **Architect**produce el diseño del sistema.
  En inglés:**架构师**产生系统设计──
- **Project Manager**Se dividen las tareas.
  En inglés:**项目经理**¿Qué es eso?
- **Engineer**los instrumentos.
  En inglés:**工程师**实现──
- **QA Engineer**hace pruebas.
  En inglés:**QA 工程师**¿Qué es eso?

Cada rol tiene un estricto esquema de entrada/salida.El mensaje de rol indica cuál es el rol y qué debe producir.`Code = SOP(Team)`La formulación  SOP deterministas convierte a un equipo de LLM en una línea de tuberías predecible.

> Cada papel tiene un modelo de entrada/salida estricto.`Code = SOP(Team)`公式确定性 SOP convertirá un equipo de LLM en una línea de flujo predecible.

El punto clave: codificar el flujo de trabajo del equipo como código, no como conversación. Cada papel de LLM es un nodo en un gráfico determinista; la estructura del gráfico es de autor humano. Los LLM hacen el trabajo local; los humanos son dueños del flujo de trabajo global.

> 关键洞察:将团队工作流编码为代码,而不是对话―― cada LLM 角色是确定性图中的节点;图结构由人类编写――LLM 做局部工作;人类拥有全局工作流――

### La deshallucinación comunicativa de ChatDev

ChatDev agrega un movimiento clave: cuando un ejecutor necesita un detalle específico que no estaba en el plan, le pide explícitamente al diseñador antes de continuar. Esto evita el fracaso clásico de la LLM de inventar plausiblemente el detalle.

> ChatDev añade una iniciativa clave: cuando un ejecutor necesita detalles específicos que no hay en un plan, se pregunta claramente al diseñador antes de continuar. Esto evita el fracaso de los detalles de diseño de LLM clásicos.

El patrón capta alucinaciones en su fuente. En lugar de detectar detalles fabricados después del hecho (duro), evita la fabricación al requerir que el ejecutor pregunte antes de asumir. El costo es un viaje de ida y vuelta adicional; el beneficio es la corrección.

> El modelo en el origen de captura de fantasía. No es un proceso de investigación de detalles de la ficción.

Implementación: el aviso de rol incluye "cuando necesita información específica que no se le dio, pregunte por nombre al papel relevante antes de producir la salida".

> 实现:角色提示包括"When you need you not provided specific information, before generating output, in accordance with the name of the relevant role".""

### Por qué el verificador es más importante

Cemri et al. (MAST) rastreó 1642 fallas de ejecución de múltiples agentes. 21.3% eran lagunas de verificación  el sistema envió una respuesta que nadie había verificado. El 79% restante a menudo se remonta a "había un cheque que falló silenciosamente o nunca se ejecutó".

> Cemri 等人(MAST) ha rastreado 1642 agentes  ejecutar fracaso。21.3% es una deficiencia de verificación el sistema ha publicado respuestas que nadie ha revisado。 el resto del 79% suele remontar a "un examen silencioso ha fallado o nunca ha funcionado"。 la verificación es un papel importante。

El número 21,3% es la estadística más citada en la ingeniería multiagente de 2026. Dice: si solo añades un papel a tu sistema, conviértelo en un verificador.

> El 21,3% es la cifra más citada en el proyecto de agentes de más de 2026 años. Dice: si sólo se añade un papel en el sistema, que se convierta en verificador. No es un crítico, no es un planificador.

PwC informó (CrewAI deployments, 2025) que agregar un bucle de validación estructurado movió la precisión del 10% al 70%.

> PwC  informe CrewAI 部署,2025) añadir un ciclo de verificación estructurada aumentará la tasa de precisión del 10%  hasta el 70%― un rol traerá un aumento de 7 veces―.

### Critico frente a verificador

- Un crítico es un magistrado que revisa un artefacto por calidad.
  El crítico es un LLM de calidad de un objeto de revisión.
- Un verificador es un programa determinista que se ejecuta en el artefacto. Objetivo.
  El verificador es un proceso de determinación que se ejecuta en el trabajo.

Utilice ambos. El crítico capta los problemas de sabor que el verificador no puede articular. El verificador capta errores que el crítico no puede ver porque sólo aparecen en el tiempo de ejecución.

>  ambos usan                                                                                                                                                                                                                                                             

Un orden común: primero verificador (rápido, mata obviamente el trabajo roto), luego crítico (lento, refina la calidad). Algunos equipos vuelven el orden para detectar problemas de sabor antes de gastar computación en código roto.

> 常见顺序:先验证者(快,杀死明显破损工作),然后批评者(慢,精炼质量) ―― algunos equipos翻转顺序以在花计算资源修复破损代码之前抓获质量问题──测试哪种适合你的任务──

### El antipatrón

Cada rol en su sistema es un LLM y cada rol de salida es "me parece bien". Modo de falla MAST clásico. Agregue al menos un verificador cuyo pase / fracaso se decide por código, no por un LLM.

> Cada rol en tu sistema es LLM, cada rol de salida es "parece mal"―¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡

### Mapas de marco

- **CrewAI**¿ Qué es esto ?`Agent(role, goal, backstory)`es la superficie de especialización de libros de texto.
  En inglés:**CrewAI**¿ Qué es esto ?`Agent(role, goal, backstory)`Es la superficie de especialización de la enseñanza.
- **LangGraph** los nodos pueden tener instrucciones especializadas; los bordes forzan la tubería.
  En inglés:**LangGraph** 节点可以有专门提示;边强制流水线──
- **AutoGen** Agentes conversables específicos de rol con nombres de una palabra en un Chat de grupo.
  En inglés:**AutoGen** En GroupChat tiene un único nombre de personaje específico ConversableAgent。
- **OpenAI Agents SDK** herramientas de intercambio entre agentes especializados en funciones.
  En inglés:**OpenAI Agents SDK** 角色专业化 Agent 之间的交接工具──

## Construye y realiza.
```figure
swarm-roles
```

## Construye el mismo

`code/main.py`Implementa una línea de 4 funciones que construye una función Python simple:

> `code/main.py`实现 una construcción simple Python  función de 4 角色流水线:

- **Planner**produce una especificación.
  En inglés:**规划者**产生规范── en el que se
- **Executor**genera una cadena de código.
  En inglés:**执行者**¿Qué es eso?
- **Critic**(SIMULACIÓN de LLM) señala problemas obvios.
  En inglés:**批评者**(LLM 模拟) 标记明显问题──
- **Verifier**ejecuta el código generado en una caja de arena (`exec`) contra un caso de ensayo.
  En inglés:**验证者**En la caja`exec`) en el caso de la prueba de uso de código de ejecución generado.

Demo se ejecuta dos veces: una vez cuando el ejecutor produce código correcto (crítico + verificador ambos pasan), una vez cuando el ejecutor produce código fuera de especificación (el crítico pierde el error porque parece plausible, el verificador lo captura porque la prueba falla).

> 演示运行两次:一次执行者产生正确的代码(批评者 + 验证者都通过),一次执行者产生偏离规范的代码(批评者因为看起来合理而错过错误,验证者因为测试失败而捕获它) 

## Usalo con el marco de ejecución

`outputs/skill-role-designer.md`toma una tarea y produce la lista de roles (3-5 roles), el esquema de entrada/salida por función y la verificación del verificador.

> `outputs/skill-role-designer.md`接收任务并产生角色名册(3-5 个角色) 、 cada rol de entrada/salida de los modelos y verificador de control.

## Envíe el producto .

Lista de control:

> 检查清单:

- **At least one deterministic verifier.**Nunca todo-LLM.
  En inglés:**至少一个确定性验证者。**Nunca más todo LLM.
- **Explicit I/O schema per role.**El planificador devuelve una especificación, no una prosa; el ejecutor lee ese esquema.
  En inglés:**每个角色有明确的 I/O 模式。**规划者回归规范,不是散文;执行者读取该模式──
- **Communicative dehallucination.**El ejecutor debe preguntar al planificador cuándo falta información; nunca la invente.
  En inglés:**交流去幻觉。** ejecutor en la falta de información debe preguntar al planificador; nunca inventar.
- **Critic/verifier ordering.**ejecuta primero el crítico (barato, detecta problemas de diseño), el verificador segundo (lento, detecta errores).
  En inglés:**批评者/验证者顺序。**Previo, el proyecto de investigación de la Universidad de San Francisco, en el que se desarrolló la investigación, se ha desarrollado un nuevo proyecto de investigación y desarrollo de la investigación.
- **Loop budget.**Max 2 rondas de revisión de crítico ejecutor antes de escalar a humano.
  En inglés:**循环预算。**En el nivel de la humanidad, más de 2 críticos-executivos modificaciones.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`y observar cómo el verificador detecta el error que el crítico no ha observado.`return`¿Qué detecta si el test de tiempo de ejecución se pierde?
   Traducción:运行`code/main.py`Y observar cómo el verificador captura el error del crítico.`return`¿Qué ha sido capturado durante la prueba?
2. Añadir un quinto papel: "analista de requisitos" que traduce el deseo del usuario en especificación lista para planificar. ¿Qué solicitudes de deshallucinación comunicativa deberían fluir hasta él?
   China: 添加第五个角色:"需求分析师",将用户愿望翻译为规范可用规范──什么样的交流去幻觉请求应该流上方?
3. Lea la sección 3 de MetaGPT ("Agentes"). Enumera el esquema de entrada/salida de cada uno de los 5 roles de MetaGPT.
   En el caso de los grupos de trabajo, el grupo de trabajo de los trabajadores de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de trabajo de la empresa de la empresa de trabajo de la empresa de la empresa de trabajo de la empresa de la empresa de trabajo de la empresa de la empresa de la empresa de trabajo de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de
4. Lea el diagrama de la cadena de chat de ChatDev (arXiv:2307.07924 Figura 3). Identifique dónde la deshallucinación comunicativa rompe un bucle que de otro modo sería infinito.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
5. La ganancia de precisión de 7 veces de PwC proviene de los bucles de verificación.
   China Translation:PwC 7 veces la tasa de precisión aumenta de la verificación ciclo. Suponemos que tres pruebas adicionales no ayudarán tareas.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Más Leer más Leer más

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) el documento de referencia de la POP-as-role-prompt
  El texto de la metaGPT:多 Agent 协作的元编程  SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) cadena de chat + deshallucinación comunicativa
  China 文翻译:Qian 等人  软件开发的通信代理(ChatDev) 聊天链 + 交流去幻觉
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomía MAST; las brechas de verificación representan el 21,3% de las fallas
   ¿Por qué muchos agentes LLM 系统会失败? MAST 分类法;验证缺口占失的21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) Superficie de especificación de rol de producción
  文档  Agente 角色  生产角色规范表面
