# Metricas de inferencia  TTFT, TPOT, ITL, Goodput, P99                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

> Cuatro métricas deciden si una implementación de inferencias está funcionando. TTFT es preempleo más cola más red. TPOT (equivalentemente ITL) es el costo de decodificación de memoria por token. La latencia de extremo a extremo es TTFT más TPOT veces longitud de salida. El rendimiento es los tokens por segundo agregados en toda la flota. Pero lo que importa para el producto es el goodput  la fracción de solicitudes que cumplieron con todos los SLO simultáneamente. Alto rendimiento con bajo goodput significa que estás procesando tokens que nunca llegan a los usuarios a tiempo. Números de referencia para Llama-3.1-8B-Instruir sobre TRT-LLM en 2026: TTFT promedio de 162 ms, TPOT promedio de 7,33 ms, E2E promedio de 1,093 ms. Siempre reportar P50, P90, P99  nunca sólo significa. Y observa la trampa de medición: GenAI-Perf excluye TTFT del cálculo de ITL, LLMPerf lo incluye; dos herramientas no están de acuerdo en TPOT para el mismo ejecutivo.

> **【中文解读】**Este capítulo presenta los indicadores clave de la calidad de los servicios y el sistema de indicadores clave de la calidad de los servicios.
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 统计基础(百分位) ・・・推理指标四件套:TTFT(首代币 时间) + TPOT(每代币 时间) + 吞吐量 + Goodput。
> ¿ Qué es esto ?**【类比】**推理指标 = "餐厅 KPI"。TTFT = 顾客坐下第一道菜上桌(prefill+queue+network);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅每小时出餐总数;Goodput = 满足所有SLO的请求比例(关键!)。陷:高吞吐低 Goodput = ha hecho muchos platos pero el cliente no ha consumido en su tiempo de comida.
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Definir con precisión TTFT, TPOT, ITL, E2E, rendimiento y goodput y nombrar el componente que cada uno mide.
  En el caso de los datos de la información, el usuario puede utilizar el código de acceso de la información.
- Explica por qué la media es la estadística equivocada para el servicio de LLM y cómo leer P50/P90/P99.
  Traducción: explica por qué el promedio es la estadística errónea de LLM  servicios, así como cómo leer P50/P90/P99。
- Construir una restricción SLO multi- (por ejemplo, TTFT < 500 ms Y TPOT < 15 ms Y E2E < 2 s) y calcular el buen rendimiento en relación con ella.
  La producción de la máquina de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de
- Nombre de dos instrumentos de referencia que no estén de acuerdo en TPOT para el mismo período y explica por qué.
  Traducción:Dicho que dos en el mismo funcionamiento producen diferentes resultados en TPOT.

## El problema es la introducción del problema

> **【中文解读】**推理服务有多个延迟轴,每个轴以不同方式失败──预先是计算有限的,随提示长度增长;Decode是内存有限的,随批量 增长;排队延迟是运维问题;网络是物理距离问题──需要不同的指标来衡量每个维度,需要百分数,还需要一个综合指标说"用户是否获得了预期的体验"这就是Goodput──

> **【拓展：LLM 推理指标体系】**El sistema de indicadores completos de LLM 推理 2026 años incluye: 1) TTFT 首代币 延迟) 用户感知到的首次响应时间; 2) TPOT/ITL(每代币 延迟/inter-token 延迟) 流式输出平滑度; 3) E2E(端到端延迟) 从请求到完成的总时间; 4) 吞吐量) 集群效率指标; 5) Goodput(有效吞吐) 同时满足所有 SLA 请求比例;;ML已经Perf Inference v6.0  Goodput 作为官方提交指标;;

"Nuestro rendimiento es de 15.000 tokens por segundo". ¿Y qué? Si el 40% de las solicitudes pasan de 2 segundos de extremo a extremo, los usuarios abandonan la sesión.

> "Nuestra capacidad de abastecimiento es de 15.000 tokens por segundo".""¿Qué pasa? Si el 40% de las solicitudes de terminación exceden los 2 segundos, el usuario abandonará la conversación―solo la capacidad de abastecimiento no puede decirle si el producto funciona correctamente―.

La inferencia tiene múltiples ejes de latencia y cada uno falla de manera diferente. El preempleo está limitado por el cálculo y se mide con una longitud rápida. El decodificación está ligada a la memoria y se mide con el tamaño del lote. El retraso en la cola es un problema operativo. La red es un problema de distancia física. Necesitas métricas distintas para cada uno, y necesitas percentillas, y necesitas un único compuesto que diga "el usuario obtuvo lo que esperaba"

