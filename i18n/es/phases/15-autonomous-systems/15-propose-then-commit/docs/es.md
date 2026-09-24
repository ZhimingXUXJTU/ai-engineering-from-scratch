# El hombre en el bucle: Proponer-Entonces-Comprometerse.

> El consenso de 2026 sobre HITL es específico. No es "el agente pregunta, el usuario hace clic en Aprobar". Es proponer-entonces-comprometer: la acción propuesta se persiste a una tienda duradera con una clave de idempotencia; aparece ante un revisor con intención, linaje de datos, permisos tocados, radio de explosión y un plan de retroceso; se comete solo después de un reconocimiento positivo; verificado después de la ejecución para confirmar que el efecto secundario realmente ocurrió. El de LangGraph `interrupt()`Además de la verificación PostgreSQL, el marco de Microsoft Agent `RequestInfoEvent`, y Cloudflare's `waitForApproval()`El modo de falla canónica es la aprobación de sello de goma: "Aplicar?" se hace clic sin revisión. La mitigación documentada es el reto y la respuesta con una lista de verificación explícita.

> **【中文解读】**2026 años HITL 共识是具体的──不是"Agent 问, user点击 Approve"──是提出-then-commit:提议动作以等键持久化到持久存储;向审查员呈现意图、数据谱系、触及权限、爆炸半径、回滚计划;仅在正面确认后提交;执行后验证确认副作用实际发生──`interrupt()`Además PostgreSQL 检查点、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare de `waitForApproval()`Todos los países han logrado el mismo modelo.

> **【拓展：四个状态机步骤】**Proponer-entonces-comprometerse es un estado de cosas: 1) Proponer Agencia 产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划; 2) Presentar 审查者(人类, non-Agent 自审) ver todos los datos; 3) Submit正面确认,动作执行; 4) 验证执行后回读副作用确认──这是数据库`RETURNING` 子句、AWS `PutObject`后 `GetObject`、Stripe/AWS API 等键模式在代理审批上的复用──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·12(Ejecución Durable) Fase 15·14(Kill Switches) Fase 14·15(HITL Agent 模式) 本节是HITL的工程化标准四步状态机──
> ¿ Qué es esto ?**【类比】**Proposal-then-Commit = "Bank大额转账审批"──普通 LLM 调用 = 即时转账(错了找客服);Proposal-then-Commit = 提交转账申请(含收款人、金额、用途、回滚预案)→ 审查员看元数据 → 批准 → 执行 → 验证到账──每一步都不能省──这是人类计算机使用、Claude Code Plan Mode、Stripe API 等的键统一模式──
> ️ **【易错点】**"Approve?" 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响 N 个文件、M 个用户) ・・・

## El problema es la introducción del problema

> **【中文解读】**El modelo de "Proposición-Entonces-Comisión" requiere que el agente genere el programa de modificación pero no lo ejecute inmediatamente, sino que lo muestre al usuario u otro agente, revisar, revisar y luego presentar. Este es el modelo clave de "Proposición-Entonces-Comisión" que dará a la persona humana o al sistema una oportunidad de "pre-examinar y corregir" en la ejecución.

> **【拓展：propose then commit】**El modelo de presentación de la propuesta posterior es la práctica de seguridad estándar de los agentes de código de 2026 años. El código de Claude 默认使用这个模式生成修改建议并等待用户确认.

El agente toma una acción.El usuario tiene que decidir: aprobar o no. Si la decisión es instantánea, probablemente no sea una revisión.

> El usuario debe decidir si se aprueba o no. Si la decisión es inmediata, no puede ser una revisión.

La cuestión de la ingeniería es cómo hacer una revisión estructurada el camino de la menor resistencia.

> Si la decisión es estructurada, es lenta pero creíble. La cuestión de la ingeniería es cómo hacer que la revisión estructural sea el camino más mínimo de resistencia.

