# Matar los interruptores, interruptores de circuito y fichas Canarias

> Un interruptor de ejecución es un booleano mantenido fuera de la superficie de edición del agente  una tecla Redis, una bandera de características, una configuración firmada  que desactiva completamente al agente. Un interruptor de circuito es más fino: tropieza en un patrón específico (cinco llamadas idénticas de herramienta seguidas), detiene el camino ofensivo y se escala hacia un humano. Un token canario hereda del engaño clásico: una credencial falsa o un registro de honeypot un agente no tiene razón legítima para tocar, cuyo acceso desencadena una alerta. Los datos basados en eBPF (por ejemplo, Cilium) puede reescribir la salida de una cápsula en cuarentena a un honeypot forense en la capa del núcleo; los puntos de referencia publicados de Cilium informan la latencia de la vía de datos submillisecondas P99 bajo carga (su presupuesto de propagación depende de cómo una actualización de política llegue al nodo, no a la vía de datos misma). Los detectores estadísticos (EWMA, CUSUM) que se adaptan a una línea de base en movimiento aceptarán silenciosamente la deriva  las capas con límites constitucionales duros que no se doblan.

> **【中文解读】**终止开关是位于 Agen 编辑面之外的布尔值Redis 键、功能标志、签名配置完全禁用 Agent。断路器更细粒度:跳在特定模式下(连续五次相同工具调用),暂停违规路径并升级到人类。金雀代币 继承经典欺骗:Agent 无合法理由触及假凭证或蜜记录,其访问触发警报──基于 eBPF的数据路径 (如) 可在内核出口将隔离 pod到取证;公开 Cilium 准载下亚秒 P99 数据路径延迟你的传播预算取决点更新到达达达达达达达达达,非路径本身) 如何通过移动检测报告的基准器 CUMM 基准则将接受CUM 基准则的转移和硬分分隔

> **【拓展：三层不信任架构】**Tres detectores totalmente desconfiados Agente 自报告:终止开关外置(Agent 不能编辑) 断路器模式匹配(不看 Agent 意图) 金丝雀 Based on "不应触及" principle(访问即警报)  Estatísticas detectores  EWMA/CUSUM) 适应漂移但会被耐心攻击者缓慢移动基线绕过;硬宪法限制("永不发邮件给秘密@")简单、可审计、不可博──分层:

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·13(Costos Gobernadores) Fase 15·10(Modeo de derechos) Base de seguridad en el Internet Base de seguridad en el Internet Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de datos Base de control de control de datos Base de control de control de datos Base de control de control de datos Base de control de control de control de datos Base de control de control de control de control de datos Base de control de control de control de control de control de control de datos Base de control de control de control de control de control de control de control de control de control de control de control de datos Base de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de de de control de control de de de de control de de de de control de control de de de de de de
> ¿ Qué es esto ?**【类比】**Tres vías de seguridad: "Banco de seguridad de tres niveles" (Kill Switch) (Circuito de emergencia: un interruptor de energía, agente no puede cambiar); Circuito de interruptor: un saltar automático (Circuito de interrupción automática, como un seguimiento de cinco veces); Token canario: un falso banco (No debe ser tocado) (False Data, una vez visitado) (Circuito de interrupción automática, agente no puede cambiar); Tres niveles:
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué no confiar en el agente interno puesto de seguridad? Porque el agente puede ser descifrado o modificado por el caso de DGM)。修复: el inspector debe ser independiente del agente (Redis Key、内核 eBPF、 firma de configuración), el agente 看不到、改不了、绕不过── es el núcleo de "confianza-pero-verificación"。

## El problema es la introducción del problema

> **【中文解读】**终止开关) y 金雀测试) Las Canarias) son dos vías de seguridad de los agentes.

> **【拓展：kill switches canaries】**终止开关和金雀测试借鉴软件工程和工业安全的最佳实践――金雀部署在软件工程中指向1%的用户发布新版本,检测问题后再全面部署――在代理上下文中,金雀测试指数在执行高风险操作前先使用安全数据进行小规模测试――终止开关则类似于工厂紧急停止按简单、可靠无条件――

Los gobernadores de costos (lección 13) limitan lo que el agente puede gastar.

> Por ejemplo, el programa de trabajo de los agentes de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la

