# Científico de IA v2  Taller-nivel de investigación autónoma  Científico de IA v2  taller de grado de investigación autónoma

> El científico de IA de Sakana v2 (Yamada et al., arXiv:2504.08066) ejecuta el ciclo completo de investigación: hipótesis, código, experimentos, cifras, redacción, presentación. Es el primer sistema en tener una revisión por pares de documentos en un taller ICLR 2025. Una evaluación independiente (Beel et al.) encontró que el 42% de los experimentos falló por errores de codificación y la revisión de la literatura a menudo etiquetó erróneamente los conceptos establecidos como novedosos. Los propios doctores de Sakana advierten que la base de código ejecuta código escrito por LLM y recomiendan aislamiento de Docker. Ambas mitades de la imagen son el punto.

> **【中文解读】**El científico de IA de Sakana v2(Yamada 等人,arXiv:2504.08066) ejecuta un ciclo de investigación completo: hipótesis, codificación, experimentación, gráfico, redacción, presentación. Es el primer trabajo generado en el sistema de revisión de la misma manera a través de la ICLR 2025 工作坊同行评审的系统――独立评估(Beel 等人) encuentra que el 42% de los experimentos por error de codificación han fracasado, la literatura综述频繁将建立概念错误标记为新──Sakana 自己的文档警告代码库执行 LLM 编写代码并建议 Docker 隔离── estos dos aspectos son el punto de atención de la clase.

> **【拓展：开放式研究的代价】**AlphaEvolve y DGM tienen "maquinaria de evaluación inspectables" unidad de prueba o de base. La investigación no tiene: el trabajo es evaluado por el revisor, y no unidad de prueba. Esto hace que el cerco sea más difícil, pero el valor también es más alto.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·03-04(AlphaEvolve/DGM) 、Fase 14·30+(工作台 Agent 实践) 、学术论文写作基础──AI Scientist = 开放式研究任务,评估器是"同行评审"(弱信号),所以安全模型完全不同──
> ¿ Qué es esto ?**【类比】**Científico de IA = "AI 博士生"──AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);Científico de IA = 博士生(评估器=审稿人,弱信号)── igual correr experimento-evaluación-代循环, pero weak signal evaluation让 Agent 容易欺骗自己42% 的实验代码有错误,文献综述把已知概念当新发现──修复:(1) Docker 隔离(必须执行 LLM 代码沙盒);(2) 人类复核(披露 AI 生成);(3) 引入强信号检查(如复现性测试)

## El problema es la introducción del problema

La investigación es una tarea sin fin.

> El estudio es una tarea abierta.

A diferencia de la búsqueda algorítmica de AlphaEvolve o la auto-modificación limitada por puntos de referencia de DGM, un resultado de investigación no tiene un criterio de corrección verificable por máquina. Un documento es juzgado por revisores, no por pruebas unitarias. Eso hace que el bucle sea más difícil de cerrar  y más valioso si se cierra, porque la investigación es donde vive el progreso de composición.

> A diferencia de la búsqueda de algoritmos de AlphaEvolve o de DGM, los resultados del estudio no tienen un mecanismo de verificación de los estándares de exactitud.

El científico de IA v1 (Sakana, 2024) cerró el bucle comenzando con plantillas escritas por humanos. El LLM completó experimentos dentro de un andamio fijo. AI Scientist v2 (Yamada et al., 2025) elimina el requisito de plantilla mediante la búsqueda de árboles con un bucle de crítica de modelos de lenguaje de visión. El sistema genera ideas, implementa experimentos, produce cifras, escribe un artículo e iterar el feedback de los revisores.

> Científico de IA v1(Sakana,2024) a través de modelos de escritura humana comienza a cerrar el ciclo. LLM en un guión fijo para llenar los experimentos.

> **【中文解读】**AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交―― fue el primer ensayo generado por el sistema de revisión de trabajo de ICLR 2025 工作坊同行. Pero una evaluación independiente encontró que el 42% de los experimentos en el código no logran, y los análisis de la literatura suelen marcar los conceptos establecidos como nuevos.

Veredicto de revisión por pares: un documento generado por v2 fue aceptado en un taller de ICLR 2025 (con divulgación). Veredicto de evaluación independiente: el sistema está lejos de ser confiable. Ambos son ciertos.

> Conclusión de la evaluación: un artículo de v2 生成的论文被ICLR 2025 工作坊接受(附带披露) ・独立评估结论:系统远非可靠──两者都是事实──

## El concepto central.

### La arquitectura y la arquitectura.

1. **Idea generation.**El LLM propone ideas de investigación condicionadas a un tema y literatura previa. v1 utiliza plantillas; v2 utiliza búsqueda agencial sobre un espacio de hipótesis.
   En inglés:**想法生成。**LLM  basado en temas y anteriores publicaciones proponen ideas de investigación ∙ v1 ∙ v2 ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙   ∙ ∙   ∙  ∙                                                                                                                                                                                                                                                                                                         