> 推理有多延迟轴,每个轴以不同方式失败──预填充是计算有限的,随提示长度增长──解码是内存有限的,随批次大小增长──排队延迟是运维问题──网络是物理距离问题──你需要每维度不同的指标,需要百分数,还需要一个综合指标说"用户是否得到了预期的体验"这是Goodput──

## El concepto central.

### TTFT  tiempo para el primer token

> **【中文解读】**TTFT = tiempo de cola + red_request + prefill_time。Prefill en el tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo de tiempo

`TTFT = queue_time + network_request + prefill_time`

Prefill domina cuando las instrucciones son largas. En Llama-3.3-70B FP8 en H100, una instrucción de 32k toma ~800 ms de prefill puro. El tiempo de cola es el comportamiento del programador bajo carga. La solicitud de red es el tiempo de cable incluyendo TLS. TTFT es la latencia que el usuario ve antes de que algo fluye de nuevo.

> 预填充在长提示时占主导──Llama-3.3-70B FP8 在 H100 上,32K 提示需要约800ms的纯预填充──排队时间是调度器的行为──网络请求是包括TLS的线缆时间──TTFT是用户在任何内容流式返回前感知到的延迟──

### TPOT / ITL  latencia entre tokens

> **【中文解读】**TPOT(tiempo por token de salida) = ITL(latencia intertoken) = latencia de decodificación por token。公式:TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下,TPOT 均值约7ms;无分块预填充时,在长预填 邻居序列期间 TPOT 可升至50ms。永远监控 P99而非均值。

Muchos nombres para una cantidad.`TPOT`(tiempo por token de salida), `ITL`(latencia entre tokens), `decode latency per token`Es el tiempo entre los tokens transmitidos consecutivos después del primero.

> Una cantidad de nombres múltiples.`TPOT`(por cada salida de token 时间)`ITL`(inter-token 延迟)`每 token 解码延迟`都是同一个──它是第一个标志 之后连续流式标志 间的时间──

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

En la misma pila Llama-3.3-70B H100 con preempleo en pedazos, TPOT significa ~ 7 ms. Sin preempleo en pedazos, durante un largo preempleo en una secuencia vecina, TPOT puede aumentar a 50 ms. Observa P99, no significa.

> En el mismo Llama-3.3-70B H100                                                                                                                                                                                                                                                          

### La latencia E2E

`E2E = TTFT + TPOT * output_tokens + network_response`

Para las salidas largas (> 500 tokens), E2E está dominado por TPOT. Para las salidas cortas con pedidos largos, E2E está dominado por TTFT.

> 对于长输出(>500 tokens),E2E por TPOT 主导──对长提示的短输出,E2E por TTFT 主导──报告按输出长度分条件的E2E──

### Capacidad de transmisión

`throughput = total_output_tokens / elapsed_time`

La métrica agregada le dice la eficiencia de la flota no la salud de las solicitudes individuales.

> 聚合指标――告诉你集群效率――不告诉你单个请求的健康状况――

### Goodput  la métrica que realmente te importa

> **【中文解读】**El buen rendimiento es el único indicador integral realmente importante. El SLO es un requisito único que se cumple simultáneamente con TTFT <= a、TPOT <= b、E2E <= c 才算"好"── Alto rendimiento en el 60% El buen rendimiento es un fracaso; bajo rendimiento en el 99% El buen rendimiento es el objetivo―2026 años MLPerf Inference v6.0 y AI plataformas de proveedores de SLA interno 追踪 todos los buenos rendimientos como indicador central―

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

El SLO es una restricción múltiple. Una solicitud es "buena" sólo si se cumple cada restricción. Goodput es la participación.

> El SLO es de muchos límites. Sólo cuando todos los límites se cumplen, la solicitud es "buena".

En 2026, el goodput es la métrica utilizada en las presentaciones de MLPerf Inference v6.0 y en el seguimiento interno de SLA en los proveedores de plataformas de IA.

> 2026 年,Goodput 是 MLPerf Inference v6.0 提交和 AI 平台提供商内部 SLA 追踪使用的指标──

### ¿Por qué la mala es la estadística equivocada?

> **【中文解读】**LLM 延迟分布是右偏的──一个包含长预填 邻居的解码批可能发发出 500 个 TPOT ~7ms的代币 和 20 个 TPOT ~60ms的代币──平均值 TPOT是9ms,但P99 TPOT是65ms──用户经常遇到P99这就是他们离开的原因──永远报告三元组(P50,P90,P99),对于用户体验,P99是需要优化的目标──

