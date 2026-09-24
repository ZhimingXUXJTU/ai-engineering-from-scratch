# Cuantización de producción  AWQ, GPTQ, GGUF K-quants, FP8, MXFP4/NVFP4  量化 生产

> El formato de cuantización no es una opción universal  es una función del hardware, el motor de servicio y la carga de trabajo. GGUF Q4_K_M o Q5_K_M posee CPU y borde, entregados a través de llama.cpp y Ollama. GPTQ gana dentro de VLLM cuando necesitas multi-LoRA en la misma base. AWQ con kernels Marlin-AWQ ofrece ~741 tok/s en un modelo de clase 7B con el mejor Pass@1 en INT4  el 2026 por defecto para la producción de centros de datos. FP8 se mantiene en el centro de Hopper, Ada y Blackwell  casi sin pérdidas y ampliamente apoyado. NVFP4 y MXFP4 (microscalación Blackwell) son agresivos y requieren validación por bloque. Dos equipos de trampas: el conjunto de datos de calibración debe coincidir con el dominio de implementación, y la caché KV está separada de la cuantización de peso  la lección AWQ "mi modelo es de 4 GB ahora" olvida la caché KV de 10-30 GB en los tamaños de lote de producción.

> **【中文解读】**Este artículo presenta la aplicación de la tecnología de producción ambiental en la implementación de la cantidad de INT8/INT4/FP8 en la reducción de los costes de cálculo.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

> ¿ Qué es esto ?**【前置】**學本节前 請先掌握:Fase 10·13(量化基础) ‧Fase 17·04(vLLM) ‧量化格式不是普适选择按硬件+引擎+工作负载选──
> ¿ Qué es esto ?**【类比】**量化格式 = "压缩行李"。GGUF Q4_K_M = 适合火车/edge(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) "Mi modelo sólo tiene 4GB" 忘了KV cache(producción batch 下 10-30GB)。
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objetivos de aprendizaje

- Nombre de los seis formatos de cuantización de producción y sus puntos dulces en 2026.
  China: 2026 六种生产级量化格式及其最佳使用场景──
- Seleccione un formato dado al hardware (CPU vs GPU, Hopper vs Blackwell), motor (vLLM, TRT-LLM, llama.cpp) y carga de trabajo (chat de rutina, razonamiento, multi-LoRA).
  Según el texto original, el proyecto de investigación de la compañía de investigación de la Universidad de Chicago, en el que se desarrollaban investigaciones sobre la existencia de un sistema de datos de datos de datos de datos de la Universidad de Chicago, en el que se desarrolló un sistema de datos de datos de datos de la Universidad de Chicago, en el que se desarrolló un sistema de datos de datos de datos de la Universidad de Chicago, en el que se desarrolló un sistema de datos de datos de datos de datos de la Universidad de Chicago.
- Computa la memoria de peso guardada y el caché KV dejado intacto para un formato elegido.
  Traducción:Cantificación de la forma de cálculo de la conservación de la memoria y de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria de la memoria.
- Nombre la trampa del conjunto de datos de calibración que degrada los modelos cuantizados en el tráfico de dominio.
  China:                                                                                                                                                                                                                                                              

## El problema es la introducción del problema

> **【中文解读】**Quantización reducida de memoria y HBM 带宽消耗正是解码阶段最需要的──FP16 模型重量占140GB,INT4 量化后仅35GB,可运行在一张H100上80GB HBM) ──但量化不是免费激进的量化降低质量 (激进的量化降低质量) 特别是推理密集型任务),不同格式需要不同引擎,不同硬件支持不同精度──2026年有六种生产级量化格式,必须根据你的技术来选择──

> **【拓展：量化技术演进】**                                                                                                                                                                                                                                                              

La cuantización reduce la memoria y el ancho de banda HBM, que es exactamente lo que necesita el decodificación. Un modelo FP16 70B es de 140 GB de pesos. Cuantice los pesos a INT4 (AWQ o GPTQ) y el modelo es de 35 GB  se ajusta a un H100 con espacio para el caché KV, lo que importa porque en 128 secuencias simultáneas con contexto 2k, el caché KV solo es de 20-30 GB.

> Quantificar la reducción de memoria y el consumo de HBM 带宽, es lo más necesario en el proceso de resolución. FP16  70B 模型权重占140GB. 将权重化为INT4(AWQ或GPTQ) 后模型只有35GB可以在一张H100上运行,还有空间放放KV 缓存,这在128并发序列、2K上下文时很重要,因为KV 缓存单独需要 20-30GB.

