# Presupuestos de acción, límites de iteración y gobernadores de costos.

> El coste mensual de un agente de comercio electrónico de tamaño medio se ha disparado de $1,200 to $El equipo de Microsoft habilitó la habilidad de "tracking de pedidos". Eso no es un error de precios. Es un agente que encontró un nuevo bucle y mantuvo el gasto dentro de él.`max_tokens`, tokens por tarea y presupuestos en dólares, límites diarios / mes, límites de iteración, enrutamiento de modelos en niveles, caché de instantes, ventanas de contexto, puntos de control HITL en acciones costosas, interruptores de muerte en violación de presupuesto.

> **【中文解读】**El programa de formación de los agentes de comercio electrónico de la empresa se desarrolla en el equipo de activación de la habilidad de "tracking de pedidos" desde el año 2000.$1,200 跳到 $4,800── esto no es un error de fijación de precios── esto es un agente que encuentra un nuevo ciclo y lo sigue gastando── Microsoft's Agent Governance Toolkit (WEB ha preparado un conjunto de herramientas para este tipo de defensas: por petición.`max_tokens`、 cada tarea ficha 和 dólares presupuesto、 diario/mes límite 代上限、分层模型路由、提示缓存、上下文窗口、昂贵动作上 HITL 检查点、预算违反时的终止开关。Antropic's Claude Code Agent SDK 以不同名称出货相同原语──金融速度限制例如10分钟内 >$50 切断访问比月度上限更快捕获循环──

> **【拓展：单一上限不够 → 分层栈】**失败模式和时间尺度需要应对:5 秒重试的失控循环 (control de la captura de datos) ⋅ 2x 工作的缓慢泄漏 (control de datos) ⋅ 2x 工作的缓慢泄漏 (control de datos) ⋅ 5x token的坏发布 (control de datos) ⋅ 5x token of the bad release (control de datos) ⋅ 3x ⋅ 5x token of the bad release (control de datos) ⋅ 3x ⋅ 5x token of the bad release (control de datos) ⋅ 3x ⋅ 5x token of the bad release (control de datos) ⋅ 3x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 5x ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 2 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 2 ⋅ 1 ⋅ 1 ⋅ 2 ⋅ 2 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1 ⋅ 1  ⋅ 1 ⋅ 2  ⋅ 1                                                        

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·10(权限模式) Fase 15·12(持久执行) 云成本管理基础──Cost Governors = 防"Denial of Wallet" (Denial of Wallet) 钱包拒绝服务攻击) 
> ¿ Qué es esto ?**【类比】**El costo del gobierno es el de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración de la administración$50 切断（防失控）；(2) 每日上限——$200/天(防慢泄漏);$3000/月（防坏发布）；(4) 单任务上限——$5/ tarea (防单次任务爆炸)
> ️ **【易错点】**Sólo se establece un límite de velocidad en el mes → Una noche se quema un mes presupuesto sólo se encuentra.

## El problema es la introducción del problema

> **【中文解读】**Los controladores de costes controlan y limitan el consumo de recursos de los agentes, principalmente en API, con el uso de fichas y tokens.

> **【拓展：cost governors】**El control de contenido es el reto clave de la implementación de productos de agentes de 2025-2026. En el caso de los casos públicos: varios usuarios reportan codificar el código de los agentes, el usuario se encuentra en un ciclo de reparación y genera miles de dólares en API.

Los agentes autónomos gastan dinero en cada turno.

> Agente independiente en cada ronda de todo el tiempo.

El mal resultado de un chatbot es una mala respuesta; el mal bucle de un agente es una factura. El término documentado en la industria para el modo de falla es "Denial of Wallet"  el agente mantiene el razonamiento, mantiene las llamadas de herramientas, mantiene la facturación, y nada lo detiene porque nada fue diseñado para.

> 聊天机器人错误输出是一条错误回复; El ciclo de errores de un agente es una fact单―― 行业记录的失败模式术语是"Denial of Wallet"Agent 持续推理、持续调用工具、持续计费,没有什么阻止它,因为没有什么被设计为阻止──

