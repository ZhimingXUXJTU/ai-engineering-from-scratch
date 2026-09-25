# Memoria híbrida: Vector + Grafico + KV (Mem0) 混合记忆:向量+图+KV(Mem0)
# Memoria híbrida: Vector + Gráfico + KV

> La memoria híbrida ejecuta tres almacenes en paralelo  vector para la similitud semántica, KV para la búsqueda rápida de hechos, gráfico para el razonamiento de relación entre entidades  con una capa de puntuación que las fusiona en la recuperación. Este es un patrón de producción ampliamente utilizado para la memoria externa; Mem0 (Chhikara et al., 2025) es una implementación de referencia.

> **【中文解读】**Mem0 se considerará memoria como tres conjuntos de almacenamiento  volúmenes utilizados para la semejamilidad de palabras  KV utilizados para la búsqueda rápida de hechos  图 utilizados para la hipótesis de relaciones físicas                                                                                                                                                                                                                                    

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Explica por qué una sola almacenaje (solo vector, solo gráfico, solo KV) es insuficiente para la memoria del agente.
  Traducción:explicación por qué el único almacenamiento (sólo el tamaño, sólo el gráfico, sólo el KV) no es suficiente para mantener el agente 记忆──
- Nombre de Mem0 tres tiendas paralelas y para lo que cada uno optimiza.
  China:                                                                                                                                                                                                                                                              
- Describa la puntuación de fusión de Mem0  relevancia, importancia, actualidad  y por qué es una suma ponderada, no una jerarquía.
  En el texto original, el texto describe la combinación de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de la definición de referencia.
- Implementar una memoria de juguete de tres pisos en stdlib con un `add()`que escribe a los tres y a`search()`que fusiona los resultados.
  Con el estándar de la biblioteca de la memoria de juego.`add()`写入所有三个存储,`search()`融合結果──

## El problema es la introducción del problema

Una tienda está mal para una de las tres clases de consultas:

> 单存储对三类查询之一是错误的:

- **Semantic similarity**¿Qué hablamos sobre la deriva de agentes la semana pasada? Vector gana, KV y grafo faltan.
  En inglés:**语义相似性**¿Qué hemos discutido la semana pasada sobre el agente?
- **Fact lookup** "cuál es el número de teléfono del usuario?" KV gana; vector es un desperdicio, gráfico es un exceso.
  En inglés:**事实查找**¿Qué es el número de teléfono del usuario?
- **Relationship reasoning**¿Qué clientes comparten la misma entidad de facturación?
  En inglés:**关系推理**¿Qué clientes comparten el mismo coste? 图胜出;向量和 KV 无法回答──

Los agentes de producción emiten los tres en una sola sesión. Una memoria de una sola tienda siempre es incorrecta para dos de ellos.`add`- ¿ Qué ?`search`superficie con una función de puntuación que las fusiona.

> ¿ Qué es esto ?**【类比】**Tres tipos de índices de memoria de la biblioteca: tres tipos de índices de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria

> En una reunión, el agente de producción emite tres preguntas. Un solo recuerdo de memoria de dos de ellas es siempre erróneo.`add`- ¿ Qué ?`search`接口后面,并使用评分函数融合它们──

> **【中文解读】**混合记忆系统 (Mem0) combina memoria de trabajo a corto plazo y memoria de duración prolongada. En la ventana anterior, el almacenamiento de memoria a corto plazo se utiliza una base de datos y gráficos de datos de velocidad. La innovación central del Mem0 es la memoria automática.

> **【拓展：Mem0 是目前最流行的 Agent 记忆解决方案之一】**Mem0 (2024-2025) es uno de los soluciones de memoria más populares en la actualidad,GitHub 25k+ estrellas. Su estructura de tres niveles: memoria corta (en el caso de los eventos en el que se desarrolla la memoria)

> ¿ Qué es esto ?**【前置】**必須先掌握:Fase 14·07(MemGPT) y Fase 14·08(Letta Blocks) Mem0 es su "escape posterior de la versión de actualización"── también necesita entender tres tipos de bases de datos:

## El concepto central.

### Tres tiendas en paralelo

