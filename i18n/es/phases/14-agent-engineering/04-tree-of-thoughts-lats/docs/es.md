# Árbol de pensamientos y LATS: Buscar deliberadamente

> Una única trayectoria de cadena de pensamiento no tiene espacio para retroceder. ToT (Yao et al., 2023) convierte el razonamiento en un árbol con autoevaluación en cada nodo. LATS (Zhou et al., 2024) unifica ToT con ReAct y Reflexion bajo Monte Carlo Tree Search.

> **【中文解读】**单条思维链没有回溯空间――TóT将推理变为带有自评树结构,Game of 24 提升从4% 升至74%──LATS 统一了TóT、ReAct 和 Reflexion,使用蒙特卡洛树搜索实现,HumanEval 达到92.7% pass@1──

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】**En la serie de modelos OpenAI o1/o3 es esencialmente buscar en el espacio de la reflexión explorar múltiples rutas, evaluar y seleccionar lo mejor.

> ¿ Qué es esto ?**【前置】**本节硬核,前置必须扎实:Fase 14·01(ReAct) LATS 内部就是 ReAct;Fase 14·03(Reflexión) LATS Reflexión 复用 Reflexion 机制; así como MCTS(蒙特卡洛树搜索)`Q(s,a) + c*sqrt(lnN/N)`Los dos elementos representan lo que, primero, ver el artículo o el curso de AlphaGo.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Razonamiento de marco como búsqueda: los nodos son "pensamientos", los bordes son "expansiones", el valor es "qué prometedor".
  China:将推理框架为搜索:节点是"pensar",边是"extender",值是"hay más grandes perspectivas"──
- Implementar una búsqueda de árbol BFS de estilo stdlib ToT con puntuación de autoevaluación.
  En el contexto de la investigación, el estudio de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los Estados Unidos.
- Extensión a un bucle de juguete LATS MCTS con selecciona / expande / simula / retropropaga.
  En inglés, el lenguaje de la lengua inglesa se traduce en inglés como "LATS MCTS 循环,包含选择/扩展/模拟/反向传播").
- Decide cuándo la búsqueda vale el multiplicador de tokens (juego de 24, generación de código) y cuándo una sola trayectoria es suficiente (P&A simple).
  China: decidir何时搜索值得付出代币 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增成本 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 倍增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值 增值

## El problema es la introducción del problema

La cadena de pensamiento es una caminata lineal. Si el primer paso es incorrecto, cada paso posterior funciona en una mala premisa. En el juego de 24 (use cuatro dígitos con + − × ÷ para hacer 24), GPT-4 CoT alcanza una precisión del 4%. El modelo elige la subexpresión incorrecta temprano y no puede recuperarse.

> Pensamiento es un progreso lineal. Si el primer paso se ha equivocado, cada paso posterior se basa en un error premeditado. En el juego de 24 (con cuatro números y + − × ÷  obtendemos 24) en el GPT-4 CoT sólo el 4% de la tasa de precisión.

El razonamiento necesita la capacidad de proponer múltiples candidatos, evaluarlos, elegir los prometedores y retroceder cuando aparecen puntos sin salida.

> La hipótesis es: proponer varios programas de candidaturas, evaluarlos, seleccionar perspectivas, retroceder en el mismo tiempo.

> **【中文解读】**Pensamiento es un progreso lineal. Si el primer paso está equivocado, cada paso posterior se basa en un supuesto equivocado.

## El concepto central.

### Árbol de pensamientos (Yao et al., NeurIPS 2023)

Cada nodo es un paso intermedio coherente ("un pensamiento"). Cada nodo puede expandirse a pensamientos de K. El LLM autoevalúa cada nodo con un prompt de puntuación.

> Cada punto es un paso intermedio en el que se puede pensar. Cada punto puede extenderse a K 个子思考.

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

La autoevaluación es la pieza de carga.`sure / likely / impossible`la clasificación, `1..10`Los tres superaron sustancialmente a CoT en el Juego de 24 (4% -> 74% con GPT-4).

