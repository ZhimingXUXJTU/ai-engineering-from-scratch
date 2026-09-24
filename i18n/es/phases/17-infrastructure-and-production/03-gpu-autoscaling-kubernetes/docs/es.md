# GPU Autoscaling en Kubernetes  Karpenter, KAI programador, Gang programando  Auto ampliado Kubernetes  GPU de ajuste

> Tres capas, no una. Los nodos de provisiones de Karpenter se ejecutan dinámicamente (menos de un minuto, un 40% más rápido que el Cluster Autoscaler). KAI Scheduler maneja la programación de pandillas, la conciencia de la topología y las colas jerárquicas  evita la trampa de asignación parcial de 7 de 8 donde siete nodos esperan y se queman en una GPU faltante. Autoscalers de nivel de aplicación (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) escala en señales específicas de inferencia  profundidad de cola, utilización de caché KV  no ciclo de trabajo de CPU / DCGM. La trampa clásica de la HPA es que`DCGM_FI_DEV_GPU_UTIL`es una medición del ciclo de tarea: 100% podría ser 10 solicitudes o 100. vLLM asigna previamente memoria de caché KV, por lo que la memoria nunca activa la escalada.`WhenEmptyOrUnderutilized`política que termina con la ejecución de trabajos de GPU en mitad de la inferencia.

> **【中文解读】**Este capítulo presenta la estrategia de expansión automática de los recursos de la GPU en Kubernetes.
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·02(平台经济学)、Fase 17·04(vLLM)、Kubernetes 基础──三层扩缩:Karpenter(节点层) + KAI Scheduler(Pod 层帮规划) + 应用层(队列深度/KV利用率)──
> ¿ Qué es esto ?**【类比】**GPU 扩缩 = "餐厅运力调度"──Karpenter = 开新店(分钟级);KAI = 桌位组合(gang scheduling 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调座。HPA 陷:DCGM utilization rate is occupan空比,100% 可能是10个或100个请求必须使用Goodput(Phase 17·08)替代──

## Objetivos de aprendizaje

- Diagrafía de las tres capas de autoescalado (provisión de nodos, programación de grupos, nivel de aplicación) y nombra la herramienta utilizada en cada capa.
  La aplicación de la palabra "pintura" se utiliza en el diseño de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web.
- ¿ Por qué ?`DCGM_FI_DEV_GPU_UTIL`es la señal HPA incorrecta para vLLM y nombrar dos reemplazos (profundidad de cola, utilización de caché KV).
  Traducción:explicar por qué`DCGM_FI_DEV_GPU_UTIL`Es el resultado de la investigación de la investigación de la investigación y de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los campos de los
- Describa la programación de banda y el modo de falla de asignación parcial que KAI Scheduler impide (7 de las 8 GPUs inactivas).
  China 翻译:描述帮 调度和 KAI Scheduler 防止的部分分配故障模式(8 个 GPU 中 7 个空) ⋅
- Nombre de la política de consolidación de Karpenter (`WhenEmptyOrUnderutilized`) que cese la ejecución de trabajos de GPU y establece la alternativa segura para 2026.
  China 合并策略: decir出终止正在运行GPU 任务的卡珀特尔 合并策略`WhenEmptyOrUnderutilized`),并说明2026年的安全替代方案──

## El problema es la introducción del problema

> **【中文解读】**GPU se expande automáticamente en Kubernetes y tiene tres niveles de fallas: 1) HPA utiliza señales erróneas (GPU 占用率而非队列深度), que provocan que el tiempo de expansión no se expanda; 2) Cluster Autoscaler 节点供应太慢,长提示请求超时; 3) 多 GPU 分布式推理时部分分配;; 7-of-8 trap), 7 GPU 空转等第 8 个.

> **【拓展：GPU 集群管理】**En 2026 Kubernetes se ha convertido en una plataforma de clasificación estándar de servicios de LLM 推理服务──NVIDIA DGX Cloud、Google GKE、AWS EKS  都提供 GPU 节点池管理──Clear challenge lies in GPU 节点池管理──H100 约$3-4/hr), la ampliación de la decisión debe ser precisa 过度供给浪费成本, la falta de suministro afecta SLA──Karpenter + KAI Scheduler 组合 es el programa de regulación de GPU más maduro en la actualidad──

