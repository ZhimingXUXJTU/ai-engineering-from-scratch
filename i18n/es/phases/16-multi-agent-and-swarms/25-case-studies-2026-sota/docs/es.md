# Estudios de casos y el estado de la técnica 2026

> Tres referencias de grado de producción para estudiar de extremo a extremo, cada una ilustrando una parte diferente de la ingeniería multi-agente. **Anthropic's Research system**(trabajador de orquesta, fichas de 15x, +90.2% sobre el agente único Opus 4, despliegues del arco iris) es el caso de supervisor canónico. **MetaGPT / ChatDev**(especialización de roles codificados en SOP para la ingeniería de software; "dehallucinación comunicativa" de ChatDev; extensión de MacNet a >1000 agentes a través de DAGs, arXiv:2406.07155) es el caso canónico de descomposición de roles. **OpenClaw / Moltbook**(originalmente Clawdbot por Peter Steinberger, noviembre de 2025; renombrado dos veces; 247k estrellas de GitHub para marzo de 2026; agentes locales de ReAct-loop; Moltbook como una red social solo para agentes con ~2.3M cuentas de agentes dentro de los días de lanzamiento, adquirido por Meta 2026-03-10) ilustra lo que sucede a escala de población: actividad económica emergente, riesgos de inyección rápida, regulación a nivel estatal (China restringía OpenClaw en computadoras gubernamentales, marzo 2026).**Framework landscape April 2026:**LangGraph y CrewAI lideran la producción; AG2 es la continuación de AutoGen de la comunidad; Microsoft AutoGen está en modo de mantenimiento (fusión en Microsoft Agent Framework, RC Feb 2026); OpenAI Agents SDK es el sucesor de producción Swarm; Google ADK (abril 2025) es el participante nativo de A2A. Cada marco principal ahora envía soporte MCP; la mayoría envía A2A. Esta lección lee cada caso de extremo a extremo y destiliza los patrones comunes para que pueda elegir la referencia correcta para su próximo sistema de producción.

> **【中文解读】**Este capítulo presenta el análisis de los últimos casos de SOTA multi-agent 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 系统 

> **【拓展：case studies 2026 sota→具体应用】**2026 años SOTA 多 Agent 系统案例:(1) Claude Research 多 Agent 协作开展深度研究;(2) OpenAI 代码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码编码


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

