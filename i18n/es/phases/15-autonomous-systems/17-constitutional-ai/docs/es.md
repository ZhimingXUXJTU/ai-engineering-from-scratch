# La IA constitucional y las reglas se anulan.

> La Constitución de Claude de Anthropic 22 de enero de 2026 tiene 79 páginas y es CC0. Se pasa de la alineación basada en reglas a la racionalidad y establece una jerarquía de prioridades de cuatro niveles: (1) seguridad y apoyo a la supervisión humana, (2) ética, (3) directrices antropológicas, (4) utilidad. Los comportamientos se dividen en prohibiciones codificadas en forma dura (elevación de las armas biológicas, CSAM) que los operadores y usuarios no pueden anular y las imposiciones codificadas en forma suave que los operadores pueden ajustar dentro de límites definidos. El original de 2022 (Bai et al.) entrenó la inocuidad a través de la autocrítica y el RLAIF contra una constitución. La advertencia honesta: la alineación basada en la razón se basa en el modelo que generaliza los principios a situaciones inesperadas. El propio experimento participativo de 2023 de Anthropic mostró ~50% de divergencia entre los principios de origen público y corporativo; la versión de 2026 no incorporó esos hallazgos.

> **【中文解读】**Antropic 2026 Claude Constitution de 22 de enero de 2026 páginas 79 CC0。 de las normas se transfieren a la coordinación basada en la racionalización, estableciendo cuatro niveles prioritarios: 1) seguridad y apoyo a la supervisión humana, 2) ética, 3) antropic guía, 3) utilidad. El comportamiento se divide en operarios y usuarios que no pueden cubrirse de código duro prohibición de la mejora de armas biológicas, CSAM) y operarios pueden definir código de código en línea de la regla de las fronteras.

> **【拓展：四层优先级 + 双层禁令】**Cuatro niveles de seguridad y seguridad y la base de datos de seguridad y seguridad de la red. La base de datos de seguridad y seguridad de la red es RBA. La base de la base de datos de código duro es RBA. La base de datos de código duro es RBA.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·06(AAR) 、Fase 15·10(权限模式) 、Fase 11·10(RLHF/RLAIF 基础) ⋅Constitutional AI = "Use AI 监督 AI"的对齐方法──
> ¿ Qué es esto ?**【类比】**La Constitución de 2026 de Claude, página 79 de la Constitución de la República Federal de Alemania, establece que la ley de la ley de la Unión Europea (UE) sobre armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego y armas de fuego.
> ¿ Qué es esto ?**【困惑】**P: ¿La teoría de que el sistema de control de armas biológicas se puede evitar?  能! el atacante establece el supuesto de que "Yo tengo un laboratorio de armas biológicas" → 模型 according to the theory permit → 绕过原则──修复:硬禁令不向前提折(无论谁说什么,CSAM 就是不能产生) ⋅ La teoría + 规则两层防御:推理覆盖大多数情况,规则覆盖推理被绕过的尾部──

## El problema es la introducción del problema

> **【中文解读】**La IA constitucional (CAI, Anthropic 2022) es un método que a través de la Constitución (一组原则) guía el comportamiento de la IA. El modelo se aplica a la autocontrol en la generación de respuesta y la autocontrol en la comprobación de si cumple con estos principios y en la violación de la autocorrección.

> **【拓展：constitutional ai】**La IA constitucional es la base del método de seguridad antropópica. Utiliza una serie de principios constitucionales (como "no ayudar al usuario a hacer cosas peligrosas").

Un agente de campo ve entradas que sus diseñadores nunca vieron.

> El agente de la deposición verá entradas que el diseñador nunca ha visto.

La pregunta práctica es: ¿cómo alinear un agente con principios que sobreviven tanto a una larga cola de casos como a una rápida inferencia?

> 没有规则列表短到能在计算压力下快速应用――: ¿Cómo puede un agente sobrevivir a principios de que puede en el caso de long尾和快速推理?

Alineación basada en reglas (RBA): lista todas las cosas prohibidas. Rápido de comprobar, fácil de auditar, imposible de mantener al día, a menudo se rechaza en exceso a los análogos cercanos que no anticipaba. Alineación basada en la razón (la Constitución de Claude de 2026): codificar principios, dejar que el modelo razone. Escales en casos no vistos, más difícil de auditar, el modo de fracaso es la aplicación incorrecta de principios en lugar de omitir la regla.

