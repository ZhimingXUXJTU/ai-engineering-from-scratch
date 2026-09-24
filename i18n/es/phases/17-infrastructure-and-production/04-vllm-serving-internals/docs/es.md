# VLLM Servicio interno: PagedAttention, Batching continuo, Prefill fragmentado  vLLM 推理服务内部机械:分页注意力、连续批处理、分块预填充
# Servicio de los motores internos  PagedAttención, Batch continuo, preempleo en pedazos

> El rendimiento moderno del motor de servicio se basa en tres fallos de composición, no en un solo truco. PagedAttention siempre está en. El batch continuo inyecta nuevas solicitudes en el batch activo entre las iteraciones de decodificación. Las rebanadas de preempleo en pedazos hacen que los tokens nunca mueran de hambre. Enciende los tres y un Llama 3.3 70B FP8 en un H100 SXM5 empuja 2.200-2.400 tok/s a 128 simultáneos  aproximadamente 25% por encima del propio estándar de vLLM y 3-4 veces un ciclo PyTorch ingenuo. Esta lección lee el programa y el núcleo de atención de vLLM  el motor de referencia para las tres técnicas  en un nivel que puede diagramar, y termina con un juego continuo batcher en `code/main.py`que los horarios preemplen y decodan de la manera que vLLM hace.

> **【中文解读】**vLLM en 2026 dominación se basa en tres complejos optimización:PagedAttention(分页注意力)始终开启;连续批处理在解码代间注入新请求;分块预填片长提示以防止解码代币 饥饿──三者全开时,Llama 3.3 70B FP8 在单卡H100上以 128并发达2,200-2,400 tok/s比朴素PyTorch 循环快 3-4倍──

> **【拓展：vLLM → LLM 推理服务标准】**vLLM es el motor de servicio de LLM de referencia más popular de 2026  PagedAttention  borrado del sistema operativo de KV Cache, se controlará la tasa de fragmentos en el 4% a continuación  Continuous batch processing permite un aumento significativo de la tasa de utilización de GPU 

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 11·12(推理优化基础) 、KV cache 概念、连续批处理──vLLM es el 2026 开源推理引擎的事实标准──
> ¿ Qué es esto ?**【类比】**vLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache(像操作系统虚拟内存分页,碎片率 < 4%);Continuous Batching = 动态拼单(新请求随时插入运行批);Chunked Prefill = 切长快速(长输入切片避免阻塞解码)。Llama 3.3 70B FP8 en H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 ⋅倍

## Objetivos de aprendizaje

- Explica PagedAttention como un alocador de caché KV: bloques, tablas de bloques y por qué la fragmentación se mantiene por debajo del 4% en la carga de producción.
  La información de la información disponible en el sitio web de la compañía se puede encontrar en el sitio web de la compañía.
- Diagrama de la partición continua a nivel de iteración: cómo las secuencias terminadas salen del lote y las nuevas se unen sin drenar.
  En la siguiente categoría, el proceso de elaboración de la serie se realiza en el siguiente modo:
- Describa el preempleo en pedazos en una frase y nombre qué métrica de latencia protege (indicación: es cola TTFT, no es el promedio de rendimiento).
  China:                                                                                                                                                                                                                                                              
- Nombre el 2026 vLLM v0.18.0 gotcha que muere equipos habilitando cada optimización a la vez.
  China: Traducción: decir que en 2026 vLLM v0.18.0 en simultáneo activar todos los equipos optimizados se encontrarán problemas.

## El problema es la introducción del problema

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批处理将所有请求填充到最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV Cache 碎片率从60-80% 降至4% 以下) 连续批处理(在解码代间动态加入新请求) 分块预填充(将长提示切片以防止解码饥饿) △

Un ciclo de servicio PyTorch ingenuo ejecuta una solicitud a la vez: tokenizar, preemplir, decodificar hasta EOS, devolver. En un usuario esto funciona. A cien, es una cola de pacientes. La solución obvia  lotamiento estático  empapa cada solicitud al prompt más largo de la ventana, empapa cada decodificación a la salida esperada más larga, y detiene todo el lote en la secuencia más lenta. Pagas por relleno que nunca usas, y las solicitudes rápidas esperan las lentas.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填充、解码直到EOS、返回──一个用户时时这行通──一百用户时,这就是一排耐心等待的人──显然修静态批处理将每一个请求填充到窗口中最长的提示,将每一个解码填充到最长期的输出,将每一个解码填充到最长期的输出,整个批次等待最慢的序列──你为未使用的填充单,快速请求等待缓慢请求──