> ¿ Qué es esto ?**【类比】**Para el juego de los jugadores de pelota, el juego de pelota es un juego de pelota, que se desarrolla en el juego de pelota, y el juego de pelota es un juego de pelota.

> El trabajo muestra tres variaciones:`sure / likely / impossible`¿Qué clase?`1..10`Número de evaluaciones y votaciones de candidatos.

### LATS (Zhou et al., ICML 2024)

El LLM desempeña tres funciones:

> LATS en MCTS se unió a TOT, React y Reflexión.

- **Policy**: proponer candidato a las próximas acciones (estilo ReAct).
  En inglés:**策略**El proyecto de ley de la Unión Europea (UE) de 2004 sobre la protección de las personas con discapacidad (UE) y la protección de las personas con discapacidad (UE) se ha aprobado en el marco de la presente Decisión.
- **Value function**: obtener una trayectoria parcial (autoevaluación de estilo ToT).
  En inglés:**价值函数**La evaluación de la situación de los trabajadores en el sector de la salud
- **Self-reflector**En caso de fallo, escriba una reflexión en lenguaje natural (estilo de reflexión) y usala para revisar futuras implementaciones.
  En inglés:**自我反思器**La reflexión es una forma de reflexión, para re-emplantear el futuro.

El feedback ambiental (observaciones) se mezcla en la función de valor para que la búsqueda se informe por resultados reales de herramientas, no sólo opiniones de modelos.

> 环境反(观察) Mix into value function, make search by real tool results rather than merely model view drive。

### MCTS, mínimo

Cuatro fases por iteración:

> Cada uno de los cuatro pasos:

1. **Select** caminar de raíz a hoja utilizando UCT (confianza superior ligada a los árboles).
   En inglés:**选择**Utilizar UCT                                                                                                                                                                                                                                                            
2. **Expand** generar hijos K a través de la póliza.
   En inglés:**扩展**Usar estrategias para generar K 个子节点──
3. **Simulate** el despliegue de un niño utilizando la póliza, puntuar la hoja con la función de valor (o recompensa ambiental).
   En inglés:**模拟**从子节点用策略展开, con función de valor (或环境奖励) 评分叶节点──
4. **Backpropagate** actualizar los recuentos de visitas y las estimaciones de valor de la ruta.
   En inglés:**反向传播**En el camino de actualizar el número de visitas y la estimación del valor.