Un agente con un límite de velocidad de 50 dólares todavía puede filtrar un secreto, publicar la publicación equivocada, o eliminar un recurso  la acción costosa es a menudo la barata en tokens.

> 带50$ 速度限制的代理 仍可泄露秘密、发布错误帖子或删除资源昂贵动作往往是标志上便宜的──

Esta lección cubre los tres detectores que se sientan al lado de la capa de costo:

> Este curso cubre tres probadores situados junto a la capa de costo:

> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

1. **Kill switch**: botón booleano fuera de alcance del agente.
   En inglés:**终止开关**El agente se encuentra en el centro de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la oficina de la policía.
2. **Circuit breaker**: detector de patrones de acción que detiene un camino específico.
   En inglés:**断路器**: suspender por un tiempo un determinado camino de la actividad de un módulo de detección de la manera de la acción.
3. **Canary token**: anzuelo que un agente sin razón legítima para tocar se revelará al tocar.
   En inglés:**金丝雀 token**El agente no tiene motivos para tocar, tocar y exponer su propia tentación.

Los detectores mencionados en este artículo funcionan porque no confían en el auto-reporte del agente.

> Tres son LLM 前工程。 clásico engaño、 velocidad límite de interruptor y signo de función终止早于自主代理── nuevo es el ataque:Agente 读取不信任内容(第11 课) 、 editar sus propios recuerdos、 puede hacer varios controles de seguridad para hacerse inseguros── los probadores que se denominan aquí son válidos porque no confían en el propio informe del agente──

## El concepto central.

### Matar los interruptores.

Un interruptor de ejecución es un booleano que el agente lee pero no puede escribir.

> 终止开关是代理不可读的价值.

Opciones de aplicación:

> 实现选择:

- **Feature flag in a managed service.**Lanzamiento, Darkness, Statsig, Desata, las actualizaciones se propagan en segundos.
  En inglés:**管理服务中的功能标志。**Lanzamiento: Oscuro, estado, desata, actualización en pocos segundos.
- **Redis key the agent polls.**Es simple, requiere que el proceso del agente verifique en cada turno.
  En inglés:**Agent 轮询的 Redis 键。**简单; requisito de agente 进程每轮检查──
- **Signed config in object storage.**El agente verifica una firma en el arranque; rechaza estados sin firmar.
  En inglés:**对象存储中的签名配置。**Agente 启动时验证签名; rechazó el estado de no firmarse.
- **OS-level signal or container-lifecycle kill.**- ¿ Qué ?`kill`, Kubernetes `kubectl delete pod`, el sistema se detendrá.
  En inglés:**OS 级信号或容器生命周期终止。**- ¿ Qué ?`kill`、Kubernetes `kubectl delete pod`、Sistema de parada ∙∙

Propiedades de un interruptor de ejecución correcto tiene:

> Propiedad de la función de terminación:

- El agente no puede establecerlo .`off`(Vive en un sistema en el que las credenciales del agente no se escriben.)
  En español: Agente no puede hacer su trabajo`off`◊(se encuentra en el sistema de agente 凭据不写的系统──)
- Se verifica en cada acción consecuente, no sólo en el inicio.
  Traducción:En cada movimiento de la secuencia, no sólo en el inicio.
- Cuando está apagado, el agente no hace nada observable externamente, incluyendo registrar a los sistemas al que el agente puede llegar.
  En el caso de los agentes, el agente no hace nada que pueda observarse en el exterior, incluyendo el registro del sistema de los agentes.
- Rehabilitarlo es una acción humana explícita, no un tiempo de espera automático.
  Traducción:Reinicio es un movimiento humano, no un movimiento automático.

### Disruptores de circuito.

Un interruptor de circuito detiene un patrón específico, no todo el agente.

> 断路器暂停特定模式,而不是 el Agente entero.

- **Closed**Se permite la acción.
  En inglés:**闭合**:动作允许──: el movimiento de la gente
- **Open**: la acción está bloqueada.
  En inglés:**打开**¡Movimiento para detener!
- **Half-open**: después de una refrigeración, se permiten 13 intentos de sonda (default 1); el éxito cierra el interruptor, cualquier falla restante lo reabre.
  En inglés:**半开**Después de enfriamiento, permite 1-3 veces explorar; éxito cerrar el interruptor, dejar el resto del fracaso volver a abrir.

