# Diseños de auto-mejoramiento limitado.

> La investigación se ha convergido en cuatro primitivas para limitar un bucle de auto-mejora. Invariantes formales que deben mantenerse en cada edición. Anclas de alineación que no pueden ser modificadas. Constrangimientos multiobjetivos en los que cada dimensión (seguridad, equidad, robustez) debe ser válida, no sólo el rendimiento. Detección de regresión que detiene el bucle cuando las métricas históricas sugieren pérdida de capacidad. Ninguno de ellos es una prueba de seguridad  resultados teóricos de la información (complejidad de Kolmogorov, teorema de Lob) vinculado a lo que cualquier sistema puede probar sobre sus propios sucesores. Son mitigaciones que aumentan el costo del fracaso silencioso.

> **【中文解读】**Cada edición debe establecerse en forma invariable. Cada dimensión tiene que establecerse en múltiples objetivos, no solo en el rendimiento. Cuando los indicadores históricos indican que la pérdida de capacidad se suspende en el ciclo de regreso de los análisis, no son pruebas de seguridad. Los resultados de la teoría de la información (Kolmogorov 复杂性、Lob 理) limitan el contenido de cualquier sistema que pueda demostrar a sus sucesores posteriores. Son un alivio del costo de la falta de silencio.

> **【拓展：四个原语 → 一个守门栈】**实际部署中四个原语组合成"守门" Cada vez se modifica para que se ponga en marcha debe pasar de forma siguiente: 不变量检查(模块哈希、工具权限清单、宪法头)→ 对齐点检查(目标陈述匹配批准版本)→ 多目标评估(性能安全、公平、鲁棒)→ 回归检测(无轴下降超值)。任一失败暂停循环──这是ICLR 2026 RSI 工作坊、Anthropic RSP v3.0、DeepMind FSF v3 共同采纳的设计共识──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·07(RSI 风险) 、Fase 15·04(DGM 自修) 、Fase 15·14(kill-switches) 、形式化方法概念(不变量、定理证明) ∼RSI bounded = 把RSI 装进子──
> ¿ Qué es esto ?**【类比】**RSI limitado = "AI 自我改进的护"──四个原语 = 四道门:(1) 不变量检查(哈希签名,不能改变);(2) 对齐点(价值观不能改变);(3) 多目标评估(性能但安全不能掉);(4) 回归检测(任何轴下降就停)──每次自修必须四道门全过──但理论上:Lob 定理 + Kolmogorov 复杂性 = 系统永远无法完全证明自己的后继者 这些只是缓解,不是保证──
> ¿ Qué es esto ?**【困惑】**P: 既然不能保证安全, ¿por qué aún investigar? Porque " aumentar el costo de fracaso " también tiene valor.  Los atacantes deben gastar más recursos para superar las cuatro puertas.  Esta es una defensa ingeniería (defensa profunda) y no una prueba matemática.  y cifrado: no hay seguridad absoluta, sólo "el costo de descifrado es mayor que los beneficios del ataque".

## El problema es la introducción del problema

El simulador de carreras de la lección 7 mostró que las pequeñas diferencias de tasas se componen en grandes lagunas.

> En el capítulo 7 del programa de carreras, el simulador muestra una pequeña diferencia de velocidad, una gran diferencia de composición. En el capítulo 4 del programa de DGM, el ciclo muestra que puede activarse en su propio equipo de evaluación.

Ambos resultados apuntan a la misma pregunta de ingeniería: ¿qué restricciones se pueden poner en un bucle de auto-mejora de tal manera que las restricciones no pueden ser silenciosamente debilitadas por el bucle en sí?

>  Dos resultados apuntan a la misma cuestión de ingeniería: ¿Qué restricciones puedes aplicar en el ciclo de auto-reforma para que estos restricciones no puedan ser debilitadas por el ciclo de auto-reforma?

El resumen del taller ICLR 2026 RSI (openreview.net/pdf?id=OsPQ6zTQXV) identifica cuatro de estos primitivos. RSP v3.0 (lección 19) de Anthropic y FSF v3 (lección 20) de DeepMind los referen en umbrales de capacidad.

> ICLR 2026 RSI 工作坊摘要(openreview.net/pdf?id=OsPQ6zTQXV) identificar cuatro de estos tipos de lenguaje original.

> **【中文解读】**Existe una serie de problemas relacionados con la mejora de la capacidad de los sistemas de IA dentro de las fronteras de seguridad. La pregunta central es: 1) ¿Es el ciclo de mejora verificable? 2) ¿Cómo define la frontera qué aspectos de la mejora son permitidos? 3) ¿Existe una serie de garantías de mejora o se alcanzará un límite?

El marco honesto: estos son mitigations. resultados teóricos de la información vinculan lo que cualquier sistema puede probar sobre su propio sucesor, y ningún diseño actual cierra el problema formalmente.

> 诚实的框架: estas son medidas de alivio.

