# Agentes generativos y simulación emergente .

> Park et al. 2023 (UIST '23, arXiv:2304.03442) poblada **Smallville**, una caja de arena de 25 agentes, con una arquitectura de tres partes: **memory stream**(registro de lenguaje natural), **reflection**(síntesis de nivel superior que el agente genera sobre su propio flujo), y **plan**(comportamiento a nivel diario, luego sub-planes). El resultado histórico fue la aparición de la fiesta del Día de San Valentín: un agente sembró con "quiere organizar una fiesta del Día de San Valentín", sin más guiones, produjo invitaciones distribuidas por la población, fechas coordinadas, y la fiesta sucedió  de 24 agentes que comenzaron sin saberlo. Las ablaciones muestran que los tres componentes son necesarios para la credibilidad. Los fallos documentados son errores de norma espacial (entrada en tiendas cerradas, compartido de baños para una sola persona). Esta es la arquitectura de referencia para las simulaciones de agentes y la evaluación social multi-agente en 2026.

> **【中文解读】**Este episodio presenta la experiencia de 25 agentes de IA en una comunidad virtual.

> **【拓展：generative agents simulation→具体应用】**斯坦福的生成式代理 实验(Park et al., 2023) creó 25 agentes de IA en una pequeña ciudad virtual que viven en su propia vida cada día de la vida, su trabajo, su trabajo, su formación de relaciones y su memoria. La innovación central es la estructura de los flujos de memoria. Cada agente se mantiene en orden de tiempo en la secuencia de sus experiencias, a través de reflexión y resumen.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

> ¿ Qué es esto ?**【前置】**Estudiar en el campo de la lengua inglesa. Estudiar en el campo de la lengua inglesa.
> ¿ Qué es esto ?**【类比】**Smallville = "AI 版模拟人生"──25 个 AI 居民各有生活、记忆、计划──情人节派对奇迹: un agente 想办派对→邀请传开→其他人调整日程→派对真发生全是涌现,无脚本──三件套:memory stream(经历日志) + reflexión(自我总结) + plan(日计划)──三者缺一不可,取消任一 agente 行为变得不可信──
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

La mayoría de los sistemas multi-agentes son equipos estrictamente escritos: planes de planificadores, códigos de codificación, revisiones de revisores. Eso funciona para tareas bien definidas. No captura el comportamiento emergente y no scriptado que surge cuando los agentes tienen memoria, prioridades y un mundo abierto. La investigación, la simulación de la sociedad y la IA de juegos cada vez más necesitan este segundo tipo.

> La mayoría de los sistemas de agentes son un equipo de escritos estrechos: planificadores de planificación, codificadores de codificación, revisores de revisión. Esto es válido para definir las tareas definidas. Pero no puede captar como un agente que posee memoria, prioridad y comportamiento no escritos que surgen en el mundo abierto. La investigación, la simulación social y la creciente cantidad de juegos en los que la IA necesita otras clases de comportamiento.

La arquitectura de Smallville es el punto de referencia para ello. Hasta Park 2023, las mejores simulaciones de agentes eran seguidores de guiones superficiales; después de eso, el patrón es el predeterminado para los agentes generativos en mundos abiertos. Si construyes una simulación de agentes en 2026, estás utilizando los tres componentes de Smallville o justificando explícitamente por qué no lo estás haciendo.

> La arquitectura de Smallville es la base de este tipo. Antes de Park 2023, el mejor agente 模拟 es el seguidor de un guión de nivel bajo; después, este modelo se convirtió en el estándar de un agente generado en el mundo abierto. Si construyes un agente 模拟 en 2026, vas a usar los tres componentes de Smallville, explicad claramente por qué no lo usas.

## Concepto de la esencia de la concepción

### Los tres componentes

**Memory stream.**Un registro de observaciones, acciones, reflexiones y planes solo en apéndice. Cada entrada tiene un sello de tiempo, un tipo, una descripción (lenguaje natural) y metadatos derivados: **recency**¿ Qué ?**importance**(auto-valorado entre 1 y 10 por el agente), y **relevance**(similaridad de cosina con la consulta actual).

> **记忆流。**Un solo extra de observación, acción, reflexión y planificación. Cada artículo tiene tiempo, tipo y descripción.**时效性**¿Qué es esto?**重要性**(Agencia 自评 1-10) y**相关性**(Con la similitud de los otros cuerpos de la investigación actual)

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

La recuperación de memoria combina las tres puntuaciones: `score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`Las entradas de arriba-k ingresan en el aviso actual.

**Reflection.**Periódicamente (cada N recuerdos o en eventos importantes), el agente genera síntesis de orden superior de recuerdos recientes. Las entradas de reflexión vuelven al flujo y son recuperables como cualquier otra memoria. Así es como los agentes construyen "entendimientos"  el equivalente de la arquitectura de creencias a largo plazo.

> **反思。**定期(每 N 条记忆或在重要事件时),Agent de la memoria reciente genera un complejo de alto nivel.

**Plan.**Descomposición de arriba hacia abajo. Primero, un plan de día en grandes trazos ("ir al trabajo, cenar con Klaus"). Luego planes a nivel de hora. Luego planes a nivel de acción. Los planes son revisables: cuando una observación contradice un plan, el agente replania el segmento afectado.

> **计划。**Se trata de un plan de trabajo de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la

### ¿Por qué importan las tres cosas (ablación)

Park et al. ejecutaron ablaciones dejando caer cada una de la observación, la reflexión y el plan.

> Park  et al. realizaron experimentos de desintegración, separadamente eliminando observaciones, reflejos y planes.

- Sin ...**observation**El agente pierde el contexto y actúa sobre creencias obsoletas.
  No hay nada**观察**,Agent 缺失上下文, basado en la convicción de que el pasado actúa.
- Sin ...**reflection**El agente no puede formar creencias de orden superior; las interacciones permanecen superficiales.
  No hay nada**反思**,Agent  incapaz de formar la fe de alta clase; 交互保持浅层──
- Sin ...**plan**El comportamiento se convierte en ruido reactivo; los objetivos se disipan.
  No hay nada**计划**, el comportamiento se convierte en un ruido reactivo; objetivo

Los puntajes de credibilidad de los evaluadores humanos son los más altos con los tres; bajar cualquiera produce una regresión medible.

> El índice de credibilidad de los evaluadores es el más alto de todos los tiempos; elimina cualquier deformación que genere una medición.

### El día de San Valentín surge

Una agente, Isabella Rodríguez, es sembrada con el objetivo de "quiere organizar una fiesta de San Valentín en el Hobbs Cafe el 14 de febrero a las 5 pm".

> Una agente, Isabella Rodríguez, fue implantada como objetivo de organizar una fiesta de amor en el Hobbs Cafe. Otros 24 agentes no recibieron semillas como esta.

1. El plan de Isabella incluye invitar a la gente.
   El plan de Isabel incluyó invitar a la gente.
2. Cada invitación se convierte en una observación en la memoria del vecino.
   Cada invitado se convierte en un observador en el flujo de recuerdos vecinos.
3. La reflexión de esa vecina genera creencias: "Isabella está dando una fiesta".
   La idea de que Isabel fuera a la calle fue una de las razones de su muerte.
4. El plan del vecino incluye "asistir a la fiesta el 14 de febrero".
   China: Neighbourhood Plan: "Junto a la ciudad"
5. Los vecinos dicen a los demás vecinos.
   En español, el vecino le dice al vecino otro.
6. A las 5 pm del 14 de febrero, varios agentes convergen en el Hobbs Cafe.
   2 de enero de 14 de enero de 17 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de enero de 15 de agosto de 15 de agosto de 15 de agosto de 15 de agosto de 15 de agosto de 15 de agosto de 15 de agosto de 15 de 2012 en el Hotel Hobbs.

Este es el surgimiento en el sentido técnico: el comportamiento a nivel del sistema (una fiesta) surgió de las interacciones locales (invitaciones bilaterales + planificación individual) sin un orquestrador central.

> Esto es un fenómeno en el sentido técnico: el comportamiento de los sistemas se produce en el contexto de la interacción local, sin un coordinador central.

### Los modos de falla documentados

Park et al. documentan explícitamente:

> Park  et al. explicó:

- **Spatial norm errors.**Los agentes entran en tiendas cerradas. Los agentes intentan usar el mismo baño individual. Los agentes comen en habitaciones no destinadas a comer. El modelo no deducen las normas sociales y físicas solo del medio ambiente.
  En inglés:**空间规范错误。**Agente 走进关闭的商店──Agent 试图使用同一个人浴室──Agent 在非用餐室用餐──模型不能仅从环境推断社会物理规范──
- **Memory overflow.**Las simulaciones profundas causan un aumento en el costo de recuperación de la memoria.
  En inglés:**记忆溢出。**La aplicación de modelos de profundidad ha llevado a un aumento en el costo de la recopilación de memorias.
- **Reflection hallucination.**Las reflexiones pueden inventar relaciones que no existen en el flujo de memoria.
  En inglés:**反思幻觉。**Reflexión: en reflexión se contiene la identificación de la fuente de la memoria y no se encuentra en la búsqueda de la prueba.

Estos son modos de falla relevantes para la producción: cualquier simulación de agente 2026 los hereda.

> Estos son modelos de fracaso relacionados con la producción: cualquier agente de 2026 se parece a todos los que los heredan.

### Reglas de ejecución de tres componentes

1. **Memory is append-only.**Nunca mute una entrada de memoria. Las correcciones son nuevas entradas.
   En inglés:**记忆只追加。**永遠不修改記憶条目──更正是新条目──
2. **Importance scores are cheap.**Llame al LLM para que califique la importancia 1-10 al momento de escribir.
   En inglés:**重要性分数是廉价的。**写入时调用 LLM 评分 1-10──缓存分数──
3. **Retrieval is ranked, not filtered.**Top-k por puntaje combinado; no utilice filtros duros (que pierden contexto).
   En inglés:**检索是排序的，不是过滤的。**按综合分数取 top-k; no use duro过(会丢失上下文)。
4. **Reflection runs periodically.**Trigger cuando la suma de la importancia de los recuerdos sin procesar exceda un umbral (por ejemplo, 150).
   En inglés:**反思定期运行。**Cuando no se ha procesado la memoria la importancia total y supera el valor (por ejemplo, 150)
5. **Plans are revisable.**Cuando una nueva observación contradice un plan, regenera sólo el segmento afectado, no todo el plan.
   En inglés:**计划可修订。**Cuando una nueva observación contradice con un plan, sólo se vuelve a generar la parte afectada, no todo el plan.

### Agentes generativos más allá de Smallville

La literatura de seguimiento 2024-2026 extiende la arquitectura:

> La documentación posterior de 2024-2026 amplió esta estructura:

- **Multi-agent social simulation for policy / market research.**Las poblaciones similares a Smallville simulan el comportamiento del usuario en respuesta a las características.
  En inglés:**用于政策/市场研究的多 Agent 社会模拟。**类似Smalville 的人群模拟用户对功能的响应──比A/B 测试更快;准确性有争议──
- **NPC AI for games.**Los juegos de rol con agentes de Smallville producen líneas de historia emergentes en lugar de misiones guionadas.
  En inglés:**游戏 NPC AI。**带有Smalville Agent  RPG  generar líneas de historia emergentes y no tareas de guionado 
- **Generative-agent evaluation benchmarks.**En lugar de precisión de tarea, la métrica se convierte en credibilidad + coherencia de comportamiento en largos períodos.
  En inglés:**生成式 Agent 评估基准。**En la actualidad, el número de empresas que se han convertido en empresas de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de servicios de alta calidad en el mercado de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la del surtalizada se ha incrementado.

La arquitectura es la referencia. las extensiones intercambian componentes (almacenamiento vectorial para la memoria, reflexión aumentada por recuperación, plan neurosímbolico) pero mantienen la estructura de tres partes.

> La estructura es referencia. La estructura es un conjunto de componentes de memoria, pero mantiene tres partes.

### Por qué esto importa para la ingeniería multi-agente

Smallville es la prueba del concepto de que la aparición de múltiples agentes es barata cuando los componentes son correctos. La arquitectura se ha replicado ahora en modelos de código abierto (los LLM más pequeños pierden credibilidad con gracia, no agudamente).**emergent social behavior**Cualquier sistema que necesite**tight task execution**utiliza los patrones de supervisor / roles / primitivos de antes en esta fase.

> Smallville es un concepto de prueba, que indica que cuando el componente es correcto, el multi-agente surge es barato.**涌现社会行为**El sistema de producción utiliza esta forma.**紧密任务执行**El sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de los primeros tiempos del sistema de control de control de los primeros tiempos del sistema de control de control de los primeros tiempos del sistema de control de control de los primeros tiempos del sistema de control de control de control de los primeros tiempos del sistema de control de control de control de control de los primeros tiempos del sistema de control de control de control de control de los primeros tiempos del sistema de control de control de control de control de control de los primeros tiempos del sistema de control de control de control de control de control de control de control de los primeros tiempos del sistema de control de control de control de control de control de control de control de control de control de control de los primeros tiempos del sistema de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de los primeros tiempos de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de los sistemas de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de

## Construye con movimiento.
```figure
a5-memory-reflection
```

## Construye el mismo

`code/main.py`Implementa los tres componentes en stdlib Python con políticas de agente scripted (sin LLM real).

- `MemoryStream` Registro de apéndice con recuperación de actualidad/importancia/relevancia.
  En inglés:`MemoryStream` 带时效性/重要性/相关性检索的仅额日志──
- `reflect(stream)` Reflexión guionada sobre recuerdos recientes de gran importancia.
  En inglés:`reflect` Reflexión sobre la escritura de los recuerdos de gran importancia reciente.
- `plan(agent_state)` Planes de día y hora basados en las creencias actuales.
  En inglés:`plan`  basado en la creencia actual de los planes de día y hora.
- El guión: 5 agentes. El agente 1 comienza con "fiesta de lanzamiento a las 5 p.m". A través de tiques simulados, la invitación se propaga y los agentes convergen.
  En el tiempo de la presentación, el agente se reunió.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La producción esperada: rastreo de tick por tick. Al final, al menos 3 de los 5 agentes muestran al partido en su plan, y convergen en el lugar de la fiesta. La semilla única produjo la llegada coordinada sin ningún orquesta.

> 预期输出:逐步跟踪―― en el último tiempo, en el último paso, de los 5 agentes, al menos 3 mostraron fiestas en el plan, se reunieron en el lugar de fiestas―, en caso de que una sola semilla no tuviera un organizador, se produjo un coordinado logro―.

## Usalo.

`outputs/skill-simulation-designer.md`diseña una simulación de agente generativo: número de agentes, esquema de memoria, cadencia de reflexión, horizonte de plan y métrica de evaluación.

> `outputs/skill-simulation-designer.md`Diseñar un agente generado 模拟:Agente cantidad 記憶模式 反思頻率 計劃範圍和評估標誌──

## Envíalo .

Reglas para las simulaciones de producción:

- **Memory is the database.**Elige una tienda real (vector DB, Postgres) en escala.
  En inglés:**记忆是数据库。**En la escala de la selección de almacenamiento real de datos, el tamaño de datos se utiliza sólo para el tipo original.
- **Log the retrieval trace.**Para cada acción, registra los recuerdos de la parte superior que lo impulsó.
  En inglés:**记录检索轨迹。**Para cada movimiento, el registro impulsa su memoria superior.
- **Budget per-agent tokens.**El plan de cada agente para recoger + reflejar + plan por tick es O(k) llamadas de LLM. N agentes × T ticks × llamadas por tick pueden enarmar su presupuesto.
  En inglés:**预算每 Agent token。**Cada agente Cada paso de tiempo Requisitos + reflejos +  planes es O(k) veces LLM 调用──N 个 Agent × T 个时间步 × 每时间步调用数可能让你的预算相形见──
- **Compact memory periodically.**Resumen y recorte de poca importancia. La política de retención es una decisión de diseño, no un detalle.
  En inglés:**定期压缩记忆。**摘要和修剪低重要性条目──保留策略是设计决策,不是细节──
- **Detect spatial / social norm violations**La arquitectura no las aprende.
  En inglés:**显式检测空间/社会规范违规。**La arquitectura no las aprenderá.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar que 3+ agentes convergen en la fiesta. ¿Aumentar a 10 ?
   Traducción:运行`code/main.py`¿Confirmará que 3 o más agentes se han reunido para la fiesta? ¿Acaso aumentará a 10?
2. ¿Cómo se ve el comportamiento? Mapa de la conclusión de ablación en Park 2023.
   China: Movimiento de reflexión. ¿Cómo se ve el comportamiento?
3. Introducir un objetivo semillado en competencia ("Klaus quiere dar una charla de investigación a las 5 pm"). ¿Se dividen los agentes o domina un objetivo? ¿Qué lo determina?
   En el caso de los agentes, el objetivo principal es la división de los agentes. ¿Qué es lo que decide?
4. Añadir restricciones espaciales: Hobbs Cafe tiene un máximo de 4 agentes. ¿El manejo de simulación se desbordará con gracia, o se encuentra en el patrón de falla del "baño de una sola persona"?
   ¿Cómo es que el hotel de Hobbs tiene un espacio limitado? ¿Cómo es que el hotel de Hobbs tiene un espacio limitado?
5. Leer Park et al. (arXiv:2304.03442) Sección 6 (experimentos de comportamiento emergente). Identifique un comportamiento no reproducible en su miniatura. ¿Qué componente de la arquitectura necesitaría mejorar?
   En el caso de los parques, el nombre de la estructura es "Park" (Park) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:2304.03442) (ArXiv:24.03442) (ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv:ArXiv: ¿CuálXiv: ¿Cuál? ¿Cuál qué componente de qué componente de qué componente de la estructura es el componente de la estructura es el componente de la estructura es la estructura es la estructura es la estructura es la estructura es la de la estructura es la de la de la de la estructura es la de la que necesita identificar

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Más Leer más Leer más

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) la arquitectura de referencia
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) Lugar de publicación
- [Smallville code release](https://github.com/joonspk-research/generative_agents) implementación de referencia de Python
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) Arte previo para agentes de memoria estructurada
