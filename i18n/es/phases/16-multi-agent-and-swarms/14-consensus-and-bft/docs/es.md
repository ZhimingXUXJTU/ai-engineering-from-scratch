# Consenso y tolerancia bizantina por la culpa de los agentes

> Los sistemas distribuidos clásicos BFT se encuentran en el marco de los LLM estocásticos.**CP-WBFT**(arXiv:2511.10400) sopesa cada voto por una investigación de confianza; **DecentLLMs**(arXiv:2507.14928) se queda sin líder con propuestas paralelas de trabajadores y agregación geométrica-mediana; **WBFT**(arXiv:2505.05103) combina votación ponderada con Clustering de estructura jerárquica para dividir los nodos Core y Edge. El resultado empírico honesto de "¿Pueden Agentes de IA estar de acuerdo?" (arXiv:2603.01213) es que incluso el acuerdo escalar es frágil hoy en día  un solo agente engañoso puede comprometer una mezcla de Agentes. La BFT es necesaria, pero no suficiente. Esta lección construye un protocolo BFT mínimo, inyecta tres ataques específicos de agentes (mentir bizantino, conformidad sicófante, monocultura de errores correlacionados) y mide cómo se enfrenta cada variante de consenso.

> **【中文解读】**Este capítulo presenta el consenso y la forma de llegar a un acuerdo en caso de posible fallo o malintención de un agente.

> **【拓展：consensus and bft→具体应用】**拜占庭容错 (BFT) 在多 Agent 系统中的应用:当部分 Agent可能故障或被攻击时,如何确保系统整体正确? 经典 BFT 算法(PBFT) 需要3f+1 个节点容忍 f 个故障节点──在 LLM Agent 上下文中,'故障' puede ser iluminación、 ser inyectado o rechazado ejecutar──实践中使用多数投票作为简化 BFT──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·07(辩论) Fase 16·13(共享内存)  Sistema distribuido BFT(PBFT、Raft)  El "故障" del agente de la LLM=幻觉、被注入、拒绝执行──
> ¿ Qué es esto ?**【类比】**BFT = "jurjuria vota pero para protegerse del espíritu"― clásico BFT = tolerancia 1/3 节点说谎(PBFT 3f+1);LLM 版 = 加权投票(按置信度)+ 几何中位数聚合 + 层级聚类──三类攻击:拜占庭说谎、附和、相关错误(same base model 全错)──结论:BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: B
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

Hay N LLM agentes cada uno que produce una respuesta. No están de acuerdo. La mayoría de votos elige el equivocado porque dos agentes están correlacionados (el mismo modelo base, los mismos datos de entrenamiento, los mismos modos de falla).

> Usted tiene N 个 LLM Agent, cada uno produce una respuesta. Ellos no coinciden. La mayoría de los votos eligió la respuesta errónea, porque dos agentes son relacionados.

Ahora añadir un agente engañoso: se encuentra a propósito. O un agente sicófante: está de acuerdo con quien ha hablado por último. En BFT clásico, la suposición es que los nodos bizantinos son una fracción.`f < n/3`La realidad de 2026 es que los nodos LLM son estocásticos incluso cuando son honestos, correlacionados entre los modelos, e influenciados por los resultados de los demás. No se puede tratarlos como votantes independientes de Bernoulli.

> Ahora se une a un agente engañoso: se pretende mentir. O un agente engañoso: se acuerda de la opinión del último hablante. En el clásico BFT, supongamos que el cliente ocupa un porcentaje.`f < n/3`并且行为任意──2026年现实是,LLM 节点即使诚实也随机,跨模型相关,并受影响彼此输出──你不能将它们视为独立的伯努利选民──

El BFT clásico (PBFT, 1999) no está equivocado  es incompleto. Se ocupa de la flexión arbitraria de bits. No se ocupa de "tres agentes honestos comparten una alucinación porque comparten datos de entrenamiento". Esta lección se basa en la base de PBFT y las capas de tres adaptaciones 2025-2026.

> 经典 BFT(PBFT, 1999)并非错它是不完整的──它处理任意位翻转──但它不处理"三个诚实代理因为共享训练数据产生相同幻觉"──本课程从PBFT的基础上发发,叠加三个2025-2026年改进──

## Concepto de la esencia de la concepción

### ¿Qué te da el BFT clásico?

La tolerancia práctica de la falta bizantina (Castro y Liskov, OSDI 1999) tolera `f < n/3`Los nodos bizantinos. El protocolo tiene tres fases (preparación, preparación, compromiso) y dos primitivas (mensajes firmados, certificados de quórum).`n >= 3f + 1`los nodos honestos o maliciosos.