Formula de TCC: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`El primer término es explotación, el segundo es exploración.`c`por tarea.

> UCT 公式:`Q(s, a) + c * sqrt(ln N(s) / N(s, a))` El primer elemento es la utilización; el segundo elemento es la exploración  la adaptación de las tareas `c`¿Qué es eso?

### La realidad de los costes

La búsqueda explota tokens. ToT en Juego de 24 utiliza 1001000x los tokens de CoT. LATS es similar. Esto no es gratuito; reserva búsqueda para:

> ️ **【易错点】**Ver ToT en el juego de 24 上 +70 个点就以为是"银弹",套到所有任务上.**后果**En simple preguntas y respuestas, el consumo de 1000 veces el token se cambia a 0% 提升, cuenta单爆炸──**一行修复**En primer lugar, utilizar 10 muestras en comparación con la CoT vs. la CoT, aumentar < 5 puntos en la búsqueda de la CoT para la tarea de "una escasez evidente de trayectoria"

> 搜索会爆炸 token──Tot en juego de 24 上消耗 CoT de 100-1000 veces el token──LATS 类似──This is not free; will search leave to:

- Tarea en la que una sola trayectoria sea demostrablemente insuficiente (juego de 24, código complejo).
  En la actualidad, el juego de 24 ̊ es un juego de 24 ̊.
- tareas donde el reloj de pared es menos importante que la corrección.
  Traducción:La verdad es una tarea más importante que el tiempo.
- tareas con una función de valor barata y confiable (teses unitarios para código, objetivo explícito para matemáticas).
  Traducción: tiene un precio bajo y un valor fiable.

Si su tarea tiene una sola respuesta correcta y un evaluador ruidoso, la búsqueda a menudo empeora las cosas  encuentra una respuesta incorrecta "buena puntuación".

> ¿ Qué es esto ?**【困惑】**P: LATS poner a TOT/ReAct/Reflexion 三個都"统一"了, ¿es eso el que ha aprendido LATS就足了吗 A: 不足──LATS es "重型武器" una vez completa búsqueda para desarrollarse en cientos de puntos, tokens de una sola misión 成本可达百万级── 95% del entorno de producción 任务使用 ReAct + 简单 Reflexion 已足──LATS sólo en "valor de funciones baratas y fiables" como 代码任务的单元测试) cuando sólo vale la pena── primero aprende el modelo de la cantidad ligera, reaprender LATS──

> Si tu tarea tiene una respuesta correcta pero el evaluador tiene ruido, la búsqueda suele empeorar la situación. Encontrará una respuesta "alta pero errónea".

> **【中文解读】**搜尋会爆炸 TokenToT en el juego de 24 上消耗 CoT 100-1000 倍. Solo en los siguientes escenarios se puede buscar:

### Posicionamiento 2026

La mayoría de los agentes de producción no ejecutan LATS. Ejecutan ReAct con verificación basada en herramientas (CRITIC, Lección 05).

> La mayoría de las empresas producen agentes no funcionan en los sistemas de detección de gases de efecto invernadero.

- Los agentes de codificación que ejecutan pruebas como función de valor (estilo HumanEval).
  En inglés, el nombre de la función de valor es el nombre de la función de valor.
- Agentes de investigación profunda que exploran múltiples vías de consulta.
  En español: explorar múltiples vías de consulta.
- Flujos de trabajo pesados de planificación dentro de los subgrafos de LangGraph.
  La obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra.

AlphaEvolve (Lección 11) es el extremo de 2025: búsqueda evolutiva sobre código, aptitud verificada por máquina, ganancias fronterizas (primera mejora en 4x4 matmul en 56 años).

> AlphaEvolve (n. 11 课) es el último caso de 2025: búsqueda de evolución en código, adaptación de máquinas, avances en la línea de la línea de acción, y la primera vez en 56 años que la matriz de la multiplicación se ha mejorado)

## Construye y realiza.
```figure
tree-of-thoughts
```

## Construye el mismo

`code/main.py`los instrumentos:

> `code/main.py`实现:

- Un pequeño ToT BFS en una tarea estilizada "pick arithmetic ops".
  En la lengua china, el método de cálculo es el método de cálculo de la función de cálculo.
- Un bucle de juguete LATS MCTS en la misma tarea (Select / Expand / Simulate / Backpropagate) con la selección de UCT.
  La lengua inglesa se traduce en inglés como "el lenguaje de la lengua" (en inglés: "el lenguaje de la lengua") y en inglés como "el lenguaje de la lengua".
- Una función de valor que compone una puntuación simbólica más una puntuación autoevaluación.
  Un conjunto de valores de evaluación y autoevaluación de la evaluación.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra que ToT expande tres candidatos por nodo con BFS, en comparación con LATS convergiendo en el mejor despliegue a través de MCTS.

> 轨迹显示 ToT Using BFS Cada nodo se expande tres candidatos, con LATS 通过 MCTS 收到最佳展开对比── ambos imprimieron un token 计数──

## Usalo con el marco de ejecución

LangGraph envía la exploración en estilo ToT como patrones de subgrafos; el blog del equipo de LangChain en LATS (mayo 2024) es el tutorial de referencia.`TreeOfThoughts`Para la mayoría de los agentes de producción de 2026 este patrón vive detrás de un`if task_complexity > threshold: use_search()`gate  ver el patrón evaluador-optimizador en la Lección 05.

> LangGraph va a explorar ToT 风格 como un modelo de gráfico; LangChain 团队关于 LATS 的博客(2024 年 5 月) es un curso de referencia.`TreeOfThoughts`Para la mayoría de los agentes de producción de 2026, este modelo existe en`if task_complexity > threshold: use_search()`门控后参见第 5 课的评估器-优化器模式──

## Envíe el producto .

`outputs/skill-search-policy.md`selecciona entre ReAct lineal, ToT, LATS y búsqueda evolutiva dada la forma de la tarea, el presupuesto y la fidelidad del evaluador.

> `outputs/skill-search-policy.md`根据任务形状、预算和评估器保真度,在线性 ReAct、ToT、LATS 和进化搜索之间选择──

## Los ejercicios.

1. Ejecutar el juguete LATS con UCT c=0.1 vs c=2.0. ¿Qué cambios en la pista?
   Traducción:Ud UCT c=0.1 y c=2.0 分别运行 LATS──轨迹有什么变化?
2. ¿MACTS todavía encuentra la mejor hoja? ¿Cuál es el mínimo de señal-ruido que tolera?
   China 翻译:将价值函数替换为更杂的评分器──MCTS ¿puede encontrar el mejor eje de la línea? ¿Cuál es el mínimo índice de ruido que puede tolerar?
3. Implementar la búsqueda de rayos de ToT (mantener el top-k en cada nivel) y comparar con BFS. ¿Cuál es mejor con un presupuesto de tokens ajustado?
   En el caso de los datos de la información, el valor de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información.
4. Leer LATS Sección 5.1. Reproduce el recuento de trayectoria de HumanEval: ¿cuántas implementaciones se necesitan para alcanzar el paso@1 reportado?
   China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China
5. Lea el artículo de LATS sobre "cuando LATS ayuda menos". Escriba una regla de decisión de un párrafo que mapee la forma de la tarea para la estrategia de búsqueda.
   China 翻译:阅读 LATS 论文关于"何时 LATS 帮助不大"的讨论──写一段决策规则映射任务形状到搜索策略──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tree of Thoughts | "Branching CoT" / "分支思维链" | Yao et al. — tree of thought nodes with self-evaluation / Yao 等人——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" / "LLM 的 MCTS" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS / Zhou 等人——在 MCTS 下统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" / "上置信界" | Select formula balancing exploitation (Q) and exploration (ln N / n) / 平衡利用(Q)和探索(ln N/n)的选择公式 |
| Value function | "How good is this state" / "状态有多好" | Prompted LLM score or environment reward; feeds backprop / 提示的 LLM 评分或环境奖励；驱动反向传播 |
| Policy | "Action proposer" / "行动提议器" | ReAct-style generator; emits candidate next thoughts/actions / ReAct 风格生成器；发出候选下一步思考/行动 |
| Rollout | "Simulated trajectory" / "模拟轨迹" | Walk from a node to a leaf using policy, score with value / 用策略从节点走到叶节点，用价值函数评分 |
| Backpropagate | "Update ancestors" / "更新祖先" | Push the leaf's reward up the path, updating visit counts and Q / 将叶节点的奖励沿路径上推，更新访问计数和 Q 值 |
| Search cost | "Token explosion" / "Token 爆炸" | 100-1000x CoT on Game of 24; budget before you adopt / Game of 24 上是 CoT 的 100-1000 倍；采用前先做预算 |

## Más Leer más Leer más

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) el papel canónico
  En el texto original, el texto se traduce en "la palabra " .
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) MCTS con retroalimentación de reflexión
  La reflexión de la mente de los hombres
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) patrones de subgrafo para la búsqueda
  En el lenguaje chino, el lenguaje de la lengua se traduce en lengua inglesa.
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) búsqueda evolutiva con evaluadores programáticos
  El desarrollo de la tecnología en el mundo de la información es un proceso de desarrollo de la información.
