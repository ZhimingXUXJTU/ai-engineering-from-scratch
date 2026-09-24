# Traducción automática

> La traducción es la tarea que pagó la investigación de PNL durante treinta años y sigue pagando ahora.
> 翻译是为NLP研究买单三十年的任务, ahora todavía continúa.

> **【中文解读】**Desde la información de la máquina de traducción hasta la de la máquina de traducción.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## El problema es la introducción del problema

Un modelo lee una oración en un idioma y produce una oración en otro. La longitud varía. El orden de las palabras varía. Algunas palabras fuente se cartografian a múltiples palabras objetivo y viceversa. Los idiomas rechazan el mapeo uno a uno. "Te extraño" en francés es "tu me manques"  literalmente "me estás faltando".
> 模型读取一语言的句子并产生另一语言的句子──长度不同──词序不同── algunos de los términos de origen se encuentran en varios objetivos,反之亦然──习语拒绝对一映射── "Te extraño" es un término francés que significa "te extraño"  字面意思是"你对我是缺失的"──没有词级对齐能经受住这个──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


La traducción automática es la tarea que obligó a la PNL a inventar codificadores-decodificadores, atención, transformadores y, finalmente, todo el paradigma de LLM. Cada paso adelante llegó porque la calidad de la traducción era medible y la brecha entre humanos y máquinas era terca.
> La traducción automática es la necesidad de la PNL de inventar un codificador-descodificador, un transformador y, finalmente, toda la tarea del modelo de LLM. Cada paso hacia adelante es debido a la calidad de la traducción que se puede medir y la diferencia entre la persona y la máquina es constante.

Esta lección se salta la lección de historia y enseña la línea de trabajo de 2026: codificador-decodificador multilingüe preentrenado (NLLB-200 o mBART), tokenización de palabras, búsqueda de rayos, evaluación BLEU y chrF, y el puñado de modos de falla que aún se envían a la producción sin capturar.
> El programa de trabajo de la Universidad de California en San Francisco, California, fue publicado en el año 2000 por el Instituto de Ciencias de la Información y la Información de la Universidad de San Francisco.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

El decodificador genera el objetivo, una subpalabra a la vez, utilizando la salida del codificador a través de la atención cruzada (lección 10). El decodificación utiliza la búsqueda de haz para evitar la trampa de decodificación codiciosa. La salida se destokeniza, detruca y se califica en relación con una referencia.
> 现代 MT es un transformer entrenado en texto plano 编码器-解码器──编码器以其语言分词读取源语言──解码器通过交叉注意力 (第十课) utiliza la salida del codificador, cada vez que genera una palabra de su idioma objetivo──解码使用束搜索避免贪心解码陷──输出经过分词、去真实大小写处理,并与参考评分──

Tres opciones operativas impulsan la calidad de MT en el mundo real.
> Tres operaciones de transporte en el mundo real.

- **Tokenizer.**SentencePiece BPE se ha formado en un corpus de idiomas mixtos.
- **Model size.**NLLB-200 600M destilado se ajusta a una computadora portátil. NLLB-200 3.3B es el estándar de producción publicado. 54.5B es el límite máximo de investigación.
- **Decoding.**Ancho del haz de luz 4-5 para el contenido general. Penal de longitud para evitar una salida demasiado corta. Descifrado restringido cuando se necesita consistencia terminológica.
> - **分词器。**En el contexto de la formación en lenguaje mixto, la lengua común es la lengua común de la lengua.
- **模型大小。**NLLB-200 蒸 600M 适合笔记本。NLLB-200 3.3B es una producción publicada默认。54.5B es una investigación sobre el suelo。
- **解码。**Général contenu束宽度 4-5──长度惩罚避免输出过短──需要术语一致性时使用约束解码──

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.


## Construye y realiza.
```figure
seq2seq-alignment
```

## Construye el mismo

### Paso 1: una llamada de MT pre-entrenada
> Tres cosas son importantes.`src_lang`告诉分词器使用哪种文字和分割──`forced_bos_token_id`告诉解码器生成哪种语言── ambas son habilidades especiales de la NLLB; mBART 和 M2M-100

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Tres cosas importan aquí.`src_lang`Indica al tokenizer qué guión y segmentación aplicar. `forced_bos_token_id`El programa de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código
> BLEU 测量输出与参考之间的 n-gram 重叠──四种参考 n-gram 大小(1-4), precisión de la tasa de geometría media, a la hora de la salida de la información, en la medida en que la información es fácilmente disponible, pero difícil de entender.

