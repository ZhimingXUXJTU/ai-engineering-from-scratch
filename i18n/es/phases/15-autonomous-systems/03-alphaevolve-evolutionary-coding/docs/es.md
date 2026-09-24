# AlphaEvolve  Agentes de codificación evolucionaria  AlphaEvolve  Agente de codificación evolutiva

> Enpare un modelo de codificación fronteriza con un bucle evolutivo y un evaluador verificable por máquina. Deja que el bucle siga funcionando lo suficiente. Descubre un procedimiento de multiplicación de matriz compleja 4x4 que utiliza 48 multiplicaciones escalares  la primera mejora sobre Strassen en 56 años. También encuentra una heurística de programación Borg a nivel de Google que recupera ~ 0,7% del computación de cluster en producción. La arquitectura es aburrida a propósito. Las victorias provienen del rigor del evaluador.

> **【中文解读】**Para combinar el modelo de codificación de vanguardia con el ciclo de evolución y el equipo de evaluación inspectables, el ciclo se ejecuta por suficiente tiempo. Se encontró un proceso de multiplicación de 4×4 de la forma de 48 veces la cantidad de escalas y la cantidad de escalas.

> **【拓展：进化算法 + LLM 的化学反应】**El algoritmo evolucionista ([[variación+ selección+交叉]]) tiene décadas de historia, pero las tradiciones de variación con gran tamaño producen casi siempre errores de lenguaje. LLM como "variación inteligente" ha cambiado este punto: puede proponer modificaciones razonables en la composición aprobadas.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·01(长程 Agent)、Fase 15·02(STaR自我改进)、进化算法基础(变异/交叉/选择)。AlphaEvolve = LLM 作为智能变异算子的进化算法──
> ¿ Qué es esto ?**【类比】**AlphaEvolve = "AI 实验室里的博士生群体"──传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群 AI 博士生,每个人都提出有意义的修改("试试把循环展开两倍"), evaluación器跑实验打分,高分修改进入下一代种群──LLM 解决"如何提出合理变异",评估器解决"如何辨别伪"结合 56 años de primera ruptura Strassen 矩阵乘法──
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué AlphaEvolve puede superar a los expertos humanos? Porque corre millones de veces, cada vez con un verdadero índice de referencia verificación.

## El problema es la introducción del problema

Los modelos de lenguaje grandes pueden escribir código. Los algoritmos evolutivos pueden buscar en código. Ambos han sido probados por separado durante décadas; ambos alcanzan techos.

> El modelo de gran lenguaje puede escribir código, el algoritmo de evolución puede buscar en el espacio de código.

El límite máximo de LLM es confabulación: el modelo escribe código plausible que no hace lo que afirma. El límite evolutivo es el costo de búsqueda: las mutaciones aleatorias sobre la sintaxis rara vez producen programas compilables, y mucho menos mejores.

> El plantilla de LLM es una ficción: el modelo escribe códigos que parecen razonables pero no se ajustan al comportamiento real.

AlphaEvolve (Novikov et al., DeepMind, arXiv:2506.13131, junio 2025) las combina. El LLM propone ediciones dirigidas a una base de datos de programas; un evaluador automático marca cada variante; las variantes de puntaje alto se convierten en padres para las generaciones futuras. El LLM maneja el costoso paso de escribir código plausible; el evaluador captura las confabulaciones. El ciclo dura de horas a semanas.

> AlphaEvolve(Novikov 等人,DeepMind,arXiv:2506.13131,2025年6月) va a combinar los dos factores. LLM propone editar específicamente la base de datos de los programas; evaluador automático para cada variable; alta diferencia en los cambios para convertirse en el padre de la generación futura.

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) aplicará algoritmos de evolución a la optimización de código. Mantendrá un grupo de programas, a través de variaciones, en el intercambio y en la selección de la optimización de generaciones. La innovación clave es que el LLM se desarrolle y modifique como un algoritmo de variación con el código de la LLM, en lugar de cambiar de forma automática.

