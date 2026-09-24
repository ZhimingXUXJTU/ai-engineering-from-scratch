# Memoria compartida y patrones de tablero negro.

> En 2026 coexistirán dos enfoques en los sistemas multiagentes: el **message pool**(todo el mundo ve los mensajes de todos, como en AutoGen GroupChat o MetaGPT) y el **blackboard with subscription**(los agentes se suscriben a eventos relevantes, como en el MCP Context-Aware o el marco de Matrix). Ambos son la única parte de estado de un sistema multi-agente  lo que significa que ambos son donde viven los errores interesantes.**memory poisoning**El estudio de la teoría de la alucinación de un "hecho" en una serie de estudios de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los resultados de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los resultados de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los resultados de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la

> **【中文解读】**Este capítulo presenta la memoria compartida y el mecanismo de coordinación en el sistema de múltiples agentes.

> **【拓展：shared memory blackboard→具体应用】**El modelo de memoria compartida/blackboard es el mecanismo de coordinación clásico de múltiples agentes 系统 todos los agentes 读写一个共享知识库――黑板模型起源于1980s Hearing-II 语音识别系统――现代实现包括Redis共享状态、向量数据库和MCP Resources――优势是简单,劣势是竞争条件(多个代理 同时写入) ――


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04(原语)、Fase 16·09(Swarm)、并发编程(锁、竞态)。共享记忆 = 多 Agent 协调的核心数据结构──
> ¿ Qué es esto ?**【类比】**共享记忆两种模式 = "办公场景"──消息池(AutoGen GroupChat) = 开放办公区(大家都听);黑板+订阅(Context-Aware MCP) = 公告板(按订阅推送)──失败模式 = 记忆投毒(Un agente 幻觉, otro agente 当真) 比崩更难调试──修复:版本号 + 来源标记 + 多源验证──

## # El problema # # El problema #

Los sistemas multi-agentes necesitan un lugar para que los agentes compartan hechos. Una opción literal es "pasar todo en mensajes"  pero que reinventa el estado compartido con copias adicionales. Otro es "dar a todos un registro global"  pero los registros globales crecen ilimitados y envenen fácilmente. Un tercero es "proyectar una vista por agente"  escalable pero con esquema pesado.

> Un tipo de opción es "transmitir todo en el mensaje" pero es como reinventar con una copia extra de la condicionalidad. Otro es "dar a cada persona un diario de la totalidad" pero el diario de la totalidad crece ilimitadamente y es fácilmente contaminado.

Las tres opciones siguen un clásico tradeoff de sistemas distribuidos: baratos pero frágiles (mensajes), simples pero no escalables (log global), escalables pero rígidos (proyecciones por agente). Ninguna opción domina.

> Tres opciones retroactivas Clásico sistema distribuido Pesas: barato pero frágil (en inglés) 消息) 简单但不可扩展 (en inglés) 整局日志) 可扩展但化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 化 (en inglés) 

Cuando uno de los agentes alucina y escribe la alucinación en estado compartido, cada agente en el torrente que lee ese estado adopta la alucinación como un hecho. Para el momento en que los humanos se dan cuenta, la cadena de razonamiento es de cinco pasos de profundidad y la causa raíz es el tercer mensaje escrito.

> Cuando uno de ellos escribe una imagen en estado compartido, cada uno de los lectores del estado se encarga de la adopción de la imagen como un hecho. Cuando el ser humano se da cuenta de que la cadena de ideas ya tiene cinco pasos, la razón fundamental es que la mayoría de los agentes tienen una disminución de precisión.

Una caída te da un rastro de pila. El envenenamiento de memoria te da un informe confidentemente incorrecto. El primero se detecta en segundos; el segundo puede tomar días de trabajo forense para rastrear la alucinación originaria.

> 崩给你堆跟踪――内存污染给你自信错误报告―― primero, unos segundos de detección; segundo, puede necesitar varios días de investigación para remontarse a la idea original―

Este es el envenenamiento de la memoria. Es la segunda familia de fallas más documentada en la taxonomía MAST (Cemri et al., arXiv:2503.13657) y es estructural: cualquier diseño de memoria compartida sin procedencia y un verificador no escriturable lo exhibirá eventualmente.

> Esto es la contaminación de la memoria. Es el segundo mayor registro en el MAST de la ley de la clase de familia fallida en casos de la familia de los que se ha perdido la memoria.

## Concepto de la esencia de la concepción

