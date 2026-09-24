# Las economías de los agentes, los incentivos de tokens, la reputación.

> Los agentes autónomos de largo horizonte (la curva de trabajo de 1 a 8 horas de METR) necesitan una agencia económica.**5-layer stack**es: **DePIN**(computación física) → **Identity**(DIDs de la W3C + capital de reputación) → **Cognition**(RAG + MCP) → **Settlement**(abstracción de cuentas) → **Governance**Las redes de incentivos a los agentes de producción incluyen:**Bittensor**(Las subredes de TAO recompensan modelos específicos de tareas), **Fetch.ai / ASI Alliance**(Token de ASI-1 Mini LLM + FET), y **Gonka**Trabajo académico: los usos descentralizados de LaMAS de AAMAS 2025 **Shapley-value credit attribution**Para recompensar justamente a los agentes que contribuyen; Google Research propone "Design Mechanism for large language models" **token auctions**Esta lección construye un mercado de agentes mínimo, aplica la atribución de crédito de valor Shapley a una tubería de agentes múltiples y ejecuta una subasta de tokens de segundo precio para que la maquinaria de teoría de juegos aterrice concretamente.

> **【中文解读】**Este apartado presenta el mecanismo de intercambio de recursos en el sistema de agentes economía más agentes precio y mercado 

> **【拓展：agent economies→具体应用】**Agente  economía de análisis  mecanismo de distribución y incentivo de recursos en el sistema                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 16 (Negotiation and Bargaining), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 16（协商与讨价还价），Phase 16 · 09（并行群体网络）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·16(协商) 、Fase 16·09(Swarm) 、 mecanismo diseño基础(Shapley 值、拍卖理论) ⋅Agent 经济 = 多 Agent 系统的市场层。
> ¿ Qué es esto ?**【类比】**Agente 经济 = "AI 自由市场"──5 层:DePIN(算力) + 身份(DID+声誉) + 认知(RAG+MCP) + 结算(账户抽象) + 治理(Agentic DAO)。Bittensor 子网奖励专门模型,Fetch.ai utiliza ASI-1 Mini + FET token,Gonka utiliza transformador PoW 把算力导向生产任务――学术:Shapley 给多 Agent 公平分、二价 拍卖防操纵――
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

Los sistemas multi-agentes se complican cuando los agentes producen valor conjuntamente pero necesitan ser recompensados individualmente. Los mecanismos clásicos  división igual, último contribuyente-tomará-todo  son injustos o jugables. La recompensa basada en la coalición a través de los valores de Shapley es justa por construcción pero costosa para calcular. La literatura 2025-2026 impulsa aproximaciones útiles: muestreo de Shapley, subastas de agregación monótona y reputación en cadena que se acumula a partir de contribuciones confirmadas.

> El sistema de múltiples agentes genera valor en conjunto con el agente, pero se complica cuando se necesita una recompensa individual. El mecanismo clásico es que el último contribuyente es totalmente injusto o manipulable. La recompensa de valor de Shapley basada en la alianza es justa pero calculada. La literatura de 2025-2026 promueve un enfoque útil: Shapeley 采样"",single mode aggregation auction" y la reputación acumulada en la cadena de contribuciones confirmadas.

Más allá de la atribución de crédito, el campo se ha vuelto a agentes económicos reales: Bittensor TAO recompensa la computación minera para ajustar los modelos específicos de subredes, Fetch.ai/ASI recompensa el uso de ASI-1 Mini LLM con tokens FET, Gonka reasigna la prueba de trabajo de transformador hacia tareas productivas de IA.

> 超越信用归因, el campo se ha convertido hacia un verdadero agente económico:Bittensor TAO 奖励挖掘计算来微调子网特定模型,Fetch.ai/ASI con ficha FET 奖励 ASI-1 Mini LLM 使用,Gonka transformará 工作量证明重新分配到生产性 AI 任务;;Agent de comercio autónomo ya existe; el problema es cómo hacer frente a los incentivos;;

Esta lección trata las economías de agentes como una familia de problemas específicos  atribución de crédito, diseño de mecanismos y reputación  y construye cada uno con la matemática mínima para que las ideas se adhieran.

> Este curso examinará a los agentes económicos como un problema específico de la atribución de crédito, el diseño de mecanismos y la reputación y utilizará la menor cantidad de matemáticas para construir cada uno de ellos, para que el concepto sea realmente entendido.