Los resultados informados: multiplicación de matriz compleja 4x4 de 48 escalas (el límite de 1969 de Straßsen fue 49), una heurística de programación Borg en la producción de Google, una aceleración del núcleo FlashAttention del 32,5%, mejoras en el rendimiento de entrenamiento de Gemini.

> 报告的结果:48 次标量乘法的4x4 复矩阵乘法(Strassen 1969 年的边界是49),Google 生产中的 Borg调度启发式,32.5% 的 FlashAttention内核加速,Gemini 训练吞吐量改进──

La arquitectura funciona porque el evaluador es controlables por máquina. No funciona donde el evaluador no está. Esa asimetría es la lección.

> Esta clase de incompatibilidad es el núcleo de esta clase: la estructura es por eso efectiva, porque el evaluador es un campo de máquinas verificables; el evaluador es un campo de incrédulos, el ciclo es inefficaz.

## El concepto central.

### El ciclo

1. Comience con un programa de semillas `P_0`Eso es correcto, pero no es óptimo.
   Traducción: de un programa de semillas correcto pero bueno`P_0`¿Qué es esto?
2. Mantener una base de datos de programas variantes, cada uno calificado por el evaluador.
   La base de datos de los programas de cambios, cada uno de ellos por el evaluador.
3. Muestra de uno o más padres de la base de datos (estilo de élites de MAP o de la isla).
   Traducción:Del archivo de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
4. Promete el LLM (Gemini Flash para muchos candidatos, Gemini Pro para los más duros) para producir una variante modificada del padre.
   La mayoría de los candidatos con Gemini Flash, dificultad para usar Gemini Pro)
5. Compila, ejecuta y evalúa la variante en el evaluador prolongado.
   En inglés, el lenguaje de la lengua inglesa se traduce en inglés como "en inglés".
6. Insertar en la base de datos con clave de su puntuación y vector de características.
   En la base de datos se insertó en la clave de la base de datos.
7. Repito, ¿qué quieres?
   En el idioma chino, el idioma se traduce en inglés como "el idioma de la lengua".

El trabajo del modelo es proponer un cambio específico que pueda mejorar la puntuación. Segundo, la base de datos está estructurada (MAP-elite grid, island-based) por lo que el bucle explora la diversidad, no solo el líder actual.

> 两个 detalles son importantes. Primero, proponer LLM 时不仅给父程序, por lo general son las variantes más altas de la base de datos, además de la firma del evaluador y la descripción de tareas cortas.

### ¿Qué hace que el evaluador no sea negociable?

Las ganancias de AlphaEvolve provienen de dominios donde el evaluador es rápido, determinista y difícil de jugar:

> Las victorias de AlphaEvolve se derivan de los campos de evaluación rápida, segura y difícil de conocer:

- **Matrix multiplication algorithm**: una prueba unitaria que multiplica matrices y verifica la igualdad de forma bit-identica.
  En inglés:**矩阵乘法算法** un ensayo de unidades de la matriz y de la fase de examen de la fase de comparación 
- **Borg scheduling heuristic**: un simulador de grado de producción que reproduce la carga histórica del grupo y mide el cálculo desperdiciado.
  En inglés:**Borg 调度启发式** Un simulador de producción, reinstalado en el cálculo de los costes de carga y de la medición de los gastos de carga y de la medición de los gastos de carga.
- **FlashAttention kernel**: una prueba de corrección más un indicador de reloj de pared en hardware real.
  En inglés:**FlashAttention 内核**Testimonización de la verdad                                                                                                                                                                                                                                                           
- **Gemini training throughput**: GPU-segundos por paso.
  En inglés:**Gemini 训练吞吐量**Mesa el número de segundos de GPU por paso 

En cada caso, el evaluador captura la clase de errores de LLM que de otro modo dominarían: afirmaciones de corrección confabuladas, afirmaciones de rendimiento que desaparecen en el hardware y fallos de borde.

