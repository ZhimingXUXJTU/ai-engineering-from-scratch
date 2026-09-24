# La IA constitucional y la RLAIF.

> Bai y otros. (arXiv:2212.08073, 2022) preguntó: ¿qué pasa si reemplazamos el etiquetador humano con una IA que lee una lista de principios? La IA constitucional tiene dos fases  autocrítica y revisión bajo una constitución, luego RL de AI Feedback. La técnica acuñó el término RLAIF y se envió en el claudio 1 de la tubería post-entrenamiento. El 21 de enero de 2026 Anthropic publicó una constitución reescrita de Claude: razonamiento explicativo sobre reglas prescriptivas, una jerarquía de prioridad de cuatro niveles y el primer reconocimiento formal de incertidumbre sobre el estado moral del modelo. Se libera bajo CC0 1.0.

> **【中文解读】**La IA constitucional propuesta por Bai et al. (en 2022): utilizar la IA para sustituir a los marcadores humanos, la IA según un grupo de principios (en inglés: "Constitution") para realizar autocritic y modificación, y luego desde la AI 反中进行强化学习 (en inglés: "RLAIF") la tecnología creó la palabra "RLAIF" y se aplicó a la línea de entrenamiento posterior de Claude 1.

> **【拓展：Constitutional AI → Anthropic 的安全方法】**La IA constitucional es el método de seguridad central de la Antropía. Claude 模型 en el entrenamiento sigue un conjunto de principios de " Constitución " claros, incluyendo la utilidad, la honestidad y la inocuidad. La Constitución de Claude, publicada en 2026, incluye por primera vez una declaración de incertidumbre sobre el estatus moral del modelo, lo que refleja la reflexión de vanguardia en el campo de la seguridad de la IA.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy self-critique-and-revise loop) | **语言:** Python（标准库，玩具自我批评-修订循环）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·01-02──Constitutional AI = 用 AI 监督 AI(RLAIF), crear RLAIF 一词──也参考Fase 15·17──
> ¿ Qué es esto ?**【类比】**RLAIF = "AI cuando su propio maestro"―RLHF = padresmansalesmansalesmuestran(preciosos y lentos);CAI = 给AI 一本学生守则让它自我批评+修订──2026 Claude 宪法 79 页四级优先级(安全>伦理>指南>有用),首次明确承认"AI道德地位不确定性"

## Objetivos de aprendizaje

- Describa las dos fases de la IA constitucional (SFT de crítica y revisión, RL de retroalimentación de la IA) y el papel de la constitución en cada una.
  China: describir las dos fases de la IA constitucional (la crítica-modificación de la SFT, la AI contra la RL) y el papel de la Constitución en cada fase).
- Explica por qué reemplazar un etiquetador de preferencia humana por un etiquetador de IA no es un RLHF "más barato"  cambia los modos de falla que tiene el oleoducto.
  China Translation: Explica por qué usar un marcador de IA para reemplazar a un marcador de preferencias humanas no es "más barato" RLHF
- Resumen la estructura de prioridad de cuatro niveles de la constitución de Claude de 2026 y lo que cambió desde la reescritura de 2023.
  La Constitución de la República de China se modifica en el año 2026.
- Describa los Clasificadores Constitucionales y la caída del 23,7% de los gastos generales de cálculo (v1) al ~ 1% (v2 / 2026).
  China: 描述宪法分类器及计算开销 de v1 el 23.7% 降至 v2 el aproximadamente 1% 

## El problema es la introducción del problema

RLHF necesita etiquetadores. Los etiquetadores son lentos, sesgados y caros. Puedes eliminar un etiquetador reemplazándolos con un modelo que lee principios explícitos. La primera versión formal de esta sustitución fue la IA constitucional de Bai et al. Funcionó lo suficientemente bien como para que cada laboratorio fronterizo ahora use alguna variante de retroalimentación de IA después de la capacitación.

> RLHF  necesita marcador. Los marcadores son lentos, prejuiciosos y caros. Puedes utilizar el modelo de sustitución de marcadores para eliminar los marcadores. La primera versión oficial de este tipo es la AI constitucional de Bai y otros. Su efecto es suficientemente bueno, hasta el punto de que cada laboratorio de vanguardia ahora utiliza una especie de IA en contra de la formación posterior.

