# SGLang y RadixAttención para cargas de trabajo pesadas prefijos
# Prefijo-Cache Servir  RadixAttención y KV Reutilización

> Trata el caché KV como un recurso reutilizable de primera clase almacenado en un árbol de radix, y cambia la programación con él: en lugar de FCFS (primero en llegar, primero en servir) como horarios vLLM, un cronista consciente de caché prioriza las solicitudes con prefijos compartidos más largos  efectivamente un cruce de radix de primera profundidad para que las ramas calientes permanezcan residentes en HBM. SGLang es el motor que construyó en torno a esta idea. En Llama 3.1 8B con las instrucciones de 1K similares a ShareGPT, SGLang alcanza ~ 16.200 tok/s a ~ 12.500 de vLLM, un ~ 29% de ventaja. En las cargas de trabajo RAG con prefijos pesados la ventaja alcanza 6,4x. En las cargas de trabajo en forma de clonación de voz, la tasa de hits de caché se eliminó en un 86%. Se desplegará en más de 400.000 GPUs en 2026 en xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. La cuestión es que el número 6.4x se evapora cuando el ordenado prefijo es inconsistente.

> **【中文解读】**Este episodio presenta la SGLang y RadixAttention por medio de la participación en la optimización de la eficiencia de la investigación 
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 、Fase 14(Agentic RAG) ・SGLang Usando árbol de radix 复用 KV cache比vLLM FCFS 更智能的调度。
> ¿ Qué es esto ?**【类比】**SGLang RadixAttention = "memória图书馆"──vLLM = Cada vez volver a buscar el catálogo;SGLang = 热门前(sistema提示+RAG contexto)存 radix tree 复用──Llama 3.1 8B 在 ShareGPT 上比 vLLM 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在40万+ GPU(xAI、LinkedIn、Cursor)──关键:前必须稳定排序才有效──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Diagrama RadixAttención: cómo se almacenan los prefijos en un árbol radix y cómo los bloques KV se comparten entre secuencias enraizadas en la misma rama.
  En el libro de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista
- Explica la programación consciente de la caché y por qué FCFS es incorrecto para el tráfico pesado de prefijos.
  Traducción: Explicar la capacidad de almacenamiento y el sentido de la regulación y por qué el FCFS es erróneo en el uso de los datos de la información.
- Calcule la velocidad esperada para una carga de trabajo dada la velocidad de impacto del prefijo-cache y la distribución de longitud rápida.
  Traducción: 给定前缓存命中率和快速长度分布,计算工作负载的预期加速──
- Nombre la disciplina de orden de inmediato que hace que el número 6.4x real vs una ventaja perdida.
  China 文翻译:说出 hace que 6.4x 加速成为现实而非流失的快速 排序纪律──

## El problema es la introducción del problema

> **【中文解读】**传统推理服务将每一个请求的提示 视为不透明即使5000个RAG 请求共享相同2000代币 系统提示,vLLM也将执行5000次完整的预填. RadixAttention 通过将代币序列存储在radix tree中解决这个问题:新请求沿树匹配已有前,只需预填 新增的后部分──挑战在调度FCFS先来先服务) 破坏前局部性,需要缓存意识调度器优先服务共享前的请求──

> **【拓展：前缀共享在 Agent 场景的价值】**El programa de trabajo de los agentes tiene características de uso compartido: sistemas de sugerencias, esquemas de instrumentos, pocos disparos de ejemplo, conversación histórica a través de la solicitud de recomposición.

El servicio clásico trata el prompt de cada solicitud como opaco. Incluso cuando 5,000 solicitudes RAG comienzan con el mismo prompt de sistema de 2,000 tokens más el mismo preámbulo de recuperación, vLLM preempla ese prefijo de 2,000 tokens 5.000 veces.

> 经典服务将每一个请求的快速 视为不透明的──即使5000 RAG请求都以相同的2000代币 系统提示加相同检查前开始,vLLM也会预填充那2,000代币前5000次──GPU 重复做同样工作──

