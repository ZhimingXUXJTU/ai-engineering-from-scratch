# Voto, autoconsistencia y topología del debate

> La agregación más barata: muestra N de agentes independientes, mayoría-voto. Wang et al. 2022 autoconsistencia hizo esto con un modelo muestrado N veces.**heterogeneous**Los agentes para escapar de la monocultura  diferentes modelos, diferentes indicaciones, diferentes temperaturas, diferentes contextos. Más allá de la mayoría de votos, el debate sobre la topología es importante: MultiAgentBench (arXiv:2503.01935, ACL 2025) evaluó la coordinación estrella / cadena / árbol / gráfico y se encontró **graph best for research**AgentVerse (ICLR 2024) documenta dos patrones emergentes  comportamientos voluntarios y comportamientos de conformidad  y la conformidad es tanto una característica (encontrar consenso) como un riesgo (pensamiento grupal, Lección 24).

> **【中文解读】**Este apartado presenta la estructura organizativa de la votación y el debate para tomar decisiones sobre el tema.

> **【拓展：voting debate topology→具体应用】**投票和辩論拓 形形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形    形    形 形       形     形                                                                                                


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·07(辩论) Fase 16·14(BFT 共识) Fase 13·03(CoT de autoconsistencia)  Vote拓 = 多 Agent 决策的几何形状──
> ¿ Qué es esto ?**【类比】**投票拓 = "conferencia de mesa de distribución"──星形 = 圆桌投票(独立);链形 = 接力修改(前面的代理的输出传给下一个);图形 = 圆桌讨论(多轮交互)──MultiAgentBench 结论:图形适合研究任务但有"协调税"──>4 个代理 性价比下降)──异质性是关键不同模型/温度/快速 防单一文化错误──
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

El debate puede mejorar la precisión (Du et al., arXiv:2305.14325). También puede degradarla.

> 辩论可以提高准确性 (Du 等人,arXiv:2305.14325),也可能降低准确性 (Debajo puede mejorar la precisión) 辩论 puede ayudar a depender de cuatro elecciones estructurales:

1. ¿Quién habla con quién (topología).
   El lenguaje de la lengua chino es el idioma de la lengua china.
2. Cuántas rondas (Du 2023: ambas rondas y agentes importan de forma independiente).
   En el año 2023, el número de personas que han sido contratadas para la operación de la empresa es de un total de un millón de personas.
3. Si los agentes son heterogéneos (modelos base diferentes rompen la monocultura).
   En inglés, el nombre de la persona que se ha convertido en un agente es el nombre de la persona que se ha convertido en un agente.
4. Si hay una voz adversaria (steel-manning vs. straw-manning).
   La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.

Los equipos que " ejecutan 5 agentes y votan " en una tarea a menudo regresan frente a un solo agente. Los fracasos no son aleatorios.

> El equipo "se ejecutará 5 agentes y votará" duro añadido a las tareas, de vez en cuando más de un solo agente.

## Concepto de la esencia de la concepción

### Autoconsistencia, línea de base de un modelo único

Wang et al. 2022 ("Autoconsistencia mejora la cadena de razonamiento del pensamiento") muestran el mismo modelo N veces a temperatura > 0 y votan por mayoría en respuestas de la vía de razonamiento. El resultado en GSM8K: ganancias sustanciales con muestras N=40 sobre un solo decodificación codiciosa.