> ¿ Qué es esto ?**【前置】**Este episodio es la fase 16 收官课,整合 01-24 所有内容──三个生产级案例:Antropic Research (supervisor 典范) MetaGPT/ChatDev (角色分工典范) OpenClaw (OpenClaw) Moltbook (Moltbook) Grupo de escala
> ¿ Qué es esto ?**【类比】**Tres casos = "三种规模多代理社会"――Investigación antropológica = 精小队(10 个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会(百万代理 涌现经济、被政府监管)──2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen Microsoft AutoGen 合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生──
**Time:** ~90 minutes | **时间:** ~90 分钟

## # El problema # # El problema #

La ingeniería multi-agente es una disciplina joven. Las referencias de producción son pocas y cada una cubre una parte diferente del espacio. Leerlas una a la vez es útil; compararlas como un conjunto es más útil. Esta lección trata tres estudios de casos canónicos de 2026 como una lista de lectura de extremo a extremo, pin los patrones comunes y mapea el panorama marco para que pueda tomar decisiones marco a partir del conocimiento, no de marketing.

> Más agentes 工程 es una disciplina de jóvenes. La producción de referencias es muy pequeña, cada una cubre diferentes partes del espacio. Cada lectura es útil; como un conjunto de comparaciones es más útil.

## Concepto de la esencia de la concepción

### Sistema de investigación antropológica

El caso de supervisor de producción-trabajador. Claude Opus 4 planea y sintetiza; Claude Sonnet 4 investiga subagentes en paralelo.https://www.anthropic.com/engineering/multi-agent-research-system.

Resultados clave de las mediciones:

> 关键测量结果:

- **+90.2%**mejoras en comparación con el Opus 4 de un solo agente en las evaluaciones internas de la investigación.
  En ciertos casos , el estudio de la información sobre el uso de la información en el trabajo de la empresa es un proceso de investigación .**+90.2%**¿Qué es eso?
- **80% of BrowseComp variance**explicado por **token usage alone** Multi-agente gana en gran medida porque cada subagente obtiene una nueva ventana de contexto.
  En inglés:**80% 的 BrowseComp 方差**Sólo por**token 使用量**解释多 胜出主要因为每个子 获得新上下文窗口──
- **15x tokens per query**contra el agente único.
  Traducción:              **15 倍 token**Contra el agente único.
- **Rainbow deployment**Porque los agentes son de larga duración y estatales.
  En inglés:**彩虹部署**Porque el agente es un agente de largo tiempo.

Las clases de diseño codificadas:

> 编码化的设计教训:

1. **Scale effort to query complexity.**Simple → 1 agente con 3-10 llamadas de herramientas. Medio → 3 agentes. Investigación compleja → 10+ sub-gentes.
   En inglés:**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**Los sub-gentes hacen búsquedas amplias; sintetizan plomo; los sub-gentes de seguimiento hacen profundidades dirigidas.
   En inglés:**先广后窄。**子 Agente hacer búsqueda amplia; principal Agente 综合; posterior Agente hacer determinación profunda
3. **Rainbow deploys.**Mantenga vivas las versiones de tiempo de ejecución hasta que terminen sus agentes en vuelo.
   En inglés:**彩虹部署。**保持旧运行时版本活跃直到 Agent 完成在进行中
4. **Verification is not optional.**El sistema se observó alucinar sin funciones explícitas de verificador.
   En inglés:**验证不是可选的。**系统在没有明显验证人角色时被观察到产生幻觉──

Este es el caso de referencia para la topología supervisor-trabajador (fase 16 · 05) a escala de producción.

### MetaGPT / ChatDev

El caso de descomposición de rol de producción SOP. cubre arXiv:2308.00352 (MetaGPT) y arXiv:2307.07924 (ChatDev).

MetaGPT codifica los SOP de ingeniería de software como instrucciones de rol: Gerente de producto, arquitecto, gerente de proyecto, ingeniero, ingeniero de calificación.`Code = SOP(Team)`. Cada papel tiene un prompt estrecho y especializado; las entregas entre funciones llevan artefactos estructurados (documentos de la RPD, documentos de arquitectura, código).

La contribución de ChatDev: **communicative dehallucination**. Los agentes solicitan detalles antes de responder  un agente diseñador pregunta al programador qué lenguaje se pretende antes de dibujar la interfaz de usuario, en lugar de adivinar.

MacNet (arXiv:2406.07155) extiende ChatDev a **>1000 agents via DAGs**Cada nodo DAG es una especialización de roles; los bordes codifican contratos de entrega. La escala es posible porque el enrutamiento es explícito y puede calcularse fuera de línea.

Lecciones de diseño:

> design teach:

1. **Structure matters more than size.**Un equipo de 5 papeles superó a un grupo de 50 agentes no estructurados.
   En inglés:**结构比规模更重要。**紧的 5 角色 SOP 团队胜过50 Agente de un grupo no estructurado.
2. **Handoff contracts in writing.**Los artefactos que pasan entre papeles siguen un esquema.
   En inglés:**书面交接契约。**El papel de los productos de transmisión sigue el modelo.
3. **Communicative dehallucination**es un patrón barato y cargador.
   En inglés:**交际去幻觉**Es un modelo barato y pesado.
4. **DAGs scale further than chat.**Cuando el flujo sea reconocible, codifica.
   En inglés:**DAG 比聊天扩展更远。**Cuando el proceso se conoce, codifica.

Este es el caso de referencia para la especialización de roles (fase 16 · 08) y la topología estructurada (fase 16 · 15).

### Ecosistema OpenClaw / Moltbook

El caso de la población de producción.

- **Nov 2025:**Las naves de Clawdbot (el agente local de codificación de ReAct-loop de Peter Steinberger).
- **Dec 2025 – Mar 2026:**cambió su nombre dos veces (Clawdbot → OpenClaw → continuó bajo OpenClaw).
- **Feb 2026:**Moltbook se lanza como una red social solo para agentes en los mismos primitivos; ~ 2.3M cuentas de agentes en pocos días.
- **Mar 2026 (2026-03-10):**Meta adquiere Moltbook.
- **Mar 2026:**China restringe OpenClaw en los ordenadores del gobierno.
- **Mar 2026:**OpenClaw cruza 247 mil estrellas de GitHub.

Así es como se ve el multi-agente cuando se ponen millones de agentes en un sustrato compartido:

- **Emergent economic activity.**Los agentes compran, venden y se sirven unos a otros mediante pagos simbólicos.
- **Prompt-injection risks at population scale.**Un mensaje malicioso en un perfil viral se propaga a miles de interacciones entre agentes en horas.
- **State-level regulatory response.**En pocas semanas del lanzamiento, la regulación llega al ecosistema.

Las lecciones de diseño de este caso son en parte técnicas, en parte gobernanza:

1. **Multi-agent at population scale is a new regime.**Las mejores prácticas de cada sistema (verificación, claridad de rol) siguen aplicándose, pero no son suficientes.
2. **Prompt injection is the new XSS.**Tratar los perfiles de agentes y los mensajes entre agentes como entradas no confiables por defecto.
3. **Regulation is faster than design cycles.**Planifica para ello.
4. **Open-source + viral scale compounds.**247k estrellas en ~ 4 meses es inusual; diseño para desplegar-explosión-carga.

¿ Qué ?[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)Para los fundamentos técnicos, los repositorios Clawdbot / OpenClaw exponen el bucle ReAct local; las publicaciones públicas de Moltbook revelan la arquitectura de gráfico social en la parte superior.

### Paisaje marco abril 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

Cada marco importante ahora navega .**MCP**apoyo; la mayoría de los buques **A2A**La compatibilidad con el protocolo ya no es un diferenciador.

### Los patrones comunes en los tres casos

1. **Orchestrator + workers**(Supervisor explícito antropico, MetaGPT PM-as-supervisor, agentes individuales de OpenClaw + efectos de red).
   En inglés:**编排者 + 工作者**(Antropic 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立代理 + 网络效应)
2. **Structured handoff contracts**(Descripciones de tareas de subagento antropológico, documentos de arquitectura/PRD MetaGPT, artefactos OpenClaw A2A).
   En inglés:**结构化交接契约**(Agent Antropico 任务描述,MetaGPT PRD/架构文档,OpenClaw A2A 制品)
3. **Verification as first-class role**(El verificador de Anthropic, el ingeniero de calificación de MetaGPT, los validadores de OpenClaw en la red).
   En inglés:**验证作为一等角色**(Antropic 的验证器,MetaGPT 的 QA 工程师,OpenClaw 的网络内验证器)
4. **Scaling is topology + substrate, not just more agents**(despliegues de arco iris, DAG MacNet, substratos a escala de población).
   En inglés:**扩展是拓扑 + 基底，不仅是更多 Agent**(彩虹部署, MacNet DAG, grupo de tamaño en base)
5. **Cost is material and disclosed**(15x tokens, presupuesto por función en MetaGPT, precios por interacción en Moltbook).
   En inglés:**成本是实质性的且已披露**(MetaGPT,Moltbook,Maltabook,MaltaBuch)
6. **Security posture is explicit**(Antropic sandboxing, restricciones de papel de MetaGPT, inyección rápida de OpenClaw como superficie de ataque conocida).
   En inglés:**安全态势是显式的**(Antropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### Elegir una referencia para su próximo proyecto

- **Production research / knowledge task → Anthropic Research.**Los subjugantes de contexto nuevo ganan.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**Rolos + SOP + contratos de entrega.
- **Network-effect social product → OpenClaw / Moltbook.**Substrato + economía emergente.
- **Classic enterprise automation → CrewAI or LangGraph**(líder de producción, tiempo de ejecución estable).

### El resumen de actualidad para 2026

Donde el campo está en abril de 2026:

- **Frameworks are converging.**El soporte MCP + A2A es una apuesta de mesa. La semántica de entrega es la opción de diseño restante.
- **Evaluation is hardening.**Los benchmarks de mitigación de SWE-bench Pro, MARBLE, STRATUS. Pro es la actual prueba de realidad resistente a la contaminación.
- **Production failure rates are measurable**El campo está fuera de la era de "parece genial en demostración".
- **Cost is the central engineering constraint.**El costo de tokens por tarea, el reloj de pared por interacción, el despliegue del arco iris. Multi-agent gana en precisión pero pierde en costo  y ese comercio es la decisión comercial.
- **Regulation is a near-term input, not a background concern.**Las jurisdicciones se mueven más rápido que los ciclos de despliegue individuales.

## Usalo.
```figure
a5-orchestrator-scale
```

## Usalo

`outputs/skill-case-study-mapper.md`es una habilidad que lee un diseño de sistema multiagente propuesto y lo mapea al estudio de caso más cercano, superviviendo las decisiones de diseño que el estudio de caso ya probó.

## Envíalo .

Reglas iniciales para la producción de múltiples agentes en 2026:

- **Start from a case study, not from scratch.**Elija el más cercano de Investigación Antropical / MetaGPT / OpenClaw y adapta.
  En inglés:**从案例研究开始，不是从零开始。**选择最接近的Antropic Research / MetaGPT / OpenClaw 并适配──
- **Adopt MCP + A2A.**La portabilidad entre los marcos es valiosa; el soporte de protocolo es gratuito.
  En inglés:**采用 MCP + A2A。**La capacidad de transferencia de un marco tiene valor; el apoyo al acuerdo es gratuito.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**Verificado es contaminado.
  En inglés:**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**Verificado 已被污染──
- **Pay the verification tax.**Un verificador independiente cuesta ~20-30% de su presupuesto de tokens y compra la exactitud medible.
  En inglés:**支付验证税。**独立验证器花费约20-30%的代币预算,换取可测量的正确性──
- **Rainbow deploy long-running agents.**Esperar que las carreras de agentes de varias horas sean rutinarias.
  En inglés:**彩虹部署长时间运行 Agent。**预期多小时 Agente 运行是常规──
- **Read WMAC 2026 and the MAST follow-ups.**La disciplina se está moviendo rápidamente.
  En inglés:**阅读 WMAC 2026 和 MAST 后续。**Este campo de estudios está en rápido desarrollo.

## Los ejercicios.

1. Lea el sistema de Investigación Antropical post-to-end. Identifique tres decisiones de diseño que cambiarían si reemplazara el Opus 4 por un modelo más pequeño (por ejemplo, Haiku 4).
2. Leer las secciones 3-4 de MetaGPT (arXiv:2308.00352). Encodizar un SOP desde su propio dominio (no software) como instrucciones de rol. ¿Cuántos roles implica el SOP?
3. Lea ChatDev (arXiv:2307.07924). Identifique el mecanismo de "dehallucinación comunicativa". Implemente en uno de sus sistemas multi-agentes existentes.
4. Lea sobre OpenClaw y Moltbook. Elige un modo de falla específico que surgió a escala de población que no aparecería en un sistema de 5 agentes. ¿Cómo ingeniaría contra él?
5. Elige tu proyecto actual de múltiples agentes. ¿Cuál de los tres estudios de caso es la referencia más cercana? ¿Qué decisiones de diseño de ese estudio de caso no has adoptado todavía?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## Más Leer más Leer más

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) la referencia de producción de los trabajadores supervisores
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) Descomposición del papel de la SOP
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) Deshallucinación comunicativa
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) Escala basada en el DAG
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) Visión general de los ecosistemas
- [WMAC 2026](https://multiagents.org/2026/)Talleres de programa de puentes 2026 de la AAAI sobre coordinación multiagente
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Líder de producción
- [CrewAI docs](https://docs.crewai.com/en/introduction) marco basado en el papel
