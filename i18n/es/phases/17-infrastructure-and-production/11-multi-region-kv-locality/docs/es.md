# Múlti-región LLM Servir y KV Cache Localidad  多区域 局部性 服务 LLM KV

> El equilibrio de carga de round-robin es activamente perjudicial para la inferencia LLM almacenada en caché. Una solicitud que no aterriza en el nodo que tiene su prefijo paga el costo de preempleo completo  aproximadamente 800 ms en P50 en un prompt largo versus ~ 80 ms con un caché hit. En 2026 el patrón de producción es un router consciente de la caché (vLLM Router en Rust, llm-d router) que consume eventos de caché KV y rutas en coincidencia prefijo-hash. La investigación reciente (GORGO) hace que la latencia de la red transregional sea un término explícito en el objetivo de enrutamiento. Las ofertas comerciales de "inflación transregional" (inflación transregional Bedrock, puertas de entrada multi-cluster GKE) tratan la inferencia como opaca  manejan la disponibilidad, no TTFT. JPMorgan y Mayo Clinic realizaron un fallo de la primera en noviembre de 2024 en 22 minutos. La realidad de DR: el 32% de los fracasos de LLM DR se deben a que los equipos hicieron copias de seguridad de pesos pero olvidaron archivos de tokenizer o configuraciones de cuantización.

> **【中文解读】**Este capítulo presenta la estrategia de optimización de la caché de la KV en la multirregión de KV 局部性跨区域部署 LLM 时的 KV 优化策略──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM)、Fase 17·06(RadixAttention)。多区域部署必须使用缓存知性路由器,不能轮回──
> ¿ Qué es esto ?**【类比】**Más de un millón de personas han estado en el área de trabajo de la empresa. En el área de trabajo de la empresa, la empresa de gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión de la gestión
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Explicar por qué las interrupciones de equilibrio de carga en round-robin almacenaron en caché la inferencia y cuantificar la penalidad TTFT.
  Traducción:Explanation why rotation load balance破坏缓存推理,并量化 TTFT 惩罚──
- Diagrama un router consciente de la caché: entradas (eventos de caché KV), algoritmo (combinación de prefijo-hash), tie-breaker (utilización de GPU).
  En el caso de los datos de la CPU, el usuario puede utilizar el sistema de datos de la CPU.
- Nombre el controlador de falla del 32% de DR para LLMs (archivos de tokenización / configuraciones de cuantización faltantes) y indique una lista de verificación de DR de tres archivos.
  China:                                                                                                                                                                                                                                                              
- Distinguir las ofertas comerciales transregionales (Bedrock CRI, GKE Multi-Cluster Gateway) de las de enrutamiento consciente de KV.
  La nueva versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión

## El problema es la introducción del problema

> **【中文解读】**Los tres problemas centrales del servicio de LLM de la región son: 1) el equilibrio de carga de la reserva de datos por la RGPD ha destruido la localización de KV Cache, lo que ha llevado a que la tasa de vida de la reserva de datos se descienda del 70% al 8%; 2) el fracaso del LLM DR del 32% de DR DR DR se debe a que el equipo ha registrado un peso de seguridad pero ha olvidado la configuración de la información; 3) el mantenimiento de datos por el RGPD exige que los usuarios de la UE no puedan salir de la UE, el router consciente de la caché no puede adaptarse a las solicitudes de los usuarios de París a través de los Estados Unidos-este-1:

> **【拓展：多区域推理的产业实践】**Las mejores prácticas de la implementación de LLM en más de 2026 años incluyen: 1) en cada región 独立的缓存知性路由器(vLLM Router / llm-d router), evitar la alta demora en la transferencia de KV a través de la región 跨区域 KV 转移的高延迟(US-EU RTT 约75ms,US-APAC 约 220ms);(2) en el estudio de GORGO se ha realizado una investigación sobre la retraso de la red como un objetivo de ruta  显式项目 联合优化 prefill_time + network_latency;(3) inferencia transregional Bedrock 和 GKE Multi-Cluster Gateway 处理可用性, pero no procesar TTFT 您仍然需要应用层缓存知性路由器.