La observación: las instrucciones en las cargas de trabajo de agente y RAG comparten prefijos largos casi siempre. Prometido de sistema, esquemas de herramientas, ejemplos de pocas tomas, encabezados de recuperación, historial de conversaciones  todo se repite a través de las solicitudes. Si guardaste la caché KV para ese prefijo una vez y lo utilizaste de nuevo, no lo volverías a preemplar.

>  observar:Agent y RAG   trabajo carga de prompto  casi siempre   compartido                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

RadixAttention hace exactamente esto. Los tokens se indexan en un árbol radix; cada nodo posee bloques KV para la secuencia de tokens en su camino desde la raíz. Una nueva solicitud camina por el árbol: cualquier nodo cuyo token coincide reutiliza los bloques KV de ese nodo. El costo de preempleo se vuelve proporcional al sufijo "nuevo", no al pedido completo.

> RadixAttention está haciendo esto. Token en el árbol radix en la indicación; cada nodo posee un conjunto de KV de la secuencia de tokens de la raíz a la ruta. Nuevo pedido en el árbol: cualquier token 匹配的节点复用该节点的 KV 块.

El reto es la programación. Si dos solicitudes comparten un prefijo de 2,000 tokens y un tercero comparte solo 200 tokens del mismo prefijo, desea servir las dos solicitudes compartidas por mucho tiempo juntas para que el prefijo largo permanezca en HBM. FCFS hace lo contrario  sirve a quien llegó primero, potencialmente desalojar la rama caliente antes de que la siguiente solicitud de prefijo largo llegue.

> 挑战在调度中. Si dos solicitudes comparten 2.000 tokens, el tercero sólo comparte 200 tokens, tú quieres servir simultáneamente dos solicitudes compartidas para mantener el largo plazo en el HBM.

## El concepto central.

### El árbol de radix como índice de KV

> **【中文解读】**Radix tree (en inglés: Radix tree) es la estructura de datos central de SGLang. Cada nodo tiene un token de alcance y de respuesta a los bloques KV. Nuevos pedidos de entrada en el tiempo junto al árbol de correspondencia: Sistema de sugerencias de correspondencia de puntos de correspondencia de 124 bloques KV, documentación de la división de correspondencia de 31 bloques, sólo se necesitan 4-6 bloques para el nuevo problema. Por ejemplo, el árbol de radix sólo necesita 4 bloques de nueva cálculo.

Un árbol radix (trie compacto) almacena secuencias de tokens. Cada nodo posee un rango de tokens y los bloques KV calculados para ese rango.

> Árbol de radix (紧前树) secuencia de tokens de almacenamiento. Cada uno de los puntos tiene un token.

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

Una nueva solicitud viene con el sistema de respuesta + "Contexto: <doc A>" + "Preguntas: Carol". El programador camina: coincidencias de prefijos del sistema (124 bloques reutilizados), coincidencias de rama doc-A (31 bloques reutilizados), luego asigna bloques nuevos sólo para "Preguntas: Carol" (4 bloques). Costo de preempleo: 4 bloques de tokens nuevos. Sin el árbol: 160 bloques. ~40x ahorro en preempleo.

> Una nueva solicitud con un sistema de sugerencias + "Contexto: <doc A>" + "Preguntas: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块),然后只为 "Preguntas: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### Programación de almacenamiento en caché

> **【中文解读】**缓存感知调度的两个关键策略: 1) 调度深度优先调度优先服务与当前运行集共享分支的请求,保持热点分支常驻HBM; 2) 分支级 LRU 淘汰以整棵分支为单位淘汰(从最少使用叶开始),而不是单块.

La reutilización respaldada por Radix Tree no tiene sentido si el caché se descompone.

> Si el almacenamiento continua, el uso de la árbol de raíz 支持的复用毫无意义.

