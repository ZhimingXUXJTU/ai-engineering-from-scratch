# EAGLE-3 Descodación especulativa en producción

> La descifrado especulativo combina un modelo de proyecto rápido con el modelo objetivo. El proyecto propone tokens K; el objetivo se verifica en un solo plazo; los tokens aceptados son gratuitos. En 2026, EAGLE-3 es la variante de grado de producción  que entrena a un draft head en los estados ocultos del modelo objetivo en lugar de en tokens crudos, empujando la tasa de aceptación alfa en la banda de 0.6-0.8 en el chat general. La pregunta correcta no es "qué tan rápido es el borrador" sino "qué es el alfa en mi tráfico?" Si el alfa cae por debajo de ~0.55, la descifrado especulativo es negativo neto a alta concurrencia porque cada borrador rechazado cuesta un segundo pase al frente objetivo. Esta lección te enseña a medir el alfa primero y a voltear la bandera segundo.

> **【中文解读】**Este capítulo presenta la técnica de la teoría de la aceleración de la teoría con un pequeño modelo.
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 、Fase 10·18(MTP 多代币预测) 、Fase 10·25(投机解码原理) ⋅本节是生产版 EAGLE-3。
> ¿ Qué es esto ?**【类比】**EAGLE-3 = "traducer打草稿"──草稿模型(draft) rápidamente adivina K 个代币,目标模型一次验证──猜对=免费,猜错=多一次验证开销──EAGLE-3 创新:用目标模型隐藏状态训练草案(而不是原始代币), aceptación tasa α 提到 0.6-0.8──生产关键问题:α 在你的流量上多少?<0.55 时反而拖慢(拒绝的草案 浪费计算力)必须先测α 再开旗──
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Nombre de las tres generaciones de descifrado especulativo y explicar qué cambios EAGLE-3 de EAGLE-2 y de un modelo clásico de proyecto.
  China Translation: 说出推测解码的三代,并解释 EAGLE-3 相比Eagle-2 和经典草案 模型改变了什么──
- Definir la tasa de aceptación alfa, calcular la velocidad esperada de alfa y K (duración del borrador), e identificar el alfa de equilibrio para su concurrencia objetivo.
  La tasa de aceptación de la tasa de alfántica, del alfabeto y del K (descripción de la longitud) calcula la tasa de aceleración de la tasa de pérdida, y determina la tasa de pérdida del objetivo y la tasa de pérdida del alfabeto.
- Explica por qué la descodificación especulativa es opt-in (no por defecto) en vLLM 2026 y por qué activarla sin medir alfa es un antipatrón de producción.
  China Translation: explica por qué la propuesta de resolución en 2026 vLLM en el medio de la opción de no-defusión), así como por qué no se mide alfa en el inicio de la producción en el modo de la producción.
- Escriba un plan de medición: qué índice de referencia, qué distribución de datos, qué punto de concurrencia, qué métrica para entrar.
  China: 写出测量计划:哪个基准测试、哪个快点 分布、哪个并发点、哪个指标作为门控──

## El problema es la introducción del problema

> **【中文解读】**推理的解码阶段是内存带宽限定的每解码一个代币 需要读取约140GB/s的权重,GPU 计算几乎空──推测解码利用这个空: Utilizando un pequeño modelo barato para generar K 个候选代币, luego hacer que el modelo objetivo verifique todas las K 个体 una vez más en una transmisión hacia adelante.  Acceptar la tasa alfa es el único indicador importante  cuando se genera un código de alta y baja calidad                                                                                                                                                                                                   

> **【拓展：推测解码的产业应用】**Google en 2025 propondrá la implementación de código de inteligencia artificial (AI) en las revisiones generales de los motores de búsqueda, en un contexto de no pérdida de calidad, ha acelerado significativamente la velocidad de respuesta.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补充全(延迟敏感)场景──但需要注意:高并发(256+)

El decodificación es de memoria. En un H100 que ejecuta Llama 3.3 70B FP8, cada token decodificado lee ~140 GB / s de pesos y emite un token. El cálculo de la GPU es casi ocioso durante el decodificación.

