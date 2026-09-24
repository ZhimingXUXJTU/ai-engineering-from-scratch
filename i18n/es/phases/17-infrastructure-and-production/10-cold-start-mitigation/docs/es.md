# Mitigación de inicio en frío para LLM sin servidor .

> Una imagen de modelo de 20 GB tarda 5-10 minutos (7B) a 20+ minutos (70B) en pasar de frío a servicio. En un mundo sin servidores, eso no es un calentamiento, es un apagón. Las mitigaciones operan en cinco capas: imágenes de nodos pre-seeded (Bottlerocket en AWS, arco de doble volumen), transmisión de modelos (NVIDIA Run:ai Model Streamer, nativo en vLLM), instantáneas de memoria de GPU (puntos de control módiles, hasta 10 veces más rápido reinicio), piscinas calientes (`min_workers=1`), carga en niveles (NVMe→DRAM→HBM de ServerlessLLM, reducción de latencia 10-200x), y migración en vivo que mueve tokens de entrada (KB) en lugar de KV caché (GB). Modal publica 2-4s de frío comienzos como piso; Baseten 5-10s por defecto, subsegundo con pre-calentamiento. Esta lección te enseña a medir, presupuestar y apilar las cinco capas.

> **【中文解读】**Este capítulo presenta las estrategias de la primera respuesta a la demora de la reducción de la MLL.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·02(平台经济学) ‧Fase 17·03(GPU 扩缩) ・LLLM sin servidor frío iniciación = 5-20 分钟(no es calor, es parar) ⋅
> ¿ Qué es esto ?**【类比】**• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Enumere las cinco capas de mitigación de arranque en frío y nombre una herramienta o patrón en cada capa.
  China: 列举冷启动缓解的五层策略,并说出每层一个工具或模式──
- Calcule el tiempo total de arranque en frío como suma de (provisión de nodos) + (peso descarga) + (peso carga en HBM) + (motor init) para un modelo 70B.
  計算 70B 模型总冷启动时间 = 节点供给 + 权重下载 + 权重加载到HBM + 引擎初始化──
