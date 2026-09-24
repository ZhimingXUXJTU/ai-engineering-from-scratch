# TensorRT-LLM en Blackwell con FP8 y NVFP4
# Compilación de inferencias especializadas en hardware  FP8 y NVFP4 en Blackwell

> La compilación de inferencias especializada en hardware comercializa la portabilidad para el rendimiento, y TensorRT-LLM  NVIDIA-sólo, sintonizado para Blackwell  es el ejemplo más claro del comercio que da frutos.$0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0,09/M en H100 + VLLM  una brecha económica de 7 veces. La pila es de tres regímenes de puntos flotantes compuestos: FP8 se mantiene crítico para los kernels de caché y atención KV porque tiene el rango dinámico que necesitan; NVFP4 (4 bits de microscalación) maneja pesos y activaciones; predicción multi-token (MTP) y prefill / decode desglosado añaden otros 2-3x en la parte superior. El modelo de soporte de día-0 carga directamente los pesos de FP4 sin conversión post-entrenamiento. La captura para los equipos de ingeniería de 2026: TRT-LLM es de código abierto pero específico de NVIDIA  CUDA- y Blackwell-especializado  así que la adopción de la trata de la portabilidad para el rendimiento. Ejecutar las matemáticas de su mezcla de modelos y hardware antes de comprometerse.

> **【中文解读】**Este capítulo presentaba el LLM de TensorRT-LLM y BlackwellNVIDIA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 、Fase 10·13(量化基础) ・・・TensorRT-LLM es NVIDIA 专属优化, en Blackwell GPU 上性能最强──
> ¿ Qué es esto ?**【类比】**TensorRT-LLM = "NVIDIA 专属跑车"―GB200 NVL72 上 SemiAnálisis 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7 倍经济性差距──三套浮点叠加:FP8(KV cache+attention 动态范围) + NVFP4(4-bit 权重激活) + MTP/解 prefill-decode 再加 2-3 倍──代价:闭源 NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合算账──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Explica por qué FP8 sigue siendo fundamental para la memoria caché y la atención de KV incluso cuando los pesos están en NVFP4.
  Traducción: Explicación por qué incluso en NVFP4, el peso de la FP8 sigue siendo clave para el almacenamiento y la atención de KV.
- Calcule la huella de HBM de un modelo fronterizo bajo BF16, FP8 y NVFP4 y razone de dónde provienen los ahorros.
  En el caso de los modelos de la HBM, el uso de la HBM en el BF16 FP8 y NVFP4 ⇒
- Nombre de las características específicas de Blackwell TRT-LLM exploits (día-0 FP4, MTP, servicio desagregado, primitivos todo a todo).
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión del versión original de la versión del versión del versión original de la versión del versión del versión del versión del versión del versión del versión del versión del versión del versión del versión del versión original de Blackwell.
- Decida cuándo el bloqueo NVIDIA de TRT-LLM vale la diferencia de costo 7x frente a VLLM en Hopper.
  China Translation: decide TRT-LLM de NVIDIA 锁定何时值相比Hopper 上 vLLM de 7x 成本差距──

## El problema es la introducción del problema

> **【中文解读】**La respuesta depende de cuatro niveles de superposición: hardware代际: Hopper H100/H200 vs Blackwell B200/GB200) 精度(BF16 → FP8 → NVFP4) 推理引擎(vLLM vs SGLang vs TRT-LLM) y编排(朴素 vs 分离式 vs Dynamo) ⋅在 Hopper + vLLM 上运行 120B MoE 约$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $0.012/M7x 差距── Este precio de la diferencia es NVIDIA 锁定你不能在其他厂商的硬件上复现──

> **【拓展：NVIDIA Blackwell 架构】**Blackwell(B200/GB200) es una GPU arquitectura lanzada en el año 2024-2025 por NVIDIA, en comparación con Hopper (H100) en LLM 推理 具有11-15x de cada GPU 吞吐提升.

La frontera de la economía de inferencia en 2026 es "cuántos tokens por dólar". La respuesta depende de cuatro opciones apiladas: generación de hardware (Hopper H100/H200 vs Blackwell B200/GB200), precisión (BF16 → FP8 → NVFP4), motor de servicio (vLLM vs SGLang vs TRT-LLM), y orquestación (plain vs disaggregated vs Dynamo).

> La respuesta depende de cuatro superposición de opciones: hardware代际(Hopper vs Blackwell) 精度(BF16 → FP8 → NVFP4) 推理引擎(vLLM vs SGLang vs TRT-LLM) y编排(朴素 vs 分离式 vs Dynamo) ↓