La solución no es un número, sino una pila de límites en diferentes escalas de tiempo y granularidades: por solicitud, por tarea, por hora, por día, por mes. Una pila bien diseñada atrapa un bucle que se va en fuga en minutos, una fuga lenta en horas y una mala liberación en un día. La misma pila mantiene un presupuesto cuando el agente es de largo horizonte y autónomo.

> 修复不是 un número. Es una limitación de diferentes escalas y dimensiones de tiempo: por petición, por tarea, por hora, por día, por mes. Bien diseñado.  En minutos captura un ciclo de pérdida de control, en horas captura lenta fuga, en un día captura mala publicación.

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

Esta es una lección de ingeniería: las matemáticas son triviales, la disciplina es donde los equipos fallan. La lista de límites a continuación está nombrada en el kit de herramientas de gobernanza de agentes de Microsoft o en los documentos SDK de agente de código antropico Claude.

> Esto es un curso de ingeniería: Matemáticas ordinarias, la ley es el punto de fracaso del equipo.

## El concepto central.

### El gobierno de los costos estático.

1. **`max_tokens` per request.**Simplemente, impide que una sola llamada emita una terminación ilimitada.
   En inglés:**每请求 `max_tokens`。**简单―― evitar que el único uso se produzca sin límites.
2. **Per-task token budget.**En toda la carrera, no exceda los tokens N. Detente duro en el tope.
   En inglés:**每任务 token 预算。**整个运行不超过 N 个代币――上限处硬停――
3. **Per-task dollar budget.**Lo mismo que los tokens pero en moneda.`max_budget_usd`en el código de Claude.
   En inglés:**每任务美元预算。**Como el símbolo, pero en moneda.`max_budget_usd`¿Qué es eso?
4. **Per-tool call cap.**No más de N `WebFetch`llamadas, N `shell_exec`llamadas, etc.
   En inglés:**每工具调用上限。**No más de N 个 `WebFetch`调用  个 `shell_exec`调用 y así sucesivamente.
5. **Iteration cap (`max_turns`).**Iteraciones de bucles de agente totales; evita bucles de razonamiento infinitos.
   En inglés:**迭代上限（`max_turns`）。**总 Agent 循环代数; prevenir el ciclo de la proposición ilimitada
6. **Per-minute / per-hour / per-day / per-month cap.**Las ventanas rodantes, las filtraciones en diferentes escalas de tiempo.
   En inglés:**每分/时/日/月上限。**滚动窗口──在不同时间尺度捕获泄漏──
7. **Financial velocity limit.**Por ejemplo, "si el gasto excede los $50 en 10 minutos, corta el acceso". Captura quemaduras basadas en bucles antes de que las tapas mensuales se disparan.
   En inglés:**金融速度限制。**Por ejemplo, "si el gasto en 10 minutos supera los 50 dólares, corta la visita"
8. **Tiered model routing.**Default a un modelo más pequeño; escala a uno más grande sólo cuando un clasificador juzgue que la tarea lo justifica.
   En inglés:**分层模型路由。**默认小模型; sólo cuando las tareas de evaluación de categorías valoran la hora de subir a un modelo mayor―
9. **Prompt caching.**Contexto de sistema rápido y estable almacenado en la caché del proveedor; el costo de token de la re-envío es cercano a cero.
   En inglés:**提示缓存。**系统提示和稳定上下文存储在供应商缓存; token de re-发发 成本接近零──
10. **Context windowing.**Compacción / resumen para mantener el contexto activo por debajo de un umbral; reducción directa de los costos de los tokens.
    En inglés:**上下文窗口。**压缩/摘要保持活跃上下文低于值; direct token 成本降低──
11. **HITL checkpoints on expensive actions.**Antes de que una acción conocida como costosa (llamada de herramientas larga, descarga grande, una costosa actualización del modelo), requiere un toque humano.
    En inglés:**昂贵动作上的 HITL 检查点。**En el tiempo que se ha pasado, el grupo de trabajo de la compañía de la industria de la información (en inglés, "Modeli de Información") ha estado trabajando en el campo de la información.