VLLM resuelve tres problemas a la vez. PagedAttention detiene la fragmentación de la caché de KV de consumir 60-80% de la memoria de la GPU de la manera que lo hace la asignación contiguosa clásica. El batch continuo permite que las solicitudes se unan y salgan del lote entre cada iteración de decodificación, por lo que el lote siempre está lleno de trabajo real. El preempleo en pedazos rompe una señal de 32k en 512 tokens que se interponen con el decodificación, por lo que una señal larga no congela cada token de decodificación en la GPU.

> vLLM una vez resuelve tres problemas. PagedAttention bloquea KV 缓存碎片像经典连续分配那样吞 60-80% de GPU 内存. Continuous批处理让请求在每个解码代之间加入和离开批次,所以批次总是充满真实工作. 分块预填将32K token的提示切成512 token的提示片段,与解码交换进行,所以长提示不会结结 GPU 上的每个解码 token.

El modelo de producción 2026 está activado por defecto. Necesitas entender lo que cada uno hace porque los modos de falla están todos en el programador, no en el modelo.

> El sistema de producción por defecto de 2026 es de tres tipos. Necesitas saber qué hacer cada uno, porque el modo de defecto está en el regulador, no en el modelo.

## El concepto central.

### PagedAttention como un sistema de memoria virtual

> **【中文解读】**PagedAttention 借借鉴操作系统虚拟内存分页思想管理 KV Cache。 tradicional distribución continua para cada secuencia previa distribución máxima longitud(como 8192 tokens), pero la solicitud media sólo utiliza 1500 tokens, el gasto 82% de HBM。 PagedAttention dividirá el KV Cache en bloques fijos de gran tamaño(默认 16 tokens), cada secuencia tiene un bloque de cartografía lógica ubicación a bloques físicos ID, según la distribución de la necesidad, la tasa de fragmentos es inferior al 4%。 es el único distribuidor de vLLM, a través de`--gpu-memory-utilization`(默认 0.9) control KV Cache HBM disponible en uso

> **【拓展：KV Cache 内存管理演进】**KV Cache 内存管理 ha experimentado tres generaciones de desarrollo: 1) 连续预分配简单但浪费60-80%内存; 2) PagedAttention(vLLM 2023) 分页管理,碎片率 <4%,成为行业标准; 3) RadixAttention(SGLang 2024)  En el escenario de uso compartido anterior, se ha optimizado aún más, mediante la búsqueda de la árbol de radix para lograr la implementación de las solicitudes de KV 复用.

Un caché KV es`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`Para Llama 3.3 70B a 8192 tokens, es aproximadamente 1.25 GB por secuencia en BF16. Si reservas 8192 ranuras por adelantado para cada solicitud pero la solicitud promedio solo utiliza 1500 tokens, desperdicias aproximadamente el 82% del HBM reservado.

> Cada secuencia de KV 缓存大小为 `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element` Llama 3.3 70B en 8192 tokens 时,BF16 下每序列约 1.25 GB── Si por cada solicitud pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-pre-prepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepreprepre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre pre

PagedAttention toma la idea de la memoria virtual del sistema operativo. El caché KV no es contiguo por secuencia. Se asigna en bloques de tamaño fijo (tokens predeterminados 16). Cada secuencia tiene una tabla de bloques que mapea sus posiciones lógicas de tokens a los ID de bloques físicos. Cuando una secuencia se expande más allá de sus bloques asignados, se agrega un bloque más. Cuando termina, sus bloques regresan al grupo.

> PagedAttention 借借借操作系统虚拟内存的思想──KV 缓存不是 de cada secuencia continuada── se distribuye con un bloque de tamaño fijo(default 16 tokens) distribuido── cada secuencia tiene una tabla de bloques, se mapeará la posición del token lógico 位置 de un bloque físico──cuando la secuencia crece más allá del bloque distribuido, se añade un nuevo bloque── completado, el bloque vuelve a la pila──

La fragmentación cae del 60-80% (clásico) a menos del 4% (Attención pagada).`--gpu-memory-utilization`(default 0.9), que indica a vLLM cuánto HBM debe reservar para los bloques KV después de cargar pesos y activaciones.

