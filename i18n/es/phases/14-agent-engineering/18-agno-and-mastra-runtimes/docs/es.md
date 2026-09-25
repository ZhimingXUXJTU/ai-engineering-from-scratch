# Agno y Mastra: Tiempo de ejecución de la producción
# Tiempos de ejecución de los agentes de producción  Instalación rápida y flujos de trabajo tipografizados

> Un agente de producción optimiza el tiempo de ejecución de lo que los marcos de prototipos ignoran: el costo de instanciación, las superficies de flujo de trabajo tipografadas y un backend listo para la entrega. El emparejamiento de 2026: Agno (Python) tiene como objetivo la instanciación de agente de microsecondas y los backends FastAPI sin estado. Mastra envía agentes, herramientas, flujos de trabajo, enrutamiento de modelo unificado y almacenamiento compuesto en el sustrato de Vercel AI SDK.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Identifique los objetivos de rendimiento de Agno y cuándo importan.
- Nombre de los tres primitivos de Mastra  Agentes, Herramientas, Flujos de Trabajo  y los adaptadores de servidor compatibles.
- Explica por qué un backend FastAPI sin estado y con escala de sesión es la vía de producción Agno recomendada.
- Seleccione Agno vs Mastra para una pila dada (Python-primero vs TypeScript-primero).

## El problema es la introducción del problema

LangGraph, AutoGen, CrewAI son un sistema de trabajo muy pesado. Los equipos que quieren "solo el bucle de agente, rápido, en mi tiempo de ejecución" pueden llegar a Agno (Python) o Mastra (TypeScript). Ambos intercambian algunos de los primitivos de propiedad del sistema por velocidad bruta y un ajuste más ajustado a la pila circundante.

> LangGraph、AutoGen、CrewAI fueron un marco de trabajo muy pesado. Querían "cuando el agente de ciclo, rápido, en mi tiempo de funcionamiento" el equipo elegiría Agno (Python) o Mastra (TypeScript).


> **【中文解读】**Agno 和 Mastra  representa dos tipos de Agente de 2026 años 运行时设计哲学。Agno(原 PhiData) buscan极简 con el menor número de códigos para construir Agente。Mastra(TypeScript) buscan todas las funciones proporcionar un Agente completo 生命周期管理。 la elección depende de la técnica y la complejidad de la demanda del equipo。

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}**Agno (GitHub 15k+ estrellas) 和 Mastra es el nuevo programa de 2026 años de Agencia 运行时的新秀。Agno filosofía es 'Agent 即函数' Cada agente es una función diferente con un conjunto de herramientas。Mastra 基于TypeScript,面向全开发者,提供完整的代理 生命周期管理(部署、监控、扩展)。 ambos apoyan múltiples modelos posterior y MCP 集成。

> ¿ Qué es esto ?**【前置】**必须先掌握:Phase 14·01(Agent Loop) yPhase 14·13(LangGraph) 本节是这两者"轻量替代品"── Si no sabes por qué "轻量化" (LangGraph),说明你还没在生产中遇到LangGraph的工程负担,建议先使用LangGraph 几周再回头看本节──

## El concepto central.

### Agno

- Python runtime, anteriormente Phi-data.
- "Sin gráficos, cadenas o patrones complicados, solo pitón puro".
- Objetivos de rendimiento de sus documentos: ~ 2μs instanciación de agente, ~ 3,75 KiB de memoria por agente, ~ 23 proveedores de modelos.
- Camino de producción: backend FastAPI sin estado de sesión. Cada solicitud inicia un nuevo agente; el estado de sesión vive en un DB.
- Multimodal nativo (texto, imagen, audio, video, archivo) y RAG agente.

Los objetivos de velocidad importan cuando tienes miles de agentes de corta duración por segundo (fán de chat, canalizaciones de evaluación), pero son menos importantes cuando un agente corre durante 10 minutos.

