# El agente de codificación autónoma paisaje (2026)

> El banco SWE-Verified pasó del 4% al 80,9% en menos de tres años. El mismo Claude Sonnet 4.5 obtuvo un puntaje del 43,2% en SWE-agent v1 y el 59,8% en Cline autonomo  el andamio alrededor del modelo ahora importa tanto como el propio modelo. OpenHands (anteriormente OpenDevin) es la plataforma más activa con licencia MIT y su bucle CodeAct ejecuta acciones Python directamente en una caja de arena en lugar de llamadas de herramientas JSON. Los números de encabezado ocultan un problema metodológico: 161 de las 500 tareas verificadas de SWE-bench requieren solo un cambio de línea de 12, y SWE-bench Pro (10 tareas de línea superior) se sitúa en 2359% para los mismos modelos fronterizos.

> **【中文解读】**SWE-bench Verified en no menos de tres años de 4% a 80.9%♦ El mismo Claude Sonnet 4.5 en SWE-agent v1 alcanzó el 43.2%, en Cline autónomo alcanzó el 59.8% El modelo alrededor de la escritura ahora y el modelo en sí mismo es tan importante♦ OpenHands(previous OpenDevin) es la plataforma de licencia MIT más activa, su ciclo de CodeAct ejecuta directamente en la caja Python 动作而不是 JSON 工具调调用♦ Los temas de la cuestión de los métodos ocultos digitales: 500 个 SWE-bench Verified 任务中 161 个只需要1-2 行变更,SWE-bench Pro(10+ 行任务) El modelo anterior solo es 23-59%♦

> **【拓展：脚手架 > 模型】**La curva de 2022-2026 muestra que el aumento de la capacidad del agente de codificación tiene tres fuentes complejas: mejor modelo básico, mejor guión de la estructura (CodeAct, reflexión, verificación)  mejor guión de la estructura (Verified, elimination of noise)  Un modelo similar en diferentes guiones de la estructura de la estructura de 16.6 puntos de diferencia.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

> ¿ Qué es esto ?**【前置】**學本節前请先掌握:Fase 14·07(工具调用) 、Fase 14·30+(工作台 Agente 实践) 、Fase 15·01(长程 Agent) ⋅本节是 2026 年编码 Agent 全景图选型必读──
> ¿ Qué es esto ?**【类比】**选编码 Agent = "选车" en lugar de "选发动机"。 identico发动机(Claude Sonnet 4.5) installado en diferentes vehículos(SWE-agent vs Cline) velocidad de diferencia 16 个百分点──脚手架(检索层、规划器、沙箱、编辑-verify 循环) sólo es producto, el modelo es sólo un componente── así que no sólo mire la clasificación de modelos, para ver "My task+my脚手架" de extremo a extremo de fiabilidad──
> ️ **【易错点】**Mira SWE-bench Verificado 分数选 Agent = 被基准骗了──500 个任务里 161 个只需1-2 行修改(容易), Mira SWE-bench Pro(10+ 行真实任务) 分数才有参考价值──修复:选 Agent 前用自己代码库的真实问题 测试,而不是看营销基准──

## El problema es la introducción del problema

> **【中文解读】**编码代理景观 es uno de los campos de aplicación de IA más rápidos de 2025-2026 años. Los principales jugadores incluyen Claude Code, Cursor, GitHub Copilot, Devine, Windsurf, etc.

> **【拓展：coding agent landscape】**2026年编码 代理的竞争格局:(1) Claude CodeAnthropic's Autonomous Coding Agent,支持全开发、Git 操作和终端命令执行;(2) Cursor基于 VS Code的 AI编辑器,强调人机协作;(3) DevinCognition AI's Full Autonomous Coding Agent,可以独立完成开发任务;(4) Windsurf(原 Codeium) AI 优先 IDE──SWE-bench 上的表现是主要竞争指标;;

La pregunta correcta es: en una distribución de tareas que coincida con mi trabajo, con el andamio que voy a ejecutar en producción, ¿qué fiabilidad de extremo a extremo obtengo?