> 碎片率 de 60-80% (经典) Bajo 4% (以下) PagedAttention) You don't need with a tag to enable PagedAttentionIt's vLLM 唯一分配器──旋是`--gpu-memory-utilization`(默认 0.9), le diga a VLLM en carga de peso y activación después de que KV bloque pre-reserva cuántos HBM.

### Participación continua en el nivel de iteración

> **【中文解读】**连续批处理在每个解码步骤之间做出接收/释放决策──每个代:(1) 移除已完成的序列;;(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

El antiguo "batch dinámico" esperaba una ventana (digamos 10 ms) para llenar un lote, luego ejecuta prefill + decode + decode + decode hasta que cada secuencia terminara.

> 旧的"动态批处理" espera una ventana (como 10 ms) para llenar los lotes, luego ejecuta prefill + decode + decode + decode hasta que cada secuencia se complete.

El batch continuo se opera entre cada paso de decodificación.`RUNNING`En cada iteración:

> 连续批处理在每个解码步骤之间操作―― se llamará conjunto de secuencias en funcionamiento `RUNNING`列表──每次代:

1. Cualquier secuencia en `RUNNING`que acaba de golpear EOS o max_tokens se elimina.
   En inglés:`RUNNING`Se eliminan cualquier secuencia de EOS o max_tokens alcanzados.
2. El programador mira la cola de espera. Si hay bloques KV libres, admite nuevas secuencias (preencher o reanudar).
   China:调度器查看等队列──如果有空 KV 块,它接纳新序列(预填充或恢复)──
3. El pase hacia adelante se ejecuta en lo que sea que ahora está en .`RUNNING`, emitiendo un nuevo token por secuencia.
   En español: previo`RUNNING`En todo el contenido se ejecuta, cada proceso emite un nuevo token.

El tamaño del lote nunca se empolga a un número fijo. Secuencias en diferentes posiciones en su salida comparten una fusionada hacia adelante.`V1 scheduler`. La invariante clave: el programador se ejecuta una vez por iteración de decodificación, no una vez por solicitud.

> 批次大小从不填充到固定数字――输出不同位置的序列共享一次融合前向传播――2026年 vLLM 中称为 `V1 scheduler`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △  △ △     △    △ △      △     △                                                                                                                         

### El preempleo en pedazos protege la cola de TTFT

> **【中文解读】**Se ha resuelto el problema de "结" de otros segmentos de descifrado. Un token de 32K en el modelo 70B requiere aproximadamente 800 ms de preempleo puro 计算, mientras que todos los otros segmentos de descifrado de los tokens están esperando.

> **【拓展：vLLM 生产部署最佳实践】**La configuración clave de la producción de la MLM para 2026 incluye:`--gpu-memory-utilization 0.9`预留 90% HBM 给 KV Cache;(2) `--max-model-len`根据实际需求设置而非默认最大值;(3) 分块预填充默认开启但不兼容某些推测解码模式;(4) `--enable-prefix-caching`En el caso de RAG/Agencia, se puede reducir significativamente la repetición de preempleo;

Prefill es computacional. Una solicitud de 32k-token en Llama 3.3 70B toma ~800 ms de prefill puro en un H100. Mientras que la solicitud de prefill se ejecuta, decodifica las fichas para cada otra secuencia en el lote de espera. En un bucle de servicio, la latencia de primer token (TTFT) de un pedido largo se convierte en la latencia de intertoken (ITL) para docenas de otros usuarios.

> 预充是计算密集型的──Llama 3.3 70B 上一个32K代币提示在单卡H100 上需要约800ms的纯预充──预充运行时,预充中所有其他序列的解码代币都在等待──在服务循环中, un长提示的首个代币延迟(TTFT) se convirtió en varios decenas de otros usuarios de代币间延迟(ITL)毛刺──

El preenrollo en piezas se divide en piezas de tamaño fijo (tokens predeterminados 512) y se programa cada pieza como una unidad. Entre los trozos el programador puede avanzar las secuencias de decodificación por un token.

> Los bloques preenchidos se preenchiran en bloques fijos de tamaño determinado (defusión 512 tokens), cada uno de ellos como unidad de regulación. Entre los bloques, el regulador puede avanzar en la secuencia de la resolución de un token.

### Las tres configuraciones interactúan

Las tres características se asumen mutuamente. PagedAttention le da al programador un recurso de KV de granos finos para negociar con.`RUNNING`En el caso de los Estados miembros, el sistema de programación de programas de programación es un sistema de programación más, no un sistema separado.

> Tres características interdependientes. La atención pagada para el regulador proporciona un pequeño volumen de KV  recursos para el regulador.`RUNNING`La decisión hecha en la lista es otra estrategia de regulación, no un sistema independiente.

No es necesario conocer cada bandera, es necesario saber lo que el programador optimiza: un buen rendimiento bajo el presupuesto del bloque KV, sujeto a la recorte de preempleo en pedazos.

> Usted no necesita saber cada señal. Usted necesita saber lo que el módulo optimiza.

### El 2026 v0.18.0 te tiene

> **【中文解读】**vLLM v0.18.0 中 no puede activarse simultáneamente `--enable-chunked-prefill`Y el modelo de proyecto 推测解码`--speculative-model`)。 La única excepción es la N-gram GPU 推测解码 en el V1 调度器。 no lee la nota de publicación sobre el inicio de todos los signos de optimización. El equipo se encontrará con errores de ejecución en el inicio, y no con una degradación de la software。 Si el resultado de la solución de la prueba se inicia en bloques de preempleo, la respuesta correcta para el año 2026 es generalmente EAGLE-3 y no el modelo de proyecto―