> 实用拜占庭容错(Castro y Liskov, OSDI 1999) tolerancia `f < n/3`个拜占庭节点──协议有三个阶段 (预备备、准备、提交) 和两个原语 (签名消息、仲裁证书)`n >= 3f + 1`个诚意或恶意节点之间就单一价值达成一致.

Las garantías son fuertes, pero se supone que:

> Estas garantías son fuertes, pero supongamos:

1. **Independent faults.**Los bizantinos no se coordinan.
   En inglés:**独立故障。**拜占庭节点不协调──
2. **Honest nodes are truly honest.**La corrección de las salidas honestas no es un problema; el protocolo solo alinea el desacuerdo.
   En inglés:**诚实节点真正诚实。**La verdadera verdad no es un problema; el acuerdo sólo trata las diferencias.
3. **The question has a ground-truth answer.**El consenso sobre un hecho equivocado sigue siendo consenso.
   En inglés:**问题有标准答案。**El consenso sobre los errores sigue siendo el consenso.

Los agentes de LLM violan los tres. Dos agentes que ejecutan el mismo modelo base comparten fallos. Un LLM "honesto" todavía alucina. Y en preguntas ambigüas, la "verdad" es lo que los agentes deciden  no hay oráculo externo.

> El agente de LLM  violaron todas las tres hipótesis  operando dos agentes del mismo modelo básico  共享故障── "húngico" LLM  todavía se producirá ilusión  En cuestiones confusas, la "verdad" es decidida por el agente  no hay predicciones externas

### Los tres ataques específicos de la LLM

**Byzantine lie.**Un agente da una respuesta deliberadamente incorrecta.`f < n/3`¿ Qué ?

> **拜占庭撒谎。**Un agente 输出故意错误的答案―如果`f < n/3`, clásico BFT se puede tratar.

**Sycophantic conformity.**Un agente lee las respuestas de otros antes de votar y se alinea con quien ha hablado por último. No es malicioso, pero correlaciona con la voz más alta.

> **谄媚从众。**Un agente en la votación antes de leer la respuesta del otro agente, y mantenerse en consonancia con el último orador. No es malicioso, pero está relacionado con la mayor voz.

**Correlated-error monoculture.**Tres agentes comparten un modelo base. Alucinan la misma respuesta equivocada. La mayoría está equivocada.

> **相关错误单一文化。**Tres agentes comparten un modelo básico. Ellos producen el mismo error de percepción. La mayoría es un error.

### Las respuestas de 2025 a 2026

**CP-WBFT**(arXiv:2511.10400)  BFT ponderado probado por confianza. Cada votante une una sonda de confianza a su respuesta (una probabilidad autoinformada o la predicción de un modelo de calibración separado).

> **CP-WBFT**(arXiv:2511.10400)Infidence detection incremented BFT── cada votante para su respuesta añade una infiencia detection(auto-informe probabilidad, o un modelo de clasificación individual)── el derecho a votar se reduce con la infiencia── el informe muestra en la gráfica completa una mejora en la BFT de +85.71%── en la medida de alivio de la multitud  de los agentes de la multitud  tendencia a tener una infiencia menor en las posiciones que se proponen voluntariamente)──

**DecentLLMs**Los agentes de trabajo proponen en paralelo, los agentes de evaluación ponen propuestas, la respuesta final es la media geométrica de las posiciones ponedoras.`f < n/2`. Mitigation for: mentira bizantina y errores correlacionados (mediana geométrica es robusta a valores extremos y se dirige hacia el cúmulo denso, no a la media basada en modelos).

> **DecentLLMs**(arXiv:2507.14928)  sin líder  Trabajo Agente y se propone el programa, evaluar Agente para el programa de evaluación, la respuesta final es la posición de evaluación `f < n/2`时稳健.                                                                                                                                                                                                                                                             

**WBFT**(arXiv:2505.05103)  Peso BFT con Clustering de Estructura Jerárquica. Los pesos de voto se asignan por calidad de respuesta más un puntaje de confianza aprendido de la historia. Agentes de grupo en Core y Edge; Agentes de Core deben lograr el consenso primero, Agentes de Edge siguen. Mitigation para: escalabilidad (Core consenso es pequeño y rápido) y parcialmente para monocultura (Core se puede elegir para la diversidad).

> **WBFT**(arXiv:2505.05103) 带层次结构聚类的加权 BFT;; votación de la carga por respuesta calidad加上从历史中学习的信任分数分配;;将代理聚类为核心和边缘;核心代理 必须先达成共识,边缘代理跟随;;针对可扩展性的缓解措施(核心共识小而快) 和部分针对单一文化的缓解;;核心可以选择多样性) 