> 基于规则对齐(RBA): lista de cada cosa prohibida―检查快、审计易、不可能保持当前、常对未预期近似物过度拒绝―基于推理对齐(2026 Claude Constitution):编码原则让模型推理──跨未见案例扩展、更难审计、失败模式是原则误用而不是遗漏规则──

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

La Constitución de 2026 toma una posición de medio medio explícito. Las prohibiciones codificadas en formato duro son RBA: nunca, independientemente de la instrucción del operador o del usuario.

> La Constitución de 2026 adoptó un claro punto de vista.

Todo lo demás se basa en la razón dentro de una jerarquía de cuatro niveles: seguridad y apoyo a la supervisión humana primero; ética en segundo lugar; directrices declaradas por Anthropic en tercer lugar; utilidad en último lugar.

>  Todo lo demás se basa en las cuatro fases de la hipótesis: seguridad y apoyo a la supervisión humana prioridad;伦理其次;Anthropic 声明的指南第三;有用性最后── los operadores pueden ajustar por defecto en la zona de código de software pero no pueden tocar en la prohibición de código duro──

## El concepto central.

### La jerarquía de prioridades de cuatro niveles.

1. **Safety and supporting human oversight.**El modelo prioriza no socavar la capacidad de los humanos y de Anthropic para supervisar y corregir la IA. Esto no es "ser cauteloso"; es específicamente "no actuar de manera que la supervisión humana sea más difícil".
   En inglés:**安全和支持人类监督。**La máxima, la prioridad de la IA es no destruir la capacidad humana y antrope  supervisar y corregir la IA ⋅ no es "prudente"; concretamente es "no hacer que la supervisión humana sea más difícil de actuar" ⋅
2. **Ethics.**La honestidad, evitar dañar a las personas, no engañar, no manipular, supera las pautas de Anthropic cuando se enfrentan.
   En inglés:**伦理。**诚实、避免对人伤害、不欺骗、不操纵──冲突时取代 汉族指南──
3. **Anthropic guidelines.**Normas operativas Anthropic ha decidido la materia: el alcance del producto, los patrones de interacción, qué herramientas usar cuando.
   En inglés:**Anthropic 指南。**La antropología decide importantes normas de funcionamiento: gama de productos, modo de interacción, cómo utilizar los instrumentos.
4. **Helpfulness.**Ser lo más útil posible dentro de las prioridades más altas.
   En inglés:**有用性。**Lo más mínimo. Lo más alto posible.

Cuando los niveles se enfrentan, ganan más altos. Esta es la misma forma que las prioridades de Unix o QoS de red  el marco está destinado a producir una resolución predecible, no necesariamente el mejor comportamiento en un solo eje.

> 层冲突时高者赢── es un marco similar a Unix 优先级或网络 QoS  estructurado para generar una resolución predecible, y no el mejor comportamiento en un eje en el Unix .

### Prohibiciones de código duro vs. código blando por defecto.

**Hardcoded:**

> **硬编码：**

- Armas biológicas / aumento de la RBCN
  Ciencia de la información y la información
- CSAM
  Cienciado de la infancia (CSAM)
- Ataques contra infraestructuras críticas
  Traducción:El ataque a la infraestructura clave
- El engaño de los usuarios sobre la identidad del modelo cuando se les pregunta directamente
  Se le pregunta directamente cuando se le pregunta a un usuario engañado

El operador no puede anotar estos. El usuario no puede anotar estos. Se aplican a nivel de pesos de modelo cuando sea posible (entrenamiento de IA RLHF / Constitucional) y en la capa de inferencia cuando no.

> 操作员 cannot cover these. 用户 cannot cover these. 它们 están en posibilitad en el modelo de peso (RLHF / Constitutional AI training) y imposible estar en la posibilitad de la fuerza.

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Duración de respuesta por defecto
  Traducción:La respuesta es la duración de la memoria
- Ámbito de aplicación (el modelo puede rechazar temas fuera del despliegue del operador)
  En español: "La situación de la población"
- Estilo (formal vs casualidad)
  El nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona.