> ¿ Qué es esto ?**【类比】**Agno 像摩托车、LangGraph 像SUV:摩托车启动快、轻便、能钻小(2μs 实例化、3.75 KiB内存), adaptado a la circulación rápida y frecuente ⋅000 ⋅秒短任务;SUV 装得多、能跑长途、有空调导航(持久化、人回路、复杂图), pero en marcha、慢占地大──**关键洞察**No es porque sea mejor, sino porque tu escenario es "altos tiempos y tareas cortas".

> La velocidad de la meta es importante cuando tienes miles de agentes temporales por segundo. Cuando un agente funciona en 10 minutos, no son tan importantes.

> Agno 和 Mastra es dos tipos de agente de la clase ligera 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos ofrecen un agente de la clase mínima 抽象──

### El Mastra

- TypeScript, construido en el SDK de Vercel AI.
- Tres primitivos:**Agents**¿ Qué ?**Tools**(Tipo de zona), **Workflows**¿ Qué ?
- Modelo unificado de router  3.300+ modelos en 94 proveedores (marzo 2026).
- Almacenamiento compuesto: memoria, flujos de trabajo, observabilidad a diferentes fondos; ClickHouse recomendado para observabilidad a escala.
- Apache 2.0 con `ee/`directorios con licencia empresarial disponible en la fuente.
- Adaptadores de servidores para Express, Hono, Fastify, Koa; integración de primera clase Next.js y Astro.
- Naves Mastra Studio (host local:4111) para el depuración.
- 22k+ GitHub estrellas, 300k+ descargas semanales en 1.0 (Jan 2026).

### Posicionamiento

Tampoco se trata de ser LangGraph.

>  ambas no están tratando de convertirse en LangGraph                                                                                                                                                                                                                                                        

> Agno 和 Mastra es dos tipos de agente de la clase ligera 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos ofrecen un agente de la clase mínima 抽象──

- **Language fit.**Agno para equipos de Python; Mastra para TypeScript.
- **Runtime ergonomics.**Agno = casi cero gastos generales; Mastra = integrado con el ecosistema Vercel.
- **Observability.**Ambos se integran con Langfuse/Phoenix/Opik (Lección 24) pero Mastra Studio es de primera parte.

### ¿Cuándo elegir cada uno?

- **Agno**Python backend, muchos agentes de corta duración, fuertes requisitos de perf, tienda FastAPI.
- **Mastra** Backend de TypeScript, Next.js / Vercel desplegado, enrutamiento unificado de modelos multi-proveedor, herramientas tipo Zod.
- **LangGraph**(Lección 13)  cuando el estado duradero y el razonamiento gráfico explícito importan más que la velocidad bruta.
- **OpenAI / Claude Agent SDK** cuando se desea la forma productiva del proveedor (lecciones 1617).

### Cuando este patrón va mal

> ️ **【易错点】**见 Agno "2μs 实例化"就无脑选 Agno。**后果**Si tu escenario es "una sola solicitud de ejecutar un agente de 10 minutos", 2μs  la implementación del impacto en el tiempo total es 0.0000003%  seleccionó el marco también perdió la capacidad de perdurada de LangGraph **一行修复**El número de casos de trabajo en el sistema de trabajo de Agno, en el caso de que continúe utilizando LangGraph, es superior al 30% de la cantidad de tiempo que se utiliza para realizar el trabajo.

- **Perf-for-perf's-sake.**Elegir Agno porque "2μs" suena bien cuando la carga de trabajo es una llamada lenta de agente por solicitud.
- **Ecosystem lock-in.**La integración con sabor a Vercel de Mastra es un plus en Vercel, un menos en otros lugares.
- **Enterprise license confusion.**El de Mastra.`ee/`Los directorios están disponibles en fuente, no Apache 2.0.

