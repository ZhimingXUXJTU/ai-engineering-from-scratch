# Trafico de sombras, Canarias, y el despliegue progresivo para LLM

> Los despliegues de LLM combinan las partes más difíciles de la implementación de software: no hay pruebas unitarias, modos de falla difusos, señales retrasadas. La secuencia es (1) modo sombra  solicitudes de prod duplicadas al modelo candidato, registro, comparación con impacto de usuario cero; captura problemas obvios de distribución pero no es una garantía de calidad; (2) lanzamiento canario  cambio progresivo de tráfico 10% → 25% → 50% → 75% → 100% con puertas en cada paso; percentil de latencia de seguimiento, costo / solicitud, tasa de error / rechazo, distribución de longitud de salida, tasa de retroalimentación del usuario; (3) pruebas A / B para alternativas distintas después de que se confirme la estabilidad. El no determinismo es irreducible  hasta una variación de precisión del 15% en las carreras con entradas idénticas debido a la no-asociabilidad de la GPU FP más la variación del tamaño del lote. El costo es variable, no constante  un modelo mejor del 20% puede ser 3 veces más caro por llamada. La velocidad de retroceso es decisiva: si el retroceso requiere una nueva implementación, usted es demasiado lento. La política se vive en configuración/banderas; el modelo se vive en el registro con digestos fijados; el retroceso = política de cambio + umbral de retroceso + modelo antiguo en segundos.

> **【中文解读】**Este episodio presenta la estrategia de implementación de Shadow / Kinshear / Gradual Deployment LLM  Servicios de Seguridad en línea.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

> ¿ Qué es esto ?**【前置】**Estudiar en la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de
> ¿ Qué es esto ?**【类比】**LLM 部署三步 = "飞机首飞流程"。Shadow = 地面模拟(复制 prod 请求,零用户影响,对比较但不切换);Canary = 真飞但逐步开载客客(10%→25%→50%→50%→100%,每步有门禁);A/B = 商业航班对比较(稳定测不同方案)。关键后:非确定性不可消除(GPU 浮点+batch 差异致 15% 准确率波动);成本是变量(好20%的模型可能贵3倍);秒回滚速度决定性(级旗 切换不可重新部署)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Distinguir entre el modo sombra (comparación de impacto cero), canario (trafico en vivo progresivo) y A/B (comparación confirmada por estabilidad).
  En el caso de los grupos de población, el número de personas que viven en el área de la población es de aproximadamente un millón de personas.
- Enumerar cinco métricas canarias específicas del LLM (latencia, coste/solicitud, error/rechazo, distribución de longitud de salida, retroalimentación del usuario).
  China: 列举五个 LLM 特定金丝雀指标 (): 延迟, 成本, 要求, 错误, 拒绝, 输出长度分布, 语义质量样本)
- Explicar por qué el no determinismo de la LLM (hasta el 15%) cambia lo que significa "estable" en un despliegue.
  Traducción: explica por qué LLM no está definido (高达15%) ha cambiado el significado de la introducción de "稳定" (estabilidad).
- Diseñar un camino de retroceso que tome segundos (invertir la política) y no horas (redistribuir).
  En el caso de los primeros tiempos, el diseño de un segundo ciclo de la estrategia de la redondadura es un proceso de redistribución.

## El problema es la introducción del problema

> **【中文解读】**La implementación de LLM ha combinado las partes más difíciles de la implementación de software: no hay unidad de prueba, no hay un modelo de fracaso, no hay señal de retraso. La secuencia correcta es: 1) el modelo de sombra, que va a copiar la solicitud de producción hasta el modelo candidato, el índice de resultados, el impacto de los usuarios; 2) la publicación de 金丝雀 10%→25%→50%→75%→100% 100% Cambio de flujo progresivo, cada etapa tiene un indicador de control; 3) la comparación de A/B 测 稳定性确认后的比比比──回滚速度是决定性的 策略标志翻转(30秒)vs 重部署(3 小时)