En Hopper con VLLM, un MoE 120B corre a ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$Algunos de esos puntos son hardware (Blackwell es 11-15 veces por CPU LLM en comparación con Hopper). Algunos son la pila: pesos FP4, borrador MTP, preempleo / decodificación desagregado y NVLink 5 todo-a-todo para comunicación de expertos de MoE.

> En Hopper + VLLM 上,120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012便宜 7 倍──部分差距来自硬件(Blackwell vs Hopper Cada GPU LLM 吞吐 11-15 倍)──部分来自:FP4 权重、MTP draft、分离式预填充/解码和 NVLink 5 all-to-all Used for MoE 专家通信──

No se puede replicar esto fuera de la pila de NVIDIA. Ese es el compromiso  portabilidad para la economía. Comprender qué opciones de pila dan qué parte de la brecha es el punto de esta lección.

> Usted no puede reproducir fuera de NVIDIA. Esto es el peso de la capacidad de transferencia de la economía. Comprender qué parte de la diferencia de contribución de la selección es el punto de este curso.

## El concepto central.

### ¿Por qué FP8 sigue siendo el suelo para KV cache

> **【中文解读】**FP8 es el requisito de precisión mínima de KV Cache. El KV Cache  almacenamiento de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la

Un error común en 2026: asumiendo que NVFP4 se aplica en todas partes. No lo hace. El caché KV necesita FP8 (8 bits flotantes) porque almacena claves de atención y valores que abarcan un amplio rango dinámico. Cuantificar KV a FP4 causa una pérdida de precisión catastrófica  la cola de la distribución cae y las puntuaciones de atención se derrumban.

> Un error común del año 2026: supongamos que NVFP4  se aplica a todas las partes. No es de. KV 缓存需要FP8 (en inglés: FP8) 位浮点), ya que el almacenamiento de KV 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到FP4 量化到F 量化到FP 量量到F 量到Figation 量到Figation 量到Figation 量到Figation 量到Figation 量到Figation 量到Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figation Figment

NVFP4 (2025-2026) se aplica a pesas y activaciones. Microscalación: cada bloque de pesas tiene su propio factor de escala para que los bloques pequeños puedan abarcar diferentes rangos dinámicos sin pérdida de escala por tensor. Para las activaciones, FP4 se mantiene porque las activaciones son de pequeño rango dentro de una capa.

> NVFP4 (en inglés NVFP4 (en inglés NVFP4)) se aplica a la carga y la activación.

La configuración típica de Blackwell:

- Peso: NVFP4 (4 bits de microscalación).
  En inglés, el nombre de la palabra "microconcierto" se refiere a la palabra "microconcierto".
- Actividades: NVFP4.
  En el caso de los niños, el número de niños en edad de edad de 5 años es de aproximadamente un millón.
- El caché de KV: FP8.
  En el caso de los niños, el número de niños en edad de edad avanzada es de aproximadamente un millón.
- acumulador de atención: FP32 (estabilidad de máxima suavidad).
  En inglés, el nombre de la persona que está en el centro de la vida es el de la persona que está en el centro de la vida.

### Las primitivas específicas de Blackwell utilizan TRT-LLM

- **Day-0 FP4 weights**Los proveedores de modelos envían directamente pesos FP4; cargas TRT-LLM sin conversión post-entrenamiento.
  En inglés:**Day-0 FP4 权重**El modelo proveedor de FP4 权重;TRT-LLM 无需训练后转换即可载;;FP4 不需要 AWQ/GPTQ 步骤;;
- **Multi-token prediction (MTP)**: la misma idea que EAGLE (fase 17 · 05) pero integrada en la estructura TRT-LLM.
  En inglés:**多 token 预测 (MTP)**La fase 17 · 05), pero se integró en el TRT-LLM 构建中──
- **Disaggregated serving**El proceso de procesamiento de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
  En inglés:**分离式服务**El código de acceso se encuentra en el archivo de datos de la GPU independiente.
- **All-to-all communication primitives**NVLink 5 redujo la latencia de comunicación experta de MoE en 3x frente a Hopper.
  En inglés:**All-to-all 通信原语**El número de comunicaciones de la UE se ha reducido en 3 veces.
- **NVFP4 + MXFP8 microscaling**: manipulación acelerada de factor de escala en los núcleos tensores Blackwell.
  En inglés:**NVFP4 + MXFP8 微缩放**El núcleo de tensión de Blackwell aumenta la velocidad de procesamiento de los componentes.

### Los números que debes memorizar

