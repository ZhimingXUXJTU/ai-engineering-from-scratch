# Los modos de fracaso: ¿Por qué los agentes rompen ?

> MASFT (Berkeley, 2025) cataloga 14 modos de falla multi-agente en 3 categorías. La taxonomía de Microsoft documenta cómo los fallos existentes de IA se amplifican en configuraciones agenciales. Los datos del campo de la industria convergen en cinco modos recurrentes: acciones alucinadas, deslizamiento de alcance, errores en cascada, pérdida de contexto, uso indebido de herramientas.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 05 (Self-Refine and CRITIC), Phase 14 · 24 (Observability) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·05(Auto-Refinación / CRITIC)  Comprender las limitaciones del agente auto-corrección error;Fase 14·24(Observabilidad) 本节假设你已经能使用OpenTelemetry 看完整的痕迹──本节教你**识别 trace 中的失败模式**, es la fase 14·29 (Tiempos de ejecución de la producción) de la fase 14·29

> ¿ Qué es esto ?**【困惑】**P: ¿Por qué el agente  fracaso es más difícil de encontrar que el software tradicional  fracaso es más difícil de encontrar? A: Porque el agente  fracaso es "software fracaso" 代码没崩、API 没返回错误, pero el agente utiliza err errores de herramientas调用、错误参数、错误顺序"成功完成" 任务了── Tradicional prueba afirmaciones sólo pueden ver API 返回码,看不到语义错── necesita LLM-as-judge o rastrear 级别的人审才能发现──

## Objetivos de aprendizaje

- Nombre de las tres categorías de fallos de MASFT y al menos cuatro modos específicos en cada una.
- Explica por qué el fracaso agente amplifica los modos de fracaso de IA existentes (bias, alucinaciones).
- Describa los cinco modos recurrentes en la industria y sus mitigantes.
- Implemente un detector stdlib que etiqueta el agente de rastreo con etiquetas de modo de falla.

## El problema es la introducción del problema

Los equipos envían agentes que trabajan en el 90% de las huellas. Los 10% de fallas no son ruido aleatorio  caen en un pequeño número de categorías recurrentes. Una vez que se puede nombrarlos, se puede monitorear para ellos y arreglarlos.

> El equipo de agentes publicados trabaja en el 90% del seguimiento normal. El 10% de los fracasos no son ruidos al azar.


> **【中文解读】**El modelo de fracaso del agente 系统与普通软件不同: 1) 级联失败一个错误决策触发后续一系列错误; 2) 目标漂移Agent 在长链执行中偏离原始目标; 3) 过度自信Agent 在错误结果上编制成功故事――理解这些模式是构建可靠的代理的前提――

> **{【拓展：2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Ag...】}**El informe de accidentes de agentes para el período 2025-2026 revela un modelo de fracaso sistémico. Por ejemplo: 1) El agente codificador modificó documentos irrelevantes que provocaron el colapso del sistema; 2) el agente investigador comenzó a discutir los problemas filosóficos en el paso 15.

> ¿ Qué es esto ?**【类比】**Los 5 principales factores de fracaso del agente son los siguientes:**幻觉动作**=看错导航开错路;(2) **范围蔓延**=Sería que haber comprado el vino en la provincia;**级联错误**=小擦后慌乱撞墙;(4) **上下文丢失**= olvidé de dónde salió;**工具误用**=把油门当车. Todos los fracasos tienen respuesta a la defensa:导航验证,明确终点,紧急停车按,定期回顾,工具白名单.

> ️ **【易错点】**Agente 失败排查的 3 个坑:**只看最终输出**Agent 自信说"完成", pero intermedios pasos completos error;务必看完整的痕迹,不仅看结尾() 的输出──(2) **不设失败预算** El mismo error连续重试 20 次烧光预算; usando el máximo de retrasos = 3 + 失败计计器──(3) **没做意图验证**El agente decide "eliminar el archivo X", pero X es /etc/passwd; 高危操作必须用户二次确认 + 路径白名单──

## El concepto central.

### MASFT (Berkeley, arXiv:2503.13657)

Taxonomía de fallas de sistemas de múltiples agentes. 14 modos de fallas agrupados en 3 categorías.

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

El argumento central: los fallos son fallos fundamentales en el diseño de los sistemas multiagentes, no las limitaciones de la MLL que deben ser fijadas con mejores modelos básicos.

> 核心主张: el fracaso es una defectos de diseño básicos del sistema de múltiples agentes, no es un límite de LLM que puede ser revisado a través de un modelo de base mejorado.

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

### Taconomía de Microsoft del modo de falla en los sistemas de IA agenciales

- Los fallos existentes de la IA (bias, alucinaciones, filtración de datos) se amplifican en entornos agentes.
- Nuevos fracasos surgen de la autonomía: acción no deseada a escala, mal uso de herramientas, deriva de misión.
- El documento blanco es el registro de riesgos de los productos agentes.

### Caracterizando las fallas en la IA agencial (arXiv:2603.06847)

- Los fracasos surgen de la orquestación, la evolución del estado interno y la interacción del medio ambiente.
- No sólo "mal código" o "mala salida de modelo".

### Encuesta de alucinaciones de agentes de LLM (arXiv:2509.18970)

Dos manifestaciones primarias:

1. **Instruction-following Deviation**El agente no sigue la señal del sistema.
2. **Long-range Contextual Misuse** el agente olvida o aplica incorrectamente el contexto de los turnos anteriores.