1. **Depth-first dispatch**Cuando se selecciona la siguiente solicitud de la cola, prefiere las solicitudes enraizadas en la misma rama que el conjunto de ejecución actual. Esto mantiene la rama caliente fijada.
   En inglés:**深度优先调度** Seleccionar la siguiente solicitud de la fila, priorizar la selección con la solicitud del grupo de operaciones y la sección de la misma.
2. **LRU at branch level, not block level**. Eliminar ramas enteras (a partir de las hojas más cortas utilizadas) en lugar de bloques individuales, para que la forma del caché coincida con la forma del radix.
   En inglés:**分支级 LRU** Eliminar toda la parte de la hoja que menos se utiliza), en lugar de un solo bloque, para que la forma de la caja coincida con la forma de la raíz ⋅

Una solicitud compartiendo 2,000 tokens se sitúa detrás de una solicitud compartiendo 50, luego la rama de 2,000 tokens es desalojada para admitir la de 50 tokens.

> FCFS 违反两者── una solicitud de compartir 2.000 tokens排在共享 50 tokens 请求后面,然后 2,000 tokens 分支被淘汰以接受 50 tokens 请求后面──

### Números de referencia que debe memorizar

- Llama 3.1 8B, H100, ShareGPT 1K: SGLang ~ 16,200 tok/s vs vLLM ~ 12,500 (~ 29% de ventaja).
  En el caso de los productos de la industria de la construcción, el precio de la producción de la industria de la construcción de la industria de la construcción de la construcción de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica de la fábrica
- RAG con prefijos pesados (el mismo sistema + el mismo documento, preguntas diferentes): hasta 6,4x en SGLang.
  La situación de la población de la región de la isla de la isla de Guanajuato es muy diferente.
- Cargas de trabajo de clonación de voz: 86,4% de prefijos y tasas de caché.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Las tasas de impacto de la producción en los clientes de SGLang: 50-99% dependiendo de la disciplina inmediata.
  La producción de los clientes de SGLang 客户的命中率:50-99%, depende de la orden de producción rápida.
- Se desplegará en más de 400.000 GPU en 2026.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

### El pedido te ha llegado .

> **【中文解读】**6.4x acelerar dependiendo de la orden de los modelos de sugerencias.`[system, tools, context, history, question]`, a veces construyendo .`[system, context, tools, history, question]`,radix tree  cannot find shared  para humanos parecen ser los mismos, para radix tree are two different sequences── ingeniero de la clave 杆 is:将提示模板视为缓存键──将不可变内容──系统提示、工具方案) poner primero, en la búsqueda de las siguientes páginas, el usuario pregunta último── una vez el modelo de clasificación se ha ajustado en el tiempo que el porcentaje de vida de los archivos de caché se elevará del 7% al 74%──