> 解码是内存限定的──在 H100 上运行 Llama 3.3 70B FP8 时, cada token de resolución 读取约140 GB/s de peso y输出一个 token──GPU 计算在解码期间几乎空瓶是HBM 带宽,而不是矩阵乘吞吐量──

La descifrado especulativo explota la brecha. Generar tokens candidatos K con un modelo de borrador barato, luego pedir al modelo objetivo para verificar todos K en un solo pase hacia adelante. Cada token verificado es efectivamente libre (amortizado en un lote de K hacia adelante el objetivo habría tenido que hacer de todos modos).

> 推测解码利用这个差距――Utiliza un proyecto barato 模型 generar K 个候选标记, luego hacer que el modelo objetivo verifique todos los K 个在一次前向传播中.

El enfoque clásico del modelo de proyecto utiliza un modelo más pequeño de la misma familia (Llama 3.2 1B redacción para Llama 3.3 70B). Funciona pero la tasa de aceptación es mediocre  la distribución del modelo más pequeña difiere del objetivo. EAGLE, luego EAGLE-2, luego EAGLE-3 entrenan una cabeza de proyección ligera directamente en los estados internos del modelo objetivo, por lo que la distribución del proyección rastrea el objetivo mucho más de cerca. Por eso el alfa pasa de 0.4 con el modelo de proyecto a 0.6-0.8 con EAGLE-3.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为 Llama 3.3 70B做草案) ―― es posible pero aceptable tasa de distribución de modelos más pequeños de la misma línea de distribución.

El objetivo: EAGLE-3 se ha optado por el VLLM 2026. `speculative_config`Los equipos que lo encienden sin medir el tráfico real a menudo ven que la latencia de cola empeora, no mejora.

> 关键点:EAGLE-3 en 2026 VLLM en el centro es opt-in de la`speculative_config`必須顯示設定──無標志,就沒有加速──不測真流量 alfa 就開啟的團隊常見尾部延遲變差而不是改善──

## El concepto central.

### ¿Qué es la descifrado especulativo realmente compra

