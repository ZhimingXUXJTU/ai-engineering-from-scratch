# Los puntos de referencia: SWE-bench, GAIA, agenteBench.

> Tres puntos de referencia de evaluación de agentes anclaje en 2026. SWE-bench prueba el parcheado de código. GAIA prueba el uso de herramientas generalistas. AgentBench prueba el razonamiento multi-ambiente. Conozca su composición, su historia de contaminación y lo que no miden.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Nombre del arnés de prueba del banco SWE (FAIL_TO_PASS) y explica por qué se bloquea en las pruebas de unidad.
- Explica por qué existe el SWE-bench Verified (OpenAI, 500 tareas) y qué elimina.
- Describa el diseño de GAIA: simple para los humanos, difícil para la IA; tres niveles de dificultad.
- Nombre los ocho entornos de AgentBench y su bloqueador principal para LLM de código abierto.
- Resumen de la conclusión de contaminación del banco SWE+ y sus implicaciones.

## El problema es la introducción del problema

Las tablas de clasificación le dicen qué modelo gana en un punto de referencia.

> 排名 te dice cuál modelo gana en un determinado nivel.

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

- Si el indicador de referencia está contaminado (soluciones en los datos de formación, fuga de pruebas).
- Si el índice de referencia mide lo que le importa (código vs navegación vs generalista).
- Si el evaluador es robusto (combinación de AST, controles de estado, revisión por humanos).


> **【中文解读】**SWE-bench y GAIA son dos de los principales agentes de 2026  capacidad基准。SWE-bench  evaluación de los agentes  capacidad de reparar el verdadero problema de GitHub 软件工程)。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题能力──通用推理── ambas han definido conjuntamente las fronteras de capacidad del agente。

> **{【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】}**SWE-bench (Princeton, 2023) incluye 2,294 个真实 GitHub issue,Agent 必须在真实代码库中定位 bug、编写修复并通过测试──2026年 SOTA 是 72% 解决率(OpenAI's Codex)──GAIA (Meta, 2023) 的 466 个问题需要网页 搜索、文件处理、代码执行等工具──人类平均 92% ,最佳代理约70%──
Conozca los tres puntos de referencia de anclaje y sus modos de falla antes de citar un número.

> Antes de citar los datos, primero comprenda estos tres test básicos y su modelo de fracaso.

> ¿ Qué es esto ?**【前置】**建议先过:Fase 14·06 工具使用) 理解代理 如何调用工具是看懂 GAIA的前提;以及基本的"机器学习评估方法论"精度/回忆"",污染"",数据污染") 测试集泄漏──如果你引用过模型基准,但不知道污染是什么,本节必须学──

## El concepto central.

### En el caso de los productos de la industria de la industria de la industria, el valor de la producción de productos de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la del del sur.

- 2.294 problemas reales de GitHub de 12 repositorios populares de Python.
- El agente obtiene: la base de código en el prefijo de compromiso + descripción del problema en lenguaje natural.
- El agente produce un parche.
- Evaluación: aplicar parche, ejecutar la suite de pruebas del repo. El parche debe cambiar las pruebas FAIL_TO_PASS (anteriormente fallido, ahora pasando) sin romper las pruebas PASS_TO_PASS.

SWE-agent (Yang et al., 2024) alcanzó el 12,5% en la liberación haciendo hincapié en las interfaces agente-computador (comando de editor de archivos, sintaxis de búsqueda que el modelo entiende).

> ¿ Qué es esto ?**【类比】**SWE-bench 像考"开卷实操": darle al agente una verdadera código biblioteca(开卷) 、 un problema 描述(考题) 、一套现有单元测试(评分标准) ✿ Agente 像人类工程师一样读代码定位 bug、写补丁、跑测──**关键设计**:测试用 FAIL_TO_PASS(修复前失败、修复后通过) + PASS_TO_PASS(no puede destruir ya ha funcionado), ¡De hecho!

> SWE-agent ((Yang等,2024) alcanzó el 12,5% en el tiempo de publicación, mediante el enfatización de la interfaz de los agentes-computadores ((文件编辑器命令、模型能理解的搜索语法) ]]

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

### En el caso de los bancos de SWE, el valor de la banca de SWE se verificó.