Tu equipo envía un servicio de LLM en Kubernetes.`DCGM_FI_DEV_GPU_UTIL`El HPA nunca aumenta  ya piensa que estás lleno. añade una réplica manualmente; TTFT cae. HPA todavía no escala. La señal te está mintiendo.

> Tu equipo en Kubernetes ha desplegado un servicio de LLM.`DCGM_FI_DEV_GPU_UTIL`作为信号设置了HPA──服务在业务时段保持在100%利用率──HPA 从不扩容它认为你已经满了──你手动添加一副本;TTFT下降──HPA 仍然不扩容──信号在欺骗你──

Separadamente, se utiliza Cluster Autoscaler para nodos. Una solicitud de 1M-token llega a las 2 a.m.; el cluster pasa 3 minutos proporcionando un nodo, y los tiempos de solicitud fuera.

> Por otro lado, usas el Cluster Autoscaler 管理节点──凌晨2点来一个M token的提示;集群花3分钟供给节点,请求超时──

Separadamente, se implementa un modelo 70B que requiere 8 GPU en 2 nodos. El grupo tiene 7 GPUs libres y 1 distribuido en 3 nodos. Cluster Autoscaler proporciona un nodo para la GPU 1 faltante. Siete nodos esperan 4 minutos quemando dinero mientras Kubernetes consigue la última GPU.

> De nuevo, tú implementaste un modelo 70B de 8 GPUs que necesita 2 nodos. El grupo tiene 7 GPUs en el aire, uno está distribuido en 3 nodos.

Tres capas, tres modos de falla diferentes. La autoescalación consciente de la GPU en 2026 no es "inclivar HPA". Es componer el provisioning de nodos, la programación de banda y la autoescalación de señales de aplicación.

> Tres niveles, tres diferentes modelos de fallas. La GPU de 2026 感知自动扩缩不是"打开 HPA" .

## El concepto central.

### Capas 1  Provisión de nodos (Carpenter)

> **【中文解读】**La primera es la oferta de nodos. Carpenter  control y regulación de Pod, en 45-60 segundos por necesidad de crear GPU 节点, en comparación con el tradicional Cluster Autoscaler 快约 40% `WhenEmptyOrUnderutilized`合并策略它将终止运行推理的 GPU 节点转移到更便宜的实例类型,导致请求失败和模型重新加载(5-20 分钟中断)。GPU 池应使用 `WhenEmpty`¿ Qué es eso ?`consolidateAfter: 1h`La estrategia de seguridad.

Karpenter observa los módulos pendientes y los nodos de provisión en ~ 45-60 segundos (Cluster Autoscaler normalmente toma 90-120 segundos para los nodos de GPU).`NodePool`restricción  si su cápsula necesita 8 H100 y el grupo no tiene un nodo correspondiente, Karpenter proporciona uno directamente en lugar de escalar un grupo existente.

> Carpenter  control y regulación de pod, en aproximadamente 45-60 segundos suministro de los nodos de cluster autoescalador para los nodos de GPU  usualmente necesita 90-120 segundos) ⋅ según `NodePool`约束动态选择实例类型 Si su Pod 需要8 个H100 且集群没有匹配节点, Carpenter 直接供应一个,而不是扩展现有组──

**The consolidation trap**: El defecto de Karpenter `consolidationPolicy: WhenEmptyOrUnderutilized`Es peligroso para los grupos de GPU. Terminará un nodo de GPU en ejecución para migrar las capsules a una instancia de tamaño correcto más barata. Para las cargas de trabajo de inferencia que significa desalojar las solicitudes en ejecución y recargar un modelo 70B en el nuevo nodo. La pérdida es minutos de capacidad más fallos de solicitud.

> **合并陷阱**: Carpenter de acuerdo`consolidationPolicy: WhenEmptyOrUnderutilized`Para la GPU 池 es muy peligroso. Por lo tanto, se puede terminar con el GPU 节, que está funcionando, y se puede mover al Pod 转移到更便宜的合适实例.

Configuración segura para las redes de GPU:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Permite a Karpenter consolidar nodos verdaderamente vacíos después de una hora pero nunca desalojar un trabajo en marcha.

