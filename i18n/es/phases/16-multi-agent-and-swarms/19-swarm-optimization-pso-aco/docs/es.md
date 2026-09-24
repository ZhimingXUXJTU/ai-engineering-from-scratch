# Optimización de la colección para LLM (PSO, ACO) 优化群体 PSO ACO LLM

> La optimización bio-inspirada está haciendo un regreso de LLM. **LMPSO**(arXiv:2504.09247) utiliza PSO donde la velocidad de cada partícula es un prompt y el LLM genera el siguiente candidato; funciona bien en las salidas de secuencias estructuradas (expresiones matemáticas, programas). **Model Swarms**(arXiv:2410.11163) trata a cada experto en LLM como una partícula de PSO en un colectivo de modelos y informes **13.3% average gain**más de 12 líneas de base en 9 conjuntos de datos con sólo 200 instancias. **SwarmPrompt**(ICAART 2025) hibrida PSO + Grey Wolf para una optimización rápida. **AMRO-S**(arXiv:2603.12933) es un especialista en feromonas inspirado en ACO para el enrutamiento de LLM multiagente  **4.7x speedup**Esta lección implementa PSO en el espacio de parámetros rápidos y ACO en el enrutamiento de agentes, mide por qué estos algoritmos clásicos se ajustan a la era LLM y cuándo no.

> **【中文解读】**Este capítulo presenta el algoritmo de optimización de grupos de partículas (PSO) y ACO (ACO) y la aplicación de organismos para la optimización en múltiples agentes.

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO) Agent 根据自身最佳位置和全局最佳位置调整搜索方向;(2) 群群优化(ACO) Agent 通过信息素标记好的路径,后者倾向于跟随强信息素路径──这些算法适应大规模搜索空间中的优化问题,如 Agent 任务分配和路径规划──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·09(Swarm 网络) 、Fase 16·14(BFT) 、 clásico algoritmo de optimización(PSO/ACO/GA) ⋅本节把生物启发算法应用到LLM 时代prompt 优化、模型路由──
> ¿ Qué es esto ?**【类比】**LLM + PSO/ACO = "群找最佳快点"──PSO = Cada agente es una partícula, velocidad=pront, hacia la mejor movimiento de la totalidad;ACO = agente en el momento 空间留下信息素, posteriormente seguido de fuerte信息素──LMPSO 适合结构化输出(máthematic expression、代码);Model Swarms Colocar cada LLM 专家当粒子,比12个基线平均高13.3%;AMRO-S utiliza ACO 路由,4.7 倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

El resultado de la prueba es que el resultado de la prueba es un resultado de una prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba

> Tienes una sugerencia en la evaluación de tareas que obtiene un 62% de puntuación. Quieres mejorarla. El método simple es el ajuste manual sin escalas, la expansión de los cambios.

La optimización clásica de bio-inspirada  PSO para espacios de búsqueda continua, ACO para la selección de trayectoria  fue diseñada exactamente para este régimen: libre de gradientes, basado en la población, barato por evaluación.

> PSO utiliza para el espacio de búsqueda continua, ACO utiliza para la selección de caminos  es exactamente para este escenario diseñado: sin gradiente  basado en la variedad  bajo costo de evaluación por cada vez 

Los mismos patrones se aplican al agente *routing* en sistemas multi-agentes. Un tipo ACO registra el rastro de feromonas en el que el agente trabajó mejor en qué tipo de tarea, permite al router explotar el rastro y descompone las feromonas para que se puedan redescubrir las rutas.

> El mismo modelo se aplica a los agentes de múltiples agentes en el sistema de datos de los agentes de los sistemas de datos de los agentes de los sistemas de datos de los agentes de los agentes de los sistemas de datos de los agentes de los agentes de los sistemas de los agentes de los agentes de los sistemas de los agentes de los agentes de los sistemas de los agentes de los agentes de los agentes de los sistemas de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los sistemas de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los sistemas de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los cuales los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los que se han descubierto de los de los de los de los de los de los de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los agentes de los cuales de los agentes de los agentes de los agentes de los agentes de los cuales de los agentes de los agentes de los agentes de los cuales de los agentes de los agentes de los agentes de los agentes de los que se recaja de los cuales de los agentes de los agentes de los agentes de los agentes de los agentes de los cuales son de los agentes de los agentes de los

## Concepto de la esencia de la concepción

### Reforma de la OPS (Kennedy & Eberhart 1995)

Optimización de las partículas en un espacio de búsqueda continua.`x_i`y velocidad.`v_i`Cada iteración:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

¿ Dónde ?`p_best`es lo mejor de la partícula,`g_best`es el mejor de los enjambre,`w, c1, c2`son la inercia + cognitivo + pesos sociales, `r1, r2`son factores aleatorios.

### OPS sobre resultados de LLM  LMPSO

