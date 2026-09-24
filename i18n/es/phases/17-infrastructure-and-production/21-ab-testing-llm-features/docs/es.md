# Pruebas A/B de LLM características  GrowthBook, Statsig, y el problema de Vibes ✓  características de LLM PR

> Las pruebas A/B tradicionales no se construyeron para LLM no deterministas. La distinción crítica: evaluaciones de respuesta "¿puede el modelo hacer el trabajo?" pruebas A/B responder "¿cuidan los usuarios?" ambos son necesarios; envío en vibe controles se terminó. Qué probar en 2026: ingeniería rápida (formulación), selección de modelos (GPT-4 vs GPT-3.5 vs OSS; precisión vs costo vs latencia), parámetros de generación (temperatura, top-p). Casos reales: una variante del modelo de recompensa de chatbot proporcionó +70% de duración de la conversación y +30% de retención; experimentos de línea de asunto de Nextdoor AI proporcionaron +1% de CTR después de refinar la función de recompensa; Khan Academy Khanmigo iteró en un eje de latencia frente a la precisión matemática. División de la plataforma: **Statsig**(adquirido por OpenAI por $1.1 mil millones en septiembre de 2025)  pruebas secuenciales, CUPED, todo en uno. **GrowthBook** código abierto, nativo de almacén, motores bayesianos + frecuentistas + secuenciales, CUPED, controles SRM, correcciones Benjamini-Hochberg + Bonferroni.

> **【中文解读】**Este capítulo presenta los métodos de LLM 测试科学评估 功能变更效果的.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·13(可观测性) ‧Fase 17·20(渐进部署) ‧统计基础(CUPED、序贯测试) ‧传统 A/B 不为非确定性 LLM 设计──
> ¿ Qué es esto ?**【类比】**LLM A/B 测试 = "use ciencia method substitute拍脑袋"。关键区别:eval 问"模型能做吗";A/B 问"用户在乎吗"。两者都要──测什么:快措辞、模型选择、生成参数(temperatura/top-p)。案例:聊天机器人变体+70%对话长度+30% 留存;Nextdoor AI 标题+1% CTR;Khanmigo 在延迟 vs 数学准确率间舍──平台:Statsig((AI 11亿收购,全功能) 、GrowthBook 开源源厂 原生、贝叶斯频率+被序贯引擎) ∼
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Distinguir evaluaciones ("puede el modelo hacer el trabajo") de pruebas A/B ("el usuario se preocupa").
  En el idioma chino, el idioma se utiliza para evaluar el usuario.
- Enumera tres ejes testables (prompt, modelo, parámetros) y seleccione la métrica para cada uno.
  En el caso de los modelos, el número de puntos de selección es el número de puntos de selección.
- Explica CUPED, pruebas secuenciales y correcciones de comparación múltiple de Benjamini-Hochberg.
  Traducción:CUPED, ensayo de ensayo y Benjamini-Hochberg
- Elija Statsig o GrowthBook basado en la postura de almacenamiento-SQL y la postura de adquisición corporativa.
  Según el estado de la almacén-SQL y la situación de la empresa en la compra de productos, el estado de la empresa en la actualidad está en el mercado.

## El problema es la introducción del problema

> **【中文解读】**传统 A/B 测试不是为不确定性 LLM 构建的. 关键区分:评估(evals) responder "¿el modelo puede hacer esto?", A/B 测试 responder "¿el usuario está preocupado?" ambos son necesarios凭感觉上线(vibes check)