Pero la cuantización no es gratuita. La cuantización agresiva degrada la calidad, especialmente en tareas pesadas de razonamiento. Diferentes formatos funcionan con diferentes motores. Diferentes hardware soportan diferentes precisiones nativamente. El zoológico de formato 2026 es real y no se puede copiar la elección de otra persona.

> Pero la cuantificación no es gratuita. La cuantificación de la energía aumenta y reduce la calidad, especialmente si se piensa en tareas de tipo intenso. Diferentes modelos se combinan con diferentes motores. Diferentes equipos de origen respaldan diferentes precisiones.

## El concepto central.

### Los seis formatos

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### GGUF  el CPU/edge por defecto

> **【拓展：GGUF 在边缘推理中的地位】**GGUF es el formato de llama.cpp y Ollama, que ocupa un lugar dominante en la teoría de CPU/margen. Q4_K_M y Q5_K_M es la producción de forma estándar en 4-5 bits, para alcanzar casi la calidad de BF16.

GGUF es un formato de archivo, no un esquema de cuantización en sí mismo  agrupan variantes K-cuánticas (Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0) en un solo recipiente. Q4_K_M y Q5_K_M son los valores predeterminados de producción  cerca de la calidad BF16 en 4-5 bits. La mejor opción para la CPU o el servicio de borde porque llama.cpp es el motor de inferencia de CPU más rápido.

> GGUF es un formato de archivo, en sí mismo no es un esquema de cuantificación. Se trata de un formato de archivo que se enmarca en un contenedor.

Penalties de rendimiento en vLLM: ~93 tok/s en 7B  el formato no está optimizado para los núcleos de GPU.

> El modelo de la CPU es el GGUF, si no se utiliza, sólo en la implementación.

### GPTQ  multi-LoRA en VLLM

GPTQ es un algoritmo de cuantización post-entrenamiento con un paso de calibración.

> GPTQ es un algoritmo de calificación posterior con entrenamiento de calificación.

La victoria única: GPTQ-Int4 admite adaptadores LoRA en vLLM. Si está sirviendo un modelo base más 10-50 variantes afinadas (cada una como un LoRA), GPTQ es su camino. NVFP4 no admite LoRA todavía a principios de 2026.

> 独特优势:GPTQ-Int4 在 vLLM 中支持LoRA 适配器──如果你在服务一个基础模型加10-50个微调变体(每个作为LoRA),GPTQ es tu ruta──截至2026年初NVFP4 尚不支持LoRA──

### AWQ  el GPU por defecto del centro de datos

> **【中文解读】**AWQ(Activación-consciente de la Cuantización de Peso) es la opción de la GPU 推理的默认选择――2026年数据中心 GPU 推理的默认选择――.

Cuantización de peso consciente de activación. Protege los ~1% de los pesos más destacados durante la cuantización. núcleos Marlin-AWQ: 10.9x velocidad vs ingenuidad. ~741 tok/s en 7B, mejor Pass@1 entre los formatos INT4.

> 激活感知权重量化──保护量化过程中约1% 最显著的权重──Marlin-AWQ 内核:比朴素方法快 10.9 倍──7B 模型约 741 tok/s,INT4 格式中 Pass@1 最高──

Elija AWQ para nuevo GPU de servicio a menos que necesite multi-LoRA (GPTQ) o agresivo Blackwell FP4 (NVFP4).

