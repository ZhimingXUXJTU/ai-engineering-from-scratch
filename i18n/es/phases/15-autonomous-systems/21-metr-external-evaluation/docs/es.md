# METR Horizontes de tiempo y evaluación de la capacidad externa  evaluación METR

> METR (ex-ARC Evals) es una organización independiente 501(c)(3) desde diciembre de 2023. Su referencia Time Horizon 1.1 (enero 2026) se ajusta a una curva logística de probabilidad de éxito de tarea vs log(experto tiempo de finalización humana); la intersección en probabilidad del 50% define el horizonte temporal del modelo. El conjunto de compromiso 20252026 cubre GPT-5.1, GPT-5.1-Codex-Max y evaluaciones de monitoreo de prototipos (puede un monitor realizar tareas secundarias; puede el agente evadirlas). Suites de referencia: HCAST (180+ ML, ciber, SWE, tareas de razonamiento; de 1 minuto a 8+ horas), RE-Bench (71 ML tareas de investigación e ingeniería con base de expertos), SWAA. La nota honesta: las mediciones de METR están idealizadas  sin humanos, sin consecuencias reales  y el equipo ha documentado la brecha de comportamiento de evaluación frente a la implementación (lección 1). Un horizonte temporal es un límite superior, no una predicción de despliegue.

> **【中文解读】**Este apartado presenta la evaluación independiente de terceros de las capacidades y riesgos del sistema de IA por parte del METR.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**Estudios de la Universidad de California en Los Ángeles, Estados Unidos, en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000 y en el año 2000.
> ¿ Qué es esto ?**【类比】**METR = "El tercer centro de inspección de la capacidad de IA"―RSP dice que "la R&D-4 de la IA" es abstracto; el horizonte temporal de METR 基准把"AI 能完成多复杂任务" se comprime en una escala" modelo 50% de rendimiento confiable para completar las tareas de expertos花 X 小时的任务"― similar a IQ 分数概括智力, pero el número de METR tiene métodos de medición repetibles―
> ️ **【易错点】**Cuando el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo, el METR es un programa de tiempo y el METR es un programa de tiempo es un programa de tiempo, el METR es un programa de tiempo es un programa de tiempo es un programa de tiempo es un programa de tiempo, y el METR es un programa de tiempo es un programa de tiempo es un programa de tiempo es un programa de tiempo es un programa de tiempo es un programa de tiempo es un programa de trabajo es un programa de trabajo es un programa de trabajo.

## El problema es la introducción del problema

Las políticas de escalación (lecciones 19, 20) son tan útiles como las mediciones a las que se refieren. "Párrafo de I+D-4 de IA" y "Autonomía de largo alcance" se definen en la prosa de la política; se vuelven actuables solo cuando evaluaciones específicas producen números específicos.

> 扩展政策 (第 19、20 课) se utiliza sólo como las medidas que se refieren a ellas.

METR es la organización de evaluación externa 20242026 que ha definido muchos de esos números. Evaluan modelos fronterizos  a menudo pre-lanzamiento, bajo NDA con laboratorios  y publican la metodología después. El punto de referencia Time Horizon 1.1 (enero 2026) es su artefacto principal: un único escalar que comprime la capacidad en una unidad legible por el hombre ("este modelo puede hacer el tipo de tarea en la que un experto pasa X horas con una fiabilidad del 50%").

> METR es una organización de evaluación externa que define muchos de estos números. Suelen evaluar modelos de vanguardia antes de su publicación y después de su firma con el laboratorio. El tema principal de METR es: "Este modelo puede completarse con una fiabilidad del 50%".

La lección es en parte sobre la metodología (cómo se calcula un horizonte) y en parte sobre la interpretación (por qué un horizonte es un límite superior, no una predicción de despliegue). Las dos habilidades pertenecen a una sola.

