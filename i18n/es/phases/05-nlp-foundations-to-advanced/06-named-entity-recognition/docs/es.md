# Nombre de identificación de entidad.

> Suena fácil hasta que se trata de límites ambigüos, entidades anidadas y jerga de dominio.
> ¡Pronta el nombre! ¡Pues parece simple, hasta que encuentras el límite de la forma!

> **【中文解读】**El nombre de la persona, el nombre de la región, el nombre de la organización, etc. son la base de la extracción de información y el esquema de conocimiento.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

"Apple demandó a Google por su acuerdo de búsqueda de iPhone en los EE.UU". Cinco entidades: Apple (ORG), Google (ORG), iPhone (PRODUCT), acuerdo de búsqueda (tal vez), US (GPE). Un buen sistema NER extrae a todos ellos con tipos correctos.

> "Apple demandó a Google por su acuerdo de búsqueda de iPhone en los EE.UU". 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCT)、search deal(可能)、US(GPE)。 una buena NER 系统能正确提取所有实体及其类型──一个差的系统会遗漏 iPhone,把水果 Apple和公司 Apple 混,把"US"标记为 PERSON──

NER es el caballo de trabajo debajo de cada red de extracción estructurada. Resumen de análisis, registro de cumplimiento, anónimo de registros médicos, comprensión de búsqueda de consultas, la base para las respuestas de chatbot, extracción de contratos legales. Nunca lo ves, siempre dependes de él.

> NER es el motor de trabajo de cada estrategia estructurada para extraer flujo de agua.

Esta lección recorre el camino clásico (basado en reglas, HMM, CRF) hacia el moderno (BiLSTM-CRF, luego transformadores).

> Este curso se transforma desde el tradicional camino (BLSTM-CRF, Transformer) a la moderna ruta (BLSTM-CRF, Transformer). Cada paso resuelve las limitaciones específicas del paso anterior.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**BIO tagging**(o BILOU) convierte la extracción de entidades en un problema de etiquetado de secuencias.`B-TYPE`(inicio de la entidad), `I-TYPE`(entidad interna), o `O`(fuera de cualquier entidad).

> **BIO 标注**(o BILOU) se extraerá el cuerpo y se transformará en un problema de etiquetado de secuencias.`B-TYPE`(实体开始)`I-TYPE`(en el cuerpo interno) o `O`(no está en ningún cuerpo)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Cadena de entidades multi-tokens: `New B-GPE`¿ Qué ?`York I-GPE`¿ Qué ?`City I-GPE`Un modelo que entiende la biología puede extraer espacios arbitrarios.

> Más de un token 实体链接:`New B-GPE`¿Qué es esto?`York I-GPE`¿Qué es esto?`City I-GPE`❖ Comprender el modelo de la BIO puede derivarse de cualquier longitud.

La evolución de la arquitectura:

> 架构演进:

- **Rule-based.**Regex + búsquedas de boletines. Alta precisión en entidades conocidas, cero cobertura en las nuevas.
  **基于规则。**正则 + 地名词典查找── para el hecho conocido tasa de precisión alta, para el hecho nuevo零覆盖──
- **HMM.**Modelo de Markov oculto, probabilidad de emisión de un token dado, probabilidad de transición de un tag a otro, decodificación Viterbi, entrenado en datos etiquetados.
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**Campo aleatorio condicional. Como HMM pero discriminativo, para que pueda mezclar características arbitrarias (forma de palabra, mayúsculas, palabras vecinas). Aún el caballo de trabajo de producción clásico en 2026 para implementaciones de bajos recursos.
  **CRF。**条件随机场──类似于 HMM,但判别式,所以可以混合任意特征(词形、大小写、相邻词)── hasta 2026 años todavía es el clásico productor principal del Low Resource Deployment──
- **BiLSTM-CRF.**Las características neuronales en lugar de hechas a mano. LSTM lee la oración en ambas direcciones, la capa CRF en la parte superior impone secuencias de etiquetas consistentes.
  **BiLSTM-CRF。**Neurociencia en lugar de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta de la etiqueta
- **Transformer-based.**Tonea la BERT con una cabeza de clasificación de tokens, mejor precisión, más computación.
  **基于 Transformer。**Usando el token 分类头微调 BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
ner-bio-tagging
```

## Construye el mismo

### Paso 1: Asignar a los asistentes de etiquetado de la Biotecnología

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Paso 2: Características hechas a mano

Para el NER clásico (no neuronal), las características son el juego.

> Para el clásico, la característica es clave.

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`retorno `xXxxxx`- ¿ Qué ?`word_shape("USA-2024")`retorno `XXX-dddd`Los patrones de capitalización son de alta señal para los sustantivos apropiados.

> `word_shape("iPhone")` regresar `xXxxxx`¿Qué es eso?`word_shape("USA-2024")` regresar `XXX-dddd`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊      ◊                                                                                                                                                                                                                                         

