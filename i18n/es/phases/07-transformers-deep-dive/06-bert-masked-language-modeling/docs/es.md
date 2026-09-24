# BERT  Modelado de lenguaje enmascarado ∙ BERT  掩码语言模型

> GPT predice la siguiente palabra. BERT predice una palabra que falta. Una frase de diferencia  y media década de todo en forma de incrustación.

> **【中文解读】**BERT es un Transformer de codificación única, con un entrenamiento de previsión de envases.

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

En 2018, cada tarea de NLP  sentimiento, NER, QA, entailment  entrenó su propio modelo desde cero en sus propios datos etiquetados. No había un punto de control "entender inglés" pre-entrenado que pudiera ajustar. ELMo (2018) mostró que se podía entrenar pre-embeddings contextuales con un LSTM bidireccional; ayudó pero no generalizó.

> En 2018, cada tarea de PNL  análisis emocional  nombres de entidades 识别、问答、文本含都需要从零训练模型上自标数据. En ese momento, no había ningún "entender inglés" de entrenamiento previo.

BERT (Devlin et al. 2018) preguntó: ¿qué pasa si tomamos un codificador transformador, lo entrenamos en cada frase en Internet, y lo obligamos a predecir palabras faltantes del contexto en ambos lados?

> BERT(Devlin  et al., 2018) planteó un problema clave: si con el Transformer 编码器, entrenar en todas las frases en Internet, lo obligó a basarse en dos lados de la predicción de abajo se oculta de palabras, ¿cómo?

El resultado: en 18 meses BERT y sus variantes (RoBERTa, ALBERT, ELECTRA) dominaron todos los listados de clasificación de la PNL que existían.

> El resultado es: en 18 个月内,BERT 及其变体 (Robert 罗伯特 艾尔伯特 埃勒特拉) dominó todas las clasificaciones de PNL ∼ hasta 2020, cada motor de búsqueda del mundo ∼ un sistema de búsqueda de contenido y de análisis de contenido tiene un BERT ∼

En 2026 los modelos de codificación solo son todavía la herramienta adecuada para la clasificación, recuperación y extracción estructurada.

> Hasta 2026, el modelo de codificador especial sigue siendo la correcta opción de la clasificación, la búsqueda y la estructuración de los extractos. Su velocidad de funcionamiento por token es de 5 a 10 veces mayor que la de un codificador rápido, su emplazamiento es el tronco de cada sistema moderno de búsqueda.

> **【中文解读】**La revolución de BERT consiste en el modelo de "pre-training+micro-modulación": en gran escala, el modelo de lenguaje de encubierto se utiliza sin etiqueta en el modelo de MLM, y luego se reduce la cantidad de parámetros en una tarea específica. La atención bidireccional del codificador permite que pueda utilizar simultáneamente el término de encubierto en el texto anterior y posterior, esto es lo que el modelo de auto-regreso (como GPT) no hace.

## El concepto central.

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### La señal de entrenamiento

Toma una frase:`the quick brown fox jumps over the lazy dog`¿ Qué ?

> ¿Qué es eso ?`the quick brown fox jumps over the lazy dog`¿Qué es eso?

Máscarar el 15% de los tokens al azar:

> 随机掩码 15% de los tokens:

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Entrenar al modelo para predecir los tokens originales en posiciones enmascaradas.`[MASK]`en la posición 1 puede utilizar `brown fox jumps`En las posiciones 2+ eso es lo que el GPT no puede hacer.

> 訓練模型在被掩藏位置预测 原始代币──因为编码器是双向的,预测位置是1 的 `[MASK]`Puede utilizar la posición 2 及后的 `brown fox jumps` Éste es el asunto que no ha hecho el GPT

### Las reglas de la máscara BERT

De los 15% de tokens seleccionados para la predicción:

> En el 15% de los tokens que se seleccionan para la predicción:

- El 80% se sustituye por `[MASK]`¿ Qué ?
  El 80% fue reemplazado por`[MASK]`¿Qué es eso?
- El 10% se sustituye por un token aleatorio.
  El 10% fue reemplazado por el token de azar.
- El 10% se mantiene sin cambios.
  En el caso de los niños, el número de niños en edad avanzada es de 10%.

