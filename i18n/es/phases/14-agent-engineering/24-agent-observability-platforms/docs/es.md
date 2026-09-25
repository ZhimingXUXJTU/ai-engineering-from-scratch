# Agente observabilidad: Langfuse, Phoenix, Opik.

> Las plataformas de observabilidad de agentes de código abierto dominan el 2026. Langfuse (MIT)  6M+ instalaciones/mes, rastreo + gestión de prompto + evaluaciones + repetición de sesión. Arize Phoenix (Elastic 2.0)  evaluaciones específicas de agentes profundas, relevancia RAG, auto-instrumentación OpenInference. Cometa Opik (Apache 2.0)  optimización automática de prompto, guardrails, detección de alucinaciones del juez LLM.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 23 (OTel GenAI) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Nombre de las tres principales plataformas de observabilidad de agentes de código abierto y sus licencias.
- Distingue en qué es más fuerte cada uno: Langfuse (sesiones de mgmt + inmediato), Phoenix (RAG + auto-instrumentamiento), Opik (optimización + barandillas).
- Explica por qué el 89% de las organizaciones informa tener observabilidad de agentes en vigor para 2026.
- Implementar una línea de trayectoria de la tabla de control con evaluación del juez de la LLM.

## El problema es la introducción del problema

OTel GenAI (Lección 23) le da el esquema. Todavía necesita la plataforma que ingere los intervalos, ejecuta evaluaciones, almacena versiones rápidas y superviene regresiones.

> OTel GenAI (n.o 23) te ha dado un esquema. Aún necesitas una plataforma para recibir el lapso de ejecución, evaluación, almacenamiento y muestra el regreso.

> ¿ Qué es esto ?**【前置】**學本節前 請先掌握:Fase 14·23                                                                                                                                                                                                                                                       `invoke_agent`En el transcurso de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la duración de la de la duración de la duración de la duración de la duración de la


> **【中文解读】**La plataforma de observación de los agentes ofrece a los agentes la capacidad de observación de los usuarios desde el final de la respuesta hasta el final de la solicitud.

## El concepto central.

### El proyecto de investigación