> Nueva GPU 推理项目选择 AWQ, excepto que necesite más LoRA(((((GPTQ) o activar el Blackwell FP4((((((NVFP4)。

### FP8  el medio fiable

> **【拓展：FP8 量化的生产应用】**FP8(8-bit 浮点) es la precisión de 2026 de la calidad inconveniente escenario. HOPPER Tensor Cores originales aceleración FP8, Blackwell 继承支持。FP8 内存储省 es la mitad de INT4, pero el riesgo de calidad es muy bajo en la teoría、医疗、代码生成等场景中近乎无损──vLLM、TRT-LLM、SGLang todos apoyan FP8── típico configuración:70B FP8 模型约70GB 权重 + KV Cache,可在一张H100 80GB运行 128 并发──

El punto flotante de 8 bits. Casi sin pérdidas. Amplio soporte. Cores de tensión de Hopper aceleran FP8 de forma nativa. Blackwell hereda. FP8 es el seguro por defecto 2026 cuando la calidad no es negociable (razón, médico, gen de código).

> El 8 bits 浮点──近乎无损──广泛支持──Hopper Tensor Cores 原生加速 FP8──Blackwell 继承──当质量不可妥协时(推理、医疗、代码生成),FP8 es la opción de seguridad de 2026 años──内存节省是INT4的一半,但质量风险远低──

### MXFP4 / NVFP4  Blackwell agresivo

Microescalado FP4. Cada bloque de pesas tiene su propio factor de escala. Agresivos pero acelerados por hardware en los núcleos de tensores Blackwell.

> 微缩放 FP4── cada bloque de peso tiene su propio factor de aceleración──激进但Blackwell Tensor Cores 硬件加速──相比FP8 每字节减半Phase 17 · 07 中的经济优势──

Las cuevas:
- No hay apoyo de la LRA todavía (a principios de 2026).
  El gobierno de la República Popular China (LRA) no apoya a LoRA hasta 2026.
- La disminución de la calidad es visible en las cargas de trabajo pesadas.
  Traducción:La carga de trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo en el trabajo.
- Valida en su conjunto de evaluaciones por modelo.
  Traducción: Cada modelo está en el conjunto de evaluaciones.

### La trampa de calibración

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 需要校准数据集来决定保护哪些权力──通用C4/WikiText 数据集在领域模型(代码、医疗、法律) 上会导致错误决策HumanEval Pass@1 可能下降几百分点──修复方法是用于领域内数据校准,通常几百个样本就够了,发货前在评估集上验证──

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎无影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH benchmark);(4) 长上下文理解INT4 在 128K+ contexto 上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用FP8 或BF16,通用聊天可用INT4──

AWQ y GPTQ requieren un conjunto de datos de calibración  típicamente C4 o WikiText. Para modelos de dominio (código, médico, legal), calibrar en texto web genérico permite que el algoritmo tome decisiones erróneas sobre qué pesos proteger. Pass@1 en HumanEval puede caer varios puntos.

> AWQ y GPTQ 需要校准数据集通常是C4或WikiText──对于领域模型(代码、医疗、法律),在通用网络文本上校准会让算法错误决策保护哪些权重──HumanEval Pass@1可能下降几百分点──

La solución: calibrar en datos dentro del dominio. Cientos de muestras de dominio suelen ser suficientes. Prueba en el conjunto de eval antes de enviar.

> 修复方法: Uses en el campo de datos de calificación.

### La trampa de caché KV

> **【中文解读】**KV Cache 陷:AWQ se va a acumular el peso a 4 bits, pero KV Cache es independiente, mantener en FP16/FP8。70B AWQ  modelo de presupuesto completo de memoria es: peso 35GB + KV Cache(128 并发 × 2K contexto) 20GB + 激活 5GB = 总计 60GB。

AWQ reduce los pesos a 4 bits. El caché KV es separado y se mantiene en FP16/FP8. Para un modelo 70B con AWQ:

- Peso: ~ 35 GB (INT4 desde 140 GB).
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Caché KV en 128 contextos simultáneos × 2k: ~ 20 GB.
  En el texto chino: 128 并发 × 2K 上下文的 KV 缓存: aproximadamente 20GB──
- Actividades: ~ 5 GB.
  En inglés, el nombre de la plataforma es "Lanks".
- Total: ~ 60 GB  se ajusta a H100 80 GB.
  En el caso de los modelos de alta calidad, el tamaño de la caja de alta calidad es de aproximadamente 60 GB.

Ingenuamente "cuantice mi modelo a 4 GB" olvida los otros 30-50 GB.

> 朴素地认为"mi modelo se ha dimensionado a 4GB 了" olvidó que además 30-50GB ⋅ tiene que tener un presupuesto total HBM ⋅

Por separado, la cuantización de caché de KV (FP8 KV o INT8 KV) es una opción diferente con sus propias compensaciones  afecta directamente a la precisión de la atención y no es una victoria libre.

> Además, el KV 缓存量化 (FP8 KV o INT8 KV) es una opción independiente con diferentes pesos que afecta directamente a la precisión de la atención, no a los beneficios de la atención.

### AWQ INT4 es peligroso para el razonamiento

En el caso de la cadena de pensamiento, matemáticas, código-gen con contexto largo, estos sufren visiblemente de cuantización agresiva. AWQ INT4 pierde ~ 3-5 puntos en MATH. Para cargas de trabajo pesadas de razonamiento, envíe FP8 o BF16; acepta el costo de memoria.

> Pensamiento, matemáticas, desarrollo de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

### Guía de selección 2026

- Servicio de CPU/ borde: GGUF Q4_K_M. Terminado.
  中文翻译:CPU/边缘服务:GGUF Q4_K_M。
- Servicio de GPU, chat de rutina, sin LRA.
  En el caso de los servicios de la policía, el gobierno de la República de China no tiene derecho a la información.
- GPU servicio, multi-LoRA: GPTQ con Marlin.
  En el caso de los servicios de la GPU, el número de personas que se encuentran en el centro de la ciudad es el número de personas que se encuentran en el centro de la ciudad.
- Carga de trabajo de razonamiento: PQ8.
  Traducción:Tú理工作负载:FP8。
- Centro de datos Blackwell, calidad validada: NVFP4 + FP8 KV.
  Centro de datos Blackwell, ya está en el mercado.
- Ambigua: ejecutar una evaluación de 1000 muestras en cada formato de candidato.
  En el caso de los candidatos, el número de candidatos es de 1.000.

## Usalo con el marco de ejecución
```figure
gpu-memory-breakdown
```

## Usalo

`code/main.py`Computa la huella de memoria (pesos + KV + activaciones) y el rendimiento relativo en los seis formatos para una gama de tamaños de modelos. muestra dónde domina el caché KV, dónde paga la compresión de peso y dónde FP8 es la opción segura.

> `code/main.py`計算一系列模型大小在六种格式下内存占用(权重 + KV + 激活) y en relación a la cantidad de desglose― mostrar KV 缓存在哪里占主导、权重压缩在哪里划算、FP8 在哪里是安全选择──

## Envíe el producto .

> **【拓展：量化选型决策树】**2026 años de clasificación de formato seleccionar el árbol de decisión:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU 通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) 不确定 → 在候选格式运行1000样本评估;;量化后的验证步骤不可省略每个模型 × 量化格式 × 硬件组合都需要独立验.;;

Esta lección produce`outputs/skill-quantization-picker.md`. Dado el hardware, el tamaño del modelo, el tipo de carga de trabajo y la tolerancia de calidad, elige un formato y produce un plan de calibración/validación.

> 本课产 出  `outputs/skill-quantization-picker.md` Dado hardware, modelo, tipo de carga de trabajo y tolerancia a la calidad, seleccionar el formato y generar el programa de calificación/evaluación.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Para un modelo 70B a 128 simultáneos con 2k contexto, calcular el total de HBM para cada formato. ¿Qué formato permite caber en un H100 80GB?
   Traducción:运行`code/main.py`◊ Para el modelo 70B de 128 y 2K, calcular el total de HBM de cada formato. ¿Qué tipo de formato se puede colocar en un H100 de 80GB?
2. Si se equivocó en cuanto a la tolerancia de calidad, ¿cuál es el camino de recuperación?
   China: tienes un modelo de código 7B. ¿Qué es el camino de recuperación si juzgas mal la tolerancia a la calidad?
3. Computa el tamaño del conjunto de datos de calibración necesario para calibrar AWQ para un modelo de dominio médico. ¿Por qué más datos no siempre son mejores?
   El modelo de área de la medicina de cálculo AWQ 校准所需的数据集大小──为什么更多数据不总是好?
4. Lea el documento del núcleo de Marlin-AWQ o las notas de liberación. Explique en tres frases por qué AWQ alcanza 741 tok/s en 7B mientras que el GPTQ crudo alcanza ~712.
   China: Marlin-AWQ 内核论文或发布说明──用三句话解释为什么AWQ en 7B arriba alcanza 741 tok/s, mientras que el GPTQ original es de aproximadamente 712──
5. ¿Cuándo tiene sentido combinar los pesos AWQ con el caché KV FP8 vs mantener KV en BF16?
   中文翻译:何时将 AWQ 权重与 FP8 KV 缓存组合有意义,何时保持 BF16 KV?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## Más Leer más Leer más

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/) índices de referencia comparativos.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) Números de rendimiento por formato.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/) Selección por formato.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html) formatos y banderas compatibles.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) formulación original de la AWQ.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323) formulación original de GPTQ.