En vLLM v0.18.0 no se puede combinar `--enable-chunked-prefill`con descifrado especulativo de modelo de proyecto (`--speculative-model`¿Qué es lo que se hace? La excepción documentada es la descifrado especulativo de GPU de N-gram en el programador V1. Los equipos que cambian cada bandera sin leer las notas de lanzamiento obtienen un error de tiempo de ejecución en el inicio, no una regresión suave. Si su ganancia especulativa valía la pena permitir preempleo en pedazos, vuelva a la opción  la respuesta correcta en 2026 es a menudo EAGLE-3 sin preempleo en pedazos, no un modelo de borrador más preempleo en pedazos que no compila.

> En vLLM v0.18.0, no puedes activar simultáneamente `--enable-chunked-prefill`Y el modelo de proyecto 推测解码`--speculative-model`)。 La excepción del registro de archivos es la N-gram GPU en el V1 调度器 推测解码。 no se lee la declaración de publicación sobre la apertura de todos los signos del equipo en el inicio de la operación en lugar de error en el momento de ejecutar la descomposición de software。 Si el beneficio de la evaluación de código se inicia en bloques preemplazos, la respuesta correcta para el año 2026 es generalmente EAGLE-3 y no el modelo de proyecto―

### Números que debes recordar

- Llama 3.3 70B FP8, H100 SXM5, 128 simultáneos, todos los tres en: 2.200-2.400 tok/s.
  En el caso de los modelos de la tecnología de la información, el sistema de información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información.
- El mismo modelo, VLLM predeterminado (sin precarga en pedazos): ~1.800 tok/s.
  En el caso de los sistemas de control de datos, el sistema de control de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- El mismo modelo, el ciclo PyTorch hacia adelante ingenuo: ~600 tok/s.
  Sin embargo, el proceso de producción de la torsión de PyTorch se ha extendido hasta el final del ciclo.
- Residuos de fragmentación de KV bajo PagedAttention a carga de producción: < 4%.
  En el caso de los productos de la industria de la producción, el precio de la producción de los productos de la industria de la producción es el de la producción de los productos de la industria de la producción.
- P99 ITL bajo carga mixta: ~ 15 ms con precarga en pedazos, ~ 50 ms sin.
  China: 拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:拼音:

### Cómo se ve el programador

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`Es exactamente este bucle en stdlib Python con recuentos falsos de tokens y latencia avanzada falsa. ejecutándolo muestra cómo el preempleo en pedazos mantiene las secuencias de decodificación vivas durante un largo preempleo.

> `code/main.py`Es la base de datos de Python en este ciclo, que se implementa con el uso de tokens falsos y falsos pre-empleo de tiempo.

## Usalo con el marco de ejecución
```figure
tensor-parallel
```

## Usalo

`code/main.py`simula un programador de estilo vLLM con características alternativas. ejecuta para ver:

> `code/main.py`模拟一个带有可换功能的vLLM风格调度器──运行:

- `NAIVE`modo: una solicitud a la vez, sin lotes.
  En inglés:`NAIVE`模式: una vez una solicitud, sin lote de tratamiento.
- `STATIC`modo: pad y espera, batch clásico.
  En inglés:`STATIC`模式: llenar y esperar, clásica por la entrega.
- `CONTINUOUS`modo: admisión y liberación a nivel de iteración.
  En inglés:`CONTINUOUS`模式: 代级的接收和释放──
- `CONTINUOUS + CHUNKED`modo: preemplar las recetas entrelazadas con decodificación.
  En inglés:`CONTINUOUS + CHUNKED`模式: preempllando 片与解码交错──

La salida muestra el rendimiento total (tokens por segundo virtual), el TTFT medio y P99 ITL.`CONTINUOUS + CHUNKED`La fila debe ser la principal en el tráfico mixto.

> 输出显示总吞吐量(每虚拟秒代币 数) 、TTFT 均值和 P99 ITL。`CONTINUOUS + CHUNKED`Se trata de un proyecto de investigación que se desarrolla en el sector de la energía.

## Envíe el producto .

> **【拓展：LLM 推理引擎对比】**El proyecto de investigación de la Universidad de Chicago (U.S.) se desarrolló en el año 2026 en el campo de la investigación de la tecnología de la información y la tecnología de la información (en inglés, "LLC") y se desarrolló en el campo de la tecnología de la información y la tecnología de la información (en inglés, "LLC") y en el campo de la tecnología de la información (en inglés, "LLC") y en el campo de la tecnología de la información (en inglés, "LLC") y en el campo de la tecnología de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en el campo de la información (en inglés, "LLC") y en inglés).

Esta lección produce`outputs/skill-vllm-scheduler-reader.md`. Dado un formato de servicio (tamaño de lote, utilización de memoria KV, tamaño de preenrollo en pedazos, configuración especulativa), produce un diagnóstico de cronometrista que nombra cuál de las tres anomalías es el cuello de botella y qué sintonizar.

> 本课产 出  `outputs/skill-vllm-scheduler-reader.md` la configuración de servicios de la serie de grandes cantidades de KV, la utilización de almacenes de KV, la configuración de los módulos de la serie de módulos de la serie de módulos de la serie de módulos de la serie de módulos de la serie de módulos de módulos de la serie de módulos de módulos de la serie de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de módulos de mód

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Comparar .`STATIC`¿ Qué ?`CONTINUOUS`¿De dónde viene la brecha de rendimiento de la eficiencia de preempleo, la eficiencia de decodificación o la latencia de cola?
   Traducción:运行`code/main.py`◊ en la carga de trabajo de la solicitud de larga duración`STATIC`Y `CONTINUOUS`¿De qué se deriva la diferencia de throughput  pre-fill efficiency  decodificación efficiency o final delay?
2. Modificar el programador de juguetes para agregar `--max-num-batched-tokens`. ¿Cuál es el valor correcto para un H100 con Llama 3.3 70B FP8? (Intención: es una función del tamaño de bloque KV y el número de bloques libres, no HBM crudo).
   Traducción:Mudificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación: Modificación`--max-num-batched-tokens` H100 运行 Llama 3.3 70B FP8 的正确值是多少?
3. Re-leer las notas de vLLM v0.18.0. ¿Qué combinaciones de banderas son mutuamente excluyentes?
   En el caso de los ejemplos de la versión de vLLM, el nombre de los ejemplos de vLLM es el de VLLM.
4. Calcule el desperdicio de fragmentación de la caché KV para un rastro de 1.000 solicitudes con promedio de 1.500 tokens de salida, std 600 tokens, bajo (a) asignación contiguosa por solicitud a 8192 max, (b) PagedAttention con bloques de 16 tokens.
   En el caso de los datos de la página de pago, el valor medio es de 1.500 tokens de salida, estándar de 600), en (a) máximo 8192 de continuidad por solicitud distribuida y (b) 16 tokens de bloques PagedAttention 下。
5. Explique en un párrafo por qué el precarga en piezas ayuda a la P99 ITL pero no a la capacidad de producción en forma aislada.
   China: Usado para explicar por qué el bloque de preempleo ayuda a P99 ITL pero no solo a aumentar la capacidad de producción.

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Más Leer más Leer más

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) fuente oficial sobre compatibilidad entre preemplazos en pedazos y decodificación especulativa.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026 libera cadencia y comportamiento específico de la versión.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) la redacción original que todavía define cómo pensar sobre el asignador.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) análisis de fragmentación y diseño de los programadores.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) detallado V1 programador paseo con gráficos de llama.