## Concepto de la esencia de la concepción

### La pila de cinco capas de agente-economía

1. **DePIN (physical compute).**Infraestructura descentralizada que alquila GPU, almacenamiento, ancho de banda, subredes de Bittensor, Render Network, Akash, no es específico para el agente, los agentes lo usan.
   En inglés:**DePIN（物理计算）。**租 GPU、存储、带宽的去中心化基础设施──Bittensor 子网、Render Network、Akash──非代理 专用;Agent 使用它──
2. **Identity.**Los identificadores descentralizados (DID) de W3C dan a cada agente un ID duradero independiente de cualquier plataforma. La reputación se acumula en el DID. El protocolo de red de agentes (ANP) utiliza el DID como la capa de descubrimiento.
   En inglés:**身份。**W3C 去中心化标识符(DID) da a cada agente un ID permanente independiente de la plataforma。 reputación acumulada hasta DID。Agent 网络协议(ANP) utiliza DID 作为发现层。
3. **Cognition.**El bucle de razonamiento del agente: LLM + RAG + MCP. Esto es lo que construyen las otras fases.
   En inglés:**认知。**El ciclo de la teoría del agente: LLM + RAG + MCP.
4. **Settlement.**La abstracción de cuentas (ERC-4337) permite a los agentes pagar el gas de sus propios saldos sin tener ETH.
   En inglés:**结算。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
5. **Governance.**Los DAO agenciales: estructuras de gobierno donde los humanos *y* agentes votan sobre cambios en el protocolo, con poder de voto vinculado a la reputación.
   En inglés:**治理。**Agente DAO: humanos* y* Agente para el acuerdo de cambio de estructura de gobierno, derecho a voto y reputación vinculado.

No todos los sistemas de producción utilizan los cinco. Bittensor utiliza 1, 2, parcialmente 3, parcialmente 4, ninguno de 5. Los agentes OpenAI no utilizan ninguno excepto 3.

### Bittensor, Fetch.ai, Gonka  lo que corre

**Bittensor (TAO).**Las subredes son tareas especializadas (modelado de lenguaje, generación de imágenes, pronóstico). Los mineros envían resultados de modelos. Los validadores los clasifican; la puntuación ponderada por apuestas distribuye las recompensas de TAO. Cada subred tiene su propia evaluación. La lección económica: pagar por la calidad de la salida específica de la tarea, no el cálculo utilizado.

**Fetch.ai / ASI Alliance.**ASI-1 Mini LLM se ejecuta en la red de Fetch.ai; los usuarios pagan tokens FET para inferir. La narrativa de agentes como pares es más fuerte aquí: un agente en Fetch puede llamar a otro para una tarea y pagar en FET.

**Gonka.**Prueba de trabajo de transformador: el "trabajo" es los pases anteriores de un transformador. Los mineros ganan ejecutando tareas de inferencia que han conocido las salidas correctas (a partir de datos de entrenamiento).

Los tres son de producción a partir de abril de 2026. La distribución de pagos difiere.

### Atribución de crédito por valor de Shapley

Tres agentes colaboran en una tarea. ¿Quién contribuyó a qué?

Valor de Shapley: la asignación única de créditos que satisface cuatro axiomas (eficiencia, simetría, linealidad, nulo).`i`¿Qué es esto ?

```
shapley(i) = (1/N!) * sum over all orderings O of (v(S_i_O ∪ {i}) - v(S_i_O))
```

donde`S_i_O`es el conjunto de agentes antes `i`en orden `O`En la práctica: enumerar todas las permutaciones, registrar la contribución marginal de cada agente en cada permutación, promedio.

Para N=3 agentes, hay 6 permutaciones. para N=10, 3.6M  así que en la práctica se muestran ordenes en lugar de enumerar.

### Subastas de segundo precio para agregación

Google Research ("Diseño de Mecanismo para grandes modelos de lenguaje") propone subastas de tokens de segundo precio para agregar los resultados de LLM. Configuración: N agentes proponen cada uno una finalización; cada uno tiene un valor privado para ser seleccionado. El subastador elige la propuesta de mayor valor y paga el *segundo valor* más alto. En la agregación monótona (el valor depende de qué propuesta se elige, no de cuántos se ofrecieron), esto es cierto  los agentes ofrecen su verdadero valor.

