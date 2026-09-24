# Política de escalación responsable antropófica v3.0

> RSP v3.0 entró en vigor el 24 de febrero de 2026, reemplazando a la política de 2023. Mitigamiento de dos niveles: lo que Anthropic hará unilateralmente frente a lo que se enmarca como una recomendación a nivel de la industria (incluyendo las normas de seguridad RAND SL-4). Añade mapas de ruta de seguridad fronteriza e informes de riesgos como documentos permanentes en lugar de entregas únicas. Se deja de cumplir el compromiso de pausa para 2023. Introduce el umbral de I+D-4 de la IA: una vez superado, Anthropic debe publicar un caso afirmativo que identifique los riesgos y mitigaciones de desalineamiento. Claude Opus 4.6 no lo cruza. En el anuncio de v3.0, Anthropic dice que "con confianza descartar esto se está volviendo difícil". SaferAI calificó el RSP 2023 en 2.2; redujeron el v3.0 a 1.9, poniendo a Anthropic en la categoría de RSP "débil" junto con OpenAI y DeepMind. Los límites cualitativos sustituyeron a los compromisos cuantitativos de 2023; la eliminación de la cláusula de pausa es la regresión más acentuada.

> **【中文解读】**RSP v3.0 于 2026 年 2 月 24 日生效,替代 2023 政策。两层缓解:Antropic 单边做什么 vs 行业范围建议(incluye RAND SL-4 安全标准) ・添加边界安全路线图和风险报告 作为常设文档而非一次性交付物品──删除 2023 暂停承诺──引入AI R&D-4 齐值:一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;降级 v3.0至 1.9,将将Anthropic 和 DeepMind 开始"一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;将降级 v3.0至 1.9,将Anthropic 和 DeepMind 启动"一个"进入 RAI 弱的定值类别; 关键条项 暂停承诺是暂停退款项;

> **【拓展：v3.0 的核心改动】**Tres cambios clave: 1) 添加前沿安全路线图、风险报告、AI R&D-4 值; 2) 删除2023 暂停承诺; 3) 重构两层缓解时间表(Antropic 单边 vs 行业建议) ――Factores de reducción de la AI: 定性 值替代定量、暂停承诺删除、AI R&D-4 缓解描述为"肯定案例"而不是具体措施、审查机制依赖于安тропо的安全咨询组缺乏独立监督──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

> ¿ Qué es esto ?**【前置】**La fase 15 de la RSI es la fase 15 de la RSI. La fase 15 de la RSI es la fase 15 de la RSI.
> ¿ Qué es esto ?**【类比】**RSP = "AI 公司的安全宪法"──2023 版 = 严格(定量值+暂停承诺);v3.0 = 灵活(定性值+删除暂停)──SaferAI 评分从2.2 降至1.9("弱"类别)──新增AI R&D-4 值 = una vez que la IA 能自动化AI 研发达到某水平, debe obligar a divulgar es un RSI 车──
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué eliminar el compromiso de suspensión? 商业压力──暂停 = 竞争对手超越你──OpenAI、Google 都没暂停,Antropic 单方面暂停=自杀──修复:行业协调(RAND SL-4 标准) + 监管干预(EU AI Act)才能避免囚犯困境──

## El problema es la introducción del problema

Los laboratorios fronterizos publican políticas de escalación que son en parte documentos técnicos, en parte documentos de gobernanza y en parte señales a los reguladores.

> La política de expansión de la primera línea de laboratorio es parte de los documentos técnicos, parte de los documentos administrativos, parte de los mensajes dirigidos a los reguladores.

RSP v3.0 es el documento actual de Anthropic. Leerlo de cerca importa no porque el cumplimiento de él sea vinculante (no lo es), sino porque el marco da forma a cómo un laboratorio concibe el riesgo catastrófico y cómo comunica compromisos al público.

> RSP v3.0 es un proyecto de investigación que se desarrolla en el ámbito de la investigación y la investigación, y que se desarrolla en el ámbito de la investigación y la investigación.

La diferencia entre la versión 3.0 y la versión 2.0 es la unidad útil. Lo que se añadió: mapas de ruta de seguridad fronteriza, informes de riesgos, el umbral de I&D-4 de IA. Lo que se eliminó: el compromiso de pausa de 2023.

> La diferencia entre la versión 3.0 y la versión 2.0 es útil.

Lo que se reformó: un calendario de mitigación de dos niveles dividido entre Anthropic-unilateral y recomendación de la industria.

> 重构:分为人类 单边和行业建议的两层缓解时间表――外部审查SaferAI将分数从2.2(v2)降低到1.9(v3.0)──这是扩展政策如何能在看上看更精细的同时变得更不严谨的――

> **【中文解读】**Política de expansión de la responsabilidad antropológica (RSP, Responsible Scaling Policy) define un marco para mantener la seguridad en el crecimiento de la capacidad de IA. Compromiso central: 1) evaluar si el modelo de evaluación periódica de la vanguardia alcanza el nuevo valor de la capacidad de riesgo; 2) definir la seguridad de los niveles y medidas de seguridad que se ajustan a la capacidad; 3) suspender la promesa si la evaluación falla, suspender la expansión.