### Empirical: "¿Pueden los agentes de IA estar de acuerdo?" (arXiv:2603.01213)

El papel mide el acuerdo escalar (agentes LLM que acuerdan un solo valor numérico) en múltiples modelos fronterizos.

> El trabajo mide la coincidencia de los valores en varios modelos de vanguardia.

- Incluso sin adversarios, los agentes de LLM no están de acuerdo en cuestiones escalares a tasas superiores al 30% en muchos puntos de referencia.
  Aunque no haya contractuales, el porcentaje de discrepancias en los muchos exámenes de base sobre la cantidad de material es superior al 30%[1].
- Un agente que adopte una personalidad engañosa puede sacar el consenso de la mezcla de agentes 40 puntos porcentuales más de la línea de base honesta.
  Traducción:El agente puede ser confundido con un agente de la empresa.
- Las tasas de desacuerdo se correlacionan con la diversidad de modelos  los conjuntos heterogéneos no coinciden más que los homogéneos (bueno: errores no correlacionados) pero también se desvían más lentamente (malo: tiempo más largo para llegar a un acuerdo).
  China: 不一致率与模型多样性相关异构集成比同构集成不一致更多(好:不相关错误),但漂移更慢(坏:更长的一致达成时间)。

El resultado: BFT le da un mecanismo para alinear las salidas, pero no le dice si la salida alineada es correcta. Combina con la verificación (fase 16 · 08 especialización de roles), la diversidad (fase 16 · 15 variantes de debate) y los agentes evaluadores (fase 16 · 24 puntos de referencia).

> 结论:BFT 提供出口对齐的机制, pero no le dice si la salida对齐 es correcta.

### El protocolo central, despojado

Una ronda mínima de BFT para los agentes de LLM:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

El paso de agrupamiento semántico es el giro específico del LLM. Dos respuestas "el estudio informa un 4,2%" y "una mejora del 4,2%" son el mismo agrupamiento.

> 语义聚类步骤是LLM's peculiar innovation. Dos respuestas"Research Report 4.2%" y"4.2% of Improvement" son las mismas.

### El ajuste del umbral

El `threshold`El parámetro decide cuándo aceptar y cuándo volver a intentar. Demasiado bajo: aceptas mayoritades débiles. Demasiado alto: nunca aceptas nada. Rango empírico: 0,5-0,67 para `n=5-7`Los agentes, más altos para los más pequeños `n`Por debajo de un umbral, escalar a un humano o a un conjunto de agentes diferentes.

> `threshold`参数决定何时接受、何时重试──太低: aceptar weak多数──太高:永远不接受任何东西── experiencia:`n=5-7`个 Agente 时为0.5-0.67,较小的 `n`时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 低于值. 时更高. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值.

### Cuando el consenso no ayuda

- **Ambiguous questions.**Si la pregunta no tiene verdad, el consenso es una opinión.
  En inglés:**模糊问题。**Si el problema no tiene una respuesta estándar, el consenso es la opinión.
- **Compound questions.**"Escribe código y explique"  dos respuestas. Vota por cada uno de forma independiente.
  En inglés:**复合问题。**"编写代码并解释"两个答案──分别独立投票──
- **Adversarial multi-round.**Si los agentes pueden observar las rondas anteriores y imitar (debate Du 2023), comienzan a estar de acuerdo entre sí independientemente de la verdad.
  En inglés:**对抗性多轮。**Si el agente puede observar las primeras dos rondas y hacerse igual, las dos se van a poner de acuerdo.

## Construye con movimiento.
```figure
swarm-consensus-wave
```

## Construye el mismo

`code/main.py`los instrumentos:

- `AgentVoter` una política escrita con (respuesta, confianza).
  En inglés:`AgentVoter` 带有(答案,置信度) de la estrategia de guión.
- `MajorityVote` Pluralidad clásica.
  En inglés:`MajorityVote` 经典多数投票──
- `CPWBFT` Votación ponderada por confianza con agrupación semántica.
  En inglés:`CPWBFT` 带语义聚类的信任度加权投票──
- `DecentLLMs` Agregación geométrica-mediana de las propuestas obtenidas.
  En inglés:`DecentLLMs` 评分 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价   评价     评 评     评  评 评    评      评      评                                                                                                                                                                           
- `Scenario` ejecuta cada agregador bajo tres patrones de ataque.
  En inglés:`Scenario` En tres tipos de ataque mode de funcionamiento de cada aglomerador.

Modelos de ataque implementados:

> 实现的攻击模式:

1. `byzantine`Un agente miente con mucha confianza.
   En inglés:`byzantine`Un agente de alta confianza en la mentira.
2. `sycophancy`Un agente copia la primera respuesta que ve, con la misma confianza.
   En inglés:`sycophancy`Un agente replica la primera respuesta que ve, con certeza.