> La pregunta correcta es: en la distribución de tareas que coincide con mi trabajo, con el uso de la escritura que voy a usar en la producción, ¿qué puedo obtener de fiabilidad de extremo a extremo?

Entre 2022 y 2026, el campo aprendió que el andamio  la capa de recuperación, el planificador, la caja de arena, el bucle de edición-verificación, el formato de retroalimentación  es cargador. Claude Sonnet 4.5 en SWE-agent v1 obtuvo un puntaje del 43,2% en SWE-bench Verified; el mismo modelo dentro del andamio autónomo de Cline obtuvo un puntaje del 59,8%. 16.6 puntos de diferencia absolutos, mismos pesos. El modelo base es un componente; el bucle es el producto.

> Entre 2022 y 2026, el sector de la enseñanza de la escritura ha obtenido un 43,2% en el SWE-agent v1 y un 59,8% en el Cline Autónomo de la escritura.

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

El problema de acompañamiento es que la saturación de referencia oculta regresiones.

> El problema con el que se acompaña es el regreso de los fundamentos y la ocultación.

SWE-bench Verified está cerca de saturado, y la cola de tareas fáciles (161 de 500 tareas que requieren ≤ 2 líneas) aumenta las puntuaciones superiores. La calidad del mundo real se mide mejor en distribuciones como SWE-bench Pro (10+ cambios de línea), donde los mismos líderes todavía se sientan en 2359%.

> SWE-bench Verificado 接近和,简单任务尾部(500 个任务中 161 个需要 ≤2 行) 拉高顶级分数──现实世界质量在 SWE-bench Pro(10+ 行变更)等分布上测量更好,同领先者仍只有23-59%──

## El concepto central.

### SWE-bench, un párrafo SWE-bench un párrafo

SWE-bench (Jimenez et al.) toma problemas reales de GitHub con parches de verdad en el suelo y pide a un agente que produzca un parche que haga pasar la suite de pruebas. SWE-bench Verified (OpenAI, 2024) es un subconjunto de 500 tareas curado por el hombre con las tareas ambigüas y rotas eliminadas. SWE-bench Pro es el sucesor más difícil de las tareas que requieren 10+ líneas de cambio, donde los agentes fronterizos actuales se sientan en 2359%.

> SWE-bench(Jimenez 等人) 带真实补丁的真实 GitHub issue, requisit Agent 产生使测试套件通过补丁──SWE-bench Verified(OpenAI,2024) es el 500 任务子集 de la planificación artificial, eliminar las tareas模糊和损坏的──SWE-bench Pro 是更难的继任者需要10+ 行变变任务,当前前沿 Agent 在 23-59%──

### Lo que la curva 2022 → 2026 realmente muestra.

- **2022**En el caso de los modelos de investigación, el valor de la producción de los modelos de investigación es de ~4% en el banco de SWE en bruto.
  En inglés:**2022**El estudio de la investigación de la SWE-bench original fue de aproximadamente un 4%
- **2024**: GPT-4 + andamios de estilo Devin en ~14%; agente SWE en ~12%.
  En inglés:**2024**:GPT-4 + Devin 式脚手架约14%;SWE-agent 约12%──
- **2025**: Claude 3.5/3.7 Sonet dentro de Aider y agente SWE empujar en el rango de 4055%.
  En inglés:**2025**Claude 3.5/3.7 Sonnet en Aider y SWE-agent dentro de 40-55% 范围
- **2026**Claude Sonnet 4.5 y competidores fronterizos en 7080%+ en el banco SWE-Verified.
  En inglés:**2026**:Claude Sonnet 4.5 和前沿竞争者在SWE-bench Verified 上 70-80%+──Epoch AI 的排名实时跟踪──

La pendiente proviene de tres fuentes de composición: mejores modelos base, mejores andamios (CodeAct, reflexión, bucles verificadores) y mejores puntos de referencia (eliminación de ruido verificado).