Las distribuciones de latencia LLM son distorsionadas a la derecha. Un lote de decodificación con un vecino de pre-empleo largo puede enviar 500 tokens con TPOT ~ 7 ms y 20 tokens con TPOT ~ 60 ms.

> LLM 延迟分布是右偏的──一个包含长预填充邻居的解码批次可以发发出500 个 TPOT 约7ms的代币和20 个 TPOT 约60ms的代币──平均值 TPOT 是9ms──P99 TPOT 是65ms──用户经常遇到P99这就是他们离开的原因──

Siempre informe el triple (P50, P90, P99). Para la experiencia del usuario, P99 es el que optimiza.

> 始终报告三元组(P50、P90、P99)。 Para la experiencia del usuario, P99 es lo que necesitas para mejorar。

### Números de referencia  Llama-3.1-8B-Instrucción sobre TRT-LLM, 2026

- TTFT medio: 162 ms
  El valor promedio de la TTFT: 162ms
- TPOT medio: 7,33 ms
  El valor promedio de TPOT: 7.33ms
- medias E2E: 1,093 ms
  El valor promedio de E2E:1,093ms
- P99 TPOT: varía entre 10 y 25 ms dependiendo de la configuración de preempleo en pedazos.
  En el caso de los equipos de carga, el tiempo de carga de los equipos de carga es de 10-25 ms.

Estos son los puntos de referencia publicados de NVIDIA. Cambian con el tamaño del modelo (70B mostraría 3-5x), el hardware (H100 vs. B200 ~ 3x), y la carga.

> Estos son datos de referencia publicados por NVIDIA. Los datos de referencia son de tamaño de modelo.

### La trampa de medición

> **【中文解读】**Las dos herramientas de prueba de base más comunes de 2026 en TPOT producen diferentes resultados: NVIDIA GenAI-Perf eliminará TTFT de ITL  cálculo de los tokens 2  comienzos, LLMPerf  contiene TTFT  desde el token 1  comienzos) ⋅ la misma solicitud  TTFT 500ms、100  salida de tokens、 700ms decodificación, GenAI-Perf  informe ITL=7.07ms, LLMPerf  informe ITL=12.00ms。 siempre explica qué herramienta utilizar, siempre publicar definición。

> **【拓展：LLM 基准测试工具生态】**El programa de pruebas de base de la LLM de 2026 incluye: 1) NVIDIA GenAI-PerfTriton 客户端,全面指标覆盖,ITL 不含TTFT; 2) LLMPerfAnyscale) Rust-backed 分词,流式感知,含TTFT的ITL; 3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题; 4) guidelm大规模合成基准测试; 5) k6 v2026.1.0流式感知,Kubernetes-native──选择工具时要了解其ITL 定义差异──

Dos de las herramientas de referencia más utilizadas para 2026 no están de acuerdo en TPOT para el mismo período:

- **NVIDIA GenAI-Perf**El ITL comienza con el token 2.
  En inglés:**NVIDIA GenAI-Perf**Desde ITL 计算中排除 TTFT──ITL 从第2个标志 开始──
- **LLMPerf**El ITL comienza con el token 1.
  En inglés:**LLMPerf**:incluye TTFT──ITL desde la 1 个代币 开始──

Para una solicitud con TTFT 500 ms y 100 tokens de salida en 700 ms total de decodificación, GenAI-Perf informa `ITL = 700/99 = 7.07 ms`, informa LLMPerf `ITL = 1200/100 = 12.00 ms`La elección de la herramienta cambia el número.

>  Para un TTFT 500ms  100  salida de token  700ms  total resolución de la solicitud, GenAI-Perf  informe `ITL = 700/99 = 7.07ms`,LLMPerf  informe `ITL = 1200/100 = 12.00ms`◊ herramienta para cambiar el número.

Siempre indique qué herramienta. Siempre publique la definición.

> 始终说明使用哪个工具──始终发布定义──

### Construir un SLO

> **【拓展：LLM SLO 设定参考】**2026 años de recomendación de consumo de grado 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput >= 99%──企业级 SLO 收紧 TTFT(200-400ms) pero放宽 E2E──测量方法:使用真实流量或LLMPerf 合成流量(`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`), objetivo 2x 峰值并发,运行 30-50 次代取百分位数──

Un SLO razonable para el consumidor para un modelo de chat 70B en 2026:

- TTFT P99 <= 800 ms.
  En el caso de los usuarios de Internet, el usuario puede utilizar el código de acceso de Internet para obtener información sobre el usuario.