Errores de subintención: omisión (paso perdido), redundancia (paso repetido), desorden (pasos fuera de orden).

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

### Los cinco modos recurrentes en la industria

Los análisis de campo de Arize, Galileo, NimbleBrain 2024-2026 convergen en:

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

1. **Hallucinated actions.**El agente invoca una herramienta que no existe o fabrica argumentos.
2. **Scope creep.**El agente expande la tarea más allá de lo que el usuario pide (crea relaciones públicas adicionales, envía correos electrónicos adicionales).
3. **Cascading errors.**Una llamada errónea desencadena efectos en el flujo posterior. Una alucinación fantasma SKU desencadena cuatro llamadas API  un incidente de múltiples sistemas.
4. **Context loss.**Las tareas de largo horizonte olvidan las restricciones de turno temprano.
5. **Tool misuse.**Llama a la herramienta correcta con argumentos equivocados, o la herramienta equivocada por completo.

Los agentes no pueden distinguir "no he podido" de "la tarea es imposible" y a menudo alucinan un mensaje de éxito en 400 errores para cerrar el bucle.

> El agente no puede distinguir entre "me fracasé" y "la tarea no se puede completar", a menudo en 400 errores se produce una sensación de éxito para cerrar el ciclo.

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

### Mitigación: puertas en cada paso

Puertas de verificación automáticas en cada paso de una cadena de razonamiento, comprobando la base de los hechos con respecto al estado ambiental.

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

- Clasificación de seguridad por paso (lección 21).
- Validación de los argumentos de llamada de herramienta (lección 06).
- Verificación de los contenidos recuperados con los hechos conocidos (lección 05, CRITA).
- Detectar alucinación de éxito mediante la revisión del estado (¿fue realmente creado el archivo?).

### Cuando el monitoreo de fallas sale mal

- **Tagging only crashes.**La mayoría de las fallas de los agentes producen una salida válida.
- **No baseline.**La detección de deriva necesita un último bien conocido; sin él no se puede decir "esto está empeorando".
- **Over-alerting.**Cada falla produce una página, un grupo y un límite de velocidad.

> **仅标记崩溃。**La mayoría de los agentes no logran producir una salida efectiva.
> **没有基线。**漂移检测 necesita un estado de buena forma conocido; sin ella no puedes decir "esto está cambiando"―
> **过度告警。**Cada fracaso produce una página.

## Construye y realiza.
```figure
failure-cascade
```

## Construye el mismo

`code/main.py`Implementa un etiquetador de modo de falla stdlib:

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

- Un conjunto de datos de rastreo sintético que cubre los cinco modos.
- Funciones del detector por modo (patrones de firma en las llamadas de la herramienta, salidas, acciones repetidas).
- Un etiquetador que etiqueta cada rastro y informa la distribución de modo.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Producción: etiquetas por rastro + distribución agregada, una reproducción barata de lo que las superficies de agrupación de rastro de Phoenix.

> 输出: cada etiqueta de seguimiento + 聚合分布,Phoenix 追踪聚类所显示内容的廉价复现──

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

## Usalo con el marco de ejecución

- **Phoenix**para el agrupamiento de derivación de producción (lección 24).
- **Langfuse**para reproducción de sesión + anotación.
- **Custom**para firmas específicas de dominio que su plataforma de observabilidad no puede detectar.

## Envíe el producto .

`outputs/skill-failure-detector.md`genera detectores de modo de falla adaptados a su dominio, conectados a una tienda de rastreo.

> `outputs/skill-failure-detector.md`Creado para detectar los errores de tu área, conecta el archivo de seguimiento.

> El modelo de éxito del agente incluye: un error de transmisión a varios grupos de personas.

## Los ejercicios.

1. Añadir un detector para "allucinación de éxito": el agente devuelve el éxito pero el estado objetivo no cambia.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Etiquetar 100 huellas reales de un producto que has construido. ¿Qué modo domina? ¿Cuál es el costo de arreglarlo?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Implementar una métrica de "radío de cascada": dada una falla en el paso N, ¿cuántos pasos aguas abajo afectó?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Lea los 14 modos de falla de MASFT, elige tres que se apliquen a su producto, escriba detectores.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Enviar un detector en un trabajo de CI: fallar la construcción si >=5% de las huellas etiquetan un modo.
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| MASFT | "Multi-agent failure taxonomy" | Berkeley 14-mode categorization |  |
| Cascading error | "Ripple failure" | One early mistake propagates through N steps |  |
| Context loss | "Forgot the constraint" | Long-horizon turn drops early-turn facts |  |
| Tool misuse | "Wrong tool / wrong args" | Valid call, wrong invocation |  |
| Success hallucination | "Faked completion" | Agent claims success on a 400; state unchanged |  |
| Scope creep | "Overreach" | Agent does more than asked |  |
| Instruction-following deviation | "Disobedience" | Ignores system prompt or user constraint |  |
| Sub-intention errors | "Plan bugs" | Omission, redundancy, disorder in plan execution |  |

## Más Leer más Leer más

- [Cemri et al., MASFT (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657) 14 modos de falla, 3 categorías
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Microsoft, Taxonomy of Failure Mode in Agentic AI Systems](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) Registro de riesgos
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Arize Phoenix](https://docs.arize.com/phoenix) Clustering de deriva en la práctica
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) cuando los patrones más simples evitan los modos por completo
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