> **【拓展：LLM A/B 测试的真实案例】**En el año 2026 LLM A/B 测试的生产案例:(1) 聊天机器人奖励模型变体+70% 对话长度、+30% 留存率;(2) Nextdoor AI 主题行实验奖励函数优化后 +1% CTR;(3) Khan Academy Khanmigo在延迟 vs 数学准确率轴上代;;平台选择:Statsig((2025年9月被 OpenAI以 $1.1B 收购) 全合一;GrowthBook开源、仓库原生、Bayesian + Frequentist + Sequential Engine;;

Ha sintonizado manualmente un mensaje de sistema. Se siente mejor. Lo envías. Cambios de conversión por ruido. Culpa a la métrica. O envió un nuevo modelo y la conversión no se movió. ¿El modelo se degradó o el cambio fue demasiado pequeño para detectar? No lo sabes, porque envió sin un A / B.

Los Evals responden si el modelo puede realizar una tarea en un conjunto etiquetado. No responden si los usuarios prefieren la salida. Sólo un experimento en línea controlado responde a eso, y solo si el experimento tiene suficiente poder, controla el no determinismo y corrige para múltiples comparaciones.

## El concepto central.

### Evals vs pruebas A/B

**Evals** fuera de línea, conjunto etiquetado, juez (rubrica o LLM-as-judge o humano). Respuesta: "¿Es la salida correcta / útil / segura en esta distribución fija?"

**A/B test**Respuesta: ¿La nueva variante mueve la métrica de nivel de usuario que importa?

Los valores de Evals comproban regresiones antes de la exposición; A/B confirma el impacto del producto después.

### Qué probar

1. **Prompt engineering** formulación, estructura de la solicitud del sistema, ejemplos.
2. **Model selection** GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. Métrica: precisión (tarea) + costo/solicitud + latencia P99.
3. **Generation parameters** temperatura, top-p, max_tokens. Metrica: específica de la tarea (diversidad de salida vs determinismo).

### CUPED  reducción de la variación

> **【中文解读】**CUPED (en inglés: CUPED) es la técnica clave de reducción de la diferencia de análisis de A/B. El principio es que antes de la comparación, el cambio de análisis de datos de los experimentos anteriores se reduce del 30-70%, y se aplica a un aumento gratuito de la cantidad de muestras.

Experimentos controlados utilizando datos pre-experimentales. Retrocede la variación pre-periódica antes de comparar el post-periodo. Reducción típica de la variación: 30-70%.

Implementación: tanto Statsig como GrowthBook se implementan.

### Pruebas secuenciales

El A/B clásico asume un tamaño de muestra fijo. Las pruebas secuenciales ("peek-and-decide") controlan la tasa de falsos positivos bajo miradas repetidas.

### Correcciones de comparación múltiple

El funcionamiento de 20 pruebas A/B con una confianza del 95% produce un falso positivo por casualidad.

### Desajuste de la relación de muestras SRM 

El hash de asignación aleatoriza a los usuarios a variantes. Si la división 50/50 entrega 47/53, algo está roto.

### Statsig vs GrowthBook

> **【拓展：Statsig vs GrowthBook 选型】**Statsig vs GrowthBook de 2026 año de elección en comparación:Statsig 2025 septiembre de 2015 fue adquirido por OpenAI con $1.1B, es un SaaS completo, con banderas de características + 实验分析 + 可观测性),内置序贯检查和 CUPED, adaptado a los equipos que quieren empaquetarse de productos.

**Statsig**¿Qué es esto ?
- Adquirido por OpenAI por $1.1B (septiembre 2025).
- Pruebas secuenciales, CUPED, poblaciones sostenidas.
- Todo en uno: banderas de características + experimentación + observabilidad.
- Mejor ajuste: el equipo ya quiere un producto en paquete, no le importa la propiedad de OpenAI.

**GrowthBook**¿Qué es esto ?
- código abierto (MIT); nativo de almacén (se lee directamente de Snowflake/BigQuery/Redshift).
- Múltiples motores: Bayesiano, Frequentista, Secuencial.
- CUPED, SRM, Bonferroni, correcciones de la BH.
- Auto-host o en la nube gestionada.
- Lo mejor: almacén de SQL, equipo de datos controla la capa métrica, quiere OSS.

### El no-determinismo complica el poder