¿ Por qué no siempre ?`[MASK]`¿ Por qué ?`[MASK]`El modelo de la formación para esperar`[MASK]`El 10% aleatorio + 10% inalterado mantiene el modelo honesto.

> ¿Por qué no siempre es útil?`[MASK]`¿Por qué ?`[MASK]`En el momento de la evaluación nunca aparecerá. Si el modelo de entrenamiento está en el 100% de la posición oculta, esperamos ver.`[MASK]`, se produce una desviación de distribución entre el entrenamiento previo y la moderación.

> **【中文解读】**El 80% de las reglas de BERT 掩码的三条规则 ((80% [MASK]、10% 随机替换、10% 保持不变) es para reducir la diferencia de distribución entre el entrenamiento previo y la moderación.

> **【拓展：BERT 在 RAG 系统中的角色】**现代 RAG(检索增强生成) en el sistema,BERT 变体 sigue siendo el núcleo de la fase de investigación. 模型──如全MiniLM-L6-v2) 本质上就是使用比较学习微调的BERT──交叉编码器──交叉编码器.

### Siguiente Previsión de Sentencia (NSP)  y por qué se dejó caer

BERT original también entrenó en NSP: dado dos oraciones A y B, predecir si B sigue A. RoBERTa (2019) lo ablacionó y mostró que NSP le duele, no ayuda.

> El primer programa de programación de la serie de programas de programación de la revista NSP fue el de la serie de programas de programación de la serie NSP.

### Lo que cambió en 2026: ModernBERT

El papel ModernBERT de 2024 reconstruyó el bloque con primitivos de 2026:

> El artículo ModernBERT de 2024 reedifica el bloque de codificación con componentes modernos:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

Y a diferencia de la pila de 2018, es nativo de atención flash. La inferencia es 23x más rápida a la longitud de secuencia 8K que DeBERTa-v3 con mejores puntajes GLUE.

> Diferente de la tecnología de 2018, ModernBERT originalmente apoya la atención flash.

### Casos de uso que todavía escogen un codificador en 2026

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Construye y realiza.
```figure
transformer-residual
```

## Construye el mismo

### Paso 1: Enmascarar la lógica

¿ Qué ?`code/main.py`La función`create_mlm_batch`Toma una lista de IDs de token, un tamaño de vocabulario y una probabilidad de máscara. devuelve IDs de entrada (con máscaras aplicadas) y etiquetas (solo en posiciones enmascaradas, -100 en otros lugares  Ignorar la convención de índice de PyTorch).

> 参见 `code/main.py`△ Función `create_mlm_batch` acepta ID de token 列表、词表大小和掩码概率, regresar a la entrada ID( ya aplicado掩码) y标签(solo en la posición de ocultamiento tiene valor, el resto es -100PyTorch 忽略索引约定) 

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Paso 2: ejecutar predicción de MLM en un corpus pequeño

Entrenamos un codificador de 2 capas + cabeza MLM en un vocabulario de 20 palabras, 200 frases.

> En 20 palabras de la lista de palabras y 200 frases entrenar un codificador de 2 niveles + MLM cabeza. No se trata de la escala. Sólo hacer un examen de la razonabilidad de la propagación.

### Paso 3: comparación de tipos de máscaras

Muestre cómo la regla de tres vías mantiene el modelo utilizable sin `[MASK]`Las dos deben producir distribuciones simbólicas razonables porque el modelo vio ambos patrones en el entrenamiento.

> 展示三路规则 cómo hacer que el modelo esté en falta `[MASK]`En algunos casos, todavía se puede usar. Los dos deben generar una distribución razonable, ya que los modelos se han visto en el entrenamiento.

### Paso 4: Tenga en cuenta la cabeza

Reemplazar la cabeza de MLM con una cabeza de clasificación en un conjunto de datos de sentimiento de juguete. Sólo las cabezas se mueven; el codificador está congelado. Este es el patrón que sigue cada aplicación BERT.

> Usar la cabeza en un juego de emociones en un conjunto de datos de MLM.