> Wang 等人 2022年 ((("autoconsistencia mejoró la racionalización de la racionalización de la cadena de pensamiento") en condiciones de temperatura > 0 a la misma muestra de modelos N veces, y a la mayoría de votos a la respuesta de la racionalización de la vía de la racionalización.

Limite: la autoconsistencia utiliza un modelo base. Los errores se correlacionan por construcción. Si el modelo tiene un sesgo sistemático, todas las muestras N lo comparten.

> Limites: la autoconformidad utiliza un modelo básico.  Error en la construcción es correlacionado.  Si el modelo tiene una parcialidad sistémica, todos los ejemplos lo comparten.

### Voto multi-agente, extensión heterogénea

Los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los científicos de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de cuíman se han cambianananan (clínrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

> Se trata de un modelo de trabajo que se puede utilizar para la fabricación de productos y servicios de la industria de la información.

El nombre canónico para el debate heterogéneo para 2026 es **A-HMAD** Debate heterogéneo multiagente adversario. No es universalmente adoptado, pero los artículos utilizan el término para "debate de modelos diferentes, que reduce los errores correlacionados del colapso de la monocultura".

> 2026 años de la construcción de la política de la sociedad civil**A-HMAD** Contrarrestabilidad de la diversidad de la cultura 辩论──并非普遍采用, pero el artículo utiliza esta palabra "difusión de diferentes modelos, reducir los errores relacionados de la unidad cultural colaps"──

### Las cuatro topologías

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Estrella: un centro, todos los demás hablan solo con el centro.
Cadena: lineal, cada agente ve la salida de la anterior.
Árbol: jerárquico, utilizado por los sistemas de agentes jerárquicos (lección 06).
Grafico: cualquier a cualquier. Incluye clique totalmente conectado y DAG arbitrarios.

> Estráfico: un centro, todos los demás agentes sólo con el centro diálogo.
> 链形:线性, cada agente 看到前一个代理的输出──类似流水线──
> 树形:层次化, utilizado para la escalado de agentes 系统 (第 06 课)
> 图形: arbitrario hasta arbitrario──incluyendo un grupo totalmente conectado y cualquier DAG──

### El impuesto de coordinación (MultiAgentBench)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) comparó estrellas, cadenas, árboles, gráficos en un conjunto de tareas que incluyen investigación, codificación y planificación.

> MultiAgentBench ((MARBLE,ACL 2025,arXiv:2503.01935) en el conjunto de tareas que incluyen el estudio, codificación y planificación se llevó a cabo un test de base sobre la forma de estrellas, la forma de cadenas, la forma de árboles, y el dibujo.

- **Graph**La topología gana en las tareas de investigación. La información fluye de cualquiera a cualquiera; los agentes pueden criticarse entre sí.
  En inglés:**图形**拓在研究任务中获胜;信息随意流动;Agentes pueden criticarse mutuamente.
- **Star**El centro de filtración y consolidación.
  En inglés:**星形**En respuesta rápida, las tareas de hecho se vencen.
- **Chain**ganancias en oleoductos graduados (refinamiento por etapas).
  En inglés:**链形**En el proceso de progreso de la corriente de agua,
- **Coordination tax**El valor de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de la cuentas de los valores de los valores de los valores de los valores de los valores de la cuentas de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de la cuento de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de la cuento de los valores de los valores de los valores de los valores de los valores de la cuento de los valores de los valores de los valores de los valores de los valores de la cuento de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los cuento de la cuento de los cuento de los cuento de los cuento de los cuento de los cuento de los cuento de los cuento de los cuento de los cu
  En inglés:**协调税**En el gráfico aparecen aproximadamente 4 agentes después.

El límite de 4 agentes es empírico, no fundamental. Reflecta la capacidad de contexto de 2026 LLM: el contexto de cada agente se llena de resultados de pares, y el valor marginal de agregar el agente N + 1 disminuye una vez que todos puedan ver a todos.

> 4 El límite superior del agente es experimental, no fundamental. Reflecta la capacidad de la LLM de 2026: cada agente de arriba abajo lleno de la salida de su compañero, una vez que todos puedan ver a cada uno, añadir N+1                                                                                                                                                                                                                                   

### Estrategias de debate multi-agentes ("¿Deberíamos estar volviéndonos locos?")

ArXiv:2311.17371 es la encuesta de 2023 de estrategias de MAD. Los hallazgos clave replicados por otros: las variantes de MAD que son *estructuralmente similares* a la autoconsistencia (muestreo independiente + agregación) a menudo tienen un rendimiento inferior a la autoconsistencia cuando se utiliza el mismo presupuesto.

> ArXiv:2311.17371 es un resumen de estrategia de MAD de 2023 ⋅ clave de la conclusión que ya ha sido replicada por otros: en la estructura de la MAD  variaciones similares a la autoconformidad ⋅ independent sample + 聚合) en el uso del mismo presupuesto ⋅ MAD en el agente ⋅ real diferente de la estructura y el debate tiene la mayor ayuda en la contraestructura ⋅

### Los patrones emergentes de agenteVerse

El objetivo de la Comisión es garantizar la seguridad de los trabajadores.https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) documenta dos comportamientos que surgen del debate multiagente incluso sin un diseño explícito:

- **Volunteer.**Un agente ofrece ayuda ("puedo dar el siguiente paso") sin ser solicitado.
  En inglés:**自愿者。**Agente 主动提供帮助 ((" puedo hacer el siguiente paso") 有用: dará trabajo al agente con más capacidad para realizar las tareas de su hijo
- **Conformity.**El agente ajusta su postura para que coincida con la de un crítico, incluso cuando el crítico está equivocado.
  En inglés:**从众。**Agente 调整立场以匹配批评者, incluso si el crítico es erróneo.

La conformidad es la razón por la que el debate hasta el acuerdo recompensa a los matones.

> Desde la mayoría de los casos, el "debatido al acuerdo" puede ser el resultado de un esfuerzo de los jueces independientes.

### Heterogeneidad: el botón real que mueve la precisión

Un patrón 2024-2026 en la literatura práctica: intercambiar uno de sus agentes N por un modelo base diferente da una mayor acceleración que aumentar N por 1. La intuición es monocultura  cada nueva fuente de error independiente vale más que una muestra correlacionada adicional.

> Un modelo de la literatura práctica de 2024-2026: cambiar uno de N 个 代理 a un modelo de base diferente en comparación con aumentar N + 1 代理 带来更大的准确率提升──直觉是单一文化 cada nuevo error independent 源比额外相关样本有更多价值──

En el límite, la heterogeneidad supera a la numerosidad. Tres modelos diferentes superan cinco copias de un modelo en la mayoría de las tareas que tienen verdad en el suelo limpio.

> En los casos extremos, la diferencia entre la estructura y el número de victorias. En la mayoría de las tareas con un estándar claro, tres modelos diferentes superan las copias de cinco modelos idénticos.

### Métodos de los jurados

El marco de la Sibyl (citado en la literatura de Minsky-LLM) formaliza un "jurado"  un pequeño conjunto de agentes especializados que refinan las respuestas votando en cada etapa. A diferencia del voto de mayoría simple, un jurado tiene funciones: un agente interexamina, uno proporciona contexto, uno califica la plausibilidad. Los métodos del jurado son un punto medio entre el voto simple (barato, propenso a la monocultura) y el MAD completo (costo, propenso a la conformidad).

> Sibyl  framework (en la literatura de Minsky-LLM 引用) formalizó el "jurígio"一小组专业化代理 通过每阶段投票来改进答案──与简单多数投票不同, el jurado tiene un papel: un agente 交叉质询, uno proporcionar sobre下文, una evaluación razonable── el método del jurado se basa en simple votación(便宜,易单一文化) y completo MAD(昂贵,易从众) entre──

### Cuando el voto con debate domina

- La pregunta tiene la verdad fundamental (hechos, matemáticas, comportamiento de código).
  China: problema tiene respuesta estándar (facto, matemática, código)
- Los agentes pueden acceder a diferentes fuentes o herramientas (la heterogeneidad está disponible).
  En inglés, el nombre de la persona que ha sido contratada para la operación es el nombre de la persona que ha sido contratada.
- Las rondas están delimitadas (2-3 típicamente) y hay un juez o verificador separado.
  China:轮次有界 (normalmente 2-3 radas), tiene un comité independiente o un verificador.
- El presupuesto permite 3-5 agentes. Más allá de 5-7 en la topología gráfica, el impuesto de coordinación domina.
  En el caso de los ejemplos de la economía, el presupuesto permite a 3-5 agentes.

### Cuando el voto con el debate duele

- La pregunta es de opinión, los agentes convergen a la respuesta que parece más segura, no más correcta.
  Traducción:El problema es de opinión. El agente recibe la respuesta más segura, pero no la más correcta.
- Todos los agentes comparten un modelo base.
  China: todos los agentes 共享基础模型──单一文化使共识毫无意义──
- Las rondas son ilimitadas.
  Sin embargo, el nombre de la ciudad se ha extendido hasta el extremo occidental.
- La tarea es simple: un agente único con autoconsistencia en N=5 es más barato y tan preciso.
  En inglés, la función de un agente es más fácil y más precisa.

## Construye con movimiento.
```figure
sw-debate-topology
```

## Construye el mismo

`code/main.py`los instrumentos:

- `run_star(agents, hub, question)` encuestas de cada trabajador, agregados.
  En inglés:`run_star` Centro de consulta para cada trabajador
- `run_chain(agents, question)` refinamiento secuencial.
  En inglés:`run_chain` 顺序改进──
- `run_tree(root, children, question)` jerárquico con agregación de profundidad-2.
  En inglés:`run_tree` 层次化, profundidad 2 聚合──
- `run_graph(agents, question, rounds)`Debate general, rondas limitadas.
  En inglés:`run_graph` Todo el debate, hay una ronda de debate.
- Un dial de heterogeneidad con guión: cada agente tiene un `error_bias`que indique su error sistemático.
  Traducción:El guión de la película tiene una estructura diferente.`error_bias`Indicar su error sistémico.
- Un arnés de medición que ejecuta cada topología en N=3, 5, 7 y informa (acurateza, total_tokens, wallclock_simulated).
  En el caso de los datos de la información, el número de datos de datos de los datos de datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de datos de los datos de los datos de datos de los datos de los datos de datos de los datos de los datos de datos de los datos de los datos de datos de los datos de datos de los datos de datos de los datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de los datos de datos de datos de las redes.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado esperado: una tabla de topología × N → (acurateza, tokens, latencia). El gráfico gana en N=3-5 en las tareas de estilo de investigación; la estrella gana en las tareas de hecho rápido; el gráfico en N=7 muestra el impuesto de coordinación (la latencia se infla más rápido que la precisión).

> 预期输出:拓 × N →(准确率,token,延迟)表格──图形在 N=3-5的研究风格任务上获胜;星形在快速事实性任务上获胜;图形在 N=7 时显示协调税(延迟膨胀快于准确率)

## Usalo.

`outputs/skill-topology-picker.md`es una habilidad que lee una descripción de tarea y recomienda una topología (estrella / cadena / árbol / gráfico), un N (número de agentes), un perfil de heterogeneidad (modelos básicos para usar) y un límite redondo.

> `outputs/skill-topology-picker.md`Es una habilidad, read取任务描述并推拓(星形/链形/树形/图形) 、N(Agent 数量) 、异构配置(使用的基础模型) 和轮次上限──

## Envíalo .

Para cualquier conjunto:

- Comience con**self-consistency at N=5**El modelo base es el más barato.
  Traducción:De un fuerte modelo de base.**N=5 自一致性**Es un poco barato.
- Actualización a **heterogeneous voting at N=3**Si la precisión importa, mide el delta.
  Si el índice de precisión es importante, elevar a**N=3 异构投票**◊ Mejores de aumento de volumen
- Sólo actualizar a **debate topology**si la tarea tiene estructura (investigación, múltiples pasos) y son factibles rondas limitadas.
  Traducción: sólo en tareas hay estructuras (en la que hay una serie de fases) y hay una serie de fases disponibles para ser mejoradas.**辩论拓扑**¿Qué es eso?
- Siempre registren el grupo de minorías. Cuando una minoría está persistentemente en lo correcto, tienen una señal de diversidad.
  Cuando la minoría se mantiene en el tiempo correcto, tienes una variedad de señales.
- "Mejor precisión a 10 veces el costo" es una decisión comercial.
  "Mejor precisión de 10 veces el costo" es una decisión comercial.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Trazar la curva de coordinación-taxa para la topología del gráfico: exactitud vs N, tokens vs N. ¿A qué N se inclina la curva?
   Traducción:运行`code/main.py`◊ dibujar gráficos de la línea de coordinación: exact rate vs N,token vs N∙ la línea de la línea de la línea de referencia está en que N 处拐折?
2. Implementar A-HMAD: tres agentes con prejuicios deliberadamente diferentes. ¿Cómo se compara el mismo prejuicio de base con A-HMAD en el ataque de monocultura de la Lección 14?
   En la actualidad, el grupo de A-HMAD tiene tres agentes con diferentes diferencias de intenciones.
3. Añadir un papel de "juzgador" a la topología del gráfico que no vota, sólo obtiene el consenso final. ¿Cambia esto el comportamiento de conformidad emergente?
   Traducción:En el gráfico, ¿aparece un papel de "comisionado", no sólo por voto, sino por el consenso final?
4. En el artículo de AgenVerse (ICLR 2024) se indica qué comportamiento emergente muestra más fuerte su implementación. ¿Puede provocar el comportamiento opuesto mediante un cambio rápido?
   En el caso de los Estados Unidos, el gobierno de China ha adoptado una política de cambio de comportamiento.
5. Lea MultiAgentBench (arXiv:2503.01935) Sección 4 (experimentos topológicos). Reproduce el resultado de "grafo-ganas-investigación" en una tarea del papel utilizando su arnés.
   En el libro de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor, el autor de la obra, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Más Leer más Leer más

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) Línea de base para un modelo único
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) ambos agentes y rondas son importantes de forma independiente
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) índice de referencia de topología que muestra el gráfico mejor para la investigación, cadena para las tuberías
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) Encuesta de estrategia de MAD; encuentra que la MAD a menudo pierde en la autoconsistencia con un presupuesto igual
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) patrones emergentes de voluntariado y de conformidad
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) Implementación de los índices de referencia