> **【拓展：LLM 非确定性与部署】**La incertidumbre de LLM es inconveniente La misma entrada en el mismo modelo puede producir hasta un 15% de diferencia de tasa de precisión. La razón:GPU FP no es unidad, tamaño de lote, diferencia, temperatura > 0 de la muestra)  Esto significa que "estabilidad" en la implementación de LLM significa "indicador dentro de la expectativa", y no "igual con la línea de base".

En 24 horas, el costo ha aumentado un 40%, el número de usuarios ha aumentado un 8%, tres boletos de clientes reportan "respuestas extrañas".

Cada pieza de eso era evitable. El modo sombra habría alcanzado el 40% de aumento de costos antes de que cualquier usuario lo viera. Canary se habría detenido en el 10% cuando se movieron los pulgares hacia abajo. La retroceso de la bandera de política habría tomado 30 segundos. La disciplina es lo que llena la brecha entre "las evaluaciones fuera de línea se ven bien" y "los usuarios reales están felices".

## El concepto central.

### Modo de sombra

> **【中文解读】**影子模式候选模型接收与生产相同的请求,输出仅记录不回归用户――日志内容包括:输出内容(与生产不同) 代码数量(成本差异)、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒绝变化、硬错误――不能捕获: usuario percibirá la calidad diferenza影子 es un test de humo, no un test de calidad―

El candidato recibe las mismas solicitudes que la producción; las salidas se registran, no se devuelven a los usuarios. Cero impacto del usuario.

- Contenido de la producción (diferencia con la producción).
- Cuentas de tokens (delta de costo).
- La latencia.
- Rechazo y error.

Captura: aumento de costos, regresión de longitud, cambios obvios de rechazo, errores difíciles. NO captura: los usuarios del delta percibirían calidad.

### Despliegue de las Canarias

> **【拓展：LLM 金丝雀发布的五个门控指标】**LLM 金丝雀 publica cinco indicadores de control de las fiestas: 1) 延迟百分位(P50/P95/P99) canary P99 > 1.5x 基线则触发; 2) cada solicitud cost>20% 高于基线则触发; 3) 错误/拒绝率2x 基线则触发; 4) 输出长度分布均值 + P99 分布偏移值则触发; 5) 用户反率指下/工单 1.5x 基线则触发;; típico progreso 1%→10%→25%→50%→75%→100%, cada etapa acumula suficiente en 5-15 minutos 分样检查间隔)

Progresividad del tráfico con puertas. Progreso típico: 1% → 10% → 25% → 50% → 75% → 100%. Puerta en 5 métricas en cada paso:

1. **Latency percentiles** P50, P95, P99. Infracción: el canario tiene P99 > 1,5 veces el valor de referencia.
2. **Cost per request** mezclado. incumplimiento: > 20% por encima del límite de referencia.
3. **Error / refusal rate**5xx más rechazos explícitos.
4. **Output length distribution** media + P99. incumplimiento: cambio de distribución.
5. **User-feedback rate** pulgares hacia abajo / presentación de boletos.

### El no determinismo es la nueva variación

Las entradas idénticas producen resultados no idénticos.

- No asociatividad de la GPU FP (el orden de reducción de puntos flotantes varía según el lote).
- Varianza de tamaño de lote (el mismo pedido en un lote de 128 vs lote de 16).
- Muestreo (temperatura > 0).

Medido: hasta un 15% de variación de precisión en ejecución a ejecución en conjuntos de evaluaciones idénticos. "Stable" en un despliegue significa que las métricas están dentro de la variación esperada, no idénticas a la línea de base.

### El costo es variable

Un modelo mejor del 20% puede ser 3 veces más caro por llamada. El costo/solicitud es una de las cinco puertas.

### El Rollback es el arma

- Bandera de política (sistema de banderas de características): porcentaje de cambio en configuración; toma segundos.
- Pinning de modelo (digest de registro): el modelo pegado no se actualiza automáticamente.
- Repetición = revertir la bandera + fijar el digesto fijado a la anterior.