Mem0 (arXiv:2504.19413, abril 2025) en `add(text, user_id, metadata)`¿Qué es esto ?

> Mem0(arXiv:2504.19413,2025 年 4 月) 在 `add(text, user_id, metadata)`上:

1. Extraer datos de los candidatos del texto (un paso impulsado por el LLM).
   La política de la Unión Europea en el ámbito de la política de la Unión Europea (UE) se ha convertido en un marco de la política de la Unión Europea (UE).
2. Escriba cada hecho en el almacén vectorial (embedding) para la búsqueda semántica.
   La traducción de la lengua chino es "trader" y "trader" en inglés.
3. Escriba cada hecho en la tienda KV con teclado (user_id, fact_type, entity) para la búsqueda O(1).
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de KV.
4. Escriba cada hecho en el almacén de gráficos (Mem0g) como bordes tipografados para consultas de relación.
   La información de cada hecho se encuentra en el archivo de datos.

En el`search(query, user_id)`¿Qué es esto ?

> En el`search(query, user_id)`上:

1. La tienda vectorial devuelve el top-k incorporando cosino.
   En español, el volumen de almacenamiento en forma de similaridad de la estructura de los cuerpos de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.
2. KV almacenaje devuelve los hits directos claves en la consulta derivada (user_id, tipo, entidad).
   KV 存储返回基于查询推导的 (usuary_id, type, entity) 键的直接命中──
3. Almacenamiento de gráficos devuelve subgrafo accesible desde las entidades de consulta.
   En español traducción:图存储返回从查询实体可达的子图.
4. Una capa de puntuación fusiona los tres.
   El lenguaje de la lengua chino es el lenguaje de la lengua chino.

### Punto de puntuación de fusión

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

- **Relevance** cosino vectorial, KV coincidencia exacta, peso de la trayectoria del gráfico.
  En inglés:**相关性**                                                                                                                                                                                                                                                              
- **Importance** etiquetado en el momento de escribir o aprendido (algunos hechos son más importantes: nombres, identidades, políticas).
  En inglés:**重要性** escribir en el tiempo de marcación o aprender obtener  ciertos hechos más importante:姓名、ID、策略)
- **Recency** decadencia exponencial con el tiempo desde la última escritura o lectura.
  En inglés:**时效性**Indece de tiempo desde la última entrada o lectura.

Los pesos se ajustan por producto.`w_recency`para los agentes de chat; más alto `w_importance`para los agentes de cumplimiento; más alto `w_relevance`para agentes de recuperación.

> ️ **【易错点】**Tres tipos de cambios de peso en el movimiento de la memoria**后果**En el caso de los usuarios de la red social, el número de usuarios de la red social se reduce a un porcentaje de los usuarios de la red social.`w_recency`太高,老的高重要性事实被时间衰减淹没了──**一行修复**En el caso de los productos de la industria de la industria, el precio de la producción es muy bajo.

> 权重按产品调优──聊天 Agente  使用更高的 `w_recency`; conformación agente 使用更高的 `w_importance`; Inspección de agentes  使用更高的`w_relevance`¿Qué es eso?

### Memorandum y razonamiento temporal

Mem0g añade un detector de conflictos. Cuando un hecho nuevo contradice un borde existente, el borde existente se marca inválido pero no se elimina.

> Mem0g añadió un controlador de conflictos. Cuando los hechos nuevos se contradencian con los márgenes existentes, los márgenes existentes se etiquetan como ineficaces pero no se eliminan.

Este es el comportamiento de grado de cumplimiento que generaliza el patrón de invalidación de Letta.

> Este es el comportamiento de la Letta 失效模式泛化合规级.

### Números de referencia

El documento Mem0 presenta los siguientes informes (2025):

> Mem0 论文报告(2025):

- **LoCoMo**(memoria de conversación de larga duración): 91.6
- **LongMemEval**(memoria episódica de largo horizonte): 93,4
- **BEAM 1M**(Metería de referencia de memoria de tokens): 64,1

Las líneas de referencia de comparación (LLM de contexto completo 128k, tienda de vectores planos, KV plano) pierden más de 10 puntos.

> Comparar con la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

### Taxonomía de alcance

