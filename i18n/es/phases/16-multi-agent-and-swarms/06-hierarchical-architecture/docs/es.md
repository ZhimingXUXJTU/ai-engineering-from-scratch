# Arquitectura jerárquica y su modo de fracaso.

> La jerarquía es supervisor anidado, agentes gerentes sobre subgerentes sobre trabajadores.`Process.hierarchical`es la versión del libro de texto: a `manager_llm`La función de la función de evaluación de las variables de trabajo es la de la función de evaluación de las variables de trabajo.`create_supervisor(create_supervisor(...))`. Es el patrón natural cuando la tarea es un organograma real. También es el patrón más probable que se desplome en un bucle de gestión.

> **【中文解读】**Este capítulo presenta la estructura de la organización de los ordenadores de múltiples niveles, que se aplica a la descomposición de tareas complejas.

> **【拓展：hierarchical architecture→具体应用】**La estructura de nivel compartido devolverá el patrón de supervisor a los administradores de nivel superior distribuidos a los administradores de nivel medio, los administradores de nivel medio distribuidos a los trabajadores de nivel bajo. Esto es similar a la estructura de nivel de la organización humana. La práctica de 2026 muestra que los niveles de 2 a 3 niveles son los más optimistas.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**學本節前請先掌握:Fase 16·05(Supervisor 模式) ・・・本节 = Supervisor 嵌套 Supervisor多层管理。失败模式 = "los gerentes abren las reuniones y no hacen nada"―
> ¿ Qué es esto ?**【类比】**La estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la empresa es la siguiente: la estructura de la estructura de la empresa es la estructura de la empresa es la estructura de la empresa es la estructura de la empresa es la estructura de la empresa esfera es la empresa es la estructura de la empresa esfera de la empresa esfera de la empresa esfera de la empresa esfera de la empresa esfera de la esfera de la empresa esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la empresa esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la empresa: la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la es
> ️ **【易错点】**见"任务复杂"就加层级 → 管理开销压系统──修复:先用序列或监督 单层跑,确认不够再分层;2-3层是上限──

## # El problema # # El problema #

Una vez que el patrón de supervisor hace clic, el siguiente paso natural es "¿qué pasa si los trabajadores son supervisores?" Los equipos tienen sub-equipajes; las empresas tienen departamentos de departamentos.

> Una vez que el modelo de supervisor se entiende, el siguiente paso de la naturaleza es "¿Si el trabajo en sí mismo es supervisor?" el equipo tiene un sub-grupo; la estructura de las empresas tiene un departamento.

La tentación es fuerte porque las organizaciones humanas trabajan de esta manera. Pero las jerarquías LLM heredan todas las patologías de las jerarquías humanas (pérdida de información, falta de comunicación, iteración lenta) sin los efectos estabilizadores de las relaciones humanas y la cultura compartida.

> La tentación es fuerte, porque las organizaciones humanas trabajan así. Pero el nivel de LLM hereda todos los estados de la humanidad, sin tener un efecto estable en las relaciones humanas y en la cultura compartida.

El problema es que los gerentes de LLM no son lo mismo que los gerentes humanos. Un gerente humano tiene antecedentes estables sobre lo que sus informes saben. Un gerente de LLM vuelve a razonar la organización a cada paso desde lo que está en su contexto.

> problemas en:LLM administrador manager humano administrador humano  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrador  Human administrator  Human administrator  Human administrador  Human administrator   Human  Human administrator  Human administrator  Human     Human  Human  Human               

Este es el modo de fracaso principal de los sistemas jerárquicos de LLM: cada nivel de gerente amplifica los errores del nivel anterior.

> Este es el modelo de fracaso central del sistema LLM: cada nivel de gerente aumenta el error de la capa superior.

## Concepto de la esencia de la concepción

### La forma

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Cada nodo interno planea, delega y sintetiza.

> Cada uno de los nodos internos tiene un plan, un comité y un conjunto.

Esto refleja una tabla de órganos humanos, que es tanto su fortaleza (modelo mental familiar) como su debilidad (los órganos humanos tienen antecedentes estables que faltan a los LLM).