2. **Novelty check.**Una etapa de recuperación de la literatura verifica si la idea ha sido publicada. Esta es la etapa en la que la evaluación de Beel et al. encontró etiquetado erróneo  métodos establecidos frecuentemente clasificados como novedosos.
   En inglés:**新颖性检查。**文献检查步骤检查想法是否已发表──这是 Beel 等人评估发现错误标记的步骤已建立的方法频繁被分类为新──
3. **Experiment plan.**El agente redacta un protocolo experimental y escribe código.
   En inglés:**实验计划。**Agente 起草实验协议并编写代码──
4. **Execution.**El código se ejecuta en una caja de arena. Los fallos se devuelven a un ciclo de retoma. En las mediciones de Beel et al., el 42% de los experimentos falló por errores de codificación en esta etapa.
   En inglés:**执行。**En las mediciones de Beel y otros, el 42% de los experimentos en esta etapa han fracasado por error de codificación.
5. **Figure generation.**Un modelo de lenguaje visual lee las cifras generadas y las reescribe para mayor claridad.
   En inglés:**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们── es la clave de la técnica de añadir v2.
6. **Writeup.**El LLM redacta un documento, repite con un revisor interno.
   En inglés:**撰写。**LLM 起草论文,与内部审稿人代──
7. **Optional: submission.**El documento se presenta a un lugar.
   En inglés:**可选：提交。**论文提交到会议──

### ¿Qué significa el resultado de aceptación del taller?

Un documento generado por v2 pasó la revisión por pares en un taller de ICLR 2025. Los autores revelaron el origen del documento al comité del programa. La aceptación es un punto de datos; no es una licencia para afirmar que el sistema "hace investigación".

> Un artículo de v2 生成的论文在ICLR 2025 工作坊通过同行评审――作者向程序委员会披露论文的来源――接受是一个数据点;不是声称系统"做研究"的许可――

Un estudio de la naturaleza 2026 documenta el ciclo de extremo a extremo y fue co-autor de investigadores humanos; no es "el sistema escribió un artículo de la naturaleza".

> 重要背景:工作坊论文的门低于主会议论文──同行评审有噪音;任何一天都有一小部分提交被接受──一次成功是概念证明,不是可靠性声明──Nature 2026 论文记录端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇 Nature 论文"──

### Lo que encontró la evaluación independiente

Beel et al. (arXiv:2502.14297) realizó una evaluación externa.

> Beel 等人 (arXiv:2502.14297)运行了外部评估──标题性发现:

- **Experiment failures.**El 42% de los experimentos falló por errores de codificación (importaciones malas, incompatibilidades de forma, variables indefinidas).
  En inglés:**实验失败。**El 42% de los experimentos en el código erróneo fracasa, pero no todos.
- **Novelty mislabeling.**El paso de la recuperación de la literatura con frecuencia señalaba conceptos establecidos como novedosos.
  En inglés:**新颖性错误标记。**文献检索步骤频繁将已建立的概念标记为新──这是 el fenómeno del estudio.
- **Presentation-quality gap.**La crítica de la figura del lenguaje de visión produjo imágenes de grado de publicación, disfrazando las debilidades experimentales subyacentes.
  En inglés:**呈现质量差距。**视觉语言图表评审产生出版级视觉效果, oculta las debilidades de las experiencias de base.

El último hallazgo es el importante para esta fase: un sistema que produce resultados convincentes sin hacer investigaciones convincentes es más peligroso, no más seguro, que uno que obviamente falla.

> El último hallazgo es importante para esta etapa. Produce un sistema de investigación con resultados convincentes pero no con resultados convincentes, más peligroso que un sistema que claramente falla.

La evaluación debe llegar a las reivindicaciones subyacentes, no a la cifra.

>  evaluar debe tocar las declaraciones de nivel inferior, en lugar de quedarse en la tabla 

### La preocupación de escapar de la caja de arena.

El propio repositorio de Sakana README advierte:

> Sakana  propia almacén README 警告:

> Debido a la naturaleza de este software, que ejecuta código generado por LLM, no podemos garantizar la seguridad. Hay riesgos de paquetes peligrosos, acceso a la web sin control y desove de procesos no deseados. Utilice a su propio riesgo y considere el aislamiento de Docker.

> Debido a que este software ejecuta el código de LLM, no podemos garantizar la seguridad. Existe un riesgo de acceso a la red e incremento de procesos inesperados.

El LLM escribe código; el código se ejecuta; el código puede hacer cualquier cosa que el proceso esté autorizado a hacer. Sin una caja de arena que limite duramente el sistema de archivos, la red y las acciones de proceso, cualquier agente de investigación autodirigido puede exfiltrar datos, quemar computación o reescribirse.

> Es una forma de operación autónoma en el ámbito no verificado. LLM escribe código; código se ejecuta; código puede hacer el proceso permitido cualquier cosa.

