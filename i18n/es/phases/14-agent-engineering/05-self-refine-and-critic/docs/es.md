# Auto-refinado y crítico: mejora iterativa de la producción .

> Self-Refine (Madaan et al., 2023) utiliza un LLM en tres roles  generar, retroalimentación, refinar  en un bucle. La ganancia promedio: +20 absoluta en 7 tareas. CRITIC (Gou et al., 2023) endurece el paso de retroalimentación mediante la verificación de enrutamiento a través de herramientas externas. En 2026 este patrón se envía en cada marco como "evaluador-optimizador" (Antropic) o un bucle de barandillas (OpenAI Agents SDK).

> **【中文解读】**Auto-refinar  hacer que un LLM desempeñe tres papeles: generar 反、精炼, ciclo de mejora. 7 个任务平均提升 20 个百分点──CRITIC 将验证步骤通过外部工具 (extraño de búsqueda, código explicador, calculador) 进行强化.

> **【拓展：CRITIC → Claude Code 的自我修复】**Claude Code en la redacción de código se ejecuta automáticamente después de la prueba de prueba. Esto es la realización de la producción de un modelo crítico. Cuando el test falla, se basa en el error de la modificación del código hasta que el test pasa.

> ¿ Qué es esto ?**【前置】**必須先過:Fase 14·01(Agent Loop) y Fase 14·03(Reflexión)。Self-Refine es la versión de Reflexión de "单次任务内" ̇Reflexión 跨多次试验,Self-Refine 在一次生成内代)。 no entiendo el mecanismo de Reflexión de "反思存存到记忆",会混的"反不持久化"特征──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Las tres instrucciones de Auto-Refinación del Estado (generar, retroalimentación, refinar) y explicar por qué la historia es importante para el instante de refinar.
  La historia de la refinería es importante.
- Explica la visión crítica de CRITIC: Los LLM no son confiables en la autoverificación sin fundamento externo.
  Traducción:Critic: no hay ninguna prueba externa, la prueba de sí misma es inestable.
- Implemente un bucle de auto-refinado stdlib con historial y un verificador externo opcional.
  Traducción:Use estándar biblioteca para lograr con registro histórico y auto-refinado ciclo de verificadores externos seleccionables.
- Mapa de este patrón al flujo de trabajo "evaluador-optimizador" de Anthropic y los barrancos de salida de OpenAI Agents SDK.
  El modelo de evaluación de los agentes de OpenAI está siendo evaluado en el estudio de la plataforma de evaluación de los agentes de OpenAI.

## El problema es la introducción del problema

Un agente produce una respuesta que es casi correcta. Tal vez una línea de código tiene un error de sintaxis. Tal vez un resumen es demasiado largo. Tal vez un plan pierde un caso de borde. Lo que quieres es: el agente critica su propia salida, luego lo arregla.

> El agente  generó una respuesta casi correcta― tal vez una línea de código tenga un error de lenguaje― tal vez el resumen sea demasiado largo― tal vez un plan haya perdido la situación marginal― lo que quieres es: el agente  critica su propia salida, y luego la repara―

Self-Refine muestra que esto funciona con un solo modelo, sin datos de capacitación, sin RL. Pero hay una trampa: los LLM son malos en la auto-verificación sobre hechos duros. CRITIC llama la solución  ruta el paso de verificación a través de herramientas externas (búsqueda, intérprete de código, calculadora, ejecutor de pruebas).

> Auto-refinado demostró que esto se puede trabajar con un solo modelo, sin necesidad de entrenamiento datos, sin necesidad de RL. Pero hay una trampa: LLM en la realidad difícil capacidad de auto-verificación es muy pobre.

Juntos estos dos documentos definen el estándar 2026 para la mejora iterativa: generar, verificar (externamente cuando sea posible), refinar, detener cuando el verificador pasa.

> Estos dos artículos definen conjuntamente el modelo de modificación de 2026: generación, prueba, prueba externa, prueba externa, prueba de tiempo, prueba de tiempo, prueba de tiempo, prueba de tiempo, etc.

