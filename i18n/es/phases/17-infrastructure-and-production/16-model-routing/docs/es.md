# Modelo de enrutamiento como una reducción de costos primitivo

> Un corredor dinámico evalúa cada solicitud (tipo de tarea, longitud de token, similitud de incorporación, confianza) y envía consultas simples a un modelo barato, aumentando las complejas a un modelo fronterizo. También se llama cascada de modelos. Los estudios de caso de producción muestran una reducción de costes de 20-60% en la calidad de iso en las implementaciones de EE.UU./Reino Unido/UE; una mejora de la eficiencia de enrutamiento del 30% en el SaaS de gran volumen se convierte en un ahorro anual de seis cifras. El contexto de 2026 es que los precios de la inferencia LLM cayeron ~ 10 veces por año  un token de clase GPT-4 se fue de $20/M to ~$0,40/M desde finales de 2022 hasta 2026. La mayor parte de la caída es mejor para las pilas (fase 17 · 04-09), no para el hardware. El enrutamiento es cómo se convierte esa caída de precios en margen sin regresión del producto. El modo de falla es la deriva del modelo barato: la ruta empuja el 40% a un modelo más débil, la calidad cae del 3-5% en las tareas de razonamiento, nadie se da cuenta por un cuarto. Rutas de puertas por métricas de calidad en línea, no sólo conjuntos de evaluaciones fuera de línea.

> **【中文解读】**Este capítulo presenta estrategias de optimización de costos de diferentes modelos según la complejidad de las tareas.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)

> ¿ Qué es esto ?**【前置】**学本节前 請先掌握:Fase 17·01(托管平台) ‧Fase 17·19(AI Gateway) 』模型路由 = 动态 bróker 按任务复杂度选便宜或贵模型──
> ¿ Qué es esto ?**【类比】**模型路由 = "医院分诊"──简单感冒→社区医生(Haiku/Sonnet);疑难杂症→专家(Opus);急诊→主任(GPT-4)──20-60% 成本降,30% 路由效率改进=六位数年省──背景:LLM 价格 2022-2026 降10倍/年,多数降来自服务改进而非硬件路由把价格转转变成利──
> ️ **【易错点】**便宜模型漂移:40% 路由到弱模型→推理质量降低 3-5%→ una cuota de tiempo no se encuentra──修复:用在线质量监控(不仅离线评估)守住底线──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Explica el modelo en cascada: barato primero con control de confianza, escalada en baja confianza.
  Traducción:Módelo de la clase: Precio bajo, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, prefiero, etc.
- Enumera las cuatro señales de enrutamiento (clasificación de tareas, longitud de la tarea, incorporación de similitud con el conjunto duro conocido, confianza en sí mismo desde el primer paso).
  En la actualidad, el sistema de control de las operaciones de la empresa es un sistema de control de las operaciones de la empresa.
- Calcule el coste combinado esperado en la división de rotación de destino y la tolerancia a pérdidas de calidad.
  Traducción:Cantificación de objetivos y de la tolerancia a la pérdida de calidad.
- Nombre de la métrica de monitoreo de deriva (puerta de calidad en línea) que atrapa el modelo barato.
  China:                                                                                                                                                                                                                                                              

## El problema es la introducción del problema

> **【中文解读】**模型路由的核心洞察:70% de las consultas son simples ("¿hace unos pocos puntos en París?""), se puede procesar con un modelo de clase Haiku con un costo perfecto del 3% ∼ solo el 30% ∼ necesita capacidad de razonamiento de nivel GPT-5 ∼ 70% ∼ modelo barato, 30% ∼ modelo de vanguardia, puede bajar en la calidad del mismo producto aproximadamente el 65% ∼ el reto clave es construir un router sin disminuir la calidad ∼

> **【拓展：模型路由的产业案例】**2026 años modelo de ruta en producción Resultados típicos: 20-60% de costo reducido(同质量下) ・ LLM 推理价格从2022年到2026年下降约10x/年(GPT-4 级从$20/M 降到 $La mayor parte de la disminución proviene de la optimización de la aplicación, en lugar de esperar a que todos los usuarios se transfieran a un modelo barato.

Su servicio cuesta $80k/mes en GPT-5. sus análisis muestran que el 70% de las consultas son simples: "¿qué hora es en París?" "refrasear esta frase". Un modelo de clase Haiku maneja perfectamente a 3% del costo. 30% necesita el razonamiento de GPT-5  codificación, matemáticas, planificación en múltiples pasos.

Si se envía el 70% a barato y el 30% a caro, su factura cae alrededor del 65% en la misma calidad del producto. Esto es enrutamiento. El truco es construir el corredor sin regredir la calidad.

## El concepto central.

### Cuatro señales de enrutamiento

> **【中文解读】**Las siguientes características se pueden encontrar en el modelo de seguridad: 1) 任务分类简单/复杂/代码/数学/聊天,可用规则分类器或小 LLM($0.25/M); 2) 提示长度>4K token normalmente necesita un modelo de primera línea,<500 normalmente no se necesita; 3) 嵌入相似度与已知困难集的余弦相似度 >0.88 则直接升级; 4) 首次通过自信度发送到廉价模型,如果日验证显示低信任度或拒绝,重试到沿线模型──

1. **Task classification**Se puede ser un clasificador basado en reglas, un LLM pequeño (Haiku-clase a $0.25/M), o incorporar similitud con baldes etiquetados.

2. **Prompt length**Las señales de +4K a menudo necesitan fronteras para la coherencia.

3. **Embedding similarity to known-hard set**Si la consulta está cerca (cosin > 0,88) de un cubo conocido de durabilidad, escala directamente a la frontera.