> ¿ Qué es esto ?**【困惑】**P: Mi equipo es Python 后端, ¿quiere también la función "多模型路由" de Mastra, ¿puede utilizar Agno 实现? A: 能, pero para escribir por sí mismo. Agno también tiene ~23 proveedores de modelos, pero el proveedor de Mastra 3300+ 模型 94 se basa en la enorme ecosistema de Vercel AI SDK. Si el "model路由" es el principal requerimiento y el equipo acepta TypeScript, Mastra es la opción preferida; si se adhiere a Python, Agno + autoencubrir un modelo de routers de una capa, también se ejecuta, el volumen de trabajo es de aproximadamente 2-3 天── no es el marco de decisión de la tecnología, sino el de la inversión.

> **为性能而性能。**Porque "2μs" parece no equivocado en elegir Agno, y la carga de trabajo es cada solicitud de un agente de velocidad lenta.
> **生态系统锁定。**El estilo de Vercel de Mastra está en ventaja en Vercel, en otros lugares está en desventaja.
> **企业许可困惑。**El maestro de la`ee/`El código fuente es accesible, no Apache 2.0... si quieres usar el fork, primero lee el permiso.

## Construye y realiza.
```figure
wb-runtime-spawn
```

## Construye el mismo

Esta lección es principalmente comparativa  ningún artefacto de código único haría justicia a ambos marcos. Ver `code/main.py`para un juguete lado a lado: un mínimo de " ejecutar un agente, transmitir la salida, persistir sesión " flujo implementado dos veces (una vez en forma de Agno, una vez en forma de Mastra).

> Esta clase es principalmente comparativa. No hay un producto de código que pueda representar simultáneamente las características de dos marcos.`code/main.py`Un proceso de "Agencia de operación 流式输出、持久化会话" se ha realizado dos veces (una vez Agno 形态, otra vez Mastra 形态)

> Agno 和 Mastra es dos tipos de agente de la clase ligera 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos ofrecen un agente de la clase mínima 抽象──

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Dos rastros estructuralmente diferentes pero funcionalmente equivalentes.

>  La estructura de las dos estructuras es diferente, pero la función es igual.

> Agno 和 Mastra es dos tipos de agente de la clase ligera 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos ofrecen un agente de la clase mínima 抽象──

## Usalo con el marco de ejecución

- **Agno** Backend Python que necesita velocidad y forma FastAPI.
- **Mastra** Backend de TypeScript con muchos proveedores y primitivos de flujo de trabajo.
- Ambos barcos tienen ganchos de observación de primera parte.

## Envíe el producto .

`outputs/skill-runtime-picker.md`elige Agno, Mastra, LangGraph o un SDK de proveedor basado en la pila, el presupuesto de latencia y la forma operativa.

> `outputs/skill-runtime-picker.md`根据技术、延迟预算和运营形态选择 Agno、Mastra、LangGraph 或供应商 SDK──

> Agno 和 Mastra es dos tipos de agente de la clase ligera 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos ofrecen un agente de la clase mínima 抽象──

## Los ejercicios.

1. Lea los documentos de Agno, lleva el ciclo de ReAct a Agno. ¿Qué ha desaparecido?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Lea los documentos de Mastra. Portar el mismo bucle a Mastra. ¿Qué cambió en la mecanografía de herramientas (Zod vs nada)?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Métese la latencia de instanciación de agente en su pila. ¿Las 2μs de Agno importan para su carga de trabajo?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Diseñar una migración: si has estado ejecutando CrewAI en Python, ¿qué se rompe si te mueves a Agno?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Lea el libro de Mastra `ee/`¿Qué restricciones afectarían a un fork de código abierto?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## Más Leer más Leer más

- [Agno Agent Framework docs](https://www.agno.com/agent-framework) objetivos de rendimiento, integración de FastAPI
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Mastra docs](https://mastra.ai/docs) primitivos, adaptadores de servidores, modelo de enrutador
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) la alternativa de gráfico estatal
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Comet Opik](https://www.comet.com/site/products/opik/) comparaciones de observabilidad citadas por las integraciones de Mastra
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