Su servicio se ejecuta en US-East-1, US-West-2, y EU-West-1. pone un ALB delante con round-robin. Prefijo caché tasa de impacto en la producción cae al 8%. TTFT P50 triplica. sus registros vLLM muestran que cada solicitud está pagando el costo de preempleo completo.

> Su servicio opera en EE.UU. Este-1, EE.UU. Oeste-2 y EE.UU. Oeste-1,.. Usted está en la vanguardia de ALB haciendo consultas,... la tasa de espera de la producción anterior cayó hasta el 8%,..

La redonda es óptima para los servicios sin estado. La inferencia LLM es estatalizada por diseño.

> 轮询负载均衡对无状态服务优优――LLM 推理自然是有状态的KV 缓存编码了模型看到的一切内容――盲路由就是路由到错误的缓存――

Separadamente, su equipo tiene un plan DR. Usted hace una copia de seguridad de los pesos del modelo para S3 cross-región. Un apagón regional golpea; usted intenta fallar; la réplica se niega a iniciar. Se olvidó tokenizer.json, la configuración de cuantificación, y la configuración de escala RoPE estaban en un balde separado que no sincronizó.

> Por otro lado, tu equipo tiene un plan de recuperación de catástrofe. Tú llevarás el modelo a un banco de reservas transregionales hasta S3.

El servicio de LLM multi-regional es un problema de caché, un problema de enrutamiento y un problema de higiene DR  no un problema de balance de carga.

> El programa de MLL de múltiples regiones es un problema de caché, un problema de ruta y un problema de recuperación de desastres.

## El concepto central.

### Enrutamiento consciente de la caché

> **【中文解读】**Mecanismo de trabajo de ruta: solicitud de llegada después, ruta para el futuro (como 512 tokens) hacer hash, consulta cada副本"¿¿tienes esta anterior 缓存?"──副本 a través de pub/sub 频道 publicar KV Cache 事件( distribución/淘汰块), ruta para el futuro 哈希→副本的索引──匹配到则路由到该副本,未匹配则按GPU利用率选择──vLLM Router(Rust 实现,2026 production-stack) 支持 O(1) 找,未匹配时回归至最小队列深度──

El router hacha el prefijo (digamos, los primeros 512 tokens); le pregunta a cada réplica "¿tienes este prefijo almacenado en caché?". Las réplicas publican eventos de caché KV en un canal pub/sub mientras asignan y despejan bloques.

> Por favor, lleve una sugerencia de llegada. El router se encuentra en el bloque de distribución y eliminación de bloques.

**vLLM Router**(Rust, 2026 producción-estaca): suscribirse a `kv.cache.block_added`eventos, mantiene un índice de réplica prefijo-hash →, rutas con búsqueda O(1). Calla a la menor profundidad de cola cuando no se combina.

> **vLLM Router**(Rust,2026 producción-estaca): 订阅 `kv.cache.block_added`事件,维护前哈希 → 副本索引,O(1) 查找路由──无匹配时回归最小队列深度──

**llm-d router**: mismo patrón, nativo de Kubernetes. Publica eventos a través de la API ControlPlane.

> **llm-d router**El mismo modo, Kubernetes originalmente.

**SGLang RadixAttention**(Fase 17 · 06) es el equivalente intra-replica.

> **SGLang RadixAttention**(Fase 17 · 06) es el equivalente en el subconjunto.

### Números

> **【拓展：KV Cache 路由的性能数据】**Diferencia de rendimiento de la ruta de un caché KV de varios puntos: 2K-token 提示在 Llama 3.3 70B FP8 H100 上,cache hit(同副本、前常驻) TTFT ~80ms;cache miss(cold prefill) TTFT ~800ms10x 差距──如果路由器在副本间实现 60-80% de la capacidad de pre-calendar, puede ser capaz de alcanzar un rendimiento de la versión de N 副本容量下近似单副本──区域间 RTT 也是关键因素:us-east-1  us-west-2 ~65ms、us-east-1  eu-west-1 ~75ms、us-east-1  southeast-1 ~220ms跨区域路由只在远程网上延迟才才时的价格──

