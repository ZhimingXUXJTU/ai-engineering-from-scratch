# Ingeniería del caos para LLM Producción 工程 生产 混沌 LLM

> La ingeniería del caos para LLM es su propia disciplina en 2026. Requisitos previos a la ejecución de experimentos en producción: SLI/SLO definido, observabilidad de traza+metría+registro, retroceso automático, libretas de ejecución, en llamada. La arquitectura tiene cuatro planos: control (programador de experimentos), objetivo (servicios, infra, almacenes de datos), seguridad (garda + abortar + filtros de tráfico), observabilidad (metricas + rastros + registros), retroalimentación (a ajustes SLO). Las barandillas de seguridad son obligatorias: las alertas de velocidad de quemadura interrumpen los experimentos si se espera que se produzca una quemadura de error-ordenario diario > 2 veces; ventanas de supresión + correlación de identificación de rastreo deducir ruido de alerta. Cadencia: revisión semanal de los pequeños canarios + SLO; día de juego mensual + postmortem; auditoría trimestral de resiliencia entre equipos + mapeo de dependencia. Experimentos específicos de LLM: sobrecarga de memoria, fallas de red, interrupciones de proveedores, instrucciones malformadas, tormentas de desalojo de caché KV. Herramientas: Ingeniería del Caos de aprovechamiento (recomendaciones derivadas del LLM, reducción de radio de explosión, integración de herramientas MCP); LitmusChaos (CNCF); Chaos Mesh (nativa de Kubernetes de la CNCF).

> **【中文解读】**Este capítulo presenta la práctica del servicio de la LLM 混沌工程主动注入故障来测试 LLM 服务性的实践.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·23(SRE) 、Fase 17·13(可观测性) 、SRE 基础(SLI/SLO/错误预算) ⋅LLM 混沌工程 = 主动注入故障测性──
> ¿ Qué es esto ?**【类比】**LLM 混沌工程 = "Ensayo de fuego"。前提:SLI/SLO 定义好、可观测、自动回滚、runbook、on-call。四平面:控制(实验调度) +目标(服务/数据/基础设施) +安全(守卫/中止/流量过) +可观测──必须护:错误预算燃烧率 > 2x 时暂停实验──节奏:每周小卡纳里度+月度游戏天+季度跨团队审计──LLM 专属实验:内存过载、网络故障、供应商 机、坏快点、KV缓存 驱逐风暴──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Nombre de los cinco requisitos previos de la ingeniería del caos (SLI/SLO, observabilidad, retroceso, libros de ejecución, en llamada) y explica por qué saltar cualquier práctica rompe la práctica.
  En el contexto de la política de la Unión Europea, el gobierno de la Unión Europea ha adoptado una política de paz y de paz.
- Diagrama los cuatro planos (control, objetivo, seguridad, observabilidad) y el bucle de retroalimentación en SLO.
  China: traduce: dibujar cuatro planos (control, objetivo, seguridad, observación) y reverso ciclo hasta el tablero de instrumentos de SLO.
- Enumere cinco experimentos específicos de LLM (supercarga de memoria, falla de red, interrupción del proveedor, respuesta incorrecta, tormenta de desalojo de KV).
  En el caso de los sistemas de gestión de datos, el sistema de gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de cuyo de cu
- Elige una herramienta  Arnes, LitmusChaos, Chaos Mesh  dada pila.
  En inglés, el lenguaje de la lengua árabe es el lenguaje de la lengua árabe.

## El problema es la introducción del problema

> **【中文解读】**LLM 混沌工程是2026年的独立学科──LLM 增加了新的故障模式:4K-token 毒化字符使分词器卡住12秒;上游提供商 429 触发网关重试,重试放大并发导致OOM;突发负载下 KV Cache 淘汰风暴引发重填级联,耗尽计算资源──这些都不会出现单元测试中混沌工程工具直到用户发现它们的方法──

