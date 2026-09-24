# Los modos de fracaso  MAST, pensamiento grupal, monocultura, errores en cascada 失败模式 群体思维 MAST

> La taxonomía de referencia para 2026 es **MAST**(Cemri et al., NeurIPS 2025, arXiv:2503.13657), derivado de 1642 rastros de ejecución en 7 MAS de código abierto de última generación que muestran **41–86.7% failure rate**. Tres categorías raíces: **Specification Problems**(41,77%)  ambigüedad de rol, definiciones poco claras de tareas; **Coordination Failures**(36,94%)  fallos de comunicación, dessincronización de estado; **Verification Gaps**(21,30%)  falta de validación, falta de controles de calidad.**Groupthink**La familia (arXiv:2508.05687) añade: colapso de la monocultura (el mismo modelo base → fallos correlacionados), sesgo de conformidad (los agentes refuerzan los errores de los demás), teoría de la mente deficiente, dinámica de motivos mixtos, fallos de fiabilidad en cascada. Ejemplo en cascada: tormentas de retoma en las que un fallo de pago desencadena retomas de pedidos, que desencadena retomas de inventario, que abruman el servicio de inventario (10 veces la carga en segundos  necesita interruptores de circuito). Envenenamiento de la memoria: la alucinación de un agente entra en la memoria compartida, los agentes aguas abajo la tratan como un hecho; la precisión se descompone gradualmente, haciendo doloroso el diagnóstico de la causa raíz.**STRATUS**(NeurIPS 2025) informa una mejora de 1.5 veces en la mitigación y el éxito a través de agentes especializados de detección / diagnóstico / validación.

> **【中文解读】**Este artículo presenta el modelo de fracaso de múltiples agentes y el modelo de fracaso de los grupos de pensamientos de múltiples agentes  sistemas 

> **【拓展：failure modes mast groupthink→具体应用】**Más agentes  sistemas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·13-15(共享内存/BFT/投票) ――MAST = 2026 多 Agent 失败模式的标准分类法──
> ¿ Qué es esto ?**【类比】**MAST 失败分类 = "hospital急诊分诊"──三类根因:规格问题(42%角色不清)、协调失败(37%通信失灵)、验证缺失(21%无质检)──MAST 1642 条 痕迹 显示 41-87% 失败率多 Agent 不是银弹──Groupthink 家族:单一文化崩(同基模型 全错)、群体盲从级付联错支(修失触发重试风暴,10 秒 10 倍负载)──重复:异见代理 + 随机化发言顺序 + 断路器──
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

Los sistemas multi-agentes fallan en 41-86,7% del tiempo en tareas reales (Cemri et al. 2025 midió esto en 7 MAS de código abierto). Eso no se puede deshacer por "solo agregar más agentes". Los fallos tienen causas estructurales. La taxonomía MAST le da las categorías. Esta lección mapea cada categoría a un patrón concreto de detección, diagnóstico y mitigación para que los números dejen de parecer arbitrarios.

> Más agentes  sistemas en tareas reales 41-86.7% del tiempo fracasa  Cemri  et al. 2025 en 7 开源 MAS 上测量) ⋅ Esto no es " añadir más agentes " en el proceso de prueba ⋅ fracaso tiene una causa estructural ⋅ MAST 类法给你类 ⋅ Este curso traerá cada clase a un modelo concreto de análisis, diagnóstico y alivio ⋅

La práctica de producción 2026 es tratar los modos de falla como entradas de diseño.

> La práctica de producción de 2026 es un modelo que no va a funcionar en el diseño de la entrada. Su estructura no es "lo suficientemente buena" hasta que pueda dirigirse a cada clase MAST y decir que su implementación de medidas de alivio.

## Concepto de la esencia de la concepción

### Categorías de MAST

**Specification Problems (41.77% of failures).**La tarea del agente no fue definida lo suficientemente estrictamente.