12. **Kill switch on budget breach.**La sesión se aborta cuando se dispara cualquier cap. Se registra el cap; requiere un camino separado de reactivación.
    En inglés:**预算违反时终止开关。**任一上限触发时会话停止──上限被记录;需要单独重新启动路径──

### ¿Por qué la pila, no un cap? ¿Por qué es un  y no un límite?

Un único límite mensual sólo captura a un agente fugitivo después de que la cartera se haya ido. Un único límite por solicitud no captura nada a nivel de sesión.

> 单一月度上限只在钱包空后抓失控代理――单一每请求上限在会话级中什么也没抓―― Diferentes modelos de fracaso requieren diferentes medidas de tiempo:

- **Runaway loop**(agente atrapado en un retiro de 5 segundos): atrapado por el límite de velocidad.
  En inglés:**失控循环**(Agente 卡在 5 秒重试): velocidad límite de captura
- **Slow leak**(agente que hace ~ 2 veces el trabajo esperado por tarea): capturado por el límite diario.
  En inglés:**缓慢泄漏**(Agent para cada tarea hace 2x 预期工作): cada día captura de límite máximo
- **Bad release**(nueva versión utiliza fichas 5x): capturado por límite semanal / mensual.
  En inglés:**坏发布**(nova versión con 5x token): Cada semana / mes captura de límite.
- **Legitimate surge**(demanda real, no un error): atrapado por el límite hora / día con registro claro.
  En inglés:**合法激增**(Real Needs, No Bug):小时/日上限带清晰日志捕获──

### La superficie presupuestaria de Claude Code La superficie presupuestaria de Claude Code
### Superficie de presupuesto de arnés

El SDK de Claude Code Agent expone (documentos públicos):

> Claude Code Agent SDK 暴露(公开文档):

- `max_turns` Cap de iteración.
  En inglés:`max_turns`代上限── y ahora mismo.
- `max_budget_usd` límite de dólar; aborto en sesión por incumplimiento.
  En inglés:`max_budget_usd`美元上限; violación del tiempo de reunión suspendido.
- `allowed_tools`- ¿ Qué ?`disallowed_tools` alojador de herramientas y denilista.
  En inglés:`allowed_tools`- ¿ Qué ?`disallowed_tools` herramientas permiten la lista y rechazan la lista.
- Puntos de gancho antes de utilizar la herramienta para la contabilidad de costes personalizada.
  En el caso de los sistemas de cálculo de costes, el cálculo de los costes de los mismos está en el marco de la definición de los costes de cálculo.

Combinar con la escalera de modo de permiso (lección 10).`autoMode`sesión sin`max_budget_usd`La Antropic enmarca explícitamente el modo automático como que requiere controles presupuestarios; el clasificador es ortogonal al costo.

> Con el régimen de la libertad de expresión`max_budget_usd`de la `autoMode`El modo automático se fija en el marco de la necesidad de control presupuestario; la clasificación de los dispositivos y los costes se mantiene en el mismo.

### La ley de IA de la UE, la agencia OWASP Top 10

El conjunto de herramientas de gobernanza de agentes de Microsoft cubre los requisitos del Top 10 de la OWASP y del artículo 14 de la Ley de IA de la UE (supervisión humana).

> El programa de gestión de agentes de Microsoft  OWASP Agentic Top 10 y la ley de IA de la UE Artículo 14                                                                                                                                                                                                                                                 

### Lo observado .$1,200 → $4.800 casos observados.$1,200 → $4.800 casos

El caso real en los documentos de Microsoft: un agente de comercio electrónico cuyo costo mensual se triplicó después de que se agregó una nueva herramienta.

> Un caso real en Microsoft: un agente de comercio electrónico en el mes siguiente, el costo de añadir nuevos instrumentos se duplicó en tres veces.

