# T5, BART  Modelos de codificación y decodificación  T5 BART  Modelo de codificación y decodificación

> Los codificadores entienden. Los decodificadores generan. Ponlos de nuevo juntos y obtienes un modelo construido para las tareas de entrada → salida: traducir, resumir, reescribir, transcribir.

> **【中文解读】**T5 Colocar todas las tareas de PNL en formato texto a texto. BART Usar para hacer el ruido de código de entrenamiento.

**Type:** Study | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Cada una de las dos funciones de GPT y BERT, sólo para decodificadores, se desprende de la arquitectura de 2017 para un objetivo diferente.

> 解码器专用 GPT 和编码器专用 BERT han refinado de forma independiente la estructura del año 2017 para diferentes objetivos.

- Traducción: Inglés → Francés.
  En inglés, el idioma es el idioma de la lengua inglesa.
- Resumen: artículo de 5,000 tokens → resumen de 200 tokens.
  中文翻译:摘要: 5.000 tokens 文章 → 200 tokens 摘要。
- Reconocimiento de voz: tokens de audio → tokens de texto.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Latin".
- Extracción estructurada: prosa → JSON.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "JSON"".

Para estos, el codificador-decodificador hace el ajuste más limpio. El codificador produce una representación densa de la fuente. El decodificador genera la salida, atendiendo cruzada a esa representación en cada paso. El entrenamiento es de cambio por uno en el lado de salida. La misma pérdida que GPT, solo condicionada a la salida del codificador.

> Para estas tareas, el codificador-descodificador es la opción más adecuada. El codificador genera un código de datos.

Dos papeles definieron el libro de juegos moderno:

> 两篇论文 define el moderno paradigma:

1. **T5**(Raffel et al. 2019). "Transformador de transferencia de texto a texto". Cada tarea de NLP se reformula como texto-en, texto-fuera. Arquitectura única, vocabulario único, pérdida única. Pretrainado en predicción de tiempo enmascarado (espacios corruptos en la entrada, decodificarlos en la salida).
   En inglés:**T5**(Raffel 等人,2019) ――"文本到文本迁移变压器"― cada tarea de NLP se redefine como文本输入文本输出―单一架构、单一词表、单一损失― con el uso de los pasos de un proyecto de predicción para realizar un entrenamiento previo 
2. **BART**(Lewis et al. 2019). "Transformador bidireccional y auto-regresista". Deniando autoencoder: entrada corrupta de múltiples maneras (interferir, máscarar, eliminar, girar), pida al decodificador que reconstruya el original.
   En inglés:**BART**(Lewis 等人,2019) ――"双向自归转变器"──去噪自编码器:用多种方式破坏输入(打乱、掩码、删除、旋转),要求解码器重建原始文本──

En 2026 el formato de codificador-decodificador se mantiene en donde la estructura de entrada importa:

> En 2026, el formato de codificador-descodificador continúa existiendo en escenarios importantes de la estructura de entrada:

- Susurro (habla → texto).
  En el caso de los niños, el uso de la lengua se debe a la presencia de la lengua.
- La pila de traducciones de Google.
  En inglés, el nombre de la página web de Google es "Google".
- Algunos modelos de complementación / reparación de código que tienen estructuras de contexto y edición distintas.
  Algunos tienen un código completo/rehabilitado en el texto siguiente.
- Flan-T5 y variantes para tareas de razonamiento estructurado.
  La estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.

Sólo el decodificador ganó el foco, pero el decodificador nunca se fue.

> El modelo de descifrador ha ganado la luz de la polluoro, pero el descifrador nunca ha desaparecido.