> ¿ Qué es esto ?**【类比】**Tres plataformas de observación como las tres partes del sistema de información de los hospitales:**Langfuse**Es un hospital de la actualidad, que se encuentra en una zona de emergencia, donde se puede encontrar una solución para el problema de la enfermedad.**Phoenix**Es un centro de inspección especializado en RAG, que puede indicarte que el comportamiento del agente y el comportamiento del agente no han cambiado, pero no importa qué sugerencia cambies.**Opik**Es un sistema de gestión de ensayos clínicos (WEB que se puede realizar a la vez en el mismo tiempo.

- 6M+ SDK instalaciones / mes, 19k+ GitHub estrellas.
- Características: seguimiento, gestión rápida con versiones + playground, evaluaciones (LLM-as-judge, comentarios de los usuarios, personalizado), repeticiones de sesión.
- junio 2025: módulos anteriormente comerciales (LLM-as-a-judge, colas de anotaciones, experimentos rápidos, Playground) de código abierto bajo el MIT.
- Más fuerte para: observabilidad de extremo a extremo con un circuito de gestión rápida apretado.

### Arize Phoenix (licencia elástica 2.0)

- Evaluación más profunda específica de los agentes: agrupamiento de rastros, detección de anomalías, relevancia de la recuperación para el RAG.
- Autonoma instrumentación de OpenInference nativo.
- Parejas con Arize AX gestionado para producción.
- No se ha producido una versión rápida  posicionada como herramienta de deriva/regresor de comportamiento junto a plataformas más amplias.
- Lo más fuerte para: relevancia RAG, deriva de comportamiento, detección de anomalías.

### Cometa Opik (Apache 2.0)

- Optimización automática de la rapidez a través de experimentos A/B.
- Barrancas de seguridad (reducción de PII, restricciones tópicas).
- El juez LLM detecta alucinaciones.
- Indicador de referencia de la propia medición de Comet: los registros de Opik + evaluaciones en 23.44s vs. Langfuse 327.15s (~14x gap)  toman los indicadores de referencia del proveedor como direccionales.
- Lo más fuerte para: bucle de optimización, experimentación automatizada, aplicación de barandillas.

### Datos de la industria

Por Maxim (2026 análisis de campo): el 89% de las organizaciones tienen observabilidad de agentes en su lugar; los problemas de calidad son la principal barrera de producción (32% de los encuestados los citan).

> La plataforma de agentes observables ofrece herramientas de seguimiento y control de indicadores y de regulación de funcionamiento.

### Escogiendo uno

| Need | Pick |
|------|------|
| All-in-one with prompt management | Langfuse |
| Deep RAG evaluation + drift | Phoenix |
| Automated optimization + guardrails | Opik |
| Open licensing, no ELv2 | Langfuse (MIT) or Opik (Apache 2.0) |
| Datadog / New Relic integration | Any — they all export OTel |

### Cuando este patrón va mal

> ¿ Qué es esto ?**【困惑】**P: El 89% de las organizaciones dicen que tienen un agente observable, pero ¿por qué el accidente está todavía? A: La mayoría de los equipos sólo hicieron "entrar en OTel → rastrear entrar en Langfuse" este paso, es como instalar una cámara de vigilancia pero nadie lo ve.

- **No eval strategy.**El rastreo sin evaluación es sólo una extracción costosa.
- **Self-rolled LLM-judge without grounding.**Se aplica el patrón CRITICO (lección 05)  los jueces necesitan herramientas externas para la verificación de los hechos.
- **Prompt versions not tied to traces.**Cuando el prodo regresa, no se puede dividir a la señal que lo causó.

> **没有评估策略。**No hay un rastro de evaluación, sólo un costoso diario.
> **自建的 LLM 评审器没有基础。**Critico 模式 (第 5 课) Aplicación 评审器 necesita herramientas externas para realizar la fact核查──
> **提示版本未与追踪关联。**Cuando la producción regresa, no puedes posicionar el problema que causa.

## Construye y realiza.

> ️ **【易错点】**场景: el equipo trazó OTel trace 接到Langfuse 后, escribió un jurado de LLM 给每条 trace 打 1-5分, pero la rubrica sólo tiene una frase "respondiendo bien mal" → 后果:分数毫无意义, juzgar Colocar" cortesía pero respondiendo mal"打 5分"",correcto pero breve"打 2分,dashboard 上 95% 满意度但客户投诉暴 → 修复: rubrica 必须分维维度((factual correctness、scope adherence、tone), por cada dimensión de la operación fracaso definición (((就是"scope adherence: agent has no ha hecho las necesidades del usuario"), y además de 50-100 条条标人工做基线 准为何强调"Phoenix" , enfatizando que el juez "Opik" tiene su propio corpus de referencia.
```figure
wb-trace-ingest
```

## Construye el mismo

`code/main.py`Implementa un colector de huellas de la stdlib + evaluador de jueces de LLM:

> La plataforma de agentes observables ofrece herramientas de seguimiento y control de indicadores y de regulación de funcionamiento.

- Ingerir las espinas en forma de GenAI.
- Grupo por sesión, etiqueta de ejecuciones fallidas (viajes de vigilancia, evaluaciones de baja confianza).
- Un juez de LLM con guión que califica las respuestas de los agentes en una rúbrica.
- Un resumen similar al tablero de instrumentos: tasa de fallas, principales razones de fallas, distribución de puntuaciones de evaluación.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: puntuaciones de evaluación por sesión y clasificación de fallos que coinciden con lo que mostraría Langfuse/Phoenix/Opik.

> 输出: por sesión de evaluación y por defecto, corresponde Langfuse/Phoenix/Opik

> La plataforma de agentes observables ofrece herramientas de seguimiento y control de indicadores y de regulación de funcionamiento.

## Usalo con el marco de ejecución

- **Langfuse**auto-hosted o en la nube; cable a través de OTel o su SDK.
- **Arize Phoenix**auto-aliñado; auto-instrumento OpenInference.
- **Comet Opik**auto-hosted o en la nube; bucle de optimización automatizado.
- **Datadog LLM Observability**para equipos de operaciones mixtas + ML que ya ejecutan Datadog.

## Envíe el producto .

`outputs/skill-obs-platform-wiring.md`elige una plataforma y traza + evalua + versiones de respuesta en un agente existente.

> `outputs/skill-obs-platform-wiring.md`选择一个平台,并将追踪 + 评估 + 提示版本接入现有代理──

> La plataforma de agentes observables ofrece herramientas de seguimiento y control de indicadores y de regulación de funcionamiento.

## Los ejercicios.

1. Exportar una semana de trazas de OTel a la nube Langfuse. ¿Qué sesiones fallaron?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Escriba una rúbrica de juez de LLM para su dominio (corrección de hechos, tono, cumplimiento del alcance).
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Comparar la versión de Langfuse con la de Phoenix, ¿qué te dice qué se rompió más rápido?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Lea los documentos de la barrera de Opik, entregue una barrera de redacción de PII a uno de sus agentes.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Revisa los tres en tu corpus, ignora los números publicados por el vendedor, mide los tuyos.
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Tracing | "Spans collector" | Ingest OTel / SDK spans; index by session |  |
| Prompt management | "Prompt CMS" | Versioned prompts tied to traces |  |
| LLM-as-judge | "Automated eval" | Separate LLM scores agent output against a rubric |  |
| Session replay | "Trace playback" | Step through past runs for debugging |  |
| RAG relevancy | "Retrieval quality" | Does the retrieved context match the query |  |
| Trace clustering | "Behavioral grouping" | Cluster similar runs for drift detection |  |
| Guardrail enforcement | "Policy at log time" | PII/toxicity/scope checks on logged content |  |

## Más Leer más Leer más

- [Langfuse docs](https://langfuse.com/) rastreo, evaluaciones, seguimiento de la información
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Arize Phoenix docs](https://docs.arize.com/phoenix) Auto-instrumentamiento, derivación
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Comet Opik](https://www.comet.com/site/products/opik/) optimización + barandillas
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) el esquema los tres consumen
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