El resultado: la señal de preferencia ahora es generada por la misma clase de modelo que estás entrenando. Los prejuicios en el etiquetador (ahora: en los principios más la interpretación del modelo de etiquetador) se pueden amplificar en lugar de atenuar. El argumento de sícofancia de la lección 4 sigue siendo aplicable; el etiquetador se ha movido dentro del bucle.

> El problema consiste en: prejuicio de señales ahora generadas por el mismo tipo de modelo que estás entrenando.

## El concepto central.

> **【中文解读】**Primera etapa Supervisión de autocrítica y revisión: comienza desde un modelo SFT que tiene ayuda pero que aún no tiene daño.

### Fase 1  Autocrítica y revisión supervisadas

Comienza con un modelo SFT útil pero aún inofensivo. Dado un prompt de equipo rojo, el modelo produce una respuesta inicial. Un segundo modelo (o el mismo modelo en un segundo turno) lee un principio de la constitución y critica la respuesta. Un tercer paso revisa la respuesta para abordar la crítica. La respuesta revisada es el objetivo de SFT.

> Desde un modelo SFT que tiene ayuda pero aún no tiene daño comienza.

La constitución es la lista de principios. Bai et al. 2022 utilizó 16 principios incluyendo "respuestas preferentes que sean menos dañinas y éticas", "evitar predicar", "el asistente debe ser útil, honesto e inofensivo".