> Esta es una reflexión de la estructura de la organización humana, que es a la vez su ventaja (concientes modelos de mentalidad) y su debilidad (con la falta de una prioridad estable en la organización humana).

### Donde brilla

- **Clear org mapping.**Si la tarea real es departamental ("revisión legal del documento, revisión financiera del documento, revisión de ingeniería del documento, luego resumen para ejecutivo"), la jerarquía es explícita.
  En inglés:**清晰的组织映射。**Si la tarea real es de carácter departamental, la estructura de nivel es clara.
- **Local summarization.**Cada sub- gerente sintetiza la producción de su equipo antes de que el gerente superior la vea.
  En inglés:**局部摘要。**Cada administrador de nivel superior ve antes la generación de su equipo de salida.

### Donde se rompe

Tres modos de falla que los post mortem 2026 siguen encontrando:

> En el año 2026 el análisis de sucesos constantes encontró tres modelos de fracaso:

Cemri et al. (MAST, arXiv:2503.13657) documenta estas como "fallas de especificación" y "desalineamiento interpersonal" subfamilias.

> Cemri 等人(MAST,arXiv:2503.13657) llevará estos registros a la "规范失败" y "人际不对齐"子家族──分层系统比平系统更容易出现这些问题,因为每层添加重新解释步骤──

1. **Task assignment error.**El gerente lee la meta, alucina una descomposición y delega a un sub-gerente equivocado. Debido a que el sub-gerente obedece a lo que se le dio, el error solo aparece en la síntesis superior.
   En inglés:**任务分配错误。**管理者读取目标,幻觉出分解,并委派给错误的子管理者──因为子管理者服从处理给定的任务, errores sólo surgen en la posición superior a la que podría captarse el ser humano.
2. **Output misinterpretation.**El subdirector devuelve "no puede verificar la reclamación X". El máximo gerente resume como "la reclamación X no confirmada". El significado deriva en todos los niveles.
   En inglés:**输出误解。**"Gestión de la información" no puede ser verificada.
3. **Consensus loops.**Dos subdirectores no están de acuerdo; el gerente superior les pide que se reconcilien; se re-delegan hacia abajo; los trabajadores vuelven a correr; los subdirectores devuelven respuestas ligeramente diferentes; bucle.`Process.hierarchical`El límite de la medida es un hiperparámetro.
   En inglés:**共识循环。**两个子管理员不一致; dos hijos administradores no coinciden; dos hijos administradores de alto nivel exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores exigen que coordinen; dos hijos administradores reorganicen; dos hijos administradores retornan con respuestas diferentes; dos hijos administradores reorganizan; dos hijos administradores reorganizan; dos hijos administradores reorganizan; dos hijos administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; dos miembros administradores reorganizan; y dos miembros de la red.`Process.hierarchical`通过步骤限制来保护, pero la limitación en sí misma es ahora un superparámetro.

### La cuestión decisiva

Secuenciales (linera) vs jerárquicos: ¿tiene su tarea sub-equipajes independientes o es un flujo lineal que finge ser un árbol?

> 顺序(线性流水线) vs 分层: ¿Tu tarea realmente tiene un subgrupo independiente, también es un proceso lineal en el árbol? Si es el último, utiliza la顺序. Si es el primero, utiliza las divisiones pero debe presupuestar claramente las reglas de coordinación.

Esta es la prueba que la mayoría de los equipos omiten. Se acercan a la jerarquía porque suena sofisticada, luego pasan semanas desactivando la deriva de descomposición.

> Es el examen que la mayoría de los equipos saltaron. Ellos escogen las camadas porque parecen altas, y luego pasan varias semanas en la preparación para desmontar las camadas.

### Implementación de la CrewAI
### Implementación del marco de trabajo

El equipo de la tripulación `Process.hierarchical`El gerente:

> `Process.hierarchical`En un equipo de expertos en el área de la educación superior.

El gerente LLM es en sí mismo un agente completo con su propio contexto, prompt y herramientas. No es un despachador determinista  hace llamadas de juicio sobre la delegación, lo que significa que puede hacer llamadas de juicio equivocadas. Esta es la fuente del modo de fracaso de asignación de tareas.