OpenAI, agosto 2024. Subconjunto de 500 tareas curado por humanos. Elimina problemas ambiguos, pruebas poco fiables y tareas donde la solución no estaba clara.

> OpenAI, agosto de 2024 ⋅ 500 个任务子集 of artificial策划 ⋅ Remove a blur issue ⋅ unreliable test and repair unknown task ⋅ "¿Puede tu agente entregar verdaderos correctos?"

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

### Contaminación

- Más del 94% de los problemas de la banca SWE preceden a la mayoría de los recortes de modelos.
- **SWE-bench+**El 32,67% de los parches exitosos encontraron soluciones filtradas en el texto de la cuestión (el modelo vio la corrección en la descripción), y el 31,08% fueron sospechosos debido a la escasa cobertura de las pruebas.
- Verificado es más limpio pero no libre de contaminación.

Implicación práctica: un modelo que obtiene un 50% en el banco SWE puede obtener un 35% en el banco SWE. Siempre informe ambos si reclama un rendimiento en el banco SWE.

> ️ **【易错点】**引用 SWE-bench 分数时不提 Verificado/SWE-bench+。**后果**El 50% de los casos de la mayoría de los casos, es posible que el 32% de los casos de la mayoría de los casos, en el caso de la mayoría de los casos, sean de la mayoría de los casos.**一行修复**: cualquier cita SWE-bench números, debe dar simultáneamente Verified 子集分数和 SWE-bench+(去污染版) 分数,注明数据来源日期。

>  Efecto real: un modelo en SWE-bench arriba de un 50% de puntaje en SWE-bench + arriba sólo puede obtener un 35%── si usted afirma SWE-bench  rendimiento, por favor, debe informar simultáneamente ambos──

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

### La Comisión no puede adoptar medidas en el sentido de que el Estado miembro no pueda adoptar medidas en virtud del artículo 107, apartado 1, del Reglamento (UE) n.o 1095/2012.

- 466 preguntas; 300 retenidas para el ranking privado en huggingface.co/gaia-benchmark.
- Filosofía del diseño: "conceptualmente simple para los humanos (92%) pero difícil para la IA (GPT-4 con plugins: 15%)."
- Pruebas de razonamiento, multi-modalidad, web, uso de herramientas.
- Tres niveles de dificultad; el nivel 3 requiere largas cadenas de herramientas en todas las modalidades.

GAIA es lo que se ejecuta para medir la "capacidad generalista". No se confunda con los puntos de referencia específicos del código.

> La GAIA es una medida de la base de "capacidad general".

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

### El artículo 6 del Reglamento (UE) n.o 1095/2013 se aplica a las medidas de seguridad y seguridad de los trabajadores.

- 8 entornos en todo el código (Bash, DB, KG), juegos (Alfworld, LTP), web (WebShop, Mind2Web) y generación abierta.
- Múltiples giros, ~ 4K-13K giros por división.
- El razonamiento a largo plazo, la toma de decisiones y la instrucción a continuación son los obstáculos para que los LLM OSS alcancen a los comerciales.

### Lo que estos no miden

- Costo operativo real (tokens, reloj de pared).
- Comportamiento de seguridad en condiciones adversas.
- El rendimiento en su dominio (utilice sus propias evaluaciones, lección 30).
- Las fallas de cola (medio de puntos de referencia; los operadores de producción se preocupan por el peor 1%).

### Cuando el benchmarking sale mal

- **Single-number fixation.**El 50% del banco SWE le dice menos que el costo de P50/P75/P95 + distribución de pasos.
- **Contaminated claims.**La información sobre el banco SWE sin mencionar el banco Verified o el banco SWE+ es engañosa.
- **Benchmark-as-development-target.**La optimización para el índice de referencia difiere de la utilidad de producción.

> ¿ Qué es esto ?**【困惑】**P: SWE-bench Verified 上 70% + de los modelos han salido, ¿es decir que los ingenieros de software deben estar en el trabajo? A: 还早──三个原因:(1) El problema de SWE-bench es un problema bien formado de "hay un uso de prueba claro、 hay una clara redirección de camino", el problema del 50% en la producción no se satisface;(2) el 70% significa que cada 3 tareas fracasan 1 个, el costo de la reparación de un entorno de producción fracasa es mucho mayor que el beneficio de la reparación exitosa;(3)**生产代码库比 SWE-bench 的 12 个开源 Python 仓库复杂得多**私有代码、跨语言、几十年遗留代码──Benzmark superior del 70% no es igual al 70% del entorno de producción──

