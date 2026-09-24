# Teoría de la mente y la coordinación emergente

> Li et al. (arXiv:2310.10701) mostraron que los agentes de LLM en una exposición de juego de texto cooperativa **emergent high-order Theory of Mind**(ToM)  razonamiento sobre lo que otro agente cree sobre las creencias de un tercer agente  pero falla en la planificación de largo horizonte debido a la gestión del contexto y alucinación. Riedl (arXiv:2510.05174) midió la sinergia de mayor orden en una población y encontró que **only**La condición de ToM-prompt produce diferenciación vinculada a la identidad y complementariedad orientada a objetivos; los LLM de menor capacidad muestran sólo una aparición falsa. Es decir, la aparición de la coordinación es prematura y condicional y depende del modelo, no gratuita. Esta lección implementa un agente minimal consciente de ToM, ejecuta una tarea de cooperación con y sin Invitación de ToM, y mide el delta de coordinación en relación con el protocolo Riedl 2025.

> **【中文解读】**Este capítulo presenta el mecanismo de coordinación de la teoría de la inteligencia del agente comprensión y predicción de otros agentes de intención.

> **【拓展：theory of mind coordination→具体应用】**La teoría de la mente es la capacidad de comprender y predecir el estado mental de los demás. En el sistema de muchos agentes, el agente con teoría de la mente puede coordinar mejor que sabe que otros agentes saben lo que quieren y lo que harán. Los estudios de 2025-2026 muestran que las intenciones de otros agentes pueden mejorar significativamente la eficiencia de coordinación, pero también aumentan los costos de cálculo.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·07(辩论) 、Fase 16·17(生成式代理) 、认知科学 概念思想理论──ToM = Agent 推理"其他 Agent 在想什么"──
> ¿ Qué es esto ?**【类比】**ToM = "Agent de la compañera de la mente"──no ToM Agent = auto-declararse;有 ToM Agent = 站在對方角度思考" él cree que yo sé esto?
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

La coordinación multi-agente a menudo parece mágica: los agentes dividen el trabajo, se anticipan entre sí, evitan la redundancia. Por lo general, esta "emergencia" es un artefacto de la ingeniería de la rapidez  alguien dijo a los agentes que "coordenaran".

> Más agente  coordinación suele parecer muy maravilloso: agente divide trabajo ¦ prejuicio mutuo ¦ evitar redundancias ¦ normalmente este tipo de "emergencia" es un producto del proyecto  alguien le dice al agente ¦ coordinar ¦ eliminar la sugerencia, coordinar desaparece ¦

El hallazgo de Riedl para 2025 es más estricto: en condiciones controladas, la coordinación sólo surge cuando se invita a los agentes a razonar sobre **other agents' minds**(ToM). Sin el comando de mando, incluso los modelos fuertes muestran patrones de coordinación que no sobreviven a los controles estadísticos.

> El proyecto de ley de 2025 se encuentra más estricto: en condiciones de control, coordinar sólo en el agente se le pide que se recomiende**其他 Agent 的心理**(ToM) tan sólo surgió. No hay ningún tipo de sugerencias, incluso los modelos fuertes también muestran un modelo de coordinación bajo control estadístico inexistente. Esto es importante para la producción: la función de "multi-agente 协调" de la publicación del equipo depende de la sugerencia y es vulnerable.

Esta lección trata a ToM como una capacidad específica (razonar sobre creencias sobre creencias), construye un agente consciente de ToM mínimo, y mide cómo se ve la coordinación real frente a cómo se ve el vestir rápido.

> Este curso se va a considerar el TOM como una capacidad específica de evaluar las creencias sobre las creencias, construir un mínimo de TOM percepción de agente, y medir la diferencia entre la coordinación real y el diseño de la sugerencia.

## Concepto de la esencia de la concepción

### Qué significa ToM

Psicología del desarrollo: un niño de 3 años piensa que el mundo interior de cualquier persona coincide con el suyo. Un niño de 5 años entiende que los demás tienen creencias diferentes. Un niño de 7 años explica las creencias sobre creencias ("cree que creo que la pelota está bajo la copa").