Mem0 divide la memoria por alcance:

> Mem0 按范围拆分记忆:

- **User memory** persiste durante las sesiones, con teclado en `user_id`¿ Qué ?
  En inglés:**用户记忆**跨会话持久化, en el`user_id`Por qué no?
- **Session memory** persiste dentro de un hilo.
  En inglés:**会话记忆** en una línea en perdurable.
- **Agent memory** Estado de instancia por agente.
  En inglés:**Agent 记忆** Cada agente 实例状态──

Cada escrito elige un alcance. La recuperación puede hacer consultas a través de ámbitos con pesos por alcance. Mezclar ámbitos sin pensar es como obtener "el asistente le dijo a Alice sobre el proyecto de Bob" incidentes.

> ¿ Qué es esto ?**【困惑】**P: ¿Mem0 Tres tipos de almacenamiento deben ser desplegados, el costo para un pequeño equipo es demasiado alto, ¿puede utilizar sólo la base de datos?**纯聊天机器人**Utilizando la cantidad de KV + KV ya suficiente con menos de 90% de complejidad);**多用户企业 Agent**(涉及权限、关系、合规) debe utilizarse la biblioteca, de lo contrario aparecerá el accidente de "Alice 见 Bob 的数据"──Mem0 的三存储是"为合规而生"的设计, no todos los escenarios son necesarios──

> Cada vez que escribe elige un rango. La búsqueda puede atravesar el rango.

### Cuando este patrón va mal

- **Embedding drift.**Los resultados vectoriales que se ven bien en las primeras cien consultas se degradan a medida que el corpus crece.
  En inglés:**嵌入漂移。**Pre100 veces de consulta parece que el resultado de la velocidad es correcto con el aumento y la degradación del material de la lengua.
- **KV schema creep.** `(user_id, type, entity)`Parece simple hasta que cada equipo añade su propio .`type`Auditará el tipo establecido trimestralmente.
  En inglés:**KV 模式蔓延。** `(user_id, type, entity)`Parece simple, hasta que cada equipo añade su propio.`type`◊ Tipo de auditoría trimestral
- **Graph explosion.**Un extractor ruidoso añade 50 bordes por mensaje.`add`Llamamos; dejamos de lado los bordes de baja confianza.
  En inglés:**图爆炸。**Un extractor de información por cada mensaje añadir 50 líneas de límite por cada vez`add`调用图写入数;丢弃低置信度边缘──

## Construye con movimiento.
```figure
ae-memory-fusion
```

## Construye el mismo

`code/main.py`Implementa el patrón de tres pisos en stdlib:

> `code/main.py`Utilizando el estándar de la biblioteca se ha logrado tres modos de almacenamiento:

- `VectorStore` similitud ingenuo de token-overlap como un sustituto de incorporación.
  En inglés:`VectorStore`Usar símbolo simple 重叠相似性替代嵌入──
- `KVStore` dictado con teclas `(user_id, fact_type, entity)`¿ Qué ?
  En inglés:`KVStore`以 `(user_id, fact_type, entity)`Por qué no?
- `GraphStore` bordes tipografados (sujeto, relación, objeto, válido).
  En inglés:`GraphStore`类型化边(主语、关系、宾语、有效)
- `Mem0` fachada de nivel superior con `add()`¿ Qué ?`search()`, la puntuación de fusión, y la recuperación consciente del alcance.
  En inglés:`Mem0`Top层门面,带 `add()`¿Qué es esto?`search()`、fusion evaluation y alcance de la percepción de la información 、
- Un rastro de trabajo en una conversación multi-usuario, multi-sesión.
  En español, el nombre de la persona que ha sido elegida para el programa es el de la persona que ha sido elegida.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

La salida muestra tres vías de recuperación separadas más el top-k fusionado.`main()`y ver el cambio de clasificación.

> 输出显示三条独立的召回路径加上融合的顶-k---在 `main()`顶部翻转评分权重观察排名变化──

## Usalo con el marco de ejecución

- **Mem0 (Apache 2.0)** listo para producción. Auto-host con Postgres + Qdrant + Neo4j, o use la nube gestionada.
  En inglés:**Mem0 (Apache 2.0)** producción就绪──用 Postgres + Qdrant + Neo4j 自托管,或使用托管云──
