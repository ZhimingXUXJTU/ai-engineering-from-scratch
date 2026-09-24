# Puntos de control y retroceso.

> Cada transición del estado gráfico persiste. Cuando un trabajador se estrella, su contrato de arrendamiento expira y otro trabajador se lleva al último punto de control. Objetos duraderos de Cloudflare mantienen el estado durante horas o semanas. Proponer y luego comprometerse (lección 15) define un plan de retroceso por acción. La verificación post-acción cierra el ciclo. El artículo 14 de la Ley de IA de la UE obliga a la supervisión humana efectiva de los sistemas de alto riesgo  en la práctica, esto significa que los puestos de control deben ser consultables, los rollbacks deben ser ensayados y la pista de auditoría debe sobrevivir a una implementación. El modo de falla aguda: sin claves de impotencia y controles de precondiciones, un retiro después de un fallo transitorio puede duplicar una acción ya aprobada. La verificación después de la acción es lo que lo captura.

> **【中文解读】**Cada gráfico de estado de cambio de perpetuación;. trabajador  collapso en su plazo de alquiler, otro trabajador  en el último punto de control de recogida;. Objetos duraderos  Cloudflare 跨数小时或数周持有状态;; Proposición-then-commitment(第15 课) para cada acción definir un plan de vuelta;.

> **【拓展：幂等+前置条件+验证+回滚四件套】**仅等不够: considerar"当余额 > $1000 时从 A 转 $100 hasta B" de la aprobación de la operación. Recuperación de la ejecución de la operación. Sólo se aprobará la revisión, pero si A  sobrevalor en la operación y la recuperación de la operación se reduce a $500, la evaluación de la operación no se produce. Cada operación posterior requiere cuatro piezas:  y similar.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**Estudiar y aprender en el campo de la seguridad y la seguridad en el trabajo.
> ¿ Qué es esto ?**【类比】**检查点回滚 = "archivio del juego y读档"──检查点 = 自动存档(cada vez que pasa un关存一次);回滚 = 读档(这关打错了回到上一关)──后果性动作四件套 = 等键(防止重启两倍执行) + 前置条件(重启后世界状态仍符合预期) + 动作后验证(确认真实副作用发生) + 失败回滚(恢复到动作前)──
> ️ **【易错点】**只有等键没有前置条件检查 → 重启时余额已被其他流程改了仍执行 → 透支──修复:恢复时必须重检"批准时的世界状态"是否还成立(如"余额>$1000"是否还成立在恢复时)

## El problema es la introducción del problema

> **【中文解读】**检查点和回滚机制 permite al agente guardar el estado de control en el proceso de ejecución, salir de error y recuperarse de su estado anterior. Esto es similar al control de la versión de Git y los datos de base de datos. 检查点保持关键节点 (como antes de modificar un documento), 回滚在检查到错误时执行. 检查点和 Git的反转是两个典型实现.

> **【拓展：checkpoints rollback】**检查点-回滚是可靠的代理系统的基础设施――实现选择:(1) 文件系统级使用 Git或快照保存文件状态;(2) 数据库级使用事务保证数据一致性;(3) 应用级Agent自我管理检查点(如LangGraph)──关键权衡是检查点粒度太细会增加开销,太粗会丢失更多工作──

La ejecución duradera (lección 12) hace que un agente fallido sea reiniciable.

> 持久执行 (第 12 课) 使崩 Agent 可恢复──Proposer-then-commit (第 15 课) 使批准动作可审计──

Esta lección se une a ellos: ¿qué sucede cuando una acción aprobada se ejecuta parcialmente, se estrella y se reanuda?

> ¿Qué ocurre cuando se ejecuta la sección de la aprobación de la operación? ¿Cuándo se ejecuta la operación? ¿para qué estado?

Los sistemas reales lo hacen de manera diferente:

> El sistema de conexión es diferente:

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

- **LangGraph**Los controles de los trabajadores se realizan en el último punto de control.`interrupt()`, que en sí misma persiste.
  En inglés:**LangGraph**Cambiar el estado de cada uno de los puntos de control a PostgreSQL. Trabajo:`interrupt()`Por su parte, se ha perpetuado.