> **【中文解读】**El pensamiento central de la auto-refinación: un modelo que desempeña un papel de generador, crítico, refinador. Pero el programa de revisión de la LLM en la realidad dura es que la auto-verificación es inconfiable.

## El concepto central.

### Auto-refinado (Madaan et al., NeurIPS 2023)

Un LLM, tres funciones:

> Un LLM, tres papeles:

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

Detalle clave:`refine`El documento abla esto: el historial de caída y la calidad caen drásticamente.

> ¿ Qué es esto ?**【类比】**Auto-refinar 像写论文的"自改稿"流程:第一稿(genera)→ 通读找问题(feedback)→ 按问题改第二稿(refinar, pero para mirar el primer稿 y批注改, de lo contrario volverá a repetir el mismo error)→ 再找问题→再改──**关键**Cada vez que se refinan, se deben juntar los historial y los lotes, de lo contrario el modelo "olvida el problema de la ronda anterior", y se cae en un ciclo.

> ️ **【易错点】**常见 bug: sólo "solo" 把上一轮输出"给精炼, no 反──**后果**En el caso de los sistemas de control de datos, el sistema de control de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de**一行修复**¿Qué es esto ?`refine_prompt = task + output_0 + critique_0 + output_1 + critique_1 + ... + output_n`La historia tiene que ser transmitida.

> ¿Qué es eso?`refine`能看到完整历史所有前来的输出和批评因此不会重复错误──论文对此进行消融实验:删除历史记录后质量急剧下降──

Título: +20 mejoras absolutas promediadas en 7 tareas (matemáticas, código, acrónimo, diálogo) incluido el GPT-4.

> 核心数据: en 7 tareas (mathematics, code, enraizamiento, diálogo) el promedio de aumento absoluto de 20 puntos porcentuales, incluido GPT-4― no necesita entrenamiento― no necesita herramientas externas― un solo modelo―.

### CRITA (Gou et al., arXiv:2305.11738, v4 feb 2024)

La debilidad de Self-Refine: el paso de retroalimentación es un LLM que se califica. Para las afirmaciones factuales esto es poco fiable (una alucinación a menudo parece convincente para el modelo que la produjo).`feedback(task, output)`con`verify(task, output, tools)`donde`tools`incluye:

> La debilidad de la auto-refinación:反步骤是LLM 给自己评分── para las declaraciones de hecho esto es inestable  para los modelos de su generación suele parecer muy convincente.`verify(task, output, tools)`替代   en el`feedback(task, output)`, entre ellos `tools`Incluye:

- Un motor de búsqueda de afirmaciones de hecho.
  En inglés, "Factorial declarations" se utiliza en el buscador.
- Un intérprete de código para la corrección del código.
  En inglés, el código es usado para explicar el código.
- Una calculadora para la aritmética.
  Traducción:Para usar el calculador de la matemática.
- Verificadores específicos de dominio (probas unitarias, controles de tipo, linters).
  En inglés, el código de verificación es el código de verificación de un grupo de pruebas.

El verificador produce una crítica estructurada basada en los resultados de las herramientas.

> 验证器 generar sobre la base de la evaluación estructurada de los resultados de los instrumentos 精炼器然后根据这一批评进行条件化 

Título: CRITIC supera a Auto-Refine en tareas de hecho porque la crítica está basada en tierra.

> ¿ Qué es esto ?**【困惑】**P: 既然 CRITIC比Self-Refine 强,为什么不全部使用CritIC? A: 因为Critic depende de herramientas externas(搜索、代码解释器、单元测试) 创意写作、邮件色**事实类用 CRITIC，创造类用 Self-Refine**¿Qué es eso?

> 核心数据:Critic 超越自我精炼在事实性任务上,因为批评是有依据的──在没有外部验证器的任务上(创意写作、格式化),Critic 退化为自我精炼──

### La condición de parada

Dos formas comunes:

> 两种常见形式:

1. **Verifier passes.**Prueba externa que da resultados satisfactorios. Preferible cuando esté disponible (pruebas de unidad, comprobador de tipo, afirmación de barandillas).
   En inglés:**验证器通过。**Exterior Testing Returns Success. En el momento de su uso, el primer ensayo de la serie de pruebas de tipo de prueba.
2. **No feedback issued.**El modelo dice "la salida está bien". Más barato pero poco fiable; empareja con un límite máximo de iteración.
   En inglés:**无反馈发出。**模型说"输出没问题"──更便宜但不可靠;配合最大代次上限──

2026 por defecto: combinarlos. "Detener si el verificador pasa OR modelo dice bien Y iteraciones >= 2 OR iteraciones >= max_iterations".

> 2026 年默认做法:组合使用──"Si el verificador pasa, o el modelo dice que no hay problema y que el número de veces >= 2, o el número de veces >= maxima, entonces se detiene──"

### El valor de la inversión de la empresa se calcula en el valor de la inversión de la empresa.

En el post de Anthropic de diciembre de 2024, se menciona esto como uno de los cinco patrones de flujo de trabajo.

> Anthropic 2024 年 12 月的文章将此命名为五种工作流模式之一──两个角色:

- Evaluador: califica la producción y produce una crítica.
  La evaluación de la calidad de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y servicios de la industria de la producción de productos y de la industria de la producción de productos y de la industria de la producción de productos y de la industria de la industria de la producción de la producción de productos y de la industria de la industria de la producción de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la China.
- Optimizador: revisa la salida dada la crítica.
  Traducción:Usualizador: según la críticaModificar el resultado.

El equipo de evaluación de la información de la empresa de análisis de datos de la empresa de análisis de datos de datos de la compañía de investigación de la compañía de investigación de datos de la compañía de investigación de investigación de la compañía de investigación de datos de la compañía de investigación de investigación de la compañía de investigación de investigación de la compañía de investigación de la compañía de investigación de investigación de la compañía de investigación de la compañía de investigación de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la compañía de investigación de la marca de investigación de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca

> 循环直到评估器通过──这是Antropic 框架下的 Self-Refine/CRITIC──Antropic 添加的关键工程细节:评估器和优化器提示应该有实质性差异,以免模型只是皮图章──

### Protectores de salida de OpenAI Agents SDK

OpenAI Agents SDK envía este patrón como "gardales de salida".`OutputGuardrailTripwireTriggered`Los guardrails pueden llamar a herramientas (estilo CRITIC) o ser funciones puras (estilo Auto-Refine).

> OpenAI Agents SDK 将此模式作为"输出护"提供──护在 Agent 最终输出上运行的验证器──如果护触发(抛出`OutputGuardrailTripwireTriggered`),输出被拒绝,Agent puede volver a probar.

### 2026 trampas

- **Rubber-stamp loops.**El mismo modelo que hace generación y crítica con el mismo estilo de rapidez converge en "me parece bien". Utilice raposas estructuralmente diferentes, o un modelo más pequeño barato para la crítica.
  En inglés:**橡皮图章循环。**El mismo modelo utiliza el mismo tipo de sugerencias para generar y criticar hasta que "parezca incorrecto" o "utilice sugerencias estructurales diferentes o critique con modelos más pequeños y más económicos".
- **Over-refinement.**Cada paso de refinamiento añade latencia y tokens. Pases de presupuesto 1-3; después de eso, escala a revisión humana.
  En inglés:**过度精炼。**Cada refinamiento aumenta la demora y el token.
- **CRITIC on trivial tasks.**Si no hay un verificador externo, CRITIC se degenera a Auto-Refine; no pague la latencia por un verificador de estubes.
  En inglés:**在简单任务上使用 CRITIC。**Si no hay un verificador externo, CRITIC 退化为自精; no se retarde el precio del pago por un verificador.

## Construye y realiza.
```figure
self-refine
```

## Construye el mismo

`code/main.py`El verificador verifica el formato (3 balas, cada una de menos de 60 caras). CRITIC agrega un "verificador de hechos" externo que penaliza alucinaciones conocidas.