### Las dos topologías principales

**Full message pool.**Cada agente lee cada mensaje. AutoGen GroupChat y MetaGPT usan esto. Simple, transparente, inspectable, pero no se escala más allá de ~ 10 agentes porque el contexto de cada agente se llena con el trabajo de otros agentes.

> **完整消息池。**Cada Agente 读取每条消息──AutoGen GroupChat 和 MetaGPT utiliza este método──简单,透明,可检查, pero no puede extenderse a aproximadamente 10 Agentes, ya que cada Agente de arriba abajo llenará el trabajo de otros Agentes──

**Blackboard with subscription.**Los agentes declaran interés en los temas; los substratos sólo rutas mensajes relevantes. CA-MCP (arXiv:2601.11595) y el marco descentralizado de Matrix (arXiv:2511.21686) utilizan esto. Escala más, pero requiere un diseño de esquema por adelantado para hacer suscripciones significativas.

> **带订阅的黑板。**Agencia  declaraciones de interés en el tema; nivel inferior sólo vía de noticias relacionadas. CA-MCP(arXiv:2601.11595) y Matrix 去中心化框架(arXiv:2511.21686) utilizar este método.

### Cuando cada uno gana

- **Full pool**La razón por la que se dice lo que es trivial cuando todo el mundo lo ve.
  En inglés:**完整池**En el agente menor, el diálogo es corto y el diálogo es rápido. Cuando todo el mundo lo ve, la razón es simple.
- **Blackboard**Los agentes de rodaje de datos de la red de rodaje de datos de la red de rodaje de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de la red de rotación de datos de datos de datos de la red de rotación de datos de datos de datos de la red de rotación de datos de datos de datos de datos de datos de la red de rotación de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
  En inglés:**黑板**En el caso de los agentes, los papeles son iguales, pero en muchos ejemplos, los grupos son iguales.

Los sistemas de producción a menudo se mezclan: una pequeña piscina completa en la parte superior (capas de planificación), tablas negras por debajo (capas de trabajadores).

> Sistema de producción usualmente mezclado uso: encima de un pequeño conjunto de piezas (planar), abajo es un plantilla (planar), abajo es un plantilla (planar).

Este híbrido es lo que hace el sistema de investigación de Anthropic: un supervisor (un grupo completo entre unos pocos agentes principales) delega a los subjugados (cada uno su propio contexto de alcance, aislado de los hermanos).

> Esta mezcla es realizada por el sistema de investigación antropópica: supervisor (en inglés)                                                                                                                                                                                                                                                     

### Envenenamiento de la memoria, en un escenario

Tres agentes trabajan en una tarea de investigación, el agente A es un agente de recuperación, el agente B es un resumidor, el agente C es un analista.

> Tres agentes 处理一个研究任务──Agent A es inspección agente──Agent B es extracción器──Agent C es analista──

1. A trae una página y escribe un mensaje a la declaración compartida: "El estudio informa una mejora de precisión del 42%".
   China 获取一个页面并向共享状态写入消息:"Un estudio reportó un aumento del 42% en la tasa de precisión.
2. La página que se trajo en realidad decía "Mejora del 4,2%". Una alucinó una decimal.
   La página de obtención dice en realidad que "4.2% 提升──"Un fantasma de un pequeño número de puntos──.
3. B, leyendo el estado compartido, escribe: "Gran aumento de precisión del 42% reportado (fuente: A). "
   China 读取共享状态,写入:" reportó un aumento significativo del 42% 准确率提升(来源:A) 』
4. C, leyendo el estado compartido, escribe: "Recomendar la adopción  42% elevación es transformador".
   El gobierno de la República de China ha aprobado el proyecto de ley de la Unión Europea para la protección de la salud y la salud.
5. El informe final cita un número del 42% que nunca existió.
   El informe final cita un 42% de números que nunca existieron.

Ningún agente se estrelló, ninguna prueba falló, el sistema "funcionó", la alucinación pasó del contexto de un agente al razonamiento de cada agente a través del estado compartido.

> 没有 Agent 崩──没有测试失败──系统"工作"了──幻觉通过共享状态从一个代理的上下文进入了每个下游代理的推理──

Por eso el envenenamiento de la memoria es insidioso: no hay accidente, error, advertencia. El sistema produce un informe confidentemente incorrecto. La única manera de detectarlo es derivar cada hecho de fuentes primarias  que derrota el punto de tener agentes.