> **【拓展：LLM 混沌工程的五类实验】**2026 LLM 特定五类混沌实验:(1) 内存过载发送长上下文高并发请求引发 KV Cache 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断断推理网关与供应商的连接,观察故障是否在 SLA内生效;(3) 供应商中断模拟100% OpenAI 429,观察路由是否失败到人类;(4) 形提示注入死载分层嵌套 Unicode、UTF-8码点卡),观察单个请求锁住员工淘汰;5) KV 淘汰巨大暴风和vLLM 块预算强制淘汰, L L 恢复服务MC 降级观察.

Se establece la prueba de caos en las pilas tradicionales. LLM pilas añaden nuevos modos de falla. Un aviso de token 4K con un carácter venenoso detiene el tokenizador durante 12 segundos. Un proveedor de agua arriba 429s; su puerta de entrada retenta; sus OOMs de servicio en simultánea amplificada retenta. Una tormenta de desalojo de caché KV bajo carga de explosión causa cascadas de reposición que saturan la computación.

Ninguno de estos aparecen en las pruebas de unidad.

## El concepto central.

### Pre-requisitos

> **【中文解读】**En producción se ejecuta un ensayo de caos en el que se han definido cinco premisas: 1) SLI/SLO 已 definido; 2) 可观测性(trace + metric + log) ya desplegado; 3) 自动回滚机制就绪; 4) 结构化跑本已编写; 5) 有值班人员响应──缺少任何一项,混沌就会变成真实事件──四个平面:控制面(实验调度器) 目标面服务/基础设施) 安全、面杀开机 + 抑制窗口 + 爆炸射线 限制) 、观测面标签 + 轨迹 关关) 反循环将发现可回到 SLO 调整、运行 更新和代码书修复──

No hay caos en la producción sin:

1. **SLI/SLO** definidos indicadores y objetivos de nivel de servicio.
2. **Observability** rastros, métricas, registros, conectados a los paneles.
3. **Automated rollback** Fase 17 · 20 Rollo de la bandera política.
4. **Runbooks** estructurados, fase 17 · 23.
5. **On-call** alguien que responda.

Faltando cualquier medio el caos se convierte en un incidente real.

### Cuatro aviones + retroalimentación

**Control plane** programador de experimentos (flujo de trabajo de Litmus, programación de Chaos Mesh, UI de Arnes).

**Target plane** servicios, capsules, nodos, balanceadores de carga, almacenamiento de datos.

**Safety plane** interruptor de apagado, ventanas de supresión, límites de radio de explosión, puertas de error de presupuesto.

**Observability plane** métricas normales + correlación de identificación de rastro para distinguir los fallos inducidos por el caos de los fallos naturales.

**Feedback loop** los resultados se reflejan en el ajuste de SLO, las actualizaciones de los directorios de ejecución, las correcciones de código.

### Las barandillas de vigilancia son obligatorias

> **【拓展：混沌工程的安全护栏】**Los tres requisitos necesarios para la seguridad de la ingeniería de caos: 1) la tasa de quema de los errores de presupuesto durante el experimento si el gasto diario excede las 2 veces esperadas, se interrumpe automáticamente el experimento; 2) la inhibición de la ventana en el intervalo de explosión del experimento, evitando el ruido en la llamada; 3) el rastreo de identificación de los errores causados por los experimentos, que los experimentos en la llamada pueden ser repetidos.

- **Burn-rate alert**: experimentar en pausa si el presupuesto de errores diario excede el 2 veces el esperado.
- **Suppression windows**: silenciar las alertas no experimentales en el radio de la explosión durante el experimento.
- **Trace-ID correlation**: todos los errores inducidos por el experimento llevan una etiqueta para que la llamada pueda deducirse.

### Cinco experimentos específicos de la LLM

1. **Memory overload** forzar una tormenta de prevención de caché KV enviando solicitudes de contexto largo con alta concurrencia. Observe: ¿el servicio se desprende graciosamente o se estrella?

2. **Network failure** cortar la conectividad entre la puerta de entrada de inferencia y el proveedor.

3. **Provider outage simulation** 100% 429 de OpenAI. Observación: ¿ha fallado el enrutamiento a Anthropic? (fase 17 · 16, 19)

4. **Malformed prompt** inyectar la carga útil de instalar tokenizadores (por ejemplo, unicode profundamente anidado, un enorme punto de código UTF-8). Observa: ¿una sola solicitud bloquea a un trabajador?

