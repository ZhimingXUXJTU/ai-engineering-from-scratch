# Reflexión: Aprendizaje de refuerzo verbal. Reflexión: lenguaje fuerte

> La RL basada en gradientes necesita miles de pruebas y un grupo de GPU para arreglar un modo de falla. Reflexion (Shinn et al., NeurIPS 2023) lo hace en lenguaje natural: después de cada ensayo fallido, el agente escribe una reflexión, la almacena en la memoria episódica y condiciona el siguiente ensayo en esa memoria. Este es el patrón detrás de la computación del tiempo de sueño de Letta, los aprendizajes de Claude Code en CLAUDE.md y la regla de aprendizaje pro-flujo de trabajo.

> **【中文解读】** Base en la RL de la escala  necesita miles de veces de experimentación y GPU 集群──Reflexión con lenguaje natural para lograr el auto-reforma: después de cada fracaso, el agente escribe un pasaje de reflexión en la memoria de la situación, la próxima vez que intenta referirse a estas memorias── este es el modelo detrás de la computación del tiempo de sueño de Letta、Claude Code de CLAUDE.md aprendizaje mecanismo──

> **【拓展：Reflexion → Claude Code 的自我学习】**El mecanismo de Claude Code CLAUDE.md es en esencia una variación de Reflexión.

> ¿ Qué es esto ?**【前置】**本节依赖:Fase 14·01(Agent Loop)你必须已经能跑通一个 ReAct 循环,因为 Reflexion的 Actor 内部就是一个 ReAct loop;以及Fase 14·02(ReWOO)理解"试验/轨迹"的概念──如果你分不清"一次试验"和"一个步骤",先回去补补 ReAct──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Nombre los tres componentes de la Reflexión (Actor, Evaluador, Auto-Reflector) y el papel de la memoria episódica.
  El actor, el evaluador y el autor reflejo y el papel de la memoria en el escenario.
- Implemente un bucle de reflexión stdlib con evaluador binario, buffer de reflexión y nuevos intentos de repetición.
  Con el estándar de la biblioteca de la realización de la reflexión  ciclo, contiene el evaluador de dos valores 反思缓冲区和全新重试──
- Elija entre fuentes de retroalimentación escalares, heurísticas y autoevaluaciones para una tarea dada.
  Traducción: para una tarea determinada seleccionar la cantidad, la iniciación o la autoevaluación de la fuente.
- Explica por qué el refuerzo verbal capta errores que la RL basada en gradientes necesitaría miles de ensayos para corregir.
  Traducción:Explain why language solitude can capture RL based on gradient  needs thousands of trials to correct errors―

## El problema es la introducción del problema

Un agente falla una tarea. En RL estándar se ejecutarían miles de pruebas más, calcularían gradientes, actualizarían pesas.

> El agente  ha fracasado en una tarea  En el estándar RL, necesitas ejecutar miles de veces más de pruebas  calcular la escala  actualizar el peso  costoso  lento, y la mayoría de los agentes de producción  no tienen un presupuesto de entrenamiento para cada fracaso 

La reflexión (Shinn et al., arXiv:2303.11366) hace una pregunta diferente: ¿qué pasa si el agente acaba de pensar en por qué falló y intentó de nuevo con ese pensamiento en su prompt?