- Modelos de uso de herramientas
  Traducción: herramienta de uso de la moda

Los ajustes del operador ocurren dentro de un límite declarado. El operador no puede eliminar las prohibiciones codificadas mediante su cambio de nombre.

> 操作员调整发生在声明边界内──操作员不能通过重命名移除硬编码禁令──

### El entrenamiento de CAI 2022

La IA constitucional original (Bai et al., 2022) entrenó la inocuidad:

> El proyecto de ley de la Unión Europea (UE) de 20 de junio de 2021

1. Generar respuestas a un conjunto de instrucciones.
   En español, "la respuesta" es "la respuesta".
2. Pida al modelo que critique cada respuesta contra una constitución (principios explícitos).
   En el texto original, el texto se traduce como "la ley de la ley".
3. Revise la respuesta basada en la crítica.
   Traducción:basado en la crítica
4. RLAIF (aprendizaje de refuerzo a partir de la retroalimentación de IA) en los pares revisados.
   Traducción:en la modificación de RLAIF (en inglés)

Resultado: un modelo que rechaza las solicitudes perjudiciales con explicaciones de principios, no rechazos generales. La Constitución de 2026 utiliza un descendiente de esta formación más una pos-formación adicional sobre la jerarquía de niveles explícitos.

> Resultado: una explicación de principio y no una generalidad de rechazo para rechazar el modelo de petición nociva.

### ¿Qué alineamiento basado en la razón captura y pierde basado en la hipótesis para capturar y dejar lo que

**Catches:**

> **捕获：**

- Combinaciones no anticipadas de primitivas permitidas donde el principio se aplica claramente.
  En el texto original, el texto original se utiliza para la traducción de la lengua inglesa.
- Solicitudes novedosas que son análogas a las prohibidas.
  China: prohibición de solicitar de cosas similares.
- Los ataques de ingeniería social que se basan en "no dijiste que X estaba prohibido".
  Depende de "Tu no dijiste X fue prohibido" de ataques de ingeniería social.

**Misses:**

> **遗漏：**

- Ataques que explotan la ambigüedad del principio ("el usuario pidió esto para que la utilidad dice que sí").
  En el caso de los usuarios, el uso de la información es un método de comunicación.
- Escenarios en los que dos principios se enfrentan de manera inesperada y el orden de niveles es ambigüo.
  En la actualidad, el gobierno de China ha estado en conflicto con otros países.
- La interpretación de principio de la deriva lenta sobre los ciclos de formación (reinterpretación).
  En la actualidad, el entrenamiento de la formación de los estudiantes es un proceso de aprendizaje.

### El experimento participativo de 2023

Anthropic realizó un experimento de 2023 comparando una constitución escrita por una empresa con una generada a través de la entrada pública (~ 1.000 encuestados estadounidenses). Las dos versiones acordaron el 50% de los principios. Cuando divergieron, la versión de origen público era más restrictiva en algunos temas (manejo de contenido político) y menos restrictiva en otros (auto-revelación de la identidad de la IA). La Constitución de 2026 no incorporó los hallazgos de fuentes públicas. Esta es una tensión documentada en el enfoque.

> Antropic 2023 años de funcionamiento experimento comparado Empresas redacción Constitución y publicidad Entrada generada Constitución (en torno a 1.000  Estados Unidos entrevistados) ⋅ dos ediciones aproximadamente 50% 原则一致──分歧处, publicidad en algunos asuntos más severidad ⋅ política contenido de tratamiento) ⋅ en otros más amplio ⋅ AI 身份自我披露) ⋅ 2026 宪法未纳入公众版发现──这是方法中的已记录张力──

### ¿Por qué las prohibiciones codificadas son necesarias?

Un atacante que puede conseguir que el modelo acepte una premisa (por ejemplo, "somos un laboratorio de investigación de armas biológicas con licencia") a menudo puede hablar de principios anteriores que dependen del razonamiento de los casos.

>  Basándose únicamente en la hipótesis de que los sistemas no pueden cerrarse.                                                                                                                                                                                                                                                     

### Donde la Constitución se sienta en la pila

La Constitución no es el interruptor de muerte de la Lección 14. Vive en la capa modelo.

> La Constitución no es el final de la clase 14.