- HGX B200 a $ 0.02 / M tokens en GPT-OSS-120B a través de TRT-LLM.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- GB200 NVL72 a $ 0,012/M tokens a través de Dynamo (orquestación TRT-LLM).
  La moneda de cambio de la moneda de la moneda de la República es el dólar de la República de China.
- H100 + vLLM ≈ $ 0.09 / M tokens en carga de trabajo comparable.
  H100 + vLLM 在可比工作负载上 alrededor de $0.09 / M tokens。
- El aumento de la capacidad de producción en tres meses de actualizaciones del TRT-LLM (2026) es de 2,8 veces mayor.
  La cantidad de agua que se absorbe en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua en el agua.
- 11-15 veces por CPU LLM de rendimiento, Blackwell vs Hopper.
  Traducción:Blackwell vs Hopper Cada GPU LLM 吞吐量 11-15 倍。
- MLPerf Inference v6.0 (abril 2026): Blackwell domina todas las tareas presentadas.
  En el caso de las misiones de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la misión de la cuyo.

### Cuánto cuesta en realidad el FP4 en calidad

> **【中文解读】**NVFP4 en la teoría de la carga de trabajo intenso ([[思维链]],数学、长上下文代码生成) puede causar una degradación de la calidad visible. Cada bloque de calificación puede aliviarse pero no eliminarse.

> **【拓展：量化精度 vs 推理成本权衡】**La selección de la precisión cuantitativa es el peso de la calidad y el costo: 1) BF16 sin pérdida de calidad, pero la demanda de memoria es grande(70B  modelo necesita 140GB); 2) FP8 casi sin pérdida, Hopper/Blackwell  aceleración de hardware, recomendado para la hipótesis de tareas de tipo intenso; 3) INT4(AWQ/GPTQ) 4-bit  peso, MATH 分数下降 3-5点, adaptado a la conversación general; 4) NVFP4 más activo, Blackwell 专用, must in target evaluation  证券生产中通常混合使用:重度低量、KV Cache FP8──

NVFP4 es agresivo. En cargas de trabajo pesadas de razonamiento (cadena de pensamiento, matemáticas, código-gen con contexto largo), los pesos de FP4 se degradan visiblemente. La calibración por bloque mitigará pero no eliminará. Los modelos de razonamiento de los equipos a menudo utilizan pesos de FP8 + activaciones de FP4 como compromiso, o se adhieren a H200 con FP8 en todo.

> NVFP4 es activado. En la carga de trabajo intenso de la teoría (思维链、数学、长上下文代码生成) en la teoría, el peso de la teoría es evidente.

La regla: siempre valida la calidad de la tarea en su conjunto de evaluaciones antes de comprometerse con pesos NVFP4.

> 规则: siempre en su evaluación en el conjunto de pruebas de la calidad de tarea antes de presentar NVFP4 权重.

### ¿Por qué esta es una decisión de bloqueo de NVIDIA

> **【中文解读】**TRT-LLM es un conjunto de C++ + CUDA + 闭源内核的组合―― los modelos necesitan un SKU específico de GPU 编译―― no admite AMD、Intel o ARM― si su estrategia de infraestructura es multi-proveedor, TRT-LLM  para esta capa es una opción indiscutible todavía puede utilizar vLLM en hardware mixto― pero si es sólo NVIDIA,7x de diferencia económica vale la pena este bloqueo―

> **【拓展：NVIDIA vs AMD 推理生态】**En 2026 la IA  Racificación de chips de mercado: NVIDIA  Gracias a CUDA 生态 y TRT-LLM  ocupará aproximadamente el 80% de la cuota de la racificación de centros de datos. AMD MI300X tiene competencia en la capacidad de cálculo original, pero el software (ROCm + vLLM) sigue al día. Intel Gaudi 3 es otra opción pero su tasa de adopción es menor.

TRT-LLM es un kernel de código cerrado. Los modelos deben compilarse para un SKU específico de GPU. No hay AMD, no hay Intel, no hay ARM. Si su estrategia infra-vendor es multivendor, TRT-LLM es un no-starter para el nivel TRT-LLM-servido.

> TRT-LLM es un conjunto de C++ + CUDA + 闭源内核的组合――模型需要为特定 GPU SKU 编译――不支持 AMD、Intel 或 ARM――如果你的基础设施策略是多供应商,TRT-LLM不可行你仍然可以在混合硬件上使用vLLM──如果你是NVIDIA-only,7x 差距值得这个锁──

### 2026 receta práctica