> Es por eso que la contaminación de memoria entra en riesgo: no hay crisis, no hay errores, no hay advertencias, no hay informes de errores de confianza del sistema, y el único método para detectarlo es redirigir cada hecho desde su origen original, lo que va en contra de la intención de poseer un agente.

### ¿Por qué esto es estructural?

Sin estado compartido, la alucinación del agente A permanece en el contexto de A. Los agentes de abajo recogerían o rederivarían y podrían atrapar el error.

> 没有共享状态,Agent A's illusion parked in A's upper down文中──下游 Agent 会重新获取或重新推导并可能捕获错误──

El problema no es el estado compartido en sí mismo  es el estado compartido **without provenance and without an independent verifier**Tres medidas de mitigación se refieren a esto:

> problemas no es el estado de compartir en sí mismo sino**没有来源追溯和没有独立验证器**El problema se ha resuelto mediante tres medidas de alivio:

Cada mitigación se dirige a un modo de falla diferente. La providencia permite rastrear errores de nuevo. La versión conserva el rastro de auditoría. El verificador no escritorio proporciona una verificación independiente. Juntos, forman una defensa profunda contra la intoxicación.

> Cada tipo de medidas de alivio contra diferentes modelos de fracaso. Fuente de rastreo hace que usted pueda rastrear errores.

1. **Attribute provenance on every write.**Cada entrada en los registros estatales compartidos quién la escribió, cuándo, bajo qué instante y (si corresponde) qué fuente citó el agente.
   En inglés:**每次写入时归属来源。**Cada artículo en el estado compartido registra quién escribió 、何時、在什么提示下、以及(si corresponde) Agente 引用什么来源──下游 Agente 根据来源以怀疑态度阅读──
2. **Version writes; treat them as append-only.**Una corrección es una nueva entrada que sustituye a la antigua, no una actualización en el lugar.
   En inglés:**版本化写入；视为仅追加。**修正是一个取代旧条目的新条条,不是原地更新──审计跟踪被保留──
3. **Keep at least one agent that cannot write to shared state.**Un agente de verificación de sólo lectura toma muestras de entradas, recoge fuentes y señala inconsistencias.
   En inglés:**保留至少一个不能写入共享状态的 Agent。**Sólo read verifier Agent 采样条目、重新获取来源并标记不一致──因为 no puede escribirse en la pila, por lo que no puede ser contaminada por la pila──

### Precedente de tablero negro (Hayes-Roth, 1985)

El patrón de la pizarra es anterior a los agentes de LLM en cuatro décadas. Hayes-Roth (1985, "Una arquitectura de tablero negro para el control") describió a las fuentes de conocimiento especializadas que observan una tablero negro global, contribuyen a soluciones parciales y desencadenan otras fuentes. La pizarra negra 2026 (CA-MCP, Matrix) es el mismo patrón con agentes LLM como fuentes de conocimiento y manchas JSON como soluciones parciales. La antigua literatura ha documentado soluciones para escribir contención, control oportunista y coherencia que los sistemas modernos redescubren.

> 黑板模式比LLM Agent早了四十年. Hayes-Roth (en 1985, "A Blackboard Architecture for Control") describió observar la totalidad de la schematicablack. Contribución de la solución y provocar otros recursos de conocimiento especializado.

La lección de Hearsay-II (la tabla de control de reconocimiento de voz de la década de 1970): control oportunista  dejando que cualquier Fuente de Conocimiento se active cuando su condición de activación coincida  produce una solución de problemas emergente.

> Escucha-II(1970s年代语音识别黑板) enseñanza: oportunidad de controlar hacer que cualquier fuente de conocimiento en su causa se ajuste a las condiciones de la causa surja problemas de solución.

### Proyección frente a vista completa

Una tabla negra pura da a cada suscriptor la misma proyección (tema-escalada).**per-agent projection**Las reducciones de estado de LangGraph son la implementación canónica de 2026  la función de reducción dobla el estado global en una rodaje específico de función.

> 純黑板給每名订阅者相同的投影 (púina黑板給每名订阅者相同的投影) ◎**每个 Agent 投影**Cada agente obtiene un estado de reglamentación de acuerdo a su papel. El estado de reglamentación de la LongGraph es un logro típico de 2026 en el que la función de reglamentación de la función se doblará en un estado general en un pedazo específico de papel.

La proyección por agente se expande más, pero necesita un esquema.

> Cada agente proyecta mejor pero necesita un modelo.