## El concepto central.

### El calendario de mitigación de dos niveles.

- **Anthropic unilateral actions**La formación se detiene por encima de un umbral, medidas de seguridad específicas, puertas de despliegue específicas.
  En inglés:**Anthropic 单边动作**No importa lo que otros laboratorios hagan.
- **Industry-wide recommendations**En el caso de la empresa, la empresa no se compromete a cumplir con el objetivo de garantizar la seguridad de los usuarios, sino que se trata de una política de defensa.
  En inglés:**行业范围建议**En el caso de la industria, la industria no tiene ningún compromiso con el desarrollo de la tecnología.

La estructura de dos niveles no estaba en v2. Significa que un lector necesita ver en qué columna vive cada compromiso. Una medida de seguridad en la columna "recomendación a nivel de la industria" no es la promesa de Anthropic; es la esperanza de Anthropic.

> 两层结构在 v2 中没有── esto significa que el lector debe ver cada compromiso en cual uno de los dos.

### El umbral de I&D-4 de IA valor

Este es el nivel de capacidad RSP v3.0 nombra como el próximo umbral importante. Específicamente: un modelo que podría automatizar una parte sustancial de la investigación de IA a un costo competitivo. Una vez que Anthropic cree que un modelo lo cruza, deben publicar un caso afirmativo identificando los riesgos de desalinamiento y las mitigaciones antes de continuar escalado.

> Es el RSP v3.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

Claude Opus 4.6 no lo cruza según el anuncio de v3.0. El documento agrega: "Es difícil descartar esto con confianza". Esa frase es importante; admite que el umbral está lo suficientemente cerca como para ser una preocupación real, no un límite especulativo.

> Claude Opus 4.6 根据 v3.0 公告未跨越它──文档添加:"Confianse地排除这变得困难──"Este es un lenguaje importante; reconoce que el valor es lo suficientemente cercano a la realidad, no a la limitación de la teoría──

La lección 6 (Investigación de Alineación Automática) y la lección 7 (Mejora de Sí Misma Recurrente) se alimentan directamente de este umbral.

> Sección 6 课                                                                                                                                                                                                                                                            

### Mapa de ruta de seguridad fronteriza y informes de riesgos

v3.0 eleva dos tipos de artefactos a documentos permanentes:

> v3.0 se actualizará dos tipos de productos para el archivo permanente:

- **Frontier Safety Roadmap**: documento prospectivo que describe el trabajo de seguridad planificado, las expectativas de capacidad y la investigación sobre la mitigación.
  En inglés:**前沿安全路线图**Descripción del plan de seguridad de trabajo, capacidad de previsión y de la investigación de la reducción de la carga.
- **Risk Report**: documento retrospectivo sobre modelos específicos después de su liberación, que describe la capacidad observada y el riesgo residual.
  En inglés:**风险报告**: publicar un modelo específico de hecho, describir la capacidad de observación y el residuo de riesgo.

Ambos son públicos. Ambos se actualizan en una cadencia declarada. La utilidad es: el lector puede rastrear cómo lo que Anthropic dijo que haría en una hoja de ruta se compara con lo que informan en un informe de riesgo.

> 两者公开──两者按声明节奏更新──效果: Reader可追踪 Antropic 在路线图中说会做与在风险报告中报告中的报告的如何对比──

### Eliminar la cláusula de pausa 删除暂停条款

El RSP 2023 incluyó un compromiso explícito de pausa: si un modelo cruzaba los umbrales de capacidad específicas, la capacitación se detendría hasta que las mitigaciones estuvieran en marcha. v3.0 reemplaza la pausa explícita con una formulación más suave (publicar un caso afirmativo, proceder si las mitigaciones son adecuadas). SaferAI y otros analistas lo calificaron directamente como la regresión más fuerte en el nuevo documento.

> 2023 RSP incluye un compromiso de suspensión de forma clara: si el modelo transcende un valor específico, el entrenamiento se suspenderá hasta que se acumule su capacidad.

El argumento de la política para el cambio: los umbrales cuantitativos en 2023 resultaron ser inalcanzables por los puntos de referencia de capacidad de la era 2026 porque los mismos puntos de referencia fueron reescalados.

> 变更的政策论文:2023 时代能力基准的定量值被2026 时代能力基准证明不可达成,因为基准本身被重缩放了──反论: la suspensión de la política de expansión es un instrumento de compromiso; la eliminación de la política de eliminación es una credibilidad──

### La baja de seguridad de la IA

SaferAI es una organización independiente que califica documentos de estilo RSP. Su calificación pública: 2023 Anthropic RSP obtuvo 2.2 (de una escala en la que 4.0 es el mejor RSP actual y 1.0 es nominal). v3.0 obtuvo 1.9. Esto movió a Anthropic de "moderado" a "débil", uniéndose a OpenAI y DeepMind en la categoría débil.