Para una factura de inferencia anual de $100M +, ejecutar en Hopper + vLLM deja 7-10x en la mesa. Migra las cargas de trabajo dominantes en costos a Blackwell + TRT-LLM + Dynamo. Mantenga el nivel de experimentación en H100 + vLLM para la velocidad de iteración del modelo. Valida la calidad en cada modelo convertido en NVFP4 antes de la producción.

>  Para el gasto anual de $100M+ en el cálculo, en Hopper + vLLM, el funcionamiento significa dejar 7-10 veces más espacio de ahorro.                                                                                                                                                                                                                                            

### El bono de desagregación

La porción desagregada de TRT-LLM (pools separados de preempleo y decodificación) se cubre en profundidad en la fase 17 · 20. En Blackwell, los multiplicadores se apilan: pesos FP4 × aceleramiento MTP × colocación desagregada × enrutamiento consciente de caché.

> La división de servicios de TRT-LLM ([[Independent Prefill and Settlement Pool]]) se desarrolló en la fase 17 · 20 en profundidad de la discusión.

## Usalo con el marco de ejecución

> **【拓展：Blackwell 迁移决策】**Desde Hopper 迁移到Blackwell + TRT-LLM 决策框架:(1) ¿Excede el gasto anual en la investigación de 5 millones de dólares? es→ vale la pena evaluar la investigación de migración;(2) ¿Es posible aceptar la NVIDIA 锁定? es→continuar usando el modelo de Hopper;(3) ¿Contiene la carga de trabajo el modelo de MoE? es→Blackwell NVLink 5 todo a todo  ofrece un adicional 3x de aceleración;(4)  ¿Excede el 30% del gasto en la investigación de tipo intenso? es→Necesita la verificación de la calidad de NVFP4 ⋅ Migración ROI normalmente en 6-12 个月内回本.
```figure
pipeline-parallel
```

## Usalo

`code/main.py`Computa huella HBM, decodificación de rendimiento (regimen de memoria limitada) y $/M-tokens para un modelo en tres pilas: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. ejecuta para ver el efecto de composición y la proporción de la brecha que cada cambio contribuye.

> `code/main.py`計算模型在三个上 HBM 占用、解码吞吐量(内存受限) y $/M-tokens:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行它查看复合效应和每个变化贡献差距份额──

## Envíe el producto .

Esta lección produce`outputs/skill-trtllm-blackwell-advisor.md`. Dada la carga de trabajo, el tamaño del modelo y el volumen anual de tokens, decide si la pila Blackwell + TRT-LLM vale la pena el bloqueo NVIDIA.

> 本课产 出  `outputs/skill-trtllm-blackwell-advisor.md` Dado un determinado trabajo de carga  modelo tamaño y cantidad de tokens anual, que decide Blackwell + TRT-LLM  si vale la pena NVIDIA  bloquear 

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`En un MoE 120B con parámetros activos del 30%, calcular el rendimiento de decodificación limitado de ancho de banda de memoria en H100 BF16, H100 FP8 y B200 NVFP4/FP8. ¿De dónde viene el salto más grande?
   Traducción:运行`code/main.py` En el 30%                                                                                                                                                                                                                                                             
2. Un cliente gasta 2 millones de dólares al año en H100 + vLLM. ¿Cuál es el número de GPUs Blackwell que necesitan comprar para amortizar una migración a TRT-LLM en 12 meses, dada la brecha económica de 7x?
   China 翻译:客户在H100 + vLLM 上每年花费2M.
3. Se ve una caída de precisión de 3 puntos en MATH después de la conversión de peso NVFP4. Nombre dos vías de recuperación: una de calidad primero (mantener los pesos FP8) y otra de costo primero (calibrar con datos en el dominio).
   China 权重转换后 MATH 精度下降 3 点──说出两条恢复路径:一条质量优先(保持 FP8 权重),一条成本优先(用领域内数据校准)
4. Lea los resultados de la inferencia de MLPerf v6.0. ¿Cuál tarea tiene la menor brecha de Blackwell-over-Hopper, y por qué?
   En inglés, el primer libro de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la serie de televisión de televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión
5. Computa el HBM necesario para un modelo 405B en pesos NVFP4 + FP8 KV caché en contexto 128k. ¿Se ajusta en un solo nodo GB200 NVL72?
   En inglés, el modelo de HBM  necesidades   ¿Se adapta a un solo GB200 NVL72 节点?

## Términos clave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Más Leer más Leer más

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) Abril 2026 resultados de la MLPerf.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) NVLink 5 todo-a-todo y núcleos de MoE.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) documentación oficial del motor.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) Orquestación desglosada por encima de TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) el conjunto de referencia que publica números de Blackwell.
