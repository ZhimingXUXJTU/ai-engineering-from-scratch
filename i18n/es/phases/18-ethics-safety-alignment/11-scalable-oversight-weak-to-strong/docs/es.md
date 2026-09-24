# Supervisión escalable y generalización de débil a fuerte

> Burns y otros. (OpenAI Superalignment, "Generalización de débil a fuerte", 2023) propuso un proxy para el problema de superalignamiento: ajustar de forma fina un modelo fuerte utilizando etiquetas producidas por un modelo más débil. Si el modelo fuerte generaliza correctamente de la supervisión débil imperfecta, los métodos actuales de alineación a escala humana pueden extenderse a sistemas sobrehumanos. La supervisión escalable y el W2SG son complementarios. La supervisión escalable (debate, modelado recurrente de la recompensa, descomposición de tareas) aumenta la capacidad efectiva del supervisor para que pueda mantenerse al día con el modelo bajo supervisión. W2SG asegura que el modelo fuerte generaliza correctamente de cualquier supervisión imperfecta que el superintendente provea. Debate Helps W2SG (arXiv:2501.13124, enero 2025) las combina.

> **【中文解读】**Este capítulo presenta la supervisión extensible de la IA de la evaluación de seguridad de la debilidad a la debilidad. Burns 等人(OpenAI 超级对齐, 2023) propone el agente de la super-preparación: etiquetas de la super-preparación generadas con modelos débiles. Si el modelo fuerte se generaliza correctamente entre la super supervisión de la perfección, el método de la super-preparación de la escala humana actual podría extenderse a sistemas superhumanos.

> **【拓展：弱到强泛化 → 超级对齐路径】**PGR(Performance Gap Recovered)= (微调后-弱)/(上限-弱) ――PGR 为 1.0 significa que el control débil completamente ha compensado el déficit;PGR 为 0 significa que el control débil no ha ayudado。Burns 等人 encontró que PGR en NLP、国际象棋题和奖励建模任务一致于正的(~20%-80%),强模型利用预训先验"理解"的意图任务,超越了弱监督者的错误。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前Please first master:Fase 18·01+10、Fase 09(RL)。W2SG = 弱监督者能否帮强模型学到正确东西,是超级对齐的核心问题──
> ¿ Qué es esto ?**【类比】**W2SG = "小学生教中学生"──en caso de que los estudiantes secundarios puedan aprender correctamente de los maestros de la escuela secundaria, se puede extender a los superhumanos AI──PGR 指标(Performance Gap Recovered) = 弱监督弥合差距比例──Burns 2023 测出 PGR 约20-80%强模型能"理解"意图超越弱监督者的错误──
> 🤔 可扩展监督(debate/递归奖励建模) + W2SG 互补:前者提升监督者能力,后者确保强模型从不完美监督中泛化──

## Objetivos de aprendizaje

- Definir la supervisión escalable y la generalización de débil a fuerte y explicar cómo son complementarias.

> Definir la expansión de la supervisión y la debilidad a la fortalecimiento, y explicar cómo se complementan.

- Describa la configuración experimental de Burns et al. 2023: ajuste fino de GPT-4 utilizando etiquetas de GPT-2.

> 描述 Burns 等人 2023 年的实验设置:使用GPT-2 产生的标签微调GPT-4──

- Explica la métrica de la brecha de rendimiento recuperada (PGR) y lo que mide.

> 解释性能差距恢复 (PGR) índice y su contenido de medida

- En el presente artículo, se especifica el número de unidades de control de las tareas y el número de unidades de control de las tareas.

> 列出三种主要可扩展监督机制 (debates, recurrencias, incentivos, construcciones, tareas y soluciones) y sus respectivos beneficios.

## El problema es la introducción del problema

Cada técnica de alineación hasta ahora en la Fase 18 asume que el supervisor puede evaluar el comportamiento del modelo. Cuando el modelo es sobrehumano, el supervisor es el eslabón débil. La pregunta sobre la superalienación: ¿puede un supervisor más débil producir confiablemente un modelo más fuerte y alineado?

> En la fase 18 hasta la fecha, cada tipo de tecnología de coordinación se ha supuesto que el supervisor puede evaluar el comportamiento del modelo. Cuando el modelo es superhumano, el supervisor es un componente débil.

Burns et al. reducen esto a una configuración empírica operationalizada: supervisa fuerte con débil, mide cuánto de la capacidad del modelo fuerte sobrevive a la supervisión débil.

> Burns  et al. lo simplificó a la configuración de la práctica de la operacionalización: con un control débil, la capacidad de medir un modelo fuerte tiene mucho que sobrevivir bajo el control débil.

## El concepto central.

> **【中文解读】**Burns  et al. Configuración de experimentación: weak模型 GPT-2 级别,强模型 GPT-4 级别,目标是强模型在金标签上限.流程:获取弱模型零样本预测 → 在弱标签上微调强模型 → 测量强微调模型准确率.

