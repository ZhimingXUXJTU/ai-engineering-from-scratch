# VLLM Production Stack con LMCache KV Descargación .
# Producción de servicio de pila  descarga de KV y enrutamiento de caché

> Una producción que sirve a los cables de pila de enrutador, motores y observabilidad en una implementación Kubernetes  y trata el caché KV como un recurso que puede dejar la GPU. La descarga de KV extrae el caché de KV de la memoria de la GPU y lo reutiliza en consultas y motores (DRAM de CPU, luego disco / Ceph). La pila de producción de vLLM es la implementación de referencia; LMCache es la capa de descarga. El conector de descarga de KV 0.11.0 vLLM (enero 2026) hace que este sea asincrónico y se pueda conectar a través de la API del conector (v0.9.0+). El camino de descarga generalmente está oculto del camino de la solicitud, aunque las fallas de caché y las promociones pueden agregar latencia de extremo a extremo. LMCache es valioso incluso sin prefijos compartidos  cuando una GPU se queda sin ranuras de KV, las solicitudes preemptadas se pueden restaurar desde la CPU en lugar de recomputar prefill. Se publicaron puntos de referencia en 16x H100 (80 GB HBM) en 4 a3-highgpu-4g: cuando la caché KV supera la HBM, tanto la descarga de CPU nativa como la LMCache mejoran sustancialmente el rendimiento; en una huella de KV baja, todas las configuraciones coinciden con la línea de base con un pequeño gasto aéreo.

> **【中文解读】**Este capítulo presenta la VLLM  Recomendación de servicios  PagadoAttención  Continuo de lote y segmento de preempleo  Tri-core optimización 
**Type:** Learn
**Languages:** Python (stdlib, toy KV-spill simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang/RadixAttention)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy KV-spill simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention)

> ¿ Qué es esto ?**【前置】**Estudiar en el campo de la tecnología de la información y la información.
> ¿ Qué es esto ?**【类比】**LMCache = "GPU 内存搬家"──KV cache 装不下 HBM → 溢出到CPU DRAM 再到磁盘──GPU 满时 preempted 请求可从CPU 恢复(无需重算预填)──异步、对用户透明──即使无共享前也值──16x H100 referencia:KV 超HBM 时大幅升吞;低KV 占用时开销很小──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Diagrama de las capas de producción de vLLM: enrutador, motores, descarga de KV, observabilidad.
  La producción de la máquina de transporte de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de
- Explica la API de conector de descarga de KV (v0.9.0+) y cómo el camino asincrónico 0.11.0 oculta la latencia de descarga.
  La versión original de la versión original de KV fue publicada en la versión de la versión de KV.
- Cuantificar cuándo LMCache CPU-DRAM ayuda (KV > HBM) vs añade gastos generales (KV lo suficientemente pequeño como para caber en HBM).
  China: LMCache CPU-DRAM en cuándo hay ayuda
- Escoge entre la descarga de CPU de vLLM nativa y el conector LMCache dado las restricciones de implementación.
  Traducción:给定部署约束, entre el descarga y el LMCache de la CPU vLLM.

## El problema es la introducción del problema

> **【中文解读】**vLLM 推理服务在高并发时 GPU HBM 占满,发生抢占事件请求被逐出、重新排队、同一个2K-token提示一分钟内被重新填充四次──GPU 计算花在冗余预填上,Goodput 远低于原始吞吐──添加更多 GPU 是线性成本,但CPU DRAM 很便宜一个插座有512GB+,延迟虽然比HBM 差几个数级级,但对于"临时热"的KV Cache 足够──

> **【拓展：vLLM Production Stack 架构】**La producción de vLLM es el programa de implementación de Kubernetes de 2026 que se propone, que contiene cinco componentes: 1) Router cache-aware Phase 17·11), consumo KV 事件; 2) motores vLLM trabajadores, por GPU o por TP/PP 组一个; 3) KV Cache 卸载 LMCache 部署或原生连接器; 4) 可观测性Prometheus + Grafana + OTel traces; 5) 面控制服务发现、配置、滚动更新──以图表 + Helm operator 形式发布──

Su servicio vLLM muestra GPUs en 100% HBM con eventos de preempción cada vez que la concurrencia sube. Las solicitudes se desalojan, se requieren y se vuelve a preencher el mismo aviso de 2K-token cuatro veces en un minuto.

Añadir más GPUs cuesta linealmente. Añadir más HBM no es posible. Pero CPU DRAM es barato  un socket tiene 512 GB + en órdenes de latencia de magnitud peores que HBM pero bien para "temporalmente caliente" KV caché.