- **Cloudflare Durable Objects**Mantenga el estado de cada llave durante horas o semanas.
  En inglés:**Cloudflare Durable Objects**跨数小时或数周持有每键状态――将计算与已批准的存储同址――
- **Microsoft Agent Framework**expone `Checkpoint`Primitivos en la API de flujo de trabajo; replay más idempotency cubre retemptantes.
  En inglés:**Microsoft Agent Framework**En el trabajo flujo API`Checkpoint`Origin语;重放加等覆盖重试──

En cada caso, la combinación que realmente funciona es: clave de idempotencia + verificación de condiciones previas + verificación post-acción + retroceso en verificación-fallo.

> En cada caso, el componente efectivo es: 等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚──

## El concepto central.

### Cada transición persiste. Cada transformación se perdurará.

Una transición de estado gráfico es cualquier paso que mueve el flujo de trabajo de un estado llamado a otro. Las implementaciones ingenuas persisten solo en puntos de compromiso específicos; las implementaciones de producción persisten en cada transición. El costo (algunos escriben más) es pequeño en relación con la ganancia de fiabilidad (la repetición aterriza en cualquier lugar, la recuperación de arrendamiento es precisa).

> 图状态转换是将工作流从一个命名状态转移到另一个命名状态的任何步骤──简单实现只在特定提交点持久化;生产实现持久化每转换──成本几次额外写) 对可靠性收益(重放落在任何地方、租约恢复精确) 小──

### Recuperación de arrendamiento Recuperación de arrendamiento

Cuando un trabajador se estrella, el flujo de trabajo no se pierde; el contrato de arrendamiento (una afirmación de corta duración de que este trabajador está ejecutando esta carrera) simplemente expira. Otro trabajador toma el último punto de control y reanuda. El mecanismo de arrendamiento es lo que permite que los sistemas de producción sobrevivan a los despliegues sin perder el trabajo en vuelo.

> Trabajo 崩时工作流不丢失; rentación(Este trabajador está en ejecución de este funcionamiento) es sólo un período de tiempo. Otro trabajador 拾起最新检查点恢复.

### Impotencia más condiciones previas.

La capacidad de trabajo no es suficiente.$100 from A to B when balance > $1000. " El flujo de trabajo se compromete, se desploma en medio de la ejecución y se reanuda. Si solo se verifica la clave de desimpedencia y se reanuda la ejecución, la transferencia se ejecuta una vez (correcto). Pero considere que entre el desplome y el reanudación, el saldo de A cae a $ 500 a través de un flujo de trabajo diferente. La verificación de desimpedencia aún pasa; la condición previa no. Sin una verificación de condición previa, enviamos un sobregiro.

> 仅等不够――考虑: 工作流被批准"当余额 > $1000 时从 A 转 $100 hasta B"── trabajo flujo de presentación, ejecución en desplome, recuperación── Si sólo el control 等 clave de ejecución de la recuperación, transferir la operación una vez ((correcto) ── pero considerar el desplome y la recuperación entre A 余额通过另一工作流降至$500──等检查仍通过;前置条件不──没有前置条件检查,我们发透支──

Cada acción consecuente requiere de ambas cosas:

> Cada movimiento sexual posterior requiere dos cosas:

- **Idempotency key**: evita la doble ejecución.
  En inglés:**幂等键**: evitar duplicadas ejecuciones
- **Precondition check**El informe de la Comisión de Asuntos Exteriores de la Comisión de Asuntos Exteriores de la Unión Europea (UEA) confirma que el Estado sigue siendo coherente con lo aprobado.
  En inglés:**前置条件检查**El estado de confirmación sigue siendo de acuerdo con la aprobación.

### Verificación después de la acción.

"La herramienta devuelta 200" no es verificación. La verificación real vuelve a leer el estado objetivo y confirma que el efecto secundario realmente ocurrió.

> "工具返回 200" no es un test.

- Actualización de la base de datos: `UPDATE ... RETURNING *`a continuación, afirmen el estado previsto de las partidas de fila devueltas.
  En el contexto de la actualidad, el gobierno de la República de China ha adoptado una nueva política de desarrollo.`UPDATE ... RETURNING *`Luego decimos que regresamos al estado previsto.
- Envío de correo electrónico: compruebe la carpeta de envío para la identificación del mensaje después de la presentación.
  Enviado después de la inspección en carpeta de mensajes.
- Escribir archivos: leer el archivo y hasharlo.
  En inglés, el texto es traducido en inglés como "documento".
- Llamada de la API: seguimiento `GET`en el recurso objetivo.
  Traducción:API 调用:对目标资源的后续 `GET`¿Qué es eso?

Si la verificación falla, el flujo de trabajo está en un estado conocido.

> 验证失败时工作流处于已知坏状态――回滚启动――

### Planes de retroceso .

Cada acción consecuente en la propuesta-entonces-compromiso (lección 15) tiene un plan de retroceso.

> Proponer-entonces-comprometerse (§ 15 课) 中每个后果性动作带回滚计划──类型:

- **In-band rollback**: revertir directamente el efecto secundario (`DELETE`después de`INSERT`¿ Qué ?`Send-correction-email`después de enviar).
  En inglés:**带内回滚**: direct反转副作用`INSERT`后 `DELETE`、Enviar despuésEnviar más correcto correo)
