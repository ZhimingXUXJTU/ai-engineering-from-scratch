# Selección de servicio de auto-hosting  llama.cpp, Ollama, TGI, vLLM, SGLang ‬ 自托管 选择 服务 SGLang vLLM
# Selección de servidores auto-hospedados  Motor de ajuste a hardware y escala

> La selección del motor es una función del hardware, la escala y el ecosistema  no una lectura de la tabla de clasificación. Cuatro motores dominan la inferencia auto-hosted en 2026: llama.cpp, Ollama, vLLM, SGLang, con TGI retrasando en el modo de mantenimiento. **llama.cpp**es más rápido en CPU  más amplio soporte de modelo, control total sobre cuantización y threading. **Ollama**es la instalación de un solo comando de dev-laptop, ~15-30% más lenta que llama.cpp (serialización Go + CGo + HTTP), 3x de la brecha de rendimiento bajo carga similar a la de prod. **TGI entered maintenance mode December 11, 2025** sólo corregir errores, ~10% más lento rendimiento bruto que vLLM pero históricamente superior observabilidad e integración de ecosistemas HF. Ese estado de mantenimiento lo convierte en una apuesta a largo plazo arriesgada  SGLang o vLLM son valores predeterminados más seguros para nuevos proyectos. **vLLM**es el estándar de producción general  v0.15.1 (febrero 2026) añade PyTorch 2.10, RTX Blackwell SM120, H200 optimización. **SGLang**es el especialista en múltiples giros / prefijos agenciales pesados  400,000+ GPUs en producción (xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS). Constrangimientos de hardware: CPU-first → llama.cpp. AMD / no NVIDIA → vLLM es el camino más fuerte (TRT-LLM está bloqueado por NVIDIA). 2026 patrón de tubería: dev = Ollama, en fase = llama.cpp, prod = vLLM o SGLang. Los motores toman diferentes formatos de peso  GGUF para la familia llama.cpp, HF safetensores para los motores GPU  por lo que una conversión de formato puede sentarse entre etapas.

> **【中文解读】**Este capítulo presenta la comparación y la selección de los sistemas de gestión automática.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)

> ¿ Qué es esto ?**【前置】**Este episodio es la fase 17 收官课,整合 04/06/07/09/18 引擎知识 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选型矩阵 四大自托管引擎选矩阵 四大自托管引擎知识
> ¿ Qué es esto ?**【类比】**Autotúbol motor = "AI 服务器品牌"―llama.cpp = CPU 王者(最广模型支持、量化全控制);Ollama = 笔记本一键安装(比 llama.cpp 慢 15-30%);TGI 已进入维护模式(2025.12.11) 修改 bug,新项目别选;vLLM = 通用生产默认(v0.15.1+ PyTorch 2.10+Blackwell);SGLang = Agent 多轮+前万密集专家(40+ GPU 在 xAI/LinkedIn/Cursor)―
> ¿ Qué es esto ?**【困惑】**P: 我的场景该选哪个? CPU-solo→llama.cpp;AMD/非 NVIDIA→vLLM(TRT-LLM 锁 NVIDIA);Agencia 多轮→SGLang;通用→vLLM。2026 流水线:dev=Ollama、staging=llama.cpp、prod=vLLM/SGLang,全用 GGUF/HF 权重一致。
**Time:** ~45 minutes | **时间:** ~45 minutes

## Objetivos de aprendizaje

- Seleccione un motor dado hardware (CPU / AMD / NVIDIA Hopper / Blackwell), escala (1 usuario / 100 / 10,000), y carga de trabajo (talla general / agente / contexto largo).
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- Nombre del estado de modo de mantenimiento TGI 2026 (11 de diciembre de 2025) y por qué desvia nuevos proyectos hacia vLLM o SGLang.
  China:  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态 (título original)  维护模式状态)  维护模式状态 (título original)  维护模式状态)  维护模式状态 (título original)  维护模式状态)  维护模式状态  维护模式状态  维护模式状态  维护模式  维护模式   维护模式   维护模式   维护模式     维护模式       维护模式         维护模式                                                                                            
- Describa la tubería de desarrollo/estación/producción utilizando los mismos pesos de GGUF o HF en toda la línea.
  En el contexto de la vida, el uso de la misma GGUF o HF 权重的开发/预发布/生产流水线.
- Explica por qué "sólo el CPU" obliga a llama.cpp y "AMD" excluye TRT-LLM.
  China: explica por qué "sólo CPU" obligó a usar llama.cpp y "AMD" excluyó TRT-LLM。

## El problema es la introducción del problema