El patrón HITL de la era 2023 era una solicitud sincrónica: "¿El agente quiere enviar correo electrónico a X con el cuerpo Y  aprobar?" El usuario hace clic en Aprobar. Todo el mundo siente que el sistema es seguro. En la práctica esta superficie está fuertemente marcada con goma: los usuarios aprueban rápidamente, las aprobaciones predicen poco, y cuando el agente falla, la pista de auditoría muestra un largo historial de aprobaciones que el usuario no puede recordar.

> 2023 时代 HITL 模式是同步提示:"¿El agente debe enviar un correo a X,正文 Y批准?" usuario haga clic en Aprobar. Todo el mundo siente el sistema de seguridad.

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

El patrón 2026  proponer-entonces-comprometer  traslada HITL a un sustrato duradero, adjunta metadatos estructurados y requiere un compromiso positivo.

> El modelo 2026 años proposed-then-commit  will HITL  transfer to持久基板上, adicional estructurada元数据, requisito de presentación correcta

Cada SDK de agente administrado envía una versión: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`Los nombres de las API difieren; la forma no.

> Cada agente de gestión SDK`interrupt()`、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare `waitForApproval()`◊API 名称不同;形态不。

## El concepto central.

### La máquina de proponer y luego comprometerse

1. **Propose.**El agente produce una acción propuesta. Persistido a un almacén duradero (PostgreSQL, Redis, Objeto Durable). Incluye:
   En inglés:**提议。**Agente 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object) ──incluye:
   - Intención (por qué el agente está haciendo esto)
     En español, "Agent" significa "Agent"
   - linaje de datos (de qué fuente se derivó la propuesta)
     En inglés, el nombre de la fuente de datos es "Data谱系" (en inglés, "Data谱系")
   - permisos tocados (que es el alcance / archivos / puntos finales)
     En inglés, el nombre de la persona que tiene el poder de ser un miembro de la comunidad es el nombre de la persona que tiene el poder de ser un miembro de la comunidad.
   - radio de explosión (cuál es el peor caso)
     La peor situación es lo que ocurre.
   - plan de retroceso (si se ha cometido, cómo lo deshacemos)
     En español, "Return" significa "revoltar" (en inglés, "revoltar")
   - clave de independencia (única por propuesta; la reaprobación devuelve el mismo registro)
     Traducción:等键(每提议唯一; volver a enviar el mismo registro)
2. **Surface.**El revisor ve la propuesta con todos los metadatos.
   En inglés:**呈现。**El revisor ve con todas las propuestas de datos.
3. **Commit.**El reconocimiento positivo.
   En inglés:**提交。**Está confirmado.
4. **Verify.**Después de la ejecución, el efecto secundario se lee de nuevo y se confirma. Si el paso de verificación falla, el sistema está en un estado conocido de mala calidad y la alerta se activa.
   En inglés:**验证。** Se han confirmado los efectos secundarios posteriores a la ejecución. Si el proceso de verificación falla, el sistema está en un estado de mal funcionamiento y inicia la alerta.

### La clave de la impotencia.

Sin una clave de impotencia, un retiro después de un fracaso transitorio puede duplicar la ejecución de una acción aprobada.

> 没有等键, reprobar el proceso de fracaso inmediato puede duplicar la ejecución de la operación aprobada.

Ejemplo concreto: el usuario aprueba "transferir $100 de A a B". Blip de red. Vuelve a intentar el flujo de trabajo. El usuario ha aprobado una vez pero la transferencia se ejecuta dos veces. La clave de idempotency une la aprobación a un solo efecto secundario único; la segunda ejecución es una no-op.

> 具体例:用户批准"从A 转 $100到B"──网络闪断──工作流重试──用户批准一次但转账执行两次──等键将批准绑定到单一唯一副作用;第二次执行是无-op──

Este es el mismo patrón de idempotencia que utilizan las API de Stripe y AWS.

> Este es el mismo modelo de uso de Stripe y AWS API.

### Durabilidad: por qué las aprobaciones duran más que los procesos 持久性: por qué las aprobaciones tienen una vida útil más larga que los procesos

La sala de espera de la aprobación es un estado que el agente no posee. El flujo de trabajo se detiene (lección 12).`interrupt()`con el punto de control PostgreSQL y no sólo en estado de memoria  una aprobación dos días después todavía encuentra el flujo de trabajo intacto.

> 批准等候室是代理 不拥有一片状态――工作流暂停――第 12 课)――批准到达时,工作流从该精确点恢复――这就是为什么LangGraph将`interrupt()`La aprobación de PostgreSQL sigue encontrando un flujo de trabajo completo en lugar de un solo estado de memoria.

### Las aprobaciones de sello de goma y la mitigación de desafíos y respuestas.

La interfaz de usuario predeterminada para HITL ("Aplicar" / "Rechazar" botones) produce aprobaciones rápidas sin revisión genuina. Mitigation documentada: una lista de verificación de desafíos y respuestas que requiere respuestas positivas a preguntas específicas antes de que se habilite el botón Aprobar.

> HITL 默认 UI("Approve"/"Reject" 按)产生快速批准无真实审查──已记录缓解:在 Approve按启动前要求对特定问题正面回答的挑战-响应清单──具体形状:

- "¿Entiendes qué recurso se refiere a esto?
  Traducción: "¿Sabes qué es esto?
- "¿Ha verificado que el radio de la explosión es aceptable?
  Traducción: "¿Viste la explosión de la mitad aceptable?
- "¿Tienes un plan de retroceso si esto falla?"
  Traducción: "¿Si fracasa tienes planes de volver a rodar?

La investigación sobre la seguridad de los agentes antropóficos cita explícitamente el HITL basado en la lista de verificación como una mitigación para los patrones de aprobación de sello de goma.

> No es para el bur bur burgués ni para el burgués es una función obligatoria no puede hacer que el examinador de un cuadro sea o requiera clarificar (aumento) o rechazar (seguridad)

### Lo que cuenta como consecuencia es lo que se calcula como consecuencia.

No todas las acciones necesitan propuestas y luego compromisos.

> No es necesario que cada movimiento proponga-entonces-comprometerse.

- **Consequential actions**(siempre HITL): escritos irreversibles, transacciones financieras, comunicación de salida, cambios en la base de datos de producción, operaciones destructivas del sistema de archivos.
  En inglés:**后果性动作**(总 HITL): inávitas, transacciones financieras, comunicaciones externas, producción de bases de datos, cambios, manipulaciones de documentos y sistemas de información.
- **Reversible actions**(a veces HITL): modificaciones de archivos locales, cambios de env de puesta en escena, escritos reversibles con retroceso claro.
  En inglés:**可逆动作**(có veces HITL): 本地文件编辑、舞台化 环境变更、带清晰回滚的可逆写──
- **Reads and inspections**(nunca HITL): leer un archivo, listar recursos, llamar a una API de sólo lectura.
  En inglés:**读和检查**(从不HITL): Read文件、列资源、调用只读API。

### Verificación después de la acción.

"La ejecución de compromisos" no es lo mismo que "el efecto secundario ocurrió". Las condiciones de partición de red y carrera pueden producir un flujo de trabajo que cree que tuvo éxito mientras que el backend no persistió.`RETURNING`cláusulas o AWS `GetObject`después de`PutObject`¿ Qué ?

> "La presentación de un proyecto no es equivalente a "se producen efectos secundarios"  Las condiciones de competencia y distribución de la red pueden generar un proceso de trabajo que tenga éxito y no se prolongará posteriormente  Los pasos de verificación se realizan después de la presentación de un proyecto.`RETURNING`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `PutObject`后 `GetObject`El mismo modelo de AWS.

### Artículo 14 de la Ley de IA de la UE Artículo 14 de la Ley de IA de la UE

El artículo 14 exige una supervisión humana efectiva de los sistemas de IA de alto riesgo en la UE. "Eficaz" no es decorativo. El lenguaje regulador excluye específicamente los patrones de sello de goma. Proponer-a continuación, comprometerse con desafío y respuesta es la forma que sobrevive al escrutinio del artículo 14 en los documentos de cumplimiento del Kit de herramientas de gobernanza de agentes de Microsoft.

> La aplicación de la ley de regulación de los agentes de la inteligencia artificial no es un uso de la tecnología de la inteligencia artificial.

## Usalo con el marco de ejecución
```figure
mx-propose-then-commit
```

## Usalo

`code/main.py`Implementa una máquina de estado de proponer y luego realizar en stdlib Python. El almacén duradero es un archivo JSON. La clave de idempotency es un hash de (thread_id, action_signature). El controlador simula tres casos: un flujo de aprobación limpio, un retiro después de un fallo transitorio (que no debe ejecutarse en doble), y un sello de goma por defecto frente a un flujo de desafío y respuesta.

> `code/main.py`Usando la base de datos Python 实现 proponer-then-commit 状态机──持久存储是 JSON 文件──等键是 (thread_id, action_signature) 的哈希──驱动器模拟三例:干净批准流、瞬态失败后的重试(必须不双执行)

## Envíe el producto .

`outputs/skill-hitl-design.md`revisa un flujo de trabajo de HITL propuesto para proponer y luego comprometer formas y señales de las capas de metadatos faltantes, de idempotencia, de verificación o de desafío y respuesta.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的建议-然后-承诺 形态并标记缺失的元数据、等、验证或挑战-响应层──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Confirmar que una nueva prueba de una propuesta aprobada utiliza el registro duradero y no reejecuta.
   Traducción:运行`code/main.py` confirmar que la propuesta ha sido aprobada y que se ha vuelto a realizar.

2. Extenda el registro de las propuestas con un `rollback`Simula una ejecución cuyo paso de verificación falla. Muestre el tiro de retroceso automáticamente.
   En inglés:`rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. Lea el marco de Microsoft Agent `RequestInfoEvent`Identificar un campo de metadatos que la API incluye que el motor de juguete está faltando. Añade y explique contra lo que protege.
   En inglés, "Mixed" es el nombre de la palabra "Mixed".`RequestInfoEvent`文档──识别 API 包含而玩具引擎缺失的一个元数据字段──添加它并解释它防止什么──