- Explica por qué la migración en vivo transfiere tokens de entrada (KB) y no KV cache (GB) y cuál es la penalización (recomputado).
  China: explicación por qué real tiempo se mueve a través de los tokens de transferencia y transferencia de datos (KB) y no KV 缓存 (GB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es qué (KB) y el precio es el precio es el que se calcula de nuevo (KB) y el precio es el que se calcula de nuevo (KB) y el precio es el que se calcula de nuevo (KB) y el precio es el que se calcula de nuevo (KB)
- Nombre del trade-off de la piscina caliente (pagar por la GPU ociosa o aceptar cola de arranque en frío) y el umbral de SLA en el que `min_workers > 0`se hace obligatorio.
  China:                                                                                                                                                                                                                                                              `min_workers > 0`变为强制性的 SLA 值──

## El problema es la introducción del problema

> **【中文解读】**El problema de inicio frío de LLM sin servidor:70B 模型从零到服务需要 3-8 分钟(节点供应 45-60s + 容器拉取 120-300s +权重载 45-120s + 引擎初始化 10-30s), SLA de SLA de lejos sobre 2s △ solución es conservar la pila de calor(min_workers=1), pero esto significa 24/7 支付空 GPU 费用5 产品各保留 1 个热副本,每月3600 GPU-hours 无论是否有用户调──

> **【拓展：Serverless LLM 平台对比】**2026 años Serverless LLM 平台的冷启动表现:Modal 凭借 GPU 快照技术实现 2-4s冷启动(业界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不包含模型加载);GCP Cloud Run + GPU 较新,冷启动约15-30s──对于TTFT P99 < 60s 的70B+ 模型,热池是强制性的没有任何冷启动优化能在 60s内完成全流──

Tu punto final sin servidor de LLM se reduce a cero durante la noche a las 8 de la mañana, el tráfico aumenta.

> Suo sin servidor LLM 端点在夜间缩容到零.

1. Karpenter proporciona un nodo de GPU: 45-60s.
   Carpenter 供给 GPU 节点:45-60 秒──
2. El contenedor saca una imagen de 30 GB con pesos: 120-300s.
   En inglés, el contenido de un reflejo de 30 GB: 120-300 segundos.
3. El motor carga pesos en HBM: 45-120s dependiendo del tamaño del modelo y la velocidad de almacenamiento.
   El motor se cargará hasta HBM:45-120 segundos, dependiendo del tamaño del modelo y la velocidad de almacenamiento.
4. vLLM o TRT-LLM inicializa los gráficos CUDA, el caché KV, el tokenizer: 10-30s.
   中文翻译:vLLM 或 TRT-LLM 初始化 CUDA graph、KV 缓存池、分词器:10-30 秒──

Total: 220-510s (aproximadamente 3-8 minutos) antes de que un token regrese. Su SLA es 2s.`min_workers=1`Si tu servicio tiene 5 productos cada uno con una réplica caliente, eso es 5 × 24 × 30 = 3.600 horas de GPU / mes, ya sea que un solo usuario llamó o no.

> 总计:220-510 秒(约 3-8 分钟)才能返回一个代币――你的SLA是2秒――你部署热池(`min_workers=1`) el problema parece desaparecer pero ahora tienes 24/7 para un GPU 付费. Si tu servicio tiene 5 productos cada uno de una copia de calor, entonces 5 × 24 × 30 = 3.600 GPU-hora/monto, independientemente de si es útil o no.

La mitigación de arranque en frío es cómo mantener la economía sin servidores mientras se aproxima a la latencia de siempre en marcha.

> El enfriamiento de la actividad se produce con el retraso de la actividad de la actividad de mantenimiento económico sin servidor.

## El concepto central.

### Capas 1  imágenes de nodos pre-semeados (Bottlerocket)

> **【中文解读】**Primera capa  Pre-播种节点镜像──AWS Bottlerocket de dos volúmenes de arquitectura se separará del sistema operativo y los datos──将容器镜像(含模型权重)`EC2NodeClass`En el caso de los nuevos nodos, el ejecutivo de la nueva línea de datos de la NVMe ha eliminado los pasos de retiro de imágenes, ahorrando 2-4 minutos para los modelos grandes.

En AWS, la arquitectura de doble volumen de Bottlerocket separa el sistema operativo de los datos.`EC2NodeClass`. Los nuevos nodos se arrancan con pesos ya en NVMe local  paso 2 y parte de 3 desaparecen. Funciona con Karpenter de forma nativa.

> En AWS, la estructura de dos volúmenes de Bottlerocket separará el sistema operativo de los datos.`EC2NodeClass`En el caso de los modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de modelos de la serie de la serie de la serie de modelos de la serie de la serie de la serie de la serie de modelos de la serie de la serie de la serie de la serie de la serie de la serie de los modelos de la serie de la serie de la serie de la serie de la serie de la serie de los modelos de la serie de la serie de la serie de la serie de la serie de los cuentas de los cuentas de los cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cu

Equivalente en GCP: imágenes personalizadas de VM con capas de contenedores precoces. En Azure: instantáneas de disco administradas con el mismo patrón.

> GCP 等价方案:预容器层的自定义 VM 镜像──Azure:托管磁盘快照加相同模式──

### Capas 2  modelo de transmisión (Run:ai Model Streamer)

> **【中文解读】**Segundo nivel Modelo de carga en línea. NVIDIA Run:ai Model Streamer no necesita el resto del archivo.

En lugar de cargar el archivo completo antes de responder a la primera solicitud, transmite pesos en la memoria de GPU capa por capa y comience el procesamiento tan pronto como el primer bloque de transformador sea residente. El NVIDIA Run:ai Model Streamer se envía nativo en vLLM 2026. Funciona con S3, GCS y NVMe local. Cortará el tiempo de carga de peso aproximadamente a la mitad para los modelos grandes superponiéndose I / O con la configuración de computación.

> No necesita en respuesta a la primera solicitud precargar el archivo completo, sino que se cargará el peso a nivel de forma gradual en la memoria de la GPU, y el primer transformador 块carga completado inmediatamente después de comenzar a procesar.

### Capas 3  Snapshots de memoria de GPU (Modal)

> **【中文解读】**Treso nivel GPU 内存快照──Modal en primera carga después de la GPU 状态(权重、CUDA graph、KV Cache 区域) hacer un punto de inspección, posteriormente volver a iniciar directamente la recolección hasta HBM比重新启动快 10x──es la técnica más cercana de "2 segundos de inicio de calor de la GPU"──代价是快照与 GPU 拓绑定

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减半权重加载时间) + (3) GPU 快照(消除重重加载) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM) ――全叠加将 70B 模型从 328s冷启降到约15s22x 改善──选择哪几层取决于SLA 严格程度和预算──