TTFT P50 en una señal de 2K, Llama 3.3 70B FP8, H100:
- El caché se encuentra en el mismo lugar (replica, prefijo residente): ~80 ms.
- Falta de almacenamiento en caché (preenchimiento en frío): ~ 800 ms.

Si su router alcanza el 60-80% de la caché de prefijos en réplicas, se aproxima el rendimiento de una réplica única a capacidad de N-replica. Si alcanza el 10%, se aproxima la escalación ingenua.

> 2K-token 提示在 Llama 3.3 70B FP8 H100 上的 TTFT P50:缓存命中(同副本,前常驻) aproximadamente 80ms;缓存未命中(冷预填充) aproximadamente 800ms──10 倍差距── Si tu router en副本间 logra una tasa de 60 a 80% de la capacidad de缓存命中, puedes tener un rendimiento de N 副本容量下近似单副本──如果只有 10%,你近似朴素扩展──

### La región transversal tiene una nueva restricción  latencia de la red

RTT interregional:
- US-East-1  US-West-2: ~65 ms.
- Estados Unidos-este-1  Europa-oeste-1: ~75 ms.
- Estados Unidos-este-1  ap-sureste-1: ~ 220 ms.

Si el enrutamiento lleva una solicitud de us-east-1 a un prefijo caliente en ap-southeast-1, el preempleo guardado (800 → 80 ms) es empequeñecido por 440 ms de ida y vuelta.`prefill_time + network_latency`A menudo la respuesta es mantener el enrutamiento regional excepto en prefijos masivos de varios MB donde prefill domina.

> 区域间 RTT:us-east-1  us-west-2 约 65ms;us-east-1  eu-west-1 约 75ms;us-east-1  ap-southeast-1 约 220ms。如果路由将请求从us-east-1 发送到ap-southeast-1 的热前,节省的预填充(800 → 80ms) 被 440ms 的往返延迟淹没──GORGO(2026年研究)明确指出联合优化`prefill_time + network_latency`La respuesta es generalmente mantener la reubicación del camino, a menos que el pre-repudio se domine en un gran número de MB.

### La "inflación transregional" comercial no ayuda aquí

La inferencia transregional de AWS Bedrock envía automáticamente las solicitudes a otras regiones durante la presión de capacidad. Optimiza la disponibilidad, no TTFT, y trata la inferencia como opaca.

> AWS Bedrock 跨区域推理在容量压力下自动将请求路由到其他区域──它优化可用性而不是 TTFT,将推理视为不透明──GKE Multi-Cluster Gateway 也是如此服务级故障转移,不感知 KV 缓存──

Aún necesitas un router consciente de la caché de la capa de la aplicación incluso cuando usas estos manejan el caso "US-East-1 está en llamas" el routing consciente de la caché maneja el caso TTFT

> Incluso con estos productos, todavía necesitas aplicar camadas de almacenamiento de datos de los circuitos de información.

### Higiene DR  el problema de los archivos faltantes del 32%

> **【中文解读】**DR 卫生的三文件最低清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置(vllm_config.yaml等);(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ▽加上:

> **【拓展：LLM 灾难恢复最佳实践】**La práctica clave de LLM DR de 2026 es: 1) 模型制品完整性不只是权重文件, también contiene tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板; 2) 跨区域同步S3 transregional replicación Usó en el almacén de modelos, asegurar que todas las regiones tengan un副本完整; 3) Automatización DR 测试 usando Chaos Engineering; 4) RTO 目标企业级 LLM 服务通常要求 RTO < 30 分钟.

Estadísticas de 2026 citadas ampliamente: el 32% de los fracasos de LLM DR ocurren porque los equipos respaldaron los pesos pero olvidaron:

- `tokenizer.json`o `tokenizer.model`
- Configuración de cuantificación (`quantize_config.json`, escalas AWQ, puntos cero GPTQ)
- Configuraciones específicas del modelo (escalado RoPE, máscaras de atención, plantillas de chat)
- Configuración del motor (`vllm_config.yaml`, muestreo por defecto, manifiestos de adaptador LoRA)