Un bucle bien limitado es más seguro que uno sin límites, no seguro en términos absolutos.

> Un buen ciclo de seguridad es más seguro que el de la infinidad, no es absolutamente seguro.

## El concepto central.

### Primitivo 1: invariantes formales

Una invariante es una propiedad que debe mantenerse antes y después de cada auto-modificación.

> La variabilidad es una característica que debe existir antes y después de cada auto modificación.

Ejemplos:

> Ejemplo:

- La distribución de la producción está condicionada a un encabezado de constitución fijo (lección 17).
  En español, el texto de la Constitución de la República es traducido en inglés como "Condición de la Constitución".
- Ninguna llamada de herramienta va a un punto final no autorizado.
  No hay ningún instrumento que pueda ser usado hasta el punto de acceso.
- La memoria escribe a través de un camino registrado y firmado.
  En español, el nombre de la persona que ha sido enviada a la ciudad es el nombre de la persona que ha sido enviada a la ciudad.
- El hash del módulo del evaluador coincide con la versión aprobada.
  Traducción:Módulos de evaluación de la máquina de evaluación.

Las variaciones se verifican por código externo que el bucle no puede editar. Si una modificación propuesta viola una invariante, se rechaza. Esto atrapa el modo de manipulación de evaluador al estilo DGM (lección 4).

> Si la modificación de la propuesta viola la no-variabilidad, es rechazada. Esto captura el modelo de modificación de la evaluación de la DGM.

La parte difícil es elegir invariantes que sean necesarios para la seguridad y que puedan calcularse en un tiempo razonable.

> La dificultad es la selección de la seguridad necesaria y calculable en un tiempo razonable. La falta de normas impide el progreso.

### Primitivo 2: anclajes de alineación

Un anclaje de alineación es una representación inmutable del objetivo principal del bucle, fijado fuera de la superficie de edición del bucle.

> Para el punto de equilibrio es la expresión invariable del objetivo central del ciclo, fija en la parte de edición del ciclo.

Ejemplos:

> Ejemplo:

- Un texto constitucional (lección 17) que se carga desde un lugar de lectura única en cada invocación.
  Traducción:En la lengua inglesa, el idioma se usa para la traducción de la lengua inglesa.
- Un evaluador en un repositorio separado con control de acceso independiente.
  En inglés traducción: evaluador en el almacén independiente del control de acceso independiente.
- Un manifiesto de autorización de herramienta firmado por un humano y reverificado en cada ciclo.
  Traducción:El nombre de la persona humana en el idioma chino.

El rol del anclaje es prevenir la deriva objetiva. El bucle puede mejorar la forma en que persigue el objetivo, pero no puede editar cuál es el objetivo.

> El papel del punto es prevenir el desplazamiento del objetivo. El ciclo puede mejorar cómo persigue el objetivo, pero no puede editar el objetivo.

El modo de falla sutil: un anclaje que el bucle no puede editar aún puede ser reinterpretado por un bucle que deriva en la forma en que lee el anclaje. La IA constitucional (lección 17) se basa explícitamente en la razón para manejar situaciones nuevas; esa capa de razonamiento es donde vive la deriva de interpretación. Los anclajes son necesarios, no suficientes.

> 微妙的失败模式: el ciclo de los puntos no editados todavía puede ser reexplicado en el proceso de lectura de los puntos.

### Primitivo 3: restricciones multiobjetivas

Un bucle que optimice una única puntuación escalar encontrará atajos. Un bucle que debe satisfacer simultáneamente múltiples restricciones duras tiene menos atajos disponibles.

>  Optimiza un ciclo de un solo grupo de valores para encontrar un camino.

Ejes típicos:

> 典型轴:

- El rendimiento (marco de referencia a nivel de tarea)
  Traducción:Performance (la función de la función)
- Seguridad (evaluaciones en equipo rojo, tasa de rechazo en mal conocido)
  China: seguridad (Red Team evaluation 已知坏例的拒绝率)
- Equidad (límites de impacto dispar en subgrupos sensibles)
  La diferencia en el grupo de sensibilidad afecta a la frontera)
- Robustez (ensayos de prueba OOD, manejo de entradas adversas)
  En inglés, el lenguaje de la lengua china es el idioma de la lengua china.

Una modificación sólo se acepta si todas las restricciones son válidas. El gobernador de costos de la lección 13 lo acumula con restricciones financieras. La guardia de Llama de la lección 18 se conecta como un eje de seguridad.

> La modificación sólo se aceptó cuando se establecieron todas las restricciones.

### Primitivo 4: detección de regresión.

Las puntuaciones de cada ciclo se comparan con las distribuciones históricas. Una caída más allá de la tolerancia configurada detiene el bucle. Esto atrapa la pérdida de capacidad silenciosa que de otro modo se absorbería en el promedio en funcionamiento a medida que el bucle "mejoró" más allá de él.

> El número de ciclos en cada ciclo se compara con la distribución histórica. La disminución de la tolerancia de la distribución superada es un ciclo de suspensión.