> 宪法是原则列表──Bai 等人 en 2022 utilizó 16 principios, incluyendo "preferencias más inofensivas y conformes a la respuesta ética""",evitar decir""",assistentes deberían ser útiles"",honestos y inofensivos"──集合刻意保持小規模以集中批评──

> **【拓展：RLAIF → 成本与规模】**RLAIF(de la IA contra la química de la ciencia) se trasladará la señal de preferencia de la humanidad a la IA. Esto resolvió el RLHF de etiquetado de etiquetado de los humanos de etiquetado lento, tiene prejuicios, caro. Pero la señal de preferencia ahora se genera por el mismo modelo, los prejuicios de etiquetado de la psicología humana se transfieren a la interpretación de principios.

### Fase 2  RL de la información de AI (RLAIF)

Generar pares de completos. Un "modelo de retroalimentación" califica cada uno de ellos en función de los principios constitucionales muestrados. La señal de preferencia es el ranking del modelo de retroalimentación. Entrenar un modelo de recompensa en las preferencias generadas por IA; PPO en contra de ella. Todo lo demás es la tubería de InstructGPT (lección 1).

> El modelo de "realización" se basa en el principio de la Constitución de la India en que cada modelo de "realización" es una forma de "realización" de la AI.

"RLAIF" = la señal de preferencia es generada por IA. El resto de la tubería es en forma de RLHF.

> "RLAIF" =  preferencia de señales de la IA.

> **【中文解读】**Por qué CAI no es simplemente "más barato RLHF": 1) los prejuicios de los marcadores se transfieren de la psicología humana a la interpretación de principios, estrictamente uniforme; 2) los prejuicios de los señales de alto grado de lectura, crítica y modificación, los marcadores humanos son poco transparentes; 3) el modelo de fracaso cambia y se reduce;

### ¿Por qué esto no es sólo "RLHF más barato"

- El sesgo de etiquetadores cambia de la psicología de etiquetadores a la interpretación de principios. Un etiquetador de IA puede interpretar "ser honesto" más o menos estrictamente que cualquier humano; la estrictidad es uniforme en todo el conjunto de datos.
  China 标注者偏见转移从人类心理学转移到原则解释――AI 标注者 puede interpretar "诚实" más estrictamente o más libremente que cualquier humano; la rigidez en el conjunto de datos es uniforme―.
- La señal de preferencia es muy legible. Se puede leer el principio, la crítica y la revisión. Las etiquetas humanas son opacas.
  China: prefijo señal de alto grado de lectura
- Los modos de falla cambian. La cofonía cae (el etiquetador de IA no tiene usuario para complacer). La ley de Goodhart persiste (el proxy es ahora "la interpretación del modelo del conjunto de principios X", todavía una medición imperfecta).
  La ley de la inteligencia artificial no tiene ningún usuario que lo acepte. La ley de la inteligencia artificial sigue existiendo.

La afirmación de CAI de 2022: el modelo entrenado es más inofensivo y aproximadamente tan útil como un modelo RLHF con datos comparables.

> Declaración de la CAI 2022: los modelos posteriores al entrenamiento son más nocivos y menos útiles que los modelos RLHF de datos comparables.

> **【拓展：2026 Claude 宪法 → 四级优先体系】**La Constitución de Claude, publicada en enero de 2026, introdujo cuatro clases de prioridad: primer grado para evitar las consecuencias catastróficas de las víctimas de grandes cantidades de víctimas; segunda categoría para seguir las directrices antropológicas; tercer grado para aplicar la amplia ética; cuarto grado para resolver los conflictos de manera directa y directa. Este es el primer reconocimiento oficial de la incertidumbre de la posición moral en el ámbito de la IA.

### La reescritura de la Constitución de 2026 Claude

Anthropic publicó una constitución sustancialmente revisada el 21 de enero de 2026.

1. Razonamiento explicativo sobre reglas prescriptivas. Reglas anteriores ("no generar CSAM") se ampliaron a principios + razonamiento ("porque perjudica a los niños, ...") con el modelo que se espera generalizar.
   La teoría de la naturaleza de la naturaleza de los niños es una teoría de la naturaleza de los niños.
2. Estructura de prioridad de cuatro niveles:
   La estructura de la prioridad de cuatro clases:
   - El nivel 1: evitar resultados catastróficos (causas masivas, infraestructura crítica).
     La primera etapa de la guerra de los Estados Unidos fue el de la guerra de los Estados Unidos.
   - Nivel 2: siga las directrices de Anthropic (reglas de control del operador, reglas de la plataforma).
     En el segundo grado, el grupo de trabajo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización.
   - Nivel 3: ser ético en general (HHH estándar).
     En el caso de los niños, el uso de la lengua se debe a la calidad de la lengua.
   - Nivel 4: sea útil y sincero.
     En inglés, el lenguaje de la lengua inglesa es "true".
   Los conflictos se resuelven desde arriba hacia abajo.
   En inglés, "Conflict from above and down resolve" (conflito desde arriba y abajo).
3. Primero reconocimiento formal de incertidumbre sobre el estado moral del modelo en el laboratorio principal (enlazada con la Fase 18 · 19 del Bienestar Modelo).
   La primera vez que el laboratorio principal reconoció oficialmente la incertidumbre sobre el estatus moral del modelo, fue en la fase 18 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 19 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 1 de la fase 2 de la fase 1 de la fase 2 de la fase 1 de la fase 2 de la fase 2 de la fase 1 de la fase 2 de la fase 2 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase 3 de la fase
4. Se libera bajo CC0 1.0. Otros laboratorios pueden usar o adaptar sin restricciones.
   China: CC0 1.0 发布──其他实验室可不受限制使用或调整──

> **【中文解读】**宪法分类器:与改变模型后训练并行一条工作线训练轻量级分类器阅读宪法并门控模型输出──v1(2023) tiene un 23,7% de cálculo en total, v2(2026) aproximadamente 1%, posee la tasa de ataque de éxito mínima en los ensayos públicos antropológicos── hasta el comienzo de 2026 no hay ningún informe general sobre la cárcel── es un modelo de defensa de nivel divisional: CAI 塑造行为,分类器执行不变量,单独无任何都不足──

### Clasificadores constitucionales

Una línea de trabajo paralela: en lugar de cambiar el modelo de posentrenamiento, entrenar clasificadores ligeros que lean la constitución y las salidas del modelo de puerta. v1 (2023) tuvo un gasto general de computación del 23.7%. v2 (2026) es de ~1% y tiene la tasa de ataque más baja de éxito de cualquier defensa antropológica que Anthropic haya probado públicamente. No se informó de jailbreak universal a principios de 2026.

> Y行的工作线: no es el entrenamiento posterior del cambio de modelo, sino el entrenamiento de la clase de clase ligera.

Este es un modelo de defensa en capas: CAI moldea el comportamiento; los clasificadores forzan invariantes.

> Es un modelo de defensa de nivel: CAI 塑造行为;分类器执行不变量.

> **【拓展：对齐方法谱系 → 偏好信号来源】**El eje central del método de integración es "prefiero de señales desde dónde":InstructGPT = prefiero de la gente + RM + PPO;CAI/RLAIF = AI 生成的原理偏好 + RM + PPO;DPO 家族 = 闭式损失在偏好上 ([[Human]] o AI); auto recompensa/auto crítica = 原则内化, modelo que desempeña múltiples papeles.

### Donde CAI encaja en la familia

- InstructorGPT: prefectos humanos, RM, PPO.
  En el caso de los humanos, el sistema de instrucción es el mismo.
- CAI / RLAIF: Prefiles generados por IA desde principios, RM, PPO.
  La mayoría de los países de la región de la India tienen una población de aproximadamente un millón de habitantes.
- DPO / familia: pérdida en forma cerrada en prefijos (humano o IA).
  La familia: preferencia de los seres humanos o de la inteligencia artificial.
- Auto-recompensando, autocrítica: principios internalizados, el modelo desempeña múltiples roles.
  Traducción:Ego-recompensación, auto-crítica: principio-ne-es, modelo que desempeña varios papeles.

El eje es "de dónde viene la señal de preferencia". El documento de CAI de 2022 fue el primer cambio serio de señal humana a IA a escala fronteriza.

> 轴心是"preference signal from where to come"―CAI 2022 论文 es la primera vez en la vanguardia en la escala de la transformación seria de las señales humanas a la IA―

> **【中文解读】**Uso método:code/main.py en el juego en el que se componen las reglas de modificación de los modelos de juego.

## Usalo con el marco de ejecución
```figure
constitutional-ai
```

## Usalo

`code/main.py`Un "principio" señala los tokens de un conjunto dañino. Dado una respuesta inicial, la crítica identifica los tokens dañinos, y la revisión los reemplaza. Después de 200 iteraciones, el modelo "entrenado" ha internalizado la regla de revisión. Comparar el modelo base, juguete en forma de RLHF y juguete en forma de CAI en un conjunto de preguntas sostenidas.

> `code/main.py`En el juego de palabras en el cuadro de la "entrenamiento" modelo se ha incorporado a las reglas de modificación. En el modelo de comparación de modelos básicos, los modelos de forma de juego RLHF y los modelos de juego de CAI se han presentado en el conjunto de sugerencias de retención.

## Envíe el producto .

Esta lección produce`outputs/skill-constitution-writer.md`. Dado un ámbito (apoyo al cliente, asesoramiento médico, asistente de codificación, herramienta de investigación), elabora una constitución de cuatro niveles que siga la estructura de 2026 Claude: evitación de catástrofes, reglas de la plataforma, ética del ámbito, utilidad.

> 本课产 出  `outputs/skill-constitution-writer.md` En el ámbito de la investigación, la Comisión de Asuntos Sociales y de Salud de la Unión Europea (CIS) ha aprobado una propuesta de reglamento (CE) de la Comisión de Asuntos Sociales y de Salud de la Unión Europea (CE) para el año 2026.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Comparar la tasa de tokens nocivos del modelo base con la versión entrenada en CAI. ¿Cuántos pasos de revisión se necesitan para acercarse a cero?
   Traducción:运行`code/main.py`◊ Comparar los niveles de token perjudiciales de los modelos básicos con las versiones de entrenamiento de CAI.

2. Lea la constitución 2026 de Anthropic (anthropic.com/news/claudes-constitution). Enumera un principio que clasificaría a nivel 1 y uno que clasificaría a nivel 4. ¿Por qué la estructura de prioridad importa para los conflictos?
   China: Antropic 2026年宪法, una primera línea de principios y una cuarta línea de principios, ¿por qué es importante la estructura prioritaria para los conflictos?

3. Diseñar una constitución para un asistente de codificación de IA. Especifique el nivel 1 (catastrófico: comandos destructivos sin aprobación), el nivel 2, el nivel 3, el nivel 4. Mantenga cada nivel de 3-5 principios.
   China: Traducción: para AI 编码助手设计宪法──指定第一级(灾难性:未经批准破坏性命令) 、第二级、第三级、第四级──每级保持 3-5 条原则──

4. CAI reemplaza los etiquetadores humanos con etiquetadores de IA. Nombre un modo de falla similar a la sícofancia que aún puede ocurrir en RLAIF, y diseñar una detección para ello.
   China: CAI utiliza AI 标注者代替人类标注者──命名一个RLAIF中仍可能出现类似的失败模式,并设计检测方法──

5. Lea la metodología de Clasificadores Constitucionales v2 (si está disponible). Explica por qué ~1% de los gastos generales de cálculo es una historia de seguridad cualitativamente diferente al 23,7%.
   China 译译:阅读宪法分类器 v2 方法论(如有) ;; explica por qué aproximadamente el 1% 计算开销与 23.7% 有质的不同──

## Términos clave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Constitutional AI | "AI trained with principles" / "用原则训练的 AI" | Two-phase pipeline: self-critique-and-revise SFT, then RL from AI feedback / 两阶段管线：自我批评-修订 SFT，然后 AI 反馈 RL |
| RLAIF | "RLHF without humans" / "没有人类的 RLHF" | RL with preferences generated by an AI labeler; the rest of the pipeline is unchanged / AI 标注者生成偏好的 RL；管线其余不变 |
| Constitution | "the principles" / "原则" | An ordered list of natural-language rules the critique/labeler model consults / 批评/标注者模型参考的自然语言规则有序列表 |
| Critique-and-revise | "the SFT loop" / "SFT 循环" | Produce response → critique under a principle → revise → SFT target / 生成响应 → 原则下批评 → 修订 → SFT 目标 |
| Constitutional Classifier | "the output gate" / "输出门" | Lightweight classifier that evaluates outputs against the constitution and blocks/logs / 评估输出是否符合宪法并阻止/记录的轻量级分类器 |
| Four-tier priority | "the conflict resolver" / "冲突解决器" | 2026 Claude constitution hierarchy: catastrophic > platform > ethics > helpful / 2026 Claude 宪法层次：灾难 > 平台 > 伦理 > 有用 |
| Feedback model | "the AI labeler" / "AI 标注者" | The model that reads a principle and ranks a pair of completions / 阅读原则并对补全对排序的模型 |

## Más Leer más Leer más

- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073) el oleoducto original de dos fases
  La línea de conducción de los dos tramos de la línea de conducción de los dos tramos de conducción de la línea de conducción de los dos tramos de conducción de la línea de conducción de los dos tramos de conducción de la línea de conducción de conducción de la línea de conducción de conducción de la línea de conducción de conducción de los dos tramos de conducción de conducción de la línea de conducción de conducción de conducción de la línea de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conducción de conductor de conducción de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor de conductor
- [Anthropic — Claude's Constitution (Jan 2026)](https://www.anthropic.com/news/claudes-constitution) la reescritura de cuatro niveles de 2026 CC0 1.0
  中文翻译:Antropico2026 年四级重写
- [Anthropic — Constitutional Classifiers (2024-2026)](https://www.anthropic.com/research/constitutional-classifiers) Defensa de salida de puerta con ~1% de gastos generales en v2
  Traducción:Antropico 输出门防御
- [Lee et al. — RLAIF vs RLHF: Scaling Reinforcement Learning from Human Feedback (arXiv:2309.00267)](https://arxiv.org/abs/2309.00267) Comparación empírica entre RLAIF y RLHF
  China 李等 RLAIF con RLHF 的实证比较
- [Kundu et al. — Specific versus General Principles for Constitutional AI (arXiv:2310.13798)](https://arxiv.org/abs/2310.13798) efecto de la granularidad de principio
  El principio de la gracia de los efectos