LMCache extrae la caché KV a la CPU DRAM para que las solicitudes preemptadas se recuperen rápidamente, y los prefijos repetidos en los motores comparten la caché sin que cada motor se vuelva a llenar.

## El concepto central.

### VLLM - pila de producción

`github.com/vllm-project/production-stack`es el despliegue de referencia Kubernetes:

- **Router** Cache-consciente (fase 17 · 11). Consume eventos de KV.
- **Engines** Trabajadores de VLLM. Uno por GPU o por grupo TP/PP.
- **KV cache offload** Despliegue de LMCache o conector nativo.
- **Observability** El raspado de Prometheus, los tableros de grafana, los rastros de OTel.
- **Control plane** Descubrimiento de servicios, configuración, actualizaciones de rodaje.

Se envió como operador de Helm Chart +.

### La API del conector de descarga de KV (v0.9.0+)

vLLM 0.9.0 introdujo una API de conector para los backends de caché KV enchufables. Su motor descarga los bloques al conector; el conector los almacena (RAM, disco, almacenamiento de objetos, LMCache).

vLLM 0.11.0 (enero 2026) añade una ruta de descarga asíncrona  descarga puede ocurrir en el fondo para que el motor no se bloquee en el caso común. La latencia de extremo a extremo y el rendimiento todavía dependen de la forma de la carga de trabajo, la tasa de impacto de la caché KV y la presión del sistema; las propias notas de vLLM indican que la descarga del núcleo personalizado puede degradar el rendimiento a bajas tasas de impacto y que la programación asíncrona ha conocido problemas de interacción con la descodificación especulativa.

### Descarga de CPU nativa vs LMCache

> **【中文解读】**两种KV Cache 卸载方案对比:(1) 原生 vLLM CPU 卸载引擎本地,存储KV块到主机 RAM,实现快速,零网络跳转,但不跨引擎共享;(2) LMCache 连接器集群级,存储块到共享LMCache 服务器(CPU DRAM + Ceph/S3 压层), cualquier motor está disponible.

**Native vLLM CPU offload**El motor local almacena bloques de KV en la memoria RAM del host. Rápido para implementar, salto de red cero. No cruza motores.

**LMCache connector**Los bloques son accesibles para cualquier motor. Se publican 16 puntos de referencia H100.

Seleccione nativo cuando un solo motor tiene presión HBM. Seleccione LMCache cuando varios motores comparten prefijos (RAG con instrucciones de sistema comunes, multi-tenant con plantillas compartidas).

### Comportamiento de referencia

> **【拓展：LMCache 基准测试数据】**LMCache en 16x H100(80GB HBM) a través de 4 个 a3-highgpu-4g 基准测试表现:(1) 低KV 足迹(短提示、低并发) 所有配置匹配基线,LMCache 增加 ~3-5% 开销;(2) 中等足迹LMCache 开始在前复用方面提供帮助;(3) KV 超过 HBM原生CPU 卸载和LMCache 都有改善吞吐,LMCache 由于跨引擎共享收益更大.

El H100 16x (HBM de 80 GB) distribuido en 4 ensayos a3-highgpu-4g:

- Baja huella de KV (promptos cortos, baja concurrencia): todas las configuraciones coinciden con la línea de base, LMCache añade ~ 3-5% de gastos generales.
- Moderada huella: LMCache comienza a ayudar en el reutilización de prefijos en los motores.
- KV supera HBM: la descarga de CPU nativa y LMCache mejoran sustancialmente el rendimiento; LMCache obtiene mayor ganancia debido al intercambio entre motores.

### Cuando el LMCache es decisivo

> **【中文解读】**LMCache en los siguientes escenarios es decisivo: 1) 多租户服务系统提示跨租户共享; 2) RAG文档块跨查询重复; 3) 微调变体(LoRA)  KV 复用减少冗余工作; 4) 抢占密集型工作负载从CPU 恢复比重新预填 更便宜;;不应启动场景:HBM 压力小(只有开销没有收益) 短上下文(<1K tokens,传输时间 > 重新预填) 单租户单单单无复用可捕获提示)

> **【拓展：KV Cache 卸载的集成】**Fase 17·17 Servicio separado + LMCache: transferencia de KV de preempleo a decodificación de la pila si no se utiliza de inmediato, se puede almacenar en LMCache; posterior consulta de LMCache 拉取而不是 volver a preemplar.