ArXiv: 2504.09247 adapta PSO para las salidas estructuradas generadas por LLM (expresiones matemáticas, programas). Cada partícula es una salida candidata. Velocidad es una *prompt* que describe cómo modificar la salida actual hacia lo mejor personal / global. El LLM genera la nueva salida a partir del prompt de velocidad. La "inercia" de la velocidad es un prompt como "hacer pequeños cambios incrementales".

Esto funciona bien cuando:
- La salida está estructurada (percibible, evaluable).
  En inglés, el resultado es estructurado.
- La aptitud es automática (teste de pruebas, evaluación aritmética).
  La capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de evaluación de la capacidad de los expertos.
- La población es pequeña (~ 10-30 partículas) por lo que las llamadas totales de LLM siguen siendo manejables.
  En el caso de los grupos de microorganismos, el número de moléculas de microorganismos es de 10 a 30 moléculas.

No funciona bien cuando la aptitud necesita revisión humana  el costo de la repetición se vuelve prohibitivo.

> Cuando la adaptación requiere un examen artificial, el efecto es malo.

### Un grupo de ejemplos

ArXiv:2410.11163 saca el PSO de la capa de salida y en la capa de *modelo*. Cada "partícula" es un LLM experto (parámetros). El enjambre mueve los parámetros hacia el mejor colectivo a través de una actualización libre de gradientes.

La idea clave es que los modelos expertos de LLM ya están cerca en un variedad compartida de parámetros (pesos de adaptadores, deltas de LoRA).

### Actualización de la ACO (Dorigo 1992)

La optimización de la colonia de hormigas: las hormigas atraviesan un gráfico; cada camino tiene una pista de feromonas. Las hormigas mueven las probabilidades de peso por la fuerza de feromonas. Las hormigas que completan la tarea depositan feromonas proporcionales a la calidad de la solución.

### AMRO-S  ACO para el enrutamiento de agentes

ArXiv:2603.12933 utiliza ACO para el enrutamiento multi-agente. Cada tipo de tarea es un "destino"; cada agente es una ruta posible.

- **Interpretable routing evidence.**La fuerza de feromonas es una señal legible para el hombre.
  En inglés:**可解释的路由证据。**La intensidad de la información es un signo que el hombre puede leer.
- **Quality-gated asynchronous update.**Las feromonas se actualizan sólo después de que se hayan superado las comprobaciones de calidad, desacoplando la inferencia del aprendizaje.
  En inglés:**质量门控异步更新。**La información sólo se actualizará después de que el control de calidad sea aprobado, se pondrá en práctica con la solución de aprendizaje.
- **4.7x speedup**en el índice de referencia de enrutamiento de múltiples agentes.
  Traducción: en muchos agentes**4.7 倍加速**¿Qué es eso?

La puerta de calidad es importante: sin ella, los agentes rápidos pero equivocados acumulan feromonas, y el sistema se bloquea en malas rutas.

> 质量门很重要: sin él, rápido pero erróneo Agente 会积累信息素, el sistema bloqueado en un camino malo.

### Cuándo utilizar PSO / ACO para LLM

**Use PSO when:**
- El espacio de búsqueda es continuo o mapas a parámetros continuos (embedings de inmediato, pesos de LoRA, parámetros de generación numérica).
  En inglés, el nombre de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- El fitness es barato y automático.
  La calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad.
- La población puede ser pequeña (10-30).
  Se puede tener un pequeño grupo de personas.

**Use ACO when:**
- Tienes un problema de enrutamiento o de selección de ruta.
  Traducción:Tu tienes un camino o un camino de elección.
- Las decisiones se refuerzan con el tiempo (los mismos tipos de tareas vuelven).
  China: decisión con tiempo enriquecimiento (shame task type will come back)
- Necesitas pruebas interpretables para las decisiones de enrutamiento.
  China: You need proof of the way of decision-making.

**Do not use either when:**
- La aptitud requiere revisión humana (demasiado costosa por iteración).
  La normalidad de la calidad de vida de los animales es la normalidad de la calidad de vida de los animales.
- El espacio de búsqueda es discreto y combinatorial de una manera que la PSO no cubre (use algoritmos genéticos en su lugar).
  En el caso de los sistemas de búsqueda de datos, el sistema de búsqueda de datos es un sistema de búsqueda de datos.
- Las decisiones en tiempo real requieren una latencia estricta (PSO/ACO convergen lentamente en relación con las heurísticas de paso único).
  La decisión de tomar una decisión en el tiempo real debe ser muy retrasada.

### ¿Por qué la bio-inspirada todavía gana?

Los métodos basados en gradientes necesitan señales diferenciables. Las salidas de LLM y las decisiones de enrutamiento no son triviales. Los métodos pseudo-gradientes (routers de refuerzo, ajustes de instrucción de tipo DPO) funcionan, pero requieren una formación costosa.