### Paso 3: una línea de base simple basada en reglas + diccionario

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Los periódicos de producción tienen millones de entradas extraídas de Wikipedia y DBpedia.`Apple`La empresa vs la fruta) es terrible.

> El nombre de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la ciudad de la capital de la ciudad de la capital de la ciudad de la ciudad de la capital de la ciudad de la capital de la ciudad de la capital de la ciudad de la capital de la capital de la ciudad de la capital de la capital de la capital de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la capital de la provincia de la provincia de la provincia de la provincia de la provincia de la capital de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la capital de la capital de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la provincia de la del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del del`Apple`vs 水果 `apple`) muy malo. Es por eso que el modelo estadístico ha ganado.

### Paso 4: el paso CRF (bozo, no implantes completos)

El CRF completo desde cero en 50 líneas no es esclarecedor sin los fundamentos de la teoría de probabilidades.`sklearn-crfsuite`en su lugar:

>  sin base de probabilidad                                                                                                                                                                                                                                                            `sklearn-crfsuite`¿Qué es esto ?

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`y `c2`Las regulaciones L1 y L2 son:`all_possible_transitions=True`permite que el modelo aprenda secuencias ilegales (por ejemplo, `I-ORG`después de`O`) son poco probables, es decir, cómo un CRF hace cumplir la coherencia de la BIO sin que usted escriba la restricción.

> `c1`Y `c2`Es L1 y L2`all_possible_transitions=True`让模型学习非法序列 (por ejemplo)`O` después aparecen `I-ORG`) no es probable, es así que CRF en caso de no escribir un vínculo obliga a la BIO un modo de tener relaciones sexuales.

### Paso 5: lo que añade un BiLSTM-CRF

Las características se aprenden. Ingresos: embeddings de tokens (GloVe o fastText). LSTM lee de izquierda a derecha y de derecha a izquierda. Los estados ocultos conectados pasan a través de una capa de salida CRF. El CRF todavía impone la consistencia de secuencia de etiquetas; el LSTM reemplaza las características hechas a mano con las aprendidas.

> Los signos de la información se encuentran en el código de acceso de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de la red de cesión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de cencia de datos de datos de cencias de datos de datos de datos de datos de datos de cencias de datos de datos de datos de datos de datos de datos de datos de la red de cencias de datos de cencias de datos de datos de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de cencias de

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

Para la capa CRF, utilizar `torchcrf.CRF`La ganancia sobre el CRF hecho a mano es medible pero menor de lo que se espera a menos que tengas decenas de miles de frases etiquetadas.

> CRF 层使用 `torchcrf.CRF`(Pip instalar pytorch-crf) ⋅ En comparación con el manual CRF de la elevación es medible, pero es menor que lo que se espera, a menos que usted tenga varios millones de puntos de referencia ⋅

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

spaCy emite NER de producción fuera de la caja.

> El espacio de producción de NER se abre a la producción de NER.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Notice `iPhone`etiquetado`ORG`en lugar de`PRODUCT` El modelo pequeño de spaCy tiene una cobertura débil de las entidades de producto.`en_core_web_lg`El modelo de transformador (`en_core_web_trf`) hace aún mejor.

> Atención .`iPhone`Fue marcado por`ORG`Y no`PRODUCT` el pequeño modelo de espacio es más débil en la cobertura del cuerpo del producto.`en_core_web_lg`)更好──Transformer 模型(`en_core_web_trf`¡Es mejor!

Cara de abrazo para NER basado en BERT:

> Abrazar la cara basado en BERT de NER:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`Si no se combinan los tokens B-X, I-X en un espacio, se obtienen etiquetas de nivel de token y se deben fusionar por sí mismos.

> `aggregation_strategy="simple"`Se puede combinar el token B-X ∞ X ∞ X ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

### NER basado en el MLL (opción 2026)

El LLM NER de tiro cero y de pocos tiros ahora es competitivo con modelos ajustados en muchos dominios, y es dramáticamente mejor cuando los datos etiquetados son escasos.

> 零样本和少样本 LLM NER es ahora competitivo en muchos campos con los modelos de micro-modulación, con mayores ventajas en la escasez de datos de etiquetado.

- **Zero-shot prompting.**Dar al LLM una lista de tipos de entidades y un esquema de ejemplo. Pida una salida JSON. Funciona fuera de la caja; la precisión es moderada en dominios nuevos.
  **零样本提示。**Darle a LLM una lista de tipos y modelos de ejemplos de entidades  Requerir JSON                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
- **ZeroTuneBio-style prompting.**Descompone la tarea en extracción de candidato → significado explicación → juicio → re-verificación. Un prompt de múltiples etapas (no de un solo disparo) aumenta la precisión sustancialmente en el NER biomédico. El mismo patrón funciona para los dominios jurídicos, financieros y científicos.
  **ZeroTuneBio 风格提示。**Se puede considerar que el trabajo de la organización es un trabajo de la organización y que se debe a que el trabajo de la organización sea un trabajo de la organización.