> **【拓展：BERT 微调的实践技巧】**Las mejores prácticas de BERT 微调 incluyen: 1) Usando menor de aprendizaje tasa(2e-5 hasta 5e-5) evitar dañar el prepraining peso; 2) para el uso de token de la clase de tareas [CLS] como expresión de la frase; 3) para NER etc. por token task, utilizar la salida de cada posición; 4) para el desarrollo de la capacidad de deshielo gradual) puede ser mejorada en el pequeño conjunto de datos.

## Usalo con el marco de ejecución

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers`modelos como `all-MiniLM-L6-v2`El codificador es el mismo, la pérdida cambió.

> **嵌入模型是微调后的 BERT。** `sentence-transformers`模型如 `all-MiniLM-L6-v2`En esencia es la misma estructura del codificador que la de BERT en comparación con el entrenamiento de pérdida, pero la función de pérdida ha cambiado.

**Cross-encoder rerankers are also fine-tuned BERT.**Clasificación en pareja en `[CLS] query [SEP] doc [SEP]`La atención bidireccional entre la consulta y el documento es exactamente lo que da a los codificadores cruzados su ventaja de calidad sobre los codificadores bien.

> **交叉编码器重排序器也是微调后的 BERT。**En el`[CLS] query [SEP] doc [SEP]`La doble atención entre las consultas y los archivos es la razón por la cual la calidad de los editores de intercambio es superior a la de los editores de intercambio.

**When not to pick BERT in 2026.**Cualquier cosa generativa. El codificador no tiene manera sensata de producir tokens autoregresivamente. También: cualquier cosa bajo los parámetros 1B donde un pequeño decodificador puede igualar la calidad con más flexibilidad (Phi-3-Mini, Qwen2-1.5B).

> **2026 年何时不选 BERT。**任何生成式任务──编码器没有 manera razonable de realizar el autorecambio de los tokens 生成──此外, en los casos de 1B 参数下面, pequeños解码器 (como Phi-3-Mini、Qwen2-1.5B) pueden obtener una flexibilidad considerable con menos parámetros──

> **【拓展：ModernBERT 的现代化改进】**ModernBERT(2024) se actualizará en 2018 la arquitectura de BERT  RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

## Envíe el producto .

¿ Qué ?`outputs/skill-bert-finetuner.md`. El alcance de las habilidades se ajusta a la finalidad de BERT (elección de la columna vertebral, especificación de la cabeza, datos, evaluación, detención) para una nueva tarea de clasificación o extracción.

> 参见 `outputs/skill-bert-finetuner.md` Esta habilidad es necesaria para la nueva clasificación o la preparación de tareas (BERT 微调方案) 

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Confirmar ~15% se seleccionan, y de esos ~80% se convierten en `[MASK]`¿ Qué ?
   Traducción:运行`code/main.py`, imprimir 10.000 tokens de distribución de escondidas, confirmar alrededor del 15% seleccionado, de los cuales alrededor del 80% se han convertido en`[MASK]`¿Qué es eso?
2. **Medium.**Implementar el enmascaramiento de palabras enteras: si una palabra es tokenizada en subpalabras, enmascarar todas las subpalabras juntas o ninguna. Medir si esto mejora la precisión de MLM en un corpus de 500 frases.
   Si un término es dividido en varios hijos de palabras, o bien todo es ocultado o bien todo no es ocultado, esto significa que el MLM ha aumentado la precisión en 500 palabras.
3. **Hard.**Entrenar un pequeño BERT de 2 capas, d=64, en 10.000 frases de un conjunto de datos público.`[CLS]`Comparar con una línea de base sólo para decodificadores en parámetros iguales ¿cuál gana?
   En el libro de datos de la revista The New York Times, el autor de la revista The New York Times, escribió:`[CLS]`¿Cuál es mejor en comparación con la línea de base de un descifrador de la misma cantidad de parámetros?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Más Leer más Leer más

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) papel original.
  El texto original de la obra fue traducido en inglés.
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)¿Cómo entrenar bien a BERT? Mata a los NSP.
  Traducción:Cómo se ha entrenado correctamente BERT; demostró que el NSP es inútil.
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) la detección de tokens sustituidos supera a MLM en computación coincidente.
  En inglés, el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de.
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663) Papel de la revista ModernBERT.
  El libro de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia.
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) referencia canónica del codificador.
  En el caso de los niños, el uso de la palabra "HuggingFace BERT" se puede utilizar en el caso de los niños.