> 斜率 proviene de tres fuentes complejas: mejor base modelo, mejor guión, mejor código, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor base de datos, mejor información y mejor información sobre la información.

### CodeAct vs JSON herramienta llamadas .

OpenHands (All-Hands-AI, arXiv:2407.16741, anteriormente OpenDevin) tomó una apuesta arquitectónica específica: en lugar de que el modelo emita llamadas de herramienta JSON que un host decodifica y ejecuta, el modelo emite código Python y un kernel de estilo Jupyter lo ejecuta en una caja de arena.

> OpenHands(All-Hands-AI,arXiv:2407.16741,前 OpenDevin) bajo una estructura específica: el modelo no se emite más por el host de código de resolución ejecutado JSON 工具调用, sino por Python 代码, ejecutado por Jupyter 风格内核在沙箱中运行──Agent puede en un movimiento en un ciclo de documentos、链式工具、 capturar sus propias anomalías──

El acuerdo de cambio:

> 权衡:

- **JSON tool calls**: cada acción es una vez; fácil de auditar; composicionalidad limitada; seguro por defecto porque cada llamada pasa por un validador explícito.
  En inglés:**JSON 工具调用**El proceso de evaluación de la seguridad de los datos de los datos de los usuarios es un proceso de evaluación de los datos de los usuarios.
- **CodeAct**: una acción puede ser un programa completo; composición; requiere una caja de arena endurecida (OpenHands utiliza aislamiento Docker); los modos de falla incluyen cualquier cosa que el tiempo de ejecución de la caja de arena permita.
  En inglés:**CodeAct**Un movimiento puede ser todo el proceso; puede ser combinado; necesita fijarse en la caja; puede ser un proceso de separación; puede ser un proceso de separación.

Ambas arquitecturas están en producción. CodeAct es dominante en plataformas abiertas (OpenHands, smolagents). Las llamadas de herramientas JSON siguen siendo dominantes en servicios administrados (Agentes Administrados Antropicos, Asistentes OpenAI) donde el proveedor controla el ejecutor.

> 两种架构都在生产中. CodeAct 在开放平台(OpenHands、smolagents) 主导.

### Escaflados en el paisaje 2026

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### ¿Por qué el andamio domina?

Una carrera de codificación es una trayectoria de largo horizonte (lección 1). Compuestos de fiabilidad a través de los pasos. Tres lugares donde el andamio compra puntos:

> 编码运行是长程轨迹 (第 1 课) ◊ fiabilidad a través de los pasos complejos (脚手架买入分数的三个地方):

1. **Retrieval**El ACI de SWE-agent, el índice de archivos de OpenHands y el mapa de repos de Aider atacan esto.
   En inglés:**检索**En el caso de los Estados Unidos, el número de personas que han sido víctimas de la pandemia es de aproximadamente un millón de personas.
2. **Verifier loop**: ejecutar pruebas, leer huellas de pila y volver a intentar es un delta de 10 puntos más en el banco SWE.
   En inglés:**验证器循环**Se trata de un proyecto de investigación que se desarrolla en el sector de la salud.
3. **Failure containment**El mismo modelo con y sin un bucle de verificación se parece a dos productos diferentes.
   En inglés:**失败遏制**El mismo modelo tiene y no tiene un ciclo de verificador que parece dos productos diferentes.

### La saturación de referencia y la distribución real.

Los autores de OpenHands y Epoch AI señalan que SWE-bench Verified tiene una cola fácil: 161 de 500 tareas necesitan solo 12 líneas de cambio. Las puntuaciones altas son impulsadas en parte por esta cola. SWE-bench Pro se limita a más de 10 cambios de línea y devuelve puntuaciones en el rango de 2359% incluso para sistemas fronterizos.