> **【中文解读】**La elección del motor de cálculo depende de tres dimensiones: hardware (CPU / AMD / NVIDIA Hopper / Blackwell)  tamaño ((1 usuario / 100 / 10,000)  trabajo de carga ((通用聊天 / Agent / 长上下文)  2025 年 12 月 11 日 HuggingFace TGI 进入维护模式 ((sólo se corrige el error), lo que hace que el nuevo proyecto debe estar en forma de memoria lejos de TGI, para convertirse en VLLM o SGLang.
- Describa la línea de desarrollo/estacionamiento/producción, incluida la conversión de formato GGUF a safetensores entre etapas.
- Explica por qué "CPU-first" apunta a llama.cpp y "AMD" excluye TRT-LLM.

> **【拓展：2026 年推理引擎选择决策】**2026 年推理引擎的硬件优先决策树:(1) Solo en CPU → llama.cpp(única opción de competencia);(2) AMD GPU → vLLM(ROCm 支持),TRT-LLM 不支持 AMD;(3) NVIDIA Hopper → vLLM 或 SGLang 或 TRT-LLM(三选一);(4) NVIDIA Blackwell → TRT-LLM 吞吐最高;(5) Apple Silicon → llama.cpppp(Metal 后端) △规模决策:1 用户→Ollama,10-100→LLvM 单,100-10K→LLM producción-stack 或 SangGL,10K+→producción-stack + 分离式 + LMC。

Su equipo inicia un nuevo proyecto de LLM auto-organizado. Un ingeniero dice Ollama, otro dice vLLM, un tercero dice "¿no funciona TGI simplemente fuera de la caja?" Los tres son adecuados para diferentes contextos. Ninguno es adecuado para todos.

En 2026 el árbol de elección importa: hardware primero, escala segunda, carga de trabajo tercera. Y un evento específico de 2025  TGI ingresando al modo de mantenimiento el 11 de diciembre  cambia el predeterminado para nuevos proyectos.

## El concepto central.

### Los cinco motores

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### La primera decisión sobre el hardware

**CPU-first**Ollama también funciona pero es más lento. Ningún otro motor es competitivo en CPU.

**AMD GPU**→ vLLM es el camino más fuerte (soporte de ROCm de AMD). SGLang también funciona. TRT-LLM está bloqueado por NVIDIA, por lo que está fuera.

**NVIDIA Hopper (H100 / H200)**→ VLLM o SGLang o TRT-LLM. Los tres de primer nivel.

**NVIDIA Blackwell (B200 / GB200)**→ TRT-LLM es el líder de rendimiento (Fase 17 · 07). vLLM y SGLang siguen de cerca.

**Apple Silicon (M-series)**Ollama envuelve esto.

### Decisión de segunda escala

**1 user / local dev**Una orden, la primera señal en segundos.

**10-100 users / small team**→ VLLM de un solo GPU.

**100-10k users / production**→ vLLM producción-estaca (fase 17 · 18) o SGLang.

**10k+ users / enterprise**→ vLLM producción-pillar + desagregado (fase 17 · 17) + LMCache (fase 17 · 18).

### Encuesta de trabajo-tercera decisión

**General chat / Q&A**→ vLLM gana en el default general.

**Agentic multi-turn (tools, planning, memory)**→ La atención radix de SGLang (fase 17 · 06) es la dominante.

**RAG with heavy prefix reuse**→ SGLang.

**Code generation**→ VLLM bien; SGLang ligeramente mejor en la caché.

**Long context (128K+)**→ VLLM + preempleo en pedazos; SGLang + KV en capas.

### La trampa de mantenimiento TGI

> **【中文解读】**TGI 陷:HuggingFace TGI entró en el modelo de mantenimiento el 11 de diciembre de 2025 solo se ha solucionado el error, ya no hay funciones actualizadas En la historia TGI tiene la máxima observabilidad y HF  生态集成 (húngaro) 模型卡、安全工具), original吞吐略低于vLLM (cerca del 10%). Para el nuevo proyecto de 2026 año, debe permanecer en el camino de TGI (también conocido como TGI), pero la implementación de TGI puede continuar, pero debe planificarse la migración (SangGL 和 vLLM) es una opción más segura.

> **【拓展：工作负载驱动的引擎选择】**工作负载维度驱动引擎选择:(1) 通用聊天/问答 → vLLM(广泛默认);(2) Agent 多轮对话(工具、规划、记忆)→ SGLang RadixAttention 主导;(3) RAG 重前复用 → SGLang;(4) 代码生成 → vLLM 足够,SGLang 缓存略好;(5) 长上下文(128K+)→ vLLM + 分块预填充,SGLang + 分层 KV──Ollama 适合开发但不是生产共享服务的理想选择Go HTTP 序列化增加开销并发管理比 vLLM 简单、Openmetry 支持滞后.

Hugging Face TGI entró en modo de mantenimiento el 11 de diciembre de 2025  solo se corrigen errores en el futuro. Históricamente: observabilidad de primer nivel, mejor integración de ecosistema HF (tarjetas de modelo, herramientas de seguridad), ligeramente detrás de vLLM en rendimiento bruto.

Para nuevos proyectos en 2026: por defecto, no se aplica TGI. Las implementaciones existentes de TGI pueden continuar pero eventualmente deberían migrar.

### El patrón de la tubería

Dev (Ollama) → staging (llama.cpp) → prod (vLLM). Los motores toman diferentes formatos de peso  GGUF para la familia llama.cpp, HF safetensors para los motores GPU  para que una conversión de formato pueda estar entre etapas. Los ingenieros iterian rápidamente en computadoras portátiles; el espejo de etapa cuantiza la producción; prod es el objetivo de servicio.

### Aviso de Ollama

Ollama es ideal para el desarrollo. No es ideal para la producción compartida: la serialización HTTP Go añade gastos generales, la gestión de concurrencia es más simple que vLLM, OpenTelemetry soporte lags. Utilice Ollama donde brilla  un usuario, un comando  y cambiar a vLLM para compartir.

### Auto-hosted vs. administrado es una decisión separada

Fase 17 · 01 (hiperscalers administrados), · 02 (plataformas de inferencia) cubierta gestionada. Esta lección asume que ya ha decidido auto-host. Razones para auto-host: residencia de datos, ajuste a medida, propiedad total de costos a escala, modelo de dominio no disponible en alojado.

### Números que debes recordar

- Modo de mantenimiento TGI: 11 de diciembre de 2025.
- vLLM v0.15.1: febrero 2026; PyTorch 2.10; soporte para Blackwell SM120.
- Impresión de producción de SGLang: 400.000+ GPUs.
- La brecha de rendimiento de Ollama vs llama.cpp: 15-30% más lenta; 3 veces menos de la carga de la prolongación.

## Usalo con el marco de ejecución
```figure
data-parallel
```

## Usalo

`code/main.py`es un caminante del árbol de decisión: dado hardware + escala + carga de trabajo, elige un motor y explica por qué.

> `code/main.py`es un caminante del árbol de decisión: dado hardware + escala + carga de trabajo, elige un motor y explica por qué.

## Envíe el producto .

> **【拓展：自托管 vs 托管的决策】**El sistema de gestión y la gestión de los datos no puede abandonar la organización; 2) el sistema de gestión y gestión de datos de los usuarios de los mismos; 3) el gasto anual de gestión y gestión de datos de gran escala de los mismos; 4) el modelo de los sectores no está disponible en la plataforma de gestión; 4) la fase 17·01 (hiperscaler de gestión) y ·02 (concentración de datos) cubre las opciones de gestión;

