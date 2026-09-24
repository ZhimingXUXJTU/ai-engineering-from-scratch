# Estrategias de fragmentación para RAG

> La configuración de fragmentos influye tanto en la calidad de recuperación como en la elección del modelo de incorporación (Vectara NAACL 2025).
> La distribución de bloques en la calidad de la búsqueda es tan grande como la selección de modelos de inserción.

> **【中文解读】**En el sistema RAG, el proceso de separación de bloques afecta directamente el resultado de la investigación.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

La solución no es "comprar un mejor modelo de incorporación". La solución es desglosar correctamente. El documento NAACL 2025 de Vectara mostró que la estrategia de desglosamiento explica tanta variación en la calidad de recuperación como la elección de incorporación.

> 修复方法不是 "buy个更好的嵌入模型"──修复方法是正确分块── Vectara's NAACL 2025 论文 show that the分块 strategy explains as many search quality differences as the choice of embedding──

> **【中文解读】**La cuestión planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en el proyecto real?

Los resultados de referencia de febrero de 2026 muestran resultados sorprendentes: el chunking de tamaño fijo ingenuo con 100 trozos de tokens y 20 trozos de tokens superpone a la mayoría de las estrategias de chunking "inteligentes" en RAG de propósito general.

> El examen de base de febrero de 2026 mostró resultados sorprendentes: simples fijos en grandes pedazos de bloques (100 tokens plus 20 tokens) superaron la mayoría de las estrategias de bloques inteligentes en general RAG.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías fundamentales.

**Fixed-size chunking.**Dividir el texto en bloques de N-token con superposición opcional. Simple, rápido, sorprendentemente eficaz. El predeterminado en la mayoría de los sistemas RAG de producción.

> **固定大小分块。**El texto se divide en bloques de N tokens, se pueden elegir sobreponerse.

**Sentence-level chunking.**Dividido en límites de oraciones. Cada pieza = una o más oraciones. Bueno para preguntas frecuentes y respuestas cortas.

> **句子级分块。**En la sección de la frontera de la frase se divide. Cada bloque = una o varias frases.

**Semantic chunking.**Incorporar oraciones, agrupar oraciones consecutivas con incrustaciones similares en trozos.

> **语义分块。**嵌入句子, se emplazarán en bloques de segmentos de continuos similares.

**Recursive character chunking.**Dividido por párrafo, luego por oración, luego por carácter.

> **递归字符分块。**按段落分割,然后按句,然后按字符──LangChain的默认──Good通用启发式──

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.
```figure
n5-chunk-cuts
```

## Construye el mismo

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

### Paso 1: despeje de tamaño fijo con superposición

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Paso 2: fragmentación semántica

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## Envíe el producto .

Salvo como`outputs/skill-chunking-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-chunking-picker.md`¿Qué es esto ?

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Los ejercicios.

1. **Easy.**Implementar un desmembramento de tamaño fijo con superposición.**简单。**实现 fijo 个小分块──测量检索质量──
2. **Medium.**Comparar el fragmento fijo vs semántico en un conjunto de datos narrativos. / **中等。**En el conjunto de datos de la narración comparar fijo vs.
3. **Hard.**Construir un tubo de fragmentación óptimo que adapte el tamaño de fragmento por tipo de documento. / **困难。**Construcción según el tipo de archivo de bloques de mayor tamaño de bloques de flujo de agua.

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Más Leer más Leer más

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) comparativo de los fragmentos. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) implementaciones en pedazos. / 分块实现。