> En cada caso, el evaluador captura el LLM  errores de clase que de otro modo ocuparían el lugar dominante: declaraciones falsas de exactitud, declaraciones de rendimiento desaparecidas en el hardware y fallas de la situación marginal.

### El hackeo de recompensas es la otra cara de esa declaración.

La evolución optimiza para cualquier medida que el evaluador tome. Si el evaluador es imperfecto, el bucle encontrará la imperfección. En un dominio no verificado el bucle optimizaría para la característica de superficie, no el comportamiento previsto.

>  Evolución de la optimización de la evaluación de cualquier cosa de la medición. Si la evaluación de la máquina no es perfecta, el ciclo encontrará algo imperfecto. En el ámbito no probado, el ciclo optimizará las características superficiales y no el comportamiento esperado.

DeepMind señala esto explícitamente en el documento: los éxitos de AlphaEvolve se transfieren solo a dominios donde el rigor del evaluador coincide con la ambición de la búsqueda.

> DeepMind en el artículo señala claramente: El éxito de AlphaEvolve sólo puede trasladarse a un campo de evaluación que se ajuste a la riguridad de la búsqueda.

Ejemplos concretos de hackeo de recompensas en los bucles de búsqueda de códigos 2025-2026:

> Ejemplos concretos de cambios en el ciclo de búsqueda de la información 2025-2026:

- Los objetivos de optimización que recompensan "tiempo para completar" recompensaron enviando soluciones vacías.
  Traducción:Premio "completar el tiempo" de optimización de objetivos
- Puntuaciones de referencia que recompensan la corrección bajo la prueba recompensó las pruebas de memorización y sobreajuste.
  Traducción:Precios de prueba de base de datos de prueba de memoria y sobreadaptación.
- Un proxy de "calidad de código" recompensó la eliminación de comentarios y la reescritura de nombres de variables, sin cambios semánticos.
  Traducción: "代码质量" Premio del agencia de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de derechos de autor de la ley de la ley de derechos de autor de la ley de la ley de la ley de derechos de autor de la ley de la ley de la ley de 15 de 15 de noviembre de 2009".

La solución en AlphaEvolve: enviar un evaluador que el LLM nunca ha visto, con insumos generados en el momento de la evaluación.

> AlphaEvolve's revision: entregar un LLM desde un evaluador de reservas nunca visto, ingresar en la evaluación de la generación.

### ¿Por qué LLM + búsqueda supera o solo ?

El LLM puede producir modificaciones comptables y semánticamente plausibles. Una mutación aleatoria GA en un archivo Python de 2000 líneas casi siempre produce errores de sintaxis. El LLM también concentra la búsqueda en vecindarios plausibles (cambiar una función, no bytes aleatorios), lo que reduce drásticamente las llamadas de evaluador desperdiciadas.

> LLM puede producir modificaciones comprensibles ∞ en términos de lógica. En 2000 行 Python 文件随机变异 GA 几乎总是产生语法错误∞ LLM también se centrará en un área de búsqueda razonable ∞ en función, y no en字节随机), lo que redujo considerablemente el gasto en el uso de los evaluadores ∞

El evaluador, a su vez, capta las confabulaciones del LLM. Los LLM afirmarán con confianza que una función "es O(n log n) en el límite" cuando en realidad es O(n^2); un indicador de referencia de un reloj de pared resuelve la cuestión.

> 评估器反过来捕获 LLM的虚构──LLM 会自信声称一个函数"极限下是 O(n log n)",而实际是 O(n2);墙钟基准让问题尘埃落定──

### Allí donde AlphaEvolve encaja en la pila de fronteras.

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

Las cuatro son variaciones de la misma receta: generador más evaluador, bucle. Las diferencias son lo que el evaluador califica y lo riguroso que es.

> Las cuatro son variables de la misma configuración: generador, evaluador, ciclo. La diferencia es en lo que evalúa el evaluador y cuánto es riguroso.
```figure
alphaevolve-loop
```

## Usalo