> 发展心理学: un niño de 3 años cree que el mundo interior de cualquier persona es igual a él mismo. Un niño de 5 años entiende que los demás tienen diferentes creencias. Un niño de 7 años piensa sobre las creencias.

Para los agentes de LLM, ToM ordena un mapa a:

> 对于LLM Agent,ToM 阶次映射到:

- **Zeroth-order:**El agente actúa sólo por sus propias observaciones.
  En inglés:**零阶：**No hay modelo de otro. Sólo se basa en sus propias observaciones.
- **First-order:**"Alice cree en X".
  En inglés:**一阶：**El agente tiene un modelo de creencia para cada otro agente.
- **Second-order:**"Alice cree que Bob cree en X".
  En inglés:**二阶：**"Alice cree en Bob cree en X".

Li et al. 2023 encontraron que los ToM de primer y segundo orden emergen en los agentes de LLM en juegos cooperativos, pero se degradan con un horizonte largo y una comunicación poco confiable.

> Li 等人, en el año 2023 encontró que la primera y segunda fases de la gestión de la gestión de la gestión de empresas en el campo de la gestión de empresas en el mercado de la gestión de empresas se han extendido, pero en el largo plazo y en el ámbito de la comunicación no fiable se han reducido.

### La prueba Sally-Anne, en resumen

Una prueba de creencia falsa de 1985: Sally pone un mármol en la cesta A, se va. Anne lo mueve a la cesta B. ¿Dónde mirará Sally cuando regrese?

> 1985                                                                                                                                                                                                                                                               

Los LLM de la era GPT-4 pasan pruebas de estilo Sally-Anne cuando se presentan claramente. Fallan cuando la narrativa es larga, la escena cambia varias veces o la pregunta se expresa indirectamente. Ese es el estado práctico de ToM en 2026 en los LLM de producción.

> GPT-4 时代的LLM 在直接问时通过Sally-Anne 风格测试――当叙述很长,场景多次变化或问题间接表达时失败――这是2026年生产LLM中 ToM的实际状态――

### La medición de coordinación de Riedl

Riedl (arXiv:2510.05174) construyó una prueba a escala de población: N agentes, un objetivo cooperativo, condiciones de prontitud variables.

> Riedl(arXiv:2510.05174) construyó grupos de tamaño测试:N 个 Agent,合作目标,可变提示条件――测量:

1. **Identity-linked differentiation.**¿Los agentes desarrollan distinciones estables de roles con el tiempo?
   En inglés:**身份关联分化。**¿El agente tiene un papel diferente?
2. **Goal-directed complementarity.**¿Las acciones de los agentes se complementan entre sí (subtareas diferentes) en lugar de duplicarse?
   En inglés:**目标导向互补性。**¿El comportamiento del agente es complementario y no repetitivo?
3. **Higher-order synergy.**Una medida estadística de si el grupo logra lo que ningún subconjunto podría.
   En inglés:**高阶协同。**¿Acaso el grupo ha alcanzado una estadística que ningún grupo puede alcanzar?

Resultado: sólo bajo la condición de la llamada de ToM las tres métricas producen una señal por encima del nivel de referencia. Sin la llamada de ToM, las métricas se desplazan cerca de la posibilidad para los modelos de capacidad moderada. Los modelos grandes muestran cierta coordinación sin la llamada de ToM explícita pero el efecto es menor que con la llamada explícita.

> 结果: sólo en condiciones de 提示 ToM, tres indicadores producen más alto que la línea de base de la señal.  Cuando no hay 提示 ToM, el indicador de un modelo de capacidad media se encuentra cerca del nivel de la manera.  Cuando el modelo grande no tiene un claro 提示 ToM muestra algunas coordenadas, pero el efecto es menor que el claro 提示.

### La ilusión de coordinación