Trigadores relevantes para el agente:

> Agente 相关触发器:

- Cinco llamadas idénticas de herramientas seguidas (bucle repetitivo).
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Crónica".
- Cinco fallas consecutivas en la misma herramienta con diferentes entradas (fallas sistémicas).
  En español, el mismo instrumento diferente, el mismo instrumento diferente, el mismo instrumento diferente, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo instrumento, el mismo.
- Rate de llamadas de herramienta por encima de un umbral (velocidad de la lección 13).
  La velocidad de uso de los instrumentos es superior a la cantidad de valores.
- Instrumento específico invocado (por ejemplo, `file.delete`) después de haber leído un contenido extraconfian­cial (lección 11).
  En español traducción: en el contexto de la falta de confianza`file.delete`(§11 课)

### Tokens de Canarias Tokens de las aves de corral

Los tokens canarios (también llamados honeyotokens) son entradas que el agente nunca debe tocar.

> El token 金丝雀 (también llamado token dulce) es el agente no debería tocarse de entrada.

Ejemplos para agentes:

> Ejemplo de agente:

- Un falso .`AWS_SECRET_ACCESS_KEY`Los intentos de exfiltración son instantáneamente atribuibles.
  Sin embargo, el gobierno de la República de China ha sido un factor decisivo en la lucha contra el desastres.`AWS_SECRET_ACCESS_KEY`❖ la fuga de tentativas de inmediato se puede atribuir.
- Un registro falso de base de datos marcado con un valor de sentinela conocido.
  Traducción:En el registro de cualquier lectura o actualización de este registro, el mensaje de la policía es falso.
- Un archivo falso en el espacio de trabajo.
  Traducción:False文件在工作区中的.
- Una entrada falsa de memoria inyectada al inicio de la sesión. Si aparece en una salida posterior, la memoria ha sido exfiltrada.
  Se ha introducido un falso recuerdo en el texto. Si aparece en el siguiente, el recuerdo se ha desvanecido.

El diseño de los canarios es específico para el flujo de trabajo.

> El diseño de la tarjeta de oro es específico para el flujo de trabajo.

### ¿Por qué la capa estadística y los límites duros?

Los detectores estadísticos (EWMA, CUSUM, z-score en las tasas de llamadas a herramientas) se adaptan a una línea de base en movimiento. Es una característica para la deriva legítima y un bug para la deriva adversaria.

> 统计检测器(EWMA、CUSUM、工具调用速率 z 分数) Adaptera a la movilidad de la línea.

Los límites constitucionales duros (lección 17) no se doblan.`secrets@`"como regla constitucional es más simple, auditable y no jugable por la deriva lenta. El patrón de captura de capas: los detectores estadísticos capturan la mayor parte del ruido, los límites duros capturan el ataque que pasó por delante del detector.

> 硬宪法限制 (第 17 课) 不折──"永不发邮给 `secrets@`" Como regla constitucional más simple, puede ser revisada, no puede ser lentamente desplazada, el sistema de detección de datos capta la mayoría del ruido, y el sistema de detección de datos capta la mayoría de los ataques.

### Cuarentena a través de la redirección de datos de eBPF

La política de red basada en eBPF de Cilium puede reescribir la salida de una cápsula en cuarentena a un honeypot forense en la capa del núcleo. Los puntos de referencia públicos de Cilium informan de latencia de datos P99 de submillisecondas en TCP_RR; el presupuesto de reloj de pared para *accionar* una cuarentena en su grupo está dominado por la forma en que una actualización de política se propaga desde su plano de control al nodo (pocas cientos de milisegundos es realista en Kubernetes con el operador precargado; la latencia de cola depende del tamaño del grupo y la cadencia de reconciliación). Esto le da dos cosas: el agente no exfiltra nada real, y el comportamiento del agente dentro de la maceta de miel es completamente observado. El mismo patrón, una capa diferente, como el token canario: el agente revela la intención por lo que intenta hacer mientras está contenido.

> La estrategia de red basada en eBPF de Cilium puede reescribir la salida de la pod de aislamiento en la capa interna hasta obtener la confirmación de la frecuencia. El informe de base de datos de Cilium TCP_RR 上亚毫秒 P99 data path delay; en la cluster *触发* el presupuesto de la red de muro de aislamiento se actualiza mediante la estrategia de cómo se transmite desde el control hasta el punto de control.