> Reflexión ((Shinn 等人, arXiv:2303.11366) planteó un problema diferente: si el agente  simplemente piensa en las causas del fracaso, entonces en la próxima oportunidad de intentar incorporarse a esta idea?

El resultado: en ALFWorld supera a ReAct y otras líneas de base no afinadas. En HotpotQA mejora sobre ReAct. En la generación de código (HumanEval / MBPP) establece el estado de la técnica en el momento. Todo sin un solo paso de gradiente.

> Resultado: en ALFWorld arriba superó ReAct y otros no micro-ajustes. En HotpotQA arriba superó ReAct. En la generación de código HumanEval/MBPP arriba alcanzó el mejor nivel de entonces. Todo esto sin necesidad de un paso de escala.

## El concepto central.

### Los tres componentes

```
Actor         : generates a trajectory (ReAct-style loop)     # 执行器：生成行动轨迹
Evaluator     : scores the trajectory — binary, heuristic, or self-eval  # 评估器：评分
Self-Reflector: writes a natural-language reflection on the failure      # 自我反思器：写反思
```

Además de una estructura de datos:

```
Episodic memory: list of prior reflections, prepended to the next trial's prompt  # 情景记忆
```

Un ensayo se ejecuta en el Actor. El evaluador lo califica. Si la puntuación es baja, el Auto-Reflector produce una reflexión ("Elegí la herramienta equivocada porque mal leí la pregunta como preguntando sobre X cuando estaba preguntando sobre Y").

> ¿ Qué es esto ?**【类比】**Reflexión 像考试做错题后的"错题本"机制:你做错一道题(Actor 失败)→ 拿到对错信号(Evaluator 评分)→ 写下"我为什么错了"(Self-Reflector 写反思)→ 下次考前翻错题本(情景记忆前置到提示) ・・・ 下次重复同类题,错的概率就低了──关键是错题本(反思) con lenguaje natural escribir, no necesita volver a entrenar el derecho de modelo.

> Una vez experimenté con el actor, un evaluador, un evaluador, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor, un autor o un autor, un autor, un autor, un autor o un autor, un autor, un autor o un autor, un autor, un autor o un autor, un autor o un autor, un autor, un autor o un autor, un autor o un autor, un autor o un autor, un autor, un autor, un autor o un autor, un miembro de la autor o un miembro de la cuenta que es un miembro de la cuenta de la cuenta de la cuenta de la cuenta de la cuenta de la cuenta del propio de la cuenta del propio de la cuenta del propio propio, un proyecto de la cuenta de la cuenta del autor o un proyecto de la cuenta del autor o un proyecto de la cuenta del autor, un proyecto de la cuenta del autor o un proyecto de la cuenta del autor, pero puede ver si se puede ver si se haya, pero puede ver si no, pero puede ver si no, "lo que es contrario, "lo contrario, pero puede ver si bien que es contrario, "lo contrario, "lo que es contrario, "lo que es contrario, "lo que es contrario, "lo que es contrario, "lo que es contrario, "lo que es contrario, "ha, es contrario, es contrario, es contrario, es contrario, es, es,

### Tres tipos de evaluadores

1. **Scalar** una señal binaria externa. ALFWorld tiene éxito o falla. HumanEval pasa o falla.
   En inglés:**标量** Exterior 2元信号──ALFWorld éxito o fracaso──HumanEval 测试通过或不通过──最简单,信号最强──
2. **Heuristic** firmas de falla predefinidas. "Si el agente produjo la misma acción dos veces seguidas, marque como atascado". "Si la trayectoria excede de 50 pasos, marque como ineficiente".
   En inglés:**启发式**预定义的失败签名──"Si el agente 连续两次产生相同行动,标记为卡住──""Si la trayectoria supera los 50 pasos, se marca como de bajo efecto──"
3. **Self-evaluated** el LLM obtiene su propia trayectoria. Necesitada cuando no hay ninguna verdad básica disponible.
   En inglés:**自评估**LLM a su propio trayectorio                                                                                                                                                                                                                                                          

El 2026 por defecto es una mezcla: escalar cuando está disponible, autoeval cuando no, heurísticas como carriles de seguridad.

> ️ **【易错点】**Tres tipos de evaluadores: en la tarea de escribir creativo, como "respuesta sin estándares", el evaluador escalar continuará generando "señales de fracaso"→ Agente 拼命反思 → Pero el reflejo en sí mismo no tiene sentido → 浪费 token hasta gastar el presupuesto.**后果**El ciclo de cambio de dinero.**一行修复**El primer ejemplo es el de la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals" para la clasificación de los "fail signals".

> El método de evaluación de la seguridad de los productos de la UE es el uso mixto: con un valor de referencia, sin tiempo de autoevaluación, y con un valor de seguridad de la UE.

### ¿Por qué esto generaliza

La reflexión no es un nuevo algoritmo sino un patrón nombrado.

> La reflexión es un nuevo algoritmo, no como decir un modelo de nombre.

- Computación del tiempo de sueño de Letta (lección 08): un agente separado reflexiona sobre conversaciones pasadas y escribe a los bloques de memoria.
  La computación del tiempo de sueño de Letta (第 8 课): un agente independiente Reflexión de conversaciones y escritura en un bloque de memoria.
- El código de Claude `CLAUDE.md`/ patrón de "salvar memoria": reflejos capturados como aprendizajes, prependidos para futuras sesiones.
  El código de Claude`CLAUDE.md`/"conservar los recuerdos" mode: el reflejo es capturado para la experiencia de aprendizaje, prepujado a la conversación futura.
- Pro-flujo de trabajo `/learn-rule`comando: correcciones capturadas como reglas explícitas.
  La política de trabajo en el país`/learn-rule`命令:纠正被捕为显式规则──
- Los nodos de reflexión de LangGraph: un nodo que califica la salida y las rutas para refinar si es necesario.
  Un punto de reflexión de un gráfico largo: un punto de reflexión que se realiza en el tiempo necesario.

Todos derivan de la misma visión: el lenguaje natural es un medio lo suficientemente rico como para llevar "lo que aprendí del fracaso" entre carreras.

> Todos ellos se originan en la misma idea: el lenguaje natural es un medio suficientemente rico, que puede transmitirse entre las operaciones "qué aprendí en el fracaso" (I learned from failure in the course of life).

> **【拓展：Reflexion → 生产环境的自我修复】**几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体:Letta's sleep-time computing 异步反思、Claude Code's CLAUDE.md 存储学习经验、LangGraph's反思节点──核心洞察相同:自然语言足够承载"从失败中学到了什么"──

### Cuando funciona y cuando no funciona

La reflexión funciona cuando:

> La reflexión en las siguientes situaciones es válida:

- Hay una señal clara de falla (fallo de prueba, error de herramienta, respuesta incorrecta).
  China: Cómen claro de la falta de éxito (testing failure, tool err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err
- La clase de tareas es reproducible (el mismo tipo de pregunta puede ser repetida).
  En inglés, el nombre de la persona que se encuentra en el grupo de trabajo es "Traducción de la persona que está en el grupo de trabajo".
- La reflexión tiene margen para mejorar la trayectoria (presupuesto de acción suficiente).
  Traducción:Reflexión: Reflexión sobre el desarrollo de la economía.

La reflexión no ayuda cuando:

> La reflexión en las siguientes situaciones no ayuda:

- El agente ya tiene éxito en el primer intento.
  En inglés, "Agent" es el nombre de un agente.
- El fallo es externo (red baja, herramienta rota)  la reflexión sobre "la red estaba baja" no ayuda a futuras ejecuciones.
  El fracaso es un "interrupto de red" externo.
- La reflexión se convierte en superstición  almacenando una narrativa sobre una carrera escamosa única.
  Sinopsis: El libro de la historia de la vida de un hombre que se ha convertido en un fantasma.

2026 trampa: rotura de la memoria. Las reflexiones se acumulan; algunas son obsoletas o incorrectas; las re-runs se vuelven más lentas a medida que crece el amortiguador episódico. Mitigation: compactación periódica (lección 06), TTL en las reflexiones, o un agente de limpieza separado del tiempo de sueño (Letta).

> ¿ Qué es esto ?**【困惑】**P: Reflexión 真的能"等价于"RL 吗?RL 改是模型权重,Reflexión 改只是快速,机制完全不同──A: 不能等价──论文标题"Verbal RL"是修辞而非数学等价──Reflexión 优势是**样本效率极高**Con 3-5 veces de reflexión se puede reparar un modelo fallido, mientras que RL requiere miles de veces de actualización gradual; el desventaja es**反思不会持久**Hasta el peso del modelo, cada nueva sesión se debe aprender. Así que la reflexión se adapta a la "escena de producción sin presupuesto entrenado",

> La situación de la región de la caída de la memoria se ha vuelto más lenta. La caída de la memoria se ha producido en el año 2026.

## Construye y realiza.
```figure
react-trace
```

## Construye el mismo

`code/main.py`El actor emite listas de candidatos; el evaluador verifica la suma; el autorreflector escribe una línea sobre lo que salió mal. La reflexión entra en la memoria episódica para el próximo ensayo.

> `code/main.py`En un juego  Tema de realización Reflexión: generar una lista de 3 elementos y para el valor objetivo.

Componentes:

> 组件:

- `Actor` una política guionada que mejora cuando ve reflejos.
  En inglés:`Actor` ver reflexión  mejorar la estrategia de guión 
- `Evaluator.binary()` Pasar/fallar en la suma objetivo.
  En inglés:`Evaluator.binary()` por el fracaso de la decisión de la meta y de la meta.
- `SelfReflector` genera un diagnóstico de falla de línea única.
  En inglés:`SelfReflector`generando una línea de diagnóstico de fracaso
- `EpisodicMemory` una lista limitada con semántica TTL.
  En inglés:`EpisodicMemory`带 TTL 语义的有界列表──

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra tres ensayos. El ensayo 1 falla, se almacena un reflejo, el ensayo 2 ve el reflejo y mejora pero aún falla, el ensayo 3 tiene éxito. Compare con una carrera de base (sin reflejo)  se queda atascado en la respuesta del ensayo 1.

> 轨迹显示三次试验──试验1 失败,储备反思,试验2 看到反思并改进但仍失败,试验3 成功──与基线运行(无反思)对比它停留在试验1的答案──

## Usalo con el marco de ejecución

LangGraph envía la reflexión como un patrón de nodos.`/memory`de comando y de flujo de trabajo pro `/learn-rule`El equipo de cálculo de tiempo de sueño de Letta ejecuta el autorreflector en tiempo de inactividad para que el agente principal permanezca limitado a la latencia. OpenAI Agents SDK no envía Reflexion directamente; lo construye con un Guardrail personalizado que rechaza las trayectorias por puntaje y memoria.`Session`que sobrevive a través de las corrientes.

> LangGraph se reflejará como un modelo de punto de suministro.`/memory`命令和 pro-workflow de `/learn-rule`La información de la información de la agencia de inteligencia (OpenAI Agents SDK) no proporciona directamente la reflexión; utiliza Guardrail (en función del número de huellas) y la memoria de la agencia de inteligencia (en función de la cantidad de huellas)`Session`Vamos a construirlo.

## Envíe el producto .

`outputs/skill-reflexion-buffer.md`crea y mantiene un amortiguador episódico con captura de reflejos, TTL y deduplicación. Dada una clase de tareas y un fracaso, emite un reflejo que realmente ayuda al siguiente ensayo (no un genérico "ten más cuidado").

> `outputs/skill-reflexion-buffer.md`创建并维护带反思捕获、TTL 和去重的情景缓冲区──给定任务类别和失败, generó un fragmento realmente que ayudó a la próxima prueba de反思((而非通用"要小心")

## Los ejercicios.

1. Cambiar de evaluador binario a evaluador escalar que devuelve una métrica de distancia (qué tan lejos de la meta). ¿Converge más rápido?
   ¿Será que el evaluador se cambiará de la segunda moneda a la de regreso de la distancia de la medida?
2. Añadir un TTL de 10 pruebas a las reflexiones. ¿Las reflexiones más viejas hacen daño o ayudan después de ese punto?
   Traducción:Defender el reflejo a 10 veces de la prueba TTL.
3. Implementar evaluador heurístico: marque el ensayo como atascado si se repite la misma acción. ¿Cómo interactúa esto con el autorreflector?
   En la actualidad, el sistema de evaluación de la actividad se ha desarrollado de forma continua.
4. ¿Cuál es la ingeniería mínima de la reflexión que obliga al actor a notarlas?
   La acción de la acción es una acción de la acción. ¿Qué es lo que más se necesita para hacer que el actor tome nota de la acción?
5. Leer la sección 4 del artículo Reflexion sobre AlfWorld. Reproduce el aumento del 130% de la tasa de éxito conceptualmente: ¿cuál es la clave delta vs. vanilla ReAct?
   China Translation: Read Reflexion 论文 4 节关于AlfWorld的内容──概念重现 130%成功率改进:相比原始ReAct的关键区别是什么?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Reflexion | "Self-correction" / "自我纠错" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory / Shinn 等人 2023——Actor、Evaluator、Self-Reflector 加情景记忆 |
| Verbal reinforcement | "Learning without gradients" / "无梯度学习" | Natural-language reflection prepended to the next trial's prompt / 自然语言反思前置到下一次试验的提示 |
| Episodic memory | "Per-task reflections" / "按任务的反思" | Bounded buffer of prior reflections for one task class / 一个任务类别的先前反思有界缓冲区 |
| Scalar evaluator | "Binary success signal" / "二元成功信号" | Pass/fail or numeric score from ground truth / 来自真值的通过/失败或数值评分 |
| Heuristic evaluator | "Pattern-based detector" / "基于模式的检测器" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) / 预定义的失败签名（如卡住循环、步数过多） |
| Self-evaluator | "LLM-as-judge on own trace" / "LLM 评价自身轨迹" | Lower-signal fallback when no ground truth — pair with tool-grounded verification / 无真值时的低信号后备——与工具锚定验证配合 |
| Memory rot | "Stale reflections" / "过时反思" | Episodic buffer fills with obsolete entries; fix with compaction/TTL / 情景缓冲区填满过时条目；用压缩/TTL 修复 |
| Sleep-time reflection | "Async self-reflection" / "异步自我反思" | Run Self-Reflector off the hot path so primary agent stays fast / 在非关键路径上运行 Self-Reflector 使主 Agent 保持快速 |

## Más Leer más Leer más

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) el papel canónico
  Reflexión 经典论文语言 Agent 的语言强化学习──
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) reflejo de asíncrono en la producción
  Lettera  Sobre el cambio de pensamiento en el entorno de producción.
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) Gestión del amortiguador episódico como parte del contexto
  En el texto de la serie de artículos sobre el proyecto de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la IA, el director de la organización de la organización de la IA, el director de la organización de la organización de la IA, el director de la organización de la organización de la CIA, el director de la agencia de la CIA, el director de la agencia de la agencia de la CIA, el director de la agencia de la agencia de la CIA, el director de la agencia de la agencia de la CIA, el director de la agencia de la agencia de la CIA.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) patrón de nodo de reflexión
  En el lenguaje chino, el lenguaje es el lenguaje de la lengua.
