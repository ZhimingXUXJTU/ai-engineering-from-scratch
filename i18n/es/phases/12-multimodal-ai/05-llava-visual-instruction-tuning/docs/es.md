# LaVA y la instrucción visual de ajuste .

> La LAVA (abril 2023) es la arquitectura multimodal más copiada del planeta. Remplazó el Q-Former de BLIP-2 con un MLP de 2 capas, reemplazó la atención cruzada cerrada de Flamingo con una concatenation token ingenua y entrenó en 158k giros de instrucción visual generados por GPT-4 a partir de títulos de texto. Cualquier practicante que construyó un VLM entre 2023 y 2026 construyó alguna variante de LLaVA. LLaVA-1.5 se añadió AnyRes. LaVA-NeXT ha aumentado la resolución. LLaVA-OneVision imagen unificada, multi-imagen y video en una sola receta. Esta lección lee la receta, aplica el proyector y explica por qué "el más simple ganó".

> **【中文解读】**La LaVA es la arquitectura multimodal más copiada entre 2023-2026 años. Su idea central es muy simple: con 2 niveles de MLP, colocar la salida del codificador de imágenes en el espacio de proyección en el modelo de lenguaje, luego colocar el token de imágenes directamente enlazada en el texto. La LaVA ha demostrado que la arquitectura simple + datos de alta calidad "podría superar el diseño complejo.

> **【拓展：多模态大模型的起源】**Antes de LLaVA, el modelo de múltiples modelos dependía principalmente de mecanismos complejos de atención transmodal (como el control de la atención transmodal de Flamingo, el Q-Former de BLIP-2). El éxito de LLaVA se marcó por la investigación de múltiples modelos que se transfirió del "diseño de mejores interfaces transmodal" a "con una interfaz más simple + más datos" en un cambio de paradigma. Este pensamiento influyó directamente en todas las siguientes VLMs principales (InternVL, Qwen-VL, Phi-Vision, etc.)

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·02(CLIP 视觉编码器);Fase 12·03(BLIP-2 桥接,对照学习);Fase 11·08(Instrucción Tuning 指令微调)。LLaVA es la forma en que se trata de un proyecto de BLIP-2, basado en datos de la organización.
> ¿ Qué es esto ?**【类比】**LLaVA = "把图片直接打印出贴在文档里"―BLIP-2 Q-Former = "把 256 páginas书压成 32 páginas resumen再交给LLM"; LLaVA MLP = "576 páginas原文整本贴给LLM"―Láva MLP = "576 páginas原文整本贴给LLM"―Láva MLP: "Láva MLP"―Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Láva MLP: "Lá"

## Objetivos de aprendizaje

- Construir un proyector de MLP de 2 capas que mapea las incrustaciones de parches de ViT (dim 1024) a las incrustaciones de un LLM (dim 4096).
- Caminar la receta de dos etapas de LLaVA: (1) alineación del proyector en pares de capciones de 558k, (2) ajuste de instrucciones visuales en 158k giros generados por GPT-4.
- Construir un mensaje de formato LLaVA con el marcador de lugar de la imagen, el mensaje de sistema y los giros de usuario/asistente.
- Explica por qué la comunidad se trasladó de Q-Former a MLP a pesar de la victoria de Q-Former en el presupuesto de tokens.

## El problema es el contexto del problema

El Q-Former de BLIP-2 (Lección 12.03) comprime una imagen a 32 tokens. Limpio, eficiente, bueno para los puntos de referencia. Pero tiene dos problemas.

En primer lugar, el Q-Former es entrenable pero su pérdida no es la tarea final. La etapa 1 entrena a ITC+ITM+ITG. La etapa 2 entrena a la pérdida de LM. Las consultas aprenden alguna representación intermedia que el LLM luego tiene que descifrar.

En segundo lugar, el Q-Former toma 188 millones de parámetros, y en la escala de 2023 de LLaVA tuviste que co-diseñarlo con tu LLM objetivo. Cambia el LLM, retraina el Q-Former. Cambia el codificador de visión, retraina. Cada combinación fue un proyecto de I + D separado.

> **【中文解读】**El Q-Former de BLIP-2 comprimirá la imagen en 32 tokens, parece alta eficiencia, pero tiene dos problemas centrales: 1)                                                                                                                                                                                                                                               

