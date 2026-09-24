# Modelos de incrustación  La inmersión profunda 2026 嵌入模型  profundidad resolución

> Word2Vec le dio un vector por palabra. Modelos de incorporación modernos le dan un vector por pasaje, translingual, con vistas escasas, densas y multi-vector, tamaño para adaptarse a su índice. Elige mal y su RAG recupera la cosa equivocada.
> Word2Vec  te da cada palabra una velocidad―Modern Embedding Model te da cada fragmento una velocidad, translanguage, tiene rara­go, 密 y multi-velo­ment vista, tamaño para tu indicación―selección de error tu RAG irá a buscar cosas erróneas―

> **【中文解读】**嵌入模型是RAG 和语义搜索的核心──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Elegir una incorporación en 2026 significa elegir entre cinco ejes: denso vs. escaso vs. multivéctor, monolingüe vs. multilingüe, tamaño del modelo, objetivo de capacitación y si se ajusta a las restricciones de dimensión de su base de datos vectorial.

> 2026 años de selección de emplazamiento significa que se seleccionan en cinco ejes: 密 vs 稀疏 vs 多向量、单语 vs 多语言、模型大小、训练目标、以及是否适合你的向量数据库尺寸约束──

> **【中文解读】**La cuestión planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en el proyecto real?

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías fundamentales.

**Dense embeddings.**Vektor de tamaño fijo único por texto (por ejemplo, 768-dim de MiniLM). Rápido para comparar, bien comprimir, estándar en bases de datos de vectores. Mejor para la recuperación de propósito general.

> **稠密嵌入。**Cada texto tiene un tamaño fijo de velocidad (como el de MiniLM) ⋅ comparado rápido, comprimido, de velocidad de datos estándar, más adecuado para la búsqueda general.

**Sparse embeddings.**Un peso por término vocabulario (como un TF-IDF aprendido). SPLADE, BM25.

> **稀疏嵌入。**Cada palabra muestra un peso (en inglés) en el formato de TF-IDF (en inglés).

**Multi-vector / ColBERT.**Un vector por token, puntuación de interacción tardía.

> **多向量 / ColBERT。**Cada token, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼, un ∼ un ∼, un ∼ un ∼, un ∼ un ∼, un ∼ un ∼, un ∼ un ∼ un ∼, un ∼ un ∼, un ∼ un ∼, un ∼ un ∼ un ∼

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.
```figure
gx-matryoshka
```

## Construye el mismo

### Paso 1: comparación de modelos de incorporación

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

query = "What is attention in transformers?"
docs = ["Self-attention computes weighted sums of values.", "The cat sat on the mat."]

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    q_emb = model.encode([query], normalize_embeddings=True)
    d_embs = model.encode(docs, normalize_embeddings=True)
    sims = (d_embs @ q_emb.T).flatten()
    print(f"{name}: {list(zip(docs, sims.round(3)))}")
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## Envíe el producto .

Salvo como`outputs/skill-embedding-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-embedding-picker.md`¿Qué es esto ?

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## Los ejercicios.

1. **Easy.**Comparar MiniLM vs BGE en una tarea de extracción de 100 consultas. / **简单。**En 100 tareas de búsqueda de datos comparar MiniLM vs BGE
2. **Medium.**Construir una recuperación híbrida densa + espacios. / **中等。**构建混合密+稀疏检索──
3. **Hard.**Afinar un modelo de incorporación en pares específicos de dominio. / **困难。**En el campo específico para los modelos de inserción de micro-modelo.

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## Más Leer más Leer más

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) incrustando puntos de referencia. / 嵌入模型基准──
- [SPLADE](https://arxiv.org/abs/2109.10086) raros aprendizajes incrustados. / 稀疏学习嵌入──
- [ColBERT](https://arxiv.org/abs/2004.12832) Retorno tardío de interacción. / 延迟交互检索。