Sin controles estadísticos, la "coordinación de emergencia" en las demostraciones a menudo refleja:

> 没有统计控制, la "涌现协调" de la demostración suele reflejarse en:

- Ingeniería rápida que se colabora en coordinación (compulsaciones del sistema que dicen "trabajar juntos").
  En inglés, "sistemas de trabajo" se dice "trabajo" en inglés.
- Prejuicio observador (vemos patrones que esperamos).
  En el caso de los observadores, el cambio de paradigma es el mismo que en el caso de los observadores.
- Selección post hoc de carreras exitosas.
  El éxito de la carrera

Los sistemas de producción que comercializan "coordinación emergente" sin señal medible deben ser tratados como comercializados.

>  no hay señales de medición en el sistema de producción de la propaganda de "emergencia coordinada" debe ser considerado como un marketing―precedente de medición reafirmación―

### Un agente minimalista consciente de TOM

Estructura:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

El `other_models`El atributo es el estado ToM. El primer orden ToM mantiene sólo un nivel.`other_models[i][other_models_of_j]`¿Qué creo que cree el agente J?

### Por qué lastimaría el largo horizonte

Li et al. documento: los límites de contexto hacen que los agentes olviden cuál creencia pertenece a quién. La alucinación agrega creencias falsas a los modelos de otros agentes. Ambos producen errores "Pensé que pensó X" que se componen con el tiempo.

Las medidas de mitigación documentadas en el documento y en los seguimientos de 2024-2026:

- **Explicit ToM state in the prompt.**Formatos estructurados: `{agent_id: belief_list}`- Forza la recuperación para preservar la vinculación entre la identidad y la creencia.
- **Shorter reasoning chains.**Menos actualizaciones de ToM por turno reducen las alucinaciones compuestas.
- **External ToM store.**Mantenga el modelo fuera del contexto del MLL; inyecta solo partes relevantes por turno.

### Cuando el ToM falla en la producción

- **Adversarial settings.**Los agentes con buena ToM son más fáciles de manipular (puedes modelar lo que ellos modelaran de ti, luego explotarlo).
- **Heterogeneous teams.**Cuando los modelos son diferentes, el modelo ToM que funciona para un oponente no generaliza.
- **Ground-truth-dependent tasks.**El TOM se trata de creencias; si la corrección depende de los hechos, el TOM puede ser una distracción.

### La coordinación que realmente se puede medir

Tres señales prácticas de que la coordinación de un equipo es real en lugar de vestida de inmediato:

1. **Complementarity over time.**¿En una tarea de varios turnos, las acciones de los agentes cubren subtareas disjoint?
2. **Anticipation.**¿La acción del agente A en la vuelta T+1 depende de una predicción sobre la acción de B en T+2 que resultó correcta?
3. **Correction.**Cuando A interpreta mal la creencia de B en la curva T, ¿corrige A con la curva T + 2?

Estos son medibles en un sistema de múltiples agentes registrados. Son la versión sustancial de la narrativa de "coordinación".

## Construye con movimiento.
```figure
sw-theory-of-mind
```

## Construye el mismo

`code/main.py`los instrumentos:

- `ToMAgent` rastrea sus propias creencias y modelos de creencias por otro agente.
  En inglés:`ToMAgent` Seguir sus propias creencias y el modelo de creencias de cada otro agente.
- Una tarea cooperativa: tres agentes deben recoger tres tokens de tres cajas; cada caja puede contener un token.
  En inglés, tres agentes deben recoger tres tokens de tres cajas; cada caja sólo puede poner un token.
- Dos configuraciones: `zeroth_order`(no ToM) y `first_order`(TOM con modelo de creencias de un nivel).
  Traducción: dos clases de configuración:`zeroth_order`(no tiene que ser) y `first_order`(带一层信念模型的 ToM)
- Medición de más de 200 ensayos aleatorios: tasa de finalización, tasa de duplicación (dos agentes dirigidos a la misma caja), promedio de vueltas hasta la finalización.
  La medida de los ensayos de composición es de la siguiente manera:

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado esperado: los agentes de orden cero duplican el esfuerzo a una tasa de ~ 35% y completan ~ 60% de los ensayos en 10 vueltas.