4. Diseñar una lista de comprobación de retos y respuestas para una acción específica (por ejemplo, "postar a una cuenta pública de Twitter"). ¿Qué tres preguntas debe responder el revisor? ¿Por qué esas tres?
   Por ejemplo, "enviar a un público Twitter 账号") diseñar desafío-响应清单―― el examinador debe responder a cuáles tres preguntas? ¿Por qué estas tres?

5. Seleccione un caso en el que una solicitud sincrónica de "¿Aplicar?" sea suficiente (no se necesita almacenamiento duradero). Explica por qué y nombra la clase de riesgo que está aceptando.
   China: Choose a "Approve" (¿Approve?)

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Más Leer más Leer más

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)¿ Qué es esto ?`RequestInfoEvent`, aprobaciones duraderas.
  En inglés:`RequestInfoEvent`、durante la aprobación.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/)¿ Qué es esto ?`waitForApproval()`y objetos duraderos.
  En inglés:`waitForApproval()`Y objetos duraderos
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) HITL como mitigación del riesgo a largo plazo.
  En inglés, el nombre de la familia de los HITL es "HITL".
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) base de regulación para los sistemas de alto riesgo.
  Traducción:El sistema de control de las aguas de alta velocidad.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) marco constitucional en torno a la supervisión.
  El gobierno de la República de China ha establecido un marco de la Constitución.
