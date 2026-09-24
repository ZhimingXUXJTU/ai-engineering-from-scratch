# Edge Inference  Apple Neural Engine, Qualcomm Hexagon, WebGPU/WebLLM, Jetson 推理 边缘 LLM GPU 欧盟

> La limitación de borde principal es el ancho de banda de memoria, no el cálculo. El DRAM móvil se sitúa a 50-90 GB/s; el centro de datos HBM3 elimina 2-3 TB/s  una brecha de 30-50x. El decodificación está ligada a la memoria así que la brecha es decisiva. En 2026 el paisaje se divide en cuatro partes. El motor neuronal Apple M4/A18 alcanza 38 TOPS con memoria unificada (sin copia de CPUNPU). Qualcomm Snapdragon X Elite / 8 Gen 4 Hexagon alcanza 45 TOPS. WebGPU + WebLLM ejecuta Llama 3.1 8B (Q4) a ~ 41 tok/s en M3 Max (aproximadamente 70-80% de nativos); 17.6k estrellas de GitHub, API compatible con OpenAI, ~70-75% de cobertura móvil. NVIDIA Jetson Orin Nano Super (8GB) se ajusta a Llama 3.2 3B / Phi-3; AGX Orin ejecuta gpt-oss-20b a través de vLLM a ~40 tok/s; Jetson T4000 (JetPack 7.1) es 2x AGX Orin. TensorRT Edge-LLM admite EAGLE-3, NVFP4, preempleo en pedazos  mostrado en CES 2026 por Bosch, ThunderSoft, MediaTek.

> **【中文解读】**Este capítulo presenta los desafíos y soluciones de la aplicación de LLM en dispositivos de borde.
**Type:** Learn
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 09 (Production Quantization)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM)、Fase 17·09(量化)。边缘推理核心约束 = 内存带宽(不是算力)。
> ¿ Qué es esto ?**【类比】**边缘 vs 数据中心 = "手机 vs 超算"――手机 DRAM 50-90 GB/s, datos center HBM3 2-3 TB/s30-50 倍差,解码(内存绑定) 下决定性。2026 四大平台:Apple NE(38 TOPS 统一内存)、Qualcomm Hexagon(45 TOPS)、WebGPU+WebLLM(M3 Max 跑 Llama 3.1 8B 41 tok/s)、Jetson(Orin AGX 跑 gpt-oss-20b 40 tok/s)。TensorRT Edge-LLM 支持EAGLE-3 + NVFP4 + chunked prefill。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Explica por qué la inferencia de LLM móvil está limitada al ancho de banda de memoria y la computación es secundaria.
  Traducción: explica por qué el movimiento LLM 推理 es de memoria con amplitud limitada, mientras que la capacidad de cálculo es secundaria.