La respuesta de LLaVA fue embarazosa en su simplicidad: tomar los 576 tokens de parches del ViT, pasar cada uno a través de una MLP de 2 capas (`1024 → 4096 → 4096`No hay cuello de botella, no hay etapa 1 de preentrenamiento en objetivos extraños, sólo entrenar al MLP en una pérdida directa de LM.

> **【中文解读】**El esquema de LLaVA es simple a embarazoso: directamente a ViT 576 个补丁代币 通过一个2层 MLP(`1024 → 4096 → 4096`), luego todo se lanza en la serie de entradas del LLM.

> ️ **【易错点】**La primera etapa debe entrenarse! Muchos piensan que pueden saltar la primera etapa  directos hacer instrucciones 微调不行! no entrenado de proyectores de salida de impulso, LLM 完全看不懂视觉代币 含义, la segunda etapa hará LLM Colocar el token de visión cuando el ruido se ignora.

¿De dónde provienen los datos? La segunda visión de LLaVA: utilizar GPT-4 (solo texto) para generar datos de instrucciones.

> **【中文解读】**La segunda innovación de LLaVA: con GPT-4 (pure text model) generar instrucciones de datos.

El resultado: un VLM que corrió en 8 A100 durante un día, venció a Flamingo en MMMU, y envió un puesto de control abierto que la comunidad podría extender. A finales de 2023 había engendrado más de 50 tenedores.

> **【拓展：LLaVA 的产业影响】**La LLAVA ha demostrado que VLM no necesita una gran capacidad de cálculo 8 张 A100 跑一天就足了. Esto redujo enormemente la puerta de la investigación de múltiples modelos, impulsó el estallido del ecosistema de VLM abierto. En el escenario financiero, la estructura de LLAVA se utiliza para comprender los gráficos de los informes financieros, las imágenes de las facturas, etc., es el componente básico de la tubería de comprensión de documentos.

## El concepto central.

> **【中文解读】**LLaVA conectará CLIP  visual editor con LLM  , a través de instrucciones visuales , el costo de entrenamiento será de aproximadamente 100 dólares.

> **【拓展：LLaVA 的开源生态】**LaVA es el modelo de múltiples modelos de código abierto más exitoso. LaVA-NeXT  soporta entrada de resolución arbitraria, LaVA-OneVision 统一图像和视频理解── rendimiento cerca del 80% de GPT-4V, ha producido un gran número de modelos derivados.


### La arquitectura y la arquitectura.

LLaVA-1.5 en 13B:  LLaVA-1.5 13B 参数版本:
- Encodrador de visión / 视觉编码器: CLIP ViT-L/14 @ 336 (congelado durante la etapa 1, opcionalmente descongelado etapa 2 / 第一阶段结,第二阶段可选解).
- Proyector / 投影器: 2 capas MLP con activación GELU / 2 capas MLP + GELU激活, `1024 → 4096 → 4096`¿ Qué ?
- LLM / 语言模型: Vicuna-13B (más tarde Llama-3.1-8B / 后续使用 Llama-3.1-8B).

Envía una imagen + texto en el momento:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

La imagen ocupa 576 tokens del contexto LLM. En 2048 contexto, eso deja 1472 tokens para el texto.

> **【中文解读】**En 2048 en la ventana de texto anterior, esto representa un 28%, sólo quedan 1472 en el texto anterior; pero en la 32k en la siguiente, esto casi puede ser ignorado.

### Etapa 1: Alineación del proyector.

Freeze ViT. Freeze LLM. Entrenar sólo el MLP de 2 capas. Dataset: 558k pares de imagen-capción (LAION-CC-SBU).

En una sola época en lote 128 esto se hace en unas pocas horas. El proyector aprende a mapear el espacio ViT al espacio LLM.

> **【中文解读】**Primer paso: Con 2 niveles de MLP, se ha realizado un entrenamiento de 558k gráficos, para que el aprendizaje de ViT pueda ser realizado en un espacio de programación de MLP.

### Etapa 2: ajuste de instrucciones visuales.

Deshielo del proyector (todavía se puede entrenar). Deshielo del LLM (generalmente completamente, a veces LoRA). Entrenamiento en 158k vueltas de instrucción visual.

Los datos de instrucciones son el truco.
1. Toma una imagen de COCO.
2. Extraer la descripción del texto (5 subtítulos humanos + lista de cuadro de límite).
3. Envía a GPT-4 con tres plantillas de instrucciones:
   - Conversación / 对话: "Generar un diálogo de ida y vuelta entre un usuario y un asistente sobre esta imagen".
   - Descripción detallada / 详细描述: "Dá una descripción rica y detallada de la imagen".
   - Razonamiento complejo: "Pregúntale una pregunta que requiera razonamiento sobre la imagen, y luego contestela".
4. Parsear la salida de GPT-4 en (instrucción, respuesta) pares.

Nada de esto toca directamente a la imagen  sólo la descripción del texto. GPT-4 alucina el contenido de imagen plausible.

> **【中文解读】**关键创新: la generación de datos no se encuentra en contacto con la imagen en sí misma sólo con la descripción textual GPT-4 会"幻觉" de un contenido de imagen razonable, aunque habrá ruido, pero 158k 条数据足以解锁对话能力 Este modo de "con modelos fuertes generar datos de entrenamiento de modelos" fue ampliamente adoptado más tarde (como Auto-Instruir, Alpaca, etc.)

> ¿ Qué es esto ?**【困惑】**P: GPT-4 没看图只看描述,那 LLaVA 训练时实际学学的"视觉"是什么?A: LLaVA 学习是两件事: 1) 投影机把 ViT 的视觉特征翻译成 LLM 能理解的语义; 2) LLM 学会"见图片 → 生成符合GPT-4风格的描述"――GPT-4 的"幻觉"实际上是合理的描述(基于标题),所以最终 LLaVA 也能产生合理的描述──
> ️ **【易错点】**Auto entrenamiento LLaVA 时数据不清洗 → GPT-4 de la iluminación contaminación entrenamiento,模型可能描述图中没有的东西──修复:使用 GPT-4V(多模态版本) sustituir el texto puro GPT-4,让 GPT-4V 真的看图生成描述(ShareGPT4V就是这个思路),质量更高──