4. **Self-confidence from first-pass**Si las pruebas de registro del modelo muestran baja confianza O se niegan O se expone el lenguaje de cobertura, vuelva a intentarlo en frontera.

### Tres patrones

> **【拓展：模型路由的三种模式】**模型路由的三种实现模式对比: 1) Pre-route前置分类器 (规则或小 LLM), aumentar 5-10ms 延迟,总体最快; 2) Cascade先发到廉价模型,低信度时升级到前沿模型,中位延迟约1.2x、升级时约2x,质量底线最好; 3) Ensemble route并行运行廉价和前沿模型,奖励模型选择最佳,最高质量但最高成本──在生产中推 Cascade 作为默认它在质量,成本,延迟之间提供最佳平衡──

**Pre-route**(clasificador por delante): ~ 5-10 ms de latencia añadida; más rápido en general.

**Cascade**(Primero barato, escala en baja confianza): ~1.2x latencia media (corrida barata más verificación), ~2x en escalada.

**Ensemble route**(se ejecuta a bajo costo y fronterizo en paralelo para una muestra, seleccionar un modelo de recompensa): la más alta calidad, el mayor coste; utilizar sólo para A/B crítico.

### Aplicación

Las pasarelas de IA (fase 17 · 19) exponen el enrutamiento.`router`Por ejemplo, el sistema de conexión de acceso a Internet (POS) es un sistema de conexión de acceso a Internet (POS) que permite a los usuarios acceder a Internet en forma automática.

Fuente abierta: RouteLLM (LMSYS), No Diamond (comercial), Prompt Mule.

### La curva de precios de 2026

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

La mayor parte de la mejora es el servicio de eficiencia  las lecciones básicas en la Fase 17 · 04-09 se convirtieron en caídas de costos del lado del proveedor.

### La deriva es el verdadero riesgo

> **【中文解读】**漂移是模型路由的真正风险──路由将将40% 发送到廉价模型,6 个月后任务分布变化(用户更成熟、问题更长), pero el módulo de clasificación del módulo sigue basándose en el entrenamiento de datos Q1──质量下降没有投诉足够响亮, hasta que el competidor no logre ganar en su evaluación de la base de los criterios.

> **【拓展：模型路由的实现方案】**2026 años modelo de ruta de implementación de opciones:(1) AI 网关(Fase 17·19)LiteLLM de router configuración Portkey de guardias+routing Kong AI Gateway de plug-style route OpenRouter de recomendación API;(2) 开源RouteLLM(LMSYS) proporcionar una completa biblioteca de ruta;(3) 商业Not Diamond 提供 SaaS 模型路由产品──三种路由模式:Pre-route(前置分类,最快) Cascade(pre廉价再升级,质量最稳定) ‧Ensemble(并行运行多模型+奖励模型选择,最高质量但最高成本) ∼

Su ruta envía el 40% al modelo barato. Durante seis meses, la distribución de tareas cambia (los usuarios se vuelven más sofisticados, hacen preguntas más largas). El router no se da cuenta porque su clasificador fue entrenado en datos de Q1. La calidad cae silenciosamente. Nadie se queja lo suficientemente fuerte. En un benchmark de competidores descubres que perdiste.

Rutas de puertas por métricas de calidad en línea:

- El usuario sube/baja por ruta.
- Juez de LLM automático en una muestra retenida (5%) por ruta.
- Taxa de escalación: si la cascada está aumentando en la ruta superior a > 30%, el modelo barato está siendo sobre-enrutado.
- Taxa de rechazo por ruta.

### Números que debes recordar

- 2026 ahorros de enrutamiento en iso-calidad: estudios de caso del 20-60%.
- Descenso de los precios de los LLM 2022-2026: ~ 10 veces por año agregado.
- GPT-4 nivel 2022 vs 2026: ~$20/M → ~$0,40/M.
- Impacto de latencia en cascada: ~ 1,2x mediana, ~ 2x escalada (~ 10% del tráfico).

## Usalo con el marco de ejecución
```figure
model-cascade-router
```

## Usalo

`code/main.py`La información de la empresa se centra en la información de los usuarios y en la información de los usuarios.

> `code/main.py`La información de la empresa se centra en la información de los usuarios y en la información de los usuarios.

> `code/main.py`La información de la empresa se centra en la información de los usuarios y en la información de los usuarios.

## Envíe el producto .

Esta lección produce`outputs/skill-router-plan.md`- Dado el volumen de trabajo y el presupuesto de calidad, elige un patrón de enrutamiento y señales.

> 本课产 出  `outputs/skill-router-plan.md`- Dado el volumen de trabajo y el presupuesto de calidad, elige un patrón de enrutamiento y señales.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿En qué piso de precisión la cascada supera la ruta previa?
   Traducción:运行`code/main.py`¿Qué clase de conexión está mejor que la de la ruta previa?
2. Su base de usuarios es de 30% empresarial (cuestiones complejas), 70% de nivel gratuito (simple). Diseñar la división de enrutamiento. ¿Qué métricas en línea se abren?
   En el caso de las empresas, el 30% de su grupo de usuarios es empresa, el 70% es gratuito.
3. Una ruta reduce la calidad en un 2% pero ahorra un 40%. ¿Es un barco?
   China 翻译: 一路由降低质量 2% Pero ahorro 40%── ¿vale la pena?
4. Implementar una verificación de confianza utilizando logprobs de OpenAI / APIs antropológicas. ¿Cuál es el umbral con el que comienza?
   La aplicación de la API de OpenAI / Anthropic API es una aplicación de la API de OpenAI.
5. En seis meses, la tasa de escalada sube del 8% al 22%. Diagnóstico de tres causas y la solución para cada uno.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Más Leer más Leer más

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) Puerta de entrada multimodelo con primitivas de enrutamiento.