Modal toma un punto de control del estado de la GPU (pesos, gráficos CUDA, región de caché KV) después de la primera carga. Los reinicios posteriores se deserializan directamente en HBM  10 veces más rápido que la reinicialización. Esta es la cosa más cercana a "iniciar una GPU caliente en 2 segundos".

> Modal en la primera carga después de la GPU  estado (权重、CUDA gráfico、KV 缓存区域) hacer un punto de inspección。后续重启直反序列化到HBM比重启动快10倍。 es la técnica más cercana de "2 segundos de inicio de GPU"──代价:快照与 GPU 拓绑定, si Karpenter 迁移到不同 SKU 需要重制作快照──

### Capas 4  piscinas calientes (min_trabajadores=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026 años de servidorless LLM plataforma de frío inicialización:Modal en GPU 快照技术实现 2-4s(业界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常10-30s(不含模型加载);original 70B 模型冷启动 3-8 分钟。Modal de rápido照技术是关键差它将 GPU 状态(权重 + CUDA graph + KV Cache 区域)序列化,重启直反序列化到HBM,重启动快 10x──代价是快照与 GPU 拓绑定,迁移到不同 SKU 需要重制快照──

La más simple de las medidas: mantener una réplica siempre lista. El costo es la tasa por hora de una GPU 24x7.$0.85-$El límite de SLA para las piscinas calientes es típicamente TTFT P99 < 60 en un modelo 70B+.

> La solución más simple es mantener una copia siempre disponible. El costo de una GPU es de 24 horas por día.$0.85-$1.50/小时 para evitar 30 segundos de inicio frío), el modelo grande es relativamente amigable(付 $4/小时 para evitar 5 minutos de inicio frío)。 la temperatura de la batería se convierte en un SLA obligatorio 值: normalmente es 70B+ 模型上 TTFT P99 < 60 秒──

### Capas 5  Carga en capas (LLM sin servidor)

ServerlessLLM trata el almacenamiento como una jerarquía: NVMe (rápido pero grande), DRAM (medio pero nivelado), HBM (pequeño pero instantáneo). Los pesos se precargan a DRAM; carga a pedido en HBM. El papel informa una reducción de latencia de 10-200 veces en cargas frías en comparación con navías de disco a HBM. La adopción de producción es temprana pero existen integraciones con vLLM.

> El servidorlessLLM almacenará en el nivel de almacenamiento:NVMe(快但大)、DRAM(中等但分层)、HBM(小但即时)。权重预加载到DRAM;按需加载到HBM。论文报告冷启动延迟降低 10-200倍──生产采用尚早,但已存在与vLLM的集成──

### Capas 6  Migración en vivo (patrón de bonificación)

Cuando un nodo se vuelve indisponible (evacución de puntos, desagüe de nodos), el patrón tradicional es iniciar en frío otra réplica y desagüe la cola de solicitud. La migración en vivo mueve los tokens de entrada (kilobytes) a un destino que tiene el modelo cargado y recalcula el caché KV en el destino. La recomputada es más barata que transferir GB de caché KV a través de la red. Aplicable a implementaciones desagregadas.

> Cuando el punto no es útil cuando se inicia el proceso de iniciación en frío, el modo tradicional es iniciar en frío otro lado de la línea de solicitud de la línea de espera.

### Las matemáticas de la piscina caliente

> **【中文解读】**热池数学: para P99 TTFT SLA 为 2s 的服务, el problema no es "热池 sí/no" sino "cuánto热副本、哪些路径需要"──高价值交互路径(实时聊天、语音 Agent)→ min_workers=1-2;后台批处理路径(夜间分类)→ escala a cero aceptable;高级层级 → 按租户专用热副本。简单算术:5 个产品每 1 热副本 = 5 × 24 × 30 = 3600 GPU-hours/月, independientemente de si es útil para el uso.

Para un servicio con P99 TTFT SLA de 2s, la pregunta no es "polar caliente sí/no" sino "cuántas réplicas calientes, y qué caminos las obtienen".