Por qué esto es importante para los sistemas de LLM: puede externalizar las tareas de finalización a múltiples agentes con precios diferentes; la subasta elige el mejor + paga justamente, y los agentes no tienen ningún incentivo para informar incorrectamente.

### Capital de reputación

Una puntuación de reputación vinculada a DID se acumula a partir de contribuciones confirmadas.

```
rep(i, t+1) = alpha * rep(i, t) + (1 - alpha) * contribution_quality(i, t)
```

Con factor de descomposición`alpha`Propiedad:

- Es barato de leer para las decisiones de enrutamiento ("enviar tareas difíciles a agentes de alta reputación").
- Es costoso de forjar (se acumula con el tiempo, vinculado a DID).
- Se puede reducir: las contribuciones que no logren la verificación se restan.

### AAMAS 2025 LaMAS descentralizada

La propuesta de LaMAS (AAMAS 2025) combina: identidad DID, atribución de crédito de valor Shapley y un mecanismo de subastas simple.

### Cuando la economía se desmorona

- **Price oracle manipulation.**Si la función de crédito puede ser jugada, los agentes lo jugarán.
- **Sybil attacks.**Un operador hace que N agentes falsos inflen su propia contribución.
- **Verification cost.**La atribución de crédito es tan justa como el verificador.Si la verificación es barata (LLC pequeña), puede ser jugada; si es cara (panel humano), el sistema no se escala.
- **Regulatory overhang.**Las economías de los agentes se cruzan con la regulación financiera. Bittensor, Fetch y Gonka operan en áreas grises legales en algunas jurisdicciones a partir de 2026.

### Cuando las economías de agentes tienen sentido

- **Open networks with heterogeneous operators.**Ningún equipo controla a todos los agentes.
- **Verifiable outputs.**Sin verificación, la atribución de crédito es una conjetura.
- **Long-horizon workflows.**Las tareas de un solo tiro no se benefician de la acumulación de reputación.
- **Tokenized payments are legally viable**en su jurisdicción.

En los sistemas corporativos cerrados, la economía deja paso a una asignación más simple (los gerentes asignan trabajo, las métricas son internas).

## Construye con movimiento.
```figure
swarm-auction
```

## Construye el mismo

`code/main.py`los instrumentos:

- `shapley(value_fn, agents)` cálculo exacto de Shapley por enumeración para N pequeño.
- `second_price_auction(bids)` mecanismo verdadero; el ganador paga el segundo más alto.
- `Reputation` Reputancia vinculada a DID con decadencia exponencial y recorte.
- Demo 1: tres agentes colaboran, exactamente Shapley atribuye crédito.
- Demo 2: cinco agentes ponen una oferta para una ranura de tareas; la subasta de segundo precio elige el ganador + pago.
- Demo 3: 100 rondas de asignación de tareas a agentes con repetición heterogénea; el enrutamiento ponderado por repetición golpea al azar.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Producción esperada: valores de Shapley para cada agente; resultado de la subasta que muestra equilibrio de la oferta verdadera; enrutamiento ponderado por repetición que muestra una ganancia de calidad del 10-20% sobre el azar después del calentamiento.

## Usalo.

`outputs/skill-economy-designer.md`diseña una economía de agente mínima: elección de la capa de identidad, mecanismo de atribución de crédito, mecanismo de pago, regla de reputación.

## Envíalo .

Dirigir una economía de agentes en 2026:

- **Start with reputation, not tokens.**La reputación es barata de implementar y valiosa sola; los tokens añaden complejidad legal y económica.
  En inglés:**从声誉开始，不是 token。** la reputación de lograr un precio barato y un valor único;  la creciente complejidad jurídica y económica
- **Verify before you reward.**Nunca distribuir crédito sin una etapa de verificación independiente.
  En inglés:**先验证再奖励。**没有独立验证步骤永远不要分配信用――自报质量会积累女巫博──
- **Shapley-sample, not Shapley-exact.**Muestra de 100-1000 ordenes; la enumeración exacta no es escalable.
  En inglés:**Shapley 采样，而非 Shapley 精确。**采样 100-1000 个排序; 精确枚举不可扩展──