5. **KV eviction storm** desalojo forzoso mediante la saturación del presupuesto del bloque de VLLM. Observe: ¿se recupera el LMCache o se degrada el servicio?

### Cadencia

- **Weekly** pequeños experimentos de canarios en la puesta en escena, tal vez un 5% de pro.
- **Monthly** el día de juego programado en un escenario específico; asistencia entre equipos; post mortem.
- **Quarterly** Auditoría de la resiliencia entre equipos; actualización del mapa de dependencias.

### Equipamiento

> **【拓展：混沌工程工具选择】**2026 años de caos en ingeniería de herramientas seleccionadas:(1) Harness Chaos Engineering商业,AI 驱动的实验推,blast radius自动缩放,MCP 工具集成;(2) LitmusChaosCNCF 毕业,Kubernetes 工作流式;(3) Chaos MeshCNCF 沙箱,Kubernetes-native CRD风格;(4) Gremlin商业,广泛支持;(5) AWS FIS / Azure Chaos Studio托管云服务──节奏建议:每周小卡纳里 实验 + SLO 审查,每月游戏日 + 后期,每季度跨团队性审计 + 依赖映射更新──

- **Harness Chaos Engineering** comercial; recomendaciones de experimentos derivados de IA; reducción de la escala del radio de explosión; integración de herramientas MCP.
- **LitmusChaos** Graduado en CNCF; basado en el flujo de trabajo de Kubernetes.
- **Chaos Mesh** Sandbox CNCF; estilo CRD nativo de Kubernetes.
- **Gremlin** comercial; apoyo amplio.
- **AWS FIS**- ¿ Qué ?**Azure Chaos Studio** Ofertas administradas en la nube.

### Comenzando pequeño

Primero experimento: un pod para matar una réplica de decodificación bajo tráfico constante. Observa el redireccionamiento y la recuperación. Si esto funciona y parece seguro, graduarse en el caos de la red.

Primero experimento específico de LLM: inyectar a un proveedor 429 durante 5 minutos. Observa la caída. La mayoría de los equipos descubren que su caída no fue completamente probada.

### Números que debes recordar

- Cuatro aviones: control, objetivo, seguridad, observabilidad.
- Pausa de la tasa de quemaduras: 2 veces el presupuesto diario esperado.
- Cadencia: canario semanal, día de juego mensual, auditoría trimestral.
- Cinco experimentos de LLM: memoria, red, proveedor, respuesta defectuosa, tormenta KV.

## Usalo con el marco de ejecución
```figure
i4-chaos-guard
```

## Usalo

`code/main.py`Simula tres experimentos de caos con puertas de seguridad de aviones.

> `code/main.py`Simula tres experimentos de caos con puertas de seguridad de aviones.

> `code/main.py`Simula tres experimentos de caos con puertas de seguridad de aviones.

## Envíe el producto .

Esta lección produce`outputs/skill-chaos-plan.md`Dado su tamaño y madurez, elige los tres primeros experimentos y las herramientas.

> 本课产 出  `outputs/skill-chaos-plan.md`Dado su tamaño y madurez, elige los tres primeros experimentos y las herramientas.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Qué experimento desactiva la puerta de la velocidad de quemadura y por qué?
   Traducción:运行`code/main.py`¿Qué experimento ha provocado el control de la temperatura?
2. Diseñar los primeros cinco experimentos de caos para un servicio RAG basado en vLLM. Incluye criterios de éxito.
   Por ejemplo, en el caso de los sistemas de gestión de los recursos humanos, el sistema de gestión de los recursos humanos (RG) se utiliza para crear un sistema de gestión de los recursos humanos.
3. Su alerta de la tasa de quemaduras interrumpió un experimento. ¿Cómo determina la causa raíz  caos o natural?
   Traducción:Tu incendio de la policía para suspender un experimento. ¿Cómo determinar el comportamiento de la causa y el comportamiento esperado?
4. ¿Cuándo es la producción la respuesta correcta?
   El análisis de la producción y la producción de los productos en el entorno de producción.
5. Nombre de tres modos de falla específicos de la LLM que el caos de red genérico no puede reproducir.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Más Leer más Leer más

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