> 让卡珀特在一小时后合并真正空的节点, pero nunca expulsa la misión en el funcionamiento.

### Capas 2  Programación de pandillas (KAI Scheduler)

> **【中文解读】**El segundo nivel es la coordinación de la regulación. El programa KAI  resolverá tres problemas por defecto que el programa no puede resolver: 1) la programación de grupos  todo tiene todo sin regulación, 8-GPU  sugerir que todo se inicie o todo espere; 2) la percepción de la escala  según el Pod NVLink/InfiniBand/机架拓放置; 3) la competencia de varios equipos en la misma GPU 池时按优先级和配额管理.

> **【拓展：GPU 调度器生态】**La selección de GPU 调度器 de 2026 incluye KAI Scheduler(原Karp,支持gang + topology + queue)、YuniKorn(Apache 项目,支持队列和抢占)、以及 el cronómetro por defecto + 设备插件。KAI Scheduler es el único esquema de programación de gang originalmente apoyado, ya ha sido integrado por Ray 和 vLLM producción-stack 集集──对需要多场景的 GPU 分布式推理的场景;;70B+ 模型),KAI es el requisito obligado──

KAI Scheduler (proyecto "Karp" entonces renombrado) maneja lo que el kube-scheduler predeterminado no hace:

**Gang scheduling**Una capsula de inferencia distribuida que requiere 8 GPU o todos los 8 comienzan juntos o ninguno lo hace. sin esto, obtienes la trampa de asignación parcial: 7 de 8 capsules comienzan, esperan indefinidamente, queman dinero.

**Topology awareness** saber qué GPU comparten NVLink, que se sientan en el mismo estante, que tienen InfiniBand entre ellos. Colocar las pods en consecuencia. Una carga de trabajo tensor-paralelo DeepSeek-V3 67B debe permanecer en un dominio NVLink; KAI Scheduler respeta eso.

**Hierarchical queues** varios equipos compiten por la misma GPU con prioridad y cuota.

KAI se implementa junto con kube-scheduler como un cronómetro secundario; se anota las cargas de trabajo para usarlo.

> KAI 作为二级调度器和 kube-scheduler 一起部署;你通过注解让工作负载使用它──Ray 和 vLLM producción-stack 都已集成──

### Capas 3  señales de nivel de aplicación

> **【中文解读】**El tercer nivel es el de la aplicación de las señales.`DCGM_FI_DEV_GPU_UTIL`Es la tasa de ocupación de GPU (cíclico de deber) indicador 100% puede significar 10 个请求或 100 个请求, ya que la GPU está ocupada.

> **【拓展：推理感知自动扩缩】**NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler es un amplificador de diseño de diseño de LLM de 2026 especializado en el uso directo de los motores de cálculo.

**The HPA trap**¿ Qué es esto ?`DCGM_FI_DEV_GPU_UTIL`es una métrica de ciclo de trabajo  mide si la GPU estaba haciendo el trabajo en cada intervalo de muestreo. El 100% de utilización podría significar 10 solicitudes simultáneas o 100; la GPU estaba ocupada de cualquier manera.

Peor aún, los motores vLLM y similares asignan previamente la memoria caché KV (hasta `--gpu-memory-utilization`El uso de memoria se mantiene cerca del 90% incluso en una sola solicitud.

**2026 replacement signals**¿Qué es esto ?

- Profundidad de la cola (número de solicitudes que esperan preempleo).
  En inglés, "Leave a Look" significa "Permanecer el tiempo".
- Utilización de la caché KV (cuál es la fracción de bloques asignados a las secuencias activas).
  La cantidad de datos que se almacenan en el archivo se distribuye a la cantidad de bloques de la serie activa.
- Por réplica P99 TTFT (su señal de SLA).
  En el caso de los países de la Unión Soviética, el gobierno de la República de China ha adoptado una política de paz.
- Producción de producto (solicitudes de satisfacción de todos los SLOs por segundo).
  En inglés, "Goodput" (en inglés, "Goodput") es el nombre de las peticiones de SLO.

NVIDIA Dynamo Planner y llm-d Workload Variant Autoscaler consumen estas señales y réplicas de escala.

> NVIDIA Dynamo Planner y llm-d Variante de Carga de Trabajo Autoscaler 消费这些信号并扩缩副本──它们 completamente sustituyeron a la HPA en el servicio LLM──

### ¿Cuándo utilizar qué

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】**Las estrategias clave para optimizar los costos de GPU 集群 en 2026 incluyen: 1) Spot InstanceAWS/GCP/Azure  GPU Spot instance se puede ahorrar 60-70%, pero necesita procesar interrupciones(Carpenter + 热池缓解); 2) Auto expansiónCarpenter en el período de no alta altura se reduce automáticamente en la cuota de puntos, 50% de gastos de ahorro; 3) GPU compartición  a través de MIG(Multi-Instance GPU) se dividirá en más ejemplos, adaptado a los modelos pequeños; 4) 混合 GPUFP8/INT4 量化减少内存需求,允许更多并发; 2) 5) 分离式部署prefill/decode 分离到不同本类 ,30-40% 精节省;;