### W2SG: la configuración de Burns et al.

- Modelo débil: clase GPT-2.
- Modelo fuerte: clase GPT-4.
- Objetivo: un límite de GPT-4 fuerte en la tarea.

Procedimiento:
1. Obtenga las predicciones de tiro cero de un modelo débil en una tarea.
2. Ajuste el modelo fuerte en datos de etiquetado débil.
3. Medir la precisión del modelo fuerte y ajustado.

> 流程:1. 获取弱模型在任务上的零样本预测――2. 在弱标签数据上的微调强模型――3. 测量强微调模型的准确率――

Líneas de base: la precisión del modelo débil, el límite supervisionado del modelo fuerte en las etiquetas de oro.

> 基线: weak模型自身的准确率,强模型在金标签上的监督上限──

Metrica de brecha: Performance Gap Recovered (PGR) = (finado - débil) / (techo - débil). PGR de 1.0 significa supervisión débil cierra completamente la brecha; PGR de 0 significa supervisión débil no ayudó.

> 差距指标: rendimiento de la diferencia de recuperación (PGR) = ((微调后 - 弱) / ((上限 - 弱) ・PGR 为表示弱监督完全弥合差距;PGR 为 0 表示弱监督没有帮助。

### Burns et al. hallazgos empíricos

En las tareas de PNL, ajedrez y modelo de recompensa, el PGR fue consistentemente positivo: el modelo fuerte se generalizó más allá de los errores del supervisor débil.

> En el NLP, los problemas y las tareas de construcción de premios, el PGR se centró en la generalización de los modelos de fuerza que superaron los errores de los supervisores débiles.

Las limitaciones Burns et al. nota:
- La brecha entre débil y fuerte aquí es la capacidad, no la alineación. El modelo débil está alineado; un modelo verdaderamente sobrehumano podría estar alineado por un humano pero con una brecha de capacidad mucho mayor.

> La diferencia entre débil y fuerte es capacidad, no para hacer frente. El modelo débil es para hacer frente.

- La generalización del modelo fuerte puede ser más sobre las tareas anteriores que sobre la recuperación de la intención de la verdad de fondo.

> La generalización del modelo fuerte puede ser más sobre la experiencia de la tarea, que sobre la recuperación de la verdadera intención.

- El verdadero problema es obtener el conocimiento latente del modelo fuerte; PGR mide una operacionalización específica.

> El potencial de conocimiento del modelo de actividad es el verdadero problema; el PGR mide una operación específica.

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】**辩论(Irving 等人 2018): dos U 实例争论相反立场,弱评判者决定──归归奖励建模(Leike 等人 2018):U 帮助人类训练 U+1 的奖励模型,监督者的有效能力随模型增长──任务分解(Christiano 等人 2018):将硬任务分解成人类可检查的子任务,归归执行──每种机制都假设关于任务结构或中间组件对齐的某些东西──

### Supervisión escalable: tres mecanismos

- **Debate (Irving et al. 2018).**Dos ejemplos de U argumentan lados opuestos; el juez débil decide. La suposición: encontrar una respuesta verdadera convincente es más fácil que encontrar una respuesta falsa convincente. El trabajo reciente de 2024-2025 (Khan et al., Michael et al.) muestra que el debate a veces ayuda y a veces no, y si ayuda depende de la estructura de la tarea.

> **辩论（Irving 等人 2018）。**Dos ejemplos de U. argumentan contra la posición; fallidos jueces decide. Suposiciones: encontrar una verdadera respuesta convincente es más fácil que encontrar una falsa respuesta convincente.

- **Recursive Reward Modeling (Leike et al. 2018).**U ayuda al humano a entrenar el modelo de recompensa para U+1.

> **递归奖励建模（Leike 等人 2018）。**U   ayudar a la formación humana U + 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).**Descompone una tarea difícil en subtareas que el humano puede comprobar, recursivamente.

> **任务分解（Christiano, Shlegeris, Amodei 2018）。**La tarea dura se puede descomponder en subtareas de la humanidad.

Cada mecanismo asume algo sobre la estructura de la tarea o la alineación de los componentes intermedios.

> Cada mecanismo supone que hay algo en la estructura de tareas o en el componente medio para un conjunto.

### Por qué la supervisión escalable y el W2SG son complementarios

La supervisión escalable aumenta la calidad de la señal efectiva del superintendente.
W2SG cierra la brecha de cualquier señal imperfecta que el superintendente pueda proporcionar.

> 可扩展监督提高监督人有效信号质量──弱到强泛化── cualquier incompleto que el supervisor pueda proporcionar, puede generar una diferencia cerrada entre los mismos.

Lang et al.  Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124) las combina: un protocolo de debate proporciona mejores etiquetas débiles, y el modelo fuerte se entrena en esas etiquetas.