> **【拓展：数据合成的范式意义】**El método de síntesis de datos de LLaVA (GPT-4 生成指令数据) ha abierto una nueva modalidad de ingeniería de datos de VLM.

### ¿Por qué la comunidad copió esto? ¿Por qué la comunidad ha seguido?

- No hay pérdidas específicas de la etapa 1 para sintonizar. pérdida de LM en todo.
- El proyector se prepara en horas, no en días.
- LLM se puede intercambiar (LLaVA-Llama2, LLaVA-Mistral, LLaVA-Llama3) mediante la reeducación del proyector.
- La tubería de datos de instrucción visual utiliza GPT-4 y es barata para regenerarse para un nuevo dominio.

### LLaVA-1.5 y LLaVA-NEXT.

LLaVA-1.5 (octubre 2023) añadido:  LLaVA-1.5  2023年10月) 新增:
- Los datos de tareas académicas (VQA, OKVQA, RefCOCO) se mezclan en la sintonía de instrucciones.
- Mejor sistema de sugerencias.
- 2048 → 32k contexto.

LLaVA-NeXT (enero 2024) añadido: ➡️ LLaVA-NeXT(2024年1月) 新增:
- AnyRes: dividir imágenes de alta resolución en una cuadrícula de 2x2 o 1x3 de 336 crops, más una miniatura global de baja resolución. Cada crop se convierte en 576 tokens; un total de alrededor de 2880 tokens visuales por imagen. Las tareas de OCR y gráfico saltaron.
- Mejor mezcla de datos de instrucciones con ShareGPT4V (capciones de alta calidad GPT-4V).
- Más fuerte base LLM (Mistral-7B, Yi-34B).

> **【拓展：AnyRes 与高分辨率理解】**AnyRes es una tecnología clave para procesar imágenes de alta resolución. Para los informes en el escenario financiero, las imágenes de archivo, las emisións y otros, la alta resolución es fundamental para entender.

### LLaVA-OneVision

Lección 12.08 cubre OneVision en profundidad. versión corta: el mismo proyector, pero entrenado con un plan de estudios que cubre una sola imagen, una imagen múltiple y un video en un modelo con un presupuesto compartido de tokens visuales.

> **【中文解读】**Sección 12.08 课将深入讲解 OneVision──简言之: utilizar el mismo proyector, pero a través del curso aprender a cubrir un único gráfico, un gráfico y un vídeo tres tareas, en un modelo compartiendo el token de visión 预算──

### La comparación con Q-Former con Q-Former

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

MLP gana en la simplicidad y la flexibilidad de tokens. Q-Former gana en el presupuesto de tokens. A finales de 2023 el presupuesto de tokens ya no era la restricción vinculante (los contextos LLM crecieron a 32k-128k +) y la simplicidad dominó.

> **【中文解读】**MLP en la flexibilidad y la flexibilidad de los tokens, Q-Former en el token  presupuestos  ganar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