La herramienta permitió al agente realizar encuestas sobre el estado de los pedidos durante cada sesión. No se detecta el bucle. No hay límite por herramienta. No hay alerta sobre el crecimiento semana tras semana. La solución fue un límite por herramienta más una alerta de crecimiento diario. Esta es una plantilla: cada nueva superficie de herramienta es un nuevo bucle potencial; cada nueva herramienta necesita su propio límite y su propia alerta.

> El instrumento permite al agente en cada sesión de la sesión el estado de la orden de la ronda. No hay límite de cada instrumento. No hay límite de cada instrumento.

## Usalo con el marco de ejecución
```figure
cost-governor-stack
```

## Usalo

`code/main.py`La simulación de un agente se ejecuta con y sin una pila de costos de gobierno de capas. El agente simulado se desvía a un bucle de votación después de algunos giros; la pila de capas la atrapa dentro de la ventana de velocidad mientras que un solo límite mensual no dispararía hasta días después.

> `code/main.py`模拟有和没有分层成本管理的代理运行──模拟代理在某些轮次后漂移到轮询循环;分层在速度窗口内捕获它,而单一级上限直到几天后才触发──

## Envíe el producto .

`outputs/skill-agent-budget-audit.md`Audita la pila de gastos de un agente propuesto y señala las capas faltantes.

> `outputs/skill-agent-budget-audit.md`审计提议的代理部 部署的成本管理并标记缺层──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirmar el límite de velocidad antes de que el límite de iteración se dispare en una trayectoria de circuito de votación.
   Traducción:运行`code/main.py` Confirmar la velocidad limitada en la línea de ciclo de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la ronda de la pregunta Capacitar la velocidad limitada en la línea de la medida de la medida de la cantidad de "costa" que el agente en la línea de la cadena de la cadena de la cadena de la cadena de la cadena de la cadena de la cadena Capacitar la cantidad de "costa" en la línea de la cadena de la cadena de la cadena de la cadena 

2. Diseñar un conjunto de tapas por herramienta para un agente de navegador (lección 11). ¿Qué herramienta necesita el tapa más ajustado? ¿Qué herramienta puede funcionar sin límites sin riesgo?
   Por ejemplo, en el caso de los equipos de navegación, el sistema de navegación de la navegación es un sistema de navegación de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de veloc

3. Lea los documentos de la herramienta de gobierno de los agentes de Microsoft. Enumera cada tipo de tapa los nombres de la herramienta. Mapa cada uno de los modos de falla (bucle de fuga, fuga lenta, mala liberación, aumento).
   En el caso de los agentes de Microsoft, el sistema de gestión de los agentes de Microsoft está diseñado para ayudar a los usuarios a obtener información sobre los resultados de los procesos de gestión de los agentes de Microsoft.

4. Precio de una operación sin vigilancia durante la noche para una tarea realista (por ejemplo, "triar 50 emisiones en un repo").`max_budget_usd`justificar el 2x.
   Por ejemplo, "分类 50 个仓库 issue")`max_budget_usd`Para tu punto de estimación de 2x...

5. El código de Claude `max_budget_usd`¿Qué es lo que provoca el corte y cómo se ve el re-habilitar?
   El código de Claude`max_budget_usd`En el tiempo de la sesión total costo. ¿Cómo se puede reiniciar el proceso de interrupción?

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Más Leer más Leer más

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop)¿ Qué es esto ?`max_turns`¿ Qué ?`max_budget_usd`, los herramientas de la ayuda.
  En inglés:`max_turns`¿Qué es esto?`max_budget_usd`、 herramientas permiten la lista―
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) puntos de control de los administradores de costes.
  El costo de la administración del gobierno es el costo de la administración del gobierno.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) control de costes del proveedor.
  Traducción:Provedor lado costo control.
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching) Mecánica de almacenamiento en caché.
  El mecanismo de almacenamiento.
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) Mecánica de almacenamiento en caché.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) perfil de costes para agentes de largo horizonte.
  El costo de la empresa es el costo de la empresa.