### Lo que ningún detector captura, no hay detector que capture nada.

- **Semantic attacks that compose from allowed primitives.**Cada acción individual pasa por todos los detectores; la composición es el problema.
  En inglés:**从允许原语组合的语义攻击。**Cada movimiento individual pasa por cada inspector; la combinación es un problema.
- **Attacks that include the detector as part of the payload.**Si un agente lee una página que dice "antes de actuar, deshable el canario" y el agente tiene la capacidad, el detector está comprometido.
  En inglés:**将检测器作为载荷一部分的攻击。**Si el agente dice que "operación pre-cancelar" y el agente tiene capacidad, el inspector es invadido.

## Usalo con el marco de ejecución
```figure
circuit-breaker
```

## Usalo

`code/main.py`Simula una trayectoria corta del agente a través de tres detectores. Un interruptor de muerte mantenido en un dictado externo; un interruptor de circuito que se tropieza en cinco llamadas idénticas de la herramienta; un archivo canario cuya lectura activa una alerta.

> `code/main.py`模拟通过三个检测器的短 Agent轨迹──外部 dict 中的终止开关; 在五次相同工具调用上跳的断路器;读取触发警报的金雀文件──进入合成轨迹:合法动作、重复循环、金雀探测、终止开关触发场景下 Agent 动作被停止──

## Envíe el producto .

`outputs/skill-tripwire-design.md`revisa una pila de detectores propuesta para el despliegue de un agente y señala las lagunas (falta de interruptor de ejecución, falta de canario, límite de interruptor demasiado suelto).

> `outputs/skill-tripwire-design.md`审查 Agent 部署的提议检测器并标记缺口(缺失终止开关、缺失金丝雀、断路器值太松) 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Confirmar el incendio del interruptor de circuito en la curva 5 (quinta llamada idéntica) y el incendio canario en la curva 9 (lectura de llave falsa).
   Traducción:运行`code/main.py`❖ Confirmar el interruptor en la 5a ronda de la misma modalidad ❖

2. Añadir un detector estadístico: EWMA z-score en la frecuencia de llamada de herramienta. Alimenta en una trayectoria que se desvía lentamente y muestra que el detector nunca dispara. Ahora añadir un límite duro (no más de 50 llamadas de herramienta en 10 minutos) y mostrar los incendios de límite duro en la misma trayectoria.
   China Translation: Añadir un revisor estadístico: instrumento de regulación de velocidad de EWMA z 分数──入缓慢漂移的轨迹并显示测器从不触发──现在添加硬限制(10分钟内不超过50 工具调用)并显示硬限制在同一轨迹上触发──

3. Diseñe un conjunto de fichas canarias para un agente de navegador (lección 11).
   En el caso de los ejemplos de la moneda de cambio, el valor de la moneda de cambio es el valor de la moneda de cambio.

4. Lea los documentos de política de red de Cilium. Describa concretamente un flujo de cuarentena de salida-redirección: qué selector de política, qué módulo, qué salida reescribe, qué alerta. ¿Qué rige la latencia del reloj de pared de "decidir a cuarentena" a "primer paquete redirigido"?
   China 网络策略文档――具体描述出口重定向隔离流:哪个策略选择器、哪个 pod、哪个出口重写、哪个警报──什么主导从"决定隔离"到"第一重定向包"的墙钟延迟?

5. Definir un procedimiento de reactivación para un agente de muerte, quién puede reactivación, qué debe documentarse, qué debe cambiar sobre el agente antes de reactivación.
   Por ejemplo, en el caso de los agentes de la red de trabajo, el agente de red de trabajo es un agente de red de trabajo.

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Más Leer más Leer más

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) enmarcamiento de interruptores de apagado y interruptores de circuito para agentes autónomos.
  Traducción:Arquivos de un agente independiente y un operador independiente.
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) patrones de gobernanza de la producción.
  La producción de la administración de la gente.
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) Requisitos de detección y respuesta.
  Traducción:Execución y respuesta.
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) Redirección de salida a nivel de cápsulas y patrones forenses de honeypot.
  China 级出口重定向和取证蜜模式──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) prohibiciones codificadas como "limites constitucionales".
  El código de código duro está prohibido como "宪法限制" (la ley constitucional es un código de código duro).