> ¿ Qué es esto ?**【困惑】**¿Por qué no se ha puesto LLaVA en Q-Former?加加复杂度变高、训练难度大、收益小( excepto en vídeos como este 预算紧张场景)。2) LLaVA-1.5 和 LLaVA-NeXT El que se debe seleccionar? 默认 LLaVA-NeXT(support high resolution AnyRes, OCR 和文档任务更强)。

### El formato de la llamada .

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`El Tokenizer ve una secuencia ligeramente más larga de lo que se ha entrenado, pero el LLM maneja la entrada nueva porque la etapa 1 lo enseñó.

> **【中文解读】** `<image>`Es el token de posición que se sustituye por 576  o 2880  en cualquier modo. LLM es capaz de procesar estas entradas nunca antes vistas, porque la primera fase de entrenamiento le ha enseñado a entender las entradas de proyección.

### Economía de parámetros.

LaVA-1.5-7B descomposición:
- CLIP ViT-L/14 @ 336: 303M (estadio congelado 1, a menudo descongelado 2 / 第一阶段结,第二阶段通常解).
- Proyector (2x lineal) / 投影器: ~22M entrenable / 可训练.
- Llama-7B: 7B.
- Total / 总计: 7.3B parámetros. Entrenable durante la etapa 2 / Segunda fase: proyector completo 7B + 22M / 全部7B + 22M proyector.

El costo de entrenamiento para la etapa 2: ~ 20 horas en 8xA100. Este es el número clave  un día, un nodo, reproducible.

> **【中文解读】**El segundo paso de la formación: 8 张 A100 跑约20小时──这是关键数字一天──一台机器──可复现──这是LLaVA 能够迅速传播的原因──
```figure
mm-llava-projector
```

## Usalo

## Usalo en práctica.

`code/main.py`Los instrumentos:`code/main.py`实现:

1. El proyector de 2 capas MLP (dim 16 → 32 → 32 para la escala de juguete) en Python puro.
2. El sistema de construcción rápida: sistema rápido + `<image>`se sustituye por N tokens proyectados + turno de usuario + generador de lugar asistente.`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符──
3. Un visualizaje de cómo se ve el bloque visual de 576 tokens en el contexto de LLM (percentual de 2k / 32k / 128k contexto consumido).

## Envíalo .

Esta lección produce`outputs/skill-llava-vibes-eval.md`. Dado que el punto de control de la familia LLaVA, se ejecuta una suite de vibraciones de 10 pulsaciones (3 subtítulos, 3 VQA, 2 razonamientos, 2 rechazos) y se informa de una tarjeta de puntuación legible por el ser humano.

> **【中文解读】**本课产 出  `outputs/skill-llava-vibes-eval.md` Dado un punto de control de la serie LLaVA, ejecutar 10 个提示的"vibes-eval" 测试套件(3 descripciones、3 VQA、2推理、2 rechazo), generar resultados artificiales  Este no es un test de base formal, sino un test de humo, para confirmar la buena conexión entre proyector y LLM 

## Los ejercicios.

1. Calcule el recuento de parámetros de formación para el proyector MLP de 2 capas en `1024 → 4096 → 4096`Con GELU y sesgo, ¿qué fracción de LLaVA-13B representa?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. Construir una solicitud de LLaVA para un caso de "rechazo"  la imagen contiene un individuo privado. Escribir la respuesta de asistente esperada. ¿Por qué debería LLaVA rechazar este tiro cero y qué datos de capacitación se necesitarían para reforzar la negativa?
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. Lea la sección AnyRes del blog LLaVA-NeXT. Compute el recuento de tokens visuales para una imagen de 1344x672 en AnyRes. Compara con 576 tokens de base en 336x336.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. El proyector LLaVA etapa 1 está entrenado con pérdida de LM en los títulos. ¿Qué sucede si se salta la etapa 1 y se va directamente a la etapa 2 (la sintonización de instrucciones visuales)?
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. LLaVA-Instruct-150k utiliza GPT-4 con capciones COCO para generar instrucciones. Para un nuevo dominio (rayos X médicos, imágenes satelitales), describa la tubería de datos de cuatro pasos para generar instrucciones de dominio. ¿Qué podría salir mal en cada paso?
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## Más Leer más Leer más

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485)¿Qué es esto?
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744)¿Qué es esto?
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793) conjunto de datos de subtítulos densos.  密集描述数据集
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) Ablaciones de diseño-espacio.
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) Unified single-image, multi-image, video. 统一单图多图视频的版本