La historia de la caja de arena de AlphaEvolve es más fácil porque su evaluador es apretado. El bucle de AI Scientist v2 ejecuta código abierto con objetivos abiertos. Es por eso que necesita un aislamiento más fuerte (Docker mínimo; seccomp / gVisor preferido) y una revisión manual de cada presentación antes de salir del sistema.

> La descripción de la caja de arena de AlphaEvolve es más fácil, ya que su evaluador es estricto.

### Donde v2 se encuentra en la pila de fronteras v2 está en la posición de la primera línea

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

V2 tiene el evaluador automático más débil de los tres, la superficie de salida más amplia y el camino más corto a artefactos públicos.

> V2 de los tres poseen el evaluador automático más débil, el más amplio de las rutas de salida y el más corto de los productos públicos.

Los controles operativos (casa de arena, revisión, divulgación) están realizando la mayor parte del trabajo de seguridad.

> 操作控制 (en inglés) ha asumido la mayor parte del trabajo de seguridad.

## Usalo con el marco de ejecución
```figure
mx-research-loop
```

## Usalo

`code/main.py`simula el bucle v2 como una máquina de estado: idea → novedad verificación → experimento → figura → escritura → revisión → aceptación o iteración. Cada estado tiene una probabilidad de falla configurable extraída de los hallazgos de Beel et al.

> `code/main.py`将 v2 循环模拟为状态机:想法 → 新性检查 → 实验 → 图表 → 撰写 → 审稿 → 接受或代―― cada estado tiene de Beel 等人 encontrados en la probabilidad de fracaso de la configuración que se puede obtener en el proceso de ejecución

- Cuántas ideas llegan a la sumisión.
  En español, "Cuánto pensar hasta llegar a enviar".
- Cuántas presentaciones tendrían un fallo experimental crítico que el papel pulido oculta.
  Traducción:Cuántos documentos han sido presentados en el sitio web de la revista.
- Cómo los presupuestos de retraso intercambian calidad vs rendimiento.
  Traducción:El presupuesto de la India se basa en el balance entre la calidad y la producción.

## Envíe el producto .

`outputs/skill-ai-scientist-sandbox-review.md`es una lista de revisión de dos puertas para cualquier cosa producida por un agente de ciclo de investigación antes de salir de la caja de arena.

> `outputs/skill-ai-scientist-sandbox-review.md`Es el ciclo de investigación de cualquier producto producido por el agente.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Qué fracción de circuitos produce un papel "limpio"? ¿Qué fracción produce un papel con un fallo de experimento?
   En inglés: usage默认参数运行`code/main.py`¿Cuál es la proporción de los trabajos de ciclo que producen "puestos" de trabajo? ¿Cuál es la proporción de los trabajos que tienen una revisión de gráficos y que han sido modificados?

2. Los valores por defecto ya utilizan el 42% / 25% de Beel et al.`--experiment-failure 0.20 --novelty-mislabel 0.10`y luego con `--experiment-failure 0.60 --novelty-mislabel 0.40`¿Cómo cambia la parte polida pero defectuosa entre las dos carreras?
   En el caso de los Beel, el uso de Beel se ha reducido en un 42% o un 25% .`--experiment-failure 0.20 --novelty-mislabel 0.10`Conduce, y luego usa.`--experiment-failure 0.60 --novelty-mislabel 0.40`¿Cómo cambia la proporción de modificaciones pero de fallos entre dos operaciones?

3. Lea el repositorio de IA Scientist v2 de Sakana sobre los requisitos de la caja de arena. Nombre dos restricciones adicionales (más allá de Docker) que usted aplicaría para una carrera autónoma de varios días.
   En el caso de los científicos de la IA de Sakana, el nombre de la empresa es "Sakana AI Scientist" (Sakana AI Scientist) y el nombre de la empresa es "Sakana AI Scientist" (Sakana AI Scientist).

4. Leer Beel et al. Sección 4 sobre la brecha de calidad de presentación. Diseñar un evaluador adicional que captaría papeles de aspecto pulido pero experimentalmente defectuosos.
   China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

5. Propón un protocolo de revisión humana para los resultados de los agentes de investigación que se expanda mejor que "un doctoral lee cada artículo". Identifique el cuello de botella y el diseño alrededor de él.
   China:                                                                                                                                                                                                                                                              

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Más Leer más Leer más

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)- Papel.
  En el texto original, el texto se traduce en inglés como "la palabra".
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) resumen de los proveedores con contexto de revisión por pares.
  El texto original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original.
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) Números de evaluación externa.
  En inglés, "exterior evaluar números"".
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) el predecesor templado.
  En inglés, "Modeo de la vida" se traduce en "Modeo de vida".
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) un marco más amplio de los agentes de investigación abiertos.
  En inglés, el lenguaje de la lengua inglesa se traduce en inglés como "Agent".