- **Dynamic prompting with RAG.**Recupere los ejemplos etiquetados más similares de un conjunto de semillas anotadas para cada llamada de inferencia; construya el prompt de pocos disparos en vuelo. En los puntos de referencia 2026, esto eleva el GPT-4 biomédico NER F1 en un 11-12% sobre el prompt estático.
  **动态 RAG 提示。**Cada vez que se recomienda recoger de la menor cantidad de etiquetas las muestras de etiquetas más similares; se construye un pequeño número de muestras de sugerencias. En el 2026 el GPT-4 生物医学 NER F1 se ha incrementado en un 11-12% en comparación con las sugerencias de estado.
- **Per-entity-type decomposition.**Para documentos largos, una sola llamada que extrae todos los tipos de entidades a la vez pierde la memoria a medida que crece la longitud. ejecuta un pase de extracción por tipo de entidad. Costo de inferencia más alto, precisión sustancialmente mayor. Este es el patrón estándar para notas clínicas y contratos legales.
  **按实体类型分解。**对于长文档, una vez调用提取所有实体类型时,随着长度增加会丢失召回率──每种实体类型运行一次抽取──推理成本更高,但准确率显著更高──这是临床笔记和法律合同的标准模式──

Recomendación de producción a partir de 2026: comience con una línea de base de tiro cero LLM antes de recopilar datos de entrenamiento.

> 2026 años de producción sugiere: antes de recoger datos de entrenamiento, primero comience con LLM 零样本基线.

### Cuando el NER clásico sigue ganando

Incluso con LLM disponibles, el NER clásico gana cuando:

> Incluso si hay LLM, clásico NER en las siguientes situaciones:

- El presupuesto de latencia es inferior a 50 ms.
  延迟预算低于50毫秒──
- Tienes miles de ejemplos etiquetados y necesitas 98% + F1.
  Tienes miles de muestras de marcas y necesitas un 98% de F1+.
- El dominio tiene una ontología estable donde un CRF o BiLSTM preentrenado transfiere bien.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
- Las limitaciones reglamentarias requieren un modelo no generativo en el lugar.
  监管约束要求本地部署的非生成式模型──

### Donde se desmorona

- **Domain shift.**El NER entrenado en contratos legales tiene un peor rendimiento que un periodista.
  **领域偏移。**En CoNLL 处理法律合同时比地名词典还差──在你的领域上微调──
- **Nested entities.**"Bank of America Tower" es al mismo tiempo un ORG y una FACILITAD. El BIO estándar no puede representar espacios superpuestos.
  **嵌套实体。**"Bank of America Tower" 同时是ORG 和 FACILITY──标准BIO 无法表示重叠跨度──你需要嵌套 NER(多遍或基于跨度的模型)──
- **Long entities.**Los modelos de nivel de tokens a veces dividen esto.`aggregation_strategy`o después del proceso.
  **长实体。**"Corporación Federal de Seguros de Depósitos de los Estados Unidos"...`aggregation_strategy`O después de procesar.
- **Sparse types.**Los modelos de uso general no tienen idea de que Scispacy y BioBERT son los puntos de partida.
  **稀疏类型。**医疗 NER 标签如Drug_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知──Scispacy 和 BioBERT es el punto de partida allí──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/skill-ner-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-ner-picker.md`¿Qué es esto ?

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Implementación `bio_to_spans`(la inversa de `spans_to_bio`) y verificar la coherencia de ida y vuelta en 10 frases.
   **简单。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `bio_to_spans`(El artículo`spans_to_bio`de la función opuesta) y en 10 个句子 验证往返一致性──
2. **Medium.**Entrenamiento del CRF sklearn-crfsuite anterior en el conjunto de datos del NER inglés CoNLL-2003.`seqeval`Resultado típico: ~ 84 F1.
   **中等。**En CoNLL-2003 Inglés NER datos集上训练上述 sklearn-crfsuite CRF──使用 `seqeval`报告每类 F1──典型结果:~84 F1──
3. **Hard.**- No . - ¿ Qué ?`distilbert-base-cased`En el caso de los datos de la red de datos, el número de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos
   **困难。**En el ámbito específico de la NER (medicina, ley o finanzas)`distilbert-base-cased`◊ Comparar con el espacio ◊ Comparar con el espacio ◊ Recoger datos de fuga de datos

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) el documento BiLSTM-CRF. Canonical. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) introduce el patrón de clasificación de tokens que se convirtió en estándar. /  introduced into becoming standard的 token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) referencia práctica para cada atributo de la`Doc.ents`y `Span`- ¿ Qué ?`Doc.ents`Y `Span`Referencia práctica de cada uno de los atributos.
- [seqeval](https://github.com/chakki-works/seqeval) la biblioteca métrica correcta. Usa siempre. / 正确的指标库──始终使用它──