> 预期输出: Zero阶级代理以约35%的比例重复工作并完成约60%的试验在10轮内――一阶级TOM代理以约5%的比例重复并完成约95%――差异就是可测量的协调效果――

## Usalo.

`outputs/skill-tom-auditor.md`Es una habilidad que audita la afirmación de un sistema multiagente de "coordinación emergente".

> `outputs/skill-tom-auditor.md`Es una habilidad de un auditor multi-agente sistema de "emergencia coordinada" declaración ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙  ∙  ∙  ∙  ∙     ∙                                                                                                                                                                                                                                                                                                     

## Envíalo .

Lista de verificación de las reclamaciones de coordinación:

- **Control condition.**Una versión de tu sistema sin la llamada de coordinación.
  En inglés:**对照条件。**没有协调提示的系统版本──两者都测量──
- **Statistical test.**¿Es significativa la diferencia entre el sistema y el control en `p < 0.05`¿En su métrica?
  En inglés:**统计测试。**¿Está la diferencia entre el sistema y la luz en su indicador?`p < 0.05`¿Highland es significativo?
- **Complementarity measure.**Desajuste de acción con el tiempo, no sólo el éxito final.
  En inglés:**互补性测量。**随时间的动作不交性, no sólo es el éxito final.
- **Failure-case log.**Cuando los agentes se coordinan mal, ¿cómo se ve el estado de ToM?
  En inglés:**失败案例日志。**Cuando el agente coordina fallo, ¿cómo es tu estado?
- **Model-capacity disclosure.**Si el efecto desaparece en modelos más pequeños, dígale.
  En inglés:**模型能力披露。**Si el efecto desaparece en un modelo más pequeño, explica esto.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar el primer orden de ToM reduce la tasa de duplicación en ~7x. ¿Persiste la brecha cuando escalas a 5 agentes y 5 cajas?
   Traducción:运行`code/main.py`¿Confirmará la primera fase de la TCM que la tasa de repetición se reducirá aproximadamente 7 veces? ¿Expandiéndose a 5 agentes y 5 cajas?
2. Implementar el ToM de segundo orden (el agente A modela lo que B piensa de C). ¿Mejora en relación con el primer orden?
   Traducción: ¿Ha mejorado el proceso en comparación con el primero? ¿En qué tarea?
3. Inyectar una**hallucination**en el estado de ToM: al azar invertir una creencia por turno. ¿Cuánto degrada este rendimiento de primer orden?
   En español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés;**幻觉**¿Cuánto disminuirá el rendimiento de una etapa?
4. Lee Li et al. (arXiv:2310.10701). Reproduce el hallazgo de "degradación de horizonte largo": a medida que los turnos crecen de 10 a 30, ¿cómo cambia su rendimiento de primer orden ToM?
   En el caso de los primeros años de la industria, el aumento de la producción de productos de la industria de la industria de la producción de productos de la industria de la industria de la producción de productos de la industria de la industria de la producción de la industria de la producción de productos de la industria de la industria de la producción de la industria de la industria de la producción de productos de la industria de la industria de la producción de la industria de la industria de la producción de la industria de la industria de la industria de la producción de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la industria de la del sector de la industria de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector de la del sector.
5. Leer Riedl 2025 (arXiv:2510.05174). Implemente las estadísticas de sinergia de orden superior en sus registros de simulación. ¿El efecto está presente sin la condición de ToM prompt?
   En el libro de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de Jesús, ¿?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Más Leer más Leer más

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) ToM emergente en juegos cooperativos; modos de fracaso de largo horizonte
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) medición a escala de población; la incidencia de ToM es la condición de carga
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) el origen del concepto de TOM en 1978
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://doi.org/10.1016/0010-0277(85)90022-8)  el artículo Sally-Anne (1985)