> SaferAI es una organización independiente que evalúa RSP 式文档. Its public rating:2023 Antropic RSP 得 2.2(4.0 es el mejor RSP actual, 1.0 es el mejor RSP nominal en la escala de la clasificación.

Los factores de rebaja por SaferAI:

> Factores de baja de seguridad:

- Los umbrales cualitativos sustituyeron a los cuantitativos.
  En inglés, el nombre de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona.
- Se ha eliminado el compromiso de pausa.
  En español: suspender el compromiso de la transferencia.
- Las mitigaciones del umbral de I+D-4 de IA se describen como "casos afirmativos" en lugar de medidas específicas.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Los mecanismos de revisión dependen del Grupo de Asesoría de Seguridad de Anthropic, con una supervisión independiente limitada.
  El mecanismo de revisión depende de la seguridad de la organización, independiente.

### ¿Qué es esta lección?

Esta no es una lección de cumplimiento. RSP v3.0 no es una regulación; nada obliga a Anthropic a seguirlo.

> Esto no es un programa de reglamentación.

La lección es leer el documento con la especificidad y el escepticismo que merece. Las políticas de escalación son los principales laboratorios públicos de señales fronterizas que emiten sobre la postura de riesgo catastrófico.

>  El programa es el de las características y dudas que se deben leer en el archivo. La política de expansión es el principal mensaje público emitido por los laboratorios de vanguardia sobre los comportamientos de riesgo de catástrofe. Leer que son habilidades prácticas para cualquier trabajo en el que los trabajadores dependen de la capacidad de vanguardia.

## Usalo con el marco de ejecución
```figure
a5-rsp-ladder
```

## Usalo

`code/main.py`Implementa un pequeño motor de decisión que refleja la forma de evaluación del umbral de RSP: dado un modelo candidato y un conjunto de mediciones de capacidad, devuelve si el umbral de I&D-4 de IA se cruza, las secciones de casos afirmativos requeridas y si la implementación puede continuar. Es intencionalmente simple; el punto es hacer explícita la lógica del documento.

> `code/main.py`实现镜像 RSP 值评估形状的小决策引擎:给定候选模型和一组能力测量,返回 AI R&D-4 值是否跨越、需要肯定案例节、部署是否可继续──它故意简单;点是让文档逻辑显式──

## Envíe el producto .

`outputs/skill-scaling-policy-review.md`revisa una política de escalado (Antropic, OpenAI, DeepMind o interna) en comparación con la referencia de v3.0: estructura de dos niveles, umbrales, compromisos de pausa, revisión independiente.

> `outputs/skill-scaling-policy-review.md`Con respecto a la versión 3.0  参考审查扩展政策 ((Antropic、OpenAI、DeepMind或内部): dos niveles de estructura、值、暂停承诺、独立审查。

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Introducir tres modelos sintéticos en diferentes niveles de capacidad.
   Traducción:运行`code/main.py`En tres diferentes niveles de capacidad de modelos sintéticos.

2. Lea RSP v3.0 en su totalidad (32 páginas). Identifique cada compromiso que vive en el nivel de "recomendación a nivel de la industria". ¿Cuál de esos compromisos habría sido "antrópico unilateral" en v2?
   En el caso de la industria, el sector de la energía es el más importante.

3. Lea la metodología de clasificación de RSP de SaferAI. Reproduce su puntaje 1.9 para la versión 3.0 aplicando su rúbrica al documento. ¿Qué fila de rúbrica impulsó la rebaja más?
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

4. Proponer un compromiso de reemplazo que preserve la credibilidad de la política y reconozca el problema de recalentamiento de los valores de referencia de 2026.
   China 暂停承诺被移除──提议保留政策可信度同时承认2026 基准重缩放问题的替代承诺──

5. Compare RSP v3.0 con OpenAI Preparedness Framework v2 (lección 20). Elige un área donde v3.0 es más fuerte. Elige un área donde el Framework de Preparación es más fuerte.
   La versión de RSP v3.0 se compara con OpenAI Preparedness Framework v2 (第 20 课) ⋅ seleccionar un campo de preparación de v3.0 更强的领域── seleccionar un campo de preparación 更强的领域──

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Más Leer más Leer más

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) la política completa de 32 páginas.
  En el texto original, el texto se traduce en inglés como "la ley de la ley".
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) resumen de los cambios de v2.
  En el caso de los niños, el nombre de la persona que se encuentra en el centro de la ciudad es el de la familia.
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) documento permanente vinculado a partir de RSP v3.0.
  La versión de RSP 3.0 está disponible en el archivo de RSP.
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) retrospectiva del modelo fronterizo actual.
  En español, "la historia de la historia" se traduce en "la historia de la historia".
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) conecta AI R&D-4 a la autonomía medida.
  China:将 AI R&D-4 连接到测量的自主性──