> **【中文解读】**推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)` Para K=5, alfa=0.7, la aceleración teórica es de 4.1x. Pero en la producción real suele alcanzar sólo 2-3x, ya que el alfa en el flujo real alcanza muy poco más de 0.7, y la producción de alta cantidad de lote aumenta cuando se produce más.

Sin el decodificación de especificaciones, el costo por token es un objetivo hacia adelante.`1 + K * alpha`El acelerador es`(1 + K * alpha) / (1 + epsilon)`donde epsilon es el costo general de la verificación de proyectos. para K=5, alfa=0.7: `(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`Los números del mundo real se agrupan alrededor de 2-3 veces porque el alfa rara vez es tan alto en el tráfico de producción y el epsilon crece en grandes cantidades de lote.

> 没有推测解码时,每次目标前向传播的成本. 有推测解码时,草案 长度 K 和接受率 alpha 下,每次目标前向的预期代币 数为`1 + K * alpha`◊ acelerar`(1 + K * alpha) / (1 + epsilon)`, de los cuales el epsilón es el borrador + 验证开销── para K=5, alfa=0.7:`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`◊ En realidad, la concentración de datos es de 2-3 veces mayor, ya que el alfa en el flujo de producción es muy pequeño y el epsilon en el tamaño de lote más alto aumenta.

### ¿Por qué alfa es la única métrica que importa?

Los tokens rechazados no desaparecen  obligan a un segundo objetivo a avanzar para el primer token rechazado. En una carga de trabajo donde el alfa baja a 0,4, pagas gastos generales de proyecto más verificación más re-roll. En alta concurrencia (digamos 256 concurrencias), el lote de decodificación ya es lo suficientemente grande como para que la brecha de ancho de banda de memoria entre "target solo" y "target con verificar" se reduzca. Por debajo de alfa 0.55 en la mayoría de los equipos de 2026, el código de especificaciones es negativo neto.

> Los tokens rechazados no desaparecerán  se obligan a la primera token rechazada  a realizar un segundo objetivo de propagación  en la carga de trabajo de alfa  bajando a 0.4, usted paga un proyecto 开销 + 验证 + 重新生成 en el alta并发 (como 256并发) , el bloque de descifrado ya es lo suficientemente grande, la brecha de banda ancha de memoria entre "单独目标" y "带验证目标" se reduce  en la mayoría de los equipos de 2026 , alfa 低于 0.55 时推测解码是净负面的

En el chat general de estilo ShareGPT, EAGLE-3 entrenado en ShareGPT alcanza 0.6-0.8. En el tráfico específico del dominio (código, médico, legal) el jefe de redacción entrenado en datos generales cae a 0.4-0.6.

> Alpha 因工作负载而异. En el estilo de la conversación general de ShareGPT, con EAGLE-3 de la capacitación ShareGPT  alcanzar 0.6-0.8 ⋅ en un flujo específico de código 医疗、法律) en el campo, con la cabeza de proyecto de la capacitación general de datos 降至 0.4-0.6 ⋅ en el campo de capacitación, la cabeza de proyecto específica puede recuperar la comparación de alfa con el objetivo de la capacitación, es una tarea de capacitación de la velocidad.

### Las generaciones de águila en un vistazo

> **【中文解读】**推测解码经历了三代演进:(1) El modelo de borrador clásico(same serie de pequeños modelos,alpha 0.3-0.5) simple pero bajo porcentaje de aceptación;(2) EAGLE-1/2(en el estado oculto del modelo objetivo entrenar el jefe de borrador,alpha 0.5-0.7) mayor porcentaje de aceptación;(3) EAGLE-3(en el estado oculto de múltiples niveles entrenar,alpha 0.6-0.8)2025-2026 años de producción.

> **【拓展：推测解码 vs 其他加速技术】**LLM 推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速, necesita extra cabeza de proyecto;(2) 量化(INT8/FP8) 推理加速 1.5-2x, tiene poca pérdida de calidad;(3) 分块预填降低ITL尾但不直接提升吞吐;(4) 分分式预填/解码消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──

- **Classic draft model**Alfabeto 0.3-0.5 Infraestructura simple  dos modelos cargados, proyecto de ejecuciones K hacia adelante por objetivo hacia adelante.
  En inglés:**经典 draft 模型**:同系列的小模型──Alpha 0.3-0.5──基础设施简单加载两个模型,草案 每次目标前向运行 K 次前向──
- **EAGLE-1 (2024)**Alfa ~ 0,5-0,6 . Un pequeño parámetro sobre la parte superior del objetivo.
  En inglés:**EAGLE-1 (2024)**En el estado oculto del objetivo, el grupo de entrenamiento de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de la capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación de capacitación
- **EAGLE-2 (2025)**Alfabeto de la línea de referencia: longitud de borrador adaptativa y borradores basados en árboles (verifique múltiples ramas en un solo paso objetivo).
  En inglés:**EAGLE-2 (2025)**El proyecto de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de la organización de la organización de la organización de las organizaciones de la organización de las organizaciones de la organización de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de las organizaciones de las organizaciones de la comunidad de las organizaciones de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de
- **EAGLE-3 (2025-2026)**Allí se puede encontrar un equipo de entrenamiento de la cabeza de proyecto en múltiples capas de objetivo (no sólo las últimas), mejor alineación.
  En inglés:**EAGLE-3 (2025-2026)**En el último nivel de entrenamiento, el jefe de reclutamiento es mejor para el equipo.

### La receta de producción para 2026

> **【中文解读】**El proceso de implementación de EAGLE-3 en el medio ambiente es de cinco pasos: 1) primero en base al modelo de base, establecer TTFT/ITL/吞吐量基线; 2) activar el proyecto de EAGLE-3 配置; 3) controlar la tasa de aceptación alfavLLM V1 通过`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) Si alfa < 0.55,禁用推测解码或训练领域特定草案头;(5) 在生产并发水平重新测试,确认 P99 ITL 没有恶化──

1. Modelo de navegación objetivo claro. Medir el TTFT de referencia, ITL, rendimiento en la concurrencia objetivo.
   En el caso de los modelos de base, el método de medición de la base de datos es el método de medición de la base de datos.
2. Habilitar el borrador EAGLE-3 a través de vLLM `speculative_config`- Re-examinar el índice de referencia.
   En inglés:`speculative_config`Initiar el proyecto EAGLE-3― re-encargar el proyecto de evaluación de base―
