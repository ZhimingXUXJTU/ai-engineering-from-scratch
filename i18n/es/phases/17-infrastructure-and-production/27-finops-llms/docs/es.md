# FinOps para LLM  Economía unitaria y atribución de múltiples inquilinos  FinOps de LLM  Unidad económica y multirrental atribución

> Las operaciones de fin de curso tradicionales se rompen en el gasto de LLM. Los costos son transacciones de tokens, no tiempo de disponibilidad de recursos. Las etiquetas no mapean  una llamada de API es una transacción, no un activo. Las decisiones de ingeniería (diseño de la oportunidad, ventana de contexto, longitud de salida) son decisiones financieras.`user_id`) para el precio de los asientos y la ampliación, por tarea (`task_id`¿ Qué es eso ?`route`) para el coste y la prioridad de la superficie del producto, por inquilino (`tenant_id`) para la economía de unidad y la renovación. Cuatro capas de tokens  prompt, herramienta, memoria, respuesta  un cubo se oculta gastar. Escala de ejecución para los productos multi-arrendatarios: límites de tasas por arrendatario (2-3 veces el pico esperado, 429 + retraso después de la prueba); límite de gasto diario (1,5-3 veces el límite contraído; activa el aumento de tasas + alerta); interruptores de apagado en el gasto z-score > 4 (pausa automática + página en llamada). Modelos de atribución: etiquetado y agregado, telemetría combinadora (trace-ID → facturación; mayor precisión), muestreo y extrapolación, asignación basada en modelos, fuente de eventos, transmisión en tiempo real. Metrica unitaria: costo por consulta resuelta, costo por artefacto generado  no $/M tokens. El etiquetado retroactivo siempre falta; instrumento de creación a petición.

> **【中文解读】** Tradicional FinOps en el gasto de LLM ha fallado  costo es Token 交易而不是资源运行时间──工程决策(提示设计、上下文窗口、输出长度) 提示设计、上下文窗口、输出长度) 提示输出长度) 提示输出长度) 提示2026年Playbook 建议在第一天建立三个归因维度:按用户,按任务,按租户──四个 Token 层 (提示、工具、单位记忆、响应) 提示、单位记忆、响应) 提示不能合并为一个桶──标标应为"每次解决的查询成本"",而不是"每百万 Token 成本"──

> **【拓展：FinOps → LLM 成本优化】**En la aplicación de LLM, el control de costes es un reto central. El principio de "construir en la solicitud en el punto de sepultura" de FinOps es la base de la observación de los resultados de los proyectos.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·13(可观测性) 、Fase 17·14(缓存) 、云 FinOps 基础──LLM FinOps = 传统 FinOps 失效后的新方法──
> ¿ Qué es esto ?**【类比】**LLM FinOps = "en función del coste de la carga de agua"。 tradicional FinOps = 按服务器 uptime(标签=资产);LLM FinOps = 按代币交易(标签=交易)。三大归因维度(1 day-one 必埋):por usuario(席位定价)、 por tarea(产品成本)、 por inquilino(单位经济)。 cuatro niveles de token(prompt/tool/memoria/respuesta)
> ️ **【易错点】**单位指标使用 $/M tokens 是错的, debería utilizar "每次解决查询的成本"──强制阶梯:限流(2-3x 峰值)→日上限(1.5-3x 合约)→ kill switch(z-score>4 自动暂停)──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Explica por qué las FinOps tradicionales (tags + tiers) rompen el gasto de LLM y nombra las tres nuevas dimensiones de atribución.
  China Translation: explica por qué tradicional FinOps (en inglés: FinOps) en el LLM   gastos en el que no funciona, y dice tres nuevas dimensiones                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
- Enumera las cuatro capas de tokens (prompt, herramienta, memoria, respuesta) y por qué la facturación de un solo cubo esconde el costo.
  En el texto original, el texto se basa en el texto de la traducción de la traducción de la lengua inglesa.
- Diseñar una escalera de aplicación (capacidad de gasto → interruptor de ejecución) para un producto multi-arrendatario.
  En inglés, el nombre de la empresa es "LLC".
- Elija una métrica unitaria (costo por consulta / artefacto resuelto) en lugar de tokens $ / M.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

## El problema es la introducción del problema

> **【中文解读】**传统 FinOps en LLM 支出失效的核心原因:LLM 成本是代币 交易而不是资源运行时间──标签(tags) no se puede mapear directamenteAPI 调用是交易而不是资产──工程决策(提示设计、上下文窗口、输出长度) es la decisión financiera── tu cuenta muestra $40,000, pero no sabes: ¿qué arrendatario gastó cuánto 哪些 productos 功能驱动的是否有用利用、是快速 膨胀还是工具调用还是记忆扩大导致──

Su cuenta dice $40,000.
- ¿Qué inquilino lo gastó?
- ¿Qué característica del producto lo impulsó?
- Si un usuario individual fue abusador.
- Ya sea que la hinchazón rápida, las llamadas de herramientas o la amplificación de la memoria fueran los culpables.

El etiquetado y agregado en el lado del proveedor funciona para los recursos en la nube (EC2, S3) donde las etiquetas se propagan a los elementos de línea. Las llamadas de LLM API no etiquetan automáticamente.

## El concepto central.

### Tres dimensiones de atribución

**Per-user**(El artículo`user_id`): quién cuesta qué. Implica el precio de los asientos, las conversaciones de expansión, identifica a los usuarios de energía.

**Per-task**(El artículo`task_id`¿ Qué es eso ?`route`): qué superficie de producto cuesta qué.