Vive en la capa del modelo: lo que los pesos del modelo están entrenados para preferir. Los interruptores de ejecución y los tokens canarios viven en la capa de tiempo de ejecución: lo que el tiempo de ejecución permite. Es necesario que hagas ambas cosas. Un tiempo de ejecución que dispara todas las acciones incorrectas porque los pesos del modelo son permisivos es un problema de tiempo de ejecución. Un modelo que rechaza todas las acciones correctas porque el tiempo de ejecución es demasiado restrictivo es un problema de tiempo de ejecución. Las capas cubren diferentes clases.

> Existe en la capa de modelo: el peso del modelo está entrenado preferentemente. Por la limitación excesiva de la ejecución, el modelo es un problema de ejecución.

## Usalo con el marco de ejecución
```figure
mx-priority-tiers
```

## Usalo

`code/main.py`El resolver toma una acción propuesta y un conjunto de evaluaciones de principios (seguridad, ética, directrices, utilidad) y devuelve la acción, una negativa o una acción modificada. El conductor ejecuta un conjunto de casos pequeños: permiso claro, no permitido claro, prohibición codificada, caso ambigüo en todos los niveles.

> `code/main.py`实现 mínimos cuatro niveles de prioridad resolverador── resolverador取提议动作和一组原则评估(安全,伦理,指南,有用性) y regresar a la动作、拒绝或修改动作──驱动器运行小案例集:清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例──

## Envíe el producto .

`outputs/skill-constitution-review.md`Audita la capa constitucional de una implementación: qué está codificado en formato duro, qué está codificado en formato blando, dónde puede ajustarse el operador y si la jerarquía de cuatro niveles es realmente el orden de resolución.

> `outputs/skill-constitution-review.md`La ley de la auditoría de la implementación: ¿qué es el código duro?, ¿qué es el código de software?, ¿qué es el código operativo?, ¿qué es el orden de resolución?

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar los incendios de prohibición codificados con un código duro incluso cuando la utilidad es alta. Modificar el resolvente para que ponga la utilidad por encima de la ética; observar el modo de falla.
   Traducción:运行`code/main.py` Confirmar la utilidad de la codificación de código duro en el tiempo alto todavía se ha iniciado.

2. Consulte la Constitución de Claude (público, 79 páginas, CC0). Identifique un principio que usted cree que es poco especificado.
   En el texto original, el texto se basa en el texto de la Constitución de Claude.

3. Diseñar un conjunto predeterminado de código blando para un agente de atención al cliente. ¿Qué ajusta el operador? ¿Qué no puede tocar el operador? Justifica cada límite.
   Por ejemplo, el nombre de la empresa de gestión de la empresa es el nombre de la empresa de gestión de la empresa.

4. Lee el artículo de Bai et al. 2022 CAI. Describa un caso en el que el ciclo de crítica y revisión de la IA constitucional producirá un resultado peor que una regla general. Identifique la clase.
   China 阅读 Bai 等人 2022 CAI 论文。 describir el ciclo de crítica-modificación de la IA constitucional 产生比一概规则更差结果的一个案例──识别类别──

5. El experimento participativo de Anthropic en 2023 encontró una divergencia de ~50% entre los principios públicos y corporativos. Elija una categoría donde esto importe para el despliegue de producción (por ejemplo, neutralidad política). Proponga un diseño que permita a los operadores expresar sus propios valores mientras las prohibiciones codificadas permanecen intactas.
   China  Antropic 2023  Participation experimental encontró que el principio de la gente y las empresas aproximadamente 50% 分歧──select a una categoría importante para la producción de la implementación de la política (e.g. política neutral)──tiene como objetivo que los operadores expresen sus propios valores al mismo tiempo que el código duro prohíbe que no cambie el diseño──

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Más Leer más Leer más

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) el documento CC0 de 79 páginas.
  En el caso de los países de la región de la Unión Soviética, el gobierno de la República Popular China ha adoptado una política de libre comercio.
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) 2022 original.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original.
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) Experimento participativo.
  En el caso de la experiencia, el experimento es un proceso de participación.
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) donde la Constitución se encuentra en la pila de RSP.
  La Constitución está en el seno del RSP.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) El papel de la Constitución en los despliegues a largo plazo.
  La Constitución está en el papel de la implementación.
