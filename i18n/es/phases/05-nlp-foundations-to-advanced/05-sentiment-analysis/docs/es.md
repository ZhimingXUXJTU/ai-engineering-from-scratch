# Análisis de sentimientos

> La tarea canónica de la PNL. La mayor parte de lo que necesitas saber sobre la clasificación de textos clásicos se muestra aquí.
> La mayoría de lo que necesitas saber está aquí.

> **【中文解读】**判断文本的情感倾向──是NLP 最经典的分类任务之一──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

"La comida no fue buena". ¿Positiva o negativa?

> "La comida no fue buena". ¿Es verdad o negativo?

El sentimiento suena simple. Un revisor dijo que les gustaba o no a algo. Etiquetar la oración. La razón por la que se convirtió en la tarea canónica de la PNL es que cada caso fácil de ver esconde uno difícil. La negación cambia de significado. El sarcasmo lo invierte. "No está mal en absoluto" es positivo a pesar de dos palabras codificadas negativamente.`tight`en la revisión de música versus `tight`en la revisión de la moda).

> El análisis emocional parece simple. Los críticos dicen que le gusta o no. El tema se convirtió en un clásico trabajo de la PNL, porque cada caso parece simple y detrás de él se oculta un caso difícil.`tight`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `tight`)。

Si entiendes por qué cada línea de base ingenua tiene un modo de fracaso específico, entiendes por qué se inventó cada modelo más rico. Esta lección construye una línea de base Bayes ingenua desde cero, agrega regresión logística y nombra las trampas que hacen que el sentimiento de producción sea un problema de grado de cumplimiento.

> El análisis emocional es el laboratorio de trabajo de la PNL clásica. Si entiendes por qué cada línea simple tiene un patrón de fracaso específico, ya entiendes por qué cada modelo más rico fue inventado.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

El sentimiento clásico es una receta de dos pasos.

> El análisis de emociones clásicos es un esquema de dos pasos.

1. **Represent.**Convierta el texto en un vector de características.
   **表示。**Se puede utilizar para la traducción de la letra a letra.
2. **Classify.**Aplique un modelo lineal (Naive Bayes, regresión logística, SVM) en ejemplos etiquetados.
   **分类。**En el ejemplar de etiquetado se encuentra el modelo lineal de la base de datos.

Bayes es el modelo más estúpido que funciona.`P(word | positive)`y `P(word | negative)`En la inferencia, multiplica las probabilidades. La suposición de independencia "naiva" es ridículamente errónea y sin embargo los resultados son sorprendentemente fuertes. La razón: con características de texto escasos y datos moderados, al clasificador le importa hacia qué lado se inclina cada palabra más que hacia cuánto.

> Paule Bayes es el modelo más simple pero administrativo`P(word | positive)`Y `P(word | negative)` La hipótesis de independencia de la "pureza" es ridícula, pero los resultados son sorprendentes.

La regresión logística fija la suposición de independencia. Aprende un peso por característica, incluyendo pesas negativas. `not good`Bayes ingenuo no puede hacer eso para los bigramas que nunca ha etiquetado.