Si su pila requiere de redistribuir para volver a rodar, arregle eso antes de rodar.

### Equipamiento

> **【拓展：LLM 渐进式部署工具链】**Selección de herramientas para la implementación de la LLM 2026: 1) Argo Rollouts / FlaggerKubernetes 原生渐进式部署控制器,与 Istio/Linkerd 加权路由集成; 2) Istio ponderada enrutamiento服务网格级流量切分; 3) KServe / Seldon Core模型服务自带卡纳里功能; 4) FlagsLaunchDarkly、Flagsmith、Unleash, strategy class翻转无需重新部署;; 回滚基础设施:策略标志标志功能系统)翻转百分比在配置中秒级) 模型注册摘要固定pinged digest 不自动升级)  Si necesitas una nueva implementación de la red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red red

**Argo Rollouts**- ¿ Qué ?**Flagger** Controller de entrega progresiva Kubernetes. Integrado con el enrutamiento ponderado Istio/Linkerd.

**Istio weighted routing** División del tráfico a nivel de red de servicio.

**KServe / Seldon Core** modelo que sirve con canario incorporado.

**Feature flags**LaunchDarkly, Flagsmith, Unleash, Flip de nivel de política, no hay redistribución.

### Cadencia de las métricas

Las puertas canarias revisan cada 5-15 minutos dependiendo del volumen de tráfico. El 1% del tráfico con 10 req/min da 50-150 puntos de datos por ventana  suficiente para la latencia pero ruidoso para la retroalimentación del usuario. El 10% da ~10x más.

### El paso A/B es opcional.

Si el nuevo modelo es claramente diferente (comportamiento diferente, curva de costos diferente, tono diferente), A/B prueba a 50% después de que canario pasa.

### Números que debes recordar

- Progresón canaria: 1% → 10% → 25% → 50% → 75% → 100%.
- Topo de no determinismo: hasta un 15% de variación entre entradas en función de las entradas idénticas.
- Cinco métricas canarias: latencia, coste, error/rechazo, duración de salida, retroalimentación del usuario.
- Por ejemplo, el precio de la empresa de la empresa de la empresa de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de marca de la marca de la marca de marca de la marca de marca de la marca de marca de la marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de
- Repetición: segundos, no horas.

## Usalo con el marco de ejecución
```figure
i4-canary-ramp
```

## Usalo

`code/main.py`Simula un despliegue canario con regresiones inyectadas.

> `code/main.py`Simula un despliegue canario con regresiones inyectadas.

> `code/main.py`Simula un despliegue canario con regresiones inyectadas.

## Envíe el producto .

Esta lección produce`outputs/skill-rollout-runbook.md`. Dado el modelo candidato, el nivel de referencia y la tolerancia al riesgo, diseña un plan de sombra→canario→100%.

> 本课产 出  `outputs/skill-rollout-runbook.md`. Dado el modelo candidato, el nivel de referencia y la tolerancia al riesgo, diseña un plan de sombra→canario→100%.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Inyectar una regresión del 25% de costos. ¿En qué etapa se detiene el canario?
   Traducción:运行`code/main.py`¿En qué etapa la capturan?
2. Su nuevo modelo tiene un aumento de 3% de precisión fuera de línea pero el costo/solicitud es +18%. ¿Es un barco?
   Traducción:Tu nuevo modelo se encuentra en línea, pero el costo/petición es de +18%.
3. Diseñe un retroceso que dure menos de 60 segundos de extremo a extremo.
   En el caso de los edificios de construcción, el edificio de construcción de la ciudad de Nueva York, en el que se encuentra el edificio, se puede ver el edificio de construcción de la ciudad de Nueva York.
4. No determinismo muestra ±7% en su evaluación.
   China:Incertidity muestra +/-7%── establecer un control de la información para evitar un error.
5. El modo sombra tiene un aumento de 40% antes de canario.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Más Leer más Leer más

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