- **Cap decay factor and floor reputation.**La descomposición ilimitada borra a los contribuyentes legítimos; la descomposición demasiado lenta recompensa a los agentes obsoletos de alta reposición.
  En inglés:**限制衰减因子和最低声誉。**无界衰减抹抹合法贡献者; 太慢的衰减奖励过时的高声誉代理──
- **Audit mechanisms adversarially.**Ejecutar escenarios de equipo rojo antes de abrir la red. Cada mecanismo tiene una teoría de juego; quieres encontrar los agujeros, no los atacantes.
  En inglés:**对抗性审计机制。**开放网络前运行红队场景── cada mecanismo tiene un problema; tú quieres encontrar la falla, no un atacante──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar la suma de valores de Shapley al valor total (axioma de eficiencia). Cambiar la función de valor; ¿cambian las asignaciones de Shapley en la dirección esperada?
2. Implemente Shapley *sampling* (Monte Carlo sobre K ordenes). ¿Cómo afecta K a la precisión de aproximación?
3. Implementar un paso de formación de coalición antes de la subasta: los agentes pueden fusionarse en equipos y licitar como una unidad. ¿Qué coaliciones forman? ¿Es el resultado Pareto mejor que la licitación individual?
4. Leer el post de diseño de mecanismos de Google Research. Identifique una suposición que, si se viola, rompe la veracidad. ¿Cómo se ve ese modo de fracaso en un entorno de LLM?
5. Leer el documento LaMAS descentralizado de AAMAS 2025. Implemente su paso Shapley sobre 10 agentes en una tarea sintética. ¿Cuánto tiempo tarda el cálculo exacto? ¿Qué tan cerca se acerca el muestreo con 100 tiros?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| DePIN / 去中心化物理基础设施 | "Decentralized physical infrastructure" / "去中心化物理基础设施" | Token-incentivized compute/storage/bandwidth. Bittensor, Akash, Render. / Token 激励的计算/存储/带宽。Bittensor、Akash、Render。 |
| DID / 去中心化标识符 | "Decentralized identifier" / "去中心化标识符" | W3C spec for portable IDs. Agent reputation binds to DID, not to a platform. / W3C 便携 ID 规范。Agent 声誉绑定到 DID，而非平台。 |
| ERC-4337 / 账户抽象 | "Account abstraction" / "账户抽象" | Contract accounts that can sponsor gas, enabling agent payments. / 可以赞助 gas 的合约账户，使 Agent 支付成为可能。 |
| Shapley value / Shapley 值 | "Fair credit attribution" / "公平信用归因" | Unique allocation satisfying efficiency, symmetry, linearity, null. / 满足效率、对称、线性、零贡献者的唯一分配。 |
| Second-price auction / 二价拍卖 | "Vickrey auction" / "Vickrey 拍卖" | Truthful mechanism: winner pays second-highest bid. Monotone aggregation compatible. / 诚实机制：获胜者支付第二高出价。兼容单调聚合。 |
| Reputation capital / 声誉资本 | "Accumulated quality score" / "累积质量分数" | DID-bound score from confirmed contributions; decays over time. / DID 绑定的来自确认贡献的分数；随时间衰减。 |
| Agentic DAO / Agent DAO | "Agents + humans govern" / "Agent + 人类治理" | DAO with agent voters as first-class, voting power tied to reputation. / Agent 投票者作为一等公民的 DAO，投票权与声誉绑定。 |
| TAO / FET / GPU credits / Token 面额 | "Token denominations" / "Token 面额" | Bittensor TAO, Fetch.ai FET, various DePIN tokens. / Bittensor TAO、Fetch.ai FET、各种 DePIN token。 |

## Más Leer más Leer más

- [The Agent Economy](https://arxiv.org/abs/2602.14219) Encuesta de 2026 de la pila de cinco capas de agentes-economía
- [Google Research — Mechanism design for large language models](https://research.google/blog/mechanism-design-for-large-language-models/) Subastas simbólicas con agregación monótona
- [AAMAS 2025 — decentralized LaMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2896.pdf) Atribución de crédito por valor de Shapley
- [Bittensor TAO documentation](https://docs.bittensor.com/) La estructura de la subred y la distribución de las recompensas
- [Fetch.ai / ASI Alliance](https://fetch.ai/) ASI-1 Mini LLM y FET token
- [W3C Decentralized Identifiers (DIDs) spec](https://www.w3.org/TR/did-core/) Fundación de identidad