3. Taxa de aceptación de registros alfa. vLLM V1 informa esto como `spec_decode_metrics.accepted_tokens_per_request`Dividir por la longitud del borrador solicitado para obtener el alfa.
   En inglés, el número de personas que han recibido el certificado de reconocimiento de la identidad de los datos de la empresa es el número de personas que han recibido el certificado de reconocimiento de la identidad de los datos.`spec_decode_metrics.accepted_tokens_per_request`報告──除以要求草案 长度得到 alpha──
4. Si el alfa < 0,55 en la distribución del tráfico de producción, deshabilitar la descifrado de especificaciones o entrenar un borrador EAGLE-3 específico de dominio.
   Si la distribución de la producción de flujo en alfa < 0.55, no se puede usar el proyecto EAGLE-3 específico en el campo de entrenamiento.
5. Con la producción simultánea, vuelva a ejecutarse.
   En la producción y en la producción, el proceso de re-evaluación se ha desarrollado.

### El punto de pérdida de producción: cola P99

El P99 puede empeorar si no se sintoniza. Los proyectos rechazados desencadenan una secuencia de dos pases (proyecto + verificación-fallo + re-rollo).

> 平均 ITL 随推测解码下降──如果不调优,P99可能恶化──被拒绝的草案 触发两次传递序列(草案 + 验证失败 + 重新生成)──在满批次下,这两次传递串行化──关注 P99 ITL,而不是 P50──

### Cuando EAGLE-3 ya esté desplegado

Google desplegó la descodificación especulativa en AI Overviews en 2025 (la misma calidad, respuesta más rápida). vLLM V1 barcos `speculative_config`como la interfaz documentada; la descifrado especulativo de GPU de N-gram en V1 es la variante compatible con preempleo en pedazos. SGLang admite EAGLE-3 como la ruta de proyecto recomendada para cargas de trabajo pesadas de prefijos.

> Google en 2025 se propondrá a la implementación de código de inteligencia artificial en revisiones de la misma calidad, más rápido responder)`speculative_config`作为档档化接口;V1 中的N-gram GPU 推测解码是与分块预填充兼容的变体──SGLang 支持EAGLE-3 作为前密集工作负载的推草案路径──

### Matemáticas de equilibrio en una línea

Aceleración esperada: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`- Configuración .`S = 1`soluciones para alfa: `alpha_breakeven = verify_overhead / K`. Para los gastos de verificación típicos ~0.15 y K=5: `alpha_breakeven = 0.03`Pero eso es la matemática de decodificación crudo. A alta concurrencia el overhead de verificación aumenta y el lote de decodificación ya amortiza las lecturas de memoria a través de las secuencias, por lo que el alfa_breakeven efectivo sube a ~0.45-0.55 en la práctica.

> 预期 aceleración比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`。设 `S = 1`求解 alfa:`alpha_breakeven = verify_overhead / K` típico control sobrecargo 约0.15,K=5:`alpha_breakeven = 0.03`▽ pero eso es el principio de la matemática. En el proceso de desarrollo, la cantidad de unidades de cálculo aumentó, y la cantidad de unidades de cálculo se ha acumulado en la secuencia de distribución.

### Cuando no utilizar la descifrado especulativo

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 concurrent) 内存带宽差距大,收益明显。 在以下场景应避免:(1) 批量离线生成延迟不重要,使用平面目标;(2) 短输出< 50 tokens) 草案 开销和验证成本主导;(3) 专业领域无领域训练的草案) alpha 太;(4) vLLM v0.18.0 + 草案-model + 零碎-pre-model + 组合 兼容.

> **【拓展：vLLM 推测解码配置】**vLLM V1 支持三种推测解码模式:(1) Draft model传统小模型作为草案,与零碎预填不兼容;(2) EAGLE在隐状态训练的草案头,推用于通用场景;(3) N-gram GPU基于提示 中 N-gram 查找的 GPU端草案,是唯一与零碎预填 兼容的模式──`speculative_config`必須明顯設定,vLLM 默认不開任何推测解码──

- Generación de batch-1 sin conexión donde la latencia no importa.
  China:延迟无关紧要的批量为 1 的离线生成――使用普通目标模型――