- **Compensating transaction**: una nueva acción que neutraliza el original (patrón SAGA estándar).
  En inglés:**补偿事务**El proyecto de ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de los Estados Unidos.
- **Out-of-band rollback**Alerta a un humano, detiene el flujo de trabajo, deja el mal estado para la investigación.
  En inglés:**带外回滚**El informe de la Comisión de Asuntos Exteriores de la Unión Europea (UE) sobre la aplicación de la ley de la protección de los derechos humanos en el ámbito de la seguridad social y de la seguridad social (OJ L 345, 20.10.2001, p.

Las acciones sin retroceso requieren un mayor HITL en el tiempo de compromiso (lección 15 de desafío y respuesta).

> No-op 回滚("我们不能撤销此") debe ser denominado en el proyecto de ley.

### Ley de IA de la UE Artículo 14 Lectura operativa                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

El artículo 14 requiere una "supervisión humana efectiva" de los sistemas de alto riesgo.

> Se trata de un proyecto de ley que se desarrolla en el ámbito de la salud y de la salud.

- Los puntos de control son consultables por un auditor.
  En inglés, "checkpoint" es una palabra que se usa para referirse a un auditor.
- Se ensayan los rollbacks (se prueban de extremo a extremo al menos una vez).
  En inglés, "Rolling to Exercise" se traduce en "Rolling to Exercise" (Rolling to Exercise).
- El rastro de auditoría sobrevive a un despliegue (el backend del checkpoint no es efímero).
  China: 查查点后端非临时 (en inglés: 检查点后端非临时)
- Las verificaciones fallidas son alertadas, no registradas en silencio.
  El fracaso de la prueba fue notificado y no registrado en silencio.

Un flujo de trabajo que se estropee en medio del compromiso, reanude y complete el efecto secundario sin una vía de verificación + retroceso no sobrevive al ensayo del artículo 14.

> 提交中崩、恢复、无验证+回滚路程完成副作用工作流不通过第 14 条测试──

### El modo de fracaso agudo: el doble ejecutar.

El incidente de producción más común en este espacio: Acción aprobada, comienza el compromiso, devuelve 200, flujo de trabajo se estrella antes de persistir en estado, se reanuda y se re-executa.

> El caso de los accidentes de producción más comunes en este ámbito: movimiento de aprobación, presentación, devolución, 200; trabajo en estado de perpetuidad, pre-cráneo, recuperación y re-execución.

1. Acción aprobada, clave de la inmunidad k.
   En español: movimiento de la aprobación, 等键 k。
2. Compromiso comienza, ejecuta, devuelve 200.
   En inglés, el nombre de la persona que ha sido enviada para la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la policía es un año pasado.
3. El flujo de trabajo se desploma antes de que persista el estado de "compromiso".
   El trabajo se ha realizado en el estado de "ha sido presentado" pre-crash──
4. El flujo de trabajo se reanuda; ve "aprobado pero no comprometido"; se reejecuta.
   La traducción de la palabra "realización" en inglés es "realización".
5. El efecto secundario dispara dos veces.
   Se trata de un problema que se puede tratar en el cuerpo.

Mitigación: persiste una intención "en vuelo" antes de la ejecución, ejecuta con una clave de idempotencia, luego marca "compromete" solo después de que la verificación post-acción tenga éxito. Si los disparos de acción y la escritura de estado fallan, usted sabe verificar y (si es necesario) volver a disparar. Si la escritura de estado tiene éxito y la acción falla, verifica y dispara exactamente una vez a través del camino de recuperación.

> 缓解: ejecutar pre-持久化"in-flight"意图, con 等键 ejecutar, sólo en la operación después de la prueba de éxito después de la marcación "ha sido enviado"──如动作触发而状态写失败,你知道要验证(如必要) 重触发──如状态写成功而动作失败,你验证并通过恢复路径精确触发一次──

## Usalo con el marco de ejecución
```figure
checkpoint-replay
```

## Usalo

`code/main.py`El conductor simula cuatro escenarios: ejecución limpia, retiro después del accidente (captura de la idempotencia), falla de la condición previa (aborto de flujo de trabajo sin disparar), falla de verificación (incendios de retroceso).

> `code/main.py`实现带等、前置条件、验证和回滚的检查点工作流──驱动器模拟四场景:干净运行、崩后重试(等捕获)、前置条件失败(工作流停止不触发)、验证失败(回滚触发)。

## Envíe el producto .

`outputs/skill-rollback-rehearsal.md`diseña un ensayo de ensayo de retroceso para un flujo de trabajo propuesto y audita el punto de control de retroceso para determinar la persistencia de la pista de auditoría.

> `outputs/skill-rollback-rehearsal.md`Para la propuesta de trabajo de diseño de la práctica de la prueba y la auditoría de la revisión de los puntos de seguimiento de la auditoría de la última duración:

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Para el caso de accidente durante el cometido, confirme los disparos de acción exactamente una vez en los retos.
   Traducción:运行`code/main.py` Verificar cuatro escenarios.  Para el caso de un colapso en el proceso de entrega, confirmar movimiento en el proceso de entrega.

2. Modifique el patrón "marcar como hecho primero, luego hacerlo" para que el estado escriba incendios después de la acción. Repite el escenario de choque. Medir cuántas acciones duplicadas disparar.
   China: Traducción:Medios de "precedencia de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea de la tarea

3. Diseñar un plan de retroceso para una acción de producción específica (por ejemplo, "post a un canal Slack"). Clasificar como dentro de banda, compensando o fuera de banda. Justificar la elección.
   Por ejemplo, "enviar a Slack 频道") diseño de un plan de rodaje.

4. Tome un flujo de trabajo que conozca. Identifique cada transición de estado. Marque cada uno con un requisito de durabilidad (persistir / no persistir). Cuente los que actualmente no persisten.
   En el caso de los trabajadores, el trabajo de los trabajadores es un proceso de trabajo.

5. Prueba de retroceso repetida: diseñar una prueba de extremo a extremo que ejecute un flujo de trabajo real, lo estropee y confirme los incendios de la ruta de retroceso. ¿Qué afirma la prueba?
   En español, el proceso de desarrollo de la tecnología de la información es un proceso de desarrollo de la información.

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Más Leer más Leer más

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Primitivas de los puntos de control y recuperación de arrendamientos.
  En el idioma chino, el idioma se traduce en chino.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) Objetos duraderos como sustrato de estado.
  中文翻译:Objetos duraderos 作为状态基板。
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) línea de base regulatoria.
  Traducción:El gobierno de la República de China
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Enmarcamiento de fiabilidad para los flujos de trabajo de largo horizonte.
  La estructura de trabajo de la empresa es la de la empresa.
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) forma del flujo de trabajo para las rutinas de código de Claude.
  El código de la rutina de trabajo de Claude