Esta lección produce`outputs/skill-engine-picker.md`Ante las limitaciones, elige un motor y escribe el plan de migración.

> 本课产 出  `outputs/skill-engine-picker.md`Ante las limitaciones, elige un motor y escribe el plan de migración.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿La salida coincide con su intuición?
   Con tu hardware / tamaño / trabajo / carga de trabajo`code/main.py`¿La producción está en conformidad con el esperado?
2. Tu infra es de 12 H100 y 8 MI300X AMD. ¿Qué motor? ¿Por qué está TRT-LLM fuera de la mesa?
   Su infraestructura es de 12 bloques H100 y 8 bloques MI300X AMD. ¿Con qué motor? ¿Por qué TRT-LLM es inelegible?
3. Un equipo quiere usar TGI en 2026 porque "es lo que sabemos".
   Un equipo piensa en 2026 usar TGI porque "es lo que conocemos"
4. Ollama dev a vLLM prod: ¿qué cambios en la cuantización, configuración y observabilidad?
   En inglés, Ollama  desarrollado hasta vLLM.
5. Producto RAG con longitud de prefijo P99 8K y alta reutilización entre los inquilinos.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| llama.cpp | "the CPU one" | Widest model support, fastest on CPU |
| Ollama | "the laptop one" | One-command install, dev-grade throughput |
| TGI | "HF's serving" | Maintenance mode since Dec 2025 |
| vLLM | "the default" | Broad production baseline 2026 |
| SGLang | "the agentic one" | Prefix-heavy, RadixAttention |
| TRT-LLM | "NVIDIA-locked" | Blackwell throughput leader, NVIDIA only |
| GGUF | "llama.cpp format" | Bundled K-quant variants |
| Production-stack | "vLLM K8s" | Phase 17 · 18 reference deployment |
| Pipeline pattern | "dev→stage→prod" | Ollama → llama.cpp → vLLM; weight formats differ per engine |

## Más Leer más Leer más

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference) notas de liberación.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