>  Administrador LLM en sí mismo es un agente completo de su propio contenido  sugerencias y herramientas  no es un regulador de determinación  que hace juicios sobre el uso de los comités, lo que significa que puede hacer juicios erróneos   es la fuente del modelo de asignación de tareas fallido

- recibe la tarea de nivel superior,
  En inglés, el nombre de la misión es "Traducir".
- asigna subtareas a las tripulaciones,
  Se asignará las tareas a la tripulación.
- evalúa las producciones de la tripulación,
  Traducción: evaluación equipo de producción,
- decide si se acepta, se re-delega o se repite.
  China: decisión es aceptar, volver a encargarse o no.

Documentación: https://docs.crewai.com/en/introduction(Buscar "Proceso jerárquico" en los conceptos centrales).

> 文档:https://docs.crewai.com/en/introduction（在核心概念中查找"HierarchicalProceso")

### La aplicación de LangGraph
### Implementación del marco gráfico

LangGraph utiliza el anidado `create_supervisor`El supervisor interno tiene su propio gráfico; el supervisor externo trata el gráfico interno como un nodo opaco. Esto es más limpio que CrewAI para el depuración (puedes pasar por cada gráfico por separado) pero es más difícil expresar la remodelación dinámica del árbol.

> LangGraph utiliza un conjunto de`create_supervisor`调用──内部监督人有自己的图;外部监督人将内部图视为不透明节点──这在调试方面比 CrewAI更清晰(puedes diferenciar los pasos en cada图), pero es más difícil expresar el movimiento del árbol reformulación──

La victoria de depuración es real: cuando algo sale mal en una jerarquía de LangGraph de 3 niveles, se puede aislar el nivel fallido pasando por cada gráfico de forma independiente.

> 调试优势真实: Cuando los niveles de 3 niveles de LangGraph se equivocan, puedes pasar por pasos independientes en cada uno de ellos para separar los niveles que han fracasado. En CrewAI, el MLL de gerente es un posible uso de la falta de transparencia.

Referencia: https://reference.langchain.com/python/langgraph-supervisor.

>  referencia:https://reference.langchain.com/python/langgraph-supervisor。

## Construye y realiza.
```figure
swarm-hierarchy-token
```

## Construye el mismo

`code/main.py`ejecuta una jerarquía de 3 niveles:

> `code/main.py`¿Qué es esto?

- gerente superior: divide una tarea en ramas "ingeniería" y "legal",
  La división de tareas se divide en "工程 " y "法务 "分支,
- Subdirector de ingeniería: se divide en trabajadores "frontend" y "backend",
  Ingeniero: separado en "pronto" y "trasto"
- Subdirector legal: un trabajador.
  El gobierno de la República de China ha sido el primer gobierno de la República de China.

Demo contrasta camino feliz (todos están de acuerdo) con un **perturbed path**donde la descomposición del gerente superior etiqueta erróneamente "legal" como "financiamiento" y observa la cascada de errores  el subgerente obedece a los trabajos financieros, el sintetizador superior informa los hallazgos financieros, la pregunta legal original queda sin respuesta.

> 演示对比了正常路径 (¿todos los que están en paz?)**扰动路径**, de los cuales la clasificación de los administradores de alto nivel se etiquetará erróneamente como "financieros" y observará errores de nivel asociado 子 administradores obedecen a hacer trabajo financiero, el informe de los integradores de alto nivel se encuentra en el informe financiero, los problemas legales originales no han sido respondidos.

El camino perturbado es la advertencia: los sistemas jerárquicos amplifican los errores en silencio. El sub- gerente no retrocede ("has dicho finanzas, pero la tarea dijo legal"). Asume que el gerente sabe mejor.

>  perturbatorial ruta es una advertencia: el sistema está silencioso ampliando el error.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La salida muestra ambos caminos con un lado a lado claro de "lo que se pidió" vs "lo que se entregó".

> 输出显示两条路径的清晰并排对比:" exigir qué"与"交付了什么"──

## Usalo con el marco de ejecución