> **单一数字执念。**SWE-bench 50%  Diga tu información es menor que P50/P75/P95 成本 + 步骤分布──
> **污染声明。**报告 SWE-bench 时不提及 Verificado o SWE-bench+ es un error de dirección.
> **基准作为开发目标。**Para la base de la optimización se desvían de la producción práctica.

## Construye y realiza.
```figure
ae-swebench-gate
```

## Construye el mismo

`code/main.py`se aplica un arnés de juego SWE-bench:

> `code/main.py` Realizar un instrumento de prueba de juguetes similar a un banco SWE:

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

- Tarea de solución de errores sintéticos (3 tareas).
- Un "agente" con guión que propone parches.
- Un ejecutor de prueba que comprueba FAIL_TO_PASS (bug ahora fijado) y PASS_TO_PASS (nada roto).
- Un clasificador de dificultad de estilo GAIA basado en la profundidad de la descomposición de la pregunta.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La salida muestra la tasa de resolución por tarea + por dificultad y hace concretas las reglas del evaluador.

> 输出 muestra la tasa de resolución de cada tarea y cada nivel de dificultad, y hace concretar las reglas del evaluador.

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

## Usalo con el marco de ejecución

- **SWE-bench Verified**Siempre reportar las puntuaciones verificadas.
- **GAIA**Para los agentes generalistas, usa la división de la tabla de clasificación privada.
- **AgentBench**para la comparación entre múltiples entornos.
- **Custom evals**(Lección 30) para la forma real de su producto.

## Envíe el producto .

`outputs/skill-benchmark-harness.md`construye un arnés de estilo SWE-bench para cualquier par de tareas de base de código con puertas FAIL_TO_PASS / PASS_TO_PASS.

> `outputs/skill-benchmark-harness.md`Para cualquier código de la biblioteca de tareas para construir una SWE-banch 风格的测试工具, con un fallo_TO_PASS / PASS_TO_PASS 门控──

> SWE-bench y GAIA es el dos núcleos básicos de la capacidad de agente. SWE-bench evalúa la capacidad de modificación de código, GAIA evalúa la capacidad de pensamiento general.

## Los ejercicios.

1. Portar el arnés de juguete para que se ejecute en un repo real (escolle uno de los suyos). Escriba 3 pruebas FAIL_TO_PASS para detectar errores conocidos.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir una métrica de recuento de pasos. ¿Cuántos pasos de agente por resolución?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Lea el documento SWE-bench+. Implemente una verificación de fuga de solución (paraleje de patrón del texto de la cuestión con la diferencia).
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Descarga una pregunta de GAIA de la división pública, rastrea lo que un agente de clase GPT-4 haría. ¿Qué herramientas necesita?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Lea la descripción de medio ambiente del agente Bench. ¿Qué medio ambiente refleja la superficie de su producto?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| SWE-bench | "Code agent benchmark" | 2,294 GitHub issues; patch must flip FAIL_TO_PASS tests |  |
| SWE-bench Verified | "Clean SWE-bench" | 500 human-curated tasks, OpenAI |  |
| FAIL_TO_PASS | "Fix gate" | Tests previously failing that must pass after the patch |  |
| PASS_TO_PASS | "No-regression gate" | Tests that were passing and must still pass |  |
| GAIA | "Generalist benchmark" | 466 human-easy / AI-hard multi-tool questions |  |
| AgentBench | "Multi-env benchmark" | 8 environments; long-horizon multi-turn |  |
| Contamination | "Training-set leak" | Benchmark tasks present in model training |  |
| SWE-bench+ | "Contamination audit" | 32.67% solution leakage found in successful SWE-bench patches |  |

## Más Leer más Leer más

- [Jimenez et al., SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) el índice de referencia original
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) el subconjunto seleccionado
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Mialon et al., GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) Referencia generalista
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Liu et al., AgentBench (arXiv:2308.03688)](https://arxiv.org/abs/2308.03688) Suite multiambiental
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