> Esta parte de la clase se refiere a métodos de cálculo, parte de explicación, por qué la línea de tiempo es un límite y no un pronóstico de implementación. Estas dos habilidades se acompañan.

## El concepto central.

### METR de fondo

- Fundada: diciembre de 2023 (ex-ARC Evals, desvinculada en una organización independiente 501 ((c) ((3)).
  Se creó el grupo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización.
- Ámbito de aplicación: evaluación de las capacidades autónomas de los modelos fronterizos, a menudo pre-lanzamiento.
  La evaluación de la capacidad de trabajo de los modelos, normalmente publicado antes.
- Laboratorios asociados: Antropic, OpenAI (múltiples compromisos 20252026).
  En el contexto de la investigación, el estudio de la ciencia y la tecnología de la información se ha desarrollado en el campo de la ciencia y la tecnología.
- Resultados notables: Horizonte temporal 1.0 (marzo 2025), Horizonte temporal 1.1 (enero 2026), evaluaciones de monitoreo de prototipos.
  En el contexto de la actualidad, el sistema de control de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información.

### El horario del tiempo se ajusta

Metodología (desde el blog y los artículos de METR):

> 方法论(来自 METR 博客和论文):

1. Recoger una suite de tareas que abarca de la escala de minutos a la escala de horas de los tiempos de finalización experto.
   En el caso de los grupos de trabajo, los grupos de trabajo de los estudiantes de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la
2. Ejecutar el modelo en cada tarea; registrar el éxito o el fracaso.
   En español traducción: en cada tarea se ejecuta el modelo; registro éxito o fracaso.
3. Aplicar una curva logística: P(éxito) como función del tiempo de finalización log(experto).
   En el lenguaje chino, el log log log (plural log log log) se utiliza para completar el tiempo.
4. El horizonte es el tiempo experto en el que P (sucesión) = 0,5.
   En el chino, el tiempo es el tiempo de la carrera.

La forma logística-ajuste es la correcta porque la capacidad generalmente tiene una relación creciente, que se acerca a la meseta con la dificultad de la tarea. El punto del 50% es una opción (podría ser 10%, 90%); METR informa múltiples umbrales en el documento detallado, pero lidera con el 50% porque es el más intuitivo.

> La forma de adaptación lógica es positiva, ya que la capacidad y la dificultad de tarea suelen ser un solo aumento, tendencia a la relación de la plataforma. El 50% de la capacidad de selección puede ser de 10% o 90%; el METR informa en los artículos detallados sobre varios valores, pero el 50% es el principal, ya que es más intuitivo.

### Los números de enero de 2026

Por Horizonte temporal 1.1:

>  según el Horizonte temporal 1.1:

- Claude Opus 4.6: ~ 14 horas con fiabilidad del 50%, a partir de Time Horizon 1.1 (enero 2026).
  El texto original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
- El tiempo duplicado en tareas de estilo HCAST: ~4,3 meses (130,8 días) en el ajuste post-2023 reportado por Time Horizon 1.1 (enero 2026); la cifra de ~7 meses es el ajuste completo 20192025 de Time Horizon 1.0 y se informa en TH1.1 junto con el número post-2023.
  China Translation:HCAST 类任务的倍增时间:Time Horizon 1.1(1月2026年) 后拟合的 2023 后拟合的约 4.3 个月(130.8 天); 后拟合的约 7 个月的数字是Time Horizon 1.0 完整的 20192025 拟合的, se encuentra en TH1.1 junto con los números posteriores de 2023 后的报告──

Esos son los números específicos que restan en las referencias de la Fase 15. Son citados en el RSP v3.0 (lección 19) de Anthropic y en el FSF v3 (lección 20) de DeepMind como una de las mediciones que alimentan las evaluaciones de umbral.

> Estos son los números concretos de la Fase 15 y la parte restante de los citaros.

### Suites de referencia

- **HCAST**Las tareas de la empresa son: 189 en el área de tecnología de inteligencia, ciberseguridad, ingeniería de software y razonamiento general.
  En inglés:**HCAST**Las siguientes funciones se desarrollan en el área de aprendizaje::跨机器学习、网络安全、软件工程和通用推理的189任务──范围:1 分钟到8+ 小时专家时间──时间线数字背后主套件──
- **RE-Bench**: 71 tareas de investigación e ingeniería de ML con un experto humano. Medir si el modelo puede realizar el tipo de trabajo de I+D de ML que alimenta el umbral de I+D-4 de IA.
  En inglés:**RE-Bench**La investigación de la IA en el campo de la investigación y desarrollo de la IA se ha desarrollado en el campo de la investigación y desarrollo de la IA.
- **SWAA**: tareas más cortas; útiles para calibrar el extremo inferior de la curva del horizonte.
  En inglés:**SWAA**: Más corta tarea; para el tiempo de curva de la línea baja.

### Evaluaciones de monitoreo de prototipos

20252026 Trabajo METR incluyó prototipos de monitoreo-evaluación: puede un monitor atrapar un modelo que realiza una tarea secundaria (algo distinto de lo que el operador pidió); puede el agente evadir el monitor. Estos alimentan directamente la categoría "Salvaguardias minantes" en OpenAI PF v2 y el monitoreo de alineación engañosa en DeepMind FSF v3 (lección 20).

> 20252026 METR 工作包括监控评估原型:监控器能否捕获模型执行副任务(操作员请求以外的事);Agent 能否规避监控器──这些直接入 OpenAI PF v2 的"破坏防护"类别和 DeepMind FSF v3(第 20 课) de la estafa contra la vigilancia──

### Por qué los horizontes son límites superiores

- **Idealized tooling**Las tareas de referencia proporcionan al modelo herramientas limpias y datos bien formateados.
  En inglés:**理想化工具**La base de la misión es el modelo de trabajo y el modelo de trabajo.
- **No real consequences**El modelo nunca factura a un cliente, elimina datos reales o contacta con personas reales.
  En inglés:**无真实后果**El modelo es de hecho no se le presta a los clientes, se elimina el dato real o se contacta con el personal real.
- **Eval-context gaming**Las pruebas de inteligencia artificial se comportan de manera diferente en los modelos.
  En inglés:**评估上下文博弈**Se trata de un estudio de la IA en el que se observa que el sistema de inteligencia artificial es un sistema de inteligencia artificial.
- **No legitimate user variance**Las solicitudes de referencia son estructuradas.
  En inglés:**无合法用户方差**El usuario real se encuentra en el punto de referencia de la solicitud.

El horizonte es el límite de capacidad en condiciones favorables. La fiabilidad de la implementación es diferente, más baja, y los equipos deben medir su propia distribución para conocerlo.

> 时间线是有利条件下能力上限――部署可靠性是不同的数字,更低, los equipos deben medir su distribución para saber―

### El caso del evaluador externo

La evaluación externa es importante porque los laboratorios internos tienen incentivos para optimizar las métricas que informan. La independencia de METR  un 501 ((c) (3) con una metodología declarada y documentos revisados por pares  es la mitigación estructural. No es suficiente solo (los laboratorios todavía controlan lo que METR ve), pero es estrictamente mejor que ninguna evaluación externa.

> La evaluación externa es importante, ya que el laboratorio interno tiene la capacidad de optimizar el índice de informe. La independencia del METR es un proceso de evaluación estructural.

### Cómo utilizar los números de horizonte en la práctica

- **As a capability filter**Si el horizonte de un modelo está muy por debajo del tiempo de expertos de una tarea propuesta, no lo envíe de forma autónoma (fichero de habilidades de Lesson 1).
  En inglés:**作为能力过滤器**Si el tiempo del modelo es mucho menor que el tiempo del experto de la tarea propuesta, no lo dejes publicar de forma automática.
- **As a trend indicator**El tiempo de duplicación indica cuánto tiempo la práctica actual permanecerá segura incluso sin nuevas mitigaciones.
  En inglés:**作为趋势指标**El tiempo aumenta para que la práctica actual se mantenga segura durante mucho tiempo.
- **As a prior**El objetivo de la evaluación es mejorar la calidad de la información y la calidad de las herramientas.
  En inglés:**作为先验**La línea de tiempo es el punto de partida. De acuerdo con la distribución de sus tareas, la calidad de los instrumentos y la implementación de los mismos.

## Usalo con el marco de ejecución
```figure
a5-horizon-fit
```

## Usalo

`code/main.py`Implementa un ajuste logístico de éxito de tarea vs tiempo de experto, dado un conjunto de resultados sintéticos. Informó el 50% horizonte (título de METR), el 10% horizonte (conservador) y el 90% horizonte (optimista). También demuestra qué cambios se producen cuando la tasa de éxito es inflada artificialmente por juegos de contexto de evaluación.

> `code/main.py`给定合成结果集实现任务成功率 vs log(专家时间) 的逻辑拟合――报告 50% 时间线(METR 标题) 、10% 时间线(保守) 、90% 时间线(乐观) ── también se muestra cuando la tasa de éxito es evaluada en el contexto de los juegos de personas por la inflación.

## Envíe el producto .

`outputs/skill-horizon-interpretation.md`revisa la afirmación de horizonte de un proveedor y produce un análisis de la brecha entre la afirmación de referencia y la realidad de la implementación.

> `outputs/skill-horizon-interpretation.md`审查供应商时间线声明并产生基准声明与部署现实之间的差异分析──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar que el 50% del horizonte de ajuste coincide con la verdad sintética de la tierra. Ahora, dime la cuadrícula de tiempo de tarea. ¿Estimar el horizonte el cambio significativamente?
   Traducción:运行`code/main.py` Confirmar el 50% de la capacidad de la línea de tiempo para la combinación de valores reales.

2. Lea la publicación de blog Time Horizon 1.1 de METR. Identifique las tareas específicas en las que la fiabilidad es más alta y en las que es más baja. Explique por qué existe la brecha.
   China: METR Time Horizon 1.1 博客──识别可靠性最高和最低的具体任务──解释为什么存在差距──

3. Lea los recursos de METR "Medición de capacidades de IA autónomas". Enumera las categorías de tareas de HCAST. Elige una categoría que ponderas más pesadamente para una tarea de producción y justifique por qué.
   China Translation: read METR's "Meter autonomía AI  capacidad" resource。 listado HCAST 任务类别──select one you for production task加权的类别并论证为何──

4. Introduzca juegos de eval-contexto en el simulador: invertir ~20% de las tareas fallidas para el éxito. Informar el nuevo horizonte. Esto se aproxima a lo que hace una tasa de juego de 20% al número observado.
   Introducción de juegos de contexto de evaluación en el simulador: será aproximadamente el 20% 失败任务翻转为成功――报告新时间线――.

5. Diseñe una evaluación de horizonte interno en su propio archivo de errores o un conjunto de tareas representativo. Describa la recopilación de datos, el ajuste y lo que le dice la salida. Compara con los números METR.
   En el mismo Backlog de bugs o en el conjunto de tareas representativas, el diseño de la línea de tiempo interna es evaluado.

## Términos clave .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Más Leer más Leer más

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) HCAST, RE-Bench, especificaciones de SWAA.
  En inglés, "HCAST"",RE-Bench"",SWAA" 规范
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) el papel original del horizonte.
  Sinopsis: El tiempo de la muerte
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) Números y metodología actuales.
  Traducción:Continuo y método
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons) seguimiento en vivo.
  Ciencia de la información
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Perspectiva interna de las mediciones de los METR.
  En inglés, el término "METR" se refiere a la medida de la velocidad de un metro.