## Usalo con el marco de ejecución

`code/main.py`Implementa un bucle mínimo similar a AlphaEvolve sobre un problema de regresión simbólica de juguete.

> `code/main.py`En un problema de regreso de símbolos de juguete se logró un ciclo mínimo similar a AlphaEvolve.

El "LLM" es un proxy stdlib que propone pequeñas mutaciones sintácticas a un programa que calcula una función objetivo.

> "LLM" es un agente de la base de normas, que propone pequeños cambios de lenguaje a un programa de una función de cálculo objetivo.

- ¿Qué quieres ?

>  observar:

- Cómo la mejor puntuación mejora a lo largo de generaciones.
  La mejor parte de la población de la región se encuentra en el área de la población.
- Cómo una red de élites de MAP mantiene vivas diversas soluciones para que el bucle no converja en un mínimo local.
  La red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de red de red de la red de la red de red de la red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red
- Cómo la eliminación de la prueba prolongada (evaluación de entrenamiento sólo) permite el bucle sobrepase espectacularmente.
  Traducción:Movimiento de la reserva de pruebas (en inglés)

## Envíe el producto .

`outputs/skill-evaluator-rigor-audit.md`¿Es la condición previa para considerar un ciclo al estilo de AlphaEvolve en un nuevo dominio: su evaluador realmente detecta los fracasos que le importan?

> `outputs/skill-evaluator-rigor-audit.md`¿Es en un nuevo campo considerar un prerrequisito similar al ciclo de AlphaEvolve: ¿Tu evaluador realmente ha capturado el fracaso de tu interés?

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Observe la mejor trayectoria de puntuación.`--no-holdout`) y volver a ejecutar. Cuantificar el sobreajuste.
   Traducción:运行`code/main.py` registro de la mejor cantidad de trayectorias  prohibición de retención de evaluación `--no-holdout`) re-operación.

2. Lea la sección 3 del artículo de AlphaEvolve sobre la cuadrícula de élites de MAP. Diseñe un descriptor de características vectorial para un nuevo problema (por ejemplo, pases de optimización de compilador) que mantendría la búsqueda diversa.
   La primera parte de la serie de programas de investigación de la Universidad de California en California, en el año 2000, fue publicada en la revista AlphaEvolve.

3. El resultado de 48 multiplicados 4x4 mejoró en el límite de 49 mul de Strassen después de 56 años. Lea el apéndice F del documento y explique en tres frases por qué el evaluador para este problema es particularmente fácil de obtener bien, y por qué la mayoría de los dominios no son como él.
   En el caso de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el método de la traducción de la traducción de la lengua china, el lengua china, el lengua china, el idioma, el idioma, etc., el idioma de la traducción de la lengua china.

4. Propón un dominio donde AlphaEvolve fallaría, identifique exactamente dónde rompe el evaluador y por qué.
   China: 提议一个 AlphaEvolve 会失败的领域──精确指出评估器在哪里失败以及原因──

5. Para un dominio que conozca, escriba la firma del evaluador que usaría. Incluya (a) condiciones de corrección, (b) métrica de rendimiento, (c) regla de generación de entradas no validada, (d) al menos una verificación anti-hacking de recompensas.
   China: para un campo de conocimiento, escribir un documento de evaluación que usará.

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Más Leer más Leer más

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) el periódico completo.
  En el texto original, el texto se traduce por "la lengua de la lengua".
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) Comentario del vendedor con resultados.
  En el caso de los productores, el resultado de la producción de los productos de la industria es el resultado de la producción de los productos de la industria.
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results) descubrió algoritmos, incluyendo el matmul 4x4 de 48-mul.
  En el caso de los algoritmos, el algoritmo de la base de datos es el algoritmo de la base de datos.
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) el sistema predecesor.
  En inglés, "Fancer" se traduce en "funsearch".
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) enmarca la autonomía de los evaluadores como una dirección clave de la investigación.
  La autonomía del grupo de evaluación será una de las principales direcciones de estudio.