- **Letta** núcleo/recall/archivo de tres niveles; trae sus propios retroespectos vectoriales y gráficos.
  En inglés:**Letta** Tres niveles de núcleo/recall/archivo;
- **Zep** alternativa comercial con KG temporal y extracción de hechos.
  En inglés:**Zep**带时序知识图谱和事实提取的商业替代方案──
- **Custom builds** cuando se necesita un control exacto sobre el extractor (conformidad) o sobre los pesos de fusión (agentes de voz donde la recencia domina).
  En inglés:**自定义构建** Cuando necesite un control preciso de la carga de un instrumento de control (en inglés) 

## Envíe el producto .

`outputs/skill-hybrid-memory.md`genera un andamio de memoria de tres pisos con un marcador de fusión, taxonomía de alcance y invalidación temporal conectado.

> `outputs/skill-hybrid-memory.md`El sistema de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria de memoria

## Los ejercicios.

1. Replace la similitud de vector de juguete con un modelo de incorporación real (transformadores de oración, Ollama, incorporaciones OpenAI).
   ¿Se puede cambiar el tamaño de los juguetes en un modelo real? ¿Se puede cambiar el tamaño de los juguetes en un modelo real?
2. Añadir una consulta temporal: `search(query, as_of=timestamp)`¿Qué tienda necesita más trabajo?
   En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.`search(query, as_of=timestamp)` Sólo regresar a este tiempo o antecedentes válidos  ¿Cuál almacenaje necesita más trabajo?
3. Implementar un detector de conflictos: si un hecho entrante contradice un borde de gráfico, inválique el borde antiguo y registre ambos.
   Se trata de un sistema de análisis de conflictos que permite a los usuarios de una página web acceder a la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página de la página web de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la
4. Portar el marcador de fusión para incluir un `user_feedback`dimensiones (pues arriba en los registros recuperados). ¿Cómo evitar juegos (el agente sólo devuelve registros que ya le gustaron)?
   La traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua inglesa`user_feedback`¿Cómo evitar el manipulado? ¿Agent sólo regresa a su registro?
5. Lea los documentos de Mem0 (`docs.mem0.ai`¿ Por qué no lo haces ?`mem0`Comparar la calidad de recuperación en las mismas 20 consultas de prueba.
   En español: Mem0 文档.`mem0`客户端调用──比较相同 20 测试查询的检索质量──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Hybrid memory | "Vector plus graph plus KV" / "向量加图加 KV" | Three stores written in parallel, fused on retrieval / 三个存储并行写入，检索时融合 |
| Fact extraction | "Memory ingestion" / "记忆摄取" | LLM step that breaks text into (entity, relation, fact) tuples / 将文本拆分为（实体、关系、事实）元组的 LLM 步骤 |
| Fusion scoring | "Relevance ranking" / "相关性排序" | Weighted sum of relevance, importance, recency / 相关性、重要性、时效性的加权和 |
| Scope | "Memory namespace" / "记忆命名空间" | user / session / agent — determines who sees what / 用户/会话/Agent——决定谁看到什么 |
| Mem0g | "Memory graph" / "记忆图" | Typed edges with temporal validity for relationship queries / 带时序有效性的类型化边，用于关系查询 |
| Temporal invalidation | "Soft delete" / "软删除" | Mark contradicted edges invalid; never delete / 标记矛盾边为无效；永不删除 |
| Embedding drift | "Retrieval rot" / "检索腐化" | Vector quality degrades as corpus grows; re-embed periodically / 向量质量随语料增长退化；定期重新嵌入 |

## Más Leer más Leer más

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) el papel original
  En el texto original, el texto original se traduce en inglés como "Mem0 原始论文").
- [Mem0 docs](https://docs.mem0.ai/platform/overview) API de producción, SDK, nube gestionada
  En inglés, el idioma de la lengua inglesa es el idioma de la lengua inglesa.
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) el predecesor de contexto virtual
  En el texto original, el texto se traduce en "MemGPT".
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) el diseño de los hermanos de tres niveles
  La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