### Paso 2: BLEU y chrF
>                                                                                                                                                                                                                                                               

BLEU mide superposición de n-gramos entre la salida y la referencia. Cuatro tamaños de n-gramos de referencia (1-4), media geométrica de precisiones, penalidad de brevedad para la salida demasiado corta. La puntuación es en [0, 100].
> 始终使用 `sacrebleu`                                                                                                                                                                                                                                                              

chrF mide la puntuación F de nivel de caracteres. Más sensible a los idiomas morfológicamente ricos donde el subconto BLEU coincide.
> 现代 MT 评估 utiliza tres indicadores complementarios.

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Siempre usar`sacrebleu`Normalisa la tokenización para que las puntuaciones sean comparables en todos los papeles.
> - **启发式**(BLEU、chrF)──快速、基于参考、可解释、对释义不敏感──用于遗留比较和归归检测──
- **学习型**(COMET、BLEURT、BERTScore) ⋅ En el juicio humano entrenado en el modelo neurológico; comparación traducción con la fuente y la semejamilidad de referencia ⋅ COMET Desde 2023 años, está relacionado con MT, es la producción estándar más importante de 2026 años de calidad ⋅
- **LLM 评委**(sin referencia)  Proposición: el modelo en el flujo 性、充分性、语调和文化适当性  GPT-4 评委在评分标准设计良好时与人类一致性约80%──用于没有参考的开放内容──

### La jerarquía de evaluación de tres niveles (2026)
> 2026 años de uso práctico:`sacrebleu`Para usar BLEU y chrF,`unbabel-comet`En el caso de los modelos de etiquetas de la UE, el modelo de etiquetas de la UE se utiliza para el uso de los datos de producción de datos de la UE.

La evaluación moderna de MT utiliza tres familias métricas complementarias.
> 无参考指标(COMET-QE、BLEURT-QE、LLM 评委) que le permita evaluar la traducción sin referencia, esto es muy importante para que no exista referencia.

- **Heuristic**(BLEU, chrF) Rápido, basado en referencias, interpretable, insensible a la paráfrase.
- **Learned**(COMET, BLEURT, BERTScore). Modelos neuronales formados en el juicio humano; comparación de similitud semántica de traducción con la fuente y la referencia. COMET tiene la mayor asociación con la investigación de MT desde 2023 y es el modelo de producción por defecto de 2026 cuando la calidad importa.
- **LLM-as-judge**(sin referencias). Promover un modelo grande para calificar las traducciones en fluidez, adecuación, tono, adecuación cultural. GPT-4 como juez coincide con el acuerdo humano en ~80% del tiempo cuando la rúbrica está bien diseñada.
> Up面工作流水线 El 80% del tiempo puede fluir, el 20% restante se encuentra en el estado de silencio.

Estampilla práctica para 2026: `sacrebleu`para BLEU y chrF, `unbabel-comet`Calibrar cada métrica con 50-100 ejemplos etiquetados por humanos antes de confiar en los datos de producción.
> - **幻觉。**模型发明源中没有内容──在不熟的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解: sobre el dominio de los términos de restricción de la resolución, sobre el contenido bajo control de la revisión de la mano de obra, control de la salida de la entrada de muchas más anormalidades──
- **偏离目标语言生成。**模型翻译成错误的语言――NLLB 在罕见语言对上出奇地容易出错――缓解:验证 `forced_bos_token_id`No siempre se utiliza el lenguaje de identificación de modelos de chequeo de salida.
- **术语漂移。**"Sign up" en el documento 1 se convierte en "s'inscribe", en el documento 2 en "creer un compte"── para la UI 文本和面向用户的字符串,一致性比原始质量更重要──缓解:词汇表约束解码或后编辑字典──
- **语体不匹配。**Para el contenido de los clientes, esto suele ser un error. Caution: si el modelo es apoyado, se utiliza el token del idioma como un consejo, o en el material formal.
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5源代币下面急剧下降──缓解:

Las métricas sin referencia (COMET-QE, BLEURT-QE, LLM-as-judge) le permiten evaluar las traducciones sin referencia, lo que es importante para los pares de idiomas de cola larga donde no existen traducciones de referencia.
> 预训模型是通才;;法律、医疗或游戏对话翻译从领域平行数据的微调中可测量地受益;; el programa no es complejo:

### Paso 3: qué se rompe en la producción
>  Muchas muestras de alta calidad en línea superaron cientos de millones de muestras de red de ruido                                                                                                                                                                                                                                                   

El tubo de trabajo anterior traducirá fluidamente el 80% del tiempo y fallará silenciosamente el 20% restante.

- **Hallucination.**El modelo inventa contenido que no estaba en la fuente. Común en el vocabulario de dominio desconocido. Síntoma: la salida es fluida pero afirma hechos que la fuente no declaró. Mitigation: decodificación restringida en términos de dominio, revisión humana de contenido regulado, monitoreo de salida mucho más tiempo que la entrada.
- **Off-target generation.**El modelo se traduce al idioma equivocado.`forced_bos_token_id`y siempre descifrar con un modelo de ID de idioma de verificación de salida.
- **Terminology drift.**"Registrar" se convierte en "s'inscrire" en el documento 1 y "creer un compte" en el documento 2. Para el texto de la interfaz de usuario y las cadenas orientadas al usuario, la consistencia es más importante que la calidad bruta.
- **Formality mismatch.**El modelo elige la forma que era más común en el entrenamiento. Para el contenido orientado al cliente esto suele ser incorrecto. Mitigation: prefijo rápido con un token de formalidad si el modelo lo soporta, o ajustar a un modelo pequeño en corpora formal-solo.
- **Length explosion on short input.**Las oraciones de entrada muy cortas a menudo producen traducciones demasiado largas porque la penalidad de longitud cae de un acantilado por debajo de ~ 5 tokens de origen.

### Paso 4: ajuste fino para un dominio

Los modelos pre-entrenados son generalistas. La traducción legal, médica o del diálogo de juego se beneficia de manera medible de la ajuste fino en datos paralelos de dominio.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


En el caso de los modelos de formación, el nivel de calidad de los datos es el más alto en la producción.


> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

La pila de producción 2026 para MT:
> MT 生产技术 del año 2026:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> # Usar la escena # # recomiendo que empieces #
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

Los LLM ahora superan a los modelos especializados de MT en varios pares de idiomas a partir de 2026, particularmente en contenido idiomático y contexto largo. La compensación es el costo por token y la latencia.
> Hasta 2026, el LLM en varios idiomas ha superado los modelos de MT especializados, especialmente en el contenido de la lengua y el contenido de la lengua.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-mt-evaluator.md`¿Qué es esto ?
> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-mt-evaluator.md`¿Qué es esto ?

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Los ejercicios.

1. **Easy.**Traducir un párrafo inglés de 5 frases al francés y volver al inglés usando `nllb-200-distilled-600M`Mejorar la proximidad del viaje de ida y vuelta al original.
2. **Medium.**Implementar una verificación de identificación de idioma en las salidas de traducción utilizando `fasttext lid.176`o `langdetect`.Integrarse en la llamada MT para que las generaciones fuera del objetivo sean capturadas antes de regresar.
3. **Hard.**- No . - ¿ Qué ?`nllb-200-distilled-600M`En el caso de las oraciones de la primera línea, el valor de la letra B es el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra B, y el valor de la letra C, y el valor de la letra C, y el valor de la letra C, y el valor de la letra C, y el valor de la letra C, y del punto de la letra C, y del punto de la letra C, del punto de la letra C, del punto de la letra C, del punto de la letra C, del punto de la letra c) del punto de la letra c) del punto de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra de la letra
> 1. **简单。**Uso `nllb-200-distilled-600M`将 5 句英语段落翻译成法语再翻回英语──测量往返与原文接近程度── usted debería ver el significado de la palabra pero con el significado de la palabra漂移──
2. **中等。**Uso `fasttext lid.176`O `langdetect`实现翻译输出的语言识别检查──集成到MT调用中,在返回前捕获偏离目标语言的生成──
3. **困难。**En su elección de 5000 para el campo de la lenguaje`nllb-200-distilled-600M`◊ Método de la información en el texto de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la publicación de la revista de la revista de la Unión Europea.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> # Los términos # # que la gente dice # # tienen un significado real #
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) el documento de la NLLB.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)¿ Por qué ?`sacrebleu`es la única forma correcta de informar BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) el papel de la crf.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) práctica de ajuste fino a través del paso.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) NLLB 论文。
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)¿ Por qué ?`sacrebleu`Es la única forma correcta de informar sobre BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) 论文──  论文──  论文── 论文── 论文── 论文── 论文──
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) 实用微调演练──