PSO y ACO sólo necesitan una función de *evaluador* Si puedes marcar una salida de candidato o una decisión de enrutamiento, puedes optimizar el espacio. Eso hace que la barra de aplicabilidad sea mucho menor.

### Limitos prácticos

- **Population budget.**N partículas × T iteraciones × costo por eval. Para evaluaciones LLM en ~$0.02 / call, a 20-particle PSO running 50 iterations costs ~$Planar en consecuencia.
- **Exploration vs exploitation.**La tasa de descomposición de feromonas y la inercia de PSO se deshacen; descomposición demasiado rápida → olvidar soluciones; demasiado lento → atascado en las primeras óptimas locales.
- **Catastrophic drift.**Los dos algoritmos pueden converger y luego divergir si el panorama de fitness cambia (nueva distribución de datos).

## Construye con movimiento.
```figure
swarm-stigmergy
```

## Construye el mismo

`code/main.py`los instrumentos:

- `LMPSO` PSO sobre parámetros de respuesta numéricos (temperatura, pesos top_k). La "generación LLM" de cada partícula se simula como una función de aptitud scripted.
- `AMRO_S` Enrutamiento en estilo ACO. 3 agentes, 4 tipos de tareas, matriz feromónica, 100 tareas enrutadas. Impresiones (task_type → opciones de agente) distribución a lo largo del tiempo para mostrar la formación de la trayectoria.
- Comparación: enrutamiento aleatorio vs ACO en el mismo flujo de tareas.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Producción esperada:
- LMPSO: g_best fitness mejora de aleatorio a casi óptimo en más de 30 iteraciones.
- AMRO-S: la tabla de feromonas se estabiliza en el agente correcto por tipo de tarea; el enrutamiento ACO supera al azar en ~ 30-40% en calidad y también reduce la latencia (menos retemplajes).

## Usalo.

`outputs/skill-swarm-optimizer.md`ayuda a elegir entre PSO, ACO, algoritmos genéticos y optimizadores basados en gradientes para problemas de optimización de LLM / agente.

## Envíalo .

- **Start small.**10-20 partículas, 20 a 50 iteraciones. escalar sólo si la curva de convergencia muestra una ganancia clara.
  En inglés:**从小开始。**10-20 partículas, 20-50 veces 代── sólo en la curva de recepción muestra un aumento evidente en el tiempo de expansión.
- **Log pheromones or g_best per iteration.**Desarmar los optimizadores de enjambre sin rastro es doloroso.
  En inglés:**每次迭代记录信息素或 g_best。**No hay trayectoria.
- **Quality-gate updates.**Especialmente para el enrutamiento de ACO: los agentes rápidos y incorrectos no deben acumular feromonas.
  En inglés:**质量门控更新。**                                                                                                                                                                                                                                                              
- **Reset decay on distribution shift.**Cuando la distribución de la evaluación cambia, las feromonas envejecidas se quedan obsoletas; restablezca o duplique temporalmente la tasa de descomposición.
  En inglés:**分布偏移时重置衰减。**Cuando se evalúa el cambio de distribución, la tasa de envejecimiento de la información se vuelve obsoleta; se repone o se multiplica temporalmente.
- **Cap the per-iteration cost.**Emírese una métrica de costo por iteración. PSO que cuesta $500 / iteración y gana el 0,5% no es enviable.
  En inglés:**限制每次迭代成本。**发发每次代成本指标──每次代花费$500 且只增加0.5%的PSO不可发行──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Observe la convergencia de LMPSO. ¿A qué tamaño se satura el tiempo para converger?
2. Implementar un experimento de "drift catastrófico": después de la iteración 30, cambiar la función de aptitud. ¿Qué tan rápido se adapta el PSO? ¿Reiniciará la configuración `p_best`¿Cómo puedo ayudar?
3. Añadir una puerta de calidad a AMRO-S: depósito de feromonas sólo en carreras con puntaje de evaluación > 0.7. ¿Cómo cambia esta convergencia frente a la versión no-garada?
4. Leer LMPSO (arXiv:2504.09247). Mapa de la "velocidad como un prompt" del papel de vuelta a su velocidad numérica. ¿Qué se pierde en la simulación y qué se conserva?
5. Leer AMRO-S (arXiv:2603.12933). Implementar el "camino rápido de inferencia" descoplado con actualización feromónica asíncrona. ¿Cómo cambia esta latencia del sistema bajo carga sostenida?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Más Leer más Leer más

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) el documento de 1995 de la OPS
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) 1992 fundaciones de la ACO
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) OPS para los resultados estructurados de MLL
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) PSO en el subespacio de peso del modelo
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) Enrutamiento con feromonas con puerta de calidad