- Enumera los cuatro objetivos de borde (Apple ANE, Qualcomm Hexagon, WebGPU/WebLLM, NVIDIA Jetson) y ajuste cada uno a un caso de uso.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Nombre la brecha de cobertura de 2026 WebGPU (Firefox Android se pone al día) y el aterrizaje de Safari iOS 26.
  El sitio web de la plataforma de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de (Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de (Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de (Internet de Internet de Internet de Internet de Internet de Internet de (Internet de Internet de Internet de Internet de Internet de Internet de (Internet de Internet de Internet de (Internet de Internet de Internet de Internet de Internet de (Internet de ( ( ( (Internet de)                                                                                                               
- Seleccione un formato de cuantificación por objetivo (Core ML INT4 + FP16 para ANE, QNN INT8/INT4 para Hexagon, WebGPU Q4 para el navegador, NVFP4 para Jetson Thor).
  Por ejemplo, el sistema de análisis de datos de la computadora de Internet (JGPU) es un sistema de análisis de datos de datos de la computadora de Internet (JGPU).

## El problema es la introducción del problema

> **【中文解读】**边缘推理的核心约束是内存带宽而不是计算能力――移动DRAM 带宽 50-90 GB/s,数据中心 HBM3 达2-3 TB/s30-50x 差距――由于 解码阶段是内存带宽限定的,这个差距是决定性的――7B 模型 Q4 量化后权重3.5GB,在 50 GB/s 带宽下不同的读取需要70ms理论上限制约14 tok/s――2026年边缘推推是四个不同的平台、四种解决方案――

> **【拓展：边缘 AI 芯片市场】**2026 años marginal AI 芯片的竞争格局:(1) Apple Neural Engine (M4/A18) 38 TOPS,统一内存架构,无需CPUNPU 数据拷贝;(2) Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4) 45 TOPS,QNN SDK 提供转换链路;(3) Intel Lunar Lake / AMD Ryzen AI 30040-50 TOPS, software生态落后于Apple/Qualcomm;((4) NVIDIA Jetson Orin/Thor边缘 GPU 方案,支持vLLM 和TensorRT Edge-LLM──语音代理是边缘推杀手级应用本地推理完全消除网络延迟──

Un cliente quiere un chatbot en el dispositivo: voz-primero, privado por defecto, funciona fuera de línea. En un MacBook Pro M3 Max, Llama 3.1 8B Q4 funciona a ~55 tok/s  bien. En un iPhone 16 Pro, el mismo modelo funciona a 3 tok/s  no está bien. En un Android de gama media con Snapdragon 8 Gen 3, 7 tok/s. En el navegador a través de WebGPU en Chrome Android v121+, 4-8 tok/s dependiendo del dispositivo.

La variación de rendimiento no es un problema de portación. Es la brecha de ancho de banda veces el formato de cuantización veces si la NPU es accesible desde el espacio del usuario.

## El concepto central.

### El ancho de banda es el verdadero techo

> **【中文解读】**边缘推理的真正天花板是内存带宽――Decode 阶段每生成一个代币 需要读取全部权重――7B Q4 模型 3.5GB,在 50 GB/s 带宽下读取需要 70ms理论上限约14 tok/s――在 90 GB/s(高端移动DRAM) 下上限升至约25 tok/s――数据中心 HBM3在不同 3 TB/s读取同一模型只需1.2ms上限830 tok/s――同样模型 下同样权重、内存子系统――

El decode lee el conjunto completo de pesas para cada token. Un modelo 7B en el Q4 es de 3.5 GB. Leer 3.5 GB a 50 GB/s toma 70 ms  un teórico techo de ~14 tok/s. A 90 GB/s (DRAM móvil de gama alta) el techo se mueve a ~25 tok/s. Ninguna cantidad de computación ayuda por debajo de este número.

Datacenter HBM3 a 3 TB/s elimina el mismo 3,5 GB en 1,2 ms  el techo es 830 tok/s. El mismo modelo, los mismos pesos.

### El motor neuronal de Apple (M4 / A18)

- Hasta 38 TOPS. Memoria unificada (CPU y ANE comparten el mismo pool)  sin gastos generales de copia.
- Acceso a través de Core ML + `.mlmodel`Modelos compilados, o mediante Shaders de rendimiento de metal (MPS) a través de PyTorch.
- Llama.cpp Metal backend utiliza MPS, no ANE directamente; ANE nativo requiere la conversión de Core ML.
- Mejor camino práctico para las aplicaciones iOS en 2026: Core ML con pesos INT4 + activaciones FP16.

### Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)

- Hasta 45 TOPS. Integrado con CPU y GPU en el SoC pero dominio de memoria separado.
- El SDK de QNN (Qualcomm Neural Network) y el AI Hub proporcionan la conversión desde PyTorch/ONNX.
- Las plantillas de chat, Llama 3.2, Phi-3 todos enviados como artefactos de primera clase en AI Hub.

### NPUs Intel / AMD (Lunar Lake, Ryzen AI 300)

- 40-50 TOPS. El software se queda atrás de Apple/Qualcomm; OpenVINO está mejorando pero es un nicho.
- Mejor para aplicaciones de copiloto de Windows ARM; nativo en escritorios AMD/Intel para local-first.

### WebGPU + WebLLM

> **【中文解读】**WebGPU + WebLLM es un programa de análisis de datos en el navegador 推理的方案无需安装,通过 WebGPU computador shader 运行模型──在M3 Max 上 Llama 3.1 8B Q4 达到 ~41 tok/s, aproximadamente 70% de la energía de la vida original──2026 覆盖率:Chrome Android v121+、Safari iOS 26 GA、Firefox Android 仍追赶,总体约70-75% 移动浏览器覆盖──17.6k GitHub stars,OpenAI 兼容的 JavaScript API──

- Ejecutar modelos en el navegador a través de los shaders de computación WebGPU; no se instala.
- Llama 3.1 8B Q4 a ~ 41 tok/s en M3 Max  aproximadamente 70-80% de nativo a través del mismo backend.
- 17.6k GitHub estrellas en WebLLM; OpenAI compatible API JS; Apache 2.0.
- 2026 cobertura: Chrome Android v121+, Safari iOS 26 GA, Firefox Android todavía alcanzando.

### NVIDIA La familia Jetson

- Orin Nano Super (8GB): se ajusta a Llama 3.2 3B, Phi-3 a buen tiempo/s.
- AGX Orin: ejecuta gpt-oss-20b a través de vLLM a ~ 40 tok/s.
- Thor / T4000 (JetPack 7.1): 2x rendimiento AGX Orin, EAGLE-3 y NVFP4 compatibles.
- TensorRT Edge-LLM (2026) admite la descifrado especulativo EAGLE-3, pesos NVFP4, preempleo en pedazos  las optimizaciones del centro de datos portadas a borde.

### La elección de la cuantificación por objetivo

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### La trampa de largo contexto en el borde

> **【中文解读】**边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. 边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. 边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. 边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. 边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. 边缘设备上 128K 下文是数据中心特性. 边缘设备上长上下文陷:Llama 3.1 的 128K 上下文是数据中心特性. 边缘设备上 128K 上下文是数据中心特性. 边缘设备上 128K 上下文是数据中心特性. 边缘设备上 128K 下文是数据中心的 128K 下文是数据中心的 128K 下文是数据中心的 128K 下文是数据中心的 128K 下文是数据中心的 128K 下文是4K 下文是4K 下文是4K 下文是4K 下文是4K 下文是4K 下文是4K 下文是4K 下文是是是是是的.

> **【拓展：边缘推理的隐私优势】**边缘推理在隐私敏感场景有独特优势: 1) 医疗患者数据不离开设备; 2) 金融交易分析在本地完成; 3) 法律律师-客户通信不上传云端; 4) 军事/政府完全离线运行.

El contexto 128K de Llama 3.1 es una característica del centro de datos. En un teléfono con 8 GB de RAM, modelo de 4 GB + caché KV de 2 GB para tokens de 32K + OS overhead = OOM.

### La voz es la aplicación asesina

> **【拓展：边缘推理的应用场景】**边缘推理的杀手级应用是语音代理语音代理对延迟极度敏感(首代币 < 500ms) ――本地推理完全消除网络延迟――结合语音转文字(Whisper Turbo 变体在边缘运行),边缘推理成为生产质量的语音环路――其他场景包括:隐私优先医疗/金融分析、离线代码补充、实时翻译――Apple's"Private Cloud Compute" es una forma de descomponer un simple equipo de tareas completadas, complejas tareas en Apple 专业云处理但承诺不存储数据――

Los agentes de voz son sensibles a la latencia (el primer token < 500 ms). La inferencia local elimina por completo la latencia de la red. Combinada con el habla a texto (variantes de Whisper Turbo se ejecutan en el borde) y la inferencia de borde se convierte en el bucle de voz de calidad de producción.

### Números que debes recordar

- Apple M4 / A18 ANE: 38 TOPS.
- Qualcomm Hexagon SD X Elite: 45 TOPS.
- WebLLM M3 Max: ~ 41 tok/s en Llama 3.1 8B Q4.
- AGX Orin: ~ 40 tok/s en gpt-oss-20b a través de VLLM.
- La brecha de ancho de banda del centro de datos: 30-50x.
- Cobertura móvil de WebGPU: ~ 70-75% (de retraso en Firefox Android).

## Usalo con el marco de ejecución
```figure
edge-bandwidth-pipe
```

## Usalo

`code/main.py`Computa límites teóricos de descifrado de rendimiento de la banda ancha de la matemática de límites de ancho de banda a través de objetivos de borde.

> `code/main.py`Desde el cálculo de la amplitud limitada matemática de los objetivos de los diferentes extremos de la teoría de la resolución de la capacidad de producción en la limitación.

## Envíe el producto .

Esta lección produce`outputs/skill-edge-target-picker.md`. En función de la plataforma (iOS/Android/browser/Jetson), el modelo y el presupuesto de latencia/memoria, elige un formato de cuantificación y una línea de conversión.

> 本课产 出  `outputs/skill-edge-target-picker.md` dar una plataforma determinada (iOS/Android/Browser/Jetson)  modelos y tarder/presupuesto de memoria, seleccionar formato y transferencia de datos

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Para un modelo 7B en el Q4 en un Snapdragon 8 Gen 3 (~ 77 GB / s ancho de banda), calcular el techo de decodificación. Comparar con 6-8 tok / s observados  ¿Es el tiempo de ejecución eficiente?
   Traducción:运行`code/main.py` calcular Snapdragon 8 Gen 3 (~ 77 GB/s 带宽) en Q4 7B 模型的解码上限──与观察到的 6-8 tok/s
2. WebGPU en Android requiere Chrome v121+. Diseñar un fallback para navegadores más antiguos  el lado del servidor a través de la misma API compatible con OpenAI.
   China Translation:Android 需要 Chrome v121+── para el diseño de un navegador viejo regresar a la aplicación 通过相同的 OpenAI 兼容 API 实现服务端推理──
3. Su aplicación iOS necesita streaming de contexto 4K. ¿Qué combinación de modelo/formato le permite mantenerse bajo 4 GB de memoria activa en un iPhone 16?
   Traducción:Tu aplicación iOS necesita 4K. ¿Qué tipo de modelo/conjunto de formato puede mantenerse en memoria activa de 4GB en el iPhone 16?
4. Jetson AGX Orin ejecuta Gpt-oss-20b a 40 tok/s. Jetson Nano encaja sólo en un 3B. Si su producto se dirige a ambos, ¿cómo unificar la pila de inferencias?
   En inglés, el modelo de producción de Jetson AGX Orin es de 40 tok/s. ¿Cómo se puede aplicar el modelo de producción de Jetson Nano?
5. Argumentar si "WebLLM está listo para la producción en 2026". Cita la cobertura, el rendimiento y la brecha de Firefox Android.
   En el contexto de la actualidad, el desarrollo de la tecnología de la información en línea se ha convertido en un proceso de desarrollo de la tecnología de la información en línea.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| ANE | "Apple neural engine" | On-device NPU in M-series and A-series; unified memory |
| Hexagon | "Qualcomm NPU" | Snapdragon NPU; QNN SDK for access |
| WebGPU | "browser GPU" | W3C-standardized browser GPU API; Chrome/Safari 2026 |
| WebLLM | "browser LLM runtime" | MLC-LLM project; Apache 2.0; OpenAI-compatible JS |
| Jetson | "NVIDIA edge" | Orin Nano / AGX / Thor / T4000 family |
| TRT Edge-LLM | "edge TensorRT" | 2026 edge port of TensorRT-LLM; EAGLE-3 + NVFP4 |
| Unified memory | "shared pool" | CPU and NPU see same RAM; no copy overhead |
| Bandwidth-bound | "memory limited" | Decode gated by bytes/sec reading weights |
| Core ML | "Apple conversion" | Apple framework for ANE-native models |
| QNN | "Qualcomm stack" | Qualcomm Neural Network SDK |

## Más Leer más Leer más

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/) paisaje y puntos de referencia.
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/) Orin / AGX / Thor.
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/) Anuncio del puerto de borde 2026
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2) diseño y valores de referencia.
- [Apple Core ML](https://developer.apple.com/documentation/coreml) Conversión de origen.
- [Qualcomm AI Hub](https://aihub.qualcomm.com/) Modelos preconvertidos para Hexagon.