>  Para el P99 TTFT SLA de 2 segundos de servicio, el problema no es "la cuota de calor sí/no" sino "cuánta cuota de calor, qué caminos las necesitan"

- Rutas interactivas de alto valor (chat en vivo, agente de voz): `min_workers=1-2`¿ Qué ?
  En el caso de los medios de comunicación, el número de usuarios es de 1.`min_workers=1-2`¿Qué es eso?
- Rutas de lote de fondo (clasificación nocturna): escala a cero aceptada, 5-10 minutos de inicio en frío tolerada.
  Traducción: 后台批处理路径 (后台批处理路径) 晚间分类: acepta reducción hasta 0, 5-10 minutos de frío
- Nivel de primera categoría: `min_workers`por inquilino con capacidad específica.
  Traducción:Paseo de la casa`min_workers`专用容量──

### Medir antes de optimizar

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重到HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

Anatomía de arranque en frío para un modelo 70B en un nodo fresco (ilustrativo):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Números que debes recordar

- Inicio en frío modal: 2-4 segundos (con instantáneas de GPU).
  Modal frío: 2-4 segundos (utilizando GPU)
- Comienza en frío por defecto de baseta: 5 a 10 segundos; subsegundo con precalentamiento.
  En español: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés: "Base" en inglés" en inglés" en inglés) en inglés) en inglés) en inglés) en inglés) en inglés) en inglés) en inglés) en inglés translation translation translation translation translation translation translation translation translation translation into English as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as as
- Inicio en frío de 70B crudo: 3-8 minutos.
  Sinopsis: El tiempo de la película es de 30 minutos.
- Run:ai Modelo de Streamer: ~ 2x velocidad de carga por peso.
  Runo:ai Modelo de transmisión: aproximadamente 2 倍权重加载加速──
- Carga en niveles de ServerlessLLM: reducción de latencia 10-200 veces (números de papel).
  En el caso de los servidores sin servidor, el sistema de datos de servidores sin servidor tiene un contenido de 10 a 200 veces más.

## Usalo con el marco de ejecución
```figure
cold-start-pipeline
```

## Usalo

`code/main.py`El modelo de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自付自足的亏平衡请求率──

## Envíe el producto .

Esta lección produce`outputs/skill-cold-start-planner.md`. Dado el SLA, el tamaño del modelo y la forma del tráfico, elige qué mitigations apilar.

> 本课产 出  `outputs/skill-cold-start-planner.md` Dado SLA  modelo de tamaño y de forma de flujo, elegir sobre qué estrategias de alivio 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Calcular la tasa de compensación de las solicitudes por encima de la cual una réplica caliente es más barata que el pago del impuesto de inicio en frío mediante caídas adicionales de las solicitudes en SLO.
   Traducción:运行`code/main.py` calcular el saldo de las solicitudes de abandono de pagos por medio de la SLO
2. Se despliega un modelo 13B con P99 TTFT SLA de 3s. Elige la pila de mitigación mínima (las capas más bajas) que lo logre.
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de 13B, P99 TTFT fue implementada en el 13 de la versión de la versión de la versión de la versión de la versión de 13 de la versión de la versión de la versión de la versión de 13 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 13 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
3. El pre-seeding de botellas elimina la atracción de la imagen, pero los pesos aún se cargan desde la instantánea a HBM.
   China 预播种 Bottlerocket 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播 预播时 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 
4. Su proveedor sin servidor ofrece instantáneas de GPU (Modal) y su equipo se niega porque "las instantáneas filtran PII".
   China: tu proveedor de servidores no tiene GPU 快照(Modal), pero el equipo rechazó debido a la "快照泄露 PII"―辩论
5. Diseñar una política de piscina caliente en niveles: ¿cuántas réplicas calientes para usuarios pagados, usuarios de prueba y cargas de trabajo de lote? Muestre las matemáticas.
   En español, el nombre de la plataforma de distribución de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Más Leer más Leer más

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) Los puntos de referencia publicados de Modal y la arquitectura de los puntos de control.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) Modelo de instantánea de volumen de datos pre-seeded.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) Peso sobrepeso carga con configuración de cálculo.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/) Manual de juego de precalentamiento.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) Diseño de carga en niveles.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) migración en vivo para desplegamientos desglosados.
