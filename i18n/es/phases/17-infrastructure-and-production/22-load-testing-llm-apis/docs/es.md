# Load Testing LLM APIs  Por qué K6 y Locust mienten  load test API por qué LLM  Estados Unidos

> Los probadores de carga tradicionales no fueron diseñados para respuestas de transmisión, longitudes de salida variables, métricas de nivel de token o saturación de GPU. Dos trampas mueren a la mayoría de los equipos. La trampa GIL: La medición a nivel de tokens de Locust ejecuta tokenización bajo el Python GIL, que compite con la generación de solicitudes bajo una concurrencia pesada; el backlog de tokenización luego infla la latencia entre tokens reportada  su cliente es el cuello de botella, no el servidor. La trampa de uniformidad de la señal: las instrucciones idénticas en un bucle prueban un punto en la distribución de los tokens; el tráfico real tiene longitud variable y coincidencias de prefijos diversas. LLMPerf arregla esto con `--mean-input-tokens`¿ Qué es eso ?`--stddev-input-tokens`. Mapeo de herramientas en 2026: especializada en LLM (GenAI-Perf, LLMPerf, LLM-Locust, guidelellm) para la precisión a nivel de tokens; **k6 v2026.1.0**¿ Qué es eso ?**k6 Operator 1.0 GA (Sept 2025)** streaming-consciente, Kubernetes nativo distribuido a través de TestRun/PrivateLoadZone CRDs, mejor para puertas CI/CD; Vegeta for Go saturación de tasa constante; Locust 2.43.3 solo con extensión LLM-Locust para streaming. patrones de carga: estado estable, rampa, punta (test de autoescalado), remojo (vacificaciones de memoria).

> **【中文解读】**Este capítulo presenta el método de prueba de la API de LLM  carga de prueba  evaluación de la evaluación de la aplicación de servicios en alta carga 


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·08(指标) 、Fase 17·03(GPU 扩缩) ──传统负载测试器不为流式响应+变长输出设计──
> ¿ Qué es esto ?**【类比】**LLM 负载测试 = "测自动驾驶 vs 测传统车"──两个陷:(1) GIL 陷:Locust 在Python GIL 下做代币化,与请求生成抢锁→报告的代币 间延迟虚高(客户端是瓶不是服务端);(2) Prompt 一致性陷:循环同样提示 只测分布一个点,真流量有多样化前匹配──LLMPerf 用`--mean-input-tokens+stddev`修复──2026 工具:GenAI-Perf/LLMPerf/LLM-Locust(LLM 专用) + k6 v2026.1(流式+K8s) + Vegeta(Go 常速率) + Locust(仅配 LLM-Locust 扩展)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objetivos de aprendizaje

- Explique los dos patrones anti-impulsivos (trampa GIL, trampa de uniformidad de la rapidez) que hacen que los probadores de carga genéricos se encuentren en las API de LLM.
  La traducción de la traducción de la lengua inglesa en inglés es traducida en inglés como "GIL" (GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en inglés: GIL) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en)) (en) (en)) (en)) (en) (en)) (en) (en)) (en)) (en)) (en) (en)) (en)) (en)) (en)
- Seleccione una herramienta para un propósito determinado: LLMPerf (corrido de referencia), k6 + extensión de transmisión (puerta CI), guidellm (síntesis a gran escala), GenAI-Perf (referencia NVIDIA).
  En inglés, el lenguaje de la lengua árabe es el lenguaje de la lengua árabe.
- Diseñe cuatro patrones de carga (estables, rampa, punta, remojo) y nombre el modo de falla de cada captura.
  En el texto original, el texto se basa en el texto de la traducción de la lengua inglesa.
- Construir una distribución realista de la cuenta de espera utilizando el promedio + stddev de tokens de entrada en lugar de longitud fija.
  En inglés, el símbolo de entrada es un símbolo de distribución real, y no de longitud fija.

## El problema es la introducción del problema

> **【中文解读】**传统负载测试工具不是为LLM设计的它们不支持流式响应、可变输出长度、代码级指标或GPU 和度。 dos comunes trampas:(1) GIL 陷Locust 代码级测量在Python GIL 下运行分词,高并发时代代码化 队列膨胀,虚报互代码延迟((tu cliente端是瓶,不是服务器);2) 均性陷循环测试中使用相同提示,前缓存中提示率接近100%,吞吐量看起来很好但完全不反映真实流量──