### El preempleo/decodificación desglosado lo complica todo

> **【中文解读】**La fase 17·17) aumenta aún más la complejidad de expansión: el preempleo Pod  según la profundidad de la fila de expansión, el descomposición Pod  según el caché KV  presión de expansión。 no se puede utilizar una sola HPA en ambos en la necesidad de sus propias estrategias de expansiónllm-d los dos se exponen como un servicio Kubernetes independiente, cada servicio tiene su propio HPA

> **【拓展：Kubernetes GPU 生态】**2026 años Kubernetes GPU  gestión de componentes clave incluyen: NVIDIA GPU Operador(auto instalación de la unidad / CUDA / contenedor herramienta) ✓ NVIDIA Dispositivo Plugin(GPU  recursos de descubrimiento y distribución) ✓ MIG(Multi-Instancia GPU, se dividirá en varios ejemplos) ✓ tiempo ✓ GPU 共享) ✓ ✓ 结合 Karpenter + KAI Scheduler + Dynamo Planner, puede realizar desde el punto de entrega hasta el Pod 调度 hasta la copia de la expansión de la GPU completa ✓

Si ejecuta una preemplaza/decodificación desagregada (fase 17 · 17), tiene dos clases de capsules con diferentes desencadenantes de escala: escala de capsules de preemplaza en profundidad de cola, escala de capsules de decodificación en presión de caché KV. llm-d expone estos como separados `Services`No trate de poner un solo HPA frente a ambos.

> Si se ejecuta una operación separada de preempleo/desenrollo (Fase 17 · 17), usted tiene dos Pods con diferentes amplificadores: Pods preemplados de acuerdo con la profundidad de la línea de expandir, Pods desencadenados de acuerdo con KV  Pressión de almacenamiento expandirse―llm-d expandirlos en forma independiente `Services`Cada persona tiene su propio HPA. No intentes dejar un HPA en la cara de los dos.

### El inicio frío también importa aquí

La mitigación de arranque en frío (fase 17 · 10) es cuando el tiempo de provisión de nodos se vuelve visible para el usuario.`min_workers=1`) para las rutas críticas de SLO, o utilizar puntos de control de estilo Modal en la capa de aplicación.

> La fase 17 · 10) es el punto de suministro de tiempo que se vuelve un lugar perceptible para el usuario.`min_workers=1`), o en la aplicación de la modalidad de uso 风格的检查点──

### Números que debes recordar

- Provisión de nodos de carpenter: ~ 45-60s vs Cluster Autoscaler ~ 90-120s (nodos GPU).
  Carpenter 节点供给: aproximadamente 45-60 秒 vs Cluster Autoscaler 约 90-120 秒(GPU 节点) 』
- El programa KAI evita la trampa de 7 de 8 residuos de asignación parcial.
  La información de la información de la empresa se encuentra en el sitio web de la empresa.
- `DCGM_FI_DEV_GPU_UTIL`como señal HPA: rotada; utilizar profundidad de cola o utilización de KV.
  En inglés:`DCGM_FI_DEV_GPU_UTIL`作为 HPA 信号:有缺陷; utilizar la profundidad de la línea de operaciones o la tasa de utilización de KV。
