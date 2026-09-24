# InternVL3: Entrenamiento Multimodal Nativo

> Cada VLM abierto antes de InternVL3 siguió la misma receta de tres pasos: tomar un texto LLM entrenado en billones de tokens de texto, conectar un codificador de visión, y luego ajustar las costuras. Esto funciona pero tiene deuda de alineación  el texto LLM ha gastado todo su presupuesto pre-entrenamiento en texto puro y no entiende nativamente los tokens visuales. Cuando se añade visión post hoc, el LLM tiene que volver a aprender a relacionar la entrada visual con su razonamiento del texto sin olvidar el texto. InternVL3 (Zhu et al., abril 2025) rechaza el enfoque post hoc: una carrera previa al entrenamiento, texto y multimodal entrelazados desde el primer paso. El resultado coincide con Gemini 2.5 Pro en MMMU-Pro en 78B parámetros abiertos. Esta lección lee el caso de la preentrenamiento nativo y lo que cambia cuando lo haces.

> **【中文解读】**Innovación central de InternVL3: rechazar el "pré-trainamiento de texto LLM Reconectamiento de texto codificador" de la versión posterior, cambiado desde el primer paso en el texto y el formato de datos de la formación de la comunicación. Esto elimina la "combinación de la deuda" de la versión posterior de VLM.

> **【拓展：原生预训练 vs 后装的成本权衡】**El entrenamiento previo a la vida eliminó la deuda, pero el costo es mucho mayor que el plan de montaje posterior. Requiere millones de GPUs de tiempo de entrenamiento inicial, y abandona la flexibilidad de reemplazar a la vez la base de LLM. Para la mayoría de los proyectos, el plan de montaje posterior sigue siendo más económico. Sólo cuando su tamaño alcanza la necesidad de entrenar un nuevo modelo de base, el entrenamiento previo a la vida original vale la pena considerar.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