> **【中文解读】**编码器-解码器架构在"输入→输出" estructuramiento de tareas todavía tiene ventajas. T5 va a unir todas las tareas de NLP en formato texto a texto, BART utilizar para hacer ruido de codificación de entrenamiento. Aunque en el campo de la producción de texto puro sólo fue sustituido por el Decoder, pero en el reconocimiento de idiomas (语音识别(Whisper) 翻译、摘要等任务中仍然是最佳选择.

## El concepto central.

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### El bucle hacia adelante

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

El decodificador se ejecuta autoregresivamente pero atende cruzando a la salida del * mismo* codificador en cada paso.

> El clave es que el codificador solo se ejecuta una vez por cada entrada. El descifrador se vuelve a funcionar, pero en cada paso se intercambia la misma cantidad de código.

> **【中文解读】**交叉注意力是编码器-解码器架构的信息桥梁:Q de los编码器,K/V de los编码器输出;;编码器只运行一次(高效),解码器每步都通过交叉注意力访问编码器的完整输出;;

> **【拓展：Whisper 的编码器-解码器设计】**El modelo de reconocimiento de idiomas de Whisper de OpenAI utiliza la arquitectura de codificadores-des codificadores, ya que el formato de los idiomas de Whisper es completamente diferente.

### T5 Preentrenamiento  Corrupción de la duración

Seleccione intervalos aleatorios de la entrada (lengitud promedio de 3 tokens, 15% total).`<extra_id_0>`¿ Qué ?`<extra_id_1>`, etc. El decodificador sólo saca los espacios corruptos con su prefijo sentinela:

> 随机选择输入中的片段( media de longitud 3 个代币,总计 15%) ⋅ con el único señalización del enviado para reemplazar cada fragmento:`<extra_id_0>`¿Qué es esto?`<extra_id_1>`... sólo emitir fragmentos de la destrucción y sus enviados:

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

Una señal más barata que predecir toda la secuencia, competitiva con el MLM (BERT) y el prefijo-LM (UniLM) en la ablación del papel T5.

> En el experimento de desintegración de los trabajos de T5, la competencia es equivalente a la de MLM (BERT) y de LM (UniLM) anteriores.

### BART preentrenamiento  Denuncia de múltiples ruidos

BART prueba cinco funciones de ruido:

> BART 尝试五种噪声函数:

1. Enmascaramiento de tokens.
   En inglés, "Token" se traduce en "token" (token).
2. Eliminación de tokens.
   En inglés, "Token" se usa para eliminar los nombres.
3. Infiltramiento de texto (mascarar un espacio, el decodificador inserta la longitud correcta).
   En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.
4. Permutación de oraciones.
   En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.
5. - La rotación de documentos.
   En inglés, el texto se traduce en inglés como "cambio de palabras".

La combinación de texto de relleno + permutación de oraciones produjo los mejores números en el torrente descendente. El decodificador siempre reconstruye el original. La salida de BART es la secuencia completa, no solo los intervalos corrompidos , por lo que el cálculo pre-entrenamiento es mayor que T5.

> 组合文本填充 + 句子排列产生了最佳下游效果──解码器总是重建原文本──BART's output is a complete sequence, not just a broken fragment thus pre-training computing volume is higher than T5──BART's output is a complete sequence, not just a broken fragment thus pre-training computing volume is higher than T5──BART's output is a complete sequence, not just a broken fragment thus pre-training computing volume is higher than T5──BART's output is a complete sequence, not just a broken fragment thus pre-training computing volume is higher than T5──BART's output is a complete sequence, not just a broken fragment

> **【中文解读】**T5 y BART de la pre-entrenamiento estrategia diferente: T5 de la duración de la corrupción sólo predice que se destruyen los fragmentos de la producción de alta eficiencia, BART de la eliminación de ruido se codifica reconstruir toda la serie de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de

### Inferencia

La misma generación autoregressiva que GPT. Se aplica el muestreo codicioso / viga / top-p. La búsqueda de viga (ancho 45) es estándar para la traducción y resumen porque la distribución de salida es más estrecha que el chat.

> 推理与 GPT的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) es la estrategia estándar de traducción y resumen, ya que la distribución de la salida es más estrecha que la de diálogo──

> **【拓展：Beam Search 在翻译中的重要性】**编码器-解码器模型在翻译和摘要任务中常用束搜索 (宽度 4-5),因为输出分布较窄. 束搜索维护多个候选序列,每步保留得分最高的几个继续扩展. 束搜索比贪心搜索,beam search 能找到更优的全局序列. 束搜索比随机采样,它更稳定.

### Cuándo elegir cada variante en 2026

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

La tendencia desde ~2022: sólo el decodificador se hace cargo de las tareas que el decodificador-encodificador solía poseer porque (a) los LLM solo con decodificador sintonizados con instrucciones se generalizan a cualquier cosa a través de la solicitud, (b) una arquitectura se escala más fácilmente que dos, (c) RLHF asume un decodificador.

> Desde 2022 la tendencia: el descifrador especial asumió las tareas que el codificador-descifrador ya tenía, ya que (a) la instrucción de un LLM de descifrador especial puede ampliarse a cualquier tarea a través de la sugerencia, (b) una sola estructura es más fácil de expandir que dos, (c) RLHF 假设使用解码器──编码器-解码器在输入模态不同(语音、图像) 或束搜索质量很重要时仍然有用──

> **【拓展：T5 的 text-to-text 统一范式】**El proyecto de T5 se centra en la creación de un nuevo programa de investigación y desarrollo de la tecnología de la información y de la información.

## Construye y realiza.
```figure
encoder-decoder
```

## Construye el mismo