### Modelos de contenido de escritura

El problema de la concurrencia es que varios agentes escriben simultáneamente, no sólo un problema de LLM.

> Muchos agentes, al mismo tiempo, escriben un problema, no sólo LLM  problemas.

- **Sequential writer (single producer).**Todos los escritos pasan por un agente coordinador que serializa.
  En inglés:**顺序写入者（单一生产者）。**Todos los escritos se escriben a través de un agente coordinado.
- **Optimistic concurrency with versioning.**Cada entrada tiene una versión; los escritores fallan en la incompatibilidad de versiones y vuelven a intentarlo.
  En inglés:**带版本控制的乐观并发。**Cada artículo tiene una versión; el escritor en la versión no coincide cuando fracasa y vuelve a intentar.
- **Topic partitioning.**Los diferentes agentes poseen temas diferentes, no hay discusiones entre temas, requiere límites de partición diseñados.
  En inglés:**主题分区。**Diferente agente  posee diferentes temas  no tiene conflictos entre temas  necesita diseño de zonas fronteras

La mayoría de los marcos 2026 son por defecto escritores secuenciales porque las llamadas de LLM son lo suficientemente lentas como para que la contención sea rara y el cuello de botella no lastime.

> La mayoría de los estudiantes de 2026 utilizan los programas de formación en línea, ya que el LLM está bastante lento, los conflictos son pocos, y el proceso no afecta.

Cuando se alcanza una disputa (envuelo de alto rendimiento, agentes de investigación paralelas escribiendo hallazgos), la partición de temas es generalmente la solución más barata.

> Cuando realmente se encuentre en conflicto, la división de temas es generalmente la más barata de las reparaciones.

### El verificador no escriturable

La más eficaz de la mitigación es el verificador de lectura única.

> La medida de alivio más importante es sólo para el usuario.

- El verificador comparte el estado con el equipo (leer la pizarra o el grupo).
  Traducción:El experto y el equipo comparten el estado de la prueba.
- Verificador no tiene manillar de escritura para compartir estado  sólo a un canal de verificación separado.
  Traducción:El verificador no tiene un único método de verificación.
- Verificador de forma independiente busca fuentes citadas en los escritos.
  La historia de la historia de los experimentos de los Estados Unidos se ha extendido a lo largo de los años.
- Las propias salidas del verificador se envía a un humano o a un agente de decisión separado, nunca devueltas a la piscina.
  El verificador su propio salida se hace viable hacia el hombre o un agente de decisión independiente, siempre no regresa a la piscina.

Sin esta separación, las salidas del verificador se convierten en nuevas entradas en el grupo, lo que significa que un grupo envenenado envenena al verificador, lo que envenena sus verificaciones.

> Sin esta separación, la salida del verificador se convierte en el nuevo artículo del estanque, lo que significa que el estanque contaminado contaminó al verificador, contaminando así su certificado.

El principio de verificación no escriturable es el siguiente: el auditor debe ser leído únicamente con respecto al sistema que se está auditando.

> Este es el principio de un auditor: el auditor debe leer sólo el sistema de auditoría.

## Construye y realiza.
```figure
swarm-blackboard
```

## Construye el mismo

`code/main.py`Implementa ambas topologías en Stdlib Python más un ataque de intoxicación de juguete y las tres mitigaciones.

> `code/main.py`Usando la base de datos Python, se han logrado dos tipos de ataques y tres medidas de alivio de contaminación de juguetes.

- `MessagePool` Registro de sólo apéndice de hilo seguro con lectura completa.
  En inglés:`MessagePool` 线程安全的仅额日志,支持完整读取──
- `Blackboard` Pub/sub con suscripciones por agente.
  En inglés:`Blackboard`                                                                                                                                                                                                                                                              
- `ProvenanceEntry` todos los registros de escritura (escrito, timestamp, prompt_hash, source_uri).
  En inglés:`ProvenanceEntry` Cada vez que escribe un registro (s)
- `PoisoningScenario` ejecuta una tarea de investigación de tres agentes donde el agente A alucina una decimal.
  En inglés:`PoisoningScenario` 运行三 Agent 研究任务, entre los cuales el agente A 幻觉一个小数点――印印最终报告――
- `Verifier` un agente de sólo lectura que recoge las fuentes y señala las inconsistencias.
  En inglés:`Verifier` Un agente de recopilación no identificado en la misma situación en la presencia de un verificador 