3. `monoculture`En el caso de los agentes, el resultado es el siguiente:
   En inglés:`monoculture`Tres agentes compartieron un error de respuesta, un error de confianza, etc.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La mayoría de los casos de monocultura no se cumplen con el caso de la monocultura. La ponderación de confianza de CPWBFT mitigará la sícofancia. La mediana geométrica de los decentes LLM se dirige hacia el cúmulo honesto cuando la monocultura es menos de la mitad de la población.

> 预期输出:一张(攻击,聚合器) -> 终极答案的表格,正确答案高亮显示――多数投票在单一文化案例中失败――CPWBFT's confidence increase eased──当单一文化不到半小时,DecentLLMs'几何中位数趋向诚实──

## Usalo.

`outputs/skill-consensus-designer.md`diseña un protocolo de consenso para un conjunto de múltiples agentes: método de agrupamiento, ponderación, umbral y política de escalada para las rondas de subumbral.

> `outputs/skill-consensus-designer.md`Por tanto, el grupo de agentes de diseño de acuerdo: métodos de agrupación, peso, valor y estrategias de promoción de la categoría de valores inferiores a la de la categoría de valores.

## Envíalo .

Antes de enviar cualquier mecanismo de consenso:

- **Attack-test with at least the three patterns**Su protocolo debe fallar de manera predecible, no silenciosamente.
  En inglés:**至少用上述三种模式进行攻击测试。**Tu acuerdo debería ser un fracaso predecible, no un fracaso silencioso.
- **Log every minority cluster**Los grupos minoritarios son su sistema de alerta temprana para errores correlacionados.
  En inglés:**记录每个少数派簇** sus orígenes ∼ minoría ∼ es el sistema de previo al error de tu relación ∼
- **Enforce bounded rounds.**No "continuar el debate hasta un acuerdo" que recompensa la sicofanía.
  En inglés:**强制限制轮次。**No hagas el debate hasta que estés de acuerdo.
- **Separate agreement from correctness.**La salida de consenso se dirige a un verificador; el verificador es independiente del conjunto.
  En inglés:**分离一致性和正确性。**共识输出交给验证器;验证器 independiente de la colección.
- **Monitor the agreement rate.**Un aumento agudo significa sesgo de conformidad; una caída aguda significa deriva del modelo.
  En inglés:**监控一致率。**El aumento acelerado significa la diferencia entre los grupos; la disminución acelerada significa la movilidad del modelo.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`.Confirmar la pluralidad fracasa el ataque de la monocultura pero CPWBFT lo mitigará parcialmente cuando la confianza de la monocultura es inferior a 0,7.
   Traducción:运行`code/main.py` Confirmar que la mayoría de los votos en el ataque a la cultura única no logró, pero cuando la confianza en la cultura única fue inferior a 0,7 horas, la parte del CPWBFT alivió el problema.
2. Añadir un cuarto patrón de ataque:**silent abstention** un agente se niega a responder ("no sé"). ¿Cómo debe tratar cada agregador las abstenciones?
   En inglés, el nombre de la organización es "Creación de la Unión Europea".**静默弃权** Un agente  rechazó responder  "I don't know")  Cada aglomerador debe tratar el abandono?
3. Cambiar el agrupamiento semántico de la canonización de cadenas a la similitud de incorporación (utilice cualquier modelo de incorporación de código abierto). ¿Qué sucede con el ataque de sícofancia?
   La traducción del idioma chino es:将语义聚类从字符串规范化替换为嵌入相似度 (incluyendo cualquier modelo de emblemas de código abierto)
4. Leer CP-WBFT (arXiv:2511.10400). Implementar el paso de calibración de la sonda de confianza (un modelo de calibración separado verifica la confianza autoinformada de cada agente). Medir el aumento de precisión en el escenario de monocultivo.
   La evaluación de la calidad de la calidad de los productos y servicios de la industria de la información (en inglés, "CPC") se ha desarrollado en el sector de la información y la información.
5. Leer "¿Pueden los agentes de IA estar de acuerdo?" (arXiv:2603.01213). Reproduce un experimento simplificado de acuerdo escalar: tres agentes, una pregunta escalar, la persona engañosa. ¿CFPBFT o DecentLLMs lo captan?
   En el caso de los agentes de inteligencia artificial, ¿podría un agente de inteligencia artificial alcanzar una conformidad?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Más Leer más Leer más

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) la fundación
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) Peso de los votos por confianza
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) Agregación geométrica-mediana
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) División de núcleo/ borde para latencia limitada
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) Fragilidad de los acuerdos escalares y ataque de persona engañosa