> 逻辑归修复了独立性假设──. Se trata de cada característica que tiene un peso, incluyendo el peso negativo──.`not good`Como un componente de la segunda divisoria, el peso negativo es un factor que se puede evaluar con la simple forma en que el componente de la segunda divisoria no se puede evaluar.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
sentiment-logits
```

## Construye el mismo

### Paso 1: un mini conjunto de datos real

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

El trabajo real utiliza decenas de miles de ejemplos (IMDb, SST-2, polaridad Yelp).

> Por lo tanto, el trabajo real es el mismo.

### Paso 2: Naive Bayes multinomial desde cero

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

La suavizamiento aditivo (alfa=1.0) es la suavizamiento de Laplace. Sin ella, una palabra no vista en una clase tiene probabilidad cero y el registro explota. `alpha=0.01`Es común en la práctica. `alpha=1.0`es el defecto de enseñanza.

> 加法平滑(alpha=1.0) es un término que se utiliza para describir el tipo de palabra que se ha visto en el mundo.`alpha=0.01`Es muy habitual.`alpha=1.0`Es un aprendizaje de la calidad.

### Paso 3: Regresión logística desde cero

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

La regularización de L2 es importante aquí. Las características del texto son escasas; sin L2 el modelo memoriza ejemplos de entrenamiento.`0.01`y sintonizar.

> La normalización L2 es importante en este contexto.`0.01`開始调参──

### Paso 4: negación de manejo (modo de falla)

Considere "no bueno" y "no malo". Un clasificador de BoW ve.`{not, good}`y `{not, bad}`Y aprende de quien apareció más en el entrenamiento.`not_good`y `not_bad`Y los aprende como características distintas.

> 考虑 "no bueno" 和 "no malo"──BoW 分类器看 `{not, good}`Y `{not, bad}`, según el entrenamiento que aparezca más para aprender.`not_good`Y `not_bad`作为不同特征学习──, esto suele ser suficiente──,

Una solución más crudera que funciona cuando no tienes bigramas: **negation scoping**. Prefijo de tokens después de una palabra de negación con `NOT_`hasta la siguiente puntuación.

> Una más gruesa pero efectiva en la falta de 2 grupos:**否定范围标记**在否定词后给标志加 `NOT_`Antes, hasta el siguiente signo.

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

Ahora .`good`y `NOT_good`El clasificador puede pesarlas opuestas. tres líneas de precisión de procesamiento medible saltan sobre los puntos de referencia del sentimiento.

> Ahora .`good`Y `NOT_good`Las características de los grupos de clasificación pueden darles un peso contrario.

### Paso 5: métricas de evaluación que importan

La exactitud por sí sola es engañosa si las clases están desequilibradas. Los corpora de sentimiento reales suelen ser de 70-80% positivo o 70-80% negativo; un clasificador de mayoría constante obtiene una exactitud del 80% y no tiene valor.

> Si las categorías no son equilibradas, sólo se observa la tasa de precisión generará errores. El contenido de la verdadera emoción es generalmente de 70-80% positivo o 70-80% negativo.

- **Per-class precision and recall.**Un par por clase, y los promediamos para obtener un solo número que respete el equilibrio de clase.
  **每类精确率和召回率。**Cada clase tiene un par.
- **Macro-F1 (primary metric for imbalanced data).**Mediano de puntuaciones por clase, igual de ponderada.
  **Macro-F1（不平衡数据的主要指标）。**El valor medio de las diferencias de F1 es igual al peso.
- **Weighted-F1 (alternative).**Igual que macro pero ponderado por la frecuencia de la clase.
  **Weighted-F1（替代方案）。**Cuando no se equilibra en sí mismo tiene un significado comercial, se hace un informe con la macro-F1.
- **Confusion matrix.**Siempre inspeccione antes de confiar en cualquier métrica escalar; revela qué par de clases el modelo confunde.
  **混淆矩阵。**Primero cálculo: Previo examen de cualquier indicador de valores en la confianza; revela qué clases de modelos se mezclaron.
- **Per-class error samples.**Toma 5 predicciones erróneas por clase. Léaslas. Nada reemplaza la lectura de los errores reales.
  **每类错误样本。**Cada clase extrae 5 errores de pronóstico.

Para datos gravemente desequilibrados (> 95-5 ratio), informe **AUROC**y **AUPRC**AUPRC es más sensible a la clase minoritaria, que es lo que normalmente se preocupa (spam, fraude, sentimiento raro).

> 对于严重不平衡的数据 ((> 95-5 比例), informe **AUROC**Y **AUPRC**代替准确率──AUPRC es más sensible a la minoría, esto es lo que normalmente te preocupa.

**Common bug to avoid.**Informar micro-F1 en lugar de macro-F1 en datos desequilibrados da un número que parece alto porque está dominado por la clase mayoritaria.

> **常见错误。**En datos desequilibrados, el informe de micro-F1 en lugar de macro-F1 dará un número que parece muy alto, ya que está dominado por la mayoría de las clases.

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

Scikit-learn lo hace en seis líneas, correctamente.

> Es un poco de aprendizaje.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Tres cosas que hay que notar.`stop_words=None`mantiene las negaciones. `ngram_range=(1, 2)`añade grandes gramos así `not_good`Se convierte en una característica. `sublinear_tf=True`Estas tres señales son la diferencia entre un 75% de precisión y un 85% de precisión en el SST-2.

> Tres lugares que merecen atención.`stop_words=None`Mantener un rechazo.`ngram_range=(1, 2)`添加二元组使                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `not_good`Se convirtió en un rasgo.`sublinear_tf=True`抑制重复词── Estos tres signos son la diferencia entre la línea de base del 75% y la línea de base del 85% de la línea de base de la SST-2.

### Cuando se debe buscar un transformador

- Detección de sarcasmo, los modelos clásicos fallan aquí.
  El modelo clásico aquí fracasará.
- Largas revisiones donde el sentimiento cambia a mediados del documento.
  情感在文档中转变的长评论──
- "La cámara era genial pero la batería era terrible". Necesitas atribuir el sentimiento a aspectos.
  基于方面情感分析――"La cámara era genial pero la batería era terrible".
- Los idiomas no ingleses y de bajo recurso. BERT multilingüe te da una línea de base de cero disparos de forma gratuita.
  No Inglés, bajo recurso de lenguaje.

Si necesita cualquiera de los anteriores, salte a la fase 7 (mergullamiento profundo de transformadores). de lo contrario, la regresión logística de Naive Bayes o TF-IDF más bigramas más manipulación de negación es su línea de base de producción para 2026.

> Si necesitas algo más, salta a la Fase 7 (Transformer Deeping) ⋅ si no, en TF-IDF + 2 组加否定处理的简单贝叶斯或逻辑回归就是你2026年生产基线――

### La trampa de reproducción (de nuevo)

Reentrenar modelos de sentimiento es rutina. Reevaluarlos no es. Los números de precisión reportados en los documentos utilizan divisiones específicas, preprocesamiento específico, tokenizers específicos. Si compara su nuevo modelo con una línea de base sin usar la misma tubería, obtendrá deltas engañosas. Siempre regenerar la línea de base en su tubería, no el número del papel.

> El nuevo modelo de emoción es una operación habitual. La reevaluación no es la tasa de precisión del informe en el artículo. El informe utiliza números específicos para la división de datos, el procesamiento previo específico, el procesamiento previo específico. Si no utilizas la misma línea de flujo para comparar el nuevo modelo con la línea de base, obtendrás un valor de error. Siempre se reproduzce la línea de base en tu línea de flujo, en lugar de usar los números en el artículo.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-sentiment-baseline.md`¿Qué es esto ?

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Los ejercicios.