> Lang 等人 El debate ayuda a la debilidad a la fortalecimiento ((arXiv:2501.13124)) combinará las dos cosas: el protocolo de debate proporciona mejores etiquetas débiles, el modelo fuerte se entrena en estos etiquetas.

> **【中文解读】**组织戏剧:OpenAI's超级对齐团队 en 2024年 5月Jan Leike 离职加入人类 后解散──但研究议程(可扩展监督、弱到强泛化、自动化对齐研究) 在人类 和学术实验室继续MATS(Leyón 28)、Redwood(Leyón 10)、Apollo(Leyón 8)、METR(Leyón 28)──La estructura de la organización ha cambiado, los problemas de investigación no han cambiado──

### El drama organizacional

El equipo de Superalignment de OpenAI se disolvió en mayo de 2024 después de la partida de Jan Leike a Anthropic. La agenda (supervisión escalable, W2SG, investigación de alineación automatizada) continuó en Anthropic y en laboratorios académicos  MATS (lección 28), Redwood (lección 10), Apollo (lección 8), METR (lección 28). La estructura organizacional cambió; las preguntas de investigación no lo hicieron.

> El equipo de superclasificación de OpenAI se unió a Anthropic en mayo de 2024 Jan Leike 离职加入Antropic 后解散──研究议程(可扩展监督、弱到强泛化、自动化对齐研究) en Antropic 和学术实验室继续MATS、Redwood、Apollo、METR── la estructura de la organización ha cambiado; los problemas de investigación no han cambiado──

### Donde esto encaja en la Fase 18

Las lecciones 6-10 describen la amenaza y el paradigma defensivo bajo la suposición de que U es poco confiable. La lección 11 es el paradigma ofensivo: hacer que el supervisor sea lo suficientemente fuerte como para verificar la alineación de U. Las lecciones 12-16 luego se vuelven a la herramienta práctica de evaluación adversarial.

> Lecciones 6-10  Describir amenazas y hipótesis de U no creíble de la defensa de la modalidad. Lección 11 es la modalidad positiva: hacer que el supervisor sea lo suficientemente fuerte para verificar la U de la preparación. Lecciones 12-16  Vía hacia la evaluación de la resistencia de la herramienta práctica.

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】**Lang 等人(arXiv:2501.13124, 2025 1月) va a extenderse la supervisión y debilitarse a fortalecerse 结合:辩论协议提供更好的弱标签,强模型在这些标签上训练――报告在 NLP 任务上的PGR 提升――这证实了两种方法是互补的可扩展监督增加监督者的有效信号质量,弱到强泛化恢复从任何信号中的差距闭闭――

## Usalo con el marco de ejecución
```figure
scalable-oversight
```

## Usalo

`code/main.py`Simula una sintonía de W2SG en una tarea sintética. El etiquetador débil tiene una precisión del 70% con errores estructurados; el modelo fuerte tiene un techo del 95% en las etiquetas de oro.

> `code/main.py`En tareas sintéticas simuladas W2SG 微调── tasa de precisión de marcador débil 70% 带有结构性错误;强模型在金标上上限为95%──你在弱标上微调强模型,测量PGR,并与强模型金标和弱模型单独结果比较──

## Envíe el producto .

Esta lección produce`outputs/skill-w2sg-pgr.md`. Dado una descripción de la configuración de supervisión, identifica al supervisor débil, al modelo fuerte, a la calidad de la supervisión y calcula (o solicita) la PGR. Indica si la afirmación es "debil puede supervisar fuerte" o "debil + mecanismo de supervisión puede supervisar fuerte".

> 本课产 出  `outputs/skill-w2sg-pgr.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △          △ △ 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`.Informe PGR para la precisión débil = 0,60, 0,70, 0,80. Explica la forma de la curva PGR.

2. Modificar el etiquetador débil para que tenga un error estructurado (por ejemplo, siempre equivocado en una clase de entrada específica). ¿Aumenta, disminuye o permanece igual el PGR?

3. Leer Burns et al. 2023 Sección 4.3 (Tascas de NLP). Reproduce la intuición de "pérdida auxiliar de confianza": cuando el modelo fuerte es más seguro que las etiquetas débiles, ¿quién gana?

4. Diseñar un protocolo de supervisión escalable que combine el debate y la descomposición de tareas para una tarea de ingeniería de software. Nombre un modo de falla de cada componente y explique cómo la combinación se dirige o no se dirige a cada uno.

5. Articula lo que falsearía la afirmación de que "la generalización de débil a fuerte es un camino viable hacia la superalienación".

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Más Leer más Leer más

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) el papel W2SG
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) el mecanismo de debate
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) Modelado recurrente de recompensas
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) 2024 Estudio empírico del debate con debatedores más fuertes
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) 2025 combinación de debates + W2SG