- Los resultados son muy cortos (menos de 50 tokens).
  Traducción: muy corta de la producción de 50 tokens (en inglés: 50 tokens)
- Dominio especializado sin un jefe de reclutamiento entrenado.
  No hay ningún campo de entrenamiento del jefe de proyecto.
- vLLM v0.18.0 más el código de especificaciones del modelo de proyecto más `--enable-chunked-prefill`Esta combinación no se compiló. La excepción documentada es el decodificación de especificaciones de GPU de N-gram en V1.
  中文翻译:vLLM v0.18.0 + modelo de proyecto 推测解码 + `--enable-chunked-prefill` Este conjunto no puede ser compilado. 文档例外是V1 中的N-gram GPU 推测解码.

## Usalo con el marco de ejecución
```figure
mx-speculative-tree
```

## Usalo

`code/main.py`simula un bucle de decodificación con y sin decodificación especulativa en una gama de valores alfa y longitudes de borrador K. Imprime el break-even alfa, la velocidad medida y el comportamiento de cola.

> `code/main.py`模拟有/无推测解码的解码循环,覆盖一系列 alpha 值和草案 长度 K――它印打亏平衡 alpha、测量加速比和尾部行为──在多个 (alfa, K) 组合上运行,精确看推测解码在哪里停止收益──

## Envíe el producto .

Esta lección produce`outputs/skill-eagle3-rollout.md`. Dado un modelo objetivo, una descripción de la distribución del tráfico y un objetivo de concurrencia, produce un plan de implementación EAGLE-3 en etapas  referencia de referencia, habilita la configuración, la medida alfa, la puerta en alfa >= 0.55, ver P99 ITL.

> 本课产 出  `outputs/skill-eagle3-rollout.md` dado un modelo de objetivo  descripción de distribución de flujo y desarrollo de objetivos, que genera una fase de EAGLE-3  lanzamiento de un plan  base de datos  activación de la configuración  medición alfa  alfa >= 0.55    control de la entrada  atención P99 ITL 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Qué alfa necesitas para un 2x de aceleración? ¿Para un 3x de aceleración? ¿Qué tan sensible es eso para verificar_overhead?
   Traducción:运行`code/main.py`¿Qué es lo que hace que el control de velocidad sea más sensible?
2. Imagínese que el tráfico de producción divide el 70% de chat general, el 30% de código. El chat general alcanza el alfa 0.7 con EAGLE-3 entrenado en ShareGPT; el código alcanza el alfa 0.4. ¿Qué es alfa mezclado y es el código de descodación de especificaciones net-positivo?
   En inglés, el número de personas que producen el producto es de aproximadamente un 70% y el número de personas que producen el producto es de aproximadamente un 30% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 40% y el número de personas que producen el producto es de aproximadamente un 50% y el número de personas que producen el producto es de aproximadamente un 50% y el número de personas que producen el producto es de aproximadamente un 50% y el número de personas que producen el producto es de aproximadamente un 50% y el mismo.
3. Lea el VLLM `speculative_config`En el caso de los Estados miembros, el número de datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los que se han introducción de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los
   En inglés:`speculative_config`文档──说出三种模式(Módulo de proyecto、EAGLE、N-gram)及哪个与分块预填兼容──
4. Vemos que la media ITL cayó un 25% después de habilitar EAGLE-3 pero P99 ITL subió un 15%.
   China: en el caso de las empresas de alta tecnología, el nivel de la ITL se reduce de un 25% pero el nivel de la ITL de P99 se eleva de un 15%.
5. Calcule el costo de memoria de la cabeza de proyección EAGLE-3 para Llama 3.3 70B. ¿Cómo se compara con ejecutar Llama 3.2 1B como un proyecto clásico?
   El proyecto de EAGLE-3 de Llama 3.3 70B fue publicado en el periódico Llama 3.2 1B.

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Más Leer más Leer más

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) fuente autorizada en `speculative_config`y compatibilidad de preempleo en V1.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) el conjunto exacto de campos.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) formulación original de la cabeza de proyecto de EAGLE.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) proyectos y árboles adaptativos.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) Sistema de LLM eficiente con decodificación especulativa.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) Lista de control de la implementación de la producción.