> `code/main.py`En una tarea de juguete para lograr el auto-refinamiento y CRITIC: dado a un determinado tema generar una lista corta.

Componentes:

> 组件:

- `generate`Producente de guión.
  En inglés:`generate`脚本生成器──
- `feedback` Autocrítica de estilo LLM.
  En inglés:`feedback`LLM 风格自我批评──
- `verify_external` Verificador basado en el estilo CRITIC.
  En inglés:`verify_external`Critic 风格 定验器──
- `refine` reescribe la salida dada historia.
  En inglés:`refine` Según el historial
- Condición de parada  pasa de verificador o max 4 iteraciones.
  China: Stop Conditions 验证器通过或最多 4 次代。

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

Comparar las carreras de Auto-Refinación vs CRITIC. CRITIC detecta un error de hecho Auto-Refinación omitida porque el verificador externo ha aterrizado el auto-crítica no lo hace.

> Comparar Auto-Refinación y CRITA 运行──CRITA  Captured Self-Refinación 遗漏 fact error, porque los verificadores externos tienen una base de auto-criticismo que no tiene ninguna 定依据──

## Usalo con el marco de ejecución

El evaluador-optimizador de Anthropic es este patrón en lenguaje amigable con Claude. Los barandillas de salida de OpenAI Agents SDK tienen forma CRITIC (los barandillas pueden llamar herramientas). LangGraph envía un nodo de reflexión que se lee como Auto-Refine. Gemini 2.5 Computer Use de Google agrega un evaluador de seguridad por paso que es una variante CRITIC: cada acción se verifica antes de comprometerse.

> Antropic evaluator-optimizer es un modelo de expresión de Claude amigo bueno. La versión de SDK de OpenAI Agents es de forma crítica.

## Envíe el producto .

`outputs/skill-refine-loop.md`Configura un bucle de evaluador-optimizador dado la forma de la tarea, la disponibilidad del verificador y el presupuesto de iteración. Emite instrucciones para el generador, evaluador/verificador y optimizador, además de una política de parada.

> `outputs/skill-refine-loop.md`De acuerdo con la forma de la tarea, la disponibilidad del verificador y el ciclo de asignación de presupuesto del evaluador-optimizador, los consejos de los resultados del evaluador/verificador y del optimizador, así como las estrategias de detención.

## Los ejercicios.

1. Ejecutar el juguete con max_iterations=1. ¿Critic todavía ayuda?
   中文翻译:用 max_iterations=1 运行――CRITIC  todavía hay ayuda?
2. Replace el verificador externo por uno ruidoso (políticos falsos al azar del 30%). ¿Qué hace el bucle? Esta es la realidad de 2026 de la mayoría de las pilas de barandillas.
   La mayoría de los usuarios de la versión de 2026 tienen que hacer esto.
3. Implementar una variante de "crítica del generador en diferentes modelos": generaciones de modelos grandes, críticas de modelos pequeños. ¿Vale más que el mismo modelo?
   Traducción: "¿Es mejor que el modelo?"
4. Lea la sección 3 de CRITIC (arXiv:2305.11738 v4). Nombre las tres categorías de herramientas de verificación y dé un ejemplo para cada una.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
5. Mapa de los agentes OpenAI SDK `output_guardrails`¿Qué es lo que el SDK se equivoca y qué es lo que se correcta?
   La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de .`output_guardrails`¿Dónde está el buen trabajo, dónde no?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## Más Leer más Leer más

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) el papel canónico
  En el libro de la obra, el autor se encuentra en el lugar de la obra.
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) Verificación basada en herramientas
  En inglés, "Critic" significa "critic".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) Modelo de flujo de trabajo de evaluador-optimizador
  En inglés, el método de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de evaluación de los agentes de evaluación de los agentes de trabajo de los agentes de evaluación de los agentes de evaluación de la calidad de los agentes de trabajo de los agentes de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) barandillas de salida como verificadores en forma de CRITIC
  En inglés, el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de