**Per-tenant**(El artículo`tenant_id`): qué cliente es rentable.

Instrumentos los tres en el lugar de llamada en el primer día.

### Cuatro capas de símbolo

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

Si juntas las cuatro, la optimización se ve ciega.

### Escala de ejecución

> **【中文解读】**Dos tipos de productos de alquiler: 1) Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido límite  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido  Rápido Rápido  Rápido  Rápido  Rápido  Rápido Rápido Rápido Rápido  Rápido  Rápido  Rápido  Rápido  Rápido R

> **【拓展：LLM FinOps 的复合优化栈】**缓存 + 批处理 + 路由 + 网关) 叠加后的效果:(1) 缓存 L2(Fase 17·14) 约10x 更便宜的输入;(2) 批处理(Fase 17·15) 50%折扣;(3) 路由到廉价模型(Fase 17·16) 60% 成本降低;(4) 网关效率(Fase 17·19) 冗余 + 重试──全叠加最优可降至朴素基线的约5-10%──大多数团队只启用了2-3杆,很少有团队叠加了四个全部──

1. **Rate limit**Por inquilino. 2-3 veces el máximo esperado.`Retry-After`El inquilino ve fricción, no hay factura sorpresa.

2. **Daily spend cap**El límite de la tasa de restricción + alerta al éxito del cliente.

3. **Kill switch**en el gasto z-score > 4 en relación con la línea de base del inquilino.

### Modelos de atribución

- **Tag-and-aggregate**En el caso de los Estados miembros, el número de datos de la base de datos es de un tamaño muy reducido.
- **Telemetry joiner**La mayor precisión, los equipos maduros hacen.
- **Sampling + extrapolation**El precio de la muestra es de 5 a 10%, multiplicado.
- **Model-based allocation**Para los datos heredados sin etiquetas.
- **Event-sourced**El costo de la información en el tiempo real.
- **Real-time streaming**: actualizaciones del tablero de instrumentos subsegundo.

### El costo por X es la métrica unitaria

> **【中文解读】**Los tokens $/M son el lenguaje de los proveedores. Los indicadores de productos deben ser: 1) Cada solución de apoyo de un solo costo; 2) Cada costo de producción; 3) Cada costo de tarea de un agente exitoso; 4) Cada usuario tendrá un minuto de costo.

Los tokens $/M son el habla del proveedor.

- Costo por boleto de apoyo resuelto.
- Costo por artículo generado.
- Costo por tarea exitosa del agente.
- Costo por sesión de usuario-minuto.

En el caso de los productos, el coste de la optimización no es garantizado.

### Forma de rastreo de la atribución de costes

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

Emite en cada llamada. Almacenar en el lago de datos. Agregado por dimensión. fase 17 · 13 observabilidad pila es donde vive este.

### El conjunto de ahorros compuestos

Stack: caché + lote + ruta + puerta de entrada.
- Cache L2 (fase 17 · 14): ~ 10 veces más barato.
- Batch (fase 17 · 15): descuento del 50%.
- Ruta al modelo barato (fase 17 · 16): reducción de costes del 60%.
- Eficiencia de la puerta de entrada (fase 17 · 19): redundancia + retrasos.

En el mejor de los casos, entre el 5 y el 10% de la base de ingenuidad.

### Números que debes recordar

- Dimensiones de atribución: por usuario, por tarea, por inquilino.
- Cuatro capas de símbolo: prompt, herramienta, memoria, respuesta.
- El interruptor de eliminación: gastar z-score > 4.
- Metrica unitaria: costo por consulta resuelta, no tokens $/M.
- Optimizaciones apiladas: ~ 5-10% de la línea de base posible.

## Usalo con el marco de ejecución
```figure
i4-spend-ladder
```

## Usalo

`code/main.py`simula un servicio de LLM multi-arrendatario con la escalera de ejecución de tres niveles. Inyecta a un arrendatario abusivo y demuestra el disparo del interruptor de muerte.

> `code/main.py`simula un servicio de LLM multi-arrendatario con la escalera de ejecución de tres niveles. Inyecta a un arrendatario abusivo y demuestra el disparo del interruptor de muerte.

> `code/main.py`simula un servicio de LLM multi-arrendatario con la escalera de ejecución de tres niveles. Inyecta a un arrendatario abusivo y demuestra el disparo del interruptor de muerte.

## Envíe el producto .

Esta lección produce`outputs/skill-finops-plan.md`.Dado el producto y la escala, diseña el esquema de atribución y la escalera de ejecución.

> 本课产 出  `outputs/skill-finops-plan.md`.Dado el producto y la escala, diseña el esquema de atribución y la escalera de ejecución.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿A qué punto dispara el interruptor de muerte?
   Traducción:运行`code/main.py`¿Cómo evitar los errores de prensa?
2. Diseñar un panel de costos por inquilino, por tarea. ¿Cuáles son las 5 vistas que construye primero?
   En español, ¿qué 5 imágenes construye primero?
3. Su inquilino más grande es unidad-economía-negativo. Propón tres intervenciones ordenadas por impacto del cliente.
   China: 你最大的租户单位经济学为负. Propuso tres medidas de intervención en función del rango de clasificación.
4. Calcula el coste por boleto resuelto para un producto de soporte: 3M tokens/bilet, ~800 boletos/día, tasa almacenada en caché GPT-5.
   China: calcular el costo de un solo producto: 3M tokens/un solo trabajo, aproximadamente 2,5 veces
5. Discutir si el etiquetado retroactivo puede funcionar alguna vez. ¿Cuándo es aceptable?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## Más Leer más Leer más

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