- TPOT P99 <= 25 ms.
  En inglés, el nombre de la marca de la marca es TPOT P99 <= 25ms(
- E2E P99 <= 3 s para las salidas de < 300 tokens.
  En inglés, el nombre de la marca de la marca de la marca es "E2E P99" (E2E P99)
- Objetivo de rendimiento >= 99%.
  En inglés, el nombre de la empresa es "Centro de la Información".

Los SLO de la empresa apretan el TTFT (200-400 ms) y aflojan el E2E. El punto es escribirlos, medir los tres y rastrear el goodput como un solo compuesto.

> 企业级 SLO 收紧 TTFT(200-400ms)并放宽 E2E──关键是要写下来、测量全部三、并将Goodput 作为单一综合指标追踪──

### Cómo medir

- Realizar tráfico real o realista sintético (LLMPerf con `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`¿Qué es lo que se hace?
  Traducción:运行真实流量或逼真合成流量 (en inglés)`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)。
- Objetivo de 2 veces la concurrencia máxima para la ejecución de referencia.
  El objetivo de la operación de pruebas de base es de 2 veces el valor de la cumbre.
- Ejecutar 30-50 iteraciones, tomar percentiles de la muestra combinada.
  Traducción:运行 30-50 次代,取合并样本的百分位数──
- Publica con el nombre de la herramienta, la versión de la herramienta, el modelo, el hardware, la concurrencia, la distribución rápida.
  En inglés, el nombre de la herramienta es el nombre de la herramienta.

## Usalo con el marco de ejecución
```figure
throughput-latency
```

## Usalo

`code/main.py`Es una calculadora de buen rendimiento de juguete. Generar una distribución de latencia sintética, aplicar un SLO, y calcular el buen rendimiento. También muestra la diferencia de TPOT GenAI-Perf vs LLMPerf en el mismo rastro.

> `code/main.py`Es un modelo de Goodput  calculador。 generar sintetizado延迟分布, aplicar SLO, calcular Goodput。 también mostrar el mismo rastro 上 GenAI-Perf vs LLMPerf de TPOT 差异。

## Envíe el producto .

> **【拓展：SLO 设定与 Goodput 门控】**2026 años de recomendación de 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 tokens 输出)、Goodput 目标 >= 99%。Enterprise level SLO 收紧 TTFT(200-400ms) pero放宽 E2E──关键实践:(1) En el CI/CD central gate 部署决策于 Goodput value而非吞吐量;(2) 用 2x峰并发行基准测试;(((运行 30-50次取百分位数;(4) 发布时标标工具名、版本、模型、硬件、发发数、代提示分布.

Esta lección produce`outputs/skill-slo-goodput-gate.md`. Dada la carga de trabajo y la SLO, produce una receta de referencia de CI/CD que se utiliza en las puertas de buen rendimiento en lugar de en el rendimiento.

> 本课产 出  `outputs/skill-slo-goodput-gate.md` Dado una carga de trabajo determinada y un SLO, genera un programa de prueba de base de CI/CD, con Goodput y no de desglose como control de la implementación.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Cómo cambia el goodput cuando se apreta el P99 TPOT de 30 ms a 15 ms?
   Traducción:运行`code/main.py` generación con un 1% de distribución de punta de la parte final  Cuando P99 TPOT de 30ms 收紧到15ms 时 Goodput 如何变化?
2. Un vendedor cita "15,000 tok/s en Llama 3.3 70B H100". Nombre tres preguntas que hacer antes de confiar en él.
   En el caso de los servicios de suministro, el precio de la oferta es de 15 mil toneladas.
3. ¿Por qué el preempleo en pedazos protege a P99 TPOT pero no a TPOT?
   Por qué no proteger el valor medio de la TPOT?
4. Construir un SLO de consumo para un asistente de voz (el primer token se escucha, no se lee). ¿Cuál métrica es más visible para el usuario?
   China: 语音助手构建消费级 SLO (en inglés: 语音助手构建消费级 SLO) 首代标是听到而非读到) ◊ ¿Cuál es el indicador más visible para el usuario?
5. Lea los documentos LLMPerf README y GenAI-Perf. Identifique otras tres métricas en las que las herramientas no estén de acuerdo.
   En el caso de los países de la Unión Europea, el número de países de la UE en el sector de la seguridad social es de 1.4% en el caso de los países de la UE.

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Más Leer más Leer más

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) definición canónica de TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) definiciones alternativas y receta de medición.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) medición aplicada en los despliegues reales.
- [LLMPerf](https://github.com/ray-project/llmperf) Indicador de referencia de código abierto basado en ray.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md) La herramienta de referencia de NVIDIA.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) el índice de referencia basado en el buen rendimiento aceptado por la industria.