- Carpenter `WhenEmptyOrUnderutilized`: termina ejecutando trabajos de GPU.`WhenEmpty + consolidateAfter: 1h`para inferir.
  En inglés: Carpenter`WhenEmptyOrUnderutilized`任务――推理使用 终止运行中的 GPU 任务―― 推理使用 `WhenEmpty + consolidateAfter: 1h`¿Qué es eso?

## Usalo con el marco de ejecución

> **【拓展：GPU 自动扩缩成本模型】**El núcleo de optimización de costos de la GPU automática es reducir el tiempo de cambio en el espacio.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17.280── a través de Karpenter 按需供应 + `WhenEmpty`合并策略 + 推理感知 HPA, puede reducirse automáticamente a 2 GPU en el período no máximo, reducirá el costo mensual a aproximadamente $8,640 (ahorro de 50%) .
```figure
autoscaling
```

## Usalo

`code/main.py`Simula una autoescalada de tres capas en una carga de trabajo de GPU quebrada. Compara HPA ingenuo (ciclo de trabajo), HPA de profundidad de cola y escalada programada por la banda KAI. Reporta solicitudes no satisfechas, minutos de GPU inactivos y una puntuación compuesta.

> `code/main.py`En突发 GPU 工作负载上模拟三层自动扩缩机──比较简单 HPA(占用率) 队列深度 HPA 和 KAI 调度扩缩──报告未满足的请求数、空 GPU 分钟数和综合评分分──

## Envíe el producto .

Esta lección produce`outputs/skill-gpu-autoscaler-plan.md`. Dada la topología del grupo, la forma de la carga de trabajo y el SLO, diseña un plan de autoescalado de tres capas.

> 本课产 出  `outputs/skill-gpu-autoscaler-plan.md` Proporcionar un conjunto de dimensiones y una forma de carga de trabajo y un SLO, diseñar un esquema de expansión automática de tres niveles.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Cuántas solicitudes de HPA en el ciclo de trabajo naívo caen que capturan HPA en la cola? ¿De dónde viene la diferencia?
   Traducción:运行`code/main.py`◊ En la carga de trabajo de emergencia, la tasa de ocupación simple de la HPA se ha desviado de cuántas solicitudes se han captado en la línea de profundidad de la HPA? ¿De qué diferencia proviene?
2. Diseñar un NodePool de Karpenter para un grupo que sirve Llama 3.3 70B FP8 en H100 SXM5. Especificar `capacity-type`¿ Qué ?`disruption.consolidationPolicy`¿ Qué ?`consolidateAfter`, y una mancha que mantiene las cargas de trabajo no GPU fuera de estos nodos.
   Por ejemplo, el modelo de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de la plataforma de Internet.`capacity-type`¿Qué es esto?`disruption.consolidationPolicy`¿Qué es esto?`consolidateAfter`Y será un punto de separación de carga de trabajo sin GPU.
3. Su equipo informa que las implementaciones están atascadas en espera porque "GPUs disponibles pero la cápsula no programará". Diagnóstico ¿es este Karpenter, kube-scheduler, o KAI Scheduler? ¿Qué métricas confirman?
   China 翻译:你的团队报告部署卡在等待状态因为"GPU可用但Pod 无法调度"――诊断是卡宾特,库布-调度仪还是KAI调度仪? ¿Qué indicadores se pueden confirmar?
4. Elige una señal para las cápsulas de preempleo desglosadas a escala automática y otra señal para las cápsulas de decodificación.
   China: choosing one signal to expand separation式预填充 Pod, otro señal para descalificar Pod──为两者提供理由──
5. Calcule el coste de la `WhenEmptyOrUnderutilized`trampa de consolidación en un servicio de producción 24x7 que promedia 60 eventos de caída de solicitudes por día en P99 TTFT > 10s.
   Traducción:计算`WhenEmptyOrUnderutilized`合并陷在24x7 costes de producción de servicio, este servicio promedio 60 veces al día solicitación de abandono de eventos, P99 TTFT > 10 segundos.

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Más Leer más Leer más

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) documentos de diseño y ejemplos de configuración.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) semántica de la política de consolidación y las deficiencias de seguridad de la GPU.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) Dinamo Planner escala señales.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) Patrón de integración de rayos.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) Guía específica de Kubernetes gestionada.
- [llm-d GitHub](https://github.com/llm-d/llm-d) Diseño de la variante de autoescalador de carga de trabajo.