- Servicio multi-arrendatario donde las instrucciones del sistema se comparten entre los inquilinos.
- RAG donde los fragmentos de documentos se repiten en las consultas.
- Variantes de ajuste fino (LoRA) en la misma base donde la reutilización del modelo base KV reduce el trabajo redundante.
- Cargas de trabajo pesadas de preempción: restaurar desde la CPU más barato que volver a precargar.

### Cuando NO habilitar

- La presión de la HBM pequeña  se paga el gasto general sin beneficios.
- Contexto corto (tokens < 1K)  tiempo de transferencia > re-pre-reemplazar.
- Carga de trabajo de un solo inquilino de una sola vez  no se reutiliza para capturar.

### Integración con servicio desglosado

Fase 17 · 17 porción desagregada + compuestos LMCache: KV transfiere de prefill pool a decodificar pool land en LMCache si no se utiliza; consultas posteriores se retiran de LMCache. Fase 17 · 11 router consciente de caché puede enrutarse al motor cuyo local O LMCache-compartido caché coincide.

### Números que debes recordar

- vLLM 0.9.0: API de conector enviado.
- vLLM 0.11.0 (Jan 2026): ruta de descarga asíncrona; el impacto de latencia de extremo a extremo depende de la carga de trabajo, la velocidad de impacto de KV y la presión del sistema (no es una garantía absoluta).
- 16x H100: LMCache ayuda cuando la huella de KV excede la HBM.
- Presión de HBM pequeña: 3-5% de gastos generales sin beneficio.

## Usalo con el marco de ejecución
```figure
zero-sharding
```

## Usalo

`code/main.py`La información de la empresa de gestión de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

> `code/main.py`La información de la empresa de gestión de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

> `code/main.py`La información de la empresa de gestión de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

## Envíe el producto .

Esta lección produce`outputs/skill-vllm-stack-decider.md`. Dada la forma de la carga de trabajo y la implementación de vLLM, decide nativo vs LMCache vs ninguno.

> 本课产 出  `outputs/skill-vllm-stack-decider.md`. Dada la forma de la carga de trabajo y la implementación de vLLM, decide nativo vs LMCache vs ninguno.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿A qué uso de HBM comienza a pagar LMCache?
   Traducción:运行`code/main.py`¿En qué HBM utilizan las tasas para empezar a planificar?
2. Un inquilino comparte un sistema de 6K-token en 200 consultas/hora.
   Un inquilino en 200 preguntas /小时中共享 6K token 系统提示――计算 LMCache 的预期节省――
3. El servidor LMCache es un solo punto de falla. Diseñar la estrategia HA (replicas, retroceso a nativo).
   El LMCache  servidor es un solo punto de fallo.
4. LMCache almacena a Ceph en disco giratorio. ¿Para un KV de 4K con 70B FP8 (500 MB), cuál es el tiempo de lectura frente a la reposición?
   Para el 70B FP8 en el token 4K KV(500MB), ¿cuánto tiempo tardará?
5. Argumentar si la ruta asíncrona vLLM 0.11.0 es "libre" ¿Dónde se esconde la cabeza?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Production-stack | "the reference deployment" | vLLM's Kubernetes Helm chart + operator |
| Connector API | "KV backend interface" | vLLM 0.9.0+ pluggable KV store interface |
| Native CPU offload | "engine-local spill" | Store KV in host RAM of same engine |
| LMCache | "cluster KV cache" | Cross-engine KV cache server on CPU DRAM + disk |
| 0.11.0 async | "non-blocking offload" | Offload hidden behind engine stream |
| Preemption | "evict to make room" | KV cache shuffle when HBM full |
| Prefix reuse | "same system prompt" | Multiple queries share beginning; cache hit |
| Ceph tier | "disk tier" | Durable storage below DRAM in the cache hierarchy |

## Más Leer más Leer más

- [vLLM Blog — KV Offloading Connector (Jan 2026)](https://blog.vllm.ai/2026/01/08/kv-offloading-connector.html)
- [vLLM Production Stack GitHub](https://github.com/vllm-project/production-stack) Diagrama del casco + operador.
- [LMCache for Enterprise-Scale LLM Inference (arXiv:2510.09665)](https://arxiv.org/html/2510.09665v2)
- [LMCache GitHub](https://github.com/LMCache/LMCache) Implementación de los conectores.
- [vLLM 0.11.0 release notes](https://github.com/vllm-project/vllm/releases) Detalles de la trayectoria asincrónica.