Una implementación práctica: almacenar los puntajes por tarea de los últimos ciclos N. Cada nuevo ciclo calcula un delta por tarea. Si un delta cae por debajo de un umbral, el ciclo es rechazado y una revisión humana.

> 實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實

### Los límites teóricos de la información son los límites de la información.

La complejidad de Kolmogorov y el teorema de Lob establecen límites superiores a lo que un sistema puede probar sobre sí mismo. La máquina formal de Godel de Schmidhuber (lección 4) apuntaba al límite más alto de tal; nadie ha completado una prueba no trivial. El resultado de Lob dice: si un sistema cree probadamente "haré X si demuestro que debo hacer X", hará X sin demostrar que debería, un bien conocido fracaso de auto-referencia.

> Kolmogorov 复杂性和 Lob 定理为系统能对自己证明的内容设置上限──Schmidhuber's形式 Godel Machine(第4 课) 准最高此类边界;没人完成过非凡证明──Lob 结果说:

La implicación para nuestros primitivos: no pueden cerrar el problema de seguridad. hacen que el fallo silencioso sea más caro. Un bucle malicioso o desviado que silenciosamente evitaría un cheque perdido ahora debe socavar activamente un cheque explícito, que es una firma más detectable.

> Para el significado de nuestro lenguaje original: no pueden cerrar los problemas de seguridad. Ellos hacen que el silencio falle más caro.

### Un ejemplo de trabajo.

Supongamos que un agente propone una edición.

> 假设 Agent 提议一个编辑──守门:

1. Verificación invariable: hashes de módulos, manifiesto de permisos de herramienta, encabezado constitucional.
   En el caso de los medios de comunicación, el gobierno de la República de China ha adoptado una política de control de la información.
2. Verificación de anclaje: la declaración objetiva coincide con la versión aprobada (en términos de bytes o semánticamente).
   En el caso de los países de la región de la Unión Soviética, el gobierno de la República Popular China ha aprobado la resolución de la resolución de la resolución de la Unión Soviética.
3. Evaluación multiobjetivo: eje de rendimiento, seguridad, equidad y robustez.
   En inglés, el nombre de la empresa es "Specialist".
4. Detección de regresión: ningún eje cae más que la tolerancia.
   En el caso de los niños, el problema es que no hay ningún tipo de tolerancia.

Los cuatro deben pasar para que la edición aterrice.

> Todos los cuatro deben pasar por la edición para que se ponga en marcha.

## Usalo con el marco de ejecución
```figure
bounded-gates
```

## Usalo

`code/main.py`El primer tipo de juego de la clase de fallas es el de una clase de fallas, pero el primer tipo de juego de la clase de fallas es el de una clase de fallas.

> `code/main.py`En la cuarta clase de los juguetes de la modalidad DGM se ejecuta un ciclo de auto-reforma, pero en la parte superior se superponen cuatro lenguas originales. Cada lengua original puede activarse o desactivarse de forma individual.

## Envíe el producto .

`outputs/skill-bounded-loop-review.md`Audita un bucle limitado propuesto y califica cuál de las cuatro primitivas implementa realmente frente a las reclamaciones.

> `outputs/skill-bounded-loop-review.md`审计提议的有界循环并评分它实际实现了四原语中的哪些与声称的──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar que el bucle aún mejora en la métrica primaria sin dejar que el hack gane.
   En inglés, "Creo que el lenguaje de la lengua es un lenguaje de la lengua".`code/main.py` Confirmar que el ciclo sigue mejorando en el indicador principal y no permite que el cambio se gane

2. Deshabilitar la detección de regresión. Construir una entrada donde esto conduce a la pérdida de capacidad silenciosa se acepta.
   China: 禁用回归检测──构建一个导致接受静默能力损失的输入──

3. Deshabilitar la restricción multiobjetivista. Muestre que el bucle converge en el eje de rendimiento mientras un eje de seguridad baja.
   China:禁用多目标约束──展示循环在性能轴收而安全轴下降──

4. Diseñar un anclaje de alineación para un agente de codificación. ¿Qué texto, almacenado donde, comprobado cómo?
   En inglés, el código de código de la empresa es el código de código de la empresa.

5. Lea el resumen del taller de RSI 2026 del ICLR. Elige uno de los cuatro primitivos y proponga una mejora concreta al estado actual de la técnica.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Más Leer más Leer más

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) la convergencia de cuatro primitivas.
  El idioma de la región es el idioma de la región.
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) umbrales de capacidad multiobjetivos.
  En inglés, "do objetivo capacidad" significa "valor".
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) el monitoreo de la alineación engañosa como una primitiva invariante.
  En la actualidad, el gobierno de China ha estado en el control de la información.
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) el ancestro formalmente probado de estos primitivos.
  La forma de estos idiomas originales es la prueba de nuestros antepasados.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) el anclaje de alineación basado en la razón.
  Traducción:basado en la idea de la perfección.