El mismo prompt produce diferentes resultados. Los cálculos tradicionales de potencia asumen observaciones de IID. Con el no determinismo LLM, el tamaño de muestra efectivo es menor que nominal. Multiplica el tamaño de muestra requerido por ~1.3-1.5x como margen de seguridad.

### Resultados reales de los casos

- Variante del modelo de recompensa de chatbot: +70% de duración de la conversación, +30% de retención.
- Líneas de temas de la puerta siguiente: +1% CTR después de refinar la función de recompensa.
- Khan Academy Khanmigo: comercio iterativo de latencia frente a la precisión matemática.

### El antipatrón: envío en vibraciones

> **【拓展：LLM 非确定性对 A/B 测试的影响】**La incertidumbre del LLM afecta a la estadística de los A/B teste. La misma sugerencia produce diferentes resultados, la misma potencia tradicional  cálculo hipótesis  IID  observación  Valores. En el LLM incertidumbre, la cantidad de muestras válidas es inferior al valor nominal  Necesita que la cantidad de muestras requerida se multiplie por 1.3-1.5x  como margen de seguridad  Las pruebas secuenciales  Las pruebas secuenciales  Permiten que el ganador se detenga en el momento de la aparición, con un tiempo de prueba de 20-40% de tiempo de la prueba de la cantidad de muestras fija  Los tiempos de prueba de la prueba fija  Más de un tiempo de comparación  Bonferroni / Benjamini-Hochberg) en el mismo tiempo de ejecución de múltiples experimentos son indispensables 

Cada ingeniero senior puede nombrar una característica que se envió porque "se siente mejor" sin A / B. La mayoría de ellos retrocedía métricas de producto que el equipo no notó durante meses. A / B es la función de fuerza.

### Números que debes recordar

- Statsig adquirida por OpenAI: $1.1B, septiembre de 2025.
- GrowthBook: MIT de código abierto; Bayesiano + Frequentista + Secuencial.
- Reducción de la varianza de la CUPED: 30-70%.
- No-determinismo de LLM → +30-50% de tamaño de muestra.

## Usalo con el marco de ejecución
```figure
mx-sequential-test
```

## Usalo

`code/main.py`Simula una prueba A/B secuencial con límites fijos y secuenciales. Muestra cómo secuencial le permite detenerse temprano.

> `code/main.py`Simula una prueba A/B secuencial con límites fijos y secuenciales. Muestra cómo secuencial le permite detenerse temprano.

> `code/main.py`Simula una prueba A/B secuencial con límites fijos y secuenciales. Muestra cómo secuencial le permite detenerse temprano.

## Envíe el producto .

Esta lección produce`outputs/skill-ab-plan.md`. Dado el cambio de características, la carga de trabajo, la línea de base, las opciones de plataforma, puertas, tamaño de muestra.

> 本课产 出  `outputs/skill-ab-plan.md`. Dado el cambio de características, la carga de trabajo, la línea de base, las opciones de plataforma, puertas, tamaño de muestra.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Para un aumento esperado del 5% con conversión del 3% de referencia, ¿qué tamaño de muestra para el 80% de potencia?
   Traducción:运行`code/main.py`◊ Previsión del 5% 提升 基线 3% 转换率, ¿cuánta cantidad de muestras se necesita?
2. Elija Statsig o GrowthBook para un cliente en el lugar regulado por la atención médica.
   China:                                                                                                                                                                                                                                                              
3. Diseñar una A/B que teste GPT-4 vs GPT-3.5 en el costo por boleto resuelto. ¿Cuál es la métrica primaria, métrica de barandillas, secundaria?
   China: diseñar una A/B en cada solución de un solo costo de trabajo GPT-4 vs GPT-3.5 ¿Cuál es el indicador principal?
4. Su canario pasa pero A/B muestra una conversión de -1,2%. ¿Se envía?
   China                                                                                                                                                                                                                                                               
5. Aplicar CUPED a un preperíodo con un 60% de la variación de la post.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## Más Leer más Leer más

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