Producción esperada:
- Corrida 1 (sin verificador): el 42% alucinado se propaga al informe final.
  El estudio de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los más más más más más más más.
- Corriendo 2 (con verificador): el verificador señala la inconsistencia, el grupo está etiquetado "banderado", el informe final incluye una retractación.
  China:运行 2(有验证人): el experto se ha marcado como "ha marcado", el informe final incluye la retirada.

## Usalo con el marco de ejecución

`outputs/skill-memory-auditor.md`Es una habilidad que audita el diseño de memoria compartida de cualquier sistema multi-agente para la procedencia, la versión y la separación de verificadores.

> `outputs/skill-memory-auditor.md`Es una habilidad para auditar cualquier estructura de múltiples agentes del sistema de memoria compartida en el diseño de origen, control de versión y verificación separada.

## Envíe el producto .

Para cualquier diseño de memoria compartida:

>  Para cualquier diseño de memoria compartida:

- Registra la procedencia en cada escrito: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`¿ Qué ?
  Traducción:El diario de la historia`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`¿Qué es eso?
- Las correcciones son nuevas entradas que hacen referencia a la sustituida.
  En el caso de los ejemplos de la historia, el nombre de la historia se encuentra en el idioma chino.
- Entablar al menos un agente de verificación de sólo lectura con acceso independiente a la fuente.
  China: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deployment: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying: deploying deploying: deploying deploying deploying deploying: deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deploying deplo
- La salida del verificador de ruta a un canal separado, no de vuelta al grupo compartido.
  China:                                                                                                                                                                                                                                                              
- El registro de la proporción de escritos que son superecciones  una proporción creciente es evidencia temprana de patrones de alucinación.
  La proporción de registro de cobertura de escritos  aumento de la proporción es evidencia temprana del modelo de ilusión 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirme que la primera prueba propaga la alucinación y la segunda prueba la captura.
   Traducción:运行`code/main.py`❖ Confirmar la ejecución 1  Diseminar la sensación y la ejecución 2  Capturarla 
2. Añadir una segunda alucinación: el agente B inventa un conjunto de datos de tamaño. El verificador debe capturar ambos sin ser sintonizado a mano para ninguno de ellos.
   China: 添加第二幻觉:Agencia B 虚构一个数据集 大小──验证者应捕获两者而无需针对任何一个手动调优──
3. Cambiar la piscina completa a una pizarra con particiones de temas (`prices`¿ Qué ?`summaries`¿ Qué ?`analyses`¿Qué escenarios de intoxicación dificulta la partición de temas, y cuáles no ayudan?
   La cuenca está en el centro de la ciudad.`prices`¿Qué es esto?`summaries`¿Qué es esto?`analyses`¿Cuáles de las situaciones de injerción de drogas son más difíciles de implementar y cuáles no?
4. Lea Hayes-Roth (1985, "A Blackboard Architecture for Control"). Identifique dos patrones de control del documento que no se discuten en esta lección de los que se beneficiarían los sistemas de 2026.
   En el libro de estudios de la Universidad de Chicago, Hayes-Roth escribió: "La arquitectura de la pizarra para el control" en el libro de estudios de la Universidad de Chicago, en el que se habla de la arquitectura de la pizarra para el control.
5. Lea CA-MCP (arXiv:2601.11595). Mapa de su Compañía de Contexto Compartido a la clase de MessagePool o Blackboard en `code/main.py`¿Qué primitivas añade CA-MCP a la parte superior?
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de`code/main.py`¿Qué lenguaje original ha sido añadido en el Centro de mensajes o en la tabla negra?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Más Leer más Leer más

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomía MAST; el envenenamiento por memoria es una subfamilia de fallos de coordinación
  Por qué muchos agentes LLM 系统会失败?  MAST 分类法;内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) Almacenamiento compartido de contexto para servidores MCP coordinados
  中文翻译:CA-MCP  上下文感知多服务器 MCP  协调 MCP 服务器的共享上下文存储
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) tablero basado en la cola de mensajes sin un orquestrador central
  Matrix  去中心化多 Agent 框架  基于消息队列的黑板,无中央编排器
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) el patrón de proyección por agente en la producción
   中文翻译:LangGraph  estado y regeneración  Producción de cada agente 投影模式
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notas de procedencia y verificación de una instalación de producción
  Traducción:Antropico  Cómo construir múltiples agentes  Sistema de investigación  de origen de la producción de la implementación 