> OpenHands Autor y Epoch AI todos marcaron SWE-bench Verified 有简单尾部:500 个任务中 161 个 个只需要1-2 行变更──高分部分由该尾部驱动──SWE-bench Pro 限制10+ 行变更, incluso el sistema de la primera línea también regresa 23-59% 范围──Tu distribución de producción casi definitivamente más cerca de Pro y no Verified──

Implicación para elegir un agente: ejecutar un subconjunto Pro-like de su propio backlog de errores. La puntuación que importa es la puntuación en las tareas representativas de lo que envías.

> 选择 Agent 的含义: en tu propio bug 积压上运行 Pro 类子集── 重要分数是代表你发布任务的分数──

## Usalo con el marco de ejecución
```figure
a5-scaffold-delta
```

## Usalo

`code/main.py`compara dos andamios de agentes de juguete en una distribución fija de mini tareas:

> `code/main.py`En la distribución de misiones fijas de mini-comparar dos juguetes de agente:

1. ¿ Qué es esto ?**JSON tool-call**un andamio que toma una acción por turno.
   En inglés:**JSON 工具调用**¿Qué es eso?
2. ¿ Qué es esto ?**CodeAct**un andamio que puede emitir un pequeño fragmento de Python por acción.
   En inglés:**CodeAct**脚手架, cada movimiento puede salir pequeño Python 代码片段──

Ambos usan un "modelo" de estubes (reglas deterministas) por lo que la comparación aisla el andamio de la calidad del modelo.

> 两者使用存根模型" (Regulas de determinación) para comparar las estructuras de escritura con las estructuras de calidad del modelo separadas.

## Envíe el producto .

`outputs/skill-scaffold-audit.md`ayuda a auditar un andamio de agentes de codificación propuesto antes de su adopción: calidad de recuperación, presencia de verificadores, aislamiento de la caja de arena y ajuste de referencia a distribución.

> `outputs/skill-scaffold-audit.md` ayudarle en la adopción de la propuesta de auditoría Pre-Code Agent 脚手架:检索质量、验证器存在、沙箱隔离、基准到分布契合──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Cuántos giros hace cada andamio en el mismo conjunto de tareas? ¿Cuál es el radio de explosión por acción de cada uno?
   Traducción:运行`code/main.py`¿Cuántas ruedas de cada pieza en el mismo conjunto de tareas? ¿Cuánto media de explosión de cada movimiento?

2. Lea el documento OpenHands (arXiv:2407.16741). El documento argumenta que CodeAct supera las llamadas de herramienta JSON en tareas complejas. Identifique un modo de falla que el documento reconoce y escriba una frase sobre cuándo ese modo predominaría en la producción.
   En el texto original, el texto se utiliza para la traducción de la lengua inglesa.

3. Seleccione una tarea de su cartera de errores que requiere más de 10 líneas de cambio en dos archivos. Estima la probabilidad de éxito de extremo a extremo para un modelo fronterizo bajo (a) llamadas a herramientas JSON y (b) CodeAct. Justifique la brecha.
   China 文翻译: de tu bug 积压中选一个需要跨两文件 10+ 行变更的任务──估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率──论证差距──

4. SWE-bench Verified tiene 161 tareas de un solo archivo, 12 líneas. Construir una puntuación que las excluya. ¿Cómo se mezcla la tabla de clasificación?
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

5. Lea "Introducing SWE-bench Verified" (OpenAI). Explica la metodología específica utilizada para eliminar tareas ambigüas y nombra una categoría que la curadora no vería.
   La traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua inglesa en inglés de la lengua inglesa en inglés de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Más Leer más Leer más

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) el índice de referencia y la metodología originales.
  Traducción:Primero y método
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) cómo se construyó el subconjunto seleccionado.
  La obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra.
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) Arquitectura de CodeAct y diseño de eventos.
  El código de acción 架构和事件流设计.
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks) puntajes en vivo.
  En español, el nombre de la persona que ha sido identificada es el nombre de la persona que ha sido identificada.
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) Enmarcado de fiabilidad de los agentes codificadores de largo horizonte.
  En inglés, el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de.