> El 32 por ciento de los resultados de la recuperación de la LLM en 2026 fueron fracasados porque el equipo registró un peso pero olvidó:

La solución es un manifiesto de DR mínimo de tres archivos:

1. Todos los archivos bajo el modelo HF repo (pesos + configuraciones + tokenizer).
2. Configuración de servicio específica del motor.
3. Manifiesto de despliegue (K8s YAML, archivo de Docker, bloqueo de dependencia).

> 修复方案是三文件最低 DR 清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置;(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅

Además, ejecuta un ejercicio DR trimestral. El ejercicio JPMorgan US-East-1 alcanzó 22 minutos de recuperación en noviembre de 2024 sólo porque el libro de jugadas fue ensayado.

> Además: cada trimestre de ejecución DR 演练――JPMorgan 2024 年 11 月 US-East-1 演练达到 22 分钟恢复,正是因为预案经过排练――

### La residencia de datos es ortogonal

Si su router de caché envía una solicitud de origen de París a us-east-1 para un ajuste de prefijos, ha violado el GDPR independientemente de la ganancia de TTFT.

> Si su cajero de percepción de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de cajero de ca

### Números que debes recordar

- Cache hit vs miss TTFT gap: ~ 10x (80 ms vs 800 ms en 2K prompt).
- RTT interregional entre Estados Unidos y la UE: ~75 ms.
- Fallo de DR: 32% fallo de configuración de tokenizer/quant.
- JPMorgan us-east-1 falloover noviembre 2024: 22 minutos (30 minutos SLA).

## Usalo con el marco de ejecución
```figure
cache-aware-router
```

## Usalo

`code/main.py`simula tres estrategias de enrutamiento (round-robin, regional consciente de caché, global consciente de caché) en una carga de trabajo multi-región.

> `code/main.py`En la actualidad, el sistema de gestión de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de las redes de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los datos de los cuentas de los cuentas de cuentas de los cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas

## Envíe el producto .

Esta lección produce`outputs/skill-multi-region-router.md`- Dadas las regiones, las restricciones de residencia y el SLA, diseña un plan de ruta.

> 本课产 出  `outputs/skill-multi-region-router.md` Dadas regiones, restricciones de residencia y SLA, diseño de la ruta de programación.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿A qué velocidad supera el enrutamiento transregional el enrutamiento local, dado el RTT de 75 ms?
   Traducción:运行`code/main.py`❖ Dado 75ms RTT, ¿en qué punto la longitud de un camino transregional es superior a la de un camino local?
2. Su tasa de caché de impacto cae del 70% al 12%. Diagnóstico tres posibles causas y los observables que confirmarían cada uno.
   Traducción:Tu tasa de vida de causal de 70%  Bajó a 12%  Diagnosis Tres causas posibles y cada uno de los indicadores de observación de confirmación 
3. Diseñar un manifiesto DR para un modelo cuantificado AWQ 70B servidos en vLLM con 5 adaptadores LoRA.
   Por ejemplo, el modelo de diseño de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de la serie de modelos de modelos de la serie de modelos de modelos de la serie de modelos de modelos de los modelos de los modelos de modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de
4.    La Comisión Europea ha aprobado el proyecto de ley de la Unión Europea (UE) para la protección de los derechos humanos y la protección de las personas con discapacidad.
   La Comisión Europea ha aprobado el proyecto de ley de la Unión Europea (UE) para la protección de los derechos humanos y la protección de las personas con discapacidad.
5. Una solicitud de origen de París coincide con un prefijo en el este de Estados Unidos. ¿Lo envía?
   China: una solicitud de origen parisiense en el este de los Estados Unidos.- ¿Te encuentras en el camino?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Más Leer más Leer más

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) reutilización de la caché KV transregional con plazo de latencia de la red.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) Documentación de fallas de disponibilidad.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) Fuente de router consciente de la caché.