> **【拓展：SGLang 在生产中的采用】**SGLang en 2026 ya se ha desplegado en más de 400.000 bloques de GPU, los usuarios incluyen xAI(Grok)、LinkedIn、Cursor、Oracle, así como el servicio de administración de GCP/Azure/AWS。 El escenario de ventajas centrales es Agent 和 RAG 工作负载 Estos escenarios en el sistema de sugerencias y herramientas definidas tienen una tasa de repetición muy alta。 El equipo de SGLang está formado por miembros de UC Berkeley LMSYS(Los creadores de Chatbot Arena, con el equipo de vLLM  tienen una estrecha colaboración─ ambos no son una competencia estrictavLLM también en 2026 añadir prefijo caching 功能─

El número 6.4x se basa en un ordenamiento de plantillas de instrucciones consistentes. Si su cliente construye instrucciones como `[system, tools, context, history, question]`en algunas solicitudes y `[system, context, tools, history, question]`En otros, el árbol no puede encontrar el prefijo compartido. lo que parece un prefijo compartido para un humano son dos secuencias distintas para el árbol radix.

> 6.4x Número depende de la orden de los datos de la solicitud de un cliente en un determinado momento.`[system, tools, context, history, question]`, entre otras peticiones`[system, context, tools, history, question]`, árbol no puede encontrar el uso compartido. Para los humanos, parece que es el uso compartido. Para el árbol radix, son dos secuencias diferentes.

El levier de ingeniero: su plantilla de solicitud es una clave de caché. Fija el orden. Coloque todo lo inmutable (sistema, herramientas, esquemas) primero. Coloque el contexto de recuperación después. Coloque la pregunta del usuario último. No deje contenido dinámico en el prefijo.

> 工程师的杆: tu prompt 模板是缓存键──固定顺序──将所有不可变内容(系统、工具、schema) poner lo más adelante──检索上下文放中间──用户问题放最后──不要在可缓存前中交错动态内容──

Caso real de la investigación: mover contenido dinámico fuera del prefijo cachéble llevó una implementación de 7% a 74% tasa de caché en un cambio.

> En el caso real de los estudios, el porcentaje de contenidos en movimiento se eleva del 7% al 74% en una sola implementación.

### Donde RadixAttention gana y pierde

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**SGLang y vLLM de previo almacenamiento de rendimiento en comparación: en Llama 3.1 8B H100, general ShareGPT 工作负载 SGLang 达到 ~16,200 tok/s vs vLLM ~12,500 tok/s (29% 优势); en gravedad 前重复使用 RAG 工作负载 优势可达6.4x;语音克隆工作负载缓存命中率 86% .

Las ganancias:
- RAG (el mismo preámbulo de recuperación, preguntas diferentes).
  En el caso de los niños, el problema es que no hay nada que hacer.
- Agentes (similes esquemas de herramientas, diferentes consultas).
  En inglés, "Agent" se llama "Agent" (Agent) y "Agent" (Agent) se llama "Agent" (Agent).
- Habla con el sistema de alarma.
  En español, el lenguaje de la lengua china es "solo" y "solo" se traduce en "solo" y "solo" en "solo".
- Cargas de trabajo de voz/visión con preámbulos repetidos.
  Traducción:重复前的语音/视觉工作负载──

Perder (retorna a la capacidad de rendimiento a nivel de vLLM):
- Generación de una sola toma con instrucciones únicas (completamiento de código, chat abierto sin instrucción del sistema).
  En inglés, el código de código completo (code complement complet, no sistema de código de código) es un código de código completo.
- Las instrucciones dinámicas donde cada solicitud intercaja contenido único en el prefijo.
  Traducción: Cada solicitud en el caché de archivos en el que se encuentra el contenido de la solicitud.

### Por qué este es un problema de cronograma, no sólo un problema del núcleo

Se puede implementar el reutilización de KV como un truco del núcleo. La visión de SGLang es que el reutilización sólo paga si el programador mantiene el residente de la rama caliente. Una política ingenua de "reutilización si está disponible" hará que la caché se cargue bajo carga mixta. El programador indexado por árbol radix es lo que convierte el truco del núcleo en una ventaja de producción del 29%.

> Se puede implementar KV 复用为内核技巧──SGLang's insight is replicable only in the regulator to keep the hot split branch constantly is only valuable──Primera estrategia de "hay reglas de replicación" en la mezcla de carga 动缓存──radix tree 索引 调度器 内核技巧 转化为 29% de la producción ventaja──

### Interacción con vLLM

En 2026 se añadió el prefijo de caché (`--enable-prefix-caching`La brecha se cerró pero no desapareció por completo  La pila entera de SGLang es radix-first; vLLM la injertó. Para cargas de trabajo dominadas por el uso reutilizado de prefijos, SGLang sigue siendo el predeterminado. Para la entrega de propósito general sin patrones de prefijos fuertes, vLLM sigue siendo igual o mejor.

> 两个系统不是 un competidor estricto.`--enable-prefix-caching`La diferencia se reduce pero no desaparece por completo. El conjunto de SGLang es un diseño radix-first.

## Usalo con el marco de ejecución
```figure
roofline
```

## Usalo

`code/main.py`Implementa una caché KV de juguete radix-tree más un cronista con dos políticas: FCFS y caché-consciente. ejecuta la misma carga de trabajo a través de ambos, informa la tasa de impacto de prefijo-cache y el delta de rendimiento. Luego ejecuta una carga de trabajo "ordenando desordenado" para mostrar el colapso de 6.4x.

> `code/main.py`实现 una simulación de árbol de radix KV 缓存加两个策略调度器:FCFS 和缓存感知──用两者运行相同工作负载,报告前缓存命中率和吞吐量差异──然后运行"乱序排序"工作负载展示 6.4x 崩──

## Envíe el producto .

> **【拓展：前缀缓存策略选择】**2026 años anterior 缓存 tiene tres niveles: 1) 应用级语义缓存(Fase 17·14) 在调用LLM前用嵌入相似度匹配历史响应,命中率 10-70%;(2) 服务端前缓存(SGLang RadixAttention / vLLM prefijo caching) 重复使用KV Cache,10x 延迟降低;(3) 跨节点缓存路由(Phase 17·11) 通过缓存意识路由将请求路由由由到持有前的副本──三者可叠加:语义缓存 →避免LLM 调用 端端前缓存避免重复预填 → 跨节点路由避免请求配

Esta lección produce`outputs/skill-radix-scheduler-advisor.md`. Dado una descripción de la carga de trabajo (forma de plantilla de solicitud, patrón de recuperación, número de inquilinos simultáneos), produce una receta de pedido de solicitud y una opción de no-entrada para la adopción de SGLang.

> 本课产 出  `outputs/skill-radix-scheduler-advisor.md`△给定工作负载描述(prompt 模板形状、检索模式、并发租户数), que genera 排序处方和 SGLang 采用 go/no-go 建议。

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Comparar FCFS y cache-consciente en la misma carga de trabajo. ¿De dónde viene el delta  ahorros de preempleo, ahorros de descifrado o retraso en la cola?
   Traducción:运行`code/main.py` Comparar los FCFS y el almacenamiento de datos en la misma carga de trabajo. ¿De qué se diferencia el preempleo de datos, el desmantelamiento de datos o el retraso de la fila?
2. Modificar la carga de trabajo para que las instrucciones al azar permute `[system, tools, context]`¿Qué pasa con el ritmo de impacto?
   Traducción: Modificar el trabajo de carga hacer rápido 随机排列 `[system, tools, context]`¿Qué cambio ha ocurrido en la tasa de destino?
3. Calcule el costo de HBM de mantener un sistema de 2,000 tokens de residencia rápida como una rama radix en Llama 3.1 8B. Compara con el costo de un lote de 16 secuencias sin reutilización de prefijos.
   China Translation: calcular en Llama 3.1 8B 上保持 2,000 tokens 系统提示作为一个基因 分支常驻的HBM 成本──与无前复用16序列批次成本比较──
4. Lea el artículo de SGLang RadixAttention. Explique en tres frases por qué el desalojo de LRU en forma de árbol supera a LRU en forma de bloque bajo carga pesada de prefijo.
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
5. Un cliente informa sólo un 8% de tasa de caché. Nombre tres causas probables y el diagnóstico que se ejecutaría para cada uno.
   China 译文:客户报告只有8% 缓存命中率──说出三个可能原因和每个诊断方法──

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Más Leer más Leer más

- [SGLang GitHub](https://github.com/sgl-project/sglang) fuente y documentos.
- [SGLang documentation](https://sgl-project.github.io/) Radix Atención y detalles de programación.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) la referencia del diseño.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) Números de referencia y razón del programador.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) La propia implementación de vLLM en forma de radix, para comparación.