> **【拓展：LLM 负载测试的四种模式】**2026 años LLM  carga de pruebas de cuatro modos: 1) 稳态(steady-state) 恒定 RPS 持续30-60分钟,捕获基线性能退化; 2) 渐增) ramp) 从0 线性增加到目标 RPS,捕获容量断点和预热异常; 3) 突发(spike) 突然3-10x RPS 持续2分钟然后回落,测试自动扩张响应、队列和和和冷启动影响; 4) 时间(稳态持续4-8小时,捕获内存漏漏、连接池漂移和可观测性溢出.

Probaste tu punto final de LLM en 500 usuarios simultáneos, lo conseguiste, lo enviaste, en producción en 200 usuarios reales el servicio cayó sobre P99 TTFT explotó, las GPUs se engancharon.

Dos cosas sucedieron. Primero, k6 envió 500 instrucciones idénticas  tu recopilación de solicitudes y caché de prefijos hizo que pareciera que estabas manejando 500 decodificadores simultáneos cuando realmente manejabas uno. Segundo, k6 no rastrea la latencia entre tokens en las respuestas de transmisión de la manera en que el ojo lo experimenta; ve una conexión HTTP, no 500 tokens llegando a intervalos variables.

Las pruebas de carga para LLM son su propia disciplina.

## El concepto central.

### La trampa de la GIL (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】**Python GIL(全局解释器锁) Impacto de los ensayos de carga en el LLM:Locust utiliza Python 运行客户端分词,在高并发时代代代码化 队列排在请求生成后面―― 报告的间代码 延迟包含客户端代码化 积压你以为是服务器慢,其实是测试工具的瓶──解决方案:(1) LLM-Locust 扩展将代码化 移到独立进程;(2) 使用编译语言工具k6kk) rfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

Locust utiliza Python y ejecuta tokenización del lado del cliente bajo el GIL. Bajo alta concurrencia las colas de tokenización detrás de la generación de solicitudes. La latencia entre tokens reportada incluye el backlog de tokenización del lado del cliente.

Corrección: La extensión de LLM-Locust traslada la tokenización a procesos separados, o utiliza un arnés de lenguaje compilado (k6, LLMPerf usando tokenizers.rs).

### La trampa de la uniformidad rápida

Todos los probadores de carga conocidos le permiten configurar un solo prompt. En una prueba de bucle de 10.000 iteraciones el mismo prompt se envía cada vez. El servidor ve el mismo prefijo cada vez que el prefijo  caché se acerca al 100%, el rendimiento se ve muy bien.

Corrección: muestra de una distribución rápida.`--mean-input-tokens 500 --stddev-input-tokens 150` diferentes longitudes, contenido diverso.

### Cuatro patrones de carga

1. **Steady-state** RPS constante durante 30 a 60 minutos.
2. **Ramp** aumentar linealmente el RPS de 0 a la meta durante 15 minutos.
3. **Spike** repentina 3-10 veces RPS durante 2 minutos y luego atrás.
4. **Soak** estado de estabilidad durante 4-8 horas. Captura: fugas de memoria, deriva del pool de conexión, sobrecarga de observabilidad.

### 2026 cartografía de herramientas

> **【中文解读】**2026 años LLM 负载测试工具选择:(1) LLMPerf(Anyscale)Rust-backed 分词 + 流式感知,性能测试的默认选择;(2) NVIDIA GenAI-PerfNVIDIA 参考工具,注意其 ITL 不含 TTFT;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;(4) k6 v2026.1.0 + k6 Operador 1.0 GA(2025 年 9 月) Go编译、无 GIL、流式、知感ernetes-native 分布测试,CI/CD gate 最佳选择──

> **【拓展：CI/CD 中的 SLA Gate】**En el CI utilizar la puerta de SLA de k6  Configuración: por PR 运行 30-50 次代,gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在值以下──违规则构建失败──使用真实提示分布(mean + stddev of input tokens)而非固定长度LLMPerf 使用`--mean-input-tokens 500 --stddev-input-tokens 150`¿Qué es esto?

**LLMPerf**(Anyscale)  Python pero tokenization respaldado por Rust. Mediano / stddev instrucciones. stream-consciente. Mejor predeterminado para ejecuciones de rendimiento.

**NVIDIA GenAI-Perf** NVIDIA. Utiliza el cliente Triton; cobertura métrica completa. Nota su ITL excluye TTFT; LLMPerf incluye. Dos herramientas producen TPOT diferentes para el mismo servidor.

**LLM-Locust**Extensión de langosta que arregla la trampa GIL.

**guidellm** Comparativo sintético a gran escala.

**k6 v2026.1.0**¿ Qué es eso ?**k6 Operator 1.0 GA (Sept 2025)**¿Qué es esto ?
- k6 mismo (Go, compilado, sin GIL) añadió métricas de transmisión conscientes.
- k6 El operador utiliza los CRD de TestRun / PrivateLoadZone para las pruebas distribuidas nativas de Kubernetes.
- Lo mejor para las puertas CI/CD y las pruebas SLA.

**Vegeta** Go, más simple que k6. Saturación HTTP de tasa constante. No es consciente de LLM, pero es bueno para las pruebas de gateway / límite de tasa.

**Locust 2.43.3 stock** tiene la trampa GIL para LLM. Sólo con extensión LLM-Locust.

### Puerta de SLA en CI

Ejecutar el K6 en la PR con:

- 30-50 iteraciones cada una en el RPS de referencia.
- Puerta: P50/P95 TTFT, 5xx < 5%, TPOT por debajo del umbral.
- Rompe la construcción en la brecha.

### Distribución rápida realista

Construir a partir de muestras reales de tráfico (si las tiene) o de distribuciones publicadas (por ejemplo, ShareGPT solicitudes para el chat, HumanEval para el código).

### Números que debes recordar

- k6 Operador 1.0 GA: septiembre de 2025.
- k6 v2026.1.0: métricas de transmisión conscientes.
- Tipo de LLMPerf: 100-1000 solicitudes en la concurrencia X.
- Puerta de CI típica: 30-50 iteraciones por PR.
- Cuatro patrones: estable, rampa, punta, remojo.

## Usalo con el marco de ejecución
```figure
load-pattern-waves
```

## Usalo

`code/main.py`simula una prueba de carga con una distribución realista de la velocidad, mide el TPOT efectivo y demuestra la trampa de velocidad uniforme.

> `code/main.py`simula una prueba de carga con una distribución realista de la velocidad, mide el TPOT efectivo y demuestra la trampa de velocidad uniforme.

> `code/main.py`simula una prueba de carga con una distribución realista de la velocidad, mide el TPOT efectivo y demuestra la trampa de velocidad uniforme.

## Envíe el producto .

Esta lección produce`outputs/skill-load-test-plan.md`. Dado la carga de trabajo y el SLA, elige la herramienta y diseña los cuatro patrones de carga.

> 本课产 出  `outputs/skill-load-test-plan.md`. Dado la carga de trabajo y el SLA, elige la herramienta y diseña los cuatro patrones de carga.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Comparar distribución uniforme vs realista ¿dónde está la brecha?
   Traducción:运行`code/main.py`◊ Comparación media vs verdadera distribución P99 TTFT  Diferencia en dónde?
2. Escriba el guión k6 para una puerta CI: TTFT P95 < 800 ms a 100 concurrencias, tiempo de ejecución 5 minutos.
   Cien: C.I. 门控的 k6 脚本:100 并发下 TTFT P95 < 800ms,运行 5 分钟──
3. Su prueba de remojo muestra que la memoria crece 50 MB/hora. Nombre tres causas y el instrumento para elegir entre ellos.
   Su inmersión muestra un aumento de 50 MB de memoria por hora.
4. Prueba de punta de 10 RPS a 100 RPS. ¿Cuál es el tiempo de recuperación esperado si se está en marcha la pila de producción Karpenter + vLLM (fase 17 · 03 + 18)?
   China 翻译: de 10 RPS 尖峰测试到 100 RPS── Si Karpenter 需要45秒供应,预期恢复时间是多少?
5. GenAI-Perf informa TPOT=6ms; LLMPerf informa TPOT=11ms en el mismo servidor.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Más Leer más Leer más

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