> **规范问题（41.77% 的失败）。**La misión del agente se define no suficientemente estrechamente. ejemplos:

- Ambigüedad de rol: dos agentes piensan que son los revisores.
  Dos agentes se consideran a sí mismos como revisores.
- La tarea se especificó: "resumir esto" cuando el usuario quería un ángulo específico.
  En el caso de los usuarios, el usuario quiere un punto de vista específico.
- Criterios de éxito implícitos: el agente no puede decir si ha tenido éxito.
  En inglés, el nombre de la persona que ha logrado el éxito es el de la persona que ha logrado el éxito.

Mitigación:

> 缓解措施:

- Escriba contratos de rol explícitos. El aviso de cada agente indica lo que hace *y lo que no hace*.
  Traducción:Notificación de los papeles de cada agente.
- Pruebas de aceptación por tarea. Antes de que el agente comience, define "hacido parece X".
  En el principio, se definió "completado de la forma es X".
- Verificación de especificaciones antes del vuelo: un agente separado revisa la definición de tarea antes de su expedición.
  Previo examen de las normas de control: agente independiente en la misión de control definido.

**Coordination Failures (36.94%).**Comunicación o averías de estado.

> **协调失败（36.94%）。**通信或状态故障──

Ejemplos:

> Ejemplo:

- Dos agentes actualizan el estado compartido sin sincronización.
  Traducción:Duos agentes 不同步地更新共享状态──
- Mensaje perdido entre agentes (fallo de cola, tiempo de espera).
  En inglés, el nombre de la persona que se encuentra en el sitio web es el nombre de la persona que se encuentra en el sitio web.
- Drift de estado: el agente A cree que la tarea está hecha; el agente B todavía está ejecutando.
  En inglés, "Agent A 认为任务完成;Agent B 还在执行──" se dice también "Agent A 认为任务完成".

Mitigación:

> 缓解措施:

- Estado compartido con una concurrencia optimista.
  Traducción:Band乐观并发的版本化共享状态.
- Reconocimiento explícito de los mensajes críticos (retrasar hasta que se haya aclarado).
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Puntos de control periódicos de sincronización de estado; detecta la deriva temprano.
  En el caso de los primeros años de la vida, el estado de la persona se ha vuelto más difícil.

**Verification Gaps (21.30%).**No hay control independiente de las salidas.

> **验证缺口（21.30%）。**No hay controles independientes de la producción.

Ejemplos:

> Ejemplo:

- Un agente afirma el éxito; nadie lo verifica.
  Un agente 声称成功;没人验证──
- Cada cadena de agentes confía en la producción del prior.
  En inglés, "Agent" significa "Agent" en inglés, "Agent" en inglés significa "Agent" en inglés.
- La cobertura de pruebas faltan en el comportamiento compuesto emergente.
  La situación de la población en el país se ha vuelto más difícil.

Mitigación:

> 缓解措施:

- Agente de verificación independiente (lección 13). Acceso de fuente independiente, sólo para lectura.
  En inglés, el nombre de la persona que se encuentra en el sitio web de la compañía es el nombre de la persona que se encuentra en el sitio web.
- Contrato de entrega explícito: "La salida de A debe pasar el control C antes de que comience B".
  China:                                                                                                                                                                                                                                                              
- Registro de resultados para análisis post hoc.
  En el caso de los resultados, el resultado es el resultado de la investigación.

### La familia de pensamiento de grupo (arXiv:2508.05687)

Cinco fallas relacionadas cuando los agentes se homogenizan o se imitan entre sí:

**Monoculture collapse.**El mismo modelo base o datos de formación → errores correlacionados. Cuando tres agentes comparten un LLM, comparten sus alucinaciones.

**Conformity bias.**Los agentes se adaptan al compañero más fuerte o más seguro, incluso cuando están equivocados.

**Deficient ToM.**Los agentes no pueden modelar las creencias de los demás; la coordinación se desmorona (lección 18).