¿ Qué ?`code/main.py`Implementamos la corrupción de la extensión de estilo T5 para un corpus de juguetes la pieza más útil de esta lección porque aparece en cada receta de preentrenamiento de codificador-decodificador desde entonces.

> 参见 `code/main.py`                                                                                                                                                                                                                                                              

### Paso 1: Corrupción de la extensión

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

El formato objetivo es la convención T5: `<sent0> span0 <sent1> span1 ...`La entrada corrompida intercaja tokens sin cambios con los tokens sentinel en ubicaciones de span.

> 目标格式遵循 T5 约定:`<sent0> span0 <sent1> span1 ...` Entradas destruidas se convertirán en tokens sin cambios y en tokens de los oficiales de la posición de la misión 交替排列──

### Paso 2: verifique el viaje de ida y vuelta

Dado el dato corrupto y el objetivo, reconstruye la oración original. Si su corrupción es reversible, el pase hacia adelante está bien definido. Esta es una verificación de la cordura  el entrenamiento real nunca hace esto, pero la prueba es barata y detecta errores individuales en su contabilidad de tiempo.

> 给定被破坏的输入和目标,重建原始句子──如果破坏是可逆的,前向传播就是良定义的──这是一个合理性检查真实训练从不这样做,但测试成本低且能发现片段簿记中的差一错──

### Paso 3: ruido BART

Cinco funciones: `token_mask`¿ Qué ?`token_delete`¿ Qué ?`text_infill`¿ Qué ?`sentence_permute`¿ Qué ?`document_rotate`Componen dos de ellos y muestren el resultado.

> 五个函数:`token_mask`¿Qué es esto?`token_delete`¿Qué es esto?`text_infill`¿Qué es esto?`sentence_permute`¿Qué es esto?`document_rotate`◊ 组合 de los dos y mostrar resultados

## Usalo con el marco de ejecución

Enlace de abrazo:

> AbrazosFace 参考:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

El truco T5: el nombre de la tarea entra en el texto de entrada. El mismo modelo maneja docenas de tareas porque cada tarea es de texto en, texto fuera. En 2026 este patrón ha sido generalizado por modelos de decodificación solo con instrucciones, pero T5 lo codificó primero.

> T5 de habilidades: el nombre de tareas escrito en el texto de entrada. El mismo modelo puede procesar docenas de tareas, ya que cada tarea es de entrada de texto y salida de texto. En 2026, este modelo ha sido ordenado por el decodificador de la modelaje de la codificación de la generalización, pero T5 es el primero en regularizar.

## Envíe el producto .

¿ Qué ?`outputs/skill-seq2seq-picker.md`. La habilidad escoge entre codificador-decodificador y decodificador-solo para una nueva tarea dada la estructura de entrada-salida, la latencia y los objetivos de calidad.

> 参见 `outputs/skill-seq2seq-picker.md` Esta habilidad se basa en la estructura de entrada-salida, retraso y objetivo de calidad, para nuevas tareas seleccionar un codificador-descodificador o una estructura especial de descodificador.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`, aplicar la corrupción de la franja de tiempo a una oración de 30 tokens, verificar que la concatenado de los tokens fuente no sentinel con los espacios de destino decodificados reproduce el original.
   Traducción:运行`code/main.py`, para una frase de 30 tokens aplicaciones destrucción, verificación será un token de origen no oficial y el código de desactivar el objetivo de fragmentos de texto puede ser recuperado original texto.
2. **Medium.**Implementar el BART `text_infill`ruido: sustituir los espacios aleatorios por un solo `<mask>`El decodificador debe inferir la longitud correcta de la franja más el contenido. Muestre un ejemplo.
   En español: implementar BART`text_infill`噪声: con un solo `<mask>`El descifrador debe deducir la longitud y contenido de un video correcto.
3. **Hard.**- No . - ¿ Qué ?`flan-t5-small`En un pequeño corpus inglés → cerdo-latino (200 pares).`Llama-3.2-1B`en los mismos datos con el mismo cálculo.
   En español: en pequeño inglés en latín porco 语料库(200 对)`flan-t5-small` 50 puntos de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la`Llama-3.2-1B`En comparación.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Más Leer más Leer más

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) T5.
  En el texto original, el texto se traduce en inglés como "T5 论文").
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461)- ¿Qué es eso?
  En inglés, el nombre de la palabra "BART" se refiere a la palabra "BART".
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) Flan-T5.
  El texto de la ley es el siguiente:
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Whisper, el codificador-decodificador canónico de 2026.
  China: Whisper 论文, 2026 年典型编码器-解码器模型──
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) aplicación de referencia.
  En el caso de los niños, el uso de la lengua se puede realizar en el interior de la casa.