`outputs/skill-hierarchy-fitness.md`evalúa si una tarea dada debe utilizar un supervisor jerárquico, secuencial o plano. Ingresos: descripción de tareas, estructura de organizaciones, presupuesto de reconciliación.

> `outputs/skill-hierarchy-fitness.md` evaluación de las tareas determinadas debe utilizarse en la clasificación 序列还是平监督者──输入: descripción de tareas、 organización estructura、 coordinación presupuesto──输出:模式建议及需要防护的特定失败模式──输入:

## Envíe el producto .

Si envías jerárquicos:

> Si usted está en la estructura de la división:

- **Cap tree depth at 2.**Tres niveles ya ocultan la mayoría de los errores de la observabilidad.
  En inglés:**将树深度限制在 2。**Tres niveles ya han ocultado la mayoría de los errores fuera de la observabilidad.
- **Explicit reconciliation budget.**Establezca un máximo de rondas antes de que el gerente superior se comprometa.
  En inglés:**明确的协调预算。**En la cima de la dirección debe presentarse antes de establecer el número máximo de rotas.
- **Provenance on every synthesis.**El resumen de cada nodo debe indicar qué salidas de hoja lo produjeron.
  En inglés:**每次综合的来源追溯。**El resumen de cada nodo debe citar la salida de sus hojas.
- **Alert on decomposition drift.**Registre la descomposición del administrador por paso; difiere de la consulta del usuario. Si la descomposición ya no cubre la consulta, active una alerta.
  En inglés:**分解漂移告警。**记录管理员的每步的分解;与用户查询对比. 记录管理员的每步的分解;与用户查询对比.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Cuántos niveles de entrega del gerente se necesitan antes de que la salida superior se desvíe completamente de la pregunta del usuario?
   Traducción:运行`code/main.py`¿Cuántos niveles de administradores necesitan comunicarse para que los niveles superiores de salida estén completamente alejados del usuario?
2. Añadir un tercer nivel (top -> sub -> sub-sub -> trabajador). Medir la frecuencia con la que el camino perturbado se corrige a sí mismo vs. diverge completamente a medida que crece la profundidad.
   La medida aumenta con la profundidad, perturba la rectación del camino de la autocorrección y la frecuencia de la total desviación.
3. Implemente un trabajador "canario" en cada sub-administrador que siempre se le haga la pregunta original al usuario sin cambios. Utilice la respuesta canaria para detectar la deriva de descomposición. ¿Cómo debe reaccionar el administrador cuando el canario no está de acuerdo con la respuesta sintetizada?
   Traducción:En cada hijo administrador se realiza una "Kinsagris" de trabajo, siempre se le pregunta sobre el problema del usuario original. ¿Cómo debe reaccionar el administrador cuando el sistema de análisis de la respuesta original no coincide con la respuesta integral?
4. Lea el artículo de CrewAI `Process.hierarchical`Documents. Identifique una barrera de seguridad de concreto que CrewAI aplica (limite de paso, restricción manager_llm) y describa el modo de falla al que se dirige.
   La historia de la tripulación de la tripulación`Process.hierarchical`文档──识别 CrewAI 应用一个具体防护措施(步骤限制、manager_llm 约束)并描述它针对的失败模式──
5. Comparar los supervisores de LangGraph anidados con los jerárquicos de CrewAI. ¿Qué hace que los bucles de reconciliación sean más baratos de detectar?
   China Translation: Comparación de los sistemas de LangGraph 监督者 con CrewAI 分层── ¿cuál hace que el ciclo de coordinación sea más fácil de detectar?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Más Leer más Leer más

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) Manual jerárquico con un gerente LLM
   Proceso.hierárquico  带管理者 LLM 的教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) supervisor en el cuadro de trabajo`create_supervisor`
  中文翻译:LangGraph 监督者参考  通过 `create_supervisor`de los supervisores de la
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system)¿Por qué Anthropic eligió deliberadamente a un supervisor plano sobre una jerarquía
  China 工程 研究系统  Why Anthropic 有意选择平监督者而不是分层
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomía MAST; sección sobre fallos de coordinación documentación de descomposición deriva
   ¿Por qué muchos agentes LLM 系统会失败?  MAST 分类法;协调失败部分记录了分解漂移