> ¿ Qué es esto ?**【前置】**學本節前 請先掌握:Fase 12·05(LLaVA 后装方案) 、Fase 12·07(開源VLM 配方) 。本節是"反LLaVA"拒后装,主张原生多模态预训──
> ¿ Qué es esto ?**【类比】**后装 VLM(LLaVA) = "成年后学外语" ya ha dominado la lengua materna ((文本),再艰难学第二语言 ((视觉) ・・・
> ¿ Qué es esto ?**【困惑】**P: 既然原生预训练如此好, ¿por qué LLaVA 仍然主流?  成本!原生预训练需要数百万GPU 小时从头跑(一次 ~数百万美元),后装 LLaVA只需8×A100 跑一天──除非你是大厂从头训新模型,否则 LLaVA 路线性价格比高得多──

## Objetivos de aprendizaje

- Explica por qué el entrenamiento post hoc de VLM acumula deuda de alineación, citando los tres síntomas medibles (olvido catastrófico, deriva de respuesta, inconsistencia visual-texto).
- Describa la mezcla de cuerpo de entrenamiento nativo de InternVL3 y por qué la proporción de texto: interconectado: subtítulo importa.
- Compare V2PE (codificación de posición visual variable) con el M-RoPE de Qwen2-VL.
- Nombre de la Optimización de implementación del Router de Resolución Visual (ViR) y lenguaje de visión descoplado (DvD).

## El problema es el contexto del problema

El entrenamiento post-hoc VLM es el predeterminado. LLaVA, BLIP-2, Qwen-VL, Idefics  todos toman un LLM ya pre-entrenado (Llama, Vicuna, Qwen, Mistral) y agregan visión.

1. LLM congelado + codificador de visión congelado + proyector entrenable, entrenado en pares de captura para alinear las incorporaciones.
2. Descongelar el LLM, entrenar en datos de instrucción (LLaVA-Instruct, ShareGPT4V).
3. Opcional para la tarea específica.

Tres síntomas de la deuda de alineación aparecen:

- El VLM post hoc olvida las habilidades de texto solo. Las puntuaciones GSM8K caen 5-10 puntos. Las puntuaciones Hellaswag caen.
- Respuesta deriva / 回答漂移. Frases pequeñas de la misma pregunta visual obtienen respuestas diferentes. El codificador de visión se conecta con el LLM con vínculos más débiles que los tokens del LLM.
- Incoherencia visual-textual / 视觉-文本不一致. El VLM puede describir una imagen correctamente y luego responder a una pregunta que contradice su propia descripción.

> **【中文解读】**后装 VLM的三种对齐债务:(1) 灾难性遗忘GSM8K 掉 5-10 分;(2) 回答漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移

## El concepto central.

### Preentrenamiento nativo multimodal

InternVL3 se desarrolla desde cero en un corpus que es nativo multimodal desde el primer paso. La mezcla es:

- 40% de datos sólo de texto (FineWeb, Proof-Pile-2, etc.) / 40% 纯文本数据
- 35% de datos de texto-imagen entrelazados (OBELICS, estilo MMC4) / 35% 交织图文数据
- 20% de datos de captura de imagen en pareja / 20% 图文配对数据
- 5% de datos de vídeo-texto / 5% 视频文本数据

Los tokens de visión, los tokens de texto y las interacciones transmódales participan en la misma pérdida desde el primer paso de gradiente.

El modelo base es una etapa única, y se sigue la instrucción, pero el modelo base ya entiende los tokens visuales como ciudadanos de primera clase.

> **【中文解读】**InternVL3 desde el primer paso se incorporará el token de visión, el token de texto y el token de forma transmodelo en la misma función de pérdida.

### V2PE (codificación de posición visual variable)

Qwen2-VL utiliza M-RoPE con asignación de eje fijo. InternVL3 introduce V2PE: el codificación de posición varía según el tipo de modalidad (texto, imagen, video) con escalabilidad de aprendizaje.

- Los tokens de texto obtienen posición 1D (índice de texto).
- Los parches de imagen obtienen posición 2D (linia, columna).
- Los cuadros de vídeo tienen posición 3D (tiempo, fila, col).

Los tres comparten la misma base de frecuencia RoPE, pero la asignación de oscuridad oculta por banda es un parámetro aprendido en lugar de una división fija.

La afirmación de ablación de V2PE: 1-2 puntos en los puntos de referencia de vídeo sobre M-RoPE en el mismo cálculo.

> **【中文解读】**Diferencias entre V2PE y M-RoPE: la distribución de dimensiones ocultas entre los diferentes niveles de frecuencia es de parámetros de aprendizaje y no de división fija. El modelo puede medir automáticamente el tiempo y la frecuencia de espacio en el proceso de entrenamiento previo.

### Router de resolución visual (ViR)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

Optimización de implementación. No todas las imágenes necesitan codificación de resolución completa. Una foto con un objeto en bajo detalle desperdicia tokens cuando se codifica en 1280px nativo. ViR es un clasificador pequeño que predice la resolución mínima necesaria para responder a la pregunta, antes de codificar.

El enrutamiento tiene tres niveles: bajo res (256 tokens), medio (576), alto (2048+). Para el 60% de las consultas en el tráfico de producción, es suficiente bajo o medio. Efecto neto: 2-3x de rendimiento a la misma calidad.

> **【中文解读】**ViR es la optimización de la implementación: una pequeña clasificación en una pequeña resolución de la consulta de pre-previsión en el código.

> **【拓展：ViR 与金融场景】**En el tratamiento de archivos financieros, la mayor parte de las consultas (como "el monto total de este emisión es cuánto") sólo requieren baja resolución, pero las tareas de OCR (como "extraer todos los proyectos") requieren alta resolución.

### Desacoplado de la lengua de visión (DvD) 解视觉-语言部署

Cuando se sirve un VLM grande, el codificador de visión se ejecuta una vez por imagen, pero el LLM se ejecuta autoregresivamente para cada token de salida. Los dos componentes tienen diferentes cuellos de botella (visión = ancho de banda de memoria de GPU para conv + atención; LLM = caché KV).

Para un modelo de codificador 8B + 400M, DvD aproximadamente duplica el rendimiento por nodo frente a co-localizado.

> **【中文解读】**DvD se distribuirá en diferentes GPUs, a través de conexiones de transmisión de flujo.

### Una etapa vs calidad de varias etapas.

El primer punto de referencia de InternVL3 es que en 78B params, coincida con el MMMU-Pro de Gemini 2.5 Pro. En 38B, coincida con el GPT-4o. En 8B, lidera el tablero de clasificación de 8B abierto. Todo en una receta de preparación de una sola etapa + instrucción-tune.

La hipótesis de la deuda de alineación es medible: InternVL3-8B pierde menos puntos de referencia de texto (MMLU, GSM8K) que Qwen2.5-VL-7B por unidad de ganancia de referencia de visión.

> **【中文解读】**InternVL3-8B Cada uno obtiene un aumento de la base de datos de la visión, pérdida de la base de datos de texto de la Qwen2.5-VL-7B menor.

### El procedimiento de evaluación de las medidas de seguridad

InternVL3.5 (agosto 2025) escala la receta. El mismo enfoque nativo de pretrain, más datos, más parámetros. Las mejoras en MMMU son incrementales.

InternVL-U (2026) añade la generación unificada  de imagen a través de cabezas MMDiT en la parte superior de la misma columna vertebral. La "U" significa "Entendimiento + generación", que persigue modelos unificados de estilo Transfusión (Lección 12.13).

> **【中文解读】**InternVL-U(2026) se ha unido a la capacidad de generación de imágenes en el mismo tronco (a través de MMDiT) para buscar la comprensión de la Transfusión 风格的理解+生成统一模型──

### Compromiso de la preparación nativa.

El preentrenamiento nativo no es gratuito:

- Computación / 计算. Entrenar un nuevo VLM desde cero cuesta lo mismo que entrenar un texto LLM  millones de horas de GPU. La adaptación post-hoc reutiliza los pesos existentes de LLM, ahorra la mayor parte del costo.
- Datos / datos. Corporaciones de imagen y texto interrelacionadas a escala son raras. OBELICS es 141M documentos; MMC4 es 571M. El texto solo se envía a fichas de 15T. La escasez de datos de preentrenamiento multimodal es una restricción dura.
- La formación preescolar nativa deja de lado la opción de presentar una nueva LLM más tarde. Post-hoc permite cambiar Llama-3.1 por Llama-4 mediante la reentrenamiento sólo del adaptador.

La apuesta que InternVL3 hace: la deuda de alineación es peor que la pérdida de reutilización. Los puntos de referencia respaldan la afirmación. El costo de producción impide que los laboratorios futuros replicen a bajo costo.

> **【中文解读】**La evaluación de los resultados de los estudios de investigación de la Universidad de Chicago (U.S.) y de la Universidad de Chicago (U.S.) se basan en el estudio de la investigación de la investigación de la Universidad de Chicago (U.S.).

## Usalo en práctica.
```figure
l5-native-pretrain
```

## Usalo

`code/main.py`es un mezclador de entrenamiento y un simulador de enrutador ViR.

- Toma una mezcla de corpus objetivo (% texto, % interleaved, % caption, % video) y calcula los pasos esperados por modalidad.
- Simula el enrutamiento de ViR en un lote de consultas (distribución: 50% de bajo detalle, 30% medio, 20% de alto detalle) y informa el recuento promedio de tokens.
- Reporta estimaciones de rendimiento de DVD dado en codificador vs LLM FLOPs.
- Imprime un lado a lado de post-hoc vs nativo pre-entrenamiento en parámetros, computación, datos, y los síntomas de alineación-deuda esperados.

## Envíalo .

Esta lección produce`outputs/skill-native-vs-posthoc-auditor.md`. Dado que se propone un plan de formación para el VLM, el programa evalúa si se debe realizar una formación nativa o post-hoc, señala el riesgo de alineación y deuda y recomienda una combinación de corpus.

> **【中文解读】**Este curso se desarrolla en el marco de la formación de la formación en materia de gestión de la rentabilidad y de la rentabilidad de los proyectos de desarrollo de la empresa.

## Los ejercicios.

1. Estima el delta de cálculo entre InternVL3-8B (pre-treino nativo) y LLaVA-OneVision-7B (post-hoc).
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 informa 40% de texto / 35% entrelazado / 20% de título / 5% de vídeo. Si su tarea objetivo es video-pesado, proponga una nueva proporción y argumentar por qué el modelo base todavía necesita datos sustanciales de texto y título.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. En el caso de los niños, el número de niños que se han ido a estudiar en el instituto de formación de post hoc es el número de niños que han tenido que regresar a la escuela.
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. ViR envía el 60% del tráfico a codificación de baja resolución. ¿Qué tipos de consultas desvía (envía a baja resolución cuando se necesita alta resolución)? Propón tres modos de falla del router.
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. DvD divide la visión y LLM en GPUs separadas. ¿Bajo qué patrón de tráfico DvD perjudica el rendimiento en lugar de ayudar?
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Más Leer más Leer más

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238)¿Por qué no me gusta?
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)♬ Entrenamiento de la vida de la VL3
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265)➡️ Expansión de la escala de InternVL3.5
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)♬ InterVL-U Comprender + generar unidad
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566) MM1.5 para la cuantificación de la deuda