1. **Easy.**Añadir`apply_negation`como un paso de preprocesamiento en la línea de aprendizaje de scikit y medir el delta de F1 en un pequeño conjunto de datos de sentimiento.
   **简单。**¿ Qué ?`apply_negation`Como un paso de pre-procesamiento añadido a un poco de aprendizaje en el flujo de agua, en un pequeño conjunto de datos de emociones, se mide la variación F1.
2. **Medium.**Implementar la regresión logística ponderada por clase (pasar `class_weight="balanced"`En el caso de los sistemas de cálculo, el resultado de la evaluación de los resultados de los resultados de los estudios de cálculo es el resultado de la evaluación de los resultados de los resultados de los resultados de los estudios de cálculo.
   **中等。**实现类别加权逻辑回归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅ en la composición de 90-10 类别不平衡上测量效果
3. **Hard.**Construye un detector de sarcasmo entrenando un segundo clasificador sobre los residuos del modelo de sentimiento. Documente su configuración experimental. Advierta al lector cuando su precisión esté por debajo de la casualidad (el nivel de probabilidad en el sarcasmo de 2 clases es de ~50%, y la mayoría de los primeros intentos aterrizan allí).
   **困难。**En el modelo emocional de residuos entrenar un segundo clasificador para construir un probador de pulsaciones. Registran su configuración de experimentación. Cuando su precisión es inferior al nivel de pulsación, advierta al lector.

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Términos clave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Más Leer más Leer más

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) la encuesta fundamental. Larga, pero las primeras cuatro secciones cubren todo lo clásico.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) el papel que mostró Bigrams + Naive Bayes es difícil de vencer en texto corto. / 证明二元组 + 朴素贝叶斯在短文本上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) referencia para `CountVectorizer`¿ Qué ?`TfidfVectorizer`, y cada botón que sintonizarás.`CountVectorizer`¿Qué es esto?`TfidfVectorizer`及你将调参的每个参数的参考──