**Mixed-motive dynamics.**Los agentes con incentivos parcialmente alineados se mueven hacia el medio de compromiso, lo que no satisface a nadie.

**Cascading reliability failures.**El patrón de error de un componente desencadena patrones de error en componentes dependientes.

### Ejemplo en cascada  la tormenta de retiro

Un patrón clásico de incidentes de 2026:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

La solución es clásica:**circuit breakers**Cuando la tasa de error en el torrente inferior exceda el umbral, cortocircuito con resultados almacenados en caché o por defecto.

Los interruptores de circuito son una de las pocas mitigantes de fallas multi-agentes que tomas prestadas directamente de sistemas distribuidos sin modificaciones.

### Envenenamiento por memoria (revisado)

Desde la lección 13: la alucinación de un agente se convierte en un hecho de memoria compartida; los agentes en aguas posteriores razonan sobre el hecho envenenado.

El síntoma es una degradación gradual de la precisión.

Mitigation: sólo adjunta registro, procedencia, verificador no escriturable. ya cubierto en la lección 13.

### STRATUS  agentes especializados para la detección de fallos

STRATUS (NeurIPS 2025) informa una mejora de 1,5 veces en el éxito de mitigación cuando se implementa:

- **Detection agent.**Reloj para patrones de síntomas (alto desacuerdo, picos de retoma, deriva de precisión).
- **Diagnosis agent.**Dados los síntomas, se deduce la causa raíz probable de la taxonomía MAST.
- **Validation agent.**Después de aplicar una mitigación, compruebe si los síntomas desaparecen.

Esta es una respuesta a incidentes de estilo SRE, aplicada a los sistemas de agentes.

### La auditoría en modo de falla

Las mejores prácticas para 2026 son una auditoría anual (o por liberación mayor) en el modo de falla:

1. **Trace sample.**Recoge 1000 huellas reales de ejecución.
2. **Categorize.**Para los fallos de cada rastro, mapa a las categorías MAST + Groupthink.
3. **Compute failure-by-category rate.**¿Qué categorías dominan su sistema?
4. **Rank mitigations.**¿Cuál solución eliminaría la mayoría de los fracasos?
5. **Pick 2-3 mitigations.**Implementación; reevaluación en el próximo trimestre.

La disciplina es más importante que las elecciones específicas. sin auditorías, los fracasos se mezclan en ruido y nunca se abordan sistemáticamente.

### Cuando los sistemas fallan silenciosamente

La categoría de fallas más peligrosa es la falla de corrección silenciosa. Un sistema que falla en voz alta (crash, excepción, alerta) se puede monitorear. Un sistema que produce resultados plausibles pero incorrectos no se puede detectar por registros de excepciones. Esta es la razón por la cual las lagunas de verificación son la categoría más cara por fallo aunque son solo del 21,30% en cuenta.

Invertir en:
- Revisas humanas basadas en muestras.
- Pruebas de regresión de conjunto de datos dorados.
- Controlo entre agentes de resultados importantes.

### El fracaso vs el fracaso lento

Algunos fallos son inmediatos; otros son lentos. Los fallos inmediatos (tiempo de espera, desajuste de esquema, error de autor) son baratos de detectar. Los fallos lentos (intoxicación de memoria, deriva de monocultura, ambigüedad de rol) son costosos de detectar y prevenir.

El movimiento de ingeniería 2026: los proxies de fallos lentos de los instrumentos para que pueda capturar la deriva antes de que se convierta en un error visible.

## Construye con movimiento.
```figure
a5-retry-cascade
```

## Construye el mismo

`code/main.py`los instrumentos:

- `FailureTaxonomy` categorizará los incidentes simulados en categorías de MAST + Groupthink.
- `CircuitBreaker` patrón clásico; se abre cuando la tasa de error excede el umbral.
- `RetryStormSimulator` muestra el fallo en cascada; enciende o apaga el interruptor.
- `DetectionAgent` matching de síntomas de estilo STRATUS.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Producción esperada:
- Tormenta de nuevo sin interruptor de circuito: los errores de inventario explotan (simulados).
- con interruptor de circuito: tapa en el umbral; se sirven respuestas en modo degradado.
- el agente de detección marca el patrón y nombra la categoría MAST.

## Usalo.

`outputs/skill-mast-auditor.md`ejecuta una auditoría de modo de falla de estilo MAST en un sistema multiagente.

## Envíalo .

Disciplina en el modo de fallo en la producción:

- **MAST audit per quarter.**Las categorías cambian a medida que tu sistema crece.
  En inglés:**每季度 MAST 审计。**No es anual. Clasificación crece y cambia con el sistema.
- **Circuit breakers everywhere.**Cada llamada de salida a cualquier servicio dependiente.
  En inglés:**到处都是熔断器。**Cada servicio de dependencia de la salida de la estación de servicio de la estación de dependencia de la estación de dependencia de la estación de dependencia de la estación de dependencia de la estación de dependencia de la estación de dependencia de dependencia de la estación de dependencia de dependencia de la estación de dependencia de dependencia de la estación de dependencia de dependencia de la estación de dependencia de dependencia de la estación de dependencia de dependencia de dependencia de la estación de dependencia de dependencia de dependencia de dependencia de dependencia de la estación de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependenciación de dependencia de dependencia de dependencia de dependencia de dependencia de dependencia de dependenciación de dependencia de dependencia de dependencia de dependencia de dependencia de la región de dependencia de dependencia de dependencia de dependencia de dependencia de la región de dependencia de dependencia de dependencia de la región de dependencia de dependencia de dependencia de dependencia de la región de dependencia de dependencia de dependenciación de dependencia de la región de dependencia de la región de dependencia de dependencia de dependencia de la región de depencia de depencia de la región de depencia de la región de depencia de la región de depencia de depencia de depenciación de depencia de la región de depencia de depencia de la región de depencia de la región de depencia de la región de depenciación de depencia de depenciación de la región de dep
- **Golden datasets.**Pequeña, de alta calidad, auditada a mano, prueba de regresión contra ellos semanalmente.
  En inglés:**黄金数据集。**La investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de los resultados de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de los resultados de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de
- **STRATUS trio.**Detección + diagnóstico + agentes de validación que monitorean la producción.
  En inglés:**STRATUS 三重奏。**检测 + 诊断 + 验证代理 监控生产――从检测代理 开始;当症状杂时添加诊断――
- **Failure budget.**Explicito SLO para la tasa de fracaso por categoría.
  En inglés:**失败预算。**按类别失败率显然SLO──超出预算触发停止发言对话──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar el interruptor de circuito, volver a intentar la tormenta, cambiar el umbral de falla y observar el cambio.
2. Implementar una **slow-failure proxy**Cuando cae de forma brusca, activa una alerta Simula una deriva de monocultivo correlacionando gradualmente las salidas de los agentes.
3. Leer Cemri et al. (arXiv:2503.13657). elige uno de sus 7 sistemas MAS y mapea sus 3 principales categorías de fallos. ¿Cómo se comparan estos con lo que predice MAST?
4. En el artículo de GrupoTexto (arXiv:2508.05687) se indica cuál de los cinco patrones es más difícil de detectar en la producción.
5. Diseñar un trio de detección-diagnóstico-validación al estilo STRATUS para un sistema multi-agente específico que usted conoce. ¿Qué síntomas vigila la detección? ¿Qué mitigantes recomienda el diagnóstico? ¿Cómo confirma la validación que funcionan?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Más Leer más Leer más

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomía MAST, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) monocultura, conformidad y taxonomía de cinco familias
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) Entrada en el procedimiento NeurIPS 2025 (detección + diagnóstico + validación)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) la referencia canónica del interruptor de circuitos
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notas de fallas de producción
